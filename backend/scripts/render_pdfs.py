"""Render all exam PDFs to JPEG pages using PyMuPDF (no OCR).

Usage:
    python backend/scripts/render_pdfs.py                 # tous les examens sans pages/
    python backend/scripts/render_pdfs.py physique        # uniquement physique/*
    python backend/scripts/render_pdfs.py physique/2024-normale
    python backend/scripts/render_pdfs.py --force svt     # re-rendre même si pages/ existe
"""
import argparse
import logging
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERREUR: PyMuPDF manquant. pip install PyMuPDF")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent.parent
EXAMS_DIR = ROOT / "backend" / "data" / "exams"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("render_pdfs")


def classify_pdf(pdf: Path) -> str:
    n = pdf.stem.lower()
    if "corrig" in n or "correction" in n or "solution" in n:
        return "correction"
    return "sujet"


def render_pdf(pdf_path: Path, out_dir: Path, prefix: str, dpi: int = 200) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    count = 0
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(out_dir / f"{prefix}_p{i}.jpg", jpg_quality=85)
        count += 1
    doc.close()
    return count


def process_exam(exam_dir: Path, force: bool = False) -> bool:
    pdfs_dir = exam_dir / "pdfs"
    pages_dir = exam_dir / "pages"
    if not pdfs_dir.exists():
        return False
    pdfs = list(pdfs_dir.glob("*.pdf"))
    if not pdfs:
        return False
    existing = list(pages_dir.glob("*.jpg")) if pages_dir.exists() else []
    if existing and not force:
        logger.info(f"[SKIP] {exam_dir.parent.name}/{exam_dir.name} ({len(existing)} pages existantes)")
        return False

    # Group by kind. Heuristic: if there are exactly 2 PDFs and only one is
    # classified as 'sujet' by keyword, treat the other as 'correction' even
    # if its filename doesn't contain 'corrige'.
    groups: dict[str, Path] = {}
    if len(pdfs) == 2:
        has_sujet_kw = [("sujet" in p.stem.lower() or "enonce" in p.stem.lower() or "énoncé" in p.stem.lower()) for p in pdfs]
        has_corr_kw = [("corrig" in p.stem.lower() or "correction" in p.stem.lower() or "solution" in p.stem.lower()) for p in pdfs]
        if sum(has_sujet_kw) == 1 and sum(has_corr_kw) == 0:
            # Exactly one is a sujet; the other must be the correction
            for p, is_sujet in zip(pdfs, has_sujet_kw):
                groups["sujet" if is_sujet else "correction"] = p
    if not groups:
        for p in pdfs:
            kind = classify_pdf(p)
            if kind not in groups or p.stat().st_size > groups[kind].stat().st_size:
                groups[kind] = p

    total = 0
    for kind, pdf in groups.items():
        n = render_pdf(pdf, pages_dir, kind)
        total += n
        logger.info(f"  {pdf.name} → {n} pages ({kind})")
    logger.info(f"[OK] {exam_dir.parent.name}/{exam_dir.name}: {total} pages")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("target", nargs="?", default="", help="subject, subject/exam, ou vide pour tout")
    ap.add_argument("--force", action="store_true")
    args = ap.parse_args()

    targets: list[Path] = []
    if not args.target:
        for subj in sorted(EXAMS_DIR.iterdir()):
            if subj.is_dir():
                targets += [e for e in sorted(subj.iterdir()) if e.is_dir()]
    elif "/" in args.target or "\\" in args.target:
        targets = [EXAMS_DIR / args.target.replace("\\", "/")]
    else:
        subj = EXAMS_DIR / args.target
        if subj.is_dir():
            targets = [e for e in sorted(subj.iterdir()) if e.is_dir()]

    logger.info(f"Examens à traiter: {len(targets)}")
    done = 0
    for t in targets:
        if process_exam(t, force=args.force):
            done += 1
    logger.info(f"DONE: {done}/{len(targets)} rendus")


if __name__ == "__main__":
    main()
