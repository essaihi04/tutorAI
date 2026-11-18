# Cahier de l'élève — Nombres complexes (partie 1) · `math_ch6_nombres_complexes`

18 novembre 2026. Le cahier idéal du chapitre, d'un seul tenant, dans l'ordre de la copie en attente (chaque rappel
juste avant la notion qui s'en sert ; le cours en ligne a les cinq rappels au début, mêmes lignes). Les parties I à XI
sont celles du cours (`activities[].title`). Programme 2e Bac PC BIOF, partie 1 : forme algébrique, plan complexe,
conjugué, module, argument, forme trigonométrique, produit / quotient / Moivre, géométrie. L'écriture exponentielle,
l'équation du second degré et la rotation sont en partie 2 : rien ici. Notations du bac : AB⃗, z_{AB⃗}, z̄, |z|,
arg z ≡ θ [2π], (u⃗, AB⃗).

Source unique des lignes et des dessins : le script d'application
`/tmp/claude-0/-home-user-tutorAI/02f8f400-8fae-5359-a79d-1358639cc2d0/scratchpad/math_ch6_nombres_complexes/appliquer.py`
(`--md` régénère le texte ci-dessous, `--sec` affiche le découpage par bloc sans rien écrire).

---
Nombres complexes (partie 1) : chaque complexe z = a + ib est un point M du plan.  

## I. Le nombre i et la forme algébrique


**1.** Pour tout réel x, x² ≥ 0 : l'équation x² = −1 n'a pas de solution dans ℝ.  
Définition : i est un nombre complexe non réel tel que i² = −1 (× i : un quart de tour).  
Donc x² = −1 a deux solutions : x = i ou x = −i, car (−i)² = i² = −1.  

> 🖉 Figure — *i : un quart de tour* : Multiplier par i, c'est un quart de tour autour de O ; deux quarts de tour font un demi-tour : i² = −1.

Rappel : dans un repère, M(x ; y) : x est l'abscisse, y l'ordonnée ; (3 ; 2) ≠ (2 ; 3).  

**2.** Définition : tout complexe z s'écrit de façon unique z = a + ib, avec a et b réels.  
a = Re(z) partie réelle ; b = Im(z) partie imaginaire, un réel sans i : Im(3 − 5i) = −5.  
z réel ⇔ Im(z) = 0 ; z imaginaire pur (z ∈ iℝ) ⇔ Re(z) = 0 ; 0 est les deux ; ℝ ⊂ ℂ.  

**3.** Égalité : z = z′ ⇔ Re(z) = Re(z′) et Im(z) = Im(z′) ; a + ib = 0 ⇔ a = 0 et b = 0.  
Ex. (x, y réels) : (x − 2) + (y + 1)i = 5 − 3i ⇔ x = 7 et y = −4 (vérifier les deux).  

**4.** i² = −1, i³ = −i, i⁴ = 1 ; i²ᵏ = (−1)ᵏ et i²ᵏ⁺¹ = (−1)ᵏ·i (k ∈ ℕ). Ex. : i⁶ = −1.  
Rappel : (a + b)² = a² + 2ab + b² ; (a − b)(a + b) = a² − b² ; on développe terme à terme.  

## II. Calculer sous forme algébrique


**1.** Produit : développer, i² = −1, regrouper : (3 + i)(2 − i) = 6 − i − i² = 7 − i.  

**2.** (1 + i)² = 1 + 2i + i² = 2i ; (1 − i)² = −2i ; donc (1 + i)⁴ = (2i)² = −4.  

**3.** Conjugué : z̄ = a − ib ; (a + ib)(a − ib) = a² + b², un réel positif (pas a² − b²).  

**4.** Quotient (c + id ≠ 0) : multiplier haut et bas par c − id, conjugué du dénominateur.  
Ex. : (3 + i)/(1 + 2i) = (3 + i)(1 − 2i)/(1² + 2²) = (5 − 5i)/5 = 1 − i.  

## III. Le plan complexe : repère orthonormé direct (O, u⃗, v⃗)


**1.** z = a + ib (a, b réels) a pour image M(a ; b) : (Ox) axe réel, (Oy) axe imaginaire.  

> 🖉 Figure — *Le point M image de 3 + 2i* : Le complexe 3 + 2i a pour image le point M(3 ; 2) : partie réelle en abscisse, partie imaginaire en ordonnée.

M(a ; b) a pour affixe z_M = a + ib ; on note M(z_M). Ex. : A(−2 ; 1) : z_A = −2 + i.  
Rappel : le vecteur AB⃗ a pour coordonnées (x_B − x_A ; y_B − y_A) : arrivée moins départ.  

**2.** Affixe d'un vecteur : z_{AB⃗} = z_B − z_A (arrivée moins départ).  
Ex. : A(1 + 2i), B(4 − i) : z_{AB⃗} = (4 − i) − (1 + 2i) = 3 − 3i.  

**3.** Milieu I de [AB] : z_I = (z_A + z_B)/2. Ex. (2025 N) : a = 1 + 2i, b = 1 − 2i : p = 1.  

**4.** ABCD parallélogramme ⇔ AB⃗ = DC⃗ ⇔ z_B − z_A = z_C − z_D ⇔ z_A + z_C = z_B + z_D.  
(Deux vecteurs égaux ont la même affixe ; les diagonales ont le même milieu.)  
Ex. : z_M − z_O = 1 + 2i = z_B − z_{M′}, donc OM⃗ = M′B⃗ : OMBM′ est un parallélogramme.  

> 🖉 Figure — *OMBM′ : un parallélogramme* : z_M − z_O = 1 + 2i et z_B − z_{M′} = 1 + 2i : OM⃗ = M′B⃗, donc OMBM′ est un parallélogramme.


## IV. Le conjugué


**1.** z̄ = a − ib (a, b réels) : M′(z̄) est le symétrique de M(z) par rapport à l'axe réel.  

> 🖉 Figure — *Le conjugué : un reflet* : z̄ garde la partie réelle et change le signe de la partie imaginaire : M′(z̄) est le symétrique de M(z) par rapport à l'axe réel.


**2.** z̅+̅z̅′̅ = z̄ + z̄′ ; z̅z̅′̅ = z̄·z̄′ ; z̅ⁿ̅ = (z̄)ⁿ (n ∈ ℕ) ; le conjugué de z̄ est z.  
Pour z′ ≠ 0, le conjugué de z/z′ est z̄/z̄′ ; pour k réel, celui de kz est k·z̄.  

**3.** z réel ⇔ z̄ = z (M sur l'axe réel : M′ = M).  
z + z̄ = 2Re(z) (un réel) ; z − z̄ = 2i Im(z) ; z imaginaire pur ⇔ z̄ = −z.  
Ex. : z = 2 + 5i : z + z̄ = 4 et z − z̄ = 10i.  

**4.** z·z̄ = a² + b², un réel positif. Ex. (2020 N) : c = √2 + i√2 : c·c̄ = 2 + 2 = 4.  

**5.** Méthode (équation avec z̄) : poser z = x + iy (x, y réels), puis égaler Re et Im.  
Ex. : z + 2z̄ = 9 + i ⇔ 3x − iy = 9 + i ⇔ x = 3 et y = −1 : S = {3 − i}.  
Rappel (Pythagore) : OHM rectangle en H : OM² = OH² + HM² ; M(3 ; 4) : OM = √25 = 5.  

## V. Le module, la distance et les ensembles de points


**1.** Module de z = a + ib (a, b réels) : |z| = √(a² + b²) = OM. Ex. : |3 + 4i| = √25 = 5.  

> 🖉 Figure — *Le module : la distance OM* : |3 + 4i| = OM = √(3² + 4²) = 5 : Pythagore dans le triangle OHM rectangle en H.

Attention : pas de i sous la racine ; (−√3)² = 3 : |−√3 + i| = √(3 + 1) = 2.  

**2.** z·z̄ = |z|² ; |zz′| = |z|·|z′| : |(1 + i)(√3 + i)| = √2 × 2 = 2√2, sans développer.  
|z/z′| = |z|/|z′| (z′ ≠ 0) ; |zⁿ| = |z|ⁿ (n ∈ ℕ) ; |z̄| = |−z| = |z| ; |z| = 0 ⇔ z = 0.  
Attention : |z + z′| ≠ |z| + |z′| en général : |1 + (−1)| = 0 mais |1| + |−1| = 2.  

**3.** Distance : AB = |z_B − z_A|, le module de l'affixe de AB⃗.  
Ex. : a = 3 − 2i, b = 1 + 4i : AB = |−2 + 6i| = √(4 + 36) = √40 = 2√10.  

**4.** Ensembles de points M(z) : |z − z_A| = AM.  
|z − z_A| = r (r > 0) : le cercle de centre A et de rayon r.  
|z − z_A| = |z − z_B| (A ≠ B) : la médiatrice du segment [AB].  
Ex. : |2z − 4i| = 6 ⇔ 2|z − 2i| = 6 ⇔ |z − 2i| = 3 : cercle de centre A(2i), de rayon 3.  

> 🖉 Figure — *|z − 2i| = 3 : un cercle* : Tous les points M tels que AM = |z − 2i| = 3 : le cercle de centre A(2i) et de rayon 3.

Méthode (Z réel) : z = x + iy ; écrire Z sous forme algébrique ; Z ∈ ℝ ⇔ Im(Z) = 0.  
Ex. : Z = (1 + i)z − 2i = (x − y) + i(x + y − 2) : Z réel ⇔ y = −x + 2 (une droite).  
Rappel : cercle trigonométrique (rayon 1, un tour = 2π) : M(cos θ ; sin θ).  

## VI. L'argument


**1.** Pour z ≠ 0 d'image M : arg z ≡ (u⃗, OM⃗) [2π], en radians, dans le sens direct.  

> 🖉 Figure — *Module et argument* : L'argument θ est l'angle orienté (u⃗, OM⃗), dans le sens direct (inverse des aiguilles d'une montre) ; le module |z| est la longueur OM.

Un argument est défini à 2π près : θ et θ + 2kπ (k entier) donnent la même direction.  
Attention : 0 n'a pas d'argument ; toujours écrire [2π] : arg z ≡ π/3 [2π].  

**2.** Pour a > 0 et b > 0 : arg a ≡ 0 ; arg(−a) ≡ π ; arg(ib) ≡ π/2 ; arg(−ib) ≡ −π/2 [2π].  

**3.** z = a + ib ≠ 0, r = |z|, θ ≡ arg z [2π] : cos θ = a/r et sin θ = b/r.  
sin de 0, π/6, π/4, π/3, π/2 : √0/2, √1/2, √2/2, √3/2, √4/2 ; cos : la liste à l'envers.  
Ex. : cos θ = √2/2 et sin θ = √2/2 : θ ≡ π/4 [2π].  

## VII. La forme trigonométrique


**1.** Pour z ≠ 0 : z = r(cos θ + i sin θ), avec r = |z| > 0 et θ ≡ arg z [2π].  
Méthode : 1) r = |z| ; 2) z = r(a/r + i b/r) ; 3) lire θ dans le tableau ; 4) conclure.  
Ex. (2023 N) : a = √2 + i√2 : |a| = 2 ; a = 2(√2/2 + i√2/2) = 2(cos π/4 + i sin π/4).  

