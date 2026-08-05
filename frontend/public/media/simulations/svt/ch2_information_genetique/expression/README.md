# Laboratoire avancé — expression génétique

Cette simulation respecte le contrat `TEMPLATE_SIMULATION.html` et tient dans
un viewport `100vh` sans défilement. L'application l'affiche à l'échelle native.

## Variantes pédagogiques

1. `transcription` : glisser/toucher cinq codons pour construire l'ARNm à
   partir du brin transcrit orienté 3′ → 5′.
2. `translation` : placer les acides aminés sous les codons de l'ARNm.
3. `mutations` : tester les codons GAG, GUA et UAA afin de comparer mutation
   silencieuse, faux-sens et non-sens.

## Données envoyées au tuteur IA

Chaque interaction envoie un message `simulation_state` contenant :

- `student_actions` : historique horodaté des manipulations ;
- `current_state.simulation_status` : `running` ou `finished` ;
- `current_state.student_answer` et `expected_answer` ;
- `current_state.errors`, `attempts` et `hints_used` ;
- `current_state.observations` : faits scientifiques observables ;
- `current_state.mutation_tests` et `protein_effect` ;
- `objective_progress` : variantes terminées / 3.

Le manifeste `simulation_manifest` expose aussi `SIMULATION_CONFIG`, les
objectifs, le schéma d'état et le schéma des commandes.

## Commandes acceptées depuis le tuteur IA

- `start`, `reset`, `set_variant`, `check` ;
- `place_codon { slot, codon }` ;
- `place_amino_acid { slot, amino_acid }` ;
- `set_mutation { codon }` ;
- `reveal_hint { level }`, `highlight { target }`, `set_speed { speed }`.

Le backend valide chaque commande contre `available_commands` avant de la
transmettre à l'iframe.
