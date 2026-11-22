# Exercice moyen de physique, ch. 3 (propagation d'une onde lumineuse) : la courbe θ = f(1/a) d'un laser vert ;
# montrer que θ = L/(2D), justifier la relation linéaire, pente → λ, largeur d'une fente inconnue, puis un laser rouge.
#
# Sources comparées (skill exercices § 2) :
# - exploration backend/data/curriculum/exploration/ondes_lumineuses.json : cas_types « courbe » (trois temps : droite par
#   l'origine, coefficient directeur avec les unités des axes, identification θ = λ·(1/a) donc k = λ ; λ en nm vérifiée
#   dans le visible), « etablir_L » (quatre lignes : tan θ = L/2D, θ petit, tan θ ≈ θ), « calcul_direct », « variation » ;
#   pieges (facteurs ×10³ et ×10⁻³ des axes oubliés ; lire a sur un axe en 1/a ; prendre la pente pour λ dans toutes les
#   courbes ; L entière comme côté opposé) ; erreurs_examen « courbe » et « établir L ».
# - vidéos des 10 profs : Laksabi et Souhaib (trois courbes), Taousse (méthode graphique en trois temps), Bazhar
#   (θ = λ/a tirée d'une courbe), Driss (L = f(1/a)).
# - nationaux comparés : 2021 N (courbe L = f(D) → λ = 600 nm, puis cheveu), 2013 N (L = f(1/a), cité par l'exploration),
#   2023 R (a = 2λD/L puis rapport rouge/jaune), 2017 R (L quand on passe au violet), 2019 R (comparer L_R et L_B).
#   Le nôtre : courbe θ = f(1/a) (pas L = f(D) ni L = f(1/a)) d'un laser vert 520 nm avec D = 2,0 m, une fente
#   inconnue (L' = 2,6 cm → a' = 0,08 mm), puis un laser rouge et la nouvelle pente : situation, données et chaîne
#   différentes de chaque national.
# - séries en ligne : recherche web faite (talamidi série corrigée 1 : un exercice où l'on vérifie θ = λ/a sur une
#   courbe ; moutamadris séries 1 et 2 BIOF) : seuls les extraits des moteurs étaient lisibles (PDF bloqués par le
#   réseau de la session). Rien n'est copié.
# - simulations : courbe.html?courbe=theta_inverse_a (laser 650 nm, sa pente 6,5·10⁻⁷ m : la voix la décrit puis dit
#   « فالتمرين » avec 520 nm) ; diffraction.html?vue=mesure réglée sur 520 nm, a' = 0,08 mm, D = 2,0 m (L = 2,6 cm),
#   puis 650 nm (L = 3,25 cm) ; ecart-angulaire.html?vue=triangle (démonstration de θ = L/(2D)).
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


    # (fin de montage)


INV_A = [2.5, 5, 10, 12.5, 20]                  # 1/a en 10³ m⁻¹ : a = 0,40 ; 0,20 ; 0,10 ; 0,08 ; 0,05 mm


def courbe(lam_nm, ymax):
    """θ (10⁻³ rad) en fonction de 1/a (10³ m⁻¹) : θ = λ·(1/a) ; pente en unités des axes = λ en 10⁻⁶ m… soit λ_nm/1000."""
    k = lam_nm / 1000
    xa, ya = 20, round(k * 20, 3)
    gy = [g for g in range(2, ymax + 1, 2) if abs(g - ya) > 0.9] + [[ya, fr(ya)]]
    el = [{"f": "courbe", "expr": f"{k}*x", "de": 0, "a": 21.5, "couleur": "cyan"}]
    el += [{"f": "point", "at": [x, round(k * x, 4)], "couleur": "jaune"} for x in INV_A if x != xa]
    el += [{"f": "point", "at": [xa, ya], "couleur": "jaune", "t": "A", "pos": "no"},
           {"f": "repere", "x": xa, "y": ya, "couleur": "faible"}]
    return {"type": "courbe", "titre": "Figure 2 : θ en fonction de 1/a",
            "axes": {"x": {"min": 0, "max": 22, "nom": "1/a", "unite": "10³ m⁻¹", "graduations": [5, 10, 15, 20]},
                     "y": {"min": 0, "max": ymax, "nom": "θ", "unite": "10⁻³ rad", "graduations": gy}},
            "legende": f"Les points de mesure ; A ({xa} × 10³ m⁻¹ ; {fr(ya)} × 10⁻³ rad) est sur la droite.",
            "elements": el}, xa, ya


def calc(lam_nm, D, Lp_cm, lam2_nm):
    lam, lam2 = lam_nm * 1e-9, lam2_nm * 1e-9
    a2 = 2 * lam * D / (Lp_cm * 1e-2)
    L2 = 2 * lam2 * D / a2
    return lam, lam2, a2, L2


