# Exercice de physique (ch. 2, ondes mécaniques progressives périodiques), niveau difficile (« Supérieur ») :
# ultrasons, un émetteur et deux récepteurs — T lue sur plusieurs périodes d'un oscillogramme, N = 1/T (ultrason ?),
# « montrer que » x₁₀ = 10λ, lecture critique de la précision (mesure sur 10 λ), v = λ·N, puis un retard « caché » :
# courbes en phase alors que τ = D/v = k·T ≠ 0.
#
# Sources comparées (skill exercices § 2) :
# - exploration ondes_mecaniques_periodiques.json : cas_types deux_recepteurs (« le déplacement entre le départ en
#   phase et le n-ième retour en phase vaut n·λ ; v = λ·N ; comparer à 340 m/s »), periode_elongation (T = divisions
#   × S_H), retard_periodique (SM = k·λ → τ = k·T) ; pieges (ms et µs confondues, « pour la première fois » = un seul λ,
#   d₂ au lieu de d₂ − d₁, T = nombre de divisions) ; valeurs_reperes (40 kHz, 25 µs, λ ≈ 8,5 mm) ;
#   erreurs_des_profs (Ridouan : exercice incohérent T = 25 µs / λ = 3,25 cm ; ici tout est calculé et cohérent).
# - vidéos des profs : Driss (devoir des deux récepteurs à ultrasons), Ridouan (montage des deux micros),
#   TOP PHYSIQUE (deux micros), mouhibi (deux micros en devoir).
# - nationaux comparés : aucun national PC 2016–2025 du dépôt sur les deux récepteurs (0 national) ; 2020 R ex. 2
#   (échographie : ultrasons, autre situation) ; 2022 R (lecture de τ et T sur y_M(t)). Ici : notre montage, mesure
#   sur plusieurs périodes et sur 10 λ, et le retard τ = 35 T non visible à l'écran : situation et chaîne originales.
# - séries en ligne : la recherche (WebSearch) a donné les titres de séries talamidi, moutamadris, alloschool,
#   Jenkal (ultrasons), Ajitfham (deux microphones) ; leur lecture (WebFetch) est bloquée par le réseau de la session
#   (ENOTFOUND).
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
def donnees(SH, p, ndiv, x1_cm, n, xn_cm, D_cm):
    D = {"SH": SH, "p": p, "ndiv": ndiv, "x1": x1_cm, "n": n, "xn": xn_cm, "D": D_cm}
    D["T"] = ndiv * SH / p                     # µs
    D["N"] = 1 / (D["T"] * 1e-6)               # Hz
    D["lam"] = xn_cm * 10 / n                  # mm
    D["v"] = D["lam"] * 1e-3 * D["N"]          # m/s
    D["tau"] = D_cm * 1e-2 / D["v"]            # s
    D["k"] = D["tau"] / (D["T"] * 1e-6)
    return D

A = donnees(10, 3, 7.5, 0.9, 10, 8.6, 30.1)
B = donnees(5, 2, 8, 0.7, 10, 6.8, 27.2)
assert abs(A["T"] - 25) < 1e-9 and abs(A["N"] - 40000) < 1e-6 and abs(A["lam"] - 8.6) < 1e-9 and abs(A["v"] - 344) < 1e-9
assert abs(A["tau"] - 8.75e-4) < 1e-12 and abs(A["k"] - 35) < 1e-9
assert abs(B["T"] - 20) < 1e-9 and abs(B["N"] - 50000) < 1e-6 and abs(B["lam"] - 6.8) < 1e-9 and abs(B["v"] - 340) < 1e-9
assert abs(B["tau"] - 8e-4) < 1e-12 and abs(B["k"] - 40) < 1e-9


def oscillo(D):
    T, SH = D["T"], D["SH"]
    tmax = 10 * SH
    return {"type": "courbe", "titre": "Figure 1 : oscillogramme, R₁ et R₂ côte à côte",
            "axes": {"x": {"min": 0, "max": tmax, "nom": "t", "unite": "µs", "graduations": [round(i * SH, 3) for i in range(11)]},
                     "y": {"min": -3, "max": 3, "nom": "u", "unite": "V", "graduations": [-2, 0, 2]}},
            "legende": f"Sensibilité horizontale : S_H = {fr(SH, 1)} µs/div (une graduation = une division). Les deux courbes sont en phase.",
            "elements": [
                {"f": "courbe", "expr": f"2.4*sin(2*pi*x/{T})", "couleur": "jaune", "texte": "R₁ (voie 1)", "texte_x": round(0.9 * T, 3), "pos": "ne"},
                {"f": "courbe", "expr": f"1.3*sin(2*pi*x/{T})", "couleur": "cyan", "texte": "R₂ (voie 2)", "texte_x": round(2.3 * T, 3), "pos": "se"},
                {"f": "cote", "de": [0, -2.7], "a": [round(D["p"] * T, 3), -2.7], "t": f"{D['p']} périodes", "couleur": "orange", "pos": "n"},
                {"f": "texte", "at": [round(0.72 * tmax, 3), 2.75], "t": f"S_H = {fr(SH, 1)} µs/div", "couleur": "blanc", "ancre": "centre"}]}


