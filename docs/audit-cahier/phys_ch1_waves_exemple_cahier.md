# Le cahier de l'élève — Ondes mécaniques progressives (`phys_ch1_waves_exemple`)

18 novembre 2026, skill `cahier-de-l-eleve`. Le cahier idéal du chapitre, écrit d'un seul tenant, puis découpé dans
`blocs[].cahier` / `cahier_figures` et `concentration.cahier` / `cahier_figures` du cours en ligne
(`backend/data/courses/phys_ch1_waves_exemple.json`, 16 diapositives, 5 blocs) et de la copie en attente
(`backend/data/courses/en_attente/phys_ch1_waves_exemple.json`, 45 diapositives, 15 blocs). Seuls ces quatre champs
changent (vérifié en comparant le reste des fichiers).

## Le plan du cahier

Numérotation du cours (titres des parties et des diapositives) : le lecteur affiche le titre de la partie (I., II., …)
quand le bloc y entre ; chaque ligne qui ouvre une sous-partie porte son numéro (I.1, I.2…), les lignes suivantes la
continuent. Aucune ligne n'utilise un symbole qui n'a pas été écrit avant.

- **I. L'onde mécanique progressive** — I.1 source, perturbation, milieu, élongation ; I.2 définition ; I.3 onde
  transversale ; I.4 onde longitudinale, dimension ; I.5 le son (bougie, cloche à vide).
- **II. La célérité** — II.0 rappel vitesse ; II.1 définition, v = d/Δt ; II.2 nature du milieu, ordres de grandeur ;
  II.3 température, tension, masse linéique (et ce qui ne change pas v).
- **III. Le retard temporel** — III.1 τ = SM/v ; III.2 y_M(t) = y_S(t − τ) (onde non amortie) ; III.3 θ, L = v·θ ;
  III.4 dates t_M = t₀ + SM/v, méthode pour tracer l'aspect.
- **IV. Lire une onde** — IV.1 aspect y(x) ou film y_M(t) ; IV.2 points qui montent, qui descendent.
- **V. Mesurer** — V.0 rappel ms, µs ; V.1–V.2 deux micros, méthode de l'oscilloscope ; V.3–V.4 ultrasons, écho.
- **VI. Rédiger comme le barème** (méthode en 4 temps).
- **VII. Cas types du national** — VII.1 oscillogramme émetteur/récepteur (2022 N) ; VII.2 émetteur entre deux micros
  (2024 R) ; VII.3 deux aspects (2024 N) ; VII.4 retard lu sur y_M(t) (2022 R) ; VII.5 droite Δt = f(d) (2021 R) ;
  VII.6 échographie (2020 R) ; VII.7 deux milieux (2018 N) ; VII.8 reconnaître le cas.
- **VIII. Bilan.**

Le cours en ligne suit le même plan, plus court (I.1–I.3, II.1–II.2, III.1–III.2, IV.1–IV.2, V.1–V.2, VI.1–VI.2) :
sa partie VI « Méthode bac et bilan » rassemble la rédaction, la reconnaissance des cas et le bilan.

## Ce qui a été ajouté ou corrigé