**2.** Le quart choisit l'angle (α : l'angle du tableau) : a < 0 et b > 0 : θ = π − α.  
Ex. : −√3 + i = 2(−√3/2 + (1/2)i) : α = π/6, donc θ = π − π/6 = 5π/6.  

> 🖉 Figure — *−√3 + i : l'angle π − π/6* : −√3 + i est en haut à gauche : on lit π/6 dans le tableau, puis θ = π − π/6 = 5π/6 ; le module vaut 2.

a < 0 et b < 0 : θ = π + α ; a > 0 et b < 0 : θ = −α. Attention : placer le point d'abord.  

> 🖉 Figure — *Les quatre quarts : α, π − α, π + α, −α* : Même α = π/6 lu dans le tableau ; les signes de a et de b placent le point : √3 + i (α), −√3 + i (π − α), −√3 − i (π + α), √3 − i (−α).


**3.** Attention : r > 0 et « cos θ + i sin θ » sans moins ; le moins rentre dans l'angle :  
cos(π + θ) = −cos θ, sin(π + θ) = −sin θ ; cos(π − θ) = −cos θ, sin(π − θ) = sin θ.  
−2(cos θ + i sin θ) = 2(cos(π + θ) + i sin(π + θ)) ;  
2(−cos θ + i sin θ) = 2(cos(π − θ) + i sin(π − θ)).  

