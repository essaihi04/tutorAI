# Exercice de maths, ch. 2 (dérivation et étude des fonctions), niveau MOYEN (le niveau du national) :
# fonction rationnelle : asymptote verticale, écriture x + 2 + 4/(x − 1), asymptote oblique, position relative,
# « montrer que f′(x) = … », tableau de variations et extremums.
# Sources comparées (lecture seule, rien de copié) :
#  - exploration/derivation_etude_fonctions.json : cas types asymptote_verticale, asymptote_oblique_donnee,
#    position_relative, montrer_derivee, signe_derivee_variations ; pièges « confondre x = a et y = b »,
#    « limite de f(x) − y au lieu de son signe », « double barre oubliée », « développer (x − 1)² » ;
#    erreurs_examen (phrase d'interprétation sans équation ni voisinage).
#  - vidéos des profs (Aderdour : un cas = une limite + un dessin + une phrase ; maths variés : branches infinies ;
#    Math_houara : « le zéro est caché sous la barre » ; Ishaq Ghanem : écrire l'équation de l'asymptote).
#  - nationaux 2016-2025 : asymptote oblique donnée dans 8 sujets, position relative dans 10, asymptote verticale
#    interprétée dans 8 (fonctions ln/exp, non reprises).
#  - séries en ligne repérées (titres et résumés de recherche ; sites non joignables depuis la session) : Lycée Mohammed
#    Serraj (monstremath : asymptote oblique et position), talamidi exercices non corrigés 2-3, alloschool (fonctions
#    rationnelles), cours Atmani (moutamadris) : la fraction (x² + bx + c)/(x − a) est le modèle classique.
# Différent des exemples du cours ((x² − 2x + 2)/(x − 1), 2x + 1 + 1/x, x + 1/x).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa

D = "/media/simulations/maths/derivation-tableau/"
ID = "math_ex_ch2_derivation_4"


def figure(nom, expr, a, ymin, ymax, titre, droite):
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": a - 6, "max": a + 7, "nom": "x", "graduations": list(range(a - 5, a + 7))},
                     "y": {"min": ymin, "max": ymax, "nom": "y", "graduations": list(range(ymin - ymin % 4 + 4, ymax, 4))}},
            "legende": f"Allure de ({nom}) : deux branches de part et d'autre de la droite x = {a}, et la droite (D) en pointillé.",
            "elements": [{"f": "courbe", "expr": expr, "de": a - 6, "a": a - 0.25, "couleur": "cyan"},
                         {"f": "courbe", "expr": expr, "de": a + 0.25, "a": a + 7, "couleur": "cyan", "texte": f"({nom})", "texte_x": a + 5.5, "pos": "no"},
                         {"f": "courbe", "expr": droite, "de": a - 6, "a": a + 7, "couleur": "orange", "trait": "pointille", "texte": "(D)", "texte_x": a - 4, "pos": "se"},
                         {"f": "repere", "x": a, "couleur": "faible"}]}


Q1 = {"id": "1", "texte": "Calculer lim f(x) quand x → 1⁺ et quand x → 1⁻, puis interpréter géométriquement les résultats.",
      "texte_dit": "السؤال un: حسب la limite ديال f de x quand x tend vers un plus، و quand x tend vers un moins، ومن بعد interpréter géométriquement.",
      "reponse": phrase("x² + x + 2 → 4 > 0 ; x − 1 → 0⁺ à droite et 0⁻ à gauche : lim f(x) = +∞ quand x → 1⁺, lim f(x) = −∞ quand x → 1⁻. La droite d'équation x = 1 est une asymptote verticale à (C)."),
      "clavier": {"aides": ["x² + x + 2 → 4", "x − 1 → 0⁺", "+∞", "−∞", "la droite d'équation x = 1", "asymptote verticale"], "pieges": ["y = 1", "lim = 4/0 = 0"]},
      "aides": [aide("Remplace x par 1 en haut : tu trouves 4. En bas, x − 1 tend vers 0 : de quel signe, à droite puis à gauche de 1 ?",
                     "عوض x ب un فالفوق: كتلقى quatre. فالتحت، x moins un كيمشي ل zéro: واش positif ولا négatif، على اليمين ومن بعد على اليسار؟"),
                aide("Un nombre positif divisé par un nombre très petit positif donne +∞. Si f(x) tend vers l'infini quand x tend vers 1, la droite est verticale : x = 1.",
                     "عدد positif على عدد صغير بزاف positif كيعطي plus l'infini. ويلا f de x مشات ل l'infini ملي x كيمشي ل un، la droite verticale: x égale un.")],
      "correction": correction([
          ("1 : lim (x² + x + 2) = 4 et lim (x − 1) = 0 (x → 1)", "الفوق كيمشي ل quatre"),
          ("x → 1⁺ : x − 1 → 0⁺, donc lim f(x) = +∞", "plus l'infini"),
          ("x → 1⁻ : x − 1 → 0⁻, donc lim f(x) = −∞", "moins l'infini"),
          ("la droite d'équation x = 1 est une asymptote verticale à (C)", "asymptote verticale")],
          "السؤال un. الفوق كيمشي ل quatre. التحت، x moins un، كيمشي ل zéro plus على اليمين، إذن la limite égale plus l'infini. وعلى اليسار، كيمشي ل zéro moins، إذن la limite égale moins l'infini. التفسير: la droite d'équation x égale un، est une asymptote verticale à la courbe."),
      "explication": "ex_d4_1", "facile": "fa_d4_1"}

