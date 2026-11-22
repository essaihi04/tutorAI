# Exercice SVT ch. 2 (rôle du muscle strié squelettique), niveau moyen : les teneurs du muscle pendant une course de 10 min.
# Ce qu'il entraîne : décrire un tableau de métabolites par périodes (valeurs lues, « passe de … à … », « augmente »,
# « diminue », « On en déduit que »), calculer un pourcentage de diminution, déduire la voie de régénération de l'ATP qui
# domine à chaque période (anaérobie alactique, anaérobie lactique, aérobie) et écrire sa réaction ou son équation avec
# ADP et Pi ; raisonner « glycogène qui baisse sans acide lactique = respiration ».
# Sources comparées (lecture seulement, rien de copié) :
# - exploration du cours : cas_types « tableau_metabolites » (2017 R, 2020 R, 2022 R), « voies_equations » (2022 N, QCM
#   2018 N et 2023 R, association 2020 R) ; pièges « anaérobie ≠ fermentation », « équations sans ADP + Pi »,
#   « décrit sans valeur », « explique quand on demande de décrire » ; valeurs_reperes (réserve d'ATP, PC une dizaine de
#   secondes, fermentation une à deux minutes, 36 ATP par glucose, 38 accepté) ;
# - vidéos des profs via l'exploration : Ikram (frise du coureur), Sarah (quatre réactions de régénération), Ouissam ;
# - nationaux : 2017 R (100 m / 1500 m nage), 2016 N (entraîné / non entraîné), 2022 N (citer deux voies et leurs
#   équations) : on garde la forme « décrire puis déduire » et l'écriture des équations, avec notre propre situation
#   (une seule course suivie dans le temps, quatre teneurs, autres valeurs) ;
# - séries en ligne : recherche du 22/11/2026 (moutamadris, alloschool, schoolmouv, digischool) : seuls les extraits des
#   résultats ont pu être lus (moutamadris.ma et dreamjob.ma bloqués par le réseau de la session) : phosphocréatine qui
#   s'épuise vite au début de l'effort, voies qui se relaient ; comparaison faite surtout avec les vidéos et les nationaux.
# Allures choisies pour coller à voies.html (ATP presque constant, PC qui chute dans les dix premières secondes, acide
# lactique qui monte jusqu'à deux à trois minutes puis baisse un peu, respiration qui domine ensuite).
# Pas de recouvrement : svt_ex_ch2_inhibiteurs_1 (même agent) traite les voies bloquées ; l'autre agent fait la secousse,
# le sarcomère légendé et la sommation.
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

D = "/media/simulations/svt/role_muscle_strie_squelettique-tableau/"
VOIES = D + "voies.html?attente=1"


def fv(x):
    if float(x).is_integer():
        return str(int(x))
    return f"{x:.1f}".replace(".", ",")


def tableau(titre, legende, entetes, lignes, larg, h_ligne=0.8):
    """Un tableau dessiné (schema à cadre) : rect + lignes + texte. Une cellule peut tenir sur deux lignes (« \\n »)."""
    toutes = [entetes] + lignes
    hs = [h_ligne * max(len(c.split("\n")) for c in r) for r in toutes]
    l, h = sum(larg), sum(hs)
    el = [{"f": "rect", "de": [0, 0], "a": [l, h], "couleur": "blanc"}]
    y = h
    for k, r in enumerate(toutes):
        y_bas = y - hs[k]
        if k < len(toutes) - 1:
            el.append({"f": "ligne", "pts": [[0, round(y_bas, 3)], [l, round(y_bas, 3)]], "couleur": "blanc" if k == 0 else "faible"})
        x = 0
        for j, cel in enumerate(r):
            morceaux = cel.split("\n")
            for m, t in enumerate(morceaux):
                yc = y - hs[k] / 2 + (len(morceaux) - 1) * h_ligne * 0.32 - m * h_ligne * 0.64
                el.append({"f": "texte", "at": [round(x + larg[j] / 2, 3), round(yc, 3)], "t": t, "taille": "petit",
                           "couleur": "cyan" if k == 0 or j == 0 else "blanc", "ancre": "centre"})
            x += larg[j]
        y = y_bas
    x = 0
    for w in larg[:-1]:
        x += w
        el.append({"f": "ligne", "pts": [[round(x, 3), 0], [round(x, 3), h]], "couleur": "faible"})
    return {"type": "schema", "titre": titre, "legende": legende, "cadre": {"l": l, "h": round(h, 3)}, "elements": el}


TEMPS = ["repos", "10 s", "1 min", "3 min", "10 min"]


def doc(atp, pc, lac, gly):
    return tableau("Document : teneurs du muscle de la cuisse au cours de la course",
                   "ATP, phosphocréatine et acide lactique en mmol par kg de muscle ; glycogène en unités arbitraires (UA), 100 au repos.",
                   ["mmol/kg"] + TEMPS,
                   [["ATP"] + [f"{v:.1f}".replace(".", ",") for v in atp], ["Phosphocréatine"] + [fv(v) for v in pc],
                    ["Acide lactique"] + [fv(v) for v in lac], ["Glycogène (UA)"] + [fv(v) for v in gly]],
                   [3.6] + [1.68] * 5)


