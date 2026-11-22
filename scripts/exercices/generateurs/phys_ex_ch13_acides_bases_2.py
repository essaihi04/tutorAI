# Exercice de chimie, ch. 13 (réactions acido-basiques), niveau facile : pKa à partir de Ka, la relation
# pH = pKa + log([A⁻]/[AH]), l'espèce prédominante et le pourcentage de la forme basique.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2021 R (6 rapport [A⁻]/[AH] à partir du pH, 7 espèce prédominante),
#    2019 N (2.6 pKa, 2.7 espèce prédominante), 2018 N (1.5 rapport puis espèce prédominante), 2022 N (2.5
#    pourcentage de la forme acide), 2024 R (1.2.3 pH pour un pourcentage donné) — backend/data/exams/physique ;
#  - profs (architecture/phys_ch13_acides_bases.md § 1 : Naceiri Mrabti, El Goufifa, fiche 5 h, Prof Bazhar) :
#    pKa = −log Ka, pH = pKa + log, domaines de prédominance puis distribution ; piège : inverser le rapport ;
#  - séries en ligne repérées (titres et résumés lus ; PDF non ouverts, hôtes hors du réseau de la session) :
#    talamidi exercices non corrigés 2 (prédominance, distribution, τ et Ka) et 5 (τ en fonction de pKa et pH),
#    moutamadris « Fiche exercices » (17-2), pc1.ma exercices Pr. Chargui, alloschool El Goufifa séance 15.
# Ici : le couple de l'acide chloroéthanoïque (pKa 2,9), notre pH ; le cours prend l'acide éthanoïque (4,8).
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch13 import *

KA, PH = 1.26e-3, 3.5
PKA = -math.log10(KA)
R = 10 ** (PH - round(PKA, 1))
PCT = 100 * R / (1 + R)
assert abs(PKA - 2.90) < 0.005 and abs(R - 3.98) < 0.01 and abs(PCT - 79.9) < 0.1

sKA, sPH = 6.3e-5, 3.6
sPKA = -math.log10(sKA)
sR = 10 ** (sPH - round(sPKA, 1))
sPCT = 100 * sR / (1 + sR)
assert abs(sPKA - 4.20) < 0.005 and abs(sR - 0.251) < 0.001 and abs(sPCT - 20.1) < 0.1

def axe_ph(pka, ph, nom_a, nom_b, titre):
    return {"type": "schema", "titre": titre, "cadre": {"l": 14, "h": 3},
            "elements": [
              {"f": "fleche", "de": [0, 1], "a": [14, 1], "couleur": "blanc"},
              {"f": "texte", "at": [13.6, 0.4], "t": "pH", "ancre": "centre"},
              {"f": "texte", "at": [0.2, 0.4], "t": "0", "ancre": "centre", "taille": "petit"},
              {"f": "texte", "at": [7, 0.4], "t": "7", "ancre": "centre", "taille": "petit"},
              {"f": "ligne", "pts": [[pka, 0.7], [pka, 2.3]], "couleur": "jaune", "epais": True},
              {"f": "texte", "at": [pka, 2.6], "t": f"pKa = ?", "couleur": "jaune", "ancre": "centre"},
              {"f": "point", "at": [ph, 1], "t": f"S", "pos": "s", "couleur": "cyan"},
              {"f": "texte", "at": [max(pka / 2, 0.8), 1.7], "t": nom_a, "couleur": "rose", "ancre": "centre", "taille": "petit"},
              {"f": "texte", "at": [(pka + 13) / 2, 1.7], "t": nom_b, "couleur": "vert", "ancre": "centre", "taille": "petit"}]}

FIG = axe_ph(2.9, PH, "ClCH₂COOH", "ClCH₂COO⁻", "Axe des pH : le couple et la solution S")
sFIG = axe_ph(4.2, sPH, "C₆H₅COOH", "C₆H₅COO⁻", "Axe des pH : le couple et la solution S")