- **Numérotation continue** : chaque sous-partie ouverte par son numéro, dans l'ordre des diapositives.
- **Taille** : les blocs du national (copie en attente) n'avaient qu'**une** ligne → 3 ou 4 lignes chacun (le cas, la
  méthode numérotée, un exemple chiffré du sujet, l'erreur fréquente) ; les lignes de 200 caractères sont coupées en
  idées (≤ ~100 caractères, sauf la définition, recopiée mot pour mot) ; bulles de diapositive ramenées à 1–2 phrases.
- **Définitions et lois** : « Définition : » ; chaque relation avec son domaine (milieu homogène, onde non amortie) et
  ses unités ; l'élongation est définie (elle était utilisée sans être écrite).
- **Méthodes numérotées** : oscilloscope (S_H, n, τ, v), tracer l'aspect à la date t, droite Δt = f(d), rédaction en
  4 temps ; une méthode par cas type du national (VII.1 à VII.7) et la table « mot-code → relation » (VII.8).
- **Compléments** : « Attention » (ressort transversal, début avec début, diviser par 2, rayon du front, τ là où la
  courbe quitte l'axe, l'amplitude ne change pas v) ; « Exemple » avec les valeurs des sujets corrigés.
- **Dessins** : les 5 dessins existants gardés (corde secouée, transversale/longitudinale, aspect, film, oscillogramme) ;
  **3 ajoutés** dans la copie en attente : « Un émetteur entre deux micros » (ℓ, d − ℓ, d = 2,85 m), « Le retard lu
  sur la courbe de M » (y_M = 6·sin(2π(t − 10)/20) mm, nulle jusqu'à 10 ms, valeurs de `national.html`), « La droite
  Δt = f(d) » (passe par 40 cm ; 0,08 ms, pente 2 × 10⁻⁴ s/m).
- `verifier_figures_cahier.py` : 0 erreur, 0 avertissement sur les deux fichiers.

## Ce qui reste

- La diapositive de rédaction de la copie s'appelle « VI. » (sans « VI.1 ») : la ligne du cahier reprend « VI. ».
- Les trois nouveaux dessins sont vérifiés par le script et calculés, pas encore regardés dans le navigateur.

## Le cahier complet — copie en attente (le cours à venir)

> Rendu vérifié dans frontend/src/components/course/memoire/CycleBloc.tsx : le lecteur affiche lui-même le titre de la partie (I., II.…) ; les titres de diapositive ne s'affichent que si un bloc a autant de lignes que de diapositives, ce qu'aucun bloc n'a ici. Les lignes ne répètent donc pas le titre de partie : elles portent seulement le numéro de sous-partie (I.1, I.2…).

### Séance 1 — L’onde, ses deux types et sa célérité

**Ouverture — un ballon sur la vague**

**I. L'onde mécanique progressive**

Bloc `wx_s1_b1` — Une perturbation qui avance sans transporter la matière (diapositives : `wx_o1_bouee`, `wx_i1_corde`, `wx_i2_definition`)

- I.1 On secoue S : la perturbation (une déformation) avance le long de la corde (le milieu).
- Élongation y : écart d'un point à sa position de repos.
- Quand elle passe, M monte, descend, puis revient à sa place : la matière n'avance pas.
- I.2 Définition : une onde mécanique progressive est le phénomène de propagation d'une perturbation dans un milieu matériel élastique, avec transport d'énergie et sans transport de matière.
- Milieu élastique : il se déforme puis reprend sa forme ; la perturbation passe de proche en proche.
- 🖉 *croquis* « Une corde secouée en S » — La perturbation avance vers M ; quand elle passe, M monte, descend puis revient à sa place : la matière n'avance pas.

Bloc `wx_s1_b2` — Transversale ou longitudinale, et le son (diapositives : `wx_i3_types`, `wx_i3b_longitudinale`, `wx_i3c_son`)

- I.3 Onde transversale : la perturbation est perpendiculaire à la direction de propagation (corde, eau).
- I.4 Onde longitudinale : la perturbation a la même direction que la propagation (ressort comprimé, son).
- Attention : un ressort secoué perpendiculairement porte une onde transversale : on compare les directions.
- Dimension : corde → 1 (unidimensionnelle) ; surface de l'eau → 2 ; son dans l'air → 3.
- I.5 Bougie devant un haut-parleur : la flamme avance et recule, donc le son est longitudinal.
- Cloche à vide : la sonnerie ne s'entend plus, donc le son ne se propage pas dans le vide.
- 🖉 *schema* « Transversale ou longitudinale ? » — Transversale : M bouge perpendiculairement à la propagation ; longitudinale (ressort, son) : M bouge dans la même direction.

**II. La célérité**

Bloc `wx_s1_b2b` — La vitesse, puis la célérité et ce dont elle dépend (diapositives : `wx_p1_vitesse`, `wx_c1_celerite`, `wx_c2_facteurs`, `wx_c2b_temperature`)

- II.0 Rappel : vitesse v = d/Δt, la distance parcourue en une seconde (d en m, Δt en s, v en m/s).
- II.1 Définition : la célérité v est la vitesse de propagation de la perturbation ; v = d/Δt.
- d se mesure du front au front ; dans un milieu homogène, v est la même partout.
- II.2 v dépend de la nature du milieu : en général v(solide) > v(liquide) > v(gaz).
- Air ≈ 340 m/s (20 °C), eau ≈ 1500 m/s, acier ≈ 5000 m/s ; même distance d : Δt = d/v.
- II.3 v croît avec la température, la tension ; décroît avec la masse linéique. Attention : l'amplitude ne change pas v.


### Séance 2 — Le retard, lire une onde, mesurer la célérité

**III. Le retard temporel**

Bloc `wx_s1_b3` — Le retard, l'élongation, la durée et la longueur (diapositives : `wx_r1_retard`, `wx_r1b_elongation`, `wx_r2_duree_longueur`, `wx_r2b_dates`)

- III.1 Retard : τ = t_M − t_S = SM/v (milieu homogène ; τ en s, SM en m, v en m/s).
- III.2 Onde non amortie : y_M(t) = y_S(t − τ) : à la date t, M fait ce que S faisait à t − τ.
- Entre deux points : τ = M₁M₂/v et y_M₂(t) = y_M₁(t − τ).
- III.3 θ : durée de perturbation d'un point (s) ; L : longueur de la perturbation (m) ; L = v·θ.
- III.4 Source partie à t₀ : M est atteint à t_M = t₀ + SM/v et revient au repos à t_M + θ.
- Méthode (aspect à la date t) : 1) front à v·(t − t₀) de S ; 2) la perturbation sur L derrière lui.
- 🖉 *courbe* « Aspect de la corde à un instant t » — La photo y(x) : le front est le plus loin de S ; la perturbation occupe la longueur L = v · θ.

