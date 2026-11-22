# Exercice de maths, ch. 3 (suites numériques), niveau moyen (niveau du national) : uₙ₊₁ = f(uₙ), f croissante.
# Sources comparées (lecture seule, rien de recopié) :
#  - exploration suites_definition.json : redaction_nationale recurrence_f_croissante, monotonie_f, convergence,
#    limite_point_fixe ; erreurs_examen « encadrement par f croissante » (f(a) et f(b) non comparés à a et b),
#    « monotonie par f(x) − x » (uₙ ∈ I non dit), « limite par ℓ = f(ℓ) » (conditions non écrites, solution hors de I) ;
#    pieges « lit les termes sur l'axe des ordonnées », « croissante donc converge vers 4 sur le dessin » ;
#  - vidéos : Djofer TJ8ngKZ93zg (représenter les termes en escalier, conjecturer), MedBrahmi HThkLAAcZ0Q (suite et
#    fonction), Driss DOTCOM pAPdp8Cms7I (« attends, f est-elle croissante ? »), biadmostafa XrpE2vSTzMM (choix de ℓ) ;
#  - nationaux : 2017 N, 2018 R, 2019 N, 2020 R, 2023 N, 2024 R, 2025 N (fin de problème : récurrence avec f, monotonie
#    par f(x) − x, convergence, ℓ = f(ℓ)) — ici sans ln ni exp : f(x) = √(2x + 3), fonction racine du chapitre 1 ;
#  - séries en ligne (résultats de recherche, pages non ouvertes : réseau fermé) : talamidi 2 bac PC série corrigée 3,
#    moutamadris 2 bac PC/SVT série 1, fayssalmaths séries corrigées 2 bac SE, pdfmath exercices nationaux corrigés,
#    xriadiat exercices corrigés suites.
# Données propres à Moalim : f(x) = √(2x + 3), u₀ = 0, I = [0 ; 3], ℓ = 3.
import math
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa: E402,F401,F403

ID = "math_ex_ch3_suites_5"
S = "/media/simulations/maths/suites-tableau/"


def figure(a, b, l, nom):
    """La courbe de f(x) = √(ax + b), la droite y = x et l'escalier depuis u₀ = 0 (trois marches)."""
    f = lambda x: math.sqrt(a * x + b)
    u = [0.0]
    for _ in range(3):
        u.append(f(u[-1]))
    pts = [[0, 0]]
    for k in range(3):
        pts += [[round(u[k], 3), round(u[k + 1], 3)], [round(u[k + 1], 3), round(u[k + 1], 3)]]
    el = [{"f": "courbe", "expr": f"sqrt({a}*x+{b})", "de": 0, "a": l + 1, "couleur": "cyan", "texte": f"(C_{nom})", "texte_x": l + 0.6, "pos": "n"},
          {"f": "courbe", "expr": "x", "de": 0, "a": l + 1, "couleur": "blanc", "texte": "(Δ) : y = x", "texte_x": l + 0.8, "pos": "se"},
          {"f": "ligne", "pts": pts, "couleur": "jaune"}]
    for k in range(3):
        if k:
            el.append({"f": "ligne", "pts": [[round(u[k], 3), round(u[k], 3)], [round(u[k], 3), 0]], "trait": "pointille", "couleur": "faible"})
        el.append({"f": "point", "at": [round(u[k], 3), 0], "couleur": "orange", "t": "u" + "₀₁₂"[k], "pos": "s"})
    return {"type": "courbe", "titre": f"La courbe de {nom}(x) = √({a}x + {b}), la droite y = x et les premiers termes",
            "axes": {"x": {"min": 0, "max": l + 1, "nom": "x", "graduations": list(range(1, l + 2))},
                     "y": {"min": 0, "max": l + 1, "nom": "y", "graduations": list(range(1, l + 2))}},
            "legende": "Les termes u₀, u₁, u₂ sont placés sur l'axe des abscisses grâce à la courbe et à la droite y = x.",
            "ratio": 0.8, "elements": el}


