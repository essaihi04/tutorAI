# Exercice de chimie, ch. 10 (suivi temporel, vitesse de réaction), niveau moyen (celui du national) : suivi par la
# mesure de la pression ; tableau et x_max, « montrer que » x = (P − P₀)·V/(R·T), P_max, t½ lu puis déduit, v(0).
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2016 R (2.3.1 grandeur à x_max/2, 2.3.2 t½, 2.3.3 v(0) en mol·m⁻³·min⁻¹),
#    2018 R (2.2.1 G½ quand x = x_max/2, 2.2.2 t½), 2019 R (II.3 x_max, II.4 v par la tangente, II.5 t½),
#    2021 N (2.3 « montrer que » v = …·dσ/dt) — backend/data/exams/physique ; pas de suivi par pression au national
#    2016-2025 : la forme (grandeur ½, t½, v(0)) est reprise des suivis conductimétriques ;
#  - profs : architecture/sources_chimie_ch9_ch11.md, chapitre B (Mahajar-Tabit, Sbiro, Boulouiha : Mg + HCl au
#    manomètre, x = x_max·ΔP/ΔP_max établi ; El Founani, Hadjyne : Fe + H⁺ en littéral), phys_ch10_cinetique.md
#    (pièges : P en Pa, V en m³, T en K ; P₀ = pression de l'air, qui ne réagit pas) ;
#  - séries en ligne (titres et résumés lus par recherche ; PDF non ouverts, réseau du conteneur limité) :
#    moutamadris (fiches 13-7, 13-8 : Mg + HCl, mesures de pression), talamidi (suivi temporel, séries 1 et 2,
#    activités 3), alloschool (élément 119798), coursdusoirpc (TD B. Mouslim), pc1.ma (fiches Hadjyne).
# Ici : nos propres masse, volumes et température (différents de la fiche moutamadris 0,12 g / 40 mL / 0,50 mol/L) ;
# courbe P(t) calculée (modèle d'ordre un, t½ = 4 min), tangente calculée.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *

R = 8.314
# ------------------------------------------------------------------ données
m, M = 36e-3, 24.0                  # g, g/mol
Ca, Va = 0.10, 60e-3                # acide chlorhydrique
Vg, T, P0 = 0.413e-3, 298.0, 101.3  # m³ de gaz, K, kPa
n_mg, n_h = m / M, Ca * Va          # 1,5e-3 ; 6,0e-3
XMAX = min(n_mg, n_h / 2)
assert abs(XMAX - 1.5e-3) < 1e-12 and abs(n_h / 2 - 3.0e-3) < 1e-12
DP = XMAX * R * T / Vg / 1000       # kPa
PMAX = P0 + DP                      # 110,3 kPa
assert round(DP, 1) == 9.0 and round(PMAX, 1) == 110.3
T12 = 4.0
P12 = (P0 + PMAX) / 2               # 105,8 kPa
assert round(P12, 1) == 105.8
_, E = x_ordre1(DP, T12)
EXPR = f"{P0}+{E}"
p0 = pente_ordre1(DP, T12, 0)       # kPa/min
yB = round(P0 + 6 * p0, 1)          # B(6 min ; 110,7 kPa)
assert yB == 110.7
dPdt = (yB - P0) / 6 * 1000         # Pa/min (lu sur la tangente)
V0 = Vg / (R * T) * dPdt / Va       # mol·L⁻¹·min⁻¹
V0m = V0 * 1000                     # mmol·L⁻¹·min⁻¹
assert abs(V0m - 4.35) < 0.01, V0m

def figP(titre, p0_, pmax, t12, tmax, gx, gy, B, expr):
    dp = pmax - p0_
    return courbe_fig(titre, ((0, tmax, "t", "min", gx), (100, gy[-1], "P", "kPa", gy)),
        [{"f": "courbe", "expr": expr, "de": 0, "a": tmax, "couleur": "cyan", "texte": "P(t)", "texte_x": tmax * 0.85, "pos": "s"},
         {"f": "courbe", "expr": f"{p0_}+{(B[1]-p0_)/B[0]:.6f}*x", "de": 0, "a": B[0] * 1.1, "couleur": "orange", "trait": "pointille"},
         {"f": "point", "at": [0, p0_], "t": f"A (0 ; {fr(p0_, 1)})", "pos": "e", "couleur": "orange"},
         {"f": "point", "at": list(B), "t": f"B ({B[0]} ; {fr(B[1], 1)})", "pos": "o", "couleur": "orange"},
         {"f": "repere", "y": round(pmax, 2), "couleur": "faible"}],
        legende="La droite (T) est la tangente à la courbe en t = 0 ; coordonnées des points en (min ; kPa).")

FIG = figP("Pression P dans le ballon en fonction du temps", P0, PMAX, T12, 24,
           [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24], [100, 102, 104, 106, 108, 110, 112], (6, yB), EXPR)

