# Exercice de chimie, ch. 10 (suivi temporel, vitesse de réaction), niveau difficile (« Supérieur ») : deux
# expériences à deux températures, document = concentration d'un RÉACTIF en fonction du temps (moins guidé) ;
# « montrer que » v = −d[H₂O₂]/dt, v(0) par la tangente, t½ sur une courbe qui descend, attribution des courbes,
# concentration d'un produit par le tableau, lecture critique d'une affirmation.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2017 N (2.2 t½ de deux expériences, réaction la plus rapide), 2023 N (3.2
#    courbe avec catalyseur, 3.4 t½ de la courbe C₂), 2024 N (1.a-1.c vrai/faux facteurs cinétiques), 2025 N (2.2
#    courbe de l'expérience (3), 2.3 vrai/faux « x_f le même pour les trois expériences », 2.4 t½), 2021 N (2.3
#    « montrer que » une expression de v) — backend/data/exams/physique ;
#  - profs : architecture/sources_chimie_ch9_ch11.md, chapitre B (« exprimer v en fonction d'une concentration :
#    v = −(1/α)·d[A]/dt », Mahajar-Tabit, El Founani, Sbiro ; facteurs cinétiques chez El Goufifa et Boulouiha) et
#    phys_ch10_cinetique.md (le signe moins pour un réactif ; même palier, t½ différents) ;
#  - séries en ligne (titres et résumés lus par recherche ; PDF non ouverts, réseau du conteneur limité) :
#    talamidi (suivi temporel séries 1 et 2), moutamadris (suivi temporel 2022, fiches 13-7 et 13-8), alloschool
#    (élément 119798), coursdusoirpc (TD B. Mouslim), pc1.ma (fiches El Founani / Hadjyne).
# Ici : nos concentrations, nos deux températures et nos courbes (calculées : [H₂O₂] = [H₂O₂]₀·2^(−t/t½)).
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *

# ------------------------------------------------------------------ données
C0, V = 40.0, 0.100                    # mmol/L, L
TA, TB = 6.0, 2.0                      # t½ des courbes (a) 25 °C et (b) 40 °C
def conc(c0, t12):
    k = math.log(2) / t12
    return (lambda t: c0 * math.exp(-k * t)), f"{c0}*exp(-{k:.6f}*x)", k
ca, ea, ka = conc(C0, TA)
cb, eb, kb = conc(C0, TB)
yB = round(C0 - C0 * ka * 8, 1)
assert yB == 3.0, yB
V0 = -(yB - C0) / 8                    # 4,625 mmol·L⁻¹·min⁻¹
assert abs(V0 - 4.625) < 1e-9 and abs(V0 - C0 * ka) / V0 < 0.01
assert abs(ca(TA) - 20) < 1e-9 and abs(cb(TB) - 20) < 1e-9
CB4 = cb(4)                            # 10 mmol/L
CI2 = C0 - CB4                         # 30 mmol/L
assert abs(CB4 - 10) < 1e-9 and abs(CI2 - 30) < 1e-9

def fig(c0, ea_, eb_, tmax, gx, gy, B):
    return courbe_fig("Concentration de l'eau oxygénée en fonction du temps",
        ((0, tmax, "t", "min", gx), (0, gy[-1], "[H₂O₂]", "mmol/L", gy)),
        [{"f": "courbe", "expr": ea_, "de": 0, "a": tmax, "couleur": "cyan", "texte": "(a)", "texte_x": 10, "pos": "ne"},
         {"f": "courbe", "expr": eb_, "de": 0, "a": tmax, "couleur": "rose", "texte": "(b)", "texte_x": 3, "pos": "ne"},
         {"f": "courbe", "expr": f"{c0}-{(c0-B[1])/B[0]:.6f}*x", "de": 0, "a": B[0], "couleur": "orange", "trait": "pointille"},
         {"f": "point", "at": [0, c0], "t": f"A (0 ; {fr(c0, 0)})", "pos": "e", "couleur": "orange"},
         {"f": "point", "at": list(B), "t": f"B ({B[0]} ; {fr(B[1], 1)})", "pos": "ne", "couleur": "orange"}],
        legende="(T) : tangente à la courbe (a) en t = 0, passant par A et B ; coordonnées en (min ; mmol/L).")

FIG = fig(C0, ea, eb, 30, [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30], [0, 5, 10, 15, 20, 25, 30, 35, 40], (8, yB))

# ------------------------------------------------------------------ similaire
sC0, sTA, sTB = 30.0, 8.0, 3.0
sca, sea, ska = conc(sC0, sTA)
scb, seb, skb = conc(sC0, sTB)
syB = round(sC0 - sC0 * ska * 10, 1)
assert syB == 4.0, syB
sV0 = -(syB - sC0) / 10                 # 2,6
sCB6 = scb(6)                           # 7,5
sCI2 = sC0 - sCB6                       # 22,5
assert abs(sCB6 - 7.5) < 1e-9
sFIG = fig(sC0, sea, seb, 40, [0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36, 39], [0, 5, 10, 15, 20, 25, 30], (10, syB))

