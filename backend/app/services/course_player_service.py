"""Published course-deck loader and low-stakes slide evaluation.

The student runtime only receives verified/published audio.  Correct answers
remain server-side.  A version-controlled local manifest is used as a safe
fallback while the additive database migration is being deployed.
"""

from __future__ import annotations

import copy
import hashlib
import json
import logging
import re
import unicodedata
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

from app.supabase_client import get_supabase_admin
from app.services.schema_catalog import SCHEMA_IDS
from app.services.scientific_visual_skill import normalize_scientific_visual
from app.services.subject_access_service import subject_access_service


_log = logging.getLogger(__name__)
_DATA_DIR = Path(__file__).resolve().parents[2] / "data" / "courses"
_LOCAL_MANIFESTS = tuple(sorted(_DATA_DIR.glob("*_course_v1.json")))


def _is_uuid(value: Any) -> bool:
    try:
        uuid.UUID(str(value))
        return True
    except (TypeError, ValueError, AttributeError):
        return False


def _normalise(value: Any) -> str:
    text = str(value or "").strip().casefold()
    text = "".join(ch for ch in unicodedata.normalize("NFD", text)
                   if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", text)


def _search_normalise(value: Any) -> str:
    """Normalisation stricte pour rechercher un thème dans une demande libre."""
    return re.sub(r"[^a-z0-9]+", " ", _normalise(value)).strip()


def _is_explicit_course_request(value: Any) -> bool:
    """Ne détourne pas une question courte vers un parcours de plusieurs heures."""
    text = _search_normalise(value)
    if not text:
        return False
    return bool(re.search(
        r"\b(cours|cour|curs|lecon|chapitre|apprendre|etudier|reviser|revision|commencer|demarrer|lancer|suivre)\b",
        text,
    ))


class CoursePlayerService:
    def __init__(self) -> None:
        self._manifest_cache: Optional[list[dict]] = None

    def _load_local_manifests(self) -> list[dict]:
        if self._manifest_cache is not None:
            return copy.deepcopy(self._manifest_cache)
        self._manifest_cache = [
            json.loads(path.read_text(encoding="utf-8"))
            for path in _LOCAL_MANIFESTS
            if path.exists()
        ]
        return copy.deepcopy(self._manifest_cache)

    def _load_local_manifest(self, lesson_title: str = "") -> Optional[dict]:
        manifests = self._load_local_manifests()
        if not manifests:
            return None
        normalised_title = _normalise(lesson_title)
        for manifest in manifests:
            if any(_normalise(token) in normalised_title for token in manifest.get("lesson_match", [])):
                return manifest
        return manifests[0] if not lesson_title else None

    def match_manifest_intent(self, text: str) -> Optional[dict]:
        """Associe une demande explicite de cours à un seul manifest local."""
        return self._rank_course_intent(text, self._load_local_manifests())

    @staticmethod
    def _rank_course_intent(text: str, candidates: list[dict]) -> Optional[dict]:
        if not _is_explicit_course_request(text):
            return None
        query = f" {_search_normalise(text)} "
        ranked: list[tuple[int, dict]] = []
        for candidate in candidates:
            aliases = candidate.get("intent_aliases") or []
            scores = []
            for alias in aliases:
                normalised_alias = _search_normalise(alias)
                if normalised_alias and f" {normalised_alias} " in query:
                    # Une expression spécifique doit l'emporter sur un mot
                    # partagé comme ATP ou muscle.
                    scores.append(len(normalised_alias.split()) * 100 + len(normalised_alias))
            if scores:
                ranked.append((max(scores), candidate))
        if not ranked:
            return None
        ranked.sort(key=lambda item: item[0], reverse=True)
        if len(ranked) > 1 and ranked[0][0] == ranked[1][0]:
            return None
        return ranked[0][1]

    def match_course_intent(self, text: str) -> Optional[dict]:
        """Include courses authored and published from the admin dashboard."""
        if not _is_explicit_course_request(text):
            return None
        candidates_by_stable = {
            str(item.get("stable_id") or item.get("id")): item
            for item in self._load_local_manifests()
        }
        try:
            rows = get_supabase_admin().table("course_decks").select(
                "id,lesson_id,title,status,metadata"
            ).eq("status", "published").execute().data or []
            for row in rows:
                metadata = row.get("metadata") or {}
                stable_id = str(metadata.get("stable_id") or row.get("id"))
                candidates_by_stable[stable_id] = {
                    "id": stable_id,
                    "stable_id": stable_id,
                    "title": row.get("title") or "Cours",
                    "intent_aliases": metadata.get("intent_aliases") or [row.get("title") or ""],
                    "lesson_match": metadata.get("lesson_match") or [row.get("title") or ""],
                    "_deck_id": str(row.get("id") or ""),
                    "_lesson_id": str(row.get("lesson_id") or ""),
                    "_source": "database",
                }
        except Exception as exc:
            _log.info("[CoursePlayer] Admin-authored intent catalogue unavailable: %s", exc)
        return self._rank_course_intent(text, list(candidates_by_stable.values()))

    @staticmethod
    def _chapter_from_lesson(lesson: dict) -> dict:
        chapter = lesson.get("chapters") or {}
        if isinstance(chapter, list):
            return chapter[0] if chapter else {}
        return chapter

    @staticmethod
    def _subject_from_chapter(chapter: dict) -> dict:
        subject = chapter.get("subjects") or {}
        if isinstance(subject, list):
            return subject[0] if subject else {}
        return subject

    @staticmethod
    def _manifest_matches_lesson(manifest: dict, lesson: dict) -> bool:
        chapter = CoursePlayerService._chapter_from_lesson(lesson)
        title_blob = _search_normalise(" ".join([
            str(lesson.get("title_fr") or ""),
            str(chapter.get("title_fr") or ""),
        ]))
        return any(
            token and token in title_blob
            for token in (
                _search_normalise(value)
                for value in manifest.get("lesson_match") or []
            )
        )

    async def get_catalog(self, student: dict) -> dict:
        """Return the student's subject folders and their authored courses.

        Published database versions authored from the admin dashboard take
        precedence over manifests. A manifest remains the deployment fallback
        until its first database version is published.
        """
        context = subject_access_service.get_context(student)
        subjects = [
            {
                "id": str(subject.get("id") or ""),
                "name_fr": subject.get("name_fr") or "Matière",
                "name_ar": subject.get("name_ar") or "",
                "icon": subject.get("icon"),
                "color": subject.get("color"),
                "catalog_key": subject.get("catalog_key") or "",
                "course_count": 0,
                "courses": [],
            }
            for subject in context.get("subjects") or []
        ]
        folders_by_id = {folder["id"]: folder for folder in subjects}

        try:
            admin = get_supabase_admin()
            lessons = admin.table("lessons").select(
                "id,title_fr,chapter_id,chapters(id,title_fr,subject_id,subjects(id,name_fr,name_ar))"
            ).execute().data or []
        except Exception as exc:
            _log.warning("[CoursePlayer] Course library unavailable: %s", exc)
            return {"subjects": subjects, "total_courses": 0}

        allowed_lessons = [
            lesson for lesson in lessons
            if str(self._chapter_from_lesson(lesson).get("subject_id") or "") in folders_by_id
        ]

        try:
            deck_rows = admin.table("course_decks").select(
                "id,lesson_id,title,status,version,estimated_minutes,metadata"
            ).execute().data or []
            deck_ids = [row["id"] for row in deck_rows]
            activity_rows = []
            if deck_ids:
                activity_rows = admin.table("course_activities").select(
                    "id,deck_id"
                ).in_("deck_id", deck_ids).execute().data or []
            activity_ids = [row["id"] for row in activity_rows]
            slide_rows = []
            if activity_ids:
                slide_rows = admin.table("course_slides").select(
                    "id,activity_id"
                ).in_("activity_id", activity_ids).execute().data or []
        except Exception as exc:
            _log.info("[CoursePlayer] Course deck metadata unavailable for library: %s", exc)
            deck_rows = []
            activity_rows = []
            slide_rows = []

        activity_ids_by_deck: dict[str, set[str]] = {}
        for activity in activity_rows:
            activity_ids_by_deck.setdefault(str(activity.get("deck_id")), set()).add(str(activity.get("id")))
        slide_count_by_deck: dict[str, int] = {}
        for deck_id, ids in activity_ids_by_deck.items():
            slide_count_by_deck[deck_id] = sum(
                1 for slide in slide_rows if str(slide.get("activity_id")) in ids
            )

        published_rows = [row for row in deck_rows if row.get("status") == "published"]
        handled_database_ids: set[str] = set()

        for manifest in self._load_local_manifests():
            stable_id = manifest.get("stable_id") or manifest.get("id")
            linked_rows = [
                row for row in published_rows
                if (row.get("metadata") or {}).get("stable_id") == stable_id
            ]
            linked_rows.sort(
                key=lambda row: (row.get("status") == "published", int(row.get("version") or 0)),
                reverse=True,
            )

            lesson = None
            deck_row = None
            for row in linked_rows:
                candidate = next(
                    (item for item in allowed_lessons if str(item.get("id")) == str(row.get("lesson_id"))),
                    None,
                )
                if candidate:
                    lesson = candidate
                    deck_row = row
                    handled_database_ids.add(str(row.get("id")))
                    break
            if lesson is None:
                lesson = next(
                    (item for item in allowed_lessons if self._manifest_matches_lesson(manifest, item)),
                    None,
                )
            if lesson is None:
                continue

            chapter = self._chapter_from_lesson(lesson)
            subject_id = str(chapter.get("subject_id") or "")
            folder = folders_by_id.get(subject_id)
            if not folder:
                continue

            deck_id = str((deck_row or {}).get("id") or manifest.get("id") or "")
            if deck_row:
                metadata = deck_row.get("metadata") or {}
                activity_count = len(activity_ids_by_deck.get(deck_id, set()))
                slide_count = slide_count_by_deck.get(deck_id, 0)
                catalog = metadata.get("catalog") or manifest.get("catalog") or {}
                course_title = deck_row.get("title") or manifest.get("title") or lesson.get("title_fr") or "Cours"
                estimated_minutes = int(deck_row.get("estimated_minutes") or manifest.get("estimated_minutes") or 0)
            else:
                activity_count = len(manifest.get("activities") or [])
                slide_count = sum(
                    len(activity.get("slides") or [])
                    for activity in manifest.get("activities") or []
                )
                catalog = manifest.get("catalog") or {}
                course_title = manifest.get("title") or lesson.get("title_fr") or "Cours"
                estimated_minutes = int(manifest.get("estimated_minutes") or 0)
            progress = await self.get_progress(str(student.get("id") or ""), deck_id)
            completed_slide_ids = (progress or {}).get("completed_slide_ids") or []
            progress_percent = (
                min(100, round(len(completed_slide_ids) * 100 / slide_count))
                if slide_count else 0
            )

            folder["courses"].append({
                "stable_id": stable_id,
                "deck_id": deck_id,
                "title": course_title,
                "summary": catalog.get("summary") or "Parcours interactif guidé par Moalim.",
                "cover_image": catalog.get("cover_image"),
                "cover_alt": catalog.get("cover_alt") or course_title or "Illustration du cours",
                "essential_topics": catalog.get("essential_topics") or [],
                "chapter_id": str(lesson.get("chapter_id") or chapter.get("id") or ""),
                "chapter_title": chapter.get("title_fr") or "",
                "lesson_id": str(lesson.get("id") or ""),
                "lesson_title": lesson.get("title_fr") or "",
                "activity_count": activity_count,
                "slide_count": slide_count,
                "estimated_minutes": estimated_minutes,
                "progress_status": (progress or {}).get("status") or "not_started",
                "progress_percent": progress_percent,
                "tutor_request": f"Je veux commencer le cours sur {course_title}",
            })

        # Courses created entirely from the admin editor have no local
        # manifest. They still appear in the same subject folders and use the
        # aliases stored in deck metadata for tutor routing.
        for deck_row in published_rows:
            deck_id = str(deck_row.get("id") or "")
            if deck_id in handled_database_ids:
                continue
            lesson = next(
                (item for item in allowed_lessons if str(item.get("id")) == str(deck_row.get("lesson_id"))),
                None,
            )
            if not lesson:
                continue
            chapter = self._chapter_from_lesson(lesson)
            folder = folders_by_id.get(str(chapter.get("subject_id") or ""))
            if not folder:
                continue
            metadata = deck_row.get("metadata") or {}
            stable_id = metadata.get("stable_id") or deck_id
            catalog = metadata.get("catalog") or {}
            activity_count = len(activity_ids_by_deck.get(deck_id, set()))
            slide_count = slide_count_by_deck.get(deck_id, 0)
            progress = await self.get_progress(str(student.get("id") or ""), deck_id)
            completed_slide_ids = (progress or {}).get("completed_slide_ids") or []
            progress_percent = min(100, round(len(completed_slide_ids) * 100 / slide_count)) if slide_count else 0
            title = deck_row.get("title") or lesson.get("title_fr") or "Cours"
            folder["courses"].append({
                "stable_id": stable_id,
                "deck_id": deck_id,
                "title": title,
                "summary": catalog.get("summary") or "Parcours interactif guidé par Moalim.",
                "cover_image": catalog.get("cover_image"),
                "cover_alt": catalog.get("cover_alt") or title,
                "essential_topics": catalog.get("essential_topics") or [],
                "chapter_id": str(lesson.get("chapter_id") or chapter.get("id") or ""),
                "chapter_title": chapter.get("title_fr") or "",
                "lesson_id": str(lesson.get("id") or ""),
                "lesson_title": lesson.get("title_fr") or "",
                "activity_count": activity_count,
                "slide_count": slide_count,
                "estimated_minutes": int(deck_row.get("estimated_minutes") or 0),
                "progress_status": (progress or {}).get("status") or "not_started",
                "progress_percent": progress_percent,
                "tutor_request": f"Je veux commencer le cours sur {title}",
            })

        for folder in subjects:
            folder["courses"].sort(key=lambda course: course["title"])
            folder["course_count"] = len(folder["courses"])
        return {
            "subjects": subjects,
            "total_courses": sum(folder["course_count"] for folder in subjects),
        }

    async def resolve_course_intent(self, text: str, student: dict) -> dict:
        """Résout une demande naturelle vers une route de cours autorisée."""
        manifest = self.match_course_intent(text)
        if not manifest:
            return {"matched": False, "reason": "not_a_known_course_request"}

        stable_id = manifest.get("stable_id") or manifest["id"]
        try:
            admin = get_supabase_admin()
        except Exception as exc:
            _log.warning("[CoursePlayer] Course catalogue unavailable: %s", exc)
            return {
                "matched": False,
                "reason": "course_catalogue_unavailable",
                "requested_course": manifest.get("title"),
            }
        lesson: Optional[dict] = None
        select = "id,title_fr,chapter_id,chapters(id,title_fr,subject_id,subjects(name_fr))"

        # An admin-authored course already knows its exact lesson. This avoids
        # relying on fuzzy title matching after an editorial rename.
        direct_lesson_id = str(manifest.get("_lesson_id") or "")
        if direct_lesson_id:
            try:
                result = admin.table("lessons").select(select).eq(
                    "id", direct_lesson_id
                ).limit(1).execute()
                candidate = result.data[0] if result.data else None
                if candidate and subject_access_service.is_lesson_allowed(student, candidate["id"]):
                    lesson = candidate
            except Exception as exc:
                _log.info("[CoursePlayer] Direct admin course lesson unavailable: %s", exc)

        # Après synchronisation, la métadonnée du deck fournit la liaison la
        # plus fiable, même si le titre éditorial de la leçon change.
        try:
            deck_rows = admin.table("course_decks").select(
                "lesson_id,status,metadata"
            ).execute().data or []
            matching_decks = [
                row for row in deck_rows
                if (row.get("metadata") or {}).get("stable_id") == stable_id
            ]
            matching_decks.sort(key=lambda row: row.get("status") == "published", reverse=True)
            for row in matching_decks if lesson is None else []:
                result = admin.table("lessons").select(select).eq(
                    "id", row["lesson_id"]
                ).limit(1).execute()
                candidate = result.data[0] if result.data else None
                if candidate and subject_access_service.is_lesson_allowed(student, candidate["id"]):
                    lesson = candidate
                    break
        except Exception as exc:
            _log.info("[CoursePlayer] Deck intent metadata unavailable: %s", exc)

        # Repli avant la première synchronisation : rapprochement contrôlé sur
        # le titre de la leçon et du chapitre.
        if lesson is None:
            try:
                lessons = admin.table("lessons").select(select).execute().data or []
                match_tokens = [_search_normalise(value) for value in manifest.get("lesson_match") or []]
                for candidate in lessons:
                    chapter = self._chapter_from_lesson(candidate)
                    title_blob = _search_normalise(" ".join([
                        str(candidate.get("title_fr") or ""),
                        str(chapter.get("title_fr") or ""),
                    ]))
                    if any(token and token in title_blob for token in match_tokens):
                        if subject_access_service.is_lesson_allowed(student, candidate["id"]):
                            lesson = candidate
                            break
            except Exception as exc:
                _log.warning("[CoursePlayer] Cannot resolve requested course: %s", exc)

        if lesson is None:
            return {
                "matched": False,
                "reason": "course_not_linked_to_a_lesson",
                "requested_course": manifest.get("title"),
            }

        deck = await self.get_deck(str(lesson["id"]))
        if not deck:
            return {
                "matched": False,
                "reason": "course_not_available",
                "requested_course": manifest.get("title"),
            }
        resolved_stable_id = deck.get("stable_id") or (deck.get("metadata") or {}).get("stable_id")
        if resolved_stable_id and resolved_stable_id != stable_id:
            return {
                "matched": False,
                "reason": "course_mapping_mismatch",
                "requested_course": manifest.get("title"),
            }

        chapter = self._chapter_from_lesson(lesson)
        subject = self._subject_from_chapter(chapter)
        return {
            "matched": True,
            "reason": "matched",
            "chapter_id": str(lesson["chapter_id"]),
            "lesson_id": str(lesson["id"]),
            "lesson_title": lesson.get("title_fr") or manifest.get("title"),
            "chapter_title": chapter.get("title_fr") or "",
            "subject_name": subject.get("name_fr") or "",
            "deck_id": str(deck.get("id") or ""),
            "deck_title": deck.get("title") or manifest.get("title"),
        }

    @staticmethod
    def _public_visual(visual: Any) -> Any:
        """Le visuel tel que le navigateur a le droit de le recevoir.

        Une figure `scientific` traverse le MÊME normaliseur que celles du
        tableau du tuteur : bornes, moteurs et expressions autorisés y sont
        déjà décidés une fois pour toutes. Un deck mal formé — ou trafiqué —
        n'envoie donc pas au navigateur une spec que les moteurs n'attendent
        pas ; il perd simplement sa figure, et la diapositive retombe sur son
        texte essentiel.

        Un `schema_id` absent de la bibliothèque est signalé ici plutôt que
        découvert par l'élève devant un cadre vide.
        """
        if not isinstance(visual, dict):
            return visual
        kind = visual.get("kind")
        if kind == "scientific":
            visual["scientific"] = normalize_scientific_visual(visual.get("scientific"))
            if visual["scientific"] is None:
                _log.warning("Slide visual 'scientific' rejected by the normaliser")
        elif kind == "schema" and visual.get("schema_id") not in SCHEMA_IDS:
            _log.warning("Slide visual references unknown schema_id=%r", visual.get("schema_id"))
        return visual

    @staticmethod
    def _public_slide(slide: dict, audio_assets: list[dict]) -> dict:
        public = copy.deepcopy(slide)
        if public.get("visual") is not None:
            public["visual"] = CoursePlayerService._public_visual(public["visual"])
        question = public.get("question") or {}
        for secret in ("answer_key", "accepted_answers", "evaluation_regex"):
            question.pop(secret, None)
        public["question"] = question
        speech_text = slide.get("speech_text") or {}

        def is_current(audio: dict) -> bool:
            language = audio.get("language") or "fr"
            speech = speech_text.get(language) or speech_text.get("fr") or ""
            expected_hash = hashlib.sha256(speech.strip().encode("utf-8")).hexdigest()
            return bool(speech) and audio.get("speech_hash") == expected_hash

        public["audio"] = {
            audio["language"]: {
                "url": audio["file_path"],
                "duration_ms": audio.get("duration_ms"),
                "version": audio.get("version", 1),
                "speech_hash": audio.get("speech_hash"),
                "status": audio.get("status"),
            }
            for audio in audio_assets
            if audio.get("status") == "published" and audio.get("file_path") and is_current(audio)
        }
        return public

    async def get_deck(self, lesson_id: str) -> Optional[dict]:
        """Return the latest published deck, or the matching local manifest."""
        try:
            admin = get_supabase_admin()
            deck_result = (
                admin.table("course_decks")
                .select("*")
                .eq("lesson_id", lesson_id)
                .eq("status", "published")
                .order("version", desc=True)
                .limit(1)
                .execute()
            )
            if deck_result.data:
                deck = deck_result.data[0]
                activities = (
                    admin.table("course_activities")
                    .select("*")
                    .eq("deck_id", deck["id"])
                    .order("order_index")
                    .execute()
                ).data or []
                activity_ids = [a["id"] for a in activities]
                slides = []
                if activity_ids:
                    slides = (
                        admin.table("course_slides")
                        .select("*")
                        .in_("activity_id", activity_ids)
                        .order("order_index")
                        .execute()
                    ).data or []
                slide_ids = [s["id"] for s in slides]
                audio_rows = []
                if slide_ids:
                    audio_rows = (
                        admin.table("course_slide_audio")
                        .select("*")
                        .in_("slide_id", slide_ids)
                        .eq("status", "published")
                        .execute()
                    ).data or []
                audio_by_slide: dict[str, list[dict]] = {}
                for audio in audio_rows:
                    audio_by_slide.setdefault(audio["slide_id"], []).append(audio)
                slides_by_activity: dict[str, list[dict]] = {}
                for slide in slides:
                    slides_by_activity.setdefault(slide["activity_id"], []).append(
                        self._public_slide(slide, audio_by_slide.get(slide["id"], []))
                    )
                deck["activities"] = [
                    {**activity, "slides": slides_by_activity.get(activity["id"], [])}
                    for activity in activities
                ]
                deck["source"] = "database"
                return deck
        except Exception as exc:
            _log.info("[CoursePlayer] Published deck unavailable, using manifest fallback: %s", exc)

        title_blob = ""
        try:
            admin = get_supabase_admin()
            lesson_result = admin.table("lessons").select("title_fr, chapter_id, chapters(title_fr)").eq(
                "id", lesson_id
            ).limit(1).execute()
            lesson = lesson_result.data[0] if lesson_result.data else {}
            title_blob = " ".join([
                str(lesson.get("title_fr") or ""),
                str((lesson.get("chapters") or {}).get("title_fr") or ""),
            ])
        except Exception:
            # The REST endpoint already checked lesson access.  During local
            # development the manifest remains useful even if Supabase is down.
            title_blob = ""
        manifest = self._load_local_manifest(title_blob)
        if not manifest:
            return None
        manifest["lesson_id"] = lesson_id
        manifest["source"] = "manifest"
        for activity in manifest.get("activities", []):
            for slide in activity.get("slides", []):
                slide.setdefault("audio", {})
                slide["question"] = {
                    k: v for k, v in (slide.get("question") or {}).items()
                    if k not in {"answer_key", "accepted_answers", "evaluation_regex"}
                }
        return manifest

    def _find_local_slide(self, slide_id: str) -> Optional[dict]:
        for manifest in self._load_local_manifests():
            for activity in manifest.get("activities", []):
                for slide in activity.get("slides", []):
                    if slide.get("id") == slide_id or slide.get("stable_id") == slide_id:
                        return slide
        return None

    async def evaluate_attempt(self, payload: dict) -> tuple[Optional[bool], str, bool]:
        if payload.get("outcome") in {"skipped_timeout", "skipped_manual", "interrupted"}:
            return None, "Réponse non fournie : la notion sera reproposée plus tard.", True

        question: dict = {}
        slide_id = payload.get("slide_id")
        if _is_uuid(slide_id):
            try:
                result = get_supabase_admin().table("course_slides").select("question").eq(
                    "id", slide_id
                ).limit(1).execute()
                if result.data:
                    question = result.data[0].get("question") or {}
            except Exception as exc:
                _log.warning("[CoursePlayer] Cannot load slide answer key: %s", exc)
        else:
            slide = self._find_local_slide(str(slide_id)) or {}
            question = slide.get("question") or {}

        answer = payload.get("answer")
        qtype = question.get("type", "open")
        answer_key = question.get("answer_key")
        accepted = question.get("accepted_answers") or []
        is_correct: Optional[bool]
        if qtype in {"qcm", "prediction", "true_false", "select", "association"} and answer_key is not None:
            is_correct = _normalise(answer) == _normalise(answer_key)
        elif qtype == "ordering" and isinstance(answer, list) and isinstance(answer_key, list):
            is_correct = [_normalise(v) for v in answer] == [_normalise(v) for v in answer_key]
        elif accepted:
            is_correct = _normalise(answer) in {_normalise(v) for v in accepted}
        else:
            is_correct = None

        if is_correct is True:
            return True, question.get("feedback_correct") or "Bonne réponse : ton observation est cohérente.", False
        if is_correct is False:
            return False, question.get("feedback_incorrect") or "Observe à nouveau le document ; cette notion sera reprise.", True
        return None, "Réponse enregistrée. Le tuteur pourra vérifier ton raisonnement.", False

    async def save_attempt(self, student_id: str, payload: dict, is_correct: Optional[bool], feedback: str) -> None:
        if not _is_uuid(payload.get("slide_id")):
            return
        try:
            get_supabase_admin().table("course_slide_attempts").insert({
                "student_id": student_id,
                "slide_id": payload["slide_id"],
                "answer": {"value": payload.get("answer")},
                "is_correct": is_correct,
                "outcome": payload.get("outcome", "answered"),
                "response_time_ms": payload.get("response_time_ms"),
                "confidence": payload.get("confidence"),
                "feedback": {"message": feedback},
            }).execute()
        except Exception as exc:
            _log.warning("[CoursePlayer] Attempt persistence failed: %s", exc)

    async def save_progress(self, student_id: str, payload: dict) -> bool:
        if not _is_uuid(payload.get("deck_id")):
            return False
        try:
            data = {
                "student_id": student_id,
                "deck_id": payload["deck_id"],
                "current_activity_id": payload.get("activity_id") if _is_uuid(payload.get("activity_id")) else None,
                "current_slide_id": payload.get("slide_id") if _is_uuid(payload.get("slide_id")) else None,
                "audio_position_ms": payload.get("audio_position_ms", 0),
                "slide_state": payload.get("slide_state") or {},
                "completed_slide_ids": payload.get("completed_slide_ids") or [],
                "status": payload.get("status", "in_progress"),
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
            get_supabase_admin().table("course_progress").upsert(
                data, on_conflict="student_id,deck_id"
            ).execute()
            return True
        except Exception as exc:
            _log.warning("[CoursePlayer] Progress persistence failed: %s", exc)
            return False

    async def get_progress(self, student_id: str, deck_id: str) -> Optional[dict]:
        if not _is_uuid(deck_id):
            return None
        try:
            result = get_supabase_admin().table("course_progress").select("*").eq(
                "student_id", student_id
            ).eq("deck_id", deck_id).limit(1).execute()
            return result.data[0] if result.data else None
        except Exception as exc:
            _log.warning("[CoursePlayer] Progress load failed: %s", exc)
            return None

    async def mark_lesson_complete(self, student_id: str, lesson_id: str) -> None:
        """Keep the existing lesson selector aligned with deck completion."""
        try:
            from app.services.session_progress_service import session_progress_service

            existing = await session_progress_service.get_lesson_progress(student_id, lesson_id)
            objectives_total = max(1, int((existing or {}).get("objectives_total") or 1))
            await session_progress_service.create_or_update_progress(
                student_id=student_id,
                lesson_id=lesson_id,
                objectives_total=objectives_total,
                objectives_completed=list(range(objectives_total)),
                current_objective_index=objectives_total,
                topics_covered=(existing or {}).get("topics_covered") or [],
                key_points_learned=(existing or {}).get("key_points_learned") or [],
                last_ai_summary=(existing or {}).get("last_ai_summary") or "Parcours interactif terminé.",
                status="completed",
            )
        except Exception as exc:
            _log.warning("[CoursePlayer] Legacy lesson completion sync failed: %s", exc)


course_player_service = CoursePlayerService()
