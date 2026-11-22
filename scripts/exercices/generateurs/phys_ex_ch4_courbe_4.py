# Exercice moyen de physique (ch. 4, décroissance radioactive) : lire une courbe N(t) de sodium 24.
# Sources comparées (skill exercices § 2) :
#  - exploration radioactivite.json : cas_types « lecture_courbe » (N₀, N₀/2 → t½ ; τ par la tangente à l'origine),
#    « lambda_t_demi », « activite_date », « desintegres » ; pièges « lit λ là où la tangente coupe l'axe » (elle donne τ),
#    « confond N(t) restants et désintégrés », « unités ×10ⁿ de l'axe oubliées » ; erreurs_examen « lecture graphique ».
#  - nationaux comparés : 2021 N ex. 3 (a(t) du plutonium 238, t½ = 88 ans lue), 2022 N ex. 2 (a(t) de l'iode 131,
#    t½ = 8 jours lue, 95 % désintégrés), 2024 N ex. 3 (N_d de l'iridium 192), 2016 R (sodium 24 : énergie seulement,
#    sans courbe). Le nôtre : courbe N(t) (pas a(t)) du sodium 24, tangente à l'origine et τ (jamais demandés ainsi au
#    national récent), N à une date par le calcul ET la lecture, puis N_d : situation, données et chaîne différentes.
#  - séries en ligne (recherche du 22/11/2026, pages non ouvrables depuis cette session : talamidi.com, kezakoo.com
#    hors réseau ; seuls les extraits du moteur de recherche lus) : talamidi « décroissance radioactive exercices 4-7 »
#    (famille U 238, géochronologie), série N. Naceiri Mrabti (« déterminer graphiquement τ, relation λ–τ »),
#    exercice BIOF sodium 24 (t½ = 15 h, circulation sanguine), moutamadris 2ᵉ Bac SM (iode 131 / iode 123),
#    labolycée (tangente à l'origine → τ, λ = 1/τ).
import sys, os, math, importlib.util
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _outils import *

_ici = os.path.dirname(os.path.abspath(__file__))
_sp = importlib.util.spec_from_file_location("tp", os.path.join(_ici, "..", "..", "..", "backend", "kaggle_tts", "texte_parle.py"))
_tp = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(_tp)
nfr = _tp.nombre_fr


def dn(x, d=2):
    """Nombre dit en français : 21.64 -> « vingt et un virgule six quatre » est évité : « vingt et un virgule soixante-quatre »."""
    s = fr(x, d).replace("−", "")
    if "," not in s:
        return nfr(int(s))
    e, dec = s.split(",")
    reste = dec.lstrip("0")
    return nfr(int(e)) + " virgule" + " zéro" * (len(dec) - len(reste)) + (" " + nfr(int(reste)) if reste else "")


def ds(x, ch=3):
    """3.7e7 -> « trois virgule sept fois dix puissance sept » (mêmes arrondis que sci())."""
    e = math.floor(math.log10(abs(x)))
    m = round(x / 10 ** e, ch - 1)
    if abs(m) >= 10:
        m /= 10; e += 1
    t = dn(m, ch - 1)
    return t if e == 0 else f"{t} fois dix puissance {'moins ' if e < 0 else ''}{nfr(abs(e))}"


SIMC = "/media/simulations/physics/radioactivite-tableau/courbe.html"
SIMP = "/media/simulations/physics/radioactivite-tableau/population.html"
SIMF = "/media/simulations/physics/radioactivite-tableau/figures.html"
LN2 = math.log(2)


def donnees_ex(N0e, T, t1):
    """N0e = N₀ en unités de l'axe ; renvoie tout ce qui se calcule."""
    lam = LN2 / T
    tau = 1 / lam
    N1 = N0e * math.exp(-lam * t1)
    return dict(lam=lam, tau=tau, N1=N1, Nd=N0e - N1)


def figure(nom, N0e, T, tmax, xpas, ymax, unite_t, puiss, titre):
    lam = LN2 / T
    tau = 1 / lam
    return {"type": "courbe", "titre": titre,
            "legende": "La droite en pointillé est la tangente à la courbe à l'origine des dates.",
            "axes": {"x": {"min": 0, "max": tmax, "nom": "t", "unite": unite_t,
                           "graduations": [round(k * xpas, 3) for k in range(int(round(tmax / xpas)) + 1)]},
                     "y": {"min": 0, "max": ymax, "nom": "N", "unite": f"10{str(puiss).translate(str.maketrans('0123456789', '⁰¹²³⁴⁵⁶⁷⁸⁹'))} noyaux",
                           "graduations": list(range(0, ymax + 1))}},
            "elements": [
                {"f": "courbe", "expr": f"{N0e}*exp(-{lam:.6f}*x)", "de": 0, "a": tmax, "couleur": "orange"},
                {"f": "courbe", "expr": f"{N0e}-{N0e}*x/{tau:.4f}", "de": 0, "a": round(tau, 4), "couleur": "cyan", "trait": "pointille"},
                {"f": "texte", "at": [round(tau * 0.62, 3), round(N0e * 0.62, 3)], "t": "tangente à l'origine", "couleur": "cyan", "ancre": "gauche"},
                {"f": "texte", "at": [round(tmax * 0.55, 3), round(ymax * 0.8, 3)], "t": nom, "couleur": "orange", "ancre": "centre"}]}


# ---------------- données de l'exercice (sodium 24) ----------------
N0e, T, t1 = 6.0, 15.0, 36.0          # N₀ = 6,0·10¹⁹ noyaux ; t½ = 15 h ; t₁ = 36 h
D = donnees_ex(N0e, T, t1)
lam, tau, N1, Nd = D["lam"], D["tau"], D["N1"] * 1e19, D["Nd"] * 1e19
N0 = N0e * 1e19