QUESTIONS = [
  Q("1", "Calculer le pKa du couple ClCH₂COOH(aq)/ClCH₂COO⁻(aq).",
    "السؤال un: حسب le p K a ديال le couple، l'acide chloroéthanoïque، l'ion chloroéthanoate.",
    val("pKa", PKA, None, "pKa = −log Ka = −log(1,26 × 10⁻³) = 2,9", tol=0.02),
    (["pKa = −log Ka", "Ka", "log"], ["pKa = log Ka", "pKa = 10^(−Ka)"]),
    [("Le pKa est défini à partir de Ka avec un logarithme décimal : n'oublie pas le signe.",
      "le p K a كنعرفوه من K a ب log. ما تنساش le signe moins."),
     ("pKa = −log Ka.", "p K a égale moins log de K a.")],
    [("1 : pKa = −log Ka", "p K a égale moins log de K a"),
     ("pKa = −log(1,26 × 10⁻³)", "moins log de un virgule vingt-six fois dix puissance moins trois"),
     ("pKa = 2,9", "p K a égale deux virgule neuf")],
    "السؤال un. p K a égale moins log de K a، يعني moins log de un virgule vingt-six fois dix puissance moins trois. p K a égale deux virgule neuf.",
    "ex_1", "fa_1"),
  Q("2", "Une solution S de ce couple a un pH = 3,5. Montrer que [A⁻]éq/[AH]éq = 10^(pH − pKa), puis calculer ce rapport (A⁻ = ClCH₂COO⁻, AH = ClCH₂COOH).",
    "السؤال deux: la solution S عندها p H égale trois virgule cinq. بين بلي le rapport A moins sur A H، égale dix puissance p H moins p K a، ومن بعد حسبو.",
    val("[A⁻]/[AH]", R, None, "pH = pKa + log([A⁻]/[AH]) donc [A⁻]/[AH] = 10^(pH − pKa) = 10^(3,5 − 2,9) = 4,0"),
    (["pH = pKa + log([A⁻]/[AH])", "10^(pH − pKa)", "log"], ["10^(pKa − pH)", "[AH]/[A⁻]"]),
    [("Pars de l'expression de Ka et prends −log des deux côtés : −log Ka = pKa, −log[H₃O⁺] = pH.",
      "بدا من l'expression ديال K a، و خود moins log من الجهتين: moins log de K a هو p K a، و moins log de la concentration des ions H trois O plus هو p H."),
     ("Tu obtiens pH = pKa + log([A⁻]/[AH]), donc log([A⁻]/[AH]) = pH − pKa.",
      "كتلقى p H égale p K a، plus log de A moins sur A H. إذن log du rapport égale p H moins p K a.")],
    [("2 : Ka = [A⁻]·[H₃O⁺]/[AH] ; −log : pKa = pH − log([A⁻]/[AH])", "خود moins log"),
     ("pH = pKa + log([A⁻]/[AH]) donc [A⁻]/[AH] = 10^(pH − pKa)", "dix puissance p H moins p K a"),
     ("[A⁻]/[AH] = 10^(3,5 − 2,9) = 10^0,6 = 4,0", "le rapport égale quatre")],
    "السؤال deux. K a égale A moins fois H trois O plus، sur A H. خود moins log من الجهتين: p K a égale p H، moins log de A moins sur A H. إذن p H égale p K a، plus log du rapport، و le rapport égale dix puissance p H moins p K a. l'application numérique: dix puissance trois virgule cinq moins deux virgule neuf، يعني dix puissance zéro virgule six. le rapport égale quatre virgule zéro.",
    "ex_2", "fa_2"),
  Q("3", "En déduire l'espèce chimique prédominante dans la solution S. Justifier.",
    "السؤال trois: استنتج l'espèce prédominante فla solution S، و برر.",
    phrase("[A⁻]/[AH] = 4,0 > 1 (ou pH = 3,5 > pKa = 2,9) : la base ClCH₂COO⁻ prédomine."),
    (["pH > pKa", "[A⁻] > [AH]", "prédomine"], ["pH < 7 donc l'acide prédomine"]),
    [("Compare le pH de S au pKa du couple, ou le rapport trouvé à 1.",
      "قارن le p H ديال S مع le p K a، ولا le rapport مع un."),
     ("À droite du pKa (pH > pKa), c'est la base qui prédomine ; attention : « pH < 7 » ne dit rien ici.",
      "على اليمين ديال le p K a، يعني p H كبر من p K a، la base هي اللي prédomine. رد البال: p H صغر من sept ما كيقول والو هنا.")],
    [("3 : pH = 3,5 > pKa = 2,9, donc [A⁻] > [AH]", "كبر من p K a"),
     ("l'ion ClCH₂COO⁻ (forme basique) prédomine dans S", "la base prédomine")],
    "السؤال trois. p H égale trois virgule cinq، كبر من p K a égale deux virgule neuf. و le rapport quatre، كبر من un. إذن la base prédomine: l'ion chloroéthanoate. واخا la solution acide، حيت p H صغر من sept.",
    "ex_3", "fa_3"),
  Q("4", "Calculer le pourcentage de la forme basique A⁻ dans la solution S.",
    "السؤال quatre: حسب le pourcentage ديال la forme basique A moins فla solution S.",
    val("%A⁻", PCT, "%", "%A⁻ = [A⁻]/([A⁻] + [AH]) = r/(1 + r) = 4,0/5,0 = 80 %"),
    (["[A⁻]/([A⁻] + [AH])", "r/(1 + r)", "%"], ["r × 100", "1/(1 + r)"]),
    [("Le pourcentage de A⁻ compare [A⁻] à la somme des deux formes du couple.",
      "le pourcentage ديال A moins كيقارن A moins مع la somme ديال les deux formes."),
     ("Divise le haut et le bas par [AH] : %A⁻ = r/(1 + r), avec r = [A⁻]/[AH] = 4,0.",
      "قسم الفوق و التحت على A H: le pourcentage égale r sur un plus r، و r égale quatre.")],
    [("4 : %A⁻ = [A⁻]/([A⁻] + [AH]) = r/(1 + r)", "r sur un plus r"),
     ("%A⁻ = 4,0/(1 + 4,0)", "quatre sur cinq"),
     ("%A⁻ = 80 %", "quatre-vingts pour cent")],
    "السؤال quatre. le pourcentage ديال A moins، égale A moins sur la somme A moins plus A H. نقسمو على A H: r sur un plus r. l'application numérique: quatre sur cinq. le pourcentage égale quatre-vingts pour cent، و l'acide vingt pour cent.",
    "ex_4", "fa_4"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : du Ka au pKa", "pKa = −log Ka : un Ka grand donne un pKa petit.",
      "acides-bases-tableau/acidite.html?vue=pka", "Ka et pKa de deux couples",
      "K a غالبا كيكون صغير بزاف. باش نخدمو بعدد ساهل، كنعرفو le p K a. la définition: p K a égale moins log de K a. مثال ديال la simulation: l'acide éthanoïque، K a égale un virgule six fois dix puissance moins cinq، إذن p K a égale quatre virgule huit. شوف les deux flèches: K a كبير، p K a صغير. فالتمرين ديالنا: K a égale un virgule vingt-six fois dix puissance moins trois، إذن p K a égale deux virgule neuf.",
      [("pKa = −log Ka", "la définition: p K a égale moins log de K a"), ("pKa = −log(1,26 × 10⁻³) = 2,9", "إذن p K a égale deux virgule neuf")],
      [("la définition: p K a", "moment:definition"), ("مثال ديال la simulation", "moment:ethanoique"), ("شوف les deux flèches", "moment:sens")]),
  sim("ex_2", "Question 2 : pH = pKa + log([A⁻]/[AH])", "On prend −log de l'expression de Ka.",
      "acides-bases-tableau/predominance.html?vue=relation", "De Ka à la relation du pH",
      "عندنا l'expression ديال K a: K a égale la concentration de A moins، fois la concentration des ions H trois O plus، sur la concentration de A H. دابا ناخدو moins log من الجهتين. moins log de K a هو p K a، و moins log de la concentration des ions H trois O plus هو p H. وهادي هي la relation: p H égale p K a، plus log de A moins sur A H. فla simulation، مع le rapport dix، p H égale p K a plus un. فالتمرين ديالنا: log du rapport égale p H moins p K a، يعني trois virgule cinq moins deux virgule neuf، zéro virgule six. إذن le rapport égale dix puissance zéro virgule six، يعني quatre virgule zéro.",
      [("pH = pKa + log([A⁻]/[AH])", "وهادي هي la relation"), ("[A⁻]/[AH] = 10^0,6 = 4,0", "يعني quatre virgule zéro")],
      [("عندنا l'expression ديال K a", "moment:ka"), ("دابا ناخدو moins log", "moment:log"),
       ("وهادي هي la relation", "moment:relation"), ("فla simulation، مع le rapport dix", "moment:exemple")]),
  sim("ex_3", "Question 3 : de quel côté du pKa ?", "À gauche du pKa, l'acide prédomine ; à droite, la base.",
      "acides-bases-tableau/predominance.html?vue=domaines", "Les domaines de prédominance",
      "دابا نرسمو l'axe des p H. فوقو كنحطو un trait عند p K a ديال le couple، فla simulation quatre virgule huit. على اليسار، p H صغر من p K a، l'acide prédomine. على اليمين، p H كبر من p K a، la base prédomine. الخلاصة، la règle: à gauche du p K a، l'acide، à droite du p K a، la base. فالتمرين ديالنا، p K a égale deux virgule neuf، و p H ديال S égale trois virgule cinq: على اليمين. إذن la base prédomine، l'ion chloroéthanoate، واخا la solution acide.",
      [("pH = 3,5 > pKa = 2,9", "و p H ديال S égale trois virgule cinq"), ("ClCH₂COO⁻ prédomine", "إذن la base prédomine")],
      [("دابا نرسمو l'axe des p H", "moment:axe"), ("فوقو كنحطو un trait", "moment:pka"),
       ("على اليسار", "moment:domaine_acide"), ("على اليمين، p H كبر", "moment:domaine_base"), ("الخلاصة، la règle", "moment:regle")]),
  sim("ex_4", "Question 4 : le pourcentage d'une forme", "Les deux pourcentages font 100 % ; ils sont égaux à pH = pKa.",
      "acides-bases-tableau/predominance.html?vue=distribution", "Le diagramme de distribution",
      "شوف les axes: l'axe vertical فيه le pourcentage، و l'axe horizontal فيه le p H. la courbe rose هي l'acide، و la courbe verte هي la base. deux courbes كيتلاقاو ف cinquante pour cent، عند p H égale p K a. فla simulation، عند p H égale cinq virgule huit، يعني p K a plus un، la base تقريبا quatre-vingt-onze pour cent. فالتمرين ديالنا، le rapport r égale quatre: le pourcentage ديال la base، égale r sur un plus r، يعني quatre sur cinq، quatre-vingts pour cent.",
      [("%A⁻ = r/(1 + r)", "égale r sur un plus r"), ("%A⁻ = 4,0/5,0 = 80 %", "quatre-vingts pour cent")],
      [("شوف les axes", "moment:axes"), ("la courbe rose", "moment:courbe_acide"), ("و la courbe verte", "moment:courbe_base"),
       ("deux courbes كيتلاقاو", "moment:croisement"), ("فla simulation، عند p H", {"set": {"pH": 5.8}})]),
]

