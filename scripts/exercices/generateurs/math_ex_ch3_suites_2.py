# Exercice de maths, ch. 3 (suites numériques), niveau facile : premier terme, récurrence, signe de uₙ₊₁ − uₙ.
# Sources comparées (lecture seule, rien de recopié) :
#  - exploration suites_definition.json : redaction_nationale recurrence_affine et monotonie_difference ; pieges
#    « supposons pour tout n », « opérations dans le mauvais ordre (× puis +) », « deux termes ne suffisent pas » ;
#    erreurs_examen « récurrence (toutes les formes) », « monotonie » ;
#  - vidéos : Driss DOTCOM RRRnDJ2bdlc (opérations successives sur l'hypothèse), maths variés czAlKlF4axM (trois titres,
#    « pour tout n » barré), Mouad Tahiri b7iH3KUEoZc (factoriser (uₙ − ℓ)), Prof fati NNxZYDMA_v4 (u₁ en remplaçant n par 0) ;
#  - nationaux : 2016 R 1-a / 1-b et 2017 R 1-a / 1-b (même type de questions, autres suites), 2020 N 1 (calcul de u₁) ;
#  - séries en ligne (résultats de recherche, pages non ouvertes : réseau fermé) : talamidi 2 bac PC série corrigée 3,
#    moutamadris 2 bac PC/SVT série 1, fayssalmaths séries corrigées 2 bac SE, pdfmath exercices nationaux corrigés 2 bac PC,
#    xriadiat exercices corrigés suites.
# Données propres à Moalim : u₀ = 6, uₙ₊₁ = (1/3)uₙ + 2 (aucun sujet national ne l'utilise).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa: E402,F401,F403

ID = "math_ex_ch3_suites_2"
S = "/media/simulations/maths/suites-tableau/"

