"""Copie les sujets du national vers le frontend, pour la feuille d'examen.

    python scripts/examens/copier_sujets.py                 # tous les sujets
    python scripts/examens/copier_sujets.py physique/2024-normale svt/2022-normale
    python scripts/examens/copier_sujets.py --liste physique/2024-normale   # exercices et figures

`backend/data` n'est pas servi au frontend : la feuille d'examen
(`frontend/public/media/simulations/shared/examen/feuille.html`) lit une copie allégée

    frontend/public/media/examens/<matière>/<année>-<session>.json        (énoncé seul, sans corrigé)
    frontend/public/media/examens/<matière>/<année>-<session>/assets/...  (figures découpées utilisées)

Le JSON garde la forme de `exam.json` (parts[].exercises[].questions[]), sans `correction`,
`correct_answer` ni `correct_pairs`, et ajoute :
    sujet        "physique/2024-normale"
    code         "NS 28F" (NS normale / RS rattrapage ; 28 physique-chimie, 34 SVT, 22 maths)
    pages_sujet  nombre de pages du sujet (scans pages/sujet_pN.jpg)
    exercices    la liste à plat (n° utilisé par `?exercice=<n>`) : nom, points, nombre de questions
Les chemins `src` des documents deviennent absolus (`/media/examens/.../assets/x.png`).
"""
from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
SOURCE = RACINE / "backend" / "data" / "exams"
CIBLE = RACINE / "frontend" / "public" / "media" / "examens"
CODES = {"physique": "28", "svt": "34", "mathematiques": "22"}
SECRETS = {"correction", "correct_answer", "correct_pairs"}


def nettoyer(o):
    if isinstance(o, dict):
        return {k: nettoyer(v) for k, v in o.items() if k not in SECRETS}
    if isinstance(o, list):
        return [nettoyer(v) for v in o]
    return o


def exercices_a_plat(exam: dict) -> list[dict]:
    """Les exercices dans l'ordre du sujet ; une partie sans exercices (SVT, 1re partie) compte pour un."""
    out = []
    for p in exam.get("parts", []):
        if p.get("exercises"):
            out.extend(p["exercises"])
        else:
            out.append(p)
    return out


def copier(dossier: Path) -> dict:
    matiere, cle = dossier.parent.name, dossier.name
    exam = json.loads((dossier / "exam.json").read_text(encoding="utf-8"))
    session = str(exam.get("session", "")).lower()
    rattrapage = "rattrapage" in session or "ratt" in cle
    cle_propre = re.sub(r"ratrrapage", "rattrapage", cle)
    exam = nettoyer(exam)
    exam["sujet"] = f"{matiere}/{cle_propre}"
    exam["code"] = f"{'RS' if rattrapage else 'NS'} {CODES.get(matiere, '')}F".strip()
    exam["pages_sujet"] = len(list((dossier / "pages").glob("sujet_p*.jpg"))) if (dossier / "pages").is_dir() else None
    base = f"/media/examens/{matiere}/{cle_propre}"
    utilises: set[str] = set()

    def chemins(o):
        if isinstance(o, dict):
            src = o.get("src")
            if isinstance(src, str) and src and not src.startswith(("/", "http")):
                utilises.add(src)
                o["src"] = f"{base}/{src}"
            for v in o.values():
                chemins(v)
        elif isinstance(o, list):
            for v in o:
                chemins(v)

    chemins(exam)
    exam["exercices"] = [
        {"n": i + 1, "nom": e.get("name"), "points": e.get("points"), "questions": len(e.get("questions", [])),
         "documents": [d.get("id") for d in e.get("documents", []) if isinstance(d, dict)]}
        for i, e in enumerate(exercices_a_plat(exam))
    ]
    (CIBLE / matiere).mkdir(parents=True, exist_ok=True)
    (CIBLE / matiere / f"{cle_propre}.json").write_text(json.dumps(exam, ensure_ascii=False, indent=1), encoding="utf-8")
    for src in sorted(utilises):
        a = dossier / src
        if a.is_file():
            b = CIBLE / matiere / cle_propre / src
            b.parent.mkdir(parents=True, exist_ok=True)
            if not b.exists() or b.stat().st_size != a.stat().st_size:
                shutil.copy2(a, b)
    return exam


def main(args: list[str]) -> None:
    liste = "--liste" in args
    args = [a for a in args if a != "--liste"]
    dossiers = [SOURCE / a for a in args] if args else sorted(p.parent for p in SOURCE.glob("*/*/exam.json"))
    for d in dossiers:
        if not (d / "exam.json").is_file():
            print(f"!! {d} : pas d'exam.json", file=sys.stderr)
            continue
        exam = copier(d)
        print(f"{exam['sujet']:<28} {exam['code']}  {len(exam['exercices'])} exercices")
        if liste:
            for e in exam["exercices"]:
                print(f"   exercice={e['n']}  ({e['points']} pts, {e['questions']} q.)  {e['nom']}  figures: {', '.join(filter(None, e['documents'])) or '—'}")


if __name__ == "__main__":
    main(sys.argv[1:])
