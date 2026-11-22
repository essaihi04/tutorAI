# Exercice de physique (ch. 2, ondes mécaniques progressives périodiques), niveau moyen :
# cuve à ondes éclairée par un stroboscope — immobilité apparente, λ sur une photo, v, retard, états vibratoires.
#
# Sources comparées (skill exercices § 2) :
# - exploration ondes_mecaniques_periodiques.json : cas_types strobo_immobilite (« N = N_éclairs », 0 national, devoirs),
#   lambda_aspect (compter les intervalles, λ = d/n), celerite_lambda_N, retard_periodique, phase_opposition ;
#   pieges (traits comptés au lieu des intervalles, cote d prise pour SM, λ laissée en cm, « virgule donc opposition ») ;
#   exclus_hors_programme (fréquence apparente, mouvement ralenti : non demandés ici) ; valeurs_reperes (cuve 0,2–0,4 m/s).
# - vidéos des profs (sources.videos) : Taousse (stroboscopie 10 min), mouhibi (cuve + stroboscope en devoir),
#   Oussama (k ∈ ℕ*), erreurs_des_profs (Laksabi 5 mm = 5×10⁻² m) : évitées.
# - nationaux comparés : 2019 N ex. 2 (cuve 20 Hz, λ = 1,5 cm, V = 0,3 m/s, τ = 2T), 2020 N ex. II (v = 0,25 m/s,
#   1 cm = 2λ, N = v/λ), 2017 N ex. II (coupe, λ, v, instant). Ici : pas de national — N vient du stroboscope
#   (N = k·N_e), autre fréquence (25 Hz), λ = 1,2 cm compté sur 5 intervalles, retard 3,5 T et comparaison M/P.
# - séries en ligne : la recherche (WebSearch) a donné les titres de séries talamidi, moutamadris, alloschool,
#   Jenkal, Ajitfham (étude stroboscopique, deux microphones) ; leur lecture (WebFetch) est bloquée par le réseau de
#   la session (ENOTFOUND) : exercice écrit d'après l'exploration et les nationaux.
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


SIMS = "/media/simulations/physics/ondes-periodiques-tableau/"

# ---------------- données (calculées) ----------------
def donnees(N, k2, lam_cm, n_int, SM_cm, SP_cm):
    D = {"N": N, "Ne1": N, "Ne2": N / k2, "k2": k2, "lam": lam_cm, "n": n_int, "d": n_int * lam_cm,
         "SM": SM_cm, "SP": SP_cm}
    D["T"] = 1 / N
    D["v"] = lam_cm * 1e-2 * N
    D["tau"] = SM_cm * 1e-2 / D["v"]
    D["tauT"] = D["tau"] / D["T"]
    D["MP"] = SP_cm - SM_cm
    D["q"] = D["MP"] / lam_cm
    return D

A = donnees(25, 2, 1.2, 5, 4.2, 7.2)
B = donnees(30, 2, 1.0, 4, 3.0, 5.0)
assert abs(A["v"] - 0.30) < 1e-9 and abs(A["tau"] - 0.14) < 1e-9 and abs(A["tauT"] - 3.5) < 1e-9 and abs(A["q"] - 2.5) < 1e-9
assert abs(B["v"] - 0.30) < 1e-9 and abs(B["tau"] - 0.10) < 1e-9 and abs(B["tauT"] - 3) < 1e-9 and abs(B["q"] - 2) < 1e-9


def figure(D, titre):
    S0, lam = 0.6, D["lam"]
    el = [{"f": "rect", "de": [0.2, 0.1], "a": [10.8, 4.9], "couleur": "faible"},
          {"f": "ligne", "pts": [[S0, 0.4], [S0, 4.6]], "couleur": "jaune", "epais": True},
          {"f": "texte", "at": [S0, 5.2], "t": "S (réglette)", "couleur": "jaune", "ancre": "centre"},
          {"f": "ligne", "pts": [[S0, 2.5], [10.6, 2.5]], "couleur": "faible", "trait": "pointille"}]
    k = 1
    while S0 + k * lam <= 10.65:
        x = round(S0 + k * lam, 3)
        el.append({"f": "ligne", "pts": [[x, 0.6], [x, 4.4]], "couleur": "blanc"})
        k += 1
    k0 = 2 if lam > 1.1 else 3
    xa, xb = round(S0 + k0 * lam, 3), round(S0 + (k0 + D["n"]) * lam, 3)
    el.append({"f": "cote", "de": [xa, 0.3], "a": [xb, 0.3], "t": f"d = {fr(D['d'], 1)} cm", "couleur": "cyan", "pos": "s"})
    el.append({"f": "point", "at": [round(S0 + D["SM"], 3), 2.5], "t": "M", "pos": "no", "couleur": "orange"})
    el.append({"f": "point", "at": [round(S0 + D["SP"], 3), 2.5], "t": "P", "pos": "no", "couleur": "rose"})
    el.append({"f": "fleche", "de": [7.0, 4.65], "a": [9.5, 4.65], "texte": "propagation", "couleur": "faible", "pos": "n"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 11, "h": 5.6},
            "legende": "Photo prise sous l'éclairage stroboscopique, vue de dessus, à l'échelle 1 : chaque trait clair est une crête.",
            "elements": el}


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


