# Le cahier de l'élève — Ondes mécaniques progressives périodiques (`phys_ch2_ondes_periodiques`)

18 novembre 2026, skill `cahier-de-l-eleve`. Le cahier idéal du chapitre, écrit d'un seul tenant, puis découpé dans
`blocs[].cahier` / `cahier_figures` et `concentration.cahier` / `cahier_figures` du cours en ligne
(`backend/data/courses/phys_ch2_ondes_periodiques.json`, 15 blocs) et de la copie en attente
(`backend/data/courses/en_attente/phys_ch2_ondes_periodiques.json`, 17 blocs, où le retard passe en partie V et les
nationaux sont joués pas à pas). Seuls ces quatre champs changent (vérifié en comparant le reste des fichiers).

## Le plan du cahier

Les titres des diapositives de ce cours ne sont pas numérotés : le cahier numérote lui-même les sous-parties dans
chaque partie (le lecteur affiche le titre de la partie, I., II., …, quand le bloc y entre). Les numéros suivent les
parties de CHAQUE fichier (la copie en attente a déplacé le retard).

- **Ouverture** — la source vibre sans arrêt ; rappels du chapitre 1 ; « périodique » ; onde périodique, sinusoïde,
  onde sinusoïdale (définitions).
- **I. La période et la fréquence** — I.1 période T (définition) ; I.2 même T partout ; I.3 fréquence N, N = 1/T ;
  I.4 convertir ; I.5 lire T (film, oscillogramme : méthodes) ; I.6 périodique non sinusoïdale.
- **II. La longueur d'onde** — II.1 périodicité spatiale ; II.2 λ (définition) ; II.3 double périodicité, lire
  l'axe ; II.4 cuve à ondes ; II.5 méthode des intervalles ; II.6 distance depuis S.
- **III. La célérité** — III.1 en T, l'onde avance de λ ; III.2 λ = v·T, v = λ·N ; III.3 rédiger ; III.4 photo datée.
- **IV. En phase, en opposition de phase** — IV.1 d = k·λ ; IV.2 d = (2k + 1)·λ/2 ; IV.3 méthode d/λ ; IV.4 n-ième
  point en opposition.
- **Le retard** (V en attente, VIII en ligne) — .1 τ = SM/v ; .2 y_M(t) = y_S(t − τ), cas SM = k·λ ; .3 lire τ ;
  .4 lire T, ne pas confondre τ et T, méthode τ → v, T → N et λ.
- **Mesurer λ et la célérité** (VI en attente, V en ligne) — .1 stroboscope ; .2 immobilité apparente ; .3 deux
  récepteurs ; .4 préfixe µs ; .5 retour en phase ; .6 méthode λ = d/n.
- **La diffraction** (VII / VI) — .1 le phénomène, onde diaphragmée ; .2 ce qui ne change pas ; .3 méthode a ≤ λ et
  dessin ; .4 ultrasons et son.
- **Milieu dispersif** (VIII / VII) — .1 autre fréquence ; .2 l'air ; .3 définition, et l'erreur « λ dépend de N ».
- **IX. Cas types du bac** — IX.1 tracer y_S(t) ; IX.2 national 2017 ; IX.3 national 2020 ; IX.4 devoir sur la cuve.
- **X. Bilan.**

## Ce qui a été ajouté ou corrigé

- **Numérotation continue** (I.1 → X), absente avant ; la même démarche dans les deux fichiers.
- **Définitions mot pour mot** marquées « Définition : » (périodique, sinusoïdale, T, N, λ, milieu dispersif).
- **Lois avec conditions et unités** : λ = v·T (milieu homogène), y_M(t) = y_S(t − τ) (onde non amortie), N = k·N_e
  (k entier non nul), changement de milieu (N garde sa valeur).
- **Méthodes numérotées** pour chaque cas type de l'exploration : lire T (film, oscillogramme), λ par les intervalles,
  d/λ (phase), deux récepteurs (λ = d/n), justifier la diffraction, tracer y_S(t), τ → v / T → N, λ.
- **Compléments tirés des erreurs du national** (`exploration/ondes_mecaniques_periodiques.json`) : λ en m avant
  v = λ·N (200 au lieu de 2 m/s, 2017 N) ; « t + τ » faux (2017 N) ; 1 cm couvre 2λ (2020 N) ; τ ≠ T (2022 R) ;
  « dispersif » = v dépend de N, pas λ (2020 R) ; même état = même position et même sens.
- **Taille** : lignes de 200 caractères coupées (une idée par ligne) ; blocs de 2 lignes (nationaux de la copie)
  portés à 3–4 ; bloc du devoir et bilan resserrés ; bulles en 1–2 phrases.
