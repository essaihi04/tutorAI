"""
Admin API Endpoints
User management, token usage analytics, online tracking.
Protected by admin password.
"""
from fastapi import APIRouter, HTTPException, Depends, File, UploadFile, status
from pydantic import BaseModel, Field
from app.admin_auth import create_admin_token, verify_admin_token
from app.config import get_settings
from app.services.admin_service import admin_service
from app.services.admin_course_service import (
    CourseEditorError,
    CourseValidationError,
    admin_course_service,
)
from app.services.admin_visual_library_service import (
    VisualLibraryError,
    admin_visual_library_service,
)
from app.services.subject_access_service import subject_access_service
from app.supabase_client import get_supabase_admin
from app.schemas.admin import AdminLogin, CreateUser, UpdateUser, ResetPassword, CreatePromoCode, UpdatePromoCode, BulkUserAction
from app.schemas.admin_course import (
    AdminCourseAudioStatus,
    AdminCourseCreate,
    AdminCourseDuplicate,
    AdminCourseSave,
)
from app.schemas.admin_visual_library import (
    AdminVisualGenerate,
    AdminVisualItemCreate,
    AdminVisualItemUpdate,
)
from datetime import datetime
from typing import Optional
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["admin-dashboard"])
settings = get_settings()


class SubjectAccessUpdate(BaseModel):
    managed: bool = True
    subject_ids: list[str] = Field(default_factory=list)
    source: str = "manual"
    ends_at: Optional[datetime] = None


# Backwards-compatible aliases: several endpoint signatures and tests import
# these private names from this module.
_create_admin_token = create_admin_token
_verify_admin_token = verify_admin_token


# ──────────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────────

@router.post("/login")
async def admin_login(data: AdminLogin):
    """Login with admin password, returns JWT."""
    if data.password != settings.admin_password:
        raise HTTPException(status_code=401, detail="Invalid admin password")
    token = _create_admin_token()
    return {"access_token": token, "token_type": "bearer"}


# ──────────────────────────────────────────────
# DASHBOARD OVERVIEW
# ──────────────────────────────────────────────

@router.get("/dashboard")
async def get_dashboard(admin: bool = Depends(_verify_admin_token)):
    """Get complete dashboard stats."""
    try:
        stats = await admin_service.get_dashboard_stats()
        return stats
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# UNIFIED VISUAL LIBRARY
# ──────────────────────────────────────────────

def _raise_visual_library_error(exc: Exception) -> None:
    if isinstance(exc, VisualLibraryError):
        raise HTTPException(status_code=422, detail=str(exc))
    logger.exception("Visual library error")
    raise HTTPException(status_code=500, detail="Erreur interne de la bibliothèque visuelle")


@router.get("/visual-library")
async def get_visual_library(admin: bool = Depends(_verify_admin_token)):
    """Return code-owned catalogues, persistent media and lesson resources."""
    try:
        return admin_visual_library_service.list_library()
    except Exception as exc:
        _raise_visual_library_error(exc)


@router.post("/visual-library/items")
async def create_visual_library_item(
    body: AdminVisualItemCreate,
    admin: bool = Depends(_verify_admin_token),
):
    try:
        return {"item": admin_visual_library_service.create_item(body)}
    except Exception as exc:
        _raise_visual_library_error(exc)


@router.get("/visual-library/items/{resource_id}/preview-content")
async def get_visual_library_preview_content(
    resource_id: str,
    admin: bool = Depends(_verify_admin_token),
):
    """Load metadata-backed simulation HTML on demand for the sandboxed admin preview."""
    try:
        return admin_visual_library_service.get_preview_content(resource_id)
    except Exception as exc:
        _raise_visual_library_error(exc)


@router.put("/visual-library/items/{resource_id}")
async def update_visual_library_item(
    resource_id: str,
    body: AdminVisualItemUpdate,
    admin: bool = Depends(_verify_admin_token),
):
    try:
        return {"item": admin_visual_library_service.update_item(resource_id, body)}
    except Exception as exc:
        _raise_visual_library_error(exc)


@router.delete("/visual-library/items/{resource_id}")
async def delete_visual_library_item(
    resource_id: str,
    admin: bool = Depends(_verify_admin_token),
):
    try:
        return admin_visual_library_service.delete_item(resource_id)
    except Exception as exc:
        _raise_visual_library_error(exc)


@router.post("/visual-library/generate")
async def generate_visual_library_item(
    body: AdminVisualGenerate,
    admin: bool = Depends(_verify_admin_token),
):
    """Generate a reviewable declarative draft; this endpoint never saves it."""
    try:
        return await admin_visual_library_service.generate_visual(
            prompt=body.prompt,
            subject=body.subject,
            title=body.title,
            engine=body.engine,
            mode=body.mode,
            current_spec=body.current_spec,
        )
    except Exception as exc:
        _raise_visual_library_error(exc)


