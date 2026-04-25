-- Migration: Create tables for Coaching Mode
-- Date: 2026-03-28

-- Table: study_plans
-- Stores personalized study plans for students
CREATE TABLE IF NOT EXISTS study_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    exam_date DATE NOT NULL DEFAULT '2026-06-04',
    diagnostic_scores JSONB DEFAULT '{}',
    total_hours_available INTEGER,
    status TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active', 'completed', 'archived')),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index for faster queries
CREATE INDEX idx_study_plans_student ON study_plans(student_id);
CREATE INDEX idx_study_plans_status ON study_plans(status);

-- Table: study_plan_sessions
-- Individual study sessions within a plan
CREATE TABLE IF NOT EXISTS study_plan_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    plan_id UUID NOT NULL REFERENCES study_plans(id) ON DELETE CASCADE,
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    chapter_id UUID NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    scheduled_date DATE NOT NULL,
    scheduled_time TEXT,
    duration_minutes INTEGER NOT NULL DEFAULT 90,
    priority TEXT NOT NULL DEFAULT 'medium' CHECK (priority IN ('high', 'medium', 'low')),
    status TEXT NOT NULL DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'skipped', 'rescheduled')),
    completed_at TIMESTAMP WITH TIME ZONE,
    notes TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_plan_sessions_plan ON study_plan_sessions(plan_id);
CREATE INDEX idx_plan_sessions_date ON study_plan_sessions(scheduled_date);
CREATE INDEX idx_plan_sessions_status ON study_plan_sessions(status);
CREATE INDEX idx_plan_sessions_subject ON study_plan_sessions(subject_id);

-- Table: diagnostic_results
-- Stores diagnostic and formative evaluation results
CREATE TABLE IF NOT EXISTS diagnostic_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    subject_id UUID NOT NULL REFERENCES subjects(id) ON DELETE CASCADE,
    chapter_id UUID REFERENCES chapters(id) ON DELETE SET NULL,
    evaluation_type TEXT NOT NULL CHECK (evaluation_type IN ('diagnostic', 'formative')),
    score NUMERIC(5, 2) NOT NULL,
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    weak_topics JSONB DEFAULT '[]',
    strong_topics JSONB DEFAULT '[]',
    questions_data JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_diagnostic_student ON diagnostic_results(student_id);
CREATE INDEX idx_diagnostic_subject ON diagnostic_results(subject_id);
CREATE INDEX idx_diagnostic_type ON diagnostic_results(evaluation_type);
CREATE INDEX idx_diagnostic_created ON diagnostic_results(created_at DESC);

-- Alter student_profiles table
-- Add coaching mode fields
ALTER TABLE student_profiles
ADD COLUMN IF NOT EXISTS coaching_mode_active BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS current_plan_id UUID REFERENCES study_plans(id) ON DELETE SET NULL,
ADD COLUMN IF NOT EXISTS overall_progress NUMERIC(5, 2) DEFAULT 0,
ADD COLUMN IF NOT EXISTS subject_progress JSONB DEFAULT '{}';

-- Create index on current_plan_id
CREATE INDEX IF NOT EXISTS idx_student_profiles_plan ON student_profiles(current_plan_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger for study_plans
DROP TRIGGER IF EXISTS update_study_plans_updated_at ON study_plans;
CREATE TRIGGER update_study_plans_updated_at
    BEFORE UPDATE ON study_plans
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Comments for documentation
COMMENT ON TABLE study_plans IS 'Personalized study plans generated from diagnostic results';
COMMENT ON TABLE study_plan_sessions IS 'Individual study sessions scheduled within a plan';
COMMENT ON TABLE diagnostic_results IS 'Results from diagnostic and formative evaluations';
COMMENT ON COLUMN study_plans.diagnostic_scores IS 'JSON object with scores per subject: {"math": 45, "physique": 60}';
COMMENT ON COLUMN study_plans.total_hours_available IS 'Total study hours available until exam date';
COMMENT ON COLUMN study_plan_sessions.scheduled_time IS 'Time range like "16:00-17:30"';
COMMENT ON COLUMN diagnostic_results.weak_topics IS 'Array of topic names where student struggled';
COMMENT ON COLUMN diagnostic_results.strong_topics IS 'Array of topic names where student excelled';
