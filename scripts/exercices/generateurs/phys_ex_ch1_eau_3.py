# Exercice de physique (ch. 1, ondes mécaniques progressives), niveau moyen : une ride à la surface de l'eau.
# Sources comparées (skill exercices § 2) :
#  - exploration ondes_mecaniques_periodiques.json (partie ch1 : erreurs_examen « 2019 N Q1.1 nature de l'onde : répond
#    sans justifier », pièges « y_M(t) = y_S(t + τ) », « τ en ms dans la parenthèse », « confond θ, τ et T ») et
#    experience_profs.json « ondes_mecaniques » (cas types « photo » : distance mesurée de front à front, v = d/Δt ;
#    « état vibratoire » : L = v·θ, date d'arrêt = arrivée + θ ; insistance « l'onde transporte de l'énergie, pas de
#    matière » ; piège « mesurer jusqu'à l'arrière de l'onde »).
#  - Nationaux comparés : 2024 N ex. 2 (caillou en O, tableau des rayons r₁ = 14 cm à t₁ et r₂ = 56 cm à
#    t₂ = t₁ + 1,5 s, v puis t₂, puis v = √(g·h)) ; 2022 R ex. 2 (courbe y_M(t) d'un point à L = 2,5 cm, onde
#    périodique) ; 2019 N ex. 2 Q1.1 (transversale ou longitudinale ? justifier). Ici : une goutte, deux COUPES
#    verticales datées (fronts à 10 cm et 25 cm), la durée θ lue comme une longueur, le retard d'un ballon et son
#    élongation par y_M(t) = y_S(t − τ) lue sur y_S(t) : autre situation, autres données, autre enchaînement.
#  - Séries en ligne : recherche faite (talamidi série corrigée 1, moutamadris 2BAC « exercices PC 1-4 », alloschool
#    119785, cours Bendaoud « aspect à t et t + θ ») ; lecture des PDF bloquée par le réseau de la session
#    (talamidi.com, moutamadris.ma, alloschool.com non résolus).
#  - Simulation : ballon.html (V = 0,25 m/s, θ = 0,4 s, ballon à d = 0,3 m) : les données de l'exercice sont
#    celles de la simulation ; le ballon y est atteint à t = 1,2 s et au plus haut à t = 1,3 s (affichés).
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


SIM = "/media/simulations/physics/ondes-tableau/ballon.html"


# ---------- la physique (même modèle que ballon.html : y(r, t) = y_S(t − r/v), une sinusoïde complète de durée θ) ----------
def yS(t, a, theta):
    return 0.0 if (t < 0 or t > theta) else a * math.sin(2 * math.pi * t / theta)


def coupe(v, theta, a, t, titre, ballon=None, rmax=35):
    """Coupe verticale de la surface à la date t : r en cm, y en mm."""
    pts = []
    for i in range(281):
        r = rmax * i / 280
        pts.append([round(r, 3), round(yS(t - r / 100 / v, a, theta), 3)])
    xf = v * t * 100
    el = [{"f": "ligne", "pts": pts, "couleur": "cyan", "epais": True},
          {"f": "point", "at": [0, 0], "t": "S", "pos": "so", "couleur": "jaune"},
          {"f": "repere", "x": round(xf, 3), "t": "front", "couleur": "jaune"}]
    if ballon is not None:
        el.append({"f": "point", "at": [ballon * 100, 0], "t": "M (ballon)", "pos": "ne", "couleur": "orange"})
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": 0, "max": rmax, "nom": "r", "unite": "cm", "graduations": list(range(5, rmax + 1, 5))},
                     "y": {"min": -1.4 * a, "max": 1.4 * a, "nom": "y", "unite": "mm", "graduations": [-a, a]}},
            "elements": el}


def courbe_source(theta, a, titre, tmax=0.6):
    pts = [[round(tmax * i / 240, 4), round(yS(tmax * i / 240, a, theta), 3)] for i in range(241)]
    pas = 0.1 if tmax <= 0.6 else 0.2
    gr = [round(pas * k, 2) for k in range(1, int(round(tmax / pas)) + 1)]
    return {"type": "courbe", "titre": titre,
            "legende": "La source S monte, descend sous le niveau de l'eau, puis revient au repos.",
            "axes": {"x": {"min": 0, "max": tmax, "nom": "t", "unite": "s", "graduations": gr},
                     "y": {"min": -1.4 * a, "max": 1.4 * a, "nom": "y_S", "unite": "mm", "graduations": [-a, a]}},
            "elements": [{"f": "ligne", "pts": pts, "couleur": "orange", "epais": True}]}


def calculs(v, theta, a, t1, t2, sm, t3):
    r1, r2 = v * t1, v * t2                     # m
    vv = (r2 - r1) / (t2 - t1)
    L = v * theta                               # lue sur la coupe à t2 : du dernier point en mouvement au front
    th = L / vv
    tau = sm / vv
    y3 = yS(t3 - tau, a, theta)
    return r1, r2, vv, L, th, tau, y3


