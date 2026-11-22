# Exercice de maths, ch. 3 (suites numériques), niveau moyen (niveau du national) : uₙ₊₁ = a·uₙ + b.
# Sources comparées (lecture seule, rien de recopié) :
#  - exploration suites_definition.json : redaction_nationale recurrence_affine, monotonie_difference, convergence,
#    suite_auxiliaire_geometrique ; erreurs_examen « mauvais couple », « lim qⁿ sans la condition −1 < q < 1 »,
#    « on écrit uₙ = u₀qⁿ alors que (uₙ) n'est pas géométrique » ; frequences_examens (11 exercices indépendants sur 20) ;
#  - vidéos : Driss DOTCOM RRRnDJ2bdlc et uFRQ1Q4-X3E (habiller l'hypothèse : × puis +), maths variés wXGsw_meVIM (barème),
#    Mouad Tahiri b7iH3KUEoZc (factoriser par (uₙ − ℓ)), MedBrahmi fSulj1kZQ0g (suite auxiliaire, revenir à uₙ),
#    Rabie Ghazouani 4YsAlmrILpE (national 2016) ;
#  - nationaux : 2016 R (u₀ = 2, uₙ₊₁ = uₙ/16 + 15/16), 2017 R (u₀ = 17, uₙ₊₁ = uₙ/4 + 12), 2022 R (√2/2) : même suite de
#    questions (récurrence, monotonie, convergence, vₙ, uₙ, limite), suite décroissante ; ici la suite MONTE vers 9 ;
#  - séries en ligne (résultats de recherche, pages non ouvertes : réseau fermé) : talamidi 2 bac PC série corrigée 3,
#    moutamadris 2 bac PC/SVT série 1, fayssalmaths série 3 « suite 2 BIOF », pdfmath exercices nationaux corrigés,
#    xriadiat exercices corrigés suites.
# Données propres à Moalim : u₀ = 2, uₙ₊₁ = (2/3)uₙ + 3, ℓ = 9 ; vₙ = 9 − uₙ (v₀ = 7, q = 2/3).
import sys
from fractions import Fraction as Fr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa: E402,F401,F403

ID = "math_ex_ch3_suites_3"
S = "/media/simulations/maths/suites-tableau/"


def nuage(u0, a, b, l, nom):
    u = [Fr(u0)]
    for _ in range(5):
        u.append(Fr(a) * u[-1] + b)
    el = [{"f": "repere", "y": l, "t": f"y = {l}", "couleur": "orange"}]
    for k, v in enumerate(u):
        el.append({"f": "point", "at": [k, round(float(v), 3)], "couleur": "cyan", "t": f"u{'₀₁₂₃₄₅'[k]}" if k < 3 else None, "pos": "se"})
    for e in el:
        if e.get("t") is None:
            e.pop("t", None)
    return {"type": "courbe", "titre": f"Les premiers termes de ({nom}) : les points (n ; uₙ)",
            "axes": {"x": {"min": 0, "max": 6, "nom": "n", "graduations": [1, 2, 3, 4, 5]},
                     "y": {"min": 0, "max": l + 1, "nom": "uₙ", "graduations": list(range(0, l + 2, 1 if l < 8 else 3))}},
            "legende": f"Les points montent et restent sous la droite y = {l}.", "elements": el}


