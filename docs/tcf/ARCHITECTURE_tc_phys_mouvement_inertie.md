# Architecture — « Le mouvement et le principe d'inertie » (`tc_phys_mouvement_inertie`, /TCF)

Tronc Commun Sciences option française, physique, d'après les chapitres « Le mouvement » et « Principe d'inertie » du
livre de l'utilisateur (résumé : `docs/tcf/CONTENU_LIVRE.md`). Un seul deck, deux grandes parties, préfixe `mi_`.
Simulations : `frontend/public/media/simulations/physics/tc_mouvement_inertie-tableau/` (kit `shared/tableau` +
`commun.js`, objet `window.Mvt`).

## Pourquoi cet ordre

1. **Prérequis d'abord, de zéro** (règle « départ de zéro ») : la force (4 caractéristiques), le poids P = m·g, la
   réaction, deux forces qui se compensent (expliquées deux fois : le livre sur la table, puis l'anneau tiré par deux
   dynamomètres), les coordonnées d'un vecteur, lire un graphique, la droite x = a·t + b. Ils servent plus loin :
   les coordonnées → OM⃗ ; la droite → x(t) du MRU ; les forces qui se compensent → pseudo-isolé.
2. **Le mouvement** dans l'ordre du livre : relativité (bus) → référentiel → repères d'espace (1, 2, 3 axes) et de
   temps → trajectoire → vitesse moyenne → enregistrement (table à coussin d'air) → vitesse instantanée → vecteur
   vitesse → MRU (tableau produit par l'animation, courbe point par point, pente = v, équation horaire, signe de v)
   → MCU (ω, T, f).
3. **Le principe d'inertie** : situation du curling → centre d'inertie (lancé en tournant : seul G en MRU) → G des
   corps symétriques → autoporteur en translation → inventaire P⃗ et R⃗ → isolé / pseudo-isolé → énoncé →
   référentiel galiléen (le bus) → méthode « appliquer le principe d'inertie » (grue), puis l'élève (seau du puits)
   → centre de masse (haltère), relation barycentrique, méthode du marteau, puis l'élève.
4. Bilan des deux parties (fiche), carte, fermeture.

Chaque méthode : montrée lentement par le tuteur sur un exemple, puis refaite par l'élève sur un autre (question au
tableau avec démonstration). Nombres simples : τ = 20 ms et 2 cm → v = 1 m/s (au lieu de 40 ms → 0,5 m/s) ;
l'application du livre garde τ = 50 ms → 0,4 m/s ; MCU du livre (R = 10 cm, v = 1 m/s, ω = 10 rad/s, T ≈ 0,63 s,
f ≈ 1,6 Hz) — π rend T non entier, on garde une décimale.

## Lexique visuel du cours (un objet, un seul dessin — `Mvt.P` et `Mvt.COUL` de `commun.js`)

| Objet | Dessin | Couleur / fonction |
|---|---|---|
| vecteur vitesse v⃗ | flèche épaisse | vert, `Mvt.vecteur(..., {couleur:'vert'})` |
| poids P⃗ | flèche de G vers le bas | rouge |
| réaction R⃗ | flèche au contact vers le haut | bleu |
| tension T⃗ | flèche le long du câble | orange |
| force F⃗ (rappel) | flèche | violet |
| vecteur position OM⃗ | flèche | rose |
| i⃗ j⃗ k⃗ | flèches courtes | cyan |
| centre d'inertie G | point rose cerclé | `P.G` |
| autoporteur | disque métal, éclateur A rouge au centre, éclateur B orange au bord | `P.autoporteur`, de côté `P.autoporteurCote` |
| table à coussin d'air | cadre métal, plateau bleu nuit, feuille claire quadrillée | `P.table` |
| point d'enregistrement | point jaune cerclé de sombre, nommé M₀, M₁… | `P.point` |
| règle | plastique jaune graduée en cm | `P.regle` |
| bus, personne, voiture, roue + valve rouge, ballon, grue, bloc de béton, seau, margelle, haltère (`P.masse`+`P.barre`), marteau | peints | `P.*` |

## Séances, blocs, diapos (simulation par diapo)

