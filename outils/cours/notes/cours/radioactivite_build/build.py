"""Construit backend/data/courses/phys_ch4_radioactivite.json depuis p1..p4.py (lancer depuis la racine du dépôt).
`python build.py --garder-reponses` garde réactions, séances, rappels et prédictions déjà posés."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2, PARTIE2B, PARTIE2C
from p2 import PARTIE3, PARTIE3B
from p3 import PARTIE4, PARTIE4B
from p4 import PARTIE5, BILAN

ACTS = [
 ("ra_partie1", "I. Le noyau et sa stabilité", "explanation", PARTIE1),
 ("ra_partie2", "II. Les désintégrations", "explanation", PARTIE2 + PARTIE2B + PARTIE2C),
 ("ra_partie3", "III. La loi de décroissance et la demi-vie", "explanation", PARTIE3 + PARTIE3B),
 ("ra_partie4", "IV. L'activité et la datation", "application", PARTIE4 + PARTIE4B),
 ("ra_partie5", "V. Cas types du national", "evaluation", PARTIE5),
 ("ra_bilan", "VI. Bilan du chapitre", "evaluation", BILAN),
]
COMP = [
 ("C1", "Donner la composition d'un noyau et reconnaître des isotopes", ["RA1"], "donner la composition d'un noyau"),
 ("C2", "Lire le diagramme (N, Z) et prévoir la stabilité d'un noyau", ["RA2"], "lire le diagramme N Z et prévoir la stabilité"),
 ("C3", "Définir la radioactivité et appliquer les lois de Soddy", ["RA3"], "définir la radioactivité et appliquer les lois de Soddy"),
 ("C4", "Écrire les désintégrations α, β⁻, β⁺ et la désexcitation γ", ["RA4", "RA2"], "écrire les désintégrations alpha, bêta et gamma"),
 ("C5", "Exploiter une famille radioactive (nombre de α et de β⁻)", ["RA5"], "exploiter une famille radioactive"),
 ("C6", "Connaître et exploiter la loi de décroissance N(t) = N₀·e^(−λt), λ et τ", ["RA6", "RA9"], "exploiter la loi de décroissance"),
 ("C7", "Définir et calculer la demi-vie t½ = ln2/λ, N₀/2ⁿ et les pourcentages", ["RA7", "RA9"], "définir et calculer la demi-vie"),
 ("C8", "Définir et calculer l'activité a = λ·N et le nombre de noyaux N = (m/M)·N_A", ["RA8", "RA9"], "calculer l'activité et le nombre de noyaux"),
 ("C9", "Dater un échantillon : t = (1/λ)·ln(a₀/a)", ["RA10"], "dater un échantillon"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": "phys_ch4_radioactivite", "stable_id": "phys_ch4_radioactivite",
 "title": "Décroissance radioactive", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["décroissance radioactive", "decroissance radioactive", "radioactivité", "radioactivite", "noyau radioactif 2 bac"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : composition du noyau et isotopes, diagramme (N, Z) et vallée de stabilité, radioactivité et lois de Soddy, désintégrations α, β⁻, β⁺ et γ, famille radioactive, loi de décroissance, constante de temps, demi-vie, activité, datation, avec les nationaux 2016 à 2025.",
             "cover_alt": "Une grille de noyaux qui se désintègrent au hasard et la courbe de décroissance à côté",
             "essential_topics": ["ᴬ_Z X : N = A − Z ; isotopes", "Diagramme (N, Z) ; vallée de stabilité", "Lois de Soddy",
                                  "α, β⁻, β⁺, γ", "Famille radioactive", "N(t) = N₀·e^(−λt) ; τ = 1/λ",
                                  "t½ = ln2/λ ; N₀/2ⁿ", "a = λ·N ; N = (m/M)·N_A", "t = (1/λ)·ln(a₀/a)"]},
 "note": "Cours 4 de physique (transformations nucléaires), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/radioactivite.json) et le contrat des simulations (radioactivite-tableau/). Brouillon : voix Bodi à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path("backend/data/courses/phys_ch4_radioactivite.json")
if out.exists() and "--garder-reponses" in sys.argv:
    old = json.loads(out.read_text(encoding="utf-8"))
    oldr = {s["id"]: s.get("concentration", {}).get("reponses") for a in old["activities"] for s in a["slides"]}
    for s in slides:
        if oldr.get(s["id"]): s["concentration"]["reponses"] = oldr[s["id"]]
    if "seances" in old: deck["seances"] = old["seances"]
    oc = {c["id"]: c for c in old.get("competences", [])}
    for c in comps:
        if oc.get(c["id"], {}).get("rappels"): c["rappels"] = oc[c["id"]]["rappels"]
    oq = {s["id"]: (s.get("question") or {}) for a in old["activities"] for s in a["slides"]}
    for s in slides:
        if s.get("question") and oq.get(s["id"], {}).get("prediction"): s["question"]["prediction"] = True
out.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(slides), "diapositives ;", sum(1 for s in slides if s.get("question")), "questions ;",
      sum(1 for s in slides if (s.get("question") or {}).get("prediction")), "prédictions ;", sum(len(s.get("exercises", [])) for s in slides), "exercices")
for c in comps: print(c["id"], len(c["slide_ids"]))
