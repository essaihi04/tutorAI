# Contrat des simulations — cours « Nombres complexes (première partie) » (math_ch6_nombres_complexes), 12 novembre 2026

Dossier des pages : `frontend/public/media/simulations/maths/operations-formes-tableau/`
(URL : `/media/simulations/maths/operations-formes-tableau/<page>.html?vue=<vue>`). Le cours cite EXACTEMENT les noms de vues,
de moments (`play_until`), de repères (`highlight`) et de paramètres ci-dessous : ne les renomme pas. On peut ajouter des moments
ou des repères en plus, jamais en retirer. Le moment `fin` est ajouté par le kit. Un repère porte le MÊME nom que le moment
du même dessin, sauf mention contraire (donc chaque moment ci-dessous est aussi un repère : `c.repere('<nom>', x, y, w, h, 'libellé')`).
`calculs.html` (+ `calculs-vues.js`, écrit par build.py) est déjà faite : n'y touche pas.

## Règles communes (toutes les pages)
- Forme : copie `maths/ln-tableau/produit.html` ou `maths/ln-tableau/courbe.html` (même `<head>`, même barre avec UN bouton
  `#run`, `data-professor-control="start reset pause resume play_until set_time"` + ` set_parameters` si la vue a des params,
  `<p class="bulle" id="feedback">`, scripts `shared/tableau/tableau.js` → `maths/commun/exposants.js` → `maths/commun/maths-tableau.js`,
  puis `professor-locate.js` defer). Lis l'en-tête de `maths/commun/maths-tableau.js` (API `MathsTableau.page`, aide `K`).
  Ne modifie PAS le kit ni les pages des autres cours ; s'il te manque une fonction (flèche, arc orienté…), écris-la dans ta page.
- Craie sur fond transparent, tout dans 760 × 420 ; RIEN sous y = 360 ; aucun texte hors cadre (`window.__horsCadre` doit
  rester vide). Écriture pas à pas : chaque moment = `K.marque('nom')` juste après ce qu'il montre ; `decrire` donne pour CHAQUE
  moment la phrase de ce qui se voit ; `explication` (repère → phrase).
