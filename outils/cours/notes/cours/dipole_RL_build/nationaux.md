# Nationaux PC BIOF 2016-2025 — dipôle RL (lus le 12 nov. 2026)

Sources : `backend/data/exams/physique/<session>/exam.json` (questions, points, corrigé du dépôt) + `extraction.json`
(`sujet_text`, `correction_text` = corrigé de prof ou grille officielle) + figures `assets/` regardées quand un nombre était douteux.
On garde seulement le dipôle RL (échelon montant, rupture, régime permanent, τ, L, r, ½·L·i²). RC, RLC, LC, modulation : exclus.

## 1. Où tombe le RL

**Le RL tombe dans 10 sessions sur 20, et chaque année dans une seule des deux sessions** (N = normale, R = rattrapage) :
2016 R, 2017 N, 2018 R, 2019 R, 2020 N, 2021 R, 2022 R, 2023 N, 2024 N, 2025 R (4 normales, 6 rattrapages).
Les 10 autres sessions ont une bobine seulement dans un RLC / LC / circuit d'accord (2016 N, 2017 R, 2018 N, 2019 N, 2020 R,
2021 N, 2022 N, 2023 R, 2024 R, 2025 N) → pas comptées. Cas limite : 2024 R q 2.1.1 (0,25 pt), « u_b(0⁺) = −5 V » au début
d'une décharge RLC (i continu dans la bobine ⇒ u_R(0⁺) = 0 ⇒ u_b = −u_C) : même idée que la rupture RL, mais pas comptée.
Total RL : **25,25 pts sur 10 sessions, soit 2,5 pts en moyenne (de 1,5 à 4 pts)**. Le RL est toujours la 1re partie d'un exercice
d'électricité, suivi d'un RLC/LC et souvent d'une modulation AM.