@router.post("/visual-library/upload")
async def upload_visual_library_media(
    lesson_id: str,
    kind: str,
    file: UploadFile = File(...),
    admin: bool = Depends(_verify_admin_token),
):
    try:
        content = await file.read(25 * 1024 * 1024 + 1)
        return admin_visual_library_service.save_upload(
            file.filename or "media",
            file.content_type or "application/octet-stream",
            content,
            kind,
            lesson_id,
        )
    except Exception as exc:
        _raise_visual_library_error(exc)
    finally:
        await file.close()


# ──────────────────────────────────────────────
# VERSIONED COURSE EDITOR
# ──────────────────────────────────────────────

def _raise_course_editor_error(exc: Exception) -> None:
    if isinstance(exc, CourseValidationError):
        raise HTTPException(
            status_code=422,
            detail={"message": str(exc), "issues": exc.issues},
        )
    if isinstance(exc, CourseEditorError):
        raise HTTPException(status_code=400, detail=str(exc))
    logger.exception("Course editor error")
    raise HTTPException(status_code=500, detail="Erreur interne de l'éditeur de cours")


@router.get("/courses")
async def list_admin_courses(admin: bool = Depends(_verify_admin_token)):
    """List database versions and manifest fallbacks visible to an author."""
    try:
        return admin_course_service.list_courses()
    except Exception as exc:
        _raise_course_editor_error(exc)


@router.get("/courses/options")
async def get_admin_course_options(admin: bool = Depends(_verify_admin_token)):
    """Return lessons, validated schemas and persistent media choices."""
    try:
        return admin_course_service.editor_options()
    except Exception as exc:
        _raise_course_editor_error(exc)


@router.post("/courses/media")
async def upload_admin_course_media(
    file: UploadFile = File(...),
    admin: bool = Depends(_verify_admin_token),
):
    """Persist an image used by a slide or a course cover."""
    try:
        content = await file.read(10 * 1024 * 1024 + 1)
        url = admin_course_service.save_media(
            file.filename or "visuel.png",
            file.content_type or "application/octet-stream",
            content,
        )
        return {"url": url}
    except Exception as exc:
        _raise_course_editor_error(exc)
    finally:
        await file.close()


@router.post("/courses")
async def create_admin_course(
    body: AdminCourseCreate,
    admin: bool = Depends(_verify_admin_token),
):
    """Create a new editable draft attached to an existing lesson."""
    try:
        return {"course": admin_course_service.create_course(body.model_dump())}
    except Exception as exc:
        _raise_course_editor_error(exc)


@router.patch("/courses/audio/{audio_id}")
async def update_admin_course_audio(
    audio_id: str,
    body: AdminCourseAudioStatus,
    admin: bool = Depends(_verify_admin_token),
):
    """Verify, publish, reject or explicitly stale a generated audio asset."""
    try:
        return {"audio": admin_course_service.set_audio_status(audio_id, body.status)}
    except Exception as exc:
        _raise_course_editor_error(exc)


@router.get("/courses/{course_ref}")
async def get_admin_course(course_ref: str, admin: bool = Depends(_verify_admin_token)):
    """Load the complete authoring payload, including answer keys and audio state."""
    try:
        return {"course": admin_course_service.get_course(course_ref)}
    except Exception as exc:
        _raise_course_editor_error(exc)


@router.put("/courses/{course_id}")
async def save_admin_course(
    course_id: str,
    body: AdminCourseSave,
    admin: bool = Depends(_verify_admin_token),
):
    """Save a complete draft, including additions, deletions and reordering."""
    try:
        return {"course": admin_course_service.save_course(course_id, body.model_dump())}
    except Exception as exc:
        _raise_course_editor_error(exc)


@router.post("/courses/{course_ref}/duplicate")
async def duplicate_admin_course(
    course_ref: str,
    body: AdminCourseDuplicate,
    admin: bool = Depends(_verify_admin_token),
):
    """Materialize a manifest or clone a locked version into a new draft."""
    try:
        return {"course": admin_course_service.duplicate_course(course_ref, body.lesson_id)}
    except Exception as exc:
        _raise_course_editor_error(exc)


@router.post("/courses/{course_id}/publish")
async def publish_admin_course(course_id: str, admin: bool = Depends(_verify_admin_token)):
    """Validate and publish one version, archiving the previous live version."""
    try:
        return {"course": admin_course_service.publish_course(course_id)}
    except Exception as exc:
        _raise_course_editor_error(exc)