QUESTIONS = [
    {"id": "1", "texte": "Montrer par récurrence que uₙ < 9 pour tout entier naturel n.",
     "texte_dit": "السؤال un: بين par récurrence بلي u indice n inférieur à neuf، pour tout n.",
     "reponse": phrase("Initialisation : u₀ = 2 < 9. Hérédité : soit n ∈ ℕ, supposons uₙ < 9 ; alors (2/3)uₙ < 6 (car 2/3 > 0), donc (2/3)uₙ + 3 < 9, c'est-à-dire uₙ₊₁ < 9. Conclusion : d'après le principe de récurrence, uₙ < 9 pour tout n ∈ ℕ."),
     "clavier": {"aides": ["Initialisation : u₀ = 2 < 9", "supposons uₙ < 9", "(2/3)uₙ < 6", "+ 3", "Conclusion"],
                 "pieges": ["supposons que pour tout n", "(2/3)uₙ < 9"]},
     "aides": [aide("Écris les trois titres. À l'hérédité, la formule fait deux opérations sur uₙ : lesquelles, et dans quel ordre ?",
                    "كتب تلاتة ديال العناوين. فl'hérédité، la formule كدير جوج عمليات على u indice n: شنو هوما، وبأي ترتيب؟"),
               aide("Pars de uₙ < 9 : multiplie par 2/3 (positif : même sens), puis ajoute 3.",
                    "بدا من u indice n inférieur à neuf. ضرب فdeux sur trois، وهو positif، إذن نفس الاتجاه. ومن بعد زيد trois.")],
     "correction": correction([
         ("1 : Initialisation : pour n = 0, u₀ = 2 < 9", "u zéro égale deux"),
         ("Hérédité : soit n ∈ ℕ ; supposons uₙ < 9 et montrons uₙ₊₁ < 9", "supposons que u indice n"),
         ("2/3 > 0 : (2/3)uₙ < 6, donc (2/3)uₙ + 3 < 9 : uₙ₊₁ < 9", "inférieur à six"),
         ("Conclusion : d'après le principe de récurrence, pour tout n ∈ ℕ, uₙ < 9", "d'après le principe de récurrence")],
         "السؤال un. initialisation: u zéro égale deux، inférieur à neuf. hérédité: soit n، supposons que u indice n inférieur à neuf. deux sur trois positif، إذن deux sur trois u indice n، inférieur à six. نزيدو trois: u indice n plus un، inférieur à neuf. conclusion: d'après le principe de récurrence، u indice n inférieur à neuf pour tout n."),
     "explication": "ex_1", "facile": "fa_1"},
    {"id": "2-1", "texte": "Vérifier que uₙ₊₁ − uₙ = (1/3)(9 − uₙ) pour tout n, puis montrer que la suite (uₙ) est croissante.",
     "texte_dit": "السؤال deux un: تحقق بلي u indice n plus un moins u indice n، égale un sur trois، fois، neuf moins u indice n. ومن بعد بين بلي la suite croissante.",
     "reponse": phrase("uₙ₊₁ − uₙ = (2/3)uₙ + 3 − uₙ = −(1/3)uₙ + 3 = (1/3)(9 − uₙ). D'après 1, uₙ < 9, donc 9 − uₙ > 0 et uₙ₊₁ − uₙ > 0 pour tout n : (uₙ) est croissante."),
     "clavier": {"aides": ["(2/3 − 1)uₙ", "−(1/3)uₙ + 3", "(1/3)(9 − uₙ)", "9 − uₙ > 0", "uₙ₊₁ − uₙ > 0"], "pieges": ["u₁ > u₀ donc croissante", "(1/3)(uₙ − 9)"]},
     "aides": [aide("Remplace uₙ₊₁, regroupe les uₙ, puis mets 1/3 en facteur : 3 = (1/3) × 9.",
                    "عوض u indice n plus un، جمع les u indice n، ومن بعد خرج un sur trois en facteur. trois égale un sur trois fois neuf."),
               aide("Pour le signe : la question 1 dit où est uₙ par rapport à 9.",
                    "باش تعرف le signe: السؤال un كيقول فين كاين u indice n بالنسبة ل neuf.")],
     "correction": correction([
         ("2-1 : uₙ₊₁ − uₙ = (2/3)uₙ + 3 − uₙ = −(1/3)uₙ + 3 = (1/3)(9 − uₙ)", "un sur trois، fois، neuf moins u indice n"),
         ("d'après 1, uₙ < 9, donc 9 − uₙ > 0 : uₙ₊₁ − uₙ > 0 pour tout n", "d'après le un"),
         ("donc la suite (uₙ) est croissante", "croissante")],
         "السؤال deux un. deux sur trois u indice n plus trois moins u indice n، égale moins un sur trois u indice n plus trois، égale un sur trois، fois، neuf moins u indice n. d'après le un، u indice n inférieur à neuf، إذن neuf moins u indice n positif. la différence positive pour tout n: la suite croissante."),
     "explication": "ex_2", "facile": "fa_2"},
    {"id": "2-2", "texte": "En déduire que la suite (uₙ) est convergente.",
     "texte_dit": "السؤال deux deux: استنتج بلي la suite convergente.",
     "reponse": phrase("(uₙ) est croissante (question 2-1) et majorée par 9 (question 1), donc elle est convergente."),
     "clavier": {"aides": ["croissante", "majorée par 9", "donc convergente"], "pieges": ["minorée", "converge vers 9 car majorée par 9"]},
     "aides": [aide("Une suite qui monte converge si elle a un plafond. Quel plafond a-t-on montré ?",
                    "suite كتطلع، كتكون convergente يلا عندها سقف. شنو هو السقف اللي بيناه؟"),
               aide("Cite les deux résultats : croissante (2-1) et majorée par 9 (1). Le plafond n'est pas forcément la limite.",
                    "عاود جوج نتائج: croissante، من deux un، وmajorée par neuf، من un. والسقف ماشي ضروري هو la limite.")],
     "correction": correction([
         ("2-2 : (uₙ) est croissante (2-1) et majorée par 9 (1)", "croissante et majorée par neuf"),
         ("donc (uₙ) est convergente", "donc convergente")],
         "السؤال deux deux. la suite croissante et majorée par neuf، donc convergente. ورد البال: majorée par neuf ما كتقولش بلي la limite هي neuf، la limite كتحسب."),
     "explication": "ex_3", "facile": "fa_3"},
    {"id": "3-1", "texte": "On pose vₙ = 9 − uₙ pour tout n. Montrer que (vₙ) est une suite géométrique de raison 2/3, et calculer v₀.",
     "texte_dit": "السؤال trois un: ناخدو v indice n égale neuf moins u indice n. بين بلي v indice n suite géométrique، la raison ديالها deux sur trois، وحسب v zéro.",
     "reponse": phrase("vₙ₊₁ = 9 − uₙ₊₁ = 9 − (2/3)uₙ − 3 = 6 − (2/3)uₙ = (2/3)(9 − uₙ) = (2/3)vₙ : (vₙ) est géométrique de raison 2/3 ; v₀ = 9 − u₀ = 7."),
     "clavier": {"aides": ["vₙ₊₁ = 9 − uₙ₊₁", "6 − (2/3)uₙ", "(2/3)(9 − uₙ)", "= (2/3)vₙ", "v₀ = 9 − u₀"],
                 "pieges": ["vₙ₊₁/vₙ sans vₙ ≠ 0", "v₀ = 9"]},
     "aides": [aide("Écris vₙ₊₁ = 9 − uₙ₊₁, puis remplace uₙ₊₁ par son expression. Le but : vₙ₊₁ = q × vₙ.",
                    "كتب v indice n plus un égale neuf moins u indice n plus un، ومن بعد عوض u indice n plus un. الهدف: v indice n plus un égale q fois v indice n."),
               aide("6 − (2/3)uₙ : mets 2/3 en facteur, car 6 = (2/3) × 9.",
                    "six moins deux sur trois u indice n: خرج deux sur trois en facteur، حيت six égale deux sur trois fois neuf.")],
     "correction": correction([
         ("3-1 : vₙ₊₁ = 9 − uₙ₊₁ = 9 − (2/3)uₙ − 3", "v indice n plus un égale neuf moins u indice n plus un"),
         ("= 6 − (2/3)uₙ = (2/3)(9 − uₙ) = (2/3)vₙ", "égale deux sur trois v indice n"),
         ("(vₙ) est géométrique de raison 2/3 ; v₀ = 9 − 2 = 7", "v zéro égale sept")],
         "السؤال trois un. v indice n plus un égale neuf moins u indice n plus un، يعني neuf moins deux sur trois u indice n moins trois، égale six moins deux sur trois u indice n. نخرجو deux sur trois: deux sur trois، fois، neuf moins u indice n، égale deux sur trois v indice n. إذن géométrique، la raison deux sur trois. وv zéro égale sept."),
     "explication": "ex_4", "facile": "fa_4"},
    {"id": "3-2", "texte": "Exprimer vₙ en fonction de n, puis montrer que uₙ = 9 − 7(2/3)ⁿ pour tout n.",
     "texte_dit": "السؤال trois deux: عبر على v indice n en fonction de n، ومن بعد بين بلي u indice n égale neuf moins sept fois deux sur trois، puissance n.",
     "reponse": phrase("vₙ = v₀ × qⁿ = 7(2/3)ⁿ ; et vₙ = 9 − uₙ donne uₙ = 9 − vₙ = 9 − 7(2/3)ⁿ."),
     "clavier": {"aides": ["vₙ = v₀ × qⁿ", "7(2/3)ⁿ", "uₙ = 9 − vₙ"], "pieges": ["uₙ = u₀ × (2/3)ⁿ", "uₙ = 9 + vₙ"]},
     "aides": [aide("(vₙ) est géométrique : vₙ = v₀ × qⁿ avec v₀ = 7 et q = 2/3.",
                    "v indice n géométrique: v indice n égale v zéro fois q puissance n، مع v zéro égale sept وq égale deux sur trois."),
               aide("Isole uₙ dans vₙ = 9 − uₙ : uₙ = 9 − vₙ. (uₙ) n'est pas géométrique, c'est (vₙ) qui l'est.",
                    "عزل u indice n: u indice n égale neuf moins v indice n. u indice n ماشي géométrique، v indice n هي اللي géométrique.")],
     "correction": correction([
         ("3-2 : vₙ = v₀ × qⁿ = 7(2/3)ⁿ", "v indice n égale sept fois"),
         ("vₙ = 9 − uₙ, donc uₙ = 9 − vₙ = 9 − 7(2/3)ⁿ", "u indice n égale neuf moins v indice n")],
         "السؤال trois deux. v indice n égale sept fois deux sur trois puissance n. وحيت v indice n égale neuf moins u indice n، u indice n égale neuf moins v indice n، يعني neuf moins sept fois deux sur trois puissance n."),
     "explication": "ex_5", "facile": "fa_5"},
    {"id": "3-3", "texte": "Calculer la limite de la suite (uₙ).",
     "texte_dit": "السؤال trois trois: حسب la limite ديال la suite u indice n.",
     "reponse": valeur("lim uₙ", 9, "−1 < 2/3 < 1, donc lim (2/3)ⁿ = 0 ; lim uₙ = 9 − 7 × 0 = 9"),
     "clavier": {"aides": ["−1 < 2/3 < 1", "lim (2/3)ⁿ = 0", "lim uₙ ="], "pieges": ["2/3 < 1 seulement", "lim uₙ = +∞"]},
     "aides": [aide("Que devient (2/3)ⁿ quand n devient très grand ? Écris d'abord la condition sur q.",
                    "شنو كيولي deux sur trois puissance n ملي n كيكبر بزاف؟ كتب الأول la condition على q."),
               aide("Si −1 < q < 1, lim qⁿ = 0. Puis remplace dans uₙ = 9 − 7(2/3)ⁿ.",
                    "يلا كان q بين moins un وun، la limite ديال q puissance n égale zéro. ومن بعد عوض فu indice n.")],
     "correction": correction([
         ("3-3 : −1 < 2/3 < 1, donc lim (2/3)ⁿ = 0", "moins un inférieur à deux sur trois"),
         ("lim uₙ = 9 − 7 × 0 = 9", "la limite égale neuf")],
         "السؤال trois trois. moins un inférieur à deux sur trois، inférieur à un، إذن la limite ديال deux sur trois puissance n، égale zéro. إذن la limite ديال u indice n، neuf moins sept fois zéro: la limite égale neuf."),
     "explication": "ex_6", "facile": "fa_6"},
]

