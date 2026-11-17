## Suites numériques

Copie en attente : `backend/data/courses/en_attente/math_ch3_suites_numeriques.json`. Il n'y avait pas de copie en attente, donc je suis parti du cours en ligne. Le cours en ligne n'a pas été modifié. Script : `scratchpad/corr3/apply_ch3.py`.

### Manques corrigés

| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Prouver f(I) ⊂ I en calculant f(I) = [f(a) ; f(b)] (haute) | Écrit : « f continue et strictement croissante sur [1 ; 2], donc f([1 ; 2]) = [f(1) ; f(2)] = [1 ; 4/3] ⊂ [1 ; 2] ». Même chose pour g : g(I) = [7/3 ; 3] ⊂ [1 ; 3]. La voix de su_f5 le dit aussi | su_f3, su_f5, su_f7, su_e2 (point 8), blocs su_s5_b2 et su_s5_b3 |
| Justifier la continuité par « car » (haute) | « f est continue sur I car elle est dérivable sur I (fonction rationnelle, x + 1 ≠ 0) », à l'écran, au cahier et dans la voix de su_f5 | su_f5, su_f7, su_e2, bloc su_s5_b3 |
| **Piste haute** : passage à la limite dans une inégalité | a ≤ uₙ ≤ b ⇒ a ≤ ℓ ≤ b, et ⚠ « le strict devient large » (1/n > 0, lim 1/n = 0). Écran, centre, cahier, voix. C'est maintenant la raison écrite de « ℓ ∈ I » | su_c3, su_f6, su_e2 (point 7), blocs su_s4_b3 et su_s5_b3, démonstration fin de cours su_c2 |
| Opérations sur les limites et 4 formes indéterminées (moyenne) | **Nouvelle diapo** su_l5b_formes_indeterminees, placée après su_l5 : mêmes règles que pour les fonctions (exemple −5 × 4ⁿ → −∞) ; « +∞ − ∞ », « 0 × ∞ », « ∞/∞ », « 0/0 ». Elle a sa voix (deux explications), son centre, son pointage, son cahier, le bloc su_s4_b2 et la compétence K5 | su_l5b (nouvelle) |
| Forme indéterminée avec deux puissances (moyenne) | Dans la nouvelle diapo : 2ⁿ − 3ⁿ = 3ⁿ((2/3)ⁿ − 1) → −∞, avec chaque condition écrite. Le calcul faux de Benmoussa n'est pas repris | su_l5b |
| Comparaison version −∞, « à partir d'un certain rang » (moyenne) | Écran, centre, cahier, voix | su_c4, bloc su_s4_b3 |
| Strictement croissante / décroissante, constante (moyenne) | Écran, centre, cahier, voix (avec ∀n) | su_m1, bloc su_s2_b3, su_e2 (point 4) |
| « géométrique de raison q et de premier terme v₀ » (moyenne) | Écrit au cahier et dans les démonstrations (v₀ = 2/3 au national 2024) | su_x2, bloc su_s3_b2, su_e1 (question et exercice) |
| « n → +∞ » sous lim (moyenne) | `lim_{n→+∞}` écrit partout : écran, centre, cahier, démonstrations et cahiers des blocs (100 endroits). La fiche et la carte (simulations) ne sont pas touchées | tout le cours |
| Définition par intervalles (basse) | Une ligne : « tout intervalle ouvert de centre ℓ contient tous les termes à partir d'un certain rang » | su_l1 |
| lim uₙ = −∞ ⇔ lim (−uₙ) = +∞ (basse) | Écrit | su_l1, bloc su_s3_b3 |
| Exemples (−1)ⁿ, cos n, (−1)ⁿ/n, n² + (−1)ⁿ (basse) | Écrits | su_b2, su_c4, bloc su_s2_b3 |
| Polynôme : la limite du terme de plus haut degré (basse, en partie) | n² − 5n + 1 = n²(1 − 5/n + 1/n²) → +∞ | su_l6 |
| Notation Σ (basse, en partie) | « uₚ + … + uₙ = Σ uₖ (k allant de p à n) » | su_a9 |
| Notation (uₙ)ₙ≥ₙ₀ (basse, à monter) | (uₙ)ₙ≥₁, (uₙ)ₙ∈ℕ*, (uₙ)ₙ≥ₚ | su_a1, bloc su_s0_b2 |
| Montrer ∀ une fois (notation) | « pour tout n ∈ ℕ (∀n ∈ ℕ) » | su_b1, su_m1, bloc su_s2_b3 |
| « Théorème des gendarmes » à l'écran (notation) | « Critère de comparaison (théorème des gendarmes) » | su_c4, démonstration su_c4, bloc su_s4_b3 |
| Somme géométrique en symboles (notation) | uₚ(1 − qⁿ⁻ᵖ⁺¹)/(1 − q) et 1 + q + … + qⁿ = (1 − qⁿ⁺¹)/(1 − q) | su_a9b, bloc su_s1_b4 |
| Dit seulement à l'oral (6 points) | Écrits : 1/√n = n^(−1/2) ; points isolés ; vérifier avec n = 0 ; uₙ = 2 + 3n ; uₙ₊₁ = 2uₙ, raison 2 ; « sans une condition, la réponse n'est pas acceptée » | su_l2, su_b1, su_a7, su_a5, su_a6, su_f5 |
| Skill « Formulas » | Les barres « a / b » des explications et des réactions des rappels sont réécrites « a/b » | su_e1 (exercice), bloc su_s6_b2, rappels K4 et K5 |

