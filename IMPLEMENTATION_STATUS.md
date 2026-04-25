# Implémentation Mode Coaching & Libre - État d'avancement

## ✅ TERMINÉ

### Backend
- [x] **Migrations SQL** (2 fichiers dans `backend/migrations/`)
  - `001_create_coaching_tables.sql` - Tables study_plans, study_plan_sessions, diagnostic_results
  - `002_create_libre_mode_tables.sql` - Tables libre_conversations, libre_messages
  - ⚠️ **À APPLIQUER MANUELLEMENT** via Dashboard Supabase (voir `migrations/README.md`)

- [x] **Services Backend**
  - `study_plan_service.py` - Génération de plans d'étude personnalisés
  - `diagnostic_service.py` - Quiz diagnostiques avec LLM

- [x] **Endpoints REST**
  - `coaching.py` - 8 endpoints (diagnostic, plan, progress, countdown)
  - `libre.py` - 4 endpoints (start, history, conversation, end)
  - Enregistrés dans `api.py`

### Frontend
- [x] **Store Zustand**
  - `coachingStore.ts` - État global pour mode coaching

- [x] **API Services**
  - Fonctions ajoutées dans `api.ts` pour coaching et libre

---

## 🚧 EN COURS / À FAIRE

### 1. Appliquer les migrations Supabase
```bash
# Via Dashboard Supabase → SQL Editor
# Exécuter 001_create_coaching_tables.sql
# Puis 002_create_libre_mode_tables.sql
```

### 2. Frontend - Pages à créer

#### DiagnosticQuiz.tsx
- Quiz interactif par matière
- Affichage des questions QCM
- Soumission et affichage des résultats
- Bouton "Générer mon programme"

#### StudyPlan.tsx
- Vue calendrier du plan d'étude
- Liste des sessions avec statut
- Barres de progression par matière
- Bouton pour démarrer une session

#### Dashboard.tsx (redesign)
- Deux cartes : Mode Coaching / Mode Libre
- Compte à rebours BAC
- Barre de progression globale
- Programme du jour
- Stats par matière

#### LibreSession.tsx
- Interface chat libre
- Pas de contrainte de chapitre
- Détection automatique du sujet par l'IA
- Affichage intelligent (schéma/image/simulation)

### 3. Routes à ajouter dans App.tsx
```tsx
/coaching/diagnostic
/coaching/plan
/coaching/session/:sessionId
/libre
/libre/:conversationId
```

### 4. WebSocket - Modifications session_handler.py
- Ajouter champ `session_mode` ("coaching" ou "libre")
- Mode Coaching : suit le plan, phases structurées
- Mode Libre : pas de chapitre, réponses libres
- Sauvegarder messages dans `libre_messages`

### 5. LLM Prompts
- Créer prompt pour mode libre (général, toutes matières)
- Prompt pour génération de questions diagnostiques
- Prompt pour évaluations formatives

---

## 📋 ORDRE D'IMPLÉMENTATION RECOMMANDÉ

1. ✅ Appliquer migrations SQL
2. Créer DiagnosticQuiz.tsx
3. Créer StudyPlan.tsx
4. Redesigner Dashboard.tsx
5. Créer LibreSession.tsx
6. Modifier session_handler.py pour modes
7. Mettre à jour prompts LLM
8. Ajouter routes dans App.tsx
9. Tester l'intégration complète

---

## 🎯 FONCTIONNALITÉS CLÉS

### Mode Coaching
1. Quiz diagnostic rapide (6 QCM par matière)
2. Génération automatique du programme
3. Calcul jours restants jusqu'au BAC (4 juin 2026)
4. Allocation intelligente des heures (faibles = plus de temps)
5. Planning quotidien avec horaires
6. Suivi de progression en temps réel

### Mode Libre
1. Chat libre sans contrainte de chapitre
2. IA détecte le sujet automatiquement
3. Choix intelligent du format de réponse :
   - Schéma SVG pour processus
   - Image pour visuel
   - Simulation pour dynamique
   - Exercice pour pratique
   - Évaluation pour diagnostic
4. Historique des conversations

---

## 🔧 FICHIERS MODIFIÉS

### Backend
- `app/services/study_plan_service.py` (nouveau)
- `app/services/diagnostic_service.py` (nouveau)
- `app/api/v1/endpoints/coaching.py` (nouveau)
- `app/api/v1/endpoints/libre.py` (nouveau)
- `app/api/v1/api.py` (modifié)

### Frontend
- `src/stores/coachingStore.ts` (nouveau)
- `src/services/api.ts` (modifié)

### Migrations
- `backend/migrations/001_create_coaching_tables.sql` (nouveau)
- `backend/migrations/002_create_libre_mode_tables.sql` (nouveau)
- `backend/migrations/README.md` (nouveau)

---

## ⚠️ NOTES IMPORTANTES

1. **Migrations** : DOIVENT être appliquées avant de tester le backend
2. **Date BAC** : Hardcodée au 4 juin 2026 dans `study_plan_service.py`
3. **LLM** : Les questions diagnostiques sont générées par DeepSeek
4. **Horaires** : 2h/jour en semaine, 3h/jour weekend
5. **Progression** : Calculée automatiquement (sessions complétées / total)
