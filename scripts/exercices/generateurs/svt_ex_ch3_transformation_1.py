# Exercice SVT ch. 3 (Notion de l'information génétique) — transformation bactérienne en boîtes de culture, niveau moyen.
# Entraîne : décrire puis déduire (lots témoins → principe transformant), raisonner enzyme par enzyme (« on suppose que…,
# l'enzyme détruit…, or…, donc… »), conclure sur la nature chimique du principe transformant (ADN purifié), expliquer la
# transformation pas à pas (fragment d'ADN, intégration, capsule) et son caractère héréditaire → l'ADN, support de
# l'information génétique (capacité NIG6 du cadre).
# Sources comparées :
# - exploration notion_information_genetique.json : cas_type « nature_chimique » (résultat de chaque lot, principe
#   transformant, pour chaque enzyme : on suppose que…, l'enzyme détruit…, or…, donc… ; conclusion : l'ADN) ; piège
#   « lit la souris meurt comme un échec d'Avery » (ici : des colonies S = des R transformés = principe non détruit).
# - vidéos (exploration) : Maison Des Sciences (Griffith 4 expériences, Avery 3 enzymes, Avery par hypothèse réfutée).
# - nationaux PC 2016-2025 : aucune question Griffith / Avery (documents des contrôles et des manuels).
# - séries en ligne : recherche faite (séries marocaines dreamjob.ma, moutamadris.ma) mais pages non lisibles depuis la
#   session (hôtes non résolus) ; comparé avec les vidéos de l'exploration.
# - cours svt_ch3 : ig_t1 à ig_t3 (souris ; ici la même logique en boîtes de culture, les colonies étant définies dans
#   l'énoncé) ; hors cadre évité : bactériophage, Hershey et Chase, gène (chapitre suivant).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

BASE = "/media/simulations/svt/notion_information_genetique-tableau/"
GRIF = BASE + "bacteries.html?vue=griffith"
AVERY0 = BASE + "bacteries.html?vue=avery&resultats=0"
AVERY = BASE + "bacteries.html?vue=avery"
PREUVE = BASE + "extraction.html?vue=preuve"


def tableau(lots, titre):
    """Tableau des lots dessiné (rect + texte) : lot, contenu de la boîte, colonies R, colonies S."""
    n = len(lots); h = 8 + 7 * (n + 1)
    xs = [0, 6, 72, 86, 100]
    el = [{"f": "rect", "de": [0, 0], "a": [100, h], "couleur": "blanc"}]
    for x in xs[1:-1]:
        el.append({"f": "ligne", "pts": [[x, 0], [x, h]], "couleur": "faible"})
    ytete = h - 5
    for i, t in enumerate(["Lot", "Contenu de la boîte", "col. R", "col. S"]):
        el.append({"f": "texte", "at": [(xs[i] + xs[i + 1]) / 2, ytete - 1], "t": t, "taille": "petit", "ancre": "centre", "couleur": "cyan"})
    el.append({"f": "ligne", "pts": [[0, h - 9], [100, h - 9]], "couleur": "blanc"})
    for j, (num, contenu, r, s) in enumerate(lots):
        y = h - 9 - 7 * (j + 1) + 2
        for i, t in enumerate([str(num), contenu, str(r), str(s)]):
            el.append({"f": "texte", "at": [(xs[i] + xs[i + 1]) / 2 if i != 1 else xs[1] + 1.5, y], "t": t, "taille": "petit",
                       "ancre": "centre" if i != 1 else "gauche", "couleur": "jaune" if i == 3 and s else "blanc"})
        if j < n - 1:
            el.append({"f": "ligne", "pts": [[0, y - 2.5], [100, y - 2.5]], "couleur": "faible", "trait": "pointille"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 100, "h": h},
            "legende": "Nombre de colonies comptées après 48 h à 37 °C. Colonie R : aspect rugueux (bactéries sans capsule) ; colonie S : aspect lisse (bactéries à capsule).",
            "elements": el}


def figure_repiquage():
    """Document 2 : une colonie S du lot 3 repiquée trois fois de suite → toujours des colonies S."""
    el = []
    for i, x in enumerate([14, 42, 70]):
        el.append({"f": "ellipse", "c": [x, 16], "rx": 10, "ry": 7, "couleur": "blanc"})
        for dx, dy in [(-4, 1), (2, 3), (4, -2), (-1, -3), (-5, -2)]:
            el.append({"f": "cercle", "c": [x + dx, 16 + dy], "r": 1.1, "couleur": "jaune", "remplir": "jaune"})
        el.append({"f": "texte", "at": [x, 5], "t": f"repiquage {i + 1}", "taille": "petit", "ancre": "centre"})
        if i < 2:
            el.append({"f": "fleche", "de": [x + 11, 16], "a": [x + 17, 16], "couleur": "faible"})
    el.append({"f": "fleche", "de": [2, 30], "a": [6, 22], "couleur": "faible"})
    el.append({"f": "texte", "at": [1, 32], "t": "une colonie S du lot 3", "taille": "petit", "ancre": "gauche", "couleur": "cyan"})
    el.append({"f": "texte", "at": [92, 16], "t": "toutes les", "taille": "petit", "ancre": "centre", "couleur": "jaune"})
    el.append({"f": "texte", "at": [92, 12], "t": "colonies : S", "taille": "petit", "ancre": "centre", "couleur": "jaune"})
    return {"type": "schema", "titre": "Document 2 : repiquages successifs d'une colonie S du lot 3", "cadre": {"l": 100, "h": 36},
            "legende": "Chaque repiquage se fait sur un milieu neuf, sans extrait : on n'obtient que des colonies S, de génération en génération.",
            "elements": el}


