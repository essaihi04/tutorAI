# Exercice SVT ch. 3 (Notion de l'information génétique) — réplication, chromatides et brins sur deux cycles, niveau
# difficile (« Supérieur »).
# Entraîne, en combinant plusieurs notions du chapitre : reconnaître un ADN en phase S et légender un œil de réplication,
# orienter un brin nouveau (antiparallèle, allongé de 5' vers 3' par l'ADN polymérase), compter chromosomes, chromatides,
# molécules, quantité d'ADN (q / 2q) et brins ¹⁵N / ¹⁴N d'une cellule 2n = 4 à la fin de S puis en métaphase du cycle
# suivant, et relier réplication semi-conservative + mitose à la conservation de l'information génétique.
# Cadre : NIG2, NIG8, NIG9, NIG10 ; aucune enzyme autre que l'ADN polymérase (exclus_hors_programme : hélicase, primase,
# fragments d'Okazaki, brin précoce / retardé), pas de carbones numérotés, pas de méiose (2n = 4 sert seulement à compter).
# Sources comparées :
# - exploration notion_information_genetique.json : cas_types « qcm_cycle » (deux chromatides de deux brins, fin de S sans
#   yeux, 5'→3'), « thymidine » (brins en deux couleurs cycle par cycle), « meselson » ; pièges « fait allonger le brin
#   nouveau de 3' vers 5' », « une chromatide = une molécule d'ADN = deux brins » ; insistance Faress (5'→3').
# - nationaux : 2018 R QCM (métaphase : deux chromatides de deux brins), 2024 R QCM (fin de S : bichromatidiens sans yeux),
#   2024 N (association ADN polymérase) ; 2017 R (thymidine sur deux cycles, plantule de fève) : situation NON reprise
#   (ici azote lourd, cellule 2n = 4, comptage des brins et des molécules).
# - séries en ligne : recherche faite, pages non lisibles depuis la session (hôtes dreamjob.ma, moutamadris.ma non résolus) ;
#   comparé avec les vidéos d'exercices de l'exploration (Lamsaf : œil de réplication, Meselson) et les nationaux.
# - cours svt_ch3 : ig_n3 (une ou deux chromatides), ig_r4/r5 (brins anciens et nouveaux génération par génération),
#   ig_r9 à ig_r11b (yeux, fourches, ADN polymérase, 5'→3', légender), ig_m4 (anaphase), ig_r12 (conservation).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

BASE = "/media/simulations/svt/notion_information_genetique-tableau/"
LEG = BASE + "replication.html?vue=legender"
REP = BASE + "replication.html?vue=replication"
MES = BASE + "meselson.html?vue=experience"
MIT = BASE + "mitose.html?vue=animale"


def figure_oeil(haut_5_a_gauche=True, titre="Document 1 : un fragment d'ADN au microscope électronique, et un œil agrandi"):
    """a) fragment d'ADN à trois yeux ; b) un œil agrandi, brins de la molécule mère (bleu) et brins en formation (orange),
    éléments numérotés 1 à 4. Le brin numéroté 4 est celui formé sur le brin du haut, du côté où il s'allonge."""
    up = lambda pts: [[x, y] for x, y in pts]
    bas = lambda pts: [[x, 50 - y] for x, y in pts]
    haut_anc = [(5, 27), (25, 27), (30, 32), (38, 36), (50, 37), (62, 36), (70, 32), (75, 27), (95, 27)]
    haut_nouv = [(29, 29.6), (38, 33.4), (50, 34.4), (62, 33.4), (71, 29.6)]
    el = [  # a) le fragment observé, trois yeux
      {"f": "ligne", "pts": [[5, 54], [18, 54]], "couleur": "blanc"}, {"f": "ligne", "pts": [[32, 54], [40, 54]], "couleur": "blanc"},
      {"f": "ligne", "pts": [[60, 54], [70, 54]], "couleur": "blanc"}, {"f": "ligne", "pts": [[80, 54], [95, 54]], "couleur": "blanc"},
      {"f": "ellipse", "c": [25, 54], "rx": 7, "ry": 2.2, "couleur": "blanc"}, {"f": "ellipse", "c": [50, 54], "rx": 10, "ry": 2.6, "couleur": "blanc"},
      {"f": "ellipse", "c": [75, 54], "rx": 5, "ry": 1.8, "couleur": "blanc"},
      {"f": "texte", "at": [2, 58.5], "t": "a) fragment d'ADN observé", "taille": "petit", "ancre": "gauche", "couleur": "cyan"},
      {"f": "fleche", "de": [50, 50.5], "a": [50, 45], "couleur": "faible", "trait": "pointille"},
      {"f": "texte", "at": [2, 47], "t": "b) un œil agrandi", "taille": "petit", "ancre": "gauche", "couleur": "cyan"},
      # b) l'œil agrandi
      {"f": "ligne", "pts": up(haut_anc), "lisse": True, "couleur": "bleu", "epais": True},
      {"f": "ligne", "pts": bas(haut_anc), "lisse": True, "couleur": "bleu", "epais": True},
      {"f": "ligne", "pts": up(haut_nouv), "lisse": True, "couleur": "orange", "epais": True},
      {"f": "ligne", "pts": bas(haut_nouv), "lisse": True, "couleur": "orange", "epais": True},
    ]
    g, d = ("5'", "3'") if haut_5_a_gauche else ("3'", "5'")
    el += [{"f": "texte", "at": [2.5, 26.2], "t": g, "taille": "petit", "ancre": "centre", "couleur": "vert"},
           {"f": "texte", "at": [97.5, 26.2], "t": d, "taille": "petit", "ancre": "centre", "couleur": "vert"},
           {"f": "texte", "at": [2.5, 21.6], "t": d, "taille": "petit", "ancre": "centre", "couleur": "vert"},
           {"f": "texte", "at": [97.5, 21.6], "t": g, "taille": "petit", "ancre": "centre", "couleur": "vert"}]
    # numéros : 1 l'œil, 2 une fourche, 3 un brin ancien, 4 le brin nouveau formé sur le brin du haut
    x4 = 36 if haut_5_a_gauche else 64      # le brin 4 est montré du côté vers lequel il s'allonge
    el += [{"f": "texte", "at": [50, 24], "t": "1", "taille": "normal", "ancre": "centre", "couleur": "jaune"},
           {"f": "fleche", "de": [16, 38], "a": [25.5, 25.5], "couleur": "jaune"}, {"f": "texte", "at": [14, 39], "t": "2", "taille": "normal", "ancre": "centre", "couleur": "jaune"},
           {"f": "fleche", "de": [86 - 50 * 0 if haut_5_a_gauche else 14, 42], "a": [64 if haut_5_a_gauche else 36, 36.4], "couleur": "jaune"},
           {"f": "texte", "at": [88 if haut_5_a_gauche else 12, 43], "t": "3", "taille": "normal", "ancre": "centre", "couleur": "jaune"},
           {"f": "fleche", "de": [x4, 44] if not haut_5_a_gauche else [x4 - 4, 44], "a": [x4, 33.2], "couleur": "jaune"},
           {"f": "texte", "at": [x4 - 4 if haut_5_a_gauche else x4, 45.5], "t": "4", "taille": "normal", "ancre": "centre", "couleur": "jaune"}]
    return {"type": "schema", "titre": titre, "cadre": {"l": 100, "h": 60},
            "legende": "Les brins de la molécule mère sont en bleu, les brins en cours de formation en orange ; les extrémités 5' et 3' des brins de la molécule mère sont indiquées.",
            "elements": el}


