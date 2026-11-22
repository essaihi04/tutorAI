# Exercice de maths, ch. 2 (dérivation et étude des fonctions), niveau MOYEN (le niveau du national) :
# dérivabilité à droite en 0 d'une fonction avec √x, demi-tangente verticale et son sens, « montrer que f′(x) = … »,
# tableau de variations, valeur minimale, tangente.
# Sources comparées (lecture seule, rien de copié) :
#  - exploration/derivation_etude_fonctions.json : cas types derivabilite_droite_gauche, interpretation_taux,
#    montrer_derivee, signe_derivee_variations, extremum_inegalite, tangente_equation ; pièges « sens de la demi-tangente
#    récité à l'envers », « limite infinie : écrire dérivable », « (√u)′ sans u′ » ; erreurs_examen 2021 N, 2022 R.
#  - vidéos des profs (Timath : exercice type contrôle avec demi-tangente à droite ; Prof fati : mini-dessin par cas ;
#    Math & Phys : demi-tangentes rédigées ; Ishaq Ghanem : « donnez l'équation »).
#  - nationaux 2021 N (3.a, 8.b), 2022 R (2.b), 2023 R (2.a-2.c) : dérivabilité à droite en 0 et interprétation
#    (fonctions avec ln, non reprises).
#  - séries en ligne repérées (titres et résumés de recherche ; sites non joignables depuis la session) : talamidi
#    exercices non corrigés 2-3, Lycée Mohammed Serraj (monstremath), devoirs Hammouda (scribd : continuité et
#    dérivabilité), cours Atmani (moutamadris) : x√x ou (x − a)√x en 0 est la situation classique des contrôles.
# Différent de l'exemple du cours (x√(x + 1), vue trace « etude_pas ») : ici (x − 3)√x, minimum entier.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa

D = "/media/simulations/maths/derivation-tableau/"
ID = "math_ex_ch2_derivation_3"


def figure(nom, expr, xmax, ymin, ymax, titre):
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": -0.5, "max": xmax, "nom": "x", "graduations": list(range(1, int(xmax) + 1))},
                     "y": {"min": ymin, "max": ymax, "nom": "y", "graduations": list(range(int(ymin) + 1, int(ymax) + 1))}},
            "legende": f"Allure de ({nom}) sur [0 ; +∞[ : chaque propriété vue sur le dessin est à justifier par le calcul.",
            "elements": [{"f": "courbe", "expr": expr, "de": 0, "a": xmax, "couleur": "cyan", "texte": f"({nom})", "texte_x": xmax - 0.5, "pos": "no"},
                         {"f": "point", "at": [0, 0], "couleur": "jaune", "t": "O", "pos": "no"}]}


Q1 = {"id": "1", "texte": "Calculer lim (f(x) − f(0))/x quand x → 0⁺. La fonction f est-elle dérivable à droite en 0 ? Interpréter géométriquement le résultat.",
      "texte_dit": "السؤال un: حسب la limite ديال f de x moins f de zéro، sur x، quand x tend vers zéro plus. واش f dérivable à droite en zéro؟ ومن بعد interpréter géométriquement le résultat.",
      "reponse": phrase("f(0) = 0 ; pour x > 0 : (f(x) − f(0))/x = (x − 3)√x/x = (x − 3)/√x ; x − 3 → −3 et √x → 0⁺, donc la limite est −∞. f n'est pas dérivable à droite en 0 ; (C) admet au point O une demi-tangente verticale dirigée vers le bas."),
      "clavier": {"aides": ["(x − 3)√x/x = (x − 3)/√x", "√x → 0⁺", "−∞", "n'est pas dérivable à droite en 0", "demi-tangente verticale", "dirigée vers le bas"], "pieges": ["tangente verticale", "dirigée vers le haut", "f est dérivable"]},
      "aides": [aide("f(0) = 0. Simplifie le taux : x = √x × √x, donc √x/x = 1/√x.",
                     "f de zéro égale zéro. simplifie le taux: x هو racine de x، fois، racine de x. إذن racine de x sur x، égale un sur racine de x."),
                aide("Écris vers quoi tend le haut (x − 3) et le bas (√x) avant de conclure. Une limite infinie n'est pas un nombre réel : pense à la demi-tangente verticale et à son sens.",
                     "كتب لاش كيمشي الفوق، x moins trois، و لاش كيمشي التحت، racine de x، قبل ما تجاوب. l'infini ماشي عدد حقيقي: فكر ف la demi-tangente verticale و الاتجاه ديالها.")],
      "correction": correction([
          ("1 : f(0) = 0 et, pour x > 0, (f(x) − f(0))/x = (x − 3)√x/x = (x − 3)/√x", "f de zéro égale zéro"),
          ("x − 3 → −3 et √x → 0⁺ quand x → 0⁺, donc lim (f(x) − f(0))/x = −∞", "la limite égale moins l'infini"),
          ("donc f n'est pas dérivable à droite en 0", "f n'est pas dérivable à droite en zéro"),
          ("(C) admet au point O une demi-tangente verticale dirigée vers le bas", "dirigée vers le bas")],
          "السؤال un. f de zéro égale zéro. le taux هو x moins trois، fois racine de x، sur x، يعني x moins trois، sur racine de x. الفوق كيمشي ل moins trois، والتحت كيمشي ل zéro plus. إذن la limite égale moins l'infini. l'infini ماشي عدد حقيقي، إذن f n'est pas dérivable à droite en zéro. والتفسير: la courbe عندها فالنقطة O، une demi-tangente verticale، dirigée vers le bas، حيت على اليمين ديال O، la courbe تحت."),
      "explication": "ex_d3_1", "facile": "fa_d3_1"}

