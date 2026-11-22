# Exercice moyen de physique (ch. 4, décroissance radioactive) : dater une statuette en bois au carbone 14.
# Sources comparées (skill exercices § 2) :
#  - exploration radioactivite.json : cas_types « equation » (Soddy + tableau), « lambda_t_demi », « datation »
#    (t = (1/λ)·ln(a₀/a), λ = ln2/t½) ; pièges « garde le signe moins, temps négatif », « a₀ d'un échantillon de masse
#    différente », « N tend vers zéro sans l'atteindre » ; erreurs_examen « datation » et « montrer que… sans étapes ».
#  - nationaux comparés : 2022 R ex. 2 (carbone 14 : composition et équation en QCM, énergie de liaison, âge d'un bois
#    avec a = 318 Bq et a₀ = 418 Bq, ce qu'animent datation.html et national.html), 2020 R ex. 3 (roche U/Th).
#    Le nôtre : activités 1,75 Bq / 2,50 Bq (rapport 0,70), équation à écrire avec Soddy, « justifier » le choix de a₀,
#    « montrer que » t = (1/λ)·ln(a₀/a), puis limite de la méthode (a' très faible, ≈ 5,6 t½) : chaîne et données à nous.
#  - séries en ligne (recherche du 22/11/2026 ; talamidi.com et kezakoo.com non joignables depuis cette session, seuls
#    les extraits du moteur lus) : talamidi « décroissance radioactive 4-7 », univ-msila (λ du carbone 14), série
#    N. Naceiri Mrabti (datation), labolycée / eduscol « datation » (limite de la méthode à quelques demi-vies).
import sys, os, math, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

_ici = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("tp", os.path.join(_ici, "..", "..", "..", "backend", "kaggle_tts", "texte_parle.py"))
_tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_tp)
nfr = _tp.nombre_fr


def dn(x, d=2):
    s = fr(x, d).replace("−", "")
    if "," not in s:
        return nfr(int(s))
    e, dec = s.split(",")
    reste = dec.lstrip("0")
    return nfr(int(e)) + " virgule" + " zéro" * (len(dec) - len(reste)) + (" " + nfr(int(reste)) if reste else "")


def ds(x, ch=3):
    e = math.floor(math.log10(abs(x)))
    m = round(x / 10 ** e, ch - 1)
    if abs(m) >= 10:
        m /= 10; e += 1
    t = dn(m, ch - 1)
    return t if e == 0 else f"{t} fois dix puissance {'moins ' if e < 0 else ''}{nfr(abs(e))}"


SIMDAT = "/media/simulations/physics/radioactivite-tableau/datation.html"
SIMDES = "/media/simulations/physics/radioactivite-tableau/desintegration.html"
SIML = "/media/simulations/physics/radioactivite-tableau/lambda.html"
SIMF = "/media/simulations/physics/radioactivite-tableau/figures.html"
SIMC = "/media/simulations/physics/radioactivite-tableau/courbe.html"
LN2 = 0.693          # la valeur écrite dans les données (et dans datation.html)
TD = 5730            # t½ du carbone 14, en ans


def calc(a0, a, a2):
    lam = LN2 / TD
    t = (1 / lam) * math.log(a0 / a)
    t2 = (1 / lam) * math.log(a0 / a2)
    return lam, t, t2, t2 / TD


a0, a, a2 = 2.50, 1.75, 0.050
lam, t, t2, n2 = calc(a0, a, a2)
a0b, ab, a2b = 3.00, 1.65, 0.075
_, tb, t2b, n2b = calc(a0b, ab, a2b)
# La simulation datation.html (a₀ = 418 Bq) réglée sur le MÊME rapport a/a₀ que l'exercice :
A0_SIM = 418
a_sim = round(a / a0 * A0_SIM)                     # 293 Bq
t_sim = TD / LN2 * math.log(A0_SIM / a_sim)        # ce que la simulation écrit (2,94·10³ ans)

lamS = sci(lam, 3)                                 # 1,21 × 10⁻⁴


def schema(nom, a_anc, a_rec, recent="bois récent", quoi="bois"):
    return {"type": "schema", "titre": f"Mesures au compteur, pour une même masse m de {quoi}",
            "cadre": {"l": 4.0, "h": 1.6},
            "legende": "Les deux échantillons ont la même masse ; le compteur donne leur activité.",
            "elements": [
                {"f": "rect", "de": [0.2, 0.35], "a": [1.7, 1.05], "couleur": "orange", "arrondi": True},
                {"f": "texte", "at": [0.95, 0.85], "t": nom, "couleur": "orange", "ancre": "centre"},
                {"f": "texte", "at": [0.95, 0.55], "t": f"a = {fr(a_anc, 3)} Bq", "couleur": "jaune", "ancre": "centre"},
                {"f": "rect", "de": [2.3, 0.35], "a": [3.8, 1.05], "couleur": "vert", "arrondi": True},
                {"f": "texte", "at": [3.05, 0.85], "t": recent, "couleur": "vert", "ancre": "centre"},
                {"f": "texte", "at": [3.05, 0.55], "t": f"a₀ = {fr(a_rec, 3)} Bq", "couleur": "jaune", "ancre": "centre"},
                {"f": "texte", "at": [2.0, 1.35], "t": "même masse m", "couleur": "blanc", "ancre": "centre"}]}