QUESTIONS = [
    {"id": "1", "texte": "Calculer u₁.",
     "texte_dit": "السؤال un: حسب u un.",
     "reponse": valeur("u₁", 4, "u₁ = (1/3)u₀ + 2 = (1/3) × 6 + 2 = 2 + 2 = 4"),
     "clavier": {"aides": ["n = 0", "u₁ = (1/3)u₀ + 2", "u₁ ="], "pieges": ["u₁ = u₀ + 1", "(1/3)(6 + 2)"]},
     "aides": [aide("u₁ est le terme qui suit u₀ : remplace n par 0 dans la relation de récurrence.",
                    "u un هو le terme اللي كيجي من بعد u zéro. عوض n ب zéro فla relation."),
               aide("u₁ = (1/3) × u₀ + 2 : on multiplie d'abord par 1/3, puis on ajoute 2.",
                    "u un égale un sur trois fois u zéro، plus deux. الأول كنضربو فun sur trois، ومن بعد كنزيدو deux.")],
     "correction": correction([
         ("1 : pour n = 0 : u₁ = (1/3)u₀ + 2", "pour n égale zéro"),
         ("u₁ = (1/3) × 6 + 2 = 2 + 2 = 4", "u un égale quatre")],
         "السؤال un. pour n égale zéro، u un égale un sur trois fois u zéro، plus deux. يعني un sur trois fois six، كتعطي deux، plus deux. إذن u un égale quatre."),
     "explication": "ex_1", "facile": "fa_1"},
    {"id": "2", "texte": "Montrer par récurrence que uₙ > 3 pour tout entier naturel n.",
     "texte_dit": "السؤال deux: بين par récurrence بلي u indice n supérieur à trois، pour tout n.",
     "reponse": phrase("Initialisation : u₀ = 6 > 3. Hérédité : soit n ∈ ℕ, supposons uₙ > 3 ; alors (1/3)uₙ > 1 (car 1/3 > 0), donc (1/3)uₙ + 2 > 3, c'est-à-dire uₙ₊₁ > 3. Conclusion : d'après le principe de récurrence, uₙ > 3 pour tout n ∈ ℕ."),
     "clavier": {"aides": ["Initialisation", "Hérédité : soit n ∈ ℕ, supposons uₙ > 3", "× 1/3", "+ 2", "Conclusion"],
                 "pieges": ["supposons que pour tout n, uₙ > 3", "u₁ = 4 > 3 donc vrai"]},
     "aides": [aide("Trois titres : Initialisation (n = 0), Hérédité (on suppose uₙ > 3, on montre uₙ₊₁ > 3), Conclusion.",
                    "تلاتة ديال العناوين: initialisation، فn égale zéro. hérédité: كنفترضو u indice n supérieur à trois، وكنبينو u indice n plus un supérieur à trois. ومن بعد la conclusion."),
               aide("Dans l'hérédité, fais à l'inégalité ce que la formule fait à uₙ : d'abord × 1/3 (positif : même sens), puis + 2.",
                    "فl'hérédité، دير للinégalité نفس الشي اللي كديرو la formule ل u indice n: الأول fois un sur trois، وهو positif، إذن نفس الاتجاه. ومن بعد plus deux.")],
     "correction": correction([
         ("2 : Initialisation : pour n = 0, u₀ = 6 > 3", "u zéro égale six"),
         ("Hérédité : soit n ∈ ℕ, supposons que uₙ > 3 et montrons que uₙ₊₁ > 3", "supposons que u indice n"),
         ("(1/3)uₙ > 1 (car 1/3 > 0), donc (1/3)uₙ + 2 > 3 : uₙ₊₁ > 3", "fois un sur trois"),
         ("Conclusion : d'après le principe de récurrence, pour tout n ∈ ℕ, uₙ > 3", "d'après le principe de récurrence")],
         "السؤال deux. initialisation: u zéro égale six، وsix supérieur à trois. hérédité: soit n، supposons que u indice n supérieur à trois، ونبينو u indice n plus un supérieur à trois. نضربو fois un sur trois، وهو positif: un sur trois fois u indice n، supérieur à un. نزيدو deux: u indice n plus un، supérieur à trois. conclusion: d'après le principe de récurrence، u indice n supérieur à trois، pour tout n."),
     "explication": "ex_2", "facile": "fa_2"},
    {"id": "3", "texte": "Vérifier que uₙ₊₁ − uₙ = −(2/3)(uₙ − 3) pour tout entier naturel n.",
     "texte_dit": "السؤال trois: تحقق بلي u indice n plus un moins u indice n، égale moins deux sur trois، fois، u indice n moins trois.",
     "reponse": phrase("uₙ₊₁ − uₙ = (1/3)uₙ + 2 − uₙ = −(2/3)uₙ + 2 = −(2/3)(uₙ − 3)."),
     "clavier": {"aides": ["(1/3)uₙ + 2 − uₙ", "(1/3 − 1)uₙ", "−(2/3)uₙ + 2", "−(2/3)(uₙ − 3)"], "pieges": ["(1/3)uₙ − uₙ = (1/3)", "−(2/3)(uₙ + 3)"]},
     "aides": [aide("Remplace uₙ₊₁ par son expression, puis regroupe les uₙ : (1/3)uₙ − uₙ = (1/3 − 1)uₙ.",
                    "عوض u indice n plus un بالexpression ديالو، ومن بعد جمع les u indice n: un sur trois moins un، fois u indice n."),
               aide("Mets −2/3 en facteur : 2 = (−2/3) × (−3). Vérifie en redéveloppant.",
                    "خرج moins deux sur trois en facteur. deux égale moins deux sur trois fois moins trois. تحقق ملي تنشر من جديد.")],
     "correction": correction([
         ("3 : uₙ₊₁ − uₙ = (1/3)uₙ + 2 − uₙ", "on remplace"),
         ("= −(2/3)uₙ + 2", "moins deux sur trois u indice n plus deux"),
         ("= −(2/3)(uₙ − 3)", "en facteur")],
         "السؤال trois. on remplace u indice n plus un: un sur trois u indice n، plus deux، moins u indice n. un sur trois moins un، كتعطي moins deux sur trois. إذن moins deux sur trois u indice n plus deux. ونخرجو moins deux sur trois en facteur: moins deux sur trois، fois، u indice n moins trois."),
     "explication": "ex_3", "facile": "fa_3"},
    {"id": "4", "texte": "En déduire que la suite (uₙ) est décroissante.",
     "texte_dit": "السؤال quatre: استنتج بلي la suite u indice n décroissante.",
     "reponse": phrase("D'après la question 2, uₙ > 3, donc uₙ − 3 > 0 ; et −2/3 < 0, donc uₙ₊₁ − uₙ = −(2/3)(uₙ − 3) < 0 pour tout n : la suite (uₙ) est décroissante."),
     "clavier": {"aides": ["uₙ − 3 > 0", "−2/3 < 0", "uₙ₊₁ − uₙ < 0", "pour tout n"], "pieges": ["u₁ < u₀ donc décroissante", "croissante"]},
     "aides": [aide("Regarde le signe de chaque facteur de uₙ₊₁ − uₙ = −(2/3)(uₙ − 3). La question 2 donne le signe de uₙ − 3.",
                    "شوف le signe ديال كل facteur. السؤال deux كيعطيك le signe ديال u indice n moins trois."),
               aide("Un négatif fois un positif donne un négatif : uₙ₊₁ − uₙ < 0 pour tout n. Deux termes u₀ > u₁ ne suffisent pas.",
                    "négatif fois positif كتعطي négatif. وماشي كافي نقارنو u zéro وu un: خاص pour tout n.")],
     "correction": correction([
         ("4 : d'après 2, uₙ > 3, donc uₙ − 3 > 0", "d'après le deux"),
         ("−2/3 < 0, donc uₙ₊₁ − uₙ < 0 pour tout n", "inférieur à zéro pour tout n"),
         ("donc la suite (uₙ) est décroissante", "décroissante")],
         "السؤال quatre. d'après le deux، u indice n supérieur à trois، إذن u indice n moins trois positif. وmoins deux sur trois négatif. إذن u indice n plus un moins u indice n، inférieur à zéro pour tout n. إذن la suite décroissante."),
     "explication": "ex_4", "facile": "fa_4"},
]

