-- Admin Dashboard: Token Usage Tracking Table
-- Tracks all LLM API calls (DeepSeek, Mistral) with token counts and costs

CREATE TABLE IF NOT EXISTS token_usage (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES auth.users(id) ON DELETE SET NULL,
    student_email TEXT,
    provider TEXT NOT NULL,            -- 'deepseek', 'mistral_ocr', 'mistral_chat', 'gemini'
    model TEXT NOT NULL,               -- 'deepseek-chat', 'mistral-ocr-latest', etc.
    endpoint TEXT DEFAULT 'chat',      -- 'chat', 'chat_stream', 'ocr', 'vision', 'tts'
    prompt_tokens INTEGER DEFAULT 0,
    completion_tokens INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    cost_usd NUMERIC(10, 6) DEFAULT 0, -- cost in USD
    request_duration_ms INTEGER DEFAULT 0,
    session_type TEXT DEFAULT 'coaching', -- 'coaching', 'libre', 'exam', 'diagnostic', 'admin'
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Indexes for fast queries
CREATE INDEX IF NOT EXISTS idx_token_usage_student_id ON token_usage(student_id);
CREATE INDEX IF NOT EXISTS idx_token_usage_provider ON token_usage(provider);
CREATE INDEX IF NOT EXISTS idx_token_usage_created_at ON token_usage(created_at);
CREATE INDEX IF NOT EXISTS idx_token_usage_student_created ON token_usage(student_id, created_at);

-- RLS: disable for admin access via service role key
ALTER TABLE token_usage ENABLE ROW LEVEL SECURITY;

-- Allow service role full access
CREATE POLICY "Service role full access on token_usage"
    ON token_usage
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Admin users table (simple role flag)
-- Add is_admin column to students if not exists
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'students' AND column_name = 'is_admin'
    ) THEN
        ALTER TABLE students ADD COLUMN is_admin BOOLEAN DEFAULT false;
    END IF;
END $$;
