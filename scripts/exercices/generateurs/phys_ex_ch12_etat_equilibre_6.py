# Exercice de chimie, ch. 12 (état d'équilibre), niveau supérieur (au-dessus du national, même forme) : un même acide
# à deux concentrations ; τ, K et sa constance, une lecture critique, puis PRÉVOIR τ et le pH d'une troisième
# solution à partir de K (équation du second degré en τ) : deux notions combinées, moins de guidage.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2021 R (9 montrer τ = 10^(−pH)/C, 10-11 effet de la dilution sur τ), 2017 N
#    (1.1-1.2 τ puis Qr,éq), 2020 R (1.3-1.4 Qr,éq en fonction de C et τ), 2023 N (1.2 proportion à l'équilibre) ;
#    au national, K est calculée à partir d'une mesure ; ici on va plus loin : on s'en sert pour prévoir ;
#  - profs (architecture/phys_ch12_etat_equilibre.md § 1 : Naceiri Mrabti, activité « plusieurs concentrations, le
#    même Qr,éq » ; El Goufifa, Moutamadris, fiche 2BAC, Bazhar : facteurs de τ) ; piège : « τ change donc K change » ;
#  - séries en ligne : talamidi (état d'équilibre, activités 1 : influence de l'état initial puis de K sur τ),
#    talamidi (acide-base, exercices non corrigés 2 : τ en fonction du pH et de C), moutamadris (exercices état
#    d'équilibre), alloschool (El Goufifa, séance 9), Naceiri Mrabti (livre 2BAC), coursdusoirpc (TD BIOF).
# Ici : l'acide lactique à nos concentrations ; pH calculés à partir de K ≈ 1,4 × 10⁻⁴ ; τ₃ par le trinôme.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _ch12 import *


def mesure(C, pH):
    h = h3o(pH); t = h / C
    return h, t, C * t * t / (1 - t)


def prevoir(C, K):
    t = (-K + math.sqrt(K * K + 4 * C * K)) / (2 * C)
    return t, -math.log10(C * t)


C1, P1, C2, P2, C3 = 5.0e-2, 2.59, 5.0e-3, 3.12, 1.0e-3
H1, T1, K1 = mesure(C1, P1)
H2, T2, K2 = mesure(C2, P2)
KR = 1.4e-4
T3, P3 = prevoir(C3, KR)
assert fr(T1, 3) == "0,051" and fr(T2, 2) == "0,15" and sci(K1, 1) == "1,4 × 10⁻⁴" and sci(K2, 1) == "1,4 × 10⁻⁴"
assert fr(T3, 2) == "0,31" and fr(P3, 2) == "3,51"
assert abs(C3 * T3 ** 2 + KR * T3 - KR) < 1e-12
sC1, sP1, sC2, sP2, sC3 = 1.0e-1, 2.44, 1.0e-2, 2.96, 2.0e-3
sH1, sT1, sK1 = mesure(sC1, sP1)
sH2, sT2, sK2 = mesure(sC2, sP2)
sT3, sP3 = prevoir(sC3, KR)
assert fr(sT1, 3) == "0,036" and fr(sT2, 2) == "0,11" and sci(sK1, 1) == "1,4 × 10⁻⁴" and sci(sK2, 1) == "1,4 × 10⁻⁴"
assert fr(sT3, 2) == "0,23" and fr(sP3, 2) == "3,33"

TRI = "C·τ² + K·τ − K = 0"
TRI_DIT = "C fois tau au carré، plus K fois tau، moins K، égale zéro"

