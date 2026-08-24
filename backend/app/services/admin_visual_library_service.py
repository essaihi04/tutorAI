"""Unified catalogue and CRUD operations for admin scientific visuals."""

from __future__ import annotations

import copy
import json
import re
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.schemas.admin_visual_library import AdminVisualItemCreate, AdminVisualItemUpdate
from app.services.admin_course_service import FRONTEND_PUBLIC, admin_course_service
from app.services.schema_catalog import SCHEMA_CATALOG, match_schema
from app.services.scientific_presets import SCIENTIFIC_PRESETS
from app.services.scientific_visual_skill import (
    MITOCHONDRION_3D_FALLBACK_PATH,
    MITOCHONDRION_3D_SPEC,
    SCIENTIFIC_VISUAL_PROMPT,
    normalize_scientific_visual,
    scientific_visual_quality,
)
from app.supabase_client import get_supabase_admin


_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}
_VISUAL_RESOURCE_TYPES = {"image", "video", "simulation"}
_STATUSES = {"draft", "validated", "published", "archived"}
_INLINE_HTML_KEYS = ("html", "content", "simulation_html")
_MAX_INLINE_HTML_BYTES = 2 * 1024 * 1024


class VisualLibraryError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _data(result: Any) -> list[dict]:
    return list(getattr(result, "data", None) or [])


def _metadata(value: Any) -> dict[str, Any]:
    return copy.deepcopy(value) if isinstance(value, dict) else {}


def _resource_url(row: dict[str, Any]) -> str:
    return str(row.get("file_path") or row.get("external_url") or "")


def _metadata_html(metadata: dict[str, Any]) -> str:
    for key in _INLINE_HTML_KEYS:
        value = metadata.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def extract_llm_json(raw: str) -> dict[str, Any]:
    """Extract one JSON object without accepting trailing prose as payload."""

    text = (raw or "").strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    start = text.find("{")
    if start < 0:
        raise VisualLibraryError("Le modèle n'a retourné aucun objet JSON.")
    try:
        value, _ = json.JSONDecoder().raw_decode(text[start:])
    except json.JSONDecodeError as exc:
        raise VisualLibraryError("Le JSON généré par le modèle est invalide.") from exc
    if not isinstance(value, dict):
        raise VisualLibraryError("Le modèle doit retourner un objet JSON.")
    return value


def normalize_generated_result(value: dict[str, Any]) -> dict[str, Any]:
    scientific = value.get("scientific") if isinstance(value.get("scientific"), dict) else value
    normalized = normalize_scientific_visual(scientific)
    if normalized is None:
        raise VisualLibraryError("Le visuel généré ne respecte pas le contrat déclaratif.")
    quality = scientific_visual_quality(normalized)
    return {
        "title": str(value.get("title") or normalized.get("title") or "Visuel scientifique")[:180],
        "description": str(value.get("description") or "")[:1200],
        "scientific": normalized,
        "quality": quality,
    }