**IV. Lire une onde : aspect ou élongation**

Bloc `wx_s1_b3b` — Lire une onde : aspect ou élongation (diapositives : `wx_l1_aspect`, `wx_l2_sens`)

- IV.1 Avant de lire une valeur, regarder l'axe horizontal.
- y(x) : aspect du milieu à un instant (photo) ; le front est à droite, le plus loin de S ; on y lit L.
- y_M(t) : mouvement d'un point (film) ; le front est à gauche, il arrive en premier ; on y lit τ et θ.
- IV.2 Sur l'aspect : devant le sommet (côté front) les points montent ; derrière, ils descendent.
- Devant le front et derrière la queue, les points sont au repos.
- 🖉 *courbe* « Le film d'un point M » — Le film de M : le front arrive en premier, à gauche (t = τ) ; même forme que la photo, vue dans un miroir.

**V. Mesurer : TP et ultrasons**

Bloc `wx_s2_b1` — Mesurer la célérité : la milliseconde et les deux micros (diapositives : `wx_p2_milli`, `wx_m1_micros`, `wx_m1b_lecture`)

- V.0 Rappel : 1 ms = 10⁻³ s ; 1 µs = 10⁻⁶ s ; dans un calcul, le temps se met en seconde.
- V.1 Deux micros distants de d : le son atteint M₁ puis M₂ ; pendant τ il parcourt d : v = d/τ.
- V.2 Méthode : 1) lire la sensibilité horizontale S_H ; 2) compter n divisions entre les deux débuts ;
- 3) τ = n × S_H, converti en s ; 4) v = d/τ, puis vérifier l'ordre de grandeur.
- Attention : début avec début (ou sommet avec sommet). M₂ éloigné de d' : τ' = (d + d')/v.
- 🖉 *courbe* « Oscillogramme : deux micros » — On mesure τ entre les deux débuts de signal (début avec début), puis v = d/τ.


### Séance 3 — L'écho, rédiger, puis le national : lire l'oscillogramme

**VI. Méthode bac : rédiger**

Bloc `wx_s2_b1b` — L’écho, puis rédiger comme le barème (diapositives : `wx_m2_sonar`, `wx_m2b_formule`, `wx_b1_redaction`)

- V.3 Ultrasons : fréquence au-delà de 20 kHz (inaudibles) ; sonar, échographie.
- Écho : l'onde va jusqu'à l'obstacle, se réfléchit et revient : elle parcourt 2d.
- V.4 Pendant τ (aller-retour) : 2d = v·τ, donc d = v·τ/2. Attention : diviser par 2.
- Rédiger comme le barème : 1) la relation ; 2) l'application numérique en unités SI ; 3) le résultat ; 4) l'unité.
- Attention : un calcul sans relation ou sans unité ne rapporte pas tous les points.

