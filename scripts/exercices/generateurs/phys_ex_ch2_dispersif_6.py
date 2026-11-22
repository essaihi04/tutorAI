# Exercice de physique (ch. 2, ondes mécaniques progressives périodiques), niveau difficile (« Supérieur ») :
# la surface de l'eau à deux fréquences — λ₁, λ₂ lues sur deux photos, v₁ ≠ v₂, « montrer que » le milieu est
# dispersif, comparaison critique avec le son dans l'air (non dispersif), puis diffraction par une même ouverture
# aux deux fréquences et condition commune a ≤ λ₂.
#
# Sources comparées (skill exercices § 2) :
# - exploration ondes_mecaniques_periodiques.json : cas_types dispersif (« v = λ·N et v′ = λ′·N′ ; comparer »),
#   diffraction_justifier, lambda_aspect ; pieges (« garde la même λ quand N change et en déduit que v double »,
#   « dit que l'eau est dispersive parce que c'est de l'eau ») ; erreurs_examen 2020 R Q2 (« c'est la célérité qui
#   décide, pas la longueur d'onde ») ; a_ne_pas_dire (« célérité proportionnelle à la fréquence », « la dispersion
#   est un phénomène », son dans l'eau à 1200 m/s) ; valeurs_reperes (air 340 m/s à toute fréquence) ;
#   erreurs_des_profs (Taousse : λ gardée à 100 et 200 Hz) : c'est le piège que la question 4 fait juger.
# - vidéos des profs : bacfacile et Oussama (dispersion, diffraction), TOP PHYSIQUE (synthèse).
# - nationaux comparés : 2020 R ex. 2 Q2 (QCM « milieu non dispersif »), 2020 N Q4 et 2024 R 2.b (diffraction en
#   QCM / vrai-faux). Ici : questions ouvertes enchaînées, deux fréquences 20 et 40 Hz, une même ouverture pour les
#   deux, et un raisonnement à critiquer : aucun national n'a cette situation ni cette chaîne. Le cas type du cours
#   (devoir 20 Hz / 30 Hz) n'est pas repris.
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
def donnees(N1, d1, N2, d2, n, Nair, lam_air_cm, a_cm):
    D = {"N1": N1, "N2": N2, "d1": d1, "d2": d2, "n": n, "Nair": Nair, "Nair2": 2 * Nair, "lair": lam_air_cm, "a": a_cm}
    D["l1"], D["l2"] = d1 / n, d2 / n
    D["v1"], D["v2"] = D["l1"] * 1e-2 * N1, D["l2"] * 1e-2 * N2
    D["vair"] = lam_air_cm * 1e-2 * Nair
    D["lair2"] = D["vair"] / D["Nair2"] * 100
    D["r1"], D["r2"] = a_cm / D["l1"], a_cm / D["l2"]
    D["amax"] = min(D["l1"], D["l2"])
    return D

A = donnees(20, 6.0, 40, 3.5, 4, 1000, 34, 1.4)
B = donnees(16, 7.0, 32, 4.0, 4, 500, 68, 1.7)
assert abs(A["l2"] - 0.875) < 1e-9 and abs(A["v1"] - 0.30) < 1e-9 and abs(A["v2"] - 0.35) < 1e-9 and abs(A["lair2"] - 17) < 1e-9
assert abs(B["l1"] - 1.75) < 1e-9 and abs(B["v1"] - 0.28) < 1e-9 and abs(B["v2"] - 0.32) < 1e-9 and abs(B["lair2"] - 34) < 1e-9
for D in (A, B):
    assert D["N2"] == 2 * D["N1"] and D["r1"] <= 1 and D["r2"] > 1.5 and abs(D["vair"] - 340) < 1e-9


def figure(lam, n, d, N, num):
    S0, el = 0.5, []
    el += [{"f": "rect", "de": [0.2, 0.1], "a": [9.8, 2.9], "couleur": "faible"},
           {"f": "ligne", "pts": [[S0, 0.3], [S0, 2.7]], "couleur": "jaune", "epais": True},
           {"f": "texte", "at": [S0, 3.2], "t": "S", "couleur": "jaune", "ancre": "centre"}]
    k = 1
    while S0 + k * lam <= 9.6:
        x = round(S0 + k * lam, 3)
        el.append({"f": "ligne", "pts": [[x, 0.5], [x, 2.5]], "couleur": "blanc"})
        k += 1
    xa = round(S0 + 2 * lam, 3); xb = round(xa + n * lam, 3)
    el.append({"f": "cote", "de": [xa, 0.25], "a": [xb, 0.25], "t": f"d{'₁' if num == 1 else '₂'} = {fr(d, 1)} cm", "couleur": "cyan", "pos": "s"})
    el.append({"f": "texte", "at": [8.0, 3.2], "t": f"N{'₁' if num == 1 else '₂'} = {fr(N, 1)} Hz", "couleur": "jaune", "ancre": "centre"})
    return {"type": "schema", "titre": f"Figure {num} : photo de la surface à N{'₁' if num == 1 else '₂'} = {fr(N, 1)} Hz",
            "cadre": {"l": 10, "h": 3.5}, "legende": "Vue de dessus, échelle 1 : chaque trait clair est une crête.", "elements": el}


