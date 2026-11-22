# Exercice de maths, ch. 3 (suites numériques), niveau moyen (niveau du national) : suite homographique.
# Sources comparées (lecture seule, rien de recopié) :
#  - exploration suites_definition.json : redaction_nationale recurrence_fraction_difference, monotonie_difference,
#    suite auxiliaire arithmétique (cas_types suite_auxiliaire_arithmetique : 2020 R, 2021 R, 2023 R), isoler_un_fraction ;
#    pieges « opérations sur l'hypothèse quand uₙ est en haut et en bas », « signe d'une fraction sans le dénominateur »,
#    « recalcule uₙ₊₁ − a déjà obtenu », « divise sans vérifier que c'est non nul » ;
#  - vidéos : Driss DOTCOM uFRQ1Q4-X3E (geste barré : uₙ deux fois → signe de uₙ₊₁ − a), Mouad Tahiri b7iH3KUEoZc
#    (ne pas recalculer), Aderdour 5d4DjGTpbu4 (national 2020, rédaction au tableau), Prof fati NNxZYDMA_v4 (deux nationaux) ;
#  - nationaux : 2016 N, 2020 R, 2021 R, 2023 R, 2024 N, 2025 R (homographiques : vérifier, récurrence, monotonie,
#    suite auxiliaire, limite) — ici une autre suite : uₙ₊₁ = (5uₙ − 4)/(uₙ + 1), point double 2 ;
#  - séries en ligne (résultats de recherche, pages non ouvertes : réseau fermé) : talamidi 2 bac PC série corrigée 3,
#    moutamadris 2 bac PC/SVT série 1, fayssalmaths séries corrigées 2 bac SE, pdfmath exercices nationaux corrigés 2 bac PC,
#    talamidi examen simili 4 (2 SPC/SVT).
# Données propres à Moalim : u₀ = 3 ; vₙ = 1/(uₙ − 2), arithmétique de raison 1/3 ; uₙ = 2 + 3/(n + 3).
import sys
from fractions import Fraction as Fr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa: E402,F401,F403

ID = "math_ex_ch3_suites_4"
S = "/media/simulations/maths/suites-tableau/"


def nuage(termes, l, ymax):
    el = [{"f": "repere", "y": l, "t": f"y = {l}", "couleur": "vert"}]
    for k, v in enumerate(termes):
        p = {"f": "point", "at": [k, round(float(v), 3)], "couleur": "cyan"}
        if k < 3:
            p.update({"t": "u" + "₀₁₂"[k], "pos": "ne"})
        el.append(p)
    return {"type": "courbe", "titre": "Les premiers termes : les points (n ; uₙ)",
            "axes": {"x": {"min": 0, "max": 6, "nom": "n", "graduations": [1, 2, 3, 4, 5]},
                     "y": {"min": 0, "max": ymax, "nom": "uₙ", "graduations": list(range(0, ymax + 1))}},
            "legende": f"Les points descendent et restent au-dessus de la droite y = {l}.", "elements": el}


def termes(u0, f):
    u = [Fr(u0)]
    for _ in range(5):
        u.append(f(u[-1]))
    return u


