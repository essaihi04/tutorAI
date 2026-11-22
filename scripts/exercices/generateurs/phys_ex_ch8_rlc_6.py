# Exercice de physique, ch. 8 (oscillations libres d'un circuit RLC série), niveau difficile n° 6 :
# exploiter les courbes d'énergie E_e(t) et E_m(t) d'un circuit RLC : identifier, U₀, la durée T/2 entre deux maximums de
# E_e (piège : ce n'est pas T), L, l'énergie dissipée, puis |i| quand u_C = 0 (lecture critique : E_m < E₀).
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture backend/data/curriculum/architecture/phys_ch8_circuit_RLC.md
#    (énergie : 14 sessions ; lc_en3 « E_e atteint son maximum deux fois par période »), fiche du cadre circuit_RLC (RLC6,
#    RLC7 : identifier les courbes E_e, E_m, E), docs/parties_voix/phys_ch8_circuit_RLC.json.
#  - cours phys_ch8_circuit_RLC : lc_en2_depart, lc_en3_echange (I_m = √(2E/L)), lc_a4_perdue, lc_a5_courbes.
#  - nationaux : 2020 R (courbes C₃, C₄ de E_e et E_m), 2021 R (courbes de la figure 6, énergie dissipée entre t₀ et t₁),
#    2019 R (E_t à t₁ avec les deux courbes), 2024 N (« dans quel dipôle est emmagasinée l'énergie à t₁ puis à t₂ ») ;
#    ici plus de pas, document moins guidé (les courbes ne sont pas nommées) : niveau supérieur, dans le cadre.
#  - séries en ligne : recherche faite (talamidi, moutamadris, Naceiri, dreamjob) mais PDF non joignables depuis cette session ;
#    nos données sont celles de energie.html (C = 4 µF, E = 6 V, L = 0,1 H, R + r = 20 Ω) ; courbes calculées par la
#    solution exacte de l'équation (même calcul que la simulation).
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch8_rlc_6"
SIMD = "/media/simulations/physics/circuit-rlc-tableau/"


def grille(tmax, dt, ymax, dy):
    els, k = [], 0
    while k * dt <= tmax + 1e-9:
        els.append({"f": "ligne", "pts": [[round(k * dt, 4), 0], [round(k * dt, 4), ymax]], "couleur": "faible"}); k += 1
    k = 0
    while k * dy <= ymax + 1e-9:
        els.append({"f": "ligne", "pts": [[0, k * dy], [tmax, k * dy]], "couleur": "faible"}); k += 1
    return els


def physique(E, L, C, Rt):
    """Solution exacte : u_C(t), i(t) (t en s), et les expressions E_e(x), E_m(x) en µJ pour x en ms."""
    lam = Rt / (2 * L); w = math.sqrt(1 / (L * C) - lam ** 2)
    u = lambda t: E * math.exp(-lam * t) * (math.cos(w * t) + lam / w * math.sin(w * t))
    i = lambda t: -(E / (L * w)) * math.exp(-lam * t) * math.sin(w * t)
    a, b, c = lam / 1000, w / 1000, lam / w
    ke = 0.5 * C * E ** 2 * 1e6; km = 0.5 * L * (E / (L * w)) ** 2 * 1e6
    ee = f"{ke:.6g}*exp(-{2 * a:.6g}*x)*(cos({b:.6g}*x)+{c:.6g}*sin({b:.6g}*x))^2"
    em = f"{km:.6g}*exp(-{2 * a:.6g}*x)*sin({b:.6g}*x)^2"
    T = 2 * math.pi / w
    t1 = (math.pi - math.atan(w / lam)) / w            # premier zéro de u_C
    return u, i, ee, em, T, t1


def figure_energies(titre, E, L, C, Rt, tmax, ymax, dt, dy, lu2, lu1):
    u, i, ee, em, T, t1 = physique(E, L, C, Rt)
    Ee = lambda t: 0.5 * C * u(t) ** 2 * 1e6; Em = lambda t: 0.5 * L * i(t) ** 2 * 1e6
    els = grille(tmax, dt, ymax, dy) + [
        {"f": "courbe", "expr": ee, "de": 0, "a": tmax, "couleur": "orange", "texte": "(1)", "texte_x": round(T * 1000 * 0.5, 3)},
        {"f": "courbe", "expr": em, "de": 0, "a": tmax, "couleur": "vert", "texte": "(2)", "texte_x": round(T * 1000 * 0.75, 3)},
        {"f": "point", "at": [round(T * 1000, 3), round(Ee(T), 2)], "t": f"t₂ : {lu2}", "pos": "n", "couleur": "jaune"},
        {"f": "point", "at": [round(t1 * 1000, 3), round(Em(t1), 2)], "t": f"t₁ : {lu1}", "pos": "n", "couleur": "jaune"}]
    fig = figure_courbe(titre, axe("t", 0, tmax, "ms", list(range(0, tmax + 1, dt))),
                        axe("E", 0, ymax, "µJ", list(range(0, ymax + 1, dy))), els,
                        legende="t₁ : première annulation de la courbe (1) ; t₂ : troisième maximum de la courbe (1).")
    return fig, T, t1, Ee, Em