LOTS = [(1, "R vivantes seules", 210, 0),
        (2, "extrait de S tués, seul", 0, 0),
        (3, "R + extrait de S tués", 196, 14),
        (4, "R + extrait + protéase", 205, 12),
        (5, "R + extrait + ribonucléase", 199, 15),
        (6, "R + extrait + désoxyribonucléase", 208, 0),
        (7, "R + ADN purifié des S tués", 201, 13)]

Q = [
  {"id": "1", "texte": "Décrire les résultats des lots 1, 2 et 3, puis déduire ce qui s'est passé dans le lot 3.",
   "texte_dit": "السؤال un: وصف les résultats ديال le lot un، le lot deux، et le lot trois، ومن بعد استنتج شنو وقع ف le lot trois.",
   "reponse": {"type": "phrase", "attendu": "Lot 1 : les bactéries R seules donnent 210 colonies R et aucune colonie S : les R ne deviennent pas S toutes seules. Lot 2 : l'extrait de S tués seul ne donne aucune colonie : il ne contient aucune bactérie vivante. Lot 3 : R vivantes + extrait de S tués donnent 196 colonies R et 14 colonies S. On en déduit qu'une substance de l'extrait des S tués a transformé une partie des bactéries R en bactéries S : c'est le principe transformant."},
   "clavier": {"aides": ["aucune colonie", "colonies S", "transformées", "principe transformant", "On en déduit que"], "pieges": ["les S tués revivent", "toutes les R"]},
   "aides": [
     {"texte": "Regarde la colonne « colonies S » : dans quel lot apparaissent-elles ? Et que montrent les lots 1 et 2 seuls ?",
      "dit": "شوف la colonne ديال les colonies S: ف أشمن lot كيبانو؟ وشنو كيبينو le lot un و le lot deux بوحدهم؟"},
     {"texte": "Le lot 2 montre que l'extrait ne contient plus de S vivantes. Les colonies S du lot 3 viennent donc forcément… de quelles bactéries ?",
      "dit": "le lot deux كيبين بلي l'extrait ما فيهش S vivantes. إذن les colonies S ديال le lot trois، منين جاو؟ من أشمن bactéries؟"}],
   "correction": {"lignes": [
       {"texte": "1 : lot 1 : R seules → 210 colonies R, aucune S", "mot": "les R بوحدهم ما كيوليوش S"},
       {"texte": "lot 2 : extrait seul → aucune colonie : pas de S vivantes", "mot": "ما فيهش حتى bactérie vivante"},
       {"texte": "lot 3 : 196 R et 14 S → des R ont été transformées en S par une substance de l'extrait : le principe transformant", "mot": "le principe transformant"}],
     "parole": "السؤال un. le lot un: deux cent dix colonies R، et aucune colonie S: les R بوحدهم ما كيوليوش S. le lot deux: aucune colonie: l'extrait ما فيهش حتى bactérie vivante. le lot trois: cent quatre-vingt-seize colonies R، et quatorze colonies S. on en déduit: شي حاجة ف l'extrait ديال S tués، بدلات شي R ل S. هادي هي le principe transformant."},
   "explication": "ex_s1", "facile": "fa_s1"},
  {"id": "2", "texte": "Pour chacun des lots 4, 5 et 6, formuler l'hypothèse testée sur la nature du principe transformant, puis l'exploiter.",
   "texte_dit": "السؤال deux: ف كل lot، le lot quatre، le lot cinq، et le lot six، قول شمن hypothèse كنجربو على le principe transformant، ومن بعد استغل le résultat.",
   "reponse": {"type": "phrase", "attendu": "Lot 4 : on suppose que le principe transformant est une protéine ; la protéase détruit les protéines de l'extrait ; or on obtient 12 colonies S : la transformation a eu lieu, donc le principe transformant n'est pas une protéine. Lot 5 : on suppose que c'est l'ARN ; la ribonucléase détruit l'ARN ; or on obtient 15 colonies S, donc ce n'est pas l'ARN. Lot 6 : on suppose que c'est l'ADN ; la désoxyribonucléase détruit l'ADN ; on n'obtient aucune colonie S : sans ADN, pas de transformation, donc le principe transformant est l'ADN."},
   "clavier": {"aides": ["on suppose que", "détruit", "or", "donc", "protéine", "ARN", "ADN"], "pieges": ["la protéase détruit l'ADN", "la ribonucléase détruit les protéines"]},
   "aides": [
     {"texte": "Chaque enzyme détruit une seule sorte de molécule de l'extrait : laquelle pour chaque lot ? Puis regarde s'il reste des colonies S.",
      "dit": "كل enzyme كتحيد نوع واحد ديال les molécules ف l'extrait. شمن نوع ف كل lot؟ ومن بعد شوف: واش بقاو les colonies S؟"},
     {"texte": "Rédige pour chaque lot : « on suppose que… ; l'enzyme détruit… ; or… ; donc… ». Des colonies S = des R transformées = le principe n'a pas été détruit.",
      "dit": "كتب ف كل lot: on suppose que، l'enzyme détruit، or، donc. يلا كاينين des colonies S، يعني la transformation وقعات، و le principe ما تحيدش."}],
   "correction": {"lignes": [
       {"texte": "2 : lot 4 : protéines détruites, or 12 colonies S → pas une protéine", "mot": "ماشي protéine"},
       {"texte": "lot 5 : ARN détruit, or 15 colonies S → pas l'ARN", "mot": "ماشي l'A R N"},
       {"texte": "lot 6 : ADN détruit → aucune colonie S → le principe transformant est l'ADN", "mot": "le principe transformant هو l'A D N"}],
     "parole": "السؤال deux. le lot quatre: on suppose que le principe transformant est une protéine. la protéase كتحيد les protéines، or، on obtient douze colonies S: إذن ماشي protéine. le lot cinq: la ribonucléase كتحيد l'A R N، or، on obtient quinze colonies S: إذن ماشي l'A R N. le lot six: la désoxyribonucléase كتحيد l'A D N، و aucune colonie S: بلا A D N، ما كايناش la transformation. إذن le principe transformant هو l'A D N."},
   "explication": "ex_s2", "facile": "fa_s2"},
  {"id": "3", "texte": "Que montre le résultat du lot 7 ? Conclure sur la nature chimique du principe transformant.",
   "texte_dit": "السؤال trois: شنو كيبين le résultat ديال le lot sept؟ واستنتج la nature chimique ديال le principe transformant.",
   "reponse": {"type": "phrase", "attendu": "Dans le lot 7, l'ADN purifié des S, seul, sans protéines ni ARN, suffit à transformer des R en S (13 colonies S). Cela confirme le lot 6 : le principe transformant est l'ADN."},
   "clavier": {"aides": ["ADN purifié", "suffit", "13 colonies S", "confirme", "le principe transformant est l'ADN"], "pieges": ["les protéines", "l'ARN"]},
   "aides": [
     {"texte": "Dans le lot 7, que reste-t-il de l'extrait des S ? Y a-t-il encore des protéines ou de l'ARN ?",
      "dit": "ف le lot sept، شنو بقا من l'extrait ديال S؟ واش مازال فيه les protéines ولا l'A R N؟"},
     {"texte": "Si l'ADN seul donne des colonies S, il suffit à la transformation : relie au lot 6, où l'ADN détruit empêchait la transformation.",
      "dit": "يلا l'A D N بوحدو عطا des colonies S، إذن هو بوحدو كافي. ربط مع le lot six، فين ملي تحيد l'A D N ما وقعاتش la transformation."}],
   "correction": {"lignes": [
       {"texte": "3 : lot 7 : l'ADN purifié seul → 13 colonies S", "mot": "l'A D N بوحدو"},
       {"texte": "l'ADN suffit à transformer R en S (confirme le lot 6)", "mot": "كافي باش يبدل R ل S"},
       {"texte": "le principe transformant est l'ADN", "mot": "le principe transformant، c'est l'A D N"}],
     "parole": "السؤال trois. ف le lot sept، l'A D N بوحدو، بلا protéines وبلا A R N، كانت la transformation، avec treize colonies S. إذن l'A D N كافي باش يبدل R ل S، وهادا كيأكد le lot six. la conclusion: le principe transformant، c'est l'A D N."},
   "explication": "ex_s3", "facile": "fa_s3"},
  {"id": "4", "texte": "Expliquer, en étapes successives, comment une bactérie R du lot 3 est devenue une bactérie S.",
   "texte_dit": "السؤال quatre: فسر خطوة ب خطوة، كيفاش bactérie R ف le lot trois ولات bactérie S.",
   "reponse": {"type": "phrase", "attendu": "1) La chaleur tue les S, leur ADN se coupe en fragments. 2) Un fragment d'ADN des S entre dans une bactérie R. 3) Il s'intègre à l'ADN de la bactérie R (intégration). 4) La bactérie R fabrique alors une capsule : elle est devenue S. 5) En se divisant, elle donne une colonie de bactéries S."},
   "clavier": {"aides": ["fragment d'ADN", "entre dans la bactérie R", "intégration", "capsule", "se divise"], "pieges": ["la bactérie S revit", "une protéine entre"]},
   "aides": [
     {"texte": "Pars de l'extrait : qu'a fait la chaleur à l'ADN des S ? Que reçoit la bactérie R ?",
      "dit": "بدا من l'extrait: شنو دارت الحرارة ل l'A D N ديال S؟ وشنو كيدخل ل la bactérie R؟"},
     {"texte": "Les étapes : fragment d'ADN → entrée dans R → intégration à son ADN → capsule → divisions (colonie S).",
      "dit": "les étapes: le fragment d'A D N، كيدخل ف R، كيتلصق ف l'A D N ديالها، كتصاوب capsule، ومن بعد كتقسم وكتعطي colonie S."}],
   "correction": {"lignes": [
       {"texte": "4 : la chaleur tue les S : leur ADN se coupe en fragments", "mot": "كيتقطع، كيولي des fragments"},
       {"texte": "un fragment d'ADN des S entre dans une R et s'intègre à son ADN", "mot": "l'intégration"},
       {"texte": "la R fabrique une capsule : elle devient S ; ses divisions donnent une colonie S", "mot": "colonie S"}],
     "parole": "السؤال quatre. الحرارة كتقتل S، و l'A D N ديالهم كيتقطع، كيولي des fragments. fragment ديال l'A D N ديال S كيدخل ف bactérie R، وكيتلصق ف l'A D N ديالها: نقولو l'intégration. la bactérie R كتصاوب capsule: ولات S. وملي كتقسم، كتعطي colonie S."},
   "explication": "ex_s4", "facile": "fa_s4"},
  {"id": "5", "texte": "En exploitant le document 2, montrer que l'ADN est le support de l'information génétique.",
   "texte_dit": "السؤال cinq: ب le document deux، بين بلي l'A D N هو le support ديال l'information génétique.",
   "reponse": {"type": "phrase", "attendu": "Les colonies S repiquées sur un milieu neuf, sans extrait, ne donnent que des colonies S, génération après génération : le caractère « capsule » acquis par la transformation est héréditaire, il est transmis aux bactéries filles. Or ce caractère a été apporté par l'ADN des S. L'ADN porte donc une information héréditaire, transmise d'une génération à l'autre : l'ADN est le support (chimique) de l'information génétique."},
   "clavier": {"aides": ["héréditaire", "transmis", "bactéries filles", "capsule", "support de l'information génétique"], "pieges": ["l'extrait est ajouté à chaque repiquage", "les protéines"]},
   "aides": [
     {"texte": "Au repiquage, on n'ajoute plus d'extrait. Les descendants restent-ils S ? Le caractère « capsule » est-il transmis ?",
      "dit": "ف le repiquage، ما بقيناش كنزيدو l'extrait. واش les bactéries filles كيبقاو S؟ واش la capsule كتورث؟"},
     {"texte": "Une information génétique : elle détermine un caractère et se transmet d'une cellule à ses cellules filles. Qui a apporté ce caractère ?",
      "dit": "l'information génétique كتحدد واحد الصفة، وكتنتقل من la cellule ل les cellules filles. وشكون اللي جاب هاد الصفة؟"}],
   "correction": {"lignes": [
       {"texte": "5 : sans extrait, les repiquages ne donnent que des colonies S : le caractère est héréditaire", "mot": "الصفة كتورث"},
       {"texte": "or ce caractère a été apporté par l'ADN des S", "mot": "جابها l'A D N"},
       {"texte": "l'ADN est le support de l'information génétique", "mot": "est le support chimique، de l'information génétique"}],
     "parole": "السؤال cinq. بلا extrait، les repiquages كيعطيو غير des colonies S، génération après génération: الصفة كتورث، كتنتقل ل les bactéries filles. وهاد الصفة جابها l'A D N ديال S. نعاود نقرا: l'A D N، est le support chimique، de l'information génétique."},
   "explication": "ex_s5", "facile": "fa_s5"},
]