Q2 = {"id": "2", "texte": "Vérifier que pour tout x ≠ 1 : f(x) = x + 2 + 4/(x − 1), puis montrer que la droite (D) d'équation y = x + 2 est une asymptote oblique à (C) au voisinage de +∞ et de −∞.",
      "texte_dit": "السؤال deux: تحقق بلي لكل x مختلف على un، f de x égale x plus deux، plus quatre sur x moins un. ومن بعد بين بلي la droite D، اللي l'équation ديالها y égale x plus deux، asymptote oblique، au voisinage de plus l'infini و moins l'infini.",
      "reponse": phrase("x + 2 + 4/(x − 1) = ((x + 2)(x − 1) + 4)/(x − 1) = (x² + x − 2 + 4)/(x − 1) = (x² + x + 2)/(x − 1) = f(x). Donc f(x) − (x + 2) = 4/(x − 1), qui tend vers 0 en +∞ et en −∞ : (D) : y = x + 2 est asymptote oblique à (C) au voisinage de +∞ et de −∞."),
      "clavier": {"aides": ["(x + 2)(x − 1) + 4", "f(x) − (x + 2) = 4/(x − 1)", "lim 4/(x − 1) = 0", "au voisinage de +∞"], "pieges": ["lim f(x)/x = 1 donc asymptote", "y = x"]},
      "aides": [aide("Pars du membre le plus facile à transformer : x + 2 + 4/(x − 1). Mets-le au même dénominateur x − 1.",
                     "بدا من الجهة الساهلة: x plus deux، plus quatre sur x moins un. حطها على نفس le dénominateur، x moins un."),
                aide("Pour l'asymptote, calcule f(x) − (x + 2) avec cette écriture, puis sa limite en +∞ et en −∞.",
                     "باش تبين l'asymptote، حسب f de x moins، x plus deux، بهاد الكتابة، ومن بعد la limite ديالو ف plus l'infini و moins l'infini.")],
      "correction": correction([
          ("2 : x + 2 + 4/(x − 1) = ((x + 2)(x − 1) + 4)/(x − 1)", "نفس le dénominateur"),
          ("= (x² + x − 2 + 4)/(x − 1) = (x² + x + 2)/(x − 1) = f(x)", "كنلقاو f de x"),
          ("f(x) − (x + 2) = 4/(x − 1) → 0 quand x → +∞ et quand x → −∞", "كيمشي ل zéro"),
          ("donc (D) : y = x + 2 est une asymptote oblique à (C) au voisinage de +∞ et de −∞", "asymptote oblique")],
          "السؤال deux. كنبداو من x plus deux، plus quatre sur x moins un، وكنحطوها على نفس le dénominateur: x plus deux، fois x moins un، plus quatre، يعني x carré plus x plus deux. كنلقاو f de x. إذن f de x moins، x plus deux، égale quatre sur x moins un، و هادا كيمشي ل zéro ف plus l'infini و ف moins l'infini. إذن la droite D، y égale x plus deux، est une asymptote oblique à la courbe، au voisinage de plus l'infini et de moins l'infini."),
      "explication": "ex_d4_2", "facile": "fa_d4_2"}

