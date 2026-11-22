# Exercice de physique, ch. 2 (ondes mécaniques progressives périodiques) — niveau facile.
# Une corde reliée à un vibreur : T lue sur y_M(t), N = 1/T, λ lue sur l'aspect, v = λ·N.
#
# Sources comparées (skill exercices § 2) :
# - exploration ondes_mecaniques_periodiques.json : cas_types « periode_elongation », « lambda_aspect », « celerite_lambda_N » ;
#   pièges « lit λ sur un axe en temps », « deux points pareils : même hauteur ET même sens », « confond T et τ » ;
#   erreurs_examen 2022 R Q1–Q4 (lit le retard à la place de la période). experience_profs.json : pas d'entrée pour ce chapitre.
# - vidéos des profs (sources.videos de l'exploration) : AdrarPhysic et Ridouan (lecture de T et de λ, « deux points pareils »),
#   TOP PHYSIQUE CHIMIE (T, λ, v = λ·N sur la corde), Laksabi (rédaction relation → A.N. → unité).
# - nationaux comparés : 2022 R ex. 2 partie 1 (y_M(t) d'une cuve, N = 50 Hz, τ, v = L/τ, λ = v/N) et 2017 N ex. II (λ sur une coupe,
#   v = λ·N). Le nôtre diffère : une corde et un vibreur, DEUX documents (film y_M(t) ET photo de la corde), T à 0,5 s et λ = 0,5 m
#   (valeurs de corde.html), le retard visible sur le film sert seulement de piège ; la chaîne est T → N → (λ, v), pas τ → v → λ.
# - séries en ligne : recherche web faite (résultats talamidi « série 3 corrigée », moutamadris « exercices 4 », alloschool
#   « activités 2 », scribd Jenkal) mais la lecture des pages est bloquée par le réseau de la session (talamidi.com, moutamadris.ma,
#   alloschool.com non résolus) : seuls les extraits de recherche ont été lus ; on s'appuie sur l'exploration et les nationaux.
import sys, os, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

CORDE = "/media/simulations/physics/ondes-periodiques-tableau/corde.html"

# ---------- nombres en mots (voix) ----------
_U = "zéro un deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize".split()
_D = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}
def _ent(n):
    n = int(n)
    if n < 17: return _U[n]
    if n < 20: return "dix-" + _U[n - 10]
    if n < 70:
        d, u = divmod(n, 10)
        return _D[d] + ("" if u == 0 else (" et un" if u == 1 else "-" + _U[u]))
    if n < 80: return "soixante" + (" et onze" if n == 71 else "-" + _ent(n - 60))
    if n < 100: return "quatre-vingts" if n == 80 else "quatre-vingt-" + _ent(n - 80)
    if n < 1000:
        c, r = divmod(n, 100)
        tete = "cent" if c == 1 else _U[c] + (" cents" if r == 0 else " cent")
        return tete if r == 0 else tete + " " + _ent(r)
    m, r = divmod(n, 1000)
    tete = "mille" if m == 1 else _ent(m) + " mille"
    return tete if r == 0 else tete + " " + _ent(r)
def mots(x, decimales=3):
    s = f"{x:.{decimales}f}".rstrip("0").rstrip(".")
    if "." not in s: return _ent(int(s))
    e, d = s.split(".")
    z = len(d) - len(d.lstrip("0"))
    return _ent(int(e)) + " virgule " + " ".join(["zéro"] * z + ([_ent(int(d.lstrip("0")))] if d.lstrip("0") else []))


def donnees(T, v, tau, longueur, A=1.0):
    """Toutes les valeurs, calculées depuis T, v (le vibreur et la corde)."""
    N = 1 / T
    lam = v * T
    return dict(T=T, N=N, v=v, lam=lam, tau=tau, L=longueur, A=A)


