# Exercice SVT ch. 2 (rôle du muscle strié squelettique) — niveau facile : le myogramme d'une secousse isolée.
# Entraîne : nommer les trois phases d'une secousse, lire des durées sur la ligne du temps (fin − début),
# calculer la durée totale, réciter la définition de la secousse (les trois mots du barème).
# Sources comparées (lecture seule, rien de copié) :
# - exploration du cours (cas_types « definir », « nommer_myogrammes » ; pieges « latence avant la stimulation »,
#   « myogramme = appareil » ; erreurs_examen « définition incomplète » ; valeurs_reperes de la secousse de grenouille) ;
# - nationaux : 2017 N « Définissez : secousse musculaire » (0,5 pt) ; 2023 R vrai/faux « le myogramme est un dispositif » ;
#   2018 N et 2020 R : myogrammes à nommer (on reste ici sur la secousse isolée, sans reprendre leurs tracés) ;
# - séries en ligne : recherche faite (résultats : cours BIOF moutamadris 1-4, recueil Charif Al Idrissi, devoir N. Bahsina
#   « Définissez : secousse musculaire », dyrassa PDF 8, alloschool 120429) mais les sites ne s'ouvrent pas depuis cette
#   session (réseau refusé) : seuls les titres et extraits du moteur de recherche ont été lus ; ils confirment la forme
#   classique « myogramme gradué → phases, durées, définition ».
# Données = celles de la simulation myographe.html (latence 0,01 s, contraction 0,04 s, relâchement 0,05 s, 20 mm),
# écrites ici en ms ; l'exercice semblable change les durées (20 / 50 / 70 ms).
import math, sys
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

SIM = "/media/simulations/svt/role_muscle_strie_squelettique-tableau/myographe.html?vue=secousse&attente=1"


