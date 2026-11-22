# Exercice de physique, ch. 2 (ondes mécaniques progressives périodiques) — niveau facile.
# Deux points d'une corde : λ lue sur l'aspect, en phase (d = k·λ), le n-ième point en opposition (d = (2k + 1)·λ/2).
#
# Sources comparées (skill exercices § 2) :
# - exploration ondes_mecaniques_periodiques.json : cas_type « phase_opposition » (0 national PC 2016–2025, mais dans tous les
#   devoirs et chez 8 profs sur 10) ; pièges « nombre à virgule donc opposition », « conclut d'après le dessin, sans calcul »,
#   « n-ième point en opposition : prend k = n » ; a_ne_pas_dire « virgule → opposition » ; exclus : quadrature (on dit
#   seulement « ni l'un ni l'autre »). experience_profs.json : pas d'entrée pour ce chapitre.
# - vidéos des profs : Taousse et Adrar (leur erreur « virgule → opposition », non reprise), Oussama (k ∈ ℕ* pour la phase,
#   k ∈ ℕ pour l'opposition), Laksabi (phrase de conclusion écrite).
# - nationaux comparés : aucun national PC 2016–2025 ne pose la phase (exploration) ; 2017 N ex. II (λ lue sur une coupe de
#   l'eau, choix parmi 4 valeurs) est la seule lecture voisine : ici une corde, λ lue entre deux crêtes sur un axe gradué en cm,
#   puis la comparaison de deux points et le troisième point en opposition — chaîne absente des nationaux.
# - séries en ligne : recherche web faite (extraits talamidi, moutamadris, alloschool, scribd Jenkal : critère d = k·λ et
#   (2k + 1)·λ/2) ; la lecture des pages est bloquée par le réseau de la session (domaines non résolus).
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

METHODE = "/media/simulations/physics/ondes-periodiques-tableau/methode-phase.html"   # λ = 4 cm, d réglable de 1 à 14 cm

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
    c, r = divmod(n, 100)
    tete = "cent" if c == 1 else _U[c] + (" cents" if r == 0 else " cent")
    return tete if r == 0 else tete + " " + _ent(r)
def mots(x, decimales=3):
    s = f"{x:.{decimales}f}".rstrip("0").rstrip(".")
    if "." not in s: return _ent(int(s))
    e, d = s.split(".")
    z = len(d) - len(d.lstrip("0"))
    return _ent(int(e)) + " virgule " + " ".join(["zéro"] * z + ([_ent(int(d.lstrip("0")))] if d.lstrip("0") else []))


def aspect(lam, xM, xP, xmax, pas, A=1.0):
    """Aspect de la corde à un instant : M (et P) sur une crête ; l'onde va de gauche à droite."""
    grad = [round(k * pas, 3) for k in range(int(round(xmax / pas)) + 1)]
    return {"type": "courbe", "titre": "Aspect de la corde à un instant t",
            "legende": "L'axe horizontal porte la position x le long de la corde (en cm). L'onde se propage dans le sens des x croissants.",
            "axes": {"x": {"min": 0, "max": xmax, "nom": "x", "unite": "cm", "graduations": [[g, fr(g)] for g in grad]},
                     "y": {"min": -1.8 * A, "max": 1.8 * A, "nom": "y", "unite": "mm", "graduations": [[A, fr(A)], [-A, fr(-A)]]}},
            "elements": [
                {"f": "courbe", "expr": f"{A}*cos(2*pi*(x-{xM})/{lam})", "de": 0, "a": xmax, "couleur": "orange"},
                {"f": "point", "at": [xM, A], "t": "M", "pos": "n", "couleur": "rouge"},
                {"f": "point", "at": [xP, A], "t": "P", "pos": "n", "couleur": "cyan"},
                {"f": "fleche", "de": [0.35 * xmax, -1.55 * A], "a": [0.6 * xmax, -1.55 * A], "couleur": "blanc",
                 "texte": "sens de propagation", "pos": "e"}]}


def calculs(lam, xM, xP, rang):
    MP = xP - xM
    q = MP / lam
    k = rang - 1                         # le n-ième point en opposition : k = n − 1 (k commence à 0)
    MN = (2 * k + 1) * lam / 2
    return dict(lam=lam, xM=xM, xP=xP, MP=MP, q=q, k=k, MN=MN, c1=xM, c2=xM + lam)


