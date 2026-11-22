# Exercice de physique, ch. 7 (dipôle RL), niveau difficile n° 7 : ouvrir l'interrupteur — une diode et un conducteur
# ohmique R₁ en parallèle sur la bobine : continuité de i, équation, τ', surtension u_b(0⁺), énergie, critique.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RL.json : cas_types « rupture » (diode + R₁ en parallèle :
#    i(0⁺) = I₀, u_b(0⁺) = −R₁·I₀, surtension), « energie » ; erreurs_examen « rupture avec diode (2025 R) : i(0⁺) = 0
#    ou u_b = 0 » ; a_ne_pas_dire : le nom courant de cette diode n'est pas employé (on la décrit seulement).
#  - nationaux : 2025 R (2-1 à 2-3 : bobine idéale, E = 10 V, R₁ = 1 kΩ) ; ici au-dessus : bobine réelle (r ≠ 0),
#    τ' de la nouvelle maille, énergie dissipée, critique « sans R₁ » (deux notions combinées). Données propres.
#  - cours phys_ch7_dipole_RL : rl_t3_diode (rupture.html?vue=diode), rl_t2a_verifier (fig_ed_rupture),
#    rl_l7_energie, rl_s8_R (influence.html?vue=R), rl_m2_fermeture (circuit-rl.html).
#  - séries en ligne : recherche web (talamidi, moutamadris, alloschool, série P7 N. Naceiri) ; pages non ouvertes
#    (domaines bloqués dans le conteneur), seuls les intitulés comparés. La simulation de la diode garde ses propres
#    valeurs (celles du cours) : la voix les dit comme l'exemple du cours, puis dit nos valeurs comme telles.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch7_rl_7"
SIMD = "/media/simulations/physics/dipole-rl-tableau/"
PAR = "&E=12&R_ohm=50&L_H=0.5"
SIM_ETA = SIMD + "circuit-rl.html?vue=etablissement" + PAR
SIM_RUP = SIMD + "circuit-rl.html?vue=rupture" + PAR
DIODE = SIMD + "rupture.html?vue=diode"
FIG_RUP = SIMD + "figures.html?fig=fig_ed_rupture"
INFL = SIMD + "influence.html?vue=R"


def montage(titre):
    """E, K, R en série avec la bobine ; en parallèle sur la bobine : diode D (passante de bas en haut) + R₁."""
    return schema(titre, 9.4, 4.8,
        dipole([1, 0.8], [1, 3.6], "G", "E", pos="o"),
        fil([1, 3.6], [1.6, 3.6]),
        dipole([1.6, 3.6], [3.2, 3.6], "K", "K"),
        dipole([3.2, 3.6], [5.4, 3.6], "R", "R", pos="s"),
        fil([5.4, 3.6], [8.4, 3.6]),
        dipole([6, 3.6], [6, 0.8], "L", "(L, r)", pos="o"),
        dipole([8.4, 3.6], [8.4, 2.2], "R", "R₁", pos="e", taille=0.8),
        dipole([8.4, 0.8], [8.4, 2.2], "D", "D", pos="e"),
        fil([8.4, 0.8], [1, 0.8]),
        courant([5.7, 3.6], "d"),
        tension([6.8, 1.2], [6.8, 3.2], "u_b", couleur="violet", pos="e"),
        legende="La diode D est passante dans le sens de la flèche de son symbole (de bas en haut).")


E, R, r, L, R1 = 12, 50, 10, 0.5, 240
I0 = E / (R + r)                 # 0,2 A
TAUP = L / (R1 + r)              # 2 ms
UB0 = -R1 * I0                   # −48 V
EM = 0.5 * L * I0 ** 2           # 0,01 J
TAUS = L / r                     # 50 ms
assert abs(I0 - 0.2) < 1e-12 and abs(TAUP - 2e-3) < 1e-12 and abs(UB0 + 48) < 1e-9 and abs(EM - 0.01) < 1e-12 and abs(TAUS - 0.05) < 1e-12
# u_b(0⁺) = L·di/dt + r·i avec L·di/dt(0⁺) = −(R₁ + r)·I₀ : on retrouve −R₁·I₀
assert abs((-(R1 + r) * I0 + r * I0) - UB0) < 1e-9
# semblable
E2, R2, r2, L2, R12 = 10, 30, 20, 0.4, 380
I02, TAUP2, UB02, EM2, TAUS2 = E2 / (R2 + r2), L2 / (R12 + r2), -R12 * E2 / (R2 + r2), 0.5 * L2 * (E2 / (R2 + r2)) ** 2, L2 / r2
assert abs(I02 - 0.2) < 1e-12 and abs(TAUP2 - 1e-3) < 1e-12 and abs(UB02 + 76) < 1e-9 and abs(EM2 - 0.008) < 1e-12 and abs(TAUS2 - 0.02) < 1e-12

