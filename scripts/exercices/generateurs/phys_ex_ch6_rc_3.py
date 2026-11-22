# Exercice de physique, ch. 6 (dipôle RC), niveau moyen n° 3 : deux condensateurs en série chargés sous E ;
# équation différentielle, analyse dimensionnelle, τ par la tangente, C_eq puis C₂.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration backend/data/curriculum/exploration/dipole_RC.json : cas_types « ed_charge_uC », « tau_graphique »,
#    « R_C_E_deduits », « association » ; pièges « confondre série et parallèle (formules des résistances) »,
#    « lire l'unité de l'axe » ; erreurs_examen « établir l'ED » (additivité écrite d'abord), « calcul de C »
#    (expression littérale avant l'A.N.) ; redaction_nationale « etablir_ED_charge », « tau_graphique ».
#  - nationaux : 2016 N, 2021 N, 2022 N (ED de u_C), 2017 R (dimension de RC), 2018 N (association, en parallèle),
#    2019 N, 2022 N (τ par la tangente) ; ici l'association est en SÉRIE et les données sont les nôtres.
#  - cours phys_ch6_dipole_RC : rc_e2_etablir (figures.html?fig=fig_ed_charge), rc_t1_dimension (fig_dimension),
#    rc_l1_tangente (courbe-charge.html?vue=tangente, réglable R_ohm, C_uF, E), rc_t2_influence (tau-rc.html, R 0,5→3 kΩ,
#    C 100→470 µF), rc_a2_serie (fig_serie) ; nos valeurs (R = 3 kΩ, C_eq = 100 µF) y sont réglées.
#  - séries en ligne : recherche faite (Naceiri Mrabti « Série P6 », talamidi, moutamadris, alloschool), pages non
#    lisibles depuis cette session (domaines bloqués) : on s'appuie sur les sources du dépôt.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch6_rc_3"
SIMD = "/media/simulations/physics/dipole-rc-tableau/"


def montage(titre):
    """E, K, R puis C₁ et C₂ en série ; u_C aux bornes de l'association (A en haut, B en bas)."""
    return schema(titre, 8.4, 4.6,
        dipole([1, 0.8], [1, 3.8], "G", "E", pos="o"),
        fil([1, 3.8], [1.8, 3.8]),
        dipole([1.8, 3.8], [3.6, 3.8], "K", "K"),
        dipole([3.6, 3.8], [6.2, 3.8], "R", "R"),
        fil([6.2, 3.8], [6.8, 3.8]),
        dipole([6.8, 3.8], [6.8, 2.3], "C", "C₁", pos="o", taille=0.8),
        dipole([6.8, 2.3], [6.8, 0.8], "C", "C₂", pos="o", taille=0.8),
        fil([6.8, 0.8], [1, 0.8]),
        courant([3.2, 0.8], "g"),
        tension([7.6, 1.0], [7.6, 3.6], "u_C", pos="e"),
        borne([6.8, 3.8], "A", "n"), borne([6.8, 0.8], "B", "s"))


def charge_tangente(E, tau, tmax, pas_t, titre):
    n = int(round(tmax / pas_t))
    return figure_courbe(titre, axe("t", 0, round(tmax + pas_t * 0.6, 3), "s", [round(i * pas_t, 3) for i in range(n + 1)]),
        axe("u_C", 0, E * 1.25, "V", list(range(0, int(E * 1.25) + 1, 2))),
        [{"f": "courbe", "expr": f"{E}*(1-exp(-x/{tau}))", "couleur": "orange", "texte": "u_C(t)", "texte_x": tmax * 0.78, "pos": "s"},
         {"f": "courbe", "expr": f"{E}*x/{tau}", "de": 0, "a": tau * 1.2, "couleur": "cyan", "trait": "pointille", "texte": "(T)", "texte_x": tau * 1.15, "pos": "o"},
         {"f": "repere", "y": E, "t": "u_C = E"}],
        legende="Courbe u_C(t) après la fermeture de K à t = 0 ; (T) : tangente à la courbe à l'origine.")


E, R, C1 = 12, 3e3, 300e-6
TAU = 0.3
CEQ = TAU / R                       # 1·10⁻⁴ F
C2 = C1 * CEQ / (C1 - CEQ)          # 1,5·10⁻⁴ F
assert abs(CEQ - 1e-4) < 1e-12 and abs(C2 - 1.5e-4) < 1e-12 and abs(1 / CEQ - (1 / C1 + 1 / C2)) < 1e-6
# semblable : E = 10 V, R = 5 kΩ, C₁ = 120 µF, C₂ = 40 µF → C_eq = 30 µF, τ = 0,15 s
assert abs(1 / (1 / 120e-6 + 1 / 40e-6) - 30e-6) < 1e-12 and abs(5e3 * 30e-6 - 0.15) < 1e-12
assert abs(120e-6 * 30e-6 / (120e-6 - 30e-6) - 40e-6) < 1e-12

