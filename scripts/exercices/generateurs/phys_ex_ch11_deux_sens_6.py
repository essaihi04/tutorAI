# Exercice de chimie, ch. 11 (transformations dans les deux sens), niveau supérieur (au-dessus du national, même
# forme) : l'état d'équilibre d'une solution d'acide benzoïque, la proportion α = 1 − τ, la composition à
# l'équilibre, puis un ajout de la base conjuguée : le pH monte, sens inverse, ions H₃O⁺ consommés, et la lecture
# critique « plus rien ne se passe » (équilibre dynamique). Deux notions du chapitre combinées, document moins guidé.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2023 N (1.2 « montrer que α = 1 − τ », proportion de l'acide), 2019 N
#    (acide benzoïque, mais par conductimétrie : 2.1 à 2.3), 2020 R (2.4 sens d'évolution, 2.5 pH du mélange),
#    2023 N (3.6 ajout d'un réactif à l'équilibre) — backend/data/exams/physique ;
#  - profs (sources_chimie_ch9_ch11.md, chapitre C, § 4-5 : Mahajar et Hadjyne, ajout d'acide pur (pH baisse) ou
#    d'éthanoate de sodium (pH monte), d'où ⇌ ; équilibre dynamique, chocs efficaces, v₁ = v₂, chez Mahajar, Sbiro,
#    Hadjyne) ; pièges : « à l'équilibre la réaction s'arrête », confondre sens direct et inverse quand le pH monte ;
#  - séries en ligne : talamidi (deux sens, non corrigés 1 ; état d'équilibre, activités 1), alloschool (séance 8
#    El Goufifa), moutamadris (cours deux sens 2022, activités 14-1), kezakoo (exercices transformation).
# Ici : nos C, V et pH (calculés pour pKa ≈ 4,20 ; le pH après ajout correspond à 63 mg de benzoate de sodium).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *
from _ch11 import *

C, V, PH, PH2 = 1.0e-2, 0.200, 3.12, 3.60
H, H2 = 10 ** -PH, 10 ** -PH2
TAU = H / C; ALPHA = 1 - TAU
XF = H * V; NAH = C * V - XF
DN = (H - H2) * V
assert abs(TAU - 0.0759) < 1e-4 and abs(ALPHA - 0.924) < 1e-3 and abs(NAH - 1.85e-3) < 1e-5 and abs(DN - 1.01e-4) < 1e-6
# plausibilité de l'ajout (pKa 4,20) : c_b ≈ 2,2e-3 mol/L, soit ≈ 63 mg de C₆H₅COONa (M = 144 g/mol) dans 200 mL
Ka = 10 ** -4.20; cb = Ka / H2 * (C - H2) - H2
assert abs(cb * V * 144 - 0.063) < 0.002 and cb * V > DN

sC, sV, sPH, sPH2 = 5.0e-3, 0.100, 3.27, 3.75
sH, sH2 = 10 ** -sPH, 10 ** -sPH2; sTAU = sH / sC; sALPHA = 1 - sTAU
sNAH = sC * sV - sH * sV; sDN = (sH - sH2) * sV
assert abs(sALPHA - 0.893) < 1e-3 and abs(sNAH - 4.46e-4) < 1e-6 and abs(sDN - 3.59e-5) < 1e-7

