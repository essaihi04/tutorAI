# Exercice SVT ch. 1 (libération de l'énergie), niveau facile : des mitochondries isolées en ExAO.
# Ce qu'il entraîne : décrire une courbe ExAO par périodes bornées par les ajouts (avec valeurs), déduire que la
# mitochondrie utilise l'acide pyruvique et non le glucose, situer la glycolyse (hyaloplasme) et l'oxydation de l'acide
# pyruvique (mitochondrie, matrice), légender la mitochondrie.
# Sources comparées (lecture seulement, rien de copié) :
# - exploration du cours : cas_types « mitochondries_isolees » (2016 R, 2019 N, 2020 R, 2021 R, 2025 N), pièges « le glucose
#   entre dans la mitochondrie », « conclut alors qu'on demande de décrire », a_ne_pas_dire (glucose → mitochondrie) ;
# - vidéo exercices Ouissam SVT (Uq0n3z9j4-c, mitochondries isolées, méthode décrire / déduire) via l'exploration ;
# - nationaux 2016 R, 2019 N, 2020 R (suspension de mitochondries, ajouts successifs, O2 et ATP) : on garde la forme
#   « décrire puis déduire », sans leur situation (pas d'ADP + Pi, pas de cyanure, pas d'ATP mesuré, autres temps et valeurs) ;
# - séries en ligne (recherche du 22/11/2026 : dyrassa « Exercice Energie », moutamadris résumé 2BAC SP, ayoubsvt) : seuls les
#   extraits des résultats de recherche ont pu être lus (dyrassa.com et khabzox.github.io bloqués par le réseau) : dispositif
#   classique glucose à t1 puis pyruvate à t2, interprétation « pyruvate utilisé, glucose dégradé dans le cytosol ».
# Pas de recouvrement : svt_ex_ch1_conditions_mitochondrie_1 (autre agent) traite ADP + Pi et le couplage O2 / ATP.
import sys, math
sys.path.insert(0, __import__("os").path.dirname(__file__))
from _commun_svt import rep, qcm_facile, vrai_faux, association, ecrire

D = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/"
EXAO = D + "exao.html?vue=mitochondries&depart=0"
PYR = D + "pyruvate.html?depart=0"
MITO = D + "mitochondrie.html?depart=0"


def courbe_o2(t_glu, t_pyr, pente, titre):
    """[O2] (%) : stable à 100 %, rien après le glucose, diminution linéaire après l'acide pyruvique."""
    fin = 100 - pente * (12 - t_pyr)
    return {"type": "courbe", "titre": titre,
            "axes": {"x": {"min": 0, "max": 12, "nom": "t", "unite": "min", "graduations": list(range(0, 13, 1))},
                     "y": {"min": 0, "max": 100, "nom": "[O₂]", "unite": "%", "graduations": list(range(0, 101, 10))}},
            "legende": "Concentration du dioxygène dans la suspension de mitochondries (100 % au départ), mesurée par la sonde (ExAO).",
            "elements": [
              {"f": "courbe", "expr": "100", "de": 0, "a": t_pyr, "couleur": "cyan"},
              {"f": "courbe", "expr": f"100-{pente:.6f}*(x-{t_pyr})", "de": t_pyr, "a": 12, "couleur": "cyan", "texte": "[O₂]", "texte_x": 11, "pos": "ne"},
              {"f": "fleche", "de": [t_glu, 60], "a": [t_glu, 96], "couleur": "jaune", "texte": "glucose", "pos": "o"},
              {"f": "fleche", "de": [t_pyr, 60], "a": [t_pyr, 96], "couleur": "orange", "texte": "acide pyruvique", "pos": "e"},
              {"f": "repere", "x": 12, "y": fin}]}, fin