| Séance | Bloc | Diapos (vue) |
|---|---|---|
| 1 Les outils | b1 Force | ouverture_cours (aucune) · r1_force (forces?force) · r2_poids (forces?poids) ❓ |
| | b2 Compensation | r3_reaction (forces?reaction) · r3b_compense (forces?compense) ❓ |
| | b3 Maths | r4_vecteur (maths?vecteur) · r5_graphique (maths?lire) · r6_droite (maths?droite) ❓ |
| 2 Décrire un mouvement | b4 Relativité | m1_bus · m2_tableau · m3_referentiel ❓ (bus) |
| | b5 Repère d'espace | m4_axe · m5_plan · m6_espace ❓ (repere) |
| | b6 Temps, trajectoire | m7_temps · m8_trajectoire · m9_formes · m10_valve 👀❓ |
| 3 La vitesse | b7 Vitesse moyenne | v1_moyenne · v2_unites · v3_eleve ❓ (vitesse) |
| | b8 Enregistrement | e1_materiel · e2_enregistrement · e3_lire ❓ (table) |
| | b9 Vitesse instantanée | e4_instant · e5_comparer · e6_eleve ❓ (table) |
| 4 Le MRU | b10 Vecteur vitesse | e7_vecteur · e8_echelle · e9_eleve ❓ (vecteur) |
| | b11 Tableau et courbe | u1_tableau · u2_courbe · u3_pente ❓ (mru) |
| | b12 Équation horaire | u4_equation · u5_signe · u6_eleve ❓ (mru) |
| 5 MCU, centre d'inertie | b13 MCU | c1_circulaire · c2_omega · c3_periode ❓ (mcu) |
| | b14 Méthode MCU | c4_methode · c5_eleve ❓ (mcu) |
| | b15 Centre d'inertie | i1_curling · i2_rotation 👀 · i3_axes · i4_symetrie ❓ (inertie) |
| 6 Le principe d'inertie | b16 Principe | i5_translation · i6_forces · i7_isole · i8_enonce ❓ (inertie) |
| | b17 Galiléen, méthode | i9_galileen (bus) · i10_grue · i11_eleve ❓ (grue) |
| | b18 Centre de masse | g1_haltere · g2_relation · g3_marteau · g4_eleve ❓ (masse) |
| 7 Bilan | b19 Retenir | b1_bilan · b2_carte (bilan) |
| | fin | fermeture_cours (aucune) |

❓ = la question « À toi » du bloc (une par bloc, sur la dernière diapo) ; 👀 = question d'observation (2 dans le cours).

## Les vues nouvelles : moments et repères (contrat entre le cours et les simulations)

Les noms ci-dessous sont utilisés par `concentration.pointage` et `demonstration.lignes[].allume` : ne pas les changer.

### forces.html?vue=compense
Anneau tenu par deux dynamomètres tirés en sens contraires (5 N chacun). Moments : anneau 0,5 ; f1 2 ; f2 4 ;
droite 6 ; intensites 8 ; somme 10 ; fin 12. Repères : anneau, f1, f2, droite, dyn1, dyn2, somme.

### vecteur.html — le vecteur vitesse
- `caracteristiques` : trajectoire courbe d'un ballon, points M₀…M₆ ; en M₃ : origine (point), tangente (pointillés),
  sens du mouvement, valeur ; puis v⃗₃ vert. Moments : trajectoire 0,5 ; origine 2 ; direction 4 ; sens 6 ; valeur 8 ;
  vecteur 10 ; fin 12. Repères : trajectoire, M3, tangente, sens, v3.
- `echelle` (méthode) : enregistrement rectiligne (2 cm, τ = 20 ms), v₃ = 1 m/s ; échelle 1 cm ↔ 0,5 m/s ;
  longueur = 1/0,5 = 2 cm : 2 carreaux de 1 cm allumés un à un, puis v⃗₃ tracé depuis M₃. Moments : enreg 0,5 ;
  valeur 2 ; echelle 4 ; longueur 6 ; compte 8 ; trace 10 ; fin 12. Repères : M3, echelle, longueur, v3.
- `eleve` : points à 3 cm, v₄ = 1,5 m/s, même échelle → 3 cm. Moments : enreg 0,5 ; valeur 2 ; longueur 4 ; trace 6 ;
  fin 8. `conclusions:false` cache longueur et flèche. Repères : M4, v4, longueur.

### mru.html — le mouvement rectiligne uniforme (τ = 20 ms, 2 cm, v = 1 m/s)
- `tableau` : l'enregistrement M₀…M₇ ; origine des abscisses en M₀ (x = 0), origine des dates en M₂ (t = 0) ; pour chaque
  point, x (règle) et t s'allument puis volent dans le tableau t (ms) / x (cm) : t = −40, −20, 0, 20, 40, 60, 80, 100 ;
  x = 0, 2, 4, 6, 8, 10, 12, 14. Moments : enreg 0,5 ; origine_x 2 ; origine_t 3,5 ; remplir 5 (8 colonnes,
  0,7 s chacune) ; fin 11. Repères : M0, M2, tableau.
