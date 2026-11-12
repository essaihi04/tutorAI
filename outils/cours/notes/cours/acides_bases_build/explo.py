"""Assemble l'exploration acides_bases (explo_a + explo_b), vérifie et écrit
backend/data/curriculum/exploration/acides_bases.json.
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/acides_bases_build/explo.py"""
import json, math, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from explo_a import *
from explo_b import *

RACINE = Path(__file__).resolve().parents[5]
CONTRAT = RACINE / "outils/cours/notes/cours/acides_bases_contrat_simulations.md"
SORTIE = RACINE / "backend/data/curriculum/exploration/acides_bases.json"
PERIMETRE = RACINE / "backend/data/curriculum/perimetre.json"
PROGRAMME = RACINE / "backend/data/curriculum/programme_semestre1.json"
KIT = RACINE / "frontend/public/media/simulations/chimie/acides-bases-tableau"

ORDRE = ("o1 o2 r1 r2 w1 w2 w3 w4 w5 b1 b2 b3 a1 a2 a3 a4 a5 c1 c2 c3 k1 k2 k3 k4 "
         "p1 p2 p3 p4 i1 i2 d1 d2 d3 d4 d5 d6 e1 e2 e3 e4 e5 n1 n2 n3 n4 n5 bl cr").split()
FIGS = {"p4": "fig_2025R", "n1": "fig_2016N", "n2": "fig_2022R", "n3": "fig_2022N", "n4": "fig_2024R"}

ex = {**ENTETE, "sources": SOURCES, "comparaison": COMPARAISON, "cadre": CADRE, "insistances": INSISTANCES,
      "valeurs_reperes": VALEURS_REPERES, "cas_types": CAS_TYPES, "pieges": PIEGES, "erreurs_examen": ERREURS_EXAMEN,
      "conseils": CONSEILS, "analogies_validees": ANALOGIES, "a_ne_pas_dire": A_NE_PAS_DIRE, "exclus_hors_programme": EXCLUS,
      "questions_eleves": QUESTIONS_ELEVES, "commentaires_eleves": COMMENTAIRES, "notions_complexes": NOTIONS,
      "cours_existant": COURS_EXISTANT, "visuels": VISUELS, "regles_des_simulations": REGLES_SIMULATIONS,
      "redaction_nationale": REDACTION, "plan": PLAN, "renvois": RENVOIS, "decisions_utilisateur": DECISIONS,
      "limites_de_l_exploration": LIMITES}

# ---- 0. kit copié
for f in ["commun.js", "exposants.js", "ab.css"]:
    assert (KIT / f).is_file(), f

# ---- 1. plan : ids, séances (4 × 3 blocs × 4), parties, champs, prédictions
ids = [d["id"] for d in DIAPOS]
assert ids == ORDRE, ids
assert len(DIAPOS) == 48 and len(SEANCES) == 4
assert all(len(s["blocs"]) == 3 and all(len(b) == 4 for b in s["blocs"]) for s in SEANCES)
assert [x for s in SEANCES for b in s["blocs"] for x in b] == ORDRE
assert SEANCES[0]["blocs"][0][:2] == ["o1", "o2"] and SEANCES[-1]["blocs"][-1][-2:] == ["bl", "cr"]
for s in SEANCES:                                # parties : couvrent la séance, dans l'ordre, titres « I. … »
    assert [x for p in s["parties"] for x in p["ids"]] == [x for b in s["blocs"] for x in b], s["n"]
    assert all(p["titre"] == "Ouverture" or re.match(r"^[IVX]+\. ", p["titre"]) for p in s["parties"]), s["n"]
assert all(len(i) == 2 for i in ORDRE)
CHAMPS = ["id", "title", "lead", "marche", "visuel", "question", "prediction", "competences", "demonstration"]
comp_ids = {c["id"] for c in COMPETENCES}
for d in DIAPOS:
    assert list(d) == CHAMPS, d["id"]
    assert all(d[k] for k in ["title", "lead", "marche", "visuel", "question", "competences"]), d["id"]
    assert set(d["competences"]) <= comp_ids, d["id"]
