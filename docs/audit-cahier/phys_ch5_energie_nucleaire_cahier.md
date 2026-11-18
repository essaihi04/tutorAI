# Le cahier de l'élève — `phys_ch5_energie_nucleaire` (Noyaux, masse et énergie)

18 novembre 2026, skill `cahier-de-l-eleve`. Cahier idéal du chapitre, écrit d'un seul tenant, puis découpé dans
`blocs[].cahier`, `blocs[].cahier_figures`, `concentration.cahier`, `concentration.cahier_figures` du cours en ligne
(`backend/data/courses/phys_ch5_energie_nucleaire.json`) et de sa copie en attente
(`backend/data/courses/en_attente/phys_ch5_energie_nucleaire.json`). Aucun autre champ n'a été touché.

## Règles de mise en page suivies

- Les parties **I à X** sont les titres des `activities`, que le lecteur écrit lui-même en tête du bloc où elles
  commencent ; le cahier numérote dedans **1., 2.…**, en continu d'un bloc à l'autre, et repart à 1 à chaque partie.
- **3 à 6 lignes** et **0 à 2 figures** par bloc ; un nombre de lignes toujours **différent** du nombre de diapositives
  du bloc (sinon `TableauCahier` range chaque ligne sous le titre numéroté d'une diapositive et la numérotation double).
- « Définition : » mot pour mot ; « Méthode « … » : 1) 2) 3) » pour chaque cas type du national
  (`exploration/energie_nucleaire.json`) ; « Attention : » pour les pertes de points relevées (`erreurs_examen`) ;
  « Remarque : », « Exemple : », « Rappel : ».
- Bulle de chaque diapositive : sa trace en une ou deux lignes.

## Le plan du cahier

- **I. La masse peut devenir énergie** : 1. Le Soleil ; rappels (joule, puissances de dix) · 2. Énergie de masse
  E = m·c² (unités) ; ΔE = Δm·c² · 3. L'unité u (définition, 1,66·10⁻²⁷ kg) · 4. eV, MeV, 1 u = 931,5 MeV/c²,
  méthode « E = Δm·c² » (u → MeV ; kg → J).
- **II. Le défaut de masse** : 1. Rappel ᴬ_Z X ; le noyau pèse moins que ses nucléons · 2. Définition, formule,
  méthode « Δm » (2022 R).
- **III. L'énergie de liaison** : 1. Définition, E_ℓ = Δm·c², exemple ⁴He · 2. E_ℓ/A.
- **IV. Stabilité et courbe d'Aston** : 1. Stabilité par E_ℓ/A, méthode « le plus stable », piège E_ℓ · 2. Courbe
  d'Aston, fusion / fission, 2023 N.
- **V. Réactions provoquées** : 1. Spontanée / provoquée, Soddy · 2. Fission, réaction en chaîne · 3. Fusion,
  méthode « A et Z » (en ligne : 3. pénétration et dangers, 4. fusion).
- **VI. Énergie libérée par les masses** : 1. La masse diminue, Δm, ΔE, E_lib, « liaison » ≠ « libérée » ·
  2. Méthode « énergie libérée » ; fission, 2016 N, 2017 R.
- **VII. Énergie libérée par les énergies de liaison** : 1. Méthode « diagramme », ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits),
  E_ℓ = A·(E_ℓ/A), 2023 N, 2020 N.
- **VIII. L'énergie d'un échantillon** : 1. N = m·N_A/M · 2. E = N·E_lib, fusion / fission, 2025 N ·
  3. Pénétration, dangers (en attente).
- **IX. Cas types du national** : 1. Le mot de la question ; piège 2019 N.
- **X. Bilan**.

## Le cahier idéal (copie en attente)

### I. La masse peut devenir énergie

*Bloc `en_s1_b0` — Avant de commencer : l'énergie et les puissances de dix*

