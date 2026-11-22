# Exercice de chimie, ch. 10 (suivi temporel, vitesse de réaction), niveau moyen (celui du national) : suivi
# conductimétrique ; tableau et x_max, « montrer que » σ = (λ₁ + λ₂)·x/V, σ_f, σ½ puis t½, v(0) en mol·m⁻³·min⁻¹.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2016 R (2.2 tableau, 2.3.1 σ½ quand x = x_max/2, 2.3.2 t½ en minutes, 2.3.3 v(0)
#    en mol·m⁻³·min⁻¹), 2018 R (2.2.1 G½, 2.2.2 t½), 2021 N (2.2 t½ à l'aide de σ = f(x), 2.3 « montrer que »
#    v = −1/(160·V₀)·dσ/dt, 2.4 v₁ en mol·m⁻³·min⁻¹) — backend/data/exams/physique ;
#  - profs : architecture/sources_chimie_ch9_ch11.md, chapitre B (Mahajar-Tabit, Sbiro, Boulouiha : hydrolyse de RCl
#    suivie par conductimétrie, x = x_max·σ/σ_max ; Hadjyne : σ = A + B·x) et phys_ch10_cinetique.md (pièges : λ en
#    mS·m²·mol⁻¹ à convertir, concentrations en mol·m⁻³, V en m³ ; σ½ ≠ σ(t_f/2)) ;
#  - séries en ligne (titres et résumés lus par recherche ; PDF non ouverts, réseau du conteneur limité) :
#    talamidi (suivi temporel, séries 1 et 2, activités 3), moutamadris (fiches 13-7, 13-8 et suivi temporel 2022),
#    alloschool (élément 119798), coursdusoirpc (TD B. Mouslim), labolycee (sujets « cinétique conductimétrie RCl »,
#    pour la forme seulement : programme français).
# Ici : nos propres quantité, volume et courbe σ(t) (calculée, modèle d'ordre un, t½ = 5 min).
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *

L_H3O, L_CL = 35.0e-3, 7.6e-3          # S·m²·mol⁻¹
LS = L_H3O + L_CL                      # 42,6e-3
# ------------------------------------------------------------------ données
N0, V = 1.0e-3, 100e-6                 # mol, m³
SF = LS * N0 / V                       # 0,426 S/m
assert abs(SF - 0.426) < 1e-9
T12 = 5.0
_, EXPR = x_ordre1(SF, T12)
yB = round(pente_ordre1(SF, T12, 0) * 6, 3)    # B(6 min ; 0,354 S/m)
assert yB == 0.354
DSDT = yB / 6                           # S·m⁻¹·min⁻¹
V0 = DSDT / LS                          # mol·m⁻³·min⁻¹
assert abs(V0 - 1.385) < 0.001, V0

def figS(sf, t12, tmax, gx, gy, B, expr):
    return courbe_fig("Conductivité σ du mélange en fonction du temps",
        ((0, tmax, "t", "min", gx), (0, gy[-1], "σ", "S/m", gy)),
        [{"f": "courbe", "expr": expr, "de": 0, "a": tmax, "couleur": "cyan", "texte": "σ(t)", "texte_x": tmax * 0.85, "pos": "s"},
         {"f": "courbe", "expr": f"{B[1]/B[0]:.6f}*x", "de": 0, "a": B[0] * 1.15, "couleur": "orange", "trait": "pointille"},
         {"f": "point", "at": [0, 0], "t": "O", "pos": "se", "couleur": "orange"},
         {"f": "point", "at": list(B), "t": f"B ({B[0]} ; {fr(B[1], 3)})", "pos": "o", "couleur": "orange"},
         {"f": "repere", "y": round(sf, 3), "couleur": "faible"}],
        legende="(T) : tangente à la courbe en t = 0, passant par O et B ; coordonnées en (min ; S/m).")

FIG = figS(SF, T12, 40, [0, 5, 10, 15, 20, 25, 30, 35, 40], [0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5], (6, yB), EXPR)

# ------------------------------------------------------------------ similaire
sN0, sV, sT12 = 2.0e-3, 100e-6, 4.0
sSF = LS * sN0 / sV                     # 0,852
_, sE = x_ordre1(sSF, sT12)
syB = round(pente_ordre1(sSF, sT12, 0) * 4, 3)
assert syB == 0.591, syB
sV0 = syB / 4 / LS                      # 3,47
sFIG = figS(sSF, sT12, 32, [0, 4, 8, 12, 16, 20, 24, 28, 32], [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0], (4, syB), sE)

