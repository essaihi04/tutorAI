# Exercice de chimie, ch. 12 (état d'équilibre), niveau facile : du pH mesuré aux trois concentrations à
# l'équilibre, puis Qr,éq = K, une étape à la fois.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2017 N (1.2 Qr,éq en fonction de C et du pH), 2021 R (6 rapport [A⁻]/[AH] à
#    partir du pH), 2022 N (1.3 Qr,éq en fonction de Cₐ et [H₃O⁺]éq), 2023 N (1.2 proportion de CH₃COOH à
#    l'équilibre) — backend/data/exams/physique ;
#  - profs (architecture/phys_ch12_etat_equilibre.md § 1 : Naceiri Mrabti, El Goufifa, Moutamadris, fiche 2BAC,
#    Bazhar) : le pH donne [H₃O⁺]éq = 10^(−pH) ; [A⁻]éq = [H₃O⁺]éq par le tableau ; [AH]éq = C − [H₃O⁺]éq ;
#    pièges : écrire → au lieu de ⇌, mettre [H₂O] dans Qr, prendre [AH]éq = [H₃O⁺]éq ;
#  - séries en ligne : talamidi (état d'équilibre, activités 1), moutamadris (exercices état d'équilibre), alloschool
#    (El Goufifa, séance 9), Naceiri Mrabti (livre 2BAC), docs Google d'un prof BIOF, talamidi (acide-base, série 5).
# Ici : l'acide propanoïque à notre concentration, notre pH (calculé à partir de K ≈ 1,3 × 10⁻⁵).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch12 import *

C, PH = 5.0e-2, 3.09
H = h3o(PH)                    # 8,1e-4
A = C - H                      # 4,9e-2
QR = H * H / A                 # 1,3e-5
assert sci(H, 1) == "8,1 × 10⁻⁴" and sci(A, 1) == "4,9 × 10⁻²" and sci(QR, 1) == "1,3 × 10⁻⁵"
sC, sPH = 1.0e-2, 3.44
sH = h3o(sPH); sA = sC - sH; sQR = sH * sH / sA
assert sci(sH, 1) == "3,6 × 10⁻⁴" and sci(sA, 1) == "9,6 × 10⁻³" and sci(sQR, 1) == "1,4 × 10⁻⁵"