# ---------------- données du semblable (bismuth 210) ----------------
N0e_b, T_b, t1_b = 4.0, 5.0, 8.0      # N₀ = 4,0·10²⁰ ; t½ = 5 jours ; t₁ = 8 jours
Db = donnees_ex(N0e_b, T_b, t1_b)
lam_b, tau_b, N1_b, Nd_b = Db["lam"], Db["tau"], Db["N1"] * 1e20, Db["Nd"] * 1e20
N0_b = N0e_b * 1e20

lamS = f"{lam:.4f}".replace(".", ",")          # 0,0462
lamS_b = f"{lam_b:.3f}".replace(".", ",")      # 0,139

Q = []
# ---- 1 : N₀
Q.append({"id": "1", "texte": "Lire graphiquement le nombre N₀ de noyaux de sodium 24 présents à la date t = 0.",
  "texte_dit": "السؤال un: اقرا على la courbe، le nombre N zéro ديال les noyaux de sodium vingt-quatre فt égale zéro.",
  "reponse": valeur("N₀", N0, "noyaux", f"N₀ = 6,0 × 10¹⁹ noyaux"),
  "clavier": {"aides": ["N₀", "t = 0", "× 10¹⁹", "noyaux"], "pieges": ["N₀ = 6 noyaux", "× 10²⁰"]},
  "aides": [aide("À t = 0, regarde où la courbe coupe l'axe des ordonnées.",
                 "شوف فين كتبدا la courbe، فt égale zéro: فين كتقطع l'axe ديال N؟"),
            aide("Lis la graduation, puis multiplie par l'unité de l'axe : 10¹⁹ noyaux.",
                 "اقرا la graduation، ومن بعد ضربها فl'unité ديال l'axe: dix puissance dix-neuf noyaux.")],
  "correction": correction([("1 : à t = 0, la courbe part de la graduation 6 de l'axe N (unité 10¹⁹ noyaux)", "la courbe كتبدا من la graduation"),
                            ("N₀ = 6,0 × 10¹⁹ noyaux", "N zéro égale six fois dix puissance dix-neuf noyaux")],
       "السؤال un. فt égale zéro، la courbe كتبدا من la graduation six ديال l'axe، و l'unité c'est dix puissance dix-neuf noyaux. إذن N zéro égale six fois dix puissance dix-neuf noyaux."),
  "explication": "ex_q1", "facile": "fa_q1"})
# ---- 2 : t½
Q.append({"id": "2", "texte": "Définir la demi-vie t½, puis la déterminer graphiquement.",
  "texte_dit": "السؤال deux: عرف la demi-vie t un demi، ومن بعد حددها على la courbe.",
  "reponse": valeur("t½", T, "h", f"N(t½) = N₀/2 = 3,0 × 10¹⁹ noyaux, on lit t½ = {fr(T)} h"),
  "clavier": {"aides": ["N(t½) = N₀/2", "N₀/2", "t½", "h"], "pieges": ["N(t½) = N₀/4", "t½ = τ"]},
  "aides": [aide("La demi-vie est la durée au bout de laquelle la moitié des noyaux initialement présents s'est désintégrée : que vaut alors N ?",
                 "la demi-vie هي la durée اللي من بعدها، la moitié des noyaux تفككات. شحال كيبقى ديال N فهاد اللحظة؟"),
            aide("Place N₀/2 = 3 × 10¹⁹ sur l'axe N, va horizontalement jusqu'à la courbe, puis descends sur l'axe des temps.",
                 "حط N zéro sur deux sur l'axe ديال N، سير أفقيا حتى ل la courbe، ومن بعد هبط ل l'axe des temps.")],
  "correction": correction([("2 : la demi-vie t½ est la durée au bout de laquelle la moitié des noyaux initialement présents s'est désintégrée", "la demi-vie، est la durée au bout de laquelle"),
                            ("N(t½) = N₀/2 = 3,0 × 10¹⁹ noyaux", "N de t un demi égale N zéro sur deux"),
                            (f"on lit t½ = {fr(T)} h", "t un demi égale quinze heures")],
       "السؤال deux. la demi-vie، est la durée au bout de laquelle، la moitié des noyaux initialement présents، s'est désintégrée. N de t un demi égale N zéro sur deux، égale trois fois dix puissance dix-neuf noyaux. كنمشيو أفقيا حتى ل la courbe، ومن بعد كنهبطو ل l'axe des temps: t un demi égale quinze heures."),
  "explication": "ex_q2", "facile": "fa_q2"})
# ---- 3 : λ
Q.append({"id": "3", "texte": "Calculer, en h⁻¹, la constante radioactive λ du sodium 24.",
  "texte_dit": "السؤال trois: حسب la constante radioactive lambda ديال le sodium vingt-quatre، ب heure puissance moins un.",
  "reponse": valeur("λ", lam, "h⁻¹", f"λ = (ln 2)/t½ = 0,693/{fr(T)} ≈ {lamS} h⁻¹"),
  "clavier": {"aides": ["λ = (ln 2)/t½", "ln 2 ≈ 0,693", "A.N. : λ = 0,693/15", "h⁻¹"], "pieges": ["λ = t½/(ln 2)", "λ = (ln 2)·t½", "h"]},
  "aides": [aide("λ et t½ sont liées par la relation établie dans le cours.",
                 "lambda و t un demi مربوطين بواحد la relation اللي برهنا فالدرس."),
            aide("t½ = (ln 2)/λ, donc λ = (ln 2)/t½ ; t½ en heures donne λ en h⁻¹.",
                 "t un demi égale ln deux sur lambda، إذن lambda égale ln deux sur t un demi. t un demi بالساعات، إذن lambda ب heure puissance moins un.")],
  "correction": correction([("3 : t½ = (ln 2)/λ donc λ = (ln 2)/t½", "lambda égale ln deux sur t un demi"),
                            (f"A.N. : λ = 0,693/{fr(T)}", "zéro virgule six cent quatre-vingt-treize sur quinze"),
                            (f"λ ≈ {lamS} h⁻¹", f"lambda égale environ {dn(lam, 4)} heure puissance moins un")],
       f"السؤال trois. t un demi égale ln deux sur lambda، إذن lambda égale ln deux sur t un demi. l'application numérique: zéro virgule six cent quatre-vingt-treize sur quinze. lambda égale environ {dn(lam, 4)} heure puissance moins un."),
  "explication": "ex_q3", "facile": "fa_q3"})