def myogramme(lat, con, rel, amp, xmax, pas_lib, titre):
    """Secousse du modèle de myogramme.js (montée en cosinus, descente un peu traînante), temps en ms."""
    s, f = lat + con, lat + con + rel
    grad = []
    for v in range(0, xmax + 1, 10):
        grad.append([v, str(v)] if v % pas_lib == 0 else [v, ""])
    dents = [[0, -7.5]]
    for k in range(0, xmax // 10):
        x = 10 * k
        dents += [[x, -6], [x + 5, -6], [x + 5, -7.5], [x + 10, -7.5]]
    # positions des lettres : à gauche de la montée, à droite de la descente
    xb = lat + con * 0.3
    xc = s + rel * 0.62
    yb = amp * (1 - math.cos(math.pi * (xb - lat) / con)) / 2
    v = (xc - s) / rel
    yc = amp * (1 + math.cos(math.pi * v)) / 2 * (1 + 1.6 * v * v)
    return {"type": "courbe", "titre": titre, "ratio": 0.62,
            "axes": {"x": {"min": 0, "max": xmax + 12, "nom": "t", "unite": "ms", "graduations": grad},
                     "y": {"min": -9, "max": round(amp * 1.3), "nom": "amplitude", "unite": "mm",
                           "graduations": [0, 5, 10, 15, 20] if amp >= 20 else [0, 4, 8, 12, 16]}},
            "legende": "Myogramme d'une secousse : excitation S à t = 0 ; sous l'axe, la ligne du temps (une dent = 10 ms).",
            "elements": [
                {"f": "courbe", "expr": "0", "de": 0, "a": lat, "couleur": "blanc"},
                {"f": "courbe", "expr": f"{amp}*(1-cos(pi*(x-{lat})/{con}))/2", "de": lat, "a": s, "couleur": "blanc"},
                {"f": "courbe", "expr": f"{amp}*(1+cos(pi*(x-{s})/{rel}))/2*(1+1.6*((x-{s})/{rel})^2)", "de": s, "a": f, "couleur": "blanc"},
                {"f": "courbe", "expr": "0", "de": f, "a": xmax, "couleur": "blanc"},
                {"f": "point", "at": [0, 0], "t": "S", "pos": "no", "couleur": "jaune"},
                {"f": "texte", "at": [lat / 2, 2.2], "t": "a", "couleur": "orange"},
                {"f": "texte", "at": [round(xb - 4, 1), round(yb + 4, 1)], "t": "b", "couleur": "rose"},
                {"f": "texte", "at": [round(xc + 5, 1), round(yc + 3, 1)], "t": "c", "couleur": "bleu"},
                {"f": "ligne", "pts": dents, "couleur": "faible"}]}


QUESTIONS = [
  {"id": "1", "texte": "Nommer les phases a, b et c du myogramme.",
   "texte_dit": "السؤال numéro un: سمي les phases a، b و c ديال le myogramme.",
   "reponse": {"type": "phrase", "attendu": "a : temps de latence (de l'excitation S au début de la réponse) ; b : phase de contraction (la courbe monte, le muscle raccourcit) ; c : phase de relâchement (la courbe redescend, le muscle s'allonge et revient au repos)."},
   "clavier": {"aides": ["temps de latence", "phase de contraction", "phase de relâchement"], "pieges": ["phase de repos", "tétanos", "amplitude"]},
   "aides": [
     {"texte": "Pose le doigt sur S, puis suis la courbe : où reste-t-elle plate, où monte-t-elle, où redescend-elle ?",
      "dit": "حط صبعك على S، ومن بعد تبع la courbe: فين باقة plate، فين كتطلع، وفين كتهبط؟"},
     {"texte": "Plate juste après S : le muscle n'a pas encore répondu. La courbe monte : le muscle raccourcit. Elle descend : il s'allonge et revient au repos.",
      "dit": "ملي la courbe باقة plate من بعد S، le muscle مازال ما جاوبش. ملي كتطلع، le muscle كيولي قصير. ملي كتهبط، le muscle كيولي طويل وكيرجع للراحة."}],
   "correction": {"lignes": [
       {"texte": "1 : a : temps de latence (de S au début de la réponse)", "mot": "a هو le temps de latence"},
       {"texte": "b : phase de contraction (la courbe monte)", "mot": "b هي la phase de contraction"},
       {"texte": "c : phase de relâchement (la courbe redescend)", "mot": "c هي la phase de relâchement"}],
     "parole": "السؤال numéro un. a هو le temps de latence: من l'excitation S حتى كتبدا la réponse. b هي la phase de contraction: la courbe كتطلع، و le muscle كيولي قصير. c هي la phase de relâchement: la courbe كتهبط، و le muscle كيرجع طويل."},
   "explication": "ex_s1", "facile": "fa_s1"},
  {"id": "2", "texte": "Déterminer, à l'aide de la ligne du temps, la durée de chacune des trois phases (en ms).",
   "texte_dit": "السؤال numéro deux: حدد، ب la ligne du temps، la durée ديال كل phase، ب les millisecondes.",
   "reponse": {"type": "phrase", "attendu": "Latence : de 0 à 10 ms, soit 10 − 0 = 10 ms. Contraction : de 10 à 50 ms, soit 50 − 10 = 40 ms. Relâchement : de 50 à 100 ms, soit 100 − 50 = 50 ms (le relâchement dure plus longtemps que la contraction)."},
   "clavier": {"aides": ["durée = instant de fin − instant de début", "ms", "−"], "pieges": ["contraction = 50 ms", "latence avant S"]},
   "aides": [
     {"texte": "Sur l'axe du temps, lis trois instants : le début de la réponse, le sommet, le retour au repos.",
      "dit": "على l'axe du temps، قرا les trois instants: فين كتبدا la réponse، فين القمة، وفين كترجع la courbe للراحة."},
     {"texte": "Chaque durée = instant de fin − instant de début. La latence commence au signal S, pas avant.",
      "dit": "كل durée، هي l'instant de fin moins l'instant de début. و la latence كتبدا من l'excitation S، ماشي قبل."}],
   "correction": {"lignes": [
       {"texte": "2 : latence = 10 − 0 = 10 ms", "mot": "la latence: dix moins zéro"},
       {"texte": "contraction = 50 − 10 = 40 ms", "mot": "la contraction: cinquante moins dix"},
       {"texte": "relâchement = 100 − 50 = 50 ms (plus long que la contraction)", "mot": "le relâchement: cent moins cinquante"}],
     "parole": "السؤال numéro deux. la courbe كتبدا تطلع à dix millisecondes، القمة à cinquante millisecondes، وكترجع للراحة à cent millisecondes. la latence: dix moins zéro، égale dix millisecondes. la contraction: cinquante moins dix، égale quarante millisecondes. le relâchement: cent moins cinquante، égale cinquante millisecondes. إذن le relâchement أطول من la contraction."},
   "explication": "ex_s2", "facile": "fa_s2"},
  {"id": "3", "texte": "Calculer la durée totale d de la secousse, de l'excitation S jusqu'au retour au repos (en ms).",
   "texte_dit": "السؤال numéro trois: حسب la durée totale d ديال la secousse، من l'excitation S حتى كترجع la courbe للراحة، ب les millisecondes.",
   "reponse": {"type": "valeur", "grandeur": "d", "valeur": 100, "unite": "ms", "tolerance": 0.02,
               "attendu": "d = latence + contraction + relâchement = 10 + 40 + 50 = 100 ms"},
   "clavier": {"aides": ["d = latence + contraction + relâchement", "+", "ms"], "pieges": ["d = 50 − 10", "0,1 ms"]},
   "aides": [
     {"texte": "La secousse commence à l'excitation S et finit quand la courbe revient au repos.",
      "dit": "la secousse كتبدا من l'excitation S، وكتسالي ملي la courbe كترجع للراحة."},
     {"texte": "Additionne les trois durées de la question 2, ou lis directement l'instant du retour au repos.",
      "dit": "جمع les trois durées ديال السؤال numéro deux، ولا قرا مباشرة l'instant فين كترجع la courbe للراحة."}],
   "correction": {"lignes": [
       {"texte": "3 : d = latence + contraction + relâchement", "mot": "d égale la latence"},
       {"texte": "d = 10 + 40 + 50 = 100 ms", "mot": "dix plus quarante plus cinquante"},
       {"texte": "vérification : retour au repos à 100 ms, 100 − 0 = 100 ms", "mot": "cent moins zéro"}],
     "parole": "السؤال numéro trois. d égale la latence، plus la contraction، plus le relâchement. d égale dix plus quarante plus cinquante، égale cent millisecondes. ونتأكدو: la courbe كترجع للراحة à cent millisecondes، et cent moins zéro، égale cent millisecondes."},
   "explication": "ex_s3", "facile": "fa_s3"},
  {"id": "4", "texte": "Définir la secousse musculaire.",
   "texte_dit": "السؤال numéro quatre: عرف la secousse musculaire.",
   "reponse": {"type": "phrase", "attendu": "La secousse musculaire est la réponse mécanique du muscle à une seule excitation efficace ; elle est formée d'une phase de contraction puis d'une phase de relâchement (après un court temps de latence)."},
   "clavier": {"aides": ["réponse mécanique du muscle", "une seule excitation", "efficace"], "pieges": ["plusieurs excitations", "contraction seulement", "le tracé du myographe"]},
   "aides": [
     {"texte": "Réponds à trois questions : combien d'excitations ? de quelle sorte ? quelles phases ?",
      "dit": "جاوب على هاد les trois questions: شحال من excitation؟ أشمن excitation؟ وأشمن phases؟"},
     {"texte": "Une définition d'examen contient : « réponse », « une seule excitation efficace », « contraction puis relâchement ».",
      "dit": "la définition ديال l'examen فيها: la réponse، une seule excitation efficace، و la contraction puis le relâchement."}],
   "correction": {"lignes": [
       {"texte": "4 : la secousse musculaire est la réponse mécanique du muscle", "mot": "la réponse mécanique du muscle"},
       {"texte": "à une seule excitation efficace,", "mot": "à une seule excitation efficace"},
       {"texte": "formée d'une phase de contraction puis d'une phase de relâchement.", "mot": "puis d'une phase de relâchement"}],
     "parole": "السؤال numéro quatre. نعاود نقرا: la secousse musculaire, est la réponse mécanique du muscle, à une seule excitation efficace, formée d'une phase de contraction, puis d'une phase de relâchement."},
   "explication": "ex_s4", "facile": "fa_s4"},
]

EXPLICATION = [
  {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : les trois phases d'une secousse",
   "screen_content": {"lead": "Plate après S : latence. Elle monte : contraction. Elle redescend : relâchement."},
   "visual": {"kind": "simulation", "url": SIM, "caption": "Le myographe et le myogramme d'une secousse"},
   "speech_text": {"mixed": "شوف le signal S تحت la courbe: هادي هي اللحظة ديال l'excitation. la courbe ما كتطلعش مباشرة: هادا هو le temps de latence. من بعد، la courbe كتطلع حتى للقمة، و le muscle كيولي قصير: هادي هي la phase de contraction. ومن بعد كتهبط حتى كترجع للراحة، و le muscle كيولي طويل: هادي هي la phase de relâchement."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "a : temps de latence", "mot": "هادا هو le temps de latence"},
                {"texte": "b : phase de contraction", "mot": "هادي هي la phase de contraction"},
                {"texte": "c : phase de relâchement", "mot": "هادي هي la phase de relâchement"}],
     "pointage": [{"mot": "شوف le signal S", "commande": "play_until", "parametres": {"moment": "stimulation"}},
                  {"mot": "le signal S", "repere": "signal_excitation"},
                  {"mot": "la courbe ما كتطلعش مباشرة", "commande": "play_until", "parametres": {"moment": "fin_latence"}},
                  {"mot": "هادا هو le temps de latence", "repere": "latence"},
                  {"mot": "هادا هو le temps de latence", "cible": "centre:0"},
                  {"mot": "la courbe كتطلع حتى للقمة", "commande": "play_until", "parametres": {"moment": "sommet"}},
                  {"mot": "هادي هي la phase de contraction", "repere": "contraction"},
                  {"mot": "هادي هي la phase de contraction", "cible": "centre:1"},
                  {"mot": "ومن بعد كتهبط", "commande": "play_until", "parametres": {"moment": "retour_repos"}},
                  {"mot": "هادي هي la phase de relâchement", "repere": "relachement"},
                  {"mot": "هادي هي la phase de relâchement", "cible": "centre:2"}]}},
  {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : lire les durées sur la ligne du temps",
   "screen_content": {"lead": "Une dent = 0,01 s = 10 ms ; durée = fin − début : 10 ms, 40 ms, 50 ms."},
   "visual": {"kind": "simulation", "url": SIM, "caption": "Les durées lues sur la ligne du temps"},
   "speech_text": {"mixed": "دابا نقيسو. la ligne du temps تحت la courbe: une dent égale un centième de seconde، soit dix millisecondes. l'excitation à zéro. la courbe كتبدا تطلع à dix millisecondes، القمة à cinquante millisecondes، والرجوع للراحة à cent millisecondes. كل durée، هي la fin moins le début. la latence: dix millisecondes. la contraction: quarante millisecondes. le relâchement: cinquante millisecondes، أطول من la contraction."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "1 dent = 0,01 s = 10 ms", "mot": "soit dix millisecondes"},
                {"texte": "durée = fin − début", "mot": "هي la fin moins le début"},
                {"texte": "latence 10 ms ; contraction 40 ms ; relâchement 50 ms", "mot": "le relâchement: cinquante millisecondes"}],
     "pointage": [{"mot": "دابا نقيسو", "commande": "play_until", "parametres": {"moment": "mesure_durees"}},
                  {"mot": "la ligne du temps", "repere": "ligne_temps"},
                  {"mot": "soit dix millisecondes", "cible": "centre:0"},
                  {"mot": "هي la fin moins le début", "cible": "centre:1"},
                  {"mot": "la latence: dix millisecondes", "repere": "latence"},
                  {"mot": "la contraction: quarante millisecondes", "repere": "contraction"},
                  {"mot": "le relâchement: cinquante millisecondes", "repere": "relachement"},
                  {"mot": "le relâchement: cinquante millisecondes", "cible": "centre:2"}]}},
  {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : la durée totale de la secousse",
   "screen_content": {"lead": "De S au retour au repos : d = 10 + 40 + 50 = 100 ms = 0,10 s."},
   "visual": {"kind": "simulation", "url": SIM, "caption": "De l'excitation au retour au repos"},
   "speech_text": {"mixed": "la secousse كتبدا من l'excitation S، وكتسالي ملي la courbe كترجع للراحة. شوف: de zéro à cent millisecondes. نجمعو les trois durées: dix plus quarante plus cinquante، égale cent millisecondes، soit zéro virgule dix seconde."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "d = 10 + 40 + 50", "mot": "dix plus quarante plus cinquante"},
                {"texte": "d = 100 ms = 0,10 s", "mot": "égale cent millisecondes"}],
     "pointage": [{"mot": "la secousse كتبدا", "commande": "play_until", "parametres": {"moment": "stimulation"}},
                  {"mot": "من l'excitation S", "repere": "signal_excitation"},
                  {"mot": "ملي la courbe كترجع للراحة", "commande": "play_until", "parametres": {"moment": "retour_repos"}},
                  {"mot": "نجمعو les trois durées", "commande": "play_until", "parametres": {"moment": "mesure_durees"}},
                  {"mot": "dix plus quarante plus cinquante", "cible": "centre:0"},
                  {"mot": "égale cent millisecondes", "cible": "centre:1"}]}},
  {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : la définition de la secousse",
   "screen_content": {"lead": "Réponse mécanique du muscle à une seule excitation efficace : contraction puis relâchement."},
   "visual": {"kind": "simulation", "url": SIM, "caption": "Une seule excitation, une secousse"},
   "speech_text": {"mixed": "نبنيو la définition، بهاد les trois questions. شحال من excitation؟ وحدة برك: une seule excitation. أشمن excitation؟ efficace، يعني كافية باش le muscle يجاوب. أشمن phases؟ من بعد la latence، la contraction، puis le relâchement. نعاود نقرا: la secousse musculaire, est la réponse mécanique du muscle, à une seule excitation efficace, formée d'une phase de contraction, puis d'une phase de relâchement."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "une seule excitation efficace", "mot": "وحدة برك"},
                {"texte": "contraction puis relâchement", "mot": "la contraction، puis le relâchement"},
                {"texte": "Secousse : réponse mécanique du muscle à une seule excitation efficace", "mot": "نعاود نقرا"}],
     "pointage": [{"mot": "شحال من excitation", "commande": "play_until", "parametres": {"moment": "stimulation"}},
                  {"mot": "وحدة برك", "repere": "signal_excitation"},
                  {"mot": "وحدة برك", "cible": "centre:0"},
                  {"mot": "أشمن phases", "commande": "play_until", "parametres": {"moment": "retour_repos"}},
                  {"mot": "la contraction، puis", "repere": "contraction"},
                  {"mot": "puis le relâchement", "repere": "relachement"},
                  {"mot": "la contraction، puis le relâchement", "cible": "centre:1"},
                  {"mot": "نعاود نقرا", "cible": "centre:2"}]}},
]

