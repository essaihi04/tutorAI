"""Construit backend/data/courses/phys_ch11_transformations_deux_sens.json depuis p1..p3.py (lancer depuis la racine du dépôt).
`python3 outils/cours/notes/cours/transformations_deux_sens_build/build.py --garder-reponses` garde réactions, séances, rappels et prédictions déjà posés.
Les compétences (C1…C8) sont lues dans l'exploration (plan.competences)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2, PARTIE3, PARTIE4
from p2 import PARTIE5, PARTIE6
from p3 import PARTIE7, PARTIE8, PARTIE9, BILAN

ACTS = [
 ("td_partie0", "Ouverture", "explanation", PARTIE1),
 ("td_partie1", "I. Acides et bases selon Brønsted", "explanation", PARTIE2),
 ("td_partie2", "II. pH d'une solution aqueuse", "explanation", PARTIE3),
 ("td_partie3", "III. Réaction d'un acide avec l'eau", "explanation", PARTIE4),
 ("td_partie4", "IV. Taux d'avancement final", "application", PARTIE5),
 ("td_partie5", "V. Transformations dans les deux sens, état d'équilibre", "explanation", PARTIE6),
 ("td_partie6", "VI. Conductimétrie : trouver τ", "application", PARTIE7),
 ("td_partie7", "VII. Dilution et nature de l'acide", "explanation", PARTIE8),
 ("td_partie8", "VIII. Sujets du national", "evaluation", PARTIE9),
 ("td_bilan", "IX. Bilan du chapitre", "evaluation", BILAN),
]
ex = json.loads(Path("backend/data/curriculum/exploration/transformations_deux_sens.json").read_text(encoding="utf-8"))
COMP = [(c["id"], c["verbe"], c.get("cadre_ids", []), c.get("dit", "")) for c in ex["plan"]["competences"]]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": "phys_ch11_transformations_deux_sens", "stable_id": "phys_ch11_transformations_deux_sens",
 "title": "Transformations chimiques s'effectuant dans les deux sens", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["transformations chimiques s'effectuant dans les deux sens", "transformations dans les deux sens", "taux d'avancement final",
                  "acide et base selon Brønsted", "couple acide/base", "pH d'une solution", "état d'équilibre", "réaction limitée", "équilibre dynamique"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : acides et bases selon Brønsted, couples, pH et pH-mètre, réaction d'un acide avec l'eau, tableau d'avancement, taux d'avancement final τ, réaction totale ou limitée, transformations dans les deux sens et état d'équilibre dynamique, conductimétrie, influence de la dilution et de la nature de l'acide, avec des sujets du national.",
             "cover_alt": "Deux flacons de même concentration à la craie, un pH-mètre qui affiche 3,4 et 2,0, et une double flèche",
             "essential_topics": ["pH = −log[H₃O⁺]", "[H₃O⁺] = 10^(−pH)", "τ = x_f/x_max", "x_f = [H₃O⁺]_éq·V", "AH + H₂O ⇌ A⁻ + H₃O⁺",
                                  "σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺]", "À l'équilibre, les deux sens ont la même vitesse : état dynamique"]},
 "note": "Cours 11 de physique-chimie (chimie), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/transformations_deux_sens.json ; vidéos non auditées, nationaux 2016-2025) et le contrat des simulations (outils/cours/notes/cours/transformations_deux_sens_contrat_simulations.md, chimie/transformations-deux-sens-tableau/). Brouillon : voix à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path("backend/data/courses/phys_ch11_transformations_deux_sens.json")
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
