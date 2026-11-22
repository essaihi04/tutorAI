# Exercice de chimie, ch. 11 (transformations dans les deux sens), niveau facile : s'entraîner aux gestes un par un
# (équation avec l'eau, [H₃O⁺] = 10^(−pH), x_max = C·V, x_f puis τ et la conclusion).
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2017 N (1.1 τ puis déduire), 2020 R (1.1 équation, 1.3 τ « que peut-on
#    déduire »), 2021 N (2.1 équation, 2.2 « montrer que τ ≈ 1,32 % »), 2022 N (1.1 équation, 1.2 τ, conclure),
#    2022 R (1.3 τ) — backend/data/exams/physique ;
#  - profs (architecture/sources_chimie_ch9_ch11.md, chapitre C : Mahajar-Tabit, El Founani, Sbiro, Hadjyne ;
#    vidéos El Omrani, Driss DOTCOM, Prof othmane, TOP PHYSIQUE CHIMIE) : tableau acide + eau, x_f par le pH,
#    τ = x_f/x_max ; pièges : oublier le signe moins de 10^(−pH), V en mL dans x_max, conclure sans comparer τ à 1 ;
#  - séries en ligne : talamidi (deux sens, exercices non corrigés 1), moutamadris (cours et exercices deux sens 2022),
#    alloschool (séance 8 El Goufifa, élément 119806 ; « taux d'avancement et conductimétrie corrigé »),
#    kezakoo (exercices transformation), coursdusoirpc (TD 2 BAC BIOF).
# Ici : l'acide propanoïque, nos propres C, V et pH (pH calculé pour pKa ≈ 4,87, arrondi comme une mesure).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *
from _ch11 import *

C, V, PH = 2.0e-2, 0.200, 3.29
H = 10 ** -PH                 # 5,13e-4 mol/L
XMAX = C * V                  # 4,0e-3 mol
XF = H * V                    # 1,03e-4 mol
TAU = XF / XMAX               # 0,0256
assert abs(XMAX - 4.0e-3) < 1e-12 and abs(H - 5.13e-4) < 1e-6 and abs(TAU - 0.0256) < 2e-4

sC, sV, sPH = 5.0e-2, 0.100, 3.09
sH = 10 ** -sPH; sX = sC * sV; sXF = sH * sV; sTAU = sXF / sX
assert abs(sH - 8.13e-4) < 1e-6 and abs(sX - 5.0e-3) < 1e-12 and abs(sTAU - 0.0163) < 2e-4

EQ = "C₂H₅COOH(aq) + H₂O(l) ⇌ C₂H₅COO⁻(aq) + H₃O⁺(aq)"
EQ_DIT = "l'acide propanoïque، plus H deux O، double flèche، l'ion propanoate، plus H trois O plus"

QUESTIONS = [
  Q("1", "Écrire l'équation de la réaction de l'acide propanoïque C₂H₅COOH avec l'eau.",
    "السؤال un: كتب l'équation ديال la réaction ديال l'acide propanoïque مع الما.",
    phrase(EQ),
    (["C₂H₅COOH", "H₂O", "C₂H₅COO⁻", "H₃O⁺", "⇌"], ["HO⁻", "C₂H₅COOH₂⁺"]),
    [("L'acide cède un proton H⁺ : à qui le donne-t-il, et que devient-il après l'avoir perdu ?",
      "l'acide كيعطي un proton. لمن كيعطيه؟ وشنو كيولي من بعد ما ضيعو؟"),
     ("L'eau capte le proton et devient H₃O⁺ ; l'acide devient sa base conjuguée C₂H₅COO⁻. La réaction n'est pas totale : double flèche.",
      "الما كيشد le proton وكيولي H trois O plus، و l'acide كيولي la base conjuguée ديالو، l'ion propanoate. و la réaction ماشي totale: la double flèche.")],
    [("1 : l'acide propanoïque cède un proton à l'eau", "كيعطي un proton للما"),
     (EQ, "l'équation")],
    f"السؤال un. l'acide propanoïque كيعطي un proton للما. l'équation: {EQ_DIT}.",
    "ex_1", "fa_1"),
  Q("2", f"La mesure du pH de la solution donne pH = {fr(PH)}. Calculer la concentration [H₃O⁺]_éq des ions oxonium dans la solution.",
    f"السؤال deux: le p H ديال المحلول égale {d(PH)}. حسب la concentration des ions H trois O plus فالمحلول.",
    val("[H₃O⁺]", H, "mol/L", f"[H₃O⁺]_éq = 10^(−pH) = 10^(−{fr(PH)}) = {sci(H, 1)} mol/L"),
    (["[H₃O⁺] = 10^(−pH)", "10^", "mol/L"], ["[H₃O⁺] = 10^(pH)", "[H₃O⁺] = −log(pH)"]),
    [("Le pH est lié à la concentration des ions H₃O⁺ : quelle relation permet de revenir du pH à la concentration ?",
      "le p H مربوط ب la concentration des ions H trois O plus. شنو la relation اللي كترجعنا من le p H ل la concentration؟"),
     ("[H₃O⁺] = 10^(−pH) : n'oublie pas le signe moins dans l'exposant.",
      "la concentration des ions H trois O plus، égale dix puissance moins p H. ما تنساش le signe moins.")],
    [("2 : [H₃O⁺]_éq = 10^(−pH)", "égale dix puissance moins p H"),
     (f"[H₃O⁺]_éq = 10^(−{fr(PH)})", f"dix puissance moins {d(PH)}"),
     (f"[H₃O⁺]_éq = {sci(H, 1)} mol/L", f"{ds(H, 1)} mole par litre")],
    f"السؤال deux. la concentration des ions H trois O plus، égale dix puissance moins p H. l'application numérique: dix puissance moins {d(PH)}. le résultat: {ds(H, 1)} mole par litre.",
    "ex_2", "fa_2"),
  Q("3", f"Le volume de la solution est V = {fr(V * 1000, 0)} mL. En s'aidant du tableau d'avancement, calculer l'avancement maximal x_max.",
    f"السؤال trois: le volume ديال المحلول V égale {d(V * 1000, 0)} millilitres. بمساعدة le tableau d'avancement، حسب x max.",
    val("x_max", XMAX, "mol", f"x_max = C·V = {sci(C, 1)} × {fr(V, 3)} = {sci(XMAX, 1)} mol"),
    (["x_max = C·V", "C·V − x_max = 0", "L", "mol"], [f"x_max = C·V = {sci(C, 1)} × {fr(V * 1000, 0)}", "x_max = C/V"]),
    [("Si la réaction était totale, quel réactif s'épuiserait ? L'eau est le solvant, elle est en excès.",
      "يلا كانت la réaction totale، شكون غادي يتسالى؟ الما هو le solvant، كاين en excès."),
     ("L'acide est le réactif limitant : C·V − x_max = 0, donc x_max = C·V, avec V en litres.",
      "l'acide هو le réactif limitant: C V moins x max égale zéro، إذن x max égale C fois V، و V ب litre.")],
    [("3 : l'eau est en excès, l'acide est limitant : C·V − x_max = 0", "C V moins x max égale zéro"),
     (f"x_max = C·V = {sci(C, 1)} × {fr(V, 3)}", "x max égale C fois V"),
     (f"x_max = {sci(XMAX, 1)} mol", f"x max égale {ds(XMAX, 1)} mole")],
    f"السؤال trois. الما en excès، إذن l'acide هو le réactif limitant: C V moins x max égale zéro. x max égale C fois V، يعني {ds(C, 1)}، fois {d(V, 1)} litre. x max égale {ds(XMAX, 1)} mole.",
    "ex_3", "fa_3"),
  Q("4", "Calculer l'avancement final x_f, puis le taux d'avancement final τ (valeur décimale). Conclure.",
    "السؤال quatre: حسب x f، ومن بعد le taux d'avancement final tau. واستنتج.",
    val("τ", TAU, None, f"x_f = [H₃O⁺]·V = {sci(XF, 2)} mol ; τ = x_f/x_max = {fr(TAU, 3)} < 1 : réaction limitée"),
    (["x_f = [H₃O⁺]·V", "τ = x_f/x_max", "< 1", "limitée"], ["τ = x_max/x_f", "x_f = C·V"]),
    [("Dans le tableau, la quantité finale des ions H₃O⁺ est x_f : et cette quantité, c'est leur concentration fois le volume.",
      "فle tableau، la quantité finale ديال les ions H trois O plus هي x f. وهاد la quantité هي la concentration fois le volume."),
     ("x_f = [H₃O⁺]_éq·V, puis τ = x_f/x_max. Compare τ à 1 pour conclure.",
      "x f égale la concentration des ions H trois O plus fois V، ومن بعد tau égale x f sur x max. قارن tau مع un باش تستنتج.")],
    [(f"4 : x_f = [H₃O⁺]_éq·V = {sci(H, 2)} × {fr(V, 3)} = {sci(XF, 2)} mol", "x f égale la concentration des ions H trois O plus fois V"),
     (f"τ = x_f/x_max = {sci(XF, 2)} / {sci(XMAX, 1)} = {fr(TAU, 3)}", "tau égale x f sur x max"),
     ("τ < 1 : la réaction de l'acide avec l'eau est limitée", "la réaction limitée")],
    f"السؤال quatre. x f égale la concentration des ions H trois O plus fois V، يعني {ds(XF, 2)} mole. tau égale x f sur x max، يعني {d(TAU, 3)}، تقريبا {pc(TAU)}. tau صغر من un، إذن la réaction limitée.",
    "ex_4", "fa_4"),
]

EXPLICATIONS = [
  sl_acide_eau("ex_1", "Question 1 : l'acide propanoïque cède un proton à l'eau",
    f"l'acide هو l'acide propanoïque، و la base conjuguée ديالو هي l'ion propanoate. إذن l'équation: {EQ_DIT}.",
    [(EQ, "إذن l'équation")]),
  sl_ph("ex_2", "Question 2 : du pH à [H₃O⁺]",
    f"le p H égale {d(PH)}. إذن la concentration égale dix puissance moins {d(PH)}، يعني {ds(H, 1)} mole par litre.",
    [(f"[H₃O⁺] = 10^(−{fr(PH)})", f"إذن la concentration égale dix puissance moins {d(PH)}"), (f"[H₃O⁺] = {sci(H, 1)} mol/L", f"يعني {ds(H, 1)} mole par litre")]),
  sl_xmax("ex_3", "Question 3 : x_max = C·V",
    f"C égale {ds(C, 1)} mole par litre، و V égale {d(V * 1000, 0)} millilitres، يعني {d(V, 1)} litre. إذن x max égale {ds(XMAX, 1)} mole.",
    [("x_max = C·V", "و V égale"), (f"x_max = {sci(C, 1)} × {fr(V, 3)} = {sci(XMAX, 1)} mol", f"إذن x max égale {ds(XMAX, 1)} mole")]),
  sl_taux("ex_4", "Question 4 : x_f puis τ",
    f"x f égale la concentration des ions H trois O plus fois V، يعني {ds(XF, 2)} mole. tau égale x f sur x max، يعني {d(TAU, 3)}. tau صغر من un: la réaction limitée.",
    [(f"x_f = {sci(XF, 2)} mol", f"يعني {ds(XF, 2)} mole"), (f"τ = {fr(TAU, 3)} < 1 : limitée", f"يعني {d(TAU, 3)}")]),
]

FACILES = [
  assoc("fa_1", "Plus facile : le rôle de chaque espèce", "Relie chaque espèce à son rôle dans la réaction.",
    "سؤال ساهل: ربط كل espèce مع الدور ديالها ف la réaction.",
    "Dans C₂H₅COOH + H₂O ⇌ C₂H₅COO⁻ + H₃O⁺, relie chaque espèce à son rôle.",
    [("1", "C₂H₅COOH"), ("2", "H₂O"), ("3", "C₂H₅COO⁻")],
    [("a", "acide : cède un proton"), ("b", "base : capte un proton"), ("c", "base conjuguée de l'acide propanoïque")],
    {"1": "a", "2": "b", "3": "c"},
    {"1-a": (True, "Oui : l'acide propanoïque cède son proton à l'eau.", "برافو: l'acide propanoïque كيعطي le proton ديالو للما."),
     "1-b": (False, "Il ne capte pas de proton : il en perd un. Que fait un acide ?", "لا، هو ما كيشدش le proton، كيضيعو. شنو كيدير l'acide؟"),
     "1-c": (False, "C₂H₅COO⁻ est ce que devient l'acide : regarde qui a encore son proton.", "لا، la base conjuguée هي اللي كيولي l'acide من بعد. شوف شكون باقي عندو le proton."),
     "2-a": (False, "Ici l'eau ne cède pas de proton : elle devient H₃O⁺, elle en gagne un.", "لا، هنا الما ما كيعطيش le proton: كيولي H trois O plus، يعني كيشد واحد."),
     "2-b": (True, "Oui : l'eau capte le proton et devient H₃O⁺ ; ici elle joue le rôle de base.", "برافو: الما كيشد le proton وكيولي H trois O plus، هنا هو la base."),
     "2-c": (False, "L'eau n'est pas la base conjuguée de l'acide propanoïque : elles ne diffèrent pas d'un seul proton.", "لا، الما ماشي la base conjuguée ديال l'acide propanoïque."),
     "3-a": (False, "L'ion propanoate n'a plus de proton à céder dans ce couple : c'est le reste de l'acide.", "لا، l'ion propanoate ما بقا عندو حتى proton يعطيه فهاد le couple."),
     "3-b": (False, "Presque : c'est bien une base, mais précise de quel acide elle vient.", "قريب: هي base، ولكن حدد من أي acide جات."),
     "3-c": (True, "Oui : C₂H₅COO⁻ est la base conjuguée de C₂H₅COOH, ils diffèrent d'un proton.", "برافو: l'ion propanoate هو la base conjuguée ديال l'acide propanoïque، الفرق غير proton.")},
    ("(1 ; a) (2 ; b) (3 ; c) : l'acide cède son proton à l'eau, qui joue ici le rôle de base.",
     "l'acide كيعطي le proton ديالو للما، والما هنا كيلعب دور la base.")),
  qcm("fa_2", "Plus facile : du pH à [H₃O⁺]", "سؤال ساهل: اختار la bonne relation.",
      f"pH = {fr(PH)}. Quelle relation donne [H₃O⁺] ?",
      ["[H₃O⁺] = 10^(pH)", "[H₃O⁺] = 10^(−pH)", "[H₃O⁺] = −log(pH)"], 1, {
        1: ("juste", f"برافو! la concentration égale dix puissance moins p H، يعني {ds(H, 1)} mole par litre.", f"Juste : [H₃O⁺] = 10^(−{fr(PH)}) = {sci(H, 1)} mol/L."),
        0: (("ما تقلقش. بلا le signe moins كتلقى رقم كبير بزاف، ماشي concentration صغيرة. عاود اختار.", "Sans le signe moins, on trouve un nombre énorme. Réessaie."),
            ("الجواب هو dix puissance moins p H. le signe moins ضروري.", "Réponse : [H₃O⁺] = 10^(−pH).")),
        2: (("لا، moins log هي اللي كتعطي le p H من la concentration، ماشي العكس. عاود اختار.", "−log donne le pH à partir de la concentration, pas l'inverse. Réessaie."),
            ("الجواب هو dix puissance moins p H: هي العكس ديال moins log.", "Réponse : [H₃O⁺] = 10^(−pH), l'inverse de pH = −log[H₃O⁺]."))},
      f"p H égale {d(PH)}. Quelle relation donne la concentration des ions H trois O plus ?"),
  qcm("fa_3", "Plus facile : x_max", "سؤال ساهل على x max. رد البال للوحدة.",
      f"C = {sci(C, 1)} mol/L et V = {fr(V * 1000, 0)} mL. x_max vaut…",
      [f"{sci(XMAX, 1)} mol", f"{fr(C * V * 1000, 1)} mol", f"{sci(C / V, 1)} mol"], 0, {
        0: ("juste", f"برافو! x max égale C fois V، و V ب litre: {ds(XMAX, 1)} mole.", f"Juste : x_max = {sci(C, 1)} × {fr(V, 3)} = {sci(XMAX, 1)} mol."),
        1: (("ما تقلقش. ضربتي ف le volume ب millilitre. خاصو يكون ب litre. عاود اختار.", "Le volume doit être en litres. Réessaie."),
            (f"الجواب هو {ds(XMAX, 1)} mole: {d(V * 1000, 0)} millilitres هي {d(V, 1)} litre.", f"Réponse : x_max = C·V = {sci(XMAX, 1)} mol (V en L).")),
        2: (("لا، قسمتي C على V. x max هي C fois V. عاود اختار.", "On ne divise pas : x_max = C·V. Réessaie."),
            (f"الجواب هو {ds(XMAX, 1)} mole، حيت x max égale C fois V.", f"Réponse : x_max = C·V = {sci(XMAX, 1)} mol."))},
      f"C égale {ds(C, 1)} mole par litre et V égale {d(V * 1000, 0)} millilitres. x max vaut ?"),
  vf("fa_4", "Plus facile : vrai ou faux", f"x_f = {sci(XF, 2)} mol et x_max = {sci(XMAX, 1)} mol.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [(f"τ = x_f/x_max ≈ {fr(TAU, 3)}.", True, "τ est le rapport de l'avancement final (mesuré) sur l'avancement maximal (calculé)."),
      ("τ = x_max/x_f, donc τ > 1.", False, "C'est l'inverse : τ = x_f/x_max, toujours inférieur ou égal à 1."),
      ("τ < 1 : la réaction de l'acide propanoïque avec l'eau est limitée.", True, "x_f < x_max : l'acide n'a pas réagi en entier.")]),
]

