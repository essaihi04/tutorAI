# Exercice de maths, ch. 2 (dérivation et étude des fonctions), niveau DIFFICILE (« Supérieur » : au-dessus du national,
# même forme) : f(x) = x − 2√x ; dérivabilité à droite en 0 et sens de la demi-tangente, dérivée non donnée, limite en
# +∞ à lever, branche parabolique de direction y = x (deux limites), concavité, restriction et fonction réciproque,
# (g⁻¹)′ en un point dont il faut d'abord trouver l'antécédent.
# Sources comparées (lecture seule, rien de copié) :
#  - exploration/derivation_etude_fonctions.json : cas types derivabilite_droite_gauche, interpretation_taux,
#    branche_parabolique, point_inflexion (concavité), reciproque_existence, reciproque_derivee ; pièges « s'arrêter à
#    lim f(x)/x = a », « (f⁻¹)′ au mauvais point », « symétriser toute la courbe » ; erreurs_examen (branche parabolique,
#    fonction réciproque : antécédent, f′(b) ≠ 0).
#  - vidéos des profs (Aderdour et maths variés : arbre des branches infinies ; Prof fati : dérivabilité de la réciproque ;
#    Timath : contrôle PC avec demi-tangente ; Ishaq Ghanem : « il ne suffit pas que f soit dérivable »).
#  - nationaux : direction la droite y = x dans 3 sujets ; fonction réciproque dans 8, dont (f⁻¹)′ en un point dans 6
#    (fonctions ln/exp, non reprises).
#  - séries en ligne repérées (titres et résumés de recherche ; sites non joignables depuis la session) : talamidi série 1
#    (réciproque sur un intervalle J), talamidi exercices non corrigés 2 (branche parabolique), Lycée Mohammed Serraj
#    (monstremath), devoirs Hammouda (scribd : réciproque), cours Atmani (moutamadris) : x − a√x est une fonction-type
#    des contrôles ; la difficulté ajoutée ici est l'enchaînement complet et l'antécédent à trouver.
# Différent des exemples du cours (x + √x, x√(x + 1), x² + 1).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa

D = "/media/simulations/maths/derivation-tableau/"
ID = "math_ex_ch2_derivation_6"


def figure(nom, expr, xmax, ymin, ymax, titre):
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": -0.5, "max": xmax, "nom": "x", "graduations": list(range(1, int(xmax) + 1, 1 if xmax <= 12 else 2))},
                     "y": {"min": ymin, "max": ymax, "nom": "y", "graduations": list(range(int(ymin) + 1, int(ymax) + 1))}},
            "legende": f"Allure de ({nom}) et la droite y = x (pointillé) : à justifier par les questions.",
            "elements": [{"f": "courbe", "expr": expr, "de": 0, "a": xmax, "couleur": "cyan", "texte": f"({nom})", "texte_x": xmax - 0.8, "pos": "se"},
                         {"f": "courbe", "expr": "x", "de": 0, "a": min(xmax, ymax), "couleur": "violet", "trait": "pointille", "texte": "y = x", "texte_x": min(xmax, ymax) - 1, "pos": "no"}]}


Q1 = {"id": "1", "texte": "Étudier la dérivabilité de f à droite en 0, puis interpréter géométriquement le résultat.",
      "texte_dit": "السؤال un: درس la dérivabilité ديال f à droite en zéro، ومن بعد interpréter géométriquement le résultat.",
      "reponse": phrase("f(0) = 0 ; pour x > 0 : (f(x) − f(0))/x = (x − 2√x)/x = 1 − 2/√x ; quand x → 0⁺, 2/√x → +∞, donc la limite est −∞ : f n'est pas dérivable à droite en 0, et (C) admet en O une demi-tangente verticale dirigée vers le bas."),
      "clavier": {"aides": ["(x − 2√x)/x = 1 − 2/√x", "2/√x → +∞", "−∞", "demi-tangente verticale", "dirigée vers le bas"], "pieges": ["dirigée vers le haut", "f′(0) = 1", "tangente horizontale"]},
      "aides": [aide("Écris le taux en 0 et simplifie : √x/x = 1/√x.", "كتب le taux ف zéro وبسطو: racine de x sur x، égale un sur racine de x."),
                aide("Le taux devient 1 − 2/√x. Vers quoi tend 2/√x quand x → 0⁺ ? Une limite infinie : non dérivable ; à droite et −∞ : la courbe est sous O.",
                     "le taux كيولي un moins deux sur racine de x. لاش كيمشي deux sur racine de x ملي x tend vers zéro plus؟ limite infinie: non dérivable. على اليمين و moins l'infini: la courbe تحت O.")],
      "correction": correction([
          ("1 : f(0) = 0 et, pour x > 0, (f(x) − f(0))/x = (x − 2√x)/x = 1 − 2/√x", "un moins deux sur racine de x"),
          ("lim 2/√x = +∞ (x → 0⁺), donc lim (f(x) − f(0))/x = −∞", "la limite égale moins l'infini"),
          ("f n'est pas dérivable à droite en 0", "n'est pas dérivable à droite en zéro"),
          ("(C) admet en O une demi-tangente verticale dirigée vers le bas", "dirigée vers le bas")],
          "السؤال un. f de zéro égale zéro. le taux هو x moins deux racine de x، sur x، يعني un moins deux sur racine de x. deux sur racine de x كيمشي ل plus l'infini، إذن la limite égale moins l'infini. إذن f n'est pas dérivable à droite en zéro، و la courbe عندها ف O، une demi-tangente verticale، dirigée vers le bas."),
      "explication": "ex_d6_1", "facile": "fa_d6_1"}

