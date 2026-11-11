# Noyaux, masse et énergie : ce que disent les examens nationaux (2e Bac PC BIOF, 2016 à 2025)

Source : backend/data/exams/physique/*/exam.json et extraction.json, schémas vus dans assets/ ; 20 sessions. Seuls 2023-R, 2024-N et 2024-R ont la grille officielle (barème et « référence dans le cadre de référence ») ; les autres corrigés sont des corrigés de professeurs. Les points viennent des marges des sujets.

## 0. Vue d'ensemble

- 15 sessions sur 20 ont un exercice de physique nucléaire (2 à 3 points). Il est seul (2,5 pts) ou partage un exercice avec les ondes (2017-R, 2019-N, 2022-N, 2022-R).
- Aucun exercice nucléaire en 2017-N, 2018-N, 2019-R, 2023-R et 2025-R (vérifié : la somme des points des 4 exercices fait 20 et aucun mot-clé nucléaire dans le texte extrait).
- **12 sessions sur 20** (12 sur les 15 exercices nucléaires) ont au moins une question de « Noyaux, masse et énergie ». Les 3 autres (2021-N, 2021-R, 2024-N) sont 100 % décroissance radioactive.
- Poids : 0,5 à 2 pts par session (environ 1 en moyenne) ; depuis 2020, presque toujours **une question à 0,5 pt** (E_lib ou E_ℓ), parfois un QCM en plus.
- Enchaînement type : composition ou équation (Soddy), puis **énergie** (E_lib, E_ℓ, stabilité), puis **décroissance** (λ, t½, a(t), N(t)). En 2023-N et 2025-N, l'énergie vient à la fin.
- **Ni fission de l'uranium 235, ni courbe d'Aston, ni puissance ou rendement de centrale, ni comparaison avec une combustion** sur 2016-2025 (la fission figure une fois dans un QCM, en 2023-N). La fusion D-T tombe deux fois (2016-N, 2023-N).

## 1. Session par session

N = normale, R = rattrapage ; « Décr. » = partie décroissance.

| Session | Exercice (noyaux, réaction) | Questions du chapitre, données exactes | Pts | Réponse attendue |
|---|---|---|---|---|
| 2016-N | Ex II (3 pts) Fusion ²H + ³H → ᴬ_ZHe + ¹n | Q1 trouver A, Z (Soddy) 0,5. **Q2 calculer en MeV E_lib** : m(²H)=2,01355 u ; m(³H)=3,01550 u ; m(He)=4,00150 u ; m(n)=1,00866 u ; 1 u = 931,5 MeV.c⁻² ; 1 MeV = 1,6.10⁻¹³ J ; c = 3.10⁸ m.s⁻¹ ; h = 6,626.10⁻³⁴ J.s. **Q3** toute E_lib devient rayonnement : longueur d'onde λ | 1 + 0,75 (+0,5) | A=4, Z=2. E_lib = abs((m(He)+m(n)−m(²H)−m(³H))·c²) = 1,889.10⁻² × 931,5 ≈ **17,6 MeV**. λ = h·c/E_lib = 6,626.10⁻³⁴×3.10⁸/(17,6×1,6.10⁻¹³) ≈ **7,1.10⁻¹⁴ m** |
| | Décr. | Q4 a₀=2,0.10⁶ Bq, a₁=1,6.10⁶ Bq à 4 ans, trouver a₂ à 12,4 ans (0,75) | | a₂ ≈ 1,0.10⁶ Bq |
| 2016-R | Ex II (2,5) ²⁴Na → ²⁴Mg + X (β⁻) | **Q2 E_lib en MeV** ; **Q3 énergie de liaison par nucléon ℰ du ²⁴Mg en J/nucléon** ; **Q4 diagramme** : ²⁴Mg* à 1,37 MeV, ²⁴Mg à 0, flèche pointillée vers le bas : fréquence ν. Données : m(Na)=23,98493 u ; m(Mg)=23,97846 u ; m(e)=0,00055 u ; m_p=1,00728 u ; m_n=1,00866 u ; 931,5 MeV.c⁻² ; 1 MeV=1,6.10⁻¹³ J ; h=6,62.10⁻³⁴ | 0,5 + 0,75 + 0,75 | E_lib = 5,92.10⁻³×931,5 ≈ **5,51 MeV** (électron compté). ℰ = (12m_p+12m_n−m(Mg))c²/24 = 0,21282×931,5/24 ≈ 8,26 MeV/nucléon ≈ **1,32.10⁻¹² J/nucléon**. ν = E/h = 1,37×1,6.10⁻¹³/6,62.10⁻³⁴ ≈ **3,31.10²⁰ Hz** |
| | Décr. | Q1 identifier X, type β⁻ | | |
| 2017-R | Ex II partie 2 (1,5) ⁶⁰Co → ⁶⁰Ni + X | **2.2 E_lib en MeV** ; **2.3 ℓ (E_ℓ/A) du ⁶⁰Ni en MeV/nucléon, puis lequel de ⁶⁰Ni et ⁵⁶Ni est le plus stable**. Données : m(Co)=59,91901 u ; m(Ni)=59,91543 u ; m(e)=0,00055 u ; m_p=1,00728 ; m_n=1,00866 ; E_ℓ/A(⁵⁶Ni)=8,64 MeV/nucléon ; 931,5 | 0,5 + 1 | Δm = −3,03.10⁻³ u, E_lib ≈ **2,82 MeV**. ℓ = (28m_p+32m_n−m)c²/60 = 0,56553×931,5/60 ≈ **8,78 MeV/nucléon** > 8,64, donc **⁶⁰Ni plus stable** |
| | Décr. | 2.1 X = électron, β⁻ | | |
| 2018-R | Ex 2 (2,5) ²⁴¹Pu → ²⁴¹Am + X | **Q2 E_lib quand un seul noyau se désintègre**. m(Am)=241,00471 u ; m(Pu)=241,00529 u ; m(X)=0,00055 u ; 931,5 | 1 | Δm = −3.10⁻⁵ u, E_lib ≈ **0,028 MeV** |
| | Décr. | Q1 équation β⁻ ; Q3 a₀=3.10⁶ Bq, a à t = 2t½ (14,35 ans) | | a₁ = a₀/4 = 7,5.10⁵ Bq |
| 2019-N | Ex 2 partie 2 (1,75) ²²²Rn → ²¹⁸Po + ⁴He | Tableau E_ℓ/A (MeV/nucléon) : He 7,07 ; Rn 7,69 ; Po 7,73. **2.1 lequel de Rn, Po est le plus stable** ; **2.2 montrer E_ℓ(He)=28,28 MeV** ; **2.3 QCM E_lib** : 7,11 / 22,56 / 6,24 / 3420,6 MeV | 0,5 ×3 | Po (7,73 > 7,69). E_ℓ = A·ξ = 4×7,07. E_lib = abs(E_ℓ(Rn) − [E_ℓ(Po)+E_ℓ(He)]) = abs(1707,18 − 1713,42) = **6,24 MeV** |
| | Décr. | 2.4 t pour a = a₀/4 : 2t½ = 7,6 jours (0,25) | | |
| 2020-N | Ex III (2,5) ²¹⁰Po → ᴬ_ZPb + α | **Diagramme d'énergie** (MeV) : 126 n + 84 p à 1,971820.10⁵ ; ²¹⁰Po à 1,955372.10⁵ ; Pb + ⁴He à 1,955318.10⁵. **2.1 E_lib** ; **2.2 défaut de masse Δm du ²¹⁰Po en kg**. 1 u = 931,41 MeV/c² ; 1 u = 1,66.10⁻²⁷ kg | 0,5 + 0,5 | E_lib = abs(E_f − E_i) = **5,4 MeV**. E_ℓ = 1,971820.10⁵ − 1,955372.10⁵ = 1644,8 MeV, Δm = E_ℓ/c² = 1,766 u = **2,93.10⁻²⁷ kg** |
| | Décr. | Q1 A=206, Z=82 ; Q3 λ en s⁻¹ (t½=138 j) ; Q4 t₁ pour a₁=3,7.10⁴ Bq (≈3198 j) | | |
| 2020-R | Ex 3 (2,5) ²³⁴U → ²³⁰Th + α | **Q2 E_ℓ du ²³⁴U en MeV**. m(U)=234,04095 u ; m_p=1,00728 ; m_n=1,00866 ; 931,5 | 0,5 | E_ℓ = (92m_p+142m_n−m)c² = 1,8585×931,5 ≈ **1731,2 MeV** |
| | Décr. | Q1 composition 92 p, 142 n ; Q3 équation α ; Q4 N(Th) = N₀(1−e^(−λt)), r = e^(λt) − 1 | | |
| 2021-N | Ex 3 (2,5) ²³⁸Pu, pacemaker | aucune | 0 | Décr. : équation α, t½ graphique, λ, N₀ = a₀/λ, t_max |
| 2021-R | Ex 3 (2,5) ³²P (β⁻) | aucune | 0 | Décr. : ln N = f(t), λ par la pente, t½, a(t) depuis m₀ (N₀ = m·N_A/M) |
| 2022-N | Ex 2 partie 2 (2,25) ¹³¹I → ¹³¹Xe + β⁻ | **Q « 2 » : calculer en MeV l'énergie libérée abs(ΔE)**. m(I)=130,906125 u ; m(Xe)=130,9050826 u ; m(β⁻)=5,48580.10⁻⁴ u ; 931,5 | 0,5 | ΔE = −4,9442.10⁻⁴ u·c², abs(ΔE) ≈ **0,4606 MeV** |
| | Décr. | équation (Xe), t½ sur la courbe (8 j), N₀ = a₀t½/ln2, t pour 95 % désintégrés | | |
| 2022-R | Ex 2 partie 2 (1,5) ¹⁴C (β⁻), datation | **Q2 E_ℓ du ¹⁴C en MeV**. m(C)=13,99995 u ; m_n=1,00866 ; m_p=1,00728 ; 931,5 | 0,5 | Δm = 6m_p+8m_n−m = 0,11301 u, E_ℓ ≈ **105,27 MeV** |
| | Décr. | QCM composition, QCM équation ; âge du bois (a₁=318, a₀=418 Bq, t½=5730 ans) ≈ 2260 ans | | |
| 2023-N | Ex 2 (2,5) ³H (β⁻) puis fusion ³H + ²H → ⁴He + n | Tableau E_ℓ (MeV) : ²H 2,366 ; ³H 8,475 ; ⁴He 28,296. **1-1 QCM** (bonne réponse E : « Lors d'une réaction de fission nucléaire, de la masse est convertie en énergie » ; distracteur D : masse du noyau = somme des masses des nucléons). **2-1 vrai/faux** a) l'énergie à fournir au ³H pour le dissocier vaut 8,475 MeV ; b) le tritium est plus stable que le deutérium. **2-2 E_lib = abs(ΔE) de la fusion** | 0,5 (QCM) + 0,25 + 0,25 + 0,5 | E vrai. a) Vrai (définition de E_ℓ). b) Vrai : ξ(³H)=2,825 > ξ(²H)=1,183 MeV/nucléon. E_lib = abs(E_ℓ(He) − [E_ℓ(³H)+E_ℓ(²H)]) = **17,455 ≈ 17,5 MeV** |
| | Décr. | 1-2 équation → ³He ; 1-3 t½ = ln2/λ ; 1-4 a quand 90 % désintégrés (m₀ = 2 µg, M = 3 g/mol, N_A) | | |
| 2024-N | Ex 3 (2) ¹⁹²Ir (β⁻, γ) | aucune | 0 | Décr. : composition, équation, N₀ = a₀/λ, N_d |
| 2024-R | Ex 3 (2) famille ²¹²Pb → ²¹²Bi → ²⁰⁸Tl → X, diagramme (A, Z) | **2-2 E_libérée = abs(ΔE) de ²¹²Bi → ²⁰⁸Tl + α**. m(Bi)=211,991286 u ; m(Tl)=207,982019 u ; m(α)=4,002603 u ; 931,5 | 0,5 (méthode 0,25 + résultat 0,25) | Δm = 0,006664 u, abs(ΔE) ≈ **6,21 MeV** |
| | Décr. | 1-1 type β⁻ lu sur le diagramme ; 1-2 X = ²⁰⁸Pb ; 2-1 équation ; 2-3 t½ = t₁ ln2 / ln(N₀/(N₀−N₁)) ≈ 60,5 min | | |
| 2025-N | Ex 2 (2,5) ¹⁰⁷Cd → ¹⁰⁷Ag + ⁰₁e + γ (β⁺) | **1 QCM** (distracteur D : « la cohésion du noyau est d'autant plus forte que son énergie de liaison par nucléon est petite », faux). **3-3 énergie libérée E par l'échantillon entre t₁ = 2t½ et t₂ = 3t½**. m(Cd)=106,88045 u ; m(Ag)=106,87947 u ; m(e)=5,486.10⁻⁴ u ; t½ = 6,93 h ; a₀ = 1,25.10¹² Bq ; 1 u = 931,49 MeV.c⁻² | 0,5 (+QCM 0,5) | E = N_d · abs(Δm·c²), avec N_d = a₀t½/(8 ln2) ≈ 5,62.10¹⁵ et abs(Δm)c² ≈ 0,402 MeV, soit **E ≈ 2,26.10¹⁵ MeV** |
| | Décr. | 2 équation β⁺ ; 3-1 a₂ = a₁/2 ; 3-2 N_d = a₀t½/(8 ln2) | | |

### Sujets représentatifs à reprendre (données complètes dans le tableau ci-dessus)

- **A. Fusion D-T par les masses (2016-N)** : 1) A, Z (0,5) ; 2) E_lib en MeV (1) ; 3) toute l'énergie part en rayonnement électromagnétique, donc λ (0,75). Δm = 5,01016 − 5,02905 = −1,889.10⁻² u, E_lib ≈ 17,6 MeV, λ ≈ 7,1.10⁻¹⁴ m.
- **B. La même fusion par les E_ℓ (2023-N, partie 2)** : vrai/faux « L'énergie qu'il faut fournir à un noyau de tritium au repos pour le dissocier en ses nucléons au repos est de 8,475 MeV » et « Le tritium est plus stable que le deutérium », puis E_lib = abs(ΔE) = 17,455 MeV. C'est le miroir de A (17,6 MeV par une autre route).
- **C. Énergie de liaison et stabilité (2017-R, ⁶⁰Co → ⁶⁰Ni)** : X et type (0,5) ; E_lib (0,5) ; E_ℓ/A du ⁶⁰Ni puis comparaison avec ⁵⁶Ni (1). Variante en J/nucléon : 2016-R (²⁴Mg).
- **D. Diagramme énergétique (2020-N, ²¹⁰Po)** : E_lib lue entre noyau et produits, puis Δm en kg à partir de l'écart entre nucléons séparés et noyau. Variante à deux niveaux γ : 2016-R.
- **E. Énergie d'un échantillon (2025-N, ¹⁰⁷Cd)** : seul passage de 1 à N noyaux, pont avec la décroissance.
- **Fission de l'uranium 235 : aucun sujet sur 2016-2025.** Un exercice de fission du cours devra être construit et présenté comme tel, pas comme « tombé au national ».

## 2. cas_types

Fréquence = nombre de sessions (sur 20) qui posent le cas.

| # | Cas type | Mots-clés de l'énoncé | Méthode | Pts | Fréquence |
|---|---|---|---|---|---|
| 1 | **Énergie libérée par une réaction, à partir des masses** | « Calculer, en MeV, l'énergie libérée E_lib (abs(ΔE), E_libérée) lors de cette désintégration / réaction », « lorsqu'un seul noyau se désintègre » | Équation équilibrée → Δm = Σm(produits) − Σm(réactifs) en u (électron ou positon compris, neutron compris) → ΔE = Δm·c² avec 1 u·c² = 931,5 MeV → E_lib = abs(ΔE) | 0,5 à 1 | **7** (2016-N, 2016-R, 2017-R, 2018-R, 2022-N, 2024-R, 2025-N) |
| 2 | **Énergie de liaison E_ℓ d'un noyau, à partir des masses** | « Calculer, en MeV, l'énergie de liaison E_ℓ du noyau… » | Composition Z, N = A − Z → Δm = Z·m_p + N·m_n − m(noyau) > 0 → E_ℓ = Δm·c² | 0,5 | **2** (2020-R, 2022-R) ; plus Δm à partir de E_ℓ (2020-N) et E_ℓ = A·ξ (2019-N) |
| 3 | **Énergie de liaison par nucléon E_ℓ/A** | « Déterminer, en MeV/nucléon (en J/nucléon), l'énergie de liaison par nucléon ℓ (ℰ) » | E_ℓ ÷ A ; conversion ×1,6.10⁻¹³ si on la demande en J | 0,75 à 1 | **2** (2016-R, 2017-R) ; plus le calcul de ξ dans les vrai/faux de 2023-N |
| 4 | **Comparer la stabilité de deux noyaux** | « Lequel est le plus stable ? Justifier », « Le tritium est plus stable que le deutérium (vrai/faux) », QCM « la cohésion… » | Comparer E_ℓ/A (jamais E_ℓ) : le plus grand E_ℓ/A donne le noyau le plus stable | 0,25 à 0,5 | **4** (2017-R, 2019-N, 2023-N, 2025-N QCM) |
| 5 | **Énergie libérée à partir des énergies de liaison** | tableau d'E_ℓ ou d'E_ℓ/A dans les données ; « Calculer E_lib » ou QCM de 4 valeurs | ΔE = Σ E_ℓ(réactifs) − Σ E_ℓ(produits) ; E_lib = abs(ΔE). Penser à E_ℓ = A·(E_ℓ/A) pour chaque noyau ; un neutron seul a E_ℓ = 0 | 0,5 | **2** (2019-N QCM, 2023-N) |
| 6 | **QCM / vrai-faux de connaissances** | « Choisir l'affirmation juste », « répondre par vrai ou faux en justifiant » | Définitions : défaut de masse (m(noyau) < Σ m nucléons), E_ℓ = énergie à fournir pour séparer le noyau en nucléons au repos, de la masse devient énergie dans une fission, cohésion liée à un E_ℓ/A grand | 0,25 à 0,5 | **2** (2023-N, 2025-N) ; le format QCM devient courant depuis 2019 |
| 7 | **Exploiter un diagramme énergétique** | « À l'aide du diagramme d'énergie représenté ci-contre, calculer… » | Niveaux : nucléons séparés (le plus haut), noyau père, produits. E_lib = abs(E_f − E_i) entre noyau et produits ; E_ℓ = écart entre nucléons séparés et noyau | 0,5 ×2 | **1** (2020-N) ; plus un diagramme de niveaux γ (2016-R) |
| 8 | **Énergie → photon (λ ou ν)** | « toute l'énergie se transforme en rayonnement électromagnétique », « transition vers l'état fondamental » | E = hν = hc/λ, avec E en J (MeV × 1,6.10⁻¹³) | 0,75 | **2** (2016-N, 2016-R) ; rien depuis 2017 |
| 9 | **Énergie libérée par un échantillon (N noyaux)** | « énergie libérée E lors de la désintégration de cet échantillon entre t₁ et t₂ » | N (par N = m·N_A/M, N = a/λ ou N_d de la décroissance) × énergie d'un noyau | 0,5 | **1** (2025-N) |
| 10 | **Défaut de masse en kg** | « défaut de masse Δm… exprimé en kilogramme » | Δm (u) = E_ℓ (MeV)/931,5, puis × 1,66.10⁻²⁷ kg | 0,5 | **1** (2020-N) |
| 11 | **Équation d'une fusion et ses nombres A, Z** | « Déterminer les nombres A et Z » | Lois de Soddy (conservation de A et de Z), comme pour une désintégration | 0,5 | **1** (2016-N) |
| — | Fission, courbe d'Aston, énergie par kg ou par mole, comparaison avec une combustion, puissance, rendement | — | — | — | **0** |

**Les 5 cas les plus fréquents** : E_lib par les masses (7) ; stabilité par E_ℓ/A (4) ; E_ℓ ou E_ℓ/A par les masses (4) ; E_lib par les E_ℓ (2) ; QCM ou vrai/faux de définitions (2).

## 3. erreurs_examen (où se perdent les points, et le geste qui corrige)

| Erreur | Où elle coûte | Geste qui corrige |
|---|---|---|
| **Signe de ΔE** : l'élève donne E_lib = −17,6 MeV, ou calcule réactifs − produits puis ne sait plus quoi faire du signe | Cas 1 et 5, chaque année | Toujours écrire les deux lignes : « ΔE = (Σm produits − Σm réactifs)·c² < 0 » puis « E_lib = abs(ΔE) = … > 0 ». Le corrigé officiel 2024-R note « Méthode » (0,25) puis « abs(ΔE) ≈ 6,21 MeV » (0,25) |
| **Oubli de l'électron (β⁻) ou du positon (β⁺)** dans Δm alors que sa masse est donnée | 2016-R, 2017-R, 2018-R, 2022-N, 2025-N | Chaque particule de l'équation entre dans Δm. En 2018-R, l'oublier donne 0,54 MeV au lieu de 0,028 MeV |
| **Oubli du neutron** dans une fusion (ou des neutrons d'une fission) | 2016-N | Compter les particules de l'équation avant d'écrire Δm. Pour une fission, il faut le neutron incident à gauche et les k neutrons à droite (le cours devra l'enseigner même si le national ne l'a pas posé) |
| **Conversion u → MeV** : Δm laissé en u, ou ×9.10¹⁶ avec des u | Tous les calculs | Écrire « 1 u·c² = 931,5 MeV », puis Δm (u) × 931,5 |
| **MeV → J** : × 1,6.10⁻¹³ (et non 1,6.10⁻¹⁹), ou conversion oubliée avant E = hν | 2016-N, 2016-R | 1 eV = 1,6.10⁻¹⁹ J, donc 1 MeV = 1,6.10⁻¹³ J. Dans hν ou hc/λ, l'énergie doit être en J |
| **E_ℓ au lieu de E_ℓ/A** pour la stabilité (dire que ⁴He est moins stable que ²³⁴U parce que 28 MeV < 1731 MeV) | 2017-R, 2019-N, 2023-N | Phrase-clé : « le noyau le plus stable est celui qui a la plus grande énergie de liaison par nucléon ». Le QCM 2025-N D piège justement là-dessus (« d'autant plus forte que… petite » : faux) |
| **Composition fausse** (N = A au lieu de A − Z) | Cas 2 et 3 | Écrire « Z = …, N = A − Z = … » avant Δm |
| **Signe du défaut de masse** : Δm = m(noyau) − Σm nucléons < 0 | Cas 2 | Le défaut de masse est positif : Δm = Z·m_p + N·m_n − m(noyau) > 0, et E_ℓ = Δm·c² > 0 |
| **Bilan par les E_ℓ à l'envers** (ΔE = E_ℓ(produits) − E_ℓ(réactifs)) | 2019-N, 2023-N | ΔE = E_ℓ(réactifs) − E_ℓ(produits) ; on rend abs(ΔE). Un nucléon libre a E_ℓ = 0 |
| **E_ℓ = A·ξ oublié** : l'élève soustrait directement les ξ (7,69 − 7,73 − 7,07) | 2019-N (le QCM contient le résultat piège 7,11 MeV, qui vient de ce mélange de ξ) | Multiplier chaque ξ par son A avant de faire le bilan |
| **Lecture de diagramme** : mauvais couple de niveaux | 2020-N | Nommer les niveaux : E_ℓ = nucléons séparés − noyau ; E_lib = noyau père − produits ; garder tous les chiffres (10⁵ MeV) |
| **Énergie d'un échantillon** : donner l'énergie d'un seul noyau, ou se tromper dans N = m·N_A/M (m en g, M en g/mol) | 2025-N (et N = m·N_A/M en décroissance : 2021-R, 2023-N) | E_totale = N × E_lib(1 noyau). Pour N, vérifier que m est en g quand M est en g/mol (2 µg = 2.10⁻⁶ g) |
| **Unité oubliée ou non demandée** (MeV au lieu de MeV/nucléon, J au lieu de MeV) ; valeur de 1 u d'un autre sujet (931,41 en 2020-N, 931,49 en 2025-N) | partout | Recopier l'unité imposée par l'énoncé (« /nucléon » compris) et prendre les constantes du jour. Δm en kg : passer par l'u (E/931,5 puis ×1,66.10⁻²⁷), pas par c² = 9.10¹⁶ |

## 4. Écritures et notations des énoncés officiels

- **Énergie libérée** : E_lib (2016 à 2020), puis « l'énergie libérée |ΔE| » (2022-N), puis **E_libérée = |ΔE|** (2023-N, 2024-R) ; « l'énergie libérée E » pour un échantillon (2025-N). Elle est **toujours positive** (valeur absolue). Dans les tableaux de ce fichier, abs(ΔE) note |ΔE|.
- **ΔE** = Δm·c², avec Δm = Σm(produits) − Σm(réactifs) : ΔE est **négatif** quand la réaction libère de l'énergie (corrigés : « ΔE = −4,9442.10⁻⁴ u·c² », « ΔE = E_f − E_i = −5,4 MeV »). Référence officielle (grille 2024-R) : « Calculer l'énergie libérée (produite) par une réaction nucléaire : E_libérée = |ΔE| ».
- **E_ℓ** : énergie de liaison, définie comme l'énergie à fournir à un noyau au repos pour le séparer en nucléons au repos (2023-N). **E_ℓ/A** n'a pas de symbole fixe : ℰ (2016-R), ℓ (2017-R), ξ (corrigés 2019-N, 2023-N), ou en-tête « Énergie de liaison par nucléon (MeV/nucléon) ». **Δm** (défaut de masse) est positif (2020-N).
- **Masses** : masses de **noyaux** en u (5 à 7 décimales), écrites m(ᴬ_ZX) = … u. On trouve m_p = 1,00728 u, m_n = 1,00866 u, m(e) = 0,00055 u ou 5,486.10⁻⁴ u, m(α) = 4,002603 u. Jamais de masses atomiques, donc jamais de correction par les électrons du cortège.
- **Constantes** : 1 u = 931,5 MeV.c⁻² (aussi MeV/c², 931,41, 931,49) ; 1 MeV = 1,6.10⁻¹³ J ; 1 u = 1,66.10⁻²⁷ kg ; c = 3.10⁸ m.s⁻¹ ; h = 6,626.10⁻³⁴ J.s ; N_A = 6,02.10²³ mol⁻¹ (seulement en décroissance).
- **Équations** : ¹₀n, ⁰₋₁e, ⁰₁e, α écrit ⁴₂He, γ ajouté en fin d'équation (2024-N, 2025-N) ; les corrigés citent les « lois de Soddy ».
- **Diagramme énergétique (2020-N)** : axe vertical E (MeV), trois paliers étiquetés à droite (« 126n + 84p », « ²¹⁰₈₄Po », « ᴬ_ZPb + ⁴₂He ») et les valeurs à gauche (1,971820.10⁵…), **sans flèches**. En 2016-R : deux niveaux γ et une flèche pointillée descendante. Le diagramme (A, Z) de 2024-R (flèches (1), (2), (3)) sert la radioactivité.
- **Formulations** : « Calculer, en MeV, … » ; « Déterminer, en MeV/nucléon, … puis déduire lequel est le plus stable » ; « Montrer que … E_ℓ = 28,28 MeV » ; « Choisir la réponse juste » ; « répondre par vrai ou faux en justifiant ».

## 5. Ce que le cadre de référence semble exiger, et ce qui ne tombe jamais

Exigé d'après les sujets (et la référence officielle citée dans la grille 2024-R) :
1. **Défaut de masse** : m(noyau) < Σ m(nucléons) (QCM 2023-N D).
2. E = m·c², énergie en MeV avec 1 u = 931,5 MeV/c², conversions MeV ↔ J et u ↔ kg.
3. Définir et calculer l'**énergie de liaison** E_ℓ = Δm·c² et l'**énergie de liaison par nucléon** E_ℓ/A ; les utiliser pour **comparer la stabilité** de noyaux.
4. **Calculer l'énergie libérée (produite) par une réaction nucléaire : E_libérée = abs(ΔE)**, par les masses (cas dominant) ou par les énergies de liaison.
5. Exploiter un **diagramme énergétique** (nucléons séparés, noyau, produits).
6. Passer d'un noyau à un échantillon (N noyaux), en le reliant à la décroissance (2025-N).
7. Savoir, au niveau d'une affirmation, que fission et fusion transforment de la masse en énergie (QCM 2023-N), et reconnaître une fusion (2016-N, 2023-N).

Ne tombe jamais sur 2016-2025 (à traiter dans le cours comme culture et entraînement, sans en faire le cœur) :
- un **exercice de fission** (²³⁵U + n → … + k n), ni E_lib de fission, ni réaction en chaîne ;
- la **courbe d'Aston** (−E_ℓ/A = f(A)) : zones de fission et de fusion ;
- l'**énergie par kg ou par mole**, la comparaison avec une combustion ;
- la **puissance** et le **rendement** d'une centrale, la masse consommée par jour ;
- les masses atomiques (correction des électrons), l'énergie cinétique des particules.

Conséquence pour le cours : trois gestes reviennent chaque année. (a) Δm en u, ×931,5, abs(ΔE) en MeV, avec toutes les particules de l'équation. (b) E_ℓ = (Z·m_p + N·m_n − m)·c², puis ÷A. (c) Comparer les E_ℓ/A. S'y ajoutent la lecture d'un diagramme énergétique et le passage à N noyaux. Fission et courbe d'Aston restent au programme du cours, mais aucun national récent ne les évalue par le calcul.
