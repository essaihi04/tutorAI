# Exercice de chimie, ch. 10 (suivi temporel, vitesse de réaction), niveau moyen (celui du national) : suivi par
# dosage après trempe ; rôle de l'eau glacée, x_max, « montrer que » x = C'·V_E·V/(2·V_p), t½ lu, v(t½).
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2017 R (1 objectif de l'eau glacée avant le dosage), 2019 R (II.3 x_max,
#    II.4 v par la tangente, II.5 t½), 2021 N (1 tableau + x_f, 2.1 définir t½), 2024 N (2 t½, 3 v à t₁) —
#    backend/data/exams/physique ;
#  - profs : architecture/sources_chimie_ch9_ch11.md, chapitre B (Mahajar-Tabit, Sbiro, El Goufifa : dosage de I₂ par
#    le thiosulfate après trempe, empois d'amidon ; Boulouiha : H₂O₂ + I⁻) et phys_ch10_cinetique.md (pièges : le
#    prélèvement n'est qu'une partie du mélange, facteur V/V_p ; n(I₂) = n_E/2, pas n_E) ;
#  - séries en ligne (titres et résumés lus par recherche ; PDF non ouverts, réseau du conteneur limité) :
#    talamidi (série 1 corrigée : oxydoréduction suivie par dosage du diiode), moutamadris (suivi temporel 2022),
#    alloschool (élément 119798), coursdusoirpc (TD B. Mouslim : vitesse de formation du diiode), pc1.ma.
# Ici : nos propres quantités (le cours prend 2,0 et 10,0 mmol dans 100 mL : pas ici), notre courbe (calculée,
# modèle d'ordre un, t½ = 8 min) et notre tangente.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *

# ------------------------------------------------------------------ données
V, VP = 200e-3, 10e-3                 # L
N_H2O2, N_I = 3.0e-3, 2.0e-2          # mol
CT = 0.010                            # mol/L thiosulfate
XMAX = min(N_H2O2, N_I / 2)
assert abs(XMAX - 3.0e-3) < 1e-12
VE1 = 12.0e-3
X1 = CT * VE1 * V / (2 * VP)          # 1,2e-3 mol
assert abs(X1 - 1.2e-3) < 1e-12
VEF = 2 * XMAX * VP / V / CT          # 30 mL à la fin
assert abs(VEF - 30e-3) < 1e-12
XF, T12 = 3.0, 8.0                    # mmol, min
x, EXPR = x_ordre1(XF, T12)
p8 = pente_ordre1(XF, T12, 8)
yC, yD = x(8) - 8 * p8, x(8) + 12 * p8
assert round(yC, 2) == 0.46 and round(yD, 2) == 3.06
V8 = (3.06 - 0.46) / 20 / 0.200       # 0,65 mmol·L⁻¹·min⁻¹
assert abs(V8 - 0.65) < 1e-9

def figX(xf, t12, tmax, gx, gy, tc, C, D, expr):
    return courbe_fig("Avancement x en fonction du temps", ((0, tmax, "t", "min", gx), (0, gy[-1], "x", "mmol", gy)),
        [{"f": "courbe", "expr": expr, "de": 0, "a": tmax, "couleur": "cyan", "texte": "x(t)", "texte_x": tmax * 0.85, "pos": "s"},
         {"f": "courbe", "expr": f"{(D[1]-C[1])/(D[0]-C[0]):.6f}*x+{C[1]}", "de": 0, "a": D[0], "couleur": "orange", "trait": "pointille"},
         {"f": "point", "at": list(C), "t": f"C (0 ; {fr(C[1], 2)})", "pos": "e", "couleur": "orange"},
         {"f": "point", "at": list(D), "t": f"D ({D[0]} ; {fr(D[1], 2)})", "pos": "n", "couleur": "orange"},
         {"f": "point", "at": [tc, round(xf / 2, 3)], "couleur": "orange"}],
        legende=f"(T) : tangente à la courbe au point d'abscisse t = {tc} min ; coordonnées en (min ; mmol).")

FIG = figX(XF, T12, 48, [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48], [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5], 8, (0, 0.46), (20, 3.06), EXPR)

# ------------------------------------------------------------------ similaire
sN_H2O2, sCT, sVE1, sT12 = 4.0e-3, 0.020, 8.0e-3, 6.0
sX = min(sN_H2O2, N_I / 2)
sX1 = sCT * sVE1 * V / (2 * VP)
assert abs(sX1 - 1.6e-3) < 1e-12
sx, sE = x_ordre1(4.0, sT12)
sp = pente_ordre1(4.0, sT12, 6)
syC, syD = sx(6) - 6 * sp, sx(6) + 10 * sp
assert round(syC, 2) == 0.61 and round(syD, 2) == 4.31
sV6 = (4.31 - 0.61) / 16 / 0.200        # 1,156
sFIG = figX(4.0, sT12, 36, [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36], [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5], 6, (0, 0.61), (16, 4.31), sE)

QUESTIONS = [
  Q("1", "Avant chaque dosage, le prélèvement est versé dans de l'eau glacée. Expliquer le rôle de cette opération.",
    "السؤال un: قبل كل dosage، كنحطو le prélèvement فالما البارد بزاف. فسر شنو الدور ديال هاد العملية.",
    phrase("C'est une trempe : le refroidissement (température plus basse) et la dilution (concentrations plus faibles) ralentissent fortement la réaction, qui est pratiquement bloquée ; on dose le diiode présent à la date du prélèvement."),
    (["trempe", "température", "dilution", "facteurs cinétiques", "bloquer"], ["catalyseur", "arrêter le dosage"]),
    [("Pendant le dosage, qui dure un moment, la réaction continuerait à former du diiode. Quels facteurs cinétiques l'eau glacée modifie-t-elle ?",
      "فوقت le dosage، la réaction غادي تبقى تكوّن le diiode. شمن facteurs cinétiques كيبدل الما البارد؟"),
     ("Elle refroidit (la température baisse) et elle dilue (les concentrations baissent) : deux facteurs cinétiques qui ralentissent la réaction.",
      "كيبرد، la température كتهبط، و كيزيد الما، la concentration كتنقص. deux facteurs cinétiques اللي كيبطؤو la réaction.")],
    [("1 : c'est une trempe : on refroidit et on dilue le prélèvement", "هادي هي la trempe"),
     ("la température et la concentration (facteurs cinétiques) diminuent : la réaction est pratiquement bloquée", "deux facteurs cinétiques"),
     ("on dose ainsi le diiode formé à la date du prélèvement", "on bloque la réaction")],
    "السؤال un. هادي هي la trempe. الما البارد كيبرد le prélèvement وكيزيد فيه الما: la température و la concentration كينقصو، و هوما deux facteurs cinétiques. إذن la réaction كتولي بطيئة بزاف: on bloque la réaction، باش نعايرو le diiode اللي كان فداك la date.",
    "ex_1", "fa_1"),
  Q("2", "Déterminer l'avancement maximal x_max et le réactif limitant.",
    "السؤال deux: حدد x max و le réactif limitant.",
    val("x_max", XMAX, "mol", "H₂O₂ limitant : x_max = n₀(H₂O₂) = 3,0 × 10⁻³ mol"),
    (["n₀(H₂O₂) − x_max = 0", "n₀(I⁻) − 2x_max = 0", "mol"], ["n₀(I⁻) − x_max = 0", "x_max = 1,0 × 10⁻² mol"]),
    [("Les ions H₃O⁺ sont en excès : deux réactifs seulement peuvent s'épuiser. Attention au coefficient 2 devant I⁻.",
      "les ions H trois O plus en excès، إذن غير deux réactifs يقدرو يتسالاو. ورد البال للcoefficient deux قدام les ions iodure."),
     ("Hypothèse 1 : 3,0 × 10⁻³ − x_max = 0. Hypothèse 2 : 2,0 × 10⁻² − 2x_max = 0. On garde la plus petite.",
      "l'hypothèse un: trois virgule zéro fois dix puissance moins trois moins x max égale zéro. l'hypothèse deux: deux virgule zéro fois dix puissance moins deux، moins deux x max، égale zéro. كناخدو الصغيرة.")],
    [("2 : si H₂O₂ limitant : x_max = 3,0 × 10⁻³ mol ; si I⁻ limitant : x_max = 1,0 × 10⁻² mol", "deux hypothèses"),
     ("x_max = 3,0 × 10⁻³ mol, l'eau oxygénée est le réactif limitant", "l'eau oxygénée هي le réactif limitant")],
    "السؤال deux. deux hypothèses: l'eau oxygénée كتعطي trois virgule zéro fois dix puissance moins trois mole، و les ions iodure كيعطيو un virgule zéro fois dix puissance moins deux mole. كناخدو الصغيرة: x max égale trois virgule zéro fois dix puissance moins trois mole، و l'eau oxygénée هي le réactif limitant.",
    "ex_2", "fa_2"),
  Q("3", "Montrer que l'avancement à la date du prélèvement s'écrit x = C'·V_E·V/(2·V_p), puis calculer x à la date t₁ où V_E = 12,0 mL.",
    "السؤال trois: بين أن x égale C prime fois V E fois V، sur deux V p. ومن بعد حسب x à t un، فين V E égale douze virgule zéro millilitres.",
    val("x(t₁)", X1, "mol", "x = C'·V_E·V/(2·V_p) = 0,010 × 12,0 × 10⁻³ × 200/(2 × 10) = 1,2 × 10⁻³ mol"),
    (["n(I₂) = x", "n(I₂)/1 = n_E/2", "n_E = C'·V_E", "V/V_p", "mol"], ["n(I₂) = n_E", "x = C'·V_E"]),
    [("Dans le prélèvement, à l'équivalence : n_p(I₂) = C'·V_E/2. Mais le prélèvement n'est qu'une partie du mélange : combien de fois V_p dans V ?",
      "فle prélèvement، عند l'équivalence: n de I deux égale C prime fois V E sur deux. ولكن le prélèvement غير جزء من le mélange: شحال من مرة V p فV؟"),
     ("Dans tout le mélange : n(I₂) = (V/V_p)·C'·V_E/2, et le tableau donne n(I₂) = x.",
      "فle mélange كامل: n de I deux égale V sur V p، fois C prime V E sur deux. و le tableau كيعطي n de I deux égale x.")],
    [("3 : à l'équivalence n_p(I₂) = C'·V_E/2 ; dans le mélange n(I₂) = (V/V_p)·C'·V_E/2 et n(I₂) = x", "n de I deux égale C prime fois V E sur deux"),
     ("donc x = C'·V_E·V/(2·V_p)", "إذن x égale C prime fois V E fois V"),
     ("x(t₁) = 0,010 × 12,0 × 10⁻³ × 200/(2 × 10) = 1,2 × 10⁻³ mol", "x de t un égale un virgule deux fois dix puissance moins trois mole")],
    "السؤال trois. عند l'équivalence، un diiode لكل deux ions thiosulfate، إذن فle prélèvement: n de I deux égale C prime fois V E sur deux. le mélange فيه V sur V p، يعني vingt prélèvements. و من le tableau، n de I deux égale x. إذن x égale C prime fois V E fois V، sur deux V p. l'application numérique: zéro virgule zéro dix، fois douze virgule zéro fois dix puissance moins trois، fois vingt، sur deux. x de t un égale un virgule deux fois dix puissance moins trois mole.",
    "ex_3", "fa_3"),
  Q("4", "La transformation est totale. Déterminer graphiquement le temps de demi-réaction t½.",
    "السؤال quatre: la transformation totale. حدد على la courbe t un demi.",
    val("t½", T12, "min", "x_f/2 = x_max/2 = 1,5 mmol ; t½ = 8 min", tol=0.06),
    (["x(t½) = x_f/2", "x_f = x_max", "t½", "min"], ["t½ = t_f/2", "x(t½) = x_max"]),
    [("Transformation totale : x_f = x_max = 3,0 mmol. Cherche la date où x vaut la moitié.",
      "la transformation totale: x f égale x max égale trois virgule zéro millimoles. قلب على la date فين x كتسوى la moitié."),
     ("x_f/2 = 1,5 mmol sur l'axe des x, horizontale jusqu'à la courbe, verticale jusqu'à l'axe des temps.",
      "x f sur deux égale un virgule cinq millimole على l'axe des x، horizontale حتى ل la courbe، ومن بعد verticale ل l'axe du temps.")],
    [("4 : x_f = x_max = 3,0 mmol, donc x(t½) = x_f/2 = 1,5 mmol", "x f sur deux égale un virgule cinq millimole"),
     ("lecture graphique : t½ = 8 min", "t un demi égale huit minutes")],
    "السؤال quatre. la transformation totale، إذن x f égale x max égale trois virgule zéro millimoles، و x f sur deux égale un virgule cinq millimole. على la courbe: t un demi égale huit minutes.",
    "ex_4", "fa_4"),
  Q("5", "La droite (T) est la tangente à la courbe au point d'abscisse t½. Calculer la vitesse volumique v(t½) en mmol·L⁻¹·min⁻¹.",
    "السؤال cinq: la droite T هي la tangente à t un demi. حسب la vitesse volumique v de t un demi، ب millimole par litre et par minute.",
    val("v(t½)", V8, "mmol·L⁻¹·min⁻¹", "v(t½) = (1/V)·(dx/dt) = (1/0,200) × (3,06 − 0,46)/(20 − 0) = 0,65 mmol·L⁻¹·min⁻¹", tol=0.05),
    (["v = (1/V)·dx/dt", "(T)", "C", "D", "V = 0,200 L"], ["V = V_p", "v = x/t"]),
    [("La pente de (T) se calcule entre ses deux points C et D. Quel volume mettre dans 1/V : celui du prélèvement ou celui du mélange ?",
      "la pente ديال T كتحسبها بين C و D. و V شمن volume: ديال le prélèvement ولا ديال le mélange؟"),
     ("V est le volume du mélange réactionnel : 200 mL = 0,200 L.",
      "V هو le volume ديال le mélange réactionnel: deux cents millilitres، zéro virgule deux cents litre.")],
    [("5 : v(t½) = (1/V)·(dx/dt) au point d'abscisse t½", "v égale un sur V"),
     ("dx/dt = (3,06 − 0,46)/(20 − 0) = 0,130 mmol/min", "la pente égale zéro virgule cent trente"),
     ("v(t½) = 0,130/0,200 = 0,65 mmol·L⁻¹·min⁻¹", "v de t un demi égale zéro virgule soixante-cinq")],
    "السؤال cinq. v égale un sur V، fois d x sur d t. la pente ديال T: trois virgule zéro six moins zéro virgule quarante-six، sur vingt، la pente égale zéro virgule cent trente millimole par minute. V هو le volume ديال le mélange، zéro virgule deux cents litre. v de t un demi égale zéro virgule soixante-cinq millimole par litre et par minute.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : la trempe",
      "Refroidir et diluer le prélèvement : la réaction est bloquée pendant le dosage.",
      "cinetique-tableau/suivi.html?vue=prelevement", "Le prélèvement figé dans l'eau glacée",
      "باش نعايرو le diiode ديال واحد la date، كاين مشكل: la réaction باقا خدامة. شوف le grand bécher: كيولي brun بشوية بشوية. ب la pipette، كناخدو شوية من le mélange. ونحطوهم فالما البارد بزاف. شوف la couleur ديال le prélèvement: ما بقاتش كتبدل. وشوف le grand bécher: باقي كيولي brun. هادي هي la trempe. الما البارد كيبرد و كيزيد الما: la température و la concentration، هوما deux facteurs cinétiques. نعاود نقرا: la trempe، on bloque la réaction، pour mesurer x à cette date.",
      [("trempe : refroidissement + dilution", "هوما deux facteurs cinétiques"), ("la réaction est bloquée pendant le dosage", "on bloque la réaction")],
      [("la réaction باقا خدامة", "moment:reaction"), ("ب la pipette", "moment:prelevement"), ("ونحطوهم", "moment:eau_glacee"),
       ("شوف la couleur ديال le prélèvement", "moment:fige"), ("وشوف le grand bécher", "moment:continue"), ("هادي هي la trempe", "moment:phrase")]),
  sim("ex_2", "Question 2 : le réactif limitant",
      "Deux hypothèses ; x_max est la plus petite valeur.",
      "cinetique-tableau/limitant.html", "Les deux hypothèses du réactif limitant",
      "كنرجعو ل l'état final ديال le tableau. كنديرو deux hypothèses. l'hypothèse un: l'eau oxygénée هي اللي كتسالى. l'hypothèse deux: les ions iodure هوما اللي كيتسالاو، مع le coefficient deux. شمن وحدة ناخدو؟ الصغيرة. فالتمرين ديالنا: trois virgule zéro fois dix puissance moins trois mole، ولا un virgule zéro fois dix puissance moins deux mole. إذن x max égale trois virgule zéro fois dix puissance moins trois mole، و l'eau oxygénée هي le réactif limitant.",
      [("x_max = 3,0 × 10⁻³ mol ; H₂O₂ limitant", "و l'eau oxygénée هي le réactif limitant")],
      [("كنرجعو ل l'état final", "moment:tableau"), ("l'hypothèse un", "moment:hypothese_1"), ("l'hypothèse deux", "moment:hypothese_2"),
       ("الصغيرة", "moment:plus_petite"), ("إذن x max égale trois", "moment:limitant")]),
  sim("ex_3", "Question 3 : du volume équivalent à x",
      "n_p(I₂) = C'·V_E/2 dans le prélèvement, puis × V/V_p pour tout le mélange.",
      "cinetique-tableau/suivi.html?vue=titrage&depart=equivalence", "Le titrage du diiode par les ions thiosulfate",
      "شفنا l'équivalence. l'équation ديال le titrage: le diiode، plus deux ions thiosulfate، كيعطيو deux ions iodure و l'ion tétrathionate. عند l'équivalence، les réactifs فالنسب ديال l'équation: n de I deux sur un، égale n E sur deux. إذن n de I deux égale C fois V E sur deux، فهاد le prélèvement. فالتمرين ديالنا، le mélange فيه vingt prélèvements، و n de I deux égale x. إذن x égale C prime fois V E fois V، sur deux V p، يعني un virgule deux fois dix puissance moins trois mole.",
      [("n_p(I₂) = C'·V_E/2", "إذن n de I deux égale C fois V E sur deux"), ("x = C'·V_E·V/(2·V_p) = 1,2 × 10⁻³ mol", "يعني un virgule deux fois dix puissance moins trois mole")],
      [("شفنا l'équivalence", "moment:equivalence"), ("l'équation ديال le titrage", "moment:equation"), ("عند l'équivalence", "moment:relation")]),
  sim("ex_4", "Question 4 : t½ et ses pièges",
      "t½ se lit à partir de x_f/2 sur l'axe des x ; à 2·t½ la réaction n'est pas finie.",
      "cinetique-tableau/demi-reaction.html?vue=piege", "Deux pièges de t½",
      "شوف la courbe. هنا t un demi، cinq virgule cinq minutes، و x égale un virgule zéro millimole. دابا ناخدو deux fois t un demi: x ماشي x f. إذن à deux t un demi، la transformation n'est pas finie. والفخ الثاني: t un demi كنبداو فيه من x f sur deux sur l'axe ديال x، ماشي من الوسط ديال l'axe du temps. فالتمرين ديالنا: x f sur deux égale un virgule cinq millimole، و t un demi égale huit minutes.",
      [("x_f/2 = 1,5 mmol", "x f sur deux égale un virgule cinq millimole"), ("t½ = 8 min", "و t un demi égale huit minutes")],
      [("شوف la courbe", "moment:courbe"), ("هنا t un demi", "moment:t_demi"), ("دابا ناخدو deux fois t un demi", "moment:double"),
       ("إذن à deux t un demi", "moment:pas_fini"), ("والفخ الثاني", "moment:piege_axe")]),
  sim("ex_5", "Question 5 : la tangente à une date quelconque",
      "Plus la date est tardive, moins la tangente est raide : v diminue.",
      "cinetique-tableau/vitesse.html?vue=diminue", "Les tangentes à 0, 8 et 20 minutes",
      "شوف la courbe ديال المثال. دابا غادي نرسمو trois tangentes. اللولة à t égale zéro: طالعة بزاف. الثانية à huit minutes: أقل طالعة، v environ zéro virgule quatre-vingt-douze millimole par litre et par minute. الثالثة à vingt minutes: تقريبا plate. إذن la vitesse volumique، diminue au cours du temps. فالتمرين ديالنا: la tangente à t un demi كتدوز من C و D، la pente zéro virgule cent trente millimole par minute، و V égale zéro virgule deux cents litre. إذن v de t un demi égale zéro virgule soixante-cinq millimole par litre et par minute.",
      [("dx/dt = (3,06 − 0,46)/20 = 0,130 mmol/min", "la pente zéro virgule cent trente"), ("v(t½) = 0,130/0,200 = 0,65 mmol·L⁻¹·min⁻¹", "إذن v de t un demi égale")],
      [("شوف la courbe", "moment:courbe"), ("اللولة à t égale zéro", "moment:tangente_0"), ("الثانية à huit minutes", "moment:tangente_8"),
       ("الثالثة à vingt minutes", "moment:tangente_20"), ("إذن la vitesse volumique", "moment:conclusion")]),
]

FACILES = [
  vf("fa_1", "Plus facile : vrai ou faux", "Le prélèvement est versé dans l'eau glacée.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("L'eau glacée abaisse la température, un facteur cinétique.", True, "Plus froid : moins de chocs efficaces, la réaction ralentit."),
      ("L'eau glacée dilue le prélèvement : les concentrations diminuent.", True, "La concentration est aussi un facteur cinétique."),
      ("L'eau glacée sert à faire réagir plus vite le diiode avec les ions thiosulfate.", False, "Elle bloque la réaction étudiée ; le dosage, lui, est rapide de toute façon.")]),
  qcm("fa_2", "Plus facile : x_max", "سؤال ساهل على x max.",
      "n₀(H₂O₂) = 3,0 × 10⁻³ mol, n₀(I⁻) = 2,0 × 10⁻² mol ; H₂O₂ + 2 I⁻ + 2 H₃O⁺ → I₂ + 4 H₂O (H₃O⁺ en excès). x_max vaut…",
      ["1,0 × 10⁻² mol", "2,0 × 10⁻² mol", "3,0 × 10⁻³ mol"], 2, {
        2: ("juste", "برافو! l'hypothèse ديال l'eau oxygénée كتعطي الصغيرة.", "Juste : x_max = 3,0 × 10⁻³ mol, H₂O₂ limitant."),
        0: (("هاد القيمة ديال les ions iodure، ولكن ماشي الصغيرة. عاود اختار.", "C'est l'hypothèse « I⁻ limitant », pas la plus petite. Réessaie."),
            ("الجواب: trois virgule zéro fois dix puissance moins trois mole، الصغيرة.", "Réponse : x_max = 3,0 × 10⁻³ mol.")),
        1: (("لا، نسيتي le coefficient deux قدام les ions iodure، و هي ماشي الصغيرة. عاود اختار.", "Tu as oublié le coefficient 2, et ce n'est pas la plus petite. Réessaie."),
            ("الجواب: trois virgule zéro fois dix puissance moins trois mole.", "Réponse : x_max = 3,0 × 10⁻³ mol."))},
      "n zéro d'eau oxygénée égale trois virgule zéro fois dix puissance moins trois mole, n zéro d'ions iodure égale deux virgule zéro fois dix puissance moins deux mole. x max vaut ?"),
  qcm("fa_3", "Plus facile : le diiode du prélèvement", "سؤال ساهل على l'équivalence.",
      "À l'équivalence, on a versé n_E = C'·V_E = 1,2 × 10⁻⁴ mol d'ions thiosulfate (I₂ + 2 S₂O₃²⁻ → 2 I⁻ + S₄O₆²⁻). Dans le prélèvement, n(I₂) vaut…",
      ["6,0 × 10⁻⁵ mol", "1,2 × 10⁻⁴ mol", "2,4 × 10⁻⁴ mol"], 0, {
        0: ("juste", "برافو! un diiode لكل deux ions thiosulfate، إذن النص.", "Juste : n(I₂) = n_E/2 = 6,0 × 10⁻⁵ mol."),
        1: (("لا، deux ions thiosulfate كيتفاعلو مع diiode واحد. شوف les coefficients. عاود اختار.", "Deux ions thiosulfate pour un diiode : regarde les coefficients. Réessaie."),
            ("الجواب: six virgule zéro fois dix puissance moins cinq mole، n E sur deux.", "Réponse : n(I₂) = n_E/2.")),
        2: (("لا، ضربتي ف deux، خاصك تقسم. عاود اختار.", "On divise par 2, on ne multiplie pas. Réessaie."),
            ("الجواب: six virgule zéro fois dix puissance moins cinq mole.", "Réponse : n(I₂) = n_E/2 = 6,0 × 10⁻⁵ mol."))},
      "À l'équivalence, on a versé un virgule deux fois dix puissance moins quatre mole d'ions thiosulfate. Dans le prélèvement, la quantité de diiode vaut ?"),
  qcm("fa_4", "Plus facile : où lire t½ ?", "سؤال ساهل: فين كنقراو t un demi؟",
      "x_f = 3,0 mmol. t½ est l'abscisse du point de la courbe d'ordonnée…",
      ["1,5 mmol", "3,0 mmol", "la moitié de l'axe des temps, 24 min"], 0, {
        0: ("juste", "برافو! x f sur deux، un virgule cinq millimole.", "Juste : x(t½) = x_f/2 = 1,5 mmol."),
        1: (("لا، trois virgule zéro هي x f كاملة، le palier. خاصنا la moitié. عاود اختار.", "3,0 mmol, c'est le palier ; il faut la moitié. Réessaie."),
            ("الجواب: un virgule cinq millimole.", "Réponse : x_f/2 = 1,5 mmol.")),
        2: (("هادا هو le piège: t un demi ماشي الوسط ديال l'axe du temps. عاود اختار.", "Piège : t½ n'est pas le milieu de l'axe des temps. Réessaie."),
            ("الجواب: un virgule cinq millimole، على l'axe des x.", "Réponse : on part de x_f/2 = 1,5 mmol."))},
      "x f égale trois virgule zéro millimoles. t un demi est l'abscisse du point d'ordonnée ?"),
  qcm("fa_5", "Plus facile : quel volume ?", "سؤال ساهل: شمن volume ف un sur V؟",
      "Pour v = (1/V)·dx/dt, le volume V est…",
      ["le volume équivalent V_E = 12,0 mL", "le volume du mélange réactionnel, 200 mL", "le volume d'un prélèvement, 10 mL"], 1, {
        1: ("juste", "برافو! x هو l'avancement ديال le mélange كامل، إذن V ديال le mélange.", "Juste : x concerne tout le mélange, V = 0,200 L."),
        0: (("لا، V E هو le volume ديال le titrage. عاود اختار.", "V_E est le volume du titrage. Réessaie."),
            ("الجواب: le volume ديال le mélange، zéro virgule deux cents litre.", "Réponse : V = 200 mL = 0,200 L.")),
        2: (("لا، x كيخص le mélange كامل، ماشي le prélèvement. عاود اختار.", "x est l'avancement de tout le mélange. Réessaie."),
            ("الجواب: le volume ديال le mélange، deux cents millilitres.", "Réponse : V = 200 mL."))},
      "Pour v égale un sur V fois d x sur d t, le volume V est ?"),
]

