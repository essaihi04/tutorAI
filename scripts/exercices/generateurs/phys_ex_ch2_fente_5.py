# Exercice de physique (ch. 2, ondes mécaniques progressives périodiques), niveau moyen :
# onde rectiligne à la surface de l'eau devant une ouverture — λ = v/N, diffraction justifiée (a comparée à λ),
# N, v, λ inchangés après l'ouverture, description de l'onde diffractée, retard d'un point après l'ouverture,
# puis ouverture élargie (onde diaphragmée).
#
# Sources comparées (skill exercices § 2) :
# - exploration ondes_mecaniques_periodiques.json : cas_types diffraction_justifier (« a ≤ λ, même unité, onde
#   diffractée : même N, même λ, même v ; arcs centrés sur l'ouverture espacés de λ »), retard_periodique,
#   phase_opposition ; pieges (fréquence ou λ qui changeraient, unités différentes, traits droits au lieu d'arcs) ;
#   a_ne_pas_dire (« si a > λ il ne se passe rien » → onde diaphragmée) ; erreurs_des_profs (condition réduite à une
#   inégalité stricte : on écrit « de l'ordre de λ ou plus petite »).
# - vidéos des profs : bacfacile (diffraction simple), Oussama (onde diaphragmée), mouhibi (diffraction en devoir).
# - nationaux comparés : 2020 N ex. II Q4 (QCM « lors de la diffraction… »), 2024 R 2.b (vrai/faux « la diffraction
#   modifie λ »). Ici : questions ouvertes à justifier, notre situation (25 Hz, 0,30 m/s, a = 1,0 cm puis 5,0 cm),
#   avec un retard après l'ouverture : aucun national n'a cette chaîne.
# - séries en ligne : la recherche (WebSearch) a donné les titres de séries talamidi, moutamadris, alloschool,
#   Jenkal, Ajitfham ; leur lecture (WebFetch) est bloquée par le réseau de la session (ENOTFOUND).
import sys, os, re, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *
from pathlib import Path
_RACINE = Path(__file__).resolve().parents[3]

_sp = importlib.util.spec_from_file_location("tp", str(_RACINE / "backend" / "kaggle_tts" / "texte_parle.py"))
_tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_tp)


def mots(s):
    """« 1,2 » -> « un virgule deux » (pour la voix)."""
    s = str(s)
    if "," in s:
        e, d = s.split(",")
        r = d.lstrip("0")
        return _tp.nombre_fr(int(e)) + " virgule" + " zéro" * (len(d) - len(r)) + (" " + _tp.nombre_fr(int(r)) if r else "")
    return _tp.nombre_fr(int(s))



# ---------------- vérification de la voix ----------------
NOMBRES = r"(?:zéro|un(?= (?:virgule|fois|sur|mètre|centimètre|millimètre|hertz|seconde|lambda|T\b)|[.،,])|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|vingt-\w+|trente|trente-\w+|quarante|quarante-\w+|cinquante|soixante|cent|mille)\b"
COLLE = re.compile("[\u0621-\u064A]+ +" + NOMBRES)


PB_VOIX = []


def controler_voix(o, k=""):
    if isinstance(o, dict):
        for kk, v in o.items(): controler_voix(v, kk)
    elif isinstance(o, list):
        for v in o: controler_voix(v, k)
    elif isinstance(o, str) and k in {"mixed", "dit", "parole", "intro_dit", "texte_dit", "enonce_dit", "mot"}:
        for m in COLLE.finditer(o):
            PB_VOIX.append(f"darija collé à un nombre : « {m.group(0)} »")
        if re.search(r"\d", o):
            PB_VOIX.append(f"chiffre dans la voix : {o[:80]}")




SIMS = "/media/simulations/physics/ondes-periodiques-tableau/"


# ---------------- données (calculées) ----------------
def donnees(N, v, a_cm, OM_cm, a2_cm):
    D = {"N": N, "v": v, "a": a_cm, "OM": OM_cm, "a2": a2_cm}
    D["lam"] = v / N * 100            # cm
    D["T"] = 1 / N
    D["tau"] = OM_cm * 1e-2 / v
    D["q"] = OM_cm / D["lam"]
    return D

A = donnees(25, 0.30, 1.0, 3.6, 5.0)
B = donnees(15, 0.27, 1.5, 4.5, 6.0)
assert abs(A["lam"] - 1.2) < 1e-9 and abs(A["tau"] - 0.12) < 1e-9 and abs(A["q"] - 3) < 1e-9
assert abs(B["lam"] - 1.8) < 1e-9 and abs(B["tau"] - 1 / 6) < 1e-9 and abs(B["q"] - 2.5) < 1e-9
for D in (A, B):
    assert D["a"] < D["lam"] and D["a2"] / D["lam"] >= 3


def etat(q):
    if abs(q - round(q)) < 1e-9:
        return "en phase"
    return "en opposition de phase" if abs(q - int(q) - 0.5) < 1e-9 else "ni en phase ni en opposition de phase"