Q2 = {"id": "2", "texte": "Calculer lim f(x) quand x → +∞. Montrer que pour tout x > 0 : f′(x) = (√x − 1)/√x, puis dresser le tableau de variations de f.",
      "texte_dit": "السؤال deux: حسب la limite ديال f de x quand x tend vers plus l'infini. وبين بلي لكل x positif: f prime de x égale، racine de x moins un، sur racine de x. ومن بعد دير le tableau de variations.",
      "reponse": phrase("f(x) = √x(√x − 2) → +∞ en +∞. f′(x) = 1 − 2 × 1/(2√x) = 1 − 1/√x = (√x − 1)/√x. √x > 0 : f′ a le signe de √x − 1 : négatif sur ]0 ; 1[, positif sur ]1 ; +∞[ ; f décroissante sur [0 ; 1], croissante sur [1 ; +∞[ ; f(0) = 0, f(1) = −1."),
      "clavier": {"aides": ["f(x) = √x(√x − 2)", "f′(x) = 1 − 1/√x", "(√x − 1)/√x", "f(1) = −1"], "pieges": ["+∞ − ∞ = 0", "f′(x) = 1 − 2/√x"]},
      "aides": [aide("En +∞, x − 2√x est une forme « +∞ − ∞ » : factorise par √x, car x = √x × √x.",
                     "ف plus l'infini، x moins deux racine de x هي forme indéterminée، plus l'infini moins l'infini. خرج racine de x facteur، حيت x هو racine de x، fois، racine de x."),
                aide("(√x)′ = 1/(2√x), donc (2√x)′ = 1/√x. Le signe de f′ vient de √x − 1, nul en x = 1.",
                     "la dérivée ديال racine de x هي un sur deux racine de x، إذن la dérivée ديال deux racine de x هي un sur racine de x. le signe ديال f prime جاي من racine de x moins un، اللي، s'annule en un.")],
      "correction": correction([
          ("2 : f(x) = √x(√x − 2) ; √x → +∞ et √x − 2 → +∞, donc lim f(x) = +∞ (x → +∞)", "la limite égale plus l'infini"),
          ("pour x > 0 : f′(x) = 1 − 2 × 1/(2√x) = 1 − 1/√x = (√x − 1)/√x", "f prime de x égale un moins un sur racine de x"),
          ("√x > 0 : f′(x) a le signe de √x − 1 : < 0 sur ]0 ; 1[, > 0 sur ]1 ; +∞[", "le signe ديال racine de x moins un"),
          ("f(0) = 0 ; f(1) = 1 − 2 = −1 ;  f : 0 ↘ −1 ↗ +∞", "f de un égale moins un")],
          "السؤال deux. f de x égale racine de x، fois، racine de x moins deux. بجوج كيمشيو ل plus l'infini، إذن la limite égale plus l'infini. f prime de x égale un moins deux fois un sur deux racine de x، يعني f prime de x égale un moins un sur racine de x، و على نفس le dénominateur: racine de x moins un، sur racine de x. التحت positif، إذن le signe ديال racine de x moins un: négatif قبل un، positif من بعد. f de zéro égale zéro، و f de un égale moins un. f décroissante حتى moins un، ومن بعد croissante حتى plus l'infini."),
      "explication": "ex_d6_2", "facile": "fa_d6_2"}

