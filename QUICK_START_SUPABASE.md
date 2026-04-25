# 🚀 Quick Start avec Supabase - AI Tutor BAC

## ⚡ Démarrage en 3 étapes

Vos clés API sont déjà configurées ! Il ne reste que 3 étapes simples.

---

## Étape 1 : Obtenir le mot de passe Supabase (2 min)

1. Aller sur https://supabase.com/dashboard/project/yzvlmulpqnovduqhhtjf/settings/database
2. Sous **"Database Password"**, cliquer sur **"Reset Database Password"** (ou copier si vous l'avez)
3. Copier le nouveau mot de passe

4. Éditer `backend\.env` et remplacer `YOUR_DB_PASSWORD` par votre mot de passe :

```env
DATABASE_URL=postgresql+asyncpg://postgres.yzvlmulpqnovduqhhtjf:VOTRE_MOT_DE_PASSE_ICI@aws-0-us-east-1.pooler.supabase.com:6543/postgres
DATABASE_URL_SYNC=postgresql://postgres.yzvlmulpqnovduqhhtjf:VOTRE_MOT_DE_PASSE_ICI@aws-0-us-east-1.pooler.supabase.com:6543/postgres
```

---

## Étape 2 : Initialiser la base de données (3 min)

### Option A : Via l'interface Supabase (Recommandé)

1. Aller sur https://supabase.com/dashboard/project/yzvlmulpqnovduqhhtjf/sql/new
2. Copier tout le contenu de `database\init_supabase.sql`
3. Coller dans l'éditeur SQL
4. Cliquer sur **"Run"** (en bas à droite)
5. Attendre ~30 secondes

✅ Vous devriez voir : "Success. No rows returned"

### Option B : Via script Python

```powershell
cd database
python seed_supabase.py
```

**Note** : Modifier le mot de passe dans `seed_supabase.py` ligne 16 avant d'exécuter

---

## Étape 3 : Démarrer l'application (2 min)

### Backend
```powershell
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Vérifier : http://localhost:8000/health
Réponse attendue : `{"status":"ok"}`

### Frontend (nouveau terminal)
```powershell
cd frontend
npm install
npm run dev
```

Ouvrir : http://localhost:5173

---

## 🎉 Tester l'application

1. Cliquer sur **"S'inscrire"**
2. Créer un compte :
   - Email : `test@example.com`
   - Username : `testuser`
   - Nom complet : `Test User`
   - Mot de passe : `password123`
3. Se connecter
4. Cliquer sur **"Physique"** → **"Ondes mécaniques progressives"**
5. Démarrer une session
6. Parler ou écrire au tuteur IA

---

## ✅ Vérifications

### Base de données créée ?
https://supabase.com/dashboard/project/yzvlmulpqnovduqhhtjf/editor

Vérifier que ces tables existent :
- subjects
- chapters
- lessons
- exercises
- students
- learning_sessions

### Backend fonctionne ?
```powershell
curl http://localhost:8000/health
```
Réponse : `{"status":"ok"}`

### Frontend fonctionne ?
Ouvrir http://localhost:5173
Voir la page d'accueil

---

## 🔑 Clés API configurées

✅ **Supabase** : Configuré  
✅ **DeepSeek** : `sk-2ee85b6898e64811bca013babc6daace`  
✅ **Google Cloud** : Projet `analytical-rain-472320-j4`  
✅ **Gemini** : `AIzaSyCas6Clc7vN25p6qx_uIqNtflQRvHN_KrI`  

---

## 📁 Fichier Google Cloud (optionnel)

Pour activer TTS/STT Google Cloud :

1. Créer `backend\credentials\` :
```powershell
New-Item -ItemType Directory -Force -Path "backend\credentials"
```

2. Télécharger la clé de service :
   - https://console.cloud.google.com/iam-admin/serviceaccounts?project=analytical-rain-472320-j4
   - Créer une clé JSON
   - Télécharger

3. Renommer en `google-cloud-key.json`

4. Placer dans `backend\credentials\google-cloud-key.json`

**Alternative** : L'app fonctionne sans Google Cloud (mode texte uniquement)

---

## 🐛 Dépannage

### Erreur : "password authentication failed"
→ Vérifier le mot de passe dans `backend\.env`

### Erreur : "relation does not exist"
→ Exécuter `database\init_supabase.sql` sur Supabase

### Erreur : "ModuleNotFoundError"
→ `pip install -r requirements.txt` dans `backend\`

### Erreur : "npm ERR!"
→ `npm install` dans `frontend\`

### Backend ne démarre pas
→ Vérifier que le mot de passe est correct dans `.env`

---

## 📚 Documentation complète

- **Configuration Supabase** : `SUPABASE_SETUP.md`
- **Guide complet** : `SETUP_GUIDE.md`
- **Résumé implémentation** : `IMPLEMENTATION_SUMMARY.md`

---

## 🎯 Prochaines étapes

Une fois l'app lancée :

1. ✅ Tester la conversation avec l'IA
2. 📝 Créer plus de leçons (voir `CONTENT_CREATION_GUIDE.md`)
3. 🎨 Ajouter des images dans `frontend\public\media\`
4. 🚀 Déployer en production

---

**Votre app est prête ! Bon apprentissage ! 🎓**
