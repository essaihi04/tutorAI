# -*- coding: utf-8 -*-
"""Écrit backend/data/curriculum/exploration/circuit_RLC.json (parties A et B + ce qui vient des nationaux, nationaux.md).
Lancer depuis la racine du dépôt : python3 outils/cours/notes/cours/circuit_RLC_build/explo.py"""
import json, sys, re, copy
from pathlib import Path
ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import explo_a as A, explo_b as B

# Sessions avec RLC (17 sur 20 ; pas de RLC en 2016 R, 2017 N, 2018 R)
NAT = ["2016 N", "2017 R", "2018 N", "2019 N", "2019 R", "2020 N", "2020 R", "2021 N", "2021 R", "2022 N", "2022 R",
       "2023 N", "2023 R", "2024 N", "2024 R", "2025 N", "2025 R"]

# --- Partie A relue : écriture des sujets pour l'entretien (u_G = k·i, jamais « R₀ ») et capacités RLC1-RLC8 définitives ---
def _sujets(o):
    """Remplace l'écriture provisoire u = R₀·i de la partie A par celle des sujets : u_G = k·i, k."""
    if isinstance(o, str):
        return o.replace("u = R₀·i", "u_G = k·i").replace("R₀", "k")
    if isinstance(o, list):
        return [_sujets(x) for x in o]
    if isinstance(o, dict):
        return {k: _sujets(v) for k, v in o.items()}
    return o

notions_complexes = _sujets(copy.deepcopy(A.notions_complexes))
analogies_validees = _sujets(copy.deepcopy(A.analogies_validees))
exclus_hors_programme = _sujets(copy.deepcopy(A.exclus_hors_programme))
regles_des_simulations = _sujets(A.regles_des_simulations)
visuels = _sujets(copy.deepcopy(A.visuels))
CAP_VISUELS = {"v_circuit_lc": "RLC1, RLC6", "v_equation": "RLC3", "v_oscillogramme": "RLC2, RLC5", "v_solution": "RLC4",
               "v_periode": "RLC4, RLC5", "v_energie": "RLC6, RLC7", "v_entretien": "RLC8", "v_analogie": "RLC1, RLC2", "v_figures": "RLC5"}
for s in visuels["simulations"]:
    if s["id"] in CAP_VISUELS:
        s["capacite"] = CAP_VISUELS[s["id"]]
visuels["_note"] += " Capacités renumérotées RLC1-RLC8 (fiche du cadre ci-dessous) ; entretien écrit u_G = k·i comme les sujets."
for v in visuels["simulations"]:
    if v["id"] == "v_entretien":
        v["poignees"] = ["k"]

def ct(id, nom, indices, methode, sessions, points):
    return {"id": id, "nom": nom, "indices": indices, "methode": methode, "sessions": sessions, "points": points}