Q2 = {"id": "2", "texte": "Montrer que pour tout x de ]0 ; +∞[ : f′(x) = 3(x − 1)/(2√x).",
      "texte_dit": "السؤال deux: بين بلي لكل x من zéro، plus l'infini: f prime de x égale trois، facteur de x moins un، sur deux racine de x.",
      "reponse": phrase("f est dérivable sur ]0 ; +∞[ ; f = u·v avec u = x − 3, v = √x : f′(x) = 1 × √x + (x − 3) × 1/(2√x) = (2x + x − 3)/(2√x) = (3x − 3)/(2√x) = 3(x − 1)/(2√x)."),
      "clavier": {"aides": ["(u·v)′ = u′v + uv′", "(√x)′ = 1/(2√x)", "(2x + x − 3)/(2√x)", "3(x − 1)"], "pieges": ["f′(x) = 1 × 1/(2√x)", "(√x)′ = 1/√x"]},
      "aides": [aide("f est un produit : u(x) = x − 3 et v(x) = √x. Rappelle-toi (u·v)′ = u′v + uv′ et (√x)′ = 1/(2√x).",
                     "f هي produit: u égale x moins trois، و v égale racine de x. تفكر: u prime v، plus u v prime، و la dérivée ديال racine de x هي un sur deux racine de x."),
                aide("Mets tout sur le dénominateur 2√x : √x = 2x/(2√x). Puis factorise le numérateur par 3.",
                     "حط كلشي على نفس le dénominateur، deux racine de x: racine de x égale deux x sur deux racine de x. ومن بعد خرج trois facteur فالفوق.")],
      "correction": correction([
          ("2 : f est dérivable sur ]0 ; +∞[ et f′(x) = 1 × √x + (x − 3) × 1/(2√x)", "u prime v، plus u v prime"),
          ("= (2x + x − 3)/(2√x) = (3x − 3)/(2√x)", "نفس le dénominateur"),
          ("donc f′(x) = 3(x − 1)/(2√x)", "trois، facteur de x moins un")],
          "السؤال deux. f dérivable sur zéro، plus l'infini، وهي produit. f prime de x égale، u prime v، plus u v prime: un fois racine de x، plus، x moins trois، fois un sur deux racine de x. كنحطو كلشي على نفس le dénominateur، deux racine de x: الفوق كيولي deux x plus x moins trois، يعني trois x moins trois. كنخرجو trois facteur: f prime de x égale، trois، facteur de x moins un، sur deux racine de x."),
      "explication": "ex_d3_2", "facile": "fa_d3_2"}

