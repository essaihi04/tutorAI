# Exercice de chimie, ch. 13 (réactions acido-basiques), niveau supérieur (au-dessus du national, même forme) :
# contrôle d'un conservateur alimentaire en poudre (acide sorbique) — réaction de dosage totale (K), équivalence,
# masse dans un sachet et lecture critique de l'étiquette, « montrer que » [A⁻]/[AH] = V_B/(V_BE − V_B) puis pKa,
# et volume pour lequel la forme basique atteint 80 %.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2024 N (2 V_BE, 3 C_A, 4 masse restante dans un comprimé, 5-2 « montrer que »
#    le rapport pour V_B < V_BE, 5-3 pKa, 5-4 K du dosage), 2025 N (1.2 à 1.5 : C_A, C₀, « justifier si l'indication
#    de l'étiquette est vérifiée », K du dosage), 2019 R (I.2.2 « montrer que m = 0,5 g »), 2022 N (2.4 masse d'acide
#    pur, 2.5 pourcentage de la forme acide), 2016 N (1.2 K du dosage, « montrer que la réaction est totale »)
#    — backend/data/exams/physique ;
#  - profs (architecture/phys_ch13_acides_bases.md § 1 : Naceiri Mrabti — titrage, demi-équivalence, τ du titrage ;
#    Prof Bazhar, vidéo du dosage) ; pièges relevés : oublier le facteur de la prise d'essai (20 mL sur 200 mL),
#    écrire [A⁻]/[AH] = V_B/V_BE, confondre « 80 % de base » et « V_B = 80 % de 20 mL » ;
#  - séries en ligne repérées (titres et résumés lus ; PDF non ouverts, hôtes hors du réseau de la session) :
#    talamidi exercices non corrigés 2 et 5, moutamadris fiches 13-7, 13-8 et 17-2, pc1.ma Pr. Chargui,
#    alloschool El Goufifa séance 15, coursdusoirpc TD 2 BAC BIOF.
# Ici : l'acide sorbique (pKa 4,8, M = 112 g/mol), notre sachet et notre courbe calculée ; au-dessus du national :
# la prise d'essai, la lecture critique de l'étiquette et le pourcentage imposé combinés au même tableau.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch13 import *

PKA, M = 4.8, 112.0
VA, CB, VTOT = 20.0, 2.0e-2, 0.200
K = 10 ** (14 - PKA)
VBE = 17.5
CA = CB * VBE / VA
MASSE = CA * VTOT * M
V4 = VBE / 5
PH4 = round(ph_dosage(VA, CA, CB, V4, PKA), 2)
R4 = V4 / (VBE - V4)
PKA4 = PH4 - math.log10(R4)
V80 = 0.8 * VBE
assert abs(K - 1.58e9) < 1e7 and abs(CA - 1.75e-2) < 1e-12 and abs(MASSE - 0.392) < 1e-6
assert abs(PH4 - 4.21) < 1e-9 and abs(R4 - 0.25) < 1e-12 and abs(PKA4 - 4.81) < 0.005 and abs(V80 - 14.0) < 1e-9
assert abs(ph_dosage(VA, CA, CB, V80, PKA) - (PKA + math.log10(4))) < 0.01

sVBE = 16.0
sCA = CB * sVBE / VA
sM = sCA * VTOT * M
sV4 = sVBE / 5
sPH4 = round(ph_dosage(VA, sCA, CB, sV4, PKA), 2)
sPKA4 = sPH4 - math.log10(sV4 / (sVBE - sV4))
sV80 = 0.8 * sVBE
assert abs(sCA - 1.6e-2) < 1e-12 and abs(sM - 0.3584) < 1e-6 and abs(sPH4 - 4.21) < 1e-9 and abs(sV80 - 12.8) < 1e-9

def g(x):
    return [x, fr(x, 1).replace(",0", "")]
FIG = fig_ph("pH du mélange en fonction du volume V_B de soude versé", VA, CA, CB, 30, PKA, True,
             [g(i * 2.5) for i in range(13)], legende="Prise d'essai : V_A = 20,0 mL de la solution S (200 mL).")
