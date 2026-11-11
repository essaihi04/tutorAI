"""Ajoute (ou remplace) la seule clé chapitres.primitives : relit, ajoute, réécrit aussitôt."""
import json, copy
from pathlib import Path
REPO = Path(r"backend/data/curriculum")
fiche = copy.deepcopy(json.loads((REPO / "exploration/primitives.json").read_text(encoding="utf-8"))["cadre"])
fiche["_note"] = ("Fiche ajoutée le 11 novembre 2026 depuis exploration/primitives.json (dix professeurs, nationaux PC 2016-2025, "
                  "perimetre.json integration). Identifiants PR1 à PR8 provisoires, à collationner sur le texte officiel.")
fiche["decisions"] = [
  "Constante notée k (« x ↦ F(x) + k, k ∈ ℝ ») — agent maths, 11 novembre 2026.",
  "1 + tan²x = 1/cos²x → tan x : une diapositive « pour mémoire ».",
  "Primitives avec ln et exp (1/x, u′/u, eˣ, u′eᵘ) et l'intégrale : seulement annoncées « plus tard ».",
  "Lien graphique f / F (PR8) : deux diapositives, sans exercice national.",
  "(u′v − uv′)/v² → u/v : une diapositive.",
  "Pas de fonctions définies par morceaux, pas de linéarisation (hors_cadre.mots).",
]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["primitives"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", list(d["chapitres"].keys()))
