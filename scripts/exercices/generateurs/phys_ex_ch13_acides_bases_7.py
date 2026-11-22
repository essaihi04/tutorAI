# Exercice de chimie, ch. 13 (réactions acido-basiques), niveau supérieur (au-dessus du national, même forme) :
# dosage d'une base faible B (produit ménager dilué) par l'acide chlorhydrique — équation, équivalence et
# concentration du produit avant dilution, pH_E < 7 justifié et indicateur, τ de la réaction du dosage à un point,
# pourcentages des deux formes et pKa, avec un contrôle par la demi-équivalence.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2023 R (2.2 à 2.8 : triméthylamine dosée, « justifier pH_E < 7 », indicateur,
#    rapport par le tableau, pKa), 2024 R (2.1 à 2.4 : R−NH₂ dosée, pH à V_A = 16 mL, τ du dosage), 2020 N (1.1 à 1.4 :
#    ammoniac dosé, C_b puis C₀ après dilution, indicateur), 2022 R (2.1 à 2.5 : méthylamine dosée, rapport
#    [B]/[BH⁺]), 2024 R (1.2.3 pourcentages des formes) — backend/data/exams/physique ;
#  - profs (architecture/phys_ch13_acides_bases.md § 1 : Naceiri Mrabti — « τ du titrage ≈ 1 », choix de
#    l'indicateur ; Prof Bazhar — dosage d'une base, colorimétrie) ; pièges relevés : pH_E = 7 pris par réflexe,
#    oublier le facteur de dilution, τ calculé avec la base au lieu du réactif limitant H₃O⁺ ;
#  - séries en ligne repérées (titres et résumés lus ; PDF non ouverts, hôtes hors du réseau de la session) :
#    talamidi exercices non corrigés 2 et 5, moutamadris fiches 13-7, 13-8 et 17-2, pc1.ma Pr. Chargui,
#    alloschool El Goufifa séance 15.
# Ici : une base notée B (pKa(BH⁺/B) = 9,5), notre dilution, nos volumes, notre courbe calculée (le cours dose
# l'ammoniac à 1,0 × 10⁻² mol/L) ; au-dessus du national : la dilution, τ du dosage et les pourcentages enchaînés.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch13 import *

PKA, F = 9.5, 20
VB, CA = 10.0, 2.0e-2
CB = 3.0e-2
VAE = CB * VB / CA
C0 = F * CB
PHE = ph_dosage(VB, CB, CA, VAE, PKA, acide=False)
V1 = 6.0
PH1 = round(ph_dosage(VB, CB, CA, V1, PKA, acide=False), 2)
XMAX = CA * V1 * 1e-3
RESTE = 10 ** (-PH1) * (VB + V1) * 1e-3
TAU = (XMAX - RESTE) / XMAX
NBH, NB = XMAX, CB * VB * 1e-3 - XMAX
PCT = 100 * NBH / (NBH + NB)
PKA1 = PH1 - math.log10(NB / NBH)
assert abs(VAE - 15.0) < 1e-9 and abs(C0 - 0.60) < 1e-9 and 5.5 < PHE < 6.0 and 4.2 < PHE < 6.2
assert abs(PH1 - 9.67) < 1e-9 and abs(XMAX - 1.2e-4) < 1e-12 and TAU > 0.9999999 and abs(PCT - 40) < 1e-9 and abs(PKA1 - 9.49) < 0.005

sCB = 2.4e-2
sVAE = sCB * VB / CA
sC0 = F * sCB
sV1 = 4.8
sPH1 = round(ph_dosage(VB, sCB, CA, sV1, PKA, acide=False), 2)
sX = CA * sV1 * 1e-3
sNB = sCB * VB * 1e-3 - sX
sPKA1 = sPH1 - math.log10(sNB / sX)
sPHE = ph_dosage(VB, sCB, CA, sVAE, PKA, acide=False)
assert abs(sVAE - 12.0) < 1e-9 and abs(sC0 - 0.48) < 1e-9 and abs(sPH1 - 9.67) < 1e-9 and abs(sPKA1 - 9.49) < 0.005 and 4.2 < sPHE < 6.2

FIG = fig_ph("pH du mélange en fonction du volume V_A d'acide chlorhydrique versé", VB, CB, CA, 25, PKA, False,
             list(range(0, 26, 3)) + [25], nomV="V_A", legende="La courbe descend : on verse un acide sur une base.")