def montage():
    return {"type": "schema", "titre": "Figure 2 : le montage", "cadre": {"l": 10, "h": 3.4},
            "legende": "R₁ reste fixe ; R₂ glisse le long de la règle, dans la direction de propagation.",
            "elements": [
                {"f": "rect", "de": [0.3, 1.2], "a": [1.3, 2.4], "couleur": "jaune"},
                {"f": "texte", "at": [0.8, 2.8], "t": "E (40 kHz ?)".replace(" (40 kHz ?)", ""), "couleur": "jaune", "ancre": "centre"},
                {"f": "fleche", "de": [1.5, 1.8], "a": [3.0, 1.8], "couleur": "faible", "texte": "ultrasons", "pos": "n"},
                {"f": "point", "at": [3.6, 1.8], "t": "R₁", "pos": "n", "couleur": "orange"},
                {"f": "point", "at": [6.4, 1.8], "t": "R₂", "pos": "n", "couleur": "cyan"},
                {"f": "fleche", "de": [6.6, 1.3], "a": [8.4, 1.3], "couleur": "cyan", "texte": "on recule R₂", "pos": "s"},
                {"f": "ligne", "pts": [[3.2, 0.5], [9.6, 0.5]], "couleur": "blanc"},
                {"f": "texte", "at": [6.4, 0.1], "t": "règle graduée", "couleur": "faible", "ancre": "centre"},
                {"f": "rect", "de": [7.6, 2.4], "a": [9.6, 3.3], "couleur": "faible"},
                {"f": "texte", "at": [8.6, 2.75], "t": "oscilloscope", "couleur": "faible", "ancre": "centre"}]}


def intro(D):
    return (f"Un émetteur E d'ondes ultrasonores et deux récepteurs R₁ et R₂ sont alignés (figure 2) ; les récepteurs sont "
            f"reliés aux deux voies d'un oscilloscope. Au départ, R₁ et R₂ sont côte à côte : on obtient l'oscillogramme de la "
            f"figure 1 (S_H = {fr(D['SH'], 1)} µs/div). On recule ensuite lentement R₂ en laissant R₁ fixe : les deux courbes "
            f"sont de nouveau en phase pour la première fois quand R₂ a reculé de x₁ = {fr(D['x1'], 1)} cm, et pour la "
            f"{D['n']}e fois quand R₂ a reculé de x₁₀ = {fr(D['xn'], 1)} cm depuis sa position de départ. La règle se lit à 1 mm près.")


def intro_dit(D):
    return (f"دابا نقراو l'énoncé. عندنا un émetteur E ديال les ultrasons، et deux récepteurs، R un وR deux، "
            f"مربوطين مع les deux voies ديال l'oscilloscope. فاللول، R un وR deux حدا بعضياتهم: كنلقاو l'oscillogramme ديال la figure un، "
            f"la sensibilité horizontale égale {mots(fr(D['SH'], 1))} micro seconde par division. "
            f"من بعد، كنبعدو R deux بشوية، وR un ثابت. les courbes كيرجعو en phase la première fois ملي R deux تبعد ب x un "
            f"égale {mots(fr(D['x1'], 1))} centimètre، وla dixième fois ملي تبعد ب x dix égale {mots(fr(D['xn'], 1))} centimètres. "
            f"والمسطرة كتقرا ب millimètre.").replace("ملي R deux تبعد ب x un égale", "ملي R deux تبعد، x un égale").replace("ملي تبعد ب x dix égale", "ملي تبعد، x dix égale")


def donnees_txt(D):
    return [f"Figure 1 : S_H = {fr(D['SH'], 1)} µs/div", f"Premier retour en phase : x₁ = {fr(D['x1'], 1)} cm ; {D['n']}e retour en phase : x₁₀ = {fr(D['xn'], 1)} cm",
            "Lecture de la règle : à 1 mm près", f"Question 6 : D = {fr(D['D'], 1)} cm",
            "Son dans l'air : environ 340 m/s ; son audible jusqu'à 20 kHz"]


def q1(D):
    p, nd, SH, T = D["p"], fr(D["ndiv"], 1), fr(D["SH"], 1), fr(D["T"], 1)
    return {"id": "1", "texte": "Déterminer la période T des ultrasons, en mesurant sur l'oscillogramme la durée de plusieurs périodes.",
            "reponse": valeur("T", D["T"], "µs", f"{p}T = {nd} div × {SH} µs/div = {fr(D['ndiv'] * D['SH'], 1)} µs ; T = {fr(D['ndiv'] * D['SH'], 1)}/{p} = {T} µs"),
            "clavier": {"aides": ["n div × S_H", f"{p}T", "µs"], "pieges": [f"T = {nd} div", "ms"]},
            "correction": correction([
                (f"1 : {p} périodes occupent {nd} divisions", f"{mots(p)} périodes"),
                (f"{p}T = {nd} × {SH} = {fr(D['ndiv'] * D['SH'], 1)} µs", f"{mots(p)} T égale {mots(nd)} fois {mots(SH)}"),
                (f"T = {T} µs = {T} × 10⁻⁶ s", f"T égale {mots(T)} micro seconde")],
                f"Question un. على الشاشة، {mots(p)} périodes occupent {mots(nd)} divisions. "
                f"{mots(p)} T égale {mots(nd)} fois {mots(SH)} micro seconde، égale {mots(fr(D['ndiv'] * D['SH'], 1))} micro seconde. "
                f"إذن T égale {mots(T)} micro seconde. علاش plusieurs périodes؟ حيت الخطأ ديال القراءة كيتقسم على عدد les périodes.")}


