# Exercice de chimie, ch. 13 (réactions acido-basiques), niveau moyen (celui du national) : réaction entre deux
# couples (acide benzoïque et ions méthanoate) — équation, « montrer que » K = 10^(pKa₂ − pKa₁), sens d'évolution
# par Qr,i, taux d'avancement final par K, puis pH du mélange à l'équilibre.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2023 N (2.1 à 2.3 : acide éthanoïque + ions méthanoate, Qr,éq en fonction de
#    Ka₁ et Ka₂, « trouver l'expression du pH en fonction de pKa₁ et pKa₂ »), 2020 R (2.1 à 2.5 : K en fonction des
#    Ka, Qr,i, sens d'évolution, pH du mélange), 2016 N (1.2 K de la réaction du dosage) — backend/data/exams/physique ;
#  - profs (architecture/phys_ch13_acides_bases.md § 1 : Naceiri Mrabti « K d'une réaction acide-base », El Goufifa,
#    fiche 5 h, Prof Bazhar) ; pièges relevés : mettre au numérateur le Ka du couple de la base qui réagit, oublier
#    que le sens se décide en comparant Qr,i à K ;
#  - séries en ligne repérées (titres et résumés lus ; PDF non ouverts, hôtes hors du réseau de la session) :
#    talamidi exercices non corrigés 2 et 5, moutamadris fiches 13-8 et 17-2, pc1.ma Pr. Chargui,
#    alloschool El Goufifa séance 15.
# Ici : acide benzoïque (pKa 4,2) et ions méthanoate (pKa 3,75), mélange équimolaire sans produits ; le cours prend
# l'acide méthanoïque avec les ions éthanoate (K = 11).
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch13 import *

PKA1, PKA2 = 4.2, 3.75
K = 10 ** (PKA2 - PKA1)
TAU = math.sqrt(K) / (1 + math.sqrt(K))
PH = (PKA1 + PKA2) / 2
assert abs(K - 0.355) < 0.001 and abs(TAU - 0.373) < 0.001 and abs(PH - (PKA1 + math.log10(TAU / (1 - TAU)))) < 1e-9

sPKA1, sPKA2 = 4.9, 4.2
sK = 10 ** (sPKA2 - sPKA1)
sTAU = math.sqrt(sK) / (1 + math.sqrt(sK))
sPH = (sPKA1 + sPKA2) / 2
assert abs(sK - 0.200) < 0.001 and abs(sTAU - 0.309) < 0.001 and abs(sPH - 4.55) < 1e-9

