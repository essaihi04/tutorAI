-- AI Tutor BAC - Database Schema
-- PostgreSQL 15+

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- ENUM TYPES
-- ============================================

CREATE TYPE difficulty_level AS ENUM ('beginner', 'intermediate', 'advanced');
CREATE TYPE lesson_type AS ENUM ('theory', 'exercise', 'simulation', 'evaluation');
CREATE TYPE question_type AS ENUM ('qcm', 'numeric', 'open_text');
CREATE TYPE teaching_mode AS ENUM ('socratic', 'direct', 'mixed');
CREATE TYPE learning_pace AS ENUM ('slow', 'medium', 'fast');
CREATE TYPE language_pref AS ENUM ('fr', 'ar', 'mixed');
CREATE TYPE session_phase AS ENUM ('activation', 'exploration', 'explanation', 'application', 'consolidation');
CREATE TYPE speaker_type AS ENUM ('student', 'ai');
CREATE TYPE sentiment_type AS ENUM ('positive', 'neutral', 'negative', 'confused');
CREATE TYPE prompt_category AS ENUM ('system_base', 'phase_activation', 'phase_exploration', 'phase_explanation', 'phase_application', 'phase_consolidation', 'correction', 'encouragement', 'diagnostic');

-- ============================================
-- CORE CONTENT TABLES
-- ============================================

CREATE TABLE subjects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name_fr VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100) NOT NULL,
    description_fr TEXT,
    description_ar TEXT,
    icon VARCHAR(50),
    color VARCHAR(7),
    order_index INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    chapter_number INTEGER NOT NULL,
    title_fr VARCHAR(200) NOT NULL,
    title_ar VARCHAR(200) NOT NULL,
    description_fr TEXT,
    description_ar TEXT,
    difficulty_level difficulty_level DEFAULT 'intermediate',
    prerequisites JSONB DEFAULT '[]',
    estimated_hours DECIMAL(4,1) DEFAULT 2.0,
    order_index INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE lessons (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    title_fr VARCHAR(200) NOT NULL,
    title_ar VARCHAR(200) NOT NULL,
    lesson_type lesson_type NOT NULL DEFAULT 'theory',
    content JSONB NOT NULL DEFAULT '{}',
    learning_objectives JSONB DEFAULT '[]',
    duration_minutes INTEGER DEFAULT 50,
    order_index INTEGER NOT NULL DEFAULT 0,
    media_resources JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE pedagogical_situations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    scenario_title_fr VARCHAR(200) NOT NULL,
    scenario_title_ar VARCHAR(200) NOT NULL,
    scenario_description JSONB NOT NULL,
    context_prompt TEXT NOT NULL,
    expected_student_path JSONB DEFAULT '[]',
    difficulty_tier difficulty_level DEFAULT 'intermediate',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    question_text_fr TEXT NOT NULL,
    question_text_ar TEXT NOT NULL,
    question_type question_type NOT NULL DEFAULT 'qcm',
    difficulty_tier difficulty_level NOT NULL DEFAULT 'beginner',
    options JSONB DEFAULT '[]',
    correct_answer JSONB NOT NULL,
    explanation_fr TEXT NOT NULL,
    explanation_ar TEXT NOT NULL,
    hints JSONB DEFAULT '[]',
    estimated_time_seconds INTEGER DEFAULT 120,
    order_index INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

 CREATE TABLE lesson_resources (
     id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
     lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
     section_title VARCHAR(200) NOT NULL,
     resource_type VARCHAR(30) NOT NULL,
     title VARCHAR(200) NOT NULL,
     description TEXT,
     file_path TEXT,
     external_url TEXT,
     trigger_text VARCHAR(200),
     phase VARCHAR(30),
     difficulty_tier difficulty_level DEFAULT 'intermediate',
     concepts JSONB DEFAULT '[]',
     metadata JSONB DEFAULT '{}',
     order_index INTEGER NOT NULL DEFAULT 0,
     created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
 );

-- ============================================
-- USER TABLES
-- ============================================

CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    preferred_language language_pref DEFAULT 'fr',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_active_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE student_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID UNIQUE NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    diagnostic_completed BOOLEAN DEFAULT FALSE,
    overall_proficiency difficulty_level DEFAULT 'beginner',
    subject_proficiencies JSONB DEFAULT '{}',
    chapter_progress JSONB DEFAULT '{}',
    learning_pace learning_pace DEFAULT 'medium',
    preferred_teaching_mode teaching_mode DEFAULT 'mixed',
    total_study_minutes INTEGER DEFAULT 0,
    streak_days INTEGER DEFAULT 0,
    last_streak_date DATE,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- SESSION & TRACKING TABLES
-- ============================================

CREATE TABLE learning_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER DEFAULT 0,
    phase_reached session_phase DEFAULT 'activation',
    completion_percentage DECIMAL(5,2) DEFAULT 0.0,
    is_review BOOLEAN DEFAULT FALSE
);

CREATE TABLE conversation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES learning_sessions(id) ON DELETE CASCADE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    speaker speaker_type NOT NULL,
    message_text TEXT NOT NULL,
    intent_classification VARCHAR(50),
    sentiment sentiment_type DEFAULT 'neutral',
    confidence_score DECIMAL(3,2)
);

CREATE TABLE exercise_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES learning_sessions(id) ON DELETE CASCADE,
    exercise_id UUID NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    student_answer JSONB NOT NULL,
    is_correct BOOLEAN NOT NULL,
    attempt_number INTEGER DEFAULT 1,
    time_taken_seconds INTEGER,
    hints_used INTEGER DEFAULT 0,
    feedback_given TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE spaced_repetition_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    next_review_date DATE NOT NULL,
    repetition_number INTEGER DEFAULT 0,
    ease_factor DECIMAL(4,2) DEFAULT 2.50,
    interval_days INTEGER DEFAULT 1,
    last_review_quality INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(student_id, lesson_id)
);

-- ============================================
-- AI PROMPT TEMPLATES
-- ============================================

CREATE TABLE ai_prompts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prompt_category prompt_category NOT NULL,
    name VARCHAR(100) NOT NULL UNIQUE,
    template_text TEXT NOT NULL,
    variables JSONB DEFAULT '[]',
    language language_pref DEFAULT 'fr',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- INDEXES
-- ============================================

CREATE INDEX idx_chapters_subject ON chapters(subject_id);
CREATE INDEX idx_lessons_chapter ON lessons(chapter_id);
CREATE INDEX idx_exercises_lesson ON exercises(lesson_id);
CREATE INDEX idx_pedagogical_situations_lesson ON pedagogical_situations(lesson_id);
CREATE INDEX idx_student_profiles_student ON student_profiles(student_id);
CREATE INDEX idx_learning_sessions_student ON learning_sessions(student_id);
CREATE INDEX idx_learning_sessions_lesson ON learning_sessions(lesson_id);
CREATE INDEX idx_conversation_logs_session ON conversation_logs(session_id);
CREATE INDEX idx_exercise_attempts_session ON exercise_attempts(session_id);
CREATE INDEX idx_exercise_attempts_exercise ON exercise_attempts(exercise_id);
CREATE INDEX idx_spaced_rep_student ON spaced_repetition_queue(student_id);
CREATE INDEX idx_spaced_rep_next_review ON spaced_repetition_queue(next_review_date);
CREATE INDEX idx_students_email ON students(email);