def q2(D):
    T, N = fr(D["T"], 1), D["N"]
    Nk = fr(N / 1000, 1)
    return {"id": "2", "texte": "En déduire la fréquence N, puis justifier qu'il s'agit d'ultrasons.",
            "reponse": valeur("N", N, "Hz", f"N = 1/T = 1/({T} × 10⁻⁶) = {sci(N, 2)} Hz"),
            "clavier": {"aides": ["N = 1/T", "10⁻⁶", "Hz", "20 kHz"], "pieges": ["N = T", "10⁻³"]},
            "correction": correction([
                ("2 : N = 1/T, avec T en seconde", "N égale un sur T"),
                (f"N = 1/({T} × 10⁻⁶) = {sci(N, 2)} Hz = {Nk} kHz", f"N égale {mots(Nk)} kilohertz"),
                (f"N = {Nk} kHz > 20 kHz : ce sont des ultrasons (inaudibles)", "vingt kilohertz")],
                f"Question deux. N égale un sur T، وT بالسيكوند: {mots(T)} fois dix puissance moins six. "
                f"N égale {mots(Nk)} kilohertz. وحنا كنسمعو le son حتى l'oreille كتوصل ل vingt kilohertz. au-dessus de vingt kilohertz، هادو ultrasons."
                .replace("حتى l'oreille كتوصل ل vingt kilohertz", "jusqu'à vingt kilohertz"))}


def q3(D):
    n, xn, lam = D["n"], fr(D["xn"], 1), fr(D["lam"], 1)
    return {"id": "3", "texte": f"Montrer que x₁₀ = {n}λ, puis calculer la longueur d'onde λ.",
            "reponse": valeur("λ", D["lam"], "mm", f"x₁₀ = {n}λ donc λ = x₁₀/{n} = {fr(D['xn'] * 10, 0)}/{n} = {lam} mm"),
            "clavier": {"aides": ["x_n = n·λ", "λ = x₁₀/10", "mm"], "pieges": ["λ = x₁₀/11", "λ = x₁₀"]},
            "correction": correction([
                ("3 : à chaque retour en phase, R₂ a reculé d'une longueur d'onde de plus", "كل مرة كيرجعو en phase"),
                (f"{n}e retour en phase : x₁₀ = {n}λ", f"x dix égale {mots(n)} lambda"),
                (f"λ = x₁₀/{n} = {fr(D['xn'] * 10, 0)}/{n} = {lam} mm", f"lambda égale {mots(lam)} millimètres")],
                f"Question trois. R un وR deux كانو en phase فاللول. كل مرة كيرجعو en phase، R deux كيكون زاد lambda. "
                f"المرة la dixième، R deux تبعد ب {mots(n)} lambda. إذن x dix égale {mots(n)} lambda. "
                f"lambda égale x dix sur {mots(n)}، égale {mots(fr(D['xn'] * 10, 0))} millimètres sur {mots(n)}. "
                f"lambda égale {mots(lam)} millimètres.".replace(f"تبعد ب {mots(n)} lambda", f"تبعد de {mots(n)} lambda"))}


def q4(D):
    x1, lam, n = fr(D["x1"] * 10, 0), fr(D["lam"], 1), D["n"]
    return {"id": "4", "texte": f"Un élève prend λ = x₁ = {x1} mm. Sachant que la règle se lit à 1 mm près, expliquer pourquoi la mesure sur {n} longueurs d'onde est plus précise.",
            "reponse": phrase(f"Une erreur de lecture de 1 mm sur x₁ = {x1} mm donne une erreur de 1 mm sur λ (environ un dixième de λ) ; sur x₁₀ = {n}λ, la même erreur de 1 mm est partagée par {n} : 0,1 mm sur λ. La mesure sur {n} λ est donc environ {n} fois plus précise : λ = {lam} mm."),
            "clavier": {"aides": ["1 mm", f"x₁₀/{n}", "erreur partagée"], "pieges": ["x₁ est plus précis", "la règle est fausse"]},
            "correction": correction([
                (f"4 : lecture à 1 mm près : sur x₁ = {x1} mm, l'erreur sur λ est de 1 mm (≈ 1/{x1} de λ)", "واحد millimètre"),
                (f"sur x₁₀ = {n}λ, l'erreur de 1 mm est divisée par {n} : 0,1 mm sur λ", f"كيتقسم على {mots(n)}".replace(f"على {mots(n)}", f"sur {mots(n)}")),
                (f"mesure sur {n}λ ≈ {n} fois plus précise : λ = {lam} mm", "plus précise")],
                f"Question quatre. المسطرة كتقرا غير ب millimètre. يلا قسنا غير x un، الخطأ ديال واحد millimètre كيطيح كامل على lambda. "
                f"ولكن يلا قسنا x dix، الخطأ هو هو، وكيتقسم sur {mots(n)}: égale zéro virgule un millimètre على lambda. "
                f"إذن la mesure sur {mots(n)} lambda، plus précise.")}


