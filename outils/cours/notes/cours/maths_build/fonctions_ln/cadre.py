"""Ajoute (ou remplace) la seule clé chapitres.fonctions_ln du cadre : relit, ajoute, réécrit aussitôt (indent 2)."""
import json, copy
from pathlib import Path
REPO = Path("backend/data/curriculum")
ex = json.loads((REPO / "exploration/fonctions_ln.json").read_text(encoding="utf-8"))
fiche = copy.deepcopy(ex["cadre"])
fiche["_note"] = ("Fiche ajoutée le 12 novembre 2026 (routine cloud) depuis exploration/fonctions_ln.json (dix professeurs, nationaux "
                  "2016-2025, perimetre.json). Le texte officiel du cadre n'a pas été relu mot à mot : capacités LN1 à LN10 provisoires, "
                  "à collationner. Lectures (dit) écrites comme la voix les dit.")
fiche["decisions"] = [
    "eʳ seulement comme nombre (« le nombre dont le ln vaut r ») : la fonction exponentielle est au chapitre suivant.",
    "Logarithme de base a exclu (absent du cadre cité et des nationaux) ; seul le logarithme décimal log x = ln x / ln 10.",
    "log décimal (2 diapositives) et systèmes (1 diapositive) gardés malgré 0 sujet national 2016-2025.",
    "lim ln(1 + x)/x = 1 et lim (ln x)/(x − 1) = 1 montrées comme nombre dérivé de ln en 1.",
    "ln|u| et u'/u gardés (primitives) ; intégrales et suites des nationaux renvoyées aux chapitres suivants.",
]
p = REPO / "cadre_reference_2bac_pc.json"
cadre = json.loads(p.read_text(encoding="utf-8"))
cadre["chapitres"]["fonctions_ln"] = fiche
p.write_text(json.dumps(cadre, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("chapitres.fonctions_ln :", len(fiche["capacites"]), "capacités,", len(fiche["formules"]), "formules,", len(fiche["hors_cadre"]["mots"]), "mots hors cadre")