C = calculs(lam=4.0, xM=2.0, xP=14.0, rang=3)
lam, MP, q, k, MN = C["lam"], C["MP"], C["q"], C["k"], C["MN"]
assert abs(q - round(q)) < 1e-9 and abs(MN - 10) < 1e-9 and MP <= 14
ls, MPs, qs, MNs = fr(lam), fr(MP), fr(q), fr(MN)
lm, MPm, qm, MNm = mots(lam), mots(MP), mots(q), mots(MN)
ORD = {1: "premier", 2: "deuxième", 3: "troisième"}
ORD_AR = {1: "اللولة", 2: "الثانية", 3: "الثالثة"}

Q1 = {"id": "1",
      "texte": "Lire sur la figure la longueur d'onde λ.",
      "texte_dit": "la question un: قرا على la figure la longueur d'onde lambda.",
      "reponse": valeur("λ", lam, "cm", f"λ = {fr(C['c2'])} − {fr(C['c1'])} = {ls} cm"),
      "clavier": {"aides": ["λ", "cm", "deux crêtes voisines"], "pieges": [f"λ = {MPs} cm", f"λ = {fr(lam / 2)} cm"]},
      "aides": [
          aide("L'axe horizontal porte une distance (en cm) : c'est bien λ qu'on y lit. Repère deux crêtes voisines.",
               "l'axe فيه la distance x، en centimètre. إذن هنا كنقراو lambda. قلب على les deux crêtes اللي حدا بعضياتهم."),
          aide("λ est la plus petite distance entre deux points dans le même état vibratoire : de crête à la crête suivante.",
               "lambda هي أصغر مسافة بين جوج نقط عندهم نفس الحالة: من crête حتى للcrête اللي من بعدها.")],
      "correction": correction([
          (f"1 : deux crêtes voisines en x = {fr(C['c1'])} cm et x = {fr(C['c2'])} cm", "les deux crêtes"),
          (f"λ = {fr(C['c2'])} − {fr(C['c1'])} = {ls} cm", f"lambda égale {lm} centimètres")],
          f"la question un. على la figure، les deux crêtes اللي حدا بعضياتهم، à x égale {mots(C['c1'])} centimètres، et à x égale {mots(C['c2'])} centimètres. "
          f"إذن lambda égale {mots(C['c2'])} moins {mots(C['c1'])}، lambda égale {lm} centimètres."),
      "explication": "ex_p1", "facile": "fa_p1"}

Q2 = {"id": "2",
      "texte": f"Les points M et P sont distants de MP = {MPs} cm. Montrer que M et P vibrent en phase.",
      "texte_dit": f"la question deux: M وP، المسافة بيناتهم MP égale {MPm} centimètres. بين بلي M وP vibrent en phase.",
      "reponse": phrase(f"MP/λ = {MPs}/{ls} = {qs} : un nombre entier. Donc MP = k·λ avec k = {qs} : M et P vibrent en phase."),
      "clavier": {"aides": ["MP/λ", "d = k·λ", "k entier", "en phase"], "pieges": ["d = (2k + 1)·λ/2", "opposition de phase"]},
      "aides": [
          aide("Le dessin ne suffit pas : on compare la distance MP à λ, dans la même unité, en calculant MP/λ.",
               "الرسم بوحدو ماشي جواب. خاصنا نحسبو MP sur lambda، بنفس الوحدة."),
          aide("Si MP/λ est un entier k, alors MP = k·λ : les deux points vibrent en phase.",
               "يلا لقيتي عدد صحيح k، إذن MP égale k fois lambda، وM وP vibrent en phase.")],
      "correction": correction([
          (f"2 : MP/λ = {MPs}/{ls} = {qs}", "MP sur lambda"),
          (f"{qs} est un entier : MP = {qs}·λ (d = k·λ, k = {qs})", "عدد صحيح"),
          ("donc M et P vibrent en phase", "M et P vibrent en phase")],
          f"la question deux. نحسبو MP sur lambda: {MPm} sur {lm}، égale {qm}. "
          f"{qm}، c'est un nombre entier: عدد صحيح. إذن MP égale k fois lambda، avec k égale {qm}. "
          f"donc M et P vibrent en phase."),
      "explication": "ex_p2", "facile": "fa_p2"}

