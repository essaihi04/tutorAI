"""Synchronise le chapitre 1 de SVT avec la progression de coaching révisée.

Le mode par défaut est une prévisualisation. Utiliser ``--apply`` pour écrire.
La migration SQL homonyme reste la source de vérité pour les déploiements.
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.supabase_client import get_supabase_admin  # noqa: E402


ENERGY_OBJECTIVES = [
    "Formuler puis vérifier les conditions de la respiration et de la fermentation à partir de données expérimentales",
    "Décrire le lieu, les étapes essentielles et le bilan de la glycolyse",
    "Relier l'ultrastructure de la mitochondrie aux étapes de la respiration cellulaire",
    "Déterminer les étapes essentielles et le bilan du cycle de Krebs",
    "Expliquer la chaîne respiratoire, le rôle de l'O2 et la phosphorylation oxydative",
    "Comparer les fermentations lactique et alcoolique à partir de leurs bilans",
    "Calculer et représenter les bilans et rendements de la respiration et de la fermentation",
]

MUSCLE_OBJECTIVES = [
    "Analyser des myogrammes : secousse, sommation et tétanos",
    "Exploiter les phénomènes thermiques et chimiques associés à la contraction",
    "Décrire l'organisation du muscle, de la fibre, de la myofibrille et du sarcomère",
    "Expliquer le glissement actine-myosine et le rôle de l'ATP dans la contraction",
    "Identifier les voies de régénération de l'ATP selon l'intensité et la durée de l'effort",
    "Résoudre un problème de type BAC en reliant documents, mécanisme et bilan énergétique",
]

ENERGY_SEQUENCE = [
    {"step": 1, "phase": "activation", "action": "Problème et prédictions à partir du dispositif EXAO sur les levures"},
    {"step": 2, "phase": "exploration", "action": "Manipuler ou lire les mesures O2, CO2 et production d'énergie"},
    {"step": 3, "phase": "explanation", "action": "Construire glycolyse, mitochondrie, Krebs et chaîne respiratoire"},
    {"step": 4, "phase": "application", "action": "Comparer fermentation et respiration et calculer les rendements"},
    {"step": 5, "phase": "consolidation", "action": "Résoudre un exercice de type BAC et produire un schéma-bilan"},
]

MUSCLE_SEQUENCE = [
    {"step": 1, "phase": "activation", "action": "Problème : comment le muscle transforme-t-il l'énergie chimique en mouvement ?"},
    {"step": 2, "phase": "exploration", "action": "Observer EMG, myogrammes, chaleur et modifications chimiques"},
    {"step": 3, "phase": "explanation", "action": "Relier organisation du sarcomère, glissement des filaments et ATP"},
    {"step": 4, "phase": "application", "action": "Choisir la filière de régénération de l'ATP selon l'effort"},
    {"step": 5, "phase": "consolidation", "action": "Traiter des documents de type BAC et rédiger une synthèse"},
]


def normalized(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFD", value.lower())
        if unicodedata.category(char) != "Mn"
    )


def should_move_to_muscle(title: str) -> bool:
    value = normalized(title)
    return any(token in value for token in (
        "sarcom", "contraction musculaire", "filieres energetiques",
        "myogram", "thermique de la contraction",
    ))


def resource_rows(energy_id: str, muscle_id: str) -> list[dict]:
    return [
        {
            "lesson_id": energy_id,
            "section_title": "Introduction expérimentale",
            "resource_type": "image",
            "title": "Reconstitution pédagogique — dispositif EXAO levures",
            "description": "Deux montages comparant respiration et fermentation chez les levures. L'élève formule ses prédictions avant l'étude des mesures.",
            "file_path": "/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/introduction/reconstitution_exao_levures.png",
            "trigger_text": "observe le dispositif EXAO levures",
            "phase": "activation",
            "difficulty_tier": "beginner",
            "concepts": ["levures", "O2", "CO2", "respiration", "fermentation"],
            "metadata": {"caption": "Reconstitution pédagogique – illustration générée", "source_type": "ai_generated_reconstruction", "pedagogical_use": "situation_probleme", "evidence_status": "illustration_non_documentaire"},
            "order_index": 0,
        },
        {
            "lesson_id": muscle_id,
            "section_title": "Introduction expérimentale",
            "resource_type": "image",
            "title": "Reconstitution pédagogique — EMG pendant un effort",
            "description": "Montage de physiologie de l'effort avec électrodes de surface et acquisition de données pour lancer le problème énergétique du muscle.",
            "file_path": "/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/introduction/reconstitution_emg_effort.png",
            "trigger_text": "observe le montage EMG effort",
            "phase": "activation",
            "difficulty_tier": "beginner",
            "concepts": ["muscle strié", "EMG", "effort", "énergie"],
            "metadata": {"caption": "Reconstitution pédagogique – illustration générée", "source_type": "ai_generated_reconstruction", "pedagogical_use": "situation_probleme", "evidence_status": "illustration_non_documentaire"},
            "order_index": 0,
        },
        {
            "lesson_id": energy_id,
            "section_title": "Laboratoire d'investigation",
            "resource_type": "simulation",
            "title": "BioLab avancé — respiration et fermentation",
            "description": "Laboratoire visuel avec prédictions, réglages O2-température-glucose, acquisition de courbes, carnet d'essais et exploration de la mitochondrie.",
            "file_path": "/media/simulations/svt/ch1_consommation_matiere_organique/labs/respiration-fermentation/index.html",
            "trigger_text": "ouvre le laboratoire respiration fermentation",
            "phase": "exploration",
            "difficulty_tier": "intermediate",
            "concepts": ["levures", "O2", "CO2", "température", "respiration", "fermentation", "mitochondrie", "ATP"],
            "metadata": {
                "kind": "advanced_virtual_lab", "protocol_version": "2.0",
                "is_primary": True, "llm_readable": True, "llm_controllable": True,
                "interaction_cycle": ["prédire", "manipuler", "mesurer", "comparer", "expliquer"],
                "missions": ["rôle du dioxygène", "effet de la température", "localisation cellulaire"],
                "integrated_generated_visuals": 3, "estimated_minutes": 15,
            },
            "order_index": 1,
        },
        {
            "lesson_id": muscle_id,
            "section_title": "Laboratoire d'investigation",
            "resource_type": "simulation",
            "title": "PhysioLab avancé — muscle et énergie",
            "description": "Laboratoire visuel avec myogrammes calculés, fréquence de stimulation, rôles du Ca2+ et de l'ATP, filières énergétiques et carnet comparatif.",
            "file_path": "/media/simulations/svt/ch1_consommation_matiere_organique/labs/muscle-energie/index.html",
            "trigger_text": "ouvre le laboratoire muscle énergie",
            "phase": "exploration",
            "difficulty_tier": "intermediate",
            "concepts": ["myogramme", "secousse", "sommation", "tétanos", "Ca2+", "actine", "myosine", "ATP", "filières énergétiques"],
            "metadata": {
                "kind": "advanced_virtual_lab", "protocol_version": "2.0",
                "is_primary": True, "llm_readable": True, "llm_controllable": True,
                "interaction_cycle": ["prédire", "stimuler", "enregistrer", "comparer", "expliquer"],
                "missions": ["fréquence et myogramme", "Ca2+ et ponts actine-myosine", "filières de régénération de l'ATP"],
                "integrated_generated_visuals": 3, "estimated_minutes": 15,
            },
            "order_index": 1,
        },
        {
            "lesson_id": muscle_id,
            "section_title": "Structure du muscle",
            "resource_type": "image",
            "title": "Structure du sarcomère",
            "description": "Schéma annoté permettant de relier fibre, myofibrille et sarcomère.",
            "file_path": "/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/schema_sarcomere.svg",
            "trigger_text": "montre structure sarcomere",
            "phase": "explanation",
            "difficulty_tier": "beginner",
            "concepts": ["sarcomère", "actine", "myosine"],
            "metadata": {"caption": "Organisation du sarcomère"},
            "order_index": 20,
        },
        {
            "lesson_id": muscle_id,
            "section_title": "Contraction musculaire",
            "resource_type": "simulation",
            "title": "Animation de la contraction musculaire",
            "description": "Simulation manipulable du glissement actine-myosine et de l'utilisation de l'ATP.",
            "file_path": "/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html",
            "trigger_text": "lance simulation contraction musculaire",
            "phase": "exploration",
            "difficulty_tier": "intermediate",
            "concepts": ["actine", "myosine", "ATP"],
            "metadata": {"interaction_cycle": "prédire-observer-expliquer-vérifier"},
            "order_index": 21,
        },
        {
            "lesson_id": muscle_id,
            "section_title": "Métabolisme énergétique",
            "resource_type": "image",
            "title": "Sources d'énergie musculaire",
            "description": "Schéma comparant phosphocréatine, glycolyse anaérobie et respiration selon l'effort.",
            "file_path": "/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/metabolisme/sources_energie_musculaire.svg",
            "trigger_text": "montre sources energie musculaire",
            "phase": "application",
            "difficulty_tier": "intermediate",
            "concepts": ["phosphocréatine", "glycolyse", "respiration"],
            "metadata": {"caption": "Voies de régénération de l'ATP"},
            "order_index": 22,
        },
        {
            "lesson_id": energy_id,
            "section_title": "Respiration cellulaire",
            "resource_type": "simulation",
            "title": "Mitochondrie 3D à observer",
            "description": "Modèle 3D manipulable : rotation, zoom et mise en évidence des membranes, crêtes et matrice.",
            "file_path": "/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_3d_sans_legendes.png",
            "trigger_text": "observe et manipule mitochondrie 3d",
            "phase": "explanation",
            "difficulty_tier": "beginner",
            "concepts": ["mitochondrie", "crêtes", "matrice"],
            "metadata": {
                "visual_kind": "scientific",
                "scientific": {
                    "engine": "three", "model": "mitochondrion",
                    "title": "Mitochondrie 3D interactive",
                    "description": "Double membrane, crêtes, matrice et ADN mitochondrial circulaire.",
                    "autoplay": True, "labels": True, "focus": "all",
                },
                "caption": "Modèle pédagogique manipulable",
                "source_type": "versioned_scientific_model",
                "interaction": "rotate_zoom_focus",
                "library_status": "published",
            },
            "order_index": 30,
        },
        {
            "lesson_id": energy_id,
            "section_title": "Fermentation",
            "resource_type": "image",
            "title": "Levures : avec ou sans O2",
            "description": "Comparaison visuelle sans texte des produits et du rendement énergétique.",
            "file_path": "/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/fermentation/levures_aerobie_anaerobie.png",
            "trigger_text": "compare levures avec sans oxygene",
            "phase": "explanation",
            "difficulty_tier": "beginner",
            "concepts": ["levures", "respiration", "fermentation", "ATP"],
            "metadata": {"caption": "Reconstitution pédagogique – illustration générée", "source_type": "ai_generated_reconstruction", "interaction": "comparer_deux_conditions"},
            "order_index": 31,
        },
        {
            "lesson_id": energy_id,
            "section_title": "Respiration cellulaire",
            "resource_type": "simulation",
            "title": "Classe les étapes de la respiration",
            "description": "Exercice visuel : placer glycolyse, Krebs et chaîne respiratoire dans l'ordre.",
            "file_path": "/media/simulations/svt/ch1_consommation_matiere_organique/exercices/ordre-respiration/index.html",
            "trigger_text": "exercice visuel ordre respiration",
            "phase": "application",
            "difficulty_tier": "intermediate",
            "concepts": ["glycolyse", "Krebs", "chaîne respiratoire"],
            "metadata": {"kind": "interactive_visual_exercise", "interaction": "click_to_order", "estimated_minutes": 3},
            "order_index": 32,
        },
        {
            "lesson_id": energy_id,
            "section_title": "Introduction expérimentale",
            "resource_type": "simulation",
            "title": "Interprète les courbes EXAO",
            "description": "Exercice visuel : associer les courbes O2/CO2 à la respiration ou à la fermentation.",
            "file_path": "/media/simulations/svt/ch1_consommation_matiere_organique/exercices/lecture-exao/index.html",
            "trigger_text": "exercice interactif courbes exao",
            "phase": "exploration",
            "difficulty_tier": "intermediate",
            "concepts": ["O2", "CO2", "EXAO", "interprétation"],
            "metadata": {"kind": "interactive_visual_exercise", "interaction": "graph_matching", "estimated_minutes": 3},
            "order_index": 33,
        },
        {
            "lesson_id": muscle_id,
            "section_title": "Structure du muscle",
            "resource_type": "image",
            "title": "Du muscle au sarcomère en 3D",
            "description": "Zoom sans légendes du muscle vers le faisceau, la fibre, la myofibrille et le sarcomère.",
            "file_path": "/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/structure/hierarchie_muscle_3d.png",
            "trigger_text": "observe organisation muscle 3d",
            "phase": "explanation",
            "difficulty_tier": "beginner",
            "concepts": ["muscle", "faisceau", "fibre", "myofibrille", "sarcomère"],
            "metadata": {"caption": "Reconstitution pédagogique – illustration générée", "source_type": "ai_generated_reconstruction", "interaction": "nommer_niveaux_organisation"},
            "order_index": 30,
        },
        {
            "lesson_id": muscle_id,
            "section_title": "Contraction musculaire",
            "resource_type": "image",
            "title": "Actine–myosine en 3D",
            "description": "Vue rapprochée sans légendes des filaments et des ponts actine-myosine.",
            "file_path": "/media/images/svt/ch1_consommation_matiere_organique/lesson_2_muscle_strie/contraction/sarcomere_actine_myosine_3d.png",
            "trigger_text": "observe actine myosine 3d",
            "phase": "explanation",
            "difficulty_tier": "intermediate",
            "concepts": ["actine", "myosine", "ponts", "sarcomère"],
            "metadata": {"caption": "Reconstitution pédagogique – illustration générée", "source_type": "ai_generated_reconstruction", "interaction": "identifier_filaments"},
            "order_index": 31,
        },
        {
            "lesson_id": muscle_id,
            "section_title": "Mesure de l'activité musculaire",
            "resource_type": "simulation",
            "title": "Reconnais les myogrammes",
            "description": "Exercice visuel : associer secousse, sommation et tétanos à trois tracés.",
            "file_path": "/media/simulations/svt/ch1_consommation_matiere_organique/exercices/reconnaitre-myogrammes/index.html",
            "trigger_text": "exercice interactif myogrammes",
            "phase": "exploration",
            "difficulty_tier": "intermediate",
            "concepts": ["secousse", "sommation", "tétanos", "myogramme"],
            "metadata": {"kind": "interactive_visual_exercise", "interaction": "curve_matching", "estimated_minutes": 3},
            "order_index": 32,
        },
        {
            "lesson_id": muscle_id,
            "section_title": "Métabolisme énergétique",
            "resource_type": "simulation",
            "title": "Choisis la filière de l'effort",
            "description": "Exercice visuel : relier durée d'effort et voie dominante de régénération de l'ATP.",
            "file_path": "/media/simulations/svt/ch1_consommation_matiere_organique/exercices/filieres-effort/index.html",
            "trigger_text": "exercice interactif filieres effort",
            "phase": "application",
            "difficulty_tier": "intermediate",
            "concepts": ["phosphocréatine", "fermentation lactique", "respiration"],
            "metadata": {"kind": "interactive_visual_exercise", "interaction": "scenario_matching", "estimated_minutes": 3},
            "order_index": 33,
        },
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="écrit les changements dans Supabase")
    args = parser.parse_args()

    db = get_supabase_admin()
    chapters = db.table("chapters").select("id,title_fr").ilike(
        "title_fr", "Consommation de la matière organique%"
    ).execute().data or []
    if not chapters:
        raise RuntimeError("Chapitre SVT introuvable")
    chapter_id = chapters[0]["id"]

    lessons = db.table("lessons").select(
        "id,title_fr,content,learning_objectives,order_index"
    ).eq("chapter_id", chapter_id).order("order_index").execute().data or []
    energy = next((row for row in lessons if normalized(row["title_fr"]).startswith("liberation de l'energie")), None)
    muscle = next((row for row in lessons if normalized(row["title_fr"]).startswith("role du muscle strie")), None)
    if not energy or not muscle:
        raise RuntimeError("Les deux leçons attendues sont introuvables")

    misplaced = db.table("lesson_resources").select("id,title").eq(
        "lesson_id", energy["id"]
    ).execute().data or []
    misplaced = [row for row in misplaced if should_move_to_muscle(row.get("title", ""))]

    planned_resources = resource_rows(energy["id"], muscle["id"])
    missing_resources = []
    for row in planned_resources:
        existing = db.table("lesson_resources").select("id").eq(
            "lesson_id", row["lesson_id"]
        ).eq("file_path", row["file_path"]).execute().data or []
        if not existing:
            missing_resources.append(row)

    print(f"Chapitre: {chapters[0]['title_fr']}")
    print(f"Leçon énergie: {energy['id']} -> {len(ENERGY_OBJECTIVES)} objectifs")
    print(f"Leçon muscle: {muscle['id']} -> {len(MUSCLE_OBJECTIVES)} objectifs")
    print(f"Ressources à déplacer vers le muscle: {len(misplaced)}")
    print(f"Ressources locales à ajouter: {len(missing_resources)}")

    if not args.apply:
        print("Prévisualisation uniquement. Relancer avec --apply pour synchroniser.")
        return 0

    energy_content = dict(energy.get("content") or {})
    energy_content["coaching_sequence"] = ENERGY_SEQUENCE
    muscle_content = dict(muscle.get("content") or {})
    muscle_content["coaching_sequence"] = MUSCLE_SEQUENCE
    db.table("lessons").update({
        "learning_objectives": ENERGY_OBJECTIVES,
        "content": energy_content,
    }).eq("id", energy["id"]).execute()
    db.table("lessons").update({
        "learning_objectives": MUSCLE_OBJECTIVES,
        "content": muscle_content,
    }).eq("id", muscle["id"]).execute()

    for row in misplaced:
        update = {"lesson_id": muscle["id"]}
        value = normalized(row.get("title", ""))
        if "myogram" in value or "thermique de la contraction" in value:
            update.update({"section_title": "Mesure de l'activité musculaire", "phase": "exploration"})
        db.table("lesson_resources").update(update).eq("id", row["id"]).execute()

    if missing_resources:
        db.table("lesson_resources").insert(missing_resources).execute()

    # Keep metadata and pedagogical priority synchronized on repeated runs.
    for row in planned_resources:
        existing = db.table("lesson_resources").select("id").eq(
            "lesson_id", row["lesson_id"]
        ).eq("file_path", row["file_path"]).execute().data or []
        if existing:
            update = {key: value for key, value in row.items() if key != "lesson_id"}
            db.table("lesson_resources").update(update).eq("id", existing[0]["id"]).execute()

    final_energy = db.table("lesson_resources").select("id", count="exact").eq(
        "lesson_id", energy["id"]
    ).execute()
    final_muscle = db.table("lesson_resources").select("id", count="exact").eq(
        "lesson_id", muscle["id"]
    ).execute()
    print(f"Synchronisation terminée: énergie={final_energy.count}, muscle={final_muscle.count} ressources")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
