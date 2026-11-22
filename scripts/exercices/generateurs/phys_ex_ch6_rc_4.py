# Exercice de physique, ch. 6 (dipôle RC), niveau moyen n° 4 : la charge q(t) d'un condensateur ; équation en q,
# constantes A et τ, Q_m → C, τ par les 63 % → R, puis i(t) et i(0).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RC.json : cas_types « ed_autre_grandeur » (q : u_C = q/C,
#    i = dq/dt), « constantes_solution », « R_C_E_deduits » (Q_m = C·E, R = τ/C), « i_t » ; pièges « appliquer
#    τ = RC avec deux inconnues » (chercher d'abord C par Q_m = C·E), « projeter 0,63 sur la courbe », « s'arrêter à
#    A et τ sans réécrire la solution » ; erreurs_examen « A et τ » (dérivée de e^(−t/τ), « pour tout t »).
#  - nationaux : 2019 N et 2023 R (ED en q), 2016 N, 2017 R, 2019 N (A et τ), 2016 N, 2021 R, 2022 N (i(t), i(0)) ;
#    ici une autre courbe (q en mC, t en ms), la méthode des 63 % et la double vérification de i(0).
#  - cours phys_ch6_dipole_RC : rc_e4_q (figures.html?fig=fig_ed_q), rc_s2_remplacer / rc_s3_factoriser
#    (fig_resolution), rc_s7_q_i (quatre-courbes.html?vue=q_i, E = 12 V fixe, R et C réglables), rc_l2_pourcent
#    (courbe-charge.html?vue=pourcent) ; nos valeurs (E = 12 V, R = 500 Ω, C = 100 µF) y sont réglées.
#  - séries en ligne : recherche faite (Naceiri Mrabti « Série P6 », talamidi, moutamadris, alloschool), pages non
#    lisibles depuis cette session (domaines bloqués) : on s'appuie sur les sources du dépôt.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch6_rc_4"
SIMD = "/media/simulations/physics/dipole-rc-tableau/"


def montage(titre):
    return schema(titre, 8, 4.4,
        dipole([1, 0.8], [1, 3.6], "G", "E", pos="o"),
        fil([1, 3.6], [2, 3.6]),
        dipole([2, 3.6], [3.8, 3.6], "K", "K"),
        dipole([3.8, 3.6], [6.4, 3.6], "R", "R", pos="s"),
        fil([6.4, 3.6], [7, 3.6]),
        dipole([7, 3.6], [7, 0.8], "C", "C", pos="o"),
        fil([7, 0.8], [1, 0.8]),
        courant([5.1, 0.8], "g"),
        tension([7.6, 1.4], [7.6, 3.0], "u_C", pos="e"),
        tension([6.1, 4.15], [4.1, 4.15], "u_R", pos="n"),
        borne([7, 3.6], "A", "n"), borne([7, 0.8], "B", "s"))


def courbe_q(Qm_mC, tau_ms, tmax, pas, qmax, pas_q, titre):
    n = int(round(tmax / pas))
    nq = int(round(qmax / pas_q))
    return figure_courbe(titre, axe("t", 0, tmax + pas * 0.6, "ms", [i * pas for i in range(n + 1)]),
        axe("q", 0, qmax, "mC", [round(i * pas_q, 2) for i in range(nq + 1)]),
        [{"f": "courbe", "expr": f"{Qm_mC}*(1-exp(-x/{tau_ms}))", "de": 0, "a": tmax, "couleur": "orange", "texte": "q(t)", "texte_x": tmax * 0.3, "pos": "se"},
         {"f": "repere", "y": Qm_mC}],
        legende="Charge q(t) de l'armature A après la fermeture de K à t = 0 (le pointillé : l'asymptote).")


E, R, C = 12, 500, 100e-6
QM = C * E                       # 1,2·10⁻³ C
TAU = R * C                      # 0,05 s
I0 = E / R                       # 0,024 A
assert abs(QM - 1.2e-3) < 1e-12 and abs(TAU - 0.05) < 1e-12 and abs(I0 - 0.024) < 1e-12
assert abs(QM / TAU - I0) < 1e-12 and abs(0.63 * QM - 0.756e-3) < 1e-12
# semblable : E = 10 V, C = 200 µF, R = 400 Ω → Q_m = 2 mC, τ = 80 ms, i(0) = 25 mA
assert abs(200e-6 * 10 - 2e-3) < 1e-12 and abs(400 * 200e-6 - 0.08) < 1e-12 and abs(10 / 400 - 0.025) < 1e-12

ED_ATT = ("D'après la loi d'additivité des tensions : u_R + u_C = E, avec u_R = R·i = R·dq/dt et u_C = q/C. "
          "Donc R·dq/dt + q/C = E, soit R·C·dq/dt + q = C·E.")
