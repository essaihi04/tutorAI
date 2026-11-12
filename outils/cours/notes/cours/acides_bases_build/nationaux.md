# Réactions acide-base et dosage (Ke, Ka, pKa, K = Ka₁/Ka₂, prédominance, indicateur, dosage) : ce que demandent les nationaux (2016-2025)

Source : `backend/data/exams/physique/<année>-<session>/` (exam.json = énoncé et corrigé ; extraction.json = texte du sujet officiel et
barème dans la marge ; assets/*.png = figures). 20 sessions relues (normale N et rattrapage R), exercice 1 (chimie, 7 pts).
Barème : points de exam.json, vérifiés sur extraction.json pour 2019 R, 2020 N, 2020 R, 2024 N (écart relevé en 2020 N).
Figures regardées (outil Read) : 2016 N fig1p3, 2022 N fig2p3, 2022 R figcicontrep3, 2024 R fig1p3, 2025 R fig1p2.
Chapitres déjà relevés : `transformations_deux_sens_build/nationaux.md` (τ, pH, Brønsted) et `etat_equilibre_build/nationaux.md` (Qr, K) :
les questions qu'ils renvoyaient ici (Ke, Ka, pKa, τ d'une base, K = Ka₁/Ka₂, prédominance, indicateur, dosage) sont toutes reprises ci-dessous.
**Tous les nombres des corrigés ont été recalculés avec python** (valeurs ci-dessous). **Vidéos non auditées** (YouTube bloqué depuis le cloud).

À savoir avant de lire :
- Le chapitre tombe dans **17 sessions sur 20** (toutes sauf 2016 R, 2017 R, 2018 R), toujours dans l'exercice 1 de chimie, pour
  **0,5 à 4,75 points** (en moyenne ≈ 2,8 pts) : c'est le chapitre de chimie le plus payant du semestre 1.
- Le **DOSAGE** tombe dans **13 sessions** (2016 N, 2018 N, 2019 R, 2020 N, 2021 N, 2021 R, 2022 N, 2022 R, 2023 R, 2024 N, 2024 R, 2025 N,
  2025 R) : équation de dosage (→), V_E sur la courbe (tangentes parallèles ou maximum de dpH/dV), C_A·V_A = C_B·V_BE, choix de l'indicateur
  (6 sessions), parfois concentration massique / dilution (2019 R, 2020 N, 2022 N, 2023 R, 2024 N, 2025 N).
- Familles de questions (ce chapitre) :
  1. **pKa à partir de Qr,éq ou de τ** (Ka = Qr,éq ; pKa = −log Ka) : 2017 N, 2019 N, 2021 N, 2022 N, 2023 N, 2025 R (6) ; pour une base,
     **Ka = Ke/Qr,éq** : 2020 N, 2020 R, 2022 R (3).
  2. **Ke, [HO⁻] = Ke/[H₃O⁺]** (τ d'une base) : 2020 N, 2020 R, 2022 R (3).
  3. **K d'une réaction acide-base avec les Ka** : K = Ka₁/Ka₂ (2020 R, 2023 N) ; K = Ka/Ke pour la réaction de dosage (2016 N, 2024 N, 2025 N),
     « K ≫ 10⁴ : totale » (2016 N) ; « K représente Ka » (2019 N).
  4. **pH = pKa + log([A⁻]/[AH])**, prédominance, diagramme de distribution : 2016 N, 2018 N, 2019 N, 2020 R, 2021 N, 2021 R, 2022 N, 2022 R,
     2023 N, 2024 N, 2024 R, 2025 R (12).
  5. **Dosage** (ci-dessus) ; **demi-équivalence pH = pKa** : 2023 R (2.7-2.8), 2024 N (5-2 : [AH]/[A⁻] = V_BE/V_B − 1) ; **nature du pH_E**
     (> 7 ou < 7) : 2019 R 3, 2023 R 2.5 ; **dosage total (τ = 1)** : 2024 R 2.4.
- Jamais demandés 2016-2025 : dosage conductimétrique (rupture de pente), échelle des pKa dessinée, pH d'un mélange quelconque.
- Les corrigés du dépôt nomment « Henderson-Hasselbalch » (2021 R 8, 2022 N 2.5, 2023 R 2.8) et « Henderson » (2023 N 2.3) : hors programme
  (perimetre.json) — le cours dit seulement « pH = pKa + log([A⁻]/[AH]) ».
- Critère d'évolution spontanée (2020 R 2.4 : Qr,i = 1 < K = 10) : semestre 2 (piles) ⟶ renvoyé.

---

## 1. Par session

Barème = points du sujet. « ⟶ ch. 11 / ch. 12 » = chapitres déjà construits ; « ⟶ S2 » = semestre 2.

### 2016 N — acide propanoïque : dosage (partie 2) ★★ (2,5 pts) — figure fig_2016N
- Données : K_A = 10^(−4,9), Ke = 10⁻¹⁴ ; V_A = 5 mL, C_B = 5·10⁻² mol/L ; zones de virage hélianthine 3-4,4, BBT 6-7,6, bleu de thymol 8-9,6.
- 1.1 (0,5) **V_BE et pH_E par les tangentes** → V_BE = 6 mL, pH_E = 8,7.
- 1.2 (0,5) **K de la réaction de dosage, montrer qu'elle est totale** → C₂H₅COOH + HO⁻ → C₂H₅COO⁻ + H₂O ; K = Ka/Ke = 10^(−4,9)/10^(−14)
  = **1,26·10⁹** (recalculé 1,259·10⁹) « ≫ 10⁴ : totale ».
- 1.3 (0,5) **C_A** = C_B·V_BE/V_A = 5·10⁻² × 6/5 = **6·10⁻² mol/L**.
- 1.4 (0,5) **indicateur** → bleu de thymol (8-9,6 contient 8,7).
- 1.5 (0,5) **espèce prédominante à V_B = 7 mL** → pH = 11,6 (lu) > pKa = 4,9 : C₂H₅COO⁻.
- Dépôt : « C₂H₅COO » sans charge dans les données (OCR) ; corrigé juste.

### 2017 N — acide butanoïque (partie II.1) (0,5 pt)
- 1.3 (0,5) **pKa = −log Qr,éq** = −log(1,57·10⁻⁵) = **4,8** (recalculé 4,80) ; 1.1 τ ⟶ ch. 11 ; 1.2 Qr,éq ⟶ ch. 12.

### 2018 N — acide lactique : dosage (partie 2) ★★ (2,5 pts)
- Données : K_A = 10^(−3,9) ; V_A = 15 mL, C_B = 3·10⁻² mol/L ; hélianthine 3-4,4, BBT 6-7,6, rouge de crésol 7,2-8,8.
- 1.1 (0,5) équation de dosage (→) ; 1.2 (0,5) **V_BE = 10 mL, pH_E ≈ 8** (« méthode des droites parallèles ») ;
  1.3 (0,5) **C_A = 3·10⁻² × 10/15 = 2·10⁻² mol/L** ; 1.4 (0,5) **rouge de crésol** ;
  1.5 (0,5) **[A⁻]/[AH] = 10^(pH − pKa) = 10^(8 − 3,9) = 1,26·10⁴** (recalculé 1,259·10⁴) → A⁻ prédomine.
- Dépôt : équation avec « COOH(l) » (au lieu de (aq)) ; corrigé juste.

### 2019 N — acide benzoïque (partie 2) ★ (1,5 pt)
- 3.4 (0,25) **« K représente Ka »** ; 3.5 (0,75) **pKa = −log(C·τ²/(1 − τ)) = 4,2** (recalculé 4,21 avec K = 6,2·10⁻⁵) ;
  3.6 (0,5) **prédominance** : pH = −log(τ·C) = 3,66 < pKa = 4,2 → C₆H₅COOH (recalculé 3,658).
- Dépôt : numérotation 2.5-2.7 au lieu de 3.4-3.6 (déjà relevé au ch. 12).

### 2019 R — aspirine : dosage (partie 2) ★ (2 pts)
- V_A = 10 mL, C_B = 10⁻² mol/L, V_BE = 10 mL, V = 278 mL ; jaune de méthyle 2,9-4, hélianthine 3,1-4,4, rouge de crésol 7,2-8,8.
- 1 (0,5) équation AH + HO⁻ → A⁻ + H₂O ; 2.1 (0,5) **C_A = 10⁻² mol/L** ; 2.2 (0,5) **m = C_A·M·V = 10⁻² × 180 × 0,278 = 0,5 g** (recalculé 0,5004) ;
  3 (0,5) **indicateur : rouge de crésol**, justifié par « à l'équivalence, A⁻ (base) : pH_E > 7 » (sans courbe).

### 2020 N — ammoniac : dosage + solution (partie 1) ★★ (3 pts)
- Dosage V_b = 15 mL par HCl C_a = 10⁻² mol/L (figure 1) ; rouge de méthyle 4,2-6,2, hélianthine 3,1-4,4, phénolphtaléine 8,2-10.
- 1.1 (0,5) **NH₃ + H₃O⁺ → NH₄⁺ + H₂O** ; 1.2 (0,5) **C_b·V_b = C_a·V_aE** ; 1.3 (0,5) V_aE = 15 mL → **C_b = 10⁻² mol/L, C₀ = 1 mol/L** (dilution 100) ;
  1.4 (0,5) **pH_E ≈ 6 → rouge de méthyle**.
- 2.2 (0,5) **[HO⁻] = Ke/[H₃O⁺] = 10^(−14)/10^(−10,6) = 3,98·10⁻⁴ mol/L** ; 2.3 τ = 0,040 ; 2.4 Qr,éq = 1,65·10⁻⁵ (ch. 12) ;
  2.5 (0,5) **Ka = Ke/Qr,éq = 6,06·10⁻¹⁰ → pKa = 9,2** (recalculé 9,22).
- Dépôt : **exam.json donne 1,0 pt à 1.1 ; le sujet (extraction.json) 0,5** ; corrigé 2.1 faux (H₃O⁺ au lieu de HO⁻, déjà relevé au ch. 11).

### 2020 R — éthanoate de sodium, mélange de deux couples ★★ (2 pts)
- 1.2 (0,5) **[HO⁻] = Ke·10^pH = 10^(−14) × 10^(7,9) = 7,94·10⁻⁷ mol/L** ; 1.5 (0,5) **Ka₁ = Ke/Qr,éq → pKa₁ = −log(10⁻¹⁴/6,31·10⁻¹⁰) = 4,8** (4,800) ;
  2.2 (0,5) **K = Ka₂/Ka₁ = 10^(pKa₁ − pKa₂) = 10^(4,8 − 3,8) = 10** ; 2.5 (0,5) **pH = pKa₂ + log([HCOO⁻]/[HCOOH])** avec x_éq = 5,39·10⁻³ mol.
- ⟶ S2 : 2.4 Qr,i = 1 < K : sens direct.
- Dépôt : **2.5 écrit « 3,8 + log(0,01539/0,00461) = 4,27 » : le calcul donne 4,32** avec ce couple (4,28 avec CH₃COOH/CH₃COO⁻) ;
  le x_éq du sujet ne vérifie pas exactement K = 10 (K = 10 donne x_éq = 5,20·10⁻³ mol).

### 2021 N — acide carboxylique inconnu : dosage, pKa ★★ (2,5 pts) — figure 2 (dosage)
- 1.1-1.3 (0,25 × 3) dosage V_a = 20 mL, C_b = 10⁻¹ mol/L : **pH_E = 8,8, V_bE = 20 mL, C_a = 10⁻¹ mol/L**.
- 2.4 (0,75) **pKa = −log(1,77·10⁻⁵) = 4,75 → acide éthanoïque** (tableau de pKa : 3,75 · 4,2 · 4,75 · 4,9) (recalculé 4,752).
- 3 (1) **V_b1 pour [AH]/[A⁻] = 2,24** : pH = 4,75 + log(1/2,24) = 4,4 → lu V_b1 ≈ 6 mL (recalculé 4,40 ; par le tableau de dosage
  V_b1 = V_bE/(1 + 2,24) = 6,17 mL).

### 2021 R — acide méthanoïque : dosage, prédominance, pKa ★★ (3,5 pts)
- 1 (1) **montage** : pH-mètre, burette, solution titrée, solution titrante ; 2 (0,5) équation ; 3 (0,25) **V_bE = 15 mL au maximum de dpH/dV_b** ;
  4 (0,5) C_a = 0,1 mol/L ; 6 (0,5) **[A⁻]/[AH] = 10^(−pH)/(C_a − 10^(−pH)) = 4,35·10⁻²** (pH = 2,38 ; recalculé 4,350·10⁻²) ;
  7 (0,25) **AH prédomine** ; 8 (0,5) **pKa = pH − log([A⁻]/[AH]) = 3,74** (recalculé 3,742).
- 9-11 τ et dilution (figure τ(pH)) ⟶ ch. 11.
- Dépôt : « relation de Henderson-Hasselbalch » nommée en 8 (hors programme).

### 2022 N — acide propanoïque : pKa, dosage ★★ (2,75 pts) — figure fig_2022N
- 1.4 (0,5) **pKa = −log(1,28·10⁻⁵) = 4,9** (recalculé 4,89).
- 2.1 (0,5) équation de dosage ; 2.2 (0,25) **V_bE = 20 mL au maximum de dpH/dV_b** ; 2.3 (0,5) C_a = 5·10⁻² × 20/20 = 5·10⁻² mol/L ;
  2.4 (0,5) dilution 10 fois : C₀ = 0,5 mol/L, m = 37 g ; 2.5 (0,5) **% de forme acide à V_b = 5 mL** : pH = 4,4 (lu) →
  [A⁻]/[AH] = 10^(4,4 − 4,9) = 0,316 → % AH = 1/(1 + 0,316) = **76 %** (recalculé 75,97 %).
- Dépôt : **équation de dosage écrite avec ⇌** (le dosage est total : →) ; « Henderson-Hasselbalch » nommé (2.5).

### 2022 R — méthylamine : pKa, dosage ★★★ (3,25 pts) — figure fig_2022R
- 1.3 [HO⁻] = Ke/[H₃O⁺] = 2,0·10⁻³ mol/L (τ = 0,20) ; 1.5 (0,5) **Ka = Ke/Qr,éq = 10⁻¹⁴/5,0·10⁻⁴ = 2,0·10⁻¹¹ → pKa = 10,7** (10,70).
- 2.1 (0,5) CH₃NH₂ + H₃O⁺ → CH₃NH₃⁺ + H₂O ; 2.2 (0,5) **V_aE = 15 mL, pH_E = 6,6 (tangentes)** ; 2.3 (0,5) C_b = 10⁻² mol/L ;
  2.4 (0,5) **BBT (6,0-7,6)** ; 2.5 (0,75) **[CH₃NH₂]/[CH₃NH₃⁺] = 10^(pH − pKa) = 10^(2,8 − 10,7) = 1,26·10⁻⁸** à V_a = 20,4 mL → CH₃NH₃⁺ prédomine.

### 2023 N — acide éthanoïque, mélange avec le méthanoate ★★ (2,5 pts)
- C_A = 5·10⁻² mol/L, pH = 3,05. 1.2 (0,75) **α(CH₃COOH) = 1 − τ = 0,982** (proportion de la forme acide ; τ = 1,78·10⁻²) ;
  1.3 (0,5) **Ka₁ = 10^(−2pH)/(C_A − 10^(−pH)) = 1,62·10⁻⁵ → pKa₁ = 4,79** ;
  2.2 (0,75) **CH₃COOH + HCOO⁻ ⇌ CH₃COO⁻ + HCOOH : K = Ka₁/Ka₂ = 10^(3,75 − 4,79) = 9,1·10⁻²** (recalculé 9,12·10⁻²) ;
  2.3 (0,5) mélange équimolaire : **pH = (pKa₁ + pKa₂)/2 = 4,27**.
- Dépôt : « relation de Henderson » nommée (2.3).

### 2023 R — triméthylamine : dosage, demi-équivalence ★★★ (3,75 pts)
- V_B = 20 mL (urine diluée 10 fois), C_A = 4·10⁻² mol/L ; points Q (10 mL ; 9,9) et E (20 mL ; 5,8) donnés.
- 2.2 (0,5) (CH₃)₃N + H₃O⁺ → (CH₃)₃NH⁺ + H₂O ; 2.3 (0,5) **C_B = 4·10⁻² mol/L** ; 2.4 (0,5) C₀ = 10·C_B = 0,4 mol/L ;
  2.5 (0,5) **pH_E < 7 : à l'équivalence, l'acide (CH₃)₃NH⁺ est présent** ; 2.6 (0,5) **rouge de méthyle (4,2-6,2)** ;
  2.7 (0,75) **à V_A = V_AE/2 : [(CH₃)₃NH⁺]/[(CH₃)₃N] = 1** (tableau) ; 2.8 (0,5) **pKa = pH(demi-équivalence) = 9,9**.
- Dépôt : « Henderson-Hasselbalch » nommé (2.8) ; seuil du sujet « 2,2·10⁻¹⁰ mol/L » non vérifié (sans effet sur le calcul).

### 2024 N — vitamine C : dosage, pKa ★★★ (4,75 pts)
- V_A = 15,0 mL de S_A (V_SA = 50,0 mL), C_B = 1,50·10⁻² mol/L ; courbes pH et dpH/dV_B.
- 1 (0,5) équation AH + HO⁻ → A⁻ + H₂O ; 2 (0,5) **V_BE = 25 mL (maximum de la dérivée)** ; 3 (0,5) **C_A = 2,5·10⁻² mol/L** ;
  4 (0,75) **m = C_A·V_SA·M = 2,5·10⁻² × 0,050 × 176 = 0,22 g = 220 mg** ;
  5-1 (0,5) **pKa = pH + log([AH]/[A⁻])** ; 5-2 (0,75) **[AH]/[A⁻] = V_BE/V_B − 1** (tableau de dosage) ;
  5-3 (0,75) V_B = 8,5 mL → [AH]/[A⁻] = 1,94 ; **pKa ≈ 4,09** (avec pH lu ≈ 3,80) ; 5-4 (0,5) **K = Ka/Ke = 10^(14 − 4,09) = 8,13·10⁹**.
- Dépôt : **corrigés réduits à « Démarche … » / « Méthode … »** (1 : « Équation de la réaction de dosage. » sans équation ; 5-2 : « Démonstration. »).

### 2024 R — amine R–NH₂ : distribution, dosage ★★★ (4,75 pts) — figure fig_2024R
- C_B = 9,0·10⁻² mol/L, pH = 11,88. 1.2.1 (0,5) **pKa = 10,8 au croisement des courbes** ; 1.2.2 (0,5) **pH = 11,88 > pKa : R–NH₂ prédomine** ;
  1.2.3 (0,75) **% acide = 4 × % base → [base]/[acide] = 0,25 → pH = 10,8 + log 0,25 = 10,2** (recalculé 10,198).
- 2.1 (0,5) R–NH₂ + H₃O⁺ → R–NH₃⁺ + H₂O ; 2.2 (0,5) **V_AE = C_B·V_B/C_A = 20,0 mL** ; 2.3 (0,75) x_f = C_A·V_A − 10^(−pH)·(V_A + V_B) = 7,2·10⁻⁴ mol ;
  2.4 (0,75) **τ = 1 : réaction de dosage totale**.
- Dépôt : « OH⁻ » au lieu de HO⁻ (notation) ; corrigés justes.

### 2025 N — hydrogénosulfite : dosage ★★★ (3,75 pts)
- Dilution 100 fois, V_A = 20,0 mL, C_B = 0,10 mol/L, V_BE = 9,6 mL ; pKa(HSO₃⁻/SO₃²⁻) = 7,2.
- 1.1 (0,5) HSO₃⁻ + HO⁻ → SO₃²⁻ + H₂O ; 1.2 (0,75) **C_A = 4,8·10⁻² mol/L** ; 1.3 (0,25) C₀ = 4,80 mol/L ; 1.4 (0,75) **C_m = C₀·M = 499 g/L ≈ 500 g/L** ;
  1.5 (0,75) **K = Ka/Ke = 10^(6,8) = 6,31·10⁶** ; 1.6 (0,75) C_éq = C_B·V_BE/(V_A + V_BE) = 3,2·10⁻² mol/L (recalculé 3,24·10⁻²).

### 2025 R — acide éthanoïque : pKa, distribution, dosage d'un reste d'acide ★★ (2,25 pts) — figure fig_2025R
- C_A = 4,2·10⁻³ mol/L, pH = 3,6. 1.3 (0,5) **Ka = (10^(−3,6))²/(C_A − 10^(−3,6)) = 1,60·10⁻⁵ → pKa = 4,8** (4,796) ;
  1.4.1 (0,5) **pKa = 4,8 au croisement** ; 1.4.2 (0,25) **courbe 1 = forme acide** (> 50 % pour pH < pKa) ;
  1.4.3 (0,5) dilution : pH₁ = 4,2 → **% CH₃COO⁻ ≈ 20 % → τ₁ = 0,20** (recalculé 20,1 %) ⟶ dilution (ch. 11) lue sur la distribution.
- 2.2 (0,5) dosage du reste d'acide (estérification) : n = C_B·V_BE = 1,50 × 0,0220 = 0,033 mol.
- Dépôt : « OH⁻ » (3.1) ; corrigés justes.

### 2016 R, 2017 R, 2018 R
- Rien de ce chapitre (électrolyse, hydrolyse, estérification, pile).

---

## 2. Bilan des cas types

| Cas type | Sessions | Points |
|---|---|---|
| Équation de la réaction de dosage (→, rapide, totale) | 2018 N, 2019 R, 2020 N, 2021 N, 2021 R, 2022 N, 2022 R, 2023 R, 2024 N, 2024 R, 2025 N (11) | 0,25-0,5 |
| V_E (et pH_E) sur la courbe : tangentes parallèles ou maximum de dpH/dV | 2016 N, 2018 N, 2020 N, 2021 N, 2021 R, 2022 N, 2022 R, 2024 N (8) | 0,25-0,5 |
| Concentration par C_A·V_A = C_B·V_BE (+ dilution, masse, C_m) | 13 sessions (toutes les sessions avec dosage) | 0,5-1,5 |
| Choix de l'indicateur coloré (zone de virage contient pH_E) | 2016 N, 2018 N, 2019 R, 2020 N, 2022 R, 2023 R (6) | 0,5 |
| pKa = −log Qr,éq (acide) ou Ka = Ke/Qr,éq (base) | 2017 N, 2019 N, 2020 N, 2020 R, 2021 N, 2022 N, 2022 R, 2023 N, 2025 R (9) | 0,5-0,75 |
| [HO⁻] = Ke/[H₃O⁺] (τ d'une base) | 2020 N, 2020 R, 2022 R (3) | 0,5 |
| K d'une réaction acide-base : Ka₁/Ka₂ ou Ka/Ke | 2016 N, 2020 R, 2023 N, 2024 N, 2025 N (5) | 0,5-0,75 |
| pH = pKa + log([A⁻]/[AH]) : rapport, %, prédominance | 2016 N, 2018 N, 2019 N, 2020 R, 2021 N, 2021 R, 2022 N, 2022 R, 2023 N, 2024 N, 2024 R (11) | 0,25-1 |
| Diagramme de distribution : pKa au croisement, courbe acide / basique | 2024 R, 2025 R (2) | 0,25-0,75 |
| Demi-équivalence : pH = pKa | 2023 R, 2024 N (2) | 0,5-1,5 |
| Nature du pH à l'équivalence (> 7 / < 7) | 2019 R, 2023 R (2) | 0,5 |

Valeurs de pKa rencontrées : 3,74 (HCOOH, 2021 R) ; 3,75 et 3,8 (HCOOH) ; 3,9 (lactique) ; 4,09 (ascorbique) ; 4,2 (benzoïque) ;
4,75 · 4,79 · 4,8 (éthanoïque) ; 4,9 (propanoïque) ; 7,2 (HSO₃⁻) ; 9,2 (NH₄⁺) ; 9,9 (triméthylammonium) ; 10,7 (méthylammonium) ; 10,8 (R–NH₃⁺).
pH_E rencontrés : 8,7 ; 8 ; 8,8 (acide faible + soude, > 7) ; 6 ; 6,6 ; 5,8 (base faible + acide chlorhydrique, < 7).

## 3. Pièges où l'élève perd des points
- Équation de dosage écrite avec ⇌ (le dosage est total : →) ; oublier qu'elle doit être rapide, totale, unique.
- C_A·V_A = C_B·V_B avec un volume quelconque au lieu de V_BE ; mL et L mélangés (le rapport V_BE/V_A s'en moque, une masse non).
- Lire V_E au milieu du saut « à l'œil » sans tracer les tangentes (le barème demande la méthode : tangentes parallèles et parallèle médiane,
  ou maximum de dpH/dV).
- Choisir l'indicateur dont la zone contient 7 au lieu de pH_E (acide faible : pH_E > 7 ; base faible : pH_E < 7).
- Confondre pKa et pH ; écrire pKa = log Ka (signe) ; écrire Ka avec une unité.
- Prédominance inversée (pH > pKa : c'est la BASE qui prédomine).
- pH = pKa à l'équivalence (faux : à la DEMI-équivalence).
- [HO⁻] = 10^(−pH) au lieu de Ke/[H₃O⁺] = 10^(pH − 14).
- K = Ka₂/Ka₁ au lieu de Ka₁/Ka₂ : Ka de l'acide qui réagit (réactif) au numérateur.
- Oublier que la dilution avant le dosage multiplie C (2020 N, 2022 N, 2023 R, 2025 N).

## 4. Erreurs du dépôt (exam.json / extraction.json) qui touchent ce chapitre
1. **2020 N 1.1** : exam.json 1,0 pt, sujet 0,5 pt.
2. **2020 R 2.5** : « 3,8 + log(…) = 4,27 » : le calcul donne 4,32 avec HCOOH/HCOO⁻ (4,28 avec CH₃COOH/CH₃COO⁻) ; x_éq du sujet (5,39·10⁻³)
   ≠ x_éq tiré de K = 10 (5,20·10⁻³).
3. **2022 N 2.1** : équation de dosage avec ⇌ (déjà relevé au ch. 11).
4. **2021 R 8, 2022 N 2.5, 2023 R 2.8** : « Henderson-Hasselbalch » ; **2023 N 2.3** : « Henderson » (hors programme, jamais dit au cours).
5. **2024 N** : corrigés sans démarche (« Démarche … », « Méthode … », « Démonstration. »), équation de dosage absente.
6. **2024 R 1.1, 2025 R 3.1** : « OH⁻ » au lieu de HO⁻ ; **2018 N 1.1** : acide noté (l) au lieu de (aq) ; **2016 N** : « C₂H₅COO » sans charge.
7. **2019 N** : numérotation 2.5-2.7 au lieu de 3.4-3.6 (déjà relevé au ch. 12).

---

## 5. Figures pour figures.html

| Clé | Diapositive | Session | Contenu |
|---|---|---|---|
| fig_2025R | p4 | 2025 R | diagramme de distribution CH₃COOH / CH₃COO⁻ : croisement à pH = 4,8 ; courbe 1 = acide |
| fig_2016N | n1 | 2016 N | dosage pH = f(V_B) de l'acide propanoïque : tangentes → V_BE = 6 mL, pH_E = 8,7 ; bleu de thymol |
| fig_2022R | n2 | 2022 R | dosage de la méthylamine par l'acide chlorhydrique : V_aE = 15 mL, pH_E = 6,6 ; BBT |
| fig_2022N | n3 | 2022 N | dosage de l'acide propanoïque + dpH/dV_b : V_bE = 20 mL ; à 5 mL, pH = 4,4 → 76 % de forme acide |
| fig_2024R | n4 | 2024 R | distribution R–NH₃⁺ / R–NH₂ : pKa = 10,8 ; 80 % d'acide à pH = 10,2 |

Les nationaux repris sans figure (2017 N, 2019 N, 2020 N, 2020 R, 2021 R, 2023 N, 2023 R, 2024 N, 2025 N) sont dessinés par leurs pages
(base?vue=national, acidite?vue=mesure, comparer?vue=national, exploiter?vue=national_2023).

### fig_2025R (p4) — 2025 R, diagramme de distribution de l'acide éthanoïque
- Abscisse : pH 0 → 14 (graduations 1, 2 … ; figure du sujet coupée vers 9) ; ordonnée : % 0 → 100 (graduations 20, 40 …).
- Courbe 1 (forme acide, décroissante) et courbe 2 (forme basique, croissante), calculées avec pKa = 4,8 :
  pH 2,8 → 99 % / 1 % ; 3,8 → 90,9 % / 9,1 % ; 4,8 → 50 % / 50 % ; 5,8 → 9,1 % / 90,9 % ; 6,8 → 1 % / 99 %.
- Questions (1.4.1 : 0,5 ; 1.4.2 : 0,25 ; 1.4.3 : 0,5) : pKa au croisement = 4,8 ; courbe 1 = acide (> 50 % pour pH < pKa) ;
  pH₁ = 4,2 → 20 % de CH₃COO⁻ → τ₁ = 0,20.

### fig_2016N (n1) — 2016 N, dosage de l'acide propanoïque par la soude
- Abscisse V_B (mL) 0 → 12 (graduations 1 mL) ; ordonnée pH 3 → 12.
- Points (lus, lissés) : (0 ; 3,0) (0,5 ; 3,8) (1 ; 4,2) (2 ; 4,6) (3 ; 4,9) (4 ; 5,2) (5 ; 5,6) (5,5 ; 6,0) (5,8 ; 6,6) (6 ; 8,7) (6,2 ; 10,6)
  (6,5 ; 11,0) (7 ; 11,6) (9 ; 12,0) (12 ; 12,2).
- Tangentes parallèles (pointillés) et parallèle médiane → **E (6 mL ; 8,7)** ; C_A = 5·10⁻² × 6/5 = 6·10⁻² mol/L ; bleu de thymol (8-9,6) ;
  à V_B = 7 mL, pH = 11,6 > pKa = 4,9 → C₂H₅COO⁻ prédomine.

### fig_2022R (n2) — 2022 R, dosage de la méthylamine par l'acide chlorhydrique
- Abscisse V_a (mL) 0 → 24 (graduations 3 mL) ; ordonnée pH 0 → 14.
- Points (lus) : (0 ; 11,3) (3 ; 11,0) (6 ; 10,7) (9 ; 10,4) (12 ; 10,0) (13,5 ; 9,6) (14,5 ; 8,8) (15 ; 6,6) (15,3 ; 4,3) (16 ; 3,6) (18 ; 3,0)
  (20,4 ; 2,8) (24 ; 2,6).
- Tangentes → **E (15 mL ; 6,6)** ; C_b = 10⁻² × 15/15 = 10⁻² mol/L ; BBT (6,0-7,6) ; à 20,4 mL, pH = 2,8 → [CH₃NH₂]/[CH₃NH₃⁺] = 1,26·10⁻⁸.

### fig_2022N (n3) — 2022 N, dosage de l'acide propanoïque, courbe et dérivée
- Abscisse V_b (mL) 0 → 30 (graduations 5) ; ordonnée pH 0 → 14 ; deuxième courbe dpH/dV_b (sans graduation) en bas.
- Points pH (lus) : (0 ; 3,1) (2 ; 4,0) (5 ; 4,4) (10 ; 4,9) (15 ; 5,4) (18 ; 5,9) (19,5 ; 6,7) (20 ; 8,8) (20,5 ; 10,5) (22 ; 11,2) (25 ; 11,6) (30 ; 11,9).
- Dérivée : pic fin à **V_bE = 20 mL** ; C_a = 5·10⁻² mol/L ; à V_b = 5 mL : pH = 4,4 → [A⁻]/[AH] = 10^(−0,5) = 0,316 → 76 % de forme acide.

### fig_2024R (n4) — 2024 R, diagramme de distribution R–NH₃⁺ / R–NH₂
- Abscisse pH 0 → 14 (graduations 2) ; ordonnée % 0 → 100 (graduations 20).
- Forme acide (trait plein, décroît) et forme basique (pointillés, croît), calculées avec pKa = 10,8 : pH 9,8 → 90,9 % / 9,1 % ; 10,2 → 80 % / 20 % ;
  10,8 → 50 % / 50 % ; 11,8 → 9,1 % / 90,9 %.
- Questions : pKa = 10,8 au croisement ; pH = 11,88 > pKa → R–NH₂ prédomine ; 80 % d'acide → pH = 10,8 + log 0,25 = 10,2.
