# Exercice de chimie, ch. 13 (réactions acido-basiques), niveau facile : le produit ionique de l'eau Ke, une solution
# d'hydroxyde de sodium ([HO⁻], [H₃O⁺], pH, nature), puis [HO⁻] dans une solution acide.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2020 N (2.2 [HO⁻] d'une solution d'ammoniac), 2020 R (1.2 pH d'une base),
#    2022 R (1.3 τ d'une base par [HO⁻]), 2024 R (1.2 base, pKe), 2016 N (QCM sur Ke et le pH)
#    — backend/data/exams/physique/*/exam.json ;
#  - profs (architecture/phys_ch13_acides_bases.md § 1 : Naceiri Mrabti, El Goufifa, fiche pédagogique 5 h,
#    Prof Bazhar en vidéo) : Ke tiré de mesures, [HO⁻] = Ke/[H₃O⁺], neutre/acide/basique ; piège relevé :
#    écrire [HO⁻] = 10^(−pH) (c'est [H₃O⁺]) ;
#  - séries en ligne repérées (titres et résumés lus ; PDF non ouverts, hôtes hors du réseau de la session) :
#    talamidi « transformations liées à des réactions acide-base » exercices non corrigés 2 et 5, et activités 1 ;
#    moutamadris « Fiche exercices » 2bac sp international (17-2) et cours BIOF ; pc1.ma, exercices Pr. Chargui ;
#    alloschool (El Goufifa, séance 15).
# Ici : nos propres concentrations (C = 2,0 × 10⁻³ mol/L ; le cours prend 10⁻², 10⁻³, 10⁻⁴) et notre propre pH.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch13 import *

KE = 1.0e-14
C, PH2 = 2.0e-3, 2.6
HO = C
H3O = KE / HO
PH = -math.log10(H3O)
HO2 = 10 ** (PH2 - 14)
assert abs(H3O - 5.0e-12) < 1e-20 and abs(PH - 11.30) < 0.01 and abs(HO2 - 3.98e-12) < 1e-13

sC, sPH2 = 5.0e-4, 3.2
sH3O = KE / sC
sPH = -math.log10(sH3O)
sHO2 = 10 ** (sPH2 - 14)
assert abs(sH3O - 2.0e-11) < 1e-19 and abs(sPH - 10.70) < 0.01 and abs(sHO2 - 1.58e-11) < 1e-13

FIG = {"type": "schema", "titre": "Deux solutions à 25 °C", "cadre": {"l": 6, "h": 2.6},
       "elements": [
         {"f": "rect", "de": [0.6, 0.3], "a": [2.2, 1.7], "couleur": "blanc", "remplir": "faible"},
         {"f": "texte", "at": [1.4, 2.1], "t": "S : soude", "couleur": "cyan", "ancre": "centre"},
         {"f": "texte", "at": [1.4, 1.0], "t": "C = 2,0 × 10^{-3} mol/L", "ancre": "centre", "taille": "petit"},
         {"f": "rect", "de": [3.8, 0.3], "a": [5.4, 1.7], "couleur": "blanc", "remplir": "faible"},
         {"f": "texte", "at": [4.6, 2.1], "t": "S′ : jus dilué", "couleur": "jaune", "ancre": "centre"},
         {"f": "texte", "at": [4.6, 1.0], "t": "pH = 2,6", "ancre": "centre", "taille": "petit"}]}

