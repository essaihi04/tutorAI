# Exercice de physique, ch. 5 (noyaux, masse et énergie), niveau moyen n° 3 : la courbe d'Aston — lire E_ℓ/A,
# calculer E_ℓ et E_ℓ/A de l'uranium 235, comparer la stabilité (le piège E_ℓ), domaines de la fission et de la fusion.
# Écrit en Python pour un JSON sûr (outils communs : scripts/exercices/outils_ex.py).
#
# Sources comparées (lecture seule, rien de copié) :
#  - exploration energie_nucleaire.json : cas_types « comparer la stabilité » (4/20), « énergie de liaison (et par
#    nucléon) à partir des masses » (4/20) ; pièges « stabilité comparée avec E_ℓ » (Oualid, Noureddine), « N = A − Z » ;
#    convergence « courbe d'Aston en −E_ℓ/A, zones fusion / stables / fission » (7/10), bornes « environ 20 » et
#    « environ 190 » ; Ridouan : « lecture de E_ℓ(U) sur Aston par projection ».
#  - nationaux : 2017 R (E_ℓ/A du ⁶⁰Ni puis « lequel est le plus stable »), 2019 N (« le plus stable » par E_ℓ/A),
#    2020 R (E_ℓ de ²³⁴U), 2025 N (vrai/faux « la cohésion … d'autant plus forte que E_ℓ/A est petite ») : même type de
#    questions, chaînées ici avec une lecture de courbe (« lire puis déduire ») comme au national.
#  - séries en ligne (talamidi : « justifier la fission à partir de la courbe d'Aston » ; série SM Mahdade : « noyaux
#    susceptibles de subir une fission ») : extraits de recherche lus ; pages non joignables depuis cette session.
#  - cours : aston.html (mêmes points, même interpolation monotone, ⁵⁶Fe −8,79, ²³⁵U −7,59 ; vue comparer
#    noyau1/noyau2), balance.html?vue=noyau&noyau=uranium235 (236,90814 u ; 234,9935 u ; 1,91464 u ; 1783,5 MeV ; 7,59).
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from outils_ex import *

ID = "phys_ex_ch5_nucleaire_3"
SIMD = "/media/simulations/physics/energie-nucleaire-tableau/"
MP, MN, U = 1.00728, 1.00866, 931.5

# ---------------------------------------------------------------- la courbe d'Aston (mêmes données que aston.html)
NOY = [(2, 1.11), (3, 2.83), (4, 7.07), (6, 5.33), (7, 5.61), (9, 6.46), (12, 7.68), (14, 7.52), (16, 7.98), (20, 8.03),
       (40, 8.55), (56, 8.79), (60, 8.78), (90, 8.71), (94, 8.59), (120, 8.50), (140, 8.29), (165, 8.15), (208, 7.87),
       (235, 7.59), (238, 7.57)]
XS, YS = [a for a, _ in NOY], [e for _, e in NOY]


def _pentes():
    n = len(XS); d = [(YS[i + 1] - YS[i]) / (XS[i + 1] - XS[i]) for i in range(n - 1)]; m = [0.0] * n
    m[0], m[-1] = d[0], d[-1]
    for i in range(1, n - 1): m[i] = 0 if d[i - 1] * d[i] <= 0 else (d[i - 1] + d[i]) / 2
    for i in range(n - 1):
        if d[i] == 0: m[i] = m[i + 1] = 0; continue
        a, b = m[i] / d[i], m[i + 1] / d[i]; h = a * a + b * b
        if h > 9: t = 3 / h ** 0.5; m[i] = t * a * d[i]; m[i + 1] = t * b * d[i]
    return m
PENTES = _pentes()


def ea(A):
    """E_ℓ/A interpolée comme aston.html (Fritsch-Carlson : passe par chaque point, sans dépasser)."""
    if A <= XS[0]: return YS[0]
    if A >= XS[-1]: return YS[-1]
    i = 0
    while A > XS[i + 1]: i += 1
    h = XS[i + 1] - XS[i]; t = (A - XS[i]) / h; t2, t3 = t * t, t * t * t
    return (2 * t3 - 3 * t2 + 1) * YS[i] + (t3 - 2 * t2 + t) * h * PENTES[i] + (-2 * t3 + 3 * t2) * YS[i + 1] + (t3 - t2) * h * PENTES[i + 1]


def aston(titre, etiquettes, repere_A=None):
    """−E_ℓ/A en fonction de A ; etiquettes : [(A, texte, position)]."""
    abs_ = sorted(set([2 + k * 0.5 for k in range(37)] + list(range(21, 239))))
    els = [{"f": "ligne", "pts": [[round(a, 2), round(-ea(a), 4)] for a in abs_], "couleur": "cyan", "epais": True}]
    for A, e in NOY:
        els.append({"f": "point", "at": [A, -e], "couleur": "faible"})
    for A, t, pos in etiquettes:
        els.append({"f": "point", "at": [A, -dict(NOY)[A]], "t": t, "pos": pos, "couleur": "jaune"})
    if repere_A:
        els.append({"f": "repere", "x": repere_A, "y": -dict(NOY)[repere_A], "couleur": "faible"})
    return figure_courbe(titre, axe("A", 0, 240, None, [0, 20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240]),
                         axe("−E_{ℓ}/A", -9.5, 0, "MeV/nucléon", list(range(-9, 1))), els,
                         legende="Courbe d'Aston : −E_ℓ/A (MeV/nucléon) en fonction du nombre de nucléons A.", ratio=0.75)


