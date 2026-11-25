# -*- coding: utf-8 -*-
"""Cours tc_phys_mouvement_inertie — en-tête, compétences (avec rappels), séances et blocs (cahier)."""

ENTETE = {
    'id': 'tc_phys_mouvement_inertie', 'stable_id': 'tc_phys_mouvement_inertie', 'lesson_id': 'tc_phys_mouvement_inertie',
    'title': 'Le mouvement et le principe d’inertie', 'version': 1, 'status': 'draft', 'language': 'mixed',
    'estimated_minutes': 200, 'mode': 'concentration', 'niveau': 'tronc_commun_sciences_biof', 'subject': 'physique',
    'lesson_match': ['le mouvement', 'principe d’inertie', 'principe d\'inertie', 'mouvement et inertie', 'centre d’inertie'],
    'catalog': {'summary': 'Tronc commun sciences, option française, physique : relativité du mouvement, référentiel, repères, trajectoire, vitesse moyenne et instantanée, enregistrement, vecteur vitesse, MRU et équation horaire, MCU (ω, T, f), centre d’inertie, principe d’inertie, référentiel galiléen, centre de masse.'},
    'note': 'Cours écrit en mode concentration d’après le livre « Cours physique-chimie TCSF » (programme 2020), chapitres « Le mouvement » et « Principe d’inertie » (résumé : docs/tcf/CONTENU_LIVRE.md ; architecture : docs/tcf/ARCHITECTURE_tc_phys_mouvement_inertie.md). Construit par scripts/tcf/mi_construire.py. Pas encore de voix : les textes à dire sont listés dans tc_phys_mouvement_inertie_voix.json.',
}


def rq(i, prompt, dit, options, correct):
    return {'id': i, 'type': 'qcm', 'prompt': prompt, 'enonce_dit': dit, 'options': options, 'correct': correct}


def rv(i, prompt, dit, correct):
    return {'id': i, 'type': 'vrai_faux', 'prompt': prompt, 'enonce_dit': dit, 'correct': correct}


def rl(i, prompt, dit, attendu):
    return {'id': i, 'type': 'libre', 'prompt': prompt, 'enonce_dit': dit, 'attendu': attendu}