Q3 = {"id": "3",
      "texte": f"Déterminer la distance MN, où N est le {ORD[C['k'] + 1]} point, à droite de M, qui vibre en opposition de phase avec M.",
      "texte_dit": f"la question trois: N هي النقطة {ORD_AR[C['k'] + 1]} على اليمين ديال M، اللي vibre en opposition de phase مع M. حدد la distance MN.",
      "reponse": valeur("MN", MN, "cm", f"MN = (2k + 1)·λ/2 avec k = {k} : MN = {2 * k + 1} × {ls}/2 = {MNs} cm"),
      "clavier": {"aides": ["d = (2k + 1)·λ/2", "k = 0", "λ", "cm", "A.N. :"], "pieges": [f"k = {k + 1}", "d = k·λ"]},
      "aides": [
          aide("Les points en opposition de phase avec M sont à MN = (2k + 1)·λ/2. Le premier correspond à k = 0 : MN = λ/2.",
               "النقط اللي vibrent en opposition de phase مع M، بعاد ب MN égale deux k plus un, fois lambda sur deux. النقطة اللولة: k égale zéro."),
          aide("k commence à 0 : le premier point a k = 0, le deuxième k = 1, le troisième k = 2. Remplace, puis calcule.",
               "النقطة اللولة: k égale zéro، الثانية k égale un، الثالثة k égale deux. عوض وحسب.")],
      "correction": correction([
          ("3 : opposition de phase : MN = (2k + 1)·λ/2", "deux k plus un"),
          (f"troisième point : k = {k}", f"k égale {mots(k)}"),
          (f"MN = {2 * k + 1} × {ls}/2 = {MNs} cm", f"MN égale {MNm} centimètres")],
          f"la question trois. en opposition de phase: MN égale deux k plus un, fois lambda sur deux. "
          f"أول قيمة ديال k: k égale zéro. النقطة الثالثة: k égale {mots(k)}. "
          f"l'application numérique: MN égale {mots(2 * k + 1)} fois {lm} sur deux. MN égale {MNm} centimètres."),
      "explication": "ex_p3", "facile": "fa_p3"}

# ---------- explication animée (methode-phase.html : λ = 4 cm, M fixe, P à la distance d réglable) ----------
m1 = (f"شوف la corde كتتحرك. M بالحمر، وP بالبرتقالي. باش نقراو lambda، كناخدو les deux crêtes اللي حدا بعضياتهم. "
      f"هاهي lambda فوق la corde: lambda égale {lm} centimètres. "
      f"فالتمرين، نفس الشي على la figure: les crêtes à x égale {mots(C['c1'])}، et à x égale {mots(C['c2'])} centimètres. "
      f"lambda égale {mots(C['c2'])} moins {mots(C['c1'])}، égale {lm} centimètres.")
m2 = (f"دابا نحطو P، à d égale {MPm} centimètres من M. شوف: M كتطلع، وP كتطلع معاها. "
      f"ولكن الرسم بوحدو ماشي جواب. أولا lambda. ثانيا la distance d. "
      f"ثالثا، كنحسبو d sur lambda: {MPm} sur {lm}، égale {qm}. "
      f"{qm}، c'est un nombre entier. إذن d égale k fois lambda، و M et P vibrent en phase.")
m3 = (f"دابا النقط اللي vibrent en opposition de phase مع M. la relation: d égale deux k plus un, fois lambda sur deux. "
      f"أول نقطة عندها k égale zéro. النقطة اللولة: k égale zéro، d égale lambda sur deux، égale deux centimètres. "
      f"الثانية: k égale un، d égale trois lambda sur deux، égale six centimètres. "
      f"الثالثة: k égale deux، d égale cinq lambda sur deux، égale dix centimètres. شوف: ملي M كتطلع، P كتهبط. "
      f"إذن la troisième، c'est k égale deux، ماشي k égale trois.")
