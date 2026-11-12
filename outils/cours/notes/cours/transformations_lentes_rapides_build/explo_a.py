"""Exploration du chapitre transformations_lentes_rapides, partie A : en-tête, cadre, notions, visuels.
explo.py assemble explo_a.py + explo_b.py (plan) et écrit backend/data/curriculum/exploration/transformations_lentes_rapides.json."""

ENTETE = {
 "cle": "transformations_lentes_rapides",
 "matiere": "Physique-Chimie",
 "filiere": "2e Bac Sciences Physiques BIOF (Maroc)",
 "titre": "Transformations lentes et transformations rapides",
 "date_exploration": "2026-11-12",
 "_note": ("Exploration faite par la routine cloud du 12 novembre 2026. VIDÉOS NON AUDITÉES : YouTube est bloqué depuis le conteneur "
           "cloud (comme pour circuit_RLC). Appui : les 20 nationaux PC 2016-2025 du dépôt (transformations_lentes_rapides_build/nationaux.md), "
           "perimetre.json (clé cinetique, qui couvre aussi ce chapitre), l'ancien cours chem_ch1_kinetics_course_v1.json et le programme "
           "(OP-PC-2007, CDR-PC-2015). À compléter par 10 audits vidéo depuis le PC avant validation. Rien n'est copié d'une vidéo."),
}

SOURCES = {
 "videos": [],
 "videos_note": "aucune : YouTube inaccessible depuis le conteneur cloud (12/11/2026) ; 10 audits à faire depuis le PC (recherche « التحولات السريعة والتحولات البطيئة 2 باك », « transformations lentes et rapides 2bac biof »)",
 "examens": [f"backend/data/exams/physique/{a}-{s}" for a in range(2016, 2026) for s in ("normale", "rattrapage")],
 "autres": ["backend/data/curriculum/perimetre.json (clé cinetique : facteurs cinétiques, trempe, termes hors programme)",
            "backend/data/courses/chem_ch1_kinetics_course_v1.json (ancien cours, 10 diapositives, croquis)",
            "outils/cours/notes/cours/transformations_lentes_rapides_build/nationaux.md (relecture des 20 sujets)"],
}

COMPARAISON = {
 "_note": "sans vidéos : comparaison faite entre les corrigés des nationaux (écriture des demi-équations, des équations, des réponses sur les facteurs cinétiques) et l'ancien cours",
 "convergences": [
  "un couple s'écrit Ox/Red (l'oxydant d'abord) et sa demi-équation Ox + n e⁻ ⇌ Red",
  "en milieu acide : on équilibre O avec H₂O, puis H avec H⁺, puis les charges avec les électrons",
  "l'équation d'oxydoréduction : même nombre d'électrons dans les deux demi-équations, les électrons ne figurent pas dans le bilan",
  "une transformation rapide se fait en une durée trop courte pour être suivie à l'œil ou avec les appareils usuels ; une lente dure de quelques secondes à plusieurs minutes (ou heures)",
  "facteurs cinétiques : la température et la concentration initiale des réactifs (plus elles sont grandes, plus la transformation est rapide), et le catalyseur",
  "la trempe (eau glacée, dilution) bloque l'évolution avant un titrage",
 ],
 "variantes_admises": [
  {"variante": "flèche des demi-équations : ⇌, ⇄ ou =", "decision": "⇌ dans les demi-équations, → dans l'équation de la réaction (comme la plupart des corrigés) ; on dit une fois que certains sujets écrivent ⇄"},
  {"variante": "H⁺ ou H₃O⁺", "decision": "H⁺ (forme des corrigés récents) ; on dit une fois que H₃O⁺ est le même ion hydraté"},
  {"variante": "explication de l'effet de la température par les « chocs efficaces »", "decision": "non : perimetre.json met « théorie des collisions / chocs efficaces » hors programme ; on dit « l'agitation des entités augmente, elles se rencontrent plus souvent »"},
  {"variante": "catalyseur dans ce chapitre ou plus tard", "decision": "dans ce chapitre, une diapositive (t3) et une courbe (t4) : c'est la question de facteur la plus posée au national (6 questions, 5 sessions, toujours H₂SO₄ dans l'estérification) ; définition seulement : accélère, ne figure pas dans l'équation, ne change pas l'état final ; pas de catalyse homogène/hétérogène/enzymatique"},
 ],
 "meilleures_explications": [
  "oxydant / réducteur : l'oxydant CAPTE des électrons, le réducteur les CÈDE ; moyen mnémotechnique : « réducteur = donneur »",
  "équilibrer une demi-équation : quatre gestes dans l'ordre (atomes autres que O et H, O avec H₂O, H avec H⁺, charges avec e⁻), puis on vérifie les charges des deux côtés",
  "rapide ou lente : deux béchers côte à côte, même ion permanganate violet ; avec les ions fer II il se décolore aussitôt, avec l'acide oxalique il met des minutes",
  "température : la même réaction dans un bain glacé et dans un bain chaud ; le chaud se colore le premier, les deux finissent pareil",
  "trempe : on verse le prélèvement dans l'eau glacée : la couleur s'arrête d'évoluer, comme une photo",
 ],
}

