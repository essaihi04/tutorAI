# Exercice de chimie, ch. 11 (transformations dans les deux sens), niveau moyen (celui du national) : une solution
# préparée par dissolution, son tableau d'avancement, la comparaison « pH si totale / pH mesuré », la démonstration
# « montrer que τ = 10^(−pH)/C », puis τ et la conclusion — les questions s'enchaînent comme à l'examen.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2021 R (Q5 équation, Q9 « montrer que τ = 10^(−pH)/C »), 2019 N (2.1 équation,
#    2.2 tableau, 2.3.2 « montrer que τ = … »), 2020 R (1.1, 1.3 τ « que peut-on déduire »), 2022 N (1.1, 1.2),
#    2022 R (1.2, 1.3), 2021 N (2.2 « montrer que τ ≈ 1,32 % ») — backend/data/exams/physique ;
#  - profs (sources_chimie_ch9_ch11.md, chapitre C : Sbiro, 1 mL d'acide pur dans 500 mL, n₀, tableau, x_f, τ ;
#    Mahajar-Tabit et Hadjyne, HCl puis acide éthanoïque, « si totale le pH serait… ») ; pièges : x_max avec V en
#    mL, écrire → au lieu de ⇌, « montrer que » sans partir de la définition ;
#  - séries en ligne : talamidi (deux sens, non corrigés 1), alloschool (séance 8 El Goufifa ; « taux d'avancement
#    et conductimétrie corrigé »), moutamadris (cours et exercices deux sens 2022), kezakoo (exercices
#    transformation), coursdusoirpc (TD 2 BAC BIOF).
# Ici : l'acide lactique (noté AH), nos propres m, V et pH (calculé pour pKa ≈ 3,86, arrondi comme une mesure).
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *
from _ch11 import *

M = 90.0                       # g/mol, acide lactique C₃H₆O₃
m, V, PH = 0.450, 0.250, 2.80
n0 = m / M; C = n0 / V         # 5,0e-3 mol ; 2,0e-2 mol/L
PHT = -math.log10(C)           # 1,70 si totale
H = 10 ** -PH                  # 1,58e-3 mol/L
TAU = H / C                    # 0,079
assert abs(C - 2.0e-2) < 1e-12 and abs(PHT - 1.70) < 0.005 and abs(TAU - 0.0792) < 2e-4

sm, sV, sPH = 0.900, 0.250, 2.64
sC = sm / M / sV; sPHT = -math.log10(sC); sH = 10 ** -sPH; sTAU = sH / sC
assert abs(sC - 4.0e-2) < 1e-12 and abs(sPHT - 1.40) < 0.005 and abs(sTAU - 0.0573) < 2e-4

EQ = "AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq)"
EQ_DIT = "A H، plus H deux O، double flèche، A moins، plus H trois O plus"
TAB = "initial : C·V, excès, 0, 0 ; en cours : C·V − x, excès, x, x ; final : C·V − x_f, excès, x_f, x_f"