A_OK = "برافو!"
FACILE = [
  association("fa_s1", "Plus facile : relier chaque partie à sa phase", "Relie chaque partie du myogramme à sa phase.",
    "نتمرنو: ربط كل جزء ديال la courbe مع la phase ديالو.",
    "Relie chaque partie du myogramme au nom de sa phase.",
    [("a", "a : la courbe reste plate juste après S"), ("b", "b : la courbe monte"), ("c", "c : la courbe redescend jusqu'au repos")],
    [("x", "temps de latence"), ("y", "phase de contraction"), ("z", "phase de relâchement"), ("w", "amplitude")],
    {"a": "x", "b": "y", "c": "z"},
    {"a-x": (True, "Oui : entre S et le début de la réponse, c'est le temps de latence.", "برافو: بين S والبداية ديال la réponse، هادا هو le temps de latence."),
     "a-y": (False, "Pendant la contraction la courbe monte ; ici elle est encore plate.", "لا، ف la contraction la courbe كتطلع، وهنا باقة plate."),
     "a-z": (False, "Le relâchement vient après le sommet ; ici le muscle n'a pas encore répondu.", "لا، le relâchement كيجي من بعد القمة، وهنا le muscle مازال ما جاوبش."),
     "a-w": (False, "L'amplitude est une hauteur, pas une phase.", "لا، l'amplitude هي الطول ديال القمة، ماشي phase."),
     "b-x": (False, "La latence, c'est quand la courbe est encore plate ; ici elle monte.", "لا، la latence ملي la courbe باقة plate، وهنا كتطلع."),
     "b-y": (True, "Oui : la courbe monte, le muscle raccourcit : phase de contraction.", "برافو: la courbe كتطلع، و le muscle كيولي قصير: la phase de contraction."),
     "b-z": (False, "Pendant le relâchement la courbe descend ; ici elle monte.", "لا، ف le relâchement la courbe كتهبط، وهنا كتطلع."),
     "b-w": (False, "L'amplitude se mesure au sommet ; la partie qui monte est une phase.", "لا، l'amplitude كتقاس ف القمة، والجزء اللي كيطلع هو phase."),
     "c-x": (False, "La latence est avant la réponse, pas à la fin.", "لا، la latence قبل la réponse، ماشي ف اللخر."),
     "c-y": (False, "La contraction fait monter la courbe ; ici elle descend.", "لا، la contraction كتطلع la courbe، وهنا كتهبط."),
     "c-z": (True, "Oui : la courbe redescend, le muscle s'allonge : phase de relâchement.", "برافو: la courbe كتهبط، و le muscle كيولي طويل: la phase de relâchement."),
     "c-w": (False, "L'amplitude est une hauteur, pas une phase.", "لا، l'amplitude هي الطول ديال القمة، ماشي phase.")},
    ("a : latence ; b : contraction ; c : relâchement. L'amplitude n'est pas une phase.",
     "a هو la latence، b هي la contraction، و c هو le relâchement. و l'amplitude ماشي phase.")),
  qcm_facile("fa_s2", "Plus facile : la durée de la contraction", "سؤال ساهل على la durée ديال la contraction.",
    "D'après le myogramme, la phase de contraction dure…", ["40 ms", "50 ms", "10 ms"], 0, {
      "0": {"juste": rep("برافو! la contraction كتبدا à dix millisecondes، وكتسالي à cinquante millisecondes. cinquante moins dix، égale quarante millisecondes.", "Juste : contraction = 50 − 10 = 40 ms.")},
      "1": {"1": rep("ما تقلقش. cinquante millisecondes، c'est l'instant ديال القمة، ماشي la durée. la contraction فين كتبدا؟ عاود اختار.", "50 ms est l'instant du sommet, pas une durée. Où commence la contraction ? Réessaie."),
            "2": rep("الجواب الصحيح، c'est quarante millisecondes. la contraction: cinquante moins dix. خاصك تنقص l'instant ديال البداية.", "Réponse : 40 ms (50 − 10) ; il faut retirer l'instant du début.")},
      "2": {"1": rep("لا، هادي la latence: dix millisecondes. la contraction، فين كتبدا وفين كتسالي؟ عاود اختار.", "10 ms, c'est la durée de la latence. Où commence et où finit la contraction ? Réessaie."),
            "2": rep("الجواب الصحيح، c'est quarante millisecondes. و la latence، c'est dix millisecondes.", "Réponse : 40 ms ; 10 ms est la durée de la latence.")}},
    "La phase de contraction dure combien de millisecondes ?"),
  qcm_facile("fa_s3", "Plus facile : la durée totale", "سؤال ساهل: la durée totale ديال la secousse.",
    "La durée totale de la secousse, de S jusqu'au retour au repos, vaut…", ["90 ms", "100 ms", "50 ms"], 1, {
      "1": {"juste": rep("برافو! dix plus quarante plus cinquante، égale cent millisecondes. la courbe كترجع للراحة à cent millisecondes.", "Juste : d = 10 + 40 + 50 = 100 ms.")},
      "0": {"1": rep("قريب. نسيتي la latence. la secousse كتبدا من l'excitation S. عاود اختار.", "Tu as oublié la latence : la secousse part de l'excitation S. Réessaie."),
            "2": rep("الجواب الصحيح، c'est cent millisecondes: dix plus quarante plus cinquante. quatre-vingt-dix millisecondes، بلا la latence.", "Réponse : 100 ms (10 + 40 + 50) ; 90 ms oublie la latence.")},
      "2": {"1": rep("لا، cinquante millisecondes، c'est l'instant ديال القمة. la secousse كتسالي فين؟ عاود اختار.", "50 ms, c'est l'instant du sommet. Où finit la secousse ? Réessaie."),
            "2": rep("الجواب الصحيح، c'est cent millisecondes. la courbe كترجع للراحة à cent millisecondes.", "Réponse : 100 ms, instant du retour au repos.")}},
    "La durée totale de la secousse vaut combien ?"),
  vrai_faux("fa_s4", "Plus facile : la définition, vrai ou faux", "Vrai ou faux : la secousse musculaire.",
    "سؤال ساهل: قرا كل جملة، وقول vrai ولا faux.",
    [("La secousse musculaire est la réponse mécanique du muscle à une seule excitation efficace.", True,
      "Vrai : une seule excitation, efficace, et une réponse mécanique (le muscle raccourcit puis s'allonge)."),
     ("Une excitation inefficace provoque une petite secousse.", False,
      "Faux : une excitation inefficace (sous le seuil) ne provoque aucune réponse ; le tracé reste plat."),
     ("La secousse comprend une phase de contraction puis une phase de relâchement.", True,
      "Vrai : après la latence, la contraction (la courbe monte) puis le relâchement (elle redescend)."),
     ("Le temps de latence commence avant l'excitation.", False,
      "Faux : la latence commence au signal d'excitation S et finit au début de la réponse."),
     ("Le myogramme est l'appareil qui enregistre la contraction.", False,
      "Faux : l'appareil est le myographe ; le myogramme est le tracé obtenu.")]),
]

