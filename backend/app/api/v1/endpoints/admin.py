"""
Admin API Endpoints
User management, token usage analytics, online tracking.
Protected by admin password.
"""
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.config import get_settings
from app.services.admin_service import admin_service
from app.schemas.admin import AdminLogin, CreateUser, UpdateUser, ResetPassword, CreatePromoCode, UpdatePromoCode, BulkUserAction
from jose import jwt
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/admin", tags=["admin-dashboard"])
security = HTTPBearer()
settings = get_settings()

ADMIN_JWT_SECRET = settings.secret_key + "_admin"
ADMIN_TOKEN_EXPIRE_HOURS = 24


def _create_admin_token() -> str:
    """Create a JWT token for admin access."""
    payload = {
        "sub": "admin",
        "role": "admin",
        "exp": datetime.utcnow() + timedelta(hours=ADMIN_TOKEN_EXPIRE_HOURS),
    }
    return jwt.encode(payload, ADMIN_JWT_SECRET, algorithm="HS256")


def _verify_admin_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> bool:
    """Verify the admin JWT token."""
    try:
        payload = jwt.decode(credentials.credentials, ADMIN_JWT_SECRET, algorithms=["HS256"])
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Not an admin token")
        return True
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired admin token")


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
                await admin_service.update_user(uid, {"is_active": False})
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
