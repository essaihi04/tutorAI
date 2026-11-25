# -*- coding: utf-8 -*-
"""Construit le cours de /TCF « Synthèse d'une espèce chimique » (tc_chim_synthese, 25/11/2026).

Usage : python -X utf8 scripts/tcf/synthese/construire.py
Écrit frontend/src/publication/tcf/cours/tc_chim_synthese.json (puis lancer scripts/tcf/lister_voix_tcf.py pour la
liste des voix). Contenu : docs/tcf/CONTENU_LIVRE.md, section « Synthèse d'espèces chimiques ».
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from outils import SLIDES, _controle_parole
import partie1, partie2  # noqa: F401 (remplissent SLIDES)

RACINE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
SORTIE = os.path.join(RACINE, 'frontend', 'src', 'publication', 'tcf', 'cours', 'tc_chim_synthese.json')

ACTIVITES = [
    ('sy_ouverture', 'Ouverture — fabriquer une espèce chimique', 'ouverture', 5),
    ('sy_partie1', 'I. Espèces chimiques et chimie de synthèse', 'explication', 25),
    ('sy_partie2', 'II. La synthèse du savon : chauffage à reflux et traitement', 'explication', 30),
    ('sy_partie3', 'III. Identifier le produit : les constantes physiques', 'explication', 20),
    ('sy_partie4', 'IV. Identifier le produit : la CCM', 'explication', 30),
    ('sy_partie5', 'V. Application : l’acétate de benzyle', 'application', 15),
    ('sy_bilan', 'Bilan du cours', 'synthese', 10),
]


def R(id, typ, prompt, dit, attendu=None, options=None, correct=None):
    _controle_parole(dit, id)
    r = {'id': id, 'type': typ, 'prompt': prompt, 'enonce_dit': 'شوف هاد السؤال: ' + dit}
    if attendu: r['attendu'] = attendu
    if options is not None: r['options'] = options
    if correct is not None: r['correct'] = correct
    return r


COMPETENCES = [
    {'id': 'C1', 'label': 'Définir une espèce chimique et distinguer espèce naturelle et espèce synthétique', 'dit': 'définir une espèce chimique, naturelle ou synthétique',
     'rappels': [R('C1_r1', 'libre', 'Définis une espèce chimique.', 'définis une espèce chimique.', 'Une espèce chimique est un ensemble d’entités identiques.'),
                 R('C1_r2', 'qcm', 'Le sucre extrait de la canne est une espèce…', 'le sucre اللي كيجي من القصب، شنو هو؟', options=['synthétique', 'naturelle', 'mélange'], correct=1),
                 R('C1_r3', 'vrai_faux', 'L’eau minérale est une seule espèce chimique.', 'l’eau minérale هي espèce chimique واحدة. vrai ou faux؟', correct=False)]},
    {'id': 'C2', 'label': 'Citer la nécessité et les trois types de la chimie de synthèse', 'dit': 'les trois types de la chimie de synthèse',
     'rappels': [R('C2_r1', 'libre', 'Cite les trois types de la chimie de synthèse.', 'عطيني les trois types ديال la chimie de synthèse.', 'Chimie lourde, chimie des spécialités, chimie fine.'),
                 R('C2_r2', 'qcm', 'Les plastiques, fabriqués en très grandes quantités, relèvent de…', 'les plastiques، بكميات كبيرة بزاف، من أشمن chimie؟', options=['la chimie fine', 'la chimie lourde', 'la chimie des spécialités'], correct=1),
                 R('C2_r3', 'vrai_faux', 'La synthèse permet de créer des espèces qui n’existent pas dans la nature.', 'la synthèse كتقدر تصاوب des espèces ماكايناش فالطبيعة. vrai ou faux؟', correct=True)]},
    {'id': 'C3', 'label': 'Définir la synthèse et reconnaître les réactifs et les produits', 'dit': 'définir la synthèse, les réactifs et les produits',
     'rappels': [R('C3_r1', 'libre', 'Définis la synthèse d’une espèce chimique.', 'شنو معنى synthétiser une espèce chimique؟', 'La préparer à partir d’autres espèces par une transformation chimique.'),
                 R('C3_r2', 'qcm', 'Dans une transformation chimique, les réactifs…', 'فواحد la transformation chimique، les réactifs شنو كيوقع ليهم؟', options=['sont consommés', 'apparaissent', 'ne changent pas'], correct=0),
                 R('C3_r3', 'vrai_faux', 'Le savon est un réactif de sa synthèse.', 'le savon réactif ف la synthèse ديالو. vrai ou faux؟', correct=False)]},
    {'id': 'C4', 'label': 'Nommer les éléments du montage à reflux et le rôle des espèces du ballon', 'dit': 'le montage à reflux et le rôle de l’éthanol et de la pierre ponce',
     'rappels': [R('C4_r1', 'libre', 'Cite les éléments du montage de chauffage à reflux.', 'عطيني les éléments ديال le montage ديال le chauffage à reflux.', 'Potence, support élévateur, chauffe-ballon, ballon, réfrigérant à boules.'),
                 R('C4_r2', 'qcm', 'Dans le réfrigérant, l’eau froide entre…', 'ف le réfrigérant، الما البارد من فين كيدخل؟', options=['par le haut', 'par le bas', 'par le ballon'], correct=1),
                 R('C4_r3', 'qcm', 'La pierre ponce sert à…', 'la pierre ponce، علاش كتصلح؟', options=['favoriser le contact', 'régulariser l’ébullition', 'refroidir'], correct=1)]},
    {'id': 'C5', 'label': 'Expliquer le rôle du chauffage et du reflux', 'dit': 'le rôle du chauffage et du reflux',
     'rappels': [R('C5_r1', 'libre', 'Quel est le rôle du chauffage ? et du reflux ?', 'شنو الدور ديال le chauffage؟ و le reflux؟', 'Le chauffage accélère la réaction ; le reflux évite la perte de réactifs et de produits.'),
                 R('C5_r2', 'vrai_faux', 'Sans réfrigérant, les vapeurs s’échappent : on perd de la matière.', 'بلا réfrigérant، les vapeurs كيخرجو، وكنضيعو la matière. vrai ou faux؟', correct=True),
                 R('C5_r3', 'qcm', 'Dans le réfrigérant, les vapeurs…', 'ف le réfrigérant، les vapeurs شنو كيوليو؟', options=['se condensent et retombent', 'brûlent', 'sortent par le haut'], correct=0)]},
    {'id': 'C6', 'label': 'Décrire le traitement : refroidir, eau salée, filtrer', 'dit': 'le traitement du mélange',
     'rappels': [R('C6_r1', 'libre', 'Cite les étapes du traitement du savon.', 'عطيني les étapes ديال le traitement ديال le savon.', 'Refroidir, verser dans l’eau salée concentrée (le savon précipite), filtrer.'),
                 R('C6_r2', 'qcm', 'Dans l’eau salée concentrée, le savon…', 'فl’eau salée concentrée، le savon شنو كيدير؟', options=['précipite', 's’évapore', 'se dissout'], correct=0),
                 R('C6_r3', 'vrai_faux', 'On peut toucher le savon obtenu sans gants.', 'نقدرو نقيسو le savon اللي درنا بلا gants. vrai ou faux؟', correct=False)]},
    {'id': 'C7', 'label': 'Identifier une espèce par ses constantes physiques ; calculer ρ et d', 'dit': 'calculer la masse volumique et la densité',
     'rappels': [R('C7_r1', 'libre', 'Écris les relations de la masse volumique et de la densité.', 'كتب la relation ديال la masse volumique و ديال la densité.', 'ρ = m/V ; d = ρ/ρ(eau), sans unité.'),
                 R('C7_r2', 'qcm', '10 mL d’un liquide pèsent 9 g. Sa masse volumique est…', 'dix millilitres ديال واحد le liquide، la masse ديالهم neuf grammes. شحال la masse volumique؟', options=['0,9 g/mL', '1,1 g/mL', '90 g/mL'], correct=0),
                 R('C7_r3', 'vrai_faux', 'Un liquide de densité 0,8 coule sous l’eau.', 'le liquide اللي la densité ديالو zéro virgule huit كيبقى تحت الما. vrai ou faux؟', correct=False)]},
    {'id': 'C8', 'label': 'Réaliser et exploiter une CCM : taches, même hauteur, Rf', 'dit': 'lire un chromatogramme et calculer un rapport frontal',
     'rappels': [R('C8_r1', 'libre', 'Écris la relation du rapport frontal et le sens de h et H.', 'كتب la relation ديال le rapport frontal، وشنو هوما h و H.', 'Rf = h/H ; h : de la ligne de dépôt au centre de la tache ; H : de la ligne de dépôt au front.'),
                 R('C8_r2', 'qcm', 'H = 8 cm et h = 2 cm. Rf vaut…', 'H égale huit centimètres، و h égale deux centimètres. شحال Rf؟', options=['4', '0,25', '0,4'], correct=1),
                 R('C8_r3', 'vrai_faux', 'Une espèce pure donne plusieurs taches.', 'une espèce pure كتعطي بزاف ديال les taches. vrai ou faux؟', correct=False),
                 R('C8_r4', 'qcm', 'On révèle des taches incolores avec…', 'كيفاش كنبينو les taches incolores؟', options=['une loupe', 'une lampe UV', 'un thermomètre'], correct=1)]},
]


def bloc(id, titre, slides, cahier, comp, retrouver, attendu, exercice, figures=None):
    b = {'id': id, 'titre': titre, 'slide_ids': slides, 'cahier': [{'texte': t} for t in cahier],
         'retrouver': {'prompt': retrouver, 'attendu': attendu, 'competence_id': comp}, 'exercice': exercice}
    if figures:
        b['cahier_figures'] = figures
    return b


def construire():
    S = {s['id']: s for _, s in SLIDES}
    fig_montage = S['sy_m1_montage']['concentration']['cahier_figures']
    fig_rf = S['sy_c7_rf']['concentration']['cahier_figures']
    seances = [
        {'id': 'sy_s1', 'titre': 'Séance 1 — Espèces chimiques et chimie de synthèse', 'blocs': [
            bloc('sy_bl1', 'Fabriquer une espèce ; l’espèce chimique', ['sy_ouverture_cours', 'sy_o0_situation', 'sy_o1_espece', 'sy_o2_naturelle'],
                 ['On apprend : synthèse, chauffage à reflux, savon, CCM.', 'I. Espèces chimiques et chimie de synthèse', '1. L’espèce chimique',
                  'Définition : une espèce chimique est un ensemble d’entités identiques (molécules, ions ou atomes).',
                  '| Espèce naturelle | Espèce synthétique |', '| existe dans la nature (sucre) | préparée par l’Homme (aspirine) |'],
                 'C1', 'Cahier fermé : définis une espèce chimique.', 'Un ensemble d’entités identiques.',
                 {'type': 'qcm', 'prompt': 'Le plastique est une espèce…', 'options': ['naturelle', 'synthétique'], 'correct': 1}),
            bloc('sy_bl2', 'La synthèse : réactifs et produits', ['sy_o3_transformation', 'sy_d1_definition', 'sy_d2_savon'],
                 ['2. La synthèse', 'Dans une transformation chimique, les réactifs sont consommés et des produits apparaissent.',
                  'Définition : synthétiser une espèce chimique, c’est la préparer à partir d’autres espèces par une transformation chimique.',
                  'Exemple : huile + soude → savon + glycérol (réactifs → produits).'],
                 'C3', 'Cahier fermé : définis la synthèse d’une espèce chimique.', 'La préparer à partir d’autres espèces par une transformation chimique.',
                 {'type': 'qcm', 'prompt': 'L’huile, dans la synthèse du savon, est…', 'options': ['un produit', 'un réactif'], 'correct': 1}),
            bloc('sy_bl3', 'Pourquoi la chimie de synthèse ; ses trois types', ['sy_n1_pourquoi', 'sy_n2_types', 'sy_n3_tri'],
                 ['3. La chimie de synthèse', 'Elle produit en grandes quantités et moins cher, et crée des espèces nouvelles.',
                  '| Chimie lourde | Chimie des spécialités | Chimie fine |',
                  '| produits de base, très grandes quantités (plastiques) | produits intermédiaires (peintures) | produits complexes, petites quantités (médicaments) |'],
                 'C2', 'Cahier fermé : cite les trois types de la chimie de synthèse.', 'Chimie lourde, chimie des spécialités, chimie fine.',
                 {'type': 'qcm', 'prompt': 'Une peinture relève de…', 'options': ['la chimie fine', 'la chimie des spécialités'], 'correct': 1}),
        ]},
        {'id': 'sy_s2', 'titre': 'Séance 2 — La synthèse du savon', 'blocs': [
            bloc('sy_bl4', 'Le montage à reflux et le ballon', ['sy_m1_montage', 'sy_m2_contenu', 'sy_m3_roles'],
                 ['II. La synthèse du savon', '1. Le chauffage à reflux',
                  'Le montage : potence, support élévateur, chauffe-ballon, ballon, réfrigérant à boules.', 'Remarque : l’eau froide entre en bas du réfrigérant et sort en haut.',
                  'Dans le ballon : huile d’olive, éthanol, solution de soude, pierre ponce.',
                  '| Éthanol | Pierre ponce |', '| favorise le contact entre les réactifs | régularise l’ébullition |',
                  'Attention : la soude est corrosive : lunettes et gants.'],
                 'C4', 'Cahier fermé : nomme les éléments du montage à reflux.', 'Potence, support élévateur, chauffe-ballon, ballon, réfrigérant à boules.',
                 {'type': 'qcm', 'prompt': 'L’eau froide entre dans le réfrigérant…', 'options': ['par le haut', 'par le bas'], 'correct': 1}, figures=fig_montage),
            bloc('sy_bl5', 'Le chauffage et le reflux', ['sy_r1_chauffage', 'sy_r2_reflux', 'sy_r3_bilan'],
                 ['2. Le rôle du chauffage et du reflux', 'Le chauffage augmente la vitesse de la réaction.',
                  'Le reflux : les vapeurs se condensent dans le réfrigérant et retombent dans le ballon.',
                  'Donc le chauffage à reflux : réaction plus rapide, sans perte de réactifs ni de produits.'],
                 'C5', 'Cahier fermé : donne le rôle du chauffage et celui du reflux.', 'Chauffage : réaction plus rapide ; reflux : pas de perte de matière.',
                 {'type': 'qcm', 'prompt': 'Le réfrigérant sert à…', 'options': ['chauffer', 'condenser les vapeurs'], 'correct': 1}),
            bloc('sy_bl6', 'Le traitement : obtenir le savon', ['sy_t1_refroidir', 'sy_t2_filtrer', 'sy_t3_etapes'],
                 ['3. Le traitement', 'Méthode : 1) arrêter le chauffage et laisser refroidir ; 2) verser dans l’eau salée concentrée : le savon précipite ; 3) filtrer.',
                  'Attention : le savon obtenu contient encore de la soude : ne pas le toucher sans gants.'],
                 'C6', 'Cahier fermé : cite les étapes du traitement.', 'Refroidir, verser dans l’eau salée concentrée, filtrer.',
                 {'type': 'qcm', 'prompt': 'Le savon précipite dans…', 'options': ['l’eau salée concentrée', 'l’éthanol'], 'correct': 0}),
        ]},
        {'id': 'sy_s3', 'titre': 'Séance 3 — Identifier le produit : les constantes physiques', 'blocs': [
            bloc('sy_bl7', 'Températures et solubilité', ['sy_i1_pourquoi', 'sy_i2_temperature', 'sy_i3_solubilite'],
                 ['III. Identifier l’espèce synthétisée', '1. Les caractéristiques physiques',
                  'On compare températures de fusion et d’ébullition, solubilité, ρ et d aux valeurs des tables.',
                  'Méthode : mesurer la température de fusion (ou d’ébullition), puis chercher la même valeur dans la table.',
                  'Définition : la solubilité est la capacité d’une espèce à se dissoudre dans un solvant.'],
                 'C7', 'Cahier fermé : comment identifier une espèce par une température ?', 'On la mesure et on cherche la même valeur dans la table.',
                 {'type': 'qcm', 'prompt': 'Un solide fond à 122 °C (table : acide benzoïque 122 °C). C’est…', 'options': ['l’aspirine', 'l’acide benzoïque'], 'correct': 1}),
            bloc('sy_bl8', 'Masse volumique et densité', ['sy_i4_masse', 'sy_i5_densite'],
                 ['2. Masse volumique et densité', 'Formule : ρ = m/V (m en g, V en mL : ρ en g/mL)',
                  'Formule : d = ρ/ρ(eau), sans unité ; ρ(eau) = 1 g/mL',
                  'Remarque : d < 1 : le liquide flotte sur l’eau ; d > 1 : il coule.'],
                 'C7', 'Cahier fermé : écris ρ et d.', 'ρ = m/V ; d = ρ/ρ(eau), sans unité.',
                 {'type': 'qcm', 'prompt': '10 mL pèsent 12 g : d = …', 'options': ['1,2', '0,83'], 'correct': 0}),
        ]},
        {'id': 'sy_s4', 'titre': 'Séance 4 — Identifier le produit : la CCM', 'blocs': [
            bloc('sy_bl9', 'La CCM pas à pas', ['sy_c1_principe', 'sy_c2_depot', 'sy_c3_elution', 'sy_c4_revelation'],
                 ['3. La chromatographie sur couche mince (CCM)', '| Phase fixe | Phase mobile |', '| la plaque (gel de silice) | l’éluant (un solvant) |',
                  'Méthode : 1) ligne de dépôt au crayon à 1 cm du bas ; 2) petites gouttes, séchage ; 3) éluant sous la ligne, cuve fermée ; 4) marquer le front ; 5) révéler (UV ou diiode).'],
                 'C8', 'Cahier fermé : cite les étapes d’une CCM.', 'Dépôts sur la ligne au crayon, élution dans la cuve fermée, front marqué, révélation.',
                 {'type': 'qcm', 'prompt': 'La ligne de dépôt se trace…', 'options': ['au stylo', 'au crayon'], 'correct': 1}),
            bloc('sy_bl10', 'Lire un chromatogramme ; le rapport frontal', ['sy_c5_compter', 'sy_c6_identifier', 'sy_c7_rf', 'sy_c8_rf_eleve'],
                 ['4. Lire un chromatogramme', '| Une seule tache | Plusieurs taches |', '| une espèce pure | un mélange |',
                  'Deux taches à la même hauteur correspondent à la même espèce.',
                  'Formule : Rf = h/H (h : ligne de dépôt → centre de la tache ; H : ligne de dépôt → front), sans unité, 0 < Rf < 1',
                  'Remarque : plus Rf est grand, plus l’espèce est soluble dans l’éluant.'],
                 'C8', 'Cahier fermé : écris la relation du rapport frontal.', 'Rf = h/H, sans unité, entre 0 et 1.',
                 {'type': 'qcm', 'prompt': 'H = 5 cm, h = 2 cm : Rf = …', 'options': ['0,4', '2,5'], 'correct': 0}, figures=fig_rf),
        ]},
        {'id': 'sy_s5', 'titre': 'Séance 5 — Application et bilan', 'blocs': [
            bloc('sy_bl11', 'Application : l’acétate de benzyle', ['sy_a1_enonce', 'sy_a2_chromatogramme', 'sy_a3_rf'],
                 ['IV. Application', 'Méthode : 1) nommer les éléments du montage ; 2) compter les taches d’un dépôt ; 3) comparer les hauteurs aux références ; 4) calculer Rf = h/H et comparer.',
                  'Remarque : une espèce incolore se révèle avec une lampe UV ou des vapeurs de diiode.'],
                 'C8', 'Cahier fermé : comment savoir quelles espèces contient un mélange ?', 'On compare la hauteur de ses taches à celles des références.',
                 {'type': 'qcm', 'prompt': 'Rf(A) = 0,3 et Rf(B) = 0,6 : la plus soluble dans l’éluant est…', 'options': ['A', 'B'], 'correct': 1}),
            bloc('sy_bl12', 'Ce qu’il faut retenir', ['sy_b1_bilan', 'sy_b2_carte'],
                 ['Bilan : espèce chimique ; trois types de chimie de synthèse ; réactifs → produits ; chauffage à reflux ; traitement ; constantes physiques ; CCM.',
                  'Formule : ρ = m/V ; d = ρ/ρ(eau) ; Rf = h/H'],
                 'C8', 'Cahier fermé : écris les trois relations du chapitre.', 'ρ = m/V ; d = ρ/ρ(eau) ; Rf = h/H.',
                 {'type': 'qcm', 'prompt': 'La densité a pour unité…', 'options': ['g/mL', 'aucune'], 'correct': 1}),
            bloc('sy_bloc_fin_cours', 'Fin du cours : retenir et réviser', ['sy_fermeture_cours'],
                 ['Méthode : 1) relire le cahier ; 2) refaire seul les calculs (ρ, d, Rf) ; 3) écrire relation → application numérique → résultat avec son unité.'],
                 'C7', 'Cahier fermé : écris ρ = ?', 'ρ = m/V.', {'type': 'qcm', 'prompt': 'ρ = …', 'options': ['m/V', 'V/m'], 'correct': 0}),
        ]},
    ]
    # ordre des diapos = ordre des blocs
    ordre = [i for se in seances for b in se['blocs'] for i in b['slide_ids']]
    assert ordre == [s['id'] for _, s in SLIDES], 'les blocs ne suivent pas l’ordre des diapos'
    assert len(set(ordre)) == len(ordre)
    activities = []
    for aid, titre, phase, dur in ACTIVITES:
        sl = [s for a, s in SLIDES if a == aid]
        for k, s in enumerate(sl):
            s['order_index'] = k
        activities.append({'id': aid, 'title': titre, 'phase': phase, 'duration_minutes': dur, 'order_index': len(activities), 'slides': sl})
    comps = []
    for c in COMPETENCES:
        c = dict(c); c['slide_ids'] = [s['id'] for _, s in SLIDES if c['id'] in s['competence_ids']]
        assert c['slide_ids'], c['id']
        comps.append({k: c[k] for k in ('id', 'label', 'dit', 'slide_ids', 'rappels')})
    deck = {
        'id': 'tc_chim_synthese', 'stable_id': 'tc_chim_synthese', 'lesson_id': 'tc_chim_synthese',
        'title': 'Synthèse d’une espèce chimique', 'version': 1, 'status': 'draft', 'language': 'mixed', 'estimated_minutes': 135,
        'mode': 'concentration', 'niveau': 'tronc_commun_sciences_biof', 'subject': 'chimie',
        'lesson_match': ['synthèse d’une espèce chimique', 'synthese des especes chimiques', 'chimie de synthèse', 'chauffage à reflux', 'chromatographie CCM'],
        'catalog': {'summary': 'Tronc Commun Sciences, option française, chimie : espèce chimique, chimie de synthèse et ses trois types, réactifs et produits, synthèse du savon (chauffage à reflux, traitement), identification par les constantes physiques (ρ, d) et par CCM (Rf), application de l’acétate de benzyle.'},
        'note': 'Cours écrit en mode concentration d’après le livre « Cours physique-chimie TCSF » (résumé : docs/tcf/CONTENU_LIVRE.md). Généré par scripts/tcf/synthese/construire.py. Pas encore de voix : textes dans tc_chim_synthese_voix.json. Valeurs simples : ρ = 8 g/10 mL = 0,8 g/mL ; B : 22 g/20 mL → d = 1,1 ; CCM : H = 8 cm, Rf(A) = 0,5, Rf(B) = 0,25 ; X : 6/10 = 0,6 ; application : H = 10 cm, Rf(A) = 0,3, Rf(B) = 0,6.',
        'activities': activities, 'competences': comps, 'seances': seances,
    }
    os.makedirs(os.path.dirname(SORTIE), exist_ok=True)
    with open(SORTIE, 'w', encoding='utf-8') as f:
        json.dump(deck, f, ensure_ascii=False, indent=2)
        f.write('\n')
    n_q = sum(1 for _, s in SLIDES if s.get('question'))
    print(f'{SORTIE} : {len(SLIDES)} diapos, {sum(len(se["blocs"]) for se in seances)} blocs, {len(comps)} compétences, {n_q} questions')


if __name__ == '__main__':
    construire()
