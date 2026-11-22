# Exercice SVT ch. 3 (Notion de l'information génétique) — thymidine radioactive et cycle cellulaire, niveau difficile
# (« Supérieur »).
# Entraîne, en combinant deux notions du chapitre (cycle cellulaire / quantité d'ADN et réplication semi-conservative) :
# décrire deux courbes en parallèle, déduire la phase S de l'incorporation de thymidine, délimiter G1, S, G2, M et leurs
# durées, relier le marquage aux brins et aux chromatides (deux chromatides marquées au premier cycle), calculer la durée de
# S par le pourcentage de noyaux marqués (t(phase) = % × durée du cycle), expliquer le délai des premières mitoses marquées
# par la durée de G2. Au-dessus du national (document moins guidé, raisonnement en plusieurs étapes), dans le cadre
# (NIG3, NIG5, NIG9) ; aucune enzyme hors programme, aucune régulation du cycle.
# Sources comparées :
# - exploration notion_information_genetique.json : cas_types « thymidine » (la thymidine n'entre que dans l'ADN pendant la
#   réplication ; schéma des brins en deux couleurs), « courbe_adn » (une ligne par phase avec q et 2q), « duree_cycle »
#   (t(phase) = % × durée du cycle ; Faress, national agronomie 2015 R) ; pièges « place la réplication en G1/G2 »,
#   « oublie M dans G1 + S + G2 + M » ; valeurs repères : cycle de 20 h, G1 9 h, S 6 h, G2 4 h, M 1 h (celles de cycle.html).
# - national 2017 R ex. 2 (plantule de fève, deux cycles, chromosomes métaphasiques) : situation NON reprise (ici une culture
#   synchronisée et un marquage bref, mesures de radioactivité et pourcentages) ; seule l'idée « la thymidine marque l'ADN
#   répliqué » est commune au chapitre.
# - séries en ligne : recherche faite, pages non lisibles depuis la session (hôtes dreamjob.ma, moutamadris.ma non résolus) ;
#   comparé avec les vidéos d'exercices de l'exploration (Faress QsPZTaFg79E : durées ; Lamsaf : Taylor) et les nationaux.
# - cours svt_ch3 : ig_c3 (courbe q → 2q), ig_c1 (cycle de 20 h), ig_c6b (durée d'une phase), ig_r7 (thymidine,
#   autoradiographie, colchicine non utilisée ici).
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

BASE = "/media/simulations/svt/notion_information_genetique-tableau/"
COURBE = BASE + "cycle.html?vue=courbe&icones=0"
CYCLE = BASE + "cycle.html?vue=cycle"
THY = BASE + "thymidine.html?vue=experience"
DUREES = BASE + "documents.html?vue=durees"


def g(x):
    return f"{x:g}".replace(".", ",")


def courbes(c, titre_suffixe=""):
    """Documents 1a et 1b : quantité d'ADN et radioactivité des cellules d'une culture synchronisée, en fonction du temps."""
    g1, s, g2, m, q, r, xmax = c["G1"], c["S"], c["G2"], c["M"], c["q"], c["r"], c["xmax"]
    t1, t2, t3 = g1, g1 + s, g1 + s + g2 + m          # début S, fin S, fin de la mitose
    tc = t3 - 0.2                                       # la chute, à la fin de la mitose
    grad = list(range(0, xmax + 1, 2))
    adn = {"type": "courbe", "titre": "Document 1a : quantité d'ADN par cellule" + titre_suffixe,
           "axes": {"x": {"min": 0, "max": xmax, "nom": "t", "unite": "h", "graduations": grad},
                    "y": {"min": 0, "max": 2 * q + 2, "nom": "ADN", "unite": "UA", "graduations": list(range(0, 2 * q + 3, 1))}},
           "legende": "Quantité moyenne d'ADN par cellule, en unités arbitraires (UA).",
           "elements": [
             {"f": "courbe", "expr": f"{q}", "de": 0, "a": t1, "couleur": "cyan"},
             {"f": "courbe", "expr": f"{q}+{q}*(x-{t1})/{s}", "de": t1, "a": t2, "couleur": "cyan"},
             {"f": "courbe", "expr": f"{2 * q}", "de": t2, "a": tc, "couleur": "cyan"},
             {"f": "courbe", "expr": f"{2 * q}-{q}*(x-{tc})/0.2", "de": tc, "a": t3, "couleur": "cyan"},
             {"f": "courbe", "expr": f"{q}", "de": t3, "a": xmax, "couleur": "cyan"}]}
    rad = {"type": "courbe", "titre": "Document 1b : radioactivité par cellule" + titre_suffixe,
           "axes": {"x": {"min": 0, "max": xmax, "nom": "t", "unite": "h", "graduations": grad},
                    "y": {"min": 0, "max": r + 2, "nom": "radioactivité", "unite": "UA", "graduations": list(range(0, r + 3, 2))}},
           "legende": "Radioactivité moyenne d'une cellule (thymidine radioactive incorporée), en unités arbitraires.",
           "elements": [
             {"f": "courbe", "expr": "0.05", "de": 0, "a": t1, "couleur": "orange"},
             {"f": "courbe", "expr": f"{r}*(x-{t1})/{s}", "de": t1, "a": t2, "couleur": "orange"},
             {"f": "courbe", "expr": f"{r}", "de": t2, "a": tc, "couleur": "orange"},
             {"f": "courbe", "expr": f"{r}-{r / 2}*(x-{tc})/0.2", "de": tc, "a": t3, "couleur": "orange"},
             {"f": "courbe", "expr": f"{r / 2}", "de": t3, "a": xmax, "couleur": "orange"}]}
    return [adn, rad]


C1 = {"G1": 9, "S": 6, "G2": 4, "M": 1, "q": 3, "r": 8, "xmax": 24}
CYC = C1["G1"] + C1["S"] + C1["G2"] + C1["M"]
assert CYC == 20
PCT = 30
TS = PCT / 100 * CYC
assert TS == C1["S"] == 6

