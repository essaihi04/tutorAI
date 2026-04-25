# Protocole de Contrôle IA pour Toutes les Simulations

## Architecture

```
Backend (SessionHandler) ↔ WebSocket ↔ Frontend (LearningSession) ↔ postMessage ↔ Simulation (iframe)
```

## 1. Simulation → IA (Remontée d'état)

```javascript
window.parent.postMessage({
  type: 'simulation_state',
  simulation_id: 'YOUR_SIMULATION_ID',  // Unique pour chaque simulation
  student_actions: ['action1', 'action2'],
  current_state: { /* état actuel */ },
  objective_progress: 0.5,  // 0.0 à 1.0
  timestamp: Date.now()
}, '*');
```

## 2. IA → Simulation (Commandes)

```javascript
{
  type: 'simulation_control',
  simulation_id: 'YOUR_SIMULATION_ID',
  command: 'start' | 'reset' | 'set_parameter' | 'highlight_element',
  parameters: { /* params */ },
  guidance_text: "Texte optionnel"
}
```

## 3. Template Simulation (à copier dans chaque simulation HTML)

```javascript
let simState = {
  id: 'YOUR_SIMULATION_ID',
  actions: [],
  state: {},
  progress: 0
};

function sendToAI() {
  window.parent.postMessage({
    type: 'simulation_state',
    simulation_id: simState.id,
    student_actions: simState.actions,
    current_state: simState.state,
    objective_progress: simState.progress,
    timestamp: Date.now()
  }, '*');
}

window.addEventListener('message', (e) => {
  if (e.data.type === 'simulation_control' && e.data.simulation_id === simState.id) {
    executeCommand(e.data.command, e.data.parameters);
  }
});

function executeCommand(cmd, params) {
  switch(cmd) {
    case 'start': startSim(); break;
    case 'reset': resetSim(); break;
    case 'set_parameter': setParam(params.name, params.value); break;
  }
}
```

## 4. Backend - Ajouter contexte pour nouvelle simulation

Dans `session_handler.py`, méthode `_build_simulation_context`:

```python
def _build_simulation_context(self, simulation_id, state, actions, progress):
    if simulation_id == 'respiration_cellulaire':
        return f"SIMULATION Respiration: O2={state.get('oxygen_present')}, ATP={state.get('atp_produced')}..."
    
    elif simulation_id == 'NOUVELLE_SIMULATION':
        return f"SIMULATION Nouvelle: état={state}. GUIDE l'étudiant..."
    
    else:
        return f"SIMULATION {simulation_id}: {state}. GUIDE socratiquement."
```

## 5. Checklist nouvelle simulation

- [ ] Choisir `simulation_id` unique
- [ ] Copier template JavaScript
- [ ] Appeler `sendToAI()` à chaque action clé
- [ ] Calculer `objective_progress`
- [ ] Implémenter `executeCommand()`
- [ ] Ajouter contexte dans backend `_build_simulation_context()`
- [ ] Tester communication bidirectionnelle
