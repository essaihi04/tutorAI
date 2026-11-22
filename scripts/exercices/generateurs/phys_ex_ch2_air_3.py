# Exercice de physique, ch. 2 (ondes mécaniques progressives périodiques) — niveau moyen.
# Un haut-parleur et deux microphones : T sur l'oscillogramme (sensibilité), N, premier retour en phase → λ, v = λ·N,
# puis un microphone à une distance donnée : en phase ou en opposition ? (justifier).
#
# Sources comparées (skill exercices § 2) :
# - exploration ondes_mecaniques_periodiques.json : cas_types « deux_recepteurs » (devoir le plus fréquent, 5 profs ; « de
#   nouveau en phase pour la première fois »), « periode_elongation » (T = n × S_H), « celerite_lambda_N », « phase_opposition » ;
#   pièges « T = 5 sans la sensibilité », « confond ms et µs », « pour la première fois = un seul λ », « λ laissée en cm dans
#   v = λ·N », « virgule → opposition » ; valeurs repères (son : 340 m/s, 20 Hz–20 kHz ; 2000 Hz ↔ T = 0,5 ms).
#   experience_profs.json : pas d'entrée pour ce chapitre.
# - vidéos des profs : Driss (devoir des deux récepteurs à ultrasons, détaillé), Ridouan (montage des deux micros ; son
#   exercice incohérent T = 25 µs / « haut-parleur » non repris), mouhibi (deux micros), TOP PHYSIQUE CHIMIE (deux micros).
# - nationaux comparés : 2024 R ex. 2 (deux microphones, mais SALVES de son, retard τ = 4 div × 0,5 ms, distance ℓ de l'émetteur :
#   pas de λ ni de phase) ; 2022 R ex. 2 partie 1 (T et N lus sur y_M(t), λ = v/N). Le nôtre : son CONTINU de 2000 Hz, deux
#   microphones d'abord côte à côte, déplacement de M₂ jusqu'au premier retour en phase → λ, v = λ·N comparée à 340 m/s,
#   puis l'état vibratoire d'un microphone placé à 59,5 cm : chaîne absente des nationaux du dépôt.
# - séries en ligne : recherche web faite (extraits moutamadris « exercices 4 » : distance pour laquelle les deux signaux sont
#   de nouveau en phase, v = 340 m/s ; talamidi « série 3 corrigée » : distance minimale pour remettre deux signaux en phase ;
#   Google Docs : deux microphones au même endroit, courbes en phase ; alloschool El Goufifa ; scribd Jenkal) ; la lecture des
#   pages est bloquée par le réseau de la session : seuls les extraits ont été lus, nos données sont les nôtres.
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

BASE = "/media/simulations/physics/ondes-periodiques-tableau/"
OSCILLO = BASE + "national.html?vue=oscillo"          # S_H = 0,1 ms/div, une période = 5 div, T = 0,5 ms, N = 2000 Hz
RECEPT = BASE + "recepteurs.html?vue=reculer"         # ultrasons 40 kHz, λ = 8,5 mm (le même geste : reculer R₂)
AIR = BASE + "air.html?vue=comparaison"               # son dans l'air : 2000 Hz → λ = 17 cm, v = 340 m/s

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


def calculs(SH_ms, ndiv, d1_cm, d2_cm):
    T_ms = ndiv * SH_ms
    T = T_ms * 1e-3
    N = 1 / T
    lam = d1_cm / 100
    v = lam * N
    q = d2_cm / d1_cm
    entier = abs(q - round(q)) < 1e-9
    demi = abs(q - int(q) - 0.5) < 1e-9
    etat = "en phase" if entier else ("en opposition de phase" if demi else "ni en phase ni en opposition")
    return dict(SH=SH_ms, n=ndiv, T_ms=T_ms, T=T, N=round(N, 6), d1=d1_cm, lam=lam, v=round(v, 6), d2=d2_cm, q=q, etat=etat, entier=entier)


