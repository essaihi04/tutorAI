# Configuration Audio - Gemini TTS Uniquement

## Statut actuel

✅ **Gemini TTS activé** avec la voix **Puck**
❌ **Fallback navigateur désactivé** (uniquement Gemini)

## Configuration backend

### Fichier: `backend/.env`

```env
GEMINI_API_KEY=AIzaSyAHnoDj3VGQUxKb5HFLguSiPyyiOesm8AQ
```

### Fichier: `backend/app/config.py`

```python
gemini_api_key: str = ""
gemini_tts_model: str = "gemini-2.5-flash-preview-tts"
gemini_tts_voice: str = "Puck"
```

### Fichier: `backend/app/services/tts_service.py`

- **Modèle**: `gemini-2.5-flash-preview-tts`
- **Voix**: `Puck`
- **Timeout**: 20 secondes
- **Cache**: activé
- **Chunking**: 150 caractères par chunk
- **Retry**: 3 tentatives avec backoff progressif (2s, 5s, 10s)

## Configuration frontend

### Fichier: `frontend/src/pages/LearningSession.tsx`

**Modifications effectuées:**
- ❌ Fallback navigateur **désactivé**
- ✅ Uniquement Gemini TTS
- ✅ Gestion des chunks audio
- ✅ Playback séquentiel

**Handler `tts_error`:**
```typescript
wsService.on('tts_error', (data) => {
  setProcessing(false);
  const errorMsg = data?.message || 'Gemini TTS error';
  
  // NO FALLBACK - Only Gemini TTS (voice Puck)
  setTtsErrorMessage(`⚠️ Erreur audio Gemini: ${errorMsg}`);
  
  console.error('[TTS Error]', errorMsg);
  revealPendingMedia();
});
```

## Flux audio complet

### 1. Backend génère l'audio

```python
# session_handler.py
chunks = await tts_service.synthesize_chunks_parallel(
    text=ai_response,
    language=self._speech_language(),
)
```

### 2. Backend envoie les chunks

```python
for chunk_index, audio_base64, mime_type in chunks:
    await self.websocket.send_json({
        "type": "audio_chunk",
        "chunk_index": chunk_index,
        "total_chunks": len(chunks),
        "audio": audio_base64,
        "format": mime_type,
        "is_last": chunk_index == len(chunks) - 1
    })
```

### 3. Frontend reçoit et joue

```typescript
// Stocke les chunks
audioChunksRef.current.push({
  index: data.chunk_index,
  audio: data.audio,
  format: data.format
});

// Joue quand tous les chunks sont reçus
if (audioChunksRef.current.length === data.total_chunks) {
  playAudioChunks();
}
```

## Vérifications à faire

### 1. Clé API Gemini valide

```bash
# Vérifier que la clé est bien dans .env
cat backend/.env | grep GEMINI_API_KEY
```

**Clé actuelle**: `AIzaSyAHnoDj3VGQUxKb5HFLguSiPyyiOesm8AQ`

### 2. Backend démarre sans erreur

```bash
cd backend
uvicorn app.main:app --reload
```

**Vérifier dans les logs:**
```
[Gemini TTS] Synthesizing 45 chars, lang=fr, voice=Puck
```

### 3. Frontend reçoit l'audio

**Console navigateur (F12):**
```
[Audio Chunk] Received chunk 1/3
[Audio Chunk] Received chunk 2/3
[Audio Chunk] Received chunk 3/3
[Audio Chunk] All 3 chunks received, starting playback
[Audio Chunk] Playing chunk 1/3
[Audio Chunk] Playing chunk 2/3
[Audio Chunk] Playing chunk 3/3
```

## Erreurs possibles

### Erreur 1: "GEMINI_API_KEY is missing"

**Cause**: Clé API non chargée

**Solution**:
1. Vérifier `backend/.env`
2. Redémarrer le backend
3. Vérifier que le fichier `.env` est à la racine de `backend/`

### Erreur 2: "429 Too Many Requests"

**Cause**: Quota Gemini API dépassé

**Solution**:
1. Attendre quelques minutes
2. Vérifier le quota sur Google Cloud Console
3. Le retry automatique va réessayer 3 fois

### Erreur 3: Pas d'audio mais pas d'erreur

**Cause**: Chunks non reçus ou playback bloqué

**Solution**:
1. Ouvrir console navigateur (F12)
2. Vérifier les logs `[Audio Chunk]`
3. Vérifier que `total_chunks` correspond au nombre de chunks reçus

### Erreur 4: Audio coupé après premier chunk

**Cause**: Playback séquentiel cassé

**Solution**:
1. Vérifier `isPlayingChunksRef.current`
2. Vérifier que `playAudioChunks()` joue tous les chunks
3. Vérifier les logs `Playing chunk X/Y`

## Test manuel

### 1. Lance une session

```
1. Va sur /dashboard
2. Choisis SVT > Chapitre 1
3. Clique "Commencer"
```

### 2. Parle ou écris

```
"Bonjour"
```

### 3. Vérifie l'audio

**Attendu:**
- ✅ Texte de l'agent s'affiche
- ✅ Audio Gemini (voix Puck) joue automatiquement
- ✅ Pas de fallback navigateur
- ✅ Lecture fluide et complète

**Si erreur:**
- ❌ Message d'erreur affiché
- ❌ Pas d'audio navigateur (désactivé)
- ❌ Logs dans console

## Commandes utiles

### Backend logs

```bash
# Voir les logs TTS
cd backend
uvicorn app.main:app --reload --log-level debug
```

### Frontend logs

```javascript
// Console navigateur (F12)
// Filtrer par "TTS" ou "Audio"
```

### Tester l'API Gemini directement

```bash
curl -X POST \
  "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-tts:generateContent?key=AIzaSyAHnoDj3VGQUxKb5HFLguSiPyyiOesm8AQ" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [{
      "parts": [{"text": "Bonjour, test audio"}]
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

## Statut final

✅ **Gemini TTS activé**
✅ **Voix Puck configurée**
✅ **Fallback navigateur désactivé**
✅ **Chunking activé pour rapidité**
✅ **Retry automatique sur erreurs**
✅ **Cache activé**

🎯 **Prêt à utiliser** - L'audio devrait maintenant fonctionner uniquement avec Gemini TTS (voix Puck).

## Si l'audio ne fonctionne toujours pas

Envoie-moi:
1. **Logs backend** (terminal où tourne uvicorn)
2. **Console navigateur** (F12 > Console)
3. **Message d'erreur exact** si affiché
