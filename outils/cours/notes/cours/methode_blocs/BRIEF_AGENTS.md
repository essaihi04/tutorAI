# Brief — adapter un cours à la méthode des blocs (11 novembre 2026)

Dossier partagé : M = outils\cours\notes\cours\methode_blocs
Cours : backend\data\courses\<deck>.json
Messages et notes en français simple. Règle de l'utilisateur : « on veut des résultats, pas seulement une belle plateforme ».

## À lire d'abord
- `.agents/skills/cours-concentration/SKILL.md`, section « Memory and rhythm » → « Data » (format exact).
- `.agents/skills/suivi-des-acquis/SKILL.md` sections 6 à 8 ; `.agents/skills/professeur/SKILL.md` règles 10, 17, 26 ;
  `.agents/skills/voix-du-cours/SKILL.md` section 1 (texte parlé).
- Le MODÈLE FINI : `M\ajouts\phys_ch1_waves_exemple.json` (fait par l'agent principal) — même forme, même niveau.
- Le cadre du chapitre : `backend/data/curriculum/cadre_reference_2bac_pc.json`, clé `chapitres.<chapitre>`
  (capacités, formules `ecriture`, `hors_cadre.mots` INTERDITS dans tout ce que tu écris).

## Outil (déjà prêt ; la photo des textes protégés est déjà prise — ne refais pas `base`)
  cd backend/data/courses
  set PYTHONIOENCODING=utf-8 (bash : export PYTHONIOENCODING=utf-8)
  python M/blocs.py apercu    <deck>.json                 → plan : diapos, durée voix, questions, exercices, cahier, compétences
  python M/blocs.py appliquer <deck>.json M/ajouts/<deck>.json
  python M/blocs.py verifier  <deck>.json <chapitre>      → doit finir par « cadre : OK » et « blocs : OK »
  python M/blocs.py items     <deck>.json M/<deck>_items.json M/<deck>_demos.json
Tu écris UNIQUEMENT `M/ajouts/<deck>.json` (avec l'outil Write, pas de heredoc bash : les apostrophes cassent bash),
puis tu l'appliques avec `appliquer` (qui relit le cours et n'ajoute que ces champs). Jamais d'édition directe du cours.

## Ce que contient ajouts/<deck>.json
1. `seances` : séances de 3 blocs ; blocs de 3 à 4 diapositives QUI SE SUIVENT dans l'ordre du cours (l'ordre de
   `apercu`), chaque diapositive dans exactement un bloc ; coupe de préférence aux limites des parties ; le bilan
   (« Ce qu'il faut retenir ») et la carte du chapitre dans la DERNIÈRE séance (dernier bloc). Si le nombre de diapositives
   ne tombe pas juste, la dernière séance peut avoir 1 ou 2 blocs (le dire dans le journal) ; jamais un bloc de 2 ou 5
   sauf impossibilité (le dire). Ids : `<préfixe>_s<n>` et `<préfixe>_s<n>_b<k>` (préfixe = celui des slides).
   Temps : voix d'un bloc = somme des `audio.mixed.duration_ms` (apercu l'affiche ; sinon ~450 caractères ≈ 30 s).
   Par bloc :
   - `titre` court ;
   - `cahier` : 2 à 4 lignes `{texte}` à copier, écrites comme le barème (définition mot pour mot du cadre, relation avec
     unités, piège), reprises/condensées des `concentration.cahier` des diapositives du bloc ;
   - `retrouver` : `{prompt: "Cahier fermé : …", attendu: <formule ou définition EXACTE du cadre (formules[].ecriture,
     ou le texte de définition du cadre/du cahier)>, competence_id: <une compétence portée par une diapo du bloc>}` ;
   - `exercice` : s'il existe un exercice (`slide.exercises[i]`, pas la question de la diapo) dans le bloc, REPRENDS-le :
     `{type, reprend: "<slide_id>/e<i>", prompt, options, correct, explanation}` (copie du contenu ; `choices`→`options` ;
     un vrai/faux repris garde `statements`). Sinon écris-en un court, niveau national : `qcm` (`options` 3, `correct`
     index, bonne réponse PAS toujours au même rang, `explanation`) ou `libre` (`attendu`) ; s'il demande un calcul ou de
     montrer/justifier : `demonstration: {parole, lignes:[{texte, mot}]}` (chaque `mot` = extrait exact de `parole`).
