# Exercice de maths, ch. 2 (dérivation et étude des fonctions), niveau DIFFICILE (« Supérieur » : au-dessus du national,
# même forme : problème en deux parties). Partie I : fonction auxiliaire g, solution unique α, encadrement, signe de g.
# Partie II : f(x) = (x³ + 1)/(x² + 1), « montrer que f′(x) = x·g(x)/(x² + 1)² », tableau avec deux facteurs de signe,
# f(α) exprimé avec la relation α³ = 2 − 3α, asymptote oblique et position relative.
# Sources comparées (lecture seule, rien de copié) :
#  - exploration/derivation_etude_fonctions.json : cas types fonction_auxiliaire (9 sujets sur 20), montrer_derivee,
#    signe_derivee_variations, asymptote_oblique_donnee, position_relative ; pièges « signe à vue », « limite de f(x) − y
#    au lieu de son signe » ; erreurs_examen (tableau incomplet, « vérifier que » circulaire).
#  - vidéos des profs (Math_houara : exercice complet ; Ishaq Ghanem : correction du national 2024 ; Mouad Tahiri :
#    résumé ; Timath : préparer le contrôle).
#  - nationaux 2016 R, 2017 N, 2018 N, 2018 R, 2020 R (partie I « soit g… », signe de g, puis f′ = g/…), 2024 N
#    (α et f(α)) : fonctions ln/exp, non reprises ; ici le schéma du problème est rejoué avec une fraction rationnelle.
#  - séries en ligne repérées (titres et résumés de recherche ; sites non joignables depuis la session) : talamidi série 1
#    et exercices non corrigés 2-3, Lycée Mohammed Serraj (monstremath), devoirs Hammouda (scribd), alloschool
#    (fonctions rationnelles) : la fonction auxiliaire polynomiale de degré 3 est classique aux contrôles.
# Différent des exemples du cours (x³ + x − 1 pour l'unicité, 2x³ − 3x² + 2 et x² − 3x − 2/x pour l'auxiliaire).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa

D = "/media/simulations/maths/derivation-tableau/"
C = D + "calculs.html?vue="
ID = "math_ex_ch2_derivation_7"


def figure(nom, expr, xmin, xmax, ymin, ymax, titre):
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": xmin, "max": xmax, "nom": "x", "graduations": list(range(int(xmin) + 1, int(xmax) + 1))},
                     "y": {"min": ymin, "max": ymax, "nom": "y", "graduations": list(range(int(ymin) + 1, int(ymax) + 1))}},
            "legende": f"Allure de ({nom}) et de la droite (Δ) : y = x (pointillé) ; les propriétés vues sont à justifier.",
            "elements": [{"f": "courbe", "expr": expr, "de": xmin, "a": xmax, "couleur": "cyan", "texte": f"({nom})", "texte_x": xmax - 0.6, "pos": "no"},
                         {"f": "courbe", "expr": "x", "de": xmin, "a": xmax, "couleur": "violet", "trait": "pointille", "texte": "(Δ)", "texte_x": xmin + 0.6, "pos": "se"}]}


Q1 = {"id": "1", "texte": "Partie I. Étudier les variations de g sur ℝ, puis montrer que l'équation g(x) = 0 admet une solution unique α dans ℝ, et que 0 < α < 1.",
      "texte_dit": "الجزء الأول، السؤال un: درس les variations ديال g sur R، ومن بعد بين بلي l'équation g de x égale zéro، عندها حل واحد α، و α بين zéro و un.",
      "reponse": phrase("g′(x) = 3x² + 3 > 0 : g est continue et strictement croissante sur ℝ, de −∞ (en −∞) à +∞ (en +∞). g(0) = −2 < 0 et g(1) = 2 > 0 : d'après le TVI (g continue et strictement monotone), g(x) = 0 admet une solution unique α dans ℝ, et α ∈ ]0 ; 1[."),
      "clavier": {"aides": ["g′(x) = 3x² + 3 > 0", "continue et strictement croissante", "g(0) = −2", "g(1) = 2", "g(0) × g(1) < 0", "solution unique α"], "pieges": ["g′(x) = 3x²", "α = 0,5"]},
      "aides": [aide("Dérive g : 3x² + 3 est toujours positif. Que dire alors du sens de variation de g ?",
                     "derive g: trois x carré plus trois ديما positif. شنو كتقول على les variations ديال g؟"),
                aide("Calcule g(0) et g(1) : de signes contraires. Continue + strictement monotone + changement de signe : une seule solution.",
                     "حسب g de zéro و g de un: عندهم signes contraires. continue، و strictement monotone، و le signe كيتبدل: حل واحد فقط.")],
      "correction": correction([
          ("1 : g′(x) = 3x² + 3 > 0 : g est strictement croissante sur ℝ", "trois x carré plus trois"),
          ("lim g(x) = −∞ (x → −∞) ; lim g(x) = +∞ (x → +∞)", "moins l'infini"),
          ("g est continue et strictement croissante sur [0 ; 1], g(0) = −2 et g(1) = 2 : g(0) × g(1) < 0", "g de zéro égale moins deux"),
          ("donc g(x) = 0 admet une solution unique α dans ℝ, et 0 < α < 1", "solution unique")],
          "السؤال un. g prime de x égale trois x carré plus trois، ديما positive: g strictement croissante sur R، من moins l'infini حتى plus l'infini. g de zéro égale moins deux، و g de un égale deux: signes contraires. g continue et strictement croissante، إذن l'équation g de x égale zéro عندها une solution unique α، و α بين zéro و un."),
      "explication": "ex_d7_1", "facile": "fa_d7_1"}