- **Dessins** : 8 dessins gardés ; « Trois lectures sur le film de M » refait sur les valeurs du national 2022 R
  (amplitude 6 mm au lieu de 1, crêtes à 15 et 35 ms cotées T = 20 ms, τ = 10 ms) et posé aussi dans la copie, où la
  diapositive n'avait plus de dessin ; le bloc « Périodique non sinusoïdale + λ » du cours en ligne reçoit le
  dessin de l'instrument. `verifier_figures_cahier.py` : 0 erreur, 0 avertissement.

## Ce qui reste

- Les titres des diapositives ne portent pas de numéro : si on les numérote un jour, reprendre ceux du cahier.
- Le dessin refait n'a pas été regardé dans le navigateur (vérifié par le script et calculé).

## Le cahier complet — copie en attente (le cours à venir)

> Rendu vérifié dans frontend/src/components/course/memoire/CycleBloc.tsx : le lecteur affiche lui-même le titre de la partie (I., II.…) ; les titres de diapositive ne s'affichent que si un bloc a autant de lignes que de diapositives, ce qu'aucun bloc n'a ici. Les lignes ne répètent donc pas le titre de partie : elles portent seulement le numéro de sous-partie (I.1, I.2…).

### Séance 1 — La source vibre : période et fréquence

**Ouverture — la source ne s'arrête plus**

Bloc `op_s1_b1` — Une source qui vibre sans arrêt (diapositives : `op_o1_vibreur`, `op_o2_acquis`, `op_o2b_retard`, `op_o3_periodique`)

- Ouverture : la source vibre sans arrêt ; chaque point du milieu recommence le même mouvement.
- Rappels (chapitre 1) : v = d/Δt ; τ = SM/v ; photo y(x) = le milieu à un instant ; film y_M(t) = un point.
- Définition : un phénomène périodique se reproduit identique à lui-même à intervalles de temps égaux ; cette durée est la période.

**I. La période et la fréquence**

Bloc `op_s1_b2` — Onde périodique, sinusoïdale, et la période T (diapositives : `op_o4_definition`, `op_pr1_sinusoide`, `op_o5_sinusoidale`, `op_t1_periode`)

- Définition : une onde progressive est périodique si la perturbation se répète, identique à elle-même, à intervalles de temps égaux.
- Rappel : une sinusoïde est une courbe qui monte et descend régulièrement ; le même motif se répète.
- Définition : une onde périodique est sinusoïdale si l'élongation de chaque point est une fonction sinusoïdale du temps.
- À un instant, la corde a la forme d'une sinusoïde : crêtes, creux ; amplitude = élongation maximale.
- I.1 Définition : la période T est la plus petite durée au bout de laquelle un point du milieu se retrouve dans le même état vibratoire (T en s).
- Attention : même état = même position et même sens de mouvement ; T se lit entre deux crêtes voisines.
- 🖉 *courbe* « Le film d'un point : la période T » — Entre deux crêtes voisines, M revient dans le même état (même position, même sens) : T = 0,5 s.

Bloc `op_s1_b3` — Même période partout, et la fréquence N = 1/T (diapositives : `op_t2_meme_periode`, `op_t3_frequence`, `op_t4_inverse`)

- I.2 Tous les points du milieu vibrent avec la même période T, celle de la source.
- I.3 Définition : la fréquence N est le nombre de périodes effectuées en une seconde ; N en hertz (Hz).
- N = 1/T (T en s, N en Hz), car en une seconde le point fait 1/T périodes.
- Exemple : T = 0,5 s → N = 1/0,5 = 2 Hz. Remarque : certains livres notent N par f ou ν.


### Séance 2 — Lire T, puis la longueur d'onde λ

Bloc `op_s2_b1` — Convertir, lire T sur le film, sur l’oscillogramme, et pour un son non sinusoïdal (diapositives : `op_t5_convertir`, `op_t6_film`, `op_t7_oscillo`, `op_t8_non_sinusoidale`)

- I.4 Convertir avant de calculer : 1 ms = 10⁻³ s ; 1 µs = 10⁻⁶ s ; 1 cm = 10⁻² m ; 1 mm = 10⁻³ m.
- I.5 Méthode (film y_M(t)) : T entre deux points voisins dans le même état (deux crêtes voisines).
- Méthode (oscillogramme) : T = n × S_H (n divisions, sensibilité horizontale S_H), en s ; puis N = 1/T.
- Attention : toujours écrire l'unité (« T = 5 » est faux).
- I.6 Une onde sinusoïdale est toujours périodique ; une onde périodique n'est pas toujours sinusoïdale.
- Diapason : sinusoïde ; instrument : motif répété non sinusoïdal ; T entre deux motifs identiques voisins.
- 🖉 *courbe* « Diapason : onde sinusoïdale » — La courbe est une sinusoïde ; T entre deux crêtes voisines.
- 🖉 *courbe* « Instrument : onde périodique non sinusoïdale » — Le même motif se répète, mais ce n'est pas une sinusoïde ; T entre deux motifs identiques voisins.