def figure_frise(n2):
    """Document 2 : le protocole en frise (¹⁵N, transfert, S du cycle 1, mitose 1, S du cycle 2, métaphase du cycle 2)."""
    etapes = [(8, "cellule sur ¹⁵N", "tous les brins ¹⁵N"), (28, "transfert sur ¹⁴N", "début de G1, cycle 1"),
              (48, "fin de S", "cycle 1"), (66, "mitose 1", "on suit une cellule fille"), (86, "métaphase", "cycle 2")]
    el = [{"f": "ligne", "pts": [[2, 14], [97, 14]], "couleur": "faible", "fleche": True}]
    for x, t1, t2 in etapes:
        el.append({"f": "point", "at": [x, 14], "couleur": "jaune"})
        el.append({"f": "texte", "at": [x, 19], "t": t1, "taille": "petit", "ancre": "centre", "couleur": "blanc"})
        el.append({"f": "texte", "at": [x, 8], "t": t2, "taille": "petit", "ancre": "centre", "couleur": "faible"})
    el.append({"f": "texte", "at": [50, 25], "t": f"cellule 2n = {n2}", "taille": "petit", "ancre": "centre", "couleur": "cyan"})
    return {"type": "schema", "titre": "Document 2 : deux cycles après le transfert sur ¹⁴N", "cadre": {"l": 100, "h": 28},
            "legende": "Les nucléotides fabriqués après le transfert contiennent seulement de l'azote léger ¹⁴N.",
            "elements": el}


def comptes(n2):
    """Comptes vérifiés : fin de S du cycle 1, puis métaphase du cycle 2 dans une cellule fille."""
    fin_s = {"chromosomes": n2, "chromatides": 2 * n2, "molecules": 2 * n2, "brins": 4 * n2, "b15": 2 * n2, "b14": 2 * n2}
    fille = {"molecules": n2, "b15": n2, "b14": n2}                       # après la mitose 1 : n2 molécules hybrides
    meta2 = {"chromatides": 2 * n2, "molecules": 2 * n2, "brins": 4 * n2, "b15": fille["b15"], "b14": 4 * n2 - fille["b15"],
             "hybrides": n2, "legeres": n2}
    assert fin_s["b15"] == 2 * n2 and meta2["b15"] + meta2["b14"] == meta2["brins"]
    return fin_s, meta2


F1, M2 = comptes(4)
assert (F1["chromatides"], F1["molecules"], F1["brins"], F1["b15"], F1["b14"]) == (8, 8, 16, 8, 8)
assert (M2["brins"], M2["b15"], M2["b14"]) == (16, 4, 12)

