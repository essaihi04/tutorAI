# Exercice de maths, ch. 2 (dérivation et étude des fonctions), niveau FACILE (s'entraîner) :
# nombre dérivé par la limite du taux, équation de la tangente, tangente horizontale.
# Sources comparées (lecture seule, rien de copié) :
#  - exploration/derivation_etude_fonctions.json : cas types derivabilite_point et tangente_equation, pièges
#    « s'arrêter à 0/0 », « oublier f(x₀) », « y = f'(x₀)(x − x₀) sans + f(x₀) » ; erreurs_examen (phrase de conclusion).
#  - vidéos des profs (Amine Hidane : dérivabilité en un point très simplifiée ; Math & Phys : exercices de dérivabilité ;
#    Driss DOTCOM : les bases, tableau des dérivées).
#  - nationaux 2016 R, 2024 R, 2025 N, 2025 R : « déterminer l'équation de la tangente » (fonctions ln/exp, non reprises).
#  - séries en ligne repérées (titres et résumés de recherche ; sites non joignables depuis la session) : talamidi série 1
#    et exercices non corrigés 2-3, Lycée Mohammed Serraj (monstremath), devoirs corrigés Hammouda (scribd), cours Atmani
#    (moutamadris) : le polynôme du second degré en un point est l'entrée classique.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa

D = "/media/simulations/maths/derivation-tableau/"
ID = "math_ex_ch2_derivation_1"


def figure(nom, expr, x0, y0, xmin, xmax, ymin, ymax, titre):
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": xmin, "max": xmax, "nom": "x", "graduations": list(range(int(xmin) + 1, int(xmax) + 1))},
                     "y": {"min": ymin, "max": ymax, "nom": "y", "graduations": list(range(int(ymin) + 1, int(ymax) + 1, 2))}},
            "legende": f"La courbe ({nom}) et le point A({x0} ; {y0}) où l'on cherche la tangente.",
            "elements": [{"f": "courbe", "expr": expr, "de": xmin, "a": xmax, "couleur": "cyan", "texte": f"({nom})", "texte_x": xmax - 0.4, "pos": "no"},
                         {"f": "point", "at": [x0, y0], "couleur": "jaune", "t": "A", "pos": "se"},
                         {"f": "repere", "x": x0, "couleur": "faible"}]}


Q1 = {"id": "1", "texte": "En utilisant la limite du taux d'accroissement, montrer que f est dérivable en 1 et calculer f′(1).",
      "texte_dit": "السؤال un: باستعمال la limite ديال le taux d'accroissement، بين بلي f dérivable en un، وحسب f prime de un.",
      "reponse": valeur("f′(1)", 3, "f(1) = 0 ; (f(x) − f(1))/(x − 1) = (x − 1)(x + 2)/(x − 1) = x + 2 ; la limite en 1 vaut 3 : f est dérivable en 1 et f′(1) = 3"),
      "clavier": {"aides": ["f(1) =", "(f(x) − f(1))/(x − 1)", "(x − 1)(x + 2)", "lim", "f′(1) ="], "pieges": ["0/0 = 0", "f′(1) = 2x + 1"]},
      "aides": [aide("Commence par f(1), puis écris le taux (f(x) − f(1))/(x − 1). En remplaçant x par 1, tu trouves 0/0 : il faut transformer.",
                     "بدا ب f de un، ومن بعد كتب le taux: f de x moins f de un، sur x moins un. يلا عوضتي x ب un كتلقى zéro sur zéro: خاصك تبدل الكتابة."),
                aide("Factorise le numérateur : x² + x − 2 s'annule en x = 1, donc il s'écrit (x − 1)(x + ?). Simplifie par (x − 1).",
                     "factorise le numérateur: x carré plus x moins deux، s'annule en un، إذن فيه le facteur x moins un. من بعد simplifie ب x moins un.")],
      "correction": correction([
          ("1 : f(1) = 1 + 1 − 2 = 0", "f de un égale zéro"),
          ("(f(x) − f(1))/(x − 1) = (x² + x − 2)/(x − 1) : forme « 0/0 »", "forme indéterminée"),
          ("= (x − 1)(x + 2)/(x − 1) = x + 2  (x ≠ 1)", "x moins un، fois، x plus deux"),
          ("lim (x + 2) = 3 ∈ ℝ  (x → 1)", "la limite égale trois"),
          ("donc f est dérivable en 1 et f′(1) = 3", "f est dérivable en un")],
          "السؤال un. f de un égale zéro. le taux هو x carré plus x moins deux، sur x moins un: كنلقاو zéro sur zéro، forme indéterminée. كنفكو le numérateur: x moins un، fois، x plus deux. كنبسطو، كيبقى x plus deux. ملي x كيقرب ل un، la limite égale trois، وهو عدد حقيقي. إذن f est dérivable en un، و f prime de un égale trois."),
      "explication": "ex_d1_1", "facile": "fa_d1_1"}

