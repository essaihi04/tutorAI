# 🔑 Obtenir le JWT Secret de Supabase

## Le Problème

Le backend a besoin du **JWT Secret** de Supabase pour valider les tokens d'authentification.

## ✅ Solution - Récupérer le JWT Secret

### Étape 1: Allez sur Supabase Dashboard

1. Ouvrez https://supabase.com/dashboard
2. Sélectionnez votre projet **ldeifdnczkzgtxctjlel**

### Étape 2: Accédez aux Paramètres API

1. Dans le menu de gauche, cliquez sur **⚙️ Settings**
2. Cliquez sur **API**

### Étape 3: Copiez le JWT Secret

Vous verrez plusieurs clés:

```
Project URL: https://ldeifdnczkzgtxctjlel.supabase.co

API Keys:
├── anon / public (déjà dans .env)
├── service_role (déjà dans .env)
└── JWT Settings
    └── JWT Secret ← CELUI-CI !
```

**Copiez le JWT Secret** (c'est une longue chaîne de caractères)

### Étape 4: Ajoutez-le au fichier .env

1. Ouvrez `backend/.env`
2. Remplacez cette ligne:
   ```
   SUPABASE_JWT_SECRET=your-jwt-secret-here-get-from-supabase-dashboard
   ```
   
   Par:
   ```
   SUPABASE_JWT_SECRET=votre-jwt-secret-copié
   ```

### Étape 5: Redémarrez le Backend

**Important:** Le backend doit redémarrer pour charger la nouvelle variable.

1. Arrêtez le backend (Ctrl+C dans le terminal)
2. Relancez:
   ```bash
   cd backend
   python -m uvicorn app.main:app --reload
   ```

---

## 🎯 Exemple Complet

Votre `.env` devrait ressembler à:

```env
# Supabase Database
SUPABASE_URL=https://ldeifdnczkzgtxctjlel.supabase.co
SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
SUPABASE_JWT_SECRET=votre-secret-jwt-ici-tres-long
```

---

## 🧪 Vérification

Après avoir ajouté le JWT Secret et redémarré:

1. **Déconnectez-vous** du Dashboard
2. **Reconnectez-vous**
3. **Essayez de démarrer une session**
4. ✅ **Ça devrait fonctionner !**

---

## 💡 Pourquoi C'est Nécessaire ?

Le **JWT Secret** est utilisé pour:
- ✅ Vérifier que les tokens sont authentiques
- ✅ Décoder les informations de l'utilisateur
- ✅ Valider que le token n'a pas été modifié

Sans ce secret, le backend ne peut pas valider les tokens Supabase.

---

## 🔍 Si Vous Ne Trouvez Pas le JWT Secret

### Option 1: Via l'Interface Supabase

**Settings** → **API** → Descendez jusqu'à **JWT Settings**

### Option 2: Via la Documentation

Le JWT Secret est aussi appelé:
- "JWT Secret"
- "JWT Signing Secret"
- "Service Secret"

### Option 3: Créer un Nouveau Projet

Si vraiment vous ne trouvez pas:
1. Le JWT Secret est généré automatiquement
2. Il devrait être visible dans Settings → API
3. Si absent, contactez le support Supabase

---

## ⚠️ Sécurité

**Ne partagez JAMAIS votre JWT Secret !**

- ❌ Ne le commitez pas sur GitHub
- ❌ Ne le partagez pas publiquement
- ✅ Gardez-le uniquement dans `.env`
- ✅ Ajoutez `.env` à `.gitignore`

---

## 📝 Résumé

1. **Supabase Dashboard** → Settings → API
2. **Copiez** le JWT Secret
3. **Ajoutez** à `backend/.env`
4. **Redémarrez** le backend
5. **Reconnectez-vous** sur le frontend
6. ✅ **Testez** !

C'est tout ! 🚀