Q3 = {"id": "3", "texte": "Calculer lim f(x)/x et lim [f(x) − x] quand x → +∞, puis déterminer la nature de la branche infinie de (C) au voisinage de +∞.",
      "texte_dit": "السؤال trois: حسب la limite ديال f de x sur x، و la limite ديال f de x moins x، quand x tend vers plus l'infini. ومن بعد حدد la branche infinie ديال la courbe، au voisinage de plus l'infini.",
      "reponse": phrase("f(x)/x = 1 − 2/√x → 1 ; f(x) − x = −2√x → −∞. Donc (C) admet au voisinage de +∞ une branche parabolique de direction la droite d'équation y = x."),
      "clavier": {"aides": ["f(x)/x = 1 − 2/√x → 1", "f(x) − x = −2√x → −∞", "branche parabolique de direction la droite y = x"], "pieges": ["asymptote oblique y = x", "direction l'axe des ordonnées"]},
      "aides": [aide("lim f(x) = +∞ : on calcule lim f(x)/x. Si elle vaut un réel a ≠ 0, il reste une limite : f(x) − ax.",
                     "la limite ديال f de x هي plus l'infini: كنحسبو la limite ديال f de x sur x. يلا كانت عدد a مختلف على zéro، باقي limite أخرى: f de x moins a x."),
                aide("Si f(x) − ax tend vers un réel b : asymptote y = ax + b ; si elle tend vers l'infini : branche parabolique de direction y = ax.",
                     "يلا f de x moins a x مشات ل عدد b: asymptote، y égale a x plus b. يلا مشات ل l'infini: branche parabolique de direction y égale a x.")],
      "correction": correction([
          ("3 : f(x)/x = 1 − 2/√x → 1 (x → +∞)", "f de x sur x كيمشي ل un"),
          ("f(x) − x = −2√x → −∞ (x → +∞)", "f de x moins x كيمشي ل moins l'infini"),
          ("donc (C) admet au voisinage de +∞ une branche parabolique de direction la droite d'équation y = x", "branche parabolique de direction")],
          "السؤال trois. f de x sur x، égale un moins deux sur racine de x، و f de x sur x كيمشي ل un. ولكن باقي limite: f de x moins x، égale moins deux racine de x، و f de x moins x كيمشي ل moins l'infini. إذن ماشي asymptote: la courbe عندها une branche parabolique de direction، la droite d'équation y égale x، au voisinage de plus l'infini."),
      "explication": "ex_d6_3", "facile": "fa_d6_3"}

Q4 = {"id": "4", "texte": "Calculer f″(x) pour x > 0 et en déduire la concavité de (C).",
      "texte_dit": "السؤال quatre: حسب f seconde de x لكل x positif، واستنتج la concavité ديال la courbe.",
      "reponse": phrase("f′(x) = 1 − x^(−1/2), donc f″(x) = 1/(2x√x) > 0 pour x > 0 : (C) est convexe (tournée vers le haut) sur ]0 ; +∞[, sans point d'inflexion."),
      "clavier": {"aides": ["f′(x) = 1 − 1/√x", "(1/v)′ = −v′/v²", "f″(x) = 1/(2x√x)", "convexe"], "pieges": ["f″(x) = −1/(2x√x)", "point d'inflexion"]},
      "aides": [aide("Dérive f′(x) = 1 − 1/√x avec (1/v)′ = −v′/v², v = √x.",
                     "derive f prime de x، égale un moins un sur racine de x، ب un sur v، la dérivée ديالها moins v prime sur v au carré، مع v égale racine de x."),
                aide("(1/√x)′ = −(1/(2√x))/x = −1/(2x√x). Attention au signe moins devant 1/√x.",
                     "la dérivée ديال un sur racine de x هي moins un sur deux x racine de x. رد البال ل le signe moins اللي قدام.")],
      "correction": correction([
          ("4 : f′(x) = 1 − 1/√x et (1/√x)′ = −1/(2x√x)", "la dérivée ديال un sur racine de x"),
          ("donc f″(x) = 1/(2x√x)", "f seconde de x égale un sur deux x racine de x"),
          ("f″(x) > 0 sur ]0 ; +∞[ : (C) est convexe, sans point d'inflexion", "convexe")],
          "السؤال quatre. f prime de x égale un moins un sur racine de x. la dérivée ديال un sur racine de x هي moins un sur deux x racine de x، والموانس كيتحيدو مع بعضياتهم: f seconde de x égale un sur deux x racine de x. هادي ديما positive، إذن la courbe convexe، tournée vers le haut، وما فيهاش point d'inflexion."),
      "explication": "ex_d6_4", "facile": "fa_d6_4"}

Q5 = {"id": "5", "texte": "Soit g la restriction de f à l'intervalle I = [1 ; +∞[. Montrer que g admet une fonction réciproque g⁻¹ définie sur un intervalle J à déterminer.",
      "texte_dit": "السؤال cinq: g هي la restriction ديال f sur I، من un حتى plus l'infini. بين بلي g عندها fonction réciproque، معرفة على intervalle J، حدد J.",
      "reponse": phrase("g est continue et strictement croissante sur I = [1 ; +∞[ (question 2), donc g admet une fonction réciproque g⁻¹ définie sur J = g(I) = [g(1) ; lim g[ = [−1 ; +∞[."),
      "clavier": {"aides": ["continue et strictement croissante sur I", "J = g(I)", "[−1 ; +∞[", "g(1) = −1"], "pieges": ["]−1 ; +∞[", "[0 ; +∞[", "bijective"]},
      "aides": [aide("Deux conditions sur I : continue et strictement monotone. Lis-les dans le tableau de la question 2.",
                     "جوج شروط على I: continue و strictement monotone. قراهم فالتابلو ديال السؤال deux."),
                aide("J = g(I) : g croissante, J va de g(1) (borne atteinte, crochet fermé) à la limite en +∞.",
                     "J هو g de I: g croissante، إذن J كتبدا من g de un، مع crochet fermé، حتى la limite ف plus l'infini.")],
      "correction": correction([
          ("5 : g est continue et strictement croissante sur I = [1 ; +∞[", "continue et strictement croissante"),
          ("donc g admet une fonction réciproque g⁻¹ définie sur J = g(I)", "fonction réciproque"),
          ("J = [g(1) ; lim g(x)[ = [−1 ; +∞[", "J égale moins un، plus l'infini")],
          "السؤال cinq. g continue et strictement croissante sur I، من un حتى plus l'infini. إذن g عندها fonction réciproque g moins un، معرفة على J égale g de I. g de un égale moins un، و la limite plus l'infini، إذن J égale moins un، plus l'infini، مع crochet fermé ف moins un."),
      "explication": "ex_d6_5", "facile": "fa_d6_5"}