Q2 = {"id": "2", "texte": "Vérifier que 0,5 < α < 0,6, puis en déduire le signe de g(x) sur ℝ.",
      "texte_dit": "السؤال deux: تحقق بلي α بين zéro virgule cinq و zéro virgule six، ومن بعد استنتج le signe ديال g de x sur R.",
      "reponse": phrase("g(0,5) = 0,125 + 1,5 − 2 = −0,375 < 0 et g(0,6) = 0,216 + 1,8 − 2 = 0,016 > 0, donc 0,5 < α < 0,6. g étant strictement croissante avec g(α) = 0 : g(x) < 0 sur ]−∞ ; α[, g(α) = 0, g(x) > 0 sur ]α ; +∞[."),
      "clavier": {"aides": ["g(0,5) = −0,375", "g(0,6) = 0,016", "g(x) < 0 pour x < α", "g(x) > 0 pour x > α"], "pieges": ["g(0,6) < 0", "g(x) > 0 pour x < α"]},
      "aides": [aide("Calcule g(0,5) et g(0,6) à la calculatrice : s'ils sont de signes contraires, α est entre les deux.",
                     "حسب g de zéro virgule cinq و g de zéro virgule six بالآلة الحاسبة: يلا عندهم signes contraires، α بيناتهم."),
                aide("g est croissante et s'annule en α : avant α, g(x) < g(α) = 0 ; après α, g(x) > 0.",
                     "g croissante، و، s'annule en α: قبل α، g de x صغر من zéro، ومن بعد α، g de x كبر من zéro.")],
      "correction": correction([
          ("2 : g(0,5) = −0,375 < 0 et g(0,6) = 0,016 > 0", "g de zéro virgule cinq"),
          ("donc 0,5 < α < 0,6", "α بين zéro virgule cinq و zéro virgule six"),
          ("g strictement croissante et g(α) = 0 : g(x) < 0 sur ]−∞ ; α[, g(x) > 0 sur ]α ; +∞[", "le signe ديال g")],
          "السؤال deux. g de zéro virgule cinq égale moins zéro virgule trois cent soixante-quinze، négatif. و g de zéro virgule six égale zéro virgule zéro seize، positif. إذن α بين zéro virgule cinq و zéro virgule six. و g croissante، و g de α égale zéro: إذن le signe ديال g: négatif قبل α، و positif من بعد α."),
      "explication": "ex_d7_2", "facile": "fa_d7_2"}

Q3 = {"id": "3", "texte": "Partie II. Montrer que pour tout x de ℝ : f′(x) = x·g(x)/(x² + 1)².",
      "texte_dit": "الجزء الثاني، السؤال trois: بين بلي لكل x من R: f prime de x égale x fois g de x، sur، x carré plus un au carré.",
      "reponse": phrase("f est dérivable sur ℝ (quotient, x² + 1 ≠ 0) ; f′(x) = (3x²(x² + 1) − 2x(x³ + 1))/(x² + 1)² = (3x⁴ + 3x² − 2x⁴ − 2x)/(x² + 1)² = (x⁴ + 3x² − 2x)/(x² + 1)² = x(x³ + 3x − 2)/(x² + 1)² = x·g(x)/(x² + 1)²."),
      "clavier": {"aides": ["(u/v)′ = (u′v − uv′)/v²", "u = x³ + 1, u′ = 3x²", "v = x² + 1, v′ = 2x", "x⁴ + 3x² − 2x", "x(x³ + 3x − 2)"], "pieges": ["u′/v′", "développer (x² + 1)²"]},
      "aides": [aide("f est un quotient u/v : u = x³ + 1, v = x² + 1. Écris u′v − uv′ avec des parenthèses.",
                     "f هي quotient: u égale x au cube plus un، و v égale x carré plus un. كتب u prime v moins u v prime، مع les parenthèses."),
                aide("Développe seulement le numérateur, laisse (x² + 1)² factorisé, puis mets x en facteur : tu dois retrouver g(x).",
                     "نشر غير الفوق، وخلي التحت كيف هو. ومن بعد خرج x facteur: خاصك تلقى g de x.")],
      "correction": correction([
          ("3 : f est dérivable sur ℝ et f′(x) = (3x²(x² + 1) − 2x(x³ + 1))/(x² + 1)²", "u prime v moins u v prime"),
          ("= (3x⁴ + 3x² − 2x⁴ − 2x)/(x² + 1)² = (x⁴ + 3x² − 2x)/(x² + 1)²", "كنشرو الفوق"),
          ("= x(x³ + 3x − 2)/(x² + 1)² = x·g(x)/(x² + 1)²", "x fois g de x")],
          "السؤال trois. f dérivable sur R، و f prime de x égale، u prime v moins u v prime، sur v au carré: trois x carré fois، x carré plus un، moins deux x fois، x au cube plus un. كنشرو الفوق: x puissance quatre plus trois x carré moins deux x. كنخرجو x facteur: x fois، x au cube plus trois x moins deux، و هادي هي g de x. إذن f prime de x égale x fois g de x، sur، x carré plus un au carré."),
      "explication": "ex_d7_3", "facile": "fa_d7_3"}

