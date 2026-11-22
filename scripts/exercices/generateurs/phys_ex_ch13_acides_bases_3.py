# Exercice de chimie, ch. 13 (réactions acido-basiques), niveau moyen (celui du national) : dosage pH-métrique
# d'une solution d'acide méthanoïque par la soude — équation, équivalence par les tangentes, C_A, indicateur,
# puis « montrer que » sur le rapport [A⁻]/[AH] avant l'équivalence et espèce prédominante.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2016 N (1.1 V_BE et pH_E, 1.3 C_A, 1.4 indicateur, 1.5 espèce prédominante),
#    2018 N (1.1 à 1.5, rapport [A⁻]/[AH] à V_B = 10 mL), 2021 N (1.1 à 1.3 et 3 rapport donné),
#    2022 N (2.1 à 2.5), 2024 N (5-2 « montrer que » le rapport à V_B < V_BE) — backend/data/exams/physique ;
#  - profs (architecture/phys_ch13_acides_bases.md § 1 : Naceiri Mrabti — titrage, tangentes, dérivée, choix de
#    l'indicateur ; Prof Bazhar, vidéo du dosage) ; pièges relevés : prendre la zone de virage qui « touche » pH_E,
#    oublier que V_B est versé (n = C_B·V_B), écrire une double flèche pour la réaction de dosage ;
#  - séries en ligne repérées (titres et résumés lus ; PDF non ouverts, hôtes hors du réseau de la session) :
#    talamidi « transformations liées à des réactions acide-base » exercices 2 et 5 ; moutamadris fiches 13-7, 13-8
#    et 17-2 ; pc1.ma exercices Pr. Chargui ; alloschool El Goufifa ; coursdusoirpc (TD 2 BAC BIOF).
# Ici : acide méthanoïque (le cours dose l'acide éthanoïque à 1,0 × 10⁻² mol/L par 1,0 × 10⁻²), nos volumes et
# concentrations ; la courbe est calculée (bilan des charges) par courbe_ph.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch13 import *

PKA = 3.75
VA, CB, CA = 20.0, 2.0e-2, 1.5e-2
VBE = CA * VA / CB
PHE = ph_dosage(VA, CA, CB, VBE, PKA)
V5 = 6.0
R5 = CB * V5 / (CA * VA - CB * V5)
PH5 = ph_dosage(VA, CA, CB, V5, PKA)
assert abs(VBE - 15.0) < 1e-9 and 7.7 < PHE < 8.0 and abs(R5 - 2 / 3) < 1e-9 and PH5 < PKA

sVA, sCB, sCA = 10.0, 1.0e-2, 2.0e-2
sVBE = sCA * sVA / sCB
sPHE = ph_dosage(sVA, sCA, sCB, sVBE, PKA)
sV5 = 5.0
sR5 = sCB * sV5 / (sCA * sVA - sCB * sV5)
assert abs(sVBE - 20.0) < 1e-9 and 7.2 < sPHE < 8.8 and abs(sR5 - 1 / 3) < 1e-9

FIG = fig_ph("pH du mélange en fonction du volume V_B de soude versé", VA, CA, CB, 30, PKA, True,
             [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30], legende="Trace toi-même les tangentes pour trouver le point d'équivalence E.")
