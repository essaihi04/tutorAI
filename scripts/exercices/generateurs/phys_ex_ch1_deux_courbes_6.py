# Exercice de physique (ch. 1, ondes mécaniques progressives), niveau DIFFICILE (« Supérieur ») : une corde, deux documents.
# Sources comparées (skill exercices § 2) :
# - experience_profs.json « ondes_mecaniques » : cas types « photo » (t = d/v pour dater une photo ; t₁ inconnu),
#   « etat_vibratoire » (lire l'axe d'abord ; couper la bosse au sommet : côté front les points montent ; L = v·θ ;
#   date d'arrêt = date d'arrivée + θ), « dessiner_aspect » ; pièges « confond τ et θ », « appelle θ période et L
#   longueur d'onde », « lire un axe en cm comme en s, confondre aspect et élongation », « mesurer jusqu'à l'arrière
#   de l'onde », « se bloquer parce que t₁ n'est pas donné » ;
# - exploration ondes_mecaniques_periodiques.json (partie ch1) : cas « instant_photo », « retard_periodique »,
#   piège « confond la période T avec le retard τ ou la durée θ » ; a_ne_pas_dire « longueur d'onde d'une
#   perturbation isolée » (on dit longueur ℓ = v·θ) ;
# - nationaux comparés : 2022 R ex. 2 (y_M(t) d'un point de la surface de l'eau → N, τ, v = L/τ), 2017 N ex. II
#   (instant de la coupe t = SM/v), 2024 N ex. 2 (aspect daté), 2020 R/2018 N (oscillogrammes). Le nôtre : une
#   corde avec DEUX documents de la même perturbation (y(x) à une date t₁ NON donnée, y_M(t) d'un point M de
#   position NON donnée) : v ne sort que de leur combinaison (ℓ sur l'un, θ sur l'autre), puis « montrer que
#   t₁ = x_F·θ/ℓ », SM, la date de retour au repos de l'extrémité, le sens du mouvement de deux points et une
#   lecture critique (M au repos alors que la perturbation est encore sur la corde) : aucun national n'a cette chaîne ;
# - séries en ligne (talamidi séries 1 et 5, moutamadris, Jenkal, dreamjob) : repérées par recherche, lecture bloquée
#   par le réseau de la session (hôtes non résolus) ; rien n'a été recopié.
# Figures : même perturbation que corde.html (montée rapide sur 30 % de θ, descente lente), calculée ici.
# Simulation : ondes-tableau/corde.html (V = 1,0 m/s, θ = 0,4 s ; vue aspect à t = 1,1 s, M à 0,5 m ; vue retard,
# M à 0,8 m ; vue sens : A à 1,05 m monte, B à 0,85 m descend) : la voix décrit la simulation avec SES valeurs,
# puis « فالتمرين » applique celles de l'exercice.
import sys, os, re, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

_TP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "backend", "kaggle_tts", "texte_parle.py")
_sp = importlib.util.spec_from_file_location("tp", _TP); tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(tp)


def dire(x, dec=3):
    s = fr(x, dec)
    m = re.match(r"(\d+),(\d+)$", s)
    return tp._decimal_fr(m) if m else tp.nombre_fr(int(s))


SIM = "/media/simulations/physics/ondes-tableau/corde.html"
MONTEE = 0.3


def forme(u):
    if u < 0 or u > 1:
        return 0.0
    return math.sin(math.pi / 2 * u / MONTEE) if u < MONTEE else math.cos(math.pi / 2 * (u - MONTEE) / (1 - MONTEE))


def donnees(v, theta, t1, SM, SE, xN, xP, amp=2.0):
    D = dict(v=v, theta=theta, t1=t1, SM=SM, SE=SE, xN=xN, xP=xP, amp=amp)
    D["l"] = v * theta                    # longueur de la perturbation
    D["xF"] = v * t1                      # front à t₁
    D["xQ"] = D["xF"] - D["l"]            # queue à t₁
    D["xS"] = D["xF"] - MONTEE * D["l"]   # sommet à t₁
    D["tM"] = SM / v                      # M atteint
    D["tMr"] = D["tM"] + theta            # M revenu au repos
    D["tE"] = SE / v
    D["tR"] = D["tE"] + theta
    # contrôles de cohérence de la situation
    assert D["xS"] < xN < D["xF"] and D["xQ"] < xP < D["xS"]    # N monte, P descend
    assert D["tMr"] < t1 and SM < D["xQ"]                        # M au repos à t₁, derrière la perturbation
    assert D["xF"] < SE
    return D


A = donnees(2.5, 0.2, 0.8, 1.0, 3.0, 1.9, 1.6)
B = donnees(2.0, 0.3, 1.1, 0.8, 3.0, 2.1, 1.8)


def y_x(D, x):
    return D["amp"] * forme((D["t1"] - x / D["v"]) / D["theta"])


def y_t(D, t):
    return D["amp"] * forme((t - D["tM"]) / D["theta"])