EQ_ATT = "¹⁴₆C → ᴬ_Z X + ⁰₋₁e ; lois de Soddy : conservation de A : 14 = A + 0 donc A = 14 ; conservation de Z : 6 = Z − 1 donc Z = 7 ; le tableau donne l'azote N : ¹⁴₆C → ¹⁴₇N + ⁰₋₁e"
Q = []
Q.append({"id": "1", "texte": "Le carbone 14 est radioactif β⁻. Écrire l'équation de sa désintégration en précisant les lois utilisées, et identifier le noyau fils.",
  "texte_dit": "السؤال un: le carbone quatorze radioactif bêta moins. كتب l'équation ديال la désintégration ديالو، وقول les lois اللي استعملتي، وعرف le noyau fils.",
  "reponse": phrase(EQ_ATT),
  "clavier": {"aides": ["¹⁴₆C → ᴬ_Z X + ⁰₋₁e", "conservation de A", "conservation de Z", "⁰₋₁e"], "pieges": ["⁰₁e", "¹⁴₅B", "Z = 5"]},
  "aides": [aide("La particule β⁻ est un électron ⁰₋₁e ; écris l'équation avec un noyau fils ᴬ_Z X inconnu.",
                 "la particule bêta moins هي un électron، A égale zéro و Z égale moins un. كتب l'équation ب noyau fils مجهول، A Z X."),
            aide("Lois de Soddy : A se conserve, puis Z se conserve ; cherche Z dans le tableau.",
                 "les lois de Soddy: A كيتحافظ، ومن بعد Z كيتحافظ. من بعد قلب على Z فالجدول.")],
  "correction": correction([("1 : ¹⁴₆C → ᴬ_Z X + ⁰₋₁e", "le carbone quatorze كيعطي A Z X"),
                            ("d'après les lois de Soddy : 14 = A + 0 ⇒ A = 14 ; 6 = Z − 1 ⇒ Z = 7", "d'après les lois de Soddy"),
                            ("Z = 7 : c'est l'azote ; ¹⁴₆C → ¹⁴₇N + ⁰₋₁e", "Z égale sept: c'est l'azote")],
       "السؤال un. le carbone quatorze كيعطي A Z X، plus un électron. d'après les lois de Soddy: la conservation de A، quatorze égale A plus zéro، إذن A égale quatorze. la conservation de Z، six égale Z moins un، إذن Z égale sept. فالجدول، Z égale sept: c'est l'azote. l'équation: le carbone quatorze كيعطي l'azote quatorze، plus un électron."),
  "explication": "ex_q1", "facile": "fa_q1"})
Q.append({"id": "2", "texte": "Calculer, en an⁻¹, la constante radioactive λ du carbone 14.",
  "texte_dit": "السؤال deux: حسب la constante radioactive lambda ديال le carbone quatorze، ب an puissance moins un.",
  "reponse": valeur("λ", lam, "an⁻¹", f"λ = (ln 2)/t½ = 0,693/5730 ≈ {lamS} an⁻¹"),
  "clavier": {"aides": ["λ = (ln 2)/t½", "t½ = 5730 ans", "an⁻¹"], "pieges": ["λ = t½/(ln 2)", "s⁻¹"]},
  "aides": [aide("t½ est donnée en années : λ sortira en an⁻¹.", "t un demi معطية بالعوام، إذن lambda غادي تخرج ب an puissance moins un."),
            aide("λ = (ln 2)/t½.", "lambda égale ln deux sur t un demi.")],
  "correction": correction([("2 : λ = (ln 2)/t½", "lambda égale ln deux sur t un demi"),
                            ("A.N. : λ = 0,693/5730", "zéro virgule six cent quatre-vingt-treize sur cinq mille sept cent trente"),
                            (f"λ ≈ {lamS} an⁻¹", "lambda égale environ " + ds(lam) + " an puissance moins un")],
       "السؤال deux. lambda égale ln deux sur t un demi. l'application numérique: zéro virgule six cent quatre-vingt-treize sur cinq mille sept cent trente. lambda égale environ " + ds(lam) + " an puissance moins un."),
  "explication": "ex_q2", "facile": "fa_q2"})
JUST = ("Tant que l'arbre est vivant, il échange du CO₂ avec l'air : le carbone 14 qui se désintègre est remplacé, la proportion de ¹⁴C reste constante. "
        "Le bois récent a donc l'activité qu'avait le bois ancien au moment où l'arbre a été coupé (t = 0). "
        "Même masse, car a = λ·N : l'activité est proportionnelle au nombre de noyaux, donc à la masse de bois.")
Q.append({"id": "3", "texte": "Justifier le choix de a₀ : l'activité d'un échantillon de bois récent de même masse que l'échantillon ancien.",
  "texte_dit": "السؤال trois: برر علاش a zéro هي l'activité ديال bois récent، عندو نفس la masse ديال l'échantillon القديم.",
  "reponse": phrase(JUST),
  "clavier": {"aides": ["échanges de CO₂", "proportion de ¹⁴C constante", "a = λ·N", "même masse"], "pieges": ["le bois récent ne contient pas de ¹⁴C"]},
  "aides": [aide("Que se passe-t-il pour le carbone 14 d'un arbre tant qu'il est vivant ? et après sa coupe ?",
                 "شنو كيوقع ل le carbone quatorze ديال الشجرة ملي هي حية؟ ومن بعد ما تقطع؟"),
            aide("Vivant : échanges avec l'air, la proportion de ¹⁴C reste constante ; et a = λ·N dépend du nombre de noyaux, donc de la masse.",
                 "ملي حية، كتبدل le carbone مع الهوا، والنسبة ديال le carbone quatorze كتبقى ثابتة. و a égale lambda N، كتبع العدد ديال les noyaux، يعني la masse.")],
  "correction": correction([("3 : vivant, l'arbre échange du CO₂ avec l'air : la proportion de ¹⁴C reste constante", "ملي الشجرة حية"),
                            ("donc le bois récent a l'activité du bois ancien à sa mort (t = 0) : c'est a₀", "إذن le bois récent"),
                            ("même masse, car a = λ·N : l'activité est proportionnelle au nombre de noyaux, donc à la masse", "a égale lambda N")],
       "السؤال trois. ملي الشجرة حية، كتبدل le carbone مع الهوا: les noyaux اللي كيتفككو كيتعوضو، والنسبة ديال le carbone quatorze كتبقى ثابتة. إذن le bois récent عندو l'activité اللي كانت عند le bois ancien ملي تقطع، فt égale zéro: هي a zéro. ونفس la masse، حيت a égale lambda N: l'activité كتبع العدد ديال les noyaux، يعني la masse."),
  "explication": "ex_q3", "facile": "fa_q3"})
