-- AI Tutor BAC - Supabase Database Initialization
-- Execute this script in Supabase SQL Editor
-- https://supabase.com/dashboard/project/yzvlmulpqnovduqhhtjf/editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create ENUM types
DO $$ BEGIN
    CREATE TYPE difficulty_level AS ENUM ('beginner', 'intermediate', 'advanced');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE question_type AS ENUM ('qcm', 'numeric', 'open', 'true_false');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE lesson_type AS ENUM ('theory', 'practice', 'lab', 'revision');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE teaching_mode AS ENUM ('Socratique', 'Directif', 'Collaboratif', 'Autonome');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create subjects table
CREATE TABLE IF NOT EXISTS subjects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name_fr VARCHAR(100) NOT NULL,
    name_ar VARCHAR(100) NOT NULL,
    description_fr TEXT,
    description_ar TEXT,
    icon VARCHAR(50),
    color VARCHAR(20),
    order_index INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create chapters table
CREATE TABLE IF NOT EXISTS chapters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    chapter_number INTEGER NOT NULL,
    title_fr VARCHAR(200) NOT NULL,
    title_ar VARCHAR(200) NOT NULL,
    description_fr TEXT,
    description_ar TEXT,
    difficulty_level difficulty_level DEFAULT 'intermediate',
    estimated_hours DECIMAL(4,1) DEFAULT 3.0,
    order_index INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create lessons table
CREATE TABLE IF NOT EXISTS lessons (
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

-- Create pedagogical_situations table
CREATE TABLE IF NOT EXISTS pedagogical_situations (
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

-- Create exercises table
CREATE TABLE IF NOT EXISTS exercises (
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

-- Create students table
CREATE TABLE IF NOT EXISTS students (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    username VARCHAR(100) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    school_level VARCHAR(100) DEFAULT '2eme BAC Sciences Physiques BIOF',
    preferred_language VARCHAR(10) DEFAULT 'fr',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    last_login TIMESTAMP WITH TIME ZONE
);

-- Create student_profiles table
CREATE TABLE IF NOT EXISTS student_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID UNIQUE NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    proficiency_level difficulty_level DEFAULT 'intermediate',
    learning_style teaching_mode DEFAULT 'Socratique',
    strengths JSONB DEFAULT '[]',
    weaknesses JSONB DEFAULT '[]',
    total_study_time_minutes INTEGER DEFAULT 0,
    sessions_completed INTEGER DEFAULT 0,
    exercises_completed INTEGER DEFAULT 0,
    average_score DECIMAL(5,2) DEFAULT 0.0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create learning_sessions table
CREATE TABLE IF NOT EXISTS learning_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    start_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    end_time TIMESTAMP WITH TIME ZONE,
    duration_minutes INTEGER,
    phases_completed JSONB DEFAULT '[]',
    final_phase VARCHAR(50),
    session_notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create conversation_logs table
CREATE TABLE IF NOT EXISTS conversation_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES learning_sessions(id) ON DELETE CASCADE,
    speaker VARCHAR(20) NOT NULL,
    message_text TEXT NOT NULL,
    phase VARCHAR(50),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create exercise_attempts table
CREATE TABLE IF NOT EXISTS exercise_attempts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id UUID NOT NULL REFERENCES learning_sessions(id) ON DELETE CASCADE,
    exercise_id UUID NOT NULL REFERENCES exercises(id) ON DELETE CASCADE,
    student_answer JSONB NOT NULL,
    is_correct BOOLEAN NOT NULL,
    attempts_count INTEGER DEFAULT 1,
    time_spent_seconds INTEGER,
    hint_level_used INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create spaced_repetition_queue table
CREATE TABLE IF NOT EXISTS spaced_repetition_queue (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    next_review_date DATE NOT NULL,
    repetition_number INTEGER DEFAULT 0,
    ease_factor DECIMAL(3,2) DEFAULT 2.5,
    interval_days INTEGER DEFAULT 1,
    last_reviewed TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create ai_prompts table
CREATE TABLE IF NOT EXISTS ai_prompts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prompt_type VARCHAR(50) NOT NULL,
    phase VARCHAR(50),
    template_text TEXT NOT NULL,
    variables JSONB DEFAULT '[]',
    language VARCHAR(10) DEFAULT 'fr',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_chapters_subject ON chapters(subject_id);
CREATE INDEX IF NOT EXISTS idx_lessons_chapter ON lessons(chapter_id);
CREATE INDEX IF NOT EXISTS idx_exercises_lesson ON exercises(lesson_id);
CREATE INDEX IF NOT EXISTS idx_sessions_student ON learning_sessions(student_id);
CREATE INDEX IF NOT EXISTS idx_sessions_lesson ON learning_sessions(lesson_id);
CREATE INDEX IF NOT EXISTS idx_conversation_session ON conversation_logs(session_id);
CREATE INDEX IF NOT EXISTS idx_attempts_session ON exercise_attempts(session_id);
CREATE INDEX IF NOT EXISTS idx_attempts_exercise ON exercise_attempts(exercise_id);
CREATE INDEX IF NOT EXISTS idx_spaced_rep_student ON spaced_repetition_queue(student_id);
CREATE INDEX IF NOT EXISTS idx_spaced_rep_next_review ON spaced_repetition_queue(next_review_date);
CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);
CREATE INDEX IF NOT EXISTS idx_students_username ON students(username);

-- Enable Row Level Security (RLS) for Supabase
ALTER TABLE students ENABLE ROW LEVEL SECURITY;
ALTER TABLE student_profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE learning_sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercise_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE spaced_repetition_queue ENABLE ROW LEVEL SECURITY;

-- Create RLS policies for students (users can only access their own data)
CREATE POLICY "Students can view own data" ON students
    FOR SELECT USING (auth.uid()::text = id::text);

CREATE POLICY "Students can update own data" ON students
    FOR UPDATE USING (auth.uid()::text = id::text);

CREATE POLICY "Student profiles viewable by owner" ON student_profiles
    FOR SELECT USING (auth.uid()::text = student_id::text);

CREATE POLICY "Student profiles updatable by owner" ON student_profiles
    FOR UPDATE USING (auth.uid()::text = student_id::text);

CREATE POLICY "Sessions viewable by owner" ON learning_sessions
    FOR SELECT USING (auth.uid()::text = student_id::text);

CREATE POLICY "Sessions insertable by owner" ON learning_sessions
    FOR INSERT WITH CHECK (auth.uid()::text = student_id::text);

-- Public read access for educational content
ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE chapters ENABLE ROW LEVEL SECURITY;
ALTER TABLE lessons ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE pedagogical_situations ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_prompts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public can view subjects" ON subjects FOR SELECT USING (true);
CREATE POLICY "Public can view chapters" ON chapters FOR SELECT USING (true);
CREATE POLICY "Public can view lessons" ON lessons FOR SELECT USING (true);
CREATE POLICY "Public can view exercises" ON exercises FOR SELECT USING (true);
CREATE POLICY "Public can view pedagogical situations" ON pedagogical_situations FOR SELECT USING (true);
CREATE POLICY "Public can view ai prompts" ON ai_prompts FOR SELECT USING (true);

-- Verification query
SELECT 
    schemaname,
    tablename
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY tablename;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database schema created successfully!';
    RAISE NOTICE 'Tables created: subjects, chapters, lessons, exercises, students, etc.';
    RAISE NOTICE 'Next step: Run the seed script to populate initial data';
END $$;