Q2 = {"id": "2", "texte": "Déterminer une équation de la tangente (T) à (C) au point A(1 ; 0).",
      "texte_dit": "السؤال deux: لقا l'équation ديال la tangente T ل la courbe، فالنقطة A، اللي الإحداثيات ديالها un و zéro.",
      "reponse": phrase("(T) : y = f′(1)(x − 1) + f(1) = 3(x − 1) + 0, donc (T) : y = 3x − 3"),
      "clavier": {"aides": ["y = f′(1)(x − 1) + f(1)", "f′(1) = 3", "f(1) = 0", "y ="], "pieges": ["y = 3x", "y = 3(x − 1) + 1"]},
      "aides": [aide("La tangente en x₀ a pour équation y = f′(x₀)(x − x₀) + f(x₀). Ici x₀ = 1.",
                     "l'équation ديال la tangente هي: y égale f prime de x zéro، facteur de x moins x zéro، plus f de x zéro. هنا x zéro égale un."),
                aide("Tu connais f′(1) (question 1) et f(1). Remplace, puis développe ; vérifie que A est sur la droite trouvée.",
                     "عندك f prime de un من السؤال un، وعندك f de un. عوض، ومن بعد نشر. وتأكد بلي A كاينة على la droite.")],
      "correction": correction([
          ("2 : (T) : y = f′(1)(x − 1) + f(1)", "y égale f prime de un"),
          ("y = 3(x − 1) + 0", "trois، facteur de x moins un"),
          ("(T) : y = 3x − 3", "y égale trois x moins trois")],
          "السؤال deux. y égale f prime de un، facteur de x moins un، plus f de un. كنعوضو: trois، facteur de x moins un، plus zéro. إذن y égale trois x moins trois. وكنتأكدو: ملي x égale un، y égale zéro، إذن A على la tangente."),
      "explication": "ex_d1_2", "facile": "fa_d1_2"}

Q3 = {"id": "3", "texte": "Calculer f′(x) pour tout x de ℝ, puis déterminer l'abscisse du point de (C) où la tangente est horizontale.",
      "texte_dit": "السؤال trois: حسب f prime de x لكل x من R، ومن بعد لقا l'abscisse ديال النقطة من la courbe، فين la tangente horizontale.",
      "reponse": valeur("x", -0.5, "f′(x) = 2x + 1 ; tangente horizontale ⇔ f′(x) = 0 ⇔ 2x + 1 = 0 ⇔ x = −0,5"),
      "clavier": {"aides": ["f′(x) =", "2x + 1", "f′(x) = 0", "x ="], "pieges": ["x = 0,5", "f′(x) = 2x"]},
      "aides": [aide("Dérive terme à terme : (x²)′ = 2x, (x)′ = 1, la constante donne 0.",
                     "derive كل terme بوحدو: x carré كتعطي deux x، و x كتعطي un، و la constante كتعطي zéro."),
                aide("Une tangente horizontale a une pente nulle : résous f′(x) = 0.",
                     "la tangente horizontale، la pente ديالها zéro: حل l'équation f prime de x égale zéro.")],
      "correction": correction([
          ("3 : f′(x) = 2x + 1", "f prime de x égale deux x plus un"),
          ("tangente horizontale ⇔ f′(x) = 0", "la pente ديالها zéro"),
          ("2x + 1 = 0 ⇔ x = −1/2 = −0,5", "x égale moins un demi")],
          "السؤال trois. f prime de x égale deux x plus un. la tangente horizontale يعني la pente ديالها zéro، يعني f prime de x égale zéro. deux x plus un égale zéro، إذن x égale moins un demi، يعني moins zéro virgule cinq."),
      "explication": "ex_d1_3", "facile": "fa_d1_3"}

