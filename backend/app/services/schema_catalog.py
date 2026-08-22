"""Les schémas SVG disponibles, vus depuis le serveur — FICHIER GÉNÉRÉ.

Ne pas éditer à la main : lancer `python tools/generate_schema_catalog.py`
après avoir ajouté un schéma dans
`frontend/src/components/session/schemas/schemas_*.ts`.

Le catalogue sert au prompt : un identifiant absent d'ici n'existe pas pour le
modèle, et un schéma que personne ne nomme ne s'affiche jamais.
"""

from __future__ import annotations

import re
import unicodedata
from functools import lru_cache

SCHEMA_CATALOG: list[dict] = [
    {"id": 'chem_cinetique', "title": 'Transformations lentes et rapides — facteurs cinétiques', "subject": 'chemistry', "keywords": ['cinétique', 'vitesse', 'réaction', 'concentration', 'temps demi-réaction', 'avancement', 'سرعة التفاعل', 'حركية كيميائية', 'facteurs cinétiques']},
    {"id": 'chem_radioactivite', "title": 'Radioactivité — Décroissance radioactive', "subject": 'chemistry', "keywords": ['radioactivité', 'décroissance', 'demi-vie', 'alpha', 'beta', 'gamma', 'noyau', 'نشاط إشعاعي', 'عمر النصف', 'تفكك']},
    {"id": 'chem_acides_bases', "title": 'Acides et bases — Équilibres en solution aqueuse', "subject": 'chemistry', "keywords": ['acide', 'base', 'pH', 'Ka', 'pKa', 'tampon', 'titrage', 'dosage', 'حمض', 'قاعدة', 'معايرة', 'équilibre']},
    {"id": 'chem_piles_electrolyse', "title": 'Piles électrochimiques et électrolyse', "subject": 'chemistry', "keywords": ['pile', 'électrolyse', 'anode', 'cathode', 'oxydation', 'réduction', 'fem', 'galvani', 'عمود كهروكيميائي', 'تحليل كهربائي', 'قطب']},
    {"id": 'chem_esterification', "title": 'Estérification et hydrolyse', "subject": 'chemistry', "keywords": ['ester', 'estérification', 'hydrolyse', 'acide carboxylique', 'alcool', 'rendement', 'catalyse', 'أسترة', 'حلمأة', 'كيمياء عضوية']},
    {"id": 'math_limites', "title": 'Limites et continuité — méthodes du BAC', "subject": 'math', "keywords": ['limite', 'continuité', 'asymptote', 'infini', 'indétermination', 'théorème', 'نهاية', 'دالة', 'استمرارية']},
    {"id": 'math_derivation', "title": 'Dérivation — Tableau de dérivées et applications', "subject": 'math', "keywords": ['dérivée', 'dérivation', 'tangente', 'variation', 'tableau', 'extremum', 'مشتقة', 'اشتقاق', 'دراسة دالة']},
    {"id": 'math_exp_ln', "title": 'Fonctions exponentielle et logarithme', "subject": 'math', "keywords": ['exponentielle', 'logarithme', 'ln', 'exp', 'croissance', 'décroissance', 'أسية', 'لوغاريتم']},
    {"id": 'math_suites', "title": 'Suites numériques — Arithmétiques et géométriques', "subject": 'math', "keywords": ['suite', 'arithmétique', 'géométrique', 'convergence', 'raison', 'terme général', 'somme', 'متتالية', 'حسابية', 'هندسية']},
    {"id": 'math_integrales', "title": "Intégration — Primitives et calcul d'aires", "subject": 'math', "keywords": ['intégrale', 'primitive', 'aire', 'intégration', 'parties', 'تكامل', 'مساحة', 'دالة أصلية']},
    {"id": 'math_probabilites', "title": 'Probabilités — Lois et dénombrement', "subject": 'math', "keywords": ['probabilité', 'dénombrement', 'combinaison', 'arrangement', 'bernoulli', 'binomiale', 'variable aléatoire', 'espérance', 'احتمال', 'توزيع', 'ثنائي الحدين']},
    {"id": 'phys_ondes_mecaniques', "title": 'Ondes mécaniques progressives — propagation et retard', "subject": 'physics', "keywords": ['onde', 'mécanique', 'progressive', 'perturbation', 'propagation', 'retard', 'célérité', 'transversale', 'longitudinale', 'موجة', 'انتشار']},
    {"id": 'phys_dipole_rc', "title": 'Dipôle RC — Charge et décharge', "subject": 'physics', "keywords": ['rc', 'condensateur', 'charge', 'décharge', 'constante temps', 'tau', 'exponentielle', 'مكثف', 'ثنائي القطب']},
    {"id": 'phys_rlc', "title": 'Oscillations RLC série', "subject": 'physics', "keywords": ['rlc', 'oscillations', 'libres', 'amorties', 'pseudo-période', 'résonance', 'énergie', 'تذبذبات', 'حرة', 'رنين']},
    {"id": 'phys_newton', "title": 'Les trois lois de Newton', "subject": 'physics', "keywords": ['newton', 'lois', 'inertie', 'accélération', 'action réaction', 'force', 'قوانين نيوتن', 'مركز القصور']},
    {"id": 'svt_glycolyse', "title": 'La Glycolyse — Dégradation du glucose', "subject": 'svt', "keywords": ['glycolyse', 'glucose', 'pyruvate', 'atp', 'cytoplasme', 'تحلل سكري', 'التحلل السكري', 'dégradation']},
    {"id": 'svt_respiration_cellulaire', "title": "Respiration cellulaire — Vue d'ensemble", "subject": 'svt', "keywords": ['respiration', 'cellulaire', 'aérobie', 'mitochondrie', 'krebs', 'chaîne respiratoire', 'atp', 'oxygène', 'تنفس خلوي', 'السلسلة التنفسية']},
    {"id": 'svt_fermentation', "title": 'Fermentation — Voies anaérobies', "subject": 'svt', "keywords": ['fermentation', 'anaérobie', 'lactique', 'alcoolique', 'éthanol', 'sans oxygène', 'تخمر', 'comparaison']},
    {"id": 'svt_muscle_sarcomere', "title": 'Structure du sarcomère', "subject": 'svt', "keywords": ['sarcomère', 'sarcomere', 'muscle', 'strié', 'actine', 'myosine', 'contraction', 'عضلة', 'بنية العضلة']},
    {"id": 'svt_adn_structure', "title": "Structure de l'ADN — Double hélice", "subject": 'svt', "keywords": ['adn', 'double hélice', 'nucléotide', 'base azotée', 'watson', 'crick', 'complémentarité', 'الحمض النووي', 'بنية']},
    {"id": 'svt_transcription_traduction', "title": 'Expression génétique — Transcription et Traduction', "subject": 'svt', "keywords": ['transcription', 'traduction', 'arnm', 'protéine', 'ribosome', 'codon', 'acide aminé', 'استنساخ', 'ترجمة', 'expression']},
    {"id": 'svt_mitose', "title": 'La Mitose — Division cellulaire conservatrice', "subject": 'svt', "keywords": ['mitose', 'division', 'prophase', 'métaphase', 'anaphase', 'télophase', 'chromosome', 'انقسام غير مباشر']},
    {"id": 'svt_subduction', "title": "Subduction — Plongement d'une plaque océanique", "subject": 'svt', "keywords": ['subduction', 'plaque plongeante', 'plaque océanique', 'fosse', 'volcanisme', 'arc volcanique', 'métamorphisme', 'الغوص', 'صفيحة']},
    {"id": 'svt_cellule_mitochondrie', "title": 'De la cellule à la mitochondrie', "subject": 'svt', "keywords": ['cellule', 'cellule eucaryote', 'cytoplasme', 'noyau', 'mitochondrie', 'respiration cellulaire', 'خلية', 'الميتوكندري']},
    {"id": 'svt_mitochondrie_structure', "title": 'Structure de la Mitochondrie — Ultrastructure', "subject": 'svt', "keywords": ['mitochondrie', 'ultrastructure de la mitochondrie', 'crêtes mitochondriales', 'membrane interne', 'membrane externe', 'crêtes', 'matrice', 'espace intermembranaire', 'الميتوكندري', 'بنية الميتوكندري']},
    {"id": 'svt_chaine_respiratoire', "title": 'Chaîne respiratoire et Phosphorylation oxydative', "subject": 'svt', "keywords": ['chaîne respiratoire', 'phosphorylation oxydative', 'atp synthase', 'complexe', 'gradient', 'nadh', 'fadh2', 'السلسلة التنفسية', 'الفسفرة التأكسدية']},
    {"id": 'svt_cycle_krebs', "title": 'Cycle de Krebs — Détail des réactions', "subject": 'svt', "keywords": ['krebs', 'cycle', 'acétyl-coa', 'citrate', 'oxaloacétate', 'matrice', 'حلقة كريبس', 'دورة كريبس']},
    {"id": 'svt_fibre_musculaire', "title": 'Ultrastructure de la fibre musculaire striée', "subject": 'svt', "keywords": ['fibre musculaire', 'myofibrille', 'réticulum sarcoplasmique', 'tubule t', 'triade', 'ultrastructure', 'الألياف العضلية', 'بنية العضلة']},
    {"id": 'svt_bilan_energetique', "title": 'Bilan énergétique — Respiration vs Fermentation', "subject": 'svt', "keywords": ['bilan', 'énergétique', 'rendement', 'comparaison', 'respiration', 'fermentation', 'atp', 'حصيلة طاقية', 'مقارنة']},
    {"id": 'svt_dorsale_accretion', "title": 'Dorsale océanique — Accrétion et expansion océanique', "subject": 'svt', "keywords": ['dorsale', 'accrétion', 'expansion océanique', 'expansion des fonds', 'plancher océanique', 'rift', 'basalte', 'gabbro', 'chambre magmatique', 'anomalies magnétiques', 'asthénosphère', 'الظهرة المحيطية', 'التوسع المحيطي']},
]

