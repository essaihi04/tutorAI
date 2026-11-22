# Exercice SVT ch. 1 (libération de l'énergie), niveau moyen : vésicules de membrane interne, gradient de H+ et ATP synthase.
# Ce qu'il entraîne : orienter la membrane interne par les sphères pédonculées (têtes côté matrice), comparer des expériences
# deux à deux puis déduire les conditions de la synthèse d'ATP, « décrire… puis déduire » une courbe de [H+], expliquer en
# chaîne de flèches (O2 accepteur final → chaîne → pompage des H+ → gradient → retour par les sphères → ATP), définir la
# phosphorylation oxydative (2018 N).
# Sources comparées (lecture seulement, rien de copié) :
# - exploration du cours : cas_types « pulse_o2 », « sens_protons », « inhibiteur » (méthode des flèches), pièges « sens
#   des protons », « [H+] nulle », a_ne_pas_dire (rotation, « un proton = un ATP », « la sphère active l'ATP synthase ») ;
# - diapositives du cours le_c10_vesicules / le_c10b (vésicules, pH 4 dedans / 8 dehors) et le_c1_pulse (national 2016 R) ;
# - nationaux : 2016 R (mitochondries SANS membrane externe, [H+] du milieu qui MONTE après l'O2) — on n'en reprend pas la
#   situation : ici des vésicules retournées (face matrice dehors), [H+] du milieu qui DESCEND, autres valeurs ; 2018 N et
#   2020 R (QCM sur la chaîne), 2024 R (sens des H+), 2023 N (ATP synthase déformée) pour les formes des questions ;
# - vidéo exercices Ouissam SVT (pulse d'O2, cyanure) via l'exploration ; séries en ligne (recherche du 22/11/2026, extraits
#   seulement, sites bloqués par le réseau) : « sphères pédonculées = ATP synthétases de la membrane interne ».
# Pas de recouvrement : ajouts successifs à des mitochondries (ADP + Pi, O2 / ATP) = svt_ex_ch1_conditions_mitochondrie_1.
import sys, math
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _commun import rep, qcm_facile, vrai_faux, association, ecrire

D = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/"
VES = D + "vesicules.html?depart=0"
VES_CAS = D + "vesicules.html?sans_manip&depart=0"
PULSE = D + "exao.html?vue=pulse_o2&depart=0"
CHAINE = D + "chaine.html?depart=0"
CHAINE_SPH = D + "chaine.html?depart=gradient_ecrit"


def schema_vesicule(titre):
    cx, cy, r = 3.0, 3.0, 1.75
    el = [{"f": "cercle", "c": [cx, cy], "r": r, "couleur": "jaune"},
          {"f": "cercle", "c": [cx, cy], "r": r - 0.14, "couleur": "jaune"}]
    for k in range(8):
        a = math.radians(22.5 + 45 * k)
        p0 = [round(cx + r * math.cos(a), 2), round(cy + r * math.sin(a), 2)]
        p1 = [round(cx + (r + 0.38) * math.cos(a), 2), round(cy + (r + 0.38) * math.sin(a), 2)]
        tete = [round(cx + (r + 0.6) * math.cos(a), 2), round(cy + (r + 0.6) * math.sin(a), 2)]
        el += [{"f": "ligne", "pts": [p0, p1], "couleur": "jaune"}, {"f": "cercle", "c": tete, "r": 0.22, "couleur": "orange", "remplir": "orange"}]
    a = math.radians(22.5)
    tete0 = [cx + (r + 0.6) * math.cos(a), cy + (r + 0.6) * math.sin(a)]
    el += [{"f": "texte", "at": [cx, cy + 0.25], "t": "intérieur", "couleur": "blanc", "taille": "petit"},
           {"f": "texte", "at": [cx, cy - 0.3], "t": "de la vésicule", "couleur": "blanc", "taille": "petit"},
           {"f": "texte", "at": [8.0, 5.6], "t": "milieu extérieur", "couleur": "cyan", "taille": "petit"},
           {"f": "fleche", "de": [6.6, 3.9], "a": [round(tete0[0] + 0.25, 2), round(tete0[1] + 0.05, 2)], "couleur": "blanc"},
           {"f": "texte", "at": [8.4, 4.05], "t": "sphère pédonculée", "couleur": "orange", "taille": "petit"},
           {"f": "texte", "at": [8.4, 3.55], "t": "(ATP synthase)", "couleur": "orange", "taille": "petit"},
           {"f": "fleche", "de": [6.6, 1.4], "a": [round(cx + r * math.cos(math.radians(-20)), 2), round(cy + r * math.sin(math.radians(-20)), 2)], "couleur": "blanc"},
           {"f": "texte", "at": [8.4, 1.4], "t": "membrane interne", "couleur": "jaune", "taille": "petit"}]
    return {"type": "schema", "titre": titre, "cadre": {"l": 10, "h": 6},
            "legende": "Vésicule obtenue en fragmentant la membrane interne aux ultrasons : la membrane se referme, sphères pédonculées tournées vers l'extérieur.",
            "elements": el}


def tableau(lignes, titre):
    """Tableau dessiné (schema à cadre) : une ligne d'en-tête + une ligne par expérience."""
    cols = [0, 1.9, 3.9, 5.9, 7.9, 10]
    tete = ["Expérience", "pH intérieur", "pH extérieur", "Sphères", "ATP produit"]
    n = len(lignes) + 1
    h = 1.0 * n
    el = [{"f": "rect", "de": [0, 0], "a": [10, h], "couleur": "blanc"}]
    for x in cols[1:-1]:
        el.append({"f": "ligne", "pts": [[x, 0], [x, h]], "couleur": "faible"})
    for i in range(1, n):
        el.append({"f": "ligne", "pts": [[0, h - i], [10, h - i]], "couleur": "faible"})
    for i, rangee in enumerate([tete] + lignes):
        y = h - i - 0.5
        for j, t in enumerate(rangee):
            el.append({"f": "texte", "at": [(cols[j] + cols[j + 1]) / 2, y - 0.08], "t": t, "taille": "petit",
                       "couleur": "jaune" if i == 0 else ("vert" if t == "oui" else "blanc")})
    return {"type": "schema", "titre": titre, "cadre": {"l": 10, "h": h},
            "legende": "Les vésicules sont placées dans une solution contenant ADP + Pi ; on règle le pH de l'intérieur et de l'extérieur.", "elements": el}