def film(d, tmax, pas):
    """Figure 1 : élongation y_M(t) du point M (même onde que corde.html : M part vers le haut à t = τ)."""
    T, tau, A = d["T"], d["tau"], d["A"]
    grad = [round(k * pas, 3) for k in range(int(round(tmax / pas)) + 1)]
    return {"type": "courbe", "titre": "Figure 1 : élongation y_M du point M en fonction du temps",
            "legende": "Le point M commence à vibrer à la date τ, puis il refait sans cesse le même mouvement.",
            "axes": {"x": {"min": 0, "max": tmax, "nom": "t", "unite": "s", "graduations": [[g, fr(g)] for g in grad]},
                     "y": {"min": -1.5 * A, "max": 1.5 * A, "nom": "y_M", "unite": "cm", "graduations": [[A, fr(A)], [-A, fr(-A)]]}},
            "elements": [
                {"f": "courbe", "expr": "0", "de": 0, "a": tau, "couleur": "rouge"},
                {"f": "courbe", "expr": f"{A}*sin(2*pi*(x-{tau})/{T})", "de": tau, "a": tmax, "couleur": "rouge"}]}


def photo(d, pas, t_photo_txt):
    """Figure 2 : aspect de la corde à une date où toute la corde vibre et la source S est sur une crête (comme la photo de corde.html)."""
    lam, L, A = d["lam"], d["L"], d["A"]
    grad = [round(k * pas, 3) for k in range(int(round(L / pas)) + 1)]
    return {"type": "courbe", "titre": f"Figure 2 : aspect de la corde à la date {t_photo_txt}",
            "legende": "Photo de toute la corde à un instant : l'axe horizontal porte la position x le long de la corde, à partir de S.",
            "axes": {"x": {"min": 0, "max": L, "nom": "x", "unite": "m", "graduations": [[g, fr(g)] for g in grad]},
                     "y": {"min": -1.5 * A, "max": 1.5 * A, "nom": "y", "unite": "cm", "graduations": [[A, fr(A)], [-A, fr(-A)]]}},
            "elements": [
                {"f": "courbe", "expr": f"{A}*cos(2*pi*x/{lam})", "de": 0, "a": L, "couleur": "orange"},
                {"f": "point", "at": [0, A], "t": "S", "pos": "ne", "couleur": "jaune"}]}


# ================= exercice =================
D = donnees(T=0.5, v=1.0, tau=0.75, longueur=2.0)          # valeurs de corde.html : v = 1 m/s, T = 0,5 s, M à 0,75 m
T, N, lam, v, tau = D["T"], D["N"], D["lam"], D["v"], D["tau"]
assert abs(N - 2) < 1e-9 and abs(lam - 0.5) < 1e-9 and abs(lam * N - v) < 1e-9

Ts, Ns, ls, vs, taus = fr(T), fr(N), fr(lam), fr(v), fr(tau)
Tm, Nm, lm, vm, taum = mots(T), mots(N), mots(lam), mots(v), mots(tau)
t_up1, t_up2 = tau, tau + T                                 # deux passages par zéro en montant, consécutifs
c1, c2 = lam, 2 * lam                                        # deux crêtes voisines sur la photo

Q1 = {"id": "1",
      "texte": "En exploitant la figure 1, déterminer la période T de l'onde.",
      "texte_dit": "la question un: استعمل la figure un، وحدد la période T ديال l'onde.",
      "reponse": valeur("T", T, "s", f"T = {fr(t_up2)} − {fr(t_up1)} = {Ts} s"),
      "clavier": {"aides": ["T", "s", "deux crêtes voisines", "même sens"], "pieges": [f"T = {taus} s", "λ"]},
      "aides": [
          aide("Sur la figure 1, l'axe horizontal porte le temps. Cherche deux instants où M est dans le même état : même position ET même sens de mouvement (deux crêtes voisines, ou deux passages par zéro en montant).",
               "شوف la figure un: l'axe فيه le temps. قلب على جوج لحظات اللي فيهم M عندها نفس الحالة: نفس البلاصة، ونفس الاتجاه. مثلا، les deux crêtes اللي حدا بعضياتهم."),
          aide(f"Attention : la date {taus} s où M commence à bouger est le retard τ, pas la période. T est la durée entre deux états identiques consécutifs.",
               f"رد البال: اللحظة اللي بدات فيها M تتحرك، هي le retard tau، ماشي la période. T هي المدة بين جوج حالات متشابهين، وحدة من بعد الأخرى.")],
      "correction": correction([
          (f"1 : M passe par zéro en montant à t = {fr(t_up1)} s, puis à t = {fr(t_up2)} s", "كتدوز من y égale zéro وهي طالعة"),
          (f"T = {fr(t_up2)} − {fr(t_up1)}", "T égale"),
          (f"T = {Ts} s", f"T égale {Tm} seconde")],
          f"la question un. على la figure un، M كتدوز من y égale zéro وهي طالعة، à t égale {mots(t_up1)} seconde، ومن بعد à t égale {mots(t_up2)} seconde. "
          f"إذن T égale {mots(t_up2)} moins {mots(t_up1)}. T égale {Tm} seconde."),
      "explication": "ex_v1", "facile": "fa_v1"}