def q5(D):
    lam, N, v = fr(D["lam"], 1), sci(D["N"], 2), fr(D["v"], 0)
    return {"id": "5", "texte": "Calculer la célérité v des ultrasons dans l'air. Commenter la valeur obtenue.",
            "reponse": valeur("v", D["v"], "m/s", f"v = λ·N = {lam} × 10⁻³ × {N} = {v} m/s"),
            "clavier": {"aides": ["v = λ·N", "10⁻³", "m/s", "340 m/s"], "pieges": ["v = λ/N", "10⁻²"]},
            "correction": correction([
                ("5 : v = λ·N, avec λ en mètre", "v égale lambda fois N"),
                (f"v = {lam} × 10⁻³ × {N}", f"{mots(lam)} fois dix puissance moins trois"),
                (f"v = {v} m/s : proche de 340 m/s, la célérité du son dans l'air", f"v égale {mots(v)} mètres par seconde")],
                f"Question cinq. v égale lambda fois N، وlambda بالمتر: {mots(lam)} fois dix puissance moins trois. "
                f"v égale {mots(lam)} fois dix puissance moins trois، fois {mots(fr(D['N'] / 1e4, 0))} fois dix puissance quatre. "
                f"v égale {mots(v)} mètres par seconde. قريبة من trois cent quarante: les ultrasons كيمشيو فالهوا بحال le son."
                .replace("قريبة من trois cent quarante", "قريبة de trois cent quarante"))}


def q6(D):
    Dm, v, tau, k, Dc, lam = fr(D["D"] / 100, 3), fr(D["v"], 0), sci(D["tau"], 3), fr(D["k"], 0), fr(D["D"] * 10, 0), fr(D["lam"], 1)
    return {"id": "6",
            "texte": (f"On place maintenant R₂ à la distance D = {fr(D['D'], 1)} cm de R₁, plus loin de l'émetteur. À l'écran, les deux courbes "
                      f"sont en phase, et un élève conclut que le retard τ de R₂ sur R₁ est nul. Montrer que τ = {k} T, puis calculer τ."),
            "reponse": valeur("τ", D["tau"], "s", f"τ = D/v = {Dm}/{v} = {tau} s"),
            "clavier": {"aides": ["τ = D/v", "D/λ", "τ = k·T", "s"], "pieges": ["τ = 0", "τ = v/D"]},
            "correction": correction([
                (f"6 : D/λ = {Dc}/{lam} = {k} : D = {k}λ", f"إذن D égale {mots(k)} lambda"),
                (f"τ = D/v = {k}λ/v = {k} T : R₂ refait le mouvement de R₁ avec {k} périodes de retard, d'où des courbes en phase", f"tau égale {mots(k)} T"),
                (f"τ = D/v = {Dm}/{v} = {tau} s ≠ 0", "tau ماشي zéro".replace("ماشي zéro", "différent de zéro"))],
                f"Question six. D sur lambda égale {mots(Dc)} sur {mots(lam)}، égale {mots(k)}. إذن D égale {mots(k)} lambda. "
                f"tau égale D sur v، égale {mots(k)} lambda sur v، وlambda sur v هي T: tau égale {mots(k)} T. "
                f"R deux كتعاود اللي دارت R un قبل {mots(k)} périodes، داكشي علاش les courbes en phase. "
                f"l'oscilloscope ما كيبينش les périodes الكاملين. l'application numérique: tau égale D sur v، égale {mots(Dm)} sur {mots(v)}، "
                f"égale {dit_sci(tau)} seconde. tau différent de zéro.".replace(f"قبل {mots(k)} périodes", f"avec {mots(k)} périodes de retard"))}


def dit_sci(s):
    """« 8,75 × 10⁻⁴ » -> « huit virgule soixante-quinze fois dix puissance moins quatre »."""
    m, e = s.split(" × 10")
    e = e.translate(str.maketrans("⁻⁰¹²³⁴⁵⁶⁷⁸⁹", "-0123456789"))
    return mots(m) + " fois dix puissance " + ("moins " if e.startswith("-") else "") + mots(e.lstrip("-"))


QS = [q1, q2, q3, q4, q5, q6]

