-- Script SQL pour créer un compte étudiant de test
-- Base de données: Supabase PostgreSQL
-- 
-- Identifiants du compte de test:
-- Email: test@example.com
-- Username: test_student
-- Password: Test123!

-- Insérer un étudiant de test
INSERT INTO public.students (
    id,
    email,
    username,
    hashed_password,
    full_name,
    school_level,
    preferred_language,
    is_active,
    created_at,
    last_login
) VALUES (
    extensions.uuid_generate_v4(),
    'test@example.com',
    'test_student',
    '$2b$12$sT6lMnWtKF4zp3A.LrpAe./sR8oykWsABX00CXqvLytSrTfS/fHTW',
    'Étudiant Test',
    '2eme BAC Sciences Physiques BIOF',
    'fr',
    true,
    NOW(),
    NULL
)
ON CONFLICT (email) DO NOTHING;

-- Vérifier que l'insertion a réussi
SELECT 
    id,
    email,
    username,
    full_name,
    school_level,
    preferred_language,
    is_active,
    created_at
FROM public.students
WHERE email = 'test@example.com';
