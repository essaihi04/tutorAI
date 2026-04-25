-- Student Answer History & Proficiency Tracking
-- Records every student answer for proficiency analysis

CREATE TABLE IF NOT EXISTS student_answer_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    subject VARCHAR(100) NOT NULL,
    topic VARCHAR(200) NOT NULL DEFAULT '',
    chapter VARCHAR(200) NOT NULL DEFAULT '',
    question_content TEXT NOT NULL DEFAULT '',
    student_answer TEXT NOT NULL DEFAULT '',
    correct_answer TEXT NOT NULL DEFAULT '',
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    score DECIMAL(5,2) NOT NULL DEFAULT 0,
    max_score DECIMAL(5,2) NOT NULL DEFAULT 1,
    question_type VARCHAR(50) NOT NULL DEFAULT 'open',
    source VARCHAR(50) NOT NULL DEFAULT 'exam',
    exam_id VARCHAR(100) DEFAULT '',
    exercise_name VARCHAR(200) DEFAULT '',
    part_name VARCHAR(200) DEFAULT '',
    year VARCHAR(10) DEFAULT '',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for fast querying
CREATE INDEX IF NOT EXISTS idx_answer_history_student ON student_answer_history(student_id);
CREATE INDEX IF NOT EXISTS idx_answer_history_subject ON student_answer_history(student_id, subject);
CREATE INDEX IF NOT EXISTS idx_answer_history_topic ON student_answer_history(student_id, subject, topic);
CREATE INDEX IF NOT EXISTS idx_answer_history_created ON student_answer_history(student_id, created_at DESC);

-- RLS
ALTER TABLE student_answer_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Students can view own answer history" ON student_answer_history
    FOR SELECT USING (auth.uid()::text = student_id::text);

CREATE POLICY "Service role can insert answer history" ON student_answer_history
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Service role can update answer history" ON student_answer_history
    FOR UPDATE USING (true);
