# Exercice de physique (ch. 1, ondes mécaniques progressives), niveau moyen : l'aspect d'une corde à une date.
# Sources comparées (skill exercices § 2) :
#  - exploration ondes_mecaniques_periodiques.json (partie ch1 : pièges « lire un axe en distance comme un axe en temps »,
#    « confond T, τ et θ », « mesurer jusqu'à l'arrière de l'onde ») et experience_profs.json « ondes_mecaniques »
#    (cas types « état vibratoire » : couper la bosse au sommet, côté front les points montent, de l'autre ils
#    descendent ; L = v·θ ; date d'arrêt = arrivée + θ ; « dessiner l'aspect » : recopier y_S(t) renversée, le début
#    du mouvement au front ; « photo » : distance jusqu'au front).
#  - Nationaux comparés : aucun national PC 2016–2025 du dépôt ne porte sur l'aspect d'une corde à une perturbation
#    unique ; les plus proches sont 2024 N ex. 2 (fronts sur l'eau, v puis une date), 2022 R ex. 2 (courbe y_M(t),
#    lecture du retard) et 2017 N ex. II Q3 (instant d'une coupe, onde périodique). Ici : une seule perturbation
#    dissymétrique sur une corde, lecture du front et de L sur y(x), sens de deux points, dates de M, allure de y_M(t).
#    L'exercice pilote phys_ex_ch1_corde_1 (v = SP/t₁, τ = SM/v, ℓ = v·θ avec v = 1 m/s, θ = 0,4 s) n'est pas repris :
#    autres données (v = 2 m/s, θ = 0,15 s), sens inverse (θ = L/v), et trois questions de lecture qu'il n'a pas.
#  - Séries en ligne : recherche faite (moutamadris « aspect de la corde à différents instants », cours Bendaoud
#    « aspect à t et t + θ », talamidi série 1, alloschool « notion de retard ») ; lecture des PDF bloquée par le réseau
#    de la session (talamidi.com, moutamadris.ma, alloschool.com non résolus).
#  - Simulation : corde.html (V = 1,0 m/s, θ = 0,4 s ; vues front, longueur, sens, aspect) : la voix décrit d'abord la
#    simulation avec SES valeurs, puis dit « فالتمرين » et applique celles de l'exercice. La figure est calculée avec la
#    forme de corde.html (montée rapide sur 30 % de θ, descente lente), comme aspect() dans le pilote.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

# ---------- les nombres en mots (voix) ----------
_U = "zéro un deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize dix-sept dix-huit dix-neuf".split()
_D = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def _ent(n):
    if n < 20: return _U[n]
    if n < 70:
        d, u = divmod(n, 10)
        return _D[d] + ("" if u == 0 else " et un" if u == 1 else "-" + _U[u])
    if n < 80: return "soixante" + (" et onze" if n == 71 else "-" + _U[n - 60])
    if n < 100:
        u = n - 80
        return "quatre-vingt" + ("s" if u == 0 else "-" + _U[u])
    if n < 1000:
        c, r = divmod(n, 100)
        t = ("cent" if c == 1 else _U[c] + " cent" + ("s" if r == 0 else ""))
        return t + ("" if r == 0 else " " + _ent(r))
    m, r = divmod(n, 1000)
    t = "mille" if m == 1 else _ent(m) + " mille"
    return t + ("" if r == 0 else " " + _ent(r))


def mots(x, decimales=3):
    s = fr(x, decimales).replace("−", "-")
    neg = s.startswith("-"); s = s.lstrip("-")
    e, _, d = s.partition(",")
    t = _ent(int(e))
    if d:
        z = len(d) - len(d.lstrip("0"))
        t += " virgule " + " ".join(["zéro"] * z + ([_ent(int(d))] if d.strip("0") else []))
    return ("moins " if neg else "") + t

SIM = "/media/simulations/physics/ondes-tableau/corde.html"
MONTEE = 0.3


def forme(u):
    if u < 0 or u > 1: return 0.0
    return math.sin(math.pi / 2 * u / MONTEE) if u < MONTEE else math.cos(math.pi / 2 * (u - MONTEE) / (1 - MONTEE))


def y(x, t, v, theta, a):
    return a * forme((t - x / v) / theta)


def sens(x, t, v, theta):
    """+1 monte, −1 descend, 0 au repos (même règle que vy() de corde.html)."""
    e = 1e-4
    d = forme((t + e - x / v) / theta) - forme((t - e - x / v) / theta)
    return 0 if abs(d) < 1e-9 else (1 if d > 0 else -1)


