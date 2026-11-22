# Exercice difficile (« Supérieur ») de physique (ch. 4, décroissance radioactive) : dater une roche par la famille
# uranium 235 → plomb 207.
# Sources comparées (skill exercices § 2) :
#  - exploration radioactivite.json : cas_types « famille » (x et y : A d'abord, puis Z), « datation » (roche :
#    r = N(fils)/N(père) = e^(λt) − 1), « nombre_noyaux » (N = (m/M)·N_A), « pourcentage » ; pièges « coefficients
#    oubliés sur A et Z », « m en kg avec M en g/mol », « utilise le λ ou le N du fils dans la loi » ;
#    exclus_hors_programme : « un seul noyau père, un fils stable » (pas de Bateman) : les noyaux intermédiaires sont
#    supposés de vie courte, en nombre négligeable, et tout le plomb 207 vient de l'uranium 235.
#  - nationaux comparés : 2012 N (²³⁸U → ²⁰⁶Pb : 8 α et 6 β⁻, cité par les professeurs et animé par segre.html),
#    2020 R ex. 3 (roche marine ²³⁴U → ²³⁰Th : « montrer que r = e^(λt) − 1 », r₁ à t₁ donnée), 2024 R ex. 3
#    (famille, diagramme). Le nôtre : autre famille (²³⁵U → ²⁰⁷Pb : 7 α et 4 β⁻), r calculé à partir de MASSES,
#    l'âge cherché (et non r), le pourcentage désintégré, puis une lecture critique (plomb initial) : au-dessus du
#    national, deux notions combinées (famille + datation), sans être un sujet national.
#  - séries en ligne (recherche du 22/11/2026 ; talamidi.com non joignable depuis cette session, seuls les extraits du
#    moteur lus) : série N. Naceiri Mrabti « datation uranium-plomb » (masses d'uranium 238 et de plomb 206),
#    talamidi « famille de l'uranium 238 » et « géochronologie », labolycée 2025 « datation d'une roche », eduscol.
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


SIMS = "/media/simulations/physics/radioactivite-tableau/segre.html"
SIMF = "/media/simulations/physics/radioactivite-tableau/figures.html"
SIMR = "/media/simulations/physics/radioactivite-tableau/rappels.html"
SIMP = "/media/simulations/physics/radioactivite-tableau/pourcentages.html"
LN2 = 0.693

SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def nuc(A, Z, X):
    return f"{str(A).translate(SUP)}{str(Z).translate(SUB)}{X}"


def calc(P):
    y = (P["A"] - P["Af"]) // 4
    x = P["Zf"] + 2 * y - P["Z"]
    r = (P["mF"] / P["MF"]) / (P["mP"] / P["MP"])
    t = P["T"] / LN2 * math.log(1 + r)
    p = r / (1 + r) * 100
    return x, y, r, t, p


EXA = dict(A=235, Z=92, X="U", nomP="uranium 235", Af=207, Zf=82, Xf="Pb", nomF="plomb 207", T=7.04e8,
           mP=2.40, mF=0.85, MP=235, MF=207, roche="un zircon (cristal d'une roche granitique)")
EXB = dict(A=232, Z=90, X="Th", nomP="thorium 232", Af=208, Zf=82, Xf="Pb", nomF="plomb 208", T=1.40e10,
           mP=5.00, mF=0.18, MP=232, MF=208, roche="un échantillon de roche volcanique")
xA, yA, rA, tA, pA = calc(EXA)
xB, yB, rB, tB, pB = calc(EXB)
assert (xA, yA) == (4, 7) and (xB, yB) == (4, 6)


def figure(P):
    pere, fils = nuc(P["A"], P["Z"], P["X"]), nuc(P["Af"], P["Zf"], P["Xf"])
    return {"type": "schema", "titre": "La roche à sa formation et aujourd'hui", "cadre": {"l": 4.4, "h": 2.0},
            "legende": f"À t = 0, la roche ne contient pas de {P['nomF']} ; aujourd'hui, on mesure les masses des deux nucléides.",
            "elements": [
                {"f": "rect", "de": [0.15, 0.3], "a": [1.75, 1.45], "couleur": "faible", "arrondi": True},
                {"f": "texte", "at": [0.95, 1.65], "t": "t = 0 (formation)", "couleur": "cyan", "ancre": "centre"},
                {"f": "texte", "at": [0.95, 1.05], "t": f"{pere} : N₀ noyaux", "couleur": "orange", "ancre": "centre"},
                {"f": "texte", "at": [0.95, 0.6], "t": f"{fils} : 0", "couleur": "vert", "ancre": "centre"},
                {"f": "fleche", "de": [1.85, 0.9], "a": [2.55, 0.9], "couleur": "blanc", "texte": "famille", "pos": "n"},
                {"f": "rect", "de": [2.65, 0.3], "a": [4.25, 1.45], "couleur": "faible", "arrondi": True},
                {"f": "texte", "at": [3.45, 1.65], "t": "aujourd'hui (date t)", "couleur": "cyan", "ancre": "centre"},
                {"f": "texte", "at": [3.45, 1.05], "t": f"{pere} : m = {fr(P['mP'], 2)} mg", "couleur": "orange", "ancre": "centre"},
                {"f": "texte", "at": [3.45, 0.6], "t": f"{fils} : m = {fr(P['mF'], 2)} mg", "couleur": "vert", "ancre": "centre"}]}


