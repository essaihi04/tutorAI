"""Assemble l'exploration transformations_deux_sens (explo_a + explo_b), vérifie et écrit
backend/data/curriculum/exploration/transformations_deux_sens.json.
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/transformations_deux_sens_build/explo.py"""
import json, math, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from explo_a import *
from explo_b import *

RACINE = Path(__file__).resolve().parents[5]
CONTRAT = RACINE / "outils/cours/notes/cours/transformations_deux_sens_contrat_simulations.md"
SORTIE = RACINE / "backend/data/curriculum/exploration/transformations_deux_sens.json"
PERIMETRE = RACINE / "backend/data/curriculum/perimetre.json"

ORDRE = ("o1 o2 b1 b2 b3 b4 p1 p2 p3 p4 p5 p6 a1 a2 a3 a4 a5 a6 e1 e2 e3 e4 e5 e6 "
         "c1 c2 c3 d1 d2 d3 n1 n2 n3 n4 bl cr").split()
FIGS = {"e6": "fig_2017N", "n1": "fig_2021R"}

ex = {**ENTETE, "sources": SOURCES, "comparaison": COMPARAISON, "cadre": CADRE, "insistances": INSISTANCES,
      "valeurs_reperes": VALEURS_REPERES, "cas_types": CAS_TYPES, "pieges": PIEGES, "erreurs_examen": ERREURS_EXAMEN,
      "conseils": CONSEILS, "analogies_validees": ANALOGIES, "a_ne_pas_dire": A_NE_PAS_DIRE, "exclus_hors_programme": EXCLUS,
      "questions_eleves": QUESTIONS_ELEVES, "commentaires_eleves": COMMENTAIRES, "notions_complexes": NOTIONS,
      "cours_existant": COURS_EXISTANT, "visuels": VISUELS, "regles_des_simulations": REGLES_SIMULATIONS,
      "redaction_nationale": REDACTION, "plan": PLAN, "renvois": RENVOIS, "decisions_utilisateur": DECISIONS,
      "limites_de_l_exploration": LIMITES}

# ---- 1. plan : ids, séances (3 × 3 blocs × 4), champs, prédictions
ids = [d["id"] for d in DIAPOS]
assert ids == ORDRE, ids
assert len(DIAPOS) == 36 and len(SEANCES) == 3
assert all(len(s["blocs"]) == 3 and all(len(b) == 4 for b in s["blocs"]) for s in SEANCES)
assert [x for s in SEANCES for b in s["blocs"] for x in b] == ORDRE
assert SEANCES[0]["blocs"][0][0] == "o1" and SEANCES[-1]["blocs"][-1][-2:] == ["bl", "cr"]
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
for f in ["AH ⇌ A⁻ + H⁺", "pH = −log[H₃O⁺]", "[H₃O⁺] = 10^(−pH)", "AH + H₂O ⇌ A⁻ + H₃O⁺", "B + H₂O ⇌ BH⁺ + HO⁻",
          "x_max = C·V", "x_f = [H₃O⁺]_éq·V", "τ = x_f/x_max", "τ = 10^(−pH)/C", "σ = Σ λᵢ·[Xᵢ]",
          "σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺]", "[H₃O⁺] = σ/(λ(H₃O⁺) + λ(A⁻))", "τ = σ/(C·(λ(H₃O⁺) + λ(A⁻)))"]:
    assert f in formules and f in contrat, f

# ---- 4. vocabulaire : hors cadre absent des diapositives, rappels et du contrat (hors ligne « Jamais »)
perimetre = json.loads(PERIMETRE.read_text(encoding="utf-8"))
hp = perimetre["matieres"]["Physique-Chimie"]["chapitres"]["acides_bases"]["termes_hors_programme"]
mots = CADRE["hors_cadre"]["mots"]
for m in ["Qr", "quotient de réaction", "constante d'équilibre", "Ka", "pKa", "Ke", "produit ionique", "activité", "Lewis",
          "Arrhenius", "degré d'ionisation", "Ostwald", "diagramme de prédominance"]:
    assert m in mots, m
texte_cours = json.dumps([DIAPOS, COMPETENCES], ensure_ascii=False)
contrat_sans_jamais = "\n".join(l for l in contrat.splitlines() if "Jamais" not in l)
def present(m, t):
    return re.search(rf"(?<![\w]){re.escape(m)}(?![\w])", t, re.I) if len(m) <= 3 else m.lower() in t.lower()
for m in mots:
    assert not present(m, texte_cours), m
    assert not present(m, contrat_sans_jamais), ("contrat", m)
for t in hp:                                     # termes hors programme de perimetre.json (motifs officiels)
    assert not re.search(t["motif"], texte_cours, re.I), t["terme"]
    assert not re.search(t["motif"], contrat_sans_jamais, re.I), ("contrat", t["terme"])
for a in A_NE_PAS_DIRE:
    for d in DIAPOS:
        t = " ".join([d["title"], d["lead"], d["marche"], d["question"]] + d["demonstration"])
        assert not re.search(a["motif"], t, re.I), (a["terme"], d["id"])

# ---- 5. nombres recalculés (exemples du contrat et nationaux)
L = math.log10
def tau(pH, C): return 10 ** -pH / C
def h_modele(C, pKa=4.8):                        # sert seulement à vérifier que les pH « mesurés » sont réalistes (jamais écrit)
    k = 10 ** -pKa; return (-k + math.sqrt(k * k + 4 * k * C)) / 2
