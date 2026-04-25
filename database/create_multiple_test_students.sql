-- Script SQL pour créer plusieurs comptes étudiants de test
-- Base de données: Supabase PostgreSQL
-- 
-- Tous les comptes utilisent le même mot de passe: Test123!

-- Compte de test 1: Étudiant principal
INSERT INTO public.students (
    id,
    email,
    username,
    hashed_password,
    full_name,
    school_level,
    preferred_language,
    is_active
) VALUES (
    extensions.uuid_generate_v4(),
    'test@example.com',
    'test_student',
    '$2b$12$sT6lMnWtKF4zp3A.LrpAe./sR8oykWsABX00CXqvLytSrTfS/fHTW',
    'Étudiant Test',
    '2eme BAC Sciences Physiques BIOF',
    'fr',
    true
) ON CONFLICT (email) DO NOTHING;

-- Compte de test 2: Étudiant arabophone
INSERT INTO public.students (
    id,
    email,
    username,
    hashed_password,
    full_name,
    school_level,
    preferred_language,
    is_active
) VALUES (
    extensions.uuid_generate_v4(),
    'ahmed@example.com',
    'ahmed_test',
    '$2b$12$sT6lMnWtKF4zp3A.LrpAe./sR8oykWsABX00CXqvLytSrTfS/fHTW',
    'أحمد التجريبي',
    '2eme BAC Sciences Physiques BIOF',
    'ar',
    true
) ON CONFLICT (email) DO NOTHING;

-- Compte de test 3: Étudiant SVT
INSERT INTO public.students (
    id,
    email,
    username,
    hashed_password,
    full_name,
    school_level,
    preferred_language,
    is_active
) VALUES (
    extensions.uuid_generate_v4(),
    'fatima@example.com',
    'fatima_test',
    '$2b$12$sT6lMnWtKF4zp3A.LrpAe./sR8oykWsABX00CXqvLytSrTfS/fHTW',
    'Fatima Zahra',
    '2eme BAC Sciences de la Vie et de la Terre',
    'fr',
    true
) ON CONFLICT (email) DO NOTHING;

-- Compte de test 4: Compte inactif
INSERT INTO public.students (
    id,
    email,
    username,
    hashed_password,
    full_name,
    school_level,
    preferred_language,
    is_active
) VALUES (
    extensions.uuid_generate_v4(),
    'inactive@example.com',
    'inactive_test',
    '$2b$12$sT6lMnWtKF4zp3A.LrpAe./sR8oykWsABX00CXqvLytSrTfS/fHTW',
    'Compte Inactif',
    '2eme BAC Sciences Physiques BIOF',
    'fr',
    false
) ON CONFLICT (email) DO NOTHING;

-- Afficher tous les comptes de test créés
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
WHERE email LIKE '%@example.com'
ORDER BY created_at DESC;
