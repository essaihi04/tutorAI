"""Construit backend/data/courses/phys_ch12_etat_equilibre.json depuis p1..p3.py (lancer depuis la racine du dépôt).
`python3 outils/cours/notes/cours/etat_equilibre_build/build.py --garder-reponses` garde réactions, séances, rappels et prédictions déjà posés.
Les compétences (C1…C8) sont lues dans l'exploration (plan.competences)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2, PARTIE3, PARTIE4
from p2 import PARTIE5, PARTIE6, PARTIE7
from p3 import PARTIE8, PARTIE9, BILAN

ACTS = [
 ("ee_partie0", "Ouverture", "explanation", PARTIE1),
 ("ee_partie1", "I. Rappels : taux d'avancement final et état d'équilibre", "explanation", PARTIE2),
 ("ee_partie2", "II. Le quotient de réaction Qr", "explanation", PARTIE3),
 ("ee_partie3", "III. Qr dans l'état initial et au cours de la transformation", "explanation", PARTIE4),
 ("ee_partie4", "IV. Le quotient de réaction à l'équilibre Qr,éq", "application", PARTIE5),
 ("ee_partie5", "V. La constante d'équilibre K", "explanation", PARTIE6),
 ("ee_partie6", "VI. Déterminer K par le pH et par la conductimétrie", "application", PARTIE7),
 ("ee_partie7", "VII. De quoi dépend le taux d'avancement final ?", "explanation", PARTIE8),
 ("ee_partie8", "VIII. Sujets du national", "evaluation", PARTIE9),
 ("ee_bilan", "IX. Bilan du chapitre", "evaluation", BILAN),
]
ex = json.loads(Path("backend/data/curriculum/exploration/etat_equilibre.json").read_text(encoding="utf-8"))
COMP = [(c["id"], c["verbe"], c.get("cadre_ids", []), c.get("dit", "")) for c in ex["plan"]["competences"]]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": "phys_ch12_etat_equilibre", "stable_id": "phys_ch12_etat_equilibre",
 "title": "État d'équilibre d'un système chimique", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["état d'équilibre d'un système chimique", "état d'équilibre", "quotient de réaction", "constante d'équilibre",
                  "Qr", "Qr,éq", "constante d'équilibre K", "taux d'avancement final et constante d'équilibre"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : quotient de réaction Qr (eau solvant et solides exclus), Qr dans l'état initial et au cours de la transformation, Qr à l'équilibre, constante d'équilibre K qui ne dépend que de la température, K de la réaction inverse, K par le pH et par la conductimétrie, K = C·τ²/(1 − τ), influence de K et de la concentration sur τ, avec des sujets du national.",
             "cover_alt": "Trois béchers d'acide éthanoïque à la craie, trois pH différents et une même constante K = 1,6·10⁻⁵ encadrée",
             "essential_topics": ["Qr = [C]^c·[D]^d/([A]^a·[B]^b)", "K = Qr,éq", "K' = 1/K", "K = C·τ²/(1 − τ)",
                                  "Qr,éq = 10^(−2pH)/(C − 10^(−pH))", "[H₃O⁺]_éq = σ/(λ(H₃O⁺) + λ(A⁻))",
                                  "τ dépend de K et de l'état initial ; K ne dépend que de la température"]},
 "note": "Cours 12 de physique-chimie (chimie), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/etat_equilibre.json ; vidéos non auditées, nationaux 2016-2025) et le contrat des simulations (outils/cours/notes/cours/etat_equilibre_contrat_simulations.md, chimie/etat-equilibre-tableau/). Brouillon : voix à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path("backend/data/courses/phys_ch12_etat_equilibre.json")
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