**II. La longueur d'onde**

Bloc `op_s2_b2` — La longueur d'onde λ, et lire l'axe (diapositives : `op_l1_photo`, `op_l2_lambda`, `op_l3_axe`)

- II.1 Sur la photo de la corde, le même motif se répète le long du milieu : périodicité spatiale.
- II.2 Définition : la longueur d'onde λ est la plus petite distance séparant deux points du milieu dans le même état vibratoire (λ en m).
- II.3 Double périodicité : sur y_M(t) (axe en s) on lit T ; sur y(x) (axe en m) on lit λ.
- Attention : lire l'axe avant de mesurer ; λ se lit de crête à crête voisine, pas jusqu'au front.
- 🖉 *courbe* « La photo de la corde : la longueur d'onde λ » — À un instant, le même motif se répète le long de la corde : de crête à crête voisine, λ = 0,5 m.

Bloc `op_s2_b3` — Les rides de la cuve : compter les intervalles (diapositives : `op_l4_rides`, `op_l5_intervalles`, `op_l6_source`)

- II.4 Cuve à ondes vue de dessus : chaque trait clair est une crête ; deux traits voisins sont distants de λ.
- Pointe → onde circulaire ; réglette → onde rectiligne (sans amortissement ni réflexion).
- II.5 Méthode : 1) distance réelle d (avec l'échelle) ; 2) compter n intervalles, pas les traits ; 3) λ = d/n.
- Exemple : 4 traits = 3 intervalles ; d = 4,5 cm → λ = 4,5/3 = 1,5 cm.
- II.6 La distance à la source se compte depuis S : compter tous les λ entre S et M.
- 🖉 *schema* « Cuve à ondes vue de dessus » — Chaque trait est une crête ; la règle couvre 4 traits mais 3 intervalles : λ = d/n = 4,5/3 = 1,5 cm.


### Séance 3 — λ = v · T, en phase ou en opposition, et le retard

**III. La célérité : λ = v·T**

Bloc `op_s3_b1` — Pendant une période, l'onde avance de λ (diapositives : `op_c1_avance`, `op_c2_relation`, `op_c3_rediger`, `op_c4_photo_datee`)

- III.1 Pendant une période T, l'onde avance d'une longueur d'onde λ.
- III.2 λ = v·T et v = λ·N (milieu homogène ; λ en m, T en s, N en Hz, v en m/s).
- Attention : λ en m avant de multiplier (λ = 4 cm, N = 50 Hz : v = 0,04 × 50 = 2 m/s, pas 200).
- Remarque : d'un milieu à l'autre, N ne change pas (imposée par la source) ; v et λ = v/N changent.
- III.3 Rédiger : relation → conversion en SI → application numérique → résultat avec unité.
- III.4 Photo datée : front à n·λ de la source à la date t → t = n·T.

**IV. En phase, en opposition de phase**

Bloc `op_s3_b2` — En phase, en opposition de phase (diapositives : `op_p1_en_phase`, `op_p2_opposition`, `op_p3_methode`, `op_p4_troisieme`)

- IV.1 Deux points vibrent en phase si leur distance est un nombre entier de λ : d = k·λ (k ∈ ℕ*).
- IV.2 Ils vibrent en opposition de phase si d = (2k + 1)·λ/2 (k ∈ ℕ) : l'un monte quand l'autre descend.
- IV.3 Méthode : 1) d et λ dans la même unité ; 2) calculer d/λ ; 3) entier → en phase ;
- entier et demi → opposition de phase ; sinon (ex. 2,25) → ni l'un ni l'autre ; 4) conclure par une phrase.
- IV.4 Le n-ième point en opposition de phase avec S : k = n − 1. Exemple : λ = 2 cm, 3e point : SM = 5λ/2 = 5 cm.
- 🖉 *courbe* « En phase, en opposition de phase » — M et P (d = λ) vibrent en phase ; M et Q (d = λ/2) vibrent en opposition de phase.

**V. Le retard dans une onde périodique**

Bloc `op_s5_b1` — Le retard dans une onde périodique (diapositives : `op_r1_retard`, `op_r2_relation`, `op_r3_trois_lectures`)