QUESTIONS = [
    {"id": "1", "texte": "Vérifier que uₙ₊₁ − 2 = 3(uₙ − 2)/(uₙ + 1) pour tout n, puis montrer par récurrence que uₙ > 2 pour tout entier naturel n.",
     "texte_dit": "السؤال un: تحقق بلي u indice n plus un moins deux، égale trois fois، u indice n moins deux، sur u indice n plus un. ومن بعد بين par récurrence بلي u indice n supérieur à deux.",
     "reponse": phrase("uₙ₊₁ − 2 = (5uₙ − 4 − 2uₙ − 2)/(uₙ + 1) = (3uₙ − 6)/(uₙ + 1) = 3(uₙ − 2)/(uₙ + 1). Initialisation : u₀ = 3 > 2. Hérédité : si uₙ > 2, alors uₙ − 2 > 0 et uₙ + 1 > 0, donc uₙ₊₁ − 2 > 0, c'est-à-dire uₙ₊₁ > 2. Conclusion : uₙ > 2 pour tout n."),
     "clavier": {"aides": ["(5uₙ − 4 − 2(uₙ + 1))/(uₙ + 1)", "3(uₙ − 2)/(uₙ + 1)", "uₙ − 2 > 0", "uₙ + 1 > 0", "uₙ₊₁ − 2 > 0"],
                 "pieges": ["uₙ > 2 ⇒ 5uₙ − 4 > 6 et uₙ + 1 > 3 ⇒ uₙ₊₁ > 2", "supposons que pour tout n"]},
     "aides": [aide("Pour la vérification : même dénominateur, 2 = 2(uₙ + 1)/(uₙ + 1). Pour l'hérédité : uₙ est en haut ET en bas, on étudie le signe de uₙ₊₁ − 2.",
                    "باش تتحقق: نفس المقام، deux égale deux fois، u indice n plus un، sur u indice n plus un. وفl'hérédité: u indice n كاين الفوق والتحت، إذن كنقراو le signe ديال u indice n plus un moins deux."),
               aide("Avec uₙ > 2 : quel est le signe de uₙ − 2 ? de uₙ + 1 ? Un signe sous chaque facteur, puis le signe du quotient.",
                    "مع u indice n supérieur à deux: شنو le signe ديال u indice n moins deux؟ وديال u indice n plus un؟ signe تحت كل facteur، ومن بعد le signe ديال le quotient.")],
     "correction": correction([
         ("1 : uₙ₊₁ − 2 = (5uₙ − 4 − 2uₙ − 2)/(uₙ + 1) = 3(uₙ − 2)/(uₙ + 1)", "même dénominateur"),
         ("Initialisation : u₀ = 3 > 2", "u zéro égale trois"),
         ("Hérédité : supposons uₙ > 2 : uₙ − 2 > 0 et uₙ + 1 > 0, donc uₙ₊₁ − 2 > 0, soit uₙ₊₁ > 2", "supposons que u indice n supérieur à deux"),
         ("Conclusion : d'après le principe de récurrence, uₙ > 2 pour tout n ∈ ℕ", "d'après le principe de récurrence")],
         "السؤال un. même dénominateur: cinq u indice n moins quatre، moins deux u indice n moins deux، sur u indice n plus un. يعني trois u indice n moins six، égale trois fois، u indice n moins deux. initialisation: u zéro égale trois، supérieur à deux. hérédité: supposons que u indice n supérieur à deux. u indice n moins deux positif، وu indice n plus un positif، إذن u indice n plus un moins deux positif. conclusion: d'après le principe de récurrence، u indice n supérieur à deux pour tout n."),
     "explication": "ex_1", "facile": "fa_1"},
    {"id": "2-1", "texte": "Montrer que uₙ₊₁ − uₙ = −(uₙ − 2)²/(uₙ + 1) pour tout n, puis en déduire que (uₙ) est décroissante.",
     "texte_dit": "السؤال deux un: بين بلي u indice n plus un moins u indice n، égale moins، u indice n moins deux au carré، sur u indice n plus un. ومن بعد استنتج بلي la suite décroissante.",
     "reponse": phrase("uₙ₊₁ − uₙ = (5uₙ − 4 − uₙ² − uₙ)/(uₙ + 1) = −(uₙ² − 4uₙ + 4)/(uₙ + 1) = −(uₙ − 2)²/(uₙ + 1). Or (uₙ − 2)² ≥ 0 et uₙ + 1 > 0, donc uₙ₊₁ − uₙ ≤ 0 pour tout n : (uₙ) est décroissante."),
     "clavier": {"aides": ["uₙ(uₙ + 1)", "−uₙ² + 4uₙ − 4", "(uₙ − 2)²", "(uₙ − 2)² ≥ 0", "uₙ₊₁ − uₙ ≤ 0"],
                 "pieges": ["(uₙ − 2)² > 0 toujours", "u₁ < u₀ donc décroissante"]},
     "aides": [aide("Même dénominateur : uₙ = uₙ(uₙ + 1)/(uₙ + 1). Développe le numérateur et reconnais une identité remarquable.",
                    "نفس المقام: u indice n égale u indice n fois، u indice n plus un، sur u indice n plus un. نشر le numérateur، وشوف واش كاينة identité remarquable."),
               aide("x² − 4x + 4 = (x − 2)². Un carré est positif ou nul ; uₙ + 1 > 0 car uₙ > 2.",
                    "x carré moins quatre x plus quatre، égale، x moins deux، au carré. le carré ديما positif ولا zéro. وu indice n plus un positif حيت u indice n supérieur à deux.")],
     "correction": correction([
         ("2-1 : uₙ₊₁ − uₙ = (5uₙ − 4 − uₙ(uₙ + 1))/(uₙ + 1) = (−uₙ² + 4uₙ − 4)/(uₙ + 1)", "moins u indice n au carré"),
         ("= −(uₙ − 2)²/(uₙ + 1)", "identité remarquable"),
         ("(uₙ − 2)² ≥ 0 et uₙ + 1 > 0 (car uₙ > 2) : uₙ₊₁ − uₙ ≤ 0 pour tout n", "inférieur ou égal à zéro"),
         ("donc (uₙ) est décroissante", "décroissante")],
         "السؤال deux un. نفس المقام: cinq u indice n moins quatre، moins u indice n fois، u indice n plus un. كتعطي moins u indice n au carré، plus quatre u indice n، moins quatre. هادي identité remarquable: moins، u indice n moins deux، au carré. le carré positif ولا zéro، وu indice n plus un positif. إذن la différence inférieur ou égal à zéro pour tout n: la suite décroissante."),
     "explication": "ex_2", "facile": "fa_2"},
    {"id": "2-2", "texte": "En déduire que la suite (uₙ) est convergente.",
     "texte_dit": "السؤال deux deux: استنتج بلي la suite convergente.",
     "reponse": phrase("(uₙ) est décroissante (2-1) et minorée par 2 (1), donc elle est convergente."),
     "clavier": {"aides": ["décroissante", "minorée par 2", "donc convergente"], "pieges": ["majorée", "converge vers 2 car minorée par 2"]},
     "aides": [aide("Une suite qui descend converge si elle a un plancher. Lequel as-tu montré ?",
                    "suite كتهبط، كتكون convergente يلا عندها أرضية. شنو هي الأرضية اللي بينتي؟"),
               aide("Cite les deux résultats avec leurs numéros : décroissante (2-1), minorée par 2 (1).",
                    "عاود جوج نتائج بالأرقام ديالهم: décroissante، من deux un، وminorée par deux، من un.")],
     "correction": correction([
         ("2-2 : (uₙ) est décroissante (2-1) et minorée par 2 (1)", "décroissante et minorée par deux"),
         ("donc (uₙ) est convergente", "donc convergente")],
         "السؤال deux deux. la suite décroissante et minorée par deux، donc convergente. وminorée par deux ما كتقولش بعد بلي la limite هي deux."),
     "explication": "ex_3", "facile": "fa_3"},
    {"id": "3-1", "texte": "On pose vₙ = 1/(uₙ − 2) pour tout n. Montrer que (vₙ) est une suite arithmétique de raison 1/3, et calculer v₀.",
     "texte_dit": "السؤال trois un: ناخدو v indice n égale un sur، u indice n moins deux. بين بلي v indice n suite arithmétique، la raison ديالها un sur trois، وحسب v zéro.",
     "reponse": phrase("vₙ₊₁ = 1/(uₙ₊₁ − 2) = (uₙ + 1)/(3(uₙ − 2)) = (uₙ − 2 + 3)/(3(uₙ − 2)) = 1/3 + 1/(uₙ − 2) = 1/3 + vₙ ; donc vₙ₊₁ − vₙ = 1/3 : (vₙ) est arithmétique de raison 1/3 ; v₀ = 1/(3 − 2) = 1."),
     "clavier": {"aides": ["vₙ₊₁ = 1/(uₙ₊₁ − 2)", "(uₙ + 1)/(3(uₙ − 2))", "uₙ + 1 = (uₙ − 2) + 3", "vₙ₊₁ − vₙ = 1/3", "v₀ ="],
                 "pieges": ["vₙ₊₁ = (1/3)vₙ", "v₀ = 1/3"]},
     "aides": [aide("Utilise la question 1 : uₙ₊₁ − 2 = 3(uₙ − 2)/(uₙ + 1). Son inverse est vₙ₊₁ ; ne recalcule pas.",
                    "استعمل السؤال un: u indice n plus un moins deux، égale trois fois، u indice n moins deux، sur u indice n plus un. المقلوب ديالو هو v indice n plus un. ما تعاودش الحساب."),
               aide("Écris uₙ + 1 = (uₙ − 2) + 3 et coupe la fraction en deux. Une suite arithmétique : vₙ₊₁ − vₙ est constant.",
                    "كتب u indice n plus un، égale، u indice n moins deux، plus trois، وقسم la fraction على جوج. suite arithmétique: v indice n plus un moins v indice n، constant.")],
     "correction": correction([
         ("3-1 : vₙ₊₁ = 1/(uₙ₊₁ − 2) = (uₙ + 1)/(3(uₙ − 2))", "v indice n plus un égale"),
         ("= ((uₙ − 2) + 3)/(3(uₙ − 2)) = 1/3 + 1/(uₙ − 2) = 1/3 + vₙ", "un sur trois plus v indice n"),
         ("vₙ₊₁ − vₙ = 1/3 : (vₙ) est arithmétique de raison 1/3 ; v₀ = 1/(3 − 2) = 1", "v zéro égale un")],
         "السؤال trois un. v indice n plus un égale un sur، u indice n plus un moins deux. من السؤال un، كتعطي، u indice n plus un، sur trois fois، u indice n moins deux. نكتبو u indice n plus un، égale، u indice n moins deux، plus trois. كنلقاو un sur trois plus v indice n. إذن la différence égale un sur trois: arithmétique، la raison un sur trois. وv zéro égale un sur، trois moins deux، v zéro égale un."),
     "explication": "ex_4", "facile": "fa_4"},
    {"id": "3-2", "texte": "Exprimer vₙ en fonction de n, puis montrer que uₙ = 2 + 3/(n + 3) pour tout n.",
     "texte_dit": "السؤال trois deux: عبر على v indice n en fonction de n، ومن بعد بين بلي u indice n égale deux plus trois sur، n plus trois.",
     "reponse": phrase("vₙ = v₀ + n r = 1 + n/3 = (n + 3)/3 ; uₙ − 2 = 1/vₙ = 3/(n + 3), donc uₙ = 2 + 3/(n + 3)."),
     "clavier": {"aides": ["vₙ = v₀ + n r", "(n + 3)/3", "uₙ − 2 = 1/vₙ", "uₙ = 2 + 1/vₙ"], "pieges": ["vₙ = (1/3)ⁿ", "uₙ = 1/vₙ − 2"]},
     "aides": [aide("Suite arithmétique : vₙ = v₀ + n r, avec v₀ = 1 et r = 1/3.",
                    "suite arithmétique: v indice n égale v zéro plus n fois r، مع v zéro égale un، وr égale un sur trois."),
               aide("Isole uₙ : vₙ = 1/(uₙ − 2) donne uₙ − 2 = 1/vₙ.",
                    "عزل u indice n: v indice n égale un sur، u indice n moins deux، كتعطي u indice n moins deux égale un sur v indice n.")],
     "correction": correction([
         ("3-2 : vₙ = v₀ + n r = 1 + n/3 = (n + 3)/3", "v indice n égale un plus n sur trois"),
         ("uₙ − 2 = 1/vₙ = 3/(n + 3), donc uₙ = 2 + 3/(n + 3)", "u indice n égale deux plus trois sur")],
         "السؤال trois deux. v indice n égale un plus n sur trois، يعني، n plus trois، sur trois. وu indice n moins deux égale un sur v indice n، égale trois sur، n plus trois. إذن u indice n égale deux plus trois sur، n plus trois."),
     "explication": "ex_5", "facile": "fa_5"},
    {"id": "3-3", "texte": "Calculer la limite de la suite (uₙ).",
     "texte_dit": "السؤال trois trois: حسب la limite ديال la suite u indice n.",
     "reponse": valeur("lim uₙ", 2, "lim (n + 3) = +∞, donc lim 3/(n + 3) = 0 ; lim uₙ = 2 + 0 = 2"),
     "clavier": {"aides": ["lim (n + 3) = +∞", "lim 3/(n + 3) = 0", "lim uₙ ="], "pieges": ["lim uₙ = 3", "lim uₙ = 2 + 1"]},
     "aides": [aide("Quand n devient très grand, que devient 3/(n + 3) ?",
                    "ملي n كيكبر بزاف، شنو كيولي trois sur، n plus trois؟"),
               aide("Un nombre fixe divisé par un nombre qui tend vers +∞ tend vers 0.",
                    "عدد ثابت، sur عدد كيمشي ل plus l'infini، كيمشي ل zéro.")],
     "correction": correction([
         ("3-3 : lim (n + 3) = +∞ donc lim 3/(n + 3) = 0", "trois sur، n plus trois، كتمشي ل zéro"),
         ("lim uₙ = 2 + 0 = 2", "la limite égale deux")],
         "السؤال trois trois. n plus trois كتمشي ل plus l'infini، إذن trois sur، n plus trois، كتمشي ل zéro. إذن la limite égale deux plus zéro: la limite égale deux."),
     "explication": "ex_6", "facile": "fa_6"},
]