# ---------------- énoncé ----------------
def intro(D):
    return (f"Le vibreur d'une cuve à ondes, de fréquence N inconnue, frappe la surface de l'eau avec une réglette S : "
            f"des ondes rectilignes se propagent sans amortissement ni réflexion. On éclaire la cuve avec un stroboscope "
            f"dont la fréquence des éclairs N_e est réglable. La plus grande fréquence des éclairs qui donne l'immobilité "
            f"apparente de la surface est N_e = {fr(D['Ne1'], 1)} Hz ; on observe aussi l'immobilité pour "
            f"N_e = {fr(D['Ne2'], 1)} Hz. La figure est une photo de la surface sous cet éclairage : la cote d couvre "
            f"plusieurs crêtes. M et P sont deux points de la surface, sur la direction de propagation.")


def intro_dit(D):
    return (f"دابا نقراو l'énoncé. عندنا une cuve à ondes، le vibreur كيضرب الما بواحد la réglette S، "
            f"وla fréquence ديالو N ما معروفاش. les ondes rectilignes كيمشيو بلا amortissement وبلا réflexion. "
            f"كنضويو la cuve بواحد le stroboscope، وla fréquence ديال الضوء N e كنبدلوها. "
            f"أكبر fréquence ديال الضوء اللي كتعطي l'immobilité apparente، N e égale {mots(fr(D['Ne1'], 1))} hertz. "
            f"وكنشوفو l'immobilité حتى ملي N e égale {mots(fr(D['Ne2'], 1))} hertz. "
            f"la figure هي تصويرة ديال الما: la cote d فوق بزاف ديال les crêtes. وM وP جوج نقط فالما.")


def donnees_txt(D):
    return [f"Immobilité apparente : N_e = {fr(D['Ne1'], 1)} Hz (la plus grande) et N_e = {fr(D['Ne2'], 1)} Hz",
            f"Sur la figure : d = {fr(D['d'], 1)} cm (photo à l'échelle 1)",
            f"SM = {fr(D['SM'], 1)} cm ; SP = {fr(D['SP'], 1)} cm"]


def etat(q):
    if abs(q - round(q)) < 1e-9:
        return "en phase"
    if abs(q - round(q - 0.5) - 0.5) < 1e-9:
        return "en opposition de phase"
    return "ni en phase ni en opposition de phase"


# Réponses communes à l'exercice et au similaire (reponse, clavier, correction)
def q1(D, sim=False):
    N = fr(D["N"], 1)
    return {"id": "1", "texte": "Expliquer l'immobilité apparente de la surface, puis déterminer la fréquence N du vibreur.",
            "reponse": valeur("N", D["N"], "Hz", f"Immobilité si N = k·N_e ; la plus grande N_e correspond à k = 1, donc N = N_e = {N} Hz"),
            "clavier": {"aides": ["N = k·N_e", "k = 1", "Hz"], "pieges": ["N = N_e/k", f"N = {fr(D['Ne2'], 1)} Hz"]},
            "correction": correction([
                (f"1 : entre deux éclairs, chaque crête avance d'un nombre entier de λ : l'image est la même, la surface paraît immobile", "l'image هي هي"),
                ("Condition : N = k·N_e (k entier) ; la plus grande N_e donne k = 1", "N égale k fois N e"),
                (f"N = N_e = {N} Hz", f"N égale {mots(N)} hertz")],
                f"Question un. بين ضوء وضوء، كل crête كتمشي عدد صحيح ديال lambda، إذن l'image هي هي، والما كيبان واقف. "
                f"la condition: N égale k fois N e، وk عدد صحيح. أكبر N e كتعطي k égale un. إذن N égale {mots(N)} hertz.")}


