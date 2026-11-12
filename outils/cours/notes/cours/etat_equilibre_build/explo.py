"""Assemble l'exploration etat_equilibre (explo_a + explo_b), vérifie et écrit
backend/data/curriculum/exploration/etat_equilibre.json.
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/etat_equilibre_build/explo.py"""
import json, math, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from explo_a import *
from explo_b import *

RACINE = Path(__file__).resolve().parents[5]
CONTRAT = RACINE / "outils/cours/notes/cours/etat_equilibre_contrat_simulations.md"
SORTIE = RACINE / "backend/data/curriculum/exploration/etat_equilibre.json"
PERIMETRE = RACINE / "backend/data/curriculum/perimetre.json"
KIT = RACINE / "frontend/public/media/simulations/chimie/etat-equilibre-tableau"

ORDRE = ("o1 o2 r1 r2 q1 q2 q3 q4 q5 i1 i2 i3 e1 e2 e3 k1 k2 k3 k4 k5 m1 m2 m3 m4 "
         "f1 f2 f3 f4 n1 n2 n3 n4 n5 n6 bl cr").split()
FIGS = {"n5": "fig_2017R"}

ex = {**ENTETE, "sources": SOURCES, "comparaison": COMPARAISON, "cadre": CADRE, "insistances": INSISTANCES,
      "valeurs_reperes": VALEURS_REPERES, "cas_types": CAS_TYPES, "pieges": PIEGES, "erreurs_examen": ERREURS_EXAMEN,
      "conseils": CONSEILS, "analogies_validees": ANALOGIES, "a_ne_pas_dire": A_NE_PAS_DIRE, "exclus_hors_programme": EXCLUS,
      "questions_eleves": QUESTIONS_ELEVES, "commentaires_eleves": COMMENTAIRES, "notions_complexes": NOTIONS,
      "cours_existant": COURS_EXISTANT, "visuels": VISUELS, "regles_des_simulations": REGLES_SIMULATIONS,
      "redaction_nationale": REDACTION, "plan": PLAN, "renvois": RENVOIS, "decisions_utilisateur": DECISIONS,
      "limites_de_l_exploration": LIMITES}

# ---- 0. kit copié
for f in ["commun.js", "exposants.js", "ee.css"]:
    assert (KIT / f).is_file(), f

# ---- 1. plan : ids, séances (3 × 3 blocs × 4), parties, champs, prédictions
ids = [d["id"] for d in DIAPOS]
assert ids == ORDRE, ids
assert len(DIAPOS) == 36 and len(SEANCES) == 3
assert all(len(s["blocs"]) == 3 and all(len(b) == 4 for b in s["blocs"]) for s in SEANCES)
assert [x for s in SEANCES for b in s["blocs"] for x in b] == ORDRE
assert SEANCES[0]["blocs"][0][0] == "o1" and SEANCES[-1]["blocs"][-1][-2:] == ["bl", "cr"]
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
assert len(pred) >= 13 and 3 * len(pred) >= len(DIAPOS) and not pred & {"bl", "cr"}, len(pred)
for s in SEANCES:
    for b in s["blocs"]:
        assert set(b) & pred, b

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
assert 4 <= len([p for p in pages if p not in ("figures", "bilan")]) <= 6, pages
assert "Math.max" in contrat and "transformations-deux-sens-tableau" in contrat      # moteur corrigé imposé

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
for f in ["Qr = [C]^c·[D]^d/([A]^a·[B]^b)", "Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH]", "Qr = [Zn²⁺]/[Cu²⁺]", "K = Qr,éq", "K' = 1/K",
          "τ = 10^(−pH)/C", "Qr,éq = 10^(−2pH)/(C − 10^(−pH))", "[A⁻]_éq = [H₃O⁺]_éq = C·τ", "[AH]_éq = C·(1 − τ)",
          "K = C·τ²/(1 − τ)", "σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺]", "[H₃O⁺]_éq = σ/(λ(H₃O⁺) + λ(A⁻))"]:
    assert f in formules and f in contrat, f