Q3 = {"id": "3", "texte": "Sachant que lim f(x) = +∞ quand x → +∞, étudier le signe de f′(x) et dresser le tableau de variations de f.",
      "texte_dit": "السؤال trois: عارفين بلي la limite ديال f de x، quand x tend vers plus l'infini، égale plus l'infini. درس le signe ديال f prime de x، ودير le tableau de variations.",
      "reponse": phrase("2√x > 0 : f′(x) a le signe de x − 1 : négatif sur ]0 ; 1[, positif sur ]1 ; +∞[. f est strictement décroissante sur [0 ; 1] et strictement croissante sur [1 ; +∞[ ; f(0) = 0, f(1) = −2, lim f = +∞ en +∞."),
      "clavier": {"aides": ["2√x > 0", "le signe de f′(x) est le signe de x − 1", "f(1) = −2", "f(0) = 0", "+∞"], "pieges": ["f(1) = 2", "f croissante sur [0 ; 1]"]},
      "aides": [aide("Dans f′(x) = 3(x − 1)/(2√x), quels facteurs sont toujours positifs sur ]0 ; +∞[ ?",
                     "ف f prime de x، شنو هوما les facteurs اللي ديما positifs sur zéro، plus l'infini؟"),
                aide("Le signe vient de x − 1. Calcule f(0) et f(1) pour écrire les valeurs au bout des flèches.",
                     "le signe جاي من x moins un. حسب f de zéro و f de un باش تكتب القيم فالراس ديال les flèches.")],
      "correction": correction([
          ("3 : 3 > 0 et 2√x > 0, donc le signe de f′(x) est le signe de x − 1", "le signe ديال x moins un"),
          ("f′(x) < 0 sur ]0 ; 1[ et f′(x) > 0 sur ]1 ; +∞[", "négatif قبل un"),
          ("f(0) = 0 ; f(1) = (1 − 3) × 1 = −2", "f de un égale moins deux"),
          ("x : 0 ↘ 1 ↗ +∞ ;  f : 0 ↘ −2 ↗ +∞", "le tableau")],
          "السؤال trois. trois positif، و deux racine de x positif، إذن le signe ديال f prime de x هو le signe ديال x moins un. négatif قبل un، و positif من بعد. f de zéro égale zéro، و f de un égale moins deux. le tableau: f décroissante من zéro حتى moins deux، ومن بعد croissante حتى plus l'infini."),
      "explication": "ex_d3_3", "facile": "fa_d3_3"}

Q4 = {"id": "4", "texte": "En déduire la valeur minimale de f sur [0 ; +∞[, puis montrer que pour tout x ≥ 0 : (x − 3)√x ≥ −2.",
      "texte_dit": "السؤال quatre: استنتج la valeur minimale ديال f sur zéro، plus l'infini، ومن بعد بين بلي لكل x positif: x moins trois، fois racine de x، supérieur ou égal à moins deux.",
      "reponse": valeur("valeur minimale", -2, "f est décroissante puis croissante, le minimum est atteint en 1 : la valeur minimale est f(1) = −2 ; donc pour tout x ≥ 0, f(x) ≥ f(1), soit (x − 3)√x ≥ −2 ; min = −2"),
      "clavier": {"aides": ["f(x) ≥ f(1)", "valeur minimale", "= −2"], "pieges": ["minimum = 1", "f(0) = 0"]},
      "aides": [aide("Dans le tableau, où se trouve la valeur la plus basse ?", "فالتابلو، فين كاينة أصغر قيمة؟"),
                aide("La valeur minimale m vérifie f(x) ≥ m pour tout x du domaine : remplace f(x) par son expression.",
                     "la valeur minimale m: f de x supérieur ou égal à m لكل x. عوض f de x بالتعبير ديالها.")],
      "correction": correction([
          ("4 : d'après le tableau, f admet en 1 un minimum : f(1) = −2", "le minimum égale moins deux"),
          ("donc pour tout x ≥ 0 : f(x) ≥ f(1)", "f de x supérieur ou égal à f de un"),
          ("c'est-à-dire (x − 3)√x ≥ −2", "supérieur ou égal à moins deux")],
          "السؤال quatre. من le tableau، f عندها minimum ف un، و le minimum égale moins deux. إذن لكل x positif، f de x supérieur ou égal à f de un، يعني، x moins trois، fois racine de x، supérieur ou égal à moins deux."),
      "explication": "ex_d3_4", "facile": "fa_d3_4"}