def intro(D):
    return (f"Une réglette S, liée à un vibreur, crée à la surface de l'eau d'une cuve à ondes une onde progressive sinusoïdale "
            f"rectiligne, sans amortissement ni réflexion. On photographie la surface (stroboscope réglé sur l'immobilité "
            f"apparente) pour deux fréquences du vibreur : N₁ = {fr(D['N1'], 1)} Hz (figure 1) puis N₂ = {fr(D['N2'], 1)} Hz "
            f"(figure 2). Sur chaque figure, la cote d va d'une crête à une autre. La profondeur de l'eau ne change pas.")


def intro_dit(D):
    return (f"دابا نقراو l'énoncé. la réglette S مربوطة مع le vibreur، وكتعطي فوق الما une onde progressive sinusoïdale rectiligne، "
            f"بلا amortissement وبلا réflexion. كنصورو الما مرتين: la fréquence N un égale {mots(fr(D['N1'], 1))} hertz، "
            f"فla figure un، ومن بعد N deux égale {mots(fr(D['N2'], 1))} hertz، فla figure deux. "
            f"ففكل figure، la cote d كتبدا من crête وكتسالي ف crête. والعمق ديال الما ما كيتبدلش.")


def donnees_txt(D):
    return [f"Figure 1 : N₁ = {fr(D['N1'], 1)} Hz ; d₁ = {fr(D['d1'], 1)} cm", f"Figure 2 : N₂ = {fr(D['N2'], 1)} Hz ; d₂ = {fr(D['d2'], 1)} cm",
            f"Son dans l'air : à {fr(D['Nair'], 0)} Hz, λ = {fr(D['lair'], 0)} cm (question 4)",
            f"Ouverture : a = {fr(D['a'], 1)} cm (questions 5 et 6)"]


def q1(D):
    n, l1, l2 = D["n"], fr(D["l1"], 2), fr(D["l2"], 3)
    return {"id": "1", "texte": "Déterminer les longueurs d'onde λ₁ (figure 1) et λ₂ (figure 2).",
            "reponse": valeur("λ₂", D["l2"], "cm", f"d₁ = {n}λ₁ : λ₁ = {fr(D['d1'], 1)}/{n} = {l1} cm ; d₂ = {n}λ₂ : λ₂ = {fr(D['d2'], 1)}/{n} = {l2} cm"),
            "clavier": {"aides": ["d = n·λ", "λ = d/n", "cm"], "pieges": [f"λ = d/{n + 1}", "λ₂ = λ₁/2"]},
            "correction": correction([
                (f"1 : chaque cote couvre {n} intervalles entre crêtes : d = {n}λ", f"d égale {mots(n)} lambda"),
                (f"λ₁ = d₁/{n} = {fr(D['d1'], 1)}/{n} = {l1} cm", f"lambda un égale {mots(l1)} centimètre"),
                (f"λ₂ = d₂/{n} = {fr(D['d2'], 1)}/{n} = {l2} cm", f"lambda deux égale {mots(l2)} centimètre")],
                f"Question un. ففكل figure، نحسبو les intervalles: d égale {mots(n)} lambda. "
                f"lambda un égale d un sur {mots(n)}: lambda un égale {mots(l1)} centimètre. "
                f"lambda deux égale d deux sur {mots(n)}: lambda deux égale {mots(l2)} centimètre.")}


def q2(D):
    l1, l2, N1, N2, v1, v2 = fr(D["l1"], 2), fr(D["l2"], 3), fr(D["N1"], 1), fr(D["N2"], 1), fr(D["v1"], 2), fr(D["v2"], 2)
    return {"id": "2", "texte": "Calculer les célérités v₁ et v₂ de l'onde pour les deux fréquences.",
            "reponse": valeur("v₂", D["v2"], "m/s", f"v₁ = λ₁·N₁ = {l1} × 10⁻² × {N1} = {v1} m/s ; v₂ = λ₂·N₂ = {l2} × 10⁻² × {N2} = {v2} m/s"),
            "clavier": {"aides": ["v = λ·N", "10⁻²", "m/s"], "pieges": ["v = λ/N", "v₂ = 2·v₁"]},
            "correction": correction([
                ("2 : v = λ·N, avec λ en mètre", "v égale lambda fois N"),
                (f"v₁ = {l1} × 10⁻² × {N1} = {v1} m/s", f"v un égale {mots(v1)} mètre par seconde"),
                (f"v₂ = {l2} × 10⁻² × {N2} = {v2} m/s", f"v deux égale {mots(v2)} mètre par seconde")],
                f"Question deux. v égale lambda fois N، وlambda بالمتر. v un égale {mots(l1)} fois dix puissance moins deux، fois {mots(N1)}: "
                f"v un égale {mots(v1)} mètre par seconde. v deux égale {mots(l2)} fois dix puissance moins deux، fois {mots(N2)}: "
                f"v deux égale {mots(v2)} mètre par seconde.")}


