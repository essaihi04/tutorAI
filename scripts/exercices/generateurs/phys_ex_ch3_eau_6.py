# Exercice de physique, ch. 3 (propagation d'une onde lumineuse), niveau difficile (« Supérieur ») : identifier un liquide
# par deux figures de diffraction (fente et écran dans une cuve).
# Sources comparées (skill exercices § 2) :
#  - exploration ondes_lumineuses.json : cas_types « indice_par_diffraction » (L = 2λ₀D/a, L' = 2λD/a, λ = λ₀/n,
#    n = L/L'), « milieu » (v = c/n, ν inchangée), « frequence » (λ₀ = c/ν, visible si 400 ≤ λ₀ ≤ 800 nm) ; pieges
#    « croit que la fréquence change dans le verre », « note c la célérité dans l'eau, confond λ₀ et λ », « trouve n < 1 »
#    (rapport inversé) ; a_ne_pas_dire « la couleur change dans le verre, la lumière n'est plus visible dans un milieu »
#    (erreur relevée chez un professeur, Ghaloumi) ; vidéos Ghaloumi (lame de verre, rapport L₂/L₁), Rahou, Boujaada.
#  - nationaux comparés : 2025 R (même idée : liquide, L = 2,4 cm, L' = 1,8 cm, « vérifier que n_L = 1,33 », puis v_L).
#    Ici : la radiation est donnée par sa fréquence (λ₀ à calculer), le « montrer que » porte sur L'/L = 1/n (démonstration
#    complète, pas une vérification), le liquide est inconnu et s'identifie dans un tableau, puis λ dans le liquide et une
#    lecture critique sur la couleur ; données différentes (ν = 4,74·10¹⁴ Hz, a = 0,10 mm, D = 1,20 m, 1,52 / 1,03 cm).
#    Aussi 2021 N (ν = c/λ₀) et 2023 R (QCM : fréquence et milieu).
#  - séries en ligne : recherche web (talamidi séries 1 et 2, moutamadris, série laser 632 nm) : extraits seulement ;
#    les sites sont bloqués par le réseau de la session (talamidi.com, moutamadris.ma non résolus).
import sys, os, math, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *
from _outils import _RACINE

_sp = importlib.util.spec_from_file_location("tp", _RACINE / "backend" / "kaggle_tts" / "texte_parle.py")
tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(tp)


def mots(s):
    """« 3,7 » -> « trois virgule sept » (nombre déjà écrit avec fr())."""
    s = str(s).replace("−", "-").replace(" ", "")
    neg = s.startswith("-"); s = s.lstrip("-")
    if "," in s:
        e, d = s.split(","); r = d.lstrip("0"); z = len(d) - len(r)
        w = tp.nombre_fr(int(e)) + " virgule" + " zéro" * z + (" " + tp.nombre_fr(int(r)) if r else "")
    else:
        w = tp.nombre_fr(int(s))
    return ("moins " if neg else "") + w


def msci(x, ch=3):
    """3,7e-2 -> « trois virgule sept fois dix puissance moins deux »."""
    e = math.floor(math.log10(abs(x))); m = round(x / 10 ** e, ch - 1)
    if abs(m) >= 10: m /= 10; e += 1
    t = mots(fr(m, ch - 1))
    return t if e == 0 else f"{t} fois dix puissance {mots(str(e))}"


SIM = "/media/simulations/physics/ondes-lumineuses-tableau/"
TABLE = [("eau", 1.33), ("éthanol", 1.36), ("glycérol", 1.47)]