QUESTIONS = [
  Q("1", "La dissolution de l'hydroxyde de sodium dans l'eau est totale : NaOH(s) → Na⁺(aq) + HO⁻(aq). Déterminer la concentration [HO⁻] dans la solution S.",
    "السؤال un: la dissolution ديال l'hydroxyde de sodium فالما totale. حدد la concentration des ions H O moins فla solution S.",
    val("[HO⁻]", HO, "mol/L", "[HO⁻] = C = 2,0 × 10⁻³ mol/L"),
    (["[HO⁻] = C", "NaOH → Na⁺ + HO⁻", "mol/L"], ["[HO⁻] = 10^(−pH)", "[HO⁻] = C/2"]),
    [("Regarde l'équation de dissolution : combien d'ions HO⁻ donne chaque NaOH dissous ? La dissolution est totale.",
      "شوف l'équation ديال la dissolution: كل N a O H كيعطي شحال من ion H O moins؟ و la dissolution totale."),
     ("Une mole de NaOH donne une mole d'ions HO⁻ : [HO⁻] = C.",
      "une mole ديال N a O H كتعطي une mole ديال les ions H O moins. إذن la concentration des ions H O moins égale C.")],
    [("1 : la dissolution est totale et une mole de NaOH donne une mole de HO⁻", "la dissolution totale"),
     ("[HO⁻] = C = 2,0 × 10⁻³ mol/L", "égale C، يعني deux virgule zéro fois dix puissance moins trois")],
    "السؤال un. la dissolution totale، و une mole ديال N a O H كتعطي une mole ديال les ions H O moins. إذن la concentration des ions H O moins égale C، يعني deux virgule zéro fois dix puissance moins trois، mole par litre.",
    "ex_1", "fa_1"),
  Q("2", "Calculer la concentration [H₃O⁺] dans la solution S. On donne Ke = 1,0 × 10⁻¹⁴ à 25 °C.",
    "السؤال deux: حسب la concentration des ions H trois O plus فla solution S. عندنا K e égale un virgule zéro fois dix puissance moins quatorze.",
    val("[H₃O⁺]", H3O, "mol/L", "[H₃O⁺] = Ke/[HO⁻] = 1,0 × 10⁻¹⁴ / 2,0 × 10⁻³ = 5,0 × 10⁻¹² mol/L"),
    (["Ke = [H₃O⁺]·[HO⁻]", "Ke", "10⁻¹⁴", "mol/L"], ["[H₃O⁺] = [HO⁻]", "[H₃O⁺] = Ke·[HO⁻]"]),
    [("Dans toute solution aqueuse à 25 °C, le produit [H₃O⁺]·[HO⁻] garde la même valeur : laquelle ?",
      "فكل solution aqueuse، à vingt-cinq degrés، le produit ديال les deux concentrations ما كيتبدلش. شنو هو؟"),
     ("Ke = [H₃O⁺]·[HO⁻], donc [H₃O⁺] = Ke/[HO⁻].",
      "K e égale la concentration des ions H trois O plus، fois la concentration des ions H O moins. إذن la concentration des ions H trois O plus، égale K e sur la concentration des ions H O moins.")],
    [("2 : Ke = [H₃O⁺]·[HO⁻] donc [H₃O⁺] = Ke/[HO⁻]", "égale K e sur la concentration des ions H O moins"),
     ("[H₃O⁺] = 1,0 × 10⁻¹⁴ / 2,0 × 10⁻³", "dix puissance moins quatorze، sur deux virgule zéro fois dix puissance moins trois"),
     ("[H₃O⁺] = 5,0 × 10⁻¹² mol/L", "cinq virgule zéro fois dix puissance moins douze")],
    "السؤال deux. K e égale le produit ديال les deux concentrations، إذن la concentration des ions H trois O plus، égale K e sur la concentration des ions H O moins. l'application numérique: un virgule zéro fois dix puissance moins quatorze، sur deux virgule zéro fois dix puissance moins trois. le résultat: cinq virgule zéro fois dix puissance moins douze، mole par litre.",
    "ex_2", "fa_2"),
  Q("3", "Calculer le pH de la solution S, puis préciser si elle est acide, neutre ou basique.",
    "السؤال trois: حسب le p H ديال la solution S، ومن بعد قول واش هي acide، neutre ولا basique.",
    val("pH", PH, None, "pH = −log[H₃O⁺] = −log(5,0 × 10⁻¹²) = 11,3 ; pH > 7 : S est basique", tol=0.01),
    (["pH = −log[H₃O⁺]", "log", "basique", "7"], ["pH = −log[HO⁻]", "pH = log[H₃O⁺]"]),
    [("Le pH se calcule avec la concentration des ions H₃O⁺, celle que tu viens de trouver.",
      "le p H كنحسبوه ب la concentration des ions H trois O plus، اللي يالاه لقيتي."),
     ("pH = −log[H₃O⁺] ; à 25 °C, une solution est basique si son pH est supérieur à 7.",
      "p H égale moins log de la concentration des ions H trois O plus. و à vingt-cinq degrés، la solution basique يلا كان le p H supérieur à sept.")],
    [("3 : pH = −log[H₃O⁺] = −log(5,0 × 10⁻¹²)", "p H égale moins log"),
     ("pH = 11,3", "le p H égale onze virgule trois"),
     ("pH > 7 à 25 °C : la solution S est basique", "la solution S basique")],
    "السؤال trois. p H égale moins log de la concentration des ions H trois O plus، يعني moins log de cinq virgule zéro fois dix puissance moins douze. le p H égale onze virgule trois. كبر من sept، à vingt-cinq degrés، إذن la solution S basique.",
    "ex_3", "fa_3"),
  Q("4", "Une solution S′ (jus de citron dilué) a un pH = 2,6 à 25 °C. Calculer la concentration [HO⁻] dans S′.",
    "السؤال quatre: la solution S prime، عندها p H égale deux virgule six. حسب la concentration des ions H O moins فيها.",
    val("[HO⁻]", HO2, "mol/L", "[HO⁻] = Ke/[H₃O⁺] = 10^(pH − 14) = 10^(−11,4) = 4,0 × 10⁻¹² mol/L"),
    (["[HO⁻] = Ke/[H₃O⁺]", "[H₃O⁺] = 10^(−pH)", "10^(pH − 14)", "mol/L"], ["[HO⁻] = 10^(−pH)", "[HO⁻] = 10^(−2,6)"]),
    [("Une solution acide contient aussi des ions HO⁻, très peu. Ke relie encore les deux concentrations.",
      "حتى la solution acide فيها les ions H O moins، ولكن قليلين بزاف. و K e باقي كيربط les deux concentrations."),
     ("[H₃O⁺] = 10^(−pH), puis [HO⁻] = Ke/[H₃O⁺], c'est-à-dire [HO⁻] = 10^(pH − 14). Attention : 10^(−pH) est [H₃O⁺], pas [HO⁻].",
      "la concentration des ions H trois O plus égale dix puissance moins p H. و la concentration des ions H O moins، égale K e sur la concentration des ions H trois O plus، يعني dix puissance p H moins quatorze. رد البال: dix puissance moins p H هي ديال les ions H trois O plus.")],
    [("4 : [HO⁻] = Ke/[H₃O⁺] = 10^(pH − 14)", "égale dix puissance p H moins quatorze"),
     ("[HO⁻] = 10^(2,6 − 14) = 10^(−11,4)", "dix puissance moins onze virgule quatre"),
     ("[HO⁻] = 4,0 × 10⁻¹² mol/L", "quatre virgule zéro fois dix puissance moins douze")],
    "السؤال quatre. la concentration des ions H O moins، égale K e sur la concentration des ions H trois O plus، يعني égale dix puissance p H moins quatorze. l'application numérique: dix puissance moins onze virgule quatre. le résultat: quatre virgule zéro fois dix puissance moins douze، mole par litre. قليلة بزاف، ولكن ماشي zéro.",
    "ex_4", "fa_4"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : la soude donne tous ses ions HO⁻",
      "Dissolution totale : une mole de NaOH donne une mole d'ions HO⁻, donc [HO⁻] = C.",
      "acides-bases-tableau/eau.html?vue=soude", "Une solution d'hydroxyde de sodium",
      "هادي la soude، يعني solution d'hydroxyde de sodium. l'équation de la dissolution: N a O H solide، simple flèche، N a plus، plus H O moins. فla simulation، C égale un virgule zéro fois dix puissance moins deux، mole par litre. la soude كتذوب كاملة، إذن la concentration des ions H O moins، égale C. فالتمرين ديالنا، C égale deux virgule zéro fois dix puissance moins trois، mole par litre. إذن la concentration des ions H O moins égale deux virgule zéro fois dix puissance moins trois، mole par litre.",
      [("NaOH(s) → Na⁺(aq) + HO⁻(aq)", "l'équation de la dissolution"), ("[HO⁻] = C = 2,0 × 10⁻³ mol/L", "إذن la concentration des ions H O moins égale deux virgule zéro")],
      [("هادي la soude", "moment:flacon"), ("la soude كتذوب كاملة", "moment:ho")]),
  sim("ex_2", "Question 2 : Ke relie [H₃O⁺] et [HO⁻]",
      "Ke = [H₃O⁺]·[HO⁻] = 1,0 × 10⁻¹⁴ à 25 °C, dans toute solution aqueuse.",
      "acides-bases-tableau/eau.html?vue=ke", "Le produit ionique de l'eau",
      "دابا نضربو les deux concentrations. le produit ionique de l'eau: K e، égale la concentration des ions H trois O plus، fois la concentration des ions H O moins. فالما الصافي: un virgule zéro fois dix puissance moins sept، fois un virgule zéro fois dix puissance moins sept، égale un virgule zéro fois dix puissance moins quatorze. à vingt-cinq degrés، K e égale dix puissance moins quatorze. وهاد la relation صحيحة ف كل solution aqueuse. فالتمرين ديالنا: la concentration des ions H trois O plus، égale K e sur la concentration des ions H O moins، يعني dix puissance moins quatorze، sur deux virgule zéro fois dix puissance moins trois، égale cinq virgule zéro fois dix puissance moins douze، mole par litre.",
      [("[H₃O⁺] = Ke/[HO⁻]", "فالتمرين ديالنا"), ("[H₃O⁺] = 5,0 × 10⁻¹² mol/L", "égale cinq virgule zéro fois dix puissance moins douze")],
      [("دابا نضربو les deux concentrations", "moment:produit"), ("فالما الصافي", "moment:calcul"),
       ("à vingt-cinq degrés، K e égale", "moment:valeur"), ("وهاد la relation صحيحة", "moment:toute_solution")]),
  sim("ex_3", "Question 3 : le pH, puis la nature de la solution",
      "pH = −log[H₃O⁺] ; à 25 °C, pH > 7 : solution basique.",
      "acides-bases-tableau/eau.html?vue=soude", "Du [H₃O⁺] au pH",
      "رجع ل la soude ديال la simulation: la concentration des ions H trois O plus، égale dix puissance moins douze. إذن le p H، égale moins log de dix puissance moins douze، égale douze. شوف l'afficheur: douze virgule zéro zéro. كبر من sept، إذن la solution basique. فالتمرين ديالنا: p H égale moins log de cinq virgule zéro fois dix puissance moins douze، égale onze virgule trois. حتى هو كبر من sept: la solution S basique.",
      [("pH = −log(5,0 × 10⁻¹²) = 11,3", "égale onze virgule trois"), ("pH > 7 : S basique", "la solution S basique")],
      [("رجع ل la soude", "moment:h3o"), ("إذن le p H", "moment:ph"), ("شوف l'afficheur", "moment:afficheur")]),
  sim("ex_4", "Question 4 : [HO⁻] dans une solution acide",
      "[HO⁻] = Ke/[H₃O⁺] = 10^(pH − 14) ; et non 10^(−pH).",
      "acides-bases-tableau/eau.html?vue=ho", "Les ions HO⁻ d'une solution acide",
      "ب K e، كنلقاو la concentration des ions H O moins. la relation: la concentration des ions H O moins، égale K e، sur la concentration des ions H trois O plus. فla simulation، l'acide éthanoïque، p H trois virgule quarante et un: كنلقاو deux virgule cinquante-sept fois dix puissance moins onze، mole par litre. قليلة بزاف، ولكن ماشي zéro. الشكل ديال le p H: la concentration des ions H O moins، égale dix puissance p H moins quatorze. رد البال: dix puissance moins p H، هي ديال les ions H trois O plus. فالتمرين ديالنا، p H égale deux virgule six: dix puissance moins onze virgule quatre، يعني quatre virgule zéro fois dix puissance moins douze، mole par litre.",
      [("[HO⁻] = 10^(pH − 14)", "الشكل ديال le p H"), ("[HO⁻] = 10^(−11,4) = 4,0 × 10⁻¹² mol/L", "يعني quatre virgule zéro fois dix puissance moins douze")],
      [("la relation: la concentration des ions H O moins", "moment:relation"), ("فla simulation، l'acide éthanoïque", "moment:acide"),
       ("الشكل ديال le p H", "moment:forme_ph"), ("رد البال", "moment:piege")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : [HO⁻] de la soude", "نتمرنو بسؤال ساهل. اختار la bonne valeur.",
      "Soude de concentration C = 2,0 × 10⁻³ mol/L, dissolution totale. [HO⁻] vaut…",
      ["1,0 × 10⁻³ mol/L", "2,0 × 10⁻³ mol/L", "5,0 × 10⁻¹² mol/L"], 1, {
        1: ("juste", "برافو! la dissolution totale، و كل N a O H كيعطي un ion H O moins. إذن la concentration des ions H O moins égale C.", "Juste : une mole de NaOH donne une mole de HO⁻ : [HO⁻] = C."),
        0: (("ما تقلقش. قسمتي C sur deux، ولكن ماكاين حتى deux فl'équation قدام H O moins. عاود اختار.", "Pas de coefficient 2 devant HO⁻ dans l'équation. Réessaie."),
            ("الجواب هو deux virgule zéro fois dix puissance moins trois mole par litre: une mole ديال N a O H كتعطي une mole ديال H O moins.", "Réponse : [HO⁻] = C = 2,0 × 10⁻³ mol/L.")),
        2: (("رد البال: هادي هي la concentration des ions H trois O plus، ماشي H O moins. عاود اختار.", "Cette valeur est celle de [H₃O⁺]. Réessaie."),
            ("الجواب هو deux virgule zéro fois dix puissance moins trois mole par litre. cinq virgule zéro fois dix puissance moins douze هي ديال les ions H trois O plus.", "Réponse : [HO⁻] = C = 2,0 × 10⁻³ mol/L."))},
      "Soude de concentration C égale deux virgule zéro fois dix puissance moins trois mole par litre, dissolution totale. La concentration des ions H O moins vaut ?"),
  qcm("fa_2", "Plus facile : utiliser Ke", "سؤال ساهل على K e. اختار la bonne relation.",
      "Quelle relation donne [H₃O⁺] quand on connaît [HO⁻] ?",
      ["[H₃O⁺] = Ke·[HO⁻]", "[H₃O⁺] = [HO⁻]", "[H₃O⁺] = Ke/[HO⁻]"], 2, {
        2: ("juste", "برافو! K e égale le produit ديال les deux concentrations، إذن كنقسمو K e على la concentration des ions H O moins.", "Juste : Ke = [H₃O⁺]·[HO⁻] donc [H₃O⁺] = Ke/[HO⁻]."),
        0: (("قريب، ولكن K e هو le produit. باش نلقاو وحدة، كنقسمو، ماشي كنضربو. عاود اختار.", "Ke est le produit des deux : pour en trouver une, on divise. Réessaie."),
            ("الجواب هو K e sur la concentration des ions H O moins، حيت K e égale le produit.", "Réponse : [H₃O⁺] = Ke/[HO⁻].")),
        1: (("لا، les deux concentrations متساويين غير فla solution neutre. هنا la soude basique. عاود اختار.", "Les deux sont égales seulement dans une solution neutre. Réessaie."),
            ("الجواب هو K e sur la concentration des ions H O moins. التساوي غير فla solution neutre.", "Réponse : [H₃O⁺] = Ke/[HO⁻] ; l'égalité n'est vraie qu'en solution neutre."))},
      "Quelle relation donne la concentration des ions H trois O plus, quand on connaît la concentration des ions H O moins ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "Solution S : [H₃O⁺] = 5,0 × 10⁻¹² mol/L, à 25 °C.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("pH = −log[H₃O⁺] = 11,3.", True, "−log(5,0 × 10⁻¹²) = 11,3."),
      ("Comme pH > 7, la solution S est acide.", False, "À 25 °C, pH > 7 signifie basique ; acide, c'est pH < 7."),
      ("Dans S, [HO⁻] est plus grande que [H₃O⁺].", True, "2,0 × 10⁻³ mol/L contre 5,0 × 10⁻¹² mol/L : c'est une solution basique.")]),
  qcm("fa_4", "Plus facile : [HO⁻] à partir du pH", "سؤال ساهل: اختار la bonne expression.",
      "Une solution a un pH = 2,6 à 25 °C. [HO⁻] s'écrit…",
      ["10^(−2,6)", "10^(2,6 − 14)", "10^(14 − 2,6)"], 1, {
        1: ("juste", "برافو! la concentration des ions H O moins، égale K e sur la concentration des ions H trois O plus، يعني dix puissance p H moins quatorze.", "Juste : [HO⁻] = Ke/[H₃O⁺] = 10^(pH − 14)."),
        0: (("رد البال: dix puissance moins p H هي la concentration des ions H trois O plus. عاود اختار.", "10^(−pH), c'est [H₃O⁺]. Réessaie."),
            ("الجواب هو dix puissance deux virgule six moins quatorze. dix puissance moins p H هي ديال les ions H trois O plus.", "Réponse : [HO⁻] = 10^(pH − 14) = 10^(−11,4).")),
        2: (("شوف: dix puissance onze virgule quatre عدد كبير بزاف، ما يمكنش يكون concentration. عاود اختار.", "10^(11,4) mol/L est impossible. Réessaie."),
            ("الجواب هو dix puissance p H moins quatorze، يعني dix puissance moins onze virgule quatre.", "Réponse : [HO⁻] = 10^(2,6 − 14) = 10^(−11,4)."))},
      "Une solution a un p H égale deux virgule six. La concentration des ions H O moins s'écrit ?"),
]