pred = {d["id"] for d in DIAPOS if d["prediction"]}
assert len(pred) >= 16 and 3 * len(pred) >= len(DIAPOS) and not pred & {"bl", "cr"}, len(pred)
for s in SEANCES:
    for b in s["blocs"]:
        assert set(b) & pred, b
CALC = re.compile(r"calcul|combien|trouve|d[ée]termine|[ée]tablis|montre|v[ée]rifie|que vaut|d[ée]duis", re.I)
for d in DIAPOS:                                 # une question de calcul porte sa démonstration
    if CALC.search(d["question"]):
        assert d["demonstration"], d["id"]

# ---- 2. visuels = « Diapositives servies » du contrat (une ligne par diapositive)
contrat = CONTRAT.read_text(encoding="utf-8")
servies = contrat.split("## Diapositives servies")[1]
lignes = [l for l in (x.strip() for x in servies.splitlines()) if l and not l.startswith(("#", "("))]
assert [l.split()[0] for l in lignes] == ORDRE, "ordre du contrat"
for d, l in zip(DIAPOS, lignes):
    assert l == f"{d['id']} {d['visuel']}", (d["id"], d["visuel"], l)
    if d["id"] in FIGS:
        assert d["visuel"] == f"figures?fig={FIGS[d['id']]}", d["id"]
    elif d["id"] in ("bl", "cr", "o1"):
        assert d["visuel"] == {"bl": "bilan", "cr": "carte", "o1": "carte"}[d["id"]]
    else:
        page, vue = d["visuel"].split("?vue=")
        assert re.search(rf"## \d\. {page}\.html", contrat) and f"`?vue={vue}`" in contrat, (d["id"], d["visuel"])
for f in FIGS.values():
    assert f"`{f}`" in contrat, f
pages = re.findall(r"^## \d\. (\w+)\.html", contrat, re.M)
assert 5 <= len([p for p in pages if p not in ("figures", "bilan")]) <= 7, pages
assert "Math.max" in contrat and "etat-equilibre-tableau" in contrat      # moteur corrigé imposé
for m in re.findall(r"(?:Moments|Repères|moments|repères) : ((?:`[^`]+`\s*)+)", contrat):   # noms en minuscules, chiffres et _
    for t in re.findall(r"`([^`]+)`", m):
        assert re.fullmatch(r"[a-z0-9_]+", t), t
agents = VISUELS["agents_simulations"]
assert len(agents) <= 4 and sorted(p for v in agents.values() for p in v) == sorted([p + ".html" for p in pages if p != "bilan"] + ["bilan.html", "carte.html"])

# ---- 3. compétences (3–4 rappels de types variés), capacités, formules
for c in COMPETENCES:
    assert 3 <= len(c["rappels"]) <= 4 and len({r["type"] for r in c["rappels"]}) >= 2, c["id"]
    assert c["cadre_ids"] and c["dit"], c["id"]
caps = {}
cc = {c["id"]: c["cadre_ids"] for c in COMPETENCES}
for d in DIAPOS:
    for c in d["competences"]:
        for k in cc[c]:
            caps.setdefault(k, []).append(d["id"])
assert set(caps) == {c["id"] for c in CADRE["capacites"]}, set(caps)
formules = {f["ecriture"] for f in CADRE["formules"]}
assert all(f["dit"] for f in CADRE["formules"])
for f in formules:
    assert f in contrat, ("formule absente du contrat", f)
texte_diapos = json.dumps(DIAPOS, ensure_ascii=False)
for f in ["Ke = [H₃O⁺]·[HO⁻]", "[HO⁻] = Ke/[H₃O⁺]", "Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq", "pKa = −log Ka", "Ka = Ke/Qr,éq",
          "K = Ka₁/Ka₂", "K = 10^(pKa₂ − pKa₁)", "K = Ka/Ke", "pH = pKa + log([A⁻]_éq/[AH]_éq)", "C_A·V_A = C_B·V_BE",
          "C_B·V_B = C_A·V_AE", "pH = pKa à V_B = V_BE/2", "τ = [HO⁻]_éq/C", "pKe = −log Ke = 14", "2H₂O ⇌ H₃O⁺ + HO⁻"]:
    assert f in formules and f in texte_diapos, f