def intro(P):
    pere, fils = nuc(P["A"], P["Z"], P["X"]), nuc(P["Af"], P["Zf"], P["Xf"])
    le = "L'" if P["nomP"][0] in "aeiouy" else "Le "
    du = "de l'" if P["nomP"][0] in "aeiouy" else "du "
    return (f"On veut dater {P['roche']}. {le}{P['nomP']} ({pere}) se transforme, par une suite de désintégrations α et β⁻ "
            f"(une famille radioactive), en {P['nomF']} ({fils}), stable. Hypothèses : à sa formation (t = 0), la roche ne contenait "
            f"pas de {P['nomF']} ; tout le {P['nomF']} vient {du}{P['nomP']} ; les noyaux intermédiaires de la famille sont en nombre "
            f"négligeable. Le document donne la composition de la roche aujourd'hui (date t).")


def donnees(P):
    return [f"t½({P['nomP']}) = {sci(P['T'], 3)} ans", "ln 2 ≈ 0,693",
            f"M({P['X']}) = {P['MP']} g/mol ; M({P['Xf']}) = {P['MF']} g/mol", "N_A = 6,02 × 10²³ mol⁻¹"]


def eq_famille(P):
    return f"{nuc(P['A'], P['Z'], P['X'])} → {nuc(P['Af'], P['Zf'], P['Xf'])} + x ⁰₋₁e + y ⁴₂He"


def att_famille(P, x, y):
    return (f"Lois de Soddy : conservation de A : {P['A']} = {P['Af']} + 0·x + 4y ⇒ y = ({P['A']} − {P['Af']})/4 = {y} ; "
            f"conservation de Z : {P['Z']} = {P['Zf']} − x + 2y ⇒ x = {P['Zf']} + 2y − {P['Z']} = {x} : {y} désintégrations α et {x} désintégrations β⁻")


DEMO = ("N_U(t) = N₀·e^(−λt) ; chaque noyau d'uranium désintégré donne un noyau de plomb : N_Pb = N₀ − N_U = N₀(1 − e^(−λt)) ; "
        "N_Pb/N_U = (1 − e^(−λt))/e^(−λt) = e^(λt) − 1 ; donc e^(λt) = 1 + N_Pb/N_U, λ·t = ln(1 + N_Pb/N_U), "
        "et avec λ = (ln 2)/t½ : t = (t½/ln 2)·ln(1 + N_Pb/N_U)")
CRIT = ("L'âge calculé est trop grand (surestimé) : le plomb 207 mesuré aujourd'hui comprend le plomb initial, qui ne vient pas "
        "de la désintégration de l'uranium ; N_Pb est donc trop grand, le rapport r aussi, et t = (t½/ln 2)·ln(1 + r) croît avec r.")

rS = f"{rA:.3f}".replace(".", ",")
Q = []
Q.append({"id": "1", "texte": f"L'équation bilan de la famille s'écrit : {eq_famille(EXA)}. Déterminer x et y en précisant les lois utilisées.",
  "texte_dit": "السؤال un: l'équation bilan ديال la famille: l'uranium deux cent trente-cinq كيعطي le plomb deux cent sept، plus x électrons، plus y noyaux d'hélium. حدد x و y، وقول les lois اللي استعملتي.",
  "reponse": phrase(att_famille(EXA, xA, yA)),
  "clavier": {"aides": ["conservation de A", "conservation de Z", "4y", "2y", "−x"], "pieges": ["235 = 207 + x + 4y", "92 = 82 + x + 2y"]},
  "aides": [aide("Commence par A : l'électron a A = 0, donc l'équation de A ne contient que y.",
                 "بدا ب A: l'électron عندو A égale zéro، إذن l'équation ديال A فيها غير y."),
            aide("A : 235 = 207 + 4y ; puis Z : 92 = 82 − x + 2y (l'électron compte −1, l'hélium +2).",
                 "A: deux cent trente-cinq égale deux cent sept plus quatre y. من بعد Z: quatre-vingt-douze égale quatre-vingt-deux moins x plus deux y.")],
  "correction": correction([("1 : d'après les lois de Soddy, conservation de A : 235 = 207 + 0·x + 4y", "la conservation de A"),
                            (f"y = (235 − 207)/4 = {yA}", f"y égale {nfr(yA)}"),
                            (f"conservation de Z : 92 = 82 − x + 2y ⇒ x = 82 + 2 × {yA} − 92 = {xA}", f"x égale {nfr(xA)}"),
                            (f"la famille comporte {yA} désintégrations α et {xA} désintégrations β⁻", "le résultat")],
       f"السؤال un. d'après les lois de Soddy، la conservation de A: deux cent trente-cinq égale deux cent sept plus quatre y، donc quatre y égale vingt-huit، و y égale {nfr(yA)}. la conservation de Z: quatre-vingt-douze égale quatre-vingt-deux moins x plus deux y. إذن x égale quatre-vingt-deux plus quatorze moins quatre-vingt-douze، x égale {nfr(xA)}. le résultat: {nfr(yA)} désintégrations alpha، et {nfr(xA)} désintégrations bêta moins."),
  "explication": "ex_q1", "facile": "fa_q1"})