sFIG = fig_ph("pH du mélange en fonction du volume V_B de soude versé", VA, sCA, CB, 30, PKA, True, list(range(0, 31, 2)))

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction du dosage (on note AH l'acide sorbique), puis montrer qu'elle est totale en calculant sa constante d'équilibre K.",
    "السؤال un: كتب l'équation ديال la réaction du dosage، و A H هو l'acide sorbique. من بعد بين بلي totale، ب الحساب ديال K.",
    val("K", K, None, "AH + HO⁻ → A⁻ + H₂O ; K = Ka/Ke = 10^(pKe − pKa) = 10^(14 − 4,8) = 1,6 × 10⁹ > 10⁴ : totale"),
    (["K = Ka/Ke", "10^(pKe − pKa)", "10⁴"], ["K = Ke/Ka", "K = Ka·Ke"]),
    [("La base qui réagit est HO⁻, du couple H₂O/HO⁻ dont la constante d'acidité est Ke. Écris K, puis multiplie haut et bas par [H₃O⁺].",
      "la base اللي كتتفاعل هي H O moins، و le couple ديالها H deux O، H O moins، و K a ديالو هو K e. كتب K، و ضرب الفوق و التحت ف H trois O plus."),
     ("K = Ka/Ke = 10^(−pKa)/10^(−14). Une réaction est pratiquement totale si K > 10⁴.",
      "K égale K a sur K e، يعني dix puissance quatorze moins p K a. و la réaction pratiquement totale يلا كانت K كبر من dix puissance quatre.")],
    [("1 : AH(aq) + HO⁻(aq) → A⁻(aq) + H₂O(l)", "l'acide sorbique، plus H O moins"),
     ("K = [A⁻]/([AH]·[HO⁻]) = Ka/Ke = 10^(14 − 4,8)", "K égale K a sur K e"),
     ("K = 1,6 × 10⁹ > 10⁴ : la réaction de dosage est totale", "un virgule six fois dix puissance neuf")],
    "السؤال un. l'acide sorbique، plus H O moins، simple flèche، l'ion sorbate، plus l'eau. K égale A moins، sur A H fois H O moins. نضربو الفوق و التحت ف H trois O plus: K égale K a sur K e، يعني dix puissance quatorze moins quatre virgule huit. K égale un virgule six fois dix puissance neuf، كبر بزاف من dix puissance quatre: la réaction totale.",
    "ex_1", "fa_1"),
  Q("2", "Déterminer graphiquement V_BE, puis calculer la concentration C_A de la solution S.",
    "السؤال deux: حدد V B E على la courbe، ومن بعد حسب C A ديال la solution S.",
    val("C_A", CA, "mol/L", "V_BE = 17,5 mL ; C_A = C_B·V_BE/V_A = 2,0 × 10⁻² × 17,5/20,0 = 1,75 × 10⁻² mol/L"),
    (["tangentes", "C_A·V_A = C_B·V_BE", "mol/L"], ["C_A = C_B·V_A/V_BE", "V_A = 200 mL"]),
    [("Le point d'équivalence est au milieu du saut de pH : méthode des tangentes. Puis la relation à l'équivalence.",
      "le point d'équivalence فالوسط ديال le saut de p H: la méthode des tangentes. من بعد la relation ديال l'équivalence."),
     ("V_BE = 17,5 mL ; C_A·V_A = C_B·V_BE avec V_A = 20,0 mL, la prise d'essai (pas 200 mL).",
      "C A fois V A égale C B fois V B E، و V A هو vingt millilitres اللي درنا ليهم le dosage، ماشي deux cents.")],
    [("2 : par la méthode des tangentes : V_BE = 17,5 mL", "V B E égale dix-sept virgule cinq millilitres"),
     ("C_A = C_B·V_BE/V_A = 2,0 × 10⁻² × 17,5/20,0", "C A égale C B fois V B E sur V A"),
     ("C_A = 1,75 × 10⁻² mol/L", "un virgule soixante-quinze fois dix puissance moins deux")],
    "السؤال deux. ب la méthode des tangentes، V B E égale dix-sept virgule cinq millilitres. عند l'équivalence، C A égale C B fois V B E sur V A، يعني deux virgule zéro fois dix puissance moins deux، fois dix-sept virgule cinq، sur vingt. C A égale un virgule soixante-quinze fois dix puissance moins deux، mole par litre.",
    "ex_2", "fa_2"),
  Q("3", "Calculer la masse m d'acide sorbique contenue dans un sachet. L'étiquette annonce 400 mg par sachet, à 5 % près : l'indication est-elle vérifiée ?",
    "السؤال trois: حسب la masse m ديال l'acide sorbique فsachet واحد. l'étiquette كتقول quatre cents milligrammes، à cinq pour cent près. واش صحيح؟",
    val("m", MASSE, "g", "écart de 2 % < 5 % : vérifiée ; m = C_A·V·M = 1,75 × 10⁻² × 0,200 × 112 = 0,392 g"),
    (["n = C_A·V", "m = n·M", "V = 200 mL", "g"], ["V = 20 mL", "m = C_A·V_A·M"]),
    [("Tout le sachet est dissous dans 200 mL : la quantité d'acide du sachet est celle des 200 mL, pas celle de la prise d'essai.",
      "le sachet كامل ذاب ف deux cents millilitres. إذن la quantité d'acide ديال le sachet هي ديال deux cents millilitres، ماشي ديال vingt."),
     ("n = C_A·V avec V = 0,200 L, puis m = n·M ; écart relatif = |m − 0,400|/0,400.",
      "n égale C A fois V، و V égale zéro virgule deux cents litre. من بعد m égale n fois M. و l'écart: الفرق على quatre cents milligrammes.")],
    [("3 : n = C_A·V = 1,75 × 10⁻² × 0,200 = 3,5 × 10⁻³ mol", "n égale C A fois V"),
     ("m = n·M = 3,5 × 10⁻³ × 112 = 0,392 g", "m égale zéro virgule trois cent quatre-vingt-douze gramme"),
     ("écart = (0,400 − 0,392)/0,400 = 2 % < 5 % : l'indication est vérifiée", "deux pour cent")],
    "السؤال trois. le sachet ذاب ف deux cents millilitres. n égale C A fois V، يعني un virgule soixante-quinze fois dix puissance moins deux، fois zéro virgule deux cents، égale trois virgule cinq fois dix puissance moins trois mole. m égale n fois M، يعني m égale zéro virgule trois cent quatre-vingt-douze gramme. l'écart مع quatre cents milligrammes: deux pour cent، صغر من cinq pour cent. إذن l'étiquette صحيحة.",
    "ex_3", "fa_3"),
  Q("4", "Pour 0 < V_B < V_BE, montrer à l'aide du tableau d'avancement que [A⁻]/[AH] = V_B/(V_BE − V_B). Pour V_B = 3,5 mL, le pH-mètre indique pH = 4,21 : en déduire le pKa du couple AH/A⁻.",
    "السؤال quatre: من أجل V B بين zéro و V B E، بين ب le tableau بلي A moins sur A H، égale V B sur V B E moins V B. ف V B égale trois virgule cinq millilitres، le p H égale quatre virgule vingt et un. استنتج p K a.",
    val("pKa", PKA4, None, "[A⁻]/[AH] = C_B·V_B/(C_A·V_A − C_B·V_B) = V_B/(V_BE − V_B) = 3,5/14,0 = 0,25 ; pKa = pH − log 0,25 = 4,21 + 0,60 = 4,81", tol=0.01),
    (["x_f = C_B·V_B", "C_A·V_A = C_B·V_BE", "pH = pKa + log([A⁻]/[AH])"], ["V_B/V_BE", "pKa = pH à V_B = 3,5 mL"]),
    [("Avant l'équivalence HO⁻ est limitant : x_f = C_B·V_B. Remplace ensuite C_A·V_A par C_B·V_BE.",
      "قبل l'équivalence، H O moins limitant: x f égale C B fois V B. من بعد بدل C A fois V A ب C B fois V B E."),
     ("[A⁻]/[AH] = C_B·V_B/(C_B·V_BE − C_B·V_B) : C_B se simplifie. Puis pKa = pH − log([A⁻]/[AH]).",
      "le rapport égale C B V B، sur C B V B E moins C B V B. C B كتحيد. من بعد p K a égale p H moins log du rapport.")],
    [("4 : x_f = C_B·V_B ; n(A⁻) = C_B·V_B ; n(AH) = C_A·V_A − C_B·V_B = C_B·(V_BE − V_B)", "x f égale C B fois V B"),
     ("même volume : [A⁻]/[AH] = V_B/(V_BE − V_B) = 3,5/14,0 = 0,25", "le rapport égale zéro virgule vingt-cinq"),
     ("pKa = pH − log([A⁻]/[AH]) = 4,21 − log 0,25 = 4,81", "p K a égale quatre virgule quatre-vingt-un")],
    "السؤال quatre. قبل l'équivalence، x f égale C B fois V B. les ions sorbate: C B fois V B. l'acide اللي بقا: C A V A moins C B V B، و C A V A égale C B V B E. نفس le volume، و C B كتحيد: le rapport égale V B، sur V B E moins V B. ف trois virgule cinq millilitres: trois virgule cinq sur quatorze، le rapport égale zéro virgule vingt-cinq. إذن p K a égale p H moins log de zéro virgule vingt-cinq، يعني quatre virgule vingt et un plus zéro virgule soixante. p K a égale quatre virgule quatre-vingt-un، environ quatre virgule huit.",
    "ex_4", "fa_4"),
  Q("5", "Déterminer le volume V_B de soude versé pour lequel la forme basique A⁻ représente 80 % des deux formes du couple. Vérifier sur la courbe.",
    "السؤال cinq: حدد V B اللي فيه la forme basique A moins كتمثل quatre-vingts pour cent. تحقق على la courbe.",
    val("V_B", V80, "mL", "80 % de A⁻ : [A⁻]/[AH] = 80/20 = 4 = V_B/(V_BE − V_B) donc V_B = 0,8·V_BE = 0,8 × 17,5 = 14,0 mL"),
    (["[A⁻]/[AH] = 4", "V_B/(V_BE − V_B)", "pH = pKa + log 4", "mL"], ["V_B = 0,8 × 20,0", "[A⁻]/[AH] = 0,8"]),
    [("80 % de A⁻ et 20 % de AH : quel est alors le rapport [A⁻]/[AH] ?",
      "quatre-vingts pour cent ديال A moins، و vingt pour cent ديال A H. شحال كيساوي le rapport؟"),
     ("Utilise la relation de la question 4 : V_B/(V_BE − V_B) = 4, puis isole V_B. Vérification : pH = pKa + log 4.",
      "استعمل la relation ديال السؤال quatre: V B sur V B E moins V B، égale quatre. عزل V B. و تحقق: p H égale p K a plus log de quatre.")],
    [("5 : 80 % de A⁻ et 20 % de AH : [A⁻]/[AH] = 4", "le rapport égale quatre"),
     ("V_B/(V_BE − V_B) = 4 donc V_B = 4·V_BE/5 = 0,8 × 17,5 = 14,0 mL", "V B égale quatorze virgule zéro millilitres"),
     ("vérification : à 14,0 mL, pH ≈ pKa + log 4 ≈ 5,4", "environ cinq virgule quatre")],
    "السؤال cinq. quatre-vingts pour cent ديال la base و vingt pour cent ديال l'acide: le rapport égale quatre. إذن V B sur V B E moins V B égale quatre، يعني V B égale quatre fois V B E sur cinq. V B égale quatorze virgule zéro millilitres. تحقق: le p H خاصو يكون p K a plus log de quatre، environ cinq virgule quatre. و هادشي اللي كتعطي la courbe.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : K = Ka/Ke, une réaction totale", "Le couple de HO⁻ est H₂O/HO⁻, de constante Ke : K = Ka/Ke.",
      "acides-bases-tableau/comparer.html?vue=totale", "Un acide avec les ions hydroxyde",
      "فla simulation، l'acide éthanoïque مع les ions hydroxyde. l'équation ب simple flèche. la base H O moins، le couple ديالها هو H deux O، H O moins، و K a ديالو هو K e. إذن K égale K a sur K e. فla simulation: dix puissance neuf virgule deux. K كبير بزاف: كبر من dix puissance quatre، إذن la réaction pratiquement totale. فالتمرين ديالنا، p K a ديال l'acide sorbique حتى هو quatre virgule huit: K égale dix puissance neuf virgule deux، يعني un virgule six fois dix puissance neuf. totale.",
      [("K = Ka/Ke = 10^(14 − 4,8)", "إذن K égale K a sur K e"), ("K = 1,6 × 10⁹ > 10⁴ : totale", "يعني un virgule six fois dix puissance neuf")],
      [("فla simulation، l'acide éthanoïque", "moment:equation"), ("la base H O moins", "moment:couple_eau"),
       ("إذن K égale K a sur K e", "moment:relation"), ("فla simulation: dix puissance", "moment:application"), ("K كبير بزاف", "moment:totale")]),
  sim("ex_2", "Question 2 : l'équivalence donne C_A", "C_A·V_A = C_B·V_BE, avec V_A la prise d'essai.",
      "acides-bases-tableau/dosage.html?vue=equivalence", "Le tableau d'avancement à l'équivalence",
      "شوف le tableau d'avancement ديال la réaction de dosage. عند l'équivalence، deux réactifs كيساليو مع بعض. la définition: à l'équivalence، les réactifs sont، dans les proportions stœchiométriques. إذن la relation: C A fois V A égale C B fois V B E. فالتمرين ديالنا، على la courbe، V B E égale dix-sept virgule cinq millilitres، و V A égale vingt millilitres. C A égale un virgule soixante-quinze fois dix puissance moins deux، mole par litre.",
      [("C_A·V_A = C_B·V_BE", "إذن la relation"), ("C_A = 1,75 × 10⁻² mol/L", "C A égale un virgule soixante-quinze")],
      [("شوف le tableau d'avancement", "moment:tableau"), ("عند l'équivalence، deux réactifs", "moment:a_equivalence"),
       ("la définition", "moment:definition"), ("إذن la relation", "moment:relation")]),
  sim("ex_3", "Question 3 : de la concentration à la masse", "n = C·V puis m = n·M ; V est le volume où tout le produit est dissous.",
      "acides-bases-tableau/exploiter.html?vue=base", "Exploiter le dosage : de C à la masse",
      "فla simulation، من بعد le dosage، كنحسبو la concentration massique: C m égale m sur V، و m égale n fois M، إذن C m égale C fois M، و فla simulation، zéro virgule dix-sept gramme par litre. فالتمرين ديالنا، la même idée: n égale C A fois V، مع V égale deux cents millilitres، حيت le sachet كامل ذاب فيهم. n égale trois virgule cinq fois dix puissance moins trois mole، و m égale n fois M، يعني zéro virgule trois cent quatre-vingt-douze gramme. l'écart مع l'étiquette deux pour cent.",
      [("m = C_A·V·M", "و m égale n fois M، يعني"), ("m = 0,392 g ; écart 2 %", "l'écart مع l'étiquette")],
      [("فla simulation، من بعد le dosage", "moment:indicateur")]),
  sim("ex_4", "Question 4 : le tableau avant l'équivalence", "n(A⁻) = C_B·V_B et n(AH) = C_B·(V_BE − V_B) : le rapport ne dépend que des volumes.",
      "acides-bases-tableau/exploiter.html?vue=demi", "Le tableau d'avancement et la demi-équivalence",
      "فla simulation، l'acide éthanoïque dosé par la soude. شوف le tableau: la soude اللي طاحت، C B fois V B، كتعطي نفس الكمية ديال les ions éthanoate. و l'acide اللي بقا: C A V A moins C B V B. فالنص، les deux متساويين، و p H égale p K a. فالتمرين ديالنا، كنبدلو C A V A ب C B V B E: le rapport égale V B، sur V B E moins V B. ف trois virgule cinq millilitres: zéro virgule vingt-cinq. و p K a égale p H moins log du rapport: quatre virgule quatre-vingt-un.",
      [("[A⁻]/[AH] = V_B/(V_BE − V_B)", "le rapport égale V B"), ("pKa = 4,21 − log 0,25 = 4,81", "quatre virgule quatre-vingt-un")],
      [("فla simulation، l'acide éthanoïque", "moment:courbe"), ("شوف le tableau", "moment:tableau"),
       ("فالنص، les deux متساويين", "moment:egalite"), ("و p H égale p K a", "moment:relation")]),
  sim("ex_5", "Question 5 : 80 % de la forme basique", "Pourcentage → rapport → volume.",
      "acides-bases-tableau/predominance.html?vue=distribution", "Le diagramme de distribution",
      "شوف les axes: le pourcentage و le p H. la courbe rose هي l'acide، و la courbe verte هي la base. deux courbes كيتلاقاو ف cinquante pour cent، عند p H égale p K a. كلما زاد le p H، كتزيد la base. فالتمرين ديالنا، quatre-vingts pour cent ديال la base: le rapport quatre. V B sur V B E moins V B égale quatre، إذن V B égale quatorze virgule zéro millilitres، و le p H environ cinq virgule quatre.",
      [("[A⁻]/[AH] = 80/20 = 4", "le rapport quatre"), ("V_B = 0,8·V_BE = 14,0 mL", "إذن V B égale quatorze virgule zéro millilitres")],
      [("شوف les axes", "moment:axes"), ("la courbe rose", "moment:courbe_acide"), ("و la courbe verte", "moment:courbe_base"),
       ("deux courbes كيتلاقاو", "moment:croisement")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : K de la réaction du dosage", "نتمرنو بسؤال ساهل.",
      "pKa(AH/A⁻) = 4,8 et pKe = 14. La constante K de AH + HO⁻ → A⁻ + H₂O vaut…",
      ["10^(4,8 − 14)", "10^(14 − 4,8)", "4,8/14"], 1, {
        1: ("juste", "برافو! K égale K a sur K e، يعني dix puissance quatorze moins quatre virgule huit، كبيرة بزاف: totale.", "Juste : K = Ka/Ke = 10^9,2 ≈ 1,6 × 10⁹."),
        0: (("قلبتي: هاد الشي هو K e sur K a. K a ديال l'acide اللي كيتفاعل فالفوق. عاود اختار.", "C'est Ke/Ka, l'inverse. Réessaie."),
            ("الجواب هو dix puissance quatorze moins quatre virgule huit: K égale K a sur K e.", "Réponse : K = Ka/Ke = 10^(14 − 4,8).")),
        2: (("K ماشي قسمة ديال les p K a. K a égale dix puissance moins p K a. عاود اختار.", "On ne divise pas les pKa entre eux. Réessaie."),
            ("الجواب هو dix puissance quatorze moins quatre virgule huit.", "Réponse : K = 10^(14 − 4,8) ≈ 1,6 × 10⁹."))},
      "p K a égale quatre virgule huit، p K e égale quatorze. La constante K de la réaction du dosage vaut ?"),
  vf("fa_2", "Plus facile : vrai ou faux", "Prise d'essai V_A = 20,0 mL ; V_BE = 17,5 mL ; C_B = 2,0 × 10⁻² mol/L.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("C_A = C_B·V_BE/V_A = 1,75 × 10⁻² mol/L.", True, "À l'équivalence, C_A·V_A = C_B·V_BE."),
      ("Dans la relation d'équivalence, V_A est le volume de la fiole (200 mL).", False, "V_A est le volume dosé, la prise d'essai : 20,0 mL."),
      ("À l'équivalence, les réactifs sont dans les proportions stœchiométriques.", True, "C'est la définition de l'équivalence.")]),
  qcm("fa_3", "Plus facile : la masse du sachet", "سؤال ساهل: اختار la bonne masse.",
      "C_A = 1,75 × 10⁻² mol/L ; le sachet est dissous dans 200 mL ; M = 112 g/mol. m vaut…",
      ["0,392 g", "0,0392 g", "3,92 g"], 0, {
        0: ("juste", "برافو! n égale C A fois zéro virgule deux cents litre، و m égale n fois M: zéro virgule trois cent quatre-vingt-douze gramme.", "Juste : m = 1,75 × 10⁻² × 0,200 × 112 = 0,392 g."),
        1: (("هادي la masse ديال vingt millilitres غير. le sachet ذاب ف deux cents. عاود اختار.", "C'est la masse dans la prise d'essai de 20 mL seulement. Réessaie."),
            ("الجواب هو zéro virgule trois cent quatre-vingt-douze gramme: خاصنا V égale deux cents millilitres.", "Réponse : m = C_A × 0,200 × 112 = 0,392 g.")),
        2: (("شوف الوحدات: deux cents millilitres هي zéro virgule deux litre، ماشي deux litres. عاود اختار.", "200 mL = 0,200 L. Réessaie."),
            ("الجواب هو zéro virgule trois cent quatre-vingt-douze gramme.", "Réponse : 0,392 g (V = 0,200 L)."))},
      "C A égale un virgule soixante-quinze fois dix puissance moins deux، le sachet ذاب ف deux cents millilitres، M égale cent douze. La masse vaut ?"),
  qcm("fa_4", "Plus facile : le rapport avant l'équivalence", "سؤال ساهل: اختار le rapport.",
      "V_BE = 17,5 mL et V_B = 3,5 mL. [A⁻]/[AH] vaut…",
      ["3,5/17,5 = 0,20", "14,0/3,5 = 4,0", "3,5/14,0 = 0,25"], 2, {
        2: ("juste", "برافو! V B sur V B E moins V B، يعني trois virgule cinq sur quatorze، zéro virgule vingt-cinq.", "Juste : V_B/(V_BE − V_B) = 3,5/14,0 = 0,25."),
        0: (("قريب! ولكن l'acide اللي بقا كيوافق V B E moins V B، ماشي V B E. عاود اختار.", "Il reste C_B·(V_BE − V_B) d'acide, pas C_B·V_BE. Réessaie."),
            ("الجواب هو trois virgule cinq sur quatorze، zéro virgule vingt-cinq.", "Réponse : 3,5/(17,5 − 3,5) = 0,25.")),
        1: (("قلبتي le rapport: هادا A H sur A moins. عاود اختار.", "C'est le rapport inverse [AH]/[A⁻]. Réessaie."),
            ("الجواب هو A moins sur A H، يعني zéro virgule vingt-cinq.", "Réponse : [A⁻]/[AH] = 0,25."))},
      "V B E égale dix-sept virgule cinq millilitres، V B égale trois virgule cinq. Le rapport A moins sur A H vaut ?"),
  vf("fa_5", "Plus facile : vrai ou faux", "80 % de A⁻ et 20 % de AH.", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Le rapport [A⁻]/[AH] vaut 4.", True, "80/20 = 4."),
      ("Il faut verser 80 % de 20,0 mL, soit 16,0 mL.", False, "Le volume se tire de V_B/(V_BE − V_B) = 4 : V_B = 0,8·V_BE = 14,0 mL."),
      ("Au point obtenu, pH = pKa + log 4 ≈ 5,4.", True, "4,8 + 0,6 = 5,4.")]),
]

