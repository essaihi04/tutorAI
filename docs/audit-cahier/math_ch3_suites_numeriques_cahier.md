# Cahier de l'élève — Suites numériques (`math_ch3_suites_numeriques`)

18 novembre 2026. Skill `cahier-de-l-eleve`. Le texte ci-dessous est exactement celui posé dans les cours par
`appliquer.py` (répertoire temporaire de la session ; rejouable). Le plan suit la **copie en attente** (rappels au
moment où ils servent) ; les différences du cours en ligne sont dans « Découpage ».

Conventions : les titres de partie `I.` à `IX.` sont ceux des activités, que l'application écrit d'elle-même en tête
du bloc qui entre dans la partie ; le cahier numérote donc `1.`, `2.`… dans chaque partie, puis `1)`, `2)` pour les
étapes d'une méthode. `lim_{n→+∞}` s'affiche avec « n→+∞ » sous « lim » (Formule.tsx). Une ligne = une idée,
≤ ~90 caractères ; 4 à 6 lignes et 0 à 1 figure par bloc. Le nombre de lignes d'un bloc n'est jamais égal à son nombre
de diapositives : sinon `TableauCahier` coiffe chaque ligne du titre d'une diapositive (mode « une ligne par diapo »),
ce qui casserait la numérotation du cahier.

## Le cahier idéal du chapitre

Les figures sont indiquées à l'endroit où elles s'écrivent : *[Figure : titre — légende]*.

### I. Une suite, ses termes ; arithmétique et géométrique

- Plan d'un exercice : récurrence, monotonie, convergence, suite auxiliaire, limite.
- 1\. Définition : une suite (uₙ) associe à chaque entier n (le rang) un nombre uₙ (le terme).
- Premier terme : u₀ si n ∈ ℕ ; u₁ si n ∈ ℕ* (on note alors (uₙ)ₙ≥₁).
- Attention : uₙ₊₁ est le terme suivant (rang n + 1) ; uₙ + 1 est uₙ augmenté de 1.
- Exemple : u₂ = 5 donne u₂ + 1 = 6, mais u₃ reste inconnu sans la relation de récurrence.

- 2\. Suite explicite uₙ = f(n) : on remplace n. Ex. uₙ = 3n + 2 : u₀ = 2, u₁ = 5.
- Suite récurrente : u₀ = 17, uₙ₊₁ = ¼uₙ + 12 ⇒ u₁ = 16,25 ; u₂ = 16,0625.
- 3\. Suite arithmétique de raison r : pour tout n ∈ ℕ, uₙ₊₁ = uₙ + r.
- Méthode : on calcule uₙ₊₁ − uₙ ; si on trouve une constante r, (uₙ) est arithmétique.
- Terme général : uₙ = uₚ + (n − p)r ; uₙ = u₀ + nr ; uₙ = u₁ + (n − 1)r.
- Exemple : u₀ = 2 et r = 3 donnent uₙ = 2 + 3n.
- *[Figure (croquis) : Suite arithmétique : des pas égaux — uₙ = 3n + 2 : de u₀ = 2 à u₃ = 11, on ajoute toujours la même chose, r = 3 (uₙ₊₁ − uₙ = 3).]*

- Rappel : qⁿ = q × q × … × q (n facteurs) ; q⁰ = 1 (et non 0) ; qⁿ⁺¹ = qⁿ × q.
- 4\. Suite géométrique de raison q : pour tout n ∈ ℕ, uₙ₊₁ = q·uₙ.
- Méthode : on écrit uₙ₊₁ et on fait apparaître q × uₙ (pas de quotient : uₙ peut être nul).
- Terme général : uₙ = uₚ·qⁿ⁻ᵖ ; uₙ = u₀·qⁿ ; uₙ = u₁·qⁿ⁻¹.
- Vérification avec n = 0 : u₀·q⁰ = u₀. Ex. 5 ; 10 ; 20 ; 40 : q = 2 et uₙ = 5 × 2ⁿ.

- 5\. Nombre de termes de uₚ à uₙ : n − p + 1. Ex. de u₀ à u₂₀₂₁ : 2022 termes.
- Somme arithmétique : S = (nombre de termes) × (premier + dernier)/2.
- uₚ + … + uₙ = (n − p + 1)(uₚ + uₙ)/2 ; ex. 1 + 2 + … + 10 = 10 × 11/2 = 55.
- Somme géométrique (q ≠ 1) : uₚ + … + uₙ = uₚ × (1 − qⁿ⁻ᵖ⁺¹)/(1 − q).
- En particulier, pour q ≠ 1 : 1 + q + q² + … + qⁿ = (1 − qⁿ⁺¹)/(1 − q).
- Attention : la puissance de q est le nombre de termes (n − p + 1).

