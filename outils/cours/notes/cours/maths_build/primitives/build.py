"""Build du cours math_ch4_primitives : python build.py [--garder-reponses]
Écrit backend/data/courses/math_ch4_primitives.json et primitives-tableau/calculs-vues.js.
Après `blocs.py appliquer`, garder les champs ajoutés (seances, rappels, prediction) : --garder-reponses les garde aussi."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import OUVERTURE, DEFINITION, FAMILLE
from p2 import TABLEAU, OPERATIONS
from p3 import FORMES, RECONNAITRE
from p4 import GRAPHIQUE, NATIONAL, BILAN

ACTS = [
 ("pr_ouverture", "Ouverture — dériver, puis revenir", "situation", OUVERTURE),
 ("pr_partie1", "I. Définition : une primitive de f sur un intervalle", "explanation", DEFINITION),
 ("pr_partie2", "II. Existence, famille F + k et condition", "explanation", FAMILLE),
 ("pr_partie3", "III. Le tableau des primitives usuelles", "explanation", TABLEAU),
 ("pr_partie4", "IV. Somme, produit, transformer l'écriture", "explanation", OPERATIONS),
 ("pr_partie5", "V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u", "explanation", FORMES),
 ("pr_partie6", "VI. Reconnaître une dérivée ; choisir la méthode", "application", RECONNAITRE),
 ("pr_partie7", "VII. La courbe de f est la pente de F", "explanation", GRAPHIQUE),
 ("pr_partie8", "VIII. Types national et devoir", "evaluation", NATIONAL),
 ("pr_bilan", "IX. Bilan et carte du chapitre", "evaluation", BILAN),
]
COMP = [
 ("K1", "Vérifier qu'une fonction est une primitive d'une autre sur un intervalle", ["PR1"], "vérifier que F est une primitive de f sur I"),
 ("K2", "Justifier l'existence de primitives sur un intervalle", ["PR2"], "justifier que f admet des primitives sur I"),
 ("K3", "Déterminer toutes les primitives d'une fonction et la primitive qui vérifie une condition", ["PR3", "PR4"], "déterminer les primitives et la primitive qui vérifie F(x₀) = y₀"),
 ("K4", "Utiliser le tableau des primitives usuelles et la linéarité", ["PR5", "PR6"], "utiliser le tableau des primitives usuelles"),
 ("K5", "Déterminer une primitive de la forme u′uⁿ ou u′uʳ en faisant apparaître u′", ["PR7"], "primitiver la forme u′uⁿ"),
 ("K6", "Déterminer une primitive des formes u′/u², u′/√u, u′·cos u, u′·sin u", ["PR7"], "primitiver les formes u′/u², u′/√u, u′cos u, u′sin u"),
 ("K7", "Reconnaître une dérivée de produit ou de quotient et transformer l'écriture avant de primitiver", ["PR6", "PR7"], "reconnaître u′v + uv′ et transformer l'écriture"),
 ("K8", "Relier le signe de f aux variations de ses primitives et lire f comme la pente de F", ["PR8", "PR3"], "relier le signe de f aux variations de F"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(8, 3 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit} for cid, lab, cad, dit in COMP]
deck = {
 "id": "math_ch4_primitives", "stable_id": "math_ch4_primitives",
 "title": "Fonctions primitives", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["fonctions primitives", "primitives", "primitive d'une fonction", "les primitives", "primitives 2 bac", "fonction primitive"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : une primitive comme dérivée lue à l'envers, vérifier une primitive (question du national), existence sur un intervalle, famille F + k et condition F(x₀) = y₀, tableau des primitives usuelles, linéarité, formes u′uⁿ, u′/u², u′/√u, u′cos u, u′sin u, dérivées de produit et de quotient reconnues, lien graphique f / F, exercices type national.",
             "cover_alt": "Deux flèches à la craie entre F et f : « dériver » en rouge, « primitiver » en vert ; dessous, des paraboles x² + k translatées",
             "essential_topics": ["F′(x) = f(x) pour tout x ∈ I", "Vérifier une primitive : dériver", "f continue sur I ⇒ primitives", "Toutes les primitives : F(x) + k", "Condition F(x₀) = y₀", "Tableau des primitives usuelles", "u′uⁿ, u′/u², u′/√u, u′cos u, u′sin u", "u′v + uv′ → uv", "Signe de f, variations de F"]},
 "note": "Cours 4 de maths (2 Bac PC BIOF), écrit en mode concentration d'après l'exploration backend/data/curriculum/exploration/primitives.json et le contrat des simulations (maths/primitives-tableau/). ln, exp et l'intégrale seulement annoncés « plus tard » ; 1 + tan² « pour mémoire » ; pas de fonctions par morceaux ni de linéarisation. Brouillon : voix et réactions préparées à faire par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path(r"backend/data/courses/math_ch4_primitives.json")
if out.exists() and "--garder-reponses" in sys.argv:
    old = json.loads(out.read_text(encoding="utf-8"))
    olds = {s["id"]: s for a in old["activities"] for s in a["slides"]}
    for s in slides:
        o = olds.get(s["id"])
        if not o: continue
        if o.get("concentration", {}).get("reponses"): s["concentration"]["reponses"] = o["concentration"]["reponses"]
        if o.get("question", {}).get("prediction") and s.get("question"): s["question"]["prediction"] = True
    for k in ("seances",):
        if k in old: deck[k] = old[k]
    oc = {c["id"]: c for c in old.get("competences", [])}
    for c in comps:
        if oc.get(c["id"], {}).get("rappels"): c["rappels"] = oc[c["id"]]["rappels"]
out.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
cal = Path(r"frontend/public/media/simulations/maths/primitives-tableau/calculs-vues.js")
cal.write_text("/* Écrit par maths_build/primitives/build.py depuis les p*.py du cours math_ch4_primitives : ne pas modifier à la main. */\nwindow.CALCULS = " + json.dumps(outils.CALCULS, ensure_ascii=False, indent=1).replace("′", "’") + ";\n", encoding="utf-8")
print(len(slides), "diapositives ;", sum(1 for s in slides if s.get("question")), "questions ;", sum(len(s.get("exercises", [])) for s in slides), "exercices ;",
      sum(1 for s in slides for o in [s.get("question")] + list(s.get("exercises") or []) if o and o.get("demonstration")), "démonstrations ;", len(outils.CALCULS), "vues de calculs")
for c in comps: print(c["id"], len(c["slide_ids"]))
