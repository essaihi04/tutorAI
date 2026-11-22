# Exercice de chimie, ch. 13 (réactions acido-basiques), niveau moyen (celui du national) : une base faible dans
# l'eau (la diméthylamine) — équation, [HO⁻] par Ke, « montrer que » τ = 10^(pH − pKe)/C, Qr,éq = C·τ²/(1 − τ),
# puis Ka = Ke/Qr,éq et pKa.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2020 N (2.1 à 2.5 : ammoniac, [HO⁻], τ, Qr,éq, pKa), 2022 R (1.2 à 1.5 :
#    méthylamine, τ, « montrer que » Qr,éq, Ka), 2020 R (1.1 à 1.5 : ion éthanoate dans l'eau), 2024 R (1.1 base
#    R−NH₂) — backend/data/exams/physique ;
#  - profs (architecture/phys_ch13_acides_bases.md § 1 : Naceiri Mrabti, Prof Bazhar « Ka : acide + eau, puis base +
#    eau ») ; pièges relevés : τ d'une base calculé avec 10^(−pH) au lieu de [HO⁻], Qr,éq pris pour Ka (Ka = Ke/Qr,éq) ;
#    hors cadre (cadre_reference : Kb, pKb, pOH) : jamais utilisés ici ;
#  - séries en ligne repérées (titres et résumés lus ; PDF non ouverts, hôtes hors du réseau de la session) :
#    talamidi exercices non corrigés 2 et 5, moutamadris fiches 13-7, 13-8 et 17-2, pc1.ma Pr. Chargui,
#    alloschool El Goufifa séance 15.
# Ici : la diméthylamine (pKa = 10,7 à 25 °C), notre C et notre pH ; le cours prend l'ammoniac à 1,0 × 10⁻² mol/L.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch13 import *

KE = 1.0e-14
C, PH = 1.0e-2, 11.3
HO = 10 ** (PH - 14)
TAU = HO / C
QR = C * TAU ** 2 / (1 - TAU)
KA = KE / QR
PKA = -math.log10(KA)
assert abs(HO - 2.0e-3) < 1e-5 and abs(TAU - 0.20) < 0.001 and abs(QR - 5.0e-4) < 5e-6 and abs(PKA - 10.7) < 0.01

sC, sPH = 4.0e-3, 11.07
sHO = 10 ** (sPH - 14)
sTAU = sHO / sC
sQR = sC * sTAU ** 2 / (1 - sTAU)
sPKA = -math.log10(KE / sQR)
assert abs(sHO - 1.17e-3) < 1e-5 and abs(sTAU - 0.294) < 0.001 and abs(sQR - 4.9e-4) < 5e-6 and abs(sPKA - 10.7) < 0.02

