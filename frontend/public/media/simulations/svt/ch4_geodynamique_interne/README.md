# Laboratoire avancé de géodynamique interne

Simulation plein écran destinée au chapitre 4 de SVT, 2e Bac PC BIOF.

## Variantes

- `chains` : ordonner océanisation, subduction, obduction et collision.
- `deformations` : modifier contrainte, comportement et raccourcissement pour obtenir pli, faille inverse et nappe.
- `metamorphism` : manipuler P et T et enregistrer schiste bleu, éclogite, gneiss et cornéenne.
- `granitization` : classer les indices du granite d'anatexie et du granite intrusif.

La variante initiale peut être choisie par l'URL :

```text
index.html?variant=metamorphism
```

## État envoyé au tuteur

Chaque message `simulation_state` expose notamment :

- `student_actions`, `current_variant`, `simulation_status` ;
- `student_answer`, `expected_answer`, `attempts`, `hints_used` ;
- `deformation_parameters`, `deformation_tests` ;
- `pt_conditions`, `metamorphic_records` ;
- `granite_assignments`, `observed_hotspots`, `completed_variants` ;
- `objective_progress`.

## Commandes LLM

`start`, `set_variant`, `reset`, `place_stage`, `set_deformation_parameters`,
`run_deformation_test`, `set_pt`, `record_pt`, `assign_granite_evidence`,
`check`, `reveal_hint`, `highlight`.

Le manifeste fournit `command_schema` et `state_schema`. Toute commande entrante
utilise le message `simulation_control` et l'identifiant
`svt_internal_geodynamics_advanced_lab`.