### Non corrigés et pourquoi

- **Deux solutions de f(x) = x dans I** (haute) : propre au Prof Fayssal, et le cadre ne l'exige pas. Le passage à la limite, maintenant écrit, donne l'outil pour ce cas.
- **De uₙ ≤ 2 − 1/n, majorée par une constante** (basse) : aucun autre professeur ne l'écrit.
- **Nouvelles pistes moyennes et basses** : non traitées, comme demandé. C'est le cas de « convergente ⇒ bornée », « croissante non majorée ⇒ +∞ », unicité de la limite, lim |uₙ|, somme pour q = 1, trois termes consécutifs, limite candidate, ⁷√(n³).
- **Simulations non modifiées** (on ne touche pas au frontend) :
  - La fiche `bilan.html` n'a pas les nouvelles lignes : seuls les bullets de su_e2 sont à jour.
  - Le tableau `gendarmes.html` ne montre pas le cas −∞.
  - La nouvelle diapo réutilise `qn.html?vue=positif` comme rappel (qⁿ → +∞ si q > 1, → 0 si 0 < q < 1). Ce ne sont pas ses exemples (4ⁿ, (2/3)ⁿ).
- **À décider** : le bloc su_s4_b2 a maintenant 5 diapos (l4b, l5, l5b, l6, l7) au lieu de 3–4. Pour revenir à 3–4, il faut créer un nouveau bloc, avec son cahier, son « retrouver » et son exercice.
- **Skill** : les règles 37 et 38 et l'étape 9b sont déjà dans `professeur` et `cours-concentration`. Rien n'a été ajouté.

### Démonstrations

- **33 relues**, dont 4 ajoutées là où une question qui demande un raisonnement n'en avait pas : su_l4c (question), blocs su_s2_b1b, su_s4_b3 et su_s6_b2.
- **28 réécrites**, lignes et parole, audio retiré. Elles ont 9 lignes au plus (su_f7). Tout est vérifié avec sympy.
- 1 est restée telle quelle : l'exercice du bloc su_s3_b2.
- L'incohérence « question 2 » de su_m4 a disparu.

