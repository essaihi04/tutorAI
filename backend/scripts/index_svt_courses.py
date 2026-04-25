"""
Extract SVT courses (scanned PDFs) via Mistral OCR and build the RAG cache.

Robust, resumable CLI:
    python backend/scripts/index_svt_courses.py --pdf Cours-Unit1-1.pdf   # one file
    python backend/scripts/index_svt_courses.py --all                      # every SVT PDF
    python backend/scripts/index_svt_courses.py --all --resume             # skip already-done pages
    python backend/scripts/index_svt_courses.py --status                   # progress report

Design notes:
- Uses Mistral OCR (`mistral-ocr-latest`) — returns structured markdown with
  preserved tables, formulas and layout, no prompt engineering needed.
- Pages are OCR'ed one-at-a-time with a short throttle (1.2s) to stay under
  the free-tier rate limit of ~1 req/s.
- Each page is persisted immediately to `data/rag_cache/svt_partial/<pdf>.json`
  so Ctrl+C loses at most the current page.
- When a PDF is fully done (all pages extracted), chunks are built and appended
  to `data/rag_cache/svt_rag_cache.json` in the format RAGService expects.
- On 429 rate-limit we back off 10s → 30s → 60s → 120s (4 tries).
- Bypasses the global RAG_DISABLED kill-switch by calling OCR directly.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
import time
from pathlib import Path

# Ensure we can import app.* even when run from repo root
BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

# We deliberately force RAG_DISABLED=0 for THIS process only so the OCR helper
# does real work even if the env file disables it globally.
os.environ["RAG_DISABLED"] = "0"

import fitz  # PyMuPDF
import httpx

from app.config import get_settings

settings = get_settings()

SVT_DIR = BACKEND_DIR / "cours 2bac pc" / "SVT"
CACHE_DIR = BACKEND_DIR / "data" / "rag_cache"
PARTIAL_DIR = CACHE_DIR / "svt_partial"
FINAL_CACHE = CACHE_DIR / "svt_rag_cache.json"

# Throttling — Mistral OCR free tier ≈ 1 req/s
SLEEP_BETWEEN_PAGES = 1.2
RATE_LIMIT_BACKOFFS = [10, 30, 60, 120]
MAX_RETRIES_PER_PAGE = len(RATE_LIMIT_BACKOFFS)

MISTRAL_OCR_URL = "https://api.mistral.ai/v1/ocr"
MISTRAL_OCR_MODEL = "mistral-ocr-latest"


# ─────────────────────── helpers ───────────────────────

def _pdf_hash(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _partial_path(pdf: Path) -> Path:
    return PARTIAL_DIR / f"{pdf.stem}.json"


def _load_partial(pdf: Path) -> dict:
    p = _partial_path(pdf)
    if p.exists():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"pdf": pdf.name, "hash": _pdf_hash(pdf), "pages": {}}


def _save_partial(pdf: Path, state: dict) -> None:
    PARTIAL_DIR.mkdir(parents=True, exist_ok=True)
    tmp = _partial_path(pdf).with_suffix(".json.tmp")
    tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(_partial_path(pdf))


# ─────────────────────── OCR ───────────────────────

def ocr_page(api_key: str, img_bytes: bytes, label: str, mime: str = "image/png") -> tuple[str, str]:
    """
    OCR one page via Mistral OCR. Returns (text, status).
    status ∈ {"ok", "empty", "rate_limited", "error"}
    """
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

    for attempt in range(MAX_RETRIES_PER_PAGE):
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
            wait = RATE_LIMIT_BACKOFFS[attempt]
            print(f"    ! 429 rate-limited on {label} — sleeping {wait}s (try {attempt + 1}/{MAX_RETRIES_PER_PAGE})")
            time.sleep(wait)
            continue

        # other HTTP error
        print(f"    ! HTTP {r.status_code} on {label}: {r.text[:300]}")
        if r.status_code in (401, 403):
            # bad key — don't hammer
            return "", "error"
        time.sleep(5)

    return "", "rate_limited"


# ─────────────────────── per-PDF pipeline ───────────────────────

def process_pdf(pdf: Path, resume: bool, api_key: str) -> dict:
    state = _load_partial(pdf) if resume else {
        "pdf": pdf.name, "hash": _pdf_hash(pdf), "pages": {}
    }
    # Invalidate if PDF changed
    if state.get("hash") != _pdf_hash(pdf):
        print(f"  ! PDF {pdf.name} changed since last run — restarting from scratch")
        state = {"pdf": pdf.name, "hash": _pdf_hash(pdf), "pages": {}}

    doc = fitz.open(pdf)
    total = doc.page_count
    done = sum(1 for v in state["pages"].values() if v.get("status") in ("ok", "empty"))
    print(f"  {pdf.name}: {total} pages — {done} already done")

    for idx in range(total):
        key = str(idx + 1)
        prev = state["pages"].get(key, {})
        if prev.get("status") in ("ok", "empty"):
            continue

        page = doc[idx]
        mat = fitz.Matrix(2, 2)
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")

        label = f"{pdf.stem} p.{idx + 1}/{total}"
        text, status = ocr_page(api_key, img_bytes, label)
        state["pages"][key] = {"text": text, "status": status, "chars": len(text)}
        _save_partial(pdf, state)
        marker = {"ok": "✓", "empty": "·", "rate_limited": "✗", "error": "!"}.get(status, "?")
        print(f"    {marker} p{idx + 1}/{total}: {len(text):5d} chars [{status}]")

        # be polite between calls
        if idx < total - 1:
            time.sleep(SLEEP_BETWEEN_PAGES)

    doc.close()
    return state


# ─────────────────────── build final cache ───────────────────────

def build_chunks_for_pdf(pdf_name: str, state: dict) -> list[dict]:
    """Convert per-page OCR state into RAG chunks (same shape as extract_pdf_content)."""
    stem = pdf_name.replace(".pdf", "")
    parts = stem.replace("Cours-", "").split("-")
    unit_info = parts[0] if parts else "Unknown"

    chunks: list[dict] = []
    for page_key in sorted(state["pages"].keys(), key=lambda s: int(s)):
        info = state["pages"][page_key]
        text = (info.get("text") or "").strip()
        if not text:
            continue
        page_num = int(page_key)
        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
        current = ""
        for para in paragraphs:
            if len(current) + len(para) < 1000:
                current = f"{current}\n{para}" if current else para
            else:
                if current:
                    chunks.append({
                        "text": current, "source": stem, "page": page_num,
                        "unit": unit_info, "type": "text",
                    })
                current = para
        if current:
            chunks.append({
                "text": current, "source": stem, "page": page_num,
                "unit": unit_info, "type": "text",
            })
    return chunks


def rebuild_final_cache() -> None:
    """Merge all partial states into the RAG cache format."""
    if not PARTIAL_DIR.exists():
        print("No partial data to merge.")
        return

    file_hashes: dict[str, str] = {}
    all_docs: list[dict] = []
    for partial in sorted(PARTIAL_DIR.glob("*.json")):
        state = json.loads(partial.read_text(encoding="utf-8"))
        pdf_name = state["pdf"]
        file_hashes[pdf_name] = state.get("hash", "")
        chunks = build_chunks_for_pdf(pdf_name, state)
        for c in chunks:
            c["subject"] = "SVT"
        all_docs.extend(chunks)
        print(f"  · {pdf_name}: {len(chunks)} chunks")

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_CACHE.write_text(
        json.dumps({"file_hashes": file_hashes, "documents": all_docs},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nFinal cache written: {FINAL_CACHE}")
    print(f"Total SVT chunks: {len(all_docs)}")


def print_status() -> None:
    pdfs = sorted(SVT_DIR.glob("*.pdf"))
    if not pdfs:
        print("No SVT PDFs found.")
        return
    total_pages = 0
    total_done = 0
    total_rate_limited = 0
    for pdf in pdfs:
        doc = fitz.open(pdf)
        n = doc.page_count
        doc.close()
        state = _load_partial(pdf)
        done = sum(1 for v in state["pages"].values() if v.get("status") in ("ok", "empty"))
        rl = sum(1 for v in state["pages"].values() if v.get("status") == "rate_limited")
        total_pages += n
        total_done += done
        total_rate_limited += rl
        bar_len = 30
        filled = int(bar_len * done / n) if n else 0
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"  {pdf.name:24s} [{bar}] {done:3d}/{n:<3d}"
              + (f"  ({rl} rate-limited)" if rl else ""))
    pct = 100 * total_done / total_pages if total_pages else 0
    print(f"\n  Total: {total_done}/{total_pages} pages ({pct:.1f}%)")
    if total_rate_limited:
        print(f"  Rate-limited pages (need retry): {total_rate_limited}")


# ─────────────────────── main ───────────────────────

def main():
    parser = argparse.ArgumentParser(description="Index SVT courses for RAG")
    parser.add_argument("--pdf", help="Process one specific PDF (filename)")
    parser.add_argument("--all", action="store_true", help="Process every SVT PDF")
    parser.add_argument("--resume", action="store_true", default=True,
                        help="Resume from partial state (default: on)")
    parser.add_argument("--no-resume", dest="resume", action="store_false",
                        help="Ignore partial state and restart each PDF")
    parser.add_argument("--status", action="store_true", help="Show progress and exit")
    parser.add_argument("--rebuild-cache", action="store_true",
                        help="Rebuild svt_rag_cache.json from partial files and exit")
    args = parser.parse_args()

    if args.status:
        print_status()
        return

    if args.rebuild_cache:
        rebuild_final_cache()
        return

    api_key = (settings.mistral_api_key or os.getenv("MISTRAL_API_KEY", "")).strip()
    if not api_key:
        print("ERROR: MISTRAL_API_KEY is not configured (backend/.env).")
        sys.exit(1)

    if args.pdf:
        target = SVT_DIR / args.pdf
        if not target.exists():
            print(f"Not found: {target}")
            sys.exit(1)
        targets = [target]
    elif args.all:
        targets = sorted(SVT_DIR.glob("*.pdf"))
    else:
        parser.print_help()
        return

    print(f"Processing {len(targets)} PDF(s)  (throttle {SLEEP_BETWEEN_PAGES}s/page)")
    for pdf in targets:
        print(f"\n>>> {pdf.name}")
        process_pdf(pdf, args.resume, api_key)

    print("\nRebuilding final cache...")
    rebuild_final_cache()


if __name__ == "__main__":
    main()