QUESTIONS = [
  Q("1", "Calculer le taux d'avancement final τ₁ de la réaction de l'acide lactique avec l'eau dans S₁.",
    "السؤال un: حسب tau un، le taux d'avancement final ديال l'acide lactique مع الما فS un.",
    val("τ₁", T1, None, f"τ₁ = x_éq/x_max = 10^(−pH₁)/C₁ = 10^(−2,59)/(5,0 × 10⁻²) ≈ {fr(T1, 3)}", tol=0.05),
    (["τ = x_éq/x_max", "10^(−pH)/C"], ["τ = C/10^(−pH)", "τ = 10^(−2pH)/C"]),
    [("Le tableau d'avancement donne x_max (l'eau en excès) et x_éq (les ions H₃O⁺ formés).", "le tableau كيعطي x max، الما en excès، و x éq، les ions H trois O plus اللي تكونو."),
     ("τ = 10^(−pH)/C.", "tau égale dix puissance moins p H، sur C.")],
    [("1 : τ₁ = 10^(−pH₁)/C₁", "tau un égale dix puissance moins p H un"),
     (f"τ₁ = 10^(−2,59)/(5,0 × 10⁻²) ≈ {fr(T1, 3)}", f"tau un égale {dfr(T1, 3)}")],
    f"السؤال un. tau un égale dix puissance moins p H un، sur C un: dix puissance moins deux virgule cinquante-neuf، sur cinq virgule zéro fois dix puissance moins deux. tau un égale {dfr(T1, 3)}.",
    "ex_1", "fa_1"),
  Q("2", "S₂ est obtenue en diluant S₁ dix fois. Calculer τ₂. Quel est l'effet de la dilution sur le taux d'avancement final ?",
    "السؤال deux: S deux هي S un مخففة dix fois. حسب tau deux. شنو l'effet ديال la dilution على tau؟",
    val("τ₂", T2, None, f"τ₂ = 10^(−3,12)/(5,0 × 10⁻³) ≈ {fr(T2, 2)} > τ₁ : la dilution augmente τ", tol=0.05),
    (["τ = 10^(−pH)/C", "C₂ = C₁/10"], ["τ₂ = τ₁/10", "τ₂ = 10·τ₁"]),
    [("Quelle est la concentration de S₂ ? Puis même relation qu'en 1.", "شحال la concentration ديال S deux؟ ومن بعد نفس la relation."),
     ("C₂ = C₁/10 = 5,0 × 10⁻³ mol/L ; τ₂ = 10^(−3,12)/C₂ ; compare à τ₁.", "C deux égale C un sur dix، يعني cinq virgule zéro fois dix puissance moins trois. tau deux égale dix puissance moins trois virgule douze، sur C deux. وقارن مع tau un.")],
    [("2 : C₂ = C₁/10 = 5,0 × 10⁻³ mol/L", "C deux égale C un sur dix"),
     (f"τ₂ = 10^(−3,12)/(5,0 × 10⁻³) ≈ {fr(T2, 2)}", f"يعني {dfr(T2, 2)}"),
     ("τ₂ > τ₁ : la dilution augmente le taux d'avancement final", "la dilution كتكبر tau")],
    f"السؤال deux. C deux égale C un sur dix، cinq virgule zéro fois dix puissance moins trois mole par litre. tau deux égale dix puissance moins trois virgule douze، sur C deux، يعني {dfr(T2, 2)}. كبر من tau un: la dilution كتكبر tau. ورد البال: tau ما ضربش ف dix.",
    "ex_2", "fa_2"),
  Q("3", "Montrer que la constante d'équilibre s'écrit K = C·τ²/(1 − τ), puis la calculer à partir de S₁ et à partir de S₂.",
    "السؤال trois: بين بلي K égale C fois tau au carré، sur un moins tau، ومن بعد حسبها ب S un و ب S deux.",
    val("K", K1, None, f"K = C·τ²/(1 − τ) ; S₂ : K ≈ {sci(K2, 1)} ; S₁ : K = 5,0 × 10⁻² × {fr(T1, 4)}²/(1 − {fr(T1, 4)}) ≈ {sci(K1, 1)}", tol=0.05),
    (["[A⁻]éq = [H₃O⁺]éq = C·τ", "[AH]éq = C(1 − τ)", "K = Qr,éq"], ["K = C·τ/(1 − τ)", "K = τ²/(1 − τ)"]),
    [("Écris les trois concentrations à l'équilibre en fonction de C et τ, puis K = Qr,éq.", "كتب les trois concentrations à l'équilibre ب C و tau، ومن بعد K égale Q r à l'équilibre."),
     ("[A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C(1 − τ). Garde trois chiffres pour τ dans le calcul.", "A moins و H trois O plus: C fois tau. A H: C fois un moins tau. وخلي trois chiffres ف tau فالحساب.")],
    [("3 : [A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C(1 − τ) ; K = C·τ²/(1 − τ)", "K égale C fois tau au carré، sur un moins tau"),
     (f"S₁ : K = 5,0 × 10⁻² × {fr(T1, 4)}²/(1 − {fr(T1, 4)}) ≈ {sci(K1, 1)}", "ب S un"),
     (f"S₂ : K = 5,0 × 10⁻³ × {fr(T2, 3)}²/(1 − {fr(T2, 3)}) ≈ {sci(K2, 1)}", "و ب S deux")],
    f"السؤال trois. A moins و H trois O plus: C fois tau. A H: C fois un moins tau. نعوضو ف Q r à l'équilibre، وواحد C كيتحيد: K égale C fois tau au carré، sur un moins tau. ب S un: K égale {dsci(K1, 1)}. و ب S deux: K égale {dsci(K2, 1)}. نفس القيمة.",
    "ex_3", "fa_3"),
  Q("4", "Un élève écrit : « Quand on dilue, τ change ; donc la constante d'équilibre K change aussi. » Critiquer cette affirmation à l'aide des résultats précédents.",
    "السؤال quatre: تلميذ كتب: ملي كنخففو، tau كيتبدل، إذن K حتى هي كتبدل. ناقش هاد الجملة بالنتائج اللي لقيتي.",
    phrase("Faux : τ passe de 0,051 à 0,15 mais K garde la même valeur (≈ 1,4 × 10⁻⁴) dans S₁ et S₂. K ne dépend que de la température ; τ dépend de l'état initial (C) et de K."),
    (["K ≈ 1,4 × 10⁻⁴ dans S₁ et S₂", "K ne dépend que de la température", "τ dépend de C"], ["K dépend de C", "τ = K"]),
    [("Compare les deux valeurs de K trouvées à la question 3.", "قارن deux valeurs ديال K اللي لقيتي فالسؤال trois."),
     ("Si K était changée par la dilution, les deux calculs donneraient deux valeurs différentes. De quoi K dépend-elle seulement ?",
      "يلا كانت K كتبدل ب la dilution، deux calculs كانو غادي يعطيو deux valeurs مختلفين. K كتتعلق غير ب شنو؟")],
    [("4 : l'affirmation est fausse", "هاد الجملة غالطة"),
     (f"τ change ({fr(T1, 3)} puis {fr(T2, 2)}) mais K ≈ {sci(K1, 1)} dans les deux solutions", "ولكن K بقات"),
     ("K ne dépend que de la température ; τ dépend de C et de K", "K كتتعلق غير ب la température")],
    f"السؤال quatre. هاد الجملة غالطة. tau تبدل، من {dfr(T1, 3)} ل {dfr(T2, 2)}، ولكن K بقات {dsci(K1, 1)} فجوج. K كتتعلق غير ب la température. أما tau، كيتعلق ب C و ب K.",
    "ex_4", "fa_4"),
  Q("5", "On prépare une solution S₃ du même acide, de concentration C₃ = 1,0 × 10⁻³ mol/L, à 25 °C. On prend K = 1,4 × 10⁻⁴. Montrer que τ₃ vérifie C₃·τ₃² + K·τ₃ − K = 0, puis calculer τ₃.",
    "السؤال cinq: كنوجدو S trois، نفس l'acide، C trois égale un virgule zéro fois dix puissance moins trois mole par litre. كناخدو K égale un virgule quatre fois dix puissance moins quatre. بين بلي " + TRI_DIT + "، ومن بعد حسب tau trois.",
    val("τ₃", T3, None, f"K = C₃·τ₃²/(1 − τ₃) ⇒ C₃·τ₃² + K·τ₃ − K = 0 ; τ₃ = (−K + √(K² + 4C₃K))/(2C₃) ≈ {fr(T3, 2)}", tol=0.04),
    (["K(1 − τ) = C·τ²", "Δ = K² + 4C·K", "τ = (−K + √Δ)/(2C)", "0 < τ < 1"], ["τ = (−K − √Δ)/(2C)", "τ = √(K/C)"]),
    [("Pars de K = C₃·τ₃²/(1 − τ₃) et fais passer (1 − τ₃) de l'autre côté.", "بدا من K égale C trois fois tau trois au carré، sur un moins tau trois، ودوز un moins tau trois للجهة الأخرى."),
     ("Tu obtiens un trinôme en τ₃ : Δ = K² + 4C₃K ; garde la racine positive (0 < τ₃ < 1).", "كتلقى معادلة من الدرجة الثانية ف tau trois: delta égale K au carré، plus quatre C trois K. خود la racine positive، حيت tau بين zéro و un.")],
    [("5 : K(1 − τ₃) = C₃·τ₃² ⇒ C₃·τ₃² + K·τ₃ − K = 0", "إذن " + TRI_DIT),
     ("Δ = K² + 4C₃·K ; τ₃ = (−K + √Δ)/(2C₃) (racine positive)", "tau خاصو يكون موجب"),
     (f"τ₃ ≈ {fr(T3, 2)}", f"tau trois égale {dfr(T3, 2)}")],
    f"السؤال cinq. K égale C trois fois tau trois au carré، sur un moins tau trois. نضربو ف un moins tau trois، ونجمعو فجهة وحدة: إذن {TRI_DIT}. delta égale K au carré، plus quatre C trois K. tau خاصو يكون موجب: tau trois égale moins K، plus racine de delta، sur deux C trois. tau trois égale {dfr(T3, 2)}.",
    "ex_5", "fa_5"),
  Q("6", "En déduire le pH attendu pour S₃. Vérifier la cohérence avec le sens d'évolution du pH quand on dilue.",
    "السؤال six: استنتج le p H ديال S trois. وتحقق واش متافق مع شنو كيوقع ل le p H ملي كنخففو.",
    val("pH₃", P3, None, f"[H₃O⁺]éq = C₃·τ₃ = {sci(C3 * T3, 2)} mol/L ; pH₃ = −log(C₃·τ₃) ≈ {fr(P3, 2)} (> 3,12 > 2,59 : le pH augmente quand on dilue)", tol=0.01),
    (["[H₃O⁺]éq = C·τ", "pH = −log[H₃O⁺]", "pH₃ > pH₂"], ["pH = −log(τ)", "pH = log(C·τ)"]),
    [("D'après le tableau, [H₃O⁺]éq = C₃·τ₃.", "من le tableau: la concentration des ions H trois O plus égale C trois fois tau trois."),
     ("pH₃ = −log(C₃·τ₃) ; compare à pH₁ = 2,59 et pH₂ = 3,12.", "p H trois égale moins log de C trois fois tau trois. وقارن مع deux virgule cinquante-neuf و trois virgule douze.")],
    [("6 : [H₃O⁺]éq = C₃·τ₃", "C trois fois tau trois"),
     (f"pH₃ = −log({sci(C3 * T3, 2)}) ≈ {fr(P3, 2)}", f"p H trois égale {dfr(P3, 2)}"),
     ("pH₁ < pH₂ < pH₃ : cohérent, la dilution fait monter le pH", "le p H كيطلع")],
    f"السؤال six. la concentration des ions H trois O plus égale C trois fois tau trois، يعني {dsci(C3 * T3, 2)} mole par litre. p H trois égale moins log ديالها: p H trois égale {dfr(P3, 2)}. كبر من trois virgule douze، و كبر من deux virgule cinquante-neuf: كل ما خففنا، le p H كيطلع. متافق.",
    "ex_6", "fa_6"),
]

