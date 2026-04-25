CREATE TABLE IF NOT EXISTS lesson_resources (
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

CREATE INDEX IF NOT EXISTS idx_lesson_resources_lesson_id ON lesson_resources(lesson_id);
CREATE INDEX IF NOT EXISTS idx_lesson_resources_type ON lesson_resources(resource_type);
CREATE INDEX IF NOT EXISTS idx_lesson_resources_phase ON lesson_resources(phase);
