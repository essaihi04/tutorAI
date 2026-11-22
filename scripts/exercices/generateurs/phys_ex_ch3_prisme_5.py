# Exercice de physique, ch. 3 (propagation d'une onde lumineuse), niveau moyen : la lumière dans le verre, puis le prisme.
# Sources comparées (skill exercices § 2) :
#  - exploration ondes_lumineuses.json : cas_types « milieu » (v = c/n, ν inchangée donc λ = λ₀/n, contrôle v < c et
#    λ < λ₀), « dispersion » (deux célérités dans le même verre → milieu dispersif ; violet le plus dévié), « qcm » ;
#    pieges « croit que la fréquence change dans le verre », « trouve n < 1 », « écrit v = c·n ou λ = λ₀·n », « ne sait
#    pas conclure après deux célérités différentes » ; a_ne_pas_dire « le rouge est le plus dévié », « la couleur change
#    dans le verre » ; exclus_hors_programme : Cauchy, minimum de déviation, Snell-Descartes en calcul (le prisme reste
#    qualitatif, cadre officiel) ; vidéos Rahou (milieu dispersif par deux vitesses), Boujaada (tableau vide / milieu),
#    Bazhar (dispersion) ; erreurs des profs relevées : « rouge plus lent que vert », « V = C/V ».
#  - nationaux comparés : 2021 N (prisme : ν_j = c/λ_0j, v = λ·ν avec λ dans le prisme donnée, conclusion dispersif),
#    2025 R et 2023 R (QCM : la fréquence ne dépend pas du milieu). Ici la chaîne part d'une célérité mesurée (n = c/v),
#    fait justifier ν et démontrer λ = λ₀/n, puis donne les indices du rouge et du violet (pas les λ dans le verre) :
#    situation et données différentes de 2021 N.
#  - séries en ligne : recherche web (talamidi séries 1 et 2 : « la fréquence est invariable quel que soit le milieu »,
#    moutamadris 2bac BIOF ondes lumineuses 1 et 2) : seuls les extraits des résultats ont été lus ; les sites sont
#    bloqués par le réseau de la session (talamidi.com, moutamadris.ma non résolus).
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