TEXTE_DIT = {
    "1": "Question un: حدد la période T ديال les ultrasons، وقيس على l'oscillogramme la durée ديال plusieurs périodes.",
    "2": "Question deux: استنتج la fréquence N، ومن بعد علل بلي هادو ultrasons.",
    "3": f"Question trois: بين بلي x dix égale {mots(A['n'])} lambda، ومن بعد حسب la longueur d'onde lambda.",
    "4": f"Question quatre: واحد التلميذ خدا lambda égale x un، égale {mots(fr(A['x1'] * 10, 0))} millimètres. المسطرة كتقرا ب millimètre. فسر علاش la mesure sur {mots(A['n'])} longueurs d'onde، plus précise.",
    "5": "Question cinq: حسب la célérité v ديال les ultrasons فالهوا، وعلق على النتيجة.",
    "6": f"Question six: دابا R deux بعيد على R un، D égale {mots(fr(A['D'], 1))} centimètres. فالشاشة les courbes en phase، والتلميذ قال le retard tau égale zéro. بين بلي tau égale {mots(fr(A['k'], 0))} T، ومن بعد حسب tau.",
}
AIDES = {
    "1": [aide("Repère sur l'axe des temps la cote « périodes » : combien de divisions, et combien de périodes ?", "شوف la cote فوق l'axe ديال الوقت: شحال من division، وشحال من période؟"),
          aide("Durée = nombre de divisions × S_H ; puis divise par le nombre de périodes.", "la durée égale le nombre de divisions fois la sensibilité. ومن بعد قسم على le nombre de périodes.")],
    "2": [aide("Convertis T en seconde : micro, c'est 10⁻⁶.", "حول T ل seconde: micro، c'est dix puissance moins six."),
          aide("N = 1/T ; l'oreille entend jusqu'à 20 kHz.", "N égale un sur T. والودن كتسمع jusqu'à vingt kilohertz.")],
    "3": [aide("Au départ, les courbes sont en phase. De combien R₂ a-t-il reculé à chaque nouveau retour en phase ?", "فاللول les courbes en phase. شحال كيزيد R deux ملي كيرجعو en phase مرة أخرى؟"),
          aide("Au n-ième retour en phase, le recul vaut n·λ : λ = x₁₀/10.", "فالمرة n، R deux تبعد de n lambda: lambda égale x dix sur dix.")],
    "4": [aide("Quelle erreur fais-tu sur une lecture de la règle ? Sur quelle longueur la répartis-tu ?", "شحال الخطأ ديال القراءة ديال المسطرة؟ وعلى شحال ديال lambda كيتقسم؟"),
          aide("Sur x₁ l'erreur de 1 mm tombe sur un seul λ ; sur x₁₀ elle se partage entre 10 λ.", "فx un، واحد millimètre كيطيح على lambda وحدة. فx dix، كيتقسم sur dix lambda.")],
    "5": [aide("Tu as λ (question 3) et N (question 2) ; attention, λ est en mm.", "عندك lambda وN. ورد البال: lambda بالمليمتر."),
          aide("v = λ·N avec λ en mètre ; compare à 340 m/s.", "v égale lambda fois N، وlambda بالمتر. قارن avec trois cent quarante mètres par seconde.")],
    "6": [aide("Calcule D/λ (même unité) : que vaut ce nombre ?", "حسب D sur lambda بنفس الوحدة: شحال كيعطي؟"),
          aide("τ = D/v et λ/v = T : si D = k·λ, alors τ = k·T et les courbes sont en phase, sans que τ soit nul.", "tau égale D sur v، وlambda sur v égale T. يلا D égale k lambda، tau égale k T، وles courbes en phase، ولكن tau différent de zéro.")],
}

questions = []
for i, f in enumerate(QS, 1):
    q = f(A)
    q["texte_dit"] = TEXTE_DIT[q["id"]]
    q["aides"] = AIDES[q["id"]]
    q["explication"] = f"ex_q{i}"
    q["facile"] = f"fa_q{i}"
    questions.append(q)

TA, NkA, lamA, vA, kA, tauA = fr(A["T"], 1), fr(A["N"] / 1000, 1), fr(A["lam"], 1), fr(A["v"], 0), fr(A["k"], 0), sci(A["tau"], 3)

# ---------------- explication animée ----------------
R = SIMS + "recepteurs.html"
m1 = (f"على الشاشة، فالسيمولاسيون، la sensibilité horizontale égale cinq micro secondes par division، et une période occupe cinq divisions. "
      f"T égale cinq fois cinq، égale vingt-cinq micro secondes. فالتمرين، la sensibilité égale {mots(fr(A['SH'], 1))} micro secondes par division، "
      f"et {mots(A['p'])} périodes occupent {mots(fr(A['ndiv'], 1))} divisions. {mots(A['p'])} T égale {mots(fr(A['ndiv'] * A['SH'], 1))} micro secondes، "
      f"إذن T égale {mots(TA)} micro secondes. كنقيسو plusieurs périodes باش تكون القراءة أدق.")
ex1 = diapo_sim("ex_q1", "Question 1 : lire T sur plusieurs périodes", "Durée = divisions × S_H ; T = durée / nombre de périodes.",
                R + "?vue=ecran", "L'écran de l'oscilloscope et sa sensibilité", m1,
                [("T = n div × S_H", "T égale cinq fois cinq"), (f"{A['p']}T = {fr(A['ndiv'], 1)} × {fr(A['SH'], 1)} µs → T = {TA} µs", f"إذن T égale {mots(TA)} micro secondes")],
                [dict(mot="على الشاشة، فالسيمولاسيون", repere="ecran"),
                 dict(mot="la sensibilité horizontale égale cinq", repere="sensibilite"),
                 dict(mot="et une période occupe", commande="play_until", parametres={"moment": "mesure"}),
                 dict(mot="et une période occupe", repere="periode"),
                 dict(mot="T égale cinq fois cinq", cible="centre:0"),
                 dict(mot=f"إذن T égale {mots(TA)} micro secondes", cible="centre:1")])

m2 = (f"فالسيمولاسيون: T égale vingt-cinq micro secondes، يعني vingt-cinq fois dix puissance moins six seconde. "
      f"N égale un sur T، égale quarante mille hertz، c'est-à-dire quarante kilohertz. قرا la sensibilité مزيان: micro، ماشي milli. "
      f"وحنا كنسمعو jusqu'à vingt kilohertz. au-dessus de vingt kilohertz: ultrason. فالتمرين، N égale {mots(NkA)} kilohertz: ultrasons.")
m2 = m2.replace("يعني vingt-cinq fois", "égale vingt-cinq fois")
ex2 = diapo_sim("ex_q2", "Question 2 : N = 1/T, puis ultrason ?", "T en seconde ; au-dessus de 20 kHz : ultrason.",
                R + "?vue=ecran", "T = 25 µs → N = 40 kHz", m2,
                [("N = 1/T (T en s)", "N égale un sur T"), (f"N = {NkA} kHz > 20 kHz : ultrasons", f"فالتمرين، N égale {mots(NkA)}")],
                [dict(mot="فالسيمولاسيون: T égale", commande="play_until", parametres={"moment": "mesure"}),
                 dict(mot="N égale un sur T", cible="centre:0"),
                 dict(mot="N égale un sur T", repere="calcul"),
                 dict(mot=f"فالتمرين، N égale {mots(NkA)}", cible="centre:1")])