def montage():
    """Figure 1 : le haut-parleur, les deux microphones sur son axe, M₂ que l'on éloigne."""
    return {"type": "schema", "titre": "Figure 1 : le montage", "cadre": {"l": 10, "h": 4},
            "legende": "M₁ reste fixe ; on éloigne M₂ du haut-parleur, le long de l'axe. Les deux microphones sont reliés aux voies A et B d'un oscilloscope.",
            "elements": [
                {"f": "rect", "de": [0.2, 1.4], "a": [1.4, 2.6], "couleur": "blanc", "arrondi": True},
                {"f": "texte", "at": [0.8, 2.85], "t": "GBF", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
                {"f": "ligne", "pts": [[1.4, 2.0], [2.0, 2.0]], "couleur": "faible"},
                {"f": "ligne", "pts": [[2.0, 1.6], [2.4, 1.6], [2.9, 1.1], [2.9, 2.9], [2.4, 2.4], [2.0, 2.4]], "ferme": True, "couleur": "jaune"},
                {"f": "texte", "at": [2.45, 3.25], "t": "haut-parleur", "couleur": "jaune", "ancre": "centre", "taille": "petit"},
                {"f": "ligne", "pts": [[2.9, 2.0], [9.8, 2.0]], "couleur": "faible", "trait": "pointille"},
                {"f": "cercle", "c": [4.5, 2.0], "r": 0.22, "couleur": "cyan"},
                {"f": "texte", "at": [4.5, 2.55], "t": "M₁", "couleur": "cyan", "ancre": "centre"},
                {"f": "cercle", "c": [7.5, 2.0], "r": 0.22, "couleur": "orange"},
                {"f": "texte", "at": [7.5, 2.55], "t": "M₂", "couleur": "orange", "ancre": "centre"},
                {"f": "fleche", "de": [7.9, 2.0], "a": [9.2, 2.0], "couleur": "orange", "texte": "on éloigne M₂", "pos": "n"},
                {"f": "cote", "de": [4.5, 1.0], "a": [7.5, 1.0], "t": "d = M₁M₂", "couleur": "blanc", "pos": "s"},
                {"f": "texte", "at": [6.0, 0.2], "t": "M₁ → voie A ; M₂ → voie B de l'oscilloscope", "couleur": "faible", "ancre": "centre", "taille": "petit"}]}


def oscillogramme(C):
    """Figure 2 : écran 10 × 8 divisions, M₁ et M₂ côte à côte : deux sinusoïdes en phase, crêtes sur les traits verticaux."""
    P = C["n"]
    el = []
    for i in range(11):
        el.append({"f": "ligne", "pts": [[i, 0], [i, 8]], "couleur": "faible"})
    for j in range(9):
        el.append({"f": "ligne", "pts": [[0, j], [10, j]], "couleur": "faible"})
    ph = P / 4 - 1                      # la première crête tombe sur le trait x = 1 division
    el += [
        {"f": "courbe", "expr": f"4+2.6*sin(2*pi*(x+{ph})/{P})", "de": 0, "a": 10, "couleur": "cyan"},
        {"f": "courbe", "expr": f"4+1.6*sin(2*pi*(x+{ph})/{P})", "de": 0, "a": 10, "couleur": "orange"},
        {"f": "texte", "at": [0.15, 7.35], "t": "voie A (M₁)", "couleur": "cyan", "taille": "petit"},
        {"f": "texte", "at": [0.15, 0.35], "t": "voie B (M₂)", "couleur": "orange", "taille": "petit"},
        {"f": "texte", "at": [9.85, 7.35], "t": f"S_H = {fr(C['SH'])} ms/div", "couleur": "jaune", "ancre": "droite", "taille": "petit"}]
    return {"type": "schema", "titre": "Figure 2 : oscillogrammes, M₁ et M₂ côte à côte", "cadre": {"l": 10, "h": 8},
            "legende": "Écran de 10 × 8 divisions. Sensibilité horizontale : " + f"{fr(C['SH'])} ms par division.",
            "elements": el}


C = calculs(SH_ms=0.1, ndiv=5, d1_cm=17, d2_cm=59.5)
assert abs(C["N"] - 2000) < 1e-6 and abs(C["v"] - 340) < 1e-6 and C["etat"] == "en opposition de phase"
SHs, Tms, Ns, ls, vs = fr(C["SH"]), fr(C["T_ms"]), fr(C["N"], 0), fr(C["lam"]), fr(C["v"], 0)
SHm, Tmm, Nm, lm, vm = mots(C["SH"]), mots(C["T_ms"]), mots(C["N"]), mots(C["lam"]), mots(C["v"])
n, d1, d2, q = C["n"], C["d1"], C["d2"], C["q"]

Q1 = {"id": "1",
      "texte": "En exploitant la figure 2, déterminer la période T du son, en ms.",
      "texte_dit": "la question un: استعمل la figure deux، وحدد la période T ديال le son، en milliseconde.",
      "reponse": valeur("T", C["T_ms"], "ms", f"T = n·S_H = {n} × {SHs} = {Tms} ms"),
      "clavier": {"aides": ["T = n·S_H", "S_H", "div", "ms", "A.N. :"], "pieges": [f"T = {n} ms", f"T = {SHs} ms"]},
      "aides": [
          aide("Sur une même courbe, compte les divisions entre deux crêtes voisines : c'est une période.",
               "على نفس la courbe، حسب les divisions بين les deux crêtes اللي حدا بعضياتهم. هادي دورة وحدة."),
          aide("Puis T = nombre de divisions × sensibilité horizontale ; garde l'unité ms de la sensibilité.",
               "من بعد: T égale le nombre de divisions، fois la sensibilité horizontale. والوحدة هي la milliseconde.")],
      "correction": correction([
          (f"1 : une période occupe n = {n} divisions", f"une période، c'est {mots(n)} divisions"),
          ("T = n·S_H", "T égale n fois la sensibilité horizontale"),
          (f"T = {n} × {SHs} = {Tms} ms", f"T égale {Tmm} milliseconde")],
          f"la question un. بين les deux crêtes اللي حدا بعضياتهم، une période، c'est {mots(n)} divisions. "
          f"T égale n fois la sensibilité horizontale. l'application numérique: T égale {mots(n)} fois {SHm}. T égale {Tmm} milliseconde."),
      "explication": "ex_a1", "facile": "fa_a1"}

Q2 = {"id": "2",
      "texte": "En déduire la fréquence N du son.",
      "texte_dit": "la question deux: استنتج la fréquence N ديال le son.",
      "reponse": valeur("N", C["N"], "Hz", f"N = 1/T = 1/({sci(C['T'])} s) = {Ns} Hz"),
      "clavier": {"aides": ["N = 1/T", "10⁻³", "s", "Hz", "A.N. :"], "pieges": [f"N = 1/{Tms} = {fr(1 / C['T_ms'])} Hz", "N = T"]},
      "aides": [
          aide("Avant de calculer N, convertis T en secondes : 1 ms = 10⁻³ s.",
               "قبل ما تحسب N، حول T en seconde: une milliseconde égale dix puissance moins trois seconde."),
          aide("Puis N = 1/T, avec T en s : N en hertz.",
               "من بعد: N égale un sur T، وT en seconde. N كتخرج en hertz.")],
      "correction": correction([
          (f"2 : T = {Tms} ms = {sci(C['T'])} s", "نحولو T"),
          ("N = 1/T", "N égale un sur T"),
          (f"N = 1/({sci(C['T'])}) = {Ns} Hz", f"N égale {Nm} hertz")],
          f"la question deux. نحولو T: {Tmm} milliseconde، égale cinq fois dix puissance moins quatre seconde. "
          f"N égale un sur T. l'application numérique: N égale un sur cinq fois dix puissance moins quatre. N égale {Nm} hertz."),
      "explication": "ex_a2", "facile": "fa_a2"}
assert abs(C["T"] - 5e-4) < 1e-12      # la parole de Q2 dit « cinq fois dix puissance moins quatre »

Q3 = {"id": "3",
      "texte": f"Au départ, M₁ et M₂ sont côte à côte : les deux courbes sont en phase (figure 2). On éloigne M₂ ; les deux courbes sont de nouveau en phase, pour la première fois, lorsque M₁M₂ = d₁ = {fr(d1)} cm. Justifier que la longueur d'onde est λ = d₁.",
      "texte_dit": f"la question trois: فاللول، M un وM deux حدا بعضياتهم، وles deux courbes en phase. كنبعدو M deux. les deux courbes كيرجعو en phase، لأول مرة، ملي M un M deux égale d un، égale {mots(d1)} centimètres. برر بلي lambda égale d un.",
      "reponse": phrase(f"Deux points voisins qui vibrent en phase sont séparés par λ. Les courbes sont de nouveau en phase pour la première fois : M₂ a reculé d'une seule longueur d'onde, donc λ = d₁ = {fr(d1)} cm = {ls} m."),
      "clavier": {"aides": ["en phase", "pour la première fois", "λ", "d = k·λ", "k = 1"], "pieges": ["λ = d₁/2", "λ = 2·d₁"]},
      "aides": [
          aide("Que veut dire « de nouveau en phase pour la première fois » ? M₂ vibre de nouveau comme M₁, et c'est le premier point où cela arrive.",
               "شنو معنى en phase لأول مرة؟ M deux رجعات كدير بحال M un، وهادي أول بلاصة فين كيوقع هادشي."),
          aide("Deux points du milieu qui vibrent en phase et qui sont les plus proches sont séparés de λ (d = k·λ avec k = 1).",
               "جوج نقط اللي vibrent en phase، وأقرب وحدة للأخرى، بيناتهم lambda: d égale k fois lambda، avec k égale un.")],
      "correction": correction([
          ("3 : en phase : d = k·λ", "d égale k fois lambda"),
          ("première fois : k = 1", "k égale un"),
          (f"donc λ = d₁ = {fr(d1)} cm = {ls} m", f"lambda égale d un، égale {mots(d1)} centimètres")],
          f"la question trois. جوج نقط اللي vibrent en phase: d égale k fois lambda. "
          f"لأول مرة، c'est k égale un. إذن lambda égale d un، égale {mots(d1)} centimètres، égale {lm} mètre."),
      "explication": "ex_a3", "facile": "fa_a3"}

Q4 = {"id": "4",
      "texte": "Calculer la célérité v du son dans l'air.",
      "texte_dit": "la question quatre: حسب la célérité v ديال le son فالهوا.",
      "reponse": valeur("v", C["v"], "m/s", f"v = λ·N = {ls} × {Ns} = {vs} m/s"),
      "clavier": {"aides": ["v = λ·N", "λ en m", "m/s", "A.N. :"], "pieges": [f"v = {fr(d1)} × {Ns}", "v = λ/N"]},
      "aides": [
          aide("Tu connais λ (question 3) et N (question 2). Mets λ en mètres.",
               "عندك lambda من la question trois، وN من la question deux. حط lambda en mètre."),
          aide("v = λ·N, λ en m et N en Hz : v en m/s. Compare à la valeur connue du son dans l'air.",
               "v égale lambda fois N. lambda en mètre، وN en hertz، كتخرج v en mètre par seconde.")],
      "correction": correction([
          ("4 : v = λ·N", "v égale lambda fois N"),
          (f"v = {ls} × {Ns}", f"{lm} fois {Nm}"),
          (f"v = {vs} m/s : c'est bien la célérité du son dans l'air", f"v égale {vm} mètres par seconde")],
          f"la question quatre. v égale lambda fois N. l'application numérique: v égale {lm} fois {Nm}. "
          f"v égale {vm} mètres par seconde. هادي هي la célérité ديال le son فالهوا."),
      "explication": "ex_a4", "facile": "fa_a4"}

Q5 = {"id": "5",
      "texte": f"On place M₂ à la distance M₁M₂ = d₂ = {fr(d2)} cm de M₁. Les deux courbes sont-elles en phase ou en opposition de phase ? Justifier.",
      "texte_dit": f"la question cinq: كنحطو M deux، à d deux égale {mots(d2)} centimètres من M un. واش les deux courbes en phase، ولا en opposition de phase؟ برر.",
      "reponse": phrase(f"d₂/λ = {fr(d2)}/{fr(d1)} = {fr(q)} = {int(q)} + 1/2 : un entier et demi. Donc d₂ = (2k + 1)·λ/2 avec k = {int(q)} : M₁ et M₂ vibrent en opposition de phase."),
      "clavier": {"aides": ["d₂/λ", "même unité", "d = (2k + 1)·λ/2", "entier et demi"], "pieges": ["d = k·λ", "en phase"]},
      "aides": [
          aide("Compare d₂ à λ dans la même unité : calcule d₂/λ.",
               "قارن d deux مع lambda، بنفس الوحدة: حسب d deux sur lambda."),
          aide("Un entier : en phase. Un entier et demi (0,5 ; 1,5 ; 2,5 ; 3,5…) : en opposition de phase. Sinon, ni l'un ni l'autre.",
               "يلا لقيتي عدد صحيح: en phase. يلا لقيتي عدد صحيح ونص: en opposition de phase. وغير هادشي: لا هادي لا هادي.")],
      "correction": correction([
          (f"5 : d₂/λ = {fr(d2)}/{fr(d1)} = {fr(q)}", "d deux sur lambda"),
          (f"{fr(q)} = {int(q)} + 1/2 : d₂ = (2k + 1)·λ/2 avec k = {int(q)}", "un nombre entier et demi"),
          ("les deux courbes sont en opposition de phase", "en opposition de phase. ")],
          f"la question cinq. d deux sur lambda: {mots(d2)} sur {mots(d1)}، égale {mots(q)}. "
          f"{mots(q)}، c'est un nombre entier et demi. إذن d deux égale deux k plus un, fois lambda sur deux، avec k égale {mots(int(q))}. "
          f"donc M un et M deux vibrent en opposition de phase. ملي la courbe A فالفوق، la courbe B لتحت."),
      "explication": "ex_a5", "facile": "fa_a5"}

# ---------- explication animée ----------
m1 = (f"هادي الشاشة ديال l'oscilloscope. شوف: la courbe ديال la voie un كتبان، ومن بعد la voie deux. "
      f"la sensibilité horizontale égale {SHm} milliseconde par division. "
      f"أولا، ناخدو les deux crêtes اللي حدا بعضياتهم ف la voie un. ثانيا، كنحسبو les divisions: une, deux, trois, quatre, cinq. "
      f"la relation: T égale le nombre de divisions، fois la sensibilité horizontale. "
      f"l'application numérique: T égale {mots(n)} fois {SHm}، égale {Tmm} milliseconde. "
      f"هي نفس القيم ديال التمرين.")
m2 = (f"نكملو على نفس الشاشة. T égale {Tmm} milliseconde. قبل ما نحسبو N، كنحولو للسيكوند: "
      f"T égale cinq fois dix puissance moins quatre seconde. "
      f"la relation: N égale un sur T. l'application numérique: N égale un sur cinq fois dix puissance moins quatre. "
      f"N égale {Nm} hertz. تحقق: هاد le son كيتسمع، حيت N كاينة entre vingt hertz et vingt kilohertz.")
m3 = (f"هنا نفس الطريقة، ولكن ب les ultrasons. R un ثابت، وكنبعدو R deux. فاللول، R un وR deux حدا بعضياتهم: les deux courbes en phase. "
      f"كنبعدو R deux: la courbe ديالو كتمشي. كتولي en opposition de phase. ومن بعد كترجع en phase، لأول مرة. "
      f"المسطرة كتقول: lambda égale huit virgule cinq millimètres. هادي هي lambda ديال les ultrasons، حيت جوج نقط اللي vibrent en phase وحدا بعضياتهم، بيناتهم lambda. "
      f"فالتمرين، نفس الشي مع le son: الرجوع الأول en phase، c'est d un égale {mots(d1)} centimètres. إذن lambda égale d un.")
m4 = (f"دابا فالهوا. هاد le haut-parleur كيعطي le son. الخطوط اللي كتشوف، هوما البلايص اللي فيهم الهوا مجموع. "
      f"en deux mille hertz، lambda égale dix-sept centimètres، بحال التمرين. "
      f"la relation: v égale lambda fois N. نحولو lambda: dix-sept centimètres، égale zéro virgule dix-sept mètre. "
      f"l'application numérique: v égale zéro virgule dix-sept fois deux mille. v égale trois cent quarante mètres par seconde. "
      f"هادي هي la célérité ديال le son فالهوا.")
assert C["N"] == 2000 and d1 == 17 and C["v"] == 340      # m4 lit les valeurs de air.html, qui sont celles de l'exercice
m5 = (f"نرجعو ل les deux récepteurs. ملي R deux بعيد ب نص lambda، شوف الشاشة: ملي la courbe ديال R un فالفوق، la courbe ديال R deux لتحت. "
      f"هادي en opposition de phase. دابا نبعدو R deux، à trois lambda sur deux. ديما en opposition de phase. "
      f"فالتمرين: d deux sur lambda، égale {mots(d2)} sur {mots(d1)}، égale {mots(q)}. "
      f"{mots(q)}، c'est trois et demi: un nombre entier et demi. إذن M un et M deux vibrent en opposition de phase.")
EXPL = [
    diapo_sim("ex_a1", "Question 1 : la période sur l'oscillogramme",
              "Une période = 5 divisions ; T = n·S_H = 5 × 0,1 ms = 0,5 ms.",
              OSCILLO, "Oscillogramme à deux voies, 0,1 ms par division", m1,
              [("T = n·S_H", "la relation: T égale"), ("T = 5 × 0,1 = 0,5 ms", f"égale {Tmm} milliseconde. ")],
              [dict(mot="هادي الشاشة", repere="ecran"),
               dict(mot="شوف: la courbe ديال", commande="play_until", parametres={"moment": "trace"}),
               dict(mot="la sensibilité horizontale égale", repere="sensibilite"),
               dict(mot="أولا، ناخدو", commande="play_until", parametres={"moment": "cretes"}),
               dict(mot="ثانيا، كنحسبو", commande="play_until", parametres={"moment": "divisions"}),
               dict(mot="la relation: T égale", commande="play_until", parametres={"moment": "relation"}),
               dict(mot="la relation: T égale", cible="centre:0"),
               dict(mot="l'application numérique: T", commande="play_until", parametres={"moment": "periode"}),
               dict(mot=f"égale {Tmm} milliseconde. ", cible="centre:1")]),
    diapo_sim("ex_a2", "Question 2 : la fréquence, avec T en secondes",
              "T = 0,5 ms = 5 × 10⁻⁴ s ; N = 1/T = 2000 Hz.",
              OSCILLO, "Le même oscillogramme : de T à N", m2,
              [("T = 5 × 10⁻⁴ s", "T égale cinq fois dix puissance moins quatre seconde"), ("N = 1/T = 2000 Hz", f"N égale {Nm} hertz")],
              [dict(mot="نكملو على نفس الشاشة", commande="play_until", parametres={"moment": "periode"}),
               dict(mot="T égale cinq fois dix puissance moins quatre seconde", cible="centre:0"),
               dict(mot="la relation: N égale", commande="play_until", parametres={"moment": "frequence"}),
               dict(mot=f"N égale {Nm} hertz", cible="centre:1")]),
    diapo_sim("ex_a3", "Question 3 : le premier retour en phase, c'est λ",
              "On recule le récepteur : de nouveau en phase pour la première fois après un déplacement de λ.",
              RECEPT, "On recule R₂ : opposition, puis de nouveau en phase", m3,
              [("1ʳᵉ fois en phase : d = λ", "الرجوع الأول en phase"), ("λ = d₁ = 17 cm", "إذن lambda égale d un")],
              [dict(mot="R un ثابت", repere="recepteur_1"),
               dict(mot="فاللول، R un", commande="play_until", parametres={"moment": "courbes_superposees"}),
               dict(mot="كنبعدو R deux: la courbe", commande="play_until", parametres={"moment": "decalage"}),
               dict(mot="كتولي en opposition", commande="play_until", parametres={"moment": "opposition"}),
               dict(mot="ومن بعد كترجع en phase", commande="play_until", parametres={"moment": "en_phase_1"}),
               dict(mot="المسطرة كتقول", repere="regle"),
               dict(mot="الرجوع الأول en phase", cible="centre:0"),
               dict(mot="إذن lambda égale d un", cible="centre:1")]),
    diapo_sim("ex_a4", "Question 4 : la célérité du son, v = λ·N",
              "À 2000 Hz, λ = 17 cm = 0,17 m : v = 0,17 × 2000 = 340 m/s.",
              AIR, "Le son dans l'air : λ à 1000 Hz et à 2000 Hz", m4,
              [("v = λ·N", "la relation: v égale lambda fois N"), ("v = 0,17 × 2000 = 340 m/s", "v égale trois cent quarante")],
              [dict(mot="هاد le haut-parleur", repere="haut_parleur"),
               dict(mot="الخطوط اللي كتشوف", repere="compression"),
               dict(mot="en deux mille hertz", commande="play_until", parametres={"moment": "comparaison"}),
               dict(mot="lambda égale dix-sept centimètres", repere="lambda_2000"),
               dict(mot="la relation: v égale lambda fois N", cible="centre:0"),
               dict(mot="v égale trois cent quarante", cible="centre:1")]),
    diapo_sim("ex_a5", "Question 5 : un entier et demi de λ, l'opposition de phase",
              "d₂/λ = 59,5/17 = 3,5 : un entier et demi, opposition de phase.",
              RECEPT + "&depart=opposition", "R₂ à λ/2, puis à 3λ/2 : les courbes en opposition de phase", m5,
              [("d = (2k + 1)·λ/2 → opposition", "هادي en opposition de phase"), ("59,5/17 = 3,5", f"égale {mots(q)}. ")],
              [dict(mot="نرجعو ل les deux récepteurs", repere="recepteur_2"),
               dict(mot="شوف الشاشة", repere="ecran"),
               dict(mot="هادي en opposition de phase", cible="centre:0"),
               dict(mot="دابا نبعدو R deux، à trois", commande="set_parameters", parametres={"d_mm": 12.75}),
               dict(mot=f"égale {mots(q)}. ", cible="centre:1")]),
]

# ---------- versions faciles ----------
FA1 = qcm_facile("fa_a1", "Plus facile : T sur l'oscillogramme",
    "نتمرنو بسؤال ساهل. اختار الجواب الصحيح.",
    f"Une période occupe {n} divisions ; la sensibilité horizontale est {SHs} ms/div. La période vaut…",
    [f"T = {n} ms", f"T = {SHs} ms", f"T = {Tms} ms"], 2, {
        "2": {"juste": rep(f"برافو! T égale {mots(n)} fois {SHm}، égale {Tmm} milliseconde.",
                           f"Juste : T = n·S_H = {n} × {SHs} = {Tms} ms.")},
        "0": {"1": rep("ما تقلقش. هادا غير le nombre de divisions. شحال كتساوي division وحدة؟ عاود اختار.",
                       "Ce n'est que le nombre de divisions : combien vaut une division ? Réessaie."),
              "2": rep(f"الجواب هو T égale {Tmm} milliseconde: {mots(n)} divisions، fois {SHm} milliseconde par division.",
                       f"Réponse : T = {n} × {SHs} = {Tms} ms.")},
        "1": {"1": rep("قريب! هادي division وحدة. ولكن la période فيها بزاف ديال les divisions. عاود اختار.",
                       "C'est la valeur d'UNE division ; une période en contient plusieurs. Réessaie."),
              "2": rep(f"الجواب هو T égale {Tmm} milliseconde. خاص تضرب la sensibilité ف le nombre de divisions.",
                       f"Réponse : T = {n} × {SHs} = {Tms} ms.")}},
    f"Une période occupe {mots(n)} divisions, la sensibilité horizontale est {SHm} milliseconde par division. La période vaut ?")

FA2 = vf_facile("fa_a2", "Plus facile : vrai ou faux",
    "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    f"La période du son est T = {Tms} ms.", [
        (f"N = 1/T = 1/({sci(C['T'])} s) = {Ns} Hz.", True, f"T est mise en secondes avant le calcul : N = {Ns} Hz."),
        (f"N = 1/{Tms} = {fr(1 / C['T_ms'])} Hz.", False, f"T est restée en ms : il faut T = {sci(C['T'])} s, donc N = {Ns} Hz."),
        (f"Un son de {Ns} Hz est audible par l'oreille humaine.", True, "Le son audible va de 20 Hz à 20 kHz.")])

