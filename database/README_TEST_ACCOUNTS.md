# Comptes de Test - AI Tutor BAC

## 📋 Comptes disponibles

Tous les comptes utilisent le mot de passe: **`Test123!`**

| Email | Username | Nom complet | Langue | Niveau | Statut |
|-------|----------|-------------|--------|--------|--------|
| test@example.com | test_student | Étudiant Test | Français | 2ème BAC Sciences Physiques BIOF | Actif |
| ahmed@example.com | ahmed_test | أحمد التجريبي | Arabe | 2ème BAC Sciences Physiques BIOF | Actif |
| fatima@example.com | fatima_test | Fatima Zahra | Français | 2ème BAC Sciences de la Vie et de la Terre | Actif |
| inactive@example.com | inactive_test | Compte Inactif | Français | 2ème BAC Sciences Physiques BIOF | Inactif |

## 🚀 Instructions d'utilisation

### Option 1: Créer un seul compte de test

1. Ouvrez le **SQL Editor** dans Supabase Dashboard
2. Copiez le contenu de `insert_test_student.sql`
3. Exécutez le script
4. Connectez-vous avec:
   - **Email**: `test@example.com`
   - **Password**: `Test123!`

### Option 2: Créer plusieurs comptes de test

1. Ouvrez le **SQL Editor** dans Supabase Dashboard
2. Copiez le contenu de `create_multiple_test_students.sql`
3. Exécutez le script
4. Vous aurez 4 comptes de test disponibles

## 🔧 Comment exécuter les scripts dans Supabase

1. Allez sur https://supabase.com/dashboard
2. Sélectionnez votre projet: `yzvlmulpqnovduqhhtjf`
3. Dans le menu de gauche, cliquez sur **SQL Editor**
4. Cliquez sur **New Query**
5. Collez le contenu du script SQL
6. Cliquez sur **Run** ou appuyez sur `Ctrl+Enter`

## 🔐 Générer un nouveau mot de passe hashé

Si vous voulez créer un compte avec un mot de passe différent:

```bash
cd backend
python generate_test_password.py
```

Modifiez le script Python pour changer le mot de passe, puis copiez le hash généré dans votre script SQL.

## 🗑️ Supprimer les comptes de test

```sql
-- Supprimer tous les comptes de test
DELETE FROM public.students 
WHERE email LIKE '%@example.com';
```

## ⚠️ Important

- Ces comptes sont **uniquement pour le développement et les tests**
- Ne les utilisez **jamais en production**
- Le mot de passe `Test123!` est faible et prévisible
- Supprimez ces comptes avant de déployer en production

## 🧪 Tester l'authentification

### Via l'API REST

```bash
# Test de login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "Test123!"
  }'
```

### Via l'interface frontend

1. Démarrez le frontend: `cd frontend && npm run dev`
2. Allez sur http://localhost:5173
3. Cliquez sur "Se connecter"
4. Utilisez les identifiants ci-dessus