**4.** Retour : a = r cos θ, b = r sin θ. Ex. : 2(cos 2π/3 + i sin 2π/3) = −1 + i√3.  
Ex. (2024 N) : |√3(1 − i)| = √3 × √2 = √6 ; √3(1 − i) = √6(cos(−π/4) + i sin(−π/4)).  

## VIII. Produit, quotient et Moivre (z et z′ non nuls)


**1.** |zz′| = |z|·|z′| et arg(zz′) ≡ arg z + arg z′ [2π] : modules ×, arguments +.  
Ex. : |1 + i| = √2, arg(1 + i) ≡ π/4 : (1 + i)² a pour module 2 et argument π/2 : c'est 2i.  
|iz| = |z| et arg(iz) ≡ arg z + π/2 [2π] : × i, un quart de tour autour de O.  

> 🖉 Figure — *Multiplier par i : un quart de tour* : i(3 + i) = −1 + 3i : même longueur √10, angle augmenté de π/2 ; le point tourne d'un quart de tour autour de O.


**2.** |z̄| = |z|, arg z̄ ≡ −arg z ; |1/z| = 1/|z|, arg(1/z) ≡ −arg z [2π].  
|z/z′| = |z|/|z′| ; arg(z/z′) ≡ arg z − arg z′ [2π] ; arg(−z) ≡ π + arg z [2π].  