Q = [
  {"id": "1", "texte": "Décrire l'évolution de la radioactivité des cellules (document 1b) en la comparant à celle de la quantité d'ADN (document 1a).",
   "texte_dit": "السؤال un: وصف l'évolution ديال la radioactivité ديال les cellules، ف le document un b، وقارنها مع la quantité d'A D N، ف le document un a.",
   "reponse": {"type": "phrase", "attendu": "De 0 à 9 h, la radioactivité est nulle alors que la quantité d'ADN reste constante à 3 UA (q). De 9 h à 15 h, la radioactivité augmente de 0 à 8 UA en même temps que la quantité d'ADN double, de 3 à 6 UA. De 15 h à 20 h, les deux restent constantes (8 UA et 6 UA). À 20 h, les deux diminuent de moitié en même temps : la radioactivité passe de 8 à 4 UA et l'ADN de 6 à 3 UA, puis elles restent constantes jusqu'à 24 h."},
   "clavier": {"aides": ["reste nulle", "augmente", "constante", "diminue de moitié", "en même temps", "UA"], "pieges": ["la radioactivité augmente en G1", "diminue lentement"]},
   "aides": [
     {"texte": "Découpe le temps en périodes là où une des deux courbes change : 9 h, 15 h, 20 h.",
      "dit": "قسم le temps ل des périodes، فين كتبدل شي courbe: neuf heures، quinze heures، et vingt heures."},
     {"texte": "Pour chaque période : ce que fait la radioactivité (valeurs), ce que fait l'ADN au même moment (valeurs).",
      "dit": "ف كل période: شنو كدير la radioactivité، مع les valeurs، وشنو كدير la quantité d'A D N ف نفس الوقت."}],
   "correction": {"lignes": [
       {"texte": "1 : 0 – 9 h : radioactivité nulle ; ADN constant, 3 UA", "mot": "la radioactivité nulle"},
       {"texte": "9 – 15 h : radioactivité de 0 à 8 UA, en même temps que l'ADN de 3 à 6 UA", "mot": "de zéro à huit unités arbitraires"},
       {"texte": "15 – 20 h : les deux constantes (8 et 6 UA)", "mot": "les deux constantes"},
       {"texte": "20 h : les deux diminuent de moitié (8 → 4 UA ; 6 → 3 UA)", "mot": "les deux كينقصو للنص"}],
     "parole": "السؤال un. de zéro à neuf heures: la radioactivité nulle، و la quantité d'A D N constante، trois unités arbitraires. de neuf à quinze heures: la radioactivité كتزيد، de zéro à huit unités arbitraires، ف نفس الوقت اللي l'A D N كيتضاعف، de trois à six. de quinze à vingt heures: les deux constantes. et à vingt heures: les deux كينقصو للنص، la radioactivité de huit à quatre، et l'A D N de six à trois."},
   "explication": "ex_s1", "facile": "fa_s1"},
  {"id": "2", "texte": "Expliquer les variations de la radioactivité, puis en déduire les limites et la durée de chacune des phases G1, S, G2 et M de ce cycle.",
   "texte_dit": "السؤال deux: فسر les variations ديال la radioactivité، ومن بعد استنتج فين كتبدا وفين كتسالي كل phase، G un، S، G deux، et la mitose، وشحال كتاخد.",
   "reponse": {"type": "phrase", "attendu": "La thymidine radioactive n'entre que dans l'ADN, lors de sa réplication : la radioactivité n'augmente que pendant la synthèse de l'ADN, la phase S, de 9 h à 15 h (6 h), quand l'ADN passe de q à 2q. Avant, de 0 à 9 h : phase G1 (9 h), pas de réplication. De 15 h à 19 h : phase G2 (4 h), l'ADN reste à 2q. De 19 h à 20 h : la mitose (1 h, chromosomes condensés) ; à 20 h, l'ADN et sa radioactivité sont partagés entre les deux cellules filles, d'où la division par deux. Le cycle dure 9 + 6 + 4 + 1 = 20 h."},
   "clavier": {"aides": ["phase S", "G1 = 9 h", "G2 = 4 h", "M = 1 h", "réplication", "partagés entre deux cellules filles", "20 h"], "pieges": ["S de 0 à 9 h", "G2 = 5 h", "la mitose de 15 à 20 h"]},
   "aides": [
     {"texte": "Dans quelle molécule entre la thymidine radioactive, et à quel moment ? Cherche quand la radioactivité monte.",
      "dit": "la thymidine radioactive، ف أشمن molécule كتدخل، وفوقاش؟ قلب على الوقت اللي كتطلع فيه la radioactivité."},
     {"texte": "La montée donne la phase S ; avant, G1 ; après, G2 jusqu'au début de la mitose (19 h, d'après les données) ; la mitose finit à la chute (20 h). Puis fais les soustractions.",
      "dit": "الطلعة هي la phase S. قبلها G un. ومن بعدها G deux، حتى تبدا la mitose، à dix-neuf heures. و la mitose كتسالي ملي كتطيح la courbe، à vingt heures. ومن بعد دير les soustractions."}],
   "correction": {"lignes": [
       {"texte": "2 : la thymidine radioactive n'entre que dans l'ADN répliqué : la radioactivité monte en phase S", "mot": "كتدخل غير ف l'A D N"},
       {"texte": "S : 9 – 15 h (6 h) ; G1 : 0 – 9 h (9 h)", "mot": "la phase S، de neuf à quinze heures"},
       {"texte": "G2 : 15 – 19 h (4 h) ; M : 19 – 20 h (1 h)", "mot": "G deux، de quinze à dix-neuf heures"},
       {"texte": "à 20 h, ADN et radioactivité partagés entre deux cellules filles ; cycle = 9 + 6 + 4 + 1 = 20 h", "mot": "le cycle، neuf plus six plus quatre plus un"}],
     "parole": "السؤال deux. la thymidine radioactive كتدخل غير ف l'A D N، ملي كتوقع la réplication. إذن la radioactivité كتطلع غير ف la phase S، de neuf à quinze heures: six heures. قبلها، G un، de zéro à neuf heures: neuf heures. من بعدها، G deux، de quinze à dix-neuf heures: quatre heures. ومن بعد la mitose، de dix-neuf à vingt heures: une heure. à vingt heures، l'A D N و la radioactivité كيتقسمو على les deux cellules filles. le cycle، neuf plus six plus quatre plus un، égale vingt heures."},
   "explication": "ex_s2", "facile": "fa_s2"},
  {"id": "3", "texte": "Les cellules sont observées à 19 h 30 après autoradiographie. Indiquer l'aspect d'un chromosome, puis le justifier par l'état des brins de ses molécules d'ADN.",
   "texte_dit": "السؤال trois: شفنا les cellules à dix-neuf heures trente، من بعد l'autoradiographie. قول كيفاش كيبان le chromosome، وبرر ب les brins ديال les molécules d'A D N ديالو.",
   "reponse": {"type": "phrase", "attendu": "À 19 h 30, la cellule est en mitose : le chromosome est condensé, formé de deux chromatides, et les deux chromatides sont marquées (couvertes de grains noirs). Pendant la phase S, chaque molécule d'ADN s'est répliquée de façon semi-conservative : chaque molécule fille garde un brin ancien non radioactif et reçoit un brin nouveau radioactif. Chaque chromatide contient une de ces molécules : les deux chromatides portent un brin radioactif."},
   "clavier": {"aides": ["deux chromatides", "toutes les deux marquées", "brin ancien", "brin nouveau radioactif", "semi-conservative"], "pieges": ["une chromatide marquée sur deux", "aucune chromatide marquée"]},
   "aides": [
     {"texte": "À 19 h 30, dans quelle phase est la cellule ? Combien de chromatides a chaque chromosome ?",
      "dit": "à dix-neuf heures trente، ف أشمن phase كاينة la cellule؟ وشحال من chromatide ف كل chromosome؟"},
     {"texte": "Dessine une molécule d'ADN avant S (deux brins anciens), puis ses deux molécules filles après S, en mettant en couleur les brins faits avec la thymidine radioactive.",
      "dit": "رسم molécule d'A D N قبل la phase S، avec deux brins anciens. ومن بعد les deux molécules filles، ولون les brins اللي تصاوبو ب la thymidine radioactive."}],
   "correction": {"lignes": [
       {"texte": "3 : à 19 h 30 (mitose) : chromosome condensé, deux chromatides toutes les deux marquées", "mot": "les deux chromatides marquées"},
       {"texte": "en S : chaque molécule fille = un brin ancien non radioactif + un brin nouveau radioactif", "mot": "brin ancien، و brin nouveau radioactif"},
       {"texte": "chaque chromatide contient une molécule à brin radioactif (réplication semi-conservative)", "mot": "réplication semi-conservative"}],
     "parole": "السؤال trois. à dix-neuf heures trente، la cellule ف la mitose: le chromosome condensé، فيه deux chromatides، et les deux chromatides marquées. علاش؟ ف la phase S، كل molécule كتعطي deux molécules: كل وحدة فيها brin ancien، و brin nouveau radioactif. وكل chromatide فيها molécule من هادو: إذن les deux marquées. هادي هي la réplication semi-conservative."},
   "explication": "ex_s3", "facile": "fa_s3"},
  {"id": "4", "texte": "Document 2 : expliquer pourquoi seuls 30 % des noyaux sont marqués, puis calculer la durée de la phase S de ces cellules. Comparer au document 1.",
   "texte_dit": "السؤال quatre: ف le document deux، فسر علاش seulement trente pour cent ديال les noyaux marqués، ومن بعد حسب la durée ديال la phase S، وقارن مع le document un.",
   "reponse": {"type": "valeur", "grandeur": "t(S)", "valeur": TS, "unite": "h", "tolerance": 0.02,
               "attendu": "Pendant le marquage bref, seuls les noyaux en phase S répliquent leur ADN et sont marqués : 30 % des cellules sont en S. t(S) = 30/100 × 20 = 0,3 × 20 = 6 h, la même durée que dans le document 1"},
   "clavier": {"aides": ["seuls les noyaux en phase S", "t(S) = % × durée du cycle", "30/100", "20 h"], "pieges": ["30 × 20", "20/30"]},
   "aides": [
     {"texte": "Le marquage ne dure que 20 minutes : quels noyaux incorporent la thymidine pendant ce temps-là ?",
      "dit": "le marquage dure seulement vingt minutes. شمن noyaux كيدخلو la thymidine ف هاد الوقت؟"},
     {"texte": "Le pourcentage de cellules dans une phase donne sa durée : t(phase) = (% / 100) × durée du cycle.",
      "dit": "la durée d'une phase، égale le pourcentage de cellules dans cette phase، sur cent، fois la durée du cycle."}],
   "correction": {"lignes": [
       {"texte": "4 : marquage bref : seuls les noyaux en phase S sont marqués → 30 % des cellules en S", "mot": "غير les noyaux اللي كانو ف la phase S"},
       {"texte": "t(S) = 30/100 × 20 = 0,3 × 20", "mot": "trente sur cent، fois vingt heures"},
       {"texte": "t(S) = 6 h : la même valeur que le document 1", "mot": "égale six heures"}],
     "parole": "السؤال quatre. pendant vingt minutes، غير les noyaux اللي كانو ف la phase S كيديرو la réplication، وكيوليو marqués: إذن trente pour cent ديال les cellules ف la phase S. t de S، égale trente sur cent، fois vingt heures، égale six heures: نفس la durée ديال le document un."},
   "explication": "ex_s4", "facile": "fa_s4"},
  {"id": "5", "texte": "Après le marquage bref, les cellules sont remises dans un milieu normal. Les premières cellules en mitose ayant des chromosomes marqués n'apparaissent qu'environ 4 h plus tard. Expliquer ce délai.",
   "texte_dit": "السؤال cinq: من بعد le marquage، رجعنا les cellules ل milieu normal. واللول ديال les cellules ف la mitose، اللي عندهم des chromosomes marqués، ما كيبانو غير après environ quatre heures. فسر علاش.",
   "reponse": {"type": "phrase", "attendu": "Seules les cellules qui étaient en phase S pendant le marquage sont marquées. Les plus proches de la mitose étaient à la fin de la phase S : elles doivent encore traverser toute la phase G2, qui dure 4 h, avant d'entrer en mitose. Les cellules déjà en G2 ou en mitose pendant le marquage n'ont pas répliqué leur ADN : leurs mitoses ne sont pas marquées. Le délai de 4 h correspond donc à la durée de G2."},
   "clavier": {"aides": ["fin de la phase S", "traverser G2", "G2 = 4 h", "non marquées"], "pieges": ["durée de G1", "durée de S"]},
   "aides": [
     {"texte": "Parmi les cellules marquées, lesquelles arriveront les premières en mitose : celles du début ou de la fin de la phase S ?",
      "dit": "من بين les cellules marquées، شكون غادي يوصلو اللولين ل la mitose: اللي كانو ف البداية ديال la phase S، ولا ف اللخر ديالها؟"},
     {"texte": "Entre la fin de S et le début de la mitose, quelle phase la cellule doit-elle traverser ? Combien de temps dure-t-elle (question 2) ?",
      "dit": "بين اللخر ديال la phase S و البداية ديال la mitose، شمن phase خاص la cellule تدوز؟ وشحال كتاخد، ف السؤال deux؟"}],
   "correction": {"lignes": [
       {"texte": "5 : seules les cellules en S pendant le marquage sont marquées", "mot": "غير les cellules اللي كانو ف la phase S"},
       {"texte": "les premières à entrer en mitose étaient à la fin de S : elles traversent G2", "mot": "خاصهم يدوزو G deux"},
       {"texte": "délai ≈ durée de G2 = 4 h (les cellules en G2 ou M au marquage ne sont pas marquées)", "mot": "le délai هو la durée ديال G deux"}],
     "parole": "السؤال cinq. غير les cellules اللي كانو ف la phase S، ملي درنا le marquage، هوما اللي marquées. واللي قراب ل la mitose فيهم، كانو ف اللخر ديال la phase S: خاصهم يدوزو G deux كاملة، عاد يدخلو ف la mitose. و G deux dure quatre heures. أما les cellules اللي كانو ف G deux ولا ف la mitose، ما دارو حتى réplication: ماشي marquées. إذن le délai هو la durée ديال G deux، quatre heures."},
   "explication": "ex_s5", "facile": "fa_s5"},
]