def figure_aspect(v, theta, a, t1, xA, xB, xM, longueur=2.0):
    pts = [[round(longueur * i / 400, 4), round(y(longueur * i / 400, t1, v, theta, a), 4)] for i in range(401)]
    return {"type": "courbe", "titre": f"Aspect de la corde à la date t₁ = {fr(t1)} s",
            "legende": "La source S est en x = 0 ; elle a commencé à bouger à t = 0. Le sens de propagation est celui des x croissants.",
            "axes": {"x": {"min": 0, "max": longueur, "nom": "x", "unite": "m",
                           "graduations": [round(0.2 * k, 1) for k in range(1, int(longueur / 0.2) + 1)]},
                     "y": {"min": -0.4 * a, "max": 1.4 * a, "nom": "y", "unite": "cm", "graduations": [a]}},
            "elements": [
                {"f": "ligne", "pts": pts, "couleur": "orange", "epais": True},
                {"f": "point", "at": [0, 0], "t": "S", "pos": "so", "couleur": "cyan"},
                {"f": "point", "at": [xA, round(y(xA, t1, v, theta, a), 3)], "t": "A", "pos": "ne", "couleur": "jaune"},
                {"f": "point", "at": [xB, round(y(xB, t1, v, theta, a), 3)], "t": "B", "pos": "no", "couleur": "jaune"},
                {"f": "point", "at": [xM, 0], "t": "M", "pos": "n", "couleur": "vert"},
                {"f": "fleche", "de": [0.3, 1.2 * a], "a": [0.7, 1.2 * a], "texte": "sens de propagation", "couleur": "blanc", "pos": "n"}]}


def calculs(v, theta, t1, xM):
    xF = v * t1                      # front, lu sur la figure
    L = v * theta                    # longueur, lue sur la figure (de la queue au front)
    vv = xF / t1
    th = L / vv
    tM = xM / vv
    return xF, L, vv, th, tM, tM + th


# ---------- données ----------
V, TH, A, T1 = 2.0, 0.15, 2, 0.6
XA, XB, XM = 1.16, 1.0, 1.6
XF, L, VV, THc, TM, TF = calculs(V, TH, T1, XM)
XQ = XF - L
XS = V * (T1 - MONTEE * TH)            # le sommet
assert abs(VV - 2) < 1e-12 and abs(THc - 0.15) < 1e-12 and abs(TM - 0.8) < 1e-12 and abs(TF - 0.95) < 1e-12
assert XS < XA < XF and XQ < XB < XS and XM > XF
assert sens(XA, T1, V, TH) == 1 and sens(XB, T1, V, TH) == -1 and sens(XM, T1, V, TH) == 0
TSOM = TM + MONTEE * THc                # M au plus haut

# ---------- similaire ----------
Vb, THb, Ab, T1b = 1.5, 0.2, 2, 0.8
XAb, XBb, XMb = 1.16, 1.0, 1.8
XFb, Lb, VVb, THcb, TMb, TFb = calculs(Vb, THb, T1b, XMb)
XQb = XFb - Lb
XSb = Vb * (T1b - MONTEE * THb)
assert XSb < XAb < XFb and XQb < XBb < XSb and abs(TFb - 1.4) < 1e-12
assert sens(XAb, T1b, Vb, THb) == 1 and sens(XBb, T1b, Vb, THb) == -1
TSOMb = TMb + MONTEE * THcb

REP3 = ("A est entre le sommet et le front : il va prendre la place du sommet, il monte. "
        "B est derrière le sommet, du côté de S : il revient vers sa position de repos, il descend.")
REP5 = (f"y_M(t) = 0 jusqu'à t_M = {fr(TM)} s ; puis M monte rapidement jusqu'au sommet (à {fr(TSOM, 3)} s), "
        f"redescend lentement jusqu'à {fr(TF)} s, puis reste au repos. La montée raide, à droite sur l'aspect y(x) (côté front), "
        f"est à gauche sur la courbe y_M(t) : la forme est renversée.")

