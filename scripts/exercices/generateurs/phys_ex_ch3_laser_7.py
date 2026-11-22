# Exercice de physique, ch. 3 (propagation d'une onde lumineuse), niveau difficile (« Supérieur ») : identifier un laser
# inconnu par une série de fentes (courbe L = f(1/a)), puis s'en servir pour mesurer une fente inconnue, avec une lecture
# critique de l'approximation tan θ ≈ θ.
# Sources comparées (skill exercices § 2) :
#  - exploration ondes_lumineuses.json : cas_types « etablir_L » (quatre lignes : tan θ = L/(2D), θ petit, θ = λ/a,
#    égalité), « courbe » (droite par l'origine, coefficient directeur avec unités converties, identification k = 2λD,
#    λ en nm vérifiée dans le visible), « frequence » (ν = c/λ₀) ; pieges « lit la pente sans convertir les axes »
#    (mm⁻¹, mm² → m²), « lit a sur un axe gradué en 1/a », « prend la pente pour λ dans toutes les courbes »,
#    « calculatrice en degrés pour vérifier tan θ ≈ θ » ; erreurs des profs : courbes aux valeurs impossibles
#    (θ = 1,4 rad, λ = 7·10⁻⁵ m), « tan θ = θ » écrit au tableau ; vidéos Laksabi (trois courbes), Taousse (méthode
#    graphique en trois temps), Driss DOTCOM (courbe L = f(1/a)).
#  - nationaux comparés : 2013 N (L = f(1/a), cité par l'exploration), 2021 N (L = f(D), pente puis λ, puis cheveu),
#    2019 R (analyse dimensionnelle), 2017 R. Ici : cinq fentes avec un tableau ET une courbe à exploiter, λ inconnue
#    (laser à identifier par ν et la couleur), réutilisation de la droite pour une fente inconnue (1/a = L/k), et
#    contrôle critique de tan θ ≈ θ sur le cas le plus défavorable : chaîne et données différentes de tout national.
#    Hors cadre évité : pas d'interférences, pas de loi de Cauchy, pas de calcul d'incertitude formel (seulement
#    l'idée, dans la correction, que la droite moyenne les erreurs de lecture des points).
#  - séries en ligne : recherche web (talamidi série 2 : approximation tan θ ≈ θ en radian ; série Google Docs « laser
#    632 nm » ; moutamadris) : extraits seulement ; les sites sont bloqués par le réseau de la session.
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
C = 3.00e8
A = [0.05, 0.08, 0.10, 0.16, 0.20]                       # mm


def courbe(D, Lmes, k_mm2, ymax):
    xs = [1 / a for a in A]
    el = [{"f": "courbe", "expr": f"{k_mm2}*x", "de": 0, "a": 21.5, "couleur": "cyan", "texte": "droite moyenne", "texte_x": 14, "pos": "no"}]
    el += [{"f": "point", "at": [round(x, 3), L], "couleur": "jaune"} for x, L in zip(xs, Lmes)]
    return {"type": "courbe", "titre": f"L en fonction de 1/a (D = {fr(D, 2)} m)",
            "legende": "Chaque point est une fente ; la droite moyenne passe par l'origine.",
            "axes": {"x": {"min": 0, "max": 22, "nom": "1/a", "unite": "mm⁻¹", "graduations": [5, 10, 15, 20]},
                     "y": {"min": 0, "max": ymax, "nom": "L", "unite": "mm", "graduations": list(range(10, ymax, 10))}},
            "elements": el}


def tableau(Lmes):
    return [f"a (mm) : {' ; '.join(fr(a, 2) for a in A)}",
            f"1/a (mm⁻¹) : {' ; '.join(fr(1 / a, 2) for a in A)}",
            f"L (mm) : {' ; '.join(fr(L, 1) for L in Lmes)}"]


# ---------------------------------------------------------------- données et calculs
D, LAM_VRAI = 1.60, 532e-9
LMES = [34.0, 21.4, 17.0, 10.6, 8.5]                     # mesures (mm), lues à la règle
for a, L in zip(A, LMES):                                 # cohérentes avec λ = 532 nm à 1 % près
    assert abs(L - 2 * LAM_VRAI * D / (a * 1e-3) * 1e3) / L < 0.012
X_LU, Y_LU = 20, 34                                       # point de la droite lu sur la courbe
K_MM2 = Y_LU / X_LU                                       # 1,7 mm²
K = K_MM2 * 1e-6                                          # m²
LAM = K / (2 * D)                                         # 5,31e-7 m
LAM_NM = LAM * 1e9
NU = C / LAM                                              # 5,65e14 Hz
L_INC = 13.6                                              # mm, fente inconnue
INV_A = L_INC / K_MM2                                     # 8 mm⁻¹
A_INC = 1 / INV_A                                         # 0,125 mm
TH = LAM / (A[0] * 1e-3)                                  # 1,06e-2 rad
TAN = math.tan(TH)
ECART = (TAN - TH) / TH * 100                             # en %
s_k, s_lam, s_nu, s_a, s_th = fr(K_MM2, 2), fr(LAM_NM, 0), sci(NU), fr(A_INC, 3), sci(TH)
# vérification indépendante de la pente : moindres carrés passant par l'origine
k_mc = sum((1 / a) * L for a, L in zip(A, LMES)) / sum((1 / a) ** 2 for a in A)
assert abs(k_mc - K_MM2) / K_MM2 < 0.01

