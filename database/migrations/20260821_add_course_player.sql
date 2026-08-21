-- Lecteur de cours versionné : activités, diapositives, audio publié et progression.
-- Les fichiers audio sont conservés dans un stockage objet ; la base garde leur
-- version, leur empreinte et leur statut de vérification.

BEGIN;

CREATE TABLE IF NOT EXISTS course_decks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lesson_id UUID NOT NULL REFERENCES lessons(id) ON DELETE CASCADE,
    version INTEGER NOT NULL DEFAULT 1,
    title VARCHAR(240) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'verified', 'published', 'archived')),
    language VARCHAR(12) NOT NULL DEFAULT 'fr',
    estimated_minutes INTEGER NOT NULL DEFAULT 50,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    published_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (lesson_id, version)
);

CREATE TABLE IF NOT EXISTS course_activities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    deck_id UUID NOT NULL REFERENCES course_decks(id) ON DELETE CASCADE,
    stable_id VARCHAR(120) NOT NULL,
    title VARCHAR(240) NOT NULL,
    phase VARCHAR(30) NOT NULL DEFAULT 'explanation',
    duration_minutes INTEGER NOT NULL DEFAULT 15,
    objective_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    order_index INTEGER NOT NULL DEFAULT 0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (deck_id, stable_id),
    UNIQUE (deck_id, order_index)
);

CREATE TABLE IF NOT EXISTS course_slides (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    activity_id UUID NOT NULL REFERENCES course_activities(id) ON DELETE CASCADE,
    stable_id VARCHAR(140) NOT NULL,
    slide_type VARCHAR(30) NOT NULL DEFAULT 'concept'
        CHECK (slide_type IN (
            'diagnostic', 'situation', 'concept', 'image', 'schema',
            'simulation', 'exercise', 'synthesis', 'evaluation'
        )),
    title VARCHAR(240) NOT NULL,
    screen_content JSONB NOT NULL DEFAULT '{}'::jsonb,
    visual JSONB NOT NULL DEFAULT '{}'::jsonb,
    speech_text JSONB NOT NULL DEFAULT '{}'::jsonb,
    question JSONB NOT NULL DEFAULT '{}'::jsonb,
    timing JSONB NOT NULL DEFAULT '{}'::jsonb,
    order_index INTEGER NOT NULL DEFAULT 0,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (activity_id, stable_id),
    UNIQUE (activity_id, order_index)
);

CREATE TABLE IF NOT EXISTS course_slide_audio (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slide_id UUID NOT NULL REFERENCES course_slides(id) ON DELETE CASCADE,
    language VARCHAR(12) NOT NULL,
    version INTEGER NOT NULL DEFAULT 1,
    speech_hash VARCHAR(64) NOT NULL,
    file_path TEXT NOT NULL,
    mime_type VARCHAR(80) NOT NULL DEFAULT 'audio/wav',
    duration_ms INTEGER,
    voice VARCHAR(80),
    provider VARCHAR(80),
    checksum VARCHAR(128),
    status VARCHAR(20) NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft', 'generated', 'verified', 'published', 'rejected', 'stale')),
    verified_by UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    verified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (slide_id, language, version)
);

CREATE TABLE IF NOT EXISTS course_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    deck_id UUID NOT NULL REFERENCES course_decks(id) ON DELETE CASCADE,
    current_activity_id UUID REFERENCES course_activities(id) ON DELETE SET NULL,
    current_slide_id UUID REFERENCES course_slides(id) ON DELETE SET NULL,
    audio_position_ms INTEGER NOT NULL DEFAULT 0,
    slide_state JSONB NOT NULL DEFAULT '{}'::jsonb,
    completed_slide_ids JSONB NOT NULL DEFAULT '[]'::jsonb,
    status VARCHAR(20) NOT NULL DEFAULT 'in_progress'
        CHECK (status IN ('not_started', 'in_progress', 'completed')),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (student_id, deck_id)
);

CREATE TABLE IF NOT EXISTS course_slide_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    slide_id UUID NOT NULL REFERENCES course_slides(id) ON DELETE CASCADE,
    answer JSONB NOT NULL DEFAULT '{}'::jsonb,
    is_correct BOOLEAN,
    outcome VARCHAR(30) NOT NULL DEFAULT 'answered'
        CHECK (outcome IN ('answered', 'skipped_timeout', 'skipped_manual', 'interrupted')),
    response_time_ms INTEGER,
    confidence INTEGER CHECK (confidence IS NULL OR confidence BETWEEN 1 AND 5),
    feedback JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_course_decks_lesson_status
    ON course_decks (lesson_id, status, version DESC);
CREATE INDEX IF NOT EXISTS idx_course_activities_deck_order
    ON course_activities (deck_id, order_index);
CREATE INDEX IF NOT EXISTS idx_course_slides_activity_order
    ON course_slides (activity_id, order_index);
CREATE INDEX IF NOT EXISTS idx_course_slide_audio_published
    ON course_slide_audio (slide_id, language, status);
CREATE INDEX IF NOT EXISTS idx_course_progress_student
    ON course_progress (student_id, updated_at DESC);
CREATE INDEX IF NOT EXISTS idx_course_attempts_student_slide
    ON course_slide_attempts (student_id, slide_id, created_at DESC);

ALTER TABLE course_decks ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_slides ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_slide_audio ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE course_slide_attempts ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Students read published course decks" ON course_decks
    FOR SELECT TO authenticated USING (status = 'published');
CREATE POLICY "Students read published course activities" ON course_activities
    FOR SELECT TO authenticated USING (
        EXISTS (SELECT 1 FROM course_decks d WHERE d.id = deck_id AND d.status = 'published')
    );
CREATE POLICY "Students read published course slides" ON course_slides
    FOR SELECT TO authenticated USING (
        EXISTS (
            SELECT 1 FROM course_activities a
            JOIN course_decks d ON d.id = a.deck_id
            WHERE a.id = activity_id AND d.status = 'published'
        )
    );
CREATE POLICY "Students read published slide audio" ON course_slide_audio
    FOR SELECT TO authenticated USING (status = 'published');

CREATE POLICY "Students read own course progress" ON course_progress
    FOR SELECT TO authenticated USING (auth.uid() = student_id);
CREATE POLICY "Students insert own course progress" ON course_progress
    FOR INSERT TO authenticated WITH CHECK (auth.uid() = student_id);
CREATE POLICY "Students update own course progress" ON course_progress
    FOR UPDATE TO authenticated USING (auth.uid() = student_id);

CREATE POLICY "Students read own slide attempts" ON course_slide_attempts
    FOR SELECT TO authenticated USING (auth.uid() = student_id);
CREATE POLICY "Students insert own slide attempts" ON course_slide_attempts
    FOR INSERT TO authenticated WITH CHECK (auth.uid() = student_id);

NOTIFY pgrst, 'reload schema';

COMMIT;
