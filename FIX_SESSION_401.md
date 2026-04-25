# 🔧 Correction Erreur 401 - Session Start

## 🔴 Problème

Erreur 401 Unauthorized lors de l'appel à `/api/v1/sessions/start`

## 🔍 Causes Possibles

1. **Token expiré ou invalide**
2. **Backend redémarré** (les tokens Supabase peuvent avoir changé)
3. **Token non envoyé** dans les headers

## ✅ Solutions

### Solution 1: Reconnectez-vous

Le plus simple:

1. **Déconnectez-vous** du Dashboard
2. **Reconnectez-vous** avec vos identifiants
3. Le nouveau token sera valide

### Solution 2: Vérifier le Token dans le Navigateur

1. Ouvrez **DevTools** (F12)
2. **Console** → Tapez:
   ```javascript
   localStorage.getItem('token')
   ```
3. Si `null` ou vide → Reconnectez-vous
4. Si présent → Le problème est ailleurs

### Solution 3: Vérifier que le Backend Fonctionne

Le backend doit être démarré sur **http://localhost:8000**

Vérifiez dans le terminal où vous avez lancé:
```bash
python -m uvicorn app.main:app --reload
```

Vous devriez voir:
```
INFO:     Application startup complete.
```

### Solution 4: Test Manuel de l'Endpoint

Utilisez le script de test:

```bash
cd backend
python test_session_start.py
```

Entrez vos identifiants et un lesson_id pour tester.

## 🎯 Correction Permanente

J'ai aussi corrigé le script SQL pour **retirer les niveaux de difficulté des chapitres**.

Les niveaux (beginner/intermediate/advanced) sont maintenant **uniquement pour les exercices**.

Le système adaptera le niveau selon les réponses de l'élève:
- ✅ Réponse correcte → Passe au niveau suivant
- ❌ Réponse incorrecte → Reste au même niveau ou descend

## 📝 Changements Effectués

### 1. SQL Script Corrigé
`database/insert_svt_content.sql` - Retiré `difficulty_level` des chapitres

**Avant:**
```sql
INSERT INTO chapters (..., difficulty_level, ...)
VALUES (..., 'intermediate', ...)
```

**Après:**
```sql
INSERT INTO chapters (..., estimated_hours, ...)
VALUES (..., 12.0, ...)
```

### 2. Les Niveaux Restent pour les Exercices

Les exercices gardent leur `difficulty_tier`:
- 🟢 `beginner` - Exercices simples
- 🟡 `intermediate` - Exercices moyens  
- 🔴 `advanced` - Exercices difficiles

L'IA proposera des exercices selon le niveau actuel de l'élève.

## 🧪 Test Complet

1. **Reconnectez-vous** au Dashboard
2. **Cliquez sur une matière** (SVT par exemple)
3. **Cliquez sur un chapitre**
4. **Démarrez une session**
5. Ça devrait fonctionner ! ✅

## 💡 Si le Problème Persiste

Vérifiez dans DevTools → Network:
- L'appel à `/api/v1/sessions/start`
- Headers → Cherchez `Authorization: Bearer ...`
- Si absent → Le token n'est pas envoyé
- Si présent → Le token est invalide

**Solution:** Déconnexion/Reconnexion pour obtenir un nouveau token valide.

## 🔐 Note sur les Tokens

Les tokens JWT Supabase ont une durée de vie limitée (généralement 1 heure).

Si vous restez connecté longtemps sans activité, le token expire.

**Solution:** Implémentez un refresh token (à faire plus tard) ou reconnectez-vous.
