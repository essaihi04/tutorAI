import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import PARTIE1, PARTIE2
from p2 import PARTIE3
from p3 import PARTIE4, PARTIE5
from p4 import PARTIE6, PARTIE7, PARTIE8
from p5 import PARTIE9, PARTIE10, BILAN

ACTS = [
 ("ol_partie1", "I. La diffraction de la lumière", "situation", PARTIE1),
 ("ol_partie2", "II. L'écart angulaire : θ = λ/a", "explanation", PARTIE2),
 ("ol_partie3", "III. La largeur de la tache : L = 2λD/a", "explanation", PARTIE3),
 ("ol_partie4", "IV. Comparer deux expériences", "application", PARTIE4),
 ("ol_partie5", "V. Exploiter une courbe", "application", PARTIE5),
 ("ol_partie6", "VI. Radiation, fréquence et spectre", "explanation", PARTIE6),
 ("ol_partie7", "VII. La lumière dans un milieu d'indice n", "explanation", PARTIE7),
 ("ol_partie8", "VIII. La dispersion de la lumière blanche", "explanation", PARTIE8),
 ("ol_partie9", "IX. Cas types et exercices du national", "evaluation", PARTIE9),
 ("ol_partie10", "X. Pour le devoir : les relations du prisme", "application", PARTIE10),
 ("ol_bilan", "XI. Bilan du chapitre", "evaluation", BILAN),
]
COMP = [
 ("C1", "Reconnaître la diffraction de la lumière et dire ce qu'elle met en évidence", ["OL1", "OL2"], "reconnaître la diffraction de la lumière"),
 ("C2", "Connaître et exploiter θ = λ/a", ["OL3", "OL2"], "utiliser teta égale lambda sur a"),
 ("C3", "Établir et utiliser L = 2λD/a", ["OL4"], "établir et utiliser L égale deux lambda D sur a"),
 ("C4", "Comparer deux expériences de diffraction : fil, rapport, liquide", ["OL4", "OL2", "OL9"], "comparer deux expériences de diffraction"),
 ("C5", "Exploiter une courbe de diffraction", ["OL5"], "exploiter une courbe de diffraction"),
 ("C6", "Caractériser une radiation : fréquence, longueur d'onde dans le vide, spectre visible", ["OL6", "OL7", "OL8"], "caractériser une radiation par sa fréquence"),
 ("C7", "Calculer la célérité et la longueur d'onde dans un milieu d'indice n", ["OL8", "OL9"], "calculer v et lambda dans un milieu d'indice n"),
 ("C8", "Interpréter la dispersion de la lumière blanche par un prisme", ["OL6", "OL10"], "interpréter la dispersion par un prisme"),
 ("C9", "Appliquer les relations du prisme (pour le devoir)", ["OL11"], "appliquer les relations du prisme"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = []
for cid, lab, cad, dit in COMP:
    comps.append({"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit})
deck = {
 "id": "phys_ch3_ondes_lumineuses", "stable_id": "phys_ch3_ondes_lumineuses",
 "title": "Propagation d'une onde lumineuse", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["propagation d'une onde lumineuse", "ondes lumineuses", "propagation d'une onde lumineuse 2 bac"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : diffraction de la lumière, θ = λ/a, L = 2λD/a, deux expériences et courbes, radiation et spectre, indice n, dispersion par un prisme, avec les nationaux 2021, 2023 et 2025.",
             "cover_alt": "Un laser éclaire une fente fine : sur l'écran, une tache centrale lumineuse et des taches secondaires",
             "essential_topics": ["Diffraction : aspect ondulatoire de la lumière", "θ = λ / a", "L = 2λD / a", "Deux expériences, fil, liquide : n = L / L'",
                                  "Courbes L = f(1/a), θ = f(1/a), L = f(D)", "λ₀ = c / ν, spectre visible 400–800 nm", "n = c / v, λ = λ₀ / n", "Dispersion, milieu dispersif ; relations du prisme"]},
 "note": "Cours 3 des ondes, écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/ondes_lumineuses.json) et le contrat des simulations (ondes-lumineuses-tableau/). Relations du prisme en partie finale courte « pour le devoir » (décision à valider). Brouillon : voix Bodi à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path(r"backend/data/courses/phys_ch3_ondes_lumineuses.json")
if out.exists() and "--garder-reponses" in sys.argv:
    old = json.loads(out.read_text(encoding="utf-8"))
    oldr = {s["id"]: s.get("concentration", {}).get("reponses") for a in old["activities"] for s in a["slides"]}
    for s in slides:
        if oldr.get(s["id"]): s["concentration"]["reponses"] = oldr[s["id"]]
out.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(len(slides), "diapositives ;", sum(1 for s in slides if s.get("question")), "questions ;", sum(len(s.get("exercises", [])) for s in slides), "exercices")
for c in comps: print(c["id"], len(c["slide_ids"]))
