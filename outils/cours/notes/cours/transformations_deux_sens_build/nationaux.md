# Transformations dans les deux sens (pH, τ, équilibre) : ce que demandent les nationaux (2016-2025)

Source : `backend/data/exams/physique/<année>-<session>/` (exam.json = énoncé et corrigé ; extraction.json = texte du sujet
officiel et barème dans la marge ; assets/*.png = figures). 20 sessions relues (normale N et rattrapage R), exercice 1 (chimie, 7 pts).
Lecture : questions et corrigés dans exam.json ; barème vérifié sur extraction.json (2017 N, 2019 N, 2020 N, 2021 R, 2023 N, 2025 R) ;
figures regardées : 2021 R figure 3 (τ en fonction du pH), 2025 R figure 1, 2017 N (déjà relevée pour la cinétique).
**Tous les nombres des corrigés ont été recalculés avec python** (valeurs ci-dessous). **Vidéos non auditées** (YouTube bloqué depuis le cloud).

À savoir avant de lire :
- Le chapitre (pH, réaction d'un acide ou d'une base avec l'eau, τ, réaction totale / limitée, conductimétrie, dilution) tombe dans
  **17 sessions sur 20** (11 avec un calcul de τ), toujours dans l'exercice 1 de chimie, toujours **mêlé** aux chapitres suivants (Qr,éq, K, Ka, pKa, Ke,
  prédominance, dosage). Calcul de τ : 2017 N (×2), 2019 N, 2020 N, 2020 R, 2021 N, 2021 R, 2022 N, 2022 R, 2023 N, 2024 R, 2025 R (11 sessions).
- Sessions sans question de ce chapitre au sens strict : 2017 R, 2019 R, 2024 N (dosage, pKa, K seulement) ; 2016 N, 2016 R, 2018 N,
  2018 R n'ont que « deux caractéristiques : lente et limitée » de l'estérification / hydrolyse (0,5 pt) ; 2023 R a « définir une base
  selon Brønsted » et « pH_E < 7 » ; 2025 N a le rendement d'une estérification (= τ).
- Le chemin de calcul est **toujours le même** : équation de l'acide (ou de la base) avec l'eau → tableau d'avancement → x_max = C·V →
  x_f = [H₃O⁺]·V avec [H₃O⁺] = 10^(−pH) (ou par σ) → τ = x_f/x_max = 10^(−pH)/C → « τ < 1 : limitée » (ou « τ = 1 : totale »).
- Ce qui appartient aux CHAPITRES SUIVANTS (renvoyé, jamais enseigné ici) : Qr, Qr,éq, K (→ `etat_equilibre`) ; Ke, [HO⁻] = Ke/[H₃O⁺],
  Ka, pKa, K = Ka₁/Ka₂, pH = pKa + log([A⁻]/[AH]), espèce prédominante, diagramme de distribution, indicateurs colorés, dosage
  (→ `acides_bases`, `dosage`) ; estérification, rendement, anhydride (→ `esterification_hydrolyse`) ; t₁/₂, vitesse (→ `cinetique`).
- Les corrigés du dépôt citent « Henderson-Hasselbalch » / « relation de Henderson » (2021 R, 2022 N, 2023 N, 2023 R) : hors programme
  (perimetre.json) — le cours ne le dit jamais.

---

## 1. Par session

Barème = points du sujet officiel. « ⟶ ch. suivant » = question renvoyée à un autre chapitre.

### 2016 N — acide propanoïque : dosage, puis estérification (partie 2)
- Ce chapitre : 2.1 « deux caractéristiques de la réaction » acide + éthanol (0,5) → **lente et limitée**. Données : n₀ = 0,5 mol de chaque,
  n_E = 0,33 mol → τ (ici « rendement ») = 0,33/0,5 = **0,66** (2.4, 0,5 ⟶ ch. estérification).
- ⟶ ch. suivant : 1.2 K = Ka/Ke ≈ 1,26·10⁹ (0,5) ; 1.4 indicateur ; 1.5 prédominance (pH > pKa).
- Dépôt : corrigés justes (K = 10^(−4,9)/10^(−14) = 1,26·10⁹ recalculé).

### 2016 R — hydrolyse de l'éthanoate d'éthyle, puis saponification
- Ce chapitre : 1.2 « deux caractéristiques » (0,5) → lente et limitée (atteint un état d'équilibre).
- ⟶ ch. suivant : 1.4 K = 0,33²/0,67² ≈ 0,242 (recalculé 0,2426) ; partie 2 = cinétique.

### 2017 N — acide butanoïque + eau (partie II.1), deux estérifications (II.2)
- Données : C = 1,0·10⁻² mol·L⁻¹, pH = 3,41 ; équation donnée C₃H₇COOH + H₂O ⇌ C₃H₇COO⁻ + H₃O⁺.
- Questions : 1.1 τ, en déduire (0,75) → τ = 10^(−3,41)/1,0·10⁻² = **0,039 = 3,9 %** (recalculé 0,0389) : réaction limitée ;
  2.3 τ de chaque estérification (0,75) → courbes x(t) : x_f = 0,2 et 0,3 mol, x_max = 0,3 mol → **τ₁ = 0,67, τ₂ = 1** : la seconde
  (anhydride) est totale.
- ⟶ ch. suivant : 1.2 Qr,éq = 10^(−2pH)/(C − 10^(−pH)) ≈ 1,57·10⁻⁵ (0,75) ; 1.3 pKa ≈ 4,8 (0,5) ; partie I pile (Qr,i).
- Dépôt : 1.1 tronqué « En déduire. » (aussi dans extraction.json : texte OCR coupé) ; corrigé juste.

### 2017 R — estérification acide éthanoïque + éthanol (tubes scellés)
- Rien de ce chapitre au sens strict (composition à l'équilibre, K = 4 ⟶ ch. suivants ; eau glacée ⟶ cinétique).
- Dépôt : équation du corrigé (7) écrite avec « CH₃–C(O)H » (un aldéhyde) au lieu de CH₃–COOH ; barème d'exam.json faux (déjà relevé).

### 2018 N — acide lactique : dosage, puis estérification
- Ce chapitre : 2.1 deux caractéristiques (0,5) → lente et limitée ; n_E = 6·10⁻⁴ mol pour n₀ = 10⁻³ → 60 % (2.4, rendement).
- ⟶ ch. suivant : 1.5 [A⁻]/[AH] = 10^(pH_E − pKa) ≈ 1,26·10⁴ ; indicateur.

### 2018 R — pile zinc-cuivre, hydrolyse de l'éthanoate de méthyle
- Ce chapitre : 1.2 deux caractéristiques (0,5) → lente et limitée.
- ⟶ ch. suivant : Qr,i = 1 et sens d'évolution (pile) ; 1.5 K = 0,2²/0,4² = 0,25.

### 2019 N — acide benzoïque, étude conductimétrique (partie 2) ★
- Données : C = 1,0·10⁻³ mol·L⁻¹, V = 1 L, σ = 8,6·10⁻³ S·m⁻¹ ; λ₁ = λ(H₃O⁺) = 35·10⁻³, λ₂ = λ(C₆H₅COO⁻) = 3,23·10⁻³ S·m²·mol⁻¹ ;
  σ = Σ λᵢ[Xᵢ] rappelée ; ions HO⁻ négligés.
- Questions : 2.1 équation avec l'eau (0,5) ; 2.2 tableau d'avancement (0,75) ; 3.1 σ en fonction de λ₁, λ₂, [H₃O⁺] (0,75)
  → σ = (λ₁ + λ₂)·[H₃O⁺]éq ; 3.2 montrer τ = σ/(C·(λ₁ + λ₂)) et calculer (0,75) → C = 1,0·10⁻³ mol·L⁻¹ = **1,0 mol·m⁻³** →
  τ = 8,6·10⁻³/(1,0 × 38,23·10⁻³) = **0,22** (recalculé 0,225 : 0,22 ou 0,23 acceptés).
- ⟶ ch. suivant : 3.3 K = C·τ²/(1 − τ) (0,75), 3.4 K = Ka (0,25), 3.5 pKa = 4,2 (0,75), 3.6 prédominance (pH = 3,66 < pKa) (0,5).
- Piège : **C en mol·m⁻³** dans τ = σ/(C·(λ₁ + λ₂)) (λ en S·m²·mol⁻¹, σ en S·m⁻¹).
- Dépôt : numérotation 2.3.x au lieu de 3.x (sujet officiel) ; corrigé juste.

### 2019 R — aspirine : dosage, suivi temporel
- Rien de ce chapitre (dosage ⟶ acides_bases/dosage ; suivi ⟶ cinétique).

### 2020 N — ammoniac (partie 1) ★
- Données : C_b = 1,0·10⁻² mol·L⁻¹ (après dosage), pH = 10,6, Ke = 10⁻¹⁴ donné.
- Questions : 2.1 équation de l'ammoniac avec l'eau (0,5) → NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ ; 2.3 τ (0,5) → τ = [HO⁻]/C_b =
  3,98·10⁻⁴/1,0·10⁻² = **0,040 = 4,0 %** (recalculé 0,0398).
- ⟶ ch. suivant : 2.2 [HO⁻] = Ke/[H₃O⁺] = 10^(−3,4) = 3,98·10⁻⁴ mol·L⁻¹ (Ke : acides_bases) ; 2.4 Qr,éq = 1,65·10⁻⁵ ; 2.5 pKa ≈ 9,2 ; dosage.
- **Dépôt : corrigé 2.1 FAUX** : « NH₃ + H₂O ⇌ NH₄⁺ + H₃O⁺ » (charges non conservées) au lieu de NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ ;
  1.1 noté 1,0 pt dans exam.json, 0,5 dans le sujet officiel.
- Pour le cours : τ d'une base passe par [HO⁻], donc par Ke → on écrit l'équation d'une base avec l'eau, le calcul de τ est renvoyé.

### 2020 R — éthanoate de sodium (partie 1) ★
- Données : C = 1,0·10⁻³ mol·L⁻¹, pH = 7,9.
- Questions : 1.1 équation CH₃COO⁻ + H₂O ⇌ CH₃COOH + HO⁻ (0,5) ; 1.3 τ, déduire (0,5) → τ = 7,94·10⁻⁷/1,0·10⁻³ =
  **7,9·10⁻⁴** : limitée (recalculé 7,94·10⁻⁴).
- ⟶ ch. suivant : 1.2 [HO⁻] = Ke·10^pH (Ke) ; 1.4 Qr,éq = C·τ²/(1 − τ) = 6,31·10⁻¹⁰ ; 1.5 pKa = 4,8 ; partie 2 : K = Ka₂/Ka₁ = 10, Qr,i, pH = 4,27.

### 2021 N — partie 2 : acide carboxylique inconnu ★
- Données : C_a = 1,0·10⁻¹ mol·L⁻¹ (dosage), pH = 2,88.
- Questions : II.1 équation AH + H₂O ⇌ A⁻ + H₃O⁺ (0,25) ; II.2 montrer τ ≈ 1,32 % (0,75) → 10^(−2,88)/10⁻¹ = **0,0132** (recalculé 0,01318).
- ⟶ ch. suivant : II.3 Qr,éq = C·τ²/(1 − τ) ≈ 1,77·10⁻⁵ ; II.4 pKa = 4,75 → acide éthanoïque ; III : V_b1 avec pH = pKa + log.
- Dépôt : titre « Partie 2 » collé à la question de cinétique 2.1 (définir t₁/₂), déjà relevé ; corrigé juste.

### 2021 R — acide méthanoïque, **influence de la dilution sur τ** (partie 1, III) ★★
- Données : C_a = 0,10 mol·L⁻¹ (dosage), pH = 2,38 ; figure 3 : **τ en fonction du pH** de solutions diluées (courbe en S de 0 à 1).
- Questions : II.1 équation avec l'eau (0,5) ; III.1 montrer τ = 10^(−pH)/C (0,25) ; III.2 compléter le tableau (0,5) : pH 2,8 →
  τ ≈ 0,10 → C = 10^(−2,8)/0,10 = **1,58·10⁻² mol·L⁻¹** ; pH 3,6 → τ ≈ 0,45 → C = 10^(−3,6)/0,45 = **5,58·10⁻⁴ mol·L⁻¹** ;
  III.3 effet de la dilution (0,25) → **plus C est petite (solution diluée), plus τ est grand**.
- ⟶ ch. suivant : II.2.1 [A⁻]/[AH] = 10^(−pH)/(C − 10^(−pH)) = 4,35·10⁻² ; II.2.2 prédominance ; II.3 pKa = 3,74 ; dosage.
- Piège : lire τ sur la figure (axe 0 → 1, pas en %) puis isoler C, pas τ.
- Dépôt : corrigé II.3 nomme « Henderson-Hasselbalch » (hors programme) ; τ(3,6) lu 0,45 (une courbe calculée avec pKa = 3,74 donne
  0,42 : écart de lecture, résultat accepté).

### 2022 N — acide propanoïque (partie 2) ★
- Données : C_a = 5,0·10⁻² mol·L⁻¹, pH = 3,1.
- Questions : 1.1 équation avec l'eau (0,5) ; 1.2 τ, conclure (0,75) → 10^(−3,1)/5·10⁻² = **0,016 = 1,6 %** : limitée (recalculé 0,0159).
- ⟶ ch. suivant : 1.3 Qr,éq = 1,28·10⁻⁵ ; 1.4 pKa = 4,9 ; 2 dosage, dilution 10 fois (C₀, m = 37 g), % de forme acide = 76 %.
- Dépôt : équation du dosage écrite avec ⇌ au lieu de → ; « Henderson-Hasselbalch » nommé (2.5).

### 2022 R — méthylamine (partie 2) ★
- Données : C_b = 1,0·10⁻² mol·L⁻¹, pH = 11,3, Ke donné.
- Questions : 1.1 **définir une base selon Brønsted** (0,25) → espèce capable de capter un proton H⁺ ; 1.2 équation
  CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + HO⁻ (0,25) ; 1.3 τ, déduire (0,5) → [HO⁻] = 10^(−2,7) = 2,0·10⁻³ → τ = **0,20** : limitée.
- ⟶ ch. suivant : [HO⁻] par Ke ; 1.4 Qr,éq = 5,0·10⁻⁴ ; 1.5 pKa = 10,7 ; dosage, indicateur, rapport [base]/[acide].

### 2023 N — acide éthanoïque (partie 1) ★
- Données : C_A = 5,0·10⁻² mol·L⁻¹, pH = 3,05.
- Questions : 1.1 équation avec l'eau (0,5) ; 1.2 **montrer α(CH₃COOH) = 1 − τ** avec le tableau d'avancement et calculer (0,75) →
  τ = 10^(−3,05)/5·10⁻² = 0,0178 → **α = 0,982 = 98,2 %**.
- ⟶ ch. suivant : 1.3 pKa = 4,79 ; partie 2 Qr,éq = Ka₁/Ka₂, pH = (pKa₁ + pKa₂)/2 ; partie 3 estérification (cinétique, rendement 66,7 %, K = 4).
- Dépôt : « relation de Henderson » (2.3) ; corrigé juste.

### 2023 R — triméthylamine (partie 2)
- Ce chapitre : 2.1 **définir une base selon Brønsted** (0,5) ; 2.5 justifier pH_E < 7 (0,5) → (CH₃)₃NH⁺ est un acide qui réagit avec l'eau
  et forme H₃O⁺ (équation de l'acide avec l'eau).
- ⟶ ch. suivant : dosage, indicateur, pKa = pH à la demi-équivalence (9,9).
- Dépôt : « Henderson-Hasselbalch » nommé (2.8).

### 2024 N — vitamine C (suivi temporel, dosage)
- Rien de ce chapitre (1.c « chocs » et t₁/₂ ⟶ cinétique ; pKa, K = 8,13·10⁹ ⟶ acides_bases).

### 2024 R — amine R–NH₂ (partie 2) ★
- Données : C_B = 9,0·10⁻² mol·L⁻¹, pH = 11,88 ; dosage V_B = 10,0 mL par C_A = 4,5·10⁻² mol·L⁻¹ ; à V_A = 16,0 mL, pH = 10,2.
- Questions : 1.1 équation R–NH₂ + H₂O ⇌ R–NH₃⁺ + HO⁻ (0,5) ; 2.3 exprimer x_f en fonction de C_A, V_A, V_B et pH (0,75) →
  x_f = C_A·V_A − 10^(−pH)·(V_A + V_B) = **7,2·10⁻⁴ mol** (le second terme vaut 1,6·10⁻¹² mol) ; 2.4 τ de la réaction de dosage (0,75)
  → x_max = C_A·V_A = 7,2·10⁻⁴ mol → **τ = 1 : la réaction de dosage est totale**.
- ⟶ ch. suivant : 1.2 pKa = 10,8 (diagramme de distribution), prédominance, pH pour 80 % d'acide (10,2) ; V_AE = 20,0 mL.
- Dépôt : HO⁻ écrit « OH⁻ » dans le corrigé 1.1 (notation du sujet : HO⁻).

### 2025 N — hydrogénosulfite (dosage), estérification (cinétique)
- Ce chapitre : 2.5 rendement de l'expérience 3 (0,5) → x_f/x_max = 133/200 = 66,5 % (même calcul que τ ; ⟶ ch. estérification).
- ⟶ ch. suivant : 1.5 K = Ka/Ke = 10^6,8 ; dosage.

### 2025 R — acide éthanoïque (partie 1) ★★
- Données : C_A = 4,2·10⁻³ mol·L⁻¹, pH = 3,6 ; figure 1 : pourcentages de CH₃COOH et CH₃COO⁻ en fonction du pH.
- Questions : 1.1 équation avec l'eau (0,5) ; 1.2 exprimer τ en fonction de C_A et pH, calculer (0,5) → 10^(−3,6)/4,2·10⁻³ = **0,060**
  (recalculé 0,0598) ; 1.4.3 après dilution, pH₁ = 4,2 : τ₁ lu sur la figure (= % de CH₃COO⁻) ≈ **0,20** ; effet de la dilution (0,5)
  → **la dilution augmente τ** (0,06 → 0,20).
- ⟶ ch. suivant : 1.3 pKa = 4,8 ; 1.4.1 pKa sur la figure (croisement) ; 1.4.2 courbe de l'acide ; parties 2 et 3 estérification, cinétique.
- Note : la lecture de τ₁ sur un diagramme de distribution appartient au chapitre acide-base ; ici on garde la conclusion « dilution → τ augmente ».

---

## 2. Bilan des cas types (ce chapitre seulement)

| Cas type | Sessions | Points |
|---|---|---|
| Écrire l'équation d'un acide (ou d'une base) avec l'eau | 2017 N (donnée), 2019 N, 2020 N, 2020 R, 2021 N, 2021 R, 2022 N, 2022 R, 2023 N, 2024 R, 2025 R (11) | 0,25-0,5 |
| Calculer τ à partir du pH : τ = 10^(−pH)/C, conclure « limitée » | 2017 N, 2021 N, 2021 R, 2022 N, 2023 N, 2025 R (6) ; base par [HO⁻] : 2020 N, 2020 R, 2022 R (3, Ke ⟶ ch. suivant) | 0,5-0,75 |
| Montrer une expression de τ (τ = 10^(−pH)/C, τ = σ/(C(λ₁+λ₂)), α = 1 − τ) | 2019 N, 2021 R, 2023 N, 2025 R | 0,25-0,75 |
| Tableau d'avancement de la réaction avec l'eau | 2019 N (0,75) ; implicite partout | 0,75 |
| Conductimétrie → [H₃O⁺] → τ | 2019 N | 1,5 |
| Influence de la dilution sur τ | 2021 R, 2025 R | 0,25-0,75 |
| Réaction totale (τ = 1) : dosage, anhydride | 2017 N 2.3, 2024 R 2.4 | 0,75 |
| Définir un acide / une base selon Brønsted | 2022 R, 2023 R | 0,25-0,5 |
| « Deux caractéristiques » : lente et limitée (estérification, hydrolyse) | 2016 N, 2016 R, 2018 N, 2018 R | 0,5 |

Valeurs de τ rencontrées : 7,9·10⁻⁴ ; 1,3 % ; 1,6 % ; 1,8 % ; 3,9 % ; 4,0 % ; 6 % ; 20 % ; 22 % ; 67 % ; 1.
pH rencontrés : 2,38 ; 2,88 ; 3,05 ; 3,1 ; 3,41 ; 3,6 ; 7,9 ; 10,2 ; 10,6 ; 11,3 ; 11,88.

## 3. Pièges où l'élève perd des points
- Oublier le signe moins : [H₃O⁺] = 10^(−pH), pas 10^(pH) ; pH = −log[H₃O⁺].
- Prendre x_f = C·V (réaction supposée totale) : x_f vient de la MESURE (pH ou σ), x_max du calcul.
- Écrire τ = x_max/x_f (inversé) ; donner τ > 1.
- Pour une base, utiliser [H₃O⁺] au lieu de [HO⁻] dans τ (2020 N, 2020 R, 2022 R).
- En conductimétrie, garder C ou [H₃O⁺] en mol·L⁻¹ avec λ en S·m²·mol⁻¹ : 1 mol·L⁻¹ = 10³ mol·m⁻³ (2019 N).
- Oublier que [CH₃COO⁻] = [H₃O⁺] (tableau) : σ = (λ₁ + λ₂)·[H₃O⁺].
- Écrire l'équation avec → au lieu de ⇌ pour une réaction limitée (et l'inverse pour un dosage).
- « La dilution diminue τ » : c'est le contraire (2021 R, 2025 R).
- Conclure « limitée » sans comparer τ à 1 (la conclusion vaut une partie des points).

## 4. Erreurs du dépôt (exam.json) qui touchent ce chapitre
1. **2020 N 2.1** : équation de l'ammoniac avec l'eau écrite « NH₃ + H₂O ⇌ NH₄⁺ + H₃O⁺ » : FAUX (charges et H non conservés) ;
   juste : NH₃ + H₂O ⇌ NH₄⁺ + HO⁻. Barème 1.1 = 1,0 dans exam.json, 0,5 dans le sujet.
2. **2017 R 7** : équation d'estérification avec « CH₃–C(O)H » (aldéhyde) au lieu de l'acide CH₃–COOH.
3. **2017 N 1.1** : énoncé tronqué « En déduire. » (texte officiel OCR coupé lui aussi).
4. **2019 N** : questions numérotées 2.3.1-2.6 au lieu de 3.1-3.6 ; τ = 0,225 arrondi à 0,22.
5. **Henderson-Hasselbalch** nommé dans les corrigés 2021 R, 2022 N, 2023 N, 2023 R (hors programme, perimetre.json).
6. **2022 N 2.1** : équation de dosage avec ⇌ (le dosage est total : →).
7. **2024 R 1.1** : « OH⁻ » au lieu de HO⁻ (notation marocaine).
8. **2021 R III.2** : τ(3,6) lu 0,45 ; cohérent avec la figure à ± 0,03 (pas une erreur, mais à dessiner tel quel).

---

## 5. Figures pour figures.html

| Clé | Diapositive | Session | Contenu |
|---|---|---|---|
| fig_2017N | e6 | 2017 N | deux courbes x(t) d'estérification : τ₁ = 0,67, τ₂ = 1 |
| fig_2021R | n1 | 2021 R | τ en fonction du pH (dilution) |

Les nationaux repris sans figure (2019 N, 2023 N, 2024 R) sont dessinés par leurs pages : conductimetrie?vue=national,
avancement?vue=proportion, avancement?vue=dosage.

### fig_2017N (e6) — 2017 N, deux estérifications (même figure que cinetique_build/nationaux.md)
- Ordonnée : x (mol), 0 → 0,35, pas 0,1. Abscisse : t (min), 0 → 75, pas 20.
- Points (t ; x₁ ; x₂) : (0 ; 0 ; 0) (2 ; 0,032 ; 0,150) (5 ; 0,070 ; 0,247) (8 ; 0,100 ; 0,281) (10 ; 0,116 ; 0,291)
  (20 ; 0,165 ; 0,300) (40 ; 0,194 ; 0,300) (60 ; 0,199 ; 0,300).
- À lire : paliers x_f₁ = 0,2 mol, x_f₂ = 0,3 mol ; x_max = 0,3 mol (trait pointillé).
- Question posée (2.3, 0,75) : τ de chaque expérience, laquelle est totale.
- Réponse au barème : τ₁ = 0,2/0,3 = 0,67 ; τ₂ = 0,3/0,3 = 1 ; la réaction de l'anhydride (2) est totale.

### fig_2021R (n1) — 2021 R, τ en fonction du pH
- Ordonnée : τ, 0 → 1, graduations 0,5 et 1 (petites divisions 0,1). Abscisse : pH, 0 → 7, graduations 2, 4, 6 (petites divisions 0,2).
- Points (courbe en S passant par les valeurs du corrigé ; modèle de calcul jamais écrit) : (1 ; 0,00) (2 ; 0,015) (2,5 ; 0,05)
  (2,8 ; 0,10) (3 ; 0,155) (3,3 ; 0,28) (3,6 ; 0,45) (4 ; 0,69) (4,5 ; 0,885) (5 ; 0,964) (5,5 ; 0,99) (6 ; 1,00) (7 ; 1,00).
- À lire : pH = 2,8 → τ ≈ 0,10 ; pH = 3,6 → τ ≈ 0,45.
- Question posée (III.1 0,25 ; III.2 0,5 ; III.3 0,25) : montrer τ = 10^(−pH)/C ; compléter τ et C pour S₁ et S₂ ; effet de la dilution.
- Réponse au barème : τ = x_f/x_max = [H₃O⁺]·V/(C·V) = 10^(−pH)/C ; C₁ = 10^(−2,8)/0,10 = 1,58·10⁻² mol·L⁻¹ ;
  C₂ = 10^(−3,6)/0,45 = 5,58·10⁻⁴ mol·L⁻¹ ; C₂ < C₁ et τ₂ > τ₁ : la dilution augmente τ.
