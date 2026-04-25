# Architecture Simulation Interactive avec IA

## Problèmes à résoudre
1. Simulation non responsive
2. IA ne peut pas comprendre/manipuler la simulation
3. Pas de guidage pédagogique basé sur les actions de l'étudiant

## Solution proposée

### 1. Communication bidirectionnelle

```
Simulation (iframe) <--postMessage--> Frontend <--WebSocket--> Backend <--> IA
```

### 2. Protocole de données

**Simulation → Frontend:**
```javascript
window.parent.postMessage({
  type: 'simulation_state',
  simulation_id: 'respiration_cellulaire',
  student_actions: ['clicked_with_o2', 'observed_mitochondria'],
  current_state: {
    oxygen_present: true,
    atp_produced: 36,
    location: 'mitochondrie',
    steps_completed: ['glycolyse', 'krebs']
  },
  objective_progress: 0.75,
  timestamp: Date.now()
}, '*');
```

**Frontend → Backend (WebSocket):**
```json
{
  "type": "simulation_update",
  "simulation_id": "respiration_cellulaire",
  "state": {...},
  "student_actions": [...]
}
```

### 3. Modifications nécessaires

#### A. Simulation HTML (responsive + communication)
- Utiliser CSS flexbox/grid responsive
- Envoyer état via postMessage à chaque action
- Recevoir instructions de l'IA via postMessage

#### B. Frontend MediaViewer
- Écouter messages de l'iframe
- Transmettre au backend via WebSocket
- Afficher guidage IA en overlay

#### C. Backend session_handler
- Nouveau handler `simulation_update`
- Enrichir contexte IA avec état simulation
- Générer questions basées sur actions

#### D. Prompt IA
- Ajouter section "SIMULATION INTERACTIVE"
- Instructions pour analyser état
- Générer questions ciblées

### 4. Exemple de flux pédagogique

**Étudiant clique "Avec O2"**
→ Simulation envoie état
→ IA analyse: "L'étudiant a activé O2"
→ IA pose: "Combien d'ATP sont produits avec O2? Regarde le résultat."

**Étudiant observe 36 ATP**
→ Simulation envoie: student_observed_atp: 36
→ IA: "Excellent! Maintenant essaie sans O2 pour comparer."

**Étudiant clique "Sans O2"**
→ IA: "Combien d'ATP maintenant? Quelle est la différence?"

### 5. Implémentation prioritaire

1. Créer nouvelle simulation responsive avec postMessage
2. Modifier MediaViewer pour écouter messages
3. Ajouter handler backend simulation_update
4. Enrichir prompt IA avec contexte simulation
5. Tester flux complet

### 6. Format simulation recommandé

- Canvas/SVG pour visualisation
- Boutons/sliders pour manipulation
- Affichage temps réel des résultats
- Responsive: min-width 320px, max-width 100%
- Communication: postMessage après chaque action
