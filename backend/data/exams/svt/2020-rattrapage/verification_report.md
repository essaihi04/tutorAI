# Rapport de vérification — 2020-rattrapage

**Titre** : Examen National du Baccalauréat - SVT 2020 Rattrapage
**Année / Session** : 2020 / Rattrapage
**Points total** : 20
**Parties** : 2 | **Questions** : 16
**Documents détectés** : 16

## Vérifications structurelles

- ✅ **Métadonnées** : OK
### ⚠ Points (7 issue(s))
- P1 (Première partie (Restitution des connaissances)): Σ = 3.0 ≠ 5
- P2 Exercice 1: Σ questions = 0 ≠ 3
- P2 Exercice 2: Σ questions = 0 ≠ 4
- P2 Exercice 3: Σ questions = 0 ≠ 4
- P2 Exercice 4: Σ questions = 0 ≠ 4
- P2 Exercice 5: Σ questions = 0 ≠ 4
- P2 (Deuxième partie : Raisonnement scientifique et communication écrite et graphique): Σ = 19.0 ≠ 15

### ⚠ Assets (1 issue(s))
- crop présent mais NON référencé dans exam.json: doc1p1.png

### ⚠ Couverture (1 issue(s))
- Exercices: PDF détecte 6 / JSON contient 5


## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3']`
- Chiffres romains trouvés : `['III', 'IV']`
- Occurrences d'« Exercice N » : 6

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🔴 poor
**Couverture** : 60%

### ⚠ Problèmes critiques (3)
- Questions manquantes dans le JSON : les questions I et II de la première partie (Restitution des connaissances) sont absentes du JSON alors qu'elles sont présentes dans le PDF sujet et la correction.
- Points incorrects : le JSON indique 'Total: 20pts' mais le PDF sujet montre clairement que la première partie vaut 5 pts et la deuxième partie 15 pts, soit un total de 20 pts, ce qui est correct. Cependant, les sous-questions dans le JSON ont des points à 0pts alors qu'ils devraient refléter les points attribués dans la correction (ex: Q1 de l'exercice 1 vaut 1.25 pts, Q2.a vaut 1 pt, etc.).
- Numérotation incorrecte : dans le JSON, les questions de la partie IV (QCM) sont numérotées avec des '?' au lieu de '1', '2', '3', '4' comme dans le PDF.

### Problèmes mineurs (2)
- Contenu de question tronqué : bien que le marqueur '…[TRUNCATED_IN_SUMMARY]' soit présent, certaines questions dans le JSON sont incomplètes par rapport au PDF, comme 'Un agriculteur souhaite obtenir la plus grande proportion possible...' qui est tronquée au-delà du marqueur.
- Documents non référencés : dans le JSON, l'exercice 3 est indiqué avec 'docs:0' mais le PDF sujet ne mentionne pas de documents pour cet exercice, ce qui est correct. Cependant, pour les autres exercices, la référence aux documents est correcte mais pourrait être plus précise (ex: exercice 1 a 3 documents, exercice 2 a 3 documents, etc.).

### Suggestions (4)
- Ajouter les questions manquantes I et II de la première partie dans le JSON avec leurs corrections correspondantes.
- Corriger les points des sous-questions dans le JSON pour qu'ils correspondent exactement aux points indiqués dans la correction PDF.
- Utiliser la numérotation correcte des questions (ex: '1', '2', etc.) au lieu de '?' pour les QCM.
- Vérifier et compléter le contenu des questions tronquées au-delà du marqueur '…[TRUNCATED_IN_SUMMARY]' pour assurer la fidélité au PDF sujet.
