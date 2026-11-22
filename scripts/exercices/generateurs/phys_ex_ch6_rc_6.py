# Exercice de physique, ch. 6 (dipôle RC), niveau difficile n° 6 : la charge suivie par u_R(t) ; équation en u_R,
# solution, E et τ lus sur une courbe sans tangente tracée, C, énergie à t = τ, date où l'énergie vaut la moitié.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RC.json : cas_types « ed_autre_grandeur » (u_R : dériver
#    l'additivité), « tau_graphique » (courbe qui descend → 0,37 ou tangente ∩ axe des temps), « R_C_E_deduits »
#    (E = u_R(0)), « energie » ; pièges « oublier le carré », « croire qu'à τ le condensateur est chargé »,
#    « oublier de convertir ms » ; erreurs_examen « énergie » (u_C prise égale à E hors du régime permanent).
#  - nationaux : 2024 R (ED en u_R), 2021 R (i(t), ED en i), 2023 R (énergie) ; ici au-dessus du national : la courbe
#    u_R(t) sans tangente tracée, u_C(τ) à déduire de l'additivité, puis une date calculée avec ln (énergie moitié).
#  - cours phys_ch6_dipole_RC : rc_e5_uR_i (figures.html?fig=fig_ed_uR_i), rc_d1_decharge (fig_decharge_solution, même
#    forme A·e^(−t/τ)), rc_l3_descente (quatre-courbes.html?vue=descente), rc_s8_quatre (vue uC_uR), rc_l8_calcul
#    (energie.html?vue=calcul : a_tau, reste_70) ; nos valeurs (E = 12 V, R = 200 Ω, C = 150 µF) y sont réglées.
#  - séries en ligne : recherche faite (Naceiri Mrabti « Série P6 », talamidi, moutamadris, alloschool), pages non
#    lisibles depuis cette session (domaines bloqués) : on s'appuie sur les sources du dépôt.
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch6_rc_6"
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


def courbe_uR(E, tau_ms, tmax, pas, titre):
    n = int(round(tmax / pas))
    return figure_courbe(titre, axe("t", 0, tmax + pas * 0.6, "ms", [i * pas for i in range(n + 1)]),
        axe("u_R", 0, E * 1.15, "V", list(range(0, E + 1))),
        [{"f": "courbe", "expr": f"{E}*exp(-x/{tau_ms})", "de": 0, "a": tmax, "couleur": "orange", "texte": "u_R(t)", "texte_x": tau_ms * 2.2, "pos": "ne"}],
        legende="Tension u_R(t) aux bornes du conducteur ohmique, après la fermeture de K à t = 0.")


E, R, C = 12, 200, 150e-6
TAU = R * C                                   # 0,03 s
UC_TAU = 0.63 * E                             # 7,56 V
EE_TAU = 0.5 * C * UC_TAU ** 2                # 4,29·10⁻³ J
T1 = TAU * math.log(1 / (1 - 1 / math.sqrt(2)))   # 36,8 ms
assert abs(TAU - 0.03) < 1e-12 and abs(C - TAU / R) < 1e-15
assert abs(EE_TAU - 4.287e-3) / 4.287e-3 < 1e-3 and abs(T1 * 1e3 - 36.8) < 0.05
assert abs(0.5 * C * (E * (1 - math.exp(-T1 / TAU))) ** 2 - 0.5 * (0.5 * C * E ** 2)) < 1e-9
# semblable : E = 9 V, R = 400 Ω, C = 100 µF → τ = 40 ms ; E_e(τ) = 1,61·10⁻³ J ; t₁ = 49,1 ms
assert abs(400 * 100e-6 - 0.04) < 1e-12 and abs(0.5 * 100e-6 * (0.63 * 9) ** 2 - 1.607e-3) < 1e-5
assert abs(40 * math.log(1 / (1 - 1 / math.sqrt(2))) - 49.1) < 0.05

ED_ATT = ("D'après la loi d'additivité : u_R + u_C = E. E est constante, on dérive : du_R/dt + du_C/dt = 0. "
          "Or i = C·du_C/dt et u_R = R·i, donc du_C/dt = i/C = u_R/(R·C). D'où du_R/dt + u_R/(R·C) = 0, soit R·C·du_R/dt + u_R = 0.")
SOL_ATT = ("u_R = E·e^(−t/τ) donne du_R/dt = −(E/τ)·e^(−t/τ). On remplace : E·e^(−t/τ)·(1 − R·C/τ) = 0 pour tout t, "
           "vérifiée si τ = R·C. À t = 0 : u_C(0) = 0 (condensateur déchargé) donc u_R(0) = E − u_C(0) = E, et E·e⁰ = E : "
           "la condition initiale est vérifiée.")