def figure(lam0, v):
    el = [
        {"f": "texte", "at": [5.0, 5.0], "t": "Document 1 : le laser traverse un bloc de verre", "couleur": "cyan", "ancre": "centre", "taille": "petit"},
        {"f": "rect", "de": [0.2, 3.6], "a": [1.4, 4.0], "couleur": "blanc", "remplir": "faible"},
        {"f": "texte", "at": [0.8, 4.3], "t": "laser", "couleur": "rouge", "ancre": "centre", "taille": "petit"},
        {"f": "rect", "de": [3.4, 3.0], "a": [6.6, 4.6], "couleur": "cyan", "remplir": "faible"},
        {"f": "ligne", "pts": [[1.4, 3.8], [9.6, 3.8]], "couleur": "rouge", "epais": True},
        {"f": "texte", "at": [2.4, 3.35], "t": f"air : c, λ₀ = {lam0} nm", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
        {"f": "texte", "at": [5.0, 3.35], "t": f"verre : v = {sci(v)} m/s", "couleur": "cyan", "ancre": "centre", "taille": "petit"},
        {"f": "texte", "at": [8.2, 3.35], "t": "air", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
        {"f": "texte", "at": [5.0, 2.55], "t": "Document 2 : lumière blanche et prisme du même verre", "couleur": "cyan", "ancre": "centre", "taille": "petit"},
        {"f": "ligne", "pts": [[3.0, 0.3], [5.0, 0.3], [4.0, 2.2]], "ferme": True, "couleur": "cyan", "remplir": "faible"},
        {"f": "ligne", "pts": [[0.4, 1.0], [3.37, 1.0]], "couleur": "blanc", "epais": True},
        {"f": "texte", "at": [1.5, 1.3], "t": "lumière blanche", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
        {"f": "ligne", "pts": [[3.37, 1.0], [4.66, 0.95]], "couleur": "blanc"},
        {"f": "ligne", "pts": [[4.66, 0.95], [9.0, 0.8]], "couleur": "rouge"},
        {"f": "ligne", "pts": [[4.66, 0.95], [9.0, 0.48]], "couleur": "vert"},
        {"f": "ligne", "pts": [[4.66, 0.95], [9.0, 0.16]], "couleur": "violet"},
        {"f": "ligne", "pts": [[9.2, 0.0], [9.2, 1.4]], "couleur": "blanc", "epais": True},
        {"f": "texte", "at": [9.55, 1.55], "t": "écran", "couleur": "blanc", "ancre": "centre", "taille": "petit"},
    ]
    return {"type": "schema", "titre": "La lumière dans le verre", "cadre": {"l": 10, "h": 5.2},
            "legende": "Document 2 : sur l'écran, un spectre continu (schéma qualitatif, angles exagérés).", "elements": el}


# ---------------------------------------------------------------- données et calculs
C = 3.00e8
LAM0, V, NR, NV = 633, 1.97e8, 1.51, 1.54
N = C / V                    # 1,523
N2 = round(N, 2)             # 1,52 (valeur arrondie réutilisée, comme sur une copie)
NU = C / (LAM0 * 1e-9)       # 4,74e14 Hz
LAM = LAM0 / N2              # 416 nm
VR, VV = C / NR, C / NV      # 1,99e8 ; 1,95e8
s_n, s_lam, s_vr, s_vv = fr(N2, 2), fr(LAM, 0), sci(VR), sci(VV)

EX = {
  "id": "phys_ex_ch3_prisme_5", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_lumineuses", "cours": "phys_ch3_ondes_lumineuses",
  "titre": "La lumière dans le verre, puis à travers un prisme", "niveau": "moyen", "duree_min": 25,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer l'indice n = c/v", "Justifier que la fréquence ne dépend pas du milieu",
                  "Établir et utiliser λ = λ₀/n", "Reconnaître un milieu dispersif ; le violet est le plus dévié"],
  "enonce": {
    "intro": (f"Un laser émet dans l'air une radiation rouge de longueur d'onde λ₀ = {LAM0} nm. Le faisceau traverse un bloc de verre "
              f"(document 1) ; on mesure dans ce verre la célérité de la lumière du laser : v = {sci(V)} m/s. "
              "On éclaire ensuite un prisme taillé dans le même verre avec un faisceau de lumière blanche (document 2). "
              f"Pour ce verre, l'indice vaut n_R = {fr(NR, 2)} pour une radiation rouge et n_V = {fr(NV, 2)} pour une radiation violette."),
    "intro_dit": (f"نقراو l'énoncé. واحد le laser كيعطي فالهوا une radiation حمرا، la longueur d'onde ديالها lambda zéro égale {mots(LAM0)} nanomètres. "
                  f"le faisceau كيدوز من واحد le bloc ديال الزجاج. فالزجاج، كنقيسو la célérité: v égale {msci(V)} mètres par seconde. "
                  "من بعد، كنضويو على واحد le prisme من نفس الزجاج، بالضو الأبيض. فهاد الزجاج، l'indice ديال le rouge، "
                  f"n R égale {mots(fr(NR, 2))}، و l'indice ديال le violet، n V égale {mots(fr(NV, 2))}."),
    "figures": [figure(LAM0, V)],
    "donnees": ["c = 3,00 × 10⁸ m/s (vide et air)", f"λ₀ = {LAM0} nm (dans l'air)", f"v = {sci(V)} m/s (dans le verre)",
                f"n_R = {fr(NR, 2)} (rouge) ; n_V = {fr(NV, 2)} (violet)"],
    "questions": [
      {"id": "1", "texte": "Calculer l'indice de réfraction n du verre pour la radiation du laser.",
       "texte_dit": "السؤال un: حسب l'indice de réfraction n ديال الزجاج، ل la radiation ديال le laser.",
       "reponse": valeur("n", round(N, 4), "", f"n = c/v = 3,00×10⁸/({sci(V)}) ≈ {s_n}"),
       "clavier": {"aides": ["n = c/v", "sans unité", "n ≥ 1"], "pieges": ["n = v/c", "n = c·v", "m/s"]},
       "aides": [aide("Comparez les deux célérités : dans le vide (ou l'air) c, et dans le verre v. Laquelle est la plus grande ?",
                      "قارن بين les deux célérités: c فالهوا، و v فالزجاج. شكون فيهم الكبيرة؟"),
                 aide("n = c/v : « en haut le vide, en bas le milieu » ; n n'a pas d'unité et vaut plus que 1.",
                      "n égale c sur v: الفوق le vide، والتحت le milieu. n بلا وحدة، و n supérieur à un.")],
       "correction": correction([("1 : n = c/v", "n égale c sur v"),
                                 (f"n = 3,00×10⁸/({sci(V)})", "l'application numérique"),
                                 (f"n ≈ {s_n} (sans unité, n > 1)", f"n égale {mots(s_n)}")],
                                f"السؤال un. n égale c sur v. l'application numérique: trois fois dix puissance huit، sur {msci(V)}. "
                                f"n égale {mots(s_n)}، بلا وحدة، و n supérieur à un."),
       "explication": "ex_p1", "facile": "fa_p1"},
      {"id": "2", "texte": "La lumière du laser change-t-elle de fréquence en passant de l'air au verre ? Justifier.",
       "texte_dit": "السؤال deux: واش la fréquence ديال الضو كتبدل ملي كيدوز من الهوا للزجاج؟ justifier.",
       "reponse": phrase(f"Non. La fréquence est imposée par la source (le laser) ; elle ne dépend pas du milieu de propagation : "
                         f"ν reste la même dans l'air et dans le verre, ν = c/λ₀ ≈ {sci(NU)} Hz, et la couleur ne change pas. "
                         "Seules la célérité et la longueur d'onde changent."),
       "clavier": {"aides": ["ν = c/λ₀", "la source impose ν", "ne dépend pas du milieu"],
                   "pieges": ["ν = v/λ₀", "la fréquence diminue dans le verre"]},
       "aides": [aide("Qui fixe la fréquence d'une onde : la source ou le milieu ? Le laser rouge reste-t-il rouge dans le verre ?",
                      "شكون اللي كيعطي la fréquence: la source ولا le milieu؟ واش الضو الحمر كيبقى حمر فالزجاج؟"),
                 aide("La fréquence d'une radiation ne change pas quand elle change de milieu ; ce sont v et λ qui changent.",
                      "la fréquence d'une radiation ما كتبدلش ملي كتبدل le milieu. اللي كيتبدلو هوما v و lambda.")],
       "correction": correction([("2 : la fréquence est imposée par la source", "la source هي اللي كتعطي la fréquence"),
                                 ("Elle ne dépend pas du milieu : ν est la même dans l'air et dans le verre.", "ما كتبدلش"),
                                 (f"ν = c/λ₀ ≈ {sci(NU)} Hz ; même couleur ; seules v et λ changent.", "غير v و lambda")],
                                "السؤال deux. لا. la source هي اللي كتعطي la fréquence، ماشي le milieu. إذن la fréquence ما كتبدلش "
                                f"من الهوا للزجاج: nu égale c sur lambda zéro، nu égale {msci(NU)} hertz فالجوج. واللون كيبقى حمر. "
                                "غير v و lambda اللي كيتبدلو."),
       "explication": "ex_p2", "facile": "fa_p2"},
      {"id": "3", "texte": "Montrer que la longueur d'onde de la radiation dans le verre s'écrit λ = λ₀/n.",
       "texte_dit": "السؤال trois: montrer que la longueur d'onde فالزجاج هي lambda égale lambda zéro sur n.",
       "reponse": phrase("Dans l'air : ν = c/λ₀ ; dans le verre : ν = v/λ (même fréquence). Donc c/λ₀ = v/λ, soit λ = λ₀·v/c. "
                         "Or n = c/v, donc v/c = 1/n : λ = λ₀/n."),
       "clavier": {"aides": ["ν = c/λ₀", "ν = v/λ", "n = c/v", "λ = λ₀/n"], "pieges": ["λ = λ₀·n", "ν change"]},
       "aides": [aide("Écrivez ν dans l'air et ν dans le verre : la fréquence est la même des deux côtés.",
                      "كتب nu فالهوا، و nu فالزجاج. la fréquence هي هي من الجوج."),
                 aide("c/λ₀ = v/λ, isolez λ, puis remplacez v/c par 1/n.",
                      "c sur lambda zéro égale v sur lambda. خرج lambda، ومن بعد بدل v sur c par un sur n.")],
       "correction": correction([("3 : air : ν = c/λ₀ ; verre : ν = v/λ (même ν)", "nu égale c sur lambda zéro"),
                                 ("c/λ₀ = v/λ donc λ = λ₀·v/c", "lambda égale lambda zéro fois v sur c"),
                                 ("n = c/v ⇒ v/c = 1/n, donc λ = λ₀/n", "lambda égale lambda zéro sur n")],
                                "السؤال trois. فالهوا، nu égale c sur lambda zéro. فالزجاج، nu égale v sur lambda، ونفس nu. "
                                "إذن c sur lambda zéro égale v sur lambda، و lambda égale lambda zéro fois v sur c. "
                                "و n égale c sur v، إذن v sur c égale un sur n. donc lambda égale lambda zéro sur n."),
       "explication": "ex_p3", "facile": "fa_p3"},
      {"id": "4", "texte": "Calculer la longueur d'onde λ de la radiation du laser dans le verre.",
       "texte_dit": "السؤال quatre: حسب la longueur d'onde lambda ديال la radiation فالزجاج.",
       "reponse": valeur("λ", round(LAM, 1), "nm", f"λ = λ₀/n = {LAM0}/{s_n} ≈ {s_lam} nm"),
       "clavier": {"aides": ["λ = λ₀/n", "nm", f"A.N. : λ = {LAM0}/{s_n}"], "pieges": ["λ = λ₀·n", "λ > λ₀"]},
       "aides": [aide("Dans le verre, l'onde ralentit et se resserre : λ doit être plus petite que λ₀.",
                      "فالزجاج، l'onde كتمشي بشوية وكتقرب: lambda خاصها تكون صغر من lambda zéro."),
                 aide("λ = λ₀/n ; on peut garder les nanomètres, car n n'a pas d'unité.",
                      "lambda égale lambda zéro sur n. تقدر تخلي nanomètre، حيت n بلا وحدة.")],
       "correction": correction([("4 : λ = λ₀/n", "lambda égale lambda zéro sur n"),
                                 (f"λ = {LAM0}/{s_n}", "l'application numérique"),
                                 (f"λ ≈ {s_lam} nm (< λ₀ : l'onde se resserre)", f"lambda égale {mots(s_lam)} nanomètres")],
                                f"السؤال quatre. lambda égale lambda zéro sur n. l'application numérique: {mots(LAM0)} sur {mots(s_n)}. "
                                f"lambda égale {mots(s_lam)} nanomètres، صغر من lambda zéro."),
       "explication": "ex_p4", "facile": "fa_p4"},
      {"id": "5", "texte": "Calculer la célérité v_R de la radiation rouge, puis la célérité v_V de la radiation violette dans le verre du prisme.",
       "texte_dit": "السؤال cinq: حسب la célérité v R ديال le rouge، ومن بعد la célérité v V ديال le violet، فالزجاج ديال le prisme.",
       "reponse": valeur("v_V", round(VV, -5), "m/s",
                         f"v_R = c/n_R = 3,00×10⁸/{fr(NR, 2)} ≈ {s_vr} m/s ; v_V = c/n_V = 3,00×10⁸/{fr(NV, 2)} ≈ {s_vv} m/s"),
       "clavier": {"aides": ["v = c/n", "m/s", "A.N. : v_V = 3,00×10⁸/1,54"], "pieges": ["v = c·n", "v = n/c"]},
       "aides": [aide("Chaque radiation a son propre indice dans le verre : utilisez n_R pour le rouge, n_V pour le violet.",
                      "كل radiation عندها l'indice ديالها فالزجاج: n R ل le rouge، و n V ل le violet."),
                 aide("De n = c/v on tire v = c/n.", "من n égale c sur v، كنخرجو v égale c sur n.")],
       "correction": correction([("5 : v = c/n", "v égale c sur n"),
                                 (f"v_R = 3,00×10⁸/{fr(NR, 2)} ≈ {s_vr} m/s", f"v R égale {msci(VR)}"),
                                 (f"v_V = 3,00×10⁸/{fr(NV, 2)} ≈ {s_vv} m/s", f"v V égale {msci(VV)}")],
                                f"السؤال cinq. v égale c sur n. ل le rouge: v R égale trois fois dix puissance huit sur {mots(fr(NR, 2))}، "
                                f"v R égale {msci(VR)} mètres par seconde. ل le violet: v V égale trois fois dix puissance huit sur {mots(fr(NV, 2))}، "
                                f"v V égale {msci(VV)} mètres par seconde."),
       "explication": "ex_p5", "facile": "fa_p5"},
      {"id": "6", "texte": "Que peut-on déduire de ces deux célérités pour le verre ? Quelle radiation est la plus déviée par le prisme ? Justifier.",
       "texte_dit": "السؤال six: شنو نستنتجو من هاد les deux célérités على الزجاج؟ وأشنو هي la radiation اللي كتتبدل أكثر ب le prisme؟ justifier.",
       "reponse": phrase("v_R ≠ v_V : la célérité de la lumière dans le verre dépend de la fréquence de la radiation, donc le verre est un "
                         "milieu dispersif. n_V > n_R : la radiation violette est la plus déviée par le prisme (le rouge est le moins dévié) ; "
                         "le prisme sépare les radiations de la lumière blanche : c'est la dispersion."),
       "clavier": {"aides": ["milieu dispersif", "v dépend de ν", "n_V > n_R", "le violet est le plus dévié"],
                   "pieges": ["le rouge est le plus dévié", "le prisme colore la lumière"]},
       "aides": [aide("Les deux radiations ont-elles la même célérité dans le même verre ? Comment s'appelle un tel milieu ?",
                      "واش les deux radiations كيمشيو بنفس la célérité فنفس الزجاج؟ شنو سميتو هاد le milieu؟"),
                 aide("Un milieu est dispersif si la célérité dépend de la fréquence. Plus l'indice est grand, plus la radiation est déviée.",
                      "un milieu est dispersif، يلا كانت la célérité كتبدل مع la fréquence. وكلما l'indice كبير، كلما la radiation كتتبدل أكثر.")],
       "correction": correction([("6 : v_R ≠ v_V : la célérité dépend de la fréquence", "la célérité كتبدل مع la fréquence"),
                                 ("Le verre est un milieu dispersif.", "le verre milieu dispersif"),
                                 ("n_V > n_R : le violet est le plus dévié, le rouge le moins dévié.", "le violet est le plus dévié")],
                                "السؤال six. v R ماشي هي v V: la célérité كتبدل مع la fréquence. إذن le verre milieu dispersif. "
                                "و n V كبر من n R، إذن le violet est le plus dévié، و le rouge هو اللي كيتبدل قل."),
       "explication": "ex_p6", "facile": "fa_p6"},
    ]
  },
}

# ---------------------------------------------------------------- explication animée
m1 = ("باش نعرفو شحال الضو كينقص من la célérité ديالو، كنستعملو l'indice. هادا الجدول: على اليسار le vide، وعلى اليمين le milieu. "
      "فle vide، الضو كيمشي ب c. فle milieu، كيمشي بشوية: la célérité v صغر من c. l'indice: n égale c sur v، الفوق le vide والتحت le milieu. "
      "n بلا وحدة، و n supérieur à un. الزجاج: environ un virgule cinq. "
      f"فالتمرين، v égale {msci(V)} mètres par seconde. إذن n égale trois fois dix puissance huit، sur {msci(V)}. n égale {mots(s_n)}.")
m2 = ("شوف les deux compteurs: واحد فالهوا، وواحد فالزجاج. كل واحد كيحسب les crêtes اللي كيدوزو فواحد la seconde. "
      "بجوج كيعطيو نفس العدد. الضو كيمشي بشوية فالزجاج، ولكن la fréquence ما كتبدلش. la source هي اللي كتعطي la fréquence، ماشي le milieu. "
      "واللون مربوط ب la fréquence: الضو الحمر كيبقى حمر فالزجاج. "
      f"فالتمرين، nu égale c sur lambda zéro، nu égale {msci(NU)} hertz، فالهوا وفالزجاج.")
m3 = ("نكملو الجدول ديال le vide و le milieu. la fréquence هي هي من كل جهة. فالهوا: nu égale c sur lambda zéro. فالزجاج: nu égale v sur lambda. "
      "نفس nu، إذن c sur lambda zéro égale v sur lambda. كنخرجو lambda: lambda égale lambda zéro fois v sur c. "
      "و n égale c sur v، إذن v sur c égale un sur n. le résultat: lambda égale lambda zéro sur n.")
m4 = (f"دابا la simulation فيها نفس القيم ديال التمرين: lambda zéro égale {mots(LAM0)} nanomètres، و n égale {mots(s_n)}. "
      "شوف l'onde فالهوا. ودابا كتدخل للزجاج: les crêtes كيقربو لبعضياتهم. la longueur d'onde كتنقص. "
      f"lambda égale lambda zéro sur n: {mots(LAM0)} sur {mots(s_n)}. lambda égale {mots(s_lam)} nanomètres. "
      "واللون؟ كيبقى حمر: la fréquence ما تبدلاتش.")
m5 = ("فla simulation، deux radiations كيدخلو لنفس الزجاج: le rouge الفوق، و le jaune التحت. فالهوا، كيمشيو مع بعضياتهم. "
      "فالزجاج، شوف: le jaune كيبقى اللور. هنا، le rouge عندو n égale un virgule soixante-deux، و le jaune عندو n égale un virgule soixante-six. "
      "كل radiation عندها l'indice ديالها، إذن la célérité ديالها: v égale c sur n. "
      f"فالتمرين، n R égale {mots(fr(NR, 2))}: v R égale {msci(VR)} mètres par seconde. "
      f"و n V égale {mots(fr(NV, 2))}: v V égale {msci(VV)} mètres par seconde.")
m6 = ("دابا الضو الأبيض كيوصل ل le prisme. كيدخل للزجاج، وملي كيخرج، الألوان كيتفرقو. فوق l'écran، واحد le spectre continu. "
      f"علاش؟ فالتمرين، n R égale {mots(fr(NR, 2))}، و n V égale {mots(fr(NV, 2))}: l'indice كيتبدل مع la radiation. "
      "إذن v égale c sur n كتبدل حتى هي مع la fréquence: le verre milieu dispersif. "
      "شوف le rouge: هو اللي كيتبدل الاتجاه ديالو قل. و le violet، اللي l'indice ديالو أكبر، هو اللي كيتبدل أكثر: le violet est le plus dévié.")
EX["explication"] = {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
  diapo_sim("ex_p1", "Question 1 : l'indice n = c/v", "En haut le vide, en bas le milieu.", SIM + "indice.html",
            "La lumière ralentit dans les milieux transparents", m1,
            [("n = c/v (sans unité, n ≥ 1)", "l'indice: n égale c sur v"), (f"n = 3,00×10⁸/({sci(V)}) ≈ {s_n}", f"n égale {mots(s_n)}.")],
            [dict(mot="هادا الجدول", commande="play_until", parametres={"moment": "trace"}),
             dict(mot="على اليسار le vide", repere="vide"), dict(mot="وعلى اليمين le milieu", repere="milieu"),
             dict(mot="كيمشي بشوية", commande="play_until", parametres={"moment": "celerite"}),
             dict(mot="l'indice: n égale c sur v", commande="play_until", parametres={"moment": "indice"}),
             dict(mot="l'indice: n égale c sur v", cible="centre:0"),
             dict(mot="الزجاج: environ", repere="verre"),
             dict(mot=f"n égale {mots(s_n)}.", cible="centre:1")]),
  diapo_sim("ex_p2", "Question 2 : la fréquence ne change pas", "Même fréquence, même couleur.", SIM + "milieu.html?depart=front_entre",
            "Deux compteurs de crêtes : dans l'air et dans le verre", m2,
            [("ν ne dépend pas du milieu", "ولكن la fréquence ما كتبدلش"), (f"ν = c/λ₀ ≈ {sci(NU)} Hz", f"nu égale {msci(NU)} hertz")],
            [dict(mot="واحد فالهوا", repere="compteur_air"), dict(mot="وواحد فالزجاج", repere="compteur_verre"),
             dict(mot="بجوج كيعطيو نفس العدد", commande="play_until", parametres={"moment": "compte_frequence"}),
             dict(mot="ولكن la fréquence ما كتبدلش", cible="centre:0"),
             dict(mot=f"nu égale {msci(NU)} hertz", cible="centre:1")]),
  diapo_sim("ex_p3", "Question 3 : montrer que λ = λ₀/n", "Même ν : c/λ₀ = v/λ.", SIM + "figures.html?fig=fig_vide_milieu",
            "Le tableau vide / milieu", m3,
            [("Même ν : c/λ₀ = v/λ", "نفس nu، إذن"), ("λ = λ₀·v/c = λ₀/n", "le résultat: lambda égale lambda zéro sur n")],
            [dict(mot="نكملو الجدول", commande="play_until", parametres={"moment": "longueur"}),
             dict(mot="la fréquence هي هي", commande="play_until", parametres={"moment": "frequence"}),
             dict(mot="نفس nu، إذن", cible="centre:0"),
             dict(mot="le résultat: lambda égale lambda zéro sur n", cible="centre:1")]),
  diapo_sim("ex_p4", "Question 4 : l'onde se resserre dans le verre", "λ = λ₀/n < λ₀.", SIM + "milieu.html",
            "L'onde du laser entre dans le verre", m4,
            [(f"λ = λ₀/n = {LAM0}/{s_n} ≈ {s_lam} nm", f"lambda égale {mots(s_lam)} nanomètres")],
            [dict(mot="دابا la simulation فيها", commande="set_parameters", parametres={"n": N2, "lambda0_nm": LAM0}),
             dict(mot="شوف l'onde فالهوا", commande="play_until", parametres={"moment": "onde_dans_air"}),
             dict(mot="شوف l'onde فالهوا", repere="lambda0"),
             dict(mot="ودابا كتدخل للزجاج", commande="play_until", parametres={"moment": "lambda_serree"}),
             dict(mot="la longueur d'onde كتنقص", commande="play_until", parametres={"moment": "mesure_lambda"}),
             dict(mot="la longueur d'onde كتنقص", repere="lambda"),
             dict(mot=f"lambda égale {mots(s_lam)} nanomètres", cible="centre:0")]),
  diapo_sim("ex_p5", "Question 5 : chaque radiation, sa célérité", "v = c/n, avec l'indice de chaque radiation.", SIM + "milieu.html?vue=deux",
            "Deux radiations dans le même verre", m5,
            [("v = c/n", "v égale c sur n"), (f"v_R ≈ {s_vr} m/s ; v_V ≈ {s_vv} m/s", f"v V égale {msci(VV)} mètres par seconde")],
            [dict(mot="le rouge الفوق", repere="front_rouge"), dict(mot="و le jaune التحت", repere="front_jaune"),
             dict(mot="فالهوا، كيمشيو", commande="play_until", parametres={"moment": "front_entre"}),
             dict(mot="فالزجاج، شوف", commande="play_until", parametres={"moment": "fronts_ecartes"}),
             dict(mot="هنا، le rouge", commande="play_until", parametres={"moment": "mesure_vitesses"}),
             dict(mot="v égale c sur n", cible="centre:0"),
             dict(mot=f"v V égale {msci(VV)} mètres par seconde", cible="centre:1")]),
  diapo_sim("ex_p6", "Question 6 : verre dispersif, violet le plus dévié", "n_V > n_R : le violet est le plus dévié.",
            SIM + "prisme-dispersion.html", "La lumière blanche traverse le prisme", m6,
            [("v dépend de ν : verre dispersif", "le verre milieu dispersif"), ("n_V > n_R : violet le plus dévié", "le violet est le plus dévié")],
            [dict(mot="الضو الأبيض كيوصل", commande="play_until", parametres={"moment": "blanc_arrive"}),
             dict(mot="كيدخل للزجاج", commande="play_until", parametres={"moment": "entre_dans_verre"}),
             dict(mot="وملي كيخرج", commande="play_until", parametres={"moment": "couleurs_se_separent"}),
             dict(mot="فوق l'écran", commande="play_until", parametres={"moment": "spectre_sur_ecran"}),
             dict(mot="le spectre continu", repere="spectre"),
             dict(mot="le verre milieu dispersif", cible="centre:0"),
             dict(mot="شوف le rouge", commande="play_until", parametres={"moment": "rouge_moins_devie"}),
             dict(mot="شوف le rouge", repere="rouge"),
             dict(mot="و le violet، اللي", commande="play_until", parametres={"moment": "violet_plus_devie"}),
             dict(mot="و le violet، اللي", repere="violet"),
             dict(mot="le violet est le plus dévié", cible="centre:1")]),
]}]}

