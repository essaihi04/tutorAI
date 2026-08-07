"""Synchronise les 14 leçons de chimie et leurs laboratoires visuels.

Le mode par défaut est une prévisualisation sans écriture. Utiliser ``--apply``
pour créer/actualiser les leçons et ressources dans Supabase.
"""

from __future__ import annotations

import argparse
import json
import sys
import unicodedata
from pathlib import Path

from dotenv import load_dotenv


BACKEND_DIR = Path(__file__).resolve().parents[1]
PROJECT_DIR = BACKEND_DIR.parent
SPEC_FILE = PROJECT_DIR / "database" / "seed_data" / "chemistry_advanced_lessons.json"

load_dotenv(BACKEND_DIR / ".env")
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.supabase_client import get_supabase_admin  # noqa: E402


def normalized(value: str) -> str:
    return "".join(
        char
        for char in unicodedata.normalize("NFD", (value or "").lower())
        if unicodedata.category(char) != "Mn"
    )


def media_resources(spec: dict) -> list[dict]:
    media = [
        {
            "type": "image",
            "url": spec["image_path"],
            "caption": spec["image_caption"],
            "trigger": f"observe le montage de {spec['focus']}",
        }
    ]
    for mission in spec["missions"]:
        media.append(
            {
                "type": "simulation",
                "url": f"{spec['lab_path']}?mission={mission['id']}",
                "caption": f"Laboratoire manipulable : {mission['title']}.",
                "trigger": mission["trigger"],
            }
        )
    return media


def lesson_content(spec: dict) -> dict:
    mission_ids = [mission["id"] for mission in spec["missions"]]
    return {
        "course_design": "prediction-manipulation-measure-model-bac",
        "guiding_question": spec["guiding_question"],
        "key_formula": spec["formula"],
        "learning_path": [
            {
                "step": 1,
                "student_action": "Observer le montage réel et identifier les grandeurs mesurées.",
                "teacher_move": "Faire décrire avant de donner le modèle.",
            },
            {
                "step": 2,
                "student_action": "Choisir une prédiction avant de lancer l'expérience.",
                "teacher_move": "Demander une justification courte fondée sur une grandeur.",
            },
            {
                "step": 3,
                "student_action": "Modifier une seule variable et enregistrer au moins deux essais.",
                "teacher_move": "Contrôler les autres paramètres et faire comparer les mesures.",
            },
            {
                "step": 4,
                "student_action": f"Expliquer les résultats avec {spec['formula']}.",
                "teacher_move": "Relier la courbe, la mesure numérique et le modèle.",
            },
            {
                "step": 5,
                "student_action": "Résoudre une question type Bac en citant mesure, loi et conclusion.",
                "teacher_move": f"Méthode : {spec['bac_method']}",
            },
        ],
        "micro_enseignements": [
            {"id": f"chem_ch{spec['chapter_number']}_observe", "title": "1. J'observe le dispositif", "type": "observation"},
            {"id": f"chem_ch{spec['chapter_number']}_predict", "title": "2. Je prédis", "type": "hypothesis"},
            {"id": f"chem_ch{spec['chapter_number']}_measure", "title": "3. Je manipule et mesure", "type": "simulation", "missions": mission_ids},
            {"id": f"chem_ch{spec['chapter_number']}_model", "title": "4. Je modélise", "type": "reasoning"},
            {"id": f"chem_ch{spec['chapter_number']}_bac", "title": "5. J'applique au Bac", "type": "application"},
        ],
        "phases": {
            "activation": {"duration_minutes": 8, "focus": "observer et prédire"},
            "exploration": {"duration_minutes": 30, "focus": "manipuler un paramètre à la fois"},
            "explanation": {"duration_minutes": 22, "focus": "relier mesures et modèle"},
            "application": {"duration_minutes": 25, "focus": "raisonnement type Bac"},
            "consolidation": {"duration_minutes": 10, "focus": "expliquer sans la simulation"},
        },
        "interactive_exercises": [
            {
                "id": f"chem_ch{spec['chapter_number']}_virtual_lab",
                "type": "advanced_virtual_lab",
                "missions": mission_ids,
                "instruction": "Prédire, effectuer deux essais contrôlés, comparer les mesures et conclure.",
                "llm_reads": [
                    "variables",
                    "measurements",
                    "student_prediction",
                    "trial_history",
                    "scientific_observation",
                ],
            }
        ],
        "misconceptions": [
            {
                "error": spec["misconception"],
                "remediation": "Créer deux essais qui isolent la variable en cause puis confronter la prédiction aux mesures.",
            }
        ],
        "differentiation": {
            "support": "Utiliser les valeurs initiales et verbaliser le sens de variation.",
            "standard": "Comparer deux essais en contrôlant les autres variables.",
            "challenge": "Justifier quantitativement avec la formule et discuter les limites du modèle.",
        },
        "bac_method": spec["bac_method"],
        "exit_ticket": [
            f"Explique le rôle de {spec['focus']} en une phrase.",
            f"Interprète la relation : {spec['formula']}.",
            "Cite une mesure de la simulation qui soutient ta conclusion.",
        ],
    }


def lesson_payload(spec: dict) -> dict:
    return {
        "title_fr": spec["title_fr"],
        "title_ar": spec["title_ar"],
        "lesson_type": "theory",
        "duration_minutes": 95,
        "order_index": 1,
        "learning_objectives": spec["objectives"],
        "content": lesson_content(spec),
        "media_resources": media_resources(spec),
    }