m3 = (f"R un وR deux فاللول en phase. كنبعدو R deux بشوية. les courbes كيتفارقو، ومن بعد كيرجعو en phase: R deux تبعد de lambda. "
      f"كنزيدو: المرة الثانية، R deux تبعد de deux lambda. فالسيمولاسيون، lambda égale huit virgule cinq millimètres. "
      f"فالمرة n، le recul égale n lambda، إذن lambda égale x n sur n. فالتمرين، la dixième fois: x dix égale {mots(fr(A['xn'], 1))} centimètres، "
      f"إذن lambda égale {mots(lamA)} millimètres.")
ex3 = diapo_sim("ex_q3", "Question 3 : chaque retour en phase, un λ de plus", "n-ième retour en phase : recul = n·λ.",
                R + "?vue=reculer", "On recule R₂ : en phase, opposition, en phase…", m3,
                [("x_n = n · λ → λ = x_n/n", "فالمرة n، le recul"), (f"λ = {fr(A['xn'] * 10, 0)}/{A['n']} = {lamA} mm", f"إذن lambda égale {mots(lamA)} millimètres")],
                [dict(mot="كنبعدو R deux", repere="recepteur_2"),
                 dict(mot="ومن بعد كيرجعو en phase", commande="play_until", parametres={"moment": "en_phase_1"}),
                 dict(mot="المرة الثانية", commande="play_until", parametres={"moment": "en_phase_2"}),
                 dict(mot="فالمرة n، le recul", cible="centre:0"),
                 dict(mot=f"إذن lambda égale {mots(lamA)} millimètres", cible="centre:1")])

m4 = (f"شوف المسطرة. فالسيمولاسيون، deux lambda égale dix-sept millimètres. المسطرة كتقرا غير ب millimètre، والخطأ ديال القراءة واحد millimètre. "
      f"يلا قسنا lambda وحدة، هاد الخطأ كيطيح كامل على lambda. يلا قسنا x dix، الخطأ هو هو، ولكن كيتقسم sur dix. "
      f"فالتمرين، x un égale {mots(fr(A['x1'] * 10, 0))} millimètres، فيها خطأ ديال تقريبا عشرة فالمية. x dix sur dix كتعطي lambda égale {mots(lamA)} millimètres، أدق بزاف.")
m4 = m4.replace("خطأ ديال تقريبا عشرة فالمية", "خطأ كبير، environ dix pour cent")
ex4 = diapo_sim("ex_q4", "Question 4 : mesurer sur plusieurs λ", "La même erreur de lecture, partagée sur plusieurs λ.",
                R + "?vue=reculer", "La règle sous R₂", m4,
                [("erreur de lecture : 1 mm", "والخطأ ديال القراءة"), (f"sur 10 λ : 0,1 mm sur λ", "ولكن كيتقسم sur dix")],
                [dict(mot="شوف المسطرة", commande="play_until", parametres={"moment": "en_phase_2"}),
                 dict(mot="شوف المسطرة", repere="regle"),
                 dict(mot="والخطأ ديال القراءة", cible="centre:0"),
                 dict(mot="ولكن كيتقسم sur dix", cible="centre:1")])

m5 = (f"فالسيمولاسيون، lambda égale huit virgule cinq millimètres، وN égale quarante mille hertz. "
      f"v égale lambda fois N، égale huit virgule cinq fois dix puissance moins trois، fois quarante mille: trois cent quarante mètres par seconde. "
      f"فالتمرين، v égale {mots(lamA)} fois dix puissance moins trois، fois {mots(fr(A['N'], 0))}، égale {mots(vA)} mètres par seconde. "
      f"قريبة de trois cent quarante: les ultrasons كيمشيو فالهوا بحال le son.")
ex5 = diapo_sim("ex_q5", "Question 5 : la célérité v = λ·N", "λ en mètre ; on compare à 340 m/s.",
                R + "?vue=reculer&depart=opposition", "Le calcul de λ puis de v", m5,
                [("v = λ · N (λ en m)", "v égale lambda fois N"), (f"v = {lamA} × 10⁻³ × {sci(A['N'], 2)} = {vA} m/s", f"égale {mots(vA)} mètres par seconde")],
                [dict(mot="فالسيمولاسيون، lambda", commande="play_until", parametres={"moment": "mesure"}),
                 dict(mot="v égale lambda fois N", cible="centre:0"),
                 dict(mot="v égale lambda fois N", repere="calcul"),
                 dict(mot=f"égale {mots(vA)} mètres par seconde", cible="centre:1")])

m6 = (f"شوف: R deux تبعد de lambda، والصوت كيوصل ليه من بعد T. ولكن les courbes فوق بعضياتهم: en phase. "
      f"والمرة الثانية، le retard égale deux T، وles courbes حتى هوما en phase. إذن الشاشة ما كتبينش les périodes الكاملين. "
      f"tau égale D sur v، وإذا D égale k lambda، tau égale k T. "
      f"فالتمرين، D sur lambda égale {mots(kA)}، إذن tau égale {mots(kA)} T، ماشي zéro. tau égale D sur v، égale {dit_sci(tauA)} seconde.")