def fig(c, ph):
    return {"type": "schema", "titre": "La solution S_B de diméthylamine", "cadre": {"l": 6, "h": 3},
            "elements": [
              {"f": "rect", "de": [1.6, 0.3], "a": [3.6, 2.0], "couleur": "blanc", "remplir": "faible"},
              {"f": "texte", "at": [2.6, 2.4], "t": "S_B : C = " + c, "couleur": "cyan", "ancre": "centre"},
              {"f": "rect", "de": [4.1, 1.2], "a": [5.8, 2.0], "couleur": "jaune"},
              {"f": "texte", "at": [4.95, 1.6], "t": ph, "couleur": "jaune", "ancre": "centre", "taille": "petit"},
              {"f": "ligne", "pts": [[4.3, 1.2], [3.0, 0.8]], "couleur": "faible"},
              {"f": "texte", "at": [4.95, 0.8], "t": "pH-mètre", "ancre": "centre", "taille": "petit"}]}

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction de la diméthylamine (CH₃)₂NH avec l'eau.",
    "السؤال un: كتب l'équation ديال la réaction ديال la diméthylamine مع الما.",
    phrase("(CH₃)₂NH(aq) + H₂O(l) ⇌ (CH₃)₂NH₂⁺(aq) + HO⁻(aq)"),
    (["(CH₃)₂NH", "H₂O", "(CH₃)₂NH₂⁺", "HO⁻", "⇌"], ["H₃O⁺", "→"]),
    [("La diméthylamine est une base : elle capte un proton. Qui le lui donne ici ?",
      "la diméthylamine هي base: كتاخد un proton. شكون كيعطيهولها هنا؟"),
     ("L'eau joue le rôle d'acide et devient HO⁻ ; la réaction est limitée : double flèche.",
      "الما كيلعب دور l'acide، و كيولي H O moins. و la réaction محدودة: double flèche.")],
    [("1 : (CH₃)₂NH(aq) + H₂O(l) ⇌ (CH₃)₂NH₂⁺(aq) + HO⁻(aq)", "la diméthylamine، plus H deux O")],
    "السؤال un. la diméthylamine، plus H deux O، double flèche، l'ion diméthylammonium، plus H O moins. الما هنا هو l'acide.",
    "ex_1", "fa_1"),
  Q("2", "Le pH de la solution S_B vaut 11,3. Calculer la concentration [HO⁻]éq.",
    "السؤال deux: le p H ديال S B égale onze virgule trois. حسب la concentration des ions H O moins à l'équilibre.",
    val("[HO⁻]éq", HO, "mol/L", "[HO⁻]éq = Ke/[H₃O⁺]éq = 10^(pH − 14) = 10^(−2,7) = 2,0 × 10⁻³ mol/L"),
    (["[HO⁻] = Ke/[H₃O⁺]", "[H₃O⁺] = 10^(−pH)", "10^(pH − 14)", "mol/L"], ["[HO⁻] = 10^(−pH)", "[HO⁻] = C"]),
    [("Le pH donne d'abord [H₃O⁺]éq ; une autre relation relie [H₃O⁺] et [HO⁻] dans toute solution.",
      "le p H كيعطي اللول la concentration des ions H trois O plus. و كاينة relation أخرى كتربطها مع H O moins."),
     ("[HO⁻]éq = Ke/[H₃O⁺]éq = 10^(pH − 14). Attention : la base est faible, [HO⁻] n'est pas C.",
      "la concentration des ions H O moins، égale K e sur la concentration des ions H trois O plus، يعني dix puissance p H moins quatorze. رد البال: la base faible، إذن ماشي C.")],
    [("2 : [HO⁻]éq = Ke/[H₃O⁺]éq = 10^(pH − 14)", "dix puissance p H moins quatorze"),
     ("[HO⁻]éq = 10^(11,3 − 14) = 10^(−2,7)", "dix puissance moins deux virgule sept"),
     ("[HO⁻]éq = 2,0 × 10⁻³ mol/L", "deux virgule zéro fois dix puissance moins trois")],
    "السؤال deux. la concentration des ions H O moins، égale K e sur la concentration des ions H trois O plus، يعني dix puissance p H moins quatorze. l'application numérique: dix puissance moins deux virgule sept، égale deux virgule zéro fois dix puissance moins trois، mole par litre.",
    "ex_2", "fa_2"),
  Q("3", "À l'aide du tableau d'avancement, montrer que le taux d'avancement final s'écrit τ = 10^(pH − pKe)/C. Calculer τ et conclure.",
    "السؤال trois: ب le tableau d'avancement، بين بلي tau égale dix puissance p H moins p K e، sur C. حسب tau و استنتج.",
    val("τ", TAU, None, "τ = x_éq/x_max = [HO⁻]éq·V/(C·V) = 10^(pH − pKe)/C = 2,0 × 10⁻³/1,0 × 10⁻² = 0,20 < 1 : réaction limitée"),
    (["τ = x_éq/x_max", "x_max = C·V", "x_éq = [HO⁻]éq·V", "pKe = 14"], ["τ = 10^(−pH)/C", "x_max = [HO⁻]·V"]),
    [("Dans le tableau, la quantité d'ions HO⁻ formés à l'équilibre est x_éq ; l'eau est en excès : quel est le réactif limitant ?",
      "فle tableau، la quantité ديال les ions H O moins à l'équilibre هي x éq. و الما en excès: شكون هو le réactif limitant؟"),
     ("x_max = C·V et x_éq = [HO⁻]éq·V ; V se simplifie, puis [HO⁻]éq = 10^(pH − pKe).",
      "x max égale C fois V، و x éq égale la concentration des ions H O moins fois V. V كيتحيد، و la concentration des ions H O moins égale dix puissance p H moins p K e.")],
    [("3 : x_max = C·V (la base est limitante) ; x_éq = n(HO⁻)éq = [HO⁻]éq·V", "x max égale C fois V"),
     ("τ = x_éq/x_max = [HO⁻]éq/C = 10^(pH − pKe)/C", "tau égale x éq sur x max"),
     ("τ = 2,0 × 10⁻³/1,0 × 10⁻² = 0,20", "tau égale zéro virgule vingt"),
     ("τ < 1 : la réaction est limitée", "la réaction محدودة")],
    "السؤال trois. الما en excès، إذن la diméthylamine هي le réactif limitant، و x max égale C fois V. فالتوازن، x éq égale la concentration des ions H O moins، fois V. إذن tau égale x éq sur x max، يعني dix puissance p H moins p K e، sur C. l'application numérique: deux virgule zéro fois dix puissance moins trois، sur un virgule zéro fois dix puissance moins deux. tau égale zéro virgule vingt، صغر من un: la réaction محدودة.",
    "ex_3", "fa_3"),
  Q("4", "Montrer que le quotient de réaction à l'équilibre s'écrit Qr,éq = C·τ²/(1 − τ), puis calculer sa valeur.",
    "السؤال quatre: بين بلي Q r à l'équilibre égale C fois tau au carré، sur un moins tau. ومن بعد حسبو.",
    val("Qr,éq", QR, None, "Qr,éq = [(CH₃)₂NH₂⁺]·[HO⁻]/[(CH₃)₂NH] = (C·τ)²/(C(1 − τ)) = C·τ²/(1 − τ) = 1,0 × 10⁻² × 0,20²/0,80 = 5,0 × 10⁻⁴"),
    (["Qr,éq", "[HO⁻] = C·τ", "[(CH₃)₂NH] = C(1 − τ)", "τ²"], ["H₂O dans Qr", "C·τ/(1 − τ)"]),
    [("Écris Qr,éq sans l'eau (solvant), puis exprime chaque concentration à l'équilibre avec C et τ grâce au tableau.",
      "كتب Q r à l'équilibre بلا الما، حيت هو le solvant. من بعد، كتب كل concentration ب C و tau من le tableau."),
     ("[(CH₃)₂NH₂⁺] = [HO⁻] = C·τ et [(CH₃)₂NH] = C − C·τ = C(1 − τ).",
      "l'ion diméthylammonium و H O moins: C fois tau. و la diméthylamine: C moins C tau، يعني C fois un moins tau.")],
    [("4 : Qr,éq = [(CH₃)₂NH₂⁺]éq·[HO⁻]éq/[(CH₃)₂NH]éq", "Q r à l'équilibre égale"),
     ("= (C·τ)²/(C(1 − τ)) = C·τ²/(1 − τ)", "C fois tau au carré، sur un moins tau"),
     ("Qr,éq = 1,0 × 10⁻² × 0,20²/0,80 = 5,0 × 10⁻⁴", "cinq virgule zéro fois dix puissance moins quatre")],
    "السؤال quatre. Q r à l'équilibre égale، l'ion diméthylammonium fois H O moins، sur la diméthylamine. الما ما كيدخلش. les deux produits: C fois tau. la base اللي بقات: C fois un moins tau. إذن Q r à l'équilibre égale C fois tau au carré، sur un moins tau. l'application numérique: un virgule zéro fois dix puissance moins deux، fois zéro virgule vingt au carré، sur zéro virgule quatre-vingts. le résultat: cinq virgule zéro fois dix puissance moins quatre.",
    "ex_4", "fa_4"),
  Q("5", "En déduire la constante d'acidité Ka du couple (CH₃)₂NH₂⁺/(CH₃)₂NH, puis son pKa.",
    "السؤال cinq: استنتج K a ديال le couple، l'ion diméthylammonium، la diméthylamine، ومن بعد p K a.",
    val("pKa", PKA, None, "Ka = Ke/Qr,éq = 1,0 × 10⁻¹⁴/5,0 × 10⁻⁴ = 2,0 × 10⁻¹¹ ; pKa = −log Ka = 10,7", tol=0.01),
    (["Ka = Ke/Qr,éq", "pKa = −log Ka", "[H₃O⁺]"], ["Ka = Qr,éq", "Ka = Qr,éq/Ke"]),
    [("Qr,éq n'est pas Ka : Ka est la constante de l'ACIDE (CH₃)₂NH₂⁺ avec l'eau. Multiplie le haut et le bas de Qr,éq par [H₃O⁺].",
      "Q r à l'équilibre ماشي K a. K a هي ديال l'acide، l'ion diméthylammonium. ضرب الفوق و التحت ف la concentration des ions H trois O plus."),
     ("En haut apparaît Ke, en bas apparaît Ka : Qr,éq = Ke/Ka, donc Ka = Ke/Qr,éq.",
      "فالفوق كيبان K e، و فالتحت كيبان K a. إذن Q r à l'équilibre égale K e sur K a، و K a égale K e sur Q r.")],
    [("5 : Qr,éq = Ke/Ka donc Ka = Ke/Qr,éq", "K a égale K e sur Q r"),
     ("Ka = 1,0 × 10⁻¹⁴/5,0 × 10⁻⁴ = 2,0 × 10⁻¹¹", "deux virgule zéro fois dix puissance moins onze"),
     ("pKa = −log(2,0 × 10⁻¹¹) = 10,7", "p K a égale dix virgule sept")],
    "السؤال cinq. نضربو الفوق و التحت ف la concentration des ions H trois O plus: Q r à l'équilibre égale K e sur K a. إذن K a égale K e sur Q r، يعني un virgule zéro fois dix puissance moins quatorze، sur cinq virgule zéro fois dix puissance moins quatre، égale deux virgule zéro fois dix puissance moins onze. و p K a égale moins log de K a: p K a égale dix virgule sept.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : une base faible dans l'eau", "La base capte un proton de l'eau : il se forme HO⁻ ; réaction limitée.",
      "acides-bases-tableau/base.html?vue=ammoniac", "L'ammoniac dans l'eau, à la loupe",
      "فla simulation، base faible: l'ammoniac، C égale un virgule zéro fois dix puissance moins deux، mole par litre. l'équation: N H trois، plus H deux O، double flèche، N H quatre plus، plus H O moins. هنا الما كيلعب دور l'acide. شوف ب la loupe: N H trois كتاخد un proton H plus من molécule ديال الما. فالتمرين ديالنا نفس الشي: la diméthylamine، plus H deux O، double flèche، l'ion diméthylammonium، plus H O moins.",
      [("(CH₃)₂NH + H₂O ⇌ (CH₃)₂NH₂⁺ + HO⁻", "فالتمرين ديالنا نفس الشي")],
      [("فla simulation، base faible", "moment:becher"), ("l'équation: N H trois", "moment:equation"), ("شوف ب la loupe", "moment:loupe")]),
  sim("ex_2", "Question 2 : [HO⁻] à partir du pH", "[HO⁻] = Ke/[H₃O⁺] = 10^(pH − 14).",
      "acides-bases-tableau/eau.html?vue=ho", "Du pH à la concentration des ions HO⁻",
      "ب K e، كنلقاو la concentration des ions H O moins. la relation: la concentration des ions H O moins، égale K e، sur la concentration des ions H trois O plus. فla simulation، l'ammoniac، p H dix virgule soixante. الشكل ديال le p H: la concentration des ions H O moins، égale dix puissance p H moins quatorze، يعني trois virgule quatre-vingt-dix-huit fois dix puissance moins quatre، mole par litre. رد البال: ماشي dix puissance moins p H. فالتمرين ديالنا، p H égale onze virgule trois: dix puissance moins deux virgule sept، يعني deux virgule zéro fois dix puissance moins trois، mole par litre.",
      [("[HO⁻]éq = 10^(pH − 14)", "الشكل ديال le p H"), ("[HO⁻]éq = 10^(−2,7) = 2,0 × 10⁻³ mol/L", "يعني deux virgule zéro fois dix puissance moins trois")],
      [("la relation: la concentration", "moment:relation"), ("فla simulation، l'ammoniac", "moment:base"),
       ("الشكل ديال le p H", "moment:forme_ph"), ("رد البال", "moment:piege")]),
  sim("ex_3", "Question 3 : τ d'une base, par les ions HO⁻", "τ = x_éq/x_max = [HO⁻]éq/C.",
      "acides-bases-tableau/base.html?vue=taux", "Le tableau d'avancement et le taux",
      "le tableau d'avancement: la base، الما en excès، l'acide conjugué، و H O moins. فالبداية: C fois V، en excès، zéro، zéro. يلا كانت la réaction totale: x max égale C fois V. ولكن فالتوازن: x éq، égale la concentration des ions H O moins à l'équilibre، fois V. إذن tau égale la concentration des ions H O moins à l'équilibre، sur C. فla simulation، zéro virgule zéro quarante. فالتمرين ديالنا: deux virgule zéro fois dix puissance moins trois، sur un virgule zéro fois dix puissance moins deux، égale zéro virgule vingt. صغر من un: la réaction محدودة.",
      [("τ = [HO⁻]éq/C = 10^(pH − pKe)/C", "إذن tau égale"), ("τ = 0,20 < 1 : limitée", "égale zéro virgule vingt")],
      [("le tableau d'avancement", "moment:tableau"), ("يلا كانت la réaction totale", "moment:x_max"), ("ولكن فالتوازن", "moment:x_eq"),
       ("إذن tau égale", "moment:relation"), ("فla simulation، zéro virgule zéro quarante", "moment:application"), ("صغر من un", "moment:limitee")]),
  sim("ex_4", "Question 4 : Qr,éq en fonction de C et τ", "Chaque concentration à l'équilibre s'écrit avec C et τ.",
      "acides-bases-tableau/base.html?vue=constante", "La constante d'équilibre avec C et τ",
      "نتفكرو le chapitre اللي فات. فla simulation، l'acide فالما: le tableau كيعطي les deux produits، C fois tau. و l'acide اللي بقا، C fois un moins tau. إذن la relation: K égale C fois tau au carré، sur un moins tau. K هي Q r à l'équilibre. فالتمرين ديالنا، نفس la forme مع la base: les produits، l'ion diméthylammonium و H O moins، C fois tau. و la base اللي بقات، C fois un moins tau. إذن Q r à l'équilibre égale un virgule zéro fois dix puissance moins deux، fois zéro virgule vingt au carré، sur zéro virgule quatre-vingts، يعني cinq virgule zéro fois dix puissance moins quatre.",
      [("Qr,éq = C·τ²/(1 − τ)", "إذن la relation"), ("Qr,éq = 5,0 × 10⁻⁴", "يعني cinq virgule zéro fois dix puissance moins quatre")],
      [("فla simulation، l'acide فالما", "moment:tableau"), ("إذن la relation", "moment:relation"), ("K هي Q r", "moment:constante")]),
  sim("ex_5", "Question 5 : Ka = Ke/Qr,éq", "On multiplie le haut et le bas de Qr,éq par [H₃O⁺] : Ke en haut, Ka en bas.",
      "acides-bases-tableau/acidite.html?vue=ammonium", "Du Qr,éq de la base au Ka du couple",
      "فla simulation، le couple، N H quatre plus، N H trois. K a égale N H trois fois H trois O plus، sur N H quatre plus. ولكن Q r à l'équilibre ديال l'ammoniac مع الما، فيها H O moins. هادي ماشي K a! نضربو الفوق و التحت ف la concentration des ions H trois O plus. فالفوق كيبان K e، و فالتحت كيبان K a. إذن K a égale K e sur Q r à l'équilibre. فالتمرين ديالنا: dix puissance moins quatorze، sur cinq virgule zéro fois dix puissance moins quatre، يعني deux virgule zéro fois dix puissance moins onze. و p K a égale dix virgule sept.",
      [("Ka = Ke/Qr,éq = 2,0 × 10⁻¹¹", "إذن K a égale K e sur Q r à l'équilibre"), ("pKa = 10,7", "و p K a égale dix virgule sept")],
      [("فla simulation، le couple", "moment:ka"), ("ولكن Q r à l'équilibre", "moment:quotient"),
       ("نضربو الفوق و التحت", "moment:multiplier"), ("إذن K a égale K e sur Q r", "moment:relation")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : la base dans l'eau", "نتمرنو بسؤال ساهل. اختار l'équation الصحيحة.",
      "Quelle équation modélise la réaction de la diméthylamine avec l'eau ?",
      ["(CH₃)₂NH + H₂O ⇌ (CH₃)₂NH₂⁺ + HO⁻", "(CH₃)₂NH + H₂O → (CH₃)₂NH₂⁺ + HO⁻", "(CH₃)₂NH + H₃O⁺ ⇌ (CH₃)₂NH₂⁺ + H₂O"], 0, {
        0: ("juste", "برافو! la base كتاخد un proton من الما، و la réaction محدودة: double flèche.", "Juste : la base capte un proton de l'eau ; réaction limitée, double flèche."),
        1: (("قريب! ولكن la base faible، و la réaction ديالها مع الما محدودة. شنو هو السهم المناسب؟ عاود اختار.", "La réaction d'une base faible avec l'eau est limitée. Réessaie."),
            ("الجواب هو مع double flèche، حيت la réaction محدودة.", "Réponse : (CH₃)₂NH + H₂O ⇌ (CH₃)₂NH₂⁺ + HO⁻.")),
        2: (("السؤال على la réaction مع الما، و فالبداية ماكاينش H trois O plus بزاف. عاود اختار.", "On demande la réaction avec l'eau. Réessaie."),
            ("الجواب هو مع H deux O، اللي كيعطي un proton و كيولي H O moins.", "Réponse : (CH₃)₂NH + H₂O ⇌ (CH₃)₂NH₂⁺ + HO⁻."))},
      "Quelle équation modélise la réaction de la diméthylamine avec l'eau ?"),
  qcm("fa_2", "Plus facile : [HO⁻] d'une base faible", "سؤال ساهل. اختار la bonne valeur.",
      "pH = 11,3 à 25 °C. [HO⁻]éq vaut…",
      ["5,0 × 10⁻¹² mol/L", "1,0 × 10⁻² mol/L", "2,0 × 10⁻³ mol/L"], 2, {
        2: ("juste", "برافو! dix puissance p H moins quatorze، يعني dix puissance moins deux virgule sept، deux virgule zéro fois dix puissance moins trois.", "Juste : [HO⁻] = 10^(pH − 14) = 2,0 × 10⁻³ mol/L."),
        0: (("هادي la concentration des ions H trois O plus، dix puissance moins p H. عاود اختار.", "C'est [H₃O⁺] = 10^(−pH). Réessaie."),
            ("الجواب هو deux virgule zéro fois dix puissance moins trois: dix puissance p H moins quatorze.", "Réponse : [HO⁻] = 10^(pH − 14) = 2,0 × 10⁻³ mol/L.")),
        1: (("هادي C. ولكن la base faible: ماشي كاملة كتعطي H O moins. عاود اختار.", "La base est faible : [HO⁻] < C. Réessaie."),
            ("الجواب هو deux virgule zéro fois dix puissance moins trois، صغر من C حيت la réaction محدودة.", "Réponse : 2,0 × 10⁻³ mol/L < C : réaction limitée."))},
      "p H égale onze virgule trois. La concentration des ions H O moins vaut ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "Base faible, C = 1,0 × 10⁻² mol/L, [HO⁻]éq = 2,0 × 10⁻³ mol/L.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("τ = [HO⁻]éq/C = 0,20.", True, "x_éq/x_max = [HO⁻]éq·V/(C·V) = 0,20."),
      ("Pour une base, τ = 10^(−pH)/C.", False, "10^(−pH) est [H₃O⁺] : pour une base, on utilise [HO⁻]éq = 10^(pH − 14)."),
      ("τ < 1 : la réaction de la base avec l'eau est limitée.", True, "x_éq < x_max.")]),
  qcm("fa_4", "Plus facile : Qr,éq", "سؤال ساهل: اختار l'expression.",
      "Avec [(CH₃)₂NH₂⁺] = [HO⁻] = C·τ et [(CH₃)₂NH] = C(1 − τ), Qr,éq vaut…",
      ["C·τ/(1 − τ)", "C·τ²/(1 − τ)", "τ²/(1 − τ)"], 1, {
        1: ("juste", "برافو! C tau fois C tau، sur C fois un moins tau، كتعطي C tau au carré sur un moins tau.", "Juste : (C·τ)²/(C(1 − τ)) = C·τ²/(1 − τ)."),
        0: (("نسيتي واحد من les produits: كاينين deux، كل واحد C fois tau. عاود اختار.", "Il y a deux produits, chacun C·τ. Réessaie."),
            ("الجواب هو C tau au carré sur un moins tau.", "Réponse : Qr,éq = C·τ²/(1 − τ).")),
        2: (("قريب! ولكن C ما كتحيدش كاملة: C au carré فالفوق، و C واحدة لتحت. عاود اختار.", "C² en haut, C en bas : il reste un C. Réessaie."),
            ("الجواب هو C tau au carré sur un moins tau: كتبقى C وحدة.", "Réponse : Qr,éq = C·τ²/(1 − τ)."))},
      "Le quotient de réaction à l'équilibre vaut ?"),
  qcm("fa_5", "Plus facile : Ka et Qr,éq", "سؤال ساهل على K a.",
      "Pour la base dans l'eau, Qr,éq = 5,0 × 10⁻⁴. Le Ka du couple (CH₃)₂NH₂⁺/(CH₃)₂NH vaut…",
      ["Ka = Ke/Qr,éq = 2,0 × 10⁻¹¹", "Ka = Qr,éq = 5,0 × 10⁻⁴", "Ka = Qr,éq/Ke = 5,0 × 10¹⁰"], 0, {
        0: ("juste", "برافو! Q r à l'équilibre égale K e sur K a، إذن K a égale K e sur Q r.", "Juste : Ka = Ke/Qr,éq = 2,0 × 10⁻¹¹."),
        1: (("هادا هو الغلط المشهور: Q r ديال la base مع الما ماشي K a. K a هي ديال l'acide مع الما. عاود اختار.", "Qr,éq de la base n'est pas Ka. Réessaie."),
            ("الجواب هو K e sur Q r: نضربو الفوق و التحت ف H trois O plus.", "Réponse : Ka = Ke/Qr,éq = 2,0 × 10⁻¹¹.")),
        2: (("قلبتي: K a ديما صغر من un هنا. Q r égale K e sur K a. عاود اختار.", "C'est l'inverse : Qr,éq = Ke/Ka. Réessaie."),
            ("الجواب هو K a égale K e sur Q r، يعني deux virgule zéro fois dix puissance moins onze.", "Réponse : Ka = Ke/Qr,éq."))},
      "Q r à l'équilibre égale cinq virgule zéro fois dix puissance moins quatre. Le K a du couple vaut ?"),
]