# ---- 4 : τ
Q.append({"id": "4", "texte": "La tangente à la courbe à l'origine coupe l'axe des temps à la date τ (constante de temps). Lire τ, puis vérifier que τ = 1/λ.",
  "texte_dit": "السؤال quatre: la tangente à l'origine كتقطع l'axe des temps فla date tau، la constante de temps. اقرا tau، ومن بعد تأكد بلي tau égale un sur lambda.",
  "reponse": valeur("τ", tau, "h", f"τ = 1/λ = 1/{lamS} ≈ {fr(tau, 1)} h", tolerance=0.05),
  "clavier": {"aides": ["τ = 1/λ", "tangente", "A.N. : τ = 1/0,0462", "h"], "pieges": ["λ = τ", "τ = t½", "τ = (ln 2)/λ"]},
  "aides": [aide("Suis la droite en pointillé jusqu'à l'axe des temps : ce point donne τ, pas λ.",
                 "تبع la droite en pointillé حتى ل l'axe des temps. هاد النقطة كتعطي tau، ماشي lambda."),
            aide("Pour vérifier, calcule 1/λ avec le λ de la question 3 et compare avec la lecture.",
                 "باش تتأكد، حسب la valeur de un sur lambda، مع lambda de la question trois، وقارنها مع القراءة.")],
  "correction": correction([("4 : la tangente à l'origine coupe l'axe des temps à τ ≈ 21,6 h (lecture)", "la tangente à l'origine كتقطع l'axe des temps"),
                            (f"calcul : τ = 1/λ = 1/{lamS} ≈ {fr(tau, 1)} h", "tau égale un sur lambda"),
                            ("la lecture et le calcul concordent : τ = 1/λ est vérifiée", "القراءة والحساب متافقين")],
       f"السؤال quatre. la tangente à l'origine كتقطع l'axe des temps، à environ vingt et un virgule six heures. بالحساب: tau égale un sur lambda، égale un sur {dn(lam, 4)}، égale environ {dn(tau, 1)} heures. القراءة والحساب متافقين: tau égale un sur lambda."),
  "explication": "ex_q4", "facile": "fa_q4"})
# ---- 5 : N(t₁)
Q.append({"id": "5", "texte": f"En utilisant la loi de décroissance, calculer le nombre N₁ de noyaux de sodium 24 restants à la date t₁ = {fr(t1)} h. Comparer avec la valeur lue sur la courbe.",
  "texte_dit": f"السؤال cinq: بla loi de décroissance، حسب le nombre N un ديال les noyaux اللي باقيين فt un égale trente-six heures. قارنو مع القيمة اللي كتقراها على la courbe.",
  "reponse": valeur("N₁", N1, "noyaux", f"N₁ = N₀·e^(−λ·t₁) = 6,0 × 10¹⁹ × e^(−{lamS} × {fr(t1)}) ≈ {sci(N1, 3)} noyaux"),
  "clavier": {"aides": ["N(t) = N₀·e^(−λt)", "e^(−λ·t₁)", "A.N. : 6,0 × 10¹⁹ × e^(−0,0462 × 36)", "noyaux"], "pieges": ["N = N₀·e^(λt)", "N = N₀ − λ·t", "N = N₀/2"]},
  "aides": [aide("t₁ = 36 h est entre 2t½ = 30 h et 3t½ = 45 h : N₁ est entre N₀/4 et N₀/8.",
                 "t un égale trente-six heures، entre deux t un demi et trois t un demi. إذن N un كاين entre N zéro sur quatre et N zéro sur huit."),
            aide("Applique N(t) = N₀·e^(−λt) avec λ en h⁻¹ et t₁ en heures, puis lis la courbe à t = 36 h.",
                 "طبق N de t égale N zéro exponentielle moins lambda t، ب lambda ب heure puissance moins un و t un بالساعات. ومن بعد اقرا la courbe à trente-six heures.")],
  "correction": correction([("5 : N(t) = N₀·e^(−λt)", "N de t égale N zéro exponentielle moins lambda t"),
                            (f"A.N. : N₁ = 6,0 × 10¹⁹ × e^(−{lamS} × {fr(t1)})", "six fois dix puissance dix-neuf fois exponentielle"),
                            (f"N₁ ≈ {sci(N1, 3)} noyaux", f"N un égale environ {ds(N1, 3)} noyaux"),
                            ("sur la courbe, à t = 36 h, on lit N ≈ 1,1 × 10¹⁹ : la lecture confirme le calcul", "على la courbe")],
       f"السؤال cinq. la loi: N de t égale N zéro exponentielle moins lambda t. l'application numérique: six fois dix puissance dix-neuf fois exponentielle moins {dn(lam, 4)} fois trente-six. N un égale environ {ds(N1, 3)} noyaux. على la courbe، à trente-six heures، كنقراو environ un virgule un fois dix puissance dix-neuf: القراءة كتأكد الحساب."),
  "explication": "ex_q5", "facile": "fa_q5"})
