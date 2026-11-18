# Cahier de l'élève — Transformations lentes et transformations rapides (phys_ch9)

18 novembre 2026 (skill `cahier-de-l-eleve`). Le cahier idéal ci-dessous suit l'ordre de la copie **en attente** (`backend/data/courses/en_attente/phys_ch9_transformations_lentes_rapides.json`) ; le cours **en ligne** a un autre ordre (la mole, la concentration et l'avancement avant « rapide ou lente », pas d'exercice joué) : sa numérotation est donnée dans la table de découpage. Source des données : `scratchpad/phys_ch9/cahier_data.py` (appliqué par `appliquer.py`).

## Le cahier idéal (version en attente, lu d'un seul tenant)

**Transformations lentes et transformations rapides** (titre du cours, affiché par l'écran)

Les titres de partie (###) sont ceux que l'écran affiche déjà (`activities[].title`) : ils ne sont pas répétés dans `blocs[].cahier`. Les lignes numérotent les sous-titres (1., 2.) en continuant d'un bloc à l'autre dans la partie.


### Ouverture

*Bloc `tl_s0_b1` — La carte ; l’ion ; la conservation*

- Ion : atome qui a perdu ou gagné un ou plusieurs électrons.
- Ex. : Cu a perdu 2 e⁻ : Cu²⁺ (ion positif) ; I a gagné 1 e⁻ : I⁻ (ion négatif).
- Une équation conserve les éléments (mêmes atomes) et les charges (même charge totale).
- Ex. : Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s) : 1 Zn et 1 Cu de chaque côté ; charges +2 et +2.


### I. Oxydants et réducteurs

*Bloc `tl_s1_b1` — Le zinc dans les ions cuivre II : oxydant, réducteur, oxydation, réduction*

- 1. Zn dans une solution de Cu²⁺ : dépôt rouge de Cu, le bleu pâlit ; Zn cède 2 e⁻ à Cu²⁺.
- Définition : un oxydant est une espèce chimique capable de capter un ou plusieurs électrons.
- Définition : un réducteur est une espèce chimique capable de céder un ou plusieurs électrons.
- Réduction : gain d'électrons (l'oxydant) ; oxydation : perte d'électrons (le réducteur).
- 2. Couple Ox/Red : un oxydant et son réducteur conjugué ; demi-équation : Ox + n e⁻ ⇌ Red.
- Ex. : Cu²⁺(aq) + 2e⁻ ⇌ Cu(s) ; 2H⁺(aq) + 2e⁻ ⇌ H₂(g). Ici Zn est oxydé, Cu²⁺ est réduit.
- *[Dessin : Zinc dans les ions cuivre II — Chaque atome Zn cède 2 électrons à un ion Cu²⁺ : dépôt rouge de cuivre sur la lame, le bleu pâlit.]*


### II. Les demi-équations électroniques

*Bloc `tl_s1_b2` — Les demi-équations, un couple à la fois*

- Méthode (milieu acide) : 1) atomes autres que O et H ; 2) O avec H₂O ; 3) H avec H⁺ ;
- 4) charges avec e⁻, toujours du côté de l'oxydant ; puis on vérifie éléments et charges.
- MnO₄⁻(aq) + 8H⁺(aq) + 5e⁻ ⇌ Mn²⁺(aq) + 4H₂O(l) (charges : +2 et +2).
- H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l)
- I₂(aq) + 2e⁻ ⇌ 2I⁻(aq)


### III. L'équation d'oxydoréduction

*Bloc `tl_s1_b3` — L’équation d’oxydoréduction*

- Oxydoréduction : transfert d'électrons du réducteur d'un couple vers l'oxydant d'un autre.
- Méthode : (Ox₁ + n₁e⁻ ⇌ Red₁) × n₂ et (Red₂ ⇌ Ox₂ + n₂e⁻) × n₁, puis on additionne :
- n₂Ox₁ + n₁Red₂ → n₂Red₁ + n₁Ox₂ : aucun électron ; on simplifie H⁺ et H₂O des deux côtés.
- Ex. : MnO₄⁻(aq) + 5Fe²⁺(aq) + 8H⁺(aq) → Mn²⁺(aq) + 5Fe³⁺(aq) + 4H₂O(l)
- H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l) : couples H₂O₂/H₂O et I₂/I⁻.
- Attention : on vérifie les éléments et la charge totale des deux côtés (ici 0 et 0).