Q = [
  {"id": "1", "texte": "Préciser, en justifiant, la phase du cycle cellulaire pendant laquelle le fragment d'ADN du document 1 a été observé, puis nommer les éléments numérotés de 1 à 4.",
   "texte_dit": "السؤال un: ف أشمن phase ديال le cycle cellulaire تشاف هاد le fragment d'A D N؟ برر، ومن بعد سمي les éléments من un حتى quatre.",
   "reponse": {"type": "phrase", "attendu": "Le fragment présente des yeux de réplication : l'ADN est en train de se répliquer, c'est la phase S de l'interphase. 1 : œil de réplication ; 2 : fourche de réplication ; 3 : brin ancien (brin de la molécule mère, qui sert de modèle) ; 4 : brin nouveau (en cours de synthèse)."},
   "clavier": {"aides": ["phase S", "yeux de réplication", "œil de réplication", "fourche de réplication", "brin ancien", "brin nouveau"], "pieges": ["phase G1", "pendant la mitose", "centromère"]},
   "aides": [
     {"texte": "Que montrent les bulles du fragment observé ? Dans quelle phase l'ADN se copie-t-il ?",
      "dit": "شنو كيبينو هاد العيون الصغار ف le fragment؟ وف أشمن phase كيتنسخ l'A D N؟"},
     {"texte": "Bleu : brins de la molécule mère ; orange : brins en formation. Le numéro 2 est au bout de la bulle, là où les deux brins se séparent.",
      "dit": "الزرق: les brins ديال la molécule mère. البرتقالي: les brins اللي كيتصاوبو. و le numéro deux ف الطرف ديال l'œil، فين كيتفرقو les deux brins."}],
   "correction": {"lignes": [
       {"texte": "1 : des yeux de réplication → l'ADN se réplique : phase S de l'interphase", "mot": "la phase S"},
       {"texte": "1 : œil de réplication ; 2 : fourche de réplication", "mot": "fourche de réplication"},
       {"texte": "3 : brin ancien (modèle) ; 4 : brin nouveau", "mot": "brin nouveau"}],
     "parole": "السؤال un. ف le fragment كاينين des yeux de réplication: l'A D N كيتنسخ، إذن la phase S ديال l'interphase. un: œil de réplication. deux: fourche de réplication. trois: brin ancien، اللي كيخدم modèle. quatre: brin nouveau."},
   "explication": "ex_s1", "facile": "fa_s1"},
  {"id": "2", "texte": "Indiquer les extrémités 5' et 3' du brin nouveau 4, puis préciser, en justifiant, le sens dans lequel il s'allonge.",
   "texte_dit": "السؤال deux: حدد les extrémités cinq prime و trois prime ديال le brin nouveau quatre، ومن بعد قول ف أشمن اتجاه كيطول، وبرر.",
   "reponse": {"type": "phrase", "attendu": "Le brin nouveau 4 est complémentaire et antiparallèle du brin ancien du haut, orienté 5' à gauche et 3' à droite : le brin 4 a donc son extrémité 3' à gauche et son extrémité 5' à droite. L'ADN polymérase allonge toujours le brin nouveau dans le sens 5' → 3' : le brin 4 s'allonge vers la gauche, vers la fourche de gauche."},
   "clavier": {"aides": ["antiparallèle", "complémentaire", "5' → 3'", "ADN polymérase", "vers la gauche"], "pieges": ["3' → 5'", "vers la droite", "même orientation que le brin ancien"]},
   "aides": [
     {"texte": "Lis l'orientation du brin ancien du haut (5' et 3'). Les deux brins d'une molécule d'ADN sont-ils orientés dans le même sens ?",
      "dit": "قرا l'orientation ديال le brin ancien اللي الفوق، cinq prime و trois prime. واش les deux brins ديال l'A D N ف نفس الاتجاه؟"},
     {"texte": "Brins antiparallèles : inverse 5' et 3'. Puis rappelle-toi dans quel sens l'ADN polymérase allonge un brin nouveau.",
      "dit": "les brins antiparallèles: قلب cinq prime و trois prime. ومن بعد تفكر: l'A D N polymérase، ف أشمن اتجاه كتطول le brin nouveau؟"}],
   "correction": {"lignes": [
       {"texte": "2 : brin ancien du haut : 5' à gauche, 3' à droite", "mot": "cinq prime على اليسار"},
       {"texte": "brin 4 antiparallèle : 3' à gauche, 5' à droite", "mot": "trois prime على اليسار"},
       {"texte": "l'ADN polymérase allonge de 5' vers 3' : le brin 4 s'allonge vers la gauche", "mot": "كيطول نحو اليسار"}],
     "parole": "السؤال deux. le brin ancien اللي الفوق: cinq prime على اليسار، و trois prime على اليمين. le brin nouveau quatre complémentaire و antiparallèle: trois prime على اليسار، و cinq prime على اليمين. و l'A D N polymérase ديما كتطول le brin nouveau، de cinq prime vers trois prime. إذن le brin quatre كيطول نحو اليسار، نحو la fourche ديال اليسار."},
   "explication": "ex_s2", "facile": "fa_s2"},
  {"id": "3", "texte": "Document 2 : pour la cellule à la fin de la phase S du cycle 1, donner le nombre de chromosomes, de chromatides et de molécules d'ADN, la quantité d'ADN (q ou 2q), puis le nombre de brins à ¹⁵N et de brins à ¹⁴N. Justifier.",
   "texte_dit": "السؤال trois: ف le document deux، ف اللخر ديال la phase S ديال le cycle un: شحال من chromosome، شحال من chromatide، وشحال من molécule d'A D N، و la quantité d'A D N، q ولا deux q. ومن بعد شحال من brin ب l'azote quinze، وشحال ب l'azote quatorze. برر.",
   "reponse": {"type": "phrase", "attendu": "À la fin de S du cycle 1 : 4 chromosomes, chacun à deux chromatides, soit 8 chromatides ; une chromatide = une molécule d'ADN : 8 molécules ; la quantité d'ADN a doublé : 2q. Chacune des 4 molécules de départ (2 brins ¹⁵N) a donné deux molécules hybrides, chacune avec un brin ancien ¹⁵N et un brin nouveau ¹⁴N : 16 brins, dont 8 brins à ¹⁵N et 8 brins à ¹⁴N."},
   "clavier": {"aides": ["4 chromosomes", "8 chromatides", "8 molécules", "2q", "8 brins ¹⁵N", "8 brins ¹⁴N", "hybride"], "pieges": ["8 chromosomes", "16 brins ¹⁵N", "4 molécules"]},
   "aides": [
     {"texte": "En G1, combien de molécules d'ADN pour 2n = 4 ? Une chromatide = une molécule d'ADN = deux brins. Que fait la phase S ?",
      "dit": "ف G un، deux n égale quatre: شحال من molécule d'A D N؟ chromatide وحدة هي molécule وحدة، فيها deux brins. وشنو كدير la phase S؟"},
     {"texte": "Réplication semi-conservative : chaque molécule fille garde un brin de la molécule mère (¹⁵N) et reçoit un brin nouveau fait avec les nucléotides du milieu (¹⁴N).",
      "dit": "la réplication semi-conservative: كل molécule fille كتحافظ على brin ديال la molécule mère، ب l'azote quinze، وكتاخد brin nouveau، ب l'azote quatorze."}],
   "correction": {"lignes": [
       {"texte": "3 : 4 chromosomes à deux chromatides = 8 chromatides = 8 molécules d'ADN ; 2q", "mot": "huit molécules d'A D N"},
       {"texte": "chaque molécule : un brin ancien ¹⁵N + un brin nouveau ¹⁴N (hybride)", "mot": "كل molécule hybride"},
       {"texte": "16 brins : 8 à ¹⁵N et 8 à ¹⁴N", "mot": "huit brins ب l'azote quinze"}],
     "parole": "السؤال trois. ف اللخر ديال la phase S: quatre chromosomes، كل واحد فيه deux chromatides: huit chromatides، يعني huit molécules d'A D N، و la quantité deux q. كل molécule hybride: brin ancien ب l'azote quinze، و brin nouveau ب l'azote quatorze. إذن seize brins: huit brins ب l'azote quinze، et huit ب l'azote quatorze."},
   "explication": "ex_s3", "facile": "fa_s3"},
  {"id": "4", "texte": "On suit une des deux cellules filles jusqu'à la métaphase du cycle 2. Calculer le nombre de brins à ¹⁴N qu'elle contient, en justifiant.",
   "texte_dit": "السؤال quatre: كنتبعو وحدة من les deux cellules filles حتى la métaphase ديال le cycle deux. حسب شحال من brin ب l'azote quatorze فيها، وبرر.",
   "reponse": {"type": "valeur", "grandeur": "brins ¹⁴N", "valeur": M2["b14"], "unite": "brins", "tolerance": 0.001,
               "attendu": "Après la mitose 1, la cellule fille a 4 molécules hybrides (4 brins ¹⁵N). En S du cycle 2 : 8 molécules, soit 8 × 2 = 16 brins ; les brins ¹⁵N restent 4 (chacun dans une molécule hybride, les 4 autres molécules sont légères) ; brins ¹⁴N = 16 − 4 = 12 brins"},
   "clavier": {"aides": ["4 molécules hybrides", "8 × 2 = 16", "4 brins ¹⁵N", "16 − 4"], "pieges": ["16 − 8", "8 brins"]},
   "aides": [
     {"texte": "Après la mitose 1, chaque cellule fille reçoit une chromatide de chaque chromosome : combien de molécules hybrides, donc de brins ¹⁵N ?",
      "dit": "من بعد la mitose un، كل cellule fille كتاخد chromatide من كل chromosome. شحال من molécule hybride، يعني شحال من brin ب l'azote quinze؟"},
     {"texte": "Les brins ¹⁵N ne se multiplient pas. En métaphase du cycle 2 : nombre total de brins = nombre de molécules × 2 ; puis retire les brins ¹⁵N.",
      "dit": "les brins ب l'azote quinze ما كيتزادوش. ف la métaphase ديال le cycle deux: le nombre total des brins، égale le nombre des molécules fois deux. ومن بعد نقص les brins ب l'azote quinze."}],
   "correction": {"lignes": [
       {"texte": "4 : après la mitose 1 : 4 molécules hybrides (4 brins ¹⁵N)", "mot": "quatre molécules hybrides"},
       {"texte": "métaphase du cycle 2 : 8 molécules × 2 = 16 brins, dont toujours 4 à ¹⁵N", "mot": "huit fois deux، égale seize brins"},
       {"texte": "brins ¹⁴N = 16 − 4 = 12 brins", "mot": "seize moins quatre، égale douze brins"}],
     "parole": "السؤال quatre. من بعد la mitose un، la cellule fille فيها quatre molécules hybrides: quatre brins ب l'azote quinze. ف la phase S ديال le cycle deux، كتولي huit molécules: huit fois deux، égale seize brins. les brins ب l'azote quinze كيبقاو quatre. إذن les brins ب l'azote quatorze: seize moins quatre، égale douze brins."},
   "explication": "ex_s4", "facile": "fa_s4"},
  {"id": "5", "texte": "Décrire la composition des deux chromatides d'un même chromosome de cette métaphase, puis montrer que les deux cellules filles qui en résulteront recevront pourtant la même information génétique.",
   "texte_dit": "السؤال cinq: وصف شنو فيهم les deux chromatides ديال نفس le chromosome ف هاد la métaphase، ومن بعد بين بلي les deux cellules filles غادي ياخدو نفس l'information génétique.",
   "reponse": {"type": "phrase", "attendu": "Une chromatide contient une molécule hybride (un brin ancien ¹⁵N et un brin nouveau ¹⁴N), l'autre une molécule légère (deux brins ¹⁴N). Leur azote diffère, mais pas leur séquence : chaque brin nouveau a été construit par complémentarité (A en face de T, C en face de G) sur un brin qui avait lui-même la séquence d'origine, donc les deux molécules ont la même séquence de bases que la molécule mère. À l'anaphase, les deux chromatides sœurs se séparent et migrent vers les pôles opposés : chaque cellule fille reçoit une chromatide de chaque chromosome, donc la même information génétique (réplication semi-conservative + mitose : reproduction conforme)."},
   "clavier": {"aides": ["molécule hybride", "molécule légère", "même séquence", "complémentarité", "pôles opposés", "même information génétique"], "pieges": ["les deux chromatides sont hybrides", "séquences différentes", "même pôle"]},
   "aides": [
     {"texte": "Une cellule fille de la mitose 1 avait des molécules hybrides. Après une nouvelle réplication sur ¹⁴N, que deviennent le brin ¹⁵N et le brin ¹⁴N de chaque molécule ?",
      "dit": "la cellule fille ديال la mitose un كانت فيها des molécules hybrides. من بعد réplication جديدة ف l'azote quatorze، شنو كيعطي le brin ب l'azote quinze، وشنو كيعطي le brin ب l'azote quatorze؟"},
     {"texte": "L'information est dans la séquence des bases, pas dans l'azote. La complémentarité donne-t-elle la même séquence ? Puis : que se passe-t-il à l'anaphase ?",
      "dit": "l'information كاينة ف la séquence ديال les bases، ماشي ف l'azote. واش la complémentarité كتعطي نفس la séquence؟ ومن بعد: شنو كيوقع ف l'anaphase؟"}],
   "correction": {"lignes": [
       {"texte": "5 : une chromatide hybride (¹⁵N + ¹⁴N), l'autre légère (¹⁴N + ¹⁴N)", "mot": "وحدة hybride، والأخرى légère"},
       {"texte": "même séquence de bases (complémentarité A–T, C–G) : même information", "mot": "نفس la séquence ديال les bases"},
       {"texte": "anaphase : chromatides sœurs vers les pôles opposés → chaque cellule fille reçoit la même information génétique", "mot": "les pôles opposés"}],
     "parole": "السؤال cinq. ف كل chromosome، les deux chromatides: وحدة hybride، brin ب l'azote quinze و brin ب l'azote quatorze، والأخرى légère، les deux brins ب l'azote quatorze. ولكن عندهم نفس la séquence ديال les bases، حيت كل brin nouveau تبنى ب la complémentarité: A مقابل T، و C مقابل G. ف l'anaphase، les chromatides sœurs كيتفرقو، وكيمشيو ل les pôles opposés. إذن كل cellule fille كتاخد نفس l'information génétique."},
   "explication": "ex_s5", "facile": "fa_s5"},
]