FA3 = qcm_facile("fa_a3", "Plus facile : pourquoi λ = d₁ ?",
    "سؤال ساهل على الرجوع الأول en phase. اختار الجواب الصحيح.",
    f"Les courbes sont de nouveau en phase pour la première fois quand M₂ a reculé de d₁ = {fr(d1)} cm. Pourquoi λ = d₁ ?",
    ["Parce que les deux courbes ont la même amplitude.",
     "Parce que le son parcourt d₁ en une seconde.",
     "Parce que deux points voisins qui vibrent en phase sont distants de λ."], 2, {
        "2": {"juste": rep("برافو! جوج نقط اللي vibrent en phase وحدا بعضياتهم، بيناتهم lambda. لأول مرة، c'est k égale un.",
                           "Juste : en phase, d = k·λ ; pour la première fois, k = 1, donc d₁ = λ.")},
        "0": {"1": rep("ما تقلقش. la courbe ديال M deux صغيرة، حيت بعيدة. l'amplitude ما كتقولش lambda. فكر فلحالة ديال الحركة. عاود اختار.",
                       "L'amplitude de M₂ est plus petite (il est plus loin) ; elle ne dit rien de λ. Pense à l'état de vibration. Réessaie."),
              "2": rep("الجواب: جوج نقط اللي vibrent en phase وحدا بعضياتهم، بيناتهم lambda. d égale k fois lambda، avec k égale un.",
                       "Réponse : deux points voisins en phase sont distants de λ (d = k·λ, k = 1).")},
        "1": {"1": rep("قريب! la distance اللي كيقطع le son، en une seconde، هي la célérité، ماشي lambda. عاود اختار.",
                       "La distance parcourue en une seconde, c'est la célérité v, pas λ. Réessaie."),
              "2": rep("الجواب: جوج نقط اللي vibrent en phase وحدا بعضياتهم، بيناتهم lambda. لأول مرة، c'est k égale un.",
                       "Réponse : en phase pour la première fois → d₁ = λ (k = 1).")}},
    "Les courbes sont de nouveau en phase pour la première fois quand M deux a reculé de d un. Pourquoi lambda égale d un ?")