texte_diapos = json.dumps(DIAPOS, ensure_ascii=False)
for f in ["Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH]", "K = Qr,éq", "K' = 1/K", "K = C·τ²/(1 − τ)", "Qr,éq = 10^(−2pH)/(C − 10^(−pH))"]:
    assert f in texte_diapos, f

# ---- 4. vocabulaire : hors cadre absent des diapositives, rappels et du contrat (hors ligne « Jamais »)
perimetre = json.loads(PERIMETRE.read_text(encoding="utf-8"))
chap = perimetre["matieres"]["Physique-Chimie"]["chapitres"]
hp = [t for k in ("acides_bases", "esterification_hydrolyse", "piles_electrolyse") for t in chap[k]["termes_hors_programme"]]
assert "critère d'évolution spontanée" in chap["piles_electrolyse"]["termes_programme"]       # décision : renvoyé au semestre 2
mots = CADRE["hors_cadre"]["mots"]
for m in ["Ka", "pKa", "Ke", "produit ionique", "autoprotolyse", "Henderson", "diagramme de prédominance", "indicateur coloré",
          "activité", "Le Chatelier", "loi de modération", "Guldberg", "enthalpie", "critère d'évolution spontanée"]:
    assert m in mots, m
texte_cours = json.dumps([DIAPOS, COMPETENCES], ensure_ascii=False)
contrat_sans_jamais = "\n".join(l for l in contrat.splitlines() if "Jamais" not in l)
def present(m, t):
    return re.search(rf"(?<![\w]){re.escape(m)}(?![\w])", t, re.I) if len(m) <= 3 else m.lower() in t.lower()
for m in mots:
    assert not present(m, texte_cours), m
    assert not present(m, contrat_sans_jamais), ("contrat", m)
for m in ["quotient de réaction", "constante d'équilibre", "état initial", "Qr,éq"]:            # mots permis bien présents
    assert m.lower() in texte_cours.lower(), m
for t in hp:                                     # termes hors programme de perimetre.json (motifs officiels)
    assert not re.search(t["motif"], texte_cours, re.I), t["terme"]
    assert not re.search(t["motif"], contrat_sans_jamais, re.I), ("contrat", t["terme"])
for a in A_NE_PAS_DIRE:
    for d in DIAPOS:
        t = " ".join([d["title"], d["lead"], d["marche"], d["question"]] + d["demonstration"])
        assert not re.search(a["motif"], t, re.I), (a["terme"], d["id"])

# ---- 5. nombres recalculés (exemples du contrat et nationaux)
L = math.log10
def h(pH): return 10 ** -pH
def qeq(pH, C): return h(pH) ** 2 / (C - h(pH))
def ktau(C, t): return C * t * t / (1 - t)
def h_modele(C, K):                              # sert seulement à vérifier que les pH « mesurés » sont réalistes (jamais écrit)
    return (-K + math.sqrt(K * K + 4 * K * C)) / 2