# ---- 4. vocabulaire : hors cadre absent des diapositives, rappels et du contrat (hors ligne « Jamais »)
perimetre = json.loads(PERIMETRE.read_text(encoding="utf-8"))
chap = perimetre["matieres"]["Physique-Chimie"]["chapitres"]
hp = [t for k in ("acides_bases", "dosage", "esterification_hydrolyse", "piles_electrolyse") for t in chap[k]["termes_hors_programme"]]
assert "critère d'évolution spontanée" in chap["piles_electrolyse"]["termes_programme"]       # renvoyé au semestre 2
programme = json.loads(PROGRAMME.read_text(encoding="utf-8"))
cles = [c["cle"] for c in programme["Physique-Chimie"]]
assert "acides_bases" in cles and "dosage" not in cles                                           # décision : le dosage reste ici
mots = CADRE["hors_cadre"]["mots"]
for m in ["Henderson", "Hasselbalch", "Flood", "Lewis", "Arrhenius", "Ostwald", "degré d'ionisation", "coefficient de dissociation",
          "activité chimique", "pouvoir tampon", "Le Chatelier", "dosage potentiométrique", "critère d'évolution spontanée",
          "évolution spontanée", "enthalpie"]:
    assert m in mots, m
texte_cours = json.dumps([DIAPOS, COMPETENCES], ensure_ascii=False)
contrat_sans_jamais = "\n".join(l for l in contrat.splitlines() if "Jamais" not in l)
def present(m, t):
    return re.search(rf"(?<![\w]){re.escape(m)}(?![\w])", t, re.I) if len(m) <= 3 else m.lower() in t.lower()
for m in mots:
    assert not present(m, texte_cours), m
    assert not present(m, contrat_sans_jamais), ("contrat", m)
for m in ["autoprotolyse", "produit ionique", "constante d'acidité", "pKa", "prédomin", "diagramme de distribution", "indicateur coloré",
          "zone de virage", "équivalence", "demi-équivalence", "méthode des tangentes", "solution titrante"]:   # mots permis bien présents
    assert m.lower() in texte_cours.lower(), m
for t in hp:                                     # termes hors programme de perimetre.json (motifs officiels)
    assert not re.search(t["motif"], texte_cours, re.I), t["terme"]
    assert not re.search(t["motif"], contrat_sans_jamais, re.I), ("contrat", t["terme"])
for a in A_NE_PAS_DIRE:
    for d in DIAPOS:
        t = " ".join([d["title"], d["lead"], d["marche"], d["question"]] + d["demonstration"])
        assert not re.search(a["motif"], t, re.I), (a["terme"], d["id"])
    assert not re.search(a["motif"], contrat_sans_jamais, re.I), ("contrat", a["terme"])

# ---- 5. nombres recalculés (exemples du contrat et nationaux)
L = math.log10
Ke = 1e-14
def h(pH): return 10 ** -pH
def sig(x, n=3): return float(f"{x:.{n}g}")
def h_acide(C, pKa):                             # sert seulement à vérifier que les pH « mesurés » sont réalistes (jamais écrit)
    Ka = 10 ** -pKa; return (-Ka + math.sqrt(Ka * Ka + 4 * Ka * C)) / 2
def ho_base(C, pKa):
    Kb_ = Ke / 10 ** -pKa; return (-Kb_ + math.sqrt(Kb_ * Kb_ + 4 * Kb_ * C)) / 2
def resoudre(f):
    lo, hi = -14.5, 0.5
    for _ in range(200):
        m = (lo + hi) / 2
        if f(10 ** m) > 0: hi = m
        else: lo = m
    return -m
def ph_acide_faible(CA, VA, CB, VB, pKa):        # acide faible dosé par une base forte (bilan des charges)
    Ka = 10 ** -pKa; V = VA + VB; Ct = CA * VA / V; Na = CB * VB / V
    return resoudre(lambda x: x + Na - Ke / x - Ct * Ka / (Ka + x))
