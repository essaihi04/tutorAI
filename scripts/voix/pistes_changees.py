"""Pistes d'une copie en attente à mettre en voix : nouvelles ou dont le texte a changé par rapport au cours en ligne,
et pistes de la copie qui n'ont pas encore de voix (18 novembre 2026, skill logique-de-cours, étape 5).
Usage : python -X utf8 scripts/voix/pistes_changees.py <deck> [--ecrire]  → backend/data/curriculum/architecture/<deck>_voix.json"""
import json, os, sys
ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)
from pistes_cours import pistes
RACINE = os.path.join(ICI, "..", "..")


def charger(chemin):
    return json.load(open(chemin, encoding="utf-8"))


def main():
    deck = sys.argv[1]
    en_ligne = charger(os.path.join(RACINE, "backend/data/courses", deck + ".json"))
    attente = charger(os.path.join(RACINE, "backend/data/courses/en_attente", deck + ".json"))
    avant = {(d, i): t for d, i, t, _ in pistes(en_ligne)}
    textes_avant = set(avant.values())      # une piste déplacée (autre id, même texte) garde sa voix dans son objet
    sortie = []
    for d, i, t, _ in pistes(attente):
        if avant.get((d, i)) == t or t in textes_avant:
            continue
        typ = {"mixed": "diapositive", "demos": "demonstration"}.get(d, "reaction_ou_enonce")
        sortie.append({"type": typ, "dossier": d, "id": i, "texte": t,
                       "raison": "nouvelle" if (d, i) not in avant else "texte changé"})
    res = {"deck": deck, "_note": "Pistes nouvelles ou au texte changé de la copie en attente (backend/data/courses/en_attente/"
           + deck + ".json), à mettre en voix Bodi sur le VPS ; les autres pistes gardent leur voix.", "pistes": sortie}
    if "--ecrire" in sys.argv:
        chemin = os.path.join(RACINE, "backend/data/curriculum/architecture", deck + "_voix.json")
        os.makedirs(os.path.dirname(chemin), exist_ok=True)
        json.dump(res, open(chemin, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        open(chemin, "a", encoding="utf-8").write("\n")
    from collections import Counter
    print(len(sortie), "pistes", dict(Counter(p["type"] for p in sortie)))
    if "-v" in sys.argv:
        for p in sortie:
            print(" ", p["dossier"], p["id"], p["raison"])


if __name__ == "__main__":
    main()