EXPLICATION = deck("explication", "Explication animée", [
    sim("ex_1", "Question 1 : la machine de la récurrence", "uₙ entre, uₙ₊₁ sort : pour u₁, on fait entrer u₀.",
        S + "axe.html?vue=machine", "La machine du cours : × ¼ puis + 12",
        "نشوفو la méthode على هاد l'exemple ديال le cours. هاد الماكينة: u indice n كيدخل، وu indice n plus un كيخرج. فl'exemple، الماكينة كتضرب فun sur quatre، ومن بعد كتزيد douze. كدخل dix-sept، كيخرج seize virgule vingt-cinq: هادا u un. عندنا نفس الفكرة: الماكينة ديالنا كتضرب فun sur trois، ومن بعد كتزيد deux. كدخل six، كيخرج deux plus deux، يعني u un égale quatre.",
        [("uₙ → × 1/3 → + 2 → uₙ₊₁", "الماكينة ديالنا"), ("u₁ = (1/3) × 6 + 2 = 4", "يعني u un égale quatre")],
        [jusqua("هاد الماكينة", "machine"), jusqua("كدخل dix-sept", "u1"), montre("الماكينة ديالنا", "centre:0"),
         montre("يعني u un égale quatre", "centre:1")]),
    sim("ex_2", "Question 2 : les dominos de la récurrence", "Le premier tombe, chacun fait tomber le suivant : tous tombent.",
        S + "dominos.html?vue=principe", "Initialisation, hérédité, conclusion",
        "la récurrence بحال les dominos. initialisation: le premier كيطيح، يعني u zéro égale six، supérieur à trois. hérédité: يلا طاح le domino n، كيطيح le domino n plus un. يعني supposons que u indice n supérieur à trois. نضربو fois un sur trois: un sur trois u indice n، supérieur à un. نزيدو deux: u indice n plus un، supérieur à trois. conclusion: كاملين كيطيحو، u indice n supérieur à trois pour tout n.",
        [("u₀ = 6 > 3", "initialisation"), ("uₙ > 3 ⇒ (1/3)uₙ + 2 > 3", "نزيدو deux"), ("uₙ > 3 pour tout n", "conclusion")],
        [jusqua("la récurrence بحال les dominos", "rangee"), jusqua("initialisation", "premier_tombe"), montre("initialisation", "centre:0"),
         jusqua("hérédité", "passage"), montre("نزيدو deux", "centre:1"), jusqua("conclusion", "tous"), montre("conclusion", "centre:2")]),
    sim("ex_3", "Question 3 : réduire et mettre en facteur", "Regrouper les uₙ, puis faire apparaître (uₙ − 3).",
        S + "calculs.html?vue=m2", "La même méthode sur l'exemple du cours",
        "نشوفو la méthode على l'exemple ديال le cours: u indice n plus un égale un sur seize u indice n، plus quinze sur seize. أولا كنعوضو u indice n plus un. ثانيا كنجمعو les u indice n: un sur seize moins un، كتعطي moins quinze sur seize. ثالثا كنخرجو moins quinze sur seize en facteur. عندنا نفس الخطوات: un sur trois moins un، كتعطي moins deux sur trois. إذن moins deux sur trois u indice n plus deux، égale moins deux sur trois، fois، u indice n moins trois.",
        [("(1/3 − 1)uₙ = −(2/3)uₙ", "عندنا نفس الخطوات"), ("−(2/3)uₙ + 2 = −(2/3)(uₙ − 3)", "إذن moins deux sur trois u indice n plus deux")],
        [jusqua("أولا كنعوضو", "difference"), jusqua("ثالثا كنخرجو", "factorise"),
         montre("عندنا نفس الخطوات", "centre:0"), montre("إذن moins deux sur trois u indice n plus deux", "centre:1")]),
    sim("ex_4", "Question 4 : décroissante, pour tout n", "Deux termes ne suffisent pas : il faut uₙ₊₁ − uₙ < 0 pour tout n.",
        S + "nuage.html?vue=monotonie", "u₁ > u₀, et pourtant la suite n'est pas croissante",
        "شوف هاد جوج نقط: u zéro égale deux، وu un égale trois. طلعات. واش la suite croissante؟ شوف النقط اللي من بعد: كيهبطو. إذن deux termes ما كافيينش. خاص le signe ديال u indice n plus un moins u indice n، pour tout n. عندنا u indice n moins trois positif، من السؤال deux، وmoins deux sur trois négatif. إذن la différence négative، pour tout n: la suite décroissante.",
        [("pour tout n", "pour tout n"), ("uₙ₊₁ − uₙ = −(2/3)(uₙ − 3) < 0", "إذن la différence négative")],
        [jusqua("شوف هاد جوج نقط", "deux_points"), jusqua("واش la suite croissante؟", "fleche"),
         jusqua("شوف النقط اللي من بعد", "suite"), jusqua("إذن deux termes ما كافيينش", "contre_exemple"),
         montre("pour tout n", "centre:0"), montre("إذن la différence négative", "centre:1")]),
])