def courbe_h(h0, hmin, t_inj, t_min, titre):
    E = 50.0
    fin = h0 - (h0 - hmin) * math.exp(-(300 - t_min) / E)
    assert h0 - fin < 0.5      # revenue à la valeur initiale vers 300 s
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": 0, "max": 360, "nom": "t", "unite": "s", "graduations": list(range(0, 361, 60)) + ([t_min] if t_min % 60 else [])},
                     "y": {"min": 0, "max": 60, "nom": "[H⁺] du milieu extérieur", "unite": "× 10⁻⁹ mol/L", "graduations": list(range(0, 61, 10))}},
            "legende": "Concentration des protons dans le milieu extérieur aux vésicules (pH-mètre).",
            "elements": [
              {"f": "courbe", "expr": f"{h0}", "de": 0, "a": t_inj, "couleur": "rouge"},
              {"f": "courbe", "expr": f"{h0}-{h0 - hmin}*sin((x-{t_inj})/{t_min - t_inj}*pi/2)", "de": t_inj, "a": t_min, "couleur": "rouge"},
              {"f": "courbe", "expr": f"{h0}-{h0 - hmin}*exp(-(x-{t_min})/{E})", "de": t_min, "a": 360, "couleur": "rouge", "texte": "[H⁺]", "texte_x": 330, "pos": "n"},
              {"f": "fleche", "de": [t_inj, 12], "a": [t_inj, h0 - 2], "couleur": "cyan", "texte": "un peu d'O₂", "pos": "e"},
              {"f": "repere", "x": t_min, "y": hmin}]}


FIG_V = schema_vesicule("Document 1 (a) : une vésicule de membrane interne")
FIG_T = tableau([["A", "7,5", "7,5", "présentes", "non"], ["B", "4", "8", "présentes", "oui"], ["C", "4", "8", "absentes", "non"]],
                "Document 1 (b) : trois expériences")
FIG_H = courbe_h(50, 30, 60, 80, "Document 2 : [H⁺] du milieu après un peu d'O₂")
FIG_TS = tableau([["A", "4,5", "8", "absentes", "non"], ["B", "4,5", "8", "présentes", "oui"], ["C", "8", "8", "présentes", "non"]],
                 "Document 1 (b) : trois expériences")
FIG_HS = courbe_h(40, 24, 80, 100, "Document 2 : [H⁺] du milieu après un peu d'O₂")