Q4 = {"id": "4", "texte": "Sachant que lim f(x) = −∞ en −∞ et lim f(x) = +∞ en +∞, étudier le signe de f′(x) et dresser le tableau de variations de f.",
      "texte_dit": "السؤال quatre: عارفين بلي la limite ف moins l'infini هي moins l'infini، وف plus l'infini هي plus l'infini. درس le signe ديال f prime de x، ودير le tableau de variations.",
      "reponse": phrase("(x² + 1)² > 0 : f′(x) a le signe de x·g(x). Sur ]−∞ ; 0[ : x < 0 et g(x) < 0, f′ > 0 ; sur ]0 ; α[ : x > 0 et g(x) < 0, f′ < 0 ; sur ]α ; +∞[ : f′ > 0. f croissante sur ]−∞ ; 0], décroissante sur [0 ; α], croissante sur [α ; +∞[ ; f(0) = 1 maximum local, f(α) minimum local."),
      "clavier": {"aides": ["le signe de f′(x) est le signe de x·g(x)", "tableau de signe à deux lignes", "f(0) = 1", "f(α)"], "pieges": ["f′ a le signe de g(x)", "f′ < 0 sur ]−∞ ; 0["]},
      "aides": [aide("Le dénominateur est positif. Le signe de f′ est celui du produit x·g(x) : fais un tableau avec une ligne pour x et une ligne pour g(x).",
                     "التحت positif. le signe ديال f prime هو le signe ديال x fois g de x: دير tableau فيه ligne ل x و ligne ل g de x."),
                aide("x change de signe en 0, g(x) en α (question 2), et 0 < α. Règle des signes ligne par ligne, puis f(0) = 1.",
                     "x كيبدل le signe ف zéro، و g ف α، و α كبر من zéro. دير la règle des signes، ومن بعد f de zéro égale un.")],
      "correction": correction([
          ("4 : (x² + 1)² > 0, donc le signe de f′(x) est le signe de x·g(x)", "le signe ديال x fois g de x"),
          ("x : −∞ ; 0 ; α ; +∞ ;  x : − 0 + + ;  g(x) : − − 0 + ;  f′(x) : + 0 − 0 +", "tableau de signe"),
          ("f(0) = 1 : maximum local ; f(α) : minimum local", "f de zéro égale un"),
          ("f : −∞ ↗ 1 ↘ f(α) ↗ +∞", "le tableau")],
          "السؤال quatre. التحت positif، إذن le signe ديال f prime هو le signe ديال x fois g de x. ف le tableau de signe: قبل zéro، x négatif و g négative، le produit positif. بين zéro و α، x positif و g négative، le produit négatif. من بعد α، les deux positifs. f de zéro égale un، maximum local، و f de α minimum local. le tableau: طالعة حتى un، هابطة حتى f de α، ومن بعد طالعة حتى plus l'infini."),
      "explication": "ex_d7_4", "facile": "fa_d7_4"}

Q5 = {"id": "5", "texte": "Montrer que f(α) = 3(1 − α)/(1 + α²).",
      "texte_dit": "السؤال cinq: بين بلي f de α égale trois، facteur de un moins α، sur un plus α carré.",
      "reponse": phrase("g(α) = 0 donne α³ + 3α − 2 = 0, donc α³ = 2 − 3α. Alors f(α) = (α³ + 1)/(α² + 1) = (2 − 3α + 1)/(α² + 1) = (3 − 3α)/(1 + α²) = 3(1 − α)/(1 + α²)."),
      "clavier": {"aides": ["g(α) = 0", "α³ = 2 − 3α", "(α³ + 1)/(α² + 1)"], "pieges": ["α = 0,5", "calculer α exactement"]},
      "aides": [aide("On ne connaît pas α exactement, mais on sait que g(α) = 0 : écris-le et isole α³.",
                     "ما كنعرفوش α بالضبط، ولكن عارفين g de α égale zéro: كتبها وخرج α au cube."),
                aide("Remplace α³ par 2 − 3α dans f(α) = (α³ + 1)/(α² + 1), puis factorise par 3.",
                     "عوض α au cube ب deux moins trois α ف f de α، ومن بعد خرج trois facteur.")],
      "correction": correction([
          ("5 : g(α) = 0, donc α³ + 3α − 2 = 0, soit α³ = 2 − 3α", "α au cube égale deux moins trois α"),
          ("f(α) = (α³ + 1)/(α² + 1) = (2 − 3α + 1)/(α² + 1)", "كنعوضو"),
          ("= (3 − 3α)/(1 + α²) = 3(1 − α)/(1 + α²)", "trois، facteur de un moins α")],
          "السؤال cinq. g de α égale zéro، إذن α au cube égale deux moins trois α. كنعوضو ف f de α: الفوق كيولي deux moins trois α plus un، يعني trois moins trois α. كنخرجو trois facteur: f de α égale trois، facteur de un moins α، sur un plus α carré."),
      "explication": "ex_d7_5", "facile": "fa_d7_5"}