EXPLICATION = deck("explication", "Explication animée", [
    sim("ex_1", "Question 1 : habiller l'hypothèse", "Multiplier par un positif, ajouter : le sens reste.",
        S + "rappels.html?vue=ordre_garde", "Ce qui garde le sens d'une inégalité",
        "شوف هاد الdroite: un inférieur à trois. نزيدو deux للجوج: trois inférieur à cinq، نفس الترتيب. نضربو fois deux، وdeux positif: deux inférieur à six، نفس الترتيب. هادي هي القاعدة. فl'hérédité ديالنا: u indice n inférieur à neuf. نضربو fois deux sur trois، وهو positif: inférieur à six. نزيدو trois: u indice n plus un، inférieur à neuf. كنديرو للinégalité نفس الشي اللي كديرو la formule ل u indice n.",
        [("uₙ < 9 ⇒ (2/3)uₙ < 6", "نضربو fois deux sur trois"), ("(2/3)uₙ + 3 < 9 : uₙ₊₁ < 9", "نزيدو trois")],
        [jusqua("شوف هاد الdroite", "depart"), jusqua("نزيدو deux للجوج", "ajoute"), jusqua("نضربو fois deux،", "fois"),
         jusqua("هادي هي القاعدة", "regle"), montre("نضربو fois deux sur trois", "centre:0"), montre("نزيدو trois", "centre:1")]),
    sim("ex_2", "Question 2-1 : le signe de la différence", "a > b ⇔ a − b > 0 : on étudie le signe de uₙ₊₁ − uₙ.",
        S + "rappels.html?vue=difference", "Comparer deux nombres par le signe de leur différence",
        "باش نقارنو جوج أعداد، كنحسبو la différence. cinq moins deux égale trois، positif: cinq أكبر. un moins quatre égale moins trois، négatif: un أصغر. القاعدة: a supérieur à b، يعني a moins b positif. عندنا u indice n plus un moins u indice n، égale un sur trois، fois، neuf moins u indice n. ومن السؤال un، u indice n inférieur à neuf، إذن neuf moins u indice n positif. la différence positive: la suite croissante.",
        [("a > b ⇔ a − b > 0", "القاعدة"), ("uₙ₊₁ − uₙ = (1/3)(9 − uₙ) > 0", "la différence positive")],
        [jusqua("cinq moins deux égale trois", "positif"), jusqua("un moins quatre", "negatif"), jusqua("القاعدة", "regle"),
         montre("القاعدة", "centre:0"), montre("la différence positive", "centre:1")]),
    sim("ex_3", "Question 2-2 : le bon couple", "Croissante et majorée, ou décroissante et minorée : convergente.",
        S + "plafond.html?vue=couple", "Monte avec un plafond, descend avec un plancher",
        "على اليسار: suite كتطلع، وفوقها سقف. ما تقدرش تدوز السقف، إذن كتوقف تحتو: convergente. على اليمين: suite كتهبط، وتحتها أرضية: حتى هي convergente. ولكن croissante et minorée، ما كتعطي والو، بحال n carré. عندنا la suite croissante، وmajorée par neuf: هادا هو الكوبل الصحيح. إذن convergente.",
        [("croissante et majorée ⇒ convergente", "هادا هو الكوبل الصحيح"), ("(uₙ) croissante, uₙ < 9", "عندنا la suite croissante")],
        [jusqua("على اليسار", "croissante_majoree"), jusqua("على اليمين", "miroir_decroissante"),
         jusqua("ولكن croissante et minorée", "mauvais_couple"), montre("عندنا la suite croissante", "centre:1"),
         jusqua("هادا هو الكوبل الصحيح", "regle"), montre("هادا هو الكوبل الصحيح", "centre:0")]),
    sim("ex_4", "Question 3-1 : la suite auxiliaire", "Ce qui dépasse la limite, ou ce qui manque, est multiplié par le même nombre.",
        S + "axe.html?vue=colonnes", "Dans l'exemple du cours : vₙ = uₙ − 16, multiplié par ¼ à chaque pas",
        "نشوفو la méthode على l'exemple ديال le cours: u indice n plus un égale un sur quatre u indice n plus douze. شوف الأعمدة: dix-sept، seize virgule vingt-cinq، كيقربو ل seize. اللي فوق seize: un، zéro virgule vingt-cinq. كل مرة كنضربو فun sur quatre: v indice n égale u indice n moins seize géométrique. عندنا العكس: u indice n تحت neuf، إذن ناخدو اللي ناقص: v indice n égale neuf moins u indice n. وكل مرة كنضربو فdeux sur trois: v indice n plus un égale deux sur trois v indice n. وv zéro égale neuf moins deux، égale sept.",
        [("vₙ₊₁ = (2/3)vₙ", "وكل مرة كنضربو فdeux sur trois"), ("v₀ = 9 − 2 = 7", "وv zéro égale neuf moins deux")],
        [jusqua("شوف الأعمدة", "termes"), jusqua("اللي فوق seize", "ecarts"), jusqua("كل مرة كنضربو فun sur quatre", "fois_quart"),
         montre("وكل مرة كنضربو فdeux sur trois", "centre:0"), montre("وv zéro égale neuf moins deux", "centre:1")]),
    sim("ex_5", "Question 3-2 : revenir à uₙ", "On exprime vₙ, puis on isole uₙ.",
        S + "calculs.html?vue=x4", "Revenir à uₙ à partir de vₙ",
        "فl'exemple ديال le cours: v indice n égale u indice n moins seize، إذن u indice n égale v indice n plus seize، يعني seize plus un sur quatre puissance n. عندنا: v indice n géométrique، إذن v indice n égale v zéro fois q puissance n، يعني sept fois deux sur trois puissance n. وv indice n égale neuf moins u indice n، إذن u indice n égale neuf moins v indice n. u indice n égale neuf moins sept fois deux sur trois puissance n.",
        [("vₙ = 7(2/3)ⁿ", "يعني sept fois deux sur trois puissance n"), ("uₙ = 9 − vₙ = 9 − 7(2/3)ⁿ", "u indice n égale neuf moins sept")],
        [jusqua("فl'exemple ديال le cours", "simple"), montre("يعني sept fois deux sur trois puissance n", "centre:0"),
         montre("u indice n égale neuf moins sept", "centre:1")]),
    sim("ex_6", "Question 3-3 : la limite de qⁿ", "Si −1 < q < 1, lim qⁿ = 0 : la condition s'écrit avant la limite.",
        S + "qn.html?vue=positif", "Les points (n ; qⁿ) pour q = 1/2, 2 et 1",
        "شوف النقط ديال un sur deux puissance n: un، zéro virgule cinq، zéro virgule vingt-cinq. كيطيحو نحو zéro. ومع deux puissance n: un، deux، quatre، كيخرجو من الفوق. ومع un: ديما un. القاعدة: يلا q بين zéro وun، la limite ديال q puissance n égale zéro. عندنا moins un inférieur à deux sur trois، inférieur à un. إذن la limite ديال deux sur trois puissance n égale zéro، وla limite ديال u indice n égale neuf.",
        [("−1 < 2/3 < 1 ⇒ lim (2/3)ⁿ = 0", "عندنا moins un inférieur à deux sur trois"), ("lim uₙ = 9 − 7 × 0 = 9", "وla limite ديال u indice n égale neuf")],
        [jusqua("شوف النقط ديال un sur deux puissance n", "q_demi"), jusqua("ومع deux puissance n", "q_deux"),
         jusqua("ومع un", "q_un"), jusqua("القاعدة", "bilan"), montre("عندنا moins un inférieur à deux sur trois", "centre:0"),
         montre("وla limite ديال u indice n égale neuf", "centre:1")]),
])

