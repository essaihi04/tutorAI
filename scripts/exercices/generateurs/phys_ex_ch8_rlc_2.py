# Exercice de physique, ch. 8 (oscillations libres d'un circuit RLC série), niveau facile n° 2 :
# lire un oscillogramme : reconnaître le régime, mesurer la pseudo-période sur plusieurs sommets, en déduire L.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture backend/data/curriculum/architecture/phys_ch8_circuit_RLC.md
#    (« lire la période, puis trouver L ou C » : 13 sessions sur 20 ; « reconnaître le régime » 2020 R, 2021 R),
#    docs/parties_voix/phys_ch8_circuit_RLC.json, fiche du cadre circuit_RLC (RLC2, RLC5).
#  - cours phys_ch8_circuit_RLC : lc_r1_pseudo, lc_r3_ordre (régimes), lc_r5_observer, lc_l1_mesure (« trois périodes, pas
#    quatre »), lc_l3_carre (le carré d'abord).
#  - nationaux : 2016 N, 2019 R, 2020 N, 2022 R (« quel est le régime ? », « la pseudo-période est voisine de T₀ :
#    déterminer L / C », π² = 10).
#  - séries en ligne : recherche faite (talamidi, moutamadris, Naceiri, dreamjob) mais PDF non joignables depuis cette session ;
#    nos données suivent la simulation observer.html réglée sur L = 0,225 H et C = 4 µF (T ≈ 6 ms).
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch8_rlc_2"
SIMD = "/media/simulations/physics/circuit-rlc-tableau/"


def u_amortie(E, L, C, Rt):
    """Solution exacte de L·q'' + Rt·q' + q/C = 0, u_C(0) = E, i(0) = 0, t en ms (même calcul que energie.html)."""
    lam = Rt / (2 * L); w = math.sqrt(1 / (L * C) - lam ** 2)
    expr = f"{E}*exp(-{lam / 1000:.6g}*x)*(cos({w / 1000:.6g}*x)+{lam / w:.6g}*sin({w / 1000:.6g}*x))"
    return expr, 2 * math.pi / w * 1000, lam


def grille(tmax, dt, ymin, ymax, dy):
    els, k = [], 0
    while k * dt <= tmax + 1e-9:
        els.append({"f": "ligne", "pts": [[round(k * dt, 4), ymin], [round(k * dt, 4), ymax]], "couleur": "faible"}); k += 1
    k = 0
    while ymin + k * dy <= ymax + 1e-9:
        y = round(ymin + k * dy, 4); els.append({"f": "ligne", "pts": [[0, y], [tmax, y]], "couleur": "faible"}); k += 1
    return els


def oscillogramme(titre, E, L, C, Rt, tmax, umax, dt=2, du=2, legende=None):
    expr, T, lam = u_amortie(E, L, C, Rt)
    els = grille(tmax, dt, -umax, umax, du) + [{"f": "courbe", "expr": expr, "de": 0, "a": tmax, "couleur": "rouge"}]
    return figure_courbe(titre, axe("t", 0, tmax, "ms", list(range(0, tmax + 1, dt))),
                         axe("u_C", -umax, umax, "V", list(range(-umax, umax + 1, du))), els, legende=legende), T, lam


# ---------------------------------------------------------------- données et calculs (π² = 10)
E, C, RT = 6, 4e-6, 20
L_VRAI = 0.225                                  # inductance de la bobine (sert à tracer la courbe)
FIG, T_EXACT, LAM = oscillogramme("Figure 1 : u_C(t) après la bascule de K", E, L_VRAI, C, RT, 20, 8,
                                  legende="Oscilloscope : 2 ms par division, 2 V par division.")
T3 = 18                                         # lu : du sommet t = 0 au quatrième sommet
T = T3 / 3                                       # 6 ms
L = (T * 1e-3) ** 2 / (40 * C)
assert abs(3 * T_EXACT - 18) < 0.3 and abs(T - 6) < 1e-12 and abs(L - 0.225) < 1e-12
# semblable : C = 10 µF, L = 0,04 H, R + r = 8 Ω, E = 8 V, 3T = 12 ms
FIGB, TB_EXACT, _ = oscillogramme("Figure 1 : u_C(t) après la bascule de K", 8, 0.04, 10e-6, 8, 16, 10,
                                  legende="Oscilloscope : 2 ms par division, 2 V par division.")