FA4 = vf_facile("fa_a4", "Plus facile : vrai ou faux",
    "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    f"λ = {fr(d1)} cm et N = {Ns} Hz.", [
        (f"v = λ·N = {ls} × {Ns} = {vs} m/s.", True, f"λ est mise en mètres : v = {vs} m/s, la célérité du son dans l'air."),
        (f"v = λ·N = {fr(d1)} × {Ns} = {fr(d1 * C['N'], 0)} m/s.", False, f"λ est restée en cm : il faut λ = {ls} m, donc v = {vs} m/s."),
        ("v = λ/N.", False, "La relation est v = λ·N (et λ = v/N).")])

G = [("1", f"M₁M₂ = {fr(2 * d1)} cm"), ("2", f"M₁M₂ = {fr(d2)} cm"), ("3", "M₁M₂ = 40 cm")]
Dr = [("a", "en phase"), ("b", "en opposition de phase"), ("c", "ni en phase, ni en opposition")]
COUPLES = {"1": "a", "2": "b", "3": "c"}
DIST = {"1": 2 * d1, "2": d2, "3": 40.0}
R = {}
for g, _ in G:
    rq = DIST[g] / d1
    for dd, nom in Dr:
        txt_q = fr(rq)
        if COUPLES[g] == dd:
            R[f"{g}-{dd}"] = (True, f"Oui : {fr(DIST[g])}/{fr(d1)} = {txt_q} → {nom}.",
                              f"برافو: d sur lambda égale {mots(DIST[g])} sur {mots(d1)}، égale {mots(round(rq, 2))}. إذن {nom}.")
        else:
            R[f"{g}-{dd}"] = (False, f"Non : calcule M₁M₂/λ = {fr(DIST[g])}/{fr(d1)} ; un entier → en phase, un entier et demi → opposition, sinon ni l'un ni l'autre.",
                              "لا: حسب M un M deux sur lambda. عدد صحيح: en phase. عدد صحيح ونص: en opposition. وغير هادشي: لا هادي لا هادي.")
