-- Migration: Add media_resources column to lessons table
-- Date: 2026-03-06
-- Description: Adds JSONB column to store media resources (images, simulations, videos) for each lesson

-- Add media_resources column if it doesn't exist
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'lessons' 
        AND column_name = 'media_resources'
    ) THEN
        ALTER TABLE lessons 
        ADD COLUMN media_resources JSONB DEFAULT '[]';
        
        RAISE NOTICE 'Column media_resources added to lessons table';
    ELSE
        RAISE NOTICE 'Column media_resources already exists';
    END IF;
END $$;

-- Update existing lesson with media resources (example for phys_ch1_l1)
-- This will be done by the seed script, but here's an example:
/*
UPDATE lessons
SET media_resources = '[
    {
        "type": "image",
        "url": "/media/images/physics/ch1_ondes_mecaniques/onde_transversale.png",
        "caption": "Onde transversale sur une corde",
        "trigger": "regarde ce schéma",
        "phase": "explanation"
    }
]'::jsonb
WHERE title_fr = 'Introduction aux ondes mecaniques progressives';
*/

-- Verify the migration
SELECT 
    column_name, 
    data_type, 
    column_default
FROM information_schema.columns
WHERE table_name = 'lessons' 
AND column_name = 'media_resources';