def figures(D):
    n = 600
    pts1 = [[round(D["SE"] * i / n, 4), round(y_x(D, D["SE"] * i / n), 4)] for i in range(n + 1)]
    gx = [[round(0.1 * k, 1), fr(0.1 * k, 1) if k % 5 == 0 else ""] for k in range(0, 31)]
    tmax = 1.2
    pts2 = [[round(tmax * i / n, 4), round(y_t(D, tmax * i / n), 4)] for i in range(n + 1)]
    gt = [[round(0.05 * k, 2), fr(0.05 * k, 1) if k % 4 == 0 else ""] for k in range(0, 25)]
    gy = [[1, "1"], [2, "2"]]
    f1 = {"type": "courbe", "titre": "Document 1 : aspect de la corde à une date t₁", "ratio": 0.45,
          "axes": {"x": {"min": 0, "max": D["SE"], "nom": "x", "unite": "m", "graduations": gx},
                   "y": {"min": -0.5, "max": 3, "nom": "y", "unite": "cm", "graduations": gy}},
          "legende": "S est en x = 0 ; l'extrémité E est en x = " + fr(D["SE"]) + " m.",
          "elements": [{"f": "ligne", "pts": pts1, "couleur": "orange", "epais": True},
                       {"f": "point", "at": [D["xN"], round(y_x(D, D["xN"]), 3)], "t": "N", "pos": "ne", "couleur": "cyan"},
                       {"f": "point", "at": [D["xP"], round(y_x(D, D["xP"]), 3)], "t": "P", "pos": "no", "couleur": "cyan"},
                       {"f": "texte", "at": [0.12, 0.45], "t": "S", "couleur": "jaune"},
                       {"f": "texte", "at": [D["SE"] - 0.08, 0.45], "t": "E", "couleur": "jaune"}]}
    f2 = {"type": "courbe", "titre": "Document 2 : élongation y_M(t) d'un point M", "ratio": 0.45,
          "axes": {"x": {"min": 0, "max": tmax, "nom": "t", "unite": "s", "graduations": gt},
                   "y": {"min": -0.5, "max": 3, "nom": "y_M", "unite": "cm", "graduations": gy}},
          "legende": "La source S commence à bouger à la date t = 0.",
          "elements": [{"f": "ligne", "pts": pts2, "couleur": "vert", "epais": True}]}
    return [f1, f2]


def intro(D):
    return ("Une corde élastique SE, de longueur " + fr(D["SE"]) + " m, est tendue horizontalement. À la date t = 0, l'extrémité S "
            "commence une perturbation unique, qui se propage le long de la corde sans amortissement ni réflexion. "
            "Le document 1 représente l'aspect de la corde à une date t₁ qui n'est pas donnée. Le document 2 représente "
            "l'élongation y_M(t) d'un point M de la corde, dont la position n'est pas donnée. Les deux documents concernent "
            "la même perturbation. Les points N et P sont marqués sur le document 1.")


def donnees_txt(D):
    return ["Source S en x = 0 ; début de la perturbation à t = 0", f"Longueur de la corde : SE = {fr(D['SE'])} m",
            f"Abscisses à la date t₁ : x_N = {fr(D['xN'])} m ; x_P = {fr(D['xP'])} m"]


# ---------- attendus ----------
def att1(D):
    return f"θ = {fr(D['theta'])} s (doc. 2) ; ℓ = {fr(D['xF'])} − {fr(D['xQ'])} = {fr(D['l'])} m (doc. 1) ; v = ℓ/θ = {fr(D['l'])}/{fr(D['theta'])} = {fr(D['v'])} m/s"


def att2(D):
    return f"x_F = v·t₁ et v = ℓ/θ, donc t₁ = x_F/v = x_F·θ/ℓ = {fr(D['xF'])} × {fr(D['theta'])}/{fr(D['l'])} = {fr(D['t1'])} s"


def att3(D):
    return f"τ = t_M = {fr(D['tM'])} s (doc. 2) ; SM = v·τ = {fr(D['v'])} × {fr(D['tM'])} = {fr(D['SM'])} m"


def att4(D):
    return f"t_E = SE/v = {fr(D['SE'])}/{fr(D['v'])} = {fr(D['tE'])} s ; t_R = t_E + θ = {fr(D['tE'])} + {fr(D['theta'])} = {fr(D['tR'])} s"


def att5(D):
    return (f"Sur le document 1, le front est en x_F = {fr(D['xF'])} m et le sommet vers x = {fr(D['xS'])} m. "
            f"N (x = {fr(D['xN'])} m) est entre le sommet et le front : il n'a pas encore atteint le sommet, il monte. "
            f"P (x = {fr(D['xP'])} m) est entre la queue et le sommet : il a déjà passé le sommet, il descend.")


def att6(D):
    return (f"L'affirmation est fausse. M est atteint à t_M = {fr(D['tM'])} s et bouge pendant θ : il revient au repos à "
            f"t_M + θ = {fr(D['tMr'])} s < t₁ = {fr(D['t1'])} s. À t₁, la perturbation occupe la zone de {fr(D['xQ'])} m à {fr(D['xF'])} m ; "
            f"M (SM = {fr(D['SM'])} m) est derrière elle : il est au repos.")


# ---------- corrections ----------
def corr1(D):
    return correction([
        (f"1 : doc. 2 : θ = {fr(D['theta'])} s ; doc. 1 : ℓ = {fr(D['l'])} m", f"teta égale {dire(D['theta'])} seconde"),
        ("ℓ = v·θ donc v = ℓ/θ", "v égale L sur teta"),
        (f"v = {fr(D['l'])}/{fr(D['theta'])} = {fr(D['v'])} m/s", f"v égale {dire(D['v'])} mètres par seconde")],
        f"la question un. على le document deux، M كتتحرك من {'t M'} حتى ل t M plus teta: teta égale {dire(D['theta'])} seconde. "
        f"على le document un، la perturbation من la queue حتى ل le front: L égale {dire(D['l'])} mètre. "
        f"فla durée teta، le front كيقطع L. إذن L égale v fois teta، وv égale L sur teta، égale {dire(D['l'])} sur {dire(D['theta'])}. "
        f"v égale {dire(D['v'])} mètres par seconde.")


