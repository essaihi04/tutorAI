"""Synchronise la leçon SVT sur la pollution avec les laboratoires avancés.

Sans ``--apply``, le script affiche uniquement les changements prévus.
La migration ``20260806_enrich_svt_ch3_pollution.sql`` reste la source de
vérité copiable dans l'éditeur SQL de Supabase.
"""

from __future__ import annotations

import argparse
import sys
import unicodedata
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BACKEND_DIR / ".env")
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.supabase_client import get_supabase_admin  # noqa: E402


OBJECTIVES = [
    "Identifier les sources, les polluants et les milieux récepteurs à partir de documents",
    "Expliquer la chaîne causale nutriments → prolifération algale → décomposition → hypoxie",
    "Distinguer bioaccumulation et biomagnification dans un réseau trophique",
    "Relier émissions, vent et inversion thermique à la dispersion du smog",
    "Expliquer la formation des dépôts acides et leurs effets sur les écosystèmes",
    "Comparer des stratégies de prévention, de traitement et de restauration à partir d'indicateurs",
]

CONTENT = {
    "guiding_question": "Comment une activité humaine perturbe-t-elle un milieu, et comment démontrer qu'une solution le restaure ?",
    "micro_enseignements": [
        {"id": "svt_ch3_pollution_diagnostic", "title": "1. Diagnostiquer : source → polluant → milieu → indicateur", "type": "activation"},
        {"id": "svt_ch3_pollution_eutrophisation", "title": "2. Enquêter : nutriments, algues et manque de O₂", "type": "exploration"},
        {"id": "svt_ch3_pollution_reseau", "title": "3. Suivre un polluant dans le réseau trophique", "type": "exploration"},
        {"id": "svt_ch3_pollution_air", "title": "4. Modéliser : émissions, météo et smog", "type": "exploration"},
        {"id": "svt_ch3_pollution_acide", "title": "5. Relier les émissions aux dépôts acides", "type": "explanation"},
        {"id": "svt_ch3_pollution_solutions", "title": "6. Décider : prévention, traitement et restauration", "type": "application"},
        {"id": "svt_ch3_pollution_bac", "title": "7. Argumenter comme au BAC avec des indicateurs", "type": "consolidation"},
    ],
    "prerequisites": [
        "Lire une courbe et comparer un témoin à un essai",
        "Connaître respiration, photosynthèse et réseau trophique",
        "Utiliser le pH et une concentration comme indicateurs",
    ],
    "sections": [
        {"title": "Pollution des eaux", "content": "Les apports excessifs en nitrates et phosphates favorisent les algues. Leur décomposition augmente la demande biologique en O₂ et peut conduire à l'hypoxie.", "type": "modele_causal"},
        {"title": "Polluants persistants", "content": "Un polluant peut s'accumuler dans un organisme et atteindre des concentrations croissantes aux niveaux trophiques supérieurs.", "type": "modele_causal"},
        {"title": "Pollution atmosphérique", "content": "La concentration au sol dépend des émissions, du vent et de la stabilité de l'atmosphère.", "type": "modele_causal"},
        {"title": "Dépôts acides", "content": "SO₂ et NOₓ peuvent former des acides, être transportés puis déposés. Les effets dépendent aussi du pouvoir tampon du milieu.", "type": "modele_causal"},
        {"title": "Solutions", "content": "Réduire à la source, intercepter les flux et restaurer le milieu sont des actions complémentaires dont l'efficacité se mesure.", "type": "decision"},
    ],
    "phases": {
        "activation": {"duration_minutes": 10, "focus": ["photographies-problèmes", "hypothèses"]},
        "exploration": {"duration_minutes": 45, "focus": ["AquaLab", "AtmosLab", "essais contrôlés"]},
        "explanation": {"duration_minutes": 25, "focus": ["chaînes causales", "indicateurs", "limites des modèles"]},
        "application": {"duration_minutes": 20, "focus": ["stratégies multi-barrières", "comparaison avant-après"]},
        "consolidation": {"duration_minutes": 10, "focus": ["argumentation type BAC", "ticket de sortie"]},
    },
    "investigation_cycle": ["observer", "prédire", "manipuler une variable", "mesurer", "comparer au témoin", "expliquer", "proposer une solution"],
    "misconceptions": [
        {"error": "Les algues produisent O₂, donc un bloom augmente toujours O₂.", "remediation": "La respiration nocturne et surtout la décomposition de la biomasse consomment O₂ et peuvent provoquer l'hypoxie."},
        {"error": "Une faible concentration dans l'eau signifie aucun risque.", "remediation": "Un polluant persistant peut se concentrer dans les organismes puis le long du réseau trophique."},
        {"error": "Le vent supprime la pollution.", "remediation": "Il dilue localement mais transporte aussi le panache vers d'autres zones."},
        {"error": "Planter des arbres suffit à éliminer toutes les sources.", "remediation": "La végétation réduit surtout l'exposition locale ; la priorité reste la réduction des émissions et des rejets."},
    ],
    "bac_method": ["nommer l'indicateur", "décrire la variation chiffrée", "relier cause et mécanisme", "conclure sans dépasser les données"],
    "exit_ticket": [
        "Reconstitue en quatre étapes le mécanisme de l'eutrophisation.",
        "Explique pourquoi un prédateur supérieur peut être le plus contaminé.",
        "Propose deux actions complémentaires et l'indicateur qui vérifiera leur efficacité.",
    ],
}