sFIG = fig_ph("pH du mélange en fonction du volume V_A d'acide chlorhydrique versé", VB, sCB, CA, 25, PKA, False,
              list(range(0, 25, 2)), nomV="V_A")

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction du dosage.",
    "السؤال un: كتب l'équation ديال la réaction du dosage.",
    phrase("B(aq) + H₃O⁺(aq) → BH⁺(aq) + H₂O(l)"),
    (["B", "H₃O⁺", "BH⁺", "H₂O", "→"], ["HO⁻", "Cl⁻", "⇌"]),
    [("La solution titrante est l'acide chlorhydrique : quelle espèce y cède un proton ? Les ions Cl⁻ sont spectateurs.",
      "la solution titrante هي l'acide chlorhydrique. شكون فيها اللي كيعطي un proton؟ les ions chlorure spectateurs."),
     ("Les ions H₃O⁺ cèdent un proton à la base B, qui devient BH⁺ ; réaction du dosage : simple flèche.",
      "les ions H trois O plus كيعطيو un proton ل la base B، و كتولي B H plus. و la réaction du dosage ب simple flèche.")],
    [("1 : B(aq) + H₃O⁺(aq) → BH⁺(aq) + H₂O(l)", "la base B، plus H trois O plus")],
    "السؤال un. la base B، plus H trois O plus، simple flèche، B H plus، plus l'eau.",
    "ex_1", "fa_1"),
  Q("2", "Déterminer graphiquement le volume V_AE versé à l'équivalence. En déduire la concentration C_B de S_B, puis la concentration C₀ du produit commercial.",
    "السؤال deux: حدد V A E على la courbe. استنتج C B ديال S B، ومن بعد C zéro ديال le produit قبل la dilution.",
    val("C₀", C0, "mol/L", "V_AE = 15,0 mL ; C_B = C_A·V_AE/V_B = 2,0 × 10⁻² × 15,0/10,0 = 3,0 × 10⁻² mol/L ; C₀ = 20·C_B = 0,60 mol/L"),
    (["tangentes", "C_B·V_B = C_A·V_AE", "C₀ = 20·C_B", "mol/L"], ["C₀ = C_B/20", "C_B = C_A·V_B/V_AE"]),
    [("Méthode des tangentes sur la courbe descendante, puis relation à l'équivalence : la quantité de base initiale égale la quantité d'ions H₃O⁺ versés.",
      "la méthode des tangentes على la courbe اللي كتهبط. من بعد la relation: la quantité de base initiale، égale la quantité d'ions H trois O plus versés."),
     ("C_B·V_B = C_A·V_AE. S_B est 20 fois moins concentrée que le produit : C₀ = 20·C_B.",
      "C B fois V B égale C A fois V A E. و S B مخففة vingt fois، إذن C zéro égale vingt fois C B.")],
    [("2 : méthode des tangentes : V_AE = 15,0 mL", "V A E égale quinze virgule zéro millilitres"),
     ("C_B = C_A·V_AE/V_B = 2,0 × 10⁻² × 15,0/10,0 = 3,0 × 10⁻² mol/L", "C B égale trois virgule zéro fois dix puissance moins deux"),
     ("dilution 20 fois : C₀ = 20·C_B = 0,60 mol/L", "C zéro égale zéro virgule soixante")],
    "السؤال deux. ب la méthode des tangentes، V A E égale quinze virgule zéro millilitres. عند l'équivalence، C B fois V B égale C A fois V A E، إذن C B égale deux virgule zéro fois dix puissance moins deux، fois quinze، sur dix. C B égale trois virgule zéro fois dix puissance moins deux، mole par litre. و le produit مخفف vingt fois، إذن C zéro égale vingt fois C B، يعني C zéro égale zéro virgule soixante mole par litre.",
    "ex_2", "fa_2"),
  Q("3", "Le pH à l'équivalence vaut pH_E ≈ 5,7. Justifier que pH_E < 7, puis choisir l'indicateur coloré adéquat.",
    "السؤال trois: p H E environ cinq virgule sept. برر علاش p H E صغر من sept، و اختار l'indicateur المناسب.",
    phrase("À l'équivalence, B et H₃O⁺ ont réagi ; la solution contient BH⁺ (un acide) et Cl⁻ (spectateur) : elle est acide, pH_E < 7. Le rouge de méthyle (4,2 – 6,2) contient pH_E ≈ 5,7."),
    (["BH⁺ est un acide", "pH_E < 7", "zone de virage", "rouge de méthyle"], ["pH_E = 7", "BBT"]),
    [("À l'équivalence, la base B et les ions H₃O⁺ ont été consommés : quelles espèces restent en solution, et laquelle agit sur le pH ?",
      "عند l'équivalence، la base B و H trois O plus تساليو. شنو بقا فالمحلول؟ و شكون فيهم كيأثر على le p H؟"),
     ("BH⁺ est l'acide conjugué de B : il rend la solution acide. Puis la zone de virage doit contenir pH_E.",
      "B H plus هو l'acide conjugué ديال B: كيخلي la solution acide. من بعد la zone de virage خاصها تحتوي p H E.")],
    [("3 : à l'équivalence, la solution contient BH⁺ (acide) et Cl⁻ (spectateur) : pH_E < 7", "B H plus هو acide"),
     ("le rouge de méthyle, zone de virage 4,2 – 6,2, contient pH_E ≈ 5,7", "le rouge de méthyle")],
    "السؤال trois. عند l'équivalence، ما بقاو غير les ions B H plus و les ions chlorure. les ions chlorure spectateurs، و B H plus هو acide، إذن la solution acide، و p H E صغر من sept. l'indicateur: le rouge de méthyle، de quatre virgule deux à six virgule deux، كيحتوي p H E environ cinq virgule sept.",
    "ex_3", "fa_3"),
  Q("4", "Pour V_A = 6,0 mL, le pH vaut 9,67. Calculer le taux d'avancement final τ de la réaction du dosage à ce point, et conclure.",
    "السؤال quatre: ف V A égale six millilitres، le p H égale neuf virgule soixante-sept. حسب tau ديال la réaction du dosage فهاد النقطة، و استنتج.",
    val("τ", TAU, None, "x_max = C_A·V_A = 1,2 × 10⁻⁴ mol ; n(H₃O⁺)restant = 10^(−9,67) × 16,0 × 10⁻³ = 3,4 × 10⁻¹² mol ; τ = (x_max − n(H₃O⁺)restant)/x_max = 1,00", tol=0.01),
    (["x_max = C_A·V_A", "n(H₃O⁺) = 10^(−pH)·(V_A + V_B)", "τ = x_f/x_max"], ["x_max = C_B·V_B", "τ = 10^(−pH)/C_A"]),
    [("Avant l'équivalence, quel réactif est limitant : la base B du bécher ou les ions H₃O⁺ versés ?",
      "قبل l'équivalence، شكون هو le réactif limitant: la base B ولا les ions H trois O plus اللي طاحو؟"),
     ("x_max = C_A·V_A ; les ions H₃O⁺ restants : [H₃O⁺]·(V_A + V_B) = 10^(−pH)·(V_A + V_B) ; x_f = x_max − ce reste ; τ = x_f/x_max.",
      "x max égale C A fois V A. اللي بقا من H trois O plus: dix puissance moins p H، fois V A plus V B. x f égale x max moins هاد الباقي، و tau égale x f sur x max.")],
    [("4 : H₃O⁺ est limitant : x_max = C_A·V_A = 1,2 × 10⁻⁴ mol", "x max égale C A fois V A"),
     ("n(H₃O⁺)restant = 10^(−9,67) × 16,0 × 10⁻³ = 3,4 × 10⁻¹² mol", "trois virgule quatre fois dix puissance moins douze"),
     ("τ = (x_max − n(H₃O⁺)restant)/x_max ≈ 1 : la réaction du dosage est totale", "tau environ un")],
    "السؤال quatre. قبل l'équivalence، les ions H trois O plus هوما le réactif limitant: x max égale C A fois V A، يعني un virgule deux fois dix puissance moins quatre mole. اللي بقا منهم: dix puissance moins neuf virgule soixante-sept، fois seize millilitres، يعني trois virgule quatre fois dix puissance moins douze mole، والو تقريبا. إذن x f égale x max تقريبا، و tau environ un: la réaction du dosage totale.",
    "ex_4", "fa_4"),
  Q("5", "Toujours pour V_A = 6,0 mL : calculer le pourcentage de la forme acide BH⁺ des deux formes du couple, puis en déduire le pKa du couple BH⁺/B. Contrôler ce résultat par une lecture sur la courbe.",
    "السؤال cinq: ف V A égale six millilitres، حسب le pourcentage ديال la forme acide B H plus، و استنتج p K a. و تحقق ب قراءة على la courbe.",
    val("pKa", PKA1, None, "n(BH⁺) = 1,2 × 10⁻⁴ mol ; n(B) = 3,0 × 10⁻⁴ − 1,2 × 10⁻⁴ = 1,8 × 10⁻⁴ mol ; %BH⁺ = 40 % ; pKa = pH − log([B]/[BH⁺]) = 9,67 − log 1,5 = 9,49", tol=0.01),
    (["n(BH⁺) = x_f", "n(B) = C_B·V_B − x_f", "pH = pKa + log([B]/[BH⁺])", "V_AE/2"], ["%BH⁺ = 60 %", "pKa = pH"]),
    [("D'après le tableau du dosage : il s'est formé x_f = C_A·V_A ions BH⁺, et il reste C_B·V_B − x_f de base B, dans le même volume.",
      "من le tableau: تكونو x f égale C A fois V A ديال B H plus، و بقا C B V B moins x f ديال la base B، فنفس le volume."),
     ("%BH⁺ = n(BH⁺)/(n(BH⁺) + n(B)) ; pKa = pH − log([B]/[BH⁺]). Contrôle : à la demi-équivalence (V_A = V_AE/2), pH = pKa.",
      "le pourcentage égale B H plus sur la somme. و p K a égale p H moins log de B sur B H plus. و للتحقق: ف la demi-équivalence، p H égale p K a.")],
    [("5 : n(BH⁺) = x_f = 1,2 × 10⁻⁴ mol ; n(B) = C_B·V_B − x_f = 1,8 × 10⁻⁴ mol", "x f égale un virgule deux"),
     ("%BH⁺ = 1,2/(1,2 + 1,8) = 40 %", "quarante pour cent"),
     ("pKa = pH − log([B]/[BH⁺]) = 9,67 − log 1,5 = 9,49 ≈ 9,5", "p K a environ neuf virgule cinq"),
     ("contrôle : à V_A = V_AE/2 = 7,5 mL, on lit pH ≈ 9,5 = pKa", "sept virgule cinq millilitres")],
    "السؤال cinq. من le tableau: B H plus، x f égale un virgule deux fois dix puissance moins quatre mole. و la base B اللي بقات: trois virgule zéro moins un virgule deux، يعني un virgule huit fois dix puissance moins quatre mole. le pourcentage ديال B H plus: un virgule deux، sur trois، يعني quarante pour cent. نفس le volume، إذن p K a égale p H moins log de un virgule cinq، يعني neuf virgule soixante-sept moins zéro virgule dix-huit. p K a environ neuf virgule cinq. التحقق: ف la demi-équivalence، sept virgule cinq millilitres، la courbe كتعطي p H environ neuf virgule cinq.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : une base dosée par un acide fort", "Les ions H₃O⁺ versés cèdent un proton à la base : simple flèche.",
      "acides-bases-tableau/exploiter.html?vue=base", "L'ammoniac dosé par l'acide chlorhydrique",
      "دابا كنقلبو: ف le bécher، فla simulation، l'ammoniac، و ف la burette l'acide chlorhydrique. la réaction de dosage: N H trois plus H trois O plus، simple flèche، N H quatre plus plus H deux O. فالتمرين ديالنا نفس الشي مع la base B: la base B، plus H trois O plus، simple flèche، B H plus، plus l'eau.",
      [("B + H₃O⁺ → BH⁺ + H₂O", "فالتمرين ديالنا نفس الشي")],
      [("دابا كنقلبو", "moment:montage"), ("la réaction de dosage", "moment:equation")]),
  sim("ex_2", "Question 2 : l'équivalence, puis la dilution", "C_B·V_B = C_A·V_AE, puis C₀ = 20·C_B.",
      "acides-bases-tableau/exploiter.html?vue=base", "L'équivalence d'une base dosée",
      "فla simulation، l'équivalence: C B fois V B égale C A fois V A E، إذن V A E égale vingt virgule zéro millilitres. شوف la courbe: هاد المرة كتهبط. le point E فالوسط ديال le saut. فالتمرين ديالنا، ب les tangentes، V A E égale quinze virgule zéro millilitres. إذن C B égale trois virgule zéro fois dix puissance moins deux، mole par litre. و le produit مخفف vingt fois: C zéro égale zéro virgule soixante mole par litre.",
      [("C_B = C_A·V_AE/V_B = 3,0 × 10⁻² mol/L", "إذن C B égale trois virgule zéro"), ("C₀ = 20·C_B = 0,60 mol/L", "C zéro égale zéro virgule soixante")],
      [("فla simulation، l'équivalence", "moment:relation"), ("شوف la courbe", "moment:courbe"), ("le point E", "moment:point_e")]),
  sim("ex_3", "Question 3 : pourquoi pH_E < 7", "Base faible dosée par un acide fort : à l'équivalence il reste l'acide conjugué BH⁺.",
      "acides-bases-tableau/exploiter.html?vue=trois_courbes", "Trois dosages, trois pH_E",
      "شوف les axes. أول courbe: l'acide chlorhydrique dosé par la soude، p H E égale sept. ثاني courbe: l'acide éthanoïque dosé par la soude، p H E égale huit virgule trois، كبر من sept. ثالث courbe: l'ammoniac dosé par l'acide chlorhydrique: p H E égale cinq virgule sept، صغر من sept، حيت la solution فيها les ions ammonium، و هادا acide. نعاود نقرا la règle: base faible et acide fort، p H E plus petit que sept. فالتمرين ديالنا، B H plus هو l'acide اللي كيبقى، و p H E environ cinq virgule sept: l'indicateur هو le rouge de méthyle.",
      [("BH⁺ acide : pH_E < 7", "فالتمرين ديالنا، B H plus"), ("rouge de méthyle : 4,2 – 6,2", "l'indicateur هو le rouge de méthyle")],
      [("شوف les axes", "moment:axes"), ("أول courbe", "moment:courbe_fort"), ("ثاني courbe", "moment:courbe_faible"),
       ("ثالث courbe", "moment:courbe_base"), ("نعاود نقرا la règle", "moment:regle")]),
  sim("ex_4", "Question 4 : τ de la réaction du dosage", "x_max par le réactif limitant, x_f = x_max − ce qui reste : τ ≈ 1.",
      "acides-bases-tableau/dosage.html?vue=reaction", "Une réaction de dosage rapide, totale et unique",
      "شوف la loupe: فla simulation، كل ion hydroxyde كيطيح، كياخد un proton. هاد la réaction فيها trois conditions. rapide. totale: كتكمل حتى يسالي واحد من les réactifs. unique. نقدرو نتأكدو ب le taux d'avancement final: x max ب le réactif limitant، و x f égale x max moins اللي بقا. فالتمرين ديالنا مقلوب: les ions H trois O plus هوما limitant، x max égale un virgule deux fois dix puissance moins quatre mole، و اللي بقا منهم trois virgule quatre fois dix puissance moins douze mole. إذن tau environ un: totale.",
      [("x_max = C_A·V_A = 1,2 × 10⁻⁴ mol", "x max égale un virgule deux"), ("τ ≈ 1 : totale", "إذن tau environ un")],
      [("شوف la loupe", "moment:loupe"), ("هاد la réaction فيها trois conditions", "moment:equation"), ("rapide", "moment:rapide"),
       ("totale: كتكمل", "moment:totale"), ("unique", "moment:unique")]),
  sim("ex_5", "Question 5 : pourcentages et pKa", "Les quantités du tableau donnent les pourcentages, puis pH = pKa + log([B]/[BH⁺]).",
      "acides-bases-tableau/predominance.html?vue=distribution", "Le diagramme de distribution",
      "شوف les axes: le pourcentage و le p H. la courbe rose هي l'acide، و la courbe verte هي la base. deux courbes كيتلاقاو ف cinquante pour cent، عند p H égale p K a. فالتمرين ديالنا: quarante pour cent ديال B H plus، و soixante pour cent ديال B. la base كثر شوية، إذن p H كبر شوية من p K a: p K a égale neuf virgule soixante-sept moins log de un virgule cinq، environ neuf virgule cinq.",
      [("%BH⁺ = 40 % ; %B = 60 %", "quarante pour cent ديال B H plus"), ("pKa = 9,67 − log 1,5 ≈ 9,5", "environ neuf virgule cinq")],
      [("شوف les axes", "moment:axes"), ("la courbe rose", "moment:courbe_acide"), ("و la courbe verte", "moment:courbe_base"),
       ("deux courbes كيتلاقاو", "moment:croisement")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : l'équation", "نتمرنو بسؤال ساهل. اختار l'équation.",
      "Dosage de la base B par l'acide chlorhydrique : l'équation est…",
      ["B + HO⁻ → BH⁺ + O²⁻", "B + H₃O⁺ → BH⁺ + H₂O", "B + H₂O ⇌ BH⁺ + HO⁻"], 1, {
        1: ("juste", "برافو! les ions H trois O plus ديال l'acide chlorhydrique كيعطيو un proton ل la base B.", "Juste : B + H₃O⁺ → BH⁺ + H₂O."),
        0: (("H O moins هو base، ما كيعطيش proton ل la base B. شكون هو l'acide فla burette؟ عاود اختار.", "HO⁻ est une base, il ne donne pas de proton. Réessaie."),
            ("الجواب هو B plus H trois O plus، simple flèche، B H plus plus l'eau.", "Réponse : B + H₃O⁺ → BH⁺ + H₂O.")),
        2: (("هادي la réaction ديال la base مع الما، ماشي مع l'acide chlorhydrique. عاود اختار.", "C'est la réaction de B avec l'eau. Réessaie."),
            ("الجواب هو مع H trois O plus، ب simple flèche.", "Réponse : B + H₃O⁺ → BH⁺ + H₂O."))},
      "Dosage de la base B par l'acide chlorhydrique. L'équation est ?"),
  qcm("fa_2", "Plus facile : la dilution", "سؤال ساهل على la dilution.",
      "S_B (C_B = 3,0 × 10⁻² mol/L) est le produit dilué 20 fois. Le produit a pour concentration…",
      ["0,60 mol/L", "1,5 × 10⁻³ mol/L", "3,0 × 10⁻² mol/L"], 0, {
        0: ("juste", "برافو! le produit مركز vingt fois كثر: C zéro égale vingt fois C B.", "Juste : C₀ = 20 × 3,0 × 10⁻² = 0,60 mol/L."),
        1: (("قسمتي على vingt. ولكن le produit هو اللي مركز كثر، ماشي S B. عاود اختار.", "Le produit est plus concentré que S_B : on multiplie. Réessaie."),
            ("الجواب هو zéro virgule soixante mole par litre: C zéro égale vingt fois C B.", "Réponse : C₀ = 20·C_B = 0,60 mol/L.")),
        2: (("هادي C B ديال S B. le produit قبل la dilution أكثر تركيز. عاود اختار.", "C'est la concentration de S_B, pas du produit. Réessaie."),
            ("الجواب هو zéro virgule soixante mole par litre.", "Réponse : C₀ = 0,60 mol/L."))},
      "S B est le produit dilué vingt fois، و C B égale trois virgule zéro fois dix puissance moins deux. Le produit a pour concentration ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "Base faible B dosée par l'acide chlorhydrique.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("À l'équivalence, la solution contient BH⁺, un acide : pH_E < 7.", True, "Base faible et acide fort : pH_E < 7."),
      ("À l'équivalence d'un dosage, le pH vaut toujours 7.", False, "Seulement pour un acide fort et une base forte."),
      ("Le BBT (6,0 – 7,6) convient pour pH_E ≈ 5,7.", False, "5,7 n'est pas dans 6,0 – 7,6 : il faut le rouge de méthyle (4,2 – 6,2).")]),
  qcm("fa_4", "Plus facile : le réactif limitant avant l'équivalence", "سؤال ساهل: اختار x max.",
      "V_A = 6,0 mL < V_AE ; C_A = 2,0 × 10⁻² mol/L ; n(B)initial = 3,0 × 10⁻⁴ mol. x_max vaut…",
      ["3,0 × 10⁻⁴ mol", "1,2 × 10⁻⁴ mol", "1,8 × 10⁻⁴ mol"], 1, {
        1: ("juste", "برافو! قبل l'équivalence، H trois O plus limitant: x max égale C A fois V A.", "Juste : x_max = C_A·V_A = 1,2 × 10⁻⁴ mol."),
        0: (("هادي la base كاملة. ولكن قبل l'équivalence، la base باقي فيها: ماشي هي limitant. عاود اختار.", "Avant l'équivalence il reste de la base : elle n'est pas limitante. Réessaie."),
            ("الجواب هو un virgule deux fois dix puissance moins quatre mole: C A fois V A.", "Réponse : x_max = C_A·V_A = 1,2 × 10⁻⁴ mol.")),
        2: (("هادي la base اللي بقات، ماشي x max. عاود اختار.", "C'est la base restante, pas x_max. Réessaie."),
            ("الجواب هو un virgule deux fois dix puissance moins quatre mole.", "Réponse : x_max = C_A·V_A."))},
      "V A égale six millilitres، C A égale deux virgule zéro fois dix puissance moins deux. x max vaut ?"),
  assoc("fa_5", "Plus facile : associer", "À V_A = 6,0 mL : n(BH⁺) = 1,2 × 10⁻⁴ mol, n(B) = 1,8 × 10⁻⁴ mol.",
        "سؤال ساهل: ربط كل grandeur مع القيمة ديالها.",
        "Relie chaque grandeur à sa valeur.",
        [("1", "%BH⁺"), ("2", "%B"), ("3", "[B]/[BH⁺]")],
        [("a", "40 %"), ("b", "60 %"), ("c", "1,5")],
        {"1": "a", "2": "b", "3": "c"},
        {"1-a": (True, "1,2/(1,2 + 1,8) = 0,40.", "برافو: un virgule deux sur trois، quarante pour cent."),
         "1-*": (False, "BH⁺ est la forme la moins abondante ici : divise n(BH⁺) par la somme.", "لا. قسم B H plus على la somme ديال les deux."),
         "2-b": (True, "1,8/3,0 = 0,60.", "برافو: un virgule huit sur trois، soixante pour cent."),
         "2-*": (False, "B est la forme la plus abondante : divise n(B) par la somme.", "لا. la base هي الأكثر: قسم B على la somme."),
         "3-c": (True, "1,8/1,2 = 1,5 (même volume).", "برافو: un virgule huit sur un virgule deux، un virgule cinq."),
         "3-*": (False, "C'est un rapport, pas un pourcentage : n(B)/n(BH⁺).", "لا. هادا rapport، ماشي pourcentage: B sur B H plus.")},
        ("40 % de BH⁺, 60 % de B, rapport 1,5 : pKa = 9,67 − log 1,5 ≈ 9,5.", "quarante pour cent، soixante pour cent، و le rapport un virgule cinq. p K a environ neuf virgule cinq.")),
]

