-- Fix Row-Level Security (RLS) pour permettre l'inscription
-- À exécuter dans le SQL Editor de Supabase Dashboard

-- Option 1: Désactiver RLS pour le développement (SIMPLE - RECOMMANDÉ POUR DEV)
ALTER TABLE public.students DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_profiles DISABLE ROW LEVEL SECURITY;

-- Option 2: Créer des policies RLS appropriées (POUR PRODUCTION)
-- Décommentez ces lignes si vous voulez garder RLS activé

/*
-- Activer RLS
ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_profiles ENABLE ROW LEVEL SECURITY;

-- Policy pour permettre l'insertion (signup)
CREATE POLICY "Allow public insert for students" 
ON public.students 
FOR INSERT 
TO anon, authenticated
WITH CHECK (true);

-- Policy pour permettre la lecture de son propre profil
CREATE POLICY "Users can read own student record" 
ON public.students 
FOR SELECT 
TO authenticated
USING (auth.uid() = id);

-- Policy pour permettre la mise à jour de son propre profil
CREATE POLICY "Users can update own student record" 
ON public.students 
FOR UPDATE 
TO authenticated
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

-- Policies pour student_profiles
CREATE POLICY "Allow public insert for student_profiles" 
ON public.student_profiles 
FOR INSERT 
TO anon, authenticated
WITH CHECK (true);

CREATE POLICY "Users can read own profile" 
ON public.student_profiles 
FOR SELECT 
TO authenticated
USING (student_id = auth.uid());

CREATE POLICY "Users can update own profile" 
ON public.student_profiles 
FOR UPDATE 
TO authenticated
USING (student_id = auth.uid())
WITH CHECK (student_id = auth.uid());
*/

-- Vérifier que RLS est désactivé
SELECT 
    schemaname,
    tablename,
    rowsecurity
FROM pg_tables
WHERE schemaname = 'public' 
AND tablename IN ('students', 'student_profiles');
