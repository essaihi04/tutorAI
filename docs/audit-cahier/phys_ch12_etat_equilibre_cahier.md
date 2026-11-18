# Cahier de l'élève — État d'équilibre d'un système chimique (`phys_ch12_etat_equilibre`)

18 novembre 2026. Le cahier idéal du chapitre, d'un seul tenant, dans l'ordre de la version en attente (la plus complète) ; puis la table de découpage des deux versions. Les titres de partie (I., II.…) sont ceux que l'écran du cahier affiche déjà depuis `activities[].title` : ils ne sont pas réécrits dans `blocs[].cahier`. Les sous-titres (1., 2.…) continuent d'un bloc à l'autre dans une partie.

Notations : exemple A = acide éthanoïque, C = 1,0·10⁻² mol/L, V = 100 mL, pH = 3,41 ; B = trois concentrations ; C = en partant des produits ; D = conductimétrie, C = 1,0·10⁻³ mol/L ; E = acide méthanoïque.

## 1. Le cahier idéal (ordre de la version en attente)

### Les outils depuis zéro : concentration, puissances de dix, acide et pH

- 1. Concentration molaire : C = n/V (C en mol/L, n en mol, V en L) ; n = C·V.
- Ex. : 2,0 mmol dans 0,100 L → C = 20 mmol/L.
- 2. Puissances de dix : 10⁻³ = 0,001 ; 4,0·10⁻⁴ = 0,00040 ; log(10ⁿ) = n.
- 3. Définition : un acide est une espèce capable de céder un proton H⁺ ; une base, d'en capter un.
- Couple AH/A⁻ : AH(aq) ⇌ A⁻(aq) + H⁺(aq) ; l'eau : H₃O⁺/H₂O et H₂O/HO⁻.
- 4. pH = −log[H₃O⁺], donc [H₃O⁺] = 10^(−pH) en mol/L. Ex. : pH = 3,41 → 3,89·10⁻⁴ mol/L.

### I. Rappels : taux d'avancement final et état d'équilibre

- 1. Taux d'avancement final — ex. A : CH₃COOH(aq) + H₂O(l) ⇌ CH₃COO⁻(aq) + H₃O⁺(aq).
- Tableau (mol) : initial C·V | excès | 0 | 0 ; en cours C·V − x | excès | x | x.
- Équilibre : C·V − x_éq | excès | x_éq | x_éq. Eau en excès : x_max = C·V.
- τ = x_éq/x_max = 10^(−pH)/C ; C = 1,0·10⁻² mol/L, pH = 3,41 : τ = 0,039 < 1 (limitée).
- C = 1,0·10⁻³ mol/L : pH = 3,93, τ = 0,117. Donc τ dépend de C.
- 2. Équilibre dynamique : les deux sens ont la même vitesse ; concentrations constantes.

### II. Le quotient de réaction Qr

- 1. Définition : Qr est une grandeur qui caractérise un système chimique dans un état donné.
- Ex. A : Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH] (produits en haut, réactifs en bas, en mol/L).
- 2. aA + bB ⇌ cC + dD : Qr = [C]^c·[D]^d/([A]^a·[B]^b) (coefficients → exposants).
- 3. L'eau solvant (en très large excès) et les solides n'apparaissent pas dans Qr.
- Ex. : Cu²⁺(aq) + Zn(s) ⇌ Cu(s) + Zn²⁺(aq) : Qr = [Zn²⁺]/[Cu²⁺].

- 4. Qr est sans unité. Ex. A : [H₃O⁺] = 2,0·10⁻⁴ ; [CH₃COOH] = 9,8·10⁻³ mol/L → Qr = 4,08·10⁻⁶.

### III. Qr dans l'état initial et au cours de la transformation

- 1. Définition : Qr,i : quotient de réaction dans l'état initial. Acide dans l'eau : Qr,i = 0.
- 2. Méthode (mélange) : 1) n(X) = C·V ; 2) V_T = somme des volumes ; 3) [X]ᵢ = n(X)/V_T.
- Ex. : HCOOH(aq) + CH₃COO⁻(aq) ⇌ HCOO⁻(aq) + CH₃COOH(aq), V_T = 300 mL :
- Qr,i = (5,0·10⁻³ × 5,0·10⁻³)/(1,0·10⁻² × 1,0·10⁻²) = 0,25 (V_T se simplifie).

- 3. Qr évolue (ex. A) : [H₃O⁺] = [CH₃COO⁻] = x/V ; Qr = (x/V)²/(C − x/V).
- Qr croît de Qr,i = 0 à sa valeur d'équilibre (1,57·10⁻⁵), puis reste constant.
- 4. Au national, Qr,i : solides et eau solvant absents, coefficients en exposants.
- 2017 N : 3Cu²⁺(aq) + 2Al(s) ⇌ 3Cu(s) + 2Al³⁺(aq) : Qr,i = [Al³⁺]ᵢ²/[Cu²⁺]ᵢ³ ≈ 1,5.
- 2020 R : quatre solutions de 100 mL à 0,1 mol/L, V_T = 400 mL : Qr,i = 1.
- Attention : concentrations APRÈS mélange, [X]ᵢ = C·V/V_T (pas C).
- *Dessin : « Qr évolue jusqu'à l'équilibre »* — Q_r part de 0, croît avec [H₃O⁺] puis s'arrête à l'équilibre : 1,57·10⁻⁵ pour [H₃O⁺] = 3,89·10⁻⁴ mol/L.

### IV. Le quotient de réaction à l'équilibre Qr,éq

- 1. Méthode : 1) [H₃O⁺]éq = 10^(−pH) ; 2) [A⁻]éq = [H₃O⁺]éq ; 3) [AH]éq = C − [H₃O⁺]éq.
- Ex. A : [CH₃COO⁻]éq = [H₃O⁺]éq = 3,89·10⁻⁴ mol/L ; [CH₃COOH]éq = 9,61·10⁻³ mol/L.
- 2. Définition : Qr,éq est le quotient de réaction dans l'état d'équilibre. Ex. A : 1,57·10⁻⁵.
- 3. Qr,éq = 10^(−2pH)/(C − 10^(−pH)) ; 2017 N (acide butanoïque, pH = 3,41) : 1,57·10⁻⁵.
- Attention : [AH]éq = C − 10^(−pH), jamais C seul (point perdu au national).

