# Nationaux PC BIOF 2016-2025 — oscillations libres RLC série (lus le 12 nov. 2026)

Sources : `backend/data/exams/physique/<session>/exam.json` (questions, points, corrigé du dépôt) + `extraction.json`
(`sujet_text`, `correction_text` = corrigé de prof ou grille officielle) + figures `assets/` et pages `pages/sujet_pN.jpg`
regardées quand un nombre était douteux. Calculs refaits en Python.
On garde : décharge d'un condensateur dans une bobine (RLC, LC idéal), équation différentielle, T₀ = 2π√(LC), régimes,
pseudo-période, énergie ½·C·u_C² + ½·L·i², énergie perdue, dE/dt, entretien u_G = k·i, u_b(0⁺).
Exclus : RC et RL seuls (déjà faits), modulation / démodulation AM, mécanique. Le **circuit d'accord** de l'AM
(f₀ = 1/(2π√(LC)) pour capter une station) est noté à part (§ 1, fin) mais pas compté.

## 1. Où tombe le RLC

**Le RLC tombe dans 17 sessions sur 20.** Seules 2016 R, 2017 N et 2018 R n'ont pas de RLC (2016 R et 2018 R ont
seulement un circuit d'accord dans l'AM ; 2017 N n'a rien). Toutes les années ont au moins une session avec RLC,
et 7 années l'ont aux deux sessions.
Total : **35,75 pts sur 17 sessions, soit 2,1 pts en moyenne (de 0,5 à 3,5 pts)** (barème du sujet ; 2019 N compté 2,5).
Le RLC est presque toujours la **2e partie** d'un exercice d'électricité : après une charge de condensateur (10 fois) ou un RL
(6 fois ; 2021 R a RC puis RL), et souvent suivi d'une partie AM. Seul 2024 N commence par le RLC (puis RL). Le condensateur et la bobine sont « les précédents » : C ou L vient de la 1re partie.
**Aucun RLC forcé / résonance** dans les 20 sujets (le mot « résonance » n'est que dans des corrigés du dépôt pour le
circuit d'accord) ; ni facteur de qualité, ni R critique, ni régime critique demandé, ni homogénéité de √(LC).

| Session | Questions RLC (points) | Ce qui est demandé |
|---|---|---|
| 2016 N (Ex III, partie 2) | 2.1 (0,25) · 2.2 (0,5) · 2.3 (0,5) · 2.4.1 (0,5) · 2.4.2 (0,25) = **2** | C = 10 µF chargé (E = 12 V), décharge dans la bobine (L, r_b) seule, courbe q(t). 2.1 régime ; 2.2 L avec T ≈ T₀ = 6 ms ⇒ L ≈ 9,1·10⁻² H ; 2.3 ΔE entre 0 et 18 ms (q = 120 puis 40 µC, deux maxima) ⇒ −6,4·10⁻⁴ J, interpréter ; **entretien** 2.4.1 équation avec u_G = k·i ; 2.4.2 k = 11 ⇒ r_b = 11 Ω |
| 2017 R (Ex III, partie 2) | 2.1 (0,5) · 2.2 (0,5) · 2.3 (0,5) · 2.4 (0,75) = **2,25** | « amortissement négligeable », C = 100 µF, courbe q(t). 2.1 équation en q ; 2.2 T₀ à partir de q = Q_m·cos(2πt/T₀) ; 2.3 vérifier L ≈ 0,91 H (T₀ = 60 ms) ; 2.4 énergie à t = 0 et t = T₀/4 (Q_m = 600 µC) : 1,8·10⁻³ J les deux fois, justifier |
| 2018 N (Ex 3, partie 3) | 3.1 (0,5) · 3.2 (0,5) · 3.3 (0,5) · 3.4 (0,75) = **2,25** | C = 2,5 µF, bobine (L, r), sans R. 3.1 pourquoi pseudo-périodique ; **entretien** 3.2 équation en q avec u_G = k·i ; 3.3 k = 5 ⇒ r = 5 Ω ; 3.4 L avec T₀ = 2,5 ms (courbe sinusoïdale) ⇒ 63 mH |
| 2019 N (Ex III, partie II) | 1 (0,25) · 2.1 (0,5) · 2.2 (0,25) · 3 (0,5) · 4.1 (0,5) · 4.2 (0,5) = **2,5** | LC idéal, E = 10 V, C = 10 µF. 1 montrer d²u_C/dt² + u_C/(LC) = 0 ; 2.1 **choisir la courbe** parmi (a) amortie, (b) cos, (c) −sin ; 2.2 T₀ = 20 ms ; 3 L = 1 H (π² = 10) ; 4.1 E_t = ½·C·E² = 5·10⁻⁴ J ; 4.2 E_m à 12 ms (u_C = −8 V) = 1,8·10⁻⁴ J |
| 2019 R (Ex 3, partie 1-II) | 1 (0,25) · 2 (0,5) · 3 (0,75) = **1,5** | Bobine du RL (L = 0,5 H, r = 10 Ω) + R = 40 Ω, courbes u_C(t) et i(t). 1 régime ; 2 C avec T ≈ T₀ = 10 ms ⇒ 5 µF ; 3 E_t à 9 ms : u_C = 4,8 V, i = 12 mA ⇒ 9,36·10⁻⁵ J |
| 2020 N (Ex IV, parties II-III) | II.1 (0,25) · II.2 (0,5) · II.3 (0,5) · III.1 (0,5) · III.2 (0,75) · III.3 (0,5) · III.4 (0,5) = **3,5** | Bobine du RL (L = 1 H, r = 10 Ω) + R = 90 Ω, courbe u_C. II.1 régime ; II.2 équation en u_C ; II.3 C = 2,5 µF (T = 10 ms) ; **entretien** III.1 k₀ = R + r = 100 Ω ; III.2 **I_m, T₀, φ** de i = I_m·cos(2πt/T₀ + φ) : 8 mA, 10 ms, π/2 ; III.3 E_t = ½·L·I_m² = 3,2·10⁻⁵ J ; III.4 E_e à 16 ms (i = 4,8 mA) = 2,05·10⁻⁵ J |
| 2020 R (Ex 4, parties 2-3) | 2.1 (0,5) · 2.2 (0,5) · 2.3 (0,5) · 3.1 (0,75) · 3.2 (0,5) · 3.3 (0,5) = **3,25** | C = 50 µF, bobine (L, r = 10 Ω), R réglable. 2.1 **tableau** R₁ = 0 → C₁ pseudo-périodique, R₂ = 390 Ω → C₂ apériodique ; 2.2 montrer l'équation en u_C ; 2.3 L = 0,2 H (T = 20 ms) ; 3.1 **courbes E_e(t), E_m(t)** : E_t = 0,64 / 0,36 / 0,24 mJ à 0 / 13 / 20 ms ; 3.2 cause (effet Joule dans r) ; 3.3 i₁ = √(2E_m/L) = 4,5·10⁻² A |
| 2021 N (Ex IV, partie II) | 1 (0,25) · 2 (0,5) · 3 (0,5) · 4 (0,25) · 5 (0,5) = **2** | LC, C = 12 µF, courbe q(t). 1 régime (périodique) ; 2 équation en q ; 3 T₀ à partir de q = Q_m·cos(2πt/T₀) ; 4 T₀ = 21 ms ; 5 L ≈ 0,92 H (π² = 10) |
| 2021 R (Ex 4, partie III) | 1 (0,5) · 2 (0,5) · 3 (0,5) = **1,5** | Bobine du RL (L = 0,51 H, r = 5 Ω), C = 100 µF, R₃ = 10 Ω puis R₄ = 100 Ω. 1 **affecter les courbes** (a) peu amortie → R₃, (b) très amortie → R₄ ; 2 T = 45 ms et T₀ = 2π√(LC) = 44,9 ms ; 3 énergie Joule entre 0 et 11,25 ms (courbes E_e, E_m) : 1,80 − 1,26 = 0,54 mJ |
| 2022 N (Ex 3, partie 2) | 2.1.1 (0,25) · 2.1.2 (0,5) · 2.1.3a (0,5) · 2.1.3b (0,5) · 2.2.1 (0,5) · 2.2.2 (0,75) = **3** | C = 50 µF, E = 12 V. Cas r = 0 : 2.1.1 montrer l'équation en u_C ; 2.1.2 **choisir la courbe** (C₁ cos 12 V / C₂ 10 V / C₃ amortie) ; 2.1.3a T₀ à partir de u_C = U₀·cos(2πt/T₀) ; 2.1.3b L = 0,05 H (T₀ = 10 ms). Cas r ≠ 0 : 2.2.1 expression de E_t ; 2.2.2 ΔE entre 0 et 9 ms (u_C = 6 V, i = 140 mA) = −2,21 mJ |
| 2022 R (Ex 3, partie 2) | 2.1 (0,5) · 2.2 (0,75) = **1,25** | Bobine du RL réglée sur L = 1 H (r = 10 Ω), condensateur seul, courbe q(t) en mC et t en s. 2.1 équation en q ; 2.2 C = 250 µF (T ≈ 0,10 s) |
| 2023 N (Ex 3, partie 2) | 2.1 (0,25) · 2.2.1 (0,5) · 2.2.2 (0,75) = **1,5** | LC, L = 1 H (du RL), courbe u_C(t) avec flèches d'échelle (5 V ; 0,5 ms). 2.1 équation en u_C ; 2.2.1 C = 0,1 µF (T₀ = 2 ms) ; 2.2.2 E_m à 1,8 ms : ½·C·(10² − 8²) = 1,8 µJ |
| 2023 R (Ex 3, partie 2) | 2.1 (0,5) · 2.2 (0,5) · 2.3 (0,75) · 2.4 (0,5) = **2,25** | C₀ = 10 µF chargé (q_max = 120 µC), L = 0,1 H idéale, R = 35 Ω. 2.1 montrer l'équation en q ; 2.2 expliquer la baisse d'amplitude ; 2.3 |ΔE| entre 0 et t₁ (q = 120 puis 40 µC) = 0,64 mJ ; **entretien** 2.4 k = R = 35 Ω |
| 2024 N (Ex 4, partie 1) | 1.1 (0,25) · 1.2 (0,5) · 1.3 (0,5) · 1.4 (0,75) = **2** | C = 0,22 nF chargé sous E (u_C(0) = 6 V), bobine (L, r), R₀. 1.1 amortissement du point de vue énergétique ; 1.2 équation en u_C ; 1.3 où est l'énergie à t₁ (u_C = 0 → bobine) et t₂ (u_C extrême → condensateur) ; 1.4 E_j entre 0 et t₂ (u_C(t₂) ≈ −4,4 V) = 1,83·10⁻⁹ J |
| 2024 R (Ex 4, partie 2) | 2.1.1 (0,25) · 2.1.2 (0,75) · 2.2 (0,5) · 2.3 (0,5) = **2** | E = 5 V, C = 0,10 µF, R = 50 Ω, L = 20 mH, r. 2.1.1 **u_b(0⁺) = −5 V** ; 2.1.2 équation en u_C ; 2.2 E_t en fonction de C, u_C, L, R, u_R ; 2.3 vérifier E_j ≈ 1,1 µJ entre 0 et t₁ (u_C(t₁) ≈ −1,5 V, u_R(t₁) ≈ 5 **mV**) |
| 2025 N (Ex 3, partie 2) | 2.1 (0,5) · 2.2.1 (0,5) · 2.2.2 (0,5) · 2.3 (0,5) · 2.4 (0,5) = **2,5** | C₀ = 1 µF chargé à U₀ = 10 V, bobine (L, r) seule. 2.1 équation en u_C ; 2.2.1 pseudo-période 4 × 7·10⁻⁵ = 2,8·10⁻⁴ s ; 2.2.2 **signe de i** entre t_A et t_B (u_C décroît ⇒ i < 0) ; 2.3 **montrer dE_T/dt = −r·i²** ; 2.4 |E_th| entre 0 et t_A (u_C = 7 V) = 2,55·10⁻⁵ J |
| 2025 R (Ex 3, partie I-3) | 3.1 (0,25) · 3.2 (0,25) = **0,5** | LC idéal, L = 0,1 H (du RL), C = 1 µF chargé sous E = 10 V. 3.1 N₀ = 1/(2π√(LC)) ≈ 503 Hz ; 3.2 I_m = E·√(C/L) ≈ 31,6 mA (conservation de l'énergie) |

Circuit d'accord AM (non compté) : 2016 R 1.2 (0,25 ; C = 49,9 pF), 2018 R 1 (0,5 ; 9 pF), 2020 R 4.2 (0,75 ; 7,7 pF),
2022 R 3.2 (0,5 ; L = 10 mH), 2023 R 3.2 (0,75 ; 11,1 et 3,2 pF), 2025 N 3.2 (0,75 ; 4,76·10⁻¹⁰ F). Même formule T₀ = 2π√(LC) :
le cours RLC peut dire en une ligne qu'elle resservira dans l'AM.

Ce qui revient tout le temps : **lire T (ou T₀) sur une courbe et en tirer L ou C (13 sessions sur 17)**,
**un calcul d'énergie (14 sur 17)**, **une équation différentielle (14 sur 17, dont 2 seulement avec l'entretien : 2016 N, 2018 N)**.

## 2. cas_types

Notations des sujets : q (µC ou mC), u_C, i, L, r (ou r_b), R, C (ou C₀), T₀ (période propre), T (pseudo-période),
Q_m, U₀ (ou U_m), I_m, φ, E_t / E_T, E_e, E_m (attention : E_m = énergie **magnétique**), E_j / E_th / ΔE, k ou k₀.
ω₀ n'apparaît **jamais** : les sujets écrivent toujours 2π/T₀. N₀ = 1/T₀ une fois (2025 R).

### T1 — Équation différentielle (décharge) — 12 sessions (+ 2 avec entretien, voir T7), 0,25 à 0,75 pt
- En q : 2017 R 2.1, 2021 N 2, 2022 R 2.1, 2023 R 2.1 (forme donnée) ; en u_C : 2019 N 1, 2020 N II.2, 2020 R 2.2, 2022 N 2.1.1, 2023 N 2.1,
  2024 N 1.2, 2024 R 2.1.2 (0,75), 2025 N 2.1. Forme donnée (« montrer que ») dans 4 sessions sur 12.
- Mots-indices : « établir / montrer que l'équation différentielle vérifiée par q(t) / u_C(t) », « loi d'additivité des tensions ».
- Rédaction des corrigés (4 lignes) :
  1. Loi d'additivité, **sans générateur** : u_C + u_b (+ u_R) = 0.
  2. u_b = L·di/dt + r·i ; u_R = R·i ; u_C = q/C ; i = dq/dt = C·du_C/dt (convention récepteur, flèches du schéma).
  3. Donc di/dt = d²q/dt² = C·d²u_C/dt².
  4. **L·C·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0** ⇒ d²u_C/dt² + ((R + r)/L)·du_C/dt + u_C/(LC) = 0 ;
     en q : **L·d²q/dt² + (R + r)·dq/dt + q/C = 0**. LC idéal : **d²q/dt² + q/(LC) = 0** (ou en u_C).
- Barème 2024 R : 0,5 méthode + 0,25 équation.

### T2 — Vérifier la solution, trouver T₀ — 3 sessions, 0,5 pt
- 2017 R 2.2 et 2021 N 3 : q = Q_m·cos(2πt/T₀) ; 2022 N 2.1.3a : u_C = U₀·cos(2πt/T₀). Toujours **cos, sans φ, départ au maximum**.
- Méthode : dq/dt = −(2π/T₀)·Q_m·sin(2πt/T₀) ; d²q/dt² = −(2π/T₀)²·q ; on remplace : [−(2π/T₀)² + 1/(LC)]·q = 0 pour tout t
  ⇒ (2π/T₀)² = 1/(LC) ⇒ **T₀ = 2π√(LC)**.
- Formule de T₀ utilisée sans démonstration dans toutes les autres sessions.

### T3 — Lire T (ou T₀) et trouver L ou C — 13 sessions, 0,25 à 0,75 pt
- L = T₀²/(4π²C) : 2016 N (6 ms ; 9,1·10⁻² H), 2017 R (60 ms ; 0,91 H), 2018 N (2,5 ms ; 63 mH), 2019 N (20 ms ; 1 H),
  2020 R (20 ms ; 0,2 H), 2021 N (21 ms ; 0,92 H), 2022 N (10 ms ; 0,05 H).
- C = T₀²/(4π²L) : 2019 R (10 ms ; 5 µF), 2020 N (10 ms ; 2,5 µF), 2022 R (0,10 s ; 250 µF), 2023 N (2 ms ; 0,1 µF).
- Lecture seule : 2025 N (2,8·10⁻⁴ s, échelle donnée par une flèche « 7·10⁻⁵ s » = 4 carreaux) ; comparer T et T₀ calculé : 2021 R.
- Phrase clé du sujet : « en assimilant la pseudo-période à la période propre » / « sachant que T ≈ T₀ ». « On prend π² = 10 » dans au moins 9 sessions.
- Lecture : « durée entre deux maxima successifs ».

### T4 — Reconnaître le régime / choisir une courbe — 9 sessions, 0,25 à 0,5 pt
- Nommer le régime : 2016 N, 2019 R, 2020 N (pseudo-périodique), 2021 N (périodique), 2018 N 3.1 « pourquoi pseudo-périodique » (r ≠ 0).
- Tableau R → courbe → régime : 2020 R (R₁ = 0 → pseudo-périodique ; R₂ = 390 Ω → **apériodique**, seule apparition du mot).
- Choisir parmi des courbes : 2019 N (critères : périodique car LC idéal + u_C(0) = E), 2022 N (même chose : C₁).
- Affecter deux courbes à deux R : 2021 R (plus R est grande, plus l'amortissement est fort).
- **Régime critique : jamais demandé.**

### T5 — Énergie : valeur à un instant, énergie perdue — 14 sessions, 0,25 à 0,75 pt
- Formule : **E_t = ½·C·u_C² + ½·L·i² = q²/(2C) + ½·L·i²**.
- À t = 0 (condensateur chargé, i = 0) : E_t = ½·C·E² (2019 N, 2022 N) ou q²/(2C) (2016 N, 2017 R, 2023 R).
- À un extremum de u_C ou q (i = 0) : seulement ½·C·u_C² (2016 N à 18 ms, 2023 R à t₁, 2024 N à t₂, 2025 N à t_A).
- LC idéal : E_t constante ⇒ E_m = E_t − ½·C·u_C² (2019 N, 2023 N) ou E_e = E_t − ½·L·i² (2020 N) ; E_t = ½·L·I_m² (2020 N) ;
  I_m = U_m·√(C/L) (2025 R) ; E(0) = E(T₀/4) (2017 R).
- Les deux termes à la fois : 2019 R (u_C et i lus), 2022 N (u_C et i lus), 2024 R (i = u_R/R).
- Énergie perdue = **E_t(début) − E_t(fin)** (Joule) : 2016 N, 2021 R, 2022 N, 2023 R, 2024 N, 2024 R, 2025 N.
- Courbes E_e(t) et E_m(t) : 2020 R (tableau, puis i = √(2E_m/L)), 2021 R.
- Expression seule (0,5) : 2022 N 2.2.1 ; 2024 R 2.2 (E_t = ½·(C·u_C² + (L/R²)·u_R²)).
- Où est l'énergie : 2024 N 1.3 (u_C = 0 ⇒ toute dans la bobine ; i = 0 ⇒ toute dans le condensateur).

### T6 — Expliquer l'amortissement — 6 sessions, 0,25 à 0,5 pt
- 2016 N 2.3 (interpréter ΔE < 0), 2018 N 3.1, 2020 R 3.2, 2023 R 2.2, 2024 N 1.1, 2025 N 2.3.
- Réponse type : « l'énergie totale diminue : elle est dissipée par **effet Joule** dans la résistance (r de la bobine, R) ».
- 2025 N 2.3 (seule démonstration) : dE_T/dt = C·u_C·du_C/dt + L·i·di/dt = i·(u_C + L·di/dt) = i·(−r·i) = **−r·i²**.

### T7 — Entretien des oscillations — 4 sessions, 0,5 à 0,75 pt
- 2016 N (k = 11 ⇒ r_b = 11 Ω), 2018 N (k = 5 ⇒ r = 5 Ω), 2020 N (k₀ = R + r = 100 Ω), 2023 R (k = R = 35 Ω).
- Méthode : u_b + u_C (+ u_R) = u_G = k·i ⇒ **L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0** ; oscillations sinusoïdales
  ⇒ terme en dq/dt nul ⇒ **k = R + r** (résistance totale). Le circuit oscille alors à T₀ (2018 N 3.4, 2020 N III.2).
- Le générateur est toujours décrit par « tension proportionnelle à l'intensité u_G = k·i » ; « résistance négative » : jamais écrit.

### T8 — Expression i(t) ou u_C(t) avec phase — 1 session (2020 N III.2, 0,75)
- i = I_m·cos(2πt/T₀ + φ) : I_m = 8 mA et T₀ = 10 ms lus ; i(0) = 0 ⇒ cos φ = 0 ; di/dt(0) < 0 (courbe qui descend)
  ⇒ −(2π/T₀)·I_m·sin φ < 0 ⇒ sin φ > 0 ⇒ **φ = +π/2**. C'est la seule détermination de φ en 10 ans.

### T9 — Instant initial et signe de i — 2 sessions
- 2024 R 2.1.1 (0,25) : i(0⁺) = 0 (continu dans la bobine) ⇒ u_R(0⁺) = 0 ⇒ **u_b(0⁺) = −u_C(0) = −E = −5 V**.
- 2025 N 2.2.2 (0,5) : i = C·du_C/dt ; u_C décroît entre t_A et t_B ⇒ **i < 0**.

## 3. Formules telles qu'écrites dans les corrigés

- u_b = L·di/dt + r·i (2020 N, 2020 R, 2024 R, 2025 N l'écrivent « u_L ») ; bobine idéale u_L = L·di/dt.
- i = dq/dt = C·du_C/dt ; di/dt = d²q/dt² = C·d²u_C/dt².
- Grille officielle 2023 R / 2024 N : « établir l'équation différentielle vérifiée par la tension aux bornes du condensateur ou par
  sa charge dans le cas d'amortissement » ; « expliquer, du point de vue énergétique, les trois régimes » ; « connaître le rôle du
  dispositif d'entretien, qui consiste à compenser l'énergie dissipée par effet Joule ».
- Solutions : q = Q_m·cos(2πt/T₀) ; u_C = U₀·cos(2πt/T₀) ; i = I_m·cos(2πt/T₀ + φ). **T₀ = 2π√(LC)** ; N₀ = 1/(2π√(LC)).
- Énergie : E_t = E_e + E_m ; E_e = ½·C·u_C² = q²/(2C) ; E_m = ½·L·i² ; dE_T/dt = −r·i² (ou −(R + r)·i²).
- Unités dans les A.N. : T₀ en s, C en F (12·10⁻⁶), L en H, q en C (120·10⁻⁶), i en A (12·10⁻³).

## 4. valeurs_reperes (vérifiées en Python)

| Session | L | C | R + r | T lue | T₀ = 2π√(LC) calculée | Énergie |
|---|---|---|---|---|---|---|
| 2016 N | 0,0912 H (trouvé) | 10 µF | r_b = 11 Ω | 6 ms | — | 7,2·10⁻⁴ J → 8,0·10⁻⁵ J ; ΔE = −6,4·10⁻⁴ J |
| 2017 R | 0,912 H (trouvé) | 100 µF | 0 | 60 ms | — | 1,8·10⁻³ J (Q_m = 600 µC ; I_m = 62,8 mA) |
| 2018 N | 63,3 mH (trouvé) | 2,5 µF | r = 5 Ω | 2,5 ms | — | — |
| 2019 N | 1,01 H (1 H avec π² = 10) | 10 µF | 0 | 20 ms | — | E_t = 5·10⁻⁴ J ; u_C(12 ms) = 10·cos(1,2π) = −8,09 V ; E_m = 1,8·10⁻⁴ J |
| 2019 R | 0,5 H | 5,07 µF (5 µF) | 50 Ω | 10 ms | — | E_t(9 ms) = 5,76·10⁻⁵ + 3,6·10⁻⁵ = 9,36·10⁻⁵ J |
| 2020 N | 1 H | 2,53 µF (2,5 µF) | 100 Ω | 10 ms | — | E_t = 3,2·10⁻⁵ J ; i(16 ms) = 8·sin(0,2π) = 4,70 mA (lu 4,8) ; E_e = 2,05·10⁻⁵ J |
| 2020 R | 0,203 H (0,2 H) | 50 µF | 10 Ω | 20 ms | — | 0,64 → 0,36 → 0,24 mJ ; U₀ = √(2 × 0,64·10⁻³/50·10⁻⁶) = 5,06 V |
| 2021 R | 0,51 H | 100 µF | 15 Ω / 105 Ω | 45 ms | 44,9 ms | q(0) = 0,6 mC ⇒ 1,80 mJ ; E_th = 0,54 mJ |
| 2022 N | 0,0507 H (0,05 H) | 50 µF | r | 10 ms | — | 3,6 mJ → 1,39 mJ ; ΔE = −2,21 mJ |
| 2023 N | 1 H | 0,101 µF (0,1 µF) | 0 | 2 ms | — | E_m(1,8 ms) = 1,8 µJ (u_C = 10·cos(1,8π) = 8,09 V) |
| 2023 R | 0,1 H | 10 µF | 35 Ω | — | 6,28 ms | 0,72 mJ → 0,08 mJ ; |ΔE| = 0,64 mJ ; k = 35 Ω |
| 2024 R | 20 mH | 0,10 µF | 50 Ω + r | — | 0,281 ms | E_t(0) = 1,25 µJ ; E_t(t₁) ≈ 0,11 µJ ⇒ E_j ≈ 1,14 µJ |
| 2025 N | 1,99 mH (non demandé) | 1 µF | r | 0,28 ms | — | ½·10⁻⁶·(100 − 49) = 2,55·10⁻⁵ J |

Ordres de grandeur : C de 0,22 nF à 250 µF (le plus souvent 2,5 à 100 µF) ; L de 2 mH à 1 H ; T₀ de 0,28 ms à 0,10 s
(le plus souvent 2 à 60 ms) ; énergies du nJ (2024 N) au mJ. Valeurs « rondes » grâce à π² = 10.

## 5. erreurs_examen (où l'on perd des points, et le geste qui corrige)

1. **Mettre E dans la maille de décharge** : le second membre est 0. Geste : refaire la maille après le basculement, sans générateur.
2. **Oublier r (ou R)** dans le terme en dq/dt, ou l'inverse : écrire r quand la bobine est « de résistance négligeable ». Geste : lister les dipôles de la maille.
3. **Confondre T et T/2** : lire entre deux maxima (ou deux passages par 0 dans le même sens), pas entre un max et un min.
   Lire sur plusieurs périodes quand c'est possible (2025 N : 4 carreaux de 7·10⁻⁵ s).
4. **Unités** : µF → 10⁻⁶ F, nF → 10⁻⁹, mH → 10⁻³ H, ms → s, µC/mC, et **mV** sur l'axe de u_R (2024 R). Geste : convertir avant la formule.
5. **Isoler L ou C** dans T₀ = 2π√(LC) : élever au carré d'abord, L = T₀²/(4π²C). Oublier le carré de T₀ donne un résultat absurde.
6. **cos ou sin, phase à t = 0** : condensateur chargé à t = 0 ⇒ q = Q_m·cos(2πt/T₀) (maximum au départ). Pour i : i(0) = 0
   ne suffit pas, il faut le sens de variation (2020 N : φ = +π/2, pas −π/2).
7. **Signe de i** : i = dq/dt = C·du_C/dt avec les flèches du schéma ; u_C décroît ⇒ i < 0 (2025 N). Lire i(t) avec son signe.
8. **Énergie à un instant** : oublier un des deux termes. Geste : si u_C est extrême, i = 0 ; si u_C = 0, i est extrême ; sinon les deux termes.
9. **Énergie perdue** : faire E(fin) − E(début) et annoncer une valeur négative comme « énergie dissipée ». Geste : |ΔE| = E(début) − E(fin) > 0.
   Prendre les deux instants à des extremums (i = 0) quand c'est possible.
10. **Lire u_C au mauvais endroit** : la valeur à t₂ est souvent négative (2024 N : −4,4 V) ; le carré enlève le signe, mais pas une mauvaise lecture.
11. **Entretien** : écrire k = r seulement alors qu'il y a aussi R (2020 N : k₀ = R + r = 100 Ω). Geste : k = résistance totale.
12. **Régimes** : plus R est grande, plus l'amortissement est fort ; « apériodique » = retour à 0 sans oscillation. Ne pas inverser les courbes (erreur du dépôt en 2021 R).
13. **u_b(0⁺)** : écrire 0 ou +E. Geste : i continu ⇒ i(0⁺) = 0 ⇒ u_R(0⁺) = 0 ⇒ u_b(0⁺) = −u_C(0).

## 6. Erreurs et incohérences repérées dans le dépôt (calculs vérifiés en Python)

Questions RLC :
- **2023 R 1.3 et 2.3 — lecture fausse (×10).** La figure 3 (assets/fig3p5.png) et la figure 2 (fig2p4.png) donnent
  q(0) = q_max = **120 µC** et q(t₁) = **40 µC** (graduation 40 µC). Le dépôt lit 12 µC et 8 µC, calcule 7,2·10⁻⁶ J et 4·10⁻⁶ J,
  puis écrit « 0,72 mJ » et « 0,64 mJ » (deux erreurs qui se compensent). Juste : (120·10⁻⁶)²/(2·10⁻⁵) = 7,2·10⁻⁴ J = 0,72 mJ ;
  (120² − 40²)·10⁻¹²/(2·10⁻⁵) = 6,4·10⁻⁴ J = 0,64 mJ (grille officielle). E = q_max/C = 12 V (le dépôt dit 1,2 V).
  2.4 (dépôt) parle de « régime pseudo-périodique non amorti » : dire « oscillations sinusoïdales (régime périodique) ».
- **2024 R 2.3 — faux.** Le dépôt lit u_C(t₁) ≈ 3 V et u_R(t₁) ≈ 2 V (axe en **mV** ignoré) et calcule ½(0,9 + 32)·10⁻⁶ = 16,45 µJ, écrit
  « 0,1645 µJ », puis 1,25 − 0,16 ≈ 1,1 µJ (bon par hasard). Sur la page du sujet (pages/sujet_p5.jpg) : u_C(t₁) ≈ −1,5 V et
  u_R(t₁) ≈ 5 mV ⇒ E_t(t₁) = ½·10⁻⁷·1,5² + ½·0,02·(10⁻⁴)² ≈ 0,11 µJ ⇒ **E_j ≈ 1,14 µJ ≈ 1,1 µJ**.
  2.1.2 (dépôt) ajoute « si on néglige r … » : la réponse attendue est L·C·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0.
- **2024 N 1.4 — lecture fausse.** Dépôt : u_C(t₂) = 4 V ⇒ 2,2·10⁻⁹ J. Figure 2 (assets/fig2p4.png) : u_C(t₂) ≈ −4,4 V
  ⇒ ½·2,2·10⁻¹⁰·(36 − 19,4) = **1,83·10⁻⁹ J** (grille officielle). 1.2 (dépôt) écrit u_R = (R + r)·i et u_L = L·di/dt : r appartient à la bobine.
- **2021 R III.1 — courbes inversées dans le dépôt.** Figure 5 (fig5p6.png) : (a) trait plein peu amorti ⇒ R₃ = 10 Ω ; (b) pointillés très
  amortis ⇒ R₄ = 100 Ω (corrigé officiel juste). III.2 du dépôt dit « sur la courbe (b) » : il faut lire T = 45 ms sur (a).
- **2019 N — barème faux dans exam.json.** II.2.1 vaut 0,5 pt sur le sujet (pages/sujet_p5.jpg), pas 1 ; I.1 et I.2 valent 0,5 chacune (pas 0,25).
  Le total 4,5 tombe juste par hasard. Partie RLC officielle : 2,5 pts (dépôt : 3).
- **Figures mal liées** :
  2022 N : doc_ex3_1 → fig1p7.png (tube de mécanique) au lieu de fig1p5.png ; doc_ex3_2 → fig2p7.png au lieu de fig2p5.png ;
  doc_ex3_3 → fig3p8.png (satellite) au lieu de **fig3p6.png** (courbes C₁, C₂, C₃) ; la figure 4 (**fig4p6.png**, i(t) et u_C(t)) n'est pas listée
  et 2.2.2 pointe vers la figure RC.
  2022 R : 2.1 et 2.2 pointent vers doc_ex3_4 / doc_ex3_5 (plan incliné, x(t)) au lieu de doc_ex3_1 (fig4p6.png) / doc_ex3_2 (fig5p6.png).
  2023 R : les deux documents de l'exercice 3 sont fig2p6.png / fig3p6.png (mécanique) ; il faut fig1p4.png, fig2p4.png, **fig3p5.png**.
  2024 N : doc_ex4_1 → fig1p5.png (cylindre) ; le schéma fig1p4.png et la courbe **fig2p4.png** ne sont pas listés.
- **Données absentes d'exam.json** (présentes seulement dans sujet_text) : 2024 N C = 0,22 nF ; 2022 R L = 1 H ; 2020 N R = 90 Ω
  (nécessaire pour k₀) ; 2025 N I₀ = 1 µA (partie RC). Sans elles, l'élève ne peut pas répondre.
- Corrigés de prof (extraction.json), fautes de frappe sans effet sur le dépôt : 2021 N « dq/dt = −(2π/T₀)·Q_m·cos » (il faut sin) ;
  2021 R « 1,80 mJ = 180 mJ » ; 2020 N « φ = π/2 s » ; 2022 N « ΔE = E₁ + E₀ » (il faut −). Le dépôt est juste sur ces points.
- 2021 N (piège, pas une erreur) : la figure 4 donne Q_m ≈ 144 µC, donc u_C(0) = 12 V, alors que la partie RC utilise E = 6 V.
- Vérifiés justes : 2016 N, 2017 R, 2018 N, 2019 N (valeurs), 2019 R, 2020 N, 2020 R (i₁ = 44,7 mA), 2021 N, 2022 N, 2022 R, 2023 N, 2025 N, 2025 R.

Hors RLC (même exercices, signalé en passant) :
- 2016 N partie RC (dépôt) : r = 20 Ω (conducteur) est écrit r_b (résistance de la bobine) dans 1.1 à 1.4.3.
- 2024 R 1.2.2 (RC) : l'axe de la figure 2 est en **µs** : τ = 5 µs ⇒ C = 5·10⁻⁶/50 = 0,10 µF (le dépôt lit des ms).
- 2025 N 3.2 (AM) : ligne intermédiaire « 80 × … » au lieu de 40 ; résultat 4,76·10⁻¹⁰ F juste (calcul exact 4,83·10⁻¹⁰ F avec π vrai).
- Circuit d'accord : le dépôt écrit « fréquence de résonance » (2018 R, 2023 R) ; le sujet dit « fréquence propre ». À éviter (résonance hors programme ici).

## 7. Figures utiles à reproduire à la craie

- Schéma charge / décharge à interrupteur double : 2016 N assets/fig1p5.png (E, r, R | C | bobine L, r_b) ; 2025 N fig1p4.png (générateur de courant, C₀, bobine).
- q(t) pseudo-périodique avec valeurs (120 → 80 → 60 → 40 µC, T = 6 ms) : 2016 N fig3p6.png — le meilleur pour ΔE entre deux maxima.
- q(t) sinusoïdale, Q_m = 600 µC, T₀ = 60 ms : 2017 R fig3p5.png. u_C(t) LC, 10 V, T₀ = 2 ms, échelles en flèches : 2023 N fig4p4.png.
- Trois courbes (a) amortie / (b) cos / (c) −sin à départager : 2019 N fig3p5.png ; variante C₁ / C₂ / C₃ : 2022 N fig3p6.png.
- u_C(t) et i(t) côte à côte (déphasage, lecture à un instant) : 2019 R fig4p5.png ; 2022 N fig4p6.png.
- Pseudo-périodique et apériodique (R = 0 et R = 390 Ω) : 2020 R fig3p5.png. Deux amortissements (R₃, R₄) : 2021 R fig5p6.png.
- Courbes E_e(t) et E_m(t) : 2020 R fig4p6.png (deux graphes) ; 2021 R fig6p7.png (sur le même graphe, 1,80 / 1,26 mJ).
- i(t) entretenue, I_m = 8 mA, T₀ = 10 ms, départ en descendant (φ = π/2) : 2020 N fig6p6.png ; q(t) entretenue : 2018 N fig6p6.png.
- u_C(t) avec t_A, t_B et flèche d'échelle 7·10⁻⁵ s : 2025 N fig3p5.png. u_C(t) avec t₁, t₂ (où est l'énergie) : 2024 N fig2p4.png.
- u_C(t) et u_R(t) en mV avec t₁ : 2024 R fig3p5.png + fig4p5.png (prendre plutôt pages/sujet_p5.jpg, plus lisible).

## 8. Au programme mais jamais (ou presque) demandé

- **Régime critique** : jamais. **Régime apériodique** : une fois (2020 R, dans un tableau).
- **Homogénéité / analyse dimensionnelle de √(LC)** : jamais (seulement T₀ = 2π√(L/g) en mécanique, 2018 R).
- **ω₀** : jamais écrit ; toujours 2π/T₀. **Phase φ** : une seule fois (2020 N, sur i). Solution avec sin : jamais.
- **dE/dt = −R·i²** : une seule fois (2025 N, avec r).
- **Entretien** : 4 fois, toujours par k = résistance totale ; montage à amplificateur, « résistance négative » : jamais.
- **u_b(0⁺)** au début de la décharge : une fois (2024 R, 0,25 pt).
- **Résonance, RLC forcé, facteur de qualité, R critique** : jamais (hors programme, confirmé).
- Toujours présent : lire T puis calculer L ou C avec T₀ = 2π√(LC), et un calcul d'énergie ½·C·u_C² + ½·L·i².
