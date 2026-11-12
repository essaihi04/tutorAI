# -*- coding: utf-8 -*-
"""Écrit backend/data/curriculum/exploration/dipole_RL.json (parties A et B + ce qui vient des nationaux, nationaux.md).
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/dipole_RL_build/explo.py"""
import json, sys
from pathlib import Path
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import explo_a as A, explo_b as B

NAT = ["2016 R", "2017 N", "2018 R", "2019 R", "2020 N", "2021 R", "2022 R", "2023 N", "2024 N", "2025 R"]

def ct(id, nom, indices, methode, sessions, points):
    return {"id": id, "nom": nom, "indices": indices, "methode": methode, "sessions": sessions, "points": points}

cas_types = [
 ct("ed_i", "établir l'équation différentielle en i (établissement)", "« établir / montrer l'équation différentielle vérifiée par i(t) »",
    "additivité u_R + u_b = E → u_R = R·i, u_b = L·di/dt + r·i → L·di/dt + (R + r)·i = E → diviser par L : di/dt + ((R + r)/L)·i = E/L (2021 R : 1/τ = (R + r)/L ; 2024 N : di/dt = −((R + r)/L)·i + E/L)",
    ["2016 R", "2018 R", "2020 N", "2021 R", "2023 N", "2024 N"], "0,25 à 0,5"),
 ct("ed_uR", "établir l'équation différentielle en u_R", "« l'équation différentielle vérifiée par u_R(t) »",
    "équation en i, puis i = u_R/R et di/dt = (1/R)·du_R/dt ; multiplier par R : du_R/dt + ((R + r)/L)·u_R = R·E/L ; à la rupture (2017 N) : (L/(R + r))·du_R/dt + u_R = 0",
    ["2017 N", "2019 R", "2022 R", "2025 R"], "0,5"),
 ct("solution", "vérifier la solution, trouver A (B) et τ", "« trouver les expressions de A et τ », « déterminer A et B »",
    "dériver, remplacer, regrouper : coefficient de e^(−t/τ) nul → τ = L/(R + r) ; terme constant nul → A = E/(R + r) ; avec i = A + B·e^(−t/τ), la condition i(0) = 0 donne B = −A",
    ["2016 R", "2017 N", "2021 R", "2023 N"], "0,5"),
 ct("permanent", "régime permanent : I₀ (I_p) ou U_R", "« en régime permanent », « en déduire l'expression de I_p »",
    "di/dt = 0 → (R + r)·I₀ = E → I₀ = E/(R + r) (Pouillet) ; U_R = R·E/(R + r) ; ou I₀ = U_Rmax/R lu",
    ["2016 R", "2017 N", "2019 R", "2021 R", "2023 N", "2025 R"], "0,25 à 0,5"),
 ct("r", "trouver r de la bobine", "« déterminer la valeur de r », « montrer que r = … »",
    "a) r = E/I₀ − R ; b) r = R·(E/U_R − 1) ; c) r = u_b(∞)/I₀ ; d) à la rupture, depuis u_R(0) = R·E/(R + r)",
    ["2017 N", "2019 R", "2020 N", "2021 R", "2022 R"], "0,5"),
 ct("tau", "lire τ sur la courbe", "« déterminer graphiquement τ »",
    "tangente à l'origine ∩ asymptote (établissement) ou ∩ axe des temps (rupture) ; 63 % de la valeur finale lue ; 37 % pour une courbe qui descend (u_L, 2018 R)",
    NAT[:8] + ["2025 R"], "0,25 (souvent inclus dans « trouver L »)"),
 ct("L", "trouver L à partir de τ", "« en déduire / vérifier la valeur de L »",
    "τ = L/(R + r) → L = τ·(R + r), τ en secondes ; bobine idéale : L = τ·R ; 2023 N : R = E/I₀ d'abord",
    ["2016 R", "2017 N", "2018 R", "2019 R", "2020 N", "2021 R", "2022 R", "2023 N", "2025 R"], "0,25 à 0,75"),
 ct("droite", "graphe di/dt = f(i)", "figure di/dt en fonction de i (axe i en mA, di/dt en 10³ A/s)",
    "di/dt = −(1/τ)·i + E/L : ordonnée à l'origine E/L → L ; pente −1/τ → τ ; coupe l'axe des i en I₀", ["2024 N"], "2 × 0,5"),
 ct("ub_t", "u_b(t) par dérivation / à un instant", "« montrer que u_L = E·e^(−t/τ) », « expression numérique de u_L(t) »",
    "bobine idéale : u_L = L·di/dt = E·e^(−t/τ) ; en SI : u_L = 24·e^(−500t) (2023 N) ; u_L(τ) = 0,37·E", ["2018 R", "2023 N"], "0,5"),
 ct("ub_perm", "u_b en régime permanent", "« tension aux bornes de la bobine en régime permanent »",
    "u_b = r·I₀ (bobine réelle) ; 0 si r = 0", ["2020 N", "2025 R"], "0,25 à 0,5"),
 ct("energie", "énergie magnétique", "« énergie emmagasinée dans la bobine à l'instant … »",
    "E_m = ½·L·i², avec i = u_R/R lu à l'instant demandé (τ, τ/2) ou I₀ en régime permanent", ["2016 R", "2017 N", "2018 R", "2025 R"], "0,25 à 0,75"),
 ct("rupture", "rupture du courant", "« on bascule K », « on ouvre K », diode + R₁ en parallèle",
    "maille sans générateur : second membre 0 ; i(0⁺) = I₀ (continuité) ; avec diode et R₁ : u_b(0⁺) = −R₁·I₀ (surtension)", ["2017 N", "2025 R"], "0,25 à 0,5"),
 ct("courbe", "identifier une courbe", "« laquelle des courbes représente u_R ? », « quelle courbe pour L₁ = 2L₀ ? »",
    "u_R(0) = 0 car i(0) = 0, u_b(0) = E ; si L change : même palier U₀ = R·E/(R + r), τ change", ["2016 R", "2019 R", "2022 R"], "0,5"),
 ct("schema", "schéma, branchement de l'acquisition", "« représenter le schéma », « comment brancher… »",
    "flèche de u_R opposée à i (convention récepteur) ; acquisition en dérivation aux bornes du dipôle visé", ["2017 N", "2018 R", "2021 R", "2022 R"], "0,25 à 0,5"),
]

