-- Migration: Add session_type column to study_plan_sessions
-- Date: 2026-04-03
-- Purpose: Track whether a session is cours/revision/lacunes/examen_blanc

ALTER TABLE study_plan_sessions
ADD COLUMN IF NOT EXISTS session_type TEXT NOT NULL DEFAULT 'cours'
CHECK (session_type IN ('cours', 'revision', 'lacunes', 'examen_blanc'));

-- Comment for documentation
COMMENT ON COLUMN study_plan_sessions.session_type IS 'Type of session: cours (learning), revision, lacunes (gap filling), examen_blanc (mock exam)';