V = CADRE["valeurs_reference"]
A = V["exemple_A"]
assert round(h(A["pH"]), 6) == A["H3O_mol_L"] and round(A["C_mol_L"] - A["H3O_mol_L"], 5) == A["CH3COOH_mol_L"]
assert round(h(A["pH"]) / A["C_mol_L"], 4) == A["tau"] and round(qeq(A["pH"], A["C_mol_L"]), 7) == A["Qr_eq"]
assert round(A["H3O_mol_L"] ** 2 / A["CH3COOH_mol_L"], 7) == A["Qr_eq"] and round(ktau(1e-2, A["tau"]), 7) == A["Qr_eq"]
assert round(A["pH"], 1) == A["pH_au_dixieme"] and round(-L(h_modele(1e-2, 1.6e-5)), 2) == A["pH"]
B = V["exemple_B"]
assert [round(-L(h_modele(c, 1.585e-5)), 2) for c in B["C_mol_L"]] == B["pH"]
assert [float(f"{h(p):.3g}") for p in B["pH"]] == B["H3O_mol_L"]
assert [round(h(p) / c, 3) for p, c in zip(B["pH"], B["C_mol_L"])] == B["tau"]
assert [round(qeq(p, c), 7) for p, c in zip(B["pH"], B["C_mol_L"])] == B["Qr_eq"]
assert all(round(q, 6) == B["K"] for q in B["Qr_eq"])
Cc = V["exemple_C"]                              # départ par les produits : même état que l'acide à 5,0·10⁻³ mol/L
assert round(h(Cc["pH"]), 6) == Cc["H3O_mol_L"] and round(5.0e-3 - h(Cc["pH"]), 5) == Cc["CH3COOH_mol_L"]
assert round(qeq(Cc["pH"], 5.0e-3), 7) == Cc["Qr_eq"]
Dd = V["exemple_D"]
lam = Dd["lambda_mS_m2_mol"]
Hm3 = Dd["sigma_S_m"] / ((lam["H3O+"] + lam["CH3COO-"]) * 1e-3)
assert round(Hm3, 3) == Dd["H3O_mol_m3"] and round(Hm3 / 1e3, 6) == Dd["H3O_mol_L"] and round(Hm3 / 1e3 / Dd["C_mol_L"], 3) == Dd["tau"]
assert round(ktau(Dd["C_mol_L"], Dd["tau"]), 7) == Dd["K"] and round(Dd["K"], 6) == B["K"]
assert round(-L(Dd["H3O_mol_L"]), 2) == B["pH"][2]                                                   # cohérent avec le pH 3,93
E = V["exemple_E"]
assert round(-L(h_modele(1e-2, 1.8e-4)), 2) == E["pH"] and round(h(E["pH"]), 5) == E["H3O_mol_L"]
assert round(h(E["pH"]) / 1e-2, 3) == E["tau"] and round(qeq(E["pH"], 1e-2), 6) == E["Qr_eq"] and round(E["Qr_eq"], 5) == E["K"]
F = V["exemple_F"]
assert F["H3O_mol_L"][0] == 0 == F["Qr"][0] and F["H3O_mol_L"][-1] == A["H3O_mol_L"] and F["Qr"][-1] == A["Qr_eq"]
assert [float(f"{x * x / (1e-2 - x):.3g}") for x in F["H3O_mol_L"][1:]] == F["Qr"][1:]
assert round((2.0e-4 * 2.0e-4) / 9.8e-3, 8) == 4.08e-6                                              # q5
G = V["exemple_G"]["n_mol"]
assert round((G["HCOO-"] * G["CH3COOH"]) / (G["HCOOH"] * G["CH3COO-"]), 6) == V["exemple_G"]["Qr_i"]
assert round(G["HCOOH"] / V["exemple_G"]["V_T_L"], 4) == 0.0333
assert round(V["exemple_H"]["Zn2+_mol_L"] / V["exemple_H"]["Cu2+_mol_L"], 6) == V["exemple_H"]["Qr_i"]
assert 1 / V["exemple_J"]["K"] == V["exemple_J"]["K_inverse"]
Kk = V["exemple_K"]
def tau_k(C, K): return h_modele(C, K) / C
assert [float(f"{tau_k(c, 1.6e-5):.2g}") for c in Kk["C_mol_L"]] == Kk["tau_K_1_6e-5"]
assert [float(f"{tau_k(c, 1.8e-4):.2g}") for c in Kk["C_mol_L"]] == Kk["tau_K_1_8e-4"]
# nationaux
assert round(0.65 ** 2 / 0.65 ** 3, 1) == 1.5                                                         # 2017 N I.1
assert round(qeq(3.41, 1e-2), 7) == 1.57e-5 and round(h(3.41) / 1e-2, 3) == 0.039                     # 2017 N II.1.1-1.2
assert round(0.33 ** 2 / 0.67 ** 2, 3) == 0.243 and round(0.33 ** 2 / 0.67 ** 2, 4) == 0.2426        # 2016 R (corrigé 0,242)
assert round((0.4 * 0.4) / (0.2 * 0.2), 6) == 4                                                        # 2017 R
assert round((0.2 * 0.2) / (0.4 * 0.4), 2) == 0.25                                                     # 2018 R
assert float(f"{ktau(1e-3, 0.22):.2g}") == 6.2e-5 and float(f"{ktau(1e-3, 0.225):.3g}") == 6.53e-5                # 2019 N
assert round(8.6e-3 / (1.0 * (35 + 3.23) * 1e-3), 2) in (0.22, 0.23)
assert round((3.98e-4) ** 2 / (1e-2 - 3.98e-4), 7) == 1.65e-5                                         # 2020 N
assert round(ktau(1e-3, 7.94e-4), 12) == 6.31e-10 and round(1e-14 * 10 ** 7.9 / 1e-3, 6) == 0.000794  # 2020 R I
assert (0.1 * 0.1 * 0.1 * 0.1) / (0.1 * 0.1 * 0.1 * 0.1) == 1                                          # 2020 R II.3
assert round(h(2.88) / 0.1, 4) == 0.0132 and round(ktau(0.1, 0.0132), 7) == 1.77e-5                   # 2021 N
assert round(qeq(3.1, 5e-2), 7) == 1.28e-5                                                             # 2022 N
assert round(ktau(1e-2, 0.20), 6) == 5.0e-4                                                            # 2022 R
assert round(10 ** (3.75 - 4.79), 4) == 0.0912                                                         # 2023 N 2.2 (chapitre 13)
x = (4 - math.sqrt(16 - 4 * 3 * 0.12)) / 6
assert round(x, 3) == 0.031 and round((0.6 + x) / 0.9, 3) == 0.701                                    # 2023 N 3.6 (semestre 2)
assert round(10 ** -4.9 / 1e-14 / 1e9, 2) == 1.26 and round(10 ** (14 - 4.09) / 1e9, 2) == 8.13        # 2016 N, 2024 N (chapitre 13)
assert round(10 ** 6.8 / 1e6, 2) == 6.31                                                               # 2025 N (chapitre 13)

