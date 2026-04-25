# Rapport de vérification — 2020-normale

**Titre** : Examen National du Baccalauréat - SVT 2020 Normale
**Année / Session** : 2020 / Normale
**Points total** : 20
**Parties** : 2 | **Questions** : 16
**Documents détectés** : 8

## Vérifications structurelles

- ✅ **Métadonnées** : OK
### ⚠ Points (1 issue(s))
- P1 (Première partie : restitution des connaissances): Σ = 10.0 ≠ 5

- ✅ **Assets** : OK
### ⚠ Couverture (1 issue(s))
- Exercices: PDF détecte 4 / JSON contient 3


## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3', '4', '5', '2020']`
- Chiffres romains trouvés : `['I', 'II', 'III', 'IV']`
- Occurrences d'« Exercice N » : 4

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🟢 good
**Couverture** : 95%

### ⚠ Problèmes critiques (1)
- La question 5 de l'exercice 3 est manquante dans le JSON. Elle est présente dans le PDF (question 5: 'Expliquez les pourcentages des phénotypes obtenus dans la descendance du quatrième croisement en illustrant votre réponse par un schéma.') avec une correction correspondante dans le PDF de correction, mais absente du JSON généré.

### Problèmes mineurs (3)
- La numérotation des questions dans le JSON pour l'exercice 3 est incorrecte : les sous-questions 4.a et 4.b sont listées comme des questions distinctes, mais dans le PDF, elles font partie de la question 4. Le JSON devrait refléter cette hiérarchie (par exemple, 4 avec sous-parties a et b).
- Le JSON liste 'Exercice 3 (4pts) — docs:0', mais l'exercice 3 dans le PDF ne fait référence à aucun document explicite. Ce n'est pas une erreur critique, mais la mention 'docs:0' pourrait être omise pour plus de précision.
- Dans le JSON, pour la question IV du Choix 1, le type est marqué comme 'association', ce qui est correct, mais la description pourrait être plus précise pour refléter qu'il s'agit d'un appariement entre deux groupes.

### Suggestions (3)
- Ajouter la question manquante 5 de l'exercice 3 au JSON avec sa correction correspondante.
- Corriger la structure hiérarchique des questions de l'exercice 3 pour refléter que 4.a et 4.b sont des sous-parties de la question 4.
- Vérifier et ajuster la numérotation et les types de questions pour assurer une correspondance exacte avec le PDF, notamment pour les questions à sous-parties.
