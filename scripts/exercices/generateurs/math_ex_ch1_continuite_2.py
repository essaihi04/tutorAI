# Exercice de maths (ch. 1, limites et continuité) — niveau FACILE (s'entraîner) : limites à l'infini et asymptote.
# Sources comparées (lues, rien de copié) :
#  - exploration limites_continuite.json : cas_types fi_infini / fi_conjugue, pièges « √(x²) = x », « forme indéterminée
#    sans indétermination », erreurs_examen « interpréter géométriquement » (la demi-phrase vaut la moitié des points) ;
#  - vidéos des profs (Driss DOTCOM, Chadyyy contrôle complet PhSC-Ghwt1g, Rabie Ghazouani) : quotient de polynômes à
#    l'infini, conjugué √(x² + ax) − x, règle des signes pour un polynôme en −∞ ;
#  - nationaux 2016-2025 (backend/data/exams/mathematiques/*) : 20 sujets sur 20 demandent une limite aux bornes puis
#    « interpréter géométriquement » (avec ln et exp : ici les mêmes gestes sur des polynômes et une racine) ;
#  - séries en ligne (recherche, lecture des sommaires ; domaines non joignables depuis la session pour une lecture
#    complète) : Talamidi « limites et continuité série 1 » et « série 2 » (2Bac PC BIOF), Moutamadris « résumé limites
#    et continuité 2bac PC/SVT », Alloschool « limite et continuité cours » et fiche Cheddadi, Pr. Haddad (sigmaths,
#    2 BAC PC & SVT) : limites en ±∞ de quotients et de √(x² + …) − x, asymptotes horizontales.
import sys
from _commun import *

ID = "math_ex_ch1_continuite_2"
LOURD = "/media/simulations/maths/limites-continuite-tableau/lourd.html?vue=lourd"
HORIZ = "/media/simulations/maths/limites-continuite-tableau/infini.html?vue=horizontale"
REGLES = "/media/simulations/maths/limites-continuite-tableau/etapes.html?vue=regles"
ECART = "/media/simulations/maths/limites-continuite-tableau/infini.html?vue=ecart"


def figure(expr, nom, ymin, ymax, gy):
    return {"type": "courbe", "titre": f"La courbe de {nom} sur [0 ; 12]",
            "axes": {"x": {"min": -0.5, "max": 12, "nom": "x", "graduations": [0, 2, 4, 6, 8, 10, 12]},
                     "y": {"min": ymin, "max": ymax, "nom": "y", "graduations": gy}},
            "legende": f"La courbe de {nom} quand x grandit : que devient-elle ?",
            "elements": [{"f": "courbe", "expr": expr, "de": 0, "a": 12, "couleur": "cyan", "texte": f"(C_{nom[0]})", "texte_x": 10, "pos": "no"}]}