sFIG = fig_ph("pH du mélange en fonction du volume V_B de soude versé", sVA, sCA, sCB, 30, PKA, True, [0, 5, 10, 15, 20, 25, 30])

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction du dosage.",
    "السؤال un: كتب l'équation ديال la réaction du dosage.",
    phrase("HCOOH(aq) + HO⁻(aq) → HCOO⁻(aq) + H₂O(l) (simple flèche : réaction rapide, totale et unique)"),
    (["HCOOH", "HO⁻", "HCOO⁻", "H₂O", "→"], ["H₃O⁺", "⇌", "Na⁺"]),
    [("Le réactif titrant est la soude : quelle espèce de la soude réagit avec l'acide ? Les ions Na⁺ sont spectateurs.",
      "la solution titrante هي la soude. شكون فيها اللي كيتفاعل مع l'acide؟ les ions sodium ما كيتفاعلوش."),
     ("L'acide HCOOH cède un proton aux ions HO⁻ ; la réaction du dosage s'écrit avec une simple flèche.",
      "l'acide méthanoïque كيعطي un proton ل les ions H O moins. و la réaction du dosage كنكتبوها ب simple flèche.")],
    [("1 : HCOOH(aq) + HO⁻(aq) → HCOO⁻(aq) + H₂O(l)", "l'équation: l'acide méthanoïque، plus les ions H O moins")],
    "السؤال un. l'équation: l'acide méthanoïque، plus les ions H O moins، simple flèche، les ions méthanoate، plus l'eau. simple flèche حيت la réaction du dosage rapide، totale و unique.",
    "ex_1", "fa_1"),
  Q("2", "Déterminer graphiquement, par la méthode des tangentes, les coordonnées V_BE et pH_E du point d'équivalence.",
    "السؤال deux: حدد على la courbe، ب la méthode des tangentes، V B E و p H E ديال le point d'équivalence.",
    val("V_BE", VBE, "mL", "pH_E ≈ 7,8 ; V_BE = 15,0 mL", tol=0.03),
    (["tangentes parallèles", "droite médiane", "E", "mL"], ["V_BE = 7,5 mL", "pH_E = 7"]),
    [("Repère le saut de pH : le point d'équivalence E est au milieu du saut.",
      "قلب على le saut de p H: le point d'équivalence E كاين فالوسط ديالو."),
     ("Trace deux tangentes parallèles, avant et après le saut, puis la parallèle à égale distance : elle coupe la courbe en E. Lis V_BE en bas et pH_E à gauche.",
      "رسم deux tangentes parallèles، قبل و من بعد le saut، ومن بعد la parallèle فالوسط. فين كتقطع la courbe هو E. اقرا V B E لتحت، و p H E على اليسار.")],
    [("2 : méthode des tangentes : la médiane coupe la courbe en E", "la parallèle فالوسط"),
     ("V_BE = 15,0 mL", "V B E égale quinze virgule zéro millilitres"),
     ("pH_E ≈ 7,8", "p H E environ sept virgule huit")],
    "السؤال deux. كنرسمو deux tangentes parallèles، قبل و من بعد le saut، و la parallèle فالوسط كتقطع la courbe ف E. نقراو: V B E égale quinze virgule zéro millilitres، و p H E environ sept virgule huit.",
    "ex_2", "fa_2"),
  Q("3", "Calculer la concentration C_A de la solution d'acide méthanoïque.",
    "السؤال trois: حسب la concentration C A ديال l'acide méthanoïque.",
    val("C_A", CA, "mol/L", "C_A = C_B·V_BE/V_A = 2,0 × 10⁻² × 15,0/20,0 = 1,5 × 10⁻² mol/L"),
    (["C_A·V_A = C_B·V_BE", "V_BE", "mol/L"], ["C_A = C_B·V_A/V_BE", "C_A·V_BE = C_B·V_A"]),
    [("À l'équivalence, les réactifs sont dans les proportions stœchiométriques : la quantité d'acide initiale égale la quantité d'ions HO⁻ versés.",
      "عند l'équivalence، les réactifs dans les proportions stœchiométriques: la quantité d'acide initiale، égale la quantité d'ions H O moins versés."),
     ("C_A·V_A = C_B·V_BE, donc C_A = C_B·V_BE/V_A (les deux volumes dans la même unité).",
      "C A fois V A égale C B fois V B E، إذن C A égale C B fois V B E، sur V A.")],
    [("3 : à l'équivalence, C_A·V_A = C_B·V_BE", "C A fois V A égale C B fois V B E"),
     ("C_A = 2,0 × 10⁻² × 15,0/20,0", "deux virgule zéro fois dix puissance moins deux، fois quinze، sur vingt"),
     ("C_A = 1,5 × 10⁻² mol/L", "un virgule cinq fois dix puissance moins deux")],
    "السؤال trois. عند l'équivalence، C A fois V A égale C B fois V B E. إذن C A égale C B fois V B E sur V A. l'application numérique: deux virgule zéro fois dix puissance moins deux، fois quinze، sur vingt. C A égale un virgule cinq fois dix puissance moins deux، mole par litre.",
    "ex_3", "fa_3"),
  Q("4", "Choisir, en justifiant, l'indicateur coloré adéquat pour repérer l'équivalence (tableau des zones de virage).",
    "السؤال quatre: اختار، و برر، l'indicateur coloré المناسب باش نعرفو l'équivalence.",
    phrase("Le rouge de crésol : sa zone de virage 7,2 – 8,8 contient pH_E ≈ 7,8."),
    (["zone de virage", "pH_E", "contient"], ["BBT", "hélianthine"]),
    [("Le bon indicateur change de couleur exactement à l'équivalence : compare pH_E à chaque zone de virage.",
      "l'indicateur المزيان كيبدل اللون عند l'équivalence بالضبط. قارن p H E مع كل zone de virage."),
     ("La zone de virage doit contenir pH_E ≈ 7,8 ; le BBT (6,0 – 7,6) vire avant l'équivalence.",
      "la zone de virage خاصها تحتوي p H E، environ sept virgule huit. le B B T، من six حتى sept virgule six، كيبدل قبل l'équivalence.")],
    [("4 : la zone de virage doit contenir pH_E ≈ 7,8", "la zone de virage خاصها تحتوي p H E"),
     ("le rouge de crésol (7,2 – 8,8) convient", "le rouge de crésol")],
    "السؤال quatre. la zone de virage خاصها تحتوي p H E، environ sept virgule huit. le rouge de crésol، de sept virgule deux à huit virgule huit، كيحتويه. إذن l'indicateur المناسب هو le rouge de crésol. le B B T كيبدل قبل l'équivalence.",
    "ex_4", "fa_4"),
  Q("5", "Pour V_B = 6,0 mL, montrer à l'aide du tableau d'avancement que [HCOO⁻]/[HCOOH] = C_B·V_B/(C_A·V_A − C_B·V_B). Calculer ce rapport et en déduire l'espèce prédominante.",
    "السؤال cinq: من أجل V B égale six millilitres، بين ب le tableau d'avancement بلي le rapport، الميثانوات على l'acide، égale C B V B، sur C A V A moins C B V B. حسبو، و استنتج l'espèce prédominante.",
    val("[HCOO⁻]/[HCOOH]", R5, None, "[HCOO⁻]/[HCOOH] = 2,0 × 10⁻² × 6,0/(1,5 × 10⁻² × 20,0 − 2,0 × 10⁻² × 6,0) = 0,67 < 1 : HCOOH prédomine"),
    (["x_f = C_B·V_B", "C_A·V_A − x_f", "même volume", "prédomine"], ["C_B·V_BE", "[HCOO⁻] = [HCOOH]"]),
    [("Avant l'équivalence, les ions HO⁻ versés sont limitants et la réaction est totale : que vaut x_f ?",
      "قبل l'équivalence، les ions H O moins هوما le réactif limitant، و la réaction totale. شحال كتساوي x f؟"),
     ("x_f = C_B·V_B : il s'est formé x_f ions HCOO⁻ et il reste C_A·V_A − x_f d'acide, dans le même volume total : les volumes se simplifient.",
      "x f égale C B fois V B. تكونو x f ديال les ions méthanoate، و بقا C A V A moins x f ديال l'acide، فنفس le volume total. إذن le volume كيتحيد فle rapport.")],
    [("5 : avant l'équivalence HO⁻ est limitant : x_f = C_B·V_B", "x f égale C B fois V B"),
     ("n(HCOO⁻) = C_B·V_B ; n(HCOOH) = C_A·V_A − C_B·V_B, même volume V_A + V_B", "نفس le volume"),
     ("[HCOO⁻]/[HCOOH] = 1,2 × 10⁻⁴/1,8 × 10⁻⁴ = 0,67", "le rapport égale zéro virgule soixante-sept"),
     ("0,67 < 1 : HCOOH prédomine", "l'acide méthanoïque prédomine")],
    "السؤال cinq. قبل l'équivalence، les ions H O moins limitant، إذن x f égale C B fois V B. les ions méthanoate: C B fois V B. l'acide اللي بقا: C A fois V A moins C B fois V B. و les deux فنفس le volume، إذن le volume كيتحيد. l'application numérique: un virgule deux fois dix puissance moins quatre، sur un virgule huit fois dix puissance moins quatre. le rapport égale zéro virgule soixante-sept، صغر من un. إذن l'acide méthanoïque prédomine. و la courbe كتأكد: le p H ف six millilitres صغر من p K a.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : la réaction du dosage", "Chaque ion HO⁻ versé prend un proton à l'acide : simple flèche.",
      "acides-bases-tableau/dosage.html?vue=reaction", "Les ions hydroxyde et l'acide, à la loupe",
      "شوف la loupe: كل ion hydroxyde H O moins كيطيح، كياخد un proton H plus من molécule ديال l'acide. فla simulation، l'acide éthanoïque. هاد la réaction فيها trois conditions. rapide: كتوقع ف الحين. totale: كتكمل حتى يسالي واحد من les réactifs. unique: ماكاينش réaction أخرى. لهذا simple flèche. فالتمرين ديالنا، l'acide méthanoïque: l'acide méthanoïque، plus les ions H O moins، simple flèche، les ions méthanoate، plus l'eau.",
      [("HCOOH + HO⁻ → HCOO⁻ + H₂O", "فالتمرين ديالنا، l'acide méthanoïque")],
      [("شوف la loupe", "moment:loupe"), ("هاد la réaction فيها trois conditions", "moment:equation"),
       ("rapide: كتوقع", "moment:rapide"), ("totale: كتكمل", "moment:totale"), ("unique: ماكاينش", "moment:unique")]),
  sim("ex_2", "Question 2 : la méthode des tangentes", "Deux tangentes parallèles, la médiane : elle coupe la courbe en E.",
      "acides-bases-tableau/dosage.html?vue=tangentes", "Le point d'équivalence par les tangentes",
      "هادي la courbe ديال la simulation. الخطوة اللولى: نرسمو une tangente قبل le saut. الخطوة الثانية: une tangente أخرى من بعد le saut، parallèle للأولى. الخطوة الثالثة: une parallèle فالوسط، à égale distance ديال deux tangentes. فين كتقطع la courbe، هو le point d'équivalence E. فla simulation: V B E égale vingt virgule zéro millilitres. فالتمرين ديالنا، نفس الخطوات على la courbe ديال l'énoncé: V B E égale quinze virgule zéro millilitres، و p H E environ sept virgule huit.",
      [("V_BE = 15,0 mL", "V B E égale quinze virgule zéro millilitres"), ("pH_E ≈ 7,8", "و p H E environ sept virgule huit")],
      [("هادي la courbe ديال la simulation", "moment:courbe"), ("الخطوة اللولى", "moment:tangente_1"), ("الخطوة الثانية", "moment:tangente_2"),
       ("الخطوة الثالثة", "moment:mediane"), ("فين كتقطع la courbe", "moment:point_e"), ("فla simulation: V B E", "moment:lecture")]),
  sim("ex_3", "Question 3 : C_A·V_A = C_B·V_BE", "À l'équivalence, la quantité d'acide initiale égale la quantité d'ions HO⁻ versés.",
      "acides-bases-tableau/dosage.html?vue=equivalence", "Le tableau d'avancement à l'équivalence",
      "شوف le tableau d'avancement ديال la réaction de dosage. قبل l'équivalence، باقي شي acide ف le bécher. عند l'équivalence، deux réactifs كيساليو مع بعض. من بعد، les ions hydroxyde en excès. la définition: à l'équivalence، les réactifs sont، dans les proportions stœchiométriques. إذن la relation: C A fois V A égale C B fois V B E. فالتمرين ديالنا: C A égale C B fois V B E sur V A، يعني deux virgule zéro fois dix puissance moins deux، fois quinze، sur vingt، égale un virgule cinq fois dix puissance moins deux، mole par litre.",
      [("C_A·V_A = C_B·V_BE", "إذن la relation"), ("C_A = 1,5 × 10⁻² mol/L", "égale un virgule cinq fois dix puissance moins deux")],
      [("شوف le tableau d'avancement", "moment:tableau"), ("قبل l'équivalence", "moment:avant"), ("عند l'équivalence، deux réactifs", "moment:a_equivalence"),
       ("من بعد، les ions hydroxyde", "moment:apres"), ("la définition", "moment:definition"), ("إذن la relation", "moment:relation")]),
  sim("ex_4", "Question 4 : la zone de virage doit contenir pH_E", "On choisit l'indicateur dont la zone de virage contient pH_E.",
      "acides-bases-tableau/exploiter.html?vue=indicateur", "Quatre indicateurs sur l'axe des pH",
      "هادي la courbe ديال la simulation، و p H E égale huit virgule trois. دابا شوف les bandes ديال quatre indicateurs على l'axe des p H: l'hélianthine، le rouge de méthyle، le B B T، و le rouge de crésol. le rouge de crésol، de sept virgule deux à huit virgule huit، contient p H E. رد البال: le B B T كيبدل اللون قبل l'équivalence. نعاود نقرا la règle: la zone de virage de l'indicateur، doit contenir p H E. فالتمرين ديالنا، p H E environ sept virgule huit: هو تاني le rouge de crésol.",
      [("7,2 < pH_E ≈ 7,8 < 8,8", "فالتمرين ديالنا، p H E environ sept virgule huit"), ("rouge de crésol", "هو تاني le rouge de crésol")],
      [("هادي la courbe ديال la simulation", "moment:courbe"), ("دابا شوف les bandes", "moment:bandes"), ("le rouge de crésol، de sept", "moment:choix"),
       ("رد البال", "moment:piege"), ("نعاود نقرا la règle", "moment:regle")]),
  sim("ex_5", "Question 5 : avant l'équivalence, le tableau donne le rapport", "x_f = C_B·V_B ; il reste C_A·V_A − C_B·V_B d'acide, dans le même volume.",
      "acides-bases-tableau/exploiter.html?vue=demi", "Le tableau d'avancement avant l'équivalence",
      "نرجعو ل la courbe ديال la simulation: l'acide éthanoïque dosé par la soude. شوف le tableau: la soude اللي طاحت، C B fois V B، كتعطي نفس الكمية ديال la base. و l'acide اللي بقا، C A fois V A، moins C B fois V B. فla simulation، فالنص، les deux quantités متساويين. فالتمرين ديالنا، ف six millilitres: la base، un virgule deux fois dix puissance moins quatre mole، و l'acide اللي بقا، un virgule huit fois dix puissance moins quatre mole. نفس le volume، إذن le rapport égale zéro virgule soixante-sept، صغر من un: l'acide méthanoïque prédomine.",
      [("[HCOO⁻]/[HCOOH] = C_B·V_B/(C_A·V_A − C_B·V_B)", "شوف le tableau"), ("= 1,2/1,8 = 0,67 < 1", "إذن le rapport égale zéro virgule soixante-sept")],
      [("نرجعو ل la courbe", "moment:courbe"), ("شوف le tableau", "moment:tableau"), ("فla simulation، فالنص", "moment:egalite")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : l'équation du dosage", "نتمرنو بسؤال ساهل. اختار l'équation الصحيحة.",
      "Quelle est l'équation de la réaction du dosage de l'acide méthanoïque par la soude ?",
      ["HCOOH + H₂O ⇌ HCOO⁻ + H₃O⁺", "HCOOH + HO⁻ → HCOO⁻ + H₂O", "HCOOH + Na⁺ → HCOONa + H⁺"], 1, {
        1: ("juste", "برافو! les ions H O moins ديال la soude كياخدو un proton من l'acide، و la réaction totale، simple flèche.", "Juste : HCOOH + HO⁻ → HCOO⁻ + H₂O."),
        0: (("هادي la réaction ديال l'acide مع الما، ماشي مع la soude. شكون فla soude اللي كيتفاعل؟ عاود اختار.", "C'est la réaction de l'acide avec l'eau, pas avec la soude. Réessaie."),
            ("الجواب هو l'acide méthanoïque plus H O moins، simple flèche، les ions méthanoate plus l'eau.", "Réponse : HCOOH + HO⁻ → HCOO⁻ + H₂O.")),
        2: (("les ions sodium spectateurs، ما كيتفاعلوش. عاود اختار.", "Les ions Na⁺ sont spectateurs. Réessaie."),
            ("الجواب هو مع les ions H O moins: les ions sodium ما كيتفاعلوش.", "Réponse : HCOOH + HO⁻ → HCOO⁻ + H₂O ; Na⁺ est spectateur."))},
      "Quelle est l'équation de la réaction du dosage, de l'acide méthanoïque par la soude ?"),
  vf("fa_2", "Plus facile : vrai ou faux", "La méthode des tangentes.", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Les deux tangentes, avant et après le saut, sont parallèles.", True, "C'est la méthode : deux tangentes parallèles, puis la droite à égale distance."),
      ("Le point d'équivalence d'un acide faible dosé par la soude a toujours pH_E = 7.", False, "pH_E = 7 pour un acide fort ; ici la solution contient HCOO⁻, une base : pH_E > 7."),
      ("V_BE se lit sur l'axe des volumes, sous le point E.", True, "On descend de E jusqu'à l'axe horizontal.")]),
  qcm("fa_3", "Plus facile : C_A", "سؤال ساهل على la relation d'équivalence.",
      "V_A = 20,0 mL, C_B = 2,0 × 10⁻² mol/L, V_BE = 15,0 mL. C_A vaut…",
      ["2,7 × 10⁻² mol/L", "1,5 × 10⁻² mol/L", "6,0 × 10⁻³ mol/L"], 1, {
        1: ("juste", "برافو! C A égale C B fois V B E sur V A، يعني un virgule cinq fois dix puissance moins deux.", "Juste : C_A = C_B·V_BE/V_A = 1,5 × 10⁻² mol/L."),
        0: (("قلبتي les volumes: هاد القيمة كتجي من C B fois V A sur V B E. عاود اختار.", "Les volumes sont inversés. Réessaie."),
            ("الجواب هو un virgule cinq fois dix puissance moins deux: C A fois V A égale C B fois V B E.", "Réponse : C_A = C_B·V_BE/V_A = 1,5 × 10⁻² mol/L.")),
        2: (("شوف: هاد القيمة ما كتجي من حتى relation ديال l'équivalence. بدا من C A fois V A égale C B fois V B E. عاود اختار.", "Pars de C_A·V_A = C_B·V_BE. Réessaie."),
            ("الجواب هو un virgule cinq fois dix puissance moins deux mole par litre.", "Réponse : C_A = 2,0 × 10⁻² × 15,0/20,0 = 1,5 × 10⁻² mol/L."))},
      "V A égale vingt millilitres، C B égale deux virgule zéro fois dix puissance moins deux mole par litre، V B E égale quinze millilitres. C A vaut ?"),
  qcm("fa_4", "Plus facile : l'indicateur", "سؤال ساهل: اختار l'indicateur.",
      "pH_E ≈ 7,8. Quel indicateur convient ?",
      ["BBT (6,0 – 7,6)", "Hélianthine (3,1 – 4,4)", "Rouge de crésol (7,2 – 8,8)"], 2, {
        2: ("juste", "برافو! la zone de virage ديال le rouge de crésol كتحتوي sept virgule huit.", "Juste : 7,2 < 7,8 < 8,8."),
        0: (("قريب! ولكن la zone ديال le B B T كتوقف ف sept virgule six، قبل sept virgule huit. عاود اختار.", "La zone du BBT s'arrête à 7,6 : il vire avant l'équivalence. Réessaie."),
            ("الجواب هو le rouge de crésol: la zone ديالو كتحتوي p H E.", "Réponse : le rouge de crésol (7,2 – 8,8) contient pH_E.")),
        1: (("l'hélianthine كتبدل ف p H acide، بعيد بزاف على sept virgule huit. عاود اختار.", "L'hélianthine vire en milieu acide, loin de 7,8. Réessaie."),
            ("الجواب هو le rouge de crésol، حيت la zone ديالو كتحتوي p H E.", "Réponse : le rouge de crésol."))},
      "p H E environ sept virgule huit. Quel indicateur convient ?"),
  vf("fa_5", "Plus facile : vrai ou faux", "V_B = 6,0 mL < V_BE = 15,0 mL.", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Avant l'équivalence, les ions HO⁻ versés sont le réactif limitant.", True, "Il reste de l'acide dans le bécher : HO⁻ est épuisé à chaque ajout."),
      ("À V_B = 6,0 mL, n(HCOO⁻) = C_B·V_B = 1,2 × 10⁻⁴ mol.", True, "2,0 × 10⁻² × 6,0 × 10⁻³ = 1,2 × 10⁻⁴ mol."),
      ("Le rapport [HCOO⁻]/[HCOOH] = 0,67 montre que la base prédomine.", False, "0,67 < 1 : c'est l'acide HCOOH qui prédomine.")]),
]