Q.append({"id": "2", "texte": "On note N_U et N_Pb les nombres de noyaux d'uranium 235 et de plomb 207 dans la roche à la date t. Montrer que l'âge de la roche s'écrit : t = (t½/ln 2)·ln(1 + N_Pb/N_U).",
  "texte_dit": "السؤال deux: N U و N Pb هوما les nombres ديال les noyaux d'uranium و de plomb فla roche، فla date t. بين بلي l'âge ديال la roche كيتكتب: t égale t un demi sur ln deux، fois ln de un plus N Pb sur N U.",
  "reponse": phrase(DEMO),
  "clavier": {"aides": ["N_U = N₀·e^(−λt)", "N_Pb = N₀ − N_U", "e^(λt)", "λ = (ln 2)/t½"], "pieges": ["N_Pb = N₀·e^(−λt)", "N_Pb = N_U"]},
  "aides": [aide("Le père suit la loi de décroissance ; chaque uranium qui se désintègre donne (au bout de la famille) un plomb : exprime N_Pb avec N₀ et N_U.",
                 "le père كيتبع la loi de décroissance. كل uranium تفكك، كيعطي فاللخر plomb واحد. كتب N Pb ب N zéro و N U."),
            aide("Forme le rapport N_Pb/N_U : N₀ se simplifie et on trouve e^(λt) − 1 ; puis prends ln.",
                 "دير le rapport N Pb sur N U: N zéro كيمشي، وكتلقى exponentielle lambda t moins un. ومن بعد دير ln.")],
  "correction": correction([("2 : N_U = N₀·e^(−λt) ; chaque U désintégré donne un Pb : N_Pb = N₀ − N_U = N₀(1 − e^(−λt))", "N Pb égale N zéro moins N U"),
                            ("N_Pb/N_U = (1 − e^(−λt))/e^(−λt) = e^(λt) − 1", "exponentielle lambda t moins un"),
                            ("e^(λt) = 1 + N_Pb/N_U ⇒ λ·t = ln(1 + N_Pb/N_U)", "lambda t égale ln de un plus N Pb sur N U"),
                            ("λ = (ln 2)/t½ ⇒ t = (t½/ln 2)·ln(1 + N_Pb/N_U)", "t égale t un demi sur ln deux")],
       "السؤال deux. le père: N U égale N zéro exponentielle moins lambda t. كل uranium تفكك كيعطي plomb واحد، إذن N Pb égale N zéro moins N U، égale N zéro fois، un moins exponentielle moins lambda t. le rapport: N Pb sur N U، N zéro كيمشي، وكنلقاو exponentielle lambda t moins un. إذن exponentielle lambda t égale un plus N Pb sur N U. كنديرو ln: lambda t égale ln de un plus N Pb sur N U. و lambda égale ln deux sur t un demi: إذن t égale t un demi sur ln deux، fois ln de un plus N Pb sur N U."),
  "explication": "ex_q2", "facile": "fa_q2"})
Q.append({"id": "3", "texte": "À partir du document, calculer le rapport r = N_Pb/N_U aujourd'hui.",
  "texte_dit": "السؤال trois: من la figure، حسب le rapport r égale N Pb sur N U، اليوم.",
  "reponse": valeur("r", rA, "", f"r = (m_Pb/M_Pb)/(m_U/M_U) = (0,85/207)/(2,40/235) ≈ {rS}"),
  "clavier": {"aides": ["N = (m/M)·N_A", "N_A se simplifie", "A.N. : (0,85/207)/(2,40/235)"], "pieges": ["r = m_Pb/m_U", "r = (m_U/M_U)/(m_Pb/M_Pb)"]},
  "aides": [aide("Chaque nombre de noyaux se calcule avec sa masse et sa masse molaire : N = (m/M)·N_A.",
                 "كل nombre de noyaux كنحسبوه ب la masse و la masse molaire ديالو: N égale m sur M fois N A."),
            aide("Dans le rapport, N_A se simplifie (et les mg aussi) : r = (m_Pb/M_Pb)/(m_U/M_U). Attention : les masses molaires sont différentes.",
                 "فle rapport، N A كيمشي، والوحدة ديال la masse حتى هي. r égale m Pb sur M Pb، sur m U sur M U. رد البال: les masses molaires ماشي بحال بحال.")],
  "correction": correction([("3 : N = (m/M)·N_A, donc r = N_Pb/N_U = (m_Pb/M_Pb)/(m_U/M_U) (N_A se simplifie)", "N A كيمشي"),
                            ("A.N. : r = (0,85/207)/(2,40/235)", "zéro virgule quatre-vingt-cinq sur deux cent sept"),
                            (f"r ≈ {rS}", "r égale environ " + dn(rA, 3))],
       "السؤال trois. N égale m sur M fois N A. فle rapport، N A كيمشي: r égale m Pb sur M Pb، sur m U sur M U. l'application numérique: zéro virgule quatre-vingt-cinq sur deux cent sept، sur deux virgule quarante sur deux cent trente-cinq. r égale environ " + dn(rA, 3) + "."),
  "explication": "ex_q3", "facile": "fa_q3"})
Q.append({"id": "4", "texte": "Calculer l'âge t de la roche.",
  "texte_dit": "السؤال quatre: حسب l'âge t ديال la roche.",
  "reponse": valeur("t", tA, "ans", f"t = (t½/ln 2)·ln(1 + r) = (7,04 × 10⁸/0,693) × ln(1 + {rS}) ≈ {sci(tA, 3)} ans"),
  "clavier": {"aides": ["t = (t½/ln 2)·ln(1 + r)", "A.N. : (7,04 × 10⁸/0,693) × ln(1,402)", "ans"], "pieges": ["ln(r)", "t = t½·r"]},
  "aides": [aide("Utilise la relation de la question 2 avec le r de la question 3 ; t½ est en années, t le sera aussi.",
                 "استعمل la relation ديال السؤال deux، مع r ديال السؤال trois. t un demi بالعوام، إذن t حتى هو بالعوام."),
            aide("Calcule d'abord ln(1 + r) à la calculatrice, puis multiplie par t½/ln 2.",
                 "حسب الأول ln de un plus r بالآلة الحاسبة، ومن بعد ضربها ف t un demi sur ln deux.")],
  "correction": correction([("4 : t = (t½/ln 2)·ln(1 + r)", "t égale t un demi sur ln deux"),
                            (f"A.N. : t = (7,04 × 10⁸/0,693) × ln(1 + {rS})", "sept virgule zéro quatre fois dix puissance huit"),
                            (f"t ≈ {sci(tA, 3)} ans", "t égale environ " + ds(tA) + " ans")],
       "السؤال quatre. t égale t un demi sur ln deux، fois ln de un plus r. l'application numérique: sept virgule zéro quatre fois dix puissance huit، sur zéro virgule six cent quatre-vingt-treize، fois ln de un virgule " + nfr(round(rA * 1000)) + ". t égale environ " + ds(tA) + " ans."),
  "explication": "ex_q4", "facile": "fa_q4"})