EXPLICATION = [
  {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : un œil de réplication, en phase S",
   "screen_content": {"lead": "Des yeux de réplication → phase S. 1 œil, 2 fourche, 3 brin ancien, 4 brin nouveau."},
   "visual": {"kind": "simulation", "url": LEG, "caption": "L'œil de réplication à légender, puis corrigé"},
   "speech_text": {"mixed": "هاد les yeux كيبانو غير ملي l'A D N كيتنسخ: إذن la phase S ديال l'interphase. شوف l'œil: les deux brins anciens، بالزرق، كيتفرقو. ف الطرف ديال l'œil، فين كيتفرقو، كاينة la fourche de réplication. وف الوسط، مقابل كل brin ancien، كيتصاوب brin nouveau، بالبرتقالي. دابا les étiquettes كيمشيو لبلاصتهم: œil de réplication، fourche، brin ancien، brin nouveau."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "yeux de réplication → phase S", "mot": "إذن la phase S ديال l'interphase"},
                {"texte": "1 œil ; 2 fourche ; 3 brin ancien ; 4 brin nouveau", "mot": "œil de réplication، fourche، brin ancien، brin nouveau"}],
     "pointage": [{"mot": "هاد les yeux", "commande": "play_until", "parametres": {"moment": "etiquettes"}},
                  {"mot": "إذن la phase S ديال l'interphase", "cible": "centre:0"},
                  {"mot": "شوف l'œil", "repere": "oeil"},
                  {"mot": "كاينة la fourche de réplication", "repere": "fourche_droite"},
                  {"mot": "دابا les étiquettes", "commande": "play_until", "parametres": {"moment": "corrige"}},
                  {"mot": "œil de réplication، fourche، brin ancien، brin nouveau", "cible": "centre:1"}]}},
  {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : antiparallèle, puis 5' → 3'",
   "screen_content": {"lead": "Brin ancien 5' → 3' de gauche à droite ; brin nouveau en face : 3' à gauche, 5' à droite, il s'allonge vers la gauche."},
   "visual": {"kind": "simulation", "url": REP, "caption": "L'ADN polymérase et le sens d'allongement"},
   "speech_text": {"mixed": "شوف le brin ancien اللي الفوق: cinq prime على اليسار، و trois prime على اليمين. le brin nouveau اللي مقابلو antiparallèle: trois prime على اليسار، و cinq prime على اليمين. l'A D N polymérase كتحط les nucléotides libres، مقابل A، T، ومقابل C، G. و le brin nouveau ديما كيطول من cinq prime ل trois prime. إذن le brin nouveau ديال الفوق كيطول نحو اليسار، و اللي لتحت كيطول نحو اليمين."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "brin ancien : 5' à gauche → 3' à droite", "mot": "cinq prime على اليسار، و trois prime على اليمين"},
                {"texte": "brin nouveau antiparallèle : 3' à gauche, 5' à droite", "mot": "le brin nouveau اللي مقابلو antiparallèle"},
                {"texte": "allongement 5' → 3' : vers la gauche", "mot": "كيطول نحو اليسار"}],
     "pointage": [{"mot": "شوف le brin ancien", "commande": "set_time", "parametres": {"time_s": 8.0}},
                  {"mot": "شوف le brin ancien", "repere": "molecule"},
                  {"mot": "cinq prime على اليسار، و trois prime على اليمين", "cible": "centre:0"},
                  {"mot": "le brin nouveau اللي مقابلو antiparallèle", "cible": "centre:1"},
                  {"mot": "l'A D N polymérase كتحط", "commande": "play_until", "parametres": {"moment": "polymerase_pose"}},
                  {"mot": "l'A D N polymérase كتحط", "repere": "polymerase"},
                  {"mot": "و le brin nouveau ديما كيطول", "commande": "play_until", "parametres": {"moment": "sens_5_3"}},
                  {"mot": "و le brin nouveau ديما كيطول", "repere": "sens"},
                  {"mot": "كيطول نحو اليسار", "cible": "centre:2"}]}},
  {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : à la fin de S, deux molécules hybrides par chromosome",
   "screen_content": {"lead": "Fin de S : 4 chromosomes à deux chromatides = 8 molécules, chacune un brin ¹⁵N + un brin ¹⁴N : 8 + 8 brins."},
   "visual": {"kind": "simulation", "url": REP, "caption": "Les yeux fusionnent : deux molécules filles"},
   "speech_text": {"mixed": "les yeux كيكبرو حتى كيتلاقاو. وكنلقاو deux molécules: كل وحدة فيها brin ancien، بالزرق، و brin nouveau، بالبرتقالي. ف التمرين، le brin ancien فيه l'azote quinze، و le brin nouveau فيه l'azote quatorze: molécule hybride. هاد les deux molécules هما les deux chromatides ديال chromosome. إذن deux n égale quatre: quatre chromosomes، huit chromatides، huit molécules hybrides. huit brins ب l'azote quinze، et huit brins ب l'azote quatorze."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "chaque molécule : brin ancien ¹⁵N + brin nouveau ¹⁴N", "mot": "molécule hybride"},
                {"texte": "2n = 4 : 4 chromosomes, 8 chromatides, 8 molécules (2q)", "mot": "huit molécules hybrides"},
                {"texte": "16 brins : 8 à ¹⁵N, 8 à ¹⁴N", "mot": "et huit brins ب l'azote quatorze"}],
     "pointage": [{"mot": "les yeux كيكبرو", "commande": "set_time", "parametres": {"time_s": 15.4}},
                  {"mot": "les yeux كيكبرو", "commande": "play_until", "parametres": {"moment": "yeux_fusionnent"}},
                  {"mot": "وكنلقاو deux molécules", "commande": "play_until", "parametres": {"moment": "deux_molecules"}},
                  {"mot": "وكنلقاو deux molécules", "repere": "molecule_1"},
                  {"mot": "كل وحدة فيها brin ancien", "repere": "molecule_2"},
                  {"mot": "molécule hybride", "cible": "centre:0"},
                  {"mot": "huit molécules hybrides", "cible": "centre:1"},
                  {"mot": "et huit brins ب l'azote quatorze", "cible": "centre:2"}]}},
  {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : à la deuxième réplication, moitié hybrides, moitié légères",
   "screen_content": {"lead": "4 molécules hybrides → 8 molécules : 4 hybrides + 4 légères ; 16 brins dont 4 à ¹⁵N : 12 brins à ¹⁴N."},
   "visual": {"kind": "simulation", "url": MES, "caption": "La même logique chez les bactéries : G2 et l'arbre des molécules"},
   "speech_text": {"mixed": "شوف نفس الفكرة عند les bactéries. ف la génération deux، deux bandes: hybride et légère، بنفس الكمية. علاش؟ شوف l'arbre: molécule hybride كتعطي une hybride et une légère. le brin lourd ما كيتزادش، كيبقى ف molécule وحدة. ف التمرين: la cellule fille فيها quatre molécules hybrides. ف la phase S ديال le cycle deux، كتولي huit molécules: quatre hybrides، et quatre légères. huit fois deux، égale seize brins. les brins ب l'azote quinze: toujours quatre. seize moins quatre، égale douze brins ب l'azote quatorze."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "1 hybride → 1 hybride + 1 légère", "mot": "molécule hybride كتعطي une hybride et une légère"},
                {"texte": "8 molécules × 2 = 16 brins ; ¹⁵N : toujours 4", "mot": "huit fois deux، égale seize brins"},
                {"texte": "brins ¹⁴N = 16 − 4 = 12", "mot": "seize moins quatre، égale douze brins"}],
     "pointage": [{"mot": "شوف نفس الفكرة", "commande": "set_time", "parametres": {"time_s": 20.4}},
                  {"mot": "ف la génération deux", "commande": "play_until", "parametres": {"moment": "g2_bandes"}},
                  {"mot": "ف la génération deux", "repere": "tube_g2"},
                  {"mot": "شوف l'arbre", "commande": "play_until", "parametres": {"moment": "arbre_g0_g3"}},
                  {"mot": "شوف l'arbre", "repere": "arbre"},
                  {"mot": "molécule hybride كتعطي une hybride et une légère", "cible": "centre:0"},
                  {"mot": "huit fois deux، égale seize brins", "cible": "centre:1"},
                  {"mot": "seize moins quatre، égale douze brins", "cible": "centre:2"}]}},
  {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : azote différent, même séquence, même information",
   "screen_content": {"lead": "Une chromatide hybride, l'autre légère, mais la même séquence ; à l'anaphase, une chromatide de chaque chromosome à chaque pôle."},
   "visual": {"kind": "simulation", "url": MIT, "caption": "La mitose : les chromatides sœurs vers les pôles opposés"},
   "speech_text": {"mixed": "ف la métaphase ديال le cycle deux، كل chromosome فيه deux chromatides: وحدة hybride، والأخرى légère. l'azote ماشي بحال بحال، ولكن la séquence ديال les bases هي هي: حيت كل brin nouveau تبنى ب la complémentarité، A مقابل T، و C مقابل G. شوف: les chromosomes على la plaque équatoriale. ف l'anaphase، le centromère كيتقسم، و les chromatides sœurs كيمشيو ل les pôles opposés. وف اللخر، deux cellules filles، كل وحدة فيها chromatide من كل chromosome: نفس l'information génétique."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "une chromatide hybride, l'autre légère", "mot": "وحدة hybride، والأخرى légère"},
                {"texte": "même séquence (A–T, C–G) : même information", "mot": "la séquence ديال les bases هي هي"},
                {"texte": "anaphase : chromatides sœurs vers les pôles opposés", "mot": "كيمشيو ل les pôles opposés"},
                {"texte": "deux cellules filles : même information génétique", "mot": "نفس l'information génétique"}],
     "pointage": [{"mot": "وحدة hybride، والأخرى légère", "cible": "centre:0"},
                  {"mot": "la séquence ديال les bases هي هي", "cible": "centre:1"},
                  {"mot": "شوف: les chromosomes", "commande": "play_until", "parametres": {"moment": "plaque_equatoriale"}},
                  {"mot": "le centromère كيتقسم", "commande": "play_until", "parametres": {"moment": "clivage_centromere"}},
                  {"mot": "كيمشيو ل les pôles opposés", "commande": "play_until", "parametres": {"moment": "migration"}},
                  {"mot": "كيمشيو ل les pôles opposés", "cible": "centre:2"},
                  {"mot": "وف اللخر، deux cellules filles", "commande": "play_until", "parametres": {"moment": "fin"}},
                  {"mot": "نفس l'information génétique", "cible": "centre:3"}]}},
]

