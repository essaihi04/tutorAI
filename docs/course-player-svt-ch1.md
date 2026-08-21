# Lecteur de cours scénarisé — SVT, chapitre 1

Ce module remplace l'affichage libre du cours par un parcours scénarisé. Il réutilise les leçons existantes, charge un deck publié quand il existe et conserve l'ancien affichage comme solution de repli.

## Parcours livré

- `svt_ch1_energy` : 11 activités, 22 diapositives, 197 minutes prévues.
- `svt_ch1_muscle` : 5 activités, 10 diapositives, 98 minutes prévues.
- Chaque activité dure de 15 à 20 minutes et associe objectif, apport scientifique, support visuel, activité de l'élève et évaluation formative.
- Chaque diapositive contient un texte de narration, une trace écrite et une microquestion temporisée. Sans réponse, le lecteur poursuit automatiquement.
- Les réponses attendues restent côté serveur. Le navigateur ne reçoit ni corrigé ni liste des réponses acceptées.

Les durées correspondent au temps pédagogique prévu, qui comprend l'observation, la manipulation des simulations, les réponses et la synthèse. Elles ne sont pas un verrou chronométrique imposé à l'élève.

## Comportement du lecteur

Depuis `/tutor` ou `/libre`, une demande explicite comme « Je veux un cours sur l'ATP », « Réviser la respiration cellulaire » ou « Commencer le cours sur la contraction musculaire » est résolue côté serveur vers une leçon autorisée. L'élève est alors redirigé vers le lecteur scénarisé. Une simple question comme « C'est quoi l'ATP ? » reste une question libre et n'ouvre pas un parcours de plusieurs heures.

1. Le lecteur reprend à la dernière diapositive enregistrée.
2. Un audio déjà vérifié est lu s'il correspond exactement au texte courant.
3. En l'absence d'audio publié, le texte reste visible et le passage est rythmé par un temps de lecture local : aucune synthèse vocale n'est déclenchée à la volée.
4. La microquestion peut être un QCM, une prédiction, un vrai/faux, une association, un classement ou une réponse courte.
5. À l'expiration du délai, la réponse est enregistrée comme absente et le cours continue.
6. Une question libre de l'élève met en pause l'audio, la minuterie et l'avancement. La réponse de l'IA s'affiche dans le lecteur, puis le cours reprend quelques secondes avant le point d'interruption.
7. Le changement d'onglet met automatiquement la lecture en pause.

## Publication des données

Appliquer d'abord, dans l'ordre, les migrations Supabase :

```text
database/migrations/20260821_add_course_player.sql
database/migrations/20260821_add_svt_ch1_course_media.sql
```

Depuis le dossier `backend`, synchroniser ensuite les deux manifests :

```powershell
python -m scripts.sync_course_decks
```

Une modification du contenu replace automatiquement le deck en brouillon. Il faut alors vérifier les textes, les corrigés, les médias et les simulations avant une nouvelle publication.

## Génération et validation des audios

La génération est volontairement séparée de la publication. Depuis `backend` :

```powershell
python -m scripts.generate_course_audio generate --deck svt_ch1_energy --language fr
python -m scripts.generate_course_audio generate --deck svt_ch1_muscle --language fr
```

Les fichiers sont versionnés dans `frontend/public/media/audio/courses/`. Un texte inchangé réutilise son fichier existant. Après écoute humaine de tous les fichiers, les publier avec l'identifiant UUID du relecteur :

```powershell
python -m scripts.generate_course_audio verify --deck svt_ch1_energy --language fr --reviewer <UUID_RELECTEUR>
python -m scripts.generate_course_audio verify --deck svt_ch1_muscle --language fr --reviewer <UUID_RELECTEUR>
```

Le lecteur n'accepte qu'un audio au statut `published` dont l'empreinte correspond au texte actuellement publié. Une correction du speech invalide donc automatiquement l'ancien audio sans l'effacer.

## Médias scientifiques

Les micrographies et la photographie diagnostique sont des reconstitutions pédagogiques, pas des documents expérimentaux bruts. Cette provenance doit rester visible dans leurs métadonnées. Les simulations ATP/ADP, chimiosmose et contraction actine–myosine sont déterministes, réinitialisables et communiquent leur état au lecteur avec `postMessage`.

## Évolutions recommandées

- Ajouter des variantes audio explicites en darija ou en mode mixte, puis leur propre cycle de vérification.
- Fournir au professeur un écran de relecture côte à côte : diapositive, speech, audio, corrigé et aperçu élève.
- Ajouter un tableau de maîtrise par objectif à partir des tentatives formatives.
- Autoriser une reprise ciblée des seules diapositives liées aux objectifs non maîtrisés.
- Prévoir des sous-titres synchronisés lorsque les fichiers audio définitifs seront publiés.
