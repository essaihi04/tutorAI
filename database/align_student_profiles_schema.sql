-- Aligner la structure de student_profiles avec le schéma actuel
-- À exécuter dans le SQL Editor de Supabase Dashboard

-- 1. Désactiver RLS
ALTER TABLE public.students DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_profiles DISABLE ROW LEVEL SECURITY;

-- 2. Rendre hashed_password optionnel dans students
ALTER TABLE public.students 
ALTER COLUMN hashed_password DROP NOT NULL;

-- 3. Supprimer les colonnes qui n'existent pas dans le schéma actuel
-- (si elles existent, sinon cette commande sera ignorée)
ALTER TABLE public.student_profiles 
DROP COLUMN IF EXISTS diagnostic_completed,
DROP COLUMN IF EXISTS overall_proficiency,
DROP COLUMN IF EXISTS learning_pace,
DROP COLUMN IF EXISTS preferred_teaching_mode;

-- 4. Vérifier que les colonnes du schéma actuel existent
-- Le schéma actuel a: proficiency_level, learning_style, strengths, weaknesses, etc.
-- Ces colonnes devraient déjà exister selon le schéma fourni

-- 5. Vérifier la structure finale
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
AND table_name = 'student_profiles'
ORDER BY ordinal_position;
