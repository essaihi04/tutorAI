"""
Ajoute les 20 entrées Physique (2016-2025, normale + rattrapage) dans
backend/data/exams/index.json, sans écraser les entrées SVT existantes.

Coefficients BAC 2BAC Sciences Physiques BIOF :
  - Physique-Chimie : coefficient 7, durée 4h = 240 min
  - Total points    : 20

Usage :
    python backend/scripts/_add_physique_index.py
"""
from __future__ import annotations

import json
from pathlib import Path

HERE = Path(__file__).resolve()
BACKEND = next(p for p in HERE.parents if (p / "data" / "exams").is_dir())
INDEX_PATH = BACKEND / "data" / "exams" / "index.json"
PHYSIQUE_DIR = BACKEND / "data" / "exams" / "physique"


def build_entry(year: int, session: str) -> dict:
    session_cap = "Normale" if session == "normale" else "Rattrapage"
    exam_id = f"physique_{year}_{session}"
    path = f"physique/{year}-{session}"
    title = f"Examen National du Baccalauréat - Physique-Chimie {year} {session_cap}"
    return {
        "id": exam_id,
        "subject": "Physique-Chimie",   # ↔ frontend SUBJECT_CONFIG.ExamHub
        "year": year,
        "session": session_cap,
        "path": path,
        "title": title,
        "subject_full": title,
        "duration_minutes": 240,   # 4h pour PC en 2BAC SP
        "coefficient": 7,          # coeff PC en 2BAC SP BIOF
        "total_points": 20,
        "note": "Il est permis d'utiliser la calculatrice non programmable",
    }


def main() -> int:
    # Load existing
    data = []
    if INDEX_PATH.exists():
        data = json.loads(INDEX_PATH.read_text(encoding="utf-8-sig"))
    print(f"  Index actuel : {len(data)} entrées")

    existing_ids = {e["id"] for e in data}
    added = 0
    skipped = 0

    for year in range(2016, 2026):
        for session in ("normale", "rattrapage"):
            entry = build_entry(year, session)

            # Vérifier que le dossier PDF existe bien
            pdf_dir = PHYSIQUE_DIR / f"{year}-{session}" / "pdfs"
            if not pdf_dir.exists():
                print(f"  ⚠ Dossier absent: {pdf_dir.relative_to(BACKEND)} — skip")
                continue

            pdf_count = len(list(pdf_dir.glob("*.pdf")))
            if pdf_count == 0:
                print(f"  ⚠ Aucun PDF dans {pdf_dir.relative_to(BACKEND)} — skip")
                continue

            if entry["id"] in existing_ids:
                print(f"  · {entry['id']:28s} déjà présent ({pdf_count} PDFs) — skip")
                skipped += 1
                continue

            data.append(entry)
            print(f"  + {entry['id']:28s} ajouté ({pdf_count} PDFs)")
            added += 1

    # Tri : année DESC, puis session, puis subject
    data.sort(key=lambda e: (-e.get("year", 0), e.get("session", ""), e.get("subject", "")))

    INDEX_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(
        f"\n━━━ RÉSULTAT ━━━\n"
        f"  + Ajoutées : {added}\n"
        f"  · Skipped  : {skipped}\n"
        f"  Total index final : {len(data)} entrées"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
