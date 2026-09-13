# Document 11 — vésicule à pH réglables

Le lecteur utilise `svt_ch1_vesicules_atp_synthase` et conserve l'introduction
animée aux étapes 0–3. À partir de l'étape 4, une seule expérience reste à
l'écran. Les anciennes étapes 4/5/6 sélectionnent 6/4, 7/7 et 6/9 ; 7/8
restent compatibles avec le cas 6/9. La lecture automatique ne fait plus
défiler les expériences après la préparation.

Deux curseurs règlent `pHi` et `pHe` entre 4 et 10, par pas de 0,5. Les trois
boutons sont des raccourcis. Le résultat est recalculé immédiatement ; le
mouvement illustratif dure 3,6 secondes et peut être rejoué ou mis en pause.
La réinitialisation rétablit 7/7, sans imposer de revoir la préparation.

## Modèle scientifique

Modèle qualitatif du document scolaire : `ΔpH = pHe − pHi` et
`[H+]i/[H+]e = 10^ΔpH`. Le sens favorisé est sortant si ΔpH > 0,
entrant si ΔpH < 0 et nul si ΔpH = 0. Dans ce modèle, le gradient sortant
permet la synthèse, avec membrane et ATP synthase intactes et ADP/Pi
disponibles dehors. Les têtes des sphères pédonculées sont à l'extérieur.

Ne pas interpréter cette règle qualitative comme un seuil thermodynamique
universel : les rendements, vitesses, concentrations absolues, l'épuisement
du gradient et le potentiel électrique Δψ ne sont pas simulés. Les pH sont
maintenus pendant l'observation, et les points H+ sont symboliques.
La synthèse réelle dépend aussi du potentiel électrique et de l'énergie de
phosphorylation : voir l'étude primaire
[Kinetic Equivalence of Transmembrane pH and Electrical Potential Differences in ATP Synthesis](https://pmc.ncbi.nlm.nih.gov/articles/PMC3308813/).

## Contrôle du tuteur

La scène React reprend le cycle et les états du modèle de simulation HTML,
mais conserve le pont natif `scientific_control` / `onStateChange` du lecteur
au lieu d'ajouter une iframe et un second protocole de messages.

- Variantes : `scene`, `acide_externe`, `equilibre`, `acide_interne`, `personnalisee`.
- `set_parameters` accepte uniquement des nombres finis `pHi` / `pHe` ; une
  modification partielle conserve l'autre pH. Cette commande n'est autorisée
  que pour ce preset.
- `set_variant` et `highlight` acceptent aussi ces paramètres. `start`,
  `pause`, `reset`, `next`, `previous` sont conservés.
- À l'ouverture, `scientific.parameters` accepte les mêmes pH.
- L'état remonte les pH, ΔpH, direction, synthèse qualitative et variantes
  terminées. Le serveur recalcule le résultat à partir des pH et ne laisse
  pas le client ou le tuteur imposer un résultat arbitraire.

## Vérifications

Depuis `frontend` : `node --test scripts/vesicle-experiment.test.mjs`.
Depuis `backend` : `python -m pytest app/tests/test_vesicle_experiment.py -q`.
Le modèle est testé sur les 169 paires de pH, les commandes, les limites,
les transitions, les resets et la progression sans doublons.