LB = (4e-3) ** 2 / (40 * 10e-6)
assert abs(3 * TB_EXACT - 12) < 0.2 and abs(LB - 0.04) < 1e-12

REG = ("Régime pseudo-périodique : u_C oscille (elle change de signe) et l'amplitude (la hauteur des sommets) diminue "
       "au cours du temps ; l'énergie est perdue par effet Joule dans la résistance totale R + r du circuit.")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "circuit_RLC", "cours": "phys_ch8_circuit_RLC",
  "titre": "Lire un oscillogramme : régime, pseudo-période, inductance", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Reconnaître le régime pseudo-périodique", "Mesurer la pseudo-période T sur plusieurs sommets", "Calculer L avec T ≈ T₀ = 2π√(LC) (π² = 10)"],
  "enonce": {
    "intro": "Un condensateur de capacité C, chargé sous la tension E = 6 V, est relié à t = 0 à une bobine (L, r) en série avec un conducteur ohmique R (résistance totale R + r = 20 Ω). Un oscilloscope visualise la tension u_C(t) aux bornes du condensateur (figure 1). On admet que la pseudo-période T est égale à la période propre T₀ = 2π√(LC).",
    "intro_dit": "دابا نقراو l'énoncé. un condensateur، la capacité ديالو C، مشارجي تحت E égale six volts. فt égale zéro، كنربطوه مع la bobine L r، ومع un conducteur ohmique R، وla résistance totale R plus r égale vingt ohms. l'oscilloscope كيورينا la tension u C ديال le condensateur، فla figure un. وكنقبلو بلي la pseudo-période T هي la période propre T zéro égale deux pi racine de L C.",
    "figures": [FIG],
    "donnees": ["C = 4 µF = 4·10⁻⁶ F", "R + r = 20 Ω", "Sensibilités : 2 ms/div ; 2 V/div", "On prend π² = 10."],
    "questions": [
      question("1", "Nommer le régime des oscillations observé sur la figure 1. Justifier.",
        "السؤال un: سمي le régime ديال les oscillations اللي كنشوفو فla figure un، وعلل.",
        phrase(REG),
        ["pseudo-périodique", "amplitude", "sommets", "effet Joule", "R + r"], ["périodique", "apériodique"],
        [aide("Regarde deux choses : u_C change-t-elle de signe ? Les sommets restent-ils à la même hauteur ?",
              "شوف حاجتين: واش u C كتبدل le signe؟ وواش les sommets كيبقاو بنفس العلو؟"),
         aide("Oscille + sommets égaux : périodique. Oscille + sommets qui baissent : pseudo-périodique. Ne change pas de signe : apériodique.",
              "كتمشي وتجي وles sommets بنفس العلو: périodique. كتمشي وتجي وles sommets كينقصو: pseudo-périodique. ما كتبدلش le signe: apériodique.")],
        corr([("1 : u_C change de signe : le circuit oscille.", "u C كتبدل le signe"),
              ("Les sommets diminuent (environ 6 V ; 4,6 V ; 3,5 V…) : l'amplitude décroît.", "les sommets كينقصو"),
              ("Le régime est pseudo-périodique (amortissement par effet Joule dans R + r).", "le régime pseudo-périodique")],
             "السؤال un. u C كتبدل le signe، إذن الدارة كتمشي وتجي. ولكن les sommets كينقصو: six volts، من بعد environ quatre virgule six، من بعد trois virgule cinq. إذن هادا le régime pseudo-périodique. l'énergie كتضيع بl'effet Joule فla résistance totale R plus r."),
        "ex_lc2_1", "fa_lc2_1"),
      question("2", "Déterminer la pseudo-période T (en ms), en la mesurant sur plusieurs pseudo-périodes.",
        "السؤال deux: حدد la pseudo-période T بles millisecondes، وقيسها على بزاف ديال les pseudo-périodes.",
        valeur("T", 6, "ms", "Du 1er sommet (t = 0) au 4e sommet : 3T = 9 div × 2 ms = 18 ms, donc T = 18/3 = 6 ms"),
        ["3T", "div", "2 ms/div", "ms"], ["4T = 18 ms", "T = 18 ms", "T/2"],
        [aide("Prends le sommet à t = 0 et le quatrième sommet. Compte les divisions entre eux, puis multiplie par 2 ms.",
              "خود le sommet اللي فt égale zéro، وle quatrième sommet. حسب les divisions اللي بيناتهم، ومن بعد ضرب fois deux millisecondes."),
         aide("Entre le 1er et le 4e sommet, il y a 3 pseudo-périodes (compte les intervalles, pas les sommets) : 3T = durée lue.",
              "بين le premier sommet وle quatrième، كاينين trois pseudo-périodes، ماشي quatre: حسب المسافات، ماشي les sommets. إذن trois T égale la durée اللي قريتي.")],
        corr([("2 : du 1er au 4e sommet : 9 divisions × 2 ms = 18 ms", "neuf divisions fois deux millisecondes"),
              ("Ces 18 ms contiennent 3 pseudo-périodes : 3T = 18 ms", "trois T égale dix-huit millisecondes"),
              ("T = 18/3 = 6 ms", "T égale six millisecondes")],
             "السؤال deux. من le premier sommet حتى le quatrième، كاينين neuf divisions fois deux millisecondes، يعني dix-huit millisecondes. بيناتهم trois pseudo-périodes، إذن trois T égale dix-huit millisecondes. إذن T égale six millisecondes."),
        "ex_lc2_2", "fa_lc2_2"),
      question("3", "En admettant T = T₀, calculer l'inductance L de la bobine.",
        "السؤال trois: إلى قبلنا بلي T égale T zéro، حسب l'inductance L ديال la bobine.",
        valeur("L", 0.225, "H", "L = T₀²/(4π²·C) = (6·10⁻³)²/(40 × 4·10⁻⁶) = 3,6·10⁻⁵/1,6·10⁻⁴ = 0,225 H"),
        ["T₀ = 2π√(LC)", "T₀² = 4π²·L·C", "π² = 10", "10⁻³", "10⁻⁶", "H"], ["L = T₀/(2πC)", "T₀ = 6 s", "L = 4π²C/T₀²"],
        [aide("La racine gêne : commence par mettre T₀ = 2π√(LC) au carré. Écris aussi T₀ en secondes : 6 ms = 6·10⁻³ s.",
              "la racine كتصعب: بدا بطلع T zéro égale deux pi racine de L C au carré. وكتب T zéro بla seconde: six millisecondes، يعني six fois dix puissance moins trois seconde."),
         aide("T₀² = 4π²·L·C, donc L = T₀²/(4π²·C), avec 4π² = 40.",
              "T zéro au carré égale quatre pi carré fois L fois C. إذن L égale T zéro au carré، sur quatre pi carré fois C، et quatre pi carré égale quarante.")],
        corr([("3 : T₀ = 2π√(LC) ⇒ T₀² = 4π²·L·C ⇒ L = T₀²/(4π²·C)", "L égale T zéro au carré، sur quatre pi carré fois C"),
              ("A.N. : L = (6·10⁻³)²/(40 × 4·10⁻⁶)", "six fois dix puissance moins trois، au carré"),
              ("L = 0,225 H", "L égale zéro virgule deux cent vingt-cinq henry")],
             "السؤال trois. T zéro au carré égale quatre pi carré fois L fois C، إذن L égale T zéro au carré، sur quatre pi carré fois C. l'application numérique: six fois dix puissance moins trois، au carré، sur quarante fois quatre fois dix puissance moins six. يعني trois virgule six fois dix puissance moins cinq، sur un virgule six fois dix puissance moins quatre. L égale zéro virgule deux cent vingt-cinq henry."),
        "ex_lc2_3", "fa_lc2_3"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_lc2_1", "Question 1 : reconnaître le régime", "Oscille et sommets qui baissent : pseudo-périodique.",
      SIMD + "regimes.html", "Trois traces de u_C : R + r = 20 Ω, 1000 Ω, 0 Ω",
      "شوف l'écran. الأول، R plus r égale vingt ohms، بحال التمرين ديالك: u C كتبدل le signe، كتمشي وتجي، ولكن كل sommet أقصر من اللي قبل منو. هادا le régime pseudo-périodique. التاني، R plus r égale mille ohms: u C كترجع vers zéro بلا ما تبدل le signe. هادا le régime apériodique. التالت، R plus r égale zéro: les sommets كلهم بنفس العلو، هادا le régime périodique. فla figure ديالك، les sommets كينقصو: إذن pseudo-périodique، وl'énergie كتضيع بl'effet Joule.",
      centre=[("Oscille, sommets qui baissent → pseudo-périodique", "هادا le régime pseudo-périodique"),
              ("Pas de changement de signe → apériodique", "هادا le régime apériodique"),
              ("Sommets égaux (R + r = 0) → périodique", "هادا le régime périodique")],
      pointage=[{"mot": "الأول، R plus r égale vingt ohms", "commande": "play_until", "parametres": {"moment": "pseudo"}},
                {"mot": "كل sommet أقصر من اللي قبل منو", "repere": "courbe_pseudo"},
                {"mot": "هادا le régime pseudo-périodique", "cible": "centre:0"},
                {"mot": "التاني، R plus r égale mille ohms", "commande": "play_until", "parametres": {"moment": "aperiodique"}},
                {"mot": "هادا le régime apériodique", "cible": "centre:1"},
                {"mot": "التالت، R plus r égale zéro", "commande": "play_until", "parametres": {"moment": "periodique"}},
                {"mot": "هادا le régime périodique", "cible": "centre:2"}]),
    diapo_sim("ex_lc2_2", "Question 2 : mesurer T sur trois pseudo-périodes", "3T = 18 ms, donc T = 6 ms.",
      SIMD + "observer.html", "La décharge avec L = 0,225 H et C = 4 µF : T ≈ 6 ms entre deux sommets",
      "دابا كنحطو les valeurs ديال التمرين: L égale zéro virgule deux cent vingt-cinq henry، وC égale quatre microfarads. شوف la courbe كتترسم: les sommets كيبانو مورا بعضهم. باش نقيسو T مزيان، ما كناخدوش deux sommets قراب. كناخدو le sommet ديال t égale zéro، وle quatrième sommet. رد البال: بيناتهم trois pseudo-périodes، ماشي quatre. كنقراو dix-huit millisecondes، إذن trois T égale dix-huit millisecondes. وT égale six millisecondes، هي اللي مكتوبة بين deux sommets.",
      centre=[("3T = 18 ms (du 1er au 4e sommet)", "إذن trois T égale dix-huit millisecondes"),
              ("T = 18/3 = 6 ms", "وT égale six millisecondes")],
      pointage=[{"mot": "دابا كنحطو les valeurs ديال التمرين", "commande": "set_parameters", "parametres": {"L_H": 0.225, "C_uF": 4}},
                {"mot": "شوف la courbe كتترسم", "repere": "courbe"},
                {"mot": "رد البال: بيناتهم trois pseudo-périodes", "repere": "courbe"},
                {"mot": "إذن trois T égale dix-huit millisecondes", "cible": "centre:0"},
                {"mot": "وT égale six millisecondes", "cible": "centre:1"},
                {"mot": "هي اللي مكتوبة بين deux sommets", "repere": "T"}]),
    diapo_sim("ex_lc2_3", "Question 3 : L, le carré d'abord", "L = T₀²/(4π²C) = (6·10⁻³)²/(40 × 4·10⁻⁶) = 0,225 H.",
      SIMD + "observer.html", "Les valeurs de L et de C sous le circuit : L = 0,225 H donne bien T ≈ 6 ms",
      "باش نلقاو L، كنبداو بla formule: T zéro égale deux pi racine de L C. la racine كتصعب، إذن كنطلعو الجوج جيهات au carré: T zéro au carré égale quatre pi carré fois L fois C. دابا نعزلو L: L égale T zéro au carré، sur quatre pi carré fois C. رد البال: T zéro بla seconde، six fois dix puissance moins trois، et quatre pi carré égale quarante. كنلقاو L égale zéro virgule deux cent vingt-cinq henry. شوف تحت le circuit: هادي هي la valeur ديال L اللي عطات هاد la courbe.",
      centre=[("T₀² = 4π²·L·C", "T zéro au carré égale quatre pi carré fois L fois C"),
              ("L = T₀²/(4π²·C)", "L égale T zéro au carré، sur quatre pi carré fois C"),
              ("L = (6·10⁻³)²/(40 × 4·10⁻⁶) = 0,225 H", "كنلقاو L égale zéro virgule deux cent vingt-cinq henry")],
      pointage=[{"mot": "باش نلقاو L", "commande": "set_parameters", "parametres": {"L_H": 0.225, "C_uF": 4}},
                {"mot": "T zéro au carré égale quatre pi carré fois L fois C", "cible": "centre:0"},
                {"mot": "L égale T zéro au carré، sur quatre pi carré fois C", "cible": "centre:1"},
                {"mot": "كنلقاو L égale zéro virgule deux cent vingt-cinq henry", "cible": "centre:2"},
                {"mot": "شوف تحت le circuit", "repere": "reglages"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    association_facile("fa_lc2_1", "Plus facile : à chaque courbe son régime", "سؤال ساهل: ربط كل وصف ديال la courbe مع le régime ديالو.",
      "Relie chaque description de u_C(t) au régime qui lui correspond.", "Relie chaque description (1, 2, 3) à un régime (a, b, c).",
      [("1", "u_C oscille, sommets tous à la même hauteur"), ("2", "u_C oscille, sommets de plus en plus bas"), ("3", "u_C revient vers 0 sans changer de signe")],
      [("a", "régime apériodique"), ("b", "régime périodique"), ("c", "régime pseudo-périodique")],
      {"1": "b", "2": "c", "3": "a"},
      {"1-a": (False, "Non : dans le régime apériodique, u_C ne change pas de signe. Ici elle oscille sans perdre de hauteur : cherche le régime sans amortissement.",
               "لا. فle régime apériodique، u C ما كتبدلش le signe. هنا كتمشي وتجي بلا ما تنقص: قلب على le régime بلا amortissement."),
       "1-b": (True, "Juste : des sommets égaux, c'est le régime périodique (R + r = 0, circuit LC idéal).",
               "صحيح: les sommets بنفس العلو، هادا le régime périodique، يعني R plus r égale zéro."),
       "1-c": (False, "Non : dans le pseudo-périodique, les sommets baissent. Ici ils restent égaux : aucune énergie n'est perdue.",
               "لا. فle pseudo-périodique، les sommets كينقصو. هنا بقاو بنفس العلو: ما ضاعت حتى énergie."),
       "2-a": (False, "Non : u_C oscille ici (elle change de signe), ce n'est pas apériodique. Les sommets baissent : quel régime ?",
               "لا. هنا u C كتبدل le signe، إذن ماشي apériodique. les sommets كينقصو: أشمن régime؟"),
       "2-b": (False, "Non : périodique veut dire sommets égaux. Ici l'amplitude diminue : il y a un amortissement.",
               "لا. périodique يعني les sommets بنفس العلو. هنا l'amplitude كتنقص: كاين amortissement."),
       "2-c": (True, "Juste : oscillations dont l'amplitude diminue : régime pseudo-périodique.",
               "صحيح: كتمشي وتجي وl'amplitude كتنقص، هادا le régime pseudo-périodique."),
       "3-a": (True, "Juste : pas d'oscillation, retour vers 0 : régime apériodique (grande résistance totale).",
               "صحيح: بلا oscillation، كترجع vers zéro: هادا le régime apériodique، مع résistance كبيرة."),
       "3-b": (False, "Non : dans le régime périodique, u_C oscille sans fin. Ici elle ne change même pas de signe.",
               "لا. فle régime périodique، u C كتمشي وتجي ديما. هنا حتى le signe ما كتبدلوش."),
       "3-c": (False, "Non : pseudo-périodique veut dire qu'u_C oscille encore. Ici elle ne change pas de signe.",
               "لا. pseudo-périodique يعني u C مازال كتمشي وتجي. هنا ما كتبدلش le signe.")},
      "(1 ; b) (2 ; c) (3 ; a). Plus R + r est grande, plus l'amortissement est fort.",
      "الجواب: un مع b، deux مع c، trois مع a. كلما كبرات R plus r، كلما كبر l'amortissement."),
    qcm_facile("fa_lc2_2", "Plus facile : trois périodes, pas quatre", "سؤال ساهل على la mesure ديال T.",
      "Du sommet à t = 0 au 4e sommet, on lit 18 ms. La pseudo-période vaut…",
      ["4,5 ms", "6 ms", "18 ms"], 1, {
        "1": {"juste": rep("برافو! بين le premier وle quatrième sommet كاينين trois T. dix-huit sur trois، six millisecondes.", "Juste : 3T = 18 ms, T = 6 ms.")},
        "0": {"1": rep("قريب. ولكن حسب المسافات بين les sommets، ماشي les sommets. شحال من مسافة بين le premier وle quatrième؟ عاود اختار.", "Compte les intervalles entre sommets, pas les sommets. Réessaie."),
              "2": rep("الجواب هو six millisecondes. من le premier حتى le quatrième sommet، trois pseudo-périodes، ماشي quatre.", "Réponse : 6 ms ; du 1er au 4e sommet il y a 3 pseudo-périodes, pas 4.")},
        "2": {"1": rep("لا. dix-huit millisecondes هي المدة ديال بزاف ديال les pseudo-périodes، ماشي وحدة. قسم. عاود اختار.", "18 ms couvre plusieurs pseudo-périodes : il faut diviser. Réessaie."),
              "2": rep("الجواب هو six millisecondes: dix-huit sur trois.", "Réponse : T = 18/3 = 6 ms.")}},
      "Du sommet à t égale zéro au quatrième sommet, on lit dix-huit millisecondes. La pseudo-période vaut ?"),
    qcm_facile("fa_lc2_3", "Plus facile : isoler L", "سؤال ساهل: عزل L من la formule.",
      "De T₀ = 2π√(LC), on tire :",
      ["L = 4π²C/T₀²", "L = T₀²/(4π²C)", "L = T₀/(2πC)"], 1, {
        "1": {"juste": rep("برافو! T zéro au carré égale quatre pi carré L C، إذن L égale T zéro au carré sur quatre pi carré C.", "Juste : T₀² = 4π²LC, donc L = T₀²/(4π²C).")},
        "0": {"1": rep("قلبتي la fraction. إلى كبرات T zéro، واش L خاصها تكبر ولا تصغر؟ عاود اختار.", "Fraction renversée : si T₀ augmente, L doit augmenter. Réessaie."),
              "2": rep("الجواب: L égale T zéro au carré، sur quatre pi carré C. T zéro خاصها تكون فوق.", "Réponse : L = T₀²/(4π²C) ; T₀ est au numérateur.")},
        "2": {"1": rep("نسيتي la racine. خاص تطلع الجيهتين au carré قبل ما تعزل L. عاود اختار.", "Il faut d'abord élever au carré pour faire disparaître la racine. Réessaie."),
              "2": rep("الجواب: L égale T zéro au carré، sur quatre pi carré C، حيت كنطلعو au carré بالأول.", "Réponse : L = T₀²/(4π²C) (on élève d'abord au carré).")}},
      "De T zéro égale deux pi racine de L C, on tire ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même expérience avec un autre condensateur : C = 10 µF, chargé sous E = 8 V, et une autre bobine. On obtient l'oscillogramme de la figure 1. On admet T = T₀.",
      "intro_dit": "نفس التمرين، بقيم أخرى. C égale dix microfarads، مشارجي تحت huit volts، مع bobine أخرى. هادا l'oscillogramme ديال la figure un. وكنقبلو T égale T zéro.",
      "figures": [FIGB],
      "donnees": ["C = 10 µF = 10⁻⁵ F", "Sensibilités : 2 ms/div ; 2 V/div", "π² = 10"],
      "questions": [
        question_semblable("1", "Nommer le régime des oscillations observé. Justifier.",
          phrase(REG), ["pseudo-périodique", "amplitude"], ["apériodique"],
          corr([("1 : u_C change de signe et ses sommets diminuent : régime pseudo-périodique.", "le régime pseudo-périodique")],
               "u C كتبدل le signe وles sommets كينقصو: هادا le régime pseudo-périodique.")),
        question_semblable("2", "Déterminer la pseudo-période T (en ms) sur plusieurs pseudo-périodes.",
          valeur("T", 4, "ms", "Du 1er au 4e sommet : 3T = 6 div × 2 ms = 12 ms, donc T = 12/3 = 4 ms"), ["3T", "ms"], ["4T = 12 ms"],
          corr([("2 : 3T = 6 × 2 = 12 ms", "trois T égale douze millisecondes"), ("T = 4 ms", "T égale quatre millisecondes")],
               "من le premier حتى le quatrième sommet، six divisions، يعني trois T égale douze millisecondes. إذن T égale quatre millisecondes.")),
        question_semblable("3", "En admettant T = T₀, calculer l'inductance L de la bobine.",
          valeur("L", 0.04, "H", "L = T₀²/(4π²·C) = (4·10⁻³)²/(40 × 10⁻⁵) = 0,04 H"), ["L = T₀²/(4π²C)", "H"], ["L = T₀/(2πC)"],
          corr([("3 : L = T₀²/(4π²·C) = (4·10⁻³)²/(40 × 10⁻⁵)", "L égale T zéro au carré، sur quatre pi carré fois C"), ("L = 0,04 H", "zéro virgule zéro quatre henry")],
               "L égale T zéro au carré، sur quatre pi carré fois C. يعني seize fois dix puissance moins six، sur quarante fois dix puissance moins cinq. L égale zéro virgule zéro quatre henry.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
