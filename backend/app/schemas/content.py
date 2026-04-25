from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class SubjectResponse(BaseModel):
    id: str
    name_fr: str
    name_ar: str
    description_fr: Optional[str] = None
    description_ar: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None
    order_index: int

    class Config:
        from_attributes = True


class ChapterResponse(BaseModel):
    id: str
    subject_id: str
    chapter_number: int
    title_fr: str
    title_ar: str
    description_fr: Optional[str] = None
    description_ar: Optional[str] = None
    difficulty_level: str
    estimated_hours: float
    order_index: int

    class Config:
        from_attributes = True


class LessonResponse(BaseModel):
    id: str
    chapter_id: str
    title_fr: str
    title_ar: str
    lesson_type: str
    content: dict
    learning_objectives: list
    duration_minutes: int
    order_index: int
    media_resources: list = []

    class Config:
        from_attributes = True


class ExerciseResponse(BaseModel):
    id: str
    lesson_id: str
    question_text_fr: str
    question_text_ar: str
    question_type: str
    difficulty_tier: str
    options: list
    explanation_fr: str
    explanation_ar: str
    hints: list
    estimated_time_seconds: int

    class Config:
        from_attributes = True


class ExerciseSubmit(BaseModel):
    exercise_id: str
    answer: Any


class ExerciseFeedback(BaseModel):
    is_correct: bool
    correct_answer: Any
    explanation_fr: str
    explanation_ar: str
    hint: Optional[str] = None