SIM_Q = [
  QS("1", "Écrire l'équation de la réaction du dosage.",
     phrase("B(aq) + H₃O⁺(aq) → BH⁺(aq) + H₂O(l)"),
     (["H₃O⁺", "→"], ["HO⁻"]),
     [("B + H₃O⁺ → BH⁺ + H₂O", "simple flèche")],
     "la base B، plus H trois O plus، simple flèche، B H plus، plus l'eau."),
  QS("2", "Déterminer V_AE, puis C_B et la concentration C₀ du produit (dilué 20 fois).",
     val("C₀", sC0, "mol/L", "V_AE = 12,0 mL ; C_B = 2,0 × 10⁻² × 12,0/10,0 = 2,4 × 10⁻² mol/L ; C₀ = 20·C_B = 0,48 mol/L"),
     (["C_B·V_B = C_A·V_AE", "C₀ = 20·C_B"], ["C₀ = C_B/20"]),
     [("V_AE = 12,0 mL ; C_B = 2,4 × 10⁻² mol/L", "V A E égale douze"), ("C₀ = 0,48 mol/L", "zéro virgule quarante-huit")],
     "V A E égale douze virgule zéro millilitres، C B égale deux virgule quatre fois dix puissance moins deux، و C zéro égale zéro virgule quarante-huit mole par litre."),
  QS("3", "Justifier pH_E < 7 et choisir l'indicateur adéquat.",
     phrase("À l'équivalence il reste BH⁺ (acide) et Cl⁻ : pH_E < 7 ; rouge de méthyle (4,2 – 6,2)."),
     (["BH⁺", "rouge de méthyle"], ["pH_E = 7"]),
     [("BH⁺ acide : pH_E < 7 ; rouge de méthyle", "le rouge de méthyle")],
     "عند l'équivalence كيبقى B H plus، و هو acide، إذن p H E صغر من sept. l'indicateur: le rouge de méthyle."),
  QS("4", "Pour V_A = 4,8 mL, pH = 9,67. Calculer τ de la réaction du dosage et conclure.",
     val("τ", 1.0, None, "x_max = C_A·V_A = 9,6 × 10⁻⁵ mol ; reste 10^(−9,67) × 14,8 × 10⁻³ = 3,2 × 10⁻¹² mol ; τ = 1,00", tol=0.01),
     (["x_max = C_A·V_A", "τ = x_f/x_max"], ["x_max = C_B·V_B"]),
     [("x_max = 9,6 × 10⁻⁵ mol ; reste négligeable : τ ≈ 1, totale", "tau environ un")],
     "x max égale C A fois V A، يعني neuf virgule six fois dix puissance moins cinq mole، و اللي بقا من H trois O plus والو تقريبا. tau environ un: totale."),
  QS("5", "Pour V_A = 4,8 mL : pourcentage de BH⁺ puis pKa du couple BH⁺/B.",
     val("pKa", sPKA1, None, "n(BH⁺) = 9,6 × 10⁻⁵ mol ; n(B) = 1,44 × 10⁻⁴ mol ; %BH⁺ = 40 % ; pKa = 9,67 − log 1,5 = 9,49", tol=0.01),
     (["pH = pKa + log([B]/[BH⁺])"], ["pKa = pH"]),
     [("%BH⁺ = 40 % ; pKa = 9,67 − log 1,5 ≈ 9,5", "quarante pour cent")],
     "B H plus: neuf virgule six fois dix puissance moins cinq mole، و B: un virgule quarante-quatre fois dix puissance moins quatre mole. quarante pour cent ديال B H plus، و p K a égale neuf virgule soixante-sept moins log de un virgule cinq، environ neuf virgule cinq."),
]