Q.append({"id": "5", "texte": "Calculer le pourcentage des noyaux d'uranium 235 présents à la formation de la roche qui se sont désintégrés depuis.",
  "texte_dit": "السؤال cinq: حسب le pourcentage ديال les noyaux d'uranium اللي كانو فالبداية، واللي تفككو من داك الوقت.",
  "reponse": valeur("p", pA, "%", f"p = N_Pb/N₀ = N_Pb/(N_U + N_Pb) = r/(1 + r) = {rS}/(1 + {rS}) ≈ {fr(pA, 1)} %"),
  "clavier": {"aides": ["N₀ = N_U + N_Pb", "désintégrés = N_Pb", "r/(1 + r)", "%"], "pieges": ["p = r", "p = N_U/N₀"]},
  "aides": [aide("Combien de noyaux d'uranium y avait-il au départ ? Chaque uranium est aujourd'hui soit un uranium, soit un plomb.",
                 "شحال كان ديال uranium فالبداية؟ كل uranium، اليوم، يا باقي uranium، يا ولا plomb."),
            aide("N₀ = N_U + N_Pb et les désintégrés sont N_Pb : p = N_Pb/(N_U + N_Pb) = r/(1 + r).",
                 "N zéro égale N U plus N Pb، و les désintégrés هوما N Pb. إذن p égale N Pb sur N U plus N Pb، يعني r sur un plus r.")],
  "correction": correction([("5 : N₀ = N_U + N_Pb ; les noyaux désintégrés sont N_Pb", "N zéro égale N U plus N Pb"),
                            (f"p = N_Pb/(N_U + N_Pb) = r/(1 + r) = {rS}/(1 + {rS})", "r sur un plus r"),
                            (f"p ≈ {fr(pA, 1)} %", "environ " + dn(pA, 1) + " pour cent")],
       "السؤال cinq. كل uranium يا باقي، يا ولا plomb: N zéro égale N U plus N Pb، و les désintégrés هوما N Pb. نقسمو على N U: p égale r sur un plus r. p égale environ " + dn(pA, 1) + " pour cent."),
  "explication": "ex_q5", "facile": "fa_q5"})
Q.append({"id": "6", "texte": "Une analyse plus fine montre qu'à sa formation la roche contenait déjà un peu de plomb 207. L'âge calculé à la question 4 est-il trop grand ou trop petit ? Justifier.",
  "texte_dit": "السؤال six: تحليل أدق بين بلي la roche، ملي تكونات، كان فيها شوية ديال le plomb deux cent sept. واش l'âge اللي حسبتي فالسؤال quatre كبير بزاف ولا صغير بزاف؟ برر.",
  "reponse": phrase(CRIT),
  "clavier": {"aides": ["N_Pb mesuré = plomb initial + plomb formé", "r trop grand", "t croît avec r"], "pieges": ["l'âge ne change pas", "trop petit"]},
  "aides": [aide("Le plomb mesuré aujourd'hui : vient-il entièrement de l'uranium ? Que devient alors r ?",
                 "le plomb اللي قسنا اليوم، واش جا كامل من l'uranium؟ إذن r، واش كبر ولا صغر؟"),
            aide("t = (t½/ln 2)·ln(1 + r) augmente quand r augmente.", "t égale t un demi sur ln deux fois ln de un plus r: كلما كبر r، كلما كبر t.")],
  "correction": correction([("6 : le plomb 207 mesuré = plomb initial + plomb formé par l'uranium", "le plomb اللي قسنا"),
                            ("donc N_Pb utilisé est trop grand, et r aussi", "r كبير بزاف"),
                            ("t = (t½/ln 2)·ln(1 + r) croît avec r : l'âge calculé est trop grand (surestimé)", "l'âge اللي حسبنا كبير بزاف")],
       "السؤال six. le plomb اللي قسنا فيه زوج: le plomb اللي كان فالبداية، و le plomb اللي جا من l'uranium. إذن N Pb اللي استعملنا كبير بزاف، و r كبير بزاف. و t égale t un demi sur ln deux fois ln de un plus r، كيكبر مع r. إذن l'âge اللي حسبنا كبير بزاف: surestimé."),
  "explication": "ex_q6", "facile": "fa_q6"})