EX = {
  "id": "phys_ex_ch3_laser_7", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_lumineuses", "cours": "phys_ch3_ondes_lumineuses",
  "titre": "Identifier un laser inconnu, puis mesurer une fente", "niveau": "difficile", "duree_min": 40,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Établir L = 2λD·(1/a)", "Exploiter une courbe linéaire : coefficient directeur avec unités",
                  "Identifier k = 2λD et calculer λ", "Calculer ν = c/λ et nommer la couleur",
                  "Utiliser la droite pour une mesure inconnue", "Juger l'approximation tan θ ≈ θ"],
  "enonce": {
    "intro": (f"Un laser de laboratoire a perdu son étiquette : sa longueur d'onde λ est inconnue. On éclaire successivement cinq fentes "
              f"de largeurs a connues ; l'écran reste à la distance D = {fr(D, 2)} m des fentes. Pour chaque fente, on mesure à la règle la "
              "largeur L de la tache centrale (tableau). La courbe représente L en fonction de 1/a. Ensuite, sans rien changer d'autre, "
              f"on place une fente de largeur inconnue a' : sa tache centrale mesure L' = {fr(L_INC, 1)} mm. "
              "Données : c = 3,00 × 10⁸ m/s ; tan θ ≈ θ pour θ petit (en radian)."),
    "intro_dit": (f"نقراو l'énoncé. واحد le laser ضاعت ليه l'étiquette: ما عارفينش la longueur d'onde ديالو lambda. "
                  f"كنضويو بيه sur cinq fentes، la largeur ديال كل وحدة a معروفة. l'écran كيبقى بعيد ب D égale {mots(fr(D, 2))} mètre. "
                  "لكل fente، كنقيسو بالمسطرة la largeur L ديال la tache centrale، وكاين الجدول. la courbe كتعطي L en fonction de un sur a. "
                  f"من بعد، بلا ما نبدلو والو، كنحطو واحد la fente ما عارفينش la largeur ديالها، a prime: la tache centrale ديالها فيها "
                  f"L prime égale {mots(fr(L_INC, 1))} millimètres."),
    "figures": [courbe(D, LMES, K_MM2, 40)],
    "donnees": tableau(LMES) + [f"D = {fr(D, 2)} m", f"L' = {fr(L_INC, 1)} mm (fente inconnue a')", "c = 3,00 × 10⁸ m/s",
                                 "Spectre visible : violet 400 nm … bleu … vert (≈ 500 – 560 nm) … jaune … rouge 800 nm"],
    "questions": [
      {"id": "1", "texte": "Montrer que la largeur de la tache centrale s'écrit L = 2λD·(1/a).",
       "texte_dit": "السؤال un: montrer que la largeur ديال la tache centrale هي L égale deux lambda D، fois un sur a.",
       "reponse": phrase("D'après la figure, tan θ = (L/2)/D = L/(2D). θ petit, en radian : tan θ ≈ θ, donc θ = L/(2D). Or θ = λ/a. "
                         "Donc L/(2D) = λ/a, soit L = 2λD/a = 2λD·(1/a)."),
       "clavier": {"aides": ["tan θ = L/(2D)", "tan θ ≈ θ", "θ = λ/a", "L = 2λD·(1/a)"], "pieges": ["tan θ = L/D", "sin θ = λ/a"]},
       "aides": [aide("Dans le triangle fente – centre de la tache – bord de la tache, quels sont le côté opposé et le côté adjacent à θ ?",
                      "فle triangle: la fente، الوسط ديال la tache، والحاشية ديالها. أشنو هو الضلع المقابل ل teta، وأشنو هو المجاور؟"),
                 aide("Quatre lignes : tan θ = L/(2D) ; θ petit donc tan θ ≈ θ ; θ = λ/a ; égaler et isoler L.",
                      "أربعة ديال السطور: tangente teta égale L sur deux D. teta صغيرة، إذن tangente teta تقريبا teta. teta égale lambda sur a. ساوي وخرج L.")],
       "correction": correction([("1 : d'après la figure, tan θ = (L/2)/D = L/(2D)", "tangente teta égale L sur deux D"),
                                 ("θ petit (en radian) : tan θ ≈ θ, donc θ = L/(2D)", "teta صغيرة"),
                                 ("or θ = λ/a", "or teta égale lambda sur a"),
                                 ("donc L/(2D) = λ/a, soit L = 2λD·(1/a)", "L égale deux lambda D، fois un sur a")],
                                "السؤال un. d'après la figure، tangente teta égale L sur deux D. teta صغيرة en radian، إذن tangente teta تقريبا teta، "
                                "و teta égale L sur deux D. or teta égale lambda sur a. donc L sur deux D égale lambda sur a، "
                                "و L égale deux lambda D، fois un sur a."),
       "explication": "ex_l1", "facile": "fa_l1"},
      {"id": "2", "texte": "Justifier que la courbe est en accord avec cette expression, puis déterminer son coefficient directeur k, en m².",
       "texte_dit": "السؤال deux: justifier باللي la courbe متفقة مع هاد l'expression، ومن بعد حدد le coefficient directeur k، en mètre carré.",
       "reponse": valeur("k", K, "m²", f"k = ΔL/Δ(1/a) = ({Y_LU} mm)/({X_LU} mm⁻¹) = {s_k} mm² = {s_k} × 10⁻⁶ m²"),
       "clavier": {"aides": ["droite passant par l'origine", "k = ΔL/Δ(1/a)", "1 mm² = 10⁻⁶ m²"],
                   "pieges": ["1 mm² = 10⁻³ m²", "k = Δ(1/a)/ΔL"]},
       "aides": [aide("La courbe est une droite qui passe par l'origine : quelle forme a la fonction ? Choisissez un point de la droite, loin de l'origine.",
                      "la courbe خط مستقيم كيدوز من l'origine: أشنو هو الشكل ديال la fonction؟ اختار نقطة فوق الخط، بعيدة على l'origine."),
                 aide("k = ΔL/Δ(1/a) avec les unités des axes : mm divisé par mm⁻¹ donne des mm² ; puis 1 mm² = 10⁻⁶ m².",
                      "k égale delta L sur delta un sur a، بالوحدات ديال les axes: millimètre sur millimètre puissance moins un كتعطي millimètre carré. et un millimètre carré égale dix puissance moins six mètre carré.")],
       "correction": correction([("2 : droite passant par l'origine : L = k·(1/a), forme de L = 2λD·(1/a)", "fonction linéaire"),
                                 (f"point de la droite : (1/a = {X_LU} mm⁻¹ ; L = {Y_LU} mm)", "كناخدو النقطة"),
                                 (f"k = {Y_LU}/{X_LU} = {s_k} mm² = {s_k} × 10⁻⁶ m²", f"k égale {mots(s_k)} fois dix puissance moins six mètre carré"),
                                 ("on lit k sur la droite moyenne, pas sur un seul point mesuré", "la droite moyenne")],
                                f"السؤال deux. la courbe خط مستقيم كيدوز من l'origine: fonction linéaire، L égale k fois un sur a، بحال l'expression. "
                                f"كناخدو النقطة ديال الخط: un sur a égale {mots(X_LU)} millimètres puissance moins un، و L égale {mots(Y_LU)} millimètres. "
                                f"k égale {mots(Y_LU)} sur {mots(X_LU)}، k égale {mots(s_k)} millimètre carré، "
                                f"يعني k égale {mots(s_k)} fois dix puissance moins six mètre carré. وكنقراو على la droite moyenne، "
                                "حيت كل نقطة فيها شوية ديال الغلط ديال القياس."),
       "explication": "ex_l2", "facile": "fa_l2"},
      {"id": "3", "texte": "En déduire la longueur d'onde λ du laser, en nm.",
       "texte_dit": "السؤال trois: استنتج la longueur d'onde lambda ديال le laser، en nanomètre.",
       "reponse": valeur("λ", round(LAM_NM, 1), "nm", f"k = 2λD donc λ = k/(2D) = {s_k}×10⁻⁶/(2 × {fr(D, 2)}) ≈ {sci(LAM)} m = {s_lam} nm"),
       "clavier": {"aides": ["k = 2λD", "λ = k/(2D)", "1 m = 10⁹ nm"], "pieges": ["λ = k", "λ = k/D", "λ = 2kD"]},
       "aides": [aide("Comparez L = k·(1/a) (la courbe) et L = 2λD·(1/a) (la théorie) : que vaut k ?",
                      "قارن L égale k fois un sur a، مع L égale deux lambda D fois un sur a. شحال كيساوي k؟"),
                 aide("k = 2λD donc λ = k/(2D), k en m² et D en m ; puis passer en nm.",
                      "k égale deux lambda D، إذن lambda égale k sur deux D. k en mètre carré و D en mètre، ومن بعد حول en nanomètre.")],
       "correction": correction([("3 : par identification, k = 2λD", "k égale deux lambda D"),
                                 (f"λ = k/(2D) = {s_k}×10⁻⁶/(2 × {fr(D, 2)})", "lambda égale k sur deux D"),
                                 (f"λ ≈ {sci(LAM)} m = {s_lam} nm", f"lambda égale {mots(s_lam)} nanomètres")],
                                f"السؤال trois. par identification، k égale deux lambda D. إذن lambda égale k sur deux D. "
                                f"l'application numérique: {mots(s_k)} fois dix puissance moins six، sur deux fois {mots(fr(D, 2))}. "
                                f"lambda égale {msci(LAM)} mètre، et lambda égale {mots(s_lam)} nanomètres."),
       "explication": "ex_l3", "facile": "fa_l3"},
      {"id": "4", "texte": "Calculer la fréquence ν de la radiation, puis donner la couleur du laser.",
       "texte_dit": "السؤال quatre: حسب la fréquence nu ديال la radiation، ومن بعد عطي اللون ديال le laser.",
       "reponse": valeur("ν", round(NU, -11), "Hz", f"ν = c/λ = 3,00×10⁸/({sci(LAM)}) ≈ {s_nu} Hz"),
       "clavier": {"aides": ["ν = c/λ", "Hz", "λ en m"], "pieges": ["ν = λ/c", "λ en nm dans le calcul"]},
       "aides": [aide("La fréquence se déduit de λ et de c ; attention, λ doit être en mètre.", "la fréquence كتخرج من lambda و c. رد البال: lambda en mètre."),
                 aide("ν = c/λ ; pour la couleur, placez λ dans le spectre visible donné.", "nu égale c sur lambda. وللون، حط lambda فوق le spectre visible.")],
       "correction": correction([("4 : ν = c/λ", "nu égale c sur lambda"),
                                 (f"ν = 3,00×10⁸/({sci(LAM)}) ≈ {s_nu} Hz", f"nu égale {msci(NU)} hertz"),
                                 (f"λ ≈ {s_lam} nm, entre 500 et 560 nm : laser vert", "laser vert")],
                                f"السؤال quatre. nu égale c sur lambda. l'application numérique: trois fois dix puissance huit، sur {msci(LAM)}. "
                                f"nu égale {msci(NU)} hertz. و lambda égale {mots(s_lam)} nanomètres، فالمنطقة ديال le vert: c'est un laser vert."),
       "explication": "ex_l4", "facile": "fa_l4"},
      {"id": "5", "texte": "Déterminer la largeur a' de la fente inconnue, en mm, en utilisant la droite.",
       "texte_dit": "السؤال cinq: حدد la largeur a prime ديال la fente المجهولة، en millimètre، بالخط.",
       "reponse": valeur("a'", A_INC, "mm", f"L' = k·(1/a') donc 1/a' = L'/k = {fr(L_INC, 1)}/{s_k} = {fr(INV_A, 2)} mm⁻¹, a' = 1/{fr(INV_A, 2)} = {s_a} mm"),
       "clavier": {"aides": ["1/a = L/k", "mm⁻¹", "a = 1/(1/a)"], "pieges": ["a' = L'/k", "a' = k·L'"]},
       "aides": [aide("Même laser, même D : le point de cette fente est sur la même droite. Que vaut alors 1/a' ?",
                      "نفس le laser ونفس D: النقطة ديال هاد la fente فوق نفس الخط. combien vaut un sur a prime؟"),
                 aide("1/a' = L'/k avec L' en mm et k en mm², puis prendre l'inverse : l'axe est gradué en 1/a, pas en a.",
                      "un sur a prime égale L prime sur k، L prime en millimètre و k en millimètre carré. من بعد خود l'inverse: l'axe gradué en un sur a، ماشي a.")],
       "correction": correction([("5 : même droite : L' = k·(1/a')", "L prime égale k fois un sur a prime"),
                                 (f"1/a' = L'/k = {fr(L_INC, 1)}/{s_k} = {fr(INV_A, 2)} mm⁻¹", "un sur a prime égale"),
                                 (f"a' = 1/{fr(INV_A, 2)} = {s_a} mm", f"a prime égale {mots(s_a)} millimètre")],
                                f"السؤال cinq. نفس الخط: L prime égale k fois un sur a prime. donc un sur a prime égale L prime sur k، "
                                f"l'application numérique: {mots(fr(L_INC, 1))} sur {mots(s_k)}: un sur a prime égale {mots(fr(INV_A, 2))} millimètres puissance moins un. "
                                f"وخود l'inverse: a prime égale {mots(s_a)} millimètre."),
       "explication": "ex_l5", "facile": "fa_l5"},
      {"id": "6", "texte": (f"Pour la fente la plus fine (a = {fr(A[0], 2)} mm), calculer l'écart angulaire θ. Vérifier à la calculatrice "
                            "(mode radian) que tan θ ≈ θ. L'approximation utilisée en 1 est-elle justifiée pour toutes les fentes ? Justifier."),
       "texte_dit": (f"السؤال six: ل la fente الرقيقة بزاف، a égale {mots(fr(A[0], 2))} millimètre، حسب l'écart angulaire teta. "
                     "تأكد بla calculatrice en mode radian باللي tangente teta تقريبا teta. واش l'approximation ديال السؤال un صحيحة لكاع les fentes؟ justifier."),
       "reponse": valeur("θ", round(TH, 6), "rad", f"θ = λ/a = {sci(LAM)}/({fr(A[0], 2)}×10⁻³) ≈ {s_th} rad"),
       "clavier": {"aides": ["θ = λ/a", "rad", "mode radian", "tan θ ≈ θ"], "pieges": ["mode degré", "θ = a/λ"]},
       "aides": [aide("θ est le plus grand pour la fente la plus fine : c'est le cas le plus défavorable pour l'approximation.",
                      "teta كتكون كبيرة بزاف مع la fente الرقيقة: هادي هي الحالة الصعيبة ل l'approximation."),
                 aide("θ = λ/a en mètre ; tapez tan(θ) en mode radian et comparez les deux nombres.",
                      "teta égale lambda sur a، كلشي en mètre. حسب tangente teta en mode radian، وقارن les deux nombres.")],
       "correction": correction([("6 : θ = λ/a", "teta égale lambda sur a"),
                                 (f"θ = {sci(LAM)}/({fr(A[0], 2)}×10⁻³) ≈ {s_th} rad", f"teta égale {msci(TH)} radian"),
                                 (f"θ ≈ {TH:.7f} rad ; tan θ ≈ {TAN:.7f} : écart relatif ≈ {ECART:.3f} %".replace(".", ","), "l'écart relatif"),
                                 ("les autres fentes sont plus larges : θ plus petit, approximation encore meilleure ; elle est justifiée", "justifiée")],
                                f"السؤال six. teta égale lambda sur a. l'application numérique: {msci(LAM)}، sur {mots(fr(A[0], 2))} fois dix puissance moins trois. "
                                f"teta égale {msci(TH)} radian. en mode radian، tangente teta تقريبا نفس القيمة: l'écart relatif inférieur à zéro virgule zéro un pour cent. "
                                "les autres fentes أوسع، إذن teta أصغر، و l'approximation أحسن. إذن l'approximation justifiée لكاع les fentes."),
       "explication": "ex_l6", "facile": "fa_l6"},
    ]
  },
}