### II. Le raisonnement par récurrence

- 1\. Principe (dominos) : P₀ vraie et Pₙ ⇒ Pₙ₊₁ pour tout n ; alors Pₙ vraie pour tout n ∈ ℕ.
- 2\. Rédaction type : « Montrons par récurrence que, pour tout n ∈ ℕ, uₙ > 16. »
- Initialisation : au premier rang (n = 0) : u₀ = 17 > 16, la propriété est vraie au rang 0.
- Hérédité : soit n ∈ ℕ ; supposons uₙ > 16 (hypothèse de récurrence) ; montrons uₙ₊₁ > 16.

- Conclusion : d'après le principe de récurrence, pour tout n ∈ ℕ, uₙ > 16.
- Attention : jamais « supposons que pour tout n » ; initialisation et conclusion sont notées.
- Rappel : a < b ⇒ a + c < b + c ; si k > 0, a < b ⇒ ka < kb (le sens reste).
- Rappel : si k < 0, a < b ⇒ ka > kb ; si 0 < a < b, 1/a > 1/b (le sens change).

- 3\. Hérédité, cas 1 : uₙ une fois (uₙ₊₁ = auₙ + b) : on fait à l'hypothèse × a, puis + b.
- Ex. (2016 R) : uₙ > 1 ⇒ (1/16)uₙ > 1/16 ⇒ (1/16)uₙ + 15/16 > 1, soit uₙ₊₁ > 1.
- Rappel : a > b ⇔ a − b > 0 (pour comparer, on étudie le signe de la différence).
- Rappel : même dénominateur : 4 − 6/(1 + x) = (4(1 + x) − 6)/(1 + x) = (4x − 2)/(1 + x).

- 4\. Hérédité, cas 2 : uₙ deux fois (fraction) : on étudie le signe de uₙ₊₁ − a.
- 1) même dénominateur ; 2) factoriser ; 3) signes en haut et en bas (on ne divise pas d'inégalités).
- Ex. uₙ₊₁ − 1 = (uₙ − 1)/(3uₙ + 4) > 0 car uₙ − 1 > 0 et 3uₙ + 4 > 0 : uₙ₊₁ > 1.
- 5\. Choisir : uₙ une fois → opérations ; deux fois → signe de uₙ₊₁ − a ; f croissante → VII.

- 6\. Écriture donnée uₙ₊₁ = 4 − 6/(1 + uₙ) : de 2 ≤ uₙ ≤ 4, on encadre 1 + uₙ, 1/(1 + uₙ),
- puis −6/(1 + uₙ), puis + 4 : 2 ≤ uₙ₊₁ ≤ 14/5 ≤ 4 (l'inverse et × (−6) changent le sens).
- Remarque : a < b ⇒ a ≤ b, pas l'inverse ; la conclusion recopie l'inégalité de l'énoncé.
- Ex. 2023 R : uₙ₊₁ = (uₙ − 2)/(2uₙ + 5) ; uₙ₊₁ + 1 = 3(uₙ + 1)/(2uₙ + 5) > 0, donc uₙ > −1.

### III. Majorée, minorée, bornée ; sens de variation

- 1\. Définitions : (uₙ) est majorée par M si ∀n ∈ ℕ, uₙ ≤ M ; minorée par m si ∀n ∈ ℕ, uₙ ≥ m.
- (uₙ) est bornée si elle est majorée et minorée : m ≤ uₙ ≤ M pour tout n ∈ ℕ.
- Méthode : pour uₙ < 5, signe de uₙ − 5. Ex. 5n²/(n² + 2) − 5 = −10/(n² + 2) < 0.
- Exemples : −1 ≤ (−1)ⁿ ≤ 1 et −1 ≤ cos n ≤ 1 : ces suites sont bornées.
- 2\. Croissante : ∀n, uₙ₊₁ ≥ uₙ ; décroissante : ∀n, uₙ₊₁ ≤ uₙ ; constante : ∀n, uₙ₊₁ = uₙ.
- Strictement : > ou <. Attention : comparer deux termes (u₁ > u₀) ne suffit pas.
- *[Figure (courbe) : Une suite bornée : 0 ≤ uₙ < 5 — uₙ = 5n²/(n² + 2) reste entre le plancher 0 et le plafond 5 : uₙ − 5 = −10/(n² + 2) < 0, le plafond n'est jamais atteint.]*

- 3\. Sens de variation, méthode 1 : le signe de uₙ₊₁ − uₙ.
- 1) calculer uₙ₊₁ − uₙ (souvent donné factorisé) ; 2) signe de chaque facteur (récurrence) ;
- 3) conclure : « pour tout n ∈ ℕ, uₙ₊₁ − uₙ ≤ 0, donc (uₙ) est décroissante ».
- Méthode 2 (uₙ > 0 pour tout n) : uₙ₊₁/uₙ ≤ 1 ⇒ décroissante ; uₙ₊₁/uₙ ≥ 1 ⇒ croissante.
- Attention : si uₙ < 0, multiplier par uₙ change le sens : on ne compare pas le quotient à 1.
- Méthode 3 (uₙ₊₁ = f(uₙ)) : le signe de f(x) − x, au VII.

