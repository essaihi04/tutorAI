# Exercice de chimie, ch. 10 (suivi temporel, vitesse de réaction), niveau facile : s'entraîner aux gestes un par un
# (n = C·V, x_max et réactif limitant, lecture de t½).
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2016 R (2.3.2 t½ en minutes), 2019 R (II.3 x_max, II.5 t½ graphique),
#    2021 N (1 tableau + x_f, 2.1 définir t½), 2024 N (2 t½ graphique), 2025 N (2.4 t½) — backend/data/exams/physique ;
#  - profs (architecture/sources_chimie_ch9_ch11.md, chapitre B : Mahajar-Tabit, El Founani, Sbiro, Hadjyne,
#    Boulouiha ; vidéos Noureddine Physique, El Omrani, TOP PHYSIQUE CHIMIE, Driss DOTCOM, Prof Oualid) :
#    S₂O₈²⁻ + I⁻ suivi par dosage, x_max recalculé à chaque activité, t½ lu à x_f/2 ; piège : lire x_max/2 d'une
#    réaction non totale, oublier l'unité de l'axe ;
#  - séries en ligne : talamidi (suivi temporel, séries 1 corrigée et 2), moutamadris (exercices suivi temporel 2022),
#    alloschool (élément 119798), coursdusoirpc (TD B. Mouslim), dreamjob (exercices corrigés suivi temporel).
# Ici : nos propres volumes et concentrations, notre propre courbe (calculée, modèle d'ordre un, t½ = 5 min).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *

C1, V1 = 0.20, 50e-3          # iodure de potassium
C2, V2 = 0.040, 50e-3         # peroxodisulfate de sodium
n1, n2 = C1 * V1, C2 * V2     # 1,0e-2 et 2,0e-3 mol
XMAX = min(n2, n1 / 2)        # 2,0e-3 mol
T12 = 5.0                     # min (lu sur la courbe)
assert abs(n2 - 2.0e-3) < 1e-12 and abs(XMAX - 2.0e-3) < 1e-12

_, EXPR = x_ordre1(XMAX * 1e3, T12)
FIG = courbe_fig("Évolution de l'avancement x au cours du temps",
    ((0, 40, "t", "min", [0, 5, 10, 15, 20, 25, 30, 35, 40]), (0, 2.4, "x", "mmol", [0, 0.4, 0.8, 1.0, 1.2, 1.6, 2.0, 2.4])),
    [{"f": "courbe", "expr": EXPR, "de": 0, "a": 40, "couleur": "cyan", "texte": "x(t)", "texte_x": 30, "pos": "s"},
     {"f": "repere", "y": 2.0, "couleur": "faible"}],
    legende="La courbe monte vite au début puis atteint un palier.")

# similaire : 0,30 mol/L × 40 mL d'iodure, 0,050 mol/L × 40 mL de peroxodisulfate ; t½ = 10 min
sC1, sV1, sC2, sV2, sT12 = 0.30, 40e-3, 0.050, 40e-3, 10.0
sn1, sn2 = sC1 * sV1, sC2 * sV2       # 1,2e-2 et 2,0e-3
sX = min(sn2, sn1 / 2)
assert abs(sn2 - 2.0e-3) < 1e-12 and abs(sX - 2.0e-3) < 1e-12
_, sEXPR = x_ordre1(sX * 1e3, sT12)
sFIG = courbe_fig("Évolution de l'avancement x au cours du temps",
    ((0, 80, "t", "min", [0, 10, 20, 30, 40, 50, 60, 70, 80]), (0, 2.4, "x", "mmol", [0, 0.4, 0.8, 1.0, 1.2, 1.6, 2.0, 2.4])),
    [{"f": "courbe", "expr": sEXPR, "de": 0, "a": 80, "couleur": "cyan", "texte": "x(t)", "texte_x": 60, "pos": "s"},
     {"f": "repere", "y": 2.0, "couleur": "faible"}])