@router.post("/courses/{course_id}/archive")
async def archive_admin_course(course_id: str, admin: bool = Depends(_verify_admin_token)):
    try:
        return {"course": admin_course_service.archive_course(course_id)}
    except Exception as exc:
        _raise_course_editor_error(exc)


@router.delete("/courses/{course_id}")
async def delete_admin_course(course_id: str, admin: bool = Depends(_verify_admin_token)):
    """Delete a non-published version and its child rows through DB cascades."""
    try:
        admin_course_service.delete_course(course_id)
        return {"ok": True}
    except Exception as exc:
        _raise_course_editor_error(exc)


# ──────────────────────────────────────────────
# USER MANAGEMENT
# ──────────────────────────────────────────────

@router.get("/users")
async def list_users(admin: bool = Depends(_verify_admin_token)):
    """List all users."""
    try:
        users = await admin_service.list_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users")
async def create_user(data: CreateUser, admin: bool = Depends(_verify_admin_token)):
    """Create a new user account."""
    try:
        user = await admin_service.create_user(
            email=data.email,
            password=data.password,
            full_name=data.full_name,
            username=data.username,
            is_admin=data.is_admin,
        )
        return {"user": user, "message": "User created successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/users/{user_id}")
async def update_user(user_id: str, data: UpdateUser, admin: bool = Depends(_verify_admin_token)):
    """Update a user."""
    try:
        updates = data.model_dump(exclude_none=True)
        user = await admin_service.update_user(user_id, updates)
        return {"user": user}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users/{user_id}/subject-access")
async def get_user_subject_access(user_id: str, admin: bool = Depends(_verify_admin_token)):
    """Return the exact learning scope an admin would apply to a student."""
    try:
        return subject_access_service.get_context_for_student_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/users/{user_id}/subject-access")