### IV. La suite auxiliaire

- 1\. But : uₙ₊₁ = ¼uₙ + 12 ne donne pas uₙ en fonction de n ; on passe par vₙ, donnée.
- Méthode (vₙ géométrique) : 1) écrire la cible vₙ₊₁ = q × vₙ ;
- 2) vₙ₊₁ = (définition au rang n + 1), on remplace uₙ₊₁ par la relation ; 3) on simplifie.
- Ex. vₙ₊₁ = uₙ₊₁ − 1 = (1/16)uₙ + 15/16 − 1 = (1/16)(uₙ − 1) = (1/16)vₙ ; q = 1/16.
- Ex. vₙ = (uₙ − 1)/(3 − uₙ) : même dénominateur 5 − uₙ en haut et en bas ⇒ vₙ₊₁ = ½vₙ.
- Conclusion : « (vₙ) est géométrique de raison q et de premier terme v₀ ».

- 2\. Retour à uₙ : 1) v₀ ; 2) vₙ = v₀·qⁿ ; 3) isoler uₙ. Ex. uₙ = vₙ + 16 = 16 + (¼)ⁿ.
- vₙ fraction : produit en croix, uₙ d'un côté, factoriser : uₙ = (1 + 3vₙ)/(1 + vₙ).
- 3\. vₙ arithmétique : vₙ₊₁ − vₙ = r (constante) ; alors vₙ = v₀ + nr, puis on isole uₙ.

### V. Limites d'une suite

- V. 1. lim_{n→+∞} uₙ = ℓ : tout intervalle ouvert de centre ℓ contient les uₙ à partir d'un rang.
- (uₙ) est convergente si elle a une limite finie ℓ ; sinon elle est divergente.
- *[Figure (courbe) : La suite converge vers 16 — uₙ = 16 + (1/4)ⁿ : u₀ = 17, u₁ = 16,25, u₂ ≈ 16,06… les termes se serrent autour de 16 : lim uₙ = 16.]*

- 2\. Suites de référence : si α > 0, lim_{n→+∞} nᵅ = +∞ ; si α < 0, lim_{n→+∞} nᵅ = 0.
- Ex. n, n², √n → +∞ ; 1/n, 1/n², 1/√n → 0 (1/√n = n^(−1/2)).
- 3\. Limite de qⁿ (par cœur) :
- −1 < q < 1 : lim_{n→+∞} qⁿ = 0 ; q = 1 : lim_{n→+∞} qⁿ = 1 ; q > 1 : lim_{n→+∞} qⁿ = +∞.
- q ≤ −1 : (qⁿ) n'a pas de limite (ex. q = −1 : 1, −1, 1, −1…).
- Remarque : q = −1/2 : le signe alterne, mais les termes tendent vers 0.
- *[Figure (courbe) : qⁿ quand q est négatif — q = −0,5 : le signe alterne et les points se serrent sur 0, lim qⁿ = 0 ; q = −1 : 1, −1, 1… pas de limite.]*

- Méthode : « comme −1 < ¼ < 1, lim_{n→+∞} (¼)ⁿ = 0 », puis les opérations.
- Ex. lim_{n→+∞} (16 + (¼)ⁿ) = 16. Attention : la condition est −1 < q < 1, pas « q < 1 ».
- 4\. Opérations : comme pour les fonctions ; formes indéterminées : +∞ − ∞, 0 × ∞, ∞/∞, 0/0.
- On factorise par le terme dominant : 2ⁿ − 3ⁿ = 3ⁿ((2/3)ⁿ − 1) → −∞ (3 > 1).
- Fraction en n : factoriser par n en haut et en bas : (n + 1)/(n + 3) → 1.
- 5\. Si lim_{n→+∞} uₙ = a et f continue en a, alors lim_{n→+∞} f(uₙ) = f(a).
- *[Figure (croquis) : La règle de q pour lim qⁿ — q dans ]−1 ; 1[ (zone jaune) : lim qⁿ = 0 ; q > 1 : +∞ ; q = 1 : 1 ; q ≤ −1 : pas de limite.]*

### VI. Convergence et comparaison