# ------------------------------------------------------------------ similaire
sm, sCa, sVa, sVg, sT, sP0, sT12 = 48e-3, 0.20, 50e-3, 0.50e-3, 293.0, 101.3, 5.0
sX = min(sm / M, sCa * sVa / 2)
assert abs(sX - 2.0e-3) < 1e-12
sDP = sX * R * sT / sVg / 1000
sPMAX = sP0 + sDP
assert round(sPMAX, 1) == 111.0, sPMAX
sP12 = (sP0 + sPMAX) / 2
_, sE = x_ordre1(sDP, sT12)
syB = round(sP0 + 6 * pente_ordre1(sDP, sT12, 0), 1)
assert syB == 109.4, syB
sV0m = sVg / (R * sT) * ((syB - sP0) / 6 * 1000) / sVa * 1000
sFIG = figP("Pression P dans le ballon en fonction du temps", sP0, sPMAX, sT12, 30,
            [0, 5, 10, 15, 20, 25, 30], [100, 102, 104, 106, 108, 110, 112], (6, syB), f"{sP0}+{sE}")

# ------------------------------------------------------------------ questions
QUESTIONS = [
  Q("1", "Dresser le tableau d'avancement de la réaction, puis déterminer l'avancement maximal x_max et le réactif limitant.",
    "السؤال un: دير le tableau d'avancement، ومن بعد حدد x max و le réactif limitant.",
    val("x_max", XMAX, "mol", "Mg limitant : x_max = m/M = 0,036/24 = 1,5 × 10⁻³ mol"),
    (["n = m/M", "n = C·V", "n₀(H⁺) − 2x_max = 0", "n₀(Mg) − x_max = 0", "mol"], ["n₀(H⁺) − x_max = 0", "x_max = 3,0 × 10⁻³ mol"]),
    [("Calcule d'abord les deux quantités initiales : le magnésium avec sa masse (n = m/M), les ions H⁺ avec n = C·V.",
      "حسب اللول deux quantités initiales: le magnésium ب la masse، n égale m sur M، و les ions H plus ب n égale C fois V."),
     ("Deux hypothèses : n₀(Mg) − x_max = 0 ou n₀(H⁺) − 2x_max = 0. On garde la plus petite valeur.",
      "deux hypothèses: n zéro de magnésium moins x max égale zéro، ولا n zéro de H plus moins deux x max égale zéro. وكناخدو الصغيرة.")],
    [("1 : n₀(Mg) = m/M = 0,036/24 = 1,5 × 10⁻³ mol ; n₀(H⁺) = C·V = 0,10 × 0,060 = 6,0 × 10⁻³ mol", "les quantités initiales"),
     ("Mg limitant : x_max = 1,5 × 10⁻³ mol ; H⁺ limitant : x_max = 3,0 × 10⁻³ mol", "deux hypothèses"),
     ("x_max = 1,5 × 10⁻³ mol, le magnésium est le réactif limitant", "le magnésium هو le réactif limitant")],
    "السؤال un. les quantités initiales: n zéro de magnésium égale m sur M، يعني un virgule cinq fois dix puissance moins trois mole، و n zéro de H plus égale C fois V، يعني six virgule zéro fois dix puissance moins trois mole. deux hypothèses: un virgule cinq fois dix puissance moins trois، ولا trois virgule zéro fois dix puissance moins trois mole. كناخدو الصغيرة: x max égale un virgule cinq fois dix puissance moins trois mole، و le magnésium هو le réactif limitant.",
    "ex_1", "fa_1"),
  Q("2", "On considère le dihydrogène comme un gaz parfait et l'air du ballon ne réagit pas. Montrer que x = (P − P₀)·V_g/(R·T).",
    "السؤال deux: le dihydrogène gaz parfait، و l'air ديال le ballon ما كيتفاعلش. بين أن x égale P moins P zéro، fois V g sur R T.",
    phrase("P = P₀ + P(H₂) donc P(H₂) = P − P₀ ; P(H₂)·V_g = n(H₂)·R·T ; d'après le tableau n(H₂) = x ; donc x = (P − P₀)·V_g/(R·T)."),
    (["P = P₀ + P(H₂)", "P·V = n·R·T", "n(H₂) = x", "V_g", "R·T"], ["P(H₂) = P", "n(H₂) = 2x"]),
    [("La pression mesurée est celle de l'air (qui reste P₀) plus celle du dihydrogène formé.",
      "la pression اللي كنقيسو هي ديال l'air، اللي كتبقى P zéro، زايد la pression ديال le dihydrogène."),
     ("Applique P(H₂)·V_g = n(H₂)·R·T au dihydrogène, puis lis n(H₂) dans le tableau d'avancement.",
      "طبق P de H deux fois V g égale n de H deux fois R T، ومن بعد قرا n de H deux فle tableau d'avancement.")],
    [("2 : P = P₀ + P(H₂), donc P(H₂) = P − P₀", "P de H deux égale P moins P zéro"),
     ("P(H₂)·V_g = n(H₂)·R·T et n(H₂) = x (tableau)", "n de H deux égale x"),
     ("x = (P − P₀)·V_g/(R·T)", "إذن x égale P moins P zéro، fois V g sur R T")],
    "السؤال deux. l'air ما كيتفاعلش، إذن P égale P zéro plus P de H deux، و P de H deux égale P moins P zéro. la loi des gaz parfaits: P de H deux fois V g égale n de H deux fois R T. ومن le tableau: n de H deux égale x. إذن x égale P moins P zéro، fois V g sur R T.",
    "ex_2", "fa_2"),
  Q("3", "En déduire que x = x_max·(P − P₀)/(P_max − P₀), puis calculer la pression P_max en fin de réaction (en kPa).",
    "السؤال trois: استنتج أن x égale x max، fois P moins P zéro، sur P max moins P zéro. ومن بعد حسب P max ف l'état final، ب kilopascal.",
    val("P_max", PMAX, "kPa", "P_max = P₀ + x_max·R·T/V_g = 101,3 + 9,0 = 110,3 kPa", tol=0.005),
    (["x_max = (P_max − P₀)·V_g/(R·T)", "Pa", "m³", "K", "kPa"], ["V_g = 0,413 L dans la relation", "P_max = x_max·R·T/V_g"]),
    [("Écris la relation de la question 2 à l'état final (x = x_max, P = P_max), puis divise les deux relations.",
      "كتب la relation ديال السؤال deux فl'état final: x égale x max، و P égale P max. ومن بعد قسم وحدة على الأخرى."),
     ("P_max − P₀ = x_max·R·T/V_g, avec V_g en m³ : 0,413 L = 0,413 × 10⁻³ m³ ; le résultat est en pascals.",
      "P max moins P zéro égale x max fois R T sur V g. و V g ب mètre cube: zéro virgule quatre cent treize fois dix puissance moins trois. le résultat ب pascal.")],
    [("3 : à l'état final x_max = (P_max − P₀)·V_g/(R·T) ; en divisant : x = x_max·(P − P₀)/(P_max − P₀)", "كنقسمو"),
     ("P_max − P₀ = 1,5 × 10⁻³ × 8,314 × 298/(0,413 × 10⁻³) ≈ 9,0 × 10³ Pa = 9,0 kPa", "P max moins P zéro égale environ neuf virgule zéro kilopascals"),
     ("P_max = 101,3 + 9,0 = 110,3 kPa", "P max égale cent dix virgule trois kilopascals")],
    "السؤال trois. فl'état final: x max égale P max moins P zéro، fois V g sur R T. كنقسمو la relation ديال x على هادي: x égale x max، fois P moins P zéro، sur P max moins P zéro. ومن بعد: P max moins P zéro égale x max fois R T sur V g، يعني un virgule cinq fois dix puissance moins trois، fois huit virgule trois cent quatorze، fois deux cent quatre-vingt-dix-huit، sur zéro virgule quatre cent treize fois dix puissance moins trois. P max moins P zéro égale environ neuf virgule zéro kilopascals. إذن P max égale cent dix virgule trois kilopascals.",
    "ex_3", "fa_3"),
  Q("4", "Montrer qu'à la date t½ la pression vaut P½ = (P₀ + P_max)/2, puis déterminer graphiquement t½.",
    "السؤال quatre: بين أن à t un demi، la pression égale P zéro plus P max، sur deux. ومن بعد حدد t un demi على la courbe.",
    val("t½", T12, "min", "P½ = (101,3 + 110,3)/2 = 105,8 kPa ; t½ = 4 min", tol=0.06),
    (["x(t½) = x_max/2", "P½ = (P₀ + P_max)/2", "t½", "min"], ["P½ = P_max/2", "t½ = t_f/2"]),
    [("À t½, x = x_max/2 (la réaction est totale). Remplace dans x = x_max·(P − P₀)/(P_max − P₀).",
      "à t un demi، x égale x max sur deux، حيت la réaction totale. عوض فla relation ديال السؤال trois."),
     ("Tu trouves P½ − P₀ = (P_max − P₀)/2. Calcule P½, place-la sur l'axe des pressions, va jusqu'à la courbe, puis descends sur l'axe des temps.",
      "غادي تلقى P un demi moins P zéro égale P max moins P zéro، sur deux. حسب P un demi، حطها على l'axe ديال la pression، سير حتى ل la courbe، ومن بعد هبط ل l'axe du temps.")],
    [("4 : à t½, x = x_max/2 donc (P½ − P₀)/(P_max − P₀) = 1/2", "x égale x max sur deux"),
     ("P½ = (P₀ + P_max)/2 = (101,3 + 110,3)/2 = 105,8 kPa", "P un demi égale cent cinq virgule huit kilopascals"),
     ("lecture graphique : t½ = 4 min", "t un demi égale quatre minutes")],
    "السؤال quatre. à t un demi، x égale x max sur deux، إذن P un demi moins P zéro، sur P max moins P zéro، égale un demi. إذن P un demi égale P zéro plus P max، sur deux، يعني P un demi égale cent cinq virgule huit kilopascals. على la courbe: t un demi égale quatre minutes.",
    "ex_4", "fa_4"),
  Q("5", "La droite (T) est la tangente à la courbe en t = 0. Montrer que v(0) = (V_g/(R·T·V))·(dP/dt)₀, puis calculer v(0) en mmol·L⁻¹·min⁻¹ (V = 60 mL, volume de la solution).",
    "السؤال cinq: la droite T هي la tangente à t égale zéro. بين أن v de zéro égale V g sur R T V، fois d P sur d t à zéro. ومن بعد حسب v de zéro ب millimole par litre et par minute. V هو le volume ديال المحلول، soixante millilitres.",
    val("v(0)", V0m, "mmol·L⁻¹·min⁻¹", "v(0) = V_g/(R·T·V) × (dP/dt)₀ = 0,413 × 10⁻³ × 1,57 × 10³/(8,314 × 298 × 0,060) ≈ 4,4 mmol·L⁻¹·min⁻¹", tol=0.04),
    (["v = (1/V)·dx/dt", "dx/dt = (V_g/(R·T))·dP/dt", "(dP/dt)₀", "Pa/min", "V = 0,060 L"], ["V = V_g", "dP/dt en kPa/min dans la relation"]),
    [("Dérive x = (P − P₀)·V_g/(R·T) : P₀, V_g, R et T sont constants. La pente (dP/dt)₀ se lit sur (T) entre A et B.",
      "اشتق x égale P moins P zéro، fois V g sur R T: P zéro و V g و R و T ثابتين. la pente d P sur d t à zéro كتقراها على T بين A و B."),
     ("(dP/dt)₀ = (110,7 − 101,3)/6 kPa/min ; convertis en Pa/min, puis v(0) = V_g/(R·T·V) × (dP/dt)₀ en mol·L⁻¹·min⁻¹.",
      "d P sur d t à zéro égale cent dix virgule sept moins cent un virgule trois، sur six، ب kilopascal par minute. حولها ل pascal par minute، ومن بعد v de zéro égale V g sur R T V، fois la pente.")],
    [("5 : v = (1/V)·dx/dt et dx/dt = (V_g/(R·T))·dP/dt, donc v = (V_g/(R·T·V))·dP/dt", "v égale V g sur R T V، fois d P sur d t"),
     ("(dP/dt)₀ = (110,7 − 101,3)/(6 − 0) ≈ 1,57 kPa/min = 1,57 × 10³ Pa/min", "la pente égale environ un virgule cinquante-sept kilopascal par minute"),
     ("v(0) = 0,413 × 10⁻³ × 1,57 × 10³/(8,314 × 298 × 0,060) ≈ 4,4 × 10⁻³ mol·L⁻¹·min⁻¹ = 4,4 mmol·L⁻¹·min⁻¹", "v de zéro égale environ quatre virgule quatre millimoles par litre et par minute")],
    "السؤال cinq. v égale un sur V، fois d x sur d t. و d x sur d t égale V g sur R T، fois d P sur d t. إذن v égale V g sur R T V، fois d P sur d t. la pente ديال T: cent dix virgule sept moins cent un virgule trois، sur six، la pente égale environ un virgule cinquante-sept kilopascal par minute، يعني mille cinq cent soixante-dix pascals par minute. l'application numérique: v de zéro égale environ quatre virgule quatre millimoles par litre et par minute.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : deux hypothèses, on garde la plus petite",
      "x_max est la plus petite des valeurs données par les deux hypothèses.",
      "cinetique-tableau/limitant.html", "Les deux hypothèses du réactif limitant",
      "شوف هاد المثال ديال le cours: deux réactifs، و deux hypothèses. l'hypothèse un كتعطي deux virgule zéro millimoles. l'hypothèse deux، مع le coefficient deux، كتعطي cinq virgule zéro millimoles. كناخدو الصغيرة. فالتمرين ديالنا: le magnésium كيعطي un virgule cinq fois dix puissance moins trois mole، و les ions H plus، مع le coefficient deux، كيعطيو trois virgule zéro fois dix puissance moins trois mole. إذن x max égale un virgule cinq fois dix puissance moins trois mole، و le magnésium هو le réactif limitant.",
      [("n₀(Mg) − x_max = 0 ; n₀(H⁺) − 2x_max = 0", "فالتمرين ديالنا"), ("x_max = 1,5 × 10⁻³ mol ; Mg limitant", "و le magnésium هو le réactif limitant")],
      [("شوف هاد المثال ديال le cours", "moment:tableau"), ("l'hypothèse un كتعطي", "moment:hypothese_1"),
       ("l'hypothèse deux، مع le coefficient deux", "moment:hypothese_2"), ("كناخدو الصغيرة", "moment:plus_petite"),
       ("إذن x max égale un virgule cinq", "moment:limitant")]),
  sim("ex_2", "Question 2 : x à partir de la pression",
      "P = P₀ + P(H₂) ; P(H₂)·V = n(H₂)·R·T ; n(H₂) = x.",
      "cinetique-tableau/pression.html?vue=relation", "La loi des gaz parfaits appliquée au dihydrogène",
      "فالبداية، le ballon فيه l'air، ب la pression P zéro. l'air ما كيتفاعلش، إذن la pression ديالو كتبقى P zéro. le dihydrogène كيزيد la pression ديالو: P de H deux égale P moins P zéro. ونطبقو la loi des gaz parfaits على le dihydrogène. ومن le tableau d'avancement: n de H deux égale x. إذن x égale P moins P zéro، fois V sur R T. رد البال للوحدات: P بالوحدة pascal، V بالوحدة mètre cube، و T بالوحدة kelvin. فالتمرين ديالنا، V هو V g، le volume اللي فيه le gaz.",
      [("P(H₂) = P − P₀ ; P(H₂)·V_g = n(H₂)·R·T", "P de H deux égale P moins P zéro"),
       ("x = (P − P₀)·V_g/(R·T)", "إذن x égale P moins P zéro، fois V sur R T")],
      [("فالبداية، le ballon فيه l'air", "start"), ("ونطبقو la loi des gaz parfaits", "moment:gaz_parfait"),
       ("ومن le tableau d'avancement", "moment:hydrogene"), ("إذن x égale P moins P zéro", "moment:relation"),
       ("رد البال للوحدات", "moment:unites")]),
  sim("ex_3", "Question 3 : la pression finale",
      "À l'état final, x = x_max : P_max − P₀ = x_max·R·T/V_g.",
      "cinetique-tableau/pression.html?vue=ballon", "Le ballon fermé et son manomètre",
      "شوف le montage: le ballon fermé، مربوط ب le manomètre. نحطو le ruban de magnésium ف l'acide. كيخرجو des bulles، هادا le dihydrogène. la pression كتطلع. ومن بعد كتوقف: هادا le palier، la réaction سالات، و x égale x max. فالتمرين ديالنا: P max moins P zéro égale x max fois R T sur V g، يعني environ neuf virgule zéro kilopascals. إذن P max égale cent dix virgule trois kilopascals.",
      [("P_max − P₀ = x_max·R·T/V_g ≈ 9,0 kPa", "يعني environ neuf virgule zéro kilopascals"),
       ("P_max = 110,3 kPa", "إذن P max égale cent dix virgule trois kilopascals")],
      [("شوف le montage", "moment:montage"), ("نحطو le ruban", "moment:ruban"), ("كيخرجو des bulles", "moment:bulles"),
       ("la pression كتطلع", "moment:monte"), ("هادا le palier", "moment:palier")]),
  sim("ex_4", "Question 4 : t½ sur la courbe",
      "À t½, x = x_max/2 : P½ = (P₀ + P_max)/2, puis la lecture en quatre gestes.",
      "cinetique-tableau/demi-reaction.html?vue=lecture", "La lecture de t½ en quatre gestes",
      "t un demi كنقراوها ب quatre خطوات. اللولة: la valeur finale، على le palier. الثانية: la moitié، على l'axe العمودي. الثالثة: كنمشيو horizontale حتى ل la courbe. الرابعة: كنهبطو verticale حتى ل l'axe du temps. فالتمرين ديالنا، l'axe العمودي هو la pression، و la moitié كتولي P un demi égale P zéro plus P max، sur deux، يعني cent cinq virgule huit kilopascals. ومن la courbe ديال l'énoncé: t un demi égale quatre minutes.",
      [("P½ = (101,3 + 110,3)/2 = 105,8 kPa", "يعني cent cinq virgule huit kilopascals"), ("t½ = 4 min", "t un demi égale quatre minutes")],
      [("اللولة: la valeur finale", "moment:x_f"), ("الثانية: la moitié", "moment:moitie"),
       ("الثالثة: كنمشيو horizontale", "moment:horizontale"), ("الرابعة: كنهبطو verticale", "moment:verticale"),
       ("ومن la courbe ديال l'énoncé", "moment:valeur")]),
  sim("ex_5", "Question 5 : la vitesse en trois lignes",
      "La relation, la pente avec son unité, l'application numérique avec les bonnes unités.",
      "cinetique-tableau/vitesse.html?vue=calcul", "Le calcul de la vitesse, comme sur la copie",
      "نكتبو le calcul ب trois lignes. اللولة، la relation: v égale un sur V، fois d x sur d t. فالتمرين ديالنا، d x sur d t égale V g sur R T، fois d P sur d t. الثانية، la pente: على la tangente T، environ un virgule cinquante-sept kilopascal par minute. الثالثة، l'application numérique، مع V égale zéro virgule zéro soixante litre. le résultat: v de zéro égale environ quatre virgule quatre millimoles par litre et par minute. رد البال: la pression ب pascal، و V g ب mètre cube.",
      [("v = (V_g/(R·T·V))·dP/dt", "d x sur d t égale V g sur R T"), ("v(0) ≈ 4,4 mmol·L⁻¹·min⁻¹", "le résultat")],
      [("اللولة، la relation", "moment:relation"), ("الثانية، la pente", "moment:pente"),
       ("الثالثة، l'application numérique", "moment:application"), ("le résultat", "moment:resultat"),
       ("رد البال", "moment:piege")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : le réactif limitant", "سؤال ساهل على le réactif limitant.",
      "n₀(Mg) = 1,5 × 10⁻³ mol et n₀(H⁺) = 6,0 × 10⁻³ mol, équation Mg + 2 H⁺ → Mg²⁺ + H₂. Le réactif limitant est…",
      ["les ions H⁺, car le coefficient est 2", "aucun : le mélange est stœchiométrique", "le magnésium"], 2, {
        2: ("juste", "برافو! le magnésium كيعطي un virgule cinq fois dix puissance moins trois، و H plus كيعطيو trois virgule zéro. الصغيرة هي ديال le magnésium.", "Juste : 1,5 × 10⁻³ < 3,0 × 10⁻³ mol, Mg est limitant."),
        0: (("le coefficient deux كيقسم n zéro de H plus على deux، ولكن باقي كبير. قارن un virgule cinq مع trois virgule zéro. عاود اختار.", "6,0 × 10⁻³/2 = 3,0 × 10⁻³ mol, plus grand que 1,5 × 10⁻³. Réessaie."),
            ("الجواب: le magnésium. n zéro de H plus sur deux égale trois virgule zéro fois dix puissance moins trois، كبر من un virgule cinq.", "Réponse : Mg (1,5 × 10⁻³ < 3,0 × 10⁻³ mol).")),
        1: (("stœchiométrique يعني deux hypothèses كيعطيو نفس x max. هنا ماشي نفس القيمة. عاود اختار.", "Stœchiométrique : les deux hypothèses donneraient la même valeur ; ce n'est pas le cas. Réessaie."),
            ("الجواب: le magnésium، حيت un virgule cinq fois dix puissance moins trois صغيرة من trois virgule zéro.", "Réponse : Mg est limitant."))},
      "n zéro de magnésium égale un virgule cinq fois dix puissance moins trois mole, et n zéro de H plus égale six virgule zéro fois dix puissance moins trois mole. Le réactif limitant est ?"),
  qcm("fa_2", "Plus facile : la pression du dihydrogène", "سؤال ساهل: شنو هي la pression ديال le dihydrogène؟",
      "P₀ est la pression initiale de l'air, P la pression mesurée. La pression du dihydrogène est…",
      ["P(H₂) = P − P₀", "P(H₂) = P", "P(H₂) = P + P₀"], 0, {
        0: ("juste", "برافو! l'air كيبقى ب P zéro، والزيادة كلها ديال le dihydrogène.", "Juste : P = P₀ + P(H₂), donc P(H₂) = P − P₀."),
        1: (("لا، le manomètre كيقيس l'air و le dihydrogène بجوج. l'air باقي فle ballon. عاود اختار.", "Le manomètre mesure l'air ET le dihydrogène. Réessaie."),
            ("الجواب: P de H deux égale P moins P zéro، حيت l'air باقي ب P zéro.", "Réponse : P(H₂) = P − P₀.")),
        2: (("لا، P زايدة على P zéro، ماشي P zéro اللي كتزاد عليها. عاود اختار.", "P contient déjà P₀. Réessaie."),
            ("الجواب: P de H deux égale P moins P zéro.", "Réponse : P(H₂) = P − P₀."))},
      "P zéro est la pression initiale de l'air, P la pression mesurée. La pression du dihydrogène est ?"),
  qcm("fa_3", "Plus facile : les unités de la loi des gaz parfaits", "سؤال ساهل على الوحدات.",
      "Dans P·V = n·R·T, avec R = 8,314 SI, il faut…",
      ["P en kPa, V en L, T en °C", "P en Pa, V en m³, T en K", "P en Pa, V en L, T en K"], 1, {
        1: ("juste", "برافو! les unités ديال le système international: pascal، mètre cube، kelvin.", "Juste : Pa, m³ et K."),
        0: (("لا، R égale huit virgule trois cent quatorze غير ب les unités SI. عاود اختار.", "R = 8,314 n'est valable qu'en unités SI. Réessaie."),
            ("الجواب: P ب pascal، V ب mètre cube، T ب kelvin.", "Réponse : Pa, m³, K.")),
        2: (("قريب! ولكن le litre ماشي وحدة SI: V خاصو ب mètre cube. عاود اختار.", "Le litre n'est pas SI : V en m³. Réessaie."),
            ("الجواب: P ب pascal، V ب mètre cube، T ب kelvin.", "Réponse : Pa, m³, K."))},
      "Dans P V égale n R T, avec R égale huit virgule trois cent quatorze, il faut ?"),
  vf("fa_4", "Plus facile : vrai ou faux", "P₀ = 101,3 kPa et P_max = 110,3 kPa.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("À t½, P = (P₀ + P_max)/2 = 105,8 kPa.", True, "À t½, x = x_max/2, donc P − P₀ est la moitié de P_max − P₀."),
      ("À t½, P = P_max/2 = 55,2 kPa.", False, "La pression ne descend jamais sous P₀ : c'est P − P₀ qui est divisé par deux."),
      ("t½ se lit sur l'axe des temps, en minutes.", True, "On descend du point de la courbe jusqu'à l'axe des temps.")]),
  qcm("fa_5", "Plus facile : la pente de la tangente", "سؤال ساهل على la pente.",
      "La tangente (T) passe par A(0 ; 101,3 kPa) et B(6 min ; 110,7 kPa). Sa pente (dP/dt)₀ vaut…",
      ["18,5 kPa/min", "0,64 min/kPa", "1,57 kPa/min"], 2, {
        2: ("juste", "برافو! cent dix virgule sept moins cent un virgule trois، sur six، كتعطي un virgule cinquante-sept kilopascal par minute.", "Juste : (110,7 − 101,3)/6 ≈ 1,57 kPa/min."),
        0: (("لا، هاد القيمة كتجي من P B sur six. la pente هي الفرق ديال P على الفرق ديال t. عاود اختار.", "On divise la différence de pression, pas P_B. Réessaie."),
            ("الجواب: un virgule cinquante-sept kilopascal par minute: الفرق، على six.", "Réponse : ΔP/Δt = 9,4/6 ≈ 1,57 kPa/min.")),
        1: (("لا، قلبتي la fraction: delta t sur delta P. la pente هي delta P sur delta t. عاود اختار.", "C'est Δt/ΔP, la fraction est renversée. Réessaie."),
            ("الجواب: un virgule cinquante-sept kilopascal par minute، delta P sur delta t.", "Réponse : ΔP/Δt ≈ 1,57 kPa/min."))},
      "La tangente passe par A, zéro et cent un virgule trois kilopascals, et B, six minutes et cent dix virgule sept kilopascals. Sa pente vaut ?"),
]

