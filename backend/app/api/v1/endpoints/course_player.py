from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_student
from app.schemas.course_player import (
    CourseIntentResolveRequest,
    CourseProgressUpdate,
    SlideAttemptCreate,
    SlideAttemptFeedback,
)
from app.services.course_player_service import course_player_service
from app.services.subject_access_service import subject_access_service


router = APIRouter(prefix="/course-player", tags=["course-player"])


def _deck_ids(deck: dict) -> tuple[set[str], set[str]]:
    activity_ids: set[str] = set()
    slide_ids: set[str] = set()
    for activity in deck.get("activities") or []:
        activity_ids.add(str(activity.get("id") or ""))
        for slide in activity.get("slides") or []:
            slide_ids.add(str(slide.get("id") or ""))
    return activity_ids, slide_ids


async def _authorised_deck(student: dict, lesson_id: str, deck_id: str) -> dict:
    if not subject_access_service.is_lesson_allowed(student, lesson_id):
        raise HTTPException(status_code=403, detail="Cette leçon n'est pas incluse dans votre accès")
    deck = await course_player_service.get_deck(lesson_id)
    if not deck or str(deck.get("id")) != str(deck_id):
        raise HTTPException(status_code=404, detail="Cours introuvable pour cette leçon")
    return deck


@router.post("/resolve")
async def resolve_course_intent(
    body: CourseIntentResolveRequest,
    student: dict = Depends(get_current_student),
):
    """Transforme une demande explicite de cours en route chapitre/leçon."""
    return await course_player_service.resolve_course_intent(body.text, student)


@router.get("/catalog")
async def get_course_catalog(student: dict = Depends(get_current_student)):
    """Matières accessibles et cours scénarisés ouvrables avec Moalim."""
    return await course_player_service.get_catalog(student)


@router.get("/lessons/{lesson_id}")
async def get_lesson_deck(lesson_id: str, student: dict = Depends(get_current_student)):
    if not subject_access_service.is_lesson_allowed(student, lesson_id):
        raise HTTPException(status_code=403, detail="Cette leçon n'est pas incluse dans votre accès")
    deck = await course_player_service.get_deck(lesson_id)
    if not deck:
        raise HTTPException(status_code=404, detail="Aucun cours publié pour cette leçon")
    progress = await course_player_service.get_progress(student["id"], str(deck.get("id") or ""))
    return {"deck": deck, "progress": progress}


@router.post("/progress")
async def save_course_progress(
    body: CourseProgressUpdate,
    student: dict = Depends(get_current_student),
):
    deck = await _authorised_deck(student, body.lesson_id, body.deck_id)
    activity_ids, slide_ids = _deck_ids(deck)
    if body.activity_id and body.activity_id not in activity_ids:
        raise HTTPException(status_code=400, detail="Activité étrangère à ce cours")
    if body.slide_id and body.slide_id not in slide_ids:
        raise HTTPException(status_code=400, detail="Diapositive étrangère à ce cours")
    persisted = await course_player_service.save_progress(student["id"], body.model_dump())
    if body.status == "completed":
        await course_player_service.mark_lesson_complete(student["id"], body.lesson_id)
    return {"saved": True, "persisted": persisted}


@router.post("/attempts", response_model=SlideAttemptFeedback)
async def save_slide_attempt(
    body: SlideAttemptCreate,
    student: dict = Depends(get_current_student),
):
    payload = body.model_dump()
    deck = await _authorised_deck(student, body.lesson_id, body.deck_id)
    _, slide_ids = _deck_ids(deck)
    if body.slide_id not in slide_ids:
        raise HTTPException(status_code=400, detail="Diapositive étrangère à ce cours")
    is_correct, feedback, should_requeue = await course_player_service.evaluate_attempt(payload)
    await course_player_service.save_attempt(student["id"], payload, is_correct, feedback)
    return SlideAttemptFeedback(
        is_correct=is_correct,
        feedback=feedback,
        should_requeue=should_requeue,
    )