MEDIA = [
    {"type": "image", "url": "/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/assets/reservoir-bloom.webp", "caption": "Réservoir marocain : zone claire et prolifération algale.", "trigger": "observe le réservoir et formule une hypothèse"},
    {"type": "simulation", "url": "/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/index.html", "caption": "AquaLab : eutrophisation, biomagnification et restauration.", "trigger": "ouvre le laboratoire pollution de l'eau"},
    {"type": "image", "url": "/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/assets/food-web.webp", "caption": "Réseau trophique aquatique pour suivre un polluant persistant.", "trigger": "observe le réseau trophique aquatique"},
    {"type": "image", "url": "/media/simulations/svt/ch3_pollution/labs/aqua-ecosysteme/assets/restoration.webp", "caption": "Traitement, zone humide et bande végétalisée.", "trigger": "compare les dispositifs de dépollution"},
    {"type": "image", "url": "/media/simulations/svt/ch3_pollution/labs/air-dispersion/assets/urban-smog.webp", "caption": "Ville marocaine sous une couche de smog.", "trigger": "observe le smog urbain et ses sources"},
    {"type": "simulation", "url": "/media/simulations/svt/ch3_pollution/labs/air-dispersion/index.html", "caption": "AtmosLab : dispersion, dépôts acides et solutions.", "trigger": "ouvre le laboratoire pollution de l'air"},
    {"type": "image", "url": "/media/simulations/svt/ch3_pollution/labs/air-dispersion/assets/acid-rain.webp", "caption": "Du panache industriel au lac soumis aux dépôts acides.", "trigger": "observe le trajet des dépôts acides"},
    {"type": "image", "url": "/media/simulations/svt/ch3_pollution/labs/air-dispersion/assets/clean-air-transition.webp", "caption": "Transport collectif, filtration et énergies renouvelables.", "trigger": "compare les solutions pour la qualité de l'air"},
]


def normalized(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFD", (value or "").lower())
        if unicodedata.category(char) != "Mn"
    )