EQ = "C₆H₅COOH(aq) + H₂O(l) ⇌ C₆H₅COO⁻(aq) + H₃O⁺(aq)"
EQ_DIT = "l'acide benzoïque، plus H deux O، double flèche، l'ion benzoate، plus H trois O plus"
INV = "C₆H₅COO⁻(aq) + H₃O⁺(aq) → C₆H₅COOH(aq) + H₂O(l)"

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction de l'acide benzoïque avec l'eau. En s'aidant du tableau d'avancement, montrer que α = 1 − τ.",
    "السؤال un: كتب l'équation ديال l'acide benzoïque مع الما. وبمساعدة le tableau d'avancement، بين أن alpha égale un moins tau.",
    phrase(EQ + " ; [C₆H₅COO⁻] = x_f/V = C·τ ; [C₆H₅COOH] = (C·V − x_f)/V = C − C·τ ; α = (C − C·τ)/C = 1 − τ"),
    (["x_f = τ·x_max", "x_max = C·V", "[A⁻] + [AH] = C", "α"], ["α = τ", "[C₆H₅COOH] = C"]),
    [("Exprime x_f avec τ : x_f = τ·x_max = τ·C·V. Puis écris les deux concentrations à l'équilibre à partir du tableau.",
      "عبر على x f ب tau: x f égale tau fois x max، يعني tau fois C fois V. ومن بعد كتب deux concentrations ف l'équilibre من le tableau."),
     ("[C₆H₅COO⁻] = C·τ et [C₆H₅COOH] = C − C·τ ; leur somme vaut C. Remplace dans α.",
      "la concentration ديال l'ion benzoate égale C fois tau، و ديال l'acide égale C moins C fois tau. المجموع égale C. عوض ف alpha.")],
    [(f"1 : {EQ}", "l'équation"),
     ("x_f = τ·x_max = τ·C·V ; [C₆H₅COO⁻] = C·τ ; [C₆H₅COOH] = C − C·τ", "x f égale tau fois C fois V"),
     ("[C₆H₅COOH] + [C₆H₅COO⁻] = C ; α = (C − C·τ)/C = 1 − τ", "إذن alpha égale un moins tau")],
    f"السؤال un. l'équation: {EQ_DIT}. x f égale tau fois x max، يعني x f égale tau fois C fois V. la concentration ديال l'ion benzoate égale C fois tau، و ديال l'acide égale C moins C fois tau، والمجموع égale C. إذن alpha égale un moins tau.",
    "ex_1", "fa_1"),
  Q("2", "Calculer τ, puis α. Commenter.",
    "السؤال deux: حسب tau، ومن بعد alpha. علق.",
    val("α", ALPHA, None, f"τ = 10^(−pH)/C = 10^(−{fr(PH)})/{sci(C, 1)} = {fr(TAU, 3)} ; α = 1 − τ = {fr(ALPHA, 3)}", tol=0.01),
    (["τ = 10^(−pH)/C", "α = 1 − τ"], ["α = τ", f"α = {fr(TAU, 3)}"]),
    [("Commence par τ, avec le pH mesuré.", "بدا ب tau، ب le p H المقاس."),
     ("τ = 10^(−pH)/C, puis α = 1 − τ : presque tout l'acide reste sous forme AH.", "tau égale dix puissance moins p H، sur C، ومن بعد alpha égale un moins tau.")],
    [(f"2 : τ = 10^(−{fr(PH)})/{sci(C, 1)} = {fr(TAU, 3)}", f"يعني {d(TAU, 3)}"),
     (f"α = 1 − τ = {fr(ALPHA, 3)}", f"يعني {d(ALPHA, 3)}"),
     (f"environ {fr(100 * ALPHA, 0)} % de l'acide reste sous forme C₆H₅COOH : la forme acide est majoritaire", "la forme acide")],
    f"السؤال deux. tau égale dix puissance moins {d(PH)}، sur {ds(C, 1)}، يعني {d(TAU, 3)}. alpha égale un moins tau، يعني {d(ALPHA, 3)}. تقريبا {d(100 * ALPHA, 0)} pour cent من l'acide بقا كيف ما هو: la forme acide هي الكثيرة.",
    "ex_2", "fa_2"),
  Q("3", "Déterminer la quantité de matière d'acide benzoïque n(C₆H₅COOH)_éq présente dans la solution à l'équilibre. Que peut-on dire des réactifs et des produits à l'équilibre ?",
    "السؤال trois: حدد la quantité de matière ديال l'acide benzoïque ف l'équilibre. شنو نقولو على les réactifs و les produits ف l'équilibre؟",
    val("n(AH)", NAH, "mol", f"x_f = 10^(−pH)·V = {sci(XF, 2)} mol ; n(C₆H₅COOH)_éq = C·V − x_f = {sci(C * V, 1)} − {sci(XF, 2)} = {sci(NAH, 2)} mol"),
    (["n = C·V − x_f", "x_f = [H₃O⁺]·V", "coexistent"], ["n = C·V", "n = x_f"]),
    [("Dans le tableau, à l'équilibre, l'acide restant vaut C·V − x_f. Commence par x_f.",
      "فle tableau، ف l'équilibre، l'acide اللي بقا égale C V moins x f. بدا ب x f."),
     ("x_f = 10^(−pH)·V ; n(AH)_éq = C·V − x_f ; les produits valent x_f, non nuls.",
      "x f égale dix puissance moins p H fois V. ومن بعد C V moins x f. و les produits عندهم x f، ماشي zéro.")],
    [(f"3 : x_f = 10^(−{fr(PH)}) × {fr(V, 3)} = {sci(XF, 2)} mol", "x f égale dix puissance moins"),
     (f"n(C₆H₅COOH)_éq = C·V − x_f = {sci(NAH, 2)} mol", "C V moins x f"),
     ("réactifs et produits coexistent à l'équilibre : aucun réactif n'est épuisé", "كاينين فنفس الوقت")],
    f"السؤال trois. x f égale dix puissance moins {d(PH)} fois {d(V, 1)}، يعني {ds(XF, 2)} mole. l'acide اللي بقا: C V moins x f، يعني {ds(NAH, 2)} mole. les réactifs و les produits كاينين فنفس الوقت: حتى réactif ما سالا.",
    "ex_3", "fa_3"),
  Q("4", f"On ajoute à la solution, sans changer pratiquement son volume, une petite quantité de benzoate de sodium solide (63 mg). Après agitation, le pH se stabilise à {fr(PH2)}. Dans quel sens le système a-t-il évolué ? Justifier et écrire l'équation correspondante.",
    f"السؤال quatre: كنزيدو شوية ديال le benzoate de sodium، بلا ما يتبدل le volume. le p H كيستقر ف {d(PH2)}. فشمن sens تطور le système؟ علل، وكتب l'équation.",
    phrase(f"pH : {fr(PH)} → {fr(PH2)}, [H₃O⁺] diminue : des ions H₃O⁺ sont consommés par les ions benzoate ajoutés : sens inverse (2) : {INV}"),
    (["[H₃O⁺] diminue", "sens inverse", "C₆H₅COO⁻ + H₃O⁺"], ["sens direct", "le pH augmente donc H₃O⁺ augmente"]),
    [("Si le pH augmente, que devient la concentration des ions H₃O⁺ ? Qui a pu les consommer ?",
      "يلا طلع le p H، شنو كيوقع ل la concentration des ions H trois O plus؟ شكون استهلكهم؟"),
     ("Les ions benzoate ajoutés captent des protons de H₃O⁺ : c'est l'équation écrite de droite à gauche.",
      "les ions benzoate اللي زدنا كيشدو le proton من H trois O plus. هادي هي l'équation من اليمين لليسار.")],
    [(f"4 : le pH passe de {fr(PH)} à {fr(PH2)} : [H₃O⁺] = 10^(−pH) diminue", "le p H طلع"),
     ("des ions H₃O⁺ sont consommés par les ions benzoate ajoutés : le système évolue dans le sens inverse (2)", "le sens inverse"),
     (INV, "l'équation")],
    f"السؤال quatre. le p H طلع من {d(PH)} ل {d(PH2)}، إذن la concentration des ions H trois O plus نقصات. les ions benzoate اللي زدنا خداو منهم le proton: le système تطور ف le sens inverse، le sens deux. l'équation: l'ion benzoate، plus H trois O plus، donne l'acide benzoïque، plus H deux O.",
    "ex_4", "fa_4"),
  Q("5", "Calculer la quantité de matière Δn d'ions H₃O⁺ consommée lors de cette évolution.",
    "السؤال cinq: حسب la quantité ديال les ions H trois O plus اللي تستهلكات.",
    val("Δn", DN, "mol", f"Δn = (10^(−{fr(PH)}) − 10^(−{fr(PH2)}))·V = ({sci(H, 2)} − {sci(H2, 2)}) × {fr(V, 3)} = {sci(DN, 2)} mol"),
    (["n = [H₃O⁺]·V", "Δn = n_avant − n_après", "10^(−pH)"], ["Δn = (pH₂ − pH₁)·V", "Δn = 10^(−(pH₂ − pH₁))·V"]),
    [("Calcule la quantité d'ions H₃O⁺ avant l'ajout, puis après : la différence a été consommée.",
      "حسب la quantité ديال les ions H trois O plus قبل، ومن بعد. الفرق هو اللي تستهلك."),
     ("n = 10^(−pH)·V pour chaque pH ; ne soustrais jamais les pH eux-mêmes.",
      "n égale dix puissance moins p H fois V، لكل p H. وما تنقصش les p H مباشرة.")],
    [(f"5 : avant : n₁ = 10^(−{fr(PH)})·V = {sci(H * V, 2)} mol ; après : n₂ = 10^(−{fr(PH2)})·V = {sci(H2 * V, 2)} mol", "قبل"),
     (f"Δn = n₁ − n₂ = {sci(DN, 2)} mol", f"{ds(DN, 2)} mole")],
    f"السؤال cinq. قبل: dix puissance moins {d(PH)} fois V، يعني {ds(H * V, 2)} mole. من بعد: dix puissance moins {d(PH2)} fois V، يعني {ds(H2 * V, 2)} mole. الفرق: {ds(DN, 2)} mole ديال les ions H trois O plus تستهلكات.",
    "ex_5", "fa_5"),
  Q("6", "Une fois le pH de nouveau stable, un élève affirme : « maintenant, plus aucune réaction ne se produit dans le bécher ». Discuter cette affirmation à l'échelle des entités.",
    "السؤال six: ملي le p H رجع ثابت، تلميذ قال: « دابا حتى réaction ما بقات كتوقع فle bécher ». ناقش هاد الكلام على مستوى les entités.",
    phrase("Faux : l'équilibre est dynamique ; les réactions dans le sens direct et dans le sens inverse continuent avec la même vitesse (v₁ = v₂, autant de chocs efficaces dans chaque sens), donc les quantités ne changent plus"),
    (["équilibre dynamique", "v₁ = v₂", "chocs efficaces", "deux sens"], ["la réaction s'arrête", "v₁ = v₂ = 0"]),
    [("À l'échelle macroscopique rien ne change ; regarde à la loupe : les deux sens de la réaction existent-ils encore ?",
      "من برا ما كيتبدل والو. ولكن ب la loupe: واش deux sens باقين كيوقعو؟"),
     ("Les deux réactions inverses se font en même temps, au même rythme : ce qui se forme dans un sens disparaît dans l'autre.",
      "deux réactions كيوقعو فنفس الوقت، بنفس la vitesse: اللي كيتكون فاتجاه، كيمشي فالاتجاه الآخر.")],
    [("6 : affirmation fausse : l'équilibre est dynamique", "l'équilibre dynamique"),
     ("les réactions dans les deux sens continuent, avec v₁ = v₂ (autant de chocs efficaces dans chaque sens)", "v un égale v deux"),
     ("les quantités de matière ne changent plus, mais les entités continuent de réagir", "les quantités")],
    "السؤال six. هاد الكلام غالط: l'équilibre dynamique. deux réactions، le sens direct و le sens inverse، باقين كيوقعو فنفس الوقت، و v un égale v deux: نفس العدد ديال chocs efficaces ف كل sens. إذن les quantités ما كيتبدلوش، ولكن les entités باقين كيتفاعلو.",
    "ex_6", "fa_6"),
]

