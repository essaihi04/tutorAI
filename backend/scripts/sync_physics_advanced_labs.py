"""Synchronise le programme visuel de Physique 2e BAC PC BIOF.

Sans --apply, affiche une prévisualisation sans écriture. Le script met à
jour les 15 chapitres, crée ou actualise leur leçon guidée et les ressources.
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
SEED_DIR = PROJECT_DIR / "database" / "seed_data"
CHAPTER_FILE = SEED_DIR / "physics_chapters.json"
LESSON_DIR = SEED_DIR / "lessons"

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


def load_program() -> tuple[list[dict], dict[int, dict]]:
    chapters = json.loads(CHAPTER_FILE.read_text(encoding="utf-8"))
    lessons = {
        number: json.loads((LESSON_DIR / f"phys_ch{number}_l1.json").read_text(encoding="utf-8"))
        for number in range(1, 16)
    }
    numbers = {item["chapter_number"] for item in chapters}
    if len(chapters) != 15 or numbers != set(range(1, 16)):
        raise RuntimeError("Le programme local doit contenir exactement les chapitres 1 à 15")
    return chapters, lessons


def resource_rows(lesson_id: str, chapter: dict, lesson: dict) -> list[dict]:
    rows: list[dict] = []
    for index, item in enumerate(lesson["media_resources"], start=1):
        simulation = item["type"] == "simulation"
        metadata = dict(item.get("metadata") or {})
        metadata.update(
            {
                "caption": item["caption"],
                "visual": True,
                "subject": "Physique 2e BAC PC BIOF",
                "chapter_number": chapter["chapter_number"],
                "source_type": (
                    "interactive_scientific_lab"
                    if simulation
                    else "ai_generated_scientific_lab"
                ),
            }
        )
        if simulation:
            metadata.update(
                {
                    "llm_readable_state": True,
                    "llm_controllable": True,
                    "state_contract": [
                        "parameters",
                        "derived_values",
                        "measurements",
                        "student_actions",
                        "attempts",
                        "hints_used",
                        "completed_variants",
                        "objective_progress",
                    ],
                    "commands": [
                        "start",
                        "set_variant",
                        "set_parameters",
                        "run_model",
                        "record_measurement",
                        "check",
                        "reset",
                        "reveal_hint",
                        "highlight",
                    ],
                    "viewport": "native_100vh_no_scroll",
                }
            )
        rows.append(
            {
                "lesson_id": lesson_id,
                "section_title": lesson["title_fr"][:200],
                "resource_type": item["type"],
                "title": item["caption"][:200],
                "description": item["caption"],
                "file_path": item["url"],
                "trigger_text": (item.get("trigger") or "")[:200],
                "phase": item.get("phase") or ("exploration" if simulation else "activation"),
                "difficulty_tier": "advanced" if simulation else "intermediate",
                "concepts": ["physique 2e BAC", chapter["title_fr"]],
                "metadata": metadata,
                "order_index": index,
            }
        )
    return rows


def chapter_payload(chapter: dict) -> dict:
    return {
        "title_fr": chapter["title_fr"],
        "title_ar": chapter["title_ar"],
        "description_fr": chapter["description_fr"],
        "description_ar": chapter.get("description_ar"),
        "difficulty_level": chapter["difficulty_level"],
        "estimated_hours": chapter["estimated_hours"],
        "order_index": chapter["order_index"],
    }


def lesson_payload(lesson: dict) -> dict:
    return {
        "title_fr": lesson["title_fr"],
        "title_ar": lesson["title_ar"],
        "lesson_type": lesson["lesson_type"],
        "duration_minutes": lesson["duration_minutes"],
        "order_index": lesson["order_index"],
        "learning_objectives": lesson["learning_objectives"],
        "content": lesson["content"],
        "media_resources": lesson["media_resources"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="écrit les changements dans Supabase")
    args = parser.parse_args()
    chapter_specs, lesson_specs = load_program()

    db = get_supabase_admin()
    subjects = db.table("subjects").select("id,name_fr").execute().data or []
    subject = next(
        (
            row
            for row in subjects
            if normalized(row.get("name_fr", "")).strip() == "physique"
        ),
        None,
    )
    if not subject:
        raise RuntimeError("Matière Physique introuvable")

    remote_chapters = (
        db.table("chapters")
        .select("id,chapter_number,title_fr")
        .eq("subject_id", subject["id"])
        .order("chapter_number")
        .execute()
        .data
        or []
    )
    by_number = {row["chapter_number"]: row for row in remote_chapters}
    missing = sorted(set(range(1, 16)) - set(by_number))
    if missing:
        raise RuntimeError(f"Chapitres distants absents : {missing}")

    plan = []
    lesson_creates = resource_creates = resource_updates = 0
    for chapter in chapter_specs:
        number = chapter["chapter_number"]
        remote = by_number[number]
        lessons = (
            db.table("lessons")
            .select("id,title_fr,order_index")
            .eq("chapter_id", remote["id"])
            .order("order_index")
            .execute()
            .data
            or []
        )
        lesson = lessons[0] if lessons else None
        if lesson is None:
            lesson_creates += 1

        rows = resource_rows(lesson["id"] if lesson else "pending", chapter, lesson_specs[number])
        missing_rows: list[dict] = []
        update_rows: list[tuple[str, dict]] = []
        if lesson:
            for row in rows:
                found = (
                    db.table("lesson_resources")
                    .select("id")
                    .eq("lesson_id", lesson["id"])
                    .eq("file_path", row["file_path"])
                    .execute()
                    .data
                    or []
                )
                if not found and "/index.html?variant=" in row["file_path"]:
                    legacy_path = row["file_path"].replace(
                        "/index.html?variant=", "/?variant="
                    )
                    found = (
                        db.table("lesson_resources")
                        .select("id")
                        .eq("lesson_id", lesson["id"])
                        .eq("file_path", legacy_path)
                        .execute()
                        .data
                        or []
                    )
                if found:
                    update_rows.append((found[0]["id"], row))
                else:
                    missing_rows.append(row)
        else:
            missing_rows = rows

        resource_creates += len(missing_rows)
        resource_updates += len(update_rows)
        plan.append((chapter, remote, lesson, missing_rows, update_rows))
        print(
            f"Ch. {number:>2} · {chapter['title_fr']}: "
            f"{'création' if lesson is None else 'actualisation'} leçon, "
            f"{len(missing_rows)} ressource(s) à ajouter, {len(update_rows)} à actualiser"
        )

    if not args.apply:
        print(
            f"Prévisualisation : 15 chapitre(s) à actualiser, "
            f"{lesson_creates} leçon(s) à créer, {15 - lesson_creates} à actualiser, "
            f"{resource_creates} ressource(s) à ajouter, {resource_updates} à actualiser. "
            "Relancer avec --apply."
        )
        return 0

    for chapter, remote, lesson, _, _ in plan:
        number = chapter["chapter_number"]
        db.table("chapters").update(chapter_payload(chapter)).eq("id", remote["id"]).execute()

        payload = lesson_payload(lesson_specs[number])
        if lesson:
            db.table("lessons").update(payload).eq("id", lesson["id"]).execute()
            lesson_id = lesson["id"]
        else:
            created = (
                db.table("lessons")
                .insert({"chapter_id": remote["id"], **payload})
                .execute()
                .data
                or []
            )
            if not created:
                raise RuntimeError(f"Échec de création de la leçon du chapitre {number}")
            lesson_id = created[0]["id"]

        for row in resource_rows(lesson_id, chapter, lesson_specs[number]):
            found = (
                db.table("lesson_resources")
                .select("id")
                .eq("lesson_id", lesson_id)
                .eq("file_path", row["file_path"])
                .execute()
                .data
                or []
            )
            if not found and "/index.html?variant=" in row["file_path"]:
                legacy_path = row["file_path"].replace(
                    "/index.html?variant=", "/?variant="
                )
                found = (
                    db.table("lesson_resources")
                    .select("id")
                    .eq("lesson_id", lesson_id)
                    .eq("file_path", legacy_path)
                    .execute()
                    .data
                    or []
                )
            if found:
                update_data = {key: value for key, value in row.items() if key != "lesson_id"}
                db.table("lesson_resources").update(update_data).eq("id", found[0]["id"]).execute()
            else:
                db.table("lesson_resources").insert(row).execute()

    final_lessons = final_resources = 0
    for chapter in by_number.values():
        lesson_rows = (
            db.table("lessons").select("id").eq("chapter_id", chapter["id"]).execute().data or []
        )
        final_lessons += len(lesson_rows)
        for item in lesson_rows:
            response = (
                db.table("lesson_resources")
                .select("id", count="exact")
                .eq("lesson_id", item["id"])
                .execute()
            )
            final_resources += response.count or 0

    print(
        f"Synchronisation terminée : {final_lessons} leçon(s) de physique, "
        f"{final_resources} ressource(s) liées."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