erreurs_examen = [
 {"question": "équation, τ, I₀", "perte": "oublier r", "geste": "écrire u_b = L·di/dt + r·i dès la loi d'Ohm puis regrouper (R + r)·i ; r = 0 seulement si l'énoncé le dit"},
 {"question": "rupture", "perte": "second membre E au lieu de 0", "geste": "refaire la maille après la bascule : u_R + u_b = 0"},
 {"question": "identifier les courbes", "perte": "confondre u_R et u_b", "geste": "à t = 0 : i = 0 donc u_R(0) = 0 et u_b(0) = E"},
 {"question": "u_b en régime permanent", "perte": "écrire u_b = 0 pour une bobine réelle", "geste": "u_b(∞) = r·I₀ ; 0 seulement si r = 0"},
 {"question": "équation en u_R", "perte": "second membre E au lieu de R·E/L", "geste": "remplacer i par u_R/R partout puis multiplier toute l'équation par R"},
 {"question": "vérifier la solution", "perte": "une seule condition écrite, ou condition initiale oubliée", "geste": "« pour tout t » puis deux égalités ; i(0) = 0 pour B"},
 {"question": "lire τ", "perte": "tangente mal coupée ; 63 % de E au lieu de la valeur finale lue", "geste": "écrire la méthode en une phrase ; 63 % de la valeur finale (2022 R : de 9,8 V)"},
 {"question": "unités", "perte": "ms, mA, mH non convertis ; axe en mA lu en A (2024 N)", "geste": "convertir avant le calcul ; lire l'unité de chaque axe"},
 {"question": "I₀", "perte": "I₀ = E/R", "geste": "Pouillet avec toutes les résistances de la maille : I₀ = E/(R + r)"},
 {"question": "énergie", "perte": "I₀ au lieu de i(t) ; oubli du carré ou du ½", "geste": "i(t) = u_R(t)/R lu à l'instant demandé, puis ½·L·i²"},
 {"question": "courbe pour une autre L (2022 R)", "perte": "choix sans éliminer la courbe dont le palier change", "geste": "U₀ ne dépend pas de L : même palier, τ double → montée plus lente"},
 {"question": "rupture avec diode (2025 R)", "perte": "i(0⁺) = 0 ou u_b = 0", "geste": "i continue : i(0⁺) = I₀ ; maille bobine–diode–R₁ : u_b = −R₁·I₀"},
]

