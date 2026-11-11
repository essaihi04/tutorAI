# Contrat des simulations — cours « Limites et continuité » (math_ch1_limites_continuite)

Dossier : `frontend/public/media/simulations/maths/limites-continuite-tableau/`
Modèle à copier (forme, style, chargement des scripts) : `traversee.html` du même dossier (ne pas le modifier).
Kit : `../commun/maths-tableau.js` (lire son en-tête), `../commun/exposants.js`, `../commun/maths.css`, `/media/simulations/shared/tableau/tableau.js`.

## Règles communes (brief maths, à respecter à la lettre)
- `MathsTableau.page({id, titre, texte, vues})`, une vue par `?vue=…`, chaque vue : `titre`, `dessiner(c, K)`, `decrire` (une phrase par moment,
  ce qui se voit), `motifs` (libellé court de chaque arrêt sur image), `explication` (repère → phrase), `params` + `poignees` + `lecture`
  quand la vue a un réglage. Les MOMENTS ci-dessous sont des noms EXACTS (le cours les cite) : chacun marqué par `K.marque('nom')`
  juste après ce qui le montre, dans l'ordre donné. Les REPÈRES (c.repere(id,…)) sont des noms exacts aussi.
- Fond transparent, tout dans 760 × 420 ; rien d'écrit sous y = 360 (la barre du lecteur couvre le bas) ; aucun texte hors cadre
  (`window.__horsCadre` doit rester vide) ; étiquettes qui ne se chevauchent pas (même aux positions extrêmes des poignées).
- Apostrophe typographique ’ dans toutes les chaînes JS françaises. Texte au tableau en français. Indices avec `_` (le kit les rend,
  ex. `C_f`, `x_0`) ; exposants avec les caractères ² ³ ⁴ ⁻¹ ou `^{…}` (exposants.js) — ex. `C_f⁻¹`, `x^{p/q}`, `⁴√16`.
- Limites écrites comme au tableau : « lim » avec, dessous, en petit « x → 1 » (ou « x → 1⁺ ») ; écris une petite fonction locale
  `limite(c, x, y, sous, suite, o)` dans ta page pour ça.
- Seulement le programme : JAMAIS les mots bijection, injective, surjective, prolongement, epsilon, L’Hôpital, équivalent, Rolle,
  Heine, Bolzano, partie entière, Horner, Newton. Pas de racine d’un nombre négatif (on écrit −∛27, jamais ∛(−27)).
- La courbe est tracée en direct (`K.anime(durée, p => K.courbePart(…))`), les pointillés de lecture à la craie (`K.proj`),
  ronds vides pour les trous / bornes exclues (`K.rond(G, x, y, false)`).
- Un repère « égal » (même échelle en x et en y) quand il y a une symétrie par rapport à y = x : w/(xmax−xmin) = h/(ymax−ymin).
- Vérifier : `python …/maths_build/check_js.py <page>` puis
  `python …/maths_build/test_page.py --shot <dossier scratch> "/media/simulations/maths/limites-continuite-tableau/<page>.html?vue=<vue>"`
  pour CHAQUE vue (serveur déjà lancé sur http://127.0.0.1:8898) ; lire chaque capture avec Read (fond blanc à la capture =
  transparent dans le lecteur : la craie claire y est pâle, c’est normal) ; corriger chevauchements, débordements, textes coupés.
  « AUCUN PROBLÈME » attendu. Ne pas modifier le kit ni traversee.html ; ne rien toucher hors de tes pages.

## approche.html (limites lues sur une courbe)
- `trou` — f(x) = (x² − 1)/(x − 1) (= x + 1, trou en (1 ; 2)). Param `x_m` (0,2..1,8, pas 0,01, défaut 0,5 ; jamais 1) ; poignée : M sur la courbe.
  Moments : `courbe_tracee` (droite trouée, rond vide en (1 ; 2)) · `depart_gauche` (M en x = 0,5, coordonnées écrites) ·
  `proche_gauche` (M glisse à 0,9 puis 0,99 : « x = 0,99 → f(x) = 1,99 ») · `depart_droite` (M en 1,5) · `proche_droite` (1,01 → 2,01) ·
  `trou_vide` (cercle autour du trou, « f(1) n’existe pas ») · `limite_lue` (flèche vers 2 sur l’axe des ordonnées ; écrit
  « lim f(x) = 2 » avec « x → 1 » dessous). Repères : `trou`, `M`, `valeur_lue`, `limite`. lecture : x_M et f(x_M) (4 décimales).