SIM_Q = [
  QS("1", "Dresser le tableau d'avancement, puis déterminer x_max et le réactif limitant.",
     val("x_max", sX, "mol", "Mg limitant : x_max = 0,048/24 = 2,0 × 10⁻³ mol"),
     (["n = m/M", "n = C·V", "mol"], ["n₀(H⁺) − x_max = 0"]),
     [("n₀(Mg) = 0,048/24 = 2,0 × 10⁻³ mol ; n₀(H⁺) = 0,20 × 0,050 = 1,0 × 10⁻² mol", "les quantités initiales"),
      ("hypothèses : 2,0 × 10⁻³ ou 5,0 × 10⁻³ mol ; x_max = 2,0 × 10⁻³ mol, Mg limitant", "x max égale deux virgule zéro")],
     "les quantités initiales: deux virgule zéro fois dix puissance moins trois mole ديال le magnésium، و un virgule zéro fois dix puissance moins deux mole ديال H plus. les hypothèses كيعطيو deux virgule zéro ولا cinq virgule zéro fois dix puissance moins trois. x max égale deux virgule zéro fois dix puissance moins trois mole، و le magnésium هو le réactif limitant."),
  QS("2", "Montrer que x = (P − P₀)·V_g/(R·T).",
     phrase("P(H₂) = P − P₀ ; P(H₂)·V_g = n(H₂)·R·T ; n(H₂) = x ; donc x = (P − P₀)·V_g/(R·T)."),
     (["P = P₀ + P(H₂)", "P·V = n·R·T", "n(H₂) = x"], ["P(H₂) = P"]),
     [("P(H₂) = P − P₀ et P(H₂)·V_g = n(H₂)·R·T", "P de H deux égale P moins P zéro"),
      ("n(H₂) = x donc x = (P − P₀)·V_g/(R·T)", "x égale P moins P zéro")],
     "l'air كتبقى ب P zéro، إذن P de H deux égale P moins P zéro. و P de H deux fois V g égale n de H deux fois R T، مع n de H deux égale x. إذن x égale P moins P zéro، fois V g sur R T."),
  QS("3", "En déduire x = x_max·(P − P₀)/(P_max − P₀), puis calculer P_max en kPa.",
     val("P_max", sPMAX, "kPa", "P_max = 101,3 + 2,0 × 10⁻³ × 8,314 × 293/(0,50 × 10⁻³) × 10⁻³ ≈ 111,0 kPa", tol=0.005),
     (["P_max − P₀ = x_max·R·T/V_g", "Pa", "m³"], ["P_max = x_max·R·T/V_g"]),
     [("P_max − P₀ = 2,0 × 10⁻³ × 8,314 × 293/(0,50 × 10⁻³) ≈ 9,7 × 10³ Pa", "P max moins P zéro"),
      ("P_max ≈ 111,0 kPa", "P max égale environ cent onze kilopascals")],
     "فl'état final: P max moins P zéro égale x max fois R T sur V g، يعني environ neuf virgule sept kilopascals. إذن P max égale environ cent onze kilopascals."),
  QS("4", "Montrer que P½ = (P₀ + P_max)/2, puis déterminer t½ graphiquement.",
     val("t½", sT12, "min", "P½ = (101,3 + 111,0)/2 ≈ 106,2 kPa ; t½ = 5 min", tol=0.06),
     (["P½ = (P₀ + P_max)/2", "t½"], ["P½ = P_max/2"]),
     [("à t½, x = x_max/2 donc P½ = (P₀ + P_max)/2 ≈ 106,2 kPa", "P un demi égale environ cent six virgule deux"),
      ("t½ = 5 min", "t un demi égale cinq minutes")],
     "à t un demi، x égale x max sur deux، إذن P un demi égale P zéro plus P max، sur deux، يعني P un demi égale environ cent six virgule deux kilopascals. على la courbe: t un demi égale cinq minutes."),
  QS("5", "Montrer que v(0) = (V_g/(R·T·V))·(dP/dt)₀, puis calculer v(0) en mmol·L⁻¹·min⁻¹ (V = 50 mL).",
     val("v(0)", sV0m, "mmol·L⁻¹·min⁻¹", "v(0) = 0,50 × 10⁻³ × 1,35 × 10³/(8,314 × 293 × 0,050) ≈ 5,5 mmol·L⁻¹·min⁻¹", tol=0.04),
     (["v = (1/V)·dx/dt", "(dP/dt)₀", "Pa/min"], ["V = V_g"]),
     [("v = (V_g/(R·T·V))·dP/dt ; (dP/dt)₀ = (109,4 − 101,3)/6 ≈ 1,35 kPa/min", "la pente égale environ un virgule trente-cinq"),
      ("v(0) ≈ 5,5 mmol·L⁻¹·min⁻¹", "v de zéro égale environ cinq virgule cinq")],
     "v égale V g sur R T V، fois d P sur d t. la pente égale environ un virgule trente-cinq kilopascal par minute. إذن v de zéro égale environ cinq virgule cinq millimoles par litre et par minute."),
]

