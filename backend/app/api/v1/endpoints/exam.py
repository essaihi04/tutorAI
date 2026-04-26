"""
Exam Mode API Endpoints
Handles exam listing, question serving, answer evaluation, and history.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from app.dependencies import get_current_student
from app.services.exam_service import exam_service

router = APIRouter(prefix="/exam", tags=["exam"])


class EvaluateAnswerRequest(BaseModel):
    exam_id: str
    question_index: int
    student_answer: str
    student_image: Optional[str] = None  # base64 image data (photo or drawing)
    attempt_id: Optional[str] = None  # in-progress attempt to persist score on


class ExtractTextRequest(BaseModel):
    image_base64: str
    question_content: Optional[str] = ""  # Optional context for better extraction
    subject: Optional[str] = ""  # Subject for context-specific OCR (math, physique, chimie, svt)


class SubmitExamRequest(BaseModel):
    exam_id: str
    answers: dict  # {"0": "answer text", "1": "answer text", ...}
    mode: str = "practice"  # "practice" | "real"
    duration_seconds: int = 0
    attempt_id: Optional[str] = None  # Existing in-progress attempt to finalize


class StartExamRequest(BaseModel):
    exam_id: str
    mode: str = "practice"


class SaveProgressRequest(BaseModel):
    attempt_id: str
    answers: Optional[dict] = None
    current_question_index: Optional[int] = None
    duration_seconds: Optional[int] = None


@router.get("/list")
async def list_exams(
    subject: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
):
    """List available exams, optionally filtered by subject and/or year."""
    exams = exam_service.list_exams(subject=subject, year=year)
    return {"exams": exams, "count": len(exams)}


@router.get("/stats")
async def get_exam_stats():
    """
    Return aggregate statistics about the exam bank:
    - total_exams  : total number of national BAC exams indexed
    - total_questions : total number of questions across all exams
    - by_subject   : per-subject breakdown {subject, exams, questions, years, points}
    - year_range   : [min_year, max_year]

    Used by the frontend ExamHub to display a header stats panel.
    """
    from app.services.exam_bank_service import exam_bank
    stats = exam_bank.get_stats()
    # Return only the useful fields for the frontend (skip 'topics' which is heavy)
    return {
        "total_exams": stats.get("total_exams", 0),
        "total_questions": stats.get("total_questions", 0),
        "by_subject": stats.get("by_subject", []),
        "year_range": stats.get("year_range", []),
        "years": stats.get("years", []),
    }


@router.get("/detail/{exam_id}")
async def get_exam(exam_id: str):
    """Get full exam content with structured questions."""
    exam = exam_service.get_exam(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Examen introuvable")
    return exam


@router.get("/question/{exam_id}/{question_index}")
async def get_question(exam_id: str, question_index: int):
    """Get a single question with its context."""
    question = exam_service.get_question(exam_id, question_index)
    if not question:
        raise HTTPException(status_code=404, detail="Question introuvable")
    return question


@router.get("/assets/{exam_id}/{filename}")
async def get_asset(exam_id: str, filename: str):
    """Serve exam image assets (schemas, tables)."""
    assets_dir = exam_service.get_assets_dir(exam_id)
    if not assets_dir:
        raise HTTPException(status_code=404, detail="Assets introuvables")
    file_path = assets_dir / filename
    if not file_path.exists() or not file_path.is_file():
        raise HTTPException(status_code=404, detail="Fichier introuvable")
    return FileResponse(str(file_path), media_type="image/png")


@router.post("/evaluate")
async def evaluate_answer(
    data: EvaluateAnswerRequest,
    student: dict = Depends(get_current_student),
):
    """Evaluate a single answer using LLM (practice mode).

    When ``attempt_id`` is provided, the per-question score is persisted on the
    in-progress attempt so the dashboard reflects practice progress without
    requiring a final submission.
    """
    result = await exam_service.evaluate_answer(
        exam_id=data.exam_id,
        question_index=data.question_index,
        student_answer=data.student_answer,
        student_image=data.student_image,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])

    if data.attempt_id and "score" in result:
        await exam_service.record_practice_score(
            student_id=student["id"],
            attempt_id=data.attempt_id,
            question_index=data.question_index,
            score=float(result.get("score") or 0),
            points_max=float(result.get("points_max") or 0),
        )

    return result


@router.post("/extract-text")
async def extract_text_from_image(data: ExtractTextRequest):
    """
    Extract text from a student's image (photo of handwritten answer).
    Returns the extracted text so it can be displayed in the input field before evaluation.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        from app.services.vision_service import analyze_student_image
        
        result = await analyze_student_image(
            image_base64=data.image_base64,
            question_content=data.question_content or "Réponse de l'élève",
            correction_content="",  # No correction needed for extraction only
            question_type="open",
            subject=data.subject or "",
        )
        
        # Return result even if there's an error - let frontend handle gracefully
        return {
            "extracted_text": result.get("extracted_text", ""),
            "elements": result.get("elements", ""),
            "curve_analysis": result.get("curve_analysis"),
            "error": result.get("error"),  # Include error for frontend to display
        }
    except Exception as e:
        logger.error(f"Extract text failed: {e}")
        # Return empty result with error instead of raising exception
        return {
            "extracted_text": "",
            "elements": "",
            "curve_analysis": None,
            "error": str(e),
        }


