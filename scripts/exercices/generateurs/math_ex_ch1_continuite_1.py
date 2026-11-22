# Exercice pilote de maths (ch. 1, limites et continuité).
import json, sys
APP = "/media/simulations/maths/limites-continuite-tableau/approche.html?vue=trou"
RAC = "/media/simulations/maths/limites-continuite-tableau/raccord.html?vue=limite_image"

def rep(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}

def qcm_facile(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit):
    return {"id": sid, "slide_type": "exercise", "title": titre, "screen_content": {"lead": prompt}, "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": reactions}}}

def figure(nom, a, b, titre):
    """La courbe trouée de x ↦ x + a (pour x ≠ a… ici : (x² − a²)/(x − a) = x + a), trou en (a ; 2a)."""
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": -1, "max": b, "nom": "x", "graduations": list(range(0, b + 1))},
                     "y": {"min": -1, "max": 2 * a + 2, "nom": "y", "graduations": list(range(0, 2 * a + 3, 2 if a > 2 else 1))}},
            "legende": f"La courbe de {nom} a un trou au point d'abscisse {a} : {nom}({a}) n'est pas donnée par la même formule.",
            "elements": [{"f": "courbe", "expr": f"x+{a}", "de": -1, "a": b, "couleur": "cyan", "texte": f"y = {nom}(x)", "texte_x": b - 0.6, "pos": "no"},
                         {"f": "point", "at": [a, 2 * a], "creux": True, "couleur": "jaune"},
                         {"f": "repere", "x": a, "couleur": "faible"}]}