SIM_Q = [
  QS("1", "Écrire l'équation de la réaction de la diméthylamine avec l'eau.",
     phrase("(CH₃)₂NH(aq) + H₂O(l) ⇌ (CH₃)₂NH₂⁺(aq) + HO⁻(aq)"),
     (["⇌", "HO⁻"], ["→", "H₃O⁺"]),
     [("(CH₃)₂NH + H₂O ⇌ (CH₃)₂NH₂⁺ + HO⁻", "double flèche")],
     "la diméthylamine، plus H deux O، double flèche، l'ion diméthylammonium، plus H O moins."),
  QS("2", "Le pH de S_B vaut 11,07. Calculer [HO⁻]éq.",
     val("[HO⁻]éq", sHO, "mol/L", "[HO⁻]éq = 10^(pH − 14) = 10^(−2,93) = 1,2 × 10⁻³ mol/L"),
     (["10^(pH − 14)", "mol/L"], ["10^(−pH)"]),
     [("[HO⁻]éq = 10^(pH − 14) = 1,2 × 10⁻³ mol/L", "dix puissance p H moins quatorze")],
     "la concentration des ions H O moins، égale dix puissance p H moins quatorze، يعني dix puissance moins deux virgule quatre-vingt-treize، égale un virgule deux fois dix puissance moins trois، mole par litre."),
  QS("3", "Montrer que τ = 10^(pH − pKe)/C, calculer τ et conclure.",
     val("τ", sTAU, None, "τ = [HO⁻]éq/C = 1,17 × 10⁻³/4,0 × 10⁻³ = 0,29 < 1 : réaction limitée"),
     (["τ = x_éq/x_max", "x_max = C·V"], ["τ = 10^(−pH)/C"]),
     [("τ = x_éq/x_max = [HO⁻]éq/C", "tau égale x éq sur x max"), ("τ = 0,29 < 1 : limitée", "zéro virgule vingt-neuf")],
     "tau égale x éq sur x max، يعني la concentration des ions H O moins sur C. l'application numérique: un virgule dix-sept fois dix puissance moins trois، sur quatre virgule zéro fois dix puissance moins trois. tau égale zéro virgule vingt-neuf، صغر من un: la réaction محدودة."),
  QS("4", "Montrer que Qr,éq = C·τ²/(1 − τ) et calculer sa valeur.",
     val("Qr,éq", sQR, None, "Qr,éq = C·τ²/(1 − τ) = 4,0 × 10⁻³ × 0,294²/0,706 = 4,9 × 10⁻⁴"),
     (["[HO⁻] = C·τ", "C(1 − τ)"], ["C·τ/(1 − τ)"]),
     [("Qr,éq = (C·τ)²/(C(1 − τ)) = C·τ²/(1 − τ)", "C fois tau au carré"), ("Qr,éq = 4,9 × 10⁻⁴", "quatre virgule neuf fois dix puissance moins quatre")],
     "Q r à l'équilibre égale C fois tau au carré، sur un moins tau. l'application numérique كتعطي quatre virgule neuf fois dix puissance moins quatre."),
  QS("5", "En déduire Ka et pKa du couple (CH₃)₂NH₂⁺/(CH₃)₂NH.",
     val("pKa", sPKA, None, "Ka = Ke/Qr,éq = 1,0 × 10⁻¹⁴/4,9 × 10⁻⁴ = 2,0 × 10⁻¹¹ ; pKa = 10,7", tol=0.01),
     (["Ka = Ke/Qr,éq", "pKa = −log Ka"], ["Ka = Qr,éq"]),
     [("Ka = Ke/Qr,éq = 2,0 × 10⁻¹¹", "K a égale K e sur Q r"), ("pKa = 10,7", "dix virgule sept")],
     "K a égale K e sur Q r à l'équilibre، يعني deux virgule zéro fois dix puissance moins onze. و p K a égale dix virgule sept."),
]

