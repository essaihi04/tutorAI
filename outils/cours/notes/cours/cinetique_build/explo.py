"""Assemble l'exploration cinetique (explo_a + explo_b), vérifie et écrit backend/data/curriculum/exploration/cinetique.json.
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/cinetique_build/explo.py"""
import json, math, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from explo_a import *
from explo_b import *

RACINE = Path(__file__).resolve().parents[5]
CONTRAT = RACINE / "outils/cours/notes/cours/cinetique_contrat_simulations.md"
SORTIE = RACINE / "backend/data/curriculum/exploration/cinetique.json"

ORDRE = "o1 o2 m1 m2 m3 a1 a2 a3 a4 a5 a6 a7 g1 g2 g3 g4 g5 g6 p1 p2 p3 p4 p5 p6 v1 v2 v3 v4 v5 v6 v7 v8 h1 h2 h3 h4 n1 n2 n3 n4 n5 n6 n7 n8 r1 r2 bl cr".split()
FIGS = {"p4": "fig_2016R", "p6": "fig_2024N", "n1": "fig_2019R", "n2": "fig_2025R", "n3": "fig_2017N", "n4": "fig_2023N",
        "n5": "fig_2025N", "n6": "fig_2021N", "n7": "fig_2018R", "n8": "fig_2017R"}

ex = {**ENTETE, "sources": SOURCES, "comparaison": COMPARAISON, "cadre": CADRE, "insistances": INSISTANCES,
      "valeurs_reperes": VALEURS_REPERES, "cas_types": CAS_TYPES, "pieges": PIEGES, "erreurs_examen": ERREURS_EXAMEN,
      "conseils": CONSEILS, "analogies_validees": ANALOGIES, "a_ne_pas_dire": A_NE_PAS_DIRE, "exclus_hors_programme": EXCLUS,
      "questions_eleves": QUESTIONS_ELEVES, "commentaires_eleves": COMMENTAIRES, "notions_complexes": NOTIONS,
      "cours_existant": COURS_EXISTANT, "visuels": VISUELS, "regles_des_simulations": REGLES_SIMULATIONS,
      "redaction_nationale": REDACTION, "plan": PLAN, "renvois": RENVOIS, "decisions_utilisateur": DECISIONS,
      "limites_de_l_exploration": LIMITES}

# ---- 1. plan : ids, séances, champs, prédictions
ids = [d["id"] for d in DIAPOS]
assert ids == ORDRE, ids
assert [x for s in SEANCES for b in s["blocs"] for x in b] == ORDRE
CHAMPS = ["id", "title", "lead", "marche", "visuel", "question", "prediction", "competences", "demonstration"]
comp_ids = {c["id"] for c in COMPETENCES}
for d in DIAPOS:
    assert list(d) == CHAMPS, d["id"]
    assert all(d[k] for k in ["title", "lead", "marche", "visuel", "question", "competences"]), d["id"]
    assert set(d["competences"]) <= comp_ids, d["id"]
pred = {d["id"] for d in DIAPOS if d["prediction"]}
assert len(pred) >= 16 and not pred & {"bl", "cr"}
for s in SEANCES:
    for b in s["blocs"]:
        assert set(b) & pred, b

# ---- 2. visuels = « Diapositives servies » du contrat
contrat = CONTRAT.read_text(encoding="utf-8")
servies = contrat.split("## Diapositives servies")[1]
for d in DIAPOS:
    if d["id"] in FIGS:
        assert d["visuel"] == f"figures?fig={FIGS[d['id']]}", d["id"]
    elif d["id"] in ("bl", "cr", "o1"):
        assert d["visuel"] == {"bl": "bilan", "cr": "carte", "o1": "carte"}[d["id"]]
    else:
        assert re.search(rf"\b{d['id']} {re.escape(d['visuel'])}\b", servies), (d["id"], d["visuel"])

# ---- 3. compétences, capacités
for c in COMPETENCES:
    assert 3 <= len(c["rappels"]) <= 4 and len({r["type"] for r in c["rappels"]}) >= 2, c["id"]
caps = {}
cc = {c["id"]: c["cadre_ids"] for c in COMPETENCES}
for d in DIAPOS:
    for c in d["competences"]:
        for k in cc[c]:
            caps.setdefault(k, []).append(d["id"])