def q3(D):
    v1, v2 = fr(D["v1"], 2), fr(D["v2"], 2)
    return {"id": "3", "texte": "Montrer que la surface de l'eau est un milieu dispersif pour ces ondes.",
            "reponse": phrase(f"v₁ = {v1} m/s et v₂ = {v2} m/s : v₂ ≠ v₁, la célérité dépend de la fréquence ; un milieu où la célérité dépend de la fréquence est dispersif, donc la surface de l'eau est un milieu dispersif."),
            "clavier": {"aides": ["v₂ ≠ v₁", "dispersif", "la célérité dépend de N"], "pieges": ["λ₂ ≠ λ₁ donc dispersif", "c'est de l'eau"]},
            "correction": correction([
                (f"3 : v₁ = {v1} m/s ≠ v₂ = {v2} m/s", "v un ماشي هي v deux"),
                ("la célérité dépend de la fréquence", "la célérité dépend de la fréquence"),
                ("donc la surface de l'eau est un milieu dispersif", "milieu dispersif")],
                f"Question trois. v un égale {mots(v1)}، وv deux égale {mots(v2)} mètre par seconde: v un ماشي هي v deux. "
                f"إذن la célérité dépend de la fréquence. نعاود: un milieu est dispersif، si la célérité dépend de la fréquence. "
                f"إذن la surface ديال الما milieu dispersif. ورد البال: ماشي lambda اللي كتقرر، la célérité هي اللي كتقرر.")}


def q4(D):
    Na, Na2, la, la2, va = fr(D["Nair"], 0), fr(D["Nair2"], 0), fr(D["lair"], 0), fr(D["lair2"], 0), fr(D["vair"], 0)
    l1, l2h, l2 = fr(D["l1"], 2), fr(D["l1"] / 2, 3), fr(D["l2"], 3)
    return {"id": "4",
            "texte": (f"Un élève affirme : « la fréquence est multipliée par 2, donc λ₂ = λ₁/2 ». Dans l'air, un son de {Na} Hz a une "
                      f"longueur d'onde λ = {la} cm. Calculer la longueur d'onde λ′ d'un son de {Na2} Hz dans l'air, puis expliquer "
                      f"pourquoi le raisonnement de l'élève est juste pour le son dans l'air et faux pour l'eau."),
            "reponse": valeur("λ′", D["lair2"], "cm", f"v = λ·N = {fr(D['lair'] / 100, 2)} × {Na} = {va} m/s, la même à toute fréquence (air non dispersif) : λ′ = v/N′ = {va}/{Na2} = {fr(D['lair2'] / 100, 2)} m = {la2} cm"),
            "clavier": {"aides": ["v = λ·N", "λ′ = v/N′", "non dispersif", "cm"], "pieges": ["λ′ = 2λ", "λ′ = λ"]},
            "correction": correction([
                (f"4 : air : v = λ·N = {fr(D['lair'] / 100, 2)} × {Na} = {va} m/s", f"égale {mots(va)} mètre par seconde"),
                (f"l'air n'est pas dispersif : v′ = v, donc λ′ = v/N′ = {va}/{Na2} = {la2} cm = λ/2", f"lambda prime égale {mots(la2)} centimètres"),
                (f"λ = v/N donne λ/2 seulement si v ne change pas ; sur l'eau v₂ ≠ v₁ : λ₂ = {l2} cm ≠ λ₁/2 = {l2h} cm", "فالما v كتبدل")],
                f"Question quatre. فالهوا: v égale lambda fois N، égale {mots(fr(D['lair'] / 100, 2))} fois {mots(Na)}، égale {mots(va)} mètre par seconde. "
                f"l'air ماشي dispersif ل le son: v ما كتبدلش. إذن lambda prime égale v sur N prime، égale {mots(va)} sur {mots(Na2)}، "
                f"lambda prime égale {mots(la2)} centimètres، يعني النص. "
                f"lambda égale v sur N كتعطي النص غير يلا v ما تبدلاتش. فالما v كتبدل: lambda deux égale {mots(l2)} centimètre، "
                f"ماشي lambda un sur deux. إذن الكلام ديال التلميذ صحيح فالهوا، وغالط فالما.")}


def q5(D):
    a, l1, l2 = fr(D["a"], 1), fr(D["l1"], 2), fr(D["l2"], 3)
    r1, r2 = fr(D["r1"], 2), fr(D["r2"], 1)
    return {"id": "5", "texte": f"On place sur le trajet de l'onde un obstacle percé d'une ouverture de largeur a = {a} cm. Montrer que la diffraction est nette à la fréquence N₁ et nettement moins marquée à la fréquence N₂.",
            "reponse": phrase(f"À N₁ : λ₁ = {l1} cm et a = {a} cm, a < λ₁ (a/λ₁ ≈ {r1}) : diffraction nette, arcs de cercle centrés sur l'ouverture. À N₂ : λ₂ = {l2} cm, a > λ₂ (a ≈ {r2} λ₂) : a est plus grande que λ₂, l'onde passe surtout tout droit, ses bords s'arrondissent seulement ; la diffraction est moins marquée."),
            "clavier": {"aides": ["a ≤ λ", "a/λ", "même unité"], "pieges": ["a/λ ne dépend pas de N", "λ₂ = λ₁"]},
            "correction": correction([
                (f"5 : N₁ : a = {a} cm < λ₁ = {l1} cm → diffraction nette", "a صغر من lambda un"),
                (f"N₂ : a = {a} cm > λ₂ = {l2} cm (a ≈ {r2} λ₂) → diffraction moins marquée", "a كبر من lambda deux"),
                ("la diffraction dépend de a comparée à λ : à a fixée, elle est plus marquée quand λ est plus grande", "كلما كبرات lambda")],
                f"Question cinq. a égale {mots(a)} centimètre. فN un، a صغر من lambda un: la diffraction nette، أقواس ديال دائرة. "
                f"فN deux، a كبر من lambda deux: l'onde كتدوز تقريبا نيشان، غير الجناب كيتقوسو. "
                f"la diffraction كتعتمد على a بالنسبة ل lambda. وa ثابتة، إذن كلما كبرات lambda، كتبان la diffraction أكثر.")}


