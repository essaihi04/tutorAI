-- Ajouter les colonnes manquantes à student_profiles
-- À exécuter dans le SQL Editor de Supabase Dashboard

-- 1. Désactiver RLS
ALTER TABLE public.students DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_profiles DISABLE ROW LEVEL SECURITY;

-- 2. Rendre hashed_password optionnel
ALTER TABLE public.students 
ALTER COLUMN hashed_password DROP NOT NULL;

-- 3. Ajouter les colonnes manquantes à student_profiles
ALTER TABLE public.student_profiles 
ADD COLUMN IF NOT EXISTS diagnostic_completed BOOLEAN DEFAULT FALSE,
ADD COLUMN IF NOT EXISTS overall_proficiency VARCHAR(50) DEFAULT 'beginner',
ADD COLUMN IF NOT EXISTS learning_pace VARCHAR(50) DEFAULT 'medium',
ADD COLUMN IF NOT EXISTS preferred_teaching_mode VARCHAR(50) DEFAULT 'mixed',
ADD COLUMN IF NOT EXISTS strengths TEXT[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS weaknesses TEXT[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS learning_goals TEXT[] DEFAULT '{}',
ADD COLUMN IF NOT EXISTS study_schedule JSONB DEFAULT '{}',
ADD COLUMN IF NOT EXISTS created_at TIMESTAMPTZ DEFAULT NOW(),
ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- 4. Vérifier la structure
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
AND table_name = 'student_profiles'
ORDER BY ordinal_position;
