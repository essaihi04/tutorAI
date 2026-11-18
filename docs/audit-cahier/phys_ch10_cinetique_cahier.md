# Cahier de l'élève — Suivi temporel d'une transformation chimique, vitesse de réaction (phys_ch10)

18 novembre 2026. Le cahier idéal du chapitre, d'un seul tenant, dans l'ordre de la copie en attente (l'architecture revue). Les titres de partie sont ceux que l'écran affiche déjà (`activities[].title`) : ils ne sont pas répétés dans `blocs[].cahier`. Script : `cahier_ch10.py` (scratchpad de la session), qui écrit les deux JSON et ce fichier.

Exemple A : H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l), V = 100 mL, suivi par titrage. Exemple B : CH₃COOC₂H₅(aq) + HO⁻(aq) → CH₃COO⁻(aq) + C₂H₅OH(aq), suivi par conductimétrie. Exemple C : Mg(s) + 2H⁺(aq) → Mg²⁺(aq) + H₂(g), suivi par la pression.

## Ouverture

*(ci_r_b1 — Ouverture ; compter en moles)*

- Introduction — Suivi temporel : on mesure une grandeur à des dates, on en déduit x(t).
- Méthode chimique : titrage d'un prélèvement (après trempe) ; on dose une espèce formée.
- Méthodes physiques : conductivité σ (conductimétrie), pression P ou volume d'un gaz.
- Rappels — La mole : 1 mol = 6,02·10²³ entités ; 1 mmol = 10⁻³ mol.
- Quantité de matière : n = m/M (m en g, M en g/mol) ; liquide : m = ρ·V, donc n = ρ·V/M.

*(ci_r_b2 — Rappels : concentration, ion, couples, équation)*

- Concentration : C = n/V (mol/L) ; n = C·V. Exemple : 2,0 mmol dans 0,100 L → 20 mmol/L.
- Ion : atome qui a perdu (Na⁺) ou gagné (Cl⁻) des électrons ; H⁺ est un proton seul.
- Exemple A — couples : H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l) ; 2I⁻(aq) ⇌ I₂(aq) + 2e⁻.
- Équation (2 e⁻ cédés, 2 captés) : H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l).
- Les coefficients donnent les proportions : 1 H₂O₂ réagit avec 2 I⁻ et donne 1 I₂.

## I. Le tableau d'avancement

*(ci_s1_b2 — Le tableau d’avancement, ligne par ligne ; x_max et le réactif limitant)*

- 1. Définition : avancement x = nombre de fois que la « recette » de l'équation a été faite.
- État initial (x = 0) : H₂O₂ 2,0 | I⁻ 10,0 | I₂ 0 (H⁺ en excès).
- En cours (x) : H₂O₂ 2,0 − x | I⁻ 10,0 − 2x | I₂ x (les I⁻ partent deux par deux).
- 2. x_max : 2,0 − x_max = 0 → 2,0 (H₂O₂) ; 10,0 − 2x_max = 0 → 5,0 (I⁻).
- On garde la plus petite : x_max = 2,0 mmol ; H₂O₂ est le réactif limitant.

Tableau d'avancement modèle (exemple A, en mmol) :

| État | Avancement | H₂O₂(aq) | 2 I⁻(aq) | 2 H⁺(aq) | I₂(aq) | 2 H₂O(l) |
|---|---|---|---|---|---|---|
| initial | 0 | 2,0 | 10,0 | excès | 0 | excès |
| en cours | x | 2,0 − x | 10,0 − 2x | excès | x | excès |
| final | x_f = x_max = 2,0 | 0 | 6,0 | excès | 2,0 | excès |


## II. Mesurer x à une date : trempe et titrage

*(ci_s1_b1 — La trempe ; le titrage du diiode)*

- 1. Trempe : prélèvement versé dans l'eau glacée pour bloquer la réaction avant le dosage.
- Rappel : refroidir et diluer ralentit (température, concentration : facteurs cinétiques).
- 2. Titrage de I₂ par S₂O₃²⁻ : I₂(aq) + 2S₂O₃²⁻(aq) → 2I⁻(aq) + S₄O₆²⁻(aq).
- Définition — équivalence : réactifs du titrage dans les proportions stœchiométriques.
- n(I₂)/1 = n_E(S₂O₃²⁻)/2 avec n_E = C·V_E, donc n(I₂) = C·V_E/2 (dans le prélèvement).
- **Dessin : Le montage du titrage** — La burette verse les ions thiosulfate dans le prélèvement : le brun (bleu avec l'amidon) disparaît à l'équivalence, on lit V_E.

*(ci_s1_b2b — n(I₂) = x : l’avancement à chaque date)*

- 3. Lien avec x : colonne I₂ du tableau : n(I₂) = x (I₂ absent au départ, coefficient 1).
- Exemple (8 min) : n(I₂) = 0,020 × 12,6·10⁻³/2 = 1,26·10⁻⁴ mol dans 10,0 mL prélevés.
- Mélange de 100 mL = 10 prélèvements : n(I₂) = 1,26·10⁻³ mol, donc x(8 min) = 1,26 mmol.
- Attention : V_E en L, puis multiplier par V(mélange)/V(prélèvement) = 10.
- Mesures (trempe + titrage) — t (min) : 0 · 2 · 4 · 6 · 8 · 10 · 15 · 20 · 30 · 40
- x (mmol) : 0 · 0,44 · 0,79 · 1,06 · 1,26 · 1,43 · 1,69 · 1,84 · 1,95 · 1,99

## III. La courbe x(t)

*(ci_s1_b3 — La courbe x(t) : tracer, lire, palier)*

- Tracé : t en abscisse, x en ordonnée ; on place les points mesurés, puis une courbe lisse.
- Lire x : t sur l'axe → verticale jusqu'à la courbe → horizontale jusqu'à l'axe des x.
- Composition à 8 min : H₂O₂ 2,0 − 1,26 = 0,74 ; I⁻ 10,0 − 2,52 = 7,48 ; I₂ 1,26 mmol.
- Palier : x ne change plus, état final ; x_f = 2,0 mmol = x_max : transformation totale.
- Remarque : x croît vite au début, puis de moins en moins vite.
- **Dessin : La courbe x(t) et son palier** — x monte vite puis de moins en moins vite ; sur le palier x = x_f = x_max = 2,0 mmol : transformation totale.

## IV. Suivi par conductimétrie

*(ci_s2_b1 — Conductance, conductivité, ions)*

- 1. Conductance G = k·σ (G en S ; k : constante de cellule, en m ; σ : conductivité, en S/m).
- 2. σ = Σ λᵢ·[Xᵢ] (λ en S·m²·mol⁻¹, [X] en mol/m³) : plus il y a d'ions, plus σ est grande.
- Attention : 1 mol/L = 10³ mol/m³ ; soude : σ₀ = (5,01 + 19,9)·10⁻³ × 10 = 0,249 S/m.
- Exemple B : CH₃COOC₂H₅(aq) + HO⁻(aq) → CH₃COO⁻(aq) + C₂H₅OH(aq) ; Na⁺ spectateur.
- σ diminue : HO⁻ (λ grand) remplacé par CH₃COO⁻ (λ petit) ; σ₀ = 0,249 → σ_f = 0,091 S/m.

*(ci_s2_b1b — Exemple B : établir σ(x))*

- 3. Exemple B : n₀(HO⁻) = 1,0·10⁻² × 0,100 = 1,0 mmol ; ester en excès : x_max = 1,0 mmol.
- En cours : [Na⁺] = n₀/V ; [HO⁻] = (n₀ − x)/V ; [CH₃COO⁻] = x/V.
- σ = σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V (V en m³) : σ est une fonction affine de x.
- État final : σ_f = (λ(Na⁺) + λ(CH₃COO⁻))·n₀/V = (5,01 + 4,09)·10⁻³ × 10 = 0,091 S/m.
- On divise σ₀ − σ par σ₀ − σ_f : x = x_max·(σ₀ − σ)/(σ₀ − σ_f).
- **Dessin : σ en fonction de x : une droite** — σ descend en ligne droite de σ₀ = 0,249 S/m (x = 0) à σ_f = 0,091 S/m (x_max = 1,0 mmol).

*(ci_s2_b1c — De σ(t) à x ; le national 2016 R)*

- 4. Méthode : 1) lire σ sur σ(t) ; 2) σ en S/m ; 3) x = x_max·(σ₀ − σ)/(σ₀ − σ_f).
- Exemple : à 10 min, σ = 0,170 S/m : x = 1,0 × (0,249 − 0,170)/(0,249 − 0,091) = 0,50 mmol.
- National 2016 R : relation donnée x = −6,3·10⁻³·σ + 1,57·10⁻³ (σ en S·m⁻¹, x en mol).
- x = x_max/2 = 5·10⁻⁴ mol → σ = (1,57·10⁻³ − 5·10⁻⁴)/(6,3·10⁻³) = 0,170 S·m⁻¹ → t ≈ 17 min.
- Attention : σ est lue en mS·m⁻¹ sur la figure (170 mS·m⁻¹) : la passer en S·m⁻¹.
- **Dessin : De σ(t) à x** — À t = 10 min on lit σ = 0,170 S/m ; x = x_max·(σ₀ − σ)/(σ₀ − σ_f) = 1,0 × 0,079/0,158 = 0,50 mmol.

