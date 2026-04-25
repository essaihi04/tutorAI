# Guide de débogage audio - Gemini TTS

## Corrections appliquées

### 1. Frontend - Envoi de `lesson_id`
**Fichier**: `frontend/src/pages/LearningSession.tsx`

**Avant:**
```typescript
wsService.sendJson({
  type: 'init_session',
  subject: 'SVT',
  chapter_title: '',
  lesson_title: lesson.title_fr,
  // ... pas de lesson_id
});
```

**Après:**
```typescript
wsService.sendJson({
  type: 'init_session',
  lesson_id: lesson.id,  // ← AJOUTÉ
  subject: 'SVT',
  chapter_title: '',
  lesson_title: lesson.title_fr,
  // ...
});
```

### 2. Backend - Logs de débogage ajoutés

**Fichier**: `backend/app/websockets/session_handler.py`

**Logs ajoutés:**
```python
print(f"[Session Init] lesson_id received: {lesson_id}")
print(f"[Session Init] Generating opening message for phase: {self.current_phase}")
print(f"[Session Init] Opening message generated: {opening[:50]}...")
print(f"[TTS Opening] Starting audio synthesis for language: {self._speech_language()}")
print(f"[TTS Opening] Audio generated successfully, sending to frontend")
print(f"[TTS Opening] Audio sent to frontend")
```

**Fichier**: `backend/app/services/tts_service.py`

**Logs ajoutés:**
```python
print(f"[Gemini TTS] synthesize() called with {len(text)} chars, lang={language}")
print(f"[Gemini TTS] API key present: {self.api_key[:20]}...")
print(f"[Gemini TTS] Cache miss - synthesizing {len(text)} chars, lang={language}, voice={self.voice}")
```

## Logs attendus maintenant

### Backend (terminal uvicorn)

**Au démarrage de session:**
```
[Session Init] lesson_id received: abc-123-def-456
[Resources] Loaded 9 resources for lesson abc-123-def-456
[Session Init] Generating opening message for phase: activation
[Session Init] Opening message generated: Bonjour ! Bienvenue dans cette leçon sur la con...
[TTS Opening] Starting audio synthesis for language: fr
[Gemini TTS] synthesize() called with 87 chars, lang=fr
[Gemini TTS] API key present: AIzaSyAHnoDj3VGQUxKb...
[Gemini TTS] Cache miss - synthesizing 87 chars, lang=fr, voice=Puck
[Gemini TTS] Synthesizing 87 chars, lang=fr, voice=Puck
[TTS Opening] Audio generated successfully, sending to frontend
[TTS Opening] Audio sent to frontend
```

**Si erreur:**
```
[TTS Opening] ERROR: HTTPStatusError: 429 Too Many Requests
Traceback (most recent call last):
  ...
```

### Frontend (console navigateur F12)

**Au démarrage:**
```
[WebSocket] Connected
[Session] Initialized
```

**Réception audio:**
```
[Audio] Received audio_response
[Audio] Playing audio...
```

**Si erreur:**
```
[TTS Error] Gemini TTS failed: ...
```

## Étapes de test

### 1. Redémarre le backend
```bash
cd backend
uvicorn app.main:app --reload
```

**Vérifie dans les logs de démarrage:**
- Pas d'erreur d'import
- Serveur démarre sur `http://127.0.0.1:8000`

### 2. Redémarre le frontend
```bash
cd frontend
npm run dev
```

**Vérifie:**
- Serveur démarre sur `http://localhost:5173`
- Pas d'erreur de compilation

### 3. Lance une session

1. Va sur `http://localhost:5173/dashboard`
2. Clique sur **SVT > Chapitre 1**
3. Clique **Commencer**

### 4. Observe les logs backend

**Tu devrais voir:**
```
[Session Init] lesson_id received: <uuid>
[Resources] Loaded X resources for lesson <uuid>
[Session Init] Generating opening message...
[TTS Opening] Starting audio synthesis...
[Gemini TTS] synthesize() called...
[Gemini TTS] API key present: AIzaSyAHnoDj3VGQUxKb...
```

### 5. Observe la console navigateur (F12)