EXPLICATION = deck("explication", "Explication animée", [
    sim("ex_1", "Question 1 : uₙ en haut et en bas", "Les opérations ne marchent plus : on étudie le signe de uₙ₊₁ − 2.",
        S + "calculs.html?vue=r4", "La même méthode sur l'exemple du cours",
        "نشوفو la méthode على l'exemple ديال le cours: u indice n كاين الفوق والتحت. يلا درنا العمليات، كنلقاو الفوق أكبر من sept والتحت أكبر من sept، ولكن le quotient؟ ما كنعرفوش. الحل: le signe ديال u indice n plus un moins un. نفس المقام، ومن بعد signe تحت كل facteur. عندنا: u indice n plus un moins deux، égale trois fois، u indice n moins deux، sur u indice n plus un. u indice n moins deux positif، وu indice n plus un positif، إذن u indice n plus un supérieur à deux.",
        [("uₙ₊₁ − 2 = 3(uₙ − 2)/(uₙ + 1)", "عندنا"), ("uₙ − 2 > 0 et uₙ + 1 > 0 ⇒ uₙ₊₁ > 2", "إذن u indice n plus un supérieur à deux")],
        [jusqua("نشوفو la méthode", "enonce"), jusqua("يلا درنا العمليات", "essai"), jusqua("الحل", "difference"),
         jusqua("نفس المقام", "calcul"), jusqua("ومن بعد signe تحت كل facteur", "signes"), montre("عندنا", "centre:0"),
         jusqua("إذن u indice n plus un supérieur à deux", "conclusion"), montre("إذن u indice n plus un supérieur à deux", "centre:1")]),
    sim("ex_2", "Question 2-1 : un signe sous chaque facteur", "Le carré est positif ou nul, le dénominateur positif : la différence est négative ou nulle.",
        S + "calculs.html?vue=m3", "L'égalité donnée, puis le signe de chaque facteur",
        "فl'exemple ديال le cours، l'égalité كانت معطية، وكنعرفو مكان u indice n من la récurrence. ومن بعد كنحطو signe تحت كل facteur. عندنا: moins، u indice n moins deux au carré، sur u indice n plus un. le carré positif ولا zéro. u indice n plus un positif، حيت u indice n supérieur à deux. ومع moins اللي القدام: la différence inférieur ou égal à zéro. إذن la suite décroissante.",
        [("(uₙ − 2)² ≥ 0", "le carré positif ولا zéro"), ("uₙ + 1 > 0", "u indice n plus un positif"),
         ("uₙ₊₁ − uₙ ≤ 0 : décroissante", "إذن la suite décroissante")],
        [jusqua("l'égalité كانت معطية", "donne"), jusqua("وكنعرفو مكان u indice n", "sait"), jusqua("ومن بعد كنحطو signe", "signes"),
         montre("le carré positif ولا zéro", "centre:0"), montre("u indice n plus un positif", "centre:1"), montre("إذن la suite décroissante", "centre:2")]),
    sim("ex_3", "Question 2-2 : un plancher sous une suite qui descend", "Décroissante et minorée : convergente.",
        S + "nuage.html?vue=plancher", "Les points descendent au-dessus d'un plancher",
        "شوف هاد النقط ديال l'exemple: كيهبطو، dix-sept، seize virgule vingt-cinq، وكيقربو ل seize. هاد الخط الأخضر هو الأرضية: حتى نقطة ما كتهبط تحتو، la suite minorée. وهادا الخط البرتقالي هو السقف. عندنا نفس الحالة: la suite décroissante، وminorée par deux. suite كتهبط فوق أرضية، كتوقف: convergente.",
        [("décroissante et minorée ⇒ convergente", "كتوقف: convergente")],
        [jusqua("شوف هاد النقط", "points"), jusqua("هاد الخط الأخضر", "plancher"), jusqua("وهادا الخط البرتقالي", "plafond"),
         montre("كتوقف: convergente", "centre:0")]),
    sim("ex_4", "Question 3-1 : arithmétique ou géométrique ?", "Arithmétique : vₙ₊₁ − vₙ constant ; géométrique : vₙ₊₁ = q × vₙ.",
        S + "calculs.html?vue=x5", "Les deux définitions, puis un exemple",
        "جوج أنواع: suite arithmétique، ملي v indice n plus un moins v indice n ثابت. suite géométrique، ملي v indice n plus un égale q fois v indice n. فl'exemple ديال le cours، la différence كتعطي un sur deux: arithmétique. عندنا: v indice n plus un égale، u indice n plus un، sur trois fois، u indice n moins deux. نكتبو u indice n plus un، u indice n moins deux plus trois، ونقسمو: un sur trois plus v indice n. la différence égale un sur trois: arithmétique.",
        [("vₙ₊₁ = 1/3 + vₙ", "ونقسمو"), ("vₙ₊₁ − vₙ = 1/3 : arithmétique", "la différence égale un sur trois")],
        [jusqua("suite arithmétique", "arith"), jusqua("suite géométrique", "geo"), jusqua("فl'exemple ديال le cours", "calcul"),
         jusqua("arithmétique. عندنا", "formule"), montre("ونقسمو", "centre:0"), montre("la différence égale un sur trois", "centre:1")]),
    sim("ex_5", "Question 3-2 : revenir à uₙ", "vₙ = v₀ + n r, puis on isole uₙ.",
        S + "calculs.html?vue=x4", "Isoler uₙ à partir de vₙ",
        "فl'exemple ديال le cours، v indice n égale u indice n moins seize، إذن u indice n égale v indice n plus seize. ومن بعد مثال فيه fraction: كنضربو en croix، كنجمعو، وكنعزلو u indice n. عندنا أسهل: v indice n égale un plus n sur trois. وu indice n moins deux égale un sur v indice n، يعني trois sur، n plus trois. إذن u indice n égale deux plus trois sur، n plus trois.",
        [("vₙ = 1 + n/3 = (n + 3)/3", "عندنا أسهل"), ("uₙ = 2 + 1/vₙ = 2 + 3/(n + 3)", "إذن u indice n égale deux plus trois sur")],
        [jusqua("فl'exemple ديال le cours", "simple"), jusqua("ومن بعد مثال فيه fraction", "fraction"),
         jusqua("وكنعزلو u indice n", "isoler"), montre("عندنا أسهل", "centre:0"), montre("إذن u indice n égale deux plus trois sur", "centre:1")]),
    sim("ex_6", "Question 3-3 : la limite d'une fraction en n", "Le dénominateur part vers +∞ : la fraction tend vers 0.",
        S + "nuage.html?vue=fraction", "Les points de (n + 1)/(n + 3) se serrent sous y = 1",
        "شوف النقط ديال l'exemple: n plus un، sur n plus trois. كيطلعو وكيقربو للخط y égale un. عندنا: u indice n égale deux plus trois sur، n plus trois. ملي n كيكبر، n plus trois كتمشي ل plus l'infini، وtrois sur، n plus trois، كتمشي ل zéro. إذن la limite égale deux.",
        [("lim 3/(n + 3) = 0", "كتمشي ل zéro"), ("lim uₙ = 2", "إذن la limite égale deux")],
        [jusqua("شوف النقط", "points"), jusqua("وكيقربو للخط", "asymptote"), jusqua("عندنا", "limite"),
         montre("كتمشي ل zéro", "centre:0"), montre("إذن la limite égale deux", "centre:1")]),
])