def corr2(D):
    return correction([
        ("2 : le front a parcouru x_F pendant t₁ : x_F = v·t₁", "x F égale v fois t un"),
        ("v = ℓ/θ, donc t₁ = x_F/v = x_F·θ/ℓ", "t un égale x F fois teta sur L"),
        (f"t₁ = {fr(D['xF'])} × {fr(D['theta'])}/{fr(D['l'])} = {fr(D['t1'])} s", f"t un égale {dire(D['t1'])} seconde")],
        "la question deux. من t égale zéro حتى t un، le front قطع x F. إذن x F égale v fois t un. "
        "وv égale L sur teta. إذن t un égale x F sur v، يعني t un égale x F fois teta sur L. "
        f"على le document un، x F égale {dire(D['xF'])} mètres. t un égale {dire(D['xF'])} fois {dire(D['theta'])}، sur {dire(D['l'])}. "
        f"t un égale {dire(D['t1'])} seconde.")


def corr3(D):
    return correction([
        (f"3 : M commence à bouger à t_M = {fr(D['tM'])} s : τ = {fr(D['tM'])} s", f"tau égale {dire(D['tM'])} seconde"),
        ("τ = SM/v, donc SM = v·τ", "SM égale v fois tau"),
        (f"SM = {fr(D['v'])} × {fr(D['tM'])} = {fr(D['SM'])} m", f"SM égale {dire(D['SM'])} mètre")],
        "la question trois. على le document deux، M كتبدا تتحرك فt M. la source بدات فt égale zéro، "
        f"إذن le retard tau égale {dire(D['tM'])} seconde. tau égale SM sur v، إذن SM égale v fois tau، "
        f"égale {dire(D['v'])} fois {dire(D['tM'])}. SM égale {dire(D['SM'])} mètre.")


def corr4(D):
    return correction([
        (f"4 : le front atteint E à t_E = SE/v = {fr(D['SE'])}/{fr(D['v'])} = {fr(D['tE'])} s", f"t E égale {dire(D['tE'])} seconde"),
        ("E bouge pendant θ : t_R = t_E + θ", "t R égale t E plus teta"),
        (f"t_R = {fr(D['tE'])} + {fr(D['theta'])} = {fr(D['tR'])} s", f"t R égale {dire(D['tR'])} seconde")],
        f"la question quatre. le front كيوصل ل E فt E égale SE sur v، égale {dire(D['SE'])} sur {dire(D['v'])}. "
        f"t E égale {dire(D['tE'])} seconde. من بعد، E كتتحرك la durée teta. إذن t R égale t E plus teta، "
        f"égale {dire(D['tE'])} plus {dire(D['theta'])}. t R égale {dire(D['tR'])} seconde.")


def corr5(D):
    return correction([
        (f"5 : à t₁, front en x = {fr(D['xF'])} m, sommet vers x = {fr(D['xS'])} m", "le front على اليمين"),
        ("N, entre le sommet et le front : il monte", "إذن N كطلع"),
        ("P, entre la queue et le sommet : il descend", "إذن P كتهبط")],
        "la question cinq. على le document un، le front على اليمين، والقمة قريبة منو. "
        "N بين القمة وle front: مازال ما وصلش للقمة، إذن N كطلع. "
        "P مور القمة: دازت عليه القمة، كيرجع للصفر، إذن P كتهبط.")


def corr6(D):
    return correction([
        (f"6 : M atteint à t_M = {fr(D['tM'])} s, au repos à t_M + θ = {fr(D['tMr'])} s", f"t M plus teta égale {dire(D['tMr'])} seconde"),
        (f"{fr(D['tMr'])} s < t₁ = {fr(D['t1'])} s : à t₁, M est au repos", "إذن فt un، M فالراحة"),
        (f"à t₁, la perturbation est entre {fr(D['xQ'])} m et {fr(D['xF'])} m : M est derrière elle", "M مور la perturbation"),
        ("L'affirmation est fausse.", "l'affirmation est fausse")],
        f"la question six. M كتبدا تتحرك فt M، وكتبقى la durée teta. t M plus teta égale {dire(D['tMr'])} seconde، "
        f"et t un égale {dire(D['t1'])} seconde. إذن فt un، M فالراحة. وعلى le document un، la perturbation entre {dire(D['xQ'])} et {dire(D['xF'])} mètres، "
        "وM مور la perturbation. إذن l'affirmation est fausse: la perturbation فوق la corde، ولكن ماشي فM.")


CL1 = {"aides": ["θ", "ℓ", "ℓ = v·θ", "A.N. :", "m/s"], "pieges": ["v = θ/ℓ", "v = ℓ·θ", "λ"]}
CL2 = {"aides": ["x_F = v·t₁", "v = ℓ/θ", "t₁ = x_F/v", "A.N. :", "s"], "pieges": ["t₁ = ℓ/v", "t₁ = θ"]}
CL3 = {"aides": ["τ", "t_M", "τ = SM/v", "A.N. :", "m"], "pieges": ["SM = τ/v", "SM = x_F"]}
CL4 = {"aides": ["t_E = SE/v", "+ θ", "A.N. :", "s"], "pieges": ["t_R = t_E − θ", "t_E = v/SE"]}
CL5 = {"aides": ["front", "sommet", "monte", "descend"], "pieges": ["N descend", "au repos"]}
CL6 = {"aides": ["t_M + θ", "t₁", "au repos", "queue"], "pieges": ["M bouge", "τ = θ"]}

