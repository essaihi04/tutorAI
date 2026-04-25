# Rapport de vérification — 2024-rattrapage

**Titre** : Examen National du Baccalauréat - SVT 2024 Rattrapage
**Année / Session** : 2024 / Rattrapage
**Points total** : 20
**Parties** : 2 | **Questions** : 15
**Documents détectés** : 10

## Vérifications structurelles

- ✅ **Métadonnées** : OK
### ⚠ Points (2 issue(s))
- P1 (Première partie : Restitution des connaissances): Σ = 4.0 ≠ 5
- P2 Exercice 2: Σ questions = 4.5 ≠ 6

- ✅ **Assets** : OK
### ⚠ Couverture (1 issue(s))
- Exercices: PDF détecte 2 / JSON contient 3


## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3', '4']`
- Chiffres romains trouvés : `['I', 'II', 'III', 'IV']`
- Occurrences d'« Exercice N » : 2

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🟢 good
**Couverture** : 95%

### ⚠ Problèmes critiques (2)
- La question I.2 dans le JSON est marquée comme ayant 0 points, mais dans le PDF elle vaut 0.5 points (0.25 pour chaque sous-question).
- La question IV dans le JSON est classée comme 'association' mais ne liste pas explicitement les paires correctes comme dans la correction PDF (1→d, 2→a, 3→e, 4→b).

### Problèmes mineurs (4)
- La numérotation dans le JSON pour la question I.2.a et I.2.b utilise '?' au lieu de 'a' et 'b' comme dans le PDF.
- Le JSON liste 'docs:5' pour l'Exercice I, mais le PDF mentionne plusieurs documents (1 à 5) sans préciser combien exactement ; cela pourrait être une légère imprécision.
- Dans l'Exercice 2, la question 3 est traitée comme une seule entrée dans le JSON, mais le PDF la divise en sous-parties a et b avec des corrections séparées ; le JSON fusionne cela sans sous-structure claire.
- Le contexte de l'Exercice 3 dans le JSON est tronqué ('comme le' au lieu de 'comme les margines'), mais ce n'est pas critique car marqué comme tronqué.

### Suggestions (4)
- Corriger les points pour la question I.2 dans le JSON pour refléter 0.5 points au total.
- Ajouter les paires correctes explicites pour la question IV dans le JSON, similaires à la correction PDF.
- Utiliser une numérotation cohérente avec le PDF pour les sous-questions (par exemple, 'a' et 'b' au lieu de '?').
- Considérer ajouter une sous-structure pour la question 3 de l'Exercice 2 dans le JSON pour mieux refléter les sous-parties a et b.