- V.1 M commence à vibrer à la date τ = SM/v, dans le même sens que le premier mouvement de S.
- V.2 Onde non amortie : y_M(t) = y_S(t − τ) : M refait ce que S a fait, avec le retard τ.
- Si SM = k·λ, alors τ = k·λ/v = k·T : M vibre en phase avec S.
- V.3 Sur y_M(t) : τ = date où M commence à bouger (avant, M est au repos).
- 🖉 *courbe* « Trois lectures sur le film de M » — τ = 10 ms au début du mouvement, T = 35 − 15 = 20 ms entre deux crêtes voisines, amplitude 6 mm : ne pas confondre τ et T.

Bloc `op_s5_b1b` — National 2022 R : T sur la courbe, puis N et v (diapositives : `op_r3c_periode`, `op_r3b_calculs`)

- V.4 Sur y_M(t) : T entre deux crêtes voisines ; l'amplitude est la hauteur maximale.
- Attention : ne pas confondre τ (début du mouvement) et T (entre deux crêtes).
- Méthode : τ → v = SM/τ ; T → N = 1/T ; puis λ = v·T (tout en unités SI).
- Exemple (2022 R) : τ = 10 ms, T = 35 − 15 = 20 ms, SM = 2,5 cm → N = 50 Hz, v = 2,5 m/s, λ = 5 cm.


### Séance 4 — Mesurer λ, puis la diffraction

**VI. Mesurer λ et la célérité**

Bloc `op_s3_b3` — Le stroboscope et les deux récepteurs (diapositives : `op_m1_strobo`, `op_m2_immobile`, `op_m3_recepteurs`)

- VI.1 Le stroboscope éclaire la cuve par des éclairs très brefs : chaque éclair donne une « photo ».
- VI.2 Immobilité apparente si N = k·N_e (N_e : fréquence des éclairs, k entier non nul).
- La plus grande fréquence des éclairs qui fige l'onde est N_e = N ; on mesure λ sur l'image figée.
- VI.3 Deux récepteurs côte à côte : courbes en phase ; récepteur éloigné : courbe décalée et plus petite.

Bloc `op_s4_b1` — Mesurer T et λ avec deux récepteurs (diapositives : `op_m4_microsecondes`, `op_m5_premier_retour`, `op_m6_nieme`, `op_m6b_deja_ecartes`)

- VI.4 Lire le préfixe de S_H (µs ≠ ms). Exemple : T = 5 × 5 µs = 25 µs ; N = 1/T = 40 kHz (ultrason).
- VI.5 En phase : maximums aux mêmes instants ; opposition : l'une maximale quand l'autre est minimale.
- Au premier retour en phase des deux courbes, le récepteur a été déplacé de λ.
- VI.6 Méthode : 1) compter n retours en phase ; 2) déplacement d = n·λ, donc λ = d/n ; 3) v = λ·N.
- Récepteurs déjà écartés au départ : seul le déplacement compte, λ = (d₂ − d₁)/n.

**VII. La diffraction**

Bloc `op_s4_b2` — La diffraction (diapositives : `op_d1_ouverture`, `op_d2_invariants`, `op_d3_justifier`)

- VII.1 Diffraction : une onde qui rencontre une ouverture (ou un obstacle) de petite dimension repart en ondes circulaires centrées sur l'ouverture.
- Ouverture large : l'onde passe sans changer de forme (onde diaphragmée). La diffraction est propre aux ondes.
- VII.2 L'onde diffractée garde la même N (source), la même v (même milieu), donc la même λ = v/N.
- VII.3 Méthode : 1) a et λ dans la même unité ; 2) a ≤ λ → diffraction, d'autant plus marquée que a est petite.
- Dessin : arcs de cercle centrés sur l'ouverture, espacés de λ.
- 🖉 *schema* « Diffraction par une ouverture (a ≤ λ) » — a ≤ λ : derrière l'ouverture, l'onde repart en arcs de cercle centrés sur l'ouverture, avec la même λ.


### Séance 5 — Le son diffracté, le milieu dispersif, deux nationaux joués pas à pas

**VIII. Milieu dispersif**

Bloc `op_s4_b3` — Le son se diffracte aussi ; milieu dispersif ou non (diapositives : `op_d4_ultrasons`, `op_s1_frequence`, `op_s2_air`, `op_s3_dispersif`)