QUESTIONS = [
  Q("1", "Calculer la quantité de matière initiale n₂ des ions peroxodisulfate S₂O₈²⁻.",
    "السؤال un: حسب la quantité de matière initiale n deux ديال les ions peroxodisulfate.",
    val("n₂", n2, "mol", "n₂ = C₂·V₂ = 0,040 × 50 × 10⁻³ = 2,0 × 10⁻³ mol"),
    (["n = C·V", "C₂", "V₂", "10⁻³", "mol"], ["n = C/V", "V₂ = 50 L"]),
    [("La solution contient C₂ mole par litre, et on en verse V₂ : quelle relation lie n, C et V ? Attention à l'unité du volume.",
      "عندك la concentration C deux، يعني شحال من mole فكل litre، وعندك le volume V deux. شنو la relation بين n و C و V؟ ورد البال للوحدة ديال le volume."),
     ("n₂ = C₂·V₂, avec V₂ en litres : 50 mL = 50 × 10⁻³ L.",
      "n deux égale C deux fois V deux. ولكن V deux خاصو يكون ب litre: cinquante millilitres égale cinquante fois dix puissance moins trois litre.")],
    [("1 : n₂ = C₂·V₂", "n deux égale C deux fois V deux"),
     ("n₂ = 0,040 × 50 × 10⁻³", "zéro virgule zéro quarante fois cinquante fois dix puissance moins trois"),
     ("n₂ = 2,0 × 10⁻³ mol", "n deux égale deux virgule zéro fois dix puissance moins trois mole")],
    "السؤال un. n deux égale C deux fois V deux، و le volume ب litre. l'application numérique: zéro virgule zéro quarante fois cinquante fois dix puissance moins trois. n deux égale deux virgule zéro fois dix puissance moins trois mole.",
    "ex_1", "fa_1"),
  Q("2", "La quantité initiale des ions iodure est n₁ = 1,0 × 10⁻² mol. À l'aide du tableau d'avancement, déterminer l'avancement maximal x_max et le réactif limitant.",
    "السؤال deux: la quantité initiale ديال les ions iodure هي n un égale un virgule zéro fois dix puissance moins deux mole. بالتابلو ديال l'avancement، حدد x max و le réactif limitant.",
    val("x_max", XMAX, "mol", "S₂O₈²⁻ limitant : x_max = n₂ = 2,0 × 10⁻³ mol"),
    (["n₁ − 2x_max = 0", "n₂ − x_max = 0", "x_max", "limitant", "mol"], ["n₁ − x_max = 0", "x_max = 5,0 × 10⁻³ mol"]),
    [("Dans l'état final, chaque réactif peut être épuisé : écris les deux hypothèses avec les coefficients de l'équation (2 devant I⁻).",
      "فl'état final، كل réactif يقدر يتسالى. كتب deux hypothèses، ورد البال: قدام les ions iodure كاين le coefficient deux."),
     ("Hypothèse 1 : n₂ − x_max = 0. Hypothèse 2 : n₁ − 2x_max = 0. On garde la plus petite valeur.",
      "l'hypothèse un: n deux moins x max égale zéro. l'hypothèse deux: n un moins deux x max égale zéro. وكناخدو الصغيرة.")],
    [("2 : si S₂O₈²⁻ est limitant : n₂ − x_max = 0 donc x_max = 2,0 × 10⁻³ mol", "l'hypothèse un"),
     ("si I⁻ est limitant : n₁ − 2x_max = 0 donc x_max = 5,0 × 10⁻³ mol", "l'hypothèse deux"),
     ("on garde la plus petite : x_max = 2,0 × 10⁻³ mol, S₂O₈²⁻ est le réactif limitant", "الصغيرة")],
    "السؤال deux. l'hypothèse un: les ions peroxodisulfate كيتسالاو، n deux moins x max égale zéro، إذن x max égale deux virgule zéro fois dix puissance moins trois mole. l'hypothèse deux: les ions iodure كيتسالاو، n un moins deux x max égale zéro، إذن x max égale cinq virgule zéro fois dix puissance moins trois mole. كناخدو الصغيرة: x max égale deux virgule zéro fois dix puissance moins trois mole، و les ions peroxodisulfate هوما le réactif limitant.",
    "ex_2", "fa_2"),
  Q("3", "La réaction est totale. Définir le temps de demi-réaction t½, puis le déterminer graphiquement.",
    "السؤال trois: la réaction totale. عرف le temps de demi-réaction t un demi، ومن بعد حددو على la courbe.",
    val("t½", T12, "min", "t½ : date où x = x_f/2 = 1,0 mmol ; t½ = 5 min", tol=0.06),
    (["x = x_f/2", "x_f = x_max", "t½", "min"], ["x = x_f", "t½ = t_f/2"]),
    [("t½ est une date : celle où l'avancement atteint la moitié de sa valeur finale. Quelle est x_f ici ?",
      "t un demi هي واحد la date: اللحظة اللي كيوصل فيها l'avancement لنص ديال la valeur finale ديالو. شحال هي x f هنا؟"),
     ("Réaction totale : x_f = x_max = 2,0 mmol. Place x_f/2 = 1,0 mmol sur l'axe des x, va horizontalement jusqu'à la courbe, puis descends sur l'axe des temps.",
      "la réaction totale، إذن x f égale x max égale deux virgule zéro millimoles. حط x f sur deux égale un virgule zéro millimole على l'axe des x، سير horizontale حتى ل la courbe، ومن بعد هبط verticale ل l'axe du temps.")],
    [("3 : t½ est la durée au bout de laquelle x = x_f/2", "t un demi هي la durée"),
     ("x_f = x_max = 2,0 mmol, donc x_f/2 = 1,0 mmol", "x f sur deux égale un virgule zéro millimole"),
     ("lecture graphique : t½ = 5 min", "t un demi égale cinq minutes")],
    "السؤال trois. t un demi هي la durée اللي كيوصل فيها l'avancement ل la moitié ديال l'avancement final. la réaction totale، إذن x f égale x max égale deux virgule zéro millimoles، و x f sur deux égale un virgule zéro millimole. على la courbe: t un demi égale cinq minutes.",
    "ex_3", "fa_3"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : la quantité de matière n = C·V",
      "La concentration dit combien de moles il y a dans chaque litre : n = C·V, avec V en litres.",
      "cinetique-tableau/prerequis.html?vue=concentration", "Le même soluté dans deux volumes",
      "شوف هاد le soluté: n égale deux virgule zéro millimoles. كنحطوه ف cent millilitres ديال الما. la concentration هي شحال من soluté كاين ف كل litre. la relation: C égale n sur V. وبالعكس: n égale C fois V. فالتمرين ديالنا: C deux égale zéro virgule zéro quarante mole par litre، و V deux égale cinquante millilitres، يعني cinquante fois dix puissance moins trois litre. إذن n deux égale C deux fois V deux، يعني deux virgule zéro fois dix puissance moins trois mole.",
      [("n₂ = C₂·V₂", "إذن n deux égale C deux fois V deux"), ("n₂ = 0,040 × 50 × 10⁻³ = 2,0 × 10⁻³ mol", "يعني deux virgule zéro fois dix puissance moins trois mole")],
      [("شوف هاد le soluté", "moment:solute"), ("كنحطوه ف cent millilitres", "moment:dissoudre"),
       ("la relation: C égale n sur V", "moment:relation"), ("وبالعكس: n égale C fois V", "moment:n_cv")]),
  sim("ex_2", "Question 2 : deux hypothèses, on garde la plus petite",
      "Chaque réactif peut s'épuiser : x_max est la plus petite des deux valeurs.",
      "cinetique-tableau/limitant.html", "Les deux hypothèses du réactif limitant",
      "شوف هاد المثال ديال le cours: l'eau oxygénée، deux virgule zéro millimoles، و les ions iodure، dix virgule zéro millimoles. كنديرو deux hypothèses. l'hypothèse un كتعطي x max égale deux virgule zéro millimoles. l'hypothèse deux، مع le coefficient deux، كتعطي cinq virgule zéro millimoles. كناخدو الصغيرة. فالتمرين ديالنا نفس الخدمة: n deux moins x max égale zéro كتعطي deux virgule zéro fois dix puissance moins trois mole، و n un moins deux x max égale zéro كتعطي cinq virgule zéro fois dix puissance moins trois mole. إذن x max égale deux virgule zéro fois dix puissance moins trois mole، و les ions peroxodisulfate هوما le réactif limitant.",
      [("n₂ − x_max = 0 ou n₁ − 2x_max = 0", "فالتمرين ديالنا نفس الخدمة"), ("x_max = 2,0 × 10⁻³ mol ; S₂O₈²⁻ limitant", "هوما le réactif limitant")],
      [("شوف هاد المثال ديال le cours", "moment:tableau"), ("l'hypothèse un كتعطي", "moment:hypothese_1"),
       ("l'hypothèse deux، مع le coefficient deux", "moment:hypothese_2"), ("كناخدو الصغيرة", "moment:plus_petite"),
       ("إذن x max égale deux virgule zéro fois dix puissance moins trois mole", "moment:limitant")]),
  sim("ex_3", "Question 3 : lire t½ en quatre gestes",
      "x_f sur le palier, x_f/2 sur l'axe des x, horizontale jusqu'à la courbe, verticale jusqu'à l'axe des temps.",
      "cinetique-tableau/demi-reaction.html?vue=lecture", "La lecture de t½ sur la courbe x(t)",
      "t un demi كنقراوها ب quatre خطوات. اللولة: x f، على le palier. الثانية: x f sur deux، على l'axe ديال x. الثالثة: كنمشيو horizontale حتى ل la courbe. الرابعة: كنهبطو verticale حتى ل l'axe du temps. فالتمرين ديالنا: la réaction totale، x f égale deux virgule zéro millimoles، إذن x f sur deux égale un virgule zéro millimole. ومن la courbe ديال l'énoncé: t un demi égale cinq minutes.",
      [("x_f/2 = 1,0 mmol", "إذن x f sur deux égale un virgule zéro millimole"), ("t½ = 5 min", "t un demi égale cinq minutes")],
      [("اللولة: x f", "moment:x_f"), ("الثانية: x f sur deux", "moment:moitie"),
       ("الثالثة: كنمشيو horizontale", "moment:horizontale"), ("الرابعة: كنهبطو verticale", "moment:verticale"),
       ("ومن la courbe ديال l'énoncé", "moment:valeur")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : n = C·V", "نتمرنو بسؤال ساهل. اختار la bonne valeur.",
      "C₂ = 0,040 mol/L et V₂ = 50 mL. La quantité n₂ vaut…",
      ["2,0 mol", "8,0 × 10⁻⁴ mol", "2,0 × 10⁻³ mol"], 2, {
        2: ("juste", "برافو! n deux égale C deux fois V deux، مع V ب litre: deux virgule zéro fois dix puissance moins trois mole.", "Juste : n₂ = 0,040 × 0,050 = 2,0 × 10⁻³ mol."),
        0: (("ما تقلقش. ضربتي فcinquante millilitres بلا ما تحولهم. le volume خاصو يكون ب litre. عاود اختار.", "Le volume doit être en litres : 50 mL = 0,050 L. Réessaie."),
            ("الجواب هو deux virgule zéro fois dix puissance moins trois mole: cinquante millilitres هي zéro virgule zéro cinquante litre.", "Réponse : n₂ = 0,040 × 0,050 = 2,0 × 10⁻³ mol.")),
        1: (("قريب! ولكن هاد القيمة كتجي من C sur V ولا من شي قسمة. la relation هي ضرب. عاود اختار.", "On ne divise pas : n = C·V. Réessaie."),
            ("الجواب هو deux virgule zéro fois dix puissance moins trois mole، حيت n égale C fois V.", "Réponse : n = C·V = 2,0 × 10⁻³ mol."))},
      "C deux égale zéro virgule zéro quarante mole par litre et V deux égale cinquante millilitres. La quantité n deux vaut ?"),
  qcm("fa_2", "Plus facile : le réactif limitant", "سؤال ساهل على le réactif limitant.",
      "Hypothèse 1 : x_max = 2,0 × 10⁻³ mol. Hypothèse 2 : x_max = 5,0 × 10⁻³ mol. Quel est x_max ?",
      ["5,0 × 10⁻³ mol", "2,0 × 10⁻³ mol", "7,0 × 10⁻³ mol"], 1, {
        1: ("juste", "برافو! كناخدو الصغيرة: ملي يتسالى le réactif limitant، la réaction كتوقف.", "Juste : on garde la plus petite valeur, 2,0 × 10⁻³ mol."),
        0: (("ما تقلقش. يلا وصلات x ل cinq virgule zéro، واش يبقى شي حاجة من les ions peroxodisulfate؟ عاود اختار.", "À 5,0 × 10⁻³ mol, les ions S₂O₈²⁻ seraient en quantité négative. Réessaie."),
            ("الجواب هو deux virgule zéro fois dix puissance moins trois mole: ملي يتسالى le réactif limitant، la réaction كتوقف.", "Réponse : x_max = 2,0 × 10⁻³ mol, la plus petite.")),
        2: (("لا، ما كنجمعوش les deux hypothèses. كل وحدة كتقول فين كتوقف la réaction. عاود اختار.", "On n'additionne pas les hypothèses. Réessaie."),
            ("الجواب هو deux virgule zéro fois dix puissance moins trois mole: كناخدو الصغيرة.", "Réponse : la plus petite des deux, 2,0 × 10⁻³ mol."))},
      "Hypothèse un, x max égale deux virgule zéro fois dix puissance moins trois mole. Hypothèse deux, cinq virgule zéro fois dix puissance moins trois mole. Quel est x max ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "Réaction totale, x_f = 2,0 mmol.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("t½ est la date où x = x_f/2 = 1,0 mmol.", True, "C'est la définition : à t½, l'avancement vaut la moitié de l'avancement final."),
      ("t½ est la moitié de la durée de la réaction.", False, "Non : t½ se lit à x = x_f/2. La réaction n'est pas finie à 2·t½."),
      ("Ici, t½ se lit en minutes, l'unité de l'axe des temps.", True, "On écrit toujours l'unité de l'axe : t½ = 5 min.")]),
]