SCHEMA_IDS: frozenset[str] = frozenset(entry["id"] for entry in SCHEMA_CATALOG)


@lru_cache(maxsize=None)
def _motif(mot: str) -> re.Pattern:
    """Un mot-clé ne compte que s'il est un MOT, pas une suite de lettres.

    Cherché en simple sous-chaîne, `exp` se trouve dans « expansion » et `ln`
    dans une dizaine de mots : un cours sur la dorsale océanique se voyait
    proposer le schéma des fonctions exponentielles. Les bornes règlent le
    problème pour le français comme pour l'arabe, les bornes de mot étant
    unicode.

    Le pluriel reste admis (`s` ou `x` final) : un cours parle des
    « myofibrilles » et des « crêtes », le mot-clé est au singulier, et
    l'exiger à la lettre faisait manquer le bon schéma.
    """
    return re.compile(rf"(?<!\w){re.escape(_sans_accents(mot))}[sx]?(?!\w)", re.UNICODE)


def _sans_accents(texte: str) -> str:
    """Un eleve tape « accretion » : le mot-cle accentue doit quand meme repondre."""
    plie = unicodedata.normalize("NFKD", texte.lower())
    return "".join(c for c in plie if not unicodedata.combining(c))


def match_schema(context: str) -> tuple[str | None, int]:
    """Le schéma de la bibliothèque qui colle le mieux au contexte, et son score.

    Un mot-clé en PLUSIEURS mots pèse double : « fibre musculaire » désigne un
    schéma, « muscle » désigne un chapitre entier. Sans cette pondération, un
    cours sur la fibre musculaire se voyait proposer le sarcomère, les deux
    étant à égalité sur des mots génériques.

    Les appelants décident du seuil : rapprocher n'est pas afficher.
    """
    contexte = _sans_accents(context or "")
    if not contexte.strip():
        return None, 0

    meilleur_id, meilleur_score, meilleur_precision = None, 0, 0
    for entry in SCHEMA_CATALOG:
        trouves = [mot for mot in entry["keywords"] if _motif(mot).search(contexte)]
        if not trouves:
            continue
        score = sum(2 if " " in mot.strip() else 1 for mot in trouves)
        # À score égal, le mot-clé le plus long tranche : « fibre musculaire »
        # l'emporte sur « muscle », qui désigne le chapitre et non la figure.
        precision = max(len(mot) for mot in trouves)
        if (score, precision) > (meilleur_score, meilleur_precision):
            meilleur_id, meilleur_score, meilleur_precision = entry["id"], score, precision
    return (meilleur_id, meilleur_score) if meilleur_score else (None, 0)