cas_types = [
 ct("ed", "établir l'équation différentielle (décharge) en q ou en u_C", "« établir / montrer que l'équation différentielle vérifiée par q(t) / u_C(t) », « loi d'additivité des tensions »",
    "additivité SANS générateur u_C + u_R + u_b = 0 ; u_b = L·di/dt + r·i, u_R = R·i, u_C = q/C, i = dq/dt = C·du_C/dt ; di/dt = d²q/dt² = C·d²u_C/dt² → L·d²q/dt² + (R + r)·dq/dt + q/C = 0 ou LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0 ; LC idéal : d²u_C/dt² + u_C/(LC) = 0",
    ["2017 R", "2019 N", "2020 N", "2020 R", "2021 N", "2022 N", "2022 R", "2023 N", "2023 R", "2024 N", "2024 R", "2025 N"], "0,25 à 0,75 (2024 R : 0,5 méthode + 0,25 équation)"),
 ct("T0", "vérifier la solution, trouver l'expression de T₀", "« sachant que q = Q_m·cos(2πt/T₀), trouver l'expression de T₀ »",
    "dq/dt = −(2π/T₀)·Q_m·sin(2πt/T₀) ; d²q/dt² = −(2π/T₀)²·q ; on remplace : [1/(LC) − (2π/T₀)²]·q = 0 pour tout t → T₀ = 2π√(LC) ; toujours cos sans φ, départ au maximum",
    ["2017 R", "2021 N", "2022 N"], "0,5"),
 ct("L_C", "lire T (ou T₀) et trouver L ou C", "« en assimilant la pseudo-période à la période propre », « sachant que T ≈ T₀ », « on prend π² = 10 »",
    "T lue entre deux maxima (sur plusieurs périodes si possible) ; T₀² = 4π²·L·C → L = T₀²/(4π²·C) ou C = T₀²/(4π²·L) ; T₀ en s, C en F",
    ["2016 N", "2017 R", "2018 N", "2019 N", "2019 R", "2020 N", "2020 R", "2021 N", "2021 R", "2022 N", "2022 R", "2023 N", "2025 N"], "0,25 à 0,75"),
 ct("regime", "reconnaître le régime, choisir ou affecter une courbe", "« quel est le régime ? », « choisir la courbe », « affecter chaque courbe à la résistance »",
    "sommets décroissants + changement de signe → pseudo-périodique ; retour sans oscillation → apériodique ; LC idéal → périodique (choisir la courbe : amplitude constante ET u_C(0) = E) ; plus R + r est grande, plus l'amortissement est fort",
    ["2016 N", "2018 N", "2019 N", "2019 R", "2020 N", "2020 R", "2021 N", "2021 R", "2022 N"], "0,25 à 0,5"),
 ct("energie", "énergie à un instant", "« calculer l'énergie totale à l'instant … », « l'énergie magnétique à t = … »",
    "E_t = ½·C·u_C² + ½·L·i² = q²/(2C) + ½·L·i² ; u_C extrême → i = 0 → seulement ½·C·u_C² ; u_C = 0 → seulement ½·L·i² ; sinon les deux termes ; LC idéal : E_t constante → E_m = E_t − ½·C·u_C² ; I_m = U_m·√(C/L)",
    ["2016 N", "2017 R", "2019 N", "2019 R", "2020 N", "2020 R", "2022 N", "2023 N", "2023 R", "2024 N", "2024 R", "2025 N", "2025 R"], "0,25 à 0,75"),
 ct("perte", "énergie dissipée entre deux instants", "« énergie dissipée par effet Joule entre t = 0 et t₁ », « variation de l'énergie totale »",
    "E_t(début) − E_t(fin) > 0, de préférence à deux extremums (i = 0) : ½·C·(U₁² − U₂²) ou (q₁² − q₂²)/(2C) ; courbes E_e, E_m : lire la somme",
    ["2016 N", "2021 R", "2022 N", "2023 R", "2024 N", "2024 R", "2025 N"], "0,5 à 0,75"),
 ct("amortissement", "expliquer l'amortissement, montrer dE/dt", "« expliquer la diminution de l'amplitude », « du point de vue énergétique », « montrer que dE_T/dt = −r·i² »",
    "l'énergie totale diminue : dissipée par effet Joule dans R et r ; dE/dt = C·u_C·du_C/dt + L·i·di/dt = i·(u_C + L·di/dt) = −(R + r)·i²",
    ["2016 N", "2018 N", "2020 R", "2023 R", "2024 N", "2025 N"], "0,25 à 0,5"),
 ct("entretien", "entretien des oscillations par u_G = k·i", "« générateur délivrant une tension proportionnelle à l'intensité u_G = k·i », « trouver k (k₀) »",
    "u_C + u_R + u_b = k·i → L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0 ; oscillations sinusoïdales → k = R + r (résistance totale) ; le circuit oscille à T₀",
    ["2016 N", "2018 N", "2020 N", "2023 R"], "0,5 à 0,75"),
 ct("phase", "expression i(t) ou u_C(t) avec φ", "« déterminer I_m, T₀ et φ »",
    "I_m et T₀ lus ; i(0) = I_m·cos φ ; le sens de départ donne le signe de sin φ (di/dt(0) = −(2π/T₀)·I_m·sin φ) ; 2020 N : i(0) = 0, i descend → φ = +π/2",
    ["2020 N"], "0,75"),
 ct("instant", "instant initial et signe de i", "« valeur de u_b juste après la bascule », « signe de i entre t_A et t_B »",
    "i continue dans la bobine : i(0⁺) = 0 → u_R(0⁺) = 0 → u_b(0⁺) = −u_C(0) ; i = C·du_C/dt : u_C décroît → i < 0",
    ["2024 R", "2025 N"], "0,25 à 0,5"),
]

erreurs_examen = [
 {"question": "équation différentielle", "perte": "E au second membre", "geste": "refaire la maille après la bascule, sans générateur : … = 0"},
 {"question": "équation différentielle", "perte": "oublier r (ou R), ou écrire r quand la bobine est « de résistance négligeable »", "geste": "lister les dipôles de la maille avant d'écrire"},
 {"question": "lire T", "perte": "lire entre un sommet et un creux (T/2)", "geste": "deux maxima successifs, ou n périodes entières puis diviser par n (2025 N : 4 carreaux)"},
 {"question": "unités", "perte": "µF, nF, mH, ms, µC non convertis ; axe de u_R en mV lu en V (2024 R)", "geste": "convertir avant la formule ; lire l'unité de chaque axe"},
 {"question": "trouver L ou C", "perte": "isoler sans élever au carré", "geste": "T₀² = 4π²·L·C d'abord, puis L = T₀²/(4π²·C)"},
 {"question": "cos ou sin, phase", "perte": "φ = 0 par habitude ; i(0) = 0 sans le sens de départ", "geste": "u_C(0) donne cos φ, le sens de départ donne le signe de sin φ (2020 N : φ = +π/2)"},
 {"question": "signe de i", "perte": "i toujours positif", "geste": "i = C·du_C/dt : u_C décroît → i < 0 (2025 N)"},
 {"question": "énergie à un instant", "perte": "oublier un des deux termes", "geste": "u_C extrême → i = 0 ; u_C = 0 → i extrême ; sinon les deux termes"},
 {"question": "énergie perdue", "perte": "annoncer E(fin) − E(début) < 0 comme énergie dissipée", "geste": "|ΔE| = E(début) − E(fin) > 0, à deux sommets (i = 0)"},
 {"question": "lecture de u_C", "perte": "mauvaise valeur à un creux (2024 N : −4,4 V)", "geste": "lire avec le signe ; le carré enlève le signe, pas une mauvaise lecture"},
 {"question": "entretien", "perte": "k = r seulement alors qu'il y a aussi R (2020 N : k₀ = R + r = 100 Ω)", "geste": "k = résistance totale de la maille"},
 {"question": "régimes", "perte": "inverser les courbes (erreur du dépôt en 2021 R)", "geste": "plus R + r est grande, plus l'amortissement est fort ; apériodique = retour sans changer de signe"},
 {"question": "u_b(0⁺)", "perte": "écrire 0 ou +E", "geste": "i continue → i(0⁺) = 0 → u_R(0⁺) = 0 → u_b(0⁺) = −u_C(0)"},
]

