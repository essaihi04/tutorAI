import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, Numeric, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base


class LearningSession(Base):
    __tablename__ = "learning_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    started_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    ended_at = Column(DateTime(timezone=True))
    duration_seconds = Column(Integer, default=0)
    phase_reached = Column(String(20), default="activation")
    completion_percentage = Column(Numeric(5, 2), default=0.0)
    is_review = Column(Boolean, default=False)

    student = relationship("Student", back_populates="sessions")
    lesson = relationship("Lesson")
    conversations = relationship("ConversationLog", back_populates="session", cascade="all, delete-orphan")
    exercise_attempts = relationship("ExerciseAttempt", back_populates="session", cascade="all, delete-orphan")


class ConversationLog(Base):
    __tablename__ = "conversation_logs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("learning_sessions.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime(timezone=True), default=datetime.utcnow)
    speaker = Column(String(10), nullable=False)
    message_text = Column(Text, nullable=False)
    intent_classification = Column(String(50))
    sentiment = Column(String(20), default="neutral")
    confidence_score = Column(Numeric(3, 2))

    session = relationship("LearningSession", back_populates="conversations")


class ExerciseAttempt(Base):
    __tablename__ = "exercise_attempts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(as_uuid=True), ForeignKey("learning_sessions.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercises.id", ondelete="CASCADE"), nullable=False)
    student_answer = Column(JSONB, nullable=False)
    is_correct = Column(Boolean, nullable=False)
    attempt_number = Column(Integer, default=1)
    time_taken_seconds = Column(Integer)
    hints_used = Column(Integer, default=0)
    feedback_given = Column(Text)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    session = relationship("LearningSession", back_populates="exercise_attempts")
    exercise = relationship("Exercise", back_populates="attempts")


class SpacedRepetitionQueue(Base):
    __tablename__ = "spaced_repetition_queue"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    lesson_id = Column(UUID(as_uuid=True), ForeignKey("lessons.id", ondelete="CASCADE"), nullable=False)
    next_review_date = Column(Date, nullable=False)
    repetition_number = Column(Integer, default=0)
    ease_factor = Column(Numeric(4, 2), default=2.50)
    interval_days = Column(Integer, default=1)
    last_review_quality = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student", back_populates="repetition_queue")
    lesson = relationship("Lesson")