### V. La constante d'équilibre K

- 1. Ex. B : C = 1,0·10⁻² ; 5,0·10⁻³ ; 1,0·10⁻³ mol/L → τ = 0,039 ; 0,055 ; 0,117 (τ change).
- Qr,éq = 1,57 ; 1,61 ; 1,56 (×10⁻⁵) : même valeur ; en partant des produits aussi (1,61·10⁻⁵).
- 2. Définition : constante d'équilibre K = Qr,éq (sans unité) ; ne dépend que de la température.
- Ex. : acide éthanoïque + eau, K = 1,6·10⁻⁵ à 25 °C. Remarque : K > 10⁴ → pratiquement totale.
- 3. Réaction inverse : K' = 1/K. Ex. : K' = 1/(1,6·10⁻⁵) = 6,25·10⁴.
- *Dessin : « Qr arrive toujours à K »* — Des réactifs (Q_{r,i} = 0, sens 1) ou des produits (sens 2) : Q_r arrive à la même valeur Q_{r,éq} = K = 1,6·10⁻⁵.

- 4. K en fonction de C et τ (acide AH dans l'eau) : x_éq = τ·x_max = τ·C·V.
- [A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C·(1 − τ), donc K = C·τ²/(1 − τ) (C en mol/L).
- Méthode : 1) τ = 10^(−pH)/C ; 2) K = C·τ²/(1 − τ). 2021 N : τ = 0,0132 → 1,77·10⁻⁵.
- Base dans l'eau, même relation : [CH₃NH₃⁺]éq = [HO⁻]éq = C_b·τ. 2022 R : τ = 0,20 → 5,0·10⁻⁴.
- Attention : « montrer » ou « vérifier » : écrire la relation littérale avant le calcul.

### VI. Déterminer K par la conductimétrie

- 1. G = k·σ (G en S, k en m, σ en S·m⁻¹) ; σ = Σλᵢ·[Xᵢ] (λᵢ en S·m²·mol⁻¹, [Xᵢ] en mol·m⁻³).
- 2. Acide AH : [A⁻]éq = [H₃O⁺]éq, donc σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺]éq (HO⁻ négligés).
- Méthode : 1) [H₃O⁺]éq = σ/(λ(H₃O⁺) + λ(A⁻)) en mol·m⁻³ ; 2) ÷ 10³ → mol/L ; 3) τ ; 4) K.
- Ex. D (C = 1,0·10⁻³ mol/L, σ = 4,6·10⁻³ S·m⁻¹) : 0,118 mol·m⁻³ ; τ = 0,118 ; K = 1,6·10⁻⁵.
- Attention : 1 mS·m⁻¹ = 10⁻³ S·m⁻¹ ; 1 µS·cm⁻¹ = 10⁻⁴ S·m⁻¹ ; 1 mol/L = 10³ mol·m⁻³.
- *Dessin : « Mesurer σ au conductimètre »* — La cellule (deux plaques) plonge dans la solution ; le conductimètre mesure G = k·σ et affiche σ.

### VI bis. National 2019 N, joué question par question

- Données : acide benzoïque, C = 1,0·10⁻³ mol/L, V = 1 L, σ = 8,6·10⁻³ S·m⁻¹.
- 2.1 : C₆H₅COOH(aq) + H₂O(l) ⇌ C₆H₅COO⁻(aq) + H₃O⁺(aq) (⇌ : réaction non totale).
- 2.2 : équilibre C·V − x_éq | excès | x_éq | x_éq ; x_max = C·V = 1,0·10⁻³ mol.
- 2.3.1 : [C₆H₅COO⁻]éq = [H₃O⁺]éq = x_éq/V, donc σ = (λ₁ + λ₂)·[H₃O⁺]éq.

- 2.3.2 : τ = x_éq/x_max = σ/(C·(λ₁ + λ₂)) = 8,6·10⁻³/(1,0 × 38,23·10⁻³) ≈ 0,22.
- Attention : ici C en mol·m⁻³ : 1,0·10⁻³ mol/L = 1,0 mol·m⁻³.
- 2.4 : K = C·τ²/(1 − τ) = 1,0·10⁻³ × 0,22²/(1 − 0,22) ≈ 6,2·10⁻⁵ (ici C en mol/L).

### VII. De quoi dépend le taux d'avancement final ?

- 1. Diluer : V₀ prélevé à la pipette, fiole jaugée de V₁ ; C₀·V₀ = C₁·V₁ (F = V₁/V₀).
- 2. Même K = 1,6·10⁻⁵ : C = 1,0·10⁻² ; 5,0·10⁻³ ; 1,0·10⁻³ mol/L → τ = 0,039 ; 0,055 ; 0,117.
- Donc, même K : plus C est petite, plus τ est grand.
- 3. Acide méthanoïque (C = 1,0·10⁻² mol/L, pH = 2,90) : Qr,éq = 1,81·10⁻⁴, donc K = 1,8·10⁻⁴.
- Chaque réaction a sa constante K (acide éthanoïque : K = 1,6·10⁻⁵).

- 4. Même C = 1,0·10⁻² mol/L : K = 1,6·10⁻⁵ → τ = 0,039 ; K = 1,8·10⁻⁴ → τ = 0,13.
- Donc, même C : plus K est grande, plus τ est grand.
- 5. Conclusion : τ dépend de K (nature de la réaction) et de l'état initial (C).
- Quand on dilue : C ↓, [H₃O⁺]éq ↓, pH ↑, τ ↑ ; K inchangée (elle ne dépend que de T).
- Attention : τ dépend de l'état initial ; K n'en dépend pas.
- *Dessin : « τ dépend de K et de C »* — C en échelle logarithmique : τ grandit quand C diminue (même K) et quand K est plus grande (même C).

### VIII. National : K lue sur une courbe

- 2017 R : CH₃COOH(l) + C₂H₅OH(l) ⇌ CH₃COOC₂H₅(l) + H₂O(l)
- Méthode : 1) palier = équilibre ; 2) tableau → x_éq ; 3) K = Qr,éq (V se simplifie).
- Ex. : n_éq(acide) = 0,6 − x_éq = 0,2 mol → x_éq = 0,4 mol ; K = (0,4 × 0,4)/(0,2 × 0,2) = 4.
- Attention : ici l'eau est un produit, pas le solvant : elle figure dans K.