# ---------- données (= la simulation ballon.html) ----------
V, TH, A = 0.25, 0.4, 4
T1, T2, SM, T3 = 0.4, 1.0, 0.30, 1.3
R1, R2, VV, L, THc, TAU, Y3 = calculs(V, TH, A, T1, T2, SM, T3)
assert abs(VV - 0.25) < 1e-12 and abs(THc - 0.4) < 1e-12 and abs(TAU - 1.2) < 1e-12 and abs(Y3 - 4) < 1e-9
U3 = T3 - TAU   # 0,1 s

# ---------- similaire ----------
Vb, THb, Ab = 0.3, 0.2, 5
T1b, T2b, SMb, T3b = 0.2, 1.0, 0.36, 1.35
R1b, R2b, VVb, Lb, THcb, TAUb, Y3b = calculs(Vb, THb, Ab, T1b, T2b, SMb, T3b)
assert abs(VVb - 0.3) < 1e-12 and abs(THcb - 0.2) < 1e-12 and abs(TAUb - 1.2) < 1e-12 and abs(Y3b + 5) < 1e-9
U3b = T3b - TAUb

cm = lambda x: fr(x * 100, 1)

EX = {
  "id": "phys_ex_ch1_eau_3", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques", "cours": "phys_ch1_waves_exemple",
  "titre": "Une ride à la surface de l'eau", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Justifier la nature transversale d'une onde",
                  "Calculer la célérité entre deux positions datées du front : v = Δr/Δt",
                  "Lire la longueur L d'une perturbation et en déduire sa durée θ = L/v",
                  "Calculer un retard τ = SM/v",
                  "Utiliser y_M(t) = y_S(t − τ) pour trouver l'élongation d'un point"],
  "enonce": {
    "intro": (f"À la date t = 0, une goutte tombe au point S de la surface d'une eau calme. Une ride circulaire, de courte durée θ, "
              f"part de S et s'étale sans amortissement. Un petit ballon M flotte à la distance SM = {cm(SM)} cm de S. "
              f"Les figures 1 et 2 représentent une coupe verticale de la surface de l'eau, suivant une demi-droite issue de S, "
              f"aux dates t₁ = {fr(T1)} s et t₂ = {fr(T2)} s. La figure 3 représente l'élongation y_S(t) de la source S."),
    "intro_dit": (f"دابا نقراو l'énoncé. فt égale zéro، طاحت واحد النقطة ديال الما فالنقطة S، فوق ما هادي. "
                  f"خرجات واحد la ride دائرية، كتدوم واحد المدة قصيرة teta، وكتمشي بلا ما تضعاف. "
                  f"واحد الكورة صغيرة M، فوق الما، بعيدة على S ب SM égale {mots(SM * 100)} centimètres. "
                  f"la figure un وla figure deux كيبينو la coupe ديال سطح الما، فt un égale {mots(T1)} seconde، "
                  f"وفt deux égale {mots(T2)} seconde. وla figure trois كتبين l'élongation ديال la source S، y S en fonction de t."),
    "figures": [coupe(V, TH, A, T1, f"Figure 1 : coupe de la surface à t₁ = {fr(T1)} s"),
                coupe(V, TH, A, T2, f"Figure 2 : coupe de la surface à t₂ = {fr(T2)} s", ballon=SM),
                courbe_source(TH, A, "Figure 3 : élongation y_S(t) de la source S")],
    "donnees": [f"t₁ = {fr(T1)} s ; t₂ = {fr(T2)} s", f"SM = {cm(SM)} cm", "On néglige l'amortissement de l'onde."],
    "questions": [
      {"id": "1", "texte": "L'onde qui se propage à la surface de l'eau est-elle transversale ou longitudinale ? Justifier.",
       "texte_dit": "la question un: l'onde اللي كتمشي فوق سطح الما، واش هي transversale ولا longitudinale؟ justifier.",
       "reponse": phrase("Transversale : chaque point de la surface (le ballon) monte et descend verticalement, alors que l'onde se propage "
                         "horizontalement ; la direction de la perturbation est perpendiculaire à la direction de propagation."),
       "clavier": {"aides": ["direction de la perturbation", "direction de propagation", "perpendiculaire", "verticale", "horizontale"],
                   "pieges": ["parallèle", "le ballon avance avec l'onde"]},
       "aides": [
         aide("Regarde le ballon : dans quelle direction bouge-t-il quand la ride passe ? Et dans quelle direction la ride avance-t-elle ?",
              "شوف الكورة: ملي كدوز la ride، فين كتحرك؟ للفوق وللتحت، ولا للقدام؟ وla ride، فين كتمشي؟"),
         aide("Compare les deux directions : perpendiculaires → transversale ; même direction → longitudinale.",
              "قارن جوج ديال الاتجاهات: يلا كانو perpendiculaires، l'onde transversale. يلا كانو فنفس الخط، longitudinale.")],
       "correction": correction([
           ("1 : chaque point de la surface monte et descend (direction verticale) ; l'onde se propage horizontalement.", "الكورة كطلع وكتهبط"),
           ("La direction de la perturbation est perpendiculaire à la direction de propagation : l'onde est transversale.", "إذن l'onde transversale")],
           "la question un. الكورة كطلع وكتهبط فبلاصتها، يعني la perturbation عمودية. وla ride كتمشي أفقيا فوق الما. "
           "la direction de la perturbation، perpendiculaire à la direction de propagation. إذن l'onde transversale."),
       "explication": "ex_e1", "facile": "fa_e1"},
      {"id": "2", "texte": "À l'aide des figures 1 et 2, déterminer la célérité v de l'onde à la surface de l'eau.",
       "texte_dit": "la question deux: avec les figures un et deux، حدد la célérité v ديال l'onde فوق الما.",
       "reponse": valeur("v", VV, "m/s", f"v = (r₂ − r₁)/(t₂ − t₁) = ({fr(R2)} − {fr(R1)})/({fr(T2)} − {fr(T1)}) = {fr(VV)} m/s"),
       "clavier": {"aides": ["v = d/Δt", "r₁", "r₂", "t₂ − t₁", "1 cm = 10⁻² m", "A.N. :"],
                   "pieges": ["v = r₂/(t₂ − t₁)", "r en cm dans le calcul"]},
       "aides": [
         aide("Sur chaque coupe, repère le front (le point le plus loin de S qui a commencé à bouger) et lis sa distance à S.",
              "فكل coupe، قلب على le front: هو أبعد نقطة على S اللي بدات تتحرك. اقرا la distance ديالو على S."),
         aide("Entre t₁ et t₂, le front parcourt r₂ − r₁ : v = (r₂ − r₁)/(t₂ − t₁), avec les distances en mètres.",
              "بين t un وt deux، le front قطع r deux moins r un. إذن v égale r deux moins r un، sur t deux moins t un. ورد البال: la distance en mètre.")],
       "correction": correction([
           (f"2 : à t₁, le front est à r₁ = {cm(R1)} cm ; à t₂, à r₂ = {cm(R2)} cm", "le front كان ف r un"),
           ("v = (r₂ − r₁)/(t₂ − t₁)", "v égale r deux moins r un"),
           (f"v = ({fr(R2)} − {fr(R1)})/({fr(T2)} − {fr(T1)}) = {fr(VV)} m/s", f"v égale {mots(VV)} mètre par seconde")],
           f"la question deux. فt un، le front كان ف r un égale {mots(R1 * 100)} centimètres. وفt deux، ف r deux égale {mots(R2 * 100)} centimètres. "
           f"le front كان ف r un، ومن بعد قطع r deux moins r un. إذن v égale r deux moins r un، sur t deux moins t un. "
           f"c'est-à-dire {mots(R2)} moins {mots(R1)}، sur {mots(T2)} moins {mots(T1)}. v égale {mots(VV)} mètre par seconde."),
       "explication": "ex_e2", "facile": "fa_e2"},
      {"id": "3", "texte": "Lire sur la figure 2 la longueur L de la perturbation, puis en déduire sa durée θ.",
       "texte_dit": "la question trois: اقرا على la figure deux la longueur L ديال la perturbation، ومن بعد استنتج la durée teta ديالها.",
       "reponse": valeur("θ", THc, "s", f"L = {cm(R2)} − {cm(R2 - L)} = {cm(L)} cm ; θ = L/v = {fr(L)}/{fr(VV)} = {fr(THc)} s"),
       "clavier": {"aides": ["L = v·θ", "θ = L/v", "front", "1 cm = 10⁻² m", "A.N. :"],
                   "pieges": ["θ = v/L", "L = r₂ (distance de S au front)"]},
       "aides": [
         aide("La perturbation s'étend du dernier point encore en mouvement (le plus proche de S) jusqu'au front. Entre les deux, quelle distance ?",
              "la perturbation كتبدا من آخر نقطة مازال كتتحرك، القريبة ل S، حتى ل le front. شحال من distance بيناتهم؟ ماشي من S."),
         aide("Pendant θ, le front avance de L : L = v·θ, donc θ = L/v (L en mètres).",
              "فla durée teta، le front كيقطع L. إذن L égale v fois teta، يعني teta égale L sur v. وL en mètre.")],
       "correction": correction([
           (f"3 : sur la figure 2, la perturbation va de r = {cm(R2 - L)} cm au front r₂ = {cm(R2)} cm : L = {cm(L)} cm = {fr(L)} m", "la perturbation كتبدا"),
           ("L = v·θ, donc θ = L/v", "إذن teta égale L sur v"),
           (f"θ = {fr(L)}/{fr(VV)} = {fr(THc)} s", f"teta égale {mots(THc)} seconde")],
           f"la question trois. على la figure deux، la perturbation كتبدا من r égale {mots((R2 - L) * 100)} centimètres، حتى ل le front، à {mots(R2 * 100)} centimètres. "
           f"إذن L égale {mots(L * 100)} centimètres، c'est-à-dire {mots(L)} mètre. "
           f"L égale v fois teta، إذن teta égale L sur v، c'est-à-dire {mots(L)} sur {mots(VV)}. teta égale {mots(THc)} seconde."),
       "explication": "ex_e3", "facile": "fa_e3"},
      {"id": "4", "texte": "Calculer le retard τ du mouvement du ballon M par rapport à celui de la source S. À la date t₂, le ballon a-t-il commencé à bouger ?",
       "texte_dit": "la question quatre: حسب le retard tau ديال الحركة ديال الكورة M بالنسبة ل la source S. وفt deux، واش الكورة بدات تتحرك؟",
       "reponse": valeur("τ", TAU, "s", f"τ = SM/v = {fr(SM)}/{fr(VV)} = {fr(TAU)} s"),
       "clavier": {"aides": ["τ = SM/v", "SM", "v", "s", "A.N. :"],
                   "pieges": ["τ = v/SM", "SM en cm"]},
       "aides": [
         aide("Le ballon commence à bouger quand le front arrive en M : le retard est la durée du trajet du front de S à M.",
              "الكورة كتبدا تتحرك ملي كيوصل ليها le front. le retard هو la durée اللي كياخد le front من S حتى ل M."),
         aide("τ = SM/v, avec SM en mètres ; compare ensuite τ et t₂.",
              "tau égale SM sur v، وSM en mètre. ومن بعد قارن tau مع t deux.")],
       "correction": correction([
           ("4 : le front parcourt SM pendant τ : τ = SM/v", "tau égale SM sur v"),
           (f"τ = {fr(SM)}/{fr(VV)} = {fr(TAU)} s", f"tau égale {mots(TAU)} seconde"),
           (f"t₂ = {fr(T2)} s < τ : à t₂, le ballon est encore au repos (sur la figure 2, le front n'a pas atteint M).", "الكورة مازال فالراحة")],
           f"la question quatre. le front كيقطع SM فla durée tau. إذن tau égale SM sur v، c'est-à-dire {mots(SM)} sur {mots(VV)}. "
           f"tau égale {mots(TAU)} seconde. وt deux égale {mots(T2)} seconde، صغر من tau. إذن فt deux، الكورة مازال فالراحة: le front ما وصلش ليها."),
       "explication": "ex_e4", "facile": "fa_e4"},
      {"id": "5", "texte": f"Justifier la relation y_M(t) = y_S(t − τ), puis déterminer, à l'aide de la figure 3, l'élongation y_M du ballon à la date t₃ = {fr(T3)} s.",
       "texte_dit": f"la question cinq: justifier la relation، y de M de t égale y de S de t moins tau. ومن بعد، avec la figure trois، حدد l'élongation ديال الكورة فt trois égale {mots(T3)} seconde.",
       "reponse": valeur("y_M", Y3, "mm", f"y_M(t₃) = y_S(t₃ − τ) = y_S({fr(T3)} − {fr(TAU)}) = y_S({fr(U3)}) = {fr(Y3)} mm"),
       "clavier": {"aides": ["y_M(t) = y_S(t − τ)", "t₃ − τ", "figure 3", "mm"],
                   "pieges": ["y_M(t) = y_S(t + τ)", "y_S(t₃)"]},
       "aides": [
         aide("Sans amortissement, le ballon refait le mouvement de S avec le retard τ. À la date t₃, il fait ce que S faisait à quelle date ?",
              "بلا تضعاف، الكورة كدير نفس الحركة ديال S، ولكن من بعد tau. فt trois، الكورة كدير شنو كانت كدير S، فأي لحظة؟"),
         aide("Calcule t₃ − τ, puis lis y_S à cette date sur la figure 3.",
              "حسب t trois moins tau، ومن بعد اقرا y S فهاد اللحظة على la figure trois.")],
       "correction": correction([
           ("5 : l'onde n'est pas amortie, M reproduit le mouvement de S avec le retard τ : y_M(t) = y_S(t − τ)", "y de M de t égale y de S de t moins tau"),
           (f"t₃ − τ = {fr(T3)} − {fr(TAU)} = {fr(U3)} s", "t trois moins tau"),
           (f"Sur la figure 3, y_S({fr(U3)} s) = {fr(Y3)} mm : y_M(t₃) = {fr(Y3)} mm, le ballon est à son point le plus haut.", f"y de M de t trois égale {mots(Y3)} millimètres")],
           f"la question cinq. l'onde non amortie، إذن M كدير نفس الحركة ديال S بالretard tau. نكتبو: y de M de t égale y de S de t moins tau. "
           f"دابا t trois moins tau égale {mots(T3)} moins {mots(TAU)}، c'est-à-dire {mots(U3)} seconde. "
           f"على la figure trois، فt égale {mots(U3)} seconde، la source كانت فالقمة. إذن y de M de t trois égale {mots(Y3)} millimètres: الكورة فالقمة."),
       "explication": "ex_e5", "facile": "fa_e5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    diapo_sim("ex_e1", "Question 1 : la ride avance, le ballon monte et descend",
      "Mouvement vertical du ballon, propagation horizontale : onde transversale.",
      SIM, "Une goutte, des rides, un ballon qui reste à sa place",
      "شوف فالتجربة. طاحت النقطة ديال الما فS، وخرجو دوائر صغار كيكبرو. la ride كتمشي أفقيا فوق الما. "
      "دابا شوف الكورة: كطلع، ومن بعد كتهبط، وكتبقى فبلاصتها. الحركة ديالها عمودية. "
      "la direction de la perturbation، perpendiculaire à la direction de propagation. إذن l'onde transversale. "
      "والكورة ما مشاتش مع la ride: l'onde كتنقل l'énergie، ماشي الما.",
      [("Ballon : vertical ; ride : horizontale", "الحركة ديالها عمودية"),
       ("⊥ → onde transversale", "إذن l'onde transversale")],
      [dict(mot="طاحت النقطة ديال الما", commande="play_until", parametres={"moment": "ride_part"}),
       dict(mot="طاحت النقطة ديال الما", repere="goutte"),
       dict(mot="la ride كتمشي أفقيا", commande="play_until", parametres={"moment": "rides_grandissent"}),
       dict(mot="la ride كتمشي أفقيا", repere="rides"),
       dict(mot="دابا شوف الكورة", repere="bouee_cote"),
       dict(mot="كطلع، ومن بعد كتهبط", commande="play_until", parametres={"moment": "bouee_creux"}),
       dict(mot="وكتبقى فبلاصتها", commande="play_until", parametres={"moment": "bouee_revenue"}),
       dict(mot="وكتبقى فبلاصتها", repere="trajet"),
       dict(mot="الحركة ديالها عمودية", cible="centre:0"),
       dict(mot="إذن l'onde transversale", cible="centre:1")]),
    diapo_sim("ex_e2", "Question 2 : la célérité, de front à front",
      "Entre t₁ et t₂, le front avance de r₂ − r₁ : v = (r₂ − r₁)/(t₂ − t₁).",
      SIM, "Le front des rides s'éloigne de S",
      f"شوف le front ديال les rides: كيتبعد على S، وكل ما زاد le temps، كيزيد يبعد. "
      f"فالتجربة مكتوب: v environ {mots(V)} mètre par seconde. "
      f"فالتمرين، فt un، le front à {mots(R1 * 100)} centimètres، وفt deux، à {mots(R2 * 100)} centimètres. "
      f"ديما من le front حتى ل le front. إذن v égale r deux moins r un، sur t deux moins t un. "
      f"c'est-à-dire {mots(R2 - R1)} sur {mots(T2 - T1)}. v égale {mots(VV)} mètre par seconde، نفس القيمة ديال التجربة.",
      [("v = (r₂ − r₁)/(t₂ − t₁)", "إذن v égale r deux moins r un"),
       (f"v = {fr(R2 - R1)}/{fr(T2 - T1)} = {fr(VV)} m/s", f"v égale {mots(VV)} mètre par seconde، نفس")],
      [dict(mot="شوف le front ديال les rides", commande="play_until", parametres={"moment": "rides_grandissent"}),
       dict(mot="شوف le front ديال les rides", repere="rides"),
       dict(mot="فالتجربة مكتوب", repere="profil"),
       dict(mot="إذن v égale r deux moins r un", cible="centre:0"),
       dict(mot=f"v égale {mots(VV)} mètre par seconde، نفس", cible="centre:1")]),
    diapo_sim("ex_e3", "Question 3 : la longueur L, puis la durée θ",
      "Pendant θ, le front avance de L : θ = L/v.",
      SIM, "Le ballon bouge pendant la durée θ",
      "شوف الكورة. ملي كتوصلها la ride، كتبدا تتحرك. كطلع، كتهبط، ومن بعد كترجع لبلاصتها. "
      "المدة اللي بقات كتتحرك هي teta، la durée de la perturbation. "
      "فهاد المدة، le front كيقطع L. إذن L égale v fois teta. "
      f"فالتمرين، على la coupe ديال t deux، la perturbation كتبدا من r égale {mots((R2 - L) * 100)} centimètres، حتى ل le front. "
      f"إذن L égale {mots(L * 100)} centimètres. teta égale L sur v، c'est-à-dire {mots(L)} sur {mots(VV)}. teta égale {mots(THc)} seconde.",
      [("L = v·θ ⇒ θ = L/v", "إذن L égale v fois teta"),
       (f"θ = {fr(L)}/{fr(VV)} = {fr(THc)} s", f"teta égale {mots(THc)} seconde")],
      [dict(mot="شوف الكورة", repere="bouee_cote"),
       dict(mot="كتبدا تتحرك", commande="play_until", parametres={"moment": "bouee_atteinte"}),
       dict(mot="ومن بعد كترجع لبلاصتها", commande="play_until", parametres={"moment": "bouee_revenue"}),
       dict(mot="ومن بعد كترجع لبلاصتها", repere="trajet"),
       dict(mot="إذن L égale v fois teta", cible="centre:0"),
       dict(mot=f"teta égale {mots(THc)} seconde", cible="centre:1")]),
    diapo_sim("ex_e4", "Question 4 : le retard du ballon",
      "Le ballon commence à bouger quand le front arrive : τ = SM/v.",
      SIM, "La ride arrive au ballon",
      f"فالتجربة، الكورة بعيدة على S ب d égale {mots(SM)} mètre، بحال التمرين. "
      "شوف la ride كتقرب من الكورة. وصلات ليها: دابا كتبدا تتحرك. "
      f"شوف le temps: t égale {mots(TAU)} seconde. هادا هو le retard tau. "
      f"إذن tau égale SM sur v، c'est-à-dire {mots(SM)} sur {mots(VV)}. tau égale {mots(TAU)} seconde. "
      f"وفt deux égale {mots(T2)} seconde، الكورة مازال ما تحركاتش.",
      [("τ = SM/v", "إذن tau égale SM sur v"),
       (f"τ = {fr(SM)}/{fr(VV)} = {fr(TAU)} s", f"tau égale {mots(TAU)} seconde. وف")],
      [dict(mot="الكورة بعيدة على S", commande="set_parameters", parametres={"d_m": SM}),
       dict(mot="الكورة بعيدة على S", repere="bouee"),
       dict(mot="شوف la ride كتقرب", commande="play_until", parametres={"moment": "bouee_atteinte"}),
       dict(mot="هادا هو le retard tau", repere="bouee_cote"),
       dict(mot="إذن tau égale SM sur v", cible="centre:0"),
       dict(mot=f"tau égale {mots(TAU)} seconde. وف", cible="centre:1")]),
    diapo_sim("ex_e5", "Question 5 : l'élongation du ballon à t₃",
      "y_M(t) = y_S(t − τ) : à t₃, le ballon fait ce que S faisait à t₃ − τ.",
      SIM, "Le ballon au plus haut",
      "دابا الكورة كتعاود نفس الحركة ديال S، ولكن من بعد tau. "
      f"شوف: الكورة طلعات للقمة. le temps مكتوب: t égale {mots(T3)} seconde. "
      f"إذن t trois moins tau égale {mots(T3)} moins {mots(TAU)}، c'est-à-dire {mots(U3)} seconde. "
      f"وفt égale {mots(U3)} seconde، la source S كانت فالقمة ديالها. "
      f"إذن y de M de t trois égale y de S de {mots(U3)}، c'est-à-dire {mots(Y3)} millimètres.",
      [("y_M(t) = y_S(t − τ)", "دابا الكورة كتعاود نفس الحركة"),
       (f"y_M({fr(T3)}) = y_S({fr(U3)}) = {fr(Y3)} mm", f"c'est-à-dire {mots(Y3)} millimètres")],
      [dict(mot="دابا الكورة كتعاود", commande="set_parameters", parametres={"d_m": SM}),
       dict(mot="دابا الكورة كتعاود نفس الحركة", cible="centre:0"),
       dict(mot="شوف: الكورة طلعات للقمة", commande="play_until", parametres={"moment": "bouee_sommet"}),
       dict(mot="شوف: الكورة طلعات للقمة", repere="bouee_cote"),
       dict(mot=f"c'est-à-dire {mots(Y3)} millimètres", cible="centre:1")]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_e1", "Plus facile : le type d'onde", "سؤال ساهل: اختار الجواب الصحيح.",
      "Le ballon monte et descend ; la ride avance horizontalement. L'onde est…",
      ["longitudinale", "transversale", "ni l'une ni l'autre"], 1, {
        "1": {"juste": rep("برافو! la perturbation عمودية، وla propagation أفقية. perpendiculaires، إذن transversale.",
                           "Juste : perturbation verticale ⊥ propagation horizontale : transversale.")},
        "0": {"1": rep("ما تقلقش. longitudinale يعني la perturbation فنفس الاتجاه ديال la propagation. واش الكورة كتمشي للقدام؟ عاود اختار.",
                       "Longitudinale : perturbation dans la direction de propagation. Le ballon avance-t-il ? Réessaie."),
              "2": rep("الجواب هو transversale. الكورة كطلع وكتهبط، عمودي على الاتجاه ديال la ride.",
                       "Réponse : transversale (mouvement vertical, propagation horizontale).")},
        "2": {"1": rep("قريب! قارن غير جوج ديال الاتجاهات: الحركة ديال الكورة، والاتجاه ديال la ride. عاود اختار.",
                       "Compare seulement deux directions : celle du ballon et celle de la ride. Réessaie."),
              "2": rep("الجواب هو transversale. جوج ديال الاتجاهات perpendiculaires.",
                       "Réponse : transversale : les deux directions sont perpendiculaires.")}},
      "Le ballon monte et descend, la ride avance horizontalement. L'onde est ?"),
    qcm_facile("fa_e2", "Plus facile : la distance parcourue par le front", "سؤال ساهل: شحال قطع le front؟",
      f"Le front est à {cm(R1)} cm à t₁ = {fr(T1)} s et à {cm(R2)} cm à t₂ = {fr(T2)} s. La célérité vaut…",
      [f"{fr(R2 / (T2 - T1))} m/s", f"{fr(VV)} m/s", f"{fr(R2 * 100 - R1 * 100)} m/s"], 1, {
        "1": {"juste": rep(f"برافو! le front قطع r deux moins r un, égale {mots((R2 - R1) * 100)} centimètres، فla durée t deux moins t un. v égale {mots(VV)} mètre par seconde.",
                           f"Juste : v = ({fr(R2)} − {fr(R1)})/({fr(T2)} − {fr(T1)}) = {fr(VV)} m/s.")},
        "0": {"1": rep("ما تقلقش. خديتي r deux كاملة. ولكن فt un، le front كان ديجا بعيد على S. شحال قطع بين t un وt deux؟ عاود اختار.",
                       "Tu as pris r₂ entier ; mais à t₁ le front était déjà à r₁. Réessaie."),
              "2": rep(f"la réponse est {mots(VV)} mètre par seconde. la distance هي r deux moins r un، ماشي r deux.",
                       f"Réponse : {fr(VV)} m/s ; la distance parcourue pendant t₂ − t₁ est r₂ − r₁.")},
        "2": {"1": rep("قريب! ولكن نسيتي تحول centimètre ل mètre، ونسيتي تقسم على la durée. عاود اختار.",
                       "Les cm ne sont pas convertis, et il manque la division par Δt. Réessaie."),
              "2": rep(f"la réponse est {mots(VV)} mètre par seconde. {mots(R2 - R1)} mètre sur {mots(T2 - T1)} seconde.",
                       f"Réponse : {fr(R2 - R1)} m / {fr(T2 - T1)} s = {fr(VV)} m/s.")}},
      f"Le front est à {mots(R1 * 100)} centimètres à t un, et à {mots(R2 * 100)} centimètres à t deux. La célérité vaut ?"),
    vf_facile("fa_e3", "Plus facile : vrai ou faux sur L et θ", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      f"À t₂, la perturbation va de {cm(R2 - L)} cm à {cm(R2)} cm ; v = {fr(VV)} m/s.", [
        (f"La longueur de la perturbation est L = {cm(R2)} cm.", False, f"Faux : {cm(R2)} cm est la distance de S au front ; L va du dernier point en mouvement au front : {cm(L)} cm."),
        (f"La longueur de la perturbation est L = {cm(L)} cm.", True, f"Vrai : L = {cm(R2)} − {cm(R2 - L)} = {cm(L)} cm."),
        (f"θ = L/v = {fr(L)}/{fr(VV)} = {fr(THc)} s.", True, "Vrai : pendant θ, le front avance de L, donc θ = L/v.")]),
    assoc_facile("fa_e4", "Plus facile : relier", "سؤال ساهل: ربط كل سؤال مع الجواب ديالو.",
      f"SM = {cm(SM)} cm ; v = {fr(VV)} m/s.", "Relie chaque grandeur à sa valeur.",
      [("1", "le retard τ = SM/v"), ("2", "la date où le ballon revient au repos, τ + θ")],
      [("a", f"{fr(TAU)} s"), ("b", f"{fr(TAU + THc)} s"), ("c", f"{fr(VV / SM, 3)} s")],
      {"1": "a", "2": "b"},
      {"1-a": (True, f"Oui : τ = {fr(SM)}/{fr(VV)} = {fr(TAU)} s.", f"برافو: tau égale SM sur v، c'est-à-dire {mots(TAU)} seconde."),
       "1-b": (False, "Ça, c'est la date où le ballon s'arrête : il commence à τ, puis bouge encore pendant θ.", "لا، هادي اللحظة اللي كتوقف فيها الكورة. كتبدا ف tau، وكتبقى كتتحرك teta."),
       "1-c": (False, "Ce nombre vient de v/SM : le retard est SM/v.", "لا، هادا v sur SM. le retard هو SM sur v."),
       "2-a": (False, "À τ, le ballon commence à bouger ; il s'arrête θ plus tard.", "لا، فtau الكورة كتبدا. كتوقف من بعد teta."),
       "2-b": (True, f"Oui : {fr(TAU)} + {fr(THc)} = {fr(TAU + THc)} s.", f"برافو: tau plus teta égale {mots(TAU + THc)} seconde."),
       "2-c": (False, "Ce nombre vient de v/SM, ce n'est pas une date du mouvement du ballon.", "لا، هادا v sur SM، ماشي اللحظة ديال الكورة.")},
      ("(1 ; a) (2 ; b) : le ballon bouge de τ à τ + θ.", "الكورة كتتحرك من tau حتى ل tau plus teta.")),
    qcm_facile("fa_e5", "Plus facile : la bonne relation", "سؤال ساهل: اختار la bonne relation.",
      "Le ballon M reproduit le mouvement de S avec le retard τ. On écrit…",
      ["y_M(t) = y_S(t + τ)", "y_M(t) = y_S(t)", "y_M(t) = y_S(t − τ)"], 2, {
        "2": {"juste": rep("برافو! M متأخرة، إذن كنقصو tau: y de M de t égale y de S de t moins tau.",
                           "Juste : M est en retard, on retranche τ.")},
        "0": {"1": rep("ما تقلقش. M متأخرة على S. واش كدير اللي غادي تدير S من بعد، ولا اللي دارت S قبل؟ عاود اختار.",
                       "M est en retard : fait-il ce que S fera plus tard, ou ce que S a fait avant ? Réessaie."),
              "2": rep("الجواب هو y de S de t moins tau. M كدير اللي دارت S قبل tau.",
                       "Réponse : y_M(t) = y_S(t − τ) : M refait ce que S faisait τ plus tôt.")},
        "1": {"1": rep("قريب! ولكن M بعيدة على S: la perturbation كتاخد الوقت باش توصل. عاود اختار.",
                       "M est loin de S : la perturbation met du temps pour arriver. Réessaie."),
              "2": rep("الجواب هو y de S de t moins tau. بلا tau، M وS كيتحركو فنفس الوقت، وهادا غالط.",
                       "Réponse : y_M(t) = y_S(t − τ) ; sans τ, M et S bougeraient en même temps.")}},
      "Le ballon M reproduit le mouvement de S avec le retard tau. On écrit ?"),
  ]}]},
  "similaire": {
    "id": "phys_ex_ch1_eau_3_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": (f"Même expérience dans une autre cuve. La ride dure θ, le ballon M est à SM = {cm(SMb)} cm de S. Les figures 1 et 2 sont "
                f"des coupes de la surface aux dates t₁ = {fr(T1b)} s et t₂ = {fr(T2b)} s ; la figure 3 donne y_S(t)."),
      "intro_dit": (f"نفس التجربة، بقيم أخرى. SM égale {mots(SMb * 100)} centimètres، t un égale {mots(T1b)} seconde، "
                    f"وt deux égale {mots(T2b)} seconde."),
      "figures": [coupe(Vb, THb, Ab, T1b, f"Figure 1 : coupe à t₁ = {fr(T1b)} s", rmax=40),
                  coupe(Vb, THb, Ab, T2b, f"Figure 2 : coupe à t₂ = {fr(T2b)} s", ballon=SMb, rmax=40),
                  courbe_source(THb, Ab, "Figure 3 : élongation y_S(t) de la source", tmax=0.4)],
      "donnees": [f"t₁ = {fr(T1b)} s ; t₂ = {fr(T2b)} s", f"SM = {cm(SMb)} cm"],
      "questions": [
        {"id": "1", "texte": "L'onde est-elle transversale ou longitudinale ? Justifier.",
         "reponse": phrase("Transversale : la surface (le ballon) bouge verticalement, l'onde se propage horizontalement : directions perpendiculaires."),
         "clavier": {"aides": ["perpendiculaire", "direction de propagation"], "pieges": ["parallèle"]},
         "correction": correction([("1 : perturbation verticale, propagation horizontale : perpendiculaires, onde transversale", "إذن l'onde transversale")],
                                  "الكورة كطلع وكتهبط، وla ride كتمشي أفقيا. perpendiculaires، إذن l'onde transversale.")},
        {"id": "2", "texte": "Déterminer la célérité v de l'onde.",
         "reponse": valeur("v", VVb, "m/s", f"v = (r₂ − r₁)/(t₂ − t₁) = ({fr(R2b)} − {fr(R1b)})/({fr(T2b)} − {fr(T1b)}) = {fr(VVb)} m/s"),
         "clavier": {"aides": ["v = d/Δt", "r₂ − r₁", "t₂ − t₁"], "pieges": ["v = r₂/(t₂ − t₁)"]},
         "correction": correction([(f"2 : r₁ = {cm(R1b)} cm, r₂ = {cm(R2b)} cm ; v = (r₂ − r₁)/(t₂ − t₁) = {fr(R2b - R1b)}/{fr(T2b - T1b)} = {fr(VVb)} m/s", "v égale r deux moins r un")],
                                  f"v égale r deux moins r un، sur t deux moins t un، c'est-à-dire {mots(R2b - R1b)} sur {mots(T2b - T1b)}. v égale {mots(VVb)} mètre par seconde.")},
        {"id": "3", "texte": "Lire la longueur L de la perturbation sur la figure 2, puis en déduire sa durée θ.",
         "reponse": valeur("θ", THcb, "s", f"L = {cm(R2b)} − {cm(R2b - Lb)} = {cm(Lb)} cm ; θ = L/v = {fr(Lb)}/{fr(VVb)} = {fr(THcb)} s"),
         "clavier": {"aides": ["θ = L/v", "L"], "pieges": ["θ = v/L"]},
         "correction": correction([(f"3 : L = {cm(Lb)} cm = {fr(Lb)} m ; θ = L/v = {fr(Lb)}/{fr(VVb)} = {fr(THcb)} s", "teta égale L sur v")],
                                  f"L égale {mots(Lb * 100)} centimètres. teta égale L sur v، c'est-à-dire {mots(Lb)} sur {mots(VVb)}. teta égale {mots(THcb)} seconde.")},
        {"id": "4", "texte": "Calculer le retard τ du ballon. À t₂, a-t-il commencé à bouger ?",
         "reponse": valeur("τ", TAUb, "s", f"τ = SM/v = {fr(SMb)}/{fr(VVb)} = {fr(TAUb)} s"),
         "clavier": {"aides": ["τ = SM/v"], "pieges": ["τ = v/SM"]},
         "correction": correction([(f"4 : τ = SM/v = {fr(SMb)}/{fr(VVb)} = {fr(TAUb)} s ; t₂ < τ : le ballon est encore au repos.", "tau égale SM sur v")],
                                  f"tau égale SM sur v، c'est-à-dire {mots(SMb)} sur {mots(VVb)}. tau égale {mots(TAUb)} seconde. وt deux صغر من tau، إذن الكورة مازال فالراحة.")},
        {"id": "5", "texte": f"Déterminer l'élongation y_M du ballon à la date t₃ = {fr(T3b)} s.",
         "reponse": valeur("y_M", Y3b, "mm", f"y_M(t₃) = y_S(t₃ − τ) = y_S({fr(U3b)}) = {fr(Y3b)} mm"),
         "clavier": {"aides": ["y_M(t) = y_S(t − τ)", "mm"], "pieges": ["y_M(t) = y_S(t + τ)"]},
         "correction": correction([(f"5 : y_M(t₃) = y_S(t₃ − τ) = y_S({fr(U3b)} s) = {fr(Y3b)} mm : le ballon est au plus bas.", "y de M de t trois")],
                                  f"y de M de t trois égale y de S de t trois moins tau، c'est-à-dire y de S de {mots(U3b)}. "
                                  f"على la figure trois، égale {mots(Y3b)} millimètres: الكورة فالتحت.")}
      ]}}
}

ecrire(EX)