- 1. Le Soleil rayonne de l'énergie et sa masse diminue : la masse peut devenir énergie.
- Rappel : l'énergie ne disparaît pas, elle change de forme ; unité : le joule (J).
- Rappel : 10³ = 1 000 ; 10⁻³ = 0,001 ; 10ᵃ × 10ᵇ = 10ᵃ⁺ᵇ ; notation scientifique : c = 3,00·10⁸ m/s.
- Exemple : c² = (3,00·10⁸)² = 9,00·10¹⁶ m²/s².

*Bloc `en_s1_b1` — E = m·c² et l'unité de masse u*

- 2. Énergie de masse : toute particule de masse m, au repos, possède une énergie de masse E = m·c².
- E en J, m en kg, c = 3,00·10⁸ m/s (célérité de la lumière dans le vide).
- Si la masse d'un système diminue de Δm, il libère ΔE = Δm·c² (1 g ↔ 9·10¹³ J).
- 3. Définition : l'unité de masse atomique u est le douzième de la masse d'un atome de carbone 12.
- 1 u = M(¹²C)/(12·N_A) = 12·10⁻³/(12 × 6,02·10²³) = 1,66·10⁻²⁷ kg ≈ la masse d'un nucléon.

*Bloc `en_s1_b1b` — L'électronvolt, 1 u = 931,5 MeV/c², l'énergie de masse*

- 4. 1 eV = 1,6·10⁻¹⁹ J ; 1 MeV = 10⁶ eV = 1,6·10⁻¹³ J ; MeV/c² est une unité de masse (m = E/c²).
- 1 u = 931,5 MeV/c² (1 u × c² = 1,4924·10⁻¹⁰ J = 931,5 MeV).
- Méthode « E = Δm·c² » : Δm en u → E = Δm × 931,5 MeV ; Δm en kg → E = Δm × (3,00·10⁸)² en J.
- Exemple : proton, E₀ = m_p·c² = 1,00728 × 931,5 MeV ≈ 938,3 MeV ≈ 1,50·10⁻¹⁰ J.


### II. Le défaut de masse

*Bloc `en_s1_b2` — Le noyau, on le pèse : le défaut de masse*

- 1. Rappel : le noyau ᴬ_Z X contient A nucléons : Z protons et N = A − Z neutrons.
- Constat : la masse d'un noyau est inférieure à la somme des masses de ses nucléons séparés (⁴He : 4,00150 u < 4,03188 u).
- 2. Définition : le défaut de masse d'un noyau est la différence entre la somme des masses de ses nucléons séparés, au repos, et la masse du noyau au repos.
- Δm = Z·m_p + (A − Z)·m_n − m(ᴬ_Z X) > 0, avec m_p = 1,00728 u et m_n = 1,00866 u.
- Méthode « Δm » : 1) Z et N ; 2) la relation ; 3) les valeurs ; 4) le résultat en u (¹⁴C : Δm = 0,11301 u).


### III. L'énergie de liaison

*Bloc `en_s1_b3` — L'énergie de liaison*

- 1. Définition : l'énergie de liaison E_ℓ est l'énergie qu'il faut fournir à un noyau au repos pour le séparer en ses nucléons au repos.
- Former le noyau libère la même énergie : E_ℓ = E(nucléons séparés) − E(noyau) = Δm·c².
- E_ℓ = [Z·m_p + (A − Z)·m_n − m(ᴬ_Z X)]·c² : en MeV avec Δm en u (× 931,5) ; en J avec Δm en kg.
- Exemple : ⁴He, E_ℓ = 0,03038 × 931,5 MeV ≈ 28,30 MeV ≈ 4,53·10⁻¹² J.
- 🖉 **Séparer ou former le noyau** — Séparer le noyau coûte E_{ℓ} ; le former libère la même énergie E_{ℓ} = Δm·c² : les nucléons séparés sont plus haut.


### IV. Stabilité et courbe d'Aston

*Bloc `en_s2_b1` — E_ℓ/A et la stabilité*