ATP, PC, LAC, GLY = [5.0, 4.6, 4.5, 4.6, 4.7], [20, 6, 3, 3, 3], [1, 2, 9, 12, 10], [100, 99, 90, 78, 56]
ATP_B, PC_B, LAC_B, GLY_B = [6.0, 5.5, 5.4, 5.5, 5.6], [25, 10, 5, 4, 4], [1, 3, 11, 14, 11], [100, 98, 87, 72, 50]
P = round((PC[0] - PC[1]) / PC[0] * 100, 1)
PB = round((PC_B[0] - PC_B[1]) / PC_B[0] * 100, 1)
assert P == 70.0 and PB == 60.0
# allures du document = allures de la simulation : ATP presque constant (baisse < 10 %), PC effondrée après 10 s,
# acide lactique maximal à 3 min puis en légère baisse, glycogène qui baisse de plus en plus en tout
for a, p, l, g in ((ATP, PC, LAC, GLY), (ATP_B, PC_B, LAC_B, GLY_B)):
    assert min(a) / a[0] > 0.89 and p[1] / p[0] <= 0.4 and max(l) == l[3] and l[4] < l[3] and g == sorted(g, reverse=True)

EQ_PC = "PC + ADP → C + ATP"
EQ_FL = "C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP"
EQ_RE = "C₆H₁₂O₆ + 6 O₂ + 36 ADP + 36 Pi → 6 CO₂ + 6 H₂O + 36 ATP"

