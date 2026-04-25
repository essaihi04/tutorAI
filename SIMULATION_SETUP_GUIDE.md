# Guide de Configuration - Simulation Interactive avec IA

## Ce qui a été créé

### 1. Nouvelle simulation responsive
**Fichier:** `frontend/public/media/simulations/svt/ch1_consommation_matiere_organique/respiration/simulation.html`

**Caractéristiques:**
- ✅ Design responsive (mobile → desktop)
- ✅ Communication bidirectionnelle via postMessage
- ✅ Envoie l'état à chaque action
- ✅ Calcule progression objectif pédagogique
- ✅ Interface moderne et intuitive

### 2. Frontend modifié
**Fichiers:**
- `frontend/src/components/session/MediaViewer.tsx`
- `frontend/src/pages/LearningSession.tsx`

**Ajouts:**
- Écoute des messages postMessage de l'iframe
- Transmission au backend via WebSocket
- Handler `onSimulationUpdate`

### 3. Backend enrichi
**Fichier:** `backend/app/websockets/session_handler.py`

**Nouvelles méthodes:**
- `_handle_simulation_update()` - Reçoit états simulation
- `_generate_simulation_guidance()` - Génère guidage IA
- `_build_simulation_context()` - Construit contexte pour IA
- `_should_provide_guidance()` - Décide quand guider

**Nouvelles propriétés:**
- `simulation_state` - État actuel
- `simulation_history` - Historique actions

## Comment ça marche

### Flux complet

```
1. Étudiant clique "Avec O2" dans simulation
   ↓
2. Simulation envoie postMessage au parent
   {
     type: 'simulation_state',
     simulation_id: 'respiration_cellulaire',
     student_actions: ['clicked_with_o2'],
     current_state: { oxygen_present: true, atp_produced: 36 },
     objective_progress: 0.5
   }
   ↓
3. MediaViewer capte le message
   ↓
4. LearningSession transmet via WebSocket
   ↓
5. Backend reçoit et analyse
   ↓
6. IA génère guidage contextuel
   "Excellent! Tu as observé 36 ATP avec O2. 
    Maintenant teste sans O2 pour comparer."
   ↓
7. Frontend affiche réponse IA + audio
```

### Guidage IA intelligent

L'IA intervient quand:
- ✅ Première action (encourage exploration)
- ✅ Objectif atteint (félicite et consolide)
- ✅ Toutes les 3 actions (maintient engagement)

L'IA pose des questions sur:
- Résultats observés (combien d'ATP?)
- Comparaisons (différence avec/sans O2?)
- Liens théoriques (rôle mitochondrie?)

## Configuration requise

### 1. Mettre à jour l'URL en base de données

```sql
UPDATE lesson_resources
SET file_path = '/media/simulations/svt/ch1_consommation_matiere_organique/respiration/simulation.html'
WHERE title = 'Simulation respiration cellulaire'
  AND resource_type = 'simulation';
```

### 2. Redémarrer le backend

```bash
cd backend
python -m uvicorn app.main:app --reload
```

### 3. Tester

1. Démarrer session sur leçon "Libération de l'énergie"
2. Demander: "une simulation de la respiration"
3. Cliquer "Avec O2" dans la simulation
4. Observer réponse IA contextuelle
5. Cliquer "Sans O2"
6. Observer guidage comparatif de l'IA

## Créer d'autres simulations

### Template de base

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Ma Simulation</title>
  <style>
    /* Responsive CSS */
  </style>
</head>
<body>
  <div class="container">
    <!-- Interface simulation -->
  </div>

  <script>
    let studentActions = [];
    
    function onStudentAction(actionName) {
      studentActions.push(actionName);
      
      const state = {
        // État actuel simulation
      };
      
      sendStateToAI(state);
    }
    
    function sendStateToAI(state) {
      window.parent.postMessage({
        type: 'simulation_state',
        simulation_id: 'ma_simulation',
        student_actions: studentActions,
        current_state: state,
        objective_progress: calculateProgress(),
        timestamp: Date.now()
      }, '*');
    }
    
    function calculateProgress() {
      // Logique progression 0.0 → 1.0
      return 0.5;
    }
  </script>
</body>
</html>
```

### Ajouter contexte IA pour nouvelle simulation

Dans `session_handler.py`, méthode `_build_simulation_context()`:

```python
if simulation_id == 'ma_simulation':
    context = f"""SIMULATION ACTIVE: Ma Simulation
Actions: {', '.join(actions)}
État: {state}

GUIDE L'ÉTUDIANT:
- Objectif pédagogique
- Questions à poser
- Liens théoriques
"""
    return context
```

## Avantages de cette architecture

### Pour l'étudiant
- ✅ Simulation responsive sur tous écrans
- ✅ Guidage IA personnalisé en temps réel
- ✅ Questions ciblées sur ses actions
- ✅ Feedback immédiat

### Pour l'IA
- ✅ Comprend exactement ce que fait l'étudiant
- ✅ Peut poser questions sur résultats observés
- ✅ Guide vers objectif pédagogique
- ✅ Détecte blocages et incompréhensions

### Pour le développeur
- ✅ Architecture extensible
- ✅ Protocole simple (postMessage)
- ✅ Facile d'ajouter nouvelles simulations
- ✅ Logs détaillés pour debug

## Prochaines étapes recommandées

1. **Tester la simulation actuelle**
   - Vérifier flux complet
   - Observer guidage IA
   - Ajuster seuils intervention

2. **Créer plus de simulations**
   - Glycolyse
   - Photosynthèse
   - Cycle de Krebs
   - Mitose/Méiose

3. **Enrichir contexte IA**
   - Ajouter détection erreurs communes
   - Personnaliser selon profil étudiant
   - Adapter difficulté questions

4. **Analytics**
   - Tracker temps par simulation
   - Identifier étapes difficiles
   - Mesurer efficacité pédagogique
