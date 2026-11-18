# Cahier de l'élève — `math_ch5_fonctions_ln` (Fonctions logarithmiques)

18 novembre 2026. Le cahier idéal du chapitre, d'un seul tenant, tel que l'élève l'a recopié bloc après bloc. Les
parties I à XI sont celles du cours (`activities[].title`, que l'écran affiche déjà en tête de bloc) ; dans les blocs,
la première ligne de chaque partie porte son numéro romain (« II. 3. … »), parce qu'un bloc peut finir une partie et en
commencer une autre. Les rappels ne sont pas numérotés (« Rappel : »). Les bulles des diapositives
(`concentration.cahier`) sont la trace d'une seule diapositive, sans numéro (l'écran numérote déjà le titre de la diapo).
Application : `appliquer.py` (répertoire de travail de l'agent, hors dépôt). Formules écrites pour `Formule.tsx` :
fractions parenthésées dès qu'un membre a une espace (« (ln x)/(ln 10) », « (2 ln x)/x »), « lim_{x→0⁺} ».

---

## Ouverture — rappels

- Ce chapitre : la fonction ln, définie sur ]0 ; +∞[, qui transforme un produit en somme.
- Rappel : F est une primitive de f sur I ⇔ F′(x) = f(x) pour tout x de I. Exemple : x² et x² + 3 sont des primitives de 2x.
- Rappel : xⁿ × xᵐ = xⁿ⁺ᵐ ; x⁰ = 1 ; x⁻¹ = 1/x ; x⁻ⁿ = 1/xⁿ ; √x = x^(1/2) (x > 0).
- Rappel : ax + b (a ≠ 0) s'annule en −b/a : signe de a après la racine, contraire avant. Exemple : x − 1 : − | 0 | +.
- Rappel : multiplier ou diviser une inégalité par un nombre négatif change son sens : −2x > 4 ⇔ x < −2.
- Rappel : ax² + bx + c = 0 : Δ = b² − 4ac ; si Δ > 0, x = (−b ± √Δ)/(2a). Exemple : x² + x − 6 = 0 ⇔ x = 2 ou x = −3.

## I. La naissance de ln : la primitive de 1/x qui s'annule en 1

1. **Pourquoi ln** : la règle xⁿ → xⁿ⁺¹/(n + 1) échoue pour n = −1 (division par 0) ; aucune fonction connue n'a pour
   dérivée x ↦ 1/x. Or x ↦ 1/x est continue sur ]0 ; +∞[ : elle y admet des primitives, F + k (k ∈ ℝ).
2. **Définition** : la fonction logarithme népérien, notée ln, est la primitive de x ↦ 1/x sur ]0 ; +∞[ qui s'annule
   en 1. Notation : ln : ]0 ; +∞[ → ℝ, x ↦ ln x ; ln x n'existe que pour x > 0.
3. **Conséquences** : ln 1 = 0 ; ln est dérivable sur ]0 ; +∞[ et (ln x)′ = 1/x.

## II. La courbe de ln : croissance, signe, e, tangente

1. Pour x > 0, (ln x)′ = 1/x > 0 : ln est strictement croissante sur ]0 ; +∞[.
2. **Signe** : 0 < x < 1 ⇔ ln x < 0 ; ln 1 = 0 ; x > 1 ⇔ ln x > 0. *(figure : « Le signe de ln x »)*
3. **Le nombre e** : ln est continue, strictement croissante, et ln 2 < 1 < ln 3 ; donc ln x = 1 a une unique solution,
   notée e : ln e = 1 (e ≈ 2,718, irrationnel).
4. **Comparer** (a > 0, b > 0) : ln a = ln b ⇔ a = b ; ln a < ln b ⇔ a < b.
5. **Tangente en 1** : y = ln′(1)(x − 1) + ln 1, soit (T) : y = x − 1.
   Remarque : la courbe de ln est sous (T) : ln x ≤ x − 1 (démontré au IX). *(figure : « le nombre e et la tangente en 1 »)*

## III. L'ensemble de définition : u(x) > 0

1. **Domaine** : ln(u(x)) existe ⇔ u(x) > 0 ; on écrit x ∈ D_f ⇔ u(x) > 0.
   Exemple : f(x) = ln(2x − 6) : 2x − 6 > 0 ⇔ x > 3, donc D_f = ]3 ; +∞[.
2. **Quotient dans ln** : tableau de signe ; on garde les x où il est > 0.
   Exemple : ln(5x/(3 − x)) : 5x/(3 − x) > 0 ⇔ 0 < x < 3, donc D_f = ]0 ; 3[.
3. **Plusieurs conditions** : on les relie par « et » (intersection), jamais par « ou ».
   Exemple : (1 + ln x)/(ln x) : x > 0 et ln x ≠ 0 ⇔ x ≠ 1 ; D_f = ]0 ; 1[ ∪ ]1 ; +∞[.
4. ln|u(x)| existe ⇔ u(x) ≠ 0 ; ln(u(x)) demande u(x) > 0. Exemple : ln|x − 2| : x ≠ 2.

## IV. Les règles de calcul (a > 0, b > 0)

1. **Produit** : ln(ab) = ln a + ln b. Exemple : ln 6 = ln 2 + ln 3.
   Preuve : (ln(ax))′ = a/(ax) = 1/x = (ln x)′, et en x = 1 l'écart vaut ln a ; donc ln(ax) = ln a + ln x : la courbe
   de ln(ax) est celle de ln montée de ln a. *(figure : « ln(2x) = ln 2 + ln x »)*
2. **Inverse et quotient** : ln(1/a) = −ln a ; ln(a/b) = ln a − ln b. Exemple : ln(1/2) = −ln 2 ≈ −0,69.
3. **Puissance et racine** : ln(aⁿ) = n ln a (n ∈ ℤ) ; ln(aʳ) = r ln a (r ∈ ℚ) ; ln √a = ½ ln a.
   Exemple : ln(1/8) = −3 ln 2 ; ln(√2 × 8) = (7/2) ln 2.
4. **Méthode (simplifier)** : 1) décomposer en facteurs premiers ; 2) appliquer les règles ; 3) regrouper les ln 2, les ln 3.
   Exemple : ln 12 − ln 27 + ln √2 = (5/2) ln 2 − 2 ln 3.
