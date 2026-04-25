# 🔴 SOLUTION: Erreur Row-Level Security (RLS)

## Problème identifié

L'erreur exacte est:
```
new row violates row-level security policy for table "students"
```

Cela signifie que **Supabase a activé Row-Level Security (RLS)** sur la table `students`, ce qui bloque toutes les insertions par défaut.

## ✅ Solution rapide (pour le développement)

### Étape 1: Désactiver RLS

1. **Allez sur** https://supabase.com/dashboard
2. **Sélectionnez** votre projet `ldeifdnczkzgtxctjlel`
3. **Allez dans** SQL Editor
4. **Exécutez ce script:**

```sql
-- Désactiver RLS pour le développement
ALTER TABLE public.students DISABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_profiles DISABLE ROW LEVEL SECURITY;

-- Vérifier que c'est désactivé
SELECT 
    tablename,
    rowsecurity
FROM pg_tables
WHERE schemaname = 'public' 
AND tablename IN ('students', 'student_profiles');
```

### Étape 2: Tester l'inscription

1. Allez sur http://localhost:5173/signup
2. Créez un compte avec:
   - Nom complet: Votre nom
   - Username: votre_username
   - Email: votre@email.com
   - Mot de passe: minimum 6 caractères
   - Langue: Français

3. L'inscription devrait maintenant fonctionner ! ✅

## 🔒 Pour la production (avec RLS activé)

Si vous voulez garder RLS activé pour la sécurité, créez des policies appropriées:

```sql
-- Activer RLS
ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.student_profiles ENABLE ROW LEVEL SECURITY;

-- Permettre l'inscription publique
CREATE POLICY "Allow public insert for students" 
ON public.students 
FOR INSERT 
TO anon, authenticated
WITH CHECK (true);

-- Permettre la lecture de son propre profil
CREATE POLICY "Users can read own student record" 
ON public.students 
FOR SELECT 
TO authenticated
USING (auth.uid() = id);

-- Permettre la mise à jour de son propre profil
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
```

## 📝 Explication

**Row-Level Security (RLS)** est une fonctionnalité de sécurité PostgreSQL/Supabase qui:
- Contrôle qui peut lire/écrire chaque ligne d'une table
- Bloque toutes les opérations par défaut quand activé
- Nécessite des "policies" pour autoriser les opérations

**Pour le développement:** Désactivez RLS pour simplifier
**Pour la production:** Créez des policies appropriées pour sécuriser vos données

## 🎯 Résumé

1. **Exécutez le script SQL** pour désactiver RLS
2. **Testez l'inscription** sur http://localhost:5173/signup
3. **Profitez de votre application** avec les pages d'auth modernes ! 🎨

Le fichier complet est dans `database/fix_rls_policies.sql`