EXPLICATIONS = [
  sl_proportion("ex_1", "Question 1 : montrer que α = 1 − τ",
    "نفس الخطوات مع l'acide benzoïque: C fois tau ديال l'ion benzoate، و C moins C fois tau ديال l'acide. إذن alpha égale un moins tau.",
    [("[C₆H₅COO⁻] = C·τ ; [C₆H₅COOH] = C − C·τ", "نفس الخطوات مع l'acide benzoïque"), ("α = 1 − τ", "إذن alpha égale un moins tau.")]),
  sl_taux("ex_2", "Question 2 : τ puis α",
    f"tau égale dix puissance moins {d(PH)}، sur {ds(C, 1)}، يعني {d(TAU, 3)}. و alpha égale un moins tau، يعني {d(ALPHA, 3)}: la forme acide هي الكثيرة.",
    [(f"τ = {fr(TAU, 3)}", f"يعني {d(TAU, 3)}"), (f"α = 1 − τ = {fr(ALPHA, 3)}", f"يعني {d(ALPHA, 3)}")]),
  sl_etat("ex_3", "Question 3 : la composition à l'équilibre",
    f"x f égale {ds(XF, 2)} mole، و l'acide اللي بقا {ds(NAH, 2)} mole. les réactifs و les produits كاينين فنفس الوقت.",
    [(f"n(C₆H₅COOH)_éq = C·V − x_f = {sci(NAH, 2)} mol", f"و l'acide اللي بقا {ds(NAH, 2)} mole")]),
  sl_inverse("ex_4", "Question 4 : on ajoute la base conjuguée",
    f"زدنا le benzoate de sodium، و le p H طلع من {d(PH)} ل {d(PH2)}. les ions benzoate خداو le proton من H trois O plus: le sens inverse.",
    [(INV, "les ions benzoate خداو le proton"), ("sens inverse (2)", "le sens inverse.")]),
  sl_ph("ex_5", "Question 5 : les ions H₃O⁺ consommés",
    f"قبل: {ds(H, 2)} mole par litre، ومن بعد: {ds(H2, 2)} mole par litre. الفرق fois V، يعني {ds(DN, 2)} mole.",
    [(f"Δn = ({sci(H, 2)} − {sci(H2, 2)}) × {fr(V, 3)}", f"قبل: {ds(H, 2)} mole par litre"), (f"Δn = {sci(DN, 2)} mol", f"يعني {ds(DN, 2)} mole")]),
  sl_dynamique("ex_6", "Question 6 : l'équilibre est dynamique",
    "ملي le p H رجع ثابت، deux sens باقين كيوقعو بنفس la vitesse. إذن الكلام ديال التلميذ غالط.",
    [("v₁ = v₂ ≠ 0 : équilibre dynamique", "deux sens باقين كيوقعو")]),
]