SIM_Q = [
  QS("1", "Dissolution totale de NaOH. Déterminer [HO⁻] dans S.",
     val("[HO⁻]", sC, "mol/L", "[HO⁻] = C = 5,0 × 10⁻⁴ mol/L"),
     (["[HO⁻] = C", "mol/L"], ["[HO⁻] = 10^(−pH)"]),
     [("[HO⁻] = C = 5,0 × 10⁻⁴ mol/L", "égale C")],
     "la dissolution totale، إذن la concentration des ions H O moins égale C، يعني cinq virgule zéro fois dix puissance moins quatre، mole par litre."),
  QS("2", "Calculer [H₃O⁺] dans S (Ke = 1,0 × 10⁻¹⁴).",
     val("[H₃O⁺]", sH3O, "mol/L", "[H₃O⁺] = Ke/[HO⁻] = 1,0 × 10⁻¹⁴ / 5,0 × 10⁻⁴ = 2,0 × 10⁻¹¹ mol/L"),
     (["Ke = [H₃O⁺]·[HO⁻]", "mol/L"], ["[H₃O⁺] = Ke·[HO⁻]"]),
     [("[H₃O⁺] = Ke/[HO⁻]", "K e sur la concentration des ions H O moins"), ("[H₃O⁺] = 2,0 × 10⁻¹¹ mol/L", "deux virgule zéro fois dix puissance moins onze")],
     "la concentration des ions H trois O plus، égale K e sur la concentration des ions H O moins، يعني deux virgule zéro fois dix puissance moins onze، mole par litre."),
  QS("3", "Calculer le pH de S et préciser sa nature.",
     val("pH", sPH, None, "pH = −log(2,0 × 10⁻¹¹) = 10,7 ; pH > 7 : S est basique", tol=0.01),
     (["pH = −log[H₃O⁺]", "basique"], ["pH = −log[HO⁻]"]),
     [("pH = −log(2,0 × 10⁻¹¹) = 10,7", "dix virgule sept"), ("pH > 7 : basique", "basique")],
     "p H égale moins log de deux virgule zéro fois dix puissance moins onze، égale dix virgule sept. كبر من sept، إذن la solution basique."),
  QS("4", "Une solution S′ a un pH = 3,2. Calculer [HO⁻] dans S′.",
     val("[HO⁻]", sHO2, "mol/L", "[HO⁻] = 10^(pH − 14) = 10^(−10,8) = 1,6 × 10⁻¹¹ mol/L"),
     (["[HO⁻] = Ke/[H₃O⁺]", "10^(pH − 14)", "mol/L"], ["[HO⁻] = 10^(−pH)"]),
     [("[HO⁻] = 10^(pH − 14) = 10^(−10,8)", "dix puissance p H moins quatorze"), ("[HO⁻] = 1,6 × 10⁻¹¹ mol/L", "un virgule six fois dix puissance moins onze")],
     "la concentration des ions H O moins، égale dix puissance p H moins quatorze، يعني dix puissance moins dix virgule huit، égale un virgule six fois dix puissance moins onze، mole par litre."),
]

