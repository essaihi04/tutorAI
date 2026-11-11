"""Écrit methode_blocs/ajouts/math_ch4_primitives.json (séances, rappels, prédictions) depuis le cours construit."""
import json
from pathlib import Path
COURS = Path(r"backend/data/courses/math_ch4_primitives.json")
OUT = Path(__file__).resolve().parents[2] / "methode_blocs/ajouts/math_ch4_primitives.json"
d = json.loads(COURS.read_text(encoding="utf-8"))
S = {s["id"]: s for a in d["activities"] for s in a["slides"]}

SEANCES = [
 ("Séance 1 — Dériver à l'envers : définition et vérification", [
   ("Primitiver : la dérivation à l'envers", ["o1", "o2", "d1"], "K1",
    "Cahier fermé : écris la relation entre F′ et f quand F est une primitive de f sur I.", "F'(x) = f(x) pour tout x ∈ I"),
   ("Définition et vérification d'une primitive", ["d2", "d3", "d4"], "K1",
    "Cahier fermé : écris la définition complète de « F est une primitive de f sur I ».", "F est une primitive de f sur I si F est dérivable sur I et F'(x) = f(x) pour tout x ∈ I"),
   ("Existence ; toujours un intervalle ; une infinité", ["e1", "e2", "e3"], "K2",
    "Cahier fermé : écris la propriété qui garantit l'existence de primitives.", "f continue sur I ⇒ f admet des primitives sur I"),
 ]),
 ("Séance 2 — Toutes les primitives, la condition, le tableau", [
   ("Toutes les primitives : F + k ; la condition F(x₀) = y₀", ["e4", "e5", "e6", "e7"], "K3",
    "Cahier fermé : G et F sont deux primitives de f sur I ; écris G(x) en fonction de F(x).", "G(x) = F(x) + k, k ∈ ℝ"),
   ("Le tableau : k, xⁿ, le coefficient devant", ["u1", "u2", "u3"], "K4",
    "Cahier fermé : écris une primitive de xⁿ (n ∈ ℕ*).", "xⁿ → xⁿ⁺¹/(n + 1)"),
   ("1/xⁿ, racines, cos et sin", ["u4", "u5", "u6"], "K4",
    "Cahier fermé : écris une primitive de 1/√x sur ]0 ; +∞[.", "1/√x → 2√x"),
 ]),
 ("Séance 3 — cos(ax + b), somme, produit, et la forme u′uⁿ", [
   ("cos(ax + b), 1 + tan²x, une somme", ["u7", "u8", "l1"], "K4",
    "Cahier fermé : écris la règle des primitives d'une somme et d'un produit par un réel α.", "f + g → F + G ; αf → αF"),
   ("Pas facteur par facteur ; transformer ; d'où vient u′uⁿ", ["l2", "l3", "c1"], "K5",
    "Cahier fermé : écris une primitive de u′uⁿ (n ∈ ℕ*).", "u'uⁿ → uⁿ⁺¹/(n + 1)"),
   ("La bulle : faire apparaître u′", ["c2", "c3", "c4"], "K5",
    "Cahier fermé : quelle forme reconnais-tu quand la dérivée de la parenthèse est devant ? Écris sa primitive.", "u'uⁿ → uⁿ⁺¹/(n + 1)"),
 ]),
 ("Séance 4 — Les autres formes, les dérivées reconnues, le lien graphique", [
   ("u′uʳ, u′/u², u′/√u", ["c5", "c6", "c7"], "K6",
    "Cahier fermé : écris une primitive de u′/u².", "u'/u² → −1/u"),
   ("Choisir la forme ; u′cos u ; reconnaître u′v + uv′", ["c8", "c9", "r1"], "K6",
    "Cahier fermé : écris une primitive de u′·cos u et une primitive de u′·sin u.", "u'·cos u → sin u ; u'·sin u → −cos u"),
   ("Quotient reconnu, organigramme, f pente de F", ["r2", "r3", "g1", "g2"], "K8",
    "Cahier fermé : que dit le signe de f sur les primitives de f ?", "F' = f : f ≥ 0 sur I ⇒ F croissante sur I"),
 ]),
 ("Séance 5 — Types national, bilan et carte", [
   ("Trois exercices type national", ["x1", "x2", "x3"], "K2",
    "Cahier fermé : comment justifies-tu que f admet des primitives sur I ?", "f continue sur I ⇒ f admet des primitives sur I"),
   ("Ce qui viendra ; ce qu'il faut retenir ; la carte", ["x4", "b1", "b2"], "K4",
    "Cahier fermé : écris une primitive de sin x (attention au signe).", "sin x → −cos x"),
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
        sids = ["pr_" + i for i in ids]
        assert any(comp in S[s]["competence_ids"] for s in sids), (bt, comp)
        cahier = [{"texte": S[s]["concentration"]["cahier"]} for s in sids][:4]
        bl.append({"id": f"pr_s{n}_b{k}", "titre": bt, "slide_ids": sids, "cahier": cahier,
                   "retrouver": {"prompt": prompt, "attendu": attendu, "competence_id": comp},
                   "exercice": exercice(sids)})
    seances.append({"id": f"pr_s{n}", "titre": titre, "blocs": bl})
ordre = [s["id"] for a in d["activities"] for s in a["slides"]]
assert [s for se in seances for b in se["blocs"] for s in b["slide_ids"]] == ordre

def qcm(id, p, o, c): return {"id": id, "type": "qcm", "prompt": p, "options": o, "correct": c}
def lib(id, p, a): return {"id": id, "type": "libre", "prompt": p, "attendu": a}
def vf(id, p, c): return {"id": id, "type": "vrai_faux", "prompt": p, "correct": c}
RAPPELS = {
 "K1": [qcm("K1_r1", "F(x) = x³ + 2x est une primitive sur ℝ de :", ["3x² + 2", "x⁴/4 + x²", "3x²"], 0),
        vf("K1_r2", "F(x) = sin x + 7 est une primitive de cos x sur ℝ.", True),
        lib("K1_r3", "Complète la définition : F est une primitive de f sur l'intervalle I si…", "F est dérivable sur I et F'(x) = f(x) pour tout x ∈ I"),
        qcm("K1_r4", "Pour montrer que F est une primitive de f sur I, on :", ["vérifie que F(0) = f(0)", "calcule une primitive de F", "dérive F et on trouve F′(x) = f(x) pour tout x de I"], 2)],
 "K2": [qcm("K2_r1", "f(x) = √x + x² admet des primitives sur :", ["ℝ", "[0 ; +∞[", "]−∞ ; 0]"], 1),
        vf("K2_r2", "On peut chercher les primitives de 1/x² sur ℝ* tout entier, avec une seule constante.", False),
        lib("K2_r3", "Complète : si f est continue sur l'intervalle I, alors…", "f admet des primitives sur I")],
 "K3": [lib("K3_r1", "x³ est une primitive de 3x² sur ℝ. Écris toutes les primitives de 3x² sur ℝ.", "x ↦ x³ + k, k ∈ ℝ"),
        qcm("K3_r2", "f(x) = 4x³ sur ℝ : la primitive F de f telle que F(1) = 0 est :", ["F(x) = x⁴ − 1", "F(x) = x⁴", "F(x) = x⁴ + 1"], 0),
        vf("K3_r3", "Parmi les primitives de f sur I, une seule vérifie F(x₀) = y₀.", True),
        qcm("K3_r4", "G et F sont deux primitives de f sur un intervalle I. G(x) − F(x) est :", ["égal à f(x)", "nul en un seul point", "une constante"], 2)],
 "K4": [qcm("K4_r1", "Une primitive de x⁴ sur ℝ :", ["4x³", "x⁵/5", "x⁵"], 1),
        qcm("K4_r2", "Une primitive de sin x sur ℝ :", ["cos x", "−cos x", "−sin x"], 1),
        lib("K4_r3", "Écris une primitive de 1/x³ sur ]0 ; +∞[.", "−1/(2x²)"),
        vf("K4_r4", "Une primitive de cos(3x) sur ℝ est 3 sin(3x).", False)],
 "K5": [qcm("K5_r1", "Une primitive de 2x(x² + 1)³ sur ℝ :", ["(x² + 1)⁴/4", "(x² + 1)⁴", "2x(x² + 1)⁴/4"], 0),
        lib("K5_r2", "Écris une primitive de u′uⁿ (n ∈ ℕ*).", "uⁿ⁺¹/(n + 1)"),
        qcm("K5_r3", "Une primitive de (3x + 1)² sur ℝ :", ["(3x + 1)³/3", "(3x + 1)³/9", "3(3x + 1)³"], 1)],
 "K6": [qcm("K6_r1", "Une primitive de 2x/(x² + 1)² sur ℝ :", ["−1/(x² + 1)", "1/(x² + 1)", "−2x/(x² + 1)"], 0),
        lib("K6_r2", "Écris une primitive de u′/√u (u > 0 sur I).", "2√u"),
        vf("K6_r3", "Une primitive de 2x·cos(x²) sur ℝ est sin(x²).", True),
        qcm("K6_r4", "Une primitive de 1/√(x + 3) sur ]−3 ; +∞[ :", ["√(x + 3)", "2√(x + 3)", "1/(2√(x + 3))"], 1)],
 "K7": [qcm("K7_r1", "Une primitive de cos x − x sin x sur ℝ :", ["sin x + x cos x", "x cos x", "−x sin x"], 1),
        vf("K7_r2", "Une primitive de x·cos x sur ℝ est (x²/2)·sin x.", False),
        lib("K7_r3", "Écris une primitive de (x³ + 2)/x² sur ]0 ; +∞[ (sépare d'abord la fraction).", "x²/2 − 2/x")],
 "K8": [qcm("K8_r1", "f(x) = 2 − x et F une primitive de f sur ℝ : F est croissante sur :", ["]−∞ ; 2]", "[2 ; +∞[", "ℝ"], 0),
        vf("K8_r2", "Si f est positive sur I, toute primitive de f est croissante sur I.", True),
        qcm("K8_r3", "f(2) = 0 et f change de signe en 2 : en x = 2, la tangente à la courbe de F est :", ["verticale", "horizontale", "de pente 2"], 1)],
}
PRED = ["o1", "d1", "e2", "e3", "e5", "u2", "u4", "u6", "u7", "l2", "c1", "c4", "c8", "r3", "g1", "x3"]
OUT.write_text(json.dumps({"seances": seances, "rappels": RAPPELS, "predictions": ["pr_" + p for p in PRED]}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok", OUT, sum(len(s["blocs"]) for s in seances), "blocs")