TAB = "RCl + 2 H₂O → ROH + H₃O⁺ + Cl⁻"
QUESTIONS = [
  Q("1", "Dresser le tableau d'avancement de la réaction et déterminer l'avancement maximal x_max.",
    "السؤال un: دير le tableau d'avancement، وحدد x max.",
    val("x_max", N0, "mol", "eau en excès, RCl limitant : n₀ − x_max = 0, x_max = n₀ = 1,0 × 10⁻³ mol"),
    (["n₀ − x", "excès", "x_max", "mol"], ["x_max = n₀/2", "l'eau est limitante"]),
    [("L'eau est le solvant : elle est en excès. Il ne reste qu'un réactif qui peut s'épuiser.",
      "الما هو le solvant: كاين en excès. إذن غير réactif واحد اللي يقدر يتسالى."),
     ("Ligne finale : n(RCl) = n₀ − x_max = 0.",
      "فl'état final: n de R C l égale n zéro moins x max، égale zéro.")],
    [("1 : état initial : n₀ ; excès ; 0 ; 0 ; 0 — en cours : n₀ − x ; excès ; x ; x ; x", "le tableau"),
     ("l'eau est en excès, RCl est limitant : n₀ − x_max = 0", "n zéro moins x max égale zéro"),
     ("x_max = n₀ = 1,0 × 10⁻³ mol", "x max égale un virgule zéro fois dix puissance moins trois mole")],
    "السؤال un. le tableau: فالبداية n zéro ديال R C l، الما en excès، و zéro ديال les produits. en cours: n zéro moins x، و x ديال كل produit. الما en excès، إذن R C l هو le réactif limitant: n zéro moins x max égale zéro. x max égale un virgule zéro fois dix puissance moins trois mole.",
    "ex_1", "fa_1"),
  Q("2", "En négligeant les ions HO⁻, montrer que la conductivité du mélange s'écrit σ = (λ(H₃O⁺) + λ(Cl⁻))·x/V.",
    "السؤال deux: نهملو les ions H O moins. بين أن sigma égale lambda de H trois O plus، plus lambda de C l moins، fois x sur V.",
    phrase("σ = λ(H₃O⁺)·[H₃O⁺] + λ(Cl⁻)·[Cl⁻] ; d'après le tableau [H₃O⁺] = [Cl⁻] = x/V ; donc σ = (λ(H₃O⁺) + λ(Cl⁻))·x/V."),
    (["σ = Σ λᵢ·[Xᵢ]", "[H₃O⁺] = x/V", "[Cl⁻] = x/V", "factoriser"], ["[H₃O⁺] = n₀/V", "σ = λ·x"]),
    [("Quels ions sont présents dans le mélange à une date t ? RCl et ROH sont des molécules.",
      "شمن ions كاينين فle mélange ف واحد la date؟ R C l و R O H هوما des molécules، ماشي ions."),
     ("Écris σ = Σ λᵢ·[Xᵢ], puis remplace chaque concentration à l'aide du tableau : n = x, donc [X] = x/V.",
      "كتب sigma égale la somme des lambda i fois la concentration. ومن le tableau: n égale x، إذن la concentration égale x sur V.")],
    [("2 : σ = λ(H₃O⁺)·[H₃O⁺] + λ(Cl⁻)·[Cl⁻]", "sigma égale lambda de H trois O plus"),
     ("d'après le tableau : [H₃O⁺] = [Cl⁻] = x/V", "la concentration égale x sur V"),
     ("σ = (λ(H₃O⁺) + λ(Cl⁻))·x/V", "كنجمعو")],
    "السؤال deux. les ions اللي كاينين: H trois O plus و C l moins. sigma égale lambda de H trois O plus fois sa concentration، plus lambda de C l moins fois sa concentration. ومن le tableau: كل واحد فيهم عندو x mole، إذن la concentration égale x sur V. كنجمعو: sigma égale lambda de H trois O plus، plus lambda de C l moins، fois x sur V.",
    "ex_2", "fa_2"),
  Q("3", "Calculer la conductivité σ_f à la fin de la réaction, puis vérifier sur la courbe que la réaction est totale.",
    "السؤال trois: حسب sigma f فاللخر ديال la réaction، ومن بعد تأكد على la courbe بلي la réaction totale.",
    val("σ_f", SF, "S/m", "σ_f = (35,0 + 7,6) × 10⁻³ × 1,0 × 10⁻³/(100 × 10⁻⁶) = 0,426 S/m"),
    (["σ_f = (λ₁ + λ₂)·x_max/V", "mS → S : × 10⁻³", "V en m³", "S/m"], ["V = 100 mL dans la relation", "V = 0,1 m³"]),
    [("À la fin, x = x_max. Attention aux unités : λ en S·m²·mol⁻¹ (35,0 mS = 35,0 × 10⁻³ S) et V en m³.",
      "فاللخر، x égale x max. ورد البال للوحدات: lambda ب siemens mètre carré par mole، و V ب mètre cube."),
     ("100 mL = 100 × 10⁻⁶ m³ = 1,0 × 10⁻⁴ m³. Compare ensuite la valeur trouvée avec le palier de la courbe.",
      "cent millilitres égale cent fois dix puissance moins six mètre cube. ومن بعد قارن مع le palier ديال la courbe.")],
    [("3 : σ_f = (λ(H₃O⁺) + λ(Cl⁻))·x_max/V", "sigma f égale"),
     ("σ_f = 42,6 × 10⁻³ × 1,0 × 10⁻³/(1,0 × 10⁻⁴) = 0,426 S/m", "sigma f égale zéro virgule quatre cent vingt-six siemens par mètre"),
     ("le palier de la courbe vaut aussi 0,426 S/m : x_f = x_max, la réaction est totale", "la réaction totale")],
    "السؤال trois. فاللخر x égale x max، إذن sigma f égale lambda de H trois O plus، plus lambda de C l moins، fois x max sur V. l'application numérique: quarante-deux virgule six fois dix puissance moins trois، fois un virgule zéro fois dix puissance moins trois، sur un virgule zéro fois dix puissance moins quatre. sigma f égale zéro virgule quatre cent vingt-six siemens par mètre. le palier ديال la courbe عندو نفس القيمة، إذن x f égale x max: la réaction totale.",
    "ex_3", "fa_3"),
  Q("4", "Montrer qu'à la date t½ la conductivité vaut σ½ = σ_f/2, puis déterminer graphiquement t½.",
    "السؤال quatre: بين أن à t un demi، sigma un demi égale sigma f sur deux، ومن بعد حدد t un demi على la courbe.",
    val("t½", T12, "min", "σ½ = σ_f/2 = 0,213 S/m ; t½ = 5 min", tol=0.06),
    (["x(t½) = x_f/2", "σ½ = σ_f/2", "t½", "min"], ["σ½ = σ(t_f/2)", "t½ = 20 min"]),
    [("σ est proportionnelle à x (question 2). Que vaut x à t½ ?",
      "sigma proportionnelle ل x، من السؤال deux. شحال كتسوى x à t un demi؟"),
     ("À t½, x = x_f/2 donc σ½ = σ_f/2 = 0,213 S/m : place cette valeur sur l'axe des σ, va jusqu'à la courbe, puis descends sur l'axe des temps.",
      "à t un demi، x égale x f sur deux، إذن sigma un demi égale sigma f sur deux، zéro virgule deux cent treize. حطها على l'axe ديال sigma، سير حتى ل la courbe، ومن بعد هبط.")],
    [("4 : σ est proportionnelle à x et à t½, x = x_f/2, donc σ½ = σ_f/2", "sigma un demi égale sigma f sur deux"),
     ("σ½ = 0,426/2 = 0,213 S/m", "zéro virgule deux cent treize siemens par mètre"),
     ("lecture graphique : t½ = 5 min", "t un demi égale cinq minutes")],
    "السؤال quatre. sigma proportionnelle ل x، و à t un demi x égale x f sur deux. إذن sigma un demi égale sigma f sur deux، يعني zéro virgule deux cent treize siemens par mètre. على la courbe: t un demi égale cinq minutes.",
    "ex_4", "fa_4"),
  Q("5", "Montrer que la vitesse volumique s'écrit v = (1/(λ(H₃O⁺) + λ(Cl⁻)))·dσ/dt, puis calculer v(0) en mol·m⁻³·min⁻¹ à l'aide de la tangente (T).",
    "السؤال cinq: بين أن la vitesse volumique، v égale un sur lambda de H trois O plus plus lambda de C l moins، fois d sigma sur d t. ومن بعد حسب v de zéro ب mole par mètre cube et par minute، بla tangente T.",
    val("v(0)", V0, "mol·m⁻³·min⁻¹", "v(0) = (dσ/dt)₀/(λ₁ + λ₂) = (0,354/6)/(42,6 × 10⁻³) ≈ 1,39 mol·m⁻³·min⁻¹", tol=0.04),
    (["v = (1/V)·dx/dt", "x = σ·V/(λ₁ + λ₂)", "(dσ/dt)₀", "mol·m⁻³·min⁻¹"], ["v = dσ/dt", "v = (λ₁ + λ₂)·dσ/dt"]),
    [("De la question 2 : x = σ·V/(λ₁ + λ₂). Remplace x dans v = (1/V)·dx/dt : V et les λ sont constants.",
      "من السؤال deux: x égale sigma fois V، sur lambda un plus lambda deux. عوض فv égale un sur V fois d x sur d t: V و les lambda ثابتين."),
     ("La pente (dσ/dt)₀ se lit sur (T) entre O et B, en S·m⁻¹·min⁻¹.",
      "la pente d sigma sur d t à zéro كتقراها على T بين O و B، ب siemens par mètre et par minute.")],
    [("5 : x = σ·V/(λ₁ + λ₂) donc v = (1/V)·dx/dt = (1/(λ₁ + λ₂))·dσ/dt", "v égale un sur lambda un plus lambda deux"),
     ("(dσ/dt)₀ = (0,354 − 0)/(6 − 0) = 0,059 S·m⁻¹·min⁻¹", "la pente égale zéro virgule zéro cinquante-neuf"),
     ("v(0) = 0,059/(42,6 × 10⁻³) ≈ 1,39 mol·m⁻³·min⁻¹", "v de zéro égale environ un virgule trente-neuf mole par mètre cube et par minute")],
    "السؤال cinq. من السؤال deux: x égale sigma fois V، sur lambda un plus lambda deux. نعوضو فv égale un sur V fois d x sur d t: V كيمشي، و v égale un sur lambda un plus lambda deux، fois d sigma sur d t. la pente ديال T: zéro virgule trois cent cinquante-quatre sur six، la pente égale zéro virgule zéro cinquante-neuf siemens par mètre et par minute. إذن v de zéro égale environ un virgule trente-neuf mole par mètre cube et par minute.",
    "ex_5", "fa_5"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : le tableau, ligne par ligne",
      "État initial, en cours (n₀ − x), état final (x_max).",
      "cinetique-tableau/avancement.html?vue=tableau&depart=etat_initial", "Le tableau d'avancement en trois lignes",
      "رجعنا ل le tableau ديال l'état initial. السطر التاني: en cours، l'avancement x: كل réactif كينقص، وكل produit كيزيد. السطر التالت: l'état final، كنبدلو x ب x max. فالتمرين ديالنا: الما en excès، و R C l كيبقى n zéro moins x. فاللخر n zéro moins x max égale zéro، إذن x max égale un virgule zéro fois dix puissance moins trois mole.",
      [("n(RCl) = n₀ − x ; eau en excès", "و R C l كيبقى n zéro moins x"), ("x_max = n₀ = 1,0 × 10⁻³ mol", "إذن x max égale un virgule zéro")],
      [("رجعنا ل le tableau", "moment:etat_initial"), ("السطر التاني", "moment:en_cours"), ("السطر التالت", "moment:etat_final")]),
  sim("ex_2", "Question 2 : σ en fonction de x",
      "σ = Σ λᵢ·[Xᵢ], chaque concentration tirée du tableau, puis on factorise.",
      "cinetique-tableau/conductimetrie.html?vue=droite", "σ en fonction de x : une droite",
      "دابا نبينو علاش sigma كتبدل مع x. فهاد المثال ديال le cours، كاينين trois ions، و كل concentration كتجي من le tableau. كنعوضو ف la formule، ومن بعد كنجمعو اللي فيهم x. دابا نرسمو sigma en fonction de x: خط مستقيم. فالتمرين ديالنا أسهل: غير deux ions، H trois O plus و C l moins، و بجوج la concentration ديالهم x sur V. إذن sigma égale lambda de H trois O plus، plus lambda de C l moins، fois x sur V. droite كتدوز من الأصل، و كتطلع.",
      [("[H₃O⁺] = [Cl⁻] = x/V", "و بجوج la concentration ديالهم x sur V"), ("σ = (λ(H₃O⁺) + λ(Cl⁻))·x/V", "إذن sigma égale lambda de H trois O plus")],
      [("دابا نبينو", "start"), ("دابا نرسمو sigma en fonction de x", "moment:axes"), ("خط مستقيم", "moment:droite"),
       ("فالتمرين ديالنا أسهل", "moment:relation")]),
  sim("ex_3", "Question 3 : les unités de la conductimétrie",
      "λ en S·m²·mol⁻¹, concentration en mol·m⁻³, σ en S·m⁻¹.",
      "cinetique-tableau/conductimetrie.html?vue=formule", "La formule de σ et ses unités",
      "شوف la formule: sigma égale la somme des lambda i، fois la concentration de l'ion i. مثال: la soude. شوف الوحدات: lambda بالوحدة siemens mètre carré par mole، والتركيز بالوحدة mole par mètre cube، ماشي mole par litre. رد البال: une mole par litre، égale mille moles par mètre cube. فالتمرين ديالنا: x max sur V égale un virgule zéro fois dix puissance moins trois، sur un virgule zéro fois dix puissance moins quatre، يعني dix moles par mètre cube. إذن sigma f égale quarante-deux virgule six fois dix puissance moins trois، fois dix، يعني zéro virgule quatre cent vingt-six siemens par mètre.",
      [("x_max/V = 10 mol·m⁻³", "يعني dix moles par mètre cube"), ("σ_f = 42,6 × 10⁻³ × 10 = 0,426 S/m", "يعني zéro virgule quatre cent vingt-six siemens par mètre")],
      [("شوف la formule", "moment:formule"), ("مثال: la soude", "moment:exemple"), ("شوف الوحدات", "moment:unites"), ("رد البال", "moment:piege")]),
  sim("ex_4", "Question 4 : t½, la moitié de la valeur finale",
      "x(t½) = x_f/2 ; σ proportionnelle à x, donc σ½ = σ_f/2.",
      "cinetique-tableau/demi-reaction.html?vue=definition", "La définition de t½",
      "شوف la courbe ديال المثال. هنا le palier: x f égale deux virgule zéro millimoles. ناخدو la moitié ديالو: un virgule zéro millimole. la date اللي كيوصل فيها x لهاد la moitié، كنسميوها t un demi. نعاود نقرا: le temps de demi-réaction، est la durée au bout de laquelle، l'avancement atteint، la moitié de sa valeur finale. فالتمرين ديالنا، sigma proportionnelle ل x، إذن sigma un demi égale sigma f sur deux، zéro virgule deux cent treize siemens par mètre. ومن la courbe: t un demi égale cinq minutes.",
      [("σ½ = σ_f/2 = 0,213 S/m", "إذن sigma un demi égale sigma f sur deux"), ("t½ = 5 min", "t un demi égale cinq minutes")],
      [("شوف la courbe", "moment:courbe"), ("هنا le palier", "moment:palier"), ("ناخدو la moitié", "moment:moitie"),
       ("نعاود نقرا", "moment:definition")]),
  sim("ex_5", "Question 5 : v à partir de dσ/dt",
      "v = (1/V)·dx/dt ; ici x = σ·V/(λ₁ + λ₂), donc v = (1/(λ₁ + λ₂))·dσ/dt.",
      "cinetique-tableau/vitesse.html?vue=definition", "La définition de la vitesse volumique",
      "شوف la formule: v de t égale un sur V، fois d x sur d t. اللول، un sur V: V هو le volume ديال le mélange. الثاني، d x sur d t: هو le coefficient directeur ديال la tangente. والوحدة: يلا V ب le mètre cube، كنلقاو mole par mètre cube. فالتمرين ديالنا: x égale sigma fois V، sur lambda un plus lambda deux. إذن v égale un sur lambda un plus lambda deux، fois d sigma sur d t. la pente ديال T: zéro virgule zéro cinquante-neuf، إذن v de zéro égale environ un virgule trente-neuf mole par mètre cube et par minute.",
      [("v = (1/(λ₁ + λ₂))·dσ/dt", "إذن v égale un sur lambda un plus lambda deux"), ("v(0) ≈ 0,059/0,0426 ≈ 1,39 mol·m⁻³·min⁻¹", "إذن v de zéro égale environ un virgule trente-neuf")],
      [("شوف la formule", "moment:formule"), ("اللول، un sur V", "moment:volume"), ("الثاني، d x sur d t", "moment:derivee"), ("والوحدة", "moment:unite")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : x_max", "سؤال ساهل على x max.",
      "n₀(RCl) = 1,0 × 10⁻³ mol et l'eau est en excès. x_max vaut…",
      ["5,0 × 10⁻⁴ mol", "1,0 × 10⁻³ mol", "2,0 × 10⁻³ mol"], 1, {
        1: ("juste", "برافو! الما en excès، إذن R C l هو le réactif limitant، و x max égale n zéro.", "Juste : x_max = n₀ = 1,0 × 10⁻³ mol."),
        0: (("لا، قسمتي على deux بسبب deux H deux O. ولكن الما en excès، ما كيحكمش. عاود اختار.", "Le coefficient 2 est celui de l'eau, en excès. Réessaie."),
            ("الجواب: un virgule zéro fois dix puissance moins trois mole. R C l عندو le coefficient un.", "Réponse : x_max = n₀ = 1,0 × 10⁻³ mol.")),
        2: (("لا، ضربتي ف deux. le coefficient ديال R C l هو un. عاود اختار.", "Le coefficient de RCl est 1. Réessaie."),
            ("الجواب: un virgule zéro fois dix puissance moins trois mole: n zéro moins x max égale zéro.", "Réponse : n₀ − x_max = 0, x_max = 1,0 × 10⁻³ mol."))},
      "n zéro de R C l égale un virgule zéro fois dix puissance moins trois mole, et l'eau est en excès. x max vaut ?"),
  assoc("fa_2", "Plus facile : associer", "À une date t, dans le mélange.",
        "سؤال ساهل: ربط كل espèce مع la concentration ديالها à la date t.",
        "Relie chaque espèce à sa concentration à la date t (V : volume du mélange).",
        [("1", "H₃O⁺"), ("2", "Cl⁻"), ("3", "RCl")],
        [("a", "x/V"), ("b", "(n₀ − x)/V"), ("c", "n₀/V")],
        {"1": "a", "2": "a", "3": "b"},
        {"1-a": (True, "Oui : il s'est formé x mol d'ions H₃O⁺.", "برافو: تكونو x mole ديال H trois O plus."),
         "1-*": (False, "H₃O⁺ est un produit : au départ il n'y en a pas.", "لا، H trois O plus produit: فالبداية ما كاينش."),
         "2-a": (True, "Oui : autant d'ions Cl⁻ que d'ions H₃O⁺, x mol.", "برافو: نفس العدد ديال H trois O plus، x mole."),
         "2-*": (False, "Cl⁻ est un produit, de coefficient 1 : il y en a x mol.", "لا، C l moins produit، عندو x mole."),
         "3-b": (True, "Oui : le réactif diminue de x.", "برافو: le réactif كينقص ب x."),
         "3-*": (False, "RCl est un réactif : il en reste n₀ − x.", "لا، R C l réactif: كيبقى منو n zéro moins x.")},
        ("[H₃O⁺] = [Cl⁻] = x/V et [RCl] = (n₀ − x)/V : seuls les ions comptent dans σ.", "les ions بجوج x sur V، و R C l n zéro moins x sur V. غير les ions اللي كيحسبو ف sigma.")),
  qcm("fa_3", "Plus facile : les unités", "سؤال ساهل على الوحدات.",
      "V = 100 mL. En m³, cela fait…",
      ["1,0 × 10⁻⁴ m³", "0,1 m³", "1,0 × 10⁻¹ L"], 0, {
        0: ("juste", "برافو! un litre égale dix puissance moins trois mètre cube، إذن cent millilitres égale dix puissance moins quatre mètre cube.", "Juste : 100 mL = 0,1 L = 1,0 × 10⁻⁴ m³."),
        1: (("لا، zéro virgule un هي ب litre، ماشي ب mètre cube. عاود اختار.", "0,1 est en litres, pas en m³. Réessaie."),
            ("الجواب: un virgule zéro fois dix puissance moins quatre mètre cube.", "Réponse : 1,0 × 10⁻⁴ m³ (1 L = 10⁻³ m³).")),
        2: (("هادي صحيحة ب litre، ولكن السؤال ب mètre cube. عاود اختار.", "Juste en litres, mais on demande des m³. Réessaie."),
            ("الجواب: un virgule zéro fois dix puissance moins quatre mètre cube.", "Réponse : 1,0 × 10⁻⁴ m³."))},
      "V égale cent millilitres. En mètre cube, cela fait ?"),
  vf("fa_4", "Plus facile : vrai ou faux", "σ_f = 0,426 S/m.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("À t½, σ = σ_f/2 = 0,213 S/m.", True, "σ est proportionnelle à x, et x(t½) = x_f/2."),
      ("t½ est la moitié de la durée totale de l'expérience, 20 min.", False, "t½ se lit à σ_f/2 sur la courbe, pas au milieu de l'axe des temps."),
      ("On lit t½ en descendant du point de la courbe jusqu'à l'axe des temps.", True, "Horizontale depuis σ½, puis verticale jusqu'à l'axe des temps.")]),
  qcm("fa_5", "Plus facile : la bonne relation", "سؤال ساهل: اختار la bonne relation.",
      "σ = (λ₁ + λ₂)·x/V. La vitesse volumique v = (1/V)·dx/dt s'écrit…",
      ["v = (λ₁ + λ₂)·dσ/dt", "v = (1/V)·dσ/dt", "v = (1/(λ₁ + λ₂))·dσ/dt"], 2, {
        2: ("juste", "برافو! x égale sigma fois V sur lambda un plus lambda deux، و V كيمشي.", "Juste : x = σ·V/(λ₁ + λ₂), donc v = (1/(λ₁ + λ₂))·dσ/dt."),
        0: (("لا، les lambda خاصهم يكونو لتحت. شوف x égale sigma fois V على شنو؟ عاود اختار.", "Les λ sont au dénominateur quand on isole x. Réessaie."),
            ("الجواب: v égale un sur lambda un plus lambda deux، fois d sigma sur d t.", "Réponse : v = (1/(λ₁ + λ₂))·dσ/dt.")),
        1: (("لا، d sigma ماشي d x. خاصك تعوض x ب sigma fois V sur les lambda. عاود اختار.", "dσ n'est pas dx : remplace x par σ·V/(λ₁ + λ₂). Réessaie."),
            ("الجواب: v égale un sur lambda un plus lambda deux، fois d sigma sur d t.", "Réponse : v = (1/(λ₁ + λ₂))·dσ/dt."))},
      "sigma égale lambda un plus lambda deux, fois x sur V. La vitesse volumique s'écrit ?"),
]

