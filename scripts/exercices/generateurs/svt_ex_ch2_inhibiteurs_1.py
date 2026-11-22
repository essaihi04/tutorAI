# Exercice SVT ch. 2 (rôle du muscle strié squelettique), niveau difficile (« Supérieur ») : voies bloquées, sans dioxygène.
# Ce qu'il entraîne : justifier un protocole (milieu sans dioxygène = respiration exclue), comparer chaque muscle au témoin
# ligne par ligne avec les valeurs, expliquer un ATP constant (régénéré aussi vite que consommé), dire pour chaque muscle
# quelle voie est bloquée et laquelle prend le relais (réaction / équation), PRÉVOIR les résultats d'un muscle aux deux
# voies bloquées et l'évolution du muscle à glycolyse bloquée si la série se prolonge : raisonnement en plusieurs étapes,
# deux notions combinées (voies de régénération + conditions de chaque voie).
# Sources comparées (lecture seulement, rien de copié) :
# - exploration du cours : cas_types « inhibiteurs » (2020 R, 2021 R : « comparer chaque muscle au témoin, ligne par ligne ;
#   dire quelle voie est bloquée et laquelle prend le relais »), « voies_equations », « hypothese » ; pièges « anaérobie ≠
#   fermentation », « équations sans ADP + Pi », « ATP synthase pour la créatine kinase » ; exclus_hors_programme vérifiés ;
# - diapositive du cours ms_r8_inhibiteurs (inhibiteurs.html, d'après 2020 R) : témoin, glycolyse bloquée, glycolyse et
#   créatine kinase bloquées ;
# - nationaux : 2020 R ex. 1 (trois muscles : témoin, glycolyse bloquée, glycolyse + kinase bloquées ; ATP et
#   phosphocréatine avant / après, durée de contraction), 2021 R (cyanure) : NOTRE situation est différente : milieu sans
#   dioxygène, un muscle à créatine kinase SEULE bloquée (absent du national), acide lactique dosé, et le muscle aux deux
#   voies bloquées n'est pas donné : il est à PRÉVOIR ; autres valeurs, bilan d'ATP cohérent (14 µmol/g dans les trois) ;
# - séries en ligne : recherche du 22/11/2026 (« iodoacétate phosphocréatine exercice ») : seuls les extraits des résultats
#   ont pu être lus (moutamadris.ma, dreamjob.ma bloqués par le réseau de la session) : expérience classique du muscle de
#   grenouille à l'iodoacétate (glycolyse bloquée : phosphocréatine qui chute, ATP stable) ; rien copié.
# Cohérence du document : 30 excitations consomment 14 µmol d'ATP par g dans chaque muscle ; 1 ATP par phosphocréatine,
# 1 ATP par acide lactique (2 ATP et 2 acides lactiques par glucose) : témoin 6 + 8 ; muscle 2 : 14 + 0 ; muscle 3 : 0 + 14.
import sys
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

D = "/media/simulations/svt/role_muscle_strie_squelettique-tableau/"
INHIB = D + "inhibiteurs.html"
VOIES = D + "voies.html?attente=1"
CHAL = D + "chaleur.html?attente=1"


def fv(x):
    return str(int(x)) if float(x).is_integer() else f"{x:.1f}".replace(".", ",")


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


def doc(m, n):
    """m : {muscle: (atp, (pc avant, pc après), (lac avant, lac après))} ; n excitations."""
    fl = lambda a, b: f"{fv(a)} → {fv(b)}"
    cols = ["temoin", "iodo", "ck"]
    return tableau("Document : dosages avant → après la série d'excitations",
                   f"Teneurs en µmol par g de muscle, avant → après la série de {n} excitations, en milieu sans dioxygène. CK : créatine kinase.",
                   ["", "Muscle 1\n(témoin)", "Muscle 2\n(iodoacétate)", "Muscle 3\n(CK bloquée)"],
                   [["ATP"] + [f"{m[c][0]:.1f} → {m[c][0]:.1f}".replace(".", ",") for c in cols],
                    ["Phosphocréatine"] + [fl(*m[c][1]) for c in cols],
                    ["Acide lactique"] + [fl(*m[c][2]) for c in cols],
                    ["Contractions"] + [f"{n} normales"] * 3],
                   [3.0, 2.8, 2.8, 2.8])


M = {"temoin": (3.0, (20, 14), (1, 9)), "iodo": (3.0, (20, 6), (1, 1)), "ck": (3.0, (20, 20), (1, 15))}
MB = {"temoin": (4.0, (25, 20), (1, 8)), "iodo": (4.0, (25, 13), (1, 1)), "ck": (4.0, (25, 25), (1, 13))}
for d in (M, MB):  # même ATP régénéré dans les trois muscles : PC consommée + acide lactique produit
    tot = [(v[1][0] - v[1][1]) + (v[2][1] - v[2][0]) for v in d.values()]
    assert len(set(tot)) == 1, tot
assert (M["iodo"][2][1] - M["iodo"][2][0]) == 0 and M["ck"][1][0] == M["ck"][1][1]

EQ_PC = "PC + ADP → C + ATP"
EQ_FL = "C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP"

