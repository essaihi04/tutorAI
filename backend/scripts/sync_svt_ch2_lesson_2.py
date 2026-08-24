"""Synchronise la leçon 2 de génétique avec le parcours visuel audité.

Sans ``--apply``, le script affiche uniquement les changements prévus.
La migration SQL reste la source de vérité pour les déploiements.
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
LESSON_FILE = PROJECT_DIR / "database" / "seed_data" / "lessons" / "svt_ch2_l2.json"
load_dotenv(BACKEND_DIR / ".env")
if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.supabase_client import get_supabase_admin  # noqa: E402


def normalized(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFD", (value or "").lower())
        if unicodedata.category(char) != "Mn"
    )


def resource_rows(lesson_id: str, media: list[dict]) -> list[dict]:
    phase_by_type = {"simulation": "exploration", "image": "explanation"}
    rows = []
    for index, item in enumerate(media, start=1):
        url = item["url"]
        title = item.get("caption") or item.get("title") or f"Ressource {index}"
        metadata = {
            "caption": item.get("caption"),
            "visual": True,
            "source_type": "ai_generated_educational_illustration" if item["type"] == "image" else "interactive_visual_lab",
        }
        if item["type"] == "simulation":
            metadata.update({
                "simulation_id": "svt_gene_expression_advanced_lab",
                "simulation_version": "3.0",
                "variants": ["demonstration", "transcription", "translation", "mutations"],
                "llm_readable_state": True,
                "llm_controllable": True,
                "commands": [
                    "start", "pause", "next", "previous", "set_variant", "reset", "place_codon",
                    "place_amino_acid", "set_mutation", "check",
                    "reveal_hint", "highlight", "set_speed",
                ],
                "viewport": "native_100vh_no_scroll",
            })
        rows.append({
            "lesson_id": lesson_id,
            "section_title": "Expression de l'information génétique",
            "resource_type": item["type"],
            "title": title[:200],
            "description": item.get("caption", title),
            "file_path": url,
            "trigger_text": item.get("trigger"),
            "phase": phase_by_type.get(item["type"], "explanation"),
            "difficulty_tier": "beginner" if index < 3 else "intermediate",
            "concepts": ["ADN", "ARNm", "protéine", "mutation"],
            "metadata": metadata,
            "order_index": index,
        })
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="écrit les changements dans Supabase")
    args = parser.parse_args()

    lesson_data = json.loads(LESSON_FILE.read_text(encoding="utf-8"))
    db = get_supabase_admin()
    chapters = db.table("chapters").select("id,chapter_number,title_fr").eq("chapter_number", 2).execute().data or []
    chapter = next((row for row in chapters if "geneti" in normalized(row.get("title_fr", ""))), None)
    if not chapter:
        raise RuntimeError("Chapitre génétique SVT introuvable")

    lessons = db.table("lessons").select("id,title_fr,order_index").eq(
        "chapter_id", chapter["id"]
    ).order("order_index").execute().data or []
    lesson = next((row for row in lessons if row.get("order_index") == 2), None)
    if not lesson:
        lesson = next((row for row in lessons if "expression" in normalized(row.get("title_fr", ""))), None)
    if not lesson:
        raise RuntimeError("Leçon d'expression génétique introuvable ; appliquer d'abord la migration de structure du chapitre")

    rows = resource_rows(lesson["id"], lesson_data["media_resources"])
    missing = []
    existing_updates = []
    for row in rows:
        existing = db.table("lesson_resources").select("id").eq(
            "lesson_id", lesson["id"]
        ).eq("file_path", row["file_path"]).execute().data or []
        if not existing:
            missing.append(row)
        else:
            existing_updates.append((existing[0]["id"], row))

    print(f"Chapitre : {chapter['title_fr']}")
    print(f"Leçon : {lesson['title_fr']} ({lesson['id']})")
    print(f"Objectifs : {len(lesson_data['learning_objectives'])}")
    print(f"Ressources visuelles à ajouter : {len(missing)}")
    print(f"Ressources existantes à actualiser : {len(existing_updates)}")
    if not args.apply:
        print("Prévisualisation uniquement. Relancer avec --apply pour synchroniser.")
        return 0

    db.table("lessons").update({
        "title_fr": lesson_data["title_fr"],
        "lesson_type": lesson_data["lesson_type"],
        "duration_minutes": lesson_data["duration_minutes"],
        "order_index": lesson_data["order_index"],
        "learning_objectives": lesson_data["learning_objectives"],
        "content": lesson_data["content"],
        "media_resources": lesson_data["media_resources"],
    }).eq("id", lesson["id"]).execute()
    if missing:
        db.table("lesson_resources").insert(missing).execute()
    for resource_id, row in existing_updates:
        update_data = {key: value for key, value in row.items() if key != "lesson_id"}
        db.table("lesson_resources").update(update_data).eq("id", resource_id).execute()

    final = db.table("lesson_resources").select("id", count="exact").eq(
        "lesson_id", lesson["id"]
    ).execute()
    print(f"Synchronisation terminée : {final.count} ressources liées à la leçon")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