ex["verification"] = {
    "dix_professeurs": "non : vidéos non auditées (YouTube bloqué depuis le cloud, yt-dlp non tenté) ; remplacées par les 20 nationaux (12 touchent le chapitre) et perimetre.json",
    "capacites_du_cadre_dans_le_plan": caps,
    "toutes_les_capacites": True,
    "diapositives": len(DIAPOS),
    "seances": [[len(b) for b in s["blocs"]] for s in SEANCES],
    "parties": {s["n"]: [(p["titre"], p["ids"]) for p in s["parties"]] for s in SEANCES},
    "ordre_du_contrat": True,
    "predictions": len(pred),
    "figures": FIGS,
    "kit_copie": "commun.js, exposants.js, ee.css dans frontend/public/media/simulations/chimie/etat-equilibre-tableau/",
    "nombres_verifies": "exemples A à K du contrat et nationaux 2016 N, 2016 R, 2017 N, 2017 R, 2018 R, 2019 N, 2020 N, 2020 R, 2021 N, 2022 N, 2022 R, 2023 N, 2024 N, 2025 N recalculés (python, explo.py)",
    "hors_cadre_absent": "aucun mot de hors_cadre ni terme hors programme de perimetre.json (acides_bases, esterification_hydrolyse, piles_electrolyse) dans les diapositives, les rappels ni le contrat (hors sa ligne « Jamais »)",
}

SORTIE.write_text(json.dumps(ex, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("écrit", SORTIE.relative_to(RACINE), "-", len(DIAPOS), "diapositives,", len(pred), "prédictions")