QUESTIONS = [
  Q("1", "Montrer que, le volume V restant constant, la vitesse volumique de la réaction s'écrit v = −d[H₂O₂]/dt.",
    "السؤال un: le volume V ثابت. بين أن la vitesse volumique، v égale moins d de la concentration d'eau oxygénée sur d t.",
    phrase("D'après le tableau n(H₂O₂) = n₀ − x, donc x = n₀ − [H₂O₂]·V ; v = (1/V)·dx/dt = (1/V)·(−V·d[H₂O₂]/dt) = −d[H₂O₂]/dt (n₀ et V constants)."),
    (["v = (1/V)·dx/dt", "n(H₂O₂) = n₀ − x", "[H₂O₂] = n/V", "dn₀/dt = 0"], ["v = d[H₂O₂]/dt", "n(H₂O₂) = x"]),
    [("Exprime x en fonction de n(H₂O₂) à l'aide du tableau d'avancement : l'eau oxygénée est un réactif.",
      "عبر على x ب n d'eau oxygénée من le tableau: l'eau oxygénée réactif، إذن كتنقص."),
     ("x = n₀ − [H₂O₂]·V. Dérive : n₀ et V sont constants. Remplace dans v = (1/V)·dx/dt.",
      "x égale n zéro moins la concentration fois V. اشتق: n zéro و V ثابتين. ومن بعد عوض فv égale un sur V fois d x sur d t.")],
    [("1 : tableau : n(H₂O₂) = n₀ − x, donc x = n₀ − [H₂O₂]·V", "x égale n zéro moins"),
     ("dx/dt = −V·d[H₂O₂]/dt (n₀ et V constants)", "n zéro و V ثابتين"),
     ("v = (1/V)·dx/dt = −d[H₂O₂]/dt", "إذن v égale moins d de la concentration sur d t")],
    "السؤال un. من le tableau: n d'eau oxygénée égale n zéro moins x، إذن x égale n zéro moins la concentration fois V. كنشتقو، و n zéro و V ثابتين: d x sur d t égale moins V fois d de la concentration sur d t. نعوضو فv égale un sur V fois d x sur d t. إذن v égale moins d de la concentration sur d t. le moins حيت réactif، باش v تكون موجبة.",
    "ex_1", "fa_1"),
  Q("2", "Calculer la vitesse volumique v(0) de la réaction correspondant à la courbe (a), à t = 0.",
    "السؤال deux: حسب la vitesse volumique v de zéro ديال la courbe a، à t égale zéro.",
    val("v(0)", V0, "mmol·L⁻¹·min⁻¹", "v(0) = −(d[H₂O₂]/dt)₀ = −(3,0 − 40)/(8 − 0) ≈ 4,6 mmol·L⁻¹·min⁻¹", tol=0.04),
    (["v = −d[H₂O₂]/dt", "(T)", "A", "B", "mmol·L⁻¹·min⁻¹"], ["v = −4,6 mmol·L⁻¹·min⁻¹", "v = (1/V)·d[H₂O₂]/dt"]),
    [("La pente de (T) se calcule entre A et B : elle est négative, car la concentration d'un réactif diminue.",
      "la pente ديال T كتحسبها بين A و B: هي سالبة، حيت la concentration ديال réactif كتنقص."),
     ("v(0) = −pente : le signe moins de la relation rend la vitesse positive. Ici, pas de 1/V : la concentration est déjà « par litre ».",
      "v de zéro égale moins la pente: le moins كيرد la vitesse موجبة. وهنا ما كاينش un sur V: la concentration ديجا par litre.")],
    [("2 : v(0) = −(d[H₂O₂]/dt)₀ (pente de la tangente (T))", "v de zéro égale moins la pente"),
     ("pente = (3,0 − 40)/(8 − 0) ≈ −4,6 mmol·L⁻¹·min⁻¹", "la pente égale environ moins quatre virgule six"),
     ("v(0) ≈ 4,6 mmol·L⁻¹·min⁻¹", "v de zéro égale environ quatre virgule six millimoles par litre et par minute")],
    "السؤال deux. v de zéro égale moins la pente ديال la tangente T. la pente: trois virgule zéro moins quarante، sur huit moins zéro، يعني la pente égale environ moins quatre virgule six millimoles par litre et par minute. إذن v de zéro égale environ quatre virgule six millimoles par litre et par minute، موجبة.",
    "ex_2", "fa_2"),
  Q("3", "La réaction est totale et H₂O₂ est le réactif limitant. Montrer qu'à t½, [H₂O₂] = [H₂O₂]₀/2, puis déterminer t½ pour la courbe (a).",
    "السؤال trois: la réaction totale و l'eau oxygénée réactif limitant. بين أن à t un demi، la concentration égale la concentration initiale sur deux، ومن بعد حدد t un demi ديال la courbe a.",
    val("t½(a)", TA, "min", "[H₂O₂](t½) = [H₂O₂]₀/2 = 20 mmol/L ; t½(a) = 6 min", tol=0.06),
    (["x_f = x_max = n₀", "x(t½) = x_f/2", "[H₂O₂]₀/2", "t½"], ["[H₂O₂](t½) = 0", "t½ = 15 min"]),
    [("H₂O₂ limitant et réaction totale : x_f = x_max = n₀. À t½, x = n₀/2 : combien reste-t-il d'eau oxygénée ?",
      "l'eau oxygénée limitant و la réaction totale: x f égale n zéro. à t un demi، x égale n zéro sur deux. شحال باقي من l'eau oxygénée؟"),
     ("n(H₂O₂) = n₀ − n₀/2 = n₀/2, donc [H₂O₂] = [H₂O₂]₀/2 = 20 mmol/L : lis la date sur la courbe (a).",
      "n égale n zéro moins n zéro sur deux، يعني n zéro sur deux. إذن la concentration égale vingt millimoles par litre: قرا la date على la courbe a.")],
    [("3 : x_f = x_max = n₀ ; à t½, x = n₀/2 donc n(H₂O₂) = n₀ − n₀/2 = n₀/2", "x égale n zéro sur deux"),
     ("[H₂O₂](t½) = [H₂O₂]₀/2 = 40/2 = 20 mmol/L", "vingt millimoles par litre"),
     ("lecture sur (a) : t½(a) = 6 min (et sur (b) : t½(b) = 2 min)", "t un demi ديال la courbe a égale six minutes")],
    "السؤال trois. la réaction totale و l'eau oxygénée limitant، إذن x f égale n zéro. à t un demi، x égale n zéro sur deux، و n d'eau oxygénée égale n zéro moins n zéro sur deux، يعني n zéro sur deux. إذن la concentration à t un demi égale quarante sur deux، vingt millimoles par litre. على la courbe a: t un demi ديال la courbe a égale six minutes. و على la courbe b: deux minutes.",
    "ex_3", "fa_3"),
  Q("4", "L'une des expériences est faite à 25 °C, l'autre à 40 °C, avec les mêmes quantités initiales. Attribuer chaque courbe à sa température. Justifier.",
    "السؤال quatre: وحدة من les expériences ب vingt-cinq degrés Celsius، و الأخرى ب quarante degrés Celsius، بنفس les quantités initiales. ربط كل courbe مع la température ديالها، وعلل.",
    phrase("t½(b) = 2 min < t½(a) = 6 min : la réaction (b) est la plus rapide. La température est un facteur cinétique (plus de chocs efficaces quand elle augmente) : (b) correspond à 40 °C et (a) à 25 °C."),
    (["t½(b) < t½(a)", "facteur cinétique", "plus rapide", "40 °C"], ["(a) à 40 °C", "même t½"]),
    [("Compare les deux t½ : laquelle des deux réactions est la plus rapide ?",
      "قارن deux t un demi: شمن réaction اللي أسرع؟"),
     ("Plus la température est élevée, plus la réaction est rapide (facteur cinétique), donc plus t½ est petit.",
      "كلما طلعت la température، كلما la réaction أسرع، و t un demi أصغر.")],
    [("4 : t½(b) = 2 min < t½(a) = 6 min : la réaction (b) est la plus rapide", "la réaction b هي الأسرع"),
     ("la température est un facteur cinétique : (b) ↔ 40 °C, (a) ↔ 25 °C", "la courbe b ديال quarante degrés Celsius")],
    "السؤال quatre. t un demi ديال b، deux minutes، صغيرة من t un demi ديال a، six minutes: la réaction b هي الأسرع. و la température facteur cinétique: كلما طلعت، كاينين plus de chocs efficaces par unité de temps. إذن la courbe b ديال quarante degrés Celsius، و la courbe a ديال vingt-cinq degrés Celsius.",
    "ex_4", "fa_4"),
  Q("5", "Pour l'expérience à 40 °C, déterminer la concentration du diiode [I₂] à la date t = 4 min.",
    "السؤال cinq: فl'expérience ديال quarante degrés Celsius، حدد la concentration ديال le diiode à t égale quatre minutes.",
    val("[I₂]", CI2, "mmol/L", "[I₂] = [H₂O₂]₀ − [H₂O₂](4 min) = 40 − 10 = 30 mmol/L", tol=0.05),
    (["n(I₂) = x", "x = n₀ − n(H₂O₂)", "[I₂] = [H₂O₂]₀ − [H₂O₂]", "courbe (b)", "mmol/L"], ["[I₂] = [H₂O₂]", "courbe (a)"]),
    [("Sur la courbe (b), lis [H₂O₂] à t = 4 min. Puis cherche dans le tableau le lien entre le diiode formé et l'eau oxygénée consommée.",
      "على la courbe b، قرا la concentration d'eau oxygénée à quatre minutes. ومن بعد شوف فle tableau: le diiode اللي تكون والما الأكسيجيني اللي تستهلك."),
     ("n(I₂) = x = n₀ − n(H₂O₂) ; en divisant par V : [I₂] = [H₂O₂]₀ − [H₂O₂].",
      "n de I deux égale x، égale n zéro moins n d'eau oxygénée. نقسمو على V: la concentration de diiode égale quarante moins la concentration d'eau oxygénée.")],
    [("5 : tableau : n(I₂) = x = n₀ − n(H₂O₂), donc [I₂] = [H₂O₂]₀ − [H₂O₂]", "n de I deux égale x"),
     ("sur (b) à t = 4 min : [H₂O₂] = 10 mmol/L", "dix millimoles par litre"),
     ("[I₂] = 40 − 10 = 30 mmol/L", "la concentration de diiode égale trente millimoles par litre")],
    "السؤال cinq. من le tableau: n de I deux égale x، و x égale n zéro moins n d'eau oxygénée. نقسمو على V: la concentration de diiode égale la concentration initiale d'eau oxygénée، moins la concentration d'eau oxygénée. على la courbe b، à quatre minutes: dix millimoles par litre. إذن la concentration de diiode égale trente millimoles par litre.",
    "ex_5", "fa_5"),
  Q("6", "Un élève affirme : « à 40 °C, on obtient finalement plus de diiode qu'à 25 °C ». Discuter cette affirmation.",
    "السؤال six: واحد التلميذ قال: ف quarante degrés Celsius، فاللخر كنلقاو diiode كثر من vingt-cinq degrés Celsius. ناقش هاد الجملة.",
    phrase("Faux : la température change la vitesse, pas l'état final. Mêmes quantités initiales, réaction totale, H₂O₂ limitant : x_f = n₀ dans les deux cas, [I₂]_f = 40 mmol/L ; les deux courbes tendent vers 0."),
    (["état final", "x_f = x_max", "[I₂]_f = 40 mmol/L", "faux"], ["vrai", "x_f plus grand à 40 °C"]),
    [("Regarde la fin des deux courbes : vers quelle valeur tend [H₂O₂] dans chaque expérience ?",
      "شوف اللخر ديال deux courbes: فين كتوصل la concentration d'eau oxygénée فكل وحدة؟"),
     ("x_f dépend des quantités initiales et du réactif limitant, pas de la température.",
      "x f كيتعلق ب les quantités initiales و le réactif limitant، ماشي ب la température.")],
    [("6 : faux : les deux courbes tendent vers [H₂O₂] = 0", "l'affirmation fausse"),
     ("mêmes quantités initiales, H₂O₂ limitant : x_f = n₀ dans les deux cas, [I₂]_f = 40 mmol/L", "نفس l'état final"),
     ("la température change seulement la vitesse (t½), pas l'état final", "la température كتبدل غير la vitesse")],
    "السؤال six. l'affirmation fausse. deux courbes كيوصلو ل zéro: l'eau oxygénée كتسالى فبجوج. نفس les quantités initiales، إذن نفس l'état final: x f égale n zéro، و la concentration finale de diiode égale quarante millimoles par litre فبجوج. la température كتبدل غير la vitesse، يعني t un demi.",
    "ex_6", "fa_6"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : la vitesse à partir d'un réactif",
      "n(réactif) = n₀ − x : v = −(1/V)·dn/dt = −d[réactif]/dt.",
      "cinetique-tableau/vitesse.html?vue=concentration", "La concentration de l'eau oxygénée diminue",
      "شي مرات le sujet ما كيعطيناش x en fonction du temps. كيعطينا la concentration ديال réactif. شوف la courbe ديال l'eau oxygénée: كتهبط، حيت هي réactif. من le tableau: la quantité d'eau oxygénée égale n zéro moins x، إذن x égale n zéro moins la quantité d'eau oxygénée. كنشتقو: n zéro ما كيتبدلش. إذن v égale moins un sur V، fois d n d'eau oxygénée sur d t. و V ما كيتبدلش، إذن v égale moins d de la concentration sur d t. رد البال: ل réactif، ديما moins، باش v تكون موجبة.",
      [("x = n₀ − n(H₂O₂)", "إذن x égale n zéro moins la quantité d'eau oxygénée"), ("v = −d[H₂O₂]/dt", "إذن v égale moins d de la concentration sur d t")],
      [("شوف la courbe ديال l'eau oxygénée", "moment:courbe_reactif")]),
  sim("ex_2", "Question 2 : la pente d'une tangente",
      "Deux points éloignés de la tangente ; ici la pente est négative.",
      "cinetique-tableau/vitesse.html?vue=tangente", "La tangente en t = 0 et deux de ses points",
      "شوف la courbe. كنختارو la date t égale zéro، هادا هو le point. دابا كنرسمو la tangente. باش نحسبو la pente، كناخدو deux points ديال la tangente، بعاد على بعضياتهم. فهاد المثال la courbe طالعة، و la pente موجبة. فالتمرين ديالنا la courbe هابطة: A، zéro و quarante، و B، huit minutes و trois virgule zéro. la pente égale environ moins quatre virgule six millimoles par litre et par minute. و v égale moins la pente: v de zéro égale environ quatre virgule six millimoles par litre et par minute.",
      [("pente = (3,0 − 40)/8 ≈ −4,6 mmol·L⁻¹·min⁻¹", "la pente égale environ moins quatre virgule six"), ("v(0) ≈ 4,6 mmol·L⁻¹·min⁻¹", "v de zéro égale environ quatre virgule six")],
      [("شوف la courbe", "moment:courbe"), ("كنختارو la date t égale zéro", {"set": {"t": 0}}), ("هادا هو le point", "moment:point"),
       ("دابا كنرسمو la tangente", "moment:tangente"), ("كناخدو deux points", "moment:deux_points"), ("فهاد المثال", "moment:pente")]),
  sim("ex_3", "Question 3 : t½ sur une courbe qui descend",
      "À t½, x = x_f/2 ; pour un réactif limitant, il en reste la moitié.",
      "cinetique-tableau/demi-reaction.html?vue=definition", "La définition de t½",
      "شوف la courbe ديال المثال. هنا le palier: x f égale deux virgule zéro millimoles. ناخدو la moitié ديالو: un virgule zéro millimole. نعاود نقرا: le temps de demi-réaction، est la durée au bout de laquelle، l'avancement atteint، la moitié de sa valeur finale. و la relation: x de t un demi égale x f sur deux. فالتمرين ديالنا، x f égale n zéro، إذن à t un demi باقي النص ديال l'eau oxygénée: vingt millimoles par litre. على la courbe a: t un demi égale six minutes.",
      [("[H₂O₂](t½) = 40/2 = 20 mmol/L", "vingt millimoles par litre"), ("t½(a) = 6 min", "t un demi égale six minutes")],
      [("شوف la courbe", "moment:courbe"), ("هنا le palier", "moment:palier"), ("ناخدو la moitié", "moment:moitie"),
       ("نعاود نقرا", "moment:definition"), ("و la relation", "moment:relation")]),
  sim("ex_4", "Question 4 : la courbe rapide et la courbe lente",
      "Plus t½ est petit, plus la transformation est rapide ; la température accélère.",
      "cinetique-tableau/temperature.html?vue=demi", "Deux températures, deux t½",
      "شوف les axes. هادي la courbe lente، ديال vingt degrés Celsius. وهادي la courbe rapide، ديال quarante degrés Celsius. نقراو t un demi ديال كل وحدة: à quarante degrés Celsius، t un demi صغيرة. إذن plus t un demi est petit، plus la transformation est rapide. فالتمرين ديالنا: la courbe b، t un demi deux minutes، هي الأسرع: هي ديال quarante degrés Celsius. و la courbe a، six minutes، ديال vingt-cinq degrés Celsius.",
      [("t½(b) = 2 min < t½(a) = 6 min", "la courbe b، t un demi deux minutes"), ("(b) : 40 °C ; (a) : 25 °C", "هي ديال quarante degrés Celsius")],
      [("شوف les axes", "moment:axes"), ("هادي la courbe lente", "moment:courbe_lente"), ("وهادي la courbe rapide", "moment:courbe_rapide"),
       ("نقراو t un demi", "moment:deux_t_demi"), ("إذن plus t un demi", "moment:conclusion")]),
  sim("ex_5", "Question 5 : le produit par le tableau",
      "Ce qui disparaît d'eau oxygénée apparaît en diiode : n(I₂) = x = n₀ − n(H₂O₂).",
      "cinetique-tableau/avancement.html?vue=tableau&depart=etat_initial", "Le tableau : réactif n₀ − x, produit x",
      "رجعنا ل le tableau ديال l'état initial. السطر التاني: en cours. l'eau oxygénée: n zéro moins x. le diiode: x. السطر التالت: l'état final. إذن كل eau oxygénée اللي مشات، كيجي فبلاصتها diiode واحد. فالتمرين ديالنا: à quatre minutes، على la courbe b، باقي dix millimoles par litre ديال l'eau oxygénée. إذن la concentration de diiode égale quarante moins dix، trente millimoles par litre.",
      [("[I₂] = [H₂O₂]₀ − [H₂O₂]", "كيجي فبلاصتها diiode واحد"), ("[I₂] = 40 − 10 = 30 mmol/L", "trente millimoles par litre")],
      [("رجعنا ل le tableau", "moment:etat_initial"), ("السطر التاني", "moment:en_cours"), ("السطر التالت", "moment:etat_final")]),
  sim("ex_6", "Question 6 : même état final",
      "La température change la vitesse, pas le palier.",
      "cinetique-tableau/temperature.html?vue=vitesse", "Deux températures, même palier",
      "شوف les axes. هادي la courbe ديال vingt degrés Celsius. وهادي la courbe ديال quarante degrés Celsius، كتطلع دغيا. ولكن شوف le palier: بجوج كيوقفو ف deux virgule zéro millimoles. نفس l'état final. فالتمرين ديالنا نفس الشي: deux courbes كيوصلو ل zéro ديال l'eau oxygénée، و la concentration finale de diiode quarante millimoles par litre فبجوج. إذن l'affirmation fausse.",
      [("même état final : [I₂]_f = 40 mmol/L", "la concentration finale de diiode quarante"), ("l'affirmation est fausse", "إذن l'affirmation fausse")],
      [("شوف les axes", "moment:axes"), ("هادي la courbe ديال vingt degrés Celsius", "moment:courbe_20"),
       ("وهادي la courbe ديال quarante degrés Celsius", "moment:courbe_40"), ("ولكن شوف le palier", "moment:meme_final")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : le signe", "سؤال ساهل على le signe.",
      "Pour un réactif de concentration [A], à volume constant, la vitesse volumique s'écrit…",
      ["v = d[A]/dt", "v = −(1/V)·d[A]/dt", "v = −d[A]/dt"], 2, {
        2: ("juste", "برافو! réactif، إذن moins، و la concentration ديجا par litre.", "Juste : v = −d[A]/dt."),
        0: (("لا، la concentration ديال réactif كتنقص، إذن la pente سالبة. بلا moins، v تولي سالبة. عاود اختار.", "Sans le signe moins, v serait négative pour un réactif. Réessaie."),
            ("الجواب: v égale moins d A sur d t.", "Réponse : v = −d[A]/dt.")),
        1: (("قريب! ولكن un sur V كيكون مع la quantité n، ماشي مع la concentration. عاود اختار.", "Le 1/V va avec n, pas avec la concentration. Réessaie."),
            ("الجواب: v égale moins d A sur d t: la concentration هي ديجا n sur V.", "Réponse : v = −d[A]/dt."))},
      "Pour un réactif de concentration A, à volume constant, la vitesse volumique s'écrit ?"),
  qcm("fa_2", "Plus facile : v(0)", "سؤال ساهل: اختار la bonne valeur.",
      "La tangente en t = 0 a une pente de −4,6 mmol·L⁻¹·min⁻¹ sur la courbe [H₂O₂](t). v(0) vaut…",
      ["4,6 mmol·L⁻¹·min⁻¹", "−4,6 mmol·L⁻¹·min⁻¹", "46 mmol·L⁻¹·min⁻¹"], 0, {
        0: ("juste", "برافو! v égale moins la pente، موجبة.", "Juste : v(0) = −(−4,6) = 4,6 mmol·L⁻¹·min⁻¹."),
        1: (("لا، la vitesse volumique ديما موجبة. نسيتي le moins ديال la relation. عاود اختار.", "Une vitesse volumique est positive : tu as oublié le signe moins. Réessaie."),
            ("الجواب: quatre virgule six، v égale moins la pente.", "Réponse : v(0) = 4,6 mmol·L⁻¹·min⁻¹.")),
        2: (("لا، ما كاين حتى قسمة على V هنا. عاود اختار.", "Pas de division par V ici. Réessaie."),
            ("الجواب: quatre virgule six millimoles par litre et par minute.", "Réponse : v(0) = 4,6 mmol·L⁻¹·min⁻¹."))},
      "La tangente en t égale zéro a une pente de moins quatre virgule six. v de zéro vaut ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "[H₂O₂]₀ = 40 mmol/L, réaction totale, H₂O₂ limitant.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("À t½, il reste [H₂O₂] = 20 mmol/L.", True, "x = x_f/2 = n₀/2 : la moitié de l'eau oxygénée a réagi."),
      ("À t½, l'eau oxygénée est épuisée.", False, "Elle est épuisée à la fin, pas à t½."),
      ("À 2·t½, la réaction est terminée.", False, "À 2·t½, il reste encore le quart : la réaction n'est pas finie.")]),
  qcm("fa_4", "Plus facile : la plus rapide", "سؤال ساهل: شمن réaction أسرع؟",
      "t½(a) = 6 min et t½(b) = 2 min. Quelle courbe correspond à la température la plus élevée ?",
      ["(a), car sa courbe descend moins vite", "(b), car son t½ est le plus petit", "on ne peut pas savoir"], 1, {
        1: ("juste", "برافو! t un demi صغيرة، réaction أسرع، température أعلى.", "Juste : t½ plus petit, réaction plus rapide, température plus élevée."),
        0: (("لا، كتهبط بشوية يعني بطيئة. و la température العالية كتزرب. عاود اختار.", "Descendre moins vite, c'est être plus lente. Réessaie."),
            ("الجواب: la courbe b، t un demi ديالها أصغر.", "Réponse : (b), son t½ est le plus petit.")),
        2: (("بلى نقدرو: la température facteur cinétique، و t un demi كتقول شكون الأسرع. عاود اختار.", "La température est un facteur cinétique et t½ compare les vitesses. Réessaie."),
            ("الجواب: la courbe b، t un demi deux minutes.", "Réponse : (b)."))},
      "t un demi de a égale six minutes et t un demi de b égale deux minutes. Quelle courbe correspond à la température la plus élevée ?"),
  qcm("fa_5", "Plus facile : le diiode formé", "سؤال ساهل على le tableau.",
      "[H₂O₂]₀ = 40 mmol/L et, à une date t, [H₂O₂] = 10 mmol/L. Alors [I₂] vaut…",
      ["10 mmol/L", "30 mmol/L", "50 mmol/L"], 1, {
        1: ("juste", "برافو! اللي مشا من l'eau oxygénée، trente، ولا diiode.", "Juste : [I₂] = 40 − 10 = 30 mmol/L."),
        0: (("لا، dix هي اللي باقية من l'eau oxygénée، ماشي اللي تكون. عاود اختار.", "10 mmol/L, c'est ce qui reste d'eau oxygénée. Réessaie."),
            ("الجواب: trente millimoles par litre: quarante moins dix.", "Réponse : 40 − 10 = 30 mmol/L.")),
        2: (("لا، ما كنجمعوش. le diiode هو اللي تستهلك من l'eau oxygénée. عاود اختار.", "On ne fait pas la somme. Réessaie."),
            ("الجواب: trente millimoles par litre.", "Réponse : 30 mmol/L."))},
      "La concentration initiale d'eau oxygénée est quarante millimoles par litre, et à une date t, dix millimoles par litre. Alors la concentration de diiode vaut ?"),
  vf("fa_6", "Plus facile : vrai ou faux", "Mêmes quantités initiales, 25 °C et 40 °C.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("À 40 °C, la réaction est plus rapide.", True, "La température est un facteur cinétique."),
      ("À 40 °C, x_f est plus grand.", False, "x_f dépend des quantités initiales : il est le même."),
      ("Les deux courbes [H₂O₂](t) tendent vers 0.", True, "H₂O₂ est limitant et la réaction est totale dans les deux cas.")]),
]

