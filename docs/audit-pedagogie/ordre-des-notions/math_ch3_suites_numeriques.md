# math_ch3_suites_numeriques
## Ordre proposé des premières notions
1. Rappel : ℕ, ℕ* et l'écriture d'une fonction f(n) (aujourd'hui absent ; à mettre avant la diapo 3)
2. Une suite = une liste numérotée : rang n, terme uₙ, premier rang (diapo 3)
3. uₙ₊₁ n'est pas uₙ + 1 (diapo 4)
4. Suite donnée par une formule en n (diapo 5)
5. Suite définie par une relation uₙ₊₁ = f(uₙ), en précisant que ce n'est pas encore le « raisonnement par récurrence » (diapo 6)
6. Suite arithmétique, puis son terme général (diapos 7-8)
7. Rappel des puissances, puis suite géométrique et son terme général (diapos 9, 10-11)
8. Nombre de termes, puis sommes arithmétique et géométrique, chacune avec un exemple fait avant la question (diapos 12-14)

La porte d'entrée (la liste numérotée, diapo 3) est la bonne. L'ordre des huit premières notions est sain. Il manque seulement le rappel de ℕ / ℕ* et une phrase qui distingue « définie par récurrence » du « raisonnement par récurrence ».

## Défauts
| # | Diapo | Type (1 notion avant / 2 trop vite / 4 question tôt) | Ce qui est dit (citation courte) | Pourquoi ça perturbe | Correction proposée (déplacer, ajouter un rappel avant la diapo N, reformuler…) | Gravité (forte/moyenne) |
|---|---|---|---|---|---|---|
| 1 | 37 | 1 notion avant | « On sait déjà, par la récurrence, que uₙ est entre deux et quatre » | La suite (national 2024, uₙ₊₁ = (4uₙ − 2)/(1 + uₙ)) n'est ni donnée ni démontrée ici : son énoncé n'arrive qu'à la diapo 80 et sa récurrence 2 ≤ uₙ ≤ 4 qu'à la diapo 81. L'élève croit avoir manqué quelque chose. | Déplacer la diapo 37 après la diapo 81 (dans l'exercice 2024), ou écrire à l'écran la relation et dire « l'énoncé a fait démontrer 2 ≤ uₙ ≤ 4 dans une question précédente ». | forte |
| 2 | 28 | 1 notion avant | « u zéro égale quatre : tu as trois inférieur ou égal à un plus uₙ inférieur ou égal à cinq » | L'hypothèse 2 ≤ uₙ ≤ 4 (ce qu'on démontre) n'est jamais dite. De plus, passer à l'inverse et multiplier par −6 un encadrement double n'a été montré que sur des inégalités simples (diapos 19-20). | Dire d'abord la propriété à démontrer (2 ≤ uₙ ≤ 4) et l'hypothèse de récurrence. Faire au moins une étape sur un encadrement double à la diapo 20 (exemple 3 ≤ x ≤ 5 ⇒ 1/5 ≤ 1/x ≤ 1/3). | forte |
| 3 | 26 (option), 27 (bloc su_n2_b4) | 4 question tôt | Options « le quotient uₙ₊₁/uₙ » et « on étudie le quotient uₙ₊₁/uₙ » | L'outil du quotient n'est enseigné qu'à la diapo 38. L'élève ne peut pas juger cette option. | Remplacer cette option par une erreur déjà vue (par exemple « diviser deux inégalités »). | moyenne |
| 4 | 31 (bloc su_n3_b1) | 4 question tôt | « Dans l'hérédité, comment choisis-tu ta méthode ? Donne les trois cas. » | Le 3ᵉ cas (f croissante) a seulement été annoncé à la diapo 27 (« on le verra plus loin ») et n'est enseigné qu'à la diapo 70. | Demander les deux cas vus, ou déplacer cette question après la diapo 70. | moyenne |
| 5 | 6 puis 15 | 2 trop vite | « une suite définie par récurrence » (diapo 6), puis « raisonnement par récurrence » (diapo 15) | Le même mot désigne deux choses différentes, la deuxième étant nouvelle. L'élève faible les confond, et la diapo 2 a déjà dit « la récurrence » au sens du raisonnement. | À la diapo 15, ajouter une phrase : « définir une suite par récurrence (diapo 6), ce n'est pas démontrer par récurrence ». | moyenne |
| 6 | 3 | 1 notion avant | « u₀ si n ∈ ℕ, u₁ si n ∈ ℕ* » | Les notations ℕ et ℕ* (tronc commun) ne sont jamais rappelées. Elles reviennent ensuite partout (blocs après 4 et 24, « ∀n ∈ ℕ »). | Ajouter une courte diapo de rappel avant la diapo 3 : ℕ = {0, 1, 2…}, ℕ* = ℕ sans 0. | moyenne |
| 7 | 31 | 2 trop vite | « on étudie le signe de uₙ₊₁ plus un » | La méthode enseignée (diapos 25-27) est « le signe de uₙ₊₁ − a ». Le passage de − a avec a = −1 à « + 1 » n'est pas dit. | Dire : « ici a = −1, donc uₙ₊₁ − (−1) = uₙ₊₁ + 1 ». | moyenne |
| 8 | 39 | 2 trop vite | « la colonne vₙ égale uₙ moins seize » | Le 16 tombe du ciel : pourquoi 16 et pas un autre nombre ? (16 est la solution de ℓ = ¼ℓ + 12, vue seulement aux diapos 60 et 72.) | Dire que l'énoncé donne toujours vₙ, ou montrer que 16 est le nombre qui ne bouge pas : ¼·16 + 12 = 16. | moyenne |
| 9 | 49 | 1 notion avant | « 1/√n = n^(−1/2) », « nᵅ si α < 0 » | Le rappel des puissances (diapo 9) ne couvre que les exposants entiers positifs. Les exposants négatifs et fractionnaires ne sont jamais rappelés. | Ajouter au rappel de la diapo 9 (ou juste avant la diapo 49) : n⁻¹ = 1/n, n^(1/2) = √n. | moyenne |
| 10 | 54 | 4 question tôt | « u n égale un plus un sur, un moins deux tiers puissance n plus un : calcule la limite » | La question demande les opérations sur les limites (somme, quotient), qui ne sont enseignées qu'à la diapo 55, juste après. | Inverser les diapos 54 et 55 (opérations d'abord), ou poser cette question après la diapo 55. | moyenne |
| 11 | 55 | 2 trop vite | Opérations sur les limites + quatre formes indéterminées + factorisation par la plus grande puissance | Trois notions nouvelles dans une seule diapo, et les formes indéterminées sont aussitôt utilisées. | Couper en deux diapos : opérations (avec l'exemple −5·4ⁿ), puis formes indéterminées et factorisation (avec l'exemple 2ⁿ − 3ⁿ). | moyenne |
| 12 | 60 | 2 trop vite | « Le plafond n'est pas la limite » puis « Règle importante : … passage à la limite » | Deux idées nouvelles dans la même diapo. Le passage à la limite, décisif à la diapo 73 pour choisir ℓ, passe comme une remarque. | Faire du passage à la limite une diapo à part, avec l'exemple 1/n > 0 et sa limite 0. | moyenne |
| 13 | 61 | 1 notion avant | Écran : « |uₙ − ℓ| ≤ vₙ et lim vₙ = 0 ⇒ lim uₙ = ℓ » | La valeur absolue n'est ni rappelée ni dite dans la voix. Cette forme sert ensuite aux diapos 67 et 87. | Rappel avant la diapo 61 : |a − b| = distance entre a et b. Le dire dans la voix à la diapo 67. | moyenne |
| 14 | 45 | 2 trop vite | « Produit en croix, puis tous les uₙ du même côté, on factorise uₙ et on divise » | Quatre manipulations algébriques en une phrase, sans aucune ligne de calcul. C'est pourtant la méthode réutilisée à la diapo 86. | Écrire chaque ligne à l'écran (vₙ(3 − uₙ) = uₙ − 1 ⇒ 3vₙ + 1 = uₙ + vₙuₙ ⇒ …). | moyenne |
| 15 | 78 | 1 notion avant | « uₙ égale un plus vₙ, avec v géométrique » | L'énoncé lu à la diapo 77 ne parle d'aucune vₙ. L'élève ne sait pas d'où sort vₙ, ni sa raison, ni v₀. | Lire dans l'énoncé (diapo 77) la question qui définit vₙ et sa formule, ou la rappeler à l'écran. | moyenne |
| 16 | 74 | 1 notion avant | « on factorise le haut : trois moins x, fois x plus un » | La factorisation d'un trinôme (racines, Δ ; tronc commun / 1ʳᵉ Bac) n'est pas rappelée. | Ajouter une ligne : « −x² + 2x + 3 a pour racines −1 et 3 ». | moyenne |
| 17 | 14 | 2 trop vite | Formule de la somme géométrique, puis tout de suite « Calcule 1 + 2 + 4 … 2¹⁰ » | Aucun exemple n'est fait avant la question, alors que la somme arithmétique en avait deux (diapo 13). | Faire d'abord un petit exemple (1 + 2 + 4 = 7 = (1 − 2³)/(1 − 2)), puis poser la question. | moyenne |

## Notions importantes dites une seule fois
- uₙ₊₁ n'est pas uₙ + 1 — diapo 4
- Notation Σ uₖ (k de p à n) — diapo 13 (écran seulement)
- Vérifier l'écriture donnée par l'énoncé : c'est l'outil (une seule apparition de uₙ) — diapo 28
- Strict / large : < entraîne ≤, pas l'inverse — diapo 29
- Inverse de deux positifs : l'ordre change — diapo 20 (réutilisé seulement à la 28, sans redire la règle)
- Définition par intervalle ouvert et limite −∞ ⇔ lim(−uₙ) = +∞ — diapo 48 (écran seulement)
- Critère avec |uₙ − ℓ| ≤ vₙ — diapo 61 (écran seulement)
- Limite d'une somme géométrique (lim Sₙ = premier terme/(1 − q)) — diapo 79
- Escalier et conjecture sur le graphique (place de u₀) — diapos 68-69
- « En déduire » après uₙ₊₁ ≤ k·uₙ : c'est une récurrence (jamais rédigée) — diapo 64