def resource_rows(lesson_id: str) -> list[dict]:
    specs = [
        ("Situation-problème", "image", "Réservoir : du clair au bloom algal", "Observer une prolifération algale et repérer les sources possibles avant toute explication.", MEDIA[0], "activation", "beginner", ["eutrophisation", "nutriments", "réservoir"], {"caption": "Reconstitution pédagogique générée — sans valeur documentaire locale", "source_type": "ai_generated_educational_reconstruction", "visual": True}),
        ("Laboratoire d'investigation", "simulation", "AquaLab avancé — pollution de l'eau", "Trois missions avec prédictions, courbes algues-O₂, réseau trophique, solutions et carnet comparatif.", MEDIA[1], "exploration", "intermediate", ["eutrophisation", "O2 dissous", "DBO", "biomagnification", "restauration"], {"kind": "advanced_virtual_lab", "protocol_version": "2.0", "simulation_id": "svt_ch3_aqualab_pollution_v2", "is_primary": True, "llm_readable": True, "llm_controllable": True, "variants": ["eutrophication", "biomagnification", "remediation"], "interaction_cycle": ["prédire", "manipuler", "mesurer", "comparer", "expliquer"], "integrated_generated_visuals": 3, "estimated_minutes": 18, "viewport": "responsive_no_external_dependency"}),
        ("Réseau trophique", "image", "Polluant persistant dans le réseau aquatique", "Identifier les niveaux trophiques avant de suivre la concentration du polluant.", MEDIA[2], "explanation", "intermediate", ["plancton", "poisson", "prédateur", "bioaccumulation", "biomagnification"], {"caption": "Reconstitution pédagogique générée", "source_type": "ai_generated_educational_reconstruction", "visual": True}),
        ("Solutions pour l'eau", "image", "Restauration multi-barrières d'un réservoir", "Comparer bande végétalisée, zone humide construite et station de traitement.", MEDIA[3], "application", "intermediate", ["prévention", "traitement", "zone humide", "restauration"], {"caption": "Reconstitution pédagogique générée", "source_type": "ai_generated_educational_reconstruction", "visual": True}),
        ("Situation-problème", "image", "Smog au-dessus d'une ville marocaine", "Repérer trafic, industrie, station de mesure et couche de smog.", MEDIA[4], "activation", "beginner", ["smog", "trafic", "industrie", "PM2.5"], {"caption": "Reconstitution pédagogique générée — sans valeur documentaire locale", "source_type": "ai_generated_educational_reconstruction", "visual": True}),
        ("Laboratoire d'investigation", "simulation", "AtmosLab avancé — pollution de l'air", "Trois missions sur dispersion du smog, dépôts acides et stratégie de réduction multi-actions.", MEDIA[5], "exploration", "intermediate", ["dispersion", "vent", "inversion thermique", "SO2", "NOx", "pluie acide", "PM2.5"], {"kind": "advanced_virtual_lab", "protocol_version": "2.0", "simulation_id": "svt_ch3_atmoslab_pollution_v2", "is_primary": True, "llm_readable": True, "llm_controllable": True, "variants": ["dispersion", "acid_rain", "solutions"], "interaction_cycle": ["prédire", "manipuler", "modéliser", "comparer", "argumenter"], "integrated_generated_visuals": 3, "estimated_minutes": 18, "viewport": "responsive_no_external_dependency"}),
        ("Dépôts acides", "image", "Du panache industriel au lac acidifié", "Faire décrire transport atmosphérique, dépôt, pH et sensibilité de l'écosystème.", MEDIA[6], "explanation", "intermediate", ["SO2", "NOx", "pH", "dépôt acide", "pouvoir tampon"], {"caption": "Reconstitution pédagogique générée", "source_type": "ai_generated_educational_reconstruction", "visual": True}),
        ("Solutions pour l'air", "image", "Ville en transition vers un air plus propre", "Comparer transport collectif, filtration industrielle, renouvelables et ceinture verte.", MEDIA[7], "application", "intermediate", ["transport collectif", "filtration", "énergies renouvelables", "exposition"], {"caption": "Reconstitution pédagogique générée", "source_type": "ai_generated_educational_reconstruction", "visual": True}),
    ]
    return [
        {
            "lesson_id": lesson_id,
            "section_title": section,
            "resource_type": kind,
            "title": title,
            "description": description,
            "file_path": media["url"],
            "trigger_text": media["trigger"],
            "phase": phase,
            "difficulty_tier": difficulty,
            "concepts": concepts,
            "metadata": metadata,
            "order_index": index,
        }
        for index, (section, kind, title, description, media, phase, difficulty, concepts, metadata) in enumerate(specs)
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="écrit les changements dans Supabase")
    args = parser.parse_args()

    db = get_supabase_admin()
    chapters = db.table("chapters").select("id,chapter_number,title_fr").eq("chapter_number", 3).execute().data or []
    chapter = next((row for row in chapters if "organique" in normalized(row.get("title_fr", ""))), None)
    if not chapter:
        raise RuntimeError("Chapitre 3 de SVT introuvable")

    lessons = db.table("lessons").select("id,title_fr,order_index").eq("chapter_id", chapter["id"]).order("order_index").execute().data or []
    lesson = next((row for row in lessons if "pollution" in normalized(row.get("title_fr", ""))), None)
    if not lesson:
        raise RuntimeError("Leçon « La pollution des milieux naturels » introuvable")

    rows = resource_rows(lesson["id"])
    missing: list[dict] = []
    updates: list[tuple[str, dict]] = []
    for row in rows:
        existing = db.table("lesson_resources").select("id").eq("lesson_id", lesson["id"]).eq("file_path", row["file_path"]).execute().data or []
        (updates if existing else missing).append((existing[0]["id"], row) if existing else row)

    print(f"Chapitre : {chapter['title_fr']}")
    print(f"Leçon : {lesson['title_fr']} ({lesson['id']})")
    print(f"Objectifs : {len(OBJECTIVES)}")
    print(f"Ressources à ajouter : {len(missing)}")
    print(f"Ressources à actualiser : {len(updates)}")
    if not args.apply:
        print("Prévisualisation uniquement. Relancer avec --apply pour synchroniser.")
        return 0

    db.table("lessons").update({"duration_minutes": 110, "learning_objectives": OBJECTIVES, "content": CONTENT, "media_resources": MEDIA}).eq("id", lesson["id"]).execute()
    if missing:
        db.table("lesson_resources").insert(missing).execute()
    for resource_id, row in updates:
        db.table("lesson_resources").update({key: value for key, value in row.items() if key != "lesson_id"}).eq("id", resource_id).execute()

    final = db.table("lesson_resources").select("id", count="exact").eq("lesson_id", lesson["id"]).execute()
    print(f"Synchronisation terminée : {final.count} ressources liées à la leçon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