SIM_Q = [
  QS("1", "Écrire l'équation du dosage et montrer qu'il est total en calculant K.",
     val("K", K, None, "K = Ka/Ke = 10^(14 − 4,8) = 1,6 × 10⁹ > 10⁴ : totale"),
     (["K = Ka/Ke"], ["K = Ke/Ka"]),
     [("AH + HO⁻ → A⁻ + H₂O ; K = Ka/Ke = 1,6 × 10⁹ : totale", "K égale K a sur K e")],
     "A H plus H O moins، simple flèche، A moins plus l'eau. K égale K a sur K e، يعني un virgule six fois dix puissance neuf: totale."),
  QS("2", "Déterminer V_BE et calculer C_A.",
     val("C_A", sCA, "mol/L", "V_BE = 16,0 mL ; C_A = 2,0 × 10⁻² × 16,0/20,0 = 1,6 × 10⁻² mol/L"),
     (["C_A·V_A = C_B·V_BE", "mol/L"], ["V_A = 200 mL"]),
     [("V_BE = 16,0 mL ; C_A = C_B·V_BE/V_A = 1,6 × 10⁻² mol/L", "un virgule six fois dix puissance moins deux")],
     "V B E égale seize virgule zéro millilitres، و C A égale C B fois V B E sur V A، يعني un virgule six fois dix puissance moins deux، mole par litre."),
  QS("3", "Calculer la masse m d'acide sorbique dans un sachet (dissous dans 200 mL). L'étiquette annonce 400 mg à 5 % près : est-ce vérifié ?",
     val("m", sM, "g", "écart de 10 % > 5 % : non vérifiée ; m = C_A·V·M = 1,6 × 10⁻² × 0,200 × 112 = 0,358 g"),
     (["m = C_A·V·M", "g"], ["V = 20 mL"]),
     [("m = 1,6 × 10⁻² × 0,200 × 112 = 0,358 g", "zéro virgule trois cent cinquante-huit gramme"), ("écart ≈ 10 % > 5 % : non vérifiée", "dix pour cent")],
     "m égale C A fois V fois M، يعني zéro virgule trois cent cinquante-huit gramme. l'écart environ dix pour cent، كبر من cinq: l'étiquette ماشي صحيحة."),
  QS("4", "Montrer que [A⁻]/[AH] = V_B/(V_BE − V_B). Pour V_B = 3,2 mL, pH = 4,21 : en déduire le pKa.",
     val("pKa", sPKA4, None, "[A⁻]/[AH] = 3,2/12,8 = 0,25 ; pKa = 4,21 − log 0,25 = 4,81", tol=0.01),
     (["x_f = C_B·V_B", "pH = pKa + log([A⁻]/[AH])"], ["V_B/V_BE"]),
     [("[A⁻]/[AH] = V_B/(V_BE − V_B) = 0,25", "zéro virgule vingt-cinq"), ("pKa = 4,21 + 0,60 = 4,81", "quatre virgule quatre-vingt-un")],
     "le rapport égale V B sur V B E moins V B، يعني trois virgule deux sur douze virgule huit، zéro virgule vingt-cinq. p K a égale p H moins log du rapport: quatre virgule quatre-vingt-un."),
  QS("5", "Déterminer V_B pour lequel A⁻ représente 80 % des deux formes.",
     val("V_B", sV80, "mL", "[A⁻]/[AH] = 4 donc V_B = 0,8·V_BE = 0,8 × 16,0 = 12,8 mL"),
     (["[A⁻]/[AH] = 4", "mL"], ["V_B = 0,8 × 20,0"]),
     [("[A⁻]/[AH] = 4 ; V_B = 0,8·V_BE = 12,8 mL", "douze virgule huit millilitres")],
     "le rapport égale quatre، إذن V B égale zéro virgule huit fois V B E، يعني douze virgule huit millilitres."),
]

