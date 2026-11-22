# Exercice de physique, ch. 6 (dipôle RC), niveau moyen n° 5 : la décharge (inverseur K en position 2) ;
# continuité de u_C, équation de décharge, A et τ, τ par les 37 %, i(t) négatif, énergie dissipée.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RC.json : cas_types « ed_decharge », « constantes_solution »,
#    « tau_graphique » (décharge → 0,37), « energie » ; pièges « prendre u_C(0) = 0 en décharge », « i positif en
#    décharge », « oublier le carré dans ½·C·u_C² » ; erreurs_examen « décharge » (C.I. et signe de i, Laksabi),
#    « τ graphique » (63 % utilisé en décharge).
#  - nationaux : 2018 N (décharge RC, i = −dq/dt dans le corrigé), décharge dans un RL / RLC dans plusieurs sujets,
#    2023 R (énergie) ; ici le même sens de i qu'à la charge (comme le cours, rc_e6_decharge), d'où i < 0.
#  - cours phys_ch6_dipole_RC : rc_d2_continuite et rc_d3_decharge_qi (continuite.html, vues enchaine / decharge,
#    réglable E, R_ohm, C_uF), rc_e6_decharge (fig_ed_decharge), rc_d1_decharge (fig_decharge_solution),
#    rc_l8_calcul (energie.html?vue=calcul, réglable u_C, C_uF) ; nos valeurs (E = 10 V, R = 2 kΩ, C = 50 µF) y sont réglées.
#  - séries en ligne : recherche faite (Naceiri Mrabti « Série P6 », talamidi, moutamadris, alloschool), pages non
#    lisibles depuis cette session (domaines bloqués) : on s'appuie sur les sources du dépôt.
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch6_rc_5"
SIMD = "/media/simulations/physics/dipole-rc-tableau/"


def montage(titre):
    """K en position 1 : E, R, C en série (charge) ; K en position 2 : R et C seuls (décharge).
    Le sens positif de i est celui de la charge (vers l'armature A)."""
    return schema(titre, 8.2, 4.8,
        dipole([1, 0.8], [1, 3.8], "G", "E", pos="o"),
        fil([1, 3.8], [2.2, 3.8]),
        inverseur([3.2, 3.8], [2.2, 3.8], [2.5, 2.7], None, "K", pos_t=[3.3, 3.25]),
        fil([2.5, 2.7], [2.5, 0.8]),
        borne([2.5, 0.8], ""),
        dipole([3.2, 3.8], [5.6, 3.8], "R", "R", pos="s"),
        fil([5.6, 3.8], [6.8, 3.8]),
        dipole([6.8, 3.8], [6.8, 0.8], "C", "C", pos="o"),
        fil([6.8, 0.8], [1, 0.8]),
        courant([6.3, 3.8], "d"),
        tension([5.3, 4.35], [3.5, 4.35], "u_R", pos="n"),
        tension([7.4, 1.4], [7.4, 3.2], "u_C", pos="e"),
        borne([6.8, 3.8], "A", "n"), borne([6.8, 0.8], "B", "s"))


def decharge(E, tau, tmax, pas_t, pas_u, titre):
    n = int(round(tmax / pas_t)); nu = int(round(E / pas_u))
    return figure_courbe(titre, axe("t", 0, round(tmax + pas_t * 0.6, 3), "s", [round(i * pas_t, 3) for i in range(n + 1)]),
        axe("u_C", 0, E * 1.15, "V", [round(i * pas_u, 2) for i in range(nu + 1)]),
        [{"f": "courbe", "expr": f"{E}*exp(-x/{tau})", "de": 0, "a": tmax, "couleur": "bleu", "texte": "u_C(t)", "texte_x": tau * 2.2, "pos": "ne"}],
        legende="Décharge : u_C(t) enregistrée après le passage de K en position 2 à t = 0.")


E, R, C = 10, 2e3, 50e-6
TAU = R * C                      # 0,1 s
U37 = 0.37 * E                   # 3,7 V
I0 = -E / R                      # −5·10⁻³ A
EE = 0.5 * C * E ** 2            # 2,5·10⁻³ J
assert abs(TAU - 0.1) < 1e-12 and abs(U37 - 3.7) < 1e-12 and abs(I0 + 5e-3) < 1e-12 and abs(EE - 2.5e-3) < 1e-12
assert abs(E * math.exp(-1) - U37) / U37 < 0.01          # 0,37·E ≈ E·e⁻¹
# semblable : E = 6 V, R = 4 kΩ, C = 50 µF → τ = 0,2 s ; i(0) = −1,5 mA ; E_e = 9·10⁻⁴ J
assert abs(4e3 * 50e-6 - 0.2) < 1e-12 and abs(-6 / 4e3 + 1.5e-3) < 1e-12 and abs(0.5 * 50e-6 * 36 - 9e-4) < 1e-12

ED_ATT = ("K en position 2 : il n'y a plus de générateur. D'après la loi d'additivité des tensions : u_R + u_C = 0, "
          "avec u_R = R·i et i = dq/dt = C·du_C/dt. Donc R·C·du_C/dt + u_C = 0.")
