# 🚀 Configuration Supabase pour AI Tutor BAC

## ✅ Clés API déjà configurées

Vos clés Supabase, DeepSeek et Google Cloud ont été ajoutées au fichier `backend/.env`.

---

## 📋 Étapes de Configuration Supabase

### 1. Obtenir le mot de passe de la base de données

1. Aller sur https://supabase.com/dashboard/project/yzvlmulpqnovduqhhtjf
2. Cliquer sur **Settings** → **Database**
3. Copier le **Database Password** (ou le réinitialiser si oublié)

### 2. Mettre à jour DATABASE_URL

Éditer `backend/.env` et remplacer `YOUR_DB_PASSWORD` par votre mot de passe :

```env
DATABASE_URL=postgresql+asyncpg://postgres.yzvlmulpqnovduqhhtjf:VOTRE_MOT_DE_PASSE@aws-0-us-east-1.pooler.supabase.com:6543/postgres
DATABASE_URL_SYNC=postgresql://postgres.yzvlmulpqnovduqhhtjf:VOTRE_MOT_DE_PASSE@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

**Note** : Remplacez `VOTRE_MOT_DE_PASSE` par le mot de passe réel de votre base de données Supabase.

---

## 🗄️ Créer le schéma de base de données

### Option 1 : Via l'interface Supabase (Recommandé)

1. Aller sur https://supabase.com/dashboard/project/yzvlmulpqnovduqhhtjf/editor
2. Cliquer sur **SQL Editor**
3. Copier le contenu de `database/schema.sql`
4. Coller dans l'éditeur SQL
5. Cliquer sur **Run**

### Option 2 : Via script Python

```powershell
cd database
python seed.py
```

Le script créera automatiquement :
- Toutes les tables (students, lessons, exercises, sessions, etc.)
- Les données initiales (subjects, chapters, lessons, exercises)
- Les index et contraintes

---

## 🔑 Fichier credentials Google Cloud

Vous avez configuré Google Cloud. Pour que TTS/STT fonctionne :

1. Créer le dossier `backend/credentials/` :
```powershell
New-Item -ItemType Directory -Force -Path "backend\credentials"
```

2. Télécharger votre clé de service Google Cloud :
   - Aller sur https://console.cloud.google.com/iam-admin/serviceaccounts
   - Projet : `analytical-rain-472320-j4`
   - Créer une clé JSON pour le service account
   - Télécharger le fichier

3. Renommer le fichier en `google-cloud-key.json`

4. Placer dans `backend/credentials/google-cloud-key.json`

---

## 🧪 Tester la connexion

### Test 1 : Connexion à Supabase

```powershell
cd backend
python -c "from app.database import engine; import asyncio; asyncio.run(engine.connect())"
```

Si succès : "Connection successful"
Si erreur : Vérifier le mot de passe dans DATABASE_URL

### Test 2 : Démarrer le backend

```powershell
cd backend
uvicorn app.main:app --reload
```

Vérifier : http://localhost:8000/health

Réponse attendue : `{"status":"ok"}`

---

## 📊 Vérifier les tables Supabase

1. Aller sur https://supabase.com/dashboard/project/yzvlmulpqnovduqhhtjf/editor
2. Vérifier que ces tables existent :
   - `subjects`
   - `chapters`
   - `lessons`
   - `exercises`
   - `students`
   - `student_profiles`
   - `learning_sessions`
   - `conversation_logs`
   - `exercise_attempts`
   - `spaced_repetition_queue`
   - `ai_prompts`

---

## 🔄 Alternatives à Redis (optionnel)

Si vous n'avez pas Redis local, utilisez **Upstash Redis** (gratuit) :

1. Créer un compte : https://upstash.com/
2. Créer une base Redis
3. Copier l'URL de connexion
4. Modifier `backend/.env` :
```env
REDIS_URL=rediss://default:YOUR_PASSWORD@us1-example.upstash.io:6379
```

**Ou** : Désactiver Redis temporairement (l'app fonctionnera sans cache)

---

## 🚀 Démarrage complet

Une fois tout configuré :

### 1. Backend
```powershell
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Frontend
```powershell
cd frontend
npm install
npm run dev
```

### 3. Tester
1. Ouvrir http://localhost:5173
2. S'inscrire
3. Se connecter
4. Démarrer une session d'apprentissage

---

## ✅ Checklist de configuration

- [ ] Mot de passe Supabase récupéré
- [ ] DATABASE_URL mis à jour dans `backend/.env`
- [ ] Schéma SQL exécuté sur Supabase
- [ ] Tables créées et visibles dans Supabase
- [ ] Fichier `google-cloud-key.json` placé dans `backend/credentials/`
- [ ] Backend démarre sans erreur
- [ ] Frontend démarre sans erreur
- [ ] Test de connexion réussi
- [ ] Inscription/connexion fonctionne

---

## 🐛 Dépannage

### Erreur : "password authentication failed"
→ Vérifier le mot de passe dans DATABASE_URL

### Erreur : "relation does not exist"
→ Exécuter `database/schema.sql` sur Supabase

### Erreur : "GOOGLE_APPLICATION_CREDENTIALS not found"
→ Vérifier que `backend/credentials/google-cloud-key.json` existe

### Erreur : "Redis connection refused"
→ Utiliser Upstash Redis ou désactiver temporairement

---

## 📞 Support Supabase

- Dashboard : https://supabase.com/dashboard/project/yzvlmulpqnovduqhhtjf
- Documentation : https://supabase.com/docs
- SQL Editor : https://supabase.com/dashboard/project/yzvlmulpqnovduqhhtjf/editor

---

**Votre configuration est presque complète ! Il ne reste que le mot de passe de la base de données à ajouter.** 🎉