assert MN == 10 and lam == 4   # m3 dit les valeurs de la simulation, qui sont aussi celles de l'exercice
EXPL = [
    diapo_sim("ex_p1", "Question 1 : λ, de crête à crête",
              "λ se lit sur un axe de distance, entre deux crêtes voisines : λ = 4 cm.",
              METHODE, "Une corde qui vibre : λ = 4 cm", m1,
              [("λ = 4 cm", f"égale {lm} centimètres.")],
              [dict(mot="M بالحمر", repere="M"),
               dict(mot="هاهي lambda فوق la corde", commande="play_until", parametres={"moment": "lambda"}),
               dict(mot="lambda égale", repere="lambda"),
               dict(mot=f"égale {lm} centimètres.", cible="centre:0")]),
    diapo_sim("ex_p2", "Question 2 : d/λ entier, donc en phase",
              "MP/λ = 12/4 = 3 : un entier, M et P vibrent en phase.",
              METHODE, "La méthode d/λ, avec d = 12 cm", m2,
              [("d = k·λ → en phase", "إذن d égale k fois lambda"), ("12/4 = 3", f"égale {qm}. ")],
              [dict(mot="دابا نحطو P", commande="set_parameters", parametres={"d_cm": MP}),
               dict(mot="M كتطلع، وP كتطلع معاها", repere="P"),
               dict(mot="أولا lambda", commande="play_until", parametres={"moment": "lambda"}),
               dict(mot="ثانيا la distance d", commande="play_until", parametres={"moment": "distance"}),
               dict(mot="ثالثا، كنحسبو", commande="play_until", parametres={"moment": "calcul"}),
               dict(mot=f"égale {qm}. ", cible="centre:1"),
               dict(mot="c'est un nombre entier", commande="play_until", parametres={"moment": "verdict"}),
               dict(mot="إذن d égale k fois lambda", cible="centre:0")]),
    diapo_sim("ex_p3", "Question 3 : le troisième point en opposition de phase",
              "d = (2k + 1)·λ/2 et k commence à 0 : le troisième point a k = 2.",
              METHODE, "Les points en opposition de phase avec M : 2 cm, 6 cm, 10 cm", m3,
              [("d = (2k + 1)·λ/2", "la relation: d égale deux k plus un"), ("k = 2 : d = 5 × 4/2 = 10 cm", "égale dix centimètres")],
              [dict(mot="la relation: d égale deux k plus un", cible="centre:0"),
               dict(mot="النقطة اللولة", commande="set_parameters", parametres={"d_cm": 2}),
               dict(mot="d égale lambda sur deux", commande="play_until", parametres={"moment": "verdict"}),
               dict(mot="الثانية: k égale un", commande="set_parameters", parametres={"d_cm": 6}),
               dict(mot="الثالثة: k égale deux", commande="set_parameters", parametres={"d_cm": MN}),
               dict(mot="égale dix centimètres", cible="centre:1"),
               dict(mot="ملي M كتطلع، P كتهبط", repere="verdict")]),
]

# ---------- versions faciles ----------
FA1 = qcm_facile("fa_p1", "Plus facile : lire λ",
    "نتمرنو بسؤال ساهل على la figure. اختار الجواب الصحيح.",
    f"Sur la figure, deux crêtes voisines sont en x = {fr(C['c1'])} cm et x = {fr(C['c2'])} cm ; M et P sont à {MPs} cm l'un de l'autre. La longueur d'onde vaut…",
    [f"λ = {MPs} cm", f"λ = {ls} cm", f"λ = {fr(lam / 2)} cm"], 1, {
        "1": {"juste": rep(f"برافو! من crête حتى للcrête اللي حداها: lambda égale {lm} centimètres.",
                           f"Juste : λ = {fr(C['c2'])} − {fr(C['c1'])} = {ls} cm, entre deux crêtes voisines.")},
        "0": {"1": rep("ما تقلقش. هادي المسافة بين M وP، وبيناتهم بزاف ديال les motifs. lambda هي motif واحد. عاود اختار.",
                       "C'est MP : il contient plusieurs motifs. λ, c'est un seul motif. Réessaie."),
              "2": rep(f"الجواب هو lambda égale {lm} centimètres. MP égale {qm} lambda، ماشي وحدة.",
                       f"Réponse : λ = {ls} cm ; MP contient {qs} λ.")},
        "2": {"1": rep("قريب! ولكن هادي من la crête حتى le creux: غير نص motif. عاود اختار.",
                       "De la crête au creux, ce n'est qu'un demi-motif. Réessaie."),
              "2": rep(f"الجواب هو lambda égale {lm} centimètres، من crête حتى للcrête اللي حداها.",
                       f"Réponse : λ = {ls} cm, de crête à crête (λ/2 = {fr(lam / 2)} cm va de la crête au creux).")}},
    f"Deux crêtes voisines sont en x égale {mots(C['c1'])} et x égale {mots(C['c2'])} centimètres. La longueur d'onde vaut ?")