EXPLICATION = [
  {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : des R deviennent S grâce à l'extrait de S tués",
   "screen_content": {"lead": "R seules : pas de S. Extrait seul : rien de vivant. Les deux ensemble : des S apparaissent."},
   "visual": {"kind": "simulation", "url": GRIF, "caption": "La même logique chez Griffith, avec des souris"},
   "speech_text": {"mixed": "هاد الفكرة شفناها مع Griffith، ب les souris. la forme S عندها capsule، و la forme R بلا capsule. les S tués par la chaleur بوحدهم، ما كيعطيو والو: ما بقاوش عايشين. ولكن R vivants مع S tués: كيبانو S vivants. فالتمرين، نفس الشي ف les boîtes de culture: le lot un، R بوحدهم، ما كاين حتى S. le lot deux، l'extrait بوحدو، aucune colonie. le lot trois، les deux ensemble: quatorze colonies S. إذن شي حاجة ف l'extrait، بدلات شي R ل S: le principe transformant."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "lot 1 : R seules → aucune S ; lot 2 : extrait seul → rien", "mot": "aucune colonie"},
                {"texte": "lot 3 : 14 colonies S → R transformées", "mot": "quatorze colonies S"},
                {"texte": "une substance de l'extrait : le principe transformant", "mot": "le principe transformant"}],
     "pointage": [{"mot": "la forme S عندها capsule", "commande": "play_until", "parametres": {"moment": "formes"}},
                  {"mot": "la forme S عندها capsule", "repere": "bacterie_s"},
                  {"mot": "و la forme R بلا capsule", "repere": "bacterie_r"},
                  {"mot": "les S tués par la chaleur", "commande": "play_until", "parametres": {"moment": "s_tues"}},
                  {"mot": "ولكن R vivants مع S tués", "commande": "play_until", "parametres": {"moment": "melange"}},
                  {"mot": "كيبانو S vivants", "commande": "play_until", "parametres": {"moment": "s_dans_le_sang"}},
                  {"mot": "كيبانو S vivants", "repere": "sang"},
                  {"mot": "aucune colonie", "cible": "centre:0"},
                  {"mot": "quatorze colonies S", "cible": "centre:1"},
                  {"mot": "le principe transformant", "cible": "centre:2"}]}},
  {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : une enzyme, une molécule détruite, un verdict",
   "screen_content": {"lead": "Protéase : S encore là → pas une protéine. Ribonucléase : pas l'ARN. Désoxyribonucléase : plus de S → l'ADN."},
   "visual": {"kind": "simulation", "url": AVERY0, "caption": "Avery : trois tubes, trois enzymes"},
   "speech_text": {"mixed": "كل tube فيه enzyme، وكل enzyme كتحيد نوع واحد. tube اللول، la protéase، كتحيد les protéines: la transformation وقعات. إذن le principe ماشي protéine. tube الثاني، la ribonucléase، كتحيد l'A R N: la transformation وقعات حتى هي. إذن ماشي l'A R N. tube الثالث، la désoxyribonucléase، كتحيد l'A D N: ما كايناش la transformation. ف التمرين: le lot six، aucune colonie S. إذن le principe transformant هو l'A D N."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "on suppose que… ; l'enzyme détruit… ; or… ; donc…", "mot": "كل enzyme كتحيد نوع واحد"},
                {"texte": "protéase, ribonucléase : des S → ni protéine, ni ARN", "mot": "إذن ماشي l'A R N"},
                {"texte": "désoxyribonucléase : aucune S → l'ADN", "mot": "إذن le principe transformant هو l'A D N"}],
     "pointage": [{"mot": "كل tube فيه enzyme", "commande": "set_time", "parametres": {"time_s": 12.2}},
                  {"mot": "كل enzyme كتحيد نوع واحد", "cible": "centre:0"},
                  {"mot": "tube اللول، la protéase", "commande": "set_parameters", "parametres": {"tube": 1, "resultats": 1}},
                  {"mot": "tube اللول، la protéase", "repere": "tube_1"},
                  {"mot": "la transformation وقعات. إذن", "repere": "souris_1"},
                  {"mot": "tube الثاني، la ribonucléase", "commande": "set_parameters", "parametres": {"tube": 2, "resultats": 2}},
                  {"mot": "tube الثاني، la ribonucléase", "repere": "tube_2"},
                  {"mot": "إذن ماشي l'A R N", "cible": "centre:1"},
                  {"mot": "tube الثالث، la désoxyribonucléase", "commande": "set_parameters", "parametres": {"tube": 3, "resultats": 3}},
                  {"mot": "ما كايناش la transformation", "repere": "souris_3"},
                  {"mot": "إذن le principe transformant هو l'A D N", "cible": "centre:2"}]}},
  {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : l'ADN seul suffit",
   "screen_content": {"lead": "L'ADN purifié, sans protéines ni ARN, transforme des R en S : le principe transformant est l'ADN."},
   "visual": {"kind": "simulation", "url": AVERY, "caption": "Un fragment d'ADN des S entre dans une bactérie R"},
   "speech_text": {"mixed": "ف le lot sept، ما بقا ف l'extrait غير l'A D N: بلا protéines، وبلا A R N. وكانت la transformation، avec treize colonies S. شوف: fragment ديال l'A D N ديال S كيدخل ف la bactérie R، وهي كتولي S. إذن l'A D N بوحدو كافي. وهادا كيأكد le lot six: ملي كنحيدو l'A D N، ما كايناش la transformation. la conclusion: le principe transformant، c'est l'A D N."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "lot 7 : ADN seul → 13 colonies S", "mot": "treize colonies S"},
                {"texte": "lots 6 et 7 : le principe transformant est l'ADN", "mot": "le principe transformant، c'est l'A D N"}],
     "pointage": [{"mot": "ف le lot sept", "commande": "set_time", "parametres": {"time_s": 12.2}},
                  {"mot": "treize colonies S", "cible": "centre:0"},
                  {"mot": "شوف: fragment", "commande": "play_until", "parametres": {"moment": "fragment_adn_entre"}},
                  {"mot": "شوف: fragment", "repere": "fragment_adn"},
                  {"mot": "وهي كتولي S", "commande": "play_until", "parametres": {"moment": "capsule"}},
                  {"mot": "la conclusion: le principe", "commande": "play_until", "parametres": {"moment": "conclusion"}},
                  {"mot": "le principe transformant، c'est l'A D N", "repere": "conclusion"},
                  {"mot": "le principe transformant، c'est l'A D N", "cible": "centre:1"}]}},
  {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : de R à S, étape par étape",
   "screen_content": {"lead": "Fragments d'ADN des S → entrée dans R → intégration → capsule → colonie S."},
   "visual": {"kind": "simulation", "url": AVERY, "caption": "La bactérie R reçoit un fragment d'ADN et fabrique une capsule"},
   "speech_text": {"mixed": "خطوة ب خطوة. واحد: الحرارة كتقتل S، و l'A D N ديالهم كيتقطع، كيولي des fragments. جوج: fragment ديال l'A D N ديال S كيدخل ف la bactérie R. تلاتة: كيتلصق ف l'A D N ديال R، وكيولي جزء منو: l'intégration. ربعة: la bactérie R كتصاوب capsule، يعني ولات S. خمسة: ملي كتقسم، كتعطي colonie، كاملة ديال S."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "1. ADN des S en fragments", "mot": "كيولي des fragments"},
                {"texte": "2. un fragment entre dans R ; 3. intégration", "mot": "l'intégration"},
                {"texte": "4. capsule : R devient S ; 5. divisions → colonie S", "mot": "كتعطي colonie"}],
     "pointage": [{"mot": "خطوة ب خطوة", "commande": "set_time", "parametres": {"time_s": 12.2}},
                  {"mot": "كيولي des fragments", "cible": "centre:0"},
                  {"mot": "جوج: fragment", "commande": "play_until", "parametres": {"moment": "fragment_adn_entre"}},
                  {"mot": "جوج: fragment", "repere": "fragment_adn"},
                  {"mot": "l'intégration", "repere": "bacterie_r"},
                  {"mot": "l'intégration", "cible": "centre:1"},
                  {"mot": "ربعة: la bactérie R كتصاوب capsule", "commande": "play_until", "parametres": {"moment": "capsule"}},
                  {"mot": "ربعة: la bactérie R كتصاوب capsule", "repere": "capsule"},
                  {"mot": "كتعطي colonie", "cible": "centre:2"}]}},
  {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : un caractère transmis, une information portée par l'ADN",
   "screen_content": {"lead": "Le caractère « capsule » se transmet aux bactéries filles : l'ADN porte l'information génétique."},
   "visual": {"kind": "simulation", "url": PREUVE, "caption": "L'ADN, dans les chromosomes de nos cellules aussi"},
   "speech_text": {"mixed": "ف le document deux، ما زدناش l'extrait. ومع ذلك، les bactéries filles كيبقاو S، génération après génération: la capsule كتورث. وهاد الصفة جابها l'A D N ديال S. إذن l'A D N فيه information كتنتقل من خلية ل les cellules filles: هادي هي l'information génétique. وعند الخلايا ديالنا حتى هي، l'A D N كاين ف les chromosomes: شوف le réactif de Feulgen، ما كيلون غير l'A D N، و les chromosomes كيوليو حمرين. نعاود نقرا: l'A D N، est le support chimique، de l'information génétique."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "sans extrait : toujours des colonies S → caractère héréditaire", "mot": "la capsule كتورث"},
                {"texte": "apporté par l'ADN des S", "mot": "جابها l'A D N"},
                {"texte": "l'ADN est le support chimique de l'information génétique", "mot": "est le support chimique، de l'information génétique"}],
     "pointage": [{"mot": "la capsule كتورث", "cible": "centre:0"},
                  {"mot": "جابها l'A D N", "cible": "centre:1"},
                  {"mot": "شوف le réactif de Feulgen", "commande": "play_until", "parametres": {"moment": "feulgen"}},
                  {"mot": "و les chromosomes كيوليو حمرين", "commande": "play_until", "parametres": {"moment": "rouge"}},
                  {"mot": "و les chromosomes كيوليو حمرين", "repere": "chromosomes_rouges"},
                  {"mot": "نعاود نقرا", "commande": "play_until", "parametres": {"moment": "donc_adn"}},
                  {"mot": "est le support chimique، de l'information génétique", "cible": "centre:2"}]}},
]