# ---- 6 : N_d
Q.append({"id": "6", "texte": "En déduire le nombre N_d de noyaux de sodium 24 désintégrés entre les dates 0 et t₁.",
  "texte_dit": "السؤال six: استنتج le nombre N d ديال les noyaux de sodium vingt-quatre اللي تفككو entre zéro et t un.",
  "reponse": valeur("N_d", Nd, "noyaux", f"N_d = N₀ − N₁ = 6,0 × 10¹⁹ − {sci(N1, 3)} ≈ {sci(Nd, 3)} noyaux"),
  "clavier": {"aides": ["N_d = N₀ − N(t)", "N₀", "N₁", "noyaux"], "pieges": ["N_d = N₁", "N_d = N₀ + N₁"]},
  "aides": [aide("Attention au mot « désintégrés » : N₁ compte les noyaux qui RESTENT.",
                 "رد البال ل la question: كتسول على les désintégrés. N un هوما les noyaux اللي باقيين."),
            aide("Les désintégrés sont ceux qui sont partis : N_d = N₀ − N₁.",
                 "les désintégrés هوما اللي مشاو: N d égale N zéro moins N un.")],
  "correction": correction([("6 : N_d = N₀ − N₁", "N d égale N zéro moins N un"),
                            (f"A.N. : N_d = 6,0 × 10¹⁹ − {sci(N1, 3)}", "six fois dix puissance dix-neuf moins"),
                            (f"N_d ≈ {sci(Nd, 3)} noyaux désintégrés", f"N d égale environ {ds(Nd, 3)} noyaux")],
       f"السؤال six. les désintégrés هوما اللي مشاو: N d égale N zéro moins N un. l'application numérique: six fois dix puissance dix-neuf moins {ds(N1, 3)}. N d égale environ {ds(Nd, 3)} noyaux."),
  "explication": "ex_q6", "facile": "fa_q6"})

