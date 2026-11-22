# Exercice de chimie, ch. 12 (état d'équilibre), niveau moyen (celui du national) : un acide dans l'eau, du pH au
# taux d'avancement final τ, « montrer que Qr,éq = C·τ²/(1 − τ) », K, puis l'effet d'une dilution sur τ.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2017 N (1.1 τ puis déduire, 1.2 Qr,éq), 2020 R (1.3 τ, 1.4 Qr,éq en fonction
#    de C et τ), 2021 N (2.2 montrer τ ≈ 1,32 %, 2.3 Qr,éq en fonction de Cₐ et τ), 2021 R (9 montrer
#    τ = 10^(−pH)/C, 10-11 effet de la dilution), 2022 N (1.2 τ et conclure) — backend/data/exams/physique ;
#  - profs (architecture/phys_ch12_etat_equilibre.md § 1 : Naceiri Mrabti (activité des trois concentrations),
#    El Goufifa, Moutamadris, fiche 2BAC, Bazhar) : τ = x_éq/x_max = 10^(−pH)/C, K = C·τ²/(1 − τ) établie depuis le
#    tableau ; pièges : oublier de conclure « limitée », croire que K change avec la dilution ;
#  - séries en ligne : talamidi (état d'équilibre, activités 1 : « τ dépend de l'état initial et de K »), talamidi
#    (acide-base, exercices non corrigés 2 : τ en fonction du pH), moutamadris (exercices état d'équilibre), alloschool
#    (El Goufifa, séance 9), Naceiri Mrabti (livre 2BAC), coursdusoirpc (TD BIOF).
# Ici : l'acide ascorbique (vitamine C, noté AH) à nos concentrations ; pH calculés à partir de K ≈ 7,9 × 10⁻⁵.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch12 import *

C, PH, PH2 = 5.0e-3, 3.23, 3.79
H = h3o(PH); TAU = H / C; K = C * TAU ** 2 / (1 - TAU)
C2 = C / 10; H2 = h3o(PH2); TAU2 = H2 / C2; K2 = C2 * TAU2 ** 2 / (1 - TAU2)
assert fr(TAU, 2) == "0,12" and sci(K, 1) == "7,9 × 10⁻⁵" and fr(TAU2, 2) == "0,32" and abs(K2 / K - 1) < 0.03
assert sci(H, 1) == "5,9 × 10⁻⁴" and sci(H2, 1) == "1,6 × 10⁻⁴"
sC, sPH, sPH2 = 1.0e-2, 3.07, 3.61
sH = h3o(sPH); sTAU = sH / sC; sK = sC * sTAU ** 2 / (1 - sTAU)
sC2 = sC / 10; sH2 = h3o(sPH2); sTAU2 = sH2 / sC2; sK2 = sC2 * sTAU2 ** 2 / (1 - sTAU2)
assert fr(sTAU, 3) == "0,085" and sci(sK, 1) == "7,9 × 10⁻⁵" and fr(sTAU2, 2) == "0,25" and abs(sK2 / sK - 1) < 0.03