NOMS = [("a", "œil de réplication"), ("b", "fourche de réplication"), ("c", "brin ancien"), ("d", "brin nouveau"), ("e", "ADN polymérase")]
DIT_NOM = {"a": "œil de réplication", "b": "fourche de réplication", "c": "brin ancien", "d": "brin nouveau", "e": "l'A D N polymérase"}
JUSTE = {"1": "a", "2": "b", "3": "c", "4": "d"}
POURQUOI = {"1": ("la bulle où les deux brins sont séparés", "la bulle فين les deux brins متفرقين"),
            "2": ("le bout de la bulle, où les brins se séparent", "الطرف ديال la bulle، فين كيتفرقو les brins"),
            "3": ("un brin bleu de la molécule mère", "brin زرق ديال la molécule mère"),
            "4": ("un brin orange, en cours de formation", "brin برتقالي، كيتصاوب")}
RETOURS = {}
for gch, juste in JUSTE.items():
    for d, nom in NOMS:
        if d == juste:
            RETOURS[f"{gch}-{d}"] = (True, f"Oui : {POURQUOI[gch][0]} : {nom}.", f"برافو: {POURQUOI[gch][1]}: {DIT_NOM[d]}.")
        elif d == "e":
            RETOURS[f"{gch}-{d}"] = (False, "Non : l'ADN polymérase est une enzyme ; elle n'est pas numérotée sur ce schéma.", "لا، l'A D N polymérase enzyme، ما عندهاش رقم ف هاد le schéma.")
        else:
            RETOURS[f"{gch}-{d}"] = (False, f"Non : le numéro {gch} montre {POURQUOI[gch][0]}, pas le {nom}." if not nom.startswith("œ") else f"Non : le numéro {gch} montre {POURQUOI[gch][0]}, pas l'{nom}.",
                                     f"لا، هاد le numéro كيبين {POURQUOI[gch][1]}، ماشي {DIT_NOM[d]}.")