SIM_Q = [
  QS("1", "Dresser le tableau d'avancement et déterminer x_max.",
     val("x_max", sN0, "mol", "eau en excès : x_max = n₀ = 2,0 × 10⁻³ mol"),
     (["n₀ − x", "excès"], ["x_max = n₀/2"]),
     [("RCl limitant (eau en excès) : n₀ − x_max = 0", "n zéro moins x max égale zéro"), ("x_max = 2,0 × 10⁻³ mol", "x max égale deux virgule zéro")],
     "الما en excès، إذن n zéro moins x max égale zéro، و x max égale deux virgule zéro fois dix puissance moins trois mole."),
  QS("2", "Montrer que σ = (λ(H₃O⁺) + λ(Cl⁻))·x/V.",
     phrase("σ = λ(H₃O⁺)·[H₃O⁺] + λ(Cl⁻)·[Cl⁻] avec [H₃O⁺] = [Cl⁻] = x/V, donc σ = (λ(H₃O⁺) + λ(Cl⁻))·x/V."),
     (["σ = Σ λᵢ·[Xᵢ]", "x/V"], ["σ = λ·x"]),
     [("σ = λ(H₃O⁺)·[H₃O⁺] + λ(Cl⁻)·[Cl⁻]", "sigma égale"), ("[H₃O⁺] = [Cl⁻] = x/V, donc σ = (λ₁ + λ₂)·x/V", "x sur V")],
     "sigma égale lambda de H trois O plus fois sa concentration، plus lambda de C l moins fois sa concentration. بجوج x sur V، إذن sigma égale lambda un plus lambda deux، fois x sur V."),
  QS("3", "Calculer σ_f et vérifier que la réaction est totale.",
     val("σ_f", sSF, "S/m", "σ_f = 42,6 × 10⁻³ × 2,0 × 10⁻³/(1,0 × 10⁻⁴) = 0,852 S/m"),
     (["σ_f = (λ₁ + λ₂)·x_max/V", "m³"], ["V = 100 mL dans la relation"]),
     [("σ_f = 42,6 × 10⁻³ × 2,0 × 10⁻³/(1,0 × 10⁻⁴) = 0,852 S/m", "sigma f égale zéro virgule huit cent cinquante-deux"),
      ("égale au palier de la courbe : réaction totale", "la réaction totale")],
     "sigma f égale lambda un plus lambda deux، fois x max sur V: sigma f égale zéro virgule huit cent cinquante-deux siemens par mètre. نفس le palier ديال la courbe، إذن la réaction totale."),
  QS("4", "Montrer que σ½ = σ_f/2, puis déterminer t½.",
     val("t½", sT12, "min", "σ½ = 0,426 S/m ; t½ = 4 min", tol=0.06),
     (["σ½ = σ_f/2", "t½"], ["t½ = t_f/2"]),
     [("σ proportionnelle à x : σ½ = σ_f/2 = 0,426 S/m", "sigma un demi égale sigma f sur deux"), ("t½ = 4 min", "t un demi égale quatre minutes")],
     "sigma proportionnelle ل x، إذن sigma un demi égale sigma f sur deux، يعني zéro virgule quatre cent vingt-six. على la courbe: t un demi égale quatre minutes."),
  QS("5", "Montrer que v = (1/(λ(H₃O⁺) + λ(Cl⁻)))·dσ/dt, puis calculer v(0) en mol·m⁻³·min⁻¹.",
     val("v(0)", sV0, "mol·m⁻³·min⁻¹", "v(0) = (0,591/4)/(42,6 × 10⁻³) ≈ 3,47 mol·m⁻³·min⁻¹", tol=0.04),
     (["v = (1/V)·dx/dt", "(dσ/dt)₀"], ["v = dσ/dt"]),
     [("v = (1/(λ₁ + λ₂))·dσ/dt ; (dσ/dt)₀ = 0,591/4 ≈ 0,148 S·m⁻¹·min⁻¹", "la pente"),
      ("v(0) ≈ 3,47 mol·m⁻³·min⁻¹", "v de zéro égale environ trois virgule quarante-sept")],
     "v égale un sur lambda un plus lambda deux، fois d sigma sur d t. la pente égale environ zéro virgule cent quarante-huit. إذن v de zéro égale environ trois virgule quarante-sept moles par mètre cube et par minute."),
]