Q3 = {"id": "3", "texte": "Étudier la position relative de (C) et de (D).",
      "texte_dit": "السؤال trois: درس la position relative ديال la courbe و la droite D.",
      "reponse": phrase("f(x) − (x + 2) = 4/(x − 1) a le signe de x − 1 : sur ]1 ; +∞[ il est positif, (C) est au-dessus de (D) ; sur ]−∞ ; 1[ il est négatif, (C) est en dessous de (D)."),
      "clavier": {"aides": ["f(x) − (x + 2) = 4/(x − 1)", "le signe de x − 1", "au-dessus", "en dessous"], "pieges": ["lim 4/(x − 1) = 0", "(C) coupe (D)"]},
      "aides": [aide("La position se lit avec le SIGNE de f(x) − (x + 2), pas avec sa limite.",
                     "la position كتقرا ب le signe ديال f de x moins، x plus deux، ماشي ب la limite ديالو."),
                aide("4 est positif : le signe de 4/(x − 1) est celui de x − 1. Positif : au-dessus ; négatif : en dessous.",
                     "quatre positif: le signe ديال quatre sur x moins un هو le signe ديال x moins un. positif: الفوق، négatif: التحت.")],
      "correction": correction([
          ("3 : f(x) − (x + 2) = 4/(x − 1), du signe de x − 1", "le signe ديال x moins un"),
          ("sur ]1 ; +∞[ : f(x) − (x + 2) > 0, (C) est au-dessus de (D)", "au-dessus"),
          ("sur ]−∞ ; 1[ : f(x) − (x + 2) < 0, (C) est en dessous de (D)", "en dessous")],
          "السؤال trois. f de x moins، x plus deux، égale quatre sur x moins un، وعندو le signe ديال x moins un. على اليمين ديال un، positif: la courbe au-dessus de la droite. وعلى اليسار ديال un، négatif: la courbe en dessous de la droite."),
      "explication": "ex_d4_3", "facile": "fa_d4_3"}

Q4 = {"id": "4", "texte": "Montrer que pour tout x ≠ 1 : f′(x) = (x + 1)(x − 3)/(x − 1)².",
      "texte_dit": "السؤال quatre: بين بلي لكل x مختلف على un: f prime de x égale، x plus un، fois، x moins trois، sur، x moins un au carré.",
      "reponse": phrase("f est dérivable sur ℝ∖{1} ; avec f(x) = x + 2 + 4/(x − 1) : f′(x) = 1 − 4/(x − 1)² = ((x − 1)² − 4)/(x − 1)² = (x − 1 − 2)(x − 1 + 2)/(x − 1)² = (x − 3)(x + 1)/(x − 1)²."),
      "clavier": {"aides": ["(1/v)′ = −v′/v²", "1 − 4/(x − 1)²", "a² − b² = (a − b)(a + b)", "(x − 1)² − 4"], "pieges": ["4/(x − 1)²", "développer (x − 1)²"]},
      "aides": [aide("Utilise l'écriture de la question 2 : la dérivée de x + 2 est 1, et (1/v)′ = −v′/v².",
                     "خدم بالكتابة ديال السؤال deux: la dérivée ديال x plus deux هي un، و un sur v، la dérivée ديالها moins v prime sur v au carré."),
                aide("Mets au même dénominateur (x − 1)², puis reconnais a² − b² avec a = x − 1 et b = 2.",
                     "حط على نفس le dénominateur، x moins un au carré، ومن بعد عقل على a carré moins b carré، مع a égale x moins un، و b égale deux.")],
      "correction": correction([
          ("4 : f est dérivable sur ℝ∖{1} et f′(x) = 1 − 4/(x − 1)²", "f prime de x égale un moins quatre"),
          ("= ((x − 1)² − 4)/(x − 1)²", "نفس le dénominateur"),
          ("= (x − 1 − 2)(x − 1 + 2)/(x − 1)² = (x − 3)(x + 1)/(x − 1)²", "a carré moins b carré")],
          "السؤال quatre. f dérivable sur R privé de un. f prime de x égale un moins quatre، sur x moins un au carré. على نفس le dénominateur: x moins un au carré، moins quatre. هادي a carré moins b carré: x moins trois، fois، x plus un. إذن f prime de x égale، x plus un، fois، x moins trois، sur، x moins un au carré."),
      "explication": "ex_d4_4", "facile": "fa_d4_4"}