EQ = "AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq)"
EQ_DIT = "A H، plus الما، ب la double flèche، كيعطيو A moins، plus les ions H trois O plus"
KREL = "Qr,éq = C·τ²/(1 − τ)"

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction de l'acide ascorbique AH avec l'eau.",
    "السؤال un: كتب l'équation ديال la réaction ديال l'acide ascorbique، A H، مع الما.",
    phrase(EQ),
    (["⇌", "H₂O", "A⁻", "H₃O⁺"], ["→", "HO⁻"]),
    [("L'acide AH cède un proton : qui le capte dans la solution ?", "l'acide A H كيعطي un proton. شكون كياخدو فالمحلول؟"),
     ("L'eau capte le proton (H₃O⁺) et AH devient sa base A⁻ ; on écrit la double flèche.",
      "الما كياخد le proton وكيولي H trois O plus، و A H كيولي A moins. وكنكتبو la double flèche.")],
    [("1 : " + EQ, "كيعطيو A moins")],
    "السؤال un. " + EQ_DIT + ".",
    "ex_1", "fa_1"),
  Q("2", "En s'aidant du tableau d'avancement, montrer que le taux d'avancement final s'écrit τ = 10^(−pH)/C. Calculer τ. Que peut-on conclure ?",
    "السؤال deux: بle tableau d'avancement، بين بلي tau égale dix puissance moins p H، sur C. حسب tau، وشنو نستنتجو؟",
    val("τ", TAU, None, f"τ = x_éq/x_max = [H₃O⁺]éq·V/(C·V) = 10^(−pH)/C = 10^(−3,23)/(5,0 × 10⁻³) ≈ {fr(TAU, 2)} < 1 : réaction limitée", tol=0.05),
    (["x_max = C·V", "x_éq = [H₃O⁺]éq·V", "τ = x_éq/x_max", "10^(−pH)", "< 1"], ["τ = C/10^(−pH)", "x_max = [H₃O⁺]·V"]),
    [("x_max : l'eau est en excès, l'acide est le réactif limitant. x_éq : regarde la colonne des ions H₃O⁺.",
      "x max: الما en excès، إذن l'acide هو le réactif limitant. و x éq: شوف la colonne ديال les ions H trois O plus."),
     ("x_max = C·V et x_éq = [H₃O⁺]éq·V = 10^(−pH)·V ; V se simplifie dans τ = x_éq/x_max.",
      "x max égale C fois V، و x éq égale dix puissance moins p H، fois V. و V كيتحيد ف tau égale x éq sur x max.")],
    [("2 : x_max = C·V (l'eau en excès) ; x_éq = [H₃O⁺]éq·V", "x max égale C fois V"),
     ("τ = x_éq/x_max = 10^(−pH)/C", "tau égale dix puissance moins p H، sur C"),
     (f"τ = 10^(−3,23)/(5,0 × 10⁻³) ≈ {fr(TAU, 2)}", f"tau égale {dfr(TAU, 2)}"),
     ("τ < 1 : la réaction de l'acide avec l'eau est limitée", "la réaction محدودة")],
    f"السؤال deux. الما en excès، إذن x max égale C fois V. ومن le tableau، x éq égale la concentration des ions H trois O plus، fois V. إذن tau égale x éq sur x max، و V كيتحيد: tau égale dix puissance moins p H، sur C. l'application numérique: dix puissance moins trois virgule vingt-trois، sur cinq virgule zéro fois dix puissance moins trois. tau égale {dfr(TAU, 2)}. tau صغير من un، إذن la réaction محدودة.",
    "ex_2", "fa_2"),
  Q("3", "Montrer que le quotient de réaction à l'équilibre s'écrit : Qr,éq = C·τ²/(1 − τ).",
    "السؤال trois: بين بلي Q r à l'équilibre égale C fois tau au carré، sur un moins tau.",
    phrase("[A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C − C·τ = C(1 − τ) ; Qr,éq = (C·τ)²/(C(1 − τ)) = C·τ²/(1 − τ)"),
    (["[A⁻]éq = C·τ", "[AH]éq = C(1 − τ)", "Qr,éq", "( )²"], ["[AH]éq = C·τ", "[AH]éq = C"]),
    [("Exprime d'abord chaque concentration à l'équilibre avec C et τ : x_éq/V = τ·x_max/V = τ·C.",
      "عبر أولا على كل concentration à l'équilibre ب C و tau: x éq sur V égale tau fois C."),
     ("[A⁻]éq = [H₃O⁺]éq = C·τ et [AH]éq = C(1 − τ) ; remplace dans Qr,éq et simplifie par C.",
      "la concentration de A moins égale celle des ions H trois O plus، égale C fois tau. و A H égale C fois un moins tau. عوض ف Q r، وبسط ب C.")],
    [("3 : [A⁻]éq = [H₃O⁺]éq = C·τ", "égale C fois tau"),
     ("[AH]éq = C − C·τ = C(1 − τ)", "C fois un moins tau"),
     ("Qr,éq = (C·τ)²/(C(1 − τ)) = C·τ²/(1 − τ)", "C fois tau au carré، sur un moins tau")],
    "السؤال trois. من le tableau: la concentration de A moins، égale celle des ions H trois O plus، égale C fois tau. l'acide خسر C fois tau، إذن كيبقى C fois un moins tau. نعوضو: Q r à l'équilibre égale C fois tau، au carré، sur C fois un moins tau. واحد C كيتحيد: Q r à l'équilibre égale C fois tau au carré، sur un moins tau.",
    "ex_3", "fa_3"),
  Q("4", "En déduire la valeur de la constante d'équilibre K associée à l'équation de la réaction.",
    "السؤال quatre: استنتج la valeur ديال la constante d'équilibre K.",
    val("K", K, None, f"K = Qr,éq = C·τ²/(1 − τ) = 5,0 × 10⁻³ × {fr(TAU, 3)}²/(1 − {fr(TAU, 3)}) ≈ {sci(K, 1)}", tol=0.05),
    (["K = Qr,éq", "C·τ²/(1 − τ)", "sans unité"], ["K = C·τ", "K = τ²/(1 − τ)"]),
    [("À l'équilibre, que vaut K par rapport à Qr,éq ?", "فl'état d'équilibre، K شحال كتساوي بالنسبة ل Q r à l'équilibre؟"),
     ("K = Qr,éq = C·τ²/(1 − τ) : remplace C = 5,0 × 10⁻³ mol/L et τ (garde trois chiffres).",
      "K égale Q r à l'équilibre، égale C fois tau au carré، sur un moins tau. عوض C و tau.")],
    [("4 : K = Qr,éq = C·τ²/(1 − τ)", "K égale Q r à l'équilibre"),
     (f"K = 5,0 × 10⁻³ × {fr(TAU, 3)}²/(1 − {fr(TAU, 3)})", "l'application numérique"),
     (f"K ≈ {sci(K, 1)} (sans unité)", f"K égale {dsci(K, 1)}")],
    f"السؤال quatre. K égale Q r à l'équilibre، égale C fois tau au carré، sur un moins tau. l'application numérique: cinq virgule zéro fois dix puissance moins trois، fois {dfr(TAU, 3)} au carré، sur un moins {dfr(TAU, 3)}. K égale {dsci(K, 1)}، بلا وحدة.",
    "ex_4", "fa_4"),
  Q("5", "On dilue dix fois la solution : C' = 5,0 × 10⁻⁴ mol/L. Le pH mesuré devient pH' = 3,79. Calculer le nouveau taux τ', puis préciser l'effet de la dilution sur τ et sur K.",
    "السؤال cinq: كنخففو la solution dix fois: C prime égale cinq virgule zéro fois dix puissance moins quatre mole par litre، و le p H ولا trois virgule soixante-dix-neuf. حسب tau prime، وشنو l'effet ديال la dilution على tau و على K؟",
    val("τ'", TAU2, None, f"τ' = 10^(−3,79)/(5,0 × 10⁻⁴) ≈ {fr(TAU2, 2)} > τ : la dilution augmente τ ; K ne change pas (il ne dépend que de la température)", tol=0.05),
    (["τ = 10^(−pH)/C", "C'", "K ne dépend que de la température"], ["K diminue", "τ' = τ/10"]),
    [("Même relation qu'à la question 2, avec C' et pH'. Compare ensuite τ' et τ.",
      "نفس la relation ديال السؤال deux، ب C prime و p H prime. ومن بعد قارن tau prime مع tau."),
     ("τ' = 10^(−pH')/C'. Pour K : de quoi dépend-elle ? Pas de la concentration initiale.",
      "tau prime égale dix puissance moins p H prime، sur C prime. و K: كتتعلق غير ب la température، ماشي ب la concentration.")],
    [(f"5 : τ' = 10^(−3,79)/(5,0 × 10⁻⁴) ≈ {fr(TAU2, 2)}", f"tau prime égale {dfr(TAU2, 2)}"),
     (f"τ' > τ = {fr(TAU, 2)} : la dilution augmente le taux d'avancement final", "la dilution كتكبر tau"),
     ("K reste la même : elle ne dépend que de la température", "K ما كتبدلش")],
    f"السؤال cinq. tau prime égale dix puissance moins trois virgule soixante-dix-neuf، sur cinq virgule zéro fois dix puissance moins quatre. tau prime égale {dfr(TAU2, 2)}. كبر من tau، اللي كان {dfr(TAU, 2)}: إذن la dilution كتكبر tau. و K ما كتبدلش، حيت K كتتعلق غير ب la température.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  slide("ex_1", "definition", "Question 1 : l'équation de l'acide avec l'eau",
        "AH cède un proton à l'eau ; réaction limitée : ⇌.",
        "فالتمرين ديالنا، نفس الشكل مع l'acide ascorbique: " + EQ_DIT + ".",
        [(EQ, "فالتمرين ديالنا، نفس الشكل")]),
  slide("ex_2", "taux", "Question 2 : τ = 10^(−pH)/C",
        "x_max = C·V, x_éq = [H₃O⁺]éq·V : V se simplifie.",
        f"فالتمرين ديالنا: tau égale dix puissance moins trois virgule vingt-trois، sur cinq virgule zéro fois dix puissance moins trois، يعني {dfr(TAU, 2)}. tau صغير من un: la réaction محدودة.",
        [("τ = 10^(−pH)/C", "فالتمرين ديالنا: tau égale"), (f"τ ≈ {fr(TAU, 2)} < 1 : limitée", "la réaction محدودة")]),
  slide("ex_3", "c_tau", "Question 3 : montrer que Qr,éq = C·τ²/(1 − τ)",
        "Chaque concentration à l'équilibre s'écrit avec C et τ.",
        "فالتمرين ديالنا نفس الخطوات: A moins و les ions H trois O plus، C fois tau. و A H، C fois un moins tau. إذن Q r à l'équilibre égale C fois tau au carré، sur un moins tau.",
        [("[A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C(1 − τ)", "فالتمرين ديالنا نفس الخطوات"), (KREL, "إذن Q r à l'équilibre égale C fois tau au carré")]),
  slide("ex_4", "k_def", "Question 4 : K = Qr,éq",
        "À l'équilibre, Qr prend la valeur K.",
        f"فالتمرين ديالنا: K égale Q r à l'équilibre، égale cinq virgule zéro fois dix puissance moins trois، fois {dfr(TAU, 3)} au carré، sur un moins {dfr(TAU, 3)}. K égale {dsci(K, 1)}.",
        [(f"K = C·τ²/(1 − τ) ≈ {sci(K, 1)}", f"K égale {dsci(K, 1)}")]),
  slide("ex_5", "dilution", "Question 5 : diluer change τ, pas K",
        "Même acide, même température : même K ; plus C est petite, plus τ est grand.",
        f"فالتمرين ديالنا: ب C prime égale cinq virgule zéro fois dix puissance moins quatre mole par litre، tau prime égale dix puissance moins trois virgule soixante-dix-neuf، sur C prime، يعني {dfr(TAU2, 2)}. كبر من {dfr(TAU, 2)}. و K بقات هي هي.",
        [(f"τ' = 10^(−3,79)/(5,0 × 10⁻⁴) ≈ {fr(TAU2, 2)}", f"يعني {dfr(TAU2, 2)}"), ("K inchangée", "و K بقات هي هي")]),
]