- `trois_trous` — trois petits repères côte à côte : (x² − 1)/(x − 1) en 1 → 2 ; (x² − 4)/(x − 2) en 2 → 4 ; (√(x + 3) − 2)/(x − 1) en 1 → 1/4.
  Au-dessus de chacun le quotient, « en remplaçant : « 0/0 » », la courbe trouée, sa limite. Moments : `trou_1`, `trou_2`, `trou_3`,
  `trois_limites` (en bas : « « 0/0 » → 2, 4, 1/4 : trois limites différentes »). Repères : `cas1`, `cas2`, `cas3`, `conclusion`.
- `deux_cotes` — f(x) = 1/(x − 1). Moments : `repere_pose` · `monte_a_droite` (un point glisse sur la branche droite de x = 2 vers 1,1 puis
  1,01 ; valeurs 10, 100 écrites ; la branche monte) · `plonge_a_gauche` (de x = 0 vers 0,9 : −10 ; la branche plonge) · `tableau_signe`
  (petit tableau de signe de x − 1 : x | −∞ 1 +∞ ; x − 1 | − 0 + ; puis « 0⁻ » à gauche, « 0⁺ » à droite) · `limites_ecrites`
  (« lim 1/(x − 1) = +∞ » sous x → 1⁺ ; « = −∞ » sous x → 1⁻) · `asymptote_tracee` (droite x = 1 en pointillés, « x = 1 : asymptote
  verticale »). Repères : `branche_droite`, `branche_gauche`, `tableau_signe`, `asymptote`.

## infini.html (à l’infini)
- `ecart` — courbes y = √(x² + x) et y = x. Moments : `deux_courbes` (fenêtre [0 ; 12]) · `ecart_x10` (segment vertical entre les deux
  courbes en x = 10, « écart ≈ 0,488 ») · `ecart_x100` (la fenêtre se dézoome en direct vers [0 ; 120], segment en x = 100, « ≈ 0,499 ») ·
  `ecart_lu` (écrit : « √(x² + x) − x → 1/2 » sous « x → +∞ », avec lim). Repère `ecart`. Param `x` (1..110, défaut 10) + poignée (point sur
  l’axe des x dans la fenêtre finale) ; lecture : x, √(x² + x), écart (3 décimales).
- `horizontale` — f(x) = (2x + 1)/(x + 1) sur [0 ; 20]. Moments : `courbe_tracee` · `droite_horizontale` (y = 2 en pointillés, la courbe la
  longe) · `interpretation` (écrit « lim f(x) = 2 (x → +∞) » puis « la droite d’équation y = 2 est une asymptote horizontale à (C_f) en +∞ »).
  Repères : `courbe`, `droite_y2`, `interpretation`.

## raccord.html (continuité en un point)
- `trois_cas` — trois petits repères : courbe d’un seul trait par (a ; f(a)) ; courbe qui saute en a ; courbe trouée avec le point
  (a ; f(a)) posé plus haut. Moments : `courbe_soudee`, `saut`, `point_ailleurs`, `conclusion` (« continue en a : la courbe arrive
  exactement sur le point (a ; f(a)) »). Repères `cas1`, `cas2`, `cas3`.
- `limite_image` — f(x) = x + 1 pour x ≠ 1 (trou en (1 ; 2)), et f(1) = fa. Param `fa` (0,5..3,5, pas 0,5, défaut 3) ; poignée : le point
  (1 ; f(1)) glissé verticalement. Moments : `courbe_tracee` · `limite_lue` (étiquette « la limite : 2 », flèche là où arrive la courbe) ·
  `image_placee` (étiquette « f(1) = 3 » sur le point) · `comparaison` (« lim f(x) = 2 ≠ f(1) : f n’est pas continue en 1 » ; si fa = 2 :
  « lim f(x) = f(1) : f est continue en 1 »). Repères `limite`, `image`.
