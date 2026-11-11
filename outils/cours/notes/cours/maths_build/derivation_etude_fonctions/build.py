"""Build du cours math_ch2_derivation_etude_fonctions : python build.py [--garder-reponses]
Écrit backend/data/courses/math_ch2_derivation_etude_fonctions.json et calculs-vues.js (simulations derivation-tableau)."""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")
import outils
from p1 import PARTIE1, PARTIE2
from p2 import PARTIE3, PARTIE4
from p3 import PARTIE5, PARTIE6
from p4 import PARTIE7, PARTIE8, PARTIE9
from p5 import PARTIE10, PARTIE11, PARTIE12, BILAN

ID = "math_ch2_derivation_etude_fonctions"
ACTS = [
 ("df_partie1", "I. Pourquoi dériver ; le nombre dérivé", "situation", PARTIE1),
 ("df_partie2", "II. L'équation de la tangente", "explanation", PARTIE2),
 ("df_partie3", "III. À droite, à gauche : demi-tangentes et point anguleux", "explanation", PARTIE3),
 ("df_partie4", "IV. Calculer une dérivée", "explanation", PARTIE4),
 ("df_partie5", "V. Signe de f' et variations", "explanation", PARTIE5),
 ("df_partie6", "VI. Concavité et point d'inflexion", "explanation", PARTIE6),
 ("df_partie7", "VII. Branches infinies", "explanation", PARTIE7),
 ("df_partie8", "VIII. Position relative d'une courbe et d'une droite", "explanation", PARTIE8),
 ("df_partie9", "IX. Axe et centre de symétrie", "explanation", PARTIE9),
 ("df_partie10", "X. Construire et lire la courbe", "application", PARTIE10),
 ("df_partie11", "XI. Dérivée et courbe de la fonction réciproque", "explanation", PARTIE11),
 ("df_partie12", "XII. Le problème d'analyse : une étude complète", "evaluation", PARTIE12),
 ("df_bilan", "XIII. Bilan du chapitre", "evaluation", BILAN),
]
COMP = [
 ("K1", "Étudier la dérivabilité d'une fonction en un point, à droite et à gauche", ["DEF1"], "étudier la dérivabilité en un point"),
 ("K2", "Interpréter géométriquement et écrire l'équation d'une tangente ou d'une demi-tangente", ["DEF2"], "écrire et interpréter une tangente"),
 ("K3", "Calculer une dérivée (produit, quotient, uⁿ, √u, ⁿ√u)", ["DEF3"], "calculer une dérivée"),
 ("K4", "Dresser un tableau de variations, déterminer un extremum et un signe", ["DEF4", "DEF5"], "dresser un tableau de variations"),
 ("K5", "Étudier la concavité et déterminer un point d'inflexion", ["DEF6"], "étudier la concavité et le point d'inflexion"),
 ("K6", "Déterminer une branche infinie et l'interpréter par une phrase", ["DEF7"], "interpréter une branche infinie"),
 ("K7", "Étudier la position relative d'une courbe et d'une droite", ["DEF7"], "étudier la position relative"),
 ("K8", "Justifier un axe ou un centre de symétrie", ["DEF8"], "justifier un axe ou un centre de symétrie"),
 ("K9", "Construire une courbe à partir de son étude et la lire", ["DEF9"], "construire et lire une courbe"),
 ("K10", "Calculer la dérivée d'une fonction réciproque en un point et construire sa courbe", ["DEF10"], "dériver une fonction réciproque en un point"),
]
# options mélangées : la bonne réponse tourne sur les places (échange déterministe)
_k = 0
for _a in ACTS:
    for _s in _a[3]:
        for _o, _cle in [(_s.get("question"), "options")] + [(e, "choices") for e in _s.get("exercises", []) if e.get("type") == "qcm"]:
            if not _o or _cle not in _o: continue
            _t = (_k * 2 + 1) % len(_o[_cle]) if _k % 3 else _k % len(_o[_cle]); _k += 1; _c = _o["correct"]
            if _t != _c:
                _o[_cle][_t], _o[_cle][_c] = _o[_cle][_c], _o[_cle][_t]; _o["correct"] = _t
acts = [{"id": i, "title": t, "phase": ph, "duration_minutes": max(8, 3 * len(sl)), "slides": sl} for i, t, ph, sl in ACTS]
slides = [s for a in acts for s in a["slides"]]
ids = [s["id"] for s in slides]
assert len(ids) == len(set(ids)), "ids en double"
comps = [{"id": cid, "label": lab, "slide_ids": [s["id"] for s in slides if cid in s["competence_ids"]], "cadre_ids": cad, "dit": dit}
         for cid, lab, cad, dit in COMP]