SIM_Q = [
  QS("1", "Calculer la quantité de matière initiale n₂ des ions peroxodisulfate.",
     val("n₂", sn2, "mol", "n₂ = C₂·V₂ = 0,050 × 40 × 10⁻³ = 2,0 × 10⁻³ mol"),
     (["n = C·V", "C₂", "V₂", "mol"], ["n = C/V"]),
     [("n₂ = C₂·V₂ = 0,050 × 40 × 10⁻³", "n deux égale C deux fois V deux"), ("n₂ = 2,0 × 10⁻³ mol", "deux virgule zéro fois dix puissance moins trois mole")],
     "n deux égale C deux fois V deux، يعني zéro virgule zéro cinquante fois quarante fois dix puissance moins trois. n deux égale deux virgule zéro fois dix puissance moins trois mole."),
  QS("2", "La quantité initiale des ions iodure est n₁ = 1,2 × 10⁻² mol. Déterminer x_max et le réactif limitant.",
     val("x_max", sX, "mol", "S₂O₈²⁻ limitant : x_max = n₂ = 2,0 × 10⁻³ mol"),
     (["n₁ − 2x_max = 0", "n₂ − x_max = 0", "mol"], ["n₁ − x_max = 0"]),
     [("n₂ − x_max = 0 : x_max = 2,0 × 10⁻³ mol ; n₁ − 2x_max = 0 : x_max = 6,0 × 10⁻³ mol", "les deux hypothèses"),
      ("x_max = 2,0 × 10⁻³ mol, S₂O₈²⁻ limitant", "x max égale deux virgule zéro fois dix puissance moins trois mole")],
     "les deux hypothèses: n deux moins x max égale zéro كتعطي deux virgule zéro fois dix puissance moins trois mole، و n un moins deux x max égale zéro كتعطي six virgule zéro fois dix puissance moins trois mole. كناخدو الصغيرة: x max égale deux virgule zéro fois dix puissance moins trois mole، و les ions peroxodisulfate هوما le réactif limitant."),
  QS("3", "La réaction est totale. Définir t½, puis le déterminer graphiquement.",
     val("t½", sT12, "min", "x_f/2 = 1,0 mmol ; t½ = 10 min", tol=0.06),
     (["x = x_f/2", "t½", "min"], ["t½ = t_f/2"]),
     [("t½ : durée au bout de laquelle x = x_f/2 = 1,0 mmol", "x égale x f sur deux"), ("t½ = 10 min", "t un demi égale dix minutes")],
     "t un demi هي la durée اللي كتولي فيها x égale x f sur deux، يعني un virgule zéro millimole. على la courbe: t un demi égale dix minutes."),
]