- `courbe` : axes t (ms) / x (cm), chaque couple du tableau devient un point (un par un), puis la droite.
  Moments : axes 0,5 ; points 2 (0,6 s par point) ; droite 7,5 ; fin 9. Repères : axes, droite.
- `pente` : sur la droite : b = x(0) = 4 cm ; deux points (0 ; 4) et (100 ; 14) ; Δx = 10 cm, Δt = 100 ms ;
  a = Δx/Δt = 0,10 m / 0,10 s = 1 m/s = v. Moments : b 0,5 ; points 2,5 ; dx 4,5 ; dt 6 ; pente 8 ; egal_v 10 ; fin 12.
  Repères : b, dx, dt, pente.
- `equation` : x(t) = v·t + x₀ ; x₀ = 0,04 m ; v = 1 m/s → x(t) = 1·t + 0,04 (m). Moments : relation 0,5 ; x0 2,5 ;
  v 4,5 ; equation 6,5 ; fin 8,5. Repères : relation, x0, v, equation.
- `signe` : le même mobile ; axe orienté dans le sens du mouvement → v_x = +1 m/s ; axe inversé → v_x = −1 m/s.
  Moments : axe1 0,5 ; vx_plus 2,5 ; axe2 5 ; vx_moins 7 ; regle 9 ; fin 11. Repères : axe1, axe2, regle.
- `eleve` (application du livre) : τ = 50 ms, points à 2 cm, M₀ origine des abscisses, M₂ origine des dates.
  v = 0,02/0,05 = 0,4 m/s ; x₀ = 4 cm ; x(t) = 0,4·t + 0,04. Moments : enreg 0,5 ; v 2 ; x0 4 ; equation 6 ; fin 8.
  `conclusions:false` cache v, x₀, l'équation. Repères : M0, M2, v, x0, equation.

### mcu.html — le mouvement circulaire uniforme
Autoporteur relié par un fil à un point fixe O de la table : il tourne ; points tous les τ = 20 ms, arcs de 2 cm, R = 10 cm.
- `circulaire` : les points se marquent sur un cercle, arcs égaux allumés un à un (comptés). Moments : lance 0,5 ;
  points 1 ; arcs 6 ; conclusion 9 ; fin 11. Repères : O, rayon, arc, trajectoire.
- `omega` : angle balayé Δθ pendant Δt ; ω = Δθ/Δt = v/R = 1/0,1 = 10 rad/s. Moments : rayon 0,5 ; angle 2 ;
  relation 4 ; calcul 6 ; fin 8. Repères : rayon, angle, relation.
- `periode` : un tour complet avec un chronomètre ; T = 2π/ω ; f = 1/T (tours par seconde). Moments : tour 0,5 ;
  T 4,5 ; relationT 6 ; f 8 ; relationf 9,5 ; fin 11. Repères : tour, chrono, T, f.
- `methode` : v = 0,02/0,02 = 1 m/s ; ω = v/R = 1/0,10 = 10 rad/s ; T = 2π/ω ≈ 0,63 s ; f = 1/T ≈ 1,6 Hz.
  Moments : donnees 0,5 ; v 2 ; omega 4 ; T 6 ; f 8 ; fin 10. Repères : donnees, v, omega, T, f.
- `eleve` : arcs de 3 cm, τ = 20 ms, R = 30 cm : v = 1,5 m/s ; ω = 5 rad/s ; T ≈ 1,26 s ; f ≈ 0,8 Hz.
  Moments : donnees 0,5 ; v 2 ; omega 3,5 ; T 5 ; f 6,5 ; fin 8. `conclusions:false` cache les résultats.

### inertie.html — le principe d'inertie
- `curling` : palet de granit glisse en ligne droite sur la glace à pas égaux (positions toutes les 0,5 s), P⃗ et R⃗
  se compensent. Moments : lance 0,5 ; glisse 1,5 ; positions 6 ; forces 8 ; question 10 ; fin 11,5.
  Repères : palet, positions, P, R.
- `rotation` : autoporteur lancé en tournant sur lui-même, deux éclateurs : A (centre, rouge) trace des points
  alignés à pas égaux ; B (bord, orange) trace des boucles. Moments : lance 0,5 ; trace 1 ; A 7 ; B 9 ; fin 11.
  `conclusions:false` : pas d'étiquette « droite / boucles » avant la réponse. Repères : A, B, traceA, traceB.
- `axes` : deux lancers sur deux faces ; l'axe de symétrie Δ₁ puis Δ₂ ; leur intersection G ; G seul toujours en MRU.
  Moments : delta1 0,5 ; delta2 3 ; G 5,5 ; mru 7,5 ; fin 10. Repères : delta1, delta2, G.