COMPETENCES = [
    {'id': 'C1', 'label': 'Utiliser les prérequis : force, poids P = m·g, forces qui se compensent, vecteur, droite x = a·t + b',
     'dit': 'les forces, le poids et la droite', 'rappels': [
        rq('C1_r1', 'Le poids d’un corps de masse 3 kg (g = 10 N/kg) vaut…', 'شوف هاد السؤال: جسم la masse ديالو trois kilogrammes. شحال هو le poids ديالو؟', ['3 N', '30 N', '0,3 N'], 1),
        rv('C1_r2', 'Deux forces qui se compensent ont la même droite d’action, des sens contraires et la même intensité.', 'شوف هاد السؤال: deux forces اللي se compensent، عندهم نفس la droite d’action، sens متعاكسين ونفس l’intensité. vrai ou faux؟', 0),
        rl('C1_r3', 'Écris l’équation d’une droite x en fonction de t, et dis ce que sont a et b.', 'شوف هاد السؤال: كتب l’équation ديال une droite، x en fonction de t، وقول شنو هما a و b.', 'x = a·t + b ; a = Δx/Δt (la pente) ; b = x à t = 0.')]},
    {'id': 'C2', 'label': 'Reconnaître la relativité du mouvement et choisir un référentiel', 'dit': 'la relativité du mouvement et le référentiel', 'rappels': [
        rl('C2_r1', 'Qu’est-ce qu’un référentiel ?', 'شوف هاد السؤال: شنو هو le référentiel؟', 'Un solide indéformable par rapport auquel on étudie le mouvement.'),
        rv('C2_r2', 'Un passager assis dans un bus qui roule est au repos par rapport au sol.', 'شوف هاد السؤال: راكب جالس ف le bus اللي كيمشي، au repos بالنسبة للأرض. vrai ou faux؟', 1),
        rq('C2_r3', 'Le référentiel terrestre, c’est…', 'شوف هاد السؤال: le référentiel terrestre، شنو هو؟', ['le Soleil', 'le sol et ce qui y est fixé', 'le bus'], 1)]},
    {'id': 'C3', 'label': 'Repérer une position (repère d’espace, vecteur position) et une date (repère de temps)', 'dit': 'les repères d’espace et de temps', 'rappels': [
        rq('C3_r1', 'Pour un mouvement dans un plan, le repère d’espace a…', 'شوف هاد السؤال: le mouvement ف واحد le plan، شحال ديال les axes خاصنا؟', ['un axe', 'deux axes', 'trois axes'], 1),
        rl('C3_r2', 'Écris le vecteur position OM⃗ dans le repère (O, i⃗, j⃗, k⃗).', 'شوف هاد السؤال: كتب le vecteur position OM ف le repère O، i، j، k.', 'OM⃗ = x·i⃗ + y·j⃗ + z·k⃗'),
        rv('C3_r3', 'L’origine des dates t = 0 est choisie par l’observateur.', 'شوف هاد السؤال: l’origine des dates، t égale zéro، كيختارها l’observateur. vrai ou faux؟', 0)]},
    {'id': 'C4', 'label': 'Définir et reconnaître une trajectoire', 'dit': 'la trajectoire', 'rappels': [
        rl('C4_r1', 'Définis la trajectoire.', 'شوف هاد السؤال: عرف la trajectoire.', 'L’ensemble des positions successives occupées par un point du mobile.'),
        rq('C4_r2', 'La trajectoire d’un point d’une roue qui tourne sur place est…', 'شوف هاد السؤال: نقطة من رويضة كتدور فبلاصتها، شنو هي la trajectoire ديالها؟', ['rectiligne', 'circulaire', 'curviligne quelconque'], 1),
        rv('C4_r3', 'La trajectoire d’un point est la même dans tous les référentiels.', 'شوف هاد السؤال: la trajectoire ديال نقطة هي نفسها ف كاع les référentiels. vrai ou faux؟', 1)]},
    {'id': 'C5', 'label': 'Calculer une vitesse moyenne et une vitesse instantanée, convertir m/s et km/h', 'dit': 'la vitesse moyenne et la vitesse instantanée', 'rappels': [
        rq('C5_r1', '10 m/s en km/h, c’est…', 'شوف هاد السؤال: dix mètres par seconde، شحال ب kilomètre par heure؟', ['36 km/h', '2,8 km/h', '100 km/h'], 0),
        rl('C5_r2', 'Écris la relation de la vitesse instantanée v_i sur un enregistrement.', 'شوف هاد السؤال: كتب la relation ديال la vitesse instantanée v i ف واحد l’enregistrement.', 'v_i = M_{i−1}M_{i+1}/(2τ)'),
        rq('C5_r3', 'Un coureur parcourt 100 m en 20 s. Sa vitesse moyenne est…', 'شوف هاد السؤال: واحد العداء قطع cent mètres ف vingt secondes. شحال هي la vitesse moyenne ديالو؟', ['5 m/s', '2 000 m/s', '0,2 m/s'], 0)]},
    {'id': 'C6', 'label': 'Représenter le vecteur vitesse et exploiter un mouvement rectiligne uniforme (équation horaire)', 'dit': 'le vecteur vitesse et le mouvement rectiligne uniforme', 'rappels': [
        rv('C6_r1', 'Le vecteur vitesse en un point est tangent à la trajectoire et orienté dans le sens du mouvement.', 'شوف هاد السؤال: le vecteur vitesse tangent ل la trajectoire، و ف le sens du mouvement. vrai ou faux؟', 0),
        rl('C6_r2', 'Écris l’équation horaire d’un mouvement rectiligne uniforme.', 'شوف هاد السؤال: كتب l’équation horaire ديال le mouvement rectiligne uniforme.', 'x(t) = v_x·t + x₀'),
        rq('C6_r3', 'Un MRU a v = 2 m/s et x₀ = 1 m (axe dans le sens du mouvement). Son équation est…', 'شوف هاد السؤال: MRU، v égale deux mètres par seconde، و x zéro égale un mètre. شنو هي l’équation horaire؟', ['x = t + 2', 'x = 2·t + 1', 'x = −2·t + 1'], 1)]},
    {'id': 'C7', 'label': 'Exploiter un mouvement circulaire uniforme : ω, T, f', 'dit': 'le mouvement circulaire uniforme', 'rappels': [
        rl('C7_r1', 'Écris la relation entre ω, v et R.', 'شوف هاد السؤال: كتب la relation بين oméga، v و R.', 'ω = v/R'),
        rq('C7_r2', 'Si T = 0,5 s, la fréquence f vaut…', 'شوف هاد السؤال: T égale zéro virgule cinq seconde. شحال هي la fréquence؟', ['0,5 Hz', '2 Hz', '5 Hz'], 1),
        rv('C7_r3', 'La période T est la durée d’un tour.', 'شوف هاد السؤال: la période T هي la durée ديال tour واحد كامل. vrai ou faux؟', 0)]},
    {'id': 'C8', 'label': 'Connaître le centre d’inertie et appliquer le principe d’inertie', 'dit': 'le principe d’inertie', 'rappels': [
        rl('C8_r1', 'Énonce le principe d’inertie.', 'شوف هاد السؤال: عطي l’énoncé ديال le principe d’inertie.', 'Dans un référentiel galiléen, si un solide est isolé ou pseudo-isolé, son centre d’inertie G est au repos ou en mouvement rectiligne uniforme.'),
        rq('C8_r2', 'Un solide pseudo-isolé est un solide…', 'شوف هاد السؤال: un solide pseudo-isolé، شنو هو؟', ['soumis à aucune force', 'dont les forces se compensent', 'qui tourne sur lui-même'], 1),
        rq('C8_r3', 'Un lustre de 2 kg est suspendu, immobile (g = 10 N/kg). La tension du fil vaut…', 'شوف هاد السؤال: une lampe، deux kilogrammes، معلقة وما كتحركش. شحال هي la tension ديال الخيط؟', ['2 N', '20 N', '0 N'], 1)]},
    {'id': 'C9', 'label': 'Déterminer un centre de masse par la relation barycentrique', 'dit': 'le centre de masse', 'rappels': [
        rl('C9_r1', 'Écris la relation barycentrique pour deux corps (O quelconque).', 'شوف هاد السؤال: كتب la relation barycentrique ديال deux corps.', 'OG⃗ = (m₁·OG⃗₁ + m₂·OG⃗₂)/(m₁ + m₂)'),
        rv('C9_r2', 'Pour un haltère à deux masses égales, le centre de masse est au milieu.', 'شوف هاد السؤال: haltère فيه deux masses متساويين، le centre de masse فالوسط. vrai ou faux؟', 0),
        rq('C9_r3', 'Deux corps : m₁ = 1 kg en A, m₂ = 3 kg en B, AB = 40 cm. AG vaut…', 'شوف هاد السؤال: un kilogramme ف A، trois kilogrammes ف B، و AB égale quarante centimètres. شحال هو AG؟', ['10 cm', '30 cm', '20 cm'], 1)]},
]