### IV. Transformations rapides et lentes

*Bloc `tl_s2_b1` — Rapide ou lente : deux durées*

- 1. Définition : une transformation rapide est achevée dès que les réactifs se rencontrent ;
- on ne peut suivre son évolution ni à l'œil nu ni avec les appareils de mesure courants.
- 2. Définition : une transformation lente dure de quelques secondes à plusieurs heures ;
- on suit son évolution à l'œil nu (couleur, trouble, gaz) ou avec un appareil de mesure.
- Ex. : rapides : MnO₄⁻ + Fe²⁺, Ag⁺(aq) + Cl⁻(aq) → AgCl(s) ; lentes : H₂O₂ + I⁻ (I₂ brun).


### V. Voir, classer, titrer

*Bloc `tl_s2_b2` — Classer ; le titrage, une réaction rapide utile*

- 1. Rapide (< 1 s) ; lente (secondes → heures) ; très lente (jours, années : la rouille).
- Remarque : le classement dépend des moyens d'observation ; on justifie par la durée.
- 2. Titrage du diiode : I₂(aq) + 2S₂O₃²⁻(aq) → 2I⁻(aq) + S₄O₆²⁻(aq), transformation rapide.
- Une réaction de titrage doit être rapide : chaque goutte réagit aussitôt.
- *[Dessin : L'échelle des durées — Rapide, lente ou très lente : le classement dépend des moyens d'observation.]*


### VI. Compter, puis la température, facteur cinétique

*Bloc `tl_s1_b4` — Compter et mesurer : la mole, la concentration*

- 1. Quantité de matière n en mole (mol) : 1 mol = 6,02·10²³ entités ; 1 mmol = 10⁻³ mol.
- 2. Concentration molaire : C = n/V (n en mol, V en L, C en mol/L).
- Ex. : 0,01 mol dans 100 mL : C = 0,01/0,100 = 0,1 mol/L.

*Bloc `tl_s2_b3` — Changer la température : l’expérience, puis le facteur cinétique*

- 3. La température — exp. 1) 20 °C, [I⁻]₀ = 0,1 mol/L ; 2) 40 °C, 0,1 ; 3) 40 °C, 0,2 mol/L.
- Exp. 1 et 2 : à 40 °C le brun fonce plus vite ; même brun final : même état final.
- Définition : un facteur cinétique est un paramètre capable de modifier la vitesse d'évolution
- d'une transformation, donc sa durée (température, concentration initiale des réactifs…).
- Donc la température est un facteur cinétique : plus elle est élevée, plus c'est rapide.
- Interprétation : au chaud, les entités s'agitent plus et se rencontrent plus souvent.


### VII. La concentration des réactifs

*Bloc `tl_s3_b1` — Les courbes au chaud ; la concentration, facteur cinétique*

- Courbes n(I₂) = f(t) : même palier (valeur finale) 2 mmol, vers 10 min à 40 °C, 30 min à 20 °C.
- Méthode : la courbe la plus raide au début correspond à la température la plus haute.
- 1. Concentration : à 20 °C, [I⁻]₀ = 0,2 mol/L brunit avant 0,1 mol/L ; même brun final.
- Donc plus la concentration initiale des réactifs est grande, plus c'est rapide.
- Interprétation : plus d'entités dans le même volume, plus de rencontres ; diluer ralentit.
- *[Dessin : n(I₂) à deux températures — Même palier (2 mmol) : même état final ; la courbe la plus raide au début, palier atteint le plus tôt, est à 40 °C.]*

*Bloc `tl_s3_b1b` — Le réactif limitant fixe le palier ; une variable à la fois*

- 2. Rappel : avancement x (mol) : n(H₂O₂) = n₀(H₂O₂) − x ; n(I⁻) = n₀(I⁻) − 2x ; n(I₂) = x.
- x_max : pour chaque réactif n₀ − a·x_max = 0 ; la plus petite valeur (réactif limitant).
- Ex. (V = 100 mL) : n₀(H₂O₂) = 2 mmol ; n₀(I⁻) = 0,1 × 0,100 = 10 mmol ; x_max = 2 mmol.
- Palier n(I₂) = x_max = 2 mmol (H₂O₂ limitant) ; doubler [I⁻]₀ (en excès) : même palier.
- Attention : doubler le réactif limitant H₂O₂ double le palier (4 mmol).
- 3. Méthode : comparer deux expériences qui ne diffèrent que par un paramètre (pas 1 et 3).
- *[Dessin : n(I₂) : I⁻ en excès, H₂O₂ limitant — Doubler [I⁻]₀ (en excès) : même palier 2 mmol, atteint plus tôt ; doubler H₂O₂ (limitant) : palier 4 mmol.]*