5. **Les pièges**
   - Attention : ln(a + b) ≠ ln a + ln b (ln 2 ≠ ln 1 + ln 1 = 0).
   - Attention : pour x ≠ 0, ln(x²) = 2 ln|x| ; ln(x²) = 2 ln x seulement si x > 0.
   - Attention : le coefficient devant ln multiplie tous les termes : 3 ln 36 = 6 ln 2 + 6 ln 3.
   - Exemple : ln 16 − ln 27 + 3 ln 36 − ln √2 = (19/2) ln 2 + 3 ln 3.
6. **ln(eʳ) = r ln e = r** : eʳ est le nombre dont le ln vaut r. Exemple : ln(e²) = 2 ; ln(1/e) = −1 ; ln √e = ½.

## V. Équations, inéquations, systèmes

1. **Méthode (équation)** : 1) D_E, l'ensemble où chaque ln existe ; 2) se ramener à ln a = ln b ⇔ a = b (a > 0,
   b > 0) ; 3) garder les solutions de D_E et conclure S = {…}.
   Exemple : ln(x − 1) + ln(x + 2) = ln 4 : D_E = ]1 ; +∞[ ; x = 2 ou x = −3 ; S = {2}.
2. **ln x = r ⇔ x = eʳ** (car r = ln eʳ). Exemple : ln(2x − 1) = 1 ⇔ x = (1 + e)/2.
3. **Inéquation** : ln a < ln b ⇔ a < b (a > 0, b > 0) : ln garde le sens.
   Méthode : D_I d'abord ; on écrit 0 = ln 1 (ou r = ln eʳ) ; on finit par l'intersection avec D_I.
   Exemples : ln(2x − 1) < 0 : S = ]½ ; 1[ ; ln(x − 2) ≤ ln(4 − x) : S = ]2 ; 3].
