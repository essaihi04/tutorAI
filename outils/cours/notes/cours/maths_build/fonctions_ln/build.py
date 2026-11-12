"""Build du cours math_ch5_fonctions_ln : python build.py [--garder-reponses]   (lancé depuis la racine du dépôt)
Écrit backend/data/courses/math_ch5_fonctions_ln.json et ln-tableau/calculs-vues.js.
--garder-reponses garde réactions, séances, rappels et prédictions déjà posés (après `blocs.py appliquer`)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import OUVERTURE, NAISSANCE, COURBE
from p2 import DOMAINE, REGLES
from p3 import EQUATIONS, LIMITES_A
from p4 import LIMITES_B, DERIVEE, PRIMITIVES
from p5 import ETUDE, LOG, BILAN

ACTS = [
 ("ln_ouverture", "Ouverture — une fonction qui transforme les produits", "situation", OUVERTURE),
 ("ln_partie1", "I. La naissance de ln : la primitive de 1/x qui s'annule en 1", "explanation", NAISSANCE),
 ("ln_partie2", "II. La courbe de ln : croissance, signe, e, tangente", "explanation", COURBE),
 ("ln_partie3", "III. L'ensemble de définition : u(x) > 0", "explanation", DOMAINE),
 ("ln_partie4", "IV. Les règles de calcul", "explanation", REGLES),
 ("ln_partie5", "V. Équations, inéquations, systèmes", "application", EQUATIONS),
 ("ln_partie6", "VI. Les limites de base", "explanation", LIMITES_A + LIMITES_B),
 ("ln_partie7", "VII. La dérivée de ln u", "explanation", DERIVEE),
 ("ln_partie8", "VIII. Les primitives u'/u", "explanation", PRIMITIVES),
 ("ln_partie9", "IX. Étude de fonction et inégalités, type national", "evaluation", ETUDE),
 ("ln_partie10", "X. Le logarithme décimal", "explanation", LOG),
 ("ln_bilan", "XI. Bilan et carte du chapitre", "evaluation", BILAN),
]
COMP = [
 ("K1", "Connaître la fonction ln : définition, dérivée, croissance, signe, nombre e, courbe", ["LN1", "LN8"], "ln est la primitive de un sur x qui s'annule en un"),
 ("K2", "Déterminer l'ensemble de définition d'une fonction comportant ln", ["LN2"], "x appartient à D f si et seulement si u de x est strictement positif"),
 ("K3", "Calculer et simplifier avec les propriétés algébriques de ln", ["LN3"], "ln de a fois b égale ln a plus ln b"),
 ("K4", "Résoudre des équations, des inéquations et des systèmes logarithmiques", ["LN4"], "ln a égale ln b équivaut à a égale b"),
 ("K5", "Calculer des limites avec les limites logarithmiques de base et interpréter", ["LN5"], "limite de ln x sur x en plus l'infini égale zéro"),
 ("K6", "Dériver une fonction comportant ln et étudier le signe de sa dérivée", ["LN6"], "la dérivée de ln u est u prime sur u"),
 ("K7", "Déterminer des primitives de la forme u'/u et vérifier une primitive comportant ln", ["LN7"], "une primitive de u prime sur u est ln de valeur absolue de u"),
 ("K8", "Étudier et représenter une fonction comportant ln, prouver une inégalité par une fonction auxiliaire", ["LN8", "LN9"], "ln x est inférieur ou égal à x moins un"),
 ("K9", "Utiliser le logarithme décimal et résoudre 10ˣ = a", ["LN10"], "logarithme décimal de x égale ln x sur ln dix"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(8, 3 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit} for cid, lab, cad, dit in COMP]
deck = {
 "id": "math_ch5_fonctions_ln", "stable_id": "math_ch5_fonctions_ln",
 "title": "Fonctions logarithmiques", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["fonctions logarithmiques", "fonction logarithme", "logarithme népérien", "fonction ln", "ln", "logarithme 2 bac", "logarithme décimal"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : ln naît comme la primitive de 1/x qui s'annule en 1 ; sa courbe (croissance, signe, e, tangente y = x − 1) ; l'ensemble de définition ; les règles de calcul ; équations, inéquations, systèmes ; les limites de base ; (ln u)' = u'/u ; les primitives u'/u ; l'étude complète type national ; le logarithme décimal et le pH.",
             "cover_alt": "La courbe de ln à la craie rouge, passant par (1 ; 0) et (e ; 1), sous la droite y = x − 1",
             "essential_topics": ["ln 1 = 0 et (ln x)' = 1/x", "ln e = 1", "x ∈ D_f ⇔ u(x) > 0", "ln(ab) = ln a + ln b", "ln a = ln b ⇔ a = b", "lim (ln x)/x = 0", "(ln u)' = u'/u", "u'/u → ln|u|", "ln x ≤ x − 1", "log x = ln x / ln 10"]},
 "note": "Cours 5 de maths (2 Bac PC BIOF), écrit en mode concentration d'après l'exploration backend/data/curriculum/exploration/fonctions_ln.json et le contrat des simulations (maths/ln-tableau/). eʳ seulement comme le nombre dont le ln vaut r (exponentielle au chapitre suivant) ; pas de logarithme de base a. Brouillon : voix et réactions préparées à faire par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path(r"backend/data/courses/math_ch5_fonctions_ln.json")
if out.exists() and "--garder-reponses" in sys.argv:
    old = json.loads(out.read_text(encoding="utf-8"))
    olds = {s["id"]: s for a in old["activities"] for s in a["slides"]}
    for s in slides:
        o = olds.get(s["id"])
        if not o: continue
        if o.get("concentration", {}).get("reponses"): s["concentration"]["reponses"] = o["concentration"]["reponses"]
        if o.get("question", {}).get("prediction") and s.get("question"): s["question"]["prediction"] = True
        if o.get("question", {}).get("prompt") and s.get("question") and "--enonces" in sys.argv: s["question"]["prompt"] = o["question"]["prompt"]
    for k in ("seances",):
        if k in old: deck[k] = old[k]
    oc = {c["id"]: c for c in old.get("competences", [])}
    for c in comps:
        if oc.get(c["id"], {}).get("rappels"): c["rappels"] = oc[c["id"]]["rappels"]
out.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
cal = Path(r"frontend/public/media/simulations/maths/ln-tableau/calculs-vues.js")
cal.write_text("/* Écrit par maths_build/fonctions_ln/build.py depuis les p*.py du cours math_ch5_fonctions_ln : ne pas modifier à la main. */\nwindow.CALCULS = " + json.dumps(outils.CALCULS, ensure_ascii=False, indent=1).replace("′", "’") + ";\n", encoding="utf-8")
print(len(slides), "diapositives ;", sum(1 for s in slides if s.get("question")), "questions ;", sum(len(s.get("exercises", [])) for s in slides), "exercices ;",
      sum(1 for s in slides for o in [s.get("question")] + list(s.get("exercises") or []) if o and o.get("demonstration")), "démonstrations ;", len(outils.CALCULS), "vues de calculs")
for c in comps: print(c["id"], len(c["slide_ids"]))