Q2 = {"id": "2",
      "texte": "En déduire la fréquence N de l'onde.",
      "texte_dit": "la question deux: استنتج la fréquence N ديال l'onde.",
      "reponse": valeur("N", N, "Hz", f"N = 1/T = 1/{Ts} = {Ns} Hz"),
      "clavier": {"aides": ["N = 1/T", "T", "Hz", "A.N. :"], "pieges": ["N = T", "N = 1/λ", "s"]},
      "aides": [
          aide("La fréquence est le nombre de périodes en une seconde : combien de fois T tient-elle dans 1 s ?",
               "la fréquence هي شحال من دورة كدير M، en une seconde؟ شحال من مرة كتدخل T، en une seconde؟"),
          aide("Utilise N = 1/T, avec T en secondes ; N s'exprime en hertz (Hz).",
               "استعمل N égale un sur T، وT en seconde. la fréquence كتكون en hertz.")],
      "correction": correction([
          ("2 : N = 1/T", "N égale un sur T"),
          (f"N = 1/{Ts}", f"un sur {Tm}"),
          (f"N = {Ns} Hz", f"N égale {Nm} hertz")],
          f"la question deux. la fréquence هي l'inverse ديال la période: N égale un sur T. "
          f"l'application numérique: N égale un sur {Tm}. N égale {Nm} hertz."),
      "explication": "ex_v2", "facile": "fa_v2"}

Q3 = {"id": "3",
      "texte": "La figure 2 représente l'aspect de la corde à une date t₁. Lire la longueur d'onde λ sur cette figure, puis calculer la célérité v de l'onde.",
      "texte_dit": "la question trois: la figure deux كتبين l'aspect ديال la corde ف واحد اللحظة t un. قرا la longueur d'onde lambda على هاد la figure، ومن بعد حسب la célérité v ديال l'onde.",
      "reponse": valeur("v", v, "m/s", f"λ = {ls} m ; v = λ·N = {ls} × {Ns} = {vs} m/s"),
      "clavier": {"aides": ["λ", "v = λ·N", "m/s", "A.N. :"], "pieges": ["v = λ/N", "v = N/λ", f"λ = {fr(2 * lam)} m"]},
      "aides": [
          aide("Sur la figure 2, l'axe horizontal porte une distance x : c'est là qu'on lit λ, entre deux crêtes voisines.",
               "شوف la figure deux: l'axe فيه la distance x، en mètre. هنا كنقراو lambda، بين les deux crêtes اللي حدا بعضياتهم."),
          aide("Puis v = λ·N, avec λ en mètres et N en hertz : v en m/s.",
               "من بعد: v égale lambda fois N. lambda en mètre، وN en hertz، كنلقاو v en mètre par seconde.")],
      "correction": correction([
          (f"3 : deux crêtes voisines en x = {fr(c1)} m et x = {fr(c2)} m, donc λ = {ls} m", f"lambda égale {lm} mètre"),
          (f"v = λ·N = {ls} × {Ns}", "v égale lambda fois N"),
          (f"v = {vs} m/s", f"v égale {vm} mètre par seconde")],
          f"la question trois. على la figure deux، les deux crêtes اللي حدا بعضياتهم، à x égale {mots(c1)} mètre، et à x égale {mots(c2)} mètre. "
          f"إذن lambda égale {lm} mètre. ومن بعد: v égale lambda fois N. l'application numérique: v égale {lm} fois {Nm}. v égale {vm} mètre par seconde."),
      "explication": "ex_v3", "facile": "fa_v3"}