DEMO = "a(t) = a₀·e^(−λt) ⇒ a/a₀ = e^(−λt) ⇒ ln(a/a₀) = −λ·t ⇒ ln(a₀/a) = λ·t ⇒ t = (1/λ)·ln(a₀/a)"
Q.append({"id": "4", "texte": "Montrer que l'âge t de l'objet s'écrit : t = (1/λ)·ln(a₀/a).",
  "texte_dit": "السؤال quatre: بين بلي l'âge t ديال l'objet، كيتكتب: t égale un sur lambda fois ln de a zéro sur a.",
  "reponse": phrase(DEMO),
  "clavier": {"aides": ["a(t) = a₀·e^(−λt)", "ln(eˣ) = x", "ln(1/x) = −ln x"], "pieges": ["t = λ·ln(a₀/a)", "t = (1/λ)·ln(a/a₀)"]},
  "aides": [aide("Pars de la loi de l'activité a(t) = a₀·e^(−λt) et isole l'exponentielle.",
                 "بدا من la loi: a égale a zéro exponentielle moins lambda t. قسم على a zéro باش تبقى exponentielle بوحدها."),
            aide("Prends ln des deux côtés (ln enlève e), puis retourne la fraction pour enlever le signe moins.",
                 "دير ln للجهتين، ln كيحيد e. من بعد قلب la fraction باش يمشي le signe moins.")],
  "correction": correction([("4 : a(t) = a₀·e^(−λt) donc a/a₀ = e^(−λt)", "a sur a zéro égale exponentielle moins lambda t"),
                            ("ln(a/a₀) = −λ·t, soit ln(a₀/a) = λ·t", "ln de a zéro sur a égale lambda t"),
                            ("t = (1/λ)·ln(a₀/a)", "t égale un sur lambda fois ln de a zéro sur a")],
       "السؤال quatre. a égale a zéro exponentielle moins lambda t، إذن a sur a zéro égale exponentielle moins lambda t. كنديرو ln: ln de a sur a zéro égale moins lambda t. كنقلبو la fraction: ln de a zéro sur a égale lambda t. إذن t égale un sur lambda fois ln de a zéro sur a."),
  "explication": "ex_q4", "facile": "fa_q4"})
Q.append({"id": "5", "texte": "Calculer l'âge t de la statuette.",
  "texte_dit": "السؤال cinq: حسب l'âge t ديال la statuette.",
  "reponse": valeur("t", t, "ans", f"t = (1/λ)·ln(a₀/a) = (5730/0,693) × ln({fr(a0, 3)}/{fr(a, 3)}) ≈ {sci(t, 3)} ans"),
  "clavier": {"aides": ["t = (1/λ)·ln(a₀/a)", "1/λ = t½/(ln 2)", "A.N. : (5730/0,693) × ln(2,5/1,75)", "ans"], "pieges": ["ln(a/a₀)", "t = λ·ln(a₀/a)"]},
  "aides": [aide("a₀ = 2,50 Bq et a = 1,75 Bq : le rapport a₀/a est plus grand que 1, son ln est positif.",
                 "a zéro égale deux virgule cinquante becquerels، و a égale un virgule soixante-quinze becquerel. a zéro sur a، plus grand que un، إذن ln ديالو positif."),
            aide("Remplace 1/λ par t½/(ln 2) : t = (t½/ln 2)·ln(a₀/a), avec t½ en années.",
                 "عوض l'expression un sur lambda ب t un demi sur ln deux. t égale t un demi sur ln deux، fois ln de a zéro sur a، و t un demi بالعوام.")],
  "correction": correction([("5 : t = (1/λ)·ln(a₀/a) = (t½/ln 2)·ln(a₀/a)", "t égale t un demi sur ln deux"),
                            (f"A.N. : t = (5730/0,693) × ln({fr(a0, 3)}/{fr(a, 3)})", "cinq mille sept cent trente sur zéro virgule six cent quatre-vingt-treize"),
                            (f"t ≈ {sci(t, 3)} ans", "t égale environ " + ds(t) + " ans")],
       "السؤال cinq. t égale t un demi sur ln deux، fois ln de a zéro sur a. l'application numérique: cinq mille sept cent trente sur zéro virgule six cent quatre-vingt-treize، fois ln de deux virgule cinq sur un virgule soixante-quinze. t égale environ " + ds(t) + " ans."),
  "explication": "ex_q5", "facile": "fa_q5"})