FACILES = [
  qcm("fa_1", "Plus facile : le pKa", "نتمرنو بسؤال ساهل. اختار la bonne relation.",
      "Quelle relation donne le pKa d'un couple ?",
      ["pKa = log Ka", "pKa = −log Ka", "pKa = 10^(−Ka)"], 1, {
        1: ("juste", "برافو! p K a égale moins log de K a. و K a صغير، إذن p K a موجب.", "Juste : pKa = −log Ka."),
        0: (("قريب! ولكن K a صغير بزاف، و log ديالو سالب. خاصنا le signe moins. عاود اختار.", "log Ka est négatif ici : il manque le signe moins. Réessaie."),
            ("الجواب هو p K a égale moins log de K a.", "Réponse : pKa = −log Ka.")),
        2: (("لا، dix puissance moins كتعطي K a من p K a، ماشي العكس. عاود اختار.", "C'est Ka = 10^(−pKa), la relation inverse. Réessaie."),
            ("الجواب هو p K a égale moins log de K a. و بالعكس، K a égale dix puissance moins p K a.", "Réponse : pKa = −log Ka (et Ka = 10^(−pKa))."))},
      "Quelle relation donne le p K a d'un couple ?"),
  qcm("fa_2", "Plus facile : le rapport", "سؤال ساهل. اختار la bonne expression.",
      "pH = 3,5 et pKa = 2,9. Le rapport [A⁻]/[AH] vaut…",
      ["10^(2,9 − 3,5)", "3,5 − 2,9", "10^(3,5 − 2,9)"], 2, {
        2: ("juste", "برافو! log du rapport égale p H moins p K a، إذن le rapport égale dix puissance zéro virgule six، يعني quatre.", "Juste : [A⁻]/[AH] = 10^(pH − pKa) = 10^0,6 ≈ 4,0."),
        0: (("قلبتي: هاد الشي كيعطي A H sur A moins. شوف la relation: p H égale p K a plus log de A moins sur A H. عاود اختار.", "C'est le rapport inverse [AH]/[A⁻]. Réessaie."),
            ("الجواب هو dix puissance p H moins p K a، يعني dix puissance zéro virgule six.", "Réponse : 10^(pH − pKa) = 10^0,6 ≈ 4,0.")),
        1: (("قريب! zéro virgule six هو log du rapport، ماشي le rapport. عاود اختار.", "0,6 est le log du rapport, pas le rapport. Réessaie."),
            ("الجواب هو dix puissance zéro virgule six: le rapport هو dix puissance log ديالو.", "Réponse : [A⁻]/[AH] = 10^0,6 ≈ 4,0."))},
      "p H égale trois virgule cinq et p K a égale deux virgule neuf. Le rapport A moins sur A H vaut ?"),
  assoc("fa_3", "Plus facile : associer", "Couple de pKa = 2,9 : relie chaque pH à l'espèce qui prédomine.",
        "سؤال ساهل: ربط كل p H مع l'espèce اللي كتحكم.",
        "Relie chaque solution (pKa = 2,9) à l'espèce prédominante.",
        [("1", "pH = 1,5"), ("2", "pH = 2,9"), ("3", "pH = 3,5")],
        [("a", "ClCH₂COOH prédomine"), ("b", "ClCH₂COO⁻ prédomine"), ("c", "[ClCH₂COOH] = [ClCH₂COO⁻]")],
        {"1": "a", "2": "c", "3": "b"},
        {"1-a": (True, "pH < pKa : à gauche du pKa, l'acide prédomine.", "برافو: p H صغر من p K a، على اليسار، l'acide prédomine."),
         "1-*": (False, "pH = 1,5 est à gauche du pKa : compare encore.", "لا. un virgule cinq صغر من p K a. شوف شكون كيحكم على اليسار."),
         "2-c": (True, "pH = pKa : log du rapport = 0, les deux formes sont égales.", "برافو: p H égale p K a، إذن les deux formes متساويين."),
         "2-*": (False, "pH = pKa exactement : que vaut alors log([A⁻]/[AH]) ?", "لا. هنا p H égale p K a بالضبط. شحال كيساوي log du rapport؟"),
         "3-b": (True, "pH > pKa : à droite du pKa, la base prédomine, même si la solution est acide.", "برافو: p H كبر من p K a، على اليمين، la base prédomine."),
         "3-*": (False, "3,5 est à droite du pKa = 2,9 : ne confonds pas « solution acide » et « l'acide prédomine ».", "لا. trois virgule cinq كبر من deux virgule neuf. ما تخلطش بين solution acide و l'acide prédomine.")},
        ("À gauche du pKa l'acide, au pKa les deux à égalité, à droite la base.", "على اليسار ديال p K a، l'acide. عند p K a، بحال بحال. على اليمين، la base.")),
  vf("fa_4", "Plus facile : vrai ou faux", "[A⁻]/[AH] = 4,0 dans la solution S.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Le pourcentage de A⁻ est 4,0/(1 + 4,0) = 80 %.", True, "%A⁻ = r/(1 + r) = 0,80."),
      ("Le pourcentage de A⁻ est 4,0 × 100 = 400 %.", False, "Un pourcentage ne dépasse pas 100 % : il faut diviser par la somme des deux formes."),
      ("Les pourcentages de AH et de A⁻ font 100 % ensemble.", True, "20 % + 80 % = 100 %.")]),
]

