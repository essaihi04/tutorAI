"""Ajoute (ou remplace) la seule clé chapitres.dipole_RC : relit le fichier, ajoute la clé, réécrit aussitôt."""
import json, copy
from pathlib import Path
REPO = Path("backend/data/curriculum")
ex = json.loads((REPO / "exploration/dipole_RC.json").read_text(encoding="utf-8"))
fiche = copy.deepcopy(ex["cadre"])
fiche["_note"] = ("Fiche ajoutée le 12 novembre 2026 (routine cloud) depuis exploration/dipole_RC.json (9 professeurs audités, nationaux PC "
                  "2016-2025 du dépôt, perimetre.json). Le texte officiel du cadre n'a pas été relu mot à mot : capacités RC1 à RC9 provisoires, "
                  "à collationner. Lectures (dit) écrites comme la voix les dit (u C, tau, dé u C sur dé t).")
F = fiche["formules"]
def f(ecr, cap, dit, **kw):
    d = {"ecriture": ecr, "capacite": cap, "dit": dit}; d.update(kw); F.append(d)
f("du_C/dt + (1/RC)·u_C = E/(RC)", "RC5", "dé u C sur dé t plus un sur R C fois u C égale E sur R C", phrase="forme des corrigés (2021 N, 2022 N, 2023 R)")
f("RC·du_C/dt + u_C = 0", "RC5", "R C dé u C sur dé t plus u C égale zéro", phrase="équation différentielle de la décharge")
f("RC·dq/dt + q = C·E", "RC5", "R C dé q sur dé t plus q égale C E")
f("RC·du_R/dt + u_R = 0", "RC5", "R C dé u R sur dé t plus u R égale zéro")
f("RC·di/dt + i = 0", "RC5", "R C dé i sur dé t plus i égale zéro")
f("u_C(t) = A + B·e^(−t/τ)", "RC6", "u C égale A plus B exponentielle de moins t sur tau", variantes_admises=["u_C(t) = A·(1 − e^(−αt))", "u_C(t) = A + B·e^(−αt)"])
f("q(t) = C·E(1 − e^(−t/τ))", "RC6", "q de t égale C E fois un moins exponentielle de moins t sur tau")
f("u_R(t) = E·e^(−t/τ)", "RC6", "u R de t égale E exponentielle de moins t sur tau", phrase="en charge")
f("i(t) = −(E/R)·e^(−t/τ)", "RC6", "i de t égale moins E sur R exponentielle de moins t sur tau", phrase="en décharge, i orienté comme pendant la charge")
f("[τ] = [R]·[C] = [T]", "RC7", "la dimension de tau est un temps")
f("u_C(5τ) ≈ 0,99·E", "RC7", "à cinq tau, u C vaut presque E")
fiche["decisions"] = [
 "Associations de condensateurs gardées (a1, a2) : 2018 N demande C₂ dans un montage en parallèle.",
 "Charge à courant constant gardée (g1, g2) : 2018 N, 2020 R, 2025 N ; à ajouter aux notions de perimetre.json à la fusion.",
 "Équation différentielle enseignée d'abord sous la forme RC·du_C/dt + u_C = E, puis la forme des corrigés du_C/dt + (1/RC)·u_C = E/(RC).",
 "Pas de courbe ln u_C = f(t) (aucun national).",
 "Énergie E_e = ½·C·u_C² admise (une phrase sur l'origine du ½), pas de démonstration.",
 "Analyse dimensionnelle de τ gardée en une diapositive.",
 "En décharge, i garde l'orientation de la charge : i = C·du_C/dt < 0 (un énoncé peut orienter autrement, l'ED de u_C ne change pas).",
]
p = REPO / "cadre_reference_2bac_pc.json"
d = json.loads(p.read_text(encoding="utf-8"))
d["chapitres"]["dipole_RC"] = fiche
p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("chapitres.dipole_RC :", len(fiche["capacites"]), "capacités,", len(F), "formules,", len(fiche["hors_cadre"]["mots"]), "mots hors cadre")
