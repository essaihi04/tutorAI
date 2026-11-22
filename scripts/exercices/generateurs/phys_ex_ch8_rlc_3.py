# Exercice de physique, ch. 8 (oscillations libres d'un circuit RLC série), niveau moyen n° 3 :
# le circuit LC idéal : établir l'équation en u_C, montrer T₀ = 2π√(LC), lire T₀ → C, trouver U_m et φ, l'énergie totale.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture backend/data/curriculum/architecture/phys_ch8_circuit_RLC.md
#    (« établir l'équation » très fréquent, « lire T puis L ou C » 13 sessions, « énergie » 14 sessions), fiche du cadre
#    circuit_RLC (RLC3, RLC4 : U_m et φ par les conditions initiales, RLC6), docs/parties_voix/phys_ch8_circuit_RLC.json.
#  - cours phys_ch8_circuit_RLC : lc_e4_equation_uc, lc_e5_lc_ideal, lc_e7_deriver, lc_e8_T0, lc_c3_angles et lc_c4_sens
#    (u_C(0) = 3 V, U_m = 6 V : φ = ±π/3, le sens de départ choisit), lc_en2_depart.
#  - nationaux : 2017 R et 2021 N (q(t) solution → T₀), 2022 N (« trouver l'expression de T₀ », « E_t »), 2020 N (I_m, T₀, φ
#    lus sur la courbe), 2019 N (E_t du LC) : même chaîne de questions, autre situation (départ à 3 V, en montant).
#  - séries en ligne : recherche faite (talamidi, moutamadris, Naceiri, dreamjob) mais PDF non joignables depuis cette session ;
#    nos données sont celles de solution.html (L = 0,1 H, C = 4 µF, U_m = 6 V, u_C(0) = 3 V, φ = −π/3).
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch8_rlc_3"
SIMD = "/media/simulations/physics/circuit-rlc-tableau/"


def grille(tmax, dt, ymin, ymax, dy):
    els, k = [], 0
    while k * dt <= tmax + 1e-9:
        els.append({"f": "ligne", "pts": [[round(k * dt, 4), ymin], [round(k * dt, 4), ymax]], "couleur": "faible"}); k += 1
    k = 0
    while ymin + k * dy <= ymax + 1e-9:
        y = round(ymin + k * dy, 4); els.append({"f": "ligne", "pts": [[0, y], [tmax, y]], "couleur": "faible"}); k += 1
    return els


def sinusoide(titre, Um, T0ms, phi, tmax, umax, dt, du, legende):
    expr = f"{Um}*cos(2*pi*x/{T0ms}+({phi:.6f}))"
    els = grille(tmax, dt, -umax, umax, du) + [{"f": "courbe", "expr": expr, "de": 0, "a": tmax, "couleur": "rouge", "texte": "u_C(t)", "texte_x": tmax * 0.93}]
    return figure_courbe(titre, axe("t", 0, tmax, "ms", list(range(0, tmax + 1, dt))),
                         axe("u_C", -umax, umax, "V", list(range(-umax, umax + 1, du))), els, legende=legende)


# ---------------------------------------------------------------- données et calculs (π² = 10)
L, UM, U0, T0 = 0.1, 6, 3, 4e-3
C = T0 ** 2 / (40 * L)
PHI = -math.acos(U0 / UM)                       # départ en montant : sin φ < 0
E_TOT = 0.5 * C * UM ** 2
assert abs(C - 4e-6) < 1e-15 and abs(PHI + math.pi / 3) < 1e-12 and abs(E_TOT - 7.2e-5) < 1e-15
assert -2 * math.pi / T0 * UM * math.sin(PHI) > 0                  # u_C croît à t = 0
FIG = sinusoide("Figure 2 : u_C(t) enregistrée", UM, 4, PHI, 10, 8, 1, 2, "u_C(0) = 3 V et u_C croît juste après t = 0.")
# semblable : L = 0,5 H, T₀ = 10 ms, U_m = 8 V, u_C(0) = −4 V en descendant
Lb, UMb, U0b, T0b = 0.5, 8, -4, 10e-3
Cb = T0b ** 2 / (40 * Lb); PHIb = math.acos(U0b / UMb); Eb = 0.5 * Cb * UMb ** 2
assert abs(Cb - 5e-6) < 1e-15 and abs(PHIb - 2 * math.pi / 3) < 1e-12 and abs(Eb - 1.6e-4) < 1e-15
assert -2 * math.pi / T0b * UMb * math.sin(PHIb) < 0               # u_C décroît à t = 0
FIGB = sinusoide("Figure 2 : u_C(t) enregistrée", UMb, 10, PHIb, 25, 10, 5, 2, "u_C(0) = −4 V et u_C décroît juste après t = 0.")