pieges = [
 {"erreur": "croire que R fait osciller le circuit", "geste": "L et C échangent l'énergie ; R + r ne fait qu'amortir"},
 {"erreur": "T₀ = 2π√(L/C) ou 2π·LC", "geste": "T₀ = 2π√(LC) : vérifier l'unité (√(LC) en secondes)"},
 {"erreur": "croire que T₀ dépend de E", "geste": "E change U_m, pas T₀"},
 {"erreur": "U_m = écart sommet–creux", "geste": "U_m = hauteur d'un sommet par rapport à 0"},
 {"erreur": "appeler « périodique » un régime amorti", "geste": "périodique seulement si R + r = 0 ou entretenu ; sinon pseudo-périodique"},
 {"erreur": "½·C·u_C sans carré ; ½·L·i à un sommet de u_C", "geste": "½·C·u_C² ; au sommet de u_C, i = 0"},
 {"erreur": "croire que E_e et E_m ont la période T₀", "geste": "elles reviennent à leur maximum deux fois par période (T₀/2)"},
 {"erreur": "croire que le générateur d'entretien impose sa période", "geste": "il compense l'effet Joule ; le circuit oscille à T₀"},
]

questions_eleves = [
 {"question": "Qui recharge le condensateur à l'envers ?", "reponse": "La bobine : quand u_C = 0 le courant est maximal, et la bobine s'oppose à sa diminution ; le courant continue dans le même sens et charge l'armature d'en face."},
 {"question": "Pourquoi « libres » ?", "reponse": "Il n'y a aucun générateur pendant les oscillations : le circuit oscille avec l'énergie mise au départ dans le condensateur."},
 {"question": "Pseudo-période ou période propre, c'est pareil ?", "reponse": "Non : T₀ = 2π√(LC) est la période du LC idéal ; T est la pseudo-période mesurée avec une résistance. Si l'amortissement est faible, T ≈ T₀ (les sujets le disent)."},
 {"question": "Pourquoi l'énergie diminue si personne ne la prend ?", "reponse": "Les résistances R et r chauffent : dE/dt = −(R + r)·i², l'énergie part en chaleur (effet Joule)."},
 {"question": "E_m, c'est l'énergie mécanique ?", "reponse": "Non : ici E_m est l'énergie magnétique de la bobine, ½·L·i². E_e est l'énergie électrique du condensateur."},
 {"question": "Faut-il écrire ω₀ ?", "reponse": "On peut, mais les sujets écrivent toujours 2π/T₀. Retiens d'abord T₀ = 2π√(LC)."},
 {"question": "Pourquoi k = R + r et pas k = r ?", "reponse": "Le générateur doit compenser toute la résistance de la maille : le terme (R + r − k)·dq/dt doit être nul."},
 {"question": "Comment savoir si i est positif ?", "reponse": "i = C·du_C/dt : si u_C augmente, i > 0 ; si u_C diminue, i < 0 (avec les flèches du schéma)."},
]

commentaires_eleves = [
 {"plainte": "(vidéos non auditées : commentaires d'élèves non lus) difficulté attendue : u_C qui devient négative", "vu": "anticipé (au RC la décharge s'arrête à 0)", "besoin": "voir le courant continuer quand u_C = 0", "reponse_du_cours": "d1, d2, d3 (v_circuit_lc bascule)"},
 {"plainte": "dériver deux fois un cosinus (anticipé)", "vu": "anticipé d'après le RL (dérivées de e^(−t/τ))", "besoin": "les deux dérivées écrites l'une sous l'autre", "reponse_du_cours": "o2, e7 (v_solution derivee_1, derivee_2)"},
 {"plainte": "confusion T et T/2 à la lecture (anticipé, erreur fréquente des corrigés)", "vu": "nationaux (13 sessions lisent T)", "besoin": "compter les périodes entre sommets", "reponse_du_cours": "l1 (v_oscillogramme mesure_nT), C5_r1, C5_r3"},
 {"plainte": "énergie à un instant : un terme oublié (anticipé)", "vu": "nationaux (14 sessions ont une énergie)", "besoin": "savoir quand i = 0 et quand u_C = 0", "reponse_du_cours": "en3, en4, a4, C6_r4"},
 {"plainte": "le choix de φ (anticipé)", "vu": "2020 N III.2", "besoin": "voir les deux angles puis le sens de départ", "reponse_du_cours": "c3, c4, n1"},
]

