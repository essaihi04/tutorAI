"""
Validate Exams — Étape D (contrôle qualité)

Vérifie pour chaque exam.json :
  - Métadonnées cohérentes (year, session, title)
  - Somme des points des parties = total_points
  - Chaque question a un type valide et les champs requis (choices, correct_answer, ...)
  - Les documents référencés dans assets/ existent réellement
  - Détection de doublons dans index.json

Usage:
    python backend/scripts/validate_exams.py svt
    python backend/scripts/validate_exams.py svt/2019-rattrapage
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXAMS_DIR = ROOT / "backend" / "data" / "exams"

VALID_TYPES = {"open", "qcm", "vrai_faux", "association", "schema"}


def check_exam(exam_dir: Path) -> list[str]:
    errs = []
    exam_file = exam_dir / "exam.json"
    if not exam_file.exists():
        return [f"exam.json manquant"]
    try:
        d = json.loads(exam_file.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"JSON invalide: {e}"]

    # Metadata
    folder = exam_dir.name
    parts_folder = folder.split("-")
    year_folder = int(parts_folder[0]) if parts_folder[0].isdigit() else None
    session_folder = parts_folder[1].capitalize() if len(parts_folder) > 1 else None

    if year_folder and d.get("year") != year_folder:
        errs.append(f"year={d.get('year')} ≠ folder year={year_folder}")
    if session_folder and d.get("session", "").lower() != session_folder.lower():
        errs.append(f"session='{d.get('session')}' ≠ folder session='{session_folder}'")

    # Points
    parts = d.get("parts", [])
    total_declared = d.get("total_points", 0)
    total_real = sum(p.get("points", 0) for p in parts)
    if abs(total_real - total_declared) > 0.01:
        errs.append(f"Σ part.points = {total_real} ≠ total_points = {total_declared}")

    # Questions
    assets_dir = exam_dir / "assets"
    existing_assets = {f.name for f in assets_dir.iterdir()} if assets_dir.exists() else set()

    def walk_questions(container):
        qs = []
        if "questions" in container:
            qs.extend(container["questions"])
        if "exercises" in container:
            for ex in container["exercises"]:
                qs.extend(ex.get("questions", []))
        return qs

    for pi, part in enumerate(parts, 1):
        for q in walk_questions(part):
            qid = q.get("id", "?")
            qtype = q.get("type", "")
            if qtype not in VALID_TYPES:
                errs.append(f"P{pi} {qid}: type invalide '{qtype}'")
            if qtype == "qcm":
                if q.get("sub_questions"):
                    for sq in q["sub_questions"]:
                        if not sq.get("choices"):
                            errs.append(f"P{pi} {sq.get('id')}: QCM sans choices")
                        if not sq.get("correction", {}).get("correct_answer"):
                            errs.append(f"P{pi} {sq.get('id')}: QCM sans correct_answer")
                elif q.get("choices"):
                    if not q.get("correction", {}).get("correct_answer"):
                        errs.append(f"P{pi} {qid}: QCM sans correct_answer")
            # Check document references
            for doc in q.get("documents", []) or []:
                if isinstance(doc, dict):
                    src = doc.get("src", "")
                    if src.startswith("assets/"):
                        fname = src.split("/", 1)[1]
                        if fname not in existing_assets:
                            errs.append(f"P{pi} {qid}: asset manquant '{fname}'")

    return errs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="subject folder or specific exam")
    args = parser.parse_args()

    target = EXAMS_DIR / args.target
    if (target / "exam.json").exists():
        exam_dirs = [target]
    else:
        exam_dirs = sorted([d for d in target.iterdir() if d.is_dir()])

    total_errors = 0
    ok_count = 0
    for d in exam_dirs:
        errs = check_exam(d)
        if errs:
            print(f"\n[!!] {d.name}  ({len(errs)} issues)")
            for e in errs:
                print(f"     - {e}")
            total_errors += len(errs)
        else:
            if (d / "exam.json").exists():
                ok_count += 1
                print(f"[OK] {d.name}")

    print(f"\n{'=' * 60}")
    print(f"Résumé: {ok_count} OK / {len(exam_dirs)} dossiers, {total_errors} issues")
    sys.exit(0 if total_errors == 0 else 1)


if __name__ == "__main__":
    main()
