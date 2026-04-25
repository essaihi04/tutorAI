import uuid
from datetime import datetime
from sqlalchemy import Column, String, Boolean, DateTime, Integer, Date, Numeric, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    preferred_language = Column(String(10), default="fr")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    last_active_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    profile = relationship("StudentProfile", back_populates="student", uselist=False, cascade="all, delete-orphan")
    sessions = relationship("LearningSession", back_populates="student", cascade="all, delete-orphan")
    repetition_queue = relationship("SpacedRepetitionQueue", back_populates="student", cascade="all, delete-orphan")


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    student_id = Column(UUID(as_uuid=True), ForeignKey("students.id", ondelete="CASCADE"), unique=True, nullable=False)
    diagnostic_completed = Column(Boolean, default=False)
    overall_proficiency = Column(String(20), default="beginner")
    subject_proficiencies = Column(JSONB, default={})
    chapter_progress = Column(JSONB, default={})
    learning_pace = Column(String(10), default="medium")
    preferred_teaching_mode = Column(String(10), default="mixed")
    total_study_minutes = Column(Integer, default=0)
    streak_days = Column(Integer, default=0)
    last_streak_date = Column(Date)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)

    student = relationship("Student", back_populates="profile")