4. **Second degré en ln x** : on pose X = ln x : (ln x)² − ln x − 2 = 0 ⇔ X = −1 ou X = 2 ; S = {1/e ; e²}.
5. **Produit nul** : 2x(ln x − 1) = 0 ⇔ x = 0 ou x = e ; 0 ∉ ]0 ; +∞[, donc S = {e}.
6. **Système** (x > 0, y > 0) : on pose X = ln x, Y = ln y, on résout, puis x = e^X, y = e^Y.
   Exemple : ln x + ln y = 3 et ln x − ln y = 1 : S = {(e² ; e)}.
7. **Plus petit entier n tel que qⁿ < a** : on passe au ln (le sens reste) : n ln q < ln a ; si 0 < q < 1, alors
   ln q < 0 : diviser par ln q renverse le sens.
   Exemples : (1/4)ⁿ < 10⁻⁴ ⇔ n > (4 ln 10)/(ln 4) ≈ 6,64 : n = 7 ; (1/3)ⁿ < 10⁻² ⇔ n > 4,19 : n = 5.

## VI. Les limites de base

1. lim_{x→+∞} ln x = +∞ (lentement) ; lim_{x→0⁺} ln x = −∞.
   Donc la droite d'équation x = 0 est asymptote verticale à la courbe de ln.
   *(figures : « Les deux branches de ln » ; tableau de variations de ln : −∞ ↗ 0 (en 1) ↗ +∞, double barre en 0)*
2. lim_{x→+∞} (ln x)/x = 0 ; pour n ∈ ℕ* : lim_{x→+∞} (ln x)/xⁿ = 0.
   Donc la courbe de ln admet une branche parabolique de direction l'axe des abscisses au voisinage de +∞.
3. lim_{x→0⁺} x ln x = 0 ; pour n ∈ ℕ* : lim_{x→0⁺} xⁿ ln x = 0 (x ln x < 0 sur ]0 ; 1[). *(figure : « x ln x → 0 en 0⁺ »)*
4. lim_{x→1} (ln x)/(x − 1) = 1 ; lim_{x→0} ln(1 + x)/x = 1 (nombre dérivé de ln en 1).
5. **Forme ∞ − ∞** : on factorise par x : x − ln x = x(1 − (ln x)/x) → +∞ en +∞.
   Attention : (ln x)/x tend vers 0, pas vers 1 ; on n'écrit jamais « ln 0 ».
6. **Limite déguisée** : on pose t = √x : ln x = 2 ln t ; (ln x)²/x = 4((ln t)/t)² → 0 quand x → +∞.
7. **En 0 à droite** : lim_{x→0⁺} f(x) = f(0) : f continue à droite en 0 ; lim_{x→0⁺} (f(x) − f(0))/x = −∞ :
   demi-tangente verticale au point d'abscisse 0.
8. **Limite de ln(u(x))** : lim_{x→a} u(x) = 0⁺ ⇒ lim_{x→a} ln(u(x)) = −∞ ; u(x) → +∞ ⇒ ln(u(x)) → +∞.
   Exemple : lim_{x→−1⁺} ln(x + 1) = −∞ : la droite d'équation x = −1 est asymptote verticale à (C_f).

## VII. La dérivée de ln u

1. (ln u)′ = u′/u (u dérivable et u > 0 sur I) ; (ln|u|)′ = u′/u (u dérivable et u ≠ 0 sur I).
2. ((ln x)²)′ = 2 × (1/x) × ln x = (2 ln x)/x ; (x ln x)′ = ln x + 1.
   Exemple (2019) : f(x) = x + ½ − ln x + ½(ln x)² ⇒ f′(x) = (x − 1 + ln x)/x.
   Attention : (ln u)′ = u′/u, et non 1/u.
3. **Signe de f′** : on garde le facteur qui change de signe. f′(x) = (1 − ln x)/x² : x² > 0, et 1 − ln x > 0 ⇔
   ln x < 1 ⇔ 0 < x < e. *(figure : tableau de signe de f′, double barre en 0)*

## VIII. Les primitives u′/u

1. Si u > 0 sur I : u′/u a pour primitive ln u sur I ; 1/x → ln x sur ]0 ; +∞[. Exemple : 2x/(x² + 1) → ln(x² + 1).
2. Si u ne s'annule pas sur I : u′/u a pour primitive ln|u| sur I. On fait apparaître u′ :
   x/(x² + 4) = ½ × 2x/(x² + 4) → ½ ln(x² + 4) ; sur ]−∞ ; 3[ : 1/(x − 3) → ln(3 − x).
3. **Vérifier une primitive** : H dérivable sur I et H′(x) = h(x) pour tout x de I. Exemple : (x ln x − x)′ = ln x.

## IX. Étude de fonction et inégalités, type national

1. **ln x ≤ x − 1** (méthode de la fonction auxiliaire) : on pose g(x) = x − 1 − ln x ; g′(x) = (x − 1)/x ; minimum
   g(1) = 0. Donc pour tout x > 0 : g(x) ≥ 0, c'est-à-dire ln x ≤ x − 1 (la courbe est sous (T)).
   *(figure nouvelle : tableau de variations de g, +∞ ↘ 0 ↗ +∞)*
2. **Problème (national 2019)** : f(x) = x + ½ − ln x + ½(ln x)² sur ]0 ; +∞[.
   a) f′(x) = g(x)/x² et x² > 0 : f′(x) a le signe de g(x) (g étudiée au début du sujet).
   b) f décroissante sur ]0 ; 1], croissante sur [1 ; +∞[ ; minimum f(1) = 3/2. *(figure : tableau de variations)*
   c) lim_{x→0⁺} f(x) = +∞ : la droite d'équation x = 0 est asymptote verticale à (C).
   d) En +∞ : f(x) = x + ½ + (½ ln x − 1) ln x → +∞ (écriture donnée par le sujet).
   e) f″(x) = (2 − ln x)/x² : f″ s'annule en e² en changeant de signe ; I(e² ; e² + ½) est un point d'inflexion de (C).
   f) Position : f(x) − x = ½(ln x − 1)² ≥ 0 : (C) est au-dessus de (Δ) : y = x ; ils se touchent en A(e ; e), car
   f(x) − x = 0 ⇔ ln x = 1 ⇔ x = e. *(figure : « (C) au-dessus de (Δ) »)*
   g) Construire (C) : placer d'abord l'asymptote x = 0, (Δ) et le minimum (1 ; 3/2) ; tangente en a :
   y = f′(a)(x − a) + f(a) ; en A(e ; e), f′(e) = 1 : la tangente est (Δ) ; puis I(e² ; e² + ½) ≈ (7,4 ; 7,9), la
   branche parabolique de direction (Δ), enfin la courbe. *(figure nouvelle : « Construction de (C) (national 2019) »)*