Q6 = {"id": "6", "texte": "Vérifier que g(9) = 3, puis montrer que g⁻¹ est dérivable en 3 et calculer (g⁻¹)′(3).",
      "texte_dit": "السؤال six: تحقق بلي g de neuf égale trois، ومن بعد بين بلي g moins un dérivable en trois، وحسب g moins un prime de trois.",
      "reponse": phrase("g(9) = 9 − 2 × 3 = 3, donc g⁻¹(3) = 9 ; g′(9) = (3 − 1)/3 = 2/3 ≠ 0, donc g⁻¹ est dérivable en 3 et (g⁻¹)′(3) = 1/g′(9) = 3/2 = 1,5"),
      "clavier": {"aides": ["g⁻¹(3) = 9", "g′(9) = 2/3 ≠ 0", "(g⁻¹)′(3) = 1/g′(9)", "= 1,5"], "pieges": ["1/g′(3)", "(g⁻¹)′(3) = 2/3"]},
      "aides": [aide("3 est une image : son antécédent est 9 (g(9) = 3). C'est en 9 qu'on dérive g, pas en 3.",
                     "trois هي image: l'antécédent ديالها هو neuf، حيت g de neuf égale trois. ف neuf كنشتقو g، ماشي ف trois."),
                aide("Calcule g′(9) avec la question 2, vérifie qu'il n'est pas nul, puis (g⁻¹)′(3) = 1/g′(9).",
                     "حسب g prime de neuf بالسؤال deux، تأكد بلي ماشي zéro، ومن بعد g moins un prime de trois، égale un sur g prime de neuf.")],
      "correction": correction([
          ("6 : g(9) = 9 − 2√9 = 9 − 6 = 3, donc g⁻¹(3) = 9", "g de neuf égale trois"),
          ("g est dérivable en 9 et g′(9) = (√9 − 1)/√9 = 2/3 ≠ 0", "g prime de neuf égale deux tiers"),
          ("donc g⁻¹ est dérivable en 3 et (g⁻¹)′(3) = 1/g′(9) = 3/2", "un sur g prime de neuf")],
          "السؤال six. neuf moins deux fois trois، كيعطي trois: إذن g de neuf égale trois. إذن g moins un de trois égale neuf. g prime de neuf égale، trois moins un، sur trois، يعني g prime de neuf égale deux tiers، وماشي zéro. إذن g moins un dérivable en trois، و g moins un prime de trois، égale un sur g prime de neuf، يعني trois demis."),
      "explication": "ex_d6_6", "facile": "fa_d6_6"}

ETUDE = D + "trace.html?vue=etude_pas"

SIM1 = sim("ex_d6_1", "Question 1 : le taux à droite, la demi-tangente verticale",
           "Limite infinie du taux : non dérivable ; la demi-tangente part du côté de la courbe.",
           ETUDE + "&depart=domaine", "L'étude de x√(x + 1) au tableau : le taux en −1",
           "نشوفو على هاد l'exemple ديال الدرس: f de x égale x racine de x plus un، فالنقطة moins un. le taux هو x sur racine de x plus un. الفوق كيمشي ل moins un، والتحت ل zéro plus: la limite égale moins l'infini. إذن f n'est pas dérivable à droite en moins un، وكاينة demi-tangente verticale. وحيت على اليمين la courbe تحت النقطة، la demi-tangente dirigée vers le bas. فالتمرين ديالك: بسط le taux ف zéro، وشوف لاش كيمشي.",
           [("taux → ±∞ : non dérivable", "la limite égale moins l'infini"), ("demi-tangente verticale, du côté de la courbe", "dirigée vers le bas")],
           [jusqua("le taux هو", "taux"), montre("la limite égale moins l'infini", "centre:0"), jusqua("وكاينة demi-tangente verticale", "demi_tangente"),
            montre("dirigée vers le bas", "centre:1")])

SIM2 = sim("ex_d6_2", "Question 2 : la dérivée et le tableau",
           "Le dénominateur positif écarté, un seul facteur donne le signe.",
           ETUDE + "&depart=derivee", "L'étude de x√(x + 1) au tableau : f′, son signe, les flèches",
           "نشوفو على هاد l'exemple: f prime de x، égale trois x plus deux، sur deux racine de x plus un. التحت positif، إذن le signe ديال f prime هو le signe ديال الفوق. négatif قبل moins deux tiers، و positif من بعد. les flèches: كتهبط حتى le minimum، ومن بعد كتطلع. فالتمرين ديالك: f prime de x égale un moins un sur racine de x، وحطها على نفس le dénominateur.",
           [("dénominateur > 0 ⇒ signe du numérateur", "التحت positif")],
           [jusqua("التحت positif", "signe_phrase"), montre("التحت positif", "centre:0"), jusqua("négatif قبل moins deux tiers", "ligne_signe"),
            jusqua("les flèches", "fleches")])

