# Ce que Moalim peut reprendre de Duolingo

Octobre 2026. Analyse faite uniquement à partir de ce que Duolingo publie lui-même : son code ouvert de révision espacée, son blog et ses articles de recherche. L'application Duolingo n'a pas été décompilée : ses conditions d'utilisation l'interdisent, et sa logique pédagogique tourne sur ses serveurs, pas dans l'application.

## 1. La philosophie

Duolingo résume sa méthode en cinq principes ([blog Duolingo](https://blog.duolingo.com/duolingo-teaching-method)) :

1. **Apprendre en faisant** : des leçons interactives, pas des exposés.
2. **Personnaliser** : chaque leçon s'adapte à ce que l'élève sait déjà.
3. **Se concentrer sur l'essentiel** : des contenus alignés sur des référentiels officiels.
4. **Rester motivé** : des leçons courtes et des mécaniques de jeu.
5. **Prendre plaisir** à apprendre.

L'idée centrale : l'élève ne doit jamais trouver un exercice trop facile, qui l'ennuie, ni trop difficile, qui le décourage ([MIT Sloan](https://sloanreview.mit.edu/?p=108193)).

## 2. Le moteur

### Birdbrain : prévoir la réussite à chaque exercice

Birdbrain estime, pour chaque élève et chaque exercice possible, la probabilité qu'il réponde juste ([blog Duolingo](https://blog.duolingo.com/learning-how-to-help-you-learn-introducing-birdbrain)). Il modélise à la fois le niveau de l'élève et la difficulté de chaque exercice. Un générateur de séance choisit ensuite les exercices dans ce stock. Selon VentureBeat, la cible est d'environ 70 % de chances de réussite quand l'élève va bien, et des exercices plus faciles quand il peine ([VentureBeat](https://venturebeat.com/ai/how-duolingo-uses-ai-in-every-part-of-its-app)). Ce chiffre vient d'un article de presse, pas d'une publication de Duolingo. Le modèle se réentraîne chaque nuit sur les leçons de la veille ([IEEE Spectrum](https://spectrum.ieee.org/duolingo)).

### Half-Life Regression : quand revoir une notion

Code et données publiés sous licence MIT : [duolingo/halflife-regression](https://github.com/duolingo/halflife-regression), article de Settles et Meeder (ACL 2016). Lu directement dans `experiment.py` :

- Chaque notion a une **demi-vie** `h` dans la mémoire de l'élève, en jours.
- La probabilité de s'en souvenir après `Δ` jours sans la revoir est `p = 2^(−Δ / h)`. À `Δ = h`, il reste une chance sur deux.
- La demi-vie se calcule à partir de l'historique : `h = 2^(θ · x)`, avec pour traits `√(1 + bonnes réponses)`, `√(1 + mauvaises réponses)`, un biais et un identifiant de la notion. Chaque notion a ainsi sa propre difficulté à retenir.
- La demi-vie est bornée entre 15 minutes et 274 jours (9 mois).
- Les poids `θ` s'apprennent sur les traces réelles des élèves : 13 millions de traces dans le jeu de données publié.

### Les révisions servent aussi à mesurer

Duolingo glisse parfois dans une leçon un exercice tiré d'une partie antérieure du cours, pour vérifier ce qui est resté ([blog Duolingo](https://blog.duolingo.com/review-exercises-help-measure-learner-recall)).

### La motivation

Les éléments les plus cités sont la série de jours, les points, les ligues et les niveaux. La série de jours est la mécanique jugée la plus efficace pour l'habitude, avec le rappel du soir et le « gel de série ». Certains élèves disent que les ligues créent de la pression ([UX Collective](https://uxdesign.cc/duolingo-analyzing-all-engagement-and-retention-techniques-3e73b79120cf), [Nogood](https://nogood.io/2023/10/09/duolingo-case-study)). Ces sources sont des études de cas et de petites enquêtes, pas des expériences contrôlées.

## 3. Où en est Moalim

| Principe Duolingo | Dans Moalim aujourd'hui |
|---|---|
| Apprendre en faisant | Fait. Le skill prof pose une question après chaque bloc d'explication, l'élève reformule et manipule les laboratoires. |
| Prévoir la réussite pour doser la difficulté | En partie. `knowledge_tracing.py` estime la maîtrise par notion et par activité, avec un modèle bayésien, pendant la séance. Elle n'est pas gardée d'une séance à l'autre, et elle ne sert pas à choisir l'exercice suivant. |
| Révision espacée | Prévue mais jamais déclenchée. La table `spaced_repetition_queue` et le service SM-2 de `spaced_repetition.py` existent, mais aucun code ne les appelle. |
| Oubli dans le temps | En partie. `student_proficiency_service.py` donne moins de poids aux réponses anciennes, mais c'est une pondération globale, pas un oubli propre à chaque notion. |
| Révision glissée dans la séance | Absente. |
| Série de jours, points | Absents de l'application, mentionnés seulement sur la page d'accueil. |
| Leçons courtes | Absentes. Tout passe par la séance complète. |

## 4. Ce qu'il faut reprendre, dans l'ordre

1. **Brancher la révision espacée par notion, avec le modèle de demi-vie.** Il remplacerait le SM-2 jamais branché. Chaque réponse jugée par le skill prof (`<eval>` correct, partiel ou faux) et chaque exercice corrigé alimentent l'historique de la notion. Au début de chaque séance, le tuteur pose une ou deux questions rapides sur les notions dont la probabilité de souvenir est passée sous 0,5. Au départ, les poids sont fixés à la main, faute de données. Ils s'apprendront sur nos propres traces quand il y en aura assez.
2. **Garder la maîtrise d'une séance à l'autre.** L'estimation bayésienne existe déjà ; il suffit de l'enregistrer par élève et par notion.
3. **Choisir l'exercice suivant pour environ 70 % de réussite prévue**, à partir de la maîtrise de l'élève et du taux de réussite de chaque exercice dans la banque d'examens. Plus facile après deux échecs.
4. **La série de jours**, avec un gel de série et un rappel du soir. Pas de classement entre élèves au début, à cause de la pression signalée.
5. **Le format court** : « 5 minutes de révision », uniquement des questions de révision, sans nouvelle notion.

## 5. Ce qu'il ne faut pas reprendre

- **Les cœurs qui bloquent la pratique après des erreurs.** Ils contredisent la règle du skill prof : une erreur appelle un indice et un nouvel essai, pas une sanction.
- **La compétition comme moteur principal.** Pour un élève de bac déjà sous pression, la série de jours personnelle motive sans comparer.
- **L'automatisation complète des contenus.** Duolingo fait rédiger le contenu brut de chaque leçon par des experts, puis l'IA en tire les exercices ([blog Duolingo](https://blog.duolingo.com/how-duolingo-experts-work-with-ai)). C'est aussi le choix de Moalim avec ses cours rédigés.