EXPLICATIONS = [
  slide("ex_1", "taux", "Question 1 : τ₁",
        "τ = 10^(−pH)/C.",
        f"فالتمرين ديالنا: tau un égale dix puissance moins deux virgule cinquante-neuf، sur cinq virgule zéro fois dix puissance moins deux، يعني {dfr(T1, 3)}.",
        [(f"τ₁ ≈ {fr(T1, 3)}", f"يعني {dfr(T1, 3)}")]),
  slide("ex_2", "dilution", "Question 2 : diluer dix fois",
        "Plus C est petite, plus τ est grand, à K égale.",
        f"فالتمرين ديالنا: S deux، C deux égale cinq virgule zéro fois dix puissance moins trois، و tau deux égale {dfr(T2, 2)}، كبر من {dfr(T1, 3)}. ولكن ماشي dix fois كبر.",
        [(f"τ₂ ≈ {fr(T2, 2)} > τ₁ ≈ {fr(T1, 3)}", f"و tau deux égale {dfr(T2, 2)}")]),
  slide("ex_3", "c_tau", "Question 3 : K = C·τ²/(1 − τ)",
        "On établit la relation, puis on la calcule deux fois.",
        f"فالتمرين ديالنا: ب S un، K égale {dsci(K1, 1)}. و ب S deux، K égale {dsci(K2, 1)}. نفس القيمة.",
        [(f"S₁ et S₂ : K ≈ {sci(K1, 1)}", "نفس القيمة")]),
  slide("ex_4", "diluer", "Question 4 : ce qui change, ce qui ne change pas",
        "Diluer change C, [H₃O⁺], pH et τ ; jamais K.",
        f"فالتمرين ديالنا: tau تبدل، ولكن K بقات {dsci(K1, 1)}. إذن الجملة ديال التلميذ غالطة.",
        [("K inchangée : l'affirmation est fausse", "إذن الجملة ديال التلميذ غالطة")]),
  slide("ex_5", "courbe", "Question 5 : prévoir τ à partir de K et C",
        "K et C fixent τ : la courbe τ(C) se calcule avec K = C·τ²/(1 − τ).",
        f"هاد la courbe كتجي من la relation، K égale C fois tau au carré، sur un moins tau. فالتمرين ديالنا: {TRI_DIT}، مع C trois égale un virgule zéro fois dix puissance moins trois. la racine positive: tau trois égale {dfr(T3, 2)}.",
        [(TRI, "فالتمرين ديالنا"), (f"τ₃ ≈ {fr(T3, 2)}", f"tau trois égale {dfr(T3, 2)}")]),
  slide("ex_6", "couple", "Question 6 : du τ au pH",
        "[H₃O⁺]éq = C·τ, puis pH = −log[H₃O⁺].",
        f"فالتمرين ديالنا: la concentration des ions H trois O plus égale C trois fois tau trois، {dsci(C3 * T3, 2)} mole par litre. إذن p H trois égale {dfr(P3, 2)}.",
        [(f"pH₃ = −log(C₃·τ₃) ≈ {fr(P3, 2)}", f"إذن p H trois égale {dfr(P3, 2)}")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : τ₁", "سؤال ساهل: اختار tau un.",
      "pH₁ = 2,59 et C₁ = 5,0 × 10⁻² mol/L. τ₁ vaut environ…",
      ["0,051", "19,5", "1,3 × 10⁻⁴"], 0, {
        0: ("juste", "برافو! tau égale dix puissance moins p H، sur C.", "Juste : τ₁ = 2,57 × 10⁻³/5,0 × 10⁻² ≈ 0,051."),
        1: (("لا، قلبتي الكسر. tau ما يفوتش un. عاود اختار.", "Fraction renversée : τ ≤ 1. Réessaie."),
            ("الجواب: zéro virgule zéro cinquante et un.", "Réponse : τ₁ ≈ 0,051.")),
        2: (("لا، ضربتي ف C بلاصة ما تقسم. عاود اختار.", "On divise par C. Réessaie."),
            ("الجواب: zéro virgule zéro cinquante et un.", "Réponse : τ₁ = 10^(−2,59)/5,0 × 10⁻² ≈ 0,051."))},
      "p H un égale deux virgule cinquante-neuf، et C un égale cinq virgule zéro fois dix puissance moins deux mole par litre. tau un vaut environ ?"),
  vf("fa_2", "Plus facile : la dilution", "S₂ = S₁ diluée dix fois.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("Diluer dix fois multiplie τ par dix.", False, "τ passe de 0,051 à 0,15 : il augmente, mais pas dix fois."),
      ("Diluer augmente τ.", True, "À K égale, plus C est petite, plus τ est grand."),
      ("Diluer fait monter le pH.", True, "pH passe de 2,59 à 3,12.")]),
  qcm("fa_3", "Plus facile : le dénominateur de K", "سؤال ساهل: اختار l'expression ديال K.",
      "Pour l'acide lactique : [A⁻]éq = [H₃O⁺]éq = C·τ. Alors K = …",
      ["C·τ/(1 − τ)", "τ²/(1 − τ)", "C·τ²/(1 − τ)"], 2, {
        2: ("juste", "برافو! C au carré tau au carré، sur C fois un moins tau: يبقى C fois tau au carré، sur un moins tau.", "Juste : K = C·τ²/(1 − τ)."),
        0: (("لا، الفوق كاينين deux concentrations C fois tau: tau au carré. عاود اختار.", "Le numérateur a deux facteurs C·τ. Réessaie."),
            ("الجواب: C fois tau au carré، sur un moins tau.", "Réponse : K = C·τ²/(1 − τ).")),
        1: (("لا، C au carré الفوق و C التحت: يبقى واحد C. عاود اختار.", "Il reste un C après simplification. Réessaie."),
            ("الجواب: C fois tau au carré، sur un moins tau.", "Réponse : K = C·τ²/(1 − τ)."))},
      "Pour l'acide lactique، K égale quoi ?"),
  vf("fa_4", "Plus facile : K et la dilution", "S₁ et S₂ : même acide, même température.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("K calculée avec S₁ et K calculée avec S₂ sont presque égales.", True, "Les deux donnent K ≈ 1,4 × 10⁻⁴."),
      ("K dépend de la concentration initiale C.", False, "K ne dépend que de la température."),
      ("τ dépend de la concentration initiale C.", True, "τ₁ ≈ 0,051 et τ₂ ≈ 0,15.")]),
  qcm("fa_5", "Plus facile : l'équation en τ", "سؤال ساهل: اختار l'équation ديال tau.",
      "K = C·τ²/(1 − τ). En multipliant par (1 − τ), on obtient…",
      ["C·τ² + K·τ − K = 0", "C·τ² − K·τ + K = 0", "C·τ² + K = 0"], 0, {
        0: ("juste", "برافو! K moins K fois tau égale C fois tau au carré، إذن C fois tau au carré، plus K fois tau، moins K، égale zéro.", "Juste : K − K·τ = C·τ², soit C·τ² + K·τ − K = 0."),
        1: (("لا، شوف les signes: ملي كندوزو K moins K fois tau للجهة الأخرى، كيتقلبو. عاود اختار.", "Vérifie les signes en changeant de côté. Réessaie."),
            ("الجواب: C fois tau au carré، plus K fois tau، moins K، égale zéro.", "Réponse : C·τ² + K·τ − K = 0.")),
        2: (("لا، نسيتي K fois tau اللي جات من le produit K fois un moins tau. عاود اختار.", "Il manque le terme K·τ. Réessaie."),
            ("الجواب: C fois tau au carré، plus K fois tau، moins K، égale zéro.", "Réponse : C·τ² + K·τ − K = 0."))},
      "K égale C fois tau au carré، sur un moins tau. En multipliant par un moins tau، on obtient quoi ?"),
  qcm("fa_6", "Plus facile : le pH de S₃", "سؤال ساهل: من tau ل le p H.",
      "C₃ = 1,0 × 10⁻³ mol/L et τ₃ = 0,31. Le pH de S₃ vaut environ…",
      ["0,51", "3,51", "3,00"], 1, {
        1: ("juste", "برافو! la concentration égale C trois fois tau trois، trois virgule un fois dix puissance moins quatre، و le p H trois virgule cinquante et un.", "Juste : pH = −log(3,1 × 10⁻⁴) ≈ 3,51."),
        0: (("لا، هادي moins log de tau بوحدو. خاصك la concentration: C fois tau. عاود اختار.", "−log(τ) n'est pas le pH : il faut −log(C·τ). Réessaie."),
            ("الجواب: trois virgule cinquante et un.", "Réponse : pH = −log(C₃·τ₃) ≈ 3,51.")),
        2: (("قريب! هادا ل acide كيتفاعل كامل: moins log de C. ولكن tau صغير من un. عاود اختار.", "3,00, c'est si la réaction était totale (τ = 1). Réessaie."),
            ("الجواب: trois virgule cinquante et un، حيت tau égale zéro virgule trente et un.", "Réponse : pH ≈ 3,51."))},
      "C trois égale un virgule zéro fois dix puissance moins trois mole par litre، et tau trois égale zéro virgule trente et un. Le p H vaut environ ?"),
]

