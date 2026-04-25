import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Text, Integer, Boolean, DateTime, Date,
    ForeignKey, Numeric, Enum as SAEnum, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name_fr = Column(String(100), nullable=False)
    name_ar = Column(String(100), nullable=False)
    description_fr = Column(Text)
    description_ar = Column(Text)
    icon = Column(String(50))
    color = Column(String(7))
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    chapters = relationship("Chapter", back_populates="subject", cascade="all, delete-orphan")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    subject_id = Column(UUID(as_uuid=True), ForeignKey("subjects.id", ondelete="CASCADE"), nullable=False)
    chapter_number = Column(Integer, nullable=False)
    title_fr = Column(String(200), nullable=False)
    title_ar = Column(String(200), nullable=False)
    description_fr = Column(Text)
    description_ar = Column(Text)
    difficulty_level = Column(String(20), default="intermediate")
    prerequisites = Column(JSONB, default=[])
    estimated_hours = Column(Numeric(4, 1), default=2.0)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    subject = relationship("Subject", back_populates="chapters")
    lessons = relationship("Lesson", back_populates="chapter", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    chapter_id = Column(UUID(as_uuid=True), ForeignKey("chapters.id", ondelete="CASCADE"), nullable=False)
    title_fr = Column(String(200), nullable=False)
    title_ar = Column(String(200), nullable=False)
    lesson_type = Column(String(20), default="theory")
    content = Column(JSONB, default={})
    learning_objectives = Column(JSONB, default=[])
    duration_minutes = Column(Integer, default=50)
    order_index = Column(Integer, default=0)
    media_resources = Column(JSONB, default=[])
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    chapter = relationship("Chapter", back_populates="lessons")
    exercises = relationship("Exercise", back_populates="lesson", cascade="all, delete-orphan")
    pedagogical_situations = relationship("PedagogicalSituation", back_populates="lesson", cascade="all, delete-orphan")


class PedagogicalSituation(Base):
    __tablename__ = "pedagogical_situations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    scenario_title_fr = Column(String(200), nullable=False)
    scenario_title_ar = Column(String(200), nullable=False)
    scenario_description = Column(JSONB, nullable=False)
    context_prompt = Column(Text, nullable=False)
    expected_student_path = Column(JSONB, default=[])
    difficulty_tier = Column(String(20), default="intermediate")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    lesson = relationship("Lesson", back_populates="pedagogical_situations")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    question_text_fr = Column(Text, nullable=False)
    question_text_ar = Column(Text, nullable=False)
    question_type = Column(String(20), default="qcm")
    difficulty_tier = Column(String(20), default="beginner")
    options = Column(JSONB, default=[])
    correct_answer = Column(JSONB, nullable=False)
    explanation_fr = Column(Text, nullable=False)
    explanation_ar = Column(Text, nullable=False)
    hints = Column(JSONB, default=[])
    estimated_time_seconds = Column(Integer, default=120)
    order_index = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    lesson = relationship("Lesson", back_populates="exercises")
    attempts = relationship("ExerciseAttempt", back_populates="exercise", cascade="all, delete-orphan")
