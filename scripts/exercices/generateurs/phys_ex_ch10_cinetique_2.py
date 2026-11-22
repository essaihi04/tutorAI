# Exercice de chimie, ch. 10 (suivi temporel, vitesse de réaction), niveau facile : la vitesse volumique par la
# tangente, à deux dates, puis comment elle évolue et l'effet d'un facteur cinétique.
# Sources comparées (lues, jamais copiées) :
#  - nationaux, exercice 1 de chimie : 2016 R (2.3.3 v à t = 0), 2019 R (II.4 v à t = 100 s par la tangente (T)),
#    2021 N (2.4 v₁ à t₁ = 4 min), 2024 N (1.a/1.c facteurs cinétiques vrai/faux, 3 v à t₁ en mmol·L⁻¹·h⁻¹),
#    2025 N (2.2 courbe de l'expérience la plus rapide) — backend/data/exams/physique ;
#  - profs : architecture/sources_chimie_ch9_ch11.md, chapitre B (Mahajar-Tabit, El Founani, Sbiro, Hadjyne,
#    Boulouiha : v = (1/V)·dx/dt par la tangente partout, « la vitesse diminue au cours du temps ») et
#    architecture/phys_ch10_cinetique.md (piège : V en litres, pas en mL ; la tangente ≠ la corde) ;
#  - séries en ligne (titres et résumés lus par recherche ; le réseau du conteneur ne laisse pas ouvrir les PDF) :
#    talamidi (suivi temporel, série 1 corrigée, série 2, activités 3), moutamadris (exercices suivi temporel 2022,
#    fiches 13-7 et 13-8), alloschool (élément 119798), coursdusoirpc (TD B. Mouslim : vitesse de formation de I₂ à
#    t₀ = 0 et t₁ = 40 min), dreamjob (exercices corrigés suivi temporel).
# Ici : réaction des ions thiosulfate en milieu acide, nos propres valeurs ; courbe calculée (modèle d'ordre un,
# k = 0,20 min⁻¹), tangentes calculées et deux points de chacune écrits sur la figure.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _chimie import *

# ------------------------------------------------------------------ données
V = 0.200                     # L
XF, K = 4.0, 0.20             # mmol, min⁻¹
T12 = math.log(2) / K
x, EXPR = x_ordre1(XF, T12)
p0 = pente_ordre1(XF, T12, 0)                  # 0,80 mmol/min
assert abs(p0 - 0.80) < 1e-9
# tangente en 0 : A(0 ; 0), B(5 min ; 4,0 mmol)
assert abs(p0 * 5 - 4.0) < 1e-9
V0 = (4.0 - 0) / (5 - 0) / V                   # 4,0 mmol·L⁻¹·min⁻¹
assert abs(V0 - 4.0) < 1e-9
# tangente en 10 min : C(0 ; 2,38), D(20 min ; 4,54)
p10 = pente_ordre1(XF, T12, 10)
yC, yD = x(10) - 10 * p10, x(10) + 10 * p10
assert round(yC, 2) == 2.38 and round(yD, 2) == 4.54
V10 = (4.54 - 2.38) / 20 / V                   # 0,54 mmol·L⁻¹·min⁻¹
assert abs(V10 - 0.54) < 1e-9 and abs(p10 / V - V10) / V10 < 0.01