FACILE = [
  qcm_facile("fa_s1", "Plus facile : d'où viennent les colonies S du lot 3 ?", "سؤال ساهل: منين جاو les colonies S ف le lot trois؟",
    "Dans le lot 3, les colonies S viennent…",
    ["de bactéries S tuées qui ont repris vie", "de bactéries R transformées en S", "de bactéries S restées vivantes dans l'extrait"], 1, {
      "1": {"juste": rep("برافو! شي R تبدلو ل S ب شي حاجة ف l'extrait: le principe transformant.", "Juste : des R ont été transformées en S par le principe transformant.")},
      "0": {"1": rep("لا، bactérie ميتة ما كترجعش عايشة. شوف le lot deux: l'extrait بوحدو شنو عطا؟ عاود اختار.", "Une bactérie tuée ne revit pas. Regarde le lot 2 : l'extrait seul donne-t-il des colonies ? Réessaie."),
            "2": rep("الجواب: des R transformées en S. les S tués ما كيرجعوش عايشين.", "Réponse : des R transformées en S ; les S tuées ne revivent pas.")},
      "2": {"1": rep("قريب، ولكن le lot deux كيبين: l'extrait بوحدو، aucune colonie. إذن ما فيهش S عايشين. عاود اختار.", "Le lot 2 montre que l'extrait seul ne donne aucune colonie : il n'y a pas de S vivantes. Réessaie."),
            "2": rep("الجواب: des R transformées en S. l'extrait ما فيهش حتى bactérie vivante.", "Réponse : des R transformées en S ; l'extrait ne contient aucune bactérie vivante.")}},
    "Dans le lot trois, d'où viennent les colonies S ?"),
  association("fa_s2", "Plus facile : chaque enzyme et ce qu'elle détruit", "Relie chaque enzyme à la molécule qu'elle détruit.",
    "سؤال ساهل: ربط كل enzyme مع la molécule اللي كتحيد.",
    "Relie chaque enzyme à la molécule qu'elle détruit.",
    [("1", "protéase"), ("2", "ribonucléase"), ("3", "désoxyribonucléase")],
    [("a", "les protéines"), ("b", "l'ARN"), ("c", "l'ADN"), ("d", "la capsule des bactéries")],
    {"1": "a", "2": "b", "3": "c"},
    {"1-a": (True, "Oui : la protéase détruit les protéines.", "برافو: la protéase كتحيد les protéines."),
     "1-b": (False, "Non : l'ARN est détruit par la ribonucléase (ribo- : ARN).", "لا، l'A R N كتحيدو la ribonucléase."),
     "1-c": (False, "Non : l'ADN est détruit par la désoxyribonucléase (désoxyribo- : ADN).", "لا، l'A D N كتحيدو la désoxyribonucléase."),
     "1-d": (False, "Non : aucune enzyme de l'expérience ne vise la capsule ; la protéase vise les protéines.", "لا، la protéase كتحيد les protéines، ماشي la capsule."),
     "2-a": (False, "Non : les protéines sont détruites par la protéase.", "لا، les protéines كتحيدهم la protéase."),
     "2-b": (True, "Oui : la ribonucléase détruit l'ARN.", "برافو: la ribonucléase كتحيد l'A R N."),
     "2-c": (False, "Non : « désoxyribo » manque : la ribonucléase détruit l'ARN, pas l'ADN.", "لا، la ribonucléase كتحيد l'A R N، ماشي l'A D N."),
     "2-d": (False, "Non : la ribonucléase vise l'ARN.", "لا، la ribonucléase كتحيد l'A R N."),
     "3-a": (False, "Non : les protéines, c'est la protéase.", "لا، les protéines ديال la protéase."),
     "3-b": (False, "Non : désoxyribonucléase : elle détruit l'ADN (acide désoxyribonucléique).", "لا، la désoxyribonucléase كتحيد l'A D N."),
     "3-c": (True, "Oui : la désoxyribonucléase détruit l'ADN.", "برافو: la désoxyribonucléase كتحيد l'A D N."),
     "3-d": (False, "Non : la désoxyribonucléase vise l'ADN.", "لا، la désoxyribonucléase كتحيد l'A D N.")},
    ("(1 ; a) (2 ; b) (3 ; c) : la capsule (d) n'est visée par aucune enzyme.", "الجواب: un مع a، deux مع b، trois مع c. و la capsule ما عندها حتى enzyme.")),
  vrai_faux("fa_s3", "Plus facile : le lot 7", "Vrai ou faux : l'ADN purifié.",
    "سؤال ساهل: صحيح ولا غالط، على le lot sept.",
    [("Dans le lot 7, il n'y a ni protéines ni ARN des S.", True, "Oui : seul l'ADN purifié des S est ajouté."),
     ("Le lot 7 montre que l'ADN seul suffit à transformer des R en S.", True, "Oui : 13 colonies S apparaissent avec l'ADN seul."),
     ("Le lot 7 montre que le principe transformant est une protéine.", False, "Non : il n'y a pas de protéines des S dans le lot 7, et la transformation a lieu.")]),
  qcm_facile("fa_s4", "Plus facile : la première étape dans la bactérie R", "سؤال ساهل: شنو اللي كيدخل ف la bactérie R؟",
    "Pour qu'une bactérie R devienne S, ce qui entre dans la bactérie R est…",
    ["un fragment d'ADN des S", "la capsule des S", "une protéine des S"], 0, {
      "0": {"juste": rep("برافو! fragment ديال l'A D N ديال S كيدخل، وكيتلصق ف l'A D N ديال R.", "Juste : un fragment d'ADN des S entre et s'intègre à l'ADN de R.")},
      "1": {"1": rep("لا، la bactérie R كتصاوب la capsule ديالها بوحدها من بعد. شنو اللي جاب l'information ديال la capsule؟ عاود اختار.", "La bactérie R fabrique elle-même sa capsule ensuite. Qui a apporté l'information ? Réessaie."),
            "2": rep("الجواب: un fragment d'ADN des S. la capsule كتصاوبها R من بعد.", "Réponse : un fragment d'ADN des S ; la capsule est fabriquée ensuite par R.")},
      "2": {"1": rep("لا، le lot quatre كيبين: ملي كنحيدو les protéines، la transformation كتوقع. عاود اختار.", "Le lot 4 montre que sans protéines la transformation a lieu. Réessaie."),
            "2": rep("الجواب: un fragment d'ADN des S، ماشي protéine.", "Réponse : un fragment d'ADN des S, pas une protéine.")}},
    "Qu'est-ce qui entre dans la bactérie R ?"),
  qcm_facile("fa_s5", "Plus facile : que montrent les repiquages ?", "سؤال ساهل: شنو كيبينو les repiquages؟",
    "Sans extrait, les repiquages d'une colonie S ne donnent que des colonies S. Cela montre que…",
    ["l'extrait est encore nécessaire à chaque génération", "les bactéries S tuées se multiplient", "le caractère acquis est transmis aux bactéries filles"], 2, {
      "2": {"juste": rep("برافو! الصفة كتورث: l'information اللي جابها l'A D N كتنتقل ل les bactéries filles.", "Juste : le caractère est héréditaire, l'information apportée par l'ADN est transmise.")},
      "0": {"1": rep("لا، ف les repiquages ما زدناش l'extrait. ومع ذلك بقاو S. عاود اختار.", "On n'ajoute plus d'extrait aux repiquages, et pourtant elles restent S. Réessaie."),
            "2": rep("الجواب: le caractère est transmis aux bactéries filles، بلا extrait.", "Réponse : le caractère est transmis aux bactéries filles.")},
      "1": {"1": rep("لا، les S tués ما كيعيشوش. اللي كيتكاثرو هوما les R اللي ولاو S. عاود اختار.", "Les S tuées ne vivent plus ; ce sont les R devenues S qui se multiplient. Réessaie."),
            "2": rep("الجواب: le caractère est transmis aux bactéries filles.", "Réponse : le caractère acquis est transmis aux bactéries filles.")}},
    "Que montrent les repiquages ?"),
]