SIM_Q = [
  QS("1", "Calculer τ₁ (S₁ : C₁ = 1,0 × 10⁻¹ mol/L, pH₁ = 2,44).",
     val("τ₁", sT1, None, f"τ₁ = 10^(−2,44)/(1,0 × 10⁻¹) ≈ {fr(sT1, 3)}", tol=0.05),
     (["10^(−pH)/C"], ["C/10^(−pH)"]),
     [(f"τ₁ ≈ {fr(sT1, 3)}", f"{dfr(sT1, 3)}")],
     f"tau un égale dix puissance moins deux virgule quarante-quatre، sur un virgule zéro fois dix puissance moins un، يعني {dfr(sT1, 3)}."),
  QS("2", "S₂ = S₁ diluée dix fois, pH₂ = 2,96. Calculer τ₂ ; effet de la dilution ?",
     val("τ₂", sT2, None, f"τ₂ = 10^(−2,96)/(1,0 × 10⁻²) ≈ {fr(sT2, 2)} > τ₁", tol=0.05),
     (["C₂ = C₁/10"], ["τ₂ = 10·τ₁"]),
     [(f"τ₂ ≈ {fr(sT2, 2)} > τ₁ : la dilution augmente τ", f"{dfr(sT2, 2)}")],
     f"tau deux égale {dfr(sT2, 2)}، كبر من tau un: la dilution كتكبر tau."),
  QS("3", "Montrer que K = C·τ²/(1 − τ) et la calculer avec S₁ et S₂.",
     val("K", sK1, None, f"S₂ : K ≈ {sci(sK2, 1)} ; S₁ : K ≈ {sci(sK1, 1)}", tol=0.05),
     (["C·τ", "C(1 − τ)"], ["K = C·τ"]),
     [(f"K = C·τ²/(1 − τ) ≈ {sci(sK1, 1)} (S₁ et S₂)", f"{dsci(sK1, 1)}")],
     f"K égale C fois tau au carré، sur un moins tau. ب S un و ب S deux: K égale {dsci(sK1, 1)}."),
  QS("4", "Critiquer : « τ change quand on dilue, donc K change ».",
     phrase("Faux : K garde la même valeur dans S₁ et S₂ ; K ne dépend que de la température, τ dépend de C."),
     (["K ne dépend que de la température"], ["K dépend de C"]),
     [("Faux : même K dans S₁ et S₂ ; K ne dépend que de la température", "غالطة")],
     "هاد الجملة غالطة: K بقات نفس القيمة. K كتتعلق غير ب la température."),
  QS("5", "S₃ : C₃ = 2,0 × 10⁻³ mol/L, K = 1,4 × 10⁻⁴. Montrer que C₃·τ₃² + K·τ₃ − K = 0 et calculer τ₃.",
     val("τ₃", sT3, None, f"τ₃ = (−K + √(K² + 4C₃K))/(2C₃) ≈ {fr(sT3, 2)}", tol=0.04),
     (["Δ = K² + 4C·K"], ["racine négative"]),
     [(TRI, TRI_DIT), (f"τ₃ ≈ {fr(sT3, 2)}", f"tau trois égale {dfr(sT3, 2)}")],
     f"{TRI_DIT}. la racine positive: tau trois égale {dfr(sT3, 2)}."),
  QS("6", "En déduire pH₃.",
     val("pH₃", sP3, None, f"pH₃ = −log(C₃·τ₃) = −log({sci(sC3 * sT3, 2)}) ≈ {fr(sP3, 2)}", tol=0.01),
     (["pH = −log(C·τ)"], ["pH = −log(τ)"]),
     [(f"pH₃ = −log(C₃·τ₃) ≈ {fr(sP3, 2)}", f"p H trois égale {dfr(sP3, 2)}")],
     f"la concentration égale C trois fois tau trois، إذن p H trois égale {dfr(sP3, 2)}."),
]

