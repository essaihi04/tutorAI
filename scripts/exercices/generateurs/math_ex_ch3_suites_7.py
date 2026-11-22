# Exercice de maths, ch. 3 (suites numériques), niveau supérieur (au-dessus du national, même forme) :
# une somme Sₙ encadrée terme à terme, limite par les gendarmes, puis une limite par minoration (√n → +∞).
# Sources comparées (lecture seule, rien de recopié) :
#  - exploration suites_definition.json : cadre SU6 (lim nᵅ, fraction en n), SU7 (critères de comparaison : gendarmes,
#    uₙ ≥ vₙ avec vₙ → +∞), SU11 (somme Sₙ et sa limite) ; pieges « compte n termes au lieu de n + 1 »,
#    « lim uₙ = lim du majorant à partir d'un seul majorant », « l'inverse change le sens » ; erreurs_examen « somme de
#    termes » et « limite après une majoration » ; a_ne_pas_dire « plus haut degré sur plus haut degré » (on factorise) ;
#  - vidéos : Rabie Ghazouani 4YsAlmrILpE (gendarmes au tableau), MedBrahmi fSulj1kZQ0g (résumé : comparaison),
#    Math & Phys pA2XEI1Uv_s (sommes, avec l'exercice faux Sₙ − Sₙ₋₁ signalé), Prof fati sTW82JsN5bY (lim nᵅ) ;
#  - nationaux : 2022 R 2-c et 2023 R (sommes de termes), 2020 N 3-b, 2021 N 4-a, 2025 R 2-e (limite par comparaison),
#    2021 R 3-c ((n + 1)/(n + 3)) — aucun n'encadre une somme terme à terme : c'est le niveau au-dessus ;
#  - séries en ligne (résultats de recherche, pages non ouvertes : réseau fermé) : fayssalmaths série 3 « limite d'une
#    suite » (2 BIOF), moutamadris 2 bac PC/SVT série 1 (limites de suites), talamidi 2 bac PC série corrigée 3,
#    xriadiat exercices corrigés « suites et limites de suites », pdfmath exercices nationaux corrigés.
# Données propres à Moalim : Sₙ = n/(n² + 1) + n/(n² + 2) + … + n/(n² + n) (n ≥ 1), lim Sₙ = 1.
import sys
from fractions import Fraction as Fr
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa: E402,F401,F403

ID = "math_ex_ch3_suites_7"
S = "/media/simulations/maths/suites-tableau/"


def figure(c):
    """Les points (n ; Sₙ) entre les deux bornes c·x/(x + 1) et c·x²/(x² + 1), sous la droite y = c."""
    el = [{"f": "courbe", "expr": f"{c}*x/(x+1)", "de": 1, "a": 9, "couleur": "vert", "trait": "pointille", "texte": "minorant", "texte_x": 8, "pos": "s"},
          {"f": "courbe", "expr": f"{c}*x^2/(x^2+1)", "de": 1, "a": 9, "couleur": "orange", "trait": "pointille", "texte": "majorant", "texte_x": 2.2, "pos": "n"},
          {"f": "repere", "y": c, "t": f"y = {c}", "couleur": "jaune"}]
    for n in range(1, 9):
        s = sum(Fr(c * n, n * n + k) for k in range(1, n + 1))
        p = {"f": "point", "at": [n, round(float(s), 3)], "couleur": "cyan"}
        if n <= 2:
            p.update({"t": f"S{'₁₂'[n - 1]}", "pos": "se"})
        el.append(p)
    return {"type": "courbe", "titre": "Les points (n ; Sₙ), coincés entre deux bornes",
            "axes": {"x": {"min": 0, "max": 9, "nom": "n", "graduations": list(range(1, 9))},
                     "y": {"min": 0, "max": c + 0.4, "nom": "Sₙ", "graduations": [c / 2, c] if c > 1 else [0.5, 1]}},
            "legende": "Chaque point Sₙ est entre la courbe verte (minorant) et la courbe orange (majorant).",
            "ratio": 0.6, "elements": el}