EXP = [
  diapo_sim("ex_q1", "Question 1 : compter les α et les β⁻ d'une famille", "A d'abord (l'électron a A = 0) : y ; puis Z : x.",
    SIMS + "?vue=famille", "La famille de l'uranium 238 sur le diagramme (N, Z)",
    "شوف la famille ديال الدرس: l'uranium deux cent trente-huit هو le père. أول flèche: désintégration alpha. من بعد bêta moins. وكتكمل، flèche من بعد flèche، حتى ل le plomb deux cent six، stable. le bilan: huit alpha et six bêta moins. فالتمرين، la famille ديال l'uranium deux cent trente-cinq. كنبداو ب A: l'électron ما كيبدلش A. deux cent trente-cinq égale deux cent sept plus quatre y، إذن y égale sept. من بعد Z: quatre-vingt-douze égale quatre-vingt-deux moins x plus deux y، إذن x égale quatre. le bilan: sept alpha et quatre bêta moins.",
    [("A : 235 = 207 + 4y ⇒ y = 7", "إذن y égale sept"), ("Z : 92 = 82 − x + 2y ⇒ x = 4", "إذن x égale quatre")],
    [dict(mot="شوف la famille", commande="play_until", parametres={"moment": "depart"}),
     dict(mot="أول flèche", commande="play_until", parametres={"moment": "premiere_alpha"}),
     dict(mot="من بعد bêta moins", commande="play_until", parametres={"moment": "premiere_beta"}),
     dict(mot="وكتكمل", commande="play_until", parametres={"moment": "arrivee"}),
     dict(mot="le bilan: huit alpha", commande="play_until", parametres={"moment": "bilan"}),
     dict(mot="le bilan: huit alpha", repere="bilan"),
     dict(mot="إذن y égale sept", cible="centre:0"),
     dict(mot="إذن x égale quatre", cible="centre:1")]),
  diapo_sim("ex_q2", "Question 2 : du rapport fils/père à l'âge", "N_fils = N₀ − N_père ; le rapport vaut e^(λt) − 1 ; ln donne t.",
    SIMF + "?fig=fig_rapport_fils_pere", "Le rapport fils / père",
    "le père كيتبع la loi: N zéro exponentielle moins lambda t. فالبداية، ما كاين حتى fils. كل père تفكك كيعطي fils واحد. إذن N fils égale N zéro moins N père. le rapport: r égale N fils sur N père. N zéro كيمشي من الفوق ومن التحت، و r égale exponentielle lambda t moins un. إذن exponentielle lambda t égale un plus r. كنديرو ln: lambda t égale ln de un plus r. و lambda égale ln deux sur t un demi: t égale t un demi sur ln deux، fois ln de un plus r. فالتمرين، le père هو l'uranium، و le fils هو le plomb.",
    [("r = N_fils/N_père = e^(λt) − 1", "r égale exponentielle lambda t moins un"), ("t = (t½/ln 2)·ln(1 + r)", "t égale t un demi sur ln deux، fois ln de un plus r")],
    [dict(mot="le père كيتبع la loi", commande="play_until", parametres={"moment": "pere"}),
     dict(mot="كل père تفكك", commande="play_until", parametres={"moment": "fils"}),
     dict(mot="le rapport: r égale", commande="play_until", parametres={"moment": "rapport"}),
     dict(mot="r égale exponentielle lambda t moins un", cible="centre:0"),
     dict(mot="t égale t un demi sur ln deux، fois ln de un plus r", cible="centre:1")]),
  diapo_sim("ex_q3", "Question 3 : le rapport à partir des masses", "N = (m/M)·N_A ; dans le rapport, N_A se simplifie.",
    SIMF + "?fig=fig_masse_N", "De la masse au nombre de noyaux",
    "باش نلقاو العدد ديال les noyaux، الأول la quantité de matière: n égale m sur M. من بعد العدد: N égale m sur M fois N A. فالتمرين، كنديرو هادشي ل le plomb و ل l'uranium، ومن بعد le rapport. N A كيمشي: r égale m Pb sur M Pb، sur m U sur M U. رد البال: M ديال le plomb ماشي M ديال l'uranium. r égale environ " + dn(rA, 3) + ".",
    [("N = (m/M)·N_A", "N égale m sur M fois N A"), (f"r = (0,85/207)/(2,40/235) ≈ {rS}", "r égale environ " + dn(rA, 3))],
    [dict(mot="الأول la quantité", commande="play_until", parametres={"moment": "quantite"}),
     dict(mot="من بعد العدد", commande="play_until", parametres={"moment": "nombre"}),
     dict(mot="N égale m sur M fois N A", cible="centre:0"),
     dict(mot="r égale environ " + dn(rA, 3), cible="centre:1")]),
  diapo_sim("ex_q4", "Question 4 : ln à la calculatrice", "ln enlève e ; t = (t½/ln 2)·ln(1 + r).",
    SIMR + "?vue=ln", "Les deux machines : e et ln",
    "عندنا les deux machines: e و ln. x كيدخل فla machine e، وكيخرج exponentielle x. ملي كتدخل فla machine ln، x كيرجع: ln كيحيد e. هادشي اللي درنا: exponentielle lambda t égale un plus r، إذن lambda t égale ln de un plus r. بالآلة الحاسبة، كنحسبو ln de un virgule " + nfr(round(rA * 1000)) + ". من بعد كنضربو ف t un demi sur ln deux: t égale environ " + ds(tA) + " ans.",
    [("λ·t = ln(1 + r)", "lambda t égale ln de un plus r"), (f"t ≈ {sci(tA, 3)} ans", "t égale environ " + ds(tA) + " ans")],
    [dict(mot="عندنا les deux machines", commande="play_until", parametres={"moment": "machines"}),
     dict(mot="x كيدخل", commande="play_until", parametres={"moment": "apres_e"}),
     dict(mot="ملي كتدخل فla machine ln", commande="play_until", parametres={"moment": "apres_ln"}),
     dict(mot="lambda t égale ln de un plus r", cible="centre:0"),
     dict(mot="بالآلة الحاسبة", commande="play_until", parametres={"moment": "calculatrice"}),
     dict(mot="t égale environ " + ds(tA) + " ans", cible="centre:1")]),
  diapo_sim("ex_q5", "Question 5 : restants et désintégrés", "Désintégrés = N₀ − restants ; ici les désintégrés sont devenus du plomb.",
    SIMP, "Cent noyaux : restants et désintégrés",
    "شوف les cent noyaux. trente pour cent désintégrés: il reste soixante-dix pour cent. quatre-vingt-dix pour cent désintégrés: il reste dix pour cent. ديما: les restants، plus les désintégrés، égale N zéro. فالتمرين، les restants هوما N U، و les désintégrés ولاو plomb: N Pb. إذن N zéro égale N U plus N Pb، و p égale r sur un plus r، égale environ " + dn(pA, 1) + " pour cent.",
    [("N₀ = N_U + N_Pb", "إذن N zéro égale N U plus N Pb"), (f"p = r/(1 + r) ≈ {fr(pA, 1)} %", "p égale r sur un plus r")],
    [dict(mot="شوف les cent noyaux", repere="echantillon"),
     dict(mot="trente pour cent désintégrés", commande="play_until", parametres={"moment": "trente"}),
     dict(mot="quatre-vingt-dix pour cent désintégrés", commande="play_until", parametres={"moment": "quatre_vingt_dix"}),
     dict(mot="إذن N zéro égale N U plus N Pb", cible="centre:0"),
     dict(mot="p égale r sur un plus r", cible="centre:1")]),
  diapo_sim("ex_q6", "Question 6 : lecture critique, le plomb initial", "Plus r est grand, plus l'âge calculé est grand.",
    SIMF + "?fig=fig_rapport_fils_pere&depart=fils", "r = 0 au départ, puis r croît avec l'âge",
    "شوف: فالبداية، ما كاين حتى fils، و r égale zéro. وكلما دوز الوقت، كلما كبر r. إذن r هو الساعة ديال la roche. ولكن يلا كان شوية ديال le plomb من الأول، le plomb اللي قسنا كبير بزاف، و r كبير بزاف. الساعة كتزيد: l'âge اللي حسبنا كبير بزاف. surestimé.",
    [("t = (t½/ln 2)·ln(1 + r) croît avec r", "كلما كبر r"), ("plomb initial ⇒ r trop grand ⇒ t surestimé", "l'âge اللي حسبنا كبير بزاف")],
    [dict(mot="شوف: فالبداية", commande="play_until", parametres={"moment": "rapport"}),
     dict(mot="كلما كبر r", commande="play_until", parametres={"moment": "fin"}),
     dict(mot="كلما كبر r", cible="centre:0"),
     dict(mot="l'âge اللي حسبنا كبير بزاف", cible="centre:1")]),
]

