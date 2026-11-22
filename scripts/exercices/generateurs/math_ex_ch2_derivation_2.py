# Exercice de maths, ch. 2 (dérivation et étude des fonctions), niveau FACILE (s'entraîner) :
# limites d'un polynôme, f′(x) factorisée, signe de f′, tableau de variations, extremums.
# Sources comparées (lecture seule, rien de copié) :
#  - exploration/derivation_etude_fonctions.json : cas types montrer_derivee, signe_derivee_variations, pièges « signe à vue »,
#    « flèche incompatible avec les limites », « extremum sans changement de signe » ; erreurs_examen (tableau incomplet).
#  - vidéos des profs (Driss DOTCOM : de f′ au signe puis au tableau ; maths variés : résumé, extremums ; Math_houara).
#  - nationaux 2016-2025 : « dresser le tableau de variations » dans 18 sujets sur 20 (fonctions ln/exp, non reprises).
#  - séries en ligne repérées (titres et résumés de recherche ; sites non joignables depuis la session) : talamidi série 1
#    et exercices non corrigés 2-3, Lycée Mohammed Serraj (monstremath), devoirs Hammouda (scribd), alloschool (étude de
#    fonctions polynômes) : le polynôme de degré 3 à deux racines entières de f′ est l'entraînement classique.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import *  # noqa

D = "/media/simulations/maths/derivation-tableau/"
ID = "math_ex_ch2_derivation_2"
VAR = D + "variations.html?vue=glisse"


def figure(nom, expr, xmin, xmax, ymin, ymax, titre):
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": xmin, "max": xmax, "nom": "x", "graduations": list(range(xmin + 1, xmax))},
                     "y": {"min": ymin, "max": ymax, "nom": "y", "graduations": list(range(ymin - ymin % 5 + 5, ymax, 5))}},
            "legende": f"La courbe ({nom}) de la fonction, pour vérifier le tableau de variations.",
            "elements": [{"f": "courbe", "expr": expr, "de": xmin, "a": xmax, "couleur": "cyan", "texte": f"({nom})", "texte_x": xmax - 0.6, "pos": "no"}]}


Q1 = {"id": "1", "texte": "Calculer la limite de f(x) quand x tend vers −∞, puis quand x tend vers +∞.",
      "texte_dit": "السؤال un: حسب la limite ديال f de x، quand x tend vers moins l'infini، ومن بعد quand x tend vers plus l'infini.",
      "reponse": phrase("En ±∞, un polynôme a la limite de son terme de plus haut degré : lim f(x) = lim x³ = −∞ quand x → −∞, et lim f(x) = lim x³ = +∞ quand x → +∞."),
      "clavier": {"aides": ["lim x³", "−∞", "+∞", "terme de plus haut degré"], "pieges": ["+∞ − ∞", "lim f(x) = +∞ en −∞"]},
      "aides": [aide("À l'infini, un polynôme se comporte comme son terme de plus haut degré.",
                     "فاللانهاية، le polynôme كيتصرف بحال le terme de plus haut degré ديالو."),
                aide("Ici, c'est x³. Que vaut x³ quand x est un très grand nombre négatif ? et positif ?",
                     "هنا هو x au cube. شنو كيعطي x au cube ملي x عدد négatif كبير بزاف؟ وملي x positif كبير؟")],
      "correction": correction([
          ("1 : lim f(x) = lim x³ = −∞  (x → −∞)", "moins l'infini"),
          ("lim f(x) = lim x³ = +∞  (x → +∞)", "plus l'infini")],
          "السؤال un. فاللانهاية، le polynôme عندو la limite ديال le terme de plus haut degré، هنا x au cube. quand x tend vers moins l'infini، la limite égale moins l'infini. و quand x tend vers plus l'infini، la limite égale plus l'infini."),
      "explication": "ex_d2_1", "facile": "fa_d2_1"}