Q6 = {"id": "6", "texte": "Vérifier que f(x) = x + (1 − x)/(x² + 1), puis montrer que (Δ) : y = x est asymptote oblique à (C) au voisinage de +∞ et de −∞, et étudier la position relative de (C) et (Δ).",
      "texte_dit": "السؤال six: تحقق بلي f de x égale x، plus، un moins x، sur x carré plus un. ومن بعد بين بلي la droite delta، y égale x، asymptote oblique، au voisinage de plus l'infini et de moins l'infini، ودرس la position relative.",
      "reponse": phrase("x + (1 − x)/(x² + 1) = (x³ + x + 1 − x)/(x² + 1) = (x³ + 1)/(x² + 1) = f(x). f(x) − x = (1 − x)/(x² + 1) → 0 en ±∞ : (Δ) asymptote oblique au voisinage de ±∞. x² + 1 > 0 : f(x) − x a le signe de 1 − x : (C) au-dessus de (Δ) sur ]−∞ ; 1[, en dessous sur ]1 ; +∞[, et (C) coupe (Δ) au point A(1 ; 1)."),
      "clavier": {"aides": ["f(x) − x = (1 − x)/(x² + 1)", "→ 0", "le signe de 1 − x", "A(1 ; 1)", "au-dessus", "en dessous"], "pieges": ["(C) au-dessus partout", "lim (1 − x)/(x² + 1) = −1"]},
      "aides": [aide("Pars de x + (1 − x)/(x² + 1) et mets au même dénominateur. Puis f(x) − x = (1 − x)/(x² + 1) : degré 1 en haut, 2 en bas.",
                     "بدا من x، plus، un moins x sur x carré plus un، وحط على نفس le dénominateur. ومن بعد f de x moins x: فالفوق degré un، وفالتحت degré deux."),
                aide("Pour la position : x² + 1 > 0, le signe vient de 1 − x. Là où la différence est nulle, (C) coupe (Δ).",
                     "ل la position: x carré plus un positif، le signe جاي من un moins x. فين الفرق égale zéro، la courbe كتقطع la droite.")],
      "correction": correction([
          ("6 : x + (1 − x)/(x² + 1) = (x³ + x + 1 − x)/(x² + 1) = (x³ + 1)/(x² + 1) = f(x)", "نفس le dénominateur"),
          ("f(x) − x = (1 − x)/(x² + 1) → 0 en ±∞ : (Δ) : y = x est asymptote oblique au voisinage de +∞ et de −∞", "asymptote oblique"),
          ("x² + 1 > 0 : f(x) − x a le signe de 1 − x", "le signe ديال un moins x"),
          ("(C) au-dessus de (Δ) sur ]−∞ ; 1[, en dessous sur ]1 ; +∞[ ; (C) ∩ (Δ) = {A(1 ; 1)}", "كتقطع la droite")],
          "السؤال six. على نفس le dénominateur، الفوق كيولي x au cube plus un: كنلقاو f de x. f de x moins x، égale un moins x، sur x carré plus un، وكيمشي ل zéro ف plus l'infini و moins l'infini: la droite y égale x، est une asymptote oblique. التحت positif، إذن le signe ديال الفرق هو le signe ديال un moins x: la courbe au-dessus قبل un، و en dessous من بعد un. وفx égale un، الفرق zéro: la courbe كتقطع la droite فالنقطة A، un، un."),
      "explication": "ex_d7_6", "facile": "fa_d7_6"}

SIM1 = sim("ex_d7_1", "Question 1 : une solution unique, lue dans le tableau",
           "Continue + strictement monotone + changement de signe : solution unique.",
           C + "ec4", "La méthode écrite au tableau sur x³ + x − 1",
           "نشوفو la méthode على هاد l'exemple: f de x égale x au cube plus x moins un، sur zéro، un. f continue. f prime de x égale trois x carré plus un، positive: f strictement croissante. f de zéro égale moins un، و f de un égale un: signes contraires. إذن l'équation f de x égale zéro عندها une solution unique α. فالتمرين ديالك: نفس الجمل مع g.",
           [("continue", "f continue"), ("strictement monotone", "f strictement croissante"), ("f(a) × f(b) < 0 ⇒ solution unique", "signes contraires")],
           [jusqua("نشوفو la méthode", "enonce"), jusqua("f continue", "continue"), montre("f continue", "centre:0"),
            jusqua("f strictement croissante", "monotone"), montre("f strictement croissante", "centre:1"),
            jusqua("signes contraires", "signes"), montre("signes contraires", "centre:2"), jusqua("إذن l'équation", "conclusion")])