def figure(D, titre):
    S0, lam, XW, YC, H = 0.6, D["lam"], 5.4, 3.5, 7.0
    a = D["a"]
    el = [{"f": "rect", "de": [0.2, 0.2], "a": [11.6, 6.8], "couleur": "faible"},
          {"f": "ligne", "pts": [[S0, 0.6], [S0, 6.4]], "couleur": "jaune", "epais": True},
          {"f": "texte", "at": [S0, 7.25], "t": "S (réglette)", "couleur": "jaune", "ancre": "centre"}]
    k = 1
    while S0 + k * lam < XW - 0.2:
        x = round(S0 + k * lam, 3)
        el.append({"f": "ligne", "pts": [[x, 0.6], [x, 6.4]], "couleur": "blanc"})
        k += 1
    el += [{"f": "ligne", "pts": [[XW, 0.2], [XW, round(YC - a / 2, 3)]], "couleur": "orange", "epais": True},
           {"f": "ligne", "pts": [[XW, round(YC + a / 2, 3)], [XW, 6.8]], "couleur": "orange", "epais": True},
           {"f": "cote", "de": [XW - 0.35, round(YC - a / 2, 3)], "a": [XW - 0.35, round(YC + a / 2, 3)], "t": "a", "couleur": "jaune", "pos": "o"},
           {"f": "point", "at": [XW, YC], "t": "O", "pos": "se", "couleur": "jaune"},
           {"f": "ligne", "pts": [[XW, YC], [11.4, YC]], "couleur": "faible", "trait": "pointille"},
           {"f": "point", "at": [round(XW + D["OM"], 3), YC], "t": "M", "pos": "n", "couleur": "cyan"},
           {"f": "cote", "de": [XW, 1.2], "a": [round(XW + D["OM"], 3), 1.2], "t": f"OM = {fr(D['OM'], 1)} cm", "couleur": "cyan", "pos": "s"},
           {"f": "texte", "at": [8.6, 5.6], "t": "?", "couleur": "faible", "taille": "grand", "ancre": "centre"},
           {"f": "fleche", "de": [1.5, 6.6], "a": [3.6, 6.6], "texte": "propagation", "couleur": "faible", "pos": "n"},
           {"f": "texte", "at": [XW + 0.2, 6.5], "t": "obstacle", "couleur": "orange", "ancre": "gauche"}]
    return {"type": "schema", "titre": titre, "cadre": {"l": 11.8, "h": H + 0.6},
            "legende": "Vue de dessus (échelle 1) : les crêtes de l'onde incidente arrivent sur l'obstacle percé d'une ouverture de largeur a. Après l'ouverture, l'onde n'est pas dessinée.",
            "elements": el}


def intro(D):
    return (f"Dans une cuve à ondes, une réglette S liée à un vibreur de fréquence N = {fr(D['N'], 1)} Hz crée à la surface "
            f"de l'eau une onde progressive sinusoïdale rectiligne, qui se propage sans amortissement avec la célérité "
            f"v = {fr(D['v'], 2)} m/s. On place sur son trajet un obstacle percé d'une ouverture de largeur a = {fr(D['a'], 1)} cm, "
            f"de centre O (figure). M est un point de la surface après l'ouverture, sur l'axe de l'ouverture. "
            f"La profondeur de l'eau est la même partout.")


def intro_dit(D):
    return (f"دابا نقراو l'énoncé. فواحد la cuve à ondes، la réglette S مربوطة مع le vibreur، la fréquence N égale {mots(fr(D['N'], 1))} hertz. "
            f"كتعطي فوق الما une onde progressive sinusoïdale rectiligne، بلا amortissement، وla célérité v égale {mots(fr(D['v'], 2))} mètre par seconde. "
            f"فالطريق ديالها، حطينا واحد الحاجز، وفيه واحد الفتحة، la largeur a égale {mots(fr(D['a'], 1))} centimètre، والمركز ديالها O. "
            f"M نقطة من بعد الفتحة، فوق l'axe ديال الفتحة. والعمق ديال الما هو هو فكل بلاصة.")


def donnees_txt(D):
    return [f"N = {fr(D['N'], 1)} Hz ; v = {fr(D['v'], 2)} m/s", f"a = {fr(D['a'], 1)} cm (questions 2 à 5) ; a′ = {fr(D['a2'], 1)} cm (question 6)",
            f"OM = {fr(D['OM'], 1)} cm"]


def q1(D):
    v, N, lam = fr(D["v"], 2), fr(D["N"], 1), fr(D["lam"], 2)
    return {"id": "1", "texte": "Calculer la longueur d'onde λ de l'onde incidente.",
            "reponse": valeur("λ", D["lam"], "cm", f"λ = v/N = {v}/{N} = {fr(D['lam'] / 100, 3)} m = {lam} cm"),
            "clavier": {"aides": ["λ = v/N", "λ = v·T", "m", "cm"], "pieges": ["λ = v·N", "λ = N/v"]},
            "correction": correction([
                ("1 : v = λ·N donc λ = v/N", "lambda égale v sur N"),
                (f"λ = {v}/{N}", f"égale {mots(v)} sur {mots(N)}"),
                (f"λ = {fr(D['lam'] / 100, 3)} m = {lam} cm", f"lambda égale {mots(lam)} centimètre")],
                f"Question un. v égale lambda fois N، إذن lambda égale v sur N، égale {mots(v)} sur {mots(N)}. "
                f"lambda égale {mots(fr(D['lam'] / 100, 3))} mètre، يعني lambda égale {mots(lam)} centimètre.")}


