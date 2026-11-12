"""Écrit methode_blocs/ajouts/math_ch5_fonctions_ln.json (séances, rappels, prédictions) depuis le cours construit.
Découpage, rappels et prédictions : plan de l'exploration (backend/data/curriculum/exploration/fonctions_ln.json)."""
import json
from pathlib import Path
COURS = Path(r"backend/data/courses/math_ch5_fonctions_ln.json")
OUT = Path(__file__).resolve().parents[2] / "methode_blocs/ajouts/math_ch5_fonctions_ln.json"
d = json.loads(COURS.read_text(encoding="utf-8"))
S = {s["id"]: s for a in d["activities"] for s in a["slides"]}
plan = json.loads(Path("backend/data/curriculum/exploration/fonctions_ln.json").read_text(encoding="utf-8"))["plan"]

SEANCES = [
 ("Séance 1 — La naissance de ln et sa courbe", [
   ("Pourquoi une fonction nouvelle", ["o1", "o2", "n1", "n2"], "K1",
    "Cahier fermé : écris la définition de ln.", "ln est la primitive de x ↦ 1/x sur ]0 ; +∞[ qui s'annule en 1"),
   ("ln 1 = 0, (ln x)' = 1/x ; croissance et signe", ["n3", "n4", "c1", "c2"], "K1",
    "Cahier fermé : écris ln 1 et la dérivée de ln.", "ln 1 = 0 et (ln x)' = 1/x sur ]0 ; +∞["),
   ("Le nombre e, comparer, la tangente ; un ln, une condition", ["c3", "c4", "c5", "d1"], "K1",
    "Cahier fermé : écris la valeur de ln e et une valeur approchée de e.", "ln e = 1 (e ≈ 2,718)"),
 ]),
 ("Séance 2 — Domaine et règles de calcul", [
   ("Tableau de signe, « et », ln|u| ; ln 6 = ln 2 + ln 3", ["d2", "d3", "d4", "a1"], "K2",
    "Cahier fermé : écris la condition d'existence de ln(u(x)).", "x ∈ D_f ⇔ u(x) > 0"),
   ("Produit, inverse, quotient, puissance ; simplifier", ["a2", "a3", "a4", "a5"], "K3",
    "Cahier fermé : écris la règle du logarithme d'un produit.", "ln(ab) = ln a + ln b"),
   ("Les pièges, ln(eʳ) = r ; la première équation", ["a6", "a7", "a8", "q1"], "K3",
    "Cahier fermé : que vaut ln(eʳ) ?", "ln(eʳ) = r"),
 ]),
 ("Séance 3 — Équations, inéquations, premières limites", [
   ("ln x = r, inéquation, second degré, produit nul", ["q2", "q3", "q4", "q5"], "K4",
    "Cahier fermé : écris les deux règles qui permettent d'enlever les ln.", "ln a = ln b ⇔ a = b ; ln a < ln b ⇔ a < b (a > 0, b > 0)"),
   ("Système, plus petit entier n ; ln en +∞ et en 0", ["q6", "q7", "l1", "l2"], "K5",
    "Cahier fermé : écris les limites de ln x en +∞ et en 0 à droite.", "lim_{x→+∞} ln x = +∞ ; lim_{x→0⁺} ln x = −∞"),
   ("x l'emporte ; le nombre dérivé ; factoriser", ["l3", "l4", "l5", "l6"], "K5",
    "Cahier fermé : écris les deux croissances comparées de base.", "lim_{x→+∞} (ln x)/x = 0 ; lim_{x→0⁺} x ln x = 0"),
 ]),
 ("Séance 4 — Limites déguisées, dérivée de ln u, primitives u'/u", [
   ("t = √x ; continuité en 0 ; (ln u)' = u'/u", ["l7", "l8", "v1"], "K6",
    "Cahier fermé : écris la dérivée de ln u.", "(ln u)' = u'/u (u > 0 sur I)"),
   ("(ln x)², le signe de f' ; à l'envers : u'/u", ["v2", "v3", "p1"], "K7",
    "Cahier fermé : écris une primitive de u'/u.", "u'/u → ln|u|"),
   ("ln|u| ; vérifier une primitive ; ln x ≤ x − 1", ["p2", "p3", "e1"], "K8",
    "Cahier fermé : écris l'inégalité entre ln x et x − 1.", "ln x ≤ x − 1 pour tout x > 0"),
 ]),
 ("Séance 5 — Le problème du national, log, bilan et carte", [
   ("Le problème : g, limites, tableau, position", ["e2", "e3", "e4", "e5"], "K8",
    "Cahier fermé : écris l'équation de la tangente à la courbe de ln au point d'abscisse 1.", "y = x − 1 (tangente à la courbe de ln au point d'abscisse 1)"),
   ("log et pH ; ce qu'il faut retenir ; la carte", ["g1", "g2", "b1", "b2"], "K9",
    "Cahier fermé : écris log x en fonction de ln.", "log x = ln x / ln 10"),
 ]),
]

def exercice(sids):
    cands = []
    for sid in sids:
        for i, e in enumerate(S[sid].get("exercises", [])):
            score = (2 if e.get("demonstration") else 0) + (1 if e["type"] == "qcm" else 0)
            cands.append((score, sid, i, e))
    cands.sort(key=lambda t: -t[0])
    _, sid, i, e = cands[0]
    x = {"type": e["type"], "reprend": f"{sid}/e{i}", "prompt": e["prompt"]}
    if e["type"] == "vrai_faux":
        x["statements"] = e["statements"]
    else:
        x["options"] = e["choices"]; x["correct"] = e["correct"]; x["explanation"] = e["explanation"]
    if e.get("demonstration"):
        x["demonstration"] = e["demonstration"]
    return x

seances = []
for n, (titre, blocs) in enumerate(SEANCES, 1):
    bl = []
    for k, (bt, ids, comp, prompt, attendu) in enumerate(blocs, 1):
        sids = ["ln_" + i for i in ids]
        assert any(comp in S[s]["competence_ids"] for s in sids), (bt, comp)
        cahier = [{"texte": S[s]["concentration"]["cahier"]} for s in sids if S[s]["concentration"].get("cahier")][:4]
        bl.append({"id": f"ln_s{n}_b{k}", "titre": bt, "slide_ids": sids, "cahier": cahier,
                   "retrouver": {"prompt": prompt, "attendu": attendu, "competence_id": comp},
                   "exercice": exercice(sids)})
    seances.append({"id": f"ln_s{n}", "titre": titre, "blocs": bl})
ordre = [s["id"] for a in d["activities"] for s in a["slides"]]
assert [s for se in seances for b in se["blocs"] for s in b["slide_ids"]] == ordre

RAPPELS = {c["id"]: c["rappels"] for c in plan["competences"]}
PRED = ["ln_" + s["id"] for s in plan["diapositives"] if s.get("prediction")]
OUT.write_text(json.dumps({"seances": seances, "rappels": RAPPELS, "predictions": PRED}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok", OUT, sum(len(s["blocs"]) for s in seances), "blocs ;", len(PRED), "prédictions ;", sum(len(v) for v in RAPPELS.values()), "rappels")