Q2 = {"id": "2", "texte": "Montrer que pour tout x de ℝ : f′(x) = 3(x + 1)(x − 3).",
      "texte_dit": "السؤال deux: بين بلي لكل x من R، f prime de x égale trois، facteur de x plus un، facteur de x moins trois.",
      "reponse": phrase("f est dérivable sur ℝ (polynôme) et f′(x) = 3x² − 6x − 9 = 3(x² − 2x − 3) = 3(x + 1)(x − 3)."),
      "clavier": {"aides": ["f est dérivable sur ℝ", "f′(x) = 3x² − 6x − 9", "3(x² − 2x − 3)", "(x + 1)(x − 3)"], "pieges": ["f′(x) = 3x² − 6x − 9 + 2", "3(x − 1)(x + 3)"]},
      "aides": [aide("Dérive terme à terme : (x³)′ = 3x², (−3x²)′ = −6x, (−9x)′ = −9, et la constante 2 donne 0.",
                     "derive كل terme: x au cube كتعطي trois x carré، moins trois x carré كتعطي moins six x، moins neuf x كتعطي moins neuf، و deux كتعطي zéro."),
                aide("Mets 3 en facteur, puis développe (x + 1)(x − 3) pour vérifier que tu retrouves x² − 2x − 3.",
                     "خرج trois facteur، ومن بعد نشر، x plus un، fois، x moins trois، وشوف واش كتلقى x carré moins deux x moins trois.")],
      "correction": correction([
          ("2 : f est dérivable sur ℝ et f′(x) = 3x² − 6x − 9", "f prime de x égale trois x carré moins six x moins neuf"),
          ("= 3(x² − 2x − 3)", "كنخرجو trois facteur"),
          ("or (x + 1)(x − 3) = x² − 3x + x − 3 = x² − 2x − 3", "كنشرو"),
          ("donc f′(x) = 3(x + 1)(x − 3)", "إذن f prime de x égale trois")],
          "السؤال deux. f dérivable sur R حيت polynôme، و f prime de x égale trois x carré moins six x moins neuf. كنخرجو trois facteur: trois، facteur de x carré moins deux x moins trois. كنشرو، x plus un، fois، x moins trois، كنلقاو x carré moins deux x moins trois. إذن f prime de x égale trois، facteur de x plus un، facteur de x moins trois."),
      "explication": "ex_d2_2", "facile": "fa_d2_2"}

Q3 = {"id": "3", "texte": "Étudier le signe de f′(x), puis dresser le tableau de variations de f.",
      "texte_dit": "السؤال trois: درس le signe ديال f prime de x، ومن بعد دير le tableau de variations ديال f.",
      "reponse": phrase("3 > 0 : f′(x) a le signe de (x + 1)(x − 3) : positif sur ]−∞ ; −1[ et ]3 ; +∞[, négatif sur ]−1 ; 3[. f est strictement croissante sur ]−∞ ; −1], strictement décroissante sur [−1 ; 3], strictement croissante sur [3 ; +∞[ ; f(−1) = 7, f(3) = −25 ; f va de −∞ à 7, puis de 7 à −25, puis de −25 à +∞."),
      "clavier": {"aides": ["le signe de f′(x) est le signe de (x + 1)(x − 3)", "f(−1) = 7", "f(3) = −25", "croissante", "décroissante"], "pieges": ["f(−1) = −7", "f′ négatif sur ]−∞ ; −1["]},
      "aides": [aide("3 est positif : le signe de f′(x) est celui de (x + 1)(x − 3), un produit qui s'annule en −1 et en 3. Fais le tableau de signe.",
                     "trois positif: le signe ديال f prime de x هو le signe ديال، x plus un، fois، x moins trois. هاد le produit، s'annule en moins un، et en trois. دير tableau de signe."),
                aide("Un trinôme est du signe de son coefficient de x² à l'extérieur des racines. Calcule f(−1) et f(3) pour les bouts des flèches.",
                     "le trinôme عندو le signe ديال le coefficient ديال x carré برا من les racines. ومن بعد حسب f de moins un و f de trois باش تكمل les flèches.")],
      "correction": correction([
          ("3 : 3 > 0, donc le signe de f′(x) est le signe de (x + 1)(x − 3)", "le signe ديال f prime de x"),
          ("f′(x) > 0 sur ]−∞ ; −1[ et sur ]3 ; +∞[ ;  f′(x) < 0 sur ]−1 ; 3[", "positif برا من moins un و trois"),
          ("f(−1) = −1 − 3 + 9 + 2 = 7 ;  f(3) = 27 − 27 − 27 + 2 = −25", "f de moins un égale sept"),
          ("x : −∞ ↗ −1 ↘ 3 ↗ +∞ ;  f : −∞ ↗ 7 ↘ −25 ↗ +∞", "le tableau")],
          "السؤال trois. trois positif، إذن le signe ديال f prime de x هو le signe ديال، x plus un، fois، x moins trois. هو positif برا من moins un و trois، و négatif بيناتهم. f de moins un égale sept، و f de trois égale moins vingt-cinq. le tableau: f croissante من moins l'infini حتى sept، décroissante من sept حتى moins vingt-cinq، ومن بعد croissante حتى plus l'infini."),
      "explication": "ex_d2_3", "facile": "fa_d2_3"}

