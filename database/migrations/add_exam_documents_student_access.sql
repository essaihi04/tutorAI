-- Allow students to read exam_documents (extracted exams)
-- This enables students to access exams transferred from the admin extraction tool

-- Drop existing restrictive policy if exists
DROP POLICY IF EXISTS "Service role full access on docs" ON exam_documents;

-- Allow authenticated users (students) to read all exam documents
CREATE POLICY "Students can read exam documents" ON exam_documents
    FOR SELECT
    USING (true);

-- Allow service role (backend) full access for insert/update/delete
CREATE POLICY "Service role can manage exam documents" ON exam_documents
    FOR ALL
    USING (true)
    WITH CHECK (true);

-- Also ensure exam_extraction_pages allows reading images for display
DROP POLICY IF EXISTS "Service role full access on pages" ON exam_extraction_pages;

CREATE POLICY "Anyone can read extraction pages" ON exam_extraction_pages
    FOR SELECT
    USING (true);

CREATE POLICY "Service role can manage extraction pages" ON exam_extraction_pages
    FOR ALL
    USING (true)
    WITH CHECK (true);
