-- Migration: Create exam_attempts table for exam mode
-- Date: 2026-04-04

CREATE TABLE IF NOT EXISTS exam_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    exam_subject TEXT NOT NULL,
    exam_year INTEGER NOT NULL,
    exam_session TEXT NOT NULL CHECK (exam_session IN ('normale', 'rattrapage')),
    mode TEXT NOT NULL DEFAULT 'practice' CHECK (mode IN ('practice', 'real')),
    answers JSONB DEFAULT '{}',
    scores JSONB DEFAULT '{}',
    total_score NUMERIC(5,2),
    max_score NUMERIC(5,2) DEFAULT 20,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE,
    duration_seconds INTEGER
);

CREATE INDEX idx_exam_attempts_student ON exam_attempts(student_id);
CREATE INDEX idx_exam_attempts_subject ON exam_attempts(exam_subject);
CREATE INDEX idx_exam_attempts_started ON exam_attempts(started_at DESC);

COMMENT ON TABLE exam_attempts IS 'Student exam attempt history for practice and real exam modes';