Q.append({"id": "6", "texte": f"Un autre objet en bois, de même masse, a aujourd'hui une activité a' = {fr(a2, 3)} Bq. Calculer son âge t', l'exprimer en nombre de demi-vies, puis expliquer pourquoi sa datation au carbone 14 est peu fiable.",
  "texte_dit": "السؤال six: objet آخر من الخشب، عندو نفس la masse، l'activité ديالو اليوم، a prime égale zéro virgule zéro cinq becquerel. حسب l'âge ديالو t prime، وقول شحال من demi-vie، وعلاش la datation ديالو ماشي مضمونة.",
  "reponse": valeur("t'", t2, "ans", f"t' = (5730/0,693) × ln({fr(a0, 3)}/{fr(a2, 3)}) ≈ {sci(t2, 3)} ans"),
  "clavier": {"aides": ["t' = (t½/ln 2)·ln(a₀/a')", "t'/t½", "ans"], "pieges": ["t' = t½·a₀/a'", "N devient nul"]},
  "aides": [aide("Même relation qu'à la question 5, avec a' ; puis divise t' par t½ = 5730 ans.",
                 "نفس la relation ديال السؤال cinq، مع a prime. ومن بعد قسم t prime sur t un demi."),
            aide("Après plusieurs demi-vies, a' n'est plus qu'une très petite fraction de a₀ : est-elle facile à mesurer avec précision ?",
                 "من بعد بزاف ديال demi-vies، a prime ولات صغيرة بزاف. واش ساهل نقيسوها مزيان؟")],
  "correction": correction([(f"6 : t' = (t½/ln 2)·ln(a₀/a') = (5730/0,693) × ln({fr(a0, 3)}/{fr(a2, 3)}) ≈ {sci(t2, 3)} ans", "t prime égale environ " + ds(t2) + " ans"),
                            (f"t'/t½ ≈ {fr(n2, 1)} : environ {fr(n2, 1)} demi-vies ; a'/a₀ = {fr(a2 / a0 * 100, 1)} %", "c'est environ " + dn(n2, 1) + " demi-vies"),
                            ("l'activité restante est très faible : sa mesure est imprécise, la méthode est limitée à quelques demi-vies du carbone 14", "l'activité اللي بقات صغيرة بزاف")],
       "السؤال six. t prime égale t un demi sur ln deux، fois ln de a zéro sur a prime. t prime égale environ " + ds(t2) + " ans. على t un demi، c'est environ " + dn(n2, 1) + " demi-vies: a prime، c'est " + dn(a2 / a0 * 100, 1) + " pour cent ديال a zéro. l'activité اللي بقات صغيرة بزاف، والقياس ديالها ماشي دقيق. إذن la méthode du carbone quatorze كتصلاح غير لبعض demi-vies."),
  "explication": "ex_q6", "facile": "fa_q6"})