def q2(D):
    a, lam = fr(D["a"], 1), fr(D["lam"], 2)
    return {"id": "2", "texte": f"Avec a = {a} cm, nommer le phénomène observé après l'ouverture. Justifier.",
            "reponse": phrase(f"La diffraction : a = {a} cm et λ = {lam} cm, dans la même unité a < λ (a est de l'ordre de λ ou plus petite), donc l'onde est diffractée."),
            "clavier": {"aides": ["a ≤ λ", "même unité", "diffraction"], "pieges": ["a > λ", "réflexion"]},
            "correction": correction([
                (f"2 : a = {a} cm ; λ = {lam} cm (même unité)", "نفس الوحدة"),
                ("a < λ : a est de l'ordre de λ ou plus petite", "a صغر من lambda"),
                ("L'onde subit une diffraction par l'ouverture", "هادي la diffraction")],
                f"Question deux. نحطو a وlambda بنفس الوحدة: a égale {mots(a)} centimètre، وlambda égale {mots(lam)} centimètre. "
                f"a صغر من lambda، إذن هادي la diffraction: l'onde كتتبدل من بعد الفتحة.")}


def q3(D):
    N, v, lam = fr(D["N"], 1), fr(D["v"], 2), fr(D["lam"], 2)
    return {"id": "3", "texte": "Déterminer la fréquence N′, la célérité v′ et la longueur d'onde λ′ de l'onde après l'ouverture. Justifier.",
            "reponse": valeur("λ′", D["lam"], "cm", f"N′ = N = {N} Hz (vibreur) ; v′ = v = {v} m/s (même milieu) ; λ′ = v′/N′ = {lam} cm"),
            "clavier": {"aides": ["N′ = N", "v′ = v", "λ′ = v′/N′", "cm"], "pieges": ["λ′ = a", "λ′ = λ/2"]},
            "correction": correction([
                (f"3 : N′ = N = {N} Hz : la fréquence est imposée par le vibreur", "la fréquence ديال le vibreur"),
                (f"v′ = v = {v} m/s : même milieu (même profondeur)", "نفس le milieu"),
                (f"λ′ = v′/N′ = {lam} cm = λ", f"lambda prime égale {mots(lam)} centimètre")],
                f"Question trois. la fréquence ديال le vibreur، وle vibreur ما تبدلش: N prime égale N، égale {mots(N)} hertz. "
                f"نفس le milieu، نفس العمق: v prime égale v، égale {mots(v)} mètre par seconde. "
                f"إذن lambda prime égale v prime sur N prime: lambda prime égale {mots(lam)} centimètre، بحال lambda.")}


def q4(D):
    lam = fr(D["lam"], 2)
    return {"id": "4", "texte": "Décrire l'onde observée après l'ouverture (forme, centre, distance entre deux crêtes voisines).",
            "reponse": phrase(f"Après l'ouverture, l'onde est circulaire : ses crêtes sont des arcs de cercle centrés sur l'ouverture O, qui se comporte comme une source ; deux crêtes voisines sont séparées de λ′ = λ = {lam} cm."),
            "clavier": {"aides": ["arcs de cercle", "centre O", "λ′ = λ"], "pieges": ["traits droits", "λ′ ≠ λ"]},
            "correction": correction([
                ("4 : l'onde diffractée est circulaire", "l'onde diffractée circulaire"),
                ("crêtes : arcs de cercle centrés sur l'ouverture O (O se comporte comme une source)", "المركز ديالها O"),
                (f"deux crêtes voisines sont distantes de λ = {lam} cm", f"بين قوس وقوس lambda، égale {mots(lam)} centimètre")],
                f"Question quatre. من بعد الفتحة، l'onde diffractée circulaire: les crêtes أقواس ديال دائرة، والمركز ديالها O، "
                f"حيت الفتحة ولات بحال la source. بين قوس وقوس lambda، égale {mots(lam)} centimètre.")}


def q5(D):
    OM, v, tau, q = fr(D["OM"], 1), fr(D["v"], 2), fr(D["tau"], 3), fr(D["q"], 1)
    e = etat(D["q"])
    return {"id": "5", "texte": "Calculer le retard τ du mouvement de M par rapport à celui du point O, puis comparer l'état vibratoire de M et de O.",
            "reponse": valeur("τ", D["tau"], "s", f"τ = OM/v′ = {OM} × 10⁻²/{v} = {tau} s"),
            "clavier": {"aides": ["τ = OM/v′", "OM/λ", "T = 1/N", "s"], "pieges": ["τ = v/OM", f"τ = {OM}/{v}"]},
            "correction": correction([
                (f"5 : τ = OM/v′ = {OM} × 10⁻²/{v}", "tau égale OM sur v prime"),
                (f"τ = {tau} s", f"tau égale {mots(tau)} seconde"),
                (f"OM/λ = {OM}/{fr(D['lam'], 2)} = {q} : M et O vibrent {e}", f"M وO vibrent {e}")],
                f"Question cinq. tau égale OM sur v prime، égale {mots(OM)} fois dix puissance moins deux، sur {mots(v)}. "
                f"tau égale {mots(tau)} seconde. ومن بعد، OM sur lambda égale {mots(q)}، إذن M وO vibrent {e}.")}