FA5 = assoc_facile("fa_a5", "Plus facile : en phase, en opposition, ou ni l'un ni l'autre",
    "سؤال ساهل: ربط كل distance ب la phase ديالها. lambda égale dix-sept centimètres.",
    f"λ = {fr(d1)} cm. Relie chaque position de M₂ à l'état des deux courbes.",
    "Relie chaque distance M₁M₂ à l'état des deux courbes.", G, Dr, COUPLES, R,
    (f"(1 ; a) (2 ; b) (3 ; c) : {fr(2 * d1)}/{fr(d1)} = 2 ; {fr(d2)}/{fr(d1)} = {fr(q)} ; 40/{fr(d1)} ≈ {fr(40 / d1)}.",
     "الجواب: d sur lambda égale deux، c'est un entier: en phase. trois et demi: en opposition. والثالثة: لا هادي لا هادي."))
assert d1 == 17

# ================= exercice semblable =================
C2 = calculs(SH_ms=0.25, ndiv=4, d1_cm=34, d2_cm=102)
assert abs(C2["T"] - 1e-3) < 1e-12      # la parole de Q2 dit « un fois dix puissance moins trois »
assert abs(C2["N"] - 1000) < 1e-6 and abs(C2["v"] - 340) < 1e-6 and C2["etat"] == "en phase"
q2 = C2["q"]
SIM_Q = [
    {"id": "1", "texte": "En exploitant la figure 2, déterminer la période T du son, en ms.",
     "reponse": valeur("T", C2["T_ms"], "ms", f"T = n·S_H = {C2['n']} × {fr(C2['SH'])} = {fr(C2['T_ms'])} ms"),
     "clavier": {"aides": ["T = n·S_H", "S_H", "div", "ms"], "pieges": [f"T = {C2['n']} ms"]},
     "correction": correction([
         (f"1 : une période = {C2['n']} divisions ; T = n·S_H", "T égale n fois la sensibilité horizontale"),
         (f"T = {C2['n']} × {fr(C2['SH'])} = {fr(C2['T_ms'])} ms", f"T égale {mots(C2['T_ms'])} milliseconde")],
         f"la question un. une période، c'est {mots(C2['n'])} divisions. T égale n fois la sensibilité horizontale، "
         f"égale {mots(C2['n'])} fois {mots(C2['SH'])}. T égale {mots(C2['T_ms'])} milliseconde.")},
    {"id": "2", "texte": "En déduire la fréquence N du son.",
     "reponse": valeur("N", C2["N"], "Hz", f"N = 1/T = 1/({sci(C2['T'])} s) = {fr(C2['N'], 0)} Hz"),
     "clavier": {"aides": ["N = 1/T", "10⁻³", "Hz"], "pieges": ["N = 1/1 = 1 Hz"]},
     "correction": correction([
         (f"2 : T = {fr(C2['T_ms'])} ms = {sci(C2['T'])} s ; N = 1/T", "N égale un sur T"),
         (f"N = {fr(C2['N'], 0)} Hz", f"N égale {mots(C2['N'])} hertz")],
         f"la question deux. T égale un fois dix puissance moins trois seconde. N égale un sur T. N égale {mots(C2['N'])} hertz.")},
    {"id": "3", "texte": f"Les courbes, d'abord en phase, sont de nouveau en phase pour la première fois lorsque M₁M₂ = d₁ = {fr(C2['d1'])} cm. Justifier que λ = d₁.",
     "reponse": phrase(f"Deux points voisins qui vibrent en phase sont séparés par λ ; de nouveau en phase pour la première fois : M₂ a reculé d'un seul λ, donc λ = d₁ = {fr(C2['d1'])} cm = {fr(C2['lam'])} m."),
     "clavier": {"aides": ["en phase", "pour la première fois", "d = k·λ", "k = 1"], "pieges": ["λ = d₁/2"]},
     "correction": correction([
         ("3 : en phase : d = k·λ ; première fois : k = 1", "k égale un"),
         (f"donc λ = d₁ = {fr(C2['d1'])} cm = {fr(C2['lam'])} m", "lambda égale d un")],
         f"la question trois. en phase: d égale k fois lambda. لأول مرة، c'est k égale un. donc lambda égale d un، égale {mots(C2['d1'])} centimètres.")},
    {"id": "4", "texte": "Calculer la célérité v du son dans l'air.",
     "reponse": valeur("v", C2["v"], "m/s", f"v = λ·N = {fr(C2['lam'])} × {fr(C2['N'], 0)} = {fr(C2['v'], 0)} m/s"),
     "clavier": {"aides": ["v = λ·N", "λ en m", "m/s"], "pieges": ["v = λ/N"]},
     "correction": correction([
         ("4 : v = λ·N", "v égale lambda fois N"),
         (f"v = {fr(C2['lam'])} × {fr(C2['N'], 0)} = {fr(C2['v'], 0)} m/s", f"v égale {mots(C2['v'])} mètres par seconde")],
         f"la question quatre. v égale lambda fois N. l'application numérique: v égale {mots(C2['lam'])} fois {mots(C2['N'])}. v égale {mots(C2['v'])} mètres par seconde.")},
    {"id": "5", "texte": f"On place M₂ à la distance M₁M₂ = d₂ = {fr(C2['d2'])} cm de M₁. Les deux courbes sont-elles en phase ou en opposition de phase ? Justifier.",
     "reponse": phrase(f"d₂/λ = {fr(C2['d2'])}/{fr(C2['d1'])} = {fr(q2)} : un nombre entier. Donc d₂ = k·λ avec k = {fr(q2)} : M₁ et M₂ vibrent en phase."),
     "clavier": {"aides": ["d₂/λ", "d = k·λ", "entier"], "pieges": ["opposition de phase"]},
     "correction": correction([
         (f"5 : d₂/λ = {fr(C2['d2'])}/{fr(C2['d1'])} = {fr(q2)}, un entier", "d deux sur lambda"),
         ("donc d₂ = k·λ : les deux courbes sont en phase", "vibrent en phase")],
         f"la question cinq. d deux sur lambda: {mots(C2['d2'])} sur {mots(C2['d1'])}، égale {mots(q2)}، c'est un nombre entier. donc M un et M deux vibrent en phase.")},
]

