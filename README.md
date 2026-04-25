# 🎓 AI Tutor BAC - Tuteur Intelligent pour le Baccalauréat Marocain

Plateforme d'apprentissage interactive avec IA conversationnelle, médias visuels et contrôle pédagogique intelligent pour les étudiants du 2ème BAC Sciences Physiques BIOF.

---

## ✨ Fonctionnalités

### 🗣️ Conversation Interactive
- **Audio** : Parlez avec le tuteur IA (Speech-to-Text)
- **Texte** : Écrivez vos réponses
- **Réponses vocales** : Le tuteur répond en audio (Text-to-Speech)
- **Bilingue** : Français et Arabe

### 🎨 Médias Visuels
- **Images explicatives** : Schémas, diagrammes, illustrations
- **Simulations interactives** : Manipulez des concepts physiques
- **Vidéos pédagogiques** : Courtes vidéos explicatives
- **Affichage automatique** : L'IA décide quand montrer les médias

### 🧠 Contrôle Intelligent
- **Progression automatique** : L'IA décide quand avancer
- **Adaptation au niveau** : Exercices adaptés à l'étudiant
- **Détection de compréhension** : Évalue en temps réel
- **Feedback immédiat** : Corrections et encouragements

### 📚 Pédagogie Structurée
1. **Activation** : Rappel des connaissances antérieures
2. **Exploration** : Découverte guidée du concept
3. **Explication** : Structuration et formalisation
4. **Application** : Exercices pratiques
5. **Consolidation** : Résumé et ancrage

### 📊 Suivi de Progression
- Profil étudiant personnalisé
- Historique des sessions
- Statistiques de performance
- Système de révision espacée (Spaced Repetition)

---

## 🚀 Installation Rapide

### Prérequis
- Docker Desktop
- Node.js 18+
- Python 3.11+

### Démarrage en 5 minutes

```powershell
# 1. Démarrer les services
docker compose up -d db redis

# 2. Initialiser la base de données
cd database
python seed.py

# 3. Démarrer le backend
cd ../backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# 4. Démarrer le frontend (nouveau terminal)
cd frontend
npm install
npm run dev
```

**Voir** : `QUICK_START.md` pour les détails

---

## 📖 Documentation

- **[Quick Start](QUICK_START.md)** - Démarrage rapide (5 min)
- **[Setup Guide](SETUP_GUIDE.md)** - Installation détaillée
- **[Implementation Summary](IMPLEMENTATION_SUMMARY.md)** - Résumé technique
- **[Content Creation Guide](CONTENT_CREATION_GUIDE.md)** - Créer du contenu pédagogique

---

## 🏗️ Architecture

### Backend (FastAPI)
- **API REST** : Authentification, contenu, sessions
- **WebSocket** : Communication temps réel
- **Services IA** : LLM (DeepSeek), STT (Google), TTS (Google)
- **Base de données** : PostgreSQL (async SQLAlchemy)
- **Cache** : Redis

### Frontend (React + Vite)
- **UI moderne** : Tailwind CSS
- **State management** : Zustand
- **Routing** : React Router
- **Real-time** : WebSocket client

### Database
- **PostgreSQL** : Données structurées
- **JSONB** : Contenu flexible (leçons, exercices)
- **Relations** : Students, Sessions, Exercises, Spaced Repetition

---

## 📁 Structure du Projet

```
ai-tutor-bac/
├── backend/
│   ├── app/
│   │   ├── api/              # Routes REST
│   │   ├── models/           # ORM SQLAlchemy
│   │   ├── schemas/          # Pydantic models
│   │   ├── services/         # LLM, STT, TTS
│   │   ├── websockets/       # Real-time session
│   │   └── utils/            # Security, helpers
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # UI components
│   │   ├── pages/            # Routes
│   │   ├── services/         # API, WebSocket
│   │   └── stores/           # Zustand state
│   └── public/media/         # Images, simulations
├── database/
│   ├── schema.sql            # PostgreSQL schema
│   ├── seed.py               # Data seeding
│   └── seed_data/            # JSON content
└── docker-compose.yml
```

---

## 🎯 Matières Disponibles

### Physique
- ✅ Ondes mécaniques progressives (Ch.1)
- 🔄 Ondes périodiques (Ch.2)
- 🔄 Ondes lumineuses (Ch.3)
- 🔄 Électricité (Ch.4-6)
- 🔄 Mécanique (Ch.7-9)

### Chimie
- 🔄 Cinétique chimique (Ch.1)
- 🔄 Équilibres chimiques (Ch.2)
- 🔄 Électrochimie (Ch.3-4)