def q6(D):
    a2, lam = fr(D["a2"], 1), fr(D["lam"], 2)
    r = fr(D["a2"] / D["lam"], 1)
    return {"id": "6", "texte": f"On remplace l'ouverture par une ouverture de largeur a′ = {a2} cm. Décrire l'onde après l'ouverture. Justifier.",
            "reponse": phrase(f"a′ = {a2} cm est grande devant λ = {lam} cm (a′ ≈ {r} λ) : la diffraction n'est plus nette ; l'onde passe tout droit, rectiligne, limitée à la largeur de l'ouverture (onde diaphragmée), avec la même λ."),
            "clavier": {"aides": ["a′ ≫ λ", "onde diaphragmée", "a′/λ"], "pieges": ["diffraction nette", "rien ne passe"]},
            "correction": correction([
                (f"6 : a′ = {a2} cm ; λ = {lam} cm : a′/λ ≈ {r}, a′ est grande devant λ", "a prime كبيرة بزاف"),
                ("la diffraction n'est pas nette", "la diffraction ما كتبانش"),
                ("l'onde passe rectiligne, limitée à la largeur de l'ouverture : onde diaphragmée", "onde diaphragmée")],
                f"Question six. a prime égale {mots(a2)} centimètres، وlambda égale {mots(lam)} centimètre: a prime كبيرة بزاف على lambda. "
                f"إذن la diffraction ما كتبانش مزيان: l'onde كتدوز نيشان، rectiligne، غير بعرض الفتحة. هادي onde diaphragmée.")}


QS = [q1, q2, q3, q4, q5, q6]

TEXTE_DIT = {
    "1": "Question un: حسب la longueur d'onde lambda ديال l'onde incidente.",
    "2": f"Question deux: مع a égale {mots(fr(A['a'], 1))} centimètre، سمي الظاهرة اللي كنشوفو من بعد الفتحة، وعلل.",
    "3": "Question trois: حدد la fréquence N prime، la célérité v prime، وla longueur d'onde lambda prime من بعد الفتحة. علل.",
    "4": "Question quatre: وصف l'onde من بعد الفتحة: الشكل ديالها، المركز ديالها، والمسافة entre deux crêtes.",
    "5": "Question cinq: حسب le retard tau ديال M بالنسبة ل O، ومن بعد قارن l'état vibratoire ديال M وO.",
    "6": f"Question six: بدلنا الفتحة بفتحة أخرى، a prime égale {mots(fr(A['a2'], 1))} centimètres. وصف l'onde من بعد الفتحة، وعلل.",
}
AIDES = {
    "1": [aide("Tu as v et N. Quelle relation relie v, λ et N ?", "عندك v وعندك N. شنو la relation اللي كتجمع v وlambda وN؟"),
          aide("v = λ·N, donc λ = v/N ; le résultat est en mètre, convertis-le en cm.", "v égale lambda fois N، إذن lambda égale v sur N. النتيجة بالمتر، حولها ل centimètre.")],
    "2": [aide("Compare la largeur a de l'ouverture à λ, dans la même unité.", "قارن la largeur a ديال الفتحة مع lambda، بنفس الوحدة."),
          aide("Si a est de l'ordre de λ ou plus petite, l'onde est diffractée.", "يلا كانت a قريبة من lambda ولا صغر منها، كاينة la diffraction.")],
    "3": [aide("Qui impose la fréquence ? Le milieu a-t-il changé après l'ouverture ?", "شكون اللي كيعطي la fréquence؟ وواش le milieu تبدل من بعد الفتحة؟"),
          aide("N′ = N (vibreur), v′ = v (même milieu), donc λ′ = v′/N′.", "N prime égale N، حيت le vibreur. v prime égale v، حيت نفس le milieu. إذن lambda prime égale v prime sur N prime.")],
    "4": [aide("Après l'ouverture, d'où semblent partir les crêtes ?", "من بعد الفتحة، منين كيبانو خارجين les crêtes؟"),
          aide("L'ouverture se comporte comme une source : arcs de cercle centrés sur O, espacés de λ.", "الفتحة كتولي بحال la source: أقواس ديال دائرة، المركز ديالها O، وبين قوس وقوس lambda.")],
    "5": [aide("L'onde va de O à M à la célérité v′ : quelle durée ? Puis combien de λ entre O et M ?", "l'onde كتمشي من O ل M بla célérité v prime: شحال ديال الوقت؟ ومن بعد شحال من lambda بين O وM؟"),
          aide("τ = OM/v′ (OM en m) ; OM/λ entier : en phase ; entier et demi : en opposition.", "tau égale OM sur v prime، وOM بالمتر. OM sur lambda عدد صحيح: en phase. عدد صحيح ونص: en opposition.")],
    "6": [aide("Compare a′ à λ : combien de fois a′ est-elle plus grande ?", "قارن a prime مع lambda: شحال من مرة a prime كبيرة على lambda؟"),
          aide("Ouverture large devant λ : l'onde passe tout droit, limitée à la largeur de l'ouverture.", "الفتحة كبيرة بزاف على lambda: l'onde كتدوز نيشان، غير بعرض الفتحة.")],
}