EX = {
  "id": "phys_ex_ch2_air_3", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques_periodiques", "cours": "phys_ch2_ondes_periodiques",
  "titre": "Un haut-parleur et deux microphones : la célérité du son", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Lire T sur un oscillogramme (T = n·S_H)", "Calculer N = 1/T", "Exploiter le premier retour en phase : λ = d₁",
                  "Calculer v = λ·N", "Comparer l'état vibratoire de deux points (d/λ)"],
  "enonce": {
    "intro": ("Un générateur basse fréquence (GBF) alimente un haut-parleur qui émet un son sinusoïdal. Deux microphones M₁ et M₂, "
              "placés sur l'axe du haut-parleur, sont reliés aux voies A et B d'un oscilloscope (figure 1). Au départ, M₁ et M₂ sont "
              "côte à côte : on observe les oscillogrammes de la figure 2. On garde ensuite M₁ fixe et on éloigne M₂ du "
              "haut-parleur, le long de l'axe."),
    "intro_dit": ("دابا نقراو l'énoncé. le GBF كيعطي le courant ل le haut-parleur، وهو كيعطي un son sinusoïdal. "
                  "deux microphones، M un وM deux، كاينين على l'axe ديال le haut-parleur، ومربوطين ب les voies A et B ديال l'oscilloscope. "
                  "فاللول، M un وM deux حدا بعضياتهم، وla figure deux كتبين l'oscillogramme. "
                  "من بعد، M un كيبقى فبلاصتو، وكنبعدو M deux، le long de l'axe."),
    "figures": [montage(), oscillogramme(C)],
    "donnees": [f"Sensibilité horizontale : S_H = {SHs} ms/div", "1 ms = 10⁻³ s"],
    "questions": [Q1, Q2, Q3, Q4, Q5]},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPL}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [FA1, FA2, FA3, FA4, FA5]}]},
  "similaire": {
    "id": "phys_ex_ch2_air_3_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": ("Un haut-parleur alimenté par un GBF émet un son sinusoïdal. Deux microphones M₁ et M₂, d'abord côte à côte sur "
                "l'axe du haut-parleur, sont reliés aux voies A et B d'un oscilloscope (figure 2). On garde M₁ fixe et on éloigne M₂."),
      "intro_dit": ("نفس التمرين، بقيم أخرى. le haut-parleur كيعطي un son sinusoïdal. M un وM deux فاللول حدا بعضياتهم، "
                    "ومن بعد كنبعدو M deux."),
      "figures": [montage(), oscillogramme(C2)],
      "donnees": [f"Sensibilité horizontale : S_H = {fr(C2['SH'])} ms/div", "1 ms = 10⁻³ s"],
      "questions": SIM_Q}},
}
ecrire(EX)