# ---------------------------------------------------------------- données et calculs (π² = 10)
C, L_VRAI, RT = 4e-6, 0.1, 20
FIG, T, T1, EE, EM = figure_energies("Figure 2 : les énergies (1) et (2) au cours du temps", 6, L_VRAI, C, RT, 10, 80, 1, 10, "32 µJ", "58 µJ")
EE0 = 72e-6
U0 = math.sqrt(2 * EE0 / C)                       # 6 V
T_LU = 2 * 2e-3                                   # deux maximums successifs de E_e : T/2 = 2 ms
L = T_LU ** 2 / (40 * C)                          # 0,1 H
EJ = EE0 - 32e-6                                  # 4·10⁻⁵ J
IM1 = math.sqrt(2 * 58e-6 / L)                    # |i(t₁)| ≈ 34 mA
assert abs(EE(0) - 72) < 1e-9 and abs(U0 - 6) < 1e-12 and abs(T / 2 * 1000 - 1.99) < 0.01
assert abs(L - 0.1) < 1e-12 and abs(EE(T) - 32.5) < 0.1 and abs(EJ - 4e-5) < 1e-15
assert abs(EM(T1) - 58.5) < 0.1 and abs(IM1 * 1000 - 34.06) < 0.02 and EE(T1) < 1e-9
# semblable : C = 10 µF, E = 4 V, L = 0,4 H, R + r = 40 Ω
FIGB, TB, T1B, EEB, EMB = figure_energies("Figure 2 : les énergies (1) et (2) au cours du temps", 4, 0.25, 10e-6, 20, 20, 90, 1, 10, "36 µJ", "65 µJ")
U0b = math.sqrt(2 * 80e-6 / 10e-6); Lb = (2 * 5e-3) ** 2 / (40 * 10e-6); EJb = 80e-6 - 36e-6; IMb = math.sqrt(2 * 65e-6 / Lb)
assert abs(EEB(0) - 80) < 1e-9 and abs(U0b - 4) < 1e-12 and abs(TB / 2 * 1000 - 5) < 0.05
assert abs(EEB(TB) - 36) < 0.2 and abs(EMB(T1B) - 65) < 0.2 and abs(Lb - 0.25) < 1e-12
assert abs(EJb - 4.4e-5) < 1e-15 and abs(IMb * 1000 - 22.8) < 0.01

