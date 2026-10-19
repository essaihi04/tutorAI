"""Contrôle de l'étape 1 : les réponses d'un élève, comptées par domaine officiel.

Lecture seule. Les réponses enregistrées avant l'étape 1 n'ont pas de domaine ;
elles sont reclassées à la volée et comptées à part, pour servir de point de
départ. La part de « Non classé » doit baisser au fil des semaines.

    python scripts/decompte_domaines.py <student_id> [--limite 500]
"""
import argparse
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.topic_atlas_service import NON_CLASSE, domaine_officiel  # noqa: E402


def decompte(lignes: list[dict]) -> tuple[Counter, Counter]:
    """(réponses classées à l'enregistrement, anciennes réponses reclassées ici)."""
    enregistrees, reclassees = Counter(), Counter()
    for ligne in lignes:
        if ligne.get("chapter"):
            enregistrees[(ligne.get("subject") or "?", ligne["chapter"])] += 1
        else:
            domaine = domaine_officiel(ligne.get("subject", ""), ligne.get("topic", ""), ligne.get("question_content", ""))
            reclassees[(ligne.get("subject") or "?", domaine)] += 1
    return enregistrees, reclassees


def afficher(titre: str, compte: Counter) -> None:
    total = sum(compte.values())
    print(f"\n{titre} — {total} réponses")
    if not total:
        return
    for (matiere, domaine), n in sorted(compte.items(), key=lambda kv: (kv[0][0], -kv[1])):
        print(f"  {matiere:16s} {n:4d}  {domaine}")
    non_classe = sum(n for (_, d), n in compte.items() if d == NON_CLASSE)
    print(f"  Non classé : {non_classe}/{total} ({100 * non_classe / total:.0f} %)")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("student_id")
    parser.add_argument("--limite", type=int, default=500)
    args = parser.parse_args()

    from app.supabase_client import get_supabase_admin

    lignes = get_supabase_admin().table("student_answer_history").select(
        "subject,topic,chapter,question_content,created_at"
    ).eq("student_id", args.student_id).order("created_at", desc=True).limit(args.limite).execute().data or []

    enregistrees, reclassees = decompte(lignes)
    afficher("Classées à l'enregistrement", enregistrees)
    afficher("Anciennes réponses, reclassées pour comparaison", reclassees)


if __name__ == "__main__":
    main()