def ph_fort(CA, VA, CB, VB):
    V = VA + VB; return resoudre(lambda x: x + CB * VB / V - Ke / x - CA * VA / V)
def ph_base_faible(CB, VB, CA, VA, pKa):
    Ka = 10 ** -pKa; V = VA + VB; Ct = CB * VB / V; Cl = CA * VA / V
    return resoudre(lambda x: x + Ct * x / (Ka + x) - Ke / x - Cl)
V = CADRE["valeurs_reference"]
A = V["exemple_A"]
assert sig(A["H3O_mol_L"] * A["HO_mol_L"]) == A["Ke"] == Ke and round(-L(A["Ke"]), 6) == A["pKe"] and round(-L(A["H3O_mol_L"]), 2) == A["pH_eau_pure"]
B = V["exemple_B"]
assert [sig(h(p)) for p in B["pH"]] == B["H3O_mol_L"] and [sig(Ke / h(p)) for p in B["pH"]] == B["HO_mol_L"]
assert sig(10 ** (B["pH"][2] - 14)) == B["HO_mol_L"][2]
Cs = V["exemple_C"]
assert sig(Ke / Cs["HO_mol_L"]) == Cs["H3O_mol_L"] and round(-L(Cs["H3O_mol_L"]), 2) == Cs["pH"]
Dd = V["exemple_D"]
am, me = Dd["ammoniac"], Dd["methylamine"]
assert sig(10 ** (am["pH"] - 14)) == am["HO_mol_L"] and round(am["HO_mol_L"] / am["C_mol_L"], 3) == am["tau"]
assert sig(am["HO_mol_L"] ** 2 / (am["C_mol_L"] - am["HO_mol_L"])) == am["Qr_eq"]
assert sig(10 ** (me["pH"] - 14), 2) == me["HO_mol_L"] and round(me["HO_mol_L"] / me["C_mol_L"], 2) == me["tau"]
assert sig(me["C_mol_L"] * me["tau"] ** 2 / (1 - me["tau"]), 2) == me["Qr_eq"]
assert abs(14 + L(ho_base(1e-2, 9.2)) - am["pH"]) < 0.02 and round(14 + L(ho_base(1e-2, 10.7)), 2) == me["pH"]
E = V["exemple_E"]
assert sig(h(3.41) ** 2 / (1e-2 - h(3.41))) == E["Qr_eq_ethanoique"] and round(-L(E["Qr_eq_ethanoique"]), 1) == E["pKa"]["CH3COOH/CH3COO-"]
for k, ka in E["Ka"].items():
    assert sig(10 ** -E["pKa"][k], 2) == ka, k
assert sig(Ke / 1.65e-5) == E["Ka_NH4_par_Ke"] and round(-L(Ke / 1.65e-5), 2) == E["pKa_NH4_par_Ke"]
assert 10 ** -E["pKa"]["H3O+/H2O"] == 1 and round(-L(Ke)) == E["pKa"]["H2O/HO-"]
F = V["exemple_F"]
ac, ba = F["acides"], F["bases"]
assert round(-L(h_acide(1e-2, 4.8)), 2) == ac["ethanoique"]["pH"] and round(-L(h_acide(1e-2, 3.75)), 2) == ac["methanoique"]["pH"]
assert round(h(3.41) / 1e-2, 3) == ac["ethanoique"]["tau"] and round(h(2.90) / 1e-2, 3) == ac["methanoique"]["tau"]
assert ba["ammoniac"]["tau"] == am["tau"] and ba["methylamine"]["tau"] == me["tau"]
G = V["exemple_G"]
assert round(10 ** (4.8 - 3.75), 1) == G["K_HCOOH_CH3COO-"] and sig(1 / 10 ** (4.8 - 3.75), 2) == G["K_inverse"]
assert sig(10 ** (9.2 - 4.8), 2) == G["K_CH3COOH_NH3"] and sig(10 ** (14 - 4.8), 2) == G["K_CH3COOH_HO-"]
assert round(10 ** (4.8 - 3.8), 6) == G["K_2020R"]
H = V["exemple_H"]
for r, p in H["rapport_pH"]:
    assert round(H["pKa"] + L(r), 1) == p