- VII.4 Ultrasons (40 kHz) : λ = v/N = 340/(40 × 10³) = 8,5 mm ; fente a = 5 mm ≤ λ → R capte hors de l'axe : diffraction.
- Son audible (20 Hz à 20 kHz) : λ = 340/N va de 1,7 cm à 17 m ; le son se diffracte par une porte.
- VIII.1 Autre fréquence du vibreur : on remesure λ avant de recalculer v = λ·N.
- VIII.2 Dans l'air, la célérité du son (≈ 340 m/s) ne dépend pas de la fréquence.
- VIII.3 Définition : un milieu est dispersif si la célérité de l'onde dépend de sa fréquence (eau : oui ; air : non).
- Attention : λ = v/N dépend toujours de N ; « dispersif » veut dire que c'est v qui dépend de N.
- 🖉 *schema* « Diffraction d'une onde ultrasonore (a ≤ λ) » — R, déplacé sur un arc centré sur la fente, capte encore le signal hors de l'axe E-fente : l'onde est diffractée.

**IX. Cas types du bac**

Bloc `op_s5_b2` — La courbe de la source, puis le national 2017 joué pas à pas (diapositives : `op_r4_source`, `op_x1_national_2017`, `op_x1b_national_2017_retard`)

- IX.1 Méthode (tracer y_S(t) à partir de y_M(t)) : même amplitude, même T, mais la courbe part de t = 0 (avance de τ).
- Le premier mouvement de M (vers le haut ou vers le bas) est celui de la source au départ.
- IX.2 National 2017 : λ lue sur la règle, de crête à crête ; v = λ·N (λ en m) ; front en M : t = SM/v.
- y_M(t) = y_S(t − τ) avec τ = SM/v = 0,03 s : y_M(t) = y_S(t − 0,03). Attention : jamais « t + τ ».

Bloc `op_s5_b3` — National 2020 joué pas à pas : λ, N, τ, puis la diffraction (diapositives : `op_x2_national_2020`, `op_x2b_national_2020_diffraction`)

- IX.3 National 2020 : compter les intervalles : 1 cm couvre 2λ → λ = 0,5 cm = 5 × 10⁻³ m.
- N = v/λ = 0,25/(5 × 10⁻³) = 50 Hz ; retard τ = d/v = 0,05/0,25 = 0,2 s.
- Diffraction : N, λ et v ne changent pas (même vibreur, même milieu) ; seule la forme de l'onde change.


### Séance 6 — Le devoir sur la cuve, puis le bilan

Bloc `op_s6_b1` — Le devoir sur la cuve : en phase, puis milieu dispersif (diapositives : `op_x3_devoir`, `op_x3b_dispersif`)

- IX.4 Devoir (cuve à 20 Hz) : AB = 3λ = 4,5 cm → λ = 1,5 cm ; v = λ·N = 0,3 m/s ; AB/λ = 3 → en phase.
- À 30 Hz : λ′ = 1,1 cm ; v′ = λ′·N′ = 0,33 m/s ≠ 0,30 m/s.
- Donc la célérité dépend de N : la surface de l'eau est un milieu dispersif.

**X. Bilan du chapitre**

Bloc `op_s6_b2` — Le bilan du chapitre (diapositives : `op_b1_bilan`, `op_b2_carte`)

- T (s), N = 1/T (Hz), λ (m) ; λ = v·T = v/N (milieu homogène).
- En phase : d = k·λ (k ∈ ℕ*) ; opposition : d = (2k + 1)·λ/2 (k ∈ ℕ) ; retard : τ = SM/v, y_M(t) = y_S(t − τ).
- Mesures : T = n × S_H ; λ = d/n ; immobilité apparente N = k·N_e.
- Diffraction si a ≤ λ (même N, v, λ). Changement de milieu : N ne change pas. Milieu dispersif : v dépend de N.


## Le cahier complet — cours en ligne

### Séance 1 — La source vibre : période et fréquence

**Ouverture — la source ne s'arrête plus**

Bloc `op_s1_b1` — Une source qui vibre sans arrêt (diapositives : `op_o1_vibreur`, `op_o2_acquis`, `op_o2b_retard`, `op_o3_periodique`)

- Ouverture : la source vibre sans arrêt ; chaque point du milieu recommence le même mouvement.
- Rappels (chapitre 1) : v = d/Δt ; τ = SM/v ; photo y(x) = le milieu à un instant ; film y_M(t) = un point.
- Définition : un phénomène périodique se reproduit identique à lui-même à intervalles de temps égaux ; cette durée est la période.

**I. La période et la fréquence**

Bloc `op_s1_b2` — Onde périodique, sinusoïdale, et la période T (diapositives : `op_o4_definition`, `op_pr1_sinusoide`, `op_o5_sinusoidale`, `op_t1_periode`)