SIM3 = sim("ex_d6_3", "Question 3 : deux limites pour la branche infinie",
           "f(x)/x → a, puis f(x) − ax → ±∞ : branche parabolique de direction y = ax.",
           D + "branches.html?vue=direction", "x + √x : la pente de OM tend vers 1, l'écart avec y = x grandit",
           "نشوفو على هاد l'exemple: f de x égale x plus racine de x، و la droite y égale x. M كتمشي لليمين. f de x sur x كتمشي ل un. ولكن ماشي كافي: شوف القطعة بين la courbe و la droite، f de x moins x، égale racine de x، وكتكبر بلا حد. إذن ماشي asymptote: branche parabolique de direction la droite d'équation y égale x. فالتمرين ديالك: f de x moins x كيمشي ل moins l'infini، والخلاصة هي هي.",
           [("lim f(x)/x = 1 …", "f de x sur x كتمشي ل un"), ("… et lim [f(x) − x] = ±∞ : branche parabolique", "إذن ماشي asymptote")],
           [jusqua("M كتمشي لليمين", "m_part"), jusqua("f de x sur x كتمشي ل un", "pente_tend_vers_a"), montre("f de x sur x كتمشي ل un", "centre:0"),
            jusqua("شوف القطعة", "ecart_grandit"), {"mot": "شوف القطعة", "repere": "ecart"}, jusqua("إذن ماشي asymptote", "limite_ecrite"), montre("إذن ماشي asymptote", "centre:1")])

SIM4 = sim("ex_d6_4", "Question 4 : f″ > 0, courbe convexe",
           "f″ positive : la courbe est au-dessus de ses tangentes.",
           D + "concavite.html?vue=roule", "Une tangente roule sur la courbe de x³ − 3x",
           "نشوفو على هاد l'exemple: x au cube moins trois x. فين f seconde positive، la courbe فوق les tangentes ديالها: convexe. شوف الجهة اليمنى: la tangente كتزلق، و la courbe ديما فوقها. وفين f seconde négative، la courbe تحت: concave. فالتمرين ديالك: f seconde ديما positive sur zéro، plus l'infini، إذن ما كاينش point d'inflexion.",
           [("f″ > 0 : convexe", "convexe"), ("f″ de signe constant : pas d'inflexion", "ما كاينش point d'inflexion")],
           [jusqua("نشوفو على هاد l'exemple", "courbe_tracee"), montre("convexe", "centre:0"), jusqua("شوف الجهة اليمنى", "courbe_au_dessus"),
            jusqua("وفين f seconde négative", "ligne_f_seconde"), montre("ما كاينش point d'inflexion", "centre:1")])

SIM5 = sim("ex_d6_5", "Question 5 : la restriction et l'intervalle J",
           "Continue et strictement monotone sur I : réciproque sur J = f(I).",
           D + "miroir.html?vue=restriction", "x² + 1 : on ne garde que la partie sur I = [0 ; +∞[",
           "نشوفو على هاد l'exemple: x carré plus un، كتهبط ومن بعد كتطلع، إذن ماشي monotone sur R. كناخدو غير la partie sur I، من zéro حتى plus l'infini: continue et strictement croissante. هاد la partie بوحدها هي اللي عندها réciproque. J هو f de I: من un حتى plus l'infini. فالتمرين ديالك: I من un حتى plus l'infini، و J كيبدا من g de un.",
           [("continue + strictement monotone sur I", "continue et strictement croissante"), ("J = f(I)", "J هو f de I")],
           [jusqua("نشوفو على هاد l'exemple", "parabole_entiere"), jusqua("continue et strictement croissante", "partie_sur_i"), montre("continue et strictement croissante", "centre:0"),
            jusqua("هاد la partie بوحدها", "reflet_de_la_partie"), jusqua("J هو f de I", "intervalle_j"), montre("J هو f de I", "centre:1")])

SIM6 = sim("ex_d6_6", "Question 6 : la dérivée de la réciproque en un point",
           "(f⁻¹)′(y₀) = 1/f′(x₀), avec f(x₀) = y₀ et f′(x₀) ≠ 0.",
           D + "miroir.html?vue=pentes", "x² + 1 : la tangente en A et son reflet en A′",
           "نشوفو على هاد l'exemple: f de x égale x carré plus un، و A فx égale deux، f de deux égale cinq. la pente ف A هي f prime de deux، égale quatre. الانعكاس ديالها ف A prime، عندها pente un quart. إذن f moins un prime de cinq، égale un sur f prime de deux. رد البال: cinq هي image، و deux هو l'antécédent. فالتمرين ديالك: trois هي image، لقا l'antécédent ديالها أولا.",
           [("(f⁻¹)′(y₀) = 1/f′(x₀), f(x₀) = y₀", "إذن f moins un prime de cinq"), ("y₀ est une image : chercher x₀", "رد البال")],
           [regle("نشوفو على هاد l'exemple", x_a=2), jusqua("la pente ف A", "triangle_a"), jusqua("الانعكاس ديالها", "triangle_reflet"),
            jusqua("إذن f moins un prime de cinq", "formule"), montre("إذن f moins un prime de cinq", "centre:0"), montre("رد البال", "centre:1")])

