# Exercice SVT ch. 3 (notion de l'information génétique), niveau facile : la courbe de la quantité d'ADN par cellule
# au cours du cycle cellulaire (phases G1, S, G2, M ; durées ; phase S ; anaphase et retour à q).
# Entraîne : lire une courbe phase par phase avec les valeurs, nommer les phases, calculer des durées par différence
# (sans oublier M), expliquer q → 2q (réplication en S, chromosome à deux chromatides) et 2q → q (anaphase : clivage du
# centromère, chromatides sœurs vers les pôles opposés ; deux cellules filles à q).
# Sources comparées (lues, rien copié) :
# - exploration notion_information_genetique.json : cas_types « courbe_adn » (très fréquente aux contrôles : Ouissam,
#   Maison Des Sciences, Driss, Wessal), « duree_cycle » ; pieges (réplication en G1/G2, « oublie M », « même pôle ») ;
#   erreurs_examen « courbe de l'ADN (contrôles) » ; variantes_admises « où la quantité redescend à q » (fin de mitose,
#   séparation des chromatides à l'anaphase) et « G1/G2 = croissance, jamais phase de repos ».
# - nationaux PC : 2018 R restitution (deux caractéristiques des chromosomes à l'anaphase de la mitose) ; 2024 N
#   (réplication en phase S) ; 2024 R (G1 monochromatidien, fin de S bichromatidien) — formes reprises, aucune situation.
# - séries en ligne (recherche du 22/11/2026 : dyrassa « Notion de l'information génétique, série d'exercices »,
#   dreamjob.ma « mitose, cours et exercices corrigés » (courbe 2Q/Q), moutamadris activités 2 Bac SP, alloschool) :
#   seuls les titres et résumés de recherche ont pu être lus, le réseau du conteneur refuse ces sites ; la courbe
#   q → 2q → q en UA et heures y est la situation classique.
# Pas de radioactivité ici (thymidine : exercice difficile de l'autre série).
import sys
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

CYCLE = "/media/simulations/svt/notion_information_genetique-tableau/cycle.html"
MITOSE = "/media/simulations/svt/notion_information_genetique-tableau/mitose.html"


def courbe_adn(g1, s, g2, m, q, xmax, ymax, titre):
    """Quantité d'ADN par cellule : palier q (G1), montée q → 2q (S), palier 2q (G2), retour à q à la fin de M."""
    pts = [[0, q], [g1, q], [s, 2 * q], [round(m - 0.2, 2), 2 * q], [m, q], [xmax, q]]
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": 0, "max": xmax, "nom": "t", "unite": "h", "graduations": list(range(0, xmax + 1, 2))},
                     "y": {"min": 0, "max": ymax, "nom": "quantité d'ADN", "unite": "UA", "graduations": list(range(0, ymax + 1, 2))}},
            "legende": "Quantité d'ADN dans le noyau d'une cellule de méristème ; après la division, la mesure suit l'une des deux cellules filles.",
            "elements": [
                {"f": "ligne", "pts": pts, "couleur": "cyan", "epais": True},
                {"f": "repere", "x": g1}, {"f": "repere", "x": s}, {"f": "repere", "x": g2}, {"f": "repere", "x": m},
                {"f": "texte", "at": [g1 / 2, ymax - 0.7], "t": "A", "couleur": "jaune"},
                {"f": "texte", "at": [(g1 + s) / 2, ymax - 0.7], "t": "B", "couleur": "jaune"},
                {"f": "texte", "at": [(s + g2) / 2, ymax - 0.7], "t": "C", "couleur": "jaune"},
                {"f": "texte", "at": [(g2 + m) / 2, ymax - 0.7], "t": "D", "couleur": "jaune"}]}


