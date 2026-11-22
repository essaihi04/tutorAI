# Exercice de physique, ch. 8 (oscillations libres d'un circuit RLC série), niveau difficile n° 7 :
# un circuit LC idéal étudié par la courbe i(t) : signe de i, φ de i(t), L ET C à partir de T₀ et de I_m (deux relations
# combinées : énergie + période propre), puis |u_C| quand E_e = E_m.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture backend/data/curriculum/architecture/phys_ch8_circuit_RLC.md,
#    fiche du cadre circuit_RLC (RLC1 : signe de i ; RLC4 : φ par les conditions initiales ; RLC5 ; RLC6 : conservation),
#    docs/parties_voix/phys_ch8_circuit_RLC.json.
#  - cours phys_ch8_circuit_RLC : lc_d5_signe et lc_c5_courant (i = C·du_C/dt, signe), lc_c4_sens (le sens de départ choisit
#    φ), lc_en3_echange (I_m = E·√(C/L), E_e = E_m à T₀/8), lc_e8_T0.
#  - nationaux : 2020 N (i(t) = I_m·cos(2πt/T₀ + φ) : I_m, T₀, φ lus sur la courbe ; E_t = ½·L·I_m²), 2019 N et 2023 N
#    (énergie totale du LC, u_C à un instant) ; ici L et C sont tous deux inconnus : deux relations à combiner (supérieur).
#  - séries en ligne : recherche faite (talamidi, moutamadris, Naceiri, dreamjob) mais PDF non joignables depuis cette session ;
#    nos données sont celles de solution.html et energie.html (E = 6 V, L = 0,1 H, C = 4 µF, I_m ≈ 38 mA, T₀ = 4 ms).
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch8_rlc_7"
SIMD = "/media/simulations/physics/circuit-rlc-tableau/"


def grille(tmax, dt, ymin, ymax, dy):
    els, k = [], 0
    while k * dt <= tmax + 1e-9:
        els.append({"f": "ligne", "pts": [[round(k * dt, 4), ymin], [round(k * dt, 4), ymax]], "couleur": "faible"}); k += 1
    k = 0
    while ymin + k * dy <= ymax + 1e-9:
        y = round(ymin + k * dy, 4); els.append({"f": "ligne", "pts": [[0, y], [tmax, y]], "couleur": "faible"}); k += 1
    return els


def courbe_i(titre, Im_mA, T0ms, tmax, imax, dt, di):
    """i(t) = I_m·cos(2πt/T₀ + π/2) = −I_m·sin(2πt/T₀) : départ en décharge (i orienté vers l'armature A)."""
    els = grille(tmax, dt, -imax, imax, di) + [
        {"f": "courbe", "expr": f"-{Im_mA}*sin(2*pi*x/{T0ms})", "de": 0, "a": tmax, "couleur": "vert", "texte": "i(t)", "texte_x": tmax * 0.95},
        {"f": "point", "at": [T0ms / 4, -Im_mA], "t": f"−{fr(Im_mA)} mA", "pos": "s", "couleur": "jaune"}]
    return figure_courbe(titre, axe("t", 0, tmax, "ms", list(range(0, tmax + 1, dt))),
                         axe("i", -imax, imax, "mA", list(range(-imax, imax + 1, di))), els,
                         legende="i est orienté vers l'armature A du condensateur (figure 1).")


def fr(v):
    return (f"{v:g}").replace(".", ",")


def montage(titre):
    g = [dipole([0.8, 0.8], [0.8, 3.6], "G", "E", pos="o"),
         fil([0.8, 3.6], [2.9, 3.6]),
         inverseur([3.4, 2.8], [2.9, 3.6], [3.9, 3.6], t="K", pos_t=[3.95, 2.75]),
         dipole([3.4, 2.8], [3.4, 0.8], "C", "C", pos="e"),
         borne([3.4, 2.05], "A", "o"), borne([3.4, 0.8], "B", "s"),
         tension([2.1, 1.2], [2.1, 2.4], "u_C", pos="o"),
         fil([3.9, 3.6], [7.6, 3.6]),
         dipole([7.6, 3.6], [7.6, 0.8], "L", "L", pos="o"),
         fil([7.6, 0.8], [0.8, 0.8]),
         courant([4.1, 0.8], "d")]
    return schema(titre, 9.2, 4.6, *g)