# ---------------------------------------------------------------- explication animée
m1 = ("هادي هي la figure ديال الامتحان. السطر اللول: d'après la figure، tangente teta égale L sur deux D. "
      "السطر الثاني: teta صغيرة، إذن tangente teta تقريبا teta، و teta égale L sur deux D. السطر الثالث: or teta égale lambda sur a. "
      "السطر الرابع: donc L sur deux D égale lambda sur a، و L égale deux lambda D sur a. "
      "دابا كنكتبوها بحال la courbe: L égale deux lambda D، fois un sur a. deux lambda D ثابت، إذن L fonction linéaire de un sur a.")
m2 = ("فla simulation، le laser و l'écran ثابتين، وكنبدلو la fente. كل fente كتعطي نقطة. "
      "les points على خط مستقيم كيدوز من l'origine: fonction linéaire. باش نحسبو le coefficient directeur، كناخدو l'origine وواحد النقطة فوق الخط. "
      "شوف الوحدات: l'axe اللي التحت en millimètre puissance moins un، و l'axe اللي على اليسار en millimètre. "
      "هنا، k égale vingt-six millimètres sur dix، k égale deux virgule six millimètres carrés. "
      f"فالتمرين، كناخدو النقطة ديال الخط: un sur a égale {mots(X_LU)}، و L égale {mots(Y_LU)} millimètres. "
      f"k égale {mots(Y_LU)} sur {mots(X_LU)}، k égale {mots(s_k)} millimètre carré، يعني k égale {mots(s_k)} fois dix puissance moins six mètre carré. "
      "وعلاش الخط، ماشي نقطة وحدة؟ كل قياس فيه شوية ديال الغلط، والخط كيعطي la moyenne.")
