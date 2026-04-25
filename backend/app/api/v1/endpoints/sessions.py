from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime
from app.supabase_client import get_supabase_admin
from app.schemas.session import SessionStart, SessionResponse, SessionEnd, StudentProfileResponse
from app.dependencies import get_current_student

router = APIRouter(prefix="/sessions", tags=["sessions"])
supabase = get_supabase_admin()


@router.post("/start")
async def start_session(
    data: SessionStart,
    student: dict = Depends(get_current_student)
):
    try:
        import uuid
        session_data = {
            "id": str(uuid.uuid4()),
            "student_id": student['id'],
            "lesson_id": str(data.lesson_id),
            "start_time": datetime.utcnow().isoformat(),
        }
        
        result = supabase.table('learning_sessions').insert(session_data).execute()
        
        if result.data:
            return result.data[0]
        else:
            raise HTTPException(status_code=500, detail="Failed to create session")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start session: {str(e)}")


@router.post("/end")
async def end_session(
    data: SessionEnd,
    student: dict = Depends(get_current_student)
):
    try:
        # Get session
        session_result = supabase.table('learning_sessions').select('*').eq('id', str(data.session_id)).eq('student_id', student['id']).execute()
        
        if not session_result.data:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session = session_result.data[0]
        
        # Calculate duration
        end_time = datetime.utcnow()
        start_time = datetime.fromisoformat(session['start_time'].replace('Z', '+00:00'))
        duration_seconds = int((end_time - start_time).total_seconds())
        
        # Update session
        supabase.table('learning_sessions').update({
            "end_time": end_time.isoformat(),
            "duration_minutes": duration_seconds // 60
        }).eq('id', str(data.session_id)).execute()
        
        # Update student profile study time
        profile_result = supabase.table('student_profiles').select('*').eq('student_id', student['id']).execute()
        
        if profile_result.data:
            profile = profile_result.data[0]
            new_study_time = (profile.get('total_study_time_minutes', 0) or 0) + (duration_seconds // 60)
            supabase.table('student_profiles').update({
                "total_study_time_minutes": new_study_time
            }).eq('student_id', student['id']).execute()
        
        return {"message": "Session ended", "duration_seconds": duration_seconds}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to end session: {str(e)}")


@router.get("/profile")
async def get_profile(
    student: dict = Depends(get_current_student)
):
    try:
        result = supabase.table('student_profiles').select('*').eq('student_id', student['id']).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Profile not found")
        
        profile = result.data[0]
        
        # Return profile with schema-compatible fields
        return {
            "proficiency_level": profile.get('proficiency_level', 'intermediate'),
            "learning_style": profile.get('learning_style', 'Socratique'),
            "strengths": profile.get('strengths', []),
            "weaknesses": profile.get('weaknesses', []),
            "total_study_time_minutes": profile.get('total_study_time_minutes', 0),
            "sessions_completed": profile.get('sessions_completed', 0),
            "exercises_completed": profile.get('exercises_completed', 0),
            "average_score": profile.get('average_score', 0.0)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get profile: {str(e)}")
