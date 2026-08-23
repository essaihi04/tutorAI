"""Schemas used by the versioned course editor in the admin dashboard."""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


CourseSlideType = Literal[
    "diagnostic",
    "situation",
    "concept",
    "image",
    "schema",
    "simulation",
    "exercise",
    "synthesis",
    "evaluation",
]


class AdminCourseSlide(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: Optional[str] = None
    stable_id: str = Field(..., min_length=2, max_length=140)
    slide_type: CourseSlideType = "concept"
    title: str = Field(..., min_length=1, max_length=240)
    screen_content: Dict[str, Any] = Field(default_factory=dict)
    visual: Dict[str, Any] = Field(default_factory=dict)
    speech_text: Dict[str, str] = Field(default_factory=dict)
    question: Dict[str, Any] = Field(default_factory=dict)
    timing: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AdminCourseActivity(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: Optional[str] = None
    stable_id: str = Field(..., min_length=2, max_length=120)
    title: str = Field(..., min_length=1, max_length=240)
    phase: str = Field("explanation", min_length=1, max_length=30)
    duration_minutes: int = Field(15, ge=1, le=180)
    objective_ids: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    slides: List[AdminCourseSlide] = Field(default_factory=list)


class AdminCourseSave(BaseModel):
    model_config = ConfigDict(extra="forbid")

    stable_id: str = Field(..., min_length=2, max_length=120)
    title: str = Field(..., min_length=1, max_length=240)
    language: str = Field("fr", min_length=2, max_length=12)
    estimated_minutes: int = Field(50, ge=1, le=3000)
    catalog: Dict[str, Any] = Field(default_factory=dict)
    lesson_match: List[str] = Field(default_factory=list)
    intent_aliases: List[str] = Field(default_factory=list)
    activities: List[AdminCourseActivity] = Field(default_factory=list)


class AdminCourseCreate(BaseModel):
    lesson_id: str = Field(..., min_length=1)
    stable_id: str = Field(..., min_length=2, max_length=120)
    title: str = Field(..., min_length=1, max_length=240)
    language: str = Field("fr", min_length=2, max_length=12)
    estimated_minutes: int = Field(50, ge=1, le=3000)


class AdminCourseDuplicate(BaseModel):
    lesson_id: Optional[str] = None


class AdminCourseAudioStatus(BaseModel):
    status: Literal["draft", "generated", "verified", "published", "rejected", "stale"]