### IX. Bilan du chapitre

- Bilan — rédiger : équation avec ⇌, tableau, relation littérale, calcul, sans unité.
- Attention : Qr et K sans unité ; C en mol/L dans K ; [Xᵢ] en mol·m⁻³ dans σ = Σλᵢ·[Xᵢ].
- *Dessin : « Lire l'équilibre sur le palier »* — n(acide) passe de 0,6 mol au palier 0,2 mol : équilibre, x_éq = 0,6 − 0,2 = 0,4 mol (allure, 2017 R).

Dessins : « Qr évolue jusqu'à l'équilibre » (Q_r = 100x²/(100 − x) ×10⁻⁶, x = [H₃O⁺] en 10⁻⁴ mol/L : passe par 1,01 ; 4,08 ; 9,28 ; 15,74) ; « Qr arrive toujours à K » (axe de Qr, sens 1 et sens 2 vers K) ; « Mesurer σ au conductimètre » (montage, nouveau) ; « τ dépend de K et de C » (τ = (−K + √(K² + 4KC))/(2C) : 0,33/0,72 à 10⁻⁴ mol/L, 0,013/0,042 à 10⁻¹ mol/L) ; « Lire l'équilibre sur le palier » (2017 R, n(acide) de 0,6 à 0,2 mol, nouveau ; le sujet ne donne pas l'échelle de temps : axe t en h sans graduation).

## 2. Table de découpage

