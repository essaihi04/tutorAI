"""Synchronise les manifests versionnés vers les tables du lecteur de cours.

Usage, depuis ``backend``::

    python -m scripts.sync_course_decks

La synchronisation laisse les decks en brouillon. La publication est effectuée
par ``generate_course_audio.py verify`` après contrôle humain de tous les sons.
"""
from __future__ import annotations

import json
import hashlib
import sys
import unicodedata
from pathlib import Path


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.supabase_client import get_supabase_admin  # noqa: E402


COURSE_DIR = BACKEND_ROOT / "data" / "courses"
MANIFESTS = sorted(COURSE_DIR.glob("*_course_v1.json"))


def normalise(value: str) -> str:
    text = unicodedata.normalize("NFD", (value or "").casefold())
    return "".join(char for char in text if unicodedata.category(char) != "Mn")


def matching_lesson(admin, manifest: dict) -> dict:
    lessons = admin.table("lessons").select("id,title_fr").execute().data or []
    tokens = [normalise(token) for token in manifest.get("lesson_match") or []]
    for lesson in lessons:
        title = normalise(lesson.get("title_fr") or "")
        if any(token in title for token in tokens):
            return lesson
    raise RuntimeError(f"Leçon introuvable pour {manifest['title']!r}")


def sync_manifest(admin, manifest_path: Path) -> tuple[int, int]:
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    lesson = matching_lesson(admin, manifest)
    version = int(manifest.get("version") or 1)
    manifest_hash = hashlib.sha256(manifest_path.read_bytes()).hexdigest()
    existing = admin.table("course_decks").select("id,status,metadata").eq(
        "lesson_id", lesson["id"]
    ).eq("version", version).limit(1).execute().data or []
    previous_hash = ((existing[0].get("metadata") or {}).get("manifest_hash") if existing else None)
    deck_status = existing[0].get("status") if existing and previous_hash == manifest_hash else "draft"
    deck_data = {
        "lesson_id": lesson["id"],
        "version": version,
        "title": manifest["title"],
        "status": deck_status,
        "language": manifest.get("language") or "fr",
        "estimated_minutes": int(manifest.get("estimated_minutes") or 50),
        "metadata": {
            "stable_id": manifest.get("stable_id") or manifest["id"],
            "manifest": manifest_path.name,
            "manifest_hash": manifest_hash,
            "catalog": manifest.get("catalog") or {},
            "lesson_match": manifest.get("lesson_match") or [],
            "intent_aliases": manifest.get("intent_aliases") or [],
            "pedagogy": "investigation-explicitation-retrieval-practice",
        },
    }
    deck_rows = admin.table("course_decks").upsert(
        deck_data, on_conflict="lesson_id,version"
    ).execute().data or []
    deck_id = deck_rows[0]["id"] if deck_rows else existing[0]["id"]

    # Libérer temporairement les index uniques avant un éventuel réordonnancement.
    # Les lignes gardent leur UUID : un speech inchangé peut donc réutiliser son
    # audio déjà généré et vérifié.
    existing_activities = admin.table("course_activities").select(
        "id,stable_id,order_index"
    ).eq("deck_id", deck_id).execute().data or []
    for offset, row in enumerate(existing_activities):
        admin.table("course_activities").update({
            "order_index": 100_000 + offset,
        }).eq("id", row["id"]).execute()
    manifest_activity_ids = {
        activity.get("stable_id") or activity["id"]
        for activity in manifest.get("activities") or []
    }

    activity_count = 0
    slide_count = 0
    for activity_index, activity in enumerate(manifest.get("activities") or []):
        activity_data = {
            "deck_id": deck_id,
            "stable_id": activity.get("stable_id") or activity["id"],
            "title": activity["title"],
            "phase": activity.get("phase") or "explanation",
            "duration_minutes": int(activity.get("duration_minutes") or 15),
            "objective_ids": activity.get("objective_ids") or [],
            "order_index": activity_index,
            "metadata": {"manifest_id": activity["id"]},
        }
        activity_rows = admin.table("course_activities").upsert(
            activity_data, on_conflict="deck_id,stable_id"
        ).execute().data or []
        if activity_rows:
            activity_id = activity_rows[0]["id"]
        else:
            activity_id = admin.table("course_activities").select("id").eq(
                "deck_id", deck_id
            ).eq("stable_id", activity_data["stable_id"]).limit(1).execute().data[0]["id"]
        activity_count += 1

        existing_slides = admin.table("course_slides").select(
            "id,stable_id,order_index"
        ).eq("activity_id", activity_id).execute().data or []
        for offset, row in enumerate(existing_slides):
            admin.table("course_slides").update({
                "order_index": 100_000 + offset,
            }).eq("id", row["id"]).execute()
        manifest_slide_ids = {
            slide.get("stable_id") or slide["id"]
            for slide in activity.get("slides") or []
        }

        for slide_index, slide in enumerate(activity.get("slides") or []):
            admin.table("course_slides").upsert({
                "activity_id": activity_id,
                "stable_id": slide.get("stable_id") or slide["id"],
                "slide_type": slide.get("slide_type") or "concept",
                "title": slide["title"],
                "screen_content": slide.get("screen_content") or {},
                "visual": slide.get("visual") or {},
                "speech_text": slide.get("speech_text") or {},
                "question": slide.get("question") or {},
                "timing": slide.get("timing") or {},
                "order_index": slide_index,
                "metadata": {"manifest_id": slide["id"]},
            }, on_conflict="activity_id,stable_id").execute()
            slide_count += 1

        for stale_slide in existing_slides:
            if stale_slide["stable_id"] not in manifest_slide_ids:
                admin.table("course_slides").delete().eq(
                    "id", stale_slide["id"]
                ).execute()

    for stale_activity in existing_activities:
        if stale_activity["stable_id"] not in manifest_activity_ids:
            admin.table("course_activities").delete().eq(
                "id", stale_activity["id"]
            ).execute()

    print(
        f"{manifest_path.name}: {activity_count} activités, {slide_count} diapositives "
        f"→ {lesson['title_fr']} ({deck_status})"
    )
    return activity_count, slide_count


def main() -> None:
    if not MANIFESTS:
        raise SystemExit("Aucun manifest de cours trouvé")
    admin = get_supabase_admin()
    totals = [sync_manifest(admin, path) for path in MANIFESTS]
    print(f"Total : {sum(a for a, _ in totals)} activités, {sum(s for _, s in totals)} diapositives")


if __name__ == "__main__":
    main()