def bloc(i, titre, ids, cahier, retrouver, exercice, figures=None):
    b = {'id': i, 'titre': titre, 'slide_ids': ids, 'cahier': [{'texte': t} for t in cahier],
         'retrouver': {'prompt': retrouver[0], 'attendu': retrouver[1], 'competence_id': retrouver[2]},
         'exercice': exercice}
    if figures:
        b['cahier_figures'] = figures
    return b


def qcm(prompt, options, correct):
    return {'type': 'qcm', 'prompt': prompt, 'options': options, 'correct': correct}


FIG_DROITE = {'type': 'courbe', 'titre': 'Une droite x = a·t + b', 'legende': 'b se lit à t = 0 ; la pente a = Δx/Δt.',
              'axes': {'x': {'min': 0, 'max': 4, 'nom': 't', 'unite': 's', 'graduations': [[1, '1'], [3, '3']]},
                       'y': {'min': 0, 'max': 9, 'nom': 'x', 'unite': 'm', 'graduations': [[1, 'b'], [3, '3'], [7, '7']]}},
              'elements': [{'f': 'courbe', 'expr': '2*x+1', 'couleur': 'cyan'}, {'f': 'cote', 'de': [1, 3], 'a': [3, 3], 't': 'Δt', 'pos': 's'},
                           {'f': 'cote', 'de': [3, 3], 'a': [3, 7], 't': 'Δx', 'pos': 'e'}, {'f': 'point', 'at': [0, 1], 't': 'b', 'pos': 'e'}]}