SIM_Q = [
  QS("1", "Expliquer le rôle de l'eau glacée.",
     phrase("Trempe : refroidissement et dilution (deux facteurs cinétiques) bloquent la réaction ; on dose le diiode présent à la date du prélèvement."),
     (["trempe", "température", "dilution"], ["catalyseur"]),
     [("trempe : la température et les concentrations diminuent", "la température و la concentration"), ("la réaction est bloquée pendant le dosage", "on bloque la réaction")],
     "هادي la trempe: la température و la concentration كينقصو، إذن on bloque la réaction pendant le dosage."),
  QS("2", "Déterminer x_max et le réactif limitant.",
     val("x_max", sX, "mol", "H₂O₂ limitant : x_max = 4,0 × 10⁻³ mol"),
     (["n₀ − x_max = 0", "n₀(I⁻) − 2x_max = 0"], ["n₀(I⁻) − x_max = 0"]),
     [("hypothèses : 4,0 × 10⁻³ mol ou 1,0 × 10⁻² mol", "deux hypothèses"), ("x_max = 4,0 × 10⁻³ mol, H₂O₂ limitant", "x max égale quatre virgule zéro")],
     "deux hypothèses: quatre virgule zéro fois dix puissance moins trois، ولا un virgule zéro fois dix puissance moins deux mole. x max égale quatre virgule zéro fois dix puissance moins trois mole، l'eau oxygénée limitant."),
  QS("3", "Montrer que x = C'·V_E·V/(2·V_p), puis calculer x à la date t₁ où V_E = 8,0 mL.",
     val("x(t₁)", sX1, "mol", "x = 0,020 × 8,0 × 10⁻³ × 200/(2 × 10) = 1,6 × 10⁻³ mol"),
     (["n(I₂) = n_E/2", "V/V_p"], ["x = C'·V_E"]),
     [("n_p(I₂) = C'·V_E/2 ; n(I₂) = (V/V_p)·n_p(I₂) = x", "n de I deux égale C prime fois V E sur deux"),
      ("x(t₁) = 0,020 × 8,0 × 10⁻³ × 20/2 = 1,6 × 10⁻³ mol", "x de t un égale un virgule six")],
     "فle prélèvement، n de I deux égale C prime fois V E sur deux، و le mélange فيه vingt prélèvements. x de t un égale un virgule six fois dix puissance moins trois mole."),
  QS("4", "La transformation est totale. Déterminer graphiquement t½.",
     val("t½", sT12, "min", "x_f/2 = 2,0 mmol ; t½ = 6 min", tol=0.06),
     (["x_f/2", "t½"], ["t½ = t_f/2"]),
     [("x_f/2 = 2,0 mmol", "x f sur deux égale deux virgule zéro"), ("t½ = 6 min", "t un demi égale six minutes")],
     "x f sur deux égale deux virgule zéro millimoles. على la courbe: t un demi égale six minutes."),
  QS("5", "Calculer v(t½) à l'aide de la tangente (T), en mmol·L⁻¹·min⁻¹ (V = 200 mL).",
     val("v(t½)", sV6, "mmol·L⁻¹·min⁻¹", "v(t½) = (1/0,200) × (4,31 − 0,61)/16 ≈ 1,16 mmol·L⁻¹·min⁻¹", tol=0.05),
     (["v = (1/V)·dx/dt", "C", "D"], ["V = V_p"]),
     [("dx/dt = (4,31 − 0,61)/16 ≈ 0,231 mmol/min", "la pente"), ("v(t½) ≈ 1,16 mmol·L⁻¹·min⁻¹", "v de t un demi égale environ un virgule seize")],
     "la pente égale environ zéro virgule deux cent trente et un millimole par minute. على zéro virgule deux cents litre: v de t un demi égale environ un virgule seize millimole par litre et par minute."),
]