# ---------- explication animée (corde.html : v = 1 m/s, T = 0,5 s, N = 2 Hz, λ = 0,5 m, M à 0,75 m) ----------
m1 = (f"شوف la corde، مربوطة ب le vibreur. النقطة M بالحمر، ولتحت la courbe ديالها، y en fonction de t. "
      f"شوف M: وصلات للفوق، نبداو le chrono. كتهبط، وكترجع. هاهي رجعات لنفس الحالة: نفس البلاصة، ونفس الاتجاه. "
      f"le chrono كيقول: T égale {Tm} seconde. هادي هي la période. "
      f"ورد البال: M ما بداتش تتحرك من الأول. le front وصل ليها من بعد. هداك هو le retard tau، ماشي la période. "
      f"فالتمرين، نفس الشي: T égale {mots(t_up2)} moins {mots(t_up1)}، égale {Tm} seconde.")
m2 = (f"دابا نحسبو شحال من دورة كدير M، en une seconde. شوف M. الدورة اللولة، en {Tm} seconde. "
      f"الدورة الثانية، en {Tm} seconde أخرى. المجموع، en tout une seconde. إذن، en une seconde، M fait deux allers-retours. "
      f"هادي هي la fréquence N. la relation: N égale un sur T. "
      f"l'application numérique: N égale un sur {Tm}. N égale {Nm} hertz.")
m3 = (f"دابا ماشي الفيديو ديال M، ولكن التصويرة ديال la corde كاملة، فلحظة وحدة. شوف: la corde واقفة. "
      f"l'axe فيه la distance x، en mètre. حطينا المسطرة تحت شكل واحد، من crête حتى للcrête اللي حداها. "
      f"المسطرة كتقول: lambda égale {lm} mètre. "
      f"دابا la célérité: v égale lambda fois N. l'application numérique: {lm} fois {Nm}. "
      f"v égale {vm} mètre par seconde.")
EXPL = [
    diapo_sim("ex_v1", "Question 1 : la période, lue sur le film de M",
              "Deux états identiques consécutifs de M : T = 0,5 s (et non le retard τ).",
              CORDE + "?vue=periode", "Le film du point M et le chronomètre", m1,
              [("T = 0,5 s", f"T égale {Tm} seconde. هادي"), ("τ ≠ T", "هداك هو le retard tau")],
              [dict(mot="النقطة M بالحمر", repere="point_m"),
               dict(mot="ولتحت la courbe ديالها", repere="courbe_ym"),
               dict(mot="شوف M: وصلات للفوق", commande="play_until", parametres={"moment": "m_premier_sommet"}),
               dict(mot="هاهي رجعات لنفس الحالة", commande="play_until", parametres={"moment": "m_meme_etat"}),
               dict(mot=f"T égale {Tm} seconde. هادي", cible="centre:0"),
               dict(mot="هداك هو le retard tau", cible="centre:1")]),
    diapo_sim("ex_v2", "Question 2 : la fréquence, le nombre de périodes par seconde",
              "En une seconde, M fait deux allers-retours : N = 1/T = 2 Hz.",
              CORDE + "?vue=periode&depart=m_premier_sommet", "M compte ses allers-retours en une seconde", m2,
              [("N = 1/T", "la relation: N égale un sur T"), ("N = 1/0,5 = 2 Hz", f"N égale {Nm} hertz")],
              [dict(mot="شوف M. الدورة", repere="point_m"),
               dict(mot="الدورة اللولة", commande="play_until", parametres={"moment": "m_meme_etat"}),
               dict(mot="الدورة الثانية", commande="play_until", parametres={"moment": "m_une_seconde"}),
               dict(mot="المجموع، en tout", repere="chrono"),
               dict(mot="la relation: N égale un sur T", cible="centre:0"),
               dict(mot=f"N égale {Nm} hertz", cible="centre:1")]),
    diapo_sim("ex_v3", "Question 3 : λ sur la photo, puis v = λ·N",
              "Sur la photo, de crête à crête : λ = 0,5 m ; v = λ·N = 1 m/s.",
              CORDE + "?vue=lambda", "La photo de la corde et la règle", m3,
              [("λ = 0,5 m", f"lambda égale {lm} mètre"), ("v = λ·N = 0,5 × 2 = 1 m/s", f"v égale {vm} mètre par seconde")],
              [dict(mot="شوف: la corde واقفة", commande="play_until", parametres={"moment": "photo"}),
               dict(mot="حطينا المسطرة", repere="motif"),
               dict(mot="المسطرة كتقول", repere="regle"),
               dict(mot=f"lambda égale {lm} mètre", cible="centre:0"),
               dict(mot=f"v égale {vm} mètre par seconde", cible="centre:1")]),
]