## V. Suivi par la pression d'un gaz ; choisir sa méthode

*(ci_s2_b2 — De la pression P à l'avancement x)*

- 1. Exemple C : Mg(s) + 2H⁺(aq) → Mg²⁺(aq) + H₂(g) ; ballon fermé et manomètre : P monte.
- Rappel : gaz parfait P·V = n·R·T (P en Pa, V en m³, n en mol, T en K ; R = 8,31 SI).
- P = P₀ + P(H₂) et n(H₂) = x : x = (P − P₀)·V/(R·T) = x_max·(P − P₀)/(P_max − P₀).
- Attention : P en Pa (1 kPa = 10³ Pa), V (volume du gaz) en m³, T en K.
- 2. Volume de H₂ recueilli : x = n(H₂) = V(H₂)/V_m (V_m = 24 L/mol) ; 24 mL → x = 1,0 mmol.

*(ci_s2_b3 — Choisir sa méthode ; le national 2024 N)*

- 3. Choisir : espèce dosable → titrage ; ions qui changent → conductimétrie ; gaz → P ou V.
- Méthodes physiques : en continu, sans prélèvement ; titrage : prélèvements et trempe.
- Rédaction : « la conductivité des réactifs et celle des produits sont très différentes ».
- Attention : 2024 N, t en heures ; x_f ≈ 0,5 mmol ; x(48 h) ≈ 0,38 mmol : pas finie.

## VI. Vitesse volumique de réaction

*(ci_s3_b1 — La pente, la tangente, la vitesse volumique)*

- Observation : x augmente de moins en moins vite (courbe raide au début, plate à la fin).
- Rappel : pente = Δx/Δt ; la tangente en un point a pour pente dx/dt à cette date.
- Définition : v(t) = (1/V)·dx/dt, quantité formée par unité de temps et par unité de volume.
- V : volume du mélange ; v en mol·m⁻³·s⁻¹ (SI, V en m³) ou en mol·L⁻¹·min⁻¹ (V en L).
- Tangente à t = 0 par A (0 ; 0) et B (8 min ; 2,0 mmol) : (dx/dt)₀ = 2,0/8 = 0,25 mmol/min.
- **Dessin : La tangente à t = 0** — Deux points de la tangente : A (0 ; 0) et B (8 min ; 2,0 mmol) → (dx/dt)₀ = 2,0/8 = 0,25 mmol/min.

*(ci_s3_b1b — Le calcul au barème ; v à partir de n(X) ou [X])*

- Méthode : 1) tangente à la date t ; 2) pente par 2 points éloignés ; 3) v = pente/V.
- Exemple : v(0) = (1/0,100) × 0,25 = 2,5 mmol·L⁻¹·min⁻¹ (V = 100 mL = 0,100 L).
- Réactif R (coeff. 1) : n(R) = n₀ − x, donc v = −(1/V)·dn(R)/dt = −d[R]/dt (signe − : v > 0).
- Produit P (coeff. 1) : n(P) = x, donc v = (1/V)·dn(P)/dt = d[P]/dt.
- Exemple : d[H₂O₂]/dt à t = 0 = (0 − 20)/(8 − 0) = −2,5 mmol·L⁻¹·min⁻¹ → v(0) = 2,5.

## VII. Évolution de la vitesse

*(ci_s3_b2 — La vitesse diminue, nulle à la fin ; la température)*

- Tangentes de plus en plus plates : v(0) = 2,5 ; v(8) ≈ 0,92 ; v(20) ≈ 0,21 mmol·L⁻¹·min⁻¹.
- Donc v diminue : les réactifs s'épuisent, moins de chocs efficaces par unité de temps.
- Sur le palier, la tangente est horizontale : v = 0, la transformation est finie.
- Facteurs cinétiques : plus la température ou [réactif]₀ est grande, plus v est grande.
- Exemple : v(0) = 2,5 à 20 °C et 7,5 mmol·L⁻¹·min⁻¹ à 40 °C ; même palier x_f = 2,0 mmol.
- **Dessin : Des tangentes de plus en plus plates** — v(0) = 2,5 ; v(8) ≈ 0,92 ; v(20) ≈ 0,21 mmol·L⁻¹·min⁻¹ : la vitesse volumique diminue.
- **Dessin : Plus concentré, plus vite** — Deux concentrations initiales d'ions iodure : avec C₁ > C₂ la tangente à l'origine est plus raide (v₀,₁ > v₀,₂) ; même palier x_f = 2,0 mmol (H₂O₂ limitant).