SIM_Q = [
  QS("1", "Montrer que v = −d[H₂O₂]/dt.",
     phrase("x = n₀ − [H₂O₂]·V ; v = (1/V)·dx/dt = −d[H₂O₂]/dt."),
     (["n(H₂O₂) = n₀ − x", "v = (1/V)·dx/dt"], ["v = d[H₂O₂]/dt"]),
     [("x = n₀ − [H₂O₂]·V", "x égale n zéro moins"), ("v = −d[H₂O₂]/dt", "v égale moins d")],
     "x égale n zéro moins la concentration fois V. كنشتقو و نقسمو على V: v égale moins d de la concentration sur d t."),
  QS("2", "Calculer v(0) pour la courbe (a).",
     val("v(0)", sV0, "mmol·L⁻¹·min⁻¹", "v(0) = −(4,0 − 30)/(10 − 0) = 2,6 mmol·L⁻¹·min⁻¹", tol=0.04),
     (["v = −d[H₂O₂]/dt", "A", "B"], ["v = −2,6 mmol·L⁻¹·min⁻¹"]),
     [("pente = (4,0 − 30)/10 = −2,6 mmol·L⁻¹·min⁻¹", "la pente égale moins deux virgule six"), ("v(0) = 2,6 mmol·L⁻¹·min⁻¹", "v de zéro égale deux virgule six")],
     "la pente égale moins deux virgule six. v égale moins la pente: v de zéro égale deux virgule six millimoles par litre et par minute."),
  QS("3", "Montrer qu'à t½, [H₂O₂] = [H₂O₂]₀/2, puis déterminer t½ pour la courbe (a).",
     val("t½(a)", sTA, "min", "[H₂O₂](t½) = 15 mmol/L ; t½(a) = 8 min", tol=0.06),
     (["x(t½) = x_f/2", "[H₂O₂]₀/2"], ["[H₂O₂](t½) = 0"]),
     [("x_f = n₀ ; à t½ il reste n₀/2 : [H₂O₂] = 30/2 = 15 mmol/L", "quinze millimoles par litre"), ("t½(a) = 8 min (t½(b) = 3 min)", "t un demi égale huit minutes")],
     "à t un demi باقي النص: quinze millimoles par litre. على la courbe a: t un demi égale huit minutes. و على b: trois minutes."),
  QS("4", "L'une des expériences est à 20 °C, l'autre à 35 °C. Attribuer chaque courbe. Justifier.",
     phrase("t½(b) = 3 min < t½(a) = 8 min : (b) est la plus rapide, donc à 35 °C ; (a) à 20 °C (la température est un facteur cinétique)."),
     (["t½(b) < t½(a)", "facteur cinétique"], ["(a) à 35 °C"]),
     [("t½(b) < t½(a) : (b) plus rapide", "b أسرع"), ("(b) : 35 °C ; (a) : 20 °C", "la courbe b ديال trente-cinq degrés Celsius")],
     "t un demi ديال b صغيرة: b أسرع. la température facteur cinétique، إذن la courbe b ديال trente-cinq degrés Celsius، و a ديال vingt degrés Celsius."),
  QS("5", "Pour l'expérience la plus chaude, déterminer [I₂] à t = 6 min.",
     val("[I₂]", sCI2, "mmol/L", "[I₂] = 30 − 7,5 = 22,5 mmol/L", tol=0.05),
     (["[I₂] = [H₂O₂]₀ − [H₂O₂]", "courbe (b)"], ["[I₂] = [H₂O₂]"]),
     [("sur (b) à 6 min : [H₂O₂] = 7,5 mmol/L", "sept virgule cinq"), ("[I₂] = 30 − 7,5 = 22,5 mmol/L", "vingt-deux virgule cinq")],
     "على la courbe b à six minutes: sept virgule cinq millimoles par litre. la concentration de diiode égale trente moins sept virgule cinq، vingt-deux virgule cinq millimoles par litre."),
  QS("6", "Un élève affirme : « à la température la plus élevée, on obtient plus de diiode ». Discuter.",
     phrase("Faux : même état final ([I₂]_f = 30 mmol/L dans les deux cas) ; la température change seulement la vitesse."),
     (["état final", "faux"], ["vrai"]),
     [("faux : même état final, [I₂]_f = 30 mmol/L", "نفس l'état final"), ("la température change seulement la vitesse", "la température كتبدل غير la vitesse")],
     "l'affirmation fausse: نفس l'état final، trente millimoles par litre ديال le diiode فبجوج. la température كتبدل غير la vitesse."),
]