**VII. Exercices du national, joués pas à pas**

Bloc `wx_s4_b1` — National 2022 normale : lire Δt sur l'oscillogramme, puis v (diapositives : `wx_n1_national_2022n`, `wx_n1c_correction_2022n`)

- VII.1 Émetteur et récepteur, oscillogramme (2022 N).
- Méthode : 1) repérer le début de (a) et de (b) ; 2) Δt = n × S_H ; 3) v = L/Δt (L en m, Δt en s).
- Exemple : n = 6 − 1 = 5 div ; Δt = 5 × 0,5 ms = 2,5 ms ; v = 0,85/(2,5 × 10⁻³) = 340 m/s.

Bloc `wx_s4_b1b` — National 2024 rattrapage : un émetteur entre deux micros (diapositives : `wx_n2_national_2024r`, `wx_n2c_correction_2024r`)

- VII.2 Émetteur entre deux micros (2024 R) : le son parcourt ℓ vers M₁ et d − ℓ vers M₂.
- τ = (d − ℓ)/v − ℓ/v = (d − 2ℓ)/v, donc ℓ = (d − v·τ)/2.
- Exemple : τ = 4 × 0,5 ms = 2 ms ; ℓ = (2,85 − 340 × 2 × 10⁻³)/2 ≈ 1,09 m.
- 🖉 *croquis* « Un émetteur entre deux micros » — Vers M₁ le son parcourt ℓ, vers M₂ il parcourt d − ℓ : τ = (d − ℓ)/v − ℓ/v = (d − 2ℓ)/v.


### Séance 4 — National : deux aspects, la courbe y_M(t), la droite Δt = f(d)

Bloc `wx_s4_b1c` — National 2024 normale : deux aspects de la surface de l'eau (diapositives : `wx_n3_national_2024n`, `wx_n3c_correction_2024n`)

- VII.3 Deux aspects de la surface de l'eau (2024 N) : le front avance de r₂ − r₁ pendant t₂ − t₁.
- v = (r₂ − r₁)/(t₂ − t₁) ; source partie de O à t = 0 : r₁ = v·t₁.
- Attention : r est le rayon du front (la ride la plus loin de O).
- Exemple : v = 0,42/1,5 = 0,28 m/s ; t₁ = 0,14/0,28 = 0,5 s ; t₂ = 0,5 + 1,5 = 2,0 s.

Bloc `wx_s4_b1d` — National 2022 rattrapage : lire le retard sur la courbe y_M(t) (diapositives : `wx_n7_national_2022r`, `wx_n7c_correction_2022r`)

- VII.4 Courbe y_M(t), source partie à t = 0 (2022 R) : τ = date où M commence à bouger.
- Puis v = SM/τ (SM en m, τ en s).
- Attention : τ se lit là où la courbe quitte l'axe, pas au premier sommet.
- Exemple : M démarre à 10 ms → τ = 0,01 s ; v = 2,5 × 10⁻²/0,01 = 2,5 m/s.
- 🖉 *courbe* « Le retard lu sur la courbe de M » — S part à t = 0 ; M reste au repos jusqu'à 10 ms : τ = 10 ms = 0,01 s, puis v = SM/τ.

Bloc `wx_s4_b2` — National 2021 rattrapage : la droite Δt = f(d) (diapositives : `wx_n4_national_2021r`, `wx_n4c_correction_2021r`)