def q6(D):
    l1, l2, am = fr(D["l1"], 2), fr(D["l2"], 3), fr(D["amax"], 3)
    return {"id": "6", "texte": "On admet que la diffraction est nette lorsque a ≤ λ. Déterminer la plus grande largeur a_max de l'ouverture qui donne une diffraction nette aux deux fréquences.",
            "reponse": valeur("a_max", D["amax"], "cm", f"a ≤ λ₁ et a ≤ λ₂ ; λ₂ < λ₁, donc a ≤ λ₂ : a_max = λ₂ = {am} cm"),
            "clavier": {"aides": ["a ≤ λ₁", "a ≤ λ₂", "la plus petite λ"], "pieges": ["a_max = λ₁", "a_max = (λ₁ + λ₂)/2"]},
            "correction": correction([
                ("6 : il faut a ≤ λ₁ et a ≤ λ₂", "inférieur ou égal à lambda un"),
                (f"λ₂ = {l2} cm < λ₁ = {l1} cm : la condition la plus forte est a ≤ λ₂", "la plus petite"),
                (f"a_max = λ₂ = {am} cm", f"a max égale {mots(am)} centimètre")],
                f"Question six. خاص a inférieur ou égal à lambda un، وحتى inférieur ou égal à lambda deux. "
                f"lambda deux هي la plus petite. إذن a خاصها تكون inférieur ou égal à lambda deux. "
                f"a max égale lambda deux، a max égale {mots(am)} centimètre.")}


QS = [q1, q2, q3, q4, q5, q6]

TEXTE_DIT = {
    "1": "Question un: حدد lambda un من la figure un، وlambda deux من la figure deux.",
    "2": "Question deux: حسب la célérité v un وv deux، pour les deux fréquences.",
    "3": "Question trois: بين بلي la surface ديال الما milieu dispersif لهاد les ondes.",
    "4": (f"Question quatre: واحد التلميذ قال: la fréquence ضربناها fois deux، إذن lambda deux égale lambda un sur deux. "
          f"فالهوا، le son de {mots(fr(A['Nair'], 0))} hertz عندو lambda égale {mots(fr(A['lair'], 0))} centimètres. "
          f"حسب lambda prime du son de {mots(fr(A['Nair2'], 0))} hertz فالهوا، ومن بعد فسر علاش الكلام ديال التلميذ صحيح فالهوا وغالط فالما."),
    "5": f"Question cinq: حطينا حاجز فيه فتحة، la largeur a égale {mots(fr(A['a'], 1))} centimètre. بين بلي la diffraction nette فN un، وأقل بزاف فN deux.",
    "6": "Question six: كنقبلو بلي la diffraction nette ملي a inférieur ou égal à lambda. حدد أكبر largeur a max اللي كتعطي la diffraction nette pour les deux fréquences.",
}
AIDES = {
    "1": [aide("Sur chaque figure, compte les intervalles entre crêtes couverts par la cote, pas les traits.", "ففكل figure، حسب les intervalles اللي تحت la cote، ماشي les traits."),
          aide("d = n·λ, donc λ = d/n, pour chaque figure.", "d égale n fois lambda، إذن lambda égale d sur n، ففكل figure.")],
    "2": [aide("Pour chaque fréquence, utilise la longueur d'onde mesurée à cette fréquence.", "لكل fréquence، خدم ب lambda اللي قستي بهاد la fréquence."),
          aide("v = λ·N avec λ en mètre.", "v égale lambda fois N، وlambda بالمتر.")],
    "3": [aide("Compare les deux célérités calculées à la question 2.", "قارن les deux célérités اللي حسبتي."),
          aide("Un milieu est dispersif si la célérité dépend de la fréquence.", "un milieu est dispersif، si la célérité dépend de la fréquence.")],
    "4": [aide("Dans l'air, calcule v à la première fréquence. Change-t-elle avec la fréquence ?", "فالهوا، حسب v بla première fréquence. واش كتبدل مع la fréquence؟"),
          aide("λ′ = v/N′ ; λ est divisée par 2 seulement si v reste la même.", "lambda prime égale v sur N prime. lambda كتولي النص غير يلا v بقات هي هي.")],
    "5": [aide("Compare a à λ₁, puis a à λ₂, dans la même unité.", "قارن a مع lambda un، ومن بعد مع lambda deux، بنفس الوحدة."),
          aide("Diffraction nette si a est de l'ordre de λ ou plus petite ; si a est plus grande que λ, elle l'est moins.", "la diffraction nette يلا a قريبة من lambda ولا صغر منها. يلا a كبر من lambda، كتبان أقل.")],
    "6": [aide("La condition doit être vraie pour les deux longueurs d'onde à la fois.", "la condition خاصها تكون صحيحة pour les deux longueurs d'onde فمرة وحدة."),
          aide("a ≤ λ₁ et a ≤ λ₂ : c'est la plus petite des deux λ qui décide.", "a inférieur ou égal à lambda un، وa inférieur ou égal à lambda deux: lambda الصغيرة هي اللي كتقرر.")],
}