Q4 = {"id": "4", "texte": "En déduire que f admet un maximum local, et donner sa valeur.",
      "texte_dit": "السؤال quatre: استنتج بلي f عندها maximum local، وعطي la valeur ديالو.",
      "reponse": valeur("maximum local", 7, "f′ s'annule en −1 en changeant de signe (+ puis −) : f admet un maximum local en −1, f(−1) = 7"),
      "clavier": {"aides": ["f′ s'annule en −1 en changeant de signe", "maximum local", "f(−1) ="], "pieges": ["f(3) = −25", "f′(−1) = 0 donc maximum"]},
      "aides": [aide("Regarde dans ton tableau où la flèche monte puis descend.", "شوف فالتابلو ديالك فين la flèche طالعة ومن بعد هابطة."),
                aide("Écris la phrase complète : f′ s'annule en −1 en changeant de signe, donc f(−1) est un extremum.",
                     "كتب الجملة كاملة: f prime، s'annule en moins un، en changeant de signe، إذن f de moins un هو extremum.")],
      "correction": correction([
          ("4 : f′ s'annule en −1 en changeant de signe (+ puis −)", "en changeant de signe"),
          ("donc f admet un maximum local en −1 : f(−1) = 7", "le maximum local égale sept"),
          ("(de même, minimum local f(3) = −25)", "minimum local")],
          "السؤال quatre. f prime، s'annule en moins un، en changeant de signe: plus ومن بعد moins. إذن f عندها maximum local ف moins un، و le maximum local égale sept. وبنفس الطريقة، ف trois كاين minimum local، moins vingt-cinq."),
      "explication": "ex_d2_4", "facile": "fa_d2_4"}

SIM1 = sim("ex_d2_1", "Question 1 : les limites d'un polynôme",
           "En −∞ et en +∞, le terme de plus haut degré l'emporte.",
           VAR, "La courbe de x³ − 3x et son tableau de variations",
           "نشوفو على هاد l'exemple: la courbe ديال x au cube moins trois x. شوف اللخر ديالها: على اليسار كتهبط بلا حد، وعلى اليمين كتطلع بلا حد. علاش؟ ملي x كبير بزاف، x au cube كيغلب moins trois x. إذن la limite هي la limite ديال x au cube: moins l'infini فاليسار، و plus l'infini فاليمين. وهادو هوما اللي كنكتبو فالبداية وفاللخر ديال le tableau. فالتمرين ديالك: le terme de plus haut degré هو حتى هو x au cube.",
           [("en ±∞ : lim polynôme = lim terme de plus haut degré", "x au cube كيغلب"), ("lim x³ = −∞ (−∞) ; +∞ (+∞)", "moins l'infini فاليسار")],
           [jusqua("نشوفو على هاد l'exemple", "courbe_tracee"), {"mot": "نشوفو على هاد l'exemple", "repere": "courbe"},
            montre("x au cube كيغلب", "centre:0"), montre("moins l'infini فاليسار", "centre:1"),
            jusqua("وهادو هوما اللي كنكتبو", "tableau_complet"), {"mot": "وهادو هوما اللي كنكتبو", "repere": "ligne_fleches"}])

SIM2 = sim("ex_d2_2", "Question 2 : dériver puis factoriser",
           "f′(x) se factorise pour qu'on puisse lire son signe.",
           D + "calculs.html?vue=va3", "Le calcul de f′ écrit au tableau sur x³ − 3x",
           "نشوفو la méthode على هاد l'exemple: f de x égale x au cube moins trois x. أول جملة: f dérivable sur R. من بعد كنشتقو: trois x carré moins trois. كنخرجو trois facteur، ومن بعد x carré moins un، كيتفك: x moins un، fois، x plus un. علاش كنفكو؟ باش نقراو le signe. فالتمرين ديالك نفس الشي: derive، خرج trois، و فك le trinôme. ومن بعد نشر باش تتأكد بلي لقيتي نفس l'expression.",
           [("(3x² − 3)′ … = 3(x − 1)(x + 1)", "كنخرجو trois facteur"), ("on factorise pour lire le signe", "باش نقراو le signe")],
           [jusqua("أول جملة", "derivable"), jusqua("كنخرجو trois facteur", "factorise"), montre("كنخرجو trois facteur", "centre:0"),
            jusqua("باش نقراو le signe", "phrase"), montre("باش نقراو le signe", "centre:1")])