QUESTIONS = [
    {"id": "1", "texte": "Calculer S₁ et S₂.",
     "texte_dit": "السؤال un: حسب S un وS deux.",
     "reponse": phrase("S₁ = 1/(1 + 1) = 1/2 (un seul terme, k = 1) ; S₂ = 2/(4 + 1) + 2/(4 + 2) = 2/5 + 1/3 = 11/15 (deux termes, k = 1 et k = 2)."),
     "clavier": {"aides": ["n = 1 : un terme", "n = 2 : k = 1 et k = 2", "2/5 + 2/6", "11/15"], "pieges": ["S₂ = 2/5", "S₂ = 2/(4 + 1 + 2)"]},
     "aides": [aide("Dans Sₙ, n est fixé et k va de 1 à n. Pour S₁ : n = 1, un seul terme. Pour S₂ : n = 2, k = 1 puis k = 2.",
                    "فS indice n، n ثابت، وk كيمشي من un حتى ل n. فS un: n égale un، terme واحد. فS deux: n égale deux، وk égale un ومن بعد deux."),
               aide("S₂ = 2/(2² + 1) + 2/(2² + 2) : réduis au même dénominateur 15.",
                    "S deux égale deux sur cinq، plus deux sur six. دير نفس المقام quinze.")],
     "correction": correction([
         ("1 : S₁ = 1/(1² + 1) = 1/2", "S un égale un sur deux"),
         ("S₂ = 2/(2² + 1) + 2/(2² + 2) = 2/5 + 1/3 = 11/15", "S deux égale onze sur quinze")],
         "السؤال un. S un: terme واحد، un sur، un plus un: S un égale un sur deux. S deux: deux termes، deux sur cinq، plus deux sur six. deux sur six هي un sur trois. نفس المقام quinze: six sur quinze plus cinq sur quinze. S deux égale onze sur quinze."),
     "explication": "ex_1", "facile": "fa_1"},
    {"id": "2", "texte": "Soit n ≥ 1. Montrer que pour tout entier k tel que 1 ≤ k ≤ n : n/(n² + n) ≤ n/(n² + k) ≤ n/(n² + 1).",
     "texte_dit": "السؤال deux: n أكبر من un. بين بلي، pour tout k بين un وn، n sur، n carré plus n، inférieur ou égal à n sur، n carré plus k، inférieur ou égal à n sur، n carré plus un.",
     "reponse": phrase("1 ≤ k ≤ n donne n² + 1 ≤ n² + k ≤ n² + n ; ces nombres sont positifs, donc en passant à l'inverse 1/(n² + n) ≤ 1/(n² + k) ≤ 1/(n² + 1) ; on multiplie par n > 0 : n/(n² + n) ≤ n/(n² + k) ≤ n/(n² + 1)."),
     "clavier": {"aides": ["n² + 1 ≤ n² + k ≤ n² + n", "passer à l'inverse", "× n (n > 0)"], "pieges": ["1/(n² + 1) ≤ 1/(n² + k)", "sans dire que n > 0"]},
     "aides": [aide("Pars de 1 ≤ k ≤ n et ajoute n² partout. Puis regarde les dénominateurs.",
                    "بدا من k بين un وn، وزيد n carré للجميع. ومن بعد شوف les dénominateurs."),
               aide("Pour des nombres positifs, passer à l'inverse change le sens ; multiplier par n > 0 le garde.",
                    "فأعداد positifs، المقلوب كيبدل الاتجاه. والضرب فn، وهو positif، كيخلي الاتجاه.")],
     "correction": correction([
         ("2 : 1 ≤ k ≤ n donne n² + 1 ≤ n² + k ≤ n² + n", "زيد n carré"),
         ("nombres positifs : 1/(n² + n) ≤ 1/(n² + k) ≤ 1/(n² + 1)", "المقلوب كيبدل الاتجاه"),
         ("n > 0 : n/(n² + n) ≤ n/(n² + k) ≤ n/(n² + 1)", "نضربو فn")],
         "السؤال deux. k بين un وn. زيد n carré: n carré plus un، inférieur ou égal à n carré plus k، inférieur ou égal à n carré plus n. هادو positifs، والمقلوب كيبدل الاتجاه: un sur، n carré plus n، هو الصغير. ومن بعد نضربو فn، وهو positif، نفس الاتجاه."),
     "explication": "ex_2", "facile": "fa_2"},
    {"id": "3", "texte": "En déduire que n²/(n² + n) ≤ Sₙ ≤ n²/(n² + 1) pour tout n ≥ 1.",
     "texte_dit": "السؤال trois: استنتج بلي n carré sur، n carré plus n، inférieur ou égal à S indice n، inférieur ou égal à n carré sur، n carré plus un.",
     "reponse": phrase("Sₙ est la somme des n termes n/(n² + k), k de 1 à n. On additionne les n encadrements de la question 2 : n × n/(n² + n) ≤ Sₙ ≤ n × n/(n² + 1), soit n²/(n² + n) ≤ Sₙ ≤ n²/(n² + 1)."),
     "clavier": {"aides": ["n termes (k de 1 à n)", "on additionne les encadrements", "n × n/(n² + n)"], "pieges": ["n + 1 termes", "n/(n² + n) ≤ Sₙ"]},
     "aides": [aide("Combien de termes dans Sₙ ? k va de 1 à n : n − 1 + 1 termes.",
                    "شحال من terme فS indice n؟ k من un حتى ل n: n moins un plus un، يعني n termes."),
               aide("Chaque terme est au moins n/(n² + n) et au plus n/(n² + 1) : la somme de n termes est au moins n fois le plus petit.",
                    "كل terme أكبر من n sur، n carré plus n، وأصغر من n sur، n carré plus un. إذن la somme ديال n termes أكبر من n fois الصغير، وأصغر من n fois الكبير.")],
     "correction": correction([
         ("3 : Sₙ compte n termes (k = 1, …, n)", "n termes"),
         ("on additionne les n encadrements de 2 : n × n/(n² + n) ≤ Sₙ ≤ n × n/(n² + 1)", "نجمعو"),
         ("donc n²/(n² + n) ≤ Sₙ ≤ n²/(n² + 1)", "n carré sur")],
         "السؤال trois. S indice n فيها n termes، من k égale un حتى ل n. نجمعو les encadrements: n fois الصغير، inférieur ou égal à S indice n، inférieur ou égal à n fois الكبير. إذن n carré sur، n carré plus n، inférieur ou égal à S indice n، inférieur ou égal à n carré sur، n carré plus un."),
     "explication": "ex_3", "facile": "fa_3"},
    {"id": "4", "texte": "Calculer les limites de n²/(n² + n) et de n²/(n² + 1), puis en déduire la limite de (Sₙ).",
     "texte_dit": "السؤال quatre: حسب la limite ديال n carré sur، n carré plus n، وديال n carré sur، n carré plus un. ومن بعد استنتج la limite ديال S indice n.",
     "reponse": valeur("lim Sₙ", 1, "n²/(n² + n) = 1/(1 + 1/n) → 1 et n²/(n² + 1) = 1/(1 + 1/n²) → 1, car lim 1/n = lim 1/n² = 0 ; d'après les gendarmes, lim Sₙ = 1"),
     "clavier": {"aides": ["factoriser par n²", "1/(1 + 1/n)", "lim 1/n = 0", "gendarmes", "lim Sₙ ="],
                 "pieges": ["lim Sₙ = lim du majorant seul", "∞/∞ = 1 sans calcul"]},
     "aides": [aide("Divise le haut et le bas par n² : n²/(n² + n) = 1/(1 + 1/n). Que devient 1/n ?",
                    "قسم الفوق والتحت على n carré: كتولي un sur، un plus un sur n. شنو كيولي un sur n؟"),
               aide("Si les deux bornes ont la même limite, la suite coincée entre elles a cette limite (gendarmes).",
                    "يلا جوج bornes عندهم نفس la limite، la suite اللي محصورة بيناتهم عندها نفس la limite.")],
     "correction": correction([
         ("4 : n²/(n² + n) = 1/(1 + 1/n) et lim 1/n = 0, donc lim n²/(n² + n) = 1", "un sur، un plus un sur n"),
         ("n²/(n² + 1) = 1/(1 + 1/n²) et lim 1/n² = 0, donc lim n²/(n² + 1) = 1", "un sur n carré"),
         ("les deux bornes tendent vers 1 : d'après les gendarmes, lim Sₙ = 1", "la limite égale un")],
         "السؤال quatre. n carré sur، n carré plus n، égale un sur، un plus un sur n. un sur n كتمشي ل zéro، إذن la limite un. ونفس الشي: un sur، un plus un sur n carré، كتمشي ل un. جوج bornes كيمشيو ل un، إذن d'après les gendarmes، la limite égale un."),
     "explication": "ex_4", "facile": "fa_4"},
    {"id": "5", "texte": "Montrer que √n × Sₙ ≥ √n/2 pour tout n ≥ 1, puis en déduire la limite de √n × Sₙ.",
     "texte_dit": "السؤال cinq: بين بلي racine carrée de n fois S indice n، supérieur ou égal à racine carrée de n sur deux. ومن بعد استنتج la limite ديال racine carrée de n fois S indice n.",
     "reponse": phrase("Sₙ ≥ n²/(n² + n) = n/(n + 1), et n/(n + 1) ≥ 1/2 car 2n ≥ n + 1 pour n ≥ 1 ; comme √n > 0, √n × Sₙ ≥ √n/2. Or lim √n/2 = +∞, donc, par comparaison, lim √n × Sₙ = +∞."),
     "clavier": {"aides": ["n²/(n² + n) = n/(n + 1)", "n/(n + 1) ≥ 1/2", "2n ≥ n + 1", "lim √n = +∞", "uₙ ≥ vₙ et vₙ → +∞"],
                 "pieges": ["lim √n × Sₙ = 1", "√n × Sₙ ≤ √n"]},
     "aides": [aide("Simplifie le minorant : n²/(n² + n) = n/(n + 1). Compare n/(n + 1) à 1/2 en faisant un produit en croix.",
                    "بسط le minorant: n carré sur، n carré plus n، égale n sur، n plus un. قارنو مع un sur deux بالضرب en croix."),
               aide("Une suite plus grande qu'une suite qui tend vers +∞ tend vers +∞. Et lim √n = +∞.",
                    "suite أكبر من suite كتمشي ل plus l'infini، حتى هي كتمشي ل plus l'infini. وracine carrée de n كتمشي ل plus l'infini.")],
     "correction": correction([
         ("5 : d'après 3, Sₙ ≥ n²/(n² + n) = n/(n + 1)", "n sur، n plus un"),
         ("n ≥ 1 : 2n ≥ n + 1, donc n/(n + 1) ≥ 1/2 ; et √n > 0 : √n × Sₙ ≥ √n/2", "supérieur ou égal à un sur deux"),
         ("lim √n/2 = +∞, donc par comparaison lim √n × Sₙ = +∞", "plus l'infini")],
         "السؤال cinq. d'après le trois، S indice n أكبر من n sur، n plus un. وn أكبر من un، إذن deux n أكبر من n plus un، يعني n sur، n plus un، supérieur ou égal à un sur deux. نضربو فracine carrée de n، وهي positive. وracine carrée de n sur deux كتمشي ل plus l'infini، إذن par comparaison، la limite plus l'infini."),
     "explication": "ex_5", "facile": "fa_5"},
]