FIG_FORCES = {'type': 'schema', 'titre': 'Un livre posé sur une table', 'legende': 'P⃗ et R⃗ : même droite, sens contraires, même intensité.',
              'cadre': {'l': 8, 'h': 6},
              'elements': [{'f': 'rect', 'de': [0.5, 1.6], 'a': [7.5, 2], 'remplir': 'orange', 'couleur': 'orange'},
                           {'f': 'rect', 'de': [2.5, 2], 'a': [5.5, 2.8], 'couleur': 'bleu', 'remplir': 'bleu'},
                           {'f': 'fleche', 'de': [4, 2.4], 'a': [4, 0.3], 'couleur': 'rouge', 'texte': 'P⃗', 'pos': 'o'},
                           {'f': 'fleche', 'de': [4.15, 2], 'a': [4.15, 4.6], 'couleur': 'bleu', 'texte': 'R⃗', 'pos': 'e'},
                           {'f': 'texte', 'at': [6.6, 5], 't': 'P⃗ + R⃗ = 0⃗', 'ancre': 'centre'}]}
FIG_XT = {'type': 'courbe', 'titre': 'MRU : x en fonction de t', 'legende': 'Une droite : la pente est la vitesse v ; à t = 0, x = x₀.',
          'axes': {'x': {'min': -40, 'max': 110, 'nom': 't', 'unite': 'ms', 'graduations': [[0, '0'], [100, '100']]},
                   'y': {'min': 0, 'max': 16, 'nom': 'x', 'unite': 'cm', 'graduations': [[4, 'x₀ = 4'], [14, '14']]}},
          'elements': [{'f': 'courbe', 'expr': '0.1*x+4', 'de': -40, 'a': 100, 'couleur': 'cyan'}, {'f': 'repere', 'x': 100, 'y': 14},
                       {'f': 'point', 'at': [0, 4], 't': 'x₀', 'pos': 'no'}, {'f': 'texte', 'at': [40, 13], 't': 'pente = v', 'ancre': 'centre'}]}
FIG_CERCLE = {'type': 'schema', 'titre': 'Mouvement circulaire uniforme', 'legende': 'Arcs égaux en durées égales ; v⃗ tangent au cercle.',
              'cadre': {'l': 8, 'h': 6},
              'elements': [{'f': 'cercle', 'c': [4, 3], 'r': 2.4, 'couleur': 'cyan'}, {'f': 'point', 'at': [4, 3], 't': 'O', 'pos': 's'},
                           {'f': 'ligne', 'pts': [[4, 3], [6.4, 3]], 'couleur': 'jaune'}, {'f': 'texte', 'at': [5.2, 3.3], 't': 'R', 'ancre': 'centre'},
                           {'f': 'point', 'at': [6.4, 3], 't': 'M', 'pos': 'e'}, {'f': 'fleche', 'de': [6.4, 3], 'a': [6.4, 5.2], 'couleur': 'vert', 'texte': 'v⃗', 'pos': 'e'}]}
FIG_HALTERE = {'type': 'schema', 'titre': 'Le marteau : O pris en G₁', 'legende': 'G est entre G₁ et G₂, plus près de la masse la plus grande.',
               'cadre': {'l': 10, 'h': 3},
               'elements': [{'f': 'ligne', 'pts': [[1, 1.5], [9, 1.5]], 'couleur': 'faible'}, {'f': 'point', 'at': [1, 1.5], 't': 'G₁ (m₁)', 'pos': 'n'},
                            {'f': 'point', 'at': [9, 1.5], 't': 'G₂ (m₂)', 'pos': 'n'}, {'f': 'point', 'at': [7.4, 1.5], 't': 'G', 'pos': 's'},
                            {'f': 'fleche', 'de': [1, 0.8], 'a': [7.4, 0.8], 'couleur': 'rose', 'texte': 'G₁G⃗', 'pos': 's'}]}