EQ = "C₂H₅COOH(aq) + H₂O(l) ⇌ C₂H₅COO⁻(aq) + H₃O⁺(aq)"
EQ_DIT = "l'acide propanoïque، plus الما، ب la double flèche، كيعطيو les ions propanoate، plus les ions H trois O plus"
QR_TXT = "Qr,éq = [C₂H₅COO⁻]éq·[H₃O⁺]éq / [C₂H₅COOH]éq"

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction de l'acide propanoïque avec l'eau.",
    "السؤال un: كتب l'équation ديال la réaction ديال l'acide propanoïque مع الما.",
    phrase(EQ + " (double flèche : réaction limitée)"),
    (["⇌", "H₂O", "H₃O⁺", "C₂H₅COO⁻"], ["→", "HO⁻"]),
    [("L'acide cède un proton H⁺ ; dans l'eau, qui le capte ? Et la réaction est-elle totale ?",
      "l'acide كيعطي un proton H plus. فالما، شكون كياخدو؟ وواش la réaction totale؟"),
     ("L'eau capte le proton et devient H₃O⁺ ; l'acide devient sa base C₂H₅COO⁻. La réaction est limitée : double flèche ⇌.",
      "الما كياخد le proton وكيولي H trois O plus، و l'acide كيولي la base ديالو، les ions propanoate. و la réaction محدودة: la double flèche.")],
    [("1 : " + EQ, "كيعطيو les ions propanoate")],
    "السؤال un. " + EQ_DIT + ". la double flèche حيت la réaction محدودة.",
    "ex_1", "fa_1"),
  Q("2", "Calculer la concentration [H₃O⁺]éq des ions oxonium à l'équilibre.",
    "السؤال deux: حسب la concentration des ions H trois O plus à l'équilibre.",
    val("[H₃O⁺]éq", H, "mol/L", f"[H₃O⁺]éq = 10^(−pH) = 10^(−3,09) = {sci(H, 1)} mol/L"),
    (["[H₃O⁺] = 10^(−pH)", "pH", "mol/L"], ["[H₃O⁺] = −log(pH)", "[H₃O⁺] = 10^(pH)"]),
    [("La réaction est rapide : le pH lu est celui de l'état d'équilibre. Quelle relation lie le pH et [H₃O⁺] ?",
      "la réaction سريعة: le p H اللي قرينا هو le p H à l'équilibre. شنو la relation بين le p H و la concentration des ions H trois O plus؟"),
     ("pH = −log[H₃O⁺], donc [H₃O⁺]éq = 10^(−pH).",
      "p H égale moins log de la concentration، إذن la concentration égale dix puissance moins p H.")],
    [("2 : [H₃O⁺]éq = 10^(−pH)", "dix puissance moins p H"),
     (f"[H₃O⁺]éq = 10^(−3,09) = {sci(H, 1)} mol/L", f"égale {dsci(H, 1)} mole par litre")],
    f"السؤال deux. la concentration des ions H trois O plus à l'équilibre، égale dix puissance moins p H، يعني dix puissance moins trois virgule zéro neuf. égale {dsci(H, 1)} mole par litre.",
    "ex_2", "fa_2"),
  Q("3", "À l'aide du tableau d'avancement, déterminer [C₂H₅COO⁻]éq et [C₂H₅COOH]éq.",
    "السؤال trois: بle tableau d'avancement، حدد la concentration des ions propanoate، و la concentration de l'acide propanoïque، à l'équilibre.",
    val("[C₂H₅COOH]éq", A, "mol/L", f"[C₂H₅COO⁻]éq = [H₃O⁺]éq = {sci(H, 1)} mol/L ; [C₂H₅COOH]éq = C − [H₃O⁺]éq = 5,0 × 10⁻² − {sci(H, 1)} = {sci(A, 1)} mol/L"),
    (["[C₂H₅COO⁻]éq = [H₃O⁺]éq", "C − [H₃O⁺]éq", "mol/L"], ["[C₂H₅COOH]éq = [H₃O⁺]éq", "[C₂H₅COOH]éq = C"]),
    [("Dans le tableau, les ions propanoate et les ions oxonium se forment ensemble, x et x. Et l'acide, combien en reste-t-il ?",
      "فle tableau، les ions propanoate و les ions H trois O plus كيتكونو مع بعض، x و x. و l'acide، شحال بقا منو؟"),
     ("[C₂H₅COO⁻]éq = [H₃O⁺]éq ; l'acide a perdu ce qui s'est formé : [C₂H₅COOH]éq = C − [H₃O⁺]éq.",
      "la concentration des ions propanoate égale celle des ions H trois O plus. و l'acide خسر قد اللي تكون: C moins la concentration des ions H trois O plus.")],
    [(f"3 : [C₂H₅COO⁻]éq = [H₃O⁺]éq = {sci(H, 1)} mol/L", "عندهم نفس التركيز"),
     ("[C₂H₅COOH]éq = C − [H₃O⁺]éq", "C moins la concentration des ions H trois O plus"),
     (f"[C₂H₅COOH]éq = 5,0 × 10⁻² − {sci(H, 1)} = {sci(A, 1)} mol/L", f"égale {dsci(A, 1)} mole par litre")],
    f"السؤال trois. les ions propanoate و les ions H trois O plus عندهم نفس التركيز: {dsci(H, 1)} mole par litre. و l'acide: C moins la concentration des ions H trois O plus، يعني cinq virgule zéro fois dix puissance moins deux، moins {dsci(H, 1)}. égale {dsci(A, 1)} mole par litre.",
    "ex_3", "fa_3"),
  Q("4", "Calculer le quotient de réaction Qr,éq dans l'état d'équilibre. En déduire la constante d'équilibre K associée à l'équation.",
    "السؤال quatre: حسب Q r à l'équilibre، واستنتج la constante d'équilibre K.",
    val("K", QR, None, f"K = Qr,éq = [C₂H₅COO⁻]éq·[H₃O⁺]éq/[C₂H₅COOH]éq = ({sci(H, 1)})²/{sci(A, 1)} = {sci(QR, 1)}", tol=0.05),
    (["Qr,éq", "K = Qr,éq", "( )²", "sans unité"], ["K = 1/Qr,éq", "mol/L"]),
    [("Écris Qr avec les concentrations à l'équilibre : les produits en haut, l'acide en bas, sans l'eau.",
      "كتب Q r ب les concentrations à l'équilibre: les produits الفوق، l'acide التحت، بلا الما."),
     ("Les deux concentrations du haut sont égales : Qr,éq = [H₃O⁺]éq²/[C₂H₅COOH]éq. Et K = Qr,éq.",
      "deux concentrations ديال الفوق متساويين: Q r à l'équilibre égale la concentration des ions H trois O plus au carré، sur la concentration de l'acide. و K égale Q r à l'équilibre.")],
    [("4 : " + QR_TXT, "Q r à l'équilibre égale la concentration des ions propanoate"),
     (f"Qr,éq = ({sci(H, 1)})²/{sci(A, 1)} = {sci(QR, 1)}", f"égale {dsci(QR, 1)}"),
     (f"K = Qr,éq = {sci(QR, 1)} (sans unité)", "إذن K égale Q r à l'équilibre")],
    f"السؤال quatre. Q r à l'équilibre égale la concentration des ions propanoate، fois la concentration des ions H trois O plus، sur la concentration de l'acide propanoïque. l'application numérique: {dsci(H, 1)}، au carré، sur {dsci(A, 1)}. égale {dsci(QR, 1)}، بلا وحدة. إذن K égale Q r à l'équilibre، {dsci(QR, 1)}.",
    "ex_4", "fa_4"),
]

