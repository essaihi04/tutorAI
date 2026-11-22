# Exercice de physique, ch. 8 (oscillations libres d'un circuit RLC série), niveau moyen n° 5 :
# l'entretien des oscillations par un générateur G (u_G = k·i) : équation, k = R + r, u_C(t), I_m, rôle de G.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture backend/data/curriculum/architecture/phys_ch8_circuit_RLC.md
#    (« entretien, k = R + r » : 2018 N, 2020 N), fiche du cadre circuit_RLC (RLC8 : u_G = k·i, fonctionnement interne admis,
#    oscillations à T₀ ; RLC6 : énergie), docs/parties_voix/phys_ch8_circuit_RLC.json.
#  - cours phys_ch8_circuit_RLC : lc_k1_entretien, lc_k2_k (« k = R + r, pas seulement r »), lc_k3_T0, lc_c2_amplitude,
#    lc_en3_echange (I_m = E·√(C/L) ≈ 38 mA).
#  - nationaux : 2016 N (k = 11 → r_b), 2018 N (k = 5 → r), 2020 N (u_G = k₀·i, i(t) = I_m·cos(…) : I_m, T₀, φ), 2023 R
#    (u_g = k·i) : notation u_G = k·i du cadre et du cours (la consigne R₀ = R + r s'écrit ici k = R + r).
#  - séries en ligne : recherche faite (talamidi, moutamadris, Naceiri, dreamjob) mais PDF non joignables depuis cette session ;
#    nos données sont celles de entretien.html (C = 4 µF, L = 0,1 H, R = r = 10 Ω, U_m = 6 V, T₀ ≈ 4 ms, k = 20 Ω).
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch8_rlc_5"
SIMD = "/media/simulations/physics/circuit-rlc-tableau/"


def grille(tmax, dt, ymin, ymax, dy):
    els, k = [], 0
    while k * dt <= tmax + 1e-9:
        els.append({"f": "ligne", "pts": [[round(k * dt, 4), ymin], [round(k * dt, 4), ymax]], "couleur": "faible"}); k += 1
    k = 0
    while ymin + k * dy <= ymax + 1e-9:
        y = round(ymin + k * dy, 4); els.append({"f": "ligne", "pts": [[0, y], [tmax, y]], "couleur": "faible"}); k += 1
    return els


def entretenue(titre, Um, T0ms, tmax, umax, dt):
    els = grille(tmax, dt, -umax, umax, 2) + [{"f": "courbe", "expr": f"{Um}*cos(2*pi*x/{T0ms})", "de": 0, "a": tmax, "couleur": "rouge"}]
    return figure_courbe(titre, axe("t", 0, tmax, "ms", list(range(0, tmax + 1, dt))),
                         axe("u_C", -umax, umax, "V", list(range(-umax, umax + 1, 2))), els,
                         legende="Avec G réglé convenablement, à partir de t = 0.")


def montage(titre):
    """Circuit RLC série (K en 2) avec le générateur G en série ; i orienté vers l'armature A."""
    g = [dipole([0.8, 0.8], [0.8, 3.6], "G", "E", pos="o"),
         fil([0.8, 3.6], [2.9, 3.6]),
         inverseur([3.4, 2.8], [2.9, 3.6], [3.9, 3.6], vers=2, t="K", pos_t=[3.95, 2.75]),
         dipole([3.4, 2.8], [3.4, 0.8], "C", "C", pos="e"),
         borne([3.4, 2.05], "A", "o"), borne([3.4, 0.8], "B", "s"),
         tension([2.1, 1.2], [2.1, 2.4], "u_C", pos="o"),
         fil([3.9, 3.6], [4.6, 3.6]),
         dipole([4.6, 3.6], [6.6, 3.6], "R", "R"),
         fil([6.6, 3.6], [7.6, 3.6]),
         dipole([7.6, 3.6], [7.6, 0.8], "L", "(L, r)", pos="e"),
         fil([7.6, 0.8], [6.8, 0.8]),
         dipole([6.8, 0.8], [4.8, 0.8], "R", "G", pos="n"),
         texte([5.8, 0.15], "u_G = k·i"),
         fil([4.8, 0.8], [0.8, 0.8]),
         courant([4.1, 0.8], "d")]
    return schema(titre, 9.6, 4.6, *g)