EX = {
  "id": "svt_ex_ch2_inhibiteurs_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "role_muscle_strie_squelettique", "cours": "svt_ch2_role_muscle_strie_squelettique",
  "titre": "Sans dioxygène, une voie bloquée : laquelle prend le relais ?", "niveau": "difficile", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Justifier un protocole expérimental", "Comparer des résultats à un témoin",
                  "Expliquer la régénération de l'ATP quand une voie est bloquée", "Prévoir le résultat d'une expérience"],
  "enonce": {
    "intro": "Trois muscles gastrocnémiens de grenouille, isolés et identiques, sont placés dans un liquide physiologique privé de dioxygène. Avant l'expérience, le muscle 1 ne reçoit aucun traitement (témoin) ; le muscle 2 est traité par l'iodoacétate, une substance qui bloque la glycolyse ; le muscle 3 est traité par une substance qui bloque la créatine kinase. Chaque muscle reçoit ensuite la même série de 30 excitations efficaces. On dose l'ATP, la phosphocréatine et l'acide lactique avant et après la série (document).",
    "intro_dit": "دابا نقراو l'énoncé. trois muscles ديال la grenouille، حاطينهم ف liquide بلا dioxygène. le muscle un، le témoin، ما درنا ليه والو. le muscle deux، عطيناه l'iodoacétate: واحد la substance اللي كتسد la glycolyse. le muscle trois، عطيناه substance اللي كتسد la créatine kinase. ومن بعد، كل muscle كياخد la même série de trente excitations. كنقيسو l'A T P، la phosphocréatine و l'acide lactique، قبل ومن بعد la série.",
    "figures": [doc(M, 30)],
    "donnees": ["Milieu privé de dioxygène pour les trois muscles",
                "Iodoacétate : bloque la glycolyse (première étape de la dégradation du glucose)",
                "Muscle 3 : la créatine kinase est bloquée",
                "Teneurs en µmol par g de muscle"],
    "questions": [
      {"id": "1", "texte": "Justifier le choix d'un milieu privé de dioxygène pour cette expérience.",
       "texte_dit": "Question un : برر علاش اخترنا milieu بلا dioxygène ف هاد التجربة.",
       "reponse": {"type": "phrase", "attendu": "Sans dioxygène, la respiration (voie aérobie) est impossible. Seules les voies anaérobies peuvent alors régénérer l'ATP : la voie de la phosphocréatine (anaérobie alactique) et la fermentation lactique (anaérobie lactique). On peut ainsi étudier ces deux voies seules, et l'effet de chaque inhibiteur sur elles."},
       "clavier": {"aides": ["respiration impossible", "voie aérobie", "voies anaérobies", "phosphocréatine", "fermentation lactique"], "pieges": ["sans dioxygène, pas de contraction", "la fermentation a besoin de dioxygène"]},
       "aides": [
         {"texte": "Parmi les trois voies de régénération de l'ATP, laquelle a besoin de dioxygène ?",
          "dit": "من بين les trois voies ديال la régénération ديال l'A T P، شمن وحدة محتاجة le dioxygène؟"},
         {"texte": "Sans dioxygène, il ne reste que les voies anaérobies : lesquelles ? Que peut-on alors étudier seul ?",
          "dit": "بلا dioxygène، كيبقاو غير les voies anaérobies. شمن هوما؟ وشنو نقدرو نقراو بوحدو؟"}],
       "correction": {"lignes": [
           {"texte": "1 : sans dioxygène, la respiration (voie aérobie) est impossible", "mot": "la respiration ما تقدرش تخدم"},
           {"texte": "seules les voies anaérobies régénèrent l'ATP : phosphocréatine et fermentation lactique", "mot": "كيبقاو غير les voies anaérobies"},
           {"texte": "on étudie ces deux voies seules et l'effet de chaque inhibiteur", "mot": "نقراو هاد les voies بوحدهم"}],
         "parole": "Question un. بلا dioxygène، la respiration ما تقدرش تخدم: هي la voie aérobie. كيبقاو غير les voies anaérobies: la voie de la phosphocréatine، و la fermentation lactique. هكا نقراو هاد les voies بوحدهم، ونشوفو شنو كيدير كل inhibiteur."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Comparer les résultats du muscle 2, puis ceux du muscle 3, avec ceux du muscle témoin.",
       "texte_dit": "Question deux : قارن les résultats ديال le muscle deux، ومن بعد ديال le muscle trois، مع le muscle témoin.",
       "reponse": {"type": "phrase", "attendu": "Muscle 2 / témoin : même nombre de contractions (30) et ATP constant (3,0 µmol/g) dans les deux ; la phosphocréatine diminue beaucoup plus dans le muscle 2 (20 → 6 µmol/g contre 20 → 14) ; l'acide lactique ne change pas dans le muscle 2 (1 → 1) alors qu'il augmente dans le témoin (1 → 9). Muscle 3 / témoin : mêmes contractions et ATP constant ; la phosphocréatine ne change pas dans le muscle 3 (20 → 20) alors qu'elle diminue dans le témoin ; l'acide lactique augmente davantage dans le muscle 3 (1 → 15 contre 1 → 9 µmol/g)."},
       "clavier": {"aides": ["contre", "alors que", "diminue beaucoup plus", "ne change pas", "augmente davantage"], "pieges": ["l'ATP diminue", "moins de contractions"]},
       "aides": [
         {"texte": "Compare ligne par ligne : ATP, phosphocréatine, acide lactique, contractions ; toujours le muscle traité face au témoin.",
          "dit": "قارن سطر ب سطر: l'A T P، la phosphocréatine، l'acide lactique، les contractions. ديما le muscle المعالج قدام le témoin."},
         {"texte": "Pour chaque ligne, écris les deux évolutions avec leurs valeurs : « … alors que … » ou « … contre … ».",
          "dit": "ف كل سطر، كتب جوج التطورات ب les valeurs ديالهم، ب alors que، ولا ب contre."}],
       "correction": {"lignes": [
           {"texte": "2 : dans les trois muscles : 30 contractions, ATP constant (3,0 µmol/g)", "mot": "l'A T P بقا ثابت"},
           {"texte": "muscle 2 : PC 20 → 6 contre 20 → 14 ; acide lactique 1 → 1 contre 1 → 9", "mot": "le muscle deux"},
           {"texte": "muscle 3 : PC 20 → 20 contre 20 → 14 ; acide lactique 1 → 15 contre 1 → 9", "mot": "le muscle trois"}],
         "parole": "Question deux. ف les trois muscles، trente contractions، و l'A T P بقا ثابت، à trois micromoles par gramme. le muscle deux: la phosphocréatine نقصات بزاف، de vingt à six، contre de vingt à quatorze ف le témoin. و l'acide lactique ما تبدلش، alors que dans le témoin il passe de un à neuf. le muscle trois: la phosphocréatine ما تبدلاتش، alors que dans le témoin elle diminue. و l'acide lactique طلع أكثر، de un à quinze، contre de un à neuf."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "L'ATP reste constant dans les trois muscles, alors qu'ils se sont contractés. Expliquer ce résultat, puis préciser pour chaque muscle la ou les voies qui ont régénéré l'ATP, avec la réaction ou l'équation correspondante.",
       "texte_dit": "Question trois : l'A T P بقا ثابت ف les trois muscles، واخا تقلصو. شرح علاش، ومن بعد قول ف كل muscle شمن voie ولا voies جددو l'A T P، مع la réaction ولا l'équation.",
       "reponse": {"type": "phrase", "attendu": "Chaque contraction consomme de l'ATP ; s'il reste constant, c'est qu'il est régénéré aussi vite qu'il est consommé. Muscle 1 (témoin) : par les deux voies anaérobies : la voie de la phosphocréatine, PC + ADP → C + ATP (créatine kinase), qui baisse un peu, et la fermentation lactique, C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP, qui produit l'acide lactique. Muscle 2 : la glycolyse bloquée empêche la fermentation lactique (pas d'acide lactique) : l'ATP est régénéré par la seule voie de la phosphocréatine, qui baisse donc beaucoup plus. Muscle 3 : la créatine kinase bloquée empêche l'utilisation de la phosphocréatine (constante) : l'ATP est régénéré par la seule fermentation lactique, qui produit donc plus d'acide lactique."},
       "clavier": {"aides": ["régénéré aussi vite qu'il est consommé", EQ_PC, EQ_FL, "glycolyse bloquée", "créatine kinase bloquée"], "pieges": ["respiration", "ATP synthase"]},
       "aides": [
         {"texte": "Un ATP constant malgré la consommation : il est remplacé. Puis, pour chaque muscle, regarde ce qui baisse (phosphocréatine) et ce qui monte (acide lactique).",
          "dit": "l'A T P ثابت واخا كيتستهلك: إذن كيتعوض. ومن بعد، ف كل muscle، شوف شنو كينقص، la phosphocréatine، وشنو كيطلع، l'acide lactique."},
         {"texte": "Phosphocréatine qui baisse = voie anaérobie alactique ; acide lactique qui monte = fermentation lactique. La glycolyse est la première étape de la fermentation ; la créatine kinase est l'enzyme de PC + ADP → C + ATP.",
          "dit": "la phosphocréatine كتنقص، يعني la voie anaérobie alactique. l'acide lactique كيطلع، يعني la fermentation lactique. la glycolyse هي البداية ديال la fermentation، و la créatine kinase هي l'enzyme ديال la phosphocréatine."}],
       "correction": {"lignes": [
           {"texte": "3 : ATP consommé mais constant : régénéré aussi vite qu'il est consommé", "mot": "كيتجدد ب نفس السرعة"},
           {"texte": "muscle 1 : " + EQ_PC + " et " + EQ_FL, "mot": "le muscle un"},
           {"texte": "muscle 2 : glycolyse bloquée → pas de fermentation : phosphocréatine seule (baisse forte)", "mot": "le muscle deux"},
           {"texte": "muscle 3 : créatine kinase bloquée → PC constante : fermentation lactique seule (plus d'acide lactique)", "mot": "le muscle trois"}],
         "parole": "Question trois. كل contraction كتستهلك l'A T P. يلا بقا ثابت، إذن كيتجدد ب نفس السرعة اللي كيتستهلك بيها. le muscle un، le témoin: كيخدم ب les deux voies anaérobies. la phosphocréatine: P C plus A D P donne C plus A T P. و la fermentation lactique: glucose plus deux A D P plus deux P i، donne deux acides lactiques plus deux A T P. le muscle deux: la glycolyse مسدودة، إذن ما كايناش la fermentation، و l'acide lactique ما طلعش. بقات غير la phosphocréatine، وعلى هادشي نقصات بزاف. le muscle trois: la créatine kinase مسدودة، إذن la phosphocréatine ما تستعملاتش. بقات غير la fermentation lactique، وعلى هادشي l'acide lactique طلع أكثر."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Un muscle 4 est traité à la fois par l'iodoacétate et par l'inhibiteur de la créatine kinase, puis soumis à la même série d'excitations dans le même milieu. Prévoir, en justifiant, l'évolution de ses teneurs en ATP, en phosphocréatine et en acide lactique, et de ses contractions.",
       "texte_dit": "Question quatre : muscle quatre، عطيناه l'iodoacétate و l'inhibiteur ديال la créatine kinase ف نفس الوقت، ف نفس le milieu، و la même série. توقع، مع التبرير، شنو غادي يوقع ل l'A T P، ل la phosphocréatine، ل l'acide lactique، و ل les contractions.",
       "reponse": {"type": "phrase", "attendu": "Dans le muscle 4, les deux voies anaérobies sont bloquées, et la respiration est impossible sans dioxygène : l'ATP n'est plus régénéré. La phosphocréatine reste à 20 µmol/g (créatine kinase bloquée) et l'acide lactique reste à 1 µmol/g (glycolyse bloquée). L'ATP est consommé sans être remplacé : sa teneur diminue jusqu'à s'épuiser (de 3,0 à 0 µmol/g) ; les contractions faiblissent puis s'arrêtent après quelques secondes, avant la fin de la série. Cela montre que l'ATP est la source directe d'énergie de la contraction et qu'il doit être régénéré."},
       "clavier": {"aides": ["les deux voies bloquées", "phosphocréatine constante", "acide lactique constant", "l'ATP s'épuise", "les contractions s'arrêtent"], "pieges": ["l'ATP reste constant", "la respiration prend le relais"]},
       "aides": [
         {"texte": "Fais la liste des trois voies et barre celles qui ne peuvent pas fonctionner dans le muscle 4.",
          "dit": "دير la liste ديال les trois voies، وشطب على اللي ما تقدرش تخدم ف le muscle quatre."},
         {"texte": "Plus aucune voie : que devient la réserve d'ATP à chaque contraction ? Et la phosphocréatine, l'acide lactique ?",
          "dit": "ما بقات حتى voie: شنو كيوقع ل la réserve ديال l'A T P ف كل contraction؟ و la phosphocréatine، و l'acide lactique؟"}],
       "correction": {"lignes": [
           {"texte": "4 : glycolyse et créatine kinase bloquées, pas de respiration sans O₂ : ATP non régénéré", "mot": "ما بقات حتى voie"},
           {"texte": "phosphocréatine constante (20 µmol/g) ; acide lactique constant (1 µmol/g)", "mot": "la phosphocréatine غادي تبقى"},
           {"texte": "l'ATP s'épuise (3,0 → 0) : les contractions s'arrêtent en quelques secondes", "mot": "l'A T P غادي يسالي"},
           {"texte": "l'ATP est la source directe d'énergie et doit être régénéré", "mot": "la source directe"}],
         "parole": "Question quatre. ف le muscle quatre، la glycolyse و la créatine kinase مسدودين، و la respiration ما تقدرش تخدم بلا dioxygène. ما بقات حتى voie كتجدد l'A T P. la phosphocréatine غادي تبقى à vingt، و l'acide lactique غادي يبقى à un. ولكن كل contraction كتستهلك l'A T P بلا ما يتعوض: l'A T P غادي يسالي، de trois à zéro. les contractions غادي يضعافو، ويوقفو من بعد quelques secondes. إذن l'A T P هو la source directe ديال l'énergie، وخاصو يتجدد."},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "On prolonge la série d'excitations du muscle 2 bien au-delà de 30 excitations. Prévoir l'évolution de ses contractions, et la comparer à celle du témoin. Justifier.",
       "texte_dit": "Question cinq : كنطولو la série ديال les excitations ديال le muscle deux، au-delà de trente excitations. توقع شنو غادي يوقع ل les contractions ديالو، وقارن مع le témoin. برر.",
       "reponse": {"type": "phrase", "attendu": "Le muscle 2 ne régénère l'ATP qu'avec la phosphocréatine, qui baisse à chaque contraction : il n'en reste que 6 µmol/g après 30 excitations. Quand la phosphocréatine sera épuisée, l'ATP ne sera plus régénéré ; il s'épuisera et les contractions s'arrêteront. Elles s'arrêteront plus tôt que celles du témoin, qui régénère aussi l'ATP par la fermentation lactique et utilise sa phosphocréatine plus lentement."},
       "clavier": {"aides": ["phosphocréatine épuisée", "plus que 6 µmol/g", "l'ATP s'épuise", "plus tôt que le témoin", "fermentation lactique"], "pieges": ["les contractions continuent sans fin", "il s'arrête tout de suite"]},
       "aides": [
         {"texte": "Dans le muscle 2, quelle est la seule réserve qui régénère l'ATP ? Combien en reste-t-il après 30 excitations ?",
          "dit": "ف le muscle deux، شمن réserve وحدها كتجدد l'A T P؟ وشحال بقا منها après trente excitations؟"},
         {"texte": "Quand cette réserve sera vide, que deviendront l'ATP et les contractions ? Le témoin, lui, dispose de quelle autre voie ?",
          "dit": "ملي تخوا هاد la réserve، شنو غادي يوقع ل l'A T P و les contractions؟ و le témoin، شمن voie أخرى عندو؟"}],
       "correction": {"lignes": [
           {"texte": "5 : muscle 2 : seule la phosphocréatine régénère l'ATP ; il n'en reste que 6 µmol/g", "mot": "il reste seulement six"},
           {"texte": "phosphocréatine épuisée → ATP non régénéré → l'ATP s'épuise → arrêt des contractions", "mot": "ملي تسالي la phosphocréatine"},
           {"texte": "arrêt plus tôt que le témoin, qui a aussi la fermentation lactique", "mot": "plus tôt que le témoin"}],
         "parole": "Question cinq. le muscle deux عندو غير la phosphocréatine باش يجدد l'A T P، و après trente excitations، il reste seulement six micromoles par gramme. ملي تسالي la phosphocréatine، l'A T P ما بقاش يتجدد: غادي يسالي، و les contractions غادي يوقفو. وغادي يوقفو plus tôt que le témoin، حيت le témoin عندو حتى la fermentation lactique، وكيستعمل la phosphocréatine ديالو بشوية."},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : sans dioxygène, pas de respiration",
     "screen_content": {"lead": "Sans O₂, la respiration s'arrête : il ne reste que la phosphocréatine et la fermentation lactique."},
     "visual": {"kind": "simulation", "url": CHAL, "caption": "Le muscle avec puis sans dioxygène : la chaleur retardée disparaît"},
     "speech_text": {"mixed": "تفكر هاد التجربة ديال الدرس. مع le dioxygène، كاينة la chaleur initiale، ومن بعد la chaleur retardée. دابا بلا dioxygène: la chaleur retardée ما جاتش. حيت la chaleur retardée كتجي من la respiration، و la respiration محتاجة le dioxygène. إذن ف milieu بلا dioxygène، la respiration ما كتخدمش. كيبقاو غير les voies anaérobies: la phosphocréatine و la fermentation lactique. هادشي علاش اخترنا هاد le milieu: باش نقراو هاد les voies بوحدهم."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "sans O₂ : pas de respiration", "mot": "la respiration ما كتخدمش"},
                  {"texte": "il reste : phosphocréatine et fermentation lactique", "mot": "كيبقاو غير les voies anaérobies"}],
       "pointage": [{"mot": "مع le dioxygène", "commande": "play_until", "parametres": {"moment": "avec_dioxygene"}},
                    {"mot": "ومن بعد la chaleur retardée", "repere": "chaleur_retardee"},
                    {"mot": "دابا بلا dioxygène", "commande": "play_until", "parametres": {"moment": "sans_dioxygene"}},
                    {"mot": "دابا بلا dioxygène", "repere": "interrupteur_o2"},
                    {"mot": "la chaleur retardée ما جاتش", "repere": "chaleur_retardee"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : comparer chaque muscle au témoin",
     "screen_content": {"lead": "Ligne par ligne, le muscle traité face au témoin, avec les valeurs."},
     "visual": {"kind": "simulation", "url": INHIB, "caption": "Le témoin et le muscle à glycolyse bloquée, excités de la même façon"},
     "speech_text": {"mixed": "الطريقة: قارن كل muscle مع le témoin، سطر ب سطر. شوف le témoin: l'A T P ثابت، و la phosphocréatine كتنقص شوية. شوف le muscle اللي la glycolyse ديالو مسدودة، بحال le muscle deux: l'A T P حتى هو ثابت، ولكن la phosphocréatine كتنقص بزاف. ف le document، elle passe de vingt à six، contre de vingt à quatorze ف le témoin. و l'acide lactique ما كيطلعش. le muscle trois ما كاينش ف هاد la simulation: ف le document، la phosphocréatine ديالو ما كتبدلش، و l'acide lactique كيطلع أكثر من le témoin."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "ATP constant, 30 contractions dans les trois muscles", "mot": "l'A T P حتى هو ثابت"},
                  {"texte": "muscle 2 : PC 20 → 6 contre 20 → 14 ; acide lactique 1 → 1 contre 1 → 9", "mot": "elle passe de vingt à six"},
                  {"texte": "muscle 3 : PC 20 → 20 ; acide lactique 1 → 15 contre 1 → 9", "mot": "le muscle trois ما كاينش"}],
       "pointage": [{"mot": "الطريقة: قارن", "commande": "play_until", "parametres": {"moment": "pc_basse"}},
                    {"mot": "شوف le témoin", "repere": "temoin"},
                    {"mot": "و la phosphocréatine كتنقص شوية", "repere": "temoin_pc"},
                    {"mot": "شوف le muscle اللي la glycolyse", "repere": "glycolyse"},
                    {"mot": "l'A T P حتى هو ثابت", "repere": "glycolyse_atp"},
                    {"mot": "ولكن la phosphocréatine كتنقص بزاف", "repere": "glycolyse_pc"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : une voie bloquée, l'autre prend le relais",
     "screen_content": {"lead": "Glycolyse bloquée → phosphocréatine seule. Créatine kinase bloquée → fermentation lactique seule."},
     "visual": {"kind": "simulation", "url": VOIES, "caption": "Les deux voies anaérobies et leurs réactions"},
     "speech_text": {"mixed": "l'A T P كيتستهلك ف كل contraction، ولكن كيبقى ثابت: إذن كيتجدد. ب شنو؟ بلا dioxygène، كاينين غير جوج طرق. الطريق اللول: la phosphocréatine، P C plus A D P donne C plus A T P، ب la créatine kinase. الطريق الثاني: la fermentation lactique، glucose plus deux A D P plus deux P i، donne deux acides lactiques plus deux A T P. ف le témoin، les deux كيخدمو. يلا سدينا la glycolyse، la fermentation كتوقف، وكتبقى غير la phosphocréatine: كتنقص بزاف، وما كاينش l'acide lactique. يلا سدينا la créatine kinase، la phosphocréatine ما كتستعملش، وكتبقى غير la fermentation: l'acide lactique كيطلع أكثر."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": EQ_PC + " (créatine kinase)", "mot": "P C plus A D P donne C plus A T P"},
                  {"texte": EQ_FL, "mot": "glucose plus deux A D P"},
                  {"texte": "glycolyse bloquée → phosphocréatine seule", "mot": "يلا سدينا la glycolyse"},
                  {"texte": "créatine kinase bloquée → fermentation seule", "mot": "يلا سدينا la créatine kinase"}],
       "pointage": [{"mot": "الطريق اللول", "commande": "play_until", "parametres": {"moment": "phosphocreatine"}},
                    {"mot": "P C plus A D P donne C plus A T P", "repere": "equation_alactique"},
                    {"mot": "الطريق الثاني", "commande": "play_until", "parametres": {"moment": "fermentation_lactique"}},
                    {"mot": "glucose plus deux A D P", "repere": "equation_lactique"},
                    {"mot": "يلا سدينا la glycolyse", "repere": "jauge_pc"},
                    {"mot": "يلا سدينا la créatine kinase", "repere": "jauge_lactique"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : les deux voies bloquées, l'ATP s'épuise",
     "screen_content": {"lead": "Plus aucune voie : phosphocréatine constante, ATP épuisé, contraction arrêtée en quelques secondes."},
     "visual": {"kind": "simulation", "url": INHIB, "caption": "Le muscle à glycolyse et créatine kinase bloquées"},
     "speech_text": {"mixed": "شوف le muscle اللي la glycolyse و la créatine kinase ديالو مسدودين: هادا هو le muscle quatre ديال السؤال. ف البداية كيتقلص، حيت عندو شوية ديال l'A T P ف la réserve. ولكن ما كاينة حتى voie كتجدد l'A T P. شوف la jauge ديال l'A T P: كتنقص حتى كتسالي. و la phosphocréatine كتبقى ثابتة. ملي سالا l'A T P، le muscle وقف: ما بقاش كيتقلص. إذن l'A T P هو la source directe ديال l'énergie."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "aucune voie : ATP non régénéré", "mot": "ما كاينة حتى voie"},
                  {"texte": "ATP épuisé ; PC et acide lactique constants", "mot": "كتنقص حتى كتسالي"},
                  {"texte": "arrêt de la contraction en quelques secondes", "mot": "le muscle وقف"}],
       "pointage": [{"mot": "شوف le muscle اللي", "repere": "double"},
                    {"mot": "ف البداية كيتقلص", "commande": "play_until", "parametres": {"moment": "depart"}},
                    {"mot": "شوف la jauge ديال l'A T P", "commande": "play_until", "parametres": {"moment": "atp_epuise"}},
                    {"mot": "شوف la jauge ديال l'A T P", "repere": "double_atp"},
                    {"mot": "و la phosphocréatine كتبقى ثابتة", "repere": "double_pc"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : la phosphocréatine seule ne dure pas",
     "screen_content": {"lead": "Glycolyse bloquée : quand la phosphocréatine est épuisée, la contraction s'arrête, plus tôt que le témoin."},
     "visual": {"kind": "simulation", "url": INHIB, "caption": "Le muscle à glycolyse bloquée, si la série continue"},
     "speech_text": {"mixed": "شوف le muscle اللي la glycolyse ديالو مسدودة. la série كتكمل. la phosphocréatine ديالو كتنقص ف كل contraction. ملي كتسالي la phosphocréatine، ما بقا والو يجدد l'A T P، و le muscle كيوقف. أما le témoin، باقي كيتقلص: عندو حتى la fermentation lactique. إذن le muscle deux غادي يوقف plus tôt que le témoin."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "glycolyse bloquée : phosphocréatine seule", "mot": "شوف le muscle اللي la glycolyse"},
                  {"texte": "PC épuisée → ATP non régénéré → arrêt", "mot": "ملي كتسالي la phosphocréatine"},
                  {"texte": "arrêt plus tôt que le témoin", "mot": "plus tôt que le témoin"}],
       "pointage": [{"mot": "شوف le muscle اللي la glycolyse", "repere": "glycolyse"},
                    {"mot": "la série كتكمل", "commande": "play_until", "parametres": {"moment": "pc_basse"}},
                    {"mot": "la phosphocréatine ديالو كتنقص", "repere": "glycolyse_pc"},
                    {"mot": "ملي كتسالي la phosphocréatine", "commande": "play_until", "parametres": {"moment": "arret_glycolyse"}},
                    {"mot": "أما le témoin، باقي", "commande": "play_until", "parametres": {"moment": "fin"}},
                    {"mot": "أما le témoin، باقي", "repere": "temoin"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : sans dioxygène", "سؤال ساهل على le milieu.",
      "Dans un milieu sans dioxygène, quelle voie ne peut pas régénérer l'ATP ?", ["la fermentation lactique", "la respiration", "la voie de la phosphocréatine"], 1, {
        "1": {"juste": rep("برافو! la respiration محتاجة le dioxygène، إذن ما كتخدمش هنا.", "Juste : la respiration a besoin de dioxygène.")},
        "0": {"1": rep("ما تقلقش. la fermentation lactique كتخدم بلا dioxygène. شكون اللي محتاج le dioxygène؟ عاود اختار.", "La fermentation lactique se fait sans dioxygène. Réessaie."),
              "2": rep("الجواب هو la respiration. la fermentation lactique anaérobie: كتخدم بلا dioxygène.", "Réponse : la respiration.")},
        "2": {"1": rep("لا، la phosphocréatine voie anaérobie: ما محتاجاش le dioxygène. عاود اختار.", "La voie de la phosphocréatine est anaérobie. Réessaie."),
              "2": rep("الجواب هو la respiration، la seule voie aérobie.", "Réponse : la respiration, la seule voie aérobie.")}},
      "Dans un milieu sans dioxygène, quelle voie ne peut pas régénérer l'ATP ?"),
    vrai_faux("fa_s2", "Plus facile : comparer au témoin", "Vrai ou faux, d'après le document.",
      "نتمرنو على المقارنة: قول واش صحيح ولا خطأ.",
      [("Dans les trois muscles, l'ATP reste à 3,0 µmol/g.", True, "Vrai : l'ATP ne change dans aucun des trois muscles."),
       ("Le muscle 2 produit plus d'acide lactique que le témoin.", False, "Faux : il n'en produit pas (1 → 1) ; le témoin passe de 1 à 9."),
       ("La phosphocréatine du muscle 3 ne change pas.", True, "Vrai : 20 → 20 µmol/g, alors qu'elle baisse dans le témoin."),
       ("La phosphocréatine baisse moins dans le muscle 2 que dans le témoin.", False, "Faux : elle baisse plus : 20 → 6 contre 20 → 14 µmol/g.")]),
    association("fa_s3", "Plus facile : chaque muscle et sa voie", "Relie chaque muscle à ce qui a régénéré son ATP.",
      "سؤال ساهل: ربط كل muscle مع la voie اللي جددت l'A T P ديالو.", "Relie chaque muscle à la ou les voies qui ont régénéré son ATP.",
      [("1", "Muscle 1 (témoin)"), ("2", "Muscle 2 (glycolyse bloquée)"), ("3", "Muscle 3 (créatine kinase bloquée)")],
      [("a", "Phosphocréatine et fermentation lactique"), ("b", "Phosphocréatine seule"), ("c", "Fermentation lactique seule")],
      {"1": "a", "2": "b", "3": "c"},
      {"1-a": (True, "Oui : sa phosphocréatine baisse un peu et il produit de l'acide lactique.", "برافو: la phosphocréatine نقصات شوية، و l'acide lactique طلع."),
       "1-b": (False, "Non : le témoin produit aussi de l'acide lactique (1 → 9).", "لا، le témoin حتى هو عطا l'acide lactique."),
       "1-c": (False, "Non : la phosphocréatine du témoin baisse aussi (20 → 14).", "لا، la phosphocréatine ديال le témoin حتى هي نقصات."),
       "2-a": (False, "Non : sans glycolyse, pas de fermentation ; pas d'acide lactique produit.", "لا، بلا glycolyse ما كايناش la fermentation."),
       "2-b": (True, "Oui : glycolyse bloquée, il ne reste que la phosphocréatine (20 → 6).", "برافو: la glycolyse مسدودة، بقات غير la phosphocréatine."),
       "2-c": (False, "Non : la fermentation commence par la glycolyse, qui est bloquée.", "لا، la fermentation كتبدا ب la glycolyse، وهي مسدودة."),
       "3-a": (False, "Non : sa phosphocréatine ne baisse pas (20 → 20).", "لا، la phosphocréatine ديالو ما نقصاتش."),
       "3-b": (False, "Non : la créatine kinase bloquée empêche d'utiliser la phosphocréatine.", "لا، la créatine kinase مسدودة، إذن la phosphocréatine ما تستعملاتش."),
       "3-c": (True, "Oui : seule la fermentation lactique fonctionne, d'où plus d'acide lactique (1 → 15).", "برافو: غير la fermentation lactique، وعلى هادشي l'acide lactique طلع أكثر.")},
      ("(1 ; a) (2 ; b) (3 ; c).", "le témoin: les deux voies. la glycolyse مسدودة: la phosphocréatine بوحدها. la créatine kinase مسدودة: la fermentation بوحدها.")),
    qcm_facile("fa_s4", "Plus facile : les deux voies bloquées", "سؤال ساهل على le muscle quatre.",
      "Dans le muscle 4 (glycolyse et créatine kinase bloquées, sans dioxygène), l'ATP…", ["reste constant grâce à la phosphocréatine", "s'épuise, et les contractions s'arrêtent", "reste constant grâce à la fermentation lactique"], 1, {
        "1": {"juste": rep("برافو! ما بقات حتى voie كتجدد l'A T P، إذن كيسالي و le muscle كيوقف.", "Juste : aucune voie ne régénère l'ATP : il s'épuise.")},
        "0": {"1": rep("ما تقلقش. la créatine kinase مسدودة: واش la phosphocréatine تقدر تخدم؟ عاود اختار.", "La créatine kinase est bloquée : la phosphocréatine peut-elle servir ? Réessaie."),
              "2": rep("الجواب هو l'A T P كيسالي. la phosphocréatine ما تقدرش تخدم بلا la créatine kinase.", "Réponse : l'ATP s'épuise et les contractions s'arrêtent.")},
        "2": {"1": rep("لا، la glycolyse مسدودة، إذن la fermentation ما كتخدمش. عاود اختار.", "La glycolyse est bloquée : pas de fermentation. Réessaie."),
              "2": rep("الجواب هو l'A T P كيسالي، و les contractions كيوقفو.", "Réponse : l'ATP s'épuise et les contractions s'arrêtent.")}},
      "Dans le muscle quatre, glycolyse et créatine kinase bloquées, sans dioxygène, l'ATP ?"),
    qcm_facile("fa_s5", "Plus facile : si la série continue", "سؤال ساهل على le muscle deux.",
      "Si la série d'excitations du muscle 2 continue longtemps, ses contractions…", ["continuent sans fin", "s'arrêtent dès la première excitation", "s'arrêtent quand la phosphocréatine est épuisée"], 2, {
        "2": {"juste": rep("برافو! la phosphocréatine هي غير اللي كتجدد l'A T P، وملي كتسالي، le muscle كيوقف.", "Juste : arrêt quand la phosphocréatine est épuisée.")},
        "0": {"1": rep("ما تقلقش. la phosphocréatine كتنقص ف كل contraction. واش ما غاديش تسالي؟ عاود اختار.", "La phosphocréatine baisse à chaque contraction. Réessaie."),
              "2": rep("الجواب هو كيوقف ملي تسالي la phosphocréatine.", "Réponse : elles s'arrêtent quand la phosphocréatine est épuisée.")},
        "1": {"1": rep("لا، ف le document le muscle deux a fait trente contractions normales. عاود اختار.", "Le muscle 2 a fait 30 contractions normales. Réessaie."),
              "2": rep("الجواب هو كيوقف ملي تسالي la phosphocréatine، ماشي من البداية.", "Réponse : quand la phosphocréatine est épuisée.")}},
      "Si la série d'excitations du muscle deux continue longtemps, ses contractions ?")
  ]}]},
  "similaire": {
    "id": "svt_ex_ch2_inhibiteurs_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même protocole avec trois autres muscles, dans un milieu privé de dioxygène : muscle 1 témoin, muscle 2 traité par l'iodoacétate (glycolyse bloquée), muscle 3 à créatine kinase bloquée. Chacun reçoit cette fois une série de 24 excitations efficaces.",
      "intro_dit": "نفس التجربة، avec trois autres muscles، بلا dioxygène: le muscle un témoin، le muscle deux ب l'iodoacétate، و le muscle trois، la créatine kinase ديالو مسدودة. هاد المرة، la série فيها vingt-quatre excitations.",
      "figures": [doc(MB, 24)],
      "donnees": ["Milieu privé de dioxygène", "Iodoacétate : bloque la glycolyse", "Teneurs en µmol par g de muscle"],
      "questions": [
        {"id": "1", "texte": "Justifier le choix d'un milieu privé de dioxygène.",
         "reponse": {"type": "phrase", "attendu": "Sans dioxygène, la respiration est impossible : seules les voies anaérobies (phosphocréatine et fermentation lactique) régénèrent l'ATP, et on peut les étudier seules."},
         "clavier": {"aides": ["respiration impossible", "voies anaérobies"], "pieges": ["pas de contraction"]},
         "correction": {"lignes": [{"texte": "1 : pas de respiration sans O₂ : seules les voies anaérobies régénèrent l'ATP", "mot": "les voies anaérobies"}],
                        "parole": "Question un. بلا dioxygène، ما كايناش la respiration: كيبقاو غير les voies anaérobies، la phosphocréatine و la fermentation lactique."}},
        {"id": "2", "texte": "Comparer les résultats du muscle 2, puis ceux du muscle 3, avec ceux du témoin.",
         "reponse": {"type": "phrase", "attendu": "Dans les trois muscles : 24 contractions et ATP constant (4,0 µmol/g). Muscle 2 : phosphocréatine 25 → 13 contre 25 → 20 dans le témoin ; acide lactique 1 → 1 contre 1 → 8. Muscle 3 : phosphocréatine 25 → 25 alors qu'elle diminue dans le témoin ; acide lactique 1 → 13 contre 1 → 8."},
         "clavier": {"aides": ["contre", "alors que"], "pieges": ["l'ATP diminue"]},
         "correction": {"lignes": [{"texte": "2 : ATP constant (4,0) et 24 contractions partout", "mot": "l'A T P ثابت"},
                                   {"texte": "muscle 2 : PC 25 → 13 contre 25 → 20 ; acide lactique 1 → 1 contre 1 → 8", "mot": "le muscle deux"},
                                   {"texte": "muscle 3 : PC 25 → 25 ; acide lactique 1 → 13 contre 1 → 8", "mot": "le muscle trois"}],
                        "parole": "Question deux. l'A T P ثابت ف les trois muscles. le muscle deux: la phosphocréatine de vingt-cinq à treize، contre de vingt-cinq à vingt، و l'acide lactique ما تبدلش. le muscle trois: la phosphocréatine ما تبدلاتش، و l'acide lactique de un à treize، contre de un à huit."}},
        {"id": "3", "texte": "Expliquer pourquoi l'ATP reste constant, puis préciser pour chaque muscle la ou les voies qui ont régénéré l'ATP, avec la réaction ou l'équation.",
         "reponse": {"type": "phrase", "attendu": "L'ATP consommé est régénéré aussi vite qu'il est consommé. Témoin : phosphocréatine (PC + ADP → C + ATP) et fermentation lactique (C₆H₁₂O₆ + 2 ADP + 2 Pi → 2 CH₃-CHOH-COOH + 2 ATP). Muscle 2 : glycolyse bloquée, pas de fermentation : phosphocréatine seule. Muscle 3 : créatine kinase bloquée : fermentation lactique seule."},
         "clavier": {"aides": [EQ_PC, EQ_FL], "pieges": ["respiration"]},
         "correction": {"lignes": [{"texte": "3 : ATP régénéré aussi vite qu'il est consommé", "mot": "كيتجدد"},
                                   {"texte": "témoin : les deux voies ; muscle 2 : PC seule ; muscle 3 : fermentation seule", "mot": "le témoin"}],
                        "parole": "Question trois. l'A T P كيتجدد ب نفس السرعة. le témoin: la phosphocréatine و la fermentation lactique. le muscle deux: غير la phosphocréatine. le muscle trois: غير la fermentation lactique."}},
        {"id": "4", "texte": "Prévoir, en justifiant, les résultats d'un muscle 4 traité par l'iodoacétate et par l'inhibiteur de la créatine kinase, soumis à la même série.",
         "reponse": {"type": "phrase", "attendu": "Les deux voies anaérobies sont bloquées et il n'y a pas de respiration : l'ATP n'est plus régénéré. Phosphocréatine constante (25 µmol/g), acide lactique constant (1 µmol/g) ; l'ATP s'épuise (4,0 → 0) et les contractions s'arrêtent en quelques secondes."},
         "clavier": {"aides": ["l'ATP s'épuise", "phosphocréatine constante"], "pieges": ["l'ATP reste constant"]},
         "correction": {"lignes": [{"texte": "4 : aucune voie : ATP 4,0 → 0, PC 25 → 25, acide lactique 1 → 1", "mot": "l'A T P غادي يسالي"},
                                   {"texte": "les contractions s'arrêtent en quelques secondes", "mot": "les contractions"}],
                        "parole": "Question quatre. ما بقات حتى voie: l'A T P غادي يسالي، de quatre à zéro، la phosphocréatine و l'acide lactique ما يتبدلوش، و les contractions غادي يوقفو من بعد quelques secondes."}},
        {"id": "5", "texte": "On prolonge la série du muscle 2 bien au-delà de 24 excitations. Prévoir l'évolution de ses contractions et la comparer à celle du témoin.",
         "reponse": {"type": "phrase", "attendu": "Le muscle 2 ne régénère l'ATP qu'avec la phosphocréatine (il en reste 13 µmol/g). Quand elle sera épuisée, l'ATP s'épuisera et les contractions s'arrêteront, plus tôt que celles du témoin, qui dispose aussi de la fermentation lactique."},
         "clavier": {"aides": ["phosphocréatine épuisée", "plus tôt que le témoin"], "pieges": ["sans fin"]},
         "correction": {"lignes": [{"texte": "5 : PC seule (13 µmol/g restants) → épuisée → ATP épuisé → arrêt", "mot": "ملي تسالي la phosphocréatine"},
                                   {"texte": "arrêt plus tôt que le témoin (fermentation lactique en plus)", "mot": "plus tôt que le témoin"}],
                        "parole": "Question cinq. ملي تسالي la phosphocréatine، l'A T P ما بقاش يتجدد، و le muscle deux غادي يوقف plus tôt que le témoin، اللي عندو حتى la fermentation lactique."}}
      ]}}
}
ecrire(EX, sys.argv[1])