| Session | Questions RL (points) | Ce qui est demandé |
|---|---|---|
| 2016 R (Ex III, partie I) | 1 (0,5) · 2 (0,5) · 3 (0,5) · 4 (0,5) · 5 (0,5) · 6 (0,5) · 7 (0,5) · 8 (0,5) = **4** | E = 12 V, bobine idéale, R = 40 Ω + un conducteur r. 1 : u_R ou u_PN ? (valeurs à t = 0) ; 2 : I_P = u_R∞/R ; 3 : vérifier r = 8 Ω (Pouillet) ; 4 : équation différentielle en i ; 5 : A et τ de i = A(1 − e^(−t/τ)) ; 6 : τ par la tangente ; 7 : L = τ(r + R) ; 8 : énergie à t = τ/2 (u_R(τ/2) lu sur la courbe) |
| 2017 N (Ex III, partie I) | 1.1 (0,5) · 1.2 (0,5) · 2.1 (0,5) · 2.2 (0,5) · 2.3a (0,5) · 2.3b (0,5) · 2.4 (0,5) = **3,5** | E = 6,5 V, R = 60 Ω, bobine (L, r), K à 2 positions. 1.1 : flèche u_R en convention récepteur ; 1.2 : expression de I_p ; **rupture** : 2.1 équation différentielle en u_R ; 2.2 τ à partir de u_R = R·I_p·e^(−t/τ) ; 2.3a r = 5 Ω à partir de u_R(0) = 6 V ; 2.3b L = 182 mH ; 2.4 énergie à t = τ |
| 2018 R (Ex III, partie I) | 1 (0,25) · 2 (0,5) · 3 (0,5) · 4 (0,5) · 5 (0,75) · 6 (0,75) = **3,25** | Bobine de mixeur, idéale, R = 10 Ω, on enregistre **u_L(t)**. 1 : brancher l'acquisition sur la bobine ; 2 : équation différentielle en i ; 3 : u_L(t) = E·e^(−Rt/L) en dérivant i ; 4 : u_L(τ) = E·e⁻¹ = 3,3 V ; 5 : τ = 1 ms lu à 3,3 V, L = 10 mH ; 6 : énergie à t = τ |
| 2019 R (Ex III, partie 1-I) | 1.1 (0,5) · 1.2 (0,5) · 1.3 (0,25) · 1.4 (0,5) · 1.5 (0,25) · 1.6 (0,25) = **2,25** | E = 10 V, R = 40 Ω, bobine (L, r), courbes u_R et u_B. 1.1 : quelle courbe est u_R ; 1.2 : montrer l'équation différentielle en u_R ; 1.3 : en déduire U_R = R·E/(R + r) ; 1.4 : r = 10 Ω ; 1.5 : τ par la tangente ; 1.6 : vérifier L = 0,5 H |
| 2020 N (Ex IV, partie I) | I.1 (0,5) · I.2 (0,5) · I.3 (0,5) = **1,5** | R = 90 Ω, bobine (L, r), courbes i(t) et u_L(t). I.1 : montrer l'équation différentielle en i ; I.2 : r = u_L(∞)/I₀ = 10 Ω ; I.3 : vérifier L = 1 H |
| 2021 R (Ex 4, partie II) | II.1 (0,25) · II.2 (0,5) · II.3 (0,5) · II.4 (0,5) · II.5 (0,25) = **2** | E = 6 V, R₂ = 95 Ω, courbe i(t). II.1 : faire le schéma ; II.2 : équation di/dt + i/τ = E/L, avec l'expression de τ ; II.3 : I_p = E/(R₂ + r) ; II.4 : r = 5 Ω ; II.5 : L = 0,51 H |
| 2022 R (Ex 3, partie 1) | 1.1 (0,25) · 1.2 (0,5) · 1.3 (0,25) · 1.4 (0,5) · 1.5 (0,25) · 1.6 (0,5) = **2,25** | E = 10 V, R = 490 Ω, L réglable. 1.1 : brancher l'acquisition pour u_R ; 1.2 : équation différentielle en u_R ; 1.3 : U₀ = 9,8 V lu ; 1.4 : r = 10 Ω ; 1.5 : L₀ = 0,5 H ; 1.6 : **quelle courbe pour L₁ = 2L₀** |
| 2023 N (Ex 3, partie 1) | 1.1 (0,25) · 1.2.1 (0,5) · 1.2.2 (0,5) · 1.3 (0,5) = **1,75** | E = 24 V, bobine idéale, courbe i(t). 1.1 : équation différentielle en i ; 1.2.1 : A et B de i = A + B·e^(−t/τ) ; 1.2.2 : L = 1 H (I₀ = 48 mA, τ = 2 ms) ; 1.3 : expression numérique u_L(t) = 24·e^(−500t) |
| 2024 N (Ex 4, partie 2) | 2.1 (0,5) · 2.2.1 (0,5) · 2.2.2 (0,5) = **1,5** | E = 6 V, R₁, bobine (L, r). 2.1 : montrer di/dt = −((R₁ + r)/L)·i + E/L ; **graphe di/dt = f(i)** : 2.2.1 vérifier L = 2 mH (ordonnée à l'origine) ; 2.2.2 τ (pente) |
| 2025 R (Ex 3, partie I) | 1.1 (0,5) · 1.2 (0,75) · 1.3 (0,5) · 1.4 (0,75) · 2.1 (0,25) · 2.2 (0,25) · 2.3 (0,25) = **3,25** | E = 10 V, R = 100 Ω, bobine idéale, **diode + R₁ = 1 kΩ** en parallèle sur la bobine. 1.1 : équation différentielle en u_R ; 1.2 : τ et I₀ ; 1.3 : L = 0,10 H ; 1.4 : u_b et E_m en régime permanent ; **rupture** : 2.1 i(0⁺) = I₀ ; 2.2 u_R1 = 100 V ; 2.3 u_b0 = −100 V |

Ce qui revient tout le temps : **une équation différentielle (10 sessions sur 10)** et **la valeur de L (10 sur 10)**, presque toujours
avec L = τ·(R + r) et τ lu sur la courbe (9 sur 10 ; 2024 N fait autrement).

## 2. cas_types

Notations : i, u_R, u_b (ou u_L, u_B, u_M selon le sujet), E, R, r, L, τ, I₀ / I_p / I_P. « R + r » = résistance totale.

### T1 — Équation différentielle en i (établissement) — 6 sessions, 0,25 à 0,5 pt
- Sessions : 2016 R q4 (0,5), 2018 R q2 (0,5), 2020 N I.1 (0,5, forme donnée), 2021 R II.2 (0,5, forme di/dt + i/τ = E/L avec τ à préciser),
  2023 N 1.1 (0,25), 2024 N 2.1 (0,5, forme di/dt = −((R₁ + r)/L)·i + E/L).
- Mots-indices : « établir / montrer que l'équation différentielle vérifiée par i(t) », « en appliquant la loi d'additivité des tensions ».
- Méthode des corrigés (3 lignes) :
  1. Loi d'additivité des tensions : u_b + u_R = E (2016 R l'écrit u_L + u_r + u_R = E).
  2. Loi d'Ohm en convention récepteur : u_R = R·i et u_b = L·di/dt + r·i (bobine idéale : u_L = L·di/dt).
  3. L·di/dt + (R + r)·i = E ⇒ **di/dt + ((R + r)/L)·i = E/L**. En 2021 R on pose 1/τ = (R₂ + r)/L ⇒ τ = L/(R₂ + r).
     En 2024 N on isole : di/dt = −((R₁ + r)/L)·i + E/L.