- 2. Énergie de liaison par nucléon : E_ℓ/A, en MeV/nucléon (⁴He : 28,30/4 = 7,07 MeV/nucléon).
- 1. Un noyau est d'autant plus stable que son énergie de liaison par nucléon E_ℓ/A est grande.
- Méthode « le plus stable » : calculer E_ℓ/A de chaque noyau, puis comparer.
- Attention : comparer E_ℓ/A, jamais E_ℓ : ²³⁵U a E_ℓ = 1783,5 MeV mais 7,59 MeV/nucléon < ⁵⁶Fe : 8,79.

*Bloc `en_s2_b2` — La courbe d'Aston*

- 2. Courbe d'Aston : −E_ℓ/A (MeV/nucléon) en fonction de A ; plus un point est bas, plus le noyau est stable.
- Elle descend vite, passe par un creux (fer, A ≈ 56, ≈ −8,8 MeV/nucléon), puis remonte doucement.
- Noyaux légers (A < 20 environ) → fusion ; lourds (A > 190 environ) → fission : les deux vont vers le creux et libèrent de l'énergie.
- Remarque : 20 < A < 190 environ : les noyaux les plus stables.
- Exemple (2023 N) : E_ℓ/A(³H) = 2,825 > E_ℓ/A(²H) = 1,183 MeV/nucléon : ³H est plus stable.
- 🖉 **La courbe d'Aston** — Plus un point est bas, plus le noyau est stable (creux vers le fer, A ≈ 56) : légers → fusion, lourds → fission.


### V. Réactions provoquées : fission et fusion

*Bloc `en_s2_b3` — Spontanée ou provoquée, la fission, la réaction en chaîne*

- 1. Réaction spontanée : le noyau se transforme seul (α, β⁻, β⁺) ; provoquée : il faut agir sur le noyau.
- Dans toute réaction nucléaire : conservation de A et de Z (lois de Soddy).
- 2. Définition : la fission est une réaction nucléaire provoquée au cours de laquelle un noyau lourd, frappé par un neutron, se scinde en deux noyaux plus légers.
- Exemple : ²³⁵₉₂U + ¹₀n → ⁹⁴₃₈Sr + ¹⁴⁰₅₄Xe + 2 ¹₀n (le neutron, neutre, n'est pas repoussé).
- Réaction en chaîne : les neutrons émis provoquent d'autres fissions ; contrôlée : centrale ; sinon : bombe A.

*Bloc `en_s2_b4` — Deux charges positives, la fusion, l'équation*

- Rappel : deux charges de même signe se repoussent : deux noyaux (positifs) se repoussent.
- 3. Définition : la fusion est une réaction nucléaire provoquée au cours de laquelle deux noyaux légers s'unissent pour former un noyau plus lourd.
- Il faut une température (≈ 10⁸ K) et une pression très élevées (cœur des étoiles) : ²₁H + ³₁H → ⁴₂He + ¹₀n.
- Méthode « A et Z » : conservation de A puis de Z ; 235 + 1 = 94 + 140 + x ⇒ x = 2 neutrons.
- Attention : ne pas oublier le neutron incident à gauche et les neutrons émis à droite.


### VI. Énergie libérée : par les masses

*Bloc `en_s3_b1` — La masse diminue : Δm, ΔE, E_lib*

- 1. Dans une réaction nucléaire qui libère de l'énergie, la masse des produits est inférieure à celle des réactifs.
- Δm = Σm(produits) − Σm(réactifs) < 0 ; ΔE = Δm·c² < 0 : le système cède de l'énergie au milieu.
- Énergie libérée : E_lib = |ΔE| > 0, surtout en énergie cinétique des produits et en rayonnement γ.
- Attention : « énergie de liaison » → un noyau, Δm > 0 ; « énergie libérée » → une réaction, Δm < 0.

*Bloc `en_s3_b2` — Calculer l'énergie libérée avec les masses (exercices du national joués)*

- 2. Méthode « énergie libérée » : 1) l'équation complète ; 2) Δm = Σm(produits) − Σm(réactifs) ; 3) ΔE = Δm × 931,5 MeV ; 4) E_lib = |ΔE|.
- Fission de ²³⁵U : Δm = −0,19834 u ; ΔE ≈ −184,8 MeV ; E_lib ≈ 185 MeV ≈ 2,96·10⁻¹¹ J.
- Fusion (2016 N) : Δm = 5,01016 − 5,02905 = −0,01889 u ; E_lib = 0,01889 × 931,5 ≈ 17,6 MeV.
- Attention : toutes les particules entrent dans Δm (e⁻, e⁺, n) : ⁶⁰₂₇Co → ⁶⁰₂₈Ni + ⁰₋₁e, E_lib = 2,82 MeV (2017 R).


