-- Create storage bucket for pedagogical resources
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'pedagogical-resources',
    'pedagogical-resources',
    true,
    52428800, -- 50MB limit
    ARRAY['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml', 'image/webp', 'video/mp4', 'video/webm', 'video/ogg']
)
ON CONFLICT (id) DO NOTHING;

-- Policy: Allow authenticated users to upload files
CREATE POLICY "Authenticated users can upload resources"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'pedagogical-resources');

-- Policy: Allow public read access to all files
CREATE POLICY "Public read access for resources"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'pedagogical-resources');

-- Policy: Allow authenticated users to update their uploads
CREATE POLICY "Authenticated users can update resources"
ON storage.objects FOR UPDATE
TO authenticated
USING (bucket_id = 'pedagogical-resources');

-- Policy: Allow authenticated users to delete files
CREATE POLICY "Authenticated users can delete resources"
ON storage.objects FOR DELETE
TO authenticated
USING (bucket_id = 'pedagogical-resources');