SIM3 = sim("ex_d2_3", "Question 3 : du signe de f′ au tableau",
           "f′ > 0 : la courbe monte ; f′ < 0 : elle descend.",
           VAR, "Un point P glisse ; le tableau se remplit à son passage",
           "نتبعو النقطة P على la courbe ديال x au cube moins trois x. فاللول la tangente طالعة: f prime positive، و la flèche طالعة. ف moins un، la tangente horizontale، ومن بعد كتهبط: f prime négative، و la flèche هابطة. ف un، la tangente horizontale مرة أخرى، ومن بعد كتطلع. le tableau كامل: x، le signe ديال f prime، و les flèches، وفالراس ديال كل flèche كنكتبو القيمة: deux، و moins deux. فالتمرين ديالك: الأعداد هوما moins un و trois، وحسب f ديالهم.",
           [("f′ > 0 : ↗ ;  f′ < 0 : ↘", "f prime positive"), ("au bout des flèches : les valeurs f(x₀)", "وفالراس ديال كل flèche")],
           [jusqua("فاللول la tangente طالعة", "monte"), montre("f prime positive", "centre:0"), jusqua("ومن بعد كتهبط", "descend"),
            jusqua("ف un، la tangente horizontale", "creux"), jusqua("le tableau كامل", "tableau_complet"),
            {"mot": "le tableau كامل", "repere": "tableau"}, montre("وفالراس ديال كل flèche", "centre:1")])

SIM4 = sim("ex_d2_4", "Question 4 : un maximum, lu dans le tableau",
           "f′ s'annule en changeant de signe : extremum.",
           VAR, "Le sommet de la courbe de x³ − 3x",
           "شوف القمة ديال la courbe ديال x au cube moins trois x. قبل moins un، f prime positive. من بعد moins un، f prime négative. f prime، s'annule en changeant de signe: إذن f de moins un هو maximum local، و هنا كيساوي deux. رد البال: ماشي كافي نقولو f prime égale zéro: خاص le signe يتبدل. فالتمرين ديالك: شوف الأعداد اللي فيهم la flèche طالعة ومن بعد هابطة.",
           [("f′ s'annule en x₀ en changeant de signe ⇒ extremum", "en changeant de signe"), ("ici : maximum local f(−1) = 2", "maximum local")],
           [jusqua("شوف القمة", "sommet"), {"mot": "شوف القمة", "repere": "sommet"}, montre("en changeant de signe", "centre:0"),
            montre("maximum local", "centre:1"), jusqua("ماشي كافي", "tableau_complet")])

FA1 = qcm("fa_d2_1", "Plus facile : la limite d'un polynôme", "سؤال ساهل على la limite.",
          "Quand x tend vers −∞, x³ − 3x² − 9x + 2 tend vers…", ["+∞", "−∞", "2"], 1, [
              (("قريب! x au cube ديال عدد négatif كيبقى négatif. عاود اختار.", "Le cube d'un nombre négatif est négatif. Réessaie."),
               ("الجواب هو moins l'infini: x au cube كيمشي ل moins l'infini.", "Réponse : −∞, comme x³.")),
              ("برافو! le terme de plus haut degré هو x au cube، وكيمشي ل moins l'infini.", "Juste : lim x³ = −∞ en −∞."),
              (("ما تقلقش. deux هو la constante، كتبقى صغيرة قدام x au cube. عاود اختار.", "La constante 2 ne compte pas devant x³. Réessaie."),
               ("الجواب هو moins l'infini: x au cube هو اللي كيغلب.", "Réponse : −∞."))],
          "Quand x tend vers moins l'infini, la limite est ?")