# ---------------------------------------------------------------- version facile
vc, cv = V / C, C * V
EX["facile"] = {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
  qcm_facile("fa_p1", "Plus facile : l'indice", "نتمرنو بسؤال ساهل. اختار la bonne valeur.",
             f"Dans le verre, v = {sci(V)} m/s ; c = 3,00 × 10⁸ m/s. L'indice du verre vaut…",
             [f"n ≈ {fr(vc, 2)}", f"n ≈ {s_n}", f"n ≈ {sci(cv, 2)}"], 1, {
               "1": {"juste": rep(f"برافو! n égale c sur v، n égale {mots(s_n)}، بلا وحدة و n supérieur à un.", f"Juste : n = c/v ≈ {s_n}.")},
               "0": {"1": rep("رد البال: n ديما supérieur à un. واش قلبتي la fraction؟ عاود اختار.", "n est toujours plus grand que 1 : la fraction est-elle à l'envers ? Réessaie."),
                     "2": rep(f"الجواب هو n égale {mots(s_n)}. n égale c sur v، ماشي v sur c.", f"Réponse : n = c/v ≈ {s_n} (et non v/c).")},
               "2": {"1": rep("هاد الرقم كبير بزاف: ضربتي c فv. l'indice كنقسمو فيه. عاود اختار.", "Tu as multiplié c par v ; l'indice est un quotient. Réessaie."),
                     "2": rep(f"الجواب هو n égale {mots(s_n)}: c sur v، ماشي c fois v.", f"Réponse : n = c/v ≈ {s_n}.")}},
             "Dans le verre, quelle est la valeur de l'indice n ?"),
  vf_facile("fa_p2", "Plus facile : air → verre", "سؤال ساهل: قول واش كل جملة صحيحة ولا غالطة.",
            "Le laser rouge passe de l'air au verre.", [
              ("La fréquence de la radiation est la même dans l'air et dans le verre.", True, "La fréquence est imposée par la source : elle ne dépend pas du milieu."),
              ("Dans le verre, la lumière du laser devient bleue.", False, "La couleur est liée à la fréquence, qui ne change pas : le laser reste rouge."),
              ("La célérité de la lumière est plus petite dans le verre que dans l'air.", True, f"v = c/n avec n > 1 : v = {sci(V)} m/s < c.")]),
  assoc_facile("fa_p3", "Plus facile : du vide au milieu", "نتمرنو: ربط كل grandeur فالزجاج مع la relation ديالها.",
               "Dans un milieu d'indice n, que devient chaque grandeur ?", "Relie chaque grandeur dans le verre à sa relation.",
               [("1", "Célérité dans le verre"), ("2", "Longueur d'onde dans le verre"), ("3", "Fréquence dans le verre")],
               [("a", "v = c/n"), ("b", "λ = λ₀/n"), ("c", "ν = c/λ₀, inchangée"), ("d", "v = c·n")],
               {"1": "a", "2": "b", "3": "c"}, {
                 "1-a": (True, "Oui : n = c/v donc v = c/n, plus petite que c.", "برافو: v égale c sur n، صغر من c."),
                 "1-b": (False, "λ₀/n est une longueur, pas une célérité.", "لا، lambda zéro sur n هي longueur، ماشي célérité."),
                 "1-c": (False, "c/λ₀ est une fréquence, en hertz : ce n'est pas une célérité.", "لا، c sur lambda zéro هي fréquence، ماشي célérité."),
                 "1-d": (False, "c·n serait plus grande que c : impossible, la lumière ralentit dans le verre.", "لا، c fois n كتكون كبر من c: الضو كينقص فالزجاج، ماشي كيزيد."),
                 "2-a": (False, "c/n est une célérité ; la longueur d'onde part de λ₀.", "لا، c sur n هي célérité. la longueur d'onde كتبدا من lambda zéro."),
                 "2-b": (True, "Oui : même ν, l'onde ralentit, donc λ = λ₀/n.", "برافو: lambda égale lambda zéro sur n."),
                 "2-c": (False, "c/λ₀ est la fréquence, pas une longueur.", "لا، هادي la fréquence، ماشي longueur."),
                 "2-d": (False, "c·n n'est pas une longueur d'onde.", "لا، هادي ماشي longueur d'onde."),
                 "3-a": (False, "c/n est la célérité dans le verre, pas la fréquence.", "لا، c sur n هي la célérité فالزجاج."),
                 "3-b": (False, "λ₀/n est la longueur d'onde dans le verre.", "لا، lambda zéro sur n هي la longueur d'onde فالزجاج."),
                 "3-c": (True, "Oui : la fréquence ne change pas de milieu.", "برافو: la fréquence ما كتبدلش."),
                 "3-d": (False, "c·n n'existe pas : et la fréquence ne change pas.", "لا، la fréquence ما كتبدلش، وهاد la relation غالطة.")},
               ("v et λ sont divisées par n ; ν reste la même. v = c·n est l'intrus.",
                "v و lambda كنقسموهم على n، و la fréquence كتبقى هي هي. v égale c fois n غالطة.")),
  qcm_facile("fa_p4", "Plus facile : λ dans le verre", "سؤال ساهل. اختار الجواب الصحيح.",
             f"λ₀ = {LAM0} nm et n = {s_n}. Dans le verre, λ vaut…",
             [f"{s_lam} nm", f"{fr(LAM0 * N2, 0)} nm", f"{LAM0} nm"], 0, {
               "0": {"juste": rep(f"برافو! lambda égale lambda zéro sur n، يعني lambda égale {mots(s_lam)} nanomètres.", f"Juste : λ = λ₀/n ≈ {s_lam} nm.")},
               "1": {"1": rep("فالزجاج l'onde كتقرب: lambda خاصها تصغر، ماشي تكبر. عاود اختار.", "Dans le verre l'onde se resserre : λ diminue. Réessaie."),
                     "2": rep(f"الجواب هو lambda égale {mots(s_lam)} nanomètres. كنقسمو على n، ماشي كنضربو.", f"Réponse : λ = λ₀/n ≈ {s_lam} nm (on divise par n).")},
               "2": {"1": rep("la fréquence هي اللي ما كتبدلش، ماشي la longueur d'onde. عاود اختار.", "C'est la fréquence qui ne change pas, pas λ. Réessaie."),
                     "2": rep(f"الجواب هو lambda égale {mots(s_lam)} nanomètres: la longueur d'onde كتنقص فالزجاج.", f"Réponse : λ ≈ {s_lam} nm ; λ change avec le milieu.")}},
             f"lambda zéro égale {mots(LAM0)} nanomètres et n égale {mots(s_n)}. Dans le verre, lambda vaut ?"),
  qcm_facile("fa_p5", "Plus facile : la célérité du violet", "سؤال ساهل على la célérité.",
             f"n_V = {fr(NV, 2)}. La célérité du violet dans ce verre vaut…",
             [f"{sci(C * NV)} m/s", f"{sci(NV / C)} m/s", f"{s_vv} m/s"], 2, {
               "2": {"juste": rep(f"برافو! v V égale c sur n V، v V égale {msci(VV)} mètres par seconde.", f"Juste : v_V = c/n_V ≈ {s_vv} m/s.")},
               "0": {"1": rep("هاد la célérité كبر من c: ما يمكنش. واش ضربتي فn؟ عاود اختار.", "Plus grande que c : impossible. As-tu multiplié par n ? Réessaie."),
                     "2": rep(f"الجواب هو v V égale {msci(VV)} mètres par seconde: v égale c sur n.", f"Réponse : v_V = c/n_V ≈ {s_vv} m/s.")},
               "1": {"1": rep("هاد القيمة صغيرة بزاف: قلبتي la fraction. عاود اختار.", "Valeur minuscule : la fraction est à l'envers. Réessaie."),
                     "2": rep(f"الجواب هو v V égale {msci(VV)} mètres par seconde: c sur n، ماشي n sur c.", f"Réponse : v_V = c/n_V ≈ {s_vv} m/s (et non n/c).")}},
             f"n V égale {mots(fr(NV, 2))}. La célérité du violet dans ce verre vaut ?"),
  vf_facile("fa_p6", "Plus facile : la dispersion", "آخر سؤال ساهل: صحيح ولا غالط؟",
            f"Dans le verre du prisme : n_R = {fr(NR, 2)} et n_V = {fr(NV, 2)}.", [
              ("Le violet est la radiation la plus déviée par le prisme.", True, "n_V > n_R : le violet est le plus dévié, le rouge le moins dévié."),
              ("Le rouge est la radiation la plus déviée.", False, "Le rouge a le plus petit indice : c'est le moins dévié."),
              ("Le verre est dispersif, car la célérité de la lumière y dépend de la fréquence.", True, "v_R ≠ v_V dans le même verre : milieu dispersif.")]),
]}]}