### VII. Énergie libérée : par les énergies de liaison

*Bloc `en_s3_b3` — Les énergies de liaison et le diagramme (exercices du national joués)*

- 1. Méthode « diagramme » : 1) en haut, les nucléons séparés ; 2) plus bas, E_i des réactifs ; 3) encore plus bas, E_f des produits ; 4) ΔE = E_f − E_i.
- ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits) (ordre inverse des masses) ; nucléon seul ou électron : E_ℓ = 0.
- Si l'énoncé donne E_ℓ/A : E_ℓ = A·(E_ℓ/A) pour chaque noyau, avant le bilan.
- Exemple (2023 N) : ΔE = (2,366 + 8,475) − (28,296 + 0) = −17,455 MeV ; E_lib ≈ 17,5 MeV.
- Lire un diagramme (2020 N) : chaque flèche vaut énergie d'arrivée − énergie de départ ; garder le facteur 10⁵.
- 🖉 **Diagramme énergétique de la fusion** — On casse les réactifs (on fournit 10,841 MeV), on forme les produits (on récupère 28,296 MeV) : ΔE = −17,455 MeV.


### VIII. L'énergie d'un échantillon, applications et dangers

*Bloc `en_s4_b1` — D'un noyau à un échantillon*

- 1. Nombre de noyaux : N = n·N_A = m·N_A/M (m en g, M en g/mol, N_A = 6,02·10²³ mol⁻¹).
- 2. Énergie d'un échantillon : E = N·E_lib ; 1 g d'²³⁵U : N ≈ 2,56·10²¹ ; E ≈ 4,7·10²³ MeV ≈ 7,6·10¹⁰ J.
- Remarque : 7,6·10¹⁰ J ≈ la combustion de 1,8 tonne de pétrole.
- À masse égale, la fusion libère plus d'énergie que la fission (≈ 3,5 contre 0,78 MeV par nucléon).
- Exemple (2025 N) : β⁺ du ¹⁰⁷Cd, E_lib = 0,402 MeV ; E = N_d·E_lib = 5,62·10¹⁵ × 0,402 ≈ 2,26·10¹⁵ MeV.


### IX. Cas types du national

*Bloc `en_s4_b2` — Applications, dangers et cas types du national*

- 3. Pénétration : α arrêté par du papier, β par quelques mm d'aluminium, γ par du plomb ou du béton épais.
- Dangers : cellules abîmées (brûlures, cancers) ; se protéger : distance, durée, écran (plomb, béton).
- 1. Le mot de la question : liaison → Δm > 0, E_ℓ ; stable → E_ℓ/A ; libérée → E_lib = |ΔE| ; échantillon → N·E_lib ; A et Z → Soddy.
- Attention (2019 N) : multiplier chaque E_ℓ/A par A : ΔE = 1707,18 − (1685,14 + 28,28) = −6,24 MeV (et non 7,11).
- 🖉 **Pouvoir de pénétration** — α est arrêté par le papier, β par quelques mm d'aluminium ; γ traverse les deux : il faut du plomb ou du béton épais.


### X. Bilan du chapitre

*Bloc `en_s4_b3` — Bilan du chapitre*