## VIII. Temps de demi-réaction

*(ci_s3_b3 — Le temps de demi-réaction)*

- Définition : t₁/₂ est la durée au bout de laquelle x atteint la moitié de sa valeur finale.
- x(t₁/₂) = x_f/2 (x_f = x_max si totale) ; jamais le milieu de l'axe des temps.
- Méthode : 1) x_f (palier) ; 2) x_f/2 sur l'axe des x ; 3) horizontale, verticale → t₁/₂.
- Exemple A : t₁/₂ ≈ 5,5 min à 20 °C ; 1,8 min à 40 °C : t₁/₂ plus petit, plus rapide.
- Attention : à 2·t₁/₂ ce n'est pas fini (fini vers 7 à 10 t₁/₂) ; mesure ≪ t₁/₂.
- **Dessin : Lire t₁/₂** — x_f = 2,0 mmol sur le palier → x_f/2 = 1,0 mmol → horizontale jusqu'à la courbe → verticale : t₁/₂ ≈ 5,5 min.
- **Dessin : Comparer deux t₁/₂** — Même x_f = 2,0 mmol : t₁/₂ ≈ 1,8 min à 40 °C, 5,5 min à 20 °C ; t₁/₂ plus petit : plus rapide.

## IX. Sujets du national

*(ci_s4_b1 — National : vitesse, t₁/₂, courbe de réactif)*

- 2019 R : pente (1,5 − 0,75)/75 = 1,0·10⁻⁵ mol/s ; V = 1,0·10⁻² L : v = 1,0·10⁻³ mol·L⁻¹·s⁻¹.
- 2025 R : « v diminue » est vrai : v = (1/V)·dx/dt et la pente de la tangente diminue.
- 2017 N : x_f/2 de chaque courbe : 0,1 mol → 8 min ; 0,15 mol → 2 min (pas x_max/2).
- 2023 N, courbe de réactif : n_A = n₀ − x ; x_f = 0,9 − 0,3 = 0,6 mol ; à t₁/₂, x = 0,3 mol.
- Donc t₁/₂ se lit à n_A = 0,9 − 0,3 = 0,6 mol (Attention : ni 0,45 ni 0,3 mol) → 3,5 h.
- **Dessin : t₁/₂ sur une courbe de réactif** — n_A = n₀ − x descend vers le palier 0,3 mol ; x_f = 0,6 mol, donc à t₁/₂ : n_A = 0,9 − 0,3 = 0,6 mol → t₁/₂ ≈ 3,5 h (C₂).

*(ci_s4_b2 — National : même x_f, σ(t), G(t), trempe)*

- 2025 N : même x_f = 133 mmol pour 3 courbes : T et catalyseur changent la durée, pas x_f.
- Méthode (relation σ(x) donnée, 2021 N) : σ = 0,25 − 160·x, on dérive : dσ/dt = −160·dx/dt.
- Donc v = −(1/(160·V₀))·dσ/dt = 0,0125/(1,6·10⁻²) = 0,78 mol·m⁻³·min⁻¹ (V₀ en m³).
- 2018 R : x_f/2 = 5·10⁻⁴ mol → G₁/₂ = 1,07·10⁻³/(6,3·10⁻²) = 0,017 S = 17 mS → t₁/₂ ≈ 17 min.
- Attention : G lue en mS mais relation en S ; dσ/dt < 0 mais v > 0.
- 2017 R : trempe = refroidir brusquement pour bloquer la réaction (écrire « bloquer »).

## X. Pièges de rédaction

## XI. Bilan du chapitre

