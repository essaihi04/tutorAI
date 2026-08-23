"""Versioned authoring service for the admin course editor.

The student player reads only published database decks (or a versioned local
manifest as a deployment fallback).  The editor therefore writes drafts,
preserves stable activity/slide identifiers and publishes explicitly.  Audio
files are never deleted when speech changes: incompatible rows are marked
``stale`` and the on-demand TTS cache naturally uses the new text hash.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, Optional

from app.services.schema_catalog import SCHEMA_CATALOG, SCHEMA_IDS
from app.services.scientific_visual_skill import normalize_scientific_visual
from app.supabase_client import get_supabase_admin


BACKEND_ROOT = Path(__file__).resolve().parents[2]
REPOSITORY_ROOT = BACKEND_ROOT.parent
COURSE_DIR = BACKEND_ROOT / "data" / "courses"
FRONTEND_PUBLIC = REPOSITORY_ROOT / "frontend" / "public"
COURSE_MEDIA_DIR = FRONTEND_PUBLIC / "media" / "images" / "course-editor"

_STABLE_ID_RE = re.compile(r"^[a-z0-9][a-z0-9_-]{1,139}$")
_ALLOWED_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif"}
_LIBRARY_IMAGE_SUFFIXES = _ALLOWED_IMAGE_SUFFIXES | {".svg"}
_ALLOWED_IMAGE_TYPES = {"image/png", "image/jpeg", "image/webp", "image/gif"}
_MAX_IMAGE_BYTES = 10 * 1024 * 1024
_QUESTION_TYPES = {"qcm", "prediction", "true_false", "select", "open", "ordering", "association"}
_VISUAL_KINDS = {"none", "image", "schema", "simulation", "scientific"}


class CourseEditorError(ValueError):
    """A user-facing course editor error."""


class CourseValidationError(CourseEditorError):
    def __init__(self, issues: list[dict[str, str]]) -> None:
        self.issues = issues
        super().__init__("Le cours contient des erreurs de validation")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _normalise(value: Any) -> str:
    text = str(value or "").strip().casefold()
    return "".join(
        char for char in unicodedata.normalize("NFD", text)
        if unicodedata.category(char) != "Mn"
    )


def _chapter(lesson: dict) -> dict:
    value = lesson.get("chapters") or {}
    return value[0] if isinstance(value, list) and value else value if isinstance(value, dict) else {}


def _subject(chapter: dict) -> dict:
    value = chapter.get("subjects") or {}
    return value[0] if isinstance(value, list) and value else value if isinstance(value, dict) else {}


def _data(result: Any) -> list[dict]:
    return list(getattr(result, "data", None) or [])


def _speech_hash(text: str) -> str:
    return hashlib.sha256((text or "").strip().encode("utf-8")).hexdigest()


def _is_persistent_image_url(value: Any) -> bool:
    url = str(value or "")
    return url.startswith("/media/") or bool(re.match(
        r"^https://[^/]+/storage/v1/object/public/pedagogical-resources/",
        url,
        flags=re.IGNORECASE,
    ))


class AdminCourseService:
    def __init__(self) -> None:
        self._manifest_cache: Optional[list[dict]] = None

    def _admin(self):
        return get_supabase_admin()

    def _manifests(self) -> list[dict]:
        if self._manifest_cache is None:
            manifests: list[dict] = []
            for path in sorted(COURSE_DIR.glob("*_course_v1.json")):
                manifest = json.loads(path.read_text(encoding="utf-8"))
                manifest["_manifest_path"] = path.name
                manifests.append(manifest)
            self._manifest_cache = manifests
        return copy.deepcopy(self._manifest_cache)

    def _manifest(self, stable_id: str) -> Optional[dict]:
        return next(
            (
                manifest for manifest in self._manifests()
                if str(manifest.get("stable_id") or manifest.get("id")) == stable_id
            ),
            None,
        )

    def list_lessons(self, admin=None) -> list[dict]:
        admin = admin or self._admin()
        rows = _data(admin.table("lessons").select(
            "id,title_fr,chapter_id,chapters(id,title_fr,subject_id,subjects(id,name_fr,name_ar))"
        ).execute())
        lessons: list[dict] = []
        for row in rows:
            chapter = _chapter(row)
            subject = _subject(chapter)
            lessons.append({
                "id": str(row.get("id") or ""),
                "title": row.get("title_fr") or "Leçon",
                "chapter_id": str(row.get("chapter_id") or chapter.get("id") or ""),
                "chapter_title": chapter.get("title_fr") or "",
                "subject_id": str(chapter.get("subject_id") or subject.get("id") or ""),
                "subject_name": subject.get("name_fr") or "Matière",
                "subject_name_ar": subject.get("name_ar") or "",
            })
        lessons.sort(key=lambda item: (item["subject_name"], item["chapter_title"], item["title"]))
        return lessons

    @staticmethod
    def _matching_lesson(manifest: dict, lessons: list[dict]) -> Optional[dict]:
        tokens = [_normalise(token) for token in manifest.get("lesson_match") or []]
        for lesson in lessons:
            haystack = _normalise(f"{lesson.get('title', '')} {lesson.get('chapter_title', '')}")
            if any(token and token in haystack for token in tokens):
                return lesson
        return None

    def list_courses(self) -> dict:
        admin = self._admin()
        lessons = self.list_lessons(admin)
        lessons_by_id = {lesson["id"]: lesson for lesson in lessons}
        manifests = self._manifests()
        manifests_by_stable = {
            str(item.get("stable_id") or item.get("id")): item for item in manifests
        }

        database_available = True
        database_error: Optional[str] = None
        try:
            decks = _data(admin.table("course_decks").select("*").order(
                "updated_at", desc=True
            ).execute())
            activities = _data(admin.table("course_activities").select(
                "id,deck_id"
            ).execute())
            slides = _data(admin.table("course_slides").select(
                "id,activity_id"
            ).execute())
            audio_rows = _data(admin.table("course_slide_audio").select(
                "slide_id,status"
            ).execute())
        except Exception as exc:
            database_available = False
            database_error = str(exc)
            decks, activities, slides, audio_rows = [], [], [], []

        activity_ids_by_deck: dict[str, set[str]] = {}
        for activity in activities:
            activity_ids_by_deck.setdefault(str(activity.get("deck_id")), set()).add(str(activity.get("id")))
        slide_ids_by_deck: dict[str, set[str]] = {}
        for deck_id, activity_ids in activity_ids_by_deck.items():
            slide_ids_by_deck[deck_id] = {
                str(slide.get("id")) for slide in slides
                if str(slide.get("activity_id")) in activity_ids
            }
        stale_by_deck: dict[str, int] = {}
        for deck_id, slide_ids in slide_ids_by_deck.items():
            stale_by_deck[deck_id] = sum(
                1 for audio in audio_rows
                if str(audio.get("slide_id")) in slide_ids and audio.get("status") == "stale"
            )

        courses: list[dict] = []
        published_stable_ids: set[str] = set()
        for deck in decks:
            metadata = deck.get("metadata") or {}
            stable_id = str(metadata.get("stable_id") or deck.get("id"))
            manifest = manifests_by_stable.get(stable_id) or {}
            catalog = metadata.get("catalog") or manifest.get("catalog") or {}
            lesson = lessons_by_id.get(str(deck.get("lesson_id"))) or {}
            deck_id = str(deck.get("id"))
            activity_count = len(activity_ids_by_deck.get(deck_id, set()))
            slide_count = len(slide_ids_by_deck.get(deck_id, set()))
            if deck.get("status") == "published":
                published_stable_ids.add(stable_id)
            courses.append({
                "ref": deck_id,
                "id": deck_id,
                "source": "database",
                "stable_id": stable_id,
                "title": deck.get("title") or "Cours",
                "version": int(deck.get("version") or 1),
                "status": deck.get("status") or "draft",
                "language": deck.get("language") or "fr",
                "estimated_minutes": int(deck.get("estimated_minutes") or 0),
                "lesson_id": str(deck.get("lesson_id") or ""),
                "lesson_title": lesson.get("title") or "",
                "chapter_title": lesson.get("chapter_title") or "",
                "subject_name": lesson.get("subject_name") or "",
                "activity_count": activity_count,
                "slide_count": slide_count,
                "cover_image": catalog.get("cover_image"),
                "stale_audio_count": stale_by_deck.get(deck_id, 0),
                "editable": deck.get("status") in {"draft", "verified"},
                "updated_at": deck.get("updated_at") or deck.get("created_at"),
            })

        # A manifest remains visible as the live deployment fallback until a
        # database version of the same course has actually been published.
        for manifest in manifests:
            stable_id = str(manifest.get("stable_id") or manifest.get("id"))
            if stable_id in published_stable_ids:
                continue
            lesson = self._matching_lesson(manifest, lessons) or {}
            activities_data = manifest.get("activities") or []
            courses.append({
                "ref": f"manifest:{stable_id}",
                "id": f"manifest:{stable_id}",
                "source": "manifest",
                "stable_id": stable_id,
                "title": manifest.get("title") or "Cours",
                "version": int(manifest.get("version") or 1),
                "status": "published_fallback",
                "language": manifest.get("language") or "fr",
                "estimated_minutes": int(manifest.get("estimated_minutes") or 0),
                "lesson_id": lesson.get("id") or "",
                "lesson_title": lesson.get("title") or "",
                "chapter_title": lesson.get("chapter_title") or "",
                "subject_name": lesson.get("subject_name") or "",
                "activity_count": len(activities_data),
                "slide_count": sum(len(item.get("slides") or []) for item in activities_data),
                "cover_image": (manifest.get("catalog") or {}).get("cover_image"),
                "stale_audio_count": 0,
                "editable": False,
                "updated_at": None,
            })

        status_order = {"draft": 0, "verified": 1, "published": 2, "published_fallback": 3, "archived": 4}
        courses.sort(key=lambda item: (
            item.get("subject_name") or "zzz",
            item.get("title") or "",
            status_order.get(str(item.get("status")), 9),
            -int(item.get("version") or 0),
        ))
        return {
            "courses": courses,
            "lessons": lessons,
            "database_available": database_available,
            "database_error": database_error,
        }

    def editor_options(self) -> dict:
        image_urls: list[str] = []
        image_root = FRONTEND_PUBLIC / "media" / "images"
        if image_root.exists():
            image_urls = [
                "/" + path.relative_to(FRONTEND_PUBLIC).as_posix()
                for path in image_root.rglob("*")
                if path.is_file() and path.suffix.lower() in _LIBRARY_IMAGE_SUFFIXES
            ]
        simulation_root = FRONTEND_PUBLIC / "media" / "simulations"
        simulation_urls: list[str] = []
        if simulation_root.exists():
            simulation_urls = [
                "/" + path.relative_to(FRONTEND_PUBLIC).as_posix()
                for path in simulation_root.rglob("index.html")
                if path.name == "index.html"
            ]
        return {
            "lessons": self.list_lessons(),
            "schemas": copy.deepcopy(SCHEMA_CATALOG),
            "media": {
                "images": sorted(image_urls),
                "simulations": sorted(simulation_urls),
            },
            "slide_types": [
                "diagnostic", "situation", "concept", "image", "schema",
                "simulation", "exercise", "synthesis", "evaluation",
            ],
            "question_types": sorted(_QUESTION_TYPES),
        }

    def _db_course(self, course_id: str, admin=None) -> dict:
        admin = admin or self._admin()
        rows = _data(admin.table("course_decks").select("*").eq(
            "id", course_id
        ).limit(1).execute())
        if not rows:
            raise CourseEditorError("Cours introuvable")
        deck = rows[0]
        activities = _data(admin.table("course_activities").select("*").eq(
            "deck_id", course_id
        ).order("order_index").execute())
        activity_ids = [row["id"] for row in activities]
        slides: list[dict] = []
        if activity_ids:
            slides = _data(admin.table("course_slides").select("*").in_(
                "activity_id", activity_ids
            ).order("order_index").execute())
        slide_ids = [row["id"] for row in slides]
        audio_rows: list[dict] = []
        if slide_ids:
            audio_rows = _data(admin.table("course_slide_audio").select("*").in_(
                "slide_id", slide_ids
            ).order("created_at", desc=True).execute())
        audio_by_slide: dict[str, list[dict]] = {}
        for audio in audio_rows:
            audio_by_slide.setdefault(str(audio.get("slide_id")), []).append(audio)
        slides_by_activity: dict[str, list[dict]] = {}
        for slide in slides:
            item = copy.deepcopy(slide)
            item["audio_assets"] = audio_by_slide.get(str(slide.get("id")), [])
            slides_by_activity.setdefault(str(slide.get("activity_id")), []).append(item)
        deck["activities"] = [
            {**activity, "slides": slides_by_activity.get(str(activity.get("id")), [])}
            for activity in activities
        ]
        return deck

    def get_course(self, course_ref: str) -> dict:
        if course_ref.startswith("manifest:"):
            stable_id = course_ref.split(":", 1)[1]
            manifest = self._manifest(stable_id)
            if not manifest:
                raise CourseEditorError("Manifest de cours introuvable")
            lesson = self._matching_lesson(manifest, self.list_lessons()) or {}
            result = copy.deepcopy(manifest)
            result.pop("_manifest_path", None)
            result.update({
                "id": course_ref,
                "ref": course_ref,
                "source": "manifest",
                "status": "published_fallback",
                "lesson_id": lesson.get("id") or "",
                "lesson": lesson,
                "editable": False,
            })
            for activity in result.get("activities") or []:
                for slide in activity.get("slides") or []:
                    slide.setdefault("audio_assets", [])
            return result

        deck = self._db_course(course_ref)
        metadata = deck.get("metadata") or {}
        stable_id = str(metadata.get("stable_id") or deck.get("id"))
        manifest = self._manifest(stable_id) or {}
        lessons = self.list_lessons()
        lesson = next((item for item in lessons if item["id"] == str(deck.get("lesson_id"))), {})
        deck.update({
            "ref": str(deck.get("id")),
            "source": "database",
            "stable_id": stable_id,
            "catalog": metadata.get("catalog") or manifest.get("catalog") or {},
            "lesson_match": metadata.get("lesson_match") or manifest.get("lesson_match") or [],
            "intent_aliases": metadata.get("intent_aliases") or manifest.get("intent_aliases") or [],
            "lesson": lesson,
            "editable": deck.get("status") in {"draft", "verified"},
        })
        return deck

    @staticmethod
    def validate_payload(payload: dict, *, for_publish: bool = False) -> list[dict[str, str]]:
        issues: list[dict[str, str]] = []

        def add(level: str, path: str, message: str) -> None:
            issues.append({"level": level, "path": path, "message": message})

        stable_id = str(payload.get("stable_id") or "")
        if not _STABLE_ID_RE.fullmatch(stable_id):
            add("error", "stable_id", "Identifiant stable invalide (minuscules, chiffres, _ ou -).")
        if not str(payload.get("title") or "").strip():
            add("error", "title", "Le titre du cours est obligatoire.")
        catalog = payload.get("catalog") or {}
        cover_image = catalog.get("cover_image")
        if cover_image and not _is_persistent_image_url(cover_image):
            add("error", "catalog.cover_image", "La couverture doit provenir de la bibliothèque persistante.")
        if for_publish and not str(catalog.get("summary") or "").strip():
            add("error", "catalog.summary", "Le résumé de la carte du cours est obligatoire.")
        if for_publish and not cover_image:
            add("error", "catalog.cover_image", "Ajoutez une miniature avant publication.")
        if for_publish and not str(catalog.get("cover_alt") or "").strip():
            add("error", "catalog.cover_alt", "Décrivez la miniature pour l'accessibilité.")
        if for_publish and len(catalog.get("essential_topics") or []) < 3:
            add("error", "catalog.essential_topics", "Indiquez au moins trois notions essentielles.")
        if for_publish and not (payload.get("intent_aliases") or []):
            add("error", "intent_aliases", "Ajoutez au moins une demande reconnue par le tuteur.")

        activities = payload.get("activities") or []
        if for_publish and not activities:
            add("error", "activities", "Un cours publié doit contenir au moins une activité.")
        activity_ids: set[str] = set()
        slide_ids: set[str] = set()
        for activity_index, activity in enumerate(activities):
            activity_path = f"activities[{activity_index}]"
            activity_stable = str(activity.get("stable_id") or "")
            if not _STABLE_ID_RE.fullmatch(activity_stable):
                add("error", f"{activity_path}.stable_id", "Identifiant d'activité invalide.")
            if activity_stable in activity_ids:
                add("error", f"{activity_path}.stable_id", "Identifiant d'activité dupliqué.")
            activity_ids.add(activity_stable)
            duration = int(activity.get("duration_minutes") or 0)
            if duration < 1 or duration > 180:
                add("error", f"{activity_path}.duration_minutes", "Durée attendue entre 1 et 180 minutes.")
            elif not 15 <= duration <= 20:
                add("warning", f"{activity_path}.duration_minutes", "Pour un parcours BAC, privilégiez une activité de 15 à 20 minutes.")
            if for_publish and not (activity.get("slides") or []):
                add("error", f"{activity_path}.slides", "Une activité publiée doit avoir au moins une diapositive.")

            for slide_index, slide in enumerate(activity.get("slides") or []):
                slide_path = f"{activity_path}.slides[{slide_index}]"
                slide_stable = str(slide.get("stable_id") or "")
                if not _STABLE_ID_RE.fullmatch(slide_stable):
                    add("error", f"{slide_path}.stable_id", "Identifiant de diapositive invalide.")
                if slide_stable in slide_ids:
                    add("error", f"{slide_path}.stable_id", "Identifiant de diapositive dupliqué dans le cours.")
                slide_ids.add(slide_stable)
                if not str(slide.get("title") or "").strip():
                    add("error", f"{slide_path}.title", "Le titre de la diapositive est obligatoire.")

                speech = slide.get("speech_text") or {}
                if for_publish and not str(speech.get("fr") or "").strip():
                    add("error", f"{slide_path}.speech_text.fr", "Le speech français est obligatoire avant publication.")
                if for_publish and not str(speech.get("mixed") or "").strip():
                    add("error", f"{slide_path}.speech_text.mixed", "Le speech Darija est obligatoire avant publication.")
                elif not str(speech.get("mixed") or "").strip():
                    add("warning", f"{slide_path}.speech_text.mixed", "Speech Darija encore vide.")

                question = slide.get("question") or {}
                qtype = question.get("type") or "open"
                if qtype not in _QUESTION_TYPES:
                    add("error", f"{slide_path}.question.type", "Type de question non reconnu.")
                if for_publish and not str(question.get("prompt") or "").strip():
                    add("error", f"{slide_path}.question.prompt", "Chaque diapositive doit proposer une petite question.")
                timeout = int(question.get("timeout_seconds") or 0)
                if for_publish and (timeout < 5 or timeout > 180):
                    add("error", f"{slide_path}.question.timeout_seconds", "Le délai doit être compris entre 5 et 180 secondes.")
                if for_publish and question.get("advance_on_timeout") is not True:
                    add("error", f"{slide_path}.question.advance_on_timeout", "Le passage automatique sans réponse doit être activé.")
                if for_publish and qtype in {"qcm", "prediction", "true_false", "select", "ordering", "association"}:
                    answer_key = question.get("answer_key")
                    if answer_key is None or answer_key == "" or answer_key == []:
                        add("error", f"{slide_path}.question.answer_key", "Ajoutez la réponse attendue pour permettre le feedback formatif.")

                visual = slide.get("visual") or {}
                kind = visual.get("kind") or "none"
                if kind not in _VISUAL_KINDS:
                    add("error", f"{slide_path}.visual.kind", "Type de visuel non reconnu.")
                elif kind == "schema" and visual.get("schema_id") not in SCHEMA_IDS:
                    add("error", f"{slide_path}.visual.schema_id", "Schéma absent du registre scientifique validé.")
                elif kind == "scientific" and normalize_scientific_visual(visual.get("scientific")) is None:
                    add("error", f"{slide_path}.visual.scientific", "Payload scientifique invalide ou moteur non autorisé.")
                elif kind in {"image", "simulation"}:
                    url = str(visual.get("url") or "")
                    valid_url = url.startswith("/media/") if kind == "simulation" else _is_persistent_image_url(url)
                    if not valid_url:
                        add("error", f"{slide_path}.visual.url", "Utilisez un média persistant de la bibliothèque du cours.")
                    if for_publish and kind == "image" and not str(visual.get("alt") or "").strip():
                        add("error", f"{slide_path}.visual.alt", "Décrivez l'image pour les élèves qui ne peuvent pas la voir.")

        return issues

    @staticmethod
    def _sanitise_payload(payload: dict) -> dict:
        cleaned = copy.deepcopy(payload)
        for activity in cleaned.get("activities") or []:
            activity["objective_ids"] = [
                str(item).strip() for item in activity.get("objective_ids") or [] if str(item).strip()
            ]
            for slide in activity.get("slides") or []:
                visual = slide.get("visual") or {}
                if visual.get("kind") == "scientific":
                    visual["scientific"] = normalize_scientific_visual(visual.get("scientific"))
                slide["visual"] = visual
                slide["speech_text"] = {
                    str(language): str(text).strip()
                    for language, text in (slide.get("speech_text") or {}).items()
                    if str(text).strip()
                }
        return cleaned

    @staticmethod
    def _metadata(payload: dict, previous: Optional[dict] = None) -> dict:
        metadata = copy.deepcopy(previous or {})
        metadata.update({
            "stable_id": payload["stable_id"],
            "catalog": payload.get("catalog") or {},
            "lesson_match": payload.get("lesson_match") or [],
            "intent_aliases": payload.get("intent_aliases") or [],
            "editor": "admin-dashboard",
        })
        return metadata

    def _next_version(self, admin, lesson_id: str) -> int:
        rows = _data(admin.table("course_decks").select("version").eq(
            "lesson_id", lesson_id
        ).order("version", desc=True).limit(1).execute())
        return int(rows[0].get("version") or 0) + 1 if rows else 1

    def _assert_lesson(self, admin, lesson_id: str) -> None:
        rows = _data(admin.table("lessons").select("id").eq("id", lesson_id).limit(1).execute())
        if not rows:
            raise CourseEditorError("Leçon introuvable")

    def _assert_stable_scope(self, admin, stable_id: str, lesson_id: str, exclude_id: str = "") -> None:
        rows = _data(admin.table("course_decks").select("id,lesson_id,metadata").execute())
        for row in rows:
            if exclude_id and str(row.get("id")) == exclude_id:
                continue
            metadata = row.get("metadata") or {}
            if metadata.get("stable_id") == stable_id and str(row.get("lesson_id")) != str(lesson_id):
                raise CourseEditorError("Cet identifiant stable appartient déjà à une autre leçon")

    def _insert_tree(self, admin, lesson_id: str, version: int, payload: dict, previous_metadata: Optional[dict] = None) -> str:
        clean = self._sanitise_payload(payload)
        deck_id = str(uuid.uuid4())
        timestamp = _now()
        try:
            admin.table("course_decks").insert({
                "id": deck_id,
                "lesson_id": lesson_id,
                "version": version,
                "title": clean["title"],
                "status": "draft",
                "language": clean.get("language") or "fr",
                "estimated_minutes": int(clean.get("estimated_minutes") or 50),
                "metadata": self._metadata(clean, previous_metadata),
                "created_at": timestamp,
                "updated_at": timestamp,
            }).execute()
            for activity_index, activity in enumerate(clean.get("activities") or []):
                activity_id = str(uuid.uuid4())
                admin.table("course_activities").insert({
                    "id": activity_id,
                    "deck_id": deck_id,
                    "stable_id": activity["stable_id"],
                    "title": activity["title"],
                    "phase": activity.get("phase") or "explanation",
                    "duration_minutes": int(activity.get("duration_minutes") or 15),
                    "objective_ids": activity.get("objective_ids") or [],
                    "order_index": activity_index,
                    "metadata": activity.get("metadata") or {},
                }).execute()
                slide_rows = []
                for slide_index, slide in enumerate(activity.get("slides") or []):
                    slide_rows.append({
                        "id": str(uuid.uuid4()),
                        "activity_id": activity_id,
                        "stable_id": slide["stable_id"],
                        "slide_type": slide.get("slide_type") or "concept",
                        "title": slide["title"],
                        "screen_content": slide.get("screen_content") or {},
                        "visual": slide.get("visual") or {},
                        "speech_text": slide.get("speech_text") or {},
                        "question": slide.get("question") or {},
                        "timing": slide.get("timing") or {},
                        "order_index": slide_index,
                        "metadata": slide.get("metadata") or {},
                        "created_at": timestamp,
                        "updated_at": timestamp,
                    })
                if slide_rows:
                    admin.table("course_slides").insert(slide_rows).execute()
        except Exception:
            try:
                admin.table("course_decks").delete().eq("id", deck_id).execute()
            except Exception:
                pass
            raise
        return deck_id

    def create_course(self, data: dict) -> dict:
        admin = self._admin()
        lesson_id = str(data["lesson_id"])
        self._assert_lesson(admin, lesson_id)
        self._assert_stable_scope(admin, data["stable_id"], lesson_id)
        suffix = uuid.uuid4().hex[:8]
        payload = {
            "stable_id": data["stable_id"],
            "title": data["title"],
            "language": data.get("language") or "fr",
            "estimated_minutes": int(data.get("estimated_minutes") or 50),
            "catalog": {"summary": "", "cover_image": "", "cover_alt": "", "essential_topics": []},
            "lesson_match": [data["title"]],
            "intent_aliases": [data["title"]],
            "activities": [{
                "stable_id": f"{data['stable_id']}_a01_{suffix}",
                "title": "Nouvelle activité",
                "phase": "explanation",
                "duration_minutes": 15,
                "objective_ids": [],
                "slides": [],
            }],
        }
        issues = self.validate_payload(payload)
        if any(item["level"] == "error" for item in issues):
            raise CourseValidationError(issues)
        deck_id = self._insert_tree(admin, lesson_id, self._next_version(admin, lesson_id), payload)
        return self.get_course(deck_id)

    def duplicate_course(self, course_ref: str, lesson_id: Optional[str] = None) -> dict:
        admin = self._admin()
        source = self.get_course(course_ref)
        target_lesson = str(lesson_id or source.get("lesson_id") or "")
        if not target_lesson:
            raise CourseEditorError("Choisissez la leçon à laquelle rattacher ce cours")
        self._assert_lesson(admin, target_lesson)
        stable_id = str(source.get("stable_id") or "")
        self._assert_stable_scope(admin, stable_id, target_lesson)
        payload = {
            "stable_id": stable_id,
            "title": source.get("title") or "Cours",
            "language": source.get("language") or "fr",
            "estimated_minutes": int(source.get("estimated_minutes") or 50),
            "catalog": source.get("catalog") or {},
            "lesson_match": source.get("lesson_match") or [],
            "intent_aliases": source.get("intent_aliases") or [],
            "activities": source.get("activities") or [],
        }
        issues = self.validate_payload(payload)
        if any(item["level"] == "error" for item in issues):
            raise CourseValidationError(issues)
        previous_metadata = source.get("metadata") or {}
        deck_id = self._insert_tree(
            admin,
            target_lesson,
            self._next_version(admin, target_lesson),
            payload,
            previous_metadata,
        )
        return self.get_course(deck_id)

    def _mark_stale_audio(self, admin, slide_id: str, speech_text: dict) -> int:
        rows = _data(admin.table("course_slide_audio").select(
            "id,language,speech_hash,status"
        ).eq("slide_id", slide_id).execute())
        stale_ids: list[str] = []
        for row in rows:
            language = row.get("language") or "fr"
            speech = speech_text.get(language) or speech_text.get("fr") or ""
            if not speech or row.get("speech_hash") != _speech_hash(speech):
                if row.get("status") not in {"stale", "rejected"}:
                    stale_ids.append(str(row["id"]))
        if stale_ids:
            admin.table("course_slide_audio").update({"status": "stale"}).in_("id", stale_ids).execute()
        return len(stale_ids)

    def save_course(self, course_id: str, payload: dict) -> dict:
        admin = self._admin()
        deck = self._db_course(course_id, admin)
        if deck.get("status") not in {"draft", "verified"}:
            raise CourseEditorError("Créez une nouvelle version pour modifier un cours publié ou archivé")
        issues = self.validate_payload(payload)
        if any(item["level"] == "error" for item in issues):
            raise CourseValidationError(issues)
        clean = self._sanitise_payload(payload)
        lesson_id = str(deck.get("lesson_id"))
        self._assert_stable_scope(admin, clean["stable_id"], lesson_id, exclude_id=course_id)

        existing_activities = deck.get("activities") or []
        activity_by_stable = {str(row.get("stable_id")): row for row in existing_activities}
        for offset, row in enumerate(existing_activities):
            admin.table("course_activities").update({
                "order_index": 100_000 + offset,
            }).eq("id", row["id"]).execute()

        stale_audio_count = 0
        retained_activity_ids: set[str] = set()
        timestamp = _now()
        for activity_index, activity in enumerate(clean.get("activities") or []):
            existing_activity = activity_by_stable.get(activity["stable_id"])
            activity_id = str(existing_activity.get("id")) if existing_activity else str(uuid.uuid4())
            activity_row = {
                "id": activity_id,
                "deck_id": course_id,
                "stable_id": activity["stable_id"],
                "title": activity["title"],
                "phase": activity.get("phase") or "explanation",
                "duration_minutes": int(activity.get("duration_minutes") or 15),
                "objective_ids": activity.get("objective_ids") or [],
                "order_index": activity_index,
                "metadata": activity.get("metadata") or {},
            }
            if existing_activity:
                admin.table("course_activities").update(activity_row).eq("id", activity_id).execute()
            else:
                admin.table("course_activities").insert(activity_row).execute()
            retained_activity_ids.add(activity_id)

            previous_slides = (existing_activity or {}).get("slides") or []
            slide_by_stable = {str(row.get("stable_id")): row for row in previous_slides}
            for offset, row in enumerate(previous_slides):
                admin.table("course_slides").update({
                    "order_index": 100_000 + offset,
                }).eq("id", row["id"]).execute()

            retained_slide_ids: set[str] = set()
            for slide_index, slide in enumerate(activity.get("slides") or []):
                existing_slide = slide_by_stable.get(slide["stable_id"])
                slide_id = str(existing_slide.get("id")) if existing_slide else str(uuid.uuid4())
                slide_row = {
                    "id": slide_id,
                    "activity_id": activity_id,
                    "stable_id": slide["stable_id"],
                    "slide_type": slide.get("slide_type") or "concept",
                    "title": slide["title"],
                    "screen_content": slide.get("screen_content") or {},
                    "visual": slide.get("visual") or {},
                    "speech_text": slide.get("speech_text") or {},
                    "question": slide.get("question") or {},
                    "timing": slide.get("timing") or {},
                    "order_index": slide_index,
                    "metadata": slide.get("metadata") or {},
                    "updated_at": timestamp,
                }
                if existing_slide:
                    admin.table("course_slides").update(slide_row).eq("id", slide_id).execute()
                else:
                    slide_row["created_at"] = timestamp
                    admin.table("course_slides").insert(slide_row).execute()
                retained_slide_ids.add(slide_id)
                stale_audio_count += self._mark_stale_audio(admin, slide_id, slide_row["speech_text"])

            for previous_slide in previous_slides:
                if str(previous_slide.get("id")) not in retained_slide_ids:
                    admin.table("course_slides").delete().eq("id", previous_slide["id"]).execute()

        for previous_activity in existing_activities:
            if str(previous_activity.get("id")) not in retained_activity_ids:
                admin.table("course_activities").delete().eq("id", previous_activity["id"]).execute()

        admin.table("course_decks").update({
            "title": clean["title"],
            "status": "draft",
            "language": clean.get("language") or "fr",
            "estimated_minutes": int(clean.get("estimated_minutes") or 50),
            "metadata": self._metadata(clean, deck.get("metadata") or {}),
            "updated_at": timestamp,
        }).eq("id", course_id).execute()
        result = self.get_course(course_id)
        result["validation_issues"] = issues
        result["stale_audio_count"] = stale_audio_count
        return result

    def publish_course(self, course_id: str) -> dict:
        admin = self._admin()
        course = self.get_course(course_id)
        if course.get("source") != "database":
            raise CourseEditorError("Importez d'abord le manifest comme brouillon")
        if course.get("status") not in {"draft", "verified", "published"}:
            raise CourseEditorError("Ce cours archivé doit être dupliqué avant publication")
        payload = {
            key: course.get(key) for key in (
                "stable_id", "title", "language", "estimated_minutes", "catalog",
                "lesson_match", "intent_aliases", "activities",
            )
        }
        issues = self.validate_payload(payload, for_publish=True)
        if any(item["level"] == "error" for item in issues):
            raise CourseValidationError(issues)

        timestamp = _now()
        # Publish the selected deck first so a transient failure never removes
        # the currently available lesson. Older versions are archived after.
        admin.table("course_decks").update({
            "status": "published",
            "published_at": timestamp,
            "updated_at": timestamp,
        }).eq("id", course_id).execute()
        old_rows = _data(admin.table("course_decks").select("id").eq(
            "lesson_id", course["lesson_id"]
        ).eq("status", "published").execute())
        old_ids = [str(row["id"]) for row in old_rows if str(row["id"]) != course_id]
        if old_ids:
            admin.table("course_decks").update({
                "status": "archived", "updated_at": timestamp,
            }).in_("id", old_ids).execute()
        result = self.get_course(course_id)
        result["validation_issues"] = issues
        return result

    def archive_course(self, course_id: str) -> dict:
        admin = self._admin()
        course = self.get_course(course_id)
        if course.get("source") != "database":
            raise CourseEditorError("Le manifest de secours ne peut pas être archivé depuis l'éditeur")
        admin.table("course_decks").update({
            "status": "archived", "updated_at": _now(),
        }).eq("id", course_id).execute()
        return self.get_course(course_id)

    def delete_course(self, course_id: str) -> None:
        admin = self._admin()
        course = self.get_course(course_id)
        if course.get("source") != "database":
            raise CourseEditorError("Un manifest versionné ne peut pas être supprimé depuis le dashboard")
        if course.get("status") == "published":
            raise CourseEditorError("Archivez le cours publié avant de le supprimer")
        admin.table("course_decks").delete().eq("id", course_id).execute()

    def set_audio_status(self, audio_id: str, status: str) -> dict:
        admin = self._admin()
        rows = _data(admin.table("course_slide_audio").update({
            "status": status,
            "verified_at": _now() if status in {"verified", "published"} else None,
        }).eq("id", audio_id).execute())
        if not rows:
            raise CourseEditorError("Audio introuvable")
        return rows[0]

    def save_media(self, filename: str, content_type: str, content: bytes) -> str:
        suffix = Path(filename or "").suffix.lower()
        if suffix not in _ALLOWED_IMAGE_SUFFIXES or content_type not in _ALLOWED_IMAGE_TYPES:
            raise CourseEditorError("Format refusé. Utilisez PNG, JPEG, WEBP ou GIF.")
        if not content or len(content) > _MAX_IMAGE_BYTES:
            raise CourseEditorError("L'image doit peser entre 1 octet et 10 Mo.")
        stem = re.sub(r"[^a-z0-9_-]+", "-", Path(filename).stem.casefold()).strip("-") or "visuel"
        stored_name = f"{stem[:60]}-{uuid.uuid4().hex[:10]}{suffix}"
        # Object storage is the production path: uploaded illustrations must
        # survive application redeployments. A local public asset is retained
        # as a development fallback when the bucket is not configured.
        try:
            storage_path = f"course-editor/{datetime.now(timezone.utc):%Y/%m}/{stored_name}"
            storage = self._admin().storage.from_("pedagogical-resources")
            storage.upload(
                path=storage_path,
                file=content,
                file_options={"content-type": content_type},
            )
            public_url = str(storage.get_public_url(storage_path) or "").rstrip("?")
            if public_url:
                return public_url
        except Exception:
            pass

        COURSE_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
        target = (COURSE_MEDIA_DIR / stored_name).resolve()
        if COURSE_MEDIA_DIR.resolve() not in target.parents:
            raise CourseEditorError("Nom de fichier invalide")
        target.write_bytes(content)
        return "/" + target.relative_to(FRONTEND_PUBLIC).as_posix()


admin_course_service = AdminCourseService()
