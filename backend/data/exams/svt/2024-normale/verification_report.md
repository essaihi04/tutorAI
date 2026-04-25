# Rapport de vérification — 2024-normale

**Titre** : Examen National du Baccalauréat - SVT 2024 Normale
**Année / Session** : 2024 / Normale
**Points total** : 20
**Parties** : 2 | **Questions** : 16
**Documents détectés** : 11

## Vérifications structurelles

- ✅ **Métadonnées** : OK
### ⚠ Points (4 issue(s))
- P1 (Première partie : Restitution des connaissances): Σ = 0.0 ≠ 5
- P2 Exercice 1: Σ questions = 0 ≠ 5
- P2 Exercice 2: Σ questions = 0 ≠ 6
- P2 Exercice 3: Σ questions = 0 ≠ 4

- ✅ **Assets** : OK
- ✅ **Couverture** : OK

## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3', '4']`
- Chiffres romains trouvés : `['I', 'II', 'III', 'IV']`
- Occurrences d'« Exercice N » : 3

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🟢 good
**Couverture** : 95%

### ⚠ Problèmes critiques (1)
- La question III dans le JSON est mal structurée : elle est listée comme une question de type 'vrai_faux' avec une correction globale, mais elle contient également quatre sous-questions individuelles non numérotées (a, b, c, d) sans correction spécifique. Dans le PDF, la question III est une seule question avec quatre propositions (a, b, c, d) à évaluer comme vrai ou faux, et la correction PDF fournit les réponses pour chaque proposition. Le JSON devrait refléter cela comme une seule question avec des sous-parties ou une liste de propositions.

### Problèmes mineurs (1)
- Dans le JSON, la question IV est listée comme ayant des options de droite (R) a, b, c, d, e, mais dans le PDF, l'ensemble B a cinq options (a, b, c, d, e). Le JSON inclut correctement 'e', mais il est noté comme 'R: e' sans problème majeur. Cependant, la numérotation dans le JSON pour les exercices de la partie 2 utilise des chiffres simples (1, 2, 3, 4) sans préfixe d'exercice, ce qui pourrait prêter à confusion, mais cela correspond au PDF où les questions sont numérotées à l'intérieur de chaque exercice.

### Suggestions (1)
- Restructurer la question III dans le JSON pour qu'elle corresponde à la structure du PDF : une seule question avec des sous-parties (a, b, c, d) et des corrections individuelles. Vérifier que toutes les questions du PDF sont présentes et correctement classées par type.