QUESTIONS = [
    {"id": "1", "texte": "En utilisant la figure, conjecturer le sens de variation de la suite (uₙ) et sa limite.",
     "texte_dit": "السؤال un: استعمل la figure، وقترح le sens de variation ديال la suite، وla limite ديالها.",
     "reponse": phrase("Sur la figure, u₀ < u₁ < u₂ < … : la suite semble croissante ; les termes se rapprochent de l'abscisse 3 du point d'intersection de (C_f) et de (Δ) : la suite semble converger vers 3."),
     "clavier": {"aides": ["u₀ < u₁ < u₂", "croissante", "point d'intersection de (C_f) et (Δ)", "converge vers 3"],
                 "pieges": ["termes lus sur l'axe des ordonnées", "décroissante"]},
     "aides": [aide("Les termes sont sur l'axe des abscisses : compare les positions de u₀, u₁, u₂.",
                    "les termes كاينين على l'axe des abscisses. قارن البلايص ديال u zéro، u un، u deux."),
               aide("Les marches de l'escalier s'arrêtent vers un point où la courbe coupe la droite y = x : quelle est son abscisse ?",
                    "الدروج ديال l'escalier كيوقفو قريب من نقطة فين la courbe كتقطع la droite y égale x. شنو هي l'abscisse ديالها؟")],
     "correction": correction([
         ("1 : sur la figure, u₀ < u₁ < u₂ : (uₙ) semble croissante", "semble croissante"),
         ("les termes s'approchent de 3, abscisse du point d'intersection de (C_f) et (Δ) : (uₙ) semble converger vers 3", "converger vers trois")],
         "السؤال un. على la figure، u zéro، u un، u deux كيمشيو لليمين: la suite semble croissante. والدروج كيقربو من النقطة فين la courbe كتقطع la droite، l'abscisse ديالها trois: la suite semble converger vers trois."),
     "explication": "ex_1", "facile": "fa_1"},
    {"id": "2", "texte": "Montrer par récurrence que 0 ≤ uₙ ≤ 3 pour tout entier naturel n.",
     "texte_dit": "السؤال deux: بين par récurrence بلي u indice n بين zéro وtrois، pour tout n.",
     "reponse": phrase("Initialisation : u₀ = 0, donc 0 ≤ u₀ ≤ 3. Hérédité : supposons 0 ≤ uₙ ≤ 3 ; f est croissante sur [0 ; 3], donc f(0) ≤ f(uₙ) ≤ f(3), soit √3 ≤ uₙ₊₁ ≤ 3 ; comme √3 ≥ 0, on a 0 ≤ uₙ₊₁ ≤ 3. Conclusion : 0 ≤ uₙ ≤ 3 pour tout n."),
     "clavier": {"aides": ["f croissante sur [0 ; 3]", "f(0) ≤ f(uₙ) ≤ f(3)", "f(0) = √3", "f(3) = 3", "uₙ₊₁ = f(uₙ)"],
                 "pieges": ["f(0) ≤ uₙ₊₁ ≤ f(3) donc 0 ≤ uₙ₊₁ ≤ 3 sans calculer", "supposons que pour tout n"]},
     "aides": [aide("f(x) = √(2x + 3) : x ↦ 2x + 3 est croissante et la racine aussi, donc f est croissante sur [0 ; 3]. Applique f à l'encadrement.",
                    "f de x égale racine carrée de deux x plus trois. deux x plus trois croissante، والracine حتى هي، إذن f croissante sur zéro trois. طبق f على l'encadrement."),
               aide("Calcule f(0) et f(3), puis compare-les à 0 et à 3. Et f(uₙ) = uₙ₊₁.",
                    "حسب f de zéro وf de trois، وقارنهم مع zéro وtrois. وf de u indice n، هي u indice n plus un.")],
     "correction": correction([
         ("2 : Initialisation : u₀ = 0, donc 0 ≤ u₀ ≤ 3", "u zéro égale zéro"),
         ("Hérédité : supposons 0 ≤ uₙ ≤ 3 ; f est croissante sur [0 ; 3], donc f(0) ≤ f(uₙ) ≤ f(3)", "f croissante"),
         ("f(0) = √3 ≥ 0 et f(3) = √9 = 3 : 0 ≤ uₙ₊₁ ≤ 3", "f de trois égale trois"),
         ("Conclusion : d'après le principe de récurrence, 0 ≤ uₙ ≤ 3 pour tout n", "d'après le principe de récurrence")],
         "السؤال deux. initialisation: u zéro égale zéro، إذن بين zéro وtrois. hérédité: supposons que u indice n بين zéro وtrois. f croissante sur zéro trois، إذن f de zéro، inférieur ou égal à u indice n plus un، inférieur ou égal à f de trois. f de zéro égale racine carrée de trois، positif. وf de trois égale trois. إذن u indice n plus un بين zéro وtrois. d'après le principe de récurrence، pour tout n."),
     "explication": "ex_2", "facile": "fa_2"},
    {"id": "3-1", "texte": "Montrer que pour tout x de [0 ; 3] : f(x) − x = (3 − x)(x + 1)/(√(2x + 3) + x), puis en déduire que f(x) − x ≥ 0 sur [0 ; 3].",
     "texte_dit": "السؤال trois un: بين بلي، pour tout x من zéro حتى ل trois، f de x moins x، égale، trois moins x، fois، x plus un، sur، racine carrée de deux x plus trois، plus x. ومن بعد استنتج بلي f de x moins x positif sur zéro trois.",
     "reponse": phrase("f(x) − x = (√(2x + 3) − x)(√(2x + 3) + x)/(√(2x + 3) + x) = (2x + 3 − x²)/(√(2x + 3) + x) = (3 − x)(x + 1)/(√(2x + 3) + x). Sur [0 ; 3] : 3 − x ≥ 0, x + 1 > 0, √(2x + 3) + x > 0, donc f(x) − x ≥ 0."),
     "clavier": {"aides": ["conjugué : √(2x + 3) + x", "2x + 3 − x²", "(3 − x)(x + 1)", "3 − x ≥ 0", "√(2x + 3) + x > 0"],
                 "pieges": ["(3 − x)(x − 1)", "f(x) − x ≤ 0"]},
     "aides": [aide("Multiplie et divise par le conjugué √(2x + 3) + x : (A − B)(A + B) = A² − B².",
                    "ضرب وقسم على le conjugué: racine carrée de deux x plus trois، plus x. A moins B، fois، A plus B، égale A carré moins B carré."),
               aide("2x + 3 − x² = −(x² − 2x − 3) : ses racines sont 3 et −1. Puis un signe sous chaque facteur, x entre 0 et 3.",
                    "deux x plus trois moins x carré: les racines ديالو trois وmoins un. ومن بعد signe تحت كل facteur، وx بين zéro وtrois.")],
     "correction": correction([
         ("3-1 : f(x) − x = (√(2x + 3) − x)(√(2x + 3) + x)/(√(2x + 3) + x)", "le conjugué"),
         ("= (2x + 3 − x²)/(√(2x + 3) + x) = (3 − x)(x + 1)/(√(2x + 3) + x)", "trois moins x، fois، x plus un"),
         ("sur [0 ; 3] : 3 − x ≥ 0, x + 1 > 0, √(2x + 3) + x > 0, donc f(x) − x ≥ 0", "f de x moins x positif")],
         "السؤال trois un. نضربو ونقسمو على le conjugué، racine carrée de deux x plus trois، plus x. الفوق كيولي deux x plus trois moins x carré، يعني، trois moins x، fois، x plus un. sur zéro trois: trois moins x positif، x plus un positif، والتحت positif. إذن f de x moins x positif."),
     "explication": "ex_3", "facile": "fa_3"},
    {"id": "3-2", "texte": "En déduire que la suite (uₙ) est croissante.",
     "texte_dit": "السؤال trois deux: استنتج بلي la suite croissante.",
     "reponse": phrase("D'après 2, uₙ ∈ [0 ; 3] ; or f(x) − x ≥ 0 sur [0 ; 3] (3-1), donc f(uₙ) − uₙ ≥ 0, c'est-à-dire uₙ₊₁ − uₙ ≥ 0 pour tout n : (uₙ) est croissante."),
     "clavier": {"aides": ["uₙ ∈ [0 ; 3]", "x = uₙ", "f(uₙ) − uₙ ≥ 0", "uₙ₊₁ − uₙ ≥ 0"], "pieges": ["f croissante donc (uₙ) croissante"]},
     "aides": [aide("Tu sais le signe de f(x) − x pour x dans [0 ; 3]. Où sont tous les uₙ ?",
                    "كتعرف le signe ديال f de x moins x، ملي x بين zéro وtrois. وفين كاينين كاع les u indice n؟"),
               aide("Remplace x par uₙ : f(uₙ) = uₙ₊₁. Attention : « f croissante » ne dit pas le sens de (uₙ).",
                    "عوض x ب u indice n: f de u indice n هي u indice n plus un. رد البال: f croissante ما كتقولش le sens ديال la suite.")],
     "correction": correction([
         ("3-2 : d'après 2, uₙ ∈ [0 ; 3] ; d'après 3-1, f(x) − x ≥ 0 sur [0 ; 3]", "d'après le deux"),
         ("donc f(uₙ) − uₙ ≥ 0, soit uₙ₊₁ − uₙ ≥ 0 pour tout n", "u indice n plus un moins u indice n positif"),
         ("(uₙ) est croissante", "croissante")],
         "السؤال trois deux. d'après le deux، u indice n بين zéro وtrois. ومن trois un، f de x moins x positif على هاد l'intervalle. نعوضو x ب u indice n: u indice n plus un moins u indice n positif pour tout n. إذن la suite croissante."),
     "explication": "ex_4", "facile": "fa_4"},
    {"id": "4", "texte": "Montrer que la suite (uₙ) est convergente, puis calculer sa limite.",
     "texte_dit": "السؤال quatre: بين بلي la suite convergente، ومن بعد حسب la limite ديالها.",
     "reponse": valeur("lim uₙ", 3, "(uₙ) croissante et majorée par 3, donc convergente ; f continue sur I = [0 ; 3], f(I) ⊂ I, u₀ ∈ I, donc ℓ = f(ℓ) : √(2ℓ + 3) = ℓ ⇔ ℓ² − 2ℓ − 3 = 0 et ℓ ≥ 0, donc ℓ = 3 (−1 ∉ I) ; lim uₙ = 3"),
     "clavier": {"aides": ["croissante et majorée", "f continue sur I", "f(I) ⊂ I", "u₀ ∈ I", "ℓ = f(ℓ)", "ℓ² − 2ℓ − 3 = 0"],
                 "pieges": ["ℓ = −1", "f(I) = I"]},
     "aides": [aide("Convergente : quel couple as-tu (questions 2 et 3-2) ? Pour la limite : ℓ est solution de f(x) = x, si les conditions sont écrites.",
                    "convergente: شنو هو الكوبل اللي عندك، من deux ومن trois deux؟ وla limite: ℓ هي solution ديال f de x égale x، يلا كتبنا les conditions."),
               aide("Conditions : f continue sur I = [0 ; 3], f(I) ⊂ I, u₀ ∈ I. Puis √(2x + 3) = x ⇔ x² = 2x + 3 avec x ≥ 0 ; garde la solution de I.",
                    "les conditions: f continue sur I، f de I inclus dans I، وu zéro dans I. ومن بعد x carré égale deux x plus trois، مع x positif. خلي غير la solution اللي فI.")],
     "correction": correction([
         ("4 : (uₙ) est croissante (3-2) et majorée par 3 (2), donc convergente ; notons ℓ sa limite", "croissante et majorée par trois"),
         ("f est continue sur I = [0 ; 3], f(I) = [√3 ; 3] ⊂ I et u₀ = 0 ∈ I, donc ℓ = f(ℓ)", "les conditions"),
         ("√(2ℓ + 3) = ℓ ⇔ ℓ² − 2ℓ − 3 = 0 et ℓ ≥ 0 ⇔ (ℓ − 3)(ℓ + 1) = 0 et ℓ ≥ 0", "ℓ carré moins deux ℓ moins trois"),
         ("ℓ = 3 (car −1 ∉ [0 ; 3]) : lim uₙ = 3", "la limite égale trois")],
         "السؤال quatre. la suite croissante et majorée par trois، donc convergente. les conditions: f continue sur zéro trois، l'image ديال zéro trois هي racine carrée de trois، trois، وهي incluse، وu zéro dans I. إذن ℓ égale f de ℓ. يعني ℓ carré moins deux ℓ moins trois égale zéro، وℓ positif. les solutions: trois ولا moins un، وmoins un ماشي فI. إذن la limite égale trois."),
     "explication": "ex_5", "facile": "fa_5"},
]