SIM2 = sim("ex_d7_2", "Question 2 : le signe de g, lu dans son tableau",
           "Le tableau de g donne son signe sans calcul de plus.",
           C + "aux_g", "Partie I d'un problème : le signe de g lu dans son tableau",
           "نشوفو على هاد l'exemple ديال الدرس: g de x égale deux x au cube moins trois x carré plus deux. le tableau ديال g كيبين le minimum، g de un égale un، positif. إذن g ديما positive. القاعدة: le signe ديال g كنقراوه من le tableau ديالها. فالتمرين ديالك: g croissante، و g de α égale zéro: قبل α négative، ومن بعد positive.",
           [("le signe de g se lit dans son tableau", "القاعدة")],
           [jusqua("نشوفو على هاد l'exemple", "enonce"), jusqua("le tableau ديال g", "ligne_fleches"), jusqua("إذن g ديما positive", "conclusion_g"),
            montre("القاعدة", "centre:0")])

SIM3 = sim("ex_d7_3", "Question 3 : la dérivée d'un quotient",
           "(u/v)′ = (u′v − uv′)/v² : le dénominateur reste factorisé.",
           C + "dv2", "La dérivée de (2x + 1)/(x − 3) écrite au tableau",
           "نشوفو la méthode على هاد l'exemple: f de x égale deux x plus un، sur x moins trois. الصيغة: u prime v moins u v prime، sur v au carré. u égale deux x plus un، u prime égale deux، v égale x moins trois، v prime égale un. كنعوضو، وكنشرو غير الفوق: moins sept، sur x moins trois au carré. والتحت كيبقى factorisé. فالتمرين ديالك: u égale x au cube plus un، و v égale x carré plus un.",
           [("(u/v)′ = (u′v − uv′)/v²", "الصيغة"), ("v² reste factorisé", "والتحت كيبقى factorisé")],
           [jusqua("الصيغة", "quotient"), montre("الصيغة", "centre:0"), jusqua("u égale deux x plus un", "uv"), jusqua("كنعوضو", "remplace"),
            jusqua("moins sept", "resultat"), jusqua("والتحت كيبقى factorisé", "piege"), montre("والتحت كيبقى factorisé", "centre:1")])

SIM4 = sim("ex_d7_4", "Question 4 : le signe de f′ vient de la partie I",
           "On écarte le dénominateur positif ; le signe vient de g (et ici aussi de x).",
           C + "va7", "Le lien entre la partie I et la partie II",
           "نشوفو على هاد l'exemple ديال الدرس: فالجزء الأول، g positive. فالجزء الثاني، f prime de x égale g de x sur x carré. x carré positif، إذن le signe ديال f prime هو le signe ديال g. g positive، إذن f croissante. فالتمرين ديالك: كاين x حتى هو فالفوق، إذن دير tableau de signe فيه deux lignes: x و g de x.",
           [("dénominateur > 0 ⇒ signe du numérateur", "x carré positif"), ("ici : signe de x·g(x), deux lignes", "deux lignes")],
           [jusqua("فالجزء الأول", "signe_g"), jusqua("فالجزء الثاني", "partie2"), jusqua("x carré positif", "lien"), montre("x carré positif", "centre:0"),
            jusqua("إذن f croissante", "conclusion"), montre("deux lignes", "centre:1")])

SIM5 = sim("ex_d7_5", "Question 5 : utiliser g(α) = 0",
           "On part d'un membre ; on remplace ce que l'on sait.",
           C + "ec2", "Partir d'un membre pour arriver à l'autre",
           "نشوفو la méthode على هاد l'exemple: باش نبينو واحد l'égalité، كنبداو من جهة وحدة، وكنوصلو للجهة الأخرى. ما كنبداوش من الجواب. وكنستعملو النتيجة اللي عطاونا. فالتمرين ديالك: النتيجة هي g de α égale zéro، يعني α au cube égale deux moins trois α. بدا من f de α، وعوض α au cube.",
           [("partir d'un membre, arriver à l'autre", "كنبداو من جهة وحدة"), ("g(α) = 0 ⇒ α³ = 2 − 3α", "يعني α au cube")],
           [jusqua("كنبداو من جهة وحدة", "un_membre"), montre("كنبداو من جهة وحدة", "centre:0"), jusqua("وكنستعملو النتيجة", "bloque"), montre("يعني α au cube", "centre:1")])

SIM6 = sim("ex_d7_6", "Question 6 : asymptote oblique et position relative",
           "La limite de f(x) − y donne l'asymptote ; son signe donne la position.",
           D + "position.html?vue=ecart", "Un segment entre (Δ) et la courbe de 2x + 1 + 1/x",
           "نشوفو على هاد l'exemple: f de x égale deux x plus un، plus un sur x، و la droite y égale deux x plus un. الفرق un sur x كيمشي ل zéro: asymptote oblique. le signe ديال الفرق كيعطي la position: فx égale un، القطعة خضرا، la courbe au-dessus. فx égale moins un، القطعة حمرا، la courbe en dessous. فالتمرين ديالك: الفرق هو un moins x، sur x carré plus un، وكيتنقل le signe ف un.",
           [("limite de f(x) − y → 0 : asymptote", "asymptote oblique"), ("signe de f(x) − y : position", "le signe ديال الفرق")],
           [jusqua("نشوفو على هاد l'exemple", "droite_tracee"), montre("asymptote oblique", "centre:0"), montre("le signe ديال الفرق", "centre:1"),
            jusqua("فx égale un، القطعة خضرا", "ecart_positif"), jusqua("فx égale moins un", "ecart_negatif"), jusqua("فالتمرين ديالك", "tableau_rempli")])