def figure(a_mm, D, L_cm, Lp_cm):
    el = [
        {"f": "rect", "de": [0.1, 3.55], "a": [1.3, 4.05], "couleur": "blanc", "remplir": "faible"},
        {"f": "texte", "at": [0.7, 4.35], "t": "laser", "couleur": "rouge", "ancre": "centre", "taille": "petit"},
        {"f": "rect", "de": [2.0, 2.7], "a": [9.3, 4.9], "couleur": "cyan", "remplir": "faible"},
        {"f": "texte", "at": [5.6, 5.1], "t": "cuve (vide, puis remplie du liquide)", "couleur": "cyan", "ancre": "centre", "taille": "petit"},
        {"f": "ligne", "pts": [[1.3, 3.8], [2.8, 3.8]], "couleur": "rouge", "epais": True},
        {"f": "ligne", "pts": [[2.8, 2.9], [2.8, 3.72]], "couleur": "jaune", "epais": True},
        {"f": "ligne", "pts": [[2.8, 3.88], [2.8, 4.7]], "couleur": "jaune", "epais": True},
        {"f": "texte", "at": [2.8, 2.45], "t": f"fente a = {fr(a_mm, 2)} mm", "couleur": "jaune", "ancre": "centre", "taille": "petit"},
        {"f": "ligne", "pts": [[2.8, 3.8], [8.9, 4.4]], "couleur": "rouge", "trait": "pointille"},
        {"f": "ligne", "pts": [[2.8, 3.8], [8.9, 3.2]], "couleur": "rouge", "trait": "pointille"},
        {"f": "ligne", "pts": [[8.9, 2.85], [8.9, 4.75]], "couleur": "blanc", "epais": True},
        {"f": "cote", "de": [2.8, 3.05], "a": [8.9, 3.05], "t": f"D = {fr(D, 2)} m", "couleur": "cyan", "pos": "n"},
        {"f": "texte", "at": [2.4, 1.85], "t": "Écran, cuve vide (air)", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
        {"f": "ellipse", "c": [2.4, 1.0], "rx": 1.15, "ry": 0.3, "couleur": "rouge", "remplir": "rouge"},
        {"f": "cote", "de": [1.25, 0.4], "a": [3.55, 0.4], "t": f"L = {fr(L_cm, 2)} cm", "couleur": "jaune", "pos": "s"},
        {"f": "texte", "at": [6.4, 1.85], "t": "Écran, cuve pleine (liquide)", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
        {"f": "ellipse", "c": [6.4, 1.0], "rx": 1.15 * Lp_cm / L_cm, "ry": 0.3, "couleur": "rouge", "remplir": "rouge"},
        {"f": "cote", "de": [6.4 - 1.15 * Lp_cm / L_cm, 0.4], "a": [6.4 + 1.15 * Lp_cm / L_cm, 0.4], "t": f"L' = {fr(Lp_cm, 2)} cm", "couleur": "jaune", "pos": "s"},
    ]
    return {"type": "schema", "titre": "Diffraction dans une cuve, vide puis remplie", "cadre": {"l": 10, "h": 5.3},
            "legende": "Même laser, même fente, même distance D : seul le milieu change.", "elements": el}


# ---------------------------------------------------------------- données et calculs
C = 3.00e8
NU, A_MM, D, L_CM, LP_CM = 4.74e14, 0.10, 1.20, 1.52, 1.03
LAM0 = C / NU                         # 6,33e-7 m
LAM0_NM = LAM0 * 1e9                  # 633 nm
L_TH = 2 * LAM0 * D / (A_MM * 1e-3) * 100   # 1,52 cm : la mesure est cohérente avec les données
assert abs(L_TH - L_CM) < 0.01
N = L_CM / LP_CM                      # 1,476
N2 = round(N, 2)                      # 1,48
LIQ = min(TABLE, key=lambda t: abs(t[1] - N))[0]   # glycérol
V = C / N2                            # 2,03e8
LAM = round(LAM0_NM) / N2             # 428 nm
s_l0, s_n, s_v, s_lam = fr(LAM0_NM, 0), fr(N2, 2), sci(V), fr(LAM, 0)
tab = " ; ".join(f"{t} : {fr(n, 2)}" for t, n in TABLE)

EX = {
  "id": "phys_ex_ch3_eau_6", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_lumineuses", "cours": "phys_ch3_ondes_lumineuses",
  "titre": "Identifier un liquide par la diffraction", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer λ₀ = c/ν et situer la radiation dans le spectre", "Montrer que L'/L = 1/n (λ = λ₀/n)",
                  "Déduire n de deux largeurs et identifier un milieu", "Calculer v = c/n et λ = λ₀/n",
                  "Critiquer une affirmation : la couleur est fixée par la fréquence"],
  "enonce": {
    "intro": (f"Un laser émet une radiation monochromatique de fréquence ν = {sci(NU)} Hz. Le faisceau traverse une fente de largeur "
              f"a = {fr(A_MM, 2)} mm ; la fente et l'écran sont placés dans une cuve transparente, à la distance D = {fr(D, 2)} m l'un de l'autre. "
              f"Cuve vide (air), la tache centrale mesure L = {fr(L_CM, 2)} cm. On remplit la cuve d'un liquide transparent inconnu, d'indice n, "
              f"sans rien changer d'autre : la tache centrale mesure alors L' = {fr(LP_CM, 2)} cm. "
              f"On suppose les angles petits (tan θ ≈ θ, θ en radian) et l'indice de l'air égal à 1. Indices de quelques liquides : {tab}."),
    "intro_dit": (f"نقراو l'énoncé. واحد le laser كيعطي une radiation monochromatique، la fréquence ديالها nu égale {msci(NU)} hertz. "
                  f"le faisceau كيدوز من واحد la fente، la largeur ديالها a égale {mots(fr(A_MM, 2))} millimètre. la fente و l'écran فواحد la cuve، "
                  f"و la distance بيناتهم D égale {mots(fr(D, 2))} mètre. ملي la cuve خاوية، la tache centrale فيها L égale {mots(fr(L_CM, 2))} centimètre. "
                  f"كنعمرو la cuve بواحد السائل ما عارفينهش، l'indice ديالو n، وما كنبدلو والو: la tache centrale كتولي L prime égale "
                  f"{mots(fr(LP_CM, 2))} centimètre. الزوايا صغار، و l'indice ديال الهوا égale un. وعندنا جدول ديال les indices: "
                  + "، ".join(f"{ {'eau': 'الما', 'éthanol': chr(108) + chr(39) + 'éthanol', 'glycérol': 'le glycérol'}[t] }: {mots(fr(n, 2))}" for t, n in TABLE) + "."),
    "figures": [figure(A_MM, D, L_CM, LP_CM)],
    "donnees": ["c = 3,00 × 10⁸ m/s (vide et air) ; n(air) = 1", f"ν = {sci(NU)} Hz", f"a = {fr(A_MM, 2)} mm ; D = {fr(D, 2)} m",
                f"L = {fr(L_CM, 2)} cm (air) ; L' = {fr(LP_CM, 2)} cm (liquide)", f"Indices : {tab}"],
    "questions": [
      {"id": "1", "texte": "Calculer la longueur d'onde λ₀ de la radiation dans l'air (en nm). Cette radiation est-elle visible ?",
       "texte_dit": "السؤال un: حسب la longueur d'onde lambda zéro ديال la radiation فالهوا، en nanomètre. واش هاد la radiation كتبان؟",
       "reponse": valeur("λ₀", round(LAM0_NM, 1), "nm", f"λ₀ = c/ν = 3,00×10⁸/({sci(NU)}) ≈ {sci(LAM0)} m = {s_l0} nm"),
       "clavier": {"aides": ["λ₀ = c/ν", "1 nm = 10⁻⁹ m", "400 nm ≤ λ₀ ≤ 800 nm"], "pieges": ["λ₀ = ν/c", "λ₀ = c·ν"]},
       "aides": [aide("La fréquence est donnée : quelle relation relie λ₀, c et ν ?", "عندنا la fréquence. أشنو la relation اللي كتربط lambda zéro و c و nu؟"),
                 aide("λ₀ = c/ν en mètre, puis multiplier par 10⁹ pour l'avoir en nm ; comparer à 400 nm et 800 nm.",
                      "lambda zéro égale c sur nu، en mètre. من بعد، multiplier par dix puissance neuf باش تلقاها en nanomètre، وقارنها avec quatre cents et huit cents.")],
       "correction": correction([("1 : λ₀ = c/ν", "lambda zéro égale c sur nu"),
                                 (f"λ₀ = 3,00×10⁸/({sci(NU)}) ≈ {sci(LAM0)} m = {s_l0} nm", f"lambda zéro égale {mots(s_l0)} nanomètres"),
                                 (f"400 nm < {s_l0} nm < 800 nm : radiation visible (rouge)", "radiation visible")],
                                f"السؤال un. lambda zéro égale c sur nu. l'application numérique: trois fois dix puissance huit sur {msci(NU)}. "
                                f"lambda zéro égale {msci(LAM0)} mètre، et lambda zéro égale {mots(s_l0)} nanomètres. "
                                f"وهي entre quatre cents et huit cents nanomètres: radiation visible، حمرا."),
       "explication": "ex_e1", "facile": "fa_e1"},
      {"id": "2", "texte": "Montrer que, dans le liquide, la largeur de la tache centrale s'écrit L' = 2λ₀D/(n·a), puis que L'/L = 1/n.",
       "texte_dit": "السؤال deux: montrer que فالسائل، L prime égale deux lambda zéro D sur n a، ومن بعد montrer que L prime sur L égale un sur n.",
       "reponse": phrase("Dans le liquide, la fréquence ne change pas et v = c/n, donc λ = v/ν = λ₀/n. Pour la tache : tan θ' = L'/(2D) ≈ θ' "
                         "et θ' = λ/a, donc L' = 2λD/a = 2λ₀D/(n·a). Dans l'air : L = 2λ₀D/a. En divisant : L'/L = 1/n."),
       "clavier": {"aides": ["λ = λ₀/n", "θ = λ/a", "tan θ = L/(2D) ≈ θ", "L = 2λ₀D/a"],
                   "pieges": ["λ = n·λ₀", "L' = n·L", "la fréquence change"]},
       "aides": [aide("Qu'est-ce qui change quand la cuve se remplit : a, D, ν ou λ ? Écrivez λ dans le liquide.",
                      "شنو اللي كيتبدل ملي كتعمر la cuve: a، D، nu ولا lambda؟ كتب lambda فالسائل."),
                 aide("λ = λ₀/n ; refaites la démonstration L = 2λD/a avec λ, puis divisez L' par L.",
                      "lambda égale lambda zéro sur n. عاود la démonstration ديال L égale deux lambda D sur a ب lambda، ومن بعد قسم L prime على L.")],
       "correction": correction([("2 : dans le liquide, ν inchangée et v = c/n, donc λ = v/ν = λ₀/n", "lambda égale lambda zéro sur n"),
                                 ("tan θ' = L'/(2D) ≈ θ' et θ' = λ/a ⇒ L' = 2λD/a = 2λ₀D/(n·a)", "L prime égale deux lambda zéro D sur n a"),
                                 ("dans l'air : L = 2λ₀D/a", "فالهوا، L égale"),
                                 ("L'/L = 1/n", "L prime sur L égale un sur n")],
                                "السؤال deux. فالسائل، la fréquence ما كتبدلش، و v égale c sur n، إذن lambda égale v sur nu، يعني lambda égale lambda zéro sur n. "
                                "ف la tache: tangente teta prime égale L prime sur deux D، تقريبا teta prime، و teta prime égale lambda sur a. "
                                "إذن L prime égale deux lambda D sur a، يعني L prime égale deux lambda zéro D sur n a. "
                                "فالهوا، L égale deux lambda zéro D sur a. كنقسمو: L prime sur L égale un sur n."),
       "explication": "ex_e2", "facile": "fa_e2"},
      {"id": "3", "texte": "En déduire la valeur de l'indice n du liquide, puis identifier ce liquide à l'aide du tableau.",
       "texte_dit": "السؤال trois: استنتج la valeur ديال l'indice n ديال السائل، ومن بعد عرف أشنو هو بالجدول.",
       "reponse": valeur("n", round(N, 4), "", f"n = L/L' = {fr(L_CM, 2)}/{fr(LP_CM, 2)} ≈ {s_n}"),
       "clavier": {"aides": ["n = L/L'", "sans unité", "n > 1"], "pieges": ["n = L'/L", "n < 1"]},
       "aides": [aide("De L'/L = 1/n, que vaut n ? Les deux largeurs sont dans la même unité : pas de conversion.",
                      "من L prime sur L égale un sur n، شحال n؟ les deux largeurs بنفس الوحدة: ما تحولش."),
                 aide("n = L/L' (doit être plus grand que 1), puis cherchez l'indice le plus proche dans le tableau.",
                      "n égale L sur L prime، و n خاصو يكون supérieur à un. من بعد قلب فالجدول على l'indice الأقرب.")],
       "correction": correction([("3 : L'/L = 1/n donc n = L/L'", "n égale L sur L prime"),
                                 (f"n = {fr(L_CM, 2)}/{fr(LP_CM, 2)} ≈ {s_n}", f"n égale {mots(s_n)}"),
                                 (f"valeur la plus proche du tableau : {LIQ} ({fr(dict(TABLE)[LIQ], 2)})", "le glycérol")],
                                f"السؤال trois. n égale L sur L prime. l'application numérique: {mots(fr(L_CM, 2))} sur {mots(fr(LP_CM, 2))}. n égale {mots(s_n)}. "
                                f"فالجدول، القيمة الأقرب هي ديال le glycérol: n égale {mots(fr(dict(TABLE)[LIQ], 2))}. إذن السائل هو le glycérol."),
       "explication": "ex_e3", "facile": "fa_e3"},
      {"id": "4", "texte": "Calculer la célérité v de la lumière du laser dans ce liquide.",
       "texte_dit": "السؤال quatre: حسب la célérité v ديال الضو ديال le laser فهاد السائل.",
       "reponse": valeur("v", round(V, -5), "m/s", f"v = c/n = 3,00×10⁸/{s_n} ≈ {s_v} m/s"),
       "clavier": {"aides": ["n = c/v", "v = c/n", "m/s"], "pieges": ["v = c·n", "v > c"]},
       "aides": [aide("Dans un milieu d'indice n, la lumière va moins vite que dans le vide.", "فواحد milieu d'indice n، الضو كيمشي بشوية على le vide."),
                 aide("De n = c/v on tire v = c/n.", "من n égale c sur v، كنخرجو v égale c sur n.")],
       "correction": correction([("4 : v = c/n", "v égale c sur n"), (f"v = 3,00×10⁸/{s_n} ≈ {s_v} m/s (< c)", f"v égale {msci(V)}")],
                                f"السؤال quatre. v égale c sur n. l'application numérique: trois fois dix puissance huit sur {mots(s_n)}. "
                                f"v égale {msci(V)} mètres par seconde، صغر من c."),
       "explication": "ex_e4", "facile": "fa_e4"},
      {"id": "5", "texte": "Calculer la longueur d'onde λ de la radiation dans le liquide.",
       "texte_dit": "السؤال cinq: حسب la longueur d'onde lambda ديال la radiation فالسائل.",
       "reponse": valeur("λ", round(LAM, 1), "nm", f"λ = λ₀/n = {s_l0}/{s_n} ≈ {s_lam} nm"),
       "clavier": {"aides": ["λ = λ₀/n", "nm"], "pieges": ["λ = λ₀·n", "λ = c/ν"]},
       "aides": [aide("Dans le liquide l'onde ralentit mais garde sa fréquence : elle se resserre.", "فالسائل l'onde كتمشي بشوية، ولكن كتبقى بنفس la fréquence: كتقرب."),
                 aide("λ = λ₀/n ; on peut rester en nm.", "lambda égale lambda zéro sur n. تقدر تبقى en nanomètre.")],
       "correction": correction([("5 : λ = λ₀/n", "lambda égale lambda zéro sur n"), (f"λ = {s_l0}/{s_n} ≈ {s_lam} nm", f"lambda égale {mots(s_lam)} nanomètres")],
                                f"السؤال cinq. lambda égale lambda zéro sur n. l'application numérique: {mots(s_l0)} sur {mots(s_n)}. lambda égale {mots(s_lam)} nanomètres."),
       "explication": "ex_e5", "facile": "fa_e5"},
      {"id": "6", "texte": (f"Un élève affirme : « Dans le liquide, λ = {s_lam} nm : c'est une longueur d'onde de la lumière violette ; "
                            "la tache observée sur l'écran immergé est donc violette. » Critiquer cette affirmation."),
       "texte_dit": (f"السؤال six: واحد التلميذ قال: فالسائل، lambda égale {mots(s_lam)} nanomètres، وهادي longueur d'onde ديال le violet، "
                     "إذن la tache فوق l'écran اللي فالسائل كتولي violette. critiquer هاد الكلام."),
       "reponse": phrase(f"L'affirmation est fausse. La couleur d'une radiation est fixée par sa fréquence, qui ne change pas d'un milieu à l'autre "
                         f"(ν = {sci(NU)} Hz). Les limites 400 nm – 800 nm du visible sont des longueurs d'onde dans le vide : on compare λ₀ = {s_l0} nm, "
                         "pas λ. La tache reste rouge ; seules v et λ ont diminué."),
       "clavier": {"aides": ["la couleur est fixée par ν", "ν ne dépend pas du milieu", "400 – 800 nm : dans le vide"],
                   "pieges": ["la couleur change dans le liquide", "on compare λ à 400 nm"]},
       "aides": [aide("Qu'est-ce qui fixe la couleur d'une radiation : sa longueur d'onde dans le milieu, ou sa fréquence ?",
                      "شنو اللي كيعطي اللون ديال radiation: la longueur d'onde فle milieu، ولا la fréquence؟"),
                 aide("ν ne change pas dans le liquide ; et les bornes 400 nm et 800 nm sont données dans le vide.",
                      "la fréquence ما كتبدلش فالسائل. و les bornes quatre cents et huit cents nanomètres، كنعطيوهم فle vide.")],
       "correction": correction([("6 : l'affirmation est fausse", "هاد الكلام غالط"),
                                 (f"la couleur est fixée par ν, qui ne change pas dans le liquide (ν = {sci(NU)} Hz)", "اللون مربوط ب la fréquence"),
                                 (f"400 – 800 nm : bornes dans le vide ; λ₀ = {s_l0} nm : rouge", "les bornes"),
                                 ("la tache reste rouge ; seules v et λ diminuent", "la tache كتبقى حمرا")],
                                "السؤال six. هاد الكلام غالط. اللون مربوط ب la fréquence، و la fréquence ما كتبدلش فالسائل. "
                                f"و les bornes quatre cents et huit cents nanomètres كنعطيوهم فle vide: كنقارنو lambda zéro égale {mots(s_l0)} nanomètres، "
                                "ماشي lambda. إذن la tache كتبقى حمرا. غير v و lambda اللي نقصو."),
       "explication": "ex_e6", "facile": "fa_e6"},
    ]
  },
}

# ---------------------------------------------------------------- explication animée
NOM_LIQ = "le " + LIQ
m1 = ("le spectre visible، de quatre cents nanomètres، le violet، à huit cents nanomètres، le rouge. "
      f"فالتمرين، ما عندناش lambda zéro، عندنا la fréquence: nu égale {msci(NU)} hertz. "
      f"lambda zéro égale c sur nu: trois fois dix puissance huit sur {msci(NU)}. lambda zéro égale {msci(LAM0)} mètre، "
      f"et lambda zéro égale {mots(s_l0)} nanomètres. كنحطوها فوق le spectre: entre quatre cents et huit cents nanomètres. "
      "إذن radiation visible، وحمرا.")
m2 = ("فla simulation، la fente و l'écran فواحد la cuve. la cuve خاوية: فالهوا، la tache centrale فيها L égale deux virgule quatre centimètres. "
      "دابا كنعمرو la cuve: شوف، la tache كتصغار. علاش؟ فالسائل، la fréquence ما كتبدلش، ولكن lambda égale lambda zéro sur n. "
      "فالهوا: L égale deux lambda zéro D sur a. فالسائل، نفس a ونفس D: L prime égale deux lambda D sur a، "
      "يعني L prime égale deux lambda zéro D sur n a. كنقسمو L prime على L: deux lambda zéro D sur a كيمشيو، كيبقى L prime sur L égale un sur n.")
m3 = ("شوف القياسات فla simulation: فالهوا، L égale deux virgule quatre centimètres، وفالما، L prime égale un virgule huit centimètre. "
      "n égale L sur L prime: n égale un virgule trente-trois، هو الما. "
      f"فالتمرين، L égale {mots(fr(L_CM, 2))} centimètre، و L prime égale {mots(fr(LP_CM, 2))} centimètre. "
      f"n égale {mots(fr(L_CM, 2))} sur {mots(fr(LP_CM, 2))}. n égale {mots(s_n)}. "
      f"فالجدول، القيمة الأقرب هي ديال {NOM_LIQ}: n égale {mots(fr(dict(TABLE)[LIQ], 2))}.")
m4 = ("l'indice: n égale c sur v، إذن v égale c sur n. فla simulation، الما: n égale un virgule trente-trois، والزجاج: environ un virgule cinq. "
      "كلما n كبير، كلما الضو كيمشي بشوية. "
      f"فالتمرين، n égale {mots(s_n)}: v égale trois fois dix puissance huit sur {mots(s_n)}. v égale {msci(V)} mètres par seconde، صغر من c.")
m5 = (f"دابا la simulation فيها القيم ديال التمرين: lambda zéro égale {mots(round(LAM0_NM))} nanomètres، و n égale {mots(s_n)}. "
      "شوف l'onde فالهوا. ودابا كتدخل للسائل: les crêtes كيقربو لبعضياتهم. la longueur d'onde كتنقص. "
      f"lambda égale lambda zéro sur n: {mots(s_l0)} sur {mots(s_n)}. lambda égale {mots(s_lam)} nanomètres.")
m6 = ("نفس القيم. شوف les deux compteurs: واحد فالهوا، وواحد فالسائل. بجوج كيعطيو نفس العدد: نفس la fréquence. "
      "واللون مربوط ب la fréquence، ماشي ب lambda. "
      f"فالسائل lambda égale {mots(s_lam)} nanomètres، ولكن الضو كيبقى حمر. "
      "les bornes quatre cents et huit cents nanomètres، كنعطيوهم فle vide. إذن التلميذ غالط: la tache فوق l'écran كتبقى حمرا.")
CUVE = SIM + "diffraction.html?vue=cuve"
EX["explication"] = {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
  diapo_sim("ex_e1", "Question 1 : λ₀ = c/ν, dans le spectre", "Visible : 400 nm ≤ λ₀ ≤ 800 nm.", SIM + f"spectre.html?lambda_nm={round(LAM0_NM)}",
            "Le spectre visible et la radiation du laser", m1,
            [("λ₀ = c/ν", "lambda zéro égale c sur nu:"), (f"λ₀ ≈ {sci(LAM0)} m = {s_l0} nm : visible, rouge", "إذن radiation visible")],
            [dict(mot="le spectre visible", commande="play_until", parametres={"moment": "bande_peinte"}),
             dict(mot="le spectre visible", repere="visible"),
             dict(mot="lambda zéro égale c sur nu:", cible="centre:0"),
             dict(mot="كنحطوها فوق le spectre", commande="play_until", parametres={"moment": "valeur"}),
             dict(mot="كنحطوها فوق le spectre", repere="curseur"),
             dict(mot="إذن radiation visible", repere="couleur"),
             dict(mot="إذن radiation visible", cible="centre:1")]),
  diapo_sim("ex_e2", "Question 2 : montrer que L'/L = 1/n", "Même a, même D, λ = λ₀/n.", CUVE,
            "La cuve se remplit : la tache se resserre", m2,
            [("L' = 2λD/a = 2λ₀D/(n·a)", "يعني L prime égale deux lambda zéro D sur n a"), ("L'/L = 1/n", "كيبقى L prime sur L égale un sur n")],
            [dict(mot="la cuve خاوية", commande="play_until", parametres={"moment": "mesure_L"}),
             dict(mot="دابا كنعمرو la cuve", commande="play_until", parametres={"moment": "cuve_se_remplit"}),
             dict(mot="دابا كنعمرو la cuve", repere="cuve"),
             dict(mot="شوف، la tache كتصغار", commande="play_until", parametres={"moment": "tache_se_resserre"}),
             dict(mot="L prime égale deux lambda D sur a", commande="play_until", parametres={"moment": "mesure_L_prime"}),
             dict(mot="يعني L prime égale deux lambda zéro D sur n a", cible="centre:0"),
             dict(mot="كيبقى L prime sur L égale un sur n", cible="centre:1")]),
  diapo_sim("ex_e3", "Question 3 : n = L/L', puis le tableau", "n = L/L' > 1.", CUVE + "&depart=tache_se_resserre",
            "Les deux largeurs, dans l'air et dans le liquide", m3,
            [("n = L/L'", "n égale L sur L prime:"), (f"n = {fr(L_CM, 2)}/{fr(LP_CM, 2)} ≈ {s_n} : {LIQ}", f"n égale {mots(s_n)}.")],
            [dict(mot="شوف القياسات", commande="play_until", parametres={"moment": "mesure_L_prime"}),
             dict(mot="فالهوا، L égale", repere="L"),
             dict(mot="n égale L sur L prime:", cible="centre:0"),
             dict(mot=f"n égale {mots(s_n)}.", cible="centre:1")]),
  diapo_sim("ex_e4", "Question 4 : v = c/n", "Plus n est grand, plus la lumière ralentit.", SIM + "indice.html",
            "La lumière ralentit dans les milieux", m4,
            [("v = c/n", "إذن v égale c sur n"), (f"v = 3,00×10⁸/{s_n} ≈ {s_v} m/s", f"v égale {msci(V)} mètres par seconde")],
            [dict(mot="l'indice: n égale c sur v", commande="play_until", parametres={"moment": "indice"}),
             dict(mot="إذن v égale c sur n", cible="centre:0"),
             dict(mot="الما: n égale", repere="eau"),
             dict(mot="والزجاج: environ", repere="verre"),
             dict(mot=f"v égale {msci(V)} mètres par seconde", cible="centre:1")]),
  diapo_sim("ex_e5", "Question 5 : λ = λ₀/n dans le liquide", "L'onde se resserre : λ < λ₀.", SIM + "milieu.html",
            "L'onde du laser entre dans le liquide", m5,
            [(f"λ = λ₀/n = {s_l0}/{s_n} ≈ {s_lam} nm", f"lambda égale {mots(s_lam)} nanomètres")],
            [dict(mot="دابا la simulation فيها", commande="set_parameters", parametres={"n": N2, "lambda0_nm": round(LAM0_NM)}),
             dict(mot="شوف l'onde فالهوا", commande="play_until", parametres={"moment": "onde_dans_air"}),
             dict(mot="شوف l'onde فالهوا", repere="lambda0"),
             dict(mot="ودابا كتدخل للسائل", commande="play_until", parametres={"moment": "lambda_serree"}),
             dict(mot="la longueur d'onde كتنقص", commande="play_until", parametres={"moment": "mesure_lambda"}),
             dict(mot="la longueur d'onde كتنقص", repere="lambda"),
             dict(mot=f"lambda égale {mots(s_lam)} nanomètres", cible="centre:0")]),
  diapo_sim("ex_e6", "Question 6 : la couleur ne change pas", "La couleur est fixée par ν, qui ne change pas.", SIM + "milieu.html",
            "Deux compteurs : même fréquence dans l'air et dans le liquide", m6,
            [("Même ν ⇒ même couleur", "نفس la fréquence"), ("400 – 800 nm : bornes dans le vide", "les bornes quatre cents")],
            [dict(mot="نفس القيم", commande="set_parameters", parametres={"n": N2, "lambda0_nm": round(LAM0_NM)}),
             dict(mot="واحد فالهوا", repere="compteur_air"), dict(mot="وواحد فالسائل", repere="compteur_verre"),
             dict(mot="بجوج كيعطيو نفس العدد", commande="play_until", parametres={"moment": "compte_frequence"}),
             dict(mot="نفس la fréquence", cible="centre:0"),
             dict(mot="les bornes quatre cents", cible="centre:1")]),
]}]}

