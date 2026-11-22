# Exercice pilote de physique (ch. 1, ondes mécaniques) : écrit en Python pour un JSON sûr.
import json, math, sys

def aspect(v, theta, t1, x0, longueur, y0=0.45, k=0.4, n=90):
    """Forme de la corde à t1 (même perturbation que corde.html : montée rapide sur 30 % de θ, descente lente)."""
    def forme(u):
        if u < 0 or u > 1: return 0.0
        return math.sin(math.pi / 2 * u / 0.3) if u < 0.3 else math.cos(math.pi / 2 * (u - 0.3) / 0.7)
    pts = []
    for i in range(n + 1):
        x = longueur * i / n
        pts.append([round(x0 + x, 3), round(y0 + k * forme((t1 - x / v) / theta), 3)])
    return pts
SIM = "/media/simulations/physics/ondes-tableau/corde.html"

def rep(parole, ecrit):
    return {"parole": parole, "ecrit": ecrit}

def qcm_facile(sid, titre, intro, prompt, options, bonne, reactions, enonce_dit):
    """Diapositive « version facile » : une petite intro dite, puis le QCM avec une réaction préparée par option."""
    return {"id": sid, "slide_type": "exercise", "title": titre,
            "screen_content": {"lead": prompt},
            "visual": {"kind": "none"},
            "speech_text": {"mixed": intro},
            "question": {"type": "qcm", "prompt": prompt, "options": options, "correct": bonne, "enonce_dit": enonce_dit},
            "concentration": {"demarrer": "reset", "reponses": {"q": reactions}}}

