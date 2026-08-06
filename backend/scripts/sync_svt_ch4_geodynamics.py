"""Synchronise les trois leçons visuelles de géodynamique interne.

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
LESSON_DIR = PROJECT_DIR / "database" / "seed_data" / "lessons"
LESSON_FILES = [
    LESSON_DIR / "svt_ch4_l1.json",
    LESSON_DIR / "svt_ch4_l2.json",
    LESSON_DIR / "svt_ch4_l3.json",
]

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


def resource_rows(lesson_id: str, lesson_data: dict) -> list[dict]:
    rows: list[dict] = []
    for index, item in enumerate(lesson_data["media_resources"], start=1):
        title = item.get("caption") or item.get("title") or f"Ressource {index}"
        metadata = {
            "caption": item.get("caption"),
            "visual": True,
            "source_type": (
                "ai_generated_scientific_illustration"
                if item["type"] == "image"
                else "interactive_visual_lab"
            ),
        }
        if item["type"] == "simulation":
            metadata.update(
                {
                    "simulation_id": "svt_internal_geodynamics_advanced_lab",
                    "simulation_version": "1.0",
                    "variants": [
                        "chains",
                        "deformations",
                        "metamorphism",
                        "granitization",
                    ],
                    "llm_readable_state": True,
                    "llm_controllable": True,
                    "commands": [
                        "start",
                        "set_variant",
                        "reset",
                        "place_stage",
                        "set_deformation_parameters",
                        "run_deformation_test",
                        "set_pt",
                        "record_pt",
                        "assign_granite_evidence",
                        "check",
                        "reveal_hint",
                        "highlight",
                    ],
                    "viewport": "native_100vh_no_scroll",
                }
            )

        rows.append(
            {
                "lesson_id": lesson_id,
                "section_title": lesson_data["title_fr"],
                "resource_type": item["type"],
                "title": title[:200],
                "description": item.get("caption", title),
                "file_path": item["url"],
                "trigger_text": item.get("trigger"),
                "phase": "exploration" if item["type"] == "simulation" else "explanation",
                "difficulty_tier": "intermediate",
                "concepts": [
                    "géodynamique interne",
                    "tectonique des plaques",
                    "métamorphisme",
                    "granitisation",
                ],
                "metadata": metadata,
                "order_index": index,
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="écrit les changements dans Supabase")
    args = parser.parse_args()

    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in LESSON_FILES]
    db = get_supabase_admin()
    chapters = (
        db.table("chapters")
        .select("id,chapter_number,title_fr")
        .eq("chapter_number", 4)
        .execute()
        .data
        or []
    )
    chapter = next(
        (
            row
            for row in chapters
            if "tectoni" in normalized(row.get("title_fr", ""))
            or "geolog" in normalized(row.get("title_fr", ""))
        ),
        None,
    )
    if not chapter:
        raise RuntimeError("Chapitre 4 de géodynamique SVT introuvable")

    existing_lessons = (
        db.table("lessons")
        .select("id,title_fr,order_index")
        .eq("chapter_id", chapter["id"])
        .order("order_index")
        .execute()
        .data
        or []
    )
    lesson_by_order = {row["order_index"]: row for row in existing_lessons}
    missing_orders = [p["order_index"] for p in payloads if p["order_index"] not in lesson_by_order]
    if missing_orders:
        raise RuntimeError(
            f"Leçon(s) distante(s) absente(s) pour order_index={missing_orders}; appliquer d'abord la migration SQL"
        )

    total_missing = 0
    total_updates = 0
    prepared: list[tuple[dict, dict, list[dict], list[tuple[str, dict]]]] = []
    print(f"Chapitre : {chapter['title_fr']}")

    for lesson_data in payloads:
        lesson = lesson_by_order[lesson_data["order_index"]]
        rows = resource_rows(lesson["id"], lesson_data)
        missing: list[dict] = []
        updates: list[tuple[str, dict]] = []
        for row in rows:
            existing = (
                db.table("lesson_resources")
                .select("id")
                .eq("lesson_id", lesson["id"])
                .eq("file_path", row["file_path"])
                .execute()
                .data
                or []
            )
            if existing:
                updates.append((existing[0]["id"], row))
            else:
                missing.append(row)

        total_missing += len(missing)
        total_updates += len(updates)
        prepared.append((lesson, lesson_data, missing, updates))
        print(
            f"- L{lesson_data['order_index']} {lesson_data['title_fr']} : "
            f"{len(missing)} ajout(s), {len(updates)} actualisation(s)"
        )

    if not args.apply:
        print(
            f"Prévisualisation : {total_missing} ressource(s) à ajouter, "
            f"{total_updates} à actualiser. Relancer avec --apply."
        )
        return 0

    for lesson, lesson_data, missing, updates in prepared:
        db.table("lessons").update(
            {
                "title_fr": lesson_data["title_fr"],
                "title_ar": lesson_data["title_ar"],
                "lesson_type": lesson_data["lesson_type"],
                "duration_minutes": lesson_data["duration_minutes"],
                "order_index": lesson_data["order_index"],
                "learning_objectives": lesson_data["learning_objectives"],
                "content": lesson_data["content"],
                "media_resources": lesson_data["media_resources"],
            }
        ).eq("id", lesson["id"]).execute()

        if missing:
            db.table("lesson_resources").insert(missing).execute()
        for resource_id, row in updates:
            update_data = {key: value for key, value in row.items() if key != "lesson_id"}
            db.table("lesson_resources").update(update_data).eq("id", resource_id).execute()

    print(
        f"Synchronisation terminée : {len(payloads)} leçons, "
        f"{total_missing} ajout(s), {total_updates} actualisation(s)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
