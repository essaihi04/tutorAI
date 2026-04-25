-- Add extracted_images column to store figure/document images from Mistral OCR
ALTER TABLE exam_extraction_pages
ADD COLUMN IF NOT EXISTS extracted_images JSONB DEFAULT '[]';
