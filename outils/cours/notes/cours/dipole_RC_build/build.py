"""Construit backend/data/courses/phys_ch6_dipole_RC.json depuis p1..p4.py (lancer depuis la racine du dépôt).
`python3 outils/cours/notes/cours/dipole_RC_build/build.py --garder-reponses` garde réactions, séances, rappels et prédictions déjà posés."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2
from p2 import PARTIE3, PARTIE4
from p3 import PARTIE5, PARTIE6
from p4 import PARTIE7, PARTIE8, PARTIE9, BILAN

ACTS = [
 ("rc_partie1", "I. Le condensateur", "explanation", PARTIE1),
 ("rc_partie2", "II. Associer des condensateurs, charger à courant constant", "application", PARTIE2),
 ("rc_partie3", "III. Le dipôle RC soumis à un échelon de tension", "explanation", PARTIE3),
 ("rc_partie4", "IV. L'équation différentielle", "explanation", PARTIE4),
 ("rc_partie5", "V. La solution et les quatre courbes", "explanation", PARTIE5),
 ("rc_partie6", "VI. La constante de temps et la décharge", "explanation", PARTIE6),
 ("rc_partie7", "VII. Lire les courbes", "application", PARTIE7),
 ("rc_partie8", "VIII. L'énergie emmagasinée", "explanation", PARTIE8),
 ("rc_partie9", "IX. Deux sujets du national", "evaluation", PARTIE9),
 ("rc_bilan", "X. Bilan du chapitre", "evaluation", BILAN),
]
COMP = [
 ("C1", "Décrire le condensateur et utiliser q = C·u_C et i = C·du_C/dt", ["RC1", "RC2"], "utiliser q égale C u C et i égale C dé u C sur dé t"),
 ("C2", "Calculer une capacité équivalente et déterminer C par une charge à courant constant", ["RC3"], "calculer une capacité équivalente"),
 ("C3", "Décrire la réponse d'un dipôle RC à un échelon de tension et brancher l'acquisition", ["RC4"], "décrire la réponse à un échelon de tension"),
 ("C4", "Établir l'équation différentielle (u_C, q, u_R, i) en charge et en décharge", ["RC5"], "établir l'équation différentielle"),
 ("C5", "Déterminer les constantes d'une solution et en déduire q(t), i(t), u_R(t)", ["RC6"], "trouver les constantes de la solution"),
 ("C6", "Connaître τ = R·C, son unité, l'influence de R et de C", ["RC7"], "connaître tau égale R C"),
 ("C7", "Déterminer τ graphiquement et exploiter les courbes pour trouver E, R, C", ["RC8"], "lire tau sur une courbe"),
 ("C8", "Calculer l'énergie emmagasinée E_e = ½·C·u_C²", ["RC9"], "calculer l'énergie du condensateur"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": "phys_ch6_dipole_RC", "stable_id": "phys_ch6_dipole_RC",
 "title": "Dipôle RC", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["dipôle RC", "dipole RC", "dipôle rc", "condensateur", "charge et décharge d'un condensateur", "dipôle RC 2 bac"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : le condensateur, q = C·u_C et i = C·du_C/dt, associations et charge à courant constant, réponse à un échelon de tension, équation différentielle en charge et en décharge, solution et constantes, τ = R·C et sa lecture sur les courbes, énergie emmagasinée, avec les nationaux 2016 à 2025.",
             "cover_alt": "Un circuit RC à la craie et la courbe de charge u_C(t) qui monte vers E",
             "essential_topics": ["q = C·u_C ; i = C·du_C/dt", "C_eq en parallèle et en série ; C = I₀/k", "Régime transitoire, régime permanent ; u_C continue",
                                  "RC·du_C/dt + u_C = E ; décharge : = 0", "u_C(t) = E(1 − e^(−t/τ)) ; u_C(t) = E·e^(−t/τ)", "τ = R·C, un temps",
                                  "Lire τ : tangente, 63 %, 37 %", "E_e = ½·C·u_C²"]},
 "note": "Cours 6 de physique (électricité), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/dipole_RC.json) et le contrat des simulations (outils/cours/notes/cours/dipole_RC_contrat_simulations.md, dipole-rc-tableau/). Brouillon : voix Bodi à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path("backend/data/courses/phys_ch6_dipole_RC.json")
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