QUESTIONS = [
  Q("1", "Calculer la concentration C de la solution S.",
    "السؤال un: حسب la concentration C ديال المحلول S.",
    val("C", C, "mol/L", f"n₀ = m/M = {fr(m, 3)}/{fr(M, 0)} = {sci(n0, 1)} mol ; C = n₀/V = {sci(n0, 1)}/{fr(V, 3)} = {sci(C, 1)} mol/L"),
    (["n = m/M", "C = n/V", "g/mol", "mol/L"], ["C = m/V", "C = n·V"]),
    [("On connaît la masse dissoute : commence par la quantité de matière, puis divise par le volume.",
      "عندك la masse اللي ذوبنا. بدا ب la quantité de matière، ومن بعد قسم على le volume."),
     ("n₀ = m/M, puis C = n₀/V avec V en litres.", "n zéro égale m sur M، ومن بعد C égale n zéro sur V، و V ب litre.")],
    [(f"1 : n₀ = m/M = {fr(m, 3)}/{fr(M, 0)} = {sci(n0, 1)} mol", "n zéro égale m sur M"),
     (f"C = n₀/V = {sci(n0, 1)}/{fr(V, 3)}", "C égale n zéro sur V"),
     (f"C = {sci(C, 1)} mol/L", f"C égale {ds(C, 1)} mole par litre")],
    f"السؤال un. n zéro égale m sur M، يعني {d(m, 3)} sur quatre-vingt-dix، égale {ds(n0, 1)} mole. C égale n zéro sur V، يعني {ds(n0, 1)}، sur {d(V, 2)} litre. C égale {ds(C, 1)} mole par litre.",
    "ex_1", "fa_1"),
  Q("2", "Écrire l'équation de la réaction de l'acide AH avec l'eau, puis dresser le tableau d'avancement (en fonction de C, V, x et x_f).",
    "السؤال deux: كتب l'équation ديال la réaction ديال A H مع الما، ومن بعد دير le tableau d'avancement ب C و V و x و x f.",
    phrase(EQ + " ; " + TAB),
    (["⇌", "C·V", "C·V − x", "x_f", "excès"], ["C·V − 2x", "→"]),
    [("L'acide cède un proton à l'eau ; l'eau est le solvant, en excès. Au départ, aucun produit.",
      "l'acide كيعطي un proton للما، والما هو le solvant، en excès. فالبداية، ما كاين حتى produit."),
     ("Coefficients tous égaux à 1 : chaque fois que x augmente, AH diminue de x et chaque produit augmente de x.",
      "les coefficients كاملين un: كل ما زادت x، A H كينقص ب x، وكل produit كيزيد ب x.")],
    [(f"2 : {EQ}", "l'équation"),
     ("état initial (x = 0) : n(AH) = C·V ; H₂O en excès ; n(A⁻) = 0 ; n(H₃O⁺) = 0", "l'état initial"),
     ("en cours (x) : C·V − x ; excès ; x ; x", "en cours"),
     ("état final (x_f) : C·V − x_f ; excès ; x_f ; x_f", "l'état final")],
    f"السؤال deux. l'équation: {EQ_DIT}. le tableau: l'état initial، A H égale C fois V، الما en excès، و zéro و zéro. en cours: C V moins x، و x، و x. l'état final: C V moins x f، و x f، و x f.",
    "ex_2", "fa_2"),
  Q("3", f"La mesure du pH de S donne pH = {fr(PH)}. Calculer le pH qu'aurait la solution si la réaction était totale, puis le comparer au pH mesuré. Conclure.",
    f"السؤال trois: le p H ديال S égale {d(PH)}. حسب le p H اللي كان غادي يكون يلا كانت la réaction totale، وقارنو مع le p H المقاس. استنتج.",
    val("pH", PHT, None, f"si totale : [H₃O⁺] = C, pH = −log C = −log({sci(C, 1)}) = {fr(PHT)} ; {fr(PH)} > {fr(PHT)} : non totale"),
    (["pH = −log[H₃O⁺]", "[H₃O⁺] = C", "−log"], ["pH = −log(C·V)", "pH = log C"]),
    [("Si la réaction était totale, tout l'acide aurait donné des ions H₃O⁺ : quelle serait alors leur concentration ?",
      "يلا كانت la réaction totale، كل l'acide كان غادي يعطي les ions H trois O plus. شحال غادي تكون la concentration ديالهم؟"),
     ("Si totale : [H₃O⁺] = C, donc pH = −log C. Un pH mesuré plus grand veut dire moins d'ions H₃O⁺.",
      "يلا totale: la concentration des ions H trois O plus égale C، إذن p H égale moins log de C. و p H كبر معناه قل ديال les ions H trois O plus.")],
    [("3 : si la réaction était totale, [H₃O⁺] = C", "égale C"),
     (f"pH = −log C = −log({sci(C, 1)}) = {fr(PHT)}", f"p H égale moins log de C، يعني {d(PHT)}"),
     (f"pH mesuré = {fr(PH)} > {fr(PHT)} : moins d'ions H₃O⁺ que prévu, la réaction n'est pas totale", "ماشي totale")],
    f"السؤال trois. يلا كانت la réaction totale، la concentration des ions H trois O plus égale C. p H égale moins log de C، يعني {d(PHT)}. le p H المقاس {d(PH)}، كبر من {d(PHT)}: كاينين قل ديال les ions H trois O plus، إذن la réaction ماشي totale.",
    "ex_3", "fa_3"),
  Q("4", "En s'aidant du tableau d'avancement, montrer que le taux d'avancement final s'écrit τ = 10^(−pH)/C.",
    "السؤال quatre: بمساعدة le tableau d'avancement، بين أن tau égale dix puissance moins p H، sur C.",
    phrase("τ = x_f/x_max ; x_f = n(H₃O⁺)_f = [H₃O⁺]·V = 10^(−pH)·V ; x_max = C·V (AH limitant) ; τ = 10^(−pH)·V/(C·V) = 10^(−pH)/C"),
    (["τ = x_f/x_max", "x_f = [H₃O⁺]·V", "x_max = C·V", "10^(−pH)"], ["x_f = C·V", "τ = x_max/x_f"]),
    [("Pars toujours de la définition τ = x_f/x_max, puis remplace x_f et x_max à l'aide du tableau.",
      "بدا ديما من la définition: tau égale x f sur x max. ومن بعد بدل x f و x max بمساعدة le tableau."),
     ("Colonne H₃O⁺ : x_f = [H₃O⁺]·V = 10^(−pH)·V. Si totale, AH s'épuise : x_max = C·V. Le volume se simplifie.",
      "la colonne ديال H trois O plus: x f égale dix puissance moins p H fois V. و x max égale C fois V. V كيتحيد.")],
    [("4 : τ = x_f/x_max", "tau égale x f sur x max"),
     ("x_f = [H₃O⁺]_éq·V = 10^(−pH)·V et x_max = C·V", "x f égale dix puissance moins p H fois V"),
     ("τ = 10^(−pH)·V/(C·V) = 10^(−pH)/C", "V كيتحيد")],
    "السؤال quatre. tau égale x f sur x max. من le tableau: x f égale dix puissance moins p H fois V، و x max égale C fois V. V كيتحيد، وكيبقى tau égale dix puissance moins p H، sur C.",
    "ex_4", "fa_4"),
  Q("5", "Calculer τ. Que peut-on déduire ?",
    "السؤال cinq: حسب tau. شنو نستنتجو؟",
    val("τ", TAU, None, f"τ = 10^(−{fr(PH)})/{sci(C, 1)} = {fr(TAU, 3)} < 1 : réaction limitée"),
    (["τ = 10^(−pH)/C", "< 1", "limitée"], ["τ = 10^(pH)/C", "τ = C/10^(−pH)"]),
    [("Remplace dans la relation que tu viens de montrer.", "عوض فla relation اللي بينتي دابا."),
     ("τ = 10^(−pH)/C, puis compare τ à 1.", "tau égale dix puissance moins p H، sur C. ومن بعد قارن tau مع un.")],
    [(f"5 : τ = 10^(−{fr(PH)})/{sci(C, 1)}", f"dix puissance moins {d(PH)}"),
     (f"τ = {fr(TAU, 3)}", f"tau égale {d(TAU, 3)}"),
     ("τ < 1 : la réaction de l'acide lactique avec l'eau est limitée", "la réaction limitée")],
    f"السؤال cinq. tau égale dix puissance moins {d(PH)}، sur {ds(C, 1)}. tau égale {d(TAU, 3)}، تقريبا {pc(TAU, 0)}. tau صغر من un: la réaction limitée.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sl_concentration("ex_1", "Question 1 : de la masse à la concentration",
    f"عندنا la masse، إذن الأول n zéro égale m sur M، يعني {ds(n0, 1)} mole. ومن بعد C égale n zéro sur V، يعني {ds(C, 1)} mole par litre.",
    [("n₀ = m/M ; C = n₀/V", "إذن الأول n zéro égale m sur M"), (f"C = {sci(C, 1)} mol/L", f"يعني {ds(C, 1)} mole par litre")]),
  sl_tableau("ex_2", "Question 2 : le tableau d'avancement",
    f"l'équation: {EQ_DIT}. و l'acide فالبداية C fois V، يعني {ds(n0, 1)} mole.",
    [(EQ, "l'équation: A H"), ("C·V − x_f ; x_f ; x_f", "و l'acide فالبداية")]),
  sl_attendu("ex_3", "Question 3 : pH attendu si totale, pH mesuré",
    f"يلا totale، la concentration des ions H trois O plus égale C، و p H égale moins log de C، يعني {d(PHT)}. ولكن لقينا {d(PH)}، كبر. إذن la réaction ماشي totale.",
    [(f"pH = −log C = {fr(PHT)}", f"يعني {d(PHT)}"), (f"{fr(PH)} > {fr(PHT)} : non totale", f"ولكن لقينا {d(PH)}")]),
  sl_relation("ex_4", "Question 4 : montrer que τ = 10^(−pH)/C",
    "نفس الخطوات بالضبط: la définition، كنبدلو x f و x max، V كيتحيد. هادي هي الكتابة اللي خاصك تكتب فالامتحان.",
    [("τ = x_f/x_max = 10^(−pH)·V/(C·V) = 10^(−pH)/C", "نفس الخطوات بالضبط")]),
  sl_taux("ex_5", "Question 5 : τ et la conclusion",
    f"tau égale dix puissance moins {d(PH)}، sur {ds(C, 1)}، يعني {d(TAU, 3)}. tau صغر من un: la réaction limitée.",
    [(f"τ = {fr(TAU, 3)} < 1 : limitée", f"يعني {d(TAU, 3)}")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : la concentration", "سؤال ساهل: اختار la bonne valeur.",
      f"m = {fr(m, 3)} g d'acide (M = {fr(M, 0)} g/mol) dans V = {fr(V * 1000, 0)} mL. C vaut…",
      [f"{fr(m / V, 2)} mol/L", f"{sci(n0 / (V * 1000), 1)} mol/L", f"{sci(C, 1)} mol/L"], 2, {
        2: ("juste", f"برافو! n zéro égale m sur M، ومن بعد C égale n zéro sur V: {ds(C, 1)} mole par litre.", f"Juste : C = ({fr(m, 3)}/{fr(M, 0)})/{fr(V, 3)} = {sci(C, 1)} mol/L."),
        0: (("ما تقلقش. m sur V كتعطي des grammes par litre، ماشي des moles. خاصك تمر ب M. عاود اختار.", "m/V donne des g/L, pas des mol/L : passe par n = m/M. Réessaie."),
            (f"الجواب: {ds(C, 1)} mole par litre. الأول n égale m sur M، ومن بعد C égale n sur V.", f"Réponse : C = n₀/V = {sci(C, 1)} mol/L.")),
        1: (("قريب! ولكن le volume خاصو يكون ب litre، ماشي ب millilitre. عاود اختار.", "Le volume doit être en litres. Réessaie."),
            (f"الجواب: {ds(C, 1)} mole par litre، مع V égale {d(V, 2)} litre.", f"Réponse : {sci(C, 1)} mol/L (V = {fr(V, 3)} L)."))},
      f"m égale {d(m, 3)} gramme d'acide, M égale quatre-vingt-dix grammes par mole, dans {d(V * 1000, 0)} millilitres. C vaut ?"),
  assoc("fa_2", "Plus facile : remplir le tableau", "Relie chaque case du tableau à son expression.",
    "سؤال ساهل: ربط كل خانة ف le tableau مع l'expression ديالها.",
    "Dans le tableau de AH + H₂O ⇌ A⁻ + H₃O⁺, relie chaque case à son expression.",
    [("1", "n(AH) à l'état initial"), ("2", "n(H₃O⁺) en cours"), ("3", "n(AH) à l'état final")],
    [("a", "C·V"), ("b", "x"), ("c", "C·V − x_f"), ("d", "C·V − x")],
    {"1": "a", "2": "b", "3": "c"},
    {"1-a": (True, "Oui : au départ, n(AH) = C·V.", "برافو: فالبداية، A H égale C fois V."),
     "1-*": (False, "Au départ, x = 0 : aucun acide n'a encore réagi.", "لا، فالبداية x égale zéro: حتى شي acide ما تفاعل."),
     "2-b": (True, "Oui : chaque fois qu'un AH réagit, un H₃O⁺ se forme : n(H₃O⁺) = x.", "برافو: كل A H تفاعل، كيتكون H trois O plus واحد: x."),
     "2-*": (False, "H₃O⁺ est un produit : il part de 0 et augmente.", "لا، H trois O plus هو produit: كيبدا من zéro وكيزيد."),
     "3-c": (True, "Oui : à l'état final, x vaut x_f : n(AH) = C·V − x_f.", "برافو: فl'état final، x كتولي x f: C V moins x f."),
     "3-d": (False, "Presque : c'est l'expression en cours. À l'état final, x prend une valeur précise.", "قريب: هادي ديال en cours. فl'état final، x كتولي x f."),
     "3-*": (False, "À l'état final, l'acide a perdu ce qui a réagi.", "لا، فl'état final l'acide نقص منو اللي تفاعل.")},
    ("(1 ; a) (2 ; b) (3 ; c) : AH part de C·V et perd x ; H₃O⁺ part de 0 et gagne x.",
     "A H كيبدا من C fois V وكينقص ب x، و H trois O plus كيبدا من zéro وكيزيد ب x.")),
  qcm("fa_3", "Plus facile : pH si totale", "سؤال ساهل على le p H.",
      f"Si la réaction était totale, [H₃O⁺] = C = {sci(C, 1)} mol/L. Le pH serait…",
      [f"{fr(PHT)}", f"{fr(PH)}", f"{fr(-PHT)}"], 0, {
        0: ("juste", f"برافو! p H égale moins log de C، يعني {d(PHT)}.", f"Juste : pH = −log({sci(C, 1)}) = {fr(PHT)}."),
        1: (("لا، هادا هو le p H اللي قسنا. السؤال على le p H يلا كانت totale. عاود اختار.", "Ça, c'est le pH mesuré. Réessaie."),
            (f"الجواب: {d(PHT)}، moins log de C. و le p H المقاس كبر منو.", f"Réponse : pH = −log C = {fr(PHT)}.")),
        2: (("نسيتي le signe moins: le p H ديال محلول acide موجب. عاود اختار.", "Tu as oublié le signe moins de −log. Réessaie."),
            (f"الجواب: {d(PHT)}، p H égale moins log de C.", f"Réponse : pH = −log C = {fr(PHT)}."))},
      f"Si la réaction était totale, la concentration des ions H trois O plus égale C, {ds(C, 1)} mole par litre. Le p H serait ?"),
  vf("fa_4", "Plus facile : les étapes de la démonstration", "τ = 10^(−pH)/C, étape par étape.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("On part de la définition τ = x_f/x_max.", True, "Une démonstration de τ part toujours de sa définition."),
      ("x_f = C·V.", False, "C·V est x_max ; x_f vient de la mesure : x_f = [H₃O⁺]·V = 10^(−pH)·V."),
      ("Le volume V se simplifie, il reste τ = 10^(−pH)/C.", True, "V est en haut et en bas de la fraction.")]),
  qcm("fa_5", "Plus facile : τ", "سؤال ساهل على tau.",
      f"pH = {fr(PH)} et C = {sci(C, 1)} mol/L. τ vaut environ…",
      [f"{fr(TAU, 3)}", "1", f"{fr(PH / (C * 1000), 2)}"], 0, {
        0: ("juste", f"برافو! tau égale dix puissance moins p H، sur C، يعني {d(TAU, 3)}. صغر من un: limitée.", f"Juste : τ = 10^(−{fr(PH)})/{sci(C, 1)} = {fr(TAU, 3)}."),
        1: (("لا، tau égale un يعني la réaction totale. ولكن le p H المقاس ماشي هو ديال totale. عاود اختار.", "τ = 1 voudrait dire totale, ce que le pH dément. Réessaie."),
            (f"الجواب: {d(TAU, 3)}. la réaction limitée.", f"Réponse : τ = {fr(TAU, 3)}.")),
        2: (("لا، ما كنقسموش le p H. كنقسمو la concentration des ions H trois O plus، dix puissance moins p H. عاود اختار.", "On ne divise pas le pH : on divise 10^(−pH). Réessaie."),
            (f"الجواب: {d(TAU, 3)}، dix puissance moins p H، sur C.", f"Réponse : τ = 10^(−pH)/C = {fr(TAU, 3)}."))},
      f"p H égale {d(PH)} et C égale {ds(C, 1)} mole par litre. Tau vaut environ ?"),
]