### VIII. Trempe, vie quotidienne et catalyseur

*Bloc `tl_s3_b2` — La trempe, la vie quotidienne et le catalyseur*

- 1. Trempe : prélèvement versé dans l'eau glacée ; refroidissement brusque et dilution :
- la transformation est bloquée (très ralentie) : on dose vite la quantité présente à t.
- 2. Le réfrigérateur ralentit, l'autocuiseur (eau à plus de 100 °C) accélère.
- 3. Définition : un catalyseur est une espèce chimique qui accélère une transformation ;
- il ne figure pas dans l'équation ; même état final. Ex. : S₂O₈²⁻ + 2I⁻, catalysée par Fe²⁺.
- Méthode : avec catalyseur, même palier x_f (avancement final), atteint plus tôt (2023 N).
- *[Dessin : Avec ou sans catalyseur — Même palier x_f = 0,3 mol (même état final) ; C₁ l'atteint plus tôt : C₁ est l'expérience avec catalyseur.]*


### IX. Un exercice type national, joué pas à pas

*Bloc `tl_np_b1` — Le sujet, les demi-équations, l’équation*

- Données : V = 100 mL ; n₀(H₂O₂) = 2 mmol ; [I⁻]₀ = 0,1 mol/L ; H⁺ en excès ; 20 et 40 °C.
- Méthode : lire le sujet deux fois (les données, puis ce qu'on cherche) avant tout calcul.
- 1) H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l) ; I₂(aq) + 2e⁻ ⇌ 2I⁻(aq).
- 2) 2 e⁻ cédés, 2 e⁻ captés : H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l).

*Bloc `tl_np_b2` — Le tableau d’avancement, ligne par ligne*

- 3) Tableau d'avancement en mmol, colonnes n(H₂O₂) | n(I⁻) | n(I₂) (H⁺ en excès) :
- État initial (x = 0) : 2 | 10 | 0 avec n₀(I⁻) = [I⁻]₀·V = 0,1 × 0,100 = 10⁻² mol.
- En cours (x) : 2 − x | 10 − 2x | x
- État final (x_max) : 2 − x_max | 10 − 2x_max | x_max
- 4) 2 − x_max = 0 → 2 mmol ; 10 − 2x_max = 0 → 5 mmol ; x_max = 2 mmol : H₂O₂ limitant.

*Bloc `tl_np_b3` — Suivre n(I₂), la température, le même état final*

- 5) Suivi : d'après le tableau, n(I₂) = x ; à la fin n(I₂) = x_max = 2 mmol (le palier).
- 6) Seule la température change : (a) finit plus tôt, donc (a) est à 40 °C.
- 7) Même valeur finale : mêmes quantités initiales, même réactif limitant H₂O₂, même x_max.
- Attention : la température change la durée, pas l'état final.
- *[Dessin : Exercice : quelle courbe à 40 °C ? — Même valeur finale x_max = 2 mmol ; (a) l'atteint plus tôt : (a) est l'expérience à 40 °C.]*

*Bloc `tl_np_b4` — La trempe, la copie complète*

- 8) Trempe : eau glacée ; froid et dilution, deux facteurs cinétiques diminuent :
- la transformation devient très lente, on dose I₂ à cet instant.
- Méthode (copie) : à chaque calcul, relation, application numérique, résultat avec son unité.


### X. Deux sujets du national


### XI. Bilan du chapitre

*Bloc `tl_s3_b3` — Deux nationaux et le bilan*

- 2025 N : (a) exp. 3 (θ₂, catalyseur) ; (b) exp. 2 (θ₂) ; (c) exp. 1 (θ₁ < θ₂) ; même x_f.
- 2017 R, eau glacée : « bloquer la transformation avant le dosage » (« refroidir » : non).
- Attention : « agiter » n'est pas attendu ; facteurs : température, concentration, catalyseur.
- Bilan : couple → demi-équations → équation → rapide ou lente → facteurs cinétiques → trempe.
- Chapitre suivant : suivre l'avancement x(t) d'une transformation lente.