Trois exemples :
- su_a9b : « 1 × (1 − 2¹¹)/(1 − 2) = 2¹¹ − 1 = 2047 » → raison et premier terme, 11 termes, 2¹¹ = 2048, 1 − 2 = −1, (−2047)/(−1) = 2047.
- su_e1 : « uₙ = (2 − vₙ)/(1 − vₙ) = 1 + 1/(1 − (2/3)ⁿ⁺¹) » → on part de v₀, puis « de premier terme 2/3 », produit en croix, regroupement, factorisation, 2 − vₙ = (1 − vₙ) + 1, la condition, et enfin lim = 2.
- Bloc su_s5_b3 : « ℓ² − ℓ − 2 = 0 → ℓ = 2 ou −1 » → les conditions de ℓ = f(ℓ), ℓ ≥ 0 avant d'élever au carré, Δ = 9, les deux racines, −1 ∉ [0 ; 2].

### Voix à enregistrer

- **Diapos dont la voix change (4)** : su_m1_pour_tout_n, su_c3_plafond_limite, su_c4_comparaison, su_f5_conditions.
- **Nouvelle diapo (1)** : su_l5b_formes_indeterminees.
- **Démonstrations (32)** :
  - questions et exercices des diapos : su_z3 q, su_a5 q, su_a9b q, su_r4b q, su_r8 q, su_m4 q, su_x3 q, su_l4c q (nouvelle), su_l7 q, su_c4 q, su_c8 q, su_f3 q, su_f7 q, su_p3 q, su_e1 q, su_e1 e0 ;
  - exercice de fin de cours : su_c2 n°0 ;
  - exercices des blocs : su_s1_b2, su_s1_b3, su_s1_b4, su_s2_b1b (nouvelle), su_s2_b2, su_s3_b1, su_s3_b3, su_s4_b1, su_s4_b2, su_s4_b3 (nouvelle), su_s5_b1, su_s5_b2, su_s5_b3, su_s6_b1, su_s6_b2 (nouvelle).
- **Réactions** : aucune nouvelle (la nouvelle diapo ne pose pas de question).

### Vérifications faites

- `json.load` : OK. Fins de ligne LF (0 CR) ; écrit avec `ensure_ascii=False, indent=2`.
- Script de vérification (71 diapos, 33 démonstrations) : **0 erreur**. Il vérifie que chaque « mot » de démonstration est dans sa parole et dans l'ordre, que chaque mot de pointage et de centre est dans `speech_text.mixed`, et qu'il n'y a ni chiffre ni symbole dans les voix et paroles sans audio. Il vérifie aussi que chaque diapo est dans exactement un bloc, que les blocs suivent l'ordre du cours et que les compétences existent.
- `verifier_figures_cahier.py` : 7 figures, **0 erreur, 0 avertissement**.
- sympy : tous les calculs sont justes.
  - Suites et sommes : uₙ₊₁ − 1 = (uₙ − 1)/(3uₙ + 4) ; uₙ₊₁ + 1 = 3(uₙ + 1)/(2uₙ + 5) ; vₙ₊₁ = (1/2)vₙ (x3) ; somme = 2047 ; somme = 93 ; u₄ = 48 ; u₁₀ = 31.
  - Fonctions f et g : g(x) − x = (3 − x)(x + 1)/(x + 2), g′ = 5/(x + 2)², g(1) = 7/3, g(3) = 3 ; f′ = 2/(x + 1)², f(2) = 4/3.
  - Limites : lim Sₙ = 3/2 ; uₙ = 1 + 1/(1 − (2/3)ⁿ⁺¹) → 2 ; 2ⁿ − 3ⁿ → −∞ ; −5·4ⁿ → −∞ ; 3¹⁰ = 59049 ; (2n + 1)/(n + 5) → 2 ; √(ℓ + 2) = ℓ ⇒ ℓ = 2.
  - Autres : (n + 1)² + (n + 1) − (n² + n) = 2n + 2 ; plus petit rang = 99 ; uₙ − 5 = −10/(n² + 2).