EX = {
  "id": "svt_ex_ch2_voies_atp_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "role_muscle_strie_squelettique", "cours": "svt_ch2_role_muscle_strie_squelettique",
  "titre": "Une course de dix minutes : les voies de régénération de l'ATP se relaient", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire un tableau de métabolites par périodes", "Calculer un pourcentage de diminution",
                  "Déduire la voie de régénération de l'ATP qui domine", "Écrire les réactions de régénération de l'ATP"],
  "enonce": {
    "intro": "Un athlète court pendant 10 minutes à une allure soutenue et régulière. Par de petits prélèvements de son muscle de la cuisse (biopsies), on dose au repos, puis à différents moments de la course, l'ATP, la phosphocréatine, l'acide lactique et le glycogène (le glucose mis en réserve dans le muscle). Le document donne les résultats.",
    "intro_dit": "دابا نقراو l'énoncé. واحد l'athlète كيجري pendant dix minutes، ب واحد السرعة ثابتة. كناخدو شوية صغيرة من le muscle ديال الفخذ، ف الراحة، ومن بعد ف بزاف ديال اللحظات ديال الجري. وكنقيسو l'A T P، la phosphocréatine، l'acide lactique، و le glycogène، يعني le glucose اللي مخزون ف le muscle. le document فيه les résultats.",
    "figures": [doc(ATP, PC, LAC, GLY)],
    "donnees": ["Teneurs en mmol par kg de muscle (glycogène : en unités arbitraires, 100 au repos)",
                "Mesures au repos, puis 10 s, 1 min, 3 min et 10 min après le départ"],
    "questions": [
      {"id": "1", "texte": "Décrire l'évolution de la teneur en ATP du muscle pendant la course, puis en déduire ce que devient l'ATP consommé par la contraction.",
       "texte_dit": "Question un : وصف كيفاش تبدلات la teneur ديال l'A T P ف le muscle ف الجري، ومن بعد استنتج شنو كيوقع ل l'A T P اللي كتستهلك la contraction.",
       "reponse": {"type": "phrase", "attendu": "Au repos, l'ATP vaut 5,0 mmol/kg ; pendant la course, il diminue à peine (entre 4,5 et 4,7 mmol/kg) et reste presque constant. On en déduit que l'ATP consommé par la contraction est régénéré au fur et à mesure, aussi vite qu'il est utilisé."},
       "clavier": {"aides": ["5,0 mmol/kg", "diminue à peine", "presque constant", "régénéré", "On en déduit que"], "pieges": ["l'ATP n'est pas utilisé", "l'ATP diminue fortement"]},
       "aides": [
         {"texte": "Regarde la ligne ATP : compare la valeur au repos aux valeurs pendant la course.",
          "dit": "شوف السطر ديال l'A T P: قارن la valeur ديال الراحة، مع les valeurs ديال الجري."},
         {"texte": "Le muscle se contracte, donc il consomme de l'ATP. Si la teneur ne baisse presque pas, que se passe-t-il en même temps ?",
          "dit": "le muscle كيتقلص، إذن كيستهلك l'A T P. يلا la teneur تقريبا ما نقصاتش، شنو كيوقع ف نفس الوقت؟"}],
       "correction": {"lignes": [
           {"texte": "1 : ATP : 5,0 mmol/kg au repos, entre 4,5 et 4,7 mmol/kg pendant la course : presque constant", "mot": "l'A T P passe de cinq"},
           {"texte": "On en déduit que l'ATP consommé est régénéré au fur et à mesure", "mot": "l'A T P est régénéré"}],
         "parole": "Question un. l'A T P passe de cinq millimoles par kilogramme au repos، à environ quatre virgule cinq ou quatre virgule sept pendant la course: تقريبا ما تبدلش. ولكن le muscle كيتقلص، إذن كيستهلك l'A T P. On en déduit que l'A T P est régénéré، ب نفس السرعة اللي كيتستهلك بيها."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Calculer le pourcentage de diminution p de la phosphocréatine pendant les dix premières secondes.",
       "texte_dit": "Question deux : حسب le pourcentage p ديال النقص ديال la phosphocréatine، pendant les dix premières secondes.",
       "reponse": {"type": "valeur", "grandeur": "p", "valeur": P, "unite": "%", "tolerance": 0.02,
                   "attendu": "p = (20 − 6)/20 × 100 = 14/20 × 100 = 70 %"},
       "clavier": {"aides": ["p = (valeur au repos − valeur à 10 s)/valeur au repos × 100", "20 − 6", "%"], "pieges": ["6/20 × 100", "(20 − 6)/6 × 100"]},
       "aides": [
         {"texte": "Lis la phosphocréatine au repos et à 10 s.",
          "dit": "قرا la phosphocréatine ف الراحة، و après dix secondes."},
         {"texte": "p = (valeur au repos − valeur à 10 s) / valeur au repos × 100.",
          "dit": "p égale la valeur au repos moins la valeur à dix secondes، sur la valeur au repos، fois cent."}],
       "correction": {"lignes": [
           {"texte": "2 : p = (valeur au repos − valeur à 10 s)/valeur au repos × 100", "mot": "p égale la valeur au repos"},
           {"texte": "p = (20 − 6)/20 × 100 = 14/20 × 100", "mot": "vingt moins six"},
           {"texte": "p = 70 % : en 10 s, la phosphocréatine perd 70 % de sa teneur", "mot": "p égale soixante-dix pour cent"}],
         "parole": "Question deux. p égale la valeur au repos moins la valeur à dix secondes، sur la valeur au repos، fois cent. vingt moins six، égale quatorze. quatorze sur vingt، fois cent. p égale soixante-dix pour cent: en dix secondes seulement، la phosphocréatine perd soixante-dix pour cent."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "En déduire la voie de régénération de l'ATP qui domine au début de la course (de 0 à 10 s). Écrire la réaction correspondante et nommer son enzyme.",
       "texte_dit": "Question trois : استنتج la voie ديال la régénération ديال l'A T P اللي كتخدم أكثر ف البداية ديال الجري، de zéro à dix secondes. كتب la réaction ديالها، وسمي l'enzyme.",
       "reponse": {"type": "phrase", "attendu": "De 0 à 10 s, la phosphocréatine chute fortement (de 20 à 6 mmol/kg) alors que l'acide lactique augmente peu (de 1 à 2 mmol/kg) : l'ATP est surtout régénéré par la voie anaérobie alactique (rapide, sans dioxygène, sans acide lactique) : PC + ADP → C + ATP (phosphocréatine + ADP → créatine + ATP), réaction catalysée par la créatine kinase."},
       "clavier": {"aides": ["voie anaérobie alactique", EQ_PC, "créatine kinase", "sans acide lactique"], "pieges": ["ATP synthase", "fermentation lactique"]},
       "aides": [
         {"texte": "Entre 0 et 10 s, quelle teneur chute le plus ? Et l'acide lactique, augmente-t-il beaucoup ?",
          "dit": "entre zéro et dix secondes، شمن teneur نقصات بزاف؟ و l'acide lactique، واش طلع بزاف؟"},
         {"texte": "La phosphocréatine donne son phosphate à l'ADP : c'est une voie rapide, sans dioxygène et sans acide lactique. Écris-la avec ADP à gauche.",
          "dit": "la phosphocréatine كتعطي le phosphate ديالها ل l'A D P. voie سريعة، بلا dioxygène وبلا acide lactique. كتبها و l'A D P على اليسار."}],
       "correction": {"lignes": [
           {"texte": "3 : de 0 à 10 s, PC : 20 → 6 mmol/kg ; acide lactique : 1 → 2 mmol/kg seulement", "mot": "la phosphocréatine طاحت de vingt à six"},
           {"texte": "voie anaérobie alactique (rapide, sans O₂, sans acide lactique)", "mot": "la voie anaérobie alactique"},
           {"texte": EQ_PC + " (créatine kinase)", "mot": "P C plus A D P donne C plus A T P"}],
         "parole": "Question trois. de zéro à dix secondes، la phosphocréatine طاحت de vingt à six millimoles par kilogramme، و l'acide lactique طلع غير de un à deux. إذن l'A T P كيتجدد ب la voie anaérobie alactique: سريعة، بلا dioxygène، وبلا acide lactique. la réaction: P C plus A D P donne C plus A T P، و l'enzyme هي la créatine kinase."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Décrire l'évolution de l'acide lactique et du glycogène entre 10 s et 3 min, puis en déduire la voie qui prend le relais. Écrire son équation.",
       "texte_dit": "Question quatre : وصف كيفاش تبدلو l'acide lactique و le glycogène، entre dix secondes et trois minutes، ومن بعد استنتج la voie اللي كتاخد البلاصة. كتب l'équation ديالها.",
       "reponse": {"type": "phrase", "attendu": "Entre 10 s et 3 min, l'acide lactique augmente fortement, de 2 à 12 mmol/kg, et le glycogène diminue, de 99 à 78 UA, alors que la phosphocréatine reste basse (6 puis 3 mmol/kg). On en déduit que le glucose venant du glycogène est dégradé par la fermentation lactique (voie anaérobie lactique), qui prend le relais : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP."},
       "clavier": {"aides": ["augmente de 2 à 12 mmol/kg", "diminue de 99 à 78 UA", "fermentation lactique", EQ_FL], "pieges": ["dégage du CO₂", "36 ATP"]},
       "aides": [
         {"texte": "Lis les lignes « acide lactique » et « glycogène » à 10 s puis à 3 min : deux valeurs pour chacune.",
          "dit": "قرا السطر ديال l'acide lactique و ديال le glycogène، à dix secondes، ومن بعد à trois minutes."},
         {"texte": "Quelle voie dégrade le glucose sans dioxygène en produisant de l'acide lactique ? Son équation contient 2 ADP + 2 Pi.",
          "dit": "شمن voie كتفكك le glucose بلا dioxygène، وكتعطي l'acide lactique؟ l'équation ديالها فيها les deux A D P plus deux P i."}],
       "correction": {"lignes": [
           {"texte": "4 : de 10 s à 3 min, acide lactique : 2 → 12 mmol/kg (augmente fortement)", "mot": "l'acide lactique طلع de deux à douze"},
           {"texte": "glycogène : 99 → 78 UA (diminue) ; phosphocréatine basse", "mot": "le glycogène نقص de quatre-vingt-dix-neuf"},
           {"texte": "On en déduit : fermentation lactique (voie anaérobie lactique)", "mot": "la fermentation lactique"},
           {"texte": EQ_FL, "mot": "glucose plus deux A D P"}],
         "parole": "Question quatre. entre dix secondes et trois minutes، l'acide lactique طلع de deux à douze millimoles par kilogramme، و le glycogène نقص de quatre-vingt-dix-neuf à soixante-dix-huit. la phosphocréatine بقات قليلة. إذن le glucose ديال le glycogène كيتفكك بلا dioxygène: هادي la fermentation lactique، la voie anaérobie lactique. glucose plus deux A D P plus deux P i، donne deux acides lactiques plus deux A T P."},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "Entre 3 min et 10 min, comparer l'évolution du glycogène à celle de l'acide lactique, puis en déduire la voie qui fournit alors l'essentiel de l'ATP. Écrire son équation globale.",
       "texte_dit": "Question cinq : entre trois minutes et dix minutes، قارن كيفاش تبدل le glycogène، مع l'acide lactique، ومن بعد استنتج la voie اللي كتعطي أكثر l'A T P. كتب l'équation globale ديالها.",
       "reponse": {"type": "phrase", "attendu": "Entre 3 et 10 min, le glycogène continue à diminuer (de 78 à 56 UA) alors que l'acide lactique n'augmente plus : il diminue un peu, de 12 à 10 mmol/kg. Le glucose est donc dégradé sans production d'acide lactique : c'est la respiration (voie aérobie, avec dioxygène, dans le hyaloplasme puis la mitochondrie) qui fournit l'essentiel de l'ATP : C₆H₁₂O₆ + 6 O₂ + 36 ADP + 36 Pi → 6 CO₂ + 6 H₂O + 36 ATP."},
       "clavier": {"aides": ["continue à diminuer", "n'augmente plus", "respiration (voie aérobie)", EQ_RE], "pieges": ["fermentation lactique", "2 ATP"]},
       "aides": [
         {"texte": "De 3 à 10 min, le glycogène est-il encore utilisé ? Et l'acide lactique, monte-t-il encore ?",
          "dit": "de trois à dix minutes، واش le glycogène باقي كيتستهلك؟ و l'acide lactique، واش باقي كيطلع؟"},
         {"texte": "Du glucose dégradé sans acide lactique : c'est la voie qui utilise le dioxygène. Son équation : glucose + 6 O₂ + 36 ADP + 36 Pi.",
          "dit": "le glucose كيتفكك بلا acide lactique: هادي la voie اللي كتستعمل le dioxygène. l'équation: glucose plus six O deux، plus trente-six A D P plus trente-six P i."}],
       "correction": {"lignes": [
           {"texte": "5 : de 3 à 10 min, glycogène : 78 → 56 UA (continue à diminuer)", "mot": "le glycogène كيكمل ينقص"},
           {"texte": "acide lactique : 12 → 10 mmol/kg (n'augmente plus)", "mot": "l'acide lactique ما بقاش كيطلع"},
           {"texte": "glucose dégradé sans acide lactique : respiration (voie aérobie)", "mot": "هادي la respiration"},
           {"texte": EQ_RE, "mot": "glucose plus six O deux"}],
         "parole": "Question cinq. de trois à dix minutes، le glycogène كيكمل ينقص، de soixante-dix-huit à cinquante-six. ولكن l'acide lactique ما بقاش كيطلع: نقص شوية، de douze à dix. إذن le glucose كيتفكك بلا ما يعطي l'acide lactique: هادي la respiration، la voie aérobie. glucose plus six O deux، plus trente-six A D P plus trente-six P i، donne six C O deux، six H deux O، et trente-six A T P."},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : l'ATP reste presque constant",
     "screen_content": {"lead": "Le muscle consomme l'ATP, et pourtant sa teneur ne baisse presque pas : il est régénéré."},
     "visual": {"kind": "simulation", "url": VOIES, "caption": "Le coureur et la jauge de la réserve d'ATP"},
     "speech_text": {"mixed": "le coureur كيبدا يجري. شوف la jauge ديال l'A T P: نقصات غير شوية، ومن بعد بقات تقريبا عامرة. ف le document حتى هو، l'A T P passe de cinq à environ quatre virgule cinq، وكيبقى تقريبا ثابت. ولكن la contraction كتستهلك l'A T P بلا ما توقف. إذن l'A T P est régénéré، ب نفس السرعة اللي كيتستهلك بيها. كيفاش؟ ب les voies اللي غادي نشوفو."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "ATP : 5,0 → 4,5 à 4,7 mmol/kg : presque constant", "mot": "وكيبقى تقريبا ثابت"},
                  {"texte": "ATP consommé = ATP régénéré", "mot": "إذن l'A T P est régénéré"}],
       "pointage": [{"mot": "le coureur كيبدا يجري", "commande": "play_until", "parametres": {"moment": "depart_reserve_atp"}},
                    {"mot": "شوف la jauge ديال l'A T P", "repere": "jauge_atp"},
                    {"mot": "ومن بعد بقات تقريبا عامرة", "commande": "play_until", "parametres": {"moment": "phosphocreatine"}}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : la phosphocréatine s'effondre en dix secondes",
     "screen_content": {"lead": "p = (20 − 6)/20 × 100 = 70 %."},
     "visual": {"kind": "simulation", "url": VOIES, "caption": "La jauge de la phosphocréatine au début de la course"},
     "speech_text": {"mixed": "شوف la jauge ديال la phosphocréatine: pendant les dix premières secondes، كتطيح بالزربة. ف le document، elle passe de vingt à six millimoles par kilogramme. la perte: vingt moins six، égale quatorze. le pourcentage: quatorze sur vingt، fois cent، égale soixante-dix pour cent. ديما كنقسمو على la valeur ديال الراحة."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "20 − 6 = 14 mmol/kg", "mot": "vingt moins six، égale quatorze"},
                  {"texte": "p = 14/20 × 100 = 70 %", "mot": "égale soixante-dix pour cent"}],
       "pointage": [{"mot": "شوف la jauge ديال la phosphocréatine", "commande": "play_until", "parametres": {"moment": "phosphocreatine"}},
                    {"mot": "شوف la jauge ديال la phosphocréatine", "repere": "jauge_pc"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : la voie anaérobie alactique",
     "screen_content": {"lead": "PC + ADP → C + ATP (créatine kinase) : immédiate, sans O₂, sans acide lactique."},
     "visual": {"kind": "simulation", "url": VOIES, "caption": "La première voie : la phosphocréatine"},
     "speech_text": {"mixed": "ف البداية، la phosphocréatine هي اللي كتنقص، و l'acide lactique تقريبا ما كيطلعش. la phosphocréatine كتعطي le phosphate ديالها ل l'A D P: P C plus A D P donne C plus A T P. l'enzyme هي la créatine kinase. سريعة بزاف، بلا dioxygène، وبلا acide lactique: هادي هي la voie anaérobie alactique. رد البال: anaérobie ما معناهاش fermentation."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "PC + ADP → C + ATP", "mot": "P C plus A D P donne C plus A T P"},
                  {"texte": "enzyme : créatine kinase", "mot": "l'enzyme هي la créatine kinase"},
                  {"texte": "voie anaérobie alactique", "mot": "هادي هي la voie anaérobie alactique"}],
       "pointage": [{"mot": "ف البداية، la phosphocréatine", "commande": "play_until", "parametres": {"moment": "phosphocreatine"}},
                    {"mot": "ف البداية، la phosphocréatine", "repere": "jauge_pc"},
                    {"mot": "و l'acide lactique تقريبا", "repere": "jauge_lactique"},
                    {"mot": "P C plus A D P donne C plus A T P", "repere": "equation_alactique"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : la fermentation lactique prend le relais",
     "screen_content": {"lead": "Acide lactique qui monte, glycogène qui baisse : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP."},
     "visual": {"kind": "simulation", "url": VOIES, "caption": "La deuxième voie : la fermentation lactique"},
     "speech_text": {"mixed": "la phosphocréatine قربات تسالي. شوف la jauge ديال l'acide lactique: كتطلع. ف le document، elle passe de deux à douze millimoles par kilogramme، و le glycogène كينقص. le glucose ديال le glycogène كيتفكك ف le hyaloplasme، بلا dioxygène: هادي la fermentation lactique، la voie anaérobie lactique. glucose plus deux A D P plus deux P i، donne deux acides lactiques plus deux A T P. seulement deux A T P par glucose."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "acide lactique : 2 → 12 mmol/kg ; glycogène : 99 → 78 UA", "mot": "elle passe de deux à douze"},
                  {"texte": "fermentation lactique (anaérobie lactique)", "mot": "هادي la fermentation lactique"},
                  {"texte": EQ_FL, "mot": "glucose plus deux A D P"}],
       "pointage": [{"mot": "la phosphocréatine قربات تسالي", "commande": "play_until", "parametres": {"moment": "fermentation_lactique"}},
                    {"mot": "شوف la jauge ديال l'acide lactique", "repere": "jauge_lactique"},
                    {"mot": "glucose plus deux A D P", "repere": "equation_lactique"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : la respiration fournit l'essentiel de l'ATP",
     "screen_content": {"lead": "Le glycogène baisse encore, l'acide lactique ne monte plus : respiration, 36 ATP par glucose."},
     "visual": {"kind": "simulation", "url": VOIES, "caption": "La troisième voie : la respiration"},
     "speech_text": {"mixed": "l'effort كيطول. شوف la jauge ديال le dioxygène المستهلك: كتطلع، وولات هي الكبيرة. و l'acide lactique ما بقاش كيطلع. ف le document، le glycogène كيكمل ينقص، ولكن l'acide lactique ما بقاش كيزيد. يعني le glucose كيتفكك بلا acide lactique، ب le dioxygène: هادي la respiration، la voie aérobie. glucose plus six O deux، plus trente-six A D P plus trente-six P i، donne six C O deux، six H deux O، et trente-six A T P. ف الجري الطويل، هي اللي كتعطي تقريبا l'A T P كامل."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "glycogène : 78 → 56 UA ; acide lactique : 12 → 10 mmol/kg", "mot": "le glycogène كيكمل ينقص"},
                  {"texte": "respiration (voie aérobie)", "mot": "هادي la respiration"},
                  {"texte": EQ_RE, "mot": "glucose plus six O deux"}],
       "pointage": [{"mot": "l'effort كيطول", "commande": "play_until", "parametres": {"moment": "respiration"}},
                    {"mot": "شوف la jauge ديال le dioxygène", "repere": "jauge_o2"},
                    {"mot": "و l'acide lactique ما بقاش كيطلع", "repere": "jauge_lactique"},
                    {"mot": "glucose plus six O deux", "repere": "equation_aerobie"},
                    {"mot": "ف الجري الطويل", "commande": "play_until", "parametres": {"moment": "effort_long"}}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    vrai_faux("fa_s1", "Plus facile : lire la ligne de l'ATP", "Vrai ou faux, d'après le document.",
      "نتمرنو: قول واش صحيح ولا خطأ.",
      [("Pendant la course, l'ATP reste presque constant.", True, "Vrai : de 5,0 à environ 4,5 à 4,7 mmol/kg."),
       ("L'ATP reste constant parce que le muscle n'en consomme pas.", False, "Faux : la contraction consomme de l'ATP ; il est régénéré aussi vite."),
       ("L'ATP consommé est régénéré au fur et à mesure.", True, "Vrai : c'est ce qu'on déduit de sa teneur presque constante.")]),
    qcm_facile("fa_s2", "Plus facile : le pourcentage de diminution", "سؤال ساهل: اختار le calcul الصحيح.",
      "Le pourcentage de diminution de la phosphocréatine en 10 s est…", ["p = 6/20 × 100", "p = (20 − 6)/6 × 100", "p = (20 − 6)/20 × 100"], 2, {
        "2": {"juste": rep("برافو! شحال نقص، على la valeur ديال الراحة، fois cent. p égale soixante-dix pour cent.", "Juste : p = 14/20 × 100 = 70 %.")},
        "0": {"1": rep("ما تقلقش. هاد القسمة كتعطي شحال بقا، ماشي شحال نقص. عاود اختار.", "Ce calcul donne ce qui reste, pas la diminution. Réessaie."),
              "2": rep("الجواب: p égale vingt moins six، sur vingt، fois cent. p égale soixante-dix pour cent.", "Réponse : p = (20 − 6)/20 × 100 = 70 %.")},
        "1": {"1": rep("قريب! ولكن كنقسمو على la valeur ديال الراحة، ماشي على la valeur اللخرة. عاود اختار.", "On divise par la valeur au repos. Réessaie."),
              "2": rep("الجواب: كنقسمو sur vingt، la valeur au repos. p égale soixante-dix pour cent.", "Réponse : on divise par 20 : p = 70 %.")}},
      "Le pourcentage de diminution de la phosphocréatine en dix secondes est ?"),
    association("fa_s3", "Plus facile : un indice, une voie", "Relie chaque indice du document à la voie qu'il révèle.",
      "سؤال ساهل: ربط كل indice مع la voie ديالو.", "Relie chaque indice à sa voie de régénération de l'ATP.",
      [("1", "La phosphocréatine chute, peu d'acide lactique"), ("2", "L'acide lactique monte fortement"), ("3", "Le glycogène baisse, l'acide lactique ne monte plus")],
      [("a", "Voie anaérobie alactique"), ("b", "Voie anaérobie lactique (fermentation lactique)"), ("c", "Voie aérobie (respiration)")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : PC + ADP → C + ATP, sans acide lactique.", "برافو: la phosphocréatine كتعطي l'A T P بلا acide lactique."),
       "1-b": (False, "Non : la fermentation lactique produit de l'acide lactique ; ici il y en a peu.", "لا، la fermentation lactique كتعطي l'acide lactique، وهنا قليل."),
       "1-c": (False, "Non : la respiration utilise le glucose ; ici c'est la phosphocréatine qui baisse.", "لا، la respiration كتستعمل le glucose، وهنا la phosphocréatine هي اللي نقصات."),
       "2-a": (False, "Non : la voie alactique ne produit pas d'acide lactique.", "لا، la voie alactique ما كتعطيش l'acide lactique."),
       "2-b": (True, "Oui : l'acide lactique est le produit de la fermentation lactique.", "برافو: l'acide lactique كيجي من la fermentation lactique."),
       "2-c": (False, "Non : la respiration ne produit pas d'acide lactique.", "لا، la respiration ما كتعطيش l'acide lactique."),
       "3-a": (False, "Non : la voie alactique utilise la phosphocréatine, pas le glycogène.", "لا، la voie alactique كتستعمل la phosphocréatine، ماشي le glycogène."),
       "3-b": (False, "Non : si c'était la fermentation, l'acide lactique monterait.", "لا، يلا كانت fermentation، l'acide lactique غادي يطلع."),
       "3-c": (True, "Oui : du glucose dégradé sans acide lactique, avec du dioxygène : la respiration.", "برافو: le glucose كيتفكك بلا acide lactique: هادي la respiration.")},
      ("(1 ; a) (2 ; b) (3 ; c).", "la phosphocréatine: alactique. l'acide lactique: la fermentation. le glycogène بلا acide lactique: la respiration.")),
    qcm_facile("fa_s4", "Plus facile : l'équation de la fermentation lactique", "سؤال ساهل: اختار l'équation.",
      "L'équation de la fermentation lactique est…", ["C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP", "C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CH₂OH + 2 CO₂ + 2 ATP", "C₆H₁₂O₆ → 2 CH₃-CHOH-COOH"], 0, {
        "0": {"juste": rep("برافو! le glucose donne deux acides lactiques، et deux A T P.", "Juste : 2 acides lactiques et 2 ATP.")},
        "1": {"1": rep("ما تقلقش. هادي كتعطي l'éthanol و le dioxyde de carbone: هادي fermentation أخرى. عاود اختار.", "Celle-ci donne de l'éthanol et du CO₂ : c'est la fermentation alcoolique. Réessaie."),
              "2": rep("الجواب هو اللولة: deux acides lactiques plus deux A T P. اللي اخترتي هي la fermentation alcoolique.", "Réponse : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP.")},
        "2": {"1": rep("قريب! ولكن فين l'A D P و l'A T P؟ une voie de régénération خاصها تعطي l'A T P. عاود اختار.", "Il manque ADP, Pi et ATP. Réessaie."),
              "2": rep("الجواب هو اللولة: glucose plus deux A D P plus deux P i، donne deux acides lactiques plus deux A T P.", "Réponse : l'équation avec 2 ADP + 2 Pi et 2 ATP.")}},
      "L'équation de la fermentation lactique est ?"),
    qcm_facile("fa_s5", "Plus facile : glycogène et acide lactique", "سؤال ساهل على اللخر ديال الجري.",
      "De 3 à 10 min, le glycogène baisse encore mais l'acide lactique ne monte plus. La voie dominante est…", ["la fermentation lactique", "la respiration", "la voie de la phosphocréatine"], 1, {
        "1": {"juste": rep("برافو! le glucose كيتفكك بلا acide lactique: la respiration.", "Juste : glucose dégradé sans acide lactique : respiration.")},
        "0": {"1": rep("ما تقلقش. la fermentation lactique كتعطي l'acide lactique. واش طلع هنا؟ عاود اختار.", "La fermentation produit de l'acide lactique : monte-t-il ici ? Réessaie."),
              "2": rep("الجواب هو la respiration، حيت l'acide lactique ما بقاش كيطلع.", "Réponse : la respiration.")},
        "2": {"1": rep("لا، la phosphocréatine ما بقاتش كتنقص، وle glycogène هو اللي كينقص. عاود اختار.", "La phosphocréatine ne baisse plus ; c'est le glycogène qui baisse. Réessaie."),
              "2": rep("الجواب هو la respiration: كتستعمل le glucose ديال le glycogène، بلا acide lactique.", "Réponse : la respiration.")}},
      "De trois à dix minutes, le glycogène baisse encore mais l'acide lactique ne monte plus. La voie dominante est ?")
  ]}]},
  "similaire": {
    "id": "svt_ex_ch2_voies_atp_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même protocole chez une autre athlète, qui court elle aussi 10 minutes à allure soutenue et régulière. Le document donne les teneurs mesurées dans son muscle de la cuisse.",
      "intro_dit": "نفس التجربة، مع athlète أخرى، كتجري حتى هي pendant dix minutes، ب سرعة ثابتة. le document فيه les teneurs ديال le muscle ديالها.",
      "figures": [doc(ATP_B, PC_B, LAC_B, GLY_B)],
      "donnees": ["Teneurs en mmol par kg de muscle (glycogène : en unités arbitraires, 100 au repos)"],
      "questions": [
        {"id": "1", "texte": "Décrire l'évolution de la teneur en ATP pendant la course, puis en déduire ce que devient l'ATP consommé.",
         "reponse": {"type": "phrase", "attendu": "Au repos, l'ATP vaut 6,0 mmol/kg ; pendant la course il reste presque constant (entre 5,4 et 5,6 mmol/kg). On en déduit que l'ATP consommé est régénéré au fur et à mesure."},
         "clavier": {"aides": ["6,0 mmol/kg", "presque constant", "régénéré"], "pieges": ["pas consommé"]},
         "correction": {"lignes": [{"texte": "1 : ATP : 6,0 → 5,4 à 5,6 mmol/kg : presque constant", "mot": "l'A T P passe de six"},
                                   {"texte": "l'ATP consommé est régénéré au fur et à mesure", "mot": "est régénéré"}],
                        "parole": "Question un. l'A T P passe de six millimoles par kilogramme à environ cinq virgule cinq: تقريبا ثابت. إذن l'A T P est régénéré ب نفس السرعة اللي كيتستهلك بيها."}},
        {"id": "2", "texte": "Calculer le pourcentage de diminution p de la phosphocréatine pendant les dix premières secondes.",
         "reponse": {"type": "valeur", "grandeur": "p", "valeur": PB, "unite": "%", "tolerance": 0.02, "attendu": "p = (25 − 10)/25 × 100 = 15/25 × 100 = 60 %"},
         "clavier": {"aides": ["(25 − 10)/25", "× 100", "%"], "pieges": ["10/25 × 100"]},
         "correction": {"lignes": [{"texte": "2 : p = (25 − 10)/25 × 100 = 15/25 × 100", "mot": "vingt-cinq moins dix"},
                                   {"texte": "p = 60 %", "mot": "soixante pour cent"}],
                        "parole": "Question deux. p égale vingt-cinq moins dix، sur vingt-cinq، fois cent. p égale soixante pour cent."}},
        {"id": "3", "texte": "En déduire la voie qui domine de 0 à 10 s. Écrire sa réaction et nommer son enzyme.",
         "reponse": {"type": "phrase", "attendu": "La phosphocréatine chute (25 → 10 mmol/kg) avec peu d'acide lactique (1 → 3 mmol/kg) : voie anaérobie alactique : PC + ADP → C + ATP, catalysée par la créatine kinase."},
         "clavier": {"aides": ["voie anaérobie alactique", EQ_PC, "créatine kinase"], "pieges": ["ATP synthase"]},
         "correction": {"lignes": [{"texte": "3 : PC 25 → 10 mmol/kg, peu d'acide lactique : voie anaérobie alactique", "mot": "la voie anaérobie alactique"},
                                   {"texte": EQ_PC + " (créatine kinase)", "mot": "P C plus A D P"}],
                        "parole": "Question trois. la phosphocréatine طاحت de vingt-cinq à dix، مع شوية ديال l'acide lactique: la voie anaérobie alactique. P C plus A D P donne C plus A T P، ب la créatine kinase."}},
        {"id": "4", "texte": "Décrire l'évolution de l'acide lactique et du glycogène entre 10 s et 3 min, puis en déduire la voie qui prend le relais. Écrire son équation.",
         "reponse": {"type": "phrase", "attendu": "De 10 s à 3 min, l'acide lactique augmente de 3 à 14 mmol/kg et le glycogène diminue de 98 à 72 UA, la phosphocréatine restant basse : fermentation lactique (voie anaérobie lactique) : C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP."},
         "clavier": {"aides": ["augmente de 3 à 14", "diminue de 98 à 72", "fermentation lactique"], "pieges": ["respiration"]},
         "correction": {"lignes": [{"texte": "4 : acide lactique 3 → 14 mmol/kg ; glycogène 98 → 72 UA", "mot": "de trois à quatorze"},
                                   {"texte": "fermentation lactique : " + EQ_FL, "mot": "la fermentation lactique"}],
                        "parole": "Question quatre. l'acide lactique طلع de trois à quatorze، و le glycogène نقص de quatre-vingt-dix-huit à soixante-douze: la fermentation lactique. glucose plus deux A D P plus deux P i، donne deux acides lactiques plus deux A T P."}},
        {"id": "5", "texte": "Entre 3 et 10 min, comparer l'évolution du glycogène à celle de l'acide lactique, puis en déduire la voie dominante. Écrire son équation globale.",
         "reponse": {"type": "phrase", "attendu": "De 3 à 10 min, le glycogène continue à diminuer (72 → 50 UA) alors que l'acide lactique n'augmente plus (14 → 11 mmol/kg) : glucose dégradé sans acide lactique : respiration (voie aérobie) : C₆H₁₂O₆ + 6 O₂ + 36 ADP + 36 Pi → 6 CO₂ + 6 H₂O + 36 ATP."},
         "clavier": {"aides": ["continue à diminuer", "n'augmente plus", "respiration"], "pieges": ["fermentation lactique"]},
         "correction": {"lignes": [{"texte": "5 : glycogène 72 → 50 UA ; acide lactique 14 → 11 mmol/kg", "mot": "de soixante-douze à cinquante"},
                                   {"texte": "respiration : " + EQ_RE, "mot": "la respiration"}],
                        "parole": "Question cinq. le glycogène كيكمل ينقص، de soixante-douze à cinquante، و l'acide lactique ما بقاش كيطلع. إذن la respiration: glucose plus six O deux، plus trente-six A D P plus trente-six P i، donne six C O deux، six H deux O، et trente-six A T P."}}
      ]}}
}
ecrire(EX, sys.argv[1])