class ExplainRequest(BaseModel):
    exam_id: str
    question_index: int
    mode: str = "before"  # "before" (hints) or "after" (full explanation)
    # Optional fields used in "after" mode to decorticate the student's actual response
    student_answer: Optional[str] = None
    student_score: Optional[float] = None
    student_points_max: Optional[float] = None
    evaluator_feedback: Optional[str] = None


@router.post("/explain")
async def explain_question(data: ExplainRequest):
    """Generate an explanation for a question.

    ``mode='before'`` — Socratic guidance, never reveal the answer.
    ``mode='after'``  — Diagnostic correction of the student's specific answer
                        (decorticate, cite phrases, link to course).
    """
    question = exam_service.get_question(data.exam_id, data.question_index)
    if not question:
        raise HTTPException(status_code=404, detail="Question introuvable")

    from app.services.llm_service import llm_service

    q_content = question.get("content", "")
    q_type = question.get("type", "open")
    q_points = question.get("points", 0)
    parent = question.get("parent_content", "")
    exercise_ctx = question.get("exercise_context", "")
    subject = data.exam_id.split("-")[0].upper() if "-" in data.exam_id else "SVT"
    correction = question.get("correction", {})
    corr_text = correction.get("content", "") if isinstance(correction, dict) else ""

    context_block = ""
    if exercise_ctx:
        context_block = f"\nContexte de l'exercice : {exercise_ctx}"
    if parent:
        context_block += f"\nÉnoncé parent : {parent}"

    if data.mode == "before":
        prompt = f"""Tu es un professeur marocain de {subject} au BAC. L'élève demande de l'AIDE AVANT de répondre.
Ton rôle : guide socratique qui oriente SANS jamais donner la réponse.

Question ({q_type}, {q_points} pts) : {q_content}{context_block}

INTERDICTION ABSOLUE :
- Ne révèle JAMAIS la réponse, ni partiellement, ni en exemple, ni en reformulation déguisée.
- Pour QCM / Vrai-Faux / Association : ne désigne AUCUNE option comme correcte.

Réponds avec ces sections markdown (sois CONCIS, 6-10 phrases au total) :

## Ce qui est demandé
Reformule en mots simples : « On te demande de… »

## Verbe-clé de la consigne
Identifie le verbe-action (décrire / justifier / comparer / démontrer / déduire / interpréter…) et dis en UNE phrase ce que ce verbe impose comme rédaction.

## Notions du cours à mobiliser
Liste 2 à 4 notions / définitions / lois / mécanismes nécessaires — SANS les appliquer à la question.

## Plan à remplir
Donne un canevas en étapes numérotées avec ce qu'il faut FAIRE à chaque étape (pas le contenu).
{("- QCM → comment éliminer les distracteurs."  if q_type == "qcm" else "")}
{("- Vrai/Faux → comment chercher un contre-exemple ou une exception." if q_type == "vrai_faux" else "")}
{("- Association → quel critère discriminant utiliser." if q_type == "association" else "")}

## Question pour démarrer
Termine par UNE question ouverte qui force l'élève à observer / se rappeler — pas à deviner la réponse."""

    else:  # after — diagnostic + corrective
        student_answer = (data.student_answer or "").strip()
        score_line = ""
        if data.student_score is not None and data.student_points_max:
            score_line = f"\nNote obtenue : {data.student_score}/{data.student_points_max}"
        student_block = (
            f"\nRÉPONSE DE L'ÉLÈVE (à analyser et citer textuellement) :\n«{student_answer}»"
            if student_answer
            else "\nL'élève n'a pas écrit de texte (peut-être uniquement un schéma)."
        )
        eval_block = (
            f"\nRetour de l'évaluateur automatique (référence interne, ne pas le citer mot pour mot) :\n{data.evaluator_feedback}"
            if (data.evaluator_feedback or "").strip()
            else ""
        )

        prompt = f"""Tu es un professeur marocain de {subject} au BAC qui CORRIGE UNE COPIE.
Tu ne fais PAS un cours générique : tu décortiques la réponse SPÉCIFIQUE de cet élève.

Question ({q_type}, {q_points} pts) : {q_content}{context_block}
{student_block}{score_line}

Correction officielle (référence) :
{corr_text}{eval_block}

Réponds avec ces sections markdown (sois PRÉCIS et CONCIS, 8-12 phrases au total) :

## ✅ Ce qui fonctionne
Cite TEXTUELLEMENT entre guillemets « … » une ou deux phrases JUSTES de l'élève et explique pourquoi c'est bon. Si rien n'est juste, dis-le avec tact.

## ⚠️ Ce qui manque ou est imprécis
Pour CHAQUE élément attendu dans la correction officielle :
- dis si l'élève l'a écrit (cite ses mots) ou pas
- explique pourquoi c'est important pour la note BAC
Si une phrase de l'élève est FAUSSE, cite-la entre guillemets et corrige-la avec l'explication.

## 📝 Comment rédiger pour avoir tous les points
Donne UNE version modèle courte et structurée, telle qu'un correcteur BAC l'attend (reformulée — pas un copier-coller).

## 📚 Concept du cours à retenir
Relie les erreurs à un mécanisme / définition / loi précis (pas de vague).

## ⚡ Piège typique
UN piège que beaucoup d'élèves font sur ce genre de question.

## 🎯 Action suivante
UNE phrase : que doit-il refaire / réviser maintenant ?"""

    try:
        response = await llm_service.chat(
            messages=[{"role": "user", "content": prompt}],
            system_prompt=f"Professeur expert de {subject} au BAC marocain. Tu expliques de façon claire, structurée et pédagogique.",
            temperature=0.3,
            max_tokens=1200,
        )
        return {"explanation": response, "mode": data.mode, "question_index": data.question_index}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/start")