Q = [
  {"id": "1", "texte": "En exploitant les deux documents, déterminer la durée θ et la longueur ℓ de la perturbation, puis en déduire la célérité v de l'onde.",
   "texte_dit": "la question un: باستعمال les deux documents، déterminer la durée teta وla longueur L ديال la perturbation، ومن بعد déduire la célérité v.",
   "reponse": valeur("v", A["v"], "m/s", att1(A)), "clavier": CL1,
   "aides": [aide("Regarde l'axe de chaque document : θ (une durée) se lit sur la courbe y_M(t), ℓ (une longueur) sur l'aspect y(x).",
                  "شوف l'axe ديال كل document. teta هي durée: كنقراوها على y de M en fonction de t. L هي longueur: كنقراوها على y en fonction de x."),
             aide("Pendant θ, le front avance de ℓ : ℓ = v·θ, donc v = ℓ/θ.",
                  "فla durée teta، le front كيقطع L. إذن L égale v fois teta، وv égale L sur teta.")],
   "correction": corr1(A), "explication": "ex_d1", "facile": "fa_d1"},
  {"id": "2", "texte": "Montrer que la date t₁ du document 1 s'écrit t₁ = x_F·θ/ℓ, où x_F est l'abscisse du front à t₁. Calculer t₁.",
   "texte_dit": "la question deux: بين بلي t un égale x F fois teta sur L، وx F هي l'abscisse ديال le front. ومن بعد calculer t un.",
   "reponse": valeur("t₁", A["t1"], "s", att2(A)), "clavier": CL2,
   "aides": [aide("Entre t = 0 et t₁, le front part de S et arrive en x_F : quelle relation lie x_F, v et t₁ ?",
                  "من t égale zéro حتى t un، le front خرج من S ووصل ل x F. شنو la relation بين x F وv وt un؟"),
             aide("x_F = v·t₁ ; remplace v par ℓ/θ, puis lis x_F sur le document 1 (le front est du côté de E).",
                  "x F égale v fois t un. عوض v ب L sur teta، وقرا x F على le document un: le front هو من جهة E.")],
   "correction": corr2(A), "explication": "ex_d2", "facile": "fa_d2"},
  {"id": "3", "texte": "Déterminer la distance SM.",
   "texte_dit": "la question trois: déterminer la distance SM.",
   "reponse": valeur("SM", A["SM"], "m", att3(A)), "clavier": CL3,
   "aides": [aide("Sur le document 2, à quelle date M commence-t-il à bouger ? La source, elle, a commencé à t = 0.",
                  "على le document deux، فوقاش M كتبدا تتحرك؟ la source بدات فt égale zéro."),
             aide("Cette date est le retard τ de M sur S, et τ = SM/v.",
                  "هاد la date هي le retard tau ديال M par rapport à S، وtau égale SM sur v.")],
   "correction": corr3(A), "explication": "ex_d3", "facile": "fa_d3"},
  {"id": "4", "texte": "Déterminer la date t_R à laquelle l'extrémité E de la corde revient définitivement au repos.",
   "texte_dit": "la question quatre: déterminer la date t R، فاش الطرف E ديال la corde كيرجع للراحة نهائيا.",
   "reponse": valeur("t_R", A["tR"], "s", att4(A)), "clavier": CL4,
   "aides": [aide("D'abord, à quelle date le front arrive-t-il en E ?",
                  "أولا، فوقاش le front كيوصل ل E؟"),
             aide("t_E = SE/v ; ensuite E bouge pendant la durée θ : t_R = t_E + θ.",
                  "t E égale SE sur v. من بعد، E كتتحرك la durée teta: t R égale t E plus teta.")],
   "correction": corr4(A), "explication": "ex_d4", "facile": "fa_d4"},
  {"id": "5", "texte": "À la date t₁, préciser le sens du mouvement (monte ou descend) des points N et P. Justifier.",
   "texte_dit": "la question cinq: فt un، واش N وP كيطلعو ولا كيهبطو؟ justifier.",
   "reponse": phrase(att5(A)), "clavier": CL5,
   "aides": [aide("Repère le front sur l'aspect (le côté où la perturbation va), puis le sommet.",
                  "لقا le front على l'aspect، من الجهة فين ماشية la perturbation، ومن بعد لقا القمة."),
             aide("Imagine la perturbation un peu plus loin vers E : un point devant le sommet va vers le sommet, un point derrière revient vers 0.",
                  "تخيل la perturbation مشات شوية لجهة E. النقطة اللي قدام القمة غادي توصل للقمة. واللي مورها غادي ترجع للصفر.")],
   "correction": corr5(A), "explication": "ex_d5", "facile": "fa_d5"},
  {"id": "6", "texte": "Un élève affirme : « À la date t₁, le point M est en mouvement, puisque la perturbation est encore sur la corde. » Critiquer cette affirmation.",
   "texte_dit": "la question six: واحد التلميذ قال: فt un، النقطة M كتتحرك، حيت la perturbation مازال فوق la corde. واش عندو الحق؟ critiquer.",
   "reponse": phrase(att6(A)), "clavier": CL6,
   "aides": [aide("M ne bouge que pendant θ à partir de t_M : jusqu'à quelle date ?",
                  "M كتتحرك غير la durée teta، من t M. حتى لفوقاش؟"),
             aide("Compare t_M + θ à t₁, et regarde où est la perturbation à t₁ sur le document 1 par rapport à M.",
                  "قارن t M plus teta مع t un. وشوف على le document un فين كاينة la perturbation، وفين كاينة M.")],
   "correction": corr6(A), "explication": "ex_d6", "facile": "fa_d6"},
]

# ---------- explication animée (corde.html : V = 1 m/s, θ = 0,4 s) ----------
M1 = ("فla simulation، عندنا les deux images. فوق، la corde: y en fonction de x، كنقراو عليها la longueur L. "
      "لتحت، النقطة M: y en fonction de t، كنقراو عليها la durée teta. "
      "شوف: la perturbation كاملة فوق la corde، L égale zéro virgule quatre mètre. "
      "ومن بعد، M كتتحرك ورجعات لبلاصتها: teta égale zéro virgule quatre seconde. "
      "فهاد la durée teta، le front كيقطع L. إذن L égale v fois teta، وv égale L sur teta. "
      "هنا v égale zéro virgule quatre sur zéro virgule quatre، donc un mètre par seconde. "
      f"فالتمرين، على le document un، la longueur égale {dire(A['l'])} mètre، وعلى le document deux، teta égale {dire(A['theta'])} seconde. "
      f"إذن v égale {dire(A['l'])} sur {dire(A['theta'])}، égale {dire(A['v'])} mètres par seconde.")
