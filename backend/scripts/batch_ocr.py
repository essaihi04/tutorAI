"""
Batch OCR Pipeline — Étape A

Pour chaque examen contenant `pdfs/sujet.pdf` (et éventuellement `pdfs/correction.pdf`)
mais sans `extraction.json` :

1. Rend chaque page du PDF en JPEG via PyMuPDF → `pages/sujet_pN.jpg`
2. Appelle Mistral OCR sur chaque page en parallèle (asyncio.gather)
3. Concatène le texte et écrit `extraction.json` partiel

Usage:
    python backend/scripts/batch_ocr.py svt                    # tous les dossiers svt/*
    python backend/scripts/batch_ocr.py svt/2019-rattrapage    # un seul dossier
    python backend/scripts/batch_ocr.py --force svt            # re-traiter même si extraction.json existe

Prérequis:
    pip install PyMuPDF httpx python-dotenv
"""
import argparse
import asyncio
import base64
import io
import json
import logging
import os
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

try:
    import fitz  # PyMuPDF
except ImportError:
    print("ERREUR: PyMuPDF manquant. Installer avec: pip install PyMuPDF")
    sys.exit(1)

# Load env
ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / "backend" / ".env")

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "").strip()
MISTRAL_OCR_URL = "https://api.mistral.ai/v1/ocr"
MISTRAL_OCR_MODEL = "mistral-ocr-latest"

EXAMS_DIR = ROOT / "backend" / "data" / "exams"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("batch_ocr")

# Concurrence limitée (Mistral free tier ~2 req/s)
MAX_CONCURRENT_OCR = 4
SEM = asyncio.Semaphore(MAX_CONCURRENT_OCR)


def pdf_to_page_images(pdf_path: Path, out_dir: Path, prefix: str, dpi: int = 200) -> list[Path]:
    """Render each PDF page to JPEG using PyMuPDF. Returns list of output paths."""
    out_dir.mkdir(parents=True, exist_ok=True)
    doc = fitz.open(pdf_path)
    zoom = dpi / 72
    mat = fitz.Matrix(zoom, zoom)
    paths = []
    for i, page in enumerate(doc, 1):
        pix = page.get_pixmap(matrix=mat, alpha=False)
        out_path = out_dir / f"{prefix}_p{i}.jpg"
        pix.save(out_path, jpg_quality=85)
        paths.append(out_path)
    doc.close()
    logger.info(f"  {pdf_path.name}: {len(paths)} pages rendered → {out_dir.name}/")
    return paths


async def ocr_image(client: httpx.AsyncClient, img_path: Path) -> tuple[Path, str]:
    """Call Mistral OCR on one image. Returns (path, markdown)."""
    async with SEM:
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        payload = {
            "model": MISTRAL_OCR_MODEL,
            "document": {"type": "image_url", "image_url": f"data:image/jpeg;base64,{b64}"},
        }
        headers = {
            "Authorization": f"Bearer {MISTRAL_API_KEY}",
            "Content-Type": "application/json",
        }
        try:
            r = await client.post(MISTRAL_OCR_URL, headers=headers, json=payload, timeout=120.0)
            r.raise_for_status()
            data = r.json()
            pages = data.get("pages", [])
            md = "\n\n".join(p.get("markdown", "") for p in pages if isinstance(p, dict))
            logger.info(f"    OCR {img_path.name}: {len(md)} chars")
            return img_path, md
        except Exception as e:
            logger.error(f"    OCR FAILED {img_path.name}: {type(e).__name__}: {e}")
            return img_path, ""


