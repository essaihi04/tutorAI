# Exercice de physique, ch. 7 (dipôle RL), niveau moyen n° 4 : la rupture du courant (K bascule de 1 à 2),
# continuité de i, résistance r de la bobine, équation de la rupture, solution I₀·e^(−t/τ), τ et L.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RL.json : cas_types « rupture » (maille sans générateur,
#    second membre 0, i(0⁺) = I₀), « r » (r = E/I₀ − R), « tau » (tangente ∩ axe des temps à la rupture, 37 %), « L » ;
#    erreurs_examen « rupture : second membre E au lieu de 0 », « faire partir i de 0 à la rupture ».
#  - nationaux : 2017 N (2.1 à 2.3 : rupture, τ, r = 5 Ω, L par la courbe u_R) : même type de questions, notre
#    situation et nos données (E = 9 V, R = 80 Ω, L = 0,45 H, r = 10 Ω).
#  - cours phys_ch7_dipole_RL : rl_t1_rupture (circuit-rl.html?vue=rupture), rl_t2a_verifier (fig_ed_rupture),
#    rl_t2_descente (37 % et tangente), rl_l3_r (trouver r).
#  - séries en ligne : recherche web (talamidi, moutamadris, alloschool, série P7 N. Naceiri) ; pages non ouvertes
#    (domaines bloqués dans le conteneur), seuls les intitulés comparés (exercices « rupture du courant » avec
#    interrupteur à deux positions et courbe u_R(t) décroissante). Valeurs réglées dans la simulation circuit-rl.html.
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch7_rl_4"
SIMD = "/media/simulations/physics/dipole-rl-tableau/"
PAR = "&E=9&R_ohm=80&L_H=0.45"
SIM_RUP = SIMD + "circuit-rl.html?vue=rupture" + PAR
SIM_ETA = SIMD + "circuit-rl.html?vue=etablissement" + PAR
FIG_RUP = SIMD + "figures.html?fig=fig_ed_rupture"


def montage(titre):
    """K à deux positions : 1 → générateur dans la maille ; 2 → R et la bobine seuls."""
    return schema(titre, 8.4, 4.8,
        dipole([1, 0.8], [1, 3.6], "G", "E", pos="o"),
        fil([1, 3.6], [2.4, 3.6]),
        inverseur([3.4, 3.6], [2.4, 3.6], [2.4, 2.5], vers=1, t="K", pos_t=[3.0, 4.15]),
        fil([2.4, 2.5], [2.4, 0.8]),
        dipole([3.4, 3.6], [6.2, 3.6], "R", "R", pos="s"),
        fil([6.2, 3.6], [7.2, 3.6]),
        dipole([7.2, 3.6], [7.2, 0.8], "L", "(L, r)", pos="o"),
        fil([7.2, 0.8], [1, 0.8]),
        courant([6.7, 3.6], "d"),
        tension([5.8, 4.2], [3.8, 4.2], "u_R", couleur="orange"),
        tension([7.8, 1.2], [7.8, 3.2], "u_b", couleur="violet", pos="e"),
        legende="K en position 1 avant t = 0 ; à t = 0, K bascule en position 2.")


def courbe_rupture(U0, tau_ms, tmax, pas, titre):
    return figure_courbe(titre, axe("t", 0, tmax, "ms", list(range(0, tmax + 1, pas))),
        axe("u_R", 0, U0 * 1.25, "V", list(range(0, int(U0 * 1.25) + 1, 2))),
        [{"f": "courbe", "expr": f"{U0}*exp(-x/{tau_ms})", "couleur": "bleu", "texte": "u_R(t)", "texte_x": tmax * 0.45},
         {"f": "courbe", "expr": f"{U0}*(1-x/{tau_ms})", "de": 0, "a": tau_ms * 1.05, "couleur": "faible", "trait": "pointille"},
         {"f": "texte", "at": [tau_ms * 0.75, U0 * 0.62], "t": "(T)", "couleur": "faible"}],
        legende="u_R(t) après la bascule de K en position 2 à t = 0 ; (T) : tangente à la courbe en t = 0.")


