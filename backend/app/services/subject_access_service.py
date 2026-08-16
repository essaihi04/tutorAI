"""Central subject entitlements for student-facing features.

The application historically exposed every subject to every authenticated
student.  ``subject_access_managed`` lets us migrate progressively:

* false / missing: exact legacy behaviour (all current subjects);
* true: strict access from ``student_subject_access``.

All catalogue filtering and authorization should go through this service so
the UI, tutoring sessions, diagnostics and exams share the same rules.
"""

from __future__ import annotations

from datetime import datetime, timezone
import logging
import unicodedata
from typing import Any, Iterable, Optional

logger = logging.getLogger(__name__)


def _plain(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value or "")
    return "".join(ch for ch in normalized if not unicodedata.combining(ch)).lower()


def canonical_subject_key(value: str) -> str:
    """Map database and exam labels to a stable product key."""
    text = _plain(value).replace("_", " ").replace("-", " ")
    compact = "".join(ch for ch in text if ch.isalnum())

    if "svt" in compact or "sciencesdelavieetdelaterre" in compact:
        return "svt"
    if "math" in compact:
        return "mathematiques"
    if "physiquechimie" in compact or compact in {"pc", "physiqueetchemie"}:
        return "physique-chimie"
    if "physique" in compact or compact == "phys":
        return "physique"
    if "chimie" in compact or compact == "chim":
        return "chimie"
    if "anglais" in compact or "english" in compact:
        return "anglais"
    if "philosoph" in compact:
        return "philosophie"
    if "francais" in compact:
        return "francais"
    return compact


def build_exam_subject_keys(subjects: Iterable[dict[str, Any]]) -> list[str]:
    """Return exam catalogue keys enabled by a set of content subjects.

    Physique-Chimie is a combined BAC exam.  It is enabled only when both
    content subjects are present (or when a future combined subject exists).
    """
    keys = {canonical_subject_key(str(subject.get("name_fr") or "")) for subject in subjects}
    keys.discard("")

    if "physique" in keys and "chimie" in keys:
        keys.add("physique-chimie")

    order = [
        "mathematiques",
        "physique-chimie",
        "physique",
        "chimie",
        "svt",
        "anglais",
        "philosophie",
        "francais",
    ]
    return [key for key in order if key in keys] + sorted(keys.difference(order))


def is_exam_subject_allowed(exam_subject: str, allowed_exam_keys: Iterable[str]) -> bool:
    return canonical_subject_key(exam_subject) in set(allowed_exam_keys)


class SubjectAccessService:
    def __init__(self, client=None):
        self._client = client

    @property
    def client(self):
        if self._client is None:
            from app.supabase_client import get_supabase_admin

            self._client = get_supabase_admin()
        return self._client

    @staticmethod
    def _is_active_access(row: dict[str, Any]) -> bool:
        if row.get("status") != "active":
            return False

        now = datetime.now(timezone.utc)
        for field, must_be_before_now in (("starts_at", True), ("ends_at", False)):
            raw = row.get(field)
            if not raw:
                continue
            try:
                parsed = datetime.fromisoformat(str(raw).replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                if must_be_before_now and parsed > now:
                    return False
                if not must_be_before_now and parsed <= now:
                    return False
            except (TypeError, ValueError):
                logger.warning("Invalid %s on student subject access row", field)
                return False
        return True

    def _all_subjects(self) -> list[dict[str, Any]]:
        result = self.client.table("subjects").select("*").order("order_index").execute()
        return result.data or []

    def _filiere_subject_ids(self, filiere: str) -> Optional[set[str]]:
        """Return None when the multi-filiere migration is not available."""
        if not filiere:
            return None
        try:
            result = self.client.table("subjects_filieres").select("subject_id").eq(
                "filiere_code", filiere
            ).execute()
            rows = result.data or []
            if not rows:
                return None
            return {str(row["subject_id"]) for row in rows if row.get("subject_id")}
        except Exception as exc:
            logger.info("Filiere subject mapping unavailable: %s", exc)
            return None

    def _managed_subject_ids(self, student_id: str) -> set[str]:
        try:
            result = self.client.table("student_subject_access").select(
                "subject_id,status,starts_at,ends_at"
            ).eq("student_id", student_id).execute()
        except Exception as exc:
            # A student explicitly placed in managed mode must fail closed.
            logger.error("Managed subject access unavailable for %s: %s", student_id, exc)
            return set()

        return {
            str(row["subject_id"])
            for row in (result.data or [])
            if row.get("subject_id") and self._is_active_access(row)
        }

    def get_context(self, student: dict[str, Any]) -> dict[str, Any]:
        all_subjects = self._all_subjects()
        filiere = str(student.get("filiere") or "SP")
        managed = bool(student.get("subject_access_managed", False))
        filiere_ids = self._filiere_subject_ids(filiere)

        if managed:
            allowed_ids = self._managed_subject_ids(str(student["id"]))
            if filiere_ids is not None:
                allowed_ids &= filiere_ids
            access_mode = "managed"
        else:
            # Exact backward-compatible path: the old frontend requested
            # /content/subjects without a filiere and therefore received all
            # subjects. No existing account changes until an admin explicitly
            # activates managed access for it.
            allowed_ids = {str(subject["id"]) for subject in all_subjects}
            access_mode = "legacy"

        subjects = [subject for subject in all_subjects if str(subject.get("id")) in allowed_ids]
        exam_subject_keys = build_exam_subject_keys(subjects)

        enriched_subjects = [
            {**subject, "catalog_key": canonical_subject_key(str(subject.get("name_fr") or ""))}
            for subject in subjects
        ]
        return {
            "student_id": str(student["id"]),
            "filiere": filiere,
            "access_mode": access_mode,
            "subjects": enriched_subjects,
            "subject_ids": [str(subject["id"]) for subject in subjects],
            "subject_names": [str(subject.get("name_fr") or "") for subject in subjects],
            "exam_subject_keys": exam_subject_keys,
            "primary_subject_id": str(subjects[0]["id"]) if subjects else None,
        }

    def get_context_for_student_id(self, student_id: str) -> dict[str, Any]:
        result = self.client.table("students").select("*").eq("id", student_id).limit(1).execute()
        if not result.data:
            return {
                "student_id": student_id,
                "filiere": None,
                "access_mode": "managed",
                "subjects": [],
                "subject_ids": [],
                "subject_names": [],
                "exam_subject_keys": [],
                "primary_subject_id": None,
            }
        return self.get_context(result.data[0])

    def is_subject_id_allowed(self, student: dict[str, Any], subject_id: str) -> bool:
        return str(subject_id) in set(self.get_context(student)["subject_ids"])

    def is_chapter_allowed(self, student: dict[str, Any], chapter_id: str) -> bool:
        result = self.client.table("chapters").select("subject_id").eq("id", chapter_id).limit(1).execute()
        if not result.data:
            return False
        return self.is_subject_id_allowed(student, str(result.data[0]["subject_id"]))

    def is_lesson_allowed(self, student: dict[str, Any], lesson_id: str) -> bool:
        result = self.client.table("lessons").select("chapter_id").eq("id", lesson_id).limit(1).execute()
        if not result.data:
            return False
        return self.is_chapter_allowed(student, str(result.data[0]["chapter_id"]))

    def is_exam_allowed(self, student: dict[str, Any], exam_subject: str) -> bool:
        context = self.get_context(student)
        return is_exam_subject_allowed(exam_subject, context["exam_subject_keys"])


subject_access_service = SubjectAccessService()