EX = exercice(
  "phys_ex_ch10_cinetique_5", "phys_ch10_cinetique", "cinetique",
  "L'eau oxygénée et les ions iodure : suivi par dosage après trempe", "moyen", 30,
  ["Expliquer la trempe", "Déterminer x_max", "Relier x au volume équivalent", "Lire t½", "Calculer v par la tangente"],
  "À t = 0, on prépare un mélange de volume V = 200 mL contenant n₀(H₂O₂) = 3,0 × 10⁻³ mol d'eau oxygénée, n₀(I⁻) = 2,0 × 10⁻² mol d'ions iodure et des ions H₃O⁺ en excès. La réaction lente et totale a pour équation : H₂O₂(aq) + 2 I⁻(aq) + 2 H₃O⁺(aq) → I₂(aq) + 4 H₂O(ℓ). À différentes dates, on prélève V_p = 10 mL du mélange, on le verse dans de l'eau glacée, puis on dose le diiode formé par une solution de thiosulfate de sodium de concentration C' = 0,010 mol/L (réaction du dosage : I₂ + 2 S₂O₃²⁻ → 2 I⁻ + S₄O₆²⁻). On obtient la courbe x(t) de la figure, avec la tangente (T) au point d'abscisse 8 min.",
  "دابا نقراو l'énoncé. فt égale zéro، عندنا mélange، le volume ديالو deux cents millilitres، فيه trois virgule zéro fois dix puissance moins trois mole ديال l'eau oxygénée، و deux virgule zéro fois dix puissance moins deux mole ديال les ions iodure، و les ions H trois O plus en excès. la réaction بطيئة و totale، كتعطي le diiode. فكل date، كناخدو dix millilitres، كنحطوهم فالما البارد بزاف، و كنعايرو le diiode ب le thiosulfate de sodium، zéro virgule zéro dix mole par litre. la figure كتعطي x en fonction du temps، مع la tangente T à huit minutes.",
  [FIG],
  ["V = 200 mL ; n₀(H₂O₂) = 3,0 × 10⁻³ mol ; n₀(I⁻) = 2,0 × 10⁻² mol ; H₃O⁺ en excès", "V_p = 10 mL ; C' = 0,010 mol/L (ions thiosulfate)",
   "Question 3 : V_E = 12,0 mL à la date t₁", "Tangente (T) : C(0 ; 0,46 mmol) et D(20 min ; 3,06 mmol)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Même réaction, même volume V = 200 mL, n₀(H₂O₂) = 4,0 × 10⁻³ mol, n₀(I⁻) = 2,0 × 10⁻² mol, H₃O⁺ en excès. Prélèvements de V_p = 10 mL, dosés par le thiosulfate à C' = 0,020 mol/L. À la date t₁, V_E = 8,0 mL. La figure donne x(t) et la tangente (T) au point d'abscisse 6 min.",
  "نفس التمرين، بقيم أخرى: quatre virgule zéro fois dix puissance moins trois mole ديال l'eau oxygénée، و le thiosulfate zéro virgule zéro vingt mole par litre. à t un، V E égale huit virgule zéro millilitres.",
  [sFIG],
  ["V = 200 mL ; n₀(H₂O₂) = 4,0 × 10⁻³ mol ; n₀(I⁻) = 2,0 × 10⁻² mol", "V_p = 10 mL ; C' = 0,020 mol/L ; V_E(t₁) = 8,0 mL", "(T) : C(0 ; 0,61 mmol) et D(16 min ; 4,31 mmol)"],
  SIM_Q)

ecrire(EX)