EXPLICATIONS = [
  slide("ex_1", "definition", "Question 1 : l'équation de l'acide avec l'eau",
        "L'acide cède un proton à l'eau ; la réaction est limitée : ⇌.",
        "فالتمرين ديالنا، نفس الشكل: " + EQ_DIT + ".",
        [(EQ, "فالتمرين ديالنا، نفس الشكل")]),
  slide("ex_2", "concentrations", "Question 2 : [H₃O⁺]éq = 10^(−pH)",
        "Le pH lu est celui de l'équilibre : [H₃O⁺]éq = 10^(−pH).",
        f"فالتمرين ديالنا: le p H égale trois virgule zéro neuf. إذن la concentration des ions H trois O plus، égale dix puissance moins trois virgule zéro neuf، يعني {dsci(H, 1)} mole par litre.",
        [(f"[H₃O⁺]éq = 10^(−3,09) = {sci(H, 1)} mol/L", f"يعني {dsci(H, 1)} mole par litre")]),
  slide("ex_3", "concentrations", "Question 3 : les deux autres concentrations",
        "[C₂H₅COO⁻]éq = [H₃O⁺]éq et [C₂H₅COOH]éq = C − [H₃O⁺]éq.",
        f"فالتمرين ديالنا: les ions propanoate، {dsci(H, 1)} mole par litre. و l'acide propanoïque: cinq virgule zéro fois dix puissance moins deux، moins {dsci(H, 1)}، يعني {dsci(A, 1)} mole par litre. l'acide بقا تقريبا كامل.",
        [("[C₂H₅COO⁻]éq = [H₃O⁺]éq", "فالتمرين ديالنا: les ions propanoate"),
         (f"[C₂H₅COOH]éq = {sci(A, 1)} mol/L", f"يعني {dsci(A, 1)} mole par litre")]),
  slide("ex_4", "qr_eq", "Question 4 : Qr,éq, c'est K",
        "On remplace les trois concentrations à l'équilibre dans Qr.",
        f"فالتمرين ديالنا: Q r à l'équilibre égale {dsci(H, 1)}، au carré، sur {dsci(A, 1)}. يعني {dsci(QR, 1)}. وهاد القيمة ديال l'état d'équilibre هي la constante d'équilibre: K égale {dsci(QR, 1)}.",
        [(f"Qr,éq = ({sci(H, 1)})²/{sci(A, 1)} = {sci(QR, 1)}", f"يعني {dsci(QR, 1)}"),
         (f"K = Qr,éq = {sci(QR, 1)}", "هي la constante d'équilibre")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : la bonne équation", "سؤال ساهل: اختار l'équation الصحيحة.",
      "Quelle est l'équation de la réaction de l'acide propanoïque avec l'eau ?",
      ["C₂H₅COOH + H₂O → C₂H₅COO⁻ + H₃O⁺", "C₂H₅COOH + H₂O ⇌ C₂H₅COO⁻ + H₃O⁺", "C₂H₅COOH + HO⁻ ⇌ C₂H₅COO⁻ + H₂O"], 1, {
        1: ("juste", "برافو! l'acide كيعطي le proton للما، و la réaction محدودة: la double flèche.", "Juste : réaction limitée, double flèche."),
        0: (("قريب! ولكن la flèche simple كتعني la réaction totale. واش l'acide propanoïque كيتفاعل كامل مع الما؟ عاود اختار.", "La flèche simple dit « totale ». Ici la réaction est limitée. Réessaie."),
            ("الجواب هو l'équation ب la double flèche: la réaction محدودة.", "Réponse : C₂H₅COOH + H₂O ⇌ C₂H₅COO⁻ + H₃O⁺.")),
        2: (("لا، ما كاينش les ions hydroxyde فالمحلول ديالنا: l'acide غير فالما. شكون كياخد le proton؟ عاود اختار.", "Il n'y a pas d'ions HO⁻ ajoutés : c'est l'eau qui capte le proton. Réessaie."),
            ("الجواب: الما هو اللي كياخد le proton وكيولي H trois O plus.", "Réponse : C₂H₅COOH + H₂O ⇌ C₂H₅COO⁻ + H₃O⁺."))},
      "Quelle est l'équation de la réaction de l'acide propanoïque avec l'eau ?"),
  qcm("fa_2", "Plus facile : du pH à la concentration", "سؤال ساهل: من le p H ل la concentration.",
      "pH = 3,09. La concentration [H₃O⁺] vaut…",
      ["10^(−3,09) ≈ 8,1 × 10⁻⁴ mol/L", "−log(3,09) ≈ −0,49 mol/L", "10^(3,09) ≈ 1,2 × 10³ mol/L"], 0, {
        0: ("juste", "برافو! la concentration égale dix puissance moins p H.", "Juste : [H₃O⁺] = 10^(−pH)."),
        1: (("ما تقلقش. log كيعطي le p H من la concentration، ماشي العكس. و concentration ما تكونش سالبة. عاود اختار.", "Une concentration n'est jamais négative ; log va dans l'autre sens. Réessaie."),
            ("الجواب: la concentration égale dix puissance moins p H.", "Réponse : [H₃O⁺] = 10^(−3,09) ≈ 8,1 × 10⁻⁴ mol/L.")),
        2: (("قريب! ولكن نسيتي le signe moins. mille mole par litre كبيرة بزاف. عاود اختار.", "Il manque le signe moins de l'exposant. Réessaie."),
            ("الجواب: dix puissance moins p H، ب le signe moins.", "Réponse : 10^(−3,09) ≈ 8,1 × 10⁻⁴ mol/L."))},
      "p H égale trois virgule zéro neuf. La concentration des ions H trois O plus vaut ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "Acide propanoïque à l'équilibre.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("[C₂H₅COO⁻]éq = [H₃O⁺]éq, car ils se forment ensemble.", True, "Dans le tableau, les deux produits valent x."),
      ("[C₂H₅COOH]éq = [H₃O⁺]éq.", False, "L'acide restant vaut C − [H₃O⁺]éq, presque C ici."),
      ("[C₂H₅COOH]éq = C − [H₃O⁺]éq.", True, "L'acide a perdu ce qui s'est formé.")]),
  qcm("fa_4", "Plus facile : la constante d'équilibre", "سؤال ساهل على la constante d'équilibre.",
      "À l'équilibre, Qr,éq = 1,3 × 10⁻⁵. Que vaut K ?",
      ["K = 1/1,3 × 10⁻⁵", "K = 1,3 × 10⁻⁵ mol/L", "K = 1,3 × 10⁻⁵"], 2, {
        2: ("juste", "برافو! K égale Q r à l'équilibre، و بلا وحدة.", "Juste : K = Qr,éq = 1,3 × 10⁻⁵, sans unité."),
        0: (("لا، un sur K هي ديال la réaction inverse. هنا نفس l'équation. عاود اختار.", "L'inverse est la constante de la réaction inverse. Réessaie."),
            ("الجواب: K égale Q r à l'équilibre، un virgule trois fois dix puissance moins cinq.", "Réponse : K = Qr,éq = 1,3 × 10⁻⁵.")),
        1: (("القيمة صحيحة، ولكن شوف l'unité: واش K عندها وحدة؟ عاود اختار.", "La valeur est bonne, mais K n'a pas d'unité. Réessaie."),
            ("الجواب: K égale un virgule trois fois dix puissance moins cinq، بلا وحدة.", "Réponse : K = 1,3 × 10⁻⁵, sans unité."))},
      "À l'équilibre، Q r à l'équilibre égale un virgule trois fois dix puissance moins cinq. Que vaut K ?"),
]