# ---------------------------------------------------------------- données et calculs (π² = 10)
E, IM, T0 = 6, 38e-3, 4e-3                      # E donné ; I_m et T₀ lus
L = T0 * E / (2 * math.pi * IM)                  # ≈ 0,1005 H
L_AN = 0.1
C = T0 ** 2 / (40 * L_AN)                        # 4·10⁻⁶ F
UC = E / math.sqrt(2)                            # 4,24 V
assert abs(L - 0.1) / 0.1 < 0.01 and abs(C - 4e-6) < 1e-15 and abs(UC - 4.243) < 1e-3
assert abs(E * math.sqrt(4e-6 / 0.1) * 1000 - 37.95) < 0.01      # la courbe vient bien de L = 0,1 H, C = 4 µF
FIG = courbe_i("Figure 2 : l'intensité i(t)", 38, 4, 10, 50, 1, 10)
# semblable : E = 8 V, L = 0,25 H, C = 10 µF : I_m = 8·√(4·10⁻⁵) ≈ 50,6 mA, T₀ = 10 ms
Eb, IMb, T0b = 8, 50.6e-3, 10e-3
Lb = T0b * Eb / (2 * math.pi * IMb); Cb = T0b ** 2 / (40 * 0.25); UCb = Eb / math.sqrt(2)
assert abs(Lb - 0.25) / 0.25 < 0.01 and abs(Cb - 1e-5) < 1e-15 and abs(8 * math.sqrt(1e-5 / 0.25) * 1000 - 50.6) < 0.01
FIGB = courbe_i("Figure 2 : l'intensité i(t)", 50.6, 10, 25, 60, 5, 10)

SIGNE = ("i = dq/dt = C·du_C/dt. À t = 0, u_C = E est maximale (tangente horizontale) : du_C/dt = 0, donc i(0) = 0. "
         "Juste après, le condensateur se décharge : u_C diminue, du_C/dt < 0, donc i < 0 (le courant circule dans le sens "
         "opposé au sens choisi, il sort de l'armature A).")