pieges = [
 {"erreur": "τ = L/R alors que la bobine a une résistance r", "geste": "τ = L/(R + r), la résistance totale du circuit"},
 {"erreur": "croire que L diminue le courant final", "geste": "I₀ = E/(R + r) ne contient pas L ; L ne fait que retarder"},
 {"erreur": "écrire u_b = L·i", "geste": "u_b dépend de la pente : L·di/dt (+ r·i)"},
 {"erreur": "faire partir i de 0 à la rupture", "geste": "continuité : i(0⁺) = valeur juste avant = I₀"},
 {"erreur": "projeter 0,63·I₀ sur la tangente", "geste": "l'horizontale va jusqu'à la COURBE, puis on descend sur l'axe des temps"},
 {"erreur": "u_b reste nulle au début car i = 0", "geste": "i = 0 mais di/dt maximal : u_b(0) = E"},
]

questions_eleves = [
 {"question": "Pourquoi u_b vaut E à la fermeture alors que i = 0 ?", "reponse": "u_b dépend de di/dt, pas de i. À t = 0, i = 0 donc u_R = 0 et toute la tension E est aux bornes de la bobine : u_b(0) = E."},
 {"question": "Pourquoi τ = L/(R + r) et pas L/R ?", "reponse": "Le courant traverse R et le fil de la bobine : la résistance totale de la maille est R + r. Si la bobine est idéale (r = 0), on retrouve L/R."},
 {"question": "Est-ce que la bobine diminue le courant ?", "reponse": "Non : elle le retarde. À la fin, I₀ = E/(R + r) ne dépend pas de L."},
 {"question": "I₀ ou I_p, c'est pareil ?", "reponse": "Oui : les sujets écrivent I₀, I_p ou I_P pour l'intensité du régime permanent."},
 {"question": "u_L, u_b, u_B : c'est la même tension ?", "reponse": "Oui, c'est la tension aux bornes de la bobine ; chaque sujet choisit sa lettre. Toujours u = L·di/dt + r·i en convention récepteur."},
 {"question": "Pourquoi le second membre est 0 à la rupture ?", "reponse": "Le générateur n'est plus dans la maille : u_R + u_b = 0."},
 {"question": "Comment savoir si la bobine est idéale ?", "reponse": "L'énoncé dit « résistance négligeable » ou r = 0. Sinon on garde r ; s'il faut la calculer, c'est en régime permanent."},
]

commentaires_eleves = [
 {"plainte": "(vidéos non auditées : commentaires d'élèves non lus) difficultés attendues d'après le RC et les nationaux : u_b(0) = E alors que i = 0", "vu": "anticipé", "besoin": "voir la pente maximale à t = 0", "reponse_du_cours": "e6 (v_courbe, ub)"},
 {"plainte": "oubli de r (anticipé, première perte de points)", "vu": "nationaux (5 sessions demandent r)", "besoin": "un réflexe d'écriture", "reponse_du_cours": "b8, e2, l3, b10, e8"},
 {"plainte": "lecture de τ (anticipé : 8 commentaires sur ce point au RC)", "vu": "exploration dipole_RC", "besoin": "voir la tangente et les 63 % se tracer", "reponse_du_cours": "l1, l2 (v_courbe tangente, pourcent)"},
 {"plainte": "rupture : signe et continuité (anticipé)", "vu": "2025 R", "besoin": "voir i continuer puis descendre, u_b devenir négative", "reponse_du_cours": "b4, t2, t4 (v_rupture)"},
]

