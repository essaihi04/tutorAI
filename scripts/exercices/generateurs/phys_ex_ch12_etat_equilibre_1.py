# Exercice de chimie, ch. 12 (état d'équilibre d'un système chimique), niveau facile : s'entraîner à écrire Qr
# (l'eau et les solides n'y entrent pas) et à calculer Qr,i d'un mélange (concentrations dans le volume total).
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2017 N (I.1 Qr,i d'une pile, solides exclus, exposants), 2018 R (I.1 Qr,i),
#    2019 R (1 Qr,i), 2020 R (2.3 Qr,i d'un mélange acide méthanoïque + éthanoate : le piège du volume total) —
#    backend/data/exams/physique ;
#  - profs (architecture/phys_ch12_etat_equilibre.md § 1 : Naceiri Mrabti, El Goufifa / AlloSchool séance 9,
#    Moutamadris, fiche 2BAC PC+SM, vidéo Bazhar) : Qr → Qr,i → Qr,éq → K ; « eau = 1, solides = 1 » ; erreur
#    fréquente : diviser n par le volume du flacon au lieu du volume total ;
#  - séries en ligne : talamidi (état d'équilibre, activités 1), moutamadris (cours « évolution spontanée », exercices
#    Qr,i), docs Google d'un prof BIOF (Qr,i et K, Ag⁺/Fe²⁺), Naceiri Mrabti (livre 2BAC, p. 149-158), alloschool
#    (El Goufifa, séance 9), talamidi (acide-base, exercices non corrigés 2).
# Ici : notre propre mélange (acide benzoïque, ions méthanoate, ions benzoate, acide méthanoïque) et nos volumes.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch12 import *

# mélange : (concentration mol/L, volume L)
S1 = (0.010, 0.100)   # acide benzoïque C6H5COOH
S2 = (0.020, 0.050)   # méthanoate de sodium (HCOO⁻)
S3 = (0.010, 0.050)   # benzoate de sodium (C6H5COO⁻)
S4 = (0.020, 0.050)   # acide méthanoïque HCOOH
n1, n2, n3, n4 = (c * v for c, v in (S1, S2, S3, S4))
VT = S1[1] + S2[1] + S3[1] + S4[1]
c1 = n1 / VT
QRI = (n3 * n4) / (n1 * n2)
assert abs(VT - 0.250) < 1e-12 and abs(c1 - 4.0e-3) < 1e-12 and abs(QRI - 0.50) < 1e-12

# similaire
T1, T2, T3, T4 = (0.020, 0.050), (0.010, 0.100), (0.020, 0.025), (0.020, 0.025)
m1, m2, m3, m4 = (c * v for c, v in (T1, T2, T3, T4))
sVT = T1[1] + T2[1] + T3[1] + T4[1]
sc1 = m1 / sVT
sQRI = (m3 * m4) / (m1 * m2)
assert abs(sVT - 0.200) < 1e-12 and abs(sc1 - 5.0e-3) < 1e-12 and abs(sQRI - 0.25) < 1e-12

FIG = tableau_texte("Les quatre solutions versées dans le bécher",
    ["Solution", "Espèce apportée", "C (mol/L)", "V (mL)"],
    [["S₁", "C₆H₅COOH", "0,010", "100"], ["S₂", "HCOO⁻ (+ Na⁺)", "0,020", "50"],
     ["S₃", "C₆H₅COO⁻ (+ Na⁺)", "0,010", "50"], ["S₄", "HCOOH", "0,020", "50"]])
sFIG = tableau_texte("Les quatre solutions versées dans le bécher",
    ["Solution", "Espèce apportée", "C (mol/L)", "V (mL)"],
    [["S₁", "C₆H₅COOH", "0,020", "50"], ["S₂", "HCOO⁻ (+ Na⁺)", "0,010", "100"],
     ["S₃", "C₆H₅COO⁻ (+ Na⁺)", "0,020", "25"], ["S₄", "HCOOH", "0,020", "25"]])

QR_TXT = "Qr = [C₆H₅COO⁻]·[HCOOH] / ([C₆H₅COOH]·[HCOO⁻])"
QR_DIT = "Q r égale la concentration des ions benzoate، fois la concentration de l'acide méthanoïque، sur la concentration de l'acide benzoïque، fois la concentration des ions méthanoate"

QUESTIONS = [
  Q("1", "Écrire l'expression du quotient de réaction Qr associé à l'équation de la réaction.",
    "السؤال un: كتب l'expression ديال le quotient de réaction Q r، ديال هاد la réaction.",
    phrase(QR_TXT + " (produits en haut, réactifs en bas, coefficients 1)"),
    (["Qr", "[C₆H₅COO⁻]", "[HCOOH]", "[C₆H₅COOH]", "[HCOO⁻]", "/"], ["[H₂O]", "Qr = [C₆H₅COOH]·[HCOO⁻]/…"]),
    [("Repère d'abord les produits (à droite de la double flèche) et les réactifs (à gauche).",
      "شوف l'équation: شكون les produits، على اليمين ديال la double flèche؟ و شكون les réactifs، على اليسار؟"),
     ("Qr = produit des concentrations des produits, divisé par le produit des concentrations des réactifs ; ici tous les coefficients valent 1.",
      "Q r égale les concentrations ديال les produits الفوق، على les concentrations ديال les réactifs التحت. وهنا كاع les coefficients كيساويو un.")],
    [("1 : les produits au numérateur, les réactifs au dénominateur", "les produits الفوق"),
     (QR_TXT, "Q r égale la concentration des ions benzoate")],
    "السؤال un. les produits الفوق، و les réactifs التحت، و les coefficients كاملين un. إذن " + QR_DIT + ".",
    "ex_1", "fa_1"),
  Q("2", "Calculer le volume total V_T du mélange, puis la concentration initiale de l'acide benzoïque [C₆H₅COOH]ᵢ dans le mélange.",
    "السؤال deux: حسب le volume total V T ديال الخليط، ومن بعد la concentration initiale ديال l'acide benzoïque فالخليط.",
    val("[C₆H₅COOH]ᵢ", c1, "mol/L", "V_T = 250 mL ; [C₆H₅COOH]ᵢ = n₁/V_T = C₁·V₁/V_T = 0,010 × 0,100/0,250 = 4,0 × 10⁻³ mol/L"),
    (["V_T = V₁ + V₂ + V₃ + V₄", "n = C·V", "[X]ᵢ = n/V_T", "mol/L"], ["[X]ᵢ = n/V₁", "[X]ᵢ = C₁"]),
    [("Après le mélange, l'acide benzoïque n'est plus dans 100 mL : il est dans tout le bécher. Quel volume ?",
      "من بعد الخليط، l'acide benzoïque ما بقاش ف cent millilitres: ولا فالبيشر كامل. شحال le volume ديالو؟"),
     ("V_T = 100 + 50 + 50 + 50 = 250 mL ; n₁ = C₁·V₁, puis [C₆H₅COOH]ᵢ = n₁/V_T.",
      "V T égale cent plus cinquante plus cinquante plus cinquante، يعني deux cent cinquante millilitres. n un égale C un fois V un، ومن بعد la concentration égale n un sur V T.")],
    [("2 : V_T = 100 + 50 + 50 + 50 = 250 mL", "V T égale deux cent cinquante millilitres"),
     ("n₁ = C₁·V₁ = 0,010 × 0,100 = 1,0 × 10⁻³ mol", "n un égale C un fois V un"),
     ("[C₆H₅COOH]ᵢ = n₁/V_T = 1,0 × 10⁻³/0,250 = 4,0 × 10⁻³ mol/L", "égale quatre virgule zéro fois dix puissance moins trois mole par litre")],
    "السؤال deux. V T égale deux cent cinquante millilitres. n un égale C un fois V un، يعني un virgule zéro fois dix puissance moins trois mole. la concentration initiale ديال l'acide benzoïque، n un sur V T، égale quatre virgule zéro fois dix puissance moins trois mole par litre. ماشي zéro virgule zéro dix: هادي كانت فالفلاكون، قبل الخليط.",
    "ex_2", "fa_2"),
  Q("3", "Calculer la valeur du quotient de réaction Qr,i dans l'état initial du mélange.",
    "السؤال trois: حسب la valeur ديال Q r i، le quotient de réaction فl'état initial ديال الخليط.",
    val("Qr,i", QRI, None, "Qr,i = n(C₆H₅COO⁻)·n(HCOOH)/(n(C₆H₅COOH)·n(HCOO⁻)) = (5,0 × 10⁻⁴ × 1,0 × 10⁻³)/(1,0 × 10⁻³ × 1,0 × 10⁻³) = 0,50"),
    (["Qr,i", "n/V_T", "V_T se simplifie", "sans unité"], ["Qr,i = 0", "mol/L"]),
    [("Remplace chaque concentration par n/V_T : que devient V_T, deux fois en haut et deux fois en bas ?",
      "بدل كل concentration ب n sur V T. V T كاين deux fois الفوق و deux fois التحت: شنو كيوقع ليه؟"),
     ("V_T se simplifie : Qr,i = n₃·n₄/(n₁·n₂), avec n = C·V pour chaque solution. Qr n'a pas d'unité.",
      "V T كيتحيد. إذن Q r i égale n trois fois n quatre، sur n un fois n deux، و n égale C fois V لكل solution. و Q r بلا وحدة.")],
    [("3 : Qr,i = ([C₆H₅COO⁻]ᵢ·[HCOOH]ᵢ)/([C₆H₅COOH]ᵢ·[HCOO⁻]ᵢ) ; V_T se simplifie", "V T كيتحيد"),
     ("Qr,i = (5,0 × 10⁻⁴ × 1,0 × 10⁻³)/(1,0 × 10⁻³ × 1,0 × 10⁻³)", "l'application numérique"),
     ("Qr,i = 0,50 (sans unité)", "Q r i égale zéro virgule cinquante")],
    "السؤال trois. فQ r i، V T كيتحيد، إذن نخدمو ب les quantités de matière: les ions benzoate cinq virgule zéro fois dix puissance moins quatre mole، l'acide méthanoïque un virgule zéro fois dix puissance moins trois، l'acide benzoïque un virgule zéro fois dix puissance moins trois، و les ions méthanoate un virgule zéro fois dix puissance moins trois. l'application numérique: Q r i égale zéro virgule cinquante، بلا وحدة.",
    "ex_3", "fa_3"),
]

EXPLICATIONS = [
  slide("ex_1", "generale", "Question 1 : écrire Qr",
        "Produits en haut, réactifs en bas, coefficients en exposants.",
        "فالتمرين ديالنا: les produits هوما les ions benzoate و l'acide méthanoïque، و les réactifs هوما l'acide benzoïque و les ions méthanoate، و les coefficients كاملين un. إذن " + QR_DIT + ".",
        [(QR_TXT, "إذن Q r égale la concentration des ions benzoate")]),
  slide("ex_2", "melange", "Question 2 : la concentration dans le volume total",
        "Après le mélange, chaque espèce occupe tout le volume V_T.",
        "فالتمرين ديالنا: V T égale deux cent cinquante millilitres. l'acide benzoïque: n un égale un virgule zéro fois dix puissance moins trois mole، sur zéro virgule deux cent cinquante litre. إذن la concentration initiale égale quatre virgule zéro fois dix puissance moins trois mole par litre.",
        [("V_T = 250 mL", "V T égale deux cent cinquante millilitres"),
         ("[C₆H₅COOH]ᵢ = 1,0 × 10⁻³/0,250 = 4,0 × 10⁻³ mol/L", "إذن la concentration initiale égale")]),
  slide("ex_3", "melange", "Question 3 : Qr,i avec les quantités de matière",
        "V_T se simplifie dans Qr,i : on calcule avec les n.",
        "فالتمرين ديالنا: Q r i égale n des ions benzoate fois n de l'acide méthanoïque، sur n de l'acide benzoïque fois n des ions méthanoate. يعني cinq virgule zéro fois dix puissance moins quatre، fois un virgule zéro fois dix puissance moins trois، sur un virgule zéro fois dix puissance moins trois، fois un virgule zéro fois dix puissance moins trois. le résultat: Q r i égale zéro virgule cinquante، بلا وحدة.",
        [("Qr,i = n₃·n₄/(n₁·n₂)", "فالتمرين ديالنا: Q r i égale"), ("Qr,i = 0,50", "le résultat: Q r i égale zéro virgule cinquante")]),
]

FACILES = [
  assoc("fa_1", "Plus facile : où va chaque espèce ?", "Place chaque espèce dans Qr.",
        "سؤال ساهل: ربط كل espèce مع البلاصة ديالها ف Q r.",
        "Relie chaque espèce à sa place dans Qr.",
        [("1", "C₆H₅COO⁻ (produit)"), ("2", "HCOO⁻ (réactif)"), ("3", "H₂O (solvant, dans une autre réaction)"), ("4", "HCOOH (produit)")],
        [("a", "Au numérateur"), ("b", "Au dénominateur"), ("c", "N'apparaît pas dans Qr")],
        {"1": "a", "2": "b", "3": "c", "4": "a"},
        {"1-a": (True, "Oui : un produit va au numérateur.", "برافو: les ions benzoate هوما produit، كيطلعو الفوق."),
         "1-b": (False, "C'est un produit : regarde de quel côté de la double flèche il est écrit.", "لا، شوف فين مكتوبين les ions benzoate ف l'équation: على اليمين، يعني produit."),
         "1-c": (False, "Il est dissous dans la solution : il a une concentration, il entre dans Qr.", "لا، les ions benzoate ذايبين، عندهم concentration، كيدخلو ف Q r."),
         "2-a": (False, "Il est écrit à gauche de la double flèche : c'est un réactif.", "لا، les ions méthanoate مكتوبين على اليسار: réactif."),
         "2-b": (True, "Oui : un réactif va au dénominateur.", "برافو: réactif، كيهبط التحت."),
         "2-c": (False, "Il est dissous, il a une concentration : il entre dans Qr.", "لا، عندهم concentration فالمحلول، كيدخلو ف Q r."),
         "3-a": (False, "L'eau solvant n'a pas de concentration à écrire dans Qr.", "لا، الما le solvant ما كنكتبوش la concentration ديالو."),
         "3-b": (False, "Même réactif, l'eau solvant ne s'écrit pas dans Qr.", "لا، حتى يلا كان réactif، الما le solvant ما كيدخلش."),
         "3-c": (True, "Oui : l'eau, solvant, n'apparaît pas dans Qr.", "برافو: الما هو le solvant، ما كيدخلش ف Q r."),
         "4-a": (True, "Oui : l'acide méthanoïque est formé, il va au numérateur.", "برافو: l'acide méthanoïque produit، كيطلع الفوق."),
         "4-b": (False, "Il est à droite de la double flèche : c'est un produit.", "لا، شوف l'équation: l'acide méthanoïque على اليمين."),
         "4-c": (False, "Il est dissous : il a une concentration, il entre dans Qr.", "لا، l'acide méthanoïque ذايب، كيدخل ف Q r.")},
        ("Produits au numérateur, réactifs au dénominateur, l'eau solvant (et un solide) n'apparaît pas.",
         "les produits الفوق، les réactifs التحت، والما le solvant ما كيدخلش.")),
  qcm("fa_2", "Plus facile : le bon volume", "سؤال ساهل: اختار le volume اللي كنقسمو عليه.",
      "On a versé 100 mL + 50 mL + 50 mL + 50 mL. Pour [C₆H₅COOH]ᵢ dans le mélange, on divise n₁ par…",
      ["100 mL", "50 mL", "250 mL"], 2, {
        2: ("juste", "برافو! من بعد الخليط، كل espèce فالبيشر كامل: V T égale deux cent cinquante millilitres.", "Juste : après le mélange, V_T = 250 mL."),
        0: (("ما تقلقش. cent millilitres هو le volume ديال le flacon ديال l'acide، قبل الخليط. فين ولا l'acide من بعد؟ عاود اختار.", "100 mL, c'est le flacon avant le mélange. Réessaie."),
            ("الجواب هو deux cent cinquante millilitres: l'acide ولا فالبيشر كامل.", "Réponse : V_T = 250 mL, tout le mélange.")),
        1: (("لا، cinquante millilitres هو حجم solution أخرى. l'acide من بعد الخليط فين كاين؟ عاود اختار.", "50 mL est le volume d'une autre solution. Réessaie."),
            ("الجواب هو deux cent cinquante millilitres: كنجمعو les quatre volumes.", "Réponse : V_T = 100 + 50 + 50 + 50 = 250 mL."))},
      "On a versé cent millilitres, plus trois fois cinquante millilitres. Pour la concentration de l'acide benzoïque dans le mélange, on divise n un par quel volume ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "Qr,i d'un mélange.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Dans Qr,i, V_T se simplifie : on peut calculer avec les quantités de matière.", True,
       "Il y a deux concentrations en haut et deux en bas : V_T se simplifie."),
      ("Qr,i s'exprime en mol/L.", False, "Qr est sans unité."),
      ("Si aucun produit n'est présent au départ, Qr,i = 0.", True, "Le numérateur est nul : Qr,i = 0.")]),
]

