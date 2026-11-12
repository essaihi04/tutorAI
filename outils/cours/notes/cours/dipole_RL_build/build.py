"""Construit backend/data/courses/phys_ch7_dipole_RL.json depuis p1..p4.py (lancer depuis la racine du dépôt).
`python3 outils/cours/notes/cours/dipole_RL_build/build.py --garder-reponses` garde réactions, séances, rappels et prédictions déjà posés."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2
from p2 import PARTIE3, PARTIE4
from p3 import PARTIE5, PARTIE6
from p4 import PARTIE7, PARTIE8, PARTIE9, BILAN

ACTS = [
 ("rl_partie1", "I. La bobine s'oppose aux variations du courant", "explanation", PARTIE1),
 ("rl_partie2", "II. La tension aux bornes d'une bobine", "explanation", PARTIE2),
 ("rl_partie3", "III. Le dipôle RL soumis à un échelon de tension", "explanation", PARTIE3),
 ("rl_partie4", "IV. L'équation différentielle", "explanation", PARTIE4),
 ("rl_partie5", "V. La solution et la constante de temps", "explanation", PARTIE5),
 ("rl_partie6", "VI. La rupture du courant", "explanation", PARTIE6),
 ("rl_partie7", "VII. Lire les courbes", "application", PARTIE7),
 ("rl_partie8", "VIII. L'énergie magnétique", "explanation", PARTIE8),
 ("rl_partie9", "IX. Deux sujets du national", "evaluation", PARTIE9),
 ("rl_bilan", "X. Bilan du chapitre", "evaluation", BILAN),
]
COMP = [
 ("C1", "Décrire la bobine et utiliser u_b = L·di/dt + r·i", ["RL1"], "utiliser u b égale L dé i sur dé t plus r i"),
 ("C2", "Expliquer le rôle de la bobine : retard, continuité de i, régime permanent", ["RL2"], "expliquer le rôle de la bobine"),
 ("C3", "Décrire la réponse d'un dipôle RL à un échelon de tension et visualiser i par u_R", ["RL3"], "décrire la réponse à un échelon de tension"),
 ("C4", "Établir l'équation différentielle (i ou u_R) à l'établissement et à la rupture", ["RL4"], "établir l'équation différentielle"),
 ("C5", "Vérifier la solution, trouver A et τ, écrire i(t), u_R(t), u_b(t)", ["RL5"], "trouver les constantes de la solution"),
 ("C6", "Connaître τ = L/(R + r), son unité, l'influence de L et de R", ["RL6"], "connaître tau égale L sur R plus r"),
 ("C7", "Exploiter les courbes pour trouver τ, I₀, E, r et L", ["RL7"], "lire tau sur une courbe et trouver r et L"),
 ("C8", "Calculer l'énergie magnétique E_m = ½·L·i²", ["RL8"], "calculer l'énergie de la bobine"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": "phys_ch7_dipole_RL", "stable_id": "phys_ch7_dipole_RL",
 "title": "Dipôle RL", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["dipôle RL", "dipole RL", "dipôle rl", "bobine", "inductance", "établissement du courant", "rupture du courant", "dipôle RL 2 bac"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : la bobine et l'auto-induction, u_b = L·di/dt + r·i, réponse à un échelon de tension, équation différentielle, solution, τ = L/(R + r), rupture du courant, lecture des courbes pour trouver r et L, énergie magnétique, avec les nationaux 2016 à 2025.",
             "cover_alt": "Un circuit RL à la craie et la courbe i(t) qui monte vers I₀",
             "essential_topics": ["u_b = L·di/dt + r·i", "i continue ; régime permanent : u_b = r·I₀", "I₀ = E/(R + r)",
                                  "L·di/dt + (R + r)·i = E ; rupture : = 0", "i(t) = I₀(1 − e^(−t/τ)) ; i(t) = I₀·e^(−t/τ)", "τ = L/(R + r), un temps",
                                  "Lire τ : tangente, 63 %, 37 % ; L = τ·(R + r)", "E_m = ½·L·i²"]},
 "note": "Cours 7 de physique (électricité), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/dipole_RL.json ; vidéos non auditées, nationaux 2016-2025) et le contrat des simulations (outils/cours/notes/cours/dipole_RL_contrat_simulations.md, dipole-rl-tableau/). Brouillon : voix à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path("backend/data/courses/phys_ch7_dipole_RL.json")
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
