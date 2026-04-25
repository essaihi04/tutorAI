"""
Render Exam Pages — convertit les PDFs (sujet + correction) de chaque examen
en images JPEG page-par-page, dans le sous-dossier `pages/`.

Aucun appel API externe : 100 % PyMuPDF local, gratuit, ~1 s/page.

Structure produite (identique à SVT) :
    <subject>/<year>-<session>/pages/sujet_p1.jpg
    <subject>/<year>-<session>/pages/sujet_p2.jpg
    <subject>/<year>-<session>/pages/correction_p1.jpg
    ...

Usage :
    python backend/scripts/render_exam_pages.py mathematiques
    python backend/scripts/render_exam_pages.py mathematiques/2024-normale
    python backend/scripts/render_exam_pages.py --force mathematiques
    python backend/scripts/render_exam_pages.py --dpi 180 mathematiques

Prérequis : pip install PyMuPDF
"""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERREUR : PyMuPDF manquant. Installer avec : pip install PyMuPDF")
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent.parent
EXAMS_DIR = ROOT / "backend" / "data" / "exams"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("render_pages")


def _detect_pdfs(pdfs_dir: Path) -> tuple[Path | None, Path | None]:
    """Auto-detect sujet and correction PDFs from a pdfs/ folder by name pattern."""
    sujet_pdf: Path | None = None
    correction_pdf: Path | None = None
    for pdf in pdfs_dir.glob("*.pdf"):
        name = pdf.stem.lower()
        if any(k in name for k in ("corrig", "correction", "solution")):
            correction_pdf = pdf
        elif any(k in name for k in ("sujet", "enonce", "énoncé")):
            sujet_pdf = pdf
        elif sujet_pdf is None:
            sujet_pdf = pdf  # fallback: 1st non-correction PDF = sujet
    return sujet_pdf, correction_pdf


def render_pdf_pages(pdf_path: Path, out_dir: Path, prefix: str, dpi: int, force: bool) -> int:
    """Render each PDF page to JPEG. Skip existing files unless --force. Returns pages written."""
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    written = 0
    for i, page in enumerate(doc, 1):
        out_path = out_dir / f"{prefix}_p{i}.jpg"
        if out_path.exists() and not force:
            continue
        pix = page.get_pixmap(matrix=mat, alpha=False)
        pix.save(out_path, jpg_quality=85)
        written += 1
    doc.close()
    return written


def process_exam(exam_dir: Path, dpi: int, force: bool) -> bool:
    """Render sujet + correction for one exam folder. Returns True on success."""
    pdfs_dir = exam_dir / "pdfs"
    if not pdfs_dir.exists():
        logger.warning(f"[SKIP] {exam_dir.name} : dossier pdfs/ absent")
        return False

    sujet_pdf, correction_pdf = _detect_pdfs(pdfs_dir)
    if sujet_pdf is None:
        logger.warning(f"[SKIP] {exam_dir.name} : aucun PDF sujet trouvé")
        return False

    pages_dir = exam_dir / "pages"
    logger.info(f"[GO] {exam_dir.name}")
    logger.info(f"  sujet      : {sujet_pdf.name}")
    n_sujet = render_pdf_pages(sujet_pdf, pages_dir, "sujet", dpi, force)
    logger.info(f"    → {n_sujet} page(s) rendue(s)")

    if correction_pdf is not None:
        logger.info(f"  correction : {correction_pdf.name}")
        n_corr = render_pdf_pages(correction_pdf, pages_dir, "correction", dpi, force)
        logger.info(f"    → {n_corr} page(s) rendue(s)")
    else:
        logger.info(f"  correction : (aucun PDF de correction trouvé)")

    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("target", help="Dossier matière (ex : 'mathematiques') ou examen (ex : 'mathematiques/2024-normale')")
    parser.add_argument("--force", action="store_true", help="Re-rendre même si les JPEG existent déjà")
    parser.add_argument("--dpi", type=int, default=200, help="Résolution de rendu (défaut : 200 dpi ≈ ~1600px de large)")
    args = parser.parse_args()

    target = EXAMS_DIR / args.target
    if not target.exists():
        logger.error(f"Cible introuvable : {target}")
        return 1

    # Single exam folder vs subject root
    if (target / "pdfs").exists():
        exam_dirs = [target]
    else:
        exam_dirs = sorted([d for d in target.iterdir() if d.is_dir() and (d / "pdfs").exists()])

    if not exam_dirs:
        logger.error(f"Aucun examen avec pdfs/ trouvé sous {target}")
        return 1

    logger.info(f"Examens à rendre : {len(exam_dirs)} (dpi={args.dpi}, force={args.force})")
    ok = 0
    for d in exam_dirs:
        try:
            if process_exam(d, dpi=args.dpi, force=args.force):
                ok += 1
        except Exception as e:
            logger.error(f"[FAIL] {d.name} : {type(e).__name__} : {e}")

    logger.info(f"\nDONE : {ok}/{len(exam_dirs)} examens traités")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