Q5 = {"id": "5", "texte": "Dresser le tableau de variations de f, puis donner le minimum local de f sur ]1 ; +∞[.",
      "texte_dit": "السؤال cinq: دير le tableau de variations ديال f، ومن بعد عطي le minimum local ديال f على un، plus l'infini.",
      "reponse": valeur("minimum local", 7, "(x − 1)² > 0 : f′ a le signe de (x + 1)(x − 3) : + sur ]−∞ ; −1[, − sur ]−1 ; 1[ et ]1 ; 3[, + sur ]3 ; +∞[ ; f(−1) = −1 (maximum local), f(3) = 7 ; le minimum local sur ]1 ; +∞[ est f(3) = 7"),
      "clavier": {"aides": ["(x − 1)² > 0", "double barre en 1", "f(−1) = −1", "f(3) ="], "pieges": ["f(3) = 5", "f(1) ="]},
      "aides": [aide("Le dénominateur (x − 1)² est positif : le signe de f′ est celui de (x + 1)(x − 3). Mets une double barre en 1.",
                     "le dénominateur، x moins un au carré، positif: le signe ديال f prime هو le signe ديال، x plus un، fois، x moins trois. وف un، دير double barre."),
                aide("Calcule f(−1) et f(3) avec l'écriture x + 2 + 4/(x − 1) ; les limites aux bornes viennent des questions 1 et 2.",
                     "حسب f de moins un و f de trois بالكتابة x plus deux، plus quatre sur x moins un. و les limites جات من السؤال un و السؤال deux.")],
      "correction": correction([
          ("5 : (x − 1)² > 0, donc f′(x) a le signe de (x + 1)(x − 3)", "le signe ديال f prime"),
          ("f(−1) = −1 + 2 + 4/(−2) = −1 ;  f(3) = 3 + 2 + 4/2 = 7", "f de trois égale sept"),
          ("x : −∞ ↗ −1 ↘ 1 ‖ 1 ↘ 3 ↗ +∞ ;  f : −∞ ↗ −1 ↘ −∞ ‖ +∞ ↘ 7 ↗ +∞", "le tableau"),
          ("sur ]1 ; +∞[, le minimum local est f(3) = 7", "le minimum local égale sept")],
          "السؤال cinq. x moins un au carré positif، إذن le signe ديال f prime هو le signe ديال، x plus un، fois، x moins trois. f de moins un égale moins un، و f de trois égale sept. le tableau: طالعة من moins l'infini حتى moins un، هابطة حتى moins l'infini، double barre ف un، ومن بعد هابطة من plus l'infini حتى sept، وطالعة حتى plus l'infini. إذن على اليمين ديال un، le minimum local égale sept."),
      "explication": "ex_d4_5", "facile": "fa_d4_5"}

SIM1 = sim("ex_d4_1", "Question 1 : une asymptote verticale",
           "f(x) → ±∞ quand x → a : la droite x = a est asymptote verticale.",
           D + "branches.html?vue=verticale", "Un point M monte le long de la droite x = 2",
           "نشوفو على هاد l'exemple: f de x égale un sur x moins deux، plus un. النقطة M كتقرب ل deux من اليمين. شوف القيم: f de x كتكبر بزاف، و M كتطلع حدا la droite verticale. ملي x tend vers deux plus، la limite égale plus l'infini. الجملة: la droite d'équation x égale deux، est une asymptote verticale. رد البال: f de x هي اللي كتمشي ل l'infini، إذن la droite verticale، x égale a. فالتمرين ديالك: كتب لاش كيمشي الفوق ولاش كيمشي التحت، على اليمين وعلى اليسار.",
           [("lim f(x) = ±∞ (x → a) ⇒ asymptote x = a", "الجملة")],
           [jusqua("نشوفو على هاد l'exemple", "courbe_tracee"), jusqua("النقطة M كتقرب", "m_part"), {"mot": "النقطة M كتقرب", "repere": "point_m"},
            jusqua("حدا la droite verticale", "asymptote_verticale"), jusqua("الجملة", "limite_ecrite"), montre("الجملة", "centre:0")])