def q2(D):
    lam, d, n = fr(D["lam"], 2), fr(D["d"], 1), D["n"]
    return {"id": "2", "texte": "Déterminer la longueur d'onde λ à partir de la figure.",
            "reponse": valeur("λ", D["lam"], "cm", f"d = {n}λ donc λ = d/{n} = {d}/{n} = {lam} cm"),
            "clavier": {"aides": ["d = n·λ", "λ = d/n", "cm"], "pieges": [f"λ = d/{n + 1}", "λ = d"]},
            "correction": correction([
                (f"2 : la cote d couvre {n} intervalles entre crêtes : d = {n}λ", f"d égale {mots(n)} lambda"),
                (f"λ = d/{n} = {d}/{n}", "lambda égale d sur"),
                (f"λ = {lam} cm", f"lambda égale {mots(lam)} centimètre")],
                f"Question deux. نحسبو les intervalles بين les crêtes، ماشي les traits: d égale {mots(n)} lambda. "
                f"إذن lambda égale d sur {mots(n)}، égale {mots(d)} sur {mots(n)}. lambda égale {mots(lam)} centimètre.")}


def q3(D):
    lam, N, v = fr(D["lam"], 2), fr(D["N"], 1), fr(D["v"], 2)
    return {"id": "3", "texte": "Calculer la célérité v de l'onde à la surface de l'eau.",
            "reponse": valeur("v", D["v"], "m/s", f"v = λ·N = {lam} × 10⁻² × {N} = {v} m/s"),
            "clavier": {"aides": ["v = λ·N", "10⁻²", "m/s"], "pieges": ["v = λ/N", f"v = {lam} × {N}"]},
            "correction": correction([
                ("3 : v = λ·N, avec λ en mètre", "v égale lambda fois N"),
                (f"v = {lam} × 10⁻² × {N}", f"{mots(lam)} fois dix puissance moins deux"),
                (f"v = {v} m/s", f"v égale {mots(v)} mètre par seconde")],
                f"Question trois. la relation: v égale lambda fois N، وlambda بالمتر. l'application numérique: "
                f"v égale {mots(lam)} fois dix puissance moins deux، fois {mots(N)}. v égale {mots(v)} mètre par seconde.")}


def q4(D):
    SM, v, tau, tT = fr(D["SM"], 1), fr(D["v"], 2), fr(D["tau"], 2), fr(D["tauT"], 1)
    return {"id": "4", "texte": f"Montrer que le retard du mouvement de M par rapport à celui de S vaut τ = {tT} T, puis calculer τ.",
            "reponse": valeur("τ", D["tau"], "s", f"τ = SM/v = {SM} × 10⁻²/{v} = {tau} s"),
            "clavier": {"aides": ["τ = SM/v", "T = 1/N", "SM/λ", "s"], "pieges": ["τ = v/SM", f"τ = {SM}/{v}"]},
            "correction": correction([
                (f"4 : SM/λ = {SM}/{fr(D['lam'], 2)} = {tT}, donc SM = {tT} λ et τ = SM/v = {tT} λ/v = {tT} T", f"SM égale {mots(tT)} lambda"),
                (f"τ = SM/v = {SM} × 10⁻²/{v}", "tau égale SM sur v"),
                (f"τ = {tau} s", f"tau égale {mots(tau)} seconde")],
                f"Question quatre. SM sur lambda égale {mots(tT)}، إذن SM égale {mots(tT)} lambda. وlambda sur v هي T، "
                f"إذن tau égale {mots(tT)} T. l'application numérique: tau égale SM sur v، égale {mots(SM)} fois dix puissance moins deux، "
                f"sur {mots(v)}. tau égale {mots(tau)} seconde.")}


def q5(D):
    MP, lam, q = fr(D["MP"], 1), fr(D["lam"], 2), fr(D["q"], 1)
    e = etat(D["q"])
    entier = abs(D["q"] - round(D["q"])) < 1e-9
    forme = f"MP = {q} λ (entier)" if entier else f"MP = {q} λ = (2k + 1)·λ/2 avec k = {int(D['q'] - 0.5)}"
    dit_e = "en phase" if entier else "en opposition de phase"
    return {"id": "5", "texte": "Comparer les états vibratoires des points M et P. Justifier.",
            "reponse": phrase(f"MP = SP − SM = {MP} cm ; MP/λ = {MP}/{lam} = {q} ; {forme} : M et P vibrent {e}."),
            "clavier": {"aides": ["MP = SP − SM", "MP/λ", "d = k·λ", "d = (2k + 1)·λ/2"], "pieges": ["SP/λ", "nombre à virgule → opposition"]},
            "correction": correction([
                (f"5 : MP = SP − SM = {fr(D['SP'], 1)} − {fr(D['SM'], 1)} = {MP} cm", "MP égale SP moins SM"),
                (f"MP/λ = {MP}/{lam} = {q}", "MP sur lambda"),
                (f"{forme} : M et P vibrent {e}", f"M وP vibrent {dit_e}")],
                f"Question cinq. MP égale SP moins SM، égale {mots(MP)} centimètre. MP sur lambda égale {mots(MP)} sur {mots(lam)}، "
                f"égale {mots(q)}. " + ("هادا عدد صحيح، " if entier else "هادا عدد صحيح ونص، ") + f"إذن M وP vibrent {dit_e}.")}