### SVT
- 🔄 Génétique (Ch.1)
- 🔄 Immunologie (Ch.2)
- 🔄 Géologie (Ch.3)

**Légende** : ✅ Complet | 🔄 En cours

---

## 🔑 Configuration

### Variables d'environnement

Créer `backend/.env` :

```env
# Database
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/ai_tutor_bac

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=votre-cle-secrete-production

# DeepSeek API
DEEPSEEK_API_KEY=sk-votre-cle-deepseek

# Google Cloud (optionnel)
GOOGLE_APPLICATION_CREDENTIALS=/app/credentials/service-account.json

# App
CORS_ORIGINS=http://localhost:5173
```

### Obtenir les clés API

**DeepSeek (LLM)** - REQUIS
- Créer un compte : https://platform.deepseek.com/
- Obtenir une clé API
- Coût : ~$0.14 / 1M tokens (très abordable)

**Google Cloud (STT/TTS)** - OPTIONNEL
- Créer un projet : https://console.cloud.google.com/
- Activer Speech-to-Text et Text-to-Speech APIs
- Créer service account et télécharger JSON

**Alternative gratuite** : Whisper (STT) + Coqui TTS (local)

---

## 🎨 Créer du Contenu

### Ajouter une leçon

1. Créer `database/seed_data/lessons/phys_ch2_l1.json`
2. Suivre le template dans `CONTENT_CREATION_GUIDE.md`
3. Ajouter les exercices dans `database/seed_data/exercises/`
4. Créer les médias dans `frontend/public/media/`
5. Relancer `python database/seed.py`

### Ajouter des médias

**Images** :
```
frontend/public/media/images/physics/ch2_ondes_periodiques/
├── longueur_onde.png
├── diffraction.svg
└── interference.gif
```

**Simulations** :
```
frontend/public/media/simulations/physics/
└── onde_periodique.html
```

**Voir** : `CONTENT_CREATION_GUIDE.md` pour les détails

---

## 🧪 Tests

### Backend
```powershell
cd backend
pytest
```

### Frontend
```powershell
cd frontend
npm test
```

### Test manuel
1. Créer un compte étudiant
2. Démarrer une session
3. Tester la conversation audio/texte
4. Vérifier l'affichage des médias
5. Faire des exercices

---

## 🚀 Déploiement

### Production

**Backend** :
- Déployer sur Railway, Render, ou VPS
- Configurer PostgreSQL et Redis
- Définir les variables d'environnement

**Frontend** :
- Build : `npm run build`
- Déployer sur Vercel, Netlify, ou Cloudflare Pages

**Voir** : Documentation de déploiement (à venir)

---

## 🤝 Contribution

### Ajouter du contenu pédagogique
1. Créer des leçons (voir `CONTENT_CREATION_GUIDE.md`)
2. Créer des exercices
3. Créer des médias visuels
4. Soumettre via pull request

### Améliorer le code
1. Fork le projet
2. Créer une branche (`git checkout -b feature/amelioration`)
3. Commit (`git commit -m 'Ajout fonctionnalité X'`)
4. Push (`git push origin feature/amelioration`)
5. Créer une Pull Request

---

## 📝 Licence

Ce projet est sous licence MIT. Voir `LICENSE` pour plus de détails.

---

## 🙏 Remerciements

- **DeepSeek** : LLM puissant et abordable
- **Google Cloud** : Services STT/TTS
- **PhET** : Simulations scientifiques open-source
- **FastAPI** : Framework backend moderne
- **React** : Bibliothèque UI performante

---

## 📞 Support

- **Documentation** : Voir les fichiers `.md` à la racine
- **Issues** : Créer une issue sur GitHub
- **Email** : support@ai-tutor-bac.com (à configurer)

---

## 🎯 Roadmap

### Version 1.0 (Actuel)
- ✅ Conversation audio/texte
- ✅ Médias visuels
- ✅ Contrôle intelligent
- ✅ 5 phases pédagogiques
- ✅ 1 leçon complète (Physique Ch.1)

### Version 1.1 (Prochain)
- [ ] 10+ leçons complètes
- [ ] Tests diagnostiques
- [ ] Recommandation de cours
- [ ] Statistiques avancées

### Version 2.0 (Futur)
- [ ] Mode hors-ligne
- [ ] Application mobile
- [ ] Gamification
- [ ] Collaboration entre étudiants

---

**Développé avec ❤️ pour les étudiants du Baccalauréat Marocain**

**Bonne chance pour vos études ! 🎓**