FA2 = qcm("fa_d2_2", "Plus facile : la bonne dérivée", "نتمرنو على la dérivée.",
          "La dérivée de x³ − 3x² − 9x + 2 est…", ["3x² − 6x − 9", "3x² − 6x − 9 + 2", "x² − 6x − 9"], 0, [
              ("برافو! trois x carré moins six x moins neuf، و la constante كتعطي zéro.", "Juste : f′(x) = 3x² − 6x − 9."),
              (("قريب! la dérivée ديال la constante deux هي zéro. عاود اختار.", "La dérivée d'une constante est 0. Réessaie."),
               ("الجواب هو trois x carré moins six x moins neuf: deux كتعطي zéro.", "Réponse : 3x² − 6x − 9.")),
              (("ما تقلقش. x au cube كتعطي trois x carré، ماشي x carré. عاود اختار.", "(x³)′ = 3x². Réessaie."),
               ("الجواب هو trois x carré moins six x moins neuf: l'exposant كينزل قدام.", "Réponse : 3x² − 6x − 9."))],
          "La dérivée de x au cube moins trois x carré moins neuf x plus deux est ?")

FA3 = association("fa_d2_3", "Plus facile : signe et sens", "Relie chaque intervalle au signe de f′ et au sens de f.",
                  "نتمرنو: ربط كل intervalle مع le signe ديال f prime.", "Relie chaque intervalle à ce qui s'y passe.",
                  [("1", "]−∞ ; −1["), ("2", "]−1 ; 3["), ("3", "]3 ; +∞[")],
                  [("a", "f′ > 0 : f croissante"), ("b", "f′ < 0 : f décroissante")],
                  {"1": "a", "2": "b", "3": "a"},
                  {"1-a": ("Oui : à gauche de −1, les deux facteurs sont négatifs, le produit est positif.", "برافو: قبل moins un، le produit positif، f croissante."),
                   "1-b": ("Teste x = −2 : 3(−1)(−5) = 15 > 0.", "لا، جرب x égale moins deux: كتلقى quinze، positif."),
                   "2-a": ("Teste x = 0 : 3(1)(−3) = −9 < 0.", "لا، جرب x égale zéro: كتلقى moins neuf، négatif."),
                   "2-b": ("Oui : entre les racines, le trinôme est négatif.", "برافو: بين les racines، le trinôme négatif، f décroissante."),
                   "3-a": ("Oui : à droite de 3, les deux facteurs sont positifs.", "برافو: من بعد trois، le produit positif، f croissante."),
                   "3-b": ("Teste x = 4 : 3(5)(1) = 15 > 0.", "لا، جرب x égale quatre: كتلقى quinze، positif.")},
                  ("(1 ; a) (2 ; b) (3 ; a) : f monte, descend, puis remonte.", "f طالعة، ومن بعد هابطة، ومن بعد طالعة."))

FA4 = vrai_faux("fa_d2_4", "Plus facile : vrai ou faux", "f′ s'annule en −1 et en 3.", "سؤال ساهل: صحيح ولا غالط؟", [
    ("f(−1) = 7 est un maximum local, car f′ passe de + à − en −1.", True, "Changement de signe + puis − : la courbe monte puis descend."),
    ("Il suffit que f′(x₀) = 0 pour avoir un extremum.", False, "Il faut que f′ change de signe en x₀."),
    ("f(3) = −25 est un minimum local.", True, "f′ passe de − à + en 3.")])

