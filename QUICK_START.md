# 🚀 Quick Start - AI Tutor BAC

## ⚡ Démarrage Rapide (5 minutes)

### Prérequis
- ✅ Docker Desktop installé
- ✅ Node.js installé
- ✅ Python 3.11+ installé

---

## 📋 Étapes d'Installation

### 1️⃣ Cloner et naviguer
```powershell
cd C:\Users\HP\Desktop\ai-tutor-bac
```

### 2️⃣ Démarrer les services Docker
```powershell
docker compose up -d db redis
```

Vérifier que les services sont actifs :
```powershell
docker compose ps
```

### 3️⃣ Configurer les clés API

Éditer `backend\.env` et ajouter votre clé DeepSeek :
```env
DEEPSEEK_API_KEY=sk-votre-cle-ici
```

**Obtenir une clé** : https://platform.deepseek.com/

### 4️⃣ Initialiser la base de données
```powershell
cd database
python seed.py
```

### 5️⃣ Démarrer le backend
```powershell
cd ..\backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Le backend sera sur : http://localhost:8000

### 6️⃣ Démarrer le frontend (nouveau terminal)
```powershell
cd frontend
npm install
npm run dev
```

Le frontend sera sur : http://localhost:5173

---

## 🎉 Tester l'Application

1. Ouvrir http://localhost:5173
2. Cliquer sur **"S'inscrire"**
3. Créer un compte étudiant
4. Se connecter
5. Cliquer sur **"Physique"** → **"Ondes mécaniques progressives"**
6. Démarrer une session d'apprentissage
7. Interagir avec le tuteur IA (texte ou voix)

---

## 🔧 Dépannage Rapide

### Docker n'est pas reconnu
→ Installer Docker Desktop : https://www.docker.com/products/docker-desktop/

### Port 5432 déjà utilisé
→ Arrêter PostgreSQL local ou changer le port dans `docker-compose.yml`

### Erreur "Module not found"
```powershell
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Images ne s'affichent pas
→ Normal, les images doivent être créées (voir `CONTENT_CREATION_GUIDE.md`)
→ Utiliser des placeholders temporaires

---

## 📚 Documentation Complète

- **Installation détaillée** : `SETUP_GUIDE.md`
- **Résumé implémentation** : `IMPLEMENTATION_SUMMARY.md`
- **Création de contenu** : `CONTENT_CREATION_GUIDE.md`
- **Plan complet** : `.windsurf/plans/ai-tutor-bac-completion-plan-b23de0.md`

---

## ✨ Fonctionnalités Disponibles

✅ Conversation audio/écrite avec l'IA
✅ 5 phases pédagogiques automatiques
✅ Affichage de médias visuels
✅ Exercices interactifs (QCM, numériques)
✅ Contrôle intelligent par l'IA
✅ Support bilingue (français/arabe)

---

## 🎯 Prochaines Étapes

1. ✅ Tester l'application
2. 📝 Créer plus de contenu pédagogique
3. 🎨 Ajouter des images et simulations
4. 🚀 Déployer en production

**Bon apprentissage ! 🎓**