def montage(titre, legende=None):
    """K en 1 : charge par E ; K en 2 : décharge dans la bobine seule (résistance négligeable). i orienté vers A."""
    g = [dipole([0.8, 0.8], [0.8, 3.6], "G", "E", pos="o"),
         fil([0.8, 3.6], [2.9, 3.6]),
         inverseur([3.4, 2.8], [2.9, 3.6], [3.9, 3.6], t="K", pos_t=[3.95, 2.75]),
         dipole([3.4, 2.8], [3.4, 0.8], "C", "C", pos="e"),
         borne([3.4, 2.05], "A", "o"), borne([3.4, 0.8], "B", "s"),
         tension([2.1, 1.2], [2.1, 2.4], "u_C", pos="o"),
         fil([3.9, 3.6], [7.6, 3.6]),
         dipole([7.6, 3.6], [7.6, 0.8], "L", "L", pos="o"),
         tension([8.3, 3.2], [8.3, 1.2], "u_L", pos="e"),
         fil([7.6, 0.8], [0.8, 0.8]),
         courant([4.1, 0.8], "d")]
    return schema(titre, 9.8, 4.6, *g, legende=legende)


EQ = ("Additivité des tensions (K en 2, sans générateur) : u_C + u_L = 0, avec u_L = L·di/dt (r = 0) et "
      "i = dq/dt = C·du_C/dt, donc di/dt = C·d²u_C/dt². D'où L·C·d²u_C/dt² + u_C = 0, soit d²u_C/dt² + (1/(LC))·u_C = 0.")
