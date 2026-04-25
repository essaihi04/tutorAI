"""
Extract Physique-Chimie courses into the RAG cache.

Most PC PDFs have native text (instant extraction via PyMuPDF).
If a PDF is scanned (no text layer), falls back to Mistral OCR.

Writes `backend/data/rag_cache/pc_rag_cache.json` in the same format as
SVT/Math caches (compatible with RAGService._index_single_source loader).

Usage:
    python backend/scripts/index_pc_courses.py
    python backend/scripts/index_pc_courses.py --status
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import fitz  # PyMuPDF
import httpx

from app.config import get_settings

settings = get_settings()

PC_DIR = BACKEND_DIR / "cours 2bac pc" / "PC"
CACHE_DIR = BACKEND_DIR / "data" / "rag_cache"
FINAL_CACHE = CACHE_DIR / "pc_rag_cache.json"
PARTIAL_DIR = CACHE_DIR / "pc_partial"

CHUNK_TARGET = 900
CHUNK_MAX = 1400

# Mistral OCR for scanned PDFs
MISTRAL_OCR_URL = "https://api.mistral.ai/v1/ocr"
MISTRAL_OCR_MODEL = "mistral-ocr-latest"
OCR_THROTTLE = 1.2
OCR_BACKOFFS = [10, 30, 60, 120]
MAX_OCR_RETRIES = len(OCR_BACKOFFS)


def pdf_hash(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _clean(text: str) -> str:
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _split_into_chunks(
    text: str, *, source: str, page: int, unit_info: str
) -> list[dict]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[dict] = []
    current = ""
    for para in paragraphs:
        if len(para) > CHUNK_MAX:
            if current:
                chunks.append({"text": current, "source": source, "page": page,
                               "unit": unit_info, "type": "text"})
                current = ""
            chunks.append({"text": para, "source": source, "page": page,
                           "unit": unit_info, "type": "text"})
            continue
        if not current:
            current = para
        elif len(current) + len(para) + 1 <= CHUNK_TARGET:
            current += "\n" + para
        else:
            chunks.append({"text": current, "source": source, "page": page,
                           "unit": unit_info, "type": "text"})
            current = para
    if current:
        chunks.append({"text": current, "source": source, "page": page,
                       "unit": unit_info, "type": "text"})
    return chunks


def _partial_path(pdf: Path) -> Path:
    return PARTIAL_DIR / f"{pdf.name}.json"


def _load_partial(pdf: Path) -> dict:
    path = _partial_path(pdf)
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _save_partial(pdf: Path, state: dict) -> None:
    PARTIAL_DIR.mkdir(parents=True, exist_ok=True)
    tmp = _partial_path(pdf).with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(_partial_path(pdf))


def _ocr_page(api_key: str, img_bytes: bytes, label: str, mime: str = "image/png") -> tuple[str, str]:
    """OCR via Mistral. Returns (markdown, status)."""
    image_b64 = base64.b64encode(img_bytes).decode("utf-8")
    payload = {
        "model": MISTRAL_OCR_MODEL,
        "document": {
            "type": "image_url",
            "image_url": f"data:{mime};base64,{image_b64}",
        },
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    for attempt in range(MAX_OCR_RETRIES):
        try:
            r = httpx.post(MISTRAL_OCR_URL, headers=headers, json=payload, timeout=120.0)
        except Exception as e:
            print(f"    ! network error ({e}); retry in 10s")
            time.sleep(10)
            continue
        if r.status_code == 200:
            try:
                data = r.json()
                pages = data.get("pages", [])
                md = "\n\n".join(
                    p.get("markdown", "") for p in pages if isinstance(p, dict)
                ).strip()
            except Exception:
                md = ""
            if len(md) > 10:
                return md, "ok"
            return md, "empty"
        if r.status_code == 429:
            wait = OCR_BACKOFFS[attempt]
            print(f"    ! 429 rate-limited on {label} — sleeping {wait}s")
            time.sleep(wait)
            continue
        print(f"    ! HTTP {r.status_code} on {label}: {r.text[:300]}")
        if r.status_code in (401, 403):
            return "", "error"
        time.sleep(5)
    return "", "rate_limited"


def extract_with_ocr(pdf: Path, api_key: str) -> list[dict]:
    """Extract scanned PDF via page-by-page OCR (resumable)."""
    source = pdf.stem
    state = _load_partial(pdf) or {
        "pdf": pdf.name, "hash": pdf_hash(pdf), "pages": {}
    }
    doc = fitz.open(pdf)
    total = doc.page_count
    done = len(state["pages"])
    print(f"  {pdf.name}: {total} pages — {done} already done (OCR mode)")
    chunks: list[dict] = []
    for idx in range(done, total):
        page = doc[idx]
        pix = page.get_pixmap(dpi=150)
        img_bytes = pix.tobytes("png")
        label = f"p{idx + 1}/{total}"
        text, status = _ocr_page(api_key, img_bytes, label, "image/png")
        if status == "ok":
            state["pages"][idx] = text
            _save_partial(pdf, state)
            print(f"    ✓ {label}: {len(text)} chars [ok]")
            time.sleep(OCR_THROTTLE)
        elif status == "empty":
            state["pages"][idx] = ""
            _save_partial(pdf, state)
            print(f"    ○ {label}: empty")
            time.sleep(OCR_THROTTLE)
        elif status == "rate_limited":
            print(f"    ✗ {label}: rate-limited after retries — resume later")
            doc.close()
            return []
        else:  # error
            print(f"    ✗ {label}: error — skipping page")
            state["pages"][idx] = ""
            _save_partial(pdf, state)
    doc.close()
    for idx, text in state["pages"].items():
        if text and len(text) > 10:
            page_chunks = _split_into_chunks(
                text, source=source, page=int(idx) + 1, unit_info="Physique-Chimie"
            )
            chunks.extend(page_chunks)
    print(f"  → {len(chunks)} chunks extracted")
    return chunks


def extract_native(pdf: Path) -> list[dict]:
    """Extract PDF with native text layer (instant)."""
    doc = fitz.open(pdf)
    total = doc.page_count
    source = pdf.stem
    chunks: list[dict] = []
    empty = 0
    for idx, page in enumerate(doc):
        text = _clean(page.get_text("text"))
        if len(text) < 50:
            empty += 1
            continue
        page_chunks = _split_into_chunks(
            text, source=source, page=idx + 1, unit_info="Physique-Chimie"
        )
        chunks.extend(page_chunks)
    doc.close()
    kept = total - empty
    print(f"  {pdf.name}: {len(chunks)} chunks from {kept} pages"
          + (f" ({empty} empty/skipped)" if empty else ""))
    return chunks


def build_cache() -> None:
    pdfs = sorted(PC_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No PC PDFs found in {PC_DIR}")
        sys.exit(1)

    api_key = (settings.mistral_api_key or os.getenv("MISTRAL_API_KEY", "")).strip()
    if not api_key:
        print("WARNING: MISTRAL_API_KEY not set — scanned PDFs will be skipped")
        api_key = None

    file_hashes: dict[str, str] = {}
    all_docs: list[dict] = []
    scanned_count = 0
    for pdf in pdfs:
        file_hashes[pdf.name] = pdf_hash(pdf)
        # Check if scanned (no text layer)
        doc = fitz.open(pdf)
        has_text = any(len(page.get_text("text").strip()) > 50 for page in doc)
        doc.close()
        if not has_text:
            scanned_count += 1
            if api_key:
                chunks = extract_with_ocr(pdf, api_key)
                if not chunks:
                    print(f"  {pdf.name}: OCR failed or interrupted — skipping")
                    continue
            else:
                print(f"  {pdf.name}: scanned but no OCR key — skipping")
                continue
        else:
            chunks = extract_native(pdf)
        for c in chunks:
            c["subject"] = "Physique-Chimie"
        all_docs.extend(chunks)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_CACHE.write_text(
        json.dumps({"file_hashes": file_hashes, "documents": all_docs},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    size_mb = FINAL_CACHE.stat().st_size / 1_000_000
    print(f"\n✓ Wrote {FINAL_CACHE}")
    print(f"  {len(all_docs)} chunks from {len(pdfs) - scanned_count} native + {scanned_count} scanned PDFs")
    print(f"  {size_mb:.1f} MB")


def status() -> None:
    if not FINAL_CACHE.exists():
        print("No PC cache yet. Run: python backend/scripts/index_pc_courses.py")
        return
    data = json.loads(FINAL_CACHE.read_text(encoding="utf-8"))
    docs = data.get("documents", [])
    print(f"PC cache: {FINAL_CACHE}")
    print(f"  {len(docs)} chunks")
    by_source: dict[str, int] = {}
    for d in docs:
        by_source[d.get("source", "?")] = by_source.get(d.get("source", "?"), 0) + 1
    for s, n in by_source.items():
        print(f"  · {s}: {n} chunks")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()
    if args.status:
        status()
    else:
        build_cache()


if __name__ == "__main__":
    main()