assert set(caps) == {c["id"] for c in CADRE["capacites"]}, set(caps)
formules = {f["ecriture"] for f in CADRE["formules"]}
for f in ["v(t) = (1/V)·dx/dt", "x(t₁/₂) = x_f/2", "G = k·σ", "σ = Σ λᵢ·[Xᵢ]", "x = x_max·(σ₀ − σ)/(σ₀ − σ_f)",
          "x = (P − P₀)·V/(R·T)", "n(I₂) = C·V_E/2", "x = V(H₂)/V_m", "σ = σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V"]:
    assert f in formules and f in contrat, f

# ---- 4. vocabulaire : hors cadre absent des diapositives et rappels, et du contrat (hors ligne « Jamais »)
texte_cours = json.dumps([DIAPOS, COMPETENCES], ensure_ascii=False).lower()
contrat_sans_jamais = "\n".join(l for l in contrat.splitlines() if "Jamais" not in l and "Beer-Lambert, « exponentielle »" not in l).lower()
for m in CADRE["hors_cadre"]["mots"]:
    assert m.lower() not in texte_cours, m
    assert m.lower() not in contrat_sans_jamais, ("contrat", m)
for a in A_NE_PAS_DIRE:
    for d in DIAPOS:
        t = " ".join([d["title"], d["lead"], d["marche"], d["question"]] + d["demonstration"])
        assert not re.search(a["motif"], t, re.I), (a["terme"], d["id"])

# ---- 5. nombres des exemples A, B, C et des nationaux
e = math.exp
xA = lambda t, k=1 / 8: 2.0 * (1 - e(-k * t))
assert [round(xA(t), 2) for t in CADRE["valeurs_reference"]["exemple_A"]["mesures_t_min"]] == CADRE["valeurs_reference"]["exemple_A"]["mesures_x_mmol"]
assert round(8 * math.log(2), 1) == 5.5 and round(8 / 3 * math.log(2), 1) == 1.8
assert round(0.25 * e(-1) / 0.100, 2) == 0.92 and round(0.25 * e(-2.5) / 0.100, 2) == 0.21 and round(xA(11), 1) == 1.5
assert round(10 * 0.020 * 12.6 / 2, 2) == 1.26 and round(2.0 - 1.26, 2) == 0.74 and round(10.0 - 2 * 1.26, 2) == 7.48
s0 = 5.01e-3 * 10 + 19.9e-3 * 10; sf = 5.01e-3 * 10 + 4.09e-3 * 10
assert round(s0, 3) == 0.249 and round(sf, 3) == 0.091 and round(s0 - (s0 - sf) * 0.5, 3) == 0.170
assert round(1.0 * (0.249 - 0.170) / (0.249 - 0.091), 2) == 0.50
assert round(1e-3 * 8.31 * 300 / 1e-3) == 2493 and round(2.49e3 * 1e-3 / (8.31 * 300), 4) == 0.0010
assert round((0.40 - 0.25) / 60 / 0.200, 4) == 0.0125                       # 2024 N
assert round((1.5 - 0.75) / 75 * 1e-3 / 10e-3, 6) == 0.001                  # 2019 R
assert round(0.08 / 0.050, 2) == 1.6                                         # 2025 R
assert round(0.0125 / (160 * 1e-4), 2) == 0.78 and round(0.25 - 160 * 5e-4, 2) == 0.17   # 2021 N
assert round((1.57e-3 - 5e-4) / 6.3e-3, 3) == 0.170 and round(6.3e-3 * 0.15 / 18 / 1e-4, 3) == 0.525  # 2016 R
assert round((1.57e-3 - 5e-4) / 6.3e-2, 3) == 0.017                          # 2018 R

ex["verification"] = {
    "dix_professeurs": "non : vidéos non auditées (YouTube bloqué depuis le cloud) ; remplacées par les 10 nationaux avec suivi temporel",
    "capacites_du_cadre_dans_le_plan": caps,
    "toutes_les_capacites": True,
    "diapositives": len(DIAPOS),
    "ordre_du_contrat": True,
    "predictions": len(pred),
    "figures": FIGS,
    "nombres_verifies": "exemples A, B, C du contrat et nationaux 2016 R, 2018 R, 2019 R, 2021 N, 2024 N, 2025 R recalculés (python, explo.py)",
    "hors_cadre_absent": "aucun mot de hors_cadre dans les diapositives, les rappels ni le contrat (hors sa ligne « Jamais »)",
}

SORTIE.write_text(json.dumps(ex, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("écrit", SORTIE.relative_to(RACINE), "-", len(DIAPOS), "diapositives,", len(pred), "prédictions")