SIM_Q = [
  QS("1", "Écrire l'expression du quotient de réaction Qr.",
     phrase(QR_TXT),
     (["Qr", "[C₆H₅COO⁻]", "[HCOOH]", "/"], ["[H₂O]"]),
     [(QR_TXT, "Q r égale la concentration des ions benzoate")],
     "les produits الفوق، و les réactifs التحت: " + QR_DIT + "."),
  QS("2", "Calculer V_T, puis [C₆H₅COOH]ᵢ dans le mélange.",
     val("[C₆H₅COOH]ᵢ", sc1, "mol/L", "V_T = 200 mL ; [C₆H₅COOH]ᵢ = 0,020 × 0,050/0,200 = 5,0 × 10⁻³ mol/L"),
     (["V_T", "n = C·V", "[X]ᵢ = n/V_T"], ["[X]ᵢ = n/V₁"]),
     [("V_T = 50 + 100 + 25 + 25 = 200 mL", "V T égale deux cents millilitres"),
      ("[C₆H₅COOH]ᵢ = 1,0 × 10⁻³/0,200 = 5,0 × 10⁻³ mol/L", "cinq virgule zéro fois dix puissance moins trois mole par litre")],
     "V T égale deux cents millilitres. n un égale un virgule zéro fois dix puissance moins trois mole، إذن la concentration égale cinq virgule zéro fois dix puissance moins trois mole par litre."),
  QS("3", "Calculer Qr,i.",
     val("Qr,i", sQRI, None, "Qr,i = (5,0 × 10⁻⁴ × 5,0 × 10⁻⁴)/(1,0 × 10⁻³ × 1,0 × 10⁻³) = 0,25"),
     (["Qr,i", "V_T se simplifie"], ["Qr,i = 0"]),
     [("Qr,i = (5,0 × 10⁻⁴ × 5,0 × 10⁻⁴)/(1,0 × 10⁻³ × 1,0 × 10⁻³)", "V T كيتحيد"), ("Qr,i = 0,25", "zéro virgule vingt-cinq")],
     "V T كيتحيد. Q r i égale cinq virgule zéro fois dix puissance moins quatre، fois cinq virgule zéro fois dix puissance moins quatre، sur un virgule zéro fois dix puissance moins trois، fois un virgule zéro fois dix puissance moins trois. Q r i égale zéro virgule vingt-cinq."),
]
assert abs(m3 - 5.0e-4) < 1e-12 and abs(m4 - 5.0e-4) < 1e-12 and abs(m1 - 1.0e-3) < 1e-12 and abs(m2 - 1.0e-3) < 1e-12
assert abs(n3 - 5.0e-4) < 1e-12 and abs(n4 - 1.0e-3) < 1e-12 and abs(n2 - 1.0e-3) < 1e-12

