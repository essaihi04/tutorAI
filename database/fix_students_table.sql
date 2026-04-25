-- Fix: Rendre hashed_password optionnel car Supabase Auth gère les mots de passe
-- À exécuter dans le SQL Editor de Supabase Dashboard

-- 1. Désactiver RLS (si pas déjà fait)
ALTER TABLE public.students DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_profiles DISABLE ROW LEVEL SECURITY;

-- 2. Rendre hashed_password optionnel (nullable)
ALTER TABLE public.students 
ALTER COLUMN hashed_password DROP NOT NULL;

-- 3. Vérifier la structure de la table
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_schema = 'public' 
AND table_name = 'students'
ORDER BY ordinal_position;