cadre = {
 "_note": "Fiche du chapitre, même forme que cadre_reference_2bac_pc.json. Capacités d'après perimetre.json (dipole_RL), la grille officielle citée dans les corrigés 2024 N / 2024 R et les nationaux PC 2016-2025. Texte officiel du cadre non relu mot à mot : RL1 à RL8 provisoires.",
 "titre": "Dipôle RL",
 "source": "CDR-PC-2015, annexe 1, Électricité : « Dipôle RL (inductance, équation différentielle, retard à l'établissement du courant, énergie magnétique) » ; OP-PC-2007 ; perimetre.json clé dipole_RL ; nationaux PC 2016-2025 du dépôt (RL dans 10 sessions sur 20).",
 "capacites": [
  {"id": "RL1", "texte": "Connaître la bobine (symbole, inductance L en henry, résistance r) et la tension à ses bornes en convention récepteur u = L·di/dt + r·i (expression admise) ; bobine idéale : u = L·di/dt."},
  {"id": "RL2", "texte": "Savoir qu'une bobine retarde l'établissement et la disparition du courant (auto-induction), que i est continue dans une bobine alors que la tension à ses bornes peut être discontinue, et qu'en régime permanent elle se comporte comme une résistance r."},
  {"id": "RL3", "texte": "Décrire la réponse d'un dipôle RL à un échelon de tension : régime transitoire, régime permanent, I₀ = E/(R + r) ; visualiser i par u_R = R·i (oscilloscope ou acquisition informatisée)."},
  {"id": "RL4", "texte": "Établir l'équation différentielle vérifiée par i ou u_R à l'établissement et à la rupture du courant (additivité des tensions, u_R = R·i, u = L·di/dt + r·i)."},
  {"id": "RL5", "texte": "Vérifier qu'une expression est solution de l'équation différentielle et déterminer ses constantes (A, B, τ) avec l'équation et la condition initiale ; écrire i(t), u_R(t), u_b(t)."},
  {"id": "RL6", "texte": "Connaître la constante de temps τ = L/(R + r), montrer qu'elle est homogène à un temps, et prévoir l'influence de L et de R sur l'établissement du courant."},
  {"id": "RL7", "texte": "Exploiter des résultats expérimentaux (courbes i(t), u_R(t), u_b(t), droite di/dt = f(i)) pour déterminer τ (tangente, 63 %, 37 %), I₀, E, r et L."},
  {"id": "RL8", "texte": "Connaître et exploiter l'expression de l'énergie magnétique emmagasinée dans une bobine E_m = ½·L·i² (expression admise)."},
 ],
 "formules": [
  {"ecriture": "u_b = L·di/dt + r·i", "capacite": "RL1", "dit": "u b égale L dé i sur dé t plus r i", "phrase": "convention récepteur ; L en henry (H), r en ohm ; les sujets écrivent aussi u_L, u_B", "variantes_admises": ["u_L = L·di/dt + r·i", "u_L = L·di/dt (bobine idéale)"]},
  {"ecriture": "u_b = L·di/dt", "capacite": "RL1", "dit": "u b égale L dé i sur dé t", "phrase": "bobine idéale (r = 0)"},
  {"ecriture": "u_b = r·I₀", "capacite": "RL2", "dit": "en régime permanent, u b égale r fois I zéro", "phrase": "di/dt = 0 : la bobine se comporte comme une résistance r"},
  {"ecriture": "u_R + u_b = E", "capacite": "RL4", "dit": "u R plus u b égale E", "phrase": "loi d'additivité des tensions à l'établissement ; à la rupture u_R + u_b = 0"},
  {"ecriture": "L·di/dt + (R + r)·i = E", "capacite": "RL4", "dit": "L dé i sur dé t plus R plus r fois i égale E", "phrase": "équation différentielle de l'établissement",
   "variantes_admises": ["di/dt + ((R + r)/L)·i = E/L", "di/dt + (1/τ)·i = E/L", "di/dt = −((R + r)/L)·i + E/L", "du_R/dt + ((R + r)/L)·u_R = R·E/L", "L·di/dt + (R + r)·i = 0", "(L/(R + r))·du_R/dt + u_R = 0"]},
  {"ecriture": "di/dt + ((R + r)/L)·i = E/L", "capacite": "RL4", "dit": "dé i sur dé t plus R plus r sur L fois i égale E sur L", "phrase": "forme finale des corrigés"},
  {"ecriture": "i(t) = I₀(1 − e^(−t/τ))", "capacite": "RL5", "dit": "i de t égale I zéro fois un moins exponentielle de moins t sur tau", "phrase": "établissement, i(0) = 0",
   "variantes_admises": ["i(t) = A(1 − e^(−t/τ))", "i(t) = A + B·e^(−t/τ)", "i(t) = (E/R)(1 − e^(−R·t/L))"]},
  {"ecriture": "I₀ = E/(R + r)", "capacite": "RL3", "dit": "I zéro égale E sur R plus r", "phrase": "intensité du régime permanent (notée aussi I_p, I_P)"},
  {"ecriture": "U_R = R·E/(R + r)", "capacite": "RL3", "dit": "U R égale R E sur R plus r", "phrase": "tension u_R du régime permanent"},
  {"ecriture": "i(t) = I₀·e^(−t/τ)", "capacite": "RL5", "dit": "i de t égale I zéro exponentielle de moins t sur tau", "phrase": "rupture, i(0) = I₀ (continuité) ; au national : u_R = R·I₀·e^(−t/τ)"},
  {"ecriture": "u_b(t) = E·e^(−t/τ)", "capacite": "RL5", "dit": "u b de t égale E exponentielle de moins t sur tau", "phrase": "établissement, bobine idéale"},
  {"ecriture": "τ = L/(R + r)", "capacite": "RL6", "dit": "tau égale L sur R plus r", "phrase": "constante de temps, en seconde ; bobine idéale τ = L/R", "variantes_admises": ["τ = L/R"]},
  {"ecriture": "[τ] = [L]/[R] = [T]", "capacite": "RL6", "dit": "la dimension de tau est un temps"},
  {"ecriture": "i(τ) = 0,63·I₀ ; i(τ) = 0,37·I₀ (rupture)", "capacite": "RL7", "dit": "à t égale tau, i vaut soixante-trois pour cent de I zéro, trente-sept pour cent à la rupture"},
  {"ecriture": "L = τ·(R + r)", "capacite": "RL7", "dit": "L égale tau fois R plus r", "phrase": "la question de tous les nationaux RL"},
  {"ecriture": "r = E/I₀ − R", "capacite": "RL7", "dit": "r égale E sur I zéro moins R", "variantes_admises": ["r = u_b/I₀", "r = R·(E/U_R − 1)"]},
  {"ecriture": "E_m = ½·L·i²", "capacite": "RL8", "dit": "E m égale un demi L i au carré", "phrase": "énergie en joule ; maximale en régime permanent ½·L·I₀²"},
 ],
 "mots_cles": ["bobine", "inductance", "henry", "résistance interne", "auto-induction", "convention récepteur", "échelon de tension", "dipôle RL",
               "établissement du courant", "rupture du courant", "continuité de l'intensité", "régime transitoire", "régime permanent", "équation différentielle",
               "solution", "condition initiale", "constante de temps", "tangente à l'origine", "asymptote", "énergie magnétique", "surtension", "diode"],
 "hors_cadre": {"mots": ["loi de Faraday", "loi de Lenz", "flux magnétique", "force électromotrice induite", "inductance mutuelle", "transformateur", "perméabilité",
                         "réactance", "déphasage", "régime sinusoïdal", "roue libre", "second ordre"],
                "motifs": [x["motif"] for x in A.a_ne_pas_dire]},
 "valeurs_reference": ["1 − e^(−1) ≈ 0,63 ; e^(−1) ≈ 0,37", "r de la bobine : 5 ou 10 Ω dans les nationaux", "L de 2 mH à 1 H ; τ de 2 µs à 10 ms"],
}