SIM2 = sim("ex_d4_2", "Question 2 : vérifier l'écriture, puis l'asymptote oblique",
           "f(x) − (ax + b) → 0 en l'infini : asymptote oblique y = ax + b.",
           D + "calculs.html?vue=bi7", "La méthode écrite au tableau sur (x² − 2x + 2)/(x − 1)",
           "نشوفو la méthode على هاد l'exemple ديال الدرس: f de x égale x carré moins deux x plus deux، sur x moins un، وكتكتب x moins un، plus un sur x moins un. باش نبينو l'asymptote، كنحسبو الفرق: f de x moins، x moins un، égale un sur x moins un. la limite ديالو ف plus l'infini égale zéro. إذن la droite y égale x moins un، asymptote oblique، au voisinage de plus l'infini. limite وحدة كافية. فالتمرين ديالك: تحقق من الكتابة بنفس le dénominateur، وحسب الفرق ف plus l'infini و moins l'infini.",
           [("f(x) − (ax + b) → 0 ⇒ asymptote oblique", "كنحسبو الفرق"), ("phrase : équation + voisinage", "au voisinage de plus l'infini")],
           [jusqua("نشوفو la méthode", "enonce"), jusqua("كنحسبو الفرق", "difference"), montre("كنحسبو الفرق", "centre:0"),
            jusqua("la limite ديالو", "limite"), jusqua("au voisinage de plus l'infini", "conclusion"), montre("au voisinage de plus l'infini", "centre:1"),
            jusqua("limite وحدة كافية", "remarque")])

SIM3 = sim("ex_d4_3", "Question 3 : la position relative",
           "Le signe de f(x) − y : positif au-dessus, négatif en dessous.",
           D + "position.html?vue=ecart", "Un segment entre (Δ) et la courbe de 2x + 1 + 1/x",
           "نشوفو على هاد l'exemple: f de x égale deux x plus un، plus un sur x، و la droite y égale deux x plus un. الفرق هو un sur x. فx égale un، القطعة خضرا: الفرق positif، la courbe au-dessus. فx égale moins un، القطعة حمرا: الفرق négatif، la courbe en dessous. le tableau ديال le signe كيعطي la position فكل intervalle. فالتمرين ديالك: الفرق هو quatre sur x moins un، شوف le signe ديالو.",
           [("f(x) − y > 0 : au-dessus ; < 0 : en dessous", "le tableau ديال le signe")],
           [jusqua("نشوفو على هاد l'exemple", "droite_tracee"), {"mot": "نشوفو على هاد l'exemple", "repere": "droite"},
            jusqua("فx égale un، القطعة خضرا", "ecart_positif"), {"mot": "فx égale un، القطعة خضرا", "repere": "segment"},
            jusqua("فx égale moins un", "ecart_negatif"), jusqua("le tableau ديال le signe", "tableau_rempli"), montre("le tableau ديال le signe", "centre:0")])

SIM4 = sim("ex_d4_4", "Question 4 : dériver l'écriture commode, puis factoriser",
           "1 − k/(x − a)² se met au même dénominateur, puis se factorise.",
           D + "calculs.html?vue=va5", "Le calcul de f′ pour x + 1/x au tableau",
           "نشوفو على هاد l'exemple: f de x égale x plus un sur x. f prime de x égale un moins un sur x carré. على نفس le dénominateur: x carré moins un، sur x carré، وكيتفك: x moins un، fois، x plus un. التحت x carré positif، إذن le signe ديال f prime هو le signe ديال الفوق. فالتمرين ديالك: derive x plus deux، plus quatre sur x moins un، ومن بعد استعمل a carré moins b carré.",
           [("(1/v)′ = −v′/v²", "f prime de x égale un moins"), ("même dénominateur, puis a² − b²", "على نفس le dénominateur")],
           [jusqua("f prime de x égale un moins", "derivee"), montre("f prime de x égale un moins", "centre:0"), montre("على نفس le dénominateur", "centre:1"),
            jusqua("التحت x carré positif", "phrase")])

