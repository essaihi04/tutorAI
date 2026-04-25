# Configuration du nouveau projet Supabase

## ✅ Changements effectués

J'ai mis à jour les fichiers de configuration avec les nouvelles informations du projet Supabase:

### Projet Supabase
- **Ancien projet**: `yzvlmulpqnovduqhhtjf`
- **Nouveau projet**: `ldeifdnczkzgtxctjlel`
- **URL**: https://ldeifdnczkzgtxctjlel.supabase.co

### Fichiers mis à jour
- ✅ `backend/.env` - Nouvelles clés API et URL Supabase

## 🔑 Étapes à compléter

### 1. Obtenir le mot de passe de la base de données

1. Allez sur https://supabase.com/dashboard
2. Sélectionnez votre projet **ldeifdnczkzgtxctjlel**
3. Allez dans **Settings** → **Database**
4. Copiez le **Database Password**

### 2. Mettre à jour le fichier .env

Ouvrez `backend/.env` et remplacez `[YOUR_DB_PASSWORD]` par le vrai mot de passe:

```env
DATABASE_URL=postgresql+asyncpg://postgres:VOTRE_MOT_DE_PASSE@db.ldeifdnczkzgtxctjlel.supabase.co:5432/postgres
DATABASE_URL_SYNC=postgresql://postgres:VOTRE_MOT_DE_PASSE@db.ldeifdnczkzgtxctjlel.supabase.co:5432/postgres
```

### 3. Mettre à jour le fichier hosts (si nécessaire)

Si vous avez des problèmes de DNS, mettez à jour `C:\Windows\System32\drivers\etc\hosts`:

**Remplacez:**
```
[ADRESSE_IP]  db.yzvlmulpqnovduqhhtjf.supabase.co
```

**Par:**
```
[ADRESSE_IP]  db.ldeifdnczkzgtxctjlel.supabase.co
```

Pour obtenir l'adresse IP, utilisez https://www.nslookup.io/ avec `db.ldeifdnczkzgtxctjlel.supabase.co`

### 4. Initialiser la base de données

Exécutez le script SQL dans Supabase Dashboard:

1. Allez dans **SQL Editor** dans Supabase Dashboard
2. Cliquez sur **New Query**
3. Copiez le contenu de `database/init_supabase.sql`
4. Exécutez le script (Ctrl+Enter)

### 5. Créer un compte de test

Dans le **SQL Editor**, exécutez:

```sql
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
    gen_random_uuid(),
    'test@example.com',
    'test_student',
    '$2b$12$sT6lMnWtKF4zp3A.LrpAe./sR8oykWsABX00CXqvLytSrTfS/fHTW',
    'Étudiant Test',
    '2eme BAC Sciences Physiques BIOF',
    'fr',
    true
) ON CONFLICT (email) DO NOTHING;
```

**Identifiants de test:**
- Email: `test@example.com`
- Mot de passe: `Test123!`

### 6. Tester la connexion

```bash
cd backend
python test_new_supabase.py
```

Entrez le mot de passe de la base de données quand demandé.

### 7. Démarrer le backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 8. Démarrer le frontend

```bash
cd frontend
npm run dev
```

### 9. Tester l'authentification

1. Allez sur http://localhost:5173/login
2. Utilisez les identifiants de test:
   - Email: `test@example.com`
   - Mot de passe: `Test123!`

## 🔍 Vérification

Si tout fonctionne correctement, vous devriez voir:
- ✅ Backend démarre sans erreur
- ✅ Frontend charge correctement
- ✅ Connexion réussie avec le compte de test
- ✅ Redirection vers le dashboard après connexion

## ⚠️ Problèmes courants

### Erreur: getaddrinfo failed
- Vérifiez votre connexion Internet
- Mettez à jour le fichier hosts (voir étape 3)
- Essayez avec un VPN

### Erreur: Invalid password
- Vérifiez que vous avez copié le bon mot de passe depuis Supabase Dashboard
- Assurez-vous qu'il n'y a pas d'espaces avant/après le mot de passe

### Erreur: Table does not exist
- Exécutez le script `init_supabase.sql` dans le SQL Editor (étape 4)

## 📝 Résumé des credentials

```env
# Supabase
SUPABASE_URL=https://ldeifdnczkzgtxctjlel.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkZWlmZG5jemt6Z3R4Y3RqbGVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMwNTcxMTUsImV4cCI6MjA3ODYzMzExNX0._6t-wGotwy00NafsRnvXdmX7SXg6z5Cd6B98889Ic1o
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkZWlmZG5jemt6Z3R4Y3RqbGVsIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc2MzA1NzExNSwiZXhwIjoyMDc4NjMzMTE1fQ.uDZEO-RBNDszxBuhK7I11K6FTc8b4U2jYJzN5gMtPJQ

# Database (à compléter avec votre mot de passe)
DATABASE_URL=postgresql+asyncpg://postgres:[YOUR_PASSWORD]@db.ldeifdnczkzgtxctjlel.supabase.co:5432/postgres
```