EX = exercice(
  "phys_ex_ch12_etat_equilibre_6", "phys_ch12_etat_equilibre", "etat_equilibre",
  "L'acide lactique dilué : K ne change pas, τ se prévoit", "difficile", 35,
  ["Calculer τ et prévoir l'effet de la dilution", "Établir et calculer K = C·τ²/(1 − τ)", "Critiquer un raisonnement sur K", "Prévoir τ et le pH à partir de K et C"],
  "L'acide lactique, noté AH, réagit avec l'eau selon : AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq). À 25 °C, une solution S₁ de concentration C₁ = 5,0 × 10⁻² mol/L a un pH₁ = 2,59. On dilue S₁ dix fois : la solution S₂ obtenue a un pH₂ = 3,12. Les mesures sont faites à l'équilibre.",
  "دابا نقراو l'énoncé. l'acide lactique، A H، كيتفاعل مع الما ب la double flèche. solution S un، C un égale cinq virgule zéro fois dix puissance moins deux mole par litre، و le p H ديالها deux virgule cinquante-neuf. كنخففو S un dix fois: S deux، و le p H ديالها trois virgule douze.",
  [], ["S₁ : C₁ = 5,0 × 10⁻² mol/L ; pH₁ = 2,59", "S₂ : S₁ diluée dix fois ; pH₂ = 3,12", "Question 5 : C₃ = 1,0 × 10⁻³ mol/L ; K = 1,4 × 10⁻⁴ (25 °C)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Acide lactique AH à 25 °C : S₁ de concentration C₁ = 1,0 × 10⁻¹ mol/L et pH₁ = 2,44 ; S₂ = S₁ diluée dix fois, pH₂ = 2,96.",
  "نفس التمرين، بقيم أخرى: C un égale un virgule zéro fois dix puissance moins un mole par litre، p H un égale deux virgule quarante-quatre، و S deux مخففة dix fois، p H deux égale deux virgule quatre-vingt-seize.",
  [], ["S₁ : C₁ = 1,0 × 10⁻¹ mol/L ; pH₁ = 2,44", "S₂ : pH₂ = 2,96", "Question 5 : C₃ = 2,0 × 10⁻³ mol/L ; K = 1,4 × 10⁻⁴"],
  SIM_Q)

ecrire(EX)