- `deux_branches` — f(x) = 3x − 1 si x < 1 ; f(x) = x² + m si x ≥ 1. Param `m` (−2..3, pas 0,5, défaut 3) ; poignée : le départ de la
  branche droite, glissé verticalement. Moments : `branche_gauche_arrive` (branche gauche jusqu’au rond vide (1 ; 2), « limite à gauche : 2 ») ·
  `branche_droite_part` (branche droite depuis (1 ; 1 + m), « limite à droite : 1 + m » avec la valeur) · `point_image` (point plein
  (1 ; f(1)), « f(1) = 1 + m ») · `verdict` (« soudée : m = 1, f est continue en 1 » ou « coupée : saut de … »). Repères `limite_gauche`,
  `limite_droite`, `f1`, `verdict`.

## usuelles.html (continuité sur un intervalle)
- `usuelles` — quatre petits repères : polynôme d’un trait (x² − 2x) « continue sur ℝ » ; x ↦ 1/x en deux morceaux « continue sur ]−∞ ; 0[ et
  sur ]0 ; +∞[ » ; √x qui naît en 0 « continue sur [0 ; +∞[ » ; sinus d’un trait « continue sur ℝ ». Moments : `polynome`, `inverse`, `racine`,
  `sinus`, `regle` (« une fonction usuelle est continue sur chaque intervalle de son domaine de définition »). Repères `polynome`, `inverse`,
  `racine`, `sinus`.
- `quotient` — f(x) = 2x/(x − 3) : la courbe en deux morceaux ; la valeur interdite 3 marquée d’une croix sur l’axe des x ; [4 ; +∞[ surligné en
  vert (« ✓ 3 n’y est pas ») ; [0 ; 5] surligné en orange (« ✗ contient 3 »). Moments : `courbe_tracee`, `valeur_interdite`, `intervalle_ok`,
  `intervalle_non`. Repères `valeur_interdite`, `intervalle_ok`, `intervalle_non`.

## composee.html (deux machines à la suite)
- `machines` — x → [ u ] → u(x) → [ √ ] → √(u(x)), avec u(x) = 3x − 6 ; sous la boîte √ : « n’accepte que du positif ». Moments : `boite_u`,
  `boite_racine`, `positif`, `exemple_ok` (x = 4 → u = 6 → √6), `exemple_refuse` (x = 1 → u = −3 → ✗ refusé), `courbes` (en bas à droite, petit
  repère : la courbe de u(x) = 3x − 6 et celle de √(3x − 6) qui naît en x = 2, « x ≥ 2 donc 3x − 6 ≥ 0 »). Repères `boite_u`, `boite_racine`, `positif`.
- `limite` — √(4 + 1/x) quand x → +∞ : la même chaîne de boîtes, une flèche la traverse : `x_infini` (« x → +∞ »), `u_limite` (« u(x) = 4 + 1/x → 4 »),
  `racine_limite` (« √(u(x)) → √4 = 2 » ; écrit « lim √(4 + 1/x) = 2 » sous x → +∞). Repères `boite_u`, `boite_racine`, `resultat`.
- `racine_n` — ⁿ√u : boîtes [ u ] → [ ∛ ] avec u(x) = x + 1 ; `boite_u`, `boite_racine_n`, `continuite` (« u continue et positive sur I, donc
  ⁿ√u continue sur I »), `limite_chaine` (x → +∞ ; u → +∞ ; ∛u → +∞). Repères `boite_u`, `boite_racine_n`, `continuite`.

## projections.html (image d’un intervalle)
- `croissante` — f(x) = x² − 4x + 1 sur [2 ; 5] → [−3 ; 6]. Params `a` (2..5, pas 0,5, défaut 2), `b` (2..5, pas 0,5, défaut 5) ; poignées a et b
  sur l’axe des x. Moments : `courbe_tracee`, `segment_pose` ([a ; b] épais sur l’axe des x), `monte_a` (pointillés de a à la courbe puis à l’axe des
  y, f(a)), `monte_b`, `image_coloree` (segment image épais coloré sur l’axe des y), `regle` (« f([a ; b]) = [f(a) ; f(b)] »).
  Repères `segment`, `fa`, `fb`, `image`, `regle`. lecture : a, b, f(a), f(b) et l’intervalle image.
- `decroissante` — g(x) = 4/x sur [1 ; 4] → [1 ; 4]. Moments : `courbe_tracee`, `segment_pose`, `monte_a`, `monte_b`, `pointilles_croises`
  (les deux pointillés se croisent : f(a) est en haut), `image_coloree`, `regle` (« décroissante : f([a ; b]) = [f(b) ; f(a)] »). Mêmes repères.
- `borne_ouverte` — g(x) = 4/x sur ]0 ; 4]. Moments : `courbe_tracee`, `segment_pose` (rond vide en 0), `rond_vide`, `limite_au_bord`
  (« lim g(x) = +∞ » sous x → 0⁺, flèche vers le haut de l’axe des y), `image_coloree` ([1 ; +∞[ coloré), `regle` (« ouvert → limite,
  fermé → image »). Repères `rond_vide`, `limite`, `image`, `regle`.
- `tout_R` — f(x) = x³ + x − 1 sur ℝ (strictement croissante). Moments : `courbe_tracee`, `limite_moins` (« −∞ » en bas, lim en −∞),
  `limite_plus` (« +∞ » en haut), `image_R` (tout l’axe des y coloré, « f(ℝ) = ]−∞ ; +∞[ = ℝ »), `zero_dans` (0 entouré sur l’axe des y,
  « 0 ∈ f(ℝ) »), `alpha` (le croisement α avec l’axe des x). Repères `image`, `zero`, `alpha`.
- `non_monotone` — h(x) = x³ − 3x sur [−2 ; 2]. Moments : `courbe_tracee`, `creux_et_bosse` (bosse M = 2 en x = −1, creux m = −2 en x = 1),
  `tableau` (petit tableau de variations à droite : x : −2, −1, 1, 2 ; h : −2 ↗ 2 ↘ −2 ↗ 2), `image_coloree` ([−2 ; 2] sur l’axe des y),
  `regle` (« f([a ; b]) = [m ; M] »). Repères `bosse`, `creux`, `tableau`, `image`.

## dichotomie.html (encadrer α)
- `etapes` — f(x) = x³ + 2x − 1 sur [0 ; 1] (α ≈ 0,4534). Repère à gauche (≈ x0 50, w 330), tableau à droite (colonnes « intervalle | milieu m |
  f(m) | nouvel intervalle | amplitude », une ligne par étape). Moments : `intervalle_depart` ([0 ; 1] en trait épais, f(0) = −1 « − », f(1) = 2 « + ») ·
  `milieu_1` (m = 1/2 marqué) · `image_milieu_1` (le point de la courbe au-dessus de 1/2 s’allume, « f(1/2) = 1/8 > 0 », signe « + ») ·
  `moitie_gardee_1` (la moitié rejetée s’efface/pâlit, « 0 < α < 1/2 », amplitude 0,5, ligne 1 du tableau) · `milieu_2` (1/4) ·
  `image_milieu_2` (« f(1/4) = −31/64 < 0 ») · `moitie_gardee_2` (« 1/4 < α < 1/2 », amplitude 0,25, ligne 2) · `milieu_3` (3/8) ·
  `image_milieu_3` (« f(3/8) = −101/512 < 0 ») · `moitie_gardee_3` (« 3/8 < α < 1/2 », amplitude 0,125, ligne 3).
  Repères `intervalle`, `milieu`, `signe`, `amplitude`, `tableau`. (Pas de mot « algorithme », pas de nombre d’itérations, pas d’erreur.)
- `probleme` — f(x) = x³ + x − 1 sur [1/2 ; 1] : `intervalle_depart` (f(1/2) = −3/8 < 0, f(1) = 1 > 0) · `milieu_1` (3/4) · `image_milieu_1`
  (f(3/4) = 11/64 > 0) · `moitie_gardee_1` (« 1/2 < α < 3/4 », amplitude 0,25). Mêmes repères.

## miroir.html (fonction réciproque)
- `aller_retour` — f(x) = x² + 1 sur [0 ; +∞[. Param `x_m` (0..2,5, pas 0,1, défaut 2) ; poignée : x sur l’axe des x. Moments : `courbe_tracee`,
  `aller` (flèches : de 2 sur l’axe des x jusqu’à la courbe puis vers l’axe des y : 5 ; « f(2) = 5 »), `retour` (autre couleur : de 5 sur l’axe des y
  à la courbe puis vers 2 ; « f⁻¹(5) = 2 »), `defait` (« f⁻¹ défait ce que f a fait » ; « f⁻¹ n’est pas 1/f »). Repères `aller`, `retour`, `x`, `y`.
- `parabole` — x ↦ x² sur ℝ. Moments : `courbe_tracee`, `deux_antecedents` (droite y = 4 qui coupe en −2 et 2 : « 4 a deux antécédents : le retour
  hésite »), `restriction` (la moitié gauche pâlit ; « restriction à [0 ; +∞[ : un seul antécédent, 2 » ; « g strictement croissante »).
  Repères `droite_y4`, `deux_points`, `restriction`.
- `I_et_J` — f(x) = x² − 4x + 1 sur I = [2 ; +∞[. Moments : `courbe_tracee`, `I_colore` (I sur l’axe des x), `J_colore` (J = [−3 ; +∞[ sur l’axe
  des y), `sens` (« f : I → J » et « f⁻¹ : J → I »). Repères `I`, `J`.
- `tableaux` — tableau de variations de f strictement décroissante sur [a ; b] (f(a) en haut, f(b) en bas), puis celui de f⁻¹ sur [f(b) ; f(a)]
  (de b à a, décroissante) : moments `tableau_f`, `tableau_reciproque`, `tableaux_echanges` (flèches montrant que les deux lignes s’échangent ;
  « même sens de variation » ; « f continue ⇒ f⁻¹ continue sur J »). Repères `tableau_f`, `tableau_reciproque`.
- `reflet` — f(x) = x² + 1 sur [0 ; +∞[ et son reflet (C_f⁻¹) : y = √(x − 1). Repère ÉGAL [−0,5 ; 5,5] × [−0,5 ; 5,5]. Param `x_m` (0..2, pas 0,1,
  défaut 1) ; poignée M sur (C_f). Moments : `courbe_tracee`, `droite_y_x` (pointillés, « y = x »), `reflet_du_point` (M(1 ; 2) → M′(2 ; 1), segment
  [MM′] perpendiculaire à y = x), `courbe_reflet` (M glisse, M′ trace (C_f⁻¹)), `points_echanges` ((0 ; 1) → (1 ; 0) ; (2 ; 5) → (5 ; 2)).
  Repères `M`, `M_prime`, `droite_y_x`, `courbe_reflet`. lecture : coordonnées de M et de M′.
- `asymptotes` — f(x) = 2 + 1/x sur ]0 ; +∞[ (asymptotes x = 0 et y = 2). Repère ÉGAL. Moments : `courbe_tracee` (avec y = 2 en pointillés),
  `droite_y_x`, `courbe_reflet` ((C_f⁻¹) : y = 1/(x − 2), x > 2), `asymptotes_echangees` (x = 2 en pointillés ; « y = 2 ↔ x = 2 » ; « x = 0 ↔ y = 0 »).
  Repères `asymptote_h`, `asymptote_v`, `courbe_reflet`.

## racine.html (racine n-ième)
- `defaire` — x ↦ x³ sur [0 ; +∞[ (x ∈ [0 ; 2,3], y ∈ [0 ; 10]). Moments : `courbe_puissance`, `aller` (2 → 8 : « 2³ = 8 »), `depart_8` (on part
  de 8 sur l’axe des y), `retour_2` (on revient à 2 : « ∛8 = 2 car 2³ = 8 »). Repères `depart_8`, `retour_2`.
- `reflet_racine` — xⁿ sur [0 ; +∞[ et son reflet par y = x. Param `n` (2..4, pas 1, défaut 3) ; poignée « n » sur une petite échelle 2-3-4 en haut à
  droite. Repère ÉGAL [0 ; 2,6]². Moments : `courbe_puissance`, `droite_y_x`, `reflet_racine` (courbe de ⁿ√x, « ⁿ√x = y ⇔ x = yⁿ »),
  `points_communs` ((0 ; 0) et (1 ; 1) entourés). Repères `courbe_racine`, `points_communs`.
- `equation` — deux petits repères : à gauche x⁴ (x ∈ [−2,5 ; 2,5]), à droite x³ (x ∈ [−3,5 ; 3,5]) ; en dessous le tableau 2 × 2.
  Moments : `a_positif_pair` (y = 16 à gauche : x = −2 ou x = 2), `a_negatif_pair` (y = −16 : aucune solution), `a_positif_impair` (y = 8 à droite :
  x = 2), `a_negatif_impair` (y = −27 : x = −3, « x = −∛27 = −3 »), `tableau_rempli` (n pair / n impair × a > 0 / a < 0 : « x = ⁿ√a ou x = −ⁿ√a »,
  « aucune solution », « x = ⁿ√a », « x = −ⁿ√(−a) »). Repères `pair`, `impair`, `tableau`.

## calculs.html (calculs écrits à la main — moteur générique, données générées par le build du cours)
- La page charge `calculs-donnees.js` (même dossier) qui définit `window.CALCULS = { "<vue>": { titre, lignes: [...] } }` ; `?vue=<id>`.
- Chaque ligne : `t` (texte), facultatifs : `lim` ("x → 3" : « lim » écrit avec ce texte en petit dessous, au début de la ligne), `frac` ([num, den] :
  fraction écrite en deux étages après `t`), `apres` (texte après la fraction), `couleur` (blanc|cyan|jaune|vert|orange|rouge), `taille` (19),
  `moment` (nom marqué juste après la ligne), `cadre` (couleur : cadre autour de la ligne), `barre` ([sous-chaînes] barrées en rouge après
  l’écriture de la ligne — cherchées dans t, num, den, apres), `entoure` ([sous-chaînes] entourées), `souligne` ([sous-chaînes]),
  `sous` ([[sous-chaîne, petit texte écrit dessous]] : la limite sous un terme), `marge` (petite note orange à droite : « ai-je le droit ? »),
  `repere` (id) + `label`, `pause` (s avant), `col` (2 = seconde colonne à x ≈ 400 ; la colonne repart en haut), `dx` (retrait), `inter`.
- Mise en page automatique : titre en haut (K.titre), lignes à partir de y ≈ 72, interligne 31 (44 pour une ligne `frac`) ; si une colonne
  dépasse y = 355, réduire taille et interligne pour tenir. `decrire` : pour chaque moment « Écrit : <texte de la ligne> ».
- Fournir un `calculs-donnees.js` d’essai (deux ou trois vues) — le build du cours le réécrira entièrement.

## ouverture.html (diapositive o1)
- `carte` — au centre une courbe (avec un trou, une asymptote, un croisement d’axe) ; autour, six questions et leur outil, écrites une à une :
  `q_limite` (« Où va-t-elle ? → limite »), `q_continuite` (« Est-elle soudée ? → continuité »), `q_image` (« Quelles hauteurs atteint-elle ?
  → image d’un intervalle »), `q_tvi` (« Coupe-t-elle l’axe ? → théorème des valeurs intermédiaires »), `q_reciproque` (« Peut-on revenir en
  arrière ? → fonction réciproque »), `q_racine` (« Que défait ⁿ√ ? → racine n-ième »), `national` (à côté de trois questions, en orange :
  « national : 20 sujets sur 20 » (limite), « 8 sur 20 » (réciproque), « 6 sur 20 » (solution unique)). Repères = noms des moments.

## bilan.html et carte.html
Copier `../../physics/ondes-periodiques-tableau/bilan.html` et `carte.html` ; remplacer `<script src="commun.js">` par
`<script src="/media/simulations/maths/commun/maths-tableau.js">` (fournit `window.OndesTableau.Scene`), charger aussi
`/media/simulations/maths/commun/exposants.js` (après tableau.js), et `ondes.css` par `/media/simulations/maths/commun/maths.css`.
Garder toute la mécanique (S.apparu, page 2 de l’élève, imprimer, acquis), changer blocs, branches, titres, textes, ids de config.
Compétences du cours : K1 … K10.
- bilan, moments (dans l’ordre) : `limites` (K1), `continuite_point` (K2), `continuite_intervalle` (K3), `image` (K4), `tvi` (K5),
  `dichotomie` (K6), `reciproque` (K7), `courbe` (K8), `racine` (K9, K10) ; plus `fiche` et `lacunes` comme le modèle.
- carte, moments : `definition` (centre « Limites et continuité » : « f est continue en a si lim f(x) = f(a) quand x → a »), puis les
  branches `limites` (K1), `continuite` (K2, K3), `image` (K4), `tvi` (K5), `dichotomie` (K6), `reciproque` (K7), `courbe` (K8),
  `racine` (K9, K10) ; `complet`.