- VII.5 Droite Δt = f(d) passant par l'origine (2021 R) : Δt = k·d, avec k = 1/v.
- Méthode : 1) un point de la droite ; 2) k = Δt/d en s/m ; 3) v = 1/k ; 4) le tableau donne le métal.
- Exemple : k = 8 × 10⁻⁵/0,4 = 2 × 10⁻⁴ s/m ; v = 1/k = 5000 m/s → aluminium.
- 🖉 *courbe* « La droite Δt = f(d) » — Droite par l'origine : Δt = k·d ; k = 8×10⁻⁵ s / 0,4 m = 2×10⁻⁴ s/m, donc v = 1/k = 5000 m/s.


### Séance 5 — National : l'écho, deux milieux ; reconnaître le cas ; bilan

Bloc `wx_s4_b2b` — National 2020 rattrapage : l'échographie (diapositives : `wx_n5_national_2020r`, `wx_n5c_correction_2020r`)

- VII.6 Échographie (2020 R) : chaque écho fait l'aller-retour depuis la sonde.
- 1er écho : 2d₁ = v·t₁ ; 2e écho : 2(d₁ + d₂) = v·t₂ ; on soustrait : 2d₂ = v·(t₂ − t₁).
- Exemple : d₂ = 1540 × 80 × 10⁻⁶/2 ≈ 6,16 × 10⁻² m = 6,16 cm.

Bloc `wx_s4_b2c` — National 2018 normale : air et pétrole, même distance (diapositives : `wx_n6_national_2018n`, `wx_n6c_correction_2018n`)

- VII.7 Deux milieux, même distance L (2018 N) : chaque onde met L/v.
- τ = t_lent − t_rapide = L/V_air − L/V_p = L·(1/V_air − 1/V_p).
- Exemple : τ = 2 × 2 ms = 4 ms ; 1/V_p = 1/340 − 4 × 10⁻³/1,84, donc V_p ≈ 1303 m/s.

Bloc `wx_s2_b2` — Reconnaître le cas type : les sept cas du national revus (diapositives : `wx_b2_national`)

- VII.8 Reconnaître le cas par le mot-code de l'énoncé :
- deux micros, oscillogramme → τ = n × S_H, v = d/τ ; deux aspects → v = Δr/Δt ;
- courbe y_M(t) → τ = date où M démarre ; écho → 2d = v·τ ;
- droite Δt = f(d) → pente k = 1/v ; deux milieux → τ = L·(1/v_lent − 1/v_rapide).

**VIII. Bilan du chapitre**

Bloc `wx_s4_b3` — Le bilan du chapitre (diapositives : `wx_b3_bilan`, `wx_b4_carte`)

- Onde = perturbation qui se propage, avec transport d'énergie, sans transport de matière.
- Transversale (⊥) ou longitudinale (∥) ; le son est longitudinal et ne passe pas dans le vide.
- v = d/Δt dépend du milieu ; τ = SM/v ; y_M(t) = y_S(t − τ) (non amortie) ; L = v·θ.
- Mesurer : τ = n × S_H, v = d/τ ; écho 2d = v·τ. Rédiger : relation → application numérique → résultat → unité.


## Le cahier complet — cours en ligne

### Séance 1 — L'onde, sa célérité et son retard

**Ouverture — un ballon sur la vague**

**I. L'onde mécanique progressive**

Bloc `wx_s1_b1` — Une perturbation qui avance sans transporter la matière (diapositives : `wx_o1_bouee`, `wx_i1_corde`, `wx_i2_definition`)

- I.1 On secoue S : la perturbation (une déformation) avance le long de la corde (le milieu).
- Élongation y : écart d'un point à sa position de repos.
- Quand elle passe, M monte, descend, puis revient à sa place : la matière n'avance pas.
- I.2 Définition : une onde mécanique progressive est le phénomène de propagation d'une perturbation dans un milieu matériel élastique, avec transport d'énergie et sans transport de matière.
- 🖉 *croquis* « Une corde secouée en S » — La perturbation avance vers M ; quand elle passe, M monte, descend puis revient à sa place : la matière n'avance pas.

**II. La célérité**