M2 = ("شوف l'aspect de la corde، y en fonction de x. le front هو أول نقطة بدات تتحرك، وهو على اليمين. "
      "le front خرج من S فt égale zéro، وقطع la distance x F فla durée t un. إذن x F égale v fois t un. "
      "وv égale L sur teta. إذن t un égale x F sur v، يعني t un égale x F fois teta sur L. "
      "فla simulation، le front à un virgule un mètre، وv égale un mètre par seconde، donc t égale un virgule un seconde: هادا هو اللي مكتوب فوق. "
      f"فالتمرين، x F égale {dire(A['xF'])} mètres. t un égale {dire(A['xF'])} fois {dire(A['theta'])}، sur {dire(A['l'])}، "
      f"égale {dire(A['t1'])} seconde.")
M3 = ("شوف النقطة M. la source كتبدا فt égale zéro. la perturbation كتوصل ل M من بعد: هادا هو le retard tau. "
      "لتحت، la courbe ديال M كتبدا فt M، وt M هو tau، حيت la source بدات à t égale zéro. "
      "فla simulation، SM égale zéro virgule huit mètre، وtau égale zéro virgule huit seconde. إذن SM égale v fois tau. "
      f"فالتمرين، على le document deux، M كتبدا تتحرك à t M égale {dire(A['tM'])} seconde. "
      f"SM égale {dire(A['v'])} fois {dire(A['tM'])}، égale {dire(A['SM'])} mètre.")
M4 = ("دابا نبعدو M حتى قريب من الطرف ديال la corde: x égale un virgule neuf mètre. "
      "la perturbation كتوصل ليها après un virgule neuf seconde، حيت t égale x sur v. "
      "ومن بعد، النقطة كتبقى كتتحرك la durée teta، وعاد كترجع للراحة. "
      "إذن الطرف E كيرجع للراحة فt R égale SE sur v، plus teta. "
      f"فالتمرين، SE égale {dire(A['SE'])} mètres. t E égale {dire(A['SE'])} sur {dire(A['v'])}، égale {dire(A['tE'])} seconde. "
      f"والراحة: t R égale {dire(A['tE'])} plus {dire(A['theta'])}، égale {dire(A['tR'])} seconde.")
M5 = ("شوف l'aspect de la corde. تخيل la perturbation مشات شوية على اليمين. "
      "النقطة A، قدام القمة، من جهة le front: غادي توصل للقمة، إذن كطلع. "
      "النقطة B، مور القمة: كترجع للصفر، إذن كتهبط. "
      f"فالتمرين، le front à {dire(A['xF'])} mètres، والقمة قريبة منو، à {dire(A['xS'])} mètre. "
      f"N، à {dire(A['xN'])} mètre، بين القمة وle front: إذن N كطلع. "
      f"P، à {dire(A['xP'])} mètre، مور القمة: إذن P كتهبط.")
M6 = ("شوف M. la perturbation كتوصل ليها فt M. M كتتحرك la durée teta، ومن بعد كترجع لبلاصتها فt M plus teta. "
      "فla simulation، M رجعات à zéro virgule neuf seconde. ولكن la perturbation مازال فوق la corde، كتمشي لقدام. "
      "إذن la perturbation فوق la corde، ماشي معناها M كتتحرك. "
      f"فالتمرين، M رجعات à t M plus teta، égale {dire(A['tM'])} plus {dire(A['theta'])}، égale {dire(A['tMr'])} seconde. "
      f"et t un égale {dire(A['t1'])} seconde: إذن فt un، M فالراحة. "
      f"وعلى le document un، la perturbation entre {dire(A['xQ'])} et {dire(A['xF'])} mètres، وM à {dire(A['SM'])} mètre، مورها.")