def fig(nom1, p1, nom2, p2):
    return tableau_texte("Les deux couples (à 25 °C)", ["Couple", "pKa"], [[nom1, p1], [nom2, p2]], cadre=(9, 0.6))

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction entre l'acide benzoïque et les ions méthanoate.",
    "السؤال un: كتب l'équation ديال la réaction بين l'acide benzoïque و les ions méthanoate.",
    phrase("C₆H₅COOH(aq) + HCOO⁻(aq) ⇌ C₆H₅COO⁻(aq) + HCOOH(aq)"),
    (["C₆H₅COOH", "HCOO⁻", "C₆H₅COO⁻", "HCOOH", "⇌"], ["H₃O⁺", "Na⁺"]),
    [("L'acide d'un couple cède un proton à la base de l'autre couple : quels sont les deux réactifs, et que deviennent-ils ?",
      "l'acide ديال couple كيعطي un proton ل la base ديال le couple الآخر. شكون هوما les deux réactifs، و شنو كيوليو؟"),
     ("C₆H₅COOH devient sa base C₆H₅COO⁻ ; HCOO⁻ devient son acide HCOOH. Les ions Na⁺ sont spectateurs.",
      "l'acide benzoïque كيولي l'ion benzoate، و l'ion méthanoate كيولي l'acide méthanoïque. les ions sodium spectateurs.")],
    [("1 : C₆H₅COOH(aq) + HCOO⁻(aq) ⇌ C₆H₅COO⁻(aq) + HCOOH(aq)", "l'acide benzoïque، plus les ions méthanoate")],
    "السؤال un. l'acide benzoïque، plus les ions méthanoate، double flèche، les ions benzoate، plus l'acide méthanoïque.",
    "ex_1", "fa_1"),
  Q("2", "Montrer que la constante d'équilibre s'écrit K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁), puis calculer K.",
    "السؤال deux: بين بلي K égale K a un sur K a deux، égale dix puissance p K a deux moins p K a un، ومن بعد حسب K.",
    val("K", K, None, "K = 10^(pKa₂ − pKa₁) = 10^(3,75 − 4,2) = 10^(−0,45) = 0,35"),
    (["K = Ka₁/Ka₂", "[H₃O⁺]", "10^(pKa₂ − pKa₁)"], ["K = Ka₂/Ka₁", "10^(pKa₁ − pKa₂)"]),
    [("Écris K avec les concentrations à l'équilibre, puis multiplie le haut et le bas par [H₃O⁺]éq.",
      "كتب K ب les concentrations à l'équilibre، و ضرب الفوق و التحت ف la concentration des ions H trois O plus."),
     ("Tu fais apparaître Ka₁ (couple de l'acide qui réagit, C₆H₅COOH) et 1/Ka₂ (couple HCOOH/HCOO⁻). Puis Ka = 10^(−pKa).",
      "كيبان K a un، ديال l'acide اللي كيتفاعل، و un sur K a deux. و من بعد K a égale dix puissance moins p K a.")],
    [("2 : K = [C₆H₅COO⁻]·[HCOOH]/([C₆H₅COOH]·[HCOO⁻]) ; × [H₃O⁺]/[H₃O⁺]", "نضربو الفوق و التحت"),
     ("K = Ka₁/Ka₂ = 10^(−pKa₁)/10^(−pKa₂) = 10^(pKa₂ − pKa₁)", "K égale K a un sur K a deux"),
     ("K = 10^(3,75 − 4,2) = 0,35", "K égale zéro virgule trente-cinq")],
    "السؤال deux. K égale les ions benzoate fois l'acide méthanoïque، sur l'acide benzoïque fois les ions méthanoate. نضربو الفوق و التحت ف la concentration des ions H trois O plus. الجزء اللول هو K a un، و الجزء الثاني هو un sur K a deux. إذن K égale K a un sur K a deux، يعني dix puissance p K a deux moins p K a un. l'application numérique: dix puissance trois virgule soixante-quinze moins quatre virgule deux. K égale zéro virgule trente-cinq.",
    "ex_2", "fa_2"),
  Q("3", "Calculer le quotient de réaction Qr,i à l'état initial et en déduire le sens d'évolution spontanée du système.",
    "السؤال trois: حسب Q r i فl'état initial، و استنتج le sens d'évolution spontanée.",
    phrase("Qr,i = [C₆H₅COO⁻]ᵢ·[HCOOH]ᵢ/([C₆H₅COOH]ᵢ·[HCOO⁻]ᵢ) = 0 car aucun produit au départ ; Qr,i < K : évolution dans le sens direct."),
    (["Qr,i", "Qr,i < K", "sens direct"], ["Qr,i = K", "sens inverse"]),
    [("Au départ, le mélange ne contient que l'acide benzoïque et les ions méthanoate : que vaut le numérateur de Qr,i ?",
      "فالبداية، le mélange فيه غير l'acide benzoïque و les ions méthanoate. شحال كيساوي الفوق ديال Q r i؟"),
     ("Compare Qr,i à K : si Qr,i < K, le système évolue dans le sens direct.",
      "قارن Q r i مع K. يلا كان Q r i صغر من K، le système كيتطور ف le sens direct.")],
    [("3 : pas de produits au départ : Qr,i = 0", "Q r i égale zéro"),
     ("Qr,i = 0 < K = 0,35 : le système évolue dans le sens direct", "le sens direct")],
    "السؤال trois. فالبداية ماكاينش les produits، إذن الفوق zéro، و Q r i égale zéro. zéro صغر من K égale zéro virgule trente-cinq، إذن le système كيتطور ف le sens direct.",
    "ex_3", "fa_3"),
  Q("4", "Le mélange initial est équimolaire : n₀ = 1,0 × 10⁻³ mol de chaque réactif. Montrer, à l'aide du tableau d'avancement, que K = τ²/(1 − τ)², puis calculer le taux d'avancement final τ.",
    "السؤال quatre: le mélange équimolaire، n zéro égale un virgule zéro fois dix puissance moins trois mole من كل réactif. بين ب le tableau بلي K égale tau au carré sur un moins tau au carré، ومن بعد حسب tau.",
    val("τ", TAU, None, "√K = τ/(1 − τ) donc τ = √K/(1 + √K) = 0,596/1,596 = 0,37"),
    (["x_max = n₀", "x_éq = τ·n₀", "√K", "τ/(1 − τ)"], ["τ = K", "τ = √K"]),
    [("Mélange équimolaire : x_max = n₀. À l'équilibre, les deux produits valent x_éq = τ·n₀ et les deux réactifs n₀ − x_éq. Le volume se simplifie.",
      "le mélange équimolaire، إذن x max égale n zéro. فالتوازن، les deux produits: tau fois n zéro، و les deux réactifs: n zéro moins x éq. و le volume كيتحيد."),
     ("K = (τ·n₀)²/((1 − τ)·n₀)² = τ²/(1 − τ)² ; prends la racine carrée : τ/(1 − τ) = √K, puis isole τ.",
      "K égale tau au carré، sur un moins tau au carré. خود la racine carrée: tau sur un moins tau égale racine de K، و عزل tau.")],
    [("4 : x_max = n₀ ; à l'équilibre : produits τ·n₀, réactifs (1 − τ)·n₀", "x max égale n zéro"),
     ("K = (τ·n₀)²/((1 − τ)·n₀)² = τ²/(1 − τ)²", "K égale tau au carré، sur un moins tau au carré"),
     ("τ/(1 − τ) = √K = 0,596 donc τ = √K/(1 + √K) = 0,37", "tau égale zéro virgule trente-sept")],
    "السؤال quatre. le mélange équimolaire، إذن x max égale n zéro. فالتوازن، كل produit: tau fois n zéro. و كل réactif: un moins tau، fois n zéro. le volume كيتحيد، إذن K égale tau au carré، sur un moins tau au carré. ناخدو la racine carrée: tau sur un moins tau، égale racine de K، يعني zéro virgule cinq cent quatre-vingt-seize. إذن tau égale racine de K، sur un plus racine de K. tau égale zéro virgule trente-sept. la réaction محدودة.",
    "ex_4", "fa_4"),
  Q("5", "Montrer qu'à l'équilibre le pH du mélange s'écrit pH = (pKa₁ + pKa₂)/2. Calculer sa valeur.",
    "السؤال cinq: بين بلي فالتوازن، p H égale p K a un plus p K a deux، sur deux. حسب القيمة ديالو.",
    val("pH", PH, None, "pH = (pKa₁ + pKa₂)/2 = (4,2 + 3,75)/2 = 3,98", tol=0.01),
    (["pH = pKa + log([A⁻]/[AH])", "[C₆H₅COO⁻] = [HCOOH]", "[C₆H₅COOH] = [HCOO⁻]"], ["pH = pKa₁ − pKa₂", "pH = 7"]),
    [("Écris pH = pKa + log([base]/[acide]) pour chacun des deux couples : le mélange n'a qu'un seul pH.",
      "كتب p H égale p K a plus log du rapport، ل les deux couples. le mélange عندو غير p H واحد."),
     ("D'après le tableau, [C₆H₅COO⁻] = [HCOOH] et [C₆H₅COOH] = [HCOO⁻] : additionne les deux relations, les log s'annulent.",
      "من le tableau، les ions benzoate قد l'acide méthanoïque، و l'acide benzoïque قد les ions méthanoate. جمع les deux relations: les log كيتحيدو.")],
    [("5 : pH = pKa₁ + log([C₆H₅COO⁻]/[C₆H₅COOH]) et pH = pKa₂ + log([HCOO⁻]/[HCOOH])", "ل les deux couples"),
     ("[C₆H₅COO⁻] = [HCOOH] et [C₆H₅COOH] = [HCOO⁻] : la somme des deux log est nulle", "les log كيتحيدو"),
     ("2·pH = pKa₁ + pKa₂ donc pH = (pKa₁ + pKa₂)/2 = (4,2 + 3,75)/2 = 3,98", "p H égale trois virgule quatre-vingt-dix-huit")],
    "السؤال cinq. نكتبو la relation ل les deux couples: p H égale p K a un، plus log ديال benzoate sur l'acide benzoïque. و p H égale p K a deux، plus log ديال méthanoate sur l'acide méthanoïque. من le tableau، les ions benzoate قد l'acide méthanoïque، و l'acide benzoïque قد les ions méthanoate. ملي نجمعو، les log كيتحيدو. إذن deux fois p H égale p K a un plus p K a deux. p H égale quatre virgule deux plus trois virgule soixante-quinze، sur deux. p H égale trois virgule quatre-vingt-dix-huit.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : deux couples se rencontrent", "L'acide d'un couple cède un proton à la base de l'autre.",
      "acides-bases-tableau/comparer.html?vue=reaction", "La réaction entre deux couples",
      "دابا deux couples كيتلاقاو. l'acide A H un كيعطي proton ل la base A deux moins. شوف l'équation: A H un plus A deux moins، double flèche، A un moins plus A H deux. فالتمرين ديالنا: l'acide benzoïque، plus les ions méthanoate، double flèche، les ions benzoate، plus l'acide méthanoïque.",
      [("C₆H₅COOH + HCOO⁻ ⇌ C₆H₅COO⁻ + HCOOH", "فالتمرين ديالنا")],
      [("دابا deux couples كيتلاقاو", "start"), ("شوف l'équation", "moment:equation")]),
  sim("ex_2", "Question 2 : K = Ka₁/Ka₂", "On multiplie par [H₃O⁺] : Ka₁ en haut, Ka₂ en bas.",
      "acides-bases-tableau/comparer.html?vue=reaction", "De K aux deux constantes d'acidité",
      "la constante K: الفوق les produits، و التحت les réactifs. باش يبانو les K a، نضربو الفوق و التحت ف la concentration des ions H trois O plus. دابا الكسر كيتقسم على deux: الجزء اللول هو K a un، و الجزء الثاني هو un sur K a deux. إذن K égale K a un sur K a deux، و K a un هو ديال l'acide اللي كيتفاعل. فالتمرين ديالنا: K égale dix puissance p K a deux moins p K a un، يعني dix puissance trois virgule soixante-quinze moins quatre virgule deux، égale zéro virgule trente-cinq.",
      [("K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁)", "إذن K égale K a un sur K a deux"), ("K = 10^(−0,45) = 0,35", "égale zéro virgule trente-cinq")],
      [("la constante K", "moment:quotient"), ("نضربو الفوق و التحت", "moment:multiplier"),
       ("دابا الكسر كيتقسم", "moment:separer"), ("إذن K égale K a un sur K a deux", "moment:relation")]),
  sim("ex_3", "Question 3 : Qr,i comparé à K", "Sans produits au départ, Qr,i = 0 < K : sens direct.",
      "acides-bases-tableau/comparer.html?vue=classement", "Les couples rangés sur l'axe des pKa",
      "شوف l'axe ديال p K a، و les couples عليه: l'acide méthanoïque ف trois virgule soixante-quinze، و l'acide éthanoïque ف quatre virgule huit. les acides على اليسار، و les bases على اليمين. كلما p K a صغير، كلما l'acide أقوى. فالتمرين ديالنا، l'acide benzoïque، p K a quatre virgule deux، أضعف من l'acide méthanoïque، و لهذا K صغر من un. ولكن فالبداية ماكاينين حتى produits: Q r i égale zéro. zéro صغر من K، إذن le système كيمشي ف le sens direct، حتى يوصل Q r ل K.",
      [("Qr,i = 0", "Q r i égale zéro"), ("Qr,i < K : sens direct", "إذن le système كيمشي ف le sens direct")],
      [("شوف l'axe ديال p K a", "moment:axe"), ("و les couples عليه", "moment:couples"), ("les acides على اليسار", "moment:acides"),
       ("و les bases على اليمين", "moment:bases"), ("كلما p K a صغير", "moment:fleches")]),
  sim("ex_4", "Question 4 : K écrit avec τ", "Chaque concentration à l'équilibre s'écrit avec τ ; le volume se simplifie.",
      "acides-bases-tableau/base.html?vue=constante", "K et le taux d'avancement final",
      "نتفكرو: فla simulation، l'acide فالما، le tableau كيعطي les produits ب tau، و l'acide اللي بقا ب un moins tau. إذن K كتكتب ب tau. فالتمرين ديالنا، les deux produits: tau fois n zéro، و les deux réactifs: un moins tau، fois n zéro. إذن K égale tau au carré، sur un moins tau au carré. la racine carrée: tau sur un moins tau، égale zéro virgule cinq cent quatre-vingt-seize. إذن tau égale zéro virgule trente-sept.",
      [("K = τ²/(1 − τ)²", "إذن K égale tau au carré"), ("τ = √K/(1 + √K) = 0,37", "إذن tau égale zéro virgule trente-sept")],
      [("نتفكرو", "moment:tableau"), ("إذن K كتكتب ب tau", "moment:relation"), ("فالتمرين ديالنا، les deux produits", "moment:constante")]),
  sim("ex_5", "Question 5 : un seul pH pour deux couples", "pH = pKa + log([base]/[acide]) pour chaque couple, puis on additionne.",
      "acides-bases-tableau/predominance.html?vue=relation", "La relation pH = pKa + log",
      "عندنا l'expression ديال K a. ناخدو moins log من الجهتين، و كنلقاو la relation: p H égale p K a، plus log de A moins sur A H. هاد la relation صحيحة ل كل couple فالمحلول. فالتمرين ديالنا، كنكتبوها ل les deux couples. les rapports مقلوبين، إذن ملي نجمعو، les log كيتحيدو. deux fois p H égale p K a un plus p K a deux، و p H égale trois virgule quatre-vingt-dix-huit.",
      [("2·pH = pKa₁ + pKa₂", "deux fois p H égale"), ("pH = (4,2 + 3,75)/2 = 3,98", "و p H égale trois virgule quatre-vingt-dix-huit")],
      [("عندنا l'expression ديال K a", "moment:ka"), ("ناخدو moins log", "moment:log"), ("و كنلقاو la relation", "moment:relation")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : l'équation", "نتمرنو بسؤال ساهل. اختار l'équation.",
      "Entre l'acide benzoïque et les ions méthanoate, il se forme…",
      ["C₆H₅COO⁻ et HCOOH", "C₆H₅COO⁻ et H₃O⁺", "HCOOH et HO⁻"], 0, {
        0: ("juste", "برافو! l'acide benzoïque كيعطي un proton ل l'ion méthanoate: كيتكونو l'ion benzoate و l'acide méthanoïque.", "Juste : C₆H₅COOH + HCOO⁻ ⇌ C₆H₅COO⁻ + HCOOH."),
        1: (("H trois O plus كيتكون ملي l'acide كيعطي le proton لالما. هنا كيعطيه ل l'ion méthanoate. عاود اختار.", "Le proton va à HCOO⁻, pas à l'eau. Réessaie."),
            ("الجواب هو l'ion benzoate و l'acide méthanoïque.", "Réponse : C₆H₅COO⁻ et HCOOH.")),
        2: (("l'ion méthanoate كياخد un proton، ما كيعطيش. و H O moins ما كيجيش من هنا. عاود اختار.", "HCOO⁻ capte un proton : il ne forme pas HO⁻ ici. Réessaie."),
            ("الجواب هو l'ion benzoate و l'acide méthanoïque.", "Réponse : C₆H₅COO⁻ et HCOOH."))},
      "Entre l'acide benzoïque et les ions méthanoate, il se forme ?"),
  qcm("fa_2", "Plus facile : K = 10^(pKa₂ − pKa₁)", "سؤال ساهل على K.",
      "pKa₁ = 4,2 (acide qui réagit) et pKa₂ = 3,75. K vaut…",
      ["10^(4,2 − 3,75) = 2,8", "10^(3,75 − 4,2) = 0,35", "4,2 − 3,75 = 0,45"], 1, {
        1: ("juste", "برافو! K égale dix puissance p K a deux moins p K a un، و p K a un ديال l'acide اللي كيتفاعل.", "Juste : K = 10^(pKa₂ − pKa₁) = 0,35."),
        0: (("قلبتي. K a un ديما فالفوق، إذن p K a un فل'exposant كيجي ب moins. عاود اختار.", "Ka₁ est au numérateur : 10^(−pKa₁) donne pKa₂ − pKa₁. Réessaie."),
            ("الجواب هو dix puissance p K a deux moins p K a un، يعني zéro virgule trente-cinq.", "Réponse : K = 10^(3,75 − 4,2) = 0,35.")),
        2: (("هادا غير الفرق، ماشي K. K هي dix puissance هاد الفرق. عاود اختار.", "K est une puissance de dix, pas une différence. Réessaie."),
            ("الجواب هو dix puissance moins zéro virgule quarante-cinq، يعني zéro virgule trente-cinq.", "Réponse : K = 10^(−0,45) = 0,35."))},
      "p K a un égale quatre virgule deux، p K a deux égale trois virgule soixante-quinze. K vaut ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "Au départ : seulement C₆H₅COOH et HCOO⁻ ; K = 0,35.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Qr,i = 0, car il n'y a aucun produit au départ.", True, "Le numérateur de Qr,i contient les produits : il est nul."),
      ("Comme K < 1, la réaction ne peut pas se produire.", False, "Qr,i = 0 < K : le système évolue dans le sens direct, même si K < 1 ; la réaction est simplement limitée."),
      ("Le système évolue dans le sens direct.", True, "Qr,i < K.")]),
  qcm("fa_4", "Plus facile : τ à partir de K", "سؤال ساهل: اختار la bonne valeur.",
      "K = τ²/(1 − τ)² et √K = 0,596. τ vaut…",
      ["0,596", "0,35", "0,37"], 2, {
        2: ("juste", "برافو! tau égale racine de K، sur un plus racine de K، يعني zéro virgule trente-sept.", "Juste : τ = √K/(1 + √K) = 0,37."),
        0: (("zéro virgule cinq cent quatre-vingt-seize هي tau sur un moins tau، ماشي tau. عاود اختار.", "0,596 = τ/(1 − τ), il reste à isoler τ. Réessaie."),
            ("الجواب هو zéro virgule trente-sept: tau égale racine de K، sur un plus racine de K.", "Réponse : τ = 0,596/1,596 = 0,37.")),
        1: (("هادي K، ماشي tau. K فيها tau au carré. عاود اختار.", "0,35 est K, pas τ. Réessaie."),
            ("الجواب هو zéro virgule trente-sept.", "Réponse : τ = √K/(1 + √K) = 0,37."))},
      "K égale tau au carré sur un moins tau au carré، و racine de K égale zéro virgule cinq cent quatre-vingt-seize. Tau vaut ?"),
  vf("fa_5", "Plus facile : vrai ou faux", "À l'équilibre : [C₆H₅COO⁻] = [HCOOH] et [C₆H₅COOH] = [HCOO⁻].",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Le mélange a un seul pH, qui vérifie la relation de chacun des deux couples.", True, "Les deux couples sont dans la même solution."),
      ("pH = (pKa₁ + pKa₂)/2 = 3,98.", True, "La somme des deux relations donne 2·pH = pKa₁ + pKa₂."),
      ("pH = pKa₁ − pKa₂ = 0,45.", False, "On additionne les deux relations : les log s'annulent et il reste 2·pH = pKa₁ + pKa₂.")]),
]