questions = []
for i, f in enumerate(QS, 1):
    q = f(A)
    q["texte_dit"] = TEXTE_DIT[q["id"]]
    q["aides"] = AIDES[q["id"]]
    q["explication"] = f"ex_q{i}"
    q["facile"] = f"fa_q{i}"
    questions.append(q)

l1A, l2A, v1A, v2A, aA, amA = fr(A["l1"], 2), fr(A["l2"], 3), fr(A["v1"], 2), fr(A["v2"], 2), fr(A["a"], 1), fr(A["amax"], 3)
N1A, N2A = fr(A["N1"], 1), fr(A["N2"], 1)

# ---------------- explication animée ----------------
URLD = SIMS + "dispersif.html"
m1 = (f"فالسيمولاسيون، نفس الما، مع les deux fréquences. نحطو la deuxième fréquence: quarante hertz. "
      f"la fréquence vingt hertz: lambda égale un virgule cinq centimètre. la fréquence quarante hertz: lambda prime égale environ zéro virgule neuf centimètre. "
      f"ماشي النص بالضبط. فالتمرين، نحسبو les intervalles: d égale {mots(A['n'])} lambda. lambda un égale {mots(l1A)} centimètre، "
      f"وlambda deux égale {mots(l2A)} centimètre.")
ex1 = diapo_sim("ex_q1", "Question 1 : deux fréquences, deux longueurs d'onde", "λ se mesure pour chaque fréquence : λ = d/n.",
                URLD, "La même eau, à deux fréquences", m1,
                [("λ = d/n", f"d égale {mots(A['n'])} lambda"), (f"λ₁ = {l1A} cm ; λ₂ = {l2A} cm", f"وlambda deux égale {mots(l2A)} centimètre")],
                [dict(mot="نحطو la deuxième fréquence", commande="set_parameters", parametres={"eau_hz": 40}),
                 dict(mot="la fréquence vingt hertz: lambda", commande="play_until", parametres={"moment": "eau_1"}),
                 dict(mot="la fréquence vingt hertz: lambda", repere="eau_1"),
                 dict(mot="la fréquence quarante hertz: lambda prime", commande="play_until", parametres={"moment": "eau_2"}),
                 dict(mot="la fréquence quarante hertz: lambda prime", repere="eau_2"),
                 dict(mot=f"d égale {mots(A['n'])} lambda", cible="centre:0"),
                 dict(mot=f"وlambda deux égale {mots(l2A)} centimètre", cible="centre:1")])

m2 = (f"نحسبو la célérité لكل fréquence: v égale lambda fois N. فالسيمولاسيون، la fréquence vingt hertz: v égale zéro virgule trente mètre par seconde. "
      f"la fréquence quarante hertz: v prime égale zéro virgule trente-cinq mètre par seconde. "
      f"فالتمرين، v un égale {mots(l1A)} fois dix puissance moins deux، fois {mots(N1A)}، égale {mots(v1A)} mètre par seconde. "
      f"وv deux égale {mots(l2A)} fois dix puissance moins deux، fois {mots(N2A)}، égale {mots(v2A)} mètre par seconde.")
ex2 = diapo_sim("ex_q2", "Question 2 : une célérité pour chaque fréquence", "v = λ·N, avec la λ mesurée à cette fréquence.",
                URLD, "v = λ·N calculée pour chaque fréquence", m2,
                [("v = λ · N (λ en m)", "v égale lambda fois N. فالسيمولاسيون"), (f"v₁ = {v1A} m/s ; v₂ = {v2A} m/s", f"égale {mots(v2A)} mètre par seconde.")],
                [dict(mot="نحسبو la célérité", commande="set_parameters", parametres={"eau_hz": 40}),
                 dict(mot="v égale lambda fois N. فالسيمولاسيون", cible="centre:0"),
                 dict(mot="la fréquence quarante hertz: v prime", commande="play_until", parametres={"moment": "eau_2"}),
                 dict(mot="la fréquence quarante hertz: v prime", repere="v_eau"),
                 dict(mot=f"égale {mots(v2A)} mètre par seconde.", cible="centre:1")])

m3 = (f"شوف: فالما، la célérité تبدلات ملي تبدلات la fréquence. فالهوا، la célérité بقات v égale trois cent quarante mètres par seconde. "
      f"نعاود نقرا: un milieu est dispersif, si la célérité de l'onde, dépend de sa fréquence. "
      f"إذن la surface ديال الما milieu dispersif، والهوا ماشي dispersif ل le son. "
      f"فالتمرين، v un égale {mots(v1A)}، وv deux égale {mots(v2A)} mètre par seconde: v deux ماشي هي v un، إذن milieu dispersif. "
      f"ورد البال: lambda ديما كتبدل مع la fréquence، حتى فالهوا. اللي كيقرر هو la célérité.")
