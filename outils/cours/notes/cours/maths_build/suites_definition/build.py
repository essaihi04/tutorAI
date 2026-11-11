"""Build du cours math_ch3_suites_numeriques : python build.py [--garder-reponses]
Écrit backend/data/courses/math_ch3_suites_numeriques.json et la page de données calculs-vues.js des simulations."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")
import outils
from p1 import PARTIE1
from p2 import PARTIE2, PARTIE3
from p3 import PARTIE4, PARTIE5
from p4 import PARTIE6, PARTIE7
from p5 import PARTIE8, BILAN

ID = "math_ch3_suites_numeriques"
ACTS = [
 ("su_partie1", "I. Une suite, ses termes ; arithmétique et géométrique", "situation", PARTIE1),
 ("su_partie2", "II. Le raisonnement par récurrence", "explanation", PARTIE2),
 ("su_partie3", "III. Majorée, minorée, bornée ; sens de variation", "explanation", PARTIE3),
 ("su_partie4", "IV. La suite auxiliaire", "explanation", PARTIE4),
 ("su_partie5", "V. Limites d'une suite", "explanation", PARTIE5),
 ("su_partie6", "VI. Convergence et comparaison", "explanation", PARTIE6),
 ("su_partie7", "VII. La suite uₙ₊₁ = f(uₙ)", "application", PARTIE7),
 ("su_partie8", "VIII. Problèmes : rang, somme, exercice complet", "evaluation", PARTIE8),
 ("su_bilan", "IX. Bilan du chapitre", "evaluation", BILAN),
]
COMP = [
 ("K1", "Calculer des termes et utiliser une suite arithmétique ou géométrique (raison, terme général, somme)", ["SU1"], "utiliser une suite arithmétique ou géométrique"),
 ("K2", "Démontrer par récurrence une minoration, une majoration ou un encadrement", ["SU2", "SU3"], "rédiger un raisonnement par récurrence"),
 ("K3", "Étudier le sens de variation d'une suite", ["SU4"], "étudier le sens de variation d'une suite"),
 ("K4", "Montrer qu'une suite auxiliaire est géométrique ou arithmétique et exprimer uₙ en fonction de n", ["SU5"], "utiliser une suite auxiliaire"),
 ("K5", "Calculer la limite d'une suite (suites de référence, qⁿ, nᵅ, opérations, f(uₙ))", ["SU6", "SU9"], "calculer la limite d'une suite"),
 ("K6", "Justifier qu'une suite converge et conclure par comparaison", ["SU7", "SU8"], "justifier la convergence et conclure par comparaison"),
 ("K7", "Étudier une suite uₙ₊₁ = f(uₙ) jusqu'à sa limite", ["SU10"], "étudier une suite u indice n plus un égale f de u indice n"),
 ("K8", "Résoudre un problème avec une suite : plus petit rang, somme et sa limite", ["SU11"], "trouver un rang et calculer une somme"),
]
# options mélangées : la bonne réponse tourne sur les trois places (échange déterministe)
_k = 0
for _a in ACTS:
    for _s in _a[3]:
        for _o, _cle in [(_s.get("question"), "options")] + [(e, "choices") for e in _s.get("exercises", []) if e.get("type") == "qcm"]:
            if not _o or _cle not in _o: continue
            _t = _k % len(_o[_cle]); _k += 1; _c = _o["correct"]
            if _t != _c:
                _o[_cle][_t], _o[_cle][_c] = _o[_cle][_c], _o[_cle][_t]; _o["correct"] = _t
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(10, 3 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = []
for cid, lab, cad, dit in COMP:
    comps.append({"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit})
# le bilan et la carte appartiennent à toutes les compétences (fiche et carte du chapitre)
for c in comps:
    for sid in ("su_e2_bilan", "su_e3_carte"):
        if sid not in c["slide_ids"]:
            c["slide_ids"].append(sid)
deck = {
 "id": ID, "stable_id": ID,
 "title": "Suites numériques", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["suites numériques", "suites numeriques", "les suites", "suites numériques 2 bac", "suite numérique"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : termes et rappels (arithmétique, géométrique, somme), raisonnement par récurrence, suites bornées, sens de variation, suite auxiliaire, limites (qⁿ, nᵅ, f(uₙ)), convergence et critère de comparaison, suite uₙ₊₁ = f(uₙ), problèmes, avec les nationaux 2016 à 2025.",
             "cover_alt": "Une rangée de cases u₀, u₁, u₂… à la craie, et l'escalier des termes entre une courbe et la droite y = x",
             "essential_topics": ["uₙ = uₚ + (n − p)r ; uₙ = uₚ·qⁿ⁻ᵖ ; sommes", "Récurrence : initialisation, hérédité, conclusion", "Majorée, minorée, bornée",
                                  "Sens de variation : uₙ₊₁ − uₙ, uₙ₊₁/uₙ", "Suite auxiliaire vₙ₊₁ = q·vₙ", "lim qⁿ, lim nᵅ, lim f(uₙ)",
                                  "Monotone et bornée ⇒ convergente ; critère de comparaison", "uₙ₊₁ = f(uₙ) : ℓ = f(ℓ)", "Plus petit rang, somme et sa limite"]},
 "note": "Cours 3 de mathématiques (semestre 1), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/suites_definition.json) ; constructions à la craie dans frontend/public/media/simulations/maths/suites-tableau/ (calculs-vues.js écrit par le build). Décisions : pas de suites adjacentes ; escalier de uₙ₊₁ = f(uₙ) comme construction (sans question notée) ; pas de ln ni d'exp (exemples rationnels, f7 avec g(x) = (4x + 3)/(x + 2)) ; « en déduire uₙ ≤ kⁿu₀ » par récurrence. Brouillon : voix Bodi à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}
# contrôle des vues de calculs : rien sous y = 356
for vue, d in outils.CALCULS.items():
    y, yp = d.get("y0", 82), None
    for l in d["lignes"]:
        if l.get("meme"): y = yp
        yp = y
        y += l.get("inter", round((l.get("taille") or d.get("taille") or 19) * 1.8))
    if yp > 356:
        outils.ERREURS.append(f"calculs {vue} : dernière ligne à y = {yp} (> 356)")
# chaque moment cité d'une vue de calculs existe
for s in slides:
    u = s["visual"].get("url", "")
    if "calculs.html?vue=" in u:
        vue = u.split("vue=")[1]
        ms = {l.get("m") for l in outils.CALCULS[vue]["lignes"]} | {"fin"}
        rs = {l["r"][0] for l in outils.CALCULS[vue]["lignes"] if l.get("r")}
        for p in s["concentration"]["pointage"]:
            if p.get("commande") == "play_until" and p["parametres"]["moment"] not in ms:
                outils.ERREURS.append(f"{s['id']}: moment {p['parametres']['moment']} absent de calculs {vue}")
            if p.get("repere") and p["repere"] not in rs:
                outils.ERREURS.append(f"{s['id']}: repère {p['repere']} absent de calculs {vue}")
if outils.ERREURS:
    print("\n".join(outils.ERREURS)); sys.exit(1)
out = Path(r"backend/data/courses") / f"{ID}.json"
if out.exists() and "--garder-reponses" in sys.argv:
    old = json.loads(out.read_text(encoding="utf-8"))
    oldr = {s["id"]: s.get("concentration", {}).get("reponses") for a in old["activities"] for s in a["slides"]}
    for s in slides:
        if oldr.get(s["id"]): s["concentration"]["reponses"] = oldr[s["id"]]
out.write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
js = Path(r"frontend/public/media/simulations/maths/suites-tableau/calculs-vues.js")
js.write_text("/* Écrit par maths_build/suites_definition/build.py depuis les p*.py du cours math_ch3_suites_numeriques : ne pas modifier à la main. */\n"
              "window.CALCULS = " + json.dumps(outils.CALCULS, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
nq = sum(1 for s in slides if s.get("question")); ne = sum(len(s.get("exercises", [])) for s in slides)
nd = sum(1 for s in slides for o in [s.get("question")] + s.get("exercises", []) if o and o.get("demonstration"))
print(len(slides), "diapositives ;", nq, "questions ;", ne, "exercices ;", nd, "démonstrations ;", len(outils.CALCULS), "vues de calculs")
for c in comps: print(c["id"], len(c["slide_ids"]))
