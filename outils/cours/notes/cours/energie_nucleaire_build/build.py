import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2, PARTIE3
from p2 import PARTIE3B, PARTIE4, PARTIE5
from p3 import PARTIE6, PARTIE6B, PARTIE7
from p4 import PARTIE8, PARTIE9, BILAN

ACTS = [
 ("en_partie1", "I. La masse peut devenir énergie", "situation", PARTIE1),
 ("en_partie2", "II. Le défaut de masse", "explanation", PARTIE2),
 ("en_partie3", "III. L'énergie de liaison", "explanation", PARTIE3 + PARTIE3B),
 ("en_partie4", "IV. Stabilité et courbe d'Aston", "explanation", PARTIE4),
 ("en_partie5", "V. Réactions provoquées : fission et fusion", "explanation", PARTIE5),
 ("en_partie6", "VI. Énergie libérée : par les masses", "application", PARTIE6 + PARTIE6B),
 ("en_partie7", "VII. Énergie libérée : par les énergies de liaison", "application", PARTIE7),
 ("en_partie8", "VIII. L'énergie d'un échantillon", "application", PARTIE8),
 ("en_partie9", "IX. Cas types du national", "evaluation", PARTIE9),
 ("en_bilan", "X. Bilan du chapitre", "evaluation", BILAN),
]
COMP = [
 ("C1", "Utiliser E = m·c² et convertir les unités (u, MeV, J)", ["EN1"], "utiliser E égale m fois c au carré et convertir les unités"),
 ("C2", "Calculer le défaut de masse d'un noyau", ["EN2"], "calculer le défaut de masse d'un noyau"),
 ("C3", "Calculer l'énergie de liaison et l'énergie de liaison par nucléon", ["EN3"], "calculer l'énergie de liaison d'un noyau"),
 ("C4", "Comparer la stabilité de noyaux et exploiter la courbe d'Aston", ["EN4"], "comparer la stabilité de deux noyaux"),
 ("C5", "Reconnaître et écrire une fission et une fusion", ["EN5"], "reconnaître une fission et une fusion"),
 ("C6", "Calculer l'énergie libérée à partir des masses", ["EN6"], "calculer l'énergie libérée avec les masses"),
 ("C7", "Calculer l'énergie libérée à partir des énergies de liaison et exploiter un diagramme énergétique", ["EN7"], "calculer l'énergie libérée avec les énergies de liaison"),
 ("C8", "Calculer l'énergie libérée par un échantillon et comparer fission et fusion", ["EN8"], "calculer l'énergie d'un échantillon"),
 ("C9", "Rédiger comme le barème : reconnaître le cas type du national", ["EN3", "EN4", "EN6", "EN7"], "reconnaître le cas type et rédiger comme le barème"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = []
for cid, lab, cad, dit in COMP:
    comps.append({"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit})
deck = {
 "id": "phys_ch5_energie_nucleaire", "stable_id": "phys_ch5_energie_nucleaire",
 "title": "Noyaux, masse et énergie", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["noyaux, masse et énergie", "noyaux masse et energie", "énergie nucléaire", "noyaux masse énergie 2 bac"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : E = m·c² et les unités, défaut de masse, énergie de liaison et stabilité, courbe d'Aston, fission et fusion, énergie libérée par les masses et par les énergies de liaison, diagramme énergétique, énergie d'un échantillon, avec les nationaux 2016 à 2025.",
             "cover_alt": "Une balance : les nucléons séparés pèsent plus lourd que le noyau qu'ils forment",
             "essential_topics": ["E = m·c² ; 1 u = 931,5 MeV/c²", "Défaut de masse Δm", "E_ℓ = Δm·c² ; E_ℓ/A", "Stabilité ; courbe d'Aston",
                                  "Fission et fusion ; lois de Soddy", "Δm = Σm(produits) − Σm(réactifs) ; E_lib = |ΔE|",
                                  "ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits) ; diagramme", "N = m·N_A/M ; E = N·E_lib"]},
 "note": "Cours 5 de physique (transformations nucléaires), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/energie_nucleaire.json) et le contrat des simulations (energie-nucleaire-tableau/). Brouillon : voix Bodi à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path(r"backend/data/courses/phys_ch5_energie_nucleaire.json")
if out.exists() and "--garder-reponses" in sys.argv:
    old = json.loads(out.read_text(encoding="utf-8"))
    oldr = {s["id"]: s.get("concentration", {}).get("reponses") for a in old["activities"] for s in a["slides"]}
    for s in slides:
        if oldr.get(s["id"]): s["concentration"]["reponses"] = oldr[s["id"]]
    for k in ("seances",):
        if k in old: deck[k] = old[k]
    oc = {c["id"]: c for c in old.get("competences", [])}
    for c in comps:
        if oc.get(c["id"], {}).get("rappels"): c["rappels"] = oc[c["id"]]["rappels"]
    oq = {s["id"]: (s.get("question") or {}) for a in old["activities"] for s in a["slides"]}
    for s in slides:
        if s.get("question") and oq.get(s["id"], {}).get("prediction"): s["question"]["prediction"] = True
out.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(slides), "diapositives ;", sum(1 for s in slides if s.get("question")), "questions ;", sum(len(s.get("exercises", [])) for s in slides), "exercices")
for c in comps: print(c["id"], len(c["slide_ids"]))