assert [round(100 / (1 + 10 ** (p - H["pKa"])), 1) for p in H["distribution_pH"]] == H["pourcent_AH"]
J = V["exemple_J"]
assert [round(ph_acide_faible(1e-2, 20, 1e-2, v, 4.8), 2) for v in J["V_B_mL"]] == J["pH"]
assert J["C_A_mol_L"] * J["V_A_mL"] / J["C_B_mol_L"] == J["V_BE_mL"] and round(J["C_A_mol_L"] * J["V_A_mL"] * 1e-3, 6) == J["n_A_mol"]
assert round(ph_acide_faible(1e-2, 20, 1e-2, 20, 4.8), 1) == J["pH_E"] and round(ph_acide_faible(1e-2, 20, 1e-2, 10, 4.8), 1) == J["pH_demi"]
assert round((ph_acide_faible(1e-2, 20, 1e-2, 20.1, 4.8) - ph_acide_faible(1e-2, 20, 1e-2, 19.9, 4.8)) / 0.2, 1) == J["derivee_max_par_mL"]
Ii = V["exemple_I"]
assert Ii["rouge_de_cresol"][0] <= J["pH_E"] <= Ii["rouge_de_cresol"][1] and not Ii["BBT"][0] <= J["pH_E"] <= Ii["BBT"][1]
K_ = V["exemple_K"]
assert [round(ph_fort(1e-2, 20, 1e-2, v), 2) for v in K_["V_B_mL"]] == K_["pH"] and Ii["BBT"][0] <= K_["pH_E"] <= Ii["BBT"][1]
Ll = V["exemple_L"]
assert [round(ph_base_faible(1e-2, 20, 1e-2, v, 9.2), 2) for v in Ll["V_A_mL"]] == Ll["pH"]
assert round(ph_base_faible(1e-2, 20, 1e-2, 20, 9.2), 1) == Ll["pH_E"] and round(ph_base_faible(1e-2, 20, 1e-2, 10, 9.2), 1) == Ll["pKa"]
assert Ii["rouge_de_methyle"][0] <= Ll["pH_E"] <= Ii["rouge_de_methyle"][1]
M = V["exemple_M"]
lam = M["lambda_mS_m2_mol"]
def sigma(vb):                                   # mS/m ; λ en mS·m²/mol, concentrations en mol/L → S/m × 10³
    Vt = 20e-3 + 200e-3 + vb * 1e-3; nH = 1e-2 * 20e-3; nB = 0.10 * vb * 1e-3
    return 1e3 * (lam["H3O+"] * max(nH - nB, 0) + lam["HO-"] * max(nB - nH, 0) + lam["Na+"] * nB + lam["Cl-"] * nH) / Vt