ED_ATT = ("D'après la loi d'additivité des tensions : u_R + u_C = E. Loi d'Ohm : u_R = R·i, avec i = dq/dt = C_eq·du_C/dt. "
          "Donc R·C_eq·du_C/dt + u_C = E.")
DIM_ATT = ("u_R = R·i donne [R] = [U]/[I] ; i = C·du_C/dt donne [C] = [I]·[T]/[U]. "
           "Donc [R]·[C] = ([U]/[I])·([I]·[T]/[U]) = [T] : τ = R·C_eq est homogène à un temps (en s).")
REG_T = {"commande": "set_parameters", "parametres": {"R_ohm": 3000, "C_uF": 100, "E": 12}}
REG_RC = {"commande": "set_parameters", "parametres": {"R_kohm": 3, "C_uF": 100}}
def avec(d, mot):
    x = dict(d); x["mot"] = mot; return x

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "dipole_RC", "cours": "phys_ch6_dipole_RC",
  "titre": "Deux condensateurs en série : de la tangente à C₂", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir l'équation différentielle de u_C pendant la charge",
                  "Montrer par analyse dimensionnelle que R·C est un temps",
                  "Déterminer τ par la tangente à l'origine",
                  "Utiliser la capacité équivalente de deux condensateurs en série"],
  "enonce": {
    "intro": "On dispose d'un condensateur de capacité C₁ = 300 µF et d'un condensateur de capacité C₂ inconnue. On les monte en série (figure 1) avec un conducteur ohmique de résistance R = 3 kΩ, un interrupteur K et un générateur idéal de tension de force électromotrice E = 12 V. Les condensateurs sont initialement déchargés. À t = 0, on ferme K ; on enregistre la tension u_C aux bornes de l'association des deux condensateurs, de capacité équivalente C_eq (figure 2, avec la tangente (T) à l'origine).",
    "intro_dit": "دابا نقراو l'énoncé. عندنا deux condensateurs: la capacité ديال الأول C un égale trois cents microfarads، و الثاني C deux ما عارفينهاش. ركبناهم en série، مع un conducteur ohmique، R égale trois kiloohms، l'interrupteur K، و un générateur، E égale douze volts. فالبداية déchargés. فt égale zéro كنسدو K، و كنسجلو la tension u C ديال les deux condensateurs، اللي عندهم la capacité équivalente C é q. هادي هي la figure deux، مع la tangente à l'origine.",
    "figures": [montage("Figure 1 : le montage"), charge_tangente(12, 0.3, 1.5, 0.1, "Figure 2 : u_C(t) et la tangente (T)")],
    "donnees": ["E = 12 V", "R = 3 kΩ = 3·10³ Ω", "C₁ = 300 µF = 300·10⁻⁶ F", "C₂ inconnue ; C_eq : capacité équivalente de l'association"],
    "questions": [
      question("1", "Établir l'équation différentielle vérifiée par la tension u_C(t) pendant la charge.",
        "السؤال un: بين l'équation différentielle اللي كتحققها la tension u C فالشحن.",
        phrase(ED_ATT),
        ["u_R + u_C = E", "u_R = R·i", "i = dq/dt", "q = C_eq·u_C", "du_C/dt"], ["u_R − u_C = E", "i = C_eq·u_C", "i = q/t"],
        [aide("Commence par la loi d'additivité des tensions dans le circuit fermé : quelles tensions s'ajoutent pour donner E ?",
              "بدا بl'additivité des tensions فle circuit: شنو هي les tensions اللي كيتزادو وكيعطيو E؟"),
         aide("Remplace u_R par R·i, puis i par C_eq·du_C/dt (car i = dq/dt et q = C_eq·u_C).",
              "عوض u R ب R fois i، ومن بعد i ب C é q fois dé u C sur dé t، حيت i égale dé q sur dé t، و q égale C é q fois u C.")],
        corr([("1 : d'après la loi d'additivité des tensions : u_R + u_C = E", "u R plus u C égale E"),
              ("Loi d'Ohm : u_R = R·i, avec i = dq/dt = C_eq·du_C/dt", "i égale C é q fois dé u C sur dé t"),
              ("Donc R·C_eq·du_C/dt + u_C = E", "R C é q fois dé u C sur dé t، plus u C، égale E")],
             "السؤال un. d'après la loi d'additivité des tensions، u R plus u C égale E. la loi d'Ohm: u R égale R fois i، و i égale C é q fois dé u C sur dé t. إذن R C é q fois dé u C sur dé t، plus u C، égale E."),
        "ex_s1", "fa_s1"),
      question("2", "Par une analyse dimensionnelle, montrer que τ = R·C_eq a la dimension d'un temps.",
        "السؤال deux: بl'analyse dimensionnelle، بين بلي tau égale R C é q عندها la dimension ديال le temps.",
        phrase(DIM_ATT),
        ["[R] = [U]/[I]", "[C] = [I]·[T]/[U]", "u_R = R·i", "i = C·du_C/dt"], ["[C] = [U]/[I]", "[R]·[C] = [U]"],
        [aide("Trouve la dimension de R avec une relation qui la contient (loi d'Ohm), puis celle de C avec i = C·du_C/dt.",
              "لقا la dimension ديال R بla loi d'Ohm، ومن بعد la dimension ديال C ب i égale C dé u C sur dé t."),
         aide("[R] = [U]/[I] et [C] = [I]·[T]/[U] : multiplie les deux et simplifie.",
              "la dimension ديال R هي U sur I، و ديال C هي I fois T sur U. ضربهم، ومن بعد بسط.")],
        corr([("2 : u_R = R·i donne [R] = [U]/[I]", "la dimension de R، c'est U sur I"),
              ("i = C·du_C/dt donne [C] = [I]·[T]/[U]", "la dimension de C، c'est I fois T sur U"),
              ("[R]·[C] = [T] : τ = R·C_eq est homogène à un temps, en secondes.", "كيبقى غير T")],
             "السؤال deux. من u R égale R i، la dimension de R، c'est U sur I. من i égale C dé u C sur dé t، la dimension de C، c'est I fois T sur U. كنضربوهم: U كتمشي مع U، و I مع I، كيبقى غير T. إذن tau égale R C é q، homogène à un temps."),
        "ex_s2", "fa_s2"),
      question("3", "Déterminer graphiquement la valeur de la constante de temps τ.",
        "السؤال trois: حدد مبيانيا la valeur ديال la constante de temps tau.",
        valeur("τ", 0.3, "s", "(T) coupe l'asymptote u_C = E au point d'abscisse τ = 0,3 s"),
        ["tangente à l'origine", "asymptote u_C = E", "abscisse", "s"], ["τ = 0,03 s", "intersection avec l'axe des temps"],
        [aide("Repère l'asymptote horizontale u_C = E = 12 V et la tangente (T) tracée à l'origine. Où se coupent-elles ?",
              "شوف l'asymptote الأفقية، u C égale E égale douze volts، و la tangente اللي مرسومة من l'origine. فين كيتلاقاو؟"),
         aide("τ est l'abscisse du point d'intersection de (T) avec l'asymptote : descends sur l'axe des temps et lis la graduation (0,1 s par graduation).",
              "tau هي l'abscisse ديال le point d'intersection ديال la tangente مع l'asymptote. هبط لl'axe des temps، وقرا: كل graduation فيها zéro virgule un seconde.")],
        corr([("3 : τ est l'abscisse du point d'intersection de la tangente (T) à l'origine avec l'asymptote u_C = E = 12 V", "tau est l'abscisse du point d'intersection"),
              ("On lit τ = 0,3 s", "tau égale zéro virgule trois seconde")],
             "السؤال trois. tau est l'abscisse du point d'intersection، de la tangente à l'origine، avec l'asymptote u C égale douze volts. كنهبطو لl'axe des temps، وكنقراو tau égale zéro virgule trois seconde."),
        "ex_s3", "fa_s3"),
      question("4", "En déduire la valeur de la capacité équivalente C_eq.",
        "السؤال quatre: استنتج la valeur ديال la capacité équivalente C é q.",
        valeur("C_eq", 1e-4, "F", "C_eq = τ/R = 0,3/(3·10³) = 1·10⁻⁴ F"),
        ["τ = R·C_eq", "C_eq = τ/R", "10³", "F", "µF"], ["C_eq = R/τ", "C_eq = R·τ", "C_eq = 0,3/3 = 0,1 F"],
        [aide("Tu connais τ (question 3) et R (données). Quelle relation les relie à C_eq ?",
              "عارف tau من السؤال trois، و R من les données. شنو هي la relation اللي كتربطهم ب C é q؟"),
         aide("τ = R·C_eq, donc C_eq = τ/R ; écris R en ohms : 3 kΩ = 3·10³ Ω.",
              "tau égale R fois C é q، إذن C é q égale tau sur R. كتب R بl'ohm: trois kiloohms égale trois fois dix puissance trois ohm.")],
        corr([("4 : τ = R·C_eq, donc C_eq = τ/R", "C é q égale tau sur R"),
              ("A.N. : C_eq = 0,3/(3·10³)", "zéro virgule trois، sur trois fois dix puissance trois"),
              ("C_eq = 1·10⁻⁴ F = 100 µF", "C é q égale dix puissance moins quatre farad")],
             "السؤال quatre. tau égale R fois C é q، إذن C é q égale tau sur R. l'application numérique: zéro virgule trois، sur trois fois dix puissance trois. C é q égale dix puissance moins quatre farad، يعني cent microfarads."),
        "ex_s4", "fa_s4"),
      question("5", "Les deux condensateurs étant montés en série, déterminer la valeur de la capacité C₂.",
        "السؤال cinq: les deux condensateurs en série. حدد la valeur ديال la capacité C deux.",
        valeur("C₂", 1.5e-4, "F", "1/C₂ = 1/C_eq − 1/C₁, donc C₂ = C₁·C_eq/(C₁ − C_eq) = 300 × 100/(300 − 100) µF = 150 µF = 1,5·10⁻⁴ F"),
        ["1/C_eq = 1/C₁ + 1/C₂", "C₂ = C₁·C_eq/(C₁ − C_eq)", "µF"], ["C₂ = C₁ − C_eq", "C_eq = C₁ + C₂"],
        [aide("En série, les capacités ne s'ajoutent pas : ce sont leurs inverses qui s'ajoutent. Écris la relation de l'association série.",
              "en série، les capacités ما كيتزادوش: les inverses ديالهم هوما اللي كيتزادو. كتب la relation ديال la série."),
         aide("1/C_eq = 1/C₁ + 1/C₂, donc 1/C₂ = 1/C_eq − 1/C₁ ; tu peux calculer en µF puis convertir.",
              "un sur C é q égale un sur C un plus un sur C deux. إذن un sur C deux égale un sur C é q moins un sur C un. تقدر تحسب بle microfarad، ومن بعد تحول.")],
        corr([("5 : en série : 1/C_eq = 1/C₁ + 1/C₂, donc 1/C₂ = 1/C_eq − 1/C₁", "un sur C é q égale un sur C un plus un sur C deux"),
              ("C₂ = C₁·C_eq/(C₁ − C_eq) = 300 × 100/(300 − 100) µF", "trois cents fois cent، sur deux cents"),
              ("C₂ = 150 µF = 1,5·10⁻⁴ F", "C deux égale cent cinquante microfarads")],
             "السؤال cinq. en série، un sur C é q égale un sur C un plus un sur C deux. إذن C deux égale C un fois C é q، sur C un moins C é q. يعني trois cents fois cent، sur deux cents. C deux égale cent cinquante microfarads، يعني un virgule cinq fois dix puissance moins quatre farad."),
        "ex_s5", "fa_s5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_s1", "Question 1 : l'équation différentielle", "Additivité, loi d'Ohm, i = C·du_C/dt : R·C_eq·du_C/dt + u_C = E.",
      SIMD + "figures.html?fig=fig_ed_charge", "Quatre lignes, toujours dans le même ordre",
      "les deux condensateurs en série كيتصرفو بحال un seul condensateur، la capacité ديالو C é q. إذن عندنا le circuit ديال la charge: E، R، و C. السطر الأول، l'additivité: u R plus u C égale E. السطر الثاني، la loi d'Ohm: u R égale R fois i. السطر الثالث: i égale dé q sur dé t، و q égale C é q fois u C، إذن i égale C é q fois dé u C sur dé t. السطر الرابع، كنعوضو: R C é q fois dé u C sur dé t، plus u C، égale E. هادي هي l'équation différentielle.",
      centre=[("u_R + u_C = E", "u R plus u C égale E"), ("R·C_eq·du_C/dt + u_C = E", "plus u C، égale E. هادي هي")],
      pointage=[{"mot": "عندنا le circuit ديال la charge", "commande": "play_until", "parametres": {"moment": "circuit"}},
                {"mot": "السطر الأول", "commande": "play_until", "parametres": {"moment": "additivite"}},
                {"mot": "u R plus u C égale E", "cible": "centre:0"},
                {"mot": "السطر الثاني", "commande": "play_until", "parametres": {"moment": "ohm"}},
                {"mot": "السطر الثالث", "commande": "play_until", "parametres": {"moment": "intensite"}},
                {"mot": "السطر الرابع", "commande": "play_until", "parametres": {"moment": "remplacer"}},
                {"mot": "plus u C، égale E. هادي هي", "cible": "centre:1"},
                {"mot": "هادي هي l'équation différentielle", "commande": "play_until", "parametres": {"moment": "resultat"}}]),
    diapo_sim("ex_s2", "Question 2 : τ est un temps", "[R] = [U]/[I], [C] = [I]·[T]/[U], donc [R]·[C] = [T].",
      SIMD + "figures.html?fig=fig_dimension", "La dimension de R, de C, puis du produit",
      "علاش tau هي le temps؟ نشوفو les dimensions. الأول R: la loi d'Ohm، u égale R fois i، إذن la dimension de R، c'est U sur I. الثاني C: i égale C dé u sur dé t، إذن la dimension de C، c'est I fois T sur U. دابا نضربوهم: U sur I، fois I fois T sur U. U كتمشي مع U، و I مع I، وكيبقى غير T. إذن R C é q، homogène à un temps، و tau كتقاس بla seconde.",
      centre=[("[R]·[C] = [T]", "وكيبقى غير T")],
      pointage=[{"mot": "الأول R", "commande": "play_until", "parametres": {"moment": "R"}},
                {"mot": "الثاني C", "commande": "play_until", "parametres": {"moment": "C"}},
                {"mot": "دابا نضربوهم", "commande": "play_until", "parametres": {"moment": "produit"}},
                {"mot": "وكيبقى غير T", "cible": "centre:0"}]),
    diapo_sim("ex_s3", "Question 3 : τ par la tangente", "La tangente à l'origine coupe l'asymptote u_C = E à t = τ = 0,3 s.",
      SIMD + "courbe-charge.html?vue=tangente", "R = 3 kΩ, C = 100 µF, E = 12 V : la tangente à l'origine et l'asymptote",
      "هادي la courbe ديال la charge، مع R égale trois kiloohms، C égale cent microfarads، و E égale douze volts. u C كتطلع وكتقرب من l'asymptote، u C égale E، يعني douze volts. دابا la tangente à l'origine: كتطلع نيشان، وكتلاقى l'asymptote. من هاد النقطة كنهبطو لl'axe des temps، وكنقراو tau égale zéro virgule trois seconde. رد البال لl'unité ديال l'axe: كل graduation فيها zéro virgule un seconde.",
      centre=[("τ = 0,3 s", "وكنقراو tau égale zéro virgule trois seconde")],
      pointage=[avec(REG_T, "هادي la courbe ديال la charge"),
                {"mot": "u C كتطلع وكتقرب", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "من l'asymptote", "commande": "play_until", "parametres": {"moment": "asymptote"}},
                {"mot": "دابا la tangente à l'origine", "commande": "play_until", "parametres": {"moment": "tangente"}},
                {"mot": "وكنقراو tau égale zéro virgule trois seconde", "repere": "tau"},
                {"mot": "وكنقراو tau égale zéro virgule trois seconde", "cible": "centre:0"},
                {"mot": "رد البال لl'unité ديال l'axe", "repere": "axe_t"}]),
    diapo_sim("ex_s4", "Question 4 : C_eq = τ/R", "C_eq = τ/R = 0,3/(3·10³) = 10⁻⁴ F = 100 µF.",
      SIMD + "tau-rc.html", "Avec R = 3 kΩ et C = 100 µF, la charge donne bien τ = 0,3 s",
      "tau égale R fois C é q، إذن C é q égale tau sur R. tau égale zéro virgule trois seconde، و R égale trois fois dix puissance trois ohm. C é q égale zéro virgule trois، sur trois fois dix puissance trois، يعني dix puissance moins quatre farad، cent microfarads. نتأكدو: نديرو R égale trois kiloohms، و C égale cent microfarads. شوف la courbe: tau كيبان فين u C كتوصل à soixante-trois pour cent من E، و هو zéro virgule trois seconde. نفس النتيجة.",
      centre=[("C_eq = τ/R", "إذن C é q égale tau sur R"), ("C_eq = 0,3/(3·10³) = 10⁻⁴ F = 100 µF", "يعني dix puissance moins quatre farad")],
      pointage=[{"mot": "إذن C é q égale tau sur R", "cible": "centre:0"},
                {"mot": "يعني dix puissance moins quatre farad", "cible": "centre:1"},
                avec(REG_RC, "نديرو R égale trois kiloohms"),
                {"mot": "شوف la courbe", "repere": "courbe"},
                {"mot": "tau كيبان فين u C", "repere": "tau"}]),
    diapo_sim("ex_s5", "Question 5 : deux condensateurs en série", "En série : 1/C_eq = 1/C₁ + 1/C₂ ; C₂ = 150 µF.",
      SIMD + "figures.html?fig=fig_serie", "En série : même charge q, les tensions s'ajoutent",
      "شوف deux condensateurs en série: عندهم نفس la charge q. les tensions كيتزادو: u égale u un plus u deux. كل tension هي q sur C، إذن un sur C é q égale un sur C un plus un sur C deux. يلا كانو غير deux condensateurs: C é q égale C un fois C deux، sur C un plus C deux. حنا عارفين C é q و C un، إذن un sur C deux égale un sur C é q moins un sur C un. C deux égale trois cents fois cent، sur trois cents moins cent، يعني cent cinquante microfarads. رد البال: la série كتنقص la capacité، C é q صغر من C un و من C deux.",
      centre=[("1/C_eq = 1/C₁ + 1/C₂", "إذن un sur C é q égale un sur C un plus un sur C deux"), ("C₂ = 300 × 100/(300 − 100) = 150 µF", "يعني cent cinquante microfarads")],
      pointage=[{"mot": "شوف deux condensateurs en série", "commande": "play_until", "parametres": {"moment": "circuit"}},
                {"mot": "les tensions كيتزادو", "commande": "play_until", "parametres": {"moment": "tensions"}},
                {"mot": "إذن un sur C é q égale un sur C un plus un sur C deux", "commande": "play_until", "parametres": {"moment": "formule"}},
                {"mot": "إذن un sur C é q égale un sur C un plus un sur C deux", "cible": "centre:0"},
                {"mot": "يلا كانو غير deux condensateurs", "commande": "play_until", "parametres": {"moment": "deux"}},
                {"mot": "يعني cent cinquante microfarads", "cible": "centre:1"},
                {"mot": "la série كتنقص la capacité", "commande": "play_until", "parametres": {"moment": "interet"}}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_s1", "Plus facile : la bonne équation", "سؤال ساهل: اختار l'équation différentielle ديال la charge.",
      "Pendant la charge sous E, u_C vérifie l'équation…",
      ["R·C·du_C/dt − u_C = E", "du_C/dt + R·C·u_C = E", "R·C·du_C/dt + u_C = E"], 2, {
        "2": {"juste": rep("مزيان! من u R plus u C égale E، مع u R égale R C dé u C sur dé t.", "Juste : u_R + u_C = E avec u_R = R·C·du_C/dt.")},
        "0": {"1": rep("ما تقلقش. l'additivité كتجمع les tensions: u R plus u C égale E. واش كاين moins؟ عاود اختار.", "L'additivité ajoute les tensions : u_R + u_C = E. Réessaie."),
              "2": rep("الجواب هو R C dé u C sur dé t، plus u C، égale E. les tensions كيتزادو، ما كاينش moins.", "Réponse : R·C·du_C/dt + u_C = E (les tensions s'ajoutent).")},
        "1": {"1": rep("قريب. ولكن R C خاصها تكون قدام la dérivée، حيت u R égale R fois i، و i فيها la dérivée. عاود اختار.", "R·C doit multiplier la dérivée, car u_R = R·i et i = C·du_C/dt. Réessaie."),
              "2": rep("الجواب هو R C dé u C sur dé t، plus u C، égale E. R C كتضرب la dérivée، ماشي u C.", "Réponse : R·C·du_C/dt + u_C = E.")}},
      "Pendant la charge, u C vérifie quelle équation ?"),
    vrai_faux_facile("fa_s2", "Plus facile : vrai ou faux", "سؤال ساهل على les dimensions: قول صحيح ولا غالط.",
      "Dimensions de R, de C et de τ = R·C.",
      [("D'après u_R = R·i, la dimension de R est [U]/[I].", True, "R = u_R/i, donc [R] = [U]/[I]."),
       ("D'après i = C·du_C/dt, la dimension de C est [U]/[I].", False, "C = i·dt/du_C, donc [C] = [I]·[T]/[U]."),
       ("Le produit R·C a la dimension d'un temps : τ s'exprime en secondes.", True, "[R]·[C] = ([U]/[I])·([I]·[T]/[U]) = [T].")]),
    qcm_facile("fa_s3", "Plus facile : lire τ sur la tangente", "سؤال ساهل على la tangente à l'origine.",
      "Sur la courbe de charge u_C(t), τ est l'abscisse du point où la tangente à l'origine coupe…",
      ["l'asymptote u_C = E", "l'axe des temps", "la courbe u_C(t)"], 0, {
        "0": {"juste": rep("برافو! la tangente à l'origine كتلاقى l'asymptote u C égale E فt égale tau.", "Juste : (T) coupe l'asymptote u_C = E à t = τ.")},
        "1": {"1": rep("ما تقلقش. la tangente ديال la charge كتطلع من l'origine، ما كترجعش لl'axe des temps. فين كتحبس؟ عاود اختار.", "La tangente d'une courbe qui monte part de l'origine et ne recoupe pas l'axe des temps. Réessaie."),
              "2": rep("الجواب هو l'asymptote u C égale E. l'axe des temps كيصلح غير للمنحنيات اللي كتهبط، بحال la décharge.", "Réponse : l'asymptote u_C = E (l'axe des temps sert pour les courbes qui descendent).")},
        "2": {"1": rep("قريب. la tangente كتمس la courbe فl'origine، ومن بعد كتبعد عليها. شوف الخط الأفقي. عاود اختار.", "La tangente touche la courbe à l'origine puis s'en écarte. Regarde la droite horizontale. Réessaie."),
              "2": rep("الجواب هو l'asymptote u C égale E. tau est l'abscisse du point d'intersection، de la tangente avec l'asymptote.", "Réponse : l'asymptote u_C = E.")}},
      "Sur la courbe de charge, tau est l'abscisse du point où la tangente à l'origine coupe quoi ?"),
    qcm_facile("fa_s4", "Plus facile : C à partir de τ", "سؤال ساهل: نحسبو la capacité من tau.",
      "τ = 0,3 s et R = 3 kΩ. La capacité C vaut…",
      ["900 F", "1·10⁻⁴ F", "0,1 F"], 1, {
        "1": {"juste": rep("مزيان! C égale tau sur R، يعني zéro virgule trois sur trois mille، كتعطي dix puissance moins quatre farad.", "Juste : C = τ/R = 0,3/3000 = 10⁻⁴ F.")},
        "0": {"1": rep("ما تقلقش. هنا ضربتي R فtau. ولكن tau égale R fois C، إذن C هي tau sur R. عاود اختار.", "Tu as multiplié R par τ ; or C = τ/R. Réessaie."),
              "2": rep("الجواب هو dix puissance moins quatre farad. C égale tau sur R.", "Réponse : C = τ/R = 10⁻⁴ F.")},
        "2": {"1": rep("قريب. قسمتي على trois، ولكن R égale trois kiloohms، يعني trois mille ohms. عاود اختار.", "Tu as divisé par 3 au lieu de 3000 : 3 kΩ = 3·10³ Ω. Réessaie."),
              "2": rep("الجواب هو dix puissance moins quatre farad. ما تنساش kilo égale mille.", "Réponse : C = 0,3/(3·10³) = 10⁻⁴ F (kilo = 10³).")}},
      "Tau égale zéro virgule trois seconde et R égale trois kiloohms. La capacité C vaut ?"),
    qcm_facile("fa_s5", "Plus facile : condensateurs en série", "سؤال ساهل على la série.",
      "C₁ = 300 µF et C₂ sont en série ; C_eq = 100 µF. Alors C₂ vaut…",
      ["200 µF", "400 µF", "150 µF"], 2, {
        "2": {"juste": rep("برافو! un sur C deux égale un sur cent moins un sur trois cents، كتعطي C deux égale cent cinquante microfarads.", "Juste : 1/C₂ = 1/100 − 1/300 ⇒ C₂ = 150 µF.")},
        "0": {"1": rep("ما تقلقش. طرحتي les capacités بحال le parallèle. en série، les inverses هوما اللي كيتزادو. عاود اختار.", "Tu as soustrait les capacités comme en parallèle ; en série, ce sont les inverses qui s'ajoutent. Réessaie."),
              "2": rep("الجواب هو cent cinquante microfarads. en série، un sur C é q égale un sur C un plus un sur C deux.", "Réponse : 150 µF, car 1/C_eq = 1/C₁ + 1/C₂.")},
        "1": {"1": rep("قريب. ولكن la série كتنقص la capacité، و C deux ماشي مجموع. استعمل les inverses. عاود اختار.", "La série diminue la capacité ; utilise les inverses. Réessaie."),
              "2": rep("الجواب هو cent cinquante microfarads. un sur C deux égale un sur cent moins un sur trois cents.", "Réponse : 1/C₂ = 1/100 − 1/300, C₂ = 150 µF.")}},
      "C un égale trois cents microfarads، و C deux en série، و C équivalente égale cent microfarads. C deux vaut ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec E = 10 V, R = 5 kΩ, C₁ = 120 µF et C₂ inconnue, en série. Les condensateurs sont initialement déchargés ; à t = 0, on ferme K. La figure 2 donne u_C(t) et la tangente (T) à l'origine.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale dix volts، R égale cinq kiloohms، و C un égale cent vingt microfarads، en série مع C deux. فt égale zéro كنسدو K.",
      "figures": [charge_tangente(10, 0.15, 0.8, 0.1, "Figure 2 : u_C(t) et la tangente (T)")],
      "donnees": ["E = 10 V", "R = 5 kΩ = 5·10³ Ω", "C₁ = 120 µF"],
      "questions": [
        question_semblable("1", "Établir l'équation différentielle vérifiée par u_C(t) pendant la charge.",
          phrase(ED_ATT), ["u_R + u_C = E", "u_R = R·i", "i = C_eq·du_C/dt"], ["i = C_eq·u_C"],
          corr([("1 : u_R + u_C = E (additivité) ; u_R = R·i ; i = C_eq·du_C/dt", "u R plus u C égale E"),
                ("R·C_eq·du_C/dt + u_C = E", "R C é q fois dé u C sur dé t، plus u C، égale E")],
               "l'additivité: u R plus u C égale E. مع u R égale R i، و i égale C é q dé u C sur dé t: R C é q fois dé u C sur dé t، plus u C، égale E.")),
        question_semblable("2", "Par une analyse dimensionnelle, montrer que τ = R·C_eq a la dimension d'un temps.",
          phrase(DIM_ATT), ["[R] = [U]/[I]", "[C] = [I]·[T]/[U]"], ["[C] = [U]/[I]"],
          corr([("2 : [R] = [U]/[I] ; [C] = [I]·[T]/[U]", "la dimension de R، U sur I"), ("[R]·[C] = [T] : un temps", "كيبقى غير T")],
               "la dimension de R، U sur I، و ديال C، I fois T sur U، كنضربوهم وكيبقى غير T.")),
        question_semblable("3", "Déterminer graphiquement la valeur de τ.",
          valeur("τ", 0.15, "s", "τ = 0,15 s"), ["tangente à l'origine", "asymptote u_C = E"], ["axe des temps"],
          corr([("3 : (T) coupe l'asymptote u_C = E = 10 V à t = τ", "la tangente كتلاقى l'asymptote"), ("τ = 0,15 s", "tau égale zéro virgule quinze seconde")],
               "la tangente كتلاقى l'asymptote u C égale dix volts. كنهبطو: tau égale zéro virgule quinze seconde.")),
        question_semblable("4", "En déduire la valeur de C_eq.",
          valeur("C_eq", 3e-5, "F", "C_eq = τ/R = 0,15/(5·10³) = 3·10⁻⁵ F"), ["C_eq = τ/R", "F"], ["C_eq = R·τ"],
          corr([("4 : C_eq = τ/R = 0,15/(5·10³)", "C é q égale tau sur R"), ("C_eq = 3·10⁻⁵ F = 30 µF", "trois fois dix puissance moins cinq farad")],
               "C é q égale tau sur R، يعني zéro virgule quinze، sur cinq fois dix puissance trois. C é q égale trois fois dix puissance moins cinq farad، trente microfarads.")),
        question_semblable("5", "Les condensateurs étant en série, déterminer la valeur de C₂.",
          valeur("C₂", 4e-5, "F", "C₂ = C₁·C_eq/(C₁ − C_eq) = 120 × 30/(120 − 30) µF = 40 µF = 4·10⁻⁵ F"), ["1/C_eq = 1/C₁ + 1/C₂", "µF"], ["C₂ = C₁ − C_eq"],
          corr([("5 : 1/C₂ = 1/C_eq − 1/C₁", "un sur C deux égale un sur C é q moins un sur C un"), ("C₂ = 120 × 30/90 = 40 µF", "C deux égale quarante microfarads")],
               "un sur C deux égale un sur C é q moins un sur C un. C deux égale cent vingt fois trente، sur quatre-vingt-dix. C deux égale quarante microfarads.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