m6 = m6.replace("وإذا D égale", "ويلا D égale").replace("ماشي zéro", "différent de zéro")
ex6 = diapo_sim("ex_q6", "Question 6 : en phase ne veut pas dire sans retard", "D = k·λ → τ = k·T : l'écran montre des courbes en phase.",
                R + "?vue=reculer", "Un λ de plus : une période de retard de plus", m6,
                [("D = k·λ → τ = D/v = k·T", "tau égale D sur v، ويلا"), (f"τ = {kA} T = {tauA} s ≠ 0", f"إذن tau égale {mots(kA)} T")],
                [dict(mot="شوف: R deux", commande="play_until", parametres={"moment": "en_phase_1"}),
                 dict(mot="ولكن les courbes فوق", repere="courbe_2"),
                 dict(mot="والمرة الثانية", commande="play_until", parametres={"moment": "en_phase_2"}),
                 dict(mot="tau égale D sur v، ويلا", cible="centre:0"),
                 dict(mot=f"إذن tau égale {mots(kA)} T", cible="centre:1")])

# ---------------- version facile ----------------
SHA, ndA, pA = fr(A["SH"], 1), fr(A["ndiv"], 1), A["p"]
fa1 = qcm_facile("fa_q1", "Plus facile : T sur plusieurs périodes", "سؤال ساهل: حسب T.",
    f"{pA} périodes occupent {ndA} divisions ; S_H = {SHA} µs/div. La période vaut…",
    [f"T = {fr(A['ndiv'] * A['SH'], 1)} µs", f"T = {ndA} µs", f"T = {TA} µs"], 2, {
        "2": {"juste": rep(f"برافو! la durée égale {mots(ndA)} fois {mots(SHA)}، وكنقسمو sur {mots(pA)}: T égale {mots(TA)} micro secondes.", f"Juste : {pA}T = {fr(A['ndiv'] * A['SH'], 1)} µs, T = {TA} µs.")},
        "0": {"1": rep("قريب! هادي la durée ديال plusieurs périodes. خاصك تقسم على عدد les périodes. عاود اختار.", "C'est la durée de plusieurs périodes : divise par leur nombre. Réessaie."),
              "2": rep(f"الجواب: T égale {mots(TA)} micro secondes. قسمنا la durée sur {mots(pA)}.", f"Réponse : T = {TA} µs.")},
        "1": {"1": rep("ما تقلقش. هادا عدد les divisions، ماشي وقت. ضرب فla sensibilité. عاود اختار.", "C'est un nombre de divisions : multiplie par S_H. Réessaie."),
              "2": rep(f"الجواب: T égale {mots(TA)} micro secondes.", f"Réponse : T = {TA} µs.")}},
    "Plusieurs périodes occupent plusieurs divisions. La période vaut ?")

fa2 = vf_facile("fa_q2", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    f"T = {TA} µs.", [
        (f"N = 1/T = 1/({TA} × 10⁻⁶) = {sci(A['N'], 2)} Hz", True, "micro = 10⁻⁶ : N = 40 000 Hz."),
        (f"N = 1/({TA} × 10⁻³) = {fr(1 / (A['T'] * 1e-3), 0)} Hz", False, "µs n'est pas ms : micro, c'est 10⁻⁶."),
        (f"Avec N = {NkA} kHz, l'onde est un ultrason.", True, "Au-dessus de 20 kHz, l'oreille n'entend plus : ultrason.")])

fa3 = qcm_facile("fa_q3", "Plus facile : le dixième retour en phase", "سؤال ساهل على le recul.",
    f"Au {A['n']}e retour en phase, R₂ a reculé de x₁₀ = {fr(A['xn'], 1)} cm. Alors…",
    [f"x₁₀ = {A['n']}λ", f"x₁₀ = {A['n'] + 1}λ", f"x₁₀ = {A['n'] - 1}λ"], 0, {
        "0": {"juste": rep(f"برافو! كل retour en phase كيزيد lambda: x dix égale dix lambda.", f"Juste : x₁₀ = 10λ, λ = {lamA} mm.")},
        "1": {"1": rep("ما تقلقش. فاللول كانو en phase ولكن R deux ما تحركش: هاداك ماشي retour. عاود اختار.", "La position de départ ne compte pas : R₂ n'a pas encore reculé. Réessaie."),
              "2": rep("الجواب: x dix égale dix lambda.", "Réponse : x₁₀ = 10λ.")},
        "2": {"1": rep("لا، la première fois، R deux تبعد de lambda. إذن la dixième fois؟ عاود اختار.", "Au premier retour, le recul vaut λ ; au dixième ? Réessaie."),
              "2": rep("الجواب: x dix égale dix lambda.", "Réponse : x₁₀ = 10λ.")}},
    "Au dixième retour en phase, combien de lambda a reculé R deux ?")

fa4 = vf_facile("fa_q4", "Plus facile : la précision", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.",
    "La règle se lit à 1 mm près.", [
        ("Mesurer x₁₀ puis diviser par 10 rend l'erreur sur λ dix fois plus petite.", True, "L'erreur de 1 mm est partagée entre 10 λ : 0,1 mm sur λ."),
        ("Mesurer x₁ donne λ plus précisément, car c'est une seule mesure.", False, "Sur x₁, l'erreur de 1 mm tombe entière sur un seul λ.")])