cadre = {
 "_note": "Fiche du chapitre, même forme que cadre_reference_2bac_pc.json. Capacités d'après perimetre.json (circuit_RLC), la grille officielle citée dans les corrigés 2023 R / 2024 N et les nationaux PC 2016-2025. Texte officiel du cadre non relu mot à mot : RLC1 à RLC8 provisoires (elles remplacent RLC1 à RLC7 de la partie A).",
 "titre": "Oscillations libres d'un circuit RLC série",
 "source": "CDR-PC-2015, annexe 1, Électricité : « Circuit RLC série (amortissement, régimes périodique/pseudo-périodique/apériodique, oscillations libres, entretien des oscillations) » ; annexe 2, TP « Oscillations libres dans un circuit RLC série » ; OP-PC-2007 ; perimetre.json clé circuit_RLC ; nationaux PC 2016-2025 du dépôt (RLC dans 17 sessions sur 20).",
 "capacites": [
  {"id": "RLC1", "texte": "Décrire la décharge d'un condensateur chargé dans une bobine : oscillations électriques libres (u_C change de signe, échange entre condensateur et bobine) ; utiliser i = dq/dt = C·du_C/dt et trouver le signe de i ; donner u_b(0⁺) par la continuité de i dans la bobine."},
  {"id": "RLC2", "texte": "Reconnaître sur un oscillogramme les régimes périodique (R + r = 0), pseudo-périodique et apériodique (le régime critique étant la frontière, sans calcul) ; savoir que l'amortissement augmente avec la résistance totale et que la pseudo-période T est voisine de T₀ pour un faible amortissement (admis)."},
  {"id": "RLC3", "texte": "Établir l'équation différentielle vérifiée par q ou par u_C dans un circuit RLC série (additivité des tensions, u_b = L·di/dt + r·i, u_C = q/C, i = dq/dt), et dans le cas idéal LC."},
  {"id": "RLC4", "texte": "Vérifier que u_C = U_m·cos(2πt/T₀ + φ) (ou q = Q_m·cos(2πt/T₀ + φ)) est solution de l'équation du LC ; en déduire T₀ = 2π√(LC) (pulsation propre ω₀ = 2π/T₀) ; montrer que √(LC) est homogène à un temps ; déterminer U_m et φ avec les conditions initiales."},
  {"id": "RLC5", "texte": "Exploiter un oscillogramme : lire T ou T₀ (sur plusieurs périodes), U_m ; calculer L ou C avec T₀ = 2π√(LC) (π² = 10) ; prévoir l'influence de L et de C sur T₀ (et l'absence d'influence de la tension de charge)."},
  {"id": "RLC6", "texte": "Exprimer l'énergie totale E = ½·C·u_C² + ½·L·i² (= q²/(2C) + ½·L·i²), décrire l'échange d'énergie entre le condensateur et la bobine, et exploiter sa conservation dans le circuit LC idéal."},
  {"id": "RLC7", "texte": "Expliquer l'amortissement par l'effet Joule : montrer que dE/dt = −(R + r)·i², calculer l'énergie dissipée entre deux instants et identifier les courbes E_e(t), E_m(t), E(t)."},
  {"id": "RLC8", "texte": "Expliquer l'entretien des oscillations par un générateur délivrant u_G = k·i (fonctionnement interne admis) : établir l'équation, montrer que k = R + r compense l'énergie dissipée, et savoir que le circuit oscille alors à la période propre T₀."},
 ],
 "formules": [
  {"ecriture": "i = dq/dt = C·du_C/dt", "capacite": "RLC1", "dit": "i égale dé q sur dé t, égale C dé u C sur dé t", "phrase": "convention récepteur ; u_C diminue → i < 0", "variantes_admises": ["q = C·u_C"]},
  {"ecriture": "u_b(0⁺) = −u_C(0)", "capacite": "RLC1", "dit": "u b juste après la bascule égale moins u C à l'instant initial", "phrase": "i(0⁺) = 0 (continuité dans la bobine) donc u_R(0⁺) = 0 (2024 R)"},
  {"ecriture": "u_C + u_R + u_b = 0", "capacite": "RLC3", "dit": "u C plus u R plus u b égale zéro", "phrase": "loi d'additivité après la bascule : pas de générateur dans la maille"},
  {"ecriture": "u_b = L·di/dt + r·i", "capacite": "RLC3", "dit": "u b égale L dé i sur dé t plus r i", "phrase": "vue au RL ; les sujets écrivent aussi u_L", "variantes_admises": ["u_L = L·di/dt + r·i", "u_L = L·di/dt (bobine idéale)"]},
  {"ecriture": "L·d²q/dt² + (R + r)·dq/dt + q/C = 0", "capacite": "RLC3", "dit": "L dé deux q sur dé t deux plus R plus r fois dé q sur dé t plus q sur C égale zéro", "phrase": "équation différentielle en q",
   "variantes_admises": ["d²q/dt² + ((R + r)/L)·dq/dt + q/(LC) = 0", "L·d²q/dt² + r·dq/dt + q/C = 0 (bobine seule)", "L·d²q/dt² + R·dq/dt + q/C = 0 (bobine idéale)"]},
  {"ecriture": "LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0", "capacite": "RLC3", "dit": "L C dé deux u C sur dé t deux plus R plus r fois C dé u C sur dé t plus u C égale zéro", "phrase": "équation différentielle en u_C",
   "variantes_admises": ["d²u_C/dt² + ((R + r)/L)·du_C/dt + u_C/(LC) = 0", "L·C·d²u_C/dt² + r·C·du_C/dt + u_C = 0"]},
  {"ecriture": "d²u_C/dt² + u_C/(LC) = 0", "capacite": "RLC3", "dit": "dé deux u C sur dé t deux plus u C sur L C égale zéro", "phrase": "circuit LC idéal (R + r = 0)", "variantes_admises": ["d²q/dt² + q/(LC) = 0", "d²u_C/dt² + (1/(LC))·u_C = 0"]},
  {"ecriture": "u_C(t) = U_m·cos(2πt/T₀ + φ)", "capacite": "RLC4", "dit": "u C de t égale U m cosinus de deux pi t sur T zéro plus phi", "phrase": "solution du LC ; U_m amplitude, φ phase à l'origine",
   "variantes_admises": ["q(t) = Q_m·cos(2πt/T₀ + φ)", "u_C(t) = U₀·cos(2πt/T₀)", "q(t) = Q_m·cos(2πt/T₀)", "i(t) = I_m·cos(2πt/T₀ + φ)"]},
  {"ecriture": "T₀ = 2π√(LC)", "capacite": "RLC4", "dit": "T zéro égale deux pi racine de L C", "phrase": "période propre, en seconde ; L en henry, C en farad", "variantes_admises": ["N₀ = 1/(2π√(LC))"]},
  {"ecriture": "ω₀ = 2π/T₀ = 1/√(LC)", "capacite": "RLC4", "dit": "oméga zéro égale deux pi sur T zéro, égale un sur racine de L C", "phrase": "pulsation propre ; jamais écrite dans les sujets (ils écrivent 2π/T₀)"},
  {"ecriture": "[L]·[C] = [T]²", "capacite": "RLC4", "dit": "la dimension de L fois C est un temps au carré", "phrase": "donc √(LC) s'exprime en secondes"},
  {"ecriture": "u_C(0) = U_m·cos φ", "capacite": "RLC4", "dit": "u C à l'instant zéro égale U m cosinus phi", "phrase": "avec le signe de du_C/dt(0) = −(2π/T₀)·U_m·sin φ pour choisir φ"},
  {"ecriture": "T ≈ T₀", "capacite": "RLC2", "dit": "la pseudo-période T est voisine de T zéro", "phrase": "admis pour un faible amortissement ; « en assimilant la pseudo-période à la période propre »"},
  {"ecriture": "L = T₀²/(4π²·C)", "capacite": "RLC5", "dit": "L égale T zéro au carré sur quatre pi carré C", "phrase": "élever au carré d'abord ; π² = 10", "variantes_admises": ["C = T₀²/(4π²·L)"]},
  {"ecriture": "E = ½·C·u_C² + ½·L·i²", "capacite": "RLC6", "dit": "E égale un demi C u C au carré plus un demi L i au carré", "phrase": "énergie totale, en joule ; E_e du condensateur, E_m (magnétique) de la bobine",
   "variantes_admises": ["E_t = q²/(2C) + ½·L·i²", "E_T = E_e + E_m"]},
  {"ecriture": "E = ½·C·E² = ½·L·I_m²", "capacite": "RLC6", "dit": "dans le circuit L C, l'énergie vaut un demi C E au carré, égale un demi L I m au carré", "phrase": "conservation (R + r = 0)", "variantes_admises": ["I_m = U_m·√(C/L)", "E_m = E − ½·C·u_C²"]},
  {"ecriture": "dE/dt = −(R + r)·i²", "capacite": "RLC7", "dit": "dé E sur dé t égale moins R plus r fois i au carré", "phrase": "l'énergie diminue par effet Joule", "variantes_admises": ["dE_T/dt = −r·i² (bobine seule)"]},
  {"ecriture": "|ΔE| = ½·C·(U₁² − U₂²)", "capacite": "RLC7", "dit": "énergie dissipée égale un demi C fois u C au début au carré moins u C à la fin au carré", "phrase": "entre deux sommets de u_C (i = 0)", "variantes_admises": ["|ΔE| = (q₁² − q₂²)/(2C)", "E_th = E_t(début) − E_t(fin)"]},
  {"ecriture": "u_G = k·i", "capacite": "RLC8", "dit": "u G égale k i", "phrase": "générateur d'entretien : tension proportionnelle à l'intensité"},
  {"ecriture": "L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0", "capacite": "RLC8", "dit": "L dé deux q sur dé t deux plus R plus r moins k fois dé q sur dé t plus q sur C égale zéro", "phrase": "équation avec le générateur d'entretien"},
  {"ecriture": "k = R + r", "capacite": "RLC8", "dit": "k égale R plus r", "phrase": "oscillations sinusoïdales de période T₀", "variantes_admises": ["k₀ = R + r", "k = r (bobine seule)"]},
 ],
 "mots_cles": ["circuit RLC série", "circuit LC", "oscillations électriques libres", "décharge", "période propre", "pulsation propre", "pseudo-période", "amortissement",
               "régime périodique", "régime pseudo-périodique", "régime apériodique", "régime critique", "équation différentielle", "amplitude", "phase à l'origine",
               "conditions initiales", "énergie électrique", "énergie magnétique", "énergie totale", "effet Joule", "entretien des oscillations", "oscillations entretenues"],
 "hors_cadre": {"mots": ["facteur de qualité", "bande passante", "résonance", "oscillations forcées", "régime forcé", "impédance", "réactance", "équation caractéristique",
                         "discriminant", "racines complexes", "pulsation complexe", "décrément logarithmique", "coefficient d'amortissement", "enveloppe exponentielle",
                         "résistance critique", "oscillateur harmonique", "déphasage", "analogie électromécanique", "circuit bouchon", "filtre passe-bande"],
                "motifs": [x["motif"] for x in A.a_ne_pas_dire]},
 "valeurs_reference": ["L = 0,1 H et C = 10 µF → T₀ ≈ 6,3 ms ; C = 4 µF, L = 0,1 H, π² = 10 → T₀ = 4 ms", "C de 0,22 nF à 250 µF (souvent 2,5 à 100 µF) ; L de 2 mH à 1 H ; T₀ de 0,28 ms à 0,10 s",
                       "énergies du nJ au mJ", "π² = 10 dans au moins 9 sessions"],
}

