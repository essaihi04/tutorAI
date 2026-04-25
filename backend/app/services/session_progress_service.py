"""
Session Progress Service
Tracks student progress within each lesson for coaching mode.
Enables resuming sessions and remembering what was already covered.
"""
import logging
from datetime import datetime, timezone
from typing import Optional
from app.supabase_client import get_supabase_admin

_log = logging.getLogger(__name__)


class SessionProgressService:
    """Manages lesson progress memory for coaching mode."""

    def __init__(self):
        self.supabase = get_supabase_admin()

    async def get_lesson_progress(self, student_id: str, lesson_id: str) -> Optional[dict]:
        """Get the current progress for a student in a specific lesson."""
        try:
            result = self.supabase.table("lesson_progress").select("*").eq(
                "student_id", student_id
            ).eq("lesson_id", lesson_id).execute()
            
            if result.data and len(result.data) > 0:
                return result.data[0]
            return None
        except Exception as e:
            _log.error(f"[Progress] Error getting lesson progress: {e}")
            return None

    async def create_or_update_progress(
        self,
        student_id: str,
        lesson_id: str,
        objectives_total: int,
        objectives_completed: list[int] = None,
        current_objective_index: int = 0,
        topics_covered: list[str] = None,
        key_points_learned: list[str] = None,
        last_ai_summary: str = "",
        status: str = "in_progress",
    ) -> dict:
        """Create or update lesson progress."""
        try:
            now = datetime.now(timezone.utc).isoformat()
            
            # Check if progress exists
            existing = await self.get_lesson_progress(student_id, lesson_id)
            
            data = {
                "student_id": student_id,
                "lesson_id": lesson_id,
                "objectives_total": objectives_total,
                "objectives_completed": objectives_completed or [],
                "current_objective_index": current_objective_index,
                "topics_covered": topics_covered or [],
                "key_points_learned": key_points_learned or [],
                "last_ai_summary": last_ai_summary,
                "status": status,
                "updated_at": now,
            }
            
            if existing:
                # Update existing
                result = self.supabase.table("lesson_progress").update(data).eq(
                    "id", existing["id"]
                ).execute()
                _log.info(f"[Progress] Updated progress: lesson={lesson_id[:8]}.. obj={current_objective_index}/{objectives_total}")
            else:
                # Create new
                data["created_at"] = now
                data["started_at"] = now
                result = self.supabase.table("lesson_progress").insert(data).execute()
                _log.info(f"[Progress] Created progress: lesson={lesson_id[:8]}.. student={student_id[:8]}..")
            
            return result.data[0] if result.data else data
        except Exception as e:
            _log.error(f"[Progress] Error saving progress: {e}")
            return {}

    async def mark_objective_completed(
        self,
        student_id: str,
        lesson_id: str,
        objective_index: int,
        objective_text: str,
        key_points: list[str] = None,
    ) -> dict:
        """Mark a specific objective as completed and save key points learned."""
        try:
            existing = await self.get_lesson_progress(student_id, lesson_id)
            if not existing:
                _log.warning(f"[Progress] No progress found to update for lesson {lesson_id}")
                return {}
            
            # Update completed objectives
            completed = existing.get("objectives_completed", [])
            if objective_index not in completed:
                completed.append(objective_index)
            
            # Update topics covered
            topics = existing.get("topics_covered", [])
            if objective_text and objective_text not in topics:
                topics.append(objective_text)
            
            # Update key points
            points = existing.get("key_points_learned", [])
            if key_points:
                for kp in key_points:
                    if kp not in points:
                        points.append(kp)
            
            # Determine status
            objectives_total = existing.get("objectives_total", 1)
            status = "completed" if len(completed) >= objectives_total else "in_progress"
            
            return await self.create_or_update_progress(
                student_id=student_id,
                lesson_id=lesson_id,
                objectives_total=objectives_total,
                objectives_completed=completed,
                current_objective_index=objective_index + 1,
                topics_covered=topics,
                key_points_learned=points,
                status=status,
            )
        except Exception as e:
            _log.error(f"[Progress] Error marking objective completed: {e}")
            return {}

    async def save_session_summary(
        self,
        student_id: str,
        lesson_id: str,
        summary: str,
    ) -> dict:
        """Save an AI-generated summary of what was covered in the session."""
        try:
            existing = await self.get_lesson_progress(student_id, lesson_id)
            if not existing:
                return {}
            
            return await self.create_or_update_progress(
                student_id=student_id,
                lesson_id=lesson_id,
                objectives_total=existing.get("objectives_total", 1),
                objectives_completed=existing.get("objectives_completed", []),
                current_objective_index=existing.get("current_objective_index", 0),
                topics_covered=existing.get("topics_covered", []),
                key_points_learned=existing.get("key_points_learned", []),
                last_ai_summary=summary,
                status=existing.get("status", "in_progress"),
            )
        except Exception as e:
            _log.error(f"[Progress] Error saving summary: {e}")
            return {}

    async def get_resume_context(self, student_id: str, lesson_id: str) -> dict:
        """Get context for resuming a lesson - what was covered, what's next."""
        progress = await self.get_lesson_progress(student_id, lesson_id)
        
        if not progress:
            return {
                "is_new_session": True,
                "has_previous_progress": False,
            }
        
        objectives_completed = progress.get("objectives_completed", [])
        objectives_total = progress.get("objectives_total", 1)
        completion_percent = round(len(objectives_completed) / objectives_total * 100) if objectives_total > 0 else 0
        
        return {
            "is_new_session": False,
            "has_previous_progress": True,
            "status": progress.get("status", "in_progress"),
            "completion_percent": completion_percent,
            "objectives_completed": objectives_completed,
            "objectives_total": objectives_total,
            "current_objective_index": progress.get("current_objective_index", 0),
            "topics_covered": progress.get("topics_covered", []),
            "key_points_learned": progress.get("key_points_learned", []),
            "last_ai_summary": progress.get("last_ai_summary", ""),
            "last_session_date": progress.get("updated_at", ""),
        }

    async def get_all_lesson_progress(self, student_id: str) -> list[dict]:
        """Get progress for all lessons for a student."""
        try:
            result = self.supabase.table("lesson_progress").select("*").eq(
                "student_id", student_id
            ).order("updated_at", desc=True).execute()
            return result.data or []
        except Exception as e:
            _log.error(f"[Progress] Error getting all progress: {e}")
            return []


# Singleton instance
session_progress_service = SessionProgressService()