EXPLICATION = deck("explication", "Explication animée", [
    sim("ex_1", "Question 1 : construire et lire l'escalier", "On monte à la courbe, on va à la droite y = x, on descend sur l'axe : c'est u₁.",
        S + "escalier.html?vue=escalier", "L'escalier sur l'exemple du cours : f(x) = 2x/(x + 1)",
        "نشوفو la méthode على l'exemple ديال le cours: f de x égale deux x sur x plus un، وla droite y égale x. نحطو u zéro égale zéro virgule cinq على l'axe des abscisses. نطلعو حتى ل la courbe: هادي f de u zéro. نمشيو أفقيا حتى ل la droite. ونهبطو للمحور: هادا u un égale zéro virgule six six sept. ومن بعد u deux égale zéro virgule huit. الدروج كيطلعو وكيقربو من النقطة فين la courbe كتقطع la droite. فla figure ديالنا نفس الشي: الدروج كيطلعو نحو trois.",
        [("u₀ < u₁ < u₂ : croissante", "الدروج كيطلعو وكيقربو"), ("limite : abscisse du point d'intersection", "فla figure ديالنا")],
        [regle("نشوفو la méthode", u0=0.5), jusqua("وla droite y égale x", "courbe_et_droite"), jusqua("نحطو u zéro", "placer_u0"),
         jusqua("نطلعو حتى ل la courbe", "monter_courbe"), jusqua("نمشيو أفقيا", "aller_droite"), jusqua("ونهبطو للمحور", "descendre_u1"),
         jusqua("ومن بعد u deux", "repeter"), montre("الدروج كيطلعو وكيقربو", "centre:0"), jusqua("فla figure ديالنا", "conjecture"),
         montre("فla figure ديالنا", "centre:1")]),
    sim("ex_2", "Question 2 : f croissante garde l'ordre", "x dans [a ; b] ⇒ f(x) dans [f(a) ; f(b)], puis on compare f(a) à a et f(b) à b.",
        S + "escalier.html?vue=boite", "L'intervalle [1 ; 2] envoyé dans [1 ; 4/3]",
        "فl'exemple: f croissante. ناخدو x بين un وdeux. f de un égale un، وf de deux égale quatre sur trois. إذن f de x بين un وquatre sur trois، وهاد l'intervalle داخل un deux. عندنا نفس الشي: f croissante sur zéro trois. f de zéro égale racine carrée de trois، وf de trois égale trois. إذن u indice n plus un بين racine carrée de trois وtrois، يعني بين zéro وtrois.",
        [("f croissante : f(0) ≤ f(uₙ) ≤ f(3)", "عندنا نفس الشي"), ("f(0) = √3 ≥ 0 ; f(3) = 3", "f de zéro égale racine carrée de trois")],
        [jusqua("فl'exemple: f croissante", "courbe"), jusqua("ناخدو x بين un وdeux", "boite_x"), jusqua("f de un égale un", "images"),
         jusqua("إذن f de x بين un", "boite_y"), montre("عندنا نفس الشي", "centre:0"), montre("f de zéro égale racine carrée de trois", "centre:1")]),
    sim("ex_3", "Question 3-1 : le signe de f(x) − x", "On écrit f(x) − x en produit, puis un signe sous chaque facteur.",
        S + "national.html?vue=g_signe", "Le signe de g(x) − x dans l'exemple du cours",
        "فl'exemple ديال le cours: g de x égale، quatre x plus trois، sur x plus deux. g de x moins x، ملي كنحسبوها، كتعطي، trois moins x، fois، x plus un، sur x plus deux. ومن بعد le tableau: trois moins x positif، x plus un positif، x plus deux positif. إذن g de x moins x positif. عندنا: كنضربو فle conjugué، وكنلقاو، trois moins x، fois، x plus un، sur racine carrée de deux x plus trois، plus x. نفس الفوق، والتحت positif. إذن f de x moins x positif sur zéro trois.",
        [("f(x) − x = (3 − x)(x + 1)/(√(2x + 3) + x)", "عندنا: كنضربو فle conjugué"), ("f(x) − x ≥ 0 sur [0 ; 3]", "إذن f de x moins x positif sur zéro trois")],
        [jusqua("فl'exemple ديال le cours", "courbe_et_droite"), jusqua("ملي كنحسبوها", "difference"), jusqua("كتعطي، trois moins x", "factorise"),
         jusqua("ومن بعد le tableau", "tableau"), jusqua("trois moins x positif", "signe_3mx"), jusqua("x plus un positif", "signe_xp1"),
         jusqua("x plus deux positif", "signe_xp2"), jusqua("إذن g de x moins x positif", "signe_g"),
         montre("عندنا: كنضربو فle conjugué", "centre:0"), montre("إذن f de x moins x positif sur zéro trois", "centre:1")]),
    sim("ex_4", "Question 3-2 : la courbe au-dessus de la droite", "uₙ dans I et f(x) ≥ x sur I : uₙ₊₁ ≥ uₙ.",
        S + "national.html?vue=g_signe", "La zone entre la courbe et la droite, puis l'escalier qui monte",
        "شوف هاد المنطقة الخضرا: la courbe فوق la droite، يعني g de x أكبر من x. والدروج كيطلعو: u un égale sept sur trois، u deux قريب من deux virgule huit cinq. حيت كل u indice n فهاد l'intervalle، كنعوضو x ب u indice n: u indice n plus un moins u indice n positif. عندنا نفس الشي: u indice n بين zéro وtrois، وf de x moins x positif. إذن la suite croissante.",
        [("uₙ ∈ [0 ; 3] et f(x) − x ≥ 0", "عندنا نفس الشي"), ("uₙ₊₁ − uₙ = f(uₙ) − uₙ ≥ 0", "إذن la suite croissante")],
        [jusqua("شوف هاد المنطقة الخضرا", "zone"), jusqua("والدروج كيطلعو", "escalier"), jusqua("كنعوضو x ب u indice n", "conclusion"),
         montre("عندنا نفس الشي", "centre:0"), montre("إذن la suite croissante", "centre:1")]),
    sim("ex_5", "Question 4 : choisir ℓ dans l'intervalle", "ℓ = f(ℓ) peut avoir deux solutions : on garde celle de I.",
        S + "escalier.html?vue=point", "Deux points d'intersection : on garde celui de l'intervalle",
        "فl'exemple: la courbe كتقطع la droite فجوج نقط: zéro، وun. ولكن les termes كاملين فun deux. إذن zéro ما ينفعش، وℓ égale un. عندنا: الأول les conditions: f continue sur zéro trois، l'image داخل l'intervalle، وu zéro فيه. ومن بعد ℓ égale f de ℓ: ℓ carré moins deux ℓ moins trois égale zéro. trois ولا moins un. moins un ماشي فzéro trois. إذن la limite égale trois.",
        [("f continue sur I, f(I) ⊂ I, u₀ ∈ I", "الأول les conditions"), ("ℓ² − 2ℓ − 3 = 0 : ℓ = 3 ou ℓ = −1", "trois ولا moins un"),
         ("−1 ∉ [0 ; 3] : ℓ = 3", "إذن la limite égale trois")],
        [jusqua("فl'exemple: la courbe كتقطع la droite", "point_intersection"), jusqua("ولكن les termes كاملين", "intervalle"),
         jusqua("إذن zéro ما ينفعش", "choix"), montre("الأول les conditions", "centre:0"), montre("trois ولا moins un", "centre:1"),
         montre("إذن la limite égale trois", "centre:2")]),
])