async def start_exam(
    data: StartExamRequest,
    student: dict = Depends(get_current_student),
):
    """Create an in-progress exam attempt.

    Called by the frontend as soon as the student opens an exam (real or
    practice) so that dashboards can show activity even before submission.
    Idempotent: if an in-progress attempt already exists, it is reused.
    """
    result = await exam_service.start_attempt(
        student_id=student["id"],
        exam_id=data.exam_id,
        mode=data.mode,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/save-progress")
async def save_exam_progress(
    data: SaveProgressRequest,
    student: dict = Depends(get_current_student),
):
    """Persist partial progress for an in-progress exam attempt."""
    result = await exam_service.save_progress(
        student_id=student["id"],
        attempt_id=data.attempt_id,
        answers=data.answers,
        current_question_index=data.current_question_index,
        duration_seconds=data.duration_seconds,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.post("/submit")
async def submit_exam(
    data: SubmitExamRequest,
    student: dict = Depends(get_current_student),
):
    """Submit a complete exam for evaluation (practice or real mode)."""
    result = await exam_service.submit_exam(
        student_id=student["id"],
        exam_id=data.exam_id,
        answers=data.answers,
        mode=data.mode,
        duration_seconds=data.duration_seconds,
        attempt_id=data.attempt_id,
    )
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result


@router.get("/history")
async def get_history(
    student: dict = Depends(get_current_student),
    limit: int = Query(20, le=100),
):
    """Get exam attempt history for the current student."""
    history = await exam_service.get_history(student["id"], limit=limit)
    return {"history": history, "count": len(history)}


@router.get("/my-stats")
async def get_my_exam_stats(
    student: dict = Depends(get_current_student),
):
    """
    Return aggregated exam statistics for the current student.

    Used by the ExamHub page to display a personal progress panel and
    fuel the "Share my progress" feature.
    """
    return await exam_service.get_student_exam_stats(student["id"])


# ──────────────────────────────────────────────
# EXTRACTED EXAMS (from PDF extraction)
# ──────────────────────────────────────────────

@router.get("/extracted/list")
async def list_extracted_exams(
    subject: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
):
    """List extracted exams from exam_documents table."""
    from app.supabase_client import supabase_admin

    result = supabase_admin.table("exam_documents").select(
        "id, created_at, is_published"
    ).order("year", desc=True).execute()

    exams = []
    for row in result.data or []:
        meta = exam_service.get_extracted_exam_meta(row["id"])
        if not meta:
            continue
        if subject and str(meta.get("subject", "")).lower() != subject.lower():
            continue
        if year and meta.get("year") != year:
            continue
        exams.append({
            "id": meta["id"],
            "subject": meta.get("subject"),
            "year": meta.get("year"),
            "session": meta.get("session"),
            "exam_title": meta.get("exam_title"),
            "created_at": row.get("created_at"),
            "is_published": row.get("is_published", False),
        })

    return {"exams": exams, "count": len(exams)}


@router.get("/extracted/{doc_id}")
async def get_extracted_exam(doc_id: str):
    """Get a specific extracted exam with full content."""
    from app.supabase_client import supabase_admin
    
    result = supabase_admin.table("exam_documents").select("*").eq("id", doc_id).single().execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Examen introuvable")
    
    return result.data


@router.get("/extracted-page-image/{job_id}/{page_number}")
async def get_extracted_page_image(job_id: str, page_number: int):
    """Serve a page image from an extraction job."""
    from fastapi.responses import Response
    from app.supabase_client import supabase_admin
    import base64

    result = supabase_admin.table("exam_extraction_pages") \
        .select("image_base64") \
        .eq("job_id", job_id) \
        .eq("page_number", page_number) \
        .limit(1) \
        .execute()

    if not result.data or not result.data[0].get("image_base64"):
        raise HTTPException(status_code=404, detail="Image introuvable")

    image_bytes = base64.b64decode(result.data[0]["image_base64"])
    return Response(content=image_bytes, media_type="image/png")


@router.get("/extracted-figure-image/{job_id}/{page_number}/{image_index}")
async def get_extracted_figure_image(job_id: str, page_number: int, image_index: int):
    """Serve an individual extracted figure/document image from OCR."""
    from fastapi.responses import FileResponse
    from app.supabase_client import supabase_admin
    from pathlib import Path

    result = supabase_admin.table("exam_extraction_pages") \
        .select("extracted_images") \
        .eq("job_id", job_id) \
        .eq("page_number", page_number) \
        .limit(1) \
        .execute()

    if not result.data or not result.data[0].get("extracted_images"):
        raise HTTPException(status_code=404, detail="Image introuvable")

    images = result.data[0]["extracted_images"]
    if image_index < 0 or image_index >= len(images):
        raise HTTPException(status_code=404, detail="Index image introuvable")

    img_path = images[image_index].get("path", "")
    if not img_path or not Path(img_path).exists():
        raise HTTPException(status_code=404, detail="Fichier image introuvable")

    return FileResponse(img_path, media_type="image/png")
