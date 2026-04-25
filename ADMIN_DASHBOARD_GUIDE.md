# 🛡️ Admin Dashboard - Guide Complet

## 📋 Vue d'ensemble

Le dashboard admin est une interface complète pour gérer la plateforme AI Tutor BAC. Il permet de:
- **Gérer les utilisateurs** (créer, modifier, désactiver, réinitialiser mots de passe)
- **Suivre la consommation des tokens** (DeepSeek, Mistral OCR, Gemini)
- **Monitorer les utilisateurs en ligne** en temps réel
- **Analyser les coûts** par jour, par utilisateur, par provider

---

## 🚀 Accès au Dashboard

### URL
```
http://localhost:5173/admin
```

### Mot de passe par défaut
```
admin123
```

⚠️ **IMPORTANT**: Changez ce mot de passe en production via la variable d'environnement `ADMIN_PASSWORD` dans `.env`

---

## 📊 Fonctionnalités

### 1. **Vue d'ensemble** (Overview)
- **Statistiques globales**:
  - Nombre total d'utilisateurs
  - Utilisateurs actifs
  - Utilisateurs en ligne (temps réel)
  - Coût aujourd'hui (requêtes + tokens)
  - Coût ce mois
  - Coût total (all-time)

- **Activité du jour**:
  - Requêtes API
  - Tokens utilisés
  - Coût en USD

- **Utilisateurs en ligne**:
  - Liste en temps réel des utilisateurs connectés
  - Indicateur vert animé

### 2. **Utilisateurs** (Users)
- **Liste complète** avec:
  - Nom complet, username, email
  - Statut (Actif/Inactif)
  - Rôle (Admin/Élève)
  - Indicateur en ligne
  - Date d'inscription

- **Actions disponibles**:
  - ➕ **Créer un compte**: Email, mot de passe, nom complet, username, rôle admin
  - 🔑 **Réinitialiser mot de passe**: Nouveau mot de passe pour un utilisateur
  - ✅/❌ **Activer/Désactiver**: Toggle le statut d'un utilisateur
  - 🗑️ **Supprimer**: Désactive l'utilisateur (soft delete)

- **Recherche**: Par nom, email ou username

### 3. **Consommation** (Usage)
- **Sélection de période**: 7, 14, 30, 90 jours

- **Statistiques globales**:
  - Coût total (USD)
  - Tokens totaux (prompt + completion)
  - Nombre de requêtes
  - Nombre de providers utilisés

- **Par fournisseur**:
  - DeepSeek (LLM principal)
  - Mistral OCR (extraction de texte)
  - Mistral Chat (vision)
  - Gemini (TTS)
  - Graphique de répartition des coûts

- **Coût par jour**:
  - Graphique en barres des 14 derniers jours
  - Nombre de requêtes par jour

- **Par utilisateur**:
  - Tableau détaillé avec:
    - Email de l'utilisateur
    - Nombre de requêtes
    - Tokens utilisés
    - Coût total en USD
    - Dernière requête
  - **Détails expandables**: Breakdown par provider pour chaque utilisateur

### 4. **Requêtes récentes** (Recent Requests)
- **100 dernières requêtes** avec:
  - Heure exacte
  - Utilisateur (email)
  - Provider (DeepSeek, Mistral, etc.)
  - Model utilisé
  - Endpoint appelé
  - Tokens (prompt + completion)
  - Coût en USD (6 décimales)
  - Durée de la requête (secondes)

---

## 🔧 Configuration Backend

### 1. Migration SQL
Exécutez la migration pour créer la table `token_usage`:
```bash
psql -U postgres -d ai_tutor_bac -f database/migrations/create_admin_token_usage.sql
```

Ou via Supabase SQL Editor:
```sql
-- Copiez le contenu de database/migrations/create_admin_token_usage.sql
```

### 2. Variables d'environnement (.env)
```bash
# Mot de passe admin (CHANGEZ EN PRODUCTION!)
ADMIN_PASSWORD=votre_mot_de_passe_securise

# Déjà configurées (vérifiez qu'elles existent)
DEEPSEEK_API_KEY=...
MISTRAL_API_KEY=...
GEMINI_API_KEY=...
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
```

### 3. Tracking automatique des tokens
Le tracking est **automatiquement intégré** dans:
- ✅ `llm_service.py` → `chat()` et `chat_stream()` (DeepSeek)
- ✅ `ocr_service.py` → Mistral OCR + DeepSeek correction

**Aucune modification nécessaire** dans les autres services — le tracking se fait en arrière-plan.

---

## 💰 Tarification (Pricing)

Les coûts sont calculés automatiquement selon les tarifs 2025:

| Provider | Model | Input ($/1M tokens) | Output ($/1M tokens) |
|----------|-------|---------------------|----------------------|
| DeepSeek | deepseek-chat | $0.14 | $0.28 |
| DeepSeek | deepseek-reasoner | $0.55 | $2.19 |
| Mistral | mistral-ocr-latest | $1.00 | $1.00 |
| Mistral | mistral-small-latest | $0.20 | $0.60 |
| Mistral | pixtral-large-latest | $2.00 | $6.00 |
| Gemini | gemini-2.5-flash-preview-tts | $0.15 | $0.60 |

**Mise à jour des prix**: Modifiez `backend/app/services/token_tracking_service.py` → `PRICING`

---

## 🔄 Auto-refresh

- **Activé par défaut**: Rafraîchit les données toutes les 30 secondes
- **Toggle**: Bouton en haut à droite (icône refresh bleue)
- **Refresh manuel**: Bouton à côté du toggle

---

## 🎨 Interface

### Design
- **Dark mode** pour la page de login
- **Light mode** pour le dashboard principal
- **Indicateurs en temps réel**: Points verts animés pour les utilisateurs en ligne
- **Graphiques**: Barres de progression, charts par jour
- **Responsive**: Fonctionne sur mobile, tablette, desktop

### Navigation
- **4 onglets** en haut: Overview, Users, Usage, Requests
- **Header sticky**: Reste visible en scrollant
- **Modals**: Pour créer utilisateur et reset password

---

## 🔐 Sécurité

### Authentification
- **JWT token** séparé pour l'admin (différent des tokens étudiants)
- **Expiration**: 24 heures
- **Stockage**: `localStorage.admin_token`
- **Déconnexion**: Bouton en haut à droite

### Permissions
- **Aucun accès étudiant**: Les étudiants ne peuvent pas accéder au dashboard admin
- **RLS Supabase**: La table `token_usage` utilise Row Level Security (service role only)
- **Admin flag**: Colonne `is_admin` dans la table `students`

### Best Practices
1. ⚠️ **Changez le mot de passe par défaut** en production
2. 🔒 **Utilisez HTTPS** en production
3. 🚫 **Ne partagez jamais** le mot de passe admin
4. 📊 **Surveillez les coûts** régulièrement
5. 🔄 **Sauvegardez** la base de données régulièrement

---

## 🐛 Dépannage

### Erreur 401 "Invalid admin token"
→ Le token a expiré ou est invalide. Déconnectez-vous et reconnectez-vous.

### Pas de données de consommation
→ Vérifiez que la migration SQL a été exécutée et que les appels LLM/OCR sont trackés.

### Utilisateurs en ligne = 0 (mais il y en a)
→ Vérifiez que le WebSocket fonctionne (`/ws/tutor/{token}`)

### Coûts = $0.00
→ Vérifiez que les clés API sont correctes et que les requêtes passent bien.

---

## 📝 Exemples d'utilisation

### Créer un compte élève
1. Allez dans l'onglet **Users**
2. Cliquez sur **Créer un compte**
3. Remplissez:
   - Nom complet: `Ahmed Benali`
   - Username: `ahmed_b`
   - Email: `ahmed@example.com`
   - Mot de passe: `password123`
   - Admin: ❌ (non coché)
4. Cliquez sur **Créer**

### Créer un compte admin
1. Même procédure, mais cochez **Compte administrateur** ✅

### Réinitialiser un mot de passe
1. Dans la liste des utilisateurs, cliquez sur l'icône 🔑
2. Entrez le nouveau mot de passe (min. 6 caractères)
3. Cliquez sur **Reset**

### Surveiller les coûts
1. Allez dans l'onglet **Consommation**
2. Sélectionnez la période (7, 14, 30, 90 jours)
3. Consultez:
   - Coût total en haut
   - Répartition par provider
   - Coût par jour (graphique)
   - Coût par utilisateur (tableau)

### Voir les requêtes en temps réel
1. Allez dans l'onglet **Requêtes récentes**
2. Consultez les 100 dernières requêtes
3. Cliquez sur **Refresh** pour mettre à jour

---

## 🚀 Prochaines étapes (optionnel)

### Améliorations possibles
- [ ] Export CSV/Excel des données de consommation
- [ ] Alertes email si coût > seuil
- [ ] Graphiques plus avancés (Chart.js, Recharts)
- [ ] Logs d'activité admin (qui a créé/modifié quoi)
- [ ] Quotas par utilisateur
- [ ] Statistiques de performance (temps de réponse moyen)
- [ ] Dashboard public (stats anonymisées)

---

## 📞 Support

Pour toute question ou problème:
1. Consultez ce guide
2. Vérifiez les logs backend: `backend/app/services/token_tracking_service.py`
3. Vérifiez la console navigateur (F12)
4. Vérifiez les tables Supabase: `token_usage`, `students`

---

**Bon monitoring! 🎉**
