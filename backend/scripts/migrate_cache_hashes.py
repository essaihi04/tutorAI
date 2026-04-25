"""
One-shot migration: normalize file_hashes in RAG caches to the full MD5
hexdigest format that RAGService._get_pdf_hash expects.

Rewrites:
  backend/data/rag_cache/math_rag_cache.json
  backend/data/rag_cache/pc_rag_cache.json
  backend/data/rag_cache/svt_rag_cache.json

Safe to re-run; preserves all documents.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
CACHE_DIR = BACKEND_DIR / "data" / "rag_cache"

# Map cache filename -> folder under `cours 2bac pc/` holding the PDFs
CACHES = [
    ("math_rag_cache.json", BACKEND_DIR / "cours 2bac pc" / "Math"),
    ("pc_rag_cache.json", BACKEND_DIR / "cours 2bac pc" / "PC"),
    ("svt_rag_cache.json", BACKEND_DIR / "cours 2bac pc" / "SVT"),
]


def full_md5(path: Path) -> str:
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()


def migrate(cache_file: Path, pdf_dir: Path) -> None:
    if not cache_file.exists():
        print(f"[skip] {cache_file.name}: cache not found")
        return
    if not pdf_dir.exists():
        print(f"[skip] {cache_file.name}: pdf dir {pdf_dir} not found")
        return

    data = json.loads(cache_file.read_text(encoding="utf-8"))
    old = data.get("file_hashes", {})
    new: dict[str, str] = {}
    for pdf in sorted(pdf_dir.glob("*.pdf")):
        new[pdf.name] = full_md5(pdf)

    missing_in_cache = sorted(set(new) - set(old))
    extra_in_cache = sorted(set(old) - set(new))
    changed = sum(1 for k in new if old.get(k) != new[k])

    data["file_hashes"] = new
    cache_file.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    docs = len(data.get("documents", []))
    print(f"[OK]  {cache_file.name}: {len(new)} hashes ({changed} changed), "
          f"{docs} chunks preserved")
    if missing_in_cache:
        print(f"       NEW PDFs not yet extracted: {missing_in_cache}")
    if extra_in_cache:
        print(f"       Removed from disk but still in cache: {extra_in_cache}")


def main() -> None:
    print(f"Cache dir: {CACHE_DIR}\n")
    for name, pdf_dir in CACHES:
        migrate(CACHE_DIR / name, pdf_dir)


if __name__ == "__main__":
    main()