EXPLICATION = deck("explication", "Explication animée", [
    sim("ex_1", "Question 1 : compter les termes", "k va de 1 à n : il y a n termes.",
        S + "arbres.html?vue=arbres", "Des arbres numérotés 5, 6, 7 : dernier − premier + 1",
        "شوف هاد الشجرات: cinq، six، sept. شحال؟ trois: sept moins cinq plus un. القاعدة: le dernier moins le premier، plus un. فS indice n، k كيمشي من un حتى ل n: n moins un plus un، يعني n termes. فS un، terme واحد: un sur deux. فS deux، deux termes: deux sur cinq، plus deux sur six. S deux égale onze sur quinze.",
        [("k de 1 à n : n termes", "يعني n termes"), ("S₁ = 1/2", "فS un"), ("S₂ = 2/5 + 2/6 = 11/15", "S deux égale onze sur quinze")],
        [jusqua("شوف هاد الشجرات", "arbres"), jusqua("شحال؟", "arbre_3"), jusqua("sept moins cinq plus un", "compte"),
         jusqua("القاعدة", "regle"), montre("يعني n termes", "centre:0"), montre("فS un", "centre:1"), montre("S deux égale onze sur quinze", "centre:2")]),
    sim("ex_2", "Question 2 : l'inverse retourne l'encadrement", "Dénominateur plus grand, fraction plus petite.",
        S + "rappels.html?vue=ordre_inverse", "Passer à l'inverse change le sens",
        "deux أصغر من quatre، ولكن un sur deux أكبر من un sur quatre: المقلوب كيبدل الاتجاه. القاعدة: يلا a وb positifs وa أصغر من b، un sur a أكبر من un sur b. عندنا: n carré plus un، أصغر من n carré plus k، أصغر من n carré plus n. ناخدو المقلوب، الاتجاه كيتبدل. ونضربو فn، positif، الاتجاه كيبقى.",
        [("n² + 1 ≤ n² + k ≤ n² + n", "عندنا"), ("n/(n² + n) ≤ n/(n² + k) ≤ n/(n² + 1)", "ونضربو فn")],
        [jusqua("deux أصغر من quatre", "inverse"), jusqua("القاعدة", "regle"), montre("عندنا", "centre:0"), montre("ونضربو فn", "centre:1")]),
    sim("ex_3", "Question 3 : n fois le même nombre", "On additionne n encadrements : n fois le minorant, n fois le majorant.",
        S + "arbres.html?vue=colonne", "Dans l'exemple du cours : 2022 fois 1 = 2022",
        "فl'exemple ديال le cours: كل terme فيه un. كنحسبو les un: un، deux، trois، حتى ل deux mille vingt-deux. deux mille vingt-deux fois un، égale deux mille vingt-deux. عندنا نفس الفكرة: n termes، وكل واحد أكبر من n sur، n carré plus n. إذن S indice n أكبر من n fois هاد العدد، يعني n carré sur، n carré plus n. ونفس الشي من الفوق.",
        [("n termes, chacun ≥ n/(n² + n)", "عندنا نفس الفكرة"), ("n²/(n² + n) ≤ Sₙ ≤ n²/(n² + 1)", "يعني n carré sur")],
        [jusqua("فl'exemple ديال le cours", "colonne"), jusqua("كنحسبو les un", "un_1"), jusqua("deux mille vingt-deux fois un", "les_un"),
         montre("عندنا نفس الفكرة", "centre:0"), montre("يعني n carré sur", "centre:1")]),
    sim("ex_4", "Question 4 : les gendarmes", "Deux bornes de même limite : la suite coincée a cette limite.",
        S + "gendarmes.html?vue=encadre", "Une suite coincée entre deux bornes qui ont la même limite",
        "فl'exemple: التحت borne فzéro. الفوق borne أخرى كتهبط حتى هي نحو zéro. la suite محصورة بيناتهم. جوج bornes كيتزيرو، وla suite معاهم: كتمشي ل zéro. عندنا: n carré sur، n carré plus n، égale un sur، un plus un sur n، كتمشي ل un. وn carré sur، n carré plus un، حتى هي كتمشي ل un. إذن d'après les gendarmes، la limite ديال S indice n égale un.",
        [("n²/(n² + n) → 1 et n²/(n² + 1) → 1", "عندنا"), ("lim Sₙ = 1", "إذن d'après les gendarmes")],
        [jusqua("التحت borne فzéro", "bas"), jusqua("الفوق borne أخرى", "haut"), jusqua("la suite محصورة", "entre"),
         jusqua("جوج bornes كيتزيرو", "resserre"), montre("عندنا", "centre:0"), montre("إذن d'après les gendarmes", "centre:1")]),
    sim("ex_5", "Question 5 : plus grand qu'une suite qui part vers +∞", "√n → +∞, donc √n/2 → +∞, et √n × Sₙ ≥ √n/2.",
        S + "nuage.html?vue=reference", "Les suites de référence : n², √n, 1/n",
        "شوف: n carré كتخرج بالزربة من الفوق. racine carrée de n كتطلع بشوية: un، un virgule quatre un، حتى ل trois virgule un six فn égale dix، ولكن كتمشي ل plus l'infini. وun sur n كتمشي ل zéro. عندنا: racine carrée de n fois S indice n، أكبر من racine carrée de n sur deux. وهادي كتمشي ل plus l'infini. اللي أكبر منها، حتى هو كيمشي ل plus l'infini.",
        [("√n × Sₙ ≥ √n/2", "عندنا"), ("lim √n/2 = +∞ ⇒ lim √n × Sₙ = +∞", "اللي أكبر منها")],
        [jusqua("n carré كتخرج", "carre"), jusqua("racine carrée de n كتطلع", "racine"), jusqua("وun sur n", "inverse"),
         jusqua("عندنا", "regle"), montre("عندنا", "centre:0"), montre("اللي أكبر منها", "centre:1")]),
])

