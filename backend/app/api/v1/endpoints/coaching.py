"""
Coaching Mode API Endpoints
Handles diagnostic, study plan generation, and progress tracking.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.dependencies import get_current_student
from app.services.diagnostic_service import diagnostic_service
from app.services.study_plan_service import study_plan_service
from app.services.bac_diagnostic_service import bac_diagnostic_service
from app.services.subject_access_service import canonical_subject_key, subject_access_service
from app.supabase_client import get_supabase_admin
from datetime import date

supabase = get_supabase_admin()

router = APIRouter(prefix="/coaching", tags=["coaching"])


def _require_subject(student: dict, subject_id: str) -> None:
    if not subject_access_service.is_subject_id_allowed(student, subject_id):
        raise HTTPException(status_code=403, detail="Cette matière n'est pas incluse dans votre accès")


def _filter_scores(student: dict, scores: dict) -> dict:
    context = subject_access_service.get_context(student)
    allowed = {canonical_subject_key(name) for name in context["subject_names"]}
    return {name: score for name, score in scores.items() if canonical_subject_key(name) in allowed}


class DiagnosticStartRequest(BaseModel):
    subject_id: str
    variation_seed: Optional[str] = None  # For generating different questions each time


class DiagnosticSessionStartRequest(BaseModel):
    subject_id: str
    num_questions: Optional[int] = 10


class NextQuestionRequest(BaseModel):
    session_id: str


class DiagnosticSubmitRequest(BaseModel):
    subject_id: str
    questions: list
    answers: dict  # {"0": "A", "1": "B", ...}


class GeneratePlanRequest(BaseModel):
    diagnostic_scores: dict  # {"Mathématiques": 45, "Physique": 60, ...}


class CompleteSessionRequest(BaseModel):
    session_id: str


@router.post("/start-diagnostic")
async def start_diagnostic(
    data: DiagnosticStartRequest,
    student: dict = Depends(get_current_student)
):
    """
    Start a diagnostic quiz for a subject.
    Generates 10 QCM/association questions grounded in real BAC exams.
    Each call with a different variation_seed generates different questions.
    """
    _require_subject(student, data.subject_id)
    try:
        questions = await diagnostic_service.generate_diagnostic_questions(
            subject_id=data.subject_id,
            num_questions=10,
            variation_seed=data.variation_seed,
            student_id=student['id'],
        )

        if not questions:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate questions. Please try again."
            )

        return {
            "subject_id": data.subject_id,
            "questions": questions,
            "total_questions": len(questions)
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start-diagnostic-session")
async def start_diagnostic_session(
    data: DiagnosticSessionStartRequest,
    student: dict = Depends(get_current_student)
):
    """
    Start a diagnostic session for question-by-question generation.
    Returns a session_id that can be used to generate questions one by one.
    """
    _require_subject(student, data.subject_id)
    try:
        session_id = await diagnostic_service.start_diagnostic_session(
            subject_id=data.subject_id,
            num_questions=data.num_questions or 10,
            student_id=student['id'],
        )

        return {
            "session_id": session_id,
            "subject_id": data.subject_id,
            "total_questions": data.num_questions or 10,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/next-diagnostic-question")
async def next_diagnostic_question(
    data: NextQuestionRequest,
    student: dict = Depends(get_current_student)
):
    """
    Generate the next question in a diagnostic session.
    Returns the question or null if all questions have been generated.
    Retries up to 3 times if the LLM returns a rejected/invalid question,
    to avoid permanently blocking the frontend at a given question index.
    """
    try:
        session = diagnostic_service._sessions.get(data.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        if session.get("student_id") and str(session.get("student_id")) != str(student["id"]):
            raise HTTPException(status_code=404, detail="Session not found")
        _require_subject(student, str(session.get("subject_id") or ""))

        already_done = session.get('questions_generated', 0) >= session.get('num_questions', 10)
        if already_done:
            return {"question": None, "completed": True}

        # Retry up to 3 times: a None return from generate_next_question means
        # the LLM output was rejected (bad chapter, bad pairs, …) — the session
        # counter was NOT incremented, so retrying is safe.
        question = None
        for attempt in range(3):
            question = await diagnostic_service.generate_next_question(
                session_id=data.session_id,
            )
            if question is not None:
                break
            # Check if the session is now actually complete (counter caught up)
            if session.get('questions_generated', 0) >= session.get('num_questions', 10):
                break
            print(f"[Diagnostic] next-question attempt {attempt+1} returned None, retrying…")

        if question is None:
            # After 3 failed attempts check if truly done or just struggling
            truly_done = session.get('questions_generated', 0) >= session.get('num_questions', 10)
            return {"question": None, "completed": truly_done}

        return {
            "question": question,
            "completed": False,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/submit-diagnostic")
async def submit_diagnostic(
    data: DiagnosticSubmitRequest,
    student: dict = Depends(get_current_student)
):
    """
    Submit diagnostic answers and get evaluation results.
    Returns score, weak topics, and strong topics.
    """
    _require_subject(student, data.subject_id)
    try:
        result = await diagnostic_service.evaluate_diagnostic(
            student_id=student['id'],
            subject_id=data.subject_id,
            questions=data.questions,
            answers=data.answers
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generate-plan")
async def generate_study_plan(
    data: GeneratePlanRequest,
    student: dict = Depends(get_current_student)
):
    """
    Generate a personalized study plan based on diagnostic results.
    Creates sessions scheduled until exam date.
    """
    try:
        diagnostic_scores = _filter_scores(student, data.diagnostic_scores)
        if not diagnostic_scores:
            raise HTTPException(status_code=400, detail="Aucune matière autorisée dans les résultats du diagnostic")
        result = await study_plan_service.generate_plan(
            student['id'],
            diagnostic_scores
        )
        
        return {
            "success": True,
            "plan_id": result["plan_id"],
            "days_remaining": result["days_remaining"],
            "total_hours": result["total_hours"],
            "sessions_count": result["sessions_count"],
            "phase_split": result.get("phase_split", {}),
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/regenerate-plan")
async def regenerate_study_plan(
    student: dict = Depends(get_current_student)
):
    """
    Regenerate study plan based on latest diagnostic results.
    Automatically fetches all previous diagnostic scores and creates a new optimized plan.
    """
    try:
        print(f"[API] Regenerate plan called for student: {student['id']}")
        
        # Get all latest diagnostic scores for this student
        diagnostic_results = supabase.table('diagnostic_results').select(
            'score, subjects(name_fr), created_at'
        ).eq('student_id', student['id']).eq('evaluation_type', 'diagnostic').order(
            'created_at', desc=True
        ).execute()
        
        print(f"[API] Found {len(diagnostic_results.data)} diagnostic results")
        for r in diagnostic_results.data:
            print(f"[API]   - {r.get('subjects', {}).get('name_fr')}: {r.get('score')}")
        
        if not diagnostic_results.data:
            raise HTTPException(status_code=400, detail="Aucun résultat de diagnostic trouvé. Veuillez d'abord passer un diagnostic.")
        
        # Build diagnostic scores dict from latest results
        diagnostic_scores = {}
        seen_subjects = set()
        
        for result in diagnostic_results.data:
            subject = result.get('subjects')
            if subject:
                subject_name = subject.get('name_fr')
                if subject_name and subject_name not in seen_subjects:
                    diagnostic_scores[subject_name] = float(result.get('score', 0))
                    seen_subjects.add(subject_name)
        
        diagnostic_scores = _filter_scores(student, diagnostic_scores)
        print(f"[API] Final diagnostic_scores to pass: {diagnostic_scores}")
        
        if not diagnostic_scores:
            raise HTTPException(status_code=400, detail="Aucune note de diagnostic valide trouvée.")
        
        # Generate new plan
        result = await study_plan_service.generate_plan(
            student['id'],
            diagnostic_scores
        )
        
        return {
            "success": True,
            "plan_id": result["plan_id"],
            "days_remaining": result["days_remaining"],
            "total_hours": result["total_hours"],
            "sessions_count": result["sessions_count"],
            "phase_split": result.get("phase_split", {}),
            "diagnostic_scores": diagnostic_scores
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plan")
async def get_plan(
    student: dict = Depends(get_current_student)
):
    """
    Get the active study plan for the current student.
    Returns plan details, sessions count, and progress.
    """
    try:
        plan = await study_plan_service.get_active_plan(student['id'])
        
        if not plan:
            return {"has_plan": False, "plan": None}

        plan["diagnostic_scores"] = _filter_scores(student, plan.get("diagnostic_scores") or {})
        return {"has_plan": True, "plan": plan}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/today")
async def get_today_schedule(
    student: dict = Depends(get_current_student)
):
    """
    Get today's scheduled study sessions.
    Returns list of sessions with subject and chapter info.
    """
    try:
        sessions = await study_plan_service.get_today_schedule(student['id'])
        allowed_ids = set(subject_access_service.get_context(student)["subject_ids"])
        sessions = [session for session in sessions if str(session.get("subject_id")) in allowed_ids]
        
        return {
            "date": date.today().isoformat(),
            "sessions": sessions,
            "count": len(sessions)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-sessions")
async def get_all_sessions(
    student: dict = Depends(get_current_student)
):
    """
    Get all sessions grouped by date and subject.
    Returns complete program with all sessions organized.
    """
    try:
        data = await study_plan_service.get_all_sessions(student['id'])
        context = subject_access_service.get_context(student)
        allowed_ids = set(context["subject_ids"])
        allowed_names = {canonical_subject_key(name) for name in context["subject_names"]}

        sessions_by_date = {}
        for session_date, sessions in (data.get("sessions_by_date") or {}).items():
            scoped = [session for session in sessions if str(session.get("subject_id")) in allowed_ids]
            if scoped:
                sessions_by_date[session_date] = scoped

        sessions_by_subject = {
            name: sessions
            for name, sessions in (data.get("sessions_by_subject") or {}).items()
            if canonical_subject_key(name) in allowed_names
        }
        flat_sessions = [session for sessions in sessions_by_date.values() for session in sessions]
        data = {
            **data,
            "sessions_by_date": sessions_by_date,
            "sessions_by_subject": sessions_by_subject,
            "total_sessions": len(flat_sessions),
            "total_duration_minutes": sum(session.get("duration_minutes", 0) for session in flat_sessions),
            "completed_duration_minutes": sum(
                session.get("duration_minutes", 0)
                for session in flat_sessions
                if session.get("status") == "completed"
            ),
        }
        return data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/complete-session")
async def complete_session(
    data: CompleteSessionRequest,
    student: dict = Depends(get_current_student)
):
    """
    Mark a study session as completed.
    Updates progress and recalculates percentages.
    """
    try:
        result = await study_plan_service.mark_session_completed(
            session_id=data.session_id,
            student_id=student['id']
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/progress")
async def get_progress(
    student: dict = Depends(get_current_student)
):
    """
    Get overall and per-subject progress.
    Returns percentages for dashboard display.
    """
    try:
        progress = await study_plan_service.get_progress(student['id'])
        allowed_ids = set(subject_access_service.get_context(student)["subject_ids"])
        progress["subject_progress"] = {
            subject_id: value
            for subject_id, value in (progress.get("subject_progress") or {}).items()
            if str(subject_id) in allowed_ids
        }
        return progress
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/exam-countdown")
async def get_exam_countdown(
    student: dict = Depends(get_current_student)
):
    """
    Get countdown to BAC exam (June 4, 2026).
    Returns days and hours remaining.
    """
    try:
        days_remaining = study_plan_service.calculate_days_until_exam()
        exam_date = study_plan_service.exam_date
        
        return {
            "exam_date": exam_date.isoformat(),
            "days_remaining": days_remaining,
            "hours_remaining": days_remaining * 24
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diagnostic-history")
async def get_diagnostic_history(
    student: dict = Depends(get_current_student)
):
    """
    Get all past diagnostic results for the student.
    """
    try:
        history = await diagnostic_service.get_diagnostic_history(student['id'])
        
        return {
            "results": history,
            "count": len(history)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/proficiency")
async def get_proficiency(
    student: dict = Depends(get_current_student)
):
    """
    Get student proficiency data from answer history agent.
    Returns overall level, per-subject scores, lacunes, strengths, progression.
    """
    try:
        from app.services.student_proficiency_service import proficiency_service
        data = await proficiency_service.get_dashboard_data(student['id'])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/adaptive-next")
async def get_adaptive_next(
    student: dict = Depends(get_current_student)
):
    """
    Get the best next study session recommendation based on live proficiency.
    Uses ZPD, spaced repetition, BAC coefficients to decide what to study next.
    """
    try:
        recommendation = await study_plan_service.get_adaptive_next_session(student['id'])
        return recommendation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/adapt-plan")
async def adapt_plan(
    student: dict = Depends(get_current_student)
):
    """
    Re-prioritize the study plan based on live proficiency data.
    Reorders pending sessions to focus on lacunes and high-coefficient subjects.
    """
    try:
        result = await study_plan_service.adapt_plan_from_proficiency(student['id'])
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/coaching-context")
async def get_coaching_context(
    student: dict = Depends(get_current_student)
):
    """
    Get full coaching context combining proficiency + plan + recommendation.
    Used by the frontend to show adaptive coaching dashboard.
    """
    try:
        context = await study_plan_service.get_coaching_session_context(student['id'])
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ═══════════════════════════════════════════════════════════════════════════════
# LESSON PROGRESS ENDPOINTS - Session memory for coaching mode
# ═══════════════════════════════════════════════════════════════════════════════

from app.services.session_progress_service import session_progress_service


class MarkObjectiveRequest(BaseModel):
    lesson_id: str
    objective_index: int
    objective_text: str
    key_points: Optional[list[str]] = None


class SaveSummaryRequest(BaseModel):
    lesson_id: str
    summary: str


@router.get("/lesson-progress/{lesson_id}")
async def get_lesson_progress(
    lesson_id: str,
    student: dict = Depends(get_current_student)
):
    """
    Get progress for a specific lesson.
    Returns objectives completed, topics covered, and resume context.
    """
    try:
        context = await session_progress_service.get_resume_context(
            student_id=student['id'],
            lesson_id=lesson_id
        )
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/all-lesson-progress")
async def get_all_lesson_progress(
    student: dict = Depends(get_current_student)
):
    """Get progress for all lessons for the current student."""
    try:
        progress_list = await session_progress_service.get_all_lesson_progress(student['id'])
        return {"progress": progress_list}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/mark-objective")
async def mark_objective_completed(
    data: MarkObjectiveRequest,
    student: dict = Depends(get_current_student)
):
    """Mark a learning objective as completed."""
    try:
        result = await session_progress_service.mark_objective_completed(
            student_id=student['id'],
            lesson_id=data.lesson_id,
            objective_index=data.objective_index,
            objective_text=data.objective_text,
            key_points=data.key_points,
        )
        return {"success": True, "progress": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── In-memory session store for BAC diagnostic (questions with answers) ──
_bac_diag_sessions: dict[str, list] = {}


class BacDiagnosticSubmitRequest(BaseModel):
    session_id: str
    answers: dict  # {"1": "a", "2": "c", ...}


@router.get("/bac-diagnostic/questions")
async def get_bac_diagnostic_questions():
    """
    Return 20 QCM questions from the real BAC exam bank (12 SVT + 8 PC).
    A session_id is generated to allow server-side answer checking.
    This endpoint is public — no auth required — to maximise conversion.
    """
    import uuid as _uuid
    questions = bac_diagnostic_service.get_questions(n_svt=7, n_pc=7, n_math=6)
    session_id = str(_uuid.uuid4())
    # Store with correct answers server-side
    _bac_diag_sessions[session_id] = questions
    # Strip _correct before sending to client
    client_questions = [{k: v for k, v in q.items() if k != "_correct"} for q in questions]
    return {"session_id": session_id, "questions": client_questions, "total": len(client_questions)}


@router.post("/bac-diagnostic/submit")
async def submit_bac_diagnostic(data: BacDiagnosticSubmitRequest):
    """
    Score the diagnostic and return:
      - score /20, bac_note_predicted, gain_if_subscribed
      - per-subject & per-domain breakdown
      - weak_domains (worst first)
      - 28-day personalised plan
    This endpoint is public — no auth required.
    """
    session_questions = _bac_diag_sessions.get(data.session_id)
    if not session_questions:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    result = bac_diagnostic_service.score(session_questions, data.answers)
    # Clean up session after scoring
    _bac_diag_sessions.pop(data.session_id, None)
    return result


@router.post("/save-session-summary")
async def save_session_summary(
    data: SaveSummaryRequest,
    student: dict = Depends(get_current_student)
):
    """Save an AI-generated summary of what was covered in the session."""
    try:
        result = await session_progress_service.save_session_summary(
            student_id=student['id'],
            lesson_id=data.lesson_id,
            summary=data.summary,
        )
        return {"success": True, "progress": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