SIM_Q = [
  QS("1", "Écrire l'équation de la réaction de l'acide propanoïque avec l'eau.",
     phrase(EQ), (["⇌", "H₃O⁺"], ["→"]),
     [(EQ, "la double flèche")],
     EQ_DIT + "، ب la double flèche."),
  QS("2", "Calculer [H₃O⁺]éq.",
     val("[H₃O⁺]éq", sH, "mol/L", f"[H₃O⁺]éq = 10^(−3,44) = {sci(sH, 1)} mol/L"),
     (["[H₃O⁺] = 10^(−pH)"], ["[H₃O⁺] = 10^(pH)"]),
     [(f"[H₃O⁺]éq = 10^(−3,44) = {sci(sH, 1)} mol/L", "dix puissance moins trois virgule quarante-quatre")],
     f"la concentration égale dix puissance moins trois virgule quarante-quatre، يعني {dsci(sH, 1)} mole par litre."),
  QS("3", "Déterminer [C₂H₅COO⁻]éq et [C₂H₅COOH]éq.",
     val("[C₂H₅COOH]éq", sA, "mol/L", f"[C₂H₅COO⁻]éq = {sci(sH, 1)} mol/L ; [C₂H₅COOH]éq = 1,0 × 10⁻² − {sci(sH, 1)} = {sci(sA, 1)} mol/L"),
     (["C − [H₃O⁺]éq"], ["[C₂H₅COOH]éq = [H₃O⁺]éq"]),
     [(f"[C₂H₅COO⁻]éq = [H₃O⁺]éq = {sci(sH, 1)} mol/L", "نفس التركيز"),
      (f"[C₂H₅COOH]éq = {sci(sA, 1)} mol/L", f"{dsci(sA, 1)} mole par litre")],
     f"les ions propanoate عندهم نفس التركيز ديال les ions H trois O plus. و l'acide: un virgule zéro fois dix puissance moins deux، moins {dsci(sH, 1)}، يعني {dsci(sA, 1)} mole par litre."),
  QS("4", "Calculer Qr,éq et en déduire K.",
     val("K", sQR, None, f"K = Qr,éq = ({sci(sH, 1)})²/{sci(sA, 1)} = {sci(sQR, 1)}", tol=0.05),
     (["K = Qr,éq"], ["mol/L"]),
     [(f"K = Qr,éq = ({sci(sH, 1)})²/{sci(sA, 1)} = {sci(sQR, 1)}", f"{dsci(sQR, 1)}")],
     f"K égale Q r à l'équilibre، {dsci(sH, 1)}، au carré، sur {dsci(sA, 1)}، يعني {dsci(sQR, 1)}، بلا وحدة. نفس K تقريبا ديال l'exercice: K ما كتتعلقش ب C."),
]