FACILES = [
  vf("fa_1", "Plus facile : vrai ou faux", "L'acide ascorbique AH dans l'eau.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Dans l'équation, AH cède un proton à l'eau.", True, "L'eau est la base qui capte H⁺ : elle devient H₃O⁺."),
      ("On écrit une flèche simple, car la réaction est rapide.", False, "Rapide ne veut pas dire totale : la réaction est limitée, on écrit ⇌."),
      ("La base conjuguée de AH est A⁻.", True, "AH et A⁻ forment le couple AH/A⁻.")]),
  qcm("fa_2", "Plus facile : le taux d'avancement final", "سؤال ساهل: اختار la bonne relation ديال tau.",
      "Pour un acide de concentration C dans l'eau, τ = …",
      ["C/10^(−pH)", "10^(−pH)/C", "10^(−pH)·C"], 1, {
        1: ("juste", "برافو! tau égale x éq sur x max، يعني dix puissance moins p H، sur C.", "Juste : τ = x_éq/x_max = 10^(−pH)/C."),
        0: (("لا، قلبتي الكسر. tau ديما صغير من un ولا يساوي un: x éq الفوق، و x max التحت. عاود اختار.", "Fraction renversée : τ = x_éq/x_max ≤ 1. Réessaie."),
            ("الجواب: tau égale dix puissance moins p H، sur C.", "Réponse : τ = 10^(−pH)/C.")),
        2: (("لا، tau ماشي ضرب. هو x éq sur x max: شنو كيعطي كل واحد فيهم؟ عاود اختار.", "τ est un quotient x_éq/x_max, pas un produit. Réessaie."),
            ("الجواب: tau égale dix puissance moins p H، sur C.", "Réponse : τ = 10^(−pH)/C."))},
      "Pour un acide de concentration C dans l'eau, tau égale quoi ?"),
  qcm("fa_3", "Plus facile : l'acide restant", "سؤال ساهل: شحال بقا من l'acide à l'équilibre؟",
      "À l'équilibre, [A⁻]éq = C·τ. Que vaut [AH]éq ?",
      ["C", "C·τ", "C(1 − τ)"], 2, {
        2: ("juste", "برافو! l'acide خسر C fois tau، إذن كيبقى C fois un moins tau.", "Juste : [AH]éq = C − C·τ = C(1 − τ)."),
        0: (("قريب! ولكن l'acide تفاعل شوية: خسر C fois tau. عاود اختار.", "L'acide a un peu réagi : il a perdu C·τ. Réessaie."),
            ("الجواب: C fois un moins tau.", "Réponse : [AH]éq = C(1 − τ).")),
        1: (("لا، C fois tau هو اللي تكون من A moins. و l'acide اللي بقا؟ عاود اختار.", "C·τ, c'est ce qui s'est formé ; l'acide restant est différent. Réessaie."),
            ("الجواب: l'acide اللي بقا هو C fois un moins tau.", "Réponse : [AH]éq = C(1 − τ)."))},
      "À l'équilibre، la concentration de A moins égale C fois tau. Que vaut la concentration de A H ?"),
  qcm("fa_4", "Plus facile : calculer K", "سؤال ساهل: اختار la valeur ديال K.",
      f"C = 5,0 × 10⁻³ mol/L et τ = 0,118. K = C·τ²/(1 − τ) vaut environ…",
      ["7,9 × 10⁻⁵", "6,7 × 10⁻⁴", "6,9 × 10⁻⁵ mol/L"], 0, {
        0: ("juste", "برافو! K égale sept virgule neuf fois dix puissance moins cinq، بلا وحدة.", "Juste : K ≈ 7,9 × 10⁻⁵."),
        1: (("لا، هاد القيمة كتجي من C fois tau، بلا tau الثاني وبلا un moins tau. عاود اختار.", "6,7 × 10⁻⁴ ≈ C·τ/(1 − τ) : il manque un τ. Réessaie."),
            ("الجواب: sept virgule neuf fois dix puissance moins cinq: tau au carré.", "Réponse : K = 5,0 × 10⁻³ × 0,118²/0,882 ≈ 7,9 × 10⁻⁵.")),
        2: (("لا، هادي نسيتي un moins tau، و K ما عندهاش وحدة. عاود اختار.", "Tu as oublié de diviser par 1 − τ, et K n'a pas d'unité. Réessaie."),
            ("الجواب: sept virgule neuf fois dix puissance moins cinq، بلا وحدة.", "Réponse : K ≈ 7,9 × 10⁻⁵, sans unité."))},
      "C égale cinq virgule zéro fois dix puissance moins trois mole par litre، et tau égale zéro virgule cent dix-huit. K vaut environ ?"),
  vf("fa_5", "Plus facile : la dilution", "On dilue dix fois la solution d'acide ascorbique.",
     "سؤال ساهل على la dilution: قول واش صحيح ولا غالط.",
     [("Après dilution, τ augmente.", True, "Même K, C plus petite : τ plus grand (0,32 au lieu de 0,12)."),
      ("Après dilution, K diminue, car la solution est moins concentrée.", False, "K ne dépend que de la température : elle ne change pas."),
      ("Après dilution, le pH augmente.", True, "[H₃O⁺] diminue (de 5,9 × 10⁻⁴ à 1,6 × 10⁻⁴ mol/L) : le pH monte.")]),
]