# ---------- versions faciles ----------
FA1 = qcm_facile("fa_v1", "Plus facile : la période",
    "نتمرنو بسؤال ساهل على la figure un. اختار الجواب الصحيح.",
    f"Sur la figure 1, M commence à vibrer à t = {taus} s, puis passe par zéro en montant à t = {fr(t_up2)} s. La période vaut…",
    [f"T = {taus} s", f"T = {Ts} s", f"T = {fr(T / 2)} s"], 1, {
        "1": {"juste": rep(f"برافو! بين جوج حالات متشابهين، نفس البلاصة ونفس الاتجاه: T égale {Tm} seconde.",
                           f"Juste : entre deux passages par zéro en montant, T = {fr(t_up2)} − {fr(t_up1)} = {Ts} s.")},
        "0": {"1": rep("ما تقلقش. هاد اللحظة هي فين بدات M تتحرك. واش هادي مدة دورة كاملة؟ عاود اختار.",
                       "Cette date est le début du mouvement de M (le retard τ), pas une période. Réessaie."),
              "2": rep(f"الجواب هو T égale {Tm} seconde. la date اللي بدات فيها M هي le retard tau. la période كتقرا بين جوج حالات متشابهين.",
                       f"Réponse : T = {Ts} s. {taus} s est le retard τ ; T se lit entre deux états identiques.")},
        "2": {"1": rep("قريب! ولكن هادي غير نص الدورة: M مشات من الفوق للتحت، وما رجعاتش لنفس الحالة. عاود اختار.",
                       "Ce n'est qu'une demi-période : M n'est pas revenu au même état. Réessaie."),
              "2": rep(f"الجواب هو T égale {Tm} seconde. خاص M ترجع لنفس البلاصة، وفنفس الاتجاه.",
                       f"Réponse : T = {Ts} s (même position ET même sens).")}},
    f"Sur la figure un, M commence à vibrer à t égale {taum} seconde, puis passe par zéro en montant à t égale {mots(t_up2)} seconde. La période vaut ?")

FA2 = vf_facile("fa_v2", "Plus facile : vrai ou faux",
    "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    f"La période de l'onde est T = {Ts} s.", [
        (f"La fréquence est N = 1/T = 1/{Ts} = {Ns} Hz.", True, f"N = 1/T : en 1 s, M fait {Ns:s} allers-retours, donc N = {Ns} Hz."),
        (f"La fréquence est N = T = {Ts} Hz.", False, f"N n'est pas T : N = 1/T = {Ns} Hz."),
        ("La fréquence s'exprime en secondes.", False, "La fréquence s'exprime en hertz (Hz) ; c'est la période qui s'exprime en secondes.")])

