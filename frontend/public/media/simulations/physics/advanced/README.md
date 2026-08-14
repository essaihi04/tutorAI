# Laboratoires avancés de Physique — 2e BAC PC BIOF

Ces quatre pages autonomes utilisent une scène de laboratoire photoréaliste, un modèle numérique, des mesures enregistrables et un contrat de contrôle pour le tuteur IA.

| Laboratoire | Variantes |
|---|---|
| WaveLab | `progressive`, `periodic`, `optics` |
| NucleoLab | `decay`, `transformations`, `mass_energy`, `spectra` |
| CircuitLab | `rc`, `rl`, `rlc`, `modulation` |
| MecaLab | `newton`, `fall`, `projectile`, `orbit`, `rotation`, `oscillator` |

## Protocole IA

Chaque laboratoire publie vers son parent :

- `simulation_manifest` : identifiant, variantes, commandes et schémas ;
- `simulation_state` : paramètres, valeurs calculées, mesures, actions, essais, indices et progression.

Commandes communes : `start`, `set_variant`, `set_parameters`, `run_model`, `record_measurement`, `check`, `reset`, `reveal_hint`, `highlight`.

Exemple :

```js
iframe.contentWindow.postMessage({
  type: "simulation_control",
  simulation_id: "physics_electricity_advanced_lab",
  command: "set_parameters",
  parameters: { resistance_ohm: 220, capacitance_uf: 100 }
}, "*");
```

Les pages acceptent aussi `?variant=<id>`. Elles sont conçues pour le viewport natif `100vh`, sans défilement global, sur ordinateur et mobile.