3. **Problème (national 2021)** : f(x) = 2x ln x − 2x sur ]0 ; +∞[, f(0) = 0.
   a) f continue à droite en 0 (x ln x → 0) ; demi-tangente verticale en O.
   b) f′(x) = 2 ln x : f décroît sur ]0 ; 1], croît sur [1 ; +∞[ ; minimum f(1) = −2.
   c) f(x) = 0 ⇔ x = e ; f(x) = x ⇔ x(2 ln x − 3) = 0 ⇔ x = e^(3/2) (x > 0).
   d) En +∞ : f(x)/x = 2 ln x − 2 → +∞ : branche parabolique de direction l'axe des ordonnées.
   e) f(x) ≥ −2 ⇔ 2x ln x ≥ 2x − 2 ⇔ ln x ≥ (x − 1)/x (on divise par 2x > 0).
   *(figure nouvelle : « Courbe du problème 2021 » : O, (1 ; −2), (e ; 0), intersection avec y = x en e^(3/2))*
4. **Étude de f(x) = ln((x + 2)/(1 − x))** : D_f = ]−2 ; 1[ (tableau de signe du quotient).
   a) lim_{x→−2⁺} f(x) = −∞ et lim_{x→1⁻} f(x) = +∞ (limite de ln(u(x))) : les droites d'équations x = −2 et x = 1
   sont asymptotes verticales à (C_f).
   b) f = ln u : f′ = u′/u = 3/((1 − x)(x + 2)) > 0 : f strictement croissante sur ]−2 ; 1[.
   c) f″ < 0 ⇒ (C_f) concave ; f″ > 0 ⇒ convexe ; f″ s'annule en changeant de signe ⇒ point d'inflexion.
   Ici f″(x) = 3(2x + 1)/((1 − x)²(x + 2)²) : point d'inflexion I(−½ ; 0). *(figures : courbe et tableau de variations)*

