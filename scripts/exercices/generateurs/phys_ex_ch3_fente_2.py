# Exercice facile de physique, ch. 3 (propagation d'une onde lumineuse) : un laser éclaire une fente ;
# θ = λ/a, puis L = 2D·θ (tan θ ≈ θ), puis l'effet d'une fente plus fine.
#
# Sources comparées (skill exercices § 2) :
# - exploration backend/data/curriculum/exploration/ondes_lumineuses.json : cas_types « calcul_direct », « etablir_L »,
#   « variation » ; pieges (côté opposé L/2 et non L ; longueurs laissées en nm et mm ; « L augmente quand a augmente » ;
#   tan θ ≈ θ en radian) ; erreurs_examen (convertir tout en mètre avant la ligne de calcul ; une phrase de conclusion
#   après une variation) ; valeurs_reperes (laser rouge 630-650 nm, a de 0,05 à 0,5 mm, θ de 10⁻³ à 10⁻² rad).
# - vidéos des 10 profs : Laksabi et Driss (θ du centre au bord, triangle, tan θ ≈ θ), Boujaada (variation de a).
# - nationaux comparés : 2017 R (fil d = 0,1 mm, D = 3,5 m, L = 56 mm → λ, puis violet), 2019 R (analyse dimensionnelle,
#   vrai/faux sur les facteurs, comparer L_R et L_B), 2023 R (a = 2λD/L puis rapport), 2025 R (L = 2λD/a établie, indice).
#   Le nôtre : λ, a et D donnés, on calcule θ puis L, puis l'effet d'une fente deux fois plus fine : situation et
#   données différentes, pas de fil, pas de seconde source, pas d'analyse dimensionnelle.
# - séries en ligne : recherche web faite (talamidi série corrigée 1, moutamadris séries 1 et 2 BIOF « Propagation des
#   ondes lumineuses ») : seuls les extraits des moteurs étaient lisibles (PDF bloqués par le réseau de la session) ;
#   situation classique « laser, fente, écran, L = 2λD/a » confirmée. Rien n'est copié.
# - simulation : ecart-angulaire.html accepte set_parameters {D_m 1–3, a_mm 0,05–0,40, lambda_nm 400–800 pas 10} :
#   les valeurs de l'exercice (640 nm, 0,16 mm, 2,5 m) y sont réglées, la simulation montre donc les mêmes θ et L.
import sys, os, math, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *
# ---------- nombres dits en mots français (calculés, jamais tapés à la main) ----------
_U = ["zéro", "un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit", "neuf", "dix", "onze", "douze", "treize",
      "quatorze", "quinze", "seize"]
_D = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def entier(n):
    """Un entier (0 ≤ n < 10⁶) en mots français."""
    if n < 17:
        return _U[n]
    if n < 20:
        return "dix-" + _U[n - 10]
    if n < 70:
        d, u = divmod(n, 10)
        return _D[d] + ("" if u == 0 else " et un" if u == 1 else "-" + _U[u])
    if n < 80:
        return "soixante" + (" et onze" if n == 71 else "-" + entier(n - 60))
    if n < 100:
        return "quatre-vingts" if n == 80 else "quatre-vingt-" + entier(n - 80)
    if n < 1000:
        c, r = divmod(n, 100)
        tete = "cent" if c == 1 else _U[c] + (" cents" if r == 0 else " cent")
        return tete if r == 0 else tete + " " + entier(r)
    m, r = divmod(n, 1000)
    tete = "mille" if m == 1 else entier(m) + " mille"
    return tete if r == 0 else tete + " " + entier(r)


def dit(x, decimales=2):
    """5.49 -> « cinq virgule quarante-neuf » ; 0.08 -> « zéro virgule zéro huit » (même arrondi que fr())."""
    s = fr(x, decimales).replace("−", "-")
    neg = s.startswith("-")
    s = s.lstrip("-")
    e, _, f = s.partition(",")
    out = entier(int(e))
    if f:
        if f.startswith("0") or len(f) > 2:
            out += " virgule " + " ".join(_U[int(c)] for c in f)
        else:
            out += " virgule " + entier(int(f))
    return ("moins " if neg else "") + out


