# Audit SVT 2e Bac PC BIOF — Géodynamique interne

Date de l'audit : 6 août 2026

## Référence utilisée

Source locale officielle :
`backend/cours 2bac pc/cadres de references 2BAC PC/cadre-de-reference-de-l-examen-national-svt-sciences-physiques (1).json`.

Le domaine 4 représente 25 % du cadre SVT et exige :

1. les chaînes récentes de subduction, d'obduction et de collision ;
2. les déformations tectoniques et leur relation avec les contraintes ;
3. le métamorphisme, les minéraux index, les séries et les diagrammes P-T ;
4. le granite d'anatexie, le granite intrusif et les métamorphismes associés ;
5. un bilan spatial et temporel relié à la tectonique des plaques.

Les supports locaux `Cours-Unit4-1.pdf`, `Cours-Unit4-2.pdf` et
`Cours-Unit4-3.pdf` confirment que l'élève doit exploiter cartes, coupes,
échantillons, lames minces, diagrammes P-T et chronologies.

## État initial du dépôt

| Élément | État observé | Risque pédagogique |
|---|---|---|
| Chapitre actif | `svt_ch4_l1.json` mélangeait tout en 140 minutes | Charge cognitive excessive |
| Métamorphisme | Aucun fichier de leçon 4.2 dans les données de seed | Leçon distante non reproductible localement |
| Granitisation | Aucun fichier de leçon 4.3 dans les données de seed | Contenu absent lors d'un nouveau seed |
| Ressources | `media_resources` vide pour la leçon active | Cours presque entièrement textuel |
| Interactivité | Aucune simulation de géodynamique | L'élève ne manipule ni contraintes ni P-T |
| Données IA | Aucun état structuré d'expérience | Le tuteur ne peut pas commenter une observation réelle |
| Doublon | `svt_ch6_l1.json` reprend le même domaine sans chapitre 6 actif | Ambiguïté de maintenance |

## Lacunes conceptuelles à combler

- Ne pas réduire une chaîne de montagnes à un volcan : distinguer les indices de subduction et de collision.
- Ne pas confondre subduction et obduction : plongement versus transport sur le continent.
- Relier chaque déformation à la contrainte et au comportement de la roche.
- Faire lire un diagramme P-T dans l'ordre : coordonnées, faciès, minéraux, contexte.
- Insister sur l'état solide du métamorphisme et la fusion partielle de l'anatexie.
- Comparer la transition régionale du granite d'anatexie à l'auréole limitée d'un pluton intrusif.
- Exiger une chronologie fondée sur des indices, conformément aux exercices nationaux.

## Restructuration retenue

| Leçon | Question directrice | Manipulation principale |
|---|---|---|
| 4.1 Chaînes et tectonique | Comment un ancien océan devient-il une chaîne ? | Ordonner le cycle et produire trois déformations |
| 4.2 Métamorphisme | Comment une roche révèle-t-elle P, T et le contexte ? | Déplacer un point P-T et enregistrer quatre signatures |
| 4.3 Granitisation | Comment distinguer anatexie et intrusion ? | Classer six indices géologiques |

Chaque leçon suit la même alternance :

1. observer une scène ;
2. formuler une hypothèse ;
3. manipuler ;
4. lire un résultat ;
5. justifier par un indice ;
6. appliquer à un document type Bac.

## Ressources ajoutées

Six scènes générées en 1536 × 1024 :

- cycle orogénique ;
- coupe de subduction ;
- collision et obduction ;
- plis, faille inverse et nappe ;
- roches métamorphiques et lames minces ;
- anatexie, intrusion et auréole de contact.

Le laboratoire `svt_internal_geodynamics_advanced_lab` comporte quatre variantes :

- `chains` ;
- `deformations` ;
- `metamorphism` ;
- `granitization`.

## Protocole IA

Le tuteur reçoit les actions, essais, erreurs, paramètres de déformation,
coordonnées P-T, faciès, minéraux, classements granitiques et progression.

Il peut utiliser uniquement les commandes annoncées dans le manifeste : changer
de variante, placer une étape, modifier les paramètres, lancer un test, régler
P-T, enregistrer une signature, classer un indice, donner un indice, mettre une
structure en évidence et vérifier.

Cette architecture évite les commentaires inventés : le tuteur doit citer une
manipulation réellement présente dans l'état de la simulation.