def assoc_phases(sid, q, qq):
    """Association des parties A, B, C, D de la courbe avec les phases ; un retour pour chaque paire."""
    gauche = [("1", f"A : palier à {q} UA, au début"), ("2", f"B : montée de {q} à {qq} UA"),
              ("3", f"C : palier à {qq} UA"), ("4", f"D : retour à {q} UA, à la fin")]
    droite = [("a", "G1"), ("b", "S"), ("c", "G2"), ("d", "Mitose (M)")]
    nq, nqq = {4: "quatre", 5: "cinq"}[q], {8: "huit", 10: "dix"}[qq]
    g_txt = {"1": f"A reste constante à {q} UA, au début du cycle", "2": f"B monte de {q} à {qq} UA",
             "3": f"C reste constante à {qq} UA", "4": f"D revient à {q} UA, à la fin du cycle"}
    g_dit = {"1": f"A كتبقى ثابتة، à {nq} unités arbitraires، فالبداية ديال le cycle",
             "2": f"B كتطلع، de {nq} à {nqq} unités arbitraires",
             "3": f"C كتبقى ثابتة، à {nqq} unités arbitraires",
             "4": f"D كترجع، à {nq} unités arbitraires، فاللخر ديال le cycle"}
    d_txt = {"a": "en G1, la quantité reste à q, avant la réplication", "b": "en S, la quantité monte de q à 2q",
             "c": "en G2, la quantité reste à 2q, après la réplication", "d": "en mitose, la quantité revient à q, à la fin du cycle"}
    d_dit = {"a": "ف G un، la quantité ثابتة à q، قبل la réplication", "b": "ف S، la quantité كتطلع، de q à deux q",
             "c": "ف G deux، la quantité ثابتة à deux q، من بعد la réplication",
             "d": "فla mitose، la quantité كترجع à q، فاللخر ديال le cycle"}
    noms = {"a": ("G1", "G un"), "b": ("la phase S", "la phase S"), "c": ("G2", "G deux"), "d": ("la mitose", "la mitose")}
    couples = {"1": "a", "2": "b", "3": "c", "4": "d"}
    retours = {}
    for g, _ in gauche:
        for d, _ in droite:
            if couples[g] == d:
                retours[f"{g}-{d}"] = (True, f"Oui : {g_txt[g]} : c'est {noms[d][0]}.", f"برافو. {g_dit[g]}: هادي {noms[d][1]}.")
            else:
                retours[f"{g}-{d}"] = (False, f"Non : {d_txt[d]}. Or {g_txt[g]}. Cherche une autre phase.",
                                       f"لا. {d_dit[d]}. ولكن {g_dit[g]}. قلب على phase أخرى.")
    return association(sid, "Plus facile : relier la courbe et les phases", "Relie chaque partie de la courbe à sa phase.",
                       "سؤال ساهل: ربط كل جزء ديال la courbe مع la phase ديالو.",
                       "Relie chaque partie de la courbe à la phase du cycle.", gauche, droite, couples, retours,
                       ("(A ; G1) (B ; S) (C ; G2) (D ; M) : G1, S et G2 forment l'interphase.",
                        "A هي G un، B هي S، C هي G deux، و D هي la mitose. G un، S و G deux، هوما l'interphase."))


# ── Données de l'exercice : G1 0–10 h, S 10–18 h, G2 18–22 h, M 22–24 h ; q = 4 UA, 2q = 8 UA ─────────────
G1, S, G2, M, Q = 10, 18, 22, 24, 4
assert (G1, S - G1, G2 - S, M - G2, G1 + (S - G1) + (G2 - S) + (M - G2)) == (10, 8, 4, 2, 24)
# Similaire : G1 0–12 h, S 12–20 h, G2 20–24 h, M 24–26 h ; q = 5 UA, 2q = 10 UA
G1b, Sb, G2b, Mb, Qb = 12, 20, 24, 26, 5
assert (G1b, Sb - G1b, G2b - Sb, Mb - G2b, Mb) == (12, 8, 4, 2, 26)