# ---------------------------------------------------------------- données et calculs (π² = 10)
C, L, R, r, UM = 4e-6, 0.1, 10, 10, 6
K = R + r
T0 = math.sqrt(40 * L * C)                       # 4 ms
W = 2 * math.pi / T0                             # 500π rad/s
IM = UM * math.sqrt(C / L)                       # ≈ 3,8·10⁻² A
assert K == 20 and abs(T0 - 4e-3) < 1e-12 and abs(W - 500 * math.pi) < 1e-9 and abs(IM * 1000 - 37.95) < 0.01
FIG = entretenue("Figure 2 : u_C(t), oscillations entretenues", UM, 4, 12, 8, 1)
# semblable : C = 2,5 µF, L = 0,25 H, R = 15 Ω, r = 8 Ω, U_m = 8 V
Cb, Lb, Rb, rb, UMb = 2.5e-6, 0.25, 15, 8, 8
T0b = math.sqrt(40 * Lb * Cb); IMb = UMb * math.sqrt(Cb / Lb)
assert abs(T0b - 5e-3) < 1e-12 and abs(IMb * 1000 - 25.3) < 0.01
FIGB = entretenue("Figure 2 : u_C(t), oscillations entretenues", UMb, 5, 15, 10, 1)

EQ = ("Additivité avec G : u_C + u_R + u_b = u_G, soit q/C + R·i + L·di/dt + r·i = k·i, avec i = dq/dt. "
      "D'où L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0.")