async def update_user_subject_access(
    user_id: str,
    data: SubjectAccessUpdate,
    admin: bool = Depends(_verify_admin_token),
):
    """Activate a strict subject pack, or return an account to legacy mode."""
    db = get_supabase_admin()
    try:
        student_result = db.table("students").select("id").eq("id", user_id).limit(1).execute()
        if not student_result.data:
            raise HTTPException(status_code=404, detail="Élève introuvable")

        if data.managed:
            requested_ids = list(dict.fromkeys(data.subject_ids))
            if requested_ids:
                subject_result = db.table("subjects").select("id").in_("id", requested_ids).execute()
                valid_ids = {str(row["id"]) for row in (subject_result.data or [])}
                invalid_ids = [subject_id for subject_id in requested_ids if subject_id not in valid_ids]
                if invalid_ids:
                    raise HTTPException(status_code=400, detail={"invalid_subject_ids": invalid_ids})

            # Preserve rows for auditability: old access is suspended, then the
            # requested pack is reactivated with its current commercial source.
            db.table("student_subject_access").update({
                "status": "suspended",
                "updated_at": datetime.utcnow().isoformat(),
            }).eq("student_id", user_id).execute()

            if requested_ids:
                rows = [
                    {
                        "student_id": user_id,
                        "subject_id": subject_id,
                        "status": "active",
                        "source": data.source,
                        "starts_at": datetime.utcnow().isoformat(),
                        "ends_at": data.ends_at.isoformat() if data.ends_at else None,
                        "updated_at": datetime.utcnow().isoformat(),
                    }
                    for subject_id in requested_ids
                ]
                db.table("student_subject_access").upsert(
                    rows,
                    on_conflict="student_id,subject_id",
                ).execute()

        db.table("students").update({
            "subject_access_managed": data.managed,
        }).eq("id", user_id).execute()

        return subject_access_service.get_context_for_student_id(user_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/users/{user_id}")
async def delete_user(user_id: str, admin: bool = Depends(_verify_admin_token)):
    """Deactivate a user."""
    try:
        await admin_service.delete_user(user_id)
        return {"message": "User deactivated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/users/bulk-action")
async def bulk_user_action(data: BulkUserAction, admin: bool = Depends(_verify_admin_token)):
    """Perform a bulk action on multiple users.
    
    Actions: delete (soft), activate, deactivate
    """
    if not data.user_ids:
        raise HTTPException(status_code=400, detail="Aucun utilisateur sélectionné")
    if data.action not in ("delete", "activate", "deactivate"):
        raise HTTPException(status_code=400, detail=f"Action inconnue: {data.action}")

    results = {"success": 0, "failed": 0, "errors": []}
    for uid in data.user_ids:
        try:
            if data.action == "delete":
                await admin_service.delete_user(uid)
            elif data.action == "activate":
                await admin_service.update_user(uid, {"is_active": True})
            elif data.action == "deactivate":
                await admin_service.deactivate_user(uid)
            results["success"] += 1
        except Exception as e:
            results["failed"] += 1
            results["errors"].append({"user_id": uid, "error": str(e)})

    return results


@router.post("/users/{user_id}/reset-password")
async def reset_password(user_id: str, data: ResetPassword, admin: bool = Depends(_verify_admin_token)):
    """Reset a user's password."""
    try:
        await admin_service.reset_password(user_id, data.new_password)
        return {"message": "Password reset successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ──────────────────────────────────────────────
# PROMO CODES
# ──────────────────────────────────────────────

def _normalize_promo_code(code: str) -> str:
    return code.strip().upper()


@router.get("/promo-codes")
async def list_promo_codes(admin: bool = Depends(_verify_admin_token)):
    try:
        result = admin_service.supabase.table("promo_codes").select("*").order("created_at", desc=True).execute()
        return {"promo_codes": result.data or []}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/promo-codes")
async def create_promo_code(data: CreatePromoCode, admin: bool = Depends(_verify_admin_token)):
    try:
        code = _normalize_promo_code(data.code)
        if not code:
            raise HTTPException(status_code=400, detail="Code promo obligatoire")
        existing = admin_service.supabase.table("promo_codes").select("id").eq("code", code).execute()
        if existing.data:
            raise HTTPException(status_code=400, detail="Ce code promo existe déjà")
        result = admin_service.supabase.table("promo_codes").insert({
            "code": code,
            "label": data.label.strip() if data.label else None,
            "is_active": data.is_active,
        }).execute()
        if not result.data:
            raise HTTPException(status_code=500, detail="Échec de création du code promo")
        return {"promo_code": result.data[0]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/promo-codes/{promo_id}")
async def update_promo_code(promo_id: str, data: UpdatePromoCode, admin: bool = Depends(_verify_admin_token)):
    updates = data.model_dump(exclude_none=True)
    if "label" in updates and updates["label"]:
        updates["label"] = updates["label"].strip()
    if not updates:
        raise HTTPException(status_code=400, detail="Aucune modification fournie")
    result = admin_service.supabase.table("promo_codes").update(updates).eq("id", promo_id).execute()
    if not result.data:
        raise HTTPException(status_code=404, detail="Code promo introuvable")
    return {"promo_code": result.data[0]}


@router.delete("/promo-codes/{promo_id}")
async def delete_promo_code(promo_id: str, admin: bool = Depends(_verify_admin_token)):
    result = admin_service.supabase.table("promo_codes").delete().eq("id", promo_id).execute()
    return {"ok": True, "deleted": bool(result.data)}


# ──────────────────────────────────────────────
# ONLINE USERS
# ──────────────────────────────────────────────

@router.get("/online")
async def get_online_users(admin: bool = Depends(_verify_admin_token)):
    """Get currently online users with IP and connection time."""
    from app.websockets.connection_manager import manager as ws_manager

    online_ids = admin_service.get_online_users()
    online_count = admin_service.get_online_count()

    # Enrich with user info + connection metadata (IP, connected_at)
    users_info = []
    if online_ids:
        for uid in online_ids:
            try:
                result = admin_service.supabase.table("students") \
                    .select("id, username, email, full_name") \
                    .eq("id", uid).execute()
                entry = result.data[0] if result.data else {"id": uid, "username": "unknown"}
            except Exception:
                entry = {"id": uid, "username": "unknown"}

            conn = ws_manager.connection_info.get(uid, {})
            entry["ip"] = conn.get("ip", "unknown")
            entry["connected_at"] = conn.get("connected_at")
            users_info.append(entry)

    return {"online_count": online_count, "online_users": users_info}


# ──────────────────────────────────────────────
# TOKEN USAGE ANALYTICS
# ──────────────────────────────────────────────

@router.get("/usage/summary")
async def get_usage_summary(days: int = 30, admin: bool = Depends(_verify_admin_token)):
    """Get aggregated token usage summary."""
    try:
        summary = await admin_service.get_usage_summary(days=days)
        return summary
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage/by-user")
async def get_usage_by_user(days: int = 30, admin: bool = Depends(_verify_admin_token)):
    """Get token usage grouped by user."""
    try:
        data = await admin_service.get_usage_by_user(days=days)
        return {"users": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/usage/recent")
async def get_recent_requests(limit: int = 50, admin: bool = Depends(_verify_admin_token)):
    """Get recent API requests."""
    try:
        data = await admin_service.get_recent_requests(limit=limit)
        return {"requests": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
