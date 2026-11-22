# Exercice SVT ch. 3 (Notion de l'information génétique) — Meselson et Stahl, niveau moyen.
# Entraîne : calculer la densité d'un ADN hybride (moyenne des témoins), décrire tube par tube puis déduire la composition
# des molécules, tester une hypothèse par sa prédiction (conservative en G1, dispersive en G2), prévoir les proportions
# d'une génération suivante (2 molécules hybrides sur 2ⁿ).
# Sources comparées :
# - exploration notion_information_genetique.json : cas_type « meselson » (décrire chaque tube avec sa densité, comparer
#   aux témoins, calculer la moyenne, confronter aux trois hypothèses génération par génération) ; pièges « conclut à la
#   semi-conservative dès G1 » ; insistance Lamsaf « une hypothèse éliminée par génération, la bande hybride ne disparaît
#   jamais » ; valeurs repères 1,710 / 1,717 / 1,724 g·cm⁻³.
# - vidéo Pr Lamsaf (Kt-Sr2em7UM, citée dans l'exploration) : témoins, moyenne 1,717, élimination génération par génération.
# - nationaux PC 2016-2025 : aucun exercice Meselson-Stahl ; QCM 2018 R sur le modèle de réplication (forme reprise dans la
#   version facile, pas son texte).
# - séries en ligne : recherche faite (résultats : séries marocaines dreamjob.ma, moutamadris.ma, TP académie de la Réunion,
#   TD lycée de Versailles) mais les pages n'ont pas pu être lues (réseau de la session : hôtes non résolus) ; comparé
#   donc avec les vidéos d'exercices de l'exploration et les nationaux.
# - cours svt_ch3 : diapositives ig_r1 à ig_r6 (mêmes mots : hybride, léger, lourd, une hypothèse rejetée par génération).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

BASE = "/media/simulations/svt/notion_information_genetique-tableau/"
EXP = BASE + "meselson.html?vue=experience"
PRED = BASE + "meselson.html?vue=predictions"


def fr(x, n=3):
    return f"{x:.{n}f}".replace(".", ",")


def figure_tubes(leger, lourd, titre):
    """Tubes de centrifugation : témoins léger et lourd, G0, G1, G2 (bandes à leur densité)."""
    hyb = round((leger + lourd) / 2, 3)
    y = lambda d: 48 - (d - leger) / (lourd - leger) * 30      # léger en haut (48), lourd en bas (18)
    tubes = [("témoin léger", 20, [(leger, 1)]), ("témoin lourd", 36, [(lourd, 1)]),
             ("G0", 54, [(lourd, 1)]), ("G1", 70, [(hyb, 1)]), ("G2", 86, [(hyb, .5), (leger, .5)])]
    el = [{"f": "ligne", "pts": [[9, 12], [9, 52]], "couleur": "faible"},
          {"f": "texte", "at": [9, 56], "t": "densité (g·cm⁻³)", "taille": "petit", "ancre": "centre", "couleur": "faible"}]
    for d in (leger, hyb, lourd):
        el.append({"f": "ligne", "pts": [[8, y(d)], [10, y(d)]], "couleur": "faible"})
        el.append({"f": "texte", "at": [7.5, y(d) - 1], "t": fr(d), "taille": "petit", "ancre": "droite", "couleur": "faible"})
    for nom, x, bandes in tubes:
        el.append({"f": "rect", "de": [x - 4, 10], "a": [x + 4, 52], "couleur": "blanc", "arrondi": True})
        for d, q in bandes:
            e = 1.4 if q == 1 else 0.8
            el.append({"f": "rect", "de": [x - 3.4, y(d) - e / 2], "a": [x + 3.4, y(d) + e / 2], "couleur": "cyan", "remplir": "cyan"})
        el.append({"f": "texte", "at": [x, 5], "t": nom, "taille": "petit", "ancre": "centre", "couleur": "jaune" if nom.startswith("G") else "blanc"})
    el.append({"f": "texte", "at": [86, 0.5], "t": "(deux bandes d'égale importance)", "taille": "petit", "ancre": "centre", "couleur": "faible"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 100, "h": 60},
            "legende": "Position des bandes d'ADN après centrifugation (l'ADN le plus lourd descend le plus bas). G0 : avant le transfert ; G1, G2 : générations après le transfert sur ¹⁴N.",
            "elements": el}


# ---- données de l'exercice (densités du cours, celles que montre meselson.html)
L, H = 1.710, 1.724
HY = round((L + H) / 2, 3)
assert HY == 1.717
P4 = 2 / 2 ** 4 * 100
assert P4 == 12.5