Q5 = {"id": "5", "texte": "Déterminer une équation de la tangente (T) à (C) au point A d'abscisse 3.",
      "texte_dit": "السؤال cinq: لقا l'équation ديال la tangente T ل la courbe، فالنقطة A اللي l'abscisse ديالها trois.",
      "reponse": phrase("f(3) = 0 ; f′(3) = 3 × 2/(2√3) = 3/√3 = √3 ; (T) : y = f′(3)(x − 3) + f(3) = √3(x − 3), soit y = √3 x − 3√3."),
      "clavier": {"aides": ["y = f′(3)(x − 3) + f(3)", "f(3) = 0", "f′(3) = √3", "y ="], "pieges": ["f′(3) = 3", "y = √3 x"]},
      "aides": [aide("Calcule f(3) puis f′(3) avec la question 2.", "حسب f de trois، ومن بعد f prime de trois بالسؤال deux."),
                aide("3/√3 = √3 (multiplie haut et bas par √3). Puis applique y = f′(3)(x − 3) + f(3).",
                     "trois sur racine de trois، égale racine de trois. ومن بعد طبق: y égale f prime de trois، facteur de x moins trois، plus f de trois.")],
      "correction": correction([
          ("5 : f(3) = 0 ; f′(3) = 3 × 2/(2√3) = √3", "f prime de trois égale racine de trois"),
          ("(T) : y = f′(3)(x − 3) + f(3) = √3(x − 3)", "y égale f prime de trois"),
          ("(T) : y = √3 x − 3√3", "y égale racine de trois x moins trois racine de trois")],
          "السؤال cinq. f de trois égale zéro. f prime de trois égale trois fois deux، sur deux racine de trois. إذن f prime de trois égale racine de trois. l'équation: y égale f prime de trois، facteur de x moins trois، plus f de trois. إذن y égale racine de trois x moins trois racine de trois."),
      "explication": "ex_d3_5", "facile": "fa_d3_5"}

SIM1 = sim("ex_d3_1", "Question 1 : limite infinie du taux, demi-tangente verticale",
           "Une limite infinie : non dérivable ; la demi-tangente verticale part du côté de la courbe.",
           D + "demi-tangentes.html?vue=sens", "Les quatre cas de demi-tangente verticale",
           "ملي la limite ديال le taux كتكون infinie، l'infini ماشي عدد حقيقي: f n'est pas dérivable. ولكن la courbe عندها demi-tangente verticale. شوف les quatre cas. الأول: على اليمين، و le taux كيمشي ل plus l'infini: la courbe فوق النقطة، la flèche طالعة. التاني: على اليمين، و le taux كيمشي ل moins l'infini: la courbe تحت، la flèche هابطة. التالت والرابع: على اليسار، كيتقلب. القاعدة: la demi-tangente كتمشي فالجهة فين كاينة la courbe. فالتمرين ديالك: حنا على اليمين ديال zéro، شوف la limite ديال le taux واش plus ولا moins l'infini.",
           [("limite infinie ⇒ non dérivable", "l'infini ماشي عدد حقيقي"), ("à droite, −∞ : vers le bas", "التاني"), ("la demi-tangente part du côté de la courbe", "القاعدة")],
           [montre("l'infini ماشي عدد حقيقي", "centre:0"), jusqua("الأول", "droite_plus_infini"), {"mot": "الأول", "repere": "cas_dp"},
            jusqua("التاني", "droite_moins_infini"), {"mot": "التاني", "repere": "cas_dm"}, montre("التاني", "centre:1"),
            jusqua("التالت والرابع", "gauche_moins_infini"), jusqua("القاعدة", "regle"), {"mot": "القاعدة", "repere": "regle"}, montre("القاعدة", "centre:2")])