FAC = [
  qcm_facile("fa_q1", "Plus facile : le nombre de désintégrations α", "نتمرنو بسؤال ساهل: شحال من alpha؟",
    "²³⁵₉₂U → ²⁰⁷₈₂Pb + x ⁰₋₁e + y ⁴₂He. La conservation de A donne…",
    ["y = 7", "y = 28", "y = 4"], 0, {
      "0": {"juste": rep("مزيان! deux cent trente-cinq moins deux cent sept، égale vingt-huit، et vingt-huit sur quatre، égale sept.", "Juste : 235 = 207 + 4y, donc y = 28/4 = 7.")},
      "1": {"1": rep("vingt-huit هو الفرق ديال A. ولكن كل alpha كتنقص A de quatre. عاود اختار.", "28 est la différence des A ; chaque α enlève 4 nucléons. Réessaie."),
            "2": rep("الجواب: y égale sept. vingt-huit sur quatre، حيت كل alpha عندها A égale quatre.", "Réponse : y = 28/4 = 7 (chaque α emporte 4 nucléons).")},
      "2": {"1": rep("quatre هو x، ديال bêta moins، ماشي y. شوف l'équation ديال A. عاود اختار.", "4 est x (les β⁻), trouvé avec Z. Pour y, utilise A. Réessaie."),
            "2": rep("الجواب: y égale sept، من l'équation ديال A: deux cent trente-cinq égale deux cent sept plus quatre y.", "Réponse : y = 7, d'après 235 = 207 + 4y.")}},
    "L'uranium deux cent trente-cinq donne le plomb deux cent sept, plus x électrons, plus y noyaux d'hélium. La conservation de A donne ?"),
  vf_facile("fa_q2", "Plus facile : les étapes de la démonstration", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.", "Père : uranium ; fils final : plomb.", [
      ("N_U(t) = N₀·e^(−λt) : le père suit la loi de décroissance.", True, "La loi décrit le noyau père, avec son λ et son N₀."),
      ("N_Pb = N₀ − N_U, car chaque uranium désintégré a donné un plomb.", True, "C'est la conservation du nombre de noyaux : restants + désintégrés = N₀."),
      ("N_Pb/N_U = e^(−λt).", False, "N_Pb/N_U = (1 − e^(−λt))/e^(−λt) = e^(λt) − 1.")]),
  qcm_facile("fa_q3", "Plus facile : le rapport des nombres de noyaux", "سؤال ساهل: اختار la bonne expression.",
    "N = (m/M)·N_A. Le rapport r = N_Pb/N_U vaut…",
    ["m_Pb/m_U", "(m_Pb/M_Pb)/(m_U/M_U)", "(m_Pb·M_Pb)/(m_U·M_U)"], 1, {
      "1": {"juste": rep("برافو! N A كيمشي، ولكن les masses molaires كيبقاو، حيت ماشي بحال بحال.", "Juste : N_A se simplifie, les masses molaires restent.")},
      "0": {"1": rep("قريب، ولكن نسيتي les masses molaires. M ديال le plomb ماشي M ديال l'uranium. عاود اختار.", "Tu as oublié les masses molaires, différentes. Réessaie."),
            "2": rep("الجواب: m Pb sur M Pb، sur m U sur M U. N A كيمشي، و M كيبقاو.", "Réponse : r = (m_Pb/M_Pb)/(m_U/M_U).")},
      "2": {"1": rep("N égale m sur M، ماشي m fois M. عاود اختار.", "N = (m/M)·N_A : on divise par M. Réessaie."),
            "2": rep("الجواب: m Pb sur M Pb، sur m U sur M U، حيت n égale m sur M.", "Réponse : r = (m_Pb/M_Pb)/(m_U/M_U) car n = m/M.")}},
    "N égale m sur M fois N A. Le rapport r égale N Pb sur N U vaut ?"),
  qcm_facile("fa_q4", "Plus facile : l'ordre de grandeur de l'âge", "سؤال ساهل: شحال تقريبا l'âge؟",
    "r ≈ 0,40 (moins de 1). L'âge de la roche est…",
    ["plus petit que t½", "entre t½ et 2t½", "plus grand que 2t½"], 0, {
      "0": {"juste": rep("مزيان! فt un demi، r égale un: plomb واحد مقابل uranium واحد. هنا r، plus petit que un، إذن ما وصلناش t un demi.", "Juste : à t = t½, r = 1 ; ici r < 1, donc t < t½.")},
      "1": {"1": rep("حسب r فt un demi: النص تفكك، إذن r égale un. واش r ديالنا كبر ولا صغر؟ عاود اختار.", "À t = t½, r = 1. Notre r est-il plus grand ou plus petit ? Réessaie."),
            "2": rep("الجواب: صغر من t un demi، حيت r، plus petit que un.", "Réponse : t < t½, car r < 1.")},
      "2": {"1": rep("à deux t un demi، كيبقى الربع، و r égale trois. عاود اختار.", "À 2t½, il reste le quart : r = 3. Réessaie."),
            "2": rep("الجواب: صغر من t un demi، حيت r، plus petit que un.", "Réponse : t < t½, car r < 1.")}},
    "r environ zéro virgule quarante, moins de un. L'âge de la roche est ?"),
  assoc_facile("fa_q5", "Plus facile : qui est qui ?", "سؤال ساهل: ربط كل grandeur مع المعنى ديالها.",
    "Dans la roche, aujourd'hui.", "Relie chaque grandeur à ce qu'elle représente.",
    [("1", "N_U"), ("2", "N_Pb"), ("3", "N_U + N_Pb")],
    [("a", "les noyaux d'uranium restants"), ("b", "les noyaux d'uranium désintégrés"), ("c", "les noyaux d'uranium à la formation, N₀")],
    {"1": "a", "2": "b", "3": "c"}, {
      "1-a": (True, "Juste : N_U compte l'uranium qui reste.", "صحيح: N U هوما l'uranium اللي باقي."),
      "1-b": (False, "Non : N_U est l'uranium encore présent, pas celui qui est parti.", "لا: N U هوما اللي باقيين، ماشي اللي مشاو."),
      "1-c": (False, "Non : N_U a diminué depuis la formation ; N₀ était plus grand.", "لا: N U نقص من الأول، N zéro كان كبر."),
      "2-a": (False, "Non : le plomb n'est plus de l'uranium ; chaque plomb vient d'un uranium désintégré.", "لا: le plomb ماشي uranium. كل plomb جا من uranium تفكك."),
      "2-b": (True, "Juste : chaque uranium désintégré a donné un plomb.", "صحيح: كل uranium تفكك عطا plomb واحد."),
      "2-c": (False, "Non : N_Pb ne compte que ceux qui se sont désintégrés.", "لا: N Pb كيحسب غير اللي تفككو."),
      "3-a": (False, "Non : la somme compte aussi les désintégrés.", "لا: المجموع فيه حتى اللي تفككو."),
      "3-b": (False, "Non : la somme compte aussi les restants.", "لا: المجموع فيه حتى اللي باقيين."),
      "3-c": (True, "Juste : restants + désintégrés = N₀.", "صحيح: les restants plus les désintégrés، égale N zéro.")},
    ("(1 ; a) (2 ; b) (3 ; c) : p = N_Pb/N₀ = r/(1 + r).", "le pourcentage: N Pb sur N zéro، يعني r sur un plus r.")),
  vf_facile("fa_q6", "Plus facile : le plomb initial", "سؤال ساهل: قول واش صحيحة ولا غالطة.", "La roche contenait déjà du plomb à sa formation.", [
      ("Le plomb mesuré aujourd'hui est plus grand que le plomb formé par l'uranium.", True, "Il contient en plus le plomb initial."),
      ("Avec ce plomb en trop, l'âge calculé est trop petit.", False, "r est trop grand, et t = (t½/ln 2)·ln(1 + r) croît avec r : l'âge est trop grand."),
      ("Plus le rapport r est grand, plus l'âge calculé est grand.", True, "ln est croissante : t croît avec r.")]),
]


