-- Migration: Add exam_source_id column to study_plan_sessions
-- Date: 2026-04-20
-- Purpose: Attach a real BAC national exam to each session of type 'examen_blanc'
--
-- The value is a stable id matching backend/data/exams/<subject>/<year>-<session>/
-- e.g. 'physique_2024_normale', 'svt_2025_rattrapage', 'mathematiques_2024_normale'.
-- Only set for session_type = 'examen_blanc'; null otherwise.

ALTER TABLE study_plan_sessions
    ADD COLUMN IF NOT EXISTS exam_source_id TEXT;

CREATE INDEX IF NOT EXISTS idx_plan_sessions_exam_source
    ON study_plan_sessions(exam_source_id)
    WHERE exam_source_id IS NOT NULL;

COMMENT ON COLUMN study_plan_sessions.exam_source_id IS
    'Stable id of the real BAC exam attached to this session '
    '(only populated when session_type = ''examen_blanc''). '
    'Matches the folder name under backend/data/exams/<subject>/<year>-<session>/.';