FIG = courbe_fig("Avancement x en fonction du temps, avec deux tangentes",
    ((0, 30, "t", "min", [0, 5, 10, 15, 20, 25, 30]), (0, 5, "x", "mmol", [0, 1, 2, 3, 4, 5])),
    [{"f": "courbe", "expr": EXPR, "de": 0, "a": 30, "couleur": "cyan", "texte": "x(t)", "texte_x": 26, "pos": "s"},
     tangente(XF, T12, 0, 0, 5.6) | {"couleur": "vert"},
     tangente(XF, T12, 10, 0, 20) | {"couleur": "orange"},
     {"f": "point", "at": [0, 0], "t": "A", "pos": "se", "couleur": "vert"},
     {"f": "point", "at": [5, 4.0], "t": "B (5 ; 4,0)", "pos": "o", "couleur": "vert"},
     {"f": "point", "at": [0, round(yC, 2)], "t": "C (0 ; 2,38)", "pos": "e", "couleur": "orange"},
     {"f": "point", "at": [20, round(yD, 2)], "t": "D (20 ; 4,54)", "pos": "n", "couleur": "orange"},
     {"f": "point", "at": [10, round(x(10), 3)], "couleur": "orange"},
     {"f": "texte", "at": [8, 0.5], "t": "(T₀) : tangente en t = 0 ; (T₁₀) : tangente en t = 10 min", "couleur": "faible", "taille": "petit"}],
    legende="Les tangentes (T₀) en A et (T₁₀) au point d'abscisse 10 min ; coordonnées des points en (min ; mmol).")

# ------------------------------------------------------------------ similaire
sV, sXF, sK = 0.250, 5.0, 0.25
sT12 = math.log(2) / sK
sx, sEXPR = x_ordre1(sXF, sT12)
assert abs(pente_ordre1(sXF, sT12, 0) * 4 - 5.0) < 1e-9          # B(4 ; 5,0)
sV0 = 5.0 / 4 / sV                                                # 5,0
sp8 = pente_ordre1(sXF, sT12, 8)
syC, syD = sx(8) - 8 * sp8, sx(8) + 8 * sp8
assert round(syC, 2) == 2.97 and round(syD, 2) == 5.68
sV8 = (5.68 - 2.97) / 16 / sV                                     # 0,6775
sFIG = courbe_fig("Avancement x en fonction du temps, avec deux tangentes",
    ((0, 24, "t", "min", [0, 4, 8, 12, 16, 20, 24]), (0, 6, "x", "mmol", [0, 1, 2, 3, 4, 5, 6])),
    [{"f": "courbe", "expr": sEXPR, "de": 0, "a": 24, "couleur": "cyan", "texte": "x(t)", "texte_x": 21, "pos": "s"},
     tangente(sXF, sT12, 0, 0, 4.6) | {"couleur": "vert"},
     tangente(sXF, sT12, 8, 0, 16) | {"couleur": "orange"},
     {"f": "point", "at": [0, 0], "t": "A", "pos": "se", "couleur": "vert"},
     {"f": "point", "at": [4, 5.0], "t": "B (4 ; 5,0)", "pos": "o", "couleur": "vert"},
     {"f": "point", "at": [0, 2.97], "t": "C (0 ; 2,97)", "pos": "e", "couleur": "orange"},
     {"f": "point", "at": [16, 5.68], "t": "D (16 ; 5,68)", "pos": "n", "couleur": "orange"}],
    legende="(T₀) tangente en t = 0 ; (T₈) tangente en t = 8 min ; coordonnées en (min ; mmol).")