SIM5 = sim("ex_d4_5", "Question 5 : le tableau, la double barre et les extremums",
           "La valeur interdite : double barre ; les extremums au bout des flèches.",
           D + "trace.html?vue=etapes", "Le tableau de x + 1/x, et la courbe tracée à partir de lui",
           "نشوفو على هاد l'exemple: le tableau ديال x plus un sur x. السطر ديال f prime: plus، zéro، moins، double barre ف zéro، moins، zéro، plus. فالراس ديال les flèches: moins deux، le maximum local، و deux، le minimum local. ف zéro، la double barre: f ما معرفاش، و la droite x égale zéro asymptote verticale. والقيم ديال les extremums هي فين la tangente horizontale. فالتمرين ديالك: la double barre ف un، و حسب f de moins un و f de trois.",
           [("valeur interdite : double barre ‖", "double barre ف zéro"), ("extremums : tangentes horizontales", "la tangente horizontale")],
           [jusqua("نشوفو على هاد l'exemple", "tableau_lu"), {"mot": "نشوفو على هاد l'exemple", "repere": "tableau"},
            montre("double barre ف zéro", "centre:0"), jusqua("و la droite x égale zéro", "asymptote_verticale"),
            jusqua("la tangente horizontale", "tangentes_horizontales"), montre("la tangente horizontale", "centre:1")])

FA1 = qcm("fa_d4_1", "Plus facile : quelle asymptote ?", "سؤال ساهل على l'asymptote.",
          "lim f(x) = +∞ quand x → 1⁺. Quelle droite est asymptote à (C) ?", ["y = 1", "x = 1", "y = x + 2"], 1, [
              (("قريب! y égale un droite أفقية. هنا x هو اللي كيمشي ل un، و f de x ل l'infini. عاود اختار.", "y = 1 est horizontale ; ici c'est x qui tend vers 1. Réessaie."),
               ("الجواب: x égale un، asymptote verticale.", "Réponse : x = 1, asymptote verticale.")),
              ("برافو! f de x كتمشي ل l'infini ملي x كيمشي ل un: la droite verticale، x égale un.", "Juste : asymptote verticale x = 1."),
              (("ما تقلقش. y égale x plus deux هي l'asymptote oblique ف l'infini، ماشي قريب من un. عاود اختار.", "y = x + 2 est l'asymptote en l'infini. Réessaie."),
               ("الجواب: x égale un.", "Réponse : x = 1."))],
          "La limite en un plus est plus l'infini. Quelle droite est asymptote ?")

FA2 = qcm("fa_d4_2", "Plus facile : la différence", "نتمرنو على الفرق.",
          "Avec f(x) = x + 2 + 4/(x − 1), f(x) − (x + 2) est égal à…", ["4/(x − 1)", "x + 2", "4"], 0, [
              ("برافو! كيبقى غير quatre sur x moins un، وهو اللي كيمشي ل zéro.", "Juste : f(x) − (x + 2) = 4/(x − 1)."),
              (("قريب! x plus deux هي la droite، كنحيدوها. عاود اختار.", "On enlève x + 2. Réessaie."),
               ("الجواب: quatre sur x moins un.", "Réponse : 4/(x − 1).")),
              (("ما تقلقش. quatre بوحدو ناقص: خاص sur x moins un. عاود اختار.", "Il manque le dénominateur. Réessaie."),
               ("الجواب: quatre sur x moins un.", "Réponse : 4/(x − 1)."))],
          "f de x moins، x plus deux، est égal à ?")

FA3 = association("fa_d4_3", "Plus facile : position", "Relie chaque intervalle à la position de (C).",
                  "نتمرنو: ربط كل intervalle مع la position ديال la courbe.", "Relie chaque intervalle à la position de (C) par rapport à (D).",
                  [("1", "]−∞ ; 1["), ("2", "]1 ; +∞[")],
                  [("a", "(C) au-dessus de (D)"), ("b", "(C) en dessous de (D)")],
                  {"1": "b", "2": "a"},
                  {"1-a": ("Teste x = 0 : 4/(0 − 1) = −4 < 0.", "لا، جرب x égale zéro: كتلقى moins quatre، négatif."),
                   "1-b": ("Oui : 4/(x − 1) < 0 quand x < 1.", "برافو: قبل un، الفرق négatif، la courbe en dessous."),
                   "2-a": ("Oui : 4/(x − 1) > 0 quand x > 1.", "برافو: من بعد un، الفرق positif، la courbe au-dessus."),
                   "2-b": ("Teste x = 2 : 4/(2 − 1) = 4 > 0.", "لا، جرب x égale deux: كتلقى quatre، positif.")},
                  ("(1 ; b) (2 ; a) : le signe de f(x) − (x + 2) donne la position.", "le signe ديال الفرق كيعطي la position."))