EQ = "C₆H₅COOH(aq) + HCOO⁻(aq) ⇌ C₆H₅COO⁻(aq) + HCOOH(aq)"
EX = exercice(
  "phys_ex_ch12_etat_equilibre_1", "phys_ch12_etat_equilibre", "etat_equilibre",
  "Un mélange de quatre solutions : écrire et calculer Qr,i", "facile", 15,
  ["Écrire l'expression du quotient de réaction Qr", "Calculer une concentration initiale dans un mélange", "Calculer Qr,i (sans unité)"],
  "Dans un bécher, on mélange les quatre solutions du tableau. Il se produit la réaction d'équation : " + EQ + ". Les ions sodium Na⁺ ne participent pas à la réaction.",
  "دابا نقراو l'énoncé. فواحد le bécher، كنخلطو quatre solutions ديال le tableau. كتوقع la réaction: l'acide benzoïque، plus les ions méthanoate، ب la double flèche، كيعطيو les ions benzoate، plus l'acide méthanoïque. les ions sodium ما كيشاركوش ف la réaction.",
  [FIG], ["Équation : " + EQ, "S₁ : acide benzoïque, C₁ = 0,010 mol/L, V₁ = 100 mL", "S₂ : méthanoate de sodium, C₂ = 0,020 mol/L, V₂ = 50 mL",
          "S₃ : benzoate de sodium, C₃ = 0,010 mol/L, V₃ = 50 mL", "S₄ : acide méthanoïque, C₄ = 0,020 mol/L, V₄ = 50 mL"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "On mélange les quatre solutions du tableau (mêmes espèces). Même réaction : " + EQ + ".",
  "نفس التمرين، بقيم أخرى. كنخلطو quatre solutions ديال le tableau، ونفس la réaction.",
  [sFIG], ["S₁ : 0,020 mol/L, 50 mL", "S₂ : 0,010 mol/L, 100 mL", "S₃ : 0,020 mol/L, 25 mL", "S₄ : 0,020 mol/L, 25 mL"],
  SIM_Q)

ecrire(EX)