## Les dessins

| Dessin | Bloc (en ligne / en attente) | Diapo | Ce qu'il montre |
|---|---|---|---|
| Zinc dans les ions cuivre II | tl_s1_b1 / tl_s1_b1 | tl_x1_zinc | croquis gardé : Zn cède 2 e⁻ à Cu²⁺, dépôt de Cu |
| L'échelle des durées | tl_s2_b2 / tl_s2_b2 | tl_r5_echelle | croquis gardé : rapide / lente / très lente |
| n(I₂) à deux températures | tl_s2_b3 / tl_s3_b1 | tl_f4_courbes | n = 2(1 − e^(−t/τ)), τ = 6 min (20 °C) et 2 min (40 °C) : 1,99 mmol à 30 et 10 min |
| n(I₂) : I⁻ en excès, H₂O₂ limitant | tl_s3_b1 / tl_s3_b1b | tl_f7_palier | paliers 2 et 4 mmol |
| Avec ou sans catalyseur | tl_s3_b2 / tl_s3_b2 | tl_t4_courbes | même palier x_f = 0,3 mol, C₁ plus tôt (2023 N) |
| Exercice : quelle courbe à 40 °C ? | — / tl_np_b3 | tl_np7_temperature | **nouveau** : courbes (a) τ = 3 min et (b) τ = 10 min de la simulation, x_max = 2 mmol |

Pas de dessin pour les définitions, les demi-équations, le tableau d'avancement (écrit en lignes : un tableau dépasse 6 étiquettes), la trempe (expérience décrite en une ligne), les nationaux et le bilan.

## Table de découpage

### En ligne (`backend/data/courses/`)