assert [round(sigma(v), 1) for v in M["V_B_mL"]] == M["sigma_mS_m"] and round(1e-2 * 20 / 0.10, 6) == M["V_BE_mL"]
N = V["exemple_N"]
assert round(0.10 * 9.6 / 20.0, 6) == N["C_A_mol_L"] and round(100 * N["C_A_mol_L"], 6) == N["C0_mol_L"] and round(N["C0_mol_L"] * N["M_g_mol"], 1) == N["Cm_g_L"]
# nationaux
assert sig(10 ** -4.9 / Ke) == 1.26e9 and round(5e-2 * 6 / 5, 6) == 6e-2                                  # 2016 N
assert round(-L(1.57e-5), 1) == 4.8                                                                     # 2017 N
assert round(3e-2 * 10 / 15, 6) == 2e-2 and sig(10 ** (8 - 3.9)) == 1.26e4                             # 2018 N
assert round(-L(6.2e-5), 1) == 4.2 and round(-L(0.22e-3), 2) == 3.66                                     # 2019 N
assert round(1e-2 * 180 * 0.278, 1) == 0.5                                                              # 2019 R
assert sig(Ke / h(10.6)) == 3.98e-4 and round(-L(Ke / 1.65e-5), 1) == 9.2                                # 2020 N
assert sig(Ke * 10 ** 7.9) == 7.94e-7 and round(-L(Ke / 6.31e-10), 1) == 4.8                             # 2020 R
assert round(3.8 + L((0.01 + 5.39e-3) / (0.01 - 5.39e-3)), 2) == 4.32 and round(4.8 + L((0.01 - 5.39e-3) / (0.01 + 5.39e-3)), 2) == 4.28
assert round(-L(1.77e-5), 2) == 4.75 and round(4.75 + L(1 / 2.24), 1) == 4.4 and round(20 / 3.24, 2) == 6.17   # 2021 N
assert sig(h(2.38) / (0.1 - h(2.38))) == 4.35e-2 and round(2.38 - L(h(2.38) / (0.1 - h(2.38))), 2) == 3.74    # 2021 R
assert round(-L(1.28e-5), 1) == 4.9 and round(100 / (1 + 10 ** (4.4 - 4.9))) == 76                       # 2022 N
assert round(-L(Ke / 5e-4), 1) == 10.7 and sig(10 ** (2.8 - 10.7)) == 1.26e-8                           # 2022 R
assert round(-L(h(6.1) / (0.05 - h(3.05))), 2) == 4.79 and sig(10 ** (3.75 - 4.79), 2) == 9.1e-2 and round((4.79 + 3.75) / 2, 2) == 4.27
assert round(1 - h(3.05) / 0.05, 3) == 0.982                                                             # 2023 N
assert round(0.5 * (9.9 - L(4e-2 * 20 / 40)), 1) == 5.8                                                  # 2023 R (E calculé)
assert round(1.5e-2 * 25 / 15, 6) == 2.5e-2 and round(2.5e-2 * 0.050 * 176, 3) == 0.22 and sig(10 ** (14 - 4.09)) == 8.13e9   # 2024 N
assert round(10.8 + L(0.25), 1) == 10.2 and round(9e-2 * 10 / 4.5e-2, 6) == 20                           # 2024 R
assert round(100 / (1 + 10 ** (10.2 - 10.8))) == 80
assert round(0.1 * 9.6 / 20, 6) == 4.8e-2 and sig(10 ** 6.8) == 6.31e6 and round(0.1 * 9.6 / 29.6, 4) == 0.0324   # 2025 N
assert round(-L(h(3.6) ** 2 / (4.2e-3 - h(3.6))), 1) == 4.8 and round(100 / (1 + 10 ** (4.8 - 4.2))) == 20   # 2025 R

ex["verification"] = {
    "dix_professeurs": "non : vidéos non auditées (YouTube bloqué depuis le cloud, yt-dlp non tenté) ; remplacées par les 20 nationaux (17 touchent le chapitre, 13 ont un dosage) et perimetre.json (clés acides_bases et dosage)",
    "capacites_du_cadre_dans_le_plan": caps,
    "toutes_les_capacites": True,
    "diapositives": len(DIAPOS),
    "seances": [[len(b) for b in s["blocs"]] for s in SEANCES],
    "parties": {s["n"]: [(p["titre"], p["ids"]) for p in s["parties"]] for s in SEANCES},
    "ordre_du_contrat": True,
    "predictions": len(pred),
    "figures": FIGS,
    "agents_simulations": agents,
    "kit_copie": "commun.js, exposants.js, ab.css dans frontend/public/media/simulations/chimie/acides-bases-tableau/",
    "nombres_verifies": "exemples A à N du contrat (courbes de dosage J, K, L recalculées par le bilan des charges, σ de M) et nationaux 2016 N, 2017 N, 2018 N, 2019 N, 2019 R, 2020 N, 2020 R, 2021 N, 2021 R, 2022 N, 2022 R, 2023 N, 2023 R, 2024 N, 2024 R, 2025 N, 2025 R recalculés (python, explo.py)",
    "hors_cadre_absent": "aucun mot de hors_cadre ni terme hors programme de perimetre.json (acides_bases, dosage, esterification_hydrolyse, piles_electrolyse) dans les diapositives, les rappels ni le contrat (hors sa ligne « Jamais »)",
}

SORTIE.write_text(json.dumps(ex, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("écrit", SORTIE.relative_to(RACINE), "-", len(DIAPOS), "diapositives,", len(pred), "prédictions")