def qb():
    P = EXB
    rs = f"{rB:.4f}".replace(".", ",")
    return [
      {"id": "1", "texte": f"L'équation bilan de la famille s'écrit : {eq_famille(P)}. Déterminer x et y en précisant les lois utilisées.",
       "reponse": phrase(att_famille(P, xB, yB)), "clavier": {"aides": ["conservation de A", "conservation de Z", "4y", "2y"], "pieges": ["232 = 208 + x + 4y"]},
       "correction": correction([(f"1 : A : 232 = 208 + 4y ⇒ y = {yB}", f"y égale {nfr(yB)}"), (f"Z : 90 = 82 − x + 2y ⇒ x = {xB}", f"x égale {nfr(xB)}"),
                                 (f"{yB} désintégrations α et {xB} désintégrations β⁻", "le bilan")],
            f"d'après les lois de Soddy: deux cent trente-deux égale deux cent huit plus quatre y، إذن y égale {nfr(yB)}. quatre-vingt-dix égale quatre-vingt-deux moins x plus deux y، إذن x égale {nfr(xB)}. le bilan: {nfr(yB)} alpha et {nfr(xB)} bêta moins.")},
      {"id": "2", "texte": "On note N_Th et N_Pb les nombres de noyaux de thorium 232 et de plomb 208 à la date t. Montrer que t = (t½/ln 2)·ln(1 + N_Pb/N_Th).",
       "reponse": phrase(DEMO.replace("N_U", "N_Th").replace("noyau d'uranium", "noyau de thorium")), "clavier": {"aides": ["N_Th = N₀·e^(−λt)", "N_Pb = N₀ − N_Th", "e^(λt)"], "pieges": ["N_Pb = N₀·e^(−λt)"]},
       "correction": correction([("2 : N_Pb = N₀ − N_Th = N₀(1 − e^(−λt)) ; N_Pb/N_Th = e^(λt) − 1", "exponentielle lambda t moins un"),
                                 ("t = (t½/ln 2)·ln(1 + N_Pb/N_Th)", "t égale t un demi sur ln deux")],
            "N Pb égale N zéro moins N Th. le rapport: exponentielle lambda t moins un. إذن t égale t un demi sur ln deux، fois ln de un plus N Pb sur N Th.")},
      {"id": "3", "texte": "À partir du document, calculer le rapport r = N_Pb/N_Th aujourd'hui.",
       "reponse": valeur("r", rB, "", f"r = (m_Pb/M_Pb)/(m_Th/M_Th) = (0,18/208)/(5,00/232) ≈ {rs}"),
       "clavier": {"aides": ["N = (m/M)·N_A", "N_A se simplifie"], "pieges": ["r = m_Pb/m_Th"]},
       "correction": correction([("3 : r = (m_Pb/M_Pb)/(m_Th/M_Th) = (0,18/208)/(5,00/232)", "r égale m Pb sur M Pb"), (f"r ≈ {rs}", "environ " + dn(rB, 4))],
            "r égale m Pb sur M Pb، sur m Th sur M Th. r égale environ " + dn(rB, 4) + ".")},
      {"id": "4", "texte": "Calculer l'âge t de la roche.",
       "reponse": valeur("t", tB, "ans", f"t = (1,40 × 10¹⁰/0,693) × ln(1 + {rs}) ≈ {sci(tB, 3)} ans"),
       "clavier": {"aides": ["t = (t½/ln 2)·ln(1 + r)", "ans"], "pieges": ["ln(r)"]},
       "correction": correction([("4 : t = (t½/ln 2)·ln(1 + r)", "t égale t un demi sur ln deux"), (f"t ≈ {sci(tB, 3)} ans", "environ " + ds(tB) + " ans")],
            "t égale t un demi sur ln deux، fois ln de un plus r. t égale environ " + ds(tB) + " ans.")},
      {"id": "5", "texte": "Calculer le pourcentage des noyaux de thorium 232 présents à la formation qui se sont désintégrés depuis.",
       "reponse": valeur("p", pB, "%", f"p = r/(1 + r) = {rs}/(1 + {rs}) ≈ {fr(pB, 2)} %"),
       "clavier": {"aides": ["N₀ = N_Th + N_Pb", "r/(1 + r)", "%"], "pieges": ["p = r"]},
       "correction": correction([("5 : p = N_Pb/(N_Th + N_Pb) = r/(1 + r)", "r sur un plus r"), (f"p ≈ {fr(pB, 2)} %", "environ " + dn(pB, 2) + " pour cent")],
            "p égale N Pb sur N zéro، يعني r sur un plus r، égale environ " + dn(pB, 2) + " pour cent.")},
      {"id": "6", "texte": "Une analyse plus fine montre qu'à sa formation la roche contenait déjà un peu de plomb 208. L'âge calculé est-il trop grand ou trop petit ? Justifier.",
       "reponse": phrase(CRIT.replace("plomb 207", "plomb 208").replace("de l'uranium", "du thorium")),
       "clavier": {"aides": ["r trop grand", "t croît avec r"], "pieges": ["trop petit"]},
       "correction": correction([("6 : plomb mesuré = plomb initial + plomb formé ⇒ r trop grand", "r كبير بزاف"), ("t croît avec r : l'âge est surestimé", "surestimé")],
            "le plomb اللي قسنا فيه حتى le plomb ديال البداية: r كبير بزاف، و t كيكبر مع r. إذن l'âge surestimé.")},
    ]