### T2 — Équation différentielle en u_R — 4 sessions, 0,5 pt
- Sessions : 2019 R 1.2, 2022 R 1.2, 2025 R 1.1 (établissement) ; 2017 N 2.1 (rupture).
- Mots-indices : « l'équation différentielle vérifiée par la tension u_R(t) aux bornes du conducteur ohmique ».
- Méthode des corrigés, établissement : on écrit l'équation en i, puis i = u_R/R, donc di/dt = (1/R)·du_R/dt ;
  on multiplie par R : **du_R/dt + ((R + r)/L)·u_R = R·E/L** (bobine idéale : du_R/dt + (R/L)·u_R = R·E/L).
  2025 R passe par (L/R)·du_R/dt + u_R = E puis multiplie par R/L.
- Rupture (2017 N) : u_b + u_R = 0 ; i = u_R/R ; u_b = L·di/dt + r·i ⇒ (L/R)·du_R/dt + (r/R + 1)·u_R = 0
  ⇒ **(L/(r + R))·du_R/dt + u_R = 0**. Le second membre est **0** : il n'y a plus de générateur dans la maille.

### T3 — Vérifier la solution / trouver A, B, τ — 4 sessions, 0,5 pt
- 2016 R q5 : i = A(1 − e^(−t/τ)). On remplace dans l'équation et on regroupe :
  A·(1/τ − (r + R)/L)·e^(−t/τ) + (A(r + R) − E)/L = 0 pour tout t ⇒ **τ = L/(r + R) et A = E/(r + R)**.
- 2023 N 1.2.1 : i = A + B·e^(−t/τ). Corrigé officiel : di/dt = −(B/τ)·e^(−t/τ), on remplace, B·e^(−t/τ)·(R/L − 1/τ) + (R/L)·A − E/L = 0
  ⇒ τ = L/R et A = E/R ; puis la condition initiale i(0) = 0 ⇒ A + B = 0 ⇒ **B = −E/R**.
- 2017 N 2.2 (rupture) : u_R = R·I_p·e^(−t/τ) dans (L/(r + R))·du_R/dt + u_R = 0 ⇒ (−L/((r + R)τ) + 1)·e^(−t/τ) = 0 ⇒ τ = L/(r + R).
- 2021 R II.2 : τ s'obtient en identifiant, sans solution à vérifier.
- Mots-indices : « trouver les expressions de A et τ pour que … soit solution », « déterminer A et B en fonction de E et R ».
- Barème : on attend les 2 conditions écrites (coefficient de e^(−t/τ) nul, terme constant nul), pas seulement le résultat.

### T4 — Régime permanent : I₀ (I_p) ou U_R — 6 sessions
- Expression : 2017 N 1.2 (0,5) avec la loi de Pouillet : « en régime permanent la bobine se comporte comme une résistance r »
  ⇒ **I_p = E/(r + R)** ; 2019 R 1.3 (0,25) et 2021 R II.3 (0,5) à partir de l'équation : i = cte ⇒ di/dt = 0 (ou du_R/dt = 0)
  ⇒ ((R + r)/L)·U_R = R·E/L ⇒ **U_R = R·E/(R + r)** ; (1/τ)·I_p = E/L ⇒ **I_p = E/(R₂ + r)**.
- Valeur lue : 2016 R q2 (0,5) I_P = u_R∞/R = 10/40 = 0,25 A ; 2025 R 1.2 I₀ = u_R(∞)/R = 10/100 = 0,1 A (0,5 pt sur 0,75) ;
  2023 N I₀ = 48 mA lu sur i(t).
- Mots-indices : « en régime permanent », « en déduire l'expression de I_p », « quand le régime permanent est atteint ».

### T5 — Trouver r de la bobine — 5 sessions (+ 2016 R où r est un conducteur ohmique), 0,5 pt
Quatre méthodes, toutes en régime permanent sauf la 2e :
- a) Avec I_p et Pouillet : **r = E/I_p − R** — 2021 R II.4 : r = 6/(60·10⁻³) − 95 = 5 Ω ; 2016 R q3 : r = 12/0,25 − 40 = 8 Ω ;
  2022 R 1.4 : i₀ = U₀/R = 9,8/490 = 0,02 A puis r = (E − U₀)/i₀ = (10 − 9,8)/0,02 = 10 Ω.
- b) Avec U_R : **r = R·(E/U_R − 1)** — 2019 R 1.4 : r = 40 × (10/8 − 1) = 10 Ω.
- c) Avec u_b en régime permanent : u_L(∞) = r·I₀ ⇒ **r = u_L(∞)/I₀** — 2020 N I.2 : r = 1/0,1 = 10 Ω.
- d) En rupture, à partir de u_R(0) = R·I_p = R·E/(R + r) — 2017 N 2.3a : r = R·(E − u_R(0))/u_R(0) = 60 × 0,5/6 = 5 Ω.
- Mots-indices : « déterminer / calculer la valeur de r », « montrer que r = … », « lorsque le régime permanent est atteint ».

