# Exercice de chimie, ch. 12 (état d'équilibre), niveau moyen (celui du national) : deux acides de même
# concentration ; Qr,éq en fonction de C et du pH (« montrer que »), K de chacun, τ de chacun, puis déduire le lien
# entre K et τ (τ dépend de la nature de la réaction).
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2017 N (1.1 τ, 1.2 Qr,éq en fonction de C et du pH), 2021 N (2.2 τ, 2.3
#    Qr,éq, 2.4 identifier l'acide par sa constante), 2022 N (1.2-1.3 τ puis Qr,éq), 2023 N (1.2-1.3 de la proportion
#    à la constante) — backend/data/exams/physique ;
#  - profs (architecture/phys_ch12_etat_equilibre.md § 1 : Naceiri Mrabti et El Goufifa : « facteurs de τ : l'état
#    initial, puis K » ; Moutamadris, fiche 2BAC, Bazhar) ; pièges : comparer deux τ de concentrations différentes,
#    dire « plus K est grand, plus la réaction est rapide » (K ne dit rien de la vitesse) ;
#  - séries en ligne : talamidi (état d'équilibre, activités 1, question 6 : facteurs de τ), talamidi (acide-base,
#    exercices non corrigés 2 et 5), moutamadris (exercices état d'équilibre), alloschool (El Goufifa, séance 9),
#    Naceiri Mrabti (livre 2BAC), docs Google d'un prof BIOF.
# Ici : l'acide butanoïque et l'acide benzoïque à notre concentration ; pH calculés à partir de K₁ = 1,5 × 10⁻⁵ et
# K₂ = 6,3 × 10⁻⁵.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch12 import *


def acide(C, pH):
    h = h3o(pH)
    return h, C - h, h * h / (C - h), h / C


C, P1, P2 = 2.0e-2, 3.27, 2.96
H1, A1, K1, T1 = acide(C, P1)
H2, A2, K2, T2 = acide(C, P2)
assert sci(K1, 1) == "1,5 × 10⁻⁵" and sci(K2, 1) == "6,4 × 10⁻⁵" and fr(T1, 3) == "0,027" and fr(T2, 3) == "0,055"
assert sci(H1, 2) == "5,37 × 10⁻⁴" and sci(H2, 2) == "1,10 × 10⁻³"
sC, sP1, sP2 = 5.0e-3, 3.57, 3.28
sH1, sA1, sK1, sT1 = acide(sC, sP1)
sH2, sA2, sK2, sT2 = acide(sC, sP2)
assert sci(sK1, 1) == "1,5 × 10⁻⁵" and sci(sK2, 1) == "6,2 × 10⁻⁵" and fr(sT1, 3) == "0,054" and fr(sT2, 3) == "0,105"

FIG = tableau_texte("Les deux solutions (même concentration C)",
    ["Solution", "Acide", "C (mol/L)", "pH à 25 °C"],
    [["S₁", "acide butanoïque C₃H₇COOH", "2,0 × 10⁻²", "3,27"], ["S₂", "acide benzoïque C₆H₅COOH", "2,0 × 10⁻²", "2,96"]], cadre=(12, 0.7))
sFIG = tableau_texte("Les deux solutions (même concentration C)",
    ["Solution", "Acide", "C (mol/L)", "pH à 25 °C"],
    [["S₁", "acide butanoïque C₃H₇COOH", "5,0 × 10⁻³", "3,57"], ["S₂", "acide benzoïque C₆H₅COOH", "5,0 × 10⁻³", "3,28"]], cadre=(12, 0.7))

REL = "Qr,éq = 10^(−2pH)/(C − 10^(−pH))"
REL_DIT = "Q r à l'équilibre égale dix puissance moins deux p H، sur C moins dix puissance moins p H"

QUESTIONS = [
  Q("1", "Pour un acide AH de concentration C dont la solution a un pH donné, montrer que : Qr,éq = 10^(−2pH)/(C − 10^(−pH)).",
    "السؤال un: ل acide A H، la concentration ديالو C، و le p H ديالو معروف، بين بلي " + REL_DIT + ".",
    phrase("[A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [AH]éq = C − 10^(−pH) ; Qr,éq = [A⁻]éq·[H₃O⁺]éq/[AH]éq = 10^(−2pH)/(C − 10^(−pH))"),
    (["[A⁻]éq = [H₃O⁺]éq", "10^(−pH)", "C − 10^(−pH)", "10^(−2pH)"], ["[AH]éq = C", "10^(−pH²)"]),
    [("Pars de l'équation AH + H₂O ⇌ A⁻ + H₃O⁺ et de l'expression de Qr,éq. Que vaut chaque concentration ?",
      "بدا من l'équation، A H plus الما، كيعطيو A moins plus H trois O plus، ومن l'expression ديال Q r à l'équilibre. شحال كل concentration؟"),
     ("Le tableau donne [A⁻]éq = [H₃O⁺]éq = 10^(−pH) et [AH]éq = C − 10^(−pH) ; 10^(−pH) × 10^(−pH) = 10^(−2pH).",
      "le tableau كيعطي: A moins و H trois O plus، dix puissance moins p H. و A H، C moins dix puissance moins p H. و dix puissance moins p H fois dix puissance moins p H، كتعطي dix puissance moins deux p H.")],
    [("1 : Qr,éq = [A⁻]éq·[H₃O⁺]éq/[AH]éq", "نبداو من la définition"),
     ("[A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [AH]éq = C − 10^(−pH)", "C moins dix puissance moins p H"),
     (REL, "إذن " + REL_DIT)],
    "السؤال un. نبداو من la définition: Q r à l'équilibre égale A moins fois H trois O plus، sur A H. من le tableau: A moins و H trois O plus عندهم نفس التركيز، dix puissance moins p H. و A H: C moins dix puissance moins p H. إذن " + REL_DIT + ".",
    "ex_1", "fa_1"),
  Q("2", "Calculer la constante d'équilibre K₁ de la réaction de l'acide butanoïque avec l'eau.",
    "السؤال deux: حسب K un، la constante d'équilibre ديال l'acide butanoïque مع الما.",
    val("K₁", K1, None, f"K₁ = Qr,éq = 10^(−6,54)/(2,0 × 10⁻² − 10^(−3,27)) = {sci(H1 * H1, 2)}/{sci(A1, 3)} ≈ {sci(K1, 1)}", tol=0.05),
    (["K = Qr,éq", "10^(−2pH)", "C − 10^(−pH)"], ["K = 10^(−pH)/C", "K = 10^(−2pH)/C²"]),
    [("K₁ est la valeur de Qr,éq : utilise la relation de la question 1 avec pH = 3,27.", "K un هي Q r à l'équilibre: استعمل la relation ديال السؤال un، ب p H égale trois virgule vingt-sept."),
     ("Au numérateur 10^(−6,54) ; au dénominateur 2,0 × 10⁻² − 10^(−3,27).", "الفوق dix puissance moins six virgule cinquante-quatre، والتحت deux virgule zéro fois dix puissance moins deux، moins dix puissance moins trois virgule vingt-sept.")],
    [("2 : K₁ = Qr,éq = 10^(−2pH₁)/(C − 10^(−pH₁))", "K un égale Q r à l'équilibre"),
     (f"K₁ = 10^(−6,54)/(2,0 × 10⁻² − 10^(−3,27))", "l'application numérique"),
     (f"K₁ ≈ {sci(K1, 1)}", f"K un égale {dsci(K1, 1)}")],
    f"السؤال deux. K un égale Q r à l'équilibre. l'application numérique: dix puissance moins six virgule cinquante-quatre، sur deux virgule zéro fois dix puissance moins deux، moins dix puissance moins trois virgule vingt-sept. K un égale {dsci(K1, 1)}.",
    "ex_2", "fa_2"),
  Q("3", "Calculer de même la constante d'équilibre K₂ de la réaction de l'acide benzoïque avec l'eau.",
    "السؤال trois: حسب بنفس الطريقة K deux، ديال l'acide benzoïque مع الما.",
    val("K₂", K2, None, f"K₂ = 10^(−5,92)/(2,0 × 10⁻² − 10^(−2,96)) = {sci(H2 * H2, 2)}/{sci(A2, 3)} ≈ {sci(K2, 1)}", tol=0.05),
    (["K = Qr,éq", "10^(−2pH)", "C − 10^(−pH)"], ["K = 10^(−pH)/C"]),
    [("Même relation, avec pH = 2,96.", "نفس la relation، ب p H égale deux virgule quatre-vingt-seize."),
     ("Deux fois 2,96 font 5,92 : K₂ = 10^(−5,92)/(2,0 × 10⁻² − 10^(−2,96)).", "deux fois deux virgule quatre-vingt-seize كتعطي cinq virgule quatre-vingt-douze. K deux égale dix puissance moins cinq virgule quatre-vingt-douze، sur C moins dix puissance moins deux virgule quatre-vingt-seize.")],
    [("3 : K₂ = 10^(−5,92)/(2,0 × 10⁻² − 10^(−2,96))", "K deux égale dix puissance moins cinq virgule quatre-vingt-douze"),
     (f"K₂ ≈ {sci(K2, 1)}", f"K deux égale {dsci(K2, 1)}")],
    f"السؤال trois. K deux égale dix puissance moins cinq virgule quatre-vingt-douze، sur deux virgule zéro fois dix puissance moins deux، moins dix puissance moins deux virgule quatre-vingt-seize. K deux égale {dsci(K2, 1)}.",
    "ex_3", "fa_3"),
  Q("4", "Calculer le taux d'avancement final τ₁ de la réaction dans S₁, puis τ₂ dans S₂.",
    "السؤال quatre: حسب tau un فS un، و tau deux فS deux.",
    val("τ₂", T2, None, f"τ₁ = 10^(−3,27)/(2,0 × 10⁻²) ≈ {fr(T1, 3)} ; τ₂ = 10^(−2,96)/(2,0 × 10⁻²) ≈ {fr(T2, 3)}", tol=0.05),
    (["τ = 10^(−pH)/C", "τ₁", "τ₂"], ["τ = C/10^(−pH)", "τ = 10^(−2pH)/C"]),
    [("τ = x_éq/x_max : pour un acide dans l'eau, quelle relation avec le pH et C ?", "tau égale x éq sur x max: ل acide فالما، شنو la relation مع le p H و C؟"),
     ("τ = 10^(−pH)/C, pour chaque solution.", "tau égale dix puissance moins p H، sur C، لكل solution.")],
    [("4 : τ = 10^(−pH)/C", "tau égale dix puissance moins p H، sur C"),
     (f"τ₁ = 10^(−3,27)/(2,0 × 10⁻²) ≈ {fr(T1, 3)}", f"tau un égale {dfr(T1, 3)}"),
     (f"τ₂ = 10^(−2,96)/(2,0 × 10⁻²) ≈ {fr(T2, 3)}", f"tau deux égale {dfr(T2, 3)}")],
    f"السؤال quatre. tau égale dix puissance moins p H، sur C. ل S un: tau un égale {dfr(T1, 3)}. ل S deux: tau deux égale {dfr(T2, 3)}. بجوج صغار من un: deux réactions محدودين.",
    "ex_4", "fa_4"),
  Q("5", "Les deux solutions ont la même concentration. Comparer K₁ et K₂, puis τ₁ et τ₂. Que peut-on déduire ?",
    "السؤال cinq: deux solutions عندهم نفس la concentration. قارن K un و K deux، ومن بعد tau un و tau deux. شنو نستنتجو؟",
    phrase("K₂ > K₁ et τ₂ > τ₁ : pour une même concentration initiale, plus la constante d'équilibre K est grande, plus le taux d'avancement final τ est grand ; τ dépend de la nature de la réaction (de K)."),
    (["K₂ > K₁", "τ₂ > τ₁", "même C", "nature de la réaction"], ["la réaction 2 est plus rapide", "τ ne dépend que de C"]),
    [("Mets côte à côte les deux K et les deux τ : lequel est le plus grand dans chaque cas ?", "حط K un و K deux حدا بعض، و tau un و tau deux. شكون الكبير فكل مرة؟"),
     ("Même C : la seule différence est la réaction (l'acide), c'est-à-dire K. Attention, K ne dit rien de la vitesse.",
      "نفس C: الفرق الوحيد هو la réaction، يعني K. ورد البال: K ما كتقول والو على la vitesse.")],
    [(f"5 : K₂ ≈ {sci(K2, 1)} > K₁ ≈ {sci(K1, 1)}", "K deux كبر من K un"),
     (f"τ₂ ≈ {fr(T2, 3)} > τ₁ ≈ {fr(T1, 3)}", "و tau deux كبر من tau un"),
     ("même C : plus K est grande, plus τ est grand ; τ dépend de la nature de la réaction", "plus K est grande، plus tau est grand")],
    "السؤال cinq. K deux كبر من K un، و tau deux كبر من tau un. و deux solutions عندهم نفس C. إذن: même C، plus K est grande، plus tau est grand. tau كيتعلق ب la nature de la réaction.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  slide("ex_1", "expression", "Question 1 : Qr,éq en fonction de C et du pH",
        "Les deux produits valent 10^(−pH), l'acide C − 10^(−pH).",
        "فالتمرين ديالنا، نفس الخطوات ل A H: إذن " + REL_DIT + ".",
        [(REL, "فالتمرين ديالنا، نفس الخطوات")]),
  slide("ex_2", "qr_eq", "Question 2 : K₁ de l'acide butanoïque",
        "K = Qr,éq : on remplace par les valeurs de S₁.",
        f"فالتمرين ديالنا، S un: p H égale trois virgule vingt-sept. K un égale dix puissance moins six virgule cinquante-quatre، sur deux virgule zéro fois dix puissance moins deux، moins dix puissance moins trois virgule vingt-sept. يعني {dsci(K1, 1)}.",
        [(f"K₁ ≈ {sci(K1, 1)}", f"يعني {dsci(K1, 1)}")]),
  slide("ex_3", "qr_eq", "Question 3 : K₂ de l'acide benzoïque",
        "Même calcul avec le pH de S₂.",
        f"فالتمرين ديالنا، S deux: p H égale deux virgule quatre-vingt-seize. K deux égale dix puissance moins cinq virgule quatre-vingt-douze، sur deux virgule zéro fois dix puissance moins deux، moins dix puissance moins deux virgule quatre-vingt-seize. يعني {dsci(K2, 1)}.",
        [(f"K₂ ≈ {sci(K2, 1)}", f"يعني {dsci(K2, 1)}")]),
  slide("ex_4", "taux", "Question 4 : τ₁ et τ₂",
        "τ = 10^(−pH)/C pour chaque solution.",
        f"فالتمرين ديالنا: tau un égale dix puissance moins trois virgule vingt-sept، sur deux virgule zéro fois dix puissance moins deux، يعني {dfr(T1, 3)}. و tau deux égale {dfr(T2, 3)}.",
        [(f"τ₁ ≈ {fr(T1, 3)}", f"يعني {dfr(T1, 3)}"), (f"τ₂ ≈ {fr(T2, 3)}", f"و tau deux égale {dfr(T2, 3)}")]),
  slide("ex_5", "nature", "Question 5 : même C, K plus grande, τ plus grand",
        "À concentration égale, τ dépend de la réaction, donc de K.",
        f"فالتمرين ديالنا، نفس الشي: l'acide benzoïque، K deux égale {dsci(K2, 1)}، و tau deux égale {dfr(T2, 3)}. l'acide butanoïque، K un égale {dsci(K1, 1)}، و tau un égale {dfr(T1, 3)}. الكبير ف K هو الكبير ف tau.",
        [("K₂ > K₁ ⇒ τ₂ > τ₁ (même C)", "الكبير ف K هو الكبير ف tau")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : l'acide restant", "سؤال ساهل: شحال بقا من l'acide à l'équilibre؟",
      "Une solution d'acide AH de concentration C a un pH donné. À l'équilibre, [AH]éq = …",
      ["10^(−pH)", "C − 10^(−pH)", "C"], 1, {
        1: ("juste", "برافو! l'acide خسر قد اللي تكون من H trois O plus.", "Juste : [AH]éq = C − 10^(−pH)."),
        0: (("لا، dix puissance moins p H هي la concentration des ions H trois O plus، يعني اللي تكون. و l'acide اللي بقا؟ عاود اختار.", "10^(−pH), c'est ce qui s'est formé. Réessaie."),
            ("الجواب: C moins dix puissance moins p H.", "Réponse : [AH]éq = C − 10^(−pH).")),
        2: (("قريب! ولكن شوية من l'acide تفاعل مع الما. خاصنا نحيدوه. عاود اختار.", "Une partie de l'acide a réagi : il faut l'enlever. Réessaie."),
            ("الجواب: C moins dix puissance moins p H.", "Réponse : [AH]éq = C − 10^(−pH)."))},
      "À l'équilibre، la concentration de l'acide A H égale quoi ?"),
  qcm("fa_2", "Plus facile : le numérateur", "سؤال ساهل على الفوق ديال Q r.",
      "pH = 3,27. Le numérateur [A⁻]éq·[H₃O⁺]éq vaut…",
      ["10^(−3,27)", "10^(−6,54)", "10^(−10,69)"], 1, {
        1: ("juste", "برافو! dix puissance moins p H، fois dix puissance moins p H: dix puissance moins deux p H.", "Juste : 10^(−3,27) × 10^(−3,27) = 10^(−6,54)."),
        0: (("قريب! هادي غير concentration وحدة. الفوق كاينين deux. عاود اختار.", "Ce n'est qu'une des deux concentrations. Réessaie."),
            ("الجواب: dix puissance moins six virgule cinquante-quatre.", "Réponse : 10^(−6,54).")),
        2: (("لا، ملي كنضربو des puissances de dix، كنجمعو les exposants، ماشي كنضربوهم. عاود اختار.", "On additionne les exposants : −3,27 + (−3,27). Réessaie."),
            ("الجواب: moins trois virgule vingt-sept، plus moins trois virgule vingt-sept، كتعطي moins six virgule cinquante-quatre.", "Réponse : 10^(−6,54)."))},
      "p H égale trois virgule vingt-sept. Le numérateur vaut ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "La constante d'équilibre K.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("K est la valeur de Qr dans l'état d'équilibre.", True, "K = Qr,éq."),
      ("K a l'unité mol/L.", False, "Qr, donc K, est sans unité."),
      ("K de l'acide benzoïque avec l'eau ne dépend que de la température.", True, "Elle ne dépend ni de C, ni du sens de départ.")]),
  qcm("fa_4", "Plus facile : calculer τ₁", "سؤال ساهل: اختار tau un.",
      "pH₁ = 3,27 et C = 2,0 × 10⁻² mol/L. τ₁ vaut environ…",
      ["37", "1,1 × 10⁻⁵", "0,027"], 2, {
        2: ("juste", "برافو! tau égale dix puissance moins p H، sur C: zéro virgule zéro vingt-sept.", "Juste : τ₁ = 5,37 × 10⁻⁴/2,0 × 10⁻² ≈ 0,027."),
        0: (("لا، قلبتي الكسر: C sur la concentration. و tau ما يمكنش يفوت un. عاود اختار.", "Fraction renversée : τ ne dépasse jamais 1. Réessaie."),
            ("الجواب: zéro virgule zéro vingt-sept.", "Réponse : τ₁ = 10^(−pH)/C ≈ 0,027.")),
        1: (("لا، ضربتي ف C بلاصة ما تقسم. عاود اختار.", "On divise par C, on ne multiplie pas. Réessaie."),
            ("الجواب: zéro virgule zéro vingt-sept.", "Réponse : τ₁ ≈ 0,027."))},
      "p H un égale trois virgule vingt-sept، et C égale deux virgule zéro fois dix puissance moins deux mole par litre. tau un vaut environ ?"),
  vf("fa_5", "Plus facile : K et τ", "Deux acides, même concentration.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("À même C, l'acide de plus grande K a le plus grand τ.", True, "K₂ > K₁ et τ₂ > τ₁."),
      ("K₂ > K₁ montre que la réaction de l'acide benzoïque est plus rapide.", False, "K dit jusqu'où va la réaction, pas à quelle vitesse."),
      ("τ dépend de la nature de la réaction et de l'état initial.", True, "τ dépend de K et de C.")]),
]