- 1\. Croissante et majorée ⇒ convergente ; décroissante et minorée ⇒ convergente.
- Attention : croissante et minorée ne suffit pas (uₙ = n² tend vers +∞).
- Attention : majorée par M ⇒ ℓ ≤ M, mais ℓ n'est pas forcément M (on calcule ℓ ensuite).
- Passage à la limite : a ≤ uₙ ≤ b pour tout n et uₙ → ℓ ⇒ a ≤ ℓ ≤ b (< devient ≤).
- 2\. Comparaison : vₙ ≤ uₙ ≤ wₙ et vₙ → ℓ, wₙ → ℓ ⇒ lim_{n→+∞} uₙ = ℓ (gendarmes).
- |uₙ − ℓ| ≤ vₙ et vₙ → 0 ⇒ uₙ → ℓ ; uₙ ≥ vₙ et vₙ → +∞ ⇒ uₙ → +∞ (à partir d'un rang).
- *[Figure (courbe) : Le plafond n'est pas forcément la limite — La suite monte sans traverser le plafond M et se tasse sous sa limite ℓ : elle converge vers ℓ ≤ M, pas forcément vers M.]*

- 3\. Cas type 0 < uₙ₊₁ ≤ k·uₙ (0 < k < 1), ex. uₙ₊₁ = 2uₙ/(2uₙ + 5), u₀ = 3/2 :
- 1) uₙ > 0 et 2uₙ + 5 ≥ 5 ⇒ 0 < uₙ₊₁ ≤ (2/5)uₙ ;
- 2) « en déduire » : récurrence courte ⇒ 0 < uₙ ≤ (2/5)ⁿu₀ = (3/2)(2/5)ⁿ ;
- 3) −1 < 2/5 < 1 ⇒ (3/2)(2/5)ⁿ → 0 ; d'après le critère de comparaison, lim_{n→+∞} uₙ = 0.
- Attention : il faut les deux bornes (0 et le majorant) et citer le critère de comparaison.
- Écart : 0 < 2 − uₙ ≤ (1/2)(2/7)ⁿ ⇒ lim_{n→+∞} (2 − uₙ) = 0, donc lim_{n→+∞} uₙ = 2.
- *[Figure (courbe) : Coincée entre 0 et une borne qui tend vers 0 — Chaque uₙ (points) reste entre 0 et (3/2)(2/5)ⁿ (pointillés), qui tend vers 0 : par comparaison, lim uₙ = 0.]*

### VII. La suite uₙ₊₁ = f(uₙ)

- 1\. Termes sur le graphique : de uₙ on monte à (C_f), on rejoint y = x, on redescend : uₙ₊₁.
- La place de u₀ par rapport à l'intersection de (C_f) et de y = x décide : monte ou descend.
- Remarque : le dessin sert à conjecturer ; la preuve se fait par récurrence et théorèmes.
- 2\. Si f est croissante sur [a ; b] : a ≤ uₙ ≤ b ⇒ f(a) ≤ uₙ₊₁ ≤ f(b) ; on compare à a et b.
- Ex. f(x) = 2x/(x + 1), croissante sur [1 ; 2] : f(1) = 1, f(2) = 4/3, donc 1 ≤ uₙ₊₁ ≤ 2.
- f continue, strictement croissante sur I = [a ; b] ⇒ f(I) = [f(a) ; f(b)] ; ici [1 ; 4/3] ⊂ I.
- *[Figure (courbe) : L'escalier de uₙ₊₁ = f(uₙ) — De u₀ on monte à la courbe de f, on va à la droite y = x, on redescend : u₁, u₂… les marches se tassent vers (1 ; 1).]*

- 3\. Méthode 3 : uₙ ∈ I pour tout n, f(x) ≤ x sur I ⇒ uₙ₊₁ ≤ uₙ : décroissante (≥ : croissante).
- 4\. (uₙ) convergente, f continue sur I (car dérivable), f(I) ⊂ I, u₀ ∈ I ⇒ ℓ = f(ℓ), ℓ ∈ I.
- Puis on résout f(x) = x dans I : x = 0 ou x = 1 ; 0 ∉ [1 ; 2], donc ℓ = 1.
- National : g(x) = (4x + 3)/(x + 2), u₀ = 1, 1 ≤ uₙ ≤ 3 ; g(x) − x = (3 − x)(x + 1)/(x + 2).
- g(x) − x ≥ 0 sur [1 ; 3] ⇒ (uₙ) croissante ; majorée par 3 ⇒ convergente.
- g(I) = [g(1) ; g(3)] = [7/3 ; 3] ⊂ I ; g(x) = x ⇔ x = −1 ou x = 3 ; −1 ∉ I ⇒ ℓ = 3.
- *[Figure (variations) : Variations de g sur I = [1 ; 3] — g′(x) = 5/(x + 2)² > 0 : g croît de g(1) = 7/3 à g(3) = 3, donc g(I) = [7/3 ; 3] ⊂ I.]*

### VIII. Problèmes : rang, somme ; un exercice national question par question

- 1\. Plus petit rang : remplacer uₙ par sa formule, résoudre, prendre le plus petit entier n.
- Ex. (n + 1)/(n + 3) ≥ 0,99 ⇔ n + 1 ≥ 0,99n + 2,97 ⇔ n ≥ 197 (dénominateur > 0).
- 2\. uₖ = 1 + vₖ, (vₖ) géométrique : on sépare les 1 (n + 1 termes) et les vₖ :
- u₀ + … + uₙ = (n + 1) + (v₀ + … + vₙ) = (n + 1) + v₀(1 − qⁿ⁺¹)/(1 − q).
- 3\. Si −1 < q < 1 : Sₙ = w₀ + … + wₙ = w₀(1 − qⁿ⁺¹)/(1 − q) → w₀/(1 − q).
- Ex. w₀ = 1, q = 1/2 : lim_{n→+∞} Sₙ = 1/(1 − 1/2) = 2.

- 4\. National 2024 : u₀ = 4, uₙ₊₁ = (4uₙ − 2)/(uₙ + 1).
- 1) uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ + 1) ≥ 0 et uₙ₊₁ − 4 = −6/(uₙ + 1) < 0 ⇒ 2 ≤ uₙ ≤ 4.
- 2) uₙ₊₁ − uₙ = −(uₙ − 1)(uₙ − 2)/(uₙ + 1) ≤ 0 : décroissante ; 3) minorée par 2 ⇒ convergente.
- 4) vₙ = (uₙ − 2)/(uₙ − 1) : vₙ₊₁ = (2/3)vₙ, v₀ = 2/3 ; 5) vₙ = (2/3)ⁿ⁺¹, uₙ = (2 − vₙ)/(1 − vₙ).
- −1 < 2/3 < 1 ⇒ lim_{n→+∞} vₙ = 0 ⇒ lim_{n→+∞} uₙ = (2 − 0)/(1 − 0) = 2.
- *[Figure (courbe) : National 2024 : uₙ descend vers 2 — Décroissante (Q2) et minorée par 2 (Q1) : (uₙ) converge ; sa limite est 2 (Q5).]*