### T6 — τ sur la courbe — lu dans 9 sessions (souvent dans la question « L »)
- Tangente à l'origine : « τ est l'abscisse du point d'intersection de la tangente à l'origine avec l'asymptote horizontale »
  (2016 R 3 ms, 2019 R 0,01 s, 2020 N 0,01 s, 2021 R 5,1 ms, 2022 R 1 ms, 2023 N 2 ms, 2025 R 1 ms).
  En rupture (2017 N) : la tangente coupe l'**axe des temps** à τ = 2,8 ms.
- 63 % : cité en plus dans 2022 R et 2025 R (« u_R atteint 63 % de sa valeur finale »).
- 37 % : 2018 R, courbe u_L décroissante : u_L(τ) = E·e⁻¹ = 9 × 0,37 = 3,3 V, puis on lit l'abscisse : τ = 1 ms.
- Points : 0,25 seul (2019 R 1.5, 2025 R dans 1.2), sinon compris dans les 0,5 à 0,75 pt de « trouver L ».

### T7 — Trouver L à partir de τ — 9 sessions, 0,25 à 0,75 pt
- Méthode des corrigés : « τ = L/(R + r) ⇒ L = τ·(R + r) », puis A.N. avec τ en s.
  2016 R : 3·10⁻³ × (8 + 40) = 0,144 H ; 2017 N : 2,8·10⁻³ × 65 = 0,182 H ; 2019 R : 0,01 × 50 = 0,5 H ; 2020 N : 0,01 × 100 = 1 H ;
  2021 R : 5,1·10⁻³ × 100 = 0,51 H ; 2022 R : 10⁻³ × 500 = 0,5 H.
- Bobine idéale (r = 0) : τ = L/R ⇒ L = τ·R — 2018 R : 10⁻³ × 10 = 0,01 H ; 2025 R : 10⁻³ × 100 = 0,1 H ;
  2023 N : R d'abord : R = E/I₀ = 24/48·10⁻³ = 500 Ω, puis L = 2·10⁻³ × 500 = 1 H.
- Mots-indices : « en déduire la valeur de L », « vérifier que L = … », « montrer que L = … ».

### T8 — Graphe di/dt = f(i) — 1 session (2024 N), 2 × 0,5 pt
- L'équation di/dt = −((R₁ + r)/L)·i + E/L est une droite di/dt = a·i + b.
- Ordonnée à l'origine b = E/L ⇒ L = E/b = 6/(3·10³) = 2·10⁻³ H.
- Pente a = −(R₁ + r)/L = −1/τ ⇒ τ = −1/a. La droite coupe l'axe des i en I_p = 6 mA (axe en **mA**) :
  a = −3·10³/6·10⁻³ = −5·10⁵ s⁻¹ ⇒ **τ = 2 µs** (grille officielle : « τ = 2 µs », 0,25 méthode + 0,25 valeur).
- Jamais demandé : u_b = f(di/dt) ou u_R = f(i).

### T9 — u_b(t) par dérivation / valeur à un instant — 2 sessions
- 2018 R q3 (0,5) : u_L = L·di/dt avec i = (E/R)(1 − e^(−Rt/L)) ⇒ di/dt = (E/R)·(R/L)·e^(−Rt/L) ⇒ **u_L = E·e^(−Rt/L)** ;
  q4 (0,5) : u_L(τ) = E·e⁻¹ ≈ 3,3 V (E = 9 V lu à t = 0).
- 2023 N 1.3 (0,5) : u_L = E·e^(−t/τ), « en unité SI » ⇒ **u_L(t) = 24·e^(−500t)** (1/τ = 500 s⁻¹).

### T10 — u_b en régime permanent — 2 sessions
- 2025 R 1.4 (0,5 pt sur 0,75), bobine idéale : u_b = L·di/dt = 0 car i = I₀ = cte (méthode 2), ou u_b = E − u_R = 10 − 10 = 0 V (méthode 1).
- 2020 N I.2 : bobine (L, r) : u_L(∞) = r·I₀ (non nul, ici 1 V) ⇒ sert à trouver r.

### T11 — Énergie magnétique ½·L·i² — 4 sessions, 0,25 à 0,75 pt
- Formule : **E_m = ½·L·i²**, et i vient de u_R lue : i = u_R/R.
- 2016 R q8 (0,5) : à t = τ/2, u_R = 4 V lu ⇒ E = ½ × 0,144 × (4/40)² = 7,2·10⁻⁴ J.
- 2017 N 2.4 (0,5) : rupture, à t = τ, u_R(τ) = 2,2 V lu ⇒ E_m = ½ × 0,182 × (2,2/60)² ≈ 1,22·10⁻⁴ J.
- 2018 R q6 (0,75) : à t = τ, i(τ) = (E/R)(1 − e⁻¹) = 0,9 × 0,632 = 0,569 A ⇒ E_m ≈ 1,62·10⁻³ J.
- 2025 R 1.4 (0,25 pt sur 0,75) : régime permanent, E_m = ½ × 0,1 × 0,1² = 5·10⁻⁴ J.
- Mots-indices : « énergie emmagasinée par / dans la bobine à l'instant … ».