- Définition : une onde progressive est périodique si la perturbation se répète, identique à elle-même, à intervalles de temps égaux.
- Rappel : une sinusoïde est une courbe qui monte et descend régulièrement ; le même motif se répète.
- Définition : une onde périodique est sinusoïdale si l'élongation de chaque point est une fonction sinusoïdale du temps.
- À un instant, la corde a la forme d'une sinusoïde : crêtes, creux ; amplitude = élongation maximale.
- I.1 Définition : la période T est la plus petite durée au bout de laquelle un point du milieu se retrouve dans le même état vibratoire (T en s).
- Attention : même état = même position et même sens de mouvement ; T se lit entre deux crêtes voisines.
- 🖉 *courbe* « Le film d'un point : la période T » — Entre deux crêtes voisines, M revient dans le même état (même position, même sens) : T = 0,5 s.

Bloc `op_s1_b3` — Même période partout, et la fréquence N = 1/T (diapositives : `op_t2_meme_periode`, `op_t3_frequence`, `op_t4_inverse`)

- I.2 Tous les points du milieu vibrent avec la même période T, celle de la source.
- I.3 Définition : la fréquence N est le nombre de périodes effectuées en une seconde ; N en hertz (Hz).
- N = 1/T (T en s, N en Hz), car en une seconde le point fait 1/T périodes.
- Exemple : T = 0,5 s → N = 1/0,5 = 2 Hz. Remarque : certains livres notent N par f ou ν.


### Séance 2 — Lire T, puis la longueur d'onde λ

Bloc `op_s2_b1` — Convertir, lire T sur le film et sur l'oscillogramme (diapositives : `op_t5_convertir`, `op_t6_film`, `op_t7_oscillo`)

- I.4 Convertir avant de calculer : 1 ms = 10⁻³ s ; 1 µs = 10⁻⁶ s ; 1 cm = 10⁻² m ; 1 mm = 10⁻³ m.
- I.5 Méthode (film y_M(t)) : T entre deux points voisins dans le même état (deux crêtes voisines).
- Méthode (oscillogramme) : T = n × S_H (n divisions, sensibilité horizontale S_H), en s ; puis N = 1/T.
- Attention : toujours écrire l'unité (« T = 5 » est faux).

**II. La longueur d'onde**

Bloc `op_s2_b2` — Périodique non sinusoïdale, puis la longueur d'onde λ (diapositives : `op_t8_non_sinusoidale`, `op_l1_photo`, `op_l2_lambda`, `op_l3_axe`)

- I.6 Une onde périodique n'est pas toujours sinusoïdale (instrument) ; T entre deux motifs identiques voisins.
- II.1 Sur la photo de la corde, le même motif se répète le long du milieu : périodicité spatiale.
- II.2 Définition : la longueur d'onde λ est la plus petite distance séparant deux points du milieu dans le même état vibratoire (λ en m).
- II.3 Double périodicité : sur y_M(t) (axe en s) on lit T ; sur y(x) (axe en m) on lit λ.
- Attention : lire l'axe avant de mesurer ; λ se lit de crête à crête voisine, pas jusqu'au front.
- 🖉 *courbe* « Instrument : onde périodique non sinusoïdale » — Le même motif se répète, mais ce n'est pas une sinusoïde ; T entre deux motifs identiques voisins.
- 🖉 *courbe* « La photo de la corde : la longueur d'onde λ » — À un instant, le même motif se répète le long de la corde : de crête à crête voisine, λ = 0,5 m.

Bloc `op_s2_b3` — Les rides de la cuve : compter les intervalles (diapositives : `op_l4_rides`, `op_l5_intervalles`, `op_l6_source`)