lamDit = ds(lam)
EXP = [
  diapo_sim("ex_q1", "Question 1 : la désintégration β⁻ du carbone 14", "Dans le noyau, un neutron devient un proton : un électron ⁰₋₁e est émis ; A et Z se conservent.",
    SIMDES + "?type=beta_moins", "¹⁴₆C → ¹⁴₇N + ⁰₋₁e",
    "le carbone quatorze عندو بزاف ديال les neutrons. شوف لداخل le noyau: neutron كيولي proton، وكيخرج un électron: هي la particule bêta moins. l'équation: le carbone quatorze كيعطي A Z X، plus un électron. d'après les lois de Soddy: A se conserve، quatorze égale A plus zéro. و Z se conserve، six égale Z moins un، إذن Z égale sept. فالجدول، Z égale sept، c'est l'azote. le noyau fils هو l'azote quatorze.",
    [("A : 14 = A + 0 ⇒ A = 14", "quatorze égale A plus zéro"), ("Z : 6 = Z − 1 ⇒ Z = 7 : azote", "six égale Z moins un"), ("¹⁴₆C → ¹⁴₇N + ⁰₋₁e", "le noyau fils هو l'azote quatorze")],
    [dict(mot="le carbone quatorze عندو", commande="play_until", parametres={"moment": "noyau_pere"}),
     dict(mot="شوف لداخل", commande="play_until", parametres={"moment": "emission"}),
     dict(mot="l'équation:", commande="play_until", parametres={"moment": "equation"}),
     dict(mot="A se conserve", commande="play_until", parametres={"moment": "soddy_A"}),
     dict(mot="quatorze égale A plus zéro", cible="centre:0"),
     dict(mot="و Z se conserve", commande="play_until", parametres={"moment": "soddy_Z"}),
     dict(mot="six égale Z moins un", cible="centre:1"),
     dict(mot="le noyau fils هو l'azote quatorze", cible="centre:2")]),
  diapo_sim("ex_q2", "Question 2 : λ du carbone 14", "λ = (ln 2)/t½ s'exprime dans l'inverse de l'unité de t½ : ici an⁻¹.",
    SIML, "λ de l'iode 131 et λ du carbone 14",
    "lambda كتبدل مع le nucléide. l'unité ديالها هي المقلوب ديال الوقت. le carbone quatorze، t un demi égale cinq mille sept cent trente ans، إذن lambda كتكتب ب an puissance moins un. lambda égale ln deux sur t un demi، égale zéro virgule six cent quatre-vingt-treize sur cinq mille sept cent trente. lambda égale environ " + lamDit + " an puissance moins un. lambda صغيرة بزاف: le carbone quatorze كيتفكك بشوية.",
    [("λ = (ln 2)/t½", "lambda égale ln deux sur t un demi"), (f"λ = 0,693/5730 ≈ {lamS} an⁻¹", "lambda égale environ " + lamDit + " an puissance moins un")],
    [dict(mot="lambda كتبدل مع le nucléide", repere="carbone"),
     dict(mot="l'unité ديالها", commande="play_until", parametres={"moment": "trace"}),
     dict(mot="lambda كتكتب ب an puissance moins un", repere="lambda_carbone"),
     dict(mot="lambda égale ln deux sur t un demi", cible="centre:0"),
     dict(mot="lambda égale environ " + lamDit + " an puissance moins un", cible="centre:1"),
     dict(mot="lambda صغيرة بزاف", commande="play_until", parametres={"moment": "course"})]),
  diapo_sim("ex_q3", "Question 3 : pourquoi a₀ est l'activité du bois récent", "Vivant : échanges de CO₂, proportion de ¹⁴C constante ; mort : le ¹⁴C se désintègre sans être remplacé.",
    SIMDAT, "Trois temps : vivant, coupé, aujourd'hui",
    "شوف الشجرة الحية: ديما كتاخد le carbone من الهوا وكترجعو. les noyaux de carbone quatorze اللي كيتفككو، كيجيو بلاصتهم noyaux جداد. إذن l'activité ديالها كتبقى ثابتة، هي a zéro. كنقطعو الشجرة: هادشي كيوقف. le carbone quatorze كيتفكك، و l'activité كتنقص. إذن le bois récent كيعطينا a zéro: l'activité ديال le bois ancien ملي تقطع. ونفس la masse، حيت a égale lambda N: كثر ديال الخشب، كثر ديال les noyaux.",
    [("vivant : proportion de ¹⁴C constante → a₀", "l'activité ديالها كتبقى ثابتة"), ("a = λ·N : même masse", "a égale lambda N")],
    [dict(mot="شوف الشجرة الحية", commande="play_until", parametres={"moment": "vivant"}),
     dict(mot="les noyaux de carbone quatorze", commande="play_until", parametres={"moment": "echanges"}),
     dict(mot="l'activité ديالها كتبقى ثابتة", cible="centre:0"),
     dict(mot="كنقطعو الشجرة", commande="play_until", parametres={"moment": "mort"}),
     dict(mot="le carbone quatorze كيتفكك", commande="play_until", parametres={"moment": "desintegration"}),
     dict(mot="إذن le bois récent", repere="a0"),
     dict(mot="a égale lambda N", cible="centre:1")]),
  diapo_sim("ex_q4", "Question 4 : établir t = (1/λ)·ln(a₀/a)", "Diviser par a₀, prendre ln, retourner la fraction, isoler t.",
    SIMF + "?fig=fig_datation_demo", "La démonstration de la relation de datation",
    "كنبداو من la loi: a égale a zéro exponentielle moins lambda t. كنقسمو على a zéro: a sur a zéro égale exponentielle moins lambda t. كنديرو ln: ln de a sur a zéro égale moins lambda t. كنقلبو la fraction باش يمشي le signe moins: ln de a zéro sur a égale lambda t. كنعزلو t: t égale un sur lambda fois ln de a zéro sur a.",
    [("a/a₀ = e^(−λt)", "a sur a zéro égale exponentielle moins lambda t"), ("ln(a₀/a) = λ·t", "ln de a zéro sur a égale lambda t"), ("t = (1/λ)·ln(a₀/a)", "t égale un sur lambda fois ln de a zéro sur a")],
    [dict(mot="كنبداو من la loi", commande="play_until", parametres={"moment": "loi"}),
     dict(mot="كنقسمو على a zéro", commande="play_until", parametres={"moment": "rapport"}),
     dict(mot="a sur a zéro égale exponentielle moins lambda t", cible="centre:0"),
     dict(mot="كنديرو ln", commande="play_until", parametres={"moment": "ln"}),
     dict(mot="ln de a zéro sur a égale lambda t", cible="centre:1"),
     dict(mot="كنعزلو t", commande="play_until", parametres={"moment": "resultat"}),
     dict(mot="t égale un sur lambda fois ln de a zéro sur a", cible="centre:2")]),
  diapo_sim("ex_q5", "Question 5 : l'âge de la statuette", "t = (t½/ln 2)·ln(a₀/a) ; même rapport a/a₀ = 0,70 que dans l'exercice.",
    SIMDAT, "Le calcul de l'âge, au compteur",
    "فالتجربة، le bois récent عندو a zéro égale quatre cent dix-huit becquerels. حطينا l'activité ديال le bois ancien à " + nfr(a_sim) + " becquerels: نفس le rapport que l'exercice، zéro virgule soixante-dix. la formule: t égale t un demi sur ln deux، fois ln de a zéro sur a. la simulation كتعطي environ " + ds(t_sim) + " ans. فالتمرين، a zéro sur a égale deux virgule cinq sur un virgule soixante-quinze، نفس le rapport. إذن t égale environ " + ds(t) + " ans.",
    [("t = (t½/ln 2)·ln(a₀/a)", "t égale t un demi sur ln deux"), (f"t = (5730/0,693) × ln(2,5/1,75) ≈ {sci(t, 3)} ans", "إذن t égale environ " + ds(t) + " ans")],
    [dict(mot="فالتجربة، le bois récent", commande="set_parameters", parametres={"a_Bq": a_sim}),
     dict(mot="حطينا l'activité", commande="play_until", parametres={"moment": "mesure"}),
     dict(mot="la formule:", commande="play_until", parametres={"moment": "formule"}),
     dict(mot="t égale t un demi sur ln deux", cible="centre:0"),
     dict(mot="la simulation كتعطي", commande="play_until", parametres={"moment": "resultat"}),
     dict(mot="إذن t égale environ " + ds(t) + " ans", cible="centre:1")]),
  diapo_sim("ex_q6", "Question 6 : la limite de la méthode", "Après n demi-vies, il reste N₀/2ⁿ : jamais zéro, mais très peu.",
    SIMC + "?courbe=paliers", "Les paliers : N₀/2, N₀/4, N₀/8…",
    "فكل demi-vie، كيتقسم sur deux. après trois demi-vies: N zéro sur huit. la formule: N égale N zéro sur deux puissance n. العدد عمرو ما كيوصل à zéro، ولكن كيولي صغير بزاف. فالتمرين، t prime égale environ " + ds(t2) + " ans، c'est environ " + dn(n2, 1) + " demi-vies. a prime، c'est seulement " + dn(a2 / a0 * 100, 1) + " pour cent ديال a zéro. l'activité صغيرة بزاف، والقياس ديالها ماشي دقيق: la datation ماشي مضمونة.",
    [("N = N₀/2ⁿ", "N égale N zéro sur deux puissance n"), (f"t' ≈ {sci(t2, 3)} ans ≈ {fr(n2, 1)}·t½", "c'est environ " + dn(n2, 1) + " demi-vies")],
    [dict(mot="فكل demi-vie", commande="play_until", parametres={"moment": "palier_1"}),
     dict(mot="après trois demi-vies", commande="play_until", parametres={"moment": "palier_3"}),
     dict(mot="la formule:", commande="play_until", parametres={"moment": "formule"}),
     dict(mot="N égale N zéro sur deux puissance n", cible="centre:0"),
     dict(mot="c'est environ " + dn(n2, 1) + " demi-vies", cible="centre:1")]),
]