*(ci_s4_b3 — Pièges d'unités, fiche et carte)*

- Méthode (rédiger v) : relation ; pente avec unité ; V converti ; unité demandée.
- Attention : V = 0,100 L (pas 100) : v(0) = 0,25/0,100 = 2,5 mmol·L⁻¹·min⁻¹.
- Attention : 1 L = 10⁻³ m³ ; λ en mS·m²·mol⁻¹ → ×10⁻³ ; σ lue en mS/m → S/m ; [X] en mol/m³.
- Bilan : mesurer → x(t) → v = (1/V)·dx/dt (tangente), v diminue → x(t₁/₂) = x_f/2.
- Facteurs cinétiques (température, concentration) : changent la durée, pas l'état final x_f.

---

## Table de découpage

### Copie en attente

| Bloc | Diapos | Lignes | Figures du bloc |
|---|---|---|---|
| `ci_r_b1` | o1_carte, o2_methodes, z1_mole | 5 (« Introduction — Suivi temporel : on mes… ») | — |
| `ci_r_b2` | z2_concentration, z3_ion, z4b_couples, z4_equation | 5 (« Concentration : C = n/V (mol/L) ; n = … ») | — |
| `ci_s1_b2` | a1_tableau, a1b_en_cours, a2_limitant | 5 (« 1. Définition : avancement x = nombre … ») | — |
| `ci_s1_b1` | m2_trempe, m3_titrage, m3b_calcul | 5 (« 1. Trempe : prélèvement versé dans l'e… ») | Le montage du titrage |
| `ci_s1_b2b` | a3_lien, m3c_calcul, m1_mesures | 6 (« 3. Lien avec x : colonne I₂ du tableau… ») | — |
| `ci_s1_b3` | a4_courbe, a5_lecture, a6_composition, a7_palier | 5 (« Tracé : t en abscisse, x en ordonnée ;… ») | La courbe x(t) et son palier |
| `ci_s2_b1` | g1_cellule, g2_ions, g3_formule, g4_descend | 5 (« 1. Conductance G = k·σ (G en S ; k : c… ») | — |
| `ci_s2_b1b` | g4b_tableau, g5_droite, g5b_rapport | 5 (« 3. Exemple B : n₀(HO⁻) = 1,0·10⁻² × 0,… ») | σ en fonction de x : une droite |
| `ci_s2_b1c` | g6_calcul, p4_2016R | 5 (« 4. Méthode : 1) lire σ sur σ(t) ; 2) σ… ») | De σ(t) à x |
| `ci_s2_b2` | p1_ballon, z6_gaz, p2_relation, p3_volume | 5 (« 1. Exemple C : Mg(s) + 2H⁺(aq) → Mg²⁺(… ») | — |
| `ci_s2_b3` | p5_choisir, p6_2024N | 4 (« 3. Choisir : espèce dosable → titrage … ») | — |
| `ci_s3_b1` | v1_pente, z5_pente, v2_definition, v3_tangente | 5 (« Observation : x augmente de moins en m… ») | La tangente à t = 0 |
| `ci_s3_b1b` | v4_bareme, v6b_espece | 5 (« Méthode : 1) tangente à la date t ; 2)… ») | — |
| `ci_s3_b2` | v5_diminue, v6_epuisement, v7_nulle, v8_temperature | 5 (« Tangentes de plus en plus plates : v(0… ») | Des tangentes de plus en plus plates ; Plus concentré, plus vite |
| `ci_s3_b3` | h1_definition, h2_lecture, h3_pieges, h4_comparer | 5 (« Définition : t₁/₂ est la durée au bout… ») | Lire t₁/₂ ; Comparer deux t₁/₂ |
| `ci_s4_b1` | n1_aspirine, n2_diminue, n3_deux, n4_reactif | 5 (« 2019 R : pente (1,5 − 0,75)/75 = 1,0·1… ») | t₁/₂ sur une courbe de réactif |
| `ci_s4_b2` | n5_trois, n6_sigma, n7_conductance, n8_trempe | 6 (« 2025 N : même x_f = 133 mmol pour 3 co… ») | — |
| `ci_s4_b3` | r1_litres, r2_unites, bl_fiche, cr_carte | 5 (« Méthode (rédiger v) : relation ; pente… ») | — |

| Diapo → bulle | Figure |
|---|---|
| `ci_o1_carte` : Plan : méthodes de suivi → tableau d'avancement → mesure de x → x(t) → vitesse → t₁/₂. | — |
| `ci_o2_methodes` : Suivi temporel : on mesure une grandeur (quantité titrée, σ, P) à des dates → x(t). | — |
| `ci_z1_mole` : 1 mol = 6,02·10²³ entités ; n = m/M ; liquide : m = ρ·V, donc n = ρ·V/M. Exemple : 36 g d'eau (M = 18 g/mol) → n = 2,0 mol. | — |
| `ci_z2_concentration` : C = n/V (mol/L) ; n = C·V. Exemple : 2,0 mmol dans 0,100 L → C = 20 mmol/L. | — |
| `ci_z3_ion` : Ion : atome qui a perdu ou gagné des électrons : Na⁺, Cl⁻ ; H⁺ = un proton seul. | — |
| `ci_z4b_couples` : H₂O₂/H₂O : H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l) ; I₂/I⁻ : 2I⁻(aq) ⇌ I₂(aq) + 2e⁻. Autant d'électrons cédés que captés : on additionne les deux demi-équations. | — |
| `ci_z4_equation` : H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l) : toujours 2 I⁻ pour 1 H₂O₂. | — |
| `ci_a1_tableau` : Tableau (mmol) — état initial (x = 0) : H₂O₂ 2,0 ; I⁻ 10,0 ; H⁺ excès ; I₂ 0. | — |
| `ci_a1b_en_cours` : Avancement x : nombre de fois que la « recette » de l'équation a été faite. En cours : H₂O₂ 2,0 − x ; I⁻ 10,0 − 2x ; I₂ x ; état final : x = x_f. | — |
| `ci_a2_limitant` : Hypothèses : 2,0 − x_max = 0 → 2,0 mmol ; 10,0 − 2x_max = 0 → 5,0 mmol. On garde la plus petite : x_max = 2,0 mmol ; H₂O₂ est le réactif limitant. | — |
| `ci_m2_trempe` : Trempe : prélèvement versé dans l'eau glacée, refroidi et dilué : la réaction est bloquée. On dose ensuite la quantité présente à cette date. | — |
| `ci_m3_titrage` : Équivalence : réactifs du titrage en proportions stœchiométriques (1 I₂ pour 2 S₂O₃²⁻). Brun → incolore (amidon : bleu → incolore) ; à 8 min, V_E = 12,6 mL. | Le montage du titrage |
| `ci_m3b_calcul` : I₂(aq) + 2S₂O₃²⁻(aq) → 2I⁻(aq) + S₄O₆²⁻(aq) (couples I₂/I⁻ et S₄O₆²⁻/S₂O₃²⁻). À l'équivalence : n(I₂)/1 = n_E(S₂O₃²⁻)/2 = C·V_E/2, donc n(I₂) = C·V_E/2. | — |
| `ci_a3_lien` : Colonne I₂ : 0 au départ, puis x : n(I₂) = x ; on mesure n(I₂) par titrage → on connaît x. | — |
| `ci_m3c_calcul` : 8 min : n(I₂) = 0,020 × 12,6·10⁻³/2 = 1,26·10⁻⁴ mol dans 10 mL ; ×10 → 1,26 mmol. Donc x(8 min) = n(I₂) = 1,26 mmol. | — |
| `ci_m1_mesures` : t (min) : 0 · 2 · 4 · 6 · 8 · 10 · 15 · 20 · 30 · 40 x (mmol) : 0 · 0,44 · 0,79 · 1,06 · 1,26 · 1,43 · 1,69 · 1,84 · 1,95 · 1,99 | — |
| `ci_a4_courbe` : Points (t ; x) des mesures puis courbe lisse : x croît vite, puis de moins en moins vite. | — |
| `ci_a5_lecture` : Lire x : axe des t → verticale jusqu'à la courbe → horizontale jusqu'à l'axe des x. Exemple : x(8 min) ≈ 1,26 mmol. | Lire x à une date |
| `ci_a6_composition` : x(8 min) = 1,26 mmol : n(H₂O₂) = 0,74 mmol ; n(I⁻) = 7,48 mmol ; n(I₂) = 1,26 mmol. | — |
| `ci_a7_palier` : Palier : x ne change plus ; x_f = 2,0 mmol = x_max : la transformation est totale. | La courbe x(t) et son palier |
| `ci_g1_cellule` : Conductimètre : G = k·σ (G en S, k en m, σ en S/m) ; σ vient des ions. Avant les mesures : étalonnage avec une solution étalon. | — |
| `ci_g2_ions` : Plus il y a d'ions, plus σ est grande : si les ions changent pendant la réaction, σ change. | — |
| `ci_g3_formule` : σ = Σ λᵢ·[Xᵢ] (λ en S·m²·mol⁻¹, [X] en mol/m³ ; 1 mol/L = 10³ mol/m³). Soude : σ₀ = 5,01·10⁻³ × 10 + 19,9·10⁻³ × 10 = 0,249 S/m. | — |
| `ci_g4_descend` : Exemple B : CH₃COOC₂H₅(aq) + HO⁻(aq) → CH₃COO⁻(aq) + C₂H₅OH(aq). HO⁻ remplacé par CH₃COO⁻ (λ plus petit) : σ baisse de 0,249 à 0,091 S/m. | — |
| `ci_g4b_tableau` : n₀(HO⁻) = [HO⁻]₀·V = 1,0 mmol ; ester en excès : HO⁻ limitant, x_max = n₀ = 1,0 mmol. En cours : HO⁻ n₀ − x ; CH₃COO⁻ x ; C₂H₅OH x ; Na⁺ n₀ (spectateur). | — |
| `ci_g5_droite` : σ = σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V : droite qui descend de σ₀ à σ_f. | σ en fonction de x : une droite |
| `ci_g5b_rapport` : σ_f = λ(Na⁺)·[Na⁺] + λ(CH₃COO⁻)·[CH₃COO⁻]_f = 0,091 S/m. x = x_max·(σ₀ − σ)/(σ₀ − σ_f) : σ = σ₀ → x = 0 ; σ = σ_f → x = x_max. | — |
| `ci_g6_calcul` : À 10 min : σ = 0,170 S/m ; x = 1,0 × (0,249 − 0,170)/(0,249 − 0,091) = 0,50 mmol. | De σ(t) à x |
| `ci_p4_2016R` : 2016 R : x = −6,3·10⁻³·σ + 1,57·10⁻³ ; x = 5·10⁻⁴ mol → σ = 0,170 S·m⁻¹ → t ≈ 17 min. Attention : σ lue en mS·m⁻¹, à convertir en S·m⁻¹. | — |
| `ci_p1_ballon` : Exemple C : Mg(s) + 2H⁺(aq) → Mg²⁺(aq) + H₂(g) ; couples Mg²⁺/Mg et H⁺/H₂. H₂ reste dans le ballon : P monte de P₀ = 101,3 kPa à 103,8 kPa. | — |
| `ci_z6_gaz` : Pression : chocs des molécules sur la paroi ; P·V = n·R·T (Pa, m³, mol, K ; R = 8,31). | — |
| `ci_p2_relation` : P(H₂) = P − P₀ et n(H₂) = x : x = (P − P₀)·V/(R·T). Fin (totale) : x = x_max·(P − P₀)/(P_max − P₀). | — |
| `ci_p3_volume` : Éprouvette retournée sur l'eau : x = V(H₂)/V_m (V_m = 24 L/mol) ; 24 mL → 1,0 mmol. | — |
| `ci_p5_choisir` : Espèce dosable → titrage après trempe ; ions → conductimétrie ; gaz → pression ou volume. Méthodes physiques : en continu, sans prélèvement ; titrage : prélèvements et trempe. | — |
| `ci_p6_2024N` : 2024 N : t en heures ! x_f ≈ 0,5 mmol ; x(24 h) = 0,25 ; x(48 h) ≈ 0,38 mmol (pas finie). | — |
| `ci_v1_pente` : x augmente au cours du temps, de moins en moins vite : rapide au début, lente à la fin. | — |
| `ci_z5_pente` : Pente = Δx/Δt ; tangente en un point : sa pente est dx/dt à cette date. | — |
| `ci_v2_definition` : v(t) = (1/V)·dx/dt : quantité formée par unité de temps et par unité de volume. Unité SI : mol·m⁻³·s⁻¹ ; en pratique mol·L⁻¹·min⁻¹ (V en L). | — |
| `ci_v3_tangente` : dx/dt = pente de la tangente : A (0 ; 0) et B (8 min ; 2,0 mmol) → (dx/dt)₀ = 0,25 mmol/min. | La tangente à t = 0 |
| `ci_v4_bareme` : v(0) = (1/V)·(dx/dt)₀ = (1/0,100) × 0,25 = 2,5 mmol·L⁻¹·min⁻¹. Attention : V en litres (en m³ pour mol·m⁻³). | — |
| `ci_v6b_espece` : Réactif : v = −d[R]/dt ; produit : v = d[P]/dt (V constant, coefficient 1). [H₂O₂] : pente (0 − 20)/8 = −2,5 mmol·L⁻¹·min⁻¹ → v(0) = 2,5 mmol·L⁻¹·min⁻¹. | — |
| `ci_v5_diminue` : v(0) = 2,5 ; v(8) ≈ 0,92 ; v(20) ≈ 0,21 mmol·L⁻¹·min⁻¹ : la vitesse diminue. Attention : x augmente, mais sa pente diminue : ne pas confondre x et v. | Des tangentes de plus en plus plates |
| `ci_v6_epuisement` : v diminue car les réactifs s'épuisent : moins de chocs efficaces par unité de temps. Facteur cinétique : C₁ > C₂ ⇒ v₀,₁ > v₀,₂ (tangente à l'origine plus raide). | Plus concentré, plus vite |
| `ci_v7_nulle` : Palier : tangente horizontale, v = 0 ; v est maximale à t = 0. | — |
| `ci_v8_temperature` : Plus chaud, plus de chocs efficaces : v(0) = 7,5 au lieu de 2,5 mmol·L⁻¹·min⁻¹. Même état final : x_f = 2,0 mmol. | Plus chaud, plus vite |
| `ci_h1_definition` : t₁/₂ : durée au bout de laquelle l'avancement atteint la moitié de sa valeur finale. x(t₁/₂) = x_f/2 ; exemple A : x(t₁/₂) = 1,0 mmol. | — |
| `ci_h2_lecture` : x_f = 2,0 → x_f/2 = 1,0 mmol → horizontale jusqu'à la courbe → verticale : t₁/₂ ≈ 5,5 min. | Lire t₁/₂ |
| `ci_h3_pieges` : Attention : à 2·t₁/₂ = 11 min, x ≈ 1,5 mmol < x_f : la transformation n'est pas finie. On part de x_f/2 sur l'axe des x, jamais du milieu de l'axe des temps. | — |
| `ci_h4_comparer` : t₁/₂ plus petit = plus rapide : 1,8 min à 40 °C contre 5,5 min à 20 °C. Choix du suivi : une mesure ≪ t₁/₂ ; t₁/₂ court → mesure en continu (σ, P). | Comparer deux t₁/₂ |
| `ci_n1_aspirine` : 2019 R : x_max = 2,8 mmol ; v(100 s) = 1,0·10⁻³ mol·L⁻¹·s⁻¹. x_f/2 = 1,4 mmol → t₁/₂ = 70 s (Attention : t en secondes). | — |
| `ci_n2_diminue` : 2025 R : vrai, v diminue ; v(3 min) = 0,08/0,050 = 1,6 mmol·L⁻¹·min⁻¹. x_f/2 = 0,4 mmol → t₁/₂ = 4 min. | — |
| `ci_n3_deux` : 2017 N : x_f/2 de chaque courbe : (1) 0,1 mol → 8 min ; (2) 0,15 mol → 2 min. (2) est la plus rapide. Attention : x_f/2, pas x_max/2. | — |
| `ci_n4_reactif` : 2023 N : n_A = n₀ − x ; x_f = 0,6 mol ; à t₁/₂, n_A = 0,6 mol → t₁/₂ ≈ 3,5 h. C₁ : même palier atteint plus tôt (catalyseur). | t₁/₂ sur une courbe de réactif |
| `ci_n5_trois` : 2025 N : même x_f = 133 mmol : les facteurs cinétiques changent la durée, pas l'état final. (b) : x_f/2 = 66,5 mmol → t₁/₂ ≈ 90 min. | — |
| `ci_n6_sigma` : 2021 N : σ = 0,25 − 160·x → v = −(1/(160·V₀))·dσ/dt = 0,78 mol·m⁻³·min⁻¹. σ₁/₂ = 0,25 − 160 × 5·10⁻⁴ = 0,17 S·m⁻¹ → t₁/₂ = 4 min. | — |
| `ci_n7_conductance` : 2018 R : G₁/₂ = (1,57·10⁻³ − 5·10⁻⁴)/(6,3·10⁻²) = 0,017 S = 17 mS → t₁/₂ ≈ 17 min. Attention : G lue en mS, relation en S. | — |
| `ci_n8_trempe` : 2017 R : trempe : le refroidissement brusque bloque la réaction ; on dose l'acide restant. Palier n(acide) = 0,2 mol → x_f = 0,6 − 0,2 = 0,4 mol. | — |
| `ci_r1_litres` : V = 100 mL = 0,100 L : v(0) = (1/0,100) × 0,25 = 2,5 mmol·L⁻¹·min⁻¹ = 2,5 mol·m⁻³·min⁻¹. | — |
| `ci_r2_unites` : 10⁻² mol/L = 10 mol/m³ ; 19,9 mS·m²·mol⁻¹ = 19,9·10⁻³ S·m²·mol⁻¹. Attention : σ lue en mS/m → S/m (250 mS/m = 0,250 S/m). | — |
| `ci_bl_fiche` : n(I₂) = C·V_E/2 ; x = x_max·(σ₀ − σ)/(σ₀ − σ_f) ; x = (P − P₀)·V/(R·T). v = (1/V)·dx/dt (tangente, V en L) ; v diminue ; x(t₁/₂) = x_f/2. | — |
| `ci_cr_carte` : Suivre x(t) → méthodes → tableau → x(t) → v(t) (tangente) → v diminue → t₁/₂. | — |