SIM2 = sim("ex_d3_2", "Question 2 : montrer que f′(x) = …",
           "Produit u·v, même dénominateur, puis la forme demandée.",
           D + "calculs.html?vue=dv6", "La méthode écrite au tableau sur x√(x + 1)",
           "نشوفو la méthode على هاد l'exemple ديال الدرس: f de x égale x، fois racine de x plus un. أول سطر: f dérivable، والمجال. من بعد le produit: u prime v، plus u v prime. من بعد نفس le dénominateur، deux racine de x plus un. وفاللخر كنوصلو بالضبط للشكل اللي طلب السؤال: trois x plus deux، sur deux racine de x plus un. فالتمرين ديالك نفس الشي: u égale x moins trois، و v égale racine de x.",
           [("(u·v)′ = u′v + uv′", "le produit"), ("tout sur 2√… puis la forme demandée", "نفس le dénominateur")],
           [jusqua("أول سطر", "derivable"), jusqua("le produit", "produit"), montre("le produit", "centre:0"),
            jusqua("نفس le dénominateur", "meme_denominateur"), montre("نفس le dénominateur", "centre:1"), jusqua("وفاللخر كنوصلو", "forme")])

SIM3 = sim("ex_d3_3", "Question 3 : le signe de f′, puis les flèches",
           "On écarte les facteurs positifs ; le signe vient d'un seul facteur.",
           D + "trace.html?vue=etude_pas&depart=derivee", "L'étude de x√(x + 1) au tableau, une étape à la fois",
           "نشوفو على هاد l'exemple: f prime de x، égale trois x plus deux، sur deux racine de x plus un. التحت ديما positif، إذن le signe ديال f prime هو le signe ديال trois x plus deux. شوف السطر ديال f prime: moins، zéro ف moins deux tiers، ومن بعد plus. والسطر ديال f: كتهبط حتى le minimum، ومن بعد كتطلع حتى plus l'infini. فالتمرين ديالك: شوف شنو هو الفاكتور اللي كيبدل le signe.",
           [("dénominateur > 0 : f′ a le signe du numérateur", "التحت ديما positif"), ("− puis + : minimum", "والسطر ديال f")],
           [montre("التحت ديما positif", "centre:0"), jusqua("التحت ديما positif", "signe_phrase"), jusqua("شوف السطر ديال f prime", "ligne_signe"),
            jusqua("والسطر ديال f", "fleches"), montre("والسطر ديال f", "centre:1")])

SIM4 = sim("ex_d3_4", "Question 4 : du minimum à l'inégalité",
           "Le minimum lu dans le tableau donne une inégalité pour tout x.",
           D + "minimum.html?vue=minimum", "x + 1/x : le minimum 2, la droite y = 2 sous la courbe",
           "نشوفو على هاد l'exemple: f de x égale x plus un sur x، sur zéro، plus l'infini. la fonction كتهبط حتى deux، ومن بعد كتطلع. إذن deux هو le minimum، ف un. لكل x positif، f de x supérieur ou égal à deux. كنعوضو f de x بالتعبير ديالها، وكنلقاو l'inégalité. فالتمرين ديالك: قرا le minimum فالتابلو، ومن بعد كتب نفس الجملة.",
           [("min f = f(x₀) ⇒ f(x) ≥ f(x₀) pour tout x", "لكل x positif")],
           [jusqua("نشوفو على هاد l'exemple", "tableau"), jusqua("la fonction كتهبط", "descend"), jusqua("ومن بعد كتطلع", "monte"),
            jusqua("إذن deux هو le minimum", "minimum"), jusqua("لكل x positif", "inegalite"), montre("لكل x positif", "centre:0"),
            jusqua("كنعوضو f de x", "conclusion")])

SIM5 = sim("ex_d3_5", "Question 5 : la tangente en un point",
           "Un point A(x₀ ; f(x₀)) et une pente f′(x₀).",
           D + "secante.html?vue=equation", "La tangente en A à la courbe de x + 1/x",
           "نشوفو la méthode على هاد l'exemple: la courbe ديال x plus un sur x، و A فx égale deux. f de deux égale cinq demis، و f prime de deux égale trois quarts. l'équation: y égale f prime de x zéro، facteur de x moins x zéro، plus f de x zéro. كتعطي y égale trois quarts x plus un. فالتمرين ديالك: x zéro égale trois، حسب f de trois و f prime de trois.",
           [("(T) : y = f′(x₀)(x − x₀) + f(x₀)", "l'équation")],
           [regle("نشوفو la méthode", a=2), jusqua("و A فx égale deux", "point_contact"), jusqua("و f prime de deux", "pente_tangente"),
            jusqua("l'équation", "equation_generale"), montre("l'équation", "centre:0"), jusqua("كتعطي", "equation_tangente")])