def qs(lam_nm, D, Lp_cm, lam2_nm, coul2):
    """reponse, clavier, correction des 6 questions (exercice et semblable)."""
    fig, xa, ya = courbe(lam_nm, 12 if lam_nm < 560 else 14)
    lam, lam2, a2, L2 = calc(lam_nm, D, Lp_cm, lam2_nm)
    k = ya * 1e-3 / (xa * 1e3)
    plus = lam2_nm > lam_nm
    r = {}
    r["1"] = {"reponse": phrase("D'après la figure 1, dans le triangle rectangle : tan θ = (L/2)/D = L/(2D). θ est petit, en radian : tan θ ≈ θ. Donc θ = L/(2D)."),
              "clavier": {"aides": ["tan θ = côté opposé/côté adjacent", "L/2", "tan θ ≈ θ"], "pieges": ["tan θ = L/D", "sin θ = L/(2D)"]},
              "correction": correction([("1 : tan θ = (L/2)/D = L/(2D)", "tangente teta égale L sur deux، sur D"),
                                        ("θ petit (en radian) : tan θ ≈ θ", "teta صغيرة en radian"),
                                        ("donc θ = L/(2D)", "إذن teta égale L sur deux D")],
                                       "Question un. d'après la figure un، فle triangle rectangle، tangente teta égale L sur deux، sur D، soit L sur deux D. "
                                       "teta صغيرة en radian، إذن tangente teta تقريبا teta. إذن teta égale L sur deux D.")}
    r["2-1"] = {"reponse": phrase("La courbe θ = f(1/a) est une droite qui passe par l'origine : θ est une fonction linéaire de 1/a, de la forme θ = k·(1/a), k étant le coefficient directeur de la droite."),
                "clavier": {"aides": ["droite qui passe par l'origine", "fonction linéaire", "θ = k·(1/a)"], "pieges": ["θ = k·a", "θ = k·(1/a) + b"]},
                "correction": correction([("2-1 : la courbe est une droite qui passe par l'origine", "droite كتدوز من l'origine"),
                                          ("donc θ = k·(1/a), k : coefficient directeur", "teta égale k fois un sur a")],
                                         "Question deux point un. la courbe droite كتدوز من l'origine. إذن teta fonction linéaire de un sur a: "
                                         "teta égale k fois un sur a، و k هو le coefficient directeur.")}
    r["2-2"] = {"reponse": valeur("λ", round(k * 1e9, 3), "nm",
                                  f"k = Δθ/Δ(1/a) = ({fr(ya)} × 10⁻³ − 0)/({xa} × 10³ − 0) = {sci(k)} m ; θ = λ·(1/a) donc λ = k = {sci(k)} m = {fr(k * 1e9, 0)} nm"),
                "clavier": {"aides": ["k = Δθ/Δ(1/a)", "θ = λ·(1/a)", "×10³", "×10⁻³", "1 nm = 10⁻⁹ m", "A.N. :", "nm"],
                            "pieges": ["k = Δ(1/a)/Δθ", "λ = 2k", "oublier ×10³ et ×10⁻³"]},
                "correction": correction([
                    (f"2-2 : k = Δθ/Δ(1/a) = ({fr(ya)} × 10⁻³)/({xa} × 10³) = {sci(k)} m", "k égale delta teta sur delta un sur a"),
                    ("θ = λ·(1/a) : par identification, k = λ", "par identification"),
                    (f"λ = {sci(k)} m = {fr(k * 1e9, 0)} nm (400 nm ≤ λ ≤ 800 nm)", f"lambda égale {entier(round(k * 1e9))} nanomètres")],
                    f"Question deux point deux. k égale delta teta sur delta un sur a، avec l'origine et le point A. "
                    f"k égale {dit(ya)} fois dix puissance moins trois، sur {entier(xa)} fois dix puissance trois، soit {sci_dit(k)} mètre. "
                    f"والدرس: teta égale lambda fois un sur a. par identification، k égale lambda. "
                    f"إذن lambda égale {entier(round(k * 1e9))} nanomètres، فle visible.")}
    r["3"] = {"reponse": valeur("a'", round(a2 * 1e3, 4), "mm",
                                f"λ/a' = L'/(2D) donc a' = 2λD/L' = 2 × {sci(lam)} × {fr(D)}/({sci(Lp_cm * 1e-2)}) = {sci(a2)} m = {fr(a2 * 1e3, 3)} mm"),
              "clavier": {"aides": ["θ = λ/a", "θ = L/(2D)", "a' = 2λD/L'", "1 cm = 10⁻² m", "A.N. :", "mm"],
                          "pieges": ["a' = λD/L'", "a' = L'/(2λD)", "L' en cm dans le calcul"]},
              "correction": correction([
                  ("3 : θ = λ/a' et θ = L'/(2D), donc λ/a' = L'/(2D)", "lambda sur a prime égale L prime sur deux D"),
                  (f"a' = 2λD/L' = 2 × {sci(lam)} × {fr(D)}/({sci(Lp_cm * 1e-2)})", "a prime égale deux lambda D sur L prime"),
                  (f"a' = {sci(a2)} m = {fr(a2 * 1e3, 3)} mm", f"a prime égale {sci_dit(a2)} mètre")],
                  f"Question trois. teta égale lambda sur a prime، و teta égale L prime sur deux D. إذن lambda sur a prime égale L prime sur deux D، "
                  f"و a prime égale deux lambda D sur L prime. a prime égale deux fois {sci_dit(lam)}، fois {dit(D)}، sur {sci_dit(Lp_cm * 1e-2)}. "
                  f"a prime égale {sci_dit(a2)} mètre، soit {dit(a2 * 1e3, 3)} millimètre.")}
    r["4-1"] = {"reponse": valeur("L_R", round(L2 * 100, 4), "cm",
                                  f"L_R = 2λ_R·D/a' = 2 × {sci(lam2)} × {fr(D)}/({sci(a2)}) = {sci(L2, 4)} m = {fr(L2 * 100, 3)} cm"),
                "clavier": {"aides": ["L = 2λD/a", "a' (question 3)", "A.N. :", "cm"], "pieges": [f"L_R = {fr(Lp_cm)} cm (λ ne compte pas)", "L = 2λa/D"]},
                "correction": correction([
                    ("4-1 : même fente a' et même D : L_R = 2λ_R·D/a'", "L R égale deux lambda R D sur a prime"),
                    (f"L_R = 2 × {sci(lam2)} × {fr(D)}/({sci(a2)})", "soit deux fois"),
                    (f"L_R = {sci(L2, 4)} m = {fr(L2 * 100, 3)} cm", f"L R égale {sci_dit(L2, 4)} mètre")],
                    f"Question quatre point un. نفس la fente a prime، ونفس D. L R égale deux lambda R D sur a prime، "
                    f"soit deux fois {sci_dit(lam2)}، fois {dit(D)}، sur {sci_dit(a2)}. L R égale {sci_dit(L2, 4)} mètre، soit {dit(L2 * 100, 3)} centimètres.")}
    comp = "plus" if plus else "moins"
    pos = "au-dessus de" if plus else "au-dessous de"
    r["4-2"] = {"reponse": phrase(f"Pour le laser {coul2}, θ = λ_{coul2[0].upper()}·(1/a) : c'est encore une droite qui passe par l'origine, mais son coefficient directeur est "
                                  f"λ_{coul2[0].upper()} = {sci(lam2)} m, {'supérieur' if plus else 'inférieur'} à k = {sci(k)} m : la droite est {comp} inclinée, {pos} celle de la figure 2."),
                "clavier": {"aides": ["θ = λ·(1/a)", "k = λ", "plus inclinée", "moins inclinée"], "pieges": ["même droite", "la droite ne passe plus par l'origine"]},
                "correction": correction([
                    (f"4-2 : θ = λ_{coul2[0].upper()}·(1/a) : droite qui passe par l'origine, de pente λ_{coul2[0].upper()}", "droite كتدوز من l'origine"),
                    (f"λ_{coul2[0].upper()} = {lam2_nm} nm {'>' if plus else '<'} λ = {lam_nm} nm", f"lambda égale {entier(lam2_nm)} nanomètres"),
                    (f"donc la droite est {comp} inclinée ({pos} celle de la figure 2)", "مايلة أكثر" if plus else "مايلة أقل")],
                    f"Question quatre point deux. مع le laser {coul2}، teta égale lambda fois un sur a: droite كتدوز من l'origine، و la pente ديالها هي lambda. "
                    f"دابا lambda égale {entier(lam2_nm)} nanomètres، {'plus grande' if plus else 'plus petite'} que {entier(lam_nm)} nanomètres. "
                    f"إذن la droite {'مايلة أكثر' if plus else 'مايلة أقل'}، {'فوق' if plus else 'تحت'} la droite ديال la figure deux.")}
    return fig, xa, ya, k, lam, lam2, a2, L2, r


