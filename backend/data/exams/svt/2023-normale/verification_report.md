# Rapport de vérification — 2023-normale

**Titre** : Examen National du Baccalauréat - SVT 2023 Normale
**Année / Session** : 2023 / Normale
**Points total** : 20
**Parties** : 2 | **Questions** : 19
**Documents détectés** : 12

## Vérifications structurelles

- ✅ **Métadonnées** : OK
### ⚠ Points (1 issue(s))
- P2 Exercice 1: Σ questions = 2.75 ≠ 5

### ⚠ Assets (1 issue(s))
- crop présent mais NON référencé dans exam.json: doc2p5.png

- ✅ **Couverture** : OK

## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3', '4', '5']`
- Chiffres romains trouvés : `[]`
- Occurrences d'« Exercice N » : 4

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🟢 good
**Couverture** : 100%

### Problèmes mineurs (3)
- La question IV dans le JSON est classée comme "association", mais dans le PDF, elle est présentée comme une correspondance entre deux ensembles avec des instructions spécifiques de recopiage des couples. Le type "association" est correct, mais une vérification plus fine pourrait noter que le JSON ne reproduit pas explicitement la structure "Ensemble 1" et "Ensemble 2" comme dans le PDF, bien que les paires soient correctes.
- Dans l'exercice 1, la question 1 est structurée en deux sous-questions (a et b) dans le PDF, mais le JSON la traite comme une seule entrée avec deux sous-parties non numérotées ("[None]"). Cela pourrait être amélioré pour refléter plus fidèlement la numérotation hiérarchique du PDF (ex: 1.a et 1.b).
- Le JSON indique "docs:0" pour l'exercice 3, mais le PDF mentionne des documents (comme les croisements présentés dans des tableaux). Cela pourrait être une omission mineure dans la métadonnée, car le contenu des questions est présent.

### Suggestions (2)
- Pour améliorer la fidélité, structurer les sous-questions avec une numérotation explicite (ex: 1.a, 1.b) plutôt que des entrées "[None]".
- Inclure des métadonnées plus précises sur les documents référencés dans chaque exercice, même s'ils sont décrits dans le texte.