**3.** Méthode « en déduire » (2017 N) : b = (1 + i)a, avec |a| = 2 et arg a ≡ π/6 :  
|b| = √2 × 2 = 2√2 ; arg b ≡ π/4 + π/6 ≡ 5π/12 [2π] (modules multipliés, pas ajoutés).  

**4.** Identification : b = (√3 − 1) + (√3 + 1)i = 2√2(cos 5π/12 + i sin 5π/12) ;  
parties réelles : 2√2 cos 5π/12 = √3 − 1, donc cos 5π/12 = (√6 − √2)/4.  

**5.** Moivre (n ∈ ℕ) : [r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ). Attention : rⁿ, pas r.  
Ex. : 1 + i = √2(cos π/4 + i sin π/4) : (1 + i)⁸ = (√2)⁸(cos 2π + i sin 2π) = 16.  
Méthode (zⁿ réel) : Moivre, réduire nθ ; sin nθ = 0 ⇒ zⁿ ∈ ℝ ; cos nθ = 0 ⇒ zⁿ ∈ iℝ.  
Ex. (2020 R) : a = cos π/4 + i sin π/4 : a²⁰²⁰ = cos 505π + i sin 505π = −1, un réel.  

## IX. Géométrie (A, B, C, D d'affixes a, b, c, d)


**1.** Pour A ≠ B : A, B, C alignés ⇔ (c − a)/(b − a) ∈ ℝ (même point A en haut et en bas).  
Rédaction : (d − a)/(c − a) = 3/2 ∈ ℝ, donc AC⃗ et AD⃗ colinéaires : A, C, D alignés.  

**2.** ΩA = |a − ω| = |−3/2 + 2i| = 5/2 et ΩB = |b − ω| = 5/2 : donc ΩA = ΩB (2025 N).  

> 🖉 Figure — *ΩA = ΩB = 5/2* : ΩA = |a − ω| = 5/2 et ΩB = |b − ω| = 5/2 : A et B sont à la même distance de Ω, sur le cercle de centre Ω et de rayon 5/2.


**3.** Angle orienté : pour A ≠ B, (u⃗, AB⃗) ≡ arg(z_B − z_A) [2π].  
Pour A ≠ B et A ≠ C : (AB⃗, AC⃗) ≡ arg((c − a)/(b − a)) [2π].  
Ce quotient imaginaire pur ⇔ (AB) ⊥ (AC) ; (AB⃗, CD⃗) ≡ arg((d − c)/(b − a)) [2π].  