fa5 = qcm_facile("fa_q5", "Plus facile : la célérité", "سؤال ساهل على la célérité.",
    f"λ = {lamA} mm et N = {sci(A['N'], 2)} Hz. La célérité vaut…",
    [f"v = {fr(A['lam'] * A['N'], 0)} m/s", f"v = {vA} m/s", f"v = {fr(A['v'] * 10, 0)} m/s"], 1, {
        "1": {"juste": rep(f"برافو! lambda بالمتر: v égale {mots(vA)} mètres par seconde، قريبة de trois cent quarante.", f"Juste : v = {lamA} × 10⁻³ × {sci(A['N'], 2)} = {vA} m/s.")},
        "0": {"1": rep("ما تقلقش. خليتي lambda بالمليمتر. حولها ل mètre. عاود اختار.", "λ est restée en mm : convertis-la en mètre. Réessaie."),
              "2": rep(f"الجواب: v égale {mots(vA)} mètres par seconde. millimètre، dix puissance moins trois.", f"Réponse : v = {vA} m/s (λ en m).")},
        "2": {"1": rep("لا، حولتي ب dix puissance moins deux. milli، dix puissance moins trois. عاود اختار.".replace("ب dix puissance", "avec dix puissance"), "milli = 10⁻³, pas 10⁻². Réessaie."),
              "2": rep(f"الجواب: v égale {mots(vA)} mètres par seconde.", f"Réponse : v = {vA} m/s.")}},
    "Lambda et N sont donnés. La célérité vaut ?")

fa6 = assoc_facile("fa_q6", "Plus facile : ce que montre l'écran", "سؤال ساهل: ربط كل D sur lambda مع اللي كنشوفو فالشاشة.",
    "Relie chaque valeur de D/λ à ce que montre l'écran.", "Relie chaque D/λ à l'écran.",
    [("1", "D/λ = 35"), ("2", "D/λ = 35,5"), ("3", "D/λ = 0")],
    [("a", "courbes en phase, retard τ = 35 T"), ("b", "courbes en opposition de phase"), ("c", "courbes en phase, retard nul")],
    {"1": "a", "2": "b", "3": "c"}, {
        "1-a": (True, "Oui : D = 35λ, τ = 35T : en phase, mais le retard n'est pas nul.", "برافو: tau égale trente-cinq T، en phase، ولكن ماشي zéro.".replace("ماشي zéro", "différent de zéro")),
        "1-b": (False, "35 est un entier : en phase.", "لا، trente-cinq عدد صحيح: en phase.".replace("لا، trente-cinq", "لا: D sur lambda égale trente-cinq")),
        "1-c": (False, "En phase oui, mais D ≠ 0 : le retard vaut 35T.", "لا، D ماشي zéro: tau égale trente-cinq T.".replace("ماشي zéro", "différent de zéro")),
        "2-a": (False, "35,5 est un entier et demi.", "لا، عدد صحيح ونص."),
        "2-b": (True, "Oui : un entier et demi : opposition de phase.", "برافو: عدد صحيح ونص، en opposition de phase."),
        "2-c": (False, "35,5 n'est pas 0.", "لا، D كبيرة."),
        "3-a": (False, "D = 0 : aucun retard.", "لا، D égale zéro: ماكاينش le retard."),
        "3-b": (False, "D = 0 : les récepteurs sont côte à côte, en phase.", "لا، D égale zéro: حدا بعضياتهم، en phase."),
        "3-c": (True, "Oui : côte à côte, retard nul.", "برافو: حدا بعضياتهم، le retard égale zéro.")},
    ("(1 ; a) (2 ; b) (3 ; c)", "en phase ماكيعنيش le retard égale zéro."))

sim_qs = [f(B) for f in QS]

EX = {
    "id": "phys_ex_ch2_ultrasons_7", "type": "exercice", "version": 1, "status": "published",
    "matiere": "physique", "chapitre": "ondes_mecaniques_periodiques", "cours": "phys_ch2_ondes_periodiques",
    "titre": "Des ultrasons, deux récepteurs et un retard trompeur", "niveau": "difficile", "duree_min": 35,
    "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
    "competences": ["Lire T sur un oscillogramme (sur plusieurs périodes)", "Calculer N = 1/T et reconnaître un ultrason",
                    "Mesurer λ par les retours en phase (x_n = n·λ)", "Juger la précision d'une mesure", "Calculer v = λ·N",
                    "Relier retard et périodicité : D = k·λ ⇒ τ = k·T"],
    "enonce": {"intro": intro(A), "intro_dit": intro_dit(A), "figures": [oscillo(A), montage()],
               "donnees": donnees_txt(A), "questions": questions},
    "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [ex1, ex2, ex3, ex4, ex5, ex6]}]},
    "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [fa1, fa2, fa3, fa4, fa5, fa6]}]},
    "similaire": {"id": "phys_ex_ch2_ultrasons_7_b", "titre": "Même exercice, autres données",
                  "enonce": {"intro": intro(B), "intro_dit": intro_dit(B), "figures": [oscillo(B), montage()],
                             "donnees": donnees_txt(B), "questions": sim_qs}},
}
controler_voix(EX)
assert not PB_VOIX, "\n".join(PB_VOIX)
ecrire(EX)