def sci_dit(x, chiffres=3):
    """5.4945e14 -> « cinq virgule quarante-neuf fois dix puissance quatorze » (comme sci())."""
    e = math.floor(math.log10(abs(x)))
    m = round(x / 10 ** e, chiffres - 1)
    if abs(m) >= 10:
        m /= 10; e += 1
    t = dit(m, chiffres - 1)
    if e == 0:
        return t
    return t + " fois dix puissance " + ("moins " + entier(-e) if e < 0 else entier(e))


_NOMBRES = set(_U[1:]) | {"zéro", "vingt", "trente", "quarante", "cinquante", "soixante", "cent", "cents", "mille",
                           "dix-sept", "dix-huit", "dix-neuf", "quatre-vingts"}
_AR = re.compile(r"[؀-ۿ]")


def controle_voix(EX):
    """Aucun mot arabe juste avant un nombre français ; aucun chiffre dans une voix."""
    pb = []
    champs = {"mixed", "dit", "parole", "intro_dit", "texte_dit", "enonce_dit", "mot"}

    def walk(o, k=""):
        if isinstance(o, dict):
            for kk, v in o.items():
                walk(v, kk)
        elif isinstance(o, list):
            for v in o:
                walk(v, k)
        elif isinstance(o, str) and k in champs:
            if re.search(r"\d", o):
                pb.append(("chiffre", o[:80]))
            toks = o.split()
            for a, b in zip(toks, toks[1:]):
                b0 = b.strip("،,.:;!?()«»").split("-")[0]
                if _AR.search(a.strip("،؟:.")) and (b0 in _NOMBRES or b.strip("،,.:;!?") in _NOMBRES):
                    pb.append(("arabe+nombre", a + " " + b, o[:60]))
    walk(EX)
    if pb:
        raise AssertionError("\n".join(map(str, pb)))


SIM = "/media/simulations/physics/ondes-lumineuses-tableau/"


