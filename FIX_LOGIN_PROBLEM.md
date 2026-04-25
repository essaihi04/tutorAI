# 🔴 Problème de connexion - Solution

## Problème identifié

Vous avez des utilisateurs dans la table `students` mais ils n'existent **pas dans Supabase Auth**. 

Quand vous vous êtes inscrit, l'utilisateur a été créé dans la table `students` mais peut-être pas dans `auth.users` (Supabase Auth).

## ✅ Solution 1: Créer l'utilisateur dans Supabase Auth manuellement

### Étape 1: Allez dans Supabase Dashboard

1. **Allez sur** https://supabase.com/dashboard
2. **Sélectionnez** votre projet `ldeifdnczkzgtxctjlel`
3. **Allez dans** Authentication → Users

### Étape 2: Créez l'utilisateur Auth

1. **Cliquez sur** "Add user" ou "Invite user"
2. **Remplissez:**
   - Email: `zizo76416@gmail.com` (ou l'email que vous avez utilisé)
   - Password: Le mot de passe que vous avez choisi
   - ✅ **Cochez "Auto Confirm User"** (très important!)
3. **Cliquez sur** "Create user"

### Étape 3: Lier l'utilisateur Auth à la table students

Exécutez ce SQL dans **SQL Editor**:

```sql
-- Mettre à jour l'ID dans la table students pour correspondre à l'ID de auth.users
UPDATE public.students s
SET id = (
    SELECT id 
    FROM auth.users 
    WHERE email = s.email
    LIMIT 1
)
WHERE email = 'zizo76416@gmail.com';  -- Remplacez par votre email

-- Mettre à jour student_profiles aussi
UPDATE public.student_profiles sp
SET student_id = (
    SELECT id 
    FROM auth.users 
    WHERE email = 'zizo76416@gmail.com'
    LIMIT 1
)
WHERE student_id IN (
    SELECT id FROM public.students WHERE email = 'zizo76416@gmail.com'
);
```

## ✅ Solution 2: Supprimer et recréer le compte (PLUS SIMPLE)

### Étape 1: Supprimer les données existantes

Dans **SQL Editor**:

```sql
-- Supprimer les profils
DELETE FROM public.student_profiles 
WHERE student_id IN (
    SELECT id FROM public.students 
    WHERE email = 'zizo76416@gmail.com'
);

-- Supprimer l'étudiant
DELETE FROM public.students 
WHERE email = 'zizo76416@gmail.com';
```

### Étape 2: S'inscrire à nouveau

1. Allez sur http://localhost:5174/signup
2. Inscrivez-vous avec le même email
3. Cette fois, l'utilisateur sera créé dans Supabase Auth ET dans la table students

## 🧪 Tester la connexion

Après avoir appliqué l'une des solutions:

1. Allez sur http://localhost:5174/login
2. Connectez-vous avec:
   - Email: votre email
   - Password: votre mot de passe
3. La connexion devrait fonctionner ! ✅

## 📝 Pourquoi ce problème ?

Lors de l'inscription, il y a 2 étapes:
1. **Créer l'utilisateur dans Supabase Auth** (gère le mot de passe)
2. **Créer l'enregistrement dans la table students** (infos du profil)

Si l'étape 1 échoue mais l'étape 2 réussit, vous avez un utilisateur dans `students` mais pas dans `auth.users`, donc la connexion échoue.

## 💡 Recommandation

**Solution 2** (supprimer et recréer) est la plus simple et garantit que tout est bien synchronisé.