EXPLICATION = [
  {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : deux courbes, les mêmes périodes",
   "screen_content": {"lead": "L'ADN : 3 UA, puis 3 → 6 UA de 9 à 15 h, 6 UA, puis 3 UA à 20 h. La radioactivité monte en même temps, de 0 à 8 UA."},
   "visual": {"kind": "simulation", "url": COURBE, "caption": "La quantité d'ADN au cours du cycle de 20 h"},
   "speech_text": {"mixed": "هادي la courbe ديال la quantité d'A D N، ف cycle de vingt heures. ف G un، la quantité ثابتة: trois unités arbitraires. ف la phase S، كتطلع de trois à six: l'A D N كيتضاعف. ف G deux، كتبقى ثابتة، à six. وف اللخر ديال la mitose، à vingt heures، كترجع، à trois. دابا la radioactivité ف التمرين: كتبقى nulle jusqu'à neuf heures، وكتطلع ف نفس الوقت اللي كتطلع فيه هاد la courbe، de zéro à huit. ومن بعد ثابتة، و à vingt heures كتنقص للنص، بحال l'A D N."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "0 – 9 h : ADN 3 UA ; radioactivité 0", "mot": "la quantité ثابتة: trois unités arbitraires"},
                {"texte": "9 – 15 h : ADN 3 → 6 UA ; radioactivité 0 → 8 UA", "mot": "كتطلع de trois à six"},
                {"texte": "20 h : les deux diminuent de moitié", "mot": "كتنقص للنص، بحال l'A D N"}],
     "pointage": [{"mot": "هادي la courbe", "cible": "visuel"},
                  {"mot": "ف G un، la quantité ثابتة", "commande": "play_until", "parametres": {"moment": "g1_q"}},
                  {"mot": "la quantité ثابتة: trois unités arbitraires", "repere": "palier_q"},
                  {"mot": "la quantité ثابتة: trois unités arbitraires", "cible": "centre:0"},
                  {"mot": "ف la phase S", "commande": "play_until", "parametres": {"moment": "debut_s"}},
                  {"mot": "كتطلع de trois à six", "commande": "play_until", "parametres": {"moment": "fin_s_2q"}},
                  {"mot": "كتطلع de trois à six", "repere": "montee"},
                  {"mot": "كتطلع de trois à six", "cible": "centre:1"},
                  {"mot": "ف G deux، كتبقى", "commande": "play_until", "parametres": {"moment": "g2"}},
                  {"mot": "ف G deux، كتبقى", "repere": "palier_2q"},
                  {"mot": "وف اللخر ديال la mitose", "commande": "play_until", "parametres": {"moment": "retour_q"}},
                  {"mot": "وف اللخر ديال la mitose", "repere": "chute"},
                  {"mot": "كتنقص للنص، بحال l'A D N", "cible": "centre:2"}]}},
  {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : la radioactivité monte seulement en phase S",
   "screen_content": {"lead": "G1 9 h (0–9 h), S 6 h (9–15 h), G2 4 h (15–19 h), M 1 h (19–20 h) : cycle de 20 h."},
   "visual": {"kind": "simulation", "url": CYCLE, "caption": "Le cycle de 20 h, phase par phase"},
   "speech_text": {"mixed": "la thymidine radioactive كتدخل غير ف l'A D N، ملي كيتصاوب l'A D N جديد. إذن la radioactivité كتطلع غير ف la phase S. شوف le cycle. G un: de zéro à neuf heures، neuf heures، ما كايناش réplication. la phase S: de neuf à quinze heures، six heures، l'A D N كيتنسخ. G deux: de quinze à dix-neuf heures، quatre heures. et la mitose: de dix-neuf à vingt heures، une heure. ف اللخر، deux cellules filles، كل وحدة كتاخد النص ديال l'A D N، والنص ديال la radioactivité."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "radioactivité ↑ = réplication = phase S", "mot": "كتطلع غير ف la phase S"},
                {"texte": "G1 9 h ; S 6 h ; G2 4 h ; M 1 h", "mot": "de dix-neuf à vingt heures، une heure"},
                {"texte": "20 h : partage entre deux cellules filles", "mot": "deux cellules filles"}],
     "pointage": [{"mot": "كتطلع غير ف la phase S", "cible": "centre:0"},
                  {"mot": "G un: de zéro à neuf heures", "commande": "play_until", "parametres": {"moment": "g1"}},
                  {"mot": "G un: de zéro à neuf heures", "repere": "g1"},
                  {"mot": "la phase S: de neuf à quinze heures", "commande": "play_until", "parametres": {"moment": "s"}},
                  {"mot": "la phase S: de neuf à quinze heures", "repere": "s"},
                  {"mot": "G deux: de quinze à dix-neuf heures", "commande": "play_until", "parametres": {"moment": "g2"}},
                  {"mot": "G deux: de quinze à dix-neuf heures", "repere": "g2"},
                  {"mot": "et la mitose: de dix-neuf", "commande": "play_until", "parametres": {"moment": "mitose"}},
                  {"mot": "et la mitose: de dix-neuf", "repere": "m"},
                  {"mot": "de dix-neuf à vingt heures، une heure", "cible": "centre:1"},
                  {"mot": "deux cellules filles", "commande": "play_until", "parametres": {"moment": "deux_filles"}},
                  {"mot": "deux cellules filles", "cible": "centre:2"}]}},
  {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : après une phase S en milieu radioactif, deux chromatides marquées",
   "screen_content": {"lead": "Chaque molécule fille : un brin ancien + un brin nouveau radioactif → les deux chromatides marquées."},
   "visual": {"kind": "simulation", "url": THY, "caption": "La thymidine radioactive pendant la réplication"},
   "speech_text": {"mixed": "الخلايا ف milieu فيه la thymidine radioactive. la thymidine كتدخل غير ف l'A D N، ملي كتوقع la réplication. شوف la molécule: كل brin ancien، بالزرق، كيولي modèle، وكيتزاد مقابلو brin nouveau radioactif، بالحمر. إذن deux molécules، كل وحدة فيها brin ancien و brin radioactif. وف la mitose، le chromosome فيه deux chromatides، وفيهم بجوج نقط كحلين: les deux chromatides marquées."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "la thymidine radioactive n'entre que dans l'ADN répliqué", "mot": "la thymidine كتدخل غير ف l'A D N"},
                {"texte": "chaque molécule : un brin ancien + un brin radioactif", "mot": "كل وحدة فيها brin ancien و brin radioactif"},
                {"texte": "métaphase : les deux chromatides marquées", "mot": "les deux chromatides marquées"}],
     "pointage": [{"mot": "الخلايا ف milieu", "commande": "play_until", "parametres": {"moment": "milieu_radioactif"}},
                  {"mot": "الخلايا ف milieu", "repere": "milieu"},
                  {"mot": "la thymidine كتدخل غير ف l'A D N", "commande": "play_until", "parametres": {"moment": "regle"}},
                  {"mot": "la thymidine كتدخل غير ف l'A D N", "cible": "centre:0"},
                  {"mot": "شوف la molécule", "commande": "play_until", "parametres": {"moment": "replication_1"}},
                  {"mot": "شوف la molécule", "repere": "molecules"},
                  {"mot": "كل وحدة فيها brin ancien و brin radioactif", "cible": "centre:1"},
                  {"mot": "وف la mitose", "commande": "play_until", "parametres": {"moment": "metaphase_1"}},
                  {"mot": "les deux chromatides marquées", "repere": "chromatide_marquee"},
                  {"mot": "les deux chromatides marquées", "cible": "centre:2"}]}},
  {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : le pourcentage de cellules donne la durée de la phase",
   "screen_content": {"lead": "Marquage bref : seuls les noyaux en S sont marqués. t(S) = 30/100 × 20 h = 6 h."},
   "visual": {"kind": "simulation", "url": DUREES, "caption": "Les cellules triées par phase, puis les durées"},
   "speech_text": {"mixed": "ف le marquage bref، غير les noyaux اللي كيديرو la réplication، يعني اللي ف la phase S، كيوليو marqués. إذن le pourcentage ديال les noyaux marqués، هو le pourcentage ديال les cellules ف la phase S. شوف: الخلايا مقسمة على les phases. la relation: la durée d'une phase، égale le pourcentage de cellules dans cette phase، sur cent، fois la durée du cycle. هنا، la phase S: six cellules sur vingt، trente pour cent، six heures. ف التمرين: trente sur cent، fois vingt heures، égale six heures."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "noyaux marqués = cellules en S (30 %)", "mot": "هو le pourcentage ديال les cellules ف la phase S"},
                {"texte": "t(phase) = (% / 100) × durée du cycle", "mot": "la durée d'une phase، égale le pourcentage"},
                {"texte": "t(S) = 30/100 × 20 = 6 h", "mot": "fois vingt heures، égale six heures"}],
     "pointage": [{"mot": "ف le marquage bref", "commande": "set_time", "parametres": {"time_s": 19.6}},
                  {"mot": "هو le pourcentage ديال les cellules ف la phase S", "cible": "centre:0"},
                  {"mot": "شوف: الخلايا مقسمة", "commande": "play_until", "parametres": {"moment": "pourcentages"}},
                  {"mot": "la durée d'une phase، égale le pourcentage", "commande": "play_until", "parametres": {"moment": "duree_g1"}},
                  {"mot": "la durée d'une phase، égale le pourcentage", "cible": "centre:1"},
                  {"mot": "هنا، la phase S", "commande": "play_until", "parametres": {"moment": "duree_s"}},
                  {"mot": "fois vingt heures، égale six heures", "cible": "centre:2"}]}},
  {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : de la fin de S à la mitose, il faut traverser G2",
   "screen_content": {"lead": "Une cellule marquée à la fin de S traverse G2 (4 h) avant la mitose : premier délai ≈ 4 h."},
   "visual": {"kind": "simulation", "url": CYCLE, "caption": "Le point du cycle part de la fin de la phase S"},
   "speech_text": {"mixed": "خود cellule كانت ف اللخر ديال la phase S ملي درنا le marquage: هاد النقطة، à quinze heures. هي marquée. باش توصل ل la mitose، خاصها تدوز G deux كاملة: de quinze à dix-neuf heures. soit quatre heures. عاد كتدخل ف la mitose، à dix-neuf heures، و les chromosomes ديالها marqués. أما les cellules اللي كانو ف G deux، ما دارو حتى réplication ف le marquage: ماشي marquées. إذن le délai هو la durée ديال G deux، quatre heures."},
   "concentration": {"demarrer": "reset",
     "centre": [{"texte": "marquée à la fin de S (15 h)", "mot": "هاد النقطة، à quinze heures"},
                {"texte": "elle traverse G2 : 15 h → 19 h = 4 h", "mot": "soit quatre heures"},
                {"texte": "délai des premières mitoses marquées = durée de G2", "mot": "إذن le délai هو la durée ديال G deux"}],
     "pointage": [{"mot": "هاد النقطة، à quinze heures", "commande": "set_parameters", "parametres": {"t_h": 15}},
                  {"mot": "هاد النقطة، à quinze heures", "repere": "s"},
                  {"mot": "هاد النقطة، à quinze heures", "cible": "centre:0"},
                  {"mot": "خاصها تدوز G deux كاملة", "commande": "play_until", "parametres": {"moment": "g2"}},
                  {"mot": "خاصها تدوز G deux كاملة", "repere": "g2"},
                  {"mot": "soit quatre heures", "cible": "centre:1"},
                  {"mot": "عاد كتدخل ف la mitose", "commande": "play_until", "parametres": {"moment": "mitose"}},
                  {"mot": "عاد كتدخل ف la mitose", "repere": "m"},
                  {"mot": "إذن le délai هو la durée ديال G deux", "cible": "centre:2"}]}},
]