### IX. Bilan du chapitre

- À encadrer : uₙ = uₚ + (n − p)r ; uₙ = uₚ·qⁿ⁻ᵖ ; les deux sommes (q ≠ 1) ; la limite de qⁿ.
- Récurrence : Initialisation ; Hérédité (soit n, supposons…, montrons…) ; Conclusion.
- Convergence : le bon couple (monotone et bornée) ; comparaison ; ℓ = f(ℓ) et ses conditions.
- Carte : récurrence → sens de variation → convergence → suite auxiliaire → limite.

## Méthodes des cas types du national (où elles sont écrites)

| Cas type (fréquence 2016-2025) | Dans le cahier |
|---|---|
| Calculer u₁, u₂ (2 sujets) | I.2 (suite récurrente) |
| Vérifier une écriture donnée de uₙ₊₁ (8) | II.6 (écriture donnée, encadrement pas à pas) |
| Récurrence, uₙ₊₁ = auₙ + b (2016 R, 2017 R) | II.2 rédaction type + II.3 hérédité cas 1 |
| Récurrence, suite homographique (10) | II.4 hérédité cas 2 (méthode 1)-2)-3)), ex. 2023 R ; VIII.4 question 1 |
| Récurrence, f croissante sur [a ; b] (10) | VII.2 (encadrement par f, f(I) ⊂ I) |
| Monotonie par uₙ₊₁ − uₙ (7) | III.3 méthode 1, étapes 1)-2)-3) ; VIII.4 question 2 |
| Monotonie par uₙ₊₁/uₙ (1) | III.3 méthode 2 (uₙ > 0) |
| Monotonie par f(x) − x (10) | VII.3 méthode 3 ; exemple national g |
| En déduire la convergence (17) | VI.1 le bon couple ; VIII.4 question 3 |
| Suite auxiliaire géométrique (8) | IV.1 méthode 1)-2)-3), IV.2 retour à uₙ ; VIII.4 questions 4-5 |
| Suite auxiliaire arithmétique (3) | IV.3 |
| Limite par qⁿ (10) | V.3 + méthode « comme −1 < q < 1 » ; VIII.4 question 5 |
| Majoration kⁿ puis comparaison (3) | VI.3 étapes 1)-2)-3) |
| uₙ₊₁ = f(uₙ), ℓ = f(ℓ) (10) | VII.4 (conditions, résoudre, garder la solution de I) |
| Limite de f(uₙ) (1) | V.5 |
| Plus petit rang (2) | VIII.1 |
| Somme de termes et sa limite (2) | I.5, VIII.2, VIII.3 |

