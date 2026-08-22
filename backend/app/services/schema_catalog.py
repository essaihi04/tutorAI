"""Les schémas SVG disponibles, vus depuis le serveur — FICHIER GÉNÉRÉ.

Ne pas éditer à la main : lancer `python tools/generate_schema_catalog.py`
après avoir ajouté un schéma dans
`frontend/src/components/session/schemas/schemas_*.ts`.

Le catalogue sert au prompt : un identifiant absent d'ici n'existe pas pour le
modèle, et un schéma que personne ne nomme ne s'affiche jamais.
"""

from __future__ import annotations

SCHEMA_CATALOG: list[dict[str, str]] = [
    {"id": 'chem_cinetique', "title": 'Cinétique chimique — Vitesse de réaction', "subject": 'chemistry'},
    {"id": 'chem_radioactivite', "title": 'Radioactivité — Décroissance radioactive', "subject": 'chemistry'},
    {"id": 'chem_acides_bases', "title": 'Acides et bases — Équilibres en solution aqueuse', "subject": 'chemistry'},
    {"id": 'chem_piles_electrolyse', "title": 'Piles électrochimiques et électrolyse', "subject": 'chemistry'},
    {"id": 'chem_esterification', "title": 'Estérification et hydrolyse', "subject": 'chemistry'},
    {"id": 'math_limites', "title": 'Limites de fonctions — Cas fondamentaux', "subject": 'math'},
    {"id": 'math_derivation', "title": 'Dérivation — Tableau de dérivées et applications', "subject": 'math'},
    {"id": 'math_exp_ln', "title": 'Fonctions exponentielle et logarithme', "subject": 'math'},
    {"id": 'math_suites', "title": 'Suites numériques — Arithmétiques et géométriques', "subject": 'math'},
    {"id": 'math_integrales', "title": "Intégration — Primitives et calcul d'aires", "subject": 'math'},
    {"id": 'math_probabilites', "title": 'Probabilités — Lois et dénombrement', "subject": 'math'},
    {"id": 'phys_ondes_mecaniques', "title": 'Ondes mécaniques — Caractéristiques', "subject": 'physics'},
    {"id": 'phys_dipole_rc', "title": 'Dipôle RC — Charge et décharge', "subject": 'physics'},
    {"id": 'phys_rlc', "title": 'Oscillations RLC série', "subject": 'physics'},
    {"id": 'phys_newton', "title": 'Les trois lois de Newton', "subject": 'physics'},
    {"id": 'svt_glycolyse', "title": 'La Glycolyse — Dégradation du glucose', "subject": 'svt'},
    {"id": 'svt_respiration_cellulaire', "title": "Respiration cellulaire — Vue d'ensemble", "subject": 'svt'},
    {"id": 'svt_fermentation', "title": 'Fermentation — Voies anaérobies', "subject": 'svt'},
    {"id": 'svt_muscle_sarcomere', "title": 'Structure du sarcomère', "subject": 'svt'},
    {"id": 'svt_adn_structure', "title": "Structure de l'ADN — Double hélice", "subject": 'svt'},
    {"id": 'svt_transcription_traduction', "title": 'Expression génétique — Transcription et Traduction', "subject": 'svt'},
    {"id": 'svt_mitose', "title": 'La Mitose — Division cellulaire conservatrice', "subject": 'svt'},
    {"id": 'svt_subduction', "title": "Subduction — Plongement d'une plaque océanique", "subject": 'svt'},
    {"id": 'svt_cellule_mitochondrie', "title": 'De la cellule à la mitochondrie', "subject": 'svt'},
    {"id": 'svt_mitochondrie_structure', "title": 'Structure de la Mitochondrie — Ultrastructure', "subject": 'svt'},
    {"id": 'svt_chaine_respiratoire', "title": 'Chaîne respiratoire et Phosphorylation oxydative', "subject": 'svt'},
    {"id": 'svt_cycle_krebs', "title": 'Cycle de Krebs — Détail des réactions', "subject": 'svt'},
    {"id": 'svt_fibre_musculaire', "title": 'Ultrastructure de la fibre musculaire striée', "subject": 'svt'},
    {"id": 'svt_bilan_energetique', "title": 'Bilan énergétique — Respiration vs Fermentation', "subject": 'svt'},
    {"id": 'svt_dorsale_accretion', "title": 'Dorsale océanique — Accrétion et expansion océanique', "subject": 'svt'},
]

SCHEMA_IDS: frozenset[str] = frozenset(entry["id"] for entry in SCHEMA_CATALOG)

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
    phys_ondes_mecaniques — Ondes mécaniques — Caractéristiques
    phys_dipole_rc — Dipôle RC — Charge et décharge
    phys_rlc — Oscillations RLC série
    phys_newton — Les trois lois de Newton
  CHIMIE :
    chem_cinetique — Cinétique chimique — Vitesse de réaction
    chem_radioactivite — Radioactivité — Décroissance radioactive
    chem_acides_bases — Acides et bases — Équilibres en solution aqueuse
    chem_piles_electrolyse — Piles électrochimiques et électrolyse
    chem_esterification — Estérification et hydrolyse
  MATHS :
    math_limites — Limites de fonctions — Cas fondamentaux
    math_derivation — Dérivation — Tableau de dérivées et applications
    math_exp_ln — Fonctions exponentielle et logarithme
    math_suites — Suites numériques — Arithmétiques et géométriques
    math_integrales — Intégration — Primitives et calcul d'aires
    math_probabilites — Probabilités — Lois et dénombrement
"""