QS = [q1, q2, q3, q4, q5]

# ---------------- aides et voix des questions (exercice principal) ----------------
TEXTE_DIT = {
    "1": "Question un: فسر l'immobilité apparente ديال الما، ومن بعد حدد la fréquence N ديال le vibreur.",
    "2": "Question deux: حدد la longueur d'onde lambda من la figure.",
    "3": "Question trois: حسب la célérité v ديال l'onde فوق الما.",
    "4": f"Question quatre: بين بلي le retard ديال M بالنسبة ل S هو tau égale {mots(fr(A['tauT'], 1))} T، ومن بعد حسب tau.",
    "5": "Question cinq: قارن l'état vibratoire ديال M وP. علل.",
}
AIDES = {
    "1": [aide("Entre deux éclairs, de combien les crêtes ont-elles avancé pour que l'image soit la même ? Et que donne la plus grande N_e ?",
               "شوف: بين ضوء وضوء، شحال خاص les crêtes يمشيو باش نشوفو نفس l'image؟ ومن بعد، شنو كتعطي أكبر N e؟"),
          aide("Immobilité : N = k·N_e avec k entier. La plus grande N_e correspond à k = 1.",
               "l'immobilité: N égale k fois N e، وk عدد صحيح. أكبر N e هي ملي k égale un.")],
    "2": [aide("Compte les intervalles entre les crêtes couvertes par la cote d, pas les traits.",
               "حسب les intervalles اللي بين les crêtes تحت la cote d، ماشي les traits."),
          aide("Si d couvre n intervalles : d = n·λ, donc λ = d/n.",
               "يلا d فيها n intervalles: d égale n fois lambda، إذن lambda égale d sur n.")],
    "3": [aide("Tu connais λ (question 2) et N (question 1). Quelle relation les relie à v ? Attention à l'unité de λ.",
               "عندك lambda وعندك N. شنو la relation اللي كتجمعهم مع v؟ ورد البال للوحدة ديال lambda."),
          aide("v = λ·N, avec λ en mètre : 1 cm = 10⁻² m.",
               "v égale lambda fois N، وlambda بالمتر: un centimètre égale dix puissance moins deux mètre.")],
    "4": [aide("Combien de λ entre S et M ? Calcule SM/λ en partant de la source S.",
               "شحال من lambda بين S وM؟ حسب SM sur lambda، وبدا من S."),
          aide("τ = SM/v ; et λ/v = T. SM en mètre, v en m/s.",
               "tau égale SM sur v. وlambda sur v égale T. SM بالمتر، وv بالمتر par seconde.")],
    "5": [aide("Calcule la distance MP, puis MP/λ dans la même unité.",
               "حسب la distance MP، ومن بعد MP sur lambda بنفس الوحدة."),
          aide("Un entier : en phase. Un entier et demi : en opposition de phase. Autre chose : ni l'un ni l'autre.",
               "عدد صحيح: en phase. عدد صحيح ونص: en opposition de phase. شي حاجة أخرى: لا هادي لا هادي.")],
}

questions = []
for i, f in enumerate(QS, 1):
    q = f(A)
    q["texte_dit"] = TEXTE_DIT[q["id"]]
    q["aides"] = AIDES[q["id"]]
    q["explication"] = f"ex_q{i}"
    q["facile"] = f"fa_q{i}"
    questions.append(q)

# ---------------- explication animée ----------------
lamA, NA, vA, tauA, tTA = fr(A["lam"], 2), fr(A["N"], 1), fr(A["v"], 2), fr(A["tau"], 2), fr(A["tauT"], 1)
m1 = (f"فالسيمولاسيون، le vibreur عندو la fréquence vingt hertz، وle stroboscope عندو la fréquence des éclairs vingt hertz. "
      f"بين ضوء وضوء، دازت T: كل crête مشات lambda، وخدات البلاصة ديال اللي قدامها. "
      f"إذن كنشوفو نفس l'image: الما كيبان واقف. هادي هي l'immobilité apparente. "
      f"la condition: N égale k fois N e، وk عدد صحيح. وأكبر N e هي ملي k égale un، يعني N e égale N. "
      f"فالتمرين، أكبر N e égale {mots(NA)} hertz. إذن N égale {mots(NA)} hertz.")