# association : chaque grandeur et sa valeur (une valeur en trop : 0,5 s)
G = [("1", "λ, lue sur la figure 2"), ("2", "N, la fréquence"), ("3", "v, la célérité")]
Dr = [("a", f"{ls} m"), ("b", f"{Ns} Hz"), ("c", f"{vs} m/s"), ("d", f"{Ts} s")]
COUPLES = {"1": "a", "2": "b", "3": "c"}
R = {
    "1-a": (True, f"Oui : sur la photo, de crête à crête, λ = {ls} m (une distance).", f"برافو: على التصويرة، من crête ل crête، lambda égale {lm} mètre."),
    "1-b": (False, "Non : λ est une longueur, en mètres. Cherche une valeur en m.", "لا: lambda هي مسافة، en mètre. قلب على valeur en mètre."),
    "1-c": (False, "Non : m/s est l'unité d'une célérité. λ est une distance.", "لا: mètre par seconde هي الوحدة ديال la célérité. lambda هي مسافة."),
    "1-d": (False, "Non : 0,5 s est la période T, lue sur un axe en temps. λ se lit sur l'axe des x, en m.", "لا: هادي هي la période T، en seconde. lambda كتقرا على l'axe ديال x، en mètre."),
    "2-a": (False, "Non : la fréquence s'exprime en hertz, pas en mètres.", "لا: la fréquence كتكون en hertz، ماشي en mètre."),
    "2-b": (True, f"Oui : N = 1/T = 1/{Ts} = {Ns} Hz.", f"برافو: N égale un sur T، égale {Nm} hertz."),
    "2-c": (False, "Non : m/s est l'unité d'une célérité. N est en hertz.", "لا: mètre par seconde هي ديال la célérité. N كتكون en hertz."),
    "2-d": (False, "Non : 0,5 s est la période T ; la fréquence est son inverse, en hertz.", "لا: هادي هي la période. la fréquence هي l'inverse ديالها، en hertz."),
    "3-a": (False, "Non : 0,5 m est λ. La célérité est en m/s : v = λ·N.", "لا: هادي هي lambda. la célérité كتكون en mètre par seconde."),
    "3-b": (False, "Non : 2 Hz est la fréquence. La célérité se calcule : v = λ·N.", "لا: هادي هي la fréquence. la célérité كنحسبوها: v égale lambda fois N."),
    "3-c": (True, f"Oui : v = λ·N = {ls} × {Ns} = {vs} m/s.", f"برافو: v égale lambda fois N، égale {vm} mètre par seconde."),
    "3-d": (False, "Non : 0,5 s est une durée, la période. La célérité est en m/s.", "لا: هادي مدة، la période. la célérité كتكون en mètre par seconde."),
}
FA3 = assoc_facile("fa_v3", "Plus facile : chaque grandeur, sa valeur",
    "سؤال ساهل: ربط كل grandeur ب la valeur ديالها. شوف l'unité.",
    "Relie chaque grandeur à sa valeur (une valeur est en trop).",
    "Relie chaque grandeur à sa valeur.", G, Dr, COUPLES, R,
    (f"(1 ; a) (2 ; b) (3 ; c). La valeur {Ts} s est la période T, lue sur la figure 1.",
     f"الجواب: lambda égale {lm} mètre، N égale {Nm} hertz، وv égale {vm} mètre par seconde. و T égale {Tm} seconde، هادي la période."))

# ================= exercice semblable =================
D2 = donnees(T=0.2, v=1.5, tau=0.4, longueur=1.2)
T2, N2, l2, v2, tau2 = D2["T"], D2["N"], D2["lam"], D2["v"], D2["tau"]
assert abs(N2 - 5) < 1e-9 and abs(l2 - 0.3) < 1e-9
u1, u2 = tau2, tau2 + T2
k1, k2 = l2, 2 * l2
SIM_Q = [
    {"id": "1", "texte": "En exploitant la figure 1, déterminer la période T de l'onde.",
     "reponse": valeur("T", T2, "s", f"T = {fr(u2)} − {fr(u1)} = {fr(T2)} s"),
     "clavier": {"aides": ["T", "s", "deux crêtes voisines", "même sens"], "pieges": [f"T = {fr(tau2)} s", "λ"]},
     "correction": correction([
         (f"1 : M passe par zéro en montant à t = {fr(u1)} s puis à t = {fr(u2)} s", "كتدوز من y égale zéro وهي طالعة"),
         (f"T = {fr(u2)} − {fr(u1)} = {fr(T2)} s", f"T égale {mots(T2)} seconde")],
         f"la question un. M كتدوز من y égale zéro وهي طالعة، à t égale {mots(u1)} seconde، ومن بعد à t égale {mots(u2)} seconde. إذن T égale {mots(T2)} seconde.")},
    {"id": "2", "texte": "En déduire la fréquence N de l'onde.",
     "reponse": valeur("N", N2, "Hz", f"N = 1/T = 1/{fr(T2)} = {fr(N2)} Hz"),
     "clavier": {"aides": ["N = 1/T", "T", "Hz", "A.N. :"], "pieges": ["N = T", "s"]},
     "correction": correction([("2 : N = 1/T", "N égale un sur T"), (f"N = 1/{fr(T2)} = {fr(N2)} Hz", f"N égale {mots(N2)} hertz")],
         f"la question deux. N égale un sur T. l'application numérique: N égale un sur {mots(T2)}. N égale {mots(N2)} hertz.")},
    {"id": "3", "texte": "Lire la longueur d'onde λ sur la figure 2, puis calculer la célérité v de l'onde.",
     "reponse": valeur("v", v2, "m/s", f"λ = {fr(l2)} m ; v = λ·N = {fr(l2)} × {fr(N2)} = {fr(v2)} m/s"),
     "clavier": {"aides": ["λ", "v = λ·N", "m/s", "A.N. :"], "pieges": ["v = λ/N", f"λ = {fr(2 * l2)} m"]},
     "correction": correction([
         (f"3 : deux crêtes voisines en x = {fr(k1)} m et x = {fr(k2)} m, donc λ = {fr(l2)} m", f"lambda égale {mots(l2)} mètre"),
         (f"v = λ·N = {fr(l2)} × {fr(N2)} = {fr(v2)} m/s", f"v égale {mots(v2)} mètre par seconde")],
         f"la question trois. les deux crêtes اللي حدا بعضياتهم، à x égale {mots(k1)} mètre، et à x égale {mots(k2)} mètre. إذن lambda égale {mots(l2)} mètre. "
         f"v égale lambda fois N. l'application numérique: v égale {mots(l2)} fois {mots(N2)}. v égale {mots(v2)} mètre par seconde.")},
]