MONTRER = ("Sans résistance, l'énergie se conserve : ½·C·E² = ½·L·I_m², donc C = L·I_m²/E². Avec T₀ = 2π√(LC) : "
           "T₀ = 2π√(L²·I_m²/E²) = 2π·L·I_m/E, donc L = E·T₀/(2π·I_m).")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "circuit_RLC", "cours": "phys_ch8_circuit_RLC",
  "titre": "Retrouver L et C à partir de la courbe i(t)", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Justifier le signe de i = C·du_C/dt", "Déterminer φ de i(t) par les conditions initiales",
                  "Combiner la conservation de l'énergie et T₀ = 2π√(LC) pour trouver L et C", "Calculer u_C quand E_e = E_m"],
  "enonce": {
    "intro": "Un condensateur de capacité C inconnue est chargé sous la tension E = 6 V (K en position 1). À t = 0, on bascule K en position 2 : il se décharge dans une bobine d'inductance L inconnue et de résistance négligeable (figure 1). Un capteur enregistre l'intensité i(t), orientée vers l'armature A (figure 2). On écrit i(t) = I_m·cos(2πt/T₀ + φ).",
    "intro_dit": "دابا نقراو l'énoncé. un condensateur، la capacité ديالو C ما معروفاش، مشارجي تحت E égale six volts. فt égale zéro، كنبدلو K لla position deux: كيتفرغ فbobine، l'inductance ديالها L ما معروفاش، وla résistance ديالها مهملة. un capteur كيسجل l'intensité i، موجهة نحو l'armature A، فla figure deux. وكنكتبو i égale I m cosinus de deux pi t sur T zéro، plus phi.",
    "figures": [montage("Figure 1 : le montage (circuit LC)"), FIG],
    "donnees": ["E = 6 V", "Résistance du circuit négligeable", "On prend π² = 10."],
    "questions": [
      question("1", "En utilisant la relation i = C·du_C/dt, justifier que i(0) = 0 et que i est négative juste après t = 0.",
        "السؤال un: بla relation i égale C dé u C sur dé t، علل علاش i de zéro égale zéro، وعلاش i سالبة مباشرة من بعد t égale zéro.",
        phrase(SIGNE),
        ["i = C·du_C/dt", "u_C(0) = E", "tangente horizontale", "du_C/dt < 0"], ["i(0) = E/R", "i > 0 pendant la décharge"],
        [aide("À t = 0, u_C vaut E, sa valeur la plus grande : que vaut la pente de la courbe u_C(t) en un maximum ?",
              "فt égale zéro، u C égale E، أكبر قيمة ديالها. شحال la pente ديال la courbe فmaximum؟"),
         aide("Pente nulle ⇒ du_C/dt = 0 ⇒ i(0) = 0. Ensuite le condensateur se décharge : u_C diminue, donc du_C/dt < 0.",
              "la pente zéro، إذن dé u C sur dé t égale zéro، وi de zéro égale zéro. من بعد le condensateur كيتفرغ: u C كتنقص، إذن dé u C sur dé t سالبة.")],
        corr([("1 : i = C·du_C/dt ; à t = 0, u_C = E est maximale : du_C/dt = 0 ⇒ i(0) = 0", "i de zéro égale zéro"),
              ("Juste après, u_C diminue (décharge) : du_C/dt < 0 ⇒ i < 0", "i سالبة"),
              ("Le courant circule dans le sens opposé à l'orientation : il sort de l'armature A.", "كيخرج من l'armature A")],
             "السؤال un. i égale C dé u C sur dé t. فt égale zéro، u C égale E، فأكبر قيمة: la tangente أفقية، إذن i de zéro égale zéro. من بعد le condensateur كيتفرغ، u C كتنقص، وla dérivée سالبة: i سالبة. يعني le courant كيخرج من l'armature A، عكس الاتجاه اللي اخترنا."),
        "ex_lc7_1", "fa_lc7_1"),
      question("2", "Relever I_m et T₀ sur la figure 2, puis déterminer φ (en rad).",
        "السؤال deux: اقرا I m وT zéro فla figure deux، ومن بعد حدد phi بle radian.",
        valeur("φ", 1.57, "rad", "I_m = 38 mA ; T₀ = 4 ms ; i(0) = I_m·cos φ = 0 ⇒ φ = ±π/2 ; i décroît au départ : di/dt(0) = −(2π/T₀)·I_m·sin φ < 0 ⇒ sin φ > 0 ⇒ φ = π/2 ≈ 1,57 rad"),
        ["i(0) = I_m·cos φ", "±π/2", "sin φ > 0", "di/dt(0)", "rad"], ["φ = −π/2", "φ = 0", "I_m = 76 mA"],
        [aide("I_m est la plus grande valeur de |i| ; T₀ la durée d'une oscillation complète. Écris i(0) = I_m·cos φ = 0 : deux angles conviennent.",
              "I m هي أكبر قيمة ديال i بla valeur absolue، وT zéro هي المدة ديال oscillation كاملة. كتب i de zéro égale I m cosinus phi égale zéro: كاينين les deux angles."),
         aide("i diminue juste après t = 0 : di/dt(0) = −(2π/T₀)·I_m·sin φ < 0, donc sin φ > 0.",
              "i كتنقص مباشرة من بعد zéro: dé i sur dé t en zéro، égale moins deux pi sur T zéro fois I m sinus phi، سالبة. إذن sinus phi موجب.")],
        corr([("2 : I_m = 38 mA ; T₀ = 4 ms", "I m égale trente-huit milliampères"),
              ("i(0) = I_m·cos φ = 0 ⇒ cos φ = 0 ⇒ φ = π/2 ou φ = −π/2", "cosinus phi égale zéro"),
              ("i décroît : di/dt(0) = −(2π/T₀)·I_m·sin φ < 0 ⇒ sin φ > 0", "sinus phi موجب"),
              ("φ = π/2 ≈ 1,57 rad", "phi égale pi sur deux")],
             "السؤال deux. كنقراو I m égale trente-huit milliampères، وT zéro égale quatre millisecondes. i de zéro égale I m cosinus phi égale zéro، إذن cosinus phi égale zéro: phi égale pi sur deux، ولا moins pi sur deux. i كتنقص فالبداية، إذن la dérivée سالبة، وsinus phi موجب. إذن phi égale pi sur deux، environ un virgule cinquante-sept radian."),
        "ex_lc7_2", "fa_lc7_2"),
      question("3", "En exprimant de deux façons l'énergie totale du circuit, montrer que L = E·T₀/(2π·I_m), puis calculer L.",
        "السؤال trois: كتب l'énergie totale بجوج طرق، وبين بلي L égale E fois T zéro، sur deux pi I m. ومن بعد حسب L.",
        valeur("L", 0.1, "H", "½·C·E² = ½·L·I_m² ⇒ C = L·I_m²/E² ; T₀ = 2π√(LC) = 2π·L·I_m/E ⇒ L = E·T₀/(2π·I_m) = 6 × 4·10⁻³/(2π × 38·10⁻³) ≈ 0,10 H"),
        ["½·C·E² = ½·L·I_m²", "T₀ = 2π√(LC)", "L = E·T₀/(2π·I_m)", "10⁻³", "H"], ["L = T₀/(2π·I_m)", "L = 2π·I_m/(E·T₀)", "I_m = 38 A"],
        [aide("Au départ, toute l'énergie est dans le condensateur ; quand |i| = I_m (u_C = 0), toute l'énergie est dans la bobine. L'énergie se conserve : égale les deux.",
              "فالبداية، l'énergie كلها فle condensateur. وملي i égale I m، يعني u C égale zéro، l'énergie كلها فla bobine. l'énergie ثابتة: ساوي بيناتهم."),
         aide("½·C·E² = ½·L·I_m² donne C = L·I_m²/E². Remplace C dans T₀ = 2π√(LC) : la racine de L² · I_m²/E² est L·I_m/E.",
              "un demi C E au carré égale un demi L I m au carré، إذن C égale L I m au carré sur E au carré. عوض C فT zéro égale deux pi racine de L C: la racine ديال L au carré I m au carré sur E au carré هي L I m sur E.")],
        corr([("3 : conservation : ½·C·E² = ½·L·I_m² ⇒ C = L·I_m²/E²", "un demi C E au carré égale un demi L I m au carré"),
              ("T₀ = 2π√(LC) = 2π√(L²·I_m²/E²) = 2π·L·I_m/E ⇒ L = E·T₀/(2π·I_m)", "L égale E T zéro sur deux pi I m"),
              ("A.N. : L = 6 × 4·10⁻³/(2π × 38·10⁻³) ≈ 0,10 H", "L environ zéro virgule un henry")],
             "السؤال trois. l'énergie ثابتة: un demi C E au carré égale un demi L I m au carré، إذن C égale L I m au carré sur E au carré. كنعوضو فT zéro égale deux pi racine de L C: T zéro égale deux pi L I m sur E. إذن L égale E T zéro sur deux pi I m. يعني six fois quatre fois dix puissance moins trois، sur deux pi fois trente-huit fois dix puissance moins trois. L environ zéro virgule un henry."),
        "ex_lc7_3", "fa_lc7_3"),
      question("4", "En déduire la capacité C du condensateur (prendre L = 0,1 H).",
        "السؤال quatre: استنتج la capacité C ديال le condensateur، وخود L égale zéro virgule un henry.",
        valeur("C", 4e-6, "F", "C = T₀²/(4π²·L) = (4·10⁻³)²/(40 × 0,1) = 4·10⁻⁶ F"),
        ["C = T₀²/(4π²L)", "C = L·I_m²/E²", "π² = 10", "F", "µF"], ["C = T₀/(2πL)", "C = 4 F"],
        [aide("Tu connais maintenant T₀ et L : utilise la période propre, mise au carré.",
              "دابا عندك T zéro وL: استعمل la période propre، وطلعها au carré."),
         aide("C = T₀²/(4π²·L), avec T₀ en secondes et 4π² = 40. Vérifie avec C = L·I_m²/E².",
              "C égale T zéro au carré، sur quatre pi carré fois L، وT zéro بla seconde، et quatre pi carré égale quarante. تأكد بC égale L I m au carré sur E au carré.")],
        corr([("4 : C = T₀²/(4π²·L)", "C égale T zéro au carré، sur quatre pi carré fois L"),
              ("A.N. : C = (4·10⁻³)²/(40 × 0,1) = 4·10⁻⁶ F = 4 µF", "C égale quatre microfarads"),
              ("Vérification : L·I_m²/E² = 0,1 × (38·10⁻³)²/36 ≈ 4·10⁻⁶ F", "نفس القيمة")],
             "السؤال quatre. C égale T zéro au carré، sur quatre pi carré fois L. يعني seize fois dix puissance moins six، sur quarante fois zéro virgule un. C égale quatre microfarads. وبالطريقة الأخرى، L I m au carré sur E au carré، كتعطي نفس القيمة."),
        "ex_lc7_4", "fa_lc7_4"),
      question("5", "Calculer la valeur absolue de u_C aux instants où l'énergie est également partagée entre le condensateur et la bobine (E_e = E_m).",
        "السؤال cinq: حسب la valeur absolue ديال u C فles instants فين l'énergie مقسومة بالنص بين le condensateur وla bobine، يعني E e égale E m.",
        valeur("|u_C|", 4.24, "V", "E_e = E_m = E_t/2 ⇒ ½·C·u_C² = ½ × ½·C·E² ⇒ |u_C| = E/√2 = 6/√2 ≈ 4,24 V"),
        ["E_e + E_m = ½·C·E²", "E_e = E_t/2", "√2", "V"], ["|u_C| = E/2 = 3 V", "|u_C| = E/4"],
        [aide("L'énergie totale vaut ½·C·E². Si E_e = E_m, chacune vaut la moitié de l'énergie totale.",
              "l'énergie totale هي un demi C E au carré. إلى كانت E e égale E m، كل وحدة هي النص ديال l'énergie totale."),
         aide("½·C·u_C² = ¼·C·E², donc u_C² = E²/2 : |u_C| = E/√2, pas E/2.",
              "un demi C u C au carré égale un quart C E au carré. إذن u C au carré égale E au carré sur deux، وu C égale E sur racine de deux، ماشي E sur deux.")],
        corr([("5 : E_e = E_m et E_e + E_m = ½·C·E² ⇒ E_e = ¼·C·E²", "E e égale un quart C E au carré"),
              ("½·C·u_C² = ¼·C·E² ⇒ u_C² = E²/2", "u C au carré égale E au carré sur deux"),
              ("|u_C| = E/√2 = 6/√2 ≈ 4,24 V", "environ quatre virgule vingt-quatre volts")],
             "السؤال cinq. E e égale E m، والمجموع un demi C E au carré: إذن E e égale un quart C E au carré. un demi C u C au carré égale un quart C E au carré، إذن u C au carré égale E au carré sur deux. u C égale six sur racine de deux، environ quatre virgule vingt-quatre volts. رد البال: ماشي E sur deux، حيت l'énergie فيها le carré."),
        "ex_lc7_5", "fa_lc7_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_lc7_1", "Question 1 : le signe de i", "i = C·du_C/dt : nul au sommet, négatif quand u_C descend.",
      SIMD + "solution.html?vue=cos", "u_C(t) en rouge, i(t) en vert : u_C descend → i < 0",
      "شوف la courbe الحمرا، u C، وتحتها la courbe الخضرا، i. فt égale zéro، u C فle sommet، six volts، وla tangente أفقية: la pente zéro. وi égale C dé u C sur dé t، إذن i de zéro égale zéro. من بعد، u C كتهبط: la pente سالبة، إذن i سالبة. ملي u C كتطلع، i موجبة. هادا هو اللي كاين فla figure deux ديالك: i كتبدا من zéro وكتمشي للسالب.",
      centre=[("i = C·du_C/dt", "وi égale C dé u C sur dé t"),
              ("Sommet : du_C/dt = 0 ⇒ i(0) = 0", "إذن i de zéro égale zéro"),
              ("u_C descend ⇒ i < 0", "la pente سالبة، إذن i سالبة")],
      pointage=[{"mot": "شوف la courbe الحمرا", "commande": "play_until", "parametres": {"moment": "courbe"}},
                {"mot": "وتحتها la courbe الخضرا", "commande": "play_until", "parametres": {"moment": "signe_i"}},
                {"mot": "وتحتها la courbe الخضرا", "repere": "courbe_i"},
                {"mot": "وi égale C dé u C sur dé t", "cible": "centre:0"},
                {"mot": "إذن i de zéro égale zéro", "cible": "centre:1"},
                {"mot": "la pente سالبة، إذن i سالبة", "repere": "signe_i"},
                {"mot": "la pente سالبة، إذن i سالبة", "cible": "centre:2"}]),
    diapo_sim("ex_lc7_2", "Question 2 : φ de i(t)", "i(0) = 0 et i décroît : φ = +π/2.",
      SIMD + "solution.html?vue=cos", "La courbe i(t) verte : I_m ≈ 38 mA, départ à zéro en descendant",
      "شوف la courbe الخضرا ديال i: أكبر قيمة ديالها I m، environ trente-huit milliampères، وT zéro environ quatre millisecondes. فt égale zéro، i égale zéro: I m cosinus phi égale zéro، إذن cosinus phi égale zéro، وphi égale plus pi sur deux ولا moins pi sur deux. باش نختارو، كنشوفو الاتجاه: i كتهبط فالبداية، إذن la dérivée سالبة: moins deux pi sur T zéro fois I m sinus phi سالبة، يعني sinus phi موجب. إذن phi égale plus pi sur deux.",
      centre=[("i(0) = I_m·cos φ = 0 ⇒ φ = ±π/2", "إذن cosinus phi égale zéro"),
              ("i décroît ⇒ sin φ > 0 ⇒ φ = π/2", "إذن phi égale plus pi sur deux")],
      pointage=[{"mot": "شوف la courbe الخضرا ديال i", "commande": "play_until", "parametres": {"moment": "signe_i"}},
                {"mot": "environ trente-huit milliampères", "repere": "courbe_i"},
                {"mot": "إذن cosinus phi égale zéro", "cible": "centre:0"},
                {"mot": "i كتهبط فالبداية", "repere": "signe_i"},
                {"mot": "إذن phi égale plus pi sur deux", "cible": "centre:1"}]),
    diapo_sim("ex_lc7_3", "Question 3 : deux relations pour L", "½·C·E² = ½·L·I_m² et T₀ = 2π√(LC) ⇒ L = E·T₀/(2π·I_m).",
      SIMD + "energie.html?vue=echange", "Toute l'énergie dans le condensateur (u_C = E), puis toute dans la bobine (i = I_m)",
      "شوف فالبداية: كلشي فle condensateur، un demi C E au carré، soixante-douze microjoules. دابا u C égale zéro: كلشي فla bobine، un demi L I m au carré. l'énergie ثابتة، إذن un demi C E au carré égale un demi L I m au carré، وC égale L I m au carré sur E au carré. كنعوضو فT zéro égale deux pi racine de L C: كيبقى T zéro égale deux pi L I m sur E. إذن L égale E T zéro sur deux pi I m. هنا six fois quatre fois dix puissance moins trois، sur deux pi fois trente-huit fois dix puissance moins trois: environ zéro virgule un henry، هي la bobine ديال هاد la simulation.",
      centre=[("½·C·E² = ½·L·I_m² ⇒ C = L·I_m²/E²", "وC égale L I m au carré sur E au carré"),
              ("T₀ = 2π√(LC) = 2π·L·I_m/E", "كيبقى T zéro égale deux pi L I m sur E"),
              ("L = E·T₀/(2π·I_m) ≈ 0,10 H", "environ zéro virgule un henry")],
      pointage=[{"mot": "شوف فالبداية", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "كلشي فle condensateur", "repere": "barre_Ee"},
                {"mot": "دابا u C égale zéro", "commande": "play_until", "parametres": {"moment": "tout_bobine"}},
                {"mot": "كلشي فla bobine", "repere": "barre_Em"},
                {"mot": "وC égale L I m au carré sur E au carré", "cible": "centre:0"},
                {"mot": "كيبقى T zéro égale deux pi L I m sur E", "cible": "centre:1"},
                {"mot": "environ zéro virgule un henry", "cible": "centre:2"}]),
    diapo_sim("ex_lc7_4", "Question 4 : C par la période propre", "C = T₀²/(4π²L) = 4 µF.",
      SIMD + "solution.html?vue=cos", "T₀ = 2π√(LC) avec L = 0,1 H et C = 4 µF : 4 ms",
      "شوف التعريف: deux pi sur T zéro au carré égale un sur L C. إذن T zéro égale deux pi racine de L C. دابا عندنا T zéro وL، إذن C égale T zéro au carré، sur quatre pi carré fois L. يعني quatre fois dix puissance moins trois، au carré، sur quarante fois zéro virgule un. C égale quatre microfarads، هي la capacité ديال هاد la simulation، وكتعطي بالضبط T zéro égale quatre millisecondes.",
      centre=[("C = T₀²/(4π²·L)", "إذن C égale T zéro au carré، sur quatre pi carré fois L"),
              ("C = (4·10⁻³)²/(40 × 0,1) = 4·10⁻⁶ F", "C égale quatre microfarads")],
      pointage=[{"mot": "شوف التعريف", "commande": "play_until", "parametres": {"moment": "identification"}},
                {"mot": "deux pi sur T zéro au carré égale un sur L C", "repere": "identification"},
                {"mot": "إذن C égale T zéro au carré، sur quatre pi carré fois L", "cible": "centre:0"},
                {"mot": "C égale quatre microfarads", "cible": "centre:1"},
                {"mot": "T zéro égale quatre millisecondes", "repere": "resultat"}]),
    diapo_sim("ex_lc7_5", "Question 5 : E_e = E_m", "Chacune vaut 36 µJ : ½·C·u_C² = ¼·C·E² ⇒ |u_C| = E/√2.",
      SIMD + "energie.html?vue=echange", "À T₀/8, les deux courbes se croisent : E_e = E_m = 36 µJ",
      "شوف les deux courbes: الحمرا كتنقص والخضرا كتزيد. هنا كيتلاقاو: E e égale E m، كل وحدة trente-six microjoules، النص ديال soixante-douze. إذن un demi C u C au carré égale un quart C E au carré، وu C au carré égale E au carré sur deux. u C égale E sur racine de deux: six sur racine de deux، environ quatre virgule vingt-quatre volts. ماشي trois volts: l'énergie فيها le carré.",
      centre=[("E_e = E_m = E_t/2 = 36 µJ", "كل وحدة trente-six microjoules"),
              ("½·C·u_C² = ¼·C·E² ⇒ |u_C| = E/√2 ≈ 4,24 V", "environ quatre virgule vingt-quatre volts")],
      pointage=[{"mot": "شوف les deux courbes", "commande": "play_until", "parametres": {"moment": "echange"}},
                {"mot": "الحمرا كتنقص", "repere": "courbe_Ee"},
                {"mot": "والخضرا كتزيد", "repere": "courbe_Em"},
                {"mot": "كل وحدة trente-six microjoules", "cible": "centre:0"},
                {"mot": "environ quatre virgule vingt-quatre volts", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_lc7_1", "Plus facile : i au départ", "سؤال ساهل: شحال i فt égale zéro؟",
      "Au moment de la bascule, u_C = E est maximale. D'après i = C·du_C/dt, i(0) vaut…",
      ["E/L", "0", "I_m"], 1, {
        "1": {"juste": rep("برافو! فle sommet la pente zéro، إذن i de zéro égale zéro.", "Juste : pente nulle au sommet, i(0) = 0.")},
        "0": {"1": rep("E sur L ما عندهاش l'unité ديال l'intensité. فكر فla pente ديال u C فle sommet. عاود اختار.", "E/L n'est pas une intensité. Pense à la pente de u_C au sommet. Réessaie."),
              "2": rep("الجواب: zéro. la tangente أفقية فle sommet، dé u C sur dé t égale zéro.", "Réponse : i(0) = 0, la tangente est horizontale.")},
        "2": {"1": rep("I m كتوصل ليها i ملي u C égale zéro، ماشي فالبداية. عاود اختار.", "i = ±I_m quand u_C = 0, pas au départ. Réessaie."),
              "2": rep("الجواب: zéro. فالبداية u C فle sommet.", "Réponse : i(0) = 0 (u_C au sommet).")}},
      "Au moment de la bascule, u C égale E est maximale. i de zéro vaut ?"),
    qcm_facile("fa_lc7_2", "Plus facile : φ de i(t)", "سؤال ساهل: اختار phi ديال i.",
      "i(0) = 0 et i devient négative juste après. Pour i = I_m·cos(2πt/T₀ + φ), φ vaut…",
      ["+π/2", "−π/2", "0"], 0, {
        "0": {"juste": rep("برافو! cosinus phi égale zéro، وi كتهبط، إذن sinus phi موجب: plus pi sur deux.", "Juste : cos φ = 0 et sin φ > 0 : φ = π/2.")},
        "1": {"1": rep("cosinus ديال moins pi sur deux حتى هو zéro. ولكن مع moins pi sur deux، i كتطلع ولا كتهبط؟ عاود اختار.", "cos(−π/2) = 0 aussi, mais alors i croîtrait au départ. Réessaie."),
              "2": rep("الجواب: plus pi sur deux. la dérivée فيها moins sinus phi، باش تكون سالبة خاص sinus phi موجب.", "Réponse : φ = +π/2 (di/dt(0) < 0 impose sin φ > 0).")},
        "2": {"1": rep("phi égale zéro كتعطي i de zéro égale I m، ماشي zéro. عاود اختار.", "φ = 0 donnerait i(0) = I_m, pas 0. Réessaie."),
              "2": rep("الجواب: plus pi sur deux.", "Réponse : φ = π/2.")}},
      "i de zéro égale zéro et i devient négative. phi vaut ?"),
    qcm_facile("fa_lc7_3", "Plus facile : la conservation", "سؤال ساهل على l'énergie ديال le circuit LC.",
      "Dans le circuit LC idéal, quelle égalité est vraie ?",
      ["½·C·E = ½·L·I_m", "½·C·E² = ½·L·I_m²", "C·E² = L·I_m"], 1, {
        "1": {"juste": rep("برافو! l'énergie اللي كانت فle condensateur كتولي كاملة فla bobine.", "Juste : ½·C·E² = ½·L·I_m².")},
        "0": {"1": rep("نسيتي les carrés: l'énergie فيها u au carré وi au carré. عاود اختار.", "Il manque les carrés. Réessaie."),
              "2": rep("الجواب: un demi C E au carré égale un demi L I m au carré.", "Réponse : ½·C·E² = ½·L·I_m².")},
        "2": {"1": rep("الجيهة ديال la bobine خاص فيها I m au carré. عاود اختار.", "Côté bobine, I_m doit être au carré. Réessaie."),
              "2": rep("الجواب: un demi C E au carré égale un demi L I m au carré.", "Réponse : ½·C·E² = ½·L·I_m².")}},
      "Dans le circuit L C idéal, quelle égalité est vraie ?"),
    qcm_facile("fa_lc7_4", "Plus facile : calculer C", "سؤال ساهل: حسب C.",
      "T₀ = 4 ms, L = 0,1 H, π² = 10. C vaut…",
      ["16 µF", "4 F", "4 µF"], 2, {
        "2": {"juste": rep("برافو! seize fois dix puissance moins six، sur quatre، quatre microfarads.", "Juste : C = 16·10⁻⁶/4 = 4·10⁻⁶ F.")},
        "0": {"1": rep("فالمقام quatre pi carré، يعني quarante، ماشي dix. عاود اختار.", "Au dénominateur : 4π² = 40, pas 10. Réessaie."),
              "2": rep("الجواب: quatre microfarads، مع quatre pi carré égale quarante.", "Réponse : 4 µF (4π² = 40).")},
        "1": {"1": rep("T zéro خاصها تكون بla seconde. عاود اختار.", "T₀ doit être en secondes. Réessaie."),
              "2": rep("الجواب: quatre microfarads، T zéro égale quatre fois dix puissance moins trois seconde.", "Réponse : 4 µF, avec T₀ = 4·10⁻³ s.")}},
      "T zéro égale quatre millisecondes, L égale zéro virgule un henry. C vaut ?"),
    qcm_facile("fa_lc7_5", "Plus facile : E_e = E_m", "سؤال ساهل: شحال u C ملي E e égale E m؟",
      "E = 6 V. Quand E_e = E_m, |u_C| vaut…",
      ["3 V", "4,24 V", "6 V"], 1, {
        "1": {"juste": rep("برافو! six sur racine de deux، environ quatre virgule vingt-quatre volts.", "Juste : |u_C| = E/√2 ≈ 4,24 V.")},
        "0": {"1": rep("E sur deux كتعطي un quart ديال l'énergie، ماشي النص، حيت كاين le carré. عاود اختار.", "E/2 donne le quart de l'énergie (à cause du carré), pas la moitié. Réessaie."),
              "2": rep("الجواب: E sur racine de deux، environ quatre virgule vingt-quatre volts.", "Réponse : E/√2 ≈ 4,24 V.")},
        "2": {"1": rep("six volts يعني كلشي فle condensateur، وE m égale zéro. عاود اختار.", "À 6 V, toute l'énergie est dans le condensateur. Réessaie."),
              "2": rep("الجواب: six sur racine de deux، environ quatre virgule vingt-quatre volts.", "Réponse : 6/√2 ≈ 4,24 V.")}},
      "E égale six volts. Quand E e égale E m, u C vaut ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même expérience : le condensateur est chargé sous E = 8 V, puis il se décharge dans une bobine de résistance négligeable. La figure 2 donne i(t), orientée vers l'armature A. i(t) = I_m·cos(2πt/T₀ + φ) ; π² = 10.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale huit volts، وla courbe ديال i فla figure deux.",
      "figures": [FIGB],
      "donnees": ["E = 8 V", "π² = 10"],
      "questions": [
        question_semblable("1", "Justifier que i(0) = 0 et que i est négative juste après t = 0.",
          phrase(SIGNE), ["i = C·du_C/dt"], ["i > 0"],
          corr([("1 : u_C(0) = E maximale ⇒ du_C/dt = 0 ⇒ i(0) = 0 ; ensuite u_C diminue ⇒ i < 0", "i سالبة")],
               "فt égale zéro، u C فle sommet، إذن i de zéro égale zéro. من بعد u C كتنقص، إذن i سالبة.")),
        question_semblable("2", "Relever I_m et T₀, puis déterminer φ (en rad).",
          valeur("φ", 1.57, "rad", "I_m ≈ 50,6 mA ; T₀ = 10 ms ; cos φ = 0 et sin φ > 0 ⇒ φ = π/2 ≈ 1,57 rad"), ["±π/2", "sin φ > 0"], ["φ = −π/2"],
          corr([("2 : I_m ≈ 50,6 mA ; T₀ = 10 ms", "T zéro égale dix millisecondes"), ("φ = π/2 ≈ 1,57 rad", "phi égale pi sur deux")],
               "I m environ cinquante virgule six milliampères، T zéro égale dix millisecondes. i de zéro égale zéro وكتنقص: phi égale pi sur deux.")),
        question_semblable("3", "Montrer que L = E·T₀/(2π·I_m), puis calculer L.",
          valeur("L", 0.25, "H", "L = E·T₀/(2π·I_m) = 8 × 10⁻²/(2π × 50,6·10⁻³) ≈ 0,25 H"), ["L = E·T₀/(2π·I_m)", "H"], ["L = T₀/(2π·I_m)"],
          corr([("3 : ½·C·E² = ½·L·I_m² et T₀ = 2π√(LC) ⇒ L = E·T₀/(2π·I_m)", "L égale E T zéro sur deux pi I m"), ("L ≈ 0,25 H", "zéro virgule vingt-cinq henry")],
               "l'énergie ثابتة وT zéro égale deux pi racine de L C، إذن L égale E T zéro sur deux pi I m. L environ zéro virgule vingt-cinq henry.")),
        question_semblable("4", "En déduire C (prendre L = 0,25 H).",
          valeur("C", 1e-5, "F", "C = T₀²/(4π²·L) = (10⁻²)²/(40 × 0,25) = 1·10⁻⁵ F"), ["C = T₀²/(4π²L)", "F"], ["C = T₀/(2πL)"],
          corr([("4 : C = (10⁻²)²/(40 × 0,25)", "C égale T zéro au carré"), ("C = 10⁻⁵ F = 10 µF", "C égale dix microfarads")],
               "C égale T zéro au carré، sur quarante fois zéro virgule vingt-cinq. C égale dix microfarads.")),
        question_semblable("5", "Calculer |u_C| quand E_e = E_m.",
          valeur("|u_C|", 5.66, "V", "|u_C| = E/√2 = 8/√2 ≈ 5,66 V"), ["E/√2", "V"], ["E/2 = 4 V"],
          corr([("5 : ½·C·u_C² = ¼·C·E² ⇒ |u_C| = E/√2", "E sur racine de deux"), ("|u_C| ≈ 5,66 V", "cinq virgule soixante-six volts")],
               "un demi C u C au carré égale un quart C E au carré، إذن u C égale E sur racine de deux، environ cinq virgule soixante-six volts.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