FA4 = vrai_faux("fa_d4_4", "Plus facile : vrai ou faux", "f′(x) = 1 − 4/(x − 1)².", "سؤال ساهل: صحيح ولا غالط؟", [
    ("La dérivée de 4/(x − 1) est −4/(x − 1)².", True, "(1/v)′ = −v′/v² avec v = x − 1, v′ = 1."),
    ("(x − 1)² − 4 = (x − 3)(x + 1).", True, "a² − b² = (a − b)(a + b) avec a = x − 1, b = 2."),
    ("Il faut développer (x − 1)² au dénominateur.", False, "Le dénominateur reste factorisé : il est positif, c'est tout ce qu'on lit.")])

FA5 = qcm("fa_d4_5", "Plus facile : la valeur au bout de la flèche", "سؤال ساهل على le minimum.",
          "f(3) = 3 + 2 + 4/(3 − 1) vaut…", ["5", "7", "9"], 1, [
              (("قريب! نسيتي quatre sur deux. عاود اختار.", "Tu as oublié 4/2. Réessaie."),
               ("الجواب: sept، trois plus deux plus deux.", "Réponse : 7.")),
              ("برافو! trois plus deux plus deux، égale sept.", "Juste : f(3) = 3 + 2 + 2 = 7."),
              (("ما تقلقش. quatre sur deux، égale deux، ماشي quatre. عاود اختار.", "4/2 = 2. Réessaie."),
               ("الجواب: sept.", "Réponse : 7."))],
          "f de trois vaut ?")