SIM_Q = [
  QS("1", "Calculer la concentration C de la solution.",
     val("C", sC, "mol/L", f"n₀ = {fr(sm, 3)}/{fr(M, 0)} = {sci(sm / M, 1)} mol ; C = n₀/V = {sci(sC, 1)} mol/L"),
     (["n = m/M", "C = n/V"], ["C = m/V"]),
     [(f"n₀ = m/M = {sci(sm / M, 1)} mol ; C = n₀/V = {sci(sC, 1)} mol/L", "C égale n zéro sur V")],
     f"n zéro égale m sur M، يعني {ds(sm / M, 1)} mole. C égale n zéro sur V، يعني {ds(sC, 1)} mole par litre."),
  QS("2", "Écrire l'équation de la réaction de AH avec l'eau et dresser le tableau d'avancement.",
     phrase(EQ + " ; " + TAB), (["⇌", "C·V − x", "x_f"], ["→"]),
     [(EQ, "l'équation"), (TAB, "le tableau")],
     f"l'équation: {EQ_DIT}. le tableau: C fois V، الما en excès، zéro و zéro، ومن بعد C V moins x، و x، و x."),
  QS("3", f"pH mesuré = {fr(sPH)}. Calculer le pH si la réaction était totale et conclure.",
     val("pH", sPHT, None, f"si totale : pH = −log C = {fr(sPHT)} ; {fr(sPH)} > {fr(sPHT)} : non totale"),
     (["pH = −log C"], ["pH = log C"]),
     [(f"pH = −log({sci(sC, 1)}) = {fr(sPHT)} < {fr(sPH)} : réaction non totale", "moins log de C")],
     f"يلا totale، p H égale moins log de C، يعني {d(sPHT)}. le p H المقاس {d(sPH)}، كبر: la réaction ماشي totale."),
  QS("4", "Montrer que τ = 10^(−pH)/C.",
     phrase("τ = x_f/x_max = 10^(−pH)·V/(C·V) = 10^(−pH)/C"), (["τ = x_f/x_max", "x_max = C·V"], ["x_f = C·V"]),
     [("τ = x_f/x_max = 10^(−pH)·V/(C·V) = 10^(−pH)/C", "tau égale x f sur x max")],
     "tau égale x f sur x max. x f égale dix puissance moins p H fois V، و x max égale C fois V. V كيتحيد: tau égale dix puissance moins p H، sur C."),
  QS("5", "Calculer τ et conclure.",
     val("τ", sTAU, None, f"τ = 10^(−{fr(sPH)})/{sci(sC, 1)} = {fr(sTAU, 3)} < 1 : limitée"),
     (["τ = 10^(−pH)/C"], ["τ = 10^(pH)/C"]),
     [(f"τ = {fr(sTAU, 3)} < 1 : réaction limitée", f"tau égale {d(sTAU, 3)}")],
     f"tau égale {d(sTAU, 3)}. صغر من un: la réaction limitée."),
]