CADRE = {
 "_note": "Fiche du chapitre, même forme que cadre_reference_2bac_pc.json. Capacités d'après le programme (OP-PC-2007), CDR-PC-2015 annexe 1 (« Transformations lentes et rapides (oxydoréduction, facteurs cinétiques) »), perimetre.json (clé cinetique) et les nationaux PC 2016-2025. Texte officiel du cadre non relu mot à mot : TLR1 à TLR7 provisoires.",
 "titre": "Transformations lentes et transformations rapides",
 "source": "CDR-PC-2015, annexe 1, Chimie, sous-domaine 1 « Transformations rapides et lentes d'un système chimique » ; annexe 2, TP « Mise en évidence des facteurs cinétiques » ; OP-PC-2007 (2BAC : rappel oxydoréduction, transformations lentes et rapides, facteurs cinétiques : température et concentration des réactifs) ; perimetre.json clé cinetique ; nationaux PC 2016-2025 du dépôt.",
 "capacites": [
  {"id": "TLR1", "texte": "Définir un oxydant, un réducteur, un couple Ox/Red, une oxydation et une réduction ; reconnaître l'oxydant et le réducteur dans une réaction."},
  {"id": "TLR2", "texte": "Écrire la demi-équation électronique d'un couple Ox/Red (en milieu acide : H₂O et H⁺) et vérifier la conservation des éléments et des charges."},
  {"id": "TLR3", "texte": "Écrire l'équation d'une réaction d'oxydoréduction à partir des demi-équations des deux couples mis en jeu."},
  {"id": "TLR4", "texte": "Distinguer expérimentalement une transformation rapide d'une transformation lente ; citer des exemples ; savoir que ce classement dépend des moyens d'observation."},
  {"id": "TLR5", "texte": "Connaître les facteurs cinétiques (température, concentration initiale des réactifs, catalyseur) et leur effet sur la durée d'une transformation ; les mettre en évidence par des expériences où un seul paramètre change."},
  {"id": "TLR6", "texte": "Exploiter des résultats expérimentaux ou des courbes obtenues dans des conditions différentes pour identifier le facteur cinétique et comparer les durées (l'état final ne dépend pas de la température)."},
  {"id": "TLR7", "texte": "Connaître des applications des facteurs cinétiques : la trempe pour bloquer une transformation, la conservation par le froid, l'accélération par le chauffage (autocuiseur)."},
 ],
 "formules": [
  {"ecriture": "Ox + n e⁻ ⇌ Red", "capacite": "TLR1", "dit": "oxydant plus n électrons donne réducteur", "phrase": "demi-équation électronique d'un couple Ox/Red"},
  {"ecriture": "Cu²⁺ + 2e⁻ ⇌ Cu", "capacite": "TLR2", "dit": "ion cuivre deux plus deux électrons donne cuivre"},
  {"ecriture": "Zn²⁺ + 2e⁻ ⇌ Zn", "capacite": "TLR2", "dit": "ion zinc deux plus deux électrons donne zinc"},
  {"ecriture": "I₂ + 2e⁻ ⇌ 2I⁻", "capacite": "TLR2", "dit": "diiode plus deux électrons donne deux ions iodure"},
  {"ecriture": "H₂O₂ + 2H⁺ + 2e⁻ ⇌ 2H₂O", "capacite": "TLR2", "dit": "eau oxygénée plus deux H plus plus deux électrons donne deux molécules d'eau"},
  {"ecriture": "MnO₄⁻ + 8H⁺ + 5e⁻ ⇌ Mn²⁺ + 4H₂O", "capacite": "TLR2", "dit": "ion permanganate plus huit H plus plus cinq électrons donne ion manganèse deux plus quatre molécules d'eau"},
  {"ecriture": "2CO₂ + 2H⁺ + 2e⁻ ⇌ H₂C₂O₄", "capacite": "TLR2", "dit": "deux CO deux plus deux H plus plus deux électrons donne acide oxalique"},
  {"ecriture": "Fe³⁺ + e⁻ ⇌ Fe²⁺", "capacite": "TLR2", "dit": "ion fer trois plus un électron donne ion fer deux"},
  {"ecriture": "S₂O₈²⁻ + 2e⁻ ⇌ 2SO₄²⁻", "capacite": "TLR2", "dit": "ion peroxodisulfate plus deux électrons donne deux ions sulfate"},
  {"ecriture": "S₄O₆²⁻ + 2e⁻ ⇌ 2S₂O₃²⁻", "capacite": "TLR2", "dit": "ion tétrathionate plus deux électrons donne deux ions thiosulfate"},
  {"ecriture": "Cr₂O₇²⁻ + 14H⁺ + 6e⁻ ⇌ 2Cr³⁺ + 7H₂O", "capacite": "TLR2", "dit": "ion dichromate plus quatorze H plus plus six électrons donne deux ions chrome trois plus sept molécules d'eau"},
  {"ecriture": "Zn + Cu²⁺ → Zn²⁺ + Cu", "capacite": "TLR3", "dit": "zinc plus ion cuivre deux donne ion zinc deux plus cuivre"},
  {"ecriture": "H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O", "capacite": "TLR3", "dit": "eau oxygénée plus deux ions iodure plus deux H plus donne diiode plus deux molécules d'eau"},
  {"ecriture": "2MnO₄⁻ + 5H₂C₂O₄ + 6H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O", "capacite": "TLR3", "dit": "deux ions permanganate plus cinq acide oxalique plus six H plus donne deux ions manganèse plus dix CO deux plus huit molécules d'eau"},
  {"ecriture": "MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O", "capacite": "TLR3", "dit": "ion permanganate plus cinq ions fer deux plus huit H plus donne ion manganèse plus cinq ions fer trois plus quatre molécules d'eau"},
  {"ecriture": "S₂O₈²⁻ + 2I⁻ → 2SO₄²⁻ + I₂", "capacite": "TLR3", "dit": "ion peroxodisulfate plus deux ions iodure donne deux ions sulfate plus diiode"},
  {"ecriture": "I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻", "capacite": "TLR3", "dit": "diiode plus deux ions thiosulfate donne deux ions iodure plus ion tétrathionate"},
 ],
 "mots_cles": ["oxydant", "réducteur", "couple Ox/Red", "oxydation", "réduction", "demi-équation", "réaction d'oxydoréduction",
               "transformation rapide", "transformation lente", "facteur cinétique", "catalyseur", "température", "concentration initiale", "trempe",
               "durée d'une transformation", "état final"],
 "hors_cadre": {
  "mots": ["arrhenius", "énergie d'activation", "ordre de réaction", "réaction d'ordre", "loi de vitesse", "constante de vitesse",
           "mécanisme réactionnel", "étape élémentaire", "état de transition", "complexe activé", "intermédiaire réactionnel",
           "théorie des collisions", "chocs efficaces", "choc efficace", "maxwell", "boltzmann", "beer-lambert", "nombre d'oxydation",
           "degré d'oxydation", "potentiel standard", "potentiel d'électrode", "échelle des potentiels", "règle du gamma", "électronégativité"],
  "motifs": ["arrhenius|[ée]nergie d'activation", "ordre (de (la )?r[ée]action)|loi de vitesse|constante de vitesse",
             "m[ée]canisme r[ée]actionnel|[ée]tat de transition|interm[ée]diaire r[ée]actionnel", "th[ée]orie des collisions|chocs? efficaces?",
             "nombre d'oxydation|degr[ée] d'oxydation|potentiel (standard|d'[ée]lectrode)|r[èe]gle du gamma"],
  "tolere_si_annonce": [],
 },
 "valeurs_reference": [
  "MnO₄⁻ violet, Mn²⁺ presque incolore ; I₂ en solution jaune à brun ; I⁻, H₂O₂, S₂O₈²⁻, SO₄²⁻ incolores ; Cu²⁺ bleu ; Fe²⁺ vert pâle, Fe³⁺ jaune-orangé (rouille)",
  "rapide : moins d'une fraction de seconde à l'œil ; lente : de quelques secondes à quelques heures ; très lente : des jours ou des années (rouille)",
  "trempe : eau glacée (vers 0 °C) et dilution, avant le titrage du diiode formé par le thiosulfate (réaction rapide)",
 ],
}