FAC = [
  qcm_facile("fa_q1", "Plus facile : l'équation β⁻ du carbone 14", "نتمرنو بسؤال ساهل. اختار l'équation الصحيحة.",
    "Le carbone 14 (Z = 6) est émetteur β⁻ (Z = 5 : B ; Z = 7 : N). Quelle équation est juste ?",
    ["¹⁴₆C → ¹⁴₅B + ⁰₁e", "¹⁴₆C → ¹⁴₇N + ⁰₋₁e", "¹⁴₆C → ¹⁰₄Be + ⁴₂He"], 1, {
      "1": {"juste": rep("برافو! bêta moins: un électron، و Z كيولي Z plus un. six égale sept moins un: c'est l'azote.", "Juste : β⁻ émet ⁰₋₁e ; 6 = 7 − 1, le fils est l'azote ¹⁴₇N.")},
      "0": {"1": rep("شوف la particule: zéro un e هو le positon، ديال bêta plus. bêta moins كتعطي un électron. عاود اختار.", "⁰₁e est le positon (β⁺). Une β⁻ émet un électron. Réessaie."),
            "2": rep("الجواب: le carbone quatorze كيعطي l'azote quatorze plus un électron. bêta moins كتعطي un électron، و Z كيولي Z plus un.", "Réponse : ¹⁴₆C → ¹⁴₇N + ⁰₋₁e (β⁻ : électron, Z augmente de 1).")},
      "2": {"1": rep("هادي désintégration alpha، ماشي bêta moins. شوف la particule. عاود اختار.", "Cette équation est une désintégration α. Réessaie."),
            "2": rep("الجواب: le carbone quatorze كيعطي l'azote quatorze plus un électron. فbêta moins، A ما كيتبدلش.", "Réponse : ¹⁴₆C → ¹⁴₇N + ⁰₋₁e : en β⁻, A ne change pas.")}},
    "Le carbone quatorze, Z égale six, est émetteur bêta moins. Quelle équation est juste ?"),
  vf_facile("fa_q2", "Plus facile : λ et t½", "سؤال ساهل على lambda: قول واش صحيحة ولا غالطة.", "t½(¹⁴C) = 5730 ans.", [
      ("λ = (ln 2)/t½ ≈ 1,21 × 10⁻⁴ an⁻¹.", True, "λ = 0,693/5730 ≈ 1,21 × 10⁻⁴ an⁻¹ : t½ en ans donne λ en an⁻¹."),
      ("λ = t½/(ln 2) ≈ 8270 an⁻¹.", False, "t½/(ln 2) est une durée (en ans), c'est 1/λ, pas λ."),
      ("Plus λ est petite, plus la décroissance est lente.", True, "t½ = (ln 2)/λ : petite λ, grande demi-vie.")]),
  assoc_facile("fa_q3", "Plus facile : la vie du carbone 14 dans le bois", "سؤال ساهل: ربط كل مرحلة مع شنو كيوقع ل l'activité.",
    "Trois moments de la vie d'un arbre.", "Relie chaque moment à ce que devient l'activité du ¹⁴C.",
    [("1", "l'arbre est vivant"), ("2", "l'arbre vient d'être coupé (t = 0)"), ("3", "aujourd'hui, le bois ancien")],
    [("a", "l'activité reste constante : échanges de CO₂ avec l'air"), ("b", "l'activité vaut a₀, puis commence à diminuer"), ("c", "l'activité a < a₀ mesurée au compteur")],
    {"1": "a", "2": "b", "3": "c"}, {
      "1-a": (True, "Juste : vivant, l'arbre remplace le ¹⁴C désintégré : activité constante.", "صحيح: ملي حية، كتعوض le carbone quatorze اللي تفكك، و l'activité كتبقى ثابتة."),
      "1-b": (False, "Non : tant que l'arbre vit, rien ne diminue. Pense aux échanges avec l'air.", "لا: ملي الشجرة حية، حتى حاجة ما كتنقص. فكر فالتبادل مع الهوا."),
      "1-c": (False, "Non : la mesure a < a₀ concerne le bois mort depuis longtemps.", "لا: a صغر من a zéro، هادي ديال الخشب اللي مات من زمان."),
      "2-a": (False, "Non : une fois coupé, l'arbre n'échange plus : l'activité ne reste plus constante.", "لا: ملي تقطعات، ما بقاتش كتبدل مع الهوا."),
      "2-b": (True, "Juste : à t = 0 l'activité vaut a₀, puis le ¹⁴C se désintègre sans être remplacé.", "صحيح: فt égale zéro، l'activité هي a zéro، ومن بعد كتنقص."),
      "2-c": (False, "Non : à t = 0, on n'a pas encore attendu : l'activité vaut encore a₀.", "لا: فt égale zéro، l'activité باقة هي a zéro."),
      "3-a": (False, "Non : le bois ancien est mort, il n'échange plus rien.", "لا: le bois ancien ميت، ما بقا كيبدل والو."),
      "3-b": (False, "Non : a₀ est l'activité au moment de la coupe, pas aujourd'hui.", "لا: a zéro هي l'activité ملي تقطعات، ماشي اليوم."),
      "3-c": (True, "Juste : aujourd'hui, on mesure a, plus petite que a₀.", "صحيح: اليوم كنقيسو a، صغر من a zéro.")},
    ("(1 ; a) (2 ; b) (3 ; c) : a₀ se mesure sur du bois récent, de même masse.", "a zéro كنقيسوها على bois récent، عندو نفس la masse.")),
  qcm_facile("fa_q4", "Plus facile : l'étape ln", "سؤال ساهل: شنو كتعطي ln؟",
    "a/a₀ = e^(−λt). En prenant ln, on obtient…",
    ["ln(a/a₀) = −λ·t", "ln(a/a₀) = λ·t", "ln(a/a₀) = e^(−λt)"], 0, {
      "0": {"juste": rep("مزيان! ln كيحيد e: ln de a sur a zéro égale moins lambda t. من بعد كنقلبو la fraction.", "Juste : ln(eˣ) = x, donc ln(a/a₀) = −λ·t.")},
      "1": {"1": rep("قريب، ولكن فين مشا le signe moins؟ ln كيحيد غير e. عاود اختار.", "Où est passé le signe moins ? ln enlève seulement e. Réessaie."),
            "2": rep("الجواب: ln de a sur a zéro égale moins lambda t. le signe moins كيبقى، وكيمشي غير ملي نقلبو la fraction.", "Réponse : ln(a/a₀) = −λ·t ; le moins part seulement en retournant la fraction.")},
      "2": {"1": rep("ln كيحيد e، ما كيخليهاش. عاود اختار.", "ln enlève e : il ne doit plus rester d'exponentielle. Réessaie."),
            "2": rep("الجواب: ln de a sur a zéro égale moins lambda t، حيت ln ديال exponentielle x كتعطي x.", "Réponse : ln(a/a₀) = −λ·t car ln(eˣ) = x.")}},
    "a sur a zéro égale exponentielle moins lambda t. En prenant ln, on obtient ?"),
  qcm_facile("fa_q5", "Plus facile : l'ordre de grandeur de l'âge", "سؤال ساهل: شحال تقريبا l'âge؟",
    "a/a₀ = 0,70 : il reste 70 % de l'activité. L'âge est…",
    ["plus petit qu'une demi-vie (5730 ans)", "entre une et deux demi-vies", "plus de deux demi-vies"], 0, {
      "0": {"juste": rep("برافو! il reste soixante-dix pour cent، كتر من النص: ما وصلناش demi-vie. l'âge environ deux mille neuf cent cinquante ans.", "Juste : 70 % > 50 %, on n'a pas atteint t½ ; t ≈ 2,95 × 10³ ans.")},
      "1": {"1": rep("فكر: après une demi-vie، il reste cinquante pour cent. soixante-dix pour cent: واش كتر ولا قل؟ عاود اختار.", "Après une demi-vie, il reste 50 %. 70 %, c'est plus ou moins ? Réessaie."),
            "2": rep("الجواب: قل من demi-vie. soixante-dix pour cent، plus que cinquante pour cent، إذن ما زال ما وصلناش t un demi.", "Réponse : moins d'une demi-vie, car 70 % > 50 %.")},
      "2": {"1": rep("après deux demi-vies، il reste seulement vingt-cinq pour cent. عاود اختار.", "Après deux demi-vies, il ne reste que 25 %. Réessaie."),
            "2": rep("الجواب: قل من demi-vie، حيت il reste soixante-dix pour cent، كتر من النص.", "Réponse : moins d'une demi-vie : il reste plus de la moitié.")}},
    "a sur a zéro égale zéro virgule soixante-dix : il reste soixante-dix pour cent de l'activité. L'âge est ?"),
  vf_facile("fa_q6", "Plus facile : jusqu'où peut-on dater ?", "سؤال ساهل: قول واش صحيحة ولا غالطة.", "Après n demi-vies, N = N₀/2ⁿ.", [
      ("Après 5 demi-vies, il ne reste plus aucun noyau de carbone 14.", False, "Il en reste N₀/2⁵ = N₀/32 ≈ 3 % : jamais zéro, mais très peu."),
      ("Après 5 ou 6 demi-vies, l'activité est si faible que sa mesure devient imprécise.", True, "C'est la limite de la datation au carbone 14 : quelques dizaines de milliers d'années."),
      ("Le carbone 14 convient pour dater un objet de quelques milliers d'années.", True, "Quelques milliers d'années, c'est moins de deux demi-vies : l'activité reste bien mesurable.")]),
]

