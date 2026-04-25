# Rapport de vérification — 2023-rattrapage

**Titre** : Examen National du Baccalauréat - SVT 2023 Rattrapage
**Année / Session** : 2023 / Rattrapage
**Points total** : 20
**Parties** : 2 | **Questions** : 18
**Documents détectés** : 14

## Vérifications structurelles

- ✅ **Métadonnées** : OK
### ⚠ Points (1 issue(s))
- P1 (Première partie : Restitution des connaissances): Σ = 0.0 ≠ 5

### ⚠ Assets (4 issue(s))
- crop présent mais NON référencé dans exam.json: doc1p1.png
- crop présent mais NON référencé dans exam.json: doc1p3.png
- crop présent mais NON référencé dans exam.json: doc2p6.png
- crop présent mais NON référencé dans exam.json: doc3p6.png

- ✅ **Couverture** : OK

## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3', '4']`
- Chiffres romains trouvés : `['I', 'II', 'III', 'IV']`
- Occurrences d'« Exercice N » : 4

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🟢 good
**Couverture** : 95%

### ⚠ Problèmes critiques (1)
- La question IV du JSON contient des descriptions incorrectes pour les éléments 2, 3 et 4. Dans le PDF, ces éléments sont décrits comme 'Filament de myosine', mais la correction attend des noms spécifiques (troponine, Tropomyosine, Tête de myosine). Le JSON devrait refléter cela avec des descriptions distinctes pour chaque élément.

### Problèmes mineurs (3)
- Dans la partie III du JSON, la structure 'L: 1, L: 2, L: 3, L: 4' suivie de toutes les options R est ambiguë. Le PDF présente clairement quatre questions distinctes avec des options spécifiques pour chacune. Le JSON devrait structurer cela en quatre questions séparées avec leurs options respectives.
- Le JSON ne mentionne pas explicitement les documents référencés dans certaines questions (par exemple, Exercice 1 question 2 fait référence au document 2, mais le JSON ne le note pas).
- Dans l'Exercice 2, la question 2.b du JSON est marquée comme 'open', mais elle implique un calcul spécifique basé sur des données génétiques, ce qui pourrait être mieux classé comme 'calculation'.

### Suggestions (4)
- Pour la partie IV, ajuster les descriptions dans le JSON pour correspondre aux éléments spécifiques attendus (par exemple, 'Élément 2' au lieu de 'Filament de myosine' pour tous).
- Restructurer la partie III dans le JSON pour avoir quatre entrées distinctes, chacune avec ses propres options, afin de mieux refléter la structure du PDF.
- Ajouter des références aux documents dans les questions où ils sont mentionnés dans le PDF pour améliorer la précision.
- Considérer une classification plus fine pour les types de questions, comme 'calculation' pour les questions impliquant des calculs spécifiques.