Q = [
  {"id": "1", "texte": "En utilisant les deux témoins, calculer la densité d attendue pour un ADN hybride (un brin à ¹⁵N et un brin à ¹⁴N).",
   "texte_dit": "السؤال un: ب les deux témoins، حسب la densité ديال l'A D N hybride، يعني molécule فيها brin ب l'azote quinze، و brin ب l'azote quatorze.",
   "reponse": {"type": "valeur", "grandeur": "d", "valeur": HY, "unite": "g·cm⁻³", "tolerance": 0.001,
               "attendu": f"d = ({fr(L)} + {fr(H)})/2 = 3,434/2 = {fr(HY)} g·cm⁻³"},
   "clavier": {"aides": ["d = (d léger + d lourd)/2", fr(L), fr(H), "g·cm⁻³"], "pieges": ["3,434", f"{fr(H)} − {fr(L)}"]},
   "aides": [
     {"texte": "Un ADN hybride a un brin léger et un brin lourd : sa densité est entre celles des deux témoins.",
      "dit": "l'A D N hybride فيه brin léger و brin lourd: la densité ديالو كاينة بين la densité ديال le témoin léger و la densité ديال le témoin lourd."},
     {"texte": "Moitié léger, moitié lourd : calcule la moyenne des deux densités des témoins.",
      "dit": "النص léger والنص lourd: حسب la moyenne ديال les deux densités، يعني جمعهم، ومن بعد la somme sur deux."}],
   "correction": {"lignes": [
       {"texte": f"1 : un ADN hybride : moitié ¹⁴N, moitié ¹⁵N, donc d = ({fr(L)} + {fr(H)})/2", "mot": "la densité ديالو هي la moyenne"},
       {"texte": "d = 3,434/2", "mot": "égale trois virgule quatre cent trente-quatre"},
       {"texte": f"d = {fr(HY)} g·cm⁻³", "mot": "égale un virgule sept cent dix-sept grammes par centimètre cube"}],
     "parole": "السؤال un. l'A D N hybride فيه brin léger و brin lourd، إذن la densité ديالو هي la moyenne. un virgule sept cent dix، plus un virgule sept cent vingt-quatre، égale trois virgule quatre cent trente-quatre. sur deux، كتعطي: d égale un virgule sept cent dix-sept grammes par centimètre cube."},
   "explication": "ex_s1", "facile": "fa_s1"},
  {"id": "2", "texte": "Décrire les résultats obtenus aux générations G0, G1 et G2, puis déduire la composition des molécules d'ADN à chaque génération.",
   "texte_dit": "السؤال deux: وصف les résultats ديال la génération zéro، la génération un، et la génération deux، ومن بعد استنتج شنو فيهم les molécules d'A D N ف كل génération.",
   "reponse": {"type": "phrase", "attendu": f"G0 : une seule bande, à {fr(H)} g·cm⁻³, comme le témoin lourd : toutes les molécules sont lourdes (deux brins à ¹⁵N). G1 : une seule bande, à {fr(HY)} g·cm⁻³ : toutes les molécules sont hybrides (densité intermédiaire, moitié ¹⁵N, moitié ¹⁴N). G2 : deux bandes d'égale importance, à {fr(HY)} et à {fr(L)} g·cm⁻³ : on en déduit 50 % de molécules hybrides et 50 % de molécules légères (deux brins à ¹⁴N)."},
   "clavier": {"aides": ["une seule bande", "deux bandes", "hybride", "léger", "lourd", "50 %", "On en déduit que"], "pieges": ["semi-conservative dès G1", "trois bandes"]},
   "aides": [
     {"texte": "Lis les tubes un par un et compare la place de chaque bande à celle des témoins.",
      "dit": "قرا les tubes واحد ب واحد، وقارن البلاصة ديال كل bande مع les témoins."},
     {"texte": "Pour chaque génération : nombre de bandes, densité de chaque bande, puis « on en déduit que les molécules sont… » (lourdes, hybrides, légères, en quelle proportion).",
      "dit": "ف كل génération: شحال من bande، والdensité ديال كل bande. ومن بعد قول: on en déduit que، les molécules lourdes ولا hybrides ولا légères، وبشحال من pour cent."}],
   "correction": {"lignes": [
       {"texte": f"2 : G0 : une bande à {fr(H)} (comme le témoin lourd) : molécules lourdes", "mot": "toutes les molécules lourdes"},
       {"texte": f"G1 : une bande à {fr(HY)} : toutes les molécules hybrides", "mot": "toutes les molécules hybrides"},
       {"texte": f"G2 : deux bandes égales, {fr(HY)} et {fr(L)} : 50 % hybrides, 50 % légères", "mot": "cinquante pour cent hybrides"}],
     "parole": "السؤال deux. ف la génération zéro: une seule bande، à un virgule sept cent vingt-quatre، بحال le témoin lourd. on en déduit: toutes les molécules lourdes. ف la génération un: une seule bande، à un virgule sept cent dix-sept. on en déduit: toutes les molécules hybrides، brin lourd و brin léger. ف la génération deux: deux bandes بنفس الكمية، à un virgule sept cent dix-sept، et à un virgule sept cent dix. on en déduit: cinquante pour cent hybrides، et cinquante pour cent légères."},
   "explication": "ex_s2", "facile": "fa_s2"},
  {"id": "3", "texte": "Indiquer le résultat que prévoit l'hypothèse conservative à la génération G1, puis montrer que le résultat obtenu en G1 permet de la rejeter.",
   "texte_dit": "السؤال trois: قول شنو كانت غادي تعطي l'hypothèse conservative ف la génération un، ومن بعد بين بلي النتيجة ديال la génération un كترفضها.",
   "reponse": {"type": "phrase", "attendu": f"Selon l'hypothèse conservative, la molécule mère reste entière (lourde) et la molécule fille est entièrement nouvelle (légère) : en G1, on aurait deux bandes d'égale importance, l'une lourde à {fr(H)} et l'autre légère à {fr(L)} g·cm⁻³. Or on obtient une seule bande, hybride, à {fr(HY)} : l'hypothèse conservative est rejetée."},
   "clavier": {"aides": ["molécule mère entière", "deux bandes", "une seule bande", "Or", "rejetée"], "pieges": ["une bande hybride", "trois bandes"]},
   "aides": [
     {"texte": "Dans l'hypothèse conservative, que devient la molécule mère lourde ? Et la molécule fille, faite sur ¹⁴N ?",
      "dit": "ف l'hypothèse conservative، la molécule mère lourde شنو كيوقع ليها؟ و la molécule fille اللي تصاوبات ف l'azote quatorze، كيفاش كتكون؟"},
     {"texte": "Une molécule lourde et une molécule légère : combien de bandes, à quelles densités ? Compare avec le tube G1 (« or… donc… »).",
      "dit": "molécule lourde و molécule légère: شحال من bande، وفين؟ قارن مع le tube ديال la génération un، وكتب: or، donc."}],
   "correction": {"lignes": [
       {"texte": "3 : conservative : molécule mère entière (lourde) + molécule fille toute nouvelle (légère)", "mot": "la molécule mère كتبقى كاملة"},
       {"texte": f"prévision en G1 : deux bandes, {fr(H)} et {fr(L)}", "mot": "deux bandes، une lourde et une légère"},
       {"texte": f"or : une seule bande à {fr(HY)} → hypothèse conservative rejetée", "mot": "l'hypothèse conservative مرفوضة"}],
     "parole": "السؤال trois. ف l'hypothèse conservative، la molécule mère كتبقى كاملة، lourde، و la molécule fille كتكون جديدة كاملة، légère. إذن ف la génération un، كانت غادي تعطي deux bandes، une lourde et une légère. ولكن النتيجة: une seule bande، hybride. إذن l'hypothèse conservative مرفوضة."},
   "explication": "ex_s3", "facile": "fa_s3"},
  {"id": "4", "texte": "Expliquer pourquoi le résultat de G1 ne permet pas de choisir entre les hypothèses semi-conservative et dispersive, puis montrer que le résultat de G2 permet de trancher.",
   "texte_dit": "السؤال quatre: فسر علاش النتيجة ديال la génération un ما كتخليناش نختارو بين la semi-conservative و la dispersive، ومن بعد بين بلي la génération deux كتفصل بيناتهم.",
   "reponse": {"type": "phrase", "attendu": f"En G1, les deux hypothèses prévoient la même chose : une seule bande hybride à {fr(HY)} (chaque molécule contient autant de ¹⁵N que de ¹⁴N). En G2, la semi-conservative prévoit deux bandes d'égale importance (hybride à {fr(HY)} et légère à {fr(L)}), alors que la dispersive prévoit une seule bande, entre {fr(L)} et {fr(HY)}. On obtient deux bandes : l'hypothèse dispersive est rejetée, seule l'hypothèse semi-conservative explique les résultats."},
   "clavier": {"aides": ["même prévision en G1", "une seule bande", "deux bandes", "dispersive rejetée", "semi-conservative"], "pieges": ["conservative", "trois bandes"]},
   "aides": [
     {"texte": "En G1, combien de bandes prévoit chacune des deux hypothèses, et à quelle densité ?",
      "dit": "ف la génération un، شحال من bande كتعطي كل hypothèse، وف أشمن densité؟"},
     {"texte": "En G2 : dans la dispersive, l'ancien et le nouveau restent mélangés dans chaque brin, donc toutes les molécules ont la même densité. Dans la semi-conservative, une molécule hybride donne une hybride et une légère.",
      "dit": "ف la génération deux: ف la dispersive، القديم والجديد مخلطين ف كل brin، إذن كل les molécules عندهم نفس la densité. وف la semi-conservative، molécule hybride كتعطي une hybride et une légère."}],
   "correction": {"lignes": [
       {"texte": f"4 : G1 : les deux hypothèses prévoient une seule bande hybride ({fr(HY)})", "mot": "les deux hypothèses كيعطيو une seule bande hybride"},
       {"texte": "G2 : semi-conservative → deux bandes égales (hybride + légère) ; dispersive → une seule bande intermédiaire", "mot": "la dispersive كتعطي une seule bande"},
       {"texte": "observé : deux bandes → dispersive rejetée ; la réplication est semi-conservative", "mot": "la semi-conservative هي اللي كتفسر les résultats"}],
     "parole": "السؤال quatre. ف la génération un، les deux hypothèses كيعطيو une seule bande hybride: ما نقدروش نختارو. ف la génération deux، la semi-conservative كتعطي deux bandes، hybride et légère، بنفس الكمية. أما la dispersive كتعطي une seule bande، بين hybride et légère. النتيجة: deux bandes. إذن la dispersive مرفوضة، و la semi-conservative هي اللي كتفسر les résultats."},
   "explication": "ex_s4", "facile": "fa_s4"},
  {"id": "5", "texte": "Les bactéries sont laissées sur ¹⁴N jusqu'à la génération G4. En vous appuyant sur l'hypothèse retenue, calculer le pourcentage de molécules hybrides attendu en G4.",
   "texte_dit": "السؤال cinq: خلينا les bactéries ف l'azote quatorze حتى la génération quatre. ب l'hypothèse اللي بقات، حسب le pourcentage ديال les molécules hybrides ف la génération quatre.",
   "reponse": {"type": "valeur", "grandeur": "p", "valeur": P4, "unite": "%", "tolerance": 0.02,
               "attendu": "G4 : 2⁴ = 16 molécules (pour une molécule de départ), dont 2 hybrides ; p = 2/16 × 100 = 12,5 %"},
   "clavier": {"aides": ["2⁴ = 16", "2 hybrides", "× 100", "%"], "pieges": ["2/8 × 100", "1/4 × 100"]},
   "aides": [
     {"texte": "Les deux brins lourds de la molécule de départ ne disparaissent jamais : chacun reste dans une molécule hybride. Combien de molécules hybrides à chaque génération ?",
      "dit": "les deux brins lourds ديال la molécule ديال البداية ما كيضيعوش: كل واحد كيبقى ف molécule hybride. إذن شحال من molécule hybride ف كل génération؟"},
     {"texte": "Le nombre de molécules double à chaque génération : 1, 2, 4, 8… Combien en G4 ? Puis p = (hybrides / total) × 100.",
      "dit": "le nombre ديال les molécules كيتضاعف ف كل génération. شحال ف la génération quatre؟ ومن بعد، le pourcentage: les hybrides، sur le total، fois cent."}],
   "correction": {"lignes": [
       {"texte": "5 : en G4 : 2⁴ = 16 molécules pour une molécule de départ", "mot": "égale seize molécules"},
       {"texte": "toujours 2 molécules hybrides (les deux brins ¹⁵N de départ)", "mot": "toujours deux hybrides"},
       {"texte": "p = 2/16 × 100 = 12,5 %", "mot": "douze virgule cinq pour cent"}],
     "parole": "السؤال cinq. le nombre ديال les molécules كيتضاعف ف كل génération: en G quatre، deux puissance quatre، égale seize molécules. les deux brins lourds ديال البداية كيبقاو: toujours deux hybrides. p égale deux sur seize، fois cent، égale douze virgule cinq pour cent."},
   "explication": "ex_s5", "facile": "fa_s5"},
]