INSISTANCES = [
 "l'oxydant capte des électrons, le réducteur en cède : ne jamais les échanger (piège n° 1 des corrigés)",
 "une demi-équation : éléments ET charges conservés ; les électrons du côté de l'oxydant",
 "dans l'équation bilan, les électrons disparaissent : même nombre d'électrons cédés et captés",
 "un facteur cinétique change la DURÉE, pas l'état final (avec les mêmes quantités initiales)",
 "pour comparer, un seul paramètre change entre deux expériences",
 "on ne parle pas de « chocs efficaces » (hors programme) : on dit que les entités se rencontrent plus souvent",
]

VALEURS_REPERES = [
 "simulation température : même mélange eau oxygénée + iodure acidifié, bain à 20 °C et bain à 40 °C ; à 40 °C la couleur brune atteint son maximum environ trois fois plus tôt (ordre de grandeur pédagogique, pas une loi)",
 "simulation concentration : [I⁻]₀ doublée, H₂O₂ réactif limitant inchangé → même quantité finale de diiode, atteinte plus tôt",
 "rapide : permanganate + ions fer II décoloré à la goutte ; lente : permanganate + acide oxalique décoloré en quelques minutes à 20 °C",
]

PIEGES = [
 {"erreur": "écrire l'oxydant du côté qui perd des électrons (électrons du mauvais côté)", "geste": "l'oxydant et les électrons sont du même côté : Ox + n e⁻ ⇌ Red"},
 {"erreur": "oublier d'équilibrer les charges, ou les vérifier avant d'avoir mis H⁺", "geste": "ordre fixe : atomes, O par H₂O, H par H⁺, puis charges par e⁻ ; compter la charge des deux côtés"},
 {"erreur": "laisser des électrons dans l'équation bilan", "geste": "multiplier les demi-équations pour avoir le même nombre d'électrons, puis additionner"},
 {"erreur": "dire que la température change la quantité finale de produit", "geste": "mêmes quantités initiales → même état final ; seule la durée change"},
 {"erreur": "comparer deux expériences où deux paramètres changent", "geste": "chercher les deux expériences qui ne diffèrent que par UN paramètre"},
 {"erreur": "croire qu'une réaction rapide « n'a pas de durée »", "geste": "elle a une durée, trop courte pour nos yeux et nos appareils"},
]