EX = exercice(
  "phys_ex_ch10_cinetique_6", "phys_ch10_cinetique", "cinetique",
  "L'eau oxygénée à deux températures : vitesse à partir d'un réactif", "difficile", 40,
  ["Établir v = −d[réactif]/dt", "Calculer une vitesse sur une courbe décroissante", "Lire t½ sur la courbe d'un réactif",
   "Attribuer des courbes à des températures", "Exploiter le tableau d'avancement", "Discuter une affirmation"],
  "On réalise deux fois la même réaction, à deux températures différentes (25 °C et 40 °C), avec les mêmes quantités initiales : dans un volume V = 100 mL constant, [H₂O₂]₀ = 40 mmol/L d'eau oxygénée, avec des ions iodure et des ions H₃O⁺ en excès. Équation : H₂O₂(aq) + 2 I⁻(aq) + 2 H₃O⁺(aq) → I₂(aq) + 4 H₂O(ℓ) ; la réaction est lente et totale. La figure donne la concentration [H₂O₂] en fonction du temps pour les deux expériences, courbes (a) et (b), et la tangente (T) à la courbe (a) en t = 0.",
  "دابا نقراو l'énoncé. كنديرو نفس la réaction deux fois، ب deux températures: vingt-cinq degrés Celsius و quarante degrés Celsius، بنفس les quantités initiales. le volume ثابت، cent millilitres. la concentration initiale d'eau oxygénée، quarante millimoles par litre، و les ions iodure و les ions H trois O plus en excès. la réaction بطيئة و totale، و كتعطي le diiode. la figure كتعطي la concentration d'eau oxygénée en fonction du temps، ل deux expériences، la courbe a و la courbe b، مع la tangente T ل la courbe a à t égale zéro.",
  [FIG],
  ["V = 100 mL (constant) ; [H₂O₂]₀ = 40 mmol/L", "I⁻ et H₃O⁺ en excès ; réaction totale", "Tangente (T) à (a) en t = 0 : A(0 ; 40 mmol/L) et B(8 min ; 3,0 mmol/L)"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Même réaction, faite à 20 °C et à 35 °C, avec V = 100 mL et [H₂O₂]₀ = 30 mmol/L (I⁻ et H₃O⁺ en excès). La figure donne [H₂O₂] en fonction du temps, courbes (a) et (b), et la tangente (T) à (a) en t = 0.",
  "نفس التمرين، بقيم أخرى: vingt degrés Celsius و trente-cinq degrés Celsius، و la concentration initiale trente millimoles par litre.",
  [sFIG],
  ["V = 100 mL ; [H₂O₂]₀ = 30 mmol/L", "(T) : A(0 ; 30 mmol/L) et B(10 min ; 4,0 mmol/L)"],
  SIM_Q)

ecrire(EX)