2. `rappels` : `{ "<id compétence>": [ … ] }` pour CHAQUE compétence, 3 à 4 questions, au moins deux formes parmi
   `libre` (`attendu`), `qcm` (`options`, `correct` index), `vrai_faux` (`prompt` = l'affirmation, `correct` true/false).
   Faisables sans le cours sous les yeux, niveau du national, pas de copie mot pour mot d'une question du cours.
   Ids `<compétence>_r<n>` (uniques dans le cours).
3. `predictions` : liste des slide_ids dont la question sera posée AVANT l'explication (« prévois avant de voir ») :
   au moins une diapositive sur trois (⌈n/3⌉), et au moins une par partie (sauf partie bilan). Choisis les questions
   existantes qui s'y prêtent (résultat d'une variation, d'une expérience, d'une observation à venir). Une question qui
   demande de relire ce qui vient d'être dit n'est pas une prédiction.
4. `enonces` (optionnel) : `{slide_id: "nouvel énoncé"}` seulement si aucune question d'une partie ne s'y prête : tu
   réécris l'ÉNONCÉ (question.prompt) pour en faire une prédiction, sans changer options ni bonne réponse. Avec parcimonie.

## Règles de texte
- Paroles nouvelles (`demonstration.parole`) = skill voix-du-cours : darija simple, français pour les termes du programme,
  les équations (« v égale d sur tau »), les nombres en lettres (« zéro virgule trois »), les unités en mots ; AUCUN chiffre,
  aucun symbole (= / × → ( ) % ²…), pas de tachkil ; toute phrase entièrement française de plus de dix mots coupée par des
  virgules. Style des démonstrations existantes : « la relation: … l'application numérique: … le résultat: … ».
  `verifier` contrôle chiffres/symboles/longueur.
- Écrit (cahier, prompts, attendus) : français du barème, formules écrites comme le cadre (`formules[].ecriture`) ;
  aucune formule hors cadre, aucun mot de `hors_cadre.mots`. N'écris pas « x = texte » pour une définition (le contrôle
  du cadre le lit comme une formule) : utilise « : ».
- Vérifie chaque calcul (les nombres de tes QCM et démonstrations) avec python.

## Interdits
- Ne change JAMAIS un `speech_text`, une `parole` déjà écrite (réactions, démonstrations), les champs `audio`, les options
  ou la bonne réponse d'une question existante, ni un exercice existant. Pas de nouvelle diapositive, pas de suppression.
  `verifier` compare à la photo et signale toute modification.
- Ne touche qu'à TES cours (liste donnée), via `appliquer`. Pas de frontend/src, pas de backend/app, pas de skill.
- D'autres sessions travaillent dans ce dépôt : ni commit, ni stash, ni reset, ni checkout ; aucun déploiement ; pas de SSH.
- Pas de sous-agent. Disque C: presque plein : pas de gros fichiers ; efface tes fichiers temporaires.

## Journal
Après chaque cours, AJOUTE (append, ne réécris pas le fichier) une section courte à `M/journal.md` :
  ## <deck> — FAIT  (séances/blocs, rappels, prédictions, énoncés réécrits, items, démonstrations, avis de verifier,
  décisions à faire valider). Si tu es coupé, ce qui reste.

## Rapport final (court, français)
Par cours : séances (blocs par séance), nombre de rappels, prédictions / diapositives, énoncés réécrits, nombre d'items
(réactions) et de démonstrations nouvelles, sortie finale de `verifier`, décisions à faire valider.