Bloc `wx_s1_b2` — Transversale ou longitudinale, et la célérité (diapositives : `wx_i3_types`, `wx_c1_celerite`, `wx_c2_facteurs`)

- I.3 Onde transversale : la perturbation est perpendiculaire à la direction de propagation (corde).
- Onde longitudinale : la perturbation a la même direction que la propagation (ressort, son).
- II.1 Célérité v : vitesse de propagation ; v = d/Δt (d en m, Δt en s, v en m/s).
- d se mesure du front au front ; dans un milieu homogène, v est la même partout.
- II.2 v dépend du milieu : nature, température ; tension et masse linéique d'une corde.
- Air ≈ 340 m/s, eau ≈ 1500 m/s. Attention : ni la source ni l'amplitude ne changent v.
- 🖉 *schema* « Transversale ou longitudinale ? » — Transversale : M bouge perpendiculairement à la propagation ; longitudinale (ressort, son) : M bouge dans la même direction.

**III. Le retard temporel**

**IV. Lire une onde : aspect ou élongation**

Bloc `wx_s1_b3` — Le retard, la longueur, et lire une onde (diapositives : `wx_r1_retard`, `wx_r2_duree_longueur`, `wx_l1_aspect`, `wx_l2_sens`)

- III.1 Retard : M reproduit le mouvement de S plus tard ; τ = SM/v (τ en s, SM en m).
- Onde non amortie : y_M(t) = y_S(t − τ).
- III.2 θ : durée de perturbation d'un point (s) ; L : longueur de la perturbation (m) ; L = v·θ.
- IV.1 Lire l'axe d'abord : y(x) = aspect à un instant, front à droite ; y(t) = film d'un point, front à gauche.
- IV.2 Sur l'aspect : devant le sommet (côté front) les points montent ; derrière, ils descendent.
- 🖉 *courbe* « Aspect de la corde à un instant t » — La photo y(x) : le front est le plus loin de S ; la perturbation occupe la longueur L = v · θ.
- 🖉 *courbe* « Le film d'un point M » — Le film de M : le front arrive en premier, à gauche (t = τ) ; même forme que la photo, vue dans un miroir.


### Séance 2 — Mesurer, rédiger, retenir

**V. Mesurer : TP et ultrasons**

**VI. Méthode bac et bilan**

Bloc `wx_s2_b1` — Mesurer la célérité : deux micros, l'écho, la rédaction (diapositives : `wx_m1_micros`, `wx_m2_sonar`, `wx_b1_redaction`)

- V.1 Méthode (deux micros) : 1) lire la sensibilité horizontale S_H ; 2) compter n divisions ;
- 3) τ = n × S_H, converti en s (1 ms = 10⁻³ s) ; 4) v = d/τ, puis vérifier l'ordre de grandeur.
- Attention : on compte du début d'un signal au début de l'autre (ou sommet avec sommet).
- V.2 Ultrasons : au-delà de 20 kHz. Écho : l'onde fait l'aller-retour, elle parcourt 2d.
- Donc 2d = v·τ et d = v·τ/2. Attention : ne pas oublier de diviser par 2.
- VI.1 Rédiger : relation → application numérique (unités SI) → résultat → unité.
- 🖉 *courbe* « Oscillogramme : deux micros » — On mesure τ entre les deux débuts de signal (début avec début), puis v = d/τ.

Bloc `wx_s2_b2` — Exercice type national et bilan du chapitre (diapositives : `wx_b2_national`, `wx_b3_bilan`, `wx_b4_carte`)

- VI.2 Reconnaître le cas : deux micros, oscillogramme → τ = n × S_H et v = d/τ ;
- photo de la corde → aspect y(x), front, L ; écho → d = v·τ/2 ; droite Δt = f(d) → pente k = 1/v.
- Bilan : onde = perturbation qui se propage, avec transport d'énergie, sans transport de matière.
- Formules : v = d/Δt ; τ = SM/v ; y_M(t) = y_S(t − τ) ; L = v·θ ; τ = n × S_H ; 2d = v·τ.