**Tu devrais voir:**
- Message de l'agent s'affiche
- Pas d'erreur TTS
- Audio joue automatiquement

## Si tu ne vois AUCUN log

### Problème 1: Backend ne démarre pas
**Vérifier:**
```bash
cd backend
python -m uvicorn app.main:app --reload
```

**Si erreur d'import:**
- Vérifier que tous les fichiers modifiés sont sauvegardés
- Vérifier qu'il n'y a pas d'erreur de syntaxe

### Problème 2: WebSocket ne se connecte pas
**Console navigateur:**
```
Failed to connect to WebSocket
```

**Solution:**
- Vérifier que le backend tourne sur `http://127.0.0.1:8000`
- Vérifier le proxy Vite dans `vite.config.ts`

### Problème 3: Session ne s'initialise pas
**Backend logs:**
```
# Rien ne s'affiche
```

**Solution:**
- Vérifier que le message `init_session` est bien envoyé
- Ouvrir console navigateur et vérifier les erreurs WebSocket

## Si tu vois les logs mais pas d'audio

### Cas 1: Logs backend OK, mais erreur TTS
```
[TTS Opening] ERROR: RuntimeError: GEMINI_API_KEY is missing
```

**Solution:**
```bash
# Vérifier .env
cat backend/.env | grep GEMINI_API_KEY

# Devrait afficher:
GEMINI_API_KEY=AIzaSyAHnoDj3VGQUxKb5HFLguSiPyyiOesm8AQ
```

**Si vide:**
- Ajouter la clé dans `backend/.env`
- Redémarrer le backend

### Cas 2: Logs backend OK, erreur 429
```
[TTS Opening] ERROR: HTTPStatusError: 429 Too Many Requests
```

**Solution:**
- Attendre 1-2 minutes
- Réessayer
- Le retry automatique va réessayer 3 fois

### Cas 3: Audio généré mais pas joué
```
[TTS Opening] Audio sent to frontend
# Mais pas de son
```

**Console navigateur:**
```
[Audio] Received audio_response
# Mais pas de playback
```

**Solution:**
- Vérifier que l'audio n'est pas muté dans le navigateur
- Vérifier les permissions audio du navigateur
- Essayer de cliquer sur la page (certains navigateurs bloquent l'autoplay)

## Commande de test rapide

### Test direct de l'API Gemini
```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key=AIzaSyAHnoDj3VGQUxKb5HFLguSiPyyiOesm8AQ" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Bonjour test"}]
    }],
    "generationConfig": {
      "responseModalities": ["AUDIO"],
      "speechConfig": {
        "voiceConfig": {
          "prebuiltVoiceConfig": {
            "voiceName": "Puck"
          }
        }
      }
    }
  }'
```

**Réponse attendue:**
```json
{
  "candidates": [{
    "content": {
      "parts": [{
        "inlineData": {
          "mimeType": "audio/wav",
          "data": "UklGRi..."
        }
      }]
    }
  }]
}
```

**Si erreur 400:**
- Clé API invalide
- Vérifier la clé sur Google Cloud Console

**Si erreur 429:**
- Quota dépassé
- Attendre quelques minutes

## Résumé des fichiers modifiés

1. ✅ `frontend/src/pages/LearningSession.tsx` - Ajout de `lesson_id`
2. ✅ `backend/app/websockets/session_handler.py` - Logs de débogage
3. ✅ `backend/app/services/tts_service.py` - Logs de débogage

## Prochaines étapes

1. **Redémarre backend et frontend**
2. **Lance une session**
3. **Regarde les logs backend**
4. **Envoie-moi les logs exacts** si ça ne marche toujours pas

## Ce que je dois voir

**Si tout fonctionne:**
```
Backend:
[Session Init] lesson_id received: ...
[TTS Opening] Audio sent to frontend

Frontend:
Message de l'agent affiché
Audio joue automatiquement
```

**Si ça ne marche pas:**
```
Envoie-moi:
1. Les logs backend complets (depuis le démarrage)
2. La console navigateur (F12 > Console)
3. Le message d'erreur exact
```