# ---------------------------------------------------------------- version facile
EX["facile"] = {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
  qcm_facile("fa_e1", "Plus facile : λ₀ à partir de ν", "نتمرنو بسؤال ساهل. اختار الجواب الصحيح.",
             f"ν = {sci(NU)} Hz et c = 3,00 × 10⁸ m/s. La longueur d'onde dans l'air vaut…",
             [f"{sci(LAM0)} nm", f"{s_l0} nm", f"{sci(C * NU)} m"], 1, {
               "1": {"juste": rep(f"برافو! lambda zéro égale c sur nu، يعني lambda zéro égale {mots(s_l0)} nanomètres.", f"Juste : λ₀ = c/ν = {sci(LAM0)} m = {s_l0} nm.")},
               "0": {"1": rep("الرقم صحيح، ولكن الوحدة؟ c sur nu كتعطي mètre، ماشي nanomètre. عاود اختار.", "Le nombre est en mètre, pas en nm. Réessaie."),
                     "2": rep(f"الجواب هو lambda zéro égale {mots(s_l0)} nanomètres. c sur nu كتعطي mètre، ومن بعد كنضربو par dix puissance neuf.", f"Réponse : {sci(LAM0)} m = {s_l0} nm.")},
               "2": {"1": rep("ضربتي c فnu: هادي ماشي longueur. lambda zéro هي c sur nu. عاود اختار.", "Tu as multiplié c par ν ; λ₀ = c/ν. Réessaie."),
                     "2": rep(f"الجواب هو lambda zéro égale {mots(s_l0)} nanomètres: lambda zéro égale c sur nu.", f"Réponse : λ₀ = c/ν = {s_l0} nm.")}},
             "Quelle est la longueur d'onde dans l'air ?"),
  assoc_facile("fa_e2", "Plus facile : air ou liquide", "نتمرنو: ربط كل حالة مع la largeur ديال la tache ديالها.",
               "Même laser, même fente, même D.", "Relie chaque milieu à l'expression de la largeur de la tache centrale.",
               [("1", "Cuve vide (air)"), ("2", "Cuve pleine (liquide d'indice n)")],
               [("a", "L = 2λ₀D/a"), ("b", "L' = 2λ₀D/(n·a)"), ("c", "L' = 2n·λ₀D/a")],
               {"1": "a", "2": "b"}, {
                 "1-a": (True, "Oui : dans l'air n ≈ 1, la longueur d'onde est λ₀.", "برافو: فالهوا، la longueur d'onde هي lambda zéro."),
                 "1-b": (False, "Dans l'air n ≈ 1 : pas de division par l'indice du liquide.", "لا، فالهوا n environ un، ما كنقسموش على l'indice ديال السائل."),
                 "1-c": (False, "Dans l'air, rien ne multiplie λ₀.", "لا، فالهوا والو ما كيضرب lambda zéro."),
                 "2-a": (False, "Dans le liquide, la longueur d'onde n'est plus λ₀ : elle devient λ₀/n.", "لا، فالسائل la longueur d'onde ولات lambda zéro sur n."),
                 "2-b": (True, "Oui : λ = λ₀/n, donc L' = 2λ₀D/(n·a).", "برافو: lambda égale lambda zéro sur n، إذن L prime كتصغار."),
                 "2-c": (False, "Multiplier par n agrandirait la tache ; or elle se resserre.", "لا، يلا ضربنا فn، la tache كتكبر، وهي كتصغار.")},
               ("Dans le liquide, λ est divisée par n, donc L aussi : L'/L = 1/n.", "فالسائل، lambda كتتقسم على n، و L حتى هي: L prime sur L égale un sur n.")),
  qcm_facile("fa_e3", "Plus facile : l'indice", "سؤال ساهل على l'indice.",
             f"L = {fr(L_CM, 2)} cm (air) et L' = {fr(LP_CM, 2)} cm (liquide). L'indice du liquide vaut…",
             [f"n ≈ {s_n}", f"n ≈ {fr(LP_CM / L_CM, 2)}", f"n ≈ {fr(L_CM * LP_CM, 2)}"], 0, {
               "0": {"juste": rep(f"برافو! n égale L sur L prime، n égale {mots(s_n)}، و n supérieur à un.", f"Juste : n = L/L' ≈ {s_n}.")},
               "1": {"1": rep("رد البال: n خاصو يكون supérieur à un. واش قلبتي le rapport؟ عاود اختار.", "n doit dépasser 1 : le rapport est-il inversé ? Réessaie."),
                     "2": rep(f"الجواب هو n égale {mots(s_n)}: n égale L sur L prime، ماشي L prime sur L.", f"Réponse : n = L/L' ≈ {s_n}.")},
               "2": {"1": rep("ضربتي les deux largeurs. l'indice هو واحد le rapport. عاود اختار.", "Tu as multiplié les largeurs ; n est un rapport. Réessaie."),
                     "2": rep(f"الجواب هو n égale {mots(s_n)}: L sur L prime.", f"Réponse : n = L/L' ≈ {s_n}.")}},
             "Quelle est la valeur de l'indice du liquide ?"),
  vf_facile("fa_e4", "Plus facile : la célérité", "سؤال ساهل: صحيح ولا غالط؟", f"Le liquide a pour indice n = {s_n}.", [
              (f"v = c/n ≈ {s_v} m/s.", True, "v = c/n, plus petite que c."),
              ("Dans le liquide, la lumière va plus vite que dans l'air.", False, "n > 1 donc v = c/n < c : elle ralentit."),
              (f"v = c·n ≈ {sci(C * N2)} m/s.", False, "Une célérité plus grande que c est impossible : v = c/n.")]),
  qcm_facile("fa_e5", "Plus facile : λ dans le liquide", "سؤال ساهل. اختار الجواب.",
             f"λ₀ = {s_l0} nm et n = {s_n}. Dans le liquide, λ vaut…",
             [f"{fr(round(LAM0_NM) * N2, 0)} nm", f"{s_l0} nm", f"{s_lam} nm"], 2, {
               "2": {"juste": rep(f"برافو! lambda égale lambda zéro sur n، lambda égale {mots(s_lam)} nanomètres.", f"Juste : λ = λ₀/n ≈ {s_lam} nm.")},
               "0": {"1": rep("فالسائل l'onde كتقرب: lambda خاصها تصغر. عاود اختار.", "L'onde se resserre : λ diminue. Réessaie."),
                     "2": rep(f"الجواب هو lambda égale {mots(s_lam)} nanomètres: كنقسمو على n.", f"Réponse : λ = λ₀/n ≈ {s_lam} nm.")},
               "1": {"1": rep("la fréquence هي اللي ما كتبدلش، ماشي lambda. عاود اختار.", "C'est ν qui ne change pas, pas λ. Réessaie."),
                     "2": rep(f"الجواب هو lambda égale {mots(s_lam)} nanomètres: lambda كتبدل مع le milieu.", f"Réponse : λ ≈ {s_lam} nm.")}},
             "Dans le liquide, quelle est la longueur d'onde ?"),
  vf_facile("fa_e6", "Plus facile : la couleur", "آخر سؤال ساهل: صحيح ولا غالط؟", "Le laser rouge éclaire la fente dans le liquide.", [
              ("La fréquence de la radiation est la même dans l'air et dans le liquide.", True, "La fréquence est imposée par la source."),
              (f"Dans le liquide λ = {s_lam} nm, donc la lumière devient violette.", False, "La couleur est fixée par la fréquence, qui ne change pas : elle reste rouge."),
              ("Les bornes 400 nm et 800 nm du visible sont des longueurs d'onde dans le vide.", True, "On y compare λ₀, pas la longueur d'onde dans un milieu.")]),
]}]}