SIM_Q = [
  QS("1", "Écrire l'équation de la réaction de l'acide propanoïque avec l'eau.", phrase(EQ),
     (["C₂H₅COOH", "H₂O", "⇌", "H₃O⁺"], ["HO⁻"]),
     [(EQ, "l'équation")], f"l'équation: {EQ_DIT}."),
  QS("2", f"pH = {fr(sPH)}. Calculer [H₃O⁺]_éq.",
     val("[H₃O⁺]", sH, "mol/L", f"[H₃O⁺]_éq = 10^(−{fr(sPH)}) = {sci(sH, 1)} mol/L"),
     (["[H₃O⁺] = 10^(−pH)", "mol/L"], ["10^(pH)"]),
     [(f"[H₃O⁺]_éq = 10^(−{fr(sPH)}) = {sci(sH, 1)} mol/L", f"{ds(sH, 1)} mole par litre")],
     f"la concentration égale dix puissance moins {d(sPH)}، يعني {ds(sH, 1)} mole par litre."),
  QS("3", f"V = {fr(sV * 1000, 0)} mL. Calculer x_max.",
     val("x_max", sX, "mol", f"x_max = C·V = {sci(sC, 1)} × {fr(sV, 3)} = {sci(sX, 1)} mol"),
     (["x_max = C·V", "mol"], ["x_max = C/V"]),
     [(f"x_max = C·V = {sci(sC, 1)} × {fr(sV, 3)} = {sci(sX, 1)} mol", "x max égale C fois V")],
     f"x max égale C fois V، يعني {ds(sC, 1)}، fois {d(sV, 1)} litre. x max égale {ds(sX, 1)} mole."),
  QS("4", "Calculer x_f, puis τ (valeur décimale). Conclure.",
     val("τ", sTAU, None, f"x_f = [H₃O⁺]·V = {sci(sXF, 2)} mol ; τ = x_f/x_max = {fr(sTAU, 3)} < 1 : limitée"),
     (["x_f = [H₃O⁺]·V", "τ = x_f/x_max"], ["τ = x_max/x_f"]),
     [(f"x_f = {sci(sH, 2)} × {fr(sV, 3)} = {sci(sXF, 2)} mol", "x f égale"),
      (f"τ = {fr(sTAU, 3)} < 1 : réaction limitée", "tau égale")],
     f"x f égale la concentration fois V، يعني {ds(sXF, 2)} mole. tau égale x f sur x max، يعني {d(sTAU, 3)}. tau صغر من un: la réaction limitée."),
]