ex1 = diapo_sim("ex_q1", "Question 1 : l'immobilité apparente donne N",
                "Un éclair par période : l'image est la même. N = k·N_e ; la plus grande N_e donne N.",
                SIMS + "stroboscope.html?vue=immobile", "Éclairs à la fréquence du vibreur : la surface paraît immobile", m1,
                [("N = k · N_e (k entier)", "la condition: N égale k fois N e"), (f"N = N_e max = {NA} Hz", f"إذن N égale {mots(NA)} hertz")],
                [dict(mot="وle stroboscope عندو", repere="frequence_eclairs"),
                 dict(mot="بين ضوء وضوء، دازت T", commande="play_until", parametres={"moment": "eclair_2"}),
                 dict(mot="إذن كنشوفو نفس l'image", commande="play_until", parametres={"moment": "immobilite"}),
                 dict(mot="la condition: N égale k fois N e", cible="centre:0"),
                 dict(mot=f"إذن N égale {mots(NA)} hertz", cible="centre:1")])

m2 = (f"فالسيمولاسيون، l'image واقفة، ودرنا المسطرة فوق les crêtes. المسطرة كتعطي d égale quatre virgule cinq centimètres. "
      f"les crêtes: quatre، ولكن d n'est pas quatre lambda! نحسبو les intervalles: un, deux, trois. إذن d égale trois lambda، وlambda égale d sur n. "
      f"فالتمرين، la cote d كتغطي les crêtes من la première حتى la sixième، إذن n égale {mots(A['n'])} intervalles. "
      f"lambda égale {mots(fr(A['d'], 1))} sur {mots(A['n'])}، égale {mots(lamA)} centimètre.")
ex2 = diapo_sim("ex_q2", "Question 2 : λ sur la photo, en comptant les intervalles",
                "d couvre n intervalles : λ = d/n.", SIMS + "cuve.html?vue=compter", "La règle posée sur les rides", m2,
                [("d = n · λ → λ = d/n", "إذن d égale trois lambda"), (f"λ = {fr(A['d'], 1)}/{A['n']} = {lamA} cm", f"égale {mots(lamA)} centimètre")],
                [dict(mot="ودرنا المسطرة فوق", commande="play_until", parametres={"moment": "regle_posee"}),
                 dict(mot="المسطرة كتعطي d", repere="regle"),
                 dict(mot="نحسبو les intervalles", repere="intervalle"),
                 dict(mot="إذن d égale trois lambda", cible="centre:0"),
                 dict(mot=f"égale {mots(lamA)} centimètre", cible="centre:1")])

m3 = (f"فالسيمولاسيون، le vibreur à vingt hertz، وlambda égale un virgule cinq centimètre. "
      f"la relation: v égale lambda fois N، وlambda بالمتر. v égale un virgule cinq fois dix puissance moins deux، fois vingt، "
      f"égale zéro virgule trente mètre par seconde. فالتمرين، lambda égale {mots(lamA)} centimètre، وN égale {mots(NA)} hertz. "
      f"v égale {mots(lamA)} fois dix puissance moins deux، fois {mots(NA)}. v égale {mots(vA)} mètre par seconde. "
      f"قيمة معقولة: فوق الما، la célérité ديما شي dixièmes ديال mètre par seconde.")
ex3 = diapo_sim("ex_q3", "Question 3 : la célérité v = λ·N",
                "λ en mètre, N en hertz : v en m/s.", SIMS + "cuve.html?vue=frequence", "λ mesurée, puis v = λ·N", m3,
                [("v = λ · N (λ en m)", "la relation: v égale lambda fois N"), (f"v = {lamA} × 10⁻² × {NA} = {vA} m/s", f"v égale {mots(vA)} mètre par seconde")],
                [dict(mot="le vibreur à vingt hertz", repere="vibreur"),
                 dict(mot="وlambda égale un virgule cinq", commande="play_until", parametres={"moment": "regle_posee"}),
                 dict(mot="la relation: v égale lambda fois N", cible="centre:0"),
                 dict(mot=f"v égale {mots(vA)} mètre par seconde", cible="centre:1"),
                 dict(mot="قيمة معقولة", repere="tableau_mesures")])

