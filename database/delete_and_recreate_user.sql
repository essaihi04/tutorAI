-- Supprimer un utilisateur existant pour pouvoir se réinscrire
-- À exécuter dans le SQL Editor de Supabase Dashboard

-- REMPLACEZ 'votre@email.com' par votre vrai email

-- 1. Supprimer le profil étudiant
DELETE FROM public.student_profiles 
WHERE student_id IN (
    SELECT id FROM public.students 
    WHERE email = 'zizo76416@gmail.com'  -- CHANGEZ ICI
);

-- 2. Supprimer l'enregistrement étudiant
DELETE FROM public.students 
WHERE email = 'zizo76416@gmail.com';  -- CHANGEZ ICI

-- 3. Vérifier que c'est supprimé
SELECT * FROM public.students WHERE email = 'zizo76416@gmail.com';  -- CHANGEZ ICI
-- Devrait retourner 0 lignes

-- 4. Maintenant, allez sur http://localhost:5174/signup et inscrivez-vous à nouveau