FA1 = qcm("fa_d3_1", "Plus facile : le sens de la demi-tangente", "سؤال ساهل على la demi-tangente.",
          "À droite de O, le taux tend vers −∞. La demi-tangente verticale en O est dirigée…", ["vers le haut", "vers le bas", "on ne peut pas savoir"], 1, [
              (("قريب! vers le haut كتكون ملي le taux كيمشي ل plus l'infini على اليمين. هنا moins l'infini. عاود اختار.", "Vers le haut : à droite avec +∞. Ici −∞. Réessaie."),
               ("الجواب: vers le bas. على اليمين و moins l'infini، la courbe تحت O.", "Réponse : vers le bas.")),
              ("برافو! على اليمين، و le taux كيمشي ل moins l'infini: la courbe تحت O، la demi-tangente vers le bas.", "Juste : à droite, −∞ : vers le bas."),
              (("ما تقلقش، كنقدرو نعرفو: le côté و le signe ديال l'infini كيعطيو الاتجاه. عاود اختار.", "Le côté et le signe de l'infini donnent le sens. Réessaie."),
               ("الجواب: vers le bas. القاعدة: la demi-tangente كتمشي فالجهة فين كاينة la courbe.", "Réponse : vers le bas."))],
          "À droite de O, le taux tend vers moins l'infini. La demi-tangente est dirigée ?")

FA2 = qcm("fa_d3_2", "Plus facile : la dérivée d'un produit", "نتمرنو على la dérivée ديال produit.",
          "La dérivée de (x − 3)√x est…", ["1 × 1/(2√x)", "√x + (x − 3)/(2√x)", "√x + (x − 3)/√x"], 1, [
              (("قريب! la dérivée ديال produit ماشي produit ديال les dérivées. عاود اختار.", "(u·v)′ ≠ u′·v′. Réessaie."),
               ("الجواب: u prime v، plus u v prime، يعني racine de x، plus، x moins trois sur deux racine de x.", "Réponse : √x + (x − 3)/(2√x).")),
              ("برافو! u prime v، plus u v prime.", "Juste : (u·v)′ = u′v + uv′."),
              (("قريب! la dérivée ديال racine de x هي un sur deux racine de x، نسيتي deux. عاود اختار.", "(√x)′ = 1/(2√x) : il manque le 2. Réessaie."),
               ("الجواب: racine de x، plus، x moins trois sur deux racine de x.", "Réponse : √x + (x − 3)/(2√x)."))],
          "La dérivée de x moins trois، fois racine de x، est ?")

FA3 = association("fa_d3_3", "Plus facile : signe et sens", "Relie chaque intervalle à ce qui s'y passe.",
                  "نتمرنو: ربط كل intervalle مع le signe ديال f prime.", "Relie chaque intervalle au signe de f′.",
                  [("1", "]0 ; 1["), ("2", "]1 ; +∞[")],
                  [("a", "f′ < 0 : f décroissante"), ("b", "f′ > 0 : f croissante"), ("c", "f′ = 0 partout")],
                  {"1": "a", "2": "b"},
                  {"1-a": ("Oui : x − 1 < 0 sur ]0 ; 1[.", "برافو: x moins un négatif قبل un."),
                   "1-b": ("Teste x = 0,25 : x − 1 = −0,75 < 0.", "لا، جرب x égale zéro virgule vingt-cinq: x moins un négatif."),
                   "1-c": ("f′ ne s'annule qu'en 1.", "لا، f prime، s'annule en un فقط."),
                   "2-a": ("Teste x = 4 : x − 1 = 3 > 0.", "لا، جرب x égale quatre: x moins un positif."),
                   "2-b": ("Oui : x − 1 > 0 après 1.", "برافو: من بعد un، x moins un positif."),
                   "2-c": ("f′ ne s'annule qu'en 1.", "لا، f prime، s'annule en un فقط.")},
                  ("(1 ; a) (2 ; b) : f descend jusqu'à f(1) = −2, puis monte.", "f هابطة حتى moins deux، ومن بعد طالعة."))