EX = {
    "id": ID, "type": "exercice", "version": 1, "status": "published",
    "matiere": "mathematiques", "chapitre": "derivation_etude_fonctions", "cours": "math_ch2_derivation_etude_fonctions",
    "titre": "Variations d'un polynôme de degré 3", "niveau": "facile", "duree_min": 20, "origine": ORIGINE,
    "competences": ["Calculer les limites d'un polynôme en ±∞", "Montrer que f′(x) = une forme donnée", "Dresser un tableau de variations", "Déterminer un extremum"],
    "enonce": {
        "intro": "On considère la fonction f définie sur ℝ par f(x) = x³ − 3x² − 9x + 2, et (C) sa courbe représentative dans un repère orthonormé.",
        "intro_dit": "دابا نقراو l'énoncé. f معرفة على R: f de x égale x au cube moins trois x carré moins neuf x plus deux. و C هي la courbe ديالها.",
        "figures": [figure("C", "x^3-3*x^2-9*x+2", -3, 5, -30, 10, "La courbe (C) de f(x) = x³ − 3x² − 9x + 2")],
        "donnees": ["f(x) = x³ − 3x² − 9x + 2, pour tout x réel"],
        "questions": [Q1, Q2, Q3, Q4]},
    "explication": deck("explication", "Explication animée", [SIM1, SIM2, SIM3, SIM4]),
    "facile": deck("facile", "Plus facile, pour s'entraîner", [FA1, FA2, FA3, FA4]),
    "similaire": {"id": ID + "_b", "titre": "Même exercice, autres données", "enonce": {
        "intro": "On considère la fonction g définie sur ℝ par g(x) = x³ + 3x² − 9x − 1.",
        "intro_dit": "نفس التمرين، بدالة أخرى: g de x égale x au cube plus trois x carré moins neuf x moins un.",
        "figures": [figure("C′", "x^3+3*x^2-9*x-1", -5, 3, -10, 30, "La courbe (C′) de g(x) = x³ + 3x² − 9x − 1")],
        "donnees": ["g(x) = x³ + 3x² − 9x − 1, pour tout x réel"],
        "questions": [
            {"id": "1", "texte": "Calculer les limites de g en −∞ et en +∞.",
             "reponse": phrase("lim g(x) = lim x³ = −∞ en −∞ ; lim g(x) = lim x³ = +∞ en +∞."),
             "clavier": {"aides": ["lim x³", "−∞", "+∞"], "pieges": ["+∞ − ∞"]},
             "correction": correction([("1 : lim g(x) = −∞ (x → −∞) ; lim g(x) = +∞ (x → +∞)", "la limite ديال x au cube")],
                                      "le terme de plus haut degré هو x au cube: la limite ديال x au cube، moins l'infini فاليسار، و plus l'infini فاليمين.")},
            {"id": "2", "texte": "Montrer que pour tout x de ℝ : g′(x) = 3(x − 1)(x + 3).",
             "reponse": phrase("g′(x) = 3x² + 6x − 9 = 3(x² + 2x − 3) = 3(x − 1)(x + 3)."),
             "clavier": {"aides": ["g′(x) = 3x² + 6x − 9", "3(x² + 2x − 3)"], "pieges": ["3(x + 1)(x − 3)"]},
             "correction": correction([("2 : g′(x) = 3x² + 6x − 9 = 3(x² + 2x − 3)", "trois x carré plus six x moins neuf"),
                                       ("(x − 1)(x + 3) = x² + 2x − 3, donc g′(x) = 3(x − 1)(x + 3)", "إذن g prime de x")],
                                      "g prime de x égale trois x carré plus six x moins neuf، يعني trois، facteur de x carré plus deux x moins trois. ونشر، x moins un، fois، x plus trois، كيعطي نفس الشي. إذن g prime de x égale trois، facteur de x moins un، facteur de x plus trois.")},
            {"id": "3", "texte": "Étudier le signe de g′(x) et dresser le tableau de variations de g.",
             "reponse": phrase("g′ > 0 sur ]−∞ ; −3[ et ]1 ; +∞[, g′ < 0 sur ]−3 ; 1[ ; g(−3) = 26, g(1) = −6 ; g : −∞ ↗ 26 ↘ −6 ↗ +∞."),
             "clavier": {"aides": ["g(−3) = 26", "g(1) = −6"], "pieges": ["g(−3) = −26"]},
             "correction": correction([("3 : g′(x) a le signe de (x − 1)(x + 3) : + sur ]−∞ ; −3[, − sur ]−3 ; 1[, + sur ]1 ; +∞[", "le signe ديال g prime"),
                                       ("g(−3) = −27 + 27 + 27 − 1 = 26 ; g(1) = 1 + 3 − 9 − 1 = −6", "g de moins trois égale vingt-six"),
                                       ("g : −∞ ↗ 26 ↘ −6 ↗ +∞", "le tableau")],
                                      "le signe ديال g prime هو le signe ديال، x moins un، fois، x plus trois: positif برا من moins trois و un. g de moins trois égale vingt-six، و g de un égale moins six. le tableau: طالعة حتى vingt-six، هابطة حتى moins six، ومن بعد طالعة.")},
            {"id": "4", "texte": "En déduire que g admet un maximum local, et donner sa valeur.",
             "reponse": valeur("maximum local", 26, "g′ s'annule en −3 en changeant de signe : maximum local g(−3) = 26"),
             "clavier": {"aides": ["en changeant de signe", "g(−3) ="], "pieges": ["g(1) = −6"]},
             "correction": correction([("4 : g′ s'annule en −3 en changeant de signe : maximum local g(−3) = 26", "le maximum local égale vingt-six")],
                                      "g prime، s'annule en moins trois، en changeant de signe، إذن le maximum local égale vingt-six.")}]}}
}
ecrire(EX)
