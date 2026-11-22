# Exercice de chimie, ch. 11 (transformations dans les deux sens), niveau moyen (celui du national) : dilutions
# successives d'un même acide ; le volume à prélever, « montrer que τ = 10^(−pH)/C », τ des trois solutions lu sur
# un tableau de mesures, puis l'influence de la dilution sur τ (« lire puis déduire »).
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2021 R (Q9 « montrer que τ = 10^(−pH)/C », Q10 tableau à compléter, Q11
#    « en déduire l'effet de la dilution sur τ »), 2025 R (dilution et τ), 2022 N (2.4 solution diluée 10 fois)
#    — backend/data/exams/physique ;
#  - profs : aucun ne traite la dilution dans ce chapitre (sources_chimie_ch9_ch11.md, chapitre C, § 7 ; Sbiro la
#    place à l'état d'équilibre : « plus la solution est diluée, plus τ est grand ») ; cadre TD7 ; pièges : croire que
#    le pH baisse quand on dilue un acide, V₀ = C₀V₁/C₁ (relation retournée), conclure sur [H₃O⁺] au lieu de τ ;
#  - séries en ligne : talamidi (état d'équilibre, activités 1 ; deux sens, non corrigés 1), alloschool (séance 8),
#    moutamadris (cours deux sens 2022), kezakoo (exercices transformation), coursdusoirpc (TD 2 BAC BIOF).
# Ici : l'acide butanoïque, nos concentrations et nos pH (calculés pour pKa ≈ 4,82, arrondis comme des mesures).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *
from _ch11 import *

C0, V1 = 2.0e-2, 100.0e-3
CS = [C0, C0 / 10, C0 / 100]
PHS = [3.27, 3.78, 4.32]
TAUS = [10 ** -p / c for p, c in zip(PHS, CS)]
V0 = CS[1] * V1 / C0                       # 10,0 mL
assert abs(V0 - 10.0e-3) < 1e-12
assert [round(t, 3) for t in TAUS] == [0.027, 0.083, 0.239]

sC0, sV1 = 5.0e-2, 50.0e-3
sCS = [sC0, sC0 / 10, sC0 / 100]; sPHS = [2.54, 3.07, 3.65]
sTAUS = [10 ** -p / c for p, c in zip(sPHS, sCS)]; sV0 = sCS[1] * sV1 / sC0
assert abs(sV0 - 5.0e-3) < 1e-12 and [round(t, 3) for t in sTAUS] == [0.058, 0.170, 0.448]

NOMS = ["S₀", "S₁", "S₂"]
def tab(cs, phs, titre="Mesures à 25 °C"):
    return tableau_texte(titre, ["Solution", "C (mol/L)", "pH", "τ"],
                         [[n, sci(c, 1), fr(p), "?"] for n, c, p in zip(NOMS, cs, phs)])

def sl_mesures(sid, titre, app, centre):
    return sim(sid, titre, "Diluer un acide : le pH monte.", T + "dilution.html?vue=mesures", "Une dilution et le pH-mètre",
        "le bécher اللول: l'acide éthanoïque، zéro virgule zéro un mole par litre، و le p H égale trois virgule quatre. دابا نديرو la dilution: dix millilitres ف une fiole de cent millilitres. المحلول ولا dilué dix fois. le bécher الثاني: le p H égale trois virgule neuf. le p H طلع. فالتمرين ديالنا: " + app,
        centre, [("le bécher اللول", "moment:solution_1"), ("دابا نديرو la dilution", "moment:dilution_1"), ("le bécher الثاني", "moment:solution_2")])

QUESTIONS = [
  Q("1", f"Calculer le volume V₀ de S₀ qu'il faut prélever pour préparer V₁ = {fr(V1 * 1000, 1)} mL de S₁.",
    f"السؤال un: حسب le volume V zéro اللي خاصنا ناخدو من S zéro، باش نوجدو {d(V1 * 1000, 1)} millilitres ديال S un.",
    val("V₀", V0 * 1000, "mL", f"C₀·V₀ = C₁·V₁ donc V₀ = C₁·V₁/C₀ = {sci(CS[1], 1)} × {fr(V1 * 1000, 1)}/{sci(C0, 1)} = {fr(V0 * 1000, 1)} mL"),
    (["C₀·V₀ = C₁·V₁", "V₀ = C₁·V₁/C₀", "mL"], ["V₀ = C₀·V₁/C₁", "V₀ = 1000 mL"]),
    [("Quand on dilue, on ajoute de l'eau, mais la quantité d'acide prélevée ne change pas.",
      "ملي كنزيدو الما، la quantité ديال l'acide اللي خدينا كتبقى هي هي."),
     ("n prélevé = n dans la fiole : C₀·V₀ = C₁·V₁, donc V₀ = C₁·V₁/C₀.",
      "C zéro fois V zéro égale C un fois V un. إذن V zéro égale C un fois V un، sur C zéro.")],
    [("1 : la quantité d'acide se conserve : C₀·V₀ = C₁·V₁", "C zéro fois V zéro égale C un fois V un"),
     (f"V₀ = C₁·V₁/C₀ = {sci(CS[1], 1)} × {fr(V1 * 1000, 1)}/{sci(C0, 1)}", "V zéro égale C un fois V un، sur C zéro"),
     (f"V₀ = {fr(V0 * 1000, 1)} mL", f"V zéro égale {d(V0 * 1000, 1)} millilitres")],
    f"السؤال un. la quantité ديال l'acide كتبقى هي هي: C zéro fois V zéro égale C un fois V un. إذن V zéro égale C un fois V un، sur C zéro، يعني {ds(CS[1], 1)} fois {d(V1 * 1000, 0)}، sur {ds(C0, 1)}. V zéro égale {d(V0 * 1000, 1)} millilitres.",
    "ex_1", "fa_1"),
  Q("2", "En s'aidant du tableau d'avancement de la réaction de l'acide avec l'eau, montrer que τ = 10^(−pH)/C.",
    "السؤال deux: بمساعدة le tableau d'avancement، بين أن tau égale dix puissance moins p H، sur C.",
    phrase("τ = x_f/x_max ; x_f = [H₃O⁺]·V = 10^(−pH)·V ; x_max = C·V ; τ = 10^(−pH)/C"),
    (["τ = x_f/x_max", "x_f = 10^(−pH)·V", "x_max = C·V"], ["x_f = C·V", "τ = C/10^(−pH)"]),
    [("Pars de la définition de τ et remplace x_f et x_max à l'aide du tableau.",
      "بدا من la définition ديال tau، وبدل x f و x max ب le tableau."),
     ("x_f = n(H₃O⁺)_f = 10^(−pH)·V ; x_max = C·V (l'eau est en excès) ; V se simplifie.",
      "x f égale dix puissance moins p H fois V، و x max égale C fois V. V كيتحيد.")],
    [("2 : τ = x_f/x_max", "tau égale x f sur x max"),
     ("x_f = [H₃O⁺]·V = 10^(−pH)·V ; x_max = C·V", "x f égale dix puissance moins p H fois V"),
     ("τ = 10^(−pH)/C", "V كيتحيد")],
    "السؤال deux. tau égale x f sur x max. x f égale dix puissance moins p H fois V، و x max égale C fois V. V كيتحيد، وكيبقى tau égale dix puissance moins p H، sur C.",
    "ex_2", "fa_2"),
  Q("3", "Calculer le taux d'avancement final τ₀ dans la solution S₀.",
    "السؤال trois: حسب tau zéro ف المحلول S zéro.",
    val("τ₀", TAUS[0], None, f"τ₀ = 10^(−{fr(PHS[0])})/{sci(C0, 1)} = {fr(TAUS[0], 3)}"),
    (["τ = 10^(−pH)/C", "C₀"], ["τ = 10^(pH)/C", "τ = pH/C"]),
    [("Lis dans le tableau le pH et la concentration de S₀.", "قرا فle tableau le p H و la concentration ديال S zéro."),
     ("τ₀ = 10^(−pH₀)/C₀ : n'oublie pas le signe moins.", "tau zéro égale dix puissance moins p H zéro، sur C zéro. ما تنساش le signe moins.")],
    [(f"3 : τ₀ = 10^(−pH₀)/C₀ = 10^(−{fr(PHS[0])})/{sci(C0, 1)}", "tau zéro égale dix puissance moins"),
     (f"τ₀ = {fr(TAUS[0], 3)}", f"tau zéro égale {d(TAUS[0], 3)}")],
    f"السؤال trois. tau zéro égale dix puissance moins {d(PHS[0])}، sur {ds(C0, 1)}. tau zéro égale {d(TAUS[0], 3)}.",
    "ex_3", "fa_3"),
  Q("4", "Calculer de même τ₁ et τ₂, et recopier le tableau complété.",
    "السؤال quatre: حسب بنفس الطريقة tau un و tau deux، وكمل le tableau.",
    val("τ₂", TAUS[2], None, f"τ₁ = 10^(−{fr(PHS[1])})/{sci(CS[1], 1)} = {fr(TAUS[1], 3)} ; τ₂ = 10^(−{fr(PHS[2])})/{sci(CS[2], 1)} = {fr(TAUS[2], 2)}"),
    (["τ = 10^(−pH)/C", "C₁", "C₂"], ["τ₂ = τ₀/100", "τ₂ = 10 τ₁"]),
    [("Même relation, avec le pH et la concentration de chaque solution.", "نفس la relation، مع le p H و la concentration ديال كل محلول."),
     ("Attention : C₁ = C₀/10 et C₂ = C₀/100 ; τ n'est pas divisé par 10.", "رد البال: C un égale C zéro sur dix، و C deux égale C zéro sur cent. tau ما كيتقسمش على dix.")],
    [(f"4 : τ₁ = 10^(−{fr(PHS[1])})/{sci(CS[1], 1)} = {fr(TAUS[1], 3)}", f"tau un égale {d(TAUS[1], 3)}"),
     (f"τ₂ = 10^(−{fr(PHS[2])})/{sci(CS[2], 1)} = {fr(TAUS[2], 2)}", f"tau deux égale {d(TAUS[2], 2)}"),
     (f"tableau : τ₀ = {fr(TAUS[0], 3)} ; τ₁ = {fr(TAUS[1], 3)} ; τ₂ = {fr(TAUS[2], 2)}", "le tableau")],
    f"السؤال quatre. tau un égale dix puissance moins {d(PHS[1])}، sur {ds(CS[1], 1)}: tau un égale {d(TAUS[1], 3)}. tau deux égale dix puissance moins {d(PHS[2])}، sur {ds(CS[2], 1)}: tau deux égale {d(TAUS[2], 2)}. وكنكتبوهم فle tableau.",
    "ex_4", "fa_4"),
  Q("5", "En exploitant le tableau, préciser comment varient le pH et τ quand on dilue la solution. En déduire l'influence de la dilution sur le taux d'avancement final.",
    "السؤال cinq: من le tableau، قول كيفاش كيتبدلو le p H و tau ملي كنزيدو الما. استنتج l'influence ديال la dilution على tau.",
    phrase("Quand C diminue, le pH augmente (moins d'ions H₃O⁺ par litre) et τ augmente : plus la solution est diluée, plus τ est grand"),
    (["pH augmente", "τ augmente", "plus la solution est diluée"], ["le pH diminue", "τ ne dépend pas de C"]),
    [("Lis la colonne du pH puis celle de τ, de S₀ à S₂ : dans quel sens va chacune ?",
      "قرا la colonne ديال le p H، ومن بعد ديال tau، من S zéro حتى ل S deux. فين كتمشي كل وحدة؟"),
     ("Le pH monte, mais τ monte aussi : il y a moins d'ions H₃O⁺ par litre, pourtant une plus grande part de l'acide a réagi.",
      "le p H كيطلع، و tau حتى هو كيطلع: قل ديال les ions H trois O plus ف كل litre، ولكن جزء كبر من l'acide تفاعل.")],
    [(f"5 : de S₀ à S₂, le pH augmente ({fr(PHS[0])} → {fr(PHS[2])}) : moins d'ions H₃O⁺ par litre", "le p H كيطلع"),
     (f"τ augmente ({fr(TAUS[0], 3)} → {fr(TAUS[2], 2)})", "و tau كيطلع"),
     ("plus la solution est diluée, plus le taux d'avancement final est grand", "plus la solution est diluée")],
    f"السؤال cinq. من S zéro حتى ل S deux، le p H كيطلع، من {d(PHS[0])} ل {d(PHS[2])}: قل ديال les ions H trois O plus ف كل litre. و tau كيطلع، من {d(TAUS[0], 3)} ل {d(TAUS[2], 2)}. إذن، plus la solution est diluée، plus le taux d'avancement final est grand.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sl_dilution("ex_1", "Question 1 : le volume à prélever",
    f"C un égale C zéro sur dix، إذن V zéro égale C un fois V un، sur C zéro، يعني {d(V0 * 1000, 1)} millilitres. ب la pipette، كناخدو {d(V0 * 1000, 0)} millilitres ونكملو حتى {d(V1 * 1000, 0)} millilitres.",
    [("V₀ = C₁·V₁/C₀", "إذن V zéro égale C un fois V un"), (f"V₀ = {fr(V0 * 1000, 1)} mL", f"يعني {d(V0 * 1000, 1)} millilitres")]),
  sl_relation("ex_2", "Question 2 : montrer que τ = 10^(−pH)/C",
    "نفس الكتابة بالضبط، وهي صحيحة ل S zéro و S un و S deux.",
    [("τ = 10^(−pH)/C", "نفس الكتابة بالضبط")]),
  sl_ph("ex_3", "Question 3 : τ₀",
    f"le p H ديال S zéro {d(PHS[0])}: la concentration égale dix puissance moins {d(PHS[0])}. على C zéro، كتعطي tau zéro égale {d(TAUS[0], 3)}.",
    [(f"τ₀ = 10^(−{fr(PHS[0])})/{sci(C0, 1)}", f"le p H ديال S zéro {d(PHS[0])}"), (f"τ₀ = {fr(TAUS[0], 3)}", f"tau zéro égale {d(TAUS[0], 3)}")]),
  sl_diluer("ex_4", "Question 4 : τ₁ et τ₂, le tableau complété",
    f"tau zéro égale {d(TAUS[0], 3)}، tau un égale {d(TAUS[1], 3)}، و tau deux égale {d(TAUS[2], 2)}. حتى هنا الأعمدة كيطلعو.",
    [(f"τ₁ = {fr(TAUS[1], 3)}", f"tau un égale {d(TAUS[1], 3)}"), (f"τ₂ = {fr(TAUS[2], 2)}", f"و tau deux égale {d(TAUS[2], 2)}")]),
  sl_mesures("ex_5", "Question 5 : l'influence de la dilution",
    f"le p H طلع من {d(PHS[0])} ل {d(PHS[2])}، و tau طلع من {d(TAUS[0], 3)} ل {d(TAUS[2], 2)}. إذن plus la solution est diluée، plus tau est grand.",
    [("pH ↑ et τ ↑ quand on dilue", f"le p H طلع من {d(PHS[0])}"), ("plus la solution est diluée, plus τ est grand", "إذن plus la solution est diluée")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : le volume à prélever", "سؤال ساهل: شحال ناخدو ب la pipette؟",
      f"Pour préparer {fr(V1 * 1000, 0)} mL de S₁, dix fois moins concentrée que S₀, on prélève…",
      [f"{fr(V1 * 1000 * 10, 0)} mL de S₀", f"{fr(V1 * 1000 / 2, 0)} mL de S₀", f"{fr(V0 * 1000, 1)} mL de S₀"], 2, {
        2: ("juste", f"برافو! V zéro égale C un fois V un، sur C zéro: {d(V0 * 1000, 0)} millilitres.", f"Juste : V₀ = V₁/10 = {fr(V0 * 1000, 1)} mL."),
        0: (("لا، قلبتي la relation. باش المحلول يولي فاتح، كناخدو شوية ونزيدو الما. عاود اختار.", "Relation retournée : on prélève peu et on complète. Réessaie."),
            (f"الجواب: {d(V0 * 1000, 0)} millilitres. V zéro égale C un fois V un، sur C zéro.", f"Réponse : V₀ = C₁·V₁/C₀ = {fr(V0 * 1000, 1)} mL.")),
        1: (("لا، النص كيعطي dilué deux fois، ماشي dix fois. عاود اختار.", "La moitié donne une dilution par 2, pas par 10. Réessaie."),
            (f"الجواب: {d(V0 * 1000, 0)} millilitres: dilué dix fois، إذن V un sur dix.", f"Réponse : {fr(V0 * 1000, 1)} mL (dilution par 10)."))},
      f"Pour préparer {d(V1 * 1000, 0)} millilitres de S un, dix fois moins concentrée, on prélève ?"),
  vf("fa_2", "Plus facile : la démonstration", "τ = 10^(−pH)/C", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("x_max = C·V, car l'acide serait épuisé si la réaction était totale.", True, "L'eau est en excès : l'acide est le réactif limitant."),
      ("x_f = 10^(−pH)·V, lu dans la colonne de H₃O⁺.", True, "n(H₃O⁺)_f = x_f = [H₃O⁺]·V."),
      ("τ = C/10^(−pH).", False, "La fraction est retournée : τ = 10^(−pH)/C ≤ 1.")]),
  qcm("fa_3", "Plus facile : τ₀", "سؤال ساهل على tau zéro.",
      f"pH₀ = {fr(PHS[0])} et C₀ = {sci(C0, 1)} mol/L. τ₀ vaut…",
      [f"{fr(TAUS[0], 3)}", f"{fr(PHS[0] / C0, 0)}", f"{sci(10 ** PHS[0] / C0, 1)}"], 0, {
        0: ("juste", f"برافو! tau zéro égale dix puissance moins p H، sur C، يعني {d(TAUS[0], 3)}.", f"Juste : τ₀ = {fr(TAUS[0], 3)}."),
        1: (("لا، قسمتي le p H مباشرة. خاصك dix puissance moins p H. عاود اختار.", "On divise 10^(−pH), pas le pH. Réessaie."),
            (f"الجواب: {d(TAUS[0], 3)}.", f"Réponse : τ₀ = 10^(−pH₀)/C₀ = {fr(TAUS[0], 3)}.")),
        2: (("نسيتي le signe moins: tau ما يمكنش يكون كبير بحال هكا. عاود اختار.", "Le signe moins est oublié : τ ≤ 1. Réessaie."),
            (f"الجواب: {d(TAUS[0], 3)}، مع le signe moins.", f"Réponse : τ₀ = {fr(TAUS[0], 3)}."))},
      f"p H zéro égale {d(PHS[0])} et C zéro égale {ds(C0, 1)} mole par litre. Tau zéro vaut ?"),
  qcm("fa_4", "Plus facile : τ₂", "سؤال ساهل على tau deux.",
      f"pH₂ = {fr(PHS[2])} et C₂ = {sci(CS[2], 1)} mol/L. τ₂ vaut environ…",
      [f"{fr(TAUS[0] / 100, 5)}", f"{fr(TAUS[2], 2)}", "1"], 1, {
        1: ("juste", f"برافو! tau deux égale {d(TAUS[2], 2)}: كبر من tau zéro.", f"Juste : τ₂ = {fr(TAUS[2], 2)}."),
        0: (("لا، tau ما كيتقسمش مع C. حسب ب le p H ديال S deux. عاود اختار.", "τ n'est pas divisé comme C : calcule avec pH₂. Réessaie."),
            (f"الجواب: {d(TAUS[2], 2)}.", f"Réponse : τ₂ = 10^(−{fr(PHS[2])})/{sci(CS[2], 1)} = {fr(TAUS[2], 2)}.")),
        2: (("لا، حتى ف S deux la réaction باقة limitée. عاود اختار.", "Même diluée, la réaction reste limitée. Réessaie."),
            (f"الجواب: {d(TAUS[2], 2)}، صغر من un.", f"Réponse : τ₂ = {fr(TAUS[2], 2)} < 1."))},
      f"p H deux égale {d(PHS[2])} et C deux égale {ds(CS[2], 1)} mole par litre. Tau deux vaut environ ?"),
  assoc("fa_5", "Plus facile : ce que fait la dilution", "Relie chaque grandeur à ce qu'elle devient quand on dilue.",
    "سؤال ساهل: ربط كل grandeur مع شنو كيوقع ليها ملي كنزيدو الما.",
    "De S₀ à S₂ (on dilue), relie chaque grandeur à son évolution.",
    [("1", "La concentration C de l'acide"), ("2", "Le pH"), ("3", "Le taux d'avancement final τ")],
    [("a", "diminue (divisée par 10 à chaque dilution)"), ("b", f"augmente ({fr(PHS[0])} → {fr(PHS[2])})"), ("c", f"augmente ({fr(TAUS[0], 3)} → {fr(TAUS[2], 2)})")],
    {"1": "a", "2": "b", "3": "c"},
    {"1-a": (True, "Oui : on ajoute de l'eau, C est divisée par 10.", "برافو: كنزيدو الما، C كتتقسم على dix."),
     "1-*": (False, "Regarde la colonne C : on ajoute de l'eau, l'acide est plus dispersé.", "لا، شوف la colonne C: كنزيدو الما، l'acide كيتفرق كثر."),
     "2-b": (True, "Oui : moins d'ions H₃O⁺ par litre, le pH monte.", "برافو: قل ديال les ions H trois O plus، le p H كيطلع."),
     "2-*": (False, "Ce sont les valeurs d'une autre colonne : lis la colonne pH.", "لا، هادو قيم ديال colonne أخرى. قرا la colonne ديال le p H."),
     "3-c": (True, "Oui : une plus grande part de l'acide réagit quand il est dilué.", "برافو: جزء كبر من l'acide كيتفاعل ملي كيكون dilué."),
     "3-*": (False, "τ n'est pas divisé par 10 : calcule-le ou lis ses valeurs.", "لا، tau ما كيتقسمش على dix. شوف les valeurs ديالو.")},
    ("(1 ; a) (2 ; b) (3 ; c) : plus la solution est diluée, plus τ est grand.",
     "plus la solution est diluée، plus tau est grand.")),
]

SIM_Q = [
  QS("1", f"Calculer V₀ pour préparer V₁ = {fr(sV1 * 1000, 1)} mL de S₁.",
     val("V₀", sV0 * 1000, "mL", f"V₀ = C₁·V₁/C₀ = {sci(sCS[1], 1)} × {fr(sV1 * 1000, 1)}/{sci(sC0, 1)} = {fr(sV0 * 1000, 1)} mL"),
     (["C₀·V₀ = C₁·V₁"], ["V₀ = C₀·V₁/C₁"]),
     [(f"V₀ = C₁·V₁/C₀ = {fr(sV0 * 1000, 1)} mL", "V zéro égale C un fois V un")],
     f"C zéro fois V zéro égale C un fois V un. V zéro égale C un fois V un، sur C zéro، يعني {d(sV0 * 1000, 1)} millilitres."),
  QS("2", "Montrer que τ = 10^(−pH)/C.",
     phrase("τ = x_f/x_max = 10^(−pH)·V/(C·V) = 10^(−pH)/C"), (["x_f/x_max"], ["x_f = C·V"]),
     [("τ = x_f/x_max = 10^(−pH)·V/(C·V) = 10^(−pH)/C", "tau égale x f sur x max")],
     "tau égale x f sur x max. x f égale dix puissance moins p H fois V، و x max égale C fois V. tau égale dix puissance moins p H، sur C."),
  QS("3", "Calculer τ₀.",
     val("τ₀", sTAUS[0], None, f"τ₀ = 10^(−{fr(sPHS[0])})/{sci(sC0, 1)} = {fr(sTAUS[0], 3)}"),
     (["τ = 10^(−pH)/C"], ["τ = 10^(pH)/C"]),
     [(f"τ₀ = {fr(sTAUS[0], 3)}", f"tau zéro égale {d(sTAUS[0], 3)}")], f"tau zéro égale {d(sTAUS[0], 3)}."),
  QS("4", "Calculer τ₁ et τ₂ et compléter le tableau.",
     val("τ₂", sTAUS[2], None, f"τ₁ = {fr(sTAUS[1], 2)} ; τ₂ = 10^(−{fr(sPHS[2])})/{sci(sCS[2], 1)} = {fr(sTAUS[2], 2)}"),
     (["τ = 10^(−pH)/C"], ["τ₂ = τ₀/100"]),
     [(f"τ₁ = {fr(sTAUS[1], 2)} ; τ₂ = {fr(sTAUS[2], 2)}", f"tau deux égale {d(sTAUS[2], 2)}")],
     f"tau un égale {d(sTAUS[1], 2)}، و tau deux égale {d(sTAUS[2], 2)}."),
  QS("5", "Comment varient le pH et τ quand on dilue ? Conclure.",
     phrase("Le pH augmente et τ augmente : plus la solution est diluée, plus τ est grand"),
     (["pH augmente", "τ augmente"], ["le pH diminue"]),
     [("pH ↑, τ ↑ : plus la solution est diluée, plus τ est grand", "plus la solution est diluée")],
     "le p H كيطلع و tau كيطلع. إذن plus la solution est diluée، plus tau est grand."),
]

EX = exercice(
  "phys_ex_ch11_deux_sens_5", "phys_ch11_transformations_deux_sens", "transformations_deux_sens",
  "Diluer l'acide butanoïque : que devient τ ?", "moyen", 25,
  ["Calculer le volume à prélever pour une dilution", "Montrer que τ = 10^(−pH)/C",
   "Calculer τ pour plusieurs concentrations", "Déduire l'influence de la dilution sur τ"],
  f"On dispose d'une solution S₀ d'acide butanoïque C₃H₇COOH de concentration C₀ = {sci(C0, 1)} mol/L. Par dilutions successives (chacune par 10), on prépare S₁ de concentration C₁ = C₀/10, puis S₂ de concentration C₂ = C₁/10. On mesure le pH de chaque solution à 25 °C (tableau). L'équation de la réaction de l'acide avec l'eau s'écrit : C₃H₇COOH(aq) + H₂O(l) ⇌ C₃H₇COO⁻(aq) + H₃O⁺(aq).",
  f"دابا نقراو l'énoncé. عندنا S zéro ديال l'acide butanoïque، C zéro égale {ds(C0, 1)} mole par litre. كنزيدو الما مرة ومرة: S un فيها C zéro sur dix، و S deux فيها C un sur dix. وكنقيسو le p H ديال كل وحدة، فle tableau.",
  [tab(CS, PHS)],
  [f"C₀ = {sci(C0, 1)} mol/L ; C₁ = {sci(CS[1], 1)} mol/L ; C₂ = {sci(CS[2], 1)} mol/L",
   f"pH₀ = {fr(PHS[0])} ; pH₁ = {fr(PHS[1])} ; pH₂ = {fr(PHS[2])} (25 °C)", f"V₁ = {fr(V1 * 1000, 1)} mL (question 1)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  f"Une solution S₀ d'acide méthanoïque HCOOH (C₀ = {sci(sC0, 1)} mol/L) est diluée deux fois de suite par 10 : S₁, puis S₂. On mesure les pH à 25 °C (tableau).",
  f"نفس التمرين، بقيم أخرى. l'acide méthanoïque، C zéro égale {ds(sC0, 1)} mole par litre، و deux dilutions par dix.",
  [tab(sCS, sPHS)],
  [f"pH₀ = {fr(sPHS[0])} ; pH₁ = {fr(sPHS[1])} ; pH₂ = {fr(sPHS[2])}", f"V₁ = {fr(sV1 * 1000, 1)} mL"],
  SIM_Q)

ecrire(EX)