# ---------------- explication animée ----------------
EXP = [
  diapo_sim("ex_q1", "Question 1 : lire N₀ sur l'axe", "À t = 0, la courbe part de N₀ ; l'axe est gradué en 10ⁿ noyaux.",
    SIMC + "?courbe=N", "La courbe N(t) du cours : N₀ lu sur l'axe",
    "شوف la courbe N en fonction de t ديال الدرس. على l'axe ديال N، l'unité c'est dix puissance vingt noyaux. فt égale zéro، كنقراو N zéro فالبداية ديال la courbe: huit virgule zéro fois dix puissance vingt noyaux. رد البال: الرقم اللي كنقراو، خاصو يتضرب فl'unité ديال l'axe. فالتمرين، l'unité c'est dix puissance dix-neuf noyaux، وla courbe كتبدا à six. إذن N zéro égale six fois dix puissance dix-neuf noyaux.",
    [("N₀ = 6,0 × 10¹⁹ noyaux", "إذن N zéro égale six fois dix puissance dix-neuf noyaux")],
    [dict(mot="شوف la courbe", commande="play_until", parametres={"moment": "courbe"}),
     dict(mot="على l'axe ديال N", repere="axe_N"),
     dict(mot="كنقراو N zéro", commande="play_until", parametres={"moment": "N0"}),
     dict(mot="خاصو يتضرب", repere="N0"),
     dict(mot="إذن N zéro égale six", cible="centre:0")]),
  diapo_sim("ex_q2", "Question 2 : t½ lue à N₀/2", "N(t½) = N₀/2 : horizontale jusqu'à la courbe, puis verticale vers l'axe des temps.",
    SIMC + "?courbe=N", "N₀/2, puis t½ sur l'axe des temps",
    "كناخدو النص ديال N zéro: فالدرس، c'est quatre fois dix puissance vingt noyaux. كنمشيو أفقيا حتى ل la courbe، ومن بعد كنهبطو ل l'axe des temps. كنقراو t un demi égale huit jours. نعاود نقرا la définition: la demi-vie، est la durée au bout de laquelle، la moitié des noyaux initialement présents، s'est désintégrée. فالتمرين، N zéro sur deux égale trois fois dix puissance dix-neuf noyaux، وكنقراو t un demi égale quinze heures.",
    [("N(t½) = N₀/2", "كناخدو النص ديال N zéro"), ("t½ = 15 h", "t un demi égale quinze heures")],
    [dict(mot="كناخدو النص", commande="play_until", parametres={"moment": "moitie"}),
     dict(mot="كنمشيو أفقيا", repere="moitie"),
     dict(mot="كنقراو t un demi", commande="play_until", parametres={"moment": "t_demi"}),
     dict(mot="كنقراو t un demi", repere="t_demi"),
     dict(mot="كناخدو النص ديال N zéro", cible="centre:0"),
     dict(mot="t un demi égale quinze heures", cible="centre:1")]),
  diapo_sim("ex_q3", "Question 3 : λ à partir de t½", "t½ = (ln 2)/λ, donc λ = (ln 2)/t½, dans l'inverse de l'unité de t½.",
    SIMF + "?fig=fig_demo_t_demi", "La démonstration de t½ = (ln 2)/λ",
    "نتفكرو كيفاش برهنا la relation. la loi: N de t égale N zéro exponentielle moins lambda t. فt un demi، N égale N zéro sur deux. N zéro كيمشي، وكندخلو ln: moins lambda t un demi égale moins ln deux. إذن t un demi égale ln deux sur lambda. نقلبوها: lambda égale ln deux sur t un demi. فالتمرين، t un demi égale quinze heures، إذن lambda égale zéro virgule six cent quatre-vingt-treize sur quinze، égale environ " + dn(lam, 4) + " heure puissance moins un. t un demi بالساعات، إذن lambda ب heure puissance moins un.",
    [("λ = (ln 2)/t½", "lambda égale ln deux sur t un demi"), (f"λ = 0,693/15 ≈ {lamS} h⁻¹", "égale environ " + dn(lam, 4) + " heure puissance moins un")],
    [dict(mot="la loi: N de t", commande="play_until", parametres={"moment": "loi"}),
     dict(mot="فt un demi، N égale", commande="play_until", parametres={"moment": "condition"}),
     dict(mot="N zéro كيمشي", commande="play_until", parametres={"moment": "ln"}),
     dict(mot="إذن t un demi égale ln deux sur lambda", commande="play_until", parametres={"moment": "resultat"}),
     dict(mot="lambda égale ln deux sur t un demi", cible="centre:0"),
     dict(mot="égale environ " + dn(lam, 4) + " heure puissance moins un", cible="centre:1")]),
  diapo_sim("ex_q4", "Question 4 : la tangente à l'origine donne τ", "La tangente à l'origine coupe l'axe des temps en τ = 1/λ (pas en λ).",
    SIMC + "?courbe=N", "La tangente à l'origine et τ",
    "على la courbe، كنرسمو la tangente à l'origine. كتقطع l'axe des temps فواحد النقطة: هي tau، la constante de temps. فالدرس، tau égale onze virgule cinq jours. رد البال: هاد النقطة كتعطي tau، ماشي lambda. و tau égale un sur lambda. فالتمرين، كنقراو tau à environ vingt et un virgule six heures. بالحساب: tau égale un sur " + dn(lam, 4) + "، égale environ " + dn(tau, 1) + " heures. نفس النتيجة.",
    [("τ = 1/λ", "و tau égale un sur lambda"), (f"τ = 1/{lamS} ≈ {fr(tau, 1)} h", "égale environ " + dn(tau, 1) + " heures")],
    [dict(mot="كنرسمو la tangente", commande="play_until", parametres={"moment": "tangente"}),
     dict(mot="كتقطع l'axe des temps", commande="play_until", parametres={"moment": "tau"}),
     dict(mot="هي tau، la constante de temps", repere="tau"),
     dict(mot="و tau égale un sur lambda", cible="centre:0"),
     dict(mot="égale environ " + dn(tau, 1) + " heures", cible="centre:1")]),
  diapo_sim("ex_q5", "Question 5 : N à une date, par la loi et sur la courbe", "N(t) = N₀·e^(−λt) ; aux paliers t = n·t½, N = N₀/2ⁿ.",
    SIMC + "?courbe=paliers", "Les paliers N₀/2, N₀/4, N₀/8 et la loi",
    "فكل demi-vie، N كيتقسم sur deux. après deux demi-vies: N zéro sur quatre. après trois demi-vies: N zéro sur huit. ولكن la date ديال التمرين ماشي palier. إذن كنحسبو ب la loi: N de t égale N zéro exponentielle moins lambda t. فالتمرين، t un égale trente-six heures، entre deux t un demi et trois t un demi. N un égale six fois dix puissance dix-neuf fois exponentielle moins " + dn(lam, 4) + " fois trente-six، égale environ " + ds(N1, 3) + " noyaux. هادشي بين N zéro sur quatre و N zéro sur huit، وla courbe كتعطي نفس الشي.",
    [("N(t) = N₀·e^(−λt)", "N de t égale N zéro exponentielle moins lambda t"), (f"N₁ ≈ {sci(N1, 3)} noyaux", "égale environ " + ds(N1, 3) + " noyaux")],
    [dict(mot="فكل demi-vie", commande="play_until", parametres={"moment": "palier_1"}),
     dict(mot="après deux demi-vies", commande="play_until", parametres={"moment": "palier_2"}),
     dict(mot="après trois demi-vies", commande="play_until", parametres={"moment": "palier_3"}),
     dict(mot="إذن كنحسبو ب la loi", commande="play_until", parametres={"moment": "formule"}),
     dict(mot="N de t égale N zéro exponentielle moins lambda t", cible="centre:0"),
     dict(mot="égale environ " + ds(N1, 3) + " noyaux", cible="centre:1")]),
  diapo_sim("ex_q6", "Question 6 : restants et désintégrés", "N(t) compte les restants ; les désintégrés : N_d = N₀ − N(t).",
    SIMP + "?vue=restants", "Deux courbes : les restants et les désintégrés",
    "شوف les deux courbes: les restants كيهبطو، و les désintégrés كيطلعو. كيتلاقاو فt un demi، ملي كيبقى النص. من بعد، كيبقى الربع، وتلاتة ديال الأرباع désintégrés. la formule: N d égale N zéro moins N de t. فالتمرين، N d égale six fois dix puissance dix-neuf moins " + ds(N1, 3) + "، égale environ " + ds(Nd, 3) + " noyaux désintégrés.",
    [("N_d = N₀ − N(t)", "N d égale N zéro moins N de t"), (f"N_d ≈ {sci(Nd, 3)} noyaux", "égale environ " + ds(Nd, 3) + " noyaux désintégrés")],
    [dict(mot="شوف les deux courbes", repere="courbe_restants"),
     dict(mot="كيتلاقاو فt un demi", commande="play_until", parametres={"moment": "croisement"}),
     dict(mot="من بعد، كيبقى الربع", commande="play_until", parametres={"moment": "deux_t_demi"}),
     dict(mot="la formule:", commande="play_until", parametres={"moment": "formule"}),
     dict(mot="N d égale N zéro moins N de t", cible="centre:0"),
     dict(mot="égale environ " + ds(Nd, 3) + " noyaux désintégrés", cible="centre:1")]),
]