- Bilan : E = m·c² ; 1 u = 1,66·10⁻²⁷ kg = 931,5 MeV/c² ; 1 MeV = 1,6·10⁻¹³ J.
- Δm = Z·m_p + (A − Z)·m_n − m(ᴬ_Z X) ; E_ℓ = Δm·c² ; stabilité : E_ℓ/A.
- Réaction : ΔE = Δm·c² = ΣE_ℓ(réactifs) − ΣE_ℓ(produits) ; E_lib = |ΔE| ; échantillon : E = N·E_lib.


## Le cahier du cours en ligne (son ordre)

Le cours en ligne place le rappel de la composition du noyau en fin de séance 1 (il ouvre donc la partie II dans le
bloc `en_s1_b1b`), « applications et dangers » juste après la réaction en chaîne (partie V, 3.), le calcul de la fusion
avant celui de la fission, et le bilan dans le bloc des cas types. Mêmes lignes, renumérotées dans cet ordre.

### I. La masse peut devenir énergie

*Bloc `en_s1_b0` — Avant de commencer : l'énergie et les puissances de dix*

- 1. Le Soleil rayonne de l'énergie et sa masse diminue : la masse peut devenir énergie.
- Rappel : l'énergie ne disparaît pas, elle change de forme ; unité : le joule (J).
- Rappel : 10³ = 1 000 ; 10⁻³ = 0,001 ; 10ᵃ × 10ᵇ = 10ᵃ⁺ᵇ ; notation scientifique : c = 3,00·10⁸ m/s.
- Exemple : c² = (3,00·10⁸)² = 9,00·10¹⁶ m²/s².

*Bloc `en_s1_b1` — E = m·c² et l'unité de masse u*

- 2. Énergie de masse : toute particule de masse m, au repos, possède une énergie de masse E = m·c².
- E en J, m en kg, c = 3,00·10⁸ m/s (célérité de la lumière dans le vide).
- Si la masse d'un système diminue de Δm, il libère ΔE = Δm·c² (1 g ↔ 9·10¹³ J).
- 3. Définition : l'unité de masse atomique u est le douzième de la masse d'un atome de carbone 12.
- 1 u = M(¹²C)/(12·N_A) = 12·10⁻³/(12 × 6,02·10²³) = 1,66·10⁻²⁷ kg ≈ la masse d'un nucléon.


### II. Le défaut de masse

*Bloc `en_s1_b1b` — L'électronvolt, 1 u = 931,5 MeV/c², la composition du noyau*

- 4. 1 eV = 1,6·10⁻¹⁹ J ; 1 MeV = 10⁶ eV = 1,6·10⁻¹³ J ; MeV/c² est une unité de masse (m = E/c²).
- 1 u = 931,5 MeV/c² (1 u × c² = 1,4924·10⁻¹⁰ J = 931,5 MeV).
- Méthode « E = Δm·c² » : Δm en u → E = Δm × 931,5 MeV ; Δm en kg → E = Δm × (3,00·10⁸)² en J.
- Exemple : proton, E₀ = m_p·c² = 1,00728 × 931,5 MeV ≈ 938,3 MeV ≈ 1,50·10⁻¹⁰ J.
- 1. Rappel : le noyau ᴬ_Z X contient A nucléons : Z protons et N = A − Z neutrons.

*Bloc `en_s1_b2` — Le défaut de masse*

- Constat : la masse d'un noyau est inférieure à la somme des masses de ses nucléons séparés (⁴He : 4,00150 u < 4,03188 u).
- 2. Définition : le défaut de masse d'un noyau est la différence entre la somme des masses de ses nucléons séparés, au repos, et la masse du noyau au repos.
- Δm = Z·m_p + (A − Z)·m_n − m(ᴬ_Z X) > 0, avec m_p = 1,00728 u et m_n = 1,00866 u.
- Méthode « Δm » : 1) Z et N ; 2) la relation ; 3) les valeurs ; 4) le résultat en u (¹⁴C : Δm = 0,11301 u).


### III. L'énergie de liaison

