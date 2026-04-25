# Créer un compte de test pour l'authentification

## 🔴 Problème actuel

L'inscription échoue avec une erreur 500. Cela peut être dû à:
1. Supabase Auth n'est pas configuré pour accepter les inscriptions
2. La confirmation d'email est requise
3. Un problème de configuration

## ✅ Solution: Créer un compte de test manuellement

### Méthode 1: Via le Dashboard Supabase (RECOMMANDÉ)

1. **Allez sur** https://supabase.com/dashboard
2. **Sélectionnez** votre projet `ldeifdnczkzgtxctjlel`
3. **Allez dans** Authentication → Users
4. **Cliquez sur** "Add user" ou "Invite user"
5. **Remplissez:**
   - Email: `test@example.com`
   - Password: `Test123!`
   - ✅ Cochez "Auto Confirm User" (important!)
6. **Cliquez sur** "Create user"

7. **Ensuite, allez dans** SQL Editor
8. **Exécutez ce script:**

```sql
-- Créer l'enregistrement étudiant
INSERT INTO public.students (
    id,
    username,
    email,
    full_name,
    preferred_language,
    is_active,
    created_at
)
SELECT 
    id,
    'test_student',
    email,
    'Étudiant Test',
    'fr',
    true,
    NOW()
FROM auth.users
WHERE email = 'test@example.com'
ON CONFLICT (email) DO NOTHING;

-- Créer le profil
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
```

### Méthode 2: Activer l'inscription publique dans Supabase

1. **Allez sur** https://supabase.com/dashboard
2. **Sélectionnez** votre projet `ldeifdnczkzgtxctjlel`
3. **Allez dans** Authentication → Settings
4. **Dans "Auth Providers"**, vérifiez que "Email" est activé
5. **Dans "Email Auth":**
   - ✅ Enable email signup
   - ✅ Disable email confirmations (pour le développement)
6. **Sauvegardez**

Ensuite, testez l'inscription depuis le frontend.

## 🧪 Tester la connexion

Une fois le compte créé:

1. **Allez sur** http://localhost:5173/login
2. **Connectez-vous avec:**
   - Email: `test@example.com`
   - Password: `Test123!`

## 🔧 Vérifier la configuration Supabase Auth

### Paramètres recommandés pour le développement:

**Authentication → Settings:**
- ✅ Enable email signup
- ❌ Disable email confirmations (pour dev)
- ✅ Enable manual linking (optionnel)

**Authentication → URL Configuration:**
- Site URL: `http://localhost:5173`
- Redirect URLs: `http://localhost:5173/**`

## 📝 Alternative: Modifier le code pour gérer les erreurs

Si vous voulez voir l'erreur exacte, modifiez temporairement le endpoint de registration pour afficher plus de détails:

```python
# Dans backend/app/api/v1/endpoints/auth.py
except Exception as e:
    import traceback
    print(f"Registration error: {str(e)}")
    print(traceback.format_exc())
    raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")
```

Puis regardez les logs du backend dans le terminal.

## 🎯 Résumé

**Pour tester rapidement:**
1. Créez un utilisateur dans Authentication → Users (Dashboard Supabase)
2. Exécutez le script SQL pour créer l'enregistrement student
3. Testez la connexion sur http://localhost:5173/login

**Pour activer l'inscription:**
1. Activez "Enable email signup" dans Authentication → Settings
2. Désactivez "Email confirmations" (pour dev)
3. Testez l'inscription sur http://localhost:5173/signup
