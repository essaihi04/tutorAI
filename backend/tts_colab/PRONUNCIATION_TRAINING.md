# Correction de prononciation — Academy TTS

## Ordre de travail

1. Ajouter ou corriger la forme parlée dans
   `backend/app/data/tts_pronunciations.json`.
2. Exécuter les tests du normaliseur.
3. Générer le banc audio et faire une transcription aveugle.
4. Enregistrer de nouvelles données seulement si la forme développée reste
   mal prononcée par Academy.

Le texte affiché à l'élève ne change pas. Seule la copie envoyée au TTS est
développée (`25%` devient `vingt-cinq pour cent`, par exemple).

## Trouver les cas réels

Depuis `backend/` :

```powershell
..\.venv\Scripts\python.exe scripts\audit_tts_pronunciations.py
..\.venv\Scripts\python.exe scripts\audit_tts_pronunciations.py --language mixed
```

Le rapport classe les nombres, unités, pourcentages, fractions, formules et
abréviations présents dans les examens et les données applicatives.

## Format des nouvelles données

Pour chaque difficulté restante, enregistrer 10 à 20 contextes différents.
Chaque clip doit être mono, 24 kHz, PCM 16 bits, propre, sans musique ni
réverbération, et durer idéalement entre 3 et 10 secondes.

La transcription d'entraînement doit être la forme réellement prononcée :

```json
{
  "audio": "clips/svt_001.wav",
  "text_raw": "La note de SVT représente 25%.",
  "text": "La note de ès vé té représente vingt-cinq pour cent.",
  "language": "fr",
  "category": ["abbreviation", "percentage"],
  "speaker": "prof_faress"
}
```

Garder un groupe de phrases par catégorie exclusivement pour l'évaluation.
Ne jamais entraîner sur ce groupe. Mélanger les nouveaux clips correctifs avec
le corpus original afin d'éviter que le modèle oublie les phrases ordinaires.

## Validation avant remplacement du checkpoint

- transcription exacte des nombres et pourcentages ;
- au moins 95 % des noms et abréviations du banc de test reconnus ;
- aucune coupure ou phrase anormalement courte ;
- écoute humaine en français et en darija ;
- comparaison avec le checkpoint de production sur des phrases ordinaires.

Le checkpoint et les scripts de fine-tuning restent actuellement sur
`MyDrive/academy_tts/`. Ils doivent être sauvegardés avant tout nouvel
entraînement. Le nouveau checkpoint ne remplace `ckpt_prof_faress` qu'après
validation complète du banc de test.