SIM_Q = [
  QS("1", "Écrire l'équation de la réaction entre l'acide propanoïque et les ions benzoate.",
     phrase("C₂H₅COOH(aq) + C₆H₅COO⁻(aq) ⇌ C₂H₅COO⁻(aq) + C₆H₅COOH(aq)"),
     (["⇌"], ["H₃O⁺"]),
     [("C₂H₅COOH + C₆H₅COO⁻ ⇌ C₂H₅COO⁻ + C₆H₅COOH", "double flèche")],
     "l'acide propanoïque، plus les ions benzoate، double flèche، les ions propanoate، plus l'acide benzoïque."),
  QS("2", "Montrer que K = 10^(pKa₂ − pKa₁) et calculer K.",
     val("K", sK, None, "K = 10^(4,2 − 4,9) = 10^(−0,7) = 0,20"),
     (["K = Ka₁/Ka₂"], ["K = Ka₂/Ka₁"]),
     [("K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁)", "K égale K a un sur K a deux"), ("K = 0,20", "zéro virgule vingt")],
     "K égale K a un sur K a deux، يعني dix puissance quatre virgule deux moins quatre virgule neuf. K égale zéro virgule vingt."),
  QS("3", "Calculer Qr,i et en déduire le sens d'évolution spontanée.",
     phrase("Qr,i = 0 (aucun produit au départ) < K : sens direct."),
     (["Qr,i < K"], ["sens inverse"]),
     [("Qr,i = 0 < K : sens direct", "le sens direct")],
     "ماكاينش les produits فالبداية، إذن Q r i égale zéro، صغر من K: le sens direct."),
  QS("4", "Mélange équimolaire (n₀ = 2,0 × 10⁻³ mol). Montrer que K = τ²/(1 − τ)² et calculer τ.",
     val("τ", sTAU, None, "τ = √K/(1 + √K) = 0,447/1,447 = 0,31"),
     (["√K", "τ/(1 − τ)"], ["τ = √K"]),
     [("K = τ²/(1 − τ)² ; τ = √K/(1 + √K)", "tau égale racine de K"), ("τ = 0,31", "zéro virgule trente et un")],
     "K égale tau au carré sur un moins tau au carré، إذن tau égale racine de K، sur un plus racine de K. tau égale zéro virgule trente et un."),
  QS("5", "Montrer que pH = (pKa₁ + pKa₂)/2 et calculer le pH.",
     val("pH", sPH, None, "pH = (4,9 + 4,2)/2 = 4,55", tol=0.01),
     (["pH = pKa + log([A⁻]/[AH])"], ["pH = pKa₁ − pKa₂"]),
     [("2·pH = pKa₁ + pKa₂ ; pH = 4,55", "quatre virgule cinquante-cinq")],
     "ملي نجمعو les deux relations، les log كيتحيدو: deux fois p H égale p K a un plus p K a deux. p H égale quatre virgule cinquante-cinq."),
]