SIM_Q = [
  QS("1", "Écrire l'équation de la réaction de AH avec l'eau.", phrase(EQ), (["⇌", "H₃O⁺"], ["→"]),
     [(EQ, "كيعطيو A moins")], EQ_DIT + "."),
  QS("2", "Montrer que τ = 10^(−pH)/C, calculer τ et conclure.",
     val("τ", sTAU, None, f"τ = 10^(−3,07)/(1,0 × 10⁻²) ≈ {fr(sTAU, 3)} < 1 : limitée", tol=0.05),
     (["τ = x_éq/x_max", "10^(−pH)"], ["τ = C/10^(−pH)"]),
     [("τ = x_éq/x_max = 10^(−pH)/C", "tau égale dix puissance moins p H، sur C"),
      (f"τ ≈ {fr(sTAU, 3)} < 1 : réaction limitée", f"tau égale {dfr(sTAU, 3)}")],
     f"x max égale C fois V، و x éq égale la concentration des ions H trois O plus fois V. إذن tau égale dix puissance moins p H، sur C. tau égale {dfr(sTAU, 3)}، صغير من un: la réaction محدودة."),
  QS("3", "Montrer que Qr,éq = C·τ²/(1 − τ).",
     phrase("[A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C(1 − τ) ; Qr,éq = C·τ²/(1 − τ)"),
     (["C·τ", "C(1 − τ)"], ["[AH]éq = C"]),
     [("[A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C(1 − τ)", "C fois tau"), (KREL, "C fois tau au carré، sur un moins tau")],
     "A moins و les ions H trois O plus: C fois tau. A H: C fois un moins tau. إذن Q r à l'équilibre égale C fois tau au carré، sur un moins tau."),
  QS("4", "En déduire K.",
     val("K", sK, None, f"K = 1,0 × 10⁻² × {fr(sTAU, 4)}²/(1 − {fr(sTAU, 4)}) ≈ {sci(sK, 1)}", tol=0.05),
     (["K = Qr,éq"], ["K = C·τ"]),
     [(f"K = C·τ²/(1 − τ) ≈ {sci(sK, 1)}", f"{dsci(sK, 1)}")],
     f"K égale C fois tau au carré، sur un moins tau، يعني {dsci(sK, 1)}، بلا وحدة."),
  QS("5", "On dilue dix fois : C' = 1,0 × 10⁻³ mol/L et pH' = 3,61. Calculer τ' et préciser l'effet de la dilution sur τ et K.",
     val("τ'", sTAU2, None, f"τ' = 10^(−3,61)/(1,0 × 10⁻³) ≈ {fr(sTAU2, 2)} > τ ; K inchangée", tol=0.05),
     (["τ = 10^(−pH)/C"], ["K diminue"]),
     [(f"τ' ≈ {fr(sTAU2, 2)} > τ : la dilution augmente τ", f"يعني {dfr(sTAU2, 2)}"),
      ("K ne dépend que de la température : inchangée", "K ما كتبدلش")],
     f"tau prime égale dix puissance moins trois virgule soixante et un، sur un virgule zéro fois dix puissance moins trois، يعني {dfr(sTAU2, 2)}. la dilution كتكبر tau، و K ما كتبدلش."),
]