SIM1 = sim("ex_d1_1", "Question 1 : la limite du taux, sur l'exemple du cours",
           "f(x) = x² en 1 : le taux se simplifie, sa limite est le nombre dérivé.",
           D + "calculs.html?vue=nd4", "La méthode écrite au tableau sur f(x) = x²",
           "نشوفو la méthode على هاد l'exemple ديال الدرس: f de x égale x carré، فالنقطة un. أول حاجة: f de un égale un. من بعد le taux: x carré moins un، sur x moins un. يلا عوضنا، كنلقاو zéro sur zéro. كنفكو: x moins un، fois، x plus un، وكنبسطو ب x moins un. كيبقى x plus un، و la limite ديالو deux. عدد حقيقي: إذن f est dérivable en un، و f prime de un égale deux. فالتمرين ديالك، دير نفس الخطوات: f de un، le taux، la factorisation، la limite، و الجملة ديال الخلاصة.",
           [("f(x₀) d'abord", "أول حاجة"), ("0/0 : on factorise par (x − x₀)", "كنفكو"), ("limite réelle ⇒ dérivable", "عدد حقيقي")],
           [jusqua("أول حاجة", "f_x0"), montre("أول حاجة", "centre:0"), jusqua("من بعد le taux", "forme"),
            jusqua("كنفكو", "factorise"), montre("كنفكو", "centre:1"), jusqua("عدد حقيقي", "conclusion1"), montre("عدد حقيقي", "centre:2")])

SIM2 = sim("ex_d1_2", "Question 2 : l'équation de la tangente",
           "y = f′(x₀)(x − x₀) + f(x₀) : un point et une pente.",
           D + "secante.html?vue=equation", "La tangente en A à la courbe de x + 1/x",
           "باش نكتبو l'équation ديال droite، خاصنا نقطة و pente. نشوفو la méthode على هاد l'exemple: la courbe ديال x plus un sur x، والنقطة A فx égale deux. f de deux égale cinq demis. la pente ديال la tangente هي f prime de deux، كتساوي trois quarts: شوف المثلث الصغير. l'équation: y égale f prime de x zéro، facteur de x moins x zéro، plus f de x zéro. هنا كتعطي y égale trois quarts x plus un. وفاللخر كنتأكدو بلي A على la tangente. فالتمرين ديالك: عوض f prime de un و f de un فنفس l'équation.",
           [("(T) : y = f′(x₀)(x − x₀) + f(x₀)", "l'équation: y égale"), ("vérifier : A ∈ (T)", "كنتأكدو بلي A على la tangente")],
           [regle("باش نكتبو l'équation", a=2), jusqua("والنقطة A فx égale deux", "point_contact"),
            jusqua("شوف المثلث الصغير", "pente_tangente"), {"mot": "شوف المثلث الصغير", "repere": "triangle_pente"},
            jusqua("l'équation: y égale", "equation_generale"), montre("l'équation: y égale", "centre:0"),
            jusqua("هنا كتعطي", "equation_tangente"), jusqua("كنتأكدو بلي A على la tangente", "verification"), montre("كنتأكدو بلي A على la tangente", "centre:1")])

SIM3 = sim("ex_d1_3", "Question 3 : tangente horizontale, f′(x) = 0",
           "Là où la tangente est horizontale, sa pente f′(x) vaut 0.",
           D + "variations.html?vue=glisse", "Un point glisse sur la courbe de x³ − 3x avec sa tangente",
           "نشوفو على هاد l'exemple: la courbe ديال x au cube moins trois x. النقطة P كتزلق، و la tangente ديالها معاها. la pente ديال la tangente هي f prime de x. شوف: فx égale moins un، la tangente horizontale، ما طالعة ما هابطة: f prime de moins un égale zéro. وفx égale un، نفس الحاجة: f prime de un égale zéro. إذن باش نلقاو فين la tangente horizontale، كنحلو f prime de x égale zéro. فالتمرين ديالك: حسب f prime de x، ومن بعد حل f prime de x égale zéro.",
           [("tangente horizontale ⇔ f′(x) = 0", "كنحلو f prime de x égale zéro")],
           [jusqua("النقطة P كتزلق", "monte"), jusqua("فx égale moins un", "sommet"), {"mot": "فx égale moins un", "repere": "sommet"},
            jusqua("وفx égale un", "creux"), {"mot": "وفx égale un", "repere": "creux"}, montre("كنحلو f prime de x égale zéro", "centre:0")])

