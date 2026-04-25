from fastapi import APIRouter, Depends, HTTPException
from app.supabase_client import get_supabase, get_supabase_admin
from app.schemas.content import SubjectResponse, ChapterResponse, LessonResponse, ExerciseResponse
from app.dependencies import get_current_student

router = APIRouter(prefix="/content", tags=["content"])
supabase = get_supabase()


@router.get("/subjects")
async def get_subjects():
    try:
        result = supabase.table('subjects').select('*').order('order_index').execute()
        return result.data if result.data else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get subjects: {str(e)}")


@router.get("/subjects/{subject_id}/chapters")
async def get_chapters(subject_id: str):
    try:
        result = supabase.table('chapters').select('*').eq('subject_id', subject_id).order('order_index').execute()
        return result.data if result.data else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get chapters: {str(e)}")


@router.get("/chapters/{chapter_id}/lessons")
async def get_lessons(chapter_id: str):
    try:
        print(f"[Content] Fetching lessons for chapter_id: {chapter_id}")
        result = supabase.table('lessons').select('*').eq('chapter_id', chapter_id).order('order_index').execute()
        lessons = result.data if result.data else []
        print(f"[Content] Found {len(lessons)} lessons for chapter_id: {chapter_id}")

        # Auto-create a default lesson if the chapter has none
        # (coaching plan sessions reference chapters directly — the learning
        # session needs a lesson row to start, and content will be grounded
        # from the RAG / cadres de référence at runtime).
        if not lessons:
            print(f"[Content] No lessons found; auto-creating a default lesson for chapter {chapter_id}")
            admin = get_supabase_admin()
            chapter_res = admin.table('chapters').select(
                'id, title_fr, title_ar, subject_id, subjects(name_fr)'
            ).eq('id', chapter_id).single().execute()

            if not chapter_res.data:
                raise HTTPException(status_code=404, detail="Chapter not found")

            chapter = chapter_res.data
            subject_name = (chapter.get('subjects') or {}).get('name_fr', '')
            default_lesson = {
                "chapter_id": chapter_id,
                "title_fr": chapter['title_fr'],
                "title_ar": chapter.get('title_ar') or chapter['title_fr'],
                "lesson_type": "theory",
                "content": {},
                "learning_objectives": [
                    f"Comprendre les notions clés de : {chapter['title_fr']}",
                    f"Appliquer les concepts à des exercices de type BAC ({subject_name})",
                    "Consolider les acquis par la pratique",
                ],
                "duration_minutes": 60,
                "order_index": 0,
            }
            insert_res = admin.table('lessons').insert(default_lesson).execute()
            lessons = insert_res.data if insert_res.data else []
            print(f"[Content] Created default lesson id={lessons[0]['id'] if lessons else 'unknown'}")

        return lessons
    except HTTPException:
        raise
    except Exception as e:
        print(f"[Content] Error fetching lessons: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get lessons: {str(e)}")


@router.get("/lessons/{lesson_id}/exercises")
async def get_exercises(lesson_id: str):
    try:
        result = supabase.table('exercises').select('*').eq('lesson_id', lesson_id).order('order_index').execute()
        return result.data if result.data else []
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get exercises: {str(e)}")
