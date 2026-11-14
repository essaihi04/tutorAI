# Audit « rythme et départ de zéro » des 23 cours (14 novembre 2026)

Règles appliquées : **33** (une chose à la fois : le principe, une question de vérification, chaque expérience seule et lentement, le résultat décisif trouvé par l'élève) et **34** (départ de zéro : prérequis enseignés depuis le début, chaque notion expliquée deux fois de deux façons). Elles sont dans `.agents/skills/professeur/SKILL.md`. Les consignes données aux agents sont dans [BRIEF.md](BRIEF.md).

## État

- Les nouvelles versions des 23 cours sont dans `backend/data/courses/en_attente/<deck>.json`. Elles ne sont **pas servies** : les cours en ligne n'ont pas changé.
- Sur chaque diapo dont la voix a changé, `audio.mixed` est retiré : il faut enregistrer la voix Bodi avant de remplacer le cours en ligne.
- Les simulations existantes n'ont reçu que des ajouts : paramètre `conclusions`, nouvelles vues, nouveaux moments. Leur comportement par défaut ne change pas, et le cours en ligne les utilise toujours.

| Matière | Audit | Ce qui change | Voix à enregistrer |
|---|---|---|---|
| Maths (6 cours) | [maths.md](maths.md) | 30 rappels depuis zéro (`rappels.html`), la voix ne donne plus le résultat avant de le demander, diapos chargées coupées, 2 questions d'observation par cours | ≈ 304 pistes |
| Physique ch1–5 | [physique-ch1-5.md](physique-ch1-5.md) | rappels (vitesse, milli, sinusoïde, radian, atome, exponentielle, puissances de dix, énergie…), 15 diapos coupées, 8 questions d'observation, ch1 (servi aux élèves) passe de 16 à 22 diapos | ≈ 157 pistes |
| Physique ch6–9 | [physique-ch6-9.md](physique-ch6-9.md) | rappels (courant, tension, loi d'Ohm, dérivée, exponentielle, cosinus, ion, mole, concentration), le principe avant chaque expérience, le régime critique séparé, 8 questions d'observation | ≈ 160 pistes |
| Chimie ch10–13 | [chimie.md](chimie.md) | rappels (mole, concentration, ion, équation, pente, log, dilution) dans `prerequis.html`, diapos coupées, 6 questions d'observation | 123 pistes |
| SVT (4 cours) | [svt.md](svt.md) | **Griffith en 5 diapos**, la 4ᵉ expérience trouvée par l'élève ; Avery en 2 ; cellule, chromosomes, mitose, glucose, ADN et protéine enseignés depuis zéro | ≈ 103 pistes |

## Pour passer en ligne

1. Libérer un GPU Kaggle : compte `ferdaous04`, kernel `academy-tts-essai`, Versions → Stop session. Le compte 2 a épuisé son quota jusqu'au 21 novembre. *Fait le 14 novembre à 17 h 14 UTC.*
2. Enregistrer les voix Bodi. 891 pistes manquent, environ 228 000 caractères, soit 3 h de GPU environ. Elles sont dans les dossiers `/srv/corpus_v4/voix_lot/att_<deck>/` du VPS ; ces dossiers ne contiennent que les pistes sans voix.
   - Le surveillant `relance_att.sh` (journal : `relance_att.log`) attend la fin des réactions SVT ch1–3 du cours en ligne.
   - Il relance ensuite le lot du compte 1 avec `VOIX_D_ABORD=att_`, ce qui met les cours en attente en tête.
   - Les dossiers de liste et de pose sont dans le dossier temporaire de la session : `attente/construire.py` et `attente/poser.py`.
3. Poser les voix dans les copies en attente : `python -X utf8 poser.py 12 [deck…]`.
   - Le script reprend le MP3 du cours en ligne quand le texte est identique, et ne convertit en MP3 (v12) que les voix neuves.
   - Il cherche les WAV dans `att_<deck>/`, puis dans `<deck>/`, puis dans `_observations/`.
   - Il dit pour chaque cours ce qui manque encore.
3. Faire relire par un professeur les réactions écrites à la main et les mots darija rares signalés.
4. Pour chaque cours : remplacer `backend/data/courses/<deck>.json` par sa copie en attente, avec ses pistes posées, puis le jouer dans le lecteur, commiter, déployer et reconstruire le lien libre.

## Pas encore vérifié

- Le déroulé dans le vrai lecteur : arrêt de la voix avant les questions d'observation, arrêts sur image des diapos coupées. Les copies en attente ne sont pas servies.
- Les voix elles-mêmes : murmures, transcription.
- `preparer_reponses.py verifier`, qui exige les pistes.
- Les restes signalés dans chaque audit, par exemple `ln_e1`, le réactif limitant en ch9, quelques sujets du national encore longs, et trois blocs du ch4 de physique sans « À toi ».