m3 = ("la courbe كتقول: L égale k fois un sur a. والدرس كيقول: L égale deux lambda D fois un sur a. نفس الشكل، إذن k égale deux lambda D. "
      "كنخرجو lambda: lambda égale k sur deux D. فla simulation، lambda égale six cent cinquante nanomètres. "
      f"فالتمرين، lambda égale {mots(s_k)} fois dix puissance moins six، sur deux fois {mots(fr(D, 2))}. "
      f"lambda égale {msci(LAM)} mètre، et lambda égale {mots(s_lam)} nanomètres.")
m4 = (f"lambda égale {mots(s_lam)} nanomètres. كنحطوها فوق le spectre: entre quatre cents et huit cents nanomètres، إذن visible. "
      "وهي فالمنطقة ديال le vert. la fréquence: nu égale c sur lambda. "
      f"nu égale trois fois dix puissance huit، sur {msci(LAM)}. nu égale {msci(NU)} hertz.")
m5 = ("دابا العكس: عندنا L، وكنقلبو على a. نفس le laser ونفس D، إذن النقطة ديال la fente الجديدة فوق نفس الخط. "
      f"فالتمرين، L prime égale {mots(fr(L_INC, 1))} millimètres. L égale k fois un sur a، donc un sur a égale L sur k. "
      f"un sur a prime égale {mots(fr(L_INC, 1))} sur {mots(s_k)}، et un sur a prime égale {mots(fr(INV_A, 2))} millimètres puissance moins un. "
      f"فla simulation، النقطة المقروءة فوق الخط، فهاد l'abscisse. رد البال: l'axe gradué en un sur a. donc a prime égale un sur {mots(fr(INV_A, 2))}: "
      f"a prime égale {mots(s_a)} millimètre.")
