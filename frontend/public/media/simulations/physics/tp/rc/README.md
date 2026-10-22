# TP — Charge et décharge d’un condensateur (dipôle RC)

Laboratoire local sans dépendance externe, 2e BAC PC BIOF, domaine Électricité. Il fonctionne comme un TP guidé : l’élève fait chaque geste et saisit chaque résultat, le labo vérifie.

## Déroulé

1. **Prédire** : si R double, que devient τ ? La réponse n’est pas notée. Elle est confrontée à la mesure à l’étape 5.
2. **Monter** : choisir E (2 à 12 V), R (100 Ω à 10 kΩ) et C (10 à 1 000 µF), puis basculer K en position 1.
3. **Mesurer** : relever u_C à la main, ou lancer l’acquisition automatique. Il faut au moins 8 points, jusqu’à 3τ.
4. **Lire τ** de deux façons, par la méthode des 63 % et par la tangente à l’origine. Les outils sous la courbe : tracer la courbe modélisée, la ligne 0,63 E, la tangente, et un curseur de lecture au clic.
5. **Calculer C** = τ / R, puis l’écart avec la valeur nominale, et confronter la prédiction.
6. **Décharge** : basculer K en position 2, puis lire τ à 37 % de U₀. L’énergie ½·C·U₀² est affichée à la fin.

## Modèle

Solutions exactes de RC·du/dt + u = E et RC·du/dt + u = 0, sans intégration pas à pas. Le générateur est idéal et le condensateur sans fuite. Les lectures sont arrondies à 0,01 V, avec un bruit de ±0,01 V reproductible. Le temps est ralenti pour que 5τ durent 8 s à l’écran.

La graduation et l’intervalle d’acquisition sont des pas « ronds » (1, 2 ou 5 × 10ⁿ), indépendants de τ : graduer en multiples de τ donnerait la réponse.

Tolérance de 5 % sur τ et sur C. Messages ciblés pour les pièges : millisecondes au lieu de secondes, farads au lieu de µF, 63 % confondu avec 37 %.

## Intégration tuteur

Identifiant : `physics_rc_tp_lab`. Même contrat que les labos de `physics/advanced` :
- le labo émet `simulation_manifest` et `simulation_state` ;
- il n’accepte `simulation_control` que depuis la fenêtre parente ;
- il pose `__SIMULATION_MANIFEST_SENT__`.

Commandes : `start`, `set_parameters` (`emf_v`, `resistance_ohm`, `capacitance_uf`), `set_switch` (`position` 1 ou 2), `record_measurement`, `auto_acquire`, `pause`, `run_until` (`time_s`), `show_model`, `show_63`, `show_tangent`, `read_at` (`time_s`), `check` (`field`, `answer`), `go_to_step`, `reveal_hint`, `reset`.

Changer le montage efface les mesures, qui ne décrivent plus ce circuit, et ramène à l’étape « Monter ». Les boutons portent `data-professor-control` pour le professeur animé.

## Vérification

`node --test frontend/tests/rc-tp-model.test.mjs` depuis la racine.