- II.4 Cuve à ondes vue de dessus : chaque trait clair est une crête ; deux traits voisins sont distants de λ.
- Pointe → onde circulaire ; réglette → onde rectiligne (sans amortissement ni réflexion).
- II.5 Méthode : 1) distance réelle d (avec l'échelle) ; 2) compter n intervalles, pas les traits ; 3) λ = d/n.
- Exemple : 4 traits = 3 intervalles ; d = 4,5 cm → λ = 4,5/3 = 1,5 cm.
- II.6 La distance à la source se compte depuis S : compter tous les λ entre S et M.
- 🖉 *schema* « Cuve à ondes vue de dessus » — Chaque trait est une crête ; la règle couvre 4 traits mais 3 intervalles : λ = d/n = 4,5/3 = 1,5 cm.


### Séance 3 — λ = v · T, puis en phase ou en opposition

**III. La célérité : λ = v·T**

Bloc `op_s3_b1` — Pendant une période, l'onde avance de λ (diapositives : `op_c1_avance`, `op_c2_relation`, `op_c3_rediger`, `op_c4_photo_datee`)

- III.1 Pendant une période T, l'onde avance d'une longueur d'onde λ.
- III.2 λ = v·T et v = λ·N (milieu homogène ; λ en m, T en s, N en Hz, v en m/s).
- Attention : λ en m avant de multiplier (λ = 4 cm, N = 50 Hz : v = 0,04 × 50 = 2 m/s, pas 200).
- Remarque : d'un milieu à l'autre, N ne change pas (imposée par la source) ; v et λ = v/N changent.
- III.3 Rédiger : relation → conversion en SI → application numérique → résultat avec unité.
- III.4 Photo datée : front à n·λ de la source à la date t → t = n·T.

**IV. En phase, en opposition de phase**

Bloc `op_s3_b2` — En phase, en opposition de phase (diapositives : `op_p1_en_phase`, `op_p2_opposition`, `op_p3_methode`, `op_p4_troisieme`)

- IV.1 Deux points vibrent en phase si leur distance est un nombre entier de λ : d = k·λ (k ∈ ℕ*).
- IV.2 Ils vibrent en opposition de phase si d = (2k + 1)·λ/2 (k ∈ ℕ) : l'un monte quand l'autre descend.
- IV.3 Méthode : 1) d et λ dans la même unité ; 2) calculer d/λ ; 3) entier → en phase ;
- entier et demi → opposition de phase ; sinon (ex. 2,25) → ni l'un ni l'autre ; 4) conclure par une phrase.
- IV.4 Le n-ième point en opposition de phase avec S : k = n − 1. Exemple : λ = 2 cm, 3e point : SM = 5λ/2 = 5 cm.
- 🖉 *courbe* « En phase, en opposition de phase » — M et P (d = λ) vibrent en phase ; M et Q (d = λ/2) vibrent en opposition de phase.

**V. Mesurer λ et la célérité**

Bloc `op_s3_b3` — Le stroboscope et les deux récepteurs (diapositives : `op_m1_strobo`, `op_m2_immobile`, `op_m3_recepteurs`)

- V.1 Le stroboscope éclaire la cuve par des éclairs très brefs : chaque éclair donne une « photo ».
- V.2 Immobilité apparente si N = k·N_e (N_e : fréquence des éclairs, k entier non nul).
- La plus grande fréquence des éclairs qui fige l'onde est N_e = N ; on mesure λ sur l'image figée.
- V.3 Deux récepteurs côte à côte : courbes en phase ; récepteur éloigné : courbe décalée et plus petite.


### Séance 4 — Mesurer λ, diffraction, milieu dispersif

Bloc `op_s4_b1` — Mesurer T et λ avec deux récepteurs (diapositives : `op_m4_microsecondes`, `op_m5_premier_retour`, `op_m6_nieme`, `op_m6b_deja_ecartes`)

- V.4 Lire le préfixe de S_H (µs ≠ ms). Exemple : T = 5 × 5 µs = 25 µs ; N = 1/T = 40 kHz (ultrason).
- V.5 En phase : maximums aux mêmes instants ; opposition : l'une maximale quand l'autre est minimale.
- Au premier retour en phase des deux courbes, le récepteur a été déplacé de λ.
- V.6 Méthode : 1) compter n retours en phase ; 2) déplacement d = n·λ, donc λ = d/n ; 3) v = λ·N.
- Récepteurs déjà écartés au départ : seul le déplacement compte, λ = (d₂ − d₁)/n.

**VI. La diffraction**

Bloc `op_s4_b2` — La diffraction (diapositives : `op_d1_ouverture`, `op_d2_invariants`, `op_d3_justifier`)

- VI.1 Diffraction : une onde qui rencontre une ouverture (ou un obstacle) de petite dimension repart en ondes circulaires centrées sur l'ouverture.
- Ouverture large : l'onde passe sans changer de forme (onde diaphragmée). La diffraction est propre aux ondes.
- VI.2 L'onde diffractée garde la même N (source), la même v (même milieu), donc la même λ = v/N.
- VI.3 Méthode : 1) a et λ dans la même unité ; 2) a ≤ λ → diffraction, d'autant plus marquée que a est petite.
- Dessin : arcs de cercle centrés sur l'ouverture, espacés de λ.
- 🖉 *schema* « Diffraction par une ouverture (a ≤ λ) » — a ≤ λ : derrière l'ouverture, l'onde repart en arcs de cercle centrés sur l'ouverture, avec la même λ.

