# État d'équilibre d'un système chimique (Qr, Qr,éq, K) : ce que demandent les nationaux (2016-2025)

Source : `backend/data/exams/physique/<année>-<session>/` (exam.json = énoncé et corrigé ; extraction.json = texte du sujet officiel et
barème dans la marge ; assets/*.png = figures). 20 sessions relues (normale N et rattrapage R), exercice 1 (chimie, 7 pts).
Lecture : questions et corrigés dans exam.json ; barème vérifié sur extraction.json (2017 N, 2018 R, 2019 R, 2020 N, 2020 R, 2021 N, 2022 N,
2022 R) ; figure regardée : 2017 R (n(acide) en fonction de t, estérification). Chapitre précédent déjà relevé :
`outils/cours/notes/cours/transformations_deux_sens_build/nationaux.md` (τ, pH, conductimétrie, dilution).
**Tous les nombres des corrigés ont été recalculés avec python** (valeurs ci-dessous). **Vidéos non auditées** (YouTube bloqué depuis le cloud).

À savoir avant de lire :
- Le chapitre (Qr, Qr,i, Qr,éq, K, K en fonction de C et τ ou de C et pH) tombe dans **12 sessions sur 20** (2016 R, 2017 N, 2017 R, 2018 R,
  2019 N, 2019 R, 2020 N, 2020 R, 2021 N, 2022 N, 2022 R, 2023 N ; 15 en comptant les K exprimées avec Ka, Ke), toujours dans l'exercice 1 de chimie,
  toujours **mêlé** : juste après le calcul de τ (chapitre 11) et juste avant pKa (chapitre 13), ou au début d'un exercice de pile (semestre 2),
  ou dans un exercice d'estérification (semestre 2).
- Quatre familles de questions :
  1. **Qr,éq (ou K) d'un acide ou d'une base avec l'eau, à partir du pH, de τ ou de σ** : 2017 N, 2019 N, 2020 N, 2020 R, 2021 N, 2022 N,
     2022 R (7 sessions, 0,5-0,75 pt) — le cœur du chapitre. Expressions demandées : Qr,éq = 10^(−2pH)/(C − 10^(−pH)) (2017 N),
     Qr,éq = [H₃O⁺]²/(C − [H₃O⁺]) (2022 N), Qr,éq = K = C·τ²/(1 − τ) (2019 N, 2020 R, 2021 N, 2022 R).
  2. **Qr,i dans l'état initial** : pile (2017 N, 2018 R, 2019 R : solides absents de Qr, coefficients en exposants) et mélange de deux
     couples (2020 R : concentrations après mélange) — 4 sessions, 0,5 pt. La question suivante (« en déduire le sens d'évolution
     spontanée », 0,5 pt) compare Qr,i à K : critère du chapitre « piles » (perimetre.json, clé piles_electrolyse) ⟶ renvoyé.
  3. **K d'une estérification / hydrolyse à partir des quantités à l'équilibre** : 2016 R, 2017 R, 2018 R (+ 2023 N 3.6 qui utilise K = 4)
     — même définition K = Qr,éq, mais l'eau n'y est PAS le solvant (elle figure dans K) ⟶ chapitre esterification_hydrolyse (semestre 2).
  4. **K d'une réaction acide-base exprimée avec Ka et Ke** (K = Ka/Ke, K = Ka₁/Ka₂, « K représente Ka ») : 2016 N, 2019 N 2.5, 2020 R 2.2,
     2023 N 2.2, 2024 N 5-4, 2025 N 1.5 ⟶ chapitre 13 (acides_bases) ; renvoyé.
- Ce que le chapitre ne fait PAS (renvoyé) : Ka, pKa, Ke, [HO⁻] = Ke/[H₃O⁺], prédominance, K = Ka₁/Ka₂ (chapitre 13) ; critère d'évolution
  (Qr,i < K → sens direct) et piles (semestre 2) ; rendement, K = 4 de l'estérification (semestre 2) ; « K > 10⁴ : réaction totale » (2016 N,
  dosage, chapitre 13).
- Les corrigés du dépôt citent « relation de Henderson » (2023 N 2.3) : hors programme (perimetre.json) — le cours ne le dit jamais.

---

## 1. Par session

Barème = points du sujet officiel. « ⟶ ch. 11 » = chapitre précédent (déjà fait) ; « ⟶ ch. 13 » = réactions acide-base ; « ⟶ S2 » = semestre 2.

### 2016 N — acide propanoïque : dosage, estérification
- Rien de ce chapitre au sens strict. 1.2 « En calculant K de la réaction du dosage, montrer qu'elle est totale » (0,5) → K = Ka/Ke =
  10^(−4,9)/10^(−14) = **1,26·10⁹** (recalculé 1,259·10⁹) « ≫ 10⁴ : totale » ⟶ ch. 13 (Ka, Ke) et dosage.
- Estérification « lente et limitée », rendement 0,66 ⟶ ch. 11 / S2.

### 2016 R — hydrolyse de l'éthanoate d'éthyle
- 1.4 Calculer K (0,5) : 1 mol d'ester + 1 mol d'eau, il reste 0,67 mol d'ester → x_éq = 0,33 mol →
  K = (0,33·0,33)/(0,67·0,67) = **0,242** (recalculé 0,2426). Méthode K = Qr,éq avec les quantités (V se simplifie) ⟶ S2 (estérification).
- Dépôt : corrigé juste.

### 2017 N — pile aluminium-cuivre (partie I), acide butanoïque (partie II.1) ★
- Partie I, 1 : **expression de Qr,i puis valeur** (0,5) : 3Cu²⁺ + 2Al(s) ⇌ 3Cu(s) + 2Al³⁺, [Cu²⁺]ᵢ = [Al³⁺]ᵢ = 6,5·10⁻¹ mol/L →
  Qr,i = [Al³⁺]ᵢ²/[Cu²⁺]ᵢ³ = 0,65²/0,65³ = **1,5** (recalculé 1,538). Solides absents, coefficients en exposants.
  2 : sens d'évolution spontanée (0,5) → Qr,i = 1,5 < K = 10²⁰⁰ : sens direct ⟶ S2 (critère).
- Partie II.1 : C = 1,0·10⁻² mol/L, pH = 3,41 ; 1.1 τ = 0,039 (0,75) ⟶ ch. 11 ; **1.2 Qr,éq en fonction de C et du pH, puis valeur** (0,75) →
  Qr,éq = [H₃O⁺]²/(C − [H₃O⁺]) = 10^(−2pH)/(C − 10^(−pH)) = 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = **1,57·10⁻⁵** (recalculé 1,575·10⁻⁵).
- ⟶ ch. 13 : 1.3 pKa = −log Qr,éq ≈ 4,8. II.2 estérification (t₁/₂, τ = 0,67 et 1) ⟶ ch. 10, 11.
- Dépôt : énoncé et extraction écrivent l'équation donnée avec « ⟵(1) » (double flèche mal lue par l'OCR) ; corrigés justes.

### 2017 R — argenture, estérification (tubes)
- 8 composition à l'équilibre (0,75) : n₀ = 0,6 mol de chaque ; palier n(acide) = 0,2 mol lu sur la figure → x_éq = 0,4 mol.
  **9 Montrer que K = 4** (0,75) → K = (0,4 × 0,4)/(0,2 × 0,2) = **4** (V se simplifie) ⟶ S2 (estérification ; l'eau, produit, figure dans K).
- Dépôt : 7 équation avec « CH₃–C(O)H » (aldéhyde) au lieu de l'acide (déjà relevé au ch. 11) ; la figure (assets/figcidessousp3.png) est
  quadrillée jusqu'à 0,5 mol environ : le départ n₀ = 0,6 mol n'y est pas visible (courbe coupée en haut) ; le palier 0,2 mol est net.

### 2018 N — électrolyse, acide lactique
- Rien de ce chapitre (rapport [A⁻]/[AH] = 10^(pH − pKa) ⟶ ch. 13 ; estérification ⟶ S2).

### 2018 R — pile zinc-cuivre, hydrolyse d'un ester ★
- 1 : **calculer Qr,i** (0,5) : Cu²⁺ + Zn(s) ⇌ Cu(s) + Zn²⁺, C₁ = C₂ = 1 mol/L → Qr,i = [Zn²⁺]ᵢ/[Cu²⁺]ᵢ = **1**.
  2 : sens (0,5) → Qr,i = 1 < K = 1,7·10³⁷ : sens direct ⟶ S2.
- II 1.5 : K de l'hydrolyse (0,75) : 0,6 mol d'ester, il en reste 0,4 → x_éq = 0,2 mol → K = (0,2 × 0,2)/(0,4 × 0,4) = **0,25** ⟶ S2.
- Dépôt : énoncé ET extraction écrivent « Q_{t,i} » (pour Qr,i) et « Cu²⁺ + Zn ⇌ **2** Zn²⁺ + Cu » (coefficient 2 parasite, équation non
  équilibrée) ; le corrigé utilise la bonne équation (Cu²⁺ + Zn ⇌ Zn²⁺ + Cu).

### 2019 N — acide benzoïque, conductimétrie (partie 2) ★★
- Données : C = 1,0·10⁻³ mol/L, V = 1 L, σ = 8,6·10⁻³ S/m, λ₁ = λ(H₃O⁺) = 35·10⁻³, λ₂ = λ(C₆H₅COO⁻) = 3,23·10⁻³ S·m²·mol⁻¹.
- ⟶ ch. 11 : équation (0,5), tableau (0,75), σ = (λ₁ + λ₂)·[H₃O⁺] (0,75), τ = σ/(C(λ₁ + λ₂)) = **0,22** avec C = 1,0 mol/m³ (0,75).
- **3.3 (dépôt 2.4) : K en fonction de C et τ** (0,75) → [A⁻]éq = [H₃O⁺]éq = C·τ, [AH]éq = C(1 − τ) → **K = C·τ²/(1 − τ)**
  = 1,0·10⁻³ × 0,22²/(1 − 0,22) = **6,2·10⁻⁵** (recalculé 6,205·10⁻⁵ ; avec τ = 0,225 : 6,53·10⁻⁵).
- ⟶ ch. 13 : 3.4 « K représente Ka » (0,25) ; 3.5 pKa = 4,2 (0,75) ; 3.6 prédominance (0,5).
- Dépôt : numérotation 2.3.1-2.7 au lieu de 3.1-3.6 (sujet officiel) ; corrigé juste.

### 2019 R — pile nickel-cadmium, aspirine
- 1 : **Qr,i puis sens** (0,5 pour les deux) : Ni²⁺ + Cd(s) ⇌ Ni(s) + Cd²⁺, C = 1 mol/L pour les deux → Qr,i = [Cd²⁺]ᵢ/[Ni²⁺]ᵢ = **1** ;
  Qr,i < K = 4,5·10⁵ → sens direct (moitié ⟶ S2).
- Dépôt : équation des données écrite « ⟵(1) » (OCR) ; corrigé juste.

### 2020 N — ammoniac (partie 1) ★
- Données : C_b = 1,0·10⁻² mol/L, pH = 10,6. [HO⁻] = Ke/[H₃O⁺] = 3,98·10⁻⁴ mol/L et τ = 0,040 ⟶ ch. 13 (Ke) / ch. 11.
- **2.4 Vérifier Qr,éq = 1,65·10⁻⁵** (0,5) → Qr,éq = [NH₄⁺]éq·[HO⁻]éq/[NH₃]éq = [HO⁻]²/(C_b − [HO⁻]) = (3,98·10⁻⁴)²/(1,0·10⁻² − 3,98·10⁻⁴)
  = **1,65·10⁻⁵** (recalculé 1,650·10⁻⁵).
- ⟶ ch. 13 : 2.5 pKa = 9,2 (Ka = Ke/Qr,éq).
- Dépôt : **corrigé 2.1 FAUX** (NH₃ + H₂O ⇌ NH₄⁺ + H₃O⁺, déjà relevé au ch. 11) ; le 2.4 est juste (il utilise HO⁻).

### 2020 R — éthanoate de sodium, mélange de deux couples, pile ★★
- I : C = 1,0·10⁻³ mol/L, pH = 7,9 ; τ = 7,94·10⁻⁴ (via Ke ⟶ ch. 13). **1.4 Qr,éq en fonction de C et τ, puis valeur** (0,5) →
  [CH₃COOH]éq = [HO⁻]éq = C·τ, [CH₃COO⁻]éq = C(1 − τ) → Qr,éq = C·τ²/(1 − τ) = **6,31·10⁻¹⁰** (recalculé 6,309·10⁻¹⁰).
- II : mélange de 4 solutions (100 mL chacune, 0,1 mol/L) : HCOOH, CH₃COO⁻, CH₃COOH, HCOO⁻ ; HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH.
  **2.3 Qr,i** (0,5) → concentrations après mélange (V_T = 400 mL) : Qr,i = (C₃V₃·C₄V₄)/(C₁V₁·C₂V₂) = **1** (V_T se simplifie).
  ⟶ ch. 13 : 2.2 K = Ka₂/Ka₁ = 10^(4,8 − 3,8) = **10** ; ⟶ S2 : 2.4 Qr,i = 1 < K = 10 : sens direct (0,5) ; 2.5 pH = 4,27 (pKa + log ⟶ ch. 13).
- Dépôt : corrigés justes.

### 2021 N — acide carboxylique inconnu (partie 2) ★
- C_a = 1,0·10⁻¹ mol/L, pH = 2,88 ; τ = 1,32 % ⟶ ch. 11.
- **2.3 Qr,éq en fonction de C_a et τ, vérifier 1,77·10⁻⁵** (0,75) → Qr,éq = C_a·τ²/(1 − τ) = 0,10 × 0,0132²/(1 − 0,0132) = **1,77·10⁻⁵**
  (recalculé 1,766·10⁻⁵ avec τ arrondi ; 1,761·10⁻⁵ avec τ non arrondi).
- ⟶ ch. 13 : 2.4 pKa = 4,75 → acide éthanoïque ; 3 dosage (pH = pKa + log).

### 2021 R — acide méthanoïque, dilution
- Rien de ce chapitre au sens strict (rapport [A⁻]/[AH], pKa ⟶ ch. 13 ; τ et dilution ⟶ ch. 11).
- Lien utile : la figure τ(pH) montre que τ change avec la dilution ; ce chapitre explique POURQUOI (même K, C différente).

### 2022 N — acide propanoïque (partie 2) ★
- C_a = 5,0·10⁻² mol/L, pH = 3,1 ; τ = 0,016 ⟶ ch. 11.
- **1.3 Qr,éq en fonction de C_a et [H₃O⁺]éq, puis valeur** (0,75) → Qr,éq = [H₃O⁺]éq²/(C_a − [H₃O⁺]éq), [H₃O⁺]éq = 10^(−3,1) = 7,94·10⁻⁴ →
  **1,28·10⁻⁵** (recalculé 1,282·10⁻⁵).
- ⟶ ch. 13 : 1.4 pKa = 4,9 ; dosage ; « Henderson-Hasselbalch » nommé (2.5).
- Dépôt : extraction.json lit « Q_{f,gq} » (OCR) ; exam.json juste.

### 2022 R — méthylamine (partie 2) ★
- C_b = 1,0·10⁻² mol/L, pH = 11,3 ; [HO⁻] = 2,0·10⁻³ mol/L (Ke ⟶ ch. 13) ; τ = 0,20 ⟶ ch. 11.
- **1.4 Montrer Qr,éq = C_b·τ²/(1 − τ), calculer** (0,5) → [CH₃NH₃⁺]éq = [HO⁻]éq = C_b·τ, [CH₃NH₂]éq = C_b(1 − τ) →
  Qr,éq = 1,0·10⁻² × 0,20²/0,80 = **5,0·10⁻⁴**.
- ⟶ ch. 13 : 1.5 Ka = Ke/Qr,éq, pKa ≈ 10,7 ; dosage.
- Dépôt : extraction lit « Q_{r,dq} » (OCR) ; exam.json juste.

### 2023 N — acide éthanoïque, mélange avec le méthanoate, estérification
- ⟶ ch. 13 : 2.2 Qr,éq de CH₃COOH + HCOO⁻ ⇌ CH₃COO⁻ + HCOOH en fonction de Ka₁ et Ka₂ (0,75) → Ka₁/Ka₂ = 10^(3,75 − 4,79) = **9,1·10⁻²** ;
  2.3 pH = (pKa₁ + pKa₂)/2 = 4,27 (« relation de Henderson » dans le corrigé : hors programme).
- ⟶ S2 : 3.6 K = 4 et ajout de 0,1 mol d'acide → (0,6 + x)²/((0,4 − x)(0,3 − x)) = 4 → x = 0,031 mol → rendement 70 % (recalculé 70,1 %).

### 2023 R — électrolyse, triméthylamine
- Rien de ce chapitre (Brønsted ⟶ ch. 11 ; dosage, pKa ⟶ ch. 13).

### 2024 N — vitamine C
- ⟶ ch. 13 : 5-4 K de la réaction de dosage (0,5) = Ka/Ke = 10^(14 − 4,09) = **8,13·10⁹** (recalculé 8,128·10⁹).
- Dépôt : corrigé réduit à « Démarche K = 8,13·10⁹ » (aucune ligne de calcul).

### 2024 R — pile fer-zinc, amine
- Rien de ce chapitre (τ = 1 du dosage ⟶ ch. 11 ; pKa ⟶ ch. 13).

### 2025 N — hydrogénosulfite, estérification
- ⟶ ch. 13 : 1.5 K du dosage = Ka/Ke = 10^6,8 = **6,31·10⁶** (0,75).

### 2025 R — acide éthanoïque, estérification
- Rien de ce chapitre au sens strict (τ, dilution ⟶ ch. 11 ; pKa ⟶ ch. 13).

---

## 2. Bilan des cas types (ce chapitre seulement)

| Cas type | Sessions | Points |
|---|---|---|
| Exprimer Qr,éq (ou K) d'un acide ou d'une base avec l'eau en fonction de C et pH / [H₃O⁺] / τ, puis calculer | 2017 N, 2019 N, 2020 N, 2020 R, 2021 N, 2022 N, 2022 R (7) | 0,5-0,75 |
| Écrire Qr,i (solides absents, exposants) et le calculer | 2017 N, 2018 R, 2019 R (piles), 2020 R (mélange) (4) | 0,5 (+ 0,5 sens ⟶ S2) |
| K = Qr,éq à partir des quantités à l'équilibre (estérification / hydrolyse) | 2016 R, 2017 R, 2018 R (3) | 0,5-0,75 (⟶ S2) |
| K exprimée avec Ka, Ke (K = Ka/Ke, Ka₁/Ka₂) | 2016 N, 2019 N, 2020 R, 2023 N, 2024 N, 2025 N (6) | 0,25-0,75 (⟶ ch. 13) |
| Effet de la dilution sur τ (K inchangée) | 2021 R, 2025 R (question de τ, ch. 11 ; l'explication par K est de ce chapitre) | 0,25-0,5 |

Valeurs de Qr,éq / K rencontrées (acide ou base avec l'eau) : 6,31·10⁻¹⁰ ; 1,28·10⁻⁵ ; 1,57·10⁻⁵ ; 1,65·10⁻⁵ ; 1,77·10⁻⁵ ; 6,2·10⁻⁵ ; 5,0·10⁻⁴.
Qr,i rencontrés : 1 (2018 R, 2019 R, 2020 R) ; 1,5 (2017 N). K (estérification, hydrolyse) : 4 ; 0,25 ; 0,242.

## 3. Pièges où l'élève perd des points
- Écrire [H₂O] (l'eau solvant) ou un solide ([Zn], [Cu]) dans Qr : ils n'y figurent pas.
- Oublier les coefficients en exposants (2017 N : [Al³⁺]²/[Cu²⁺]³).
- Inverser Qr (réactifs en haut) ; ou écrire K de la réaction inverse sans passer à 1/K.
- Remplacer [AH]éq par C (oublier « C − [H₃O⁺]éq » ou « C(1 − τ) ») : 2017 N, 2022 N le demandent explicitement.
- Donner une unité à Qr ou à K (sans unité ; concentrations en mol/L).
- Prendre les concentrations AVANT mélange pour Qr,i (2020 R : diviser par V_T, qui se simplifie ensuite).
- Croire que K dépend de la concentration initiale (ou de la dilution) : seul τ en dépend ; K ne dépend que de la température.
- Arrondir τ trop tôt (2019 N : 0,22 ou 0,225 donnent 6,2·10⁻⁵ ou 6,5·10⁻⁵) : garder 3 chiffres dans les calculs intermédiaires.
- « Montrer que » sans partir de la définition de Qr,éq et du tableau d'avancement (2019 N, 2020 R, 2021 N, 2022 R).

## 4. Erreurs du dépôt (exam.json / extraction.json) qui touchent ce chapitre
1. **2018 R I** : « Q_{t,i} » au lieu de Qr,i, et « Cu²⁺ + Zn ⇌ 2 Zn²⁺ + Cu » (coefficient 2 parasite) dans l'énoncé et l'extraction ; le corrigé
   utilise Cu²⁺ + Zn ⇌ Zn²⁺ + Cu (juste).
2. **2017 N I, 2019 R I** : la double flèche des données lue « ⟵(1) » par l'OCR (énoncé et extraction).
3. **2022 N 1.3** « Q_{f,gq} », **2022 R 1.4** « Q_{r,dq} » dans extraction.json (OCR) ; exam.json juste.
4. **2019 N** : numérotation 2.3.1-2.7 au lieu de 3.1-3.6 ; K = C·τ²/(1 − τ) noté 2.4 (officiel 3.3).
5. **2020 N 2.1** : équation de l'ammoniac avec l'eau fausse (H₃O⁺ au lieu de HO⁻), sans effet sur 2.4 (déjà relevé au ch. 11).
6. **2024 N 5-4** : corrigé sans démarche (« Démarche K = 8,13·10⁹ »).
7. **2023 N 2.3** : « relation de Henderson » nommée (hors programme).
8. **2017 R** : figure coupée vers 0,5 mol (n₀ = 0,6 mol invisible) ; équation 7 avec un aldéhyde (déjà relevé au ch. 11).
9. **2021 N 2.3** : 1,77·10⁻⁵ obtenu avec τ arrondi à 0,0132 (1,76·10⁻⁵ sinon) — pas une erreur, à accepter.

---

## 5. Figures pour figures.html

| Clé | Diapositive | Session | Contenu |
|---|---|---|---|
| fig_2017R | n5 | 2017 R | n(acide) en fonction de t : palier 0,2 mol → x_éq = 0,4 mol → K = 4 |

Les nationaux repris sans figure (2017 N, 2018 R, 2019 N, 2020 R, 2021 N, 2022 R) sont dessinés par leurs pages :
equilibre?vue=national_2017, equilibre?vue=base, equilibre?vue=national_2021, quotient?vue=national, quotient?vue=pile,
conductimetrie?vue=national.

### fig_2017R (n5) — 2017 R, estérification acide éthanoïque + éthanol (tubes scellés)
- Ordonnée : n (mol) de l'acide restant, 0 → 0,6, graduations 0,2 · 0,4 · 0,6 (on dessine jusqu'à 0,6 pour que le départ se voie).
  Abscisse : t (h), 0 → 200, graduations 40 · 80 · 120 · 160.
- Points (t ; n) relevés sur la figure du dépôt (lissés ; départ 0,6 mol prolongé) : (0 ; 0,60) (10 ; 0,46) (20 ; 0,37) (40 ; 0,27) (60 ; 0,23)
  (80 ; 0,21) (100 ; 0,205) (120 ; 0,202) (160 ; 0,200) (200 ; 0,200).
- À lire : palier n_éq(acide) = 0,2 mol.
- Questions posées (8 : 0,75 ; 9 : 0,75) : composition à l'équilibre ; montrer que K = 4.
- Réponse au barème : x_éq = 0,6 − 0,2 = 0,4 mol ; acide 0,2, alcool 0,2, ester 0,4, eau 0,4 mol ;
  K = [ester]·[eau]/([acide]·[alcool]) = (0,4 × 0,4)/(0,2 × 0,2) = 4 (V se simplifie). Ici l'eau est un produit (pas le solvant) : elle figure.
