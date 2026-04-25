# Rapport de vérification — 2022-rattrapage

**Titre** : Examen National du Baccalauréat - SVT 2022 Rattrapage
**Année / Session** : 2022 / Rattrapage
**Points total** : 20
**Parties** : 2 | **Questions** : 17
**Documents détectés** : 10

## Vérifications structurelles

- ✅ **Métadonnées** : OK
### ⚠ Points (2 issue(s))
- P2 Exercice 1: Σ questions = 2.5 ≠ 5
- P2 Exercice 3: Σ questions = 2.5 ≠ 5

### ⚠ Assets (1 issue(s))
- crop présent mais NON référencé dans exam.json: doc22p2.png

- ✅ **Couverture** : OK

## Marqueurs détectés dans le PDF OCR

- Numéros arabes trouvés : `['1', '2', '3', '4', '5']`
- Chiffres romains trouvés : `['I', 'II', 'IV']`
- Occurrences d'« Exercice N » : 3

## Analyse sémantique (DeepSeek)

**Qualité globale** : 🔴 poor
**Couverture** : 60%

### ⚠ Problèmes critiques (4)
- La question IV du sujet PDF (attribution des noms aux structures d'un complexe ophiolitique, 1pt) est complètement absente du JSON.
- La numérotation des questions dans le JSON ne correspond pas au PDF : le PDF a une numérotation continue (I, II, III, IV) pour la première partie, mais le JSON les liste comme [None] sans numérotation claire.
- Les points totaux ne correspondent pas : le PDF indique 5 points pour la première partie, mais le JSON liste 1+2+1+1=5pts correctement, mais la structure est confuse.
- Le JSON omet la référence aux documents dans plusieurs questions : par exemple, la question IV du PDF fait référence à un document (image), mais le JSON ne le mentionne pas.

### Problèmes mineurs (3)
- Dans le JSON, la question 1 de l'exercice 1 est marquée comme 'open 0pts', mais elle contient deux sous-questions (a et b) avec des points spécifiques (0.75pt chacun), ce qui est correctement détaillé, mais la numérotation parente est imprécise.
- La correction pour la question 1-b dans le JSON est tronquée avec '…[TRUNCATED_IN_SUMMARY]', mais selon les instructions, cela doit être ignoré, donc pas d'erreur réelle.
- Le JSON utilise 'association' pour certaines questions de la première partie, ce qui correspond au type dans le PDF, donc pas d'erreur de classification.

### Suggestions (4)
- Ajouter la question IV manquante du PDF au JSON avec sa correction correspondante.
- Ajuster la numérotation dans le JSON pour refléter fidèlement celle du PDF (ex: utiliser 'I', 'II', etc., pour la première partie).
- Vérifier et inclure toutes les références aux documents dans les questions du JSON, en particulier pour les questions basées sur des images ou tableaux.
- S'assurer que la structure hiérarchique des questions (ex: questions avec sous-questions) est clairement représentée dans le JSON.