ex3 = diapo_sim("ex_q3", "Question 3 : montrer que l'eau est dispersive", "Dispersif : la célérité dépend de la fréquence.",
                URLD, "L'eau dispersive, l'air non dispersif", m3,
                [("Dispersif : v dépend de N", "نعاود نقرا: un milieu est dispersif"), (f"v₂ = {v2A} m/s ≠ v₁ = {v1A} m/s → dispersif", "إذن milieu dispersif")],
                [dict(mot="شوف: فالما", commande="play_until", parametres={"moment": "eau_2"}),
                 dict(mot="شوف: فالما", repere="v_eau"),
                 dict(mot="فالهوا، la célérité بقات", commande="play_until", parametres={"moment": "air_2"}),
                 dict(mot="فالهوا، la célérité بقات", repere="v_air"),
                 dict(mot="نعاود نقرا: un milieu est dispersif", cible="centre:0"),
                 dict(mot="إذن la surface ديال الما", commande="play_until", parametres={"moment": "verdict"}),
                 dict(mot="إذن la surface ديال الما", repere="verdict_eau"),
                 dict(mot="إذن milieu dispersif", cible="centre:1")])

m4 = (f"دابا فالهوا. la fréquence mille hertz: lambda égale trente-quatre centimètres. la fréquence deux mille hertz: lambda égale dix-sept centimètres. "
      f"v égale zéro virgule trente-quatre fois mille، égale trois cent quarante mètres par seconde. "
      f"وزيرو virgule dix-sept fois deux mille، كتعطي حتى هي v égale trois cent quarante mètres par seconde. "
      f"la fréquence ضربناها fois deux، وlambda ولات النص، حيت la célérité بقات هي هي. "
      f"فالما، la célérité تبدلات: lambda deux égale {mots(l2A)} centimètre، ماشي النص ديال lambda un.")
m4 = m4.replace("وزيرو virgule", "et zéro virgule")
ex4 = diapo_sim("ex_q4", "Question 4 : dans l'air, λ divisée par 2", "Air non dispersif : v fixe, donc λ′ = λ/2 quand N double.",
                SIMS + "air.html?vue=comparaison", "Le son à 1000 Hz et à 2000 Hz", m4,
                [("v = λ·N = 340 m/s aux deux fréquences", "v égale zéro virgule trente-quatre fois mille"),
                 (f"eau : λ₂ = {l2A} cm ≠ λ₁/2", "فالما، la célérité تبدلات")],
                [dict(mot="دابا فالهوا", commande="play_until", parametres={"moment": "mesure_lambda"}),
                 dict(mot="la fréquence mille hertz: lambda", repere="lambda_1000"),
                 dict(mot="la fréquence deux mille hertz: lambda", commande="play_until", parametres={"moment": "comparaison"}),
                 dict(mot="la fréquence deux mille hertz: lambda", repere="lambda_2000"),
                 dict(mot="v égale zéro virgule trente-quatre fois mille", cible="centre:0"),
                 dict(mot="حيت la célérité بقات هي هي", repere="conclusion"),
                 dict(mot="فالما، la célérité تبدلات", cible="centre:1")])

m5 = (f"فالسيمولاسيون، lambda égale un virgule cinq centimètre. الفتحة صغيرة، a égale un centimètre: a صغر من lambda، أقواس ديال دائرة: la diffraction nette. "
      f"دابا نكبرو الفتحة: a égale trois centimètres، deux fois lambda. شوف: l'onde كتدوز تقريبا نيشان، غير الجناب كيتقوسو. "
      f"اللي كيهم هو a بالنسبة ل lambda. فالتمرين، a ثابتة، وlambda هي اللي كتبدل: a égale {mots(aA)} centimètre، "
      f"lambda un égale {mots(l1A)}، وlambda deux égale {mots(l2A)} centimètre. فN un، a صغر من lambda un: nette. فN deux، a كبر من lambda deux: أقل.")
ex5 = diapo_sim("ex_q5", "Question 5 : a comparée à λ₁ puis à λ₂", "C'est a comparée à λ qui compte.",
                SIMS + "fente.html?vue=etroite", "Ouverture étroite puis plus large devant λ", m5,
                [("a ≤ λ → diffraction nette", "a صغر من lambda، أقواس"), (f"a = {aA} cm : a < λ₁ = {l1A} cm ; a > λ₂ = {l2A} cm", "فN un، a صغر من lambda un")],
                [dict(mot="الفتحة صغيرة، a égale", commande="play_until", parametres={"moment": "quatre_arcs"}),
                 dict(mot="الفتحة صغيرة، a égale", repere="ouverture"),
                 dict(mot="a صغر من lambda، أقواس", cible="centre:0"),
                 dict(mot="دابا نكبرو الفتحة", commande="set_parameters", parametres={"a_cm": 3}),
                 dict(mot="شوف: l'onde كتدوز", commande="play_until", parametres={"moment": "quatre_arcs"}),
                 dict(mot="شوف: l'onde كتدوز", repere="onde_diffractee"),
                 dict(mot="فN un، a صغر من lambda un", cible="centre:1")])

m6 = (f"فالسيمولاسيون، lambda égale un virgule cinq centimètre. نديرو a égale un virgule cinq centimètre: a égale lambda، والأقواس باقيين: la diffraction nette. "
      f"فالتمرين، عندنا les deux longueurs d'onde. خاص a inférieur ou égal à lambda un، وحتى inférieur ou égal à lambda deux. "
      f"lambda deux هي la plus petite، إذن هي اللي كتقرر. a max égale lambda deux، égale {mots(amA)} centimètre.")
