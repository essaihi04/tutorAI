# Exercice de physique, ch. 8 (oscillations libres d'un circuit RLC série), niveau moyen n° 4 :
# l'amortissement : équation en q du RLC, régime et explication énergétique, dE/dt = −(R + r)·i², énergie dissipée.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - pas de fichier d'exploration pour ce chapitre : architecture backend/data/curriculum/architecture/phys_ch8_circuit_RLC.md
#    (« calculer une énergie, à un instant, perdue entre deux sommets » : 14 sessions ; « établir l'équation » très fréquent),
#    fiche du cadre circuit_RLC (RLC3, RLC7), docs/parties_voix/phys_ch8_circuit_RLC.json.
#  - cours phys_ch8_circuit_RLC : lc_e1 à lc_e3 (équation en q), lc_a1_joule, lc_a2_derivee, lc_a3_dEdt, lc_a4_perdue
#    (« E du début moins E de la fin », aux sommets i = 0).
#  - nationaux : 2016 N (ΔE entre deux instants, puis interpréter), 2022 N (ΔE dissipée entre t₀ et t₁), 2023 R (|ΔE| par
#    effet Joule), 2024 N (« expliquer l'amortissement », E_j = |ΔE_t|), 2025 N (dE/dt) : mêmes gestes, notre situation.
#  - séries en ligne : recherche faite (talamidi, moutamadris, Naceiri, dreamjob) mais PDF non joignables depuis cette session ;
#    nos données sont celles de energie.html (vue amortie) : C = 4 µF, E = 6 V, L = 0,1 H, R = r = 10 Ω, sommets 6 V puis 4,0 V.
import sys, math, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch8_rlc_4"
SIMD = "/media/simulations/physics/circuit-rlc-tableau/"


def u_amortie(E, L, C, Rt):
    """Solution exacte de L·q'' + Rt·q' + q/C = 0, u_C(0) = E, i(0) = 0 ; t en ms (même calcul que energie.html)."""
    lam = Rt / (2 * L); w = math.sqrt(1 / (L * C) - lam ** 2)
    expr = f"{E}*exp(-{lam / 1000:.6g}*x)*(cos({w / 1000:.6g}*x)+{lam / w:.6g}*sin({w / 1000:.6g}*x))"
    T = 2 * math.pi / w
    return expr, T * 1000, E * math.exp(-lam * T)


def grille(tmax, dt, ymin, ymax, dy):
    els, k = [], 0
    while k * dt <= tmax + 1e-9:
        els.append({"f": "ligne", "pts": [[round(k * dt, 4), ymin], [round(k * dt, 4), ymax]], "couleur": "faible"}); k += 1
    k = 0
    while ymin + k * dy <= ymax + 1e-9:
        y = round(ymin + k * dy, 4); els.append({"f": "ligne", "pts": [[0, y], [tmax, y]], "couleur": "faible"}); k += 1
    return els


def courbe_uc(titre, E, L, C, Rt, tmax, umax, dt, lu):
    expr, Tms, u1 = u_amortie(E, L, C, Rt)
    els = grille(tmax, dt, -umax, umax, 2) + [
        {"f": "courbe", "expr": expr, "de": 0, "a": tmax, "couleur": "rouge"},
        {"f": "point", "at": [0, E], "couleur": "jaune"},
        {"f": "point", "at": [round(Tms, 3), round(u1, 3)], "t": f"t₁ : {lu}", "pos": "n", "couleur": "jaune"}]
    return figure_courbe(titre, axe("t", 0, tmax, "ms", list(range(0, tmax + 1, dt))),
                         axe("u_C", -umax, umax, "V", list(range(-umax, umax + 1, 2))), els,
                         legende="t₁ : deuxième sommet de u_C (première pseudo-période)."), Tms, u1


def montage(titre):
    """Décharge (K en 2) dans R et la bobine (L, r) ; i orienté vers A ; flèches en convention récepteur."""
    g = [dipole([0.8, 0.8], [0.8, 3.6], "G", "E", pos="o"),
         fil([0.8, 3.6], [2.9, 3.6]),
         inverseur([3.4, 2.8], [2.9, 3.6], [3.9, 3.6], t="K", pos_t=[3.95, 2.75]),
         dipole([3.4, 2.8], [3.4, 0.8], "C", "C", pos="e"),
         borne([3.4, 2.05], "A", "o"), borne([3.4, 0.8], "B", "s"),
         tension([2.1, 1.2], [2.1, 2.4], "u_C", pos="o"),
         fil([3.9, 3.6], [4.6, 3.6]),
         dipole([4.6, 3.6], [6.6, 3.6], "R", "R", pos="s"),
         tension([5.0, 4.2], [6.2, 4.2], "u_R", pos="n"),
         fil([6.6, 3.6], [7.6, 3.6]),
         dipole([7.6, 3.6], [7.6, 0.8], "L", "(L, r)", pos="o"),
         tension([8.3, 3.2], [8.3, 1.2], "u_b", pos="e"),
         fil([7.6, 0.8], [0.8, 0.8]),
         courant([4.1, 0.8], "d")]
    return schema(titre, 9.8, 4.9, *g)