FACILE = deck("facile", "Plus facile, pour s'entraîner", [
    qcm("fa_1", "Plus facile : quelle méthode ?", "نتمرنو: شنو هي الطريقة؟",
        "uₙ₊₁ = (5uₙ − 4)/(uₙ + 1) : uₙ apparaît deux fois. Pour montrer uₙ₊₁ > 2, on étudie…",
        ["le signe de uₙ₊₁ − 2", "5uₙ − 4 > 6 puis on divise", "le signe de uₙ₊₁ − uₙ"], 0, [
            ("برافو! u indice n الفوق والتحت: كنقراو le signe ديال u indice n plus un moins deux.", "Juste : uₙ deux fois → signe de uₙ₊₁ − 2."),
            (("ما تقلقش. ملي u indice n الفوق والتحت، العمليات ما كتعطيش le quotient. عاود اختار.", "Avec uₙ en haut et en bas, les opérations ne concluent pas. Réessaie."),
             ("الجواب هو le signe ديال u indice n plus un moins deux.", "Réponse : signe de uₙ₊₁ − 2.")),
            (("قريب! u indice n plus un moins u indice n هي ديال la monotonie، ماشي ديال المقارنة مع deux. عاود اختار.", "uₙ₊₁ − uₙ sert à la monotonie. Réessaie."),
             ("الجواب هو le signe ديال u indice n plus un moins deux.", "Réponse : signe de uₙ₊₁ − 2."))],
        "u indice n apparaît deux fois. Pour montrer u indice n plus un supérieur à deux، on étudie quoi ?"),
    vrai_faux("fa_2", "Plus facile : vrai ou faux", "uₙ₊₁ − uₙ = −(uₙ − 2)²/(uₙ + 1) et uₙ > 2.",
        "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
            ("(uₙ − 2)² ≥ 0 pour tout n.", True, "Un carré est toujours positif ou nul."),
            ("uₙ + 1 > 0, car uₙ > 2.", True, "uₙ > 2 donne uₙ + 1 > 3 > 0."),
            ("Donc uₙ₊₁ − uₙ ≥ 0 et la suite est croissante.", False, "Il y a un signe « − » devant : uₙ₊₁ − uₙ ≤ 0, la suite est décroissante.")]),
    association("fa_3", "Plus facile : monotone et bornée", "Relie chaque situation à ce qu'on peut conclure.",
        "سؤال ساهل: ربط كل حالة مع الخلاصة ديالها.", "Relie chaque situation à sa conclusion.",
        [("1", "décroissante et minorée par 2"), ("2", "décroissante et majorée par 3"), ("3", "croissante et majorée par 5")],
        [("a", "convergente"), ("b", "on ne peut rien conclure")],
        {"1": "a", "2": "b", "3": "a"},
        {"1-a": ("Oui : elle descend au-dessus d'un plancher.", "برافو: كتهبط فوق أرضية."),
         "1-b": ("Si : un plancher arrête une suite qui descend.", "لا، الأرضية كتوقف suite كتهبط."),
         "2-a": ("Non : un plafond au-dessus d'une suite qui descend ne la freine pas.", "لا، سقف فوق suite كتهبط ما كيوقفهاش."),
         "2-b": ("Oui : décroissante et majorée, c'est le mauvais couple.", "برافو: décroissante et majorée، هادا الكوبل الغالط."),
         "3-a": ("Oui : elle monte sous un plafond.", "برافو: كتطلع تحت سقف."),
         "3-b": ("Si : un plafond arrête une suite qui monte.", "لا، السقف كيوقف suite كتطلع.")},
        ("(1 ; a) (2 ; b) (3 ; a) : décroissante + minorée, ou croissante + majorée.", "القاعدة: décroissante et minorée، ولا croissante et majorée.")),
    qcm("fa_4", "Plus facile : la raison", "سؤال ساهل على la suite arithmétique.",
        "vₙ₊₁ = vₙ + 1/3 pour tout n. Alors (vₙ) est…", ["géométrique de raison 1/3", "arithmétique de raison 1/3", "arithmétique de raison 3"], 1, [
            (("ما تقلقش. كنزيدو un sur trois، ما كنضربوش. عاود اختار.", "On ajoute 1/3, on ne multiplie pas. Réessaie."),
             ("الجواب هو arithmétique، la raison un sur trois.", "Réponse : arithmétique de raison 1/3.")),
            ("برافو! كل مرة كنزيدو un sur trois: arithmétique، la raison un sur trois.", "Juste : vₙ₊₁ − vₙ = 1/3."),
            (("قريب! اللي كنزيدو هو un sur trois، ماشي trois. عاود اختار.", "On ajoute 1/3, pas 3. Réessaie."),
             ("الجواب هو la raison un sur trois.", "Réponse : raison 1/3."))],
        "v indice n plus un égale v indice n plus un sur trois. Alors v indice n est quoi ?"),
    qcm("fa_5", "Plus facile : isoler uₙ", "سؤال ساهل: عزل u indice n.",
        "vₙ = 1/(uₙ − 2). Alors uₙ = …", ["1/vₙ − 2", "2 + 1/vₙ", "2vₙ + 1"], 1, [
            (("ما تقلقش. u indice n moins deux égale un sur v indice n، ومن بعد كنزيدو deux، ماشي كننقصو. عاود اختار.", "uₙ − 2 = 1/vₙ, puis on ajoute 2. Réessaie."),
             ("الجواب هو deux plus un sur v indice n.", "Réponse : uₙ = 2 + 1/vₙ.")),
            ("برافو! u indice n moins deux égale un sur v indice n، إذن u indice n égale deux plus un sur v indice n.", "Juste : uₙ − 2 = 1/vₙ."),
            (("قريب! خاصك تقلب: u indice n moins deux هو المقلوب ديال v indice n. عاود اختار.", "uₙ − 2 est l'inverse de vₙ. Réessaie."),
             ("الجواب هو deux plus un sur v indice n.", "Réponse : uₙ = 2 + 1/vₙ."))],
        "v indice n égale un sur، u indice n moins deux. Alors u indice n égale quoi ?"),
    qcm("fa_6", "Plus facile : la limite", "سؤال ساهل على la limite.",
        "Que vaut lim 3/(n + 3) ?", ["0", "1", "+∞"], 0, [
            ("برافو! trois sur عدد كيكبر بلا حد، كيمشي ل zéro.", "Juste : le dénominateur tend vers +∞."),
            (("ما تقلقش. n plus trois كيكبر بزاف، إذن la fraction كتصغر. عاود اختار.", "Le dénominateur grandit : la fraction diminue. Réessaie."),
             ("الجواب هو zéro.", "Réponse : 0.")),
            (("قريب! اللي كيمشي ل plus l'infini هو التحت، ماشي la fraction. عاود اختار.", "C'est le dénominateur qui tend vers +∞. Réessaie."),
             ("الجواب هو zéro.", "Réponse : 0."))],
        "Que vaut la limite de trois sur، n plus trois ?"),
])