EX = exercice(
  "phys_ex_ch10_cinetique_4", "phys_ch10_cinetique", "cinetique",
  "L'hydrolyse du chlorure de tertiobutyle : suivi par conductimétrie", "moyen", 30,
  ["Dresser un tableau d'avancement", "Établir σ en fonction de x", "Déterminer t½ à partir de σ", "Calculer v(0) en mol·m⁻³·min⁻¹"],
  "À la date t = 0, on introduit n₀ = 1,0 × 10⁻³ mol de 2-chloro-2-méthylpropane, noté RCl, dans un mélange d'eau et d'acétone ; le volume du mélange est V = 100 mL et reste constant. La réaction, lente, a pour équation : " + TAB + ". On suit la conductivité σ du mélange avec une cellule conductimétrique ; la figure donne σ en fonction du temps et la tangente (T) en t = 0.",
  "دابا نقراو l'énoncé. فt égale zéro، كنحطو un virgule zéro fois dix puissance moins trois mole ديال R C l، فخليط ديال الما و l'acétone. le volume ديال le mélange، V égale cent millilitres. la réaction بطيئة: R C l، plus deux molécules d'eau، كيعطيو R O H، و l'ion H trois O plus، و l'ion C l moins. كنتبعو la conductivité sigma، و la figure كتعطي sigma en fonction du temps، مع la tangente T à t égale zéro.",
  [FIG],
  ["n₀(RCl) = 1,0 × 10⁻³ mol ; V = 100 mL (constant)", "λ(H₃O⁺) = 35,0 mS·m²·mol⁻¹ ; λ(Cl⁻) = 7,6 mS·m²·mol⁻¹",
   "On néglige la conductivité due aux ions HO⁻ et à l'eau.", "Tangente (T) : O(0 ; 0) et B(6 min ; 0,354 S/m)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Même réaction, même volume V = 100 mL, mais n₀(RCl) = 2,0 × 10⁻³ mol. La figure donne σ en fonction du temps et la tangente (T) en t = 0.",
  "نفس التمرين، بقيم أخرى: نفس le volume، ولكن n zéro de R C l égale deux virgule zéro fois dix puissance moins trois mole.",
  [sFIG],
  ["n₀(RCl) = 2,0 × 10⁻³ mol ; V = 100 mL", "λ(H₃O⁺) = 35,0 mS·m²·mol⁻¹ ; λ(Cl⁻) = 7,6 mS·m²·mol⁻¹", "Tangente (T) : O(0 ; 0) et B(4 min ; 0,591 S/m)"],
  SIM_Q)

ecrire(EX)