EXPL = [
  diapo_sim("ex_d1", "Question 1 : ℓ sur un document, θ sur l'autre", "ℓ se lit sur y(x), θ sur y_M(t) : v = ℓ/θ.",
            SIM + "?vue=longueur", "La longueur L sur la corde, la durée θ sur la courbe de M", M1,
            [("ℓ = v·θ ⇒ v = ℓ/θ", "وv égale L sur teta"), (f"v = {fr(A['l'])}/{fr(A['theta'])} = {fr(A['v'])} m/s", f"égale {dire(A['v'])} mètres par seconde")],
            [dict(mot="فla simulation، عندنا les deux images", commande="start"),
             dict(mot="la perturbation كاملة فوق la corde", commande="play_until", parametres={"moment": "toute_sur_corde"}),
             dict(mot="L égale zéro virgule quatre mètre", repere="longueur_l"),
             dict(mot="M كتتحرك ورجعات لبلاصتها", commande="play_until", parametres={"moment": "m_revenu"}),
             dict(mot="teta égale zéro virgule quatre seconde", repere="duree_theta"),
             dict(mot="وv égale L sur teta", cible="centre:0"),
             dict(mot=f"égale {dire(A['v'])} mètres par seconde", cible="centre:1")]),
  diapo_sim("ex_d2", "Question 2 : dater l'aspect", "Le front a parcouru x_F pendant t₁ : x_F = v·t₁.",
            SIM + "?vue=aspect", "L'aspect y(x) : le front est à droite", M2,
            [("x_F = v·t₁ et v = ℓ/θ ⇒ t₁ = x_F·θ/ℓ", "يعني t un égale x F fois teta sur L"),
             (f"t₁ = {fr(A['xF'])} × {fr(A['theta'])}/{fr(A['l'])} = {fr(A['t1'])} s", f"égale {dire(A['t1'])} seconde")],
            [dict(mot="شوف l'aspect de la corde", commande="start"),
             dict(mot="وهو على اليمين", commande="play_until", parametres={"moment": "fin"}),
             dict(mot="وهو على اليمين", repere="axe_x"),
             dict(mot="يعني t un égale x F fois teta sur L", cible="centre:0"),
             dict(mot=f"égale {dire(A['t1'])} seconde", cible="centre:1")]),
  diapo_sim("ex_d3", "Question 3 : le retard de M, lu sur y_M(t)", "La source part à t = 0 : M commence à bouger à t_M = τ, et SM = v·τ.",
            SIM + "?vue=retard", "S et M : la même courbe, décalée de τ", M3,
            [("τ = t_M ; SM = v·τ", "إذن SM égale v fois tau"),
             (f"SM = {fr(A['v'])} × {fr(A['tM'])} = {fr(A['SM'])} m", f"égale {dire(A['SM'])} mètre")],
            [dict(mot="شوف النقطة M", repere="point_m"),
             dict(mot="la source كتبدا", commande="start"),
             dict(mot="هادا هو le retard tau", commande="play_until", parametres={"moment": "m_atteint"}),
             dict(mot="هادا هو le retard tau", repere="retard_tau"),
             dict(mot="إذن SM égale v fois tau", cible="centre:0"),
             dict(mot=f"égale {dire(A['SM'])} mètre", cible="centre:1")]),
  diapo_sim("ex_d4", "Question 4 : quand l'extrémité revient-elle au repos ?", "Atteinte à SE/v, elle bouge encore pendant θ.",
            SIM + "?vue=retard", "Un point près du bout de la corde", M4,
            [("t_E = SE/v ; t_R = t_E + θ", "t R égale SE sur v، plus teta"),
             (f"t_R = {fr(A['tE'])} + {fr(A['theta'])} = {fr(A['tR'])} s", f"égale {dire(A['tR'])} seconde")],
            [dict(mot="دابا نبعدو M", commande="set_parameters", parametres={"x_m": 1.9}),
             dict(mot="دابا نبعدو M", repere="point_m"),
             dict(mot="la perturbation كتوصل ليها", commande="play_until", parametres={"moment": "m_atteint"}),
             dict(mot="كتبقى كتتحرك la durée teta", commande="play_until", parametres={"moment": "fin"}),
             dict(mot="t R égale SE sur v، plus teta", cible="centre:0"),
             dict(mot=f"égale {dire(A['tR'])} seconde", cible="centre:1")]),
  diapo_sim("ex_d5", "Question 5 : qui monte, qui descend ?", "Devant le sommet (côté front) : monte ; derrière : descend.",
            SIM + "?vue=sens", "Les flèches : le mouvement de chaque point", M5,
            [("devant le sommet : monte ; derrière : descend", "النقطة A، قدام القمة"),
             (f"N ({fr(A['xN'])} m) monte ; P ({fr(A['xP'])} m) descend", "إذن P كتهبط")],
            [dict(mot="شوف l'aspect de la corde", commande="start"),
             dict(mot="تخيل la perturbation", commande="play_until", parametres={"moment": "fin"}),
             dict(mot="النقطة A، قدام القمة", repere="point_a"),
             dict(mot="النقطة A، قدام القمة", cible="centre:0"),
             dict(mot="إذن P كتهبط", cible="centre:1")]),
  diapo_sim("ex_d6", "Question 6 : M au repos, la perturbation plus loin", "M bouge de t_M à t_M + θ, puis reste au repos.",
            SIM + "?vue=longueur&depart=source_monte", "M revient au repos ; la perturbation continue", M6,
            [("M au repos après t_M + θ", "كترجع لبلاصتها فt M plus teta"),
             (f"t_M + θ = {fr(A['tMr'])} s < t₁ = {fr(A['t1'])} s : M au repos", "إذن فt un، M فالراحة")],
            [dict(mot="la perturbation كتوصل ليها", commande="play_until", parametres={"moment": "m_atteint"}),
             dict(mot="la perturbation كتوصل ليها", repere="point_m"),
             dict(mot="كترجع لبلاصتها فt M plus teta", commande="play_until", parametres={"moment": "m_revenu"}),
             dict(mot="كترجع لبلاصتها فt M plus teta", cible="centre:0"),
             dict(mot="M رجعات à zéro virgule neuf seconde", repere="duree_theta"),
             dict(mot="ولكن la perturbation مازال فوق la corde", commande="play_until", parametres={"moment": "fin"}),
             dict(mot="ولكن la perturbation مازال فوق la corde", repere="longueur_l"),
             dict(mot="إذن فt un، M فالراحة", cible="centre:1")]),
]