FA1 = qcm("fa_d7_1", "Plus facile : pourquoi une seule solution ?", "سؤال ساهل على الحل الوحيد.",
          "g(0) = −2 et g(1) = 2. Pour avoir UNE SEULE solution dans ]0 ; 1[, il faut aussi que g soit…", ["positive", "continue et strictement monotone", "dérivable en 0"], 1, [
              (("قريب! g ماشي positive، g de zéro négatif. عاود اختار.", "g(0) < 0. Réessaie."),
               ("الجواب: continue et strictement monotone.", "Réponse : continue et strictement monotone.")),
              ("برافو! continue باش تقطع l'axe، و strictement monotone باش تقطعو مرة وحدة.", "Juste : continue et strictement monotone."),
              (("ما تقلقش. dérivable ف نقطة وحدة ما كيكفيش. عاود اختار.", "Une seule valeur ne suffit pas. Réessaie."),
               ("الجواب: continue et strictement monotone.", "Réponse : continue et strictement monotone."))],
          "Pour une seule solution, g doit être ?")

FA2 = association("fa_d7_2", "Plus facile : le signe de g", "Relie chaque intervalle au signe de g(x).",
                  "نتمرنو: ربط كل intervalle مع le signe ديال g.", "g est strictement croissante et g(α) = 0.",
                  [("1", "]−∞ ; α["), ("2", "]α ; +∞[")],
                  [("a", "g(x) < 0"), ("b", "g(x) > 0")],
                  {"1": "a", "2": "b"},
                  {"1-a": ("Oui : avant α, g(x) < g(α) = 0.", "برافو: قبل α، g صغر من zéro."),
                   "1-b": ("g est croissante : avant α, ses valeurs sont plus petites que g(α) = 0.", "لا، g croissante: قبل α القيم صغر من zéro."),
                   "2-a": ("g est croissante : après α, ses valeurs dépassent g(α) = 0.", "لا، من بعد α القيم كبر من zéro."),
                   "2-b": ("Oui : après α, g(x) > 0.", "برافو: من بعد α، g positive.")},
                  ("(1 ; a) (2 ; b) : g négative avant α, positive après.", "g négative قبل α، و positive من بعد."))

FA3 = qcm("fa_d7_3", "Plus facile : la formule du quotient", "سؤال ساهل على la dérivée ديال quotient.",
          "(u/v)′ = …", ["u′/v′", "(u′v − uv′)/v²", "(u′v + uv′)/v²"], 1, [
              (("قريب! la dérivée ديال quotient ماشي quotient ديال les dérivées. عاود اختار.", "(u/v)′ ≠ u′/v′. Réessaie."),
               ("الجواب: u prime v moins u v prime، sur v au carré.", "Réponse : (u′v − uv′)/v².")),
              ("برافو! u prime v moins u v prime، sur v au carré.", "Juste : (u′v − uv′)/v²."),
              (("ما تقلقش. plus ديال le produit. هنا moins. عاود اختار.", "Le + est celui du produit. Réessaie."),
               ("الجواب: u prime v moins u v prime، sur v au carré.", "Réponse : (u′v − uv′)/v²."))],
          "La dérivée de u sur v est ?")

FA4 = vrai_faux("fa_d7_4", "Plus facile : vrai ou faux", "f′(x) = x·g(x)/(x² + 1)² et 0 < α.", "سؤال ساهل: صحيح ولا غالط؟", [
    ("Sur ]0 ; α[, f′(x) < 0.", True, "x > 0 et g(x) < 0 : le produit est négatif."),
    ("Le signe de f′(x) est le signe de g(x).", False, "Il y a aussi le facteur x, qui change de signe en 0."),
    ("f(0) = 1 est un maximum local.", True, "f′ passe de + à − en 0.")])

FA5 = qcm("fa_d7_5", "Plus facile : remplacer α³", "سؤال ساهل على α.",
          "g(α) = α³ + 3α − 2 = 0. Donc α³ = …", ["2 − 3α", "3α − 2", "2 + 3α"], 0, [
              ("برافو! كنحيدو trois α و moins deux للجهة الأخرى.", "Juste : α³ = 2 − 3α."),
              (("قريب! ملي كيدوز terme للجهة الأخرى كيبدل le signe. عاود اختار.", "Un terme qui change de membre change de signe. Réessaie."),
               ("الجواب: deux moins trois α.", "Réponse : 2 − 3α.")),
              (("ما تقلقش. trois α كيدوز بـ moins. عاود اختار.", "3α passe avec un signe moins. Réessaie."),
               ("الجواب: deux moins trois α.", "Réponse : 2 − 3α."))],
          "α au cube égale ?")