m6 = ("فla simulation، teta égale six virgule cinq fois dix puissance moins trois radian، و la calculatrice en mode radian كتعطي tangente teta بنفس القيمة. "
      f"فالتمرين، la fente الرقيقة: a égale {mots(fr(A[0], 2))} millimètre. teta égale lambda sur a: {msci(LAM)}، sur {msci(A[0] * 1e-3, 1)}. "
      f"teta égale {msci(TH)} radian. tangente teta، en mode radian، تقريبا نفس القيمة: l'écart relatif inférieur à zéro virgule zéro un pour cent. "
      "les autres fentes أوسع، إذن teta أصغر، و l'approximation أحسن.")
CRB = SIM + "courbe.html"
EX["explication"] = {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
  diapo_sim("ex_l1", "Question 1 : les quatre lignes, puis la forme de la courbe", "L = 2λD·(1/a) : fonction linéaire de 1/a.",
            SIM + "figures.html?fig=fig_montage_examen", "Le schéma de l'examen et les quatre lignes", m1,
            [("L = 2λD·(1/a)", "L égale deux lambda D، fois un sur a")],
            [dict(mot="هادي هي la figure", commande="play_until", parametres={"moment": "trace"}),
             dict(mot="السطر اللول: d'après", commande="play_until", parametres={"moment": "ligne1"}),
             dict(mot="السطر الثاني: teta", commande="play_until", parametres={"moment": "ligne2"}),
             dict(mot="السطر الثالث: or", commande="play_until", parametres={"moment": "ligne3"}),
             dict(mot="السطر الرابع: donc", commande="play_until", parametres={"moment": "ligne4"}),
             dict(mot="L égale deux lambda D، fois un sur a", cible="centre:0")]),
  diapo_sim("ex_l2", "Question 2 : la pente, avec ses unités", "k = ΔL/Δ(1/a) en mm², puis en m².", CRB,
            "Une fente, un point ; la droite par l'origine", m2,
            [("Droite par l'origine : L = k·(1/a)", "fonction linéaire. باش"),
             (f"k = {Y_LU}/{X_LU} = {s_k} mm² = {s_k} × 10⁻⁶ m²", f"يعني k égale {mots(s_k)} fois dix puissance moins six mètre carré")],
            [dict(mot="كل fente كتعطي نقطة", commande="play_until", parametres={"moment": "point_4"}),
             dict(mot="les points على خط", commande="play_until", parametres={"moment": "droite"}),
             dict(mot="fonction linéaire. باش", cible="centre:0"),
             dict(mot="كناخدو l'origine", repere="origine"),
             dict(mot="l'axe اللي التحت", repere="axe_x"),
             dict(mot="و l'axe اللي على اليسار", repere="axe_y"),
             dict(mot="هنا، k égale", commande="play_until", parametres={"moment": "pente"}),
             dict(mot=f"يعني k égale {mots(s_k)} fois dix puissance moins six mètre carré", cible="centre:1")]),
  diapo_sim("ex_l3", "Question 3 : identifier k = 2λD", "Même forme : k = 2λD, λ = k/(2D).", CRB + "?depart=droite",
            "La droite et l'identification", m3,
            [("k = 2λD ⇒ λ = k/(2D)", "lambda égale k sur deux D"), (f"λ ≈ {sci(LAM)} m = {s_lam} nm", f"et lambda égale {mots(s_lam)} nanomètres")],
            [dict(mot="la courbe كتقول", commande="play_until", parametres={"moment": "pente"}),
             dict(mot="la courbe كتقول", repere="droite"),
             dict(mot="نفس الشكل، إذن", commande="play_until", parametres={"moment": "identification"}),
             dict(mot="كنخرجو lambda", repere="identification"),
             dict(mot="lambda égale k sur deux D", cible="centre:0"),
             dict(mot=f"et lambda égale {mots(s_lam)} nanomètres", cible="centre:1")]),
  diapo_sim("ex_l4", "Question 4 : la fréquence et la couleur", "ν = c/λ ; λ dans le vert.", SIM + f"spectre.html?lambda_nm={round(LAM_NM)}",
            "La radiation du laser placée sur le spectre", m4,
            [("400 nm < λ < 800 nm : visible, vert", "إذن visible"), (f"ν = c/λ ≈ {s_nu} Hz", f"nu égale {msci(NU)} hertz")],
            [dict(mot="كنحطوها فوق le spectre", commande="play_until", parametres={"moment": "valeur"}),
             dict(mot="كنحطوها فوق le spectre", repere="curseur"),
             dict(mot="إذن visible", cible="centre:0"),
             dict(mot="وهي فالمنطقة ديال le vert", repere="couleur"),
             dict(mot="la fréquence: nu", repere="frequence"),
             dict(mot=f"nu égale {msci(NU)} hertz", cible="centre:1")]),
  diapo_sim("ex_l5", "Question 5 : lire 1/a sur la droite", "1/a' = L'/k, puis a' = 1/(1/a').", CRB,
            "Un point lu sur la droite", m5,
            [("1/a' = L'/k", "donc un sur a égale L sur k"), (f"1/a' = {fr(INV_A, 2)} mm⁻¹ ; a' = {s_a} mm", f"a prime égale {mots(s_a)} millimètre")],
            [dict(mot="دابا العكس", commande="play_until", parametres={"moment": "droite"}),
             dict(mot="donc un sur a égale L sur k", cible="centre:0"),
             dict(mot="فla simulation، النقطة المقروءة", commande="set_parameters", parametres={"x_lu": INV_A}),
             dict(mot="فهاد l'abscisse", repere="point_lu"),
             dict(mot="رد البال: l'axe", repere="axe_x"),
             dict(mot=f"a prime égale {mots(s_a)} millimètre", cible="centre:1")]),
  diapo_sim("ex_l6", "Question 6 : tan θ ≈ θ, même pour la fente la plus fine", "En radian, un petit angle égale sa tangente.",
            SIM + "ecart-angulaire.html", "L'angle θ et sa tangente", m6,
            [(f"θ = λ/a ≈ {s_th} rad", f"teta égale {msci(TH)} radian"), ("tan θ ≈ θ : écart < 0,01 %", "l'écart relatif inférieur")],
            [dict(mot="فla simulation، teta", commande="play_until", parametres={"moment": "petit_angle"}),
             dict(mot="فla simulation، teta", repere="theta"),
             dict(mot=f"teta égale {msci(TH)} radian", cible="centre:0"),
             dict(mot="l'écart relatif inférieur", cible="centre:1")]),
]}]}