data = {
 "cle": "circuit_RLC", "matiere": "physique-chimie", "filiere": "2e Bac Sciences Physiques BIOF (Maroc)", "titre": "Oscillations libres d'un circuit RLC série", "date_exploration": "2026-11-12",
 "_note": ("Exploration du 12 novembre 2026 (routine cloud, skill exploration-de-cours ; le cours phys_ch8_circuit_RLC n'est pas construit ; préfixe des diapositives lc_). "
           "VIDÉOS NON AUDITÉES : YouTube bloqué depuis le cloud ; aucune vidéo de professeur lue. "
           "L'exploration s'appuie sur les 20 nationaux PC 2016-2025 du dépôt (RLC dans 17 sessions, analyse détaillée : outils/cours/notes/cours/circuit_RLC_build/nationaux.md), "
           "sur perimetre.json (circuit_RLC), sur la grille officielle citée dans les corrigés 2023 R / 2024 N, et sur les explorations dipole_RC et dipole_RL (même méthode, même tableau). "
           "À compléter par l'audit de dix vidéos depuis le PC Windows avant validation."),
 "sources": {"videos": [], "videos_note": "aucune : YouTube inaccessible depuis le conteneur cloud (12/11/2026)",
             "examens": [f"backend/data/exams/physique/{s[:4]}-{'normale' if s[-1] == 'N' else 'rattrapage'}" for s in NAT],
             "autres": ["backend/data/curriculum/perimetre.json (circuit_RLC)", "backend/data/curriculum/exploration/dipole_RC.json", "backend/data/curriculum/exploration/dipole_RL.json",
                        "database/seed_data/lessons/phys_ch8_l1.json"]},
 "comparaison": {"_note": "sans vidéos : comparaison faite entre les corrigés des 17 sessions RLC (notations, formes de l'équation, méthodes)",
                 "convergences": ["R + r écrit tel quel dans le terme en dq/dt", "équation d'abord en q ou en u_C, puis divisée par L ou LC", "T₀ = 2π√(LC) toujours, jamais ω₀ ; π² = 10",
                                  "énergie ½·C·u_C² + ½·L·i² (ou q²/(2C)) ; énergie perdue entre deux sommets", "entretien : u_G = k·i et k = résistance totale"],
                 "variantes_admises": [{"variante": "q ou u_C", "decision": "les deux équations sont faites (e3, e4) ; la solution est travaillée en u_C, avec renvoi à q = Q_m·cos"},
                                       {"variante": "U_m, U₀ ; Q_m ; I_m", "decision": "le cours écrit U_m et annonce que les sujets écrivent aussi U₀"},
                                       {"variante": "u_b, u_L", "decision": "le cours écrit u_b (comme au RL) et annonce u_L"},
                                       {"variante": "E_t, E_T ; E_th, E_j, ΔE", "decision": "le cours écrit E (énergie totale) et cite les autres lettres dans les exercices"},
                                       {"variante": "k, k₀ ; « résistance négative » (programme) jamais dans les sujets", "decision": "le cours écrit u_G = k·i (à valider)"}],
                 "meilleures_explications": ["la même recette que le RC et le RL (additivité, remplacer, ranger), avec une dérivée de plus", "u_C = 0 quand i est maximal : la bobine garde le courant",
                                             "énergie aux sommets : i = 0, un seul terme"]},
 "cadre": cadre,
 "insistances": ["toute équation part de la loi d'additivité sans générateur : … = 0", "r ne s'oublie jamais : (R + r) devant dq/dt",
                 "T₀ = 2π√(LC) ; pour L ou C, élever au carré d'abord", "T se lit entre deux sommets, sur plusieurs périodes si possible",
                 "énergie à un sommet de u_C : i = 0 ; énergie perdue = E(début) − E(fin)", "i = C·du_C/dt : son signe suit la pente de u_C",
                 "entretien : k = R + r, le circuit oscille à T₀"],
 "valeurs_reperes": ["2016 N : C = 10 µF, q = 120 → 40 µC → énergie perdue 6,4·10⁻⁴ J ; k = 11 → r_b = 11 Ω",
                     "2019 N : E = 10 V, C = 10 µF, T₀ = 20 ms → L = 1 H ; E = 5·10⁻⁴ J ; E_m(12 ms) = 1,8·10⁻⁴ J",
                     "2020 N : L = 1 H, R + r = 100 Ω, T = 10 ms → C = 2,5 µF ; k₀ = 100 Ω ; I_m = 8 mA, φ = +π/2 ; E_t = 3,2·10⁻⁵ J ; E_e(16 ms) ≈ 2,05·10⁻⁵ J",
                     "2021 R : L = 0,51 H, C = 100 µF → T₀ = 44,9 ms (T lue 45 ms) ; 1,80 → 1,26 mJ, E_th = 0,54 mJ",
                     "2022 N : C = 50 µF, T₀ = 10 ms → L = 0,05 H", "2023 N : L = 1 H, T₀ = 2 ms → C = 0,1 µF",
                     "2025 N : C₀ = 1 µF, U₀ = 10 V, T = 2,8·10⁻⁴ s ; |E_th| = 2,55·10⁻⁵ J", "2025 R : L = 0,1 H, C = 1 µF, E = 10 V → N₀ ≈ 503 Hz, I_m ≈ 31,6 mA"],
 "cas_types": cas_types, "pieges": pieges, "erreurs_examen": erreurs_examen,
 "conseils": ["le RLC tombe dans 17 sessions sur 20 (2,1 points en moyenne), presque toujours en 2e partie de l'exercice d'électricité après un RC ou un RL : C ou L vient de la 1re partie",
              "trois questions sûres : lire T et trouver L ou C, une équation différentielle, un calcul d'énergie", "convertir µF, nF, mH, ms, µC avant tout calcul ; π² = 10",
              "pour l'énergie, choisir des instants où i = 0 (sommets de u_C)", "la formule T₀ = 2π√(LC) resservira dans la modulation d'amplitude (circuit d'accord)"],
 "analogies_validees": analogies_validees, "a_ne_pas_dire": A.a_ne_pas_dire, "exclus_hors_programme": exclus_hors_programme,
 "questions_eleves": questions_eleves, "commentaires_eleves": commentaires_eleves, "notions_complexes": notions_complexes,
 "visuels": visuels, "regles_des_simulations": regles_des_simulations,
 "redaction_nationale": {"_note": "lignes attendues d'après les corrigés du dépôt et les grilles officielles citées (des erreurs du dépôt sont relevées dans limites et nationaux.md § 6)",
     "etablir_ED": ["u_C + u_R + u_b = 0", "u_R = R·i ; u_b = L·di/dt + r·i ; i = dq/dt = C·du_C/dt", "di/dt = d²q/dt² = C·d²u_C/dt²", "LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0 (ou L·d²q/dt² + (R + r)·dq/dt + q/C = 0)"],
     "trouver_T0": ["dq/dt = −(2π/T₀)·Q_m·sin(2πt/T₀)", "d²q/dt² = −(2π/T₀)²·q", "[1/(LC) − (2π/T₀)²]·q = 0 pour tout t", "T₀ = 2π√(LC)"],
     "trouver_L_ou_C": ["T lue entre deux maxima : T = … s", "T ≈ T₀ = 2π√(LC)", "L = T₀²/(4π²·C) = … H (π² = 10)"],
     "energie_instant": ["E = ½·C·u_C² + ½·L·i²", "à cet instant u_C = … et i = … (i = 0 si u_C est extrême)", "E = … J"],
     "energie_perdue": ["à t₁ et t₂, sommets : i = 0", "E(t₁) = ½·C·u_C(t₁)² ; E(t₂) = ½·C·u_C(t₂)²", "|ΔE| = E(t₁) − E(t₂) = … J, dissipée par effet Joule"],
     "dE_dt": ["dE/dt = C·u_C·du_C/dt + L·i·di/dt = i·(u_C + L·di/dt)", "équation : u_C + L·di/dt = −(R + r)·i", "dE/dt = −(R + r)·i² < 0"],
     "entretien": ["u_C + u_R + u_b = u_G = k·i", "L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0", "oscillations sinusoïdales : R + r − k = 0", "k = R + r = … Ω"],
     "phase": ["I_m et T₀ lus", "i(0) = I_m·cos φ → cos φ = …", "sens de départ → signe de sin φ", "φ = … rad"]},
 "plan": {"principes": "une idée nouvelle par diapositive ; une chose vue, une phrase, une question ; même tableau et même boîte des relations que le RC et le RL ; on part du RC et du RL (même recette : additivité, équation, solution) ; chaque bloc a au moins une prédiction et presque tous finissent sur une question de national ; deux nationaux traités en entier à la fin",
          "duree_estimee_min": 200,
          "decoupage_conseille": "quatre séances de trois blocs de quatre diapositives (bilan et carte dans le dernier bloc)",
          "prefixe_diapositives": "lc_",
          "prerequis_verifies_au_debut": ["courant_charge_q_it", "lois_kirchhoff", "derivee_sinus_cosinus"],
          "nationaux_en_entier": {"n1": "2020 N (Ex IV parties II-III, 3,5 pts : régime, équation en u_C, C, entretien k₀, I_m T₀ φ, énergies)",
                                  "n2": "2025 N (Ex 3 partie 2, 2,5 pts : équation en u_C, pseudo-période sur 4 carreaux, signe de i, dE_T/dt = −r·i², énergie dissipée)"},
          "seances": B.seances, "competences": B.competences, "diapositives": B.diapositives},
 "cours_existant": _sujets(copy.deepcopy(A.cours_existant)),
 "renvois": {"au_chapitre_dipole_RC": "q = C·u_C, i = dq/dt, E_e = ½·C·u_C², décharge dans R (rappel d1) ; même recette (o2, e1)",
             "au_chapitre_dipole_RL": "u_b = L·di/dt + r·i, continuité de i (d3, d6 : u_b(0⁺) reprend la rupture t4 du RL), E_m = ½·L·i² (en1)",
             "au_chapitre_modulation": "T₀ = 2π√(LC) (N₀ = 1/(2π√(LC))) resservira pour le circuit d'accord (six sessions)",
             "au_chapitre_oscillateur_mecanique": "rapprochement qualitatif avec le ressort et le pendule (semestre 2), sans tableau d'analogie"},
 "decisions_utilisateur": [
  {"question": "Entretien : écrire u_G = k·i (comme les sujets) au lieu de u = R₀·i (partie A) ?", "constat": "les 4 sujets d'entretien écrivent u_G = k·i (k₀ en 2020 N) ; « résistance négative » est dans perimetre.json mais jamais dans les sujets", "proposition": "u_G = k·i partout (k1-k3, n1) ; « résistance négative » non dit"},
  {"question": "Garde-t-on l'homogénéité de √(LC) ?", "constat": "jamais demandée au national ; « démonstration attendue » dans perimetre.json", "proposition": "oui, une diapositive (p1)"},
  {"question": "Régime critique ?", "constat": "jamais demandé ; perimetre.json : frontière, sans formule", "proposition": "une phrase dans r2, aucune valeur de R calculée"},
  {"question": "ω₀ ?", "constat": "jamais écrit dans les sujets (toujours 2π/T₀)", "proposition": "une ligne en e8, T₀ = 2π√(LC) d'abord"},
  {"question": "φ par les conditions initiales : quatre diapositives (c1-c4) ?", "constat": "une seule fois au national (2020 N, sur i) ; au programme (perimetre.json)", "proposition": "oui, quatre diapositives, reprises dans n1"},
  {"question": "Quels nationaux en entier ?", "constat": "2023 R est riche mais son corrigé du dépôt lit q ×10 trop petit ; 2020 N (3,5 pts) et 2025 N (2,5 pts) couvrent régime, équation, C, entretien, phase, énergie, signe de i, dE/dt", "proposition": "2020 N (n1) et 2025 N (n2)"},
  {"question": "Code couleur des courbes", "constat": "rouge = condensateur au RC, vert = bobine au RL", "proposition": "rouge = condensateur (u_C, q, E_e), vert = bobine (i, E_m), blanc = énergie totale, jaune réservé au surlignage"},
  {"question": "Image oscillations_lab.webp pour l'analogie balançoire / ressort ?", "constat": "matériel du chapitre oscillateur mécanique", "proposition": "pas dans le plan ; analogie dite à l'oral (d4) avec v_analogie à valider"},
  {"question": "Capacités RLC1-RLC8", "constat": "partie A citait RLC1-RLC7 provisoires (autre découpage)", "proposition": "RLC1-RLC8 de la fiche (régimes et dissipation séparés, signe de i et u_b(0⁺) dans RLC1)"},
 ],
 "limites_de_l_exploration": ["VIDÉOS NON AUDITÉES : aucun des dix professeurs (YouTube bloqué depuis le cloud) ; à faire depuis le PC avant validation",
     "commentaires d'élèves non lus : difficultés anticipées d'après le RC, le RL et les nationaux",
     "erreurs du dépôt relevées (nationaux.md § 6) : 2023 R 1.3 et 2.3 (q lu 12 et 8 µC au lieu de 120 et 40 µC, E = 1,2 V au lieu de 12 V ; « pseudo-périodique non amorti ») ; 2024 R 2.3 (axe de u_R en mV lu en V ; u_C(t₁) ≈ −1,5 V) et 2.1.2 (« si on néglige r ») ; 2024 N 1.4 (u_C(t₂) lu 4 V au lieu de −4,4 V → 1,83·10⁻⁹ J) et 1.2 (r mis dans u_R) ; 2021 R III.1-III.2 (courbes (a)/(b) inversées) ; 2019 N barème faux dans exam.json (RLC 2,5 pts et non 3)",
     "figures mal liées dans exam.json : 2022 N (fig3p6.png, fig4p6.png), 2022 R, 2023 R (fig1p4, fig2p4, fig3p5), 2024 N (fig1p4, fig2p4) ; données absentes d'exam.json : 2024 N C = 0,22 nF, 2022 R L = 1 H, 2020 N R = 90 Ω, 2025 N I₀ = 1 µA",
     "le dépôt écrit « fréquence de résonance » pour le circuit d'accord (2018 R, 2023 R) : mot hors cadre ici",
     "capacités RLC1-RLC8 provisoires (texte officiel non relu mot à mot)",
     "aucune simulation RLC existante réutilisable : toutes à créer (circuit-rlc-tableau)"],
}

