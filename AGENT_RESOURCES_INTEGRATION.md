# Intégration Agent - Ressources Pédagogiques

## Modifications effectuées

### `backend/app/websockets/session_handler.py`

#### Nouvelles propriétés
- `self.lesson_resources` : cache des ressources de la leçon
- `self.current_lesson_id` : ID de la leçon en cours

#### Nouvelles méthodes

**`_load_lesson_resources(lesson_id)`**
- Charge toutes les ressources depuis `lesson_resources` table
- Appelée automatiquement lors de l'initialisation de session si `lesson_id` fourni
- Stocke les ressources en cache pour accès rapide

**`_find_best_resource(concepts, resource_type, phase)`**
- Trouve la meilleure ressource selon :
  - **Concepts** : score basé sur le nombre de concepts correspondants
  - **Type** : image, video, simulation, exam, etc.
  - **Phase** : activation, exploration, explanation, application, consolidation
- Retourne la ressource avec le meilleur score

**`_auto_suggest_resource(student_input, ai_response)`**
- Détecte automatiquement les concepts mentionnés dans la conversation
- Identifie si l'élève est confus (mots-clés : "comprends pas", "aide", "difficile", etc.)
- Si confusion détectée :
  1. Cherche d'abord une **image**
  2. Sinon une **simulation**
  3. Sinon n'importe quelle ressource pertinente
- Affiche automatiquement la ressource trouvée

**`_display_resource(resource)`**
- Affiche la ressource au frontend via WebSocket
- Gère les types :
  - `image` → `show_media` avec type image
  - `video` → `show_media` avec type video
  - `simulation` → `show_media` avec type simulation
  - `exam` → `show_exam` avec URL et métadonnées

#### Modifications de méthodes existantes

**`_init_session(message)`**
- Appelle `_load_lesson_resources()` si `lesson_id` fourni
- Charge toutes les ressources au démarrage de la session

**`_process_student_input(student_input)`**
- Appelle `_auto_suggest_resource()` après chaque réponse de l'agent
- Suggestion automatique basée sur le contexte de la conversation

## Comment ça fonctionne

### Flux automatique

1. **Démarrage de session**
   - Frontend envoie `init_session` avec `lesson_id`
   - Backend charge toutes les ressources de la leçon
   - Ressources mises en cache dans `self.lesson_resources`

2. **Pendant la conversation**
   - Élève : "Je ne comprends pas la glycolyse"
   - Agent détecte :
     - Concept : `glycolyse`
     - Confusion : `comprends pas`
   - Agent cherche la meilleure ressource :
     - Type : `image` (priorité pour confusion)
     - Concepts : `['glycolyse']`
     - Phase : `explanation`
   - Trouve : "Schéma de la glycolyse"
   - Affiche automatiquement l'image

3. **Affichage**
   - WebSocket envoie `show_media` au frontend
   - Frontend affiche l'image dans `MediaViewer`
   - Élève voit le schéma instantanément

### Critères de sélection

**Score de pertinence**
- +1 point par concept correspondant
- Ressource avec le meilleur score est choisie

**Filtres**
1. **Phase** : ressources de la phase actuelle prioritaires
2. **Type** : si confusion → images/simulations prioritaires
3. **Concepts** : correspondance exacte ou partielle

**Fallback**
- Si aucun concept ne correspond → première ressource de la phase
- Si aucune ressource de la phase → première ressource disponible

## Exemples concrets

### Exemple 1 : Élève confus sur la glycolyse

**Conversation**
```
Élève: "C'est quoi la glycolyse ?"
Agent: "La glycolyse est la première étape..."
```

**Détection**
- Concepts : `['glycolyse']`
- Confusion : `c'est quoi`

**Sélection**
- Type prioritaire : `image`
- Ressource trouvée : "Schéma de la glycolyse"
- Concepts : `['glycolyse', 'ATP', 'cytoplasme']`
- Score : 1 (1 concept correspondant)

**Résultat**
- Image affichée automatiquement
- URL : `/media/images/svt/ch1_.../schema_glycolyse.svg`

### Exemple 2 : Élève demande de l'aide sur la respiration

**Conversation**
```
Élève: "Je ne comprends pas comment fonctionne la respiration cellulaire"
Agent: "La respiration cellulaire se déroule dans la mitochondrie..."
```

**Détection**
- Concepts : `['respiration', 'mitochondrie']`
- Confusion : `comprends pas`

**Sélection**
1. Cherche image avec `respiration` → trouvé
2. Ressource : "Cycle de Krebs et chaîne respiratoire"
3. Score : 1

**Résultat**
- Image affichée
- Si pas d'image → cherche simulation
- Si simulation trouvée → affichée à la place

### Exemple 3 : Élève veut s'entraîner

**Conversation**
```
Élève: "Je veux m'entraîner sur la fermentation"
Agent: "Très bien, voici un exercice..."
```

**Détection**
- Concepts : `['fermentation']`
- Pas de confusion détectée

**Résultat**
- Aucune ressource affichée automatiquement
- L'agent peut utiliser la commande `EXERCICE:id` manuellement

## Configuration requise

### Frontend

Le message `init_session` doit inclure `lesson_id` :

```typescript
websocket.send(JSON.stringify({
  type: 'init_session',
  lesson_id: 'uuid-de-la-lecon',
  subject: 'SVT',
  chapter_title: 'Consommation de la matière organique',
  lesson_title: 'Libération de l\'énergie',
  phase: 'explanation',
  language: 'fr'
}));
```

### Base de données

La table `lesson_resources` doit contenir :
- `lesson_id` : UUID de la leçon
- `resource_type` : type de ressource
- `title` : titre
- `description` : description
- `file_path` : chemin du fichier
- `phase` : phase pédagogique
- `concepts` : array de concepts
- `difficulty_tier` : niveau

## Logs de débogage

Le backend affiche :
```
[Resources] Loaded 9 resources for lesson abc-123
[Resources] Displayed image: Schéma de la glycolyse
```

## Prochaines améliorations possibles

1. **Enrichir le prompt système** avec la liste des ressources disponibles
2. **Permettre à l'agent** de choisir explicitement une ressource via commande
3. **Ajouter un historique** des ressources déjà affichées pour éviter les répétitions
4. **Scorer aussi par difficulté** selon le niveau de l'élève
5. **Détecter les demandes explicites** : "montre-moi une image", "lance une simulation"

## Test manuel

1. Ajoute des ressources via l'interface admin
2. Lance une session avec `lesson_id`
3. Dis "Je ne comprends pas [concept]"
4. Vérifie que la ressource s'affiche automatiquement

## Statut

✅ **Implémenté**
- Chargement automatique des ressources
- Sélection intelligente par concepts/phase/type
- Suggestion automatique en cas de confusion
- Affichage automatique des ressources

⏳ **À tester**
- Flux complet avec données réelles
- Performance avec beaucoup de ressources
- Pertinence de la sélection automatique