**VII. Milieu dispersif**

Bloc `op_s4_b3` — Le son se diffracte aussi ; milieu dispersif ou non (diapositives : `op_d4_ultrasons`, `op_s1_frequence`, `op_s2_air`, `op_s3_dispersif`)

- VI.4 Ultrasons (40 kHz) : λ = v/N = 340/(40 × 10³) = 8,5 mm ; fente a = 5 mm ≤ λ → R capte hors de l'axe : diffraction.
- Son audible (20 Hz à 20 kHz) : λ = 340/N va de 1,7 cm à 17 m ; le son se diffracte par une porte.
- VII.1 Autre fréquence du vibreur : on remesure λ avant de recalculer v = λ·N.
- VII.2 Dans l'air, la célérité du son (≈ 340 m/s) ne dépend pas de la fréquence.
- VII.3 Définition : un milieu est dispersif si la célérité de l'onde dépend de sa fréquence (eau : oui ; air : non).
- Attention : λ = v/N dépend toujours de N ; « dispersif » veut dire que c'est v qui dépend de N.
- 🖉 *schema* « Diffraction d'une onde ultrasonore (a ≤ λ) » — R, déplacé sur un arc centré sur la fente, capte encore le signal hors de l'axe E-fente : l'onde est diffractée.


### Séance 5 — Le retard, les cas du bac, le bilan

**VIII. Le retard dans une onde périodique**

Bloc `op_s5_b1` — Le retard dans une onde périodique (diapositives : `op_r1_retard`, `op_r2_relation`, `op_r3_trois_lectures`, `op_r3b_calculs`)

- VIII.1 M commence à vibrer à la date τ = SM/v, dans le même sens que le premier mouvement de S.
- VIII.2 Onde non amortie : y_M(t) = y_S(t − τ) ; si SM = k·λ, τ = k·T : M vibre en phase avec S.
- VIII.3 Sur y_M(t) : τ = date où M commence à bouger ; T entre deux crêtes voisines ; amplitude = hauteur maximale.
- Attention : ne pas confondre τ (début du mouvement) et T (entre deux crêtes).
- VIII.4 Méthode : τ → v = SM/τ ; T → N = 1/T ; puis λ = v·T (tout en unités SI).
- Exemple : τ = 10 ms, T = 20 ms, SM = 2,5 cm → v = 2,5 m/s, N = 50 Hz, λ = 5 cm.
- 🖉 *courbe* « Trois lectures sur le film de M » — τ = 10 ms au début du mouvement, T = 35 − 15 = 20 ms entre deux crêtes voisines, amplitude 6 mm : ne pas confondre τ et T.

**IX. Cas types du bac**

Bloc `op_s5_b2` — La courbe de la source, deux cas du national (diapositives : `op_r4_source`, `op_x1_national_2017`, `op_x2_national_2020`)

- IX.1 Méthode (tracer y_S(t) à partir de y_M(t)) : même amplitude, même T, mais la courbe part de t = 0 (avance de τ).
- Le premier mouvement de M (vers le haut ou vers le bas) est celui de la source au départ.
- IX.2 National 2017 : λ = 4 cm (crête à crête) ; v = λ·N = 0,04 × 50 = 2 m/s ; t = SM/v = 0,06/2 = 30 ms.
- SM/λ = 6/4 = 1,5 → M et S en opposition de phase ; y_M(t) = y_S(t − 0,03) (jamais t + τ).
- IX.3 National 2020 : 1 cm couvre 2λ → λ = 0,5 cm ; N = v/λ = 0,25/(5 × 10⁻³) = 50 Hz ; τ = d/v = 0,2 s.

**X. Bilan du chapitre**

Bloc `op_s5_b3` — Le devoir sur la cuve, puis le bilan du chapitre (diapositives : `op_x3_devoir`, `op_b1_bilan`, `op_b2_carte`)

- IX.4 Devoir : AB = 3λ = 4,5 cm → λ = 1,5 cm ; v = λ·N = 0,3 m/s ; AB/λ = 3 → A et B en phase.
- À 30 Hz : v′ = λ′·N′ = 0,33 m/s ≠ v → milieu dispersif.
- En phase : d = k·λ (k ∈ ℕ*) ; opposition : d = (2k + 1)·λ/2 (k ∈ ℕ) ; retard : τ = SM/v, y_M(t) = y_S(t − τ).
- Mesures : T = n × S_H ; λ = d/n ; immobilité apparente N = k·N_e.
- Diffraction si a ≤ λ (même N, v, λ). Changement de milieu : N ne change pas. Milieu dispersif : v dépend de N.

