"""Construit backend/data/courses/phys_ch10_cinetique.json depuis p1..p4.py (lancer depuis la racine du dépôt).
`python3 outils/cours/notes/cours/cinetique_build/build.py --garder-reponses` garde réactions, séances, rappels et prédictions déjà posés.
Les compétences (C1…C8) sont lues dans l'exploration (plan.competences)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2, PARTIE3
from p2 import PARTIE4, PARTIE5
from p3 import PARTIE6, PARTIE7, PARTIE8
from p4 import PARTIE9, PARTIE10, BILAN

ACTS = [
 ("ci_partie0", "Ouverture", "explanation", PARTIE1),
 ("ci_partie1", "I. Suivre une transformation au cours du temps", "explanation", PARTIE2),
 ("ci_partie2", "II. Tableau d'avancement et courbe x(t)", "application", PARTIE3),
 ("ci_partie3", "III. Suivi par conductimétrie", "explanation", PARTIE4),
 ("ci_partie4", "IV. Suivi par la pression d'un gaz ; choisir sa méthode", "application", PARTIE5),
 ("ci_partie5", "V. Vitesse volumique de réaction", "explanation", PARTIE6),
 ("ci_partie6", "VI. Évolution de la vitesse", "explanation", PARTIE7),
 ("ci_partie7", "VII. Temps de demi-réaction", "explanation", PARTIE8),
 ("ci_partie8", "VIII. Sujets du national", "evaluation", PARTIE9),
 ("ci_partie9", "IX. Pièges de rédaction", "evaluation", PARTIE10),
 ("ci_bilan", "X. Bilan du chapitre", "evaluation", BILAN),
]
ex = json.loads(Path("backend/data/curriculum/exploration/cinetique.json").read_text(encoding="utf-8"))
COMP = [(c["id"], c["verbe"], c.get("cadre_ids", []), c.get("dit", "")) for c in ex["plan"]["competences"]]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": "phys_ch10_cinetique", "stable_id": "phys_ch10_cinetique",
 "title": "Suivi temporel d'une transformation chimique, vitesse de réaction", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["suivi temporel d'une transformation chimique", "suivi temporel", "vitesse de réaction", "vitesse volumique de réaction",
                  "temps de demi-réaction", "temps de demi-reaction", "cinétique chimique", "cinetique chimique", "conductimétrie", "avancement x(t)"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : suivre une transformation au cours du temps (titrage après trempe, conductimétrie, pression d'un gaz), tableau d'avancement et courbe x(t), vitesse volumique de réaction par la tangente, évolution de la vitesse, temps de demi-réaction, avec des sujets du national.",
             "cover_alt": "Une courbe x(t) à la craie qui monte puis atteint un palier, avec une tangente verte à l'origine",
             "essential_topics": ["v(t) = (1/V)·dx/dt", "x(t₁/₂) = x_f/2", "x = x_max·(σ₀ − σ)/(σ₀ − σ_f)", "x = (P − P₀)·V/(R·T)",
                                  "Trempe : eau glacée pour bloquer la réaction avant le titrage", "La vitesse diminue : les réactifs s'épuisent"]},
 "note": "Cours 10 de physique-chimie (chimie), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/cinetique.json ; vidéos non auditées, nationaux 2016-2025) et le contrat des simulations (outils/cours/notes/cours/cinetique_contrat_simulations.md, chimie/cinetique-tableau/). Brouillon : voix à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path("backend/data/courses/phys_ch10_cinetique.json")
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