ANALOGIES = [
 {"image": "le réducteur est un « donneur » d'électrons, l'oxydant un « receveur », comme une passe au football : le ballon (électron) ne disparaît pas", "limite": "les électrons ne se promènent pas seuls dans la solution : ils passent directement d'une entité à l'autre"},
 {"image": "le réfrigérateur ralentit les transformations qui abîment les aliments ; l'autocuiseur (cocotte) cuit plus vite car l'eau y bout au-dessus de 100 °C", "limite": "la cuisson n'est pas une seule réaction d'oxydoréduction : l'image sert pour l'effet de la température seulement"},
 {"image": "la trempe est une photo : on fige le mélange pour le doser tranquillement", "limite": "la trempe ralentit fortement, elle n'arrête pas à 100 % : on titre vite"},
 {"image": "plus il y a de monde dans le souk, plus on se croise souvent : plus la concentration est grande, plus les entités se rencontrent", "limite": "image qualitative seulement : pas de loi de vitesse au programme"},
]

A_NE_PAS_DIRE = [
 {"terme": "chocs efficaces / théorie des collisions", "motif": "chocs? efficaces?|th[ée]orie des collisions", "dire_plutot": "les entités s'agitent plus et se rencontrent plus souvent"},
 {"terme": "le catalyseur change l'état final", "motif": "catalyseur (augmente|change|modifie) (la quantit[ée]|l'[ée]tat final|le rendement)", "dire_plutot": "le catalyseur accélère, l'état final reste le même"},
 {"terme": "l'oxydant cède des électrons", "motif": "oxydant (c[èe]de|perd|donne) (des |un |les )?[ée]lectrons?", "dire_plutot": "l'oxydant capte des électrons"},
 {"terme": "le réducteur capte des électrons", "motif": "r[ée]ducteur (capte|gagne|re[çc]oit) (des |un |les )?[ée]lectrons?", "dire_plutot": "le réducteur cède des électrons"},
 {"terme": "la température augmente la quantité de produit formé", "motif": "temp[ée]rature augmente la quantit[ée]", "dire_plutot": "la température raccourcit la durée ; l'état final reste le même"},
]