sFIG = {"type": "schema", "titre": "Deux solutions à 25 °C", "cadre": {"l": 6, "h": 2.6},
        "elements": [
          {"f": "rect", "de": [0.6, 0.3], "a": [2.2, 1.7], "couleur": "blanc", "remplir": "faible"},
          {"f": "texte", "at": [1.4, 2.1], "t": "S : soude", "couleur": "cyan", "ancre": "centre"},
          {"f": "texte", "at": [1.4, 1.0], "t": "C = 5,0 × 10^{-4} mol/L", "ancre": "centre", "taille": "petit"},
          {"f": "rect", "de": [3.8, 0.3], "a": [5.4, 1.7], "couleur": "blanc", "remplir": "faible"},
          {"f": "texte", "at": [4.6, 2.1], "t": "S′", "couleur": "jaune", "ancre": "centre"},
          {"f": "texte", "at": [4.6, 1.0], "t": "pH = 3,2", "ancre": "centre", "taille": "petit"}]}

EX = exercice(
  "phys_ex_ch13_acides_bases_1", "phys_ch13_acides_bases", "acides_bases",
  "Une solution de soude et un jus dilué : Ke, [HO⁻] et pH", "facile", 15,
  ["Déterminer [HO⁻] d'une solution d'hydroxyde de sodium", "Utiliser Ke = [H₃O⁺]·[HO⁻]", "Calculer un pH et dire si une solution est acide, neutre ou basique", "Calculer [HO⁻] à partir du pH"],
  "Toutes les solutions sont à 25 °C. On prépare une solution S d'hydroxyde de sodium (soude) de concentration C = 2,0 × 10⁻³ mol/L. On dispose aussi d'une solution S′, un jus de citron dilué, dont le pH-mètre indique pH = 2,6.",
  "دابا نقراو l'énoncé. كاع les solutions à vingt-cinq degrés. عندنا la solution S ديال l'hydroxyde de sodium، يعني la soude، la concentration ديالها C égale deux virgule zéro fois dix puissance moins trois، mole par litre. وعندنا la solution S prime، جوس ديال الحامض مخفف، le p H mètre كيعطي deux virgule six.",
  [FIG],
  ["C = 2,0 × 10⁻³ mol/L (soude, solution S)", "pH(S′) = 2,6", "Ke = 1,0 × 10⁻¹⁴ à 25 °C", "NaOH(s) → Na⁺(aq) + HO⁻(aq) (dissolution totale)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "À 25 °C, une solution S de soude a pour concentration C = 5,0 × 10⁻⁴ mol/L. Une solution S′ a un pH = 3,2.",
  "نفس التمرين، بقيم أخرى. la soude، C égale cinq virgule zéro fois dix puissance moins quatre، mole par litre. و la solution S prime، p H égale trois virgule deux.",
  [sFIG],
  ["C = 5,0 × 10⁻⁴ mol/L", "pH(S′) = 3,2", "Ke = 1,0 × 10⁻¹⁴ à 25 °C"],
  SIM_Q)

ecrire(EX)