# ---------------------------------------------------------------- exercice semblable (cette fois, de l'eau)
b_nu, b_a, b_D, b_L, b_Lp = 5.64e14, 0.08, 1.50, 2.00, 1.50
b_l0 = C / b_nu; b_l0nm = b_l0 * 1e9
assert abs(2 * b_l0 * b_D / (b_a * 1e-3) * 100 - b_L) < 0.01
b_n = b_L / b_Lp; b_n2 = round(b_n, 2); b_liq = min(TABLE, key=lambda t: abs(t[1] - b_n))[0]
b_v = C / b_n2; b_lam = round(b_l0nm) / b_n2
EX["similaire"] = {"id": "phys_ex_ch3_eau_6_b", "titre": "Même exercice, autres données", "enonce": {
  "intro": (f"Un laser émet une radiation de fréquence ν = {sci(b_nu)} Hz. Fente de largeur a = {fr(b_a, 2)} mm, écran à D = {fr(b_D, 2)} m, "
            f"tous deux dans une cuve. Cuve vide : L = {fr(b_L, 2)} cm ; cuve remplie d'un liquide inconnu : L' = {fr(b_Lp, 2)} cm. "
            f"Indices : {tab}."),
  "intro_dit": (f"نفس التمرين، بقيم أخرى. nu égale {msci(b_nu)} hertz، a égale {mots(fr(b_a, 2))} millimètre، و D égale {mots(fr(b_D, 2))} mètre. "
                f"la cuve خاوية: L égale {mots(fr(b_L, 2))} centimètres. la cuve عامرة: L prime égale {mots(fr(b_Lp, 2))} centimètre."),
  "figures": [figure(b_a, b_D, b_L, b_Lp)],
  "donnees": ["c = 3,00 × 10⁸ m/s", f"ν = {sci(b_nu)} Hz", f"a = {fr(b_a, 2)} mm ; D = {fr(b_D, 2)} m", f"L = {fr(b_L, 2)} cm ; L' = {fr(b_Lp, 2)} cm", f"Indices : {tab}"],
  "questions": [
    {"id": "1", "texte": "Calculer λ₀ (en nm). La radiation est-elle visible ?",
     "reponse": valeur("λ₀", round(b_l0nm, 1), "nm", f"λ₀ = c/ν = 3,00×10⁸/({sci(b_nu)}) ≈ {sci(b_l0)} m = {fr(b_l0nm, 0)} nm"),
     "clavier": {"aides": ["λ₀ = c/ν", "nm"], "pieges": ["λ₀ = ν/c"]},
     "correction": correction([("1 : λ₀ = c/ν", "lambda zéro égale c sur nu"), (f"λ₀ ≈ {fr(b_l0nm, 0)} nm : visible (vert)", f"lambda zéro égale {mots(fr(b_l0nm, 0))} nanomètres")],
                              f"السؤال un. lambda zéro égale c sur nu. lambda zéro égale {mots(fr(b_l0nm, 0))} nanomètres: radiation visible، خضرا.")},
    {"id": "2", "texte": "Montrer que L' = 2λ₀D/(n·a), puis que L'/L = 1/n.",
     "reponse": phrase("ν inchangée, v = c/n donc λ = λ₀/n ; L' = 2λD/a = 2λ₀D/(n·a) ; L = 2λ₀D/a ; donc L'/L = 1/n."),
     "clavier": {"aides": ["λ = λ₀/n", "L = 2λD/a"], "pieges": ["L' = n·L"]},
     "correction": correction([("2 : λ = λ₀/n donc L' = 2λ₀D/(n·a)", "L prime égale deux lambda zéro D sur n a"), ("L'/L = 1/n", "L prime sur L égale un sur n")],
                              "السؤال deux. lambda égale lambda zéro sur n، إذن L prime égale deux lambda zéro D sur n a. و L égale deux lambda zéro D sur a: L prime sur L égale un sur n.")},
    {"id": "3", "texte": "En déduire n, puis identifier le liquide.",
     "reponse": valeur("n", round(b_n, 4), "", f"n = L/L' = {fr(b_L, 2)}/{fr(b_Lp, 2)} ≈ {fr(b_n2, 2)}"),
     "clavier": {"aides": ["n = L/L'"], "pieges": ["n = L'/L"]},
     "correction": correction([("3 : n = L/L'", "n égale L sur L prime"), (f"n ≈ {fr(b_n2, 2)} : {b_liq}", f"n égale {mots(fr(b_n2, 2))}")],
                              f"السؤال trois. n égale L sur L prime. n égale {mots(fr(b_n2, 2))}: هو الما.")},
    {"id": "4", "texte": "Calculer la célérité v de la lumière dans ce liquide.",
     "reponse": valeur("v", round(b_v, -5), "m/s", f"v = c/n = 3,00×10⁸/{fr(b_n2, 2)} ≈ {sci(b_v)} m/s"),
     "clavier": {"aides": ["v = c/n"], "pieges": ["v = c·n"]},
     "correction": correction([("4 : v = c/n", "v égale c sur n"), (f"v ≈ {sci(b_v)} m/s", f"v égale {msci(b_v)}")],
                              f"السؤال quatre. v égale c sur n. v égale {msci(b_v)} mètres par seconde.")},
    {"id": "5", "texte": "Calculer λ dans le liquide.",
     "reponse": valeur("λ", round(b_lam, 1), "nm", f"λ = λ₀/n = {round(b_l0nm)}/{fr(b_n2, 2)} ≈ {fr(b_lam, 0)} nm"),
     "clavier": {"aides": ["λ = λ₀/n"], "pieges": ["λ = λ₀·n"]},
     "correction": correction([("5 : λ = λ₀/n", "lambda égale lambda zéro sur n"), (f"λ ≈ {fr(b_lam, 0)} nm", f"lambda égale {mots(fr(b_lam, 0))} nanomètres")],
                              f"السؤال cinq. lambda égale lambda zéro sur n. lambda égale {mots(fr(b_lam, 0))} nanomètres.")},
    {"id": "6", "texte": f"Un élève affirme : « Dans l'eau, λ = {fr(b_lam, 0)} nm, à la limite du violet : la tache devient violette. » Critiquer.",
     "reponse": phrase("Faux : la couleur est fixée par la fréquence, qui ne change pas dans l'eau ; les bornes 400 – 800 nm sont données dans le vide (λ₀). La tache reste verte."),
     "clavier": {"aides": ["la couleur est fixée par ν"], "pieges": ["la couleur change dans l'eau"]},
     "correction": correction([("6 : faux, la couleur est fixée par ν (inchangée)", "اللون مربوط ب la fréquence"), ("bornes du visible dans le vide : la tache reste verte", "كتبقى خضرا")],
                              "السؤال six. غالط. اللون مربوط ب la fréquence، و la fréquence ما كتبدلش فالما. les bornes كنعطيوهم فle vide. la tache كتبقى خضرا.")},
  ]}}

ecrire(EX)