# ------------------------------------------------------------------ questions
QUESTIONS = [
  Q("1", "Déterminer la vitesse volumique de la réaction v(0) à la date t = 0, en mmol·L⁻¹·min⁻¹.",
    "السؤال un: حدد la vitesse volumique de réaction، v de zéro، à t égale zéro، ب millimole par litre et par minute.",
    val("v(0)", V0, "mmol·L⁻¹·min⁻¹", "v(0) = (1/V)·(dx/dt)₀ = (1/0,200) × (4,0 − 0)/(5 − 0) = 4,0 mmol·L⁻¹·min⁻¹"),
    (["v = (1/V)·dx/dt", "(dx/dt)₀", "Δx/Δt", "V = 0,200 L", "mmol·L⁻¹·min⁻¹"], ["V = 200 L", "v = x/t", "v = V·dx/dt"]),
    [("dx/dt à t = 0 est la pente de la tangente (T₀) au point A : prends deux points de cette droite, A et B.",
      "d x sur d t à t égale zéro، هي la pente ديال la tangente T zéro ف le point A. خود deux points ديال هاد la droite: A و B."),
     ("v(0) = (1/V)·(x_B − x_A)/(t_B − t_A), avec V en litres : 200 mL = 0,200 L.",
      "v de zéro égale un sur V، fois x B moins x A، sur t B moins t A. و V ب litre: deux cents millilitres égale zéro virgule deux cents litre.")],
    [("1 : v(0) = (1/V)·(dx/dt)₀", "v de zéro égale un sur V"),
     ("(dx/dt)₀ = (4,0 − 0)/(5 − 0) = 0,80 mmol/min", "la pente égale zéro virgule quatre-vingts millimole par minute"),
     ("v(0) = (1/0,200) × 0,80 = 4,0 mmol·L⁻¹·min⁻¹", "v de zéro égale quatre virgule zéro millimoles par litre et par minute")],
    "السؤال un. v de zéro égale un sur V، fois d x sur d t à zéro. d x sur d t هي la pente ديال la tangente: quatre virgule zéro moins zéro، sur cinq moins zéro، يعني la pente égale zéro virgule quatre-vingts millimole par minute. V égale zéro virgule deux cents litre. إذن v de zéro égale quatre virgule zéro millimoles par litre et par minute.",
    "ex_1", "fa_1"),
  Q("2", "Déterminer de la même façon la vitesse volumique v(10) à la date t = 10 min.",
    "السؤال deux: حدد بنفس الطريقة la vitesse volumique، v de dix، à t égale dix minutes.",
    val("v(10)", V10, "mmol·L⁻¹·min⁻¹", "v(10) = (1/0,200) × (4,54 − 2,38)/(20 − 0) = 0,54 mmol·L⁻¹·min⁻¹", tol=0.05),
    (["v = (1/V)·dx/dt", "(T₁₀)", "C", "D", "Δx/Δt"], ["v = x(10)/10", "v = (1/V)·x/t"]),
    [("La tangente à t = 10 min est la droite (T₁₀) : ses points C et D sont écrits sur la figure. Ne prends pas le point de la courbe divisé par 10.",
      "la tangente à t égale dix minutes هي la droite T dix. les points C و D مكتوبين فla figure. ما تقسمش x de dix على dix: هادي ماشي la pente."),
     ("Pente = (x_D − x_C)/(t_D − t_C), puis v(10) = pente/V.",
      "la pente égale x D moins x C، sur t D moins t C. ومن بعد v de dix égale la pente sur V.")],
    [("2 : v(10) = (1/V)·(dx/dt)₁₀", "v de dix égale un sur V"),
     ("(dx/dt)₁₀ = (4,54 − 2,38)/(20 − 0) = 0,108 mmol/min", "la pente égale zéro virgule cent huit millimole par minute"),
     ("v(10) = 0,108/0,200 ≈ 0,54 mmol·L⁻¹·min⁻¹", "v de dix égale environ zéro virgule cinquante-quatre")],
    "السؤال deux. v de dix égale un sur V، fois la pente ديال la tangente T dix. la pente: quatre virgule cinquante-quatre moins deux virgule trente-huit، sur vingt moins zéro، يعني la pente égale zéro virgule cent huit millimole par minute. على zéro virgule deux cents litre: v de dix égale environ zéro virgule cinquante-quatre millimole par litre et par minute.",
    "ex_2", "fa_2"),
  Q("3", "Comparer v(0) et v(10). Quel facteur cinétique explique cette évolution ?",
    "السؤال trois: قارن v de zéro و v de dix. شنو le facteur cinétique اللي كيفسر هاد التطور؟",
    phrase("v(10) < v(0) : la vitesse volumique diminue au cours du temps, car la concentration des réactifs diminue (facteur cinétique : la concentration des réactifs)."),
    (["v(10) < v(0)", "concentration des réactifs", "diminue", "facteur cinétique"], ["la température diminue", "x diminue"]),
    [("Compare les deux nombres trouvés. Puis demande-toi ce qui change dans le bécher pendant la réaction.",
      "قارن deux résultats اللي لقيتي. ومن بعد سول راسك: شنو اللي كيتبدل فle bécher ملي la réaction خدامة؟"),
     ("Les réactifs se consomment : leur concentration diminue, et la concentration est un facteur cinétique.",
      "les réactifs كيتستهلكو: la concentration ديالهم كتنقص. و la concentration هي facteur cinétique.")],
    [("3 : v(10) = 0,54 < v(0) = 4,0 mmol·L⁻¹·min⁻¹ : la vitesse diminue au cours du temps", "la vitesse diminue au cours du temps"),
     ("car la concentration des réactifs (facteur cinétique) diminue", "car la concentration des réactifs diminue")],
    "السؤال trois. v de dix صغيرة بزاف من v de zéro: la vitesse diminue au cours du temps. علاش؟ les réactifs كيتستهلكو، car la concentration des réactifs diminue. و la concentration هي facteur cinétique.",
    "ex_3", "fa_3"),
  Q("4", "On refait la même expérience à une température plus élevée. Comment varient la vitesse v(0) et l'avancement final x_f ? Justifier.",
    "السؤال quatre: كنعاودو نفس l'expérience ب température أكبر. كيفاش كتبدل v de zéro و x f؟ علل.",
    phrase("v(0) augmente (la température est un facteur cinétique : plus de chocs efficaces par unité de temps) ; x_f ne change pas (mêmes quantités initiales, même réactif limitant)."),
    (["v(0) augmente", "x_f inchangé", "chocs efficaces", "facteur cinétique"], ["x_f augmente", "v(0) diminue"]),
    [("La température change-t-elle la vitesse, ou la quantité de réactif limitant ?",
      "la température واش كتبدل la vitesse، ولا كتبدل la quantité ديال le réactif limitant؟"),
     ("Plus chaud : les entités bougent plus, plus de chocs efficaces par unité de temps. Mais le palier dépend seulement des quantités initiales.",
      "ملي كتسخن، les entités كيتحركو كثر، و كاينين plus de chocs efficaces par unité de temps. ولكن le palier كيتعلق غير ب les quantités initiales.")],
    [("4 : la température est un facteur cinétique : v(0) augmente (plus de chocs efficaces par unité de temps)", "v de zéro كتكبر"),
     ("x_f ne change pas : mêmes quantités initiales, x_f = x_max = 4,0 mmol", "x f ما كتتبدلش")],
    "السؤال quatre. la température هي facteur cinétique: v de zéro كتكبر، حيت كاينين plus de chocs efficaces par unité de temps. ولكن x f ما كتتبدلش: نفس les quantités initiales، إذن x f égale x max égale quatre virgule zéro millimoles.",
    "ex_4", "fa_4"),
]

