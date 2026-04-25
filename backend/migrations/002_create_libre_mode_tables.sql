-- Migration: Create tables for Libre Mode
-- Date: 2026-03-28

-- Table: libre_conversations
-- Stores free-form Q&A conversations in Libre mode
CREATE TABLE IF NOT EXISTS libre_conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES students(id) ON DELETE CASCADE,
    title TEXT,
    subject_detected TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    ended_at TIMESTAMP WITH TIME ZONE,
    total_messages INTEGER DEFAULT 0,
    topics_covered JSONB DEFAULT '[]',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_libre_conversations_student ON libre_conversations(student_id);
CREATE INDEX idx_libre_conversations_started ON libre_conversations(started_at DESC);

-- Table: libre_messages
-- Individual messages in libre conversations
CREATE TABLE IF NOT EXISTS libre_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES libre_conversations(id) ON DELETE CASCADE,
    speaker TEXT NOT NULL CHECK (speaker IN ('student', 'ai')),
    message_text TEXT NOT NULL,
    response_type TEXT,
    media_shown JSONB DEFAULT '{}',
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_libre_messages_conversation ON libre_messages(conversation_id);
CREATE INDEX idx_libre_messages_timestamp ON libre_messages(timestamp);

-- Comments
COMMENT ON TABLE libre_conversations IS 'Free-form Q&A conversations in Libre mode';
COMMENT ON TABLE libre_messages IS 'Individual messages within libre conversations';
COMMENT ON COLUMN libre_conversations.subject_detected IS 'Auto-detected subject (math, physique, chimie, svt, mixed)';
COMMENT ON COLUMN libre_conversations.topics_covered IS 'Array of topics discussed: ["glycolyse", "mitochondrie"]';
COMMENT ON COLUMN libre_messages.response_type IS 'Type of AI response: text, schema, image, simulation, exercise, evaluation';
COMMENT ON COLUMN libre_messages.media_shown IS 'JSON with media details: {"type": "schema", "id": "svt_glycolyse"}';
