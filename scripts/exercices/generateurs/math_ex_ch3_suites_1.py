# Exercice de maths, ch. 3 (suites numériques), niveau facile : suite arithmétique et suite géométrique.
# Sources comparées (lecture seule, rien de recopié) :
#  - exploration suites_definition.json : cas_types calcul_termes / somme_termes, pieges « n termes au lieu de n + 1 »,
#    « q⁰ = 0 », « exposant de la somme = nombre de termes », erreurs_examen « somme de termes » (2022 R, 2023 R) ;
#  - vidéos : Driss DOTCOM RRRnDJ2bdlc (rappels arithmétique / géométrique), Prof fati sTW82JsN5bY (révision des formules),
#    maths variés czAlKlF4axM (somme : nombre de termes × (premier + dernier)/2), Mouad Tahiri b7iH3KUEoZc (erreur q⁰ = 0) ;
#  - nationaux : 2022 R 2-c (S = u₀ + … + u₂₀₂₁ : nombre de termes), 2016 R / 2017 R 2-b (uₙ en fonction de n) ;
#  - séries en ligne (vues par les résultats de recherche, pages non ouvertes : réseau fermé) : talamidi 2 bac PC série
#    corrigée 3 (suites), moutamadris 2 bac PC/SVT série 1, fayssalmaths séries corrigées 2 bac SE, pdfmath « exercices
#    nationaux corrigés 2 bac PC », xriadiat (e-monsite) exercices corrigés suites ; talamidi 1 bac SE séries 2 (rappels).
# Données propres à Moalim : u₀ = 2, r = 5 (comme le réglage de sauts.html : u₀ = 2) ; v₀ = 3, q = 2.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa: E402,F401,F403

ID = "math_ex_ch3_suites_1"
S = "/media/simulations/maths/suites-tableau/"


