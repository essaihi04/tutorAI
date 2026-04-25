-- Script pour créer un compte de test dans Supabase
-- À exécuter dans le SQL Editor de Supabase Dashboard

-- 1. Créer un utilisateur dans auth.users (Supabase Auth)
-- Note: Supabase Auth gère automatiquement les utilisateurs lors de l'inscription
-- Nous allons créer directement un enregistrement dans la table students

-- 2. Insérer un étudiant de test dans la table students
INSERT INTO public.students (
    id,
    username,
    email,
    full_name,
    preferred_language,
    is_active,
    created_at
) VALUES (
    gen_random_uuid(),
    'test_student',
    'test@example.com',
    'Étudiant Test',
    'fr',
    true,
    NOW()
) ON CONFLICT (email) DO NOTHING;

-- 3. Créer le profil associé
INSERT INTO public.student_profiles (
    id,
    student_id,
    diagnostic_completed,
    overall_proficiency,
    learning_pace,
    preferred_teaching_mode
)
SELECT 
    gen_random_uuid(),
    s.id,
    false,
    'beginner',
    'medium',
    'mixed'
FROM public.students s
WHERE s.email = 'test@example.com'
ON CONFLICT (student_id) DO NOTHING;

-- 4. Vérifier que l'insertion a réussi
SELECT 
    s.id,
    s.username,
    s.email,
    s.full_name,
    s.preferred_language,
    s.is_active,
    s.created_at,
    sp.id as profile_id
FROM public.students s
LEFT JOIN public.student_profiles sp ON sp.student_id = s.id
WHERE s.email = 'test@example.com';

-- Note importante:
-- Pour que ce compte puisse se connecter via Supabase Auth,
-- vous devez également créer l'utilisateur dans le Dashboard Supabase:
-- 1. Allez dans Authentication > Users
-- 2. Cliquez sur "Add user"
-- 3. Email: test@example.com
-- 4. Password: Test123!
-- 5. Cochez "Auto Confirm User"