EX = {
  "id": "svt_ex_ch1_chaine_respiratoire_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "reactions_responsables_liberation_energie", "cours": "svt_ch1_reactions_responsables_liberation_energie",
  "titre": "Des vésicules de membrane interne : protons, sphères pédonculées et ATP", "niveau": "moyen", "duree_min": 35,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Comparer des expériences puis déduire", "Décrire une courbe de [H⁺] puis déduire", "Expliquer le fonctionnement de la chaîne respiratoire", "Définir la phosphorylation oxydative"],
  "enonce": {
    "intro": "Des mitochondries sont traitées aux ultrasons : la membrane interne se fragmente et chaque fragment se referme en une petite vésicule (document 1 a). Expérience 1 : des vésicules sont placées dans une solution contenant ADP + Pi, en réglant le pH à l'intérieur et à l'extérieur ; certaines vésicules ont perdu leurs sphères pédonculées (document 1 b). Expérience 2 : des vésicules entières sont placées dans une solution sans dioxygène, riche en NADH,H⁺ et en ADP + Pi ; on injecte une petite quantité de dioxygène, vite consommée, et on mesure [H⁺] du milieu extérieur (document 2). On constate aussi que de l'ATP apparaît dans le milieu après l'injection.",
    "intro_dit": "دابا نقراو l'énoncé. درنا des mitochondries فles ultrasons: la membrane interne تقطعات، وكل قطعة تسدات، وولات vésicule صغيرة. هادا le document un a. فl'expérience une، حطينا les vésicules فsolution فيها ADP و phosphate، وبدلنا le pH داخل و le pH برا. وشي vésicules حيدنا ليهم les sphères pédonculées: هادا le tableau ديال le document un b. فl'expérience deux، حطينا des vésicules كاملين فsolution ما فيهاش le dioxygène، وفيها بزاف ديال N A D H, H plus، و ADP و phosphate. زدنا شوية ديال le dioxygène، كيتستهلك بالزربة، وقسنا la concentration ديال les protons برا: هادا le document deux. ولقينا حتى l'ATP بان فle milieu من بعد ما زدنا le dioxygène.",
    "figures": [FIG_V, FIG_T, FIG_H],
    "donnees": ["Vésicules de membrane interne, sphères pédonculées tournées vers l'extérieur",
                "Expérience 2 : solution sans O₂, riche en NADH,H⁺ et ADP + Pi ; un peu d'O₂ injecté à t = 60 s",
                "Après l'injection, de l'ATP apparaît dans le milieu extérieur",
                "La membrane interne est imperméable aux protons H⁺, sauf au niveau des sphères pédonculées"],
    "questions": [
      {"id": "1", "texte": "En exploitant le document 1 a, préciser à quelle face de la membrane interne correspond la face extérieure de la vésicule, puis à quel compartiment de la mitochondrie correspond l'intérieur de la vésicule. Justifier.",
       "texte_dit": "السؤال un: بle document un a، قول الوجه اللي برا ديال la vésicule، شمن وجه هو ديال la membrane interne، و الداخل ديال la vésicule، شمن compartiment ديال la mitochondrie. برر.",
       "reponse": {"type": "phrase", "attendu": "Dans la mitochondrie, les têtes des sphères pédonculées sont toujours tournées vers la matrice. Sur la vésicule, elles sont tournées vers l'extérieur : la face extérieure de la vésicule est donc la face de la membrane interne du côté de la matrice, et l'intérieur de la vésicule correspond à l'espace intermembranaire."},
       "clavier": {"aides": ["têtes des sphères pédonculées", "côté matrice", "espace intermembranaire", "donc"], "pieges": ["hyaloplasme", "membrane externe"]},
       "aides": [
         {"texte": "Dans une mitochondrie, de quel côté de la membrane interne sont les têtes des sphères pédonculées ?",
          "dit": "فla mitochondrie، الراس ديال les sphères pédonculées، فشمن جهة ديال la membrane interne كيكون؟"},
         {"texte": "Les têtes sont toujours du côté de la matrice ; l'autre côté de la membrane interne donne sur l'espace intermembranaire.",
          "dit": "الراس ديما جهة la matrice. والجهة الأخرى ديال la membrane interne، هي l'espace intermembranaire."}],
       "correction": {"lignes": [
           {"texte": "1 : dans la mitochondrie, les têtes des sphères pédonculées sont côté matrice", "mot": "ديما جهة la matrice"},
           {"texte": "ici elles sont dehors : face extérieure de la vésicule = face matricielle", "mot": "الوجه اللي برا هو الوجه ديال la matrice"},
           {"texte": "donc l'intérieur de la vésicule = espace intermembranaire", "mot": "هو l'espace intermembranaire"}],
         "parole": "السؤال un. فla mitochondrie، الراس ديال les sphères pédonculées ديما جهة la matrice. هنا الراس برا: إذن الوجه اللي برا هو الوجه ديال la matrice. و الداخل ديال la vésicule هو l'espace intermembranaire."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Comparer les résultats des expériences A et B, puis B et C (document 1 b). Déduire les conditions nécessaires à la synthèse d'ATP.",
       "texte_dit": "السؤال deux: قارن les résultats ديال A و B، ومن بعد B و C، فle document un b. واستنتج les conditions اللي خاصين باش تكون la synthèse ديال l'ATP.",
       "reponse": {"type": "phrase", "attendu": "A et B (sphères présentes) : en A, le pH est le même dedans et dehors (7,5) et il n'y a pas d'ATP ; en B, l'intérieur (pH 4) est plus riche en H⁺ que l'extérieur (pH 8) et de l'ATP est produit. B et C (même gradient, pH 4 / 8) : de l'ATP est produit en B avec les sphères, mais pas en C sans les sphères. On en déduit que la synthèse d'ATP nécessite un gradient de protons (intérieur, côté espace intermembranaire, plus riche en H⁺ que le côté matrice) et des sphères pédonculées (ATP synthases)."},
       "clavier": {"aides": ["alors que", "plus riche en H⁺", "gradient de protons", "sphères pédonculées", "On en déduit que"], "pieges": ["pH plus élevé à l'intérieur", "le dioxygène"]},
       "aides": [
         {"texte": "Entre A et B, une seule chose change ; entre B et C aussi. Trouve-la à chaque fois et regarde l'effet sur l'ATP.",
          "dit": "بين A و B، حاجة وحدة اللي تبدلات، وبين B و C حتى هي. لقاها، وشوف شنو وقع لl'ATP."},
         {"texte": "Un pH plus bas veut dire plus de H⁺. Écris : « en B …, alors qu'en A … : donc … », puis la même chose pour B et C.",
          "dit": "le pH اللي صغر، يعني H plus كثر. كتب: en B، alors qu'en A، donc. ومن بعد نفس الحاجة ل B و C."}],
       "correction": {"lignes": [
           {"texte": "2 : A (pH 7,5 / 7,5) : pas d'ATP, alors que B (pH 4 / 8) : ATP → il faut un gradient de H⁺", "mot": "خاص le gradient de protons"},
           {"texte": "B (sphères) : ATP, alors que C (sans sphères, même gradient) : pas d'ATP → il faut les sphères", "mot": "خاص les sphères pédonculées"},
           {"texte": "On en déduit que la synthèse d'ATP nécessite un gradient de protons et des sphères pédonculées", "mot": "on en déduit que"}],
         "parole": "السؤال deux. فA، نفس le pH داخل وبرا، وما كاينش l'ATP، alors que فB، الداخل acide أكثر، يعني فيه H plus كثر، وكاين l'ATP: إذن خاص le gradient de protons. فB كاين l'ATP، alors que فC، بلا sphères، وبنفس le gradient، ما كاينش: إذن خاص les sphères pédonculées. on en déduit que la synthèse ديال l'ATP خاصها le gradient de protons، و les sphères pédonculées."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "Décrire l'évolution de [H⁺] du milieu extérieur (document 2), puis déduire le sens de déplacement des protons après l'injection de dioxygène.",
       "texte_dit": "السؤال trois: وصف l'évolution ديال la concentration ديال les protons برا، فle document deux، ومن بعد استنتج فشمن اتجاه كيتحركو les protons من بعد le dioxygène.",
       "reponse": {"type": "phrase", "attendu": "Avant l'injection (de 0 à 60 s), [H⁺] du milieu extérieur est stable à 50 × 10⁻⁹ mol/L. Juste après l'injection de O₂, elle diminue rapidement jusqu'à 30 × 10⁻⁹ mol/L à 80 s. Ensuite, elle augmente progressivement et revient à sa valeur initiale (50 × 10⁻⁹ mol/L) vers 300 s. On en déduit qu'après l'injection de O₂, des protons passent du milieu extérieur vers l'intérieur des vésicules, puis ressortent vers le milieu extérieur."},
       "clavier": {"aides": ["stable", "diminue rapidement", "augmente progressivement", "valeur initiale", "× 10⁻⁹ mol/L", "On en déduit que"], "pieges": ["nulle", "augmente rapidement"]},
       "aides": [
         {"texte": "Trois périodes : avant 60 s, de 60 à 80 s, après 80 s. Lis la valeur au début et à la fin de chaque période.",
          "dit": "ثلاث ديال المراحل: avant soixante secondes، entre soixante et quatre-vingts secondes، و après quatre-vingts secondes. قرا la valeur فالبداية وفاللخر ديال كل مرحلة."},
         {"texte": "Si les H⁺ du milieu extérieur diminuent, où sont-ils passés ? Les vésicules sont la seule autre place.",
          "dit": "يلا H plus ديال برا نقصو، فين مشاو؟ ما كاين غير الداخل ديال les vésicules."}],
       "correction": {"lignes": [
           {"texte": "3 : avant 60 s : [H⁺] stable à 50 × 10⁻⁹ mol/L", "mot": "stable à cinquante fois dix puissance moins neuf"},
           {"texte": "après O₂ : diminue rapidement jusqu'à 30 × 10⁻⁹ mol/L à 80 s", "mot": "jusqu'à trente fois dix puissance moins neuf"},
           {"texte": "puis augmente progressivement et revient à 50 × 10⁻⁹ mol/L vers 300 s", "mot": "كترجع للvaleur initiale"},
           {"texte": "On en déduit que les H⁺ entrent dans les vésicules, puis en ressortent", "mot": "on en déduit que"}],
         "parole": "السؤال trois. avant soixante secondes، la concentration ديال les protons برا stable à cinquante fois dix puissance moins neuf mole par litre. من بعد le dioxygène، كتنقص بالزربة، jusqu'à trente fois dix puissance moins neuf mole par litre، à quatre-vingts secondes. من بعد كتطلع بشوية، وكترجع للvaleur initiale، vers trois cents secondes. on en déduit que les protons دخلو من برا للداخل ديال les vésicules، ومن بعد رجعو خرجو."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Expliquer la diminution de [H⁺] du milieu extérieur juste après l'injection de dioxygène.",
       "texte_dit": "السؤال quatre: شرح علاش la concentration ديال les protons برا كتنقص، مباشرة من بعد ما زدنا le dioxygène.",
       "reponse": {"type": "phrase", "attendu": "Le dioxygène est l'accepteur final des électrons : son arrivée permet à la chaîne respiratoire de fonctionner → NADH,H⁺ est oxydé en NAD⁺ : il cède deux électrons et deux protons → les électrons passent de transporteur en transporteur (réactions d'oxydoréduction) jusqu'au dioxygène, réduit en eau → ce transfert s'accompagne du pompage des H⁺ du côté matrice (ici le milieu extérieur) vers le côté espace intermembranaire (ici l'intérieur des vésicules) → [H⁺] du milieu extérieur diminue et un gradient de protons se forme."},
       "clavier": {"aides": ["accepteur final", "NADH,H⁺ est oxydé", "transporteurs", "pompage des H⁺", "côté matrice", "gradient de protons", "→"], "pieges": ["les H⁺ passent par les sphères", "le dioxygène pompe les protons"]},
       "aides": [
         {"texte": "Sans O₂, la chaîne respiratoire est arrêtée. Quel est le rôle du dioxygène au bout de la chaîne ?",
          "dit": "بلا dioxygène، la chaîne respiratoire واقفة. شنو هو الدور ديال le dioxygène فاللخر ديال la chaîne؟"},
         {"texte": "Écris la chaîne avec des flèches : O₂ accepteur final → oxydation de NADH,H⁺ → transfert des électrons → pompage des H⁺ (de quel côté vers quel côté, ici ?) → [H⁺] extérieure diminue.",
          "dit": "كتب la chaîne بles flèches: le dioxygène accepteur final، من بعد l'oxydation ديال N A D H, H plus، من بعد le transfert des électrons، من بعد le pompage ديال les protons، من شمن جهة لشمن جهة هنا؟ وفاللخر la concentration برا كتنقص."}],
       "correction": {"lignes": [
           {"texte": "4 : O₂ accepteur final des électrons → la chaîne respiratoire fonctionne", "mot": "l'accepteur final des électrons"},
           {"texte": "→ NADH,H⁺ oxydé → électrons transférés de transporteur en transporteur jusqu'à O₂ (H₂O)", "mot": "N A D H, H plus كيتأكسد"},
           {"texte": "→ pompage des H⁺ du côté matrice (extérieur) vers le côté espace intermembranaire (intérieur)", "mot": "le pompage ديال les protons"},
           {"texte": "→ [H⁺] du milieu extérieur diminue : gradient de protons", "mot": "le gradient de protons"}],
         "parole": "السؤال quatre. le dioxygène هو l'accepteur final des électrons: ملي زدناه، la chaîne respiratoire بدات تخدم. N A D H, H plus كيتأكسد: كيعطي deux électrons و deux protons. les électrons كيدوزو من transporteur ل transporteur، حتى ل le dioxygène، اللي كيولي l'eau. وفنفس الوقت، كاين le pompage ديال les protons، من جهة la matrice، اللي هي برا هنا، لجهة l'espace intermembranaire، اللي هي الداخل ديال la vésicule. إذن la concentration ديال les protons برا كتنقص، وكيتكون le gradient de protons."},
       "explication": "ex_s4", "facile": "fa_s4"},
      {"id": "5", "texte": "Expliquer le retour de [H⁺] du milieu extérieur à sa valeur initiale et l'apparition d'ATP, puis nommer et définir le processus mis en évidence.",
       "texte_dit": "السؤال cinq: شرح علاش la concentration ديال les protons برا كترجع للvaleur initiale، وعلاش كيبان l'ATP. ومن بعد سمي وعرف هاد le processus.",
       "reponse": {"type": "phrase", "attendu": "Le dioxygène injecté est vite consommé : la chaîne s'arrête et le pompage cesse. Les H⁺ accumulés à l'intérieur des vésicules ressortent vers le milieu extérieur (côté matrice) en suivant le gradient, à travers les sphères pédonculées, seul passage dans la membrane interne : [H⁺] extérieure revient à sa valeur initiale. Ce retour des H⁺ permet aux sphères pédonculées (ATP synthases) de phosphoryler l'ADP : ADP + Pi → ATP. C'est la phosphorylation oxydative : la synthèse d'ATP par phosphorylation de l'ADP, couplée à l'oxydation des transporteurs réduits par la chaîne respiratoire, grâce au gradient de protons, au niveau de la membrane interne."},
       "clavier": {"aides": ["sphères pédonculées", "ATP synthase", "ADP + Pi → ATP", "phosphorylation oxydative", "couplée à l'oxydation", "membrane interne"], "pieges": ["à travers toute la membrane", "dans la matrice"]},
       "aides": [
         {"texte": "La membrane interne ne laisse pas passer les H⁺, sauf à un endroit. Par où les H⁺ de l'intérieur peuvent-ils ressortir ? Qu'y a-t-il à cet endroit ?",
          "dit": "la membrane interne ما كتخليش les protons يدوزو، غير من بلاصة وحدة. منين يقدرو يخرجو les protons ديال الداخل؟ وشنو كاين تما؟"},
         {"texte": "La définition : quel est le produit (ATP à partir d'ADP + Pi), avec quoi elle est couplée (oxydation des transporteurs réduits), grâce à quoi (gradient de H⁺), où (membrane interne).",
          "dit": "فالتعريف: شنو كيتصاوب، ATP من ADP و phosphate. مع شنو مرتبطة، l'oxydation ديال les transporteurs réduits. بشنو، le gradient ديال les protons. وفين، la membrane interne."}],
       "correction": {"lignes": [
           {"texte": "5 : O₂ consommé → pompage arrêté ; les H⁺ ressortent par les sphères pédonculées (seul passage)", "mot": "كيخرجو من les sphères pédonculées"},
           {"texte": "→ [H⁺] extérieure revient à sa valeur initiale", "mot": "كترجع للvaleur initiale"},
           {"texte": "→ ce retour permet aux ATP synthases de faire ADP + Pi → ATP", "mot": "ADP و phosphate كيوليو ATP"},
           {"texte": "phosphorylation oxydative : phosphorylation de l'ADP en ATP, couplée à l'oxydation des transporteurs réduits, grâce au gradient de protons (membrane interne)", "mot": "la phosphorylation oxydative"}],
         "parole": "السؤال cinq. le dioxygène تستهلك بالزربة: la chaîne وقفات، و le pompage وقف. les protons اللي تجمعو داخل، كيخرجو من les sphères pédonculées، حيت هي البلاصة الوحيدة اللي كيدوزو منها. إذن la concentration برا كترجع للvaleur initiale. وملي كيدوزو من les sphères، ADP و phosphate كيوليو ATP. هادي هي la phosphorylation oxydative. نعاود نقرا: la phosphorylation oxydative, c'est la phosphorylation de l'ADP en ATP, couplée à l'oxydation des transporteurs réduits, grâce au gradient de protons, au niveau de la membrane interne."},
       "explication": "ex_s5", "facile": "fa_s5"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : une vésicule à l'envers",
     "screen_content": {"lead": "Têtes des sphères dehors : dehors = côté matrice ; dedans = espace intermembranaire."},
     "visual": {"kind": "simulation", "url": VES, "caption": "Des ultrasons à la vésicule retournée"},
     "speech_text": {"mixed": "شوف la mitochondrie: les sphères pédonculées فوق la membrane interne، والراس ديالهم جهة la matrice. دابا les ultrasons: la membrane interne كتقطع لقطع صغار. شوف: القطعة كتسد، ولكن مقلوبة: les sphères ولاو برا. إذن الوجه اللي برا ديال la vésicule، هو الوجه ديال la matrice. و الداخل ديال la vésicule، هو l'espace intermembranaire."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "dans la mitochondrie : têtes des sphères côté matrice", "mot": "والراس ديالهم جهة la matrice"},
                  {"texte": "vésicule : sphères dehors → dehors = côté matrice", "mot": "هو الوجه ديال la matrice"},
                  {"texte": "dedans = espace intermembranaire", "mot": "هو l'espace intermembranaire"}],
       "pointage": [{"mot": "شوف la mitochondrie", "commande": "play_until", "parametres": {"moment": "manip_mitochondrie"}},
                    {"mot": "والراس ديالهم جهة la matrice", "cible": "centre:0"},
                    {"mot": "دابا les ultrasons", "commande": "play_until", "parametres": {"moment": "manip_ultrasons", "duree_s": 2.2}},
                    {"mot": "القطعة كتسد", "commande": "play_until", "parametres": {"moment": "manip_vesicule", "duree_s": 1.1}},
                    {"mot": "هو الوجه ديال la matrice", "commande": "play_until", "parametres": {"moment": "manip_cotes"}},
                    {"mot": "هو الوجه ديال la matrice", "cible": "centre:1"},
                    {"mot": "هو l'espace intermembranaire", "cible": "centre:2"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : deux conditions pour l'ATP",
     "screen_content": {"lead": "Pas de gradient : pas d'ATP. Pas de sphères : pas d'ATP."},
     "visual": {"kind": "simulation", "url": VES_CAS, "caption": "Les trois expériences, une à une"},
     "speech_text": {"mixed": "l'expérience A: نفس le pH داخل وبرا. شوف le compteur: ما كاينش l'ATP. l'expérience B: الداخل pH quatre، وبرا pH huit. الداخل فيه H plus كثر. شوف: les protons كيخرجو من les sphères، وكتصاوب l'ATP. l'expérience C: نفس le gradient، ولكن بلا sphères. شوف: ما كاينش l'ATP. إذن la synthèse ديال l'ATP خاصها جوج حوايج: le gradient de protons، و les sphères pédonculées."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "A : pH égaux → pas d'ATP", "mot": "ما كاينش l'ATP. l'expérience B"},
                  {"texte": "B : intérieur plus riche en H⁺ → ATP", "mot": "وكتصاوب l'ATP"},
                  {"texte": "C : sans sphères → pas d'ATP", "mot": "ولكن بلا sphères"},
                  {"texte": "conditions : gradient de protons + sphères pédonculées", "mot": "le gradient de protons، و les sphères pédonculées"}],
       "pointage": [{"mot": "نفس le pH داخل وبرا", "commande": "play_until", "parametres": {"moment": "ph_egaux_pas_d_atp", "duree_s": 2.2}},
                    {"mot": "ما كاينش l'ATP. l'expérience B", "cible": "centre:0"},
                    {"mot": "les protons كيخرجو من les sphères", "commande": "play_until", "parametres": {"moment": "interieur_acide_atp", "duree_s": 2.6}},
                    {"mot": "وكتصاوب l'ATP", "cible": "centre:1"},
                    {"mot": "ولكن بلا sphères", "commande": "play_until", "parametres": {"moment": "sans_spheres_pas_d_atp", "duree_s": 2.5}},
                    {"mot": "ولكن بلا sphères", "cible": "centre:2"},
                    {"mot": "le gradient de protons، و les sphères pédonculées", "commande": "play_until", "parametres": {"moment": "conclusion"}},
                    {"mot": "le gradient de protons، و les sphères pédonculées", "cible": "centre:3"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : le même phénomène, vu à l'envers",
     "screen_content": {"lead": "Mitochondrie : les H⁺ sortent dans la solution. Vésicule retournée : ils entrent, [H⁺] dehors diminue."},
     "visual": {"kind": "simulation", "url": PULSE, "caption": "Un peu d'O₂ injecté : la courbe de [H⁺]"},
     "speech_text": {"mixed": "شوف هاد l'expérience ديال الدرس: des mitochondries بلا membrane externe. قبل l'injection، la concentration ديال les protons stable. زدنا شوية ديال le dioxygène. شوف: كتطلع بالزربة، les protons خرجو من la matrice للsolution. ومن بعد كتنقص بشوية، حتى كترجع للvaleur initiale. فالvésicules ديال التمرين، كلشي مقلوب: جهة la matrice هي برا. إذن les protons كيدخلو للvésicules، و la concentration برا كتنقص، de cinquante à trente fois dix puissance moins neuf mole par litre. ومن بعد كيرجعو يخرجو، و la concentration كترجع à cinquante."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "vésicules retournées : côté matrice = dehors", "mot": "كلشي مقلوب"},
                  {"texte": "les H⁺ entrent dans les vésicules", "mot": "les protons كيدخلو للvésicules"},
                  {"texte": "[H⁺] dehors : 50 → 30 × 10⁻⁹ mol/L (à 80 s)", "mot": "و la concentration برا كتنقص"},
                  {"texte": "puis les H⁺ ressortent : retour à 50 × 10⁻⁹ mol/L", "mot": "و la concentration كترجع"}],
       "pointage": [{"mot": "قبل l'injection", "commande": "play_until", "parametres": {"moment": "avant_injection"}},
                    {"mot": "زدنا شوية ديال le dioxygène", "commande": "play_until", "parametres": {"moment": "o2_injecte"}},
                    {"mot": "كتطلع بالزربة", "commande": "play_until", "parametres": {"moment": "pic"}},
                    {"mot": "ومن بعد كتنقص بشوية", "commande": "play_until", "parametres": {"moment": "descente", "duree_s": 1}},
                    {"mot": "حتى كترجع للvaleur initiale", "commande": "play_until", "parametres": {"moment": "valeur_initiale", "duree_s": 1}},
                    {"mot": "كلشي مقلوب", "cible": "centre:0"},
                    {"mot": "les protons كيدخلو للvésicules", "cible": "centre:1"},
                    {"mot": "و la concentration برا كتنقص", "cible": "centre:2"},
                    {"mot": "و la concentration كترجع", "cible": "centre:3"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : le dioxygène relance la chaîne, les H⁺ sont pompés",
     "screen_content": {"lead": "O₂ accepteur final → NADH,H⁺ oxydé → électrons transférés → H⁺ pompés côté espace intermembranaire."},
     "visual": {"kind": "simulation", "url": CHAINE, "caption": "La chaîne respiratoire dans la membrane interne"},
     "speech_text": {"mixed": "شوف: جا N A D H, H plus من la matrice. طيح deux protons فla matrice، و deux électrons فT un: N A D H, H plus est oxydé. les électrons كيدوزو من transporteur ل transporteur. وفاللخر، le dioxygène خدا les électrons و des protons، وتكون l'eau: le dioxygène هو l'accepteur final. دابا شوف les protons: ملي كيدوزو les électrons، les protons كيطلعو من la matrice لl'espace intermembranaire. تجمعو بزاف الفوق: هادا le gradient de protons. فالvésicule، جهة la matrice هي برا: إذن les protons كيتحيدو من برا، و la concentration برا كتنقص."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "NADH,H⁺ → NAD⁺ + 2 H⁺ + 2 e⁻ (oxydation)", "mot": "N A D H, H plus est oxydé"},
                  {"texte": "½ O₂ + 2 H⁺ + 2 e⁻ → H₂O : O₂ accepteur final", "mot": "le dioxygène هو l'accepteur final"},
                  {"texte": "H⁺ pompés : matrice → espace intermembranaire", "mot": "les protons كيطلعو من la matrice"},
                  {"texte": "vésicule : H⁺ pris dehors → [H⁺] extérieure diminue", "mot": "la concentration برا كتنقص"}],
       "pointage": [{"mot": "جا N A D H, H plus من la matrice", "commande": "play_until", "parametres": {"moment": "taxi_arrive", "duree_s": 1.2}},
                    {"mot": "N A D H, H plus est oxydé", "commande": "play_until", "parametres": {"moment": "taxi_decharge"}},
                    {"mot": "N A D H, H plus est oxydé", "cible": "centre:0"},
                    {"mot": "les électrons كيدوزو من transporteur ل transporteur", "commande": "play_until", "parametres": {"moment": "electrons_passent"}},
                    {"mot": "le dioxygène خدا les électrons", "commande": "play_until", "parametres": {"moment": "o2_recoit"}},
                    {"mot": "le dioxygène هو l'accepteur final", "commande": "play_until", "parametres": {"moment": "o2_accepteur"}},
                    {"mot": "le dioxygène هو l'accepteur final", "cible": "centre:1"},
                    {"mot": "les protons كيطلعو من la matrice", "commande": "play_until", "parametres": {"moment": "protons_pompes"}},
                    {"mot": "les protons كيطلعو من la matrice", "cible": "centre:2"},
                    {"mot": "تجمعو بزاف الفوق", "commande": "play_until", "parametres": {"moment": "espace_charge"}},
                    {"mot": "هادا le gradient de protons", "commande": "play_until", "parametres": {"moment": "gradient_ecrit"}},
                    {"mot": "la concentration برا كتنقص", "cible": "centre:3"}]}},
    {"id": "ex_s5", "slide_type": "simulation", "title": "Question 5 : le retour par les sphères, et l'ATP",
     "screen_content": {"lead": "Les H⁺ reviennent par les sphères pédonculées : ADP + Pi → ATP (phosphorylation oxydative)."},
     "visual": {"kind": "simulation", "url": CHAINE_SPH, "caption": "Les protons repassent par la sphère pédonculée"},
     "speech_text": {"mixed": "دابا les protons بزاف فجهة l'espace intermembranaire. ما يقدروش يدوزو من la membrane interne. كاين غير باب واحد: la sphère pédonculée. شوف: les protons كيرجعو منها. وشوف عند الراس: ADP و phosphate ولاو ATP. هادي هي la phosphorylation oxydative. فالvésicule، les protons كيرجعو يخرجو للبرا من les sphères، ولهذا la concentration برا كترجع للvaleur initiale، وكيبان l'ATP. نعاود نقرا: la phosphorylation oxydative, c'est la phosphorylation de l'ADP en ATP, couplée à l'oxydation des transporteurs réduits, grâce au gradient de protons."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "seul passage des H⁺ : la sphère pédonculée (ATP synthase)", "mot": "كاين غير باب واحد"},
                  {"texte": "ADP + Pi → ATP", "mot": "ADP و phosphate ولاو ATP"},
                  {"texte": "vésicule : H⁺ ressortent → [H⁺] extérieure revient à sa valeur initiale", "mot": "la concentration برا كترجع للvaleur initiale"},
                  {"texte": "phosphorylation oxydative = ADP → ATP, couplée à l'oxydation des transporteurs réduits, grâce au gradient", "mot": "نعاود نقرا"}],
       "pointage": [{"mot": "كاين غير باب واحد", "cible": "centre:0"},
                    {"mot": "les protons كيرجعو منها", "commande": "play_until", "parametres": {"moment": "retour_par_la_sphere"}},
                    {"mot": "ADP و phosphate ولاو ATP", "commande": "play_until", "parametres": {"moment": "atp_forme"}},
                    {"mot": "ADP و phosphate ولاو ATP", "cible": "centre:1"},
                    {"mot": "la concentration برا كترجع للvaleur initiale", "cible": "centre:2"},
                    {"mot": "نعاود نقرا", "cible": "centre:3"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : où sont les têtes des sphères ?", "نتمرنو بسؤال ساهل على les sphères pédonculées.",
      "Dans la mitochondrie, les têtes des sphères pédonculées sont tournées vers…", ["l'espace intermembranaire", "la matrice", "le hyaloplasme"], 1, {
        "1": {"juste": rep("برافو! الراس ديال les sphères ديما جهة la matrice.", "Juste : les têtes sont côté matrice.")},
        "0": {"1": rep("ما تقلقش. l'espace intermembranaire هو فين كيتجمعو les protons. الراس كيكون فالجهة الأخرى. عاود اختار.", "C'est là que s'accumulent les H⁺ ; les têtes sont de l'autre côté. Réessaie."),
              "2": rep("الجواب هو la matrice. الراس ديال les sphères ديما جهة la matrice.", "Réponse : la matrice.")},
        "2": {"1": rep("لا، les sphères كاينين على la membrane interne، داخل la mitochondrie. عاود اختار.", "Les sphères sont sur la membrane interne, dans la mitochondrie. Réessaie."),
              "2": rep("الجواب هو la matrice، الداخل ديال la mitochondrie.", "Réponse : la matrice.")}},
      "Dans la mitochondrie, les têtes des sphères pédonculées sont tournées vers ?"),
    association("fa_s2", "Plus facile : chaque expérience et son explication", "Relie chaque expérience à ce qui l'explique.",
      "سؤال ساهل: ربط كل expérience مع الشرح ديالها.", "Relie chaque expérience à son explication.",
      [("1", "A : pH 7,5 dedans et dehors, sphères présentes"), ("2", "B : pH 4 dedans, pH 8 dehors, sphères présentes"), ("3", "C : pH 4 dedans, pH 8 dehors, sans sphères")],
      [("a", "ATP produit : gradient de H⁺ et sphères présents"), ("b", "Pas d'ATP : pas de gradient de H⁺"), ("c", "Pas d'ATP : pas de sphères pédonculées")],
      {"1": "b", "2": "a", "3": "c"}, {
        "1-a": (False, "Non : en A, le pH est le même des deux côtés, il n'y a pas de gradient.", "لا، فA نفس le pH من جوج الجهات، ما كاينش le gradient."),
        "1-b": (True, "Oui : pH égaux, pas de gradient, donc pas d'ATP.", "برافو: نفس le pH، ما كاينش le gradient، إذن ما كاينش l'ATP."),
        "1-c": (False, "Non : en A, les sphères sont présentes ; c'est le gradient qui manque.", "لا، فA les sphères كاينين، اللي ناقص هو le gradient."),
        "2-a": (True, "Oui : intérieur plus riche en H⁺ et sphères présentes : ATP produit.", "برافو: الداخل فيه H plus كثر، و les sphères كاينين: كتصاوب l'ATP."),
        "2-b": (False, "Non : en B, il y a un gradient (pH 4 dedans, pH 8 dehors).", "لا، فB كاين le gradient، pH quatre داخل و pH huit برا."),
        "2-c": (False, "Non : en B, les sphères sont présentes, et de l'ATP est produit.", "لا، فB les sphères كاينين، وكتصاوب l'ATP."),
        "3-a": (False, "Non : en C, il n'y a pas d'ATP.", "لا، فC ما كاينش l'ATP."),
        "3-b": (False, "Non : en C, le gradient existe (pH 4 / pH 8) ; c'est autre chose qui manque.", "لا، فC le gradient كاين. شي حاجة أخرى اللي ناقصة."),
        "3-c": (True, "Oui : même gradient qu'en B, mais sans sphères : pas d'ATP.", "برافو: نفس le gradient، ولكن بلا sphères: ما كاينش l'ATP.")},
      ("(1 ; b) (2 ; a) (3 ; c) : il faut un gradient de H⁺ ET des sphères pédonculées.", "خاص le gradient de protons، و les sphères pédonculées، بجوج.")),
    qcm_facile("fa_s3", "Plus facile : juste après le dioxygène", "سؤال ساهل على la courbe ديال le document deux.",
      "Juste après l'injection de dioxygène, [H⁺] du milieu extérieur…", ["augmente rapidement", "diminue rapidement", "reste stable"], 1, {
        "1": {"juste": rep("برافو! كتنقص بالزربة: les protons كيدخلو للvésicules.", "Juste : [H⁺] diminue rapidement ; les H⁺ entrent dans les vésicules.")},
        "0": {"1": rep("ما تقلقش. هادا هو اللي كيوقع مع mitochondrie بلا membrane externe. هنا شوف la courbe: واش كتطلع ولا كتهبط؟ عاود اختار.", "C'est ce qu'on voit avec des mitochondries ; ici, regarde : la courbe monte-t-elle ? Réessaie."),
              "2": rep("الجواب هو كتنقص بالزربة. les vésicules مقلوبين، les protons كيدخلو ليهم.", "Réponse : [H⁺] diminue rapidement.")},
        "2": {"1": rep("stable غير قبل le dioxygène. après soixante secondes، شنو كيوقع؟ عاود اختار.", "Elle n'est stable qu'avant l'injection. Après 60 s ? Réessaie."),
              "2": rep("الجواب هو كتنقص بالزربة، jusqu'à trente fois dix puissance moins neuf mole par litre.", "Réponse : elle diminue rapidement jusqu'à 30 × 10⁻⁹ mol/L.")}},
      "Juste après l'injection de dioxygène, la concentration des protons dehors ?"),
    association("fa_s4", "Plus facile : le sens des protons", "Relie chaque structure au sens des H⁺.",
      "سؤال ساهل: ربط كل structure مع الاتجاه ديال les protons.", "Relie chaque structure au sens de déplacement des H⁺ qu'elle permet.",
      [("1", "Chaîne respiratoire (transporteurs)"), ("2", "Sphère pédonculée (ATP synthase)")],
      [("a", "De la matrice vers l'espace intermembranaire"), ("b", "De l'espace intermembranaire vers la matrice"), ("c", "À travers la membrane externe")],
      {"1": "a", "2": "b"}, {
        "1-a": (True, "Oui : en transférant les électrons, la chaîne pompe les H⁺ de la matrice vers l'espace intermembranaire.", "برافو: la chaîne كتطلع les protons من la matrice ل l'espace intermembranaire."),
        "1-b": (False, "Non : ce retour vers la matrice se fait par la sphère pédonculée.", "لا، الرجوع ل la matrice كيكون من la sphère pédonculée."),
        "1-c": (False, "Non : la chaîne respiratoire est dans la membrane interne, pas la membrane externe.", "لا، la chaîne respiratoire فla membrane interne، ماشي فla membrane externe."),
        "2-a": (False, "Non : la sphère ramène les H⁺ ; ce sont les transporteurs qui les sortent de la matrice.", "لا، la sphère كترجع les protons. les transporteurs هوما اللي كيخرجوهم من la matrice."),
        "2-b": (True, "Oui : les H⁺ reviennent vers la matrice par la sphère pédonculée, et l'ATP se forme.", "برافو: les protons كيرجعو ل la matrice من la sphère، وكتصاوب l'ATP."),
        "2-c": (False, "Non : la sphère pédonculée est sur la membrane interne.", "لا، la sphère pédonculée على la membrane interne.")},
      ("(1 ; a) (2 ; b) : la chaîne sort les H⁺ de la matrice, la sphère les ramène.", "la chaîne كتخرج les protons من la matrice، و la sphère كترجعهم.")),
    qcm_facile("fa_s5", "Plus facile : où se fait la phosphorylation oxydative ?", "سؤال ساهل على la phosphorylation oxydative.",
      "La phosphorylation oxydative se fait…", ["dans la matrice", "dans l'espace intermembranaire", "au niveau de la membrane interne (sphères pédonculées)"], 2, {
        "2": {"juste": rep("برافو! la phosphorylation oxydative كتوقع فla membrane interne، عند les sphères pédonculées.", "Juste : au niveau de la membrane interne.")},
        "0": {"1": rep("قريب، الراس ديال la sphère جهة la matrice، ولكن la sphère راكبة فواحد la membrane. شمن membrane؟ عاود اختار.", "La tête est côté matrice, mais la sphère est fixée sur une membrane. Laquelle ? Réessaie."),
              "2": rep("الجواب هو la membrane interne. la matrice فيها le cycle de Krebs.", "Réponse : la membrane interne ; la matrice, c'est le cycle de Krebs.")},
        "1": {"1": rep("لا، l'espace intermembranaire غير فين كيتجمعو les protons. عاود اختار.", "L'espace intermembranaire est seulement là où s'accumulent les H⁺. Réessaie."),
              "2": rep("الجواب هو la membrane interne، عند les sphères pédonculées.", "Réponse : la membrane interne.")}},
      "La phosphorylation oxydative se fait où ?")
  ]}]},
  "similaire": {
    "id": "svt_ex_ch1_chaine_respiratoire_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Mêmes vésicules de membrane interne, sphères pédonculées tournées vers l'extérieur. Expérience 1 : trois nouvelles conditions (document 1 b). Expérience 2 : vésicules entières dans une solution sans dioxygène, riche en NADH,H⁺ et en ADP + Pi ; un peu de dioxygène, vite consommé, est injecté à t = 80 s (document 2) ; de l'ATP apparaît ensuite dans le milieu.",
      "intro_dit": "نفس les vésicules. فl'expérience une، trois conditions جداد. فl'expérience deux، زدنا شوية ديال le dioxygène à quatre-vingts secondes، ومن بعد بان l'ATP.",
      "figures": [FIG_V, FIG_TS, FIG_HS],
      "donnees": ["Solution sans O₂, riche en NADH,H⁺ et ADP + Pi ; un peu d'O₂ injecté à t = 80 s",
                  "Après l'injection, de l'ATP apparaît dans le milieu extérieur",
                  "La membrane interne est imperméable aux protons H⁺, sauf au niveau des sphères pédonculées"],
      "questions": [
        {"id": "1", "texte": "Préciser à quelle face de la membrane interne correspond la face extérieure de la vésicule, puis à quel compartiment correspond l'intérieur. Justifier.",
         "reponse": {"type": "phrase", "attendu": "Les têtes des sphères pédonculées sont toujours côté matrice ; ici elles sont dehors : la face extérieure est la face matricielle, l'intérieur correspond à l'espace intermembranaire."},
         "clavier": {"aides": ["côté matrice", "espace intermembranaire"], "pieges": ["hyaloplasme"]},
         "correction": {"lignes": [{"texte": "1 : têtes des sphères côté matrice ; ici dehors : dehors = face matricielle", "mot": "جهة la matrice"},
                                   {"texte": "intérieur = espace intermembranaire", "mot": "l'espace intermembranaire"}],
                        "parole": "الراس ديال les sphères ديما جهة la matrice، وهنا برا. إذن برا هو جهة la matrice، و الداخل هو l'espace intermembranaire."}},
        {"id": "2", "texte": "Comparer les résultats des expériences A et B, puis B et C (document 1 b). Déduire les conditions nécessaires à la synthèse d'ATP.",
         "reponse": {"type": "phrase", "attendu": "A et B (même gradient, pH 4,5 dedans / 8 dehors) : pas d'ATP en A sans sphères, alors que B avec sphères produit de l'ATP. B et C (sphères présentes) : ATP en B avec un intérieur plus riche en H⁺, alors qu'en C (pH 8 / 8, pas de gradient) pas d'ATP. On en déduit que la synthèse d'ATP nécessite des sphères pédonculées et un gradient de protons."},
         "clavier": {"aides": ["alors que", "gradient de protons", "sphères pédonculées", "On en déduit que"], "pieges": ["le dioxygène"]},
         "correction": {"lignes": [{"texte": "2 : A (sans sphères) : pas d'ATP, alors que B (sphères) : ATP → il faut les sphères", "mot": "خاص les sphères"},
                                   {"texte": "C (pH 8 / 8) : pas d'ATP, alors que B (pH 4,5 / 8) : ATP → il faut un gradient de H⁺", "mot": "خاص le gradient"}],
                        "parole": "A بلا sphères ما كاينش l'ATP، alors que B فيه: خاص les sphères. C بلا gradient ما كاينش l'ATP، alors que B فيه: خاص le gradient de protons."}},
        {"id": "3", "texte": "Décrire l'évolution de [H⁺] du milieu extérieur (document 2), puis déduire le sens de déplacement des protons après l'injection de dioxygène.",
         "reponse": {"type": "phrase", "attendu": "Avant 80 s, [H⁺] est stable à 40 × 10⁻⁹ mol/L. Après l'injection de O₂, elle diminue rapidement jusqu'à 24 × 10⁻⁹ mol/L à 100 s, puis augmente progressivement et revient à 40 × 10⁻⁹ mol/L vers 300 s. On en déduit que les H⁺ entrent dans les vésicules, puis en ressortent."},
         "clavier": {"aides": ["stable", "diminue rapidement", "augmente progressivement", "× 10⁻⁹ mol/L"], "pieges": ["nulle"]},
         "correction": {"lignes": [{"texte": "3 : stable à 40 × 10⁻⁹ mol/L, puis diminue jusqu'à 24 × 10⁻⁹ mol/L à 100 s", "mot": "jusqu'à vingt-quatre fois dix puissance moins neuf"},
                                   {"texte": "puis revient à 40 × 10⁻⁹ mol/L ; les H⁺ entrent dans les vésicules puis ressortent", "mot": "on en déduit que"}],
                        "parole": "stable à quarante fois dix puissance moins neuf mole par litre، ومن بعد le dioxygène كتنقص jusqu'à vingt-quatre fois dix puissance moins neuf، à cent secondes، ومن بعد كترجع à quarante. on en déduit que les protons كيدخلو للvésicules، ومن بعد كيخرجو."}},
        {"id": "4", "texte": "Expliquer la diminution de [H⁺] du milieu extérieur juste après l'injection de dioxygène.",
         "reponse": {"type": "phrase", "attendu": "O₂, accepteur final des électrons, permet le fonctionnement de la chaîne respiratoire → NADH,H⁺ oxydé → électrons transférés jusqu'à O₂ (H₂O) → pompage des H⁺ du côté matrice (extérieur) vers le côté espace intermembranaire (intérieur) → [H⁺] extérieure diminue."},
         "clavier": {"aides": ["accepteur final", "pompage des H⁺", "côté matrice"], "pieges": ["sphères"]},
         "correction": {"lignes": [{"texte": "4 : O₂ accepteur final → NADH,H⁺ oxydé → transfert des électrons", "mot": "l'accepteur final"},
                                   {"texte": "→ pompage des H⁺ de l'extérieur (côté matrice) vers l'intérieur → [H⁺] extérieure diminue", "mot": "le pompage"}],
                        "parole": "le dioxygène هو l'accepteur final: la chaîne كتخدم، N A D H, H plus كيتأكسد، les électrons كيدوزو، وكاين le pompage ديال les protons من برا، جهة la matrice، للداخل."}},
        {"id": "5", "texte": "Expliquer le retour de [H⁺] du milieu extérieur à sa valeur initiale et l'apparition d'ATP, puis nommer et définir le processus mis en évidence.",
         "reponse": {"type": "phrase", "attendu": "O₂ consommé : le pompage s'arrête ; les H⁺ ressortent par les sphères pédonculées (seul passage) : [H⁺] extérieure revient à sa valeur initiale, et ce retour permet ADP + Pi → ATP. C'est la phosphorylation oxydative : phosphorylation de l'ADP en ATP, couplée à l'oxydation des transporteurs réduits, grâce au gradient de protons (membrane interne)."},
         "clavier": {"aides": ["sphères pédonculées", "ADP + Pi → ATP", "phosphorylation oxydative"], "pieges": ["dans la matrice"]},
         "correction": {"lignes": [{"texte": "5 : retour des H⁺ par les sphères pédonculées → ADP + Pi → ATP", "mot": "من les sphères pédonculées"},
                                   {"texte": "phosphorylation oxydative : ADP → ATP, couplée à l'oxydation des transporteurs réduits, grâce au gradient", "mot": "la phosphorylation oxydative"}],
                        "parole": "les protons كيرجعو يخرجو من les sphères pédonculées، وكتصاوب l'ATP. هادي la phosphorylation oxydative."}}
      ]}}
}

ecrire(EX, sys.argv[1])