m4 = (f"هنا la corde، ماشي الما، ولكن نفس la règle. فالسيمولاسيون، SM égale zéro virgule soixante-quinze mètre، "
      f"v égale un mètre par seconde، وT égale zéro virgule cinq seconde. S كتتحرك الأولى. من بعد كتوصل l'onde ل M. "
      f"هاد le décalage هو le retard tau. tau égale SM sur v، égale zéro virgule soixante-quinze seconde، "
      f"وSM égale un virgule cinq lambda، إذن tau égale un virgule cinq T. "
      f"فالتمرين، SM sur lambda égale {mots(fr(A['SM'], 1))} sur {mots(lamA)}، égale {mots(tTA)}. إذن tau égale {mots(tTA)} T. "
      f"tau égale SM sur v، égale {mots(tauA)} seconde.")
ex4 = diapo_sim("ex_q4", "Question 4 : le retard τ du point M",
                "SM = n·λ donne τ = n·T ; τ = SM/v.", SIMS + "corde.html?vue=retard", "M refait le mouvement de S avec un retard τ", m4,
                [("τ = SM/v ; λ/v = T", "tau égale SM sur v، égale zéro"), (f"SM = {tTA} λ → τ = {tTA} T = {tauA} s", f"إذن tau égale {mots(tTA)} T")],
                [dict(mot="S كتتحرك الأولى", commande="start"),
                 dict(mot="كتوصل l'onde ل M", commande="play_until", parametres={"moment": "front_atteint_m"}),
                 dict(mot="هاد le décalage هو le retard tau", repere="retard_tau"),
                 dict(mot="tau égale SM sur v، égale zéro", cible="centre:0"),
                 dict(mot=f"إذن tau égale {mots(tTA)} T", cible="centre:1")])

m5 = (f"الرسم بوحدو ماشي جواب: خاصنا نحسبو d sur lambda. فالسيمولاسيون، lambda égale quatre centimètres، وd égale dix centimètres. "
      f"d sur lambda égale dix sur quatre، égale deux virgule cinq: عدد صحيح ونص. إذن les deux points vibrent en opposition de phase. "
      f"فالتمرين، MP égale {mots(fr(A['MP'], 1))} centimètres، وlambda égale {mots(lamA)} centimètre. "
      f"MP sur lambda égale {mots(fr(A['q'], 1))}، نفس الحالة. إذن M وP vibrent en opposition de phase.")
ex5 = diapo_sim("ex_q5", "Question 5 : M et P, en phase ou en opposition ?",
                "Un entier : en phase. Un entier et demi : en opposition.", SIMS + "methode-phase.html", "On compte les λ entre les deux points", m5,
                [("d/λ = 2,5 = 2 + 1/2 → opposition de phase", "d sur lambda égale dix sur quatre"),
                 (f"MP/λ = {fr(A['MP'], 1)}/{lamA} = {fr(A['q'], 1)} → opposition", "إذن M وP vibrent en opposition de phase")],
                [dict(mot="lambda égale quatre centimètres", commande="play_until", parametres={"moment": "lambda"}),
                 dict(mot="وd égale dix centimètres", commande="play_until", parametres={"moment": "distance"}),
                 dict(mot="d sur lambda égale dix sur quatre", commande="play_until", parametres={"moment": "calcul"}),
                 dict(mot="d sur lambda égale dix sur quatre", cible="centre:0"),
                 dict(mot="إذن les deux points vibrent", commande="play_until", parametres={"moment": "verdict"}),
                 dict(mot="إذن M وP vibrent en opposition de phase", cible="centre:1")])