EX = {
  "id": "phys_ex_ch1_corde_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "physique", "chapitre": "ondes_mecaniques", "cours": "phys_ch1_waves_exemple",
  "titre": "Une perturbation le long d'une corde", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer la célérité v = d/Δt", "Calculer un retard τ = SM/v", "Calculer la longueur d'une perturbation ℓ = v·θ"],
  "enonce": {
    "intro": "Une corde élastique, de longueur 2 m, est tendue horizontalement. À la date t = 0, on provoque au bout S de la corde une perturbation de courte durée θ = 0,4 s. Elle se propage le long de la corde sans amortissement. La figure représente l'aspect de la corde à la date t₁ = 0,6 s : le front de l'onde est alors au point P.",
    "intro_dit": "دابا نقراو l'énoncé. عندنا une corde élastique، طولها deux mètres، ممدودة أفقيا. فt égale zéro، كنديرو فالطرف S une perturbation قصيرة، المدة ديالها thêta égale zéro virgule quatre seconde. la perturbation كتمشي فla corde بلا ما تضعاف. la figure كتبين la corde فt un égale zéro virgule six seconde: le front ديال l'onde وصل للنقطة P.",
    "figures": [{
      "type": "schema", "titre": "Aspect de la corde à t₁ = 0,6 s", "cadre": {"l": 2.3, "h": 1.3},
      "legende": "Le front de l'onde est en P : la partie de la corde après P est encore au repos.",
      "elements": [
        {"f": "ligne", "pts": aspect(1.0, 0.4, 0.6, 0.1, 2.0), "couleur": "orange", "epais": True},
        {"f": "point", "at": [0.1, 0.45], "t": "S", "pos": "so", "couleur": "jaune"},
        {"f": "point", "at": [0.68, 0.45], "t": "P", "pos": "se", "couleur": "cyan"},
        {"f": "cote", "de": [0.1, 0.15], "a": [0.68, 0.15], "t": "SP = 0,6 m", "couleur": "cyan", "pos": "s"},
        {"f": "fleche", "de": [1.1, 0.95], "a": [1.6, 0.95], "texte": "sens de propagation", "couleur": "blanc", "pos": "n"},
        {"f": "texte", "at": [1.9, 1.15], "t": "t₁ = 0,6 s", "couleur": "jaune", "ancre": "centre"}
      ]}],
    "donnees": ["θ = 0,4 s (durée de la perturbation)", "SP = 0,6 m à la date t₁ = 0,6 s", "SM = 0,8 m (question 2)"],
    "questions": [
      {"id": "1", "texte": "Calculer la célérité v de l'onde le long de la corde.",
       "texte_dit": "السؤال un: حسب la célérité v ديال l'onde فla corde.",
       "reponse": {"type": "valeur", "grandeur": "v", "valeur": 1, "unite": "m/s", "tolerance": 0.03,
                   "attendu": "v = SP/t₁ = 0,6/0,6 = 1 m/s"},
       "clavier": {"aides": ["v = d/Δt", "SP", "t₁", "m/s"], "pieges": ["v = Δt/d", "km/h"]},
       "aides": [
         {"texte": "Pendant la durée t₁, le front est parti de S et il est arrivé en P : quelle distance a-t-il parcourue ?",
          "dit": "شوف la figure: من t égale zéro حتى t un، le front خرج من S ووصل ل P. شحال قطع ديال la distance؟"},
         {"texte": "La célérité est la distance parcourue par le front divisée par la durée : v = SP/t₁.",
          "dit": "la célérité هي la distance اللي قطع le front، على la durée. إذن v égale SP sur t un. عوض بالقيم."}],
       "correction": {"lignes": [
           {"texte": "1 : le front parcourt SP pendant la durée t₁", "mot": "le front قطع SP"},
           {"texte": "v = SP/t₁ = 0,6/0,6", "mot": "v égale SP sur t un"},
           {"texte": "v = 1 m/s", "mot": "v égale un mètre par seconde"}],
         "parole": "السؤال un. من t égale zéro حتى t un، le front قطع SP. إذن v égale SP sur t un، يعني zéro virgule six sur zéro virgule six. v égale un mètre par seconde."},
       "explication": "ex_c1", "facile": "fa_c1"},
      {"id": "2", "texte": "Un point M de la corde est à la distance SM = 0,8 m de S. Calculer le retard τ du mouvement de M par rapport à celui de S.",
       "texte_dit": "السؤال deux: النقطة M بعيدة على S ب SM égale zéro virgule huit mètre. حسب le retard tau ديال M بالنسبة ل S.",
       "reponse": {"type": "valeur", "grandeur": "τ", "valeur": 0.8, "unite": "s", "tolerance": 0.03,
                   "attendu": "τ = SM/v = 0,8/1 = 0,8 s"},
       "clavier": {"aides": ["τ = SM/v", "SM", "v", "s"], "pieges": ["τ = v/SM", "τ = SM·v"]},
       "aides": [
         {"texte": "M refait le mouvement de S plus tard : le retard est la durée que met le front pour aller de S à M.",
          "dit": "M كدير نفس الحركة ديال S، ولكن من بعد. le retard هو la durée اللي كياخد le front باش يمشي من S ل M."},
         {"texte": "Pendant τ, le front parcourt SM à la célérité v : τ = SM/v.",
          "dit": "فهاد la durée، le front كيقطع SM بla célérité v. إذن tau égale SM sur v."}],
       "correction": {"lignes": [
           {"texte": "2 : le front va de S à M pendant τ", "mot": "le front كيمشي من S ل M"},
           {"texte": "τ = SM/v = 0,8/1", "mot": "tau égale SM sur v"},
           {"texte": "τ = 0,8 s", "mot": "tau égale zéro virgule huit seconde"}],
         "parole": "السؤال deux. le front كيمشي من S ل M فla durée tau. إذن tau égale SM sur v، يعني zéro virgule huit sur un. tau égale zéro virgule huit seconde."},
       "explication": "ex_c2", "facile": "fa_c2"},
      {"id": "3", "texte": "Calculer la longueur ℓ de la perturbation sur la corde.",
       "texte_dit": "السؤال trois: حسب la longueur l ديال la perturbation فوق la corde.",
       "reponse": {"type": "valeur", "grandeur": "ℓ", "valeur": 0.4, "unite": "m", "tolerance": 0.03,
                   "attendu": "ℓ = v·θ = 1 × 0,4 = 0,4 m"},
       "clavier": {"aides": ["ℓ = v·θ", "θ", "v", "m"], "pieges": ["ℓ = v/θ", "ℓ = θ/v"]},
       "aides": [
         {"texte": "La perturbation dure θ : pendant θ, son début a déjà avancé ; la longueur est la distance entre son début et sa fin.",
          "dit": "la perturbation كتدوم thêta. فهاد la durée، البداية ديالها كتكون مشات. la longueur هي la distance بين البداية والنهاية ديالها."},
         {"texte": "Pendant θ, le front avance de v·θ : ℓ = v·θ.",
          "dit": "فla durée thêta، le front كيقطع v fois thêta. إذن l égale v fois thêta."}],
       "correction": {"lignes": [
           {"texte": "3 : pendant θ, le front avance de v·θ", "mot": "le front كيقطع v fois thêta"},
           {"texte": "ℓ = v·θ = 1 × 0,4", "mot": "l égale v fois thêta"},
           {"texte": "ℓ = 0,4 m", "mot": "l égale zéro virgule quatre mètre"}],
         "parole": "السؤال trois. فla durée thêta، le front كيقطع v fois thêta. إذن l égale v fois thêta، يعني un fois zéro virgule quatre. l égale zéro virgule quatre mètre."},
       "explication": "ex_c3", "facile": "fa_c3"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_c1", "slide_type": "simulation", "title": "Question 1 : la célérité, lue sur le front",
     "screen_content": {"lead": "Le front part de S à t = 0 et arrive en P à t₁ : v = SP/t₁."},
     "visual": {"kind": "simulation", "url": SIM + "?vue=front", "caption": "Le front avance le long de la corde"},
     "speech_text": {"mixed": "شوف la corde. فt égale zéro، la source S كتبدا تتحرك. la perturbation كتمشي، وle front هو أول نقطة كتبدا تتحرك. شوف le front كيتقدم. كل ما زاد le temps، كيقطع distance كبيرة. la célérité هي la distance اللي قطع le front، على la durée. فالتمرين، le front قطع SP égale zéro virgule six mètre، فzéro virgule six seconde. إذن v égale SP sur t un، يعني un mètre par seconde."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "v = SP/t₁", "mot": "إذن v égale SP sur t un"}, {"texte": "v = 0,6/0,6 = 1 m/s", "mot": "يعني un mètre par seconde"}],
       "pointage": [{"mot": "la source S كتبدا تتحرك", "commande": "start"},
                    {"mot": "شوف le front كيتقدم", "commande": "play_until", "parametres": {"moment": "toute_sur_corde"}},
                    {"mot": "إذن v égale SP sur t un", "cible": "centre:0"},
                    {"mot": "يعني un mètre par seconde", "cible": "centre:1"}]}},
    {"id": "ex_c2", "slide_type": "simulation", "title": "Question 2 : le retard τ du point M",
     "screen_content": {"lead": "M refait le mouvement de S, plus tard : τ = SM/v."},
     "visual": {"kind": "simulation", "url": SIM + "?vue=retard", "caption": "S et M : le même mouvement, décalé de τ"},
     "speech_text": {"mixed": "دابا شوف النقطة M، اللي بعيدة على S ب zéro virgule huit mètre. S كتتحرك الأولى. من بعد، كتوصل la perturbation ل M، وM كدير نفس الحركة. لتحت، deux courbes: نفس الشكل، غير M جات من بعد. هاد le décalage هو le retard tau. فهاد la durée، le front قطع SM. إذن tau égale SM sur v، يعني zéro virgule huit sur un. tau égale zéro virgule huit seconde."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "τ = SM/v", "mot": "إذن tau égale SM sur v"}, {"texte": "τ = 0,8/1 = 0,8 s", "mot": "tau égale zéro virgule huit seconde"}],
       "pointage": [{"mot": "S كتتحرك الأولى", "commande": "start"},
                    {"mot": "كتوصل la perturbation ل M", "commande": "play_until", "parametres": {"moment": "m_atteint"}},
                    {"mot": "هاد le décalage هو le retard tau", "repere": "retard_tau"},
                    {"mot": "إذن tau égale SM sur v", "cible": "centre:0"},
                    {"mot": "tau égale zéro virgule huit seconde", "cible": "centre:1"}]}},
    {"id": "ex_c3", "slide_type": "simulation", "title": "Question 3 : la longueur de la perturbation",
     "screen_content": {"lead": "Pendant la durée θ, le front avance de v·θ : c'est la longueur ℓ."},
     "visual": {"kind": "simulation", "url": SIM + "?vue=longueur", "caption": "Toute la perturbation est sur la corde"},
     "speech_text": {"mixed": "la source كتتحرك غير thêta égale zéro virgule quatre seconde، ومن بعد كترجع ترتاح. فهاد la durée، le front كيتقدم. ملي كترجع S للراحة، la perturbation كاملة فوق la corde. la longueur ديالها هي la distance اللي قطع le front فthêta. إذن l égale v fois thêta، يعني un fois zéro virgule quatre. l égale zéro virgule quatre mètre."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "ℓ = v·θ", "mot": "إذن l égale v fois thêta"}, {"texte": "ℓ = 1 × 0,4 = 0,4 m", "mot": "l égale zéro virgule quatre mètre"}],
       "pointage": [{"mot": "la source كتتحرك غير thêta", "commande": "start"},
                    {"mot": "la perturbation كاملة فوق la corde", "commande": "play_until", "parametres": {"moment": "toute_sur_corde"}},
                    {"mot": "إذن l égale v fois thêta", "cible": "centre:0"},
                    {"mot": "l égale zéro virgule quatre mètre", "cible": "centre:1"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_c1", "Plus facile : la célérité", "نتمرنو بسؤال ساهل. اختار la bonne relation.",
      "Le front a parcouru SP = 0,6 m en t₁ = 0,6 s. Quelle relation donne la célérité ?",
      ["v = SP/t₁", "v = t₁/SP", "v = SP·t₁"], 0, {
        "0": {"juste": rep("برافو عليك! la célérité هي la distance على la durée: v égale SP sur t un، يعني un mètre par seconde.", "Juste : v = SP/t₁ = 0,6/0,6 = 1 m/s.")},
        "1": {"1": rep("ما تقلقش. شوف l'unité: la célérité بالمتر على الثانية. واش t un sur SP كتعطي mètre par seconde؟ عاود اختار.", "Regarde l'unité : m/s, c'est des mètres divisés par des secondes. Réessaie."),
              "2": rep("الجواب هو v égale SP sur t un. la distance هي اللي فوق، وla durée تحت، باش نلقاو mètre par seconde.", "Réponse : v = SP/t₁ (distance sur durée, en m/s).")},
        "2": {"1": rep("قريب! ولكن ملي كنضربو la distance فla durée، كنلقاو mètre fois seconde، ماشي mètre par seconde. عاود اختار.", "Un produit donne des m·s, pas des m/s. Réessaie."),
              "2": rep("الجواب هو v égale SP sur t un. خاصنا نقسمو la distance على la durée، ماشي نضربوهم.", "Réponse : v = SP/t₁ : on divise la distance par la durée.")}},
      "Le front a parcouru SP égale zéro virgule six mètre en t un égale zéro virgule six seconde. Quelle relation donne la célérité ?"),
    qcm_facile("fa_c2", "Plus facile : le retard", "سؤال ساهل على le retard. اختار الجواب الصحيح.",
      "v = 1 m/s et SM = 0,8 m. Le retard de M par rapport à S vaut…",
      ["τ = 0,8 s", "τ = 1,25 s", "τ = 0,08 s"], 0, {
        "0": {"juste": rep("برافو! tau égale SM sur v، يعني zéro virgule huit sur un، zéro virgule huit seconde.", "Juste : τ = SM/v = 0,8/1 = 0,8 s.")},
        "1": {"1": rep("ما تقلقش. un virgule vingt-cinq كتجي من v sur SM. le retard هو la distance على la célérité. عاود اختار.", "1,25 vient de v/SM ; le retard est SM/v. Réessaie."),
              "2": rep("الجواب هو zéro virgule huit seconde. tau égale SM sur v، ماشي v sur SM.", "Réponse : τ = SM/v = 0,8 s (et non v/SM).")},
        "2": {"1": rep("قريب! ولكن شوف القسمة: zéro virgule huit sur un، شحال كتعطي؟ عاود اختار.", "Refais la division : 0,8 ÷ 1 = ? Réessaie."),
              "2": rep("الجواب هو zéro virgule huit seconde. zéro virgule huit sur un كتعطي zéro virgule huit، ماشي zéro virgule zéro huit.", "Réponse : 0,8/1 = 0,8 s.")}},
      "v égale un mètre par seconde et SM égale zéro virgule huit mètre. Le retard de M par rapport à S vaut ?"),
    {"id": "fa_c3", "slide_type": "exercise", "title": "Plus facile : vrai ou faux",
     "screen_content": {"lead": "La perturbation dure θ = 0,4 s et v = 1 m/s."},
     "visual": {"kind": "none"},
     "speech_text": {"mixed": "سؤال ساهل: قول واش هاد الجملة صحيحة ولا غالطة."},
     "exercises": [{"type": "vrai_faux", "prompt": "Vrai ou faux ?", "statements": [
        {"text": "La longueur de la perturbation est ℓ = v·θ = 0,4 m.", "correct": True, "explanation": "Pendant θ, le front avance de v·θ = 1 × 0,4 = 0,4 m."},
        {"text": "La longueur de la perturbation est ℓ = v/θ = 2,5 m.", "correct": False, "explanation": "v/θ n'est pas une longueur ; ℓ = v·θ = 0,4 m."}]}],
     "concentration": {"demarrer": "reset"}}
  ]}]},
  "similaire": {
    "id": "phys_ex_ch1_corde_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Une corde de longueur 3 m est tendue horizontalement. À t = 0, on provoque au bout S une perturbation de durée θ = 0,2 s. À la date t₁ = 0,8 s, le front de l'onde est au point P, avec SP = 1,2 m.",
      "intro_dit": "نفس التمرين، بقيم أخرى. une corde طولها trois mètres. فt égale zéro، كنديرو فS une perturbation، المدة ديالها thêta égale zéro virgule deux seconde. فt un égale zéro virgule huit seconde، le front وصل ل P، وSP égale un virgule deux mètre.",
      "figures": [{
        "type": "schema", "titre": "Aspect de la corde à t₁ = 0,8 s", "cadre": {"l": 3.3, "h": 1.3},
        "elements": [
          {"f": "ligne", "pts": aspect(1.5, 0.2, 0.8, 0.1, 3.0, n=120), "couleur": "orange", "epais": True},
          {"f": "point", "at": [0.1, 0.45], "t": "S", "pos": "so", "couleur": "jaune"},
          {"f": "point", "at": [1.3, 0.45], "t": "P", "pos": "se", "couleur": "cyan"},
          {"f": "cote", "de": [0.1, 0.15], "a": [1.3, 0.15], "t": "SP = 1,2 m", "couleur": "cyan", "pos": "s"},
          {"f": "texte", "at": [2.7, 1.15], "t": "t₁ = 0,8 s", "couleur": "jaune", "ancre": "centre"}]}],
      "donnees": ["θ = 0,2 s", "SP = 1,2 m à t₁ = 0,8 s", "SM = 0,9 m (question 2)"],
      "questions": [
        {"id": "1", "texte": "Calculer la célérité v de l'onde.",
         "reponse": {"type": "valeur", "grandeur": "v", "valeur": 1.5, "unite": "m/s", "tolerance": 0.03, "attendu": "v = SP/t₁ = 1,2/0,8 = 1,5 m/s"},
         "clavier": {"aides": ["v = d/Δt", "SP", "t₁", "m/s"], "pieges": ["v = Δt/d"]},
         "correction": {"lignes": [{"texte": "v = SP/t₁ = 1,2/0,8", "mot": "v égale SP sur t un"}, {"texte": "v = 1,5 m/s", "mot": "un virgule cinq mètre par seconde"}],
                        "parole": "v égale SP sur t un، يعني un virgule deux sur zéro virgule huit. v égale un virgule cinq mètre par seconde."}},
        {"id": "2", "texte": "M est à SM = 0,9 m de S. Calculer le retard τ de M par rapport à S.",
         "reponse": {"type": "valeur", "grandeur": "τ", "valeur": 0.6, "unite": "s", "tolerance": 0.03, "attendu": "τ = SM/v = 0,9/1,5 = 0,6 s"},
         "clavier": {"aides": ["τ = SM/v", "SM", "v", "s"], "pieges": ["τ = v/SM"]},
         "correction": {"lignes": [{"texte": "τ = SM/v = 0,9/1,5", "mot": "tau égale SM sur v"}, {"texte": "τ = 0,6 s", "mot": "zéro virgule six seconde"}],
                        "parole": "tau égale SM sur v، يعني zéro virgule neuf sur un virgule cinq. tau égale zéro virgule six seconde."}},
        {"id": "3", "texte": "Calculer la longueur ℓ de la perturbation.",
         "reponse": {"type": "valeur", "grandeur": "ℓ", "valeur": 0.3, "unite": "m", "tolerance": 0.03, "attendu": "ℓ = v·θ = 1,5 × 0,2 = 0,3 m"},
         "clavier": {"aides": ["ℓ = v·θ", "θ", "v", "m"], "pieges": ["ℓ = v/θ"]},
         "correction": {"lignes": [{"texte": "ℓ = v·θ = 1,5 × 0,2", "mot": "l égale v fois thêta"}, {"texte": "ℓ = 0,3 m", "mot": "zéro virgule trois mètre"}],
                        "parole": "l égale v fois thêta، يعني un virgule cinq fois zéro virgule deux. l égale zéro virgule trois mètre."}}
      ]}}
}
import re
def _voix(o):
    if isinstance(o, dict): return {k: _voix(v) for k, v in o.items()}
    if isinstance(o, list): return [_voix(v) for v in o]
    if isinstance(o, str):
        return o.replace("thêta", "teta").replace("l égale", "L égale").replace("la longueur l ", "la longueur L ")
    return o
EX = _voix(EX)
json.dump(EX, open(sys.argv[1], "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
print("ok", sys.argv[1])