EX = {
  "id": "math_ex_ch1_continuite_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "mathematiques", "chapitre": "limites_continuite", "cours": "math_ch1_limites_continuite",
  "titre": "Une fonction trouée : limite et continuité en un point", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Lever une forme indéterminée 0/0 en factorisant", "Utiliser lim f(x) = f(a) pour la continuité en a"],
  "enonce": {
    "intro": "On considère la fonction f définie sur ℝ par : f(x) = (x² − 1)/(x − 1) si x ≠ 1, et f(1) = a, où a est un nombre réel.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا la fonction f، معرفة على R: f de x égale x carré moins un، sur x moins un، يلا كان x مختلف على un. وf de un égale a، وa هو nombre réel.",
    "figures": [figure("f", 1, 3, "La courbe de f(x) = (x² − 1)/(x − 1) pour x ≠ 1")],
    "donnees": ["f(x) = (x² − 1)/(x − 1) pour x ≠ 1", "f(1) = a"],
    "questions": [
      {"id": "1", "texte": "Calculer la limite de f(x) quand x tend vers 1.",
       "texte_dit": "السؤال un: حسب la limite ديال f de x، quand x tend vers un.",
       "reponse": {"type": "valeur", "grandeur": "lim f(x)", "valeur": 2, "tolerance": 0.001,
                   "attendu": "x² − 1 = (x − 1)(x + 1), donc pour x ≠ 1, f(x) = x + 1 ; lim f(x) = 1 + 1 = 2"},
       "clavier": {"aides": ["x² − 1", "(x − 1)(x + 1)", "x + 1", "lim"], "pieges": ["0/0 = 0", "f(1)"]},
       "aides": [
         {"texte": "Remplace x par 1 : tu trouves 0/0. C'est une forme indéterminée : il faut transformer f(x).",
          "dit": "عوض x ب un: كتلقى zéro sur zéro. هادي forme indéterminée، خاصك تبدل الكتابة ديال f de x."},
         {"texte": "Factorise le numérateur : x² − 1 = (x − 1)(x + 1), puis simplifie par (x − 1).",
          "dit": "factorise le numérateur: x carré moins un égale، x moins un، fois، x plus un. ومن بعد simplifie ب x moins un."}],
       "correction": {"lignes": [
           {"texte": "1 : en x = 1, on trouve 0/0 : forme indéterminée", "mot": "forme indéterminée"},
           {"texte": "x² − 1 = (x − 1)(x + 1)", "mot": "x carré moins un égale"},
           {"texte": "pour x ≠ 1 : f(x) = x + 1", "mot": "f de x égale x plus un"},
           {"texte": "lim f(x) = 1 + 1 = 2  (x → 1)", "mot": "la limite égale deux"}],
         "parole": "السؤال un. ملي كنعوضو x ب un، كنلقاو zéro sur zéro: forme indéterminée. x carré moins un égale، x moins un، fois، x plus un. إذن، يلا كان x مختلف على un، f de x égale x plus un. ملي x كيقرب ل un، la limite égale deux."},
       "explication": "ex_m1", "facile": "fa_m1"},
      {"id": "2", "texte": "Déterminer la valeur de a pour que f soit continue en 1.",
       "texte_dit": "السؤال deux: لقا la valeur ديال a، باش تكون f continue en un.",
       "reponse": {"type": "valeur", "grandeur": "a", "valeur": 2, "tolerance": 0.001,
                   "attendu": "f est continue en 1 si lim f(x) = f(1), soit a = 2"},
       "clavier": {"aides": ["lim f(x) = f(1)", "a =", "continue"], "pieges": ["a = 0", "a = 1"]},
       "aides": [
         {"texte": "Une fonction est continue en 1 quand sa limite en 1 est égale à son image f(1).",
          "dit": "la fonction continue en un، ملي la limite ديالها en un، كتساوي l'image f de un."},
         {"texte": "La limite vaut 2 (question 1) et f(1) = a : écris l'égalité.",
          "dit": "la limite كتساوي deux، من السؤال un، وf de un égale a. كتب l'égalité."}],
       "correction": {"lignes": [
           {"texte": "2 : f continue en 1 ⇔ lim f(x) = f(1)", "mot": "continue en un"},
           {"texte": "lim f(x) = 2 et f(1) = a", "mot": "la limite égale deux"},
           {"texte": "donc a = 2", "mot": "a égale deux"}],
         "parole": "السؤال deux. f continue en un، يعني la limite en un كتساوي f de un. la limite égale deux، وf de un égale a. إذن a égale deux."},
       "explication": "ex_m2", "facile": "fa_m2"},
      {"id": "3", "texte": "On prend a = 3. La fonction f est-elle continue en 1 ? Justifier.",
       "texte_dit": "السؤال trois: ناخدو a égale trois. واش f continue en un؟ برر الجواب ديالك.",
       "reponse": {"type": "phrase", "attendu": "Non : lim f(x) = 2 en 1, mais f(1) = 3 ; la limite n'est pas égale à l'image, donc f n'est pas continue en 1."},
       "clavier": {"aides": ["lim f(x) = 2", "f(1) = 3", "≠", "n'est pas continue"], "pieges": ["continue"]},
       "aides": [
         {"texte": "Compare deux nombres : la limite en 1 (question 1) et l'image f(1) = 3.",
          "dit": "قارن جوج حوايج: la limite en un، من السؤال un، وl'image f de un égale trois."},
         {"texte": "2 ≠ 3 : la courbe arrive à la hauteur 2, mais le point est à la hauteur 3.",
          "dit": "deux ماشي هو trois: la courbe كتوصل للعلو deux، ولكن le point فالعلو trois."}],
       "correction": {"lignes": [
           {"texte": "3 : lim f(x) = 2 en 1", "mot": "la limite en un égale deux"},
           {"texte": "f(1) = a = 3", "mot": "f de un égale trois"},
           {"texte": "2 ≠ 3 : f n'est pas continue en 1", "mot": "n'est pas continue en un"}],
         "parole": "السؤال trois. la limite en un égale deux، وf de un égale trois. deux ماشي هو trois، إذن f n'est pas continue en un."},
       "explication": "ex_m3", "facile": "fa_m3"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_m1", "slide_type": "simulation", "title": "Question 1 : la limite en 1, là où mène la courbe",
     "screen_content": {"lead": "Pour x ≠ 1, f(x) = x + 1 : la courbe est une droite trouée en (1 ; 2)."},
     "visual": {"kind": "simulation", "url": APP, "caption": "Un point glisse sur la courbe vers x = 1"},
     "speech_text": {"mixed": "شوف la courbe. هادي droite، ولكن فيها trou فx égale un. علاش؟ حيت ملي كنعوضو x ب un، كنلقاو zéro sur zéro. نفكوها: x carré moins un égale، x moins un، fois، x plus un. إذن f de x égale x plus un، يلا كان x مختلف على un. دابا شوف le point M كيقرب ل un من اليسار، ومن اليمين. f de x كتقرب ل deux. le trou باقي خاوي، ولكن la limite égale deux."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "x² − 1 = (x − 1)(x + 1)", "mot": "نفكوها"}, {"texte": "f(x) = x + 1 (x ≠ 1)", "mot": "إذن f de x égale x plus un"}, {"texte": "lim f(x) = 2", "mot": "ولكن la limite égale deux"}],
       "pointage": [{"mot": "شوف la courbe", "commande": "play_until", "parametres": {"moment": "courbe_tracee"}},
                    {"mot": "فيها trou", "repere": "trou"},
                    {"mot": "نفكوها", "cible": "centre:0"},
                    {"mot": "إذن f de x égale x plus un", "cible": "centre:1"},
                    {"mot": "كيقرب ل un من اليسار", "commande": "play_until", "parametres": {"moment": "proche_gauche"}},
                    {"mot": "ومن اليمين", "commande": "play_until", "parametres": {"moment": "proche_droite"}},
                    {"mot": "le trou باقي خاوي", "commande": "play_until", "parametres": {"moment": "limite_lue"}},
                    {"mot": "ولكن la limite égale deux", "cible": "centre:2"}]}},
    {"id": "ex_m2", "slide_type": "simulation", "title": "Question 2 : boucher le trou avec f(1) = 2",
     "screen_content": {"lead": "f est continue en 1 quand le point (1 ; f(1)) bouche le trou : lim f(x) = f(1)."},
     "visual": {"kind": "simulation", "url": RAC, "caption": "Le point (1 ; a) monte ou descend jusqu'au trou"},
     "speech_text": {"mixed": "la courbe كتوصل للعلو deux فx égale un: هادي هي la limite. دابا le point ديال f de un، اللي هو a. يلا حطيناه فالعلو deux، كيسد le trou، وla courbe كتولي بلا قطع. هادي هي la continuité: la limite égale l'image. إذن a égale deux."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "f continue en 1 ⇔ lim f(x) = f(1)", "mot": "la limite égale l'image"}, {"texte": "a = 2", "mot": "إذن a égale deux"}],
       "pointage": [{"mot": "la courbe كتوصل للعلو deux", "commande": "set_parameters", "parametres": {"fa": 2}},
                    {"mot": "هادي هي la limite", "commande": "play_until", "parametres": {"moment": "limite_lue"}},
                    {"mot": "يلا حطيناه فالعلو deux", "commande": "play_until", "parametres": {"moment": "image_placee"}},
                    {"mot": "la limite égale l'image", "commande": "play_until", "parametres": {"moment": "comparaison"}},
                    {"mot": "إذن a égale deux", "cible": "centre:1"}]}},
    {"id": "ex_m3", "slide_type": "simulation", "title": "Question 3 : avec a = 3, le point est ailleurs",
     "screen_content": {"lead": "Avec f(1) = 3, la courbe arrive à 2 mais le point est à 3 : f n'est pas continue en 1."},
     "visual": {"kind": "simulation", "url": RAC, "caption": "Le point (1 ; 3) ne bouche pas le trou"},
     "speech_text": {"mixed": "دابا a égale trois. la courbe باقي كتوصل للعلو deux. ولكن le point ديال f de un، فالعلو trois. le trou باقي خاوي، وle point بعيد عليه. la limite égale deux، وf de un égale trois. إذن f n'est pas continue en un."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "lim f(x) = 2 ≠ f(1) = 3", "mot": "la limite égale deux، وf de un égale trois"}, {"texte": "f n'est pas continue en 1", "mot": "إذن f n'est pas continue en un"}],
       "pointage": [{"mot": "دابا a égale trois", "commande": "set_parameters", "parametres": {"fa": 3}},
                    {"mot": "la courbe باقي كتوصل للعلو deux", "commande": "play_until", "parametres": {"moment": "limite_lue"}},
                    {"mot": "فالعلو trois", "commande": "play_until", "parametres": {"moment": "image_placee"}},
                    {"mot": "la limite égale deux، وf de un égale trois", "commande": "play_until", "parametres": {"moment": "comparaison"}},
                    {"mot": "إذن f n'est pas continue en un", "cible": "centre:1"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_m1", "Plus facile : la factorisation", "نتمرنو بسؤال ساهل: اختار la bonne factorisation.",
      "Quelle est la factorisation de x² − 1 ?", ["(x − 1)(x + 1)", "(x − 1)²", "x(x − 1)"], 0, {
        "0": {"juste": rep("برافو عليك! x carré moins un égale، x moins un، fois، x plus un. ومن بعد كنبسطو ب x moins un.", "Juste : x² − 1 = (x − 1)(x + 1).")},
        "1": {"1": rep("ما تقلقش. نشرو، x moins un، au carré: كنلقاو x carré moins deux x plus un، ماشي x carré moins un. عاود اختار.", "(x − 1)² = x² − 2x + 1, pas x² − 1. Réessaie."),
              "2": rep("الجواب هو، x moins un، fois، x plus un. هادي identité remarquable: a carré moins b carré.", "Réponse : (x − 1)(x + 1), identité a² − b².")},
        "2": {"1": rep("قريب! نشرو x fois، x moins un: كنلقاو x carré moins x، ماشي x carré moins un. عاود اختار.", "x(x − 1) = x² − x, pas x² − 1. Réessaie."),
              "2": rep("الجواب هو، x moins un، fois، x plus un. x fois، x moins un، كتعطي x carré moins x.", "Réponse : (x − 1)(x + 1).")}},
      "Quelle est la factorisation de x carré moins un ?"),
    qcm_facile("fa_m2", "Plus facile : la définition de la continuité", "سؤال ساهل على la continuité.",
      "f est continue en 1 si…", ["lim f(x) = f(1) quand x tend vers 1", "f(1) = 0", "f(x) = 0/0 en 1"], 0, {
        "0": {"juste": rep("برافو! f continue en un، ملي la limite en un كتساوي l'image f de un.", "Juste : f continue en 1 ⇔ lim f(x) = f(1).")},
        "1": {"1": rep("ما تقلقش. f de un ممكن تكون أي قيمة. المهم هو نقارنو la limite مع l'image. عاود اختار.", "f(1) peut valoir n'importe quoi : on compare la limite et l'image. Réessaie."),
              "2": rep("الجواب هو la limite égale l'image. f de un égale zéro ما كافياش.", "Réponse : lim f(x) = f(1).")},
        "2": {"1": rep("قريب! zéro sur zéro هي forme indéterminée، ماشي la continuité. عاود اختار.", "0/0 est une forme indéterminée, pas une continuité. Réessaie."),
              "2": rep("الجواب هو la limite égale l'image f de un.", "Réponse : lim f(x) = f(1).")}},
      "f est continue en un si ?"),
    {"id": "fa_m3", "slide_type": "exercise", "title": "Plus facile : vrai ou faux", "screen_content": {"lead": "lim f(x) = 2 en 1 et f(1) = 3."},
     "visual": {"kind": "none"}, "speech_text": {"mixed": "سؤال ساهل: قول واش هاد الجمل صحيحة ولا غالطة."},
     "exercises": [{"type": "vrai_faux", "prompt": "Vrai ou faux ?", "statements": [
        {"text": "f est continue en 1, car f(1) existe.", "correct": False, "explanation": "Il ne suffit pas que f(1) existe : il faut lim f(x) = f(1). Ici 2 ≠ 3."},
        {"text": "f n'est pas continue en 1, car lim f(x) ≠ f(1).", "correct": True, "explanation": "La limite vaut 2 et l'image 3 : elles sont différentes."}]}],
     "concentration": {"demarrer": "reset"}}
  ]}]},
  "similaire": {
    "id": "math_ex_ch1_continuite_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "On considère la fonction g définie sur ℝ par : g(x) = (x² − 9)/(x − 3) si x ≠ 3, et g(3) = b.",
      "intro_dit": "نفس التمرين، بدالة أخرى: g de x égale x carré moins neuf، sur x moins trois، يلا كان x مختلف على trois، وg de trois égale b.",
      "figures": [figure("g", 3, 5, "La courbe de g(x) = (x² − 9)/(x − 3) pour x ≠ 3")],
      "donnees": ["g(x) = (x² − 9)/(x − 3) pour x ≠ 3", "g(3) = b"],
      "questions": [
        {"id": "1", "texte": "Calculer la limite de g(x) quand x tend vers 3.",
         "reponse": {"type": "valeur", "grandeur": "lim g(x)", "valeur": 6, "tolerance": 0.001, "attendu": "x² − 9 = (x − 3)(x + 3), donc g(x) = x + 3 pour x ≠ 3 ; lim g(x) = 6"},
         "clavier": {"aides": ["x² − 9", "(x − 3)(x + 3)", "x + 3"], "pieges": ["0/0 = 0"]},
         "correction": {"lignes": [{"texte": "x² − 9 = (x − 3)(x + 3)", "mot": "x carré moins neuf"}, {"texte": "g(x) = x + 3 pour x ≠ 3", "mot": "g de x égale x plus trois"}, {"texte": "lim g(x) = 6", "mot": "la limite égale six"}],
                        "parole": "x carré moins neuf égale، x moins trois، fois، x plus trois. إذن g de x égale x plus trois، يلا كان x مختلف على trois. la limite égale six."}},
        {"id": "2", "texte": "Déterminer b pour que g soit continue en 3.",
         "reponse": {"type": "valeur", "grandeur": "b", "valeur": 6, "tolerance": 0.001, "attendu": "lim g(x) = g(3) ⇔ b = 6"},
         "clavier": {"aides": ["lim g(x) = g(3)", "b ="], "pieges": ["b = 0"]},
         "correction": {"lignes": [{"texte": "g continue en 3 ⇔ lim g(x) = g(3)", "mot": "continue en trois"}, {"texte": "b = 6", "mot": "b égale six"}],
                        "parole": "g continue en trois، يعني la limite كتساوي g de trois. إذن b égale six."}},
        {"id": "3", "texte": "On prend b = 5. g est-elle continue en 3 ? Justifier.",
         "reponse": {"type": "phrase", "attendu": "Non : lim g(x) = 6 mais g(3) = 5 ; 6 ≠ 5, donc g n'est pas continue en 3."},
         "clavier": {"aides": ["lim g(x) = 6", "g(3) = 5", "≠"], "pieges": ["continue"]},
         "correction": {"lignes": [{"texte": "lim g(x) = 6 et g(3) = 5", "mot": "la limite égale six"}, {"texte": "6 ≠ 5 : g n'est pas continue en 3", "mot": "n'est pas continue en trois"}],
                        "parole": "la limite égale six، وg de trois égale cinq. six ماشي هو cinq، إذن g n'est pas continue en trois."}}
      ]}}
}
json.dump(EX, open(sys.argv[1], "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
print("ok", sys.argv[1])