FA6 = association("fa_d7_6", "Plus facile : limite ou signe ?", "Relie chaque question à l'outil qui y répond.",
                  "نتمرنو: ربط كل سؤال مع الأداة ديالو.", "f(x) − x = (1 − x)/(x² + 1).",
                  [("1", "(Δ) est-elle asymptote ?"), ("2", "(C) est-elle au-dessus de (Δ) ?")],
                  [("a", "la limite de f(x) − x en ±∞"), ("b", "le signe de f(x) − x")],
                  {"1": "a", "2": "b"},
                  {"1-a": ("Oui : la limite 0 donne l'asymptote.", "برافو: la limite zéro كتعطي asymptote."),
                   "1-b": ("Le signe donne la position, pas l'asymptote.", "لا، le signe كيعطي la position."),
                   "2-a": ("La limite dit seulement que (C) se rapproche ; la position vient du signe.", "لا، la limite ما كتقولش الفوق ولا التحت."),
                   "2-b": ("Oui : positif, au-dessus ; négatif, en dessous.", "برافو: positif الفوق، négatif التحت.")},
                  ("(1 ; a) (2 ; b) : asymptote par la limite, position par le signe.", "asymptote ب la limite، و la position ب le signe."))

EX = {
    "id": ID, "type": "exercice", "version": 1, "status": "published",
    "matiere": "mathematiques", "chapitre": "derivation_etude_fonctions", "cours": "math_ch2_derivation_etude_fonctions",
    "titre": "Problème : fonction auxiliaire, α et fonction rationnelle", "niveau": "difficile", "duree_min": 50, "origine": ORIGINE,
    "competences": ["Montrer l'unicité d'une solution α et l'encadrer", "Déduire le signe d'une fonction auxiliaire", "Montrer que f′(x) = une forme donnée (quotient)", "Dresser un tableau avec deux facteurs de signe", "Exprimer f(α) avec g(α) = 0", "Asymptote oblique et position relative"],
    "enonce": {
        "intro": "Partie I : soit g la fonction définie sur ℝ par g(x) = x³ + 3x − 2. Partie II : soit f la fonction définie sur ℝ par f(x) = (x³ + 1)/(x² + 1), (C) sa courbe dans un repère orthonormé et (Δ) la droite d'équation y = x.",
        "intro_dit": "دابا نقراو l'énoncé. الجزء الأول: g de x égale x au cube plus trois x moins deux، sur R. الجزء الثاني: f de x égale x au cube plus un، sur x carré plus un، و C هي la courbe ديالها، و delta هي la droite y égale x.",
        "figures": [figure("C", "(x^3+1)/(x^2+1)", -3, 3, -3, 3, "Allure de (C) : f(x) = (x³ + 1)/(x² + 1)")],
        "donnees": ["g(x) = x³ + 3x − 2", "f(x) = (x³ + 1)/(x² + 1)", "(Δ) : y = x", "lim f = −∞ en −∞, lim f = +∞ en +∞"],
        "questions": [Q1, Q2, Q3, Q4, Q5, Q6]},
    "explication": deck("explication", "Explication animée", [SIM1, SIM2, SIM3, SIM4, SIM5, SIM6]),
    "facile": deck("facile", "Plus facile, pour s'entraîner", [FA1, FA2, FA3, FA4, FA5, FA6]),
    "similaire": {"id": ID + "_b", "titre": "Même exercice, autres données", "enonce": {
        "intro": "Partie I : g(x) = x³ + 3x − 6 sur ℝ. Partie II : f(x) = (x³ + 3)/(x² + 1) sur ℝ, (C′) sa courbe et (Δ) : y = x.",
        "intro_dit": "نفس التمرين، بدالة أخرى: g de x égale x au cube plus trois x moins six، و f de x égale x au cube plus trois، sur x carré plus un.",
        "figures": [figure("C′", "(x^3+3)/(x^2+1)", -3, 4, -3, 4, "Allure de (C′) : f(x) = (x³ + 3)/(x² + 1)")],
        "donnees": ["g(x) = x³ + 3x − 6", "f(x) = (x³ + 3)/(x² + 1)", "(Δ) : y = x"],
        "questions": [
            {"id": "1", "texte": "Étudier les variations de g et montrer que g(x) = 0 admet une solution unique α, avec 1 < α < 2.",
             "reponse": phrase("g′(x) = 3x² + 3 > 0 : g continue strictement croissante ; g(1) = −2 < 0, g(2) = 8 > 0 : solution unique α ∈ ]1 ; 2[."),
             "clavier": {"aides": ["g(1) = −2", "g(2) = 8"], "pieges": ["g′(x) = 3x²"]},
             "correction": correction([("1 : g′(x) = 3x² + 3 > 0 ; g(1) = −2, g(2) = 8 : solution unique α ∈ ]1 ; 2[", "solution unique")],
                                      "g prime ديما positive، g de un égale moins deux و g de deux égale huit: une solution unique α بين un و deux.")},
            {"id": "2", "texte": "Vérifier que 1,2 < α < 1,3 et en déduire le signe de g(x).",
             "reponse": phrase("g(1,2) = −0,672 < 0, g(1,3) = 0,097 > 0 : 1,2 < α < 1,3 ; g < 0 sur ]−∞ ; α[, g > 0 sur ]α ; +∞[."),
             "clavier": {"aides": ["g(1,2) = −0,672", "g(1,3) = 0,097"], "pieges": ["g(1,3) < 0"]},
             "correction": correction([("2 : g(1,2) = −0,672 < 0 et g(1,3) = 0,097 > 0 : 1,2 < α < 1,3", "α بين un virgule deux و un virgule trois"),
                                       ("g(x) < 0 sur ]−∞ ; α[ et g(x) > 0 sur ]α ; +∞[", "le signe ديال g")],
                                      "α بين un virgule deux و un virgule trois. le signe ديال g: négatif قبل α، و positif من بعد.")},
            {"id": "3", "texte": "Montrer que f′(x) = x·g(x)/(x² + 1)².",
             "reponse": phrase("f′(x) = (3x²(x² + 1) − 2x(x³ + 3))/(x² + 1)² = (x⁴ + 3x² − 6x)/(x² + 1)² = x(x³ + 3x − 6)/(x² + 1)²."),
             "clavier": {"aides": ["(u′v − uv′)/v²", "x⁴ + 3x² − 6x"], "pieges": ["u′/v′"]},
             "correction": correction([("3 : f′(x) = (x⁴ + 3x² − 6x)/(x² + 1)² = x·g(x)/(x² + 1)²", "x fois g de x")],
                                      "u prime v moins u v prime، sur v au carré، وكنلقاو الفوق x puissance quatre plus trois x carré moins six x، يعني x fois g de x.")},
            {"id": "4", "texte": "Étudier le signe de f′(x) et dresser le tableau de variations de f (lim f = ±∞ en ±∞).",
             "reponse": phrase("f′ a le signe de x·g(x) : + sur ]−∞ ; 0[, − sur ]0 ; α[, + sur ]α ; +∞[ ; f(0) = 3 maximum local, f(α) minimum local."),
             "clavier": {"aides": ["f(0) = 3", "signe de x·g(x)"], "pieges": ["signe de g seul"]},
             "correction": correction([("4 : f′ : + 0 − 0 + (en 0 et α) ; f(0) = 3 maximum local ; f(α) minimum local", "f de zéro égale trois")],
                                      "le signe ديال x fois g de x: positif، négatif، positif. f de zéro égale trois، maximum local، و f de α minimum local.")},
            {"id": "5", "texte": "Montrer que f(α) = 3(3 − α)/(1 + α²).",
             "reponse": phrase("α³ = 6 − 3α, donc f(α) = (6 − 3α + 3)/(α² + 1) = 3(3 − α)/(1 + α²)."),
             "clavier": {"aides": ["α³ = 6 − 3α"], "pieges": ["α³ = 3α − 6"]},
             "correction": correction([("5 : g(α) = 0 donne α³ = 6 − 3α ; f(α) = (9 − 3α)/(1 + α²) = 3(3 − α)/(1 + α²)", "α au cube égale six moins trois α")],
                                      "α au cube égale six moins trois α. كنعوضو: الفوق كيولي neuf moins trois α، إذن f de α égale trois، facteur de trois moins α، sur un plus α carré.")},
            {"id": "6", "texte": "Vérifier que f(x) = x + (3 − x)/(x² + 1), montrer que (Δ) est asymptote oblique en ±∞ et étudier la position relative.",
             "reponse": phrase("f(x) − x = (3 − x)/(x² + 1) → 0 en ±∞ : asymptote oblique ; (C′) au-dessus de (Δ) sur ]−∞ ; 3[, en dessous sur ]3 ; +∞[, intersection A(3 ; 3)."),
             "clavier": {"aides": ["(3 − x)/(x² + 1)", "A(3 ; 3)"], "pieges": ["A(1 ; 1)"]},
             "correction": correction([("6 : f(x) − x = (3 − x)/(x² + 1) → 0 en ±∞ : (Δ) asymptote oblique", "asymptote oblique"),
                                       ("signe de 3 − x : au-dessus sur ]−∞ ; 3[, en dessous sur ]3 ; +∞[, A(3 ; 3)", "la position")],
                                      "الفرق trois moins x، sur x carré plus un، كيمشي ل zéro: asymptote oblique. والفرق عندو le signe ديال trois moins x، و la position: الفوق قبل trois، التحت من بعد، وكتقطعها ف A، trois، trois.")}]}}
}


def _alpha(o, k=""):
    """La voix dit « alpha » : la lettre grecque reste dans l'écrit seulement."""
    if isinstance(o, dict):
        return {kk: _alpha(v, kk) for kk, v in o.items()}
    if isinstance(o, list):
        return [_alpha(v, k) for v in o]
    if isinstance(o, str) and k in ("dit", "parole", "texte_dit", "intro_dit", "enonce_dit", "mixed", "mot"):
        return o.replace("α", "alpha")
    return o


ecrire(_alpha(EX))