SIM_Q = [
  QS("1", "Montrer que Qr,éq = 10^(−2pH)/(C − 10^(−pH)).",
     phrase("[A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [AH]éq = C − 10^(−pH) ; " + REL),
     (["10^(−pH)", "C − 10^(−pH)"], ["[AH]éq = C"]),
     [("[A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [AH]éq = C − 10^(−pH)", "dix puissance moins p H"), (REL, REL_DIT)],
     "A moins و H trois O plus: dix puissance moins p H. A H: C moins dix puissance moins p H. إذن " + REL_DIT + "."),
  QS("2", "Calculer K₁ (acide butanoïque, pH = 3,57).",
     val("K₁", sK1, None, f"K₁ = 10^(−7,14)/(5,0 × 10⁻³ − 10^(−3,57)) ≈ {sci(sK1, 1)}", tol=0.05),
     (["10^(−2pH)"], ["10^(−pH)/C"]),
     [(f"K₁ = 10^(−7,14)/(5,0 × 10⁻³ − 10^(−3,57)) ≈ {sci(sK1, 1)}", f"{dsci(sK1, 1)}")],
     f"K un égale dix puissance moins sept virgule quatorze، sur cinq virgule zéro fois dix puissance moins trois، moins dix puissance moins trois virgule cinquante-sept. K un égale {dsci(sK1, 1)}."),
  QS("3", "Calculer K₂ (acide benzoïque, pH = 3,28).",
     val("K₂", sK2, None, f"K₂ = 10^(−6,56)/(5,0 × 10⁻³ − 10^(−3,28)) ≈ {sci(sK2, 1)}", tol=0.05),
     (["10^(−2pH)"], ["10^(−pH)/C"]),
     [(f"K₂ ≈ {sci(sK2, 1)}", f"{dsci(sK2, 1)}")],
     f"K deux égale dix puissance moins six virgule cinquante-six، sur cinq virgule zéro fois dix puissance moins trois، moins dix puissance moins trois virgule vingt-huit. K deux égale {dsci(sK2, 1)}."),
  QS("4", "Calculer τ₁ puis τ₂.",
     val("τ₂", sT2, None, f"τ₁ = 10^(−3,57)/(5,0 × 10⁻³) ≈ {fr(sT1, 3)} ; τ₂ = 10^(−3,28)/(5,0 × 10⁻³) ≈ {fr(sT2, 3)}", tol=0.05),
     (["τ = 10^(−pH)/C"], ["τ = C/10^(−pH)"]),
     [(f"τ₁ ≈ {fr(sT1, 3)} ; τ₂ ≈ {fr(sT2, 3)}", f"tau deux égale {dfr(sT2, 3)}")],
     f"tau un égale {dfr(sT1, 3)}، و tau deux égale {dfr(sT2, 3)}."),
  QS("5", "Comparer K₁, K₂ puis τ₁, τ₂ ; conclure.",
     phrase("K₂ > K₁ et τ₂ > τ₁ : à même C, plus K est grande, plus τ est grand."),
     (["K₂ > K₁", "τ₂ > τ₁"], ["plus rapide"]),
     [("K₂ > K₁ et τ₂ > τ₁ : même C, plus K est grande, plus τ est grand", "plus K est grande، plus tau est grand")],
     "K deux كبر، و tau deux كبر. إذن même C، plus K est grande، plus tau est grand."),
]