def verification(d):
    caps = {c["id"]: [] for c in cadre["capacites"]}
    comp2cap = {c["id"]: c["cadre_ids"] for c in B.competences}
    for s in B.diapositives:
        for c in s["competences"]:
            for k in comp2cap[c]:
                caps[k].append(s["id"])
    motifs = [re.compile(m) for m in cadre["hors_cadre"]["motifs"]]
    mots = [m.lower() for m in cadre["hors_cadre"]["mots"]]
    hors = []
    for s in B.diapositives:
        t = json.dumps(s, ensure_ascii=False).lower()
        if any(m.search(t) for m in motifs) or any(m in t for m in mots):
            hors.append(s["id"])
    blocs = [b for se in B.seances for b in se["blocs"]]
    ids = [x["id"] for x in B.diapositives]
    pred = {x["id"] for x in B.diapositives if x["prediction"]}
    return {"dix_professeurs": "non : aucune vidéo (YouTube bloqué depuis le cloud) ; remplacés par les 17 sessions RLC des nationaux",
            "capacites_du_cadre_dans_le_plan": caps,
            "toutes_les_capacites": all(caps.values()),
            "diapositives": len(B.diapositives), "predictions": len(pred),
            "prediction_dans_chaque_bloc": all(any(x in pred for x in b) for b in blocs),
            "seances_couvrent_le_plan": [x for b in blocs for x in b] == ids,
            "rappels": sum(len(c["rappels"]) for c in B.competences),
            "calculs_verifies_en_python": len(B.verifier_calculs()),
            "diapositives_avec_mot_hors_cadre": hors}
data["verification"] = verification(data)

if __name__ == "__main__":
    out = Path("backend/data/curriculum/exploration/circuit_RLC.json")
    out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    v = data["verification"]
    print(out, out.stat().st_size, "octets ;", v["diapositives"], "diapositives,", v["predictions"], "prédictions,", v["rappels"], "rappels,",
          v["calculs_verifies_en_python"], "calculs ; capacités toutes couvertes :", v["toutes_les_capacites"],
          "; prédiction par bloc :", v["prediction_dans_chaque_bloc"], "; hors cadre dans le plan :", v["diapositives_avec_mot_hors_cadre"])