SIM_Q = [
  QS("1", "Calculer le pKa du couple C₆H₅COOH(aq)/C₆H₅COO⁻(aq) (Ka = 6,3 × 10⁻⁵).",
     val("pKa", sPKA, None, "pKa = −log(6,3 × 10⁻⁵) = 4,2", tol=0.02),
     (["pKa = −log Ka"], ["pKa = log Ka"]),
     [("pKa = −log Ka = −log(6,3 × 10⁻⁵)", "moins log de K a"), ("pKa = 4,2", "quatre virgule deux")],
     "p K a égale moins log de K a، يعني moins log de six virgule trois fois dix puissance moins cinq، égale quatre virgule deux."),
  QS("2", "S a un pH = 3,6. Montrer que [A⁻]/[AH] = 10^(pH − pKa) et calculer ce rapport.",
     val("[A⁻]/[AH]", sR, None, "[A⁻]/[AH] = 10^(3,6 − 4,2) = 10^(−0,6) = 0,25"),
     (["pH = pKa + log([A⁻]/[AH])"], ["10^(pKa − pH)"]),
     [("pH = pKa + log([A⁻]/[AH]) donc [A⁻]/[AH] = 10^(pH − pKa)", "dix puissance p H moins p K a"), ("[A⁻]/[AH] = 10^(−0,6) = 0,25", "zéro virgule vingt-cinq")],
     "p H égale p K a plus log du rapport، إذن le rapport égale dix puissance p H moins p K a، يعني dix puissance moins zéro virgule six، égale zéro virgule vingt-cinq."),
  QS("3", "En déduire l'espèce prédominante dans S. Justifier.",
     phrase("pH = 3,6 < pKa = 4,2 (rapport 0,25 < 1) : l'acide C₆H₅COOH prédomine."),
     (["pH < pKa", "prédomine"], ["pH < 7"]),
     [("pH < pKa : [AH] > [A⁻], C₆H₅COOH prédomine", "l'acide prédomine")],
     "p H صغر من p K a، و le rapport صغر من un، إذن l'acide prédomine، l'acide benzoïque."),
  QS("4", "Calculer le pourcentage de la forme basique A⁻ dans S.",
     val("%A⁻", sPCT, "%", "%A⁻ = r/(1 + r) = 0,25/1,25 = 20 %"),
     (["r/(1 + r)", "%"], ["r × 100"]),
     [("%A⁻ = r/(1 + r) = 0,25/1,25", "r sur un plus r"), ("%A⁻ = 20 %", "vingt pour cent")],
     "le pourcentage égale r sur un plus r، يعني zéro virgule vingt-cinq sur un virgule vingt-cinq، égale vingt pour cent."),
]