EXPLICATIONS = [
  sim("ex_1", "Question 1 : la pente de la tangente en t = 0",
      "dx/dt à t = 0 est la pente de la tangente : Δx/Δt entre deux points éloignés de la tangente.",
      "cinetique-tableau/vitesse.html?vue=tangente", "La tangente à la courbe x(t) en t = 0",
      "شوف la courbe x en fonction du temps. كنختارو la date t égale zéro، هادا هو le point. دابا كنرسمو la tangente: droite كتقيس la courbe فهاد le point. كناخدو deux points ديال la tangente، بعاد على بعضياتهم. فهاد المثال: zéro و zéro، و huit minutes و deux virgule zéro millimoles، إذن la pente égale zéro virgule vingt-cinq millimole par minute. فالتمرين ديالنا: A و B، يعني la pente égale quatre virgule zéro sur cinq، zéro virgule quatre-vingts millimole par minute. ومن بعد كنقسمو على V égale zéro virgule deux cents litre. إذن v de zéro égale quatre virgule zéro millimoles par litre et par minute.",
      [("(dx/dt)₀ = 4,0/5 = 0,80 mmol/min", "zéro virgule quatre-vingts millimole par minute"),
       ("v(0) = 0,80/0,200 = 4,0 mmol·L⁻¹·min⁻¹", "إذن v de zéro égale quatre virgule zéro")],
      [("شوف la courbe", "moment:courbe"), ("كنختارو la date t égale zéro", {"set": {"t": 0}}),
       ("هادا هو le point", "moment:point"), ("دابا كنرسمو la tangente", "moment:tangente"),
       ("كناخدو deux points", "moment:deux_points"), ("فهاد المثال", "moment:pente")]),
  sim("ex_2", "Question 2 : le calcul en trois lignes",
      "La relation, la pente avec son unité, puis l'application numérique avec V en litres.",
      "cinetique-tableau/vitesse.html?vue=calcul", "Le calcul de la vitesse, comme sur la copie",
      "نكتبو le calcul ب trois lignes. اللولة، la relation: v égale un sur V، fois d x sur d t. الثانية، la pente: فالتمرين ديالنا، la tangente T dix كتدوز من C و D، la pente égale quatre virgule cinquante-quatre moins deux virgule trente-huit، sur vingt، يعني zéro virgule cent huit millimole par minute. الثالثة، l'application numérique: V égale zéro virgule deux cents litre. le résultat: v de dix égale environ zéro virgule cinquante-quatre millimole par litre et par minute. رد البال: V ديما en litres، ماشي en millilitres.",
      [("(dx/dt)₁₀ = (4,54 − 2,38)/20 = 0,108 mmol/min", "يعني zéro virgule cent huit millimole par minute"),
       ("v(10) = 0,108/0,200 ≈ 0,54 mmol·L⁻¹·min⁻¹", "le résultat")],
      [("اللولة، la relation", "moment:relation"), ("الثانية، la pente", "moment:pente"),
       ("الثالثة، l'application numérique", "moment:application"), ("le résultat", "moment:resultat"),
       ("رد البال", "moment:piege")]),
  sim("ex_3", "Question 3 : la vitesse diminue",
      "Les tangentes deviennent de moins en moins raides : les réactifs s'épuisent.",
      "cinetique-tableau/vitesse.html?vue=diminue", "Trois tangentes sur la même courbe",
      "شوف la courbe ديال المثال. غادي نرسمو trois tangentes. اللولة à t égale zéro: طالعة بزاف، deux virgule cinq millimoles par litre et par minute. الثانية à huit minutes: أقل طالعة. الثالثة à vingt minutes: تقريبا plate. إذن la vitesse volumique، diminue au cours du temps. فالتمرين ديالنا نفس الشي: quatre virgule zéro à zéro، و zéro virgule cinquante-quatre à dix minutes. علاش؟ les réactifs كيتستهلكو، car la concentration des réactifs diminue.",
      [("v(10) < v(0) : v diminue au cours du temps", "إذن la vitesse volumique، diminue au cours du temps"),
       ("cause : la concentration des réactifs diminue", "car la concentration des réactifs diminue")],
      [("شوف la courbe", "moment:courbe"), ("اللولة à t égale zéro", "moment:tangente_0"),
       ("الثانية à huit minutes", "moment:tangente_8"), ("الثالثة à vingt minutes", "moment:tangente_20"),
       ("إذن la vitesse volumique", "moment:conclusion")]),
  sim("ex_4", "Question 4 : la température, facteur cinétique",
      "Plus chaud : la tangente à l'origine est plus raide, mais le palier reste le même.",
      "cinetique-tableau/temperature.html?vue=vitesse", "Deux températures, même état final",
      "شوف les axes: x en fonction du temps. هادي la courbe ديال vingt degrés Celsius. وهادي la courbe ديال quarante degrés Celsius، كتطلع دغيا. دابا نرسمو les tangentes à l'origine: à quarante degrés Celsius، la pente trois fois plus grande. علاش؟ كلما زادت la température، les entités كيتحركو كثر: plus de chocs efficaces par unité de temps. ولكن شوف le palier: بجوج كيوقفو ف deux virgule zéro millimoles. فالتمرين ديالنا: v de zéro كتكبر، و x f كتبقى quatre virgule zéro millimoles.",
      [("T plus grande ⇒ v(0) plus grande", "plus de chocs efficaces par unité de temps"),
       ("x_f = x_max = 4,0 mmol : inchangé", "و x f كتبقى quatre virgule zéro millimoles")],
      [("شوف les axes", "moment:axes"), ("هادي la courbe ديال vingt degrés Celsius", "moment:courbe_20"),
       ("وهادي la courbe ديال quarante degrés Celsius", "moment:courbe_40"), ("دابا نرسمو les tangentes", "moment:tangentes"),
       ("علاش؟ كلما زادت", "moment:comparer"), ("ولكن شوف le palier", "moment:meme_final")]),
]