A = CADRE["valeurs_reference"]["exemple_A"]
assert round(10 ** -A["pH"], 5) == A["H3O_mol_L"] == 4.0e-4
assert round(A["C_mol_L"] * A["V_L"], 6) == A["x_max_mol"] and round(10 ** -3.4 * 0.100, 6) == A["x_f_mol"]
assert round(A["x_f_mol"] / A["x_max_mol"], 3) == A["tau"] == round(tau(3.4, 1e-2), 3)
assert round(-L(A["C_mol_L"]), 1) == A["pH_si_totale"] and round(-L(h_modele(1e-2)), 1) == 3.4
assert round(1.0e-3 - 4.0e-5, 6) == A["equilibre_mol"]["CH3COOH"]
assert round(tau(2.0, 1e-2), 6) == 1 and round(10 ** -2.0 * 0.100, 6) == 1.0e-3                     # exemple B
lam = CADRE["valeurs_reference"]["exemple_C"]["lambda_mS_m2_mol"]
assert round((lam["H3O+"] + lam["CH3COO-"]) * 1e-3 * 10 ** -3.4 * 1e3, 4) == 0.0156               # σ(A) = 1,56·10⁻² S/m
assert round((lam["H3O+"] + lam["Cl-"]) * 1e-3 * 10, 3) == 0.426                                   # σ(B)
H = 1.56e-2 / ((lam["H3O+"] + lam["CH3COO-"]) * 1e-3)
assert round(H, 3) == 0.399 and round(H / 1e3 / 1e-2, 3) == 0.040                                   # exemple C
Dd = CADRE["valeurs_reference"]["exemple_D"]
assert [round(-L(h_modele(c)), 1) for c in Dd["C_mol_L"]] == Dd["pH"]
assert [round(tau(p, c), 2 if c < 1e-2 else 3) for p, c in zip(Dd["pH"], Dd["C_mol_L"])] == Dd["tau"]
assert round(-L(h_modele(1e-2, 3.75)), 1) == 2.9 and round(tau(2.9, 1e-2), 2) == 0.13              # acide méthanoïque
assert round(-L(5e-3), 1) == 2.3 and round(-L(h_modele(5e-3)), 1) == 3.6                            # exemple E
assert round(0.33 / 0.5, 2) == 0.66                                                                  # exemple F (2016 N)
assert round(tau(3.41, 1e-2), 3) == 0.039 and round(0.2 / 0.3, 2) == 0.67                            # 2017 N
assert round(8.6e-3 / (1.0 * (35 + 3.23) * 1e-3), 2) in (0.22, 0.23)                                 # 2019 N
assert round(1e-14 / 10 ** -10.6 / 1e-2, 3) == 0.040                                                  # 2020 N (Ke : chapitre suivant)
assert round(1e-14 * 10 ** 7.9 / 1e-3, 6) == 0.000794                                                 # 2020 R
assert round(tau(2.88, 0.1), 4) == 0.0132                                                             # 2021 N
assert round(10 ** -2.8 / 0.10, 4) == 0.0158 and round(10 ** -3.6 / 0.45, 6) == 0.000558             # 2021 R
assert round(tau(3.1, 5e-2), 3) == 0.016                                                              # 2022 N
assert round(1e-14 / 10 ** -11.3 / 1e-2, 2) == 0.20                                                   # 2022 R
assert round(tau(3.05, 5e-2), 4) == 0.0178 and round(1 - tau(3.05, 5e-2), 3) == 0.982                # 2023 N
xf = 4.5e-2 * 16.0e-3 - 10 ** -10.2 * 26.0e-3
assert round(xf, 5) == 0.00072 and round(xf / (4.5e-2 * 16.0e-3), 6) == 1.0                          # 2024 R
assert round(tau(3.6, 4.2e-3), 2) == 0.06 and round(1 / (1 + 10 ** (4.8 - 4.2)), 2) == 0.20           # 2025 R

ex["verification"] = {
    "dix_professeurs": "non : vidéos non auditées (YouTube bloqué depuis le cloud, yt-dlp non tenté) ; remplacées par les 20 nationaux (17 touchent le chapitre) et perimetre.json",
    "capacites_du_cadre_dans_le_plan": caps,
    "toutes_les_capacites": True,
    "diapositives": len(DIAPOS),
    "seances": [[len(b) for b in s["blocs"]] for s in SEANCES],
    "ordre_du_contrat": True,
    "predictions": len(pred),
    "figures": FIGS,
    "nombres_verifies": "exemples A à F du contrat et nationaux 2016 N, 2017 N, 2019 N, 2020 N, 2020 R, 2021 N, 2021 R, 2022 N, 2022 R, 2023 N, 2024 R, 2025 R recalculés (python, explo.py)",
    "hors_cadre_absent": "aucun mot de hors_cadre ni terme hors programme de perimetre.json dans les diapositives, les rappels ni le contrat (hors sa ligne « Jamais »)",
}

SORTIE.write_text(json.dumps(ex, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("écrit", SORTIE.relative_to(RACINE), "-", len(DIAPOS), "diapositives,", len(pred), "prédictions")