EXPLICATION = [
  {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : la densité d'un ADN hybride, la moyenne des témoins",
   "screen_content": {"lead": "Témoin léger 1,710 ; témoin lourd 1,724 ; hybride : la moyenne, 1,717 g·cm⁻³."},
   "visual": {"kind": "simulation", "url": EXP, "caption": "Les témoins, puis le calcul de la moyenne"},
   "speech_text": {"mixed": "شوف les deux témoins. l'A D N léger، ديال l'azote quatorze، كيبقى الفوق: un virgule sept cent dix. و l'A D N lourd، ديال l'azote quinze، كيهبط التحت: un virgule sept cent vingt-quatre. molécule hybride فيها brin léger و brin lourd، إذن la densité ديالها هي la moyenne. un virgule sept cent dix، plus un virgule sept cent vingt-quatre، égale trois virgule quatre cent trente-quatre، sur deux، égale un virgule sept cent dix-sept grammes par centimètre cube. وهادي هي بالضبط la bande ديال la génération un."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "témoins : 1,710 (léger) ; 1,724 (lourd)", "mot": "شوف les deux témoins"},
                {"texte": "d = (1,710 + 1,724)/2 = 1,717 g·cm⁻³", "mot": "sur deux، égale un virgule sept cent dix-sept"}],
     "pointage": [{"mot": "شوف les deux témoins", "commande": "play_until", "parametres": {"moment": "temoins"}},
                  {"mot": "شوف les deux témoins", "cible": "centre:0"},
                  {"mot": "l'A D N léger، ديال", "repere": "tube_leger"},
                  {"mot": "و l'A D N lourd، ديال", "repere": "tube_lourd"},
                  {"mot": "molécule hybride فيها", "commande": "play_until", "parametres": {"moment": "calcul_moyenne"}},
                  {"mot": "sur deux، égale un virgule sept cent dix-sept", "repere": "calcul"},
                  {"mot": "sur deux، égale un virgule sept cent dix-sept", "cible": "centre:1"},
                  {"mot": "وهادي هي بالضبط", "repere": "tube_g1"}]}},
  {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : lire chaque tube, puis déduire",
   "screen_content": {"lead": "G0 : lourd. G1 : une bande hybride. G2 : hybride + léger, moitié-moitié."},
   "visual": {"kind": "simulation", "url": EXP, "caption": "Les tubes G0, G1, G2 comparés aux témoins"},
   "speech_text": {"mixed": "نقراو les tubes واحد ب واحد، ونقارنو مع les témoins. ف la génération zéro: une seule bande، à un virgule sept cent vingt-quatre، بحال le témoin lourd: les molécules lourdes. ف la génération un: une seule bande، à un virgule sept cent dix-sept: toutes les molécules hybrides. ف la génération deux: deux bandes بنفس الكمية، hybride et légère: cinquante pour cent hybrides، et cinquante pour cent légères. ف كل génération: نوصف، ومن بعد on en déduit."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "G0 : une bande à 1,724 → lourdes", "mot": "بحال le témoin lourd"},
                {"texte": "G1 : une bande à 1,717 → hybrides", "mot": "toutes les molécules hybrides"},
                {"texte": "G2 : 1,717 + 1,710 → 50 % / 50 %", "mot": "cinquante pour cent hybrides"}],
     "pointage": [{"mot": "نقراو les tubes", "commande": "play_until", "parametres": {"moment": "temoins"}},
                  {"mot": "ف la génération zéro", "commande": "play_until", "parametres": {"moment": "g0"}},
                  {"mot": "ف la génération zéro", "repere": "tube_g0"},
                  {"mot": "بحال le témoin lourd", "cible": "centre:0"},
                  {"mot": "ف la génération un", "commande": "play_until", "parametres": {"moment": "g1_bande"}},
                  {"mot": "ف la génération un", "repere": "tube_g1"},
                  {"mot": "toutes les molécules hybrides", "cible": "centre:1"},
                  {"mot": "ف la génération deux", "commande": "play_until", "parametres": {"moment": "g2_bandes"}},
                  {"mot": "ف la génération deux", "repere": "tube_g2"},
                  {"mot": "cinquante pour cent hybrides", "cible": "centre:2"}]}},
  {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : la conservative prévoyait deux bandes dès G1",
   "screen_content": {"lead": "Conservative : une molécule lourde + une légère → deux bandes en G1. Observé : une seule bande hybride."},
   "visual": {"kind": "simulation", "url": EXP, "caption": "L'hypothèse conservative confrontée au tube G1"},
   "speech_text": {"mixed": "l'hypothèse conservative كتقول: la molécule mère كتبقى كاملة، lourde، و la molécule fille جديدة كاملة، légère. إذن ف la génération un، كانت غادي تعطي deux bandes: une bande lourde، et une bande légère. ولكن le tube ديال la génération un فيه une seule bande، hybride. إذن l'hypothèse conservative مرفوضة."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "prévision : deux bandes (1,724 et 1,710)", "mot": "كانت غادي تعطي deux bandes"},
                {"texte": "observé : une bande à 1,717 → rejetée", "mot": "إذن l'hypothèse conservative مرفوضة"}],
     "pointage": [{"mot": "l'hypothèse conservative كتقول", "commande": "play_until", "parametres": {"moment": "conservative"}},
                  {"mot": "l'hypothèse conservative كتقول", "repere": "h_conservative"},
                  {"mot": "كانت غادي تعطي deux bandes", "cible": "centre:0"},
                  {"mot": "ولكن le tube", "commande": "play_until", "parametres": {"moment": "g1_bande"}},
                  {"mot": "ولكن le tube", "repere": "tube_g1"},
                  {"mot": "إذن l'hypothèse conservative مرفوضة", "commande": "play_until", "parametres": {"moment": "conservative_rejetee"}},
                  {"mot": "إذن l'hypothèse conservative مرفوضة", "cible": "centre:1"}]}},
  {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : G2 sépare la semi-conservative et la dispersive",
   "screen_content": {"lead": "En G1, même prévision. En G2 : semi-conservative deux bandes, dispersive une seule. Observé : deux bandes."},
   "visual": {"kind": "simulation", "url": PRED, "caption": "Le tableau des prédictions, comparé aux résultats"},
   "speech_text": {"mixed": "هاد le tableau فيه شنو كتقول كل hypothèse. ف la génération un، les deux hypothèses كيعطيو une seule bande hybride: ما نقدروش نختارو. ف la génération deux، la semi-conservative كتعطي deux bandes، hybride et légère. أما la dispersive كتعطي une seule bande، بين hybride et légère. دابا les résultats: deux bandes. إذن la dispersive مرفوضة، و la semi-conservative هي اللي كتفسر les résultats."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "G1 : semi-conservative = dispersive (une bande hybride)", "mot": "ما نقدروش نختارو"},
                {"texte": "G2 : semi → deux bandes ; dispersive → une bande", "mot": "أما la dispersive كتعطي une seule bande"},
                {"texte": "observé : deux bandes → semi-conservative", "mot": "و la semi-conservative هي اللي كتفسر les résultats"}],
     "pointage": [{"mot": "هاد le tableau", "commande": "play_until", "parametres": {"moment": "tableau"}},
                  {"mot": "ما نقدروش نختارو", "cible": "centre:0"},
                  {"mot": "ف la génération deux، la semi-conservative", "commande": "play_until", "parametres": {"moment": "ligne_semi"}},
                  {"mot": "ف la génération deux، la semi-conservative", "repere": "l_semi"},
                  {"mot": "أما la dispersive كتعطي une seule bande", "commande": "play_until", "parametres": {"moment": "ligne_dispersive"}},
                  {"mot": "أما la dispersive كتعطي une seule bande", "repere": "l_dispersive"},
                  {"mot": "أما la dispersive كتعطي une seule bande", "cible": "centre:1"},
                  {"mot": "دابا les résultats", "commande": "play_until", "parametres": {"moment": "observe"}},
                  {"mot": "دابا les résultats", "repere": "observe"},
                  {"mot": "إذن la dispersive مرفوضة", "commande": "play_until", "parametres": {"moment": "comparaison"}},
                  {"mot": "و la semi-conservative هي اللي كتفسر les résultats", "cible": "centre:2"}]}},
  {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : toujours deux molécules hybrides",
   "screen_content": {"lead": "Les deux brins lourds de départ restent chacun dans une molécule hybride : 2 sur 2ⁿ."},
   "visual": {"kind": "simulation", "url": EXP, "caption": "Le tube G3 et l'arbre des molécules"},
   "speech_text": {"mixed": "شوف le tube ديال la génération trois: la bande légère كتكبر، و la bande hybride كتصغر، ولكن ما كتختفيش. علاش؟ شوف l'arbre. les deux brins lourds ديال البداية ما كيضيعوش: كل واحد كيبقى ف molécule hybride. génération un: deux molécules. génération deux: quatre molécules. génération trois: huit molécules. le nombre des molécules hybrides، lui، reste deux. ف la génération quatre: huit fois deux، égale seize molécules، et toujours deux hybrides. deux sur seize، fois cent، égale douze virgule cinq pour cent."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "à chaque génération : nombre de molécules × 2", "mot": "génération trois: huit molécules"},
                {"texte": "hybrides : toujours 2", "mot": "reste deux"},
                {"texte": "G4 : 2/16 × 100 = 12,5 %", "mot": "égale douze virgule cinq pour cent"}],
     "pointage": [{"mot": "شوف le tube ديال la génération trois", "commande": "play_until", "parametres": {"moment": "g3"}},
                  {"mot": "شوف le tube ديال la génération trois", "repere": "tube_g3"},
                  {"mot": "شوف l'arbre", "commande": "play_until", "parametres": {"moment": "arbre_g0_g3"}},
                  {"mot": "شوف l'arbre", "repere": "arbre"},
                  {"mot": "génération trois: huit molécules", "cible": "centre:0"},
                  {"mot": "reste deux", "cible": "centre:1"},
                  {"mot": "égale douze virgule cinq pour cent", "cible": "centre:2"}]}},
]