- `corps` : sphère, cylindre, disque, barre homogènes, leurs axes de symétrie, G au centre (un par un).
  Moments : sphere 0,5 ; cylindre 3 ; disque 5,5 ; barre 8 ; fin 10. Repères : sphere, cylindre, disque, barre.
- `translation` : autoporteur lancé sans rotation : A, B et G en MRU (trois lignes de points à pas égaux).
  Moments : lance 0,5 ; trace 1 ; mru 6 ; fin 8. Repères : A, B, G.
- `forces` : de côté, autoporteur sur la table : P⃗ (rouge, en G, vers le bas), R⃗ (bleue, au contact, vers le haut),
  même droite, même intensité : P⃗ + R⃗ = 0⃗. Moments : systeme 0,5 ; P 2 ; R 4 ; compense 6 ; pseudo 8 ; fin 10.
  Repères : systeme, P, R, somme.
- `isole` : à gauche une sonde loin de tout (aucune force : isolé, n'existe pas en pratique), à droite l'autoporteur
  (P⃗ + R⃗ = 0⃗ : pseudo-isolé). Moments : sonde 0,5 ; isole 2,5 ; autoporteur 5 ; pseudo 7 ; fin 9.
  Repères : sonde, autoporteur.
- `enonce` : deux cas : G au repos (v⃗_G = 0⃗) et G en MRU (v⃗_G constant, flèches vertes égales) ; l'énoncé écrit.
  Moments : repos 0,5 ; mru 3 ; enonce 6 ; fin 9. Repères : repos, mru, enonce.

### grue.html — appliquer le principe d'inertie
- `methode` : la grue monte un bloc de béton (m = 1 500 kg) à vitesse constante ; méthode en 4 étapes :
  1) système {bloc} ; 2) forces P⃗ (rouge) et T⃗ (orange) dessinées ; 3) mouvement de G : MRU → principe d'inertie
  dans le référentiel terrestre (galiléen) : P⃗ + T⃗ = 0⃗ ; 4) T = P = m·g = 1 500 × 10 = 1,5 × 10⁴ N.
  Moments : monte 0,5 ; systeme 3 ; forces 5 ; mru 7 ; principe 9 ; calcul 11 ; fin 13.
  Repères : bloc, P, T, systeme, calcul.
- `eleve` : un seau d'eau (m = 8 kg) monté à vitesse constante dans un puits (margelle) : T = P = 80 N.
  Moments : monte 0,5 ; forces 3 ; calcul 5 ; fin 7. `conclusions:false` cache T⃗ et le calcul.

### masse.html — le centre de masse
- `haltere` : deux masses égales en A₁ et A₂ ; C au milieu ; CA⃗₁ + CA⃗₂ = 0⃗ ; l'haltère posée sur un doigt en C
  tient en équilibre. Moments : haltere 0,5 ; masses 2 ; C 4 ; vecteurs 6 ; equilibre 8 ; fin 10.
  Repères : A1, A2, C, vecteurs.
- `relation` : relation barycentrique OG⃗ = (m₁·OG⃗₁ + m₂·OG⃗₂)/(m₁ + m₂), O quelconque ; tige à deux masses
  inégales : G près de la plus lourde. Moments : systeme 0,5 ; O 2 ; relation 4 ; G 6 ; fin 8. Repères : O, G1, G2, G.
- `marteau` (méthode) : manche m₁ = 100 g (centre G₁), tête m₂ = 400 g (centre G₂), G₁G₂ = 25 cm ; O en G₁ :
  G₁G⃗ = m₂·G₁G⃗₂/(m₁ + m₂) → G₁G = 400/500 × 25 = 20 cm. Moments : marteau 0,5 ; G1G2 2 ; O 4 ; relation 6 ;
  calcul 8 ; G 10 ; fin 12. Repères : G1, G2, G, calcul.
- `eleve` : tige légère, m₁ = 200 g en A, m₂ = 600 g en B, AB = 40 cm ; O en A : AG = 600/800 × 40 = 30 cm.
  Moments : systeme 0,5 ; relation 2 ; calcul 4 ; G 6 ; fin 8. `conclusions:false` cache le calcul et G.

### bilan.html — fiche et carte
`?vue=fiche` / `?vue=carte` : 9 blocs (C1…C9). Moments : prerequis 1 ; relativite 3 ; reperes 5 ; trajectoire 7 ;
vitesse 9 ; mru 11 ; mcu 13 ; inertie 15 ; masse 17 ; fin 19.
