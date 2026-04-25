# Prompt pour Créer des Simulations Interactives avec IA

## Contexte
Tu es un développeur expert en simulations pédagogiques interactives. Tu dois créer une simulation HTML standalone qui communique avec une IA tuteur via postMessage.

## Architecture Requise

### Communication bidirectionnelle
- La simulation envoie son état à l'IA via `window.parent.postMessage()`
- L'IA peut envoyer des instructions via `window.addEventListener('message')`

### Protocole de données
Chaque action de l'étudiant doit envoyer:
```javascript
window.parent.postMessage({
  type: 'simulation_state',
  simulation_id: 'nom_unique_simulation',
  student_actions: ['action1', 'action2', ...],
  current_state: {
    // État actuel de la simulation
  },
  objective_progress: 0.0-1.0,  // Progression vers objectif pédagogique
  timestamp: Date.now()
}, '*');
```

## Template de Prompt

---

**Crée une simulation interactive HTML standalone pour [SUJET].**

### Objectif pédagogique
[Décrire l'objectif d'apprentissage]

### Contenu de la simulation
- **Titre:** [Titre de la simulation]
- **Concept:** [Concept scientifique à illustrer]
- **Variables manipulables:** [Liste des paramètres que l'étudiant peut modifier]
- **Résultats observables:** [Ce que l'étudiant doit observer/mesurer]

### Spécifications techniques

#### 1. Design responsive
- Mobile-first (min-width: 320px)
- Adaptatif jusqu'à desktop (max-width: 1200px)
- Utiliser flexbox/grid CSS
- Police lisible (min 14px sur mobile)
- Boutons tactiles (min 44x44px)

#### 2. Interface utilisateur
- Titre clair et descriptif
- Instructions concises
- Contrôles intuitifs (boutons, sliders, inputs)
- Zone d'affichage résultats bien visible
- Feedback visuel immédiat sur actions

#### 3. Style moderne
- Palette de couleurs cohérente
- Dégradés subtils
- Ombres et bordures arrondies
- Transitions fluides (0.3s)
- États hover/active pour interactivité

#### 4. Communication avec IA

##### Variables à tracker
```javascript
let studentActions = [];  // Historique actions
let currentState = {};    // État actuel simulation
```

##### Fonction d'envoi état
```javascript
function sendStateToAI(state) {
  window.parent.postMessage({
    type: 'simulation_state',
    simulation_id: '[ID_UNIQUE]',
    student_actions: studentActions,
    current_state: state,
    objective_progress: calculateProgress(),
    timestamp: Date.now()
  }, '*');
}
```

##### Calcul progression
```javascript
function calculateProgress() {
  // Retourner 0.0 à 1.0 selon critères:
  // - Toutes les conditions testées?
  // - Résultats observés?
  // - Comparaisons effectuées?
  return progress;
}
```

##### Réception instructions IA (optionnel)
```javascript
window.addEventListener('message', (event) => {
  if (event.data.type === 'ai_instruction') {
    // Réagir aux instructions IA
    // Ex: mettre en surbrillance un élément
  }
});
```

#### 5. Actions à tracker

Pour chaque action utilisateur:
1. Ajouter nom action à `studentActions`
2. Mettre à jour `currentState`
3. Appeler `sendStateToAI(currentState)`
4. Afficher résultat visuellement

Exemples d'actions:
- `clicked_[element]`
- `changed_[parameter]_to_[value]`
- `observed_[result]`
- `compared_[condition1]_vs_[condition2]`

#### 6. État de la simulation

L'objet `current_state` doit contenir:
- Valeurs de tous les paramètres
- Résultats calculés/affichés
- Étapes complétées
- Données observées

Exemple:
```javascript
{
  parameter1: value1,
  parameter2: value2,
  result_calculated: true,
  result_value: 42,
  steps_completed: ['step1', 'step2']
}
```

### Structure HTML requise

```html
<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Titre Simulation]</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      background: linear-gradient(135deg, [couleur1], [couleur2]);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 1rem;
    }
    .container {
      background: white;
      border-radius: 20px;
      padding: 2rem;
      max-width: 800px;
      width: 100%;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    h1 {
      color: #333;
      margin-bottom: 1rem;
      font-size: clamp(1.5rem, 4vw, 2rem);
    }
    .controls {
      display: flex;
      gap: 1rem;
      margin: 1.5rem 0;
      flex-wrap: wrap;
    }
    button {
      flex: 1;
      min-width: 140px;
      padding: 1rem;
      font-size: 1rem;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      transition: all 0.3s;
      font-weight: 600;
    }
    button:hover {
      transform: translateY(-2px);
    }
    .result {
      background: #f3f4f6;
      padding: 1.5rem;
      border-radius: 12px;
      margin-top: 1.5rem;
      min-height: 200px;
    }
    @media (max-width: 640px) {
      .container { padding: 1rem; }
      .controls { flex-direction: column; }
      button { min-width: 100%; }
    }
  </style>
</head>
<body>
  <div class="container">
    <h1>🔬 [Titre]</h1>
    <p>[Description courte]</p>
    
    <div class="controls">
      <!-- Contrôles interactifs -->
    </div>
    
    <div class="result" id="result">
      <!-- Résultats affichés ici -->
    </div>
  </div>

  <script>
    let studentActions = [];
    let currentState = {};
    
    function onAction(actionName, newState) {
      studentActions.push(actionName);
      currentState = newState;
      displayResult(newState);
      sendStateToAI(newState);
    }
    
    function displayResult(state) {
      // Afficher résultats visuellement
    }
    
    function sendStateToAI(state) {
      window.parent.postMessage({
        type: 'simulation_state',
        simulation_id: '[ID_UNIQUE]',
        student_actions: studentActions,
        current_state: state,
        objective_progress: calculateProgress(),
        timestamp: Date.now()
      }, '*');
      console.log('[Simulation] État envoyé:', state);
    }
    
    function calculateProgress() {
      // Logique progression 0.0 → 1.0
      return 0.0;
    }
  </script>
</body>
</html>
```

### Critères de qualité

✅ **Fonctionnel**
- Simulation fonctionne standalone
- Tous les calculs sont corrects
- Pas d'erreurs console

✅ **Pédagogique**
- Objectif d'apprentissage clair
- Manipulation intuitive
- Résultats faciles à interpréter
- Encourage exploration

✅ **Technique**
- Code propre et commenté
- Variables bien nommées
- Responsive sur tous écrans
- Communication IA fonctionnelle

✅ **UX/UI**
- Design moderne et attrayant
- Feedback visuel immédiat
- Instructions claires
- Accessibilité (contraste, tailles)

### Livrables attendus

1. **Fichier HTML complet** (standalone, pas de dépendances externes)
2. **ID unique** pour la simulation
3. **Liste des actions trackées** avec leurs noms
4. **Structure de l'objet state** documentée
5. **Logique de calcul progression** expliquée

---

## Exemples de Prompts Spécifiques

### Exemple 1: Photosynthèse

```
Crée une simulation interactive HTML standalone pour la PHOTOSYNTHÈSE.

Objectif pédagogique:
Comprendre l'impact de la lumière, du CO2 et de l'eau sur la production de glucose et d'O2.

Contenu:
- Titre: Simulation Photosynthèse
- Concept: Équation 6CO2 + 6H2O + lumière → C6H12O6 + 6O2
- Variables manipulables:
  * Intensité lumineuse (0-100%)
  * Concentration CO2 (faible/moyenne/élevée)
  * Disponibilité eau (faible/moyenne/élevée)
- Résultats observables:
  * Quantité glucose produit
  * Quantité O2 libéré
  * Vitesse de réaction

Actions à tracker:
- changed_light_to_[value]
- changed_co2_to_[level]
- changed_water_to_[level]
- observed_glucose_[amount]
- observed_oxygen_[amount]
- compared_conditions

État simulation:
{
  light_intensity: 0-100,
  co2_level: 'low'|'medium'|'high',
  water_level: 'low'|'medium'|'high',
  glucose_produced: number,
  oxygen_produced: number,
  reaction_rate: number,
  conditions_tested: []
}

Progression:
- 0.33: Au moins une condition testée
- 0.66: Deux conditions différentes testées
- 1.0: Trois conditions testées et comparées

ID simulation: 'photosynthese'

[Suivre toutes les spécifications techniques du template ci-dessus]
```

### Exemple 2: Cycle de Krebs

```
Crée une simulation interactive HTML standalone pour le CYCLE DE KREBS.

Objectif pédagogique:
Visualiser les étapes du cycle de Krebs et comprendre la production d'ATP, NADH et FADH2.

Contenu:
- Titre: Cycle de Krebs - Production d'énergie
- Concept: Oxydation complète de l'acétyl-CoA
- Variables manipulables:
  * Démarrer/arrêter le cycle
  * Vitesse du cycle (lent/normal/rapide)
  * Présence d'inhibiteurs (oui/non)
- Résultats observables:
  * Molécules produites à chaque étape
  * Bilan énergétique total
  * Temps par cycle

Actions à tracker:
- started_cycle
- changed_speed_to_[speed]
- added_inhibitor
- removed_inhibitor
- observed_step_[number]
- completed_full_cycle
- observed_atp_production
- observed_nadh_production
- observed_fadh2_production

État simulation:
{
  cycle_running: boolean,
  speed: 'slow'|'normal'|'fast',
  inhibitor_present: boolean,
  current_step: 1-8,
  cycles_completed: number,
  atp_produced: number,
  nadh_produced: number,
  fadh2_produced: number
}

Progression:
- 0.25: Cycle démarré
- 0.50: Un cycle complet observé
- 0.75: Testé avec inhibiteur
- 1.0: Comparé avec/sans inhibiteur

ID simulation: 'cycle_krebs'

[Suivre toutes les spécifications techniques du template ci-dessus]
```

### Exemple 3: Mitose

```
Crée une simulation interactive HTML standalone pour la MITOSE.

Objectif pédagogique:
Identifier et comprendre les différentes phases de la mitose et leurs caractéristiques.

Contenu:
- Titre: Simulation Mitose Cellulaire
- Concept: Division cellulaire en 5 phases (Interphase, Prophase, Métaphase, Anaphase, Télophase)
- Variables manipulables:
  * Avancer phase par phase
  * Lecture automatique (play/pause)
  * Vitesse animation
  * Zoom sur chromosomes
- Résultats observables:
  * Position chromosomes
  * État chromatine
  * Formation fuseau mitotique
  * Nombre cellules finales

Actions à tracker:
- started_simulation
- advanced_to_[phase]
- toggled_autoplay
- changed_speed_to_[speed]
- zoomed_on_chromosomes
- observed_chromosome_condensation
- observed_spindle_formation
- observed_chromosome_separation
- completed_mitosis

État simulation:
{
  current_phase: 'interphase'|'prophase'|'metaphase'|'anaphase'|'telophase',
  autoplay: boolean,
  speed: 'slow'|'normal'|'fast',
  zoom_active: boolean,
  phases_observed: [],
  mitosis_completed: boolean
}

Progression:
- 0.20: Chaque phase observée (×5)
- 1.0: Toutes les phases observées + mitose complétée

ID simulation: 'mitose'

[Suivre toutes les spécifications techniques du template ci-dessus]
```

## Checklist avant livraison

- [ ] Simulation fonctionne en standalone (ouvrir HTML dans navigateur)
- [ ] Responsive testé (mobile 320px → desktop 1200px)
- [ ] Tous les boutons/contrôles fonctionnent
- [ ] `sendStateToAI()` appelé à chaque action
- [ ] `calculateProgress()` retourne valeurs cohérentes 0.0-1.0
- [ ] Console logs montrent états envoyés
- [ ] Design moderne et professionnel
- [ ] Instructions claires pour l'étudiant
- [ ] Pas d'erreurs JavaScript
- [ ] Code commenté et lisible