def montage():
    """Le montage vu de dessus, angle exagéré : laser, fente (a), éventail, écran à D, tache de largeur L, θ."""
    return {"type": "schema", "titre": "Le montage vu de dessus (angle exagéré)", "cadre": {"l": 10.4, "h": 5},
            "legende": "θ va du centre de la tache centrale à son bord ; L est la largeur de la tache centrale.",
            "elements": [
                {"f": "rect", "de": [0.2, 2.2], "a": [1.4, 2.8], "couleur": "blanc"},
                {"f": "texte", "at": [0.8, 3.15], "t": "laser", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
                {"f": "ligne", "pts": [[1.4, 2.5], [3, 2.5]], "couleur": "rouge", "epais": True},
                {"f": "ligne", "pts": [[3, 0.9], [3, 2.38]], "couleur": "blanc", "epais": True},
                {"f": "ligne", "pts": [[3, 2.62], [3, 4.1]], "couleur": "blanc", "epais": True},
                {"f": "texte", "at": [3, 4.45], "t": "fente", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
                {"f": "texte", "at": [2.75, 2.75], "t": "a", "couleur": "cyan", "ancre": "droite"},
                {"f": "ligne", "pts": [[3, 2.5], [9, 4.0]], "couleur": "rouge"},
                {"f": "ligne", "pts": [[3, 2.5], [9, 1.0]], "couleur": "rouge"},
                {"f": "ligne", "pts": [[3, 2.5], [9, 2.5]], "couleur": "faible", "trait": "pointille"},
                {"f": "arc", "c": [3, 2.5], "r": 1.6, "de": 0, "a": 14.04, "couleur": "orange"},
                {"f": "texte", "at": [4.95, 2.85], "t": "θ", "couleur": "orange", "ancre": "centre"},
                {"f": "ligne", "pts": [[9, 0.5], [9, 4.5]], "couleur": "blanc", "epais": True},
                {"f": "texte", "at": [9, 4.8], "t": "écran", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
                {"f": "cote", "de": [9.5, 1.0], "a": [9.5, 4.0], "t": "L", "couleur": "jaune", "pos": "e"},
                {"f": "cote", "de": [3, 0.35], "a": [9, 0.35], "t": "D", "couleur": "cyan", "pos": "n"}]}


def cm(x_m):
    return x_m * 100


def calc(lam_nm, a_mm, D, a2_mm):
    lam, a, a2 = lam_nm * 1e-9, a_mm * 1e-3, a2_mm * 1e-3
    th = lam / a
    L = 2 * D * th
    L2 = 2 * lam * D / a2
    return lam, a, a2, th, L, L2


def questions_calc(lam_nm, a_mm, D, a2_mm):
    """reponse, clavier, correction des 3 questions (exercice et semblable)."""
    lam, a, a2, th, L, L2 = calc(lam_nm, a_mm, D, a2_mm)
    q1 = {"reponse": valeur("θ", th, "rad", f"θ = λ/a = {sci(lam)}/({sci(a)}) = {sci(th)} rad"),
          "clavier": {"aides": ["θ = λ/a", "1 nm = 10⁻⁹ m", "1 mm = 10⁻³ m", "A.N. :", "rad"],
                      "pieges": ["θ = a/λ", "λ en nm et a en mm", "degré"]},
          "correction": correction([
              (f"1 : λ = {lam_nm} nm = {sci(lam)} m ; a = {fr(a_mm)} mm = {sci(a)} m", "كنحولو lambda و a en mètre"),
              (f"θ = λ/a = {sci(lam)}/({sci(a)})", "teta égale lambda sur a"),
              (f"θ = {sci(th)} rad", "teta égale " + sci_dit(th) + " radian")],
              f"Question un. كنحولو lambda و a en mètre: lambda égale {sci_dit(lam)} mètre، و a égale {sci_dit(a)} mètre. "
              f"teta égale lambda sur a، soit {sci_dit(lam)}، sur {sci_dit(a)}. teta égale {sci_dit(th)} radian.")}
    q2 = {"reponse": valeur("L", round(cm(L), 3), "cm", f"tan θ = L/(2D) ≈ θ, donc L = 2D·θ = 2 × {fr(D)} × {sci(th)} = {sci(L)} m = {fr(cm(L))} cm"),
          "clavier": {"aides": ["tan θ = L/(2D)", "tan θ ≈ θ", "L = 2D·θ", "A.N. :", "cm"],
                      "pieges": ["tan θ = L/D", "L = D·θ", "L = 2θ/D"]},
          "correction": correction([
              ("2 : tan θ = (L/2)/D = L/(2D)", "tangente teta égale L sur deux D"),
              ("θ petit (en radian) : tan θ ≈ θ, donc L = 2D·θ", "إذن L égale deux D fois teta"),
              (f"L = 2 × {fr(D)} × {sci(th)} = {sci(L)} m = {fr(cm(L))} cm", f"soit {dit(cm(L))} centimètres")],
              f"Question deux. d'après la figure، tangente teta égale L sur deux، sur D، يعني tangente teta égale L sur deux D. "
              f"teta صغيرة en radian، إذن L égale deux D fois teta. L égale deux fois {dit(D)}، fois {sci_dit(th)}. "
              f"L égale {sci_dit(L)} mètre، soit {dit(cm(L))} centimètres.")}
    q3 = {"reponse": valeur("L'", round(cm(L2), 3), "cm",
                            f"L' = 2λD/a' = 2 × {sci(lam)} × {fr(D)}/({sci(a2)}) = {sci(L2)} m = {fr(cm(L2))} cm : a diminue, L augmente"),
          "clavier": {"aides": ["L = 2λD/a", "a' = " + fr(a2_mm) + " mm", "A.N. :", "cm"],
                      "pieges": ["L = 2λa/D", "L' = L", "a diminue donc L diminue"]},
          "correction": correction([
              ("3 : L' = 2λD/a' (λ et D ne changent pas)", "L prime égale deux lambda D sur a prime"),
              (f"L' = 2 × {sci(lam)} × {fr(D)}/({sci(a2)}) = {fr(cm(L2))} cm", f"soit {dit(cm(L2))} centimètres"),
              ("a est au dénominateur : quand a diminue, L augmente", "a فالتحت")],
              f"Question trois. lambda و D ما تبدلوش. L prime égale deux lambda D sur a prime، soit deux fois {sci_dit(lam)}، "
              f"fois {dit(D)}، sur {sci_dit(a2)}. L prime égale {sci_dit(L2)} mètre، soit {dit(cm(L2))} centimètres. "
              f"a فالتحت فla relation: ملي a كتنقص، L كتزيد.")}
    return q1, q2, q3


LAM, A, D, A2 = 640, 0.16, 2.5, 0.08           # exercice (réglables dans ecart-angulaire.html et diffraction.html)
LAMB, AB, DB, A2B = 520, 0.20, 3.0, 0.10       # semblable
lam, a, a2, TH, L, L2 = calc(LAM, A, D, A2)
Q1, Q2, Q3 = questions_calc(LAM, A, D, A2)
Q1B, Q2B, Q3B = questions_calc(LAMB, AB, DB, A2B)
REGLAGE = {"D_m": D, "a_mm": A, "lambda_nm": LAM}
TH_NM_MM = LAM / A                               # piège : λ en nm, a en mm
TH_INV = a / lam                                 # piège : a/λ

EX = {
  "id": "phys_ex_ch3_fente_2", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_lumineuses", "cours": "phys_ch3_ondes_lumineuses",
  "titre": "Un laser rouge et une fente fine", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer l'écart angulaire θ = λ/a", "Calculer la largeur L de la tache centrale avec tan θ ≈ θ",
                  "Prévoir l'effet de la largeur a de la fente sur L"],
  "enonce": {
    "intro": f"On éclaire une fente fine verticale de largeur a avec un laser rouge de longueur d'onde λ = {LAM} nm. Sur un écran placé à la distance D de la fente, on observe une figure de diffraction. La figure représente le montage vu de dessus : θ est l'écart angulaire, L la largeur de la tache centrale.",
    "intro_dit": f"دابا نقراو l'énoncé. كنضويو على une fente fine بواحد le laser rouge، la longueur d'onde ديالو lambda égale {entier(LAM)} nanomètres. فوق l'écran، على la distance D من la fente، كنشوفو une figure de diffraction. la figure كتبين le montage vu de dessus: teta هي l'écart angulaire، و L هي la largeur ديال la tache centrale.",
    "figures": [montage()],
    "donnees": [f"λ = {LAM} nm", f"a = {fr(A)} mm", f"D = {fr(D)} m", f"a' = {fr(A2)} mm (question 3)", "1 nm = 10⁻⁹ m ; 1 mm = 10⁻³ m"],
    "questions": [
      {"id": "1", "texte": "Calculer l'écart angulaire θ.",
       "texte_dit": "Question un: حسب l'écart angulaire teta.", **Q1,
       "aides": [aide("θ dépend de la longueur d'onde du laser et de la largeur de la fente. Avant le calcul, mets les deux longueurs dans la même unité.",
                      "teta كتعلق ب la longueur d'onde ديال le laser، و ب la largeur ديال la fente. قبل الحساب، حط les deux en mètre."),
                 aide("θ = λ/a, avec λ et a en mètre ; θ est alors en radian.",
                      "teta égale lambda sur a، و lambda و a en mètre. teta كتخرج en radian.")],
       "explication": "ex_f1", "facile": "fa_f1"},
      {"id": "2", "texte": "D'après la figure, tan θ = (L/2)/D. L'angle θ étant petit, on prend tan θ ≈ θ (θ en radian). Calculer, en cm, la largeur L de la tache centrale.",
       "texte_dit": "Question deux: من la figure، tangente teta égale L sur deux، sur D. teta صغيرة، إذن tangente teta تقريبا teta. حسب la largeur L ديال la tache centrale en centimètre.",
       **Q2,
       "aides": [aide("Dans le triangle, le côté en face de θ est la moitié de la tache, L/2 ; le côté collé à θ est D.",
                      "فle triangle، le côté اللي قدام teta هو النص ديال la tache، L sur deux. و le côté اللي لاصق ف teta هو D."),
                 aide("tan θ = L/(2D) et tan θ ≈ θ : donc L = 2D·θ. Convertis le résultat en cm.",
                      "tangente teta égale L sur deux D، و tangente teta تقريبا teta. إذن L égale deux D fois teta. ومن بعد حول en centimètre.")],
       "explication": "ex_f2", "facile": "fa_f2"},
      {"id": "3", "texte": f"On remplace la fente par une fente plus fine, de largeur a' = {fr(A2)} mm ; le laser et l'écran ne changent pas. Calculer, en cm, la nouvelle largeur L' de la tache centrale. Comment varie L quand a diminue ?",
       "texte_dit": f"Question trois: كنبدلو la fente ب fente أرق، a prime égale {dit(A2)} millimètre. le laser و l'écran ما تبدلوش. حسب la largeur جديدة L prime en centimètre. كيفاش كتبدل L ملي a كتنقص؟",
       **Q3,
       "aides": [aide("Des questions 1 et 2 : L = 2D·θ et θ = λ/a. Qu'est-ce qui change ici : λ, D ou a ?",
                      "من السؤال الأول والثاني: L égale deux D fois teta، و teta égale lambda sur a. شنو اللي تبدل هنا: lambda، ولا D، ولا a؟"),
                 aide("L = 2λD/a : a est au dénominateur. Calcule L' avec a' en mètre.",
                      "L égale deux lambda D sur a: a فالتحت. حسب L prime ب a prime en mètre.")],
       "explication": "ex_f3", "facile": "fa_f3"},
    ]},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    diapo_sim("ex_f1", "Question 1 : l'écart angulaire θ = λ/a", "θ va du centre de la tache à son bord : θ = λ/a.",
      f"{SIM}ecart-angulaire.html", "Le montage réglé avec les valeurs de l'exercice",
      f"هادا le montage vu de dessus: le laser، la fente، و l'écran. كنحطو les valeurs ديال التمرين: lambda égale {entier(LAM)} nanomètres، "
      f"a égale {dit(A)} millimètre، et D égale {dit(D)} mètres. الشعاع اللول كيمشي نيشان للوسط ديال la tache centrale. "
      f"الشعاع الثاني كيمشي للطرف ديالها، فين كتبدا أول extinction. الزاوية بيناتهم هي l'écart angulaire teta. "
      f"رد البال: فالرسم الزاوية كبيرة باش نشوفوها مزيان. الدرس كيعطينا: teta égale lambda sur a، ب lambda و a en mètre. "
      f"teta égale {sci_dit(lam)}، sur {sci_dit(a)}. teta égale {sci_dit(TH)} radian.",
      [("θ = λ/a", "teta égale lambda sur a"), (f"θ = {sci(lam)}/({sci(a)}) = {sci(TH)} rad", f"teta égale {sci_dit(TH)} radian")],
      [dict(mot="كنحطو les valeurs", commande="set_parameters", parametres=REGLAGE),
       dict(mot="الشعاع اللول كيمشي", commande="play_until", parametres={"moment": "rayon_centre"}),
       dict(mot="الشعاع الثاني كيمشي", commande="play_until", parametres={"moment": "rayon_bord"}),
       dict(mot="الزاوية بيناتهم", commande="play_until", parametres={"moment": "angle_theta"}),
       dict(mot="رد البال: فالرسم", repere="theta"),
       dict(mot="teta égale lambda sur a", cible="centre:0"),
       dict(mot=f"teta égale {sci_dit(TH)} radian", cible="centre:1")]),
    diapo_sim("ex_f2", "Question 2 : du triangle à L = 2D·θ", "tan θ = L/(2D) ≈ θ, donc L = 2D·θ.",
      f"{SIM}ecart-angulaire.html", "La demi-largeur L/2, le triangle seul, puis tan θ ≈ θ",
      f"نفس le montage، بالقيم ديال التمرين. من الوسط ديال la tache حتى الطرف ديالها: هادي L sur deux، النص ديال L. "
      f"دابا كنخرجو le triangle بوحدو: الزاوية teta فla fente، L sur deux قدامها، و D لاصق فيها. "
      f"tangente teta égale le côté opposé sur le côté adjacent: tangente teta égale L sur deux D. "
      f"teta صغيرة en radian، إذن tangente teta تقريبا teta، et L égale deux D fois teta. "
      f"L égale deux fois {dit(D)}، fois {sci_dit(TH)}. L égale {sci_dit(L)} mètre، soit {dit(cm(L))} centimètres. "
      f"شوف la simulation: L égale {dit(cm(L))} centimètres.",
      [("tan θ = L/(2D) ≈ θ", "tangente teta égale L sur deux D"), (f"L = 2 × {fr(D)} × {sci(TH)} = {fr(cm(L))} cm", "et L égale deux D fois teta")],
      [dict(mot="نفس le montage", commande="set_parameters", parametres=REGLAGE),
       dict(mot="من الوسط ديال la tache", commande="play_until", parametres={"moment": "demi_largeur"}),
       dict(mot="هادي L sur deux", repere="L_sur_2"),
       dict(mot="دابا كنخرجو le triangle", commande="play_until", parametres={"moment": "triangle_isole"}),
       dict(mot="و D لاصق فيها", repere="D"),
       dict(mot="tangente teta égale le côté", commande="play_until", parametres={"moment": "tan_ecrit"}),
       dict(mot="tangente teta égale L sur deux D", cible="centre:0"),
       dict(mot="teta صغيرة en radian", commande="play_until", parametres={"moment": "petit_angle"}),
       dict(mot="et L égale deux D fois teta", cible="centre:1"),
       dict(mot="شوف la simulation", repere="L")]),
    diapo_sim("ex_f3", "Question 3 : une fente plus fine", "a au dénominateur : a diminue, L augmente.",
      f"{SIM}diffraction.html?vue=mesure", "L'écran vu de face, avec la règle : a, puis a' deux fois plus petite",
      f"هادي l'écran vu de face، مع la règle. كنحطو la fente: a égale {dit(A)} millimètre. "
      f"شوف la tache centrale: L égale {dit(cm(L))} centimètres. دابا كنبدلو غير la fente: a prime égale {dit(A2)} millimètre، la moitié. "
      f"la tache ولات عريضة: L prime égale {dit(cm(L2))} centimètres، le double. "
      f"L égale deux lambda D sur a: a فالتحت، إذن ملي a كتنقص، L كتزيد. "
      f"بالحساب: L prime égale deux fois {sci_dit(lam)}، fois {dit(D)}، sur {sci_dit(a2)}. L prime égale {sci_dit(L2)} mètre، soit {dit(cm(L2))} centimètres.",
      [("L = 2λD/a : a diminue, L augmente", "a فالتحت، إذن"), (f"L' = 2 × {sci(lam)} × {fr(D)}/({sci(a2)}) = {fr(cm(L2))} cm", "بالحساب: L prime")],
      [dict(mot="كنحطو la fente", commande="set_parameters", parametres=REGLAGE),
       dict(mot="شوف la tache centrale", commande="play_until", parametres={"moment": "mesure_L"}),
       dict(mot="centimètres. دابا", repere="L"),
       dict(mot="دابا كنبدلو غير la fente", commande="set_parameters", parametres={"a_mm": A2}),
       dict(mot="la tache ولات عريضة", commande="play_until", parametres={"moment": "mesure_L"}),
       dict(mot="le double", repere="L"),
       dict(mot="a فالتحت، إذن", cible="centre:0"),
       dict(mot="بالحساب: L prime", cible="centre:1")]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_f1", "Plus facile : calculer θ", "سؤال ساهل: اختار la bonne valeur ديال teta.",
      f"λ = {LAM} nm et a = {fr(A)} mm. L'écart angulaire θ vaut…",
      [f"θ = {fr(TH_NM_MM, 0)} rad", f"θ = {fr(TH_INV, 0)} rad", f"θ = {sci(TH)} rad"], 2, {
        "2": {"juste": rep(f"برافو! teta égale lambda sur a، ب lambda و a en mètre. teta égale {sci_dit(TH)} radian: زاوية صغيرة بزاف.",
                           f"Juste : θ = λ/a = {sci(lam)}/({sci(a)}) = {sci(TH)} rad.")},
        "0": {"1": rep("ما تقلقش. la relation صحيحة، ولكن lambda بقات en nanomètre و a en millimètre. حول les deux en mètre. عاود اختار.",
                       "La relation est bonne, mais λ est en nm et a en mm : convertis les deux en mètre. Réessaie."),
              "2": rep(f"الجواب: teta égale {sci_dit(lam)}، sur {sci_dit(a)}، soit {sci_dit(TH)} radian.",
                       f"Réponse : θ = {sci(lam)}/({sci(a)}) = {sci(TH)} rad (longueurs en mètre).")},
        "1": {"1": rep("قريب! ولكن قلبتي la relation: teta égale lambda sur a، ماشي a sur lambda. عاود اختار.",
                       "La fraction est inversée : θ = λ/a, pas a/λ. Réessaie."),
              "2": rep(f"الجواب: teta égale lambda sur a، soit {sci_dit(TH)} radian. teta ديما صغيرة فهاد التجربة.",
                       f"Réponse : θ = λ/a = {sci(TH)} rad (θ est petit).")}},
      f"lambda égale {entier(LAM)} nanomètres، et a égale {dit(A)} millimètre. L'écart angulaire teta vaut ?"),
    vf_facile("fa_f2", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      "Dans le triangle du montage : θ au sommet (la fente), D collé à θ.", [
        ("Le côté en face de θ est L/2, la moitié de la tache centrale.", True, "θ va du centre de la tache à son bord : le côté opposé est L/2."),
        ("tan θ = L/D.", False, "Le côté opposé est L/2, pas L : tan θ = (L/2)/D = L/(2D)."),
        (f"Avec tan θ ≈ θ : L = 2D·θ = {fr(cm(L))} cm.", True, f"L = 2 × {fr(D)} × {sci(TH)} = {sci(L)} m = {fr(cm(L))} cm.")]),
    assoc_facile("fa_f3", "Plus facile : qui change quoi ?", "سؤال ساهل: ربط كل تبديل مع la conséquence ديالو.",
      "L = 2λD/a et θ = λ/a.", "Relie chaque changement à son effet.",
      [("1", "On rend la fente plus fine (a diminue)"), ("2", "On éloigne l'écran (D augmente)"), ("3", "On prend un laser bleu (λ diminue)")],
      [("a", "θ augmente et L augmente"), ("b", "θ ne change pas, L augmente"), ("c", "θ diminue et L diminue")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : a est au dénominateur de θ = λ/a et de L = 2λD/a : a diminue, θ et L augmentent.", "برافو: a فالتحت، ملي a كتنقص، teta و L كيزيدو."),
       "1-b": (False, "θ = λ/a dépend de a : si a change, θ change.", "لا، teta égale lambda sur a: ملي a كتبدل، teta كتبدل حتى هي."),
       "1-c": (False, "a est au dénominateur : quand a diminue, θ et L augmentent, ils ne diminuent pas.", "لا، a فالتحت: ملي a كتنقص، teta و L ما كينقصوش."),
       "2-a": (False, "θ = λ/a ne contient pas D : éloigner l'écran ne change pas θ.", "لا، D ما كايناش ف teta égale lambda sur a: teta ما كتبدلش."),
       "2-b": (True, "Oui : θ = λ/a ne dépend pas de D, mais L = 2λD/a augmente avec D.", "برافو: teta ما كتبدلش، ولكن L كتزيد مع D."),
       "2-c": (False, "D est au numérateur de L : D augmente, L augmente.", "لا، D فالفوق ف la relation ديال L: ملي D كتزيد، L كتزيد."),
       "3-a": (False, "λ est au numérateur : λ diminue, θ et L diminuent.", "لا، lambda فالفوق: ملي lambda كتنقص، teta و L كينقصو."),
       "3-b": (False, "θ = λ/a dépend de λ : un autre laser change θ.", "لا، teta كتعلق ب lambda: laser آخر كيبدل teta."),
       "3-c": (True, "Oui : λ au numérateur de θ et de L : λ diminue, les deux diminuent.", "برافو: lambda فالفوق، ملي lambda كتنقص، teta و L كينقصو.")},
      ("(1 ; a) (2 ; b) (3 ; c) : L = 2λD/a, λ et D en haut, a en bas.",
       "L égale deux lambda D sur a: lambda و D فالفوق، و a فالتحت.")),
  ]}]},
  "similaire": {
    "id": "phys_ex_ch3_fente_2_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": f"On éclaire une fente fine de largeur a avec un laser vert de longueur d'onde λ = {LAMB} nm. Un écran est placé à la distance D de la fente (même montage que la figure).",
      "intro_dit": f"نفس التمرين، بقيم أخرى. le laser vert، lambda égale {entier(LAMB)} nanomètres، كيضوي على une fente fine. l'écran على la distance D من la fente.",
      "figures": [montage()],
      "donnees": [f"λ = {LAMB} nm", f"a = {fr(AB)} mm", f"D = {fr(DB)} m", f"a' = {fr(A2B)} mm (question 3)", "1 nm = 10⁻⁹ m ; 1 mm = 10⁻³ m"],
      "questions": [
        {"id": "1", "texte": "Calculer l'écart angulaire θ.", **Q1B},
        {"id": "2", "texte": "On prend tan θ ≈ θ (θ petit, en radian). Calculer, en cm, la largeur L de la tache centrale.", **Q2B},
        {"id": "3", "texte": f"On remplace la fente par une fente de largeur a' = {fr(A2B)} mm, sans rien changer d'autre. Calculer, en cm, la nouvelle largeur L'. Comment varie L quand a diminue ?", **Q3B},
      ]}},
}
controle_voix(EX)
ecrire(EX)