EX = exercice(
  "phys_ex_ch13_acides_bases_6", "phys_ch13_acides_bases", "acides_bases",
  "Un conservateur en sachet : dosage de l'acide sorbique", "difficile", 40,
  ["Montrer qu'une réaction de dosage est totale (K = Ka/Ke)", "Déterminer V_BE et C_A", "Calculer une masse et juger une étiquette", "Établir [A⁻]/[AH] = V_B/(V_BE − V_B) et en déduire pKa", "Relier un pourcentage à un volume versé"],
  "Un conservateur alimentaire est vendu en sachets ; l'étiquette annonce 400 mg d'acide sorbique C₅H₇COOH (noté AH) par sachet, à 5 % près. On dissout entièrement un sachet dans l'eau pour obtenir V = 200 mL de solution S. On dose une prise d'essai V_A = 20,0 mL de S par une solution d'hydroxyde de sodium de concentration C_B = 2,0 × 10⁻² mol/L, en suivant le pH (figure). Données à 25 °C : M(AH) = 112 g/mol ; pKa(AH/A⁻) = 4,8 ; pKe = 14.",
  "دابا نقراو l'énoncé. واحد le conservateur alimentaire كيتباع ف des sachets. l'étiquette كتقول quatre cents milligrammes ديال l'acide sorbique فكل sachet، à cinq pour cent près. كنسميوه A H. كنذوبو sachet كامل فالما، و كنلقاو deux cents millilitres ديال la solution S. كناخدو vingt virgule zéro millilitres، و كنديرو ليهم le dosage ب la soude، C B égale deux virgule zéro fois dix puissance moins deux، mole par litre. و la figure كتعطي le p H en fonction de V B.",
  [FIG],
  ["Volume de la solution S : V = 200 mL", "Prise d'essai : V_A = 20,0 mL", "C_B = 2,0 × 10⁻² mol/L", "M(AH) = 112 g/mol", "pKa(AH/A⁻) = 4,8 ; pKe = 14", "À V_B = 3,5 mL : pH = 4,21"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Un autre sachet du même conservateur (étiquette : 400 mg à 5 % près) est dissous dans 200 mL d'eau. On dose V_A = 20,0 mL de la solution par la soude à C_B = 2,0 × 10⁻² mol/L (figure). À V_B = 3,2 mL, pH = 4,21. M = 112 g/mol ; pKa = 4,8.",
  "نفس التمرين، بقيم أخرى. sachet آخر، ذاب ف deux cents millilitres، و نفس le dosage. ف trois virgule deux millilitres، le p H égale quatre virgule vingt et un.",
  [sFIG],
  ["V = 200 mL ; V_A = 20,0 mL", "C_B = 2,0 × 10⁻² mol/L", "M = 112 g/mol ; pKa = 4,8", "À V_B = 3,2 mL : pH = 4,21"],
  SIM_Q)

ecrire(EX)