EX = {
  "id": "phys_ex_ch4_roche_6", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "radioactivite", "cours": "phys_ch4_radioactivite",
  "titre": "Dater une roche par la famille uranium 235 – plomb 207", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série).",
  "competences": ["Compter les désintégrations α et β⁻ d'une famille (lois de Soddy)", "Établir t = (t½/ln 2)·ln(1 + N_fils/N_père)",
                  "Calculer un rapport de nombres de noyaux à partir de masses", "Calculer l'âge d'une roche et un pourcentage désintégré",
                  "Critiquer une hypothèse de datation"],
  "enonce": {
    "intro": intro(EXA),
    "intro_dit": "دابا نقراو l'énoncé. بغينا نعرفو l'âge ديال zircon، بلورة من roche granitique. l'uranium deux cent trente-cinq، ب désintégrations alpha و bêta moins، يعني famille radioactive، كيولي le plomb deux cent sept، stable. les hypothèses: ملي تكونات la roche، ما كانش فيها le plomb deux cent sept. le plomb كامل جا من l'uranium. و les noyaux اللي فالوسط ديال la famille قلال بزاف. la figure كتعطي شنو فيها la roche اليوم.",
    "figures": [figure(EXA)],
    "donnees": donnees(EXA),
    "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXP}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FAC}]},
  "similaire": {"id": "phys_ex_ch4_roche_6_b", "titre": "Même exercice, autres données : la famille thorium 232 – plomb 208",
    "enonce": {"intro": intro(EXB),
               "intro_dit": "نفس التمرين، بقيم أخرى: le thorium deux cent trente-deux كيولي le plomb deux cent huit، stable، ب famille radioactive.",
               "figures": [figure(EXB)], "donnees": donnees(EXB), "questions": qb()}},
}

if __name__ == "__main__":
    ecrire(EX)