# ---------------- version facile ----------------
fa1 = qcm_facile("fa_q1", "Plus facile : la fréquence du vibreur", "سؤال ساهل على le stroboscope. اختار الجواب الصحيح.",
    f"L'immobilité apparente est obtenue pour N_e = {NA} Hz (la plus grande) et pour N_e = {fr(A['Ne2'], 1)} Hz. La fréquence du vibreur est…",
    [f"N = {fr(A['Ne2'], 1)} Hz", f"N = {NA} Hz", f"N = {fr(2 * A['N'], 1)} Hz"], 1, {
        "1": {"juste": rep(f"برافو! N égale k fois N e، وأكبر N e كتعطي k égale un. إذن N égale {mots(NA)} hertz.",
                           f"Juste : N = k·N_e et la plus grande N_e correspond à k = 1 : N = {NA} Hz.")},
        "0": {"1": rep("ما تقلقش. بهاد la fréquence، k égale deux: بين ضوء وضوء دازت la durée deux T. واش هادي هي أكبر N e؟ عاود اختار.",
                       f"À {fr(A['Ne2'], 1)} Hz, il passe 2T entre deux éclairs (k = 2). Cherche k = 1. Réessaie."),
              "2": rep(f"الجواب: N égale {mots(NA)} hertz. أكبر N e هي اللي كتساوي N، يعني k égale un.",
                       f"Réponse : N = {NA} Hz (k = 1, la plus grande N_e).")},
        "2": {"1": rep("قريب، ولكن N égale k fois N e، وk عدد صحيح. أكبر N e هي ملي k égale un، ماشي k égale deux. عاود اختار.",
                       "Avec la plus grande N_e, k = 1 : on ne multiplie pas par 2. Réessaie."),
              "2": rep(f"الجواب: N égale {mots(NA)} hertz. ضربتي أكبر N e fois deux، ولكن k égale un.",
                       f"Réponse : N = {NA} Hz ; la plus grande N_e correspond à k = 1.")}},
    f"L'immobilité apparente est obtenue pour N e égale {mots(NA)} hertz, la plus grande. La fréquence du vibreur est ?")

fa2 = qcm_facile("fa_q2", "Plus facile : compter les intervalles", "سؤال ساهل: شحال من lambda فla cote؟",
    f"La cote d = {fr(A['d'], 1)} cm va de la première à la sixième crête. Combien de λ couvre-t-elle ?",
    ["6 λ", "5 λ", "7 λ"], 1, {
        "1": {"juste": rep(f"برافو! six crêtes، ومن crête ل crête: cinq intervalles. إذن d égale cinq lambda، وlambda égale {mots(lamA)} centimètre.",
                           f"Juste : 6 crêtes, 5 intervalles : d = 5λ, λ = {lamA} cm.")},
        "0": {"1": rep("ما تقلقش. حسبتي les traits، ماشي les intervalles. بحال الأصابع: خمسة ديال الأصابع، وبيناتهم ربعة ديال الفراغات. عاود اختار.",
                       "Tu as compté les crêtes ; λ est l'intervalle entre deux crêtes. Réessaie."),
              "2": rep("الجواب: d égale cinq lambda. six crêtes، cinq intervalles.", "Réponse : 5 λ (6 crêtes → 5 intervalles).")},
        "2": {"1": rep("لا، خاص نحسبو غير les intervalles اللي داخل la cote. عاود اختار.", "Compte seulement les intervalles dans la cote. Réessaie."),
              "2": rep("الجواب: d égale cinq lambda. six crêtes، cinq intervalles.", "Réponse : 5 λ.")}},
    "La cote d va de la première à la sixième crête. Combien de lambda couvre-t-elle ?")

fa3 = vf_facile("fa_q3", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    f"λ = {lamA} cm et N = {NA} Hz.", [
        (f"v = λ·N = {lamA} × 10⁻² × {NA} = {vA} m/s", True, f"λ en mètre : {lamA} cm = {lamA} × 10⁻² m, donc v = {vA} m/s."),
        (f"v = λ·N = {lamA} × {NA} = {fr(A['lam'] * A['N'], 1)} m/s", False, "λ est restée en cm : il faut la convertir en mètre avant de multiplier."),
        (f"v = λ/N = {lamA} × 10⁻²/{NA}", False, "La relation est v = λ·N (ou v = λ/T), pas λ/N.")])

fa4 = qcm_facile("fa_q4", "Plus facile : le retard", "سؤال ساهل على le retard.",
    f"SM = {tTA} λ et T = {fr(A['T'], 2)} s. Le retard de M par rapport à S vaut…",
    [f"τ = {tTA} T = {tauA} s", f"τ = T/{tTA}", f"τ = {tTA} λ"], 0, {
        "0": {"juste": rep(f"برافو! كل lambda كتاخد T. إذن tau égale {mots(tTA)} T، égale {mots(tauA)} seconde.",
                           f"Juste : chaque λ est parcourue en T : τ = {tTA} T = {tauA} s.")},
        "1": {"1": rep("ما تقلقش. M بعيدة على S، إذن l'onde كتاخد وقت كبير من T، ماشي صغير. عاود اختار.",
                       "M est à plusieurs λ de S : le retard est plus grand que T. Réessaie."),
              "2": rep(f"الجواب هو tau égale {mots(tTA)} T. كل lambda كتاخد T.", f"Réponse : τ = {tTA} T = {tauA} s.")},
        "2": {"1": rep("لا، le retard هو وقت، بالسيكوند، ماشي مسافة. عاود اختار.", "Un retard est une durée (s), pas une longueur. Réessaie."),
              "2": rep(f"الجواب هو tau égale {mots(tTA)} T. lambda مسافة، وT هو الوقت.", f"Réponse : τ = {tTA} T = {tauA} s (une durée).")}},
    f"SM égale {mots(tTA)} lambda. Le retard de M par rapport à S vaut ?")