FA1 = qcm("fa_d6_1", "Plus facile : simplifier le taux", "سؤال ساهل على le taux.",
          "Pour x > 0, (x − 2√x)/x est égal à…", ["1 − 2√x", "1 − 2/√x", "x − 2"], 1, [
              (("قريب! racine de x sur x ماشي racine de x. عاود اختار.", "√x/x = 1/√x. Réessaie."),
               ("الجواب: un moins deux sur racine de x.", "Réponse : 1 − 2/√x.")),
              ("برافو! racine de x sur x، égale un sur racine de x.", "Juste : (x − 2√x)/x = 1 − 2/√x."),
              (("ما تقلقش. خاصك تقسم كل terme sur x. عاود اختار.", "Divise chaque terme par x. Réessaie."),
               ("الجواب: un moins deux sur racine de x.", "Réponse : 1 − 2/√x."))],
          "x moins deux racine de x، sur x، est égal à ?")

FA2 = qcm("fa_d6_2", "Plus facile : la dérivée de 2√x", "نتمرنو على la dérivée.",
          "La dérivée de 2√x est…", ["1/√x", "2/√x", "1/(2√x)"], 0, [
              ("برافو! deux fois un sur deux racine de x، égale un sur racine de x.", "Juste : (2√x)′ = 2 × 1/(2√x) = 1/√x."),
              (("قريب! نسيتي deux اللي فالتحت ف la dérivée ديال racine de x. عاود اختار.", "(√x)′ = 1/(2√x). Réessaie."),
               ("الجواب: un sur racine de x.", "Réponse : 1/√x.")),
              (("ما تقلقش. هادي la dérivée ديال racine de x بوحدها، نسيتي deux. عاود اختار.", "C'est (√x)′ ; multiplie par 2. Réessaie."),
               ("الجواب: un sur racine de x.", "Réponse : 1/√x."))],
          "La dérivée de deux racine de x est ?")

FA3 = association("fa_d6_3", "Plus facile : l'arbre des branches", "Relie chaque résultat à sa conclusion.",
                  "نتمرنو: ربط كل نتيجة مع الخلاصة ديالها.", "lim f(x) = +∞ en +∞. Relie chaque cas à la nature de la branche.",
                  [("1", "lim f(x)/x = +∞"), ("2", "lim f(x)/x = 0"), ("3", "lim f(x)/x = 1 et lim [f(x) − x] = −∞")],
                  [("a", "branche parabolique de direction (Oy)"), ("b", "branche parabolique de direction (Ox)"), ("c", "branche parabolique de direction y = x"), ("d", "asymptote oblique y = x")],
                  {"1": "a", "2": "b", "3": "c"},
                  {"1-a": ("Oui : f(x) grandit plus vite que toute droite.", "برافو: la courbe كتطلع بزربة، direction l'axe des ordonnées."),
                   "1-b": ("f(x)/x → 0 donne (Ox), pas +∞.", "لا، zéro هو اللي كيعطي l'axe des abscisses."),
                   "1-c": ("Pour y = x, il faut f(x)/x → 1.", "لا، باش تكون direction y égale x خاص f de x sur x يمشي ل un."),
                   "1-d": ("Une asymptote demande f(x)/x → a réel.", "لا، asymptote كتحتاج limite finie."),
                   "2-a": ("(Oy) correspond à f(x)/x → ±∞.", "لا، l'axe des ordonnées كيجي مع l'infini."),
                   "2-b": ("Oui : la courbe s'aplatit vers l'horizontale.", "برافو: zéro، direction l'axe des abscisses."),
                   "2-c": ("Pour y = x, il faut f(x)/x → 1.", "لا، خاص un، ماشي zéro."),
                   "2-d": ("Avec 0, pas d'asymptote oblique.", "لا، مع zéro ما كاينش asymptote oblique."),
                   "3-a": ("Ici f(x)/x tend vers 1, un réel.", "لا، هنا f de x sur x كيمشي ل un."),
                   "3-b": ("Ici f(x)/x tend vers 1, pas 0.", "لا، un ماشي zéro."),
                   "3-c": ("Oui : f(x) − x tend vers l'infini : branche parabolique de direction y = x.", "برافو: الفرق كيمشي ل l'infini: branche parabolique de direction y égale x."),
                   "3-d": ("Pour une asymptote, f(x) − x doit tendre vers un réel b.", "لا، asymptote كتحتاج الفرق يمشي ل عدد b.")},
                  ("(1 ; a) (2 ; b) (3 ; c) : la dernière limite décide.", "la limite اللخرة هي اللي كتقرر."))