E, R, r, L = 9, 80, 10, 0.45
I0 = E / (R + r)                 # 0,1 A
U0 = R * I0                      # 8 V
TAU = L / (R + r)                # 5 ms
assert abs(I0 - 0.1) < 1e-12 and abs(U0 - 8) < 1e-12 and abs(TAU - 5e-3) < 1e-12
assert abs(E / (U0 / R) - R - r) < 1e-9 and abs(TAU * (R + r) - L) < 1e-12
# semblable
E2, R2, r2, L2 = 12, 100, 20, 0.36
I02, U02, TAU2 = E2 / (R2 + r2), R2 * E2 / (R2 + r2), L2 / (R2 + r2)
assert abs(I02 - 0.1) < 1e-12 and abs(U02 - 10) < 1e-12 and abs(TAU2 - 3e-3) < 1e-12

ATT3 = ("K en position 2 : le générateur n'est plus dans la maille. Additivité : u_R + u_b = 0, avec u_R = R·i et "
        "u_b = L·di/dt + r·i. Donc L·di/dt + (R + r)·i = 0.")
ATT4 = ("i = I₀·e^(−t/τ) donne di/dt = −(I₀/τ)·e^(−t/τ). On remplace : −(L/τ)·I₀·e^(−t/τ) + (R + r)·I₀·e^(−t/τ) = 0, "
        "soit I₀·e^(−t/τ)·((R + r) − L/τ) = 0 pour tout t, donc τ = L/(R + r). La condition initiale i(0) = I₀ est vérifiée (e⁰ = 1).")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RL", "cours": "phys_ch7_dipole_RL",
  "titre": "La rupture du courant : r, τ et L à partir de u_R(t)", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Utiliser la continuité de i dans une bobine (i(0⁺) = I₀)", "Déterminer r à partir de I₀ = E/(R + r)",
                  "Établir l'équation différentielle de la rupture", "Vérifier la solution I₀·e^(−t/τ) et exprimer τ",
                  "Lire τ (tangente à l'origine) et en déduire L"],
  "enonce": {
    "intro": "On réalise le montage de la figure 1 : générateur idéal de f.é.m. E, interrupteur K à deux positions, conducteur ohmique de résistance R, bobine d'inductance L et de résistance r. K est en position 1 depuis longtemps : le régime permanent est atteint, le courant vaut I₀. À t = 0, on bascule K en position 2. Un système d'acquisition enregistre la tension u_R(t) aux bornes du conducteur ohmique (figure 2).",
    "intro_dit": "دابا نقراو l'énoncé. عندنا un générateur E، l'interrupteur K à deux positions، un conducteur ohmique R، و une bobine، l'inductance ديالها L و la résistance ديالها r. K فla position un من شحال هادي: وصلنا لle régime permanent، و le courant égale I zéro. فt égale zéro، كنحولو K لla position deux. ونسجلو la tension u R ديال le conducteur ohmique، وهي la figure deux.",
    "figures": [montage("Figure 1 : le montage"), courbe_rupture(8, 5, 30, 5, "Figure 2 : u_R(t) après la bascule")],
    "donnees": ["E = 9 V", "R = 80 Ω", "Bobine : L et r inconnues", "u_b = L·di/dt + r·i"],
    "questions": [
      question("1", "Justifier que l'intensité du courant juste après la bascule est égale à I₀, puis déterminer I₀ à l'aide de la figure 2.",
        "السؤال un: برر علاش le courant مباشرة من بعد ما حولنا K كيساوي I zéro، ومن بعد لقا I zéro ف la figure deux.",
        valeur("I₀", 0.1, "A", "i est continue : i(0⁺) = I₀ ; I₀ = u_R(0)/R = 8/80 = 0,1 A"),
        ["i(0⁺) = I₀", "u_R = R·i", "A"], ["i(0⁺) = 0", "I₀ = E/R = 9/80"],
        [aide("Une bobine peut-elle faire passer son courant d'un coup de I₀ à 0 ? Puis lis la valeur de u_R à t = 0 sur la figure 2.",
              "واش la bobine تقدر تبدل le courant ديالها دغيا من I zéro ل zéro؟ ومن بعد قرا u R ف t égale zéro فla figure deux."),
         aide("i est continue dans une bobine : i(0⁺) = I₀. Et u_R = R·i, donc I₀ = u_R(0)/R.",
              "i est continue فla bobine: i de zéro égale I zéro. و u R égale R i، إذن I zéro égale u R de zéro sur R.")],
        corr([("1 : le courant dans une bobine est continu : i(0⁺) = I₀", "le courant ديال la bobine continu"),
              ("u_R = R·i ⇒ I₀ = u_R(0)/R ; on lit u_R(0) = 8 V", "I zéro égale u R de zéro sur R"),
              ("I₀ = 8/80 = 0,1 A", "zéro virgule un ampère")],
             "السؤال un. le courant ديال la bobine continu، ما كينقزش: i مباشرة من بعد la bascule égale I zéro. و u R égale R i، إذن I zéro égale u R de zéro sur R. كنقراو u R de zéro égale huit volts. إذن I zéro égale huit sur quatre-vingts، يعني zéro virgule un ampère."),
        "ex_rl4_1", "fa_rl4_1"),
      question("2", "Montrer que la résistance de la bobine est r = 10 Ω.",
        "السؤال deux: بين بلي la résistance ديال la bobine هي r égale dix ohms.",
        valeur("r", 10, "Ω", "I₀ = E/(R + r) ⇒ r = E/I₀ − R = 9/0,1 − 80 = 10 Ω"),
        ["I₀ = E/(R + r)", "r = E/I₀ − R", "Ω"], ["r = E/I₀ = 90 Ω", "r = R·I₀"],
        [aide("Avant la bascule, K était en position 1 en régime permanent : quelle relation donne I₀ en fonction de E, R et r ?",
              "قبل la bascule، K كان فla position un، فle régime permanent. أشمن relation كتعطي I zéro بدلالة E و R و r؟"),
         aide("I₀ = E/(R + r), donc R + r = E/I₀ et r = E/I₀ − R.",
              "I zéro égale E sur R plus r. إذن R plus r égale E sur I zéro، و r égale E sur I zéro moins R.")],
        corr([("2 : en régime permanent (K en 1) : I₀ = E/(R + r)", "I zéro égale E sur R plus r"),
              ("r = E/I₀ − R = 9/0,1 − 80", "r égale E sur I zéro moins R"),
              ("r = 90 − 80 = 10 Ω", "r égale dix ohms")],
             "السؤال deux. قبل la bascule، فle régime permanent: I zéro égale E sur R plus r. إذن r égale E sur I zéro moins R. neuf sur zéro virgule un، كتعطي quatre-vingt-dix، moins quatre-vingts. إذن r égale dix ohms."),
        "ex_rl4_2", "fa_rl4_2"),
      question("3", "Établir l'équation différentielle vérifiée par i(t) après la bascule de K en position 2.",
        "السؤال trois: أثبت l'équation différentielle اللي كتحققها i من بعد ما حولنا K لla position deux.",
        phrase(ATT3),
        ["u_R + u_b = 0", "u_R = R·i", "u_b = L·di/dt + r·i"], ["u_R + u_b = E", "L·di/dt + R·i = 0 (r oubliée)"],
        [aide("En position 2, le générateur est-il encore dans la maille ? Écris la loi d'additivité dans la maille R – bobine.",
              "فla position deux، واش le générateur مازال فla maille؟ كتب la loi d'additivité ف la maille ديال R و la bobine."),
         aide("u_R + u_b = 0, puis remplace u_R = R·i et u_b = L·di/dt + r·i, et regroupe.",
              "u R plus u b égale zéro. من بعد عوض u R ب R i، و u b ب L dé i sur dé t plus r i، وجمع.")],
        corr([("3 : K en position 2, pas de générateur : u_R + u_b = 0", "u R plus u b égale zéro"),
              ("R·i + L·di/dt + r·i = 0", "R i plus L dé i sur dé t plus r i"),
              ("L·di/dt + (R + r)·i = 0", "L dé i sur dé t، plus R plus r fois i، égale zéro")],
             "السؤال trois. فla position deux، le générateur ما بقاش فla maille. la loi d'additivité: u R plus u b égale zéro. كنعوضو: R i plus L dé i sur dé t plus r i égale zéro. إذن L dé i sur dé t، plus R plus r fois i، égale zéro. على اليمين zéro، ماشي E."),
        "ex_rl4_3", "fa_rl4_3"),
      question("4", "Vérifier que i(t) = I₀·e^(−t/τ) est solution de cette équation, et exprimer τ en fonction de L, R et r.",
        "السؤال quatre: تحقق بلي i égale I zéro fois exponentielle de moins t sur tau هي solution، وعبر على tau بدلالة L و R و r.",
        phrase(ATT4),
        ["di/dt = −(I₀/τ)·e^(−t/τ)", "pour tout t", "τ = L/(R + r)"], ["di/dt = (I₀/τ)·e^(−t/τ)", "τ = (R + r)/L"],
        [aide("Dérive i(t) = I₀·e^(−t/τ) (attention au signe moins), puis remplace i et di/dt dans l'équation.",
              "دير la dérivée ديال I zéro exponentielle de moins t sur tau، رد البال ل le signe moins. ومن بعد عوض i و dé i sur dé t ف l'équation."),
         aide("Tu obtiens I₀·e^(−t/τ)·((R + r) − L/τ) = 0 pour tout t : la parenthèse doit être nulle.",
              "غادي تلقى I zéro exponentielle de moins t sur tau، fois R plus r moins L sur tau، égale zéro pour tout t. إذن la parenthèse égale zéro.")],
        corr([("4 : di/dt = −(I₀/τ)·e^(−t/τ)", "dé i sur dé t égale moins I zéro sur tau"),
              ("−(L/τ)·I₀·e^(−t/τ) + (R + r)·I₀·e^(−t/τ) = 0 ⇒ I₀·e^(−t/τ)·((R + r) − L/τ) = 0 pour tout t", "pour tout t"),
              ("τ = L/(R + r) ; et i(0) = I₀·e⁰ = I₀ : la condition initiale est vérifiée", "tau égale L sur R plus r")],
             "السؤال quatre. dé i sur dé t égale moins I zéro sur tau، fois exponentielle de moins t sur tau. كنعوضو: moins L sur tau fois I zéro exponentielle، plus R plus r fois I zéro exponentielle، égale zéro. يعني I zéro exponentielle، fois R plus r moins L sur tau، égale zéro، pour tout t. إذن tau égale L sur R plus r. و i de zéro égale I zéro: la condition initiale صحيحة."),
        "ex_rl4_4", "fa_rl4_4"),
      question("5", "Déterminer graphiquement la constante de temps τ, puis calculer l'inductance L de la bobine.",
        "السؤال cinq: لقا tau بالمبيان، ومن بعد حسب L، l'inductance ديال la bobine.",
        valeur("L", 0.45, "H", "τ = 5 ms (la tangente (T) coupe l'axe des temps) ; L = τ·(R + r) = 5·10⁻³ × 90 = 0,45 H"),
        ["τ = L/(R + r)", "L = τ·(R + r)", "10⁻³", "H"], ["L = τ·R = 0,4 H", "L = 5 × 90 = 450 H"],
        [aide("Sur la figure 2, la tangente (T) à l'origine coupe l'axe des temps en t = τ (ou bien : u_R(τ) = 0,37·u_R(0)).",
              "فla figure deux، la tangente T ف l'origine كتقطع l'axe des temps ف t égale tau. ولا: u R de tau égale zéro virgule trente-sept fois u R de zéro."),
         aide("L = τ·(R + r), avec τ en secondes et R + r = 90 Ω.",
              "L égale tau fois R plus r، و tau بla seconde، و R plus r égale quatre-vingt-dix ohms.")],
        corr([("5 : la tangente (T) coupe l'axe des temps en t = τ : τ = 5 ms = 5·10⁻³ s", "tau égale cinq millisecondes"),
              ("τ = L/(R + r) ⇒ L = τ·(R + r) = 5·10⁻³ × 90", "L égale tau fois R plus r"),
              ("L = 0,45 H", "L égale zéro virgule quarante-cinq henry")],
             "السؤال cinq. la tangente T كتقطع l'axe des temps ف t égale tau: tau égale cinq millisecondes، يعني cinq fois dix puissance moins trois seconde. tau égale L sur R plus r، إذن L égale tau fois R plus r: cinq fois dix puissance moins trois fois quatre-vingt-dix. L égale zéro virgule quarante-cinq henry."),
        "ex_rl4_5", "fa_rl4_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_rl4_1", "Question 1 : i ne saute pas", "i(0⁺) = I₀ (continuité) ; I₀ = u_R(0)/R = 8/80 = 0,1 A.",
      SIM_RUP, "K bascule en 2 : u_R part de 8 V, pas de 0",
      "شوف: le courant مستقر، i égale I zéro، و u R égale huit volts. دابا كنحولو K لla position deux. شوف l'écran: u R ما طاحتش ل zéro دغيا. كتبدا من huit volts، و كتنزل بشوية. علاش؟ le courant ديال la bobine continu، ما كينقزش: i de zéro égale I zéro. و u R égale R i، إذن I zéro égale huit sur quatre-vingts، يعني zéro virgule un ampère، cent milliampères.",
      centre=[("i(0⁺) = I₀ (i continue dans la bobine)", "le courant ديال la bobine continu"), ("I₀ = u_R(0)/R = 8/80 = 0,1 A", "يعني zéro virgule un ampère")],
      pointage=[{"mot": "دابا كنحولو K لla position deux", "commande": "play_until", "parametres": {"moment": "bascule"}},
                {"mot": "شوف l'écran", "commande": "play_until", "parametres": {"moment": "courbe_rupture"}},
                {"mot": "كتبدا من huit volts", "repere": "courbe"},
                {"mot": "le courant ديال la bobine continu", "cible": "centre:0"},
                {"mot": "يعني zéro virgule un ampère", "cible": "centre:1"}]),
    diapo_sim("ex_rl4_2", "Question 2 : r = E/I₀ − R", "K en 1, régime permanent : I₀ = E/(R + r) ⇒ r = 9/0,1 − 80 = 10 Ω.",
      SIM_ETA, "Avant la bascule : K en position 1, régime permanent",
      "نرجعو لقبل la bascule. K فla position un، E égale neuf volts، R égale quatre-vingts ohms. le courant كيتأسس، وفle régime permanent: I zéro égale E sur R plus r. إذن R plus r égale E sur I zéro: neuf sur zéro virgule un، يعني quatre-vingt-dix ohms. r égale quatre-vingt-dix moins quatre-vingts، يعني dix ohms. شوف la bobine: r égale dix ohms.",
      centre=[("I₀ = E/(R + r) ⇒ r = E/I₀ − R", "I zéro égale E sur R plus r"), ("r = 9/0,1 − 80 = 10 Ω", "يعني dix ohms")],
      pointage=[{"mot": "K فla position un", "commande": "play_until", "parametres": {"moment": "fermeture"}},
                {"mot": "E égale neuf volts", "repere": "generateur"},
                {"mot": "R égale quatre-vingts ohms", "repere": "resistance"},
                {"mot": "وفle régime permanent", "commande": "play_until", "parametres": {"moment": "permanent"}},
                {"mot": "I zéro égale E sur R plus r", "cible": "centre:0"},
                {"mot": "يعني dix ohms", "cible": "centre:1"},
                {"mot": "شوف la bobine", "repere": "bobine"}]),
    diapo_sim("ex_rl4_3", "Question 3 : l'équation de la rupture", "u_R + u_b = 0 ⇒ L·di/dt + (R + r)·i = 0.",
      FIG_RUP, "En position 2, le générateur n'est plus dans la maille : 0 à droite",
      "شوف le circuit: K فla position deux، le générateur E ما بقاش فla maille. بقات غير R و la bobine. la loi d'additivité: u R plus u b égale zéro. كنعوضو: R i، plus L dé i sur dé t، plus r i، égale zéro. le résultat: L dé i sur dé t، plus R plus r fois i، égale zéro. نفس l'équation ديال l'établissement، ولكن على اليمين zéro.",
      centre=[("u_R + u_b = 0", "u R plus u b égale zéro"), ("L·di/dt + (R + r)·i = 0", "le résultat: L dé i sur dé t")],
      pointage=[{"mot": "شوف le circuit", "commande": "play_until", "parametres": {"moment": "circuit"}},
                {"mot": "la loi d'additivité", "commande": "play_until", "parametres": {"moment": "additivite"}},
                {"mot": "u R plus u b égale zéro", "cible": "centre:0"},
                {"mot": "le résultat: L dé i sur dé t", "commande": "play_until", "parametres": {"moment": "resultat"}}]),
    diapo_sim("ex_rl4_4", "Question 4 : vérifier I₀·e^(−t/τ)", "di/dt = −(I₀/τ)·e^(−t/τ) ; on remplace : τ = L/(R + r).",
      FIG_RUP, "La solution de la rupture : i part de I₀ et tend vers 0",
      "عندنا l'équation: L dé i sur dé t، plus R plus r fois i، égale zéro. la solution: I zéro fois exponentielle de moins t sur tau. la dérivée: moins I zéro sur tau، fois exponentielle de moins t sur tau. كنعوضو: I zéro exponentielle، fois R plus r moins L sur tau، égale zéro، pour tout t. إذن tau égale L sur R plus r. و ف t égale zéro، exponentielle de zéro égale un: i de zéro égale I zéro. شوف la figure: i كتبدا من I zéro و كتمشي ل zéro.",
      centre=[("di/dt = −(I₀/τ)·e^(−t/τ)", "la dérivée: moins I zéro sur tau"), ("I₀·e^(−t/τ)·((R + r) − L/τ) = 0 ⇒ τ = L/(R + r)", "إذن tau égale L sur R plus r")],
      pointage=[{"mot": "عندنا l'équation", "commande": "play_until", "parametres": {"moment": "resultat"}},
                {"mot": "la dérivée: moins I zéro sur tau", "cible": "centre:0"},
                {"mot": "إذن tau égale L sur R plus r", "cible": "centre:1"},
                {"mot": "شوف la figure", "commande": "play_until", "parametres": {"moment": "fin"}}]),
    diapo_sim("ex_rl4_5", "Question 5 : τ puis L", "La tangente coupe l'axe des temps en τ = 5 ms ; L = τ·(R + r) = 0,45 H.",
      SIM_RUP, "u_R descend de 8 V vers 0 : τ se lit sur la tangente à l'origine",
      "شوف la courbe ديال u R: كتبدا من huit volts و كتنزل نحو zéro. فla figure deux ديال l'énoncé، la tangente T ف t égale zéro كتقطع l'axe des temps ف tau. كنقراو tau égale cinq millisecondes. نتأكدو: ف tau، u R égale zéro virgule trente-sept fois huit، يعني environ trois volts. من بعد، tau égale L sur R plus r، إذن L égale tau fois R plus r. cinq fois dix puissance moins trois، fois quatre-vingt-dix، كتعطي zéro virgule quarante-cinq henry.",
      centre=[("τ = 5 ms (tangente ∩ axe des temps)", "كنقراو tau égale cinq millisecondes"), ("L = τ·(R + r) = 5·10⁻³ × 90 = 0,45 H", "كتعطي zéro virgule quarante-cinq henry")],
      pointage=[{"mot": "شوف la courbe ديال u R", "commande": "play_until", "parametres": {"moment": "courbe_rupture"}},
                {"mot": "كتبدا من huit volts", "repere": "courbe"},
                {"mot": "كنقراو tau égale cinq millisecondes", "cible": "centre:0"},
                {"mot": "كتعطي zéro virgule quarante-cinq henry", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_rl4_1", "Plus facile : juste après la bascule", "سؤال ساهل على la continuité ديال le courant.",
      "Le courant valait I₀ = 0,1 A ; on bascule K en position 2. Juste après, i vaut…",
      ["0", "I₀ = 0,1 A", "E/R"], 1, {
        "1": {"juste": rep("برافو! le courant ديال la bobine continu: i de zéro égale I zéro.", "Juste : i est continue dans une bobine, i(0⁺) = I₀.")},
        "0": {"1": rep("la bobine كتعارض les variations ديال le courant. واش تقدر i تطيح ل zéro دغيا؟ عاود.", "La bobine s'oppose aux variations de i : peut-il tomber à 0 d'un coup ? Réessaie."),
              "2": rep("الجواب هو I zéro، zéro virgule un ampère. le courant ديال la bobine ما كينقزش، كينقص بشوية.", "Réponse : i(0⁺) = I₀ = 0,1 A ; il diminue ensuite progressivement.")},
        "2": {"1": rep("فla position deux، le générateur ما بقاش فla maille. E ما بقاتش كتدخل. عاود.", "En position 2, le générateur n'est plus dans la maille. Réessaie."),
              "2": rep("الجواب هو I zéro: le courant اللي كان قبل la bascule، حيت i continue.", "Réponse : I₀, la valeur juste avant la bascule.")}},
      "Le courant valait I zéro. On bascule K. Juste après، i vaut ?"),
    qcm_facile("fa_rl4_2", "Plus facile : trouver r", "سؤال ساهل باش نلقاو r.",
      "E = 9 V, R = 80 Ω, I₀ = 0,1 A. La résistance de la bobine vaut…",
      ["10 Ω", "90 Ω", "0 Ω"], 0, {
        "0": {"juste": rep("برافو! E sur I zéro égale quatre-vingt-dix، ناقص quatre-vingts، كتعطي dix ohms.", "Juste : r = E/I₀ − R = 90 − 80 = 10 Ω.")},
        "1": {"1": rep("quatre-vingt-dix هي la résistance totale R plus r. شحال بقا ل la bobine؟ عاود.", "90 Ω, c'est R + r. Que reste-t-il pour la bobine ? Réessaie."),
              "2": rep("الجواب هو dix ohms: R plus r égale quatre-vingt-dix، و R égale quatre-vingts.", "Réponse : r = 90 − 80 = 10 Ω.")},
        "2": {"1": rep("إلى كانت r égale zéro، I zéro غادي تكون E sur R. واش neuf sur quatre-vingts كتعطي zéro virgule un؟ عاود.", "Si r = 0, I₀ = 9/80 ≠ 0,1 A. Réessaie."),
              "2": rep("الجواب هو dix ohms: E sur I zéro moins R.", "Réponse : r = E/I₀ − R = 10 Ω.")}},
      "E égale neuf volts، R égale quatre-vingts ohms، I zéro égale zéro virgule un ampère. r vaut ?"),
    qcm_facile("fa_rl4_3", "Plus facile : l'équation de la rupture", "سؤال ساهل: اختار l'équation ديال la rupture.",
      "Après la bascule de K en position 2, i(t) vérifie…",
      ["L·di/dt + (R + r)·i = E", "L·di/dt + (R + r)·i = 0", "L·di/dt − (R + r)·i = 0"], 1, {
        "1": {"juste": rep("برافو! بلا générateur: u R plus u b égale zéro.", "Juste : sans générateur, u_R + u_b = 0.")},
        "0": {"1": rep("هادي ديال l'établissement. فla position deux، واش le générateur مازال فla maille؟ عاود.", "C'est l'équation de l'établissement ; en position 2 le générateur n'est plus là. Réessaie."),
              "2": rep("الجواب: L dé i sur dé t plus R plus r fois i égale zéro. على اليمين zéro، حيت ما كاينش E.", "Réponse : L·di/dt + (R + r)·i = 0.")},
        "2": {"1": rep("شوف le signe: u R égale R i و u b فيها plus r i. كاين شي moins؟ عاود.", "Vérifie le signe : u_R = R·i et u_b contient +r·i. Réessaie."),
              "2": rep("الجواب: L dé i sur dé t plus R plus r fois i égale zéro، بle signe plus.", "Réponse : L·di/dt + (R + r)·i = 0.")}},
      "Après la bascule، i vérifie quelle équation ?"),
    vrai_faux_facile("fa_rl4_4", "Plus facile : vrai ou faux", "سؤال ساهل على la solution ديال la rupture.",
      "Solution proposée : i(t) = I₀·e^(−t/τ).",
      [("Sa dérivée est di/dt = −(I₀/τ)·e^(−t/τ).", True, "La dérivée de e^(−t/τ) est −(1/τ)·e^(−t/τ)."),
       ("Elle vérifie i(0) = I₀.", True, "e⁰ = 1, donc i(0) = I₀ : c'est la continuité du courant."),
       ("En remplaçant, on trouve τ = (R + r)/L.", False, "On trouve (R + r) − L/τ = 0, donc τ = L/(R + r).")]),
    qcm_facile("fa_rl4_5", "Plus facile : la tangente", "سؤال ساهل على la tangente à l'origine.",
      "Pour une courbe qui descend (rupture), la tangente à l'origine coupe l'axe des temps à…",
      ["t = 5τ", "t = τ", "t = 0,37 s"], 1, {
        "1": {"juste": rep("برافو! la tangente à l'origine كتقطع l'axe des temps ف t égale tau.", "Juste : la tangente coupe l'axe des temps en t = τ.")},
        "0": {"1": rep("cinq tau هي la fin ديال le régime transitoire. la tangente كتقطع قبل. عاود.", "5τ, c'est la fin du régime transitoire. Réessaie."),
              "2": rep("الجواب هو t égale tau. cinq tau هي فين i environ zéro.", "Réponse : t = τ (à 5τ, i ≈ 0).")},
        "2": {"1": rep("zéro virgule trente-sept هو نسبة ديال la valeur، ماشي وقت. عاود.", "0,37 est une fraction de la valeur, pas un temps. Réessaie."),
              "2": rep("الجواب هو t égale tau. و ف tau، la valeur égale zéro virgule trente-sept fois la valeur الأولى.", "Réponse : t = τ ; en τ, la valeur vaut 0,37 fois la valeur initiale.")}},
      "Pour une courbe qui descend، la tangente à l'origine coupe l'axe des temps à quel instant ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec E = 12 V et R = 100 Ω ; la bobine (L, r) est inconnue. K est en position 1 depuis longtemps ; à t = 0, on le bascule en position 2. La figure 2 donne u_R(t).",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale douze volts، و R égale cent ohms. فt égale zéro، كنحولو K لla position deux.",
      "figures": [courbe_rupture(10, 3, 18, 3, "Figure 2 : u_R(t) après la bascule")],
      "donnees": ["E = 12 V", "R = 100 Ω", "Bobine : L et r inconnues"],
      "questions": [
        question_semblable("1", "Justifier que l'intensité du courant juste après la bascule est égale à I₀, puis déterminer I₀ à l'aide de la figure 2.",
          valeur("I₀", 0.1, "A", "i(0⁺) = I₀ ; I₀ = u_R(0)/R = 10/100 = 0,1 A"), ["i(0⁺) = I₀", "u_R = R·i"], ["i(0⁺) = 0"],
          corr([("1 : i continue : i(0⁺) = I₀ ; I₀ = u_R(0)/R = 10/100", "I zéro égale u R de zéro sur R"), ("I₀ = 0,1 A", "zéro virgule un ampère")],
               "i continue فla bobine. I zéro égale u R de zéro sur R، يعني dix sur cent، كتعطي zéro virgule un ampère.")),
        question_semblable("2", "Montrer que la résistance de la bobine est r = 20 Ω.",
          valeur("r", 20, "Ω", "r = E/I₀ − R = 12/0,1 − 100 = 20 Ω"), ["r = E/I₀ − R", "Ω"], ["r = E/I₀"],
          corr([("2 : I₀ = E/(R + r) ⇒ r = E/I₀ − R = 120 − 100", "r égale E sur I zéro moins R"), ("r = 20 Ω", "vingt ohms")],
               "r égale E sur I zéro moins R، يعني cent vingt moins cent، كتعطي vingt ohms.")),
        question_semblable("3", "Établir l'équation différentielle vérifiée par i(t) après la bascule de K en position 2.",
          phrase(ATT3), ["u_R + u_b = 0", "u_b = L·di/dt + r·i"], ["u_R + u_b = E"],
          corr([("3 : u_R + u_b = 0 ; R·i + L·di/dt + r·i = 0", "u R plus u b égale zéro"), ("L·di/dt + (R + r)·i = 0", "R plus r fois i، égale zéro")],
               "u R plus u b égale zéro. إذن L dé i sur dé t، plus R plus r fois i، égale zéro.")),
        question_semblable("4", "Vérifier que i(t) = I₀·e^(−t/τ) est solution de cette équation, et exprimer τ en fonction de L, R et r.",
          phrase(ATT4), ["di/dt = −(I₀/τ)·e^(−t/τ)", "pour tout t"], ["τ = (R + r)/L"],
          corr([("4 : di/dt = −(I₀/τ)·e^(−t/τ) ; I₀·e^(−t/τ)·((R + r) − L/τ) = 0 pour tout t", "pour tout t"), ("τ = L/(R + r)", "tau égale L sur R plus r")],
               "dé i sur dé t égale moins I zéro sur tau fois l'exponentielle. كنعوضو: pour tout t، tau égale L sur R plus r.")),
        question_semblable("5", "Déterminer graphiquement la constante de temps τ, puis calculer l'inductance L de la bobine.",
          valeur("L", 0.36, "H", "τ = 3 ms ; L = τ·(R + r) = 3·10⁻³ × 120 = 0,36 H"), ["L = τ·(R + r)", "H"], ["L = τ·R"],
          corr([("5 : τ = 3 ms (tangente ∩ axe des temps)", "tau égale trois millisecondes"), ("L = τ·(R + r) = 3·10⁻³ × 120 = 0,36 H", "zéro virgule trente-six henry")],
               "tau égale trois millisecondes. L égale tau fois R plus r، يعني trois fois dix puissance moins trois fois cent vingt، كتعطي zéro virgule trente-six henry.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