FACILE = deck("facile", "Plus facile, pour s'entraîner", [
    qcm("fa_1", "Plus facile : l'hérédité", "نتمرنو: شنو هي الخطوة الأولى فl'hérédité؟",
        "On suppose uₙ < 9. Quelle est la bonne première ligne ?", ["uₙ + 3 < 12", "(2/3)uₙ < 6", "(2/3)uₙ > 6"], 1, [
            (("ما تقلقش. la formule كتضرب الأول فdeux sur trois، ومن بعد كتزيد trois. عاود اختار.", "La formule multiplie d'abord par 2/3. Réessaie."),
             ("الجواب هو deux sur trois u indice n inférieur à six: كنبداو بالضرب.", "Réponse : (2/3)uₙ < 6 : d'abord ×, puis +.")),
            ("برافو! deux sur trois positif، إذن نفس الاتجاه: inférieur à six.", "Juste : 2/3 > 0, le sens reste."),
            (("قريب! deux sur trois positif، إذن الاتجاه ما كيتبدلش. عاود اختار.", "2/3 > 0 : le sens ne change pas. Réessaie."),
             ("الجواب هو inférieur à six: الضرب فpositif كيخلي نفس الاتجاه.", "Réponse : (2/3)uₙ < 6."))],
        "On suppose u indice n inférieur à neuf. Quelle est la bonne première ligne ?"),
    qcm("fa_2", "Plus facile : le signe", "سؤال ساهل على le signe.",
        "uₙ < 9. Quel est le signe de uₙ₊₁ − uₙ = (1/3)(9 − uₙ) ?", ["négatif", "on ne peut pas savoir", "positif"], 2, [
            (("ما تقلقش. u indice n أصغر من neuf، إذن neuf moins u indice n positif. عاود اختار.", "9 − uₙ > 0. Réessaie."),
             ("الجواب هو positif: un sur trois positif، وneuf moins u indice n positif.", "Réponse : positif.")),
            (("قريب! السؤال un كيعطيك u indice n inférieur à neuf: استعملو. عاود اختار.", "Utilise la question 1. Réessaie."),
             ("الجواب هو positif، والsuite croissante.", "Réponse : positif.")),
            ("برافو! positif fois positif: la suite croissante.", "Juste : positif, donc (uₙ) croissante.")],
        "Quel est le signe de u indice n plus un moins u indice n ?"),
    association("fa_3", "Plus facile : le bon couple", "Relie chaque situation à ce qu'on peut conclure.",
        "سؤال ساهل: ربط كل حالة مع الخلاصة ديالها.", "Relie chaque situation à sa conclusion.",
        [("1", "croissante et majorée"), ("2", "décroissante et minorée"), ("3", "croissante et minorée")],
        [("a", "convergente"), ("b", "on ne peut rien conclure")],
        {"1": "a", "2": "a", "3": "b"},
        {"1-a": ("Oui : elle monte sous un plafond.", "برافو: كتطلع تحت سقف."),
         "1-b": ("Si : un plafond arrête une suite qui monte.", "لا، السقف كيوقف suite كتطلع."),
         "2-a": ("Oui : elle descend au-dessus d'un plancher.", "برافو: كتهبط فوق أرضية."),
         "2-b": ("Si : un plancher arrête une suite qui descend.", "لا، الأرضية كتوقف suite كتهبط."),
         "3-a": ("Non : n² est croissante et minorée par 0, et tend vers +∞.", "لا، n carré croissante et minorée، وكتمشي ل plus l'infini."),
         "3-b": ("Oui : un plancher sous une suite qui monte ne la freine pas.", "برافو: أرضية تحت suite كتطلع ما كتوقفهاش.")},
        ("(1 ; a) (2 ; a) (3 ; b) : il faut le bon couple.", "القاعدة: croissante et majorée، ولا décroissante et minorée.")),
    qcm("fa_4", "Plus facile : la suite auxiliaire", "سؤال ساهل على v indice n.",
        "vₙ = 9 − uₙ et u₀ = 2. Que vaut v₀ ?", ["v₀ = 7", "v₀ = 9", "v₀ = −7"], 0, [
            ("برافو! v zéro égale neuf moins deux، égale sept.", "Juste : v₀ = 9 − u₀ = 7."),
            (("ما تقلقش. خاصك تنقص u zéro: neuf moins u zéro. عاود اختار.", "On retranche u₀. Réessaie."),
             ("الجواب هو sept: neuf moins deux.", "Réponse : v₀ = 9 − 2 = 7.")),
            (("قريب! بدلتي الترتيب: v zéro égale neuf moins u zéro، ماشي u zéro moins neuf. عاود اختار.", "C'est 9 − u₀, pas u₀ − 9. Réessaie."),
             ("الجواب هو sept.", "Réponse : v₀ = 7."))],
        "v indice n égale neuf moins u indice n، et u zéro égale deux. Que vaut v zéro ?"),
    vrai_faux("fa_5", "Plus facile : vrai ou faux", "vₙ = 7(2/3)ⁿ et vₙ = 9 − uₙ.",
        "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
            ("uₙ = 2 × (2/3)ⁿ, car u₀ = 2.", False, "(uₙ) n'est pas géométrique : c'est (vₙ) qui l'est."),
            ("uₙ = 9 − vₙ = 9 − 7(2/3)ⁿ.", True, "On isole uₙ dans vₙ = 9 − uₙ."),
            ("u₀ = 9 − 7 × (2/3)⁰ = 2.", True, "(2/3)⁰ = 1 : on retrouve u₀ = 2.")]),
    qcm("fa_6", "Plus facile : lim qⁿ", "سؤال ساهل على la limite ديال q puissance n.",
        "Que vaut lim (2/3)ⁿ ?", ["+∞", "0", "2/3"], 1, [
            (("ما تقلقش. deux sur trois أصغر من un: كل مرة كتضرب فيه، كيصغر. عاود اختار.", "2/3 < 1 : les puissances diminuent. Réessaie."),
             ("الجواب هو zéro: moins un inférieur à deux sur trois، inférieur à un.", "Réponse : 0, car −1 < 2/3 < 1.")),
            ("برافو! moins un inférieur à deux sur trois، inférieur à un: la limite zéro.", "Juste : −1 < 2/3 < 1, donc lim (2/3)ⁿ = 0."),
            (("قريب! deux sur trois puissance n كيتبدل مع n: كيصغر. عاود اختار.", "(2/3)ⁿ change avec n. Réessaie."),
             ("الجواب هو zéro.", "Réponse : 0."))],
        "Que vaut la limite de deux sur trois، puissance n ?"),
])