ex6 = diapo_sim("ex_q6", "Question 6 : la plus grande ouverture qui diffracte aux deux fréquences", "a ≤ λ₁ et a ≤ λ₂ : la plus petite λ décide.",
                SIMS + "fente.html?vue=etroite", "a = λ : la diffraction est encore nette", m6,
                [("a ≤ λ₁ et a ≤ λ₂", "خاص a inférieur ou égal"), (f"a_max = λ₂ = {amA} cm", "a max égale lambda deux")],
                [dict(mot="نديرو a égale un virgule cinq", commande="set_parameters", parametres={"a_cm": 1.5}),
                 dict(mot="والأقواس باقيين", commande="play_until", parametres={"moment": "quatre_arcs"}),
                 dict(mot="والأقواس باقيين", repere="onde_diffractee"),
                 dict(mot="خاص a inférieur ou égal", cible="centre:0"),
                 dict(mot="a max égale lambda deux", cible="centre:1")])

# ---------------- version facile ----------------
fa1 = qcm_facile("fa_q1", "Plus facile : λ₂ sur la figure 2", "سؤال ساهل: حسب lambda deux.",
    f"Sur la figure 2, la cote d₂ = {fr(A['d2'], 1)} cm va d'une crête à la cinquième crête suivante… non : elle couvre {A['n']} intervalles. λ₂ vaut…".replace("va d'une crête à la cinquième crête suivante… non : elle ", ""),
    [f"λ₂ = {fr(A['d2'] / (A['n'] + 1), 2)} cm", f"λ₂ = {l2A} cm", f"λ₂ = {fr(A['l1'] / 2, 2)} cm"], 1, {
        "1": {"juste": rep(f"برافو! d deux égale {mots(A['n'])} lambda deux، إذن lambda deux égale {mots(l2A)} centimètre.", f"Juste : λ₂ = d₂/{A['n']} = {l2A} cm.")},
        "0": {"1": rep("ما تقلقش. قسمتي على عدد les crêtes، ماشي les intervalles. عاود اختار.", "Tu as divisé par le nombre de crêtes, pas d'intervalles. Réessaie."),
              "2": rep(f"الجواب: lambda deux égale {mots(l2A)} centimètre. d deux sur {mots(A['n'])}.", f"Réponse : λ₂ = d₂/{A['n']} = {l2A} cm.")},
        "2": {"1": rep("لا، هادي lambda un sur deux. lambda deux خاصها تتقاس فla figure deux. عاود اختار.", "C'est λ₁/2 : λ₂ se mesure sur la figure 2. Réessaie."),
              "2": rep(f"الجواب: lambda deux égale {mots(l2A)} centimètre، مقيوسة فla figure deux.", f"Réponse : λ₂ = {l2A} cm, mesurée sur la figure 2.")}},
    f"La cote d deux couvre {mots(A['n'])} intervalles. Lambda deux vaut ?")

fa2 = vf_facile("fa_q2", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    f"λ₂ = {l2A} cm et N₂ = {N2A} Hz.", [
        (f"v₂ = λ₂·N₂ = {l2A} × 10⁻² × {N2A} = {v2A} m/s", True, "λ₂ convertie en mètre, puis multipliée par N₂."),
        (f"v₂ = 2·v₁ puisque N₂ = 2·N₁", False, "La célérité n'est pas proportionnelle à la fréquence : on la calcule avec la λ mesurée."),
        (f"v₂ = {l2A} × {N2A} = {fr(A['l2'] * A['N2'], 0)} m/s", False, "λ₂ est restée en cm : il faut la convertir en mètre.")])

fa3 = qcm_facile("fa_q3", "Plus facile : milieu dispersif", "سؤال ساهل على milieu dispersif.",
    "Un milieu est dispersif si…",
    ["la longueur d'onde dépend de la fréquence", "l'onde s'y amortit", "la célérité de l'onde dépend de sa fréquence"], 2, {
        "2": {"juste": rep("برافو! un milieu est dispersif، si la célérité dépend de la fréquence.", "Juste : dispersif = la célérité dépend de la fréquence.")},
        "0": {"1": rep("ما تقلقش. lambda ديما كتبدل مع la fréquence، حتى فالهوا. شنو اللي كيقرر؟ عاود اختار.", "λ change toujours avec N, même dans l'air. Qu'est-ce qui décide ? Réessaie."),
              "2": rep("الجواب: la célérité هي اللي كتقرر. lambda كتبدل ديما.", "Réponse : la célérité dépend de la fréquence.")},
        "1": {"1": rep("لا، l'amortissement حاجة أخرى: l'amplitude كتنقص. عاود اختار.", "L'amortissement concerne l'amplitude, pas la dispersion. Réessaie."),
              "2": rep("الجواب: la célérité dépend de la fréquence. l'amortissement ماشي هو dispersif.", "Réponse : la célérité dépend de la fréquence.")}},
    "Un milieu est dispersif si ?")