# ---------------------------------------------------------------- version facile
EX["facile"] = {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
  vf_facile("fa_l1", "Plus facile : les lignes de la démonstration", "سؤال ساهل: صحيح ولا غالط؟", "Démonstration de L = 2λD/a.", [
              ("D'après la figure, tan θ = L/(2D).", True, "Le côté opposé à θ est L/2, le côté adjacent est D."),
              ("D'après la figure, tan θ = L/D.", False, "θ va du centre au bord de la tache : le côté opposé est L/2, pas L."),
              ("On peut écrire tan θ ≈ θ parce que θ est petit et exprimé en radian.", True, "C'est la condition de l'approximation.")]),
  qcm_facile("fa_l2", "Plus facile : la pente en m²", "نتمرنو على الوحدات. اختار الجواب.",
             f"Sur la droite : 1/a = {X_LU} mm⁻¹ et L = {Y_LU} mm. Le coefficient directeur vaut…",
             [f"k = {fr(X_LU / Y_LU, 2)} mm⁻²", f"k = {s_k} × 10⁻⁶ m²", f"k = {s_k} × 10⁻³ m²"], 1, {
               "1": {"juste": rep(f"برافو! k égale {mots(Y_LU)} sur {mots(X_LU)}، k égale {mots(s_k)} millimètre carré، يعني k égale {mots(s_k)} fois dix puissance moins six mètre carré.",
                                  f"Juste : k = {Y_LU}/{X_LU} = {s_k} mm² = {s_k} × 10⁻⁶ m².")},
               "0": {"1": rep("قلبتي la fraction: le coefficient directeur هو delta L sur delta un sur a. عاود اختار.", "Pente = ΔL/Δ(1/a), pas l'inverse. Réessaie."),
                     "2": rep(f"الجواب هو k égale {mots(s_k)} fois dix puissance moins six mètre carré: L فوق، et un sur a تحت.", f"Réponse : k = ΔL/Δ(1/a) = {s_k} × 10⁻⁶ m².")},
               "2": {"1": rep("الرقم صحيح، ولكن التحويل: un millimètre carré، شحال en mètre carré؟ عاود اختار.", "Le nombre est juste ; revois la conversion des mm² en m². Réessaie."),
                     "2": rep(f"الجواب هو k égale {mots(s_k)} fois dix puissance moins six mètre carré، car un millimètre carré égale dix puissance moins six mètre carré، et un millimètre égale dix puissance moins trois mètre، وكنربعو.", "Réponse : 1 mm² = (10⁻³ m)² = 10⁻⁶ m².")}},
             "Quelle est la valeur du coefficient directeur ?"),
  qcm_facile("fa_l3", "Plus facile : identifier", "سؤال ساهل: اختار la bonne relation.",
             "L = k·(1/a) (courbe) et L = 2λD·(1/a) (théorie). Alors λ =…",
             ["λ = k", "λ = 2kD", "λ = k/(2D)"], 2, {
               "2": {"juste": rep("برافو! k égale deux lambda D، إذن lambda égale k sur deux D.", "Juste : k = 2λD donc λ = k/(2D).")},
               "0": {"1": rep("هادي صحيحة غير فla courbe ديال teta en fonction de un sur a. هنا L فوق. عاود اختار.", "k = λ seulement pour θ = f(1/a). Ici c'est L. Réessaie."),
                     "2": rep("الجواب هو lambda égale k sur deux D: هنا k égale deux lambda D.", "Réponse : λ = k/(2D).")},
               "1": {"1": rep("شوف: k égale deux lambda D. باش نخرجو lambda، كنضربو ولا كنقسمو par deux D؟ عاود اختار.", "Pour isoler λ dans k = 2λD, on divise par 2D. Réessaie."),
                     "2": rep("الجواب هو lambda égale k sur deux D: كنقسمو par deux D.", "Réponse : λ = k/(2D).")}},
             "Quelle relation donne lambda ?"),
  assoc_facile("fa_l4", "Plus facile : longueur d'onde et couleur", "نتمرنو: ربط كل longueur d'onde مع اللون ديالها.",
               "Spectre visible : 400 nm (violet) à 800 nm (rouge).", "Relie chaque longueur d'onde dans le vide à sa couleur.",
               [("1", f"{s_lam} nm"), ("2", "650 nm"), ("3", "420 nm")],
               [("a", "vert"), ("b", "rouge"), ("c", "violet"), ("d", "non visible")],
               {"1": "a", "2": "b", "3": "c"}, {
                 "1-a": (True, "Oui : vers 530 nm, c'est le vert.", "برافو: proche de cinq cent trente nanomètres، هادا le vert."),
                 "1-b": (False, "Le rouge est vers 620 à 800 nm.", "لا، le rouge كيكون proche de huit cents nanomètres."),
                 "1-c": (False, "Le violet est près de 400 nm.", "لا، le violet proche de quatre cents nanomètres."),
                 "1-d": (False, "Entre 400 et 800 nm : visible.", "لا، entre quatre cents et huit cents nanomètres كتبان."),
                 "2-a": (False, "650 nm est trop grand pour le vert.", "لا، lambda égale six cent cinquante، كبيرة على le vert."),
                 "2-b": (True, "Oui : 650 nm, rouge.", "برافو: six cent cinquante nanomètres، حمر."),
                 "2-c": (False, "Le violet est à l'autre bout, près de 400 nm.", "لا، le violet فالجهة الأخرى."),
                 "2-d": (False, "650 nm est dans le visible.", "لا، lambda égale six cent cinquante nanomètres، كتبان."),
                 "3-a": (False, "420 nm est trop petit pour le vert.", "لا، lambda égale quatre cent vingt، صغيرة على le vert."),
                 "3-b": (False, "Le rouge est vers les grandes longueurs d'onde.", "لا، le rouge عندو longueur d'onde كبيرة."),
                 "3-c": (True, "Oui : près de 400 nm, violet.", "برافو: proche de quatre cents nanomètres، violet."),
                 "3-d": (False, "420 nm est encore visible (au-dessus de 400 nm).", "لا، lambda égale quatre cent vingt nanomètres، باقة كتبان.")},
               ("Du violet (400 nm) au rouge (800 nm) en passant par le vert ; « non visible » est l'intrus.",
                "من le violet حتى le rouge، والوسط le vert. non visible ما عندها حتى زوج.")),
  qcm_facile("fa_l5", "Plus facile : lire a sur l'axe 1/a", "سؤال ساهل. اختار الجواب.",
             f"Sur la droite, la fente inconnue donne 1/a' = {fr(INV_A, 2)} mm⁻¹. Sa largeur vaut…",
             [f"a' = {s_a} mm", f"a' = {fr(INV_A, 2)} mm", f"a' = {fr(L_INC * K_MM2, 1)} mm"], 0, {
               "0": {"juste": rep(f"برافو! a prime égale un sur {mots(fr(INV_A, 2))}، a prime égale {mots(s_a)} millimètre.", f"Juste : a' = 1/{fr(INV_A, 2)} = {s_a} mm.")},
               "1": {"1": rep("رد البال: l'axe gradué en un sur a، ماشي a. خاصك l'inverse. عاود اختار.", "L'axe est gradué en 1/a : il faut prendre l'inverse. Réessaie."),
                     "2": rep(f"الجواب هو a prime égale {mots(s_a)} millimètre: l'inverse de {mots(fr(INV_A, 2))}.", f"Réponse : a' = 1/{fr(INV_A, 2)} = {s_a} mm.")},
               "2": {"1": rep("ضربتي L prime فk. un sur a égale L sur k، ماشي L fois k. عاود اختار.", "1/a = L/k, pas L·k. Réessaie."),
                     "2": rep(f"الجواب هو a prime égale {mots(s_a)} millimètre.", f"Réponse : a' = {s_a} mm.")}},
             "Quelle est la largeur de la fente inconnue ?"),
  vf_facile("fa_l6", "Plus facile : l'approximation", "آخر سؤال ساهل: صحيح ولا غالط؟", "On vérifie tan θ ≈ θ à la calculatrice.", [
              ("La calculatrice doit être en mode radian.", True, "θ = λ/a est en radian ; en degré, la comparaison n'a pas de sens."),
              ("La fente la plus fine donne le plus grand θ : c'est le cas le plus difficile pour l'approximation.", True, "θ = λ/a : a petite, θ grand."),
              ("tan θ ≈ θ reste vraie même pour θ = 1 rad.", False, "tan 1 ≈ 1,56 : l'approximation n'est valable que pour les petits angles.")]),
]}]}