REGQ = {"commande": "set_parameters", "parametres": {"R_ohm": 200, "C_uF": 150}}
REGE = {"commande": "set_parameters", "parametres": {"u_C": 12, "C_uF": 150}}
def avec(d, mot):
    x = dict(d); x["mot"] = mot; return x

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RC", "cours": "phys_ch6_dipole_RC",
  "titre": "La charge vue par u_R(t), et l'énergie stockée", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir l'équation différentielle vérifiée par u_R",
                  "Vérifier une solution et sa condition initiale",
                  "Exploiter une courbe qui décroît : E et τ",
                  "Calculer l'énergie stockée à un instant donné",
                  "Déterminer une date avec la fonction ln"],
  "enonce": {
    "intro": "Un condensateur de capacité C, initialement déchargé, est chargé à travers un conducteur ohmique de résistance R = 200 Ω par un générateur idéal de tension de force électromotrice E (figure 1). À t = 0, on ferme K. Un système d'acquisition enregistre la tension u_R(t) aux bornes du conducteur ohmique (figure 2). E et C sont inconnues.",
    "intro_dit": "دابا نقراو l'énoncé. un condensateur، la capacité ديالو C، فالبداية déchargé، كنشارجيوه عبر un conducteur ohmique، R égale deux cents ohms، مع un générateur، E. هادي la figure un. فt égale zéro كنسدو K، و كنسجلو la tension u R ديال la résistance، وهي la figure deux. E و C ما عارفينهومش.",
    "figures": [montage("Figure 1 : le montage"), courbe_uR(12, 30, 180, 15, "Figure 2 : la tension u_R(t)")],
    "donnees": ["R = 200 Ω", "E et C inconnues", "1 ms = 10⁻³ s"],
    "questions": [
      question("1", "Montrer que la tension u_R vérifie l'équation différentielle R·C·du_R/dt + u_R = 0.",
        "السؤال un: بين بلي u R كتحقق l'équation différentielle R C dé u R sur dé t، plus u R، égale zéro.",
        phrase(ED_ATT),
        ["u_R + u_C = E", "dE/dt = 0", "du_C/dt = i/C", "u_R = R·i"], ["du_C/dt = u_R·R·C", "u_R + u_C = 0"],
        [aide("Écris la loi d'additivité, puis dérive-la par rapport au temps : que devient la dérivée de E ?",
              "كتب l'additivité، ومن بعد شتقها بالنسبة لle temps. شنو كتولي la dérivée ديال E؟"),
         aide("du_C/dt = i/C et i = u_R/R, donc du_C/dt = u_R/(R·C) ; remplace, puis multiplie par R·C.",
              "dé u C sur dé t égale i sur C، و i égale u R sur R. إذن dé u C sur dé t égale u R sur R C. عوض، ومن بعد ضرب fois R C.")],
        corr([("1 : u_R + u_C = E ; E constante, on dérive : du_R/dt + du_C/dt = 0", "dé u R sur dé t plus dé u C sur dé t égale zéro"),
              ("du_C/dt = i/C = u_R/(R·C)", "dé u C sur dé t égale u R sur R C"),
              ("Donc R·C·du_R/dt + u_R = 0", "R C dé u R sur dé t، plus u R، égale zéro")],
             "السؤال un. u R plus u C égale E. E ثابتة، كنشتقو: dé u R sur dé t plus dé u C sur dé t égale zéro. و dé u C sur dé t égale i sur C، يعني dé u C sur dé t égale u R sur R C. إذن R C dé u R sur dé t، plus u R، égale zéro."),
        "ex_r1", "fa_r1"),
      question("2", "Vérifier que u_R(t) = E·e^(−t/τ) est solution de cette équation si τ = R·C, et justifier que u_R(0) = E.",
        "السؤال deux: تأكد بلي u R égale E fois exponentielle de moins t sur tau، solution إلى كان tau égale R C، و علل بلي u R de zéro égale E.",
        phrase(SOL_ATT),
        ["du_R/dt = −(E/τ)·e^(−t/τ)", "pour tout t", "u_C(0) = 0", "u_R(0) = E − u_C(0)"], ["u_R(0) = 0", "du_R/dt = (E/τ)·e^(−t/τ)"],
        [aide("Dérive u_R(t) (attention au signe), remplace dans l'équation et factorise par E·e^(−t/τ).",
              "شتق u R، ورد البال لle signe. عوض فl'équation، وخرج E fois exponentielle."),
         aide("Pour la condition initiale : à t = 0 le condensateur est déchargé, u_C(0) = 0 ; utilise l'additivité.",
              "la condition initiale: فt égale zéro le condensateur déchargé، u C de zéro égale zéro. استعمل l'additivité.")],
        corr([("2 : du_R/dt = −(E/τ)·e^(−t/τ)", "dé u R sur dé t égale moins E sur tau"),
              ("On remplace : E·e^(−t/τ)·(1 − R·C/τ) = 0 pour tout t : vraie si τ = R·C", "vraie si tau égale R C"),
              ("u_C(0) = 0, donc u_R(0) = E − u_C(0) = E = E·e⁰", "u R de zéro égale E")],
             "السؤال deux. dé u R sur dé t égale moins E sur tau، fois exponentielle. كنعوضو: E fois exponentielle، fois un moins R C sur tau، égale zéro، pour tout t. هادي vraie si tau égale R C. و فt égale zéro، u C de zéro égale zéro، إذن u R de zéro égale E، و E fois exponentielle de zéro égale E."),
        "ex_r2", "fa_r2"),
      question("3", "Exploiter la figure 2 pour déterminer la force électromotrice E et la constante de temps τ (en ms).",
        "السؤال trois: استغل la figure deux باش تحدد E و la constante de temps tau، بla milliseconde.",
        valeur("τ", 30, "ms", "E = u_R(0) = 12 V ; u_R(τ) = 0,37·E = 4,44 V, on lit τ = 30 ms"),
        ["E = u_R(0)", "u_R(τ) = 0,37·E", "tangente ∩ axe des temps", "ms"], ["u_R(τ) = 0,63·E", "E = u_R final"],
        [aide("Où lit-on E sur une courbe u_R(t) qui part de sa valeur maximale ? Puis, pour une courbe qui décroît, quel pourcentage utilise-t-on pour τ ?",
              "فين كنقراو E على la courbe ديال u R اللي كتبدا من القيمة الكبيرة؟ ومن بعد، لla courbe اللي كتهبط، شمن pour cent كنستعملو لtau؟"),
         aide("E = u_R(0). Puis u_R(τ) = 0,37·E : horizontale jusqu'à la courbe, puis verticale (ou tangente à l'origine jusqu'à l'axe des temps).",
              "E égale u R de zéro. ومن بعد u R de tau égale zéro virgule trente-sept fois E: خط أفقي حتى la courbe، ومن بعد عمودي. ولا la tangente à l'origine حتى l'axe des temps.")],
        corr([("3 : à t = 0, u_R(0) = E : on lit E = 12 V", "E égale douze volts"),
              ("u_R(τ) = 0,37·E = 0,37 × 12 = 4,44 V", "quatre virgule quarante-quatre volts"),
              ("On projette sur la courbe puis sur l'axe des temps : τ = 30 ms", "tau égale trente millisecondes")],
             "السؤال trois. فt égale zéro، u R de zéro égale E: كنقراو E égale douze volts. فt égale tau، u R égale zéro virgule trente-sept fois E، يعني quatre virgule quarante-quatre volts. كنمشيو حتى la courbe، وكنهبطو: tau égale trente millisecondes."),
        "ex_r3", "fa_r3"),
      question("4", "En déduire la valeur de la capacité C.",
        "السؤال quatre: استنتج la valeur ديال la capacité C.",
        valeur("C", 1.5e-4, "F", "C = τ/R = 30·10⁻³/200 = 1,5·10⁻⁴ F"),
        ["C = τ/R", "10⁻³", "F", "µF"], ["C = R·τ", "C = 30/200 = 0,15 F"],
        [aide("τ = R·C : tu connais τ et R. N'oublie pas de convertir τ en secondes.",
              "tau égale R C: عارف tau و R. ما تنساش تحول tau لla seconde."),
         aide("C = τ/R, avec τ = 30·10⁻³ s et R = 200 Ω.",
              "C égale tau sur R، مع tau égale trente fois dix puissance moins trois seconde، و R égale deux cents ohms.")],
        corr([("4 : τ = R·C donc C = τ/R", "C égale tau sur R"),
              ("A.N. : C = 30·10⁻³/200 = 1,5·10⁻⁴ F = 150 µF", "un virgule cinq fois dix puissance moins quatre farad")],
             "السؤال quatre. tau égale R C، إذن C égale tau sur R. trente fois dix puissance moins trois، sur deux cents. C égale un virgule cinq fois dix puissance moins quatre farad، يعني cent cinquante microfarads."),
        "ex_r4", "fa_r4"),
      question("5", "Calculer l'énergie électrique emmagasinée dans le condensateur à la date t = τ.",
        "السؤال cinq: حسب l'énergie électrique المخزونة فle condensateur فt égale tau.",
        valeur("E_e", 4.29e-3, "J", "u_C(τ) = E − u_R(τ) = 0,63·E = 7,56 V ; E_e = ½·C·u_C² = ½ × 1,5·10⁻⁴ × 7,56² = 4,29·10⁻³ J"),
        ["u_C = E − u_R", "E_e = ½·C·u_C²", "J"], ["E_e = ½·C·E²", "E_e = ½·C·u_R²", "u_C(τ) = 0,37·E"],
        [aide("L'énergie est stockée dans le condensateur : il faut u_C(τ), pas u_R(τ). Utilise l'additivité u_R + u_C = E.",
              "l'énergie مخزونة فle condensateur: خاصك u C de tau، ماشي u R. استعمل l'additivité: u R plus u C égale E."),
         aide("u_C(τ) = E − 0,37·E = 0,63·E, puis E_e = ½·C·u_C² (avec le carré).",
              "u C de tau égale E moins zéro virgule trente-sept E، يعني zéro virgule soixante-trois E. ومن بعد E e égale un demi C u C au carré.")],
        corr([("5 : u_C(τ) = E − u_R(τ) = E − 0,37·E = 0,63·E = 7,56 V", "sept virgule cinquante-six volts"),
              ("E_e = ½·C·u_C(τ)²", "E e égale un demi fois C fois u C au carré"),
              ("A.N. : E_e = ½ × 1,5·10⁻⁴ × 7,56² ≈ 4,29·10⁻³ J", "quatre virgule vingt-neuf fois dix puissance moins trois joule")],
             "السؤال cinq. u C de tau égale E moins u R de tau، يعني zéro virgule soixante-trois fois E، sept virgule cinquante-six volts. E e égale un demi fois C fois u C au carré. un demi fois un virgule cinq fois dix puissance moins quatre، fois sept virgule cinquante-six au carré. E e environ quatre virgule vingt-neuf fois dix puissance moins trois joule. يعني environ quarante pour cent من l'énergie finale، ماشي soixante-trois."),
        "ex_r5", "fa_r5"),
      question("6", "Montrer que l'énergie stockée atteint la moitié de sa valeur finale à la date t₁ = τ·ln(2 + √2), puis calculer t₁ (en ms). Comparer t₁ à τ.",
        "السؤال six: بين بلي l'énergie كتوصل لla moitié ديال la valeur finale فt un égale tau fois ln de deux plus racine de deux، ومن بعد حسب t un بla milliseconde، و قارنها مع tau.",
        valeur("t₁", 36.8, "ms", "½·C·u_C² = ½·(½·C·E²) donne u_C = E/√2, soit 1 − e^(−t₁/τ) = 1/√2, e^(t₁/τ) = √2/(√2 − 1) = 2 + √2 ; t₁ = τ·ln(2 + √2) = 30 × 1,228 ≈ 36,8 ms"),
        ["u_C = E/√2", "e^(−t/τ)", "ln", "√2/(√2 − 1) = 2 + √2", "ms"], ["u_C = E/2", "t₁ = τ/2", "t₁ = τ·ln2"],
        [aide("Écris E_e(t₁) = ½ × ½·C·E², simplifie pour trouver u_C(t₁) en fonction de E (attention : l'énergie dépend du carré).",
              "كتب E e de t un égale un demi fois un demi C E au carré. بسط باش تلقى u C de t un en fonction de E، ورد البال: l'énergie فيها le carré."),
         aide("u_C = E/√2 et u_C = E(1 − e^(−t/τ)) : isole e^(−t₁/τ), puis prends le ln.",
              "u C égale E sur racine de deux، و u C égale E fois un moins exponentielle. خلي l'exponentielle بوحدها، ومن بعد خود ln.")],
        corr([("6 : ½·C·u_C² = ½·(½·C·E²) donne u_C(t₁) = E/√2", "u C de t un égale E sur racine de deux"),
              ("E(1 − e^(−t₁/τ)) = E/√2, donc e^(−t₁/τ) = 1 − 1/√2 et e^(t₁/τ) = √2/(√2 − 1) = 2 + √2", "exponentielle de t un sur tau égale deux plus racine de deux"),
              ("t₁ = τ·ln(2 + √2) = 30 × 1,228 ≈ 36,8 ms", "trente-six virgule huit millisecondes"),
              ("t₁ > τ : à τ, u_C = 0,63·E mais l'énergie n'est qu'à 40 % ; il faut attendre 1,23τ pour la moitié.", "t un كبر من tau")],
             "السؤال six. un demi C u C au carré égale la moitié ديال un demi C E au carré، إذن u C de t un égale E sur racine de deux. و E fois un moins exponentielle égale E sur racine de deux، إذن exponentielle de t un sur tau égale deux plus racine de deux. t un égale tau fois ln de deux plus racine de deux، يعني trente fois un virgule deux deux huit، environ trente-six virgule huit millisecondes. t un كبر من tau: فtau، l'énergie غير quarante pour cent، حيت فيها le carré."),
        "ex_r6", "fa_r6"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_r1", "Question 1 : l'équation de u_R", "On dérive u_R + u_C = E, puis du_C/dt = u_R/(R·C).",
      SIMD + "figures.html?fig=fig_ed_uR_i", "Dériver l'additivité, puis remplacer du_C/dt",
      "باش نلقاو l'équation ديال u R، كنبداو من l'additivité: u R plus u C égale E. E ثابتة، إذن la dérivée ديالها zéro. كنشتقو: dé u R sur dé t plus dé u C sur dé t égale zéro. ومن بعد: dé u C sur dé t égale i sur C، و i égale u R sur R، إذن dé u C sur dé t égale u R sur R C. كنعوضو و كنضربو fois R C: R C dé u R sur dé t، plus u R، égale zéro. فاليمين zéro: u R كتمشي نحو zéro.",
      centre=[("du_R/dt + du_C/dt = 0", "كنشتقو: dé u R sur dé t plus dé u C sur dé t égale zéro"), ("R·C·du_R/dt + u_R = 0", "R C dé u R sur dé t، plus u R، égale zéro")],
      pointage=[{"mot": "كنشتقو: dé u R sur dé t plus dé u C sur dé t égale zéro", "commande": "play_until", "parametres": {"moment": "deriver"}},
                {"mot": "كنشتقو: dé u R sur dé t plus dé u C sur dé t égale zéro", "cible": "centre:0"},
                {"mot": "إذن dé u C sur dé t égale u R sur R C", "commande": "play_until", "parametres": {"moment": "relation"}},
                {"mot": "كنعوضو و كنضربو fois R C", "commande": "play_until", "parametres": {"moment": "uR"}},
                {"mot": "R C dé u R sur dé t، plus u R، égale zéro", "cible": "centre:1"}]),
    diapo_sim("ex_r2", "Question 2 : vérifier la solution", "Même forme que la décharge : A·e^(−t/τ) avec τ = R·C ; ici A = u_R(0) = E.",
      SIMD + "figures.html?fig=fig_decharge_solution", "La même équation que la décharge : y(t) = A·e^(−t/τ)",
      "l'équation ديال u R عندها نفس الشكل ديال la décharge: R C fois la dérivée، plus la fonction، égale zéro. إذن نفس الطريقة. la forme: A fois exponentielle de moins t sur tau. la dérivée: moins A sur tau، fois exponentielle. كنعوضو: A fois exponentielle، fois un moins R C sur tau، égale zéro، pour tout t. إذن tau égale R C. و A؟ فt égale zéro le condensateur déchargé، u C égale zéro، إذن u R de zéro égale E. A égale E.",
      centre=[("τ = R·C", "إذن tau égale R C"), ("u_R(0) = E − u_C(0) = E", "إذن u R de zéro égale E")],
      pointage=[{"mot": "la forme: A fois exponentielle", "commande": "play_until", "parametres": {"moment": "forme"}},
                {"mot": "la dérivée: moins A sur tau", "commande": "play_until", "parametres": {"moment": "deriver"}},
                {"mot": "كنعوضو: A fois exponentielle", "commande": "play_until", "parametres": {"moment": "remplacer"}},
                {"mot": "إذن tau égale R C", "commande": "play_until", "parametres": {"moment": "tau"}},
                {"mot": "إذن tau égale R C", "cible": "centre:0"},
                {"mot": "إذن u R de zéro égale E", "cible": "centre:1"}]),
    diapo_sim("ex_r3", "Question 3 : E et τ sur une courbe qui descend", "u_R = R·i : même allure que i(t) ; 37 % ou tangente jusqu'à l'axe des temps.",
      SIMD + "quatre-courbes.html?vue=descente", "R = 200 Ω, C = 150 µF : i(t) descend ; τ par la tangente et par les 37 %",
      "u R égale R fois i، إذن u R و i عندهم نفس الشكل. شوف i en fonction de t: كتبدا من الفوق وكتهبط نحو zéro. على la courbe ديالنا، القيمة ديال البداية هي u R de zéro égale E، يعني douze volts. دابا tau: la tangente à l'origine كتقطع l'axe des temps فtau. ولا zéro virgule trente-sept fois la valeur de départ: الخط الأفقي حتى la courbe، ومن بعد كنهبطو. tau égale R C، يعني deux cents fois cent cinquante fois dix puissance moins six، trente millisecondes. على u R: zéro virgule trente-sept fois douze، quatre virgule quarante-quatre volts، و كنقراو tau égale trente millisecondes.",
      centre=[("E = u_R(0) = 12 V", "يعني douze volts"), ("u_R(τ) = 0,37 × 12 = 4,44 V → τ = 30 ms", "و كنقراو tau égale trente millisecondes")],
      pointage=[avec(REGQ, "u R égale R fois i"),
                {"mot": "شوف i en fonction de t", "commande": "play_until", "parametres": {"moment": "i"}},
                {"mot": "يعني douze volts", "cible": "centre:0"},
                {"mot": "دابا tau: la tangente à l'origine", "commande": "play_until", "parametres": {"moment": "tangente_descente"}},
                {"mot": "كتقطع l'axe des temps فtau", "repere": "tangente"},
                {"mot": "ولا zéro virgule trente-sept", "commande": "play_until", "parametres": {"moment": "ligne_37"}},
                {"mot": "trente millisecondes. على u R", "repere": "tau"},
                {"mot": "و كنقراو tau égale trente millisecondes", "cible": "centre:1"}]),
    diapo_sim("ex_r4", "Question 4 : C = τ/R", "C = τ/R = 30·10⁻³/200 = 1,5·10⁻⁴ F.",
      SIMD + "quatre-courbes.html?vue=uC_uR", "u_C monte, u_R descend : u_C + u_R = E à chaque instant",
      "شوف u C كتطلع، و u R كتهبط. فكل لحظة u C plus u R égale E. les deux عندهم نفس tau، tau égale R C. إذن C égale tau sur R. ما تنساش: tau égale trente millisecondes، يعني trente fois dix puissance moins trois seconde. C égale trente fois dix puissance moins trois، sur deux cents. C égale un virgule cinq fois dix puissance moins quatre farad، يعني cent cinquante microfarads.",
      centre=[("C = τ/R", "إذن C égale tau sur R"), ("C = 30·10⁻³/200 = 1,5·10⁻⁴ F", "C égale un virgule cinq fois dix puissance moins quatre farad")],
      pointage=[avec(REGQ, "شوف u C كتطلع"),
                {"mot": "شوف u C كتطلع", "commande": "play_until", "parametres": {"moment": "uC"}},
                {"mot": "و u R كتهبط", "commande": "play_until", "parametres": {"moment": "uR"}},
                {"mot": "فكل لحظة u C plus u R égale E", "commande": "play_until", "parametres": {"moment": "somme"}},
                {"mot": "إذن C égale tau sur R", "cible": "centre:0"},
                {"mot": "C égale un virgule cinq fois dix puissance moins quatre farad", "cible": "centre:1"}]),
    diapo_sim("ex_r5", "Question 5 : l'énergie à t = τ", "u_C(τ) = 0,63·E : E_e ≈ 0,40 × ½·C·E² ≈ 4,3·10⁻³ J.",
      SIMD + "energie.html?vue=calcul", "C = 150 µF, E = 12 V : l'énergie finale, puis l'énergie à t = τ",
      "شوف الحساب مع C égale cent cinquante microfarads، و E égale douze volts. فle régime permanent، u C égale E: E e égale un demi C E au carré، environ un virgule zéro huit fois dix puissance moins deux joule. ولكن السؤال على t égale tau. فtau، u C ماشي E: u C égale E moins u R، يعني zéro virgule soixante-trois fois E، sept virgule cinquante-six volts. E e égale un demi C fois sept virgule cinquante-six au carré، environ quatre virgule trois fois dix puissance moins trois joule. هادي environ quarante pour cent من l'énergie finale، حيت zéro virgule soixante-trois au carré كتعطي zéro virgule quarante.",
      centre=[("u_C(τ) = 0,63·E = 7,56 V", "sept virgule cinquante-six volts"), ("E_e = ½ × 1,5·10⁻⁴ × 7,56² ≈ 4,3·10⁻³ J", "environ quatre virgule trois fois dix puissance moins trois joule")],
      pointage=[avec(REGE, "شوف الحساب"),
                {"mot": "فle régime permanent", "commande": "play_until", "parametres": {"moment": "regime_permanent"}},
                {"mot": "ولكن السؤال على t égale tau", "commande": "play_until", "parametres": {"moment": "a_tau"}},
                {"mot": "sept virgule cinquante-six volts", "cible": "centre:0"},
                {"mot": "environ quatre virgule trois fois dix puissance moins trois joule", "cible": "centre:1"},
                {"mot": "هادي environ quarante pour cent", "repere": "resultat"}]),
    diapo_sim("ex_r6", "Question 6 : la moitié de l'énergie", "Moitié de l'énergie ⇒ u_C = E/√2 ; t₁ = τ·ln(2 + √2) ≈ 1,23τ.",
      SIMD + "energie.html?vue=calcul", "Une fraction de l'énergie donne une fraction de u_C avec une racine carrée",
      "la figure كتورينا مثال: l'énergie كتنقص de trente pour cent، كيبقى soixante-dix pour cent، و u C égale racine de zéro virgule soixante-dix fois E. نفس الفكرة عندنا: la moitié ديال l'énergie، إذن u C au carré égale la moitié ديال E au carré، يعني u C égale E sur racine de deux. ومن بعد، u C égale E fois un moins exponentielle. exponentielle de moins t un sur tau égale un moins un sur racine de deux. كنقلبو و كناخدو ln: t un égale tau fois ln de deux plus racine de deux، يعني environ un virgule vingt-trois tau، trente-six virgule huit millisecondes.",
      centre=[("E_e = ½·E_e,max ⇒ u_C = E/√2", "يعني u C égale E sur racine de deux"), ("t₁ = τ·ln(2 + √2) ≈ 36,8 ms", "trente-six virgule huit millisecondes")],
      pointage=[avec(REGE, "la figure كتورينا مثال"),
                {"mot": "l'énergie كتنقص de trente pour cent", "commande": "play_until", "parametres": {"moment": "reste_70"}},
                {"mot": "يعني u C égale E sur racine de deux", "cible": "centre:0"},
                {"mot": "trente-six virgule huit millisecondes", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_r1", "Plus facile : l'équation de u_R", "سؤال ساهل: اختار l'équation ديال u R فla charge.",
      "Pendant la charge sous E, la tension u_R vérifie…",
      ["R·C·du_R/dt + u_R = E", "R·C·du_R/dt + u_R = 0", "R·C·du_R/dt − u_R = 0"], 1, {
        "1": {"juste": rep("برافو! ملي كنشتقو l'additivité، la dérivée ديال E كتولي zéro.", "Juste : en dérivant u_R + u_C = E, dE/dt = 0.")},
        "0": {"1": rep("ما تقلقش. هادي كتشبه l'équation ديال u C. ولكن ل u R كنشتقو l'additivité: شنو la dérivée ديال E؟ عاود اختار.", "On dérive l'additivité : que vaut la dérivée de E (constante) ? Réessaie."),
              "2": rep("الجواب هو R C dé u R sur dé t، plus u R، égale zéro. u R كتمشي نحو zéro، ماشي نحو E.", "Réponse : R·C·du_R/dt + u_R = 0 ; u_R tend vers 0.")},
        "2": {"1": rep("قريب. ولكن ما كاينش moins: dé u C sur dé t égale u R sur R C، و كيتزاد. عاود اختار.", "Pas de signe moins : du_C/dt = +u_R/(RC). Réessaie."),
              "2": rep("الجواب هو R C dé u R sur dé t، plus u R، égale zéro.", "Réponse : R·C·du_R/dt + u_R = 0.")}},
      "Pendant la charge, la tension u R vérifie quelle équation ?"),
    qcm_facile("fa_r2", "Plus facile : u_R au départ", "سؤال ساهل على u R فt égale zéro.",
      "Le condensateur est déchargé. Juste après la fermeture de K, u_R vaut…",
      ["0", "0,63·E", "E"], 2, {
        "2": {"juste": rep("مزيان! u C de zéro égale zéro، إذن u R de zéro égale E.", "Juste : u_C(0) = 0, donc u_R(0) = E.")},
        "0": {"1": rep("ما تقلقش. اللي كيبدا من zéro هو u C، حيت le condensateur déchargé. و u R؟ استعمل l'additivité. عاود اختار.", "C'est u_C qui part de 0 ; utilise u_R + u_C = E. Réessaie."),
              "2": rep("الجواب هو E. u R plus u C égale E، و u C de zéro égale zéro.", "Réponse : u_R(0) = E, car u_C(0) = 0.")},
        "1": {"1": rep("لا، zéro virgule soixante-trois كتخص u C فt égale tau. هنا t égale zéro. عاود اختار.", "0,63·E concerne u_C à t = τ ; ici t = 0. Réessaie."),
              "2": rep("الجواب هو E. فالبداية كل la tension ديال le générateur فla résistance.", "Réponse : u_R(0) = E.")}},
      "Juste après la fermeture de K, u R vaut ?"),
    qcm_facile("fa_r3", "Plus facile : τ sur une courbe qui descend", "سؤال ساهل على la courbe ديال u R.",
      "Sur la courbe u_R(t) (qui décroît de E vers 0), on lit τ là où u_R vaut…",
      ["0,37·E", "0,63·E", "E/2"], 0, {
        "0": {"juste": rep("برافو! la courbe كتهبط: فtau كيبقى trente-sept pour cent من la valeur de départ.", "Juste : courbe qui décroît → 0,37·E.")},
        "1": {"1": rep("ما تقلقش. soixante-trois pour cent كتصلح للمنحنى اللي كيطلع، بحال u C. عاود اختار.", "0,63 sert pour une courbe qui monte (u_C). Réessaie."),
              "2": rep("الجواب هو zéro virgule trente-sept fois E. u R égale E fois exponentielle de moins un، يعني zéro virgule trente-sept E.", "Réponse : u_R(τ) = E·e⁻¹ ≈ 0,37·E.")},
        "2": {"1": rep("قريب. E sur deux ماشي فtau. شنو كتعطي exponentielle de moins un؟ عاود اختار.", "E/2 n'est pas atteint à τ ; que vaut e⁻¹ ? Réessaie."),
              "2": rep("الجواب هو zéro virgule trente-sept fois E، حيت exponentielle de moins un environ zéro virgule trente-sept.", "Réponse : 0,37·E (e⁻¹ ≈ 0,37).")}},
      "Sur la courbe de u R qui descend، on lit tau là où u R vaut combien ?"),
    qcm_facile("fa_r4", "Plus facile : C à partir de τ", "سؤال ساهل: C من tau و R.",
      "τ = 30 ms et R = 200 Ω. La capacité C vaut…",
      ["1,5·10⁻⁴ F", "6 F", "0,15 F"], 0, {
        "0": {"juste": rep("مزيان! C égale tau sur R، trente fois dix puissance moins trois، sur deux cents.", "Juste : C = 30·10⁻³/200 = 1,5·10⁻⁴ F.")},
        "1": {"1": rep("ما تقلقش. ضربتي tau فR. ولكن C égale tau sur R. عاود اختار.", "Tu as multiplié τ par R ; or C = τ/R. Réessaie."),
              "2": rep("الجواب هو un virgule cinq fois dix puissance moins quatre farad. C égale tau sur R.", "Réponse : C = τ/R = 1,5·10⁻⁴ F.")},
        "2": {"1": rep("قريب. نسيتي تحول les millisecondes لla seconde. عاود اختار.", "Tu as oublié de convertir les ms en s. Réessaie."),
              "2": rep("الجواب هو un virgule cinq fois dix puissance moins quatre farad: trente millisecondes égale trente fois dix puissance moins trois seconde.", "Réponse : 1,5·10⁻⁴ F (30 ms = 30·10⁻³ s).")}},
      "Tau égale trente millisecondes et R égale deux cents ohms. C vaut ?"),
    vrai_faux_facile("fa_r5", "Plus facile : vrai ou faux", "سؤال ساهل على l'énergie فt égale tau.",
      "Charge sous E : énergie du condensateur à t = τ.",
      [("À t = τ, u_C = 0,63·E, donc E_e = ½·C·(0,63·E)².", True, "u_C(τ) = E − u_R(τ) = 0,63·E, puis E_e = ½·C·u_C²."),
       ("À t = τ, l'énergie stockée vaut 63 % de l'énergie finale.", False, "0,63² ≈ 0,40 : seulement 40 % de ½·C·E²."),
       ("Pour l'énergie du condensateur, on utilise u_R.", False, "L'énergie stockée dépend de la tension du condensateur, u_C.")]),
    qcm_facile("fa_r6", "Plus facile : la moitié de l'énergie", "سؤال ساهل على la moitié ديال l'énergie.",
      "L'énergie stockée vaut la moitié de sa valeur finale ½·C·E² quand u_C vaut…",
      ["E/2", "E/√2", "0,63·E"], 1, {
        "1": {"juste": rep("برافو! u C au carré égale la moitié ديال E au carré، إذن u C égale E sur racine de deux.", "Juste : u_C² = E²/2, donc u_C = E/√2.")},
        "0": {"1": rep("ما تقلقش. l'énergie فيها le carré. إلى u C égale E sur deux، l'énergie كتولي le quart. عاود اختار.", "Avec u_C = E/2, l'énergie serait le quart (carré). Réessaie."),
              "2": rep("الجواب هو E sur racine de deux. حيت l'énergie proportionnelle à u C au carré.", "Réponse : E/√2, car E_e est proportionnelle à u_C².")},
        "2": {"1": rep("قريب. zéro virgule soixante-trois au carré كتعطي zéro virgule quarante، ماشي la moitié. عاود اختار.", "0,63² ≈ 0,40, pas 0,5. Réessaie."),
              "2": rep("الجواب هو E sur racine de deux، يعني environ zéro virgule soixante et onze fois E.", "Réponse : u_C = E/√2 ≈ 0,71·E.")}},
      "L'énergie vaut la moitié de sa valeur finale quand u C vaut combien ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec R = 400 Ω ; E et C sont inconnues. Le condensateur est initialement déchargé ; à t = 0, on ferme K. La figure 2 donne u_R(t).",
      "intro_dit": "نفس التمرين، بقيم أخرى. R égale quatre cents ohms، و E و C ما عارفينهومش. la figure deux كتعطي u R en fonction de t.",
      "figures": [courbe_uR(9, 40, 240, 20, "Figure 2 : la tension u_R(t)")],
      "donnees": ["R = 400 Ω"],
      "questions": [
        question_semblable("1", "Montrer que R·C·du_R/dt + u_R = 0.",
          phrase(ED_ATT), ["dE/dt = 0", "du_C/dt = u_R/(R·C)"], ["u_R + u_C = 0"],
          corr([("1 : on dérive u_R + u_C = E : du_R/dt + du_C/dt = 0", "كنشتقو l'additivité"), ("du_C/dt = u_R/(R·C), donc R·C·du_R/dt + u_R = 0", "R C dé u R sur dé t، plus u R، égale zéro")],
               "كنشتقو l'additivité، و dé u C sur dé t égale u R sur R C. إذن R C dé u R sur dé t، plus u R، égale zéro.")),
        question_semblable("2", "Vérifier que u_R = E·e^(−t/τ) est solution si τ = R·C, et justifier u_R(0) = E.",
          phrase(SOL_ATT), ["pour tout t", "u_C(0) = 0"], ["u_R(0) = 0"],
          corr([("2 : E·e^(−t/τ)·(1 − R·C/τ) = 0 pour tout t : τ = R·C", "tau égale R C"), ("u_C(0) = 0, donc u_R(0) = E", "u R de zéro égale E")],
               "كنعوضو: E fois exponentielle، fois un moins R C sur tau، égale zéro، إذن tau égale R C. و u C de zéro égale zéro، إذن u R de zéro égale E.")),
        question_semblable("3", "Déterminer E et τ (en ms).",
          valeur("τ", 40, "ms", "E = u_R(0) = 9 V ; u_R(τ) = 0,37 × 9 = 3,33 V, on lit τ = 40 ms"), ["E = u_R(0)", "0,37·E"], ["0,63·E"],
          corr([("3 : E = u_R(0) = 9 V", "E égale neuf volts"), ("0,37·E = 3,33 V : τ = 40 ms", "tau égale quarante millisecondes")],
               "E égale u R de zéro، يعني E égale neuf volts. zéro virgule trente-sept fois neuf، trois virgule trente-trois volts، و كنقراو tau égale quarante millisecondes.")),
        question_semblable("4", "En déduire C.",
          valeur("C", 1e-4, "F", "C = τ/R = 40·10⁻³/400 = 1·10⁻⁴ F"), ["C = τ/R"], ["C = R·τ"],
          corr([("4 : C = τ/R = 40·10⁻³/400", "C égale tau sur R"), ("C = 1·10⁻⁴ F", "dix puissance moins quatre farad")],
               "C égale tau sur R، quarante fois dix puissance moins trois، sur quatre cents. C égale dix puissance moins quatre farad.")),
        question_semblable("5", "Calculer l'énergie emmagasinée à t = τ.",
          valeur("E_e", 1.61e-3, "J", "u_C(τ) = 0,63 × 9 = 5,67 V ; E_e = ½ × 10⁻⁴ × 5,67² ≈ 1,61·10⁻³ J"), ["u_C = E − u_R", "E_e = ½·C·u_C²"], ["E_e = ½·C·E²"],
          corr([("5 : u_C(τ) = 0,63·E = 5,67 V", "cinq virgule soixante-sept volts"), ("E_e = ½ × 10⁻⁴ × 5,67² ≈ 1,61·10⁻³ J", "un virgule soixante et un fois dix puissance moins trois joule")],
               "u C de tau égale zéro virgule soixante-trois fois neuf، cinq virgule soixante-sept volts. E e égale un demi C u C au carré، environ un virgule soixante et un fois dix puissance moins trois joule.")),
        question_semblable("6", "Montrer que t₁ = τ·ln(2 + √2) quand l'énergie vaut la moitié de sa valeur finale ; calculer t₁ (en ms).",
          valeur("t₁", 49.1, "ms", "u_C = E/√2 ⇒ e^(t₁/τ) = 2 + √2 ; t₁ = τ·ln(2 + √2) = 40 × 1,228 ≈ 49,1 ms"), ["u_C = E/√2", "ln"], ["u_C = E/2"],
          corr([("6 : u_C(t₁) = E/√2, e^(t₁/τ) = 2 + √2", "u C égale E sur racine de deux"), ("t₁ = 40 × 1,228 ≈ 49,1 ms", "quarante-neuf virgule un millisecondes")],
               "u C égale E sur racine de deux، إذن t un égale tau fois ln de deux plus racine de deux، يعني quarante fois un virgule deux deux huit، environ quarante-neuf virgule un millisecondes.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