# ---------- version facile ----------
l, th, v = A["l"], A["theta"], A["v"]
FAC = [
  qcm_facile("fa_d1", "Plus facile : la célérité", "سؤال ساهل: اختار la bonne célérité.",
             f"ℓ = {fr(l)} m (document 1) et θ = {fr(th)} s (document 2). La célérité vaut…",
             [f"v = ℓ·θ = {fr(l * th)} m/s", f"v = ℓ/θ = {fr(v)} m/s", f"v = θ/ℓ = {fr(th / l)} m/s"], 1, {
               "1": {"juste": rep(f"برافو! L égale v fois teta، إذن v égale L sur teta، égale {dire(v)} mètres par seconde.",
                                  f"Juste : v = ℓ/θ = {fr(l)}/{fr(th)} = {fr(v)} m/s.")},
               "0": {"1": rep("ما تقلقش. شوف l'unité: mètre fois seconde ماشي mètre par seconde. عاود اختار.",
                              "m × s ne donne pas des m/s. Réessaie."),
                     "2": rep(f"la réponse est {dire(v)} mètres par seconde. من L égale v fois teta، كنقسمو L على teta.",
                              f"Réponse : v = ℓ/θ = {fr(v)} m/s.")},
               "2": {"1": rep("قريب! ولكن قلبتي القسمة: la distance فوق، وla durée تحت. عاود اختار.",
                              "La fraction est inversée : distance sur durée. Réessaie."),
                     "2": rep(f"la réponse est {dire(v)} mètres par seconde: L sur teta، ماشي teta sur L.",
                              f"Réponse : v = ℓ/θ = {fr(v)} m/s.")}},
             f"L égale {dire(l)} mètre, et teta égale {dire(th)} seconde. La célérité vaut ?"),
  vf_facile("fa_d2", "Plus facile : dater l'aspect", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
            "Le document 1 est l'aspect de la corde à une date t₁.", [
              ("À t₁, le front est à la distance x_F = v·t₁ de la source.", True, "Le front part de S à t = 0 et avance à la célérité v."),
              ("On lit t₁ directement sur l'axe horizontal du document 1.", False, "L'axe du document 1 est une distance x (en m), pas un temps."),
              (f"Avec x_F = {fr(A['xF'])} m et v = {fr(v)} m/s : t₁ = {fr(A['t1'])} s.", True, f"t₁ = x_F/v = {fr(A['xF'])}/{fr(v)} = {fr(A['t1'])} s.")]),
  qcm_facile("fa_d3", "Plus facile : la distance SM", "سؤال ساهل: حسب SM.",
             f"M commence à bouger à t_M = {fr(A['tM'])} s ; v = {fr(v)} m/s. SM vaut…",
             [f"{fr(A['tM'] / v)} m", f"{fr(v / A['tM'])} m", f"{fr(A['SM'])} m"], 2, {
               "2": {"juste": rep(f"برافو! SM égale v fois tau، égale {dire(v)} fois {dire(A['tM'])}، donc {dire(A['SM'])} mètre.",
                                  f"Juste : SM = v·τ = {fr(v)} × {fr(A['tM'])} = {fr(A['SM'])} m.")},
               "0": {"1": rep("ما تقلقش. قسمتي tau par v. من tau égale SM sur v، كنخرجو SM. عاود اختار.",
                              "τ/v n'est pas une distance. Réessaie."),
                     "2": rep(f"la réponse est {dire(A['SM'])} mètre: SM égale v fois tau.",
                              f"Réponse : SM = v·τ = {fr(A['SM'])} m.")},
               "1": {"1": rep("قريب! ولكن v sur tau ماشي distance. عاود اختار.",
                              "v/τ n'est pas une distance. Réessaie."),
                     "2": rep(f"la réponse est {dire(A['SM'])} mètre: SM égale v fois tau.",
                              f"Réponse : SM = v·τ = {fr(A['SM'])} m.")}},
             f"M commence à bouger à t M égale {dire(A['tM'])} seconde, et v égale {dire(v)} mètres par seconde. SM vaut ?"),
  qcm_facile("fa_d4", "Plus facile : retour au repos", "سؤال ساهل: فوقاش E كترجع للراحة؟",
             f"Le front atteint E à t_E = {fr(A['tE'])} s ; θ = {fr(th)} s. E revient au repos à…",
             [f"{fr(A['tE'])} s", f"{fr(A['tR'])} s", f"{fr(A['tE'] - th)} s"], 1, {
               "1": {"juste": rep(f"برافو! E كتتحرك la durée teta، إذن t R égale t E plus teta، égale {dire(A['tR'])} seconde.",
                                  f"Juste : t_R = t_E + θ = {fr(A['tR'])} s.")},
               "0": {"1": rep("ما تقلقش. فt E، E كتبدا تتحرك، ماشي كتوقف. عاود اختار.",
                              "À t_E, E commence à bouger. Réessaie."),
                     "2": rep(f"la réponse est {dire(A['tR'])} seconde: E كتتحرك la durée teta من بعد t E.",
                              f"Réponse : t_R = t_E + θ = {fr(A['tR'])} s.")},
               "2": {"1": rep("قريب! ولكن الراحة كتجي من بعد، ماشي قبل t E. عاود اختار.",
                              "Le repos vient après t_E, pas avant. Réessaie."),
                     "2": rep(f"la réponse est {dire(A['tR'])} seconde: t E plus teta، ماشي moins.",
                              f"Réponse : t_R = t_E + θ = {fr(A['tR'])} s.")}},
             f"Le front atteint E à t E égale {dire(A['tE'])} seconde, et teta égale {dire(th)} seconde. E revient au repos à ?"),
  assoc_facile("fa_d5", "Plus facile : le mouvement des points", "سؤال ساهل: ربط كل نقطة مع الحركة ديالها فt un.",
               "Relie chaque point du document 1 à son mouvement à t₁.", "Relie chaque point à son mouvement à t₁.",
               [("1", f"N (x = {fr(A['xN'])} m), entre le sommet et le front"), ("2", f"P (x = {fr(A['xP'])} m), entre la queue et le sommet"),
                ("3", f"Q (x = {fr((A['xF'] + A['SE']) / 2)} m), après le front")],
               [("a", "monte"), ("b", "descend"), ("c", "au repos")],
               {"1": "a", "2": "b", "3": "c"},
               {"1-a": (True, "Oui : devant le sommet, N va vers le sommet : il monte.", "صحيح: N قدام القمة، غادي توصل ليها، إذن كطلع."),
                "1-b": (False, "N est devant le sommet, côté front : le sommet n'est pas encore passé.", "N قدام القمة، مازال ما دازتش عليه."),
                "1-c": (False, "N est dans la perturbation : il bouge.", "N داخل la perturbation، إذن كيتحرك."),
                "2-a": (False, "P est derrière le sommet : le sommet est déjà passé.", "P مور القمة، دازت عليه القمة."),
                "2-b": (True, "Oui : derrière le sommet, P revient vers 0 : il descend.", "صحيح: P مور القمة، كيرجع للصفر، إذن كتهبط."),
                "2-c": (False, "P est encore dans la perturbation : il bouge.", "P مازال داخل la perturbation، إذن كيتحرك."),
                "3-a": (False, "Après le front, la perturbation n'est pas encore arrivée.", "مور le front، la perturbation مازال ما وصلات."),
                "3-b": (False, "Après le front, rien n'a encore bougé.", "مور le front، حتى حاجة ما تحركات."),
                "3-c": (True, "Oui : la perturbation n'est pas encore arrivée en Q.", "صحيح: la perturbation مازال ما وصلات ل Q.")},
               ("Couples : (1 ; a) (2 ; b) (3 ; c).", "N كطلع، P كتهبط، وQ فالراحة.")),
  vf_facile("fa_d6", "Plus facile : M au repos ?", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
            f"M est atteint à t_M = {fr(A['tM'])} s ; θ = {fr(th)} s ; t₁ = {fr(A['t1'])} s.", [
              (f"M revient au repos à t_M + θ = {fr(A['tMr'])} s.", True, "M bouge seulement pendant θ à partir de t_M."),
              ("À t₁, M bouge, puisque la perturbation est sur la corde.", False, f"À t₁ = {fr(A['t1'])} s > {fr(A['tMr'])} s, M est déjà revenu au repos."),
              (f"À t₁, la perturbation occupe la zone de {fr(A['xQ'])} m à {fr(A['xF'])} m.", True, "De la queue (x_F − ℓ) au front (x_F).")]),
]