fa4 = assoc_facile("fa_q4", "Plus facile : air ou eau ?", "سؤال ساهل: ربط كل milieu مع اللي كيوقع ملي la fréquence كتضرب fois deux.",
    "Quand la fréquence est multipliée par 2…", "Relie chaque milieu à ce qui arrive.",
    [("1", "le son dans l'air"), ("2", "les rides à la surface de l'eau")],
    [("a", "v ne change pas, λ est divisée par 2"), ("b", "v change, λ n'est pas exactement divisée par 2"), ("c", "λ ne change pas")],
    {"1": "a", "2": "b"}, {
        "1-a": (True, "Oui : l'air n'est pas dispersif pour le son.", "برافو: l'air ماشي dispersif، v بقات هي هي."),
        "1-b": (False, "Dans l'air, v = 340 m/s à toute fréquence.", "لا، فالهوا v égale trois cent quarante mètres par seconde ديما."),
        "1-c": (False, "λ = v/N change quand N change.", "لا، lambda égale v sur N، كتبدل ملي N كتبدل."),
        "2-a": (False, "Sur l'eau, v change avec N : milieu dispersif.", "لا، فالما v كتبدل مع N: milieu dispersif."),
        "2-b": (True, "Oui : milieu dispersif, on remesure λ.", "برافو: milieu dispersif، خاصنا نعاودو نقيسو lambda."),
        "2-c": (False, "λ change toujours quand N change.", "لا، lambda كتبدل ديما ملي N كتبدل.")},
    ("(1 ; a) (2 ; b)", "فالهوا v ثابتة وlambda النص. فالما v كتبدل."))

fa5 = qcm_facile("fa_q5", "Plus facile : quand la diffraction est-elle nette ?", "سؤال ساهل على la diffraction.",
    f"a = {aA} cm. Pour quelle longueur d'onde la diffraction est-elle la plus nette ?",
    [f"λ₂ = {l2A} cm", f"λ₁ = {l1A} cm", "La même pour les deux"], 1, {
        "1": {"juste": rep("برافو! lambda un كبر من a: la diffraction nette.", f"Juste : a < λ₁ : diffraction nette.")},
        "0": {"1": rep("ما تقلقش. a كبر من lambda deux. la diffraction nette ملي a صغر من lambda. عاود اختار.", "a > λ₂ : la diffraction est moins marquée. Réessaie."),
              "2": rep("الجواب: lambda un. a صغر من lambda un.", f"Réponse : λ₁ = {l1A} cm, car a < λ₁.")},
        "2": {"1": rep("لا، la diffraction كتعتمد على a بالنسبة ل lambda، وlambda تبدلات. عاود اختار.", "La diffraction dépend de a comparée à λ, et λ a changé. Réessaie."),
              "2": rep("الجواب: lambda un، حيت a صغر منها.", f"Réponse : λ₁ (a < λ₁).")}},
    f"a égale {mots(aA)} centimètre. Pour quelle longueur d'onde la diffraction est-elle la plus nette ?")

fa6 = qcm_facile("fa_q6", "Plus facile : la condition pour deux λ", "سؤال ساهل: شمن lambda كتقرر؟",
    "Il faut a ≤ λ₁ et a ≤ λ₂, avec λ₂ < λ₁. Alors a_max vaut…",
    ["λ₁", "λ₂", "λ₁ + λ₂"], 1, {
        "1": {"juste": rep("برافو! lambda الصغيرة هي اللي كتقرر: a max égale lambda deux.", "Juste : a_max = λ₂, la plus petite.")},
        "0": {"1": rep("ما تقلقش. يلا a égale lambda un، واش a inférieur ou égal à lambda deux؟ عاود اختار.", "Avec a = λ₁, a > λ₂ : la condition n'est pas vérifiée. Réessaie."),
              "2": rep("الجواب: lambda deux. خاص الجوج يكونو صحاح.", "Réponse : a_max = λ₂.")},
        "2": {"1": rep("لا، هادي كبيرة على les deux lambda. عاود اختار.", "C'est plus grand que les deux λ. Réessaie."),
              "2": rep("الجواب: lambda deux، la plus petite.", "Réponse : a_max = λ₂.")}},
    "Il faut a inférieur ou égal à lambda un, et à lambda deux. Alors a max vaut ?")

sim_qs = [f(B) for f in QS]

EX = {
    "id": "phys_ex_ch2_dispersif_6", "type": "exercice", "version": 1, "status": "published",
    "matiere": "physique", "chapitre": "ondes_mecaniques_periodiques", "cours": "phys_ch2_ondes_periodiques",
    "titre": "L'eau, un milieu dispersif, et la diffraction à deux fréquences", "niveau": "difficile", "duree_min": 35,
    "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
    "competences": ["Lire λ sur une photo (d = n·λ)", "Calculer v = λ·N pour deux fréquences", "Montrer qu'un milieu est dispersif",
                    "Comparer avec le son dans l'air (non dispersif)", "Justifier la diffraction en comparant a et λ",
                    "Combiner deux conditions de diffraction"],
    "enonce": {"intro": intro(A), "intro_dit": intro_dit(A),
               "figures": [figure(A["l1"], A["n"], A["d1"], A["N1"], 1), figure(A["l2"], A["n"], A["d2"], A["N2"], 2)],
               "donnees": donnees_txt(A), "questions": questions},
    "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [ex1, ex2, ex3, ex4, ex5, ex6]}]},
    "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [fa1, fa2, fa3, fa4, fa5, fa6]}]},
    "similaire": {"id": "phys_ex_ch2_dispersif_6_b", "titre": "Même exercice, autres données",
                  "enonce": {"intro": intro(B), "intro_dit": intro_dit(B),
                             "figures": [figure(B["l1"], B["n"], B["d1"], B["N1"], 1), figure(B["l2"], B["n"], B["d2"], B["N2"], 2)],
                             "donnees": donnees_txt(B), "questions": sim_qs}},
}
controler_voix(EX)
assert not PB_VOIX, "\n".join(PB_VOIX)
ecrire(EX)