# ---------------------------------------------------------------- données et calculs
E, C, L, R, r = 6, 4e-6, 0.1, 10, 10
FIG, T_MS, U1_VRAI = courbe_uc("Figure 2 : u_C(t) après la bascule", E, L, C, R + r, 12, 8, 1, "4,0 V")
U1 = 4.0                                              # lu sur la figure
E0 = 0.5 * C * E ** 2
E1 = 0.5 * C * U1 ** 2
EJ = E0 - E1
assert abs(U1_VRAI - 4.03) < 0.02 and abs(T_MS - 3.98) < 0.01
assert abs(E0 - 7.2e-5) < 1e-15 and abs(EJ - 4e-5) < 1e-15
# semblable : C = 10 µF, E = 8 V, L = 0,25 H, R + r = 24 Ω (R = 16 Ω, r = 8 Ω), sommet t₁ : 5,0 V
FIGB, TB, U1B_VRAI = courbe_uc("Figure 2 : u_C(t) après la bascule", 8, 0.25, 10e-6, 24, 30, 10, 3, "5,0 V")
E0b = 0.5 * 10e-6 * 64; EJb = 0.5 * 10e-6 * (64 - 25)
assert abs(U1B_VRAI - 4.96) < 0.03 and abs(E0b - 3.2e-4) < 1e-15 and abs(EJb - 1.95e-4) < 1e-15

EQ = ("Additivité (K en 2) : u_C + u_R + u_b = 0, avec u_C = q/C, u_R = R·i, u_b = L·di/dt + r·i et i = dq/dt. "
      "D'où L·d²q/dt² + (R + r)·dq/dt + q/C = 0.")
REG = ("Régime pseudo-périodique : u_C oscille mais l'amplitude diminue. L'énergie totale du circuit diminue car une partie "
       "est dissipée en chaleur par effet Joule dans la résistance totale R + r : c'est l'amortissement.")
