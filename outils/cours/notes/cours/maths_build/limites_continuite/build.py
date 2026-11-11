import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import OUVERTURE, LIMITES
from p2 import CONTINUITE_POINT, CONTINUITE_INTERVALLE
from p3 import IMAGE, TVI
from p4 import DICHOTOMIE, RECIPROQUE
from p5 import RACINE, PUISSANCES, LIMITES_RACINE
from p6 import PROBLEME, BILAN

ACTS = [
 ("lc_ouverture", "Ouverture — six questions sur une courbe", "situation", OUVERTURE),
 ("lc_partie1", "I. Rappel : calculer une limite", "explanation", LIMITES),
 ("lc_partie2", "II. Continuité en un point", "explanation", CONTINUITE_POINT),
 ("lc_partie3", "III. Continuité sur un intervalle", "explanation", CONTINUITE_INTERVALLE),
 ("lc_partie4", "IV. Image d'un intervalle", "explanation", IMAGE),
 ("lc_partie5", "V. Le théorème des valeurs intermédiaires", "explanation", TVI),
 ("lc_partie6", "VI. Pour les devoirs : la dichotomie", "application", DICHOTOMIE),
 ("lc_partie7", "VII. La fonction réciproque", "explanation", RECIPROQUE),
 ("lc_partie8", "VIII. Racine n-ième et puissances rationnelles", "explanation", RACINE + PUISSANCES),
 ("lc_partie9", "IX. Limites avec des racines n-ièmes", "application", LIMITES_RACINE),
 ("lc_bilan", "X. Problème national et bilan", "evaluation", PROBLEME + BILAN),
]
COMP = [
 ("K1", "Calculer une limite, lever une forme indéterminée et interpréter géométriquement le résultat", ["LC1"], "calculer une limite et lever une forme indéterminée"),
 ("K2", "Étudier la continuité d'une fonction en un point, à droite et à gauche", ["LC2"], "étudier la continuité en un point"),
 ("K3", "Justifier la continuité d'une fonction sur un intervalle", ["LC3"], "justifier la continuité sur un intervalle"),
 ("K4", "Déterminer l'image d'un intervalle par une fonction continue", ["LC4"], "déterminer l'image d'un intervalle"),
 ("K5", "Montrer qu'une équation admet une solution, unique, et la localiser (théorème des valeurs intermédiaires)", ["LC5", "LC6"], "appliquer le théorème des valeurs intermédiaires"),
 ("K6", "Encadrer une solution par dichotomie", ["LC7"], "encadrer une solution par dichotomie"),
 ("K7", "Montrer qu'une fonction admet une réciproque, déterminer J, son sens de variation et son expression", ["LC8"], "montrer qu'une fonction admet une fonction réciproque"),
 ("K8", "Construire la courbe de la fonction réciproque", ["LC9"], "construire la courbe de la fonction réciproque"),
 ("K9", "Calculer, simplifier, comparer et résoudre avec les racines n-ièmes et les puissances rationnelles", ["LC10", "LC11"], "calculer avec les racines n-ièmes"),
 ("K10", "Calculer une limite et justifier une continuité avec des racines n-ièmes", ["LC12"], "calculer une limite avec une racine n-ième"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(8, 3 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit} for cid, lab, cad, dit in COMP]
deck = {
 "id": "math_ch1_limites_continuite", "stable_id": "math_ch1_limites_continuite",
 "title": "Limites et continuité", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["limites et continuité", "limites et continuite", "continuité", "théorème des valeurs intermédiaires", "fonction réciproque", "racine n-ième", "limites et continuité 2 bac"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : rappel des limites, continuité en un point et sur un intervalle, image d'un intervalle, théorème des valeurs intermédiaires, dichotomie (devoirs), fonction réciproque et sa courbe, racine n-ième, puissances rationnelles, limites avec ∛, problème type national.",
             "cover_alt": "Une courbe à la craie : un trou, une asymptote verticale, et le point où elle coupe l'axe des abscisses",
             "cover_image": "/media/images/course-covers/mathematiques-limites-continuite-v1.png",
             "essential_topics": ["Formes indéterminées et outils", "lim f(x) = f(a) : continuité en a", "Continuité sur un intervalle, √u", "Image d'un intervalle", "Théorème des valeurs intermédiaires, solution unique", "Dichotomie (devoirs)", "Fonction réciproque, J = f(I), courbe symétrique", "Racine n-ième, x^(p/q), a³ − b³"]},
 "note": "Cours 1 de maths (2 Bac PC BIOF), écrit en mode concentration d'après l'exploration backend/data/curriculum/exploration/limites_continuite.json et le contrat des simulations (maths/limites-continuite-tableau/). Dichotomie en bloc court « pour les devoirs » ; « prolongement par continuité » ni écrit ni dit ; puissances rationnelles en trois diapositives (x > 0). Remplace l'ancien cours math_ch1_limits_v1 (non supprimé). Brouillon : voix Bodi et réactions préparées à faire par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path(r"backend/data/courses/math_ch1_limites_continuite.json")
if out.exists() and "--garder-reponses" in sys.argv:
    old = json.loads(out.read_text(encoding="utf-8"))
    oldr = {s["id"]: s.get("concentration", {}).get("reponses") for a in old["activities"] for s in a["slides"]}
    for s in slides:
        if oldr.get(s["id"]): s["concentration"]["reponses"] = oldr[s["id"]]
out.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
cal = Path(r"frontend/public/media/simulations/maths/limites-continuite-tableau/calculs-donnees.js")
cal.write_text("/* Écrit par le build du cours math_ch1_limites_continuite (maths_build/limites_continuite/build.py) : ne pas éditer à la main. */\nwindow.CALCULS = " + json.dumps(outils.CALCULS, ensure_ascii=False, indent=1).replace("′", "’") + ";\n", encoding="utf-8")
print(len(slides), "diapositives ;", sum(1 for s in slides if s.get("question")), "questions ;", sum(len(s.get("exercises", [])) for s in slides), "exercices ;",
      sum(1 for s in slides for o in [s.get("question")] + list(s.get("exercises") or []) if o and o.get("demonstration")), "démonstrations ;", len(outils.CALCULS), "vues de calculs")
for c in comps: print(c["id"], len(c["slide_ids"]))