QUESTIONS = [
    {"id": "1", "texte": "Exprimer uₙ en fonction de n, puis calculer u₈.",
     "texte_dit": "السؤال un: عبر على u indice n en fonction de n، ومن بعد حسب u huit.",
     "reponse": valeur("u₈", 42, "uₙ = u₀ + n r = 2 + 5n ; u₈ = 2 + 5 × 8 = 42"),
     "clavier": {"aides": ["uₙ = u₀ + n r", "2 + 5n", "u₈ ="], "pieges": ["uₙ = u₀ × rⁿ", "u₈ = 2 + 5 × 7"]},
     "aides": [aide("Pour aller de u₀ à u₈, on ajoute la raison r à chaque pas : combien de pas ?",
                    "باش نمشيو من u zéro حتى ل u huit، كل مرة كنزيدو la raison r. شحال من خطوة كاينة؟"),
               aide("Formule d'une suite arithmétique : uₙ = u₀ + n r, avec u₀ = 2 et r = 5.",
                    "la formule ديال suite arithmétique: u indice n égale u zéro plus n fois r. وهنا u zéro égale deux، وr égale cinq.")],
     "correction": correction([
         ("1 : (uₙ) arithmétique de raison r = 5 : uₙ = u₀ + n r", "u indice n égale u zéro plus n fois r"),
         ("uₙ = 2 + 5n", "u indice n égale deux plus cinq n"),
         ("u₈ = 2 + 5 × 8 = 42", "u huit égale deux plus cinq fois huit")],
         "السؤال un. la suite arithmétique، la raison ديالها cinq. إذن u indice n égale u zéro plus n fois r. يعني u indice n égale deux plus cinq n. ونعوضو n ب huit: u huit égale deux plus cinq fois huit، égale quarante-deux."),
     "explication": "ex_1", "facile": "fa_1"},
    {"id": "2", "texte": "Calculer la somme S = u₀ + u₁ + … + u₈.",
     "texte_dit": "السؤال deux: حسب la somme S، égale u zéro plus u un، حتى ل u huit.",
     "reponse": valeur("S", 198, "S = (nombre de termes) × (u₀ + u₈)/2 = 9 × (2 + 42)/2 = 198"),
     "clavier": {"aides": ["nombre de termes", "8 − 0 + 1 = 9", "(u₀ + u₈)/2", "S ="], "pieges": ["8 termes", "8 × (2 + 42)/2"]},
     "aides": [aide("Compte d'abord les termes de u₀ à u₈ : dernier indice − premier indice + 1.",
                    "حسب الأول شحال من terme كاين من u zéro حتى ل u huit: le dernier indice moins le premier indice، plus un."),
               aide("Somme d'une suite arithmétique : S = (nombre de termes) × (premier terme + dernier terme)/2.",
                    "la somme ديال suite arithmétique: le nombre de termes، fois، le premier terme plus le dernier terme، sur deux.")],
     "correction": correction([
         ("2 : de u₀ à u₈ : 8 − 0 + 1 = 9 termes", "neuf termes"),
         ("S = 9 × (u₀ + u₈)/2", "S égale neuf fois"),
         ("S = 9 × (2 + 42)/2 = 9 × 22 = 198", "égale cent quatre-vingt-dix-huit")],
         "السؤال deux. من u zéro حتى ل u huit: huit moins zéro plus un، يعني neuf termes، ماشي huit. S égale neuf fois، u zéro plus u huit، sur deux. يعني neuf fois، deux plus quarante-deux، sur deux، يعني neuf fois vingt-deux، égale cent quatre-vingt-dix-huit."),
     "explication": "ex_2", "facile": "fa_2"},
    {"id": "3", "texte": "Exprimer vₙ en fonction de n, puis calculer v₅.",
     "texte_dit": "السؤال trois: عبر على v indice n en fonction de n، ومن بعد حسب v cinq.",
     "reponse": valeur("v₅", 96, "vₙ = v₀ × qⁿ = 3 × 2ⁿ ; v₅ = 3 × 2⁵ = 3 × 32 = 96"),
     "clavier": {"aides": ["vₙ = v₀ × qⁿ", "3 × 2ⁿ", "2⁵ = 32", "v₅ ="], "pieges": ["vₙ = v₀ + n q", "3 × 2⁴", "6⁵"]},
     "aides": [aide("Pour une suite géométrique, chaque pas multiplie par q : de v₀ à v₅, combien de fois multiplie-t-on par 2 ?",
                    "فsuite géométrique، كل خطوة كنضربو فq. من v zéro حتى ل v cinq، شحال من مرة كنضربو فdeux؟"),
               aide("Formule : vₙ = v₀ × qⁿ, avec v₀ = 3 et q = 2. Attention : 3 × 2⁵ n'est pas 6⁵.",
                    "la formule: v indice n égale v zéro fois q puissance n. v zéro égale trois، وq égale deux. رد البال: trois fois deux puissance cinq، ماشي six puissance cinq.")],
     "correction": correction([
         ("3 : (vₙ) géométrique de raison q = 2 : vₙ = v₀ × qⁿ", "v indice n égale v zéro fois q puissance n"),
         ("vₙ = 3 × 2ⁿ", "v indice n égale trois fois deux puissance n"),
         ("v₅ = 3 × 2⁵ = 3 × 32 = 96", "égale quatre-vingt-seize")],
         "السؤال trois. la suite géométrique، la raison ديالها deux. إذن v indice n égale v zéro fois q puissance n. يعني v indice n égale trois fois deux puissance n. v cinq égale trois fois deux puissance cinq، يعني trois fois trente-deux، égale quatre-vingt-seize."),
     "explication": "ex_3", "facile": "fa_3"},
    {"id": "4", "texte": "Calculer la somme T = v₀ + v₁ + … + v₅.",
     "texte_dit": "السؤال quatre: حسب la somme T، égale v zéro plus v un، حتى ل v cinq.",
     "reponse": valeur("T", 189, "T = v₀ × (1 − q⁶)/(1 − q) = 3 × (1 − 2⁶)/(1 − 2) = 3 × 63 = 189"),
     "clavier": {"aides": ["5 − 0 + 1 = 6 termes", "(1 − q⁶)/(1 − q)", "2⁶ = 64", "T ="], "pieges": ["(1 − q⁵)/(1 − q)", "(1 − 2⁶)/(1 + 2)"]},
     "aides": [aide("Compte les termes de v₀ à v₅ : ce nombre sera la puissance de q dans la formule.",
                    "حسب شحال من terme من v zéro حتى ل v cinq. هاد العدد هو la puissance ديال q فla formule."),
               aide("Somme géométrique (q ≠ 1) : T = premier terme × (1 − q^(nombre de termes))/(1 − q).",
                    "la somme géométrique: le premier terme، fois، un moins q puissance le nombre de termes، sur un moins q.")],
     "correction": correction([
         ("4 : de v₀ à v₅ : 5 − 0 + 1 = 6 termes", "six termes"),
         ("T = v₀ × (1 − q⁶)/(1 − q)", "un moins q puissance six"),
         ("T = 3 × (1 − 64)/(1 − 2) = 3 × 63 = 189", "égale cent quatre-vingt-neuf")],
         "السؤال quatre. من v zéro حتى ل v cinq: cinq moins zéro plus un، يعني six termes. T égale v zéro fois، un moins q puissance six، sur un moins q. يعني trois fois، un moins soixante-quatre، sur un moins deux. moins soixante-trois sur moins un، كتعطي soixante-trois. إذن T égale trois fois soixante-trois، égale cent quatre-vingt-neuf."),
     "explication": "ex_4", "facile": "fa_4"},
]