FA1 = qcm("fa_d1_1", "Plus facile : simplifier le taux", "نتمرنو بسؤال ساهل على le taux.",
          "Pour x ≠ 1, (x² + x − 2)/(x − 1) est égal à…", ["x + 1", "x + 2", "x − 2"], 1, [
              (("قريب! نشرو x moins un، fois، x plus un: كنلقاو x carré moins un، ماشي x carré plus x moins deux. عاود اختار.", "(x − 1)(x + 1) = x² − 1. Réessaie."),
               ("الجواب هو x plus deux: x moins un، fois، x plus deux، كتعطي x carré plus x moins deux.", "Réponse : x + 2, car (x − 1)(x + 2) = x² + x − 2.")),
              ("برافو! x moins un، fois، x plus deux، كتعطي x carré plus x moins deux. وملي كنبسطو، كيبقى x plus deux.", "Juste : x² + x − 2 = (x − 1)(x + 2)."),
              (("ما تقلقش. نشرو x moins un، fois، x moins deux: كنلقاو x carré moins trois x plus deux. عاود اختار.", "(x − 1)(x − 2) = x² − 3x + 2. Réessaie."),
               ("الجواب هو x plus deux. تأكد ديما بالنشر.", "Réponse : x + 2 ; vérifie toujours en développant."))],
          "Pour x différent de un, x carré plus x moins deux، sur x moins un، égale ?")

FA2 = association("fa_d1_2", "Plus facile : relier", "Relie chaque élément de la tangente en A(1 ; 0) à sa valeur.",
                  "نتمرنو: ربط كل حاجة مع القيمة ديالها.", "Relie chaque élément à sa valeur.",
                  [("1", "f(1), l'ordonnée de A"), ("2", "f′(1), la pente de (T)"), ("3", "l'équation de (T)")],
                  [("a", "0"), ("b", "3"), ("c", "y = 3x − 3"), ("d", "y = 3x")],
                  {"1": "a", "2": "b", "3": "c"},
                  {"1-a": ("Oui : f(1) = 1 + 1 − 2 = 0.", "برافو: f de un égale zéro."),
                   "1-b": ("3 est la pente f′(1), pas l'ordonnée de A. Calcule 1 + 1 − 2.", "لا، trois هي la pente. حسب un plus un moins deux."),
                   "1-c": ("C'est une équation de droite, pas un nombre.", "لا، هادي équation ديال droite، ماشي عدد."),
                   "1-d": ("C'est une équation de droite, pas un nombre.", "لا، هادي équation ديال droite، ماشي عدد."),
                   "2-a": ("0 est l'ordonnée de A ; la pente vient de la question 1.", "لا، zéro هو f de un. la pente جات من السؤال un."),
                   "2-b": ("Oui : la limite du taux vaut 3.", "برافو: la limite ديال le taux égale trois."),
                   "2-c": ("La pente est un nombre, pas une équation.", "لا، la pente عدد، ماشي équation."),
                   "2-d": ("La pente est un nombre, pas une équation.", "لا، la pente عدد، ماشي équation."),
                   "3-a": ("Il faut une équation y = …", "لا، خاصنا équation: y égale."),
                   "3-b": ("Il faut une équation y = …", "لا، خاصنا équation: y égale."),
                   "3-c": ("Oui : y = 3(x − 1) + 0 = 3x − 3.", "برافو: y égale trois x moins trois."),
                   "3-d": ("y = 3x oublie le − 3 : A(1 ; 0) n'est pas sur cette droite.", "لا، y égale trois x ما كدوزش من A. نسيتي moins trois.")},
                  ("(1 ; a) (2 ; b) (3 ; c) : (T) : y = 3x − 3.", "f de un égale zéro، la pente trois، و la tangente y égale trois x moins trois."))

FA3 = vrai_faux("fa_d1_3", "Plus facile : vrai ou faux", "f′(x) = 2x + 1.", "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة.", [
    ("La tangente est horizontale là où f′(x) = 0.", True, "Une tangente horizontale a une pente nulle, et la pente est f′(x)."),
    ("La tangente est horizontale là où f(x) = 0.", False, "f(x) = 0 donne les points sur l'axe des abscisses, pas la pente."),
    ("f′(x) = 0 pour x = −0,5.", True, "2 × (−0,5) + 1 = 0.")])