FACILES = [
  qcm("fa_1", "Plus facile : la vitesse à t = 0", "نتمرنو بسؤال ساهل. اختار la bonne valeur.",
      "La tangente en t = 0 passe par A(0 ; 0) et B(5 min ; 4,0 mmol). V = 0,200 L. v(0) vaut…",
      ["0,80 mmol·L⁻¹·min⁻¹", "4,0 mmol·L⁻¹·min⁻¹", "0,16 mmol·L⁻¹·min⁻¹"], 1, {
        1: ("juste", "برافو! la pente zéro virgule quatre-vingts millimole par minute، على zéro virgule deux cents litre، كتعطي quatre virgule zéro.", "Juste : v(0) = 0,80/0,200 = 4,0 mmol·L⁻¹·min⁻¹."),
        0: (("قريب! هادي هي la pente d x sur d t، ولكن نسيتي un sur V. عاود اختار.", "C'est la pente dx/dt ; il manque le facteur 1/V. Réessaie."),
            ("الجواب هو quatre virgule zéro: v égale la pente sur V، يعني zéro virgule quatre-vingts sur zéro virgule deux cents.", "Réponse : v(0) = 0,80/0,200 = 4,0 mmol·L⁻¹·min⁻¹.")),
        2: (("لا، ضربتي la pente ف V. la relation فيها un sur V، يعني قسمة. عاود اختار.", "On divise par V, on ne multiplie pas. Réessaie."),
            ("الجواب هو quatre virgule zéro: v égale un sur V fois d x sur d t.", "Réponse : v = (1/V)·dx/dt = 4,0 mmol·L⁻¹·min⁻¹."))},
      "La tangente en t égale zéro passe par A et B, cinq minutes et quatre virgule zéro millimoles. V égale zéro virgule deux cents litre. v de zéro vaut ?"),
  qcm("fa_2", "Plus facile : la bonne pente", "سؤال ساهل: شمن حساب كيعطي la pente à dix minutes؟",
      "Pour v(10), quelle pente faut-il calculer ?",
      ["x(10)/10, le point de la courbe", "(x_D − x_C)/(t_D − t_C), la tangente (T₁₀)", "(x_B − x_A)/(t_B − t_A), la tangente (T₀)"], 1, {
        1: ("juste", "برافو! la vitesse à dix minutes كتجي من la tangente فهاد la date: les points C و D.", "Juste : la pente de la tangente (T₁₀), entre C et D."),
        0: (("لا، x de dix sur dix هي la pente ديال la corde من الأصل، ماشي la tangente. عاود اختار.", "x(10)/10 est la pente de la corde depuis l'origine, pas de la tangente. Réessaie."),
            ("الجواب: la pente ديال la tangente T dix، بين C و D.", "Réponse : (x_D − x_C)/(t_D − t_C), sur la tangente (T₁₀).")),
        2: (("لا، T zéro هي la tangente ديال t égale zéro. خاصنا la tangente ديال dix minutes. عاود اختار.", "(T₀) sert pour t = 0, pas pour t = 10 min. Réessaie."),
            ("الجواب: la tangente T dix، بين C و D.", "Réponse : la tangente au point d'abscisse 10 min, entre C et D."))},
      "Pour v de dix, quelle pente faut-il calculer ?"),
  vf("fa_3", "Plus facile : vrai ou faux", "v(0) = 4,0 et v(10) = 0,54 mmol·L⁻¹·min⁻¹.",
     "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
     [("La vitesse volumique diminue au cours du temps.", True, "v(10) est bien plus petite que v(0)."),
      ("La vitesse diminue parce que l'avancement x diminue.", False, "x augmente toujours ; c'est la pente de la courbe qui diminue."),
      ("La vitesse diminue parce que la concentration des réactifs diminue.", True, "Les réactifs se consomment : moins de chocs efficaces par unité de temps.")]),
  assoc("fa_4", "Plus facile : associer", "Même expérience, à une température plus élevée.",
        "سؤال ساهل: ربط كل grandeur مع شنو كيوقع ليها ملي كتطلع la température.",
        "Relie chaque grandeur à ce qu'elle devient quand on chauffe le mélange.",
        [("1", "La vitesse v(0)"), ("2", "L'avancement final x_f"), ("3", "Le temps de demi-réaction t½")],
        [("a", "augmente"), ("b", "ne change pas"), ("c", "diminue")],
        {"1": "a", "2": "b", "3": "c"},
        {"1-a": (True, "Oui : plus de chocs efficaces par unité de temps, la réaction démarre plus vite.", "برافو: plus de chocs efficaces، la vitesse كتكبر."),
         "1-*": (False, "La température est un facteur cinétique : elle accélère la réaction.", "لا، la température facteur cinétique: كتزرب la réaction."),
         "2-b": (True, "Oui : x_f dépend des quantités initiales, pas de la température.", "برافو: x f كيتعلق غير ب les quantités initiales."),
         "2-*": (False, "Les quantités initiales n'ont pas changé : le palier reste à x_max.", "لا، نفس les quantités initiales، إذن نفس le palier."),
         "3-c": (True, "Oui : la réaction plus rapide atteint x_f/2 plus tôt.", "برافو: la réaction أسرع، كتوصل ل x f sur deux بكري."),
         "3-*": (False, "Une réaction plus rapide atteint plus tôt la moitié de x_f.", "لا، ملي la réaction أسرع، كتوصل ل la moitié بكري.")},
        ("Plus chaud : v(0) augmente, x_f ne change pas, t½ diminue.", "ملي كتسخن: v de zéro كتكبر، x f ما كتتبدلش، و t un demi كتصغار.")),
]