# ---- exercice semblable : autres comptages, enzymes dans un autre ordre (lot 4 désoxyribonucléase, 5 protéase, 6 ribonucléase)
LOTS_B = [(1, "R vivantes seules", 180, 0),
          (2, "extrait de S tués, seul", 0, 0),
          (3, "R + extrait de S tués", 172, 9),
          (4, "R + extrait + désoxyribonucléase", 178, 0),
          (5, "R + extrait + protéase", 175, 8),
          (6, "R + extrait + ribonucléase", 169, 10),
          (7, "R + ADN purifié des S tués", 170, 11)]
SIM_Q = [
  {"id": "1", "texte": "Décrire les résultats des lots 1, 2 et 3, puis déduire ce qui s'est passé dans le lot 3.",
   "reponse": {"type": "phrase", "attendu": "Lot 1 : 180 colonies R, aucune S. Lot 2 : aucune colonie (pas de bactérie vivante dans l'extrait). Lot 3 : 172 R et 9 S. On en déduit qu'une substance de l'extrait de S tués a transformé des R en S : le principe transformant."},
   "clavier": {"aides": ["aucune colonie", "transformées", "principe transformant"], "pieges": ["les S tués revivent"]},
   "correction": {"lignes": [{"texte": "1 : lot 1 : 180 R, aucune S ; lot 2 : aucune colonie", "mot": "aucune colonie"},
                             {"texte": "lot 3 : 9 S → des R transformées : le principe transformant", "mot": "le principe transformant"}],
                  "parole": "le lot un: aucune colonie S. le lot deux: aucune colonie. le lot trois: neuf colonies S. إذن شي R تبدلو ل S: le principe transformant."}},
  {"id": "2", "texte": "Pour chacun des lots 4, 5 et 6, formuler l'hypothèse testée sur la nature du principe transformant, puis l'exploiter.",
   "reponse": {"type": "phrase", "attendu": "Lot 4 : on suppose que c'est l'ADN ; la désoxyribonucléase le détruit ; aucune colonie S : sans ADN pas de transformation, c'est donc l'ADN. Lot 5 : protéines détruites, or 8 colonies S : ce n'est pas une protéine. Lot 6 : ARN détruit, or 10 colonies S : ce n'est pas l'ARN."},
   "clavier": {"aides": ["on suppose que", "or", "donc"], "pieges": ["la protéase détruit l'ADN"]},
   "correction": {"lignes": [{"texte": "2 : lot 4 : ADN détruit → aucune S → l'ADN", "mot": "l'A D N"},
                             {"texte": "lots 5 et 6 : des S → ni protéine, ni ARN", "mot": "ni protéine"}],
                  "parole": "le lot quatre: بلا A D N، aucune colonie S: c'est l'A D N. le lot cinq et le lot six: كاينين des colonies S: ni protéine، ni A R N."}},
  {"id": "3", "texte": "Que montre le résultat du lot 7 ? Conclure sur la nature chimique du principe transformant.",
   "reponse": {"type": "phrase", "attendu": "L'ADN purifié seul transforme des R en S (11 colonies S) : il suffit à la transformation ; le principe transformant est l'ADN."},
   "clavier": {"aides": ["ADN purifié", "suffit"], "pieges": ["les protéines"]},
   "correction": {"lignes": [{"texte": "3 : l'ADN seul → 11 colonies S : il suffit", "mot": "onze colonies S"},
                             {"texte": "le principe transformant est l'ADN", "mot": "c'est l'A D N"}],
                  "parole": "l'A D N بوحدو donne onze colonies S: le principe transformant، c'est l'A D N."}},
  {"id": "4", "texte": "Expliquer, en étapes successives, comment une bactérie R du lot 3 est devenue une bactérie S.",
   "reponse": {"type": "phrase", "attendu": "L'ADN des S tués est coupé en fragments ; un fragment entre dans une bactérie R et s'intègre à son ADN ; la bactérie fabrique une capsule : elle devient S ; ses divisions donnent une colonie S."},
   "clavier": {"aides": ["fragment d'ADN", "intégration", "capsule"], "pieges": ["la bactérie S revit"]},
   "correction": {"lignes": [{"texte": "4 : fragment d'ADN des S → entre dans R → intégration", "mot": "l'intégration"},
                             {"texte": "capsule : R devient S → colonie S", "mot": "capsule"}],
                  "parole": "fragment ديال l'A D N ديال S كيدخل ف R، وكيتلصق: l'intégration. R كتصاوب capsule، وكتولي S."}},
  {"id": "5", "texte": "En exploitant le document 2, montrer que l'ADN est le support de l'information génétique.",
   "reponse": {"type": "phrase", "attendu": "Sans extrait, les repiquages ne donnent que des colonies S : le caractère acquis est héréditaire, transmis aux bactéries filles ; or il a été apporté par l'ADN des S : l'ADN est le support de l'information génétique."},
   "clavier": {"aides": ["héréditaire", "transmis"], "pieges": ["l'extrait est ajouté à chaque repiquage"]},
   "correction": {"lignes": [{"texte": "5 : caractère transmis aux bactéries filles, apporté par l'ADN", "mot": "كتورث"},
                             {"texte": "l'ADN est le support de l'information génétique", "mot": "le support chimique"}],
                  "parole": "الصفة كتورث، وجابها l'A D N: l'A D N est le support chimique، de l'information génétique."}},
]