questions = []
for i, f in enumerate(QS, 1):
    q = f(A)
    q["texte_dit"] = TEXTE_DIT[q["id"]]
    q["aides"] = AIDES[q["id"]]
    q["explication"] = f"ex_q{i}"
    q["facile"] = f"fa_q{i}"
    questions.append(q)

vA, NA, lamA, aA, a2A, OMA, tauA, qA = (fr(A["v"], 2), fr(A["N"], 1), fr(A["lam"], 2), fr(A["a"], 1), fr(A["a2"], 1),
                                        fr(A["OM"], 1), fr(A["tau"], 3), fr(A["q"], 1))

# ---------------- explication animée ----------------
m1 = (f"فالسيمولاسيون، le vibreur à vingt hertz، وla célérité zéro virgule trente mètre par seconde. "
      f"المسطرة قبل الفتحة كتعطي lambda égale un virgule cinq centimètre. نتحققو بالحساب: lambda égale v sur N، "
      f"égale zéro virgule trente sur vingt، égale un virgule cinq centimètre. "
      f"فالتمرين، lambda égale {mots(vA)} sur {mots(NA)}، égale {mots(lamA)} centimètre.")
ex1 = diapo_sim("ex_q1", "Question 1 : la longueur d'onde λ = v/N", "λ = v/N, puis on convertit en cm.",
                SIMS + "fente.html?vue=large", "λ mesurée avant l'ouverture", m1,
                [("λ = v/N", "lambda égale v sur N"), (f"λ = {vA}/{NA} = {lamA} cm", f"égale {mots(lamA)} centimètre")],
                [dict(mot="فالسيمولاسيون، le vibreur", commande="play_until", parametres={"moment": "regle_avant"}),
                 dict(mot="المسطرة قبل الفتحة", repere="regle_avant"),
                 dict(mot="lambda égale v sur N", cible="centre:0"),
                 dict(mot=f"égale {mots(lamA)} centimètre", cible="centre:1")])

m2 = (f"شوف l'onde incidente كتوصل للفتحة. فاللول الفتحة كبيرة: l'onde كتدوز نيشان. دابا نديرو الفتحة صغيرة: "
      f"a égale un centimètre، وlambda égale un virgule cinq centimètre. شوف: من بعد الفتحة، كيخرجو أقواس ديال دائرة. هادي la diffraction. "
      f"باش تعلل: a وlambda بنفس الوحدة، وa قريبة من lambda ولا صغر منها. "
      f"فالتمرين، a égale {mots(aA)} centimètre، وlambda égale {mots(lamA)} centimètre: a صغر من lambda، إذن la diffraction.")
ex2 = diapo_sim("ex_q2", "Question 2 : a comparée à λ : la diffraction", "a de l'ordre de λ ou plus petite : diffraction.",
                SIMS + "fente.html?vue=large", "Une ouverture étroite : l'onde repart en arcs de cercle", m2,
                [("a ≤ λ (même unité) → diffraction", "باش تعلل: a وlambda"), (f"a = {aA} cm < λ = {lamA} cm", "a صغر من lambda، إذن")],
                [dict(mot="شوف l'onde incidente", commande="play_until", parametres={"moment": "ouverture_atteinte"}),
                 dict(mot="دابا نديرو الفتحة صغيرة", commande="set_parameters", parametres={"a_cm": 1}),
                 dict(mot="a égale un centimètre", repere="ouverture"),
                 dict(mot="شوف: من بعد الفتحة", commande="play_until", parametres={"moment": "quatre_arcs"}),
                 dict(mot="هادي la diffraction", repere="onde_diffractee"),
                 dict(mot="باش تعلل: a وlambda", cible="centre:0"),
                 dict(mot="a صغر من lambda، إذن", cible="centre:1")])

m3 = (f"نقيسو lambda قبل الفتحة: un virgule cinq centimètre. ومن بعد الفتحة: un virgule cinq centimètre. نفس lambda. علاش؟ "
      f"la fréquence ديال le vibreur، وle vibreur ما تبدلش: N prime égale N. la célérité ديال الما، والما ما تبدلش: v prime égale v. "
      f"إذن lambda prime égale v prime sur N prime، égale lambda. فالتمرين، N prime égale {mots(NA)} hertz، "
      f"v prime égale {mots(vA)} mètre par seconde، وlambda prime égale {mots(lamA)} centimètre.")