FACILE = deck("facile", "Plus facile, pour s'entraîner", [
    qcm("fa_1", "Plus facile : où lire les termes ?", "نتمرنو: فين كنقراو les termes؟",
        "Dans la construction en escalier, les termes u₀, u₁, u₂ se lisent…", ["sur l'axe des ordonnées", "sur l'axe des abscisses", "sur la courbe"], 1, [
            (("ما تقلقش. la droite y égale x كترجع la valeur لl'axe des abscisses. عاود اختار.", "La droite y = x ramène la valeur sur l'axe des abscisses. Réessaie."),
             ("الجواب هو l'axe des abscisses.", "Réponse : sur l'axe des abscisses.")),
            ("برافو! les termes كنحطوهم على l'axe des abscisses، وla droite y égale x كتعاونا.", "Juste : sur l'axe des abscisses."),
            (("قريب! la courbe كتعطي l'image، ولكن الterme كنحطوه على المحور. عاود اختار.", "La courbe donne l'image ; le terme se place sur l'axe. Réessaie."),
             ("الجواب هو l'axe des abscisses.", "Réponse : sur l'axe des abscisses."))],
        "Dans la construction en escalier، les termes se lisent où ?"),
    vrai_faux("fa_2", "Plus facile : vrai ou faux", "f(x) = √(2x + 3) est croissante sur [0 ; 3] ; on suppose 0 ≤ uₙ ≤ 3.",
        "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
            ("f(0) ≤ f(uₙ) ≤ f(3), car f est croissante.", True, "Une fonction croissante garde l'ordre."),
            ("f(0) = 0.", False, "f(0) = √3 ≈ 1,73 ; il est bien ≥ 0."),
            ("f(3) = 3, donc uₙ₊₁ ≤ 3.", True, "f(3) = √9 = 3.")]),
    association("fa_3", "Plus facile : le signe de chaque facteur", "Pour x dans [0 ; 3], relie chaque facteur à son signe.",
        "سؤال ساهل: ربط كل facteur مع le signe ديالو، ملي x بين zéro وtrois.", "Pour x ∈ [0 ; 3], relie chaque facteur à son signe.",
        [("1", "3 − x"), ("2", "x + 1"), ("3", "√(2x + 3) + x")],
        [("a", "positif ou nul (nul en 3)"), ("b", "strictement positif"), ("c", "négatif")],
        {"1": "a", "2": "b", "3": "b"},
        {"1-a": ("Oui : x ≤ 3 donne 3 − x ≥ 0, et 0 en x = 3.", "برافو: x صغير من trois، إذن trois moins x positif، وzéro فtrois."),
         "1-b": ("Presque : en x = 3, il vaut 0.", "قريب، ولكن فx égale trois كيساوي zéro."),
         "1-c": ("Non : x ≤ 3, donc 3 − x ≥ 0.", "لا، x صغير من trois، إذن trois moins x positif."),
         "2-a": ("Il ne s'annule pas sur [0 ; 3] : x + 1 ≥ 1.", "لا، ما كيوليش zéro: x plus un ديما أكبر من un."),
         "2-b": ("Oui : x ≥ 0 donne x + 1 ≥ 1 > 0.", "برافو: x positif، إذن x plus un أكبر من zéro."),
         "2-c": ("Non : x ≥ 0, donc x + 1 > 0.", "لا، x positif، إذن x plus un positif."),
         "3-a": ("Il ne s'annule pas : √(2x + 3) ≥ √3 > 0.", "لا، ما كيوليش zéro: la racine ديما أكبر من zéro."),
         "3-b": ("Oui : une racine positive plus x ≥ 0.", "برافو: racine positive، زائد x positif."),
         "3-c": ("Non : une racine est positive, et x ≥ 0.", "لا، la racine positive، وx positif.")},
        ("(1 ; a) (2 ; b) (3 ; b) : donc f(x) − x ≥ 0 sur [0 ; 3].", "إذن f de x moins x positif sur zéro trois.")),
    qcm("fa_4", "Plus facile : d'où vient le sens de (uₙ) ?", "سؤال ساهل: منين كيجي le sens ديال la suite؟",
        "uₙ ∈ [0 ; 3] et f(x) ≥ x sur [0 ; 3]. Alors…", ["uₙ₊₁ ≥ uₙ : croissante", "uₙ₊₁ ≤ uₙ : décroissante", "on ne peut rien dire"], 0, [
            ("برافو! f de u indice n أكبر من u indice n، يعني u indice n plus un أكبر من u indice n.", "Juste : f(uₙ) ≥ uₙ."),
            (("ما تقلقش. f de x أكبر من x، إذن u indice n plus un أكبر من u indice n. عاود اختار.", "f(x) ≥ x donne uₙ₊₁ ≥ uₙ. Réessaie."),
             ("الجواب هو croissante.", "Réponse : croissante.")),
            (("قريب! u indice n فI، إذن نقدرو نعوضو x ب u indice n. عاود اختار.", "uₙ ∈ I : on peut prendre x = uₙ. Réessaie."),
             ("الجواب هو croissante.", "Réponse : croissante."))],
        "u indice n dans zéro trois، et f de x supérieur ou égal à x. Alors quoi ?"),
    qcm("fa_5", "Plus facile : choisir ℓ", "سؤال ساهل: اختار ℓ.",
        "ℓ² − 2ℓ − 3 = 0 donne ℓ = 3 ou ℓ = −1, et 0 ≤ uₙ ≤ 3. Alors ℓ = …", ["−1", "3", "0"], 1, [
            (("ما تقلقش. les termes كاملين بين zéro وtrois، إذن la limite حتى هي بين zéro وtrois. عاود اختار.", "La limite est dans [0 ; 3]. Réessaie."),
             ("الجواب هو trois: moins un ماشي فl'intervalle.", "Réponse : ℓ = 3 ; −1 ∉ [0 ; 3].")),
            ("برافو! trois فl'intervalle، وmoins un لا.", "Juste : ℓ = 3."),
            (("قريب! zéro ماشي solution ديال l'équation. عاود اختار.", "0 n'est pas solution. Réessaie."),
             ("الجواب هو trois.", "Réponse : ℓ = 3."))],
        "Les solutions sont trois ou moins un. Alors ℓ égale quoi ?"),
])