### T12 — Rupture du courant — 2 sessions
- 2017 N (montage à 2 positions, « en prenant les précautions nécessaires ») : on étudie u_R(t) décroissant, voir T2, T3, T5 d), T11.
- 2025 R (diode + R₁ en parallèle sur la bobine), juste après l'ouverture :
  2.1 (0,25) « le courant dans une bobine est continu » : **i(0⁺) = i(0⁻) = I₀ = 0,1 A** ;
  2.2 (0,25) u_R1 = R₁·i(0) = 1000 × 0,1 = 100 V ;
  2.3 (0,25) maille bobine–diode–R₁ : u_b + u_R1 = 0 ⇒ **u_b0 = −100 V** (10 fois E : surtension).
- La forme i(t) = I₀·e^(−t/τ) en rupture n'est jamais demandée en i (seulement en u_R).

### T13 — Identifier une courbe — 3 sessions
- u_R ou autre tension à t = 0 : 2016 R q1 (0,5) i(0) = 0 ⇒ u_R(0) = 0, et u_PN(0) = E − r·i(0) = 12 V ⇒ C₁ = u_PN, C₂ = u_R ;
  2019 R 1.1 (0,5) : « u_R(0) = R·i(0) = 0 ⇒ la courbe passe par l'origine » ⇒ courbe (2).
- Courbe pour une autre valeur de L : 2022 R 1.6 (0,5). Corrigé officiel : on élimine C₄ (valeur finale différente de 9,8 V,
  or U₀ = R·E/(R + r) ne dépend pas de L), puis τ₁ = L₁/(R + r) = 2τ ⇒ la courbe à la montée la plus lente : **C₂**.

### T14 — Schéma / branchement — 4 sessions, 0,25 à 0,5 pt
- 2017 N 1.1 (0,5) flèche u_R en convention récepteur (sens opposé à i) ; 2018 R q1 (0,25) acquisition aux bornes de la bobine ;
  2021 R II.1 (0,25) schéma du RL ; 2022 R 1.1 (0,25) acquisition aux bornes de R (« comme un oscilloscope »).

### Jamais demandé dans le RL
Analyse dimensionnelle de L/R (seulement R₂C₂ en AM, 2016 R) ; i(t) en rupture écrit en i ; influence de R sur τ ;
u_b = f(di/dt) ; définition du henry ; méthode ln ; « régime permanent atteint vers 5τ ».

## 3. Formules telles qu'écrites dans les corrigés

- Tension de la bobine : **u_b = L·di/dt + r·i** (2017 N, 2025 R : u_b ; 2019 R : u_B ; 2020 N, 2021 R, 2022 R : u_L = L·di/dt + r·i ;
  2018 R, 2023 N, bobine idéale : u_L = L·di/dt). La grille officielle dit : « u = r.i + L.di/dt aux bornes d'une bobine en convention récepteur ».
  2016 R sépare u_L + u_r + u_R (r = conducteur). 2024 N (corrigé du dépôt) écrit u_R = (R₁ + r)·i et u_L = L·di/dt (r mis avec R, notation à éviter).
- Courant permanent : I_P (2016 R, 2021 R), I_p (2017 N), **I₀** (2020 N, 2022 R officiel, 2023 N, 2025 R), I (2019 R), i₀ (2022 R dépôt).
  Les deux noms existent : le cours peut dire « I₀ (ou I_p) ».
- Résistance totale : toujours **R + r** (ou r + R, R₂ + r, R₁ + r). **R_t n'apparaît jamais.**
- Équation différentielle : on écrit d'abord **L·di/dt + (R + r)·i = E**, puis **di/dt + ((R + r)/L)·i = E/L** (forme finale encadrée).
  Variantes : di/dt + (1/τ)·i = E/L (2021 R) ; di/dt = −((R₁ + r)/L)·i + E/L (2024 N) ;
  du_R/dt + ((R + r)/L)·u_R = R·E/L (2019 R, 2022 R) ; du_R/dt + (R/L)·u_R = R·E/L (2025 R) ;
  rupture : (L/(r + R))·du_R/dt + u_R = 0 (2017 N).
- Solutions : i(t) = A(1 − e^(−t/τ)) (2016 R) ; i(t) = (E/R)(1 − e^(−R·t/L)) (2018 R) ; i(t) = A + B·e^(−t/τ) (2023 N) ;
  u_R(t) = R·I_p·e^(−t/τ) (rupture, 2017 N) ; u_L(t) = E·e^(−t/τ).