def schema_mito(numeros, titre):
    """Mitochondrie en coupe : membrane externe, membrane interne avec ses crêtes, matrice.
    `numeros` : {"membrane_externe": n, "membrane_interne": n, "crete": n, "matrice": n}."""
    cx, cy, RX, RY, rx, ry = 5.0, 3.0, 4.2, 2.3, 3.85, 1.95
    el = [{"f": "ellipse", "c": [cx, cy], "rx": RX, "ry": RY, "couleur": "orange"},
          {"f": "ellipse", "c": [cx, cy], "rx": rx, "ry": ry, "couleur": "jaune"}]
    y_int = lambda x: ry * math.sqrt(max(0.0, 1 - ((x - cx) / rx) ** 2))
    for x, bas in [(2.6, True), (4.4, True), (6.2, True), (3.5, False), (5.3, False), (7.1, False)]:
        y0 = cy - y_int(x) if bas else cy + y_int(x)
        y1 = cy - 0.1 if bas else cy + 0.1
        y0, y1 = round(y0, 2), round(y1, 2)
        el.append({"f": "ligne", "pts": [[x - 0.17, y0], [x - 0.17, y1], [x + 0.17, y1], [x + 0.17, y0]], "couleur": "jaune"})
    # flèches de légende (pointes sur la structure) et numéros
    pointes = {"membrane_externe": ([1.2, 5.6], [2.3, 4.75]), "membrane_interne": ([0.5, 1.0], [1.45, 2.3]),
               "crete": ([8.9, 0.4], [7.3, 3.5]), "matrice": ([9.4, 5.6], [6.3, 3.6])}
    for cle, (de, a) in pointes.items():
        el.append({"f": "fleche", "de": de, "a": a, "couleur": "blanc"})
        el.append({"f": "texte", "at": [de[0] + (-0.25 if de[0] < 5 else 0.25), de[1] + 0.05], "t": str(numeros[cle]), "couleur": "blanc", "taille": "grand"})
    return {"type": "schema", "titre": titre, "cadre": {"l": 10, "h": 6},
            "legende": "Schéma d'une mitochondrie observée au microscope électronique (coupe).", "elements": el}


FIG1, FIN1 = courbe_o2(2, 5, 15 / 7, "Document 1 : [O₂] dans la suspension de mitochondries")
FIG2 = schema_mito({"membrane_externe": 1, "membrane_interne": 2, "crete": 3, "matrice": 4}, "Document 2 : une mitochondrie")
FIGS, FINS = courbe_o2(3, 6, 2, "Document 1 : [O₂] dans la suspension de mitochondries")
FIG2S = schema_mito({"membrane_externe": 4, "membrane_interne": 3, "crete": 2, "matrice": 1}, "Document 2 : une mitochondrie")
assert abs(FIN1 - 85) < 1e-9 and abs(FINS - 88) < 1e-9