FACILE = [
  qcm_facile("fa_s1", "Plus facile : la densité hybride", "سؤال ساهل: اختار la densité ديال l'A D N hybride.",
    "Avec des témoins à 1,710 et 1,724 g·cm⁻³, un ADN hybride a une densité de…",
    ["3,434 g·cm⁻³", "1,717 g·cm⁻³", "1,724 g·cm⁻³"], 1, {
      "1": {"juste": rep("برافو! la moyenne: un virgule sept cent dix، plus un virgule sept cent vingt-quatre، sur deux، égale un virgule sept cent dix-sept.", "Juste : d = (1,710 + 1,724)/2 = 1,717 g·cm⁻³.")},
      "0": {"1": rep("قريب! جمعتي les deux densités مزيان، ولكن la moyenne خاصها قسمة. شنو خاصك دير من بعد الجمع؟ عاود اختار.", "Tu as fait la somme ; une moyenne se divise ensuite. Réessaie."),
            "2": rep("الجواب هو un virgule sept cent dix-sept. trois virgule quatre cent trente-quatre هي غير la somme، خاصها تتقسم على deux.", "Réponse : 1,717 g·cm⁻³ ; 3,434 n'est que la somme, à diviser par 2.")},
      "2": {"1": rep("لا، un virgule sept cent vingt-quatre هي la densité ديال l'A D N lourd، avec deux brins lourds. l'hybride فيه un seul brin lourd. عاود اختار.", "1,724, c'est l'ADN lourd (deux brins ¹⁵N). Un hybride n'a qu'un brin lourd. Réessaie."),
            "2": rep("الجواب هو un virgule sept cent dix-sept: la moyenne بين le léger و le lourd.", "Réponse : 1,717 g·cm⁻³, la moyenne du léger et du lourd.")}},
    "Avec des témoins à un virgule sept cent dix et un virgule sept cent vingt-quatre, la densité de l'A D N hybride est ?"),
  association("fa_s2", "Plus facile : chaque génération et son tube", "Relie chaque génération à son résultat.",
    "سؤال ساهل: ربط كل génération مع le résultat ديالها.",
    "Relie chaque génération au résultat de la centrifugation.",
    [("1", "G0"), ("2", "G1"), ("3", "G2")],
    [("a", "une seule bande à 1,724"), ("b", "une seule bande à 1,717"), ("c", "deux bandes égales : 1,717 et 1,710"), ("d", "une seule bande à 1,710")],
    {"1": "a", "2": "b", "3": "c"},
    {"1-a": (True, "Oui : en G0, avant le transfert, l'ADN est lourd.", "برافو: ف la génération zéro، قبل الانتقال، l'A D N lourd."),
     "1-b": (False, "Non : 1,717, c'est l'hybride ; en G0 il n'y a pas encore eu de réplication sur ¹⁴N.", "لا، هادي hybride. ف la génération zéro، مازال ما كانتش réplication ف l'azote quatorze."),
     "1-c": (False, "Non : deux bandes, c'est après deux réplications sur ¹⁴N.", "لا، deux bandes كيبانو غير من بعد deux réplications ف l'azote quatorze."),
     "1-d": (False, "Non : en G0, les bactéries ont poussé sur ¹⁵N : leur ADN est lourd, pas léger.", "لا، ف la génération zéro، les bactéries كانو ف l'azote quinze: l'A D N ديالهم lourd، ماشي léger."),
     "2-a": (False, "Non : après une réplication sur ¹⁴N, chaque molécule a reçu un brin nouveau léger.", "لا، من بعد une seule réplication، كل molécule فيها brin جديد léger."),
     "2-b": (True, "Oui : en G1, une seule bande hybride à 1,717.", "برافو: ف la génération un، une seule bande hybride."),
     "2-c": (False, "Non : la bande légère n'apparaît qu'en G2.", "لا، la bande légère كتبان غير ف la génération deux."),
     "2-d": (False, "Non : en G1 les brins lourds sont encore là, chacun dans une molécule hybride.", "لا، ف la génération un، les brins lourds مازال كاينين، كل واحد ف molécule hybride."),
     "3-a": (False, "Non : en G2, il n'y a plus de molécule lourde.", "لا، ف la génération deux، ما بقاتش حتى molécule lourde."),
     "3-b": (False, "Non : en G2, une partie des molécules est devenue légère.", "لا، ف la génération deux، شي molécules ولاو légères."),
     "3-c": (True, "Oui : en G2, deux bandes égales, hybride et légère.", "برافو: ف la génération deux، deux bandes بنفس الكمية، hybride et légère."),
     "3-d": (False, "Non : la bande hybride ne disparaît jamais.", "لا، la bande hybride ما كتختفيش أبدا.")},
    ("(1 ; a) (2 ; b) (3 ; c) : la bande à 1,710 seule (d) n'apparaît dans aucun tube.", "الجواب: un مع a، deux مع b، trois مع c. و d ما كايناش ف حتى tube.")),
  vrai_faux("fa_s3", "Plus facile : l'hypothèse conservative", "Vrai ou faux : l'hypothèse conservative.",
    "سؤال ساهل: صحيح ولا غالط، على l'hypothèse conservative.",
    [("Dans l'hypothèse conservative, la molécule mère reste entière après la réplication.", True, "Oui : la molécule mère reste lourde et la molécule fille est entièrement nouvelle."),
     ("L'hypothèse conservative prévoit une seule bande hybride en G1.", False, "Non : elle prévoit deux bandes, une lourde (1,724) et une légère (1,710)."),
     ("Le tube G1 suffit à rejeter l'hypothèse conservative.", True, "Oui : on observe une seule bande à 1,717, pas deux bandes.")]),
  qcm_facile("fa_s4", "Plus facile : la prévision dispersive en G2", "سؤال ساهل: شنو كتقول la dispersive ف la génération deux؟",
    "En G2, l'hypothèse dispersive prévoit…",
    ["deux bandes : hybride et légère", "une seule bande, entre 1,710 et 1,717", "deux bandes : lourde et légère"], 1, {
      "1": {"juste": rep("برافو! ف la dispersive، القديم والجديد مخلطين ف كل brin: كل les molécules عندهم نفس la densité، une seule bande.", "Juste : une seule bande intermédiaire, puisque toutes les molécules ont la même densité.")},
      "0": {"1": rep("هادي هي اللي كتقول la semi-conservative. ف la dispersive، واش les molécules عندهم densités مختلفة؟ عاود اختار.", "Ça, c'est la semi-conservative. Dans la dispersive, les molécules ont-elles des densités différentes ? Réessaie."),
            "2": rep("الجواب هو une seule bande، entre un virgule sept cent dix et un virgule sept cent dix-sept. deux bandes هي ديال la semi-conservative.", "Réponse : une seule bande intermédiaire ; deux bandes hybride + légère, c'est la semi-conservative.")},
      "2": {"1": rep("لا، lourde et légère هي ديال la conservative. ف la dispersive، كيفاش القديم والجديد؟ عاود اختار.", "Lourde et légère, c'est la conservative. Dans la dispersive, comment sont l'ancien et le nouveau ? Réessaie."),
            "2": rep("الجواب هو une seule bande intermédiaire: ف la dispersive، كل molécule فيها نفس الخليط.", "Réponse : une seule bande intermédiaire.")}},
    "En génération deux, l'hypothèse dispersive prévoit ?"),
  qcm_facile("fa_s5", "Plus facile : combien d'hybrides en G4 ?", "سؤال ساهل: ف la génération quatre، شحال من molécule hybride؟",
    "En G4, pour une molécule de départ, on a 16 molécules. Combien sont hybrides ?",
    ["8", "2", "4"], 1, {
      "1": {"juste": rep("برافو! les deux brins lourds ديال البداية كيبقاو، كل واحد ف molécule hybride. deux sur seize، égale douze virgule cinq pour cent.", "Juste : 2 hybrides sur 16, soit 12,5 %.")},
      "0": {"1": rep("لا، huit هو النص. واش les brins lourds كيتزادو؟ شحال كانو ف البداية؟ عاود اختار.", "8, c'est la moitié. Les brins lourds se multiplient-ils ? Combien y en avait-il au départ ? Réessaie."),
            "2": rep("الجواب هو deux: les brins lourds ما كيتزادوش، deux au départ، et deux à chaque génération.", "Réponse : 2 ; les brins lourds ne se multiplient pas.")},
      "2": {"1": rep("قريب، ولكن au départ، il y avait seulement deux brins lourds. وكل brin lourd كيبقى ف une seule molécule. عاود اختار.", "Il n'y avait que deux brins lourds au départ, chacun dans une seule molécule. Réessaie."),
            "2": rep("الجواب هو deux: deux brins lourds، deux molécules hybrides.", "Réponse : 2 molécules hybrides (deux brins lourds).")}},
    "En génération quatre, sur seize molécules, combien sont hybrides ?"),
]