FA4 = vrai_faux("fa_d3_4", "Plus facile : vrai ou faux", "Le minimum de f sur [0 ; +∞[ est f(1) = −2.", "سؤال ساهل: صحيح ولا غالط؟", [
    ("Pour tout x ≥ 0, f(x) ≥ −2.", True, "−2 est la plus petite valeur prise par f."),
    ("Le minimum de f est atteint en x = −2.", False, "Le minimum est atteint en x = 1 ; sa valeur est −2."),
    ("Pour tout x ≥ 0, f(x) ≥ 0.", False, "f(1) = −2 < 0.")])

FA5 = qcm("fa_d3_5", "Plus facile : simplifier f′(3)", "سؤال ساهل على f prime de trois.",
          "f′(3) = 3 × 2/(2√3) est égal à…", ["3", "√3", "1/√3"], 1, [
              (("قريب! نسيتي racine de trois فالتحت. عاود اختار.", "Il reste √3 au dénominateur. Réessaie."),
               ("الجواب: racine de trois، حيت trois sur racine de trois، égale racine de trois.", "Réponse : √3.")),
              ("برافو! trois sur racine de trois، égale racine de trois.", "Juste : 3/√3 = √3."),
              (("ما تقلقش. trois sur racine de trois ماشي un sur racine de trois. عاود اختار.", "3/√3 ≠ 1/√3. Réessaie."),
               ("الجواب: racine de trois. ضرب الفوق والتحت ف racine de trois.", "Réponse : √3."))],
          "f prime de trois est égal à ?")