EX = exercice(
  "phys_ex_ch13_acides_bases_2", "phys_ch13_acides_bases", "acides_bases",
  "L'acide chloroéthanoïque : pKa, rapport et espèce prédominante", "facile", 15,
  ["Calculer pKa = −log Ka", "Établir et utiliser pH = pKa + log([A⁻]/[AH])", "Trouver l'espèce prédominante", "Calculer le pourcentage d'une forme du couple"],
  "À 25 °C, la constante d'acidité du couple acide chloroéthanoïque / ion chloroéthanoate, ClCH₂COOH(aq)/ClCH₂COO⁻(aq), vaut Ka = 1,26 × 10⁻³. Une solution S contenant ce couple a un pH = 3,5. On note AH l'acide et A⁻ sa base conjuguée.",
  "دابا نقراو l'énoncé. à vingt-cinq degrés، la constante d'acidité ديال le couple، l'acide chloroéthanoïque، l'ion chloroéthanoate، K a égale un virgule vingt-six fois dix puissance moins trois. la solution S فيها هاد le couple، و le p H ديالها trois virgule cinq. كنسميو l'acide A H، و la base A moins.",
  [FIG],
  ["Ka(ClCH₂COOH/ClCH₂COO⁻) = 1,26 × 10⁻³ à 25 °C", "pH(S) = 3,5"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "À 25 °C, le couple acide benzoïque / ion benzoate, C₆H₅COOH(aq)/C₆H₅COO⁻(aq), a pour constante d'acidité Ka = 6,3 × 10⁻⁵. Une solution S de ce couple a un pH = 3,6.",
  "نفس التمرين، بقيم أخرى. le couple، l'acide benzoïque، l'ion benzoate، K a égale six virgule trois fois dix puissance moins cinq. و la solution S، p H égale trois virgule six.",
  [sFIG],
  ["Ka(C₆H₅COOH/C₆H₅COO⁻) = 6,3 × 10⁻⁵", "pH(S) = 3,6"],
  SIM_Q)

ecrire(EX)