FA2 = vf_facile("fa_p2", "Plus facile : vrai ou faux",
    "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    f"λ = {ls} cm et MP = {MPs} cm.", [
        (f"MP/λ = {qs}, un entier : M et P vibrent en phase.", True, f"MP = {qs}·λ = k·λ avec k entier : en phase."),
        ("Si MP/λ = 2,3, M et P vibrent en opposition de phase.", False, "2,3 n'est ni un entier ni un entier et demi : ni en phase, ni en opposition."),
        ("Pour conclure, il suffit de regarder la figure, sans calcul.", False, "Il faut calculer MP/λ (dans la même unité), puis écrire la phrase de conclusion.")])

G = [("1", "1ᵉʳ point en opposition avec M"), ("2", "2ᵉ point en opposition avec M"), ("3", "3ᵉ point en opposition avec M")]
Dr = [("a", f"{fr(lam / 2)} cm"), ("b", f"{fr(3 * lam / 2)} cm"), ("c", f"{fr(5 * lam / 2)} cm"), ("d", f"{ls} cm")]
COUPLES = {"1": "a", "2": "b", "3": "c"}
KS = {"1": 0, "2": 1, "3": 2}
VAL = {"a": lam / 2, "b": 3 * lam / 2, "c": 5 * lam / 2, "d": lam}
NOMK = {"a": ("k = 0", "k égale zéro"), "b": ("k = 1", "k égale un"), "c": ("k = 2", "k égale deux")}
R = {}
for g, _ in G:
    kk = KS[g]
    for dd, _ in Dr:
        if COUPLES[g] == dd:
            R[f"{g}-{dd}"] = (True, f"Oui : k = {kk}, MN = ({2 * kk + 1})·λ/2 = {fr(VAL[dd])} cm.",
                              f"برافو: k égale {mots(kk)}، MN égale {mots(VAL[dd])} centimètres.")
        elif dd == "d":
            R[f"{g}-{dd}"] = (False, f"Non : {ls} cm = λ, et à une distance λ on est en phase, pas en opposition.",
                              f"لا: هادي هي lambda، وبعاد ب lambda كيكونو en phase، ماشي en opposition.")
        else:
            R[f"{g}-{dd}"] = (False, f"Non : {fr(VAL[dd])} cm correspond à {NOMK[dd][0]}. Compte k à partir de 0 : ce point-là a k = {kk}.",
                              f"لا: هادي ديال {NOMK[dd][1]}. بدا من k égale zéro، وهاد النقطة عندها k égale {mots(kk)}.")
FA3 = assoc_facile("fa_p3", "Plus facile : les points en opposition de phase",
    "سؤال ساهل: ربط كل نقطة ب la distance ديالها من M. تفكر: أول نقطة عندها k égale zéro.",
    f"λ = {ls} cm. Relie chaque point à sa distance de M (une distance est en trop).",
    "Relie chaque point à sa distance de M.", G, Dr, COUPLES, R,
    (f"(1 ; a) (2 ; b) (3 ; c). Le n-ième point a k = n − 1. {ls} cm = λ : point en phase.",
     f"الجواب: d égale deux، six، et dix centimètres. النقطة رقم n عندها k égale n moins un. و lambda égale {lm} centimètres: en phase."))
assert lam == 4

