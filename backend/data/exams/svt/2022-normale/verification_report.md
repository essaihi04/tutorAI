# Rapport de vérification — 2022-normale

**Titre** : Examen National du Baccalauréat - SVT 2022 Normale
**Année / Session** : 2022 / Normale
**Points total** : 20
**Parties** : 2 | **Questions** : 17
**Documents détectés** : 10

## Vérifications structurelles

- ✅ **Métadonnées** : OK
### ⚠ Points (1 issue(s))
- P1 (Première partie : Restitution des connaissances): Σ = 3.0 ≠ 5

- ✅ **Assets** : OK
- ✅ **Couverture** : OK

## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3', '4', '5', '2022']`
- Chiffres romains trouvés : `['I', 'II', 'III']`
- Occurrences d'« Exercice N » : 3

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🟢 good
**Couverture** : 100%

### Problèmes mineurs (3)
- La numérotation des questions dans le JSON ne correspond pas exactement à celle du PDF. Dans le PDF, la partie I est structurée en I, II, III, mais le JSON aplatit cela en une liste avec des sous-questions. Cela n'est pas une erreur critique, mais c'est une divergence de structure.
- Dans le JSON, la question III est classée comme "association", ce qui est correct, mais le PDF la présente comme une correspondance entre deux ensembles. La classification est correcte, mais le terme "association" pourrait être légèrement imprécis par rapport à la formulation du PDF.
- Le JSON indique "Total: 20pts", mais le PDF montre 5 pts pour la partie I et 15 pts pour la partie II, totalisant 20 pts. C'est correct, mais il n'y a pas de vérification explicite des points dans le JSON au-delà de cette déclaration initiale.

### Suggestions (3)
- Pour améliorer la fidélité, aligner la structure hiérarchique du JSON sur celle du PDF, en conservant les sections I, II, III comme des conteneurs distincts.
- Vérifier que tous les points attribués dans le JSON correspondent exactement à ceux du PDF pour chaque question, bien que cela semble correct ici.
- S'assurer que les références aux documents dans le JSON (comme "docs:4" pour l'exercice 1) sont correctes et complètes par rapport au PDF.