FA4 = vrai_faux("fa_d6_4", "Plus facile : vrai ou faux", "f″(x) = 1/(2x√x) sur ]0 ; +∞[.", "سؤال ساهل: صحيح ولا غالط؟", [
    ("f″(x) > 0 pour tout x > 0.", True, "2x√x > 0 quand x > 0."),
    ("(C) a un point d'inflexion.", False, "f″ ne change jamais de signe sur ]0 ; +∞[."),
    ("(C) est convexe sur ]0 ; +∞[.", True, "f″ > 0 : la courbe est tournée vers le haut.")])

FA5 = qcm("fa_d6_5", "Plus facile : l'intervalle J", "سؤال ساهل على J.",
          "g est continue et strictement croissante sur [1 ; +∞[, g(1) = −1 et lim g = +∞. Alors J = …", ["]−1 ; +∞[", "[1 ; +∞[", "[−1 ; +∞["], 2, [
              (("قريب! g de un موجودة، إذن crochet fermé ف moins un. عاود اختار.", "−1 est atteint : crochet fermé. Réessaie."),
               ("الجواب: moins un، plus l'infini، مع crochet fermé.", "Réponse : [−1 ; +∞[.")),
              (("ما تقلقش. هادا I، ماشي J. J هو les images. عاود اختار.", "C'est I ; J est l'ensemble des images. Réessaie."),
               ("الجواب: moins un، plus l'infini.", "Réponse : [−1 ; +∞[.")),
              ("برافو! J égale g de I: من g de un حتى plus l'infini.", "Juste : J = [−1 ; +∞[.")],
          "J est égal à ?")

FA6 = qcm("fa_d6_6", "Plus facile : où dériver g ?", "سؤال ساهل على la réciproque.",
          "g(9) = 3. Pour calculer (g⁻¹)′(3), on utilise…", ["1/g′(3)", "1/g′(9)", "g′(9)"], 1, [
              (("قريب! trois هي image. l'antécédent ديالها هو neuf. عاود اختار.", "3 est une image ; son antécédent est 9. Réessaie."),
               ("الجواب: un sur g prime de neuf.", "Réponse : 1/g′(9).")),
              ("برافو! كنشتقو g ف l'antécédent، neuf.", "Juste : (g⁻¹)′(3) = 1/g′(9)."),
              (("ما تقلقش. خاص un sur، حيت les pentes كيتقلبو فالمراية. عاود اختار.", "Les pentes s'inversent : 1/g′. Réessaie."),
               ("الجواب: un sur g prime de neuf.", "Réponse : 1/g′(9)."))],
          "Pour calculer g moins un prime de trois, on utilise ?")