# ---------------------------------------------------------------- exercice semblable
b_lam0, b_v, b_nr, b_nv = 532, 1.85e8, 1.60, 1.65
b_n = C / b_v; b_n2 = round(b_n, 2); b_nu = C / (b_lam0 * 1e-9); b_lam = b_lam0 / b_n2; b_vr, b_vv = C / b_nr, C / b_nv
EX["similaire"] = {"id": "phys_ex_ch3_prisme_5_b", "titre": "Même exercice, autres données", "enonce": {
  "intro": (f"Un laser vert émet dans l'air une radiation de longueur d'onde λ₀ = {b_lam0} nm. Dans un bloc de verre « flint », "
            f"la célérité de cette lumière est v = {sci(b_v)} m/s. Un prisme taillé dans ce verre est éclairé en lumière blanche ; "
            f"son indice vaut n_R = {fr(b_nr, 2)} pour le rouge et n_V = {fr(b_nv, 2)} pour le violet."),
  "intro_dit": (f"نفس التمرين، بقيم أخرى. le laser خضر، lambda zéro égale {mots(b_lam0)} nanomètres. فالزجاج، v égale {msci(b_v)} mètres par seconde. "
                f"و le prisme: n R égale {mots(fr(b_nr, 2))}، و n V égale {mots(fr(b_nv, 2))}."),
  "figures": [figure(b_lam0, b_v)],
  "donnees": ["c = 3,00 × 10⁸ m/s", f"λ₀ = {b_lam0} nm", f"v = {sci(b_v)} m/s", f"n_R = {fr(b_nr, 2)} ; n_V = {fr(b_nv, 2)}"],
  "questions": [
    {"id": "1", "texte": "Calculer l'indice n du verre pour la radiation du laser.",
     "reponse": valeur("n", round(b_n, 4), "", f"n = c/v = 3,00×10⁸/({sci(b_v)}) ≈ {fr(b_n2, 2)}"),
     "clavier": {"aides": ["n = c/v"], "pieges": ["n = v/c"]},
     "correction": correction([("1 : n = c/v", "n égale c sur v"), (f"n ≈ {fr(b_n2, 2)}", f"n égale {mots(fr(b_n2, 2))}")],
                              f"السؤال un. n égale c sur v. n égale {mots(fr(b_n2, 2))}.")},
    {"id": "2", "texte": "La fréquence change-t-elle en passant de l'air au verre ? Justifier.",
     "reponse": phrase(f"Non : la fréquence est imposée par la source et ne dépend pas du milieu ; ν = c/λ₀ ≈ {sci(b_nu)} Hz dans l'air et dans le verre."),
     "clavier": {"aides": ["la source impose ν", "ν = c/λ₀"], "pieges": ["ν diminue"]},
     "correction": correction([("2 : ν imposée par la source, indépendante du milieu", "la source هي اللي كتعطي la fréquence"),
                               (f"ν = c/λ₀ ≈ {sci(b_nu)} Hz des deux côtés", f"nu égale {msci(b_nu)} hertz")],
                              f"السؤال deux. لا. la source هي اللي كتعطي la fréquence. nu égale {msci(b_nu)} hertz فالجوج.")},
    {"id": "3", "texte": "Montrer que λ = λ₀/n.",
     "reponse": phrase("ν = c/λ₀ = v/λ (même ν) donc λ = λ₀·v/c ; n = c/v donc λ = λ₀/n."),
     "clavier": {"aides": ["ν = c/λ₀", "ν = v/λ", "n = c/v"], "pieges": ["λ = λ₀·n"]},
     "correction": correction([("3 : c/λ₀ = v/λ (même ν)", "c sur lambda zéro égale v sur lambda"), ("λ = λ₀·v/c = λ₀/n", "lambda égale lambda zéro sur n")],
                              "السؤال trois. نفس nu، إذن c sur lambda zéro égale v sur lambda. و v sur c égale un sur n: lambda égale lambda zéro sur n.")},
    {"id": "4", "texte": "Calculer λ dans le verre.",
     "reponse": valeur("λ", round(b_lam, 1), "nm", f"λ = λ₀/n = {b_lam0}/{fr(b_n2, 2)} ≈ {fr(b_lam, 0)} nm"),
     "clavier": {"aides": ["λ = λ₀/n", "nm"], "pieges": ["λ = λ₀·n"]},
     "correction": correction([("4 : λ = λ₀/n", "lambda égale lambda zéro sur n"), (f"λ ≈ {fr(b_lam, 0)} nm", f"lambda égale {mots(fr(b_lam, 0))} nanomètres")],
                              f"السؤال quatre. lambda égale lambda zéro sur n. lambda égale {mots(fr(b_lam, 0))} nanomètres.")},
    {"id": "5", "texte": "Calculer v_R puis v_V dans le verre du prisme.",
     "reponse": valeur("v_V", round(b_vv, -5), "m/s", f"v_R = c/n_R ≈ {sci(b_vr)} m/s ; v_V = c/n_V = 3,00×10⁸/{fr(b_nv, 2)} ≈ {sci(b_vv)} m/s"),
     "clavier": {"aides": ["v = c/n", "m/s"], "pieges": ["v = c·n"]},
     "correction": correction([("5 : v = c/n", "v égale c sur n"), (f"v_R ≈ {sci(b_vr)} m/s ; v_V ≈ {sci(b_vv)} m/s", f"v V égale {msci(b_vv)}")],
                              f"السؤال cinq. v égale c sur n. v R égale {msci(b_vr)}، و v V égale {msci(b_vv)} mètres par seconde.")},
    {"id": "6", "texte": "Que déduire pour ce verre ? Quelle radiation est la plus déviée ? Justifier.",
     "reponse": phrase("v_R ≠ v_V : la célérité dépend de la fréquence, le verre est dispersif ; n_V > n_R : le violet est le plus dévié."),
     "clavier": {"aides": ["milieu dispersif", "n_V > n_R"], "pieges": ["le rouge est le plus dévié"]},
     "correction": correction([("6 : v dépend de ν : verre dispersif", "milieu dispersif"), ("n_V > n_R : violet le plus dévié", "le violet est le plus dévié")],
                              "السؤال six. la célérité كتبدل مع la fréquence: milieu dispersif. و n V كبر، إذن le violet est le plus dévié.")},
  ]}}

ecrire(EX)