# ---- exercice semblable : une autre souche bactérienne, autres densités, jusqu'à G3
L2, H2 = 1.702, 1.716
HY2 = round((L2 + H2) / 2, 3)
assert HY2 == 1.709
P3 = 2 / 2 ** 3 * 100
SIM_Q = [
  {"id": "1", "texte": "En utilisant les deux témoins, calculer la densité d attendue pour un ADN hybride.",
   "reponse": {"type": "valeur", "grandeur": "d", "valeur": HY2, "unite": "g·cm⁻³", "tolerance": 0.001,
               "attendu": f"d = ({fr(L2)} + {fr(H2)})/2 = 3,418/2 = {fr(HY2)} g·cm⁻³"},
   "clavier": {"aides": ["d = (d léger + d lourd)/2", fr(L2), fr(H2)], "pieges": ["3,418"]},
   "correction": {"lignes": [{"texte": f"1 : d = ({fr(L2)} + {fr(H2)})/2", "mot": "la moyenne"},
                             {"texte": f"d = 3,418/2 = {fr(HY2)} g·cm⁻³", "mot": "un virgule sept cent neuf"}],
                  "parole": "l'A D N hybride: la moyenne. un virgule sept cent deux، plus un virgule sept cent seize، égale trois virgule quatre cent dix-huit، sur deux، égale un virgule sept cent neuf grammes par centimètre cube."}},
  {"id": "2", "texte": "Décrire les résultats obtenus aux générations G0, G1 et G2, puis déduire la composition des molécules d'ADN à chaque génération.",
   "reponse": {"type": "phrase", "attendu": f"G0 : une seule bande à {fr(H2)} (comme le témoin lourd) : molécules lourdes. G1 : une seule bande à {fr(HY2)} : toutes les molécules sont hybrides. G2 : deux bandes égales à {fr(HY2)} et {fr(L2)} : 50 % hybrides, 50 % légères."},
   "clavier": {"aides": ["une seule bande", "deux bandes", "hybride", "On en déduit que"], "pieges": ["trois bandes"]},
   "correction": {"lignes": [{"texte": f"2 : G0 : {fr(H2)} → lourdes", "mot": "lourdes"},
                             {"texte": f"G1 : {fr(HY2)} → hybrides", "mot": "hybrides"},
                             {"texte": f"G2 : {fr(HY2)} + {fr(L2)} → 50 % / 50 %", "mot": "cinquante pour cent"}],
                  "parole": "ف la génération zéro، une seule bande lourde: les molécules lourdes. ف la génération un، une seule bande à un virgule sept cent neuf: toutes hybrides. ف la génération deux، deux bandes égales: cinquante pour cent hybrides، et cinquante pour cent légères."}},
  {"id": "3", "texte": "Indiquer le résultat que prévoit l'hypothèse conservative à la génération G1, puis montrer que le résultat obtenu en G1 permet de la rejeter.",
   "reponse": {"type": "phrase", "attendu": f"Conservative : une molécule mère entière (lourde) et une molécule fille entièrement nouvelle (légère) : deux bandes en G1, à {fr(H2)} et à {fr(L2)}. Or on obtient une seule bande à {fr(HY2)} : hypothèse rejetée."},
   "clavier": {"aides": ["deux bandes", "Or", "rejetée"], "pieges": ["une bande hybride"]},
   "correction": {"lignes": [{"texte": f"3 : conservative → deux bandes ({fr(H2)} et {fr(L2)}) en G1", "mot": "deux bandes"},
                             {"texte": f"or : une bande à {fr(HY2)} → rejetée", "mot": "مرفوضة"}],
                  "parole": "la conservative كانت غادي تعطي deux bandes، une lourde et une légère. ولكن كاينة une seule bande hybride: إذن مرفوضة."}},
  {"id": "4", "texte": "Expliquer pourquoi le résultat de G1 ne permet pas de choisir entre les hypothèses semi-conservative et dispersive, puis montrer que le résultat de G2 permet de trancher.",
   "reponse": {"type": "phrase", "attendu": f"En G1, les deux prévoient une seule bande hybride à {fr(HY2)}. En G2, semi-conservative : deux bandes égales ({fr(HY2)} et {fr(L2)}) ; dispersive : une seule bande entre {fr(L2)} et {fr(HY2)}. Deux bandes observées : la dispersive est rejetée, la réplication est semi-conservative."},
   "clavier": {"aides": ["même prévision en G1", "deux bandes", "semi-conservative"], "pieges": ["conservative"]},
   "correction": {"lignes": [{"texte": "4 : G1 : même prévision (une bande hybride)", "mot": "une seule bande hybride"},
                             {"texte": "G2 : deux bandes observées → dispersive rejetée, semi-conservative", "mot": "la semi-conservative"}],
                  "parole": "ف la génération un، les deux hypothèses كيعطيو une seule bande hybride. ف la génération deux، deux bandes: la dispersive مرفوضة، والجواب la semi-conservative."}},
  {"id": "5", "texte": "Les bactéries sont laissées sur ¹⁴N jusqu'à la génération G3. En vous appuyant sur l'hypothèse retenue, calculer le pourcentage de molécules hybrides attendu en G3.",
   "reponse": {"type": "valeur", "grandeur": "p", "valeur": P3, "unite": "%", "tolerance": 0.02,
               "attendu": "G3 : 2³ = 8 molécules, dont 2 hybrides ; p = 2/8 × 100 = 25 %"},
   "clavier": {"aides": ["2³ = 8", "2 hybrides", "× 100"], "pieges": ["2/6 × 100", "50 %"]},
   "correction": {"lignes": [{"texte": "5 : G3 : 2³ = 8 molécules, dont 2 hybrides", "mot": "huit molécules"},
                             {"texte": "p = 2/8 × 100 = 25 %", "mot": "vingt-cinq pour cent"}],
                  "parole": "en G trois: huit molécules، et toujours deux hybrides. deux sur huit، fois cent، égale vingt-cinq pour cent."}},
]
assert P3 == 25

