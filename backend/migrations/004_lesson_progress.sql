-- Migration: Lesson Progress Tracking for Coaching Mode
-- Tracks student progress within each lesson to enable session resumption

CREATE TABLE IF NOT EXISTS lesson_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    
    -- Progress tracking
    objectives_total INTEGER NOT NULL DEFAULT 1,
    objectives_completed INTEGER[] DEFAULT '{}',
    current_objective_index INTEGER DEFAULT 0,
    
    -- Memory of what was covered
    topics_covered TEXT[] DEFAULT '{}',
    key_points_learned TEXT[] DEFAULT '{}',
    last_ai_summary TEXT DEFAULT '',
    
    -- Status
    status TEXT DEFAULT 'in_progress' CHECK (status IN ('not_started', 'in_progress', 'completed')),
    
    -- Timestamps
    started_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Unique constraint: one progress record per student per lesson
    UNIQUE(student_id, lesson_id)
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_lesson_progress_student ON lesson_progress(student_id);
CREATE INDEX IF NOT EXISTS idx_lesson_progress_lesson ON lesson_progress(lesson_id);
CREATE INDEX IF NOT EXISTS idx_lesson_progress_status ON lesson_progress(status);

-- RLS policies
ALTER TABLE lesson_progress ENABLE ROW LEVEL SECURITY;

-- Students can only see their own progress
CREATE POLICY "Students can view own progress" ON lesson_progress
    FOR SELECT USING (auth.uid() = student_id);

CREATE POLICY "Students can insert own progress" ON lesson_progress
    FOR INSERT WITH CHECK (auth.uid() = student_id);

CREATE POLICY "Students can update own progress" ON lesson_progress
    FOR UPDATE USING (auth.uid() = student_id);

-- Notify PostgREST to reload schema
NOTIFY pgrst, 'reload schema';