# ---------------------------------------------------------------- exercice semblable
b_D, b_lam = 2.00, 650e-9
b_L = [52.2, 32.4, 26.1, 16.2, 13.0]
for a, L in zip(A, b_L):
    assert abs(L - 2 * b_lam * b_D / (a * 1e-3) * 1e3) / L < 0.012
b_x, b_y = 20, 52
b_k = b_y / b_x; b_lam_c = b_k * 1e-6 / (2 * b_D); b_nu = C / b_lam_c
b_Linc = 18.2; b_inv = b_Linc / b_k; b_a = 1 / b_inv; b_th = b_lam_c / (A[0] * 1e-3)
EX["similaire"] = {"id": "phys_ex_ch3_laser_7_b", "titre": "Même exercice, autres données", "enonce": {
  "intro": (f"Même méthode avec un autre laser inconnu ; l'écran est à D = {fr(b_D, 2)} m des fentes. Les mesures sont dans le tableau et "
            f"la courbe L = f(1/a). Une fente inconnue a' donne ensuite L' = {fr(b_Linc, 1)} mm. c = 3,00 × 10⁸ m/s ; tan θ ≈ θ (θ petit, en radian)."),
  "intro_dit": (f"نفس التمرين، بقيم أخرى. laser آخر، و D égale {mots(fr(b_D, 2))} mètres. la fente المجهولة كتعطي L prime égale {mots(fr(b_Linc, 1))} millimètres."),
  "figures": [courbe(b_D, b_L, b_k, 60)],
  "donnees": tableau(b_L) + [f"D = {fr(b_D, 2)} m", f"L' = {fr(b_Linc, 1)} mm", "c = 3,00 × 10⁸ m/s"],
  "questions": [
    {"id": "1", "texte": "Montrer que L = 2λD·(1/a).",
     "reponse": phrase("tan θ = L/(2D) ; θ petit : tan θ ≈ θ ; θ = λ/a ; donc L = 2λD·(1/a)."),
     "clavier": {"aides": ["tan θ = L/(2D)", "θ = λ/a"], "pieges": ["tan θ = L/D"]},
     "correction": correction([("1 : tan θ = L/(2D) ≈ θ et θ = λ/a", "tangente teta égale L sur deux D"), ("L = 2λD·(1/a)", "L égale deux lambda D")],
                              "السؤال un. tangente teta égale L sur deux D، تقريبا teta، و teta égale lambda sur a. إذن L égale deux lambda D، fois un sur a.")},
    {"id": "2", "texte": "Déterminer le coefficient directeur k de la droite, en m².",
     "reponse": valeur("k", b_k * 1e-6, "m²", f"k = ({b_y} mm)/({b_x} mm⁻¹) = {fr(b_k, 2)} mm² = {fr(b_k, 2)} × 10⁻⁶ m²"),
     "clavier": {"aides": ["k = ΔL/Δ(1/a)", "1 mm² = 10⁻⁶ m²"], "pieges": ["10⁻³ m²"]},
     "correction": correction([("2 : k = ΔL/Δ(1/a)", "k égale delta L"), (f"k = {fr(b_k, 2)} × 10⁻⁶ m²", f"k égale {mots(fr(b_k, 2))} fois dix puissance moins six")],
                              f"السؤال deux. k égale delta L sur delta un sur a. k égale {mots(fr(b_k, 2))} fois dix puissance moins six mètre carré.")},
    {"id": "3", "texte": "En déduire λ en nm.",
     "reponse": valeur("λ", round(b_lam_c * 1e9, 1), "nm", f"λ = k/(2D) = {fr(b_k, 2)}×10⁻⁶/(2 × {fr(b_D, 2)}) ≈ {sci(b_lam_c)} m = {fr(b_lam_c * 1e9, 0)} nm"),
     "clavier": {"aides": ["λ = k/(2D)"], "pieges": ["λ = k"]},
     "correction": correction([("3 : k = 2λD ⇒ λ = k/(2D)", "lambda égale k sur deux D"), (f"λ ≈ {fr(b_lam_c * 1e9, 0)} nm", f"lambda égale {mots(fr(b_lam_c * 1e9, 0))} nanomètres")],
                              f"السؤال trois. lambda égale k sur deux D. lambda égale {mots(fr(b_lam_c * 1e9, 0))} nanomètres.")},
    {"id": "4", "texte": "Calculer ν et donner la couleur du laser.",
     "reponse": valeur("ν", round(b_nu, -11), "Hz", f"ν = c/λ = 3,00×10⁸/({sci(b_lam_c)}) ≈ {sci(b_nu)} Hz"),
     "clavier": {"aides": ["ν = c/λ"], "pieges": ["λ en nm"]},
     "correction": correction([("4 : ν = c/λ", "nu égale c sur lambda"), (f"ν ≈ {sci(b_nu)} Hz ; laser rouge", f"nu égale {msci(b_nu)} hertz")],
                              f"السؤال quatre. nu égale c sur lambda. nu égale {msci(b_nu)} hertz: c'est un laser rouge.")},
    {"id": "5", "texte": "Déterminer a' en mm à l'aide de la droite.",
     "reponse": valeur("a'", round(b_a, 4), "mm", f"1/a' = L'/k = {fr(b_Linc, 1)}/{fr(b_k, 2)} = {fr(b_inv, 2)} mm⁻¹, a' = 1/{fr(b_inv, 2)} ≈ {fr(b_a, 3)} mm"),
     "clavier": {"aides": ["1/a = L/k"], "pieges": ["a' = L'/k"]},
     "correction": correction([("5 : 1/a' = L'/k", "un sur a prime égale L prime sur k"), (f"a' ≈ {fr(b_a, 3)} mm", f"a prime égale {mots(fr(b_a, 3))} millimètre")],
                              f"السؤال cinq. un sur a prime égale L prime sur k، donc un sur a prime égale {mots(fr(b_inv, 2))}. a prime égale {mots(fr(b_a, 3))} millimètre.")},
    {"id": "6", "texte": f"Pour a = {fr(A[0], 2)} mm, calculer θ et juger l'approximation tan θ ≈ θ.",
     "reponse": valeur("θ", round(b_th, 6), "rad", f"θ = λ/a = {sci(b_lam_c)}/({fr(A[0], 2)}×10⁻³) ≈ {sci(b_th)} rad"),
     "clavier": {"aides": ["θ = λ/a", "mode radian"], "pieges": ["mode degré"]},
     "correction": correction([("6 : θ = λ/a", "teta égale lambda sur a"), (f"θ ≈ {sci(b_th)} rad ; tan θ ≈ θ (écart < 0,01 %) : justifiée", f"teta égale {msci(b_th)} radian")],
                              f"السؤال six. teta égale lambda sur a. teta égale {msci(b_th)} radian. tangente teta تقريبا teta: l'approximation justifiée.")},
  ]}}

ecrire(EX)