SIM_Q = [
  QS("1", "Déterminer v(0) en mmol·L⁻¹·min⁻¹ (V = 250 mL).",
     val("v(0)", sV0, "mmol·L⁻¹·min⁻¹", "v(0) = (1/0,250) × (5,0 − 0)/(4 − 0) = 5,0 mmol·L⁻¹·min⁻¹"),
     (["v = (1/V)·dx/dt", "Δx/Δt", "V = 0,250 L"], ["V = 250 L"]),
     [("v(0) = (1/V)·(dx/dt)₀ ; (dx/dt)₀ = 5,0/4 = 1,25 mmol/min", "la pente égale un virgule vingt-cinq"),
      ("v(0) = 1,25/0,250 = 5,0 mmol·L⁻¹·min⁻¹", "v de zéro égale cinq virgule zéro")],
     "v de zéro égale un sur V fois la pente. la pente égale un virgule vingt-cinq millimole par minute. على zéro virgule deux cent cinquante litre: v de zéro égale cinq virgule zéro millimoles par litre et par minute."),
  QS("2", "Déterminer v(8) à la date t = 8 min.",
     val("v(8)", sV8, "mmol·L⁻¹·min⁻¹", "v(8) = (1/0,250) × (5,68 − 2,97)/(16 − 0) ≈ 0,68 mmol·L⁻¹·min⁻¹", tol=0.05),
     (["v = (1/V)·dx/dt", "C", "D"], ["v = x(8)/8"]),
     [("(dx/dt)₈ = (5,68 − 2,97)/16 ≈ 0,169 mmol/min", "la pente égale environ zéro virgule cent soixante-neuf"),
      ("v(8) ≈ 0,68 mmol·L⁻¹·min⁻¹", "v de huit égale environ zéro virgule soixante-huit")],
     "la pente ديال la tangente: cinq virgule soixante-huit moins deux virgule quatre-vingt-dix-sept، sur seize، la pente égale environ zéro virgule cent soixante-neuf millimole par minute. على zéro virgule deux cent cinquante: v de huit égale environ zéro virgule soixante-huit millimole par litre et par minute."),
  QS("3", "Comparer v(0) et v(8). Quel facteur cinétique explique cette évolution ?",
     phrase("v(8) < v(0) : la vitesse diminue au cours du temps car la concentration des réactifs diminue."),
     (["v diminue", "concentration des réactifs"], ["x diminue"]),
     [("v(8) < v(0) : la vitesse diminue au cours du temps", "la vitesse diminue au cours du temps"),
      ("car la concentration des réactifs diminue", "car la concentration des réactifs diminue")],
     "v de huit صغيرة من v de zéro: la vitesse diminue au cours du temps، car la concentration des réactifs diminue."),
  QS("4", "On refait l'expérience à une température plus basse. Comment varient v(0) et x_f ?",
     phrase("v(0) diminue (moins de chocs efficaces par unité de temps) ; x_f ne change pas (mêmes quantités initiales)."),
     (["v(0) diminue", "x_f inchangé"], ["x_f diminue"]),
     [("v(0) diminue : la température est un facteur cinétique", "v de zéro كتنقص"),
      ("x_f = 5,0 mmol ne change pas", "x f ما كتتبدلش")],
     "ملي كتبرد، v de zéro كتنقص: moins de chocs efficaces par unité de temps. ولكن x f ما كتتبدلش، كتبقى cinq virgule zéro millimoles."),
]