*Bloc `en_s1_b3` — L'énergie de liaison*

- 1. Définition : l'énergie de liaison E_ℓ est l'énergie qu'il faut fournir à un noyau au repos pour le séparer en ses nucléons au repos.
- Former le noyau libère la même énergie : E_ℓ = E(nucléons séparés) − E(noyau) = Δm·c².
- E_ℓ = [Z·m_p + (A − Z)·m_n − m(ᴬ_Z X)]·c² : en MeV avec Δm en u (× 931,5) ; en J avec Δm en kg.
- Exemple : ⁴He, E_ℓ = 0,03038 × 931,5 MeV ≈ 28,30 MeV ≈ 4,53·10⁻¹² J.
- 🖉 **Séparer ou former le noyau** — Séparer le noyau coûte E_{ℓ} ; le former libère la même énergie E_{ℓ} = Δm·c² : les nucléons séparés sont plus haut.


### IV. Stabilité et courbe d'Aston

*Bloc `en_s2_b1` — E_ℓ/A et la stabilité*

- 2. Énergie de liaison par nucléon : E_ℓ/A, en MeV/nucléon (⁴He : 28,30/4 = 7,07 MeV/nucléon).
- 1. Un noyau est d'autant plus stable que son énergie de liaison par nucléon E_ℓ/A est grande.
- Méthode « le plus stable » : calculer E_ℓ/A de chaque noyau, puis comparer.
- Attention : comparer E_ℓ/A, jamais E_ℓ : ²³⁵U a E_ℓ = 1783,5 MeV mais 7,59 MeV/nucléon < ⁵⁶Fe : 8,79.

*Bloc `en_s2_b2` — La courbe d'Aston*

- 2. Courbe d'Aston : −E_ℓ/A (MeV/nucléon) en fonction de A ; plus un point est bas, plus le noyau est stable.
- Elle descend vite, passe par un creux (fer, A ≈ 56, ≈ −8,8 MeV/nucléon), puis remonte doucement.
- Noyaux légers (A < 20 environ) → fusion ; lourds (A > 190 environ) → fission : les deux vont vers le creux et libèrent de l'énergie.
- Remarque : 20 < A < 190 environ : les noyaux les plus stables.
- Exemple (2023 N) : E_ℓ/A(³H) = 2,825 > E_ℓ/A(²H) = 1,183 MeV/nucléon : ³H est plus stable.
- 🖉 **La courbe d'Aston** — Plus un point est bas, plus le noyau est stable (creux vers le fer, A ≈ 56) : légers → fusion, lourds → fission.


### V. Réactions provoquées : fission et fusion

*Bloc `en_s2_b3` — Spontanée ou provoquée, la fission, la réaction en chaîne*

- 1. Réaction spontanée : le noyau se transforme seul (α, β⁻, β⁺) ; provoquée : il faut agir sur le noyau.
- 2. Définition : la fission est une réaction nucléaire provoquée au cours de laquelle un noyau lourd, frappé par un neutron, se scinde en deux noyaux plus légers.
- Réaction en chaîne : les neutrons émis provoquent d'autres fissions ; contrôlée : centrale ; sinon : bombe A.
- 3. Pénétration : α arrêté par du papier, β par quelques mm d'aluminium, γ par du plomb ou du béton épais.
- Dangers : cellules abîmées (brûlures, cancers) ; se protéger : distance, durée, écran (plomb, béton).
- 🖉 **Pouvoir de pénétration** — α est arrêté par le papier, β par quelques mm d'aluminium ; γ traverse les deux : il faut du plomb ou du béton épais.

*Bloc `en_s2_b4` — Deux charges positives, la fusion, l'équation*