EX = {
    "id": ID, "type": "exercice", "version": 1, "status": "published",
    "matiere": "mathematiques", "chapitre": "derivation_etude_fonctions", "cours": "math_ch2_derivation_etude_fonctions",
    "titre": "Étude complète de x − 2√x et de sa réciproque", "niveau": "difficile", "duree_min": 45, "origine": ORIGINE,
    "competences": ["Étudier la dérivabilité à droite et le sens d'une demi-tangente", "Lever une forme +∞ − ∞ et dresser le tableau", "Déterminer une branche parabolique de direction y = ax", "Étudier la concavité par f″", "Montrer l'existence d'une réciproque et trouver J", "Calculer (f⁻¹)′ en un point"],
    "enonce": {
        "intro": "On considère la fonction f définie sur [0 ; +∞[ par f(x) = x − 2√x, et (C) sa courbe représentative dans un repère orthonormé (O, i, j).",
        "intro_dit": "دابا نقراو l'énoncé. f معرفة sur zéro، plus l'infini: f de x égale x moins deux racine de x. و C هي la courbe ديالها.",
        "figures": [figure("C", "x-2*sqrt(x)", 10, -2, 5, "Allure de (C) : f(x) = x − 2√x")],
        "donnees": ["f(x) = x − 2√x pour x ≥ 0", "g : restriction de f à I = [1 ; +∞["],
        "questions": [Q1, Q2, Q3, Q4, Q5, Q6]},
    "explication": deck("explication", "Explication animée", [SIM1, SIM2, SIM3, SIM4, SIM5, SIM6]),
    "facile": deck("facile", "Plus facile, pour s'entraîner", [FA1, FA2, FA3, FA4, FA5, FA6]),
    "similaire": {"id": ID + "_b", "titre": "Même exercice, autres données", "enonce": {
        "intro": "On considère la fonction h définie sur [0 ; +∞[ par h(x) = x − 4√x, et (C′) sa courbe ; k est la restriction de h à I = [4 ; +∞[.",
        "intro_dit": "نفس التمرين، بدالة أخرى: h de x égale x moins quatre racine de x، و k هي la restriction ديالها على quatre، plus l'infini.",
        "figures": [figure("C′", "x-4*sqrt(x)", 26, -5, 6, "Allure de (C′) : h(x) = x − 4√x")],
        "donnees": ["h(x) = x − 4√x pour x ≥ 0", "k : restriction de h à I = [4 ; +∞["],
        "questions": [
            {"id": "1", "texte": "Étudier la dérivabilité de h à droite en 0 et interpréter.",
             "reponse": phrase("(h(x) − h(0))/x = 1 − 4/√x → −∞ : h n'est pas dérivable à droite en 0 ; demi-tangente verticale en O dirigée vers le bas."),
             "clavier": {"aides": ["1 − 4/√x", "−∞"], "pieges": ["vers le haut"]},
             "correction": correction([("1 : (h(x) − h(0))/x = 1 − 4/√x → −∞ (x → 0⁺) : h non dérivable à droite en 0", "la limite égale moins l'infini"),
                                       ("demi-tangente verticale en O, dirigée vers le bas", "dirigée vers le bas")],
                                      "le taux هو un moins quatre sur racine de x، و la limite égale moins l'infini. h n'est pas dérivable à droite en zéro، demi-tangente verticale، dirigée vers le bas.")},
            {"id": "2", "texte": "Calculer lim h en +∞, montrer que h′(x) = (√x − 2)/√x pour x > 0, puis dresser le tableau de variations de h.",
             "reponse": phrase("h(x) = √x(√x − 4) → +∞ ; h′(x) = 1 − 2/√x = (√x − 2)/√x ; h décroissante sur [0 ; 4], croissante sur [4 ; +∞[ ; h(4) = −4."),
             "clavier": {"aides": ["√x(√x − 4)", "h(4) = −4"], "pieges": ["h′(x) = 1 − 4/√x"]},
             "correction": correction([("2 : h(x) = √x(√x − 4) → +∞ ; h′(x) = 1 − 2/√x = (√x − 2)/√x", "h prime de x égale un moins deux sur racine de x"),
                                       ("h′ a le signe de √x − 2 ; h(4) = −4 ; h : 0 ↘ −4 ↗ +∞", "h de quatre égale moins quatre")],
                                      "la limite égale plus l'infini. h prime de x égale un moins deux sur racine de x، و le signe هو le signe ديال racine de x moins deux. h de quatre égale moins quatre: décroissante ومن بعد croissante.")},
            {"id": "3", "texte": "Calculer lim h(x)/x et lim [h(x) − x] en +∞ ; nature de la branche infinie.",
             "reponse": phrase("h(x)/x = 1 − 4/√x → 1 ; h(x) − x = −4√x → −∞ : branche parabolique de direction la droite y = x au voisinage de +∞."),
             "clavier": {"aides": ["→ 1", "−4√x → −∞"], "pieges": ["asymptote y = x"]},
             "correction": correction([("3 : h(x)/x → 1 et h(x) − x = −4√x → −∞ : branche parabolique de direction y = x au voisinage de +∞", "branche parabolique de direction")],
                                      "h de x sur x كيمشي ل un، و h de x moins x كيمشي ل moins l'infini: branche parabolique de direction، la droite y égale x.")},
            {"id": "4", "texte": "Calculer h″(x) pour x > 0 et en déduire la concavité de (C′).",
             "reponse": phrase("h′(x) = 1 − 2/√x, h″(x) = 1/(x√x) > 0 : (C′) convexe sur ]0 ; +∞[."),
             "clavier": {"aides": ["h″(x) = 1/(x√x)", "convexe"], "pieges": ["point d'inflexion"]},
             "correction": correction([("4 : h″(x) = 1/(x√x) > 0 : (C′) est convexe sur ]0 ; +∞[", "h seconde de x égale un sur x racine de x")],
                                      "h seconde de x égale un sur x racine de x، positive، إذن la courbe convexe.")},
            {"id": "5", "texte": "Montrer que k admet une fonction réciproque définie sur un intervalle J à déterminer.",
             "reponse": phrase("k continue et strictement croissante sur [4 ; +∞[ : réciproque définie sur J = [−4 ; +∞[."),
             "clavier": {"aides": ["J = k(I)", "[−4 ; +∞["], "pieges": ["]−4 ; +∞["]},
             "correction": correction([("5 : k continue et strictement croissante sur I : réciproque sur J = [k(4) ; +∞[ = [−4 ; +∞[", "J égale moins quatre، plus l'infini")],
                                      "k continue et strictement croissante sur I، إذن عندها fonction réciproque، و J égale moins quatre، plus l'infini.")},
            {"id": "6", "texte": "Vérifier que k(25) = 5, puis calculer (k⁻¹)′(5).",
             "reponse": phrase("k(25) = 25 − 20 = 5 ; k′(25) = (5 − 2)/5 = 3/5 ≠ 0 ; (k⁻¹)′(5) = 1/k′(25) = 5/3 ≈ 1,67"),
             "clavier": {"aides": ["k⁻¹(5) = 25", "1/k′(25)"], "pieges": ["1/k′(5)"]},
             "correction": correction([("6 : k(25) = 25 − 4 × 5 = 5 ; k′(25) = 3/5 ≠ 0", "k prime de vingt-cinq égale trois cinquièmes"),
                                       ("(k⁻¹)′(5) = 1/k′(25) = 5/3", "cinq tiers")],
                                      "k de vingt-cinq égale cinq. k prime de vingt-cinq égale trois cinquièmes، ماشي zéro. إذن k moins un prime de cinq، égale cinq tiers.")}]}}
}
ecrire(EX)