# ---------------- version facile ----------------
FAC = [
  qcm_facile("fa_q1", "Plus facile : lire avec l'unité de l'axe", "نتمرنو بسؤال ساهل. اختار la bonne lecture.",
    "Sur l'axe N (unité 10¹⁹ noyaux), la courbe part de la graduation 6. N₀ vaut…",
    ["6 noyaux", "6,0 × 10²⁰ noyaux", "6,0 × 10¹⁹ noyaux"], 2, {
      "2": {"juste": rep("مزيان! la graduation six كتضرب فl'unité ديال l'axe: N zéro égale six fois dix puissance dix-neuf noyaux.", "Juste : N₀ = 6 × 10¹⁹ = 6,0 × 10¹⁹ noyaux.")},
      "0": {"1": rep("قريب، ولكن نسيتي l'unité ديال l'axe. شوف شنو مكتوب حدا N. عاود اختار.", "Tu as oublié l'unité de l'axe (10¹⁹ noyaux). Réessaie."),
            "2": rep("الجواب: N zéro égale six fois dix puissance dix-neuf noyaux. la graduation six كتضرب فl'unité ديال l'axe.", "Réponse : N₀ = 6,0 × 10¹⁹ noyaux (graduation × unité de l'axe).")},
      "1": {"1": rep("شوف مزيان la puissance de dix فl'unité ديال l'axe. عاود اختار.", "Relis la puissance de 10 écrite sur l'axe. Réessaie."),
            "2": rep("الجواب: N zéro égale six fois dix puissance dix-neuf noyaux، حيت l'unité c'est dix puissance dix-neuf، pas vingt.", "Réponse : 6,0 × 10¹⁹ noyaux : l'axe est en 10¹⁹, pas en 10²⁰.")}},
    "Sur l'axe N, l'unité est dix puissance dix-neuf noyaux, et la courbe part de la graduation six. N zéro vaut ?"),
  vf_facile("fa_q2", "Plus facile : la demi-vie", "سؤال ساهل على la demi-vie: قول واش كل جملة صحيحة ولا غالطة.",
    "N₀ = 6,0 × 10¹⁹ noyaux.", [
      ("À la date t½, il reste N₀/2 = 3,0 × 10¹⁹ noyaux.", True, "Par définition, à t½ la moitié des noyaux s'est désintégrée : il en reste N₀/2."),
      ("À la date t½, il ne reste plus aucun noyau.", False, "À t½, il reste la moitié : N₀/2 = 3,0 × 10¹⁹ noyaux."),
      ("Pour lire t½, on place N₀/2 sur l'axe N, on va jusqu'à la courbe, puis on descend sur l'axe des temps.", True, "C'est la lecture graphique de t½.")]),
  qcm_facile("fa_q3", "Plus facile : la relation λ–t½", "سؤال ساهل: اختار la bonne relation.",
    "t½ = 15 h. Quelle relation donne la constante radioactive ?",
    ["λ = t½/(ln 2)", "λ = (ln 2)/t½", "λ = (ln 2)·t½"], 1, {
      "1": {"juste": rep("برافو! lambda égale ln deux sur t un demi، égale zéro virgule six cent quatre-vingt-treize sur quinze.", "Juste : λ = (ln 2)/t½ = 0,693/15 ≈ 0,0462 h⁻¹.")},
      "0": {"1": rep("شوف l'unité: lambda خاصها تكون ب heure puissance moins un. t un demi sur ln deux كتعطي des heures. عاود اختار.", "Cette relation donne des heures, pas des h⁻¹. Réessaie."),
            "2": rep("الجواب هو lambda égale ln deux sur t un demi. t un demi تحت، باش lambda تكون ب heure puissance moins un.", "Réponse : λ = (ln 2)/t½ (t½ au dénominateur, λ en h⁻¹).")},
      "2": {"1": rep("قريب، ولكن الضرب كيعطي des heures. خاص t un demi تكون تحت. عاود اختار.", "Un produit par t½ donne des heures. Réessaie."),
            "2": rep("الجواب هو lambda égale ln deux sur t un demi، ماشي fois t un demi.", "Réponse : λ = (ln 2)/t½, on divise par t½.")}},
    "t un demi égale quinze heures. Quelle relation donne la constante radioactive ?"),
  assoc_facile("fa_q4", "Plus facile : que lit-on sur la courbe ?", "سؤال ساهل: ربط كل قراءة على la courbe مع la grandeur ديالها.",
    "Trois lectures sur la courbe N(t).", "Relie chaque lecture à la grandeur qu'elle donne.",
    [("1", "point où la tangente à l'origine coupe l'axe des temps"), ("2", "date où N = N₀/2"), ("3", "ordonnée de la courbe à t = 0")],
    [("a", "la constante de temps τ"), ("b", "la demi-vie t½"), ("c", "le nombre initial N₀")],
    {"1": "a", "2": "b", "3": "c"}, {
      "1-a": (True, "Juste : la tangente à l'origine coupe l'axe des temps en τ = 1/λ.", "صحيح: la tangente à l'origine كتقطع l'axe des temps ف tau، و tau égale un sur lambda."),
      "1-b": (False, "Non : t½ se lit à N₀/2, pas avec la tangente. Cherche la grandeur liée à la tangente.", "لا: t un demi كتقرا ف N zéro sur deux، ماشي ب la tangente. قلب على la grandeur ديال la tangente."),
      "1-c": (False, "Non : N₀ est sur l'axe N, la tangente coupe l'axe des temps : c'est une durée.", "لا: la tangente كتقطع l'axe des temps، إذن هي durée، ماشي N zéro."),
      "2-a": (False, "Non : N₀/2 donne une autre durée que τ. Relis la définition de la demi-vie.", "لا: N zéro sur deux كتعطي durée أخرى. عاود قرا la définition ديال la demi-vie."),
      "2-b": (True, "Juste : à t½, il reste la moitié des noyaux, N = N₀/2.", "صحيح: فt un demi، كيبقى النص، N égale N zéro sur deux."),
      "2-c": (False, "Non : N₀/2 est la moitié de N₀, la date où on l'atteint est une durée.", "لا: N zéro sur deux هي النص ديال N zéro. la date ديالها هي durée."),
      "3-a": (False, "Non : à t = 0, on lit un nombre de noyaux, pas une durée.", "لا: فt égale zéro، كنقراو عدد ديال les noyaux، ماشي durée."),
      "3-b": (False, "Non : à t = 0, on lit un nombre de noyaux, pas une durée.", "لا: فt égale zéro، كنقراو عدد ديال les noyaux، ماشي durée."),
      "3-c": (True, "Juste : à t = 0, la courbe part de N₀.", "صحيح: فt égale zéro، la courbe كتبدا من N zéro.")},
    ("(1 ; a) (2 ; b) (3 ; c). Attention : la tangente donne τ, et λ = 1/τ.", "رد البال: la tangente كتعطي tau، و lambda égale un sur tau.")),
  qcm_facile("fa_q5", "Plus facile : entre deux paliers", "سؤال ساهل: فين كاين N un؟",
    "t½ = 15 h et t₁ = 36 h. Le nombre N₁ de noyaux restants est…",
    ["entre N₀/2 et N₀/4", "entre N₀/4 et N₀/8", "plus petit que N₀/8"], 1, {
      "1": {"juste": rep("مزيان! t un égale trente-six heures، entre trente et quarante-cinq heures، c'est entre deux et trois demi-vies. إذن N un كاين entre N zéro sur quatre و N zéro sur huit.", "Juste : 2t½ = 30 h < 36 h < 3t½ = 45 h, donc N₀/8 < N₁ < N₀/4.")},
      "0": {"1": rep("حسب la valeur de deux t un demi: trente heures. واش t un كاين avant ولا après؟ عاود اختار.", "Calcule 2t½ = 30 h : 36 h est-il avant ou après ? Réessaie."),
            "2": rep("الجواب: entre N zéro sur quatre et N zéro sur huit. t un كاين après deux demi-vies et avant trois.", "Réponse : entre N₀/4 et N₀/8, car 30 h < 36 h < 45 h.")},
      "2": {"1": rep("حسب la valeur de trois t un demi: quarante-cinq heures. واش وصلنا ليها؟ عاود اختار.", "Calcule 3t½ = 45 h : y est-on déjà ? Réessaie."),
            "2": rep("الجواب: entre N zéro sur quatre et N zéro sur huit. t un كاين avant trois demi-vies، إذن ما وصلناش ل N zéro sur huit.", "Réponse : entre N₀/4 et N₀/8 : 36 h < 3t½ = 45 h.")}},
    "t un demi égale quinze heures et t un égale trente-six heures. Le nombre N un de noyaux restants est ?"),
  vf_facile("fa_q6", "Plus facile : restants ou désintégrés ?", "سؤال ساهل: قول واش صحيحة ولا غالطة.",
    "N₀ = 6,0 × 10¹⁹ et N₁ = 1,1 × 10¹⁹ noyaux restants.", [
      ("Le nombre de noyaux désintégrés est N₁ = 1,1 × 10¹⁹.", False, "N₁ compte les noyaux restants ; les désintégrés : N_d = N₀ − N₁."),
      ("Le nombre de noyaux désintégrés est N_d = N₀ − N₁ ≈ 4,9 × 10¹⁹.", True, "Les désintégrés sont ceux qui sont partis : N₀ − N₁."),
      ("N₁ + N_d = N₀.", True, "Restants + désintégrés = noyaux de départ.")]),
]

