"""Ajoute (ou remplace) la seule clé chapitres.suites_definition : relit, ajoute, réécrit aussitôt."""
import json, copy, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
R = Path(r"backend/data/curriculum")
fiche = copy.deepcopy(json.loads((R / "exploration/suites_definition.json").read_text(encoding="utf-8"))["cadre"])
fiche["_note"] = ("Fiche ajoutée le 11 novembre 2026 depuis exploration/suites_definition.json (onze professeurs, nationaux 2016-2025, "
                  "perimetre.json clés suites_definition et convergence, réunies ici). Identifiants SU1 à SU11 provisoires ; PDF officiel non relu. "
                  "Suites adjacentes : hors des compétences (non traitées). ln et exp : pas encore vus au 1er semestre, exemples rationnels.")
for f in fiche["formules"]:
    if f["capacite"] == "SU9":
        f["variantes_admises"] = ["lim √(uₙ + 7) = 3 car lim uₙ = 2 et la fonction racine carrée est continue en 9"]
    if f["ecriture"] == "lim qⁿ = 0 si −1 < q < 1":
        f["variantes_admises"] = [v for v in f["variantes_admises"] if "e⁻" not in v]
plus = {"uₙ = uₚ + (n − p)r": ["vₙ = v₀ + nr"], "uₙ = uₚ·qⁿ⁻ᵖ": ["vₙ = v₀·qⁿ", "uₙ = u₀ × qⁿ"],
        "uₙ₊₁ = q·uₙ": ["vₙ₊₁ = q·vₙ"], "uₙ₊₁ = uₙ + r": ["vₙ₊₁ − vₙ = r"],
        "uₚ + … + uₙ = uₚ·(1 − qⁿ⁻ᵖ⁺¹)/(1 − q)": ["S = (premier terme) × (1 − q puissance (nombre de termes))/(1 − q)"]}
for f in fiche["formules"]:
    for v in plus.get(f["ecriture"], []):
        if v not in f.setdefault("variantes_admises", []): f["variantes_admises"].append(v)
p = R / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["suites_definition"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok", list(d["chapitres"]))