ex3 = diapo_sim("ex_q3", "Question 3 : ce qui ne change pas", "Même fréquence, même célérité, même longueur d'onde.",
                SIMS + "fente.html?vue=etroite", "λ mesurée avant et après l'ouverture : la même", m3,
                [("N′ = N (vibreur) ; v′ = v (même milieu)", "la fréquence ديال le vibreur"), (f"λ′ = v′/N′ = λ = {lamA} cm", "إذن lambda prime égale v prime")],
                [dict(mot="نقيسو lambda قبل الفتحة", commande="play_until", parametres={"moment": "regle_avant"}),
                 dict(mot="نقيسو lambda قبل الفتحة", repere="regle_avant"),
                 dict(mot="ومن بعد الفتحة", commande="play_until", parametres={"moment": "regle_apres"}),
                 dict(mot="ومن بعد الفتحة", repere="regle_apres"),
                 dict(mot="la fréquence ديال le vibreur", cible="centre:0"),
                 dict(mot="إذن lambda prime égale v prime", cible="centre:1")])

m4 = (f"شوف من بعد الفتحة. les crêtes ماشي خطوط نيشان: أقواس ديال دائرة. المركز ديالها هو الفتحة O: الفتحة ولات بحال la source جديدة. "
      f"وبين قوس وقوس، lambda، بحال قبل الفتحة. إذن فالجواب كتب: l'onde diffractée circulaire، centrée sur O، وentre deux crêtes voisines lambda. "
      f"فالتمرين، lambda égale {mots(lamA)} centimètre.")
ex4 = diapo_sim("ex_q4", "Question 4 : décrire l'onde diffractée", "Arcs de cercle centrés sur l'ouverture, espacés de λ.",
                SIMS + "fente.html?vue=etroite", "L'ouverture se comporte comme une source", m4,
                [("onde circulaire, centrée sur O", "إذن فالجواب كتب"), (f"crêtes espacées de λ = {lamA} cm", f"فالتمرين، lambda égale {mots(lamA)}")],
                [dict(mot="شوف من بعد الفتحة", commande="play_until", parametres={"moment": "quatre_arcs"}),
                 dict(mot="المركز ديالها هو الفتحة O", repere="ouverture"),
                 dict(mot="وبين قوس وقوس", repere="onde_diffractee"),
                 dict(mot="إذن فالجواب كتب", cible="centre:0"),
                 dict(mot=f"فالتمرين، lambda égale {mots(lamA)}", cible="centre:1")])

m5 = (f"هنا la corde، ولكن نفس la règle. حطينا M بعيدة على S، SM égale un virgule cinq mètre. v égale un mètre par seconde، وT égale zéro virgule cinq seconde. "
      f"S كتتحرك الأولى. من بعد كتوصل l'onde ل M. le retard tau égale SM sur v، égale un virgule cinq seconde، يعني trois T. "
      f"وSM égale trois lambda: M وS vibrent en phase. فالتمرين، O هي la source ديال l'onde diffractée. "
      f"tau égale OM sur v prime، égale {mots(tauA)} seconde. وOM sur lambda égale {mots(qA)}: M وO vibrent {etat(A['q'])}.")
m5 = m5.replace("يعني trois T", "égale trois T")
ex5 = diapo_sim("ex_q5", "Question 5 : le retard de M, puis l'état vibratoire", "τ = OM/v′ ; OM/λ entier → en phase.",
                SIMS + "corde.html?vue=retard", "M refait le mouvement de la source avec un retard τ", m5,
                [("τ = OM/v′", "tau égale OM sur v prime"), (f"τ = {tauA} s ; OM/λ = {qA} → {etat(A['q'])}", f"M وO vibrent {etat(A['q'])}")],
                [dict(mot="حطينا M بعيدة", commande="set_parameters", parametres={"x_m": 1.5}),
                 dict(mot="S كتتحرك الأولى", commande="start"),
                 dict(mot="كتوصل l'onde ل M", commande="play_until", parametres={"moment": "front_atteint_m"}),
                 dict(mot="le retard tau égale SM sur v", repere="retard_tau"),
                 dict(mot="M وS vibrent en phase", commande="play_until", parametres={"moment": "fin"}),
                 dict(mot="tau égale OM sur v prime", cible="centre:0"),
                 dict(mot=f"M وO vibrent {etat(A['q'])}", cible="centre:1")])

m6 = (f"شوف: الفتحة صغيرة، a égale un centimètre: كاينة la diffraction. دابا نكبرو الفتحة: a égale cinq centimètres، "
      f"يعني plus de trois fois lambda. شوف: l'onde كتدوز نيشان، غير بعرض الفتحة. هادي onde diaphragmée. lambda ما تبدلاتش. "
      f"فالتمرين، a prime égale {mots(a2A)} centimètres، وlambda égale {mots(lamA)} centimètre: a prime كبيرة بزاف على lambda. "
      f"إذن onde diaphragmée، ماشي diffraction nette.")