Chaque bloc : 3 à 6 lignes, nombre de lignes ≠ nombre de diapos (sinon l'écran range une ligne sous chaque titre de diapo), 0 ou 1 figure. Chaque bulle (`concentration.cahier`, chaîne) : 1 ou 2 phrases (séparées par un saut de ligne). Bloc → lignes (début de chaque ligne) et figures ; puis diapo → bulle.

### Version en attente (`backend/data/courses/en_attente/phys_ch12_etat_equilibre.json`)

| Bloc (diapos) | Lignes du bloc | Figures |
|---|---|---|
| `ee_b01` (z1_concentration, z2_puissance, z4_couple, z5_ph) | 6 : 1. Concentration molaire / Ex. / 2. Puissances de dix / 3. Définition / Couple AH/A⁻ / 4. pH = −log[H₃O⁺], donc [H₃O⁺] = 10^(−p | — |
| `ee_b02` (r1_taux, o2_flacons, r2_equilibre) | 6 : 1. Taux d'avancement final — ex. A / Tableau (mol) / Équilibre / τ = x_éq/x_max = 10^(−pH)/C ; C = 1,0·10 / C = 1,0·10⁻³ mol/L / 2. Équilibre dynamique | — |
| `ee_b03` (q1_quotient, q2_generale, q3_eau, q4_solides) | 5 : 1. Définition / Ex. A / 2. aA + bB ⇌ cC + dD / 3. L'eau solvant (en très large excès) e / Ex. | — |
| `ee_b04` (q5_sans_unite, i1_initial, i2_melange, i2b_calcul) | 5 : 4. Qr est sans unité. Ex. A / 1. Définition / 2. Méthode (mélange) / Ex. / Qr,i = (5,0·10⁻³ × 5,0·10⁻³)/(1,0·10⁻² × | — |
| `ee_b05` (i3_au_cours, n4_pile, n3_melange) | 6 : 3. Qr évolue (ex. A) / Qr croît de Qr,i = 0 à sa valeur d'équil / 4. Au national, Qr,i / 2017 N / 2020 R / Attention | Qr évolue jusqu'à l'équilibre |
| `ee_b06` (e1_concentrations, e2_quotient, e3_expression, n1_national) | 5 : 1. Méthode / Ex. A / 2. Définition / 3. Qr,éq = 10^(−2pH)/(C − 10^(−pH)) ; 20 / Attention | — |
| `ee_b07` (k1_trois, k2_produits, k3_constante, k4_inverse) | 5 : 1. Ex. B / Qr,éq = 1,57 ; 1,61 ; 1,56 (×10⁻⁵) / 2. Définition / Ex. / 3. Réaction inverse | Qr arrive toujours à K |
| `ee_b08` (k5_tau, n6_taux, n2_base) | 5 : 4. K en fonction de C et τ (acide AH dan / [A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C·(1  / Méthode / Base dans l'eau, même relation / Attention | — |
| `ee_b09` (m2a_conductance, m2_conductimetrie, m3_calcul) | 5 : 1. G = k·σ (G en S, k en m, σ en S·m⁻¹)  / 2. Acide AH / Méthode / Ex. D (C = 1,0·10⁻³ mol/L, σ = 4,6·10⁻³  / Attention | Mesurer σ au conductimètre |
| `ee_b09b` (x1_equation, x2_tableau, x3_sigma) | 4 : Données / 2.1 / 2.2 / 2.3.1 | — |
| `ee_b09c` (x4_taux, x5_constante) | 3 : 2.3.2 / Attention / 2.4 | — |
| `ee_b10` (z3_dilution, f1_dilution, m1_methanoique) | 5 : 1. Diluer / 2. Même K = 1,6·10⁻⁵ / Donc, même K / 3. Acide méthanoïque (C = 1,0·10⁻² mol/L / Chaque réaction a sa constante K (acide  | — |
| `ee_b11` (f2_nature, f3_courbe, f4_bilan) | 5 : 4. Même C = 1,0·10⁻² mol/L / Donc, même C / 5. Conclusion / Quand on dilue / Attention | τ dépend de K et de C |
| `ee_b12` (n5_courbe, bl_fiche, cr_carte) | 6 : 2017 R / Méthode / Ex. / Attention / Bilan — rédiger / Attention | Lire l'équilibre sur le palier |

| Diapo | Bulle | Figure |
|---|---|---|
| `ee_z1_concentration` | Concentration molaire : C = n/V (C en mol/L, n en mol, V en L) ; n = C·V. ⏎ Ex. : 2,0 mmol dans 0,100 L → C = 20 mmol/L. | — |
| `ee_z2_puissance` | 10⁻¹ = 0,1 ; 10⁻² = 0,01 ; 10⁻³ = 0,001 ; 4,0·10⁻⁴ = 0,00040. ⏎ log(10ⁿ) = n : log(10⁻³) = −3 ; −log(10⁻³) = 3. | — |
| `ee_z4_couple` | Acide : espèce capable de céder un proton H⁺ ; base : espèce capable de capter un proton H⁺. ⏎ Couple AH/A⁻ : AH(aq) ⇌ A⁻(aq) + H⁺(aq) (CH₃COOH/CH₃COO⁻ ; NH₄⁺/NH₃). | — |
| `ee_z5_ph` | L'eau est dans deux couples : H₃O⁺/H₂O et H₂O/HO⁻. ⏎ pH = −log[H₃O⁺] ; [H₃O⁺] = 10^(−pH). Ex. : pH = 3,41 → [H₃O⁺] = 3,89·10⁻⁴ mol/L. | — |
| `ee_r1_taux` | Ex. A : tableau ; eau en excès : x_max = C·V ; x_éq = [H₃O⁺]éq·V. ⏎ τ = x_éq/x_max = 10^(−pH)/C = 3,89·10⁻⁴/(1,0·10⁻²) = 0,039 < 1 : réaction limitée. | — |
| `ee_o2_flacons` | τ = 10^(−pH)/C : C = 1,0·10⁻² mol/L → τ = 0,039 ; C = 1,0·10⁻³ mol/L → τ = 0,117. ⏎ Donc τ dépend de C : on cherche une grandeur qui n'en dépend pas. | — |
| `ee_r2_equilibre` | Équilibre dynamique : les deux sens ont la même vitesse ; concentrations constantes. ⏎ Ex. A : [CH₃COO⁻]éq = [H₃O⁺]éq = 3,89·10⁻⁴ mol/L ; [CH₃COOH]éq = 9,61·10⁻³ mol/L. | — |
| `ee_q1_quotient` | Définition : Qr est une grandeur qui caractérise un système chimique dans un état donné. ⏎ Ex. A : Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH] (concentrations en mol/L). | — |
| `ee_q2_generale` | aA + bB ⇌ cC + dD : Qr = [C]^c·[D]^d/([A]^a·[B]^b) (coefficients → exposants). ⏎ Ex. : 2I⁻(aq) + S₂O₈²⁻(aq) ⇌ I₂(aq) + 2SO₄²⁻(aq) : Qr = [I₂]·[SO₄²⁻]²/([I⁻]²·[S₂O₈²⁻]). | — |
| `ee_q3_eau` | L'eau solvant, en très large excès, n'apparaît pas dans Qr. ⏎ Ex. A : Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH] (pas de [H₂O]). | — |
| `ee_q4_solides` | Les solides n'apparaissent pas : Cu²⁺(aq) + Zn(s) ⇌ Cu(s) + Zn²⁺(aq) → Qr = [Zn²⁺]/[Cu²⁺]. ⏎ Fe³⁺(aq) + 3HO⁻(aq) ⇌ Fe(OH)₃(s) : Qr = 1/([Fe³⁺]·[HO⁻]³). | — |
| `ee_q5_sans_unite` | Qr se calcule avec les concentrations en mol/L ; Qr est sans unité. ⏎ Ex. A : Qr = (2,0·10⁻⁴ × 2,0·10⁻⁴)/(9,8·10⁻³) = 4,08·10⁻⁶. | — |
| `ee_i1_initial` | Définition : Qr,i est le quotient de réaction dans l'état initial. ⏎ Acide versé dans l'eau : [CH₃COO⁻]ᵢ = [H₃O⁺]ᵢ = 0, donc Qr,i = 0. | — |
| `ee_i2_melange` | Mélange : [X]ᵢ = n(X)/V_T (concentrations APRÈS mélange) ; ici V_T = 300 mL. ⏎ n = C·V : HCOOH et CH₃COO⁻ 1,0·10⁻² mol ; CH₃COOH et HCOO⁻ 5,0·10⁻³ mol. | — |
| `ee_i2b_calcul` | Qr,i = [HCOO⁻]ᵢ·[CH₃COOH]ᵢ/([HCOOH]ᵢ·[CH₃COO⁻]ᵢ) ; V_T se simplifie. ⏎ Qr,i = (5,0·10⁻³ × 5,0·10⁻³)/(1,0·10⁻² × 1,0·10⁻²) = 0,25. | — |
| `ee_i3_au_cours` | Ex. A : Qr = (x/V)²/(C − x/V) : Qr dépend de l'avancement x. ⏎ Qr part de Qr,i = 0, augmente puis reste constant à l'équilibre (1,57·10⁻⁵). | Qr évolue jusqu'à l'équilibre |
| `ee_n4_pile` | 2017 N : 3Cu²⁺(aq) + 2Al(s) ⇌ 3Cu(s) + 2Al³⁺(aq) ; solides absents, coefficients en exposants. ⏎ Qr,i = [Al³⁺]ᵢ²/[Cu²⁺]ᵢ³ = (6,5·10⁻¹)²/(6,5·10⁻¹)³ = 1/(6,5·10⁻¹) ≈ 1,5. | — |
| `ee_n3_melange` | 2020 R : V_T = 400 mL ; [X]ᵢ = C·V/V_T (concentrations APRÈS mélange). ⏎ Qr,i = (C₃V₃·C₄V₄)/(C₁V₁·C₂V₂) = 1 (V_T se simplifie). | — |
| `ee_e1_concentrations` | Réaction rapide : pH mesuré = pH à l'équilibre ; [H₃O⁺]éq = 10^(−pH) = 3,89·10⁻⁴ mol/L. ⏎ [CH₃COO⁻]éq = [H₃O⁺]éq ; [CH₃COOH]éq = C − [H₃O⁺]éq = 9,61·10⁻³ mol/L. | — |
| `ee_e2_quotient` | Définition : Qr,éq est le quotient de réaction dans l'état d'équilibre. ⏎ Ex. A : Qr,éq = (3,89·10⁻⁴)²/(9,61·10⁻³) = 1,57·10⁻⁵ (sans unité). | — |
| `ee_e3_expression` | [A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [AH]éq = C − 10^(−pH) : Qr,éq = 10^(−2pH)/(C − 10^(−pH)). ⏎ Attention : ne pas remplacer [AH]éq par C. | — |
| `ee_n1_national` | 2017 N : Qr,éq = 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = 1,57·10⁻⁵ (sans unité). | — |
| `ee_k1_trois` | Ex. B : τ = 0,039 ; 0,055 ; 0,117 (change avec C) ; Qr,éq = 1,57 ; 1,61 ; 1,56 (×10⁻⁵). ⏎ Donc Qr,éq ne dépend pas de C (aux erreurs de mesure près). | — |
| `ee_k2_produits` | Ex. C (on part des produits, pH = 3,56) : [H₃O⁺]éq = 2,75·10⁻⁴ ; [CH₃COOH]éq = 4,72·10⁻³ mol/L. ⏎ Qr,éq = 1,61·10⁻⁵ : même valeur qu'en partant de l'acide. | — |
| `ee_k3_constante` | Définition : K = Qr,éq = [C]éq^c·[D]éq^d/([A]éq^a·[B]éq^b), sans unité ; ne dépend que de T. ⏎ Acide éthanoïque + eau : K = 1,6·10⁻⁵ à 25 °C ; si K > 10⁴, réaction pratiquement totale. | Qr arrive toujours à K |
| `ee_k4_inverse` | Réaction inverse : CH₃COO⁻(aq) + H₃O⁺(aq) ⇌ CH₃COOH(aq) + H₂O(l) : K' = 1/K. ⏎ K' = 1/(1,6·10⁻⁵) = 6,25·10⁴ > 10⁴ : pratiquement totale. | — |
| `ee_k5_tau` | x_éq = τ·C·V : [A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C·(1 − τ). ⏎ K = (C·τ)²/(C·(1 − τ)) = C·τ²/(1 − τ) (C en mol/L). | — |
| `ee_n6_taux` | 2021 N : τ = 10^(−2,88)/0,10 = 0,0132 ; Qr,éq = 0,10 × 0,0132²/(1 − 0,0132) = 1,77·10⁻⁵. | — |
| `ee_n2_base` | 2022 R : CH₃NH₂(aq) + H₂O(l) ⇌ CH₃NH₃⁺(aq) + HO⁻(aq) ; [CH₃NH₃⁺]éq = [HO⁻]éq = C_b·τ. ⏎ Qr,éq = C_b·τ²/(1 − τ) = 1,0·10⁻² × 0,20²/(1 − 0,20) = 5,0·10⁻⁴. | — |
| `ee_m2a_conductance` | G = k·σ (G en S ; k, constante de cellule, en m ; σ en S·m⁻¹). ⏎ σ = Σλᵢ·[Xᵢ] (λᵢ en S·m²·mol⁻¹, [Xᵢ] en mol·m⁻³) ; réaction rapide : σ mesurée à l'équilibre. | Mesurer σ au conductimètre |
| `ee_m2_conductimetrie` | σ = λ(H₃O⁺)·[H₃O⁺] + λ(CH₃COO⁻)·[CH₃COO⁻] = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] (HO⁻ négligés). ⏎ [H₃O⁺]éq = σ/(λ(H₃O⁺) + λ(A⁻)), en mol·m⁻³. | — |
| `ee_m3_calcul` | Ex. D : [H₃O⁺]éq = 4,6·10⁻³/(39,09·10⁻³) = 0,118 mol·m⁻³ = 1,18·10⁻⁴ mol/L. ⏎ τ = 0,118 ; K = C·τ²/(1 − τ) = 1,58·10⁻⁵ ≈ 1,6·10⁻⁵ : même K que par le pH. | — |
| `ee_x1_equation` | 2019 N, 2.1 : C₆H₅COOH(aq) + H₂O(l) ⇌ C₆H₅COO⁻(aq) + H₃O⁺(aq) (non totale ; eau en excès). | — |
| `ee_x2_tableau` | 2.2 : initial C·V | excès | 0 | 0 ; en cours C·V − x | excès | x | x. ⏎ Équilibre : C·V − x_éq | excès | x_éq | x_éq ; x_max = C·V = 1,0·10⁻³ mol. | — |
| `ee_x3_sigma` | 2.3.1 : σ = λ₁·[H₃O⁺]éq + λ₂·[C₆H₅COO⁻]éq (HO⁻ négligés). ⏎ [C₆H₅COO⁻]éq = [H₃O⁺]éq, donc σ = (λ₁ + λ₂)·[H₃O⁺]éq. | — |
| `ee_x4_taux` | 2.3.2 : x_éq = σ·V/(λ₁ + λ₂) et x_max = C·V, donc τ = σ/(C·(λ₁ + λ₂)). ⏎ C = 1,0 mol·m⁻³ : τ = 8,6·10⁻³/(1,0 × 38,23·10⁻³) ≈ 0,22. | — |
| `ee_x5_constante` | 2.4 : [C₆H₅COO⁻]éq = [H₃O⁺]éq = C·τ ; [C₆H₅COOH]éq = C·(1 − τ) ; K = C·τ²/(1 − τ). ⏎ K = 1,0·10⁻³ × 0,22²/(1 − 0,22) ≈ 6,2·10⁻⁵ (C en mol/L ; K sans unité). | — |
| `ee_z3_dilution` | Diluer : V₀ prélevé à la pipette, fiole jaugée de V₁, eau distillée jusqu'au trait. ⏎ C₀·V₀ = C₁·V₁ ; facteur F = V₁/V₀ (10 mL → 100 mL : diluée 10 fois). | — |
| `ee_f1_dilution` | Même K = 1,6·10⁻⁵ : C = 1,0·10⁻² ; 5,0·10⁻³ ; 1,0·10⁻³ mol/L → τ = 0,039 ; 0,055 ; 0,117. ⏎ Même K : plus C est petite, plus τ est grand. | — |
| `ee_m1_methanoique` | Ex. E : HCOOH(aq) + H₂O(l) ⇌ HCOO⁻(aq) + H₃O⁺(aq) ; C = 1,0·10⁻² mol/L ; pH = 2,90. ⏎ Qr,éq = 10^(−5,80)/(1,0·10⁻² − 10^(−2,90)) = 1,81·10⁻⁴ : K = 1,8·10⁻⁴ ; chaque réaction a sa K. | — |
| `ee_f2_nature` | Même C = 1,0·10⁻² mol/L : K = 1,6·10⁻⁵ → τ = 0,039 ; K = 1,8·10⁻⁴ → τ = 0,13. ⏎ Même C : plus K est grande, plus τ est grand (K traduit la nature de la réaction). | — |
| `ee_f3_courbe` | τ dépend de K (nature de la réaction) et de C (état initial). ⏎ C = 1,0·10⁻⁴ mol/L : τ = 0,33 et 0,72 ; C = 1,0·10⁻¹ mol/L : τ = 0,013 et 0,042. | τ dépend de K et de C |
| `ee_f4_bilan` | Quand on dilue : C ↓ ; [H₃O⁺]éq ↓ ; pH ↑ ; τ ↑ ; K inchangée. ⏎ Attention : τ dépend de l'état initial ; K ne dépend que de la température. | — |
| `ee_n5_courbe` | 2017 R : palier n_éq(acide) = 0,2 mol ; x_éq = 0,6 − 0,2 = 0,4 mol. ⏎ K = (0,4 × 0,4)/(0,2 × 0,2) = 4 (V se simplifie) ; ici l'eau est un produit : elle figure. | Lire l'équilibre sur le palier |
| `ee_bl_fiche` | Qr (eau solvant et solides absents) ; Qr,i ; Qr,éq = K (ne dépend que de T) ; K' = 1/K. ⏎ τ = 10^(−pH)/C ; K = C·τ²/(1 − τ) ; σ = Σλᵢ·[Xᵢ] ; diluer : τ ↑, K inchangée. | — |
| `ee_cr_carte` | À l'équilibre : Qr,éq = K. Qr,i → Qr évolue → Qr,éq = K ; τ dépend de K et de C. | — |

### Version en ligne (`backend/data/courses/phys_ch12_etat_equilibre.json`)

| Bloc (diapos) | Lignes du bloc | Figures |
|---|---|---|
| `ee_r_b1` (o1_carte, o2_flacons, z1_concentration) | 6 : Plan / 1. Rappel / Acide éthanoïque / Donc τ dépend de C / 2. Concentration molaire / Ex. | — |
| `ee_s1_b1` (z2_puissance, r1_taux, r2_equilibre) | 6 : 3. Puissances de dix / 1. Taux d'avancement final — ex. A / Tableau (mol) / Équilibre / τ = x_éq/x_max = 10^(−pH)/C ; C = 1,0·10 / 2. Équilibre dynamique | — |
| `ee_s1_b2` (q1_quotient, q2_generale, q3_eau, q4_solides) | 5 : 1. Définition / Ex. A / 2. aA + bB ⇌ cC + dD / 3. L'eau solvant (en très large excès) e / Ex. | — |
| `ee_s1_b3` (q5_sans_unite, i1_initial, i2_melange, i2b_calcul, i3_au_cours) | 6 : 4. Qr est sans unité. Ex. A / 1. Définition / 2. Méthode (mélange) / Ex. (V_T = 300 mL) / 3. Qr = (x/V)²/(C − x/V) croît de 0 jusq / Attention | Qr évolue jusqu'à l'équilibre |
| `ee_s2_b1` (e1_concentrations, e2_quotient, e3_expression, k1_trois) | 5 : 1. Méthode / 2. Définition / 3. Qr,éq = 10^(−2pH)/(C − 10^(−pH)). Att / 1. Ex. B (même acide) / τ = 0,039 ; 0,055 ; 0,117 (τ change) ; Q | — |
| `ee_s2_b2` (k2_produits, k3_constante, k4_inverse, k5_tau) | 6 : Ex. C (en partant des produits, pH = 3,5 / 2. Définition / Ex. / 3. Réaction inverse / 4. Acide AH / Donc K = (C·τ)²/(C·(1 − τ)) = C·τ²/(1 −  | Qr arrive toujours à K |
| `ee_s2_b3` (m1_methanoique, m2a_conductance, m2_conductimetrie, m3_calcul, m4_national) | 6 : 1. Par le pH / Chaque réaction a sa constante K (acide  / 2. G = k·σ (G en S, k en m, σ en S·m⁻¹)  / Méthode / Ex. D / 2019 N | Mesurer σ au conductimètre |
| `ee_s3_b1` (z3_dilution, f1_dilution, f2_nature, f3_courbe, f4_bilan) | 6 : 1. Diluer / 2. Même K = 1,6·10⁻⁵ / Donc, même K / 3. Même C = 1,0·10⁻² mol/L / 4. τ dépend de K (nature de la réaction) / Quand on dilue | τ dépend de K et de C |
| `ee_s3_b2` (n1_national, n2_base, n3_melange, n4_pile) | 5 : Méthode — rédiger / 2017 N / 2022 R (base) / 2020 R / 2017 N (pile) | — |
| `ee_s3_b3` (n5_courbe, n6_taux, bl_fiche, cr_carte) | 5 : 2017 R / Attention / 2021 N / Bilan / Attention | Lire l'équilibre sur le palier |

| Diapo | Bulle | Figure |
|---|---|---|
| `ee_o1_carte` | Plan : rappels ; quotient de réaction Qr ; constante d'équilibre K ; facteurs de τ. | — |
| `ee_o2_flacons` | Rappel : pH = −log[H₃O⁺] ; τ = 10^(−pH)/C : C = 1,0·10⁻² mol/L → τ = 0,039 ; 1,0·10⁻³ → 0,117. ⏎ Donc τ dépend de C : on cherche une grandeur qui n'en dépend pas. | — |
| `ee_z1_concentration` | Concentration molaire : C = n/V (C en mol/L, n en mol, V en L) ; n = C·V. ⏎ Ex. : 2,0 mmol dans 0,100 L → C = 20 mmol/L. | — |
| `ee_z2_puissance` | 10⁻¹ = 0,1 ; 10⁻² = 0,01 ; 10⁻³ = 0,001 ; 4,0·10⁻⁴ = 0,00040. ⏎ log(10ⁿ) = n : log(10⁻³) = −3 ; −log(10⁻³) = 3. | — |
| `ee_r1_taux` | Ex. A : tableau ; eau en excès : x_max = C·V ; x_éq = [H₃O⁺]éq·V. ⏎ τ = x_éq/x_max = 10^(−pH)/C = 3,89·10⁻⁴/(1,0·10⁻²) = 0,039 < 1 : réaction limitée. | — |
| `ee_r2_equilibre` | Équilibre dynamique : les deux sens ont la même vitesse ; concentrations constantes. ⏎ Ex. A : [CH₃COO⁻]éq = [H₃O⁺]éq = 3,89·10⁻⁴ mol/L ; [CH₃COOH]éq = 9,61·10⁻³ mol/L. | — |
| `ee_q1_quotient` | Définition : Qr est une grandeur qui caractérise un système chimique dans un état donné. ⏎ Ex. A : Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH] (concentrations en mol/L). | — |
| `ee_q2_generale` | aA + bB ⇌ cC + dD : Qr = [C]^c·[D]^d/([A]^a·[B]^b) (coefficients → exposants). ⏎ Ex. : 2I⁻(aq) + S₂O₈²⁻(aq) ⇌ I₂(aq) + 2SO₄²⁻(aq) : Qr = [I₂]·[SO₄²⁻]²/([I⁻]²·[S₂O₈²⁻]). | — |
| `ee_q3_eau` | L'eau solvant, en très large excès, n'apparaît pas dans Qr. ⏎ Ex. A : Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH] (pas de [H₂O]). | — |
| `ee_q4_solides` | Les solides n'apparaissent pas : Cu²⁺(aq) + Zn(s) ⇌ Cu(s) + Zn²⁺(aq) → Qr = [Zn²⁺]/[Cu²⁺]. ⏎ Fe³⁺(aq) + 3HO⁻(aq) ⇌ Fe(OH)₃(s) : Qr = 1/([Fe³⁺]·[HO⁻]³). | — |
| `ee_q5_sans_unite` | Qr se calcule avec les concentrations en mol/L ; Qr est sans unité. ⏎ Ex. A : Qr = (2,0·10⁻⁴ × 2,0·10⁻⁴)/(9,8·10⁻³) = 4,08·10⁻⁶. | — |
| `ee_i1_initial` | Définition : Qr,i est le quotient de réaction dans l'état initial. ⏎ Acide versé dans l'eau : [CH₃COO⁻]ᵢ = [H₃O⁺]ᵢ = 0, donc Qr,i = 0. | — |
| `ee_i2_melange` | Mélange : [X]ᵢ = n(X)/V_T (concentrations APRÈS mélange) ; ici V_T = 300 mL. ⏎ n = C·V : HCOOH et CH₃COO⁻ 1,0·10⁻² mol ; CH₃COOH et HCOO⁻ 5,0·10⁻³ mol. | — |
| `ee_i2b_calcul` | Qr,i = [HCOO⁻]ᵢ·[CH₃COOH]ᵢ/([HCOOH]ᵢ·[CH₃COO⁻]ᵢ) ; V_T se simplifie. ⏎ Qr,i = (5,0·10⁻³ × 5,0·10⁻³)/(1,0·10⁻² × 1,0·10⁻²) = 0,25. | — |
| `ee_i3_au_cours` | Ex. A : Qr = (x/V)²/(C − x/V) : Qr dépend de l'avancement x. ⏎ Qr part de Qr,i = 0, augmente puis reste constant à l'équilibre (1,57·10⁻⁵). | Qr évolue jusqu'à l'équilibre |
| `ee_e1_concentrations` | Réaction rapide : pH mesuré = pH à l'équilibre ; [H₃O⁺]éq = 10^(−pH) = 3,89·10⁻⁴ mol/L. ⏎ [CH₃COO⁻]éq = [H₃O⁺]éq ; [CH₃COOH]éq = C − [H₃O⁺]éq = 9,61·10⁻³ mol/L. | — |
| `ee_e2_quotient` | Définition : Qr,éq est le quotient de réaction dans l'état d'équilibre. ⏎ Ex. A : Qr,éq = (3,89·10⁻⁴)²/(9,61·10⁻³) = 1,57·10⁻⁵ (sans unité). | — |
| `ee_e3_expression` | [A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; [AH]éq = C − 10^(−pH) : Qr,éq = 10^(−2pH)/(C − 10^(−pH)). ⏎ Attention : ne pas remplacer [AH]éq par C. | — |
| `ee_k1_trois` | Ex. B : τ = 0,039 ; 0,055 ; 0,117 (change avec C) ; Qr,éq = 1,57 ; 1,61 ; 1,56 (×10⁻⁵). ⏎ Donc Qr,éq ne dépend pas de C (aux erreurs de mesure près). | — |
| `ee_k2_produits` | Ex. C (on part des produits, pH = 3,56) : [H₃O⁺]éq = 2,75·10⁻⁴ ; [CH₃COOH]éq = 4,72·10⁻³ mol/L. ⏎ Qr,éq = 1,61·10⁻⁵ : même valeur qu'en partant de l'acide. | — |
| `ee_k3_constante` | Définition : K = Qr,éq = [C]éq^c·[D]éq^d/([A]éq^a·[B]éq^b), sans unité ; ne dépend que de T. ⏎ Acide éthanoïque + eau : K = 1,6·10⁻⁵ à 25 °C ; si K > 10⁴, réaction pratiquement totale. | Qr arrive toujours à K |
| `ee_k4_inverse` | Réaction inverse : CH₃COO⁻(aq) + H₃O⁺(aq) ⇌ CH₃COOH(aq) + H₂O(l) : K' = 1/K. ⏎ K' = 1/(1,6·10⁻⁵) = 6,25·10⁴ > 10⁴ : pratiquement totale. | — |
| `ee_k5_tau` | x_éq = τ·C·V : [A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C·(1 − τ). ⏎ K = (C·τ)²/(C·(1 − τ)) = C·τ²/(1 − τ) (C en mol/L). | — |
| `ee_m1_methanoique` | Par le pH : HCOOH(aq) + H₂O(l) ⇌ HCOO⁻(aq) + H₃O⁺(aq) ; C = 1,0·10⁻² mol/L ; pH = 2,90. ⏎ Qr,éq = 10^(−5,80)/(1,0·10⁻² − 10^(−2,90)) = 1,81·10⁻⁴ : K = 1,8·10⁻⁴ ; chaque réaction a sa K. | — |
| `ee_m2a_conductance` | G = k·σ (G en S ; k, constante de cellule, en m ; σ en S·m⁻¹). ⏎ σ = Σλᵢ·[Xᵢ] (λᵢ en S·m²·mol⁻¹, [Xᵢ] en mol·m⁻³) ; réaction rapide : σ mesurée à l'équilibre. | Mesurer σ au conductimètre |
| `ee_m2_conductimetrie` | σ = λ(H₃O⁺)·[H₃O⁺] + λ(CH₃COO⁻)·[CH₃COO⁻] = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] (HO⁻ négligés). ⏎ [H₃O⁺]éq = σ/(λ(H₃O⁺) + λ(A⁻)), en mol·m⁻³. | — |
| `ee_m3_calcul` | Ex. D : [H₃O⁺]éq = 4,6·10⁻³/(39,09·10⁻³) = 0,118 mol·m⁻³ = 1,18·10⁻⁴ mol/L. ⏎ τ = 0,118 ; K = C·τ²/(1 − τ) = 1,58·10⁻⁵ ≈ 1,6·10⁻⁵ : même K que par le pH. | — |
| `ee_m4_national` | 2019 N : τ = σ/(C·(λ₁ + λ₂)) = 8,6·10⁻³/(1,0 × 38,23·10⁻³) ≈ 0,22 (C = 1,0 mol·m⁻³). ⏎ K = C·τ²/(1 − τ) = 1,0·10⁻³ × 0,22²/(1 − 0,22) ≈ 6,2·10⁻⁵ (C en mol/L). | — |
| `ee_z3_dilution` | Diluer : V₀ prélevé à la pipette, fiole jaugée de V₁, eau distillée jusqu'au trait. ⏎ C₀·V₀ = C₁·V₁ ; facteur F = V₁/V₀ (10 mL → 100 mL : diluée 10 fois). | — |
| `ee_f1_dilution` | Même K = 1,6·10⁻⁵ : C = 1,0·10⁻² ; 5,0·10⁻³ ; 1,0·10⁻³ mol/L → τ = 0,039 ; 0,055 ; 0,117. ⏎ Même K : plus C est petite, plus τ est grand. | — |
| `ee_f2_nature` | Même C = 1,0·10⁻² mol/L : K = 1,6·10⁻⁵ → τ = 0,039 ; K = 1,8·10⁻⁴ → τ = 0,13. ⏎ Même C : plus K est grande, plus τ est grand (K traduit la nature de la réaction). | — |
| `ee_f3_courbe` | τ dépend de K (nature de la réaction) et de C (état initial). ⏎ C = 1,0·10⁻⁴ mol/L : τ = 0,33 et 0,72 ; C = 1,0·10⁻¹ mol/L : τ = 0,013 et 0,042. | τ dépend de K et de C |
| `ee_f4_bilan` | Quand on dilue : C ↓ ; [H₃O⁺]éq ↓ ; pH ↑ ; τ ↑ ; K inchangée. ⏎ Attention : τ dépend de l'état initial ; K ne dépend que de la température. | — |
| `ee_n1_national` | 2017 N : Qr,éq = 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = 1,57·10⁻⁵ (sans unité). | — |
| `ee_n2_base` | 2022 R : CH₃NH₂(aq) + H₂O(l) ⇌ CH₃NH₃⁺(aq) + HO⁻(aq) ; [CH₃NH₃⁺]éq = [HO⁻]éq = C_b·τ. ⏎ Qr,éq = C_b·τ²/(1 − τ) = 1,0·10⁻² × 0,20²/(1 − 0,20) = 5,0·10⁻⁴. | — |
| `ee_n3_melange` | 2020 R : V_T = 400 mL ; [X]ᵢ = C·V/V_T (concentrations APRÈS mélange). ⏎ Qr,i = (C₃V₃·C₄V₄)/(C₁V₁·C₂V₂) = 1 (V_T se simplifie). | — |
| `ee_n4_pile` | 2017 N : 3Cu²⁺(aq) + 2Al(s) ⇌ 3Cu(s) + 2Al³⁺(aq) ; solides absents, coefficients en exposants. ⏎ Qr,i = [Al³⁺]ᵢ²/[Cu²⁺]ᵢ³ = (6,5·10⁻¹)²/(6,5·10⁻¹)³ = 1/(6,5·10⁻¹) ≈ 1,5. | — |
| `ee_n5_courbe` | 2017 R : palier n_éq(acide) = 0,2 mol ; x_éq = 0,6 − 0,2 = 0,4 mol. ⏎ K = (0,4 × 0,4)/(0,2 × 0,2) = 4 (V se simplifie) ; ici l'eau est un produit : elle figure. | Lire l'équilibre sur le palier |
| `ee_n6_taux` | 2021 N : τ = 10^(−2,88)/0,10 = 0,0132 ; Qr,éq = 0,10 × 0,0132²/(1 − 0,0132) = 1,77·10⁻⁵. | — |
| `ee_bl_fiche` | Qr (eau solvant et solides absents) ; Qr,i ; Qr,éq = K (ne dépend que de T) ; K' = 1/K. ⏎ τ = 10^(−pH)/C ; K = C·τ²/(1 − τ) ; σ = Σλᵢ·[Xᵢ] ; diluer : τ ↑, K inchangée. | — |
| `ee_cr_carte` | À l'équilibre : Qr,éq = K. Qr,i → Qr évolue → Qr,éq = K ; τ dépend de K et de C. | — |

Version en ligne : même cahier, redécoupé dans son ordre (carte et flacons d'ouverture, pas de diapo sur le couple acide/base ni sur le pH : ils sont écrits en « Rappel : » dans `ee_r_b1` et `ee_s1_b1` ; nationaux groupés en partie VIII ; `ee_m4_national` = 2019 N lu en une diapo, écrit en une ligne dans `ee_s2_b3`).
