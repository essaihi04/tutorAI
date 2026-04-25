# Resource Decision Logic

## Choix architectural
Le système utilise un **moteur de décision hybride** et non un agent libre.

Ordre de priorité:
- demande explicite de l'élève
- phase pédagogique
- type de concept
- niveau de l'élève
- ressources disponibles
- historique récent des modes affichés

## Modes possibles
- `whiteboard`
- `image`
- `simulation`
- `video`
- `exercise`
- `evaluation`
- `exam`

## Règles principales

### Demande explicite
- `simulation` si l'élève demande une simulation
- `image` si l'élève demande une image, photo, illustration ou schéma
- `whiteboard` si l'élève demande de dessiner ou d'expliquer au tableau
- `exercise` si l'élève demande un exercice
- `evaluation` si l'élève demande un test, quiz ou QCM

### Phase pédagogique
- `activation` favorise `image`
- `exploration` favorise `simulation`
- `explanation` favorise `whiteboard`
- `application` favorise `exercise`
- `consolidation` favorise `evaluation`

### Type de concept
- concept dynamique -> `simulation`
- concept structurel -> `image`
- concept comparatif -> `whiteboard`
- concept causal -> `whiteboard`

### Adaptation au profil
- débutant: bonus à `image` et `whiteboard`
- avancé: bonus à `simulation` et `exercise`

### Anti-répétition
Le moteur applique une pénalité au dernier mode utilisé pour éviter les répétitions inutiles.

## Intégration backend
- service: `backend/app/services/resource_decision_service.py`
- orchestration: `backend/app/websockets/session_handler.py`

## Sortie typique
```json
{
  "primary_mode": "simulation",
  "resource_type_for_suggestion": "simulation",
  "explicit_media_request": true,
  "should_prepare_whiteboard": false,
  "auto_present_resource": true,
  "reason_code": "explicit_request"
}
```

## Comportement attendu
- une modalité principale par moment
- pas de superposition confuse entre tableau blanc et média
- support de fallback selon les ressources réellement disponibles