- Rappel : deux charges de même signe se repoussent : deux noyaux (positifs) se repoussent.
- 4. Définition : la fusion est une réaction nucléaire provoquée au cours de laquelle deux noyaux légers s'unissent pour former un noyau plus lourd.
- Il faut une température (≈ 10⁸ K) et une pression très élevées (cœur des étoiles) : ²₁H + ³₁H → ⁴₂He + ¹₀n.
- Méthode « A et Z » : conservation de A puis de Z ; 235 + 1 = 94 + 140 + x ⇒ x = 2 neutrons.
- Attention : ne pas oublier le neutron incident à gauche et les neutrons émis à droite.


### VI. Énergie libérée : par les masses

*Bloc `en_s3_b1` — La masse diminue : Δm, ΔE, E_lib*

- 1. Dans une réaction nucléaire qui libère de l'énergie, la masse des produits est inférieure à celle des réactifs.
- Δm = Σm(produits) − Σm(réactifs) < 0 ; ΔE = Δm·c² < 0 : le système cède de l'énergie au milieu.
- Énergie libérée : E_lib = |ΔE| > 0, surtout en énergie cinétique des produits et en rayonnement γ.
- Attention : « énergie de liaison » → un noyau, Δm > 0 ; « énergie libérée » → une réaction, Δm < 0.

*Bloc `en_s3_b2` — Calculer l'énergie libérée avec les masses*

- 2. Méthode « énergie libérée » : 1) l'équation complète ; 2) Δm = Σm(produits) − Σm(réactifs) ; 3) ΔE = Δm × 931,5 MeV ; 4) E_lib = |ΔE|.
- Fusion (2016 N) : Δm = 5,01016 − 5,02905 = −0,01889 u ; E_lib = 0,01889 × 931,5 ≈ 17,6 MeV.
- Fission de ²³⁵U : Δm = −0,19834 u ; ΔE ≈ −184,8 MeV ; E_lib ≈ 185 MeV ≈ 2,96·10⁻¹¹ J.
- Attention : toutes les particules entrent dans Δm (e⁻, e⁺, n) : ⁶⁰₂₇Co → ⁶⁰₂₈Ni + ⁰₋₁e, E_lib = 2,82 MeV (2017 R).


### VII. Énergie libérée : par les énergies de liaison

*Bloc `en_s3_b3` — Les énergies de liaison et le diagramme*

- 1. Méthode « diagramme » : 1) en haut, les nucléons séparés ; 2) plus bas, E_i des réactifs ; 3) encore plus bas, E_f des produits ; 4) ΔE = E_f − E_i.
- ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits) (ordre inverse des masses) ; nucléon seul ou électron : E_ℓ = 0.
- Si l'énoncé donne E_ℓ/A : E_ℓ = A·(E_ℓ/A) pour chaque noyau, avant le bilan.
- Exemple (2023 N) : ΔE = (2,366 + 8,475) − (28,296 + 0) = −17,455 MeV ; E_lib ≈ 17,5 MeV.
- Lire un diagramme (2020 N) : chaque flèche vaut énergie d'arrivée − énergie de départ ; garder le facteur 10⁵.
- 🖉 **Diagramme énergétique de la fusion** — On casse les réactifs (on fournit 10,841 MeV), on forme les produits (on récupère 28,296 MeV) : ΔE = −17,455 MeV.


### VIII. L'énergie d'un échantillon

*Bloc `en_s4_b1` — D'un noyau à un échantillon*

- 1. Nombre de noyaux : N = n·N_A = m·N_A/M (m en g, M en g/mol, N_A = 6,02·10²³ mol⁻¹).
- 2. Énergie d'un échantillon : E = N·E_lib ; 1 g d'²³⁵U : N ≈ 2,56·10²¹ ; E ≈ 4,7·10²³ MeV ≈ 7,6·10¹⁰ J.
- Remarque : 7,6·10¹⁰ J ≈ la combustion de 1,8 tonne de pétrole.
- À masse égale, la fusion libère plus d'énergie que la fission (≈ 3,5 contre 0,78 MeV par nucléon).
- Exemple (2025 N) : β⁺ du ¹⁰⁷Cd, E_lib = 0,402 MeV ; E = N_d·E_lib = 5,62·10¹⁵ × 0,402 ≈ 2,26·10¹⁵ MeV.