ENONCE = {
    "intro": "On considère la suite numérique (uₙ) définie par : u₀ = 2 et uₙ₊₁ = (2/3)uₙ + 3 pour tout entier naturel n.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا la suite u indice n: u zéro égale deux، وu indice n plus un égale deux sur trois u indice n، plus trois، pour tout n.",
    "figures": [nuage(2, Fr(2, 3), 3, 9, "uₙ")],
    "donnees": ["u₀ = 2", "uₙ₊₁ = (2/3)uₙ + 3 pour tout n ∈ ℕ", "vₙ = 9 − uₙ (question 3)"],
    "questions": QUESTIONS,
}

SIMILAIRE = {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
        "intro": "On considère la suite numérique (uₙ) définie par : u₀ = 1 et uₙ₊₁ = (1/2)uₙ + 3 pour tout entier naturel n. On pose vₙ = 6 − uₙ.",
        "intro_dit": "نفس التمرين، بأرقام أخرى: u zéro égale un، وu indice n plus un égale un sur deux u indice n، plus trois. وv indice n égale six moins u indice n.",
        "figures": [nuage(1, Fr(1, 2), 3, 6, "uₙ")],
        "donnees": ["u₀ = 1", "uₙ₊₁ = (1/2)uₙ + 3", "vₙ = 6 − uₙ"],
        "questions": [
            {"id": "1", "texte": "Montrer par récurrence que uₙ < 6 pour tout entier naturel n.",
             "reponse": phrase("Initialisation : u₀ = 1 < 6. Hérédité : uₙ < 6 ⇒ (1/2)uₙ < 3 ⇒ (1/2)uₙ + 3 < 6 : uₙ₊₁ < 6. Conclusion : uₙ < 6 pour tout n."),
             "clavier": {"aides": ["Initialisation", "(1/2)uₙ < 3", "Conclusion"], "pieges": ["supposons que pour tout n"]},
             "correction": correction([("1 : u₀ = 1 < 6", "u zéro égale un"), ("uₙ < 6 ⇒ (1/2)uₙ + 3 < 6 : uₙ₊₁ < 6", "supposons que"),
                                       ("d'après le principe de récurrence, uₙ < 6 pour tout n", "d'après le principe de récurrence")],
                                      "initialisation: u zéro égale un، inférieur à six. hérédité: supposons que u indice n inférieur à six. un sur deux u indice n، inférieur à trois، plus trois: inférieur à six. d'après le principe de récurrence، u indice n inférieur à six pour tout n.")},
            {"id": "2-1", "texte": "Vérifier que uₙ₊₁ − uₙ = (1/2)(6 − uₙ), puis montrer que (uₙ) est croissante.",
             "reponse": phrase("uₙ₊₁ − uₙ = −(1/2)uₙ + 3 = (1/2)(6 − uₙ) > 0 car uₙ < 6 : (uₙ) est croissante."),
             "clavier": {"aides": ["(1/2)(6 − uₙ)", "6 − uₙ > 0"], "pieges": ["u₁ > u₀"]},
             "correction": correction([("2-1 : uₙ₊₁ − uₙ = −(1/2)uₙ + 3 = (1/2)(6 − uₙ)", "un sur deux، fois، six moins u indice n"),
                                       ("uₙ < 6 donc uₙ₊₁ − uₙ > 0 : (uₙ) croissante", "croissante")],
                                      "la différence égale un sur deux، fois، six moins u indice n. u indice n inférieur à six، إذن positive pour tout n: la suite croissante.")},
            {"id": "2-2", "texte": "En déduire que la suite (uₙ) est convergente.",
             "reponse": phrase("(uₙ) est croissante et majorée par 6, donc convergente."),
             "clavier": {"aides": ["croissante", "majorée par 6"], "pieges": ["minorée"]},
             "correction": correction([("2-2 : croissante et majorée par 6, donc convergente", "croissante et majorée")],
                                      "la suite croissante et majorée par six، donc convergente.")},
            {"id": "3-1", "texte": "Montrer que (vₙ) est géométrique de raison 1/2, et calculer v₀.",
             "reponse": phrase("vₙ₊₁ = 6 − uₙ₊₁ = 3 − (1/2)uₙ = (1/2)(6 − uₙ) = (1/2)vₙ ; v₀ = 6 − 1 = 5."),
             "clavier": {"aides": ["vₙ₊₁ = 6 − uₙ₊₁", "(1/2)vₙ", "v₀ ="], "pieges": ["v₀ = 6"]},
             "correction": correction([("3-1 : vₙ₊₁ = 6 − uₙ₊₁ = 3 − (1/2)uₙ = (1/2)vₙ", "égale un sur deux v indice n"), ("v₀ = 6 − 1 = 5", "v zéro égale cinq")],
                                      "v indice n plus un égale six moins u indice n plus un، يعني trois moins un sur deux u indice n، égale un sur deux v indice n. géométrique، la raison un sur deux. v zéro égale cinq.")},
            {"id": "3-2", "texte": "Exprimer vₙ, puis uₙ, en fonction de n.",
             "reponse": phrase("vₙ = 5(1/2)ⁿ et uₙ = 6 − vₙ = 6 − 5(1/2)ⁿ."),
             "clavier": {"aides": ["vₙ = v₀ × qⁿ", "uₙ = 6 − vₙ"], "pieges": ["uₙ = (1/2)ⁿ"]},
             "correction": correction([("3-2 : vₙ = 5(1/2)ⁿ ; uₙ = 6 − 5(1/2)ⁿ", "u indice n égale six moins cinq")],
                                      "v indice n égale cinq fois un sur deux puissance n، وu indice n égale six moins cinq fois un sur deux puissance n.")},
            {"id": "3-3", "texte": "Calculer la limite de la suite (uₙ).",
             "reponse": valeur("lim uₙ", 6, "−1 < 1/2 < 1 donc lim (1/2)ⁿ = 0 ; lim uₙ = 6 − 0 = 6"),
             "clavier": {"aides": ["−1 < 1/2 < 1", "lim (1/2)ⁿ = 0"], "pieges": ["lim uₙ = +∞"]},
             "correction": correction([("3-3 : −1 < 1/2 < 1 donc lim (1/2)ⁿ = 0 ; lim uₙ = 6", "la limite égale six")],
                                      "moins un inférieur à un sur deux، inférieur à un، إذن un sur deux puissance n كتمشي ل zéro. la limite égale six.")},
        ]}}

EX = {"id": ID, "type": "exercice", "version": 1, "status": "published", "matiere": "mathematiques",
      "chapitre": "suites_definition", "cours": "math_ch3_suites_numeriques",
      "titre": "Une suite uₙ₊₁ = a·uₙ + b : récurrence, monotonie, suite auxiliaire et limite", "niveau": "moyen", "duree_min": 30,
      "origine": ORIGINE,
      "competences": ["Rédiger une récurrence par opérations sur l'hypothèse", "Étudier la monotonie par uₙ₊₁ − uₙ",
                      "Conclure à la convergence (monotone et bornée)", "Montrer qu'une suite auxiliaire est géométrique",
                      "Exprimer uₙ en fonction de n et calculer sa limite"],
      "enonce": ENONCE, "explication": EXPLICATION, "facile": FACILE, "similaire": SIMILAIRE}

if __name__ == "__main__":
    ecrire(EX)