FACILE = [
  vrai_faux("fa_s1", "Plus facile : lire les deux courbes", "Vrai ou faux : les documents 1a et 1b.",
    "سؤال ساهل: صحيح ولا غالط، على les deux courbes.",
    [("De 0 à 9 h, la radioactivité des cellules reste nulle.", True, "Oui : pas de réplication, la thymidine n'entre pas dans l'ADN."),
     ("La radioactivité augmente de 9 h à 15 h, en même temps que la quantité d'ADN double.", True, "Oui : de 0 à 8 UA pendant que l'ADN passe de 3 à 6 UA."),
     ("À 20 h, la radioactivité par cellule double.", False, "Non : elle diminue de moitié (8 → 4 UA), comme l'ADN (6 → 3 UA) : partage entre deux cellules filles.")]),
  association("fa_s2", "Plus facile : chaque phase et sa durée", "Relie chaque phase à sa durée.",
    "سؤال ساهل: ربط كل phase مع la durée ديالها.",
    "Relie chaque phase du cycle (document 1) à sa durée.",
    [("1", "G1"), ("2", "S"), ("3", "G2"), ("4", "M (mitose)")],
    [("a", "9 h"), ("b", "6 h"), ("c", "4 h"), ("d", "1 h"), ("e", "20 h")],
    {"1": "a", "2": "b", "3": "c", "4": "d"},
    {**{f"1-{d}": (d == "a", "Oui : G1 va de 0 à 9 h, soit 9 h." if d == "a" else "Non : G1 va de 0 h au début de la montée (9 h).",
                   "برافو: G un، de zéro à neuf heures: neuf heures." if d == "a" else "لا، G un كتبدا à zéro، وكتسالى ملي كتبدا الطلعة، à neuf heures.") for d in "abcde"},
     **{f"2-{d}": (d == "b", "Oui : S va de 9 à 15 h, soit 6 h." if d == "b" else "Non : S correspond à la montée de la radioactivité, de 9 à 15 h.",
                   "برافو: la phase S، de neuf à quinze heures: six heures." if d == "b" else "لا، la phase S هي الطلعة ديال la radioactivité، de neuf à quinze heures.") for d in "abcde"},
     **{f"3-{d}": (d == "c", "Oui : G2 va de 15 à 19 h, soit 4 h." if d == "c" else "Non : G2 va de la fin de S (15 h) au début de la mitose (19 h).",
                   "برافو: G deux، de quinze à dix-neuf heures: quatre heures." if d == "c" else "لا، G deux من اللخر ديال la phase S، à quinze heures، حتى تبدا la mitose، à dix-neuf heures.") for d in "abcde"},
     **{f"4-{d}": (d == "d", "Oui : la mitose va de 19 à 20 h, soit 1 h." if d == "d" else "Non : la mitose va de 19 h à 20 h ; 20 h, c'est tout le cycle." if d == "e" else "Non : la mitose va de 19 h à 20 h.",
                   "برافو: la mitose، de dix-neuf à vingt heures: une heure." if d == "d" else "لا، vingt heures هي le cycle كامل. la mitose، de dix-neuf à vingt heures." if d == "e" else "لا، la mitose، de dix-neuf à vingt heures.") for d in "abcde"}},
    ("(1 ; a) (2 ; b) (3 ; c) (4 ; d) : 9 + 6 + 4 + 1 = 20 h, la durée du cycle (e).", "الجواب: G un neuf heures، S six heures، G deux quatre heures، et la mitose une heure. le total، vingt heures، c'est le cycle.")),
  qcm_facile("fa_s3", "Plus facile : le chromosome à 19 h 30", "سؤال ساهل: كيفاش كيبان le chromosome à dix-neuf heures trente؟",
    "À 19 h 30, après une phase S en milieu radioactif, le chromosome observé a…",
    ["une seule chromatide marquée sur deux", "deux chromatides, toutes les deux marquées", "deux chromatides non marquées"], 1, {
      "1": {"juste": rep("برافو! كل molécule فيها brin ancien و brin radioactif، إذن les deux chromatides marquées.", "Juste : chaque chromatide a une molécule avec un brin radioactif.")},
      "0": {"1": rep("قريب! une seule chromatide marquée كتكون من بعد un deuxième cycle ف milieu normal. هنا، la réplication الوحيدة كانت ف milieu radioactif. عاود اختار.", "Une chromatide sur deux, c'est après un second cycle en milieu normal. Ici, la seule réplication s'est faite en milieu radioactif. Réessaie."),
            "2": rep("الجواب: les deux chromatides marquées. كل molécule خدات brin nouveau radioactif.", "Réponse : deux chromatides, toutes les deux marquées.")},
      "2": {"1": rep("لا، la réplication وقعات ف milieu radioactif: les brins nouveaux فيهم la thymidine radioactive. عاود اختار.", "La réplication a eu lieu en milieu radioactif : les brins nouveaux sont radioactifs. Réessaie."),
            "2": rep("الجواب: les deux chromatides marquées.", "Réponse : deux chromatides, toutes les deux marquées.")}},
    "À dix-neuf heures trente, le chromosome a ?"),
  qcm_facile("fa_s4", "Plus facile : la relation de la durée", "سؤال ساهل: اختار la relation.",
    "30 % des noyaux sont en phase S, le cycle dure 20 h. La durée de S est…",
    ["t(S) = 30 × 20 = 600 h", "t(S) = 20/30 h", "t(S) = 30/100 × 20 = 6 h"], 2, {
      "2": {"juste": rep("برافو! trente sur cent، fois vingt heures، égale six heures.", "Juste : t(S) = 0,3 × 20 = 6 h.")},
      "0": {"1": rep("لا، six cents heures كبر من le cycle كامل! le pourcentage خاصو يتقسم على cent. عاود اختار.", "600 h, c'est plus que tout le cycle ! Le pourcentage se divise par 100. Réessaie."),
            "2": rep("الجواب: trente sur cent، fois vingt، égale six heures.", "Réponse : t(S) = 30/100 × 20 = 6 h.")},
      "1": {"1": rep("لا، هادي قسمة مقلوبة. la durée ديال phase هي جزء من le cycle: le pourcentage fois la durée du cycle. عاود اختار.", "C'est une division sans sens ici : la durée d'une phase = pourcentage × durée du cycle. Réessaie."),
            "2": rep("الجواب: trente sur cent، fois vingt، égale six heures.", "Réponse : t(S) = 30/100 × 20 = 6 h.")}},
    "La durée de la phase S est ?"),
  qcm_facile("fa_s5", "Plus facile : le délai de 4 h", "سؤال ساهل: le délai ديال quatre heures شنو هو؟",
    "Le délai d'environ 4 h avant les premières mitoses marquées correspond à la durée de…",
    ["la phase G1", "la phase G2", "la phase S"], 1, {
      "1": {"juste": rep("برافو! cellule ف اللخر ديال la phase S خاصها تدوز G deux، quatre heures، عاد تدخل ف la mitose.", "Juste : de la fin de S à la mitose, il faut traverser G2 (4 h).")},
      "0": {"1": rep("لا، G un كاينة قبل la phase S، ماشي من بعدها. شنو كاين بين S و la mitose؟ عاود اختار.", "G1 est avant S. Qu'y a-t-il entre S et la mitose ? Réessaie."),
            "2": rep("الجواب: G deux. G un كاينة قبل la phase S.", "Réponse : G2 ; G1 est avant S.")},
      "2": {"1": rep("قريب، les cellules marquées كانو ف la phase S. ولكن من بعد S، شمن phase كتجي قبل la mitose؟ عاود اختار.", "Les cellules marquées étaient en S ; mais après S, quelle phase vient avant la mitose ? Réessaie."),
            "2": rep("الجواب: G deux. la phase S dure six heures، et non quatre.", "Réponse : G2 ; S dure 6 h, pas 4.")}},
    "Le délai de quatre heures correspond à quelle phase ?"),
]