FACILE = [
  association("fa_s1", "Plus facile : légender l'œil de réplication", "Relie chaque numéro du document 1 à son nom.",
    "سؤال ساهل: ربط كل numéro مع la légende ديالو.",
    "Relie chaque numéro du document 1 à son nom.",
    [("1", "numéro 1"), ("2", "numéro 2"), ("3", "numéro 3 (bleu)"), ("4", "numéro 4 (orange)")], NOMS, JUSTE, RETOURS,
    ("(1 ; a) (2 ; b) (3 ; c) (4 ; d) : l'ADN polymérase (e) n'est pas numérotée.", "الجواب: un مع a، deux مع b، trois مع c، quatre مع d. و l'A D N polymérase ما عندهاش رقم.")),
  qcm_facile("fa_s2", "Plus facile : le sens d'allongement", "سؤال ساهل: ف أشمن اتجاه كيطول le brin nouveau؟",
    "Le brin nouveau est toujours allongé par l'ADN polymérase dans le sens…",
    ["3' → 5'", "5' → 3'", "des deux sens à la fois"], 1, {
      "1": {"juste": rep("برافو! l'A D N polymérase ديما كتطول le brin nouveau، de cinq prime vers trois prime.", "Juste : toujours de 5' vers 3'.")},
      "0": {"1": rep("لا، هادا هو الغلط اللي كيديرو بزاف. l'A D N polymérase كتزيد les nucléotides ف أشمن طرف؟ عاود اختار.", "C'est l'erreur la plus fréquente. À quelle extrémité l'ADN polymérase ajoute-t-elle les nucléotides ? Réessaie."),
            "2": rep("الجواب: de cinq prime vers trois prime، ديما.", "Réponse : de 5' vers 3', toujours.")},
      "2": {"1": rep("لا، le brin nouveau كيطول ف اتجاه واحد فقط. عاود اختار.", "Un brin nouveau s'allonge dans un seul sens. Réessaie."),
            "2": rep("الجواب: de cinq prime vers trois prime.", "Réponse : de 5' vers 3'.")}},
    "Le brin nouveau s'allonge dans quel sens ?"),
  vrai_faux("fa_s3", "Plus facile : la fin de la phase S", "Vrai ou faux : la cellule 2n = 4 à la fin de S du cycle 1.",
    "سؤال ساهل: صحيح ولا غالط، على la cellule ف اللخر ديال la phase S.",
    [("À la fin de S, la cellule a 8 chromosomes.", False, "Non : toujours 4 chromosomes, mais chacun a maintenant deux chromatides (8 chromatides)."),
     ("Une chromatide contient une molécule d'ADN, formée de deux brins.", True, "Oui : 8 chromatides = 8 molécules = 16 brins."),
     ("À la fin de S du cycle 1, chaque molécule a un brin ¹⁵N et un brin ¹⁴N.", True, "Oui : réplication semi-conservative, 8 brins ¹⁵N et 8 brins ¹⁴N.")]),
  qcm_facile("fa_s4", "Plus facile : combien de brins ¹⁴N ?", "سؤال ساهل: شحال من brin ب l'azote quatorze؟",
    "En métaphase du cycle 2, la cellule fille a 16 brins, dont 4 à ¹⁵N. Le nombre de brins à ¹⁴N est…",
    ["8", "16", "12"], 2, {
      "2": {"juste": rep("برافو! seize moins quatre، égale douze brins ب l'azote quatorze.", "Juste : 16 − 4 = 12 brins à ¹⁴N.")},
      "0": {"1": rep("لا، huit هو النص. les brins ب l'azote quinze غير quatre. عاود اختار.", "8, c'est la moitié ; or il n'y a que 4 brins ¹⁵N. Réessaie."),
            "2": rep("الجواب: seize moins quatre، égale douze.", "Réponse : 16 − 4 = 12.")},
      "1": {"1": rep("لا، seize هو le total. خاصك تنقص les brins ب l'azote quinze. عاود اختار.", "16 est le total ; retire les brins ¹⁵N. Réessaie."),
            "2": rep("الجواب: seize moins quatre، égale douze.", "Réponse : 16 − 4 = 12.")}},
    "En métaphase du cycle deux, combien de brins à l'azote quatorze ?"),
  qcm_facile("fa_s5", "Plus facile : les deux chromatides du cycle 2", "سؤال ساهل: les deux chromatides ف le cycle deux.",
    "En métaphase du cycle 2, les deux chromatides d'un chromosome…",
    ["sont toutes les deux hybrides", "ont des séquences de bases différentes", "diffèrent par leur azote mais ont la même séquence de bases"], 2, {
      "2": {"juste": rep("برافو! وحدة hybride والأخرى légère، ولكن نفس la séquence ديال les bases: نفس l'information.", "Juste : une hybride, une légère, même séquence.")},
      "0": {"1": rep("لا، الخلية فيها غير quatre brins ب l'azote quinze، و huit chromatides. واش يكفيو؟ عاود اختار.", "Il n'y a que 4 brins ¹⁵N pour 8 chromatides : cela suffit-il ? Réessaie."),
            "2": rep("الجواب: وحدة hybride والأخرى légère، بنفس la séquence.", "Réponse : l'une hybride, l'autre légère, même séquence.")},
      "1": {"1": rep("لا، la complémentarité كتعطي نسخة مطابقة. A ديما مقابل T، و C مقابل G. عاود اختار.", "La complémentarité donne une copie identique (A–T, C–G). Réessaie."),
            "2": rep("الجواب: نفس la séquence، و l'azote هو اللي مختلف.", "Réponse : même séquence, seul l'azote diffère.")}},
    "Les deux chromatides d'un chromosome, en métaphase du cycle deux ?"),
]