FACILE = deck("facile", "Plus facile, pour s'entraîner", [
    qcm("fa_1", "Plus facile : calculer u₁", "نتمرنو بسؤال ساهل: حسب u un.",
        "u₀ = 6 et uₙ₊₁ = (1/3)uₙ + 2. Que vaut u₁ ?", ["u₁ = 7", "u₁ = 4", "u₁ = 8/3"], 1, [
            (("ما تقلقش. زدتي un ل u zéro. u un ماشي u zéro plus un: عوض n ب zéro فla relation. عاود اختار.", "u₁ n'est pas u₀ + 1 : remplace n par 0. Réessaie."),
             ("الجواب هو quatre: un sur trois fois six، deux، plus deux.", "Réponse : u₁ = (1/3) × 6 + 2 = 4.")),
            ("برافو! un sur trois fois six كتعطي deux، plus deux، égale quatre.", "Juste : u₁ = 2 + 2 = 4."),
            (("قريب! زدتي deux قبل ما تضرب. الأول fois un sur trois، ومن بعد plus deux. عاود اختار.", "Tu as ajouté avant de multiplier. Réessaie."),
             ("الجواب هو quatre: الأول un sur trois fois six، ومن بعد plus deux.", "Réponse : u₁ = 4."))],
        "u zéro égale six، et u indice n plus un égale un sur trois u indice n plus deux. Que vaut u un ?"),
    association("fa_2", "Plus facile : les trois titres", "Relie chaque titre de la récurrence à ce qu'on y écrit.",
        "سؤال ساهل: ربط كل عنوان ديال la récurrence مع اللي كنكتبو فيه.",
        "Relie chaque titre à ce qu'on y écrit.",
        [("1", "Initialisation"), ("2", "Hérédité"), ("3", "Conclusion")],
        [("a", "u₀ = 6 > 3"), ("b", "soit n ∈ ℕ, supposons uₙ > 3 ; montrons uₙ₊₁ > 3"), ("c", "d'après le principe de récurrence, uₙ > 3 pour tout n"),
         ("d", "supposons que uₙ > 3 pour tout n")],
        {"1": "a", "2": "b", "3": "c"},
        {"1-a": ("Oui : on vérifie le premier terme.", "برافو: كنتحققو من le premier terme."),
         "1-b": ("Non : ça, c'est le passage de n à n + 1.", "لا، هادي هي الدوزة من n ل n plus un."),
         "1-c": ("Non : la conclusion vient à la fin.", "لا، la conclusion كتجي فالأخير."),
         "1-d": ("Non : on ne suppose rien à l'initialisation, on vérifie u₀.", "لا، فl'initialisation ما كنفترضو والو، كنتحققو من u zéro."),
         "2-a": ("Non : u₀ = 6 > 3, c'est le premier domino.", "لا، هادا le premier domino."),
         "2-b": ("Oui : on suppose au rang n, on montre au rang n + 1.", "برافو: كنفترضو فالرتبة n، وكنبينو فالرتبة n plus un."),
         "2-c": ("Non : ça se dit quand l'hérédité est finie.", "لا، هادي كتقال ملي كتسالي l'hérédité."),
         "2-d": ("Non : « pour tout n », c'est ce qu'on veut montrer, on ne peut pas le supposer.", "لا، pour tout n هو اللي بغينا نبينو، ما يمكنش نفترضوه."),
         "3-a": ("Non : u₀ = 6 > 3 est l'initialisation.", "لا، هادي initialisation."),
         "3-b": ("Non : c'est l'hérédité.", "لا، هادي hérédité."),
         "3-c": ("Oui : la phrase finale, avec « pour tout n ».", "برافو: الجملة الأخيرة، مع pour tout n."),
         "3-d": ("Non : on conclut, on ne suppose plus.", "لا، هنا كنستنتجو، ما بقيناش كنفترضو.")},
        ("(1 ; a) (2 ; b) (3 ; c) : « supposons pour tout n » est l'intrus, il est faux.",
         "القاعدة: initialisation، hérédité، conclusion. والجملة supposons pour tout n غالطة.")),
    qcm("fa_3", "Plus facile : regrouper les uₙ", "سؤال ساهل: شحال كتعطي un sur trois u indice n moins u indice n؟",
        "(1/3)uₙ − uₙ = ?", ["(1/3)", "−(2/3)uₙ", "(2/3)uₙ"], 1, [
            (("ما تقلقش. u indice n ما كيمشيش: un sur trois moins un، fois u indice n. عاود اختار.", "uₙ ne disparaît pas : (1/3 − 1)uₙ. Réessaie."),
             ("الجواب هو moins deux sur trois u indice n: un sur trois moins un، égale moins deux sur trois.", "Réponse : (1/3 − 1)uₙ = −(2/3)uₙ.")),
            ("برافو! un sur trois moins un، égale moins deux sur trois.", "Juste : (1/3 − 1)uₙ = −(2/3)uₙ."),
            (("قريب! رد البال لle signe: un sur trois صغير على un، إذن النتيجة négative. عاود اختار.", "Attention au signe : 1/3 − 1 < 0. Réessaie."),
             ("الجواب هو moins deux sur trois u indice n.", "Réponse : −(2/3)uₙ."))],
        "un sur trois u indice n moins u indice n égale ?"),
    vrai_faux("fa_4", "Plus facile : vrai ou faux", "uₙ₊₁ − uₙ = −(2/3)(uₙ − 3) et uₙ > 3 pour tout n.",
        "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
            ("u₁ < u₀, donc la suite est décroissante.", False, "Deux termes ne suffisent pas : il faut uₙ₊₁ − uₙ < 0 pour tout n."),
            ("uₙ − 3 > 0 et −2/3 < 0, donc uₙ₊₁ − uₙ < 0 pour tout n.", True, "Un négatif fois un positif est négatif."),
            ("La suite est décroissante.", True, "uₙ₊₁ − uₙ < 0 pour tout n.")]),
])

