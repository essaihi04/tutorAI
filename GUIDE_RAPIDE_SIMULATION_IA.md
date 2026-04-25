# Guide Rapide - Créer une Simulation Pilotée par IA

## En 5 étapes

### 1. Copier le template
```bash
cp frontend/public/media/simulations/TEMPLATE_SIMULATION.html \
   frontend/public/media/simulations/votre_matiere/votre_simulation.html
```

### 2. Configurer l'identifiant unique
```javascript
const SIMULATION_CONFIG = {
  id: 'votre_simulation_id',  // Ex: 'forces_mouvement', 'circuit_electrique'
  objectives: ['Objectif 1', 'Objectif 2']
};
```

### 3. Implémenter votre simulation
- Créez votre interface HTML/CSS
- Implémentez votre logique de simulation
- Appelez `recordAction('nom_action')` à chaque action de l'étudiant
- Mettez à jour `simulationState.currentState` avec vos variables

### 4. Ajouter le contexte IA dans le backend
Dans `backend/app/websockets/session_handler.py`, méthode `_build_simulation_context`:

```python
elif simulation_id == 'votre_simulation_id':
    return f"""SIMULATION ACTIVE: Votre Simulation
Actions: {', '.join(actions)}
Progression: {int(progress * 100)}%
État: {state}

INSTRUCTIONS PÉDAGOGIQUES:
- Guide l'étudiant vers l'objectif
- Pose des questions sur les observations
- Encourage l'expérimentation"""
```

### 5. Tester
1. Démarrez le backend et frontend
2. Lancez une session avec votre leçon
3. L'IA guidera automatiquement l'étudiant avec voix

## Commandes IA disponibles

L'IA peut envoyer ces commandes à votre simulation:

| Commande | Usage |
|----------|-------|
| `start` | Démarrer automatiquement |
| `reset` | Réinitialiser |
| `set_parameter` | Modifier un paramètre |
| `highlight_element` | Mettre en évidence |
| `show_hint` | Afficher un indice |

## Exemple complet - Circuit électrique

```javascript
// Configuration
const SIMULATION_CONFIG = {
  id: 'circuit_electrique',
  objectives: ['Comprendre la loi d\'Ohm']
};

// État
let simulationState = {
  id: 'circuit_electrique',
  actions: [],
  currentState: {
    voltage: 0,
    resistance: 0,
    current: 0
  },
  progress: 0
};

// Action étudiant
function setVoltage(value) {
  simulationState.currentState.voltage = value;
  simulationState.currentState.current = value / simulationState.currentState.resistance;
  recordAction(`set_voltage_${value}V`);
  updateDisplay();
}

// Commande IA
function executeAICommand(command, params) {
  switch(command) {
    case 'set_parameter':
      if (params.name === 'voltage') setVoltage(params.value);
      break;
  }
}
```

## Communication automatique

✅ **Simulation → IA** : Automatique à chaque `recordAction()`
- L'IA reçoit l'état et génère un guidage vocal adapté

✅ **IA → Simulation** : Automatique via WebSocket
- L'IA peut piloter la simulation directement

## Bonnes pratiques

1. **Appelez `recordAction()` à chaque action significative**
2. **Calculez `progress` basé sur les objectifs pédagogiques**
3. **Mettez à jour `currentState` avec toutes les variables importantes**
4. **Implémentez les commandes génériques (`start`, `reset`, etc.)**
5. **Testez la communication bidirectionnelle**

## Ressources

- 📄 Protocole complet: `SIMULATION_AI_CONTROL_PROTOCOL.md`
- 📝 Template: `frontend/public/media/simulations/TEMPLATE_SIMULATION.html`
- 🔬 Exemple: `frontend/public/media/simulations/svt/.../respiration/simulation.html`
