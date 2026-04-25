# Rapport de vérification — 2025-rattrapage

**Titre** : Examen National du Baccalauréat - SVT 2025 Rattrapage
**Année / Session** : 2025 / Rattrapage
**Points total** : 20
**Parties** : 2 | **Questions** : 14
**Documents détectés** : 13

## Vérifications structurelles

- ✅ **Métadonnées** : OK
- ✅ **Points** : OK
- ✅ **Assets** : OK
- ✅ **Couverture** : OK

**Toutes les vérifications structurelles sont passées ✓**

## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3', '4']`
- Chiffres romains trouvés : `['I', 'II', 'III', 'IV']`
- Occurrences d'« Exercice N » : 4

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🟢 good
**Couverture** : 100%

### Problèmes mineurs (2)
- La question IV dans le JSON est structurée avec des sous-questions individuelles (par exemple, "L'ozone troposphérique...") marquées avec des points 0pts, ce qui pourrait être une erreur de représentation car dans le PDF, c'est une seule question avec 4 sous-parties notées collectivement 1pt. Le JSON devrait probablement refléter cela comme une question unique avec des sous-éléments.
- Dans le JSON, pour la question III (association), le contenu de la question 4 est tronqué dans la partie gauche ("L: 4. L'eutrophisation résulte des événements suivants : 1. Mort des êtres vivants ; 2. Diminution de l"), ce qui est une omission partielle du texte original du PDF. Bien que cela n'affecte pas la correction, c'est une divergence de contenu.

### Suggestions (2)
- Pour améliorer la fidélité, assurez-vous que le contenu textuel des questions dans le JSON correspond exactement au PDF, en évitant les troncatures non marquées comme "…[TRUNCATED_IN_SUMMARY]".
- Considérez ajuster la structure du JSON pour les questions à sous-parties (comme IV) pour mieux refléter la notation groupée du PDF, par exemple en les regroupant sous une seule entrée avec des sous-questions internes.