## X. Le logarithme décimal

1. log x = (ln x)/(ln 10) (x > 0) ; mêmes règles de calcul que ln. log 1 = 0 ; log 10 = 1 ; log(10ⁿ) = n (n ∈ ℤ).
2. 10ˣ = a ⇔ x = log a (a > 0) ; 10ˣ ≤ a ⇔ x ≤ log a (log strictement croissante).
   En chimie : pH = −log[H₃O⁺], donc [H₃O⁺] = 10^(−pH) mol/L.

## XI. Bilan

Recopie la fiche et la carte (diapositives `ln_b1`, `ln_b2`) ; entoure en rouge ce qui est à retravailler.

---

## Découpage

### Cours en ligne (`math_ch5_fonctions_ln.json`)

| Bloc | Diapos | Lignes | Début | Figures |
|---|---|---|---|---|
| `ln_s0_b1` | o1, z1_primitive, z2_puissances | 4 | Ce chapitre  | — |
| `ln_s0_b2` | z3_signe, z4_sens, z5_second_degre | 5 | Rappel  | — |
| `ln_s1_b1` | n1, n2 | 3 | I. 1. Pourquoi ln  | — |
| `ln_s1_b2` | n3, n4, c1, c2 | 5 | I. 2. Définition  | Le signe de ln x |
| `ln_s1_b3` | c3, c4, c5, d1 | 6 | II. 3. Le nombre e  | ln : le nombre e et la tangente en 1 |
| `ln_s2_b1` | d2, d3, d4, a1 | 6 | III. 2. Quotient dans ln  | — |
| `ln_s2_b2` | a2, a3, a3_b | 4 | IV. 1. (suite) Preuve  | ln(2x) = ln 2 + ln x |
| `ln_s2_b2b` | a4, a4_b, a5 | 4 | IV. 3. Puissance (a > 0)  | — |
| `ln_s2_b3` | a6, a6_b, a7 | 4 | IV. 5. Attention  | — |
| `ln_s2_b4` | a8, q1, q1_b | 5 | IV. 6. ln(eʳ) = r ln e = r  | — |
| `ln_s3_b1` | q2, q3, q4, q5 | 6 | V. 2. ln x = r ⇔ x = eʳ (car r = ln eʳ). | — |
| `ln_s3_b2` | q6, q7, l1, l2 | 6 | V. 6. Système (x > 0, y > 0)  | Les deux branches de ln ; Tableau de variations de ln |
| `ln_s3_b3` | l3, l4, l5, l6 | 6 | VI. 2. lim_{x→+∞} (ln x)/x = 0 ; pour n  | x ln x tend vers 0 en 0⁺ |
| `ln_s4_b1` | l7, l8, l9, v1 | 6 | VI. 6. On pose t = √x  | — |
| `ln_s4_b2` | v2, v2_b, v3, p1 | 6 | VII. 2. ((ln x)²)′ = 2 × (1/x) × ln x =  | Signe de f′(x) = (1 − ln x)/x² |
| `ln_s4_b3` | p2, p3, e1 | 5 | VIII. 2. Si u ne s'annule pas sur I  | Variations de g(x) = x − 1 − ln x |
| `ln_s5_b1` | e2, e3, e3_b, e4 | 6 | IX. 2. Problème (national 2019)  | Variations de f (national 2019) ; (C) au-dessus de (Δ) : y = x |
| `ln_s5_b1b` | e5, e5_b, e5_c | 6 | IX. 3. Problème (national 2021)  | Courbe du problème 2021 |
| `ln_s5_b1c` | e6, e6_b, e6_c | 6 | IX. 4. Étude de f(x) = ln((x + 2)/(1 − x | f(x) = ln((x + 2)/(1 − x)) ; Variations de f(x) = ln((x + 2)/(1 − x)) |
| `ln_s5_b2` | g1, g2, b1, b2 | 5 | X. 1. Logarithme décimal  | — |

### Copie en attente (`en_attente/math_ch5_fonctions_ln.json`)

| Bloc | Diapos | Lignes | Début | Figures |
|---|---|---|---|---|
| `ln_s0_b1` | o1, z1_primitive, z2_puissances | 4 | Ce chapitre  | — |
| `ln_s1_b1` | n1, n2 | 3 | I. 1. Pourquoi ln  | — |
| `ln_s1_b2` | n3, n4, c1, c2 | 5 | I. 2. Définition  | Le signe de ln x |
| `ln_s1_b3` | c3, c4, c5 | 5 | II. 3. Le nombre e  | ln : le nombre e et la tangente en 1 |
| `ln_s0_b2` | z4_sens, d1, z3_signe, d2 | 6 | Rappel  | — |
| `ln_s2_b1` | d3, d4, a1 | 4 | III. 3. Plusieurs conditions  | — |
| `ln_s2_b2` | a2, a3, a3_b | 4 | IV. 1. (suite) Preuve  | ln(2x) = ln 2 + ln x |
| `ln_s2_b2b` | a4, a4_b, a5 | 4 | IV. 3. Puissance (a > 0)  | — |
| `ln_s2_b3` | a6, a6_b, a7 | 4 | IV. 5. Attention  | — |
| `ln_s2_b4` | a8, q1, z5_second_degre, q1_b | 6 | IV. 6. ln(eʳ) = r ln e = r  | — |
| `ln_s3_b1` | q2, q3, q3_b, q4, q5 | 6 | V. 2. ln x = r ⇔ x = eʳ (car r = ln eʳ). | — |
| `ln_s3_b2` | q6, q7, q7_b, l1, l2 | 6 | V. 6. Système (x > 0, y > 0)  | Les deux branches de ln ; Tableau de variations de ln |
| `ln_s3_b3` | l3, l4, l5, l6 | 6 | VI. 2. lim_{x→+∞} (ln x)/x = 0 ; pour n  | x ln x tend vers 0 en 0⁺ |
| `ln_s4_b1` | l7, l8, l9, v1 | 6 | VI. 6. On pose t = √x  | — |
| `ln_s4_b2` | v2, v2_b, v3, p1 | 6 | VII. 2. ((ln x)²)′ = 2 × (1/x) × ln x =  | Signe de f′(x) = (1 − ln x)/x² |
| `ln_s4_b3` | p2, p3, e1 | 5 | VIII. 2. Si u ne s'annule pas sur I  | Variations de g(x) = x − 1 − ln x |
| `ln_s5_b1` | e2, e3, e3_b, e3_c | 5 | IX. 2. Problème (national 2019)  | Variations de f (national 2019) |
| `ln_s5_b1e` | e3_d, e4, e4_b | 4 | IX. 2. e) f″(x) = (2 − ln x)/x²  | (C) au-dessus de (Δ) : y = x |
| `ln_s5_b1d` | e4_c, e4_d | 3 | IX. 2. g) Construire (C)  | Construction de (C) (national 2019) |
| `ln_s5_b1b` | e5, e5_b, e5_q, e5_c | 6 | IX. 3. Problème (national 2021)  | Courbe du problème 2021 |
| `ln_s5_b1c` | e6, e6_b, e6_c | 6 | IX. 4. Étude de f(x) = ln((x + 2)/(1 − x | f(x) = ln((x + 2)/(1 − x)) ; Variations de f(x) = ln((x + 2)/(1 − x)) |
| `ln_s5_b2` | g1, g2, b1, b2 | 5 | X. 1. Logarithme décimal  | — |

Nombre de lignes d'un bloc toujours différent du nombre de ses diapositives : sinon `TableauCahier` range une ligne sous chaque titre de diapo et la numérotation se doublerait.