ATT2 = ("Après l'ouverture de K, le courant de la bobine passe par R₁ et la diode (passante, tension nulle) : maille "
        "bobine – R₁ – D. Additivité : u_b + R₁·i = 0, avec u_b = L·di/dt + r·i. Donc L·di/dt + (R₁ + r)·i = 0.")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RL", "cours": "phys_ch7_dipole_RL",
  "titre": "Ouvrir K : une diode pour la bobine, et la surtension", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer I₀ et expliquer le rôle de la diode", "Établir l'équation de la rupture dans la maille bobine – R₁ – diode",
                  "Exprimer et calculer τ' = L/(R₁ + r)", "Calculer la surtension u_b(0⁺) = −R₁·I₀",
                  "Calculer l'énergie ½·L·I₀² et dire où elle va", "Critiquer un choix de montage avec τ"],
  "enonce": {
    "intro": "Un générateur idéal de f.é.m. E alimente, à travers un interrupteur simple K, un conducteur ohmique de résistance R en série avec une bobine (L, r). En parallèle sur la bobine, on place une diode D en série avec un conducteur ohmique de résistance R₁ (figure). La diode est idéale : passante, la tension à ses bornes est nulle ; bloquée, elle ne laisse passer aucun courant. K est fermé depuis longtemps ; à t = 0, on ouvre K.",
    "intro_dit": "دابا نقراو l'énoncé. un générateur E، l'interrupteur K، un conducteur ohmique R، و une bobine، L و r. en parallèle مع la bobine، كاينة une diode D مع un conducteur ohmique R un. la diode idéale: ملي passante، la tension ديالها zéro، و ملي bloquée، ما كيدوز فيها حتى courant. K مسدود من شحال هادي، و فt égale zéro كنحلو K.",
    "figures": [montage("Figure : le montage")],
    "donnees": ["E = 12 V ; R = 50 Ω", "Bobine : L = 0,5 H ; r = 10 Ω", "R₁ = 240 Ω", "u_b = L·di/dt + r·i"],
    "questions": [
      question("1", "K étant fermé (régime permanent), expliquer pourquoi la diode est bloquée, puis calculer l'intensité I₀ du courant dans la bobine.",
        "السؤال un: K مسدود، فle régime permanent. شرح علاش la diode bloquée، ومن بعد حسب I zéro، le courant ديال la bobine.",
        valeur("I₀", 0.2, "A", "diode en inverse : bloquée ; I₀ = E/(R + r) = 12/(50 + 10) = 0,2 A"),
        ["I₀ = E/(R + r)", "diode bloquée", "A"], ["I₀ = E/R = 0,24 A", "I₀ = E/(R + R₁ + r)"],
        [aide("Regarde le sens passant de la diode et la tension u_b = r·I₀ > 0 de la bobine : la diode est-elle dans son sens passant ? Si elle est bloquée, quels dipôles restent dans la maille ?",
              "شوف le sens passant ديال la diode، و u b égale r I zéro كبر من zéro. واش la diode فle sens passant؟ إلى كانت bloquée، شنو كيبقى فla maille؟"),
         aide("Diode bloquée : la branche D – R₁ ne compte pas. I₀ = E/(R + r).",
              "la diode bloquée: la branche ديال D و R un ما كتحسبش. I zéro égale E sur R plus r.")],
        corr([("1 : la tension aux bornes de la branche D – R₁ (u_b = r·I₀ > 0) est dans le sens bloquant de D : D est bloquée", "la diode bloquée"),
              ("la branche D – R₁ ne conduit pas : I₀ = E/(R + r)", "I zéro égale E sur R plus r"),
              ("A.N. : I₀ = 12/60 = 0,2 A", "zéro virgule deux ampère")],
             "السؤال un. ملي K مسدود، la tension ديال la bobine كتجي ضد le sens passant ديال D: la diode bloquée، و la branche ديال D و R un ما كيدوز فيها والو. إذن I zéro égale E sur R plus r: douze sur soixante، يعني zéro virgule deux ampère."),
        "ex_rl7_1", "fa_rl7_1"),
      question("2", "Établir l'équation différentielle vérifiée par i(t), intensité du courant dans la bobine, après l'ouverture de K.",
        "السؤال deux: أثبت l'équation différentielle اللي كتحققها i، le courant ديال la bobine، من بعد ما كنحلو K.",
        phrase(ATT2),
        ["u_b + u_R₁ = 0", "u_R₁ = R₁·i", "u_D = 0"], ["L·di/dt + (R + r)·i = 0", "u_b + u_R₁ = E"],
        [aide("K ouvert : le générateur et R ne sont plus traversés. Par où passe le courant de la bobine ? Quelle maille se forme ?",
              "K محلول: le générateur و R ما بقا كيدوز فيهم والو. فين كيدوز le courant ديال la bobine؟ أشمن maille؟"),
         aide("Maille bobine – R₁ – diode passante (u_D = 0) : u_b + R₁·i = 0, puis remplace u_b.",
              "la maille ديال la bobine و R un و la diode passante، u D égale zéro: u b plus R un i égale zéro. ومن بعد عوض u b.")],
        corr([("2 : K ouvert : le courant de la bobine passe par R₁ et D (passante, u_D = 0)", "le courant ديال la bobine كيدوز ف R un و la diode"),
              ("u_b + R₁·i = 0 ; u_b = L·di/dt + r·i", "u b plus R un i égale zéro"),
              ("L·di/dt + (R₁ + r)·i = 0", "L dé i sur dé t، plus R un plus r fois i، égale zéro")],
             "السؤال deux. ملي كنحلو K، le courant ديال la bobine كيدوز ف R un و la diode، و la diode passante: u D égale zéro. la loi d'additivité: u b plus R un i égale zéro. كنعوضو u b: L dé i sur dé t، plus R un plus r fois i، égale zéro. ماشي R، هي R un."),
        "ex_rl7_2", "fa_rl7_2"),
      question("3", "Vérifier que i(t) = I₀·e^(−t/τ') est solution, exprimer τ' et calculer sa valeur (en ms).",
        "السؤال trois: تحقق بلي i égale I zéro exponentielle de moins t sur tau prime هي solution، عبر على tau prime و حسبها بla milliseconde.",
        valeur("τ'", 2, "ms", "τ' = L/(R₁ + r) = 0,5/(240 + 10) = 2·10⁻³ s = 2 ms"),
        ["di/dt = −(I₀/τ')·e^(−t/τ')", "τ' = L/(R₁ + r)", "ms"], ["τ' = L/(R + r) = 8,3 ms", "τ' = L/r"],
        [aide("Dérive i(t), remplace dans l'équation de la question 2 : le coefficient de e^(−t/τ') doit être nul pour tout t.",
              "دير la dérivée ديال i، و عوض ف l'équation ديال السؤال deux: le coefficient ديال l'exponentielle خاصو يكون zéro pour tout t."),
         aide("Tu trouves τ' = L/(R₁ + r) : la résistance de la nouvelle maille, pas R + r.",
              "غادي تلقى tau prime égale L sur R un plus r: la résistance ديال la maille الجديدة، ماشي R plus r.")],
        corr([("3 : di/dt = −(I₀/τ')·e^(−t/τ') ; I₀·e^(−t/τ')·((R₁ + r) − L/τ') = 0 pour tout t", "pour tout t"),
              ("τ' = L/(R₁ + r) ; i(0) = I₀ (continuité)", "tau prime égale L sur R un plus r"),
              ("A.N. : τ' = 0,5/250 = 2·10⁻³ s = 2 ms", "deux millisecondes")],
             "السؤال trois. dé i sur dé t égale moins I zéro sur tau prime، fois l'exponentielle. كنعوضو: I zéro exponentielle، fois R un plus r moins L sur tau prime، égale zéro، pour tout t. إذن tau prime égale L sur R un plus r. و i de zéro égale I zéro. l'application numérique: zéro virgule cinq sur deux cent cinquante، كتعطي deux millisecondes."),
        "ex_rl7_3", "fa_rl7_3"),
      question("4", "Calculer la tension u_b(0⁺) aux bornes de la bobine juste après l'ouverture de K. Comparer à E.",
        "السؤال quatre: حسب u b مباشرة من بعد ما حلينا K، وقارنها مع E.",
        valeur("u_b(0⁺)", -48, "V", "u_b(0⁺) = −R₁·i(0⁺) = −R₁·I₀ = −240 × 0,2 = −48 V"),
        ["u_b = −R₁·i", "i(0⁺) = I₀", "V"], ["u_b(0⁺) = r·I₀ = 2 V", "u_b(0⁺) = 0"],
        [aide("Dans la maille bobine – R₁ – D, u_b = −R₁·i. Que vaut i juste après l'ouverture ?",
              "فla maille، u b égale moins R un i. شحال كتساوي i مباشرة من بعد ما حلينا K؟"),
         aide("i est continue : i(0⁺) = I₀ = 0,2 A. Donc u_b(0⁺) = −R₁·I₀ ; compare |u_b(0⁺)| à E = 12 V.",
              "i continue: i de zéro égale I zéro، zéro virgule deux ampère. إذن u b égale moins R un fois I zéro. قارن la valeur ديالها مع E égale douze volts.")],
        corr([("4 : maille : u_b = −R₁·i ; continuité : i(0⁺) = I₀", "u b égale moins R un i"),
              ("u_b(0⁺) = −240 × 0,2 = −48 V", "moins quarante-huit volts"),
              ("|u_b(0⁺)| = 48 V = 4 × E : surtension (elle change de signe), limitée par R₁", "quatre fois E")],
             "السؤال quatre. فla maille، u b égale moins R un i. و i continue، i de zéro égale I zéro. إذن u b égale moins deux cent quarante fois zéro virgule deux، يعني moins quarante-huit volts. هادي quatre fois E، و la signe تقلبات: une surtension، و R un هي اللي كتحددها."),
        "ex_rl7_4", "fa_rl7_4"),
      question("5", "Calculer l'énergie E_m emmagasinée dans la bobine juste avant l'ouverture de K. Que devient-elle ensuite ?",
        "السؤال cinq: حسب l'énergie E m اللي فla bobine قبل ما نحلو K. فين كتمشي من بعد؟",
        valeur("E_m", 0.01, "J", "E_m = ½·L·I₀² = ½ × 0,5 × 0,2² = 0,01 J"),
        ["E_m = ½·L·i²", "J"], ["E_m = ½·L·I₀ = 0,05 J", "E_m = L·I₀² = 0,02 J"],
        [aide("L'énergie d'une bobine dépend de L et du carré du courant qui la traverse.",
              "l'énergie ديال la bobine كتتعلق ب L و ب le carré ديال le courant."),
         aide("E_m = ½·L·I₀², avec I₀ = 0,2 A. Ensuite le courant passe dans R₁ et r : effet Joule.",
              "E m égale un demi L I zéro au carré. ومن بعد le courant كيدوز ف R un و r: l'effet Joule.")],
        corr([("5 : E_m = ½·L·I₀²", "E m égale un demi L I zéro au carré"),
              ("A.N. : E_m = ½ × 0,5 × 0,2² = 0,01 J", "zéro virgule zéro un joule"),
              ("Après l'ouverture, cette énergie est dissipée par effet Joule dans R₁ et dans r.", "l'effet Joule")],
             "السؤال cinq. E m égale un demi L I zéro au carré: un demi fois zéro virgule cinq fois zéro virgule deux au carré، يعني zéro virgule zéro un joule. من بعد ما كنحلو K، هاد l'énergie كتولي سخانة ف R un و ف r: هادا l'effet Joule."),
        "ex_rl7_5", "fa_rl7_5"),
      question("6", "Un élève propose de supprimer R₁ (diode seule) « pour que le courant s'annule plus vite ». Calculer la nouvelle constante de temps τ'' (en ms) et conclure.",
        "السؤال six: تلميذ بغا يحيد R un، و يخلي غير la diode، باش le courant يوصل ل zéro دغيا. حسب tau seconde بla milliseconde، و قول واش عندو الحق.",
        valeur("τ''", 50, "ms", "τ'' = L/r = 0,5/10 = 0,05 s = 50 ms"),
        ["τ = L/(résistance de la maille)", "ms"], ["τ'' = 0", "τ'' < τ'"],
        [aide("Sans R₁, quelle résistance reste dans la maille bobine – diode ?",
              "بلا R un، شنو هي la résistance اللي بقات فla maille ديال la bobine و la diode؟"),
         aide("τ'' = L/r. Compare à τ' = 2 ms : plus la résistance de la maille est petite, plus τ est grand.",
              "tau seconde égale L sur r. قارن مع tau prime: كل ما صغرات la résistance، كتكبر tau.")],
        corr([("6 : sans R₁, maille bobine – D : τ'' = L/r", "tau seconde égale L sur r"),
              ("A.N. : τ'' = 0,5/10 = 0,05 s = 50 ms", "cinquante millisecondes"),
              ("τ'' = 25 τ' : le courant s'annule bien plus lentement ; l'élève a tort (R₁ accélère l'annulation, au prix d'une surtension plus grande).", "التلميذ غالط")],
             "السؤال six. بلا R un، فla maille بقات غير r. tau seconde égale L sur r: zéro virgule cinq sur dix، يعني cinquante millisecondes، vingt-cinq fois tau prime. إذن التلميذ غالط: le courant كيوصل ل zéro بشوية بزاف. R un كتسرع، ولكن كتكبر la surtension."),
        "ex_rl7_6", "fa_rl7_6"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_rl7_1", "Question 1 : diode bloquée, I₀ = E/(R + r)", "Diode bloquée : seule la maille E – R – bobine conduit ; I₀ = 12/60 = 0,2 A.",
      SIM_ETA, "Diode bloquée : tout se passe comme dans le circuit RL simple",
      "ملي K مسدود، la diode bloquée: la tension ديال la bobine كتجي ضد le sens passant ديالها، و ما كيدوز فيها والو. إذن الدارة بحال هادي، بلا la diode. شوف: E égale douze volts، R égale cinquante ohms، و la bobine، r égale dix ohms. كنسدو K، و كنتسناو le régime permanent. I zéro égale E sur R plus r: douze sur soixante، يعني zéro virgule deux ampère، deux cents milliampères.",
      centre=[("D bloquée : I₀ = E/(R + r)", "I zéro égale E sur R plus r"), ("I₀ = 12/60 = 0,2 A", "يعني zéro virgule deux ampère")],
      pointage=[{"mot": "E égale douze volts", "repere": "generateur"},
                {"mot": "R égale cinquante ohms", "repere": "resistance"},
                {"mot": "r égale dix ohms", "repere": "bobine"},
                {"mot": "كنسدو K", "commande": "play_until", "parametres": {"moment": "courbe_i"}},
                {"mot": "و كنتسناو le régime permanent", "commande": "play_until", "parametres": {"moment": "permanent"}},
                {"mot": "I zéro égale E sur R plus r", "cible": "centre:0"},
                {"mot": "يعني zéro virgule deux ampère", "repere": "regime_permanent"}]),
    diapo_sim("ex_rl7_2", "Question 2 : la maille bobine – R₁ – diode", "K ouvert : u_b + R₁·i = 0 ⇒ L·di/dt + (R₁ + r)·i = 0.",
      DIODE, "Sans diode, une étincelle ; avec la diode, le courant de la bobine trouve un chemin",
      "شوف: يلا حلينا un interrupteur بسيط، le courant ديال la bobine ما عندو فين يدوز: كتبان une étincelle. دابا كنزيدو la diode مع R un en parallèle مع la bobine. ملي كنحلو K، le courant ديال la bobine كيدوز ف la diode و R un. la maille: la bobine، R un، و la diode passante، u D égale zéro. la loi d'additivité: u b plus R un i égale zéro. إذن L dé i sur dé t، plus R un plus r fois i، égale zéro.",
      centre=[("u_b + R₁·i = 0 (u_D = 0)", "u b plus R un i égale zéro"), ("L·di/dt + (R₁ + r)·i = 0", "إذن L dé i sur dé t")],
      pointage=[{"mot": "كتبان une étincelle", "commande": "play_until", "parametres": {"moment": "etincelle"}},
                {"mot": "دابا كنزيدو la diode", "commande": "play_until", "parametres": {"moment": "diode"}},
                {"mot": "مع R un", "repere": "R1"},
                {"mot": "u b plus R un i égale zéro", "cible": "centre:0"},
                {"mot": "إذن L dé i sur dé t", "cible": "centre:1"}]),
    diapo_sim("ex_rl7_3", "Question 3 : τ' = L/(R₁ + r)", "Même forme que la rupture du cours, avec R₁ à la place de R : τ' = 0,5/250 = 2 ms.",
      FIG_RUP, "L'équation de la rupture : la résistance de la maille fixe τ",
      "فالدرس، la maille ديال la rupture كانت R و la bobine، و l'équation: L dé i sur dé t، plus R plus r fois i، égale zéro. هنا la maille هي R un و la bobine، إذن نفس l'équation مع R un. la solution: I zéro exponentielle de moins t sur tau prime. كنعوضو: tau prime égale L sur R un plus r. فالتمرين: zéro virgule cinq sur deux cent cinquante، كتعطي deux millisecondes.",
      centre=[("τ' = L/(R₁ + r)", "tau prime égale L sur R un plus r"), ("τ' = 0,5/250 = 2·10⁻³ s = 2 ms", "كتعطي deux millisecondes")],
      pointage=[{"mot": "فالدرس، la maille ديال la rupture", "commande": "play_until", "parametres": {"moment": "circuit"}},
                {"mot": "و l'équation", "commande": "play_until", "parametres": {"moment": "resultat"}},
                {"mot": "la solution", "commande": "play_until", "parametres": {"moment": "fin"}},
                {"mot": "tau prime égale L sur R un plus r", "cible": "centre:0"},
                {"mot": "كتعطي deux millisecondes", "cible": "centre:1"}]),
    diapo_sim("ex_rl7_4", "Question 4 : la surtension", "u_b(0⁺) = −R₁·I₀ : exemple du cours −1000 × 0,1 = −100 V ; ici −240 × 0,2 = −48 V.",
      DIODE, "Juste après l'ouverture : i = I₀ passe dans R₁, u_b = −R₁·I₀",
      "شوف المثال ديال الدرس: I zéro égale zéro virgule un ampère، و R un égale mille ohms. ملي كنحلو K، i ما كتنقزش: i de zéro égale I zéro، و كتدوز ف R un. la maille كتعطي u b égale moins R un i. شوف la flèche ديال u b: moins mille fois zéro virgule un، moins cent volts. فالتمرين ديالنا، نفس العلاقة: moins deux cent quarante fois zéro virgule deux، يعني moins quarante-huit volts، quatre fois E.",
      centre=[("u_b(0⁺) = −R₁·I₀", "كتعطي u b égale moins R un i"), ("ici : u_b(0⁺) = −240 × 0,2 = −48 V", "يعني moins quarante-huit volts")],
      pointage=[{"mot": "شوف المثال ديال الدرس", "commande": "play_until", "parametres": {"moment": "diode"}},
                {"mot": "ملي كنحلو K", "commande": "play_until", "parametres": {"moment": "surtension"}},
                {"mot": "كتعطي u b égale moins R un i", "cible": "centre:0"},
                {"mot": "شوف la flèche ديال u b", "repere": "fleche_ub"},
                {"mot": "يعني moins quarante-huit volts", "cible": "centre:1"}]),
    diapo_sim("ex_rl7_5", "Question 5 : l'énergie de la bobine", "E_m = ½·L·I₀² = ½ × 0,5 × 0,2² = 0,01 J, dissipée par effet Joule dans R₁ et r.",
      SIM_RUP, "Le courant de 200 mA ne s'annule pas d'un coup : la bobine rend son énergie",
      "قبل ما نحلو K، i égale I zéro، deux cents milliampères، و la bobine فيها L égale zéro virgule cinq henry. l'énergie: E m égale un demi L I zéro au carré، un demi fois zéro virgule cinq fois zéro virgule deux au carré، يعني zéro virgule zéro un joule. شوف: le courant كينقص بشوية. la bobine كترجع l'énergie ديالها، و فالتمرين كتولي سخانة ف R un و ف r: l'effet Joule.",
      centre=[("E_m = ½·L·I₀² = ½ × 0,5 × 0,2² = 0,01 J", "يعني zéro virgule zéro un joule"), ("→ effet Joule dans R₁ et r", "l'effet Joule")],
      pointage=[{"mot": "la bobine فيها L égale zéro virgule cinq henry", "repere": "bobine"},
                {"mot": "يعني zéro virgule zéro un joule", "cible": "centre:0"},
                {"mot": "le courant كينقص بشوية", "commande": "play_until", "parametres": {"moment": "courbe_rupture"}},
                {"mot": "l'effet Joule", "cible": "centre:1"}]),
    diapo_sim("ex_rl7_6", "Question 6 : sans R₁, plus lent", "Plus la résistance de la maille est petite, plus τ est grand : τ'' = 0,5/10 = 50 ms.",
      INFL, "Exemple du cours : R plus grande, τ plus petit (2 ms → 1 ms)",
      "شوف المثال ديال الدرس: مع R égale cinquante ohms، tau égale deux millisecondes. مع R égale cent dix ohms، tau égale une milliseconde. كل ما كبرات la résistance، صغرات tau. دابا التلميذ بغا يحيد R un: la résistance ديال la maille كتولي غير r، dix ohms. إذن tau seconde égale zéro virgule cinq sur dix، cinquante millisecondes، كبر بزاف من deux millisecondes. التلميذ غالط.",
      centre=[("τ = L/(résistance de la maille)", "كل ما كبرات la résistance، صغرات tau"), ("τ'' = 0,5/10 = 50 ms ≫ τ' = 2 ms", "cinquante millisecondes")],
      pointage=[{"mot": "شوف المثال ديال الدرس", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "مع R égale cent dix ohms", "commande": "play_until", "parametres": {"moment": "R_double"}},
                {"mot": "كل ما كبرات la résistance، صغرات tau", "commande": "play_until", "parametres": {"moment": "comparer"}},
                {"mot": "cinquante millisecondes", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_rl7_1", "Plus facile : I₀", "سؤال ساهل على I zéro.",
      "E = 12 V, R = 50 Ω, r = 10 Ω, diode bloquée. I₀ vaut…",
      ["0,24 A", "0,2 A", "0,05 A"], 1, {
        "1": {"juste": rep("برافو! douze sur soixante، zéro virgule deux ampère.", "Juste : I₀ = 12/60 = 0,2 A.")},
        "0": {"1": rep("نسيتي la résistance ديال la bobine. عاود.", "Tu as oublié r. Réessaie."),
              "2": rep("الجواب هو zéro virgule deux ampère: E sur R plus r.", "Réponse : I₀ = E/(R + r) = 0,2 A.")},
        "2": {"1": rep("la diode bloquée: R un ما كيدوز فيها والو. عاود.", "La diode est bloquée : R₁ n'est pas traversée. Réessaie."),
              "2": rep("الجواب هو zéro virgule deux ampère. R un ما كتدخلش ملي la diode bloquée.", "Réponse : 0,2 A ; R₁ ne compte pas.")}},
      "E égale douze volts، R égale cinquante ohms، r égale dix ohms. I zéro vaut ?"),
    qcm_facile("fa_rl7_2", "Plus facile : la bonne maille", "سؤال ساهل: اختار l'équation من بعد ما كنحلو K.",
      "K ouvert, diode passante : i(t) dans la bobine vérifie…",
      ["L·di/dt + (R₁ + r)·i = 0", "L·di/dt + (R + r)·i = 0", "L·di/dt + (R₁ + r)·i = E"], 0, {
        "0": {"juste": rep("برافو! la maille: la bobine، R un و la diode، بلا générateur.", "Juste : maille bobine – R₁ – D, sans générateur.")},
        "1": {"1": rep("K محلول: R ما بقا كيدوز فيها والو. فين كيدوز le courant؟ عاود.", "K ouvert : R n'est plus traversée. Réessaie."),
              "2": rep("الجواب: L dé i sur dé t plus R un plus r fois i égale zéro.", "Réponse : L·di/dt + (R₁ + r)·i = 0.")},
        "2": {"1": rep("واش le générateur مازال فla maille؟ عاود.", "Le générateur est-il dans la maille ? Réessaie."),
              "2": rep("الجواب: على اليمين zéro، حيت le générateur برا la maille.", "Réponse : second membre nul.")}},
      "K ouvert، i vérifie quelle équation ?"),
    qcm_facile("fa_rl7_3", "Plus facile : τ'", "سؤال ساهل على tau prime.",
      "Après l'ouverture de K, la constante de temps est…",
      ["L/(R + r)", "L/(R + R₁ + r)", "L/(R₁ + r)"], 2, {
        "2": {"juste": rep("برافو! tau prime égale L sur R un plus r.", "Juste : τ' = L/(R₁ + r).")},
        "0": {"1": rep("هادي ديال l'établissement. من بعد ما حلينا K، R ما بقاتش فla maille. عاود.", "C'est τ de l'établissement. Réessaie."),
              "2": rep("الجواب هو L sur R un plus r.", "Réponse : τ' = L/(R₁ + r).")},
        "1": {"1": rep("R ما بقاتش فla maille ملي K محلول. عاود.", "R n'est plus dans la maille. Réessaie."),
              "2": rep("الجواب هو L sur R un plus r، بلا R.", "Réponse : τ' = L/(R₁ + r).")}},
      "Après l'ouverture de K، tau prime égale ?"),
    vrai_faux_facile("fa_rl7_4", "Plus facile : vrai ou faux", "سؤال ساهل على la surtension.",
      "I₀ = 0,2 A ; R₁ = 240 Ω ; E = 12 V.",
      [("Juste après l'ouverture, le courant dans la bobine vaut encore I₀.", True, "i est continue dans une bobine."),
       ("u_b(0⁺) = −R₁·I₀ = −48 V : en valeur absolue, c'est 4 fois E.", True, "C'est une surtension, limitée par R₁."),
       ("Juste après l'ouverture, u_b = E = 12 V.", False, "La maille ne contient plus le générateur : u_b = −R₁·i = −48 V.")]),
    qcm_facile("fa_rl7_5", "Plus facile : l'énergie", "سؤال ساهل على l'énergie.",
      "L = 0,5 H et I₀ = 0,2 A. E_m = ½·L·I₀² vaut…",
      ["0,01 J", "0,05 J", "0,1 J"], 0, {
        "0": {"juste": rep("برافو! un demi fois zéro virgule cinq fois zéro virgule zéro quatre، zéro virgule zéro un joule.", "Juste : ½ × 0,5 × 0,04 = 0,01 J.")},
        "1": {"1": rep("نسيتي le carré ديال I zéro. عاود.", "Tu as oublié le carré. Réessaie."),
              "2": rep("الجواب هو zéro virgule zéro un joule: I zéro au carré égale zéro virgule zéro quatre.", "Réponse : 0,01 J (I₀² = 0,04).")},
        "2": {"1": rep("نسيتي le carré و un demi. عاود.", "Il manque le ½ et le carré. Réessaie."),
              "2": rep("الجواب هو zéro virgule zéro un joule.", "Réponse : 0,01 J.")}},
      "L égale zéro virgule cinq henry، I zéro égale zéro virgule deux ampère. E m vaut ?"),
    qcm_facile("fa_rl7_6", "Plus facile : sans R₁", "سؤال ساهل: بلا R un، شنو كيوقع ل tau؟",
      "Si on supprime R₁ (diode seule), la constante de temps de la rupture devient…",
      ["plus petite", "plus grande", "la même"], 1, {
        "1": {"juste": rep("برافو! la résistance ديال la maille كتصغر، إذن tau كتكبر.", "Juste : la résistance de la maille diminue, τ augmente.")},
        "0": {"1": rep("tau égale L sur la résistance. إلى صغرات la résistance، شنو كيوقع ل tau؟ عاود.", "τ = L/(résistance) : si la résistance diminue… Réessaie."),
              "2": rep("الجواب: plus grande. tau seconde égale L sur r، cinquante millisecondes.", "Réponse : plus grande (τ'' = L/r = 50 ms).")},
        "2": {"1": rep("la résistance ديال la maille تبدلات، إذن tau تبدلات. عاود.", "La résistance de la maille a changé. Réessaie."),
              "2": rep("الجواب: plus grande، حيت بقات غير r فla maille.", "Réponse : plus grande.")}},
      "Si on supprime R un، la constante de temps devient ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage avec E = 10 V, R = 30 Ω, une bobine L = 0,4 H, r = 20 Ω, et R₁ = 380 Ω. K est fermé depuis longtemps ; à t = 0, on ouvre K.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale dix volts، R égale trente ohms، L égale zéro virgule quatre henry، r égale vingt ohms، و R un égale trois cent quatre-vingts ohms.",
      "figures": [montage("Figure : le montage")],
      "donnees": ["E = 10 V ; R = 30 Ω", "Bobine : L = 0,4 H ; r = 20 Ω", "R₁ = 380 Ω"],
      "questions": [
        question_semblable("1", "K étant fermé (régime permanent), expliquer pourquoi la diode est bloquée, puis calculer l'intensité I₀ du courant dans la bobine.",
          valeur("I₀", 0.2, "A", "I₀ = E/(R + r) = 10/50 = 0,2 A"), ["I₀ = E/(R + r)", "A"], ["I₀ = E/R"],
          corr([("1 : D en inverse, bloquée ; I₀ = E/(R + r) = 10/50", "I zéro égale E sur R plus r"), ("I₀ = 0,2 A", "zéro virgule deux ampère")],
               "la diode bloquée. I zéro égale E sur R plus r، يعني dix sur cinquante، كتعطي zéro virgule deux ampère.")),
        question_semblable("2", "Établir l'équation différentielle vérifiée par i(t) après l'ouverture de K.",
          phrase(ATT2), ["u_b + R₁·i = 0"], ["L·di/dt + (R + r)·i = 0"],
          corr([("2 : u_b + R₁·i = 0", "u b plus R un i égale zéro"), ("L·di/dt + (R₁ + r)·i = 0", "R un plus r fois i")],
               "u b plus R un i égale zéro. إذن L dé i sur dé t، plus R un plus r fois i، égale zéro.")),
        question_semblable("3", "Vérifier que i(t) = I₀·e^(−t/τ') est solution, exprimer τ' et calculer sa valeur (en ms).",
          valeur("τ'", 1, "ms", "τ' = L/(R₁ + r) = 0,4/400 = 10⁻³ s = 1 ms"), ["τ' = L/(R₁ + r)", "ms"], ["τ' = L/(R + r)"],
          corr([("3 : τ' = L/(R₁ + r) = 0,4/400", "tau prime égale L sur R un plus r"), ("τ' = 1 ms", "une milliseconde")],
               "tau prime égale L sur R un plus r: zéro virgule quatre sur quatre cents، يعني une milliseconde.")),
        question_semblable("4", "Calculer la tension u_b(0⁺) aux bornes de la bobine juste après l'ouverture de K. Comparer à E.",
          valeur("u_b(0⁺)", -76, "V", "u_b(0⁺) = −R₁·I₀ = −380 × 0,2 = −76 V"), ["u_b = −R₁·i", "V"], ["u_b(0⁺) = 0"],
          corr([("4 : u_b(0⁺) = −R₁·I₀ = −380 × 0,2", "u b égale moins R un fois I zéro"), ("u_b(0⁺) = −76 V (7,6 fois E en valeur absolue)", "moins soixante-seize volts")],
               "u b égale moins R un fois I zéro، يعني moins soixante-seize volts.")),
        question_semblable("5", "Calculer l'énergie E_m emmagasinée dans la bobine juste avant l'ouverture de K. Que devient-elle ensuite ?",
          valeur("E_m", 0.008, "J", "E_m = ½·L·I₀² = ½ × 0,4 × 0,2² = 8·10⁻³ J"), ["E_m = ½·L·i²", "J"], ["E_m = ½·L·I₀"],
          corr([("5 : E_m = ½ × 0,4 × 0,2² = 8·10⁻³ J", "huit fois dix puissance moins trois joule"), ("dissipée par effet Joule dans R₁ et r", "l'effet Joule")],
               "E m égale un demi L I zéro au carré، يعني huit fois dix puissance moins trois joule، و كتمشي سخانة ف R un و r: l'effet Joule.")),
        question_semblable("6", "Un élève propose de supprimer R₁ (diode seule) « pour que le courant s'annule plus vite ». Calculer la nouvelle constante de temps τ'' (en ms) et conclure.",
          valeur("τ''", 20, "ms", "τ'' = L/r = 0,4/20 = 0,02 s = 20 ms"), ["τ'' = L/r", "ms"], ["τ'' < τ'"],
          corr([("6 : τ'' = L/r = 0,4/20 = 20 ms", "tau seconde égale L sur r"), ("τ'' = 20 τ' : plus lent, l'élève a tort", "التلميذ غالط")],
               "tau seconde égale L sur r، يعني vingt millisecondes، كبر بزاف من tau prime. التلميذ غالط.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