**4.** Méthode (nature de ABC) : longueurs AB = |b − a|, AC, BC, et q = (c − a)/(b − a).  
q = i : |q| = 1 donne AC = AB ; arg q ≡ π/2 donne (AB) ⊥ (AC) : isocèle rectangle en A.  
AB = AC = BC : équilatéral (ex. a = 2, b = 1 + i√3, c = 3 + i√3 : trois côtés de 2).  

> 🖉 Figure — *Isocèle et rectangle en A* : a = 1 + i, b = 3 + 2i, c = 3i : (c − a)/(b − a) = i, donc AC = AB et (AB) ⊥ (AC).


## X. Deux sujets nationaux. 2023 N : a = √2 + i√2, b = 1 + √2 + i, c = b̄, d = 2i.

1) a = 2(cos π/4 + i sin π/4) ; 2) b − d = 1 + √2 + i − 2i = 1 + √2 − i = c.  
3) (√2 + 1)(b − a) = b − d avec b ≠ a, donc (b − d)/(b − a) = √2 + 1 ∈ ℝ.  
Donc AB⃗ et DB⃗ sont colinéaires : A, B et D sont alignés.  

> 🖉 Figure — *2023 N : A, B et D alignés* : b − d = c : DB⃗ = OC⃗ ; (b − d)/(b − a) = √2 + 1 est réel, donc la droite (DB) passe par A.

4) ac = 2b et c = b̄ : arg a + arg c ≡ arg b [2π] et arg c ≡ −arg b [2π] ;  
donc π/4 − arg b ≡ arg b, soit 2 arg b ≡ π/4 [2π].  
2024 N : b = (√6 + √2)(cos π/12 + i sin π/12) ; 24 × π/12 = 2π : b²⁴ = (√6 + √2)²⁴, réel.  

## XI. Bilan : recopie la fiche en 8 points, formules encadrées, pièges en orange.

Carte : au centre M et ses deux écritures a + ib et r(cos θ + i sin θ), puis les branches.  


---

## Les méthodes du national (où elles sont écrites)

| Cas type (fréquence 2016–2025) | Paragraphe |
|---|---|
| Forme algébrique d'un produit, d'un carré (13/20) | II.1, II.2 |
| Quotient sous forme algébrique (10/20) | II.4 |
| Égalité, déterminer x et y (devoirs) | I.3 ; équation avec z̄ : IV.5 |
| Conjugué (10/20) | IV.1 à IV.4 |
| Module, vérifier \|a\| = … (17/20) | V.1, V.2 ; \|λz\| = \|λ\|·\|z\| : VII.4 (2024 N) |
| Forme trigonométrique, vérifier un argument (17/20) | VII.1 (méthode en 4 temps), VII.2 (le quart), VII.3 (fausses formes) |
| Trigonométrique → algébrique (2/20) | VII.4 |
| Module et argument d'un produit, « en déduire » (6/20) | VIII.1 à VIII.3 |
| Identification, cos 5π/12 (2017 N) | VIII.4 |
| Puissance, zⁿ réel (6/20) | VIII.5 (Moivre + méthode) |
| Milieu (3/20) | III.3 |
| Distance, égalité de distances (10/20) | V.3, IX.2 |
| Alignement (9/20) | IX.1 (rédaction), X (2023 N) |
| Angle, orthogonalité, nature d'un triangle | IX.3, IX.4 |
| Ensembles de points (cercle, médiatrice, droite) | V.4 |

## Les dessins (tous en repère orthonormé : `ratio = (332·Δy/Δx + 52)/400`)

11 dessins gardés (vérifiés : valeurs, angles, échelle), 2 nouveaux :
- **Les quatre quarts** (`nc_t3_b`, bloc `nc_s3_b2b`) : ±√3 ± i, α = π/6 et ses trois corrections π − α, π + α, −α —
  le piège le plus fréquent du national (angle lu sans regarder les signes).