ENONCE = {
    "intro": "On considère la suite numérique (uₙ) définie par : u₀ = 6 et uₙ₊₁ = (1/3)uₙ + 2 pour tout entier naturel n.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا la suite u indice n: u zéro égale six، وu indice n plus un égale un sur trois u indice n، plus deux، pour tout n.",
    "figures": [{"type": "schema", "titre": "La relation de récurrence : une machine", "cadre": {"l": 10, "h": 3},
                 "legende": "uₙ entre, on multiplie par 1/3, puis on ajoute 2 : uₙ₊₁ sort.",
                 "elements": [{"f": "texte", "at": [0.2, 1.4], "t": "uₙ", "couleur": "cyan", "taille": "grand"},
                              {"f": "fleche", "de": [1.0, 1.5], "a": [2.4, 1.5], "couleur": "blanc"},
                              {"f": "rect", "de": [2.5, 0.8], "a": [7.3, 2.2], "couleur": "jaune", "arrondi": True},
                              {"f": "texte", "at": [4.9, 1.4], "t": "× 1/3  puis  + 2", "couleur": "jaune", "ancre": "centre"},
                              {"f": "fleche", "de": [7.4, 1.5], "a": [8.8, 1.5], "couleur": "blanc"},
                              {"f": "texte", "at": [8.9, 1.4], "t": "uₙ₊₁", "couleur": "cyan", "taille": "grand"}]}],
    "donnees": ["u₀ = 6", "uₙ₊₁ = (1/3)uₙ + 2 pour tout n ∈ ℕ"],
    "questions": QUESTIONS,
}