EX = exercice(
  "phys_ex_ch11_deux_sens_1", "phys_ch11_transformations_deux_sens", "transformations_deux_sens",
  "L'acide propanoïque dans l'eau : pH, x_max, x_f et τ", "facile", 15,
  ["Écrire l'équation de la réaction d'un acide avec l'eau", "Calculer [H₃O⁺] = 10^(−pH)",
   "Calculer x_max = C·V et x_f = [H₃O⁺]·V", "Calculer τ = x_f/x_max et conclure"],
  f"On prépare un volume V = {fr(V * 1000, 0)} mL d'une solution aqueuse d'acide propanoïque C₂H₅COOH de concentration C = {sci(C, 1)} mol/L. À 25 °C, la mesure du pH de la solution donne pH = {fr(PH)}.",
  f"دابا نقراو l'énoncé. عندنا {d(V * 1000, 0)} millilitres ديال محلول ديال l'acide propanoïque، la concentration ديالو C égale {ds(C, 1)} mole par litre. le p H mètre كيعطي p H égale {d(PH)}.",
  [],
  [f"V = {fr(V * 1000, 0)} mL", f"C = {sci(C, 1)} mol/L", f"pH = {fr(PH)} (à 25 °C)", "Couple : C₂H₅COOH(aq) / C₂H₅COO⁻(aq)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  f"On prépare V = {fr(sV * 1000, 0)} mL d'une solution d'acide propanoïque de concentration C = {sci(sC, 1)} mol/L. Son pH vaut {fr(sPH)}.",
  f"نفس التمرين، بقيم أخرى. {d(sV * 1000, 0)} millilitres ديال l'acide propanoïque، C égale {ds(sC, 1)} mole par litre، و p H égale {d(sPH)}.",
  [], [f"V = {fr(sV * 1000, 0)} mL", f"C = {sci(sC, 1)} mol/L", f"pH = {fr(sPH)}"],
  SIM_Q)

ecrire(EX)
