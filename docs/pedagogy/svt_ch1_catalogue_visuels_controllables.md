# Catalogue visuel — SVT Ch. 1 « Consommation de la matière organique et flux d’énergie »

Ce catalogue évite de fabriquer un média pour chaque écran. Le tuteur réutilise
d’abord les schémas BAC validés ; il ouvre un laboratoire complet lorsque
l’élève doit mesurer ou tester une hypothèse ; il utilise une scène transparente
sur le tableau pour révéler, comparer ou piloter un processus pendant son
explication.

## Besoins du parcours et routage

| Activité | Besoin visuel | Support retenu | Identifiant |
|---:|---|---|---|
| 0 | Relier photosynthèse, glucose et consommation | Croquis simple + graphique ordinaire | tableau live |
| 1 | Poser le problème matière → ATP → travail | Carte de processus transparente | `svt_ch1_carte_metabolique` |
| 2 | Hydrolyse, phosphorylation et couplage | Scène Cytoscape animée | `svt_ch1_cycle_atp` |
| 3 | Comparer des levures avec/sans O₂ | Courbes JSXGraph + laboratoire complet | `svt_ch1_levures_exao`, `labs/respiration-fermentation` |
| 4 | Étapes et bilan de la glycolyse | Schéma BAC validé | `svt_glycolyse` |
| 5 | Compartiments de la mitochondrie | Schéma BAC validé | `svt_mitochondrie_structure` |
| 6 | Pyruvate et cycle de Krebs | Schéma BAC validé | `svt_cycle_krebs` |
| 7 | Électrons, gradient H⁺, ATP synthase et O₂ | Schéma + scène Cytoscape animée | `svt_chaine_respiratoire`, `svt_ch1_chimiosmose` |
| 8 | Bilans et rendement | Schémas + tableau/calcul ordinaire | `svt_respiration_cellulaire`, `svt_bilan_energetique` |
| 9 | Fermentations lactique et alcoolique | Schéma BAC validé | `svt_fermentation` |
| 10 | Construire la synthèse métabolique | Carte Cytoscape à branches | `svt_ch1_carte_metabolique` |
| 11 | Secousse, sommation, tétanos | Courbe JSXGraph contrôlable + laboratoire | `svt_ch1_myogrammes`, `labs/muscle-energie` |
| 12 | Muscle, fibre, myofibrille, sarcomère | Schémas BAC validés | `svt_fibre_musculaire`, `svt_muscle_sarcomere` |
| 13 | Cycle actine–myosine, Ca²⁺ et ATP | Scène Cytoscape animée + laboratoire | `svt_ch1_cycle_actomyosine`, `labs/muscle-energie` |
| 14 | Filières selon durée, puissance et O₂ | Carte Cytoscape contrôlable + exercice | `svt_ch1_filieres_effort`, `filieres-effort` |
| 15 | Dossier BAC et schéma-bilan final | Carte métabolique + schémas existants | `svt_ch1_carte_metabolique` |

## Contrôle par le tuteur LLM

Une scène est ouverte par une ligne `scientific` déclarative :

```json
{
  "type": "scientific",
  "content": "Observons le transfert d’énergie.",
  "scientific": {
    "engine": "preset",
    "presetId": "svt_ch1_cycle_atp",
    "variant": "cycle_complet",
    "autoplay": true
  }
}
```

La scène déjà visible reçoit ensuite une commande bornée :

```json
{
  "type": "scientific",
  "action": "control",
  "payload": {
    "presetId": "svt_ch1_cycle_atp",
    "command": "highlight",
    "parameters": { "variant": "hydrolyse" }
  }
}
```

Commandes autorisées : `start`, `pause`, `reset`, `next`, `previous`,
`set_variant`, `highlight`. Le LLM ne transmet ni JavaScript, ni HTML, ni URL.
Les mêmes commandes restent accessibles à l’élève au bas de la scène.

## Documents authentiques à conserver

Les éléments suivants ne doivent pas être générés comme de fausses données :

- feuille après test à l’eau iodée ;
- photographie du dispositif EXAO ;
- micrographie électronique de mitochondrie avec échelle ;
- coupe de muscle strié ;
- micrographie de sarcomère au repos et contracté.

Chaque document réel indique sa source, sa licence, son échelle ou son
grossissement. Une illustration synthétique est annoncée comme telle.