EX = {
  "id": "svt_ex_ch3_meselson_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "notion_information_genetique", "cours": "svt_ch3_notion_information_genetique",
  "titre": "Azote lourd, azote léger : tester les hypothèses de la réplication", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Calculer la densité d'un ADN hybride", "Décrire des résultats de centrifugation puis déduire",
                  "Confronter une hypothèse à ses prévisions", "Prévoir les proportions d'une génération suivante"],
  "enonce": {
    "intro": "Pour savoir comment l'ADN se réplique, on cultive des bactéries pendant de nombreuses générations dans un milieu dont la seule source d'azote est l'azote lourd ¹⁵N : leur ADN devient lourd (génération G0). On les transfère ensuite dans un milieu à azote léger ¹⁴N, où elles se divisent une fois par génération. À chaque génération, on extrait l'ADN et on le centrifuge : chaque molécule se place selon sa densité. Deux témoins sont centrifugés en même temps : un ADN léger (deux brins à ¹⁴N) et un ADN lourd (deux brins à ¹⁵N). Trois hypothèses sont proposées : conservative (la molécule mère reste entière, la molécule fille est entièrement nouvelle), semi-conservative (chaque molécule fille garde un brin de la molécule mère), dispersive (ancien et nouveau mélangés dans chaque brin).",
    "intro_dit": "دابا نقراو l'énoncé. ربينا des bactéries بزاف ديال les générations ف milieu فيه غير l'azote lourd، l'azote quinze: l'A D N ديالهم ولا lourd، هادي la génération zéro. من بعد، نقلناهم ل milieu فيه l'azote léger، l'azote quatorze، وكل génération كيتقسمو مرة. ف كل génération، كنخرجو l'A D N، وكنديرو la centrifugation: كل molécule كتوقف حسب la densité ديالها. ومعاهم deux témoins: A D N léger، و A D N lourd. وكاينين trois hypothèses: conservative، semi-conservative، et dispersive. le document كيبين les bandes ف كل tube.",
    "figures": [figure_tubes(L, H, "Document : centrifugation de l'ADN extrait")],
    "donnees": [f"Témoin léger (¹⁴N/¹⁴N) : {fr(L)} g·cm⁻³", f"Témoin lourd (¹⁵N/¹⁵N) : {fr(H)} g·cm⁻³",
                "Une génération = une réplication de l'ADN suivie d'une division de chaque bactérie"],
    "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPLICATION}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FACILE}]},
  "similaire": {"id": "svt_ex_ch3_meselson_1_b", "titre": "Même exercice, autres données", "enonce": {
    "intro": "Même expérience avec une autre espèce de bactérie, dont l'ADN a une autre densité : cultures sur ¹⁵N (G0), transfert sur ¹⁴N, centrifugation de l'ADN à chaque génération, avec deux témoins (ADN léger et ADN lourd de cette espèce).",
    "intro_dit": "نفس التجربة، ب نوع آخر ديال les bactéries، ول l'A D N ديالو densité أخرى: l'azote quinze، من بعد l'azote quatorze، و la centrifugation ف كل génération، مع deux témoins.",
    "figures": [figure_tubes(L2, H2, "Document : centrifugation de l'ADN extrait (autre espèce)")],
    "donnees": [f"Témoin léger : {fr(L2)} g·cm⁻³", f"Témoin lourd : {fr(H2)} g·cm⁻³", "Une génération = une réplication suivie d'une division"],
    "questions": SIM_Q}},
}

if __name__ == "__main__":
    ecrire(EX, sys.argv[1])
