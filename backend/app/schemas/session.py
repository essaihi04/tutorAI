from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SessionStart(BaseModel):
    lesson_id: str
    is_review: bool = False


class SessionResponse(BaseModel):
    id: str
    student_id: str
    lesson_id: str
    started_at: datetime
    phase_reached: str
    completion_percentage: float
    is_review: bool

    class Config:
        from_attributes = True


class SessionEnd(BaseModel):
    session_id: str


class ConversationMessage(BaseModel):
    session_id: str
    message_text: str
    speaker: str = "student"


class StudentProfileResponse(BaseModel):
    diagnostic_completed: bool
    overall_proficiency: str
    subject_proficiencies: dict
    chapter_progress: dict
    learning_pace: str
    total_study_minutes: int
    streak_days: int

    class Config:
        from_attributes = True


class DiagnosticAnswer(BaseModel):
    exercise_id: str
    answer: str


class DiagnosticSubmit(BaseModel):
    answers: list[DiagnosticAnswer]