SIM_Q = [
  {"id": "1", "texte": "Nommer les phases a, b et c du myogramme.",
   "reponse": {"type": "phrase", "attendu": "a : temps de latence ; b : phase de contraction ; c : phase de relâchement."},
   "clavier": {"aides": ["temps de latence", "phase de contraction", "phase de relâchement"], "pieges": ["phase de repos", "amplitude"]},
   "correction": {"lignes": [{"texte": "1 : a : temps de latence", "mot": "a هو le temps de latence"},
                             {"texte": "b : phase de contraction", "mot": "b هي la phase de contraction"},
                             {"texte": "c : phase de relâchement", "mot": "c هي la phase de relâchement"}],
                  "parole": "السؤال numéro un. a هو le temps de latence. b هي la phase de contraction، la courbe كتطلع. c هي la phase de relâchement، la courbe كتهبط."}},
  {"id": "2", "texte": "Déterminer, à l'aide de la ligne du temps, la durée de chacune des trois phases (en ms).",
   "reponse": {"type": "phrase", "attendu": "Latence : 20 − 0 = 20 ms. Contraction : 70 − 20 = 50 ms. Relâchement : 140 − 70 = 70 ms (plus long que la contraction)."},
   "clavier": {"aides": ["durée = instant de fin − instant de début", "ms"], "pieges": ["contraction = 70 ms"]},
   "correction": {"lignes": [{"texte": "2 : latence = 20 − 0 = 20 ms", "mot": "la latence: vingt moins zéro"},
                             {"texte": "contraction = 70 − 20 = 50 ms", "mot": "la contraction: soixante-dix moins vingt"},
                             {"texte": "relâchement = 140 − 70 = 70 ms", "mot": "le relâchement: cent quarante moins soixante-dix"}],
                  "parole": "السؤال numéro deux. la latence: vingt moins zéro، égale vingt millisecondes. la contraction: soixante-dix moins vingt، égale cinquante millisecondes. le relâchement: cent quarante moins soixante-dix، égale soixante-dix millisecondes."}},
  {"id": "3", "texte": "Calculer la durée totale d de la secousse, de l'excitation S jusqu'au retour au repos (en ms).",
   "reponse": {"type": "valeur", "grandeur": "d", "valeur": 140, "unite": "ms", "tolerance": 0.02,
               "attendu": "d = latence + contraction + relâchement = 20 + 50 + 70 = 140 ms"},
   "clavier": {"aides": ["d = latence + contraction + relâchement", "ms"], "pieges": ["d = 50 + 70"]},
   "correction": {"lignes": [{"texte": "3 : d = 20 + 50 + 70", "mot": "vingt plus cinquante plus soixante-dix"},
                             {"texte": "d = 140 ms", "mot": "égale cent quarante millisecondes"}],
                  "parole": "السؤال numéro trois. d égale vingt plus cinquante plus soixante-dix، égale cent quarante millisecondes."}},
  {"id": "4", "texte": "Définir la secousse musculaire.",
   "reponse": {"type": "phrase", "attendu": "La secousse musculaire est la réponse mécanique du muscle à une seule excitation efficace ; elle est formée d'une phase de contraction puis d'une phase de relâchement."},
   "clavier": {"aides": ["réponse mécanique du muscle", "une seule excitation efficace"], "pieges": ["plusieurs excitations"]},
   "correction": {"lignes": [{"texte": "4 : réponse mécanique du muscle à une seule excitation efficace", "mot": "à une seule excitation efficace"},
                             {"texte": "phase de contraction puis phase de relâchement", "mot": "puis d'une phase de relâchement"}],
                  "parole": "السؤال numéro quatre. la secousse musculaire, est la réponse mécanique du muscle, à une seule excitation efficace, formée d'une phase de contraction, puis d'une phase de relâchement."}},
]