SIMILAIRE = {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
        "intro": "On considère la suite numérique (uₙ) définie par : u₀ = 1 et uₙ₊₁ = (1/2)uₙ + 2 pour tout entier naturel n.",
        "intro_dit": "نفس التمرين، بأرقام أخرى: u zéro égale un، وu indice n plus un égale un sur deux u indice n، plus deux.",
        "donnees": ["u₀ = 1", "uₙ₊₁ = (1/2)uₙ + 2"],
        "questions": [
            {"id": "1", "texte": "Calculer u₁.",
             "reponse": valeur("u₁", 2.5, "u₁ = (1/2) × 1 + 2 = 2,5"),
             "clavier": {"aides": ["n = 0", "u₁ ="], "pieges": ["u₁ = 2"]},
             "correction": correction([("1 : u₁ = (1/2)u₀ + 2 = 0,5 + 2 = 2,5", "u un égale")],
                                      "pour n égale zéro، u un égale un sur deux fois un، plus deux، égale deux virgule cinq.")},
            {"id": "2", "texte": "Montrer par récurrence que uₙ < 4 pour tout entier naturel n.",
             "reponse": phrase("Initialisation : u₀ = 1 < 4. Hérédité : supposons uₙ < 4 ; (1/2)uₙ < 2, donc (1/2)uₙ + 2 < 4 : uₙ₊₁ < 4. Conclusion : uₙ < 4 pour tout n."),
             "clavier": {"aides": ["Initialisation", "Hérédité", "× 1/2", "+ 2", "Conclusion"], "pieges": ["supposons que pour tout n"]},
             "correction": correction([("2 : Initialisation : u₀ = 1 < 4", "u zéro égale un"),
                                       ("Hérédité : uₙ < 4 ⇒ (1/2)uₙ < 2 ⇒ (1/2)uₙ + 2 < 4 : uₙ₊₁ < 4", "supposons que"),
                                       ("Conclusion : d'après le principe de récurrence, uₙ < 4 pour tout n", "d'après le principe de récurrence")],
                                      "initialisation: u zéro égale un، inférieur à quatre. hérédité: supposons que u indice n inférieur à quatre. fois un sur deux: inférieur à deux. plus deux: u indice n plus un inférieur à quatre. conclusion: d'après le principe de récurrence، u indice n inférieur à quatre pour tout n.")},
            {"id": "3", "texte": "Vérifier que uₙ₊₁ − uₙ = −(1/2)(uₙ − 4) pour tout entier naturel n.",
             "reponse": phrase("uₙ₊₁ − uₙ = (1/2)uₙ + 2 − uₙ = −(1/2)uₙ + 2 = −(1/2)(uₙ − 4)."),
             "clavier": {"aides": ["(1/2 − 1)uₙ", "−(1/2)(uₙ − 4)"], "pieges": ["−(1/2)(uₙ + 4)"]},
             "correction": correction([("3 : uₙ₊₁ − uₙ = (1/2)uₙ + 2 − uₙ = −(1/2)uₙ + 2", "on remplace"),
                                       ("= −(1/2)(uₙ − 4)", "en facteur")],
                                      "on remplace: un sur deux u indice n plus deux moins u indice n، égale moins un sur deux u indice n plus deux. moins un sur deux en facteur: moins un sur deux، fois، u indice n moins quatre.")},
            {"id": "4", "texte": "En déduire le sens de variation de la suite (uₙ).",
             "reponse": phrase("uₙ < 4 donc uₙ − 4 < 0, et −1/2 < 0, donc uₙ₊₁ − uₙ > 0 pour tout n : (uₙ) est croissante."),
             "clavier": {"aides": ["uₙ − 4 < 0", "uₙ₊₁ − uₙ > 0"], "pieges": ["décroissante"]},
             "correction": correction([("4 : uₙ − 4 < 0 et −1/2 < 0, donc uₙ₊₁ − uₙ > 0", "négatif fois négatif"),
                                       ("donc (uₙ) est croissante", "croissante")],
                                      "u indice n moins quatre négatif، وmoins un sur deux négatif. négatif fois négatif كتعطي positif: la différence positive pour tout n. إذن la suite croissante.")},
        ]}}

EX = {"id": ID, "type": "exercice", "version": 1, "status": "published", "matiere": "mathematiques",
      "chapitre": "suites_definition", "cours": "math_ch3_suites_numeriques",
      "titre": "Une suite récurrente : premier terme, récurrence et sens de variation", "niveau": "facile", "duree_min": 15,
      "origine": ORIGINE,
      "competences": ["Calculer un terme d'une suite définie par récurrence", "Rédiger un raisonnement par récurrence",
                      "Étudier le sens de variation par le signe de uₙ₊₁ − uₙ"],
      "enonce": ENONCE, "explication": EXPLICATION, "facile": FACILE, "similaire": SIMILAIRE}

if __name__ == "__main__":
    ecrire(EX)
