"""Construit backend/data/courses/phys_ch8_circuit_RLC.json depuis p1..p4.py (lancer depuis la racine du dépôt).
`python3 outils/cours/notes/cours/circuit_RLC_build/build.py --garder-reponses` garde réactions, séances, rappels et prédictions déjà posés."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2
from p2 import PARTIE3, PARTIE4
from p3 import PARTIE5, PARTIE6, PARTIE7
from p4 import PARTIE8, PARTIE9, PARTIE10, BILAN

ACTS = [
 ("lc_partie1", "I. Un condensateur qui se vide dans une bobine", "explanation", PARTIE1),
 ("lc_partie2", "II. Les trois régimes", "explanation", PARTIE2),
 ("lc_partie3", "III. L'équation différentielle", "explanation", PARTIE3),
 ("lc_partie4", "IV. La solution du circuit LC et la période propre", "explanation", PARTIE4),
 ("lc_partie5", "V. Les conditions initiales : U_m et φ", "explanation", PARTIE5),
 ("lc_partie6", "VI. Lire un oscillogramme", "application", PARTIE6),
 ("lc_partie7", "VII. L'échange d'énergie", "explanation", PARTIE7),
 ("lc_partie8", "VIII. L'amortissement", "explanation", PARTIE8),
 ("lc_partie9", "IX. L'entretien des oscillations", "explanation", PARTIE9),
 ("lc_partie10", "X. Deux sujets du national", "evaluation", PARTIE10),
 ("lc_bilan", "XI. Bilan du chapitre", "evaluation", BILAN),
]
COMP = [
 ("C1", "Décrire la décharge d'un condensateur dans une bobine, utiliser i = dq/dt = C·du_C/dt et trouver u_b(0⁺)", ["RLC1"],
  "décrire les oscillations libres et trouver le signe de i"),
 ("C2", "Reconnaître les régimes périodique, pseudo-périodique et apériodique ; rôle de la résistance totale R + r", ["RLC2"],
  "reconnaître les régimes et le rôle de R plus r"),
 ("C3", "Établir l'équation différentielle vérifiée par q ou par u_C (RLC, puis LC idéal)", ["RLC3"],
  "établir l'équation différentielle en q ou en u C"),
 ("C4", "Vérifier la solution u_C = U_m·cos(2πt/T₀ + φ), en déduire T₀ = 2π√(LC), trouver U_m et φ", ["RLC4"],
  "vérifier la solution et trouver T zéro égale deux pi racine de L C"),
 ("C5", "Lire T sur un oscillogramme, utiliser T ≈ T₀, calculer L ou C (π² = 10), influence de L et de C", ["RLC5"],
  "lire la période et calculer L ou C"),
 ("C6", "Exprimer l'énergie totale E = ½·C·u_C² + ½·L·i² et décrire l'échange entre condensateur et bobine", ["RLC6"],
  "calculer l'énergie totale du circuit"),
 ("C7", "Expliquer l'amortissement par l'effet Joule, dE/dt = −(R + r)·i², énergie perdue entre deux instants", ["RLC7"],
  "calculer l'énergie perdue par effet Joule"),
 ("C8", "Expliquer l'entretien par u_G = k·i et montrer que k = R + r", ["RLC8"],
  "entretenir les oscillations avec k égale R plus r"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": "phys_ch8_circuit_RLC", "stable_id": "phys_ch8_circuit_RLC",
 "title": "Oscillations libres d'un circuit RLC série", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["circuit RLC", "circuit RLC série", "oscillations libres", "oscillations libres d'un circuit RLC série", "circuit LC",
                  "oscillations électriques", "période propre", "RLC", "rlc 2 bac"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : un condensateur chargé qui se vide dans une bobine, les oscillations libres, les régimes périodique, pseudo-périodique et apériodique, l'équation différentielle en q et en u_C, la solution du circuit LC et T₀ = 2π√(LC), U_m et φ, la lecture des oscillogrammes pour trouver L ou C, l'échange d'énergie, l'amortissement par effet Joule et l'entretien u_G = k·i, avec les nationaux 2016 à 2025.",
             "cover_alt": "Un circuit RLC à la craie et la courbe u_C(t) qui oscille en s'amortissant",
             "essential_topics": ["i = dq/dt = C·du_C/dt ; u_b(0⁺) = −u_C(0)", "Régimes : périodique, pseudo-périodique, apériodique",
                                  "L·d²q/dt² + (R + r)·dq/dt + q/C = 0", "LC : d²u_C/dt² + u_C/(LC) = 0",
                                  "u_C(t) = U_m·cos(2πt/T₀ + φ) ; T₀ = 2π√(LC)", "T ≈ T₀ ; C = T₀²/(4π²·L) ; π² = 10",
                                  "E = ½·C·u_C² + ½·L·i² ; dE/dt = −(R + r)·i²", "Entretien : u_G = k·i ; k = R + r"]},
 "note": "Cours 8 de physique (électricité), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/circuit_RLC.json ; vidéos non auditées, nationaux 2016-2025) et le contrat des simulations (outils/cours/notes/cours/circuit_RLC_contrat_simulations.md, circuit-rlc-tableau/). Brouillon : voix à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path("backend/data/courses/phys_ch8_circuit_RLC.json")
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