async def process_exam(exam_dir: Path, force: bool = False) -> bool:
    """Process one exam folder. Returns True if extraction.json was (re)created.

    Priorité :
    1. Si `pages/sujet_p*.jpg` existe déjà → on OCR directement (pas besoin de PDFs)
    2. Sinon, on rend les PDFs via PyMuPDF puis on OCR
    """
    extraction_file = exam_dir / "extraction.json"
    pages_dir = exam_dir / "pages"
    pdfs_dir = exam_dir / "pdfs"

    if extraction_file.exists() and not force:
        logger.info(f"[SKIP] {exam_dir.name}: extraction.json existe déjà (utilisez --force)")
        return False

    sujet_pages: list[Path] = []
    correction_pages: list[Path] = []

    # PRIORITY 1: Use existing pages/*.jpg if available
    if pages_dir.exists():
        existing = sorted(pages_dir.glob("*.jp*g")) + sorted(pages_dir.glob("*.png"))
        for p in existing:
            name_lower = p.stem.lower()
            if name_lower.startswith("correction") or "corrig" in name_lower:
                correction_pages.append(p)
            elif name_lower.startswith("sujet") or "enonce" in name_lower or "énoncé" in name_lower:
                sujet_pages.append(p)
        if sujet_pages:
            logger.info(f"  pages/ existe: {len(sujet_pages)} sujet + {len(correction_pages)} correction (JPEG/PNG)")

    # PRIORITY 2: Render from PDFs if no pages found
    if not sujet_pages:
        if not pdfs_dir.exists():
            logger.warning(f"[SKIP] {exam_dir.name}: ni pages/ ni pdfs/ trouvés")
            return False

        sujet_pdf = None
        correction_pdf = None
        all_pdfs = list(pdfs_dir.glob("*.pdf"))
        for pdf in all_pdfs:
            name_lower = pdf.stem.lower()
            if "corrig" in name_lower or "correction" in name_lower or "solution" in name_lower:
                correction_pdf = pdf
            elif "sujet" in name_lower or "enonce" in name_lower or "énoncé" in name_lower:
                sujet_pdf = pdf
            elif sujet_pdf is None:
                sujet_pdf = pdf

        # Heuristic: if exactly 2 PDFs, sujet identified but no correction keyword,
        # treat the other PDF as correction
        if sujet_pdf is not None and correction_pdf is None and len(all_pdfs) == 2:
            for pdf in all_pdfs:
                if pdf != sujet_pdf:
                    correction_pdf = pdf
                    break

        if sujet_pdf is None:
            logger.warning(f"[SKIP] {exam_dir.name}: aucun PDF sujet trouvé dans pdfs/")
            return False

        logger.info(f"  Rendu PDF: sujet={sujet_pdf.name}" + (f", correction={correction_pdf.name}" if correction_pdf else ""))
        sujet_pages = pdf_to_page_images(sujet_pdf, pages_dir, "sujet")
        if correction_pdf is not None and correction_pdf.exists():
            correction_pages = pdf_to_page_images(correction_pdf, pages_dir, "correction")

    logger.info(f"[GO] {exam_dir.name}: OCR {len(sujet_pages)} sujet + {len(correction_pages)} correction pages")

    # OCR all pages in parallel
    async with httpx.AsyncClient() as client:
        tasks = [ocr_image(client, p) for p in sujet_pages + correction_pages]
        results = await asyncio.gather(*tasks)

    # Aggregate by source
    sujet_texts = []
    correction_texts = []
    for path, md in results:
        if "sujet" in path.name:
            sujet_texts.append(md)
        else:
            correction_texts.append(md)

    sujet_text = "\n\n".join(sujet_texts)
    correction_text = "\n\n".join(correction_texts)

    # Extract year + session from folder name
    folder = exam_dir.name  # e.g. "2019-rattrapage"
    parts = folder.split("-")
    year = int(parts[0]) if parts[0].isdigit() else 0
    session = parts[1].capitalize() if len(parts) > 1 else "Normale"

    # Extract subject from parent folder (svt, mathematiques, physique-chimie, ...)
    subject_slug = exam_dir.parent.name.lower()
    subject_display_map = {
        "svt": "SVT",
        "mathematiques": "Mathématiques",
        "mathematique": "Mathématiques",
        "math": "Mathématiques",
        "physique-chimie": "Physique-Chimie",
        "physique": "Physique",
        "chimie": "Chimie",
    }
    subject_display = subject_display_map.get(subject_slug, subject_slug.capitalize())

    # Write extraction.json
    package = {
        "exam_id": f"{subject_slug}_{year}_{session.lower()}",
        "subject": subject_slug,
        "year": year,
        "session": session,
        "title": f"Examen National du Baccalauréat - {subject_display} {year} {session}",
        "sujet_text": sujet_text,
        "correction_text": correction_text,
        "documents": [],  # Rempli plus tard par batch_build_json.py
        "pages_rendered": {
            "sujet": [p.name for p in sujet_pages],
            "correction": [p.name for p in correction_pages],
        },
    }
    extraction_file.write_text(json.dumps(package, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"  [OK] extraction.json: sujet={len(sujet_text)} chars, correction={len(correction_text)} chars")
    return True


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="subject folder (e.g. 'svt') or specific exam (e.g. 'svt/2019-rattrapage')")
    parser.add_argument("--force", action="store_true", help="Re-process even if extraction.json exists")
    args = parser.parse_args()

    if not MISTRAL_API_KEY:
        logger.error("MISTRAL_API_KEY manquante dans backend/.env")
        sys.exit(1)

    target = EXAMS_DIR / args.target
    if not target.exists():
        logger.error(f"Cible introuvable: {target}")
        sys.exit(1)

    # Determine list of exam folders
    if (target / "pdfs").exists() or (target / "exam.json").exists():
        exam_dirs = [target]
    else:
        # Subject root: iterate all exam folders
        exam_dirs = sorted([d for d in target.iterdir() if d.is_dir()])

    logger.info(f"Exams à traiter: {len(exam_dirs)}")
    processed = 0
    for d in exam_dirs:
        try:
            ok = await process_exam(d, force=args.force)
            if ok:
                processed += 1
        except Exception as e:
            logger.error(f"[FAIL] {d.name}: {type(e).__name__}: {e}")

    logger.info(f"\nDONE: {processed}/{len(exam_dirs)} examens traités")


if __name__ == "__main__":
    asyncio.run(main())
