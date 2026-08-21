from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


CourseStatus = Literal["not_started", "in_progress", "completed"]
AttemptOutcome = Literal["answered", "skipped_timeout", "skipped_manual", "interrupted"]


class CourseProgressUpdate(BaseModel):
    deck_id: str
    lesson_id: str
    activity_id: Optional[str] = None
    slide_id: Optional[str] = None
    audio_position_ms: int = Field(0, ge=0)
    slide_state: Dict[str, Any] = Field(default_factory=dict)
    completed_slide_ids: List[str] = Field(default_factory=list)
    status: CourseStatus = "in_progress"


class SlideAttemptCreate(BaseModel):
    deck_id: str
    lesson_id: str
    slide_id: str
    answer: Any = None
    outcome: AttemptOutcome = "answered"
    response_time_ms: Optional[int] = Field(None, ge=0)
    confidence: Optional[int] = Field(None, ge=1, le=5)


class SlideAttemptFeedback(BaseModel):
    is_correct: Optional[bool] = None
    feedback: str
    should_requeue: bool = False


class CourseIntentResolveRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=600)