EX = {
  "id": "phys_ex_ch2_vibreur_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques_periodiques", "cours": "phys_ch2_ondes_periodiques",
  "titre": "Une corde reliée à un vibreur : T, N, λ et v", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Lire la période T sur y_M(t)", "Calculer la fréquence N = 1/T", "Lire λ sur l'aspect du milieu", "Calculer la célérité v = λ·N"],
  "enonce": {
    "intro": ("L'extrémité S d'une corde élastique horizontale est reliée à un vibreur qui lui impose, à partir de la date t = 0, "
              "un mouvement vertical sinusoïdal. Une onde progressive périodique se propage le long de la corde, sans amortissement "
              "et sans réflexion. La figure 1 donne l'élongation y_M d'un point M de la corde en fonction du temps. "
              "La figure 2 donne l'aspect de la corde à une date t₁ où toute la corde vibre."),
    "intro_dit": ("دابا نقراو l'énoncé. عندنا une corde élastique أفقية، والطرف ديالها S مربوط ب le vibreur. "
                  "من t égale zéro، le vibreur كيحرك S للفوق ولتحت، mouvement sinusoïdal. "
                  "une onde progressive périodique كتمشي فوق la corde، بلا ما تضعاف، وبلا ما ترجع. "
                  "la figure un فيها y de M en fonction de t: الفيديو ديال النقطة M. "
                  "la figure deux فيها l'aspect ديال la corde ف واحد اللحظة t un: التصويرة ديال la corde كاملة."),
    "figures": [film(D, 2.0, 0.25), photo(D, 0.25, "t₁")],
    "donnees": ["Figure 1 : y_M(t), axe des temps en s", "Figure 2 : aspect de la corde, axe des x en m (x mesuré depuis S)"],
    "questions": [Q1, Q2, Q3]},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPL}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [FA1, FA2, FA3]}]},
  "similaire": {
    "id": "phys_ex_ch2_vibreur_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": ("Un vibreur impose à l'extrémité S d'une corde un mouvement sinusoïdal à partir de t = 0. La figure 1 donne "
                "l'élongation y_M d'un point M de la corde en fonction du temps ; la figure 2 donne l'aspect de la corde à une date t₁."),
      "intro_dit": ("نفس التمرين، بقيم أخرى. le vibreur كيحرك S من t égale zéro. la figure un فيها y de M en fonction de t، "
                    "وla figure deux فيها l'aspect ديال la corde ف واحد اللحظة t un."),
      "figures": [film(D2, 1.2, 0.1), photo(D2, 0.15, "t₁")],
      "donnees": ["Figure 1 : y_M(t), axe des temps en s", "Figure 2 : aspect de la corde, axe des x en m"],
      "questions": SIM_Q}},
}
ecrire(EX)