SQ = [
  {"id": "1", "texte": Q[0]["texte"], "reponse": valeur("v", B["v"], "m/s", att1(B)), "clavier": CL1, "correction": corr1(B)},
  {"id": "2", "texte": Q[1]["texte"], "reponse": valeur("t₁", B["t1"], "s", att2(B)), "clavier": CL2, "correction": corr2(B)},
  {"id": "3", "texte": Q[2]["texte"], "reponse": valeur("SM", B["SM"], "m", att3(B)), "clavier": CL3, "correction": corr3(B)},
  {"id": "4", "texte": Q[3]["texte"], "reponse": valeur("t_R", B["tR"], "s", att4(B)), "clavier": CL4, "correction": corr4(B)},
  {"id": "5", "texte": Q[4]["texte"], "reponse": phrase(att5(B)), "clavier": CL5, "correction": corr5(B)},
  {"id": "6", "texte": Q[5]["texte"], "reponse": phrase(att6(B)), "clavier": CL6, "correction": corr6(B)},
]

EX = {
  "id": "phys_ex_ch1_deux_courbes_6", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques", "cours": "phys_ch1_waves_exemple",
  "titre": "Une corde, deux documents", "niveau": "difficile", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série).",
  "competences": ["Distinguer l'aspect y(x) et l'élongation y_M(t), et lire ℓ, θ, τ", "Combiner ℓ = v·θ, x_F = v·t et τ = SM/v",
                  "Dater le mouvement d'un point (t_M, t_M + θ)", "Trouver le sens du mouvement d'un point sur l'aspect"],
  "enonce": {
    "intro": intro(A),
    "intro_dit": ("دابا نقراو l'énoncé. عندنا une corde élastique SE، "
                  f"la longueur égale {dire(A['SE'])} mètres، ممدودة أفقيا. فt égale zéro، الطرف S كيدير une perturbation وحدة، "
                  "وكتمشي فla corde بلا ما تضعاف. le document un كيبين l'aspect de la corde فواحد la date t un، "
                  "وهاد la date ما معطياش. le document deux كيبين l'élongation ديال واحد النقطة M، y de M en fonction de t، "
                  "والبلاصة ديال M ما معطياش. رد البال: les deux documents، ولكن نفس la perturbation. "
                  "وعلى le document un، كاينين les points N et P."),
    "figures": figures(A), "donnees": donnees_txt(A), "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPL}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FAC}]},
  "similaire": {"id": "phys_ex_ch1_deux_courbes_6_b", "titre": "Même exercice, autres données",
    "enonce": {"intro": intro(B),
               "intro_dit": ("نفس التمرين، بقيم أخرى. une corde SE، "
                             f"la longueur égale {dire(B['SE'])} mètres. les deux documents ديال نفس la perturbation: "
                             "l'aspect فt un، وy de M en fonction de t."),
               "figures": figures(B), "donnees": donnees_txt(B), "questions": SQ}},
}

_NB = set("deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize vingt trente quarante cinquante soixante cent cents mille zéro quatre-vingts".split())
_AR = re.compile(r"[؀-ۿ]")


def controle_voix(o, k=""):
    pb = []
    if isinstance(o, dict):
        for kk, vv in o.items():
            pb += controle_voix(vv, kk)
    elif isinstance(o, list):
        for vv in o:
            pb += controle_voix(vv, k)
    elif isinstance(o, str) and k in {"mixed", "dit", "parole", "intro_dit", "texte_dit", "enonce_dit", "mot"}:
        if re.search(r"\d", o):
            pb.append(("chiffre", o[:60]))
        mots = o.split()
        for a, b in zip(mots, mots[1:]):
            if _AR.search(a) and not re.search(r"[،,.;!?؟]$", a) and b.strip("،,.:;!?؟").split("-")[0] in _NB:
                pb.append(("darija+nombre", a + " " + b))
    return pb


_pb = controle_voix(EX)
assert not _pb, _pb
ecrire(EX)