LAM, D, LP, LAMR = 520, 2.0, 2.6, 650         # exercice : laser vert, D, L' mesurée (cm), laser rouge
LAMB_, DB, LPB, LAM2B = 600, 1.5, 1.5, 450    # semblable : laser orange, laser bleu
FIG, XA, YA, K, lam, lamR, A2, LR, R = qs(LAM, D, LP, LAMR, "rouge")
FIGB, XAB, YAB, KB, *_, RB = qs(LAMB_, DB, LPB, LAM2B, "bleu")
assert abs(K - LAM * 1e-9) < 1e-15 and abs(KB - LAMB_ * 1e-9) < 1e-15
A2MM = A2 * 1e3
REG = {"D_m": D, "a_mm": round(A2MM, 2), "lambda_nm": LAM}
LR_INV = LP * LAM / LAMR                       # piège : rapport inversé
NU_A = 20e3 / (YA * 1e-3)                      # piège : pente inversée


def avec(q, **champs):
    q = dict(q); q.update(champs); return q


EX = {
  "id": "phys_ex_ch3_courbe_3", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_lumineuses", "cours": "phys_ch3_ondes_lumineuses",
  "titre": "La droite θ = f(1/a) d'un laser vert", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Montrer que θ = L/(2D) avec tan θ ≈ θ", "Exploiter une courbe linéaire θ = f(1/a) : pente et identification k = λ",
                  "Calculer la largeur d'une fente a = 2λD/L", "Prévoir l'effet de la longueur d'onde sur L et sur la pente"],
  "enonce": {
    "intro": (f"On réalise une expérience de diffraction avec un laser vert de longueur d'onde λ inconnue. L'écran est placé à la distance "
              f"D = {fr(D)} m de la fente (figure 1). On utilise plusieurs fentes de largeurs a différentes ; pour chacune, on mesure la largeur L "
              f"de la tache centrale et on calcule l'écart angulaire θ. On trace ensuite la courbe θ = f(1/a) (figure 2). L'angle θ est petit : "
              f"on prend tan θ ≈ θ (θ en radian)."),
    "intro_dit": (f"دابا نقراو l'énoncé. كنديرو expérience de diffraction ب le laser vert، و la longueur d'onde lambda ديالو ما معروفاش. "
                  f"l'écran على la distance D égale {dit(D)} mètres من la fente. كنستعملو بزاف ديال les fentes، كل وحدة عندها a ديالها. "
                  f"لكل fente، كنقيسو L ديال la tache centrale، وكنحسبو teta. ومن بعد كنرسمو teta en fonction de un sur a، فla figure deux. "
                  f"teta صغيرة، إذن tangente teta تقريبا teta، en radian."),
    "figures": [montage(), FIG],
    "donnees": [f"D = {fr(D)} m", f"Point A de la droite : 1/a = {XA} × 10³ m⁻¹ ; θ = {fr(YA)} × 10⁻³ rad",
                f"Question 3 : L' = {fr(LP)} cm", f"Question 4 : λ_R = {LAMR} nm", "1 nm = 10⁻⁹ m ; 1 mm = 10⁻³ m ; 1 cm = 10⁻² m"],
    "questions": [
      avec(R["1"], id="1", texte="En s'aidant de la figure 1, montrer que θ = L/(2D).",
           texte_dit="Question un: من la figure un، بين بلي teta égale L sur deux D.",
           aides=[aide("Trouve le triangle rectangle de la figure 1 : θ au sommet (la fente). Quel côté est en face de θ, quel côté est collé à θ ?",
                       "قلب على le triangle rectangle فla figure un: teta فla fente. شنو le côté اللي قدام teta، وشنو اللي لاصق فيها؟"),
                  aide("Côté opposé L/2, côté adjacent D : tan θ = (L/2)/D. Puis θ petit en radian : tan θ ≈ θ.",
                       "le côté opposé هو L sur deux، و le côté adjacent هو D. إذن tangente teta égale L sur deux، sur D. ومن بعد teta صغيرة en radian: tangente teta تقريبا teta.")],
           explication="ex_c1", facile="fa_c1"),
      avec(R["2-1"], id="2-1", texte="Justifier que la courbe de la figure 2 traduit une relation de la forme θ = k·(1/a).",
           texte_dit="Question deux point un: علل علاش la courbe ديال la figure deux كتعطي teta égale k fois un sur a.",
           aides=[aide("Regarde la forme de la courbe, et par où elle passe.", "شوف la forme ديال la courbe، ومن فين كتدوز."),
                  aide("Une droite qui passe par l'origine représente une fonction linéaire : y = k·x.",
                       "droite كتدوز من l'origine، معناها fonction linéaire: y égale k fois x.")],
           explication="ex_c2", facile="fa_c2"),
      avec(R["2-2"], id="2-2", texte="Déterminer la valeur du coefficient directeur k, puis, sachant que θ = λ/a, en déduire la longueur d'onde λ du laser en nm.",
           texte_dit="Question deux point deux: حسب le coefficient directeur k، ومن بعد، ب teta égale lambda sur a، استنتج la longueur d'onde lambda en nanomètre.",
           aides=[aide("Prends l'origine et le point A. Lis bien les facteurs des axes : ×10³ m⁻¹ et ×10⁻³ rad.",
                       "خود l'origine و le point A. ورد البال ل les facteurs ديال les axes: dix puissance trois mètre puissance moins un، et dix puissance moins trois radian."),
                  aide("k = Δθ/Δ(1/a). Écris le cours sous la même forme : θ = λ·(1/a), puis identifie k.",
                       "k égale delta teta sur delta un sur a. ومن بعد كتب الدرس بنفس الشكل: teta égale lambda fois un sur a، وقارن مع k.")],
           explication="ex_c3", facile="fa_c3"),
      avec(R["3"], id="3", texte=f"On remplace la fente par une fente de largeur inconnue a' ; on garde le laser vert et D = {fr(D)} m. On mesure L' = {fr(LP)} cm. Déterminer a' en mm.",
           texte_dit=f"Question trois: كنبدلو la fente ب fente أخرى، la largeur ديالها a prime ما معروفاش. نفس le laser vert، ونفس D. كنقيسو L prime égale {dit(LP)} centimètres. حدد a prime en millimètre.",
           aides=[aide("Tu as deux écritures de θ : celle du cours (avec λ et a') et celle de la question 1 (avec L' et D).",
                       "عندك جوج طرق باش تكتب teta: ديال الدرس، ب lambda و a prime، و ديال السؤال الأول، ب L prime و D."),
                  aide("λ/a' = L'/(2D), donc a' = 2λD/L'. Mets L' en mètre, puis donne a' en mm.",
                       "lambda sur a prime égale L prime sur deux D، إذن a prime égale deux lambda D sur L prime. حط L prime en mètre، ومن بعد عطي a prime en millimètre.")],
           explication="ex_c4", facile="fa_c4"),
      avec(R["4-1"], id="4-1", texte=f"On garde la fente a' et l'écran, et on remplace le laser vert par un laser rouge de longueur d'onde λ_R = {LAMR} nm. Calculer, en cm, la largeur L_R de la nouvelle tache centrale.",
           texte_dit=f"Question quatre point un: نفس la fente a prime ونفس l'écran، ولكن كنبدلو le laser vert ب le laser rouge: lambda R égale {entier(LAMR)} nanomètres. حسب la largeur L R en centimètre.",
           aides=[aide("Qu'est-ce qui change par rapport à la question 3 : λ, a' ou D ?", "شنو اللي تبدل من السؤال ثلاثة: lambda، ولا a prime، ولا D؟"),
                  aide("L = 2λD/a : remplace λ par λ_R, garde a' et D.", "L égale deux lambda D sur a: بدل lambda ب lambda R، وخلي a prime و D.")],
           explication="ex_c5", facile="fa_c5"),
      avec(R["4-2"], id="4-2", texte="Avec le laser rouge, on trace de nouveau θ = f(1/a). Comment se place cette droite par rapport à celle de la figure 2 ? Justifier.",
           texte_dit="Question quatre point deux: ب le laser rouge، كنعاودو نرسمو teta en fonction de un sur a. فين كتجي هاد la droite بالنسبة ل la droite ديال la figure deux؟ علل.",
           aides=[aide("Que représente le coefficient directeur de la droite θ = f(1/a) (question 2-2) ?", "شنو هو le coefficient directeur ديال la droite teta en fonction de un sur a، dans la question deux point deux؟"),
                  aide("θ = λ·(1/a) : la pente est λ. Compare λ_R et λ du laser vert.", "teta égale lambda fois un sur a: la pente هي lambda. قارن lambda R مع lambda ديال le laser vert.")],
           explication="ex_c6", facile="fa_c6"),
    ]},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    diapo_sim("ex_c1", "Question 1 : montrer que θ = L/(2D)", "tan θ = (L/2)/D ; θ petit : tan θ ≈ θ.",
      f"{SIM}ecart-angulaire.html?vue=triangle&depart=triangle_isole", "Le triangle seul : θ, L/2 en face, D collé",
      "هادا le triangle بوحدو، خرجناه من le montage. الزاوية teta فla fente. le côté opposé هو L sur deux، النص ديال la tache centrale. "
      "و le côté adjacent هو D. tangente teta égale le côté opposé sur le côté adjacent: tangente teta égale L sur deux، sur D، يعني L sur deux D. "
      "teta صغيرة بزاف، en radian، إذن tangente teta تقريبا teta. إذن teta égale L sur deux D. هادي هي les trois lignes اللي خاصك تكتب فالورقة.",
      [("tan θ = (L/2)/D = L/(2D)", "يعني L sur deux D"), ("θ petit : tan θ ≈ θ, donc θ = L/(2D)", "إذن teta égale L sur deux D")],
      [dict(mot="الزاوية teta فla fente", repere="theta"),
       dict(mot="le côté opposé هو L", repere="L_sur_2"),
       dict(mot="و le côté adjacent هو D", repere="D"),
       dict(mot="tangente teta égale le côté", commande="play_until", parametres={"moment": "tan_ecrit"}),
       dict(mot="يعني L sur deux D", cible="centre:0"),
       dict(mot="teta صغيرة بزاف", commande="play_until", parametres={"moment": "petit_angle"}),
       dict(mot="إذن teta égale L sur deux D", cible="centre:1")]),
    diapo_sim("ex_c2", "Question 2-1 : une droite qui passe par l'origine", "Droite par l'origine : θ = k·(1/a).",
      f"{SIM}courbe.html?courbe=theta_inverse_a", "θ en fonction de 1/a : les points, puis la droite",
      "على اليسار، l'expérience: la fente كتبدل. على اليمين، la courbe: teta en fonction de un sur a. فla simulation، le laser rouge، six cent cinquante nanomètres. "
      "la fente اللولة، والثانية، والثالثة، والرابعة: كل fente كتعطي نقطة. شوف: النقط كاملين على خط مستقيم، كيدوز من l'origine. "
      "إذن teta fonction linéaire de un sur a: teta égale k fois un sur a. فالتمرين، les points ديال la figure deux حتى هوما على droite كتدوز من l'origine: نفس الجواب.",
      [("droite par l'origine : θ = k·(1/a)", "teta égale k fois un sur a")],
      [dict(mot="على اليسار، l'expérience", repere="vue_experience"),
       dict(mot="على اليمين، la courbe", repere="vue_courbe"),
       dict(mot="la fente اللولة", commande="play_until", parametres={"moment": "point_1"}),
       dict(mot="والثانية", commande="play_until", parametres={"moment": "point_2"}),
       dict(mot="والثالثة", commande="play_until", parametres={"moment": "point_3"}),
       dict(mot="والرابعة", commande="play_until", parametres={"moment": "point_4"}),
       dict(mot="شوف: النقط", commande="play_until", parametres={"moment": "droite"}),
       dict(mot="كيدوز من l'origine", repere="origine"),
       dict(mot="teta égale k fois un sur a", cible="centre:0")]),
    diapo_sim("ex_c3", "Question 2-2 : la pente, puis λ", "k = Δθ/Δ(1/a) ; θ = λ·(1/a) donc k = λ.",
      f"{SIM}courbe.html?courbe=theta_inverse_a&depart=droite", "Le triangle de pente et l'identification",
      f"باش نحسبو le coefficient directeur، كناخدو l'origine وواحد النقطة واضحة. فla simulation: un sur a égale dix fois dix puissance trois mètre puissance moins un، "
      f"و teta égale six virgule cinq fois dix puissance moins trois radian. k égale delta teta sur delta un sur a، soit six virgule cinq fois dix puissance moins sept mètre. "
      f"والدرس: teta égale lambda fois un sur a. par identification، k égale lambda: six cent cinquante nanomètres. "
      f"فالتمرين، le point A: un sur a égale {entier(XA)} fois dix puissance trois، et teta égale {dit(YA)} fois dix puissance moins trois. "
      f"k égale {dit(YA)} fois dix puissance moins trois، sur {entier(XA)} fois dix puissance trois، soit {sci_dit(K)} mètre. "
      f"إذن lambda égale {entier(LAM)} nanomètres، فle visible.",
      [(f"k = ({fr(YA)} × 10⁻³)/({XA} × 10³) = {sci(K)} m", f"k égale {dit(YA)} fois"), (f"λ = k = {LAM} nm", f"إذن lambda égale {entier(LAM)}")],
      [dict(mot="كناخدو l'origine", repere="origine"),
       dict(mot="k égale delta teta", commande="play_until", parametres={"moment": "pente"}),
       dict(mot="par identification", commande="play_until", parametres={"moment": "identification"}),
       dict(mot=f"k égale {dit(YA)} fois", cible="centre:0"),
       dict(mot=f"إذن lambda égale {entier(LAM)}", cible="centre:1")]),
    diapo_sim("ex_c4", "Question 3 : la largeur a' de la fente inconnue", "λ/a' = L'/(2D), donc a' = 2λD/L'.",
      f"{SIM}diffraction.html?vue=mesure", "Le laser vert de l'exercice et la tache mesurée sur la règle",
      f"فهاد la simulation، كنحطو le laser vert ديال التمرين: lambda égale {entier(LAM)} nanomètres، و l'écran à la distance D égale {dit(D)} mètres. "
      f"ودابا la fente المجهولة. شوف la tache centrale فla règle: L prime égale {dit(LP)} centimètres. "
      f"نفس la relation ديال الدرس: lambda sur a prime égale L prime sur deux D. إذن a prime égale deux lambda D sur L prime. "
      f"a prime égale deux fois {sci_dit(lam)}، fois {dit(D)}، sur {sci_dit(LP * 1e-2)}. a prime égale {sci_dit(A2)} mètre، soit {dit(A2MM, 3)} millimètre.",
      [("λ/a' = L'/(2D) donc a' = 2λD/L'", "lambda sur a prime égale"), (f"a' = {sci(A2)} m = {fr(A2MM, 3)} mm", f"a prime égale {sci_dit(A2)} mètre")],
      [dict(mot="كنحطو le laser vert", commande="set_parameters", parametres=REG),
       dict(mot="شوف la tache centrale", commande="play_until", parametres={"moment": "mesure_L"}),
       dict(mot=f"L prime égale {dit(LP)}", repere="L"),
       dict(mot="lambda sur a prime égale", cible="centre:0"),
       dict(mot=f"a prime égale {sci_dit(A2)} mètre", cible="centre:1")]),
    diapo_sim("ex_c5", "Question 4-1 : le laser rouge, même fente", "λ au numérateur : λ augmente, L augmente.",
      f"{SIM}diffraction.html?vue=mesure", "La tache verte, puis la rouge ; la verte reste en pointillé",
      f"نفس la fente a prime، ونفس l'écran. الأول le laser vert: شوف la tache الخضرا. دابا كنبدلو غير le laser: le laser rouge، lambda R égale {entier(LAMR)} nanomètres. "
      f"الخط ديال النقط هو la tache الخضرا اللي كانت قبل: la tache الحمرا عريضة كثر. L égale deux lambda D sur a: lambda فالفوق، ملي lambda كتزيد، L كتزيد. "
      f"L R égale deux fois {sci_dit(lamR)}، fois {dit(D)}، sur {sci_dit(A2)}. L R égale {sci_dit(LR)} mètre، soit {dit(LR * 100, 3)} centimètres.",
      [("L = 2λD/a : λ augmente, L augmente", "lambda فالفوق"), (f"L_R = {sci(LR)} m = {fr(LR * 100, 3)} cm", f"L R égale {sci_dit(LR)} mètre")],
      [dict(mot="نفس la fente a prime", commande="set_parameters", parametres={**REG, "trace_precedente": True}),
       dict(mot="الأول le laser vert", commande="play_until", parametres={"moment": "mesure_L"}),
       dict(mot="دابا كنبدلو غير le laser", commande="set_parameters", parametres={"lambda_nm": LAMR}),
       dict(mot="الخط ديال النقط", repere="tache_avant"),
       dict(mot="la tache الحمرا عريضة", repere="L"),
       dict(mot="lambda فالفوق", cible="centre:0"),
       dict(mot=f"L R égale {sci_dit(LR)} mètre", cible="centre:1")]),
    diapo_sim("ex_c6", "Question 4-2 : la pente, c'est λ", "θ = λ·(1/a) : plus λ est grande, plus la droite est inclinée.",
      f"{SIM}courbe.html?courbe=theta_inverse_a&depart=droite", "La pente de la droite θ = f(1/a) et l'identification k = λ",
      f"فla simulation، la droite ديال le laser rouge: la pente k égale six virgule cinq fois dix puissance moins sept mètre. "
      f"par identification، la pente ديال la droite teta en fonction de un sur a هي lambda. "
      f"فالتمرين، le laser vert عطانا k égale {sci_dit(K)} mètre. مع le laser rouge، la pente égale {sci_dit(lamR)} mètre: كبر. "
      f"إذن la droite ديال le rouge كتدوز حتى هي من l'origine، ولكن مايلة أكثر، فوق la droite ديال la figure deux.",
      [(f"k_R = λ_R = {sci(lamR)} m > k = {sci(K)} m", "مع le laser rouge"), ("droite par l'origine, plus inclinée", "مايلة أكثر")],
      [dict(mot="فla simulation، la droite", commande="play_until", parametres={"moment": "pente"}),
       dict(mot="la pente k égale", repere="pente"),
       dict(mot="par identification", commande="play_until", parametres={"moment": "identification"}),
       dict(mot="مع le laser rouge", cible="centre:0"),
       dict(mot="مايلة أكثر", cible="centre:1")]),
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    vf_facile("fa_c1", "Plus facile : vrai ou faux", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
      "Le triangle de la figure 1 : θ à la fente, D collé à θ.", [
        ("D'après la figure, tan θ = (L/2)/D.", True, "Le côté en face de θ est L/2 (du centre au bord de la tache), le côté collé est D."),
        ("D'après la figure, tan θ = L/D.", False, "θ va du centre de la tache à son bord : le côté opposé est L/2, pas L."),
        ("θ petit, en radian : tan θ ≈ θ, donc θ = L/(2D).", True, "C'est la dernière ligne de la démonstration.")]),
    qcm_facile("fa_c2", "Plus facile : quelle relation ?", "سؤال ساهل: اختار la relation اللي كتعطيها la courbe.",
      "La courbe θ = f(1/a) est une droite qui passe par l'origine. On peut écrire…",
      ["θ = k·a", "θ = k·(1/a)", "θ = k·(1/a) + b, avec b ≠ 0"], 1, {
        "1": {"juste": rep("برافو! droite كتدوز من l'origine: fonction linéaire، teta égale k fois un sur a.", "Juste : droite par l'origine, θ = k·(1/a).")},
        "0": {"1": rep("شوف l'axe اللي لتحت: c'est un sur a، ماشي a. عاود اختار.", "L'axe horizontal est 1/a, pas a. Réessaie."),
              "2": rep("الجواب: teta égale k fois un sur a. la droite كتدوز من l'origine، و l'axe des abscisses، c'est un sur a.", "Réponse : θ = k·(1/a) (l'abscisse est 1/a).")},
        "2": {"1": rep("شوف la droite: واش كتدوز من l'origine؟ يلا دازت، ما كاينش b. عاود اختار.", "La droite passe-t-elle par l'origine ? Alors pas de b. Réessaie."),
              "2": rep("الجواب: teta égale k fois un sur a. la droite كتدوز من l'origine، إذن fonction linéaire، بلا b.", "Réponse : θ = k·(1/a) : droite par l'origine, sans terme b.")}},
      "La courbe teta en fonction de un sur a est une droite qui passe par l'origine. On peut écrire ?"),
    qcm_facile("fa_c3", "Plus facile : lire la pente", "سؤال ساهل: اختار la valeur ديال lambda.",
      f"Le point A ({XA} × 10³ m⁻¹ ; {fr(YA)} × 10⁻³ rad) est sur la droite. La longueur d'onde vaut…",
      [f"λ = {fr(YA / XA, 2)} m", f"λ = {sci(NU_A)} m", f"λ = {LAM} nm"], 2, {
        "2": {"juste": rep(f"برافو! k égale delta teta sur delta un sur a، soit {sci_dit(K)} mètre، et lambda égale k: {entier(LAM)} nanomètres.",
                           f"Juste : k = ({fr(YA)} × 10⁻³)/({XA} × 10³) = {sci(K)} m = λ = {LAM} nm.")},
        "0": {"1": rep("قريب! ولكن نسيتي les facteurs ديال les axes: dix puissance moins trois et dix puissance trois. عاود اختار.",
                       "Tu as oublié les facteurs des axes : ×10⁻³ rad et ×10³ m⁻¹. Réessaie."),
              "2": rep(f"الجواب: k égale {dit(YA)} fois dix puissance moins trois، sur {entier(XA)} fois dix puissance trois، soit {sci_dit(K)} mètre، soit {entier(LAM)} nanomètres.",
                       f"Réponse : k = ({fr(YA)} × 10⁻³)/({XA} × 10³) = {sci(K)} m, donc λ = {LAM} nm.")},
        "1": {"1": rep("قلبتي القسمة: la pente هي delta teta sur delta un sur a، اللي فوق هو teta. عاود اختار.",
                       "La division est inversée : k = Δθ/Δ(1/a), θ au numérateur. Réessaie."),
              "2": rep(f"الجواب: k égale delta teta sur delta un sur a، soit {sci_dit(K)} mètre. و lambda égale k: {entier(LAM)} nanomètres.",
                       f"Réponse : k = Δθ/Δ(1/a) = {sci(K)} m = λ = {LAM} nm.")}},
      f"Le point A, un sur a égale {entier(XA)} fois dix puissance trois mètre puissance moins un، et teta égale {dit(YA)} fois dix puissance moins trois radian، est sur la droite. La longueur d'onde vaut ?"),
    qcm_facile("fa_c4", "Plus facile : la relation pour a'", "سؤال ساهل: اختار la relation ديال a prime.",
      f"λ = {LAM} nm, D = {fr(D)} m, L' = {fr(LP)} cm. Quelle relation donne a' ?",
      ["a' = L'/(2λD)", "a' = 2λD/L'", "a' = λD/L'"], 1, {
        "1": {"juste": rep(f"برافو! lambda sur a prime égale L prime sur deux D، إذن a prime égale deux lambda D sur L prime: {dit(A2MM, 3)} millimètre.",
                           f"Juste : a' = 2λD/L' = {fr(A2MM, 3)} mm.")},
        "0": {"1": rep("شوف la relation: lambda sur a prime égale L prime sur deux D. a prime فالتحت، إذن ملي كنخرجوها كتطلع، و L prime كتنزل. عاود اختار.",
                       "Pars de λ/a' = L'/(2D) et isole a' avec soin. Réessaie."),
              "2": rep(f"الجواب: a prime égale deux lambda D sur L prime، soit {dit(A2MM, 3)} millimètre.", f"Réponse : a' = 2λD/L' = {fr(A2MM, 3)} mm.")},
        "2": {"1": rep("قريب! ولكن تفكر: le côté opposé هو L sur deux، ماشي L. فين مشا le deux؟ عاود اختار.",
                       "Le côté opposé est L/2 : il manque le facteur 2. Réessaie."),
              "2": rep(f"الجواب: a prime égale deux lambda D sur L prime، soit {dit(A2MM, 3)} millimètre. نسيتي le deux.", f"Réponse : a' = 2λD/L' = {fr(A2MM, 3)} mm (le facteur 2 vient de L/2).")}},
      f"lambda égale {entier(LAM)} nanomètres، D égale {dit(D)} mètres، L prime égale {dit(LP)} centimètres. Quelle relation donne a prime ?"),
    qcm_facile("fa_c5", "Plus facile : la tache rouge", "سؤال ساهل: اختار la largeur ديال la tache الحمرا.",
      f"Même fente a', même D ; on passe de λ = {LAM} nm à λ_R = {LAMR} nm (avant : L' = {fr(LP)} cm). L_R vaut…",
      [f"L_R = {fr(LR * 100, 3)} cm", f"L_R = {fr(LR_INV, 2)} cm", f"L_R = {fr(LP)} cm"], 0, {
        "0": {"juste": rep(f"برافو! lambda كبرات، إذن L كبرات: L R égale {dit(LR * 100, 3)} centimètres.", f"Juste : L_R = 2λ_R·D/a' = {fr(LR * 100, 3)} cm.")},
        "1": {"1": rep("قلبتي le rapport: lambda كبرات، إذن L خاصها تكبر حتى هي. عاود اختار.", "λ augmente, donc L doit augmenter : ton rapport est inversé. Réessaie."),
              "2": rep(f"الجواب: L R égale deux lambda R D sur a prime، soit {dit(LR * 100, 3)} centimètres. lambda كبرات، إذن L كبرات.",
                       f"Réponse : L_R = {fr(LR * 100, 3)} cm (λ plus grande, tache plus large).")},
        "2": {"1": rep("L كتعلق ب lambda: L égale deux lambda D sur a. واش lambda تبدلات؟ عاود اختار.", "L = 2λD/a dépend de λ : λ a changé. Réessaie."),
              "2": rep(f"الجواب: L R égale {dit(LR * 100, 3)} centimètres. lambda تبدلات، إذن L تبدلات.", f"Réponse : L_R = {fr(LR * 100, 3)} cm, car λ a changé.")}},
      f"Même fente a prime، même D. lambda passe de {entier(LAM)} à {entier(LAMR)} nanomètres. Avant، L prime égale {dit(LP)} centimètres. L R vaut ?"),
    assoc_facile("fa_c6", "Plus facile : chaque laser, sa droite", "سؤال ساهل: ربط كل laser مع la droite ديالو.",
      "θ = λ·(1/a) : la pente de la droite est λ.", "Relie chaque laser à sa droite θ = f(1/a).",
      [("1", f"Laser vert, λ = {LAM} nm"), ("2", f"Laser rouge, λ_R = {LAMR} nm"), ("3", "Laser bleu, λ_B = 450 nm")],
      [("a", f"Droite de pente {sci(LAM * 1e-9)} m"), ("b", f"Droite de pente {sci(LAMR * 1e-9)} m, la plus inclinée"), ("c", "Droite de pente 4,5 × 10⁻⁷ m, la moins inclinée")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, f"Oui : la pente est λ = {LAM} nm = {sci(LAM * 1e-9)} m.", "برافو: la pente هي lambda ديال le laser vert."),
       "1-b": (False, "Cette pente correspond à 650 nm : ce n'est pas le laser vert.", "لا، هاد la pente كتساوي lambda ديال le laser rouge، ماشي le vert."),
       "1-c": (False, "Cette pente correspond à 450 nm : ce n'est pas le laser vert.", "لا، هاد la pente ديال le laser bleu، ماشي le vert."),
       "2-a": (False, "Le rouge a la plus grande λ : sa droite est la plus inclinée.", "لا، le rouge عندو أكبر lambda: la droite ديالو هي اللي مايلة أكثر."),
       "2-b": (True, "Oui : λ_R est la plus grande, donc la pente la plus grande.", "برافو: lambda R هي الكبيرة، إذن la pente هي الكبيرة."),
       "2-c": (False, "La droite la moins inclinée a la plus petite λ : c'est le bleu.", "لا، la droite اللي مايلة أقل عندها أصغر lambda: هادا le bleu."),
       "3-a": (False, "Cette pente correspond au laser vert.", "لا، هاد la pente ديال le laser vert."),
       "3-b": (False, "La plus inclinée est celle de la plus grande λ : le rouge.", "لا، اللي مايلة أكثر هي ديال أكبر lambda: le rouge."),
       "3-c": (True, "Oui : λ_B est la plus petite, donc la pente la plus petite.", "برافو: lambda B هي الصغيرة، إذن la pente هي الصغيرة.")},
      ("(1 ; a) (2 ; b) (3 ; c) : pour θ = f(1/a), la pente est λ.", "teta en fonction de un sur a: la pente هي lambda. كلما lambda كبيرة، كلما la droite مايلة أكثر.")),
  ]}]},
  "similaire": {
    "id": "phys_ex_ch3_courbe_3_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": (f"Même expérience avec un laser orange de longueur d'onde λ inconnue ; l'écran est à D = {fr(DB)} m de la fente. "
                f"Pour plusieurs fentes, on mesure L, on calcule θ et on trace θ = f(1/a) (figure 2). On prend tan θ ≈ θ."),
      "intro_dit": (f"نفس التمرين، بقيم أخرى. le laser orange، و lambda ما معروفاش. l'écran à la distance D égale {dit(DB)} mètre. "
                    f"كنرسمو teta en fonction de un sur a."),
      "figures": [montage(), FIGB],
      "donnees": [f"D = {fr(DB)} m", f"Point A de la droite : 1/a = {XAB} × 10³ m⁻¹ ; θ = {fr(YAB)} × 10⁻³ rad",
                  f"Question 3 : L' = {fr(LPB)} cm", f"Question 4 : λ_B = {LAM2B} nm", "1 nm = 10⁻⁹ m ; 1 mm = 10⁻³ m ; 1 cm = 10⁻² m"],
      "questions": [
        avec(RB["1"], id="1", texte="En s'aidant de la figure 1, montrer que θ = L/(2D)."),
        avec(RB["2-1"], id="2-1", texte="Justifier que la courbe de la figure 2 traduit une relation de la forme θ = k·(1/a)."),
        avec(RB["2-2"], id="2-2", texte="Déterminer k, puis, sachant que θ = λ/a, en déduire λ en nm."),
        avec(RB["3"], id="3", texte=f"Avec une fente de largeur inconnue a' (même laser, même D), on mesure L' = {fr(LPB)} cm. Déterminer a' en mm."),
        avec(RB["4-1"], id="4-1", texte=f"Même fente a', même écran ; on remplace le laser orange par un laser bleu, λ_B = {LAM2B} nm. Calculer, en cm, la largeur L_B de la tache centrale."),
        avec(RB["4-2"], id="4-2", texte="Avec le laser bleu, comment se place la droite θ = f(1/a) par rapport à celle de la figure 2 ? Justifier."),
      ]}},
}
# le semblable parle du laser bleu : L_B (et non L_R) dans ses corrections
for q in EX["similaire"]["enonce"]["questions"]:
    if q["id"] == "4-1":
        q["reponse"]["grandeur"] = "L_B"
        q["reponse"]["attendu"] = q["reponse"]["attendu"].replace("L_R", "L_B").replace("λ_R", "λ_B")
        q["clavier"]["pieges"][0] = q["clavier"]["pieges"][0].replace("L_R", "L_B")
        for l in q["correction"]["lignes"]:
            l["texte"] = l["texte"].replace("L_R", "L_B").replace("λ_R", "λ_B"); l["mot"] = l["mot"].replace("L R", "L B").replace("lambda R", "lambda B")
        q["correction"]["parole"] = q["correction"]["parole"].replace("L R", "L B").replace("lambda R", "lambda B")
controle_voix(EX)
ecrire(EX)