# ---- exercice semblable : autres cellules, cycle de 16 h (G1 6 h, S 6 h, G2 3 h, M 1 h), q = 2 UA
C2 = {"G1": 6, "S": 6, "G2": 3, "M": 1, "q": 2, "r": 6, "xmax": 20}
CYC2 = 16
PCT2 = 37.5
assert C2["G1"] + C2["S"] + C2["G2"] + C2["M"] == CYC2 and PCT2 / 100 * CYC2 == 6
SIM_Q = [
  {"id": "1", "texte": "Décrire l'évolution de la radioactivité des cellules (document 1b) en la comparant à celle de la quantité d'ADN (document 1a).",
   "reponse": {"type": "phrase", "attendu": "De 0 à 6 h, radioactivité nulle, ADN constant à 2 UA. De 6 à 12 h, la radioactivité augmente de 0 à 6 UA pendant que l'ADN double de 2 à 4 UA. De 12 à 16 h, les deux restent constantes. À 16 h, les deux diminuent de moitié (6 → 3 UA ; 4 → 2 UA), puis restent constantes."},
   "clavier": {"aides": ["reste nulle", "augmente", "diminue de moitié"], "pieges": ["augmente en G1"]},
   "correction": {"lignes": [{"texte": "1 : 0 – 6 h : radioactivité nulle ; ADN 2 UA", "mot": "nulle"},
                             {"texte": "6 – 12 h : radioactivité 0 → 6 UA, ADN 2 → 4 UA ; 12 – 16 h : constantes", "mot": "de zéro à six"},
                             {"texte": "16 h : les deux diminuent de moitié", "mot": "للنص"}],
                  "parole": "de zéro à six heures: la radioactivité nulle. de six à douze heures: كتطلع de zéro à six، و l'A D N de deux à quatre. et à seize heures: les deux كينقصو للنص."}},
  {"id": "2", "texte": "Expliquer les variations de la radioactivité, puis en déduire les limites et la durée de chacune des phases G1, S, G2 et M de ce cycle.",
   "reponse": {"type": "phrase", "attendu": "La thymidine radioactive n'entre que dans l'ADN répliqué : la radioactivité monte en phase S, de 6 à 12 h (6 h). G1 : 0 – 6 h (6 h). G2 : 12 – 15 h (3 h). M : 15 – 16 h (1 h) ; à 16 h, partage entre deux cellules filles. Cycle : 6 + 6 + 3 + 1 = 16 h."},
   "clavier": {"aides": ["phase S", "G2 = 3 h", "16 h"], "pieges": ["G2 = 4 h"]},
   "correction": {"lignes": [{"texte": "2 : S : 6 – 12 h (6 h) ; G1 : 0 – 6 h (6 h)", "mot": "la phase S"},
                             {"texte": "G2 : 12 – 15 h (3 h) ; M : 15 – 16 h (1 h) ; cycle = 16 h", "mot": "seize heures"}],
                  "parole": "la radioactivité كتطلع غير ف la phase S، de six à douze heures. G un، six heures. G deux، trois heures. la mitose، une heure. le cycle، seize heures."}},
  {"id": "3", "texte": "Les cellules sont observées à 15 h 30 après autoradiographie. Indiquer l'aspect d'un chromosome, puis le justifier par l'état des brins de ses molécules d'ADN.",
   "reponse": {"type": "phrase", "attendu": "À 15 h 30 (mitose), le chromosome a deux chromatides, toutes les deux marquées : en S, chaque molécule fille a gardé un brin ancien non radioactif et reçu un brin nouveau radioactif (réplication semi-conservative)."},
   "clavier": {"aides": ["deux chromatides marquées", "brin nouveau radioactif"], "pieges": ["une chromatide marquée sur deux"]},
   "correction": {"lignes": [{"texte": "3 : deux chromatides, toutes les deux marquées", "mot": "les deux chromatides marquées"},
                             {"texte": "chaque molécule : un brin ancien + un brin radioactif", "mot": "brin radioactif"}],
                  "parole": "le chromosome فيه deux chromatides، et les deux chromatides marquées: كل molécule فيها brin ancien و brin radioactif."}},
  {"id": "4", "texte": "Document 2 : expliquer pourquoi seuls 37,5 % des noyaux sont marqués, puis calculer la durée de la phase S de ces cellules. Comparer au document 1.",
   "reponse": {"type": "valeur", "grandeur": "t(S)", "valeur": 6, "unite": "h", "tolerance": 0.02,
               "attendu": "Seuls les noyaux en phase S sont marqués : 37,5 % des cellules sont en S. t(S) = 37,5/100 × 16 = 0,375 × 16 = 6 h, comme dans le document 1"},
   "clavier": {"aides": ["t(S) = % × durée du cycle", "16 h"], "pieges": ["37,5 × 16"]},
   "correction": {"lignes": [{"texte": "4 : noyaux marqués = cellules en S (37,5 %)", "mot": "la phase S"},
                             {"texte": "t(S) = 37,5/100 × 16 = 6 h", "mot": "égale six heures"}],
                  "parole": "غير les noyaux ف la phase S marqués. t de S، égale trente-sept virgule cinq sur cent، fois seize heures، égale six heures."}},
  {"id": "5", "texte": "Après le marquage bref, les cellules sont remises dans un milieu normal. Les premières cellules en mitose ayant des chromosomes marqués n'apparaissent qu'environ 3 h plus tard. Expliquer ce délai.",
   "reponse": {"type": "phrase", "attendu": "Les cellules marquées les plus proches de la mitose étaient à la fin de S : elles doivent traverser G2 (3 h) avant la mitose ; celles en G2 ou en M au marquage ne sont pas marquées. Le délai correspond à la durée de G2."},
   "clavier": {"aides": ["fin de S", "G2 = 3 h"], "pieges": ["durée de G1"]},
   "correction": {"lignes": [{"texte": "5 : marquées à la fin de S → traversent G2", "mot": "G deux"},
                             {"texte": "délai = durée de G2 = 3 h", "mot": "trois heures"}],
                  "parole": "les cellules ف اللخر ديال la phase S خاصهم يدوزو G deux، عاد يدخلو ف la mitose: le délai هو la durée ديال G deux، trois heures."}},
]