EXPR = "U_m = 6 V et T₀ = 4 ms ; u_C(0) = U_m donc cos φ = 1, φ = 0 ; 2π/T₀ = 2π/(4·10⁻³) = 500π rad/s : u_C(t) = 6·cos(500π·t) (t en s, u_C en V)."
ROLE = ("G fournit au circuit, à chaque instant, l'énergie que R et r dissipent par effet Joule (k·i² = (R + r)·i²) : "
        "l'énergie totale reste constante, l'amplitude ne diminue plus, et le circuit oscille à sa période propre T₀ = 2π√(LC).")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "circuit_RLC", "cours": "phys_ch8_circuit_RLC",
  "titre": "Entretenir les oscillations d'un circuit RLC", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir l'équation différentielle avec le générateur G (u_G = k·i)", "Montrer que k = R + r",
                  "Écrire l'expression numérique de u_C(t)", "Calculer I_m par la conservation de l'énergie", "Expliquer le rôle énergétique de G"],
  "enonce": {
    "intro": "Le circuit RLC série de la figure 1 (condensateur C chargé, conducteur ohmique R, bobine (L, r)) donne des oscillations amorties. Pour les entretenir, on monte en série un générateur G qui délivre une tension proportionnelle à l'intensité : u_G = k·i (k est une constante positive réglable). Pour une valeur convenable de k, on obtient la courbe u_C(t) de la figure 2.",
    "intro_dit": "دابا نقراو l'énoncé. le circuit RLC série ديال la figure un، فيه le condensateur C مشارجي، le conducteur ohmique R، وla bobine L r، كيعطي des oscillations amorties. باش نخليوهم ديما، كنزيدو en série un générateur G، كيعطي une tension proportionnelle à l'intensité: u G égale k i، وk constante موجبة كنقدرو نبدلوها. ملي k مزيانة، كنلقاو la courbe u C ديال la figure deux.",
    "figures": [montage("Figure 1 : le circuit RLC avec le générateur G"), FIG],
    "donnees": ["C = 4 µF", "L = 0,1 H", "R = 10 Ω ; r = 10 Ω", "π² = 10"],
    "questions": [
      question("1", "Établir l'équation différentielle vérifiée par la charge q(t) en présence du générateur G.",
        "السؤال un: بين l'équation différentielle اللي كتحققها la charge q، مع le générateur G.",
        phrase(EQ),
        ["u_C + u_R + u_b = u_G", "u_G = k·i", "i = dq/dt", "(R + r − k)"], ["u_C + u_R + u_b = 0", "(R + r + k)", "(r − k)"],
        [aide("Cette fois la maille contient un générateur : la somme u_C + u_R + u_b n'est plus nulle. À quoi est-elle égale ?",
              "هاد المرة كاين générateur فla maille: la somme u C plus u R plus u b ما بقاتش zéro. شحال كتساوي؟"),
         aide("u_C + u_R + u_b = u_G = k·i. Remplace chaque tension (q/C, R·i, L·di/dt + r·i), puis passe k·i de l'autre côté et regroupe les termes en dq/dt.",
              "u C plus u R plus u b égale u G، égale k i. عوض كل tension: q sur C، R i، L dé i sur dé t plus r i. من بعد دوز k i للجيهة الأخرى، وجمع les termes ديال dé q sur dé t.")],
        corr([("1 : additivité : u_C + u_R + u_b = u_G = k·i", "u C plus u R plus u b égale u G"),
              ("q/C + R·i + L·di/dt + r·i − k·i = 0, avec i = dq/dt", "moins k i égale zéro"),
              ("L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0", "L dé deux q sur dé t deux، plus R plus r moins k fois dé q sur dé t")],
             "السؤال un. مع G: u C plus u R plus u b égale u G، égale k i. كنعوضو: q sur C، plus R i، plus L dé i sur dé t، plus r i، moins k i égale zéro. وi égale dé q sur dé t. إذن L dé deux q sur dé t deux، plus R plus r moins k fois dé q sur dé t، plus q sur C، égale zéro."),
        "ex_lc5_1", "fa_lc5_1"),
      question("2", "Déterminer la valeur de k pour laquelle les oscillations sont sinusoïdales (figure 2).",
        "السؤال deux: حدد la valeur ديال k اللي كتخلي les oscillations sinusoïdales، بحال la figure deux.",
        valeur("k", 20, "Ω", "Oscillations sinusoïdales : R + r − k = 0, donc k = R + r = 10 + 10 = 20 Ω"),
        ["R + r − k = 0", "k = R + r", "Ω"], ["k = r = 10 Ω", "k = R = 10 Ω", "k = 0"],
        [aide("Compare avec l'équation du circuit LC idéal, dont la solution est sinusoïdale : quel terme doit disparaître ?",
              "قارن مع l'équation ديال le circuit LC idéal، اللي la solution ديالو sinusoïdale: أشمن terme خاصو يتحيد؟"),
         aide("Le terme en dq/dt doit être nul : R + r − k = 0. Attention : k compense toute la résistance, R et r.",
              "le terme ديال dé q sur dé t خاصو يكون zéro: R plus r moins k égale zéro. رد البال: k كتعوض la résistance كاملة، R وr.")],
        corr([("2 : sinusoïdales ⇒ terme d'amortissement nul : R + r − k = 0", "R plus r moins k égale zéro"),
              ("k = R + r = 10 + 10", "k égale R plus r"),
              ("k = 20 Ω (u_G en V, i en A)", "k égale vingt ohms")],
             "السؤال deux. باش تكون sinusoïdale، خاص le terme ديال l'amortissement يتحيد: R plus r moins k égale zéro. إذن k égale R plus r، يعني dix plus dix. k égale vingt ohms."),
        "ex_lc5_2", "fa_lc5_2"),
      question("3", "Relever U_m et T₀ sur la figure 2, puis écrire l'expression numérique de u_C(t) = U_m·cos(2πt/T₀ + φ).",
        "السؤال trois: اقرا U m وT zéro فla figure deux، ومن بعد كتب l'expression numérique ديال u C égale U m cosinus de deux pi t sur T zéro، plus phi.",
        phrase(EXPR),
        ["U_m", "T₀", "u_C(0) = U_m·cos φ", "2π/T₀", "500π"], ["φ = π/2", "u_C(t) = 6·cos(4t)", "U_m = 12 V"],
        [aide("U_m est la hauteur d'un sommet ; T₀ est la durée entre deux sommets successifs. Que vaut u_C à t = 0 ?",
              "U m هي العلو ديال sommet. T zéro هي المدة بين deux sommets متتابعين. شحال u C فt égale zéro؟"),
         aide("u_C(0) = U_m·cos φ = U_m donne cos φ = 1, donc φ = 0. Puis calcule 2π/T₀ avec T₀ en secondes.",
              "u C de zéro égale U m cosinus phi، égale U m: إذن cosinus phi égale un، وphi égale zéro. من بعد حسب deux pi sur T zéro، وT zéro بla seconde.")],
        corr([("3 : U_m = 6 V ; T₀ = 4 ms = 4·10⁻³ s", "U m égale six volts"),
              ("u_C(0) = U_m ⇒ cos φ = 1 ⇒ φ = 0", "phi égale zéro"),
              ("2π/T₀ = 500π rad/s : u_C(t) = 6·cos(500π·t)", "u C égale six cosinus de cinq cents pi t")],
             "السؤال trois. U m égale six volts، وT zéro égale quatre millisecondes. فt égale zéro، u C égale U m، إذن cosinus phi égale un، وphi égale zéro. deux pi sur quatre fois dix puissance moins trois، كتعطي cinq cents pi radians par seconde. إذن u C égale six cosinus de cinq cents pi t."),
        "ex_lc5_3", "fa_lc5_3"),
      question("4", "L'énergie totale se conserve. Calculer l'intensité maximale I_m du courant (en mA).",
        "السؤال quatre: l'énergie totale ثابتة. حسب l'intensité maximale I m ديال le courant، بles milliampères.",
        valeur("I_m", 38, "mA", "½·C·U_m² = ½·L·I_m² ⇒ I_m = U_m·√(C/L) = 6 × √(4·10⁻⁶/0,1) ≈ 3,8·10⁻² A = 38 mA"),
        ["½·C·U_m² = ½·L·I_m²", "I_m = U_m·√(C/L)", "√", "mA"], ["I_m = U_m·C/L", "I_m² = 1,44·10⁻³ A", "I_m = U_m/R"],
        [aide("Quand u_C = ±U_m, i = 0 : toute l'énergie est dans le condensateur. Quand u_C = 0, |i| = I_m : toute l'énergie est dans la bobine.",
              "ملي u C égale U m، i égale zéro: l'énergie كلها فle condensateur. وملي u C égale zéro، i égale I m: l'énergie كلها فla bobine."),
         aide("Écris ½·C·U_m² = ½·L·I_m², puis isole I_m : I_m = U_m·√(C/L).",
              "كتب un demi C U m au carré، égale un demi L I m au carré. ومن بعد عزل I m: I m égale U m racine de C sur L.")],
        corr([("4 : énergie constante : ½·C·U_m² = ½·L·I_m²", "un demi C U m au carré égale un demi L I m au carré"),
              ("I_m = U_m·√(C/L) = 6 × √(4·10⁻⁵)", "I m égale U m racine de C sur L"),
              ("I_m ≈ 3,8·10⁻² A = 38 mA", "I m environ trente-huit milliampères")],
             "السؤال quatre. l'énergie ثابتة: un demi C U m au carré égale un demi L I m au carré. إذن I m égale U m racine de C sur L، يعني six fois racine de quatre fois dix puissance moins cinq. I m environ trente-huit milliampères."),
        "ex_lc5_4", "fa_lc5_4"),
      question("5", "Expliquer le rôle énergétique du générateur G. Les oscillations entretenues ont-elles la période T₀ ? Justifier.",
        "السؤال cinq: شرح الدور ديال le générateur G من جهة l'énergie. واش les oscillations entretenues عندهم la période T zéro؟ علل.",
        phrase(ROLE),
        ["effet Joule", "énergie totale constante", "T₀ = 2π√(LC)"], ["G impose sa propre période", "G supprime la résistance"],
        [aide("Sans G, où partait l'énergie perdue ? Avec k = R + r, l'énergie totale change-t-elle encore ?",
              "بلا G، فين كانت كتمشي l'énergie اللي كتضيع؟ ومع k égale R plus r، واش l'énergie totale مازال كتبدل؟"),
         aide("Avec k = R + r, l'équation devient celle du circuit LC : d²q/dt² + q/(LC) = 0. Quelle est alors la période ?",
              "مع k égale R plus r، l'équation كتولي ديال le circuit LC: dé deux q sur dé t deux، plus q sur L C، égale zéro. شنو هي la période؟")],
        corr([("5 : G fournit à chaque instant l'énergie dissipée par effet Joule dans R et r : l'énergie totale reste constante.", "كيرجع l'énergie اللي ضاعت بl'effet Joule"),
              ("Avec k = R + r, l'équation est celle du circuit LC : les oscillations ont la période propre T₀ = 2π√(LC) = 4 ms.", "la période propre T zéro")],
             "السؤال cinq. le générateur G، فكل لحظة، كيرجع l'énergie اللي ضاعت بl'effet Joule فR وفr. إذن l'énergie totale كتبقى ثابتة وl'amplitude ما كتنقصش. ومع k égale R plus r، l'équation هي ديال le circuit LC، إذن la période هي la période propre T zéro، égale quatre millisecondes."),
        "ex_lc5_5", "fa_lc5_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_lc5_1", "Question 1 : l'équation avec G", "u_C + u_R + u_b = k·i ⇒ L·q'' + (R + r − k)·q' + q/C = 0.",
      SIMD + "entretien.html", "Sans G, les sommets baissent ; on ajoute G (u_G = k·i), puis l'équation",
      "شوف l'écran: بلا G، les sommets كيهبطو، six، quatre، deux virgule sept volts. دابا كنزيدو en série le générateur G: u G égale k i. la loi d'additivité ولات: u C plus u R plus u b égale u G، égale k i. كنعوضو بحال ديما، وكنجيبو k i للجيهة الأخرى. كنلقاو: L dé deux q sur dé t deux، plus R plus r moins k fois dé q sur dé t، plus q sur C، égale zéro.",
      centre=[("u_C + u_R + u_b = u_G = k·i", "u C plus u R plus u b égale u G"),
              ("L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0", "كنلقاو: L dé deux q sur dé t deux")],
      pointage=[{"mot": "شوف l'écran", "commande": "play_until", "parametres": {"moment": "amorti"}},
                {"mot": "les sommets كيهبطو", "repere": "courbe"},
                {"mot": "دابا كنزيدو en série le générateur G", "commande": "play_until", "parametres": {"moment": "dispositif"}},
                {"mot": "u G égale k i", "repere": "formule_uG"},
                {"mot": "u C plus u R plus u b égale u G", "commande": "play_until", "parametres": {"moment": "equation"}},
                {"mot": "u C plus u R plus u b égale u G", "cible": "centre:0"},
                {"mot": "كنلقاو: L dé deux q sur dé t deux", "repere": "equation"},
                {"mot": "كنلقاو: L dé deux q sur dé t deux", "cible": "centre:1"}]),
    diapo_sim("ex_lc5_2", "Question 2 : k = R + r", "Terme du milieu nul : k = R + r = 20 Ω.",
      SIMD + "entretien.html", "Le terme (R + r − k)·dq/dt, puis k réglé sur R + r = 20 Ω",
      "شوف le terme ديال الوسط: R plus r moins k، fois dé q sur dé t. هو اللي كيخوي l'énergie. باش يتحيد، خاص R plus r moins k égale zéro. إذن k égale R plus r، la résistance totale، ماشي غير r. هنا R égale dix ohms وr égale dix ohms، إذن k égale vingt ohms. شوف دابا: مع k égale vingt ohms، les sommets كلهم six volts.",
      centre=[("R + r − k = 0", "خاص R plus r moins k égale zéro"),
              ("k = R + r = 10 + 10 = 20 Ω", "إذن k égale vingt ohms")],
      pointage=[{"mot": "شوف le terme ديال الوسط", "commande": "play_until", "parametres": {"moment": "equation"}},
                {"mot": "شوف le terme ديال الوسط", "repere": "terme_milieu"},
                {"mot": "خاص R plus r moins k égale zéro", "cible": "centre:0"},
                {"mot": "إذن k égale R plus r", "commande": "play_until", "parametres": {"moment": "compensation"}},
                {"mot": "إذن k égale vingt ohms", "cible": "centre:1"},
                {"mot": "شوف دابا", "commande": "play_until", "parametres": {"moment": "entretenu"}},
                {"mot": "les sommets كلهم six volts", "repere": "sommets"}]),
    diapo_sim("ex_lc5_3", "Question 3 : l'expression de u_C(t)", "U_m = 6 V, T₀ = 4 ms, φ = 0 : u_C = 6·cos(500π·t).",
      SIMD + "solution.html?vue=cos", "La sinusoïde : U_m = 6 V et T₀ ≈ 4 ms ; départ au sommet",
      "شوف la sinusoïde. U m هي العلو ديال sommet: six volts. T zéro هي المدة بين deux sommets: quatre millisecondes. فt égale zéro، la courbe كتبدا من le sommet: u C de zéro égale U m، إذن cosinus phi égale un، وphi égale zéro. deux pi sur T zéro: deux pi sur quatre fois dix puissance moins trois، يعني cinq cents pi radians par seconde. إذن u C égale six cosinus de cinq cents pi t.",
      centre=[("U_m = 6 V ; T₀ = 4 ms", "six volts"),
              ("u_C(0) = U_m ⇒ φ = 0", "وphi égale zéro"),
              ("u_C(t) = 6·cos(500π·t)", "إذن u C égale six cosinus de cinq cents pi t")],
      pointage=[{"mot": "شوف la sinusoïde", "commande": "play_until", "parametres": {"moment": "Um"}},
                {"mot": "U m هي العلو ديال sommet", "repere": "Um"},
                {"mot": "six volts", "cible": "centre:0"},
                {"mot": "T zéro هي المدة بين deux sommets", "commande": "play_until", "parametres": {"moment": "T0"}},
                {"mot": "T zéro هي المدة بين deux sommets", "repere": "T0"},
                {"mot": "وphi égale zéro", "cible": "centre:1"},
                {"mot": "إذن u C égale six cosinus de cinq cents pi t", "cible": "centre:2"}]),
    diapo_sim("ex_lc5_4", "Question 4 : I_m par l'énergie", "½·C·U_m² = ½·L·I_m² ⇒ I_m = U_m·√(C/L) ≈ 38 mA.",
      SIMD + "energie.html?vue=echange", "Toute l'énergie passe du condensateur (u_C = U_m) à la bobine (i = I_m)",
      "شوف les deux barres. فالبداية، u C égale six volts وi égale zéro: كلشي فle condensateur، soixante-douze microjoules. دابا u C كتوصل à zéro: la barre الحمرا خاوية، وكلشي فla bobine، وi فأكبر قيمة ديالها، I m. l'énergie ثابتة، إذن un demi C U m au carré égale un demi L I m au carré. إذن I m égale U m racine de C sur L. يعني six fois racine de quatre fois dix puissance moins cinq: environ trente-huit milliampères.",
      centre=[("½·C·U_m² = ½·L·I_m²", "إذن un demi C U m au carré égale un demi L I m au carré"),
              ("I_m = U_m·√(C/L) = 6 × √(4·10⁻⁵) ≈ 38 mA", "environ trente-huit milliampères")],
      pointage=[{"mot": "شوف les deux barres", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "كلشي فle condensateur", "repere": "barre_Ee"},
                {"mot": "دابا u C كتوصل", "commande": "play_until", "parametres": {"moment": "tout_bobine"}},
                {"mot": "وكلشي فla bobine", "repere": "barre_Em"},
                {"mot": "إذن un demi C U m au carré égale un demi L I m au carré", "cible": "centre:0"},
                {"mot": "environ trente-huit milliampères", "cible": "centre:1"}]),
    diapo_sim("ex_lc5_5", "Question 5 : le rôle de G", "G rend l'énergie perdue par effet Joule ; la période reste T₀.",
      SIMD + "entretien.html", "Avec k = R + r : amplitude constante, période T₀ ≈ 4 ms",
      "مع k égale R plus r، شوف les sommets: كلهم بنفس العلو. علاش؟ le générateur G، فكل لحظة، كيرجع l'énergie اللي ضاعت بl'effet Joule فR وفr. إذن l'énergie totale ثابتة. وla période؟ l'équation ولات هي ديال le circuit LC، إذن la période هي T zéro égale deux pi racine de L C، environ quatre millisecondes. G كيعوض l'énergie، ولكن ما كيفرضش la période ديالو.",
      centre=[("G compense l'énergie dissipée par effet Joule", "كيرجع l'énergie اللي ضاعت بl'effet Joule"),
              ("Période : T₀ = 2π√(LC) ≈ 4 ms", "environ quatre millisecondes")],
      pointage=[{"mot": "مع k égale R plus r", "commande": "play_until", "parametres": {"moment": "entretenu"}},
                {"mot": "كلهم بنفس العلو", "repere": "sommets"},
                {"mot": "كيرجع l'énergie اللي ضاعت بl'effet Joule", "cible": "centre:0"},
                {"mot": "وla période؟", "commande": "play_until", "parametres": {"moment": "periode_T0"}},
                {"mot": "environ quatre millisecondes", "repere": "T0"},
                {"mot": "environ quatre millisecondes", "cible": "centre:1"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_lc5_1", "Plus facile : l'équation avec G", "نتمرنو: اختار l'équation مع le générateur G.",
      "Avec G (u_G = k·i) en série, l'équation en q devient :",
      ["L·q'' + (R + r + k)·q' + q/C = 0", "L·q'' + (R + r − k)·q' + q/C = 0", "L·q'' + (r − k)·q' + q/C = 0"], 1, {
        "1": {"juste": rep("برافو! k i جات من الجيهة الأخرى، إذن كتنقص من R plus r.", "Juste : L·q'' + (R + r − k)·q' + q/C = 0.")},
        "0": {"1": rep("ملي كتدوز k i من u G للجيهة الأخرى، كيتبدل le signe ديالها. عاود اختار.", "En passant k·i de l'autre côté, son signe change. Réessaie."),
              "2": rep("الجواب: R plus r moins k. u G كتعطي l'énergie، ما كتزيدش l'amortissement.", "Réponse : (R + r − k) ; G compense, il n'amortit pas.")},
        "2": {"1": rep("فين مشات R؟ le résistor حتى هو فla maille. عاود اختار.", "Et R ? Le résistor est aussi dans la maille. Réessaie."),
              "2": rep("الجواب: R plus r moins k، la résistance totale.", "Réponse : (R + r − k), avec la résistance totale.")}},
      "Avec G en série, l'équation en q devient ?"),
    qcm_facile("fa_lc5_2", "Plus facile : la bonne valeur de k", "سؤال ساهل: شحال خاص k؟",
      "R = 10 Ω et r = 10 Ω. Pour des oscillations sinusoïdales, k vaut…",
      ["10 Ω", "0 Ω", "20 Ω"], 2, {
        "2": {"juste": rep("برافو! k égale R plus r، vingt ohms.", "Juste : k = R + r = 20 Ω.")},
        "0": {"1": rep("dix ohms كتعوض غير وحدة من les deux résistances. شحال هي la résistance totale؟ عاود اختار.", "10 Ω ne compense qu'une des deux résistances. Réessaie."),
              "2": rep("الجواب: vingt ohms. k خاصها تعوض R وr بجوج.", "Réponse : 20 Ω ; k compense R et r.")},
        "1": {"1": rep("k égale zéro يعني بلا G: les sommets كيبقاو يهبطو. عاود اختار.", "k = 0, c'est sans G : les oscillations restent amorties. Réessaie."),
              "2": rep("الجواب: k égale R plus r، vingt ohms.", "Réponse : k = R + r = 20 Ω.")}},
      "R égale dix ohms et r égale dix ohms. Pour des oscillations sinusoïdales, k vaut ?"),
    qcm_facile("fa_lc5_3", "Plus facile : l'expression de u_C", "سؤال ساهل: اختار l'expression ديال u C.",
      "U_m = 6 V, T₀ = 4 ms, départ au sommet. u_C(t) = …",
      ["6·cos(500π·t)", "12·cos(500π·t)", "6·cos(4·t)"], 0, {
        "0": {"juste": rep("برافو! U m égale six، et deux pi sur T zéro égale cinq cents pi.", "Juste : u_C = 6·cos(500π·t).")},
        "1": {"1": rep("douze volts هي المسافة بين le sommet وle creux، يعني deux U m. عاود اختار.", "12 V est l'écart sommet–creux, 2·U_m. Réessaie."),
              "2": rep("الجواب: six cosinus de cinq cents pi t. U m هي العلو ديال sommet.", "Réponse : 6·cos(500π·t) ; U_m est la hauteur d'un sommet.")},
        "2": {"1": rep("داخل le cosinus خاص deux pi sur T zéro، وT zéro بla seconde. عاود اختار.", "Dans le cosinus, il faut 2π/T₀ avec T₀ en secondes. Réessaie."),
              "2": rep("الجواب: deux pi sur quatre fois dix puissance moins trois، يعني cinq cents pi.", "Réponse : 2π/(4·10⁻³) = 500π rad/s.")}},
      "U m égale six volts, T zéro égale quatre millisecondes. u C égale ?"),
    qcm_facile("fa_lc5_4", "Plus facile : l'intensité maximale", "سؤال ساهل على I m.",
      "U_m = 6 V, C = 4 µF, L = 0,1 H. I_m = U_m·√(C/L) vaut…",
      ["0,24 mA", "38 mA", "1,44 mA"], 1, {
        "1": {"juste": rep("برافو! six fois racine de quatre fois dix puissance moins cinq، environ trente-huit milliampères.", "Juste : I_m ≈ 38 mA.")},
        "0": {"1": rep("نسيتي la racine: C sur L خاصها racine. عاود اختار.", "Tu as oublié la racine de C/L. Réessaie."),
              "2": rep("الجواب: trente-huit milliampères. I m égale U m fois racine de C sur L.", "Réponse : 38 mA, avec √(C/L).")},
        "2": {"1": rep("هادي I m au carré، ماشي I m. خود la racine. عاود اختار.", "C'est I_m² (en A²), pas I_m : prends la racine. Réessaie."),
              "2": rep("الجواب: racine de un virgule quarante-quatre fois dix puissance moins trois، environ trente-huit milliampères.", "Réponse : I_m = √(1,44·10⁻³) ≈ 3,8·10⁻² A = 38 mA.")}},
      "U m égale six volts, C égale quatre microfarads, L égale zéro virgule un henry. I m vaut ?"),
    vrai_faux_facile("fa_lc5_5", "Plus facile : vrai ou faux", "سؤال ساهل على le rôle ديال G.",
      "Oscillations entretenues avec k = R + r.",
      [("G fournit l'énergie perdue par effet Joule dans R et r.", True, "C'est le rôle de G : l'énergie totale reste constante."),
       ("G impose sa propre période au circuit.", False, "Le circuit oscille à sa période propre T₀ = 2π√(LC) ; G ne fait que compenser les pertes."),
       ("Avec k = R + r, l'amplitude de u_C reste constante.", True, "Le terme d'amortissement est nul : les sommets restent à la même hauteur.")]),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même dispositif (figure 1) avec C = 2,5 µF, L = 0,25 H, R = 15 Ω et r = 8 Ω. Pour une valeur convenable de k, on obtient la courbe u_C(t) de la figure 2.",
      "intro_dit": "نفس التمرين، بقيم أخرى. C égale deux virgule cinq microfarads، L égale zéro virgule vingt-cinq henry، R égale quinze ohms، وr égale huit ohms.",
      "figures": [FIGB],
      "donnees": ["C = 2,5 µF", "L = 0,25 H", "R = 15 Ω ; r = 8 Ω", "π² = 10"],
      "questions": [
        question_semblable("1", "Établir l'équation différentielle vérifiée par q(t) en présence de G.",
          phrase(EQ), ["u_C + u_R + u_b = k·i"], ["u_C + u_R + u_b = 0"],
          corr([("1 : L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0", "R plus r moins k")],
               "u C plus u R plus u b égale k i، إذن L dé deux q sur dé t deux، plus R plus r moins k fois dé q sur dé t، plus q sur C، égale zéro.")),
        question_semblable("2", "Déterminer k pour des oscillations sinusoïdales.",
          valeur("k", 23, "Ω", "k = R + r = 15 + 8 = 23 Ω"), ["k = R + r", "Ω"], ["k = r = 8 Ω"],
          corr([("2 : R + r − k = 0 ⇒ k = R + r = 23 Ω", "k égale vingt-trois ohms")],
               "R plus r moins k égale zéro، إذن k égale quinze plus huit، k égale vingt-trois ohms.")),
        question_semblable("3", "Relever U_m et T₀, puis écrire l'expression numérique de u_C(t).",
          phrase("U_m = 8 V, T₀ = 5 ms, u_C(0) = U_m donc φ = 0 ; 2π/T₀ = 400π rad/s : u_C(t) = 8·cos(400π·t)."), ["2π/T₀", "400π"], ["φ = π/2"],
          corr([("3 : U_m = 8 V ; T₀ = 5 ms ; φ = 0", "U m égale huit volts"), ("u_C(t) = 8·cos(400π·t)", "huit cosinus de quatre cents pi t")],
               "U m égale huit volts، T zéro égale cinq millisecondes، وphi égale zéro. إذن u C égale huit cosinus de quatre cents pi t.")),
        question_semblable("4", "Calculer l'intensité maximale I_m (en mA).",
          valeur("I_m", 25.3, "mA", "I_m = U_m·√(C/L) = 8 × √(2,5·10⁻⁶/0,25) = 8 × √(10⁻⁵) ≈ 2,53·10⁻² A = 25,3 mA"), ["I_m = U_m·√(C/L)", "mA"], ["I_m = U_m·C/L"],
          corr([("4 : I_m = U_m·√(C/L) = 8 × √(10⁻⁵)", "I m égale U m racine de C sur L"), ("I_m ≈ 25,3 mA", "vingt-cinq virgule trois milliampères")],
               "I m égale U m racine de C sur L، يعني huit fois racine de dix puissance moins cinq. I m environ vingt-cinq virgule trois milliampères.")),
        question_semblable("5", "Expliquer le rôle énergétique de G et la période des oscillations.",
          phrase(ROLE.replace("T₀ = 2π√(LC)", "T₀ = 2π√(LC) = 5 ms")), ["effet Joule", "T₀"], ["G impose sa période"],
          corr([("5 : G compense l'énergie dissipée par effet Joule ; période propre T₀ = 5 ms.", "la période propre")],
               "G كيرجع l'énergie اللي ضاعت بl'effet Joule، وles oscillations عندهم la période propre، cinq millisecondes.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