EX = exercice(
  "phys_ex_ch12_etat_equilibre_3", "phys_ch12_etat_equilibre", "etat_equilibre",
  "La vitamine C dans l'eau : τ, K et la dilution", "moyen", 25,
  ["Montrer que τ = 10^(−pH)/C et conclure", "Établir Qr,éq = C·τ²/(1 − τ)", "Calculer K", "Prévoir l'effet de la dilution sur τ et K"],
  "L'acide ascorbique (vitamine C), de formule C₆H₈O₆, est noté AH ; sa base conjuguée est notée A⁻. On dissout un comprimé dans l'eau pour obtenir une solution S de volume V et de concentration C = 5,0 × 10⁻³ mol/L. À 25 °C, le pH de S vaut 3,23. On dilue ensuite S dix fois.",
  "دابا نقراو l'énoncé. l'acide ascorbique، يعني la vitamine C، كنسميوه A H، و la base ديالو A moins. كنذوبو comprimé فالما، وكنلقاو solution S، la concentration ديالها C égale cinq virgule zéro fois dix puissance moins trois mole par litre. le p H ديالها trois virgule vingt-trois. ومن بعد كنخففو S dix fois.",
  [], ["C = 5,0 × 10⁻³ mol/L ; pH = 3,23 (25 °C)", "Après dilution dix fois : C' = 5,0 × 10⁻⁴ mol/L ; pH' = 3,79", "Couple AH/A⁻"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Une solution d'acide ascorbique AH a une concentration C = 1,0 × 10⁻² mol/L et un pH = 3,07 à 25 °C. On la dilue dix fois.",
  "نفس التمرين، بقيم أخرى: C égale un virgule zéro fois dix puissance moins deux mole par litre، و le p H trois virgule zéro sept.",
  [], ["C = 1,0 × 10⁻² mol/L ; pH = 3,07", "Après dilution dix fois : C' = 1,0 × 10⁻³ mol/L ; pH' = 3,61"],
  SIM_Q)

ecrire(EX)