IDENT = ("À t = 0, le condensateur est chargé et i(0) = 0 : E_e(0) = ½·C·u_C(0)² est maximale et E_m(0) = ½·L·i(0)² = 0. "
         "La courbe (1), qui part de 72 µJ, est E_e(t) ; la courbe (2), qui part de 0, est E_m(t).")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "circuit_RLC", "cours": "phys_ch8_circuit_RLC",
  "titre": "Lire les courbes d'énergie d'un circuit RLC", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Identifier les courbes E_e(t) et E_m(t)", "Relier la durée entre deux maximums de E_e à la pseudo-période",
                  "Calculer L avec T ≈ T₀", "Calculer l'énergie dissipée par effet Joule", "Calculer |i| à partir de E_m"],
  "enonce": {
    "intro": "Un condensateur de capacité C, chargé sous une tension U₀, est relié à t = 0 à une bobine (L, r) en série avec un conducteur ohmique R (circuit RLC série, R + r = 20 Ω). Un logiciel calcule, à partir des mesures, l'énergie électrique E_e(t) emmagasinée dans le condensateur et l'énergie magnétique E_m(t) emmagasinée dans la bobine : ce sont les courbes (1) et (2) de la figure 2, que l'on ne sait pas encore attribuer. On admet que la pseudo-période T est égale à la période propre T₀.",
    "intro_dit": "دابا نقراو l'énoncé. un condensateur، la capacité ديالو C، مشارجي تحت la tension U zéro، كنربطوه فt égale zéro مع la bobine L r ومع un conducteur ohmique R. la résistance totale R plus r égale vingt ohms. un logiciel كيحسب l'énergie électrique E e ديال le condensateur، وl'énergie magnétique E m ديال la bobine. هوما les courbes un et deux فla figure deux، ومازال ما عرفناش شكون هي شكون. وكنقبلو بلي la pseudo-période T égale la période propre T zéro.",
    "figures": [FIG],
    "donnees": ["C = 4 µF = 4·10⁻⁶ F", "R + r = 20 Ω", "π² = 10"],
    "questions": [
      question("1", "Identifier, en justifiant, la courbe qui représente E_e(t) et celle qui représente E_m(t).",
        "السؤال un: عرف، مع التعليل، أشمن courbe هي E e، وأشمن courbe هي E m.",
        phrase(IDENT),
        ["E_e = ½·C·u_C²", "E_m = ½·L·i²", "i(0) = 0", "u_C(0) = U₀"], ["E_m(0) maximale", "(1) = E_m"],
        [aide("Que vaut l'intensité i juste au début de la décharge, à t = 0 ? Et la tension u_C ?",
              "شحال i فالبداية ديال la décharge، فt égale zéro؟ وشحال la tension u C؟"),
         aide("i(0) = 0, donc E_m(0) = ½·L·i(0)² = 0 ; u_C(0) = U₀ ≠ 0, donc E_e(0) est maximale. Quelle courbe part de zéro ?",
              "i de zéro égale zéro، إذن E m de zéro égale zéro. وu C de zéro égale U zéro، إذن E e فالبداية فأكبر قيمة. أشمن courbe كتبدا من zéro؟")],
        corr([("1 : à t = 0, i(0) = 0 ⇒ E_m(0) = ½·L·i(0)² = 0", "E m de zéro égale zéro"),
              ("u_C(0) = U₀ ⇒ E_e(0) = ½·C·U₀² maximale", "E e فأكبر قيمة"),
              ("(1) : E_e(t) ; (2) : E_m(t)", "la courbe un هي E e")],
             "السؤال un. فt égale zéro، le courant مازال ما بداش: i de zéro égale zéro، إذن E m de zéro égale zéro. وle condensateur مشارجي: E e فأكبر قيمة. إذن la courbe un هي E e، وla courbe deux، اللي كتبدا من zéro، هي E m."),
        "ex_lc6_1", "fa_lc6_1"),
      question("2", "Déterminer la tension initiale U₀ = u_C(0) aux bornes du condensateur.",
        "السؤال deux: حدد la tension البدئية U zéro، يعني u C de zéro.",
        valeur("U₀", 6, "V", "E_e(0) = ½·C·U₀² = 72 µJ ⇒ U₀ = √(2E_e(0)/C) = √(2 × 72·10⁻⁶/4·10⁻⁶) = √36 = 6 V"),
        ["E_e = ½·C·u_C²", "U₀ = √(2E_e/C)", "µJ", "10⁻⁶", "V"], ["U₀ = 2E_e/C", "U₀ = 36 V", "E_e(0) = 72 J"],
        [aide("Lis E_e(0) sur la courbe (1) et convertis-la en joules (1 µJ = 10⁻⁶ J).",
              "اقرا E e de zéro فla courbe un، وحولها لle joule: un microjoule égale dix puissance moins six joule."),
         aide("E_e(0) = ½·C·U₀², donc U₀² = 2E_e(0)/C, puis prends la racine.",
              "E e de zéro égale un demi C U zéro au carré. إذن U zéro au carré égale deux E e sur C، ومن بعد خود la racine.")],
        corr([("2 : E_e(0) = 72 µJ = 7,2·10⁻⁵ J = ½·C·U₀²", "E e de zéro égale soixante-douze microjoules"),
              ("U₀ = √(2E_e(0)/C) = √(2 × 7,2·10⁻⁵/4·10⁻⁶) = √36", "U zéro égale racine de deux E e sur C"),
              ("U₀ = 6 V", "U zéro égale six volts")],
             "السؤال deux. كنقراو E e de zéro égale soixante-douze microjoules، وهي un demi C U zéro au carré. إذن U zéro égale racine de deux E e sur C، يعني racine de trente-six. U zéro égale six volts."),
        "ex_lc6_2", "fa_lc6_2"),
      question("3", "Montrer que la durée qui sépare deux maximums successifs de E_e(t) est égale à T/2. En déduire T, puis l'inductance L de la bobine.",
        "السؤال trois: بين بلي المدة بين deux maximums متتابعين ديال E e هي T sur deux. استنتج T، ومن بعد l'inductance L ديال la bobine.",
        valeur("L", 0.1, "H", "E_e = ½·C·u_C² est maximale quand |u_C| est maximale (sommet ET creux de u_C, i = 0), soit tous les T/2 ; lu : T/2 = 2 ms ⇒ T = 4 ms ; L = T²/(4π²·C) = (4·10⁻³)²/(40 × 4·10⁻⁶) = 0,1 H"),
        ["E_e ∝ u_C²", "sommet et creux", "T/2", "L = T₀²/(4π²C)", "H"], ["T = 2 ms", "L = 0,025 H", "T = durée entre deux maximums de E_e"],
        [aide("E_e dépend de u_C². Quand u_C est à un creux (valeur négative), u_C² est-il petit ou grand ? Combien de maximums de E_e par pseudo-période ?",
              "E e كتعتمد على u C au carré. ملي u C فle creux، يعني سالبة، واش u C au carré صغيرة ولا كبيرة؟ شحال من maximum ديال E e فكل pseudo-période؟"),
         aide("Deux maximums par pseudo-période (sommet et creux de u_C) : la durée lue entre deux maximums de (1) vaut T/2. Puis T² = 4π²·L·C.",
              "deux maximums فكل pseudo-période: le sommet وle creux ديال u C. إذن المدة اللي كتقرا بين deux maximums هي T sur deux. ومن بعد T au carré égale quatre pi carré L C.")],
        corr([("3 : E_e = ½·C·u_C² est maximale au sommet et au creux de u_C : deux maximums par pseudo-période, séparés de T/2", "deux maximums فكل pseudo-période"),
              ("Lecture : T/2 = 2 ms ⇒ T = 4 ms = 4·10⁻³ s", "T sur deux égale deux millisecondes"),
              ("T = T₀ = 2π√(LC) ⇒ L = T²/(4π²·C) = (4·10⁻³)²/(40 × 4·10⁻⁶)", "L égale T au carré، sur quatre pi carré fois C"),
              ("L = 0,1 H", "L égale zéro virgule un henry")],
             "السؤال trois. E e égale un demi C u C au carré: كتوصل لأكبر قيمة فle sommet وحتى فle creux ديال u C. إذن deux maximums فكل pseudo-période، وبيناتهم T sur deux. كنقراو T sur deux égale deux millisecondes، إذن T égale quatre millisecondes. ماشي deux. من بعد L égale T au carré، sur quatre pi carré fois C، يعني seize fois dix puissance moins six، sur quarante fois quatre fois dix puissance moins six. L égale zéro virgule un henry."),
        "ex_lc6_3", "fa_lc6_3"),
      question("4", "Justifier que l'énergie totale à la date t₂ est égale à E_e(t₂), puis calculer l'énergie E_J dissipée par effet Joule entre t = 0 et t₂.",
        "السؤال quatre: علل بلي l'énergie totale فt deux هي E e de t deux، ومن بعد حسب l'énergie E J اللي ضاعت بl'effet Joule بين t égale zéro وt deux.",
        valeur("E_J", 4e-5, "J", "À t₂, E_m(t₂) = 0 (i = 0), donc E(t₂) = E_e(t₂) = 32 µJ ; à t = 0, E = 72 µJ ; E_J = E(0) − E(t₂) = 72 − 32 = 40 µJ = 4·10⁻⁵ J"),
        ["E = E_e + E_m", "E_m(t₂) = 0", "E_J = E(0) − E(t₂)", "µJ", "J"], ["E_J = E(t₂)", "E_J = 72 µJ", "E_J = E(t₂) − E(0)"],
        [aide("Que vaut la courbe (2) à la date t₂ ? Écris l'énergie totale E = E_e + E_m à t = 0 et à t₂.",
              "شحال la courbe deux فt deux؟ كتب l'énergie totale E égale E e plus E m، فt égale zéro وفt deux."),
         aide("L'énergie dissipée est ce que le circuit a perdu : E_J = E(0) − E(t₂), avec E(0) = 72 µJ et E(t₂) = E_e(t₂).",
              "l'énergie اللي ضاعت هي اللي نقصات من الدارة: E J égale E de zéro moins E de t deux. E de zéro égale soixante-douze microjoules، وE de t deux هي E e de t deux.")],
        corr([("4 : à t₂, E_m(t₂) = 0 (i = 0) : E(t₂) = E_e(t₂) = 32 µJ", "E m de t deux égale zéro"),
              ("À t = 0 : E(0) = E_e(0) = 72 µJ", "E de zéro égale soixante-douze microjoules"),
              ("E_J = E(0) − E(t₂) = 72 − 32 = 40 µJ = 4·10⁻⁵ J (effet Joule dans R + r)", "E J égale quarante microjoules")],
             "السؤال quatre. فt deux، la courbe deux égale zéro، يعني i égale zéro: E m de t deux égale zéro، وE de t deux égale E e de t deux، trente-deux microjoules. فt égale zéro، E de zéro égale soixante-douze microjoules. إذن E J égale soixante-douze moins trente-deux، E J égale quarante microjoules، يعني quatre fois dix puissance moins cinq joule، مشات chaleur فR plus r."),
        "ex_lc6_4", "fa_lc6_4"),
      question("5", "À la date t₁, la courbe (1) s'annule. Calculer la valeur absolue |i(t₁)| de l'intensité (en mA). Pourquoi E_m(t₁) est-elle inférieure à 72 µJ ?",
        "السؤال cinq: فt un، la courbe un كتولي zéro. حسب la valeur absolue ديال i de t un، بles milliampères. وعلاش E m de t un صغر من soixante-douze microjoules؟",
        valeur("|i(t₁)|", 34, "mA", "À t₁, u_C = 0 : E(t₁) = E_m(t₁) = ½·L·i² = 58 µJ ⇒ |i(t₁)| = √(2E_m/L) = √(2 × 58·10⁻⁶/0,1) ≈ 3,4·10⁻² A = 34 mA (E_m < 72 µJ : une partie de l'énergie est déjà dissipée par effet Joule)"),
        ["E_m = ½·L·i²", "|i| = √(2E_m/L)", "10⁻⁶", "mA"], ["|i| = 2E_m/L", "|i| = √(2 × 72·10⁻⁶/0,1)", "E_m(t₁) = 72 µJ"],
        [aide("Si E_e(t₁) = 0, alors u_C(t₁) = 0 : où est toute l'énergie du circuit à cet instant ? Lis E_m(t₁) sur la courbe (2).",
              "إلى كانت E e de t un égale zéro، إذن u C égale zéro: فين كاينة l'énergie كاملة فهاد اللحظة؟ اقرا E m de t un فla courbe deux."),
         aide("E_m(t₁) = ½·L·i(t₁)², donc |i(t₁)| = √(2E_m(t₁)/L), avec E_m en joules. Et entre 0 et t₁, l'énergie totale a-t-elle pu rester constante ?",
              "E m de t un égale un demi L i au carré، إذن i égale racine de deux E m sur L، وE m بle joule. وبين zéro وt un، واش l'énergie totale بقات ثابتة؟")],
        corr([("5 : à t₁, u_C = 0 ⇒ E_e = 0 : E(t₁) = E_m(t₁) = ½·L·i(t₁)² = 58 µJ", "E m de t un égale cinquante-huit microjoules"),
              ("|i(t₁)| = √(2E_m(t₁)/L) = √(2 × 58·10⁻⁶/0,1) = √(1,16·10⁻³)", "racine de deux E m sur L"),
              ("|i(t₁)| ≈ 3,4·10⁻² A = 34 mA", "trente-quatre milliampères"),
              ("E_m(t₁) < 72 µJ : entre 0 et t₁, de l'énergie a déjà été dissipée par effet Joule (dE/dt = −(R + r)·i² < 0).", "ضاع جزء بl'effet Joule")],
             "السؤال cinq. فt un، E e égale zéro، يعني u C égale zéro: l'énergie كاملة فla bobine. E m de t un égale cinquante-huit microjoules، وهي un demi L i au carré. إذن i égale racine de deux E m sur L، يعني racine de un virgule seize fois dix puissance moins trois. i environ trente-quatre milliampères. وE m صغر من soixante-douze، حيت من zéro حتى t un، ضاع جزء بl'effet Joule."),
        "ex_lc6_5", "fa_lc6_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_lc6_1", "Question 1 : quelle courbe est E_e ?", "À t = 0, i = 0 : E_m(0) = 0 ; la courbe qui part du haut est E_e.",
      SIMD + "energie.html?vue=amortie", "E_e (rouge) part de son maximum, E_m (verte) part de zéro",
      "شوف les courbes ديال l'énergie. فt égale zéro، le condensateur مشارجي وle courant مازال ما بداش: i égale zéro. إذن E m égale un demi L i au carré، égale zéro: la courbe الخضرا كتبدا من zéro. وE e égale un demi C u C au carré، فأكبر قيمة: la courbe الحمرا كتبدا من الفوق. فالتمرين ديالك، la courbe un كتبدا من الفوق: هي E e. وla courbe deux كتبدا من zéro: هي E m.",
      centre=[("t = 0 : i = 0 ⇒ E_m(0) = 0", "la courbe الخضرا كتبدا من zéro"),
              ("(1) = E_e ; (2) = E_m", "la courbe un كتبدا من الفوق: هي E e")],
      pointage=[{"mot": "شوف les courbes ديال l'énergie", "commande": "play_until", "parametres": {"moment": "pertes"}},
                {"mot": "la courbe الخضرا كتبدا من zéro", "repere": "courbe_Em"},
                {"mot": "la courbe الخضرا كتبدا من zéro", "cible": "centre:0"},
                {"mot": "la courbe الحمرا كتبدا من الفوق", "repere": "courbe_Ee"},
                {"mot": "la courbe un كتبدا من الفوق: هي E e", "cible": "centre:1"}]),
    diapo_sim("ex_lc6_2", "Question 2 : U₀ à partir de E_e(0)", "E_e(0) = ½·C·U₀² = 72 µJ ⇒ U₀ = 6 V.",
      SIMD + "energie.html?vue=echange", "Au départ, toute l'énergie est dans le condensateur : 72 µJ",
      "شوف la barre الحمرا فالبداية: كلشي فle condensateur، soixante-douze microjoules. هادي E e de zéro égale un demi C U zéro au carré. إذن U zéro au carré égale deux E e sur C: deux fois soixante-douze fois dix puissance moins six، sur quatre fois dix puissance moins six، يعني trente-six. إذن U zéro égale six volts، وهي la tension ديال الشحن فهاد la simulation.",
      centre=[("E_e(0) = ½·C·U₀² = 72 µJ", "هادي E e de zéro égale un demi C U zéro au carré"),
              ("U₀ = √(2E_e(0)/C) = √36 = 6 V", "إذن U zéro égale six volts")],
      pointage=[{"mot": "شوف la barre الحمرا فالبداية", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "soixante-douze microjoules", "repere": "barre_Ee"},
                {"mot": "هادي E e de zéro égale un demi C U zéro au carré", "cible": "centre:0"},
                {"mot": "هادي E e de zéro", "repere": "formule"},
                {"mot": "إذن U zéro égale six volts", "cible": "centre:1"}]),
    diapo_sim("ex_lc6_3", "Question 3 : deux maximums de E_e par période", "E_e maximale au sommet et au creux : T/2 entre deux maximums.",
      SIMD + "energie.html?vue=echange", "E_e est maximale à t = 0 (sommet de u_C) et à T₀/2 (creux de u_C)",
      "شوف la courbe الحمرا، E e. فt égale zéro، u C فle sommet: E e فأكبر قيمة. من بعد كتنقص، وكلشي كيدوز لla bobine. ومن بعد، عند le creux ديال u C، فT zéro sur deux، environ deux millisecondes: i égale zéro، وE e رجعات لأكبر قيمة. علاش؟ حيت u C au carré: le creux سالب، ولكن le carré موجب. إذن E e عندها deux maximums فكل période. المدة بين deux maximums هي T sur deux، ماشي T. هنا deux millisecondes، إذن T égale quatre millisecondes، وL égale T au carré sur quarante C، يعني zéro virgule un henry.",
      centre=[("E_e = ½·C·u_C² : maximale au sommet et au creux de u_C", "إذن E e عندها deux maximums فكل période"),
              ("Deux maximums successifs : T/2 = 2 ms ⇒ T = 4 ms", "إذن T égale quatre millisecondes"),
              ("L = T²/(4π²·C) = 0,1 H", "يعني zéro virgule un henry")],
      pointage=[{"mot": "شوف la courbe الحمرا", "commande": "play_until", "parametres": {"moment": "depart"}},
                {"mot": "من بعد كتنقص", "commande": "play_until", "parametres": {"moment": "tout_bobine"}},
                {"mot": "عند le creux ديال u C", "commande": "play_until", "parametres": {"moment": "tout_condensateur"}},
                {"mot": "وE e رجعات لأكبر قيمة", "repere": "courbe_Ee"},
                {"mot": "إذن E e عندها deux maximums فكل période", "cible": "centre:0"},
                {"mot": "إذن T égale quatre millisecondes", "cible": "centre:1"},
                {"mot": "يعني zéro virgule un henry", "cible": "centre:2"}]),
    diapo_sim("ex_lc6_4", "Question 4 : l'énergie dissipée", "À un maximum de E_e, i = 0 : E = E_e ; E_J = E(0) − E(t₂).",
      SIMD + "energie.html?vue=amortie", "Les sommets de u_C à t = 0 et t = T : |ΔE| = ½·C·(6² − 4²) = 4·10⁻⁵ J",
      "شوف les deux sommets ديال u C: فt égale zéro وفt égale T. فكل sommet، i égale zéro: E m égale zéro، وl'énergie totale هي E e. فالأول، soixante-douze microjoules. فالتاني، u C environ quatre volts: E e environ trente-deux microjoules. l'énergie اللي ضاعت: soixante-douze moins trente-deux، يعني quarante microjoules، quatre fois dix puissance moins cinq joule. ديما E ديال البداية moins E ديال اللخر.",
      centre=[("Sommet : i = 0 ⇒ E = E_e", "وl'énergie totale هي E e"),
              ("E_J = 72 − 32 = 40 µJ = 4·10⁻⁵ J", "يعني quarante microjoules")],
      pointage=[{"mot": "شوف les deux sommets", "commande": "play_until", "parametres": {"moment": "deux_sommets"}},
                {"mot": "فالأول، soixante-douze microjoules", "repere": "sommet_1"},
                {"mot": "وl'énergie totale هي E e", "cible": "centre:0"},
                {"mot": "فالتاني، u C environ quatre volts", "repere": "sommet_2"},
                {"mot": "يعني quarante microjoules", "repere": "energie_perdue"},
                {"mot": "يعني quarante microjoules", "cible": "centre:1"}]),
    diapo_sim("ex_lc6_5", "Question 5 : |i| quand u_C = 0", "u_C = 0 : E = E_m = ½·L·i² ⇒ |i| = √(2E_m/L).",
      SIMD + "energie.html?vue=echange", "Quand u_C = 0, E_e = 0 : toute l'énergie est dans la bobine",
      "شوف ملي u C كتوصل à zéro: la barre الحمرا خاوية، وكلشي فla bobine. فهاد la simulation بلا résistance، E m égale soixante-douze microjoules. E m égale un demi L i au carré، إذن i égale racine de deux E m sur L. هنا racine de deux fois soixante-douze fois dix puissance moins six، sur zéro virgule un: environ trente-huit milliampères. فالتمرين ديالك، كاينة résistance: قبل ما توصل u C à zéro، ضاع جزء بl'effet Joule. لهذا E m de t un صغر من soixante-douze microjoules، خود la valeur اللي مكتوبة فla courbe deux.",
      centre=[("u_C = 0 ⇒ E = E_m = ½·L·i²", "وكلشي فla bobine"),
              ("|i| = √(2E_m/L)", "إذن i égale racine de deux E m sur L"),
              ("Avec R + r ≠ 0 : E_m(t₁) < E(0) (effet Joule)", "ضاع جزء بl'effet Joule")],
      pointage=[{"mot": "شوف ملي u C كتوصل à zéro", "commande": "play_until", "parametres": {"moment": "tout_bobine"}},
                {"mot": "la barre الحمرا خاوية", "repere": "barre_Ee"},
                {"mot": "وكلشي فla bobine", "repere": "barre_Em"},
                {"mot": "وكلشي فla bobine", "cible": "centre:0"},
                {"mot": "إذن i égale racine de deux E m sur L", "cible": "centre:1"},
                {"mot": "ضاع جزء بl'effet Joule", "cible": "centre:2"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_lc6_1", "Plus facile : la courbe qui part de zéro", "سؤال ساهل: أشمن énergie كتبدا من zéro؟",
      "À t = 0, le condensateur est chargé et i(0) = 0. Quelle énergie est nulle à t = 0 ?",
      ["E_e, celle du condensateur", "E_m, celle de la bobine", "aucune des deux"], 1, {
        "1": {"juste": rep("برافو! E m égale un demi L i au carré، وi de zéro égale zéro.", "Juste : E_m(0) = ½·L·i(0)² = 0.")},
        "0": {"1": rep("le condensateur مشارجي فالبداية: واش E e ديالو zéro؟ شوف شنو اللي zéro فالبداية: u C ولا i؟ عاود اختار.", "Le condensateur est chargé : son énergie n'est pas nulle. Qu'est-ce qui est nul, u_C ou i ? Réessaie."),
              "2": rep("الجواب: E m. i de zéro égale zéro، إذن E m de zéro égale zéro.", "Réponse : E_m, car i(0) = 0.")},
        "2": {"1": rep("فكر فi de zéro. شنو كتعطي dans un demi L i au carré؟ عاود اختار.", "Pense à i(0) = 0 dans ½·L·i². Réessaie."),
              "2": rep("الجواب: E m، حيت i de zéro égale zéro.", "Réponse : E_m = 0 à t = 0.")}},
      "À t égale zéro, i de zéro égale zéro. Quelle énergie est nulle ?"),
    qcm_facile("fa_lc6_2", "Plus facile : U₀ à partir de l'énergie", "سؤال ساهل: حسب U zéro.",
      "C = 4 µF et E_e(0) = 72 µJ. U₀ vaut…",
      ["36 V", "6 V", "18 V"], 1, {
        "1": {"juste": rep("برافو! racine de deux fois soixante-douze sur quatre، racine de trente-six، six volts.", "Juste : U₀ = √(2 × 72/4) = √36 = 6 V.")},
        "0": {"1": rep("trente-six هي U zéro au carré. ما نسيتيش la racine؟ عاود اختار.", "36 est U₀² : il manque la racine. Réessaie."),
              "2": rep("الجواب: six volts. trente-six هي le carré.", "Réponse : 6 V ; 36 V² est U₀².")},
        "2": {"1": rep("نسيتي un demi ولا la racine. U zéro au carré égale deux E e sur C. عاود اختار.", "U₀² = 2E_e/C : vérifie le 2 et la racine. Réessaie."),
              "2": rep("الجواب: six volts، racine de deux E e sur C.", "Réponse : U₀ = √(2E_e/C) = 6 V.")}},
      "C égale quatre microfarads et E e de zéro égale soixante-douze microjoules. U zéro vaut ?"),
    qcm_facile("fa_lc6_3", "Plus facile : le piège de T/2", "سؤال ساهل على le piège ديال T sur deux.",
      "Entre deux maximums successifs de E_e, on lit 2 ms. La pseudo-période de u_C vaut…",
      ["1 ms", "2 ms", "4 ms"], 2, {
        "2": {"juste": rep("برافو! E e كتوصل لأكبر قيمة deux fois فكل période، إذن T égale deux fois deux، quatre millisecondes.", "Juste : deux maximums par pseudo-période, T = 2 × 2 = 4 ms.")},
        "0": {"1": rep("لا، T أكبر من المدة بين deux maximums ديال E e، ماشي أصغر. عاود اختار.", "T est plus grande que l'écart entre deux maximums de E_e, pas plus petite. Réessaie."),
              "2": rep("الجواب: quatre millisecondes. فكل période، deux maximums: le sommet وle creux.", "Réponse : 4 ms (sommet et creux de u_C).")},
        "1": {"1": rep("هادا هو le piège: E e فيها u C au carré، وle creux حتى هو كيعطي maximum. شحال من maximum فكل période؟ عاود اختار.", "Piège : E_e ∝ u_C², le creux de u_C donne aussi un maximum. Réessaie."),
              "2": rep("الجواب: quatre millisecondes. deux millisecondes هي T sur deux.", "Réponse : 4 ms ; 2 ms est T/2.")}},
      "Entre deux maximums successifs de E e, on lit deux millisecondes. La pseudo-période vaut ?"),
    qcm_facile("fa_lc6_4", "Plus facile : l'énergie dissipée", "سؤال ساهل: l'énergie اللي ضاعت.",
      "E(0) = 72 µJ ; à t₂, E_m = 0 et E_e = 32 µJ. L'énergie dissipée entre 0 et t₂ vaut…",
      ["40 µJ", "32 µJ", "104 µJ"], 0, {
        "0": {"juste": rep("برافو! soixante-douze moins trente-deux، quarante microjoules.", "Juste : 72 − 32 = 40 µJ.")},
        "1": {"1": rep("trente-deux هي l'énergie اللي بقات، ماشي اللي ضاعت. عاود اختار.", "32 µJ est l'énergie qui reste, pas celle perdue. Réessaie."),
              "2": rep("الجواب: quarante microjoules، E de zéro moins E de t deux.", "Réponse : E(0) − E(t₂) = 40 µJ.")},
        "2": {"1": rep("جمعتي. l'énergie اللي ضاعت هي الفرق. عاود اختار.", "Tu as additionné : l'énergie dissipée est une différence. Réessaie."),
              "2": rep("الجواب: soixante-douze moins trente-deux، quarante microjoules.", "Réponse : 72 − 32 = 40 µJ.")}},
      "E de zéro égale soixante-douze microjoules, E de t deux égale trente-deux microjoules. L'énergie dissipée vaut ?"),
    vrai_faux_facile("fa_lc6_5", "Plus facile : vrai ou faux", "سؤال ساهل على l'énergie ملي u C égale zéro.",
      "Circuit RLC, à l'instant t₁ où u_C = 0.",
      [("À t₁, toute l'énergie du circuit est dans la bobine : E = ½·L·i².", True, "u_C = 0 ⇒ E_e = 0 : E = E_m."),
       ("|i(t₁)| = √(2E_m(t₁)/L).", True, "On isole i dans E_m = ½·L·i²."),
       ("Avec R + r = 20 Ω, E_m(t₁) est égale à E(0) = 72 µJ.", False, "Entre 0 et t₁, de l'énergie a déjà été dissipée par effet Joule : E_m(t₁) < 72 µJ.")]),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même étude avec un condensateur de capacité C = 10 µF, une autre bobine et R + r = 20 Ω. La figure 2 donne les deux énergies (1) et (2). On admet T = T₀ ; π² = 10.",
      "intro_dit": "نفس التمرين، بقيم أخرى. C égale dix microfarads، bobine أخرى، وR plus r égale vingt ohms.",
      "figures": [FIGB],
      "donnees": ["C = 10 µF = 10⁻⁵ F", "R + r = 20 Ω", "π² = 10"],
      "questions": [
        question_semblable("1", "Identifier, en justifiant, la courbe de E_e(t) et celle de E_m(t).",
          phrase(IDENT.replace("72 µJ", "80 µJ")), ["i(0) = 0", "E_m(0) = 0"], ["(1) = E_m"],
          corr([("1 : i(0) = 0 ⇒ E_m(0) = 0 : (2) = E_m ; (1) = E_e", "la courbe un هي E e")],
               "i de zéro égale zéro، إذن E m de zéro égale zéro: la courbe deux هي E m، وla courbe un هي E e.")),
        question_semblable("2", "Déterminer U₀ = u_C(0).",
          valeur("U₀", 4, "V", "U₀ = √(2E_e(0)/C) = √(2 × 80·10⁻⁶/10⁻⁵) = √16 = 4 V"), ["U₀ = √(2E_e/C)", "V"], ["U₀ = 16 V"],
          corr([("2 : E_e(0) = 80 µJ ⇒ U₀ = √(2E_e(0)/C) = √16", "racine de seize"), ("U₀ = 4 V", "U zéro égale quatre volts")],
               "E e de zéro égale quatre-vingts microjoules. U zéro égale racine de deux E e sur C، يعني racine de seize، U zéro égale quatre volts.")),
        question_semblable("3", "Montrer que deux maximums successifs de E_e sont séparés de T/2 ; en déduire T, puis L.",
          valeur("L", 0.25, "H", "T/2 = 5 ms ⇒ T = 10 ms ; L = T²/(4π²·C) = (10⁻²)²/(40 × 10⁻⁵) = 0,25 H"), ["T/2", "L = T²/(4π²C)", "H"], ["T = 5 ms", "L = 0,0625 H"],
          corr([("3 : E_e maximale au sommet et au creux de u_C : T/2 = 5 ms ⇒ T = 10 ms", "T égale dix millisecondes"), ("L = (10⁻²)²/(40 × 10⁻⁵) = 0,25 H", "L égale zéro virgule vingt-cinq henry")],
               "deux maximums فكل pseudo-période، إذن T sur deux égale cinq millisecondes، وT égale dix millisecondes. L égale T au carré sur quarante C، L égale zéro virgule vingt-cinq henry.")),
        question_semblable("4", "Calculer l'énergie E_J dissipée par effet Joule entre t = 0 et t₂.",
          valeur("E_J", 4.4e-5, "J", "E_J = E(0) − E_e(t₂) = 80 − 36 = 44 µJ = 4,4·10⁻⁵ J"), ["E_J = E(0) − E(t₂)", "J"], ["E_J = 36 µJ"],
          corr([("4 : à t₂, E_m = 0 : E_J = 80 − 36 = 44 µJ", "quatre-vingts moins trente-six"), ("E_J = 4,4·10⁻⁵ J", "quatre virgule quatre fois dix puissance moins cinq joule")],
               "فt deux، E m égale zéro. E J égale quatre-vingts moins trente-six، يعني quarante-quatre microjoules، quatre virgule quatre fois dix puissance moins cinq joule.")),
        question_semblable("5", "À t₁, la courbe (1) s'annule. Calculer |i(t₁)| (en mA) et expliquer pourquoi E_m(t₁) < E(0).",
          valeur("|i(t₁)|", 22.8, "mA", "|i(t₁)| = √(2E_m(t₁)/L) = √(2 × 65·10⁻⁶/0,25) ≈ 2,28·10⁻² A = 22,8 mA"), ["|i| = √(2E_m/L)", "mA"], ["E_m(t₁) = 80 µJ"],
          corr([("5 : u_C = 0 ⇒ E = E_m = 65 µJ ; |i| = √(2 × 65·10⁻⁶/0,25)", "racine de deux E m sur L"), ("|i(t₁)| ≈ 22,8 mA ; E_m < 80 µJ à cause de l'effet Joule", "environ vingt-deux virgule huit milliampères")],
               "فt un، u C égale zéro، إذن E égale E m، soixante-cinq microjoules. i égale racine de deux E m sur L، environ vingt-deux virgule huit milliampères. وE m صغر من quatre-vingts بسبب l'effet Joule.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