SOL = ("du_C/dt = −(2π/T₀)·U_m·sin(2πt/T₀ + φ) ; d²u_C/dt² = −(2π/T₀)²·U_m·cos(2πt/T₀ + φ) = −(2π/T₀)²·u_C. "
       "En remplaçant : [1/(LC) − (2π/T₀)²]·u_C = 0 pour tout t, donc (2π/T₀)² = 1/(LC) et T₀ = 2π√(LC).")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "circuit_RLC", "cours": "phys_ch8_circuit_RLC",
  "titre": "Le circuit LC idéal : équation, solution et conditions initiales", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir l'équation différentielle en u_C du circuit LC", "Montrer que T₀ = 2π√(LC)", "Lire T₀ et calculer C",
                  "Déterminer U_m et φ par les conditions initiales", "Calculer l'énergie totale"],
  "enonce": {
    "intro": "Un condensateur de capacité C est chargé (K en position 1), puis on bascule K en position 2 : il se décharge dans une bobine d'inductance L = 0,1 H et de résistance négligeable (figure 1). L'acquisition de u_C(t) commence un peu plus tard, à un instant pris comme origine des dates t = 0 (figure 2). La solution de l'équation différentielle s'écrit u_C(t) = U_m·cos(2πt/T₀ + φ).",
    "intro_dit": "دابا نقراو l'énoncé. un condensateur، la capacité ديالو C، كنشارجيوه وK فla position un. من بعد كنبدلو K لla position deux: le condensateur كيتفرغ فbobine، l'inductance ديالها L égale zéro virgule un henry، وla résistance ديالها مهملة. هادي la figure un. l'enregistrement ديال u C كيبدا من بعد شوية، فلحظة اللي خديناها origine des dates، t égale zéro. هادي la figure deux. la solution ديال l'équation différentielle هي u C égale U m fois cosinus de deux pi t sur T zéro، plus phi.",
    "figures": [montage("Figure 1 : le montage (circuit LC)"), FIG],
    "donnees": ["L = 0,1 H (résistance de la bobine négligeable)", "On prend π² = 10."],
    "questions": [
      question("1", "Établir l'équation différentielle vérifiée par la tension u_C(t) lorsque K est en position 2.",
        "السؤال un: بين l'équation différentielle اللي كتحققها la tension u C ملي K فla position deux.",
        phrase(EQ),
        ["u_C + u_L = 0", "u_L = L·di/dt", "i = C·du_C/dt", "d²u_C/dt²", "1/(LC)"], ["u_C + u_L = E", "i = dq/dt = q/C", "d²u_C/dt² − u_C/(LC) = 0"],
        [aide("K est en position 2 : y a-t-il un générateur dans la maille ? Écris la loi d'additivité des tensions, puis la tension de chaque dipôle.",
              "K فla position deux: واش كاين générateur فهاد la maille؟ كتب la loi d'additivité des tensions، ومن بعد la tension ديال كل dipôle."),
         aide("u_C + u_L = 0 ; u_L = L·di/dt ; i = C·du_C/dt, donc di/dt = C·d²u_C/dt². Remplace, puis divise par LC.",
              "u C plus u L égale zéro. u L égale L dé i sur dé t. وi égale C dé u C sur dé t، إذن dé i sur dé t égale C dé deux u C sur dé t deux. عوض، ومن بعد قسم على L C.")],
        corr([("1 : additivité : u_C + u_L = 0 (pas de générateur)", "u C plus u L égale zéro"),
              ("u_L = L·di/dt et i = C·du_C/dt ⇒ u_L = LC·d²u_C/dt²", "u L égale L C dé deux u C sur dé t deux"),
              ("LC·d²u_C/dt² + u_C = 0 ⇒ d²u_C/dt² + (1/(LC))·u_C = 0", "dé deux u C sur dé t deux، plus un sur L C fois u C، égale zéro")],
             "السؤال un. ما كاينش générateur، إذن la loi d'additivité: u C plus u L égale zéro. la bobine résistance ديالها مهملة: u L égale L dé i sur dé t. وi égale C dé u C sur dé t. إذن u L égale L C dé deux u C sur dé t deux. كنقسمو على L C: dé deux u C sur dé t deux، plus un sur L C fois u C، égale zéro."),
        "ex_lc3_1", "fa_lc3_1"),
      question("2", "Montrer que u_C(t) = U_m·cos(2πt/T₀ + φ) est solution de cette équation si T₀ = 2π√(LC).",
        "السؤال deux: بين بلي u C égale U m cosinus de deux pi t sur T zéro plus phi، هي solution ديال هاد l'équation، إلى كانت T zéro égale deux pi racine de L C.",
        phrase(SOL),
        ["du_C/dt", "−(2π/T₀)·U_m·sin", "d²u_C/dt² = −(2π/T₀)²·u_C", "(2π/T₀)² = 1/(LC)"], ["du_C/dt = (2π/T₀)·U_m·sin", "T₀ = 2π·LC"],
        [aide("Dérive deux fois u_C : la dérivée de cos(at + φ) est −a·sin(at + φ), avec a = 2π/T₀.",
              "دير la dérivée deux fois ل u C: la dérivée ديال cosinus de a t plus phi هي moins a sinus de a t plus phi، وa égale deux pi sur T zéro."),
         aide("Tu trouves d²u_C/dt² = −(2π/T₀)²·u_C. Remplace dans l'équation : u_C se met en facteur, et le crochet doit être nul.",
              "غادي تلقى dé deux u C sur dé t deux égale moins deux pi sur T zéro au carré fois u C. عوض فl'équation: u C كتخرج facteur، وخاص ما بين les crochets يكون zéro.")],
        corr([("2 : du_C/dt = −(2π/T₀)·U_m·sin(2πt/T₀ + φ)", "la première dérivée"),
              ("d²u_C/dt² = −(2π/T₀)²·u_C", "moins deux pi sur T zéro au carré fois u C"),
              ("[1/(LC) − (2π/T₀)²]·u_C = 0 pour tout t ⇒ (2π/T₀)² = 1/(LC) ⇒ T₀ = 2π√(LC)", "إذن T zéro égale deux pi racine de L C")],
             "السؤال deux. la première dérivée: moins deux pi sur T zéro، fois U m، fois sinus. la deuxième dérivée: moins deux pi sur T zéro au carré fois u C. كنعوضو فl'équation: u C fois، un sur L C moins deux pi sur T zéro au carré، égale zéro، فكل لحظة. إذن deux pi sur T zéro au carré égale un sur L C. إذن T zéro égale deux pi racine de L C."),
        "ex_lc3_2", "fa_lc3_2"),
      question("3", "Déterminer graphiquement la période propre T₀, puis calculer la capacité C du condensateur.",
        "السؤال trois: حدد مبيانيا la période propre T zéro، ومن بعد حسب la capacité C ديال le condensateur.",
        valeur("C", 4e-6, "F", "T₀ = 4 ms ; C = T₀²/(4π²·L) = (4·10⁻³)²/(40 × 0,1) = 4·10⁻⁶ F"),
        ["T₀ = 2π√(LC)", "C = T₀²/(4π²L)", "10⁻³", "π² = 10", "F", "µF"], ["C = T₀/(2πL)", "T₀ = 2 ms", "C = 4 F"],
        [aide("T₀ est la durée au bout de laquelle u_C reprend la même valeur en variant dans le même sens : par exemple de t = 0 (3 V, en montant) jusqu'au retour à 3 V en montant. Écris-la en secondes.",
              "T zéro هي المدة اللي من بعدها u C كترجع لنفس القيمة وبنفس الاتجاه. مثلا من t égale zéro، trois volts وهي طالعة، حتى ترجع à trois volts وهي طالعة. كتبها بla seconde."),
         aide("T₀² = 4π²·L·C, donc C = T₀²/(4π²·L), avec 4π² = 40.",
              "T zéro au carré égale quatre pi carré fois L fois C. إذن C égale T zéro au carré، sur quatre pi carré fois L، et quatre pi carré égale quarante.")],
        corr([("3 : u_C reprend la valeur 3 V en croissant à t = 0 et à t = 4 ms (même durée entre deux maximums) : T₀ = 4 ms = 4·10⁻³ s", "T zéro égale quatre millisecondes"),
              ("C = T₀²/(4π²·L)", "C égale T zéro au carré، sur quatre pi carré fois L"),
              ("A.N. : C = (4·10⁻³)²/(40 × 0,1) = 4·10⁻⁶ F = 4 µF", "C égale quatre microfarads")],
             "السؤال trois. u C كترجع à trois volts وهي طالعة، فt égale zéro et à quatre millisecondes. إذن T zéro égale quatre millisecondes، يعني quatre fois dix puissance moins trois seconde. C égale T zéro au carré، sur quatre pi carré fois L. يعني seize fois dix puissance moins six، sur quarante fois zéro virgule un. C égale quatre microfarads."),
        "ex_lc3_3", "fa_lc3_3"),
      question("4", "Relever U_m, puis déterminer la phase φ (en rad) à l'aide des conditions initiales.",
        "السؤال quatre: اقرا U m، ومن بعد حدد la phase phi بle radian، بالشروط البدئية.",
        valeur("φ", -1.05, "rad", "U_m = 6 V ; u_C(0) = U_m·cos φ = 3 V ⇒ cos φ = 0,5 ⇒ φ = ±π/3 ; u_C croît à t = 0 ⇒ du_C/dt(0) = −(2π/T₀)·U_m·sin φ > 0 ⇒ sin φ < 0 ⇒ φ = −π/3 ≈ −1,05 rad"),
        ["u_C(0) = U_m·cos φ", "cos φ = 0,5", "±π/3", "sin φ", "du_C/dt(0)", "rad"], ["φ = 0", "φ = +π/3", "U_m = 12 V"],
        [aide("U_m est la hauteur d'un sommet. À t = 0, lis u_C(0) et écris u_C(0) = U_m·cos φ : deux angles conviennent.",
              "U m هي العلو ديال sommet. فt égale zéro، اقرا u C de zéro، وكتب u C de zéro égale U m cosinus phi: كاينين les deux angles."),
         aide("Pour choisir, regarde le sens de départ : u_C croît, donc du_C/dt(0) = −(2π/T₀)·U_m·sin φ > 0, donc sin φ < 0.",
              "باش تختار، شوف الاتجاه ديال la courbe فالبداية: u C كتطلع، إذن dé u C sur dé t en zéro، égale moins deux pi sur T zéro fois U m sinus phi، موجبة. إذن sinus phi سالب.")],
        corr([("4 : U_m = 6 V (hauteur d'un sommet)", "U m égale six volts"),
              ("u_C(0) = U_m·cos φ = 3 V ⇒ cos φ = 3/6 = 0,5 ⇒ φ = π/3 ou φ = −π/3", "cosinus phi égale zéro virgule cinq"),
              ("u_C croît à t = 0 : du_C/dt(0) = −(2π/T₀)·U_m·sin φ > 0 ⇒ sin φ < 0", "sinus phi سالب"),
              ("φ = −π/3 ≈ −1,05 rad", "phi égale moins pi sur trois")],
             "السؤال quatre. U m égale six volts، العلو ديال sommet. فt égale zéro، u C de zéro égale trois volts، وu C de zéro égale U m cosinus phi. إذن cosinus phi égale zéro virgule cinq: phi égale plus pi sur trois، ولا moins pi sur trois. la courbe كتطلع فالبداية، إذن la dérivée موجبة، وsinus phi سالب. إذن phi égale moins pi sur trois، environ moins un virgule zéro cinq radian."),
        "ex_lc3_4", "fa_lc3_4"),
      question("5", "Exprimer l'énergie totale E du circuit, puis calculer sa valeur.",
        "السؤال cinq: عطي l'expression ديال l'énergie totale E ديال الدارة، ومن بعد حسب la valeur ديالها.",
        valeur("E", 7.2e-5, "J", "E = ½·C·u_C² + ½·L·i² ; à un sommet i = 0 : E = ½·C·U_m² = ½ × 4·10⁻⁶ × 6² = 7,2·10⁻⁵ J"),
        ["E = ½·C·u_C² + ½·L·i²", "i = 0", "½·C·U_m²", "J"], ["E = ½·C·u_C(0)²", "E = ½·C·U_m", "E = C·U_m²"],
        [aide("L'énergie totale est la somme de l'énergie du condensateur et de celle de la bobine. Sans résistance, elle reste constante : choisis un instant où le calcul est facile.",
              "l'énergie totale هي l'énergie ديال le condensateur، plus l'énergie ديال la bobine. بلا résistance، كتبقى ثابتة: اختار لحظة فين الحساب ساهل."),
         aide("À un sommet de u_C, i = C·du_C/dt = 0 : toute l'énergie est dans le condensateur, E = ½·C·U_m². Attention : à t = 0, i ≠ 0 ici.",
              "فsommet ديال u C، i égale C dé u C sur dé t، égale zéro: l'énergie كلها فle condensateur، E égale un demi C U m au carré. رد البال: فt égale zéro هنا، i ماشي zéro.")],
        corr([("5 : E = ½·C·u_C² + ½·L·i², constante (pas de résistance)", "E égale un demi C u C au carré، plus un demi L i au carré"),
              ("À un sommet, u_C = U_m et i = 0 : E = ½·C·U_m²", "E égale un demi C U m au carré"),
              ("A.N. : E = ½ × 4·10⁻⁶ × 6² = 7,2·10⁻⁵ J", "E égale sept virgule deux fois dix puissance moins cinq joule")],
             "السؤال cinq. E égale un demi C u C au carré، plus un demi L i au carré، وبلا résistance كتبقى ثابتة. فsommet، u C égale U m وi égale zéro. إذن E égale un demi C U m au carré. يعني un demi fois quatre fois dix puissance moins six، fois six au carré. E égale sept virgule deux fois dix puissance moins cinq joule، يعني soixante-douze microjoules."),
        "ex_lc3_5", "fa_lc3_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_lc3_1", "Question 1 : l'équation en u_C", "u_C + u_L = 0 ⇒ d²u_C/dt² + u_C/(LC) = 0.",
      SIMD + "equation.html", "La maille de décharge, puis l'équation en u_C et le cas LC idéal",
      "شوف la maille ديال la décharge: K فla position deux، ما كاينش générateur. فهاد la simulation كاين résistor R وla résistance r ديال la bobine. l'équation en u C كتكتب: L C dé deux u C sur dé t deux، plus R plus r fois C dé u C sur dé t، plus u C égale zéro. دابا فالتمرين ديالك، ما كاينش résistor وr مهملة: le terme ديال الوسط كيتحيد. كيبقى L C dé deux u C sur dé t deux، plus u C égale zéro. كنقسمو على L C: dé deux u C sur dé t deux، plus un sur L C fois u C، égale zéro. هادي l'équation ديال le circuit LC idéal.",
      centre=[("u_C + u_L = 0 ; i = C·du_C/dt", "ما كاينش générateur"),
              ("LC·d²u_C/dt² + u_C = 0", "كيبقى L C dé deux u C sur dé t deux، plus u C égale zéro"),
              ("d²u_C/dt² + (1/(LC))·u_C = 0", "هادي l'équation ديال le circuit LC idéal")],
      pointage=[{"mot": "شوف la maille ديال la décharge", "commande": "play_until", "parametres": {"moment": "fleches"}},
                {"mot": "ما كاينش générateur", "cible": "centre:0"},
                {"mot": "l'équation en u C كتكتب", "commande": "play_until", "parametres": {"moment": "equation_uc"}},
                {"mot": "le terme ديال الوسط كيتحيد", "commande": "play_until", "parametres": {"moment": "lc_ideal"}},
                {"mot": "le terme ديال الوسط", "repere": "terme_milieu"},
                {"mot": "كيبقى L C dé deux u C sur dé t deux، plus u C égale zéro", "cible": "centre:1"},
                {"mot": "هادي l'équation ديال le circuit LC idéal", "cible": "centre:2"}]),
    diapo_sim("ex_lc3_2", "Question 2 : dériver deux fois, identifier", "d²u_C/dt² = −(2π/T₀)²·u_C ⇒ (2π/T₀)² = 1/(LC).",
      SIMD + "solution.html?vue=cos", "La sinusoïde, ses deux dérivées, puis l'identification",
      "شوف la sinusoïde ديال u C. كندير la première dérivée: moins deux pi sur T zéro، fois U m، fois sinus. ومن بعد la deuxième dérivée: moins deux pi sur T zéro au carré، fois U m cosinus، يعني moins deux pi sur T zéro au carré fois u C. كنعوضو فl'équation: u C كتخرج facteur. باش تكون صحيحة فكل لحظة، خاص deux pi sur T zéro au carré égale un sur L C. إذن T zéro égale deux pi racine de L C.",
      centre=[("du_C/dt = −(2π/T₀)·U_m·sin(2πt/T₀ + φ)", "la première dérivée"),
              ("d²u_C/dt² = −(2π/T₀)²·u_C", "يعني moins deux pi sur T zéro au carré fois u C"),
              ("(2π/T₀)² = 1/(LC) ⇒ T₀ = 2π√(LC)", "إذن T zéro égale deux pi racine de L C")],
      pointage=[{"mot": "شوف la sinusoïde ديال u C", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "كندير la première dérivée", "commande": "play_until", "parametres": {"moment": "derivee_1"}},
                {"mot": "la première dérivée", "cible": "centre:0"},
                {"mot": "ومن بعد la deuxième dérivée", "commande": "play_until", "parametres": {"moment": "derivee_2"}},
                {"mot": "يعني moins deux pi sur T zéro au carré fois u C", "cible": "centre:1"},
                {"mot": "كنعوضو فl'équation", "commande": "play_until", "parametres": {"moment": "identification"}},
                {"mot": "إذن T zéro égale deux pi racine de L C", "cible": "centre:2"}]),
    diapo_sim("ex_lc3_3", "Question 3 : lire T₀, trouver C", "T₀ = 4 ms entre deux sommets ; C = T₀²/(4π²L) = 4 µF.",
      SIMD + "solution.html?vue=cos", "T₀ ≈ 4 ms lue entre deux sommets successifs (L = 0,1 H, C = 4 µF)",
      "شوف la courbe: T zéro هي المدة بين deux sommets متتابعين. هنا كنقراو quatre millisecondes. بحال التمرين ديالك، L égale zéro virgule un henry. من T zéro égale deux pi racine de L C، كنطلعو au carré ونعزلو C: C égale T zéro au carré، sur quatre pi carré fois L. يعني quatre fois dix puissance moins trois، au carré، sur quarante fois zéro virgule un. C égale quatre fois dix puissance moins six farad، يعني quatre microfarads.",
      centre=[("T₀ = 4 ms = 4·10⁻³ s", "هنا كنقراو quatre millisecondes"),
              ("C = T₀²/(4π²·L)", "C égale T zéro au carré، sur quatre pi carré fois L"),
              ("C = (4·10⁻³)²/(40 × 0,1) = 4·10⁻⁶ F", "C égale quatre fois dix puissance moins six farad")],
      pointage=[{"mot": "شوف la courbe", "commande": "play_until", "parametres": {"moment": "T0"}},
                {"mot": "T zéro هي المدة بين deux sommets", "repere": "T0"},
                {"mot": "هنا كنقراو quatre millisecondes", "cible": "centre:0"},
                {"mot": "C égale T zéro au carré، sur quatre pi carré fois L", "cible": "centre:1"},
                {"mot": "C égale quatre fois dix puissance moins six farad", "cible": "centre:2"}]),
    diapo_sim("ex_lc3_4", "Question 4 : U_m et φ", "cos φ = 3/6 = 0,5 : φ = ±π/3 ; départ en montant : φ = −π/3.",
      SIMD + "solution.html?vue=phase", "Départ à u_C(0) = 3 V avec U_m = 6 V : deux angles, le sens de départ choisit",
      "شوف هاد la courbe: U m égale six volts، وu C de zéro égale trois volts، بحال التمرين ديالك. u C de zéro égale U m cosinus phi، إذن cosinus phi égale trois sur six، يعني zéro virgule cinq. كاينين les deux angles: plus pi sur trois، et moins pi sur trois. le cosinus ما كيشوفش le signe. شوف الاتجاه ديال la courbe فالبداية: كتطلع. إذن la dérivée موجبة: moins deux pi sur T zéro fois U m sinus phi، أكبر من zéro. إذن sinus phi سالب، وphi égale moins pi sur trois.",
      centre=[("u_C(0) = U_m·cos φ ⇒ cos φ = 3/6 = 0,5", "يعني zéro virgule cinq"),
              ("φ = π/3 ou φ = −π/3", "كاينين les deux angles"),
              ("u_C croît ⇒ sin φ < 0 ⇒ φ = −π/3 rad", "وphi égale moins pi sur trois")],
      pointage=[{"mot": "شوف هاد la courbe", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "u C de zéro égale trois volts", "repere": "point_depart"},
                {"mot": "يعني zéro virgule cinq", "cible": "centre:0"},
                {"mot": "كاينين les deux angles", "commande": "play_until", "parametres": {"moment": "deux_angles"}},
                {"mot": "plus pi sur trois، et moins pi sur trois", "repere": "angles"},
                {"mot": "شوف الاتجاه ديال la courbe فالبداية", "commande": "play_until", "parametres": {"moment": "phi_choisi"}},
                {"mot": "إذن sinus phi سالب", "repere": "phi"},
                {"mot": "وphi égale moins pi sur trois", "cible": "centre:2"}]),
    diapo_sim("ex_lc3_5", "Question 5 : l'énergie totale", "À un sommet, i = 0 : E = ½·C·U_m² = 7,2·10⁻⁵ J.",
      SIMD + "energie.html?vue=echange", "E_e (rouge) et E_m (vert) s'échangent ; leur somme reste à 72 µJ",
      "شوف le graphe ديال l'énergie، وles deux barres: الحمرا ديال le condensateur، والخضرا ديال la bobine. فsommet ديال u C، u C égale six volts وi égale zéro: la barre الخضرا خاوية، وكلشي فle condensateur. إذن E égale un demi C U m au carré. يعني un demi fois quatre fois dix puissance moins six، fois six au carré: sept virgule deux fois dix puissance moins cinq joule. ومن بعد l'énergie كتدوز بين le condensateur وla bobine، ولكن la somme كتبقى ثابتة. رد البال: فالتمرين ديالك، فt égale zéro، u C égale trois volts وi ماشي zéro، إذن ما تحسبش غير un demi C u C de zéro au carré.",
      centre=[("E = ½·C·u_C² + ½·L·i²", "la somme كتبقى ثابتة"),
              ("Sommet : i = 0 ⇒ E = ½·C·U_m² = ½ × 4·10⁻⁶ × 6² = 7,2·10⁻⁵ J", "sept virgule deux fois dix puissance moins cinq joule")],
      pointage=[{"mot": "شوف le graphe ديال l'énergie", "repere": "axe_E"},
                {"mot": "فsommet ديال u C", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "la barre الخضرا خاوية", "repere": "barre_Em"},
                {"mot": "sept virgule deux fois dix puissance moins cinq joule", "cible": "centre:1"},
                {"mot": "ومن بعد l'énergie كتدوز", "commande": "play_until", "parametres": {"moment": "somme_constante"}},
                {"mot": "la somme كتبقى ثابتة", "cible": "centre:0"},
                {"mot": "la somme كتبقى ثابتة", "repere": "courbe_E"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_lc3_1", "Plus facile : l'équation du circuit LC", "نتمرنو بسؤال ساهل: اختار l'équation ديال le circuit LC.",
      "Quelle est l'équation différentielle vérifiée par u_C dans un circuit LC idéal ?",
      ["d²u_C/dt² − u_C/(LC) = 0", "d²u_C/dt² + LC·u_C = 0", "d²u_C/dt² + u_C/(LC) = 0"], 2, {
        "2": {"juste": rep("برافو! dé deux u C sur dé t deux، plus un sur L C fois u C، égale zéro.", "Juste : d²u_C/dt² + u_C/(LC) = 0.")},
        "0": {"1": rep("قريب، ولكن le signe. من u C plus u L égale zéro، واش كيبان moins؟ عاود اختار.", "Vérifie le signe : u_C + LC·d²u_C/dt² = 0. Réessaie."),
              "2": rep("الجواب: plus un sur L C fois u C. من u C plus L C dé deux u C sur dé t deux égale zéro، كلشي بplus.", "Réponse : d²u_C/dt² + u_C/(LC) = 0 (tout est en +).")},
        "1": {"1": rep("ملي كتقسم على L C، L C كتولي فالمقام، ماشي فالبسط. عاود اختار.", "En divisant par LC, LC passe au dénominateur. Réessaie."),
              "2": rep("الجواب: plus un sur L C fois u C، حيت كنقسمو على L C.", "Réponse : d²u_C/dt² + (1/(LC))·u_C = 0.")}},
      "Quelle est l'équation différentielle vérifiée par u C dans un circuit L C idéal ?"),
    vrai_faux_facile("fa_lc3_2", "Plus facile : les dérivées", "سؤال ساهل على les dérivées ديال le cosinus.",
      "u_C = U_m·cos(2πt/T₀ + φ).",
      [("du_C/dt = −(2π/T₀)·U_m·sin(2πt/T₀ + φ).", True, "La dérivée de cos est −sin, et on multiplie par 2π/T₀."),
       ("d²u_C/dt² = +(2π/T₀)²·u_C.", False, "d²u_C/dt² = −(2π/T₀)²·u_C : la dérivée seconde a le signe contraire de u_C."),
       ("La solution convient seulement si (2π/T₀)² = 1/(LC).", True, "C'est la condition qui annule le crochet pour tout t : T₀ = 2π√(LC).")]),
    qcm_facile("fa_lc3_3", "Plus facile : calculer C", "سؤال ساهل: حسب C.",
      "T₀ = 4 ms et L = 0,1 H (π² = 10). La capacité C vaut…",
      ["4 F", "4 µF", "16 µF"], 1, {
        "1": {"juste": rep("برافو! C égale quatre fois dix puissance moins trois au carré، sur quarante fois zéro virgule un، يعني quatre microfarads.", "Juste : C = (4·10⁻³)²/(40 × 0,1) = 4·10⁻⁶ F.")},
        "0": {"1": rep("شوف l'unité ديال T zéro: واش حطيتي quatre ولا quatre fois dix puissance moins trois؟ عاود اختار.", "As-tu converti T₀ en secondes ? Réessaie."),
              "2": rep("الجواب هو quatre microfarads. T zéro خاصها تكون بla seconde: quatre fois dix puissance moins trois.", "Réponse : 4 µF ; T₀ = 4·10⁻³ s, pas 4.")},
        "2": {"1": rep("قريب. ولكن فالمقام quatre pi carré، يعني quarante، ماشي dix. عاود اختار.", "Au dénominateur il y a 4π² = 40, pas π² = 10. Réessaie."),
              "2": rep("الجواب هو quatre microfarads: quatre pi carré égale quarante.", "Réponse : 4 µF, avec 4π² = 40.")}},
      "T zéro égale quatre millisecondes et L égale zéro virgule un henry. La capacité C vaut ?"),
    qcm_facile("fa_lc3_4", "Plus facile : choisir φ", "سؤال ساهل: اختار phi.",
      "U_m = 6 V, u_C(0) = 3 V et u_C croît juste après t = 0. La phase φ vaut…",
      ["+π/3", "0", "−π/3"], 2, {
        "2": {"juste": rep("برافو! cosinus phi égale zéro virgule cinq، وla courbe كتطلع، إذن sinus phi سالب: moins pi sur trois.", "Juste : cos φ = 0,5 et sin φ < 0 : φ = −π/3.")},
        "0": {"1": rep("cosinus ديال plus pi sur trois صحيح zéro virgule cinq. ولكن شوف الاتجاه: إلى كانت phi موجبة، la courbe كتطلع ولا كتهبط؟ عاود اختار.", "cos(π/3) = 0,5, mais avec φ > 0, u_C décroît au départ. Réessaie."),
              "2": rep("الجواب هو moins pi sur trois. la dérivée en zéro فيها moins sinus phi: باش تكون موجبة، خاص sinus phi سالب.", "Réponse : φ = −π/3 ; du_C/dt(0) = −(2π/T₀)·U_m·sin φ > 0 impose sin φ < 0.")},
        "1": {"1": rep("phi égale zéro يعني la courbe كتبدا من le sommet، six volts. هنا كتبدا من trois volts. عاود اختار.", "φ = 0 donnerait u_C(0) = U_m = 6 V, pas 3 V. Réessaie."),
              "2": rep("الجواب هو moins pi sur trois: cosinus phi égale zéro virgule cinq، والطلوع كيعطي sinus phi سالب.", "Réponse : φ = −π/3.")}},
      "U m égale six volts, u C de zéro égale trois volts, et u C croît. La phase phi vaut ?"),
    qcm_facile("fa_lc3_5", "Plus facile : l'énergie totale", "سؤال ساهل على l'énergie totale.",
      "C = 4 µF, U_m = 6 V, u_C(0) = 3 V. L'énergie totale du circuit LC vaut…",
      ["1,8·10⁻⁵ J", "7,2·10⁻⁵ J", "1,2·10⁻⁵ J"], 1, {
        "1": {"juste": rep("برافو! فsommet، i égale zéro، إذن E égale un demi C U m au carré، sept virgule deux fois dix puissance moins cinq joule.", "Juste : E = ½·C·U_m² = 7,2·10⁻⁵ J.")},
        "0": {"1": rep("هادي un demi C u C de zéro au carré. ولكن فt égale zéro، i ماشي zéro: la bobine عندها حتى هي énergie. عاود اختار.", "C'est ½·C·u_C(0)² : à t = 0, i ≠ 0, la bobine a aussi de l'énergie. Réessaie."),
              "2": rep("الجواب: sept virgule deux fois dix puissance moins cinq joule. خود sommet فين i égale zéro.", "Réponse : E = ½·C·U_m² = 7,2·10⁻⁵ J (à un sommet, i = 0).")},
        "2": {"1": rep("نسيتي le carré: E égale un demi C u au carré. عاود اختار.", "Tu as oublié le carré : E = ½·C·U_m². Réessaie."),
              "2": rep("الجواب: un demi fois quatre fois dix puissance moins six fois trente-six، يعني sept virgule deux fois dix puissance moins cinq joule.", "Réponse : ½ × 4·10⁻⁶ × 36 = 7,2·10⁻⁵ J.")}},
      "C égale quatre microfarads, U m égale six volts. L'énergie totale vaut ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage, avec une bobine d'inductance L = 0,5 H (résistance négligeable) et un autre condensateur. L'acquisition commence à un instant pris comme origine des dates (figure 2) : u_C(0) = −4 V et u_C décroît. u_C(t) = U_m·cos(2πt/T₀ + φ) ; π² = 10.",
      "intro_dit": "نفس التمرين، بقيم أخرى. L égale zéro virgule cinq henry، وcondensateur آخر. فt égale zéro، u C égale moins quatre volts، وكتهبط.",
      "figures": [FIGB],
      "donnees": ["L = 0,5 H", "π² = 10"],
      "questions": [
        question_semblable("1", "Établir l'équation différentielle vérifiée par u_C(t) lorsque K est en position 2.",
          phrase(EQ), ["u_C + u_L = 0", "i = C·du_C/dt"], ["u_C + u_L = E"],
          corr([("1 : u_C + L·C·d²u_C/dt² = 0 ⇒ d²u_C/dt² + (1/(LC))·u_C = 0", "dé deux u C sur dé t deux، plus un sur L C fois u C، égale zéro")],
               "u C plus u L égale zéro، وu L égale L C dé deux u C sur dé t deux. إذن dé deux u C sur dé t deux، plus un sur L C fois u C، égale zéro.")),
        question_semblable("2", "Montrer que u_C(t) = U_m·cos(2πt/T₀ + φ) est solution si T₀ = 2π√(LC).",
          phrase(SOL), ["d²u_C/dt² = −(2π/T₀)²·u_C"], ["T₀ = 2π·LC"],
          corr([("2 : d²u_C/dt² = −(2π/T₀)²·u_C ⇒ (2π/T₀)² = 1/(LC) ⇒ T₀ = 2π√(LC)", "T zéro égale deux pi racine de L C")],
               "la deuxième dérivée égale moins deux pi sur T zéro au carré fois u C. إذن deux pi sur T zéro au carré égale un sur L C، وT zéro égale deux pi racine de L C.")),
        question_semblable("3", "Déterminer graphiquement T₀, puis calculer C.",
          valeur("C", 5e-6, "F", "T₀ = 10 ms ; C = T₀²/(4π²·L) = (10⁻²)²/(40 × 0,5) = 5·10⁻⁶ F"), ["C = T₀²/(4π²L)", "F"], ["C = T₀/(2πL)"],
          corr([("3 : T₀ = 10 ms ; C = (10⁻²)²/(40 × 0,5)", "T zéro égale dix millisecondes"), ("C = 5·10⁻⁶ F = 5 µF", "C égale cinq microfarads")],
               "T zéro égale dix millisecondes. C égale dix puissance moins quatre، sur quarante fois zéro virgule cinq. C égale cinq microfarads.")),
        question_semblable("4", "Relever U_m, puis déterminer φ (en rad).",
          valeur("φ", 2.09, "rad", "U_m = 8 V ; cos φ = −4/8 = −0,5 ⇒ φ = ±2π/3 ; u_C décroît ⇒ sin φ > 0 ⇒ φ = 2π/3 ≈ 2,09 rad"), ["cos φ = −0,5", "sin φ > 0", "rad"], ["φ = −2π/3", "φ = π/3"],
          corr([("4 : U_m = 8 V ; cos φ = −0,5 ⇒ φ = ±2π/3", "يعني moins zéro virgule cinq"), ("u_C décroît ⇒ sin φ > 0 ⇒ φ = 2π/3 ≈ 2,09 rad", "phi égale deux pi sur trois")],
               "U m égale huit volts. cosinus phi égale moins quatre sur huit، يعني moins zéro virgule cinq: plus ou moins deux pi sur trois. la courbe كتهبط، إذن sinus phi موجب: phi égale deux pi sur trois، environ deux virgule zéro neuf radians.")),
        question_semblable("5", "Exprimer l'énergie totale E, puis calculer sa valeur.",
          valeur("E", 1.6e-4, "J", "E = ½·C·U_m² = ½ × 5·10⁻⁶ × 8² = 1,6·10⁻⁴ J"), ["E = ½·C·U_m²", "J"], ["E = ½·C·u_C(0)²"],
          corr([("5 : à un sommet i = 0 : E = ½·C·U_m²", "E égale un demi C U m au carré"), ("E = ½ × 5·10⁻⁶ × 64 = 1,6·10⁻⁴ J", "un virgule six fois dix puissance moins quatre joule")],
               "فsommet، i égale zéro: E égale un demi C U m au carré، يعني un demi fois cinq fois dix puissance moins six fois soixante-quatre. E égale un virgule six fois dix puissance moins quatre joule.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