EX = exercice(
  "phys_ex_ch11_deux_sens_3", "phys_ch11_transformations_deux_sens", "transformations_deux_sens",
  "L'acide lactique : tableau d'avancement, pH et taux d'avancement final", "moyen", 25,
  ["Calculer C à partir d'une masse dissoute", "Écrire l'équation et dresser le tableau d'avancement",
   "Comparer le pH mesuré au pH d'une réaction totale", "Montrer que τ = 10^(−pH)/C", "Calculer τ et conclure"],
  f"L'acide lactique, noté AH (formule brute C₃H₆O₃), se forme dans les muscles et dans le lait qui tourne. On dissout une masse m = {fr(m, 3)} g d'acide lactique dans de l'eau distillée et on obtient un volume V = {fr(V * 1000, 0)} mL d'une solution S. À 25 °C, le pH de S vaut {fr(PH)}.",
  f"دابا نقراو l'énoncé. l'acide lactique، نسميوه A H، كيتكون فالعضلات وفالحليب ملي كيحماض. كنذوبو {d(m, 3)} gramme منو فالما، وكنلقاو {d(V * 1000, 0)} millilitres ديال المحلول S. le p H ديال S égale {d(PH)}.",
  [],
  [f"m = {fr(m, 3)} g ; M(AH) = {fr(M, 0)} g/mol", f"V = {fr(V * 1000, 0)} mL", f"pH = {fr(PH)} (25 °C)", "Couple : AH(aq) / A⁻(aq)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  f"On dissout m = {fr(sm, 3)} g d'acide lactique AH (M = {fr(M, 0)} g/mol) dans l'eau ; on obtient V = {fr(sV * 1000, 0)} mL de solution, de pH = {fr(sPH)} à 25 °C.",
  f"نفس التمرين، بقيم أخرى. {d(sm, 3)} gramme ديال l'acide lactique ف {d(sV * 1000, 0)} millilitres، و p H égale {d(sPH)}.",
  [], [f"m = {fr(sm, 3)} g ; M = {fr(M, 0)} g/mol", f"V = {fr(sV * 1000, 0)} mL", f"pH = {fr(sPH)}"],
  SIM_Q)

ecrire(EX)