AT_ATT = ("u_C = A·e^(−t/τ) donne du_C/dt = −(A/τ)·e^(−t/τ). On remplace : −R·C·(A/τ)·e^(−t/τ) + A·e^(−t/τ) = 0, "
          "soit A·e^(−t/τ)·(1 − R·C/τ) = 0 pour tout t. A·e^(−t/τ) n'est pas nul, donc τ = R·C. "
          "Condition initiale : u_C(0) = A = E. Donc u_C(t) = E·e^(−t/RC).")
REG = {"commande": "set_parameters", "parametres": {"E": 10, "R_ohm": 2000, "C_uF": 50}}
REGE = {"commande": "set_parameters", "parametres": {"u_C": 10, "C_uF": 50}}
def avec(d, mot):
    x = dict(d); x["mot"] = mot; return x

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RC", "cours": "phys_ch6_dipole_RC",
  "titre": "La décharge : K en position 2", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Utiliser la continuité de u_C (condition initiale de la décharge)",
                  "Établir l'équation différentielle de la décharge et trouver A et τ",
                  "Déterminer τ par la méthode des 37 %",
                  "Exprimer i(t) en décharge et interpréter son signe",
                  "Calculer l'énergie E_e = ½·C·u_C²"],
  "enonce": {
    "intro": "On réalise le montage de la figure 1 : un générateur idéal de tension (E = 10 V), un conducteur ohmique de résistance R = 2 kΩ, un condensateur de capacité C = 50 µF et un inverseur K. L'inverseur est d'abord en position 1 assez longtemps pour que le condensateur soit complètement chargé. À la date t = 0, on bascule K en position 2. Le sens positif choisi pour i est indiqué sur la figure 1. La figure 2 donne u_C(t) pendant la décharge.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا le montage ديال la figure un: un générateur، E égale dix volts، un conducteur ohmique، R égale deux kiloohms، un condensateur، C égale cinquante microfarads، و l'interrupteur K، عندو deux positions. الأول K فla position un، حتى تشارجا le condensateur مزيان. فt égale zéro، كنديرو K فla position deux. le sens ديال i مرسوم فla figure un. و la figure deux كتعطي u C فla décharge.",
    "figures": [montage("Figure 1 : le montage à inverseur"), decharge(10, 0.1, 0.6, 0.05, 1, "Figure 2 : la décharge u_C(t)")],
    "donnees": ["E = 10 V", "R = 2 kΩ = 2·10³ Ω", "C = 50 µF = 50·10⁻⁶ F", "t = 0 : bascule de K de la position 1 à la position 2"],
    "questions": [
      question("1", "Quelle est la valeur de u_C juste après la bascule de K en position 2 (t = 0) ? Justifier.",
        "السؤال un: شحال هي u C مباشرة من بعد ما K دازت لla position deux، فt égale zéro؟ علل.",
        valeur("u_C(0)", 10, "V", "La tension aux bornes d'un condensateur est continue ; à la fin de la charge u_C = E, donc u_C(0) = E = 10 V"),
        ["continuité de u_C", "régime permanent", "u_C = E", "V"], ["u_C(0) = 0", "u_C(0) = 0,37·E"],
        [aide("Avant la bascule, la charge était finie : quelle était alors la tension u_C ? Peut-elle changer brusquement ?",
              "قبل ما نبدلو K، la charge كانت سالات: شحال كانت u C؟ واش تقدر تتبدل فجأة؟"),
         aide("u_C est continue (elle ne saute jamais) : sa valeur juste après la bascule est celle de la fin de la charge, E.",
              "u C continue، ما كتنقزش. إذن la valeur ديالها مباشرة من بعد هي la valeur ديال آخر la charge، يعني E.")],
        corr([("1 : en fin de charge (régime permanent) u_C = E", "u C égale E"),
              ("La tension aux bornes d'un condensateur est continue", "la tension ديال le condensateur continue"),
              ("donc u_C(0) = E = 10 V", "u C de zéro égale dix volts")],
             "السؤال un. فآخر la charge، u C égale E. و la tension ديال le condensateur continue، ما كتنقزش. إذن u C de zéro égale dix volts."),
        "ex_d1", "fa_d1"),
      question("2", "Montrer que l'équation différentielle vérifiée par u_C pendant la décharge s'écrit R·C·du_C/dt + u_C = 0.",
        "السؤال deux: بين بلي l'équation différentielle ديال u C فla décharge هي R C dé u C sur dé t، plus u C، égale zéro.",
        phrase(ED_ATT),
        ["u_R + u_C = 0", "u_R = R·i", "i = C·du_C/dt"], ["u_R + u_C = E", "i = −C·du_C/dt"],
        [aide("En position 2, le générateur n'est plus dans le circuit : la loi d'additivité s'écrit avec R et C seulement.",
              "فla position deux، le générateur خرج من le circuit. l'additivité كتكون غير ب R و C."),
         aide("u_R + u_C = 0, puis u_R = R·i avec i = C·du_C/dt (même sens de i qu'à la charge).",
              "u R plus u C égale zéro، ومن بعد u R égale R i، و i égale C dé u C sur dé t، بنفس le sens ديال la charge.")],
        corr([("2 : K en position 2, d'après la loi d'additivité : u_R + u_C = 0", "u R plus u C égale zéro"),
              ("u_R = R·i et i = dq/dt = C·du_C/dt", "i égale C dé u C sur dé t"),
              ("Donc R·C·du_C/dt + u_C = 0", "R C dé u C sur dé t، plus u C، égale zéro")],
             "السؤال deux. فla position deux، ما بقاش le générateur. l'additivité: u R plus u C égale zéro. u R égale R i، و i égale C dé u C sur dé t. إذن R C dé u C sur dé t، plus u C، égale zéro."),
        "ex_d2", "fa_d2"),
      question("3", "La solution de cette équation s'écrit u_C(t) = A·e^(−t/τ). Déterminer les expressions de A et de τ.",
        "السؤال trois: la solution كتكتب u C égale A fois exponentielle de moins t sur tau. حدد l'expression ديال A و ديال tau.",
        phrase(AT_ATT),
        ["du_C/dt = −(A/τ)·e^(−t/τ)", "pour tout t", "condition initiale"], ["A = 0", "du_C/dt = (A/τ)·e^(−t/τ)"],
        [aide("Dérive u_C = A·e^(−t/τ) (attention au signe moins), puis remplace dans l'équation de la question 2.",
              "شتق u C égale A fois exponentielle، ورد البال لle signe moins. ومن بعد عوض فl'équation ديال السؤال deux."),
         aide("Factorise par A·e^(−t/τ), qui n'est jamais nul : la parenthèse doit être nulle. Puis A vient de u_C(0) = E.",
              "خرج A fois exponentielle، وهي عمرها ما كتكون zéro: إذن la parenthèse égale zéro. ومن بعد A كتجي من u C de zéro égale E.")],
        corr([("3 : du_C/dt = −(A/τ)·e^(−t/τ)", "dé u C sur dé t égale moins A sur tau"),
              ("A·e^(−t/τ)·(1 − R·C/τ) = 0 pour tout t, et A·e^(−t/τ) ≠ 0, donc τ = R·C", "إذن tau égale R C"),
              ("u_C(0) = A = E, donc u_C(t) = E·e^(−t/RC)", "A égale E")],
             "السؤال trois. dé u C sur dé t égale moins A sur tau، fois exponentielle. كنعوضو: A fois exponentielle، fois un moins R C sur tau، égale zéro، pour tout t. A fois exponentielle ماشي zéro، إذن tau égale R C. و u C de zéro égale A، و هي E. إذن A égale E، و u C égale E fois exponentielle de moins t sur R C."),
        "ex_d3", "fa_d3"),
      question("4", "Déterminer graphiquement τ par la méthode des 37 %, puis vérifier le résultat avec les valeurs de R et C.",
        "السؤال quatre: حدد tau مبيانيا بla méthode ديال trente-sept pour cent، ومن بعد تأكد ب R و C.",
        valeur("τ", 0.1, "s", "u_C(τ) = 0,37·E = 3,7 V ; on lit τ = 0,1 s (R·C = 2·10³ × 50·10⁻⁶ = 0,1 s)"),
        ["u_C(τ) = 0,37·E", "projeter sur la courbe", "τ = R·C", "s"], ["u_C(τ) = 0,63·E", "τ = 0,6 s"],
        [aide("En décharge, à t = τ, u_C n'a plus que 37 % de sa valeur de départ E. Calcule cette tension.",
              "فla décharge، فt égale tau، u C كيبقى فيها غير trente-sept pour cent من E. حسب هاد la tension."),
         aide("Horizontale à 3,7 V jusqu'à la courbe, puis verticale vers l'axe des temps ; compare avec R·C.",
              "خط أفقي من trois virgule sept volts حتى la courbe، ومن بعد عمودي لl'axe des temps. ومن بعد قارن مع R fois C.")],
        corr([("4 : à t = τ : u_C(τ) = 0,37·E = 0,37 × 10 = 3,7 V", "trois virgule sept volts"),
              ("On projette sur la courbe puis sur l'axe des temps : τ = 0,1 s", "tau égale zéro virgule un seconde"),
              ("Vérification : τ = R·C = 2·10³ × 50·10⁻⁶ = 0,1 s", "R fois C كتعطي نفس القيمة")],
             "السؤال quatre. فt égale tau، u C égale zéro virgule trente-sept fois E، يعني trois virgule sept volts. كنمشيو حتى la courbe، وكنهبطو: tau égale zéro virgule un seconde. و R fois C كتعطي نفس القيمة: deux fois dix puissance trois، fois cinquante fois dix puissance moins six، zéro virgule un seconde."),
        "ex_d4", "fa_d4"),
      question("5", "Établir l'expression de i(t) pendant la décharge, calculer i(0) (en mA) et interpréter son signe.",
        "السؤال cinq: بين l'expression ديال i فla décharge، حسب i de zéro بle milliampère، و فسر le signe ديالها.",
        valeur("i(0)", -5, "mA", "i = C·du_C/dt = −(E/R)·e^(−t/RC) ; i(0) = −E/R = −10/(2·10³) = −5 mA : i < 0, le courant circule dans le sens contraire du sens choisi"),
        ["i = C·du_C/dt", "i(0) = −E/R", "signe de i", "mA"], ["i(0) = +5 mA", "i(0) = 0", "i = (E/R)·e^(−t/RC)"],
        [aide("i = C·du_C/dt : dérive u_C(t) = E·e^(−t/RC). Pendant la décharge, u_C diminue : quel est le signe de la dérivée ?",
              "i égale C dé u C sur dé t. شتق u C égale E fois exponentielle. فla décharge، u C كتنقص: شنو هو le signe ديال la dérivée؟"),
         aide("Tu obtiens i(t) = −(E/R)·e^(−t/RC) ; à t = 0, e⁰ = 1, donc i(0) = −E/R.",
              "كتلقى i égale moins E sur R، fois exponentielle. فt égale zéro، exponentielle de zéro égale un، إذن i de zéro égale moins E sur R.")],
        corr([("5 : i = C·du_C/dt = C·(−E/(RC))·e^(−t/RC) = −(E/R)·e^(−t/RC)", "i égale moins E sur R، fois exponentielle"),
              ("i(0) = −E/R = −10/(2·10³) = −5·10⁻³ A = −5 mA", "moins cinq milliampères"),
              ("i < 0 : le courant de décharge circule dans le sens contraire du sens positif choisi (celui de la charge).", "le courant كيدور فle sens المعاكس")],
             "السؤال cinq. i égale C dé u C sur dé t، يعني i égale moins E sur R، fois exponentielle de moins t sur R C. فt égale zéro: i de zéro égale moins dix sur deux mille، moins cinq milliampères. i négative: le courant كيدور فle sens المعاكس ديال le sens اللي اخترنا، يعني عكس la charge."),
        "ex_d5", "fa_d5"),
      question("6", "Calculer l'énergie électrique emmagasinée dans le condensateur à t = 0. Que devient cette énergie à la fin de la décharge ?",
        "السؤال six: حسب l'énergie électrique اللي مخزونة فle condensateur فt égale zéro. فين كتمشي هاد l'énergie فآخر la décharge؟",
        valeur("E_e", 2.5e-3, "J", "E_e = ½·C·u_C(0)² = ½·C·E² = ½ × 50·10⁻⁶ × 10² = 2,5·10⁻³ J ; à la fin de la décharge, u_C devient nulle : toute l'énergie est dissipée par effet Joule dans R"),
        ["E_e = ½·C·u_C²", "u_C(0) = E", "J", "effet Joule"], ["E_e = ½·C·u_C", "E_e = C·E²"],
        [aide("L'énergie d'un condensateur dépend de sa capacité et de sa tension. Quelle est la tension à t = 0 (question 1) ?",
              "l'énergie ديال le condensateur كتعلق ب la capacité و la tension. شحال هي la tension فt égale zéro، من السؤال un؟"),
         aide("E_e = ½·C·u_C² (n'oublie pas le carré) ; à la fin, u_C tend vers 0 : où est passée l'énergie ?",
              "E e égale un demi fois C fois u C au carré، ما تنساش le carré. فالآخر u C كتمشي نحو zéro: فين مشات l'énergie؟")],
        corr([("6 : E_e = ½·C·u_C², avec u_C(0) = E", "E e égale un demi fois C fois u C au carré"),
              ("A.N. : E_e = ½ × 50·10⁻⁶ × 10² = 2,5·10⁻³ J", "deux virgule cinq fois dix puissance moins trois joule"),
              ("À la fin, u_C → 0 : cette énergie a été dissipée par effet Joule dans le conducteur ohmique R.", "par effet Joule")],
             "السؤال six. E e égale un demi fois C fois u C au carré، و u C de zéro égale E. l'application numérique: un demi fois cinquante fois dix puissance moins six، fois dix au carré. E e égale deux virgule cinq fois dix puissance moins trois joule. فالآخر u C كتولي zéro: l'énergie كلها تصرفات فla résistance، par effet Joule."),
        "ex_d6", "fa_d6"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_d1", "Question 1 : u_C ne saute pas", "À la bascule, u_C reste à E = 10 V, puis descend.",
      SIMD + "continuite.html?vue=enchaine", "E = 10 V, R = 2 kΩ, C = 50 µF : la charge, la bascule, puis la décharge",
      "شوف الفوق u C، و التحت i. الأول la charge: u C كتطلع حتى E égale dix volts. دابا K كتدوز لla position deux. كناخدو هنا une nouvelle origine des temps: t égale zéro فلحظة la bascule. شوف u C: ما نقزاتش. بقات dix volts، ومن بعد بدات كتهبط. la tension ديال le condensateur continue. إذن u C de zéro égale E، يعني dix volts، ماشي zéro.",
      centre=[("u_C(0) = E = 10 V", "يعني dix volts، ماشي zéro")],
      pointage=[avec(REG, "شوف الفوق u C"),
                {"mot": "الأول la charge", "commande": "play_until", "parametres": {"moment": "charge"}},
                {"mot": "دابا K كتدوز لla position deux", "commande": "play_until", "parametres": {"moment": "bascule"}},
                {"mot": "une nouvelle origine des temps", "commande": "play_until", "parametres": {"moment": "nouvelle_origine"}},
                {"mot": "شوف u C: ما نقزاتش", "commande": "play_until", "parametres": {"moment": "uC_continue"}},
                {"mot": "la tension ديال le condensateur continue", "repere": "uC_continue"},
                {"mot": "يعني dix volts، ماشي zéro", "cible": "centre:0"}]),
    diapo_sim("ex_d2", "Question 2 : l'équation de la décharge", "Sans générateur : u_R + u_C = 0, donc R·C·du_C/dt + u_C = 0.",
      SIMD + "figures.html?fig=fig_ed_decharge", "R et C seuls : le second membre devient 0",
      "K فla position deux. شوف le circuit: R و C بوحدهم، ما كاينش le générateur. l'additivité: u R plus u C égale zéro. نفس السطور ديال la charge: u R égale R i، و i égale C dé u C sur dé t. النتيجة: R C dé u C sur dé t، plus u C، égale zéro. حضي: كنخليو i فنفس le sens ديال la charge.",
      centre=[("u_R + u_C = 0", "u R plus u C égale zéro"), ("R·C·du_C/dt + u_C = 0", "النتيجة: R C dé u C sur dé t، plus u C، égale zéro")],
      pointage=[{"mot": "شوف le circuit", "commande": "play_until", "parametres": {"moment": "circuit"}},
                {"mot": "l'additivité", "commande": "play_until", "parametres": {"moment": "additivite"}},
                {"mot": "u R plus u C égale zéro", "cible": "centre:0"},
                {"mot": "النتيجة: R C dé u C sur dé t، plus u C، égale zéro", "commande": "play_until", "parametres": {"moment": "resultat"}},
                {"mot": "النتيجة: R C dé u C sur dé t، plus u C، égale zéro", "cible": "centre:1"}]),
    diapo_sim("ex_d3", "Question 3 : A et τ", "Dériver, remplacer : τ = R·C ; condition initiale : A = E.",
      SIMD + "figures.html?fig=fig_decharge_solution", "Dériver, remplacer, factoriser, puis la condition initiale",
      "كنجربو u C égale A fois exponentielle de moins t sur tau. la dérivée: moins A sur tau، fois exponentielle. كنعوضو فl'équation، وكنخرجو A fois exponentielle: A fois exponentielle، fois un moins R C sur tau، égale zéro. A fois exponentielle ماشي zéro، إذن tau égale R C. و la condition initiale: u C de zéro égale E، إذن A égale E. النتيجة: u C égale E fois exponentielle de moins t sur tau.",
      centre=[("τ = R·C", "إذن tau égale R C"), ("A = E : u_C(t) = E·e^(−t/τ)", "إذن A égale E")],
      pointage=[{"mot": "كنجربو u C égale A fois exponentielle", "commande": "play_until", "parametres": {"moment": "forme"}},
                {"mot": "la dérivée", "commande": "play_until", "parametres": {"moment": "deriver"}},
                {"mot": "كنعوضو فl'équation", "commande": "play_until", "parametres": {"moment": "remplacer"}},
                {"mot": "إذن tau égale R C", "commande": "play_until", "parametres": {"moment": "tau"}},
                {"mot": "إذن tau égale R C", "cible": "centre:0"},
                {"mot": "و la condition initiale", "commande": "play_until", "parametres": {"moment": "condition"}},
                {"mot": "إذن A égale E", "cible": "centre:1"},
                {"mot": "النتيجة: u C égale E fois exponentielle", "commande": "play_until", "parametres": {"moment": "resultat"}}]),
    diapo_sim("ex_d4", "Question 4 : τ par les 37 %", "0,37·E = 3,7 V : horizontale jusqu'à la courbe, puis verticale : τ = 0,1 s.",
      SIMD + "continuite.html?vue=decharge", "La décharge : 0,37·E jusqu'à la courbe, puis l'axe des temps",
      "شوف la décharge: u C كتبدا من E égale dix volts، وكتهبط نحو zéro. فt égale tau، كيبقى غير zéro virgule trente-sept fois E، يعني trois virgule sept volts. كنرسمو الخط الأفقي ديال trois virgule sept volts حتى la courbe، ومن تما كنهبطو لl'axe des temps: tau égale zéro virgule un seconde. ونفس النتيجة ب la tangente à l'origine: كتقطع l'axe des temps فtau. و R fois C: deux mille fois cinquante fois dix puissance moins six، zéro virgule un seconde.",
      centre=[("u_C(τ) = 0,37 × 10 = 3,7 V", "يعني trois virgule sept volts"), ("τ = 0,1 s = R·C", "tau égale zéro virgule un seconde")],
      pointage=[avec(REG, "شوف la décharge"),
                {"mot": "وكتهبط نحو zéro", "commande": "play_until", "parametres": {"moment": "decharge"}},
                {"mot": "يعني trois virgule sept volts", "cible": "centre:0"},
                {"mot": "كنرسمو الخط الأفقي", "commande": "play_until", "parametres": {"moment": "decharge_37"}},
                {"mot": "كنرسمو الخط الأفقي", "repere": "ligne_37"},
                {"mot": "tau égale zéro virgule un seconde", "repere": "tau"},
                {"mot": "tau égale zéro virgule un seconde", "cible": "centre:1"},
                {"mot": "ب la tangente à l'origine", "repere": "tangente"}]),
    diapo_sim("ex_d5", "Question 5 : i est négative", "i = C·du_C/dt < 0 : à la bascule, i saute de 0 à −E/R = −5 mA.",
      SIMD + "continuite.html?vue=enchaine", "u_C continue, mais i change de sens à la bascule",
      "شوف التحت i en fonction de t. فآخر la charge، i égale zéro. ملي K كتدوز لla position deux، i كتنقز لتحت: moins E sur R، يعني moins dix sur deux mille، moins cinq milliampères. علاش négative؟ i égale C dé u C sur dé t، و u C كتنقص، إذن la dérivée négative. le courant كيدور فle sens المعاكس. ومن بعد i كترجع نحو zéro: i égale moins E sur R، fois exponentielle de moins t sur tau.",
      centre=[("i(0) = −E/R = −5 mA", "moins cinq milliampères"), ("i(t) = −(E/R)·e^(−t/τ)", "i égale moins E sur R، fois exponentielle")],
      pointage=[avec(REG, "شوف التحت i en fonction de t"),
                {"mot": "فآخر la charge، i égale zéro", "commande": "play_until", "parametres": {"moment": "nouvelle_origine"}},
                {"mot": "i كتنقز لتحت", "commande": "play_until", "parametres": {"moment": "saut_i"}},
                {"mot": "moins cinq milliampères", "repere": "saut_i"},
                {"mot": "moins cinq milliampères", "cible": "centre:0"},
                {"mot": "i égale moins E sur R، fois exponentielle", "cible": "centre:1"}]),
    diapo_sim("ex_d6", "Question 6 : l'énergie du condensateur", "E_e = ½·C·E² = ½ × 50·10⁻⁶ × 10² = 2,5·10⁻³ J.",
      SIMD + "energie.html?vue=calcul", "C = 50 µF, u_C = 10 V : l'énergie stockée au début de la décharge",
      "le condensateur مشارجي: u C égale dix volts، و C égale cinquante microfarads. l'énergie ديالو: E e égale un demi fois C fois u C au carré. رد البال لle carré. un demi fois cinquante fois dix puissance moins six، fois cent. E e égale deux virgule cinq fois dix puissance moins trois joule. فla décharge، u C كتمشي vers zéro، إذن l'énergie كتمشي vers zéro: تصرفات كلها فla résistance، par effet Joule.",
      centre=[("E_e = ½·C·u_C²", "E e égale un demi fois C fois u C au carré"), ("E_e = ½ × 50·10⁻⁶ × 10² = 2,5·10⁻³ J", "E e égale deux virgule cinq fois dix puissance moins trois joule")],
      pointage=[avec(REGE, "le condensateur مشارجي"),
                {"mot": "l'énergie ديالو", "commande": "play_until", "parametres": {"moment": "regime_permanent"}},
                {"mot": "E e égale un demi fois C fois u C au carré", "repere": "formule"},
                {"mot": "E e égale un demi fois C fois u C au carré", "cible": "centre:0"},
                {"mot": "un demi fois cinquante", "repere": "calcul"},
                {"mot": "E e égale deux virgule cinq fois dix puissance moins trois joule", "repere": "resultat"},
                {"mot": "E e égale deux virgule cinq fois dix puissance moins trois joule", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_d1", "Plus facile : u_C à la bascule", "سؤال ساهل على la continuité ديال u C.",
      "Le condensateur est chargé sous E = 10 V. Juste après la bascule de K en position 2, u_C vaut…",
      ["0 V", "10 V", "3,7 V"], 1, {
        "1": {"juste": rep("برافو! u C continue، إذن كتبقى dix volts فلحظة la bascule.", "Juste : u_C est continue, u_C(0) = E = 10 V.")},
        "0": {"1": rep("ما تقلقش. le condensateur ما كيتفرغش فلحظة. u C ما كتنقزش. شحال كانت قبل؟ عاود اختار.", "Le condensateur ne se vide pas instantanément : u_C ne saute pas. Réessaie."),
              "2": rep("الجواب هو dix volts. u C continue: u C de zéro égale E. zéro هي غلطة معروفة فla décharge.", "Réponse : 10 V ; u_C(0) = 0 est l'erreur classique en décharge.")},
        "2": {"1": rep("قريب. trois virgule sept volts هي la valeur فt égale tau، ماشي فt égale zéro. عاود اختار.", "3,7 V est la valeur à t = τ, pas à t = 0. Réessaie."),
              "2": rep("الجواب هو dix volts. فt égale zéro، u C مازال égale E.", "Réponse : u_C(0) = E = 10 V.")}},
      "Le condensateur est chargé sous dix volts. Juste après la bascule en position deux, u C vaut ?"),
    qcm_facile("fa_d2", "Plus facile : l'équation de la décharge", "سؤال ساهل: اختار l'équation ديال la décharge.",
      "K en position 2 (R et C seuls). L'équation différentielle de u_C est…",
      ["R·C·du_C/dt + u_C = 0", "R·C·du_C/dt + u_C = E", "R·C·du_C/dt − u_C = 0"], 0, {
        "0": {"juste": rep("مزيان! ما كاينش le générateur، إذن u R plus u C égale zéro.", "Juste : sans générateur, u_R + u_C = 0.")},
        "1": {"1": rep("ما تقلقش. هادي ديال la charge. فla position deux، واش مازال E فle circuit؟ عاود اختار.", "C'est l'équation de la charge ; en position 2, E n'est plus dans le circuit. Réessaie."),
              "2": rep("الجواب هو R C dé u C sur dé t، plus u C، égale zéro. الفرق مع la charge غير فاليمين.", "Réponse : R·C·du_C/dt + u_C = 0 (seul le second membre change).")},
        "2": {"1": rep("قريب. l'additivité كتجمع: u R plus u C. ما كاينش moins. عاود اختار.", "L'additivité donne u_R + u_C = 0 : pas de signe moins. Réessaie."),
              "2": rep("الجواب هو R C dé u C sur dé t، plus u C، égale zéro.", "Réponse : R·C·du_C/dt + u_C = 0.")}},
      "K en position deux. L'équation différentielle de u C est ?"),
    vrai_faux_facile("fa_d3", "Plus facile : vrai ou faux", "سؤال ساهل على la solution ديال la décharge.",
      "u_C(t) = A·e^(−t/τ) est solution de R·C·du_C/dt + u_C = 0, avec u_C(0) = E.",
      [("A = E, car u_C(0) = A·e⁰ = A.", True, "La condition initiale de la décharge est u_C(0) = E, et e⁰ = 1."),
       ("A = 0, car le condensateur finit par se vider.", False, "u_C tend vers 0 à la fin, mais A est la valeur au départ : A = E."),
       ("En décharge aussi, τ = R·C.", True, "On trouve 1 − R·C/τ = 0, donc τ = R·C, comme à la charge.")]),
    qcm_facile("fa_d4", "Plus facile : décharge et 37 %", "سؤال ساهل على la décharge فt égale tau.",
      "Pendant la décharge depuis E, à la date t = τ, u_C vaut…",
      ["0,63·E", "0,37·E", "0"], 1, {
        "1": {"juste": rep("برافو! فla décharge، فt égale tau، كيبقى trente-sept pour cent من E.", "Juste : en décharge, u_C(τ) = 0,37·E.")},
        "0": {"1": rep("ما تقلقش. soixante-trois pour cent هي ديال la charge. هنا u C كتهبط. عاود اختار.", "63 % sert pour la charge ; ici u_C descend. Réessaie."),
              "2": rep("الجواب هو zéro virgule trente-sept fois E. la charge: soixante-trois، la décharge: trente-sept.", "Réponse : 0,37·E (charge → 0,63 ; décharge → 0,37).")},
        "2": {"1": rep("لا، فtau مازال le condensateur ما تفرغش. خاص environ cinq tau. عاود اختار.", "À τ, le condensateur n'est pas vide : il faut environ 5τ. Réessaie."),
              "2": rep("الجواب هو zéro virgule trente-sept fois E. u C كتوصل à zéro غير من بعد environ cinq tau.", "Réponse : 0,37·E ; u_C ≈ 0 seulement vers 5τ.")}},
      "Pendant la décharge, à t égale tau, u C vaut ?"),
    qcm_facile("fa_d5", "Plus facile : le signe de i", "سؤال ساهل على le signe ديال i فla décharge.",
      "On garde pour i le même sens positif qu'à la charge. Pendant la décharge, i est…",
      ["positive", "nulle", "négative"], 2, {
        "2": {"juste": rep("مزيان! i égale C dé u C sur dé t، و u C كتنقص، إذن i négative: le courant كيدور فالاتجاه المعاكس.", "Juste : i = C·du_C/dt < 0 car u_C diminue.")},
        "0": {"1": rep("ما تقلقش. فكر: u C كتنقص. شنو هو le signe ديال dé u C sur dé t؟ عاود اختار.", "u_C diminue : quel est le signe de du_C/dt ? Réessaie."),
              "2": rep("الجواب هو négative. q كتنقص، إذن dé q sur dé t négative، و i négative.", "Réponse : négative, car q diminue (dq/dt < 0).")},
        "1": {"1": rep("قريب. فآخر la décharge i كتولي zéro، ولكن فالبداية كاين un courant. عاود اختار.", "i tend vers 0 à la fin, mais un courant circule pendant la décharge. Réessaie."),
              "2": rep("الجواب هو négative. i كتبدا من moins E sur R، وكترجع نحو zéro.", "Réponse : négative ; i part de −E/R et remonte vers 0.")}},
      "Avec le même sens positif qu'à la charge, pendant la décharge, i est ?"),
    qcm_facile("fa_d6", "Plus facile : l'énergie stockée", "سؤال ساهل على l'énergie.",
      "C = 50 µF chargé sous u_C = 10 V. L'énergie emmagasinée vaut…",
      ["2,5·10⁻⁴ J", "2,5·10⁻³ J", "5·10⁻³ J"], 1, {
        "1": {"juste": rep("برافو! un demi fois cinquante fois dix puissance moins six، fois cent، كتعطي deux virgule cinq fois dix puissance moins trois joule.", "Juste : E_e = ½ × 50·10⁻⁶ × 10² = 2,5·10⁻³ J.")},
        "0": {"1": rep("ما تقلقش. نسيتي le carré ديال u C. عاود اختار.", "Tu as oublié le carré de u_C. Réessaie."),
              "2": rep("الجواب هو deux virgule cinq fois dix puissance moins trois joule. E e égale un demi C u C au carré.", "Réponse : E_e = ½·C·u_C² = 2,5·10⁻³ J (avec le carré).")},
        "2": {"1": rep("قريب. نسيتي un demi. عاود اختار.", "Tu as oublié le facteur ½. Réessaie."),
              "2": rep("الجواب هو deux virgule cinq fois dix puissance moins trois joule. ما تنساش un demi.", "Réponse : E_e = ½·C·u_C² = 2,5·10⁻³ J.")}},
      "C égale cinquante microfarads chargé sous dix volts. L'énergie emmagasinée vaut ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec E = 6 V, R = 4 kΩ et C = 50 µF. Le condensateur est chargé (K en position 1) ; à t = 0, on bascule K en position 2. La figure 2 donne u_C(t) pendant la décharge.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale six volts، R égale quatre kiloohms، و C égale cinquante microfarads. فt égale zéro، K كتدوز لla position deux.",
      "figures": [decharge(6, 0.2, 1.2, 0.1, 0.5, "Figure 2 : la décharge u_C(t)")],
      "donnees": ["E = 6 V", "R = 4 kΩ = 4·10³ Ω", "C = 50 µF = 50·10⁻⁶ F"],
      "questions": [
        question_semblable("1", "Quelle est la valeur de u_C juste après la bascule (t = 0) ? Justifier.",
          valeur("u_C(0)", 6, "V", "u_C est continue : u_C(0) = E = 6 V"), ["continuité de u_C"], ["u_C(0) = 0"],
          corr([("1 : u_C est continue ; en fin de charge u_C = E", "u C continue"), ("u_C(0) = E = 6 V", "six volts")],
               "u C continue، و فآخر la charge u C égale E. إذن u C de zéro égale six volts.")),
        question_semblable("2", "Montrer que R·C·du_C/dt + u_C = 0 pendant la décharge.",
          phrase(ED_ATT), ["u_R + u_C = 0", "i = C·du_C/dt"], ["u_R + u_C = E"],
          corr([("2 : u_R + u_C = 0 ; u_R = R·i ; i = C·du_C/dt", "u R plus u C égale zéro"), ("R·C·du_C/dt + u_C = 0", "R C dé u C sur dé t، plus u C، égale zéro")],
               "u R plus u C égale zéro، مع u R égale R i، و i égale C dé u C sur dé t. إذن R C dé u C sur dé t، plus u C، égale zéro.")),
        question_semblable("3", "La solution s'écrit u_C(t) = A·e^(−t/τ). Déterminer A et τ.",
          phrase(AT_ATT), ["pour tout t", "condition initiale"], ["A = 0"],
          corr([("3 : A·e^(−t/τ)·(1 − R·C/τ) = 0 pour tout t : τ = R·C", "tau égale R C"), ("u_C(0) = A = E", "A égale E")],
               "كنعوضو: A fois exponentielle، fois un moins R C sur tau، égale zéro، إذن tau égale R C. و u C de zéro égale A، إذن A égale E.")),
        question_semblable("4", "Déterminer τ par la méthode des 37 %, puis vérifier avec R et C.",
          valeur("τ", 0.2, "s", "u_C(τ) = 0,37 × 6 = 2,22 V ; on lit τ = 0,2 s (R·C = 4·10³ × 50·10⁻⁶ = 0,2 s)"), ["u_C(τ) = 0,37·E"], ["0,63·E"],
          corr([("4 : 0,37·E = 2,22 V ; on lit τ = 0,2 s", "tau égale zéro virgule deux seconde"), ("R·C = 4·10³ × 50·10⁻⁶ = 0,2 s", "R fois C")],
               "zéro virgule trente-sept fois six، deux virgule vingt-deux volts. كنقراو tau égale zéro virgule deux seconde. و R fois C كتعطي نفس القيمة.")),
        question_semblable("5", "Établir i(t), calculer i(0) (en mA) et interpréter son signe.",
          valeur("i(0)", -1.5, "mA", "i = −(E/R)·e^(−t/RC) ; i(0) = −E/R = −6/(4·10³) = −1,5 mA : i < 0, sens contraire du sens choisi"), ["i = C·du_C/dt", "i(0) = −E/R"], ["i(0) = +1,5 mA"],
          corr([("5 : i = C·du_C/dt = −(E/R)·e^(−t/RC)", "i égale moins E sur R"), ("i(0) = −6/(4·10³) = −1,5 mA < 0 : sens contraire", "moins un virgule cinq milliampère")],
               "i égale moins E sur R، fois exponentielle. i de zéro égale moins un virgule cinq milliampère: négative، le courant كيدور فle sens المعاكس.")),
        question_semblable("6", "Calculer l'énergie emmagasinée à t = 0. Que devient-elle à la fin de la décharge ?",
          valeur("E_e", 9e-4, "J", "E_e = ½·C·E² = ½ × 50·10⁻⁶ × 6² = 9·10⁻⁴ J ; elle est dissipée par effet Joule dans R"), ["E_e = ½·C·u_C²"], ["E_e = ½·C·u_C"],
          corr([("6 : E_e = ½·C·E² = ½ × 50·10⁻⁶ × 6²", "un demi fois C fois E au carré"), ("E_e = 9·10⁻⁴ J, dissipée par effet Joule dans R", "neuf fois dix puissance moins quatre joule")],
               "E e égale un demi fois C fois E au carré، يعني un demi fois cinquante fois dix puissance moins six، fois trente-six. E e égale neuf fois dix puissance moins quatre joule، و كتتصرف فla résistance par effet Joule.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
