# Rapport de vérification — 2025-normale

**Titre** : Examen National du Baccalauréat - SVT 2025 Normale
**Année / Session** : 2025 / Normale
**Points total** : 20
**Parties** : 2 | **Questions** : 17
**Documents détectés** : 11

## Vérifications structurelles

- ✅ **Métadonnées** : OK
### ⚠ Points (3 issue(s))
- P2 Exercice 1: Σ questions = 0 ≠ 5
- P2 Exercice 2: Σ questions = 0 ≠ 5
- P2 Exercice 3: Σ questions = 0 ≠ 5

- ✅ **Assets** : OK
- ✅ **Couverture** : OK

## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3', '4', '5']`
- Chiffres romains trouvés : `['I', 'II', 'III', 'IV']`
- Occurrences d'« Exercice N » : 3

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🟢 good
**Couverture** : 100%

### Problèmes mineurs (3)
- La numérotation des questions dans le JSON ne correspond pas exactement à celle du PDF. Par exemple, dans le PDF, la partie I est une question QCM unique avec 4 sous-questions, mais dans le JSON, elle est traitée comme 4 questions distinctes sans regroupement clair. De même, les sous-questions comme 1.a et 1.b dans l'exercice 1 sont listées séparément sans indiquer qu'elles font partie de la question 1.
- Les points attribués dans le JSON pour certaines questions sont incorrects. Par exemple, dans le PDF, la question II.a vaut 0.5 point, mais dans le JSON, elle est marquée comme 0.5pts, ce qui est correct, mais la structure pourrait être plus précise. Aucune erreur majeure de points n'a été détectée, mais la vérification des totaux pourrait être améliorée.
- Le JSON ne référence pas explicitement les documents mentionnés dans les questions. Par exemple, dans l'exercice 1, les questions se basent sur les documents 2 et 3, mais cela n'est pas clairement indiqué dans la structure JSON au-delà du champ 'docs' général.

### Suggestions (3)
- Améliorer la structure hiérarchique du JSON pour refléter fidèlement la numérotation et le regroupement des questions du PDF, par exemple en utilisant des sous-listes pour les sous-questions.
- Vérifier et ajuster les points attribués à chaque question pour assurer une correspondance exacte avec le PDF, en particulier pour les questions composites.
- Ajouter des champs dans le JSON pour référencer spécifiquement les documents utilisés dans chaque question, afin de faciliter la navigation et la compréhension.