- Texte au tableau en français ; apostrophe typographique ’ dans les chaînes JS ; prime écrit ’ (z’ : la police n'a pas ′) ;
  exposants ² ³ ⁿ (exposants.js) ; indices `_{A}` (z_{A} rendu zₐ par le kit ; jamais de « _ » visible).
- Le CONJUGUÉ : la barre combinante (z̄) n'est pas sûre dans la police : dessine la barre au trait au-dessus de la lettre
  (petite fonction `barre(c, x, y, largeur)`), ou écris « conj(z) » nulle part : toujours une barre dessinée.
- Plan complexe : axe horizontal légendé « axe réel », axe vertical « axe imaginaire », O, vecteurs u et v (petites flèches) ;
  repère orthonormé (même unité sur les deux axes). Arcs d'angle orientés avec une pointe de flèche. Angles écrits π/6, π/4…
- Seulement le programme : JAMAIS « corps », « inégalité triangulaire », « arctan », « plan d’Argand », « barycentre »,
  « similitude », « racine carrée d’un complexe », « Arg » (majuscule), « e^{iθ} » (exponentielle : partie 2), jamais [r ; θ].
- Couleurs du kit : blanc, cyan (points, vecteurs), jaune (résultat, affixe), vert (juste, partie réelle), rouge (barré, piège),
  orange (partie imaginaire, pointillés de projection), faible / tresfaible (axes, grille).
- Une vue avec `params` a des `poignees` (l'élève glisse un point du dessin) et une `lecture` (phrase des valeurs actuelles).
- Vérifie : `node --check` des scripts (ou `python outils/cours/notes/cours/maths_build/check_js.py <pages>`) ; serveur
  `python3 -m http.server 8898 -d frontend/public --bind 127.0.0.1` en arrière-plan pendant les tests, ARRÊTÉ ensuite ; puis
  `python3 outils/cours/notes/cours/maths_build/test_page.py [--shot <dossier du scratchpad>] <url…>` sur chaque vue (pas d'erreur,
  encre, moments et repères attendus, aucun hors cadre). Regarde une capture par vue (Read) puis efface-la.

## Carte des diapositives → visuels (pour les agents du cours)
o1 ouverture?vue=carte · o2 calculs · a1 nombre-i?vue=droite · a2 nombre-i?vue=quart · a3 plan?vue=placer · a4 plan?vue=purs ·
a5 calculs · a6 nombre-i?vue=cycle · c1–c4 calculs · p1 plan?vue=placer · p2 plan?vue=affixe · p3 vecteur?vue=vecteur ·
p4 vecteur?vue=milieu · j1 conjugue?vue=miroir · j2 calculs · j3 conjugue?vue=reel · j4 calculs · m1 module?vue=triangle ·
m2 module?vue=cercle · m3 calculs · m4 vecteur?vue=distance · g1 argument?vue=angle · g2 argument?vue=tour · g3 argument?vue=axes ·
g4 angles?vue=tableau · t1 trig?vue=passage · t2 calculs · t3 trig?vue=signes · t4 trig?vue=faux · t5 trig?vue=retour · t6 calculs ·
r1 produit?vue=carre · r2 produit?vue=fois_i · r3 produit?vue=inverses · r4 produit?vue=regle · r5 calculs · r6 moivre?vue=spirale ·
r7 moivre?vue=reel · r8 calculs · i1 alignement?vue=alignes · i2 conjugue?vue=distances · n1 calculs · n2 moivre?vue=national ·
b1 bilan.html · b2 carte.html

## GROUPE A — ouverture, nombre-i, plan, vecteur, conjugue

### ouverture.html (id `nc_ouverture`)
- vue `carte` — « Nombres complexes : la carte du chapitre ». Moments : `plan` (au centre, un petit plan complexe, un point M et
  « z = a + ib ») ; `questions` (autour, des bulles dans l'ordre du national : « forme algébrique », « quotient », « conjugué »,
  « module », « forme trigonométrique », « produit et puissance », « milieu, distance, alignement ») ; `frequences` (bandeau jaune en
  bas : « complexes : 20 sujets sur 20 ; forme trigonométrique : 17 sur 20 ») ; `partie2` (en pointillé, à droite : « partie 2 :
  équation, écriture exponentielle, rotation »). Repères : `plan`, `questions`, `frequences`, `partie2`.

### nombre-i.html (id `nc_nombre_i`)
- vue `droite` — « Aucun réel n’a un carré négatif ». Moments : `droite` (droite graduée de −3 à 3) ; `carres` (au-dessus de −3, −1,
  0, 2 : leurs carrés 9, 1, 0, 4, tous verts « ≥ 0 ») ; `bloque` (« x² = −1 » écrit, « aucun réel » en rouge, la ligne barrée).
- vue `quart` — « i : un quart de tour ». Moments : `demi_tour` (le point 2 fait un demi-tour autour de O et arrive en −2 : « × (−1) =
  demi-tour ») ; `quart_de_tour` (le point 1 tourne d'un quart de tour, sort de la droite, un axe vertical se dessine, le point est
  nommé i) ; `deux_quarts` (second quart : i arrive sur −1, « i × i = i² = −1 » encadré jaune) ; `solutions` (« x² = −1 : x = i ou
  x = −i », −i placé en bas).
- vue `cycle` — « Les puissances de i ». Params `n` {min 0, max 12, pas 1, defaut 4}. Moments : `un` (1 sur l'axe réel, « i⁰ = 1 ») ;
  `tours` (i¹ = i, i² = −1, i³ = −i, i⁴ = 1 placés l'un après l'autre par quarts de tour, une flèche courbe entre chacun) ;
  `cycle` (« tous les 4, on revient : i⁴ = 1 » encadré) ; `compteur` (le point se pose sur iⁿ pour n = valeur du paramètre,
  « iⁿ = … » écrit). Poignée `n` : le point courant.

### plan.html (id `nc_plan`)
- vue `placer` — « Un complexe, un point ». Params `a` {−4…4, pas 0.5, defaut 3}, `b` {−3…3, pas 0.5, defaut 2}. Moments :
  `axes` (axe réel, axe imaginaire, O, u, v) ; `placer` (3 + 2i : flèche « avancer de 3 » sur l'axe réel, puis « monter de 2 », le
  point M se pose, « M(3 ; 2) » et « z = 3 + 2i » à côté, 3 en vert, 2 en orange) ; `poignees` (M suit a et b, l'affixe
  a + ib se réécrit). Poignée : M.
- vue `affixe` — « L’affixe d’un point ». Moments : `axes` ; `point_a` (A(−2 ; 1) placé, « z_{A} = −2 + i » écrit en jaune) ;
  `origine` (O : « z_{O} = 0 ») ; `numero` (« l’affixe : le numéro du point » encadré).
- vue `purs` — « Réels et imaginaires purs ». Moments : `axes` ; `reels` (un point descend sur l'axe réel, b = 0, « réel » en vert
  le long de l'axe réel) ; `imaginaires` (un point glisse sur l'axe imaginaire, a = 0, « imaginaire pur » en orange) ; `zero`
  (O entouré : « 0 est les deux »).

### vecteur.html (id `nc_vecteur`)
- vue `vecteur` — « Affixe d’un vecteur : arrivée moins départ ». Moments : `deux_points` (A(1 + 2i), B(4 − i)) ; `vecteur`
  (flèche de A vers B, « z_{AB} = z_{B} − z_{A} ») ; `translate` (la flèche glisse jusqu'à O, son extrémité est le point 3 − 3i) ;
  `somme` (deux vecteurs OM et OM’ et leur somme : la diagonale du parallélogramme, « z + z’ »).
- vue `milieu` — « Le milieu de [AB] ». Moments : `deux_points` (A(1 + 2i), B(1 − 2i)) ; `segment` ([AB] tracé) ; `milieu`
  (P au milieu, « p = (a + b)/2 = 1 » en jaune).
- vue `distance` — « La distance AB = |z_{B} − z_{A}| ». Moments : `deux_points` (A(3 − 2i), B(1 + 4i)) ; `vecteur` (flèche AB,
  « b − a = −2 + 6i ») ; `translate` (la flèche glisse en O) ; `module` (« AB = |b − a| = √40 = 2√10 » encadré jaune).

### conjugue.html (id `nc_conjugue`)
- vue `miroir` — « Le conjugué : le reflet ». Params `a` {−4…4, pas 0.5, defaut 3}, `b` {−3…3, pas 0.5, defaut 2}. Moments :
  `point` (M(z), z = 3 + 2i) ; `miroir` (l'axe réel épaissi, M’ apparaît dessous : même abscisse, ordonnée opposée, « z̄ = 3 − 2i »
  avec la barre dessinée) ; `deplace` (M suit a et b, M’ suit en reflet). Poignée : M.
- vue `reel` — « z̄ = z : un réel ». Moments : `point` ; `miroir` ; `sur_l_axe` (M posé sur l'axe réel : M’ = M, « z̄ = z ⇔ z réel ») ;
  `somme` (M et M’ : « z + z̄ = 2a » lu sur l'axe réel, « z − z̄ = 2ib » en orange).
- vue `distances` — « ΩA = ΩB (2025 N) ». Moments : `points` (A(1 + 2i), B(1 − 2i) reflets l'un de l'autre) ; `omega` (Ω(5/2) sur
  l'axe réel) ; `egal` (les segments ΩA et ΩB, même longueur marquée d'un trait, « ΩA = ΩB = 5/2 »).

## GROUPE B — module, argument, angles, trig

### module.html (id `nc_module`)
- vue `triangle` — « Le module : une distance ». Moments : `point` (M(3 ; 4)) ; `triangle` (H projection sur l'axe réel, triangle
  rectangle OHM, côtés 3 et 4) ; `pythagore` (« OM² = 3² + 4² = 25 », « OM = 5 », « |z| » écrit sur l'hypoténuse, « |3 + 4i| = 5 »
  encadré jaune).
- vue `cercle` — « Même module, même cercle ». Moments : `cercle` (cercle de centre O de rayon 5) ; `autres` (M glisse sur −3 + 4i,
  5i, −5 : « |z| = 5 » reste) ; `sans_i` (« |a + ib| = √(a² + b²) : pas de i dans la racine » encadré, le « i² » d'une fausse écriture
  barré en rouge).

### argument.html (id `nc_argument`)
- vue `angle` — « L’argument : l’angle (u, OM) ». Params `t` {−180…180, pas 15, defaut 60, sens « angle en degrés »}. Moments :
  `point` (M sur un cercle de rayon 2) ; `angle` (arc orienté de u vers OM, « θ » écrit, « arg z ≡ θ [2π] ») ; `glisse` (M parcourt
  le cercle, θ suit, même module). Poignée : M (sur le cercle). La lecture donne θ en radians (fraction de π si possible).
- vue `tour` — « Un tour de plus : [2π] ». Moments : `point` ; `angle` (π/3) ; `tour` (M fait un tour complet : « π/3 + 2π = 7π/3 »,
  même point) ; `zero` (O entouré : « 0 n’a pas d’argument »).
- vue `axes` — « Réels et imaginaires purs ». Moments : `positif` (2 → 0) ; `negatif` (−3 → π) ; `haut` (2i → π/2) ; `bas`
  (−2i → −π/2) ; chaque angle écrit avec son arc.
- vue `projections` — « cos θ = a/r, sin θ = b/r ». Moments : `point` ; `projections` (pointillés orange vers les axes, « a = r cos θ »,
  « b = r sin θ ») ; `formules` (« cos θ = a/r ; sin θ = b/r » encadré).
- vue `quadrants` — « Les signes choisissent le quart ». Moments : `quatre` (les points √3 + i, −√3 + i, −√3 − i, √3 − i) ; `angles`
  (π/6, π − π/6 = 5π/6, −π + π/6 = −5π/6, −π/6 écrits près de chaque point) ; `signes` (dans chaque quart, les signes de a et b).

### angles.html (id `nc_angles`)
- vue `tableau` — « Le tableau des angles ». Moments : `cercle` (le premier quart du cercle avec 0, π/6, π/4, π/3, π/2) ; `valeurs`
  (sous chaque angle, cos et sin) ; `astuce` (√0/2, √1/2, √2/2, √3/2, √4/2 : monte pour le sinus, descend pour le cosinus) ;
  `lecture` (la colonne π/4 s'allume : cos = sin = √2/2). Repères aussi : `pi_6`, `pi_4`, `pi_3` (les trois colonnes).

### trig.html (id `nc_trig`)
- vue `passage` — « z = r(cos θ + i sin θ) ». Moments : `point` (√3 + i placé) ; `module` (OM = 2 tracé, « r = |z| = 2 ») ; `facteur`
  (« √3 + i = 2(√3/2 + (1/2)i) » écrit) ; `angle` (« √3/2 = cos π/6 ; 1/2 = sin π/6 », l'arc π/6 se dessine) ; `forme`
  (« = 2(cos π/6 + i sin π/6) » encadré jaune).
- vue `signes` — « −√3 + i : l’angle π − π/6 ». Moments : `point` (−√3 + i) ; `module` (r = 2) ; `facteur` (2(−√3/2 + (1/2)i)) ;
  `angle` (π − π/6 = 5π/6, arc) ; `forme` (« 2(cos 5π/6 + i sin 5π/6) »).
- vue `faux` — « Deux fausses formes ». Moments : `module_negatif` (« −2(cos π/3 + i sin π/3) » : le « −2 » entouré en rouge, « r > 0
  toujours ») ; `correction` (« = 2(cos 4π/3 + i sin 4π/3) » : le moins rentre dans l'angle, π + π/3) ; `moins_cos`
  (« 2(−cos θ + i sin θ) » barré, « = 2(cos(π − θ) + i sin(π − θ)) »).
- vue `retour` — « Retour à a + ib ». Moments : `forme` (« 2(cos 2π/3 + i sin 2π/3) ») ; `valeurs` (« cos 2π/3 = −1/2 ;
  sin 2π/3 = √3/2 ») ; `algebrique` (« = −1 + i√3 », encadré) ; `point` (le point se place, l'arc 2π/3).

## GROUPE C — produit, moivre, alignement, bilan, carte

### produit.html (id `nc_produit`)
- vue `carre` — « (1 + i)² : angles ajoutés, longueurs multipliées ». Moments : `facteur` (1 + i placé, |1 + i| = √2, angle π/4) ;
  `carre` (l'angle π/4 empilé deux fois : π/2 ; la longueur √2 × √2 = 2 ; le point 2i se pose) ; `verification` (« (1 + i)² = 2i »
  encadré jaune).
- vue `regle` — « Le produit : r × r’, θ + θ’ ». Params `t1` {0…180, pas 15, defaut 30}, `t2` {0…180, pas 15, defaut 45}. Moments :
  `deux` (z et z’ avec leurs angles θ et θ’) ; `regle` (le produit zz’ : les deux arcs bout à bout, θ + θ’, longueur rr’) ;
  `formules` (« |zz’| = |z|·|z’| ; arg(zz’) ≡ arg z + arg z’ [2π] » encadré). Poignées : les points z et z’.
- vue `fois_i` — « Multiplier par i : un quart de tour ». Moments : `point` (3 + i) ; `tourne` (le point tourne d'un quart de tour
  autour de O jusqu'à −1 + 3i, même longueur, arc π/2) ; `calcul` (« i(3 + i) = −1 + 3i »).
- vue `inverses` — « 1/z, z̄, z/z’ ». Moments : `point` (z = 2(cos π/3 + i sin π/3)) ; `conjugue` (z̄ : angle −π/3, même longueur) ;
  `inverse` (1/z : angle −π/3, longueur 1/2) ; `quotient` (« arg(z/z’) ≡ arg z − arg z’ » : on recule de θ’).

### moivre.html (id `nc_moivre`)
- vue `spirale` — « Moivre : la puissance multiplie l’angle ». Params `n` {1…8, pas 1, defaut 8}. Moments : `cercle` (sur le cercle
  unité : z = cos π/4 + i sin π/4, z², …, z⁸, l'angle avance de π/4) ; `spirale` (z = 1 + i : longueurs √2, 2, 2√2, 4…, les points
  s'écartent ; (1 + i)⁸ = 16 sur l'axe réel) ; `formule` (« [r(cos θ + i sin θ)]ⁿ = rⁿ(cos nθ + i sin nθ) » encadré). Poignée : le point zⁿ.
- vue `reel` — « Une puissance réelle ». Moments : `cercle` ; `reel` (les puissances qui tombent sur l'axe réel s'allument : « nθ
  multiple de π ⇒ zⁿ réel ») ; `imaginaire` (celles sur l'axe imaginaire : « nθ ≡ π/2 [π] ⇒ zⁿ imaginaire pur »).
- vue `national` — « 2024 N : b²⁴ ». Moments : `angle` (« b = (√6 + √2)(cos π/12 + i sin π/12) », l'angle π/12) ; `tour`
  (24 × π/12 = 2π : un tour complet, arc) ; `reel` (« b²⁴ = (√6 + √2)²⁴ : un réel » encadré).

### alignement.html (id `nc_alignement`)
- vue `alignes` — « Trois points alignés : un quotient réel ». Params `cx` {−4…4, pas 0.5, defaut 2}, `cy` {−3…3, pas 0.5, defaut 0.5}.
  Moments : `vecteurs` (A, B et les vecteurs AB et AC partant de A) ; `alignes` (C sur la droite (AB) : « (c − a)/(b − a) = k réel »,
  la valeur k s'affiche sur l'axe réel) ; `sort` (C tiré hors de la droite : le quotient quitte l'axe réel, « pas réel : pas alignés »).
  Poignée : C.
- vue `national` — « 2021 R : A, C, D ». Moments : `points` (A(3 + 2i), C(−1 − 2i), D(−3 − 4i)) ; `vecteurs` (c − a = −4 − 4i,
  d − a = −6 − 6i) ; `quotient` (« (d − a)/(c − a) = 3/2 : réel ») ; `conclusion` (la droite passe par les trois, « alignés » encadré).

### bilan.html (id `nc_b1_bilan`) — copie la forme de `maths/ln-tableau/bilan.html` (page 2 de l'élève avec lacunes, play_until par bloc)
8 blocs, moments `bloc1` … `bloc8` (repères du même nom) : 1 « i² = −1 ; z = a + ib » ; 2 « Quotient : × conjugué du bas » ;
3 « Affixes : z_{AB} = z_{B} − z_{A} ; milieu (a + b)/2 » ; 4 « Conjugué : reflet ; z·z̄ = a² + b² » ; 5 « Module : |z| = √(a² + b²) ;
AB = |b − a| » ; 6 « Argument et forme : r(cos θ + i sin θ), r > 0 » ; 7 « Produit, quotient, Moivre » ; 8 « Alignement :
(c − a)/(b − a) réel ». Moment `fiche` (tout écrit) avant `bloc1` ou à la fin, au choix, mais présent.

### carte.html (id `nc_b2_carte`) — copie la forme de `maths/ln-tableau/carte.html`
Moments : `centre` (un point M, ses deux écritures « a + ib » et « r(cos θ + i sin θ) » reliées par les flèches « module et
argument » / « cos et sin ») ; `branches` (autour : calcul algébrique, conjugué, module, argument, produit et Moivre, géométrie) ;
`partie2` (en pointillé : « écriture exponentielle », « équation du second degré », « rotation » — annoncés, rien de calculé).
Repères : `centre`, `branches`, `partie2`.