EX = exercice(
  "phys_ex_ch10_cinetique_2", "phys_ch10_cinetique", "cinetique",
  "Les ions thiosulfate en milieu acide : la vitesse par la tangente", "facile", 15,
  ["Déterminer une vitesse volumique par la tangente", "Comparer deux vitesses et expliquer leur évolution", "Prévoir l'effet de la température"],
  "À la date t = 0, on mélange une solution de thiosulfate de sodium et une solution d'acide chlorhydrique en excès ; le volume du mélange est V = 200 mL. La réaction, lente et totale, a pour équation : S₂O₃²⁻(aq) + 2 H₃O⁺(aq) → S(s) + SO₂(aq) + 3 H₂O(ℓ). La figure donne l'avancement x en fonction du temps, avec la tangente (T₀) en t = 0 et la tangente (T₁₀) au point d'abscisse t = 10 min.",
  "دابا نقراو l'énoncé. فt égale zéro، كنخلطو le thiosulfate de sodium مع l'acide chlorhydrique en excès. le volume ديال le mélange، V égale deux cents millilitres. la réaction بطيئة و totale: les ions thiosulfate، plus deux ions H trois O plus، كيعطيو le soufre، le dioxyde de soufre، و الما. la figure كتعطي x en fonction du temps، مع la tangente T zéro à t égale zéro، و la tangente T dix à t égale dix minutes.",
  [FIG],
  ["V = 200 mL (volume du mélange, constant)", "Tangente (T₀) : A(0 ; 0) et B(5 min ; 4,0 mmol)", "Tangente (T₁₀) : C(0 ; 2,38 mmol) et D(20 min ; 4,54 mmol)",
   "Équation : S₂O₃²⁻ + 2 H₃O⁺ → S + SO₂ + 3 H₂O"],
  QUESTIONS, EXPLICATIONS, FACILES,
  "Même exercice, autres données",
  "Même réaction des ions thiosulfate avec l'acide chlorhydrique en excès, mais le volume du mélange est V = 250 mL. La figure donne x en fonction du temps, la tangente (T₀) en t = 0 et la tangente (T₈) au point d'abscisse t = 8 min.",
  "نفس التمرين، بقيم أخرى. نفس la réaction، ولكن le volume ديال le mélange، V égale deux cent cinquante millilitres. la figure فيها la tangente T zéro، و la tangente T huit à huit minutes.",
  [sFIG],
  ["V = 250 mL", "(T₀) : A(0 ; 0) et B(4 min ; 5,0 mmol)", "(T₈) : C(0 ; 2,97 mmol) et D(16 min ; 5,68 mmol)"],
  SIM_Q)

ecrire(EX)