INTRO = ("Des cellules animales en culture sont synchronisées : à t = 0, elles commencent toutes la phase G1 de leur cycle. On ajoute alors au milieu "
         "de la thymidine radioactive, un constituant des nucléotides de l'ADN (elle reste dans le milieu pendant toute l'expérience). On mesure "
         "au cours du temps la quantité d'ADN et la radioactivité d'une cellule (documents 1a et 1b) ; des chromosomes condensés sont observés de 19 h "
         "à 20 h. Document 2 : dans une autre culture des mêmes cellules, non synchronisée (cellules réparties dans toutes les phases, cycle de 20 h), "
         "on ajoute la thymidine radioactive pendant 20 minutes seulement, puis on fait aussitôt une autoradiographie : 30 % des noyaux sont marqués.")
INTRO_DIT = ("دابا نقراو l'énoncé. خلايا ف culture، كلهم بداو G un ف نفس الوقت، ف t égale zéro. زدنا ف le milieu la thymidine radioactive، "
             "وهي جزء من les nucléotides ديال l'A D N، وبقات ف le milieu طول التجربة. قسنا la quantité d'A D N، و la radioactivité ديال la cellule، "
             "ف le document un a، و le document un b. و les chromosomes condensés كيبانو de dix-neuf à vingt heures. ف le document deux: "
             "culture أخرى، الخلايا ف كل les phases، و le cycle de vingt heures. زدنا la thymidine radioactive pendant vingt minutes seulement، ومن بعد "
             "l'autoradiographie: trente pour cent ديال les noyaux marqués.")