EX = {
    "id": ID, "type": "exercice", "version": 1, "status": "published",
    "matiere": "mathematiques", "chapitre": "derivation_etude_fonctions", "cours": "math_ch2_derivation_etude_fonctions",
    "titre": "Fonction rationnelle : asymptotes, position, variations", "niveau": "moyen", "duree_min": 35, "origine": ORIGINE,
    "competences": ["Interpréter une limite infinie (asymptote verticale)", "Montrer qu'une droite est asymptote oblique", "Étudier la position relative", "Montrer que f′(x) = une forme donnée", "Dresser un tableau de variations avec une valeur interdite"],
    "enonce": {
        "intro": "On considère la fonction f définie sur ℝ∖{1} par f(x) = (x² + x + 2)/(x − 1), (C) sa courbe représentative dans un repère orthonormé, et (D) la droite d'équation y = x + 2.",
        "intro_dit": "دابا نقراو l'énoncé. f معرفة على R privé de un: f de x égale x carré plus x plus deux، sur x moins un. C هي la courbe ديالها، و D هي la droite اللي l'équation ديالها y égale x plus deux.",
        "figures": [figure("C", "(x^2+x+2)/(x-1)", 1, -12, 18, "Allure de (C) et de (D)", "x+2")],
        "donnees": ["f(x) = (x² + x + 2)/(x − 1), x ≠ 1", "(D) : y = x + 2", "lim f(x) = +∞ en +∞ et lim f(x) = −∞ en −∞ (admis)"],
        "questions": [Q1, Q2, Q3, Q4, Q5]},
    "explication": deck("explication", "Explication animée", [SIM1, SIM2, SIM3, SIM4, SIM5]),
    "facile": deck("facile", "Plus facile, pour s'entraîner", [FA1, FA2, FA3, FA4, FA5]),
    "similaire": {"id": ID + "_b", "titre": "Même exercice, autres données", "enonce": {
        "intro": "On considère la fonction g définie sur ℝ∖{2} par g(x) = (x² − x + 7)/(x − 2), (C′) sa courbe et (D′) la droite d'équation y = x + 1.",
        "intro_dit": "نفس التمرين، بدالة أخرى: g de x égale x carré moins x plus sept، sur x moins deux، و la droite D prime: y égale x plus un.",
        "figures": [figure("C′", "(x^2-x+7)/(x-2)", 2, -16, 24, "Allure de (C′) et de (D′)", "x+1")],
        "donnees": ["g(x) = (x² − x + 7)/(x − 2), x ≠ 2", "(D′) : y = x + 1", "lim g(x) = +∞ en +∞ et lim g(x) = −∞ en −∞ (admis)"],
        "questions": [
            {"id": "1", "texte": "Calculer lim g(x) quand x → 2⁺ et quand x → 2⁻ ; interpréter.",
             "reponse": phrase("x² − x + 7 → 9 > 0 : lim g = +∞ en 2⁺, −∞ en 2⁻ ; la droite x = 2 est asymptote verticale à (C′)."),
             "clavier": {"aides": ["→ 9", "x − 2 → 0⁺", "x = 2"], "pieges": ["y = 2"]},
             "correction": correction([("1 : lim g(x) = +∞ (x → 2⁺) ; lim g(x) = −∞ (x → 2⁻)", "plus l'infini"),
                                       ("la droite d'équation x = 2 est une asymptote verticale à (C′)", "asymptote verticale")],
                                      "الفوق كيمشي ل neuf. على اليمين la limite égale plus l'infini، وعلى اليسار moins l'infini. إذن la droite x égale deux، asymptote verticale.")},
            {"id": "2", "texte": "Vérifier que g(x) = x + 1 + 9/(x − 2), puis montrer que (D′) est asymptote oblique à (C′) en +∞ et en −∞.",
             "reponse": phrase("x + 1 + 9/(x − 2) = (x² − x − 2 + 9)/(x − 2) = g(x) ; g(x) − (x + 1) = 9/(x − 2) → 0 en ±∞ : (D′) asymptote oblique."),
             "clavier": {"aides": ["(x + 1)(x − 2) + 9", "9/(x − 2) → 0"], "pieges": ["y = x"]},
             "correction": correction([("2 : x + 1 + 9/(x − 2) = ((x + 1)(x − 2) + 9)/(x − 2) = (x² − x + 7)/(x − 2) = g(x)", "نفس le dénominateur"),
                                       ("g(x) − (x + 1) = 9/(x − 2) → 0 en ±∞ : (D′) : y = x + 1 est asymptote oblique", "asymptote oblique")],
                                      "على نفس le dénominateur كنلقاو g de x. الفرق g de x moins، x plus un، égale neuf sur x moins deux، وكيمشي ل zéro. إذن la droite y égale x plus un، asymptote oblique.")},
            {"id": "3", "texte": "Étudier la position relative de (C′) et (D′).",
             "reponse": phrase("g(x) − (x + 1) = 9/(x − 2) : > 0 sur ]2 ; +∞[ ((C′) au-dessus), < 0 sur ]−∞ ; 2[ ((C′) en dessous)."),
             "clavier": {"aides": ["le signe de x − 2"], "pieges": ["lim = 0"]},
             "correction": correction([("3 : sur ]2 ; +∞[, (C′) au-dessus de (D′) ; sur ]−∞ ; 2[, (C′) en dessous", "au-dessus")],
                                      "le signe ديال neuf sur x moins deux هو le signe ديال x moins deux: من بعد deux، la courbe au-dessus، وقبل deux، en dessous.")},
            {"id": "4", "texte": "Montrer que g′(x) = (x + 1)(x − 5)/(x − 2)².",
             "reponse": phrase("g′(x) = 1 − 9/(x − 2)² = ((x − 2)² − 9)/(x − 2)² = (x − 5)(x + 1)/(x − 2)²."),
             "clavier": {"aides": ["1 − 9/(x − 2)²", "a² − b²"], "pieges": ["9/(x − 2)²"]},
             "correction": correction([("4 : g′(x) = 1 − 9/(x − 2)² = ((x − 2)² − 9)/(x − 2)² = (x + 1)(x − 5)/(x − 2)²", "a carré moins b carré")],
                                      "g prime de x égale un moins neuf، sur x moins deux au carré. على نفس le dénominateur، ومن بعد a carré moins b carré: x moins cinq، fois، x plus un.")},
            {"id": "5", "texte": "Dresser le tableau de variations de g et donner le minimum local de g sur ]2 ; +∞[.",
             "reponse": valeur("minimum local", 9, "g′ a le signe de (x + 1)(x − 5) ; g(−1) = −3 (maximum local), g(5) = 5 + 1 + 3 = 9 ; minimum local sur ]2 ; +∞[ : g(5) = 9"),
             "clavier": {"aides": ["g(5) =", "g(−1) = −3"], "pieges": ["g(5) = 6"]},
             "correction": correction([("5 : g(−1) = −3 (maximum local) ; g(5) = 9 (minimum local) ; double barre en 2", "g de cinq égale neuf"),
                                       ("le minimum local sur ]2 ; +∞[ est g(5) = 9", "le minimum local égale neuf")],
                                      "g de moins un égale moins trois، maximum local. و g de cinq égale neuf. إذن على اليمين ديال deux، le minimum local égale neuf.")}]}}
}
ecrire(EX)