FACILE = deck("facile", "Plus facile, pour s'entraîner", [
    qcm("fa_1", "Plus facile : combien de termes ?", "نتمرنو: شحال من terme فS indice n؟",
        "Sₙ = n/(n² + 1) + n/(n² + 2) + … + n/(n² + n). Combien de termes ?", ["n − 1", "n + 1", "n"], 2, [
            (("ما تقلقش. حسب le dernier moins le premier، plus un. عاود اختار.", "Compte dernier − premier + 1. Réessaie."),
             ("الجواب هو n: k من un حتى ل n.", "Réponse : n termes (k de 1 à n).")),
            (("قريب! k كيبدا من un، ماشي من zéro. عاود اختار.", "k commence à 1, pas à 0. Réessaie."),
             ("الجواب هو n.", "Réponse : n termes.")),
            ("برافو! n moins un plus un، égale n.", "Juste : n − 1 + 1 = n termes.")],
        "Combien de termes dans S indice n ?"),
    vrai_faux("fa_2", "Plus facile : vrai ou faux", "1 ≤ k ≤ n.",
        "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
            ("n² + 1 ≤ n² + k ≤ n² + n.", True, "On ajoute n² à 1 ≤ k ≤ n."),
            ("1/(n² + 1) ≤ 1/(n² + k).", False, "Le plus grand dénominateur donne la plus petite fraction : c'est ≥."),
            ("n/(n² + n) ≤ n/(n² + k).", True, "n² + n est le plus grand dénominateur.")]),
    association("fa_3", "Plus facile : la somme de n termes", "Relie chaque somme à son résultat.",
        "سؤال ساهل: ربط كل somme مع النتيجة ديالها.", "Relie chaque somme de termes égaux à son résultat.",
        [("1", "n termes égaux à n/(n² + n)"), ("2", "n termes égaux à n/(n² + 1)"), ("3", "2022 termes égaux à 1")],
        [("a", "n²/(n² + n)"), ("b", "n²/(n² + 1)"), ("c", "2022"), ("d", "n/(n² + n)")],
        {"1": "a", "2": "b", "3": "c"},
        {"1-a": ("Oui : n × n/(n² + n) = n²/(n² + n).", "برافو: n fois n sur، n carré plus n."),
         "1-b": ("Non : le dénominateur est n² + n.", "لا، le dénominateur هو n carré plus n."),
         "1-c": ("Non : c'est la somme de 2022 fois 1.", "لا، هادي ديال deux mille vingt-deux fois un."),
         "1-d": ("Non : c'est un seul terme ; il y en a n.", "لا، هادا terme واحد، وعندنا n termes."),
         "2-a": ("Non : le dénominateur est n² + 1.", "لا، le dénominateur هو n carré plus un."),
         "2-b": ("Oui : n × n/(n² + 1) = n²/(n² + 1).", "برافو: n fois n sur، n carré plus un."),
         "2-c": ("Non : c'est la somme de 2022 fois 1.", "لا، هادي ديال deux mille vingt-deux fois un."),
         "2-d": ("Non : regarde le dénominateur, et il y a n termes.", "لا، شوف le dénominateur، وعندنا n termes."),
         "3-a": ("Non : 2022 fois 1, c'est 2022.", "لا، deux mille vingt-deux fois un."),
         "3-b": ("Non : 2022 fois 1, c'est 2022.", "لا، deux mille vingt-deux fois un."),
         "3-c": ("Oui : 2022 × 1 = 2022.", "برافو: deux mille vingt-deux fois un، égale deux mille vingt-deux."),
         "3-d": ("Non : 2022 fois 1, c'est 2022.", "لا، deux mille vingt-deux fois un.")},
        ("(1 ; a) (2 ; b) (3 ; c) : n termes égaux à t font n × t.", "القاعدة: n termes كيساويو t، la somme هي n fois t.")),
    qcm("fa_4", "Plus facile : la limite d'une fraction", "سؤال ساهل على la limite.",
        "lim n²/(n² + n) = ?", ["0", "+∞", "1"], 2, [
            (("ما تقلقش. قسم الفوق والتحت على n carré: un sur، un plus un sur n. عاود اختار.", "Divise par n². Réessaie."),
             ("الجواب هو un: un sur n كتمشي ل zéro.", "Réponse : 1/(1 + 1/n) → 1.")),
            (("قريب! الفوق والتحت بجوج كيكبرو، خاصنا نقسمو على n carré. عاود اختار.", "Haut et bas grandissent : divise par n². Réessaie."),
             ("الجواب هو un.", "Réponse : 1.")),
            ("برافو! un sur، un plus un sur n، كتمشي ل un.", "Juste : 1/(1 + 1/n) → 1.")],
        "La limite de n carré sur، n carré plus n، égale quoi ?"),
    qcm("fa_5", "Plus facile : minorer pour conclure", "سؤال ساهل: comparaison.",
        "vₙ ≥ √n/2 pour tout n ≥ 1. Alors lim vₙ = …", ["+∞", "1/2", "on ne peut rien dire"], 0, [
            ("برافو! racine carrée de n sur deux كتمشي ل plus l'infini، وv indice n أكبر منها.", "Juste : par comparaison, lim vₙ = +∞."),
            (("ما تقلقش. un sur deux ثابت، ولكن racine carrée de n كتكبر. عاود اختار.", "√n grandit. Réessaie."),
             ("الجواب هو plus l'infini.", "Réponse : +∞.")),
            (("قريب! suite أكبر من suite كتمشي ل plus l'infini، حتى هي كتمشي ل plus l'infini. عاود اختار.", "Plus grande qu'une suite qui tend vers +∞. Réessaie."),
             ("الجواب هو plus l'infini.", "Réponse : +∞."))],
        "v indice n supérieur ou égal à racine carrée de n sur deux. Alors la limite ?"),
])