EX = exercice(
  "phys_ex_ch12_etat_equilibre_2", "phys_ch12_etat_equilibre", "etat_equilibre",
  "Une solution d'acide propanoïque : du pH à la constante K", "facile", 15,
  ["Écrire l'équation d'un acide avec l'eau", "Calculer [H₃O⁺]éq à partir du pH", "Déterminer les concentrations à l'équilibre", "Calculer Qr,éq et en déduire K"],
  "On prépare une solution aqueuse d'acide propanoïque C₂H₅COOH de concentration C = 5,0 × 10⁻² mol/L. À 25 °C, la mesure du pH de cette solution donne pH = 3,09. La réaction de l'acide avec l'eau est rapide : le pH mesuré est celui de l'état d'équilibre.",
  "دابا نقراو l'énoncé. عندنا solution ديال l'acide propanoïque، la concentration ديالها C égale cinq virgule zéro fois dix puissance moins deux mole par litre. le p H mètre كيعطي trois virgule zéro neuf. la réaction ديال l'acide مع الما سريعة: le p H اللي قرينا هو le p H à l'équilibre.",
  [], ["C = 5,0 × 10⁻² mol/L", "pH = 3,09 à 25 °C", "[H₃O⁺] = 10^(−pH)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Une solution d'acide propanoïque de concentration C = 1,0 × 10⁻² mol/L a un pH = 3,44 à 25 °C (pH de l'état d'équilibre).",
  "نفس التمرين، بقيم أخرى: C égale un virgule zéro fois dix puissance moins deux mole par litre، و le p H égale trois virgule quarante-quatre.",
  [], ["C = 1,0 × 10⁻² mol/L", "pH = 3,44 à 25 °C"],
  SIM_Q)

ecrire(EX)