EX = {
    "id": ID, "type": "exercice", "version": 1, "status": "published",
    "matiere": "mathematiques", "chapitre": "derivation_etude_fonctions", "cours": "math_ch2_derivation_etude_fonctions",
    "titre": "Nombre dérivé et tangente à une parabole", "niveau": "facile", "duree_min": 15, "origine": ORIGINE,
    "competences": ["Montrer qu'une fonction est dérivable en un point par la limite du taux", "Écrire l'équation d'une tangente", "Trouver une tangente horizontale par f′(x) = 0"],
    "enonce": {
        "intro": "On considère la fonction f définie sur ℝ par f(x) = x² + x − 2, et (C) sa courbe représentative dans un repère orthonormé (O, i, j).",
        "intro_dit": "دابا نقراو l'énoncé. عندنا la fonction f، معرفة على R: f de x égale x carré plus x moins deux. و C هي la courbe ديالها فواحد repère orthonormé.",
        "figures": [figure("C", "x^2+x-2", 1, 0, -3, 2, -3, 4, "La courbe (C) de f(x) = x² + x − 2")],
        "donnees": ["f(x) = x² + x − 2, pour tout x réel", "A(1 ; 0) est un point de (C)"],
        "questions": [Q1, Q2, Q3]},
    "explication": deck("explication", "Explication animée", [SIM1, SIM2, SIM3]),
    "facile": deck("facile", "Plus facile, pour s'entraîner", [FA1, FA2, FA3]),
    "similaire": {"id": ID + "_b", "titre": "Même exercice, autres données", "enonce": {
        "intro": "On considère la fonction g définie sur ℝ par g(x) = x² − 2x − 3, et (C′) sa courbe ; B(3 ; 0) est un point de (C′).",
        "intro_dit": "نفس التمرين، بدالة أخرى: g de x égale x carré moins deux x moins trois، والنقطة B ديال la courbe، اللي الإحداثيات ديالها trois و zéro.",
        "figures": [figure("C′", "x^2-2*x-3", 3, 0, -2, 4, -5, 5, "La courbe (C′) de g(x) = x² − 2x − 3")],
        "donnees": ["g(x) = x² − 2x − 3", "B(3 ; 0) est un point de (C′)"],
        "questions": [
            {"id": "1", "texte": "Montrer que g est dérivable en 3 et calculer g′(3) par la limite du taux d'accroissement.",
             "reponse": valeur("g′(3)", 4, "g(3) = 0 ; (g(x) − g(3))/(x − 3) = (x − 3)(x + 1)/(x − 3) = x + 1 ; la limite en 3 vaut 4 : g′(3) = 4"),
             "clavier": {"aides": ["g(3) =", "(x − 3)(x + 1)", "lim", "g′(3) ="], "pieges": ["0/0 = 0"]},
             "correction": correction([("1 : g(3) = 9 − 6 − 3 = 0", "g de trois égale zéro"),
                                       ("(g(x) − g(3))/(x − 3) = (x − 3)(x + 1)/(x − 3) = x + 1", "x moins trois، fois، x plus un"),
                                       ("lim (x + 1) = 4 ∈ ℝ (x → 3) : g′(3) = 4", "g prime de trois égale quatre")],
                                      "g de trois égale zéro. le taux كيتفك: x moins trois، fois، x plus un، sur x moins trois، كيبقى x plus un. la limite égale quatre، إذن g est dérivable en trois، و g prime de trois égale quatre.")},
            {"id": "2", "texte": "Déterminer une équation de la tangente (T′) à (C′) au point B(3 ; 0).",
             "reponse": phrase("(T′) : y = g′(3)(x − 3) + g(3) = 4(x − 3), donc y = 4x − 12"),
             "clavier": {"aides": ["y = g′(3)(x − 3) + g(3)", "y ="], "pieges": ["y = 4x"]},
             "correction": correction([("2 : (T′) : y = g′(3)(x − 3) + g(3) = 4(x − 3) + 0", "y égale g prime de trois"),
                                       ("(T′) : y = 4x − 12", "y égale quatre x moins douze")],
                                      "y égale g prime de trois، facteur de x moins trois، plus g de trois. إذن y égale quatre x moins douze.")},
            {"id": "3", "texte": "Calculer g′(x), puis déterminer l'abscisse du point de (C′) où la tangente est horizontale.",
             "reponse": valeur("x", 1, "g′(x) = 2x − 2 ; g′(x) = 0 ⇔ x = 1"),
             "clavier": {"aides": ["g′(x) =", "g′(x) = 0", "x ="], "pieges": ["x = −1"]},
             "correction": correction([("3 : g′(x) = 2x − 2", "g prime de x égale deux x moins deux"),
                                       ("g′(x) = 0 ⇔ x = 1", "x égale un")],
                                      "g prime de x égale deux x moins deux. la tangente horizontale ملي g prime de x égale zéro، يعني x égale un.")}]}}
}
ecrire(EX)