EX = {
    "id": ID, "type": "exercice", "version": 1, "status": "published",
    "matiere": "mathematiques", "chapitre": "derivation_etude_fonctions", "cours": "math_ch2_derivation_etude_fonctions",
    "titre": "Une fonction avec √x : demi-tangente, variations, minimum", "niveau": "moyen", "duree_min": 30, "origine": ORIGINE,
    "competences": ["Étudier la dérivabilité à droite et interpréter géométriquement", "Montrer que f′(x) = une forme donnée", "Dresser un tableau de variations", "Déduire une inégalité du minimum", "Écrire l'équation d'une tangente"],
    "enonce": {
        "intro": "On considère la fonction f définie sur [0 ; +∞[ par f(x) = (x − 3)√x, et (C) sa courbe représentative dans un repère orthonormé (O, i, j).",
        "intro_dit": "دابا نقراو l'énoncé. f معرفة sur zéro، plus l'infini: f de x égale، x moins trois، fois racine de x. و C هي la courbe ديالها.",
        "figures": [figure("C", "(x-3)*sqrt(x)", 5, -3, 5, "Allure de (C) : f(x) = (x − 3)√x")],
        "donnees": ["f(x) = (x − 3)√x pour x ≥ 0", "lim f(x) = +∞ quand x → +∞"],
        "questions": [Q1, Q2, Q3, Q4, Q5]},
    "explication": deck("explication", "Explication animée", [SIM1, SIM2, SIM3, SIM4, SIM5]),
    "facile": deck("facile", "Plus facile, pour s'entraîner", [FA1, FA2, FA3, FA4, FA5]),
    "similaire": {"id": ID + "_b", "titre": "Même exercice, autres données", "enonce": {
        "intro": "On considère la fonction g définie sur [0 ; +∞[ par g(x) = (x − 6)√x, et (C′) sa courbe ; on admet que lim g(x) = +∞ quand x → +∞.",
        "intro_dit": "نفس التمرين، بدالة أخرى: g de x égale، x moins six، fois racine de x، sur zéro، plus l'infini.",
        "figures": [figure("C′", "(x-6)*sqrt(x)", 8, -6, 6, "Allure de (C′) : g(x) = (x − 6)√x")],
        "donnees": ["g(x) = (x − 6)√x pour x ≥ 0", "lim g(x) = +∞ quand x → +∞"],
        "questions": [
            {"id": "1", "texte": "Calculer lim (g(x) − g(0))/x quand x → 0⁺ ; g est-elle dérivable à droite en 0 ? Interpréter.",
             "reponse": phrase("(g(x) − g(0))/x = (x − 6)/√x → −∞ : g n'est pas dérivable à droite en 0 ; demi-tangente verticale en O dirigée vers le bas."),
             "clavier": {"aides": ["(x − 6)/√x", "−∞", "demi-tangente verticale"], "pieges": ["dirigée vers le haut"]},
             "correction": correction([("1 : (g(x) − g(0))/x = (x − 6)/√x → −∞ (x → 0⁺)", "la limite égale moins l'infini"),
                                       ("g n'est pas dérivable à droite en 0 : demi-tangente verticale en O, dirigée vers le bas", "dirigée vers le bas")],
                                      "le taux هو x moins six، sur racine de x، و la limite égale moins l'infini. إذن g n'est pas dérivable à droite en zéro، و la courbe عندها ف O، une demi-tangente verticale، dirigée vers le bas.")},
            {"id": "2", "texte": "Montrer que pour tout x > 0 : g′(x) = 3(x − 2)/(2√x).",
             "reponse": phrase("g′(x) = √x + (x − 6)/(2√x) = (2x + x − 6)/(2√x) = 3(x − 2)/(2√x)."),
             "clavier": {"aides": ["u′v + uv′", "(3x − 6)/(2√x)"], "pieges": ["(√x)′ = 1/√x"]},
             "correction": correction([("2 : g′(x) = √x + (x − 6)/(2√x) = (3x − 6)/(2√x) = 3(x − 2)/(2√x)", "trois، facteur de x moins deux")],
                                      "g prime de x égale racine de x، plus، x moins six، sur deux racine de x. على نفس le dénominateur: trois x moins six، يعني trois، facteur de x moins deux، sur deux racine de x.")},
            {"id": "3", "texte": "Étudier le signe de g′(x) et dresser le tableau de variations de g.",
             "reponse": phrase("g′ a le signe de x − 2 : g décroissante sur [0 ; 2], croissante sur [2 ; +∞[ ; g(0) = 0, g(2) = −4√2, lim +∞."),
             "clavier": {"aides": ["le signe de x − 2", "g(2) = −4√2"], "pieges": ["g(2) = 4√2"]},
             "correction": correction([("3 : g′(x) a le signe de x − 2 : − sur ]0 ; 2[, + sur ]2 ; +∞[", "le signe ديال x moins deux"),
                                       ("g(2) = −4√2 ; g : 0 ↘ −4√2 ↗ +∞", "g de deux égale moins quatre racine de deux")],
                                      "le signe ديال g prime هو le signe ديال x moins deux. g de deux égale moins quatre racine de deux. g décroissante من zéro حتى moins quatre racine de deux، ومن بعد croissante حتى plus l'infini.")},
            {"id": "4", "texte": "En déduire la valeur minimale de g sur [0 ; +∞[ (valeur exacte et valeur approchée à 10⁻² près).",
             "reponse": valeur("valeur minimale", -5.657, "la valeur minimale est g(2) = −4√2 ≈ −5,66", tolerance=0.003),
             "clavier": {"aides": ["g(2) = −4√2", "≈"], "pieges": ["−4"]},
             "correction": correction([("4 : valeur minimale g(2) = −4√2 ≈ −5,66 ; pour tout x ≥ 0, (x − 6)√x ≥ −4√2", "la valeur minimale égale moins quatre racine de deux")],
                                      "la valeur minimale égale moins quatre racine de deux، يعني environ moins cinq virgule soixante-six.")},
            {"id": "5", "texte": "Déterminer une équation de la tangente à (C′) au point d'abscisse 6.",
             "reponse": phrase("g(6) = 0 ; g′(6) = 3 × 4/(2√6) = 6/√6 = √6 ; y = √6(x − 6), soit y = √6 x − 6√6."),
             "clavier": {"aides": ["y = g′(6)(x − 6) + g(6)", "g′(6) = √6"], "pieges": ["y = √6 x"]},
             "correction": correction([("5 : g(6) = 0 ; g′(6) = √6", "g prime de six égale racine de six"),
                                       ("y = √6(x − 6) = √6 x − 6√6", "y égale racine de six x moins six racine de six")],
                                      "g de six égale zéro، و g prime de six égale racine de six. إذن y égale racine de six x moins six racine de six.")}]}}
}
ecrire(EX)