data = {
 "cle": "dipole_RL", "matiere": "physique-chimie", "filiere": "2e Bac Sciences Physiques BIOF (Maroc)", "titre": "Dipôle RL", "date_exploration": "2026-11-12",
 "_note": ("Exploration du 12 novembre 2026 (routine cloud, skill exploration-de-cours ; le cours phys_ch7_dipole_RL n'est pas construit). "
           "VIDÉOS NON AUDITÉES : YouTube bloqué depuis le cloud (yt-dlp absent, installation impossible) ; aucune vidéo de professeur lue. "
           "L'exploration s'appuie sur les 20 nationaux PC 2016-2025 du dépôt (RL dans 10 sessions, analyse détaillée : outils/cours/notes/cours/dipole_RL_build/nationaux.md), "
           "sur perimetre.json (dipole_RL), sur la grille officielle citée dans les corrigés 2024, et sur l'exploration dipole_RC (même méthode, mêmes professeurs, "
           "même tableau). À compléter par l'audit de dix vidéos depuis le PC Windows avant validation."),
 "sources": {"videos": [], "videos_note": "aucune : YouTube inaccessible depuis le conteneur cloud (12/11/2026)",
             "examens": [f"backend/data/exams/physique/{s[:4]}-{'normale' if s[-1] == 'N' else 'rattrapage'}" for s in NAT],
             "autres": ["backend/data/curriculum/perimetre.json (dipole_RL)", "backend/data/curriculum/exploration/dipole_RC.json", "database/seed_data/lessons/phys_ch7_l1.json"]},
 "comparaison": {"_note": "sans vidéos : comparaison faite entre les corrigés des dix sessions RL (notations, formes de l'équation, méthodes pour r)",
                 "convergences": ["R + r toujours écrit tel quel (jamais R_t)", "équation d'abord L·di/dt + (R + r)·i = E puis divisée par L", "L = τ·(R + r) avec τ lu à la tangente", "u = L·di/dt + r·i en convention récepteur"],
                 "variantes_admises": [{"variante": "I₀, I_p, I_P", "decision": "le cours écrit I₀ et dit « I₀ (les sujets écrivent aussi I_p) »"},
                                       {"variante": "u_b, u_L, u_B", "decision": "le cours écrit u_b ; il annonce que u_L et u_B désignent la même tension"},
                                       {"variante": "solution A(1 − e^(−t/τ)) ou A + B·e^(−t/τ)", "decision": "les deux sont faites (s1-s4, puis un exercice A + B)"},
                                       {"variante": "quatre méthodes pour r", "decision": "toutes vues : b10 (u_b/I₀), e8 (U_R), l3 (E/I₀ − R), n1"}],
                 "meilleures_explications": ["la même recette que le RC (additivité, remplacer, ranger) : renvoi au chapitre précédent", "u_b(0) = E par la continuité de i"]},
 "cadre": cadre,
 "insistances": ["toute équation part de la loi d'additivité lue sur le circuit", "r ne s'oublie jamais : u_b = L·di/dt + r·i, puis (R + r)·i",
                 "i est continue dans une bobine : i(0) = 0 à la fermeture, i(0⁺) = I₀ à la rupture", "u_R est l'image de i : i = u_R/R",
                 "la valeur de L est demandée dans tous les sujets : L = τ·(R + r)"],
 "valeurs_reperes": ["1 − e^(−1) ≈ 0,63 ; e^(−1) ≈ 0,37", "2019 R : E = 10 V, R = 40 Ω, U_R = 8 V → r = 10 Ω ; τ = 10 ms → L = 0,5 H",
                     "2021 R : E = 6 V, R₂ = 95 Ω, I₀ = 60 mA → r = 5 Ω ; τ = 5,1 ms → L = 0,51 H", "2022 R : U₀ = 9,8 V, R = 490 Ω → I₀ = 0,02 A, r = 10 Ω, L₀ = 0,5 H",
                     "2024 N : E/L = 3·10³ A/s → L = 2 mH ; τ = 2 µs", "2025 R : I₀ = 0,1 A, L = 0,1 H, E_m = 5·10⁻⁴ J, u_b(0⁺) = −100 V"],
 "cas_types": cas_types, "pieges": pieges, "erreurs_examen": erreurs_examen,
 "conseils": ["le RL tombe dans 10 sessions sur 20 (une par année), toujours en première partie de l'exercice d'électricité, 1,5 à 4 points",
              "deux questions sûres : une équation différentielle et la valeur de L", "écrire la méthode de lecture de τ en une phrase : elle est notée",
              "convertir ms, mA, mH avant tout calcul"],
 "analogies_validees": A.analogies_validees, "a_ne_pas_dire": A.a_ne_pas_dire, "exclus_hors_programme": A.exclus_hors_programme,
 "questions_eleves": questions_eleves, "commentaires_eleves": commentaires_eleves, "notions_complexes": A.notions_complexes,
 "visuels": A.visuels, "regles_des_simulations": A.regles_des_simulations,
 "redaction_nationale": {"_note": "lignes attendues d'après les corrigés du dépôt (pas des barèmes officiels ; une erreur relevée en 2024 N, voir limites)",
     "etablir_ED": ["u_R + u_b = E", "u_R = R·i ; u_b = L·di/dt + r·i", "L·di/dt + (R + r)·i = E", "di/dt + ((R + r)/L)·i = E/L"],
     "verifier_solution": ["di/dt = (A/τ)·e^(−t/τ)", "on remplace et on regroupe", "pour tout t : L/τ − (R + r) = 0 et (R + r)·A − E = 0", "τ = L/(R + r) ; A = E/(R + r)"],
     "trouver_r": ["I₀ = U_R/R (lu)", "I₀ = E/(R + r)", "r = E/I₀ − R = … Ω"],
     "trouver_L": ["τ lu par la tangente à l'origine : τ = … s", "τ = L/(R + r)", "L = τ·(R + r) = … H"],
     "energie": ["i = u_R/R à l'instant demandé", "E_m = ½·L·i² = … J"]},
 "plan": {"principes": "une idée nouvelle par diapositive ; une chose vue, une phrase, une question ; même tableau et même boîte des relations que le RC ; la forme de l'équation et la lecture de τ comme au RC, avec r en plus ; chaque bloc finit sur une question d'un sujet national ; prédiction sur au moins une diapositive sur trois",
          "duree_estimee_min": 200,
          "decoupage_conseille": "quatre séances de trois blocs de quatre diapositives (bilan et carte dans le dernier bloc)",
          "prerequis_verifies_au_debut": ["loi_ohm_tension_intensite", "lois_kirchhoff", "derivee_usuelle"],
          "seances": B.seances, "competences": B.competences, "diapositives": B.diapositives},
 "cours_existant": A.cours_existant,
 "renvois": {"au_chapitre_dipole_RC": "même méthode (additivité, équation, solution, τ, tangente, 63 %) ; rappelée en o2 et e1", "au_chapitre_RLC": "décharge d'un condensateur dans une bobine, énergie ½·C·u_C² + ½·L·i² ; u_b(0⁺) au début d'une décharge (2024 R) reprend t4"},
 "decisions_utilisateur": [
  {"question": "Garde-t-on l'analyse dimensionnelle de τ ?", "constat": "jamais demandée au national pour le RL, mais « démonstration attendue » dans perimetre.json", "proposition": "oui, une diapositive (s5)"},
  {"question": "Garde-t-on l'influence de R sur τ ?", "constat": "jamais demandée (seulement L, 2022 R) ; perimetre.json la cite", "proposition": "oui, une diapositive (s8)"},
  {"question": "Étincelle et diode à la rupture ?", "constat": "étincelle jamais demandée ; diode + R₁ en 2025 R ; « roue libre » hors programme (perimetre.json)", "proposition": "étincelle en une phrase (t3), diode + R₁ traitée par l'exercice 2025 R (t4), le mot « roue libre » jamais dit"},
  {"question": "Courant triangulaire (GBF) pour faire voir u = L·di/dt ?", "constat": "TP habituel « tension aux bornes d'une bobine » (CDR annexe 2), pas un cas de national", "proposition": "oui, deux diapositives (b6, b7) : c'est la façon de VOIR que u suit la pente"},
  {"question": "Notation I₀ ou I_p ?", "constat": "les deux dans les sujets", "proposition": "I₀ écrit, I_p annoncé"},
  {"question": "Code couleur des courbes", "constat": "rouge/bleu pris par charge/décharge au RC", "proposition": "vert = établissement, bleu = rupture"},
 ],
 "limites_de_l_exploration": ["VIDÉOS NON AUDITÉES : aucun des dix professeurs (YouTube bloqué depuis le cloud) ; à faire depuis le PC avant validation",
     "commentaires d'élèves non lus : difficultés anticipées d'après le RC et les nationaux",
     "corrigé du dépôt faux en 2024 N 2.2.2 (τ = 6,7·10⁻⁴ s au lieu de 2 µs : axe en mA lu en A) ; données manquantes dans exam.json pour 2016 R, 2017 N, 2018 R, 2020 N, 2024 N ; mauvaises figures liées en 2022 R (voir nationaux.md § 6)",
     "capacités RL1-RL8 provisoires (texte officiel non relu mot à mot)"],
}

def verification(d):
    caps = {c["id"]: [] for c in cadre["capacites"]}
    comp2cap = {c["id"]: c["cadre_ids"] for c in B.competences}
    for s in B.diapositives:
        for c in s["competences"]:
            for k in comp2cap[c]:
                caps[k].append(s["id"])
    return {"dix_professeurs": "non : aucune vidéo (YouTube bloqué depuis le cloud) ; remplacés par les dix sessions RL des nationaux",
            "capacites_du_cadre_dans_le_plan": caps,
            "toutes_les_capacites": all(caps.values()),
            "diapositives": len(B.diapositives), "predictions": sum(x["prediction"] for x in B.diapositives),
            "rappels": sum(len(c["rappels"]) for c in B.competences)}
data["verification"] = verification(data)

if __name__ == "__main__":
    out = Path("backend/data/curriculum/exploration/dipole_RL.json")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    v = data["verification"]
    print(out, out.stat().st_size, "octets ;", v["diapositives"], "diapositives,", v["predictions"], "prédictions,", v["rappels"], "rappels ; capacités toutes couvertes :", v["toutes_les_capacites"])