| Bloc | Parties affichées | Diapos | Lignes du bloc (début) | Figures |
|---|---|---|---|---|
| `tl_s0_b1` | Ouverture | o1_carte, rp1_ion, rp2_conservation | 4 l. : « Ion : atome qui a perdu ou gagné un ou plusieurs électrons.… » | — |
| `tl_s1_b1` | I | x1_zinc, x2_oxydant, x3_couple, x3b_couple | 6 l. : « 1. Zn dans une solution de Cu²⁺ : dépôt rouge de Cu, le bleu… » | Zinc dans les ions cuivre II |
| `tl_s1_b2` | II | x4_oxygene, x5_charges, x6_eau, x6b_diiode | 5 l. : « Méthode (milieu acide) : 1) atomes autres que O et H ; 2) O … » | — |
| `tl_s1_b3` | III | x7_equation, x8_fer, x9_oxalique, x10_verifier | 6 l. : « Oxydoréduction : transfert d'électrons du réducteur d'un cou… » | — |
| `tl_s1_b4` | IV | rp3_mole, rp4_concentration, rp5_avancement | 6 l. : « 1. Pour compter : n en mol (1 mol = 6,02·10²³ entités ; 1 mm… » | — |
| `tl_s2_b1` | (suite) | r1_bechers, r2_rapide, r3_lente, r4_indices | 5 l. : « 2. Définition : une transformation rapide est achevée dès qu… » | — |
| `tl_s2_b2` | V, VI | r5_echelle, r6_classer, r7_titrage, r8_duree | 5 l. : « 1. Rapide (< 1 s) ; lente (secondes → heures) ; très lente (… » | L'échelle des durées |
| `tl_s2_b3` | (suite) | f1_facteur, f2_bains, f3_agitation, f4_courbes | 6 l. : « Définition : un facteur cinétique est un paramètre capable d… » | n(I₂) à deux températures |
| `tl_s3_b1` | VII | f5_concentre, f6_rencontres, f7_palier, f8_variable | 6 l. : « 1. À 20 °C, [I⁻]₀ = 0,2 mol/L brunit avant 0,1 mol/L ; même … » | n(I₂) : I⁻ en excès, H₂O₂ limitant |
| `tl_s3_b2` | VIII | t1_trempe, t2_vie, t3_catalyseur, t4_courbes | 6 l. : « 1. Trempe : prélèvement versé dans l'eau glacée ; refroidiss… » | Avec ou sans catalyseur |
| `tl_s3_b3` | IX, X | n1_lecture, n2_glacee, bl_fiche, cr_carte | 5 l. : « 2025 N : (a) exp. 3 (θ₂, catalyseur) ; (b) exp. 2 (θ₂) ; (c)… » | — |

### En attente (`backend/data/courses/en_attente/`)

| Bloc | Parties affichées | Diapos | Lignes du bloc (début) | Figures |
|---|---|---|---|---|
| `tl_s0_b1` | Ouverture | o1_carte, rp1_ion, rp2_conservation | 4 l. : « Ion : atome qui a perdu ou gagné un ou plusieurs électrons.… » | — |
| `tl_s1_b1` | I | x1_zinc, x2_oxydant, x3_couple, x3b_couple | 6 l. : « 1. Zn dans une solution de Cu²⁺ : dépôt rouge de Cu, le bleu… » | Zinc dans les ions cuivre II |
| `tl_s1_b2` | II | x4_oxygene, x5_charges, x6_eau, x6b_diiode | 5 l. : « Méthode (milieu acide) : 1) atomes autres que O et H ; 2) O … » | — |
| `tl_s1_b3` | III | x7_equation, x8_fer, x9_oxalique, x10_verifier | 6 l. : « Oxydoréduction : transfert d'électrons du réducteur d'un cou… » | — |
| `tl_s2_b1` | IV | r1_bechers, r2_rapide, r3_lente, r4_indices | 5 l. : « 1. Définition : une transformation rapide est achevée dès qu… » | — |
| `tl_s2_b2` | V | r5_echelle, r6_classer, r7_titrage | 4 l. : « 1. Rapide (< 1 s) ; lente (secondes → heures) ; très lente (… » | L'échelle des durées |
| `tl_s1_b4` | VI | rp3_mole, rp4_concentration | 3 l. : « 1. Quantité de matière n en mole (mol) : 1 mol = 6,02·10²³ e… » | — |
| `tl_s2_b3` | (suite) | r8_duree, f2_bains, f1_facteur, f3_agitation | 6 l. : « 3. La température — exp. 1) 20 °C, [I⁻]₀ = 0,1 mol/L ; 2) 40… » | — |
| `tl_s3_b1` | VII | f4_courbes, f5_concentre, f6_rencontres | 5 l. : « Courbes n(I₂) = f(t) : même palier (valeur finale) 2 mmol, v… » | n(I₂) à deux températures |
| `tl_s3_b1b` | (suite) | rp5_avancement, f7_palier, f8_variable | 6 l. : « 2. Rappel : avancement x (mol) : n(H₂O₂) = n₀(H₂O₂) − x ; n(… » | n(I₂) : I⁻ en excès, H₂O₂ limitant |
| `tl_s3_b2` | VIII | t1_trempe, t2_vie, t3_catalyseur, t4_courbes | 6 l. : « 1. Trempe : prélèvement versé dans l'eau glacée ; refroidiss… » | Avec ou sans catalyseur |
| `tl_np_b1` | IX | np0_sujet, np1_demi, np2_equation | 4 l. : « Données : V = 100 mL ; n₀(H₂O₂) = 2 mmol ; [I⁻]₀ = 0,1 mol/L… » | — |
| `tl_np_b2` | (suite) | np3_initial, np4_encours, np5_limitant | 5 l. : « 3) Tableau d'avancement en mmol, colonnes n(H₂O₂) | n(I⁻) | … » | — |
| `tl_np_b3` | (suite) | np6_suivi, np7_temperature, np8_final | 4 l. : « 5) Suivi : d'après le tableau, n(I₂) = x ; à la fin n(I₂) = … » | Exercice : quelle courbe à 40 °C ? |
| `tl_np_b4` | (suite) | np9_trempe, np10_copie | 3 l. : « 8) Trempe : eau glacée ; froid et dilution, deux facteurs ci… » | — |
| `tl_s3_b3` | X, XI | n1_lecture, n2_glacee, bl_fiche, cr_carte | 5 l. : « 2025 N : (a) exp. 3 (θ₂, catalyseur) ; (b) exp. 2 (θ₂) ; (c)… » | — |

### Diapo → bulle (identique dans les deux versions ; `concentration.cahier`, 1 ou 2 lignes séparées par un saut de ligne)