EX = {
  "id": "svt_ex_ch2_secousse_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "role_muscle_strie_squelettique", "cours": "svt_ch2_role_muscle_strie_squelettique",
  "titre": "Le myogramme d'une secousse musculaire : phases, durées, définition", "niveau": "facile", "duree_min": 15,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Nommer les phases d'une secousse sur un myogramme", "Lire une durée sur la ligne du temps", "Définir la secousse musculaire"],
  "enonce": {
    "intro": "Un muscle gastrocnémien de grenouille est relié à un myographe. À t = 0, on lui applique une seule excitation électrique efficace (signal S). La figure représente le myogramme obtenu ; sous l'axe, la ligne du temps est graduée en millisecondes (une dent = 10 ms).",
    "intro_dit": "نقراو l'énoncé. عندنا le muscle gastrocnémien ديال الضفدعة، مربوط ب le myographe. ف t égale zéro، on lui applique une seule excitation efficace، c'est le signal S. la figure كتبين le myogramme اللي حصلنا عليه. وتحت l'axe، la ligne du temps ب les millisecondes: une dent égale dix millisecondes.",
    "figures": [myogramme(10, 40, 50, 20, 120, 10, "Myogramme d'une secousse musculaire")],
    "donnees": ["Excitation unique et efficace S à t = 0", "Ligne du temps : une dent = 10 ms", "Amplitude de la secousse : 20 mm"],
    "questions": QUESTIONS},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPLICATION}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FACILE}]},
  "similaire": {
    "id": "svt_ex_ch2_secousse_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même expérience sur un autre muscle de grenouille : à t = 0, une seule excitation efficace S. La figure représente le myogramme obtenu (ligne du temps : une dent = 10 ms).",
      "intro_dit": "نفس التجربة، ب muscle آخر ديال الضفدعة. ف t égale zéro، une seule excitation efficace S. la figure كتبين le myogramme. la ligne du temps: une dent égale dix millisecondes.",
      "figures": [myogramme(20, 50, 70, 16, 160, 20, "Myogramme d'une secousse (autre muscle)")],
      "donnees": ["Excitation unique et efficace S à t = 0", "Ligne du temps : une dent = 10 ms", "Amplitude de la secousse : 16 mm"],
      "questions": SIM_Q}},
}

if __name__ == "__main__":
    ecrire(EX, sys.argv[1])