EX = {
  "id": "svt_ex_ch3_cycle_adn_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "notion_information_genetique", "cours": "svt_ch3_notion_information_genetique",
  "titre": "La quantité d'ADN au cours du cycle cellulaire", "niveau": "facile", "duree_min": 20,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Lire la courbe de la quantité d'ADN au cours du cycle", "Nommer les phases du cycle cellulaire et calculer leurs durées",
                  "Relier q → 2q à la réplication en phase S", "Expliquer le retour à q par l'anaphase et la division"],
  "enonce": {
    "intro": "Pour étudier le cycle cellulaire, on mesure la quantité d'ADN contenue dans le noyau d'une cellule de méristème de racine (zone où les cellules se divisent), du début d'un cycle jusqu'à la fin de la mitose qui le termine, puis dans l'une des deux cellules filles. La figure représente cette quantité, en unités arbitraires (UA), en fonction du temps (h). Les lettres A, B, C et D désignent les phases successives du cycle.",
    "intro_dit": "دابا نقراو l'énoncé. باش نقراو le cycle cellulaire، قسنا la quantité d'A D N فle noyau ديال cellule ديال la racine، فالبلاصة فين les cellules كيتقسمو. بدينا من البداية ديال cycle، حتى للخر ديال la mitose اللي كتسالي بيها، ومن بعد تبعنا l'une des deux cellules filles. la figure كتبين la quantité d'A D N، بl'unité arbitraire، en fonction du temps بالساعات. les lettres A، B، C و D هوما les phases ديال le cycle، وحدة من بعد الأخرى.",
    "figures": [courbe_adn(G1, S, G2, M, Q, 28, 10, "Quantité d'ADN par cellule au cours du temps")],
    "donnees": ["Quantité d'ADN en unités arbitraires (UA) ; temps en heures (h)",
                "A, B, C, D : phases successives du cycle cellulaire",
                "Après t = 24 h, la courbe suit l'une des deux cellules filles"],
    "questions": [
      {"id": "1", "texte": "Nommer les phases A, B, C et D. Préciser les phases qui forment l'interphase.",
       "texte_dit": "السؤال un: سمي les phases A، B، C و D. وقول شمن phases كيكونو l'interphase.",
       "reponse": {"type": "phrase", "attendu": "A : phase G1 ; B : phase S ; C : phase G2 ; D : mitose (phase M). L'interphase est formée de G1, S et G2 (A, B et C)."},
       "clavier": {"aides": ["G1", "S", "G2", "mitose", "interphase"], "pieges": ["méiose", "prophase"]},
       "aides": [
         {"texte": "Regarde ce que fait la courbe dans chaque phase : palier à 4 UA, montée, palier à 8 UA, puis retour à 4 UA.",
          "dit": "شوف شنو كدير la courbe فكل phase: كتبقى ثابتة، à quatre unités arbitraires، من بعد كتطلع، من بعد كتبقى ثابتة، à huit unités arbitraires، ومن بعد كترجع، à quatre."},
         {"texte": "L'ordre du cycle est G1, S, G2 puis M ; la quantité d'ADN double pendant la phase S.",
          "dit": "الترتيب ديال le cycle هو G un، S، G deux، ومن بعد M. وla quantité d'A D N كتضاعف فla phase S."}],
       "correction": {"lignes": [
           {"texte": "1 : A = phase G1 (palier à q = 4 UA)", "mot": "A هي la phase G un"},
           {"texte": "B = phase S (la quantité d'ADN double)", "mot": "B هي la phase S"},
           {"texte": "C = phase G2 ; D = mitose (M)", "mot": "C هي G deux"},
           {"texte": "interphase = G1 + S + G2 (A, B et C)", "mot": "وl'interphase فيها"}],
         "parole": "السؤال un. A هي la phase G un. B هي la phase S، فين la quantité d'A D N كتضاعف. C هي G deux، و D هي la mitose. وl'interphase فيها G un، S و G deux."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Déterminer la durée de chacune des phases A, B, C et D, puis la durée T du cycle cellulaire.",
       "texte_dit": "السؤال deux: حدد la durée ديال كل phase، ومن بعد la durée T ديال le cycle cellulaire.",
       "reponse": {"type": "valeur", "grandeur": "T", "valeur": 24, "unite": "h", "tolerance": 0.02,
                   "attendu": "G1 = 10 h ; S = 18 − 10 = 8 h ; G2 = 22 − 18 = 4 h ; M = 24 − 22 = 2 h ; T = 10 + 8 + 4 + 2 = 24 h"},
       "clavier": {"aides": ["durée = fin − début", "T = G1 + S + G2 + M", "h"], "pieges": ["T = G1 + S + G2", "28 h"]},
       "aides": [
         {"texte": "Lis sur l'axe du temps l'heure du début et l'heure de la fin de chaque phase (traits pointillés).",
          "dit": "قرا على l'axe du temps فوقاش كتبدا وفوقاش كتسالي كل phase. شوف les traits pointillés."},
         {"texte": "Durée d'une phase = heure de fin − heure de début ; T = G1 + S + G2 + M (n'oublie pas M).",
          "dit": "la durée ديال phase هي la fin moins le début. وT égale G un plus S plus G deux plus M. ما تنساش M."}],
       "correction": {"lignes": [
           {"texte": "2 : G1 = 10 h ; S = 18 − 10 = 8 h", "mot": "S égale dix-huit moins dix"},
           {"texte": "G2 = 22 − 18 = 4 h ; M = 24 − 22 = 2 h", "mot": "G deux égale vingt-deux moins dix-huit"},
           {"texte": "T = 10 + 8 + 4 + 2 = 24 h", "mot": "T égale dix plus huit"}],
         "parole": "السؤال deux. G un dure dix heures. S égale dix-huit moins dix، égale huit heures. G deux égale vingt-deux moins dix-huit، égale quatre heures. M égale vingt-quatre moins vingt-deux، égale deux heures. T égale dix plus huit plus quatre plus deux، égale vingt-quatre heures."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Décrire la variation de la quantité d'ADN pendant la phase B, puis l'expliquer en précisant l'état des chromosomes à la fin de cette phase.",
       "texte_dit": "السؤال trois: وصف كيفاش كتبدل la quantité d'A D N فla phase B، ومن بعد فسرها، وقول كيف دايرين les chromosomes فاللخر ديال هاد la phase.",
       "reponse": {"type": "phrase", "attendu": "Pendant la phase B (de 10 h à 18 h), la quantité d'ADN augmente de 4 UA (q) à 8 UA (2q) : elle double. Explication : c'est la réplication de l'ADN, en phase S. À la fin de S, chaque chromosome est formé de deux chromatides identiques reliées par le centromère."},
       "clavier": {"aides": ["augmente", "double", "q → 2q", "réplication", "deux chromatides"], "pieges": ["diminue", "une chromatide", "mitose"]},
       "aides": [
         {"texte": "Lis la valeur au début (10 h) et à la fin (18 h) de la phase B. Comment passe-t-on de l'une à l'autre ?",
          "dit": "قرا la valeur فالبداية ديال B، à dix heures، وفاللخر، à dix-huit heures. كيفاش كتدوز من وحدة للأخرى؟"},
         {"texte": "Décrire = valeurs et sens de variation ; expliquer = la cause : que fait l'ADN en phase S ? Un chromosome copié a combien de chromatides ?",
          "dit": "وصف يعني les valeurs، وواش كتزاد ولا كتنقص. فسر يعني السبب: شنو كيوقع ل l'A D N فla phase S؟ وle chromosome اللي تنسخ، شحال فيه ديال les chromatides؟"}],
       "correction": {"lignes": [
           {"texte": "3 : de 10 h à 18 h, la quantité d'ADN augmente de 4 à 8 UA : elle double (q → 2q)", "mot": "de quatre à huit unités arbitraires"},
           {"texte": "cause : réplication de l'ADN en phase S", "mot": "السبب هو la réplication"},
           {"texte": "fin de S : chromosomes à deux chromatides", "mot": "chromosome à deux chromatides"}],
         "parole": "السؤال trois. pendant la phase B، de dix heures à dix-huit heures، la quantité d'A D N كتزاد، de quatre à huit unités arbitraires: كتضاعف: de q à deux q. السبب هو la réplication ديال l'A D N، فla phase S. وفاللخر ديال S، كل chromosome كيولي chromosome à deux chromatides، مربوطين بle centromère."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Expliquer le retour de la quantité d'ADN à 4 UA à la fin de la phase D, en décrivant ce qui se passe à l'anaphase.",
       "texte_dit": "السؤال quatre: فسر علاش la quantité d'A D N كترجع، à quatre unités arbitraires، فاللخر ديال la phase D. ووصف شنو كيوقع فl'anaphase.",
       "reponse": {"type": "phrase", "attendu": "À l'anaphase, le centromère de chaque chromosome se clive : les deux chromatides sœurs se séparent et migrent vers les pôles opposés (une chromatide de chaque chromosome vers chaque pôle). À la fin de la mitose (télophase), la cellule se divise en deux cellules filles : chacune reçoit la moitié de 2q, soit q = 4 UA, et la même information génétique."},
       "clavier": {"aides": ["clivage du centromère", "chromatides sœurs", "pôles opposés", "deux cellules filles", "q = 4 UA"], "pieges": ["chromosomes homologues", "réplication"]},
       "aides": [
         {"texte": "Pendant l'anaphase, regarde ce qui arrive au centromère et aux deux chromatides de chaque chromosome.",
          "dit": "فl'anaphase، شوف شنو كيوقع لle centromère. و les deux chromatides ديال كل chromosome، فين كيمشيو؟"},
         {"texte": "La mitose se termine par la division de la cellule en deux cellules filles : comment se partage la quantité 2q ?",
          "dit": "la mitose كتسالي ملي la cellule se divise en deux cellules filles. كيفاش كتقسم la quantité deux q؟"}],
       "correction": {"lignes": [
           {"texte": "4 : anaphase : clivage du centromère", "mot": "le centromère كيتقسم"},
           {"texte": "les chromatides sœurs migrent vers les pôles opposés", "mot": "نحو les pôles opposés"},
           {"texte": "fin de mitose : deux cellules filles, chacune q = 4 UA", "mot": "se divise en deux cellules filles"}],
         "parole": "السؤال quatre. فl'anaphase، le centromère كيتقسم: les deux chromatides sœurs كيتفارقو، وكل وحدة كتمشي لجهة، نحو les pôles opposés. فاللخر ديال la mitose، la cellule se divise en deux cellules filles. كل cellule fille كتاخد النص ديال la quantité deux q، يعني q، quatre unités arbitraires، ونفس l'information génétique."},
       "explication": "ex_s4", "facile": "fa_s4"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : les phases du cycle, dans l'ordre",
     "screen_content": {"lead": "G1, S, G2 (l'interphase), puis la mitose : A, B, C, D sur la courbe."},
     "visual": {"kind": "simulation", "url": CYCLE + "?vue=cycle", "caption": "Le cycle cellulaire : le point fait le tour des phases"},
     "speech_text": {"mixed": "شوف هاد الدايرة: هي le cycle cellulaire. le point كيدور. الأول G un: la cellule كتكبر. من بعد la phase S: l'A D N كيتنسخ، هادي la réplication. من بعد G deux: la cellule كتكبر مرة أخرى. G un، S و G deux، هوما l'interphase. وفاللخر la mitose: la cellule كتقسم. فla courbe ديالك، نفس الترتيب: A، B، C و D."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "A = G1 ; B = S ; C = G2 ; D = M", "mot": "نفس الترتيب"}, {"texte": "interphase = G1 + S + G2", "mot": "هوما l'interphase"}],
       "pointage": [{"mot": "شوف هاد الدايرة", "repere": "cercle"},
                    {"mot": "الأول G un", "commande": "play_until", "parametres": {"moment": "g1"}},
                    {"mot": "الأول G un", "repere": "g1"},
                    {"mot": "من بعد la phase S", "commande": "play_until", "parametres": {"moment": "s"}},
                    {"mot": "من بعد la phase S", "repere": "s"},
                    {"mot": "من بعد G deux", "commande": "play_until", "parametres": {"moment": "g2"}},
                    {"mot": "من بعد G deux", "repere": "g2"},
                    {"mot": "هوما l'interphase", "commande": "play_until", "parametres": {"moment": "interphase"}},
                    {"mot": "هوما l'interphase", "repere": "interphase"},
                    {"mot": "هوما l'interphase", "cible": "centre:1"},
                    {"mot": "وفاللخر la mitose", "commande": "play_until", "parametres": {"moment": "mitose"}},
                    {"mot": "وفاللخر la mitose", "repere": "m"},
                    {"mot": "نفس الترتيب", "cible": "centre:0"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : la durée d'une phase = fin − début",
     "screen_content": {"lead": "On lit le début et la fin de chaque phase sur l'axe du temps ; T = G1 + S + G2 + M."},
     "visual": {"kind": "simulation", "url": CYCLE + "?vue=courbe&icones=0", "caption": "La courbe tracée phase par phase (cycle de 20 h de la simulation)"},
     "speech_text": {"mixed": "باش تحسب la durée ديال phase، قرا الحدود ديالها على l'axe du temps. فهاد la simulation، G un كتمشي de zéro à neuf heures: neuf heures. la phase S، de neuf à quinze heures: quinze moins neuf، égale six heures. G deux، de quinze à dix-neuf heures: quatre heures. وla mitose، de dix-neuf à vingt heures: une heure. la durée ديال le cycle هي la somme ديال les phases: vingt heures. فl'exercice ديالك، دير نفس الحساب، وما تنساش la mitose."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "durée d'une phase = fin − début", "mot": "قرا الحدود ديالها"}, {"texte": "T = G1 + S + G2 + M (sans oublier M)", "mot": "la somme ديال les phases"}],
       "pointage": [{"mot": "قرا الحدود ديالها", "repere": "axe_temps"},
                    {"mot": "قرا الحدود ديالها", "cible": "centre:0"},
                    {"mot": "G un كتمشي", "commande": "play_until", "parametres": {"moment": "g1_q"}},
                    {"mot": "G un كتمشي", "repere": "palier_q"},
                    {"mot": "la phase S، de neuf", "commande": "play_until", "parametres": {"moment": "fin_s_2q"}},
                    {"mot": "la phase S، de neuf", "repere": "montee"},
                    {"mot": "G deux، de quinze", "commande": "play_until", "parametres": {"moment": "g2"}},
                    {"mot": "G deux، de quinze", "repere": "palier_2q"},
                    {"mot": "وla mitose، de dix-neuf", "commande": "set_time", "parametres": {"time_s": 11.9}},
                    {"mot": "وla mitose، de dix-neuf", "commande": "play_until", "parametres": {"moment": "retour_q"}},
                    {"mot": "وla mitose، de dix-neuf", "repere": "chute"},
                    {"mot": "la somme ديال les phases", "cible": "centre:1"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : en phase S, l'ADN se réplique (q → 2q)",
     "screen_content": {"lead": "Pendant S, la quantité d'ADN double ; à la fin de S, chaque chromosome a deux chromatides."},
     "visual": {"kind": "simulation", "url": CYCLE + "?vue=courbe", "caption": "La courbe et l'aspect du chromosome de chaque phase"},
     "speech_text": {"mixed": "شوف la courbe فla phase S. فالبداية ديال S، la quantité d'A D N كتبدا تطلع. فوق la courbe، le chromosome فيه بحال شي عيون صغار: les yeux de réplication. l'A D N كيتنسخ. فاللخر ديال S، la quantité passe à deux q: تضاعفات. هادي la réplication. وفG deux، le chromosome ولا: chromosome à deux chromatides."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "phase S : q → 2q (réplication de l'ADN)", "mot": "هادي la réplication"}, {"texte": "fin de S : chromosome à deux chromatides", "mot": "chromosome à deux chromatides"}],
       "pointage": [{"mot": "شوف la courbe فla phase S", "commande": "play_until", "parametres": {"moment": "debut_s"}},
                    {"mot": "les yeux de réplication", "commande": "play_until", "parametres": {"moment": "yeux_replication"}},
                    {"mot": "les yeux de réplication", "repere": "yeux"},
                    {"mot": "la quantité passe à deux q", "commande": "play_until", "parametres": {"moment": "fin_s_2q"}},
                    {"mot": "la quantité passe à deux q", "repere": "montee"},
                    {"mot": "هادي la réplication", "cible": "centre:0"},
                    {"mot": "le chromosome ولا:", "commande": "play_until", "parametres": {"moment": "deux_chromatides"}},
                    {"mot": "chromosome à deux chromatides", "repere": "chromosome"},
                    {"mot": "chromosome à deux chromatides", "cible": "centre:1"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : l'anaphase, puis deux cellules filles à q",
     "screen_content": {"lead": "Clivage du centromère, chromatides sœurs vers les pôles opposés ; chaque cellule fille reçoit q."},
     "visual": {"kind": "simulation", "url": MITOSE + "?vue=animale&diapo=ex_anaphase", "caption": "L'anaphase puis la télophase d'une cellule animale (2n = 4)"},
     "speech_text": {"mixed": "هادي l'anaphase. le centromère ديال كل chromosome كيتقسم. les deux chromatides sœurs كيتفارقو، وكل وحدة كتمشي لجهة، نحو les pôles opposés. فكل pôle، quatre chromatides. من بعد، فla télophase، la cellule كتضيق فالوسط، et deux noyaux se forment. كل cellule fille كتاخد النص ديال l'A D N، يعني q. وعندها نفس les chromosomes ديال la cellule mère."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "anaphase : clivage du centromère ; chromatides sœurs vers les pôles opposés", "mot": "نحو les pôles opposés"},
                  {"texte": "fin de mitose : 2q → q dans chaque cellule fille", "mot": "النص ديال l'A D N"}],
       "pointage": [{"mot": "هادي l'anaphase", "commande": "set_time", "parametres": {"time_s": 13.2}},
                    {"mot": "le centromère ديال كل chromosome", "commande": "play_until", "parametres": {"moment": "clivage_centromere"}},
                    {"mot": "كيتفارقو", "commande": "play_until", "parametres": {"moment": "migration"}},
                    {"mot": "نحو les pôles opposés", "repere": "chromatides"},
                    {"mot": "نحو les pôles opposés", "cible": "centre:0"},
                    {"mot": "فla télophase", "commande": "play_until", "parametres": {"moment": "etranglement"}},
                    {"mot": "كتضيق فالوسط", "repere": "etranglement"},
                    {"mot": "et deux noyaux se forment", "commande": "play_until", "parametres": {"moment": "deux_noyaux"}},
                    {"mot": "et deux noyaux se forment", "repere": "noyaux_fils"},
                    {"mot": "كل cellule fille", "commande": "play_until", "parametres": {"moment": "fin"}},
                    {"mot": "النص ديال l'A D N", "cible": "centre:1"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    assoc_phases("fa_s1", Q, 2 * Q),
    qcm_facile("fa_s2", "Plus facile : la durée du cycle", "سؤال ساهل: كيفاش كنحسبو la durée ديال le cycle؟",
      "La durée T du cycle cellulaire se calcule par :", ["T = G1 + S + G2", "T = G1 + S + G2 + M", "T = S + M"], 1, {
        "1": {"juste": rep("برافو! T égale G un plus S plus G deux plus M. فl'exercice، T égale vingt-quatre heures.", "Juste : T = G1 + S + G2 + M = 24 h.")},
        "0": {"1": rep("قريب! هادي غير l'interphase. le cycle فيه حتى phase أخرى، فاللخر ديالو. عاود اختار.", "Ce n'est que l'interphase. Le cycle contient une autre phase, à la fin. Réessaie."),
              "2": rep("الجواب هو T égale G un plus S plus G deux plus M. نسيتي la mitose.", "Réponse : T = G1 + S + G2 + M ; tu as oublié la mitose.")},
        "2": {"1": rep("ما تقلقش. le cycle فيه phases أخرى، قبل S وبعدها. عاود اختار.", "Le cycle contient d'autres phases, avant et après S. Réessaie."),
              "2": rep("الجواب هو T égale G un plus S plus G deux plus M. خاص تجمع les phases كاملين.", "Réponse : T = G1 + S + G2 + M : on additionne toutes les phases.")}},
      "la durée T ديال le cycle cellulaire، كيفاش كتحسب؟"),
    vrai_faux("fa_s3", "Plus facile : la phase S", "Vrai ou faux : la phase S et les chromatides.",
      "سؤال ساهل: vrai ولا faux، على la phase S.", [
        ("Pendant la phase S, la quantité d'ADN passe de q à 2q.", True, "Vrai : la réplication double l'ADN pendant la phase S."),
        ("L'ADN se réplique en G2.", False, "Faux : en G2, la quantité reste à 2q ; la réplication se fait en phase S."),
        ("À la fin de la phase S, chaque chromosome est formé de deux chromatides.", True, "Vrai : deux chromatides identiques, reliées par le centromère."),
        ("Avant la réplication, chaque chromosome a deux chromatides.", False, "Faux : avant la réplication, chaque chromosome a une seule chromatide (monochromatidien).")]),
    qcm_facile("fa_s4", "Plus facile : l'anaphase", "سؤال ساهل على l'anaphase.",
      "À l'anaphase de la mitose :", ["la quantité d'ADN double", "les chromatides sœurs restent ensemble au milieu de la cellule",
                                       "les chromatides sœurs se séparent et migrent vers les pôles opposés"], 2, {
        "2": {"juste": rep("برافو! le centromère كيتقسم، و les chromatides sœurs كيمشيو نحو les pôles opposés.", "Juste : clivage du centromère, puis migration des chromatides sœurs vers les pôles opposés.")},
        "0": {"1": rep("ما تقلقش. la quantité d'A D N كتضاعف فla phase S، ماشي فl'anaphase. فl'anaphase، شنو كيوقع لle centromère؟ عاود اختار.", "L'ADN double en phase S, pas à l'anaphase. Que devient le centromère à l'anaphase ? Réessaie."),
              "2": rep("الجواب هو: les chromatides sœurs كيتفارقو، وكيمشيو نحو les pôles opposés. التضاعف كيكون فla phase S.", "Réponse : les chromatides sœurs se séparent et migrent vers les pôles opposés ; l'ADN double en phase S.")},
        "1": {"1": rep("قريب! فl'anaphase، les chromatides كيتحركو. le centromère شنو كيوقع ليه؟ عاود اختار.", "À l'anaphase, les chromatides bougent. Que devient le centromère ? Réessaie."),
              "2": rep("الجواب هو: le centromère كيتقسم، و les chromatides sœurs كيمشيو نحو les pôles opposés.", "Réponse : le centromère se clive et les chromatides sœurs migrent vers les pôles opposés.")}},
      "فl'anaphase ديال la mitose، شنو كيوقع؟")
  ]}]},
  "similaire": {
    "id": "svt_ex_ch3_cycle_adn_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même étude sur une cellule d'une autre racine. La figure représente la quantité d'ADN contenue dans le noyau de la cellule, en unités arbitraires (UA), en fonction du temps (h), puis dans l'une des deux cellules filles. Les lettres A, B, C et D désignent les phases successives du cycle.",
      "intro_dit": "نفس الدراسة، فcellule ديال racine أخرى. la figure كتبين la quantité d'A D N فle noyau، بl'unité arbitraire، en fonction du temps بالساعات، ومن بعد فl'une des deux cellules filles. A، B، C و D هوما les phases ديال le cycle.",
      "figures": [courbe_adn(G1b, Sb, G2b, Mb, Qb, 30, 12, "Quantité d'ADN par cellule au cours du temps")],
      "donnees": ["Quantité d'ADN en unités arbitraires (UA) ; temps en heures (h)",
                  "A, B, C, D : phases successives du cycle cellulaire",
                  "Après t = 26 h, la courbe suit l'une des deux cellules filles"],
      "questions": [
        {"id": "1", "texte": "Nommer les phases A, B, C et D. Préciser les phases qui forment l'interphase.",
         "reponse": {"type": "phrase", "attendu": "A : phase G1 ; B : phase S ; C : phase G2 ; D : mitose (phase M). L'interphase est formée de G1, S et G2 (A, B et C)."},
         "clavier": {"aides": ["G1", "S", "G2", "mitose", "interphase"], "pieges": ["méiose", "prophase"]},
         "correction": {"lignes": [
             {"texte": "1 : A = G1 ; B = S (la quantité d'ADN double)", "mot": "A هي la phase G un"},
             {"texte": "C = G2 ; D = mitose (M) ; interphase = G1 + S + G2", "mot": "C هي G deux"}],
           "parole": "السؤال un. A هي la phase G un، B هي la phase S. C هي G deux، و D هي la mitose. وl'interphase فيها G un، S و G deux."}},
        {"id": "2", "texte": "Déterminer la durée de chacune des phases A, B, C et D, puis la durée T du cycle cellulaire.",
         "reponse": {"type": "valeur", "grandeur": "T", "valeur": 26, "unite": "h", "tolerance": 0.02,
                     "attendu": "G1 = 12 h ; S = 20 − 12 = 8 h ; G2 = 24 − 20 = 4 h ; M = 26 − 24 = 2 h ; T = 12 + 8 + 4 + 2 = 26 h"},
         "clavier": {"aides": ["durée = fin − début", "T = G1 + S + G2 + M", "h"], "pieges": ["T = G1 + S + G2", "30 h"]},
         "correction": {"lignes": [
             {"texte": "2 : G1 = 12 h ; S = 20 − 12 = 8 h", "mot": "S égale vingt moins douze"},
             {"texte": "G2 = 24 − 20 = 4 h ; M = 26 − 24 = 2 h", "mot": "G deux égale vingt-quatre moins vingt"},
             {"texte": "T = 12 + 8 + 4 + 2 = 26 h", "mot": "T égale douze plus huit"}],
           "parole": "السؤال deux. G un dure douze heures. S égale vingt moins douze، égale huit heures. G deux égale vingt-quatre moins vingt، égale quatre heures. M égale vingt-six moins vingt-quatre، égale deux heures. T égale douze plus huit plus quatre plus deux، égale vingt-six heures."}},
        {"id": "3", "texte": "Décrire la variation de la quantité d'ADN pendant la phase B, puis l'expliquer en précisant l'état des chromosomes à la fin de cette phase.",
         "reponse": {"type": "phrase", "attendu": "Pendant la phase B (de 12 h à 20 h), la quantité d'ADN augmente de 5 UA (q) à 10 UA (2q) : elle double. Explication : c'est la réplication de l'ADN, en phase S. À la fin de S, chaque chromosome est formé de deux chromatides identiques reliées par le centromère."},
         "clavier": {"aides": ["augmente", "double", "q → 2q", "réplication", "deux chromatides"], "pieges": ["diminue", "une chromatide", "mitose"]},
         "correction": {"lignes": [
             {"texte": "3 : de 12 h à 20 h, la quantité d'ADN augmente de 5 à 10 UA : elle double (q → 2q)", "mot": "de cinq à dix unités arbitraires"},
             {"texte": "cause : réplication de l'ADN en phase S ; fin de S : chromosomes à deux chromatides", "mot": "السبب هو la réplication"}],
           "parole": "السؤال trois. de douze heures à vingt heures، la quantité d'A D N كتزاد، de cinq à dix unités arbitraires: كتضاعف. السبب هو la réplication ديال l'A D N، فla phase S. وفاللخر ديال S، كل chromosome ولا chromosome à deux chromatides."}},
        {"id": "4", "texte": "Expliquer le retour de la quantité d'ADN à 5 UA à la fin de la phase D, en décrivant ce qui se passe à l'anaphase.",
         "reponse": {"type": "phrase", "attendu": "À l'anaphase, le centromère de chaque chromosome se clive : les deux chromatides sœurs se séparent et migrent vers les pôles opposés. À la fin de la mitose, la cellule se divise en deux cellules filles : chacune reçoit la moitié de 2q, soit q = 5 UA, et la même information génétique."},
         "clavier": {"aides": ["clivage du centromère", "chromatides sœurs", "pôles opposés", "deux cellules filles", "q = 5 UA"], "pieges": ["chromosomes homologues", "réplication"]},
         "correction": {"lignes": [
             {"texte": "4 : anaphase : clivage du centromère ; chromatides sœurs vers les pôles opposés", "mot": "نحو les pôles opposés"},
             {"texte": "fin de mitose : deux cellules filles, chacune q = 5 UA", "mot": "se divise en deux cellules filles"}],
           "parole": "السؤال quatre. فl'anaphase، le centromère كيتقسم، و les chromatides sœurs كيمشيو نحو les pôles opposés. فاللخر ديال la mitose، la cellule se divise en deux cellules filles، وكل وحدة كتاخد q، cinq unités arbitraires."}}
      ]}}
}
ecrire(EX, sys.argv[1])
