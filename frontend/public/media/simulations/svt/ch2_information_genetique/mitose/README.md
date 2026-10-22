# TP — La mitose dans la racine d’oignon

Laboratoire local sans dépendance externe, 2e BAC PC BIOF, SVT, domaine 2 : information génétique.

## Déroulé

1. **Préparer la lame** : remettre le protocole dans l’ordre (prélever, fixer, hydrolyser, rincer, colorer, écraser). Une étape placée trop tôt est refusée, avec la raison (par exemple : sans hydrolyse, les cellules ne s’étalent pas).
2. **Observer** : objectif ×10, puis ×40, et mise au point jusqu’à une image nette. À ×40, on peut déplacer la lame.
3. **Identifier** cinq cellules numérotées, une par phase. Chaque confusion classique a son indice (métaphase / anaphase, télophase / interphase…).
4. **Calculer**, à partir du comptage du champ (48 cellules) et d’un cycle de 20 h : l’indice mitotique, puis la durée de la métaphase.
5. **Interpréter** la quantité d’ADN au cours du cycle (q → 2q en phase S, retour à q après la mitose). La courbe s’affiche quand la réponse est juste.

## Modèle

Le champ est reproductible (graine 7) : 34 interphases, 6 prophases, 3 métaphases, 2 anaphases et 3 télophases, soit IM ≈ 29 %. Ce sont des proportions réalistes pour un méristème de racine.

Les cellules sont dessinées selon leur phase :
- interphase : chromatine diffuse et nucléole ;
- prophase : filaments ;
- métaphase : fuseau et plaque équatoriale ;
- anaphase : deux lots en V ;
- télophase : deux noyaux et paroi en formation.

Pièges détectés : fraction au lieu de pourcentage, division par les cellules en interphase au lieu du total, heures au lieu de minutes, dénominateur réduit aux cellules en division.

## Intégration tuteur

Identifiant : `svt_mitosis_tp_lab`. Même contrat que les autres labos : `simulation_manifest` / `simulation_state` émis, `simulation_control` accepté seulement depuis la fenêtre parente, `__SIMULATION_MANIFEST_SENT__` posé.

Commandes : `start`, `protocol_add` (`step_id`), `protocol_undo`, `set_objective` (10 ou 40), `set_focus` (`value` 0..1), `pan` (`dx`, `dy`), `center_on` (`cell` 1..5), `check` (`field` identify, index, duration ou dna ; `answer` ; `cell`), `go_to_step`, `reveal_hint`, `reset`.

## Vérification

`node --test frontend/tests/mitosis-tp-model.test.mjs` depuis la racine.