# ---- exercice semblable : 2n = 6, brin du haut orienté 3' à gauche
F1b, M2b = comptes(6)
assert (F1b["chromatides"], F1b["brins"], F1b["b15"], M2b["brins"], M2b["b15"], M2b["b14"]) == (12, 24, 12, 24, 6, 18)
SIM_Q = [
  {"id": "1", "texte": "Préciser, en justifiant, la phase du cycle cellulaire pendant laquelle le fragment d'ADN du document 1 a été observé, puis nommer les éléments numérotés de 1 à 4.",
   "reponse": {"type": "phrase", "attendu": "Des yeux de réplication : l'ADN se réplique, phase S. 1 : œil de réplication ; 2 : fourche de réplication ; 3 : brin ancien ; 4 : brin nouveau."},
   "clavier": {"aides": ["phase S", "œil de réplication", "fourche de réplication"], "pieges": ["phase G1"]},
   "correction": {"lignes": [{"texte": "1 : yeux de réplication → phase S", "mot": "la phase S"},
                             {"texte": "1 œil ; 2 fourche ; 3 brin ancien ; 4 brin nouveau", "mot": "brin nouveau"}],
                  "parole": "des yeux de réplication: la phase S. un، œil de réplication. deux، fourche de réplication. trois، brin ancien. quatre، brin nouveau."}},
  {"id": "2", "texte": "Indiquer les extrémités 5' et 3' du brin nouveau 4, puis préciser, en justifiant, le sens dans lequel il s'allonge.",
   "reponse": {"type": "phrase", "attendu": "Le brin ancien du haut est orienté 3' à gauche, 5' à droite ; le brin 4, antiparallèle, a son 5' à gauche et son 3' à droite. L'ADN polymérase allonge de 5' vers 3' : le brin 4 s'allonge vers la droite, vers la fourche de droite."},
   "clavier": {"aides": ["antiparallèle", "5' → 3'", "vers la droite"], "pieges": ["vers la gauche", "3' → 5'"]},
   "correction": {"lignes": [{"texte": "2 : brin 4 : 5' à gauche, 3' à droite (antiparallèle)", "mot": "antiparallèle"},
                             {"texte": "allongement 5' → 3' : vers la droite", "mot": "نحو اليمين"}],
                  "parole": "le brin quatre antiparallèle: cinq prime على اليسار. l'A D N polymérase كتطول de cinq prime vers trois prime: إذن كيطول نحو اليمين."}},
  {"id": "3", "texte": "Document 2 : pour la cellule à la fin de la phase S du cycle 1, donner le nombre de chromosomes, de chromatides et de molécules d'ADN, la quantité d'ADN (q ou 2q), puis le nombre de brins à ¹⁵N et de brins à ¹⁴N. Justifier.",
   "reponse": {"type": "phrase", "attendu": "6 chromosomes à deux chromatides : 12 chromatides = 12 molécules d'ADN ; 2q ; chaque molécule est hybride : 24 brins, dont 12 à ¹⁵N et 12 à ¹⁴N."},
   "clavier": {"aides": ["12 chromatides", "2q", "hybride"], "pieges": ["12 chromosomes"]},
   "correction": {"lignes": [{"texte": "3 : 6 chromosomes, 12 chromatides, 12 molécules, 2q", "mot": "douze molécules"},
                             {"texte": "24 brins : 12 à ¹⁵N, 12 à ¹⁴N", "mot": "vingt-quatre brins"}],
                  "parole": "six chromosomes، douze chromatides، douze molécules، deux q. كل molécule hybride: vingt-quatre brins، douze ب l'azote quinze، et douze ب l'azote quatorze."}},
  {"id": "4", "texte": "On suit une des deux cellules filles jusqu'à la métaphase du cycle 2. Calculer le nombre de brins à ¹⁴N qu'elle contient, en justifiant.",
   "reponse": {"type": "valeur", "grandeur": "brins ¹⁴N", "valeur": M2b["b14"], "unite": "brins", "tolerance": 0.001,
               "attendu": "Cellule fille : 6 molécules hybrides (6 brins ¹⁵N) ; en métaphase du cycle 2 : 12 molécules × 2 = 24 brins ; brins ¹⁴N = 24 − 6 = 18 brins"},
   "clavier": {"aides": ["12 × 2 = 24", "6 brins ¹⁵N", "24 − 6"], "pieges": ["24 − 12"]},
   "correction": {"lignes": [{"texte": "4 : 12 molécules × 2 = 24 brins, dont 6 à ¹⁵N", "mot": "vingt-quatre brins"},
                             {"texte": "brins ¹⁴N = 24 − 6 = 18 brins", "mot": "dix-huit brins"}],
                  "parole": "douze molécules fois deux، égale vingt-quatre brins. les brins ب l'azote quinze: six. vingt-quatre moins six، égale dix-huit brins."}},
  {"id": "5", "texte": "Décrire la composition des deux chromatides d'un même chromosome de cette métaphase, puis montrer que les deux cellules filles qui en résulteront recevront pourtant la même information génétique.",
   "reponse": {"type": "phrase", "attendu": "Une chromatide hybride (¹⁵N + ¹⁴N), l'autre légère (¹⁴N + ¹⁴N), avec la même séquence de bases (complémentarité A–T, C–G). À l'anaphase, les chromatides sœurs se séparent vers les pôles opposés : chaque cellule fille reçoit la même information génétique."},
   "clavier": {"aides": ["hybride", "légère", "même séquence", "pôles opposés"], "pieges": ["séquences différentes"]},
   "correction": {"lignes": [{"texte": "5 : une chromatide hybride, l'autre légère, même séquence", "mot": "نفس la séquence"},
                             {"texte": "anaphase : pôles opposés → même information génétique", "mot": "نفس l'information génétique"}],
                  "parole": "وحدة hybride والأخرى légère، ولكن نفس la séquence. ف l'anaphase كيمشيو ل les pôles opposés: نفس l'information génétique."}},
]