def resource_rows(lesson_id: str, spec: dict) -> list[dict]:
    rows = []
    lab_id = Path(spec["lab_path"]).parent.name
    for index, item in enumerate(media_resources(spec), start=1):
        simulation = item["type"] == "simulation"
        mission_id = item["url"].split("?mission=", 1)[1] if simulation else None
        metadata = {
            "caption": item["caption"],
            "visual": True,
            "source_type": "interactive_scientific_lab" if simulation else "ai_generated_lab_scene",
            "subject": "Chimie 2e BAC",
            "chapter_number": spec["chapter_number"],
        }
        if simulation:
            metadata.update(
                {
                    "simulation_id": f"chimie-{lab_id}-2bac",
                    "simulation_version": "2.0",
                    "mission_id": mission_id,
                    "llm_readable_state": True,
                    "llm_controllable": True,
                    "state_contract": [
                        "variables",
                        "measurements",
                        "student_prediction",
                        "mission_coverage",
                        "trial_history",
                        "scientific_observation",
                        "model_limits",
                    ],
                    "commands": [
                        "start",
                        "reset",
                        "set_variant",
                        "set_parameters",
                        "run_trial",
                        "highlight",
                        "get_state",
                        "set_prediction",
                    ],
                    "viewport": "responsive",
                }
            )
        rows.append(
            {
                "lesson_id": lesson_id,
                "section_title": spec["title_fr"][:200],
                "resource_type": item["type"],
                "title": item["caption"][:200],
                "description": item["caption"],
                "file_path": item["url"],
                "trigger_text": item["trigger"][:200],
                "phase": "exploration" if simulation else "activation",
                "difficulty_tier": "advanced" if simulation else "intermediate",
                "concepts": ["chimie 2e BAC", spec["focus"]],
                "metadata": metadata,
                "order_index": index,
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="écrit les changements dans Supabase")
    args = parser.parse_args()

    specs = json.loads(SPEC_FILE.read_text(encoding="utf-8"))
    if len(specs) != 14 or {item["chapter_number"] for item in specs} != set(range(1, 15)):
        raise RuntimeError("Le fichier de programme doit contenir exactement les chapitres 1 à 14")

    db = get_supabase_admin()
    subjects = db.table("subjects").select("id,name_fr").execute().data or []
    subject = next((row for row in subjects if "chimi" in normalized(row.get("name_fr", ""))), None)
    if not subject:
        raise RuntimeError("Matière Chimie introuvable")
    chapters = (
        db.table("chapters")
        .select("id,chapter_number,title_fr")
        .eq("subject_id", subject["id"])
        .order("chapter_number")
        .execute()
        .data
        or []
    )
    by_number = {row["chapter_number"]: row for row in chapters}
    missing_chapters = sorted(set(range(1, 15)) - set(by_number))
    if missing_chapters:
        raise RuntimeError(f"Chapitres distants absents : {missing_chapters}")

    plan = []
    lesson_creates = resource_creates = resource_updates = 0
    for spec in specs:
        chapter = by_number[spec["chapter_number"]]
        lessons = (
            db.table("lessons")
            .select("id,title_fr,order_index")
            .eq("chapter_id", chapter["id"])
            .order("order_index")
            .execute()
            .data
            or []
        )
        lesson = lessons[0] if lessons else None
        if not lesson:
            lesson_creates += 1
        missing_resources, updates = [], []
        if lesson:
            for row in resource_rows(lesson["id"], spec):
                found = (
                    db.table("lesson_resources")
                    .select("id")
                    .eq("lesson_id", lesson["id"])
                    .eq("file_path", row["file_path"])
                    .execute()
                    .data
                    or []
                )
                if found:
                    updates.append((found[0]["id"], row))
                else:
                    missing_resources.append(row)
        else:
            missing_resources = resource_rows("pending", spec)
        resource_creates += len(missing_resources)
        resource_updates += len(updates)
        plan.append((spec, chapter, lesson, missing_resources, updates))
        print(
            f"Ch. {spec['chapter_number']:>2} · {spec['focus']}: "
            f"{'création' if lesson is None else 'actualisation'} leçon, "
            f"{len(missing_resources)} ressource(s) à ajouter, {len(updates)} à actualiser"
        )

    if not args.apply:
        print(
            f"Prévisualisation : {lesson_creates} leçon(s) à créer, "
            f"{14 - lesson_creates} à actualiser, {resource_creates} ressource(s) à ajouter, "
            f"{resource_updates} à actualiser. Relancer avec --apply."
        )
        return 0

    for spec, chapter, lesson, _, _ in plan:
        payload = lesson_payload(spec)
        if lesson:
            db.table("lessons").update(payload).eq("id", lesson["id"]).execute()
            lesson_id = lesson["id"]
        else:
            created = db.table("lessons").insert({"chapter_id": chapter["id"], **payload}).execute().data or []
            if not created:
                raise RuntimeError(f"Échec de création de la leçon du chapitre {spec['chapter_number']}")
            lesson_id = created[0]["id"]

        for row in resource_rows(lesson_id, spec):
            found = (
                db.table("lesson_resources")
                .select("id")
                .eq("lesson_id", lesson_id)
                .eq("file_path", row["file_path"])
                .execute()
                .data
                or []
            )
            if found:
                update_data = {key: value for key, value in row.items() if key != "lesson_id"}
                db.table("lesson_resources").update(update_data).eq("id", found[0]["id"]).execute()
            else:
                db.table("lesson_resources").insert(row).execute()

    final_lessons = 0
    final_resources = 0
    for chapter in chapters:
        lesson_rows = db.table("lessons").select("id").eq("chapter_id", chapter["id"]).execute().data or []
        final_lessons += len(lesson_rows)
        for lesson in lesson_rows:
            response = db.table("lesson_resources").select("id", count="exact").eq("lesson_id", lesson["id"]).execute()
            final_resources += response.count or 0
    print(f"Synchronisation terminée : {final_lessons} leçon(s) de chimie, {final_resources} ressource(s) liées.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