QB = [
  {"id": "1", "texte": "Le carbone 14 est radioactif β⁻. Écrire l'équation de sa désintégration en précisant les lois utilisées, et identifier le noyau fils.",
   "reponse": phrase(EQ_ATT), "clavier": Q[0]["clavier"],
   "correction": correction([("1 : ¹⁴₆C → ᴬ_Z X + ⁰₋₁e ; Soddy : A = 14, Z = 7 : azote", "d'après les lois de Soddy"), ("¹⁴₆C → ¹⁴₇N + ⁰₋₁e", "l'azote quatorze")],
        "d'après les lois de Soddy، A égale quatorze و Z égale sept: c'est l'azote. le carbone quatorze كيعطي l'azote quatorze، plus un électron.")},
  {"id": "2", "texte": "Calculer, en an⁻¹, la constante radioactive λ du carbone 14.",
   "reponse": valeur("λ", lam, "an⁻¹", f"λ = (ln 2)/t½ = 0,693/5730 ≈ {lamS} an⁻¹"), "clavier": Q[1]["clavier"],
   "correction": correction([("2 : λ = (ln 2)/t½ = 0,693/5730", "lambda égale ln deux sur t un demi"), (f"λ ≈ {lamS} an⁻¹", "environ " + lamDit)],
        "lambda égale ln deux sur t un demi، égale environ " + lamDit + " an puissance moins un.")},
  {"id": "3", "texte": "Justifier le choix de a₀ : l'activité d'un os récent de même masse que l'os ancien.",
   "reponse": phrase(JUST.replace("l'arbre", "l'animal").replace("Le bois récent", "L'os récent").replace("le bois ancien au moment où l'arbre a été coupé", "l'os ancien au moment de la mort").replace("échange du CO₂ avec l'air", "échange du carbone avec son milieu (alimentation, respiration)").replace("de bois", "d'os")),
   "clavier": {"aides": ["échanges de carbone", "proportion de ¹⁴C constante", "a = λ·N", "même masse"], "pieges": ["l'os récent ne contient pas de ¹⁴C"]},
   "correction": correction([("3 : vivant, l'animal échange du carbone avec son milieu : proportion de ¹⁴C constante", "ملي الحيوان حي"),
                             ("l'os récent a l'activité de l'os ancien à la mort : a₀ ; même masse car a = λ·N", "a égale lambda N")],
        "ملي الحيوان حي، كيبدل le carbone مع اللي داير بيه، والنسبة ديال le carbone quatorze كتبقى ثابتة. إذن l'os récent عندو a zéro. ونفس la masse، حيت a égale lambda N.")},
  {"id": "4", "texte": "Montrer que l'âge t de l'os s'écrit : t = (1/λ)·ln(a₀/a).",
   "reponse": phrase(DEMO), "clavier": Q[3]["clavier"],
   "correction": correction([("4 : a/a₀ = e^(−λt) ⇒ ln(a₀/a) = λ·t", "ln de a zéro sur a égale lambda t"), ("t = (1/λ)·ln(a₀/a)", "t égale un sur lambda fois ln de a zéro sur a")],
        "a sur a zéro égale exponentielle moins lambda t. كنديرو ln ونقلبو la fraction: ln de a zéro sur a égale lambda t. إذن t égale un sur lambda fois ln de a zéro sur a.")},
  {"id": "5", "texte": "Calculer l'âge t de l'os.",
   "reponse": valeur("t", tb, "ans", f"t = (5730/0,693) × ln({fr(a0b, 3)}/{fr(ab, 3)}) ≈ {sci(tb, 3)} ans"), "clavier": Q[4]["clavier"],
   "correction": correction([(f"5 : t = (t½/ln 2)·ln(a₀/a) = (5730/0,693) × ln({fr(a0b, 3)}/{fr(ab, 3)})", "t égale t un demi sur ln deux"), (f"t ≈ {sci(tb, 3)} ans", "environ " + ds(tb) + " ans")],
        "t égale t un demi sur ln deux، fois ln de trois sur un virgule soixante-cinq. t égale environ " + ds(tb) + " ans.")},
  {"id": "6", "texte": f"Un autre os, de même masse, a une activité a' = {fr(a2b, 3)} Bq. Calculer son âge t', l'exprimer en nombre de demi-vies, puis expliquer pourquoi sa datation est peu fiable.",
   "reponse": valeur("t'", t2b, "ans", f"t' = (5730/0,693) × ln({fr(a0b, 3)}/{fr(a2b, 3)}) ≈ {sci(t2b, 3)} ans"), "clavier": Q[5]["clavier"],
   "correction": correction([(f"6 : t' ≈ {sci(t2b, 3)} ans, soit environ {fr(n2b, 1)} demi-vies", "t prime égale environ " + ds(t2b) + " ans"),
                             ("activité restante très faible : mesure imprécise, datation peu fiable", "l'activité صغيرة بزاف")],
        "t prime égale environ " + ds(t2b) + " ans، c'est environ " + dn(n2b, 1) + " demi-vies. l'activité صغيرة بزاف، والقياس ديالها ماشي دقيق.")},
]