- **τ = L/(R + r)** ; bobine idéale τ = L/R ; **I_p = E/(R + r)** (loi de Pouillet) ; **U_R = R·E/(R + r)** ; **E_m = ½·L·i²** (noté 𝓔, E_m, 𝓔ₘᵉ, E_mf).
- Unités dans les A.N. : τ en s (3·10⁻³), L en H, i en A (48·10⁻³) ; 2017 N officiel fait 2,8 ms × 65 Ω = 182 mH.

## 4. valeurs_reperes

| Session | E | R | r bobine | L | τ | I₀ / I_p | Autre |
|---|---|---|---|---|---|---|---|
| 2016 R | 12 V | 40 Ω (+ conducteur r = 8 Ω) | 0 | 0,144 H | 3 ms | 0,25 A | u_R(τ/2) ≈ 4 V ; E_m = 7,2·10⁻⁴ J |
| 2017 N | 6,5 V | 60 Ω | 5 Ω | 182 mH | 2,8 ms | 0,1 A | u_R(0) = 6 V ; u_R(τ) = 2,2 V ; E_m = 1,22·10⁻⁴ J |
| 2018 R | 9 V (lu) | 10 Ω | 0 | 10 mH | 1 ms | 0,9 A | u_L(τ) = 3,3 V ; E_m(τ) = 1,62·10⁻³ J |
| 2019 R | 10 V | 40 Ω | 10 Ω | 0,5 H | 10 ms | 0,2 A | U_R = 8 V ; u_B(∞) = 2 V |
| 2020 N | 10 V (u_L(0), pas donné) | 90 Ω | 10 Ω | 1 H | 10 ms | 100 mA | u_L(∞) = 1 V |
| 2021 R | 6 V | R₂ = 95 Ω | 5 Ω | 0,51 H | 5,1 ms | 60 mA | — |
| 2022 R | 10 V | 490 Ω | 10 Ω | L₀ = 0,5 H ; L₁ = 1 H | 1 ms ; 2 ms | 0,02 A | U₀ = 9,8 V |
| 2023 N | 24 V | 500 Ω (calculé) | 0 | 1 H | 2 ms | 48 mA | u_L = 24·e^(−500t) |
| 2024 N | 6 V | R₁ + r = 1 kΩ | — | 2 mH | 2 µs | 6 mA | E/L = 3·10³ A/s |
| 2025 R | 10 V | 100 Ω (R₁ = 1 kΩ) | 0 | 0,1 H | 1 ms | 0,1 A | E_m = 5·10⁻⁴ J ; u_b0 = −100 V |

Ordres de grandeur : E de 6 à 24 V ; R de 10 Ω à 1 kΩ ; r = 5 ou 10 Ω (jamais autre chose) ; L de 2 mH à 1 H
(le plus souvent 0,1 à 1 H) ; τ de 2 µs à 10 ms (le plus souvent 1 à 10 ms) ; I₀ de 6 mA à 0,9 A.
Bobine idéale (r = 0) : 2016 R, 2018 R, 2023 N, 2025 R.

## 5. erreurs_examen (où l'on perd des points, et le geste qui corrige)

1. **Oublier r** dans τ, I_p ou dans l'équation. Geste : écrire u_b = L·di/dt + r·i dès la loi d'Ohm, puis regrouper (R + r)·i.
   Ne mettre r = 0 que si l'énoncé dit « résistance négligeable ».
2. **Second membre faux en rupture** : il vaut 0, pas E (2017 N : u_b + u_R = 0). Geste : refaire la maille après le basculement.
3. **Confondre u_R et u_b** sur les courbes. Geste : à t = 0, i = 0 ⇒ u_R(0) = 0 (courbe qui part de 0) et u_b(0) = E (courbe qui part de E).
4. **Croire que u_b = 0 en régime permanent** pour une bobine réelle : u_b(∞) = r·I₀ (2019 R : 2 V ; 2020 N : 1 V). Geste : u_b(∞) = 0 seulement si r = 0 (2025 R).
5. **Équation en u_R** : oublier de multiplier E par R (second membre R·E/L). Geste : remplacer i par u_R/R partout, puis multiplier toute l'équation par R.
6. **Vérifier la solution sans les deux conditions** (coefficient de e^(−t/τ) nul ET terme constant nul), ou oublier la condition initiale
   i(0) = 0 pour B (2023 N). Geste : écrire « pour tout t » puis le système de deux égalités.