EX = {
  "id": "svt_ex_ch3_thymidine_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "notion_information_genetique", "cours": "svt_ch3_notion_information_genetique",
  "titre": "Thymidine radioactive : repérer la phase S et mesurer le cycle", "niveau": "difficile", "duree_min": 40,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire deux courbes en parallèle", "Situer la réplication en phase S et calculer la durée des phases",
                  "Relier le marquage aux brins et aux chromatides", "Calculer la durée d'une phase par un pourcentage",
                  "Expliquer un délai par la durée de G2"],
  "enonce": {
    "intro": INTRO, "intro_dit": INTRO_DIT,
    "figures": courbes(C1),
    "donnees": ["Culture synchronisée : toutes les cellules commencent G1 à t = 0", "Chromosomes condensés (mitose) observés de 19 h à 20 h",
                "Document 2 (culture non synchronisée, cycle de 20 h) : marquage de 20 min → 30 % de noyaux marqués",
                "Durée d'une phase = (% de cellules dans la phase / 100) × durée du cycle"],
    "questions": Q},
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": EXPLICATION}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": FACILE}]},
  "similaire": {"id": "svt_ex_ch3_thymidine_1_b", "titre": "Même exercice, autres données", "enonce": {
    "intro": ("Même protocole avec d'autres cellules : culture synchronisée au début de G1 à t = 0, thymidine radioactive dans le milieu pendant toute "
              "l'expérience (documents 1a et 1b) ; chromosomes condensés observés de 15 h à 16 h. Document 2 : culture non synchronisée des mêmes "
              "cellules (cycle de 16 h), marquage de 20 minutes puis autoradiographie : 37,5 % des noyaux sont marqués."),
    "intro_dit": "نفس البروتوكول ب خلايا أخرى. les chromosomes condensés كيبانو de quinze à seize heures. و ف le document deux، le cycle de seize heures، et trente-sept virgule cinq pour cent ديال les noyaux marqués.",
    "figures": courbes(C2, " (autres cellules)"),
    "donnees": ["Chromosomes condensés observés de 15 h à 16 h", "Document 2 (cycle de 16 h) : 37,5 % de noyaux marqués"],
    "questions": SIM_Q}},
}

if __name__ == "__main__":
    ecrire(EX, sys.argv[1])