SIM_Q = [
  QS("1", "Écrire l'équation de la réaction du dosage.",
     phrase("HCOOH(aq) + HO⁻(aq) → HCOO⁻(aq) + H₂O(l)"),
     (["HO⁻", "→"], ["⇌", "H₃O⁺"]),
     [("HCOOH + HO⁻ → HCOO⁻ + H₂O", "simple flèche")],
     "l'acide méthanoïque، plus les ions H O moins، simple flèche، les ions méthanoate، plus l'eau."),
  QS("2", "Déterminer V_BE et pH_E par la méthode des tangentes.",
     val("V_BE", sVBE, "mL", "pH_E ≈ 7,8 ; V_BE = 20,0 mL"),
     (["tangentes", "E", "mL"], ["V_BE = 10,0 mL"]),
     [("V_BE = 20,0 mL ; pH_E ≈ 7,8", "V B E égale vingt virgule zéro")],
     "ب la méthode des tangentes: V B E égale vingt virgule zéro millilitres، و p H E environ sept virgule huit."),
  QS("3", "Calculer C_A.",
     val("C_A", sCA, "mol/L", "C_A = C_B·V_BE/V_A = 1,0 × 10⁻² × 20,0/10,0 = 2,0 × 10⁻² mol/L"),
     (["C_A·V_A = C_B·V_BE", "mol/L"], ["C_A = C_B·V_A/V_BE"]),
     [("C_A = C_B·V_BE/V_A = 1,0 × 10⁻² × 20,0/10,0", "C A égale C B fois V B E sur V A"), ("C_A = 2,0 × 10⁻² mol/L", "deux virgule zéro fois dix puissance moins deux")],
     "C A égale C B fois V B E sur V A، يعني un virgule zéro fois dix puissance moins deux، fois vingt، sur dix. C A égale deux virgule zéro fois dix puissance moins deux، mole par litre."),
  QS("4", "Choisir l'indicateur coloré adéquat. Justifier.",
     phrase("Le rouge de crésol : sa zone de virage 7,2 – 8,8 contient pH_E ≈ 7,8."),
     (["zone de virage", "pH_E"], ["BBT"]),
     [("la zone 7,2 – 8,8 du rouge de crésol contient pH_E", "le rouge de crésol")],
     "la zone de virage ديال le rouge de crésol، de sept virgule deux à huit virgule huit، كتحتوي p H E. إذن le rouge de crésol."),
  QS("5", "Pour V_B = 5,0 mL, montrer que [HCOO⁻]/[HCOOH] = C_B·V_B/(C_A·V_A − C_B·V_B), le calculer et en déduire l'espèce prédominante.",
     val("[HCOO⁻]/[HCOOH]", sR5, None, "[HCOO⁻]/[HCOOH] = 5,0 × 10⁻⁵/(2,0 × 10⁻⁴ − 5,0 × 10⁻⁵) = 0,33 < 1 : HCOOH prédomine"),
     (["x_f = C_B·V_B", "prédomine"], ["C_B·V_BE"]),
     [("x_f = C_B·V_B = 5,0 × 10⁻⁵ mol ; n(HCOOH) = 1,5 × 10⁻⁴ mol", "x f égale C B fois V B"), ("rapport = 0,33 < 1 : HCOOH prédomine", "zéro virgule trente-trois")],
     "قبل l'équivalence، x f égale C B fois V B، يعني cinq virgule zéro fois dix puissance moins cinq mole، و l'acide اللي بقا un virgule cinq fois dix puissance moins quatre mole. le rapport égale zéro virgule trente-trois، صغر من un: l'acide méthanoïque prédomine."),
]