# ---------------- similaire (bismuth 210) ----------------
lamb_txt = lamS_b
QB = [
  {"id": "1", "texte": "Lire graphiquement le nombre N₀ de noyaux de bismuth 210 à t = 0.",
   "reponse": valeur("N₀", N0_b, "noyaux", "N₀ = 4,0 × 10²⁰ noyaux"),
   "clavier": {"aides": ["N₀", "t = 0", "× 10²⁰", "noyaux"], "pieges": ["N₀ = 4 noyaux"]},
   "correction": correction([("1 : à t = 0, la courbe part de la graduation 4 (unité 10²⁰ noyaux)", "la courbe كتبدا من la graduation quatre"),
                             ("N₀ = 4,0 × 10²⁰ noyaux", "N zéro égale quatre fois dix puissance vingt noyaux")],
        "فt égale zéro، la courbe كتبدا من la graduation quatre. إذن N zéro égale quatre fois dix puissance vingt noyaux.")},
  {"id": "2", "texte": "Définir la demi-vie t½, puis la déterminer graphiquement.",
   "reponse": valeur("t½", T_b, "jours", f"N(t½) = N₀/2 = 2,0 × 10²⁰ noyaux, on lit t½ = {fr(T_b)} jours"),
   "clavier": {"aides": ["N(t½) = N₀/2", "t½", "jours"], "pieges": ["N(t½) = N₀/4"]},
   "correction": correction([("2 : t½ : durée au bout de laquelle la moitié des noyaux initialement présents s'est désintégrée", "la moitié des noyaux"),
                             (f"N(t½) = N₀/2 = 2,0 × 10²⁰ ; on lit t½ = {fr(T_b)} jours", "t un demi égale cinq jours")],
        "la demi-vie، est la durée au bout de laquelle، la moitié des noyaux initialement présents، s'est désintégrée. N zéro sur deux égale deux fois dix puissance vingt، وكنقراو t un demi égale cinq jours.")},
  {"id": "3", "texte": "Calculer, en jour⁻¹, la constante radioactive λ du bismuth 210.",
   "reponse": valeur("λ", lam_b, "jour⁻¹", f"λ = (ln 2)/t½ = 0,693/{fr(T_b)} ≈ {lamb_txt} jour⁻¹"),
   "clavier": {"aides": ["λ = (ln 2)/t½", "jour⁻¹"], "pieges": ["λ = t½/(ln 2)"]},
   "correction": correction([("3 : λ = (ln 2)/t½ = 0,693/5", "lambda égale ln deux sur t un demi"), (f"λ ≈ {lamb_txt} jour⁻¹", f"environ {dn(lam_b, 3)} jour puissance moins un")],
        f"lambda égale ln deux sur t un demi، égale zéro virgule six cent quatre-vingt-treize sur cinq، égale environ {dn(lam_b, 3)} jour puissance moins un.")},
  {"id": "4", "texte": "La tangente à l'origine coupe l'axe des temps à la date τ. Lire τ, puis vérifier que τ = 1/λ.",
   "reponse": valeur("τ", tau_b, "jours", f"τ = 1/λ = 1/{lamb_txt} ≈ {fr(tau_b, 1)} jours", tolerance=0.05),
   "clavier": {"aides": ["τ = 1/λ", "jours"], "pieges": ["λ = τ", "τ = t½"]},
   "correction": correction([("4 : lecture : τ ≈ 7,2 jours", "كنقراو tau"), (f"τ = 1/λ = 1/{lamb_txt} ≈ {fr(tau_b, 1)} jours : vérifié", "tau égale un sur lambda")],
        f"كنقراو tau à environ sept virgule deux jours. بالحساب: tau égale un sur lambda، égale environ {dn(tau_b, 1)} jours. متافقين.")},
  {"id": "5", "texte": f"Calculer, par la loi de décroissance, le nombre N₁ de noyaux restants à t₁ = {fr(t1_b)} jours ; comparer avec la lecture.",
   "reponse": valeur("N₁", N1_b, "noyaux", f"N₁ = N₀·e^(−λ·t₁) = 4,0 × 10²⁰ × e^(−{lamb_txt} × {fr(t1_b)}) ≈ {sci(N1_b, 3)} noyaux"),
   "clavier": {"aides": ["N(t) = N₀·e^(−λt)", "noyaux"], "pieges": ["N = N₀·e^(λt)"]},
   "correction": correction([("5 : N₁ = N₀·e^(−λ·t₁)", "N un égale N zéro exponentielle moins lambda t un"),
                             (f"N₁ ≈ {sci(N1_b, 3)} noyaux, ce que confirme la courbe", "environ " + ds(N1_b, 3) + " noyaux")],
        f"N un égale N zéro exponentielle moins lambda t un، égale quatre fois dix puissance vingt fois exponentielle moins {dn(lam_b, 3)} fois huit. N un égale environ {ds(N1_b, 3)} noyaux، وla courbe كتأكد.")},
  {"id": "6", "texte": "En déduire le nombre N_d de noyaux désintégrés entre 0 et t₁.",
   "reponse": valeur("N_d", Nd_b, "noyaux", f"N_d = N₀ − N₁ = 4,0 × 10²⁰ − {sci(N1_b, 3)} ≈ {sci(Nd_b, 3)} noyaux"),
   "clavier": {"aides": ["N_d = N₀ − N(t)", "noyaux"], "pieges": ["N_d = N₁"]},
   "correction": correction([("6 : N_d = N₀ − N₁", "N d égale N zéro moins N un"), (f"N_d ≈ {sci(Nd_b, 3)} noyaux", "environ " + ds(Nd_b, 3) + " noyaux")],
        f"N d égale N zéro moins N un، égale environ {ds(Nd_b, 3)} noyaux.")},
]