EXPLICATION = deck("explication", "Explication animée", [
    sim("ex_1", "Question 1 : huit sauts de + 5", "De u₀ à u₈ : 8 sauts de + 5, donc u₈ = 2 + 5 × 8.",
        S + "sauts.html?vue=arith", "Le caillou saute de case en case : chaque saut ajoute r",
        "شوف هاد الخانات: u zéro، u un، حتى ل u huit. كل قفزة كتزيد la raison r. من u zéro حتى ل u n، كاينين n قفزات. إذن u indice n égale u zéro plus n fois r. دابا l'exemple ديالنا: u zéro égale deux، وr égale cinq. من u zéro حتى ل u huit، huit قفزات ديال plus cinq. u huit égale deux plus cinq fois huit، égale quarante-deux.",
        [("uₙ = u₀ + n r", "إذن u indice n égale u zéro plus n fois r"), ("u₈ = 2 + 5 × 8 = 42", "u huit égale deux plus cinq fois huit")],
        [regle("شوف هاد الخانات", n=8, r=5), jusqua("شوف هاد الخانات", "cases"),
         jusqua("كل قفزة كتزيد la raison r", "formule"), jusqua("كاينين n قفزات", "p_zero"),
         montre("إذن u indice n égale u zéro plus n fois r", "centre:0"),
         jusqua("دابا l'exemple ديالنا", "exemple"), montre("u huit égale deux plus cinq fois huit", "centre:1")]),
    sim("ex_2", "Question 2 : compter les termes avant d'additionner", "De u₀ à u₈ : 8 − 0 + 1 = 9 termes, pas 8.",
        S + "arbres.html?vue=arbres", "Des arbres numérotés 5, 6, 7 : combien d'arbres ?",
        "قبل ما نجمعو، خاصنا نحسبو الحدود. شوف هاد الشجرات: الرقم cinq، الرقم six، الرقم sept. شحال من شجرة؟ trois، ماشي deux. sept moins cinq plus un، égale trois. القاعدة: من u p حتى ل u n، كاين n moins p plus un termes. عندنا من u zéro حتى ل u huit: huit moins zéro plus un، يعني neuf termes. ومن بعد la somme ديال suite arithmétique: le nombre de termes، fois، le premier plus le dernier، sur deux. S égale neuf fois، deux plus quarante-deux، sur deux، égale cent quatre-vingt-dix-huit.",
        [("n − p + 1 termes", "القاعدة"), ("8 − 0 + 1 = 9 termes", "يعني neuf termes"), ("S = 9 × (2 + 42)/2 = 198", "S égale neuf fois")],
        [jusqua("شوف هاد الشجرات", "arbres"), jusqua("شحال من شجرة؟", "arbre_3"), jusqua("sept moins cinq plus un", "compte"),
         jusqua("القاعدة", "regle"), montre("القاعدة", "centre:0"), montre("يعني neuf termes", "centre:1"),
         montre("S égale neuf fois", "centre:2")]),
    sim("ex_3", "Question 3 : cinq sauts de × 2", "De v₀ à v₅ : 5 sauts de × q, donc v₅ = v₀ × q⁵ = 3 × 2⁵.",
        S + "sauts.html?vue=geo", "Chaque saut multiplie par q",
        "هاد المرة كل قفزة كتضرب فq. هنا الخانات مكتوب فيها u، ولكن نفس الشي ل v. من الخانة zéro حتى ل الخانة n، كاينين n قفزات ديال fois q. إذن v indice n égale v zéro fois q puissance n. ملي n égale zéro، ماكايناش قفزة: q puissance zéro égale un، ماشي zéro. عندنا v zéro égale trois، وq égale deux. v cinq égale trois fois deux puissance cinq، يعني trois fois trente-deux، égale quatre-vingt-seize.",
        [("vₙ = v₀ × qⁿ", "إذن v indice n égale v zéro fois q puissance n"), ("q⁰ = 1", "q puissance zéro égale un"),
         ("v₅ = 3 × 2⁵ = 96", "v cinq égale trois fois deux puissance cinq")],
        [regle("هاد المرة كل قفزة كتضرب فq", n=5), jusqua("هاد المرة كل قفزة كتضرب فq", "formule"),
         jusqua("كاينين n قفزات ديال fois q", "p_zero"), montre("إذن v indice n égale v zéro fois q puissance n", "centre:0"),
         jusqua("ملي n égale zéro", "q_zero"), montre("q puissance zéro égale un", "centre:1"),
         montre("v cinq égale trois fois deux puissance cinq", "centre:2")]),
    sim("ex_4", "Question 4 : la somme géométrique", "T = premier terme × (1 − q^N)/(1 − q), N = nombre de termes = 6.",
        S + "calculs.html?vue=a9", "Les deux formules de somme, au tableau",
        "شوف الطبلة. الفوق، la somme arithmétique: le nombre de termes، fois، le premier plus le dernier، sur deux. l'exemple ديال le cours: un plus deux حتى ل dix، égale cinquante-cinq. التحت، la somme géométrique: le premier terme، fois، un moins q puissance N، sur un moins q. وN هو le nombre de termes. عندنا من v zéro حتى ل v cinq، six termes، إذن N égale six. T égale trois fois، un moins deux puissance six، sur un moins deux. يعني trois fois، moins soixante-trois، sur moins un، égale cent quatre-vingt-neuf.",
        [("S = premier × (1 − q^N)/(1 − q)", "التحت، la somme géométrique"), ("N = 6", "إذن N égale six"),
         ("T = 3 × (1 − 64)/(1 − 2) = 189", "T égale trois fois")],
        [jusqua("الفوق، la somme arithmétique", "arith"), jusqua("l'exemple ديال le cours", "exemple_arith"),
         jusqua("التحت، la somme géométrique", "geo"), montre("التحت، la somme géométrique", "centre:0"),
         jusqua("وN هو le nombre de termes", "puissance"), montre("إذن N égale six", "centre:1"), montre("T égale trois fois", "centre:2")]),
])