FACILES = [
  vf("fa_1", "Plus facile : vrai ou faux", "α est la proportion de l'acide restant à l'équilibre.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("[C₆H₅COO⁻]_éq = C·τ.", True, "x_f = τ·C·V, et la concentration est x_f/V."),
      ("[C₆H₅COOH]_éq + [C₆H₅COO⁻]_éq = C.", True, "L'acide perdu se retrouve en base conjuguée : la somme reste C."),
      ("α = τ.", False, "α est la part qui n'a PAS réagi : α = 1 − τ.")]),
  qcm("fa_2", "Plus facile : α", "سؤال ساهل على alpha.",
      f"τ = {fr(TAU, 3)}. La proportion α de la forme acide vaut…",
      [f"{fr(TAU, 3)}", f"{fr(ALPHA, 3)}", f"{fr(1 + TAU, 3)}"], 1, {
        1: ("juste", f"برافو! alpha égale un moins tau، يعني {d(ALPHA, 3)}.", f"Juste : α = 1 − τ = {fr(ALPHA, 3)}."),
        0: (("لا، هادي tau، الجزء اللي تفاعل. alpha هي اللي بقا. عاود اختار.", "C'est τ, la part qui a réagi ; α est la part restante. Réessaie."),
            (f"الجواب: {d(ALPHA, 3)}، alpha égale un moins tau.", f"Réponse : α = 1 − τ = {fr(ALPHA, 3)}.")),
        2: (("لا، proportion ما تفوتش un. عاود اختار.", "Une proportion ne dépasse pas 1. Réessaie."),
            (f"الجواب: {d(ALPHA, 3)}: un moins tau، ماشي un plus tau.", f"Réponse : α = 1 − τ = {fr(ALPHA, 3)}."))},
      f"Tau égale {d(TAU, 3)}. La proportion alpha de la forme acide vaut ?"),
  qcm("fa_3", "Plus facile : l'acide restant", "سؤال ساهل على l'acide اللي بقا.",
      f"C·V = {sci(C * V, 1)} mol et x_f = {sci(XF, 2)} mol. n(C₆H₅COOH)_éq vaut…",
      [f"{sci(C * V, 1)} mol", f"{sci(XF, 2)} mol", f"{sci(NAH, 2)} mol"], 2, {
        2: ("juste", f"برافو! C V moins x f، يعني {ds(NAH, 2)} mole.", f"Juste : n = C·V − x_f = {sci(NAH, 2)} mol."),
        0: (("لا، هادي الكمية اللي فالبداية. شوية تفاعل. عاود اختار.", "C'est la quantité initiale : une partie a réagi. Réessaie."),
            (f"الجواب: {ds(NAH, 2)} mole، C V moins x f.", f"Réponse : C·V − x_f = {sci(NAH, 2)} mol.")),
        1: (("لا، x f هي ديال les produits. l'acide اللي بقا هو C V moins x f. عاود اختار.", "x_f, c'est la quantité de chaque produit. Réessaie."),
            (f"الجواب: {ds(NAH, 2)} mole.", f"Réponse : {sci(NAH, 2)} mol."))},
      f"C V égale {ds(C * V, 1)} mole et x f égale {ds(XF, 2)} mole. La quantité d'acide restant vaut ?"),
  qcm("fa_4", "Plus facile : le sens d'évolution", "سؤال ساهل: فشمن sens تطور le système؟",
      f"Après l'ajout de benzoate de sodium, le pH passe de {fr(PH)} à {fr(PH2)}. Le système a évolué…",
      ["dans le sens direct : il s'est formé des ions H₃O⁺", "dans le sens inverse : des ions H₃O⁺ ont été consommés", "il n'a pas évolué"], 1, {
        1: ("juste", "برافو! le p H طلع، إذن les ions H trois O plus نقصو: le sens inverse.", "Juste : pH ↑ → [H₃O⁺] ↓ → sens inverse."),
        0: (("لا، يلا تكونو ions H trois O plus، le p H كينقص. هنا طلع. عاود اختار.", "Plus d'ions H₃O⁺ ferait baisser le pH. Réessaie."),
            ("الجواب: le sens inverse. le p H طلع، إذن H trois O plus تستهلكو.", "Réponse : sens inverse, les ions H₃O⁺ ont été consommés.")),
        2: (("لا، le p H تبدل، إذن la composition تبدلات. عاود اختار.", "Le pH a changé : la composition aussi. Réessaie."),
            ("الجواب: le sens inverse.", "Réponse : sens inverse."))},
      f"Après l'ajout, le p H passe de {d(PH)} à {d(PH2)}. Le système a évolué ?"),
  qcm("fa_5", "Plus facile : ce qui a été consommé", "سؤال ساهل: كيفاش نحسبو الفرق؟",
      "Pour trouver la quantité d'ions H₃O⁺ consommée, on calcule…",
      ["(pH₂ − pH₁)·V", "(10^(−pH₁) − 10^(−pH₂))·V", "10^(−pH₂)·V"], 1, {
        1: ("juste", "برافو! la quantité قبل، ناقص la quantité من بعد.", "Juste : n₁ − n₂, chacune = 10^(−pH)·V."),
        0: (("لا، le p H ماشي quantité. خاصك تمر ب dix puissance moins p H. عاود اختار.", "Le pH n'est pas une quantité : passe par 10^(−pH). Réessaie."),
            ("الجواب: dix puissance moins p H un، ناقص dix puissance moins p H deux، fois V.", "Réponse : Δn = (10^(−pH₁) − 10^(−pH₂))·V.")),
        2: (("هادي غير الكمية اللي بقات من بعد، ماشي اللي تستهلكات. عاود اختار.", "C'est la quantité restante, pas la quantité consommée. Réessaie."),
            ("الجواب: الفرق بين قبل ومن بعد.", "Réponse : la différence avant − après."))},
      "Pour trouver la quantité d'ions H trois O plus consommée, on calcule ?"),
  assoc("fa_6", "Plus facile : l'équilibre dynamique", "Relie chaque affirmation à ce qui se passe à l'équilibre.",
    "سؤال ساهل: ربط كل جملة مع اللي كيوقع ف l'équilibre.",
    "À l'équilibre, relie chaque grandeur à sa description.",
    [("1", "Les quantités de matière"), ("2", "Les réactions dans les deux sens"), ("3", "Les vitesses v₁ et v₂")],
    [("a", "ne changent plus"), ("b", "continuent en même temps"), ("c", "sont égales, et non nulles"), ("d", "sont toutes les deux nulles")],
    {"1": "a", "2": "b", "3": "c"},
    {"1-a": (True, "Oui : le pH et les quantités restent constants.", "برافو: le p H و les quantités ثابتين."),
     "1-*": (False, "Regarde le pH-mètre : la valeur ne bouge plus.", "لا، شوف le p H mètre: الرقم ما بقاش كيتحرك."),
     "2-b": (True, "Oui : les entités réagissent toujours, dans les deux sens.", "برافو: les entités باقين كيتفاعلو ف deux sens."),
     "2-*": (False, "À la loupe, les échanges de protons continuent.", "لا، ب la loupe، le proton باقي كيدوز."),
     "3-c": (True, "Oui : autant de réactions dans un sens que dans l'autre.", "برافو: نفس العدد ف كل sens."),
     "3-d": (False, "Si les vitesses étaient nulles, rien ne réagirait plus : ce n'est pas un équilibre dynamique.", "لا، يلا كانو zéro، حتى حاجة ما تتفاعل، وهادا ماشي l'équilibre dynamique."),
     "3-*": (False, "Compare les deux vitesses : l'une ne l'emporte pas sur l'autre.", "لا، قارن deux vitesses: حتى وحدة ما كتغلب الأخرى.")},
    ("(1 ; a) (2 ; b) (3 ; c) : l'équilibre est dynamique.", "l'équilibre dynamique: les quantités ثابتين، و deux sens كيوقعو بنفس la vitesse.")),
]