ENONCE = {
    "intro": "Soit f la fonction définie sur [−3/2 ; +∞[ par f(x) = √(2x + 3), (C_f) sa courbe et (Δ) la droite d'équation y = x. On considère la suite (uₙ) définie par u₀ = 0 et uₙ₊₁ = f(uₙ) pour tout entier naturel n.",
    "intro_dit": "دابا نقراو l'énoncé. f de x égale racine carrée de deux x plus trois. C f هي la courbe ديالها، وdelta هي la droite y égale x. والsuite: u zéro égale zéro، وu indice n plus un égale f de u indice n، pour tout n.",
    "figures": [figure(2, 3, 3, "f")],
    "donnees": ["f(x) = √(2x + 3)", "u₀ = 0 ; uₙ₊₁ = f(uₙ)", "(Δ) : y = x"],
    "questions": QUESTIONS,
}

SIMILAIRE = {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
        "intro": "Soit g(x) = √(3x + 4), (C_g) sa courbe et (Δ) : y = x. On considère la suite (uₙ) définie par u₀ = 0 et uₙ₊₁ = g(uₙ).",
        "intro_dit": "نفس التمرين، بدالة أخرى: g de x égale racine carrée de trois x plus quatre، u zéro égale zéro، وu indice n plus un égale g de u indice n.",
        "figures": [figure(3, 4, 4, "g")],
        "donnees": ["g(x) = √(3x + 4)", "u₀ = 0 ; uₙ₊₁ = g(uₙ)"],
        "questions": [
            {"id": "1", "texte": "En utilisant la figure, conjecturer le sens de variation de (uₙ) et sa limite.",
             "reponse": phrase("u₀ < u₁ < u₂ : (uₙ) semble croissante et converger vers 4, abscisse du point d'intersection de (C_g) et (Δ)."),
             "clavier": {"aides": ["croissante", "converge vers 4"], "pieges": ["axe des ordonnées"]},
             "correction": correction([("1 : (uₙ) semble croissante et converger vers 4", "semble croissante")],
                                      "على la figure، les termes كيمشيو لليمين: la suite semble croissante، وكتقرب من quatre.")},
            {"id": "2", "texte": "Montrer par récurrence que 0 ≤ uₙ ≤ 4 pour tout n.",
             "reponse": phrase("u₀ = 0 ; si 0 ≤ uₙ ≤ 4, g croissante donne g(0) = 2 ≤ uₙ₊₁ ≤ g(4) = 4, donc 0 ≤ uₙ₊₁ ≤ 4. Donc 0 ≤ uₙ ≤ 4 pour tout n."),
             "clavier": {"aides": ["g croissante sur [0 ; 4]", "g(0) = 2", "g(4) = 4"], "pieges": ["sans calculer g(0) et g(4)"]},
             "correction": correction([("2 : u₀ = 0 ∈ [0 ; 4]", "u zéro égale zéro"), ("g croissante : g(0) = 2 ≤ uₙ₊₁ ≤ g(4) = 4", "g croissante"),
                                       ("d'après le principe de récurrence, 0 ≤ uₙ ≤ 4", "d'après le principe de récurrence")],
                                      "u zéro égale zéro. supposons u indice n بين zéro وquatre. g croissante: g de zéro égale deux، وg de quatre égale quatre. d'après le principe de récurrence، u indice n بين zéro وquatre.")},
            {"id": "3-1", "texte": "Montrer que pour x ∈ [0 ; 4] : g(x) − x = (4 − x)(x + 1)/(√(3x + 4) + x), et en déduire que g(x) − x ≥ 0 sur [0 ; 4].",
             "reponse": phrase("g(x) − x = (3x + 4 − x²)/(√(3x + 4) + x) = (4 − x)(x + 1)/(√(3x + 4) + x) ≥ 0 sur [0 ; 4]."),
             "clavier": {"aides": ["conjugué", "(4 − x)(x + 1)"], "pieges": ["(4 − x)(x − 1)"]},
             "correction": correction([("3-1 : g(x) − x = (3x + 4 − x²)/(√(3x + 4) + x) = (4 − x)(x + 1)/(√(3x + 4) + x)", "le conjugué"),
                                       ("chaque facteur ≥ 0 sur [0 ; 4] : g(x) − x ≥ 0", "positif")],
                                      "le conjugué كيعطي، quatre moins x، fois، x plus un، sur racine carrée de trois x plus quatre، plus x. كل facteur positif sur zéro quatre.")},
            {"id": "3-2", "texte": "En déduire que (uₙ) est croissante.",
             "reponse": phrase("uₙ ∈ [0 ; 4] et g(x) − x ≥ 0 sur [0 ; 4], donc uₙ₊₁ − uₙ = g(uₙ) − uₙ ≥ 0 : (uₙ) croissante."),
             "clavier": {"aides": ["x = uₙ", "uₙ₊₁ − uₙ ≥ 0"], "pieges": ["g croissante donc (uₙ) croissante"]},
             "correction": correction([("3-2 : uₙ ∈ [0 ; 4], donc g(uₙ) − uₙ ≥ 0 : uₙ₊₁ ≥ uₙ ; (uₙ) croissante", "croissante")],
                                      "u indice n بين zéro وquatre، إذن u indice n plus un moins u indice n positif: la suite croissante.")},
            {"id": "4", "texte": "Montrer que (uₙ) est convergente, puis calculer sa limite.",
             "reponse": valeur("lim uₙ", 4, "croissante et majorée par 4 : convergente ; g continue sur I = [0 ; 4], g(I) ⊂ I, u₀ ∈ I : ℓ² − 3ℓ − 4 = 0 et ℓ ≥ 0, donc ℓ = 4 ; lim uₙ = 4"),
             "clavier": {"aides": ["croissante et majorée", "g(I) ⊂ I", "ℓ = g(ℓ)"], "pieges": ["ℓ = −1"]},
             "correction": correction([("4 : croissante et majorée par 4, donc convergente", "convergente"),
                                       ("g continue sur [0 ; 4], g([0 ; 4]) = [2 ; 4] ⊂ [0 ; 4], u₀ ∈ [0 ; 4] : ℓ = g(ℓ)", "les conditions"),
                                       ("ℓ² − 3ℓ − 4 = 0 ⇔ ℓ = 4 ou ℓ = −1 ; −1 ∉ [0 ; 4] : lim uₙ = 4", "la limite égale quatre")],
                                      "croissante et majorée par quatre: convergente. les conditions: g continue، l'image داخل l'intervalle، وu zéro فيه. ℓ carré moins trois ℓ moins quatre égale zéro: quatre ولا moins un. إذن la limite égale quatre.")},
        ]}}