deck = {
 "id": ID, "stable_id": ID,
 "title": "Dérivation et étude des fonctions", "version": 1, "status": "draft", "language": "fr",
 "estimated_minutes": sum(a["duration_minutes"] for a in acts), "mode": "concentration",
 "lesson_match": ["dérivation et étude des fonctions", "derivation et etude des fonctions", "dérivation", "étude des fonctions", "dérivabilité", "étude de fonctions 2 bac"],
 "catalog": {"summary": "Le cours au tableau, en mode concentration : de la sécante à la tangente, dérivabilité à droite et à gauche, demi-tangentes, calcul des dérivées, signe de f' et variations, concavité, branches infinies, position relative, symétrie, tracé de la courbe et dérivée de la fonction réciproque, avec les nationaux 2016 à 2025.",
             "cover_alt": "Une courbe à la craie, sa tangente en un point, une asymptote en pointillé et le tableau de variations dessous",
             "essential_topics": ["lim (f(x) − f(x₀))/(x − x₀) = f'(x₀)", "y = f'(x₀)(x − x₀) + f(x₀) ; demi-tangentes, point anguleux",
                                  "(u·v)', (u/v)', (uⁿ)', (√u)', (ⁿ√u)'", "Signe de f', tableau de variations, extremum", "f'' et point d'inflexion",
                                  "Asymptotes et branches paraboliques", "Position relative : signe de f(x) − y", "Axe et centre de symétrie, tracé",
                                  "(f⁻¹)'(y₀) = 1/f'(x₀)"]},
 "note": "Cours 2 de mathématiques (semestre 1), écrit en mode concentration d'après l'exploration (backend/data/curriculum/exploration/derivation_etude_fonctions.json) ; constructions à la craie dans frontend/public/media/simulations/maths/derivation-tableau/ (calculs-vues.js écrit par le build). Décisions : pas d'approximation affine chiffrée ; asymptote oblique à partir de la droite donnée (pas de division euclidienne) ; dérivée de ⁿ√u gardée (une diapositive) ; jamais « bijection » ; fonctions des exemples : polynômes, rationnelles, racines (ln et exp plus tard). Brouillon : voix Bodi à générer par la session principale ; validation par l'utilisateur.",
 "activities": acts, "competences": comps,
}

def lignes_y(d):
    y, yp = d.get("y0", 82), None
    for l in d["lignes"]:
        if l.get("meme"): y = yp
        yp = y
        if l.get("tab"):
            h = 30 + sum(62 if r.get("var") else 34 for r in l["tab"]["rows"])
            yb = y - 18 + h
            if yb > 362: outils.ERREURS.append(f"tableau trop bas (bas à {yb})")
            y += l.get("inter", h + 26)
        else:
            y += l.get("inter", round((l.get("taille") or d.get("taille") or 19) * 1.8))
    return yp
for vue, d in outils.CALCULS.items():
    yp = lignes_y(d)
    if yp > 356:
        outils.ERREURS.append(f"calculs {vue} : dernière ligne à y = {yp} (> 356)")
for s in slides:
    u = s["visual"].get("url", "")
    if "calculs.html?vue=" in u:
        vue = u.split("vue=")[1]
        L = outils.CALCULS[vue]["lignes"]
        ms = {l.get("m") for l in L} | {"fin"} | {r.get("m") for l in L if l.get("tab") for r in l["tab"]["rows"]}
        rs = {l["r"][0] for l in L if l.get("r")} | {r["r"][0] for l in L if l.get("tab") for r in l["tab"]["rows"] if r.get("r")} | {l["tab"]["r"][0] for l in L if l.get("tab") and l["tab"].get("r")}
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
js = Path(r"frontend/public/media/simulations/maths/derivation-tableau/calculs-vues.js")
js.write_text("/* Écrit par maths_build/derivation_etude_fonctions/build.py depuis les p*.py du cours math_ch2_derivation_etude_fonctions : ne pas modifier à la main. */\n"
              "window.CALCULS = " + json.dumps(outils.CALCULS, ensure_ascii=False, indent=1) + ";\n", encoding="utf-8")
nq = sum(1 for s in slides if s.get("question")); ne = sum(len(s.get("exercises", [])) for s in slides)
nd = sum(1 for s in slides for o in [s.get("question")] + s.get("exercises", []) if o and o.get("demonstration"))
print(len(slides), "diapositives ;", nq, "questions ;", ne, "exercices ;", nd, "démonstrations ;", len(outils.CALCULS), "vues de calculs")
for c in comps: print(c["id"], len(c["slide_ids"]))