7. **Lire τ de travers** : la tangente doit couper l'asymptote (établissement) ou l'axe des temps (rupture) ; la méthode 63 % ou 37 %
   se fait sur la valeur finale lue, pas sur E (2022 R : 63 % de 9,8 V, pas de 10 V). Geste : écrire la méthode utilisée en une phrase (c'est noté).
8. **Unités** : ms → s, mA → A, mH → H avant le calcul (τ = 5,1 ms = 5,1·10⁻³ s ; I_p = 60 mA). Le graphe 2024 N a i en **mA** et di/dt en
   **10³ A·s⁻¹** : lire l'axe en A donne τ ≈ 0,67 ms au lieu de 2 µs (c'est l'erreur du corrigé du dépôt, voir § 6).
9. **I₀ = E/R au lieu de E/(R + r)**, ou R = E/I₀ appliqué à une bobine réelle. Geste : Pouillet avec toutes les résistances de la maille.
10. **Énergie** : prendre E/R (valeur finale) au lieu de i(t) à l'instant demandé, ou oublier le carré / le ½. Geste : i(t) = u_R(t)/R, lu à l'instant demandé.
11. **Courbe pour L différente (2022 R)** : choisir sans éliminer celle dont la valeur finale change. Geste : U₀ = R·E/(R + r) ne dépend
    pas de L ⇒ même palier, τ deux fois plus grand ⇒ montée plus lente.
12. **Rupture avec diode (2025 R)** : écrire u_b = 0 ou i(0⁺) = 0. Geste : i est continu dans une bobine ⇒ i(0⁺) = I₀ ;
    maille bobine–diode–R₁ (diode idéale, u_D = 0) ⇒ u_b = −R₁·I₀.
13. **Signe** : u_b(0⁺) est négatif à la rupture (−100 V en 2025 R ; −5 V en 2024 R). Geste : garder les flèches de tension du schéma.
14. **Schéma / acquisition** (0,25 à 0,5 pt) : flèche de u_R opposée à i (convention récepteur) ; acquisition en dérivation aux bornes du dipôle visé.

## 6. Erreurs et incohérences repérées dans les corrigés du dépôt (calculs vérifiés en Python)

Questions RL :
- **2024 N 2.2.2 — faux.** Le dépôt écrit a = −1,5·10³ s⁻¹ et τ ≈ 6,7·10⁻⁴ s. La figure 4 a i en mA : la droite va de
  di/dt = 3·10³ A/s (i = 0) à di/dt = 0 (i = 6 mA) ⇒ a = −5·10⁵ s⁻¹ ⇒ **τ = 2·10⁻⁶ s**, comme la grille officielle (« τ = 2 µs »).
  Contrôle : I_p = E/(R₁ + r) = 6 mA ⇒ R₁ + r = 1 kΩ et τ = L/(R₁ + r) = 2·10⁻³/10³ = 2 µs. (2.2.1, L = 2 mH : juste.)
- 2024 N 2.1 (dépôt) : écrit « u_R = (R₁ + r)·i et u_L = L·di/dt ». Le résultat est juste, mais r appartient à la bobine :
  écrire u_b = L·di/dt + r·i et u_R1 = R₁·i.
- **Énoncés incomplets dans exam.json** : des données qui ne sont que dans `sujet_text` (extraction.json) manquent dans `context` / questions :
  2016 R (E = 12 V, R = 40 Ω), 2017 N (E = 6,5 V, R = 60 Ω), 2018 R (R = 10 Ω), 2020 N (R = 90 Ω), 2024 N (E = 6 V, C = 0,22 nF).
  Sans elles, l'élève ne peut pas répondre.
- **2022 R : mauvais documents.** Les questions RL 1.1–1.6 pointent vers doc_ex3_1/doc_ex3_2 (= figure 4 RLC et figure 5 q(t)).
  Les figures RL (assets/fig1p5.png, fig2p5.png, fig3p5.png) ne sont pas dans la liste ; les « Figure 1 / Figure 2 » listées sont de la mécanique.
- 2022 R 1.6 (dépôt) : justifie par « C₂ plus lente que C₁ », sans éliminer C₄ (palier ≈ 11 V sur la figure ; le corrigé officiel dit 12 V)
  ni C₃ (τ plus petit). Le corrigé officiel fait ces deux étapes.
- 2022 R 1.4, **corrigé officiel (extraction.json) faux** : I₀ = 9,8/490 = « 0,2 A » (en fait 0,02 A), puis r = 10/0,2 − 490 (donnerait −440 Ω).
  Le dépôt a corrigé : i₀ = 0,02 A, r = 10 Ω. Juste.
- 2016 R : points. exam.json donne 8 × 0,5 = 4 pts à la partie RL et 1 pt à l'AM, mais le sujet annonce « Partie I : 3,5 pts » et « Partie II : 1,5 pt ».
- 2016 R q8 : u_R(τ/2) lu = 4 V ⇒ 7,2·10⁻⁴ J. Juste à la lecture près (valeur exacte 10(1 − e^(−0,5)) = 3,93 V ⇒ 6,97·10⁻⁴ J).
- 2017 N : la description de la figure 1 dit « source de tension alternative » (faux : générateur idéal continu E = 6,5 V).
  Le corrigé officiel a une faute de frappe en 2.1 (« … + u_R = E » puis « = 0 ») ; le dépôt est juste.
- 2021 R II.4, corrigé officiel : « I_P = 60 ms » (faute d'unité, c'est 60 mA) ; en II.3 « di/dt + (1/τ)·I_P » (il fallait 0 + …). Dépôt juste.
- 2023 N 1.2.1 (dépôt) : trouve A par le régime permanent et B par i(0) = 0, sans remplacer dans l'équation ; le corrigé officiel remplace
  et obtient aussi τ = L/R (nécessaire en 1.2.2). Acceptable mais moins complet.
- 2025 R 2.2, corrigé officiel : « R₁·i(0) = R·I₀ = 10³ × 0,1 » (R au lieu de R₁, faute de frappe). Dépôt juste.
- 2018 R q6 (énergie) : pas de corrigé officiel ; calcul du dépôt vérifié (1,62·10⁻³ J). Juste.
- Vérifiés justes : 2016 R (I_P, r, L), 2017 N (r = 5 Ω, L = 0,182 H, u_R(τ) = 6/e = 2,2 V, E_m = 1,22·10⁻⁴ J), 2018 R (3,31 V ; 0,01 H),
  2019 R (r = 10 Ω ; L = 0,5 H), 2020 N (r = 10 Ω ; L = 1 H ; E = (R + r)·I₀ = 10 V), 2021 R (5 Ω ; 0,51 H), 2023 N (R = 500 Ω ; L = 1 H ;
  1/τ = 500 s⁻¹), 2025 R (0,1 A ; 0,1 H ; 5·10⁻⁴ J ; 100 V ; −100 V).

Hors RL (même exercices, signalé en passant) :
- 2021 R III.1 (RLC) : le dépôt inverse les courbes. Figure 5 : (a) peu amortie ⇒ R₃ = 10 Ω ; (b) très amortie ⇒ R₄ = 100 Ω (comme le corrigé officiel).
- 2024 N 1.4 (RLC) : dépôt 2,2·10⁻⁹ J avec u_C(t₂) = 4 V ; grille officielle 1,83·10⁻⁹ J (u_C(t₂) ≈ 4,4 V sur la figure).
- 2024 R 1.2.2 (RC) : C = 5·10⁻³/50 = 10⁻⁴ F (100 µF), pas 0,10 µF : pour C = 0,10 µF il faut τ = 5 µs. 2024 R 2.3 : le calcul donne
  E_t(t₁) = ½(0,9·10⁻⁶ + 32·10⁻⁶) = 16,45 µJ (plus que E_t(0) = 1,25 µJ, impossible) ; le dépôt écrit 0,1645 µJ ⇒ lecture de u_R(t₁) fausse.
- 2023 R 1.3 et 2.3 (RC/RLC) : 7,2·10⁻⁶ J écrit « 0,72 mJ » (c'est 7,2 µJ) ; 4·10⁻⁶ J écrit « 0,64 mJ » (c'est 4 µJ).

## 7. Au programme mais jamais (ou presque) demandé

La grille officielle (cadre de référence cité dans 2024 N / 2024 R) liste : u = r·i + L·di/dt en convention récepteur ;
« une bobine retarde l'établissement et la disparition du courant ; i(t) est continue, la tension à ses bornes est discontinue à t = 0 » ;
établir l'équation différentielle et vérifier sa solution ; constante de temps (expression + lecture) ; déterminer L et r à partir
de résultats expérimentaux ; énergie magnétique ½·L·i².
- **Surtension / étincelle à la rupture** : une seule fois, et sans le mot (2025 R : u_b0 = −100 V, 10 fois E). « Étincelle » : jamais.
- **Diode de protection (roue libre)** : seulement 2025 R (diode + R₁). En 2017 N elle est cachée dans « en prenant les précautions nécessaires ».
- **Rupture écrite en i** (i = I₀·e^(−t/τ)) : jamais ; la rupture n'est faite qu'avec u_R (2017 N) ou à t = 0⁺ (2025 R).
- **Analyse dimensionnelle de τ = L/R** : jamais pour le RL.
- **Influence de R ou de r sur τ** : jamais (seulement L, 2022 R).
- **Énergie libérée à la rupture / effet Joule dans le RL** : jamais.
- **Forme L·di/dt = E à t = 0** (pente de la tangente E/L) : jamais demandée seule ; seulement via le graphe di/dt = f(i) (2024 N).
- **u_b = f(di/dt), ln, ≈ 5τ pour le régime permanent, bobine à noyau de fer, définition du henry** : jamais.
- Toujours présent : équation différentielle + valeur de L. Très fréquent : r par le régime permanent, τ par la tangente.