F = lambda v: (5 * v - 4) / (v + 1)
G = lambda v: (3 * v - 1) / (v + 1)

ENONCE = {
    "intro": "On considère la suite numérique (uₙ) définie par : u₀ = 3 et uₙ₊₁ = (5uₙ − 4)/(uₙ + 1) pour tout entier naturel n.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا la suite u indice n: u zéro égale trois، وu indice n plus un égale، cinq u indice n moins quatre، sur u indice n plus un، pour tout n.",
    "figures": [nuage(termes(3, F), 2, 4)],
    "donnees": ["u₀ = 3", "uₙ₊₁ = (5uₙ − 4)/(uₙ + 1) pour tout n ∈ ℕ", "vₙ = 1/(uₙ − 2) (question 3)"],
    "questions": QUESTIONS,
}

SIMILAIRE = {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
        "intro": "On considère la suite (uₙ) définie par : u₀ = 2 et uₙ₊₁ = (3uₙ − 1)/(uₙ + 1) pour tout n. On pose vₙ = 1/(uₙ − 1).",
        "intro_dit": "نفس التمرين، بأرقام أخرى: u zéro égale deux، وu indice n plus un égale، trois u indice n moins un، sur u indice n plus un. وv indice n égale un sur، u indice n moins un.",
        "figures": [nuage(termes(2, G), 1, 3)],
        "donnees": ["u₀ = 2", "uₙ₊₁ = (3uₙ − 1)/(uₙ + 1)", "vₙ = 1/(uₙ − 1)"],
        "questions": [
            {"id": "1", "texte": "Vérifier que uₙ₊₁ − 1 = 2(uₙ − 1)/(uₙ + 1), puis montrer par récurrence que uₙ > 1 pour tout n.",
             "reponse": phrase("uₙ₊₁ − 1 = (3uₙ − 1 − uₙ − 1)/(uₙ + 1) = 2(uₙ − 1)/(uₙ + 1). u₀ = 2 > 1 ; si uₙ > 1, uₙ − 1 > 0 et uₙ + 1 > 0, donc uₙ₊₁ > 1. Donc uₙ > 1 pour tout n."),
             "clavier": {"aides": ["2(uₙ − 1)/(uₙ + 1)", "uₙ₊₁ − 1 > 0"], "pieges": ["opérations sur l'hypothèse"]},
             "correction": correction([("1 : uₙ₊₁ − 1 = 2(uₙ − 1)/(uₙ + 1)", "même dénominateur"), ("u₀ = 2 > 1 ; uₙ > 1 ⇒ uₙ₊₁ − 1 > 0", "supposons que"),
                                       ("d'après le principe de récurrence, uₙ > 1 pour tout n", "d'après le principe de récurrence")],
                                      "même dénominateur: deux fois، u indice n moins un، sur u indice n plus un. u zéro égale deux، supérieur à un. supposons que u indice n supérieur à un: le numérateur positif وle dénominateur positif. d'après le principe de récurrence، u indice n supérieur à un pour tout n.")},
            {"id": "2-1", "texte": "Montrer que uₙ₊₁ − uₙ = −(uₙ − 1)²/(uₙ + 1), puis en déduire que (uₙ) est décroissante.",
             "reponse": phrase("uₙ₊₁ − uₙ = (3uₙ − 1 − uₙ² − uₙ)/(uₙ + 1) = −(uₙ − 1)²/(uₙ + 1) ≤ 0 : (uₙ) est décroissante."),
             "clavier": {"aides": ["(uₙ − 1)²", "≤ 0"], "pieges": ["croissante"]},
             "correction": correction([("2-1 : uₙ₊₁ − uₙ = −(uₙ² − 2uₙ + 1)/(uₙ + 1) = −(uₙ − 1)²/(uₙ + 1) ≤ 0", "au carré"), ("(uₙ) décroissante", "décroissante")],
                                      "la différence égale moins، u indice n moins un au carré، sur u indice n plus un. le carré positif، le dénominateur positif، إذن inférieur ou égal à zéro: la suite décroissante.")},
            {"id": "2-2", "texte": "En déduire que la suite (uₙ) est convergente.",
             "reponse": phrase("(uₙ) est décroissante et minorée par 1, donc convergente."),
             "clavier": {"aides": ["décroissante", "minorée par 1"], "pieges": ["majorée"]},
             "correction": correction([("2-2 : décroissante et minorée par 1, donc convergente", "décroissante et minorée")],
                                      "la suite décroissante et minorée par un، donc convergente.")},
            {"id": "3-1", "texte": "Montrer que (vₙ) est arithmétique de raison 1/2, et calculer v₀.",
             "reponse": phrase("vₙ₊₁ = (uₙ + 1)/(2(uₙ − 1)) = ((uₙ − 1) + 2)/(2(uₙ − 1)) = 1/2 + vₙ ; v₀ = 1/(2 − 1) = 1."),
             "clavier": {"aides": ["uₙ + 1 = (uₙ − 1) + 2", "vₙ₊₁ − vₙ = 1/2"], "pieges": ["vₙ₊₁ = (1/2)vₙ"]},
             "correction": correction([("3-1 : vₙ₊₁ = (uₙ + 1)/(2(uₙ − 1)) = 1/2 + vₙ", "un sur deux plus v indice n"), ("raison 1/2 ; v₀ = 1", "v zéro égale un")],
                                      "v indice n plus un égale، u indice n plus un، sur deux fois، u indice n moins un، يعني un sur deux plus v indice n. arithmétique، la raison un sur deux، وv zéro égale un.")},
            {"id": "3-2", "texte": "Exprimer vₙ en fonction de n, puis montrer que uₙ = 1 + 2/(n + 2).",
             "reponse": phrase("vₙ = 1 + n/2 = (n + 2)/2 ; uₙ = 1 + 1/vₙ = 1 + 2/(n + 2)."),
             "clavier": {"aides": ["vₙ = v₀ + n r", "uₙ = 1 + 1/vₙ"], "pieges": ["vₙ = (1/2)ⁿ"]},
             "correction": correction([("3-2 : vₙ = (n + 2)/2 ; uₙ = 1 + 2/(n + 2)", "u indice n égale un plus deux sur")],
                                      "v indice n égale un plus n sur deux. u indice n égale un plus un sur v indice n، يعني u indice n égale un plus deux sur، n plus deux.")},
            {"id": "3-3", "texte": "Calculer la limite de la suite (uₙ).",
             "reponse": valeur("lim uₙ", 1, "lim 2/(n + 2) = 0 ; lim uₙ = 1 + 0 = 1"),
             "clavier": {"aides": ["lim 2/(n + 2) = 0"], "pieges": ["lim uₙ = 2"]},
             "correction": correction([("3-3 : lim 2/(n + 2) = 0, donc lim uₙ = 1", "la limite égale un")],
                                      "deux sur، n plus deux، كتمشي ل zéro. إذن la limite égale un.")},
        ]}}

EX = {"id": ID, "type": "exercice", "version": 1, "status": "published", "matiere": "mathematiques",
      "chapitre": "suites_definition", "cours": "math_ch3_suites_numeriques",
      "titre": "Une suite homographique : récurrence, monotonie, suite auxiliaire arithmétique", "niveau": "moyen", "duree_min": 35,
      "origine": ORIGINE,
      "competences": ["Rédiger une récurrence par le signe de uₙ₊₁ − a", "Étudier la monotonie par uₙ₊₁ − uₙ factorisé",
                      "Conclure à la convergence (monotone et bornée)", "Montrer qu'une suite auxiliaire est arithmétique",
                      "Exprimer uₙ en fonction de n et calculer sa limite"],
      "enonce": ENONCE, "explication": EXPLICATION, "facile": FACILE, "similaire": SIMILAIRE}

if __name__ == "__main__":
    ecrire(EX)
