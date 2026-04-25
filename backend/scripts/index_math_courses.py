"""
Extract Math course(s) into the RAG cache.

The Math textbook has a native text layer, so we use PyMuPDF directly — no OCR,
no Mistral, no rate limits. Runs in ~1 second for 174 pages.

Writes `backend/data/rag_cache/math_rag_cache.json` in the same format as the
SVT cache (compatible with RAGService._index_single_source loader).

Usage:
    python backend/scripts/index_math_courses.py
    python backend/scripts/index_math_courses.py --status
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

import fitz  # PyMuPDF

MATH_DIR = BACKEND_DIR / "cours 2bac pc" / "Math"
CACHE_DIR = BACKEND_DIR / "data" / "rag_cache"
FINAL_CACHE = CACHE_DIR / "math_rag_cache.json"

CHUNK_TARGET = 900      # soft target chars per chunk
CHUNK_MAX = 1400        # hard upper bound


def pdf_hash(path: Path) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


def _clean(text: str) -> str:
    # Collapse excessive whitespace while preserving paragraph breaks.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _split_into_chunks(
    text: str, *, source: str, page: int, unit_info: str
) -> list[dict]:
    """Group paragraphs into chunks of ~CHUNK_TARGET chars, never > CHUNK_MAX."""
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[dict] = []
    current = ""
    for para in paragraphs:
        if len(para) > CHUNK_MAX:
            # flush current, emit oversize paragraph on its own (rare)
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


def extract_pdf(pdf: Path) -> list[dict]:
    """Extract every page into chunks. Returns list of chunk dicts."""
    doc = fitz.open(pdf)
    total_pages = doc.page_count
    source = pdf.stem
    unit_info = "Math"
    docs: list[dict] = []
    empty_pages = 0
    for idx, page in enumerate(doc):
        text = _clean(page.get_text("text"))
        if len(text) < 50:
            empty_pages += 1
            continue
        page_chunks = _split_into_chunks(
            text, source=source, page=idx + 1, unit_info=unit_info
        )
        docs.extend(page_chunks)
    doc.close()
    kept = total_pages - empty_pages
    print(f"  {pdf.name}: {len(docs)} chunks from {kept} pages"
          + (f" ({empty_pages} empty/skipped)" if empty_pages else ""))
    return docs


def build_cache() -> None:
    pdfs = sorted(MATH_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"No Math PDFs found in {MATH_DIR}")
        sys.exit(1)

    file_hashes: dict[str, str] = {}
    all_docs: list[dict] = []
    for pdf in pdfs:
        file_hashes[pdf.name] = pdf_hash(pdf)
        chunks = extract_pdf(pdf)
        for c in chunks:
            c["subject"] = "Mathematiques"
        all_docs.extend(chunks)

    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    FINAL_CACHE.write_text(
        json.dumps({"file_hashes": file_hashes, "documents": all_docs},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    size_mb = FINAL_CACHE.stat().st_size / 1_000_000
    print(f"\n✓ Wrote {FINAL_CACHE}")
    print(f"  {len(all_docs)} chunks, {size_mb:.1f} MB")


def status() -> None:
    if not FINAL_CACHE.exists():
        print("No Math cache yet. Run: python backend/scripts/index_math_courses.py")
        return
    data = json.loads(FINAL_CACHE.read_text(encoding="utf-8"))
    docs = data.get("documents", [])
    print(f"Math cache: {FINAL_CACHE}")
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