## Découpage

### Copie en attente (`en_attente/math_ch3_suites_numeriques.json`)

| Bloc | Diapositives | Parties ouvertes | Lignes | Début des lignes | Figure |
|---|---|---|---|---|---|
| `su_n1_b1` | 3 | I | 5 | Plan d'un exercice  / 1. Définition  / Premier terme  / Attention  / Exemple  | — |
| `su_n1_b2` | 4 | — | 6 | 2. Suite explicite uₙ = f(n) / Suite récurrente  / 3. Suite arithmétique de rai / Méthode  / Terme général  / Exemple  | Suite arithmétique : des pas égaux |
| `su_n1_b3` | 3 | — | 5 | Rappel  / 4. Suite géométrique de rais / Méthode  / Terme général  / Vérification avec n = 0  | — |
| `su_n1_b4` | 3 | — | 6 | 5. Nombre de termes de uₚ à  / Somme arithmétique  / uₚ + … + uₙ = (n − p + 1)(uₚ / Somme géométrique (q ≠ 1)  / En particulier, pour q ≠ 1  / Attention  | — |
| `su_n2_b1` | 3 | II | 4 | 1. Principe (dominos)  / 2. Rédaction type  / Initialisation  / Hérédité  | — |
| `su_n2_b2` | 3 | — | 4 | Conclusion  / Attention  / Rappel  / Rappel  | — |
| `su_n2_b3` | 3 | — | 4 | 3. Hérédité, cas 1  / Ex. (2016 R)  / Rappel  / Rappel  | — |
| `su_n2_b4` | 3 | — | 4 | 4. Hérédité, cas 2  / 1) même dénominateur ; 2) fa / Ex. uₙ₊₁ − 1 = (uₙ − 1)/(3uₙ / 5. Choisir  | — |
| `su_n3_b1` | 3 | — | 4 | 6. Écriture donnée uₙ₊₁ = 4  / puis −6/(1 + uₙ), puis + 4  / Remarque  / Ex. 2023 R  | — |
| `su_n3_b2` | 3 | III | 6 | 1. Définitions  / (uₙ) est bornée si elle est  / Méthode  / Exemples  / 2. Croissante  / Strictement  | Une suite bornée : 0 ≤ uₙ < 5 |
| `su_s3_b1` | 3 | — | 6 | 3. Sens de variation, méthod / 1) calculer uₙ₊₁ − uₙ (souve / 3) conclure  / Méthode 2 (uₙ > 0 pour tout  / Attention  / Méthode 3 (uₙ₊₁ = f(uₙ))  | — |
| `su_s3_b2` | 3 | IV | 6 | 1. But  / Méthode (vₙ géométrique)  / 2) vₙ₊₁ = (définition au ran / Ex. vₙ₊₁ = uₙ₊₁ − 1 = (1/16) / Ex. vₙ = (uₙ − 1)/(3 − uₙ)  / Conclusion  | — |
| `su_s3_b3` | 4 | V | 5 | 2. Retour à uₙ  / vₙ fraction  / 3. vₙ arithmétique  / V. 1. lim_{n→+∞} uₙ = ℓ  / (uₙ) est convergente si elle | La suite converge vers 16 |
| `su_s4_b1` | 4 | — | 6 | 2. Suites de référence  / Ex. n, n², √n → +∞ ; 1/n, 1/ / 3. Limite de qⁿ (par cœur)  / −1 < q < 1  / q ≤ −1  / Remarque  | qⁿ quand q est négatif |
| `su_s4_b2` | 5 | — | 6 | Méthode  / Ex. lim_{n→+∞} (16 + (¼)ⁿ) = / 4. Opérations  / On factorise par le terme do / Fraction en n  / 5. Si lim_{n→+∞} uₙ = a et f | La règle de q pour lim qⁿ |
| `su_s4_b3` | 4 | VI | 6 | 1. Croissante et majorée ⇒ c / Attention  / Attention  / Passage à la limite  / 2. Comparaison  / |uₙ − ℓ| ≤ vₙ et vₙ → 0 ⇒ uₙ | Le plafond n'est pas forcément la limite |
| `su_s5_b1` | 4 | — | 6 | 3. Cas type 0 < uₙ₊₁ ≤ k·uₙ  / 1) uₙ > 0 et 2uₙ + 5 ≥ 5 ⇒ 0 / 2) « en déduire »  / 3) −1 < 2/5 < 1 ⇒ (3/2)(2/5) / Attention  / Écart  | Coincée entre 0 et une borne qui tend vers 0 |
| `su_s5_b2` | 3 | VII | 6 | 1. Termes sur le graphique  / La place de u₀ par rapport à / Remarque  / 2. Si f est croissante sur [ / Ex. f(x) = 2x/(x + 1), crois / f continue, strictement croi | L'escalier de uₙ₊₁ = f(uₙ) |
| `su_s5_b3` | 5 | — | 6 | 3. Méthode 3  / 4. (uₙ) convergente, f conti / Puis on résout f(x) = x dans / National  / g(x) − x ≥ 0 sur [1 ; 3] ⇒ ( / g(I) = [g(1) ; g(3)] = [7/3  | Variations de g sur I = [1 ; 3] |
| `su_s6_b1` | 3 | VIII | 6 | 1. Plus petit rang  / Ex. (n + 1)/(n + 3) ≥ 0,99 ⇔ / 2. uₖ = 1 + vₖ, (vₖ) géométr / u₀ + … + uₙ = (n + 1) + (v₀  / 3. Si −1 < q < 1  / Ex. w₀ = 1, q = 1/2  | — |
| `su_n8_b1` | 6 | — | 5 | 4. National 2024  / 1) uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ  / 2) uₙ₊₁ − uₙ = −(uₙ − 1)(uₙ  / 4) vₙ = (uₙ − 2)/(uₙ − 1)  / −1 < 2/3 < 1 ⇒ lim_{n→+∞} vₙ | National 2024 : uₙ descend vers 2 |
| `su_n8_b2` | 2 | IX | 4 | À encadrer  / Récurrence  / Convergence  / Carte  | — |

### Cours en ligne (`math_ch3_suites_numeriques.json`)

| Bloc | Diapositives | Parties ouvertes | Lignes | Début des lignes | Figure |
|---|---|---|---|---|---|
| `su_s0_b1` | 4 | I | 5 | Plan d'un exercice  / 1. Rappels. Puissances  / Inégalités  / Attention  / Exemple  | — |
| `su_s0_b2` | 4 | — | 6 | Comparer  / Même dénominateur  / 2. Définition  / Premier terme  / Attention  / Exemple  | — |
| `su_s1_b2` | 4 | — | 6 | 3. Suite explicite uₙ = f(n) / Suite récurrente  / 4. Suite arithmétique de rai / Méthode  / Terme général  / Exemple  | Suite arithmétique : des pas égaux |
| `su_s1_b3` | 3 | — | 5 | 5. Suite géométrique de rais / Méthode  / Terme général  / Vérification avec n = 0  / 6. Nombre de termes de uₚ à  | — |
| `su_s1_b4` | 2 | — | 5 | Somme arithmétique  / uₚ + … + uₙ = (n − p + 1)(uₚ / Somme géométrique (q ≠ 1)  / En particulier, pour q ≠ 1  / Attention  | — |
| `su_s2_b1` | 4 | II | 6 | 1. Principe (dominos)  / 2. Rédaction type  / Initialisation  / Hérédité  / Conclusion  / Attention  | — |
| `su_s2_b1b` | 3 | — | 5 | 3. Hérédité, cas 1  / Ex. (2016 R)  / 4. Hérédité, cas 2  / 1) même dénominateur ; 2) fa / Ex. uₙ₊₁ − 1 = (uₙ − 1)/(3uₙ | — |
| `su_s2_b2` | 4 | — | 5 | 5. Choisir  / 6. Écriture donnée uₙ₊₁ = 4  / puis −6/(1 + uₙ), puis + 4  / Remarque  / Ex. 2023 R  | — |
| `su_s2_b3` | 3 | III | 6 | 1. Définitions  / (uₙ) est bornée si elle est  / Méthode  / Exemples  / 2. Croissante  / Strictement  | Une suite bornée : 0 ≤ uₙ < 5 |
| `su_s3_b1` | 3 | — | 6 | 3. Sens de variation, méthod / 1) calculer uₙ₊₁ − uₙ (souve / 3) conclure  / Méthode 2 (uₙ > 0 pour tout  / Attention  / Méthode 3 (uₙ₊₁ = f(uₙ))  | — |
| `su_s3_b2` | 3 | IV | 6 | 1. But  / Méthode (vₙ géométrique)  / 2) vₙ₊₁ = (définition au ran / Ex. vₙ₊₁ = uₙ₊₁ − 1 = (1/16) / Ex. vₙ = (uₙ − 1)/(3 − uₙ)  / Conclusion  | — |
| `su_s3_b3` | 4 | V | 5 | 2. Retour à uₙ  / vₙ fraction  / 3. vₙ arithmétique  / V. 1. lim_{n→+∞} uₙ = ℓ  / (uₙ) est convergente si elle | La suite converge vers 16 |
| `su_s4_b1` | 4 | — | 6 | 2. Suites de référence  / Ex. n, n², √n → +∞ ; 1/n, 1/ / 3. Limite de qⁿ (par cœur)  / −1 < q < 1  / q ≤ −1  / Remarque  | qⁿ quand q est négatif |
| `su_s4_b2` | 5 | — | 6 | Méthode  / Ex. lim_{n→+∞} (16 + (¼)ⁿ) = / 4. Opérations  / On factorise par le terme do / Fraction en n  / 5. Si lim_{n→+∞} uₙ = a et f | La règle de q pour lim qⁿ |
| `su_s4_b3` | 4 | VI | 6 | 1. Croissante et majorée ⇒ c / Attention  / Attention  / Passage à la limite  / 2. Comparaison  / |uₙ − ℓ| ≤ vₙ et vₙ → 0 ⇒ uₙ | Le plafond n'est pas forcément la limite |
| `su_s5_b1` | 4 | — | 6 | 3. Cas type 0 < uₙ₊₁ ≤ k·uₙ  / 1) uₙ > 0 et 2uₙ + 5 ≥ 5 ⇒ 0 / 2) « en déduire »  / 3) −1 < 2/5 < 1 ⇒ (3/2)(2/5) / Attention  / Écart  | Coincée entre 0 et une borne qui tend vers 0 |
| `su_s5_b2` | 3 | VII | 6 | 1. Termes sur le graphique  / La place de u₀ par rapport à / Remarque  / 2. Si f est croissante sur [ / Ex. f(x) = 2x/(x + 1), crois / f continue, strictement croi | L'escalier de uₙ₊₁ = f(uₙ) |
| `su_s5_b3` | 4 | — | 6 | 3. Méthode 3  / 4. (uₙ) convergente, f conti / Puis on résout f(x) = x dans / National  / g(x) − x ≥ 0 sur [1 ; 3] ⇒ ( / g(I) = [g(1) ; g(3)] = [7/3  | Variations de g sur I = [1 ; 3] |
| `su_s6_b1` | 3 | VIII | 6 | 1. Plus petit rang  / Ex. (n + 1)/(n + 3) ≥ 0,99 ⇔ / 2. uₖ = 1 + vₖ, (vₖ) géométr / u₀ + … + uₙ = (n + 1) + (v₀  / 3. Si −1 < q < 1  / Ex. w₀ = 1, q = 1/2  | — |
| `su_s6_b2` | 3 | IX | 6 | 4. National 2024  / 1) uₙ₊₁ − 2 = 2(uₙ − 2)/(uₙ  / 2) uₙ₊₁ − uₙ = −(uₙ − 1)(uₙ  / 4) vₙ = (uₙ − 2)/(uₙ − 1)  / −1 < 2/3 < 1 ⇒ lim_{n→+∞} vₙ / IX. Carte  | National 2024 : uₙ descend vers 2 |

Limite du rendu : `TableauCahier` écrit les titres de partie entrés dans un bloc EN TÊTE du bloc, pas à la ligne où la partie commence. Deux blocs sont concernés : `su_s3_b3` (fin de IV, début de V : la ligne du V commence donc par « V. 1. ») et, dans le cours en ligne, `su_s6_b2` (fin de VIII, ligne « IX. Carte »).

Différences du cours en ligne : la partie I s'ouvre sur les rappels (`I.1 Rappels` : puissances, inégalités, différence,
même dénominateur), puis 2. Définition, 3. Suite explicite, 4. Arithmétique, 5. Géométrique, 6. Nombre de termes et
sommes ; la partie II n'a donc plus ses « Rappel : » et numérote 1. Principe, 2. Rédaction, 3. Hérédité cas 1,
4. cas 2, 5. Choisir, 6. Écriture donnée. Le dernier bloc (`su_s6_b2`) porte l'exercice national 2024 en entier
(diapositive unique `su_e1_complet`) et la ligne « Carte » du bilan ; la figure `Variations de g` est sur
`su_f7_national` (sur `su_f7b_limite` dans la copie en attente) et la figure du national 2024 sur `su_e1_complet`
(sur `su_e1_q3` dans la copie en attente).

Bulles des diapositives (`concentration.cahier`) : une chaîne d'une à deux lignes par diapositive, la trace de cette
diapositive (dictionnaire `SLIDES` du script ; `su_e1_complet` et `su_f7_national` diffèrent entre les deux fichiers).
Figures de diapositive : `su_a4_arithmetique`, `su_b2_bornee`, `su_l1_converge`, `su_l4_qn_negatif` (nouvelle),
`su_l4b_glisse_q`, `su_c3_plafond_limite`, `su_c7_conclure`, `su_f1_escalier`, + `Variations de g` (nouvelle) et
`National 2024 : uₙ descend vers 2` (nouvelle).