EX = {
  "id": "phys_ex_ch1_aspect_4", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques", "cours": "phys_ch1_waves_exemple",
  "titre": "L'aspect d'une corde à une date", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Lire la position du front sur l'aspect y(x) et en déduire v",
                  "Lire la longueur L de la perturbation et en déduire sa durée θ = L/v",
                  "Trouver le sens du mouvement d'un point sur l'aspect",
                  "Dater le début et la fin du mouvement d'un point : t_M = SM/v, t_M + θ",
                  "Passer de l'aspect y(x) à l'élongation y_M(t) : forme renversée"],
  "enonce": {
    "intro": (f"Une longue corde élastique est tendue horizontalement. À la date t = 0, on provoque au bout S (x = 0) une seule "
              f"perturbation de durée θ : S monte rapidement, puis redescend plus lentement à sa position de repos. La perturbation "
              f"se propage sans amortissement. La figure représente l'aspect de la corde à la date t₁ = {fr(T1)} s. "
              f"A et B sont deux points de la corde ; M est le point d'abscisse x_M = {fr(XM)} m."),
    "intro_dit": (f"دابا نقراو l'énoncé. une corde طويلة، ممدودة أفقيا. فt égale zéro، كنديرو فالطرف S واحد la perturbation وحدة، "
                  f"المدة ديالها teta: S كطلع بالزربة، ومن بعد كتهبط بشوية حتى ترجع لبلاصتها. la perturbation كتمشي بلا ما تضعاف. "
                  f"la figure كتبين l'aspect de la corde فt un égale {mots(T1)} seconde. "
                  f"A وB جوج نقط فوق la corde، وM هي النقطة اللي عندها x M égale {mots(XM)} mètre."),
    "figures": [figure_aspect(V, TH, A, T1, XA, XB, XM)],
    "donnees": [f"t₁ = {fr(T1)} s", f"x_M = SM = {fr(XM)} m", "Graduations de l'axe x : 0,2 m"],
    "questions": [
      {"id": "1", "texte": "Lire sur la figure l'abscisse x_F du front de l'onde à la date t₁, puis en déduire la célérité v.",
       "texte_dit": "la question un: اقرا على la figure l'abscisse x F ديال le front فt un، ومن بعد استنتج la célérité v.",
       "reponse": valeur("v", VV, "m/s", f"x_F = {fr(XF)} m ; v = x_F/t₁ = {fr(XF)}/{fr(T1)} = {fr(VV)} m/s"),
       "clavier": {"aides": ["v = d/Δt", "x_F", "t₁", "m/s", "A.N. :"],
                   "pieges": ["x_F = abscisse du sommet", "v = t₁/x_F"]},
       "aides": [
         aide("Le front est le point le plus loin de S qui a commencé à bouger : au-delà, la corde est encore au repos. Lis son abscisse.",
              "le front هو أبعد نقطة على S بدات تتحرك. من موراه، la corde مازال فالراحة. اقرا l'abscisse ديالو، ماشي ديال القمة."),
         aide("Le front est parti de S à t = 0 et a parcouru x_F pendant t₁ : v = x_F/t₁.",
              "le front خرج من S فt égale zéro، وقطع x F فla durée t un. إذن v égale x F sur t un.")],
       "correction": correction([
           (f"1 : sur la figure, le front est en x_F = {fr(XF)} m", "le front كاين ف x F"),
           ("Il a parcouru x_F depuis S pendant t₁ : v = x_F/t₁", "v égale x F sur t un"),
           (f"v = {fr(XF)}/{fr(T1)} = {fr(VV)} m/s", f"v égale {mots(VV)} mètres par seconde")],
           f"la question un. على la figure، le front كاين ف x F égale {mots(XF)} mètre. le front خرج من S فt égale zéro، "
           f"إذن v égale x F sur t un، c'est-à-dire {mots(XF)} sur {mots(T1)}. v égale {mots(VV)} mètres par seconde."),
       "explication": "ex_a1", "facile": "fa_a1"},
      {"id": "2", "texte": "Lire sur la figure la longueur L de la perturbation, puis en déduire sa durée θ.",
       "texte_dit": "la question deux: اقرا على la figure la longueur L ديال la perturbation، ومن بعد استنتج la durée teta.",
       "reponse": valeur("θ", THc, "s", f"L = {fr(XF)} − {fr(XQ)} = {fr(L)} m ; θ = L/v = {fr(L)}/{fr(VV)} = {fr(THc)} s"),
       "clavier": {"aides": ["L = v·θ", "θ = L/v", "front", "A.N. :"],
                   "pieges": ["θ = v/L", f"L = x_F"]},
       "aides": [
         aide("La perturbation va du dernier point en mouvement (côté S) jusqu'au front. Lis les deux abscisses.",
              "la perturbation كتبدا من آخر نقطة كتتحرك، من جهة S، حتى ل le front. اقرا les deux abscisses."),
         aide("Pendant θ, le front avance de L : L = v·θ, donc θ = L/v.",
              "فla durée teta، le front كيقطع L. إذن L égale v fois teta، وteta égale L sur v.")],
       "correction": correction([
           (f"2 : la perturbation va de x = {fr(XQ)} m à x_F = {fr(XF)} m : L = {fr(L)} m", "la perturbation كتبدا من"),
           ("L = v·θ, donc θ = L/v", "teta égale L sur v"),
           (f"θ = {fr(L)}/{fr(VV)} = {fr(THc)} s", f"teta égale {mots(THc)} seconde")],
           f"la question deux. la perturbation كتبدا من x égale {mots(XQ)} mètre، حتى ل le front، à {mots(XF)} mètre. "
           f"إذن L égale {mots(L)} mètre. وL égale v fois teta، إذن teta égale L sur v، c'est-à-dire {mots(L)} sur {mots(VV)}. "
           f"teta égale {mots(THc)} seconde."),
       "explication": "ex_a2", "facile": "fa_a2"},
      {"id": "3", "texte": "Préciser, en justifiant, le sens du mouvement (monte ou descend) des points A et B à la date t₁.",
       "texte_dit": "la question trois: قول، مع justifier، واش النقطة A كطلع ولا كتهبط فt un، ونفس الشي للنقطة B.",
       "reponse": phrase(REP3),
       "clavier": {"aides": ["sommet", "front", "monte", "descend"], "pieges": ["A et B montent tous les deux", "B monte car il est haut"]},
       "aides": [
         aide("Coupe la bosse à son sommet. Quel point est du côté du front ? Lequel est du côté de S ?",
              "قسم la perturbation فالقمة. شكون من جهة le front؟ وشكون من جهة S؟"),
         aide("Imagine la perturbation déplacée un petit peu vers la droite : le point devant le sommet prend sa place (il monte), le point derrière revient vers le repos (il descend).",
              "تخيل la perturbation مشات شوية على اليمين. النقطة اللي قدام القمة غادي توصل للقمة: كطلع. واللي مور القمة غادي ترجع للصفر: كتهبط.")],
       "correction": correction([
           ("3 : la perturbation avance vers les x croissants.", "la perturbation كتمشي على اليمين"),
           ("A est entre le sommet et le front : il va atteindre le sommet, donc A monte.", "إذن A كطلع"),
           ("B est derrière le sommet : il revient vers le repos, donc B descend.", "إذن B كتهبط")],
           "la question trois. la perturbation كتمشي على اليمين. A بين القمة وle front: من بعد شوية، القمة غادي توصل ليها. إذن A كطلع. "
           "B مور القمة، من جهة S: غادي ترجع لبلاصتها. إذن B كتهبط."),
       "explication": "ex_a3", "facile": "fa_a3"},
      {"id": "4", "texte": "Déterminer la date t_M à laquelle le point M commence à bouger, puis la date t'_M à laquelle il revient au repos.",
       "texte_dit": "la question quatre: حدد اللحظة t M اللي كتبدا فيها النقطة M تتحرك، ومن بعد اللحظة t M prime اللي كترجع فيها للراحة.",
       "reponse": valeur("t'_M", TF, "s", f"t_M = SM/v = {fr(XM)}/{fr(VV)} = {fr(TM)} s ; t'_M = t_M + θ = {fr(TM)} + {fr(THc)} = {fr(TF)} s"),
       "clavier": {"aides": ["t_M = SM/v", "t_M + θ", "θ", "s", "A.N. :"],
                   "pieges": ["t'_M = t_M + L", "t_M = SM·v"]},
       "aides": [
         aide("M commence à bouger quand le front arrive en M ; il bouge ensuite pendant toute la durée de la perturbation.",
              "M كتبدا تتحرك ملي كيوصلها le front. ومن بعد كتبقى كتتحرك المدة ديال la perturbation كاملة."),
         aide("t_M = SM/v (la source a démarré à t = 0) ; M revient au repos à t_M + θ.",
              "t M égale SM sur v، حيت la source بدات فt égale zéro. وM كترجع للراحة فt M plus teta.")],
       "correction": correction([
           ("4 : le front arrive en M à t_M = SM/v", "t M égale SM sur v"),
           (f"t_M = {fr(XM)}/{fr(VV)} = {fr(TM)} s", f"t M égale {mots(TM)} seconde"),
           (f"M bouge pendant θ : t'_M = t_M + θ = {fr(TM)} + {fr(THc)} = {fr(TF)} s", f"t M prime égale {mots(TF)} seconde")],
           f"la question quatre. le front كيوصل ل M فt M égale SM sur v، c'est-à-dire {mots(XM)} sur {mots(VV)}. t M égale {mots(TM)} seconde. "
           f"من بعد، M كتبقى كتتحرك teta. إذن t M prime égale t M plus teta، c'est-à-dire {mots(TM)} plus {mots(THc)}. "
           f"t M prime égale {mots(TF)} seconde."),
       "explication": "ex_a4", "facile": "fa_a4"},
      {"id": "5", "texte": "Décrire l'allure de la courbe y_M(t), élongation du point M en fonction du temps, en la comparant à l'aspect de la corde.",
       "texte_dit": "la question cinq: وصف la courbe y de M en fonction de t، وقارنها مع l'aspect de la corde.",
       "reponse": phrase(REP5),
       "clavier": {"aides": ["t_M", "t_M + θ", "montée rapide", "descente lente", "renversée"],
                   "pieges": ["même forme que l'aspect, front à droite", "y_M(t) commence à t = 0"]},
       "aides": [
         aide("M refait le mouvement de S avec un retard : comment S a-t-il bougé (vite ou lentement en montant) ? Entre quelles dates M bouge-t-il ?",
              "M كدير نفس الحركة ديال S، ولكن من بعد. S كيفاش تحركات: طلعات بالزربة ولا بشوية؟ وM بين أشمن لحظات كتتحرك؟"),
         aide("Sur y(x), le front (début du mouvement) est à droite ; sur y_M(t), le début du mouvement est la plus petite date, à gauche : la forme est renversée.",
              "فy en fonction de x، le front على اليمين. وفy en fonction de t، البداية ديال الحركة هي أصغر لحظة، على اليسار. إذن la forme مقلوبة.")],
       "correction": correction([
           (f"5 : y_M(t) = 0 pour t < {fr(TM)} s : M n'est pas encore atteint", "M مازال ما وصلاتهاش"),
           (f"de {fr(TM)} s à {fr(TF)} s : montée rapide jusqu'au sommet, puis descente lente ; ensuite y_M = 0", "كطلع بالزربة"),
           ("La montée raide est à droite sur y(x) (côté front) et à gauche sur y_M(t) : forme renversée.", "la forme مقلوبة")],
           f"la question cinq. قبل t M، M مازال ما وصلاتهاش la perturbation: y de M égale zéro. "
           f"من t M حتى ل t M prime، M كطلع بالزربة حتى للقمة، ومن بعد كتهبط بشوية، بحال S. ومن بعد كتبقى فالراحة. "
           f"فl'aspect، الطلعة القاصحة على اليمين، من جهة le front. وفy de M en fonction de t، على اليسار، حيت هي اللول. إذن la forme مقلوبة."),
       "explication": "ex_a5", "facile": "fa_a5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    diapo_sim("ex_a1", "Question 1 : le front, puis la célérité",
      "Le front est parti de S à t = 0 : v = x_F/t₁.",
      SIM + "?vue=front", "Deux photos de la corde : on mesure de front à front",
      "شوف la corde فالتجربة. le front كيتقدم، وكل photo كتورينا فين وصل. ديما كنقيسو من le front، ماشي من القمة. "
      "فالتجربة، v égale un mètre par seconde. "
      f"فالتمرين، le front خرج من S فt égale zéro، وفt un، على la figure، وصل ل x F égale {mots(XF)} mètre. "
      f"إذن v égale x F sur t un، c'est-à-dire {mots(XF)} sur {mots(T1)}. v égale {mots(VV)} mètres par seconde.",
      [("v = x_F/t₁", "إذن v égale x F sur t un"),
       (f"v = {fr(XF)}/{fr(T1)} = {fr(VV)} m/s", f"v égale {mots(VV)} mètres par seconde")],
      [dict(mot="le front كيتقدم", commande="start"),
       dict(mot="ديما كنقيسو من le front", repere="distance_d"),
       dict(mot="إذن v égale x F sur t un", cible="centre:0"),
       dict(mot=f"v égale {mots(VV)} mètres par seconde", cible="centre:1")]),
    diapo_sim("ex_a2", "Question 2 : la longueur L, puis θ",
      "Sur y(x) on lit L ; pendant θ le front avance de L : θ = L/v.",
      SIM + "?vue=longueur", "Front, queue et longueur L",
      "شوف la source: كتتحرك المدة teta، ومن بعد كترجع ترتاح. فهاد المدة، le front كيتقدم. "
      "دابا la perturbation كاملة فوق la corde: عندها le front، وعندها اللخر. la distance بيناتهم هي L. "
      "فالتجربة، L égale zéro virgule quatre mètre، وteta égale zéro virgule quatre seconde. "
      f"فالتمرين، على la figure، la perturbation كتبدا من x égale {mots(XQ)} mètre، حتى ل le front. إذن L égale {mots(L)} mètre. "
      f"وteta égale L sur v، c'est-à-dire {mots(L)} sur {mots(VV)}. teta égale {mots(THc)} seconde.",
      [("L = v·θ ⇒ θ = L/v", "وteta égale L sur v"),
       (f"θ = {fr(L)}/{fr(VV)} = {fr(THc)} s", f"teta égale {mots(THc)} seconde")],
      [dict(mot="شوف la source", commande="start"),
       dict(mot="دابا la perturbation كاملة فوق la corde", commande="play_until", parametres={"moment": "toute_sur_corde"}),
       dict(mot="la distance بيناتهم هي L", repere="longueur_l"),
       dict(mot="وteta égale L sur v", cible="centre:0"),
       dict(mot=f"teta égale {mots(THc)} seconde", cible="centre:1")]),
    diapo_sim("ex_a3", "Question 3 : qui monte, qui descend ?",
      "Devant le sommet, les points montent ; derrière, ils descendent.",
      SIM + "?vue=sens", "Le sens du mouvement de chaque point",
      "تخيل la perturbation مشات شوية على اليمين. النقطة اللي قدام القمة، من جهة le front، غادي توصل للقمة: إذن كطلع. "
      "النقطة اللي مور القمة، غادي ترجع للصفر: إذن كتهبط. "
      "فالتجربة، des flèches صغار كيبينو الحركة: A قدام القمة، والفليشة ديالها للفوق. وB مور القمة، والفليشة ديالها للتحت. "
      "فالتمرين، نفس الشي: A بين القمة وle front، إذن A كطلع. وB مور القمة، إذن B كتهبط.",
      [("Devant le sommet (côté front) : monte", "إذن كطلع"),
       ("Derrière le sommet : descend", "إذن كتهبط. فالتجربة")],
      [dict(mot="تخيل la perturbation", commande="start"),
       dict(mot="إذن كطلع", cible="centre:0"),
       dict(mot="إذن كتهبط. فالتجربة", cible="centre:1"),
       dict(mot="A قدام القمة", repere="point_a")]),
    diapo_sim("ex_a4", "Question 4 : quand M bouge-t-il ?",
      "M démarre à t_M = SM/v et revient au repos à t_M + θ.",
      SIM + "?vue=longueur&depart=source_monte", "M atteint, puis revenu au repos",
      "شوف النقطة M فالتجربة. la perturbation كتقرب. وصلات ل M: دابا M كتبدا تتحرك. هادي هي t M égale SM sur v. "
      "M كتبقى كتتحرك المدة teta. شوف: M رجعات لبلاصتها، فt M plus teta. "
      f"فالتمرين، t M égale SM sur v، c'est-à-dire {mots(XM)} sur {mots(VV)}، égale {mots(TM)} seconde. "
      f"وM كترجع للراحة فt M plus teta، c'est-à-dire {mots(TM)} plus {mots(THc)}، égale {mots(TF)} seconde.",
      [("t_M = SM/v ; repos à t_M + θ", "هادي هي t M égale SM sur v"),
       (f"t_M = {fr(TM)} s ; t'_M = {fr(TF)} s", f"égale {mots(TF)} seconde")],
      [dict(mot="la perturbation كتقرب", commande="play_until", parametres={"moment": "m_atteint"}),
       dict(mot="دابا M كتبدا تتحرك", repere="point_m"),
       dict(mot="هادي هي t M égale SM sur v", cible="centre:0"),
       dict(mot="شوف: M رجعات لبلاصتها", commande="play_until", parametres={"moment": "m_revenu"}),
       dict(mot="شوف: M رجعات لبلاصتها", repere="duree_theta"),
       dict(mot=f"égale {mots(TF)} seconde", cible="centre:1")]),
    diapo_sim("ex_a5", "Question 5 : de l'aspect y(x) à l'élongation y_M(t)",
      "Même forme, renversée : front à droite sur y(x), à gauche sur y_M(t).",
      SIM + "?vue=aspect", "Aspect de la corde et élongation d'un point",
      "شوف les deux courbes. لفوق، l'aspect de la corde: y en fonction de x. le front على اليمين، حيت هو اللي بعيد على la source. "
      "لتحت، l'élongation ديال النقطة M: y en fonction de t. هنا le front على اليسار، حيت هو اللي كيوصل اللول. "
      "إذن la forme مقلوبة. "
      f"فالتمرين، y de M égale zéro jusqu'à t M, égale {mots(TM)} seconde. ومن بعد M كطلع بالزربة، وكتهبط بشوية jusqu'à {mots(TF)} seconde.",
      [("y(x) : front à droite ; y_M(t) : front à gauche", "إذن la forme مقلوبة"),
       (f"y_M(t) : 0, puis montée rapide à {fr(TM)} s, descente lente jusqu'à {fr(TF)} s", "ومن بعد M كطلع بالزربة")],
      [dict(mot="شوف les deux courbes", commande="start"),
       dict(mot="l'aspect de la corde", repere="axe_x"),
       dict(mot="l'élongation ديال النقطة M", repere="axe_t"),
       dict(mot="إذن la forme مقلوبة", cible="centre:0"),
       dict(mot="ومن بعد M كطلع بالزربة", cible="centre:1")]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_a1", "Plus facile : où est le front ?", "سؤال ساهل: فين كاين le front؟",
      f"Sur l'aspect à t₁ = {fr(T1)} s, la perturbation va de x = {fr(XQ)} m à x = {fr(XF)} m ; le sommet est vers x = {fr(XS, 1)} m. Le front est en…",
      [f"x = {fr(XS, 1)} m", f"x = {fr(XQ)} m", f"x = {fr(XF)} m"], 2, {
        "2": {"juste": rep(f"برافو! le front هو أبعد نقطة على S بدات تتحرك: x égale {mots(XF)} mètre. إذن v égale {mots(XF)} sur {mots(T1)}، c'est-à-dire {mots(VV)} mètres par seconde.",
                           f"Juste : x_F = {fr(XF)} m, donc v = {fr(XF)}/{fr(T1)} = {fr(VV)} m/s.")},
        "0": {"1": rep("ما تقلقش. هادي القمة، ماشي le front. le front هو أول نقطة بدات تتحرك، الأبعد على S. عاود اختار.",
                       "C'est le sommet, pas le front. Le front est le point en mouvement le plus loin de S. Réessaie."),
              "2": rep(f"la réponse est x égale {mots(XF)} mètre. القمة ماشي le front.",
                       f"Réponse : x_F = {fr(XF)} m ; le sommet n'est pas le front.")},
        "1": {"1": rep("قريب! هادي اللخر ديال la perturbation، من جهة S. le front من الجهة الأخرى. عاود اختار.",
                       "C'est la fin de la perturbation, côté S. Le front est de l'autre côté. Réessaie."),
              "2": rep(f"la réponse est x égale {mots(XF)} mètre. le front هو اللي بعيد على S.",
                       f"Réponse : x_F = {fr(XF)} m, l'extrémité la plus loin de S.")}},
      f"La perturbation va de x égale {mots(XQ)} mètre à x égale {mots(XF)} mètre. Le front est en ?"),
    vf_facile("fa_a2", "Plus facile : vrai ou faux sur L et θ", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      f"La perturbation va de x = {fr(XQ)} m à x = {fr(XF)} m ; v = {fr(VV)} m/s.", [
        (f"La longueur de la perturbation est L = {fr(XF)} m.", False, f"Faux : {fr(XF)} m est la distance de S au front ; L = {fr(XF)} − {fr(XQ)} = {fr(L)} m."),
        (f"L = {fr(L)} m et θ = L/v = {fr(THc)} s.", True, "Vrai : pendant θ, le front avance de L."),
        (f"θ = v/L = {fr(VV / L, 2)} s.", False, "Faux : v/L n'est pas une durée ; θ = L/v.")]),
    assoc_facile("fa_a3", "Plus facile : relier", "سؤال ساهل: ربط كل نقطة مع الحركة ديالها.",
      "A est devant le sommet, B derrière le sommet, M au-delà du front.", "Relie chaque point à son mouvement à la date t₁.",
      [("1", "A (entre le sommet et le front)"), ("2", "B (derrière le sommet)"), ("3", "M (au-delà du front)")],
      [("a", "monte"), ("b", "descend"), ("c", "au repos")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : A va prendre la place du sommet, il monte.", "برافو: A قدام القمة، غادي توصلها، إذن كطلع."),
       "1-b": (False, "A est devant le sommet, du côté du front : le sommet arrive vers lui.", "لا، A قدام القمة. القمة جاية ليها، إذن ماشي كتهبط."),
       "1-c": (False, "A est déjà atteint par la perturbation : il bouge.", "لا، A وصلاتها la perturbation، إذن كتتحرك."),
       "2-a": (False, "B est derrière le sommet : le sommet s'éloigne de lui.", "لا، B مور القمة. القمة كتبعد عليها، إذن ماشي كطلع."),
       "2-b": (True, "Oui : B revient vers le repos, il descend.", "برافو: B مور القمة، كترجع للصفر، إذن كتهبط."),
       "2-c": (False, "B est encore dans la perturbation : il bouge.", "لا، B مازال فla perturbation، إذن كتتحرك."),
       "3-a": (False, "Le front n'est pas encore arrivé en M.", "لا، le front مازال ما وصلش ل M."),
       "3-b": (False, "Le front n'est pas encore arrivé en M.", "لا، le front مازال ما وصلش ل M."),
       "3-c": (True, "Oui : au-delà du front, la corde est encore au repos.", "برافو: من مور le front، la corde مازال فالراحة.")},
      ("(1 ; a) (2 ; b) (3 ; c) : devant le sommet ça monte, derrière ça descend, au-delà du front c'est au repos.",
       "قدام القمة كطلع، مور القمة كتهبط، ومن مور le front فالراحة.")),
    qcm_facile("fa_a4", "Plus facile : la date d'arrêt de M", "سؤال ساهل: فوقاش كترجع M للراحة؟",
      f"M est atteint à t_M = {fr(TM)} s ; la perturbation dure θ = {fr(THc)} s. M revient au repos à…",
      [f"{fr(TF)} s", f"{fr(TM)} s", f"{fr(TM + L, 2)} s"], 0, {
        "0": {"juste": rep(f"برافو! t M plus teta، c'est-à-dire {mots(TM)} plus {mots(THc)}، égale {mots(TF)} seconde.",
                           f"Juste : t_M + θ = {fr(TM)} + {fr(THc)} = {fr(TF)} s.")},
        "1": {"1": rep("ما تقلقش. هادي اللحظة اللي كتبدا فيها M. من بعد كتبقى كتتحرك شي مدة. شحال؟ عاود اختار.",
                       "C'est la date où M commence ; il bouge ensuite pendant θ. Réessaie."),
              "2": rep(f"la réponse est {mots(TF)} seconde. M كتبدا ف t M، وكتبقى كتتحرك teta.",
                       f"Réponse : {fr(TF)} s = t_M + θ.")},
        "2": {"1": rep("قريب! ولكن زدتي L، وهي واحد la longueur بالمتر، ماشي la durée. عاود اختار.",
                       "Tu as ajouté L, une longueur en mètres, pas une durée. Réessaie."),
              "2": rep(f"la réponse est {mots(TF)} seconde. كنزيدو teta، ماشي L.",
                       f"Réponse : t_M + θ = {fr(TF)} s (on ajoute θ, pas L).")}},
      f"M est atteint à t M égale {mots(TM)} seconde, et la perturbation dure teta égale {mots(THc)} seconde. M revient au repos à ?"),
    qcm_facile("fa_a5", "Plus facile : l'allure de y_M(t)", "سؤال ساهل: اختار الوصف الصحيح ديال la courbe.",
      "Sur l'aspect y(x), la montée raide est à droite (côté front). Sur la courbe y_M(t)…",
      ["la montée raide est à droite aussi", "la montée raide est à gauche : M monte vite puis descend lentement",
       "la courbe commence à t = 0"], 1, {
        "1": {"juste": rep("برافو! فy en fonction de t، البداية ديال الحركة على اليسار. M كطلع بالزربة، ومن بعد كتهبط بشوية.",
                           "Juste : sur y_M(t), le début du mouvement est à gauche ; la forme est renversée.")},
        "0": {"1": rep("ما تقلقش. شوف l'axe: هنا le temps. أول حاجة كتوقع ل M، فين كتكون: فالأول ولا فاللخر؟ عاود اختار.",
                       "Regarde l'axe : c'est le temps. Ce qui arrive en premier à M est-il à gauche ou à droite ? Réessaie."),
              "2": rep("الجواب: الطلعة القاصحة على اليسار. le front هو اللي كيوصل اللول، إذن فأصغر لحظة.",
                       "Réponse : la montée raide est à gauche : le front arrive en premier.")},
        "2": {"1": rep("قريب! ولكن M بعيدة على S. واش la perturbation كتوصلها فt égale zéro؟ عاود اختار.",
                       "M est loin de S : la perturbation l'atteint-elle à t = 0 ? Réessaie."),
              "2": rep(f"الجواب: la courbe كتبدا ف t M، ماشي à t égale zéro. ومن بعد الطلعة القاصحة على اليسار.",
                       f"Réponse : y_M = 0 jusqu'à t_M = {fr(TM)} s, puis montée raide (à gauche) et descente lente.")}},
      "Sur l'aspect, la montée raide est à droite. Sur la courbe y de M en fonction de t ?"),
  ]}]},
  "similaire": {
    "id": "phys_ex_ch1_aspect_4_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": (f"Même corde, autre perturbation de durée θ, créée en S à t = 0. La figure représente l'aspect de la corde à la date "
                f"t₁ = {fr(T1b)} s. M est le point d'abscisse x_M = {fr(XMb)} m."),
      "intro_dit": (f"نفس la corde، perturbation أخرى. la figure كتبين l'aspect فt un égale {mots(T1b)} seconde، "
                    f"وx M égale {mots(XMb)} mètre."),
      "figures": [figure_aspect(Vb, THb, Ab, T1b, XAb, XBb, XMb)],
      "donnees": [f"t₁ = {fr(T1b)} s", f"x_M = {fr(XMb)} m"],
      "questions": [
        {"id": "1", "texte": "Lire x_F, l'abscisse du front à t₁, puis déduire v.",
         "reponse": valeur("v", VVb, "m/s", f"x_F = {fr(XFb)} m ; v = x_F/t₁ = {fr(XFb)}/{fr(T1b)} = {fr(VVb)} m/s"),
         "clavier": {"aides": ["v = x_F/t₁"], "pieges": ["x_F = sommet"]},
         "correction": correction([(f"1 : x_F = {fr(XFb)} m ; v = x_F/t₁ = {fr(XFb)}/{fr(T1b)} = {fr(VVb)} m/s", "v égale x F sur t un")],
                                  f"le front ف x F égale {mots(XFb)} mètre. v égale x F sur t un، c'est-à-dire {mots(XFb)} sur {mots(T1b)}. v égale {mots(VVb)} mètre par seconde.")},
        {"id": "2", "texte": "Lire la longueur L de la perturbation, puis déduire θ.",
         "reponse": valeur("θ", THcb, "s", f"L = {fr(XFb)} − {fr(XQb)} = {fr(Lb)} m ; θ = L/v = {fr(Lb)}/{fr(VVb)} = {fr(THcb)} s"),
         "clavier": {"aides": ["θ = L/v"], "pieges": ["θ = v/L"]},
         "correction": correction([(f"2 : L = {fr(Lb)} m ; θ = L/v = {fr(Lb)}/{fr(VVb)} = {fr(THcb)} s", "teta égale L sur v")],
                                  f"L égale {mots(Lb)} mètre. teta égale L sur v، c'est-à-dire {mots(Lb)} sur {mots(VVb)}. teta égale {mots(THcb)} seconde.")},
        {"id": "3", "texte": "Préciser, en justifiant, le sens du mouvement de A et de B à t₁.",
         "reponse": phrase(REP3),
         "clavier": {"aides": ["sommet", "front"], "pieges": ["B monte"]},
         "correction": correction([("3 : A, devant le sommet, monte ; B, derrière le sommet, descend.", "A كطلع")],
                                  "A قدام القمة، إذن A كطلع. B مور القمة، إذن B كتهبط.")},
        {"id": "4", "texte": "Déterminer les dates t_M et t'_M du début et de la fin du mouvement de M.",
         "reponse": valeur("t'_M", TFb, "s", f"t_M = {fr(XMb)}/{fr(VVb)} = {fr(TMb)} s ; t'_M = t_M + θ = {fr(TMb)} + {fr(THcb)} = {fr(TFb)} s"),
         "clavier": {"aides": ["t_M = SM/v", "t_M + θ"], "pieges": ["t_M + L"]},
         "correction": correction([(f"4 : t_M = SM/v = {fr(TMb)} s ; t'_M = t_M + θ = {fr(TFb)} s", "t M égale SM sur v")],
                                  f"t M égale SM sur v، c'est-à-dire {mots(XMb)} sur {mots(VVb)}، égale {mots(TMb)} seconde. "
                                  f"t M prime égale t M plus teta، égale {mots(TFb)} seconde.")},
        {"id": "5", "texte": "Décrire l'allure de y_M(t) en la comparant à l'aspect de la corde.",
         "reponse": phrase(f"y_M = 0 jusqu'à {fr(TMb)} s, montée rapide jusqu'au sommet (à {fr(TSOMb, 3)} s), descente lente jusqu'à "
                           f"{fr(TFb)} s, puis repos ; la montée raide, à droite sur y(x), est à gauche sur y_M(t) : forme renversée."),
         "clavier": {"aides": ["montée rapide", "descente lente", "renversée"], "pieges": ["même forme, front à droite"]},
         "correction": correction([(f"5 : y_M = 0 avant {fr(TMb)} s ; montée rapide puis descente lente jusqu'à {fr(TFb)} s ; forme renversée par rapport à y(x).", "la forme مقلوبة")],
                                  "قبل t M، y de M égale zéro. من بعد كطلع بالزربة، وكتهبط بشوية، ومن بعد فالراحة. la forme مقلوبة بالمقارنة مع l'aspect.")}
      ]}}
}

ecrire(EX)