EX = exercice(
  "phys_ex_ch13_acides_bases_3", "phys_ch13_acides_bases", "acides_bases",
  "Dosage pH-métrique d'une solution d'acide méthanoïque", "moyen", 30,
  ["Écrire l'équation d'une réaction de dosage", "Déterminer V_BE et pH_E par la méthode des tangentes", "Calculer C_A à l'équivalence", "Choisir un indicateur coloré", "Exploiter le tableau d'avancement avant l'équivalence"],
  "On dose un volume V_A = 20,0 mL d'une solution S_A d'acide méthanoïque HCOOH, de concentration C_A inconnue, par une solution d'hydroxyde de sodium (Na⁺(aq) + HO⁻(aq)) de concentration C_B = 2,0 × 10⁻² mol/L. Un pH-mètre permet de tracer la courbe pH = f(V_B) de la figure 1. Le tableau de la figure 2 donne les zones de virage de quelques indicateurs colorés. Données à 25 °C : pKa(HCOOH/HCOO⁻) = 3,75 ; Ke = 1,0 × 10⁻¹⁴.",
  "دابا نقراو l'énoncé. كنديرو le dosage ديال vingt virgule zéro millilitres، ديال la solution S A، ديال l'acide méthanoïque. la concentration ديالها C A ما معروفاش. la solution titrante هي la soude، C B égale deux virgule zéro fois dix puissance moins deux، mole par litre. ب le p H mètre، رسمنا la courbe ديال le p H en fonction de V B، فla figure un. و la figure deux فيها les zones de virage ديال شي indicateurs colorés. و p K a ديال le couple égale trois virgule soixante-quinze.",
  [FIG, fig_indicateurs()],
  ["V_A = 20,0 mL", "C_B = 2,0 × 10⁻² mol/L", "pKa(HCOOH/HCOO⁻) = 3,75", "Ke = 1,0 × 10⁻¹⁴ à 25 °C"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "On dose V_A = 10,0 mL d'une solution d'acide méthanoïque de concentration C_A par la soude de concentration C_B = 1,0 × 10⁻² mol/L. La figure donne pH = f(V_B). Données : pKa(HCOOH/HCOO⁻) = 3,75 ; zones de virage dans le tableau.",
  "نفس التمرين، بقيم أخرى. dix virgule zéro millilitres ديال l'acide méthanoïque، و la soude، C B égale un virgule zéro fois dix puissance moins deux، mole par litre.",
  [sFIG, fig_indicateurs()],
  ["V_A = 10,0 mL", "C_B = 1,0 × 10⁻² mol/L", "pKa(HCOOH/HCOO⁻) = 3,75"],
  SIM_Q)

ecrire(EX)