EX = exercice(
  "phys_ex_ch13_acides_bases_7", "phys_ch13_acides_bases", "acides_bases",
  "Un produit ménager basique : dosage d'une base faible par l'acide chlorhydrique", "difficile", 40,
  ["Écrire la réaction du dosage d'une base", "Exploiter l'équivalence et une dilution", "Justifier pH_E < 7 et choisir un indicateur", "Calculer τ de la réaction du dosage", "Calculer des pourcentages et un pKa à partir du tableau"],
  "Un produit ménager contient une base faible notée B (couple BH⁺/B). On dilue ce produit 20 fois : on obtient une solution S_B de concentration C_B. On dose V_B = 10,0 mL de S_B par une solution d'acide chlorhydrique (H₃O⁺(aq) + Cl⁻(aq)) de concentration C_A = 2,0 × 10⁻² mol/L ; la figure 1 donne pH = f(V_A). Le tableau (figure 2) donne des zones de virage. Données à 25 °C : pKe = 14 ; pour V_A = 6,0 mL, pH = 9,67.",
  "دابا نقراو l'énoncé. واحد le produit ménager فيه base faible، كنسميوها B، و le couple ديالها B H plus، B. خففنا le produit vingt fois، و لقينا la solution S B. كنديرو le dosage ديال dix virgule zéro millilitres من S B، ب l'acide chlorhydrique، C A égale deux virgule zéro fois dix puissance moins deux، mole par litre. la figure un كتعطي le p H en fonction de V A، و la figure deux فيها les zones de virage. و ف V A égale six millilitres، le p H égale neuf virgule soixante-sept.",
  [FIG, fig_indicateurs()],
  ["V_B = 10,0 mL de S_B (produit dilué 20 fois)", "C_A = 2,0 × 10⁻² mol/L", "pKe = 14 à 25 °C", "Pour V_A = 6,0 mL : pH = 9,67"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Un autre produit contenant la même base B est dilué 20 fois (solution S_B). On dose V_B = 10,0 mL de S_B par l'acide chlorhydrique à C_A = 2,0 × 10⁻² mol/L (figure). Pour V_A = 4,8 mL, pH = 9,67.",
  "نفس التمرين، بقيم أخرى. produit آخر، مخفف vingt fois، و نفس le dosage. ف V A égale quatre virgule huit millilitres، le p H égale neuf virgule soixante-sept.",
  [sFIG, fig_indicateurs()],
  ["V_B = 10,0 mL ; dilution 20 fois", "C_A = 2,0 × 10⁻² mol/L", "Pour V_A = 4,8 mL : pH = 9,67"],
  SIM_Q)

ecrire(EX)