EXCLUS = [
 "types de catalyse (homogène, hétérogène, enzymatique) et mode d'action du catalyseur : non traités (on garde la définition seulement)",
 "suivi temporel quantitatif (tableau d'avancement en fonction du temps, vitesse volumique, temps de demi-réaction) : chapitre suivant « cinetique »",
 "théorie des collisions, énergie d'activation, loi d'Arrhenius, ordre de réaction : hors programme (perimetre.json)",
 "nombre d'oxydation, potentiels standard : hors programme",
 "surface de contact (ancien cours) : non retenue par le programme marocain du chapitre ; pas au national",
]

QUESTIONS_ELEVES = [
 {"question": "Comment savoir lequel est l'oxydant dans un couple ?", "reponse": "On écrit toujours le couple Ox/Red : l'oxydant à gauche. Dans la demi-équation, l'oxydant est du même côté que les électrons."},
 {"question": "Pourquoi on ajoute H⁺ et pas OH⁻ ?", "reponse": "Les réactions du programme se font en milieu acide (on ajoute de l'acide sulfurique) : on équilibre H avec H⁺."},
 {"question": "Une réaction rapide, c'est une réaction qui n'a pas de durée ?", "reponse": "Non : sa durée est seulement trop courte pour être suivie à l'œil ou avec nos appareils."},
 {"question": "Si on chauffe, est-ce qu'on obtient plus de produit ?", "reponse": "Non : avec les mêmes quantités initiales, l'état final est le même ; il est seulement atteint plus tôt."},
 {"question": "Pourquoi l'eau glacée pour la trempe ?", "reponse": "Le froid et la dilution ralentissent tellement la réaction qu'elle semble arrêtée : on peut doser le prélèvement sans qu'il change."},
]

COMMENTAIRES = [
 {"plainte": "je confonds oxydant et réducteur, oxydation et réduction", "vu": "ancien cours et corrigés (piège n° 1)", "reponse_du_cours": "x1-x3 : transfert.html vue zinc puis couple ; « l'oxydant capte, le réducteur cède » répété dans chaque bloc ; rappels C1"},
 {"plainte": "je n'arrive pas à équilibrer les demi-équations avec H₂O et H⁺", "vu": "nationaux (demi-équations demandées)", "reponse_du_cours": "x4-x6 : demi-equation.html, quatre gestes un par un, permanganate puis eau oxygénée ; exercice de bloc"},
 {"plainte": "je ne sais pas combien multiplier pour l'équation bilan", "vu": "corrigés", "reponse_du_cours": "x7-x9 : equation.html, moment multiplier ; PPCM des électrons (5 et 2 → 10)"},
 {"plainte": "rapide ou lente : c'est quoi la limite ?", "vu": "ancien cours", "reponse_du_cours": "r2, r3, r7 : bechers.html vues comparer et echelle ; le classement dépend des moyens d'observation"},
]