EX = exercice(
  "phys_ex_ch10_cinetique_1", "phys_ch10_cinetique", "cinetique",
  "Les ions iodure et les ions peroxodisulfate : x_max et t½", "facile", 15,
  ["Calculer une quantité de matière n = C·V", "Déterminer x_max et le réactif limitant", "Définir et lire t½ sur la courbe x(t)"],
  "À la date t = 0, on mélange un volume V₁ = 50 mL d'une solution d'iodure de potassium de concentration C₁ = 0,20 mol/L et un volume V₂ = 50 mL d'une solution de peroxodisulfate de sodium de concentration C₂ = 0,040 mol/L. Il se produit une réaction lente et totale, d'équation : S₂O₈²⁻(aq) + 2 I⁻(aq) → 2 SO₄²⁻(aq) + I₂(aq). Un suivi par dosage permet de tracer la courbe de l'avancement x en fonction du temps (figure).",
  "دابا نقراو l'énoncé. فt égale zéro، كنخلطو cinquante millilitres ديال l'iodure de potassium، la concentration ديالو zéro virgule vingt mole par litre، مع cinquante millilitres ديال le peroxodisulfate de sodium، la concentration ديالو zéro virgule zéro quarante mole par litre. كتوقع réaction بطيئة و totale: les ions peroxodisulfate، plus deux ions iodure، كيعطيو deux ions sulfate، plus le diiode. بle dosage، رسمنا la courbe ديال l'avancement x en fonction du temps.",
  [FIG],
  ["V₁ = 50 mL ; C₁ = 0,20 mol/L (ions iodure I⁻)", "V₂ = 50 mL ; C₂ = 0,040 mol/L (ions peroxodisulfate S₂O₈²⁻)",
   "n₁(I⁻) = 1,0 × 10⁻² mol (question 2)", "Équation : S₂O₈²⁻ + 2 I⁻ → 2 SO₄²⁻ + I₂"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "À t = 0, on mélange V₁ = 40 mL d'iodure de potassium à C₁ = 0,30 mol/L et V₂ = 40 mL de peroxodisulfate de sodium à C₂ = 0,050 mol/L. Même réaction lente et totale : S₂O₈²⁻ + 2 I⁻ → 2 SO₄²⁻ + I₂. La figure donne x en fonction du temps.",
  "نفس التمرين، بقيم أخرى. كنخلطو quarante millilitres ديال l'iodure de potassium، zéro virgule trente mole par litre، مع quarante millilitres ديال le peroxodisulfate، zéro virgule zéro cinquante mole par litre. la figure كتعطي x en fonction du temps.",
  [sFIG],
  ["V₁ = 40 mL ; C₁ = 0,30 mol/L", "V₂ = 40 mL ; C₂ = 0,050 mol/L", "n₁(I⁻) = 1,2 × 10⁻² mol"],
  SIM_Q)

ecrire(EX)