| Diapo | Bulle | Figure |
|---|---|---|
| `tl_o1_carte` | Au programme : rappels d'oxydoréduction (couple Ox/Red, demi-équation, équation) ; / rapide ou lente ; facteurs cinétiques (température, concentration, catalyseur) ; trempe. | — |
| `tl_rp1_ion` | Ion : atome qui a perdu ou gagné un ou plusieurs électrons. / Ex. : Cu a perdu 2 e⁻ : Cu²⁺ (ion positif) ; I a gagné 1 e⁻ : I⁻ (ion négatif). | — |
| `tl_rp2_conservation` | Une équation conserve les éléments (mêmes atomes) et les charges (même charge totale). / Ex. : Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s) : charges +2 et +2. | — |
| `tl_x1_zinc` | Zn dans une solution de Cu²⁺ : dépôt rouge de cuivre, le bleu pâlit. / Chaque atome Zn cède 2 électrons à un ion Cu²⁺ : il se forme Cu(s) et Zn²⁺(aq). | Zinc dans les ions cuivre II |
| `tl_x2_oxydant` | Oxydant : espèce chimique capable de capter un ou plusieurs électrons (ici Cu²⁺). / Réducteur : espèce chimique capable de céder un ou plusieurs électrons (ici Zn). | — |
| `tl_x3_couple` | Réduction : gain d'électrons (par l'oxydant). / Oxydation : perte d'électrons (par le réducteur). | — |
| `tl_x3b_couple` | Couple Ox/Red : un oxydant et son réducteur conjugué ; demi-équation : Ox + n e⁻ ⇌ Red. / Ex. : Cu²⁺(aq) + 2e⁻ ⇌ Cu(s) ; Zn²⁺(aq) + 2e⁻ ⇌ Zn(s) ; 2H⁺(aq) + 2e⁻ ⇌ H₂(g). | — |
| `tl_x4_oxygene` | Méthode (milieu acide) : 1) atomes autres que O et H ; 2) O avec H₂O ; 3) H avec H⁺ ; 4) e⁻. / Étape 2 du permanganate : MnO₄⁻(aq) ⇌ Mn²⁺(aq) + 4H₂O(l). | — |
| `tl_x5_charges` | MnO₄⁻(aq) + 8H⁺(aq) + 5e⁻ ⇌ Mn²⁺(aq) + 4H₂O(l) / Charges : +7 à gauche, +2 à droite, donc 5e⁻ du côté de l'oxydant ; vérification : +2 et +2. | — |
| `tl_x6_eau` | H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l) / On vérifie toujours les éléments et les charges des deux côtés. | — |
| `tl_x6b_diiode` | I₂(aq) + 2e⁻ ⇌ 2I⁻(aq) (atomes, puis charges ; les électrons du côté de l'oxydant). | — |
| `tl_x7_equation` | Réduction de l'oxydant + oxydation du réducteur, même nombre d'électrons, on additionne : / Zn(s) + Cu²⁺(aq) → Zn²⁺(aq) + Cu(s) (aucun électron dans l'équation). | — |
| `tl_x8_fer` | (Ox₁ + n₁e⁻ ⇌ Red₁) × n₂ ; (Red₂ ⇌ Ox₂ + n₂e⁻) × n₁ : n₂Ox₁ + n₁Red₂ → n₂Red₁ + n₁Ox₂. / Fe²⁺ × 5 : MnO₄⁻(aq) + 5Fe²⁺(aq) + 8H⁺(aq) → Mn²⁺(aq) + 5Fe³⁺(aq) + 4H₂O(l). | — |
| `tl_x9_oxalique` | × 2 et × 5 (10 électrons), puis on simplifie les H⁺ (16 − 10 = 6) : / 2MnO₄⁻(aq) + 5H₂C₂O₄(aq) + 6H⁺(aq) → 2Mn²⁺(aq) + 10CO₂(aq) + 8H₂O(l). | — |
| `tl_x10_verifier` | H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l) : mêmes éléments, charges 0 et 0. / Lire les couples : espèces du même élément, l'oxydant d'abord : I₂/I⁻ et H₂O₂/H₂O. | — |
| `tl_r1_bechers` | Même oxydant MnO₄⁻ : décoloré aussitôt par Fe²⁺, en plusieurs minutes par H₂C₂O₄. / Donc les transformations chimiques n'ont pas toutes la même durée. | — |
| `tl_r2_rapide` | Définition : une transformation rapide est achevée dès que les réactifs se rencontrent ; / on ne peut suivre son évolution ni à l'œil nu ni avec les appareils de mesure courants. | — |
| `tl_r3_lente` | Définition : une transformation lente dure de quelques secondes à plusieurs heures ; / on peut suivre son évolution à l'œil nu ou avec un appareil de mesure. Ex. : H₂O₂ + I⁻. | — |
| `tl_r4_indices` | Indices : couleur (I₂ brun) ; trouble (S₂O₃²⁻(aq) + 2H⁺(aq) → S(s) + SO₂(aq) + H₂O(l)) ; / gaz (Zn(s) + 2H⁺(aq) → Zn²⁺(aq) + H₂(g)) ; sinon un conductimètre, un manomètre. | — |
| `tl_r5_echelle` | Rapide (< 1 s) ; lente (secondes → heures) ; très lente (jours, années : la rouille). / Remarque : le classement rapide / lente dépend des moyens d'observation. | L'échelle des durées |
| `tl_r6_classer` | On justifie par la durée : « lente, car son évolution dure plusieurs minutes ». / Attention : une transformation n'est pas lente parce qu'elle donne peu de produit. | — |
| `tl_r7_titrage` | Titrage : I₂(aq) + 2S₂O₃²⁻(aq) → 2I⁻(aq) + S₄O₆²⁻(aq), transformation rapide. / Une réaction de titrage doit être rapide : chaque goutte réagit aussitôt. | — |
| `tl_rp3_mole` | Quantité de matière n, en mole (mol) : 1 mol = 6,02·10²³ entités ; 1 mmol = 10⁻³ mol. | — |
| `tl_rp4_concentration` | Concentration molaire : C = n/V (n en mol, V en L, C en mol/L). / Ex. : 0,01 mol dans 100 mL : C = 0,01/0,100 = 0,1 mol/L. | — |
| `tl_r8_duree` | Exp. 1 : 20 °C, [I⁻]₀ = 0,1 mol/L ; exp. 2 : 40 °C, 0,1 mol/L ; exp. 3 : 40 °C, 0,2 mol/L. / Entre 1 et 2, seule la température change. | — |
| `tl_f2_bains` | À 40 °C, le brun fonce plus vite ; à la fin, même brun : même quantité de I₂. / Donc à température plus élevée, la transformation est plus rapide (même état final). | — |
| `tl_f1_facteur` | Définition : un facteur cinétique est un paramètre capable de modifier la vitesse / d'évolution d'une transformation, donc sa durée. Ex. : température, concentration. | — |
| `tl_f3_agitation` | Au chaud, les entités réactives s'agitent plus et se rencontrent plus souvent : / la transformation est plus rapide (même état final). | — |
| `tl_f4_courbes` | n(I₂) = f(t) : même palier 2 mmol ; atteint vers 10 min à 40 °C, vers 30 min à 20 °C. / La courbe la plus raide au début correspond à la température la plus élevée. | n(I₂) à deux températures |
| `tl_f5_concentre` | À 20 °C, [I⁻]₀ = 0,2 mol/L brunit avant 0,1 mol/L ; même brun final. / Donc la concentration initiale des réactifs est un facteur cinétique. | — |
| `tl_f6_rencontres` | Plus les réactifs sont concentrés, plus les entités se rencontrent souvent : / la transformation est plus rapide. Diluer ralentit. | — |
| `tl_rp5_avancement` | Avancement x : n(H₂O₂) = n₀(H₂O₂) − x ; n(I⁻) = n₀(I⁻) − 2x ; n(I₂) = x. / n₀(H₂O₂) = 2 mmol, n₀(I⁻) = 10 mmol : x_max = 2 mmol (et non 5), H₂O₂ limitant. | — |
| `tl_f7_palier` | H₂O₂ limitant : palier n(I₂) = x_max = 2 mmol ; doubler [I⁻]₀ (en excès) : même palier. / Attention : doubler H₂O₂ (le réactif limitant) double le palier : 4 mmol. | n(I₂) : I⁻ en excès, H₂O₂ limitant |
| `tl_f8_variable` | Méthode : on compare deux expériences qui ne diffèrent que par un seul paramètre. / 1 et 2 : la température ; 2 et 3 : la concentration ; 1 et 3 : on ne peut pas conclure. | — |
| `tl_t1_trempe` | Trempe : prélèvement versé dans l'eau glacée ; refroidissement brusque et dilution / bloquent la transformation : on dose vite, par S₂O₃²⁻, le I₂ présent à cet instant. | — |
| `tl_t2_vie` | Le réfrigérateur ralentit les transformations qui abîment les aliments ; / l'autocuiseur (eau au-dessus de 100 °C) accélère la cuisson. | — |
| `tl_t3_catalyseur` | Définition : un catalyseur est une espèce chimique qui accélère une transformation ; / il ne figure pas dans l'équation de la réaction ; l'état final est le même. | — |
| `tl_t4_courbes` | Même palier x_f = 0,3 mol ; C₁ l'atteint plus tôt : C₁ est l'expérience avec catalyseur. / Attention : ne pas choisir la courbe au palier le plus haut. | Avec ou sans catalyseur |
| `tl_np0_sujet` | Exercice : V = 100 mL ; n₀(H₂O₂) = 2 mmol ; [I⁻]₀ = 0,1 mol/L ; H⁺ en excès ; / on suit n(I₂) à 20 °C et à 40 °C. Méthode : lire le sujet deux fois. | — |
| `tl_np1_demi` | H₂O₂(aq) + 2H⁺(aq) + 2e⁻ ⇌ 2H₂O(l) ; I₂(aq) + 2e⁻ ⇌ 2I⁻(aq). | — |
| `tl_np2_equation` | 2I⁻(aq) ⇌ I₂(aq) + 2e⁻ : 2 e⁻ cédés, 2 e⁻ captés, on additionne : / H₂O₂(aq) + 2I⁻(aq) + 2H⁺(aq) → I₂(aq) + 2H₂O(l). | — |
| `tl_np3_initial` | État initial (x = 0) : n₀(H₂O₂) = 2 mmol ; n₀(I₂) = 0. / n₀(I⁻) = [I⁻]₀·V = 0,1 × 0,100 = 10⁻² mol = 10 mmol. | — |
| `tl_np4_encours` | En cours (x) : n(H₂O₂) = 2 − x ; n(I⁻) = 10 − 2x (coefficient 2) ; n(I₂) = x. | — |
| `tl_np5_limitant` | 2 − x_max = 0 donne 2 mmol ; 10 − 2x_max = 0 donne 5 mmol. / x_max = 2 mmol (la plus petite) : H₂O₂ est le réactif limitant, I⁻ est en excès. | — |
| `tl_np6_suivi` | D'après le tableau, n(I₂) = x ; à la fin, n(I₂) = x_max = 2 mmol. | — |
| `tl_np7_temperature` | Seule la température change : (a) atteint sa valeur finale plus tôt, / donc (a) est à 40 °C (la température est un facteur cinétique). | Exercice : quelle courbe à 40 °C ? |
| `tl_np8_final` | Mêmes quantités initiales : même réactif limitant H₂O₂, même x_max = 2 mmol. / La température change la durée, pas l'état final. | — |
| `tl_np9_trempe` | Trempe : prélèvement dans l'eau glacée ; la température et la concentration diminuent : / la transformation devient très lente, on dose I₂ à cet instant. | — |
| `tl_np10_copie` | Copie : demi-équations → équation → tableau (x_max = 2 mmol) → n(I₂) = x → (a) à 40 °C / → même état final → trempe. Chaque calcul : relation, application numérique, unité. | — |
| `tl_n1_lecture` | 2025 N : (a) ↔ exp. 3 (θ₂ et catalyseur) ; (b) ↔ exp. 2 (θ₂) ; (c) ↔ exp. 1 (θ₁). / « x_f est le même » : vrai, la température et le catalyseur ne changent que la durée. | — |
| `tl_n2_glacee` | 2017 R : eau glacée « pour bloquer la transformation avant le dosage » (« refroidir » : non). / Accélérer : élever la température, ajouter un catalyseur ; « agiter » n'est pas attendu. | — |
| `tl_bl_fiche` | Ox + n e⁻ ⇌ Red ; équation sans électrons ; rapide ou lente (durée) ; / facteurs cinétiques : température, concentration, catalyseur (même état final) ; trempe. | — |
| `tl_cr_carte` | Couple Ox/Red → demi-équations → équation → rapide ou lente → facteurs cinétiques → trempe. / Chapitre suivant : suivre l'avancement x(t) d'une transformation lente. | — |

Les 11 diapos `tl_np*` n'existent que dans la version en attente.

