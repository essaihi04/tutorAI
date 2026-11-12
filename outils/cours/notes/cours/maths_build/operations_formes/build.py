"""Build du cours math_ch6_nombres_complexes : python build.py [--garder-reponses]   (lancé depuis la racine du dépôt)
Écrit backend/data/courses/math_ch6_nombres_complexes.json et operations-formes-tableau/calculs-vues.js.
--garder-reponses garde réactions, séances, rappels et prédictions déjà posés (après `blocs.py appliquer`)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import outils
from p1 import OUVERTURE, NOMBRE_I, CALCUL
from p2 import PLAN, CONJUGUE, MODULE
from p3 import ARGUMENT, TRIG, PRODUIT_A
from p4 import PRODUIT_B, GEOMETRIE, NATIONAUX, BILAN

ACTS = [
 ("nc_ouverture", "Ouverture — le nombre qui fait tourner", "situation", OUVERTURE),
 ("nc_partie1", "I. Le nombre i et la forme algébrique", "explanation", NOMBRE_I),
 ("nc_partie2", "II. Calculer sous forme algébrique", "application", CALCUL),
 ("nc_partie3", "III. Le plan complexe : affixes", "explanation", PLAN),
 ("nc_partie4", "IV. Le conjugué", "explanation", CONJUGUE),
 ("nc_partie5", "V. Le module et la distance", "explanation", MODULE),
 ("nc_partie6", "VI. L'argument", "explanation", ARGUMENT),
 ("nc_partie7", "VII. La forme trigonométrique", "explanation", TRIG),
 ("nc_partie8", "VIII. Produit, quotient et Moivre", "explanation", PRODUIT_A + PRODUIT_B),
 ("nc_partie9", "IX. Géométrie : alignement, distances", "application", GEOMETRIE),
 ("nc_partie10", "X. Deux sujets nationaux", "evaluation", NATIONAUX),
 ("nc_bilan", "XI. Bilan et carte du chapitre", "evaluation", BILAN),
]
COMP = [
 ("K1", "Connaître ℂ et la forme algébrique : i² = −1, partie réelle, partie imaginaire, réel, imaginaire pur, égalité, puissances de i", ["NC1"], "i au carré égale moins un"),
 ("K2", "Calculer sous forme algébrique : produit, carré, puissance, quotient par le conjugué du dénominateur", ["NC2"], "on multiplie en haut et en bas par le conjugué du dénominateur"),
 ("K3", "Représenter un complexe dans le plan : image, affixe d'un point, d'un vecteur, du milieu", ["NC3"], "l'affixe du vecteur A B égale z B moins z A"),
 ("K4", "Utiliser le conjugué : symétrie par rapport à l'axe réel, propriétés, z + z̄, z − z̄, z·z̄", ["NC4"], "z fois z barre égale a carré plus b carré"),
 ("K5", "Calculer un module et une distance : |z| = √(a² + b²) = OM, propriétés, AB = |z_B − z_A|", ["NC5"], "le module de z égale la racine de a carré plus b carré"),
 ("K6", "Déterminer un argument et passer de la forme algébrique à la forme trigonométrique, et réciproquement", ["NC6", "NC7"], "z égale r facteur de cos teta plus i sin teta"),
 ("K7", "Calculer avec la forme trigonométrique : produit, quotient, inverse, conjugué, puissance (Moivre)", ["NC8", "NC9"], "l'argument d'un produit est la somme des arguments"),
 ("K8", "Interpréter géométriquement : milieu, distance, égalité de distances, alignement par un quotient réel", ["NC10", "NC3", "NC5"], "A, B et C alignés si le quotient c moins a sur b moins a est réel"),
]
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(8, 4 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit} for cid, lab, cad, dit in COMP]
deck = {
 "id": "math_ch6_nombres_complexes", "stable_id": "math_ch6_nombres_complexes",
 "title": "Nombres complexes (première partie)", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["nombres complexes", "nombres complexes partie 1", "nombre complexe", "forme algébrique", "forme trigonométrique", "module et argument", "conjugué", "formule de Moivre", "complexes 2 bac"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : i naît comme un quart de tour ; la forme algébrique et le calcul (quotient par le conjugué) ; le plan complexe (affixe d'un point, d'un vecteur, du milieu) ; le conjugué comme reflet ; le module comme distance ; l'argument comme angle ; la forme trigonométrique ; produit, quotient et Moivre ; alignement et distances ; deux sujets nationaux.",
             "cover_alt": "Le plan complexe à la craie : un point M, son reflet par rapport à l'axe réel, le cercle de son module et l'arc de son argument",
             "essential_topics": ["i² = −1", "z = a + ib", "quotient : × conjugué du dénominateur", "z_AB = z_B − z_A", "z·z̄ = a² + b²", "|z| = √(a² + b²)", "AB = |z_B − z_A|", "z = r(cos θ + i sin θ)", "arg(zz′) ≡ arg z + arg z′ [2π]", "Moivre", "(c − a)/(b − a) réel ⇒ alignés"]},
 "note": "Cours 6 de maths (2 Bac PC BIOF), première partie des nombres complexes, écrit en mode concentration d'après l'exploration backend/data/curriculum/exploration/operations_formes.json et le contrat des simulations (maths/operations-formes-tableau/). Écriture exponentielle, Euler, équations du second degré et transformations : partie 2 (seulement annoncées). Brouillon : voix et réactions préparées à faire par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path(r"backend/data/courses/math_ch6_nombres_complexes.json")
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
cal = Path(r"frontend/public/media/simulations/maths/operations-formes-tableau/calculs-vues.js")
cal.write_text("/* Écrit par maths_build/operations_formes/build.py depuis les p*.py du cours math_ch6_nombres_complexes : ne pas modifier à la main. */\nwindow.CALCULS = " + json.dumps(outils.CALCULS, ensure_ascii=False, indent=1).replace("′", "’") + ";\n", encoding="utf-8")
print(len(slides), "diapositives ;", sum(1 for s in slides if s.get("question")), "questions ;", sum(len(s.get("exercises", [])) for s in slides), "exercices ;",
      sum(1 for s in slides for o in [s.get("question")] + list(s.get("exercises") or []) if o and o.get("demonstration")), "démonstrations ;", len(outils.CALCULS), "vues de calculs")
for c in comps: print(c["id"], len(c["slide_ids"]))