fa5 = assoc_facile("fa_q5", "Plus facile : d/λ et état vibratoire", "سؤال ساهل: ربط كل قيمة ديال d sur lambda مع l'état vibratoire.",
    "Relie chaque valeur de d/λ à l'état vibratoire des deux points.", "Relie chaque d/λ à sa conclusion.",
    [("1", "d/λ = 3"), ("2", "d/λ = 2,5"), ("3", "d/λ = 2,3")],
    [("a", "en phase"), ("b", "en opposition de phase"), ("c", "ni en phase ni en opposition")],
    {"1": "a", "2": "b", "3": "c"}, {
        "1-a": (True, "Oui : 3 est un entier, d = 3λ : en phase.", "برافو: trois عدد صحيح، إذن en phase."),
        "1-b": (False, "3 est un entier, pas un entier et demi.", "لا، trois عدد صحيح، ماشي عدد صحيح ونص."),
        "1-c": (False, "3 est un entier : c'est un cas connu.", "لا، trois عدد صحيح: هادي حالة معروفة."),
        "2-a": (False, "2,5 n'est pas un entier.", "لا، deux virgule cinq ماشي عدد صحيح."),
        "2-b": (True, "Oui : 2,5 = 2 + 1/2, un entier et demi : opposition de phase.", "برافو: deux virgule cinq، عدد صحيح ونص: en opposition de phase."),
        "2-c": (False, "2,5 est un entier et demi : c'est l'opposition de phase.", "لا، deux virgule cinq عدد صحيح ونص: en opposition."),
        "3-a": (False, "2,3 n'est pas un entier.", "لا، deux virgule trois ماشي عدد صحيح."),
        "3-b": (False, "Une virgule ne suffit pas : seul un entier et demi donne l'opposition.", "لا، ماشي أي virgule: غير عدد صحيح ونص كيعطي l'opposition."),
        "3-c": (True, "Oui : 2,3 n'est ni un entier ni un entier et demi.", "برافو: deux virgule trois، لا عدد صحيح لا عدد صحيح ونص.")},
    ("(1 ; a) (2 ; b) (3 ; c)", "trois: en phase. deux virgule cinq: en opposition. deux virgule trois: لا هادي لا هادي."))

# ---------------- similaire ----------------
sim_qs = [f(B) for f in QS]
for q in sim_qs:
    q.pop("texte_dit", None)
sim_qs[3]["texte"] = f"Montrer que le retard du mouvement de M par rapport à celui de S vaut τ = {fr(B['tauT'], 1)} T, puis calculer τ."

EX = {
    "id": "phys_ex_ch2_cuve_4", "type": "exercice", "version": 1, "status": "published",
    "matiere": "physique", "chapitre": "ondes_mecaniques_periodiques", "cours": "phys_ch2_ondes_periodiques",
    "titre": "Une cuve à ondes sous le stroboscope", "niveau": "moyen", "duree_min": 25,
    "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
    "competences": ["Exploiter l'immobilité apparente : N = k·N_e", "Lire λ sur une photo (d = n·λ)", "Calculer v = λ·N",
                    "Calculer un retard τ = SM/v et l'exprimer en T", "Comparer l'état vibratoire de deux points"],
    "enonce": {"intro": intro(A), "intro_dit": intro_dit(A),
               "figures": [figure(A, "Photo de la surface sous le stroboscope")],
               "donnees": donnees_txt(A), "questions": questions},
    "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [ex1, ex2, ex3, ex4, ex5]}]},
    "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [fa1, fa2, fa3, fa4, fa5]}]},
    "similaire": {"id": "phys_ex_ch2_cuve_4_b", "titre": "Même exercice, autres données",
                  "enonce": {"intro": intro(B), "intro_dit": intro_dit(B),
                             "figures": [figure(B, "Photo de la surface sous le stroboscope")],
                             "donnees": donnees_txt(B), "questions": sim_qs}},
}
controler_voix(EX)
assert not PB_VOIX, "\n".join(PB_VOIX)
ecrire(EX)
