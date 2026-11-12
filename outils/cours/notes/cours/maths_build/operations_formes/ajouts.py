"""Écrit methode_blocs/ajouts/math_ch6_nombres_complexes.json (séances, rappels, prédictions) depuis le cours construit.
Découpage, rappels et prédictions : plan de l'exploration (backend/data/curriculum/exploration/operations_formes.json)."""
import json
from pathlib import Path
COURS = Path(r"backend/data/courses/math_ch6_nombres_complexes.json")
OUT = Path(__file__).resolve().parents[2] / "methode_blocs/ajouts/math_ch6_nombres_complexes.json"
d = json.loads(COURS.read_text(encoding="utf-8"))
S = {s["id"]: s for a in d["activities"] for s in a["slides"]}
plan = json.loads(Path("backend/data/curriculum/exploration/operations_formes.json").read_text(encoding="utf-8"))["plan"]
SID = {"b1": "nc_b1_bilan", "b2": "nc_b2_carte"}

SEANCES = [
 ("Séance 1 — Le nombre i et le calcul algébrique", [
   ("Le nombre i : un quart de tour", ["o1", "o2", "a1", "a2"], "K1",
    "Cahier fermé : quel est le carré de i ?", "i² = −1"),
   ("La forme algébrique, réels et imaginaires purs, égalité, puissances de i", ["a3", "a4", "a5", "a6"], "K1",
    "Cahier fermé : écris la forme algébrique d'un complexe z et nomme ses parties.", "z = a + ib, avec a = Re(z) et b = Im(z) réels"),
   ("Produit, carré, conjugué, quotient", ["c1", "c2", "c3", "c4"], "K2",
    "Cahier fermé : que vaut (a + ib)(a − ib) ?", "(a + ib)(a − ib) = a² + b²"),
 ]),
 ("Séance 2 — Le plan complexe : affixe, conjugué, module", [
   ("Un complexe, un point : affixes d'un point, d'un vecteur, du milieu", ["p1", "p2", "p3", "p4"], "K3",
    "Cahier fermé : écris l'affixe du vecteur AB.", "z_AB = z_B − z_A"),
   ("Le conjugué : le reflet", ["j1", "j2", "j3", "j4"], "K4",
    "Cahier fermé : écris z + z̄ et z − z̄.", "z + z̄ = 2Re(z) ; z − z̄ = 2i Im(z)"),
   ("Le module : une distance", ["m1", "m2", "m3", "m4"], "K5",
    "Cahier fermé : écris la distance AB avec les affixes.", "AB = |z_B − z_A|"),
 ]),
 ("Séance 3 — Argument et forme trigonométrique", [
   ("L'argument : un angle à 2π près", ["g1", "g2", "g3", "g4"], "K6",
    "Cahier fermé : écris cos θ et sin θ avec a, b et |z|.", "cos θ = a/|z| et sin θ = b/|z|"),
   ("La forme trigonométrique et les signes", ["t1", "t2", "t3", "t4"], "K6",
    "Cahier fermé : écris la forme trigonométrique de z.", "z = r(cos θ + i sin θ), r = |z| > 0, θ ≡ arg z [2π]"),
   ("Retour à a + ib ; le produit fait tourner", ["t5", "t6", "r1", "r2"], "K7",
    "Cahier fermé : écris l'argument d'un produit.", "arg(zz′) ≡ arg z + arg z′ [2π]"),
 ]),
 ("Séance 4 — Produit, Moivre, géométrie et sujets nationaux", [
   ("Quotient, inverse, conjugué ; déduire ; identifier ; Moivre", ["r3", "r4", "r5", "r6"], "K7",
    "Cahier fermé : écris la formule de Moivre.", "(cos θ + i sin θ)ⁿ = cos nθ + i sin nθ"),
   ("Puissances réelles ; alignement ; égalité de distances", ["r7", "r8", "i1", "i2"], "K8",
    "Cahier fermé : quand trois points A, B, C sont-ils alignés ?", "A, B, C alignés ⇔ (z_C − z_A)/(z_B − z_A) ∈ ℝ"),
   ("Deux sujets nationaux ; ce qu'il faut retenir ; la carte", ["n1", "n2", "b1", "b2"], "K2",
    "Cahier fermé : comment écrit-on un quotient sous forme algébrique ?", "(a + ib)/(c + id) = (a + ib)(c − id)/(c² + d²)"),
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

def sid(i): return SID.get(i, "nc_" + i)

seances = []
for n, (titre, blocs) in enumerate(SEANCES, 1):
    bl = []
    for k, (bt, ids, comp, prompt, attendu) in enumerate(blocs, 1):
        sids = [sid(i) for i in ids]
        assert any(comp in S[s]["competence_ids"] for s in sids), (bt, comp, [S[s]["competence_ids"] for s in sids])
        cahier = [{"texte": S[s]["concentration"]["cahier"]} for s in sids if S[s]["concentration"].get("cahier")][:4]
        bl.append({"id": f"nc_s{n}_b{k}", "titre": bt, "slide_ids": sids, "cahier": cahier,
                   "retrouver": {"prompt": prompt, "attendu": attendu, "competence_id": comp},
                   "exercice": exercice(sids)})
    seances.append({"id": f"nc_s{n}", "titre": titre, "blocs": bl})
ordre = [s["id"] for a in d["activities"] for s in a["slides"]]
assert [s for se in seances for b in se["blocs"] for s in b["slide_ids"]] == ordre

# Rappels du plan ; la bonne réponse des QCM déplacée pour ne pas être toujours au même rang.
RAPPELS = {}
for c in plan["competences"]:
    rs = json.loads(json.dumps(c["rappels"], ensure_ascii=False))
    for j, r in enumerate(rs):
        if r["type"] == "qcm":
            opts = r["options"]; bon = opts[r["correct"]]
            cible = (j + len(c["id"])) % len(opts)
            autres = [o for o in opts if o != bon]
            autres.insert(cible, bon)
            r["options"] = autres; r["correct"] = cible
    RAPPELS[c["id"]] = rs
PRED = [sid(s["id"]) for s in plan["diapositives"] if s.get("prediction")]
OUT.write_text(json.dumps({"seances": seances, "rappels": RAPPELS, "predictions": PRED}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
print("ok", OUT, sum(len(s["blocs"]) for s in seances), "blocs ;", len(PRED), "prédictions ;", sum(len(v) for v in RAPPELS.values()), "rappels")