DEDT = ("E = q²/(2C) + ½·L·i², donc dE/dt = (q/C)·dq/dt + L·i·di/dt = i·(q/C + L·d²q/dt²). D'après l'équation, "
        "q/C + L·d²q/dt² = −(R + r)·i, donc dE/dt = −(R + r)·i² ≤ 0 : l'énergie totale diminue.")

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "circuit_RLC", "cours": "phys_ch8_circuit_RLC",
  "titre": "L'amortissement : équation, dE/dt et énergie dissipée", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir l'équation différentielle en q du circuit RLC série", "Expliquer l'amortissement par l'effet Joule",
                  "Montrer que dE/dt = −(R + r)·i²", "Calculer l'énergie totale et l'énergie dissipée entre deux sommets"],
  "enonce": {
    "intro": "On charge totalement un condensateur de capacité C sous la tension E (K en position 1). À t = 0, on bascule K en position 2 : le condensateur se décharge dans un conducteur ohmique de résistance R et une bobine (L, r) (figure 1). On enregistre u_C(t) (figure 2). On note q la charge de l'armature A et i = dq/dt.",
    "intro_dit": "دابا نقراو l'énoncé. كنشارجيو un condensateur، la capacité ديالو C، تحت la tension E، وK فla position un. فt égale zéro، كنبدلو K لla position deux: le condensateur كيتفرغ فconducteur ohmique R، وفla bobine L r. هادي la figure un. وكنسجلو u C، فla figure deux. q هي la charge ديال l'armature A، وi égale dé q sur dé t.",
    "figures": [montage("Figure 1 : le circuit RLC série"), FIG],
    "donnees": ["E = 6 V", "C = 4 µF = 4·10⁻⁶ F", "L = 0,1 H", "R = 10 Ω ; r = 10 Ω"],
    "questions": [
      question("1", "Établir l'équation différentielle vérifiée par la charge q(t) lorsque K est en position 2.",
        "السؤال un: بين l'équation différentielle اللي كتحققها la charge q ملي K فla position deux.",
        phrase(EQ),
        ["u_C + u_R + u_b = 0", "u_C = q/C", "u_R = R·i", "u_b = L·di/dt + r·i", "i = dq/dt"], ["u_C + u_R + u_b = E", "u_b = L·di/dt", "u_C = C·q"],
        [aide("Sans générateur, la somme des trois tensions de la maille est nulle. Écris ensuite chaque tension en fonction de q ou de i.",
              "بلا générateur، la somme ديال les trois tensions فla maille égale zéro. من بعد كتب كل tension بq ولا بi."),
         aide("u_C = q/C ; u_R = R·i ; u_b = L·di/dt + r·i ; puis i = dq/dt et di/dt = d²q/dt². Range les termes.",
              "u C égale q sur C. u R égale R i. u b égale L dé i sur dé t، plus r i. ومن بعد i égale dé q sur dé t، وdé i sur dé t égale dé deux q sur dé t deux. رتب les termes.")],
        corr([("1 : additivité : u_C + u_R + u_b = 0", "u C plus u R plus u b égale zéro"),
              ("q/C + R·i + L·di/dt + r·i = 0, avec i = dq/dt", "q sur C، plus R i، plus L dé i sur dé t، plus r i"),
              ("L·d²q/dt² + (R + r)·dq/dt + q/C = 0", "L dé deux q sur dé t deux، plus R plus r fois dé q sur dé t، plus q sur C، égale zéro")],
             "السؤال un. ما كاينش générateur: u C plus u R plus u b égale zéro. كنعوضو: q sur C، plus R i، plus L dé i sur dé t، plus r i، égale zéro. وi égale dé q sur dé t. إذن L dé deux q sur dé t deux، plus R plus r fois dé q sur dé t، plus q sur C، égale zéro."),
        "ex_lc4_1", "fa_lc4_1"),
      question("2", "Nommer le régime observé sur la figure 2, puis expliquer, d'un point de vue énergétique, la diminution de l'amplitude.",
        "السؤال deux: سمي le régime اللي فla figure deux، ومن بعد شرح، من جهة l'énergie، علاش l'amplitude كتنقص.",
        phrase(REG),
        ["pseudo-périodique", "effet Joule", "R + r", "chaleur", "énergie totale"], ["périodique", "la bobine crée de l'énergie"],
        [aide("Regarde la hauteur des sommets de u_C : reste-t-elle la même ? Quel dipôle transforme l'énergie électrique en chaleur ?",
              "شوف العلو ديال les sommets ديال u C: واش كيبقى هو هو؟ وأشمن dipôle كيحول l'énergie électrique لchaleur؟"),
         aide("Oscillations dont l'amplitude diminue : pseudo-périodique. L'énergie perdue part en chaleur par effet Joule dans R et r.",
              "oscillations وl'amplitude كتنقص: pseudo-périodique. l'énergie اللي كتضيع كتمشي chaleur، بl'effet Joule، فR وفr.")],
        corr([("2 : u_C oscille et ses sommets diminuent : régime pseudo-périodique.", "le régime pseudo-périodique"),
              ("L'énergie totale diminue : elle est dissipée en chaleur par effet Joule dans R + r (amortissement).", "بl'effet Joule")],
             "السؤال deux. u C كتمشي وتجي، ولكن les sommets كينقصو: le régime pseudo-périodique. l'énergie totale كتنقص، حيت جزء منها كيتحول chaleur بl'effet Joule، فla résistance totale R plus r. هادا هو l'amortissement."),
        "ex_lc4_2", "fa_lc4_2"),
      question("3", "L'énergie totale du circuit est E = q²/(2C) + ½·L·i². Montrer que dE/dt = −(R + r)·i², et conclure.",
        "السؤال trois: l'énergie totale هي E égale q au carré sur deux C، plus un demi L i au carré. بين بلي dé E sur dé t égale moins R plus r fois i au carré، واستنتج.",
        phrase(DEDT),
        ["dE/dt", "d(q²)/dt = 2q·dq/dt", "d(i²)/dt = 2i·di/dt", "i = dq/dt", "−(R + r)·i²"], ["dE/dt = (R + r)·i²", "dE/dt = 0"],
        [aide("Dérive chaque terme : d(q²/(2C))/dt = (q/C)·dq/dt et d(½·L·i²)/dt = L·i·di/dt. Mets i en facteur.",
              "دير la dérivée ديال كل terme: la dérivée ديال q au carré sur deux C هي q sur C fois dé q sur dé t، وديال un demi L i au carré هي L i dé i sur dé t. خرج i facteur."),
         aide("Tu obtiens dE/dt = i·(q/C + L·d²q/dt²). Utilise l'équation de la question 1 pour remplacer la parenthèse.",
              "غادي تلقى dé E sur dé t égale i fois، q sur C plus L dé deux q sur dé t deux. استعمل l'équation ديال السؤال un باش تعوض هاد la parenthèse.")],
        corr([("3 : dE/dt = (q/C)·dq/dt + L·i·di/dt = i·(q/C + L·d²q/dt²)", "i fois، q sur C plus L dé deux q sur dé t deux"),
              ("D'après l'équation : q/C + L·d²q/dt² = −(R + r)·dq/dt = −(R + r)·i", "égale moins R plus r fois i"),
              ("dE/dt = −(R + r)·i² ≤ 0 : E diminue (effet Joule).", "dé E sur dé t égale moins R plus r fois i au carré")],
             "السؤال trois. la dérivée: q sur C fois dé q sur dé t، plus L i dé i sur dé t. يعني i fois، q sur C plus L dé deux q sur dé t deux. من l'équation، هاد la parenthèse égale moins R plus r fois i. إذن dé E sur dé t égale moins R plus r fois i au carré، وهي سالبة: l'énergie totale كتنقص بl'effet Joule."),
        "ex_lc4_3", "fa_lc4_3"),
      question("4", "Calculer l'énergie totale E₀ du circuit à t = 0.",
        "السؤال quatre: حسب l'énergie totale E zéro ديال الدارة فt égale zéro.",
        valeur("E₀", 7.2e-5, "J", "À t = 0 : u_C = E = 6 V et i = 0, donc E₀ = ½·C·E² = ½ × 4·10⁻⁶ × 6² = 7,2·10⁻⁵ J"),
        ["E = ½·C·u_C² + ½·L·i²", "i(0) = 0", "10⁻⁶", "J"], ["E₀ = ½·C·E", "E₀ = ½·L·i²", "C = 4 F"],
        [aide("À t = 0, le condensateur est chargé sous E et le courant n'a pas encore commencé : que vaut i(0) ?",
              "فt égale zéro، le condensateur مشارجي تحت E، وle courant مازال ما بداش: شحال i de zéro؟"),
         aide("i(0) = 0, donc toute l'énergie est dans le condensateur : E₀ = ½·C·E², avec C en farads.",
              "i de zéro égale zéro، إذن l'énergie كلها فle condensateur: E zéro égale un demi C E au carré، وC بle farad.")],
        corr([("4 : à t = 0, u_C = E et i = 0 : E₀ = ½·C·E²", "E zéro égale un demi C E au carré"),
              ("A.N. : E₀ = ½ × 4·10⁻⁶ × 6²", "un demi fois quatre fois dix puissance moins six"),
              ("E₀ = 7,2·10⁻⁵ J", "sept virgule deux fois dix puissance moins cinq joule")],
             "السؤال quatre. فt égale zéro، u C égale E وi égale zéro. إذن E zéro égale un demi C E au carré. يعني un demi fois quatre fois dix puissance moins six، fois six au carré. E zéro égale sept virgule deux fois dix puissance moins cinq joule."),
        "ex_lc4_4", "fa_lc4_4"),
      question("5", "Calculer l'énergie E_J dissipée par effet Joule entre t = 0 et la date t₁ du deuxième sommet (figure 2).",
        "السؤال cinq: حسب l'énergie E J اللي ضاعت بl'effet Joule، بين t égale zéro وt un، اللي هي le deuxième sommet فla figure deux.",
        valeur("E_J", 4e-5, "J", "À t₁ : u_C = 4,0 V et i = 0 ; E₁ = ½·C·u_C(t₁)² = 3,2·10⁻⁵ J ; E_J = E₀ − E₁ = ½·C·(6² − 4²) = ½ × 4·10⁻⁶ × 20 = 4·10⁻⁵ J"),
        ["E_J = E₀ − E₁", "i = 0 au sommet", "½·C·(U₀² − U₁²)", "J"], ["½·C·(6 − 4)²", "E_J = E₁", "E_J = E₁ − E₀ < 0"],
        [aide("À un sommet de u_C, que vaut i ? Lis u_C(t₁) sur la figure 2 et calcule l'énergie totale E₁ à t₁.",
              "فsommet ديال u C، شحال i؟ اقرا u C de t un فla figure deux، وحسب l'énergie totale E un فt un."),
         aide("Aux deux sommets i = 0 : E = ½·C·u_C². L'énergie dissipée est la diminution : E_J = E₀ − E₁ = ½·C·(6² − 4²).",
              "فles deux sommets، i égale zéro: E égale un demi C u C au carré. l'énergie اللي ضاعت هي الفرق: E J égale E zéro moins E un، يعني un demi C، fois six au carré moins quatre au carré.")],
        corr([("5 : au sommet t₁, i = 0 et u_C(t₁) = 4,0 V : E₁ = ½·C·u_C(t₁)² = 3,2·10⁻⁵ J", "E un égale trois virgule deux fois dix puissance moins cinq joule"),
              ("E_J = E₀ − E₁ = ½·C·(6² − 4²) = ½ × 4·10⁻⁶ × 20", "six au carré moins quatre au carré"),
              ("E_J = 4·10⁻⁵ J, transformée en chaleur dans R + r", "E J égale quatre fois dix puissance moins cinq joule")],
             "السؤال cinq. فle sommet t un، i égale zéro وu C égale quatre volts. إذن E un égale un demi C fois seize، يعني E un égale trois virgule deux fois dix puissance moins cinq joule. l'énergie اللي ضاعت: E zéro moins E un، يعني un demi C، fois six au carré moins quatre au carré، يعني un demi fois quatre fois dix puissance moins six fois vingt. E J égale quatre fois dix puissance moins cinq joule، مشات chaleur فR وفr."),
        "ex_lc4_5", "fa_lc4_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_lc4_1", "Question 1 : l'équation en q", "u_C + u_R + u_b = 0 ⇒ L·d²q/dt² + (R + r)·dq/dt + q/C = 0.",
      SIMD + "equation.html", "La maille de décharge : chaque tension remplacée, puis l'équation en q",
      "شوف la maille: le condensateur، le résistor R، وla bobine L r. ما كاينش générateur، إذن u C plus u R plus u b égale zéro. كنعوضو كل tension تحت la flèche ديالها: u C égale q sur C، u R égale R i، وu b égale L dé i sur dé t plus r i. من بعد i égale dé q sur dé t، وdé i sur dé t égale dé deux q sur dé t deux. كنرتبو، وكنلقاو: L dé deux q sur dé t deux، plus R plus r fois dé q sur dé t، plus q sur C، égale zéro.",
      centre=[("u_C + u_R + u_b = 0", "إذن u C plus u R plus u b égale zéro"),
              ("q/C + R·i + L·di/dt + r·i = 0", "كنعوضو كل tension"),
              ("L·d²q/dt² + (R + r)·dq/dt + q/C = 0", "وكنلقاو: L dé deux q sur dé t deux")],
      pointage=[{"mot": "شوف la maille", "commande": "play_until", "parametres": {"moment": "fleches"}},
                {"mot": "إذن u C plus u R plus u b égale zéro", "commande": "play_until", "parametres": {"moment": "additivite"}},
                {"mot": "إذن u C plus u R plus u b égale zéro", "cible": "centre:0"},
                {"mot": "كنعوضو كل tension", "commande": "play_until", "parametres": {"moment": "remplacer"}},
                {"mot": "كنعوضو كل tension", "cible": "centre:1"},
                {"mot": "من بعد i égale dé q sur dé t", "commande": "play_until", "parametres": {"moment": "deriver_deux_fois"}},
                {"mot": "كنرتبو", "commande": "play_until", "parametres": {"moment": "equation_q"}},
                {"mot": "وكنلقاو: L dé deux q sur dé t deux", "cible": "centre:2"}]),
    diapo_sim("ex_lc4_2", "Question 2 : pourquoi les sommets baissent", "L'énergie totale diminue : effet Joule dans R + r.",
      SIMD + "energie.html?vue=amortie", "E_e, E_m et E(t) avec R + r = 20 Ω : E descend ; le résistor chauffe",
      "شوف les courbes ديال l'énergie، مع R plus r égale vingt ohms، بحال التمرين ديالك. الحمرا ديال le condensateur، والخضرا ديال la bobine. وشوف la courbe البيضا، l'énergie totale: ما بقاتش ثابتة، كتنقص بالدرج. فين مشات؟ شوف le résistor: كيسخن. l'énergie كتتحول chaleur، بl'effet Joule، فR وفr. لهذا les sommets ديال u C كينقصو: هادا le régime pseudo-périodique.",
      centre=[("E diminue : effet Joule dans R + r", "بl'effet Joule، فR وفr"),
              ("Amplitude qui diminue → régime pseudo-périodique", "هادا le régime pseudo-périodique")],
      pointage=[{"mot": "شوف les courbes ديال l'énergie", "commande": "play_until", "parametres": {"moment": "pertes"}},
                {"mot": "الحمرا ديال le condensateur", "repere": "courbe_Ee"},
                {"mot": "والخضرا ديال la bobine", "repere": "courbe_Em"},
                {"mot": "la courbe البيضا، l'énergie totale", "repere": "courbe_E"},
                {"mot": "شوف le résistor", "commande": "play_until", "parametres": {"moment": "chaleur"}},
                {"mot": "كيسخن", "repere": "resistance"},
                {"mot": "بl'effet Joule، فR وفr", "cible": "centre:0"},
                {"mot": "هادا le régime pseudo-périodique", "cible": "centre:1"}]),
    diapo_sim("ex_lc4_3", "Question 3 : dE/dt = −(R + r)·i²", "dE/dt = i·(q/C + L·d²q/dt²) = −(R + r)·i².",
      SIMD + "energie.html?vue=amortie", "Dériver chaque énergie, puis remplacer par l'équation",
      "دابا نديرو la dérivée ديال l'énergie totale. la dérivée ديال un demi C u C au carré هي u C fois i، يعني q sur C fois i. وla dérivée ديال un demi L i au carré هي L i dé i sur dé t. كنخرجو i facteur: dé E sur dé t égale i fois، q sur C plus L dé deux q sur dé t deux. من l'équation، هاد la parenthèse égale moins R plus r fois i. إذن dé E sur dé t égale moins R plus r fois i au carré. i au carré ديما موجب، إذن dé E sur dé t سالبة: l'énergie كتنقص.",
      centre=[("dE/dt = (q/C)·i + L·i·di/dt", "la dérivée ديال un demi C u C au carré"),
              ("q/C + L·d²q/dt² = −(R + r)·i", "هاد la parenthèse égale moins R plus r fois i"),
              ("dE/dt = −(R + r)·i² ≤ 0", "إذن dé E sur dé t égale moins R plus r fois i au carré")],
      pointage=[{"mot": "دابا نديرو la dérivée", "commande": "play_until", "parametres": {"moment": "derivee"}},
                {"mot": "la dérivée ديال un demi C u C au carré", "repere": "derivee"},
                {"mot": "la dérivée ديال un demi C u C au carré", "cible": "centre:0"},
                {"mot": "هاد la parenthèse égale moins R plus r fois i", "cible": "centre:1"},
                {"mot": "إذن dé E sur dé t égale moins R plus r fois i au carré", "commande": "play_until", "parametres": {"moment": "dE_dt"}},
                {"mot": "إذن dé E sur dé t égale moins R plus r fois i au carré", "cible": "centre:2"},
                {"mot": "i au carré ديما موجب", "repere": "dE_dt"}]),
    diapo_sim("ex_lc4_4", "Question 4 : l'énergie au départ", "À t = 0, i = 0 : E₀ = ½·C·E² = 7,2·10⁻⁵ J.",
      SIMD + "energie.html?vue=amortie", "Le premier sommet de u_C (t = 0) : toute l'énergie est dans le condensateur",
      "شوف le premier sommet، فt égale zéro. u C égale six volts، وle courant مازال ما بداش: i égale zéro. إذن la bobine ما فيها والو، وكلشي فle condensateur. E zéro égale un demi C E au carré. يعني un demi fois quatre fois dix puissance moins six، fois six au carré. E zéro égale sept virgule deux fois dix puissance moins cinq joule، يعني soixante-douze microjoules.",
      centre=[("t = 0 : i = 0 ⇒ E₀ = ½·C·E²", "E zéro égale un demi C E au carré"),
              ("E₀ = ½ × 4·10⁻⁶ × 6² = 7,2·10⁻⁵ J", "E zéro égale sept virgule deux fois dix puissance moins cinq joule")],
      pointage=[{"mot": "شوف le premier sommet", "commande": "play_until", "parametres": {"moment": "deux_sommets"}},
                {"mot": "u C égale six volts", "repere": "sommet_1"},
                {"mot": "E zéro égale un demi C E au carré", "cible": "centre:0"},
                {"mot": "E zéro égale sept virgule deux fois dix puissance moins cinq joule", "cible": "centre:1"}]),
    diapo_sim("ex_lc4_5", "Question 5 : l'énergie perdue entre deux sommets", "E_J = ½·C·(6² − 4²) = 4·10⁻⁵ J.",
      SIMD + "energie.html?vue=amortie", "Deux sommets de u_C : 6 V à t = 0, 4 V à t = T ≈ 4 ms",
      "شوف les deux sommets ديال u C: الأول فt égale zéro، six volts. التاني فt égale T، environ quatre millisecondes، quatre volts. فsommet، u C كتوقف وكترجع، إذن i égale zéro، وl'énergie كلها فle condensateur. l'énergie اللي ضاعت: E zéro moins E un، يعني un demi C، fois six au carré moins quatre au carré. six au carré moins quatre au carré، يعني trente-six moins seize، égale vingt. إذن un demi fois quatre fois dix puissance moins six fois vingt: quatre fois dix puissance moins cinq joule. رد البال: ماشي six moins quatre au carré.",
      centre=[("Sommets : i = 0 ⇒ E = ½·C·u_C²", "إذن i égale zéro"),
              ("E_J = ½·C·(6² − 4²) = ½ × 4·10⁻⁶ × 20", "يعني un demi C، fois six au carré moins quatre au carré"),
              ("E_J = 4·10⁻⁵ J", "quatre fois dix puissance moins cinq joule")],
      pointage=[{"mot": "شوف les deux sommets", "commande": "play_until", "parametres": {"moment": "deux_sommets"}},
                {"mot": "الأول فt égale zéro", "repere": "sommet_1"},
                {"mot": "التاني فt égale T", "repere": "sommet_2"},
                {"mot": "إذن i égale zéro", "cible": "centre:0"},
                {"mot": "يعني un demi C، fois six au carré moins quatre au carré", "cible": "centre:1"},
                {"mot": "quatre fois dix puissance moins cinq joule", "repere": "energie_perdue"},
                {"mot": "quatre fois dix puissance moins cinq joule", "cible": "centre:2"}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_lc4_1", "Plus facile : l'équation en q", "نتمرنو: اختار l'équation ديال le circuit RLC.",
      "Quelle est l'équation différentielle vérifiée par q dans le circuit RLC série (sans générateur) ?",
      ["L·d²q/dt² + (R + r)·dq/dt + q/C = 0", "L·d²q/dt² + R·dq/dt + q/C = 0", "L·d²q/dt² + (R + r)·dq/dt + C·q = 0"], 0, {
        "0": {"juste": rep("برافو! la résistance totale R plus r كاينة قدام dé q sur dé t، وq sur C هي u C.", "Juste : L·q'' + (R + r)·q' + q/C = 0.")},
        "1": {"1": rep("قريب. ولكن la bobine حتى هي عندها résistance r. فين مشات؟ عاود اختار.", "La bobine a aussi une résistance r : où est-elle ? Réessaie."),
              "2": rep("الجواب: R plus r fois dé q sur dé t. u b فيها r i، إذن r كتزاد على R.", "Réponse : (R + r)·dq/dt ; u_b contient r·i.")},
        "2": {"1": rep("u C égale q sur C، ماشي C fois q. عاود اختار.", "u_C = q/C, pas C·q. Réessaie."),
              "2": rep("الجواب: le dernier terme هو q sur C، حيت q égale C u C.", "Réponse : le terme est q/C, car q = C·u_C.")}},
      "Quelle est l'équation différentielle vérifiée par q dans le circuit R L C série ?"),
    vrai_faux_facile("fa_lc4_2", "Plus facile : vrai ou faux", "سؤال ساهل على l'amortissement.",
      "Circuit RLC série, R + r = 20 Ω.",
      [("Les sommets de u_C baissent : le régime est pseudo-périodique.", True, "Oscillations dont l'amplitude diminue : pseudo-périodique."),
       ("L'énergie perdue est transformée en chaleur dans R et r (effet Joule).", True, "C'est l'effet Joule qui amortit les oscillations."),
       ("La bobine idéale dissipe de l'énergie.", False, "L'inductance L ne dissipe pas d'énergie : elle la stocke (½·L·i²). Seules les résistances dissipent.")]),
    qcm_facile("fa_lc4_3", "Plus facile : le signe de dE/dt", "سؤال ساهل: le signe ديال dé E sur dé t.",
      "Dans le circuit RLC, dE/dt = …",
      ["−(R + r)·i²", "+(R + r)·i²", "0"], 0, {
        "0": {"juste": rep("برافو! dé E sur dé t égale moins R plus r fois i au carré، سالبة: l'énergie كتنقص.", "Juste : dE/dt = −(R + r)·i² ≤ 0.")},
        "1": {"1": rep("إلى كانت موجبة، l'énergie كتزيد. واش les sommets كيكبرو؟ عاود اختار.", "Positive, l'énergie augmenterait : les sommets monteraient. Réessaie."),
              "2": rep("الجواب: moins R plus r fois i au carré. l'énergie كتنقص بl'effet Joule.", "Réponse : −(R + r)·i² ; l'énergie diminue (effet Joule).")},
        "2": {"1": rep("zéro يعني l'énergie ثابتة: هادا le circuit LC بلا résistance. هنا كاينة R plus r. عاود اختار.", "dE/dt = 0 seulement sans résistance (LC idéal). Réessaie."),
              "2": rep("الجواب: moins R plus r fois i au carré، حيت كاينة résistance.", "Réponse : −(R + r)·i², car R + r ≠ 0.")}},
      "Dans le circuit R L C, dé E sur dé t égale ?"),
    qcm_facile("fa_lc4_4", "Plus facile : l'énergie au départ", "سؤال ساهل: l'énergie فt égale zéro.",
      "C = 4 µF chargé sous E = 6 V, i(0) = 0. L'énergie totale à t = 0 vaut…",
      ["1,2·10⁻⁵ J", "7,2·10⁻⁵ J", "1,44·10⁻⁴ J"], 1, {
        "1": {"juste": rep("برافو! un demi fois quatre fois dix puissance moins six fois trente-six، sept virgule deux fois dix puissance moins cinq joule.", "Juste : ½ × 4·10⁻⁶ × 6² = 7,2·10⁻⁵ J.")},
        "0": {"1": rep("نسيتي le carré ديال E. عاود اختار.", "Tu as oublié de mettre E au carré. Réessaie."),
              "2": rep("الجواب: sept virgule deux fois dix puissance moins cinq joule، E au carré.", "Réponse : E₀ = ½·C·E² = 7,2·10⁻⁵ J.")},
        "2": {"1": rep("نسيتي un demi. عاود اختار.", "Tu as oublié le facteur ½. Réessaie."),
              "2": rep("الجواب: un demi C E au carré، sept virgule deux fois dix puissance moins cinq joule.", "Réponse : E₀ = ½·C·E² = 7,2·10⁻⁵ J (avec le ½).")}},
      "C égale quatre microfarads chargé sous six volts. L'énergie totale à t égale zéro vaut ?"),
    qcm_facile("fa_lc4_5", "Plus facile : l'énergie perdue", "سؤال ساهل: l'énergie اللي ضاعت بين deux sommets.",
      "C = 4 µF ; sommets de u_C : 6 V puis 4 V. L'énergie dissipée entre ces deux sommets vaut…",
      ["8·10⁻⁶ J", "3,2·10⁻⁵ J", "4·10⁻⁵ J"], 2, {
        "2": {"juste": rep("برافو! un demi C، fois six au carré moins quatre au carré، يعني quatre fois dix puissance moins cinq joule.", "Juste : ½·C·(6² − 4²) = 4·10⁻⁵ J.")},
        "0": {"1": rep("حسبتي six moins quatre au carré. ولكن خاص الفرق بين deux énergies: كل وحدة فيها u C au carré. عاود اختار.", "Tu as calculé (6 − 4)² : il faut la différence des énergies, 6² − 4². Réessaie."),
              "2": rep("الجواب: un demi C fois trente-six moins seize، quatre fois dix puissance moins cinq joule. ماشي six moins quatre au carré.", "Réponse : ½·C·(6² − 4²) = 4·10⁻⁵ J, pas ½·C·(6 − 4)².")},
        "1": {"1": rep("هادي l'énergie اللي بقات فle deuxième sommet. السؤال على اللي ضاعت. عاود اختار.", "3,2·10⁻⁵ J est l'énergie qui reste au deuxième sommet, pas celle perdue. Réessaie."),
              "2": rep("الجواب: E zéro moins E un، sept virgule deux moins trois virgule deux، quatre fois dix puissance moins cinq joule.", "Réponse : E₀ − E₁ = 7,2·10⁻⁵ − 3,2·10⁻⁵ = 4·10⁻⁵ J.")}},
      "C égale quatre microfarads, sommets six volts puis quatre volts. L'énergie dissipée vaut ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même montage (figure 1) avec E = 8 V, C = 10 µF, L = 0,25 H, R = 16 Ω et r = 8 Ω. La figure 2 donne u_C(t) après la bascule ; t₁ est la date du deuxième sommet.",
      "intro_dit": "نفس التمرين، بقيم أخرى. E égale huit volts، C égale dix microfarads، L égale zéro virgule vingt-cinq henry، R égale seize ohms، وr égale huit ohms.",
      "figures": [FIGB],
      "donnees": ["E = 8 V", "C = 10 µF = 10⁻⁵ F", "L = 0,25 H", "R = 16 Ω ; r = 8 Ω"],
      "questions": [
        question_semblable("1", "Établir l'équation différentielle vérifiée par q(t) lorsque K est en position 2.",
          phrase(EQ), ["u_C + u_R + u_b = 0", "i = dq/dt"], ["u_b = L·di/dt"],
          corr([("1 : L·d²q/dt² + (R + r)·dq/dt + q/C = 0", "L dé deux q sur dé t deux، plus R plus r fois dé q sur dé t، plus q sur C، égale zéro")],
               "u C plus u R plus u b égale zéro، إذن L dé deux q sur dé t deux، plus R plus r fois dé q sur dé t، plus q sur C، égale zéro.")),
        question_semblable("2", "Nommer le régime, puis expliquer la diminution de l'amplitude.",
          phrase(REG), ["pseudo-périodique", "effet Joule"], ["périodique"],
          corr([("2 : pseudo-périodique ; énergie dissipée par effet Joule dans R + r.", "بl'effet Joule")],
               "le régime pseudo-périodique: l'énergie كتضيع chaleur بl'effet Joule فR plus r.")),
        question_semblable("3", "Montrer que dE/dt = −(R + r)·i², et conclure.",
          phrase(DEDT), ["dE/dt = i·(q/C + L·d²q/dt²)"], ["dE/dt = 0"],
          corr([("3 : dE/dt = i·(q/C + L·d²q/dt²) = −(R + r)·i² ≤ 0", "moins R plus r fois i au carré")],
               "dé E sur dé t égale i fois، q sur C plus L dé deux q sur dé t deux، يعني moins R plus r fois i au carré. l'énergie كتنقص.")),
        question_semblable("4", "Calculer l'énergie totale E₀ à t = 0.",
          valeur("E₀", 3.2e-4, "J", "E₀ = ½·C·E² = ½ × 10⁻⁵ × 8² = 3,2·10⁻⁴ J"), ["E₀ = ½·C·E²", "J"], ["E₀ = ½·C·E"],
          corr([("4 : E₀ = ½·C·E² = ½ × 10⁻⁵ × 64", "un demi C E au carré"), ("E₀ = 3,2·10⁻⁴ J", "trois virgule deux fois dix puissance moins quatre joule")],
               "E zéro égale un demi C E au carré، يعني un demi fois dix puissance moins cinq fois soixante-quatre. E zéro égale trois virgule deux fois dix puissance moins quatre joule.")),
        question_semblable("5", "Calculer l'énergie E_J dissipée par effet Joule entre t = 0 et t₁.",
          valeur("E_J", 1.95e-4, "J", "E_J = ½·C·(8² − 5²) = ½ × 10⁻⁵ × 39 = 1,95·10⁻⁴ J"), ["E_J = E₀ − E₁", "J"], ["½·C·(8 − 5)²"],
          corr([("5 : aux sommets i = 0 : E_J = ½·C·(8² − 5²)", "huit au carré moins cinq au carré"), ("E_J = 1,95·10⁻⁴ J", "un virgule quatre-vingt-quinze fois dix puissance moins quatre joule")],
               "فles sommets i égale zéro. E J égale un demi C، fois huit au carré moins cinq au carré، يعني un demi fois dix puissance moins cinq fois trente-neuf. E J égale un virgule quatre-vingt-quinze fois dix puissance moins quatre joule.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