EX = {
  "id": "svt_ex_ch3_replication_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "notion_information_genetique", "cours": "svt_ch3_notion_information_genetique",
  "titre": "Yeux de réplication et brins marqués sur deux cycles", "niveau": "difficile", "duree_min": 40,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Reconnaître et légender un œil de réplication", "Orienter un brin nouveau (5' → 3')",
                  "Compter chromosomes, chromatides, molécules et brins au cours du cycle",
                  "Relier réplication semi-conservative et mitose à la conservation de l'information génétique"],
  "enonce": {
    "intro": "Document 1 : un fragment d'ADN d'une cellule animale, observé au microscope électronique, présente plusieurs bulles ; l'une d'elles est agrandie et schématisée. Document 2 : une cellule animale (2n = 4) a été cultivée longtemps dans un milieu dont la seule source d'azote est l'azote lourd ¹⁵N : tous les brins de son ADN contiennent ¹⁵N. Au début de la phase G1 d'un cycle (cycle 1), elle est transférée dans un milieu à azote léger ¹⁴N, où elle accomplit deux cycles. On suit ses chromosomes à la fin de la phase S du cycle 1, puis dans une de ses deux cellules filles jusqu'à la métaphase du cycle 2.",
    "intro_dit": "دابا نقراو l'énoncé. ف le document un: fragment d'A D N ديال cellule animale، تشاف ف le microscope électronique، فيه بحال شي bulles، ووحدة منهم مكبرة. ف le document deux: cellule animale، deux n égale quatre، عاشت مدة طويلة ف milieu فيه غير l'azote lourd، l'azote quinze: إذن كل les brins ديال l'A D N ديالها فيهم l'azote quinze. ف البداية ديال G un ديال le cycle un، نقلناها ل milieu فيه l'azote léger، l'azote quatorze، ودارت deux cycles. كنتبعو les chromosomes ديالها ف اللخر ديال la phase S، ومن بعد ف وحدة من les cellules filles، حتى la métaphase ديال le cycle deux.",
    "figures": [figure_oeil(True), figure_frise(4)],
    "donnees": ["Une chromatide = une molécule d'ADN = deux brins", "Cellule 2n = 4 ; tous les brins ¹⁵N au départ",
                "Après le transfert, les nucléotides disponibles ne contiennent que ¹⁴N"],
    "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPLICATION}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FACILE}]},
  "similaire": {"id": "svt_ex_ch3_replication_1_b", "titre": "Même exercice, autres données", "enonce": {
    "intro": "Même étude avec une autre cellule animale (2n = 6) : un œil de réplication agrandi (document 1, attention à l'orientation des brins), puis une cellule dont tous les brins contiennent ¹⁵N, transférée sur ¹⁴N au début de G1 du cycle 1 et suivie pendant deux cycles (document 2).",
    "intro_dit": "نفس الدراسة ب cellule أخرى، deux n égale six. رد البال ل l'orientation ديال les brins ف le document un.",
    "figures": [figure_oeil(False, "Document 1 : un œil de réplication agrandi (autre cellule)"), figure_frise(6)],
    "donnees": ["Une chromatide = une molécule d'ADN = deux brins", "Cellule 2n = 6 ; tous les brins ¹⁵N au départ"],
    "questions": SIM_Q}},
}

if __name__ == "__main__":
    ecrire(EX, sys.argv[1])