### Cours en ligne

| Bloc | Diapos | Lignes | Figures du bloc |
|---|---|---|---|
| `ci_r_b1` | o1_carte, o2_methodes, z1_mole | 5 (« Introduction — Suivi temporel : on mes… ») | — |
| `ci_r_b2` | z2_concentration, z3_ion, z4b_couples, z4_equation | 5 (« Concentration : C = n/V (mol/L) ; n = … ») | — |
| `ci_s1_b1` | m1_mesures, m2_trempe, m3_titrage | 5 (« Exemple A (V = 100 mL) : le diiode I₂ … ») | Le montage du titrage |
| `ci_s1_b2` | m3b_calcul, m3c_calcul, a1_tableau, a1b_en_cours | 5 (« 3. Équivalence : n(I₂)/1 = n_E(S₂O₃²⁻)… ») | — |
| `ci_s1_b2b` | a2_limitant, a3_lien | 5 (« 2. x_max : 2,0 − x_max = 0 → 2,0 (H₂O₂… ») | — |
| `ci_s1_b3` | a4_courbe, a5_lecture, a6_composition, a7_palier | 6 (« 4. La courbe x(t)… ») | La courbe x(t) et son palier |
| `ci_s2_b1` | g1_cellule, g2_ions, g3_formule, g4_descend | 5 (« 1. Conductance G = k·σ (G en S ; k : c… ») | — |
| `ci_s2_b1b` | g4b_tableau, g5_droite, g5b_rapport, g6_calcul | 6 (« 3. Exemple B : n₀(HO⁻) = 1,0·10⁻² × 0,… ») | σ en fonction de x : une droite ; De σ(t) à x |
| `ci_s2_b2` | p1_ballon, z6_gaz, p2_relation | 4 (« 1. Exemple C : Mg(s) + 2H⁺(aq) → Mg²⁺(… ») | — |
| `ci_s2_b3` | p3_volume, p4_2016R, p5_choisir, p6_2024N | 6 (« 2. Volume de H₂ recueilli : x = n(H₂) … ») | — |
| `ci_s3_b1` | v1_pente, z5_pente, v2_definition, v3_tangente, v4_bareme | 6 (« Observation : x augmente de moins en m… ») | La tangente à t = 0 |
| `ci_s3_b2` | v5_diminue, v6_epuisement, v6b_espece, v7_nulle, v8_temperature | 6 (« Tangentes de plus en plus plates : v(0… ») | Des tangentes de plus en plus plates ; Plus concentré, plus vite |
| `ci_s3_b3` | h1_definition, h2_lecture, h3_pieges, h4_comparer | 5 (« Définition : t₁/₂ est la durée au bout… ») | Lire t₁/₂ ; Comparer deux t₁/₂ |
| `ci_s4_b1` | n1_aspirine, n2_diminue, n3_deux, n4_reactif | 5 (« 2019 R : pente (1,5 − 0,75)/75 = 1,0·1… ») | t₁/₂ sur une courbe de réactif |
| `ci_s4_b2` | n5_trois, n6_sigma, n7_conductance, n8_trempe | 6 (« 2025 N : même x_f = 133 mmol pour 3 co… ») | — |
| `ci_s4_b3` | r1_litres, r2_unites, bl_fiche, cr_carte | 5 (« Méthode (rédiger v) : relation ; pente… ») | — |

| Diapo → bulle | Figure |
|---|---|
| `ci_o1_carte` : Plan : méthodes de suivi → tableau d'avancement → mesure de x → x(t) → vitesse → t₁/₂. | — |
| `ci_o2_methodes` : Suivi temporel : on mesure une grandeur (quantité titrée, σ, P) à des dates → x(t). | — |
| `ci_z1_mole` : 1 mol = 6,02·10²³ entités ; n = m/M ; liquide : m = ρ·V, donc n = ρ·V/M. Exemple : 36 g d'eau (M = 18 g/mol) → n = 2,0 mol. | — |
| `ci_z2_concentration` : C = n/V (mol/L) ; n = C·V. Exemple : 2,0 mmol dans 0,100 L → C = 20 mmol/L. | — |
| `ci_z3_ion` : Ion : atome qui a perdu ou gagné des électrons : Na⁺, Cl⁻ ; H⁺ = un proton seul. | — |
| `ci_z4b_couples` : H₂O₂/H₂O : H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l) ; I₂/I⁻ : 2I⁻(aq) ⇌ I₂(aq) + 2e⁻. Autant d'électrons cédés que captés : on additionne les deux demi-équations. | — |
| `ci_z4_equation` : H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l) : toujours 2 I⁻ pour 1 H₂O₂. | — |
| `ci_m1_mesures` : Exemple A (V = 100 mL) : le diiode I₂ se forme (incolore → brun) ; on le dose à des dates. | — |
| `ci_m2_trempe` : Trempe : prélèvement versé dans l'eau glacée, refroidi et dilué : la réaction est bloquée. On dose ensuite la quantité présente à cette date. | — |
| `ci_m3_titrage` : Équivalence : réactifs du titrage en proportions stœchiométriques (1 I₂ pour 2 S₂O₃²⁻). Brun → incolore (amidon : bleu → incolore) ; à 8 min, V_E = 12,6 mL. | Le montage du titrage |
| `ci_m3b_calcul` : I₂(aq) + 2S₂O₃²⁻(aq) → 2I⁻(aq) + S₄O₆²⁻(aq) (couples I₂/I⁻ et S₄O₆²⁻/S₂O₃²⁻). À l'équivalence : n(I₂)/1 = n_E(S₂O₃²⁻)/2 = C·V_E/2, donc n(I₂) = C·V_E/2. | — |
| `ci_m3c_calcul` : 8 min : n(I₂) = 0,020 × 12,6·10⁻³/2 = 1,26·10⁻⁴ mol dans 10 mL prélevés. Mélange de 100 mL = 10 prélèvements : n(I₂) = 1,26·10⁻³ mol = 1,26 mmol. | — |
| `ci_a1_tableau` : Tableau (mmol) — état initial (x = 0) : H₂O₂ 2,0 ; I⁻ 10,0 ; H⁺ excès ; I₂ 0. | — |
| `ci_a1b_en_cours` : Avancement x : nombre de fois que la « recette » de l'équation a été faite. En cours : H₂O₂ 2,0 − x ; I⁻ 10,0 − 2x ; I₂ x ; état final : x = x_f. | — |
| `ci_a2_limitant` : Hypothèses : 2,0 − x_max = 0 → 2,0 mmol ; 10,0 − 2x_max = 0 → 5,0 mmol. On garde la plus petite : x_max = 2,0 mmol ; H₂O₂ est le réactif limitant. | — |
| `ci_a3_lien` : Colonne I₂ : 0 au départ, puis x : n(I₂) = x ; donc x(8 min) = 1,26 mmol. Mesures : t (min) 0 · 2 · 4 · 8 · 20 · 40 → x (mmol) 0 · 0,44 · 0,79 · 1,26 · 1,84 · 1,99 | — |
| `ci_a4_courbe` : Points (t ; x) des mesures puis courbe lisse : x croît vite, puis de moins en moins vite. | — |
| `ci_a5_lecture` : Lire x : axe des t → verticale jusqu'à la courbe → horizontale jusqu'à l'axe des x. Exemple : x(8 min) ≈ 1,26 mmol. | Lire x à une date |
| `ci_a6_composition` : x(8 min) = 1,26 mmol : n(H₂O₂) = 0,74 mmol ; n(I⁻) = 7,48 mmol ; n(I₂) = 1,26 mmol. | — |
| `ci_a7_palier` : Palier : x ne change plus ; x_f = 2,0 mmol = x_max : la transformation est totale. | La courbe x(t) et son palier |
| `ci_g1_cellule` : Conductimètre : G = k·σ (G en S, k en m, σ en S/m) ; σ vient des ions. Avant les mesures : étalonnage avec une solution étalon. | — |
| `ci_g2_ions` : Plus il y a d'ions, plus σ est grande : si les ions changent pendant la réaction, σ change. | — |
| `ci_g3_formule` : σ = Σ λᵢ·[Xᵢ] (λ en S·m²·mol⁻¹, [X] en mol/m³ ; 1 mol/L = 10³ mol/m³). Soude : σ₀ = 5,01·10⁻³ × 10 + 19,9·10⁻³ × 10 = 0,249 S/m. | — |
| `ci_g4_descend` : Exemple B : CH₃COOC₂H₅(aq) + HO⁻(aq) → CH₃COO⁻(aq) + C₂H₅OH(aq). HO⁻ remplacé par CH₃COO⁻ (λ plus petit) : σ baisse de 0,249 à 0,091 S/m. | — |
| `ci_g4b_tableau` : n₀(HO⁻) = [HO⁻]₀·V = 1,0 mmol ; ester en excès : HO⁻ limitant, x_max = n₀ = 1,0 mmol. En cours : HO⁻ n₀ − x ; CH₃COO⁻ x ; C₂H₅OH x ; Na⁺ n₀ (spectateur). | — |
| `ci_g5_droite` : σ = σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V : droite qui descend de σ₀ à σ_f. | σ en fonction de x : une droite |
| `ci_g5b_rapport` : σ_f = λ(Na⁺)·[Na⁺] + λ(CH₃COO⁻)·[CH₃COO⁻]_f = 0,091 S/m. x = x_max·(σ₀ − σ)/(σ₀ − σ_f) : σ = σ₀ → x = 0 ; σ = σ_f → x = x_max. | — |
| `ci_g6_calcul` : À 10 min : σ = 0,170 S/m ; x = 1,0 × (0,249 − 0,170)/(0,249 − 0,091) = 0,50 mmol. | De σ(t) à x |
| `ci_p1_ballon` : Exemple C : Mg(s) + 2H⁺(aq) → Mg²⁺(aq) + H₂(g) ; couples Mg²⁺/Mg et H⁺/H₂. H₂ reste dans le ballon : P monte de P₀ = 101,3 kPa à 103,8 kPa. | — |
| `ci_z6_gaz` : Pression : chocs des molécules sur la paroi ; P·V = n·R·T (Pa, m³, mol, K ; R = 8,31). | — |
| `ci_p2_relation` : P(H₂) = P − P₀ et n(H₂) = x : x = (P − P₀)·V/(R·T). Fin (totale) : x = x_max·(P − P₀)/(P_max − P₀). | — |
| `ci_p3_volume` : Éprouvette retournée sur l'eau : x = V(H₂)/V_m (V_m = 24 L/mol) ; 24 mL → 1,0 mmol. | — |
| `ci_p4_2016R` : 2016 R : x = −6,3·10⁻³·σ + 1,57·10⁻³ ; x = 5·10⁻⁴ mol → σ = 0,170 S·m⁻¹ → t ≈ 17 min. Attention : σ lue en mS·m⁻¹, à convertir en S·m⁻¹. | — |
| `ci_p5_choisir` : Espèce dosable → titrage après trempe ; ions → conductimétrie ; gaz → pression ou volume. Méthodes physiques : en continu, sans prélèvement ; titrage : prélèvements et trempe. | — |
| `ci_p6_2024N` : 2024 N : t en heures ! x_f ≈ 0,5 mmol ; x(24 h) = 0,25 ; x(48 h) ≈ 0,38 mmol (pas finie). | — |
| `ci_v1_pente` : x augmente au cours du temps, de moins en moins vite : rapide au début, lente à la fin. | — |
| `ci_z5_pente` : Pente = Δx/Δt ; tangente en un point : sa pente est dx/dt à cette date. | — |
| `ci_v2_definition` : v(t) = (1/V)·dx/dt : quantité formée par unité de temps et par unité de volume. Unité SI : mol·m⁻³·s⁻¹ ; en pratique mol·L⁻¹·min⁻¹ (V en L). | — |
| `ci_v3_tangente` : dx/dt = pente de la tangente : A (0 ; 0) et B (8 min ; 2,0 mmol) → (dx/dt)₀ = 0,25 mmol/min. | La tangente à t = 0 |
| `ci_v4_bareme` : v(0) = (1/V)·(dx/dt)₀ = (1/0,100) × 0,25 = 2,5 mmol·L⁻¹·min⁻¹. Attention : V en litres (en m³ pour mol·m⁻³). | — |
| `ci_v5_diminue` : v(0) = 2,5 ; v(8) ≈ 0,92 ; v(20) ≈ 0,21 mmol·L⁻¹·min⁻¹ : la vitesse diminue. Attention : x augmente, mais sa pente diminue : ne pas confondre x et v. | Des tangentes de plus en plus plates |
| `ci_v6_epuisement` : v diminue car les réactifs s'épuisent : moins de chocs efficaces par unité de temps. Facteur cinétique : C₁ > C₂ ⇒ v₀,₁ > v₀,₂ (tangente à l'origine plus raide). | Plus concentré, plus vite |
| `ci_v6b_espece` : Réactif : v = −d[R]/dt ; produit : v = d[P]/dt (V constant, coefficient 1). [H₂O₂] : pente (0 − 20)/8 = −2,5 mmol·L⁻¹·min⁻¹ → v(0) = 2,5 mmol·L⁻¹·min⁻¹. | — |
| `ci_v7_nulle` : Palier : tangente horizontale, v = 0 ; v est maximale à t = 0. | — |
| `ci_v8_temperature` : Plus chaud, plus de chocs efficaces : v(0) = 7,5 au lieu de 2,5 mmol·L⁻¹·min⁻¹. Même état final : x_f = 2,0 mmol. | Plus chaud, plus vite |
| `ci_h1_definition` : t₁/₂ : durée au bout de laquelle l'avancement atteint la moitié de sa valeur finale. x(t₁/₂) = x_f/2 ; exemple A : x(t₁/₂) = 1,0 mmol. | — |
| `ci_h2_lecture` : x_f = 2,0 → x_f/2 = 1,0 mmol → horizontale jusqu'à la courbe → verticale : t₁/₂ ≈ 5,5 min. | Lire t₁/₂ |
| `ci_h3_pieges` : Attention : à 2·t₁/₂ = 11 min, x ≈ 1,5 mmol < x_f : la transformation n'est pas finie. On part de x_f/2 sur l'axe des x, jamais du milieu de l'axe des temps. | — |
| `ci_h4_comparer` : t₁/₂ plus petit = plus rapide : 1,8 min à 40 °C contre 5,5 min à 20 °C. Choix du suivi : une mesure ≪ t₁/₂ ; t₁/₂ court → mesure en continu (σ, P). | Comparer deux t₁/₂ |
| `ci_n1_aspirine` : 2019 R : x_max = 2,8 mmol ; v(100 s) = 1,0·10⁻³ mol·L⁻¹·s⁻¹. x_f/2 = 1,4 mmol → t₁/₂ = 70 s (Attention : t en secondes). | — |
| `ci_n2_diminue` : 2025 R : vrai, v diminue ; v(3 min) = 0,08/0,050 = 1,6 mmol·L⁻¹·min⁻¹. x_f/2 = 0,4 mmol → t₁/₂ = 4 min. | — |
| `ci_n3_deux` : 2017 N : x_f/2 de chaque courbe : (1) 0,1 mol → 8 min ; (2) 0,15 mol → 2 min. (2) est la plus rapide. Attention : x_f/2, pas x_max/2. | — |
| `ci_n4_reactif` : 2023 N : n_A = n₀ − x ; x_f = 0,6 mol ; à t₁/₂, n_A = 0,6 mol → t₁/₂ ≈ 3,5 h. C₁ : même palier atteint plus tôt (catalyseur). | t₁/₂ sur une courbe de réactif |
| `ci_n5_trois` : 2025 N : même x_f = 133 mmol : les facteurs cinétiques changent la durée, pas l'état final. (b) : x_f/2 = 66,5 mmol → t₁/₂ ≈ 90 min. | — |
| `ci_n6_sigma` : 2021 N : σ = 0,25 − 160·x → v = −(1/(160·V₀))·dσ/dt = 0,78 mol·m⁻³·min⁻¹. σ₁/₂ = 0,25 − 160 × 5·10⁻⁴ = 0,17 S·m⁻¹ → t₁/₂ = 4 min. | — |
| `ci_n7_conductance` : 2018 R : G₁/₂ = (1,57·10⁻³ − 5·10⁻⁴)/(6,3·10⁻²) = 0,017 S = 17 mS → t₁/₂ ≈ 17 min. Attention : G lue en mS, relation en S. | — |
| `ci_n8_trempe` : 2017 R : trempe : le refroidissement brusque bloque la réaction ; on dose l'acide restant. Palier n(acide) = 0,2 mol → x_f = 0,6 − 0,2 = 0,4 mol. | — |
| `ci_r1_litres` : V = 100 mL = 0,100 L : v(0) = (1/0,100) × 0,25 = 2,5 mmol·L⁻¹·min⁻¹ = 2,5 mol·m⁻³·min⁻¹. | — |
| `ci_r2_unites` : 10⁻² mol/L = 10 mol/m³ ; 19,9 mS·m²·mol⁻¹ = 19,9·10⁻³ S·m²·mol⁻¹. Attention : σ lue en mS/m → S/m (250 mS/m = 0,250 S/m). | — |
| `ci_bl_fiche` : n(I₂) = C·V_E/2 ; x = x_max·(σ₀ − σ)/(σ₀ − σ_f) ; x = (P − P₀)·V/(R·T). v = (1/V)·dx/dt (tangente, V en L) ; v diminue ; x(t₁/₂) = x_f/2. | — |
| `ci_cr_carte` : Suivre x(t) → méthodes → tableau → x(t) → v(t) (tangente) → v diminue → t₁/₂. | — |