EX = exercice(
  "phys_ex_ch13_acides_bases_5", "phys_ch13_acides_bases", "acides_bases",
  "L'acide benzoïque et les ions méthanoate : K, sens d'évolution et pH", "moyen", 30,
  ["Écrire la réaction entre deux couples", "Établir K = 10^(pKa₂ − pKa₁)", "Prévoir le sens d'évolution avec Qr,i", "Calculer τ à partir de K", "Établir le pH d'un mélange"],
  "À 25 °C, on mélange V₁ = 50 mL d'une solution d'acide benzoïque C₆H₅COOH de concentration 2,0 × 10⁻² mol/L et V₂ = 50 mL d'une solution de méthanoate de sodium (Na⁺(aq) + HCOO⁻(aq)) de même concentration : le mélange contient n₀ = 1,0 × 10⁻³ mol de chaque réactif, et aucun des produits. Le tableau donne les pKa des deux couples.",
  "دابا نقراو l'énoncé. à vingt-cinq degrés، كنخلطو cinquante millilitres ديال l'acide benzoïque، و cinquante millilitres ديال le méthanoate de sodium، نفس la concentration، deux virgule zéro fois dix puissance moins deux، mole par litre. فle mélange، n zéro égale un virgule zéro fois dix puissance moins trois mole من كل réactif، و ماكاين حتى produit. le tableau فيه p K a ديال les deux couples.",
  [fig("C₆H₅COOH / C₆H₅COO⁻ (couple 1)", "pKa₁ = 4,2", "HCOOH / HCOO⁻ (couple 2)", "pKa₂ = 3,75")],
  ["n₀(C₆H₅COOH) = n₀(HCOO⁻) = 1,0 × 10⁻³ mol", "pKa₁(C₆H₅COOH/C₆H₅COO⁻) = 4,2", "pKa₂(HCOOH/HCOO⁻) = 3,75", "Volume du mélange : V = 100 mL"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "On mélange 2,0 × 10⁻³ mol d'acide propanoïque C₂H₅COOH et 2,0 × 10⁻³ mol d'ions benzoate C₆H₅COO⁻ (sans produits au départ). pKa₁(C₂H₅COOH/C₂H₅COO⁻) = 4,9 ; pKa₂(C₆H₅COOH/C₆H₅COO⁻) = 4,2.",
  "نفس التمرين، بقيم أخرى. deux virgule zéro fois dix puissance moins trois mole ديال l'acide propanoïque، و نفس الكمية ديال les ions benzoate. p K a un égale quatre virgule neuf، و p K a deux égale quatre virgule deux.",
  [fig("C₂H₅COOH / C₂H₅COO⁻ (couple 1)", "pKa₁ = 4,9", "C₆H₅COOH / C₆H₅COO⁻ (couple 2)", "pKa₂ = 4,2")],
  ["n₀ = 2,0 × 10⁻³ mol de chaque réactif", "pKa₁ = 4,9 ; pKa₂ = 4,2"],
  SIM_Q)

ecrire(EX)