AT_ATT = ("q = A(1 − e^(−t/τ)) donne dq/dt = (A/τ)·e^(−t/τ). On remplace : R·C·(A/τ)·e^(−t/τ) + A − A·e^(−t/τ) = C·E, "
          "soit A·e^(−t/τ)·(R·C/τ − 1) + A = C·E pour tout t. Donc R·C/τ − 1 = 0 et A = C·E : τ = R·C et A = C·E ; "
          "q(t) = C·E(1 − e^(−t/RC)).")
REG4 = {"commande": "set_parameters", "parametres": {"R_ohm": 500, "C_uF": 100}}
REGC = {"commande": "set_parameters", "parametres": {"R_ohm": 500, "C_uF": 100, "E": 12}}
def avec(d, mot):
    x = dict(d); x["mot"] = mot; return x

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RC", "cours": "phys_ch6_dipole_RC",
  "titre": "La charge q(t) : trouver C, R et i(0)", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir l'équation différentielle vérifiée par q(t)",
                  "Trouver A et τ pour que q = A(1 − e^(−t/τ)) soit solution",
                  "Exploiter une courbe q(t) : Q_m, τ par la méthode des 63 %",
                  "Déduire C, R et l'intensité initiale i(0)"],
  "enonce": {
    "intro": "On charge un condensateur de capacité C, initialement déchargé, à travers un conducteur ohmique de résistance R, à l'aide d'un générateur idéal de tension de force électromotrice E = 12 V (figure 1). À la date t = 0, on ferme K. Un système d'acquisition permet de tracer la charge q(t) de l'armature A du condensateur (figure 2). R et C sont inconnues.",
    "intro_dit": "دابا نقراو l'énoncé. كنشارجيو un condensateur، la capacité ديالو C، و فالبداية déchargé، عبر un conducteur ohmique، R، مع un générateur، E égale douze volts. هادي la figure un. فt égale zéro كنسدو K، ونرسمو la charge q ديال l'armature A، وهي la figure deux. R و C ما عارفينهومش.",
    "figures": [montage("Figure 1 : le montage"), courbe_q(1.2, 50, 300, 25, 1.4, 0.2, "Figure 2 : la charge q(t)")],
    "donnees": ["E = 12 V", "R et C inconnues", "1 mC = 10⁻³ C ; 1 ms = 10⁻³ s"],
    "questions": [
      question("1", "Établir l'équation différentielle vérifiée par la charge q(t).",
        "السؤال un: بين l'équation différentielle اللي كتحققها la charge q.",
        phrase(ED_ATT),
        ["u_R + u_C = E", "u_C = q/C", "i = dq/dt", "u_R = R·i"], ["u_C = C·q", "i = q/t"],
        [aide("Pars de la loi d'additivité des tensions, puis écris u_R et u_C en fonction de q seulement.",
              "بدا بl'additivité des tensions، ومن بعد كتب u R و u C غير بq."),
         aide("u_C = q/C et u_R = R·i = R·dq/dt ; remplace, puis multiplie toute l'équation par C.",
              "u C égale q sur C، و u R égale R fois dé q sur dé t. عوض، ومن بعد ضرب l'équation كاملة fois C.")],
        corr([("1 : d'après la loi d'additivité des tensions : u_R + u_C = E", "u R plus u C égale E"),
              ("u_R = R·i = R·dq/dt et u_C = q/C, donc R·dq/dt + q/C = E", "R dé q sur dé t، plus q sur C، égale E"),
              ("R·C·dq/dt + q = C·E", "R C dé q sur dé t، plus q، égale C fois E")],
             "السؤال un. d'après la loi d'additivité des tensions، u R plus u C égale E. u R égale R dé q sur dé t، و u C égale q sur C. إذن R dé q sur dé t، plus q sur C، égale E. كنضربو fois C: R C dé q sur dé t، plus q، égale C fois E."),
        "ex_q1", "fa_q1"),
      question("2", "La solution de cette équation s'écrit q(t) = A(1 − e^(−t/τ)). Trouver les expressions de A et de τ en fonction des paramètres du circuit.",
        "السؤال deux: la solution كتكتب q égale A، fois un moins exponentielle de moins t sur tau. لقا l'expression ديال A و ديال tau.",
        phrase(AT_ATT),
        ["dq/dt = (A/τ)·e^(−t/τ)", "pour tout t", "τ = R·C", "A = C·E"], ["dq/dt = −(A/τ)·e^(−t/τ)", "A = E"],
        [aide("Calcule d'abord dq/dt, puis remplace q et dq/dt dans R·C·dq/dt + q = C·E.",
              "حسب الأول dé q sur dé t، ومن بعد عوض q و la dérivée ديالها فl'équation."),
         aide("Regroupe les termes en e^(−t/τ) : A·e^(−t/τ)·(R·C/τ − 1) + A = C·E doit être vraie pour tout t.",
              "جمع les termes اللي فيهم l'exponentielle: A fois exponentielle، fois R C sur tau moins un، plus A، égale C E. هادي خاصها تكون صحيحة pour tout t.")],
        corr([("2 : dq/dt = (A/τ)·e^(−t/τ)", "dé q sur dé t égale A sur tau"),
              ("On remplace : A·e^(−t/τ)·(R·C/τ − 1) + A = C·E pour tout t", "pour tout t"),
              ("Donc R·C/τ − 1 = 0 et A = C·E : τ = R·C et A = C·E", "tau égale R C، و A égale C fois E"),
              ("q(t) = C·E(1 − e^(−t/RC))", "q égale C E، fois un moins exponentielle")],
             "السؤال deux. dé q sur dé t égale A sur tau، fois exponentielle de moins t sur tau. كنعوضو، وكنجمعو: A fois exponentielle، fois R C sur tau moins un، plus A، égale C E، pour tout t. إذن R C sur tau moins un égale zéro، و A égale C E. يعني tau égale R C، و A égale C fois E. و la solution: q égale C E، fois un moins exponentielle de moins t sur R C."),
        "ex_q2", "fa_q2"),
      question("3", "Déterminer graphiquement la charge maximale Q_m du condensateur, puis en déduire la valeur de la capacité C.",
        "السؤال trois: حدد مبيانيا la charge maximale Q m، ومن بعد استنتج la valeur ديال la capacité C.",
        valeur("C", 1e-4, "F", "Q_m = 1,2 mC ; Q_m = C·E donc C = Q_m/E = 1,2·10⁻³/12 = 1·10⁻⁴ F"),
        ["Q_m = C·E", "C = Q_m/E", "mC", "10⁻³", "F"], ["C = Q_m·E", "C = E/Q_m", "Q_m = 1,4 mC"],
        [aide("Quand t devient grand, la courbe se rapproche d'une droite horizontale (le pointillé) : quelle valeur de q lit-on ?",
              "ملي t كيكبر، la courbe كتقرب من خط أفقي، وهو le pointillé. شحال ديال q كنقراو؟"),
         aide("Au régime permanent, q = Q_m = A = C·E, donc C = Q_m/E ; écris Q_m en coulombs.",
              "فle régime permanent، q égale Q m égale C fois E. إذن C égale Q m sur E. كتب Q m بle coulomb.")],
        corr([("3 : l'asymptote donne Q_m = 1,2 mC = 1,2·10⁻³ C", "Q m égale un virgule deux millicoulomb"),
              ("Au régime permanent : Q_m = C·E, donc C = Q_m/E", "C égale Q m sur E"),
              ("A.N. : C = 1,2·10⁻³/12 = 1·10⁻⁴ F = 100 µF", "C égale dix puissance moins quatre farad")],
             "السؤال trois. l'asymptote كتعطي Q m égale un virgule deux millicoulomb. فle régime permanent، Q m égale C fois E، إذن C égale Q m sur E. يعني un virgule deux fois dix puissance moins trois، sur douze. C égale dix puissance moins quatre farad، يعني cent microfarads."),
        "ex_q3", "fa_q3"),
      question("4", "Déterminer la constante de temps τ par la méthode des 63 %, puis en déduire la valeur de la résistance R.",
        "السؤال quatre: حدد tau بla méthode ديال soixante-trois pour cent، ومن بعد استنتج la valeur ديال la résistance R.",
        valeur("R", 500, "Ω", "q(τ) = 0,63·Q_m = 0,756 mC ; on lit τ = 50 ms ; R = τ/C = 50·10⁻³/10⁻⁴ = 500 Ω"),
        ["q(τ) = 0,63·Q_m", "R = τ/C", "ms", "Ω"], ["projeter sur l'axe des q", "R = C/τ", "R = τ·C"],
        [aide("À t = τ, la charge vaut 63 % de sa valeur maximale. Calcule 0,63·Q_m, puis cherche cette valeur sur la courbe.",
              "فt égale tau، la charge كتكون à soixante-trois pour cent من Q m. حسب zéro virgule soixante-trois fois Q m، وقلب على هاد la valeur فla courbe."),
         aide("Horizontale à 0,756 mC jusqu'à la courbe, puis verticale vers l'axe des temps : on lit τ. Ensuite τ = R·C donne R = τ/C (τ en secondes).",
              "خط أفقي من zéro virgule sept cent cinquante-six millicoulomb حتى la courbe، ومن بعد عمودي لl'axe des temps: كتقرا tau. ومن بعد R égale tau sur C، و tau بla seconde.")],
        corr([("4 : à t = τ : q(τ) = 0,63·Q_m = 0,63 × 1,2 = 0,756 mC", "zéro virgule sept cent cinquante-six millicoulomb"),
              ("On projette sur la courbe puis sur l'axe des temps : τ = 50 ms", "tau égale cinquante millisecondes"),
              ("τ = R·C, donc R = τ/C = 50·10⁻³/10⁻⁴ = 500 Ω", "R égale cinq cents ohms")],
             "السؤال quatre. فt égale tau، q égale zéro virgule soixante-trois fois Q m، يعني zéro virgule sept cent cinquante-six millicoulomb. كنمشيو حتى la courbe، ومن بعد كنهبطو: tau égale cinquante millisecondes. tau égale R C، إذن R égale tau sur C، يعني cinquante fois dix puissance moins trois، sur dix puissance moins quatre. R égale cinq cents ohms."),
        "ex_q4", "fa_q4"),
      question("5", "Établir l'expression de l'intensité i(t), puis calculer sa valeur i(0) juste après la fermeture de K (en mA).",
        "السؤال cinq: بين l'expression ديال l'intensité i، ومن بعد حسب i de zéro، مباشرة من بعد ما كنسدو K، بle milliampère.",
        valeur("i(0)", 24, "mA", "i(t) = dq/dt = (C·E/τ)·e^(−t/τ) = (E/R)·e^(−t/RC) ; i(0) = E/R = 12/500 = 0,024 A = 24 mA"),
        ["i = dq/dt", "e⁰ = 1", "i(0) = E/R", "mA"], ["i(0) = 0", "i(0) = E/C", "i(0) = Q_m"],
        [aide("L'intensité est la dérivée de la charge : i = dq/dt. Dérive q(t) = C·E(1 − e^(−t/RC)).",
              "l'intensité هي la dérivée ديال la charge: i égale dé q sur dé t. شتق q égale C E، fois un moins exponentielle."),
         aide("Tu obtiens i(t) = (E/R)·e^(−t/RC). À t = 0, e⁰ = 1 : i(0) = E/R. Vérifie avec la pente à l'origine Q_m/τ.",
              "كتلقى i égale E sur R، fois exponentielle de moins t sur R C. فt égale zéro، exponentielle de zéro égale un، إذن i de zéro égale E sur R. تأكد ب Q m sur tau.")],
        corr([("5 : i = dq/dt = (C·E/τ)·e^(−t/τ) = (E/R)·e^(−t/RC)", "i égale E sur R، fois exponentielle"),
              ("À t = 0 : i(0) = E/R = 12/500", "i de zéro égale E sur R"),
              ("i(0) = 0,024 A = 24 mA (on retrouve Q_m/τ = 1,2·10⁻³/0,05 = 0,024 A)", "vingt-quatre milliampères")],
             "السؤال cinq. i égale dé q sur dé t، يعني C E sur tau، fois exponentielle de moins t sur tau. و C E sur R C égale E sur R، إذن i égale E sur R، fois exponentielle. فt égale zéro: i de zéro égale E sur R، يعني douze sur cinq cents، zéro virgule zéro vingt-quatre ampère، vingt-quatre milliampères. ونفس الشي ب Q m sur tau."),
        "ex_q5", "fa_q5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_q1", "Question 1 : l'équation en q", "u_C = q/C, i = dq/dt : R·C·dq/dt + q = C·E.",
      SIMD + "figures.html?fig=fig_ed_q", "On écrit tout avec q, puis on multiplie par C",
      "دابا l'équation ديال q. كنبداو ب deux relations: u C égale q sur C، و i égale dé q sur dé t. فl'additivité، u R plus u C égale E، كنعوضو: R dé q sur dé t، plus q sur C، égale E. ما بغيناش q sur C، إذن كنضربو fois C. النتيجة: R C dé q sur dé t، plus q، égale C fois E. فle régime permanent، dé q sur dé t égale zéro، إذن q égale C fois E.",
      centre=[("R·dq/dt + q/C = E", "R dé q sur dé t، plus q sur C، égale E"), ("R·C·dq/dt + q = C·E", "النتيجة: R C dé q sur dé t، plus q، égale C fois E")],
      pointage=[{"mot": "كنبداو ب deux relations", "commande": "play_until", "parametres": {"moment": "relations"}},
                {"mot": "كنعوضو", "commande": "play_until", "parametres": {"moment": "remplacer"}},
                {"mot": "R dé q sur dé t، plus q sur C، égale E", "cible": "centre:0"},
                {"mot": "كنضربو fois C", "commande": "play_until", "parametres": {"moment": "multiplier"}},
                {"mot": "النتيجة: R C dé q sur dé t، plus q، égale C fois E", "commande": "play_until", "parametres": {"moment": "resultat"}},
                {"mot": "النتيجة: R C dé q sur dé t، plus q، égale C fois E", "cible": "centre:1"}]),
    diapo_sim("ex_q2", "Question 2 : trouver A et τ", "Dériver, remplacer, factoriser par e^(−t/τ) : τ = R·C et A = C·E.",
      SIMD + "figures.html?fig=fig_resolution", "La même méthode que pour u_C : dériver, remplacer, factoriser, conclure",
      "la figure كتحل l'équation ديال u C، وحنا عندنا q. الطريقة هي هي، غير فاليمين C fois E بلاصة E. الخطوة الأولى، la forme: un moins exponentielle de moins t sur tau. الخطوة الثانية، la dérivée: A sur tau، fois exponentielle de moins t sur tau. الخطوة الثالثة، كنعوضو فl'équation. ومن بعد كنجمعو les termes اللي فيهم l'exponentielle. هادشي صحيح pour tout t، إذن R C sur tau moins un égale zéro، والباقي A égale C fois E. إذن tau égale R C، و A égale C fois E. وكنعاودو نكتبو la solution: q égale C E، fois un moins exponentielle de moins t sur R C.",
      centre=[("dq/dt = (A/τ)·e^(−t/τ)", "الخطوة الثانية، la dérivée"), ("τ = R·C ; A = C·E", "إذن tau égale R C، و A égale C fois E")],
      pointage=[{"mot": "الخطوة الأولى", "commande": "play_until", "parametres": {"moment": "forme"}},
                {"mot": "الخطوة الثانية، la dérivée", "commande": "play_until", "parametres": {"moment": "deriver"}},
                {"mot": "الخطوة الثانية، la dérivée", "cible": "centre:0"},
                {"mot": "الخطوة الثالثة", "commande": "play_until", "parametres": {"moment": "remplacer"}},
                {"mot": "كنجمعو les termes", "commande": "play_until", "parametres": {"moment": "factoriser"}},
                {"mot": "هادشي صحيح pour tout t", "commande": "play_until", "parametres": {"moment": "accolade"}},
                {"mot": "إذن tau égale R C، و A égale C fois E", "cible": "centre:1"},
                {"mot": "وكنعاودو نكتبو la solution", "commande": "play_until", "parametres": {"moment": "reecrire"}}]),
    diapo_sim("ex_q3", "Question 3 : Q_m puis C", "Q_m = C·E : C = Q_m/E = 1,2·10⁻³/12 = 10⁻⁴ F.",
      SIMD + "quatre-courbes.html?vue=q_i", "E = 12 V, R = 500 Ω, C = 100 µF : q(t) monte vers Q_m = C·E = 1,2 mC",
      "شوف la courbe ديال q en fonction de t. فt égale zéro، q égale zéro. ومن بعد q كتطلع، وكتقرب من la valeur maximale Q m. هنا E égale douze volts، و C égale cent microfarads، إذن Q m égale C fois E، يعني un virgule deux millicoulomb. فالسؤال، كنقراو Q m على l'asymptote، وكنحسبو C égale Q m sur E. un virgule deux fois dix puissance moins trois، sur douze، كتعطي dix puissance moins quatre farad.",
      centre=[("Q_m = C·E", "إذن Q m égale C fois E"), ("C = Q_m/E = 1,2·10⁻³/12 = 10⁻⁴ F", "كتعطي dix puissance moins quatre farad")],
      pointage=[avec(REG4, "شوف la courbe ديال q"),
                {"mot": "فt égale zéro، q égale zéro", "commande": "play_until", "parametres": {"moment": "q"}},
                {"mot": "وكتقرب من la valeur maximale Q m", "repere": "graphe_q"},
                {"mot": "إذن Q m égale C fois E", "repere": "expression_q"},
                {"mot": "إذن Q m égale C fois E", "cible": "centre:0"},
                {"mot": "كتعطي dix puissance moins quatre farad", "cible": "centre:1"}]),
    diapo_sim("ex_q4", "Question 4 : τ par les 63 %, puis R", "q = C·u_C : q et u_C ont la même allure ; à t = τ, 63 % de la valeur finale.",
      SIMD + "courbe-charge.html?vue=pourcent", "R = 500 Ω, C = 100 µF, E = 12 V : 63 % de la valeur finale à t = τ = 50 ms",
      "q égale C fois u C، إذن la courbe ديال q عندها نفس الشكل ديال u C. شوف u C: كتطلع حتى E égale douze volts. فt égale tau، كتكون à soixante-trois pour cent من la valeur finale. كنرسمو الخط الأفقي حتى la courbe، ومن بعد كنهبطو لl'axe des temps: tau égale cinquante millisecondes. فالسؤال، نفس الشي على q: zéro virgule soixante-trois fois Q m، يعني zéro virgule sept cent cinquante-six millicoulomb. ومن بعد R égale tau sur C، يعني cinquante fois dix puissance moins trois، sur dix puissance moins quatre: R égale cinq cents ohms.",
      centre=[("q(τ) = 0,63·Q_m = 0,756 mC → τ = 50 ms", "يعني zéro virgule sept cent cinquante-six millicoulomb"), ("R = τ/C = 50·10⁻³/10⁻⁴ = 500 Ω", "R égale cinq cents ohms")],
      pointage=[avec(REGC, "شوف u C"),
                {"mot": "كتطلع حتى E égale douze volts", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "كنرسمو الخط الأفقي", "commande": "play_until", "parametres": {"moment": "ligne_63"}},
                {"mot": "ومن بعد كنهبطو", "commande": "play_until", "parametres": {"moment": "projection"}},
                {"mot": "tau égale cinquante millisecondes", "repere": "tau"},
                {"mot": "يعني zéro virgule sept cent cinquante-six millicoulomb", "cible": "centre:0"},
                {"mot": "R égale cinq cents ohms", "cible": "centre:1"}]),
    diapo_sim("ex_q5", "Question 5 : i(t) et i(0)", "i = dq/dt = (E/R)·e^(−t/RC) ; i(0) = E/R = 24 mA.",
      SIMD + "quatre-courbes.html?vue=q_i", "i(t) est la pente de q(t) : maximale à t = 0, puis elle tend vers 0",
      "شوف q en fonction de t، و تحتها i en fonction de t. i égale dé q sur dé t: هي la pente ديال q. فالبداية la pente كبيرة، إذن i كبيرة. ومن بعد q كتقرب من Q m، la pente كتصغر، و i كتمشي نحو zéro. l'expression: i égale E sur R، fois exponentielle de moins t sur R C. فt égale zéro: i de zéro égale E sur R، يعني douze sur cinq cents، zéro virgule zéro vingt-quatre ampère، vingt-quatre milliampères.",
      centre=[("i(t) = (E/R)·e^(−t/RC)", "l'expression: i égale E sur R"), ("i(0) = E/R = 12/500 = 24 mA", "vingt-quatre milliampères")],
      pointage=[avec(REG4, "شوف q en fonction de t"),
                {"mot": "و تحتها i en fonction de t", "commande": "play_until", "parametres": {"moment": "i"}},
                {"mot": "هي la pente ديال q", "repere": "graphe_q"},
                {"mot": "i كتمشي نحو zéro", "repere": "graphe_i"},
                {"mot": "l'expression: i égale E sur R", "repere": "expression_i"},
                {"mot": "l'expression: i égale E sur R", "cible": "centre:0"},
                {"mot": "vingt-quatre milliampères", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_q1", "Plus facile : l'équation en q", "سؤال ساهل: اختار l'équation ديال q.",
      "Pendant la charge sous E, la charge q vérifie…",
      ["R·C·dq/dt + q = E", "R·C·dq/dt + q = C·E", "R·dq/dt + C·q = E"], 1, {
        "1": {"juste": rep("برافو! R dé q sur dé t، plus q sur C، égale E، ومن بعد كنضربو fois C.", "Juste : R·dq/dt + q/C = E, multipliée par C.")},
        "0": {"1": rep("قريب. ملي ضربنا fois C، حتى E تضربات. شنو كيولي فاليمين؟ عاود اختار.", "En multipliant par C, le second membre E est multiplié aussi. Réessaie."),
              "2": rep("الجواب هو R C dé q sur dé t، plus q، égale C fois E. فle régime permanent، q égale C fois E.", "Réponse : R·C·dq/dt + q = C·E (au régime permanent q = C·E).")},
        "2": {"1": rep("ما تقلقش. u C égale q sur C، ماشي C fois q. عاود اختار.", "u_C = q/C, pas C·q. Réessaie."),
              "2": rep("الجواب هو R C dé q sur dé t، plus q، égale C fois E، حيت u C égale q sur C.", "Réponse : R·C·dq/dt + q = C·E, car u_C = q/C.")}},
      "Pendant la charge, la charge q vérifie quelle équation ?"),
    vrai_faux_facile("fa_q2", "Plus facile : vrai ou faux", "سؤال ساهل على la solution: صحيح ولا غالط.",
      "q(t) = A(1 − e^(−t/τ)) est solution de R·C·dq/dt + q = C·E.",
      [("La constante A est égale à C·E : c'est la charge maximale Q_m.", True, "Quand t devient grand, e^(−t/τ) tend vers 0 et q tend vers A = C·E."),
       ("La constante de temps vaut τ = R/C.", False, "On trouve τ = R·C (le facteur R·C/τ − 1 doit être nul)."),
       ("La condition q(0) = 0 est vérifiée, car e⁰ = 1.", True, "q(0) = A(1 − 1) = 0 : le condensateur est déchargé à t = 0.")]),
    qcm_facile("fa_q3", "Plus facile : C à partir de Q_m", "سؤال ساهل: نحسبو C من Q m.",
      "Q_m = 1,2 mC et E = 12 V. La capacité C vaut…",
      ["1,44·10⁻² F", "1·10⁴ F", "1·10⁻⁴ F"], 2, {
        "2": {"juste": rep("مزيان! C égale Q m sur E، يعني un virgule deux fois dix puissance moins trois، sur douze.", "Juste : C = Q_m/E = 1,2·10⁻³/12 = 10⁻⁴ F.")},
        "0": {"1": rep("ما تقلقش. هنا ضربتي Q m فE. ولكن Q m égale C fois E، إذن C égale Q m sur E. عاود اختار.", "Tu as multiplié Q_m par E ; or C = Q_m/E. Réessaie."),
              "2": rep("الجواب هو dix puissance moins quatre farad. C égale Q m sur E.", "Réponse : C = Q_m/E = 10⁻⁴ F.")},
        "1": {"1": rep("قريب. قسمتي E على Q m، والعكس هو الصحيح. عاود اختار.", "Tu as calculé E/Q_m ; c'est l'inverse. Réessaie."),
              "2": rep("الجواب هو dix puissance moins quatre farad. C égale Q m sur E، ماشي E sur Q m.", "Réponse : C = Q_m/E = 10⁻⁴ F.")}},
      "Q m égale un virgule deux millicoulomb et E égale douze volts. La capacité C vaut ?"),
    qcm_facile("fa_q4", "Plus facile : la méthode des 63 %", "سؤال ساهل على la méthode ديال soixante-trois pour cent.",
      "Pour lire τ sur la courbe q(t) de charge, on trace l'horizontale q = 0,63·Q_m jusqu'à…",
      ["la courbe q(t), puis on descend sur l'axe des temps", "la tangente à l'origine", "l'axe des charges"], 0, {
        "0": {"juste": rep("برافو! الخط الأفقي حتى la courbe، ومن بعد كنهبطو لl'axe des temps، وكنقراو tau.", "Juste : horizontale jusqu'à la courbe, puis verticale vers l'axe des temps.")},
        "1": {"1": rep("ما تقلقش. la tangente كتصلح لطريقة أخرى. soixante-trois pour cent هي valeur ديال la courbe نفسها. عاود اختار.", "La tangente sert à une autre méthode ; 63 % est une valeur prise sur la courbe. Réessaie."),
              "2": rep("الجواب: حتى la courbe، ومن بعد l'axe des temps. هادي غلطة معروفة فالامتحان: projeter sur la tangente.", "Réponse : on projette sur la courbe (erreur classique : projeter sur la tangente).")},
        "2": {"1": rep("لا، الخط الأفقي كيبدا من l'axe des charges. خاصو يوصل لشي حاجة كتعطي t. عاود اختار.", "L'horizontale part de l'axe des charges ; elle doit rencontrer ce qui donne t. Réessaie."),
              "2": rep("الجواب: حتى la courbe q de t، ومن بعد كنهبطو لl'axe des temps باش نقراو tau.", "Réponse : jusqu'à la courbe, puis on descend sur l'axe des temps.")}},
      "Pour lire tau sur la courbe de charge, on trace l'horizontale zéro virgule soixante-trois fois Q m jusqu'à quoi ?"),
    qcm_facile("fa_q5", "Plus facile : l'intensité au départ", "سؤال ساهل على l'intensité فt égale zéro.",
      "Juste après la fermeture de K (le condensateur est déchargé), l'intensité i vaut…",
      ["0", "E/C", "E/R"], 2, {
        "2": {"juste": rep("مزيان! فt égale zéro، u C égale zéro، إذن u R égale E، و i de zéro égale E sur R. هي أكبر valeur.", "Juste : u_C(0) = 0, donc R·i(0) = E et i(0) = E/R (valeur maximale).")},
        "0": {"1": rep("ما تقلقش. le condensateur خاوي، ولكن le courant كيبدا كبير، حيت la pente ديال q كبيرة فالبداية. عاود اختار.", "Le condensateur est vide, mais la pente de q(t) est maximale au départ : i n'est pas nulle. Réessaie."),
              "2": rep("الجواب هو E sur R. i كتنقص من E sur R نحو zéro، ماشي العكس.", "Réponse : i(0) = E/R ; i diminue de E/R vers 0.")},
        "1": {"1": rep("قريب. E sur C ماشي intensité: شوف l'unité. فt égale zéro، u R égale E. عاود اختار.", "E/C n'est pas une intensité (unité). À t = 0, u_R = E. Réessaie."),
              "2": rep("الجواب هو E sur R، من la loi d'Ohm: R fois i de zéro égale E.", "Réponse : i(0) = E/R, car R·i(0) = E.")}},
      "Juste après la fermeture de K, l'intensité i vaut ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec E = 10 V ; R et C sont inconnues. Le condensateur est initialement déchargé ; à t = 0, on ferme K. La figure 2 donne la charge q(t).",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale dix volts، و R و C ما عارفينهومش. فt égale zéro كنسدو K، و la figure deux كتعطي q en fonction de t.",
      "figures": [courbe_q(2, 80, 480, 40, 2.4, 0.4, "Figure 2 : la charge q(t)")],
      "donnees": ["E = 10 V"],
      "questions": [
        question_semblable("1", "Établir l'équation différentielle vérifiée par q(t).",
          phrase(ED_ATT), ["u_C = q/C", "i = dq/dt"], ["u_C = C·q"],
          corr([("1 : u_R + u_C = E, u_R = R·dq/dt, u_C = q/C", "u R plus u C égale E"), ("R·C·dq/dt + q = C·E", "R C dé q sur dé t، plus q، égale C fois E")],
               "u R plus u C égale E، مع u R égale R dé q sur dé t، و u C égale q sur C. إذن R C dé q sur dé t، plus q، égale C fois E.")),
        question_semblable("2", "La solution s'écrit q(t) = A(1 − e^(−t/τ)). Trouver A et τ.",
          phrase(AT_ATT), ["dq/dt = (A/τ)·e^(−t/τ)", "pour tout t"], ["A = E"],
          corr([("2 : A·e^(−t/τ)·(R·C/τ − 1) + A = C·E pour tout t", "pour tout t"), ("τ = R·C ; A = C·E", "tau égale R C، و A égale C fois E")],
               "كنعوضو وكنجمعو، pour tout t. إذن tau égale R C، و A égale C fois E.")),
        question_semblable("3", "Déterminer Q_m, puis en déduire C.",
          valeur("C", 2e-4, "F", "Q_m = 2 mC ; C = Q_m/E = 2·10⁻³/10 = 2·10⁻⁴ F"), ["C = Q_m/E", "F"], ["C = Q_m·E"],
          corr([("3 : Q_m = 2 mC ; C = Q_m/E", "C égale Q m sur E"), ("C = 2·10⁻³/10 = 2·10⁻⁴ F", "deux fois dix puissance moins quatre farad")],
               "Q m égale deux millicoulombs. C égale Q m sur E، يعني deux fois dix puissance moins trois، sur dix. C égale deux fois dix puissance moins quatre farad.")),
        question_semblable("4", "Déterminer τ par la méthode des 63 %, puis en déduire R.",
          valeur("R", 400, "Ω", "q(τ) = 0,63 × 2 = 1,26 mC ; τ = 80 ms ; R = τ/C = 80·10⁻³/(2·10⁻⁴) = 400 Ω"), ["q(τ) = 0,63·Q_m", "R = τ/C"], ["R = τ·C"],
          corr([("4 : 0,63·Q_m = 1,26 mC, on lit τ = 80 ms", "tau égale quatre-vingts millisecondes"), ("R = τ/C = 80·10⁻³/(2·10⁻⁴) = 400 Ω", "R égale quatre cents ohms")],
               "zéro virgule soixante-trois fois deux، un virgule vingt-six millicoulomb، كنقراو tau égale quatre-vingts millisecondes. R égale tau sur C، R égale quatre cents ohms.")),
        question_semblable("5", "Établir l'expression de i(t), puis calculer i(0) (en mA).",
          valeur("i(0)", 25, "mA", "i(t) = (E/R)·e^(−t/RC) ; i(0) = E/R = 10/400 = 0,025 A = 25 mA"), ["i = dq/dt", "i(0) = E/R"], ["i(0) = 0"],
          corr([("5 : i = dq/dt = (E/R)·e^(−t/RC)", "i égale E sur R، fois exponentielle"), ("i(0) = E/R = 10/400 = 25 mA", "vingt-cinq milliampères")],
               "i égale dé q sur dé t، يعني i égale E sur R، fois exponentielle de moins t sur R C. i de zéro égale dix sur quatre cents، vingt-cinq milliampères.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