- **2023 N : A, B et D alignés** (`nc_n1` en ligne, `nc_n1_alignes` en attente ; bloc `nc_s4_b3`) : A(√2 + i√2),
  B(1 + √2 + i), D(2i) sur une même droite, et OC⃗ = DB⃗ (c = b − d). Vérifié : (b − d)/(b − a) = √2 + 1, ac = 2b,
  2 arg b = π/4.

## Découpage

Une ligne du cahier = une entrée `{"texte"}` du bloc ; la bulle de chaque diapositive (`concentration.cahier`) reprend ses propres lignes sans le titre de partie (1 à 2 lignes d'écran). Les figures du bloc sont celles de ses diapositives, dans l'ordre de `slide_ids`.

### Cours en ligne (`backend/data/courses/math_ch6_nombres_complexes.json`)

| Bloc | Diapositives | Lignes | Figures |
|---|---|---|---|
| `nc_s1_b0` | `o1`, `z1_repere`, `z2_vecteur`, `z3_pythagore` | 4 : « Nombres complexes (partie 1) : chaque … » → « Rappel (Pythagore) : OHM recta… » | — |
| `nc_s1_b1` | `z4_cercle`, `z5_identites`, `a1`, `a2` | 6 : « Rappel : cercle trigonométrique (rayon… » → « Donc x² = −1 a deux solutions … » | i : un quart de tour |
| `nc_s1_b2` | `a3`, `a4`, `a5`, `a6` | 6 : « 2. Définition : tout complexe z s'écri… » → « 4. i² = −1, i³ = −i, i⁴ = 1 ; … » | — |
| `nc_s1_b3` | `c1`, `c2`, `c3`, `c4` | 6 : « II. Calculer sous forme algébrique… » → « Ex. : (3 + i)/(1 + 2i) = (3 + … » | — |
| `nc_s2_b1` | `p1`, `p2`, `p3` | 5 : « III. Le plan complexe : repère orthono… » → « Ex. : A(1 + 2i), B(4 − i) : z_… » | Le point M image de 3 + 2i |
| `nc_s2_b1b` | `p4`, `p5` | 4 : « 3. Milieu I de [AB] : z_I = (z_A + z_B… » → « Ex. : z_M − z_O = 1 + 2i = z_B… » | OMBM′ : un parallélogramme |
| `nc_s2_b2` | `j1`, `j2`, `j3` | 5 : « IV. Le conjugué… » → « 3. z réel ⇔ z̄ = z (M sur l'ax… » | Le conjugué : un reflet |
| `nc_s2_b2b` | `j3_b`, `j4` | 3 : « z + z̄ = 2Re(z) (un réel) ; z − z̄ = 2… » → « 4. z·z̄ = a² + b², un réel pos… » | — |
| `nc_s2_b3` | `j5`, `m1`, `m2`, `m3` | 6 : « 5. Méthode (équation avec z̄) : poser … » → « 2. z·z̄ = |z|² ; |zz′| = |z|·|… » | Le module : la distance OM |
| `nc_s2_b3b` | `m3_b`, `m4` | 4 : « |z/z′| = |z|/|z′| (z′ ≠ 0) ; |zⁿ| = |z… » → « Ex. : a = 3 − 2i, b = 1 + 4i :… » | — |
| `nc_s2_b3c` | `m5`, `m6` | 6 : « 4. Ensembles de points M(z) : |z − z_A… » → « Ex. : Z = (1 + i)z − 2i = (x −… » | |z − 2i| = 3 : un cercle |
| `nc_s3_b1` | `g1`, `g2`, `g3` | 5 : « VI. L'argument… » → « 2. Pour a > 0 et b > 0 : arg a… » | Module et argument |
| `nc_s3_b1b` | `g4`, `g4_b` | 3 : « 3. z = a + ib ≠ 0, r = |z|, θ ≡ arg z … » → « Ex. : cos θ = √2/2 et sin θ = … » | — |
| `nc_s3_b2` | `t1`, `t2`, `t3` | 6 : « VII. La forme trigonométrique… » → « Ex. : −√3 + i = 2(−√3/2 + (1/2… » | −√3 + i : l'angle π − π/6 |
| `nc_s3_b2b` | `t3_b`, `t4` | 3 : « a < 0 et b < 0 : θ = π + α ; a > 0 et … » → « cos(π + θ) = −cos θ, sin(π + θ… » | Les quatre quarts : α, π − α, π + α, −α |
| `nc_s3_b3` | `t4_b`, `t5`, `t6` | 4 : « −2(cos θ + i sin θ) = 2(cos(π + θ) + i… » → « Ex. (2024 N) : |√3(1 − i)| = √… » | — |
| `nc_s3_b3b` | `r1`, `r2` | 4 : « VIII. Produit, quotient et Moivre (z e… » → « |iz| = |z| et arg(iz) ≡ arg z … » | Multiplier par i : un quart de tour |
| `nc_s4_b1` | `r3`, `r3_b`, `r4` | 4 : « 2. |z̄| = |z|, arg z̄ ≡ −arg z ; |1/z|… » → « |b| = √2 × 2 = 2√2 ; arg b ≡ π… » | — |
| `nc_s4_b1b` | `r5`, `r6` | 4 : « 4. Identification : b = (√3 − 1) + (√3… » → « Ex. : 1 + i = √2(cos π/4 + i s… » | — |
| `nc_s4_b2` | `r7`, `r8`, `i1`, `i2` | 6 : « Méthode (zⁿ réel) : Moivre, réduire nθ… » → « 2. ΩA = |a − ω| = |−3/2 + 2i| … » | ΩA = ΩB = 5/2 |
| `nc_s4_b2b` | `i3`, `i4` | 6 : « 3. Angle orienté : pour A ≠ B, (u⃗, AB… » → « AB = AC = BC : équilatéral (ex… » | Isocèle et rectangle en A |
| `nc_s4_b3` | `n1`, `n2`, `b1_bilan`, `b2_carte` | 6 : « X. Deux sujets nationaux. 2023 N : a =… » → « Carte : au centre M et ses deu… » | 2023 N : A, B et D alignés |

### Copie en attente (`backend/data/courses/en_attente/math_ch6_nombres_complexes.json`)

| Bloc | Diapositives | Lignes | Figures |
|---|---|---|---|
| `nc_s1_b0` | `o1`, `a1`, `a2` | 5 : « Nombres complexes (partie 1) : chaque … » → « Donc x² = −1 a deux solutions … » | i : un quart de tour |
| `nc_s1_b1` | `z1_repere`, `a3`, `a4` | 4 : « Rappel : dans un repère, M(x ; y) : x … » → « z réel ⇔ Im(z) = 0 ; z imagina… » | — |
| `nc_s1_b2` | `a5`, `a6`, `z5_identites`, `c1` | 6 : « 3. Égalité : z = z′ ⇔ Re(z) = Re(z′) e… » → « 1. Produit : développer, i² = … » | — |
| `nc_s1_b3` | `c2`, `c3`, `c4` | 4 : « 2. (1 + i)² = 1 + 2i + i² = 2i ; (1 − … » → « Ex. : (3 + i)/(1 + 2i) = (3 + … » | — |
| `nc_s2_b1` | `p1`, `p2`, `z2_vecteur`, `p3` | 6 : « III. Le plan complexe : repère orthono… » → « Ex. : A(1 + 2i), B(4 − i) : z_… » | Le point M image de 3 + 2i |
| `nc_s2_b1b` | `p4`, `p5` | 4 : « 3. Milieu I de [AB] : z_I = (z_A + z_B… » → « Ex. : z_M − z_O = 1 + 2i = z_B… » | OMBM′ : un parallélogramme |
| `nc_s2_b2` | `j1`, `j2`, `j3` | 5 : « IV. Le conjugué… » → « 3. z réel ⇔ z̄ = z (M sur l'ax… » | Le conjugué : un reflet |
| `nc_s2_b2b` | `j3_b`, `j4` | 3 : « z + z̄ = 2Re(z) (un réel) ; z − z̄ = 2… » → « 4. z·z̄ = a² + b², un réel pos… » | — |
| `nc_s2_b3` | `j5`, `z3_pythagore`, `m1` | 5 : « 5. Méthode (équation avec z̄) : poser … » → « 1. Module de z = a + ib (a, b … » | Le module : la distance OM |
| `nc_s2_b3b` | `m2`, `m3`, `m3_b`, `m4` | 6 : « Attention : pas de i sous la racine ; … » → « Ex. : a = 3 − 2i, b = 1 + 4i :… » | — |
| `nc_s2_b3c` | `m5`, `m6` | 6 : « 4. Ensembles de points M(z) : |z − z_A… » → « Ex. : Z = (1 + i)z − 2i = (x −… » | |z − 2i| = 3 : un cercle |
| `nc_s3_b1` | `z4_cercle`, `g1`, `g2`, `g3` | 6 : « Rappel : cercle trigonométrique (rayon… » → « 2. Pour a > 0 et b > 0 : arg a… » | Module et argument |
| `nc_s3_b1b` | `g4`, `g4_b` | 3 : « 3. z = a + ib ≠ 0, r = |z|, θ ≡ arg z … » → « Ex. : cos θ = √2/2 et sin θ = … » | — |
| `nc_s3_b2` | `t1`, `t2`, `t3` | 6 : « VII. La forme trigonométrique… » → « Ex. : −√3 + i = 2(−√3/2 + (1/2… » | −√3 + i : l'angle π − π/6 |
| `nc_s3_b2b` | `t3_b`, `t4` | 3 : « a < 0 et b < 0 : θ = π + α ; a > 0 et … » → « cos(π + θ) = −cos θ, sin(π + θ… » | Les quatre quarts : α, π − α, π + α, −α |
| `nc_s3_b3` | `t4_b`, `t5`, `t6` | 4 : « −2(cos θ + i sin θ) = 2(cos(π + θ) + i… » → « Ex. (2024 N) : |√3(1 − i)| = √… » | — |
| `nc_s3_b3b` | `r1`, `r2` | 4 : « VIII. Produit, quotient et Moivre (z e… » → « |iz| = |z| et arg(iz) ≡ arg z … » | Multiplier par i : un quart de tour |
| `nc_s4_b1` | `r3`, `r3_b`, `r4` | 4 : « 2. |z̄| = |z|, arg z̄ ≡ −arg z ; |1/z|… » → « |b| = √2 × 2 = 2√2 ; arg b ≡ π… » | — |
| `nc_s4_b1b` | `r5`, `r6` | 4 : « 4. Identification : b = (√3 − 1) + (√3… » → « Ex. : 1 + i = √2(cos π/4 + i s… » | — |
| `nc_s4_b2` | `r7`, `r8`, `i1`, `i2` | 6 : « Méthode (zⁿ réel) : Moivre, réduire nθ… » → « 2. ΩA = |a − ω| = |−3/2 + 2i| … » | ΩA = ΩB = 5/2 |
| `nc_s4_b2b` | `i3`, `i4` | 6 : « 3. Angle orienté : pour A ≠ B, (u⃗, AB… » → « AB = AC = BC : équilatéral (ex… » | Isocèle et rectangle en A |
| `nc_s4_b3` | `n1`, `n1_b`, `n1_alignes`, `n1_c` | 6 : « X. Deux sujets nationaux. 2023 N : a =… » → « donc π/4 − arg b ≡ arg b, soit… » | 2023 N : A, B et D alignés |
| `nc_s4_b4` | `n2`, `b1_bilan`, `b2_carte` | 3 : « 2024 N : b = (√6 + √2)(cos π/12 + i si… » → « Carte : au centre M et ses deu… » | — |

Particularités : en ligne, les cinq rappels sont écrits aux blocs `nc_s1_b0`–`nc_s1_b1` (avant leur usage) ; le sujet 2023 N tient en 3 lignes sur `nc_n1`. En attente, chaque rappel est dans le bloc de la notion, et 2023 N est écrit question par question (`nc_n1` → `nc_n1_c`, 6 lignes) ; 2024 N, bilan et carte forment `nc_s4_b4`. Le deuxième exemple de puissance (`nc_r8`, 2023 R) n'est que dans la bulle de sa diapositive (bloc `nc_s4_b2` plein).