SEANCES = [
  {'id': 'mi_s1', 'titre': 'Séance 1 — Les outils : forces, vecteurs, graphiques', 'blocs': [
    bloc('mi_b1', 'Une force, le poids', ['mi_ouverture_cours', 'mi_r1_force', 'mi_r2_poids'],
         ['On apprend : référentiel, repère, trajectoire, vitesse, principe d’inertie.', 'I. Rappels : les forces', '1. Une force',
          'Définition : une force est représentée par un vecteur : point d’application, droite d’action, sens, intensité (en N).',
          'Une force est de contact (la main qui pousse) ou à distance (le poids).',
          'Formule : P = m·g (P en N, m en kg, g = 10 N/kg) ; P⃗ vertical, vers le bas, appliqué en G.'],
         ('Cahier fermé : écris la relation du poids avec ses unités.', 'P = m·g (P en N, m en kg, g ≈ 10 N/kg).', 'C1'),
         qcm('Le poids d’un corps de 4 kg (g = 10 N/kg) vaut…', ['4 N', '40 N', '0,4 N'], 1)),
    bloc('mi_b2', 'Deux forces qui se compensent', ['mi_r3_reaction', 'mi_r3b_compense'],
         ['2. Deux forces qui se compensent', 'La réaction R⃗ d’un support sans frottement est perpendiculaire au support.',
          'Définition : deux forces se compensent si elles ont la même droite d’action, des sens contraires et la même intensité.',
          'Formule : F⃗₁ + F⃗₂ = 0⃗ (un livre posé : P⃗ + R⃗ = 0⃗)'],
         ('Cahier fermé : quand deux forces se compensent-elles ?', 'Même droite d’action, sens contraires, même intensité : F⃗₁ + F⃗₂ = 0⃗.', 'C1'),
         qcm('Un livre de 2 kg posé sur une table : la réaction R vaut…', ['2 N', '20 N', '0 N'], 1), [FIG_FORCES]),
    bloc('mi_b3', 'Vecteurs et graphiques', ['mi_r4_vecteur', 'mi_r5_graphique', 'mi_r6_droite'],
         ['3. Rappels de mathématiques', 'Dans un repère (O, i⃗, j⃗) : M(x ; y) ⇔ OM⃗ = x·i⃗ + y·j⃗.',
          'Méthode : lire un graphique : 1) les axes et leurs unités ; 2) partir de la valeur ; 3) aller à la courbe ; 4) lire l’autre axe.',
          'Formule : une droite : x = a·t + b ; b = x à t = 0 ; a = Δx/Δt (la pente).'],
         ('Cahier fermé : comment calcule-t-on la pente a d’une droite ?', 'a = Δx/Δt entre deux points de la droite.', 'C1'),
         qcm('Une droite passe par (0 ; 1) et (1 ; 4). Sa pente vaut…', ['1', '3', '4'], 1), [FIG_DROITE]),
  ]},
  {'id': 'mi_s2', 'titre': 'Séance 2 — Décrire un mouvement', 'blocs': [
    bloc('mi_b4', 'Le mouvement est relatif', ['mi_m1_bus', 'mi_m2_tableau', 'mi_m3_referentiel'],
         ['II. Le mouvement', '1. Relativité du mouvement',
          'Un corps peut être au repos par rapport à un corps, et en mouvement par rapport à un autre : le mouvement est relatif.',
          'Définition : le référentiel est un solide indéformable par rapport auquel on étudie le mouvement.',
          'Exemple : le référentiel terrestre (le sol et ce qui y est fixé).'],
         ('Cahier fermé : définis le référentiel.', 'Un solide indéformable par rapport auquel on étudie le mouvement.', 'C2'),
         qcm('Une personne assise dans une voiture qui roule est au repos par rapport…', ['au sol', 'à la voiture', 'à un arbre'], 1)),
    bloc('mi_b5', 'Le repère d’espace', ['mi_m4_axe', 'mi_m5_plan', 'mi_m6_espace'],
         ['2. Le repère d’espace', '| Mouvement | Repère | Vecteur position |', '| rectiligne | (O, i⃗) | OM⃗ = x·i⃗ |',
          '| plan | (O, i⃗, j⃗) | OM⃗ = x·i⃗ + y·j⃗ |', '| dans l’espace | (O, i⃗, j⃗, k⃗) | OM⃗ = x·i⃗ + y·j⃗ + z·k⃗ |',
          'Attention : une coordonnée peut être négative.'],
         ('Cahier fermé : écris le vecteur position dans le plan.', 'OM⃗ = x·i⃗ + y·j⃗', 'C3'),
         qcm('Une voiture sur une route droite : le repère d’espace a…', ['un axe', 'deux axes', 'trois axes'], 0)),
    bloc('mi_b6', 'Le temps et la trajectoire', ['mi_m7_temps', 'mi_m8_trajectoire', 'mi_m9_formes', 'mi_m10_valve'],
         ['3. Le repère de temps', 'Une horloge et une origine des dates t = 0, choisie par l’observateur.', '4. La trajectoire',
          'Définition : la trajectoire est l’ensemble des positions successives occupées par un point du mobile.',
          '| Rectiligne | Circulaire | Curviligne |', '| une droite | un cercle | une courbe |',
          'Attention : la trajectoire dépend du référentiel.'],
         ('Cahier fermé : définis la trajectoire.', 'L’ensemble des positions successives occupées par un point du mobile.', 'C4'),
         qcm('La trajectoire d’une balle qu’on lance en l’air vers l’avant est…', ['rectiligne', 'circulaire', 'curviligne'], 2)),
  ]},
  {'id': 'mi_s3', 'titre': 'Séance 3 — La vitesse', 'blocs': [
    bloc('mi_b7', 'La vitesse moyenne', ['mi_v1_moyenne', 'mi_v2_unites', 'mi_v3_eleve'],
         ['5. La vitesse moyenne', 'Formule : v_m = d/Δt (d en m, Δt en s, v_m en m/s)', 'Trajectoire courbe : d est la longueur de l’arc parcouru.',
          'Formule : 1 m/s = 3,6 km/h', 'Méthode : m/s → km/h : × 3,6 ; km/h → m/s : ÷ 3,6.'],
         ('Cahier fermé : écris la relation de la vitesse moyenne et ses unités.', 'v_m = d/Δt (m, s, m/s).', 'C5'),
         qcm('36 km/h en m/s, c’est…', ['10 m/s', '129,6 m/s', '3,6 m/s'], 0)),
    bloc('mi_b8', 'L’enregistrement', ['mi_e1_materiel', 'mi_e2_enregistrement', 'mi_e3_lire'],
         ['6. L’enregistrement d’un mouvement', 'Table à coussin d’air horizontale : l’autoporteur glisse sans frottement.',
          'L’éclateur marque un point toutes les τ : même durée entre deux points voisins.',
          'Méthode : durée entre deux points = (nombre d’intervalles) × τ.'],
         ('Cahier fermé : que représente τ sur un enregistrement ?', 'La durée constante entre deux points voisins.', 'C5'),
         qcm('τ = 40 ms : la durée entre M₀ et M₃ est…', ['80 ms', '120 ms', '160 ms'], 1)),
    bloc('mi_b9', 'La vitesse instantanée', ['mi_e4_instant', 'mi_e5_comparer', 'mi_e6_eleve'],
         ['7. La vitesse instantanée', 'Formule : v_i = M_{i−1}M_{i+1}/(2τ)',
          'Méthode : 1) les voisins M_{i−1} et M_{i+1} ; 2) leur distance en m ; 3) la durée 2τ en s ; 4) le calcul avec l’unité.'],
         ('Cahier fermé : écris la relation de la vitesse instantanée.', 'v_i = M_{i−1}M_{i+1}/(2τ)', 'C5'),
         qcm('M₁M₃ = 4 cm et τ = 40 ms : v₂ vaut…', ['0,5 m/s', '1 m/s', '0,1 m/s'], 0)),
  ]},
  {'id': 'mi_s4', 'titre': 'Séance 4 — Le vecteur vitesse et le mouvement rectiligne uniforme', 'blocs': [
    bloc('mi_b10', 'Le vecteur vitesse', ['mi_e7_vecteur', 'mi_e8_echelle', 'mi_e9_eleve'],
         ['8. Le vecteur vitesse', '| Origine | Direction | Sens | Valeur |', '| M_i | tangente à la trajectoire | celui du mouvement | v_i |',
          'Méthode : 1) choisir l’échelle ; 2) longueur = v_i ÷ échelle ; 3) tracer depuis M_i, dans le sens du mouvement.'],
         ('Cahier fermé : donne les quatre caractéristiques du vecteur vitesse.', 'Origine M_i ; tangent à la trajectoire ; sens du mouvement ; valeur v_i.', 'C6'),
         qcm('Échelle 1 cm ↔ 2 m/s : un vecteur de 6 m/s mesure…', ['3 cm', '12 cm', '6 cm'], 0)),
    bloc('mi_b11', 'Le mouvement rectiligne uniforme', ['mi_u1_tableau', 'mi_u2_courbe', 'mi_u3_pente'],
         ['9. Le mouvement rectiligne uniforme (MRU)', 'Définition : MRU : trajectoire rectiligne et vitesse constante.',
          'La courbe x = f(t) d’un MRU est une droite : x = a·t + b.', 'La pente a est la vitesse ; b = x₀, l’abscisse à t = 0.'],
         ('Cahier fermé : définis le mouvement rectiligne uniforme.', 'Trajectoire rectiligne et vitesse constante.', 'C6'),
         qcm('Pour un MRU, la courbe x = f(t) est…', ['une droite', 'une parabole', 'un cercle'], 0), [FIG_XT]),
    bloc('mi_b12', 'L’équation horaire', ['mi_u4_equation', 'mi_u5_signe', 'mi_u6_eleve'],
         ['Formule : équation horaire du MRU : x(t) = v_x·t + x₀', 'v_x = +v si l’axe est dans le sens du mouvement ; v_x = −v sinon.',
          'Méthode : 1) v ; 2) x₀ (l’abscisse à t = 0) ; 3) écrire x(t) = v_x·t + x₀ (x en m, t en s).'],
         ('Cahier fermé : écris l’équation horaire du MRU.', 'x(t) = v_x·t + x₀', 'C6'),
         qcm('x(t) = 3·t + 2 (SI) : la vitesse vaut…', ['2 m/s', '3 m/s', '5 m/s'], 1)),
  ]},
  {'id': 'mi_s5', 'titre': 'Séance 5 — Le mouvement circulaire uniforme et le centre d’inertie', 'blocs': [
    bloc('mi_b13', 'Le mouvement circulaire uniforme', ['mi_c1_circulaire', 'mi_c2_omega', 'mi_c3_periode'],
         ['10. Le mouvement circulaire uniforme (MCU)', 'Définition : MCU : trajectoire circulaire et vitesse constante.',
          'Formule : ω = v/R (ω en rad/s, v en m/s, R en m)', 'Formule : T = 2π/ω (en s) : la durée d’un tour.',
          'Formule : f = 1/T (en Hz) : le nombre de tours par seconde.'],
         ('Cahier fermé : écris les relations de ω, T et f.', 'ω = v/R ; T = 2π/ω ; f = 1/T.', 'C7'),
         qcm('La fréquence f d’un MCU s’exprime en…', ['rad/s', 'Hz', 's'], 1), [FIG_CERCLE]),
    bloc('mi_b14', 'Méthode : ω, T et f', ['mi_c4_methode', 'mi_c5_eleve'],
         ['Méthode : 1) v = arc/τ ; 2) ω = v/R ; 3) T = 2π/ω ; 4) f = 1/T, chaque fois avec l’unité.', 'Attention : R en mètres ; f = 1/T = ω/(2π).'],
         ('Cahier fermé : donne les étapes du calcul de T à partir d’un enregistrement circulaire.', 'v = arc/τ, puis ω = v/R, puis T = 2π/ω.', 'C7'),
         qcm('ω = 2π rad/s : la période vaut…', ['1 s', '2π s', '0,5 s'], 0)),
    bloc('mi_b15', 'Le centre d’inertie', ['mi_i1_curling', 'mi_i2_rotation', 'mi_i3_axes', 'mi_i4_symetrie'],
         ['III. Le principe d’inertie', '1. Le centre d’inertie',
          'Un solide lancé sur une table horizontale : un seul de ses points est toujours en MRU.',
          'Définition : ce point est le centre d’inertie G du solide.',
          'Corps homogène : G est à l’intersection de ses éléments de symétrie (sphère, cylindre, disque : au centre).'],
         ('Cahier fermé : qu’a de particulier le centre d’inertie d’un autoporteur lancé ?', 'C’est le seul point toujours en mouvement rectiligne uniforme.', 'C8'),
         qcm('Le centre d’inertie d’une boule homogène est…', ['à sa surface', 'en son centre', 'en dessous d’elle'], 1)),
  ]},
  {'id': 'mi_s6', 'titre': 'Séance 6 — Le principe d’inertie et le centre de masse', 'blocs': [
    bloc('mi_b16', 'Le principe d’inertie', ['mi_i5_translation', 'mi_i6_forces', 'mi_i7_isole', 'mi_i8_enonce'],
         ['2. Systèmes isolés et pseudo-isolés', 'Définition : isolé : soumis à aucune force (n’existe pas en pratique).',
          'Définition : pseudo-isolé : les forces se compensent, ΣF⃗ = 0⃗ (ex. : P⃗ + R⃗ = 0⃗).', '3. Le principe d’inertie',
          'Définition : dans un référentiel galiléen, si un solide est isolé ou pseudo-isolé, G est au repos ou en MRU (v⃗_G constant).'],
         ('Cahier fermé : énonce le principe d’inertie.', 'Dans un référentiel galiléen, un solide isolé ou pseudo-isolé a son centre d’inertie au repos ou en MRU.', 'C8'),
         qcm('L’autoporteur glisse sur la table horizontale sans frottement : il est…', ['isolé', 'pseudo-isolé', 'ni l’un ni l’autre'], 1)),
    bloc('mi_b17', 'Référentiel galiléen et méthode', ['mi_i9_galileen', 'mi_i10_grue', 'mi_i11_eleve'],
         ['4. Le référentiel galiléen', 'Référentiel où le principe d’inertie est vérifié : le référentiel terrestre ; tout référentiel en MRU par rapport à lui.',
          'Méthode : 1) le système ; 2) les forces (schéma) ; 3) le mouvement de G (repos ou MRU) ; 4) ΣF⃗ = 0⃗ → la force cherchée.'],
         ('Cahier fermé : donne les quatre étapes pour appliquer le principe d’inertie.', 'Système ; inventaire des forces ; mouvement de G ; somme des forces nulle.', 'C8'),
         qcm('Un ascenseur de 500 kg monte à vitesse constante (g = 10 N/kg). La tension du câble vaut…', ['500 N', '5 000 N', '0 N'], 1)),
    bloc('mi_b18', 'Le centre de masse', ['mi_g1_haltere', 'mi_g2_relation', 'mi_g3_marteau', 'mi_g4_eleve'],
         ['5. Le centre de masse', 'Centre de masse C de points A_i de masses m_i : Σ m_i·CA⃗_i = 0⃗ ; solide homogène : C et G confondus.',
          'Deux masses égales : C est au milieu du segment.', 'Formule : OG⃗ = (m₁·OG⃗₁ + m₂·OG⃗₂)/(m₁ + m₂), O point quelconque',
          'Méthode : prendre O en G₁ : G₁G⃗ = m₂·G₁G⃗₂/(m₁ + m₂).'],
         ('Cahier fermé : écris la relation barycentrique pour deux corps.', 'OG⃗ = (m₁·OG⃗₁ + m₂·OG⃗₂)/(m₁ + m₂)', 'C9'),
         qcm('m₁ = m₂ : le centre de masse est…', ['au milieu de G₁G₂', 'en G₁', 'en G₂'], 0), [FIG_HALTERE]),
  ]},
  {'id': 'mi_s7', 'titre': 'Séance 7 — Retenir et réviser', 'blocs': [
    bloc('mi_b19', 'Ce qu’il faut retenir', ['mi_b1_bilan', 'mi_b2_carte'],
         ['Bilan : les formules à savoir', '| v_m = d/Δt | v_i = M_{i−1}M_{i+1}/(2τ) | x(t) = v_x·t + x₀ |', '| ω = v/R | T = 2π/ω | f = 1/T |',
          'Principe d’inertie : ΣF⃗ = 0⃗ ⇔ v⃗_G constant (référentiel galiléen).'],
         ('Cahier fermé : écris l’équation horaire du MRU et la relation ω = v/R.', 'x(t) = v_x·t + x₀ ; ω = v/R.', 'C6'),
         qcm('Un solide pseudo-isolé, dans un référentiel galiléen, a son centre d’inertie…', ['accéléré', 'au repos ou en MRU', 'en MCU'], 1)),
    bloc('mi_bloc_fin_cours', 'Fin du cours : retenir et réviser', ['mi_fermeture_cours'],
         ['Méthode : 1) relire le cahier ; 2) refaire seul les calculs (v_m, v_i, x(t), ω, T, f, une tension, un centre de masse) ; 3) rédiger : relation → application numérique → résultat avec son unité.'],
         ('Cahier fermé : cite trois idées à retenir du cours.', 'Le mouvement est relatif ; MRU : x(t) = v_x·t + x₀ ; principe d’inertie : pseudo-isolé ⇒ G au repos ou en MRU.', 'C8'),
         qcm('Pour un calcul en physique, on écrit…', ['le résultat seul', 'la relation, l’application numérique, le résultat avec l’unité', 'l’unité seule'], 1)),
  ]},
]