EX = exercice(
  "phys_ex_ch10_cinetique_3", "phys_ch10_cinetique", "cinetique",
  "Un ruban de magnésium dans un ballon fermé : suivi par la pression", "moyen", 30,
  ["Déterminer x_max et le réactif limitant", "Établir x en fonction de la pression", "Déterminer t½ à partir d'une grandeur mesurée", "Calculer v(0) par la tangente"],
  "Dans un ballon fermé relié à un manomètre, on verse V = 60 mL d'acide chlorhydrique de concentration C = 0,10 mol/L. À t = 0, on y introduit un ruban de magnésium de masse m = 36 mg. Le volume occupé par les gaz au-dessus de la solution est V_g = 0,413 L ; la température reste T = 298 K. La réaction, lente et totale, a pour équation : Mg(s) + 2 H⁺(aq) → Mg²⁺(aq) + H₂(g). La figure donne la pression P mesurée en fonction du temps, et la tangente (T) à la courbe en t = 0.",
  "دابا نقراو l'énoncé. فواحد le ballon fermé مربوط ب le manomètre، كنحطو soixante millilitres ديال l'acide chlorhydrique، zéro virgule dix mole par litre. فt égale zéro، كنزيدو le ruban de magnésium، la masse ديالو trente-six milligrammes. le volume ديال les gaz فوق المحلول، V g égale zéro virgule quatre cent treize litre، و la température deux cent quatre-vingt-dix-huit kelvins. la réaction totale: le magnésium، plus deux ions H plus، كيعطيو l'ion magnésium و le dihydrogène. la figure كتعطي la pression P en fonction du temps، مع la tangente T à t égale zéro.",
  [FIG],
  ["V = 60 mL ; C = 0,10 mol/L (acide chlorhydrique)", "m(Mg) = 36 mg ; M(Mg) = 24 g/mol", "V_g = 0,413 L ; T = 298 K ; R = 8,314 Pa·m³·mol⁻¹·K⁻¹",
   "P₀ = 101,3 kPa (pression de l'air à t = 0)", "Tangente (T) : A(0 ; 101,3 kPa) et B(6 min ; 110,7 kPa)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Même montage. V = 50 mL d'acide chlorhydrique à C = 0,20 mol/L ; ruban de magnésium de masse m = 48 mg ; V_g = 0,50 L ; T = 293 K ; P₀ = 101,3 kPa. La figure donne P en fonction du temps et la tangente (T) en t = 0.",
  "نفس التمرين، بقيم أخرى. cinquante millilitres ديال l'acide، zéro virgule vingt mole par litre، و le ruban de magnésium، quarante-huit milligrammes. V g égale zéro virgule cinquante litre، و T égale deux cent quatre-vingt-treize kelvins.",
  [sFIG],
  ["V = 50 mL ; C = 0,20 mol/L", "m(Mg) = 48 mg ; M(Mg) = 24 g/mol", "V_g = 0,50 L ; T = 293 K ; R = 8,314 SI ; P₀ = 101,3 kPa",
   "Tangente (T) : A(0 ; 101,3 kPa) et B(6 min ; 109,4 kPa)"],
  SIM_Q)

ecrire(EX)