SIM_Q = [
  QS("1", "Écrire l'équation de la réaction de l'acide benzoïque avec l'eau et montrer que α = 1 − τ.",
     phrase(EQ + " ; α = (C − C·τ)/C = 1 − τ"), (["x_f = τ·C·V", "α"], ["α = τ"]),
     [(EQ, "l'équation"), ("α = (C − C·τ)/C = 1 − τ", "alpha égale un moins tau")],
     f"l'équation: {EQ_DIT}. la base égale C fois tau، و l'acide C moins C fois tau. إذن alpha égale un moins tau."),
  QS("2", "Calculer τ, puis α.",
     val("α", sALPHA, None, f"τ = 10^(−{fr(sPH)})/{sci(sC, 1)} = {fr(sTAU, 3)} ; α = 1 − τ = {fr(sALPHA, 3)}", tol=0.01),
     (["α = 1 − τ"], ["α = τ"]),
     [(f"τ = {fr(sTAU, 3)} ; α = {fr(sALPHA, 3)}", f"alpha égale {d(sALPHA, 3)}")],
     f"tau égale {d(sTAU, 3)}، و alpha égale {d(sALPHA, 3)}."),
  QS("3", "Déterminer n(C₆H₅COOH)_éq. Que dire des réactifs et des produits ?",
     val("n(AH)", sNAH, "mol", f"n = C·V − 10^(−pH)·V = {sci(sC * sV, 1)} − {sci(sH * sV, 2)} = {sci(sNAH, 2)} mol"),
     (["C·V − x_f"], ["C·V"]),
     [(f"n(C₆H₅COOH)_éq = {sci(sNAH, 2)} mol ; réactifs et produits coexistent", f"{ds(sNAH, 2)} mole")],
     f"C V moins x f، يعني {ds(sNAH, 2)} mole. les réactifs و les produits كاينين فنفس الوقت."),
  QS("4", f"Après ajout de benzoate de sodium, pH = {fr(sPH2)}. Sens d'évolution ? Équation ?",
     phrase(f"[H₃O⁺] diminue : sens inverse ; {INV}"), (["sens inverse"], ["sens direct"]),
     [(f"pH ↑ : H₃O⁺ consommés, sens inverse : {INV}", "le sens inverse")],
     "le p H طلع، les ions H trois O plus تستهلكو: le sens inverse."),
  QS("5", "Calculer Δn(H₃O⁺) consommée.",
     val("Δn", sDN, "mol", f"Δn = ({sci(sH, 2)} − {sci(sH2, 2)}) × {fr(sV, 3)} = {sci(sDN, 2)} mol"),
     (["10^(−pH)·V"], ["(pH₂ − pH₁)·V"]),
     [(f"Δn = {sci(sDN, 2)} mol", f"{ds(sDN, 2)} mole")],
     f"الفرق بين قبل ومن بعد، fois V: {ds(sDN, 2)} mole."),
  QS("6", "« Plus aucune réaction ne se produit » : discuter.",
     phrase("Faux : équilibre dynamique, les deux sens continuent avec v₁ = v₂"), (["v₁ = v₂"], ["la réaction s'arrête"]),
     [("Faux : équilibre dynamique, v₁ = v₂", "l'équilibre dynamique")],
     "غالط: l'équilibre dynamique، deux sens باقين، و v un égale v deux."),
]