EX = exercice(
  "phys_ex_ch12_etat_equilibre_5", "phys_ch12_etat_equilibre", "etat_equilibre",
  "Deux acides à la même concentration : K et τ", "moyen", 25,
  ["Établir Qr,éq = 10^(−2pH)/(C − 10^(−pH))", "Calculer K à partir du pH", "Calculer τ", "Relier K et τ à concentration égale"],
  "On prépare deux solutions aqueuses de même concentration C = 2,0 × 10⁻² mol/L : S₁ d'acide butanoïque C₃H₇COOH et S₂ d'acide benzoïque C₆H₅COOH. On mesure leur pH à 25 °C (tableau). Chaque acide, noté AH, réagit avec l'eau selon : AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq).",
  "دابا نقراو l'énoncé. عندنا deux solutions، بنفس la concentration، C égale deux virgule zéro fois dix puissance moins deux mole par litre. S un فيها l'acide butanoïque، و S deux فيها l'acide benzoïque. قسنا le p H ديال كل وحدة: trois virgule vingt-sept، و deux virgule quatre-vingt-seize. كل acide، A H، كيتفاعل مع الما، ب la double flèche.",
  [FIG], ["C = 2,0 × 10⁻² mol/L pour S₁ et S₂", "S₁ (acide butanoïque) : pH₁ = 3,27", "S₂ (acide benzoïque) : pH₂ = 2,96"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Deux solutions de même concentration C = 5,0 × 10⁻³ mol/L : S₁ (acide butanoïque) de pH 3,57 et S₂ (acide benzoïque) de pH 3,28, à 25 °C.",
  "نفس التمرين، بقيم أخرى: C égale cinq virgule zéro fois dix puissance moins trois mole par litre، و les p H: trois virgule cinquante-sept، و trois virgule vingt-huit.",
  [sFIG], ["C = 5,0 × 10⁻³ mol/L", "pH₁ = 3,57 ; pH₂ = 3,28"],
  SIM_Q)

ecrire(EX)