FACILE = deck("facile", "Plus facile, pour s'entraîner", [
    qcm("fa_1", "Plus facile : le terme général", "نتمرنو بسؤال ساهل: اختار la bonne formule.",
        "(uₙ) arithmétique, u₀ = 2, r = 5. Que vaut uₙ ?", ["uₙ = 2 × 5ⁿ", "uₙ = 2 + 5n", "uₙ = 5 + 2n"], 1, [
            (("ما تقلقش. ضرب فcinq كل مرة، هادي suite géométrique. فsuite arithmétique كنزيدو la raison. عاود اختار.", "2 × 5ⁿ : c'est une suite géométrique. Réessaie."),
             ("الجواب هو u indice n égale deux plus cinq n: كنزيدو cinq، n مرات، على u zéro.", "Réponse : uₙ = u₀ + n r = 2 + 5n.")),
            ("برافو! u indice n égale u zéro plus n fois r، يعني deux plus cinq n.", "Juste : uₙ = u₀ + n r = 2 + 5n."),
            (("قريب! بدلتي u zéro وr. u zéro هو deux، وla raison هي cinq. عاود اختار.", "Tu as inversé u₀ et r. Réessaie."),
             ("الجواب هو deux plus cinq n: u zéro égale deux، وكل خطوة كتزيد cinq.", "Réponse : uₙ = 2 + 5n."))],
        "u indice n arithmétique، u zéro égale deux، r égale cinq. Que vaut u indice n ?"),
    association("fa_2", "Plus facile : combien de termes ?", "Relie chaque somme à son nombre de termes.",
        "سؤال ساهل: ربط كل somme مع le nombre de termes ديالها.",
        "Relie chaque somme à son nombre de termes.",
        [("1", "u₀ + u₁ + … + u₈"), ("2", "u₁ + u₂ + … + u₈"), ("3", "u₃ + u₄ + … + u₉")],
        [("a", "9 termes"), ("b", "8 termes"), ("c", "7 termes"), ("d", "10 termes")],
        {"1": "a", "2": "b", "3": "c"},
        {"1-a": ("Oui : 8 − 0 + 1 = 9.", "برافو: huit moins zéro plus un، égale neuf."),
         "1-b": ("8 − 0 = 8 oublie le +1 : u₀ compte aussi.", "لا، نسيتي plus un: حتى u zéro كيتحسب."),
         "1-c": ("Trop peu : compte dernier − premier + 1.", "لا، قليل بزاف. حسب le dernier moins le premier، plus un."),
         "1-d": ("Trop : de 0 à 8, ce n'est pas 10.", "لا، بزاف. من zéro حتى ل huit ماشي dix."),
         "2-a": ("Ici on commence à u₁, pas à u₀.", "لا، هنا كنبداو من u un، ماشي من u zéro."),
         "2-b": ("Oui : 8 − 1 + 1 = 8.", "برافو: huit moins un plus un، égale huit."),
         "2-c": ("8 − 1 = 7 oublie le +1.", "لا، نسيتي plus un."),
         "2-d": ("Trop : compte dernier − premier + 1.", "لا، بزاف. حسب le dernier moins le premier، plus un."),
         "3-a": ("Trop : on commence à u₃, pas à u₀.", "لا، هنا كنبداو من u trois، ماشي من u zéro."),
         "3-b": ("Trop : refais 9 − 3 + 1.", "لا، بزاف. عاود حسب neuf moins trois plus un."),
         "3-c": ("Oui : 9 − 3 + 1 = 7.", "برافو: neuf moins trois plus un، égale sept."),
         "3-d": ("Trop : de u₃ à u₉, refais 9 − 3 + 1.", "لا، بزاف. عاود حسب neuf moins trois plus un.")},
        ("(1 ; a) (2 ; b) (3 ; c) : nombre de termes = dernier indice − premier indice + 1.",
         "القاعدة: le nombre de termes، égale le dernier indice moins le premier indice، plus un.")),
    vrai_faux("fa_3", "Plus facile : vrai ou faux", "(vₙ) géométrique, v₀ = 3, q = 2.",
        "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
            ("vₙ = 3 × 2ⁿ.", True, "vₙ = v₀ × qⁿ avec v₀ = 3 et q = 2."),
            ("v₅ = 6⁵, car 3 × 2 = 6.", False, "On multiplie 3 par 2⁵ : la puissance porte seulement sur 2. v₅ = 3 × 32 = 96."),
            ("v₀ = 3 × 2⁰ = 0.", False, "2⁰ = 1, donc v₀ = 3 × 1 = 3.")]),
    qcm("fa_4", "Plus facile : la puissance dans la somme", "سؤال ساهل على la somme géométrique.",
        "T = v₀ + … + v₅ = 3 × (1 − 2^N)/(1 − 2). Que vaut N ?", ["N = 5", "N = 4", "N = 6"], 2, [
            (("قريب! cinq هو le dernier indice، ولكن N هو le nombre de termes. من zéro حتى ل cinq، شحال؟ عاود اختار.", "5 est le dernier indice ; N est le nombre de termes. Réessaie."),
             ("الجواب هو N égale six: cinq moins zéro plus un، six termes.", "Réponse : N = 5 − 0 + 1 = 6.")),
            (("ما تقلقش. حسب الحدود من v zéro حتى ل v cinq: le dernier moins le premier، plus un. عاود اختار.", "Compte dernier − premier + 1. Réessaie."),
             ("الجواب هو N égale six، le nombre de termes.", "Réponse : N = 6.")),
            ("برافو! من v zéro حتى ل v cinq، six termes، إذن N égale six.", "Juste : 6 termes, donc N = 6.")],
        "T égale trois fois، un moins deux puissance N، sur un moins deux. Que vaut N ?"),
])