EX = exercice(
  "phys_ex_ch11_deux_sens_6", "phys_ch11_transformations_deux_sens", "transformations_deux_sens",
  "L'acide benzoïque à l'équilibre : α = 1 − τ, puis on ajoute sa base conjuguée", "difficile", 35,
  ["Montrer que α = 1 − τ", "Déterminer la composition à l'équilibre", "Reconnaître le sens inverse quand le pH monte",
   "Calculer une quantité d'ions H₃O⁺ consommée", "Expliquer l'équilibre dynamique (v₁ = v₂)"],
  f"L'acide benzoïque C₆H₅COOH est un conservateur alimentaire (E210). On prépare V = {fr(V * 1000, 0)} mL d'une solution S d'acide benzoïque de concentration C = {sci(C, 1)} mol/L. À 25 °C, le pH de S, une fois stable, vaut {fr(PH)}. On définit la proportion de la forme acide à l'équilibre : α = [C₆H₅COOH]_éq/([C₆H₅COOH]_éq + [C₆H₅COO⁻]_éq).",
  f"دابا نقراو l'énoncé. l'acide benzoïque كيتستعمل باش يحفظ الماكلة. عندنا {d(V * 1000, 0)} millilitres ديال المحلول S، C égale {ds(C, 1)} mole par litre، و le p H ديالو، ملي كيستقر، {d(PH)}. alpha هي la proportion ديال la forme acide ف l'équilibre: la concentration ديال l'acide، sur la somme des deux concentrations.",
  [],
  [f"V = {fr(V * 1000, 0)} mL ; C = {sci(C, 1)} mol/L", f"pH = {fr(PH)} (25 °C)", f"pH après l'ajout : {fr(PH2)} (questions 4 et 5)",
   "Couple : C₆H₅COOH(aq) / C₆H₅COO⁻(aq)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  f"V = {fr(sV * 1000, 0)} mL de solution d'acide benzoïque, C = {sci(sC, 1)} mol/L, pH = {fr(sPH)} à 25 °C. Après ajout d'un peu de benzoate de sodium (volume inchangé), le pH se stabilise à {fr(sPH2)}.",
  f"نفس التمرين، بقيم أخرى. {d(sV * 1000, 0)} millilitres، C égale {ds(sC, 1)} mole par litre، p H égale {d(sPH)}، ومن بعد l'ajout، {d(sPH2)}.",
  [], [f"V = {fr(sV * 1000, 0)} mL ; C = {sci(sC, 1)} mol/L", f"pH = {fr(sPH)} ; après ajout : {fr(sPH2)}"],
  SIM_Q)

ecrire(EX)