EX = {
  "id": "svt_ex_ch1_mitochondries_1", "type": "exercice", "version": 1, "status": "published",
  "matiere": "svt", "chapitre": "reactions_responsables_liberation_energie", "cours": "svt_ch1_reactions_responsables_liberation_energie",
  "titre": "Des mitochondries isolées : glucose ou acide pyruvique ?", "niveau": "facile", "duree_min": 20,
  "origine": "Exercice original écrit pour Moalim (ni sujet du national, ni copie d'un livre).",
  "competences": ["Décrire une courbe ExAO par périodes", "Localiser la glycolyse et l'oxydation de l'acide pyruvique", "Légender la mitochondrie"],
  "enonce": {
    "intro": "On isole des mitochondries de cellules de foie et on les place dans une solution riche en dioxygène. Une sonde mesure la concentration du dioxygène [O₂] (en % de la valeur de départ). À t = 2 min, on ajoute du glucose ; à t = 5 min, on ajoute de l'acide pyruvique. On sait que, dans une cellule entière, le glucose est consommé en présence de dioxygène. Le document 1 montre l'évolution de [O₂] ; le document 2 représente une mitochondrie.",
    "intro_dit": "دابا نقراو l'énoncé. خرجنا des mitochondries من les cellules ديال le foie، وحطيناهم فsolution فيها بزاف ديال le dioxygène. une sonde كتقيس la concentration ديال le dioxygène، بالpourcentage. à deux minutes، زدنا le glucose. ومن بعد، à cinq minutes، زدنا l'acide pyruvique. وكنعرفو بلي la cellule كاملة كتستهلك le glucose، ملي كاين le dioxygène. le document un فيه la courbe ديال le dioxygène، و le document deux فيه واحد la mitochondrie.",
    "figures": [FIG1, FIG2],
    "donnees": ["Mitochondries isolées dans une solution riche en O₂ ; [O₂] = 100 % au départ",
                "Ajout de glucose à t = 2 min ; ajout d'acide pyruvique à t = 5 min",
                "Dans une cellule entière, le glucose est consommé en présence de dioxygène"],
    "questions": [
      {"id": "1", "texte": "Décrire l'évolution de [O₂] avant l'ajout du glucose, après l'ajout du glucose, puis après l'ajout de l'acide pyruvique.",
       "texte_dit": "السؤال un: وصف l'évolution ديال la concentration ديال le dioxygène، قبل le glucose، من بعد le glucose، ومن بعد l'acide pyruvique.",
       "reponse": {"type": "phrase", "attendu": "Avant 2 min, [O₂] reste stable à 100 %. Après l'ajout du glucose (de 2 à 5 min), [O₂] reste stable à 100 %. Après l'ajout de l'acide pyruvique (à 5 min), [O₂] diminue, de 100 % à 85 % à 12 min."},
       "clavier": {"aides": ["reste stable", "diminue", "100 %", "85 %", "Avant…", "Après l'ajout…"], "pieges": ["augmente", "s'annule"]},
       "aides": [
         {"texte": "Les deux flèches (glucose, acide pyruvique) coupent la courbe en trois périodes : avant 2 min, de 2 à 5 min, après 5 min.",
          "dit": "les deux flèches كيقسمو la courbe لثلاث ديال المراحل: avant deux minutes، entre deux et cinq minutes، و après cinq minutes."},
         {"texte": "Pour chaque période : le sens (stable, diminue) et les valeurs lues sur l'axe de [O₂] (au début et à la fin).",
          "dit": "فكل مرحلة، قول واش ثابتة ولا كتنقص، وعطي les valeurs اللي كتقرا على l'axe، فالبداية وفاللخر."}],
       "correction": {"lignes": [
           {"texte": "1 : avant 2 min : [O₂] stable à 100 %", "mot": "stable à cent pour cent"},
           {"texte": "après le glucose (2 à 5 min) : [O₂] reste stable à 100 %", "mot": "كتبقى stable"},
           {"texte": "après l'acide pyruvique : [O₂] diminue, de 100 % à 85 % à 12 min", "mot": "de cent à quatre-vingt-cinq pour cent"}],
         "parole": "السؤال un. avant deux minutes، la concentration ديال le dioxygène stable à cent pour cent. من بعد le glucose، كتبقى stable، ما تبدل والو. من بعد l'acide pyruvique، كتنقص، de cent à quatre-vingt-cinq pour cent، à douze minutes."},
       "explication": "ex_s1", "facile": "fa_s1"},
      {"id": "2", "texte": "Déduire la molécule que les mitochondries utilisent en consommant le dioxygène. Justifier.",
       "texte_dit": "السؤال deux: استنتج شمن molécule كيستعملو les mitochondries ملي كيستهلكو le dioxygène. برر.",
       "reponse": {"type": "phrase", "attendu": "Les mitochondries n'utilisent pas le glucose, car [O₂] ne change pas après son ajout. Elles utilisent l'acide pyruvique, car [O₂] diminue après son ajout : elles oxydent l'acide pyruvique en consommant le dioxygène."},
       "clavier": {"aides": ["n'utilisent pas le glucose", "acide pyruvique", "car [O₂]", "consomment le dioxygène"], "pieges": ["le glucose entre dans la mitochondrie"]},
       "aides": [
         {"texte": "Regarde ce que fait [O₂] juste après chaque ajout : une molécule utilisée avec le dioxygène fait baisser [O₂].",
          "dit": "شوف شنو كتدير la concentration ديال le dioxygène من بعد كل زيادة. la molécule اللي كتستعمل مع le dioxygène، كتنقص la concentration ديالو."},
         {"texte": "Écris deux phrases : « les mitochondries n'utilisent pas … car … » puis « elles utilisent … car … ».",
          "dit": "كتب جوج جمل: les mitochondries n'utilisent pas، ومن بعد car. ومن بعد: elles utilisent، و car."}],
       "correction": {"lignes": [
           {"texte": "2 : après le glucose, [O₂] ne change pas : le glucose n'est pas utilisé", "mot": "le glucose ما كيتستعملش"},
           {"texte": "après l'acide pyruvique, [O₂] diminue : l'acide pyruvique est utilisé", "mot": "l'acide pyruvique كيتستعمل"},
           {"texte": "donc les mitochondries oxydent l'acide pyruvique en consommant le dioxygène", "mot": "كيأكسدو l'acide pyruvique"}],
         "parole": "السؤال deux. من بعد le glucose، la concentration ديال le dioxygène ما تبدلاتش: إذن le glucose ما كيتستعملش. من بعد l'acide pyruvique، كتنقص: إذن l'acide pyruvique كيتستعمل. donc les mitochondries كيأكسدو l'acide pyruvique، وكيستهلكو le dioxygène."},
       "explication": "ex_s2", "facile": "fa_s2"},
      {"id": "3", "texte": "En utilisant le résultat de la question 2 et les données, déduire le lieu de la glycolyse et le lieu de l'oxydation de l'acide pyruvique dans la cellule.",
       "texte_dit": "السؤال trois: بالجواب ديال السؤال deux وبles données، استنتج فين كتوقع la glycolyse، وفين كيتأكسد l'acide pyruvique فla cellule.",
       "reponse": {"type": "phrase", "attendu": "La cellule consomme le glucose mais la mitochondrie ne l'utilise pas : la glycolyse (glucose → 2 acides pyruviques) se fait hors de la mitochondrie, dans le hyaloplasme. L'acide pyruvique formé entre dans la mitochondrie, où il est oxydé en présence de dioxygène (dans la matrice)."},
       "clavier": {"aides": ["glycolyse", "hyaloplasme", "acide pyruvique", "mitochondrie", "matrice"], "pieges": ["noyau", "membrane externe"]},
       "aides": [
         {"texte": "La cellule entière consomme le glucose, la mitochondrie seule ne l'utilise pas. Où le glucose est-il donc transformé ?",
          "dit": "la cellule كاملة كتستهلك le glucose، و la mitochondrie بوحدها ما كتستعملوش. إذن فين كيتحول le glucose؟"},
         {"texte": "La glycolyse transforme le glucose en acide pyruvique. Le compartiment de la cellule hors des organites s'appelle le hyaloplasme.",
          "dit": "la glycolyse كتحول le glucose ل l'acide pyruvique. والجزء ديال la cellule اللي برا من les organites، سميتو le hyaloplasme."}],
       "correction": {"lignes": [
           {"texte": "3 : la cellule consomme le glucose, la mitochondrie ne l'utilise pas", "mot": "la mitochondrie ما كتستعملوش"},
           {"texte": "donc la glycolyse (glucose → 2 acides pyruviques) se fait dans le hyaloplasme", "mot": "la glycolyse كتوقع فle hyaloplasme"},
           {"texte": "l'acide pyruvique entre dans la mitochondrie, où il est oxydé (matrice)", "mot": "كيدخل للmitochondrie"}],
         "parole": "السؤال trois. la cellule كتستهلك le glucose، ولكن la mitochondrie ما كتستعملوش. إذن la glycolyse كتوقع فle hyaloplasme، برا من la mitochondrie: le glucose كيعطي deux acides pyruviques. من بعد، l'acide pyruvique كيدخل للmitochondrie، وتما كيتأكسد، فla matrice، مع le dioxygène."},
       "explication": "ex_s3", "facile": "fa_s3"},
      {"id": "4", "texte": "Nommer les éléments 1, 2, 3 et 4 du document 2, puis préciser le compartiment où l'acide pyruvique est dégradé.",
       "texte_dit": "السؤال quatre: سمي les éléments un، deux، trois، et quatre ديال le document deux، ومن بعد قول فين كيتفكك l'acide pyruvique.",
       "reponse": {"type": "phrase", "attendu": "1 : membrane externe ; 2 : membrane interne ; 3 : crête ; 4 : matrice. L'acide pyruvique est dégradé dans la matrice (4)."},
       "clavier": {"aides": ["membrane externe", "membrane interne", "crête", "matrice"], "pieges": ["espace intermembranaire", "hyaloplasme", "noyau"]},
       "aides": [
         {"texte": "Va de l'extérieur vers l'intérieur : la première enveloppe, la deuxième, ses replis, puis tout ce qui est à l'intérieur.",
          "dit": "بدا من برا للداخل: الغشاء اللول، الغشاء التاني، les replis ديالو، ومن بعد داكشي اللي داخل."},
         {"texte": "Les replis de la membrane interne s'appellent les crêtes ; l'intérieur de la mitochondrie s'appelle la matrice.",
          "dit": "les replis ديال la membrane interne سميتهم les crêtes. والداخل ديال la mitochondrie سميتو la matrice."}],
       "correction": {"lignes": [
           {"texte": "4 : 1 membrane externe ; 2 membrane interne", "mot": "un la membrane externe"},
           {"texte": "3 crête ; 4 matrice", "mot": "trois la crête"},
           {"texte": "l'acide pyruvique est dégradé dans la matrice (4)", "mot": "كيتفكك فla matrice"}],
         "parole": "السؤال quatre. un la membrane externe، deux la membrane interne، trois la crête، et quatre la matrice. و l'acide pyruvique كيتفكك فla matrice: le numéro quatre."},
       "explication": "ex_s4", "facile": "fa_s4"}
    ]
  },
  "explication": {"activities": [{"id": "explication", "title": "Explication animée", "slides": [
    {"id": "ex_s1", "slide_type": "simulation", "title": "Question 1 : trois périodes, bornées par les ajouts",
     "screen_content": {"lead": "Stable avant, stable après le glucose, diminue après l'acide pyruvique."},
     "visual": {"kind": "simulation", "url": EXAO, "caption": "Mitochondries isolées : la sonde et la courbe de [O₂]"},
     "speech_text": {"mixed": "شوف le montage: des mitochondries بوحدهم فsolution فيها le dioxygène. la courbe كتبدا stable à cent pour cent. دابا كنزيدو le glucose. شوف: la courbe بقات stable، ما تبدل والو. من بعد كنزيدو l'acide pyruvique. شوف: le dioxygène بدا كينقص. فle document ديال التمرين، كينقص jusqu'à quatre-vingt-cinq pour cent، à douze minutes. إذن ثلاث ديال المراحل، كل وحدة بين جوج زيادات: stable، من بعد stable، من بعد كينقص."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "avant 2 min : [O₂] stable à 100 %", "mot": "la courbe كتبدا stable"},
                  {"texte": "après le glucose : [O₂] reste stable", "mot": "la courbe بقات stable"},
                  {"texte": "après l'acide pyruvique : [O₂] diminue (100 → 85 % à 12 min)", "mot": "le dioxygène بدا كينقص"}],
       "pointage": [{"mot": "la courbe كتبدا stable", "commande": "play_until", "parametres": {"moment": "palier"}},
                    {"mot": "la courbe كتبدا stable", "cible": "centre:0"},
                    {"mot": "دابا كنزيدو le glucose", "commande": "play_until", "parametres": {"moment": "glucose_ajoute"}},
                    {"mot": "la courbe بقات stable", "commande": "play_until", "parametres": {"moment": "ajout_glucose_rien", "duree_s": 1.2}},
                    {"mot": "la courbe بقات stable", "cible": "centre:1"},
                    {"mot": "من بعد كنزيدو l'acide pyruvique", "commande": "play_until", "parametres": {"moment": "pyruvate_ajoute"}},
                    {"mot": "le dioxygène بدا كينقص", "commande": "play_until", "parametres": {"moment": "ajout_pyruvate", "duree_s": 1.6}},
                    {"mot": "le dioxygène بدا كينقص", "cible": "centre:2"}]}},
    {"id": "ex_s2", "slide_type": "simulation", "title": "Question 2 : la mitochondrie utilise l'acide pyruvique, pas le glucose",
     "screen_content": {"lead": "Glucose : rien ne change. Acide pyruvique : O₂ consommé."},
     "visual": {"kind": "simulation", "url": EXAO, "caption": "Ce que montre chaque ajout"},
     "speech_text": {"mixed": "نعاودو نشوفو l'expérience بالطريقة ديال الاستنتاج. زدنا le glucose: la courbe ما تبدلاتش. يعني les mitochondries ما كيستعملوش le glucose. زدنا l'acide pyruvique: le dioxygène كينقص. يعني les mitochondries كيستعملو l'acide pyruvique، وكيأكسدوه، وهي كتستهلك le dioxygène. وردو البال: le glucose ما كيدخلش للmitochondrie، اللي كيدخل هو l'acide pyruvique."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "glucose ajouté : rien → glucose non utilisé", "mot": "ما كيستعملوش le glucose"},
                  {"texte": "acide pyruvique ajouté : [O₂] diminue → acide pyruvique utilisé", "mot": "كيستعملو l'acide pyruvique"},
                  {"texte": "le glucose n'entre pas dans la mitochondrie", "mot": "le glucose ما كيدخلش للmitochondrie"}],
       "pointage": [{"mot": "زدنا le glucose", "commande": "play_until", "parametres": {"moment": "glucose_ajoute"}},
                    {"mot": "la courbe ما تبدلاتش", "commande": "play_until", "parametres": {"moment": "ajout_glucose_rien", "duree_s": 1.2}},
                    {"mot": "ما كيستعملوش le glucose", "cible": "centre:0"},
                    {"mot": "زدنا l'acide pyruvique", "commande": "play_until", "parametres": {"moment": "pyruvate_ajoute"}},
                    {"mot": "le dioxygène كينقص", "commande": "play_until", "parametres": {"moment": "ajout_pyruvate", "duree_s": 1.6}},
                    {"mot": "كيستعملو l'acide pyruvique", "cible": "centre:1"},
                    {"mot": "le glucose ما كيدخلش للmitochondrie", "cible": "centre:2"}]}},
    {"id": "ex_s3", "slide_type": "simulation", "title": "Question 3 : la glycolyse dehors, l'acide pyruvique dedans",
     "screen_content": {"lead": "Glycolyse dans le hyaloplasme ; l'acide pyruvique entre dans la matrice."},
     "visual": {"kind": "simulation", "url": PYR, "caption": "L'acide pyruvique passe du hyaloplasme à la matrice"},
     "speech_text": {"mixed": "la cellule كتستهلك le glucose، ولكن la mitochondrie ما كتستعملوش. إذن le glucose كيتحول برا من la mitochondrie، فle hyaloplasme: هادي la glycolyse، وكتعطي l'acide pyruvique. شوف: هادا l'acide pyruvique فle hyaloplasme. دابا شوف: دخل للmatrice، دوز من les deux membranes. وتما، فla matrice، كيتأكسد: شوف، خرج منو C O deux. إذن la glycolyse فle hyaloplasme، و l'oxydation ديال l'acide pyruvique فla mitochondrie."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "glycolyse : glucose → acide pyruvique, dans le hyaloplasme", "mot": "هادي la glycolyse"},
                  {"texte": "l'acide pyruvique entre dans la matrice de la mitochondrie", "mot": "دخل للmatrice"},
                  {"texte": "il y est oxydé : un CO₂ part", "mot": "خرج منو C O deux"}],
       "pointage": [{"mot": "هادي la glycolyse", "cible": "centre:0"},
                    {"mot": "هادا l'acide pyruvique فle hyaloplasme", "commande": "play_until", "parametres": {"moment": "pyruvate_hyaloplasme"}},
                    {"mot": "دخل للmatrice", "commande": "play_until", "parametres": {"moment": "entre_dans_matrice"}},
                    {"mot": "دخل للmatrice", "cible": "centre:1"},
                    {"mot": "خرج منو C O deux", "commande": "play_until", "parametres": {"moment": "co2_part", "duree_s": 1.2}},
                    {"mot": "خرج منو C O deux", "cible": "centre:2"}]}},
    {"id": "ex_s4", "slide_type": "simulation", "title": "Question 4 : légender la mitochondrie",
     "screen_content": {"lead": "De l'extérieur vers l'intérieur : membrane externe, membrane interne, crêtes, matrice."},
     "visual": {"kind": "simulation", "url": MITO, "caption": "La mitochondrie et ses parties"},
     "speech_text": {"mixed": "نسميو les parties ديال la mitochondrie، من برا للداخل. اللول، الغشاء اللي برا: la membrane externe. من داخل، غشاء تاني: la membrane interne. شوف كيفاش داخلة وخارجة: هادو les crêtes. وكل داكشي اللي داخل: la matrice. وفla matrice كيتفكك l'acide pyruvique: l'acétyl-CoA و le cycle de Krebs. فle document ديال التمرين: un la membrane externe، deux la membrane interne، trois la crête، et quatre la matrice."},
     "concentration": {"demarrer": "reset",
       "centre": [{"texte": "1 membrane externe ; 2 membrane interne", "mot": "la membrane externe. من داخل"},
                  {"texte": "3 crête ; 4 matrice", "mot": "وكل داكشي اللي داخل"},
                  {"texte": "acide pyruvique dégradé dans la matrice", "mot": "وفla matrice كيتفكك l'acide pyruvique"}],
       "pointage": [{"mot": "الغشاء اللي برا", "commande": "play_until", "parametres": {"moment": "membrane_externe"}},
                    {"mot": "غشاء تاني", "commande": "play_until", "parametres": {"moment": "membrane_interne"}},
                    {"mot": "la membrane externe. من داخل", "cible": "centre:0"},
                    {"mot": "هادو les crêtes", "commande": "play_until", "parametres": {"moment": "cretes"}},
                    {"mot": "وكل داكشي اللي داخل", "commande": "play_until", "parametres": {"moment": "matrice"}},
                    {"mot": "وكل داكشي اللي داخل", "cible": "centre:1"},
                    {"mot": "وفla matrice كيتفكك l'acide pyruvique", "commande": "play_until", "parametres": {"moment": "lieux_matrice"}},
                    {"mot": "وفla matrice كيتفكك l'acide pyruvique", "cible": "centre:2"}]}}
  ]}]},
  "facile": {"activities": [{"id": "facile", "title": "Plus facile, pour s'entraîner", "slides": [
    qcm_facile("fa_s1", "Plus facile : après le glucose", "نتمرنو بسؤال ساهل على la courbe.",
      "Juste après l'ajout du glucose (entre 2 et 5 min), [O₂]…", ["diminue", "reste stable à 100 %", "augmente"], 1, {
        "1": {"juste": rep("برافو! من بعد le glucose، la concentration ديال le dioxygène كتبقى stable à cent pour cent.", "Juste : après le glucose, [O₂] reste stable à 100 %.")},
        "0": {"1": rep("ما تقلقش. كتنقص غير من بعد l'acide pyruvique. شوف la courbe entre deux et cinq minutes. عاود اختار.", "Elle ne diminue qu'après l'acide pyruvique. Regarde entre 2 et 5 min. Réessaie."),
              "2": rep("الجواب هو stable à cent pour cent. la courbe كتنقص غير après cinq minutes، ملي زدنا l'acide pyruvique.", "Réponse : [O₂] reste stable à 100 % ; elle diminue seulement après l'acide pyruvique.")},
        "2": {"1": rep("لا، la courbe ما كتطلعش أبدا هنا. شوف واش ثابتة ولا كتهبط. عاود اختار.", "La courbe ne monte jamais ici. Est-elle plate ou descendante ? Réessaie."),
              "2": rep("الجواب هو stable à cent pour cent. le glucose ما بدل والو.", "Réponse : [O₂] reste stable à 100 % : le glucose ne change rien.")}},
      "Juste après l'ajout du glucose, la concentration du dioxygène ?"),
    vrai_faux("fa_s2", "Plus facile : vrai ou faux", "Dis si chaque phrase est vraie ou fausse.",
      "سؤال ساهل: قول واش كل جملة vrai ولا faux.", [
        ("Les mitochondries isolées utilisent le glucose.", False, "Faux : après l'ajout du glucose, [O₂] ne change pas ; le glucose n'est pas utilisé."),
        ("Les mitochondries isolées utilisent l'acide pyruvique en consommant le dioxygène.", True, "Vrai : après l'ajout de l'acide pyruvique, [O₂] diminue."),
        ("Le glucose entre dans la mitochondrie.", False, "Faux : c'est l'acide pyruvique qui entre dans la mitochondrie.")]),
    association("fa_s3", "Plus facile : chaque étape à sa place", "Relie chaque étape à son lieu.",
      "سؤال ساهل: ربط كل étape مع البلاصة ديالها.", "Relie chaque étape au lieu où elle se déroule.",
      [("1", "Glycolyse : glucose → 2 acides pyruviques"), ("2", "Oxydation de l'acide pyruvique avec consommation de O₂")],
      [("a", "Hyaloplasme"), ("b", "Mitochondrie"), ("c", "Noyau")], {"1": "a", "2": "b"}, {
        "1-a": (True, "Oui : la glycolyse se fait dans le hyaloplasme.", "برافو: la glycolyse كتوقع فle hyaloplasme."),
        "1-b": (False, "Non : la mitochondrie isolée n'utilise pas le glucose.", "لا، la mitochondrie بوحدها ما كتستعملش le glucose."),
        "1-c": (False, "Non : le noyau ne dégrade pas le glucose.", "لا، le noyau ما كيفككش le glucose."),
        "2-a": (False, "Non : l'acide pyruvique quitte le hyaloplasme pour être oxydé ailleurs.", "لا، l'acide pyruvique كيخرج من le hyaloplasme باش يتأكسد فبلاصة أخرى."),
        "2-b": (True, "Oui : l'acide pyruvique est oxydé dans la mitochondrie, avec le dioxygène.", "برافو: l'acide pyruvique كيتأكسد فla mitochondrie، مع le dioxygène."),
        "2-c": (False, "Non : le noyau ne consomme pas le dioxygène pour oxyder l'acide pyruvique.", "لا، le noyau ما عندو علاقة مع l'oxydation ديال l'acide pyruvique.")},
      ("(1 ; a) (2 ; b) : glycolyse dans le hyaloplasme, oxydation de l'acide pyruvique dans la mitochondrie.",
       "la glycolyse فle hyaloplasme، و l'oxydation ديال l'acide pyruvique فla mitochondrie.")),
    qcm_facile("fa_s4", "Plus facile : où est dégradé l'acide pyruvique ?", "سؤال ساهل على la mitochondrie.",
      "Dans la mitochondrie, l'acide pyruvique est dégradé dans…", ["la membrane externe", "la matrice", "l'espace intermembranaire"], 1, {
        "1": {"juste": rep("برافو! l'acide pyruvique كيتفكك فla matrice، الداخل ديال la mitochondrie.", "Juste : l'acide pyruvique est dégradé dans la matrice.")},
        "0": {"1": rep("قريب، ولكن la membrane externe غير كتسد la mitochondrie. l'acide pyruvique كيدوز منها لداخل. عاود اختار.", "La membrane externe limite la mitochondrie ; l'acide pyruvique la traverse. Réessaie."),
              "2": rep("الجواب هو la matrice. l'acide pyruvique كيدوز من les deux membranes، وكيتفكك فla matrice.", "Réponse : la matrice ; il traverse les deux membranes.")},
        "2": {"1": rep("لا، l'espace intermembranaire غير بين جوج الأغشية. l'acide pyruvique كيمشي أبعد، لداخل. عاود اختار.", "L'espace intermembranaire est entre les deux membranes ; l'acide pyruvique va plus loin. Réessaie."),
              "2": rep("الجواب هو la matrice، الداخل ديال la mitochondrie، فين كاين le cycle de Krebs.", "Réponse : la matrice, où se fait le cycle de Krebs.")}},
      "Dans la mitochondrie, l'acide pyruvique est dégradé dans ?")
  ]}]},
  "similaire": {
    "id": "svt_ex_ch1_mitochondries_1_b", "titre": "Même exercice, autres données",
    "enonce": {
      "intro": "Même expérience avec des mitochondries de cellules musculaires : le glucose est ajouté à t = 3 min et l'acide pyruvique à t = 6 min. Dans une cellule musculaire entière, le glucose est consommé en présence de dioxygène. Dans le document 2, les numéros sont placés autrement.",
      "intro_dit": "نفس التجربة، مع des mitochondries ديال les cellules musculaires. le glucose à trois minutes، و l'acide pyruvique à six minutes. و la cellule musculaire كاملة كتستهلك le glucose مع le dioxygène. فle document deux، les numéros تبدلو.",
      "figures": [FIGS, FIG2S],
      "donnees": ["[O₂] = 100 % au départ", "Glucose ajouté à t = 3 min ; acide pyruvique ajouté à t = 6 min",
                  "Dans une cellule entière, le glucose est consommé en présence de dioxygène"],
      "questions": [
        {"id": "1", "texte": "Décrire l'évolution de [O₂] avant l'ajout du glucose, après l'ajout du glucose, puis après l'ajout de l'acide pyruvique.",
         "reponse": {"type": "phrase", "attendu": "Avant 3 min, [O₂] reste stable à 100 %. Après l'ajout du glucose (de 3 à 6 min), [O₂] reste stable à 100 %. Après l'ajout de l'acide pyruvique (à 6 min), [O₂] diminue, de 100 % à 88 % à 12 min."},
         "clavier": {"aides": ["reste stable", "diminue", "100 %", "88 %"], "pieges": ["augmente"]},
         "correction": {"lignes": [{"texte": "1 : avant 3 min et après le glucose : [O₂] stable à 100 %", "mot": "stable à cent pour cent"},
                                   {"texte": "après l'acide pyruvique : [O₂] diminue, de 100 % à 88 % à 12 min", "mot": "de cent à quatre-vingt-huit pour cent"}],
                        "parole": "avant trois minutes، ومن بعد le glucose، la concentration ديال le dioxygène stable à cent pour cent. من بعد l'acide pyruvique، كتنقص، de cent à quatre-vingt-huit pour cent، à douze minutes."}},
        {"id": "2", "texte": "Déduire la molécule que les mitochondries utilisent en consommant le dioxygène. Justifier.",
         "reponse": {"type": "phrase", "attendu": "Les mitochondries n'utilisent pas le glucose ([O₂] ne change pas après son ajout) ; elles utilisent et oxydent l'acide pyruvique en consommant le dioxygène ([O₂] diminue après son ajout)."},
         "clavier": {"aides": ["n'utilisent pas le glucose", "acide pyruvique", "car"], "pieges": ["le glucose entre dans la mitochondrie"]},
         "correction": {"lignes": [{"texte": "2 : glucose : [O₂] ne change pas → non utilisé", "mot": "le glucose ما كيتستعملش"},
                                   {"texte": "acide pyruvique : [O₂] diminue → oxydé avec consommation de O₂", "mot": "l'acide pyruvique كيتأكسد"}],
                        "parole": "مع le glucose، ما تبدل والو: le glucose ما كيتستعملش. مع l'acide pyruvique، le dioxygène كينقص: l'acide pyruvique كيتأكسد."}},
        {"id": "3", "texte": "Déduire le lieu de la glycolyse et le lieu de l'oxydation de l'acide pyruvique dans la cellule.",
         "reponse": {"type": "phrase", "attendu": "La glycolyse (glucose → 2 acides pyruviques) se fait hors de la mitochondrie, dans le hyaloplasme ; l'acide pyruvique entre dans la mitochondrie où il est oxydé (matrice)."},
         "clavier": {"aides": ["glycolyse", "hyaloplasme", "mitochondrie", "matrice"], "pieges": ["noyau"]},
         "correction": {"lignes": [{"texte": "3 : glycolyse dans le hyaloplasme", "mot": "la glycolyse فle hyaloplasme"},
                                   {"texte": "oxydation de l'acide pyruvique dans la mitochondrie (matrice)", "mot": "فla mitochondrie"}],
                        "parole": "la glycolyse فle hyaloplasme، و l'acide pyruvique كيتأكسد فla mitochondrie، فla matrice."}},
        {"id": "4", "texte": "Nommer les éléments 1, 2, 3 et 4 du document 2, puis préciser le compartiment où l'acide pyruvique est dégradé.",
         "reponse": {"type": "phrase", "attendu": "1 : matrice ; 2 : crête ; 3 : membrane interne ; 4 : membrane externe. L'acide pyruvique est dégradé dans la matrice (1)."},
         "clavier": {"aides": ["membrane externe", "membrane interne", "crête", "matrice"], "pieges": ["espace intermembranaire", "hyaloplasme"]},
         "correction": {"lignes": [{"texte": "4 : 1 matrice ; 2 crête ; 3 membrane interne ; 4 membrane externe", "mot": "un la matrice"},
                                   {"texte": "acide pyruvique dégradé dans la matrice (1)", "mot": "كيتفكك فla matrice"}],
                        "parole": "un la matrice، deux la crête، trois la membrane interne، et quatre la membrane externe. و l'acide pyruvique كيتفكك فla matrice: le numéro un."}}
      ]}}
}

ecrire(EX, sys.argv[1])