ENONCE = {
    "intro": "On considère la suite arithmétique (uₙ) de premier terme u₀ = 2 et de raison r = 5, et la suite géométrique (vₙ) de premier terme v₀ = 3 et de raison q = 2.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا deux suites. الأولى u indice n، arithmétique: u zéro égale deux، وla raison r égale cinq. الثانية v indice n، géométrique: v zéro égale trois، وla raison q égale deux.",
    "figures": [{"type": "schema", "titre": "Une suite arithmétique : on ajoute r ; une suite géométrique : on multiplie par q",
                 "cadre": {"l": 10, "h": 4},
                 "legende": "De u₀ à uₙ : n sauts de + 5 ; de v₀ à vₙ : n sauts de × 2.",
                 "elements": [{"f": "texte", "at": [0.3, 3.3], "t": "u₀ = 2", "couleur": "cyan"},
                              {"f": "fleche", "de": [1.8, 3.4], "a": [3.2, 3.4], "couleur": "vert", "texte": "+ 5", "pos": "n"},
                              {"f": "texte", "at": [3.4, 3.3], "t": "u₁ = 7", "couleur": "cyan"},
                              {"f": "fleche", "de": [4.9, 3.4], "a": [6.3, 3.4], "couleur": "vert", "texte": "+ 5", "pos": "n"},
                              {"f": "texte", "at": [6.5, 3.3], "t": "u₂ = 12   …", "couleur": "cyan"},
                              {"f": "texte", "at": [0.3, 1.0], "t": "v₀ = 3", "couleur": "jaune"},
                              {"f": "fleche", "de": [1.8, 1.1], "a": [3.2, 1.1], "couleur": "orange", "texte": "× 2", "pos": "n"},
                              {"f": "texte", "at": [3.4, 1.0], "t": "v₁ = 6", "couleur": "jaune"},
                              {"f": "fleche", "de": [4.9, 1.1], "a": [6.3, 1.1], "couleur": "orange", "texte": "× 2", "pos": "n"},
                              {"f": "texte", "at": [6.5, 1.0], "t": "v₂ = 12   …", "couleur": "jaune"}]}],
    "donnees": ["(uₙ) arithmétique : u₀ = 2, r = 5", "(vₙ) géométrique : v₀ = 3, q = 2"],
    "questions": QUESTIONS,
}