EX = {
  "id": "phys_ex_ch4_carbone_5", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "radioactivite", "cours": "phys_ch4_radioactivite",
  "titre": "Dater une statuette en bois au carbone 14", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série).",
  "competences": ["Écrire une équation β⁻ avec les lois de Soddy", "Calculer λ = (ln 2)/t½", "Justifier le choix de a₀ en datation",
                  "Établir t = (1/λ)·ln(a₀/a)", "Calculer un âge et discuter la limite de la méthode"],
  "enonce": {
    "intro": "Un archéologue trouve une statuette en bois. Pour la dater, on mesure au compteur l'activité a d'un échantillon de ce bois, puis l'activité a₀ d'un échantillon de bois récent de même masse (document). On choisit comme origine des dates (t = 0) le moment où l'arbre a été coupé.",
    "intro_dit": "دابا نقراو l'énoncé. واحد العالم ديال الآثار لقى statuette ديال الخشب. باش نعرفو l'âge ديالها، كنقيسو ب le compteur l'activité a ديال échantillon من هاد الخشب، و l'activité a zéro ديال bois récent، عندو نفس la masse. t égale zéro هي اللحظة اللي تقطعات فيها الشجرة.",
    "figures": [schema("bois de la statuette", a, a0)],
    "donnees": ["t½(¹⁴C) = 5730 ans", "ln 2 ≈ 0,693", "Extrait du tableau : ₅B ; ₆C ; ₇N ; ₈O"],
    "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXP}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FAC}]},
  "similaire": {"id": "phys_ex_ch4_carbone_5_b", "titre": "Même exercice, autres données : un os ancien",
    "enonce": {
      "intro": "On date un os trouvé dans une grotte. Le compteur donne l'activité a d'un échantillon de cet os et l'activité a₀ d'un échantillon d'os récent de même masse (document). t = 0 : la mort de l'animal.",
      "intro_dit": "نفس التمرين، بقيم أخرى: عظم قديم. كنقيسو l'activité a ديالو، و a zéro ديال عظم جديد عندو نفس la masse.",
      "figures": [schema("os ancien", ab, a0b, "os récent", "matière osseuse")],
      "donnees": ["t½(¹⁴C) = 5730 ans", "ln 2 ≈ 0,693", "Extrait du tableau : ₅B ; ₆C ; ₇N ; ₈O"],
      "questions": QB}},
}

if __name__ == "__main__":
    ecrire(EX)
