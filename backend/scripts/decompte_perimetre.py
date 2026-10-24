"""Contrôle de la phase d'observation du périmètre : ce qui a dépassé, où, combien.

Lecture seule du journal écrit par perimetre.journaliser().

    python scripts/decompte_perimetre.py [--journal data/perimetre_journal.jsonl]
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.perimetre import JOURNAL  # noqa: E402


def lire(chemin: Path) -> list[dict]:
    if not chemin.exists():
        return []
    lignes = []
    for brute in chemin.read_text(encoding="utf-8").splitlines():
        brute = brute.strip()
        if brute:
            lignes.append(json.loads(brute))
    return lignes


def decompte(lignes: list[dict]) -> tuple[Counter, Counter, int]:
    """(par terme, par chapitre, tours concernés)."""
    par_terme, par_chapitre = Counter(), Counter()
    for ligne in lignes:
        par_chapitre[(ligne.get("matiere") or "?", ligne.get("chapitre") or "(sans fiche)")] += 1
        for t in ligne.get("termes", []):
            par_terme[t.get("terme") or "?"] += 1
    return par_terme, par_chapitre, len(lignes)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--journal", type=Path, default=JOURNAL)
    parser.add_argument("--exemples", type=int, default=2, help="extraits montrés par terme")
    args = parser.parse_args()

    lignes = lire(args.journal)
    par_terme, par_chapitre, tours = decompte(lignes)
    print(f"Tours avec un dépassement : {tours}  (journal : {args.journal})")
    print("\nPar chapitre")
    for (matiere, chapitre), n in par_chapitre.most_common():
        print(f"  {n:4d}  {matiere} / {chapitre}")
    print("\nPar terme")
    for terme, n in par_terme.most_common():
        print(f"  {n:4d}  {terme}")
        montres = 0
        for ligne in lignes:
            for t in ligne.get("termes", []):
                if t.get("terme") == terme and montres < args.exemples:
                    print(f"          « …{t.get('extrait', '')}… »")
                    montres += 1


if __name__ == "__main__":
    main()