EX = {
  "id": "svt_ex_ch3_transformation_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "notion_information_genetique", "cours": "svt_ch3_notion_information_genetique",
  "titre": "Des colonies R qui deviennent S : la nature du principe transformant", "niveau": "moyen", "duree_min": 30,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire des résultats puis déduire", "Exploiter une expérience par hypothèse (enzymes)",
                  "Identifier la nature chimique du principe transformant", "Montrer que l'ADN est le support de l'information génétique"],
  "enonce": {
    "intro": "Les pneumocoques existent sous deux formes. La forme S possède une capsule ; sur un milieu de culture, chaque bactérie S donne une colonie d'aspect lisse. La forme R n'a pas de capsule ; elle donne une colonie d'aspect rugueux. Chaque colonie est formée des descendants d'une seule bactérie. Un chercheur prépare un extrait de bactéries S tuées par la chaleur, puis réalise les cultures du document 1 (une enzyme ajoutée à l'extrait détruit un seul type de molécule). Il repique ensuite une colonie S du lot 3 sur des milieux neufs, sans extrait (document 2).",
    "intro_dit": "دابا نقراو l'énoncé. les pneumocoques عندهم deux formes. la forme S عندها capsule، وكل bactérie S كتعطي colonie lisse. la forme R ما عندهاش capsule، وكتعطي colonie rugueuse. كل colonie جاية من une seule bactérie. واحد الباحث صاوب extrait ديال bactéries S tuées par la chaleur، ودار les cultures ديال le document un. كل enzyme كتحيد نوع واحد ديال les molécules. ومن بعد، خدا colonie S من le lot trois، وزرعها ف milieu جديد بلا extrait: هادا le document deux.",
    "figures": [tableau(LOTS, "Document 1 : cultures de bactéries R"), figure_repiquage()],
    "donnees": ["R : bactéries R vivantes ; extrait : extrait de bactéries S tuées par la chaleur ; l'enzyme est ajoutée à l'extrait avant les R",
                "Protéase : détruit les protéines", "Ribonucléase : détruit l'ARN", "Désoxyribonucléase : détruit l'ADN",
                "L'extrait de S tués contient notamment des protéines, de l'ARN et de l'ADN des S"],
    "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPLICATION}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FACILE}]},
  "similaire": {"id": "svt_ex_ch3_transformation_1_b", "titre": "Même exercice, autres données", "enonce": {
    "intro": "Même protocole avec une autre souche de pneumocoques : extrait de S tués par la chaleur, cultures de bactéries R (document 1), puis repiquage d'une colonie S du lot 3 sur des milieux neufs sans extrait (document 2). Attention : les enzymes ne sont pas dans le même ordre.",
    "intro_dit": "نفس البروتوكول ب souche أخرى ديال les pneumocoques. رد البال: les enzymes ماشي بنفس الترتيب.",
    "figures": [tableau(LOTS_B, "Document 1 : cultures de bactéries R (autre souche)"), figure_repiquage()],
    "donnees": ["R : bactéries R vivantes ; extrait : extrait de S tuées par la chaleur, traité par l'enzyme avant d'ajouter les R",
                "Protéase : détruit les protéines", "Ribonucléase : détruit l'ARN", "Désoxyribonucléase : détruit l'ADN"],
    "questions": SIM_Q}},
}

if __name__ == "__main__":
    ecrire(EX, sys.argv[1])
