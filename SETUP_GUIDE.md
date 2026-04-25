# Guide d'Installation AI Tutor BAC

## Prérequis

### 1. Docker Desktop (Requis)
Docker n'est pas installé sur votre système. Installez-le :
- **Télécharger** : https://www.docker.com/products/docker-desktop/
- **Installer** Docker Desktop pour Windows
- **Redémarrer** votre ordinateur après installation

### 2. Node.js (pour le frontend)
Vérifiez si installé : `node --version`
Si non installé : https://nodejs.org/ (version LTS recommandée)

### 3. Python 3.11+ (pour le backend)
Vérifiez si installé : `python --version`

---

## Étapes d'Installation

### Étape 1 : Démarrer les services Docker

```powershell
cd C:\Users\HP\Desktop\ai-tutor-bac
docker compose up -d db redis
```

Vérifier que les services sont actifs :
```powershell
docker compose ps
```

### Étape 2 : Initialiser la base de données

```powershell
cd database
python seed.py
```

### Étape 3 : Installer les dépendances backend

```powershell
cd backend
pip install -r requirements.txt
```

### Étape 4 : Démarrer le backend

```powershell
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Le backend sera accessible sur : http://localhost:8000

### Étape 5 : Installer les dépendances frontend

```powershell
cd frontend
npm install
```

### Étape 6 : Démarrer le frontend

```powershell
cd frontend
npm run dev
```

Le frontend sera accessible sur : http://localhost:5173

---

## Configuration des Clés API

### DeepSeek (LLM)
1. Créer un compte sur https://platform.deepseek.com/
2. Obtenir une clé API
3. Modifier `backend/.env` :
   ```
   DEEPSEEK_API_KEY=sk-votre-cle-ici
   ```

### Google Cloud (STT/TTS) - Optionnel pour développement
1. Créer un projet sur https://console.cloud.google.com/
2. Activer Speech-to-Text et Text-to-Speech APIs
3. Créer un service account et télécharger le JSON
4. Placer le fichier dans `backend/credentials/service-account.json`
5. Modifier `backend/.env` :
   ```
   GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account.json
   ```

**Alternative locale (sans Google Cloud)** :
- STT : Utiliser Whisper (OpenAI)
- TTS : Utiliser Coqui TTS

---

## Vérification de l'Installation

### Test Backend
```powershell
curl http://localhost:8000/health
```
Réponse attendue : `{"status":"ok"}`

### Test Frontend
Ouvrir http://localhost:5173 dans le navigateur
Vous devriez voir la page d'accueil

### Test Authentification
1. Cliquer sur "S'inscrire"
2. Créer un compte
3. Se connecter
4. Accéder au Dashboard

---

## Dépannage

### Erreur : "Docker n'est pas reconnu"
→ Installer Docker Desktop et redémarrer

### Erreur : "Port 5432 déjà utilisé"
→ PostgreSQL est déjà installé localement
→ Arrêter le service local ou changer le port dans docker-compose.yml

### Erreur : "Module not found"
→ Backend : `pip install -r requirements.txt`
→ Frontend : `npm install`

### Erreur : "DEEPSEEK_API_KEY invalid"
→ Vérifier la clé dans backend/.env
→ Ou utiliser une alternative locale (Ollama)

---

## Prochaines Étapes

Une fois l'installation terminée :
1. ✅ Tester l'authentification
2. ✅ Créer un compte étudiant
3. ✅ Explorer le Dashboard
4. ✅ Démarrer une session d'apprentissage
5. 🔧 Compléter le contenu pédagogique (Phase 4)