ENONCE = {
    "intro": "Pour tout entier naturel n ≥ 1, on pose : Sₙ = n/(n² + 1) + n/(n² + 2) + … + n/(n² + n), somme des termes n/(n² + k) pour k allant de 1 à n.",
    "intro_dit": "دابا نقراو l'énoncé. pour tout n أكبر من un، S indice n هي la somme ديال les termes n sur، n carré plus k، ملي k كيمشي من un حتى ل n.",
    "figures": [figure(1)],
    "donnees": ["Sₙ = n/(n² + 1) + n/(n² + 2) + … + n/(n² + n)", "n ≥ 1 ; k va de 1 à n"],
    "questions": QUESTIONS,
}

SIMILAIRE = {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
        "intro": "Pour tout entier n ≥ 1, on pose : Sₙ = 2n/(n² + 1) + 2n/(n² + 2) + … + 2n/(n² + n).",
        "intro_dit": "نفس التمرين، بأرقام أخرى: S indice n هي la somme ديال deux n sur، n carré plus k، ملي k كيمشي من un حتى ل n.",
        "figures": [figure(2)],
        "donnees": ["Sₙ = 2n/(n² + 1) + … + 2n/(n² + n)", "n ≥ 1"],
        "questions": [
            {"id": "1", "texte": "Calculer S₁ et S₂.",
             "reponse": phrase("S₁ = 2/2 = 1 ; S₂ = 4/5 + 4/6 = 4/5 + 2/3 = 22/15."),
             "clavier": {"aides": ["S₁ = 2/(1 + 1)", "4/5 + 4/6"], "pieges": ["S₂ = 4/5"]},
             "correction": correction([("1 : S₁ = 2/(1 + 1) = 1 ; S₂ = 4/5 + 4/6 = 22/15", "S deux égale vingt-deux sur quinze")],
                                      "S un égale deux sur deux، égale un. S deux égale quatre sur cinq، plus quatre sur six، S deux égale vingt-deux sur quinze.")},
            {"id": "2", "texte": "Montrer que pour 1 ≤ k ≤ n : 2n/(n² + n) ≤ 2n/(n² + k) ≤ 2n/(n² + 1).",
             "reponse": phrase("n² + 1 ≤ n² + k ≤ n² + n, positifs ; l'inverse change le sens ; × 2n > 0 : 2n/(n² + n) ≤ 2n/(n² + k) ≤ 2n/(n² + 1)."),
             "clavier": {"aides": ["n² + 1 ≤ n² + k ≤ n² + n", "× 2n"], "pieges": ["sens non changé"]},
             "correction": correction([("2 : n² + 1 ≤ n² + k ≤ n² + n ; inverses : sens contraire ; × 2n > 0", "المقلوب")],
                                      "n carré plus un، أصغر من n carré plus k، أصغر من n carré plus n. المقلوب كيبدل الاتجاه، والضرب فdeux n كيخليه.")},
            {"id": "3", "texte": "En déduire que 2n²/(n² + n) ≤ Sₙ ≤ 2n²/(n² + 1).",
             "reponse": phrase("Sₙ a n termes ; on additionne : n × 2n/(n² + n) ≤ Sₙ ≤ n × 2n/(n² + 1)."),
             "clavier": {"aides": ["n termes"], "pieges": ["n + 1 termes"]},
             "correction": correction([("3 : n termes : 2n²/(n² + n) ≤ Sₙ ≤ 2n²/(n² + 1)", "n termes")],
                                      "S indice n فيها n termes. نجمعو: deux n carré sur، n carré plus n، inférieur ou égal à S indice n، inférieur ou égal à deux n carré sur، n carré plus un.")},
            {"id": "4", "texte": "Calculer les limites des deux bornes, puis la limite de (Sₙ).",
             "reponse": valeur("lim Sₙ", 2, "2n²/(n² + n) = 2/(1 + 1/n) → 2 et 2n²/(n² + 1) = 2/(1 + 1/n²) → 2 ; d'après les gendarmes, lim Sₙ = 2"),
             "clavier": {"aides": ["2/(1 + 1/n)", "gendarmes"], "pieges": ["lim Sₙ = 1"]},
             "correction": correction([("4 : les deux bornes tendent vers 2 : lim Sₙ = 2", "la limite égale deux")],
                                      "deux sur، un plus un sur n، كتمشي ل deux، ونفس الشي للأخرى. d'après les gendarmes، la limite égale deux.")},
            {"id": "5", "texte": "Montrer que √n × Sₙ ≥ √n pour tout n ≥ 1, puis en déduire la limite de √n × Sₙ.",
             "reponse": phrase("Sₙ ≥ 2n/(n + 1) ≥ 1 car 2n ≥ n + 1 ; donc √n × Sₙ ≥ √n, et lim √n = +∞ : lim √n × Sₙ = +∞."),
             "clavier": {"aides": ["2n/(n + 1) ≥ 1", "lim √n = +∞"], "pieges": ["lim = 2"]},
             "correction": correction([("5 : Sₙ ≥ 2n/(n + 1) ≥ 1, donc √n × Sₙ ≥ √n → +∞ : lim √n × Sₙ = +∞", "plus l'infini")],
                                      "S indice n أكبر من deux n sur، n plus un، وهادي أكبر من un. إذن racine carrée de n fois S indice n، أكبر من racine carrée de n، اللي كتمشي ل plus l'infini.")},
        ]}}

EX = {"id": ID, "type": "exercice", "version": 1, "status": "published", "matiere": "mathematiques",
      "chapitre": "suites_definition", "cours": "math_ch3_suites_numeriques",
      "titre": "Une somme encadrée terme à terme : gendarmes et comparaison", "niveau": "difficile", "duree_min": 40,
      "origine": ORIGINE,
      "competences": ["Compter les termes d'une somme", "Encadrer une somme terme à terme",
                      "Calculer la limite d'une fraction en n", "Conclure par les gendarmes ou par minoration"],
      "enonce": ENONCE, "explication": EXPLICATION, "facile": FACILE, "similaire": SIMILAIRE}

if __name__ == "__main__":
    ecrire(EX)
