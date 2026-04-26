"""
Registration requests endpoints.
- Public: POST /registration-requests (anyone can submit an inscription form)
- Admin:  GET/PATCH/DELETE /admin/registration-requests
- Admin:  POST /admin/registration-requests/{id}/activate  (create account)
"""
from datetime import datetime, timedelta
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
import logging
import uuid

from app.schemas.registration import (
    RegistrationRequestCreate,
    RegistrationRequestUpdate,
)
from app.supabase_client import get_supabase_admin, get_supabase
from app.api.v1.endpoints.admin import _verify_admin_token

logger = logging.getLogger(__name__)

# Public router
public_router = APIRouter(prefix="/registration-requests", tags=["registration"])

# Admin router (mounted under /admin)
admin_router = APIRouter(prefix="/admin/registration-requests", tags=["admin-registration"])


TABLE = "registration_requests"


# ─── PUBLIC ────────────────────────────────────────────────────────────

@public_router.post("", status_code=201)
async def create_registration_request(payload: RegistrationRequestCreate):
    """Public endpoint — prospective student submits the inscription form."""
    sb = get_supabase_admin()
    data = payload.model_dump(exclude_none=False)
    promo_code = (data.get("promo_code") or "").strip().upper()
    if promo_code:
        try:
            promo_res = sb.table("promo_codes").select("code").eq("code", promo_code).eq("is_active", True).execute()
            if not promo_res.data:
                raise HTTPException(400, "Code promo invalide ou désactivé")
        except HTTPException:
            raise
        except Exception as e:
            logger.warning(f"Promo code validation skipped (table missing?): {e}")
    data["promo_code"] = promo_code or None
    data["status"] = "pending"
    try:
        res = sb.table(TABLE).insert(data).execute()
        if not res.data:
            raise HTTPException(500, "Échec de l'enregistrement")
        return {
            "ok": True,
            "id": res.data[0].get("id"),
            "message": "Demande enregistrée. Nous vous contacterons très bientôt.",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Registration insert failed")
        raise HTTPException(500, f"Erreur serveur: {e}")


# ─── ADMIN ─────────────────────────────────────────────────────────────

@admin_router.get("")
async def list_registration_requests(
    status: str | None = None,
    admin: bool = Depends(_verify_admin_token),
):
    sb = get_supabase_admin()
    q = sb.table(TABLE).select("*").order("created_at", desc=True)
    if status:
        q = q.eq("status", status)
    res = q.execute()
    return {"requests": res.data or []}


@admin_router.patch("/{request_id}")
async def update_registration_request(
    request_id: str,
    payload: RegistrationRequestUpdate,
    admin: bool = Depends(_verify_admin_token),
):
    sb = get_supabase_admin()
    updates = payload.model_dump(exclude_none=True)
    if not updates:
        raise HTTPException(400, "Aucune modification fournie")

    # Auto-timestamp status transitions
    if updates.get("status") == "contacted":
        updates["contacted_at"] = datetime.utcnow().isoformat()
    if updates.get("status") == "activated":
        updates["activated_at"] = datetime.utcnow().isoformat()

    res = sb.table(TABLE).update(updates).eq("id", request_id).execute()
    if not res.data:
        raise HTTPException(404, "Demande introuvable")
    return {"request": res.data[0]}


@admin_router.delete("/{request_id}")
async def delete_registration_request(
    request_id: str,
    admin: bool = Depends(_verify_admin_token),
):
    sb = get_supabase_admin()
    sb.table(TABLE).delete().eq("id", request_id).execute()
    return {"ok": True}


# ─── ACTIVATE (create account from inscription) ──────────────────────

class ActivateRequest(BaseModel):
    password: str = Field(..., min_length=4, max_length=128)
    account_type: str = Field("permanent", pattern=r"^(test|permanent)$")
    username: Optional[str] = None  # auto-derived if empty
    promo_code: Optional[str] = None


@admin_router.post("/{request_id}/activate")
async def activate_registration_request(
    request_id: str,
    payload: ActivateRequest,
    admin: bool = Depends(_verify_admin_token),
):
    """Create a real Supabase user account from a registration request.

    account_type:
      - **permanent**: no expiry
      - **test**: expires in 24 hours (expires_at set on student row)
    """
    sb = get_supabase_admin()
    sb_public = get_supabase()

    # 1. Fetch the registration request
    req_res = sb.table(TABLE).select("*").eq("id", request_id).execute()
    if not req_res.data:
        raise HTTPException(404, "Demande introuvable")
    reg = req_res.data[0]

    if reg.get("created_user_id"):
        raise HTTPException(400, "Un compte a déjà été créé pour cette demande")

    prenom = (reg.get("prenom") or "").strip()
    nom = (reg.get("nom") or "").strip()
    full_name = f"{prenom} {nom}".strip() or "Étudiant"
    digits = "".join(c for c in (reg.get("phone") or "") if c.isdigit())

    # 2. Build canonical "prenom.nom" base (ascii lowercase, no spaces/accents/symbols)
    def _slug(s: str) -> str:
        s = s.lower().strip()
        for fr, to in [
            ("é","e"),("è","e"),("ê","e"),("ë","e"),
            ("à","a"),("â","a"),("ä","a"),
            ("ô","o"),("ö","o"),
            ("î","i"),("ï","i"),
            ("û","u"),("ü","u"),("ù","u"),
            ("ç","c"),("ñ","n"),
            ("œ","oe"),("æ","ae"),
        ]:
            s = s.replace(fr, to)
        # keep only [a-z0-9-]
        return "".join(ch for ch in s if ch.isalnum() or ch == "-")

    slug_prenom = _slug(prenom)
    slug_nom = _slug(nom)
    base = f"{slug_prenom}.{slug_nom}".strip(".") or f"user{digits[-4:] or uuid.uuid4().hex[:4]}"

    username = (payload.username or "").strip() or base

    # Canonical login email: nom.prenom@moalim.online (no longer phone-based)
    email = f"{base}@moalim.online"

    # 3. Resolve duplicates with numeric suffixes (1, 2, 3…)
    def _email_taken(e: str) -> bool:
        return bool(sb.table("students").select("id").eq("email", e).execute().data)

    def _username_taken(u: str) -> bool:
        return bool(sb.table("students").select("id").eq("username", u).execute().data)

    if _email_taken(email):
        for i in range(2, 100):
            cand = f"{base}{i}@moalim.online"
            if not _email_taken(cand):
                email = cand
                break
        else:
            email = f"{base}.{uuid.uuid4().hex[:4]}@moalim.online"

    if _username_taken(username):
        for i in range(2, 100):
            cand = f"{base}{i}"
            if not _username_taken(cand):
                username = cand
                break
        else:
            username = f"{base}{uuid.uuid4().hex[:4]}"

    # 4. Create Supabase Auth user
    try:
        auth_res = sb_public.auth.sign_up({"email": email, "password": payload.password})
        if not auth_res.user:
            raise HTTPException(500, "Échec de création du compte Auth")
        user_id = str(auth_res.user.id)
    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Supabase auth sign_up failed")
        raise HTTPException(500, f"Erreur Auth: {e}")

    # 5. Compute expires_at
    expires_at = None
    if payload.account_type == "test":
        expires_at = (datetime.utcnow() + timedelta(days=1)).isoformat()
    promo_code = (payload.promo_code or reg.get("promo_code") or "").strip().upper() or None

    # 6. Insert student row
    student_data = {
        "id": user_id,
        "username": username,
        "email": email,
        "full_name": full_name,
        "preferred_language": "fr",
        "is_active": True,
        "is_admin": False,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": expires_at,
        "created_from_request_id": request_id,
        "promo_code": promo_code,
    }
    try:
        stu_res = sb.table("students").insert(student_data).execute()
        if not stu_res.data:
            raise HTTPException(500, "Échec insertion student")
    except HTTPException:
        raise
    except Exception as e:
        # Fallback: maybe students.promo_code column is missing -> retry without it
        logger.warning(f"Student insert with promo_code failed, retrying without: {e}")
        student_data.pop("promo_code", None)
        try:
            stu_res = sb.table("students").insert(student_data).execute()
            if not stu_res.data:
                raise HTTPException(500, "Échec insertion student")
        except Exception as e2:
            logger.exception("Student insert failed (fallback)")
            raise HTTPException(500, f"Erreur student: {e2}")
        # Try to set promo_code via separate update so it goes through if col exists
        if promo_code:
            try:
                sb.table("students").update({"promo_code": promo_code}).eq("id", user_id).execute()
            except Exception as e3:
                logger.warning(f"students.promo_code column missing, cannot store promo: {e3}")

    # 7. Insert student_profiles row
    try:
        sb.table("student_profiles").insert({
            "id": str(uuid.uuid4()),
            "student_id": user_id,
            "proficiency_level": "intermediate",
            "learning_style": "Socratique",
            "strengths": [],
            "weaknesses": [],
            "total_study_time_minutes": 0,
            "sessions_completed": 0,
            "exercises_completed": 0,
            "average_score": 0.0,
        }).execute()
    except Exception as e:
        logger.warning(f"Profile creation failed (non-fatal): {e}")

    # 8. Update registration_request → activated
    sb.table(TABLE).update({
        "status": "activated",
        "activated_at": datetime.utcnow().isoformat(),
        "created_user_id": user_id,
    }).eq("id", request_id).execute()

    return {
        "ok": True,
        "user_id": user_id,
        "username": username,
        "email": email,
        "full_name": full_name,
        "account_type": payload.account_type,
        "expires_at": expires_at,
    }