EX = {"id": ID, "type": "exercice", "version": 1, "status": "published", "matiere": "mathematiques",
      "chapitre": "suites_definition", "cours": "math_ch3_suites_numeriques",
      "titre": "Une suite uₙ₊₁ = f(uₙ) avec une racine : escalier, récurrence, monotonie et limite", "niveau": "moyen", "duree_min": 35,
      "origine": ORIGINE,
      "competences": ["Représenter les termes et conjecturer", "Encadrer uₙ par récurrence avec la croissance de f",
                      "Étudier la monotonie par le signe de f(x) − x", "Calculer la limite par ℓ = f(ℓ) avec ses conditions"],
      "enonce": ENONCE, "explication": EXPLICATION, "facile": FACILE, "similaire": SIMILAIRE}



def dire_l(o, k=""):
    """ℓ se dit « L » : on le remplace dans les textes dits (les textes écrits gardent ℓ)."""
    if isinstance(o, dict):
        return {kk: dire_l(v, kk) for kk, v in o.items()}
    if isinstance(o, list):
        return [dire_l(v, k) for v in o]
    if isinstance(o, str) and k in {"mixed", "dit", "parole", "intro_dit", "texte_dit", "enonce_dit", "mot"}:
        return o.replace("ℓ", "L")
    return o


if __name__ == "__main__":
    ecrire(dire_l(EX))