EX = exercice(
  "phys_ex_ch13_acides_bases_4", "phys_ch13_acides_bases", "acides_bases",
  "La diméthylamine dans l'eau : τ, Qr,éq et pKa", "moyen", 30,
  ["Écrire la réaction d'une base avec l'eau", "Calculer [HO⁻] à partir du pH", "Établir et calculer τ d'une base", "Établir Qr,éq en fonction de C et τ", "Déduire Ka = Ke/Qr,éq et pKa"],
  "La diméthylamine (CH₃)₂NH est une base faible. On prépare une solution aqueuse S_B de diméthylamine de concentration C = 1,0 × 10⁻² mol/L. À 25 °C, le pH-mètre indique pH = 11,3. Donnée : Ke = 1,0 × 10⁻¹⁴ (pKe = 14) à 25 °C.",
  "دابا نقراو l'énoncé. la diméthylamine هي base faible. وجدنا la solution S B ديال la diméthylamine، C égale un virgule zéro fois dix puissance moins deux، mole par litre. à vingt-cinq degrés، le p H mètre كيعطي onze virgule trois. و K e égale dix puissance moins quatorze.",
  [fig("1,0 × 10^{-2} mol/L", "pH = 11,3")],
  ["C = 1,0 × 10⁻² mol/L", "pH(S_B) = 11,3 à 25 °C", "Ke = 1,0 × 10⁻¹⁴ ; pKe = 14", "Couple (CH₃)₂NH₂⁺(aq)/(CH₃)₂NH(aq)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Une solution de diméthylamine a pour concentration C = 4,0 × 10⁻³ mol/L ; son pH vaut 11,07 à 25 °C. Ke = 1,0 × 10⁻¹⁴.",
  "نفس التمرين، بقيم أخرى. la diméthylamine، C égale quatre virgule zéro fois dix puissance moins trois، mole par litre، و le p H égale onze virgule zéro sept.",
  [fig("4,0 × 10^{-3} mol/L", "pH = 11,07")],
  ["C = 4,0 × 10⁻³ mol/L", "pH = 11,07", "Ke = 1,0 × 10⁻¹⁴"],
  SIM_Q)

ecrire(EX)