# ================= exercice semblable =================
C2 = calculs(lam=6.0, xM=3.0, xP=27.0, rang=3)
l2, MP2, q2, k2, MN2 = C2["lam"], C2["MP"], C2["q"], C2["k"], C2["MN"]
assert abs(q2 - round(q2)) < 1e-9
SIM_Q = [
    {"id": "1", "texte": "Lire sur la figure la longueur d'onde λ.",
     "reponse": valeur("λ", l2, "cm", f"λ = {fr(C2['c2'])} − {fr(C2['c1'])} = {fr(l2)} cm"),
     "clavier": {"aides": ["λ", "cm", "deux crêtes voisines"], "pieges": [f"λ = {fr(MP2)} cm", f"λ = {fr(l2 / 2)} cm"]},
     "correction": correction([
         (f"1 : deux crêtes voisines en x = {fr(C2['c1'])} cm et x = {fr(C2['c2'])} cm", "les deux crêtes"),
         (f"λ = {fr(C2['c2'])} − {fr(C2['c1'])} = {fr(l2)} cm", f"lambda égale {mots(l2)} centimètres")],
         f"la question un. les deux crêtes اللي حدا بعضياتهم، à x égale {mots(C2['c1'])}، et à x égale {mots(C2['c2'])} centimètres. lambda égale {mots(l2)} centimètres.")},
    {"id": "2", "texte": f"Les points M et P sont distants de MP = {fr(MP2)} cm. Montrer que M et P vibrent en phase.",
     "reponse": phrase(f"MP/λ = {fr(MP2)}/{fr(l2)} = {fr(q2)} : un nombre entier. Donc MP = k·λ avec k = {fr(q2)} : M et P vibrent en phase."),
     "clavier": {"aides": ["MP/λ", "d = k·λ", "en phase"], "pieges": ["d = (2k + 1)·λ/2"]},
     "correction": correction([
         (f"2 : MP/λ = {fr(MP2)}/{fr(l2)} = {fr(q2)}, un entier", "MP sur lambda"),
         ("donc MP = k·λ : M et P vibrent en phase", "M et P vibrent en phase")],
         f"la question deux. MP sur lambda: {mots(MP2)} sur {mots(l2)}، égale {mots(q2)}، c'est un nombre entier. donc M et P vibrent en phase.")},
    {"id": "3", "texte": "Déterminer la distance MN, où N est le troisième point, à droite de M, qui vibre en opposition de phase avec M.",
     "reponse": valeur("MN", MN2, "cm", f"MN = (2k + 1)·λ/2 avec k = {k2} : MN = {2 * k2 + 1} × {fr(l2)}/2 = {fr(MN2)} cm"),
     "clavier": {"aides": ["d = (2k + 1)·λ/2", "k = 0", "cm"], "pieges": [f"k = {k2 + 1}", "d = k·λ"]},
     "correction": correction([
         (f"3 : MN = (2k + 1)·λ/2, troisième point : k = {k2}", "deux k plus un"),
         (f"MN = {2 * k2 + 1} × {fr(l2)}/2 = {fr(MN2)} cm", f"MN égale {mots(MN2)} centimètres")],
         f"la question trois. MN égale deux k plus un, fois lambda sur deux، avec k égale {mots(k2)}. "
         f"l'application numérique: MN égale {mots(2 * k2 + 1)} fois {mots(l2)} sur deux. MN égale {mots(MN2)} centimètres.")},
]

EX = {
  "id": "phys_ex_ch2_phase_2", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques_periodiques", "cours": "phys_ch2_ondes_periodiques",
  "titre": "Deux points d'une corde : en phase ou en opposition ?", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Lire λ sur l'aspect du milieu", "Montrer que deux points vibrent en phase (d = k·λ)", "Situer le n-ième point en opposition de phase (d = (2k + 1)·λ/2)"],
  "enonce": {
    "intro": ("Une onde progressive sinusoïdale se propage sans amortissement le long d'une corde élastique. "
              "La figure représente l'aspect d'une partie de la corde à un instant t. Les points M et P de la corde sont marqués."),
    "intro_dit": ("دابا نقراو l'énoncé. une onde progressive sinusoïdale كتمشي فوق une corde élastique، بلا ما تضعاف. "
                  "la figure كتبين l'aspect ديال la corde ف واحد اللحظة t، وفيها النقطتين M وP."),
    "figures": [aspect(lam, C["xM"], C["xP"], 16.0, 2.0)],
    "donnees": [f"Figure : aspect de la corde, axe des x gradué en cm ; M en x = {fr(C['xM'])} cm, P en x = {fr(C['xP'])} cm"],
    "questions": [Q1, Q2, Q3]},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPL}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [FA1, FA2, FA3]}]},
  "similaire": {
    "id": "phys_ex_ch2_phase_2_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": ("Une onde progressive sinusoïdale se propage le long d'une corde. La figure représente l'aspect d'une partie "
                "de la corde à un instant t, avec deux points M et P."),
      "intro_dit": "نفس التمرين، بقيم أخرى. la figure كتبين l'aspect ديال la corde ف واحد اللحظة، وفيها M وP.",
      "figures": [aspect(l2, C2["xM"], C2["xP"], 30.0, 3.0)],
      "donnees": ["Figure : aspect de la corde, axe des x gradué en cm"],
      "questions": SIM_Q}},
}
ecrire(EX)