ex6 = diapo_sim("ex_q6", "Question 6 : une ouverture large", "a′ grande devant λ : onde diaphragmée.",
                SIMS + "fente.html?vue=etroite", "On élargit l'ouverture", m6,
                [("a′ ≫ λ → onde diaphragmée", "هادي onde diaphragmée"), (f"a′ = {a2A} cm ; λ = {lamA} cm", f"فالتمرين، a prime égale {mots(a2A)}")],
                [dict(mot="شوف: الفتحة صغيرة", commande="play_until", parametres={"moment": "quatre_arcs"}),
                 dict(mot="دابا نكبرو الفتحة", commande="set_parameters", parametres={"a_cm": 5}),
                 dict(mot="شوف: l'onde كتدوز", commande="play_until", parametres={"moment": "quatre_arcs"}),
                 dict(mot="هادي onde diaphragmée", repere="onde_diffractee"),
                 dict(mot="هادي onde diaphragmée", cible="centre:0"),
                 dict(mot=f"فالتمرين، a prime égale {mots(a2A)}", cible="centre:1")])

# ---------------- version facile ----------------
fa1 = qcm_facile("fa_q1", "Plus facile : λ = v/N", "سؤال ساهل: اختار la bonne valeur ديال lambda.",
    f"v = {vA} m/s et N = {NA} Hz. La longueur d'onde vaut…",
    [f"λ = {fr(A['v'] * A['N'], 1)} m", f"λ = {lamA} cm", f"λ = {fr(A['N'] / A['v'], 1)} m"], 1, {
        "1": {"juste": rep(f"برافو! lambda égale v sur N، égale {mots(fr(A['lam'] / 100, 3))} mètre، يعني {mots(lamA)} centimètre.".replace(f"يعني {mots(lamA)}", f"c'est-à-dire {mots(lamA)}"),
                           f"Juste : λ = v/N = {vA}/{NA} = {lamA} cm.")},
        "0": {"1": rep("ما تقلقش. ضربتي v fois N. v égale lambda fois N، إذن lambda كتجي بالقسمة. عاود اختار.", "Tu as multiplié : λ = v/N, on divise. Réessaie."),
              "2": rep("الجواب: lambda égale v sur N، ماشي v fois N.", f"Réponse : λ = v/N = {lamA} cm.")},
        "2": {"1": rep("قريب، ولكن قلبتي القسمة. N sur v ماشي longueur. عاود اختار.", "N/v n'est pas une longueur : la fraction est inversée. Réessaie."),
              "2": rep("الجواب: lambda égale v sur N. v هي اللي فوق.", f"Réponse : λ = v/N = {lamA} cm.")}},
    f"v égale {mots(vA)} mètre par seconde, et N égale {mots(NA)} hertz. La longueur d'onde vaut ?")

fa2 = qcm_facile("fa_q2", "Plus facile : y a-t-il diffraction ?", "سؤال ساهل على la diffraction.",
    f"λ = {lamA} cm et a = {fr(A['a'] * 10, 1)} mm. Que se passe-t-il après l'ouverture ?",
    [f"Rien : {fr(A['a'] * 10, 1)} est plus grand que {lamA}", "On ne peut pas comparer des mm et des cm", f"Diffraction : a = {fr(A['a'], 1)} cm < λ"], 2, {
        "2": {"juste": rep("برافو! حولنا ل centimètre: a صغر من lambda، إذن كاينة la diffraction.", f"Juste : a = {aA} cm < λ = {lamA} cm : diffraction.")},
        "0": {"1": rep("ما تقلقش. قارنتي أعداد بوحدات مختلفة. حول a ل centimètre أولا. عاود اختار.", "Les deux nombres ne sont pas dans la même unité. Convertis d'abord. Réessaie."),
              "2": rep("الجواب: كاينة la diffraction. a بالسنتيمتر صغر من lambda.", f"Réponse : a = {aA} cm < λ = {lamA} cm : diffraction.")},
        "1": {"1": rep("كنقدرو نقارنو، غير خاصنا نحولو لنفس الوحدة. عاود اختار.", "On peut comparer après conversion dans la même unité. Réessaie."),
              "2": rep("الجواب: كاينة la diffraction. حول a ل centimètre، وقارن.", f"Réponse : a = {aA} cm < λ : diffraction.")}},
    "lambda et a sont donnés. Que se passe-t-il après l'ouverture ?")

fa3 = vf_facile("fa_q3", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    "Une onde est diffractée par une ouverture, dans le même milieu.", [
        ("La fréquence de l'onde diffractée est celle du vibreur.", True, "La fréquence est imposée par la source : N′ = N."),
        ("La diffraction diminue la longueur d'onde.", False, "Même milieu : v′ = v et N′ = N, donc λ′ = λ."),
        ("La célérité reste la même après l'ouverture.", True, "Le milieu (l'eau, même profondeur) n'a pas changé : v′ = v.")])