EX = {
  "id": ID, "type": "exercice", "version": 1, "status": "published",
  "matiere": "mathematiques", "chapitre": "limites_continuite", "cours": "math_ch1_limites_continuite",
  "titre": "Trois limites à l'infini et une asymptote", "niveau": "facile", "duree_min": 15,
  "origine": ORIGINE,
  "competences": ["Calculer la limite d'un quotient de polynômes à l'infini", "Interpréter géométriquement une limite finie à l'infini",
                  "Calculer la limite d'un polynôme à l'infini", "Lever « +∞ − ∞ » avec l'expression conjuguée"],
  "enonce": {
    "intro": "On considère les fonctions f, g et h définies par : f(x) = (2x² − 3)/(x² + 1) sur ℝ ; g(x) = −x³ + 4x² + 1 sur ℝ ; h(x) = √(x² + 4x) − x sur [0 ; +∞[. (C_f) est la courbe de f dans un repère orthonormé.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا ثلاث fonctions. f de x égale، deux x carré moins trois، sur، x carré plus un. g de x égale moins x cube، plus quatre x carré، plus un. وh de x égale، racine carrée de، x carré plus quatre x، moins x، على l'intervalle من zéro حتى plus l'infini.",
    "figures": [figure("(2*x^2-3)/(x^2+1)", "f", -3.5, 3, [-3, -2, -1, 0, 1, 2])],
    "donnees": ["f(x) = (2x² − 3)/(x² + 1), x ∈ ℝ", "g(x) = −x³ + 4x² + 1, x ∈ ℝ", "h(x) = √(x² + 4x) − x, x ∈ [0 ; +∞["],
    "questions": [
      {"id": "1", "texte": "Calculer la limite de f(x) quand x tend vers +∞.",
       "texte_dit": "السؤال un: حسب la limite ديال f de x، quand x tend vers plus l'infini.",
       "reponse": valeur("lim f(x)", 2, "en +∞ : « ∞/∞ » ; lim f(x) = lim 2x²/x² = 2"),
       "clavier": {"aides": ["lim", "x → +∞", "2x²/x²", "plus haut degré", "="], "pieges": ["−3/1 = −3", "∞/∞ = 1"]},
       "aides": [aide("En remplaçant, le haut et le bas tendent vers +∞ : c'est « ∞/∞ », une forme indéterminée.",
                      "ملي كنعوضو، الفوق كيمشي ل plus l'infini، والتحت حتى هو. هادي l'infini sur l'infini، forme indéterminée."),
                 aide("À l'infini, on garde le terme de plus haut degré en haut et en bas : 2x² et x².",
                      "فl'infini، كنخليو غير le terme de plus haut degré، فالفوق deux x carré، وفالتحت x carré.")],
       "correction": correction([("1 : en +∞, « ∞/∞ » : forme indéterminée", "forme indéterminée"),
                                 ("lim f(x) = lim 2x²/x²  (x → +∞)", "le terme de plus haut degré"),
                                 ("lim f(x) = 2", "la limite égale deux")],
         "السؤال un. ملي x tend vers plus l'infini، كنلقاو l'infini sur l'infini: forme indéterminée. فl'infini، كنخليو le terme de plus haut degré: deux x carré، sur، x carré. كنبسطو x carré، إذن la limite égale deux."),
       "explication": "ex_1", "facile": "fa_1"},
      {"id": "2", "texte": "Interpréter géométriquement le résultat de la question 1.",
       "texte_dit": "السؤال deux: interpréter géométriquement le résultat ديال السؤال un.",
       "reponse": phrase("lim f(x) = 2 quand x → +∞, donc la droite d'équation y = 2 est une asymptote horizontale à (C_f) au voisinage de +∞."),
       "clavier": {"aides": ["la droite d'équation y = 2", "asymptote horizontale", "à (C_f)", "au voisinage de +∞"], "pieges": ["x = 2", "asymptote verticale"]},
       "aides": [aide("Une limite FINIE quand x tend vers l'infini donne une droite horizontale : laquelle ?",
                      "واحد la limite finie، ملي x tend vers l'infini، كتعطي droite horizontale. شمن droite؟"),
                 aide("La droite horizontale à la hauteur ℓ a pour équation y = ℓ (et non x = ℓ).",
                      "la droite horizontale اللي فالعلو ديال la limite، l'équation ديالها y égale la limite، ماشي x.")],
       "correction": correction([("2 : lim f(x) = 2 quand x → +∞", "la limite égale deux"),
                                 ("donc la droite d'équation y = 2 est une asymptote horizontale à (C_f) au voisinage de +∞", "asymptote horizontale")],
         "السؤال deux. la limite égale deux، quand x tend vers plus l'infini. إذن la droite d'équation y égale deux، est une asymptote horizontale à la courbe، au voisinage de plus l'infini."),
       "explication": "ex_2", "facile": "fa_2"},
      {"id": "3", "texte": "Calculer la limite de g(x) quand x tend vers −∞.",
       "texte_dit": "السؤال trois: حسب la limite ديال g de x، quand x tend vers moins l'infini.",
       "reponse": phrase("lim g(x) = lim −x³ = +∞ quand x → −∞ (terme de plus haut degré ; x³ → −∞ et −(−∞) = +∞)."),
       "clavier": {"aides": ["lim", "x → −∞", "−x³", "+∞"], "pieges": ["−∞", "+∞ − ∞"]},
       "aides": [aide("Pour un polynôme à l'infini, seul le terme de plus haut degré compte : ici −x³.",
                      "فl'infini، le polynôme عندو la limite ديال le terme de plus haut degré. هنا هو moins x cube."),
                 aide("Quand x tend vers −∞, x³ tend vers −∞. Et le signe moins devant ?",
                      "ملي x tend vers moins l'infini، x cube كيمشي ل moins l'infini. وشنو كيدير le signe moins اللي قدامو؟")],
       "correction": correction([("3 : lim g(x) = lim −x³  (x → −∞)", "le terme de plus haut degré"),
                                 ("x³ → −∞, donc −x³ → +∞", "x cube كيمشي ل moins l'infini"),
                                 ("lim g(x) = +∞", "la limite égale plus l'infini")],
         "السؤال trois. فl'infini، كنخليو le terme de plus haut degré: moins x cube. ملي x tend vers moins l'infini، x cube كيمشي ل moins l'infini، والsigne moins كيقلبو. إذن la limite égale plus l'infini."),
       "explication": "ex_3", "facile": "fa_3"},
      {"id": "4", "texte": "Calculer la limite de h(x) quand x tend vers +∞.",
       "texte_dit": "السؤال quatre: حسب la limite ديال h de x، quand x tend vers plus l'infini.",
       "reponse": valeur("lim h(x)", 2, "h(x) = 4x/(√(x² + 4x) + x) = 4/(√(1 + 4/x) + 1) pour x > 0 ; lim h(x) = 4/(1 + 1) = 2"),
       "clavier": {"aides": ["√(x² + 4x) + x", "(a − b)(a + b) = a² − b²", "4x", "√(1 + 4/x)", "="], "pieges": ["+∞ − ∞ = 0", "√(x² + 4x) = x + 2"]},
       "aides": [aide("En remplaçant, on trouve « +∞ − ∞ » : forme indéterminée. Multiplie haut et bas par l'expression conjuguée √(x² + 4x) + x.",
                      "ملي كنعوضو كنلقاو plus l'infini moins l'infini: forme indéterminée. ضرب الفوق والتحت فl'expression conjuguée: racine carrée de، x carré plus quatre x، plus x."),
                 aide("(a − b)(a + b) = a² − b² donne en haut x² + 4x − x² = 4x ; puis mets x en facteur en bas (x > 0).",
                      "a moins b، fois، a plus b، égale a carré moins b carré. فالفوق كيبقى quatre x. ومن بعد خرج x facteur فالتحت، حيت x positif.")],
       "correction": correction([("4 : en +∞, « +∞ − ∞ » : forme indéterminée", "forme indéterminée"),
                                 ("h(x) = (x² + 4x − x²)/(√(x² + 4x) + x) = 4x/(√(x² + 4x) + x)", "l'expression conjuguée"),
                                 ("pour x > 0 : h(x) = 4/(√(1 + 4/x) + 1)", "خرجنا x facteur"),
                                 ("lim h(x) = 4/(1 + 1) = 2", "la limite égale deux")],
         "السؤال quatre. ملي كنعوضو كنلقاو plus l'infini moins l'infini: forme indéterminée. كنضربو الفوق والتحت فl'expression conjuguée، فالفوق كيبقى quatre x. خرجنا x facteur فالتحت: h de x égale quatre، sur، racine carrée de، un plus quatre sur x، plus un. quatre sur x كيمشي ل zéro، إذن la limite égale quatre sur deux، يعني la limite égale deux."),
       "explication": "ex_4", "facile": "fa_4"}
    ]
  },
  "explication": deck("explication", "Explication animée", [
    sim("ex_1", "Question 1 : à l'infini, le terme le plus lourd", "À l'infini, un quotient de polynômes a la limite du quotient des termes de plus haut degré.",
        LOURD, "Le terme le plus lourd écrase les autres",
        "نشوفو la méthode على هاد l'exemple: trois x carré plus un، sur، x carré moins x. ملي x tend vers plus l'infini، كنلقاو l'infini sur l'infini: forme indéterminée. دابا x كيكبر. شوف الفوق: trois x carré كياكل كلشي، وun ما كيبان والو. والتحت: x carré كياكل x. كيبقى غير trois x carré sur x carré، يعني trois. فالتمرين ديالنا نفس الشي: deux x carré sur x carré، إذن la limite égale deux. رد بالك: هاد القاعدة غير فl'infini.",
        [("lim (3x² + 1)/(x² − x) = 3", "يعني trois"), ("lim (2x² − 3)/(x² + 1) = lim 2x²/x² = 2", "إذن la limite égale deux")],
        [jusqua("كنلقاو l'infini sur l'infini", "infini_infini"), jusqua("دابا x كيكبر", "croissance"),
         jusqua("كيبقى غير trois x carré", "lourds"), jusqua("يعني trois", "resultat"), montre("يعني trois", "centre:0"),
         montre("إذن la limite égale deux", "centre:1"), jusqua("رد بالك", "attention")]),
    sim("ex_2", "Question 2 : une limite finie à l'infini, une asymptote horizontale", "lim f(x) = ℓ en +∞ : la droite d'équation y = ℓ est une asymptote horizontale.",
        HORIZ, "La courbe longe la droite horizontale",
        "شوف la courbe ديال، deux x plus un، sur، x plus un. ملي x كيكبر بزاف، كتمشي حدا la droite y égale deux، بلا ما توصل ليها. la limite en plus l'infini égale deux. كنكتبو: la droite d'équation y égale deux، est une asymptote horizontale à la courbe، en plus l'infini. فالتمرين ديالنا حتى هي la limite égale deux، إذن نفس الجملة. رد بالك: y égale deux، ماشي x égale deux.",
        [("y = 2 : asymptote horizontale à (C_f) en +∞", "est une asymptote horizontale")],
        [jusqua("شوف la courbe", "courbe_tracee"), jusqua("كتمشي حدا la droite", "droite_horizontale"),
         jusqua("كنكتبو", "interpretation"), montre("est une asymptote horizontale", "centre:0")]),
    sim("ex_3", "Question 3 : un polynôme en moins l'infini", "Polynôme à l'infini : le terme de plus haut degré, puis la règle des signes.",
        REGLES, "Ce qui n'est pas indéterminé",
        "هادو les règles اللي ماشي forme indéterminée. plus l'infini plus plus l'infini، كتعطي plus l'infini. والproduit: moins l'infini، fois، moins l'infini، كيعطي plus l'infini، بla règle des signes. فالتمرين: g de x عندها la limite ديال moins x cube. x cube كيمشي ل moins l'infini، وle signe moins كيقلبو، إذن la limite égale plus l'infini.",
        [("lim g(x) = lim −x³ = +∞ (x → −∞)", "إذن la limite égale plus l'infini")],
        [jusqua("هادو les règles", "titre"), jusqua("plus l'infini plus plus l'infini", "somme"),
         jusqua("والproduit", "produit"), montre("إذن la limite égale plus l'infini", "centre:0")]),
    sim("ex_4", "Question 4 : plus l'infini moins l'infini, l'expression conjuguée", "√(x² + ax) − x en +∞ : l'écart se stabilise ; on le calcule avec le conjugué.",
        ECART, "L'écart entre la racine et x",
        "نشوفو la méthode على هاد l'exemple: racine carrée de، x carré plus x، moins x. شوف الجوج courbes: كيمشيو بحال بحال. فx égale dix، l'écart قريب من zéro virgule quatre huit huit. وفx égale cent، l'écart قريب من zéro virgule quatre neuf neuf. l'écart ما كيكبرش، كيقرب ل un demi. هادي forme indéterminée اللي كتفكها l'expression conjuguée. فالتمرين ديالنا، كنلقاو quatre x فالفوق، ومن بعد la limite égale deux.",
        [("(a − b)(a + b) = a² − b²", "l'expression conjuguée"), ("lim (√(x² + 4x) − x) = 2", "la limite égale deux")],
        [jusqua("شوف الجوج courbes", "deux_courbes"), jusqua("فx égale dix", "ecart_x10"),
         jusqua("وفx égale cent", "ecart_x100"), jusqua("كيقرب ل un demi", "ecart_lu"),
         montre("l'expression conjuguée", "centre:0"), montre("la limite égale deux", "centre:1")]),
  ]),
  "facile": deck("facile", "Plus facile, pour s'entraîner", [
    qcm("fa_1", "Plus facile : le terme de plus haut degré", "نتمرنو بسؤال ساهل: شنو هي la limite؟",
        "lim (5x² + 1)/(x² − 2) quand x → +∞ vaut :", ["1", "5", "−1/2"], 1, [
          (("لا. l'infini sur l'infini ماشي un. شوف le terme de plus haut degré فالفوق وفالتحت. عاود اختار.", "∞/∞ n'est pas 1 : regarde les termes de plus haut degré."),
           ("الجواب هو cinq: cinq x carré sur x carré égale cinq.", "Réponse : 5, car 5x²/x² = 5.")),
          ("برافو! فl'infini كنخليو cinq x carré sur x carré، يعني cinq.", "Juste : lim = lim 5x²/x² = 5."),
          (("قريب، ولكن un sur moins deux هو اللي كيعطينا x égale zéro. فl'infini ماشي كنعوضو. عاود اختار.", "1/(−2), c'est la valeur en 0, pas à l'infini. Réessaie."),
           ("الجواب هو cinq: فl'infini كنخليو le terme de plus haut degré، cinq x carré sur x carré.", "Réponse : 5."))],
        "La limite de cinq x carré plus un, sur x carré moins deux, quand x tend vers plus l'infini, vaut ?"),
    association("fa_2", "Plus facile : associer la limite et la droite", "Relie chaque limite à son interprétation.",
        "سؤال ساهل: ربط كل limite مع la droite ديالها.", "Relie chaque limite à son interprétation géométrique.",
        [("1", "lim f(x) = 2 quand x → +∞"), ("2", "lim f(x) = +∞ quand x → 2⁺")],
        [("a", "y = 2 asymptote horizontale"), ("b", "x = 2 asymptote verticale"), ("c", "pas d'asymptote")],
        {"1": "a", "2": "b"},
        {"1-a": ("Oui : limite finie à l'infini → droite horizontale y = 2.", "برافو: la limite finie فl'infini، كتعطي la droite horizontale y égale deux."),
         "1-b": ("Non : x = 2 est verticale ; ici x part à l'infini et f(x) reste près de 2.", "لا، x égale deux droite verticale. هنا x كيمشي ل l'infini، وf de x قريبة من deux."),
         "1-c": ("Non : une limite finie à l'infini donne bien une asymptote.", "لا، la limite finie فl'infini كتعطي asymptote."),
         "2-a": ("Non : ici c'est x qui s'approche de 2, et f(x) part à l'infini.", "لا، هنا x هو اللي كيقرب ل deux، وf de x كتمشي ل l'infini."),
         "2-b": ("Oui : limite infinie en 2 → droite verticale x = 2.", "برافو: la limite infinie فdeux، كتعطي la droite verticale x égale deux."),
         "2-c": ("Non : une limite infinie en un réel donne une asymptote verticale.", "لا، la limite infinie فواحد le réel كتعطي asymptote verticale.")},
        ("(1 ; a) (2 ; b) : limite finie à l'infini → horizontale ; limite infinie en un réel → verticale.",
         "la limite finie فl'infini كتعطي horizontale. la limite infinie فواحد le réel كتعطي verticale.")),
    vrai_faux("fa_3", "Plus facile : vrai ou faux", "x tend vers −∞.", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
        ("Quand x → −∞, x³ → −∞.", True, "Un nombre négatif au cube reste négatif : (−10)³ = −1000."),
        ("Quand x → −∞, −x³ → −∞.", False, "Le signe moins change −∞ en +∞ : −x³ → +∞."),
        ("lim (−x³ + 4x² + 1) = lim −x³ quand x → −∞.", True, "À l'infini, un polynôme a la limite de son terme de plus haut degré.")]),
    qcm("fa_4", "Plus facile : l'expression conjuguée", "سؤال ساهل على l'expression conjuguée.",
        "(√(x² + 4x) − x)(√(x² + 4x) + x) est égal à :", ["x² + 4x − x", "4x", "0"], 1, [
          (("قريب، ولكن x خاصو يتطلع au carré: a carré moins b carré. عاود اختار.", "Il faut b², donc x² et pas x. Réessaie."),
           ("الجواب هو quatre x: x carré plus quatre x، moins x carré.", "Réponse : (x² + 4x) − x² = 4x.")),
          ("برافو! a carré moins b carré: x carré plus quatre x، moins x carré، يعني quatre x.", "Juste : a² − b² = x² + 4x − x² = 4x."),
          (("لا، ماشي zéro: x carré كيمشي، ولكن quatre x كيبقى. عاود اختار.", "Les x² s'en vont, mais 4x reste. Réessaie."),
           ("الجواب هو quatre x، حسب a carré moins b carré.", "Réponse : 4x."))],
        "Racine carrée de x carré plus quatre x, moins x, fois, racine carrée de x carré plus quatre x, plus x, est égal à ?"),
  ]),
  "similaire": {
    "id": ID + "_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "On considère f(x) = (−x² + 5)/(2x² + 1) sur ℝ ; g(x) = 2x³ − x + 7 sur ℝ ; h(x) = √(x² + 6x) − x sur [0 ; +∞[.",
      "intro_dit": "نفس التمرين، بدوال أخرى. f de x égale، moins x carré plus cinq، sur، deux x carré plus un. g de x égale deux x cube، moins x، plus sept. وh de x égale، racine carrée de، x carré plus six x، moins x.",
      "figures": [figure("(-x^2+5)/(2*x^2+1)", "f", -1, 5.5, [-1, 0, 1, 2, 3, 4, 5])],
      "donnees": ["f(x) = (−x² + 5)/(2x² + 1)", "g(x) = 2x³ − x + 7", "h(x) = √(x² + 6x) − x, x ≥ 0"],
      "questions": [
        {"id": "1", "texte": "Calculer la limite de f(x) quand x tend vers +∞.",
         "reponse": valeur("lim f(x)", -0.5, "lim f(x) = lim −x²/(2x²) = −1/2 = −0,5"),
         "clavier": {"aides": ["−x²/(2x²)", "plus haut degré"], "pieges": ["5/1 = 5"]},
         "correction": correction([("1 : « ∞/∞ » ; lim f(x) = lim −x²/(2x²)", "le terme de plus haut degré"), ("lim f(x) = −1/2", "la limite égale moins un demi")],
           "فl'infini كنخليو le terme de plus haut degré: moins x carré، sur، deux x carré. إذن la limite égale moins un demi.")},
        {"id": "2", "texte": "Interpréter géométriquement le résultat.",
         "reponse": phrase("La droite d'équation y = −1/2 est une asymptote horizontale à (C_f) au voisinage de +∞."),
         "clavier": {"aides": ["y = −1/2", "asymptote horizontale"], "pieges": ["x = −1/2"]},
         "correction": correction([("2 : la droite d'équation y = −1/2 est une asymptote horizontale à (C_f) au voisinage de +∞", "asymptote horizontale")],
           "la droite d'équation y égale moins un demi، est une asymptote horizontale à la courbe، au voisinage de plus l'infini.")},
        {"id": "3", "texte": "Calculer la limite de g(x) quand x tend vers −∞.",
         "reponse": phrase("lim g(x) = lim 2x³ = −∞ quand x → −∞."),
         "clavier": {"aides": ["2x³", "−∞"], "pieges": ["+∞"]},
         "correction": correction([("3 : lim g(x) = lim 2x³ = −∞", "la limite égale moins l'infini")],
           "كنخليو deux x cube. x cube كيمشي ل moins l'infini، وdeux positif، إذن la limite égale moins l'infini.")},
        {"id": "4", "texte": "Calculer la limite de h(x) quand x tend vers +∞.",
         "reponse": valeur("lim h(x)", 3, "h(x) = 6x/(√(x² + 6x) + x) = 6/(√(1 + 6/x) + 1) ; lim h(x) = 6/2 = 3"),
         "clavier": {"aides": ["√(x² + 6x) + x", "6x"], "pieges": ["+∞ − ∞ = 0"]},
         "correction": correction([("4 : h(x) = 6x/(√(x² + 6x) + x)", "l'expression conjuguée"), ("h(x) = 6/(√(1 + 6/x) + 1) ; lim h(x) = 3", "la limite égale trois")],
           "بl'expression conjuguée كيبقى six x فالفوق. خرجنا x facteur، six sur x كيمشي ل zéro، إذن la limite égale six sur deux، يعني la limite égale trois.")},
      ]}}
}
ecrire(EX)