SIMILAIRE = {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
        "intro": "On considère la suite arithmétique (uₙ) de premier terme u₀ = 1 et de raison r = 4, et la suite géométrique (vₙ) de premier terme v₀ = 2 et de raison q = 3.",
        "intro_dit": "نفس التمرين، بأرقام أخرى. u indice n arithmétique: u zéro égale un، وr égale quatre. v indice n géométrique: v zéro égale deux، وq égale trois.",
        "donnees": ["(uₙ) arithmétique : u₀ = 1, r = 4", "(vₙ) géométrique : v₀ = 2, q = 3"],
        "questions": [
            {"id": "1", "texte": "Exprimer uₙ en fonction de n, puis calculer u₈.",
             "reponse": valeur("u₈", 33, "uₙ = 1 + 4n ; u₈ = 1 + 4 × 8 = 33"),
             "clavier": {"aides": ["uₙ = u₀ + n r", "u₈ ="], "pieges": ["u₈ = 1 + 4 × 7"]},
             "correction": correction([("1 : uₙ = u₀ + n r = 1 + 4n", "u indice n égale un plus quatre n"), ("u₈ = 1 + 4 × 8 = 33", "u huit égale")],
                                      "u indice n égale u zéro plus n fois r، يعني u indice n égale un plus quatre n. u huit égale un plus quatre fois huit، égale trente-trois.")},
            {"id": "2", "texte": "Calculer la somme S = u₀ + u₁ + … + u₈.",
             "reponse": valeur("S", 153, "S = 9 × (1 + 33)/2 = 9 × 17 = 153"),
             "clavier": {"aides": ["9 termes", "(u₀ + u₈)/2"], "pieges": ["8 termes"]},
             "correction": correction([("2 : de u₀ à u₈ : 9 termes", "neuf termes"), ("S = 9 × (1 + 33)/2 = 153", "S égale neuf fois")],
                                      "من u zéro حتى ل u huit، neuf termes. S égale neuf fois، un plus trente-trois، sur deux، يعني neuf fois dix-sept، égale cent cinquante-trois.")},
            {"id": "3", "texte": "Exprimer vₙ en fonction de n, puis calculer v₅.",
             "reponse": valeur("v₅", 486, "vₙ = 2 × 3ⁿ ; v₅ = 2 × 3⁵ = 2 × 243 = 486"),
             "clavier": {"aides": ["vₙ = v₀ × qⁿ", "3⁵ = 243"], "pieges": ["6⁵"]},
             "correction": correction([("3 : vₙ = v₀ × qⁿ = 2 × 3ⁿ", "v indice n égale deux fois trois puissance n"), ("v₅ = 2 × 243 = 486", "égale quatre cent quatre-vingt-six")],
                                      "v indice n égale v zéro fois q puissance n، يعني v indice n égale deux fois trois puissance n. v cinq égale deux fois deux cent quarante-trois، égale quatre cent quatre-vingt-six.")},
            {"id": "4", "texte": "Calculer la somme T = v₀ + v₁ + … + v₅.",
             "reponse": valeur("T", 728, "T = 2 × (1 − 3⁶)/(1 − 3) = 2 × (−728)/(−2) = 728"),
             "clavier": {"aides": ["6 termes", "(1 − q⁶)/(1 − q)", "3⁶ = 729"], "pieges": ["(1 − q⁵)/(1 − q)"]},
             "correction": correction([("4 : 6 termes : T = v₀ × (1 − q⁶)/(1 − q)", "six termes"), ("T = 2 × (1 − 729)/(1 − 3) = 728", "égale sept cent vingt-huit")],
                                      "من v zéro حتى ل v cinq، six termes. T égale deux fois، un moins sept cent vingt-neuf، sur un moins trois. يعني deux fois trois cent soixante-quatre، égale sept cent vingt-huit.")},
        ]}}

EX = {"id": ID, "type": "exercice", "version": 1, "status": "published", "matiere": "mathematiques",
      "chapitre": "suites_definition", "cours": "math_ch3_suites_numeriques",
      "titre": "Suite arithmétique et suite géométrique : terme général et sommes", "niveau": "facile", "duree_min": 15,
      "origine": ORIGINE,
      "competences": ["Exprimer le terme général d'une suite arithmétique ou géométrique", "Compter les termes d'une somme",
                      "Calculer une somme de termes consécutifs"],
      "enonce": ENONCE, "explication": EXPLICATION, "facile": FACILE, "similaire": SIMILAIRE}

if __name__ == "__main__":
    ecrire(EX)