class AdminVisualLibraryService:
    def _admin(self):
        return get_supabase_admin()

    @staticmethod
    def _lesson_map(lessons: list[dict]) -> dict[str, dict]:
        return {str(item.get("id")): item for item in lessons}

    @staticmethod
    def _schema_items() -> list[dict[str, Any]]:
        labels = {
            "svt": "SVT",
            "physics": "Physique",
            "chemistry": "Chimie",
            "math": "Mathématiques",
        }
        return [
            {
                "id": f"schema:{entry['id']}",
                "catalog_id": entry["id"],
                "kind": "schema",
                "title": entry["title"],
                "description": "Schéma SVG validé et versionné dans le projet.",
                "subject": labels.get(entry.get("subject"), entry.get("subject") or ""),
                "subject_key": entry.get("subject") or "",
                "chapter": "",
                "lesson": "",
                "lesson_id": "",
                "concepts": list(entry.get("keywords") or [])[:12],
                "source": "core",
                "status": "validated",
                "editable": False,
                "deletable": False,
                "preview": {"kind": "schema", "schema_id": entry["id"]},
            }
            for entry in SCHEMA_CATALOG
        ]

    @staticmethod
    def _preset_items() -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for preset_id, definition in SCIENTIFIC_PRESETS.items():
            default_variant = str(definition["default_variant"])
            items.append({
                "id": f"preset:{preset_id}",
                "catalog_id": preset_id,
                "kind": "preset",
                "title": definition.get("title") or preset_id,
                "description": "Scène contrôlable validée : lecture, pause, étapes et variantes.",
                "subject": definition.get("subject") or "",
                "subject_key": "svt" if definition.get("subject") == "SVT" else "",
                "chapter": "Consommation de la matière organique",
                "lesson": "",
                "lesson_id": "",
                "concepts": list(definition.get("keywords") or []),
                "source": "core",
                "status": "validated",
                "editable": False,
                "deletable": False,
                "variants": sorted(definition["variants"]),
                "preview": {
                    "kind": "scientific",
                    "scientific": {
                        "engine": "preset",
                        "presetId": preset_id,
                        "variant": default_variant,
                        "autoplay": False,
                        "step": int(definition.get("max_step") or 0),
                    },
                },
            })
        return items

    @staticmethod
    def _resource_item(row: dict[str, Any], lesson: dict[str, Any]) -> dict[str, Any]:
        metadata = _metadata(row.get("metadata"))
        scientific = normalize_scientific_visual(metadata.get("scientific")) if isinstance(metadata.get("scientific"), dict) else None
        # Compatibilité avec la ressource historique montrée comme une
        # « Mitochondrie 3D » alors qu'elle n'était qu'un PNG. Elle devient
        # interactive dès le déploiement du code, même avant l'application de
        # la migration de données qui inscrit ce même contrat en métadonnées.
        if scientific is None and _resource_url(row) == MITOCHONDRION_3D_FALLBACK_PATH:
            scientific = normalize_scientific_visual(MITOCHONDRION_3D_SPEC)
        kind = "scientific" if scientific else str(row.get("resource_type") or "resource")
        status = str(metadata.get("library_status") or "published")
        if status not in _STATUSES:
            status = "published"
        preview: dict[str, Any] = {"kind": kind}
        url = _resource_url(row)
        if scientific:
            preview["scientific"] = scientific
        elif kind == "simulation" and url == "local:metadata" and _metadata_html(metadata):
            # The HTML can be large and must not be shipped with the complete
            # catalogue. The authenticated preview endpoint fetches it only
            # when an administrator opens this resource.
            preview["inline_html"] = True
        elif url and url != "local:metadata":
            preview["url"] = url
        else:
            preview["available"] = False
            preview["reason"] = (
                "Le contenu HTML enregistré dans les métadonnées est absent."
                if url == "local:metadata"
                else "Aucun média exploitable n'est associé à cette ressource."
            )
        return {
            "id": f"resource:{row.get('id')}",
            "resource_id": str(row.get("id") or ""),
            "kind": kind,
            "title": row.get("title") or "Ressource",
            "description": row.get("description") or "",
            "subject": lesson.get("subject_name") or "",
            "subject_key": lesson.get("subject_id") or "",
            "chapter": lesson.get("chapter_title") or "",
            "lesson": lesson.get("title") or "",
            "lesson_id": str(row.get("lesson_id") or ""),
            "section_title": row.get("section_title") or "",
            "concepts": list(row.get("concepts") or []),
            "source": metadata.get("library_source") or "database",
            "status": status,
            "editable": True,
            "deletable": True,
            "file_path": row.get("file_path"),
            "external_url": row.get("external_url"),
            "trigger_text": row.get("trigger_text"),
            "phase": row.get("phase") or "explanation",
            "difficulty_tier": row.get("difficulty_tier") or "intermediate",
            "version": int(metadata.get("library_version") or 1),
            "quality": metadata.get("quality"),
            "preview": preview,
        }

    @staticmethod
    def _filesystem_items(known_urls: set[str]) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        image_root = FRONTEND_PUBLIC / "media" / "images"
        if image_root.exists():
            for path in image_root.rglob("*"):
                if not path.is_file() or path.suffix.lower() not in _IMAGE_SUFFIXES:
                    continue
                url = "/" + path.relative_to(FRONTEND_PUBLIC).as_posix()
                if url in known_urls:
                    continue
                items.append({
                    "id": f"file:{url}", "kind": "image", "title": path.stem.replace("_", " "),
                    "description": "Fichier média non encore rattaché à une leçon.",
                    "subject": "", "subject_key": "", "chapter": "", "lesson": "", "lesson_id": "",
                    "concepts": [], "source": "filesystem", "status": "validated",
                    "editable": False, "deletable": False,
                    "preview": {"kind": "image", "url": url},
                })
        simulation_root = FRONTEND_PUBLIC / "media" / "simulations"
        if simulation_root.exists():
            for path in simulation_root.rglob("index.html"):
                url = "/" + path.relative_to(FRONTEND_PUBLIC).as_posix()
                if url in known_urls:
                    continue
                items.append({
                    "id": f"file:{url}", "kind": "simulation", "title": path.parent.name.replace("_", " "),
                    "description": "Simulation HTML du catalogue local, non rattachée à une leçon.",
                    "subject": "", "subject_key": "", "chapter": "", "lesson": "", "lesson_id": "",
                    "concepts": [], "source": "filesystem", "status": "validated",
                    "editable": False, "deletable": False,
                    "preview": {"kind": "simulation", "url": url},
                })
        return items

    def list_library(self) -> dict[str, Any]:
        admin = self._admin()
        database_available = True
        database_error = None
        try:
            lessons = admin_course_service.list_lessons(admin)
        except Exception as exc:
            lessons = []
            database_available = False
            database_error = str(exc)
        lesson_map = self._lesson_map(lessons)
        rows: list[dict] = []
        if database_available:
            try:
                rows = _data(admin.table("lesson_resources").select("*").order("order_index").execute())
            except Exception as exc:
                database_available = False
                database_error = str(exc)

        resource_items = [
            self._resource_item(row, lesson_map.get(str(row.get("lesson_id")), {}))
            for row in rows
            if str(row.get("resource_type") or "") in _VISUAL_RESOURCE_TYPES
        ]
        known_urls = {_resource_url(row) for row in rows if _resource_url(row)}
        items = self._schema_items() + self._preset_items() + resource_items + self._filesystem_items(known_urls)
        items.sort(key=lambda item: (
            item.get("subject") or "zzz",
            0 if item.get("lesson_id") else 1,
            item.get("chapter") or "",
            item.get("lesson") or "",
            item.get("kind") or "",
            item.get("title") or "",
        ))
        counts: dict[str, int] = {}
        for item in items:
            counts[item["kind"]] = counts.get(item["kind"], 0) + 1
        return {
            "items": items,
            "lessons": lessons,
            "stats": {"total": len(items), "by_kind": counts, "editable": sum(bool(item.get("editable")) for item in items)},
            "database_available": database_available,
            "database_error": database_error,
        }

    def _ensure_lesson(self, lesson_id: str, admin: Any) -> None:
        rows = _data(admin.table("lessons").select("id").eq("id", lesson_id).limit(1).execute())
        if not rows:
            raise VisualLibraryError("Leçon introuvable.")

    def get_preview_content(self, resource_id: str) -> dict[str, str]:
        """Return metadata-backed HTML only when an admin explicitly opens it."""

        admin = self._admin()
        rows = _data(
            admin.table("lesson_resources")
            .select("id,title,resource_type,file_path,metadata")
            .eq("id", resource_id)
            .limit(1)
            .execute()
        )
        if not rows:
            raise VisualLibraryError("Ressource introuvable.")

        row = rows[0]
        if str(row.get("resource_type") or "") != "simulation":
            raise VisualLibraryError("Cette ressource n'est pas une simulation HTML.")
        if str(row.get("file_path") or "") != "local:metadata":
            raise VisualLibraryError("Cette simulation utilise déjà un fichier de prévisualisation.")

        metadata = _metadata(row.get("metadata"))
        html = _metadata_html(metadata)
        if not html:
            raise VisualLibraryError("Le contenu HTML de cette simulation est absent.")
        if len(html.encode("utf-8")) > _MAX_INLINE_HTML_BYTES:
            raise VisualLibraryError("Le contenu HTML dépasse la taille maximale de prévisualisation.")

        return {
            "html": html,
            "mime_type": str(metadata.get("mime_type") or "text/html"),
            "title": str(row.get("title") or "Simulation HTML"),
        }

    @staticmethod
    def _validated_scientific(value: Any) -> tuple[dict[str, Any], dict[str, Any]]:
        normalized = normalize_scientific_visual(value)
        if normalized is None:
            raise VisualLibraryError("Le visuel scientifique est invalide ou contient des éléments interdits.")
        quality = scientific_visual_quality(normalized)
        if not quality["acceptable"]:
            raise VisualLibraryError("Qualité insuffisante : " + " ".join(quality["issues"]))
        return normalized, quality

    def create_item(self, body: AdminVisualItemCreate) -> dict[str, Any]:
        admin = self._admin()
        self._ensure_lesson(body.lesson_id, admin)
        metadata: dict[str, Any] = {
            "visual_kind": body.kind,
            "library_status": body.status,
            "library_source": body.source,
            "library_version": 1,
            "library_updated_at": _now(),
        }
        if body.kind == "scientific":
            normalized, quality = self._validated_scientific(body.scientific)
            metadata.update({"scientific": normalized, "quality": quality})
        elif not (body.file_path or body.external_url):
            raise VisualLibraryError("Une URL ou un fichier est obligatoire pour ce type de ressource.")
        row = {
            "lesson_id": body.lesson_id,
            "section_title": body.section_title,
            "resource_type": "simulation" if body.kind == "scientific" else body.kind,
            "title": body.title,
            "description": body.description,
            "file_path": body.file_path,
            "external_url": body.external_url,
            "trigger_text": body.trigger_text,
            "phase": body.phase,
            "difficulty_tier": body.difficulty_tier,
            "concepts": [str(item).strip()[:80] for item in body.concepts if str(item).strip()][:30],
            "metadata": metadata,
            "order_index": 0,
        }
        result = _data(admin.table("lesson_resources").insert(row).execute())
        if not result:
            raise VisualLibraryError("La ressource n'a pas pu être créée.")
        lessons = self._lesson_map(admin_course_service.list_lessons(admin))
        return self._resource_item(result[0], lessons.get(body.lesson_id, {}))

    def update_item(self, resource_id: str, body: AdminVisualItemUpdate) -> dict[str, Any]:
        admin = self._admin()
        rows = _data(admin.table("lesson_resources").select("*").eq("id", resource_id).limit(1).execute())
        if not rows:
            raise VisualLibraryError("Ressource introuvable.")
        current = rows[0]
        changes = body.model_dump(exclude_unset=True)
        lesson_id = str(changes.pop("lesson_id", current.get("lesson_id") or ""))
        self._ensure_lesson(lesson_id, admin)
        metadata = _metadata(current.get("metadata"))
        kind = str(changes.pop("kind", metadata.get("visual_kind") or current.get("resource_type") or "simulation"))
        if kind == "scientific":
            candidate = changes.pop("scientific", metadata.get("scientific"))
            normalized, quality = self._validated_scientific(candidate)
            metadata.update({"visual_kind": "scientific", "scientific": normalized, "quality": quality})
        else:
            changes.pop("scientific", None)
            metadata.pop("scientific", None)
            metadata.pop("quality", None)
            metadata["visual_kind"] = kind
        status = changes.pop("status", metadata.get("library_status") or "draft")
        metadata.update({
            "library_status": status,
            "library_version": int(metadata.get("library_version") or 1) + 1,
            "library_updated_at": _now(),
        })
        update = {**changes, "lesson_id": lesson_id, "resource_type": "simulation" if kind == "scientific" else kind, "metadata": metadata}
        if "concepts" in update and update["concepts"] is not None:
            update["concepts"] = [str(item).strip()[:80] for item in update["concepts"] if str(item).strip()][:30]
        result = _data(admin.table("lesson_resources").update(update).eq("id", resource_id).execute())
        if not result:
            raise VisualLibraryError("La ressource n'a pas pu être modifiée.")
        lessons = self._lesson_map(admin_course_service.list_lessons(admin))
        return self._resource_item(result[0], lessons.get(lesson_id, {}))

    def delete_item(self, resource_id: str) -> dict[str, Any]:
        admin = self._admin()
        rows = _data(admin.table("lesson_resources").select("id,file_path").eq("id", resource_id).limit(1).execute())
        if not rows:
            raise VisualLibraryError("Ressource introuvable.")
        admin.table("lesson_resources").delete().eq("id", resource_id).execute()
        return {"ok": True, "file_retained": bool(rows[0].get("file_path"))}

    @staticmethod
    def existing_match(prompt: str) -> dict[str, Any] | None:
        schema_id, score = match_schema(prompt)
        if not schema_id or score < 3:
            return None
        entry = next((item for item in SCHEMA_CATALOG if item["id"] == schema_id), None)
        return {"kind": "schema", "id": schema_id, "title": entry["title"], "score": score} if entry else None

    async def generate_visual(
        self,
        *,
        prompt: str,
        subject: str,
        title: str | None,
        engine: str,
        mode: str,
        current_spec: dict[str, Any] | None,
    ) -> dict[str, Any]:
        """Ask the configured LLM for JSON, then normalize it before returning it."""

        from app.services.llm_service import llm_service

        safe_current = None
        if current_spec is not None:
            safe_current = normalize_scientific_visual(current_spec)
            if safe_current is None:
                raise VisualLibraryError("Le visuel actuel est invalide et ne peut pas être envoyé au modèle.")

        engine_rule = (
            "Choisis toi-même le moteur le plus petit et le plus juste."
            if engine == "auto"
            else f"Utilise obligatoirement le moteur déclaratif `{engine}`."
        )
        task = (
            f"Matière : {subject or 'non précisée'}\n"
            f"Titre souhaité : {title or 'à proposer'}\n"
            f"Mode : {'amélioration' if mode == 'edit' else 'création'}\n"
            f"{engine_rule}\n"
            f"Demande pédagogique : {prompt.strip()}"
        )
        if safe_current is not None:
            task += "\nVisuel actuel à améliorer :\n" + json.dumps(safe_current, ensure_ascii=False)

        system_prompt = (
            SCIENTIFIC_VISUAL_PROMPT
            + "\n\n[MODE AUTEUR ADMIN]\n"
            "Retourne UNIQUEMENT un objet JSON de la forme "
            '{"title":"...","description":"...","scientific":{"engine":"..."}}. '
            "N'ajoute ni Markdown, ni HTML, ni JavaScript, ni URL. Le contenu doit être "
            "directement prévisualisable et conforme au niveau BAC."
        )
        messages = [{"role": "user", "content": task}]
        last_error = ""
        generated: dict[str, Any] | None = None
        for attempt in range(2):
            if attempt and last_error:
                messages.append({
                    "role": "user",
                    "content": (
                        "Corrige entièrement ta réponse. Défauts détectés par le validateur : "
                        + last_error
                        + " Retourne seulement le nouvel objet JSON complet."
                    ),
                })
            raw = await llm_service.chat(
                messages=messages,
                system_prompt=system_prompt,
                temperature=0.2,
                max_tokens=2200,
                session_type="admin_visual_library",
            )
            try:
                generated = normalize_generated_result(extract_llm_json(raw))
                if generated["quality"]["acceptable"]:
                    break
                last_error = " ".join(generated["quality"]["issues"])
            except VisualLibraryError as exc:
                last_error = str(exc)

        if generated is None:
            raise VisualLibraryError(last_error or "Le modèle n'a pas produit de visuel valide.")
        generated["existing_match"] = self.existing_match(prompt) if mode == "create" else None
        return generated

    def save_upload(self, filename: str, content_type: str, content: bytes, kind: str, lesson_id: str) -> dict[str, str]:
        allowed = {
            "image": {"image/png", "image/jpeg", "image/webp", "image/gif", "image/svg+xml"},
            "video": {"video/mp4", "video/webm", "video/ogg"},
        }
        if kind not in allowed or content_type not in allowed[kind]:
            raise VisualLibraryError("Type de fichier non autorisé.")
        if not content or len(content) > 25 * 1024 * 1024:
            raise VisualLibraryError("Le fichier doit peser moins de 25 Mo.")
        suffix = Path(filename).suffix.lower()
        storage_path = f"{kind}s/lesson_{lesson_id[:8]}/{uuid.uuid4().hex}{suffix}"
        admin = self._admin()
        self._ensure_lesson(lesson_id, admin)
        admin.storage.from_("pedagogical-resources").upload(
            path=storage_path,
            file=content,
            file_options={"content-type": content_type},
        )
        public_url = str(admin.storage.from_("pedagogical-resources").get_public_url(storage_path)).rstrip("?")
        return {"file_path": public_url, "storage_path": storage_path}


admin_visual_library_service = AdminVisualLibraryService()