# ---------------------------------------------------------------- calculs
EA_FE_LU = 8.8                                  # lecture sur la courbe (8,79 exactement)
assert abs(ea(56) - 8.79) < 1e-9
EL_FE = 56 * EA_FE_LU                           # 492,8 ≈ 493 MeV (492,2 avec 8,79)
assert round(EL_FE) == 493
SOM_U = 92 * MP + 143 * MN                      # 236,90814 u
DM_U = SOM_U - 234.9935                         # 1,91464 u
EL_U = DM_U * U                                 # 1783,5 MeV
EA_U = EL_U / 235                               # 7,59 MeV/nucléon
assert abs(SOM_U - 236.90814) < 1e-9 and abs(DM_U - 1.91464) < 1e-9 and round(EL_U, 1) == 1783.5 and round(EA_U, 2) == 7.59
# semblable : zirconium 90 lu, uranium 238
EL_ZR = 90 * 8.7                                # 783 MeV (lecture 8,7)
assert abs(ea(90) - 8.71) < 1e-9 and round(EL_ZR) == 783
DM_U8 = 92 * MP + 146 * MN - 238.00028          # 1,93384 u
EL_U8 = DM_U8 * U                               # 1801,4 MeV
EA_U8 = EL_U8 / 238                             # 7,57
assert abs(DM_U8 - 1.93384) < 1e-9 and round(EL_U8, 1) == 1801.4 and round(EA_U8, 2) == 7.57

ASTON = SIMD + "aston.html?vue=courbe"
BAL_U = SIMD + "balance.html?vue=noyau&noyau=uranium235"
COMP = SIMD + "aston.html?vue=comparer&noyau1=fe56&noyau2=u235"

EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "energie_nucleaire", "cours": "phys_ch5_energie_nucleaire",
  "titre": "La courbe d'Aston : stabilité du fer et de l'uranium", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Lire −E_ℓ/A sur la courbe d'Aston et en déduire E_ℓ", "Calculer E_ℓ et E_ℓ/A à partir des masses",
                  "Comparer la stabilité de deux noyaux par E_ℓ/A", "Situer les domaines de la fission et de la fusion"],
  "enonce": {
    "intro": "La figure représente la courbe d'Aston : l'opposé de l'énergie de liaison par nucléon, −E_ℓ/A, en fonction du nombre de nucléons A. On compare le fer ⁵⁶₂₆Fe, présent au cœur des étoiles massives, et l'uranium ²³⁵₉₂U, utilisé dans les centrales nucléaires.",
    "intro_dit": "دابا نقراو l'énoncé. la figure هي la courbe d'Aston: moins E l sur A، en fonction de A، عدد les nucléons. غادي نقارنو le fer cinquante-six، اللي كاين فقلب النجوم الكبار، و l'uranium deux cent trente-cinq، اللي كيستعملوه فles centrales nucléaires.",
    "figures": [aston("Figure : la courbe d'Aston", [(56, "⁵⁶Fe", "s"), (235, "²³⁵U", "s")], repere_A=56)],
    "donnees": ["m(²³⁵₉₂U) = 234,9935 u", "m_p = 1,00728 u ; m_n = 1,00866 u", "1 u = 931,5 MeV/c²"],
    "questions": [
      question("1", "Lire sur la courbe la valeur de E_ℓ/A du noyau ⁵⁶₂₆Fe, puis en déduire son énergie de liaison E_ℓ (en MeV).",
        "السؤال un: قرا على la courbe la valeur ديال E l sur A ديال le fer cinquante-six، ومن بعد استنتج l'énergie de liaison ديالو ب méga électron volt.",
        valeur("E_ℓ(Fe)", 493, "MeV", "−E_ℓ/A ≈ −8,8 MeV/nucléon ; E_ℓ = A·(E_ℓ/A) ≈ 56 × 8,8 = 493 MeV"),
        ["E_ℓ = A·(E_ℓ/A)", "A = 56", "MeV/nucléon", "MeV"], ["E_ℓ = −8,8 MeV", "E_ℓ = 8,8/56"],
        [aide("Repère le point du fer 56 sur la courbe, puis projette-le horizontalement sur l'axe vertical. Attention : l'axe porte −E_ℓ/A.",
              "قلب على la point ديال le fer cinquante-six فla courbe، وسير أفقي حتى l'axe العمودي. رد البال: l'axe فيه moins E l sur A."),
         aide("Si −E_ℓ/A = −8,8, alors E_ℓ/A = 8,8 MeV/nucléon ; puis E_ℓ = A × (E_ℓ/A).",
              "يلا moins E l sur A égale moins huit virgule huit، إذن E l sur A égale huit virgule huit. ومن بعد E l égale A fois E l sur A.")],
        corr([("1 : on lit −E_ℓ/A ≈ −8,8 MeV/nucléon, donc E_ℓ/A ≈ 8,8 MeV/nucléon", "E l sur A égale environ huit virgule huit"),
              ("E_ℓ = A·(E_ℓ/A) = 56 × 8,8", "E l égale A fois E l sur A"),
              ("E_ℓ ≈ 493 MeV", "environ quatre cent quatre-vingt-treize méga électron volt")],
             "السؤال un. على la courbe، moins E l sur A ديال le fer égale environ moins huit virgule huit. إذن E l sur A égale environ huit virgule huit méga électron volt par nucléon. E l égale A fois E l sur A، يعني cinquante-six fois huit virgule huit، كتعطي environ quatre cent quatre-vingt-treize méga électron volt."),
        "ex_n3_1", "fa_n3_1"),
      question("2", "Calculer le défaut de masse Δm du noyau ²³⁵₉₂U, puis son énergie de liaison E_ℓ en MeV.",
        "السؤال deux: حسب le défaut de masse ديال النواة ديال l'uranium deux cent trente-cinq، ومن بعد l'énergie de liaison ديالها ب méga électron volt.",
        valeur("E_ℓ(U)", 1783.5, "MeV", "Δm = 92 × 1,00728 + 143 × 1,00866 − 234,9935 = 1,91464 u ; E_ℓ = Δm·c² = 1,91464 × 931,5 = 1783,5 MeV"),
        ["Δm = Z·m_p + (A − Z)·m_n − m", "N = A − Z = 143", "E_ℓ = Δm·c²", "931,5"], ["N = 235", "E_ℓ = Δm × 9·10¹⁶"],
        [aide("Compte d'abord les nucléons : Z = 92 protons et N = A − Z neutrons.",
              "حسب اللول les nucléons: Z égale quatre-vingt-douze protons، و N égale A moins Z neutrons."),
         aide("Δm = Z·m_p + (A − Z)·m_n − m(U), puis E_ℓ = Δm (en u) × 931,5 MeV.",
              "delta m égale Z m p plus A moins Z m n moins m de l'uranium. ومن بعد E l égale delta m ب u fois neuf cent trente et un virgule cinq.")],
        corr([("2 : Z = 92 ; N = A − Z = 235 − 92 = 143", "N égale A moins Z égale cent quarante-trois"),
              ("Δm = 92 × 1,00728 + 143 × 1,00866 − 234,9935 = 236,90814 − 234,9935 = 1,91464 u", "delta m égale un virgule quatre-vingt-onze mille quatre cent soixante-quatre u"),
              ("E_ℓ = Δm·c² = 1,91464 × 931,5", "E l égale delta m fois c au carré"),
              ("E_ℓ = 1783,5 MeV", "mille sept cent quatre-vingt-trois virgule cinq méga électron volt")],
             "السؤال deux. Z égale quatre-vingt-douze، و N égale A moins Z égale cent quarante-trois. delta m égale quatre-vingt-douze fois un virgule zéro zéro sept cent vingt-huit، plus cent quarante-trois fois un virgule zéro zéro huit cent soixante-six، moins deux cent trente-quatre virgule neuf mille neuf cent trente-cinq. يعني delta m égale un virgule quatre-vingt-onze mille quatre cent soixante-quatre u. ومن بعد E l égale delta m fois c au carré، يعني un virgule quatre-vingt-onze mille quatre cent soixante-quatre fois neuf cent trente et un virgule cinq: E l égale mille sept cent quatre-vingt-trois virgule cinq méga électron volt."),
        "ex_n3_2", "fa_n3_2"),
      question("3", "En déduire l'énergie de liaison par nucléon de ²³⁵₉₂U et vérifier que le résultat est en accord avec la courbe.",
        "السؤال trois: استنتج l'énergie de liaison par nucléon ديال l'uranium deux cent trente-cinq، وتأكد بلي النتيجة متفقة مع la courbe.",
        valeur("E_ℓ/A(U)", 7.59, "MeV/nucléon", "E_ℓ/A = 1783,5/235 = 7,59 MeV/nucléon"),
        ["E_ℓ/A", "A = 235", "MeV/nucléon"], ["E_ℓ/Z = 1783,5/92", "E_ℓ/N"],
        [aide("Divise l'énergie de liaison trouvée à la question 2 par le nombre de nucléons.",
              "قسم l'énergie de liaison ديال السؤال deux على عدد les nucléons."),
         aide("E_ℓ/A = E_ℓ/235. Sur la courbe, le point de ²³⁵U doit être à −E_ℓ/A ≈ −7,6.",
              "E l sur A égale E l sur deux cent trente-cinq. وعلى la courbe، la point ديال l'uranium خاصها تكون environ à moins sept virgule six.")],
        corr([("3 : E_ℓ/A = 1783,5/235", "E l sur A égale mille sept cent quatre-vingt-trois virgule cinq sur deux cent trente-cinq"),
              ("E_ℓ/A = 7,59 MeV/nucléon", "sept virgule cinquante-neuf méga électron volt par nucléon"),
              ("Sur la courbe, le point de ²³⁵U est à −E_ℓ/A ≈ −7,6 : accord.", "على la courbe، la point ديال l'uranium")],
             "السؤال trois. E l sur A égale mille sept cent quatre-vingt-trois virgule cinq sur deux cent trente-cinq، يعني sept virgule cinquante-neuf méga électron volt par nucléon. على la courbe، la point ديال l'uranium كاينة environ à moins sept virgule six: متفقين."),
        "ex_n3_3", "fa_n3_3"),
      question("4", "Un élève affirme : « l'uranium 235 est plus stable que le fer 56, car son énergie de liaison est plus grande ». Justifier que cette affirmation est fausse.",
        "السؤال quatre: تلميذ قال: l'uranium plus stable من le fer، حيت l'énergie de liaison ديالو كبر. برهن بلي هاد الكلام غالط.",
        phrase("Faux : la stabilité se compare avec l'énergie de liaison par nucléon, pas avec E_ℓ. E_ℓ(U) = 1783,5 MeV > E_ℓ(Fe) ≈ 493 MeV seulement parce que U a beaucoup plus de nucléons. Or E_ℓ/A(Fe) ≈ 8,8 MeV/nucléon > E_ℓ/A(U) = 7,59 MeV/nucléon : le fer 56 est plus stable que l'uranium 235 (sur la courbe, son point est plus bas)."),
        ["E_ℓ/A", "plus stable", "8,8 > 7,59"], ["comparer E_ℓ", "E_ℓ(U) > E_ℓ(Fe)"],
        [aide("Quelle grandeur mesure la stabilité d'un noyau : E_ℓ ou E_ℓ/A ? Pourquoi E_ℓ de l'uranium est-elle si grande ?",
              "شنو هي la grandeur اللي كتقيس la stabilité: E l ولا E l sur A؟ وعلاش E l ديال l'uranium كبيرة بزاف؟"),
         aide("Compare E_ℓ/A(Fe) ≈ 8,8 et E_ℓ/A(U) = 7,59 : le plus stable a la plus grande E_ℓ/A (le point le plus bas de la courbe).",
              "قارن E l sur A ديال le fer، environ huit virgule huit، مع E l sur A ديال l'uranium، sept virgule cinquante-neuf. le plus stable عندو E l sur A الكبيرة، يعني la point اللي لتحت فla courbe.")],
        corr([("4 : la stabilité se compare avec E_ℓ/A, pas avec E_ℓ", "la stabilité كنقارنوها ب E l sur A"),
              ("E_ℓ(U) est grande car U a 235 nucléons (le fer : 56)", "حيت عندو A égale deux cent trente-cinq nucléons"),
              ("E_ℓ/A(Fe) ≈ 8,8 MeV/nucléon > E_ℓ/A(U) = 7,59 MeV/nucléon", "huit virgule huit plus grand que sept virgule cinquante-neuf"),
              ("Donc le fer 56 est plus stable : l'affirmation est fausse.", "إذن le fer هو اللي plus stable")],
             "السؤال quatre. la stabilité كنقارنوها ب E l sur A، ماشي ب E l. E l ديال l'uranium كبيرة غير حيت عندو A égale deux cent trente-cinq nucléons، و le fer عندو A égale cinquante-six. و E l sur A ديال le fer، environ huit virgule huit، huit virgule huit plus grand que sept virgule cinquante-neuf ديال l'uranium. إذن le fer هو اللي plus stable، والتلميذ غالط."),
        "ex_n3_4", "fa_n3_4"),
      question("5", "À l'aide de la courbe, préciser les noyaux qui peuvent libérer de l'énergie par fission et ceux qui peuvent en libérer par fusion. Justifier.",
        "السؤال cinq: بالاستعانة ب la courbe، حدد les noyaux اللي يقدرو يعطيو l'énergie ب la fission، و اللي يقدرو يعطيوها ب la fusion. علل.",
        phrase("Les noyaux lourds (A > 190 environ, comme ²³⁵U) peuvent subir une fission : ils se scindent en deux noyaux moyens, plus bas sur la courbe (E_ℓ/A plus grande), donc plus stables, et de l'énergie est libérée. Les noyaux légers (A < 20 environ, comme ²H et ³H) peuvent subir une fusion : ils s'unissent en un noyau plus lourd, plus bas sur la courbe, donc plus stable, avec libération d'énergie. Les noyaux du creux (20 < A < 190, autour du fer) sont les plus stables."),
        ["A > 190", "A < 20", "fission", "fusion", "plus stable"], ["fission des noyaux légers", "fusion des noyaux lourds"],
        [aide("Les deux réactions conduisent à des noyaux plus stables. Où sont les noyaux les plus stables sur la courbe ?",
              "les deux réactions كيعطيو noyaux plus stables. فين كاينين les noyaux اللي plus stables فla courbe؟"),
         aide("Un noyau lourd (à droite, A > 190 environ) descend vers le creux en se cassant ; des noyaux légers (à gauche, A < 20 environ) y descendent en s'unissant.",
              "noyau lourd، على اليمين، A plus grand que cent quatre-vingt-dix environ، كيهبط للتحت ملي كيتقسم. و les noyaux légers، على اليسار، A inférieur à vingt environ، كيهبطو ملي كيلصقو.")],
        corr([("5 : fission : noyaux lourds, A > 190 environ (ex. ²³⁵U) ; ils donnent deux noyaux moyens plus stables", "la fission: les noyaux lourds"),
              ("fusion : noyaux légers, A < 20 environ (ex. ²H, ³H) ; ils donnent un noyau plus lourd plus stable", "la fusion: les noyaux légers"),
              ("Dans les deux cas, E_ℓ/A augmente (on descend vers le creux du fer) et de l'énergie est libérée.", "فالحالتين كنهبطو نحو le fer")],
             "السؤال cinq. la fission: les noyaux lourds، A plus grand que cent quatre-vingt-dix environ، بحال l'uranium. كيتقسمو لجوج noyaux moyens plus stables. la fusion: les noyaux légers، A inférieur à vingt environ، بحال le deutérium و le tritium. كيلصقو ويعطيو noyau plus lourd و plus stable. فالحالتين كنهبطو نحو le fer: E l sur A كتكبر، وكتخرج l'énergie."),
        "ex_n3_5", "fa_n3_5"),
    ]
  },
  "explication": deck("explication", "Explication animée", [
    diapo_sim("ex_n3_1", "Question 1 : lire le fer sur la courbe", "−E_ℓ/A(Fe) ≈ −8,8 ; E_ℓ = 56 × 8,8 ≈ 493 MeV",
      ASTON, "La courbe d'Aston : le creux est le fer 56",
      "شوف les axes: فالأفقي A، وفالعمودي moins E l sur A. رد البال للإشارة moins: كلما هبطنا، E l sur A كتكبر. هادي هي la courbe. التحت ديالها هو le fer cinquante-six: moins huit virgule soixante-dix-neuf، يعني environ moins huit virgule huit. إذن E l sur A égale huit virgule huit méga électron volt par nucléon. و E l égale A fois E l sur A: cinquante-six fois huit virgule huit، environ quatre cent quatre-vingt-treize méga électron volt.",
      centre=[("E_ℓ/A(Fe) ≈ 8,8 MeV/nucléon", "إذن E l sur A égale huit virgule huit"),
              ("E_ℓ = A·(E_ℓ/A) = 56 × 8,8 ≈ 493 MeV", "و E l égale A fois E l sur A")],
      pointage=[{"mot": "شوف les axes", "commande": "play_until", "parametres": {"moment": "axes"}},
                {"mot": "فالعمودي moins E l sur A", "repere": "axe_y"},
                {"mot": "هادي هي la courbe", "commande": "play_until", "parametres": {"moment": "courbe_tracee"}},
                {"mot": "التحت ديالها هو le fer", "commande": "play_until", "parametres": {"moment": "fer"}},
                {"mot": "moins huit virgule soixante-dix-neuf", "repere": "fer"}]),
    diapo_sim("ex_n3_2", "Question 2 : E_ℓ de l'uranium 235", "Δm = 236,90814 − 234,9935 = 1,91464 u ; E_ℓ = 1,91464 × 931,5 = 1783,5 MeV",
      BAL_U, "La balance : 92 protons et 143 neutrons séparés, contre le noyau ²³⁵U",
      "شوف الميزان. على اليسار les nucléons ديال l'uranium بعاد: quatre-vingt-douze protons، و A moins Z égale cent quarante-trois neutrons. la masse ديالهم: deux cent trente-six virgule quatre-vingt-dix mille huit cent quatorze u. على اليمين النواة: deux cent trente-quatre virgule neuf mille neuf cent trente-cinq u. الميزان كيهبط من جيهة les nucléons. delta m égale un virgule quatre-vingt-onze mille quatre cent soixante-quatre u. ومن بعد E l égale delta m fois neuf cent trente et un virgule cinq، يعني mille sept cent quatre-vingt-trois virgule cinq méga électron volt.",
      centre=[("N = A − Z = 235 − 92 = 143", "A moins Z égale cent quarante-trois"),
              ("Δm = 236,90814 − 234,9935 = 1,91464 u", "delta m égale un virgule quatre-vingt-onze"),
              ("E_ℓ = 1,91464 × 931,5 = 1783,5 MeV", "ومن بعد E l égale delta m fois neuf cent")],
      pointage=[{"mot": "على اليسار les nucléons", "commande": "play_until", "parametres": {"moment": "nucleons_poses"}},
                {"mot": "على اليمين النواة", "commande": "play_until", "parametres": {"moment": "noyau_pose"}},
                {"mot": "الميزان كيهبط", "commande": "play_until", "parametres": {"moment": "balance_penche"}},
                {"mot": "delta m égale un virgule", "commande": "play_until", "parametres": {"moment": "delta_m"}},
                {"mot": "ومن بعد E l égale", "commande": "play_until", "parametres": {"moment": "energie"}}]),
    diapo_sim("ex_n3_3", "Question 3 : E_ℓ/A de l'uranium 235", "E_ℓ/A = 1783,5/235 = 7,59 MeV/nucléon",
      BAL_U, "On divise E_ℓ par A = 235",
      "شوف la colonne: E l égale mille sept cent quatre-vingt-trois virgule cinq méga électron volt. كنقسمو على A، عدد les nucléons، يعني sur deux cent trente-cinq: sept virgule cinquante-neuf méga électron volt par nucléon. ماشي على Z. وعلى la courbe d'Aston، l'uranium كاين بالضبط à moins sept virgule cinquante-neuf: النتيجة متفقة.",
      centre=[("E_ℓ/A = 1783,5 / 235 = 7,59 MeV/nucléon", "sur deux cent trente-cinq: sept virgule cinquante-neuf")],
      pointage=[{"mot": "شوف la colonne", "commande": "play_until", "parametres": {"moment": "energie"}},
                {"mot": "كنقسمو على A", "commande": "play_until", "parametres": {"moment": "par_nucleon"}},
                {"mot": "sept virgule cinquante-neuf méga électron volt par nucléon", "repere": "par_nucleon"}]),
    diapo_sim("ex_n3_4", "Question 4 : le piège de E_ℓ", "E_ℓ/A(Fe) = 8,79 > E_ℓ/A(U) = 7,59 : le fer est plus stable",
      COMP, "Deux points de lecture : le fer 56 et l'uranium 235",
      "هادا فخ معروف. l'uranium عندو E l كبيرة: mille sept cent quatre-vingt-trois. ولكن عندو A égale deux cent trente-cinq nucléons. la stabilité كنقارنوها ب E l sur A. شوف la point الأولى: le fer، moins huit virgule soixante-dix-neuf. la point الثانية: l'uranium، moins sept virgule cinquante-neuf. le fer لتحت: E l sur A ديالو كبر، إذن هو اللي plus stable.",
      centre=[("Stabilité : on compare E_ℓ/A, jamais E_ℓ", "la stabilité كنقارنوها ب E l sur A"),
              ("8,79 > 7,59 : ⁵⁶Fe plus stable que ²³⁵U", "إذن هو اللي plus stable")],
      pointage=[{"mot": "هادا فخ معروف", "commande": "play_until", "parametres": {"moment": "courbe_tracee"}},
                {"mot": "شوف la point الأولى", "commande": "play_until", "parametres": {"moment": "noyau1"}},
                {"mot": "la point الثانية", "commande": "play_until", "parametres": {"moment": "noyau2"}},
                {"mot": "le fer لتحت", "commande": "play_until", "parametres": {"moment": "comparaison"}}]),
    diapo_sim("ex_n3_5", "Question 5 : fission et fusion sur la courbe", "Légers (A < 20) : fusion ; lourds (A > 190) : fission ; on descend vers le fer",
      SIMD + "aston.html?vue=courbe&depart=plus_stable", "Les trois zones de la courbe d'Aston",
      "شوف الطرف ديال اليسار: les noyaux légers، A inférieur à vingt environ. باش يهبطو، كيلصقو: هادي la fusion. دابا الطرف ديال اليمين: les noyaux lourds، A plus grand que cent quatre-vingt-dix environ. باش يهبط، le noyau كيتقسم: هادي la fission. فالوسط، les noyaux اللي plus stables، بحال le fer. فالحالتين كنهبطو: E l sur A كتكبر، وكتخرج l'énergie.",
      centre=[("A < 20 environ : fusion", "هادي la fusion"), ("A > 190 environ : fission", "هادي la fission")],
      pointage=[{"mot": "شوف الطرف ديال اليسار", "commande": "play_until", "parametres": {"moment": "zone_fusion"}},
                {"mot": "دابا الطرف ديال اليمين", "commande": "play_until", "parametres": {"moment": "zone_fission"}},
                {"mot": "فالوسط، les noyaux", "commande": "play_until", "parametres": {"moment": "zone_stable"}},
                {"mot": "فالحالتين كنهبطو", "commande": "play_until", "parametres": {"moment": "fleches"}}]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm_facile("fa_n3_1", "Plus facile : lire la courbe", "نتمرنو بسؤال ساهل على la courbe d'Aston.",
      "Sur la courbe, un point est à −E_ℓ/A = −8,0 pour A = 20. Son énergie de liaison vaut :",
      ["−160 MeV", "160 MeV", "0,4 MeV"], 1, {
        "1": {"juste": rep("برافو! E l sur A égale huit، و E l égale vingt fois huit، يعني cent soixante méga électron volt.", "Juste : E_ℓ = 20 × 8,0 = 160 MeV.")},
        "0": {"1": rep("ما تقلقش. l'axe فيه moins E l sur A. واش l'énergie de liaison كتكون négative؟ عاود اختار.", "L'axe porte −E_ℓ/A : E_ℓ, elle, est positive. Réessaie."),
              "2": rep("الجواب هو E l égale cent soixante méga électron volt. l'énergie de liaison ديما positive، الإشارة moins راها غير فl'axe.", "Réponse : 160 MeV ; E_ℓ est toujours positive.")},
        "2": {"1": rep("قريب، ولكن قسمتي. E l égale A fois E l sur A: واش نقسمو ولا نضربو؟ عاود اختار.", "E_ℓ = A × (E_ℓ/A) : il faut multiplier. Réessaie."),
              "2": rep("الجواب هو E l égale vingt fois huit، يعني cent soixante méga électron volt.", "Réponse : E_ℓ = 20 × 8,0 = 160 MeV.")}},
      "Sur la courbe, un point est à moins E l sur A égale moins huit pour A égale vingt. Son énergie de liaison vaut combien ?"),
    qcm_facile("fa_n3_2", "Plus facile : les neutrons de l'uranium", "سؤال ساهل: شحال من neutron فl'uranium deux cent trente-cinq؟",
      "Combien de neutrons contient le noyau ²³⁵₉₂U ?",
      ["235", "92", "143"], 2, {
        "2": {"juste": rep("برافو! N égale A moins Z، يعني deux cent trente-cinq moins quatre-vingt-douze، يعني cent quarante-trois.", "Juste : N = 235 − 92 = 143.")},
        "0": {"1": rep("ما تقلقش. deux cent trente-cinq هو A، عدد les nucléons كاملين. واش كلهم neutrons؟ عاود اختار.", "235 = A, tous les nucléons. Sont-ils tous des neutrons ? Réessaie."),
              "2": rep("الجواب هو N égale cent quarante-trois. N égale A moins Z.", "Réponse : N = A − Z = 143.")},
        "1": {"1": rep("لا، quatre-vingt-douze هو Z، عدد les protons. عاود اختار.", "92 = Z, le nombre de protons. Réessaie."),
              "2": rep("الجواب هو N égale cent quarante-trois، يعني A moins Z.", "Réponse : N = A − Z = 143.")}},
      "Combien de neutrons contient le noyau d'uranium deux cent trente-cinq, Z égale quatre-vingt-douze ?"),
    qcm_facile("fa_n3_3", "Plus facile : diviser par quoi ?", "سؤال ساهل: على شنو كنقسمو E l؟",
      "E_ℓ(²³⁵U) = 1783,5 MeV. Pour obtenir l'énergie de liaison par nucléon, on divise par :",
      ["92", "235", "143"], 1, {
        "1": {"juste": rep("برافو! كنقسمو على A égale deux cent trente-cinq، عدد les nucléons.", "Juste : on divise par A = 235.")},
        "0": {"1": rep("ما تقلقش. quatre-vingt-douze هو عدد les protons. واش les protons بوحدهم هوما les nucléons؟ عاود اختار.", "92 protons seulement : et les neutrons ? Réessaie."),
              "2": rep("الجواب هو A égale deux cent trente-cinq: protons et neutrons.", "Réponse : par A = 235 (protons + neutrons).")},
        "2": {"1": rep("لا، cent quarante-trois هو عدد les neutrons بوحدهم. عاود اختار.", "143 : les neutrons seulement. Réessaie."),
              "2": rep("الجواب هو A égale deux cent trente-cinq، جميع les nucléons.", "Réponse : par A = 235, tous les nucléons.")}},
      "E l de l'uranium deux cent trente-cinq égale mille sept cent quatre-vingt-trois virgule cinq méga électron volt. On divise par quoi pour avoir E l sur A ?"),
    vrai_faux_facile("fa_n3_4", "Plus facile : vrai ou faux", "سؤال ساهل على la stabilité.",
      "E_ℓ(U) = 1783,5 MeV ; E_ℓ(Fe) ≈ 493 MeV ; E_ℓ/A(U) = 7,59 ; E_ℓ/A(Fe) ≈ 8,8 MeV/nucléon.",
      [("Le noyau le plus stable est celui qui a la plus grande énergie de liaison E_ℓ.", False, "On compare E_ℓ/A, pas E_ℓ : un gros noyau a une grande E_ℓ parce qu'il a beaucoup de nucléons."),
       ("Le fer 56 est plus stable que l'uranium 235.", True, "8,8 > 7,59 MeV/nucléon."),
       ("Sur la courbe d'Aston, le noyau le plus stable est le point le plus bas.", True, "L'axe porte −E_ℓ/A : plus bas = E_ℓ/A plus grande.")]),
    association_facile("fa_n3_5", "Plus facile : les zones de la courbe", "سؤال ساهل: ربط كل منطقة ديال la courbe بالشي اللي كيوقع فيها.",
      "Relie chaque zone de la courbe d'Aston à ce qui s'y passe.", "Associer chaque zone à son comportement.",
      [("1", "noyaux légers (A < 20 environ)"), ("2", "noyaux moyens (20 < A < 190, autour du fer)"), ("3", "noyaux lourds (A > 190 environ)")],
      [("a", "peuvent libérer de l'énergie par fission"), ("b", "sont les plus stables"), ("c", "peuvent libérer de l'énergie par fusion")],
      {"1": "c", "2": "b", "3": "a"},
      {"1-c": (True, "Oui : deux noyaux légers s'unissent et descendent vers le creux.", "صحيح. deux noyaux légers كيلصقو وكيهبطو نحو التحت."),
       "1-a": (False, "Un noyau léger qui se casse donnerait des noyaux encore plus légers, plus haut sur la courbe. Que doivent faire les noyaux légers ?", "noyau léger يلا تقسم، كيطلع الفوق فla courbe. شنو خاص les noyaux légers يديرو؟"),
       "1-b": (False, "Les noyaux légers sont en haut à gauche : ils ne sont pas les plus stables.", "les noyaux légers الفوق على اليسار: ماشي هوما اللي plus stables."),
       "2-b": (True, "Oui : le creux de la courbe, autour du fer 56, ce sont les noyaux les plus stables.", "صحيح. التحت ديال la courbe، حدا le fer، هوما les noyaux اللي plus stables."),
       "2-a": (False, "Les noyaux moyens sont déjà au creux : en se cassant, ils remonteraient. Cherche ce qui les caractérise.", "les noyaux moyens راهم ديجا لتحت. قلب على الصفة ديالهم."),
       "2-c": (False, "Les noyaux moyens sont déjà au creux : en s'unissant, ils remonteraient vers la droite.", "les noyaux moyens راهم لتحت. يلا لصقو كيطلعو."),
       "3-a": (True, "Oui : un noyau lourd se scinde en deux noyaux moyens, plus stables.", "صحيح. noyau lourd كيتقسم لجوج noyaux moyens plus stables."),
       "3-b": (False, "Les noyaux lourds sont un peu plus haut que le fer : ils ne sont pas les plus stables.", "les noyaux lourds الفوق شوية على le fer: ماشي هوما اللي plus stables."),
       "3-c": (False, "Un noyau lourd qui s'unirait à un autre deviendrait encore plus lourd, plus haut sur la courbe.", "noyau lourd يلا لصق مع آخر، كيولي أثقل وكيطلع الفوق.")},
      "(1 ; c) (2 ; b) (3 ; a) : légers → fusion ; moyens → les plus stables ; lourds → fission.",
      "الأزواج: un avec c، deux avec b، trois avec a. les noyaux légers: la fusion. les noyaux moyens: plus stables. les noyaux lourds: la fission."),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres noyaux : le zirconium 90 et l'uranium 238",
    "enonce": {
      "intro": "Même courbe d'Aston. On compare le zirconium ⁹⁰₄₀Zr et l'uranium ²³⁸₉₂U.",
      "intro_dit": "نفس la courbe d'Aston. غادي نقارنو le zirconium quatre-vingt-dix و l'uranium deux cent trente-huit.",
      "figures": [aston("Figure : la courbe d'Aston", [(90, "⁹⁰Zr", "s"), (238, "²³⁸U", "s")], repere_A=90)],
      "donnees": ["m(²³⁸₉₂U) = 238,00028 u", "m_p = 1,00728 u ; m_n = 1,00866 u", "1 u = 931,5 MeV/c²"],
      "questions": [
        question_semblable("1", "Lire sur la courbe E_ℓ/A du noyau ⁹⁰₄₀Zr, puis en déduire son énergie de liaison E_ℓ (en MeV).",
          valeur("E_ℓ(Zr)", 783, "MeV", "E_ℓ/A ≈ 8,7 MeV/nucléon ; E_ℓ = 90 × 8,7 = 783 MeV"), ["E_ℓ = A·(E_ℓ/A)", "MeV"], ["E_ℓ = −8,7 MeV"],
          corr([("1 : on lit −E_ℓ/A ≈ −8,7, donc E_ℓ/A ≈ 8,7 MeV/nucléon", "égale environ huit virgule sept"), ("E_ℓ = 90 × 8,7 ≈ 783 MeV", "sept cent quatre-vingt-trois")],
               "على la courbe، E l sur A ديال le zirconium égale environ huit virgule sept. E l égale quatre-vingt-dix fois huit virgule sept، يعني environ sept cent quatre-vingt-trois méga électron volt.")),
        question_semblable("2", "Calculer le défaut de masse Δm du noyau ²³⁸₉₂U, puis son énergie de liaison E_ℓ en MeV.",
          valeur("E_ℓ(U)", 1801.4, "MeV", "Δm = 92 × 1,00728 + 146 × 1,00866 − 238,00028 = 1,93384 u ; E_ℓ = 1,93384 × 931,5 = 1801,4 MeV"),
          ["N = A − Z = 146", "E_ℓ = Δm·c²"], ["N = 238"],
          corr([("2 : N = 238 − 92 = 146 ; Δm = 92 × 1,00728 + 146 × 1,00866 − 238,00028 = 1,93384 u", "delta m égale un virgule quatre-vingt-treize mille trois cent quatre-vingt-quatre u"),
                ("E_ℓ = 1,93384 × 931,5 = 1801,4 MeV", "mille huit cent un virgule quatre")],
               "N égale cent quarante-six. delta m égale un virgule quatre-vingt-treize mille trois cent quatre-vingt-quatre u. E l égale delta m fois neuf cent trente et un virgule cinq، يعني mille huit cent un virgule quatre méga électron volt.")),
        question_semblable("3", "En déduire l'énergie de liaison par nucléon de ²³⁸₉₂U et vérifier l'accord avec la courbe.",
          valeur("E_ℓ/A(U)", 7.57, "MeV/nucléon", "E_ℓ/A = 1801,4/238 = 7,57 MeV/nucléon"), ["E_ℓ/A", "A = 238"], ["E_ℓ/Z"],
          corr([("3 : E_ℓ/A = 1801,4/238 = 7,57 MeV/nucléon ; accord avec la courbe (≈ −7,6)", "sept virgule cinquante-sept")],
               "E l sur A égale mille huit cent un virgule quatre sur deux cent trente-huit، يعني sept virgule cinquante-sept méga électron volt par nucléon، متفقة مع la courbe.")),
        question_semblable("4", "« L'uranium 238 est plus stable que le zirconium 90, car son énergie de liaison est plus grande. » Justifier que cette affirmation est fausse.",
          phrase("Faux : on compare E_ℓ/A, pas E_ℓ. E_ℓ/A(Zr) ≈ 8,7 MeV/nucléon > E_ℓ/A(U) = 7,57 MeV/nucléon : le zirconium 90 est plus stable ; E_ℓ(U) est grande seulement parce que U a 238 nucléons."),
          ["E_ℓ/A", "plus stable"], ["comparer E_ℓ"],
          corr([("4 : on compare E_ℓ/A : 8,7 > 7,57, donc ⁹⁰Zr est plus stable que ²³⁸U ; l'affirmation est fausse.", "le zirconium هو اللي plus stable")],
               "كنقارنو E l sur A: huit virgule sept plus grand que sept virgule cinquante-sept، إذن le zirconium هو اللي plus stable.")),
        question_semblable("5", "À l'aide de la courbe, préciser les noyaux qui peuvent libérer de l'énergie par fission et ceux qui peuvent en libérer par fusion. Justifier.",
          phrase("Fission : noyaux lourds (A > 190 environ, comme ²³⁸U) qui se scindent en noyaux moyens plus stables ; fusion : noyaux légers (A < 20 environ) qui s'unissent en un noyau plus stable ; dans les deux cas E_ℓ/A augmente et de l'énergie est libérée."),
          ["A > 190", "A < 20"], ["fusion des noyaux lourds"],
          corr([("5 : fission des noyaux lourds (A > 190), fusion des noyaux légers (A < 20) : on descend vers le creux, E_ℓ/A augmente, énergie libérée.", "la fission ديال les noyaux lourds")],
               "la fission ديال les noyaux lourds، و la fusion ديال les noyaux légers. فالحالتين E l sur A كتكبر وكتخرج l'énergie.")),
      ]}}
}

if __name__ == "__main__":
    ecrire(EX)