EX = {
  "id": "phys_ex_ch4_courbe_4", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "radioactivite", "cours": "phys_ch4_radioactivite",
  "titre": "Lire la courbe de décroissance du sodium 24", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre ou d'une série).",
  "competences": ["Lire N₀ et t½ sur une courbe N(t)", "Calculer λ = (ln 2)/t½", "Lire τ sur la tangente à l'origine, τ = 1/λ",
                  "Calculer N(t) = N₀·e^(−λt)", "Calculer le nombre de noyaux désintégrés N_d = N₀ − N(t)"],
  "enonce": {
    "intro": "Le sodium 24 (²⁴₁₁Na) est radioactif β⁻ ; on l'utilise en médecine pour suivre la circulation du sang. On étudie un échantillon de sodium 24 à partir d'une date choisie comme origine (t = 0). La figure représente l'évolution du nombre N de noyaux de sodium 24 restants en fonction du temps, et la tangente à la courbe à l'origine (en pointillé).",
    "intro_dit": "دابا نقراو l'énoncé. le sodium vingt-quatre radioactif bêta moins، كيستعملوه فالطب باش يتبعو الدم فالجسم. عندنا un échantillon de sodium vingt-quatre، من t égale zéro. la figure كتبين N en fonction de t: le nombre ديال les noyaux de sodium اللي باقيين. ومرسومة حتى la tangente à l'origine، en pointillé.",
    "figures": [figure("sodium 24", N0e, T, 75, 5, 7, "h", 19, "Nombre N de noyaux de sodium 24 restants en fonction du temps")],
    "donnees": ["ln 2 ≈ 0,693", f"t₁ = {fr(t1)} h (question 5)"],
    "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXP}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FAC}]},
  "similaire": {"id": "phys_ex_ch4_courbe_4_b", "titre": "Même exercice, autres données : le bismuth 210",
    "enonce": {
      "intro": "Le bismuth 210 (²¹⁰₈₃Bi) est radioactif β⁻. La figure représente l'évolution du nombre N de noyaux de bismuth 210 restants dans un échantillon en fonction du temps, et la tangente à la courbe à l'origine (en pointillé).",
      "intro_dit": "نفس التمرين، بقيم أخرى. le bismuth deux cent dix radioactif bêta moins. la figure كتبين N en fonction de t، مع la tangente à l'origine en pointillé.",
      "figures": [figure("bismuth 210", N0e_b, T_b, 25, 2.5, 5, "jours", 20, "Nombre N de noyaux de bismuth 210 restants en fonction du temps")],
      "donnees": ["ln 2 ≈ 0,693", f"t₁ = {fr(t1_b)} jours (question 5)"],
      "questions": QB}},
}

if __name__ == "__main__":
    ecrire(EX)