### IX. Cas types du national


### X. Bilan du chapitre

*Bloc `en_s4_b2` — Cas types du national et bilan du chapitre*

- 1. Le mot de la question : liaison → Δm > 0, E_ℓ ; stable → E_ℓ/A ; libérée → E_lib = |ΔE| ; échantillon → N·E_lib ; A et Z → Soddy.
- Attention (2019 N) : multiplier chaque E_ℓ/A par A : ΔE = 1707,18 − (1685,14 + 28,28) = −6,24 MeV (et non 7,11).
- Bilan : E = m·c² ; 1 u = 1,66·10⁻²⁷ kg = 931,5 MeV/c² ; 1 MeV = 1,6·10⁻¹³ J.
- Δm = Z·m_p + (A − Z)·m_n − m(ᴬ_Z X) ; E_ℓ = Δm·c² ; stabilité : E_ℓ/A.
- Réaction : ΔE = Δm·c² = ΣE_ℓ(réactifs) − ΣE_ℓ(produits) ; E_lib = |ΔE| ; échantillon : E = N·E_lib.


## Dessins (gardés, déjà justes)

| Diapositive | Dessin |
|---|---|
| en_l2_former | Séparer ou former le noyau (E_ℓ = Δm·c²) |
| en_a2b_fission | La courbe d'Aston (creux vers le fer, bornes 20 et 190, flèches fusion / fission) |
| en_e1_diagramme | Diagramme énergétique de la fusion (10,841 ; 28,296 ; ΔE = −17,455 MeV) |
| en_r3b_applications_dangers | Pouvoir de pénétration (papier, aluminium, plomb / béton) |

Pas de nouveau dessin : les autres notions sont des formules et des calculs (règle « un dessin là où la notion se
dessine »). Valeurs recalculées en Python : Δm(¹⁴C) = 0,11301 u ; 0,03038 × 931,5 = 28,30 MeV ; 1783,5/235 = 7,59 ;
492,2/56 = 8,79 ; 8,475/3 = 2,825 ; 2,366/2 = 1,183 ; 0,01889 × 931,5 = 17,6 ; 0,19834 × 931,5 = 184,8 ;
0,00303 × 931,5 = 2,82 ; N(1 g ²³⁵U) = 2,56·10²¹ ; E = 7,6·10¹⁰ J ; |Δm|(¹⁰⁷Cd) × 931,49 = 0,402 MeV ;
222 × 7,69 − 218 × 7,73 − 4 × 7,07 = −6,24 MeV.

## Ce qui a été corrigé par rapport au cahier d'avant

- Pas de numérotation, pas d'étiquettes Définition / Méthode / Attention : ajoutées ; définitions de l'u, du défaut de
  masse, de l'énergie de liaison, de la fission et de la fusion écrites mot pour mot.
- Copie en attente : ses blocs gardaient l'ordre de l'ancien cours (rappel du noyau, dangers) ; ils suivent maintenant
  leurs diapositives ; la figure « pénétration » suit sa diapositive dans le bloc `en_s4_b2`.
- Méthodes en étapes : E = Δm·c² (u → MeV, kg → J), Δm, le plus stable, A et Z, énergie libérée par les masses,
  diagramme / énergies de liaison, échantillon ; pièges 2017 R (l'électron compte), 2019 N (× A), neutron oublié.
- Bulles raccourcies à une ou deux lignes (le bilan et la carte faisaient un paragraphe).

## Ce qui reste

- Les définitions longues (défaut de masse, énergie de liaison, fission, fusion) dépassent 90 caractères : gardées
  entières, mot pour mot.
- Le bloc en ligne `en_s2_b3` (fission, chaîne, pénétration, dangers + figure) est le plus chargé (≈ 580 caractères) :
  l'exemple de l'équation de fission y reste dans la bulle de sa diapositive et dans le bloc de la fusion (méthode A et Z).

