"""
Admin Service
Handles user management, token usage analytics, and online user tracking.
"""
import logging
from typing import Optional
from datetime import datetime, timedelta
from app.supabase_client import get_supabase_admin, get_supabase
from app.websockets.connection_manager import manager
from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class AdminService:
    """Admin operations: user CRUD, analytics, online tracking."""

    def __init__(self):
        self._supabase = None

    @property
    def supabase(self):
        if self._supabase is None:
            self._supabase = get_supabase_admin()
        return self._supabase

    # ──────────────────────────────────────────────
    # USER MANAGEMENT
    # ──────────────────────────────────────────────

    async def list_users(self) -> list[dict]:
        """List all students with their profiles."""
        result = self.supabase.table("students").select("*").order("created_at", desc=True).execute()
        users = result.data or []

        # Enrich with online status
        for user in users:
            user["is_online"] = manager.is_connected(user.get("id", ""))

        return users

    async def create_user(self, email: str, password: str, full_name: str, username: str, promo_code: Optional[str] = None, is_admin: bool = False) -> dict:
        """Create a new user account via Supabase Auth + students table."""
        supabase_public = get_supabase()

        # Check existing
        existing = self.supabase.table("students").select("id").eq("email", email).execute()
        if existing.data:
            raise ValueError("Email already registered")

        existing_username = self.supabase.table("students").select("id").eq("username", username).execute()
        if existing_username.data:
            raise ValueError("Username already taken")

        # Create auth user
        auth_response = supabase_public.auth.sign_up({
            "email": email,
            "password": password,
        })

        if not auth_response.user:
            raise ValueError("Failed to create auth user")

        user_id = str(auth_response.user.id)

        # Create student record
        import uuid
        student_data = {
            "id": user_id,
            "username": username,
            "email": email,
            "full_name": full_name,
            "preferred_language": "fr",
            "promo_code": promo_code.strip().upper() if promo_code else None,
            "is_active": True,
            "is_admin": is_admin,
            "created_at": datetime.utcnow().isoformat(),
        }

        student_result = self.supabase.table("students").insert(student_data).execute()
        if not student_result.data:
            raise ValueError("Failed to create student record")

        # Create profile
        profile_data = {
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
        }
        self.supabase.table("student_profiles").insert(profile_data).execute()

        return student_result.data[0]

    async def update_user(self, user_id: str, updates: dict) -> dict:
        """Update a user's info."""
        allowed = {"full_name", "username", "is_active", "is_admin", "preferred_language", "promo_code"}
        filtered = {k: v for k, v in updates.items() if k in allowed}

        if not filtered:
            raise ValueError("No valid fields to update")

        result = self.supabase.table("students").update(filtered).eq("id", user_id).execute()
        if not result.data:
            raise ValueError("User not found")
        return result.data[0]

    async def delete_user(self, user_id: str) -> bool:
        """Delete a user (soft delete - set is_active=False)."""
        self.supabase.table("students").update({"is_active": False}).eq("id", user_id).execute()
        return True

    async def reset_password(self, user_id: str, new_password: str) -> bool:
        """Reset a user's password via Supabase Admin API."""
        try:
            self.supabase.auth.admin.update_user_by_id(user_id, {"password": new_password})
            return True
        except Exception as e:
            logger.error(f"Failed to reset password for {user_id}: {e}")
            raise ValueError(f"Password reset failed: {e}")

    # ──────────────────────────────────────────────
    # ONLINE USERS
    # ──────────────────────────────────────────────

    def get_online_users(self) -> list[str]:
        """Get list of currently connected student IDs."""
        return list(manager.active_connections.keys())

    def get_online_count(self) -> int:
        """Get number of currently connected users."""
        return len(manager.active_connections)

    # ──────────────────────────────────────────────
    # TOKEN USAGE ANALYTICS
    # ──────────────────────────────────────────────

    async def get_usage_summary(self, days: int = 30) -> dict:
        """Get aggregated token usage summary."""
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        result = self.supabase.table("token_usage") \
            .select("*") \
            .gte("created_at", since) \
            .order("created_at", desc=True) \
            .execute()

        records = result.data or []

        total_cost = sum(float(r.get("cost_usd", 0)) for r in records)
        total_requests = len(records)
        total_tokens = sum(r.get("total_tokens", 0) for r in records)
        total_prompt = sum(r.get("prompt_tokens", 0) for r in records)
        total_completion = sum(r.get("completion_tokens", 0) for r in records)

        # Per provider breakdown
        providers = {}
        for r in records:
            p = r.get("provider", "unknown")
            if p not in providers:
                providers[p] = {"requests": 0, "tokens": 0, "cost_usd": 0.0}
            providers[p]["requests"] += 1
            providers[p]["tokens"] += r.get("total_tokens", 0)
            providers[p]["cost_usd"] += float(r.get("cost_usd", 0))

        # Round costs
        for p in providers:
            providers[p]["cost_usd"] = round(providers[p]["cost_usd"], 4)

        # Per day breakdown (last 30 days)
        daily = {}
        for r in records:
            day = r.get("created_at", "")[:10]
            if day not in daily:
                daily[day] = {"requests": 0, "tokens": 0, "cost_usd": 0.0}
            daily[day]["requests"] += 1
            daily[day]["tokens"] += r.get("total_tokens", 0)
            daily[day]["cost_usd"] += float(r.get("cost_usd", 0))

        for d in daily:
            daily[d]["cost_usd"] = round(daily[d]["cost_usd"], 4)

        return {
            "period_days": days,
            "total_cost_usd": round(total_cost, 4),
            "total_requests": total_requests,
            "total_tokens": total_tokens,
            "total_prompt_tokens": total_prompt,
            "total_completion_tokens": total_completion,
            "providers": providers,
            "daily": daily,
        }

    async def get_usage_by_user(self, days: int = 30) -> list[dict]:
        """Get token usage grouped by user."""
        since = (datetime.utcnow() - timedelta(days=days)).isoformat()

        result = self.supabase.table("token_usage") \
            .select("*") \
            .gte("created_at", since) \
            .execute()

        records = result.data or []

        # Group by student
        users = {}
        student_ids_to_fetch = set()
        
        for r in records:
            sid = r.get("student_id") or "anonymous"
            if sid not in users:
                users[sid] = {
                    "student_id": sid,
                    "student_email": r.get("student_email", ""),
                    "full_name": "",
                    "username": "",
                    "requests": 0,
                    "total_tokens": 0,
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "cost_usd": 0.0,
                    "providers": {},
                    "last_request": r.get("created_at", ""),
                }
                if sid != "anonymous":
                    student_ids_to_fetch.add(sid)
            
            u = users[sid]
            u["requests"] += 1
            u["total_tokens"] += r.get("total_tokens", 0)
            u["prompt_tokens"] += r.get("prompt_tokens", 0)
            u["completion_tokens"] += r.get("completion_tokens", 0)
            u["cost_usd"] += float(r.get("cost_usd", 0))

            p = r.get("provider", "unknown")
            if p not in u["providers"]:
                u["providers"][p] = {"requests": 0, "tokens": 0, "cost_usd": 0.0}
            u["providers"][p]["requests"] += 1
            u["providers"][p]["tokens"] += r.get("total_tokens", 0)
            u["providers"][p]["cost_usd"] += float(r.get("cost_usd", 0))

            # Track most recent
            if r.get("created_at", "") > u["last_request"]:
                u["last_request"] = r.get("created_at", "")

        # Fetch student details from students table
        if student_ids_to_fetch:
            students_result = self.supabase.table("students") \
                .select("id, email, full_name, username") \
                .in_("id", list(student_ids_to_fetch)) \
                .execute()
            
            students_map = {s["id"]: s for s in (students_result.data or [])}
            
            # Enrich user data with student info
            for sid, user_data in users.items():
                if sid in students_map:
                    student = students_map[sid]
                    user_data["full_name"] = student.get("full_name", "")
                    user_data["username"] = student.get("username", "")
                    # Use email from students table if not in token_usage
                    if not user_data["student_email"]:
                        user_data["student_email"] = student.get("email", "")

        # Round and sort by cost desc
        result_list = list(users.values())
        for u in result_list:
            u["cost_usd"] = round(u["cost_usd"], 4)
            for p in u["providers"]:
                u["providers"][p]["cost_usd"] = round(u["providers"][p]["cost_usd"], 4)

        result_list.sort(key=lambda x: x["cost_usd"], reverse=True)
        return result_list

    async def get_recent_requests(self, limit: int = 50) -> list[dict]:
        """Get recent API requests."""
        result = self.supabase.table("token_usage") \
            .select("*") \
            .order("created_at", desc=True) \
            .limit(limit) \
            .execute()

        return result.data or []

    async def get_dashboard_stats(self) -> dict:
        """Get all stats needed for the admin dashboard overview."""
        # Total users
        users_result = self.supabase.table("students").select("id, is_active, created_at, email").execute()
        all_users = users_result.data or []
        total_users = len(all_users)
        active_users = sum(1 for u in all_users if u.get("is_active", True))

        # Online count
        online_count = self.get_online_count()
        online_ids = self.get_online_users()

        # Today's usage
        today = datetime.utcnow().replace(hour=0, minute=0, second=0).isoformat()
        today_result = self.supabase.table("token_usage") \
            .select("*") \
            .gte("created_at", today) \
            .execute()
        today_records = today_result.data or []
        today_cost = round(sum(float(r.get("cost_usd", 0)) for r in today_records), 4)
        today_requests = len(today_records)
        today_tokens = sum(r.get("total_tokens", 0) for r in today_records)

        # This month's usage
        month_start = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0).isoformat()
        month_result = self.supabase.table("token_usage") \
            .select("cost_usd, total_tokens") \
            .gte("created_at", month_start) \
            .execute()
        month_records = month_result.data or []
        month_cost = round(sum(float(r.get("cost_usd", 0)) for r in month_records), 4)
        month_tokens = sum(r.get("total_tokens", 0) for r in month_records)

        # All time total
        all_result = self.supabase.table("token_usage") \
            .select("cost_usd, total_tokens") \
            .execute()
        all_records = all_result.data or []
        all_time_cost = round(sum(float(r.get("cost_usd", 0)) for r in all_records), 4)

        return {
            "total_users": total_users,
            "active_users": active_users,
            "online_count": online_count,
            "online_user_ids": online_ids,
            "today": {
                "cost_usd": today_cost,
                "requests": today_requests,
                "tokens": today_tokens,
            },
            "this_month": {
                "cost_usd": month_cost,
                "tokens": month_tokens,
            },
            "all_time_cost_usd": all_time_cost,
        }


admin_service = AdminService()