fa4 = assoc_facile("fa_q4", "Plus facile : décrire l'onde diffractée", "سؤال ساهل: ربط كل حاجة مع الوصف ديالها.",
    "Relie chaque caractéristique de l'onde diffractée à sa description.", "Relie chaque caractéristique à sa description.",
    [("1", "forme des crêtes"), ("2", "centre des crêtes"), ("3", "distance entre deux crêtes voisines")],
    [("a", "arcs de cercle"), ("b", "l'ouverture O"), ("c", "λ, la même qu'avant")],
    {"1": "a", "2": "b", "3": "c"}, {
        "1-a": (True, "Oui : après l'ouverture, les crêtes sont des arcs de cercle.", "برافو: les crêtes ولاو أقواس ديال دائرة."),
        "1-b": (False, "O est un point : c'est le centre, pas la forme.", "لا، O نقطة: هي المركز، ماشي الشكل."),
        "1-c": (False, "λ est une distance, pas une forme.", "لا، lambda مسافة، ماشي شكل."),
        "2-a": (False, "Les arcs sont la forme ; leur centre est un point.", "لا، الأقواس هوما الشكل. المركز نقطة."),
        "2-b": (True, "Oui : l'ouverture se comporte comme une source.", "برافو: الفتحة ولات بحال la source."),
        "2-c": (False, "λ est une distance, pas un centre.", "لا، lambda مسافة، ماشي مركز."),
        "3-a": (False, "La forme ne donne pas la distance.", "لا، الشكل ما كيعطيش المسافة."),
        "3-b": (False, "O est le centre, pas une distance.", "لا، O هو المركز، ماشي مسافة."),
        "3-c": (True, "Oui : λ′ = λ dans le même milieu.", "برافو: lambda prime égale lambda، نفس le milieu.")},
    ("(1 ; a) (2 ; b) (3 ; c)", "أقواس ديال دائرة، المركز ديالها O، وبين قوس وقوس lambda."))

fa5 = qcm_facile("fa_q5", "Plus facile : le retard de M", "سؤال ساهل على le retard.",
    f"OM = {OMA} cm et v′ = {vA} m/s. Le retard de M par rapport à O vaut…",
    [f"τ = {fr(A['OM'] / A['v'], 0)} s", f"τ = {tauA} s", f"τ = {fr(A['v'] / (A['OM'] * 1e-2), 2)} s"], 1, {
        "1": {"juste": rep(f"برافو! tau égale OM sur v prime، وOM بالمتر: tau égale {mots(tauA)} seconde.", f"Juste : τ = OM/v′ = {OMA} × 10⁻²/{vA} = {tauA} s.")},
        "0": {"1": rep("ما تقلقش. خليتي OM بالسنتيمتر. حولها ل mètre أولا. عاود اختار.", "OM est restée en cm : convertis-la en mètre. Réessaie."),
              "2": rep(f"الجواب: tau égale {mots(tauA)} seconde. OM بالمتر.", f"Réponse : τ = {tauA} s (OM en m).")},
        "2": {"1": rep("قريب، ولكن قلبتي القسمة: tau égale OM sur v prime. عاود اختار.", "La fraction est inversée : τ = OM/v′. Réessaie."),
              "2": rep(f"الجواب: tau égale {mots(tauA)} seconde، OM sur v prime.", f"Réponse : τ = OM/v′ = {tauA} s.")}},
    f"OM égale {mots(OMA)} centimètres. Le retard de M par rapport à O vaut ?")

fa6 = vf_facile("fa_q6", "Plus facile : une ouverture large", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    f"λ = {lamA} cm et a′ = {a2A} cm.", [
        ("L'onde passe tout droit, limitée à la largeur de l'ouverture.", True, "a′ est grande devant λ : onde diaphragmée."),
        ("Aucune onde ne passe, puisque a′ > λ.", False, "L'onde passe : seulement, elle n'est plus nettement diffractée."),
        ("La longueur d'onde après l'ouverture est toujours λ.", True, "Même milieu, même fréquence : même λ.")])

# ---------------- similaire ----------------
sim_qs = [f(B) for f in QS]

EX = {
    "id": "phys_ex_ch2_fente_5", "type": "exercice", "version": 1, "status": "published",
    "matiere": "physique", "chapitre": "ondes_mecaniques_periodiques", "cours": "phys_ch2_ondes_periodiques",
    "titre": "Une onde à la surface de l'eau devant une fente", "niveau": "moyen", "duree_min": 25,
    "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
    "competences": ["Calculer λ = v/N", "Justifier la diffraction (a comparée à λ)", "Savoir que N, v et λ ne changent pas après l'ouverture",
                    "Décrire l'onde diffractée", "Calculer un retard et comparer deux états vibratoires", "Reconnaître une onde diaphragmée"],
    "enonce": {"intro": intro(A), "intro_dit": intro_dit(A), "figures": [figure(A, "La cuve vue de dessus")],
               "donnees": donnees_txt(A), "questions": questions},
    "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [ex1, ex2, ex3, ex4, ex5, ex6]}]},
    "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [fa1, fa2, fa3, fa4, fa5, fa6]}]},
    "similaire": {"id": "phys_ex_ch2_fente_5_b", "titre": "Même exercice, autres données",
                  "enonce": {"intro": intro(B), "intro_dit": intro_dit(B), "figures": [figure(B, "La cuve vue de dessus")],
                             "donnees": donnees_txt(B), "questions": sim_qs}},
}
controler_voix(EX)
assert not PB_VOIX, "\n".join(PB_VOIX)
ecrire(EX)
