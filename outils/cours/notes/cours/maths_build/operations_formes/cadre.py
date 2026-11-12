"""Ajoute (ou remplace) la seule clé chapitres.operations_formes du cadre : relit, ajoute, réécrit aussitôt (indent 2)."""
import json, copy
from pathlib import Path
REPO = Path("backend/data/curriculum")
ex = json.loads((REPO / "exploration/operations_formes.json").read_text(encoding="utf-8"))
fiche = copy.deepcopy(ex["cadre"])
fiche["_note"] = ("Fiche ajoutée le 12 novembre 2026 (routine cloud) depuis exploration/operations_formes.json (dix professeurs, nationaux "
                  "2016-2025, perimetre.json). Capacités NC1 à NC10 provisoires, à collationner avec le texte officiel. "
                  "Lectures (dit) écrites comme la voix les dit.")
fiche["decisions"] = [
    "Partie 1 seulement : forme algébrique, quotient, affixe (point, vecteur, milieu), conjugué, module et distance, argument, forme trigonométrique, produit et quotient, Moivre, alignement par un quotient réel.",
    "Écriture exponentielle, formules d'Euler, équation à Δ < 0, transformations, angle (AB, AC), triangles et ensembles de points : partie 2 (seulement annoncés).",
    "Jamais la notation [r ; θ] ; pas d'inégalité triangulaire ni d'arctan ; la calculatrice seulement pour vérifier.",
    "Multiplier par i : « un quart de tour » dit qualitativement, sans écriture de rotation.",
]
p = REPO / "cadre_reference_2bac_pc.json"
cadre = json.loads(p.read_text(encoding="utf-8"))
cadre["chapitres"]["operations_formes"] = fiche
p.write_text(json.dumps(cadre, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("chapitres.operations_formes :", len(fiche["capacites"]), "capacités,", len(fiche["formules"]), "formules,", len(fiche["hors_cadre"]["mots"]), "mots hors cadre")