def schema_title(schema_id: str) -> str:
    for entry in SCHEMA_CATALOG:
        if entry["id"] == schema_id:
            return entry["title"]
    return ""


SCHEMA_CATALOG_PROMPT = """[SCHÉMAS SVG DISPONIBLES — 30 identifiants]
Ces schémas sont déjà dessinés, animés et annotés. Les afficher coûte moins
cher et rend mieux qu'un dessin improvisé : si l'un d'eux couvre la notion,
c'est LUI qu'on affiche, dans TOUS les modes (cours, exercice, examen,
question libre).
Format : <schema>identifiant</schema> — ou l'action `show_schema`.
N'INVENTE JAMAIS un identifiant : s'il n'est pas dans cette liste, il n'existe
pas, et l'élève ne voit rien.

  SVT :
    svt_glycolyse — La Glycolyse — Dégradation du glucose
    svt_respiration_cellulaire — Respiration cellulaire — Vue d'ensemble
    svt_fermentation — Fermentation — Voies anaérobies
    svt_muscle_sarcomere — Structure du sarcomère
    svt_adn_structure — Structure de l'ADN — Double hélice
    svt_transcription_traduction — Expression génétique — Transcription et Traduction
    svt_mitose — La Mitose — Division cellulaire conservatrice
    svt_subduction — Subduction — Plongement d'une plaque océanique
    svt_cellule_mitochondrie — De la cellule à la mitochondrie
    svt_mitochondrie_structure — Structure de la Mitochondrie — Ultrastructure
    svt_chaine_respiratoire — Chaîne respiratoire et Phosphorylation oxydative
    svt_cycle_krebs — Cycle de Krebs — Détail des réactions
    svt_fibre_musculaire — Ultrastructure de la fibre musculaire striée
    svt_bilan_energetique — Bilan énergétique — Respiration vs Fermentation
    svt_dorsale_accretion — Dorsale océanique — Accrétion et expansion océanique
  PHYSIQUE :
    phys_ondes_mecaniques — Ondes mécaniques progressives — propagation et retard
    phys_dipole_rc — Dipôle RC — Charge et décharge
    phys_rlc — Oscillations RLC série
    phys_newton — Les trois lois de Newton
  CHIMIE :
    chem_cinetique — Transformations lentes et rapides — facteurs cinétiques
    chem_radioactivite — Radioactivité — Décroissance radioactive
    chem_acides_bases — Acides et bases — Équilibres en solution aqueuse
    chem_piles_electrolyse — Piles électrochimiques et électrolyse
    chem_esterification — Estérification et hydrolyse
  MATHS :
    math_limites — Limites et continuité — méthodes du BAC
    math_derivation — Dérivation — Tableau de dérivées et applications
    math_exp_ln — Fonctions exponentielle et logarithme
    math_suites — Suites numériques — Arithmétiques et géométriques
    math_integrales — Intégration — Primitives et calcul d'aires
    math_probabilites — Probabilités — Lois et dénombrement
"""
