# Contrat des simulations — cours « Dérivation et étude des fonctions » (math_ch2_derivation_etude_fonctions)

Dossier : `frontend\public\media\simulations\maths\derivation-tableau\`
URL servie : `/media/simulations/maths/derivation-tableau/<page>.html?vue=<vue>`

Le cours (voix, pointage) cite EXACTEMENT les noms de vues, de moments (`K.marque`) et de repères (`c.repere`) ci-dessous :
ne les renomme pas, n'en oublie aucun. Tu peux AJOUTER des moments/repères intermédiaires si utile (ex. `repere_pose`,
`courbe_tracee`). Chaque moment a sa phrase dans `decrire` et un libellé court dans `motifs`.

## À lire avant d'écrire (ne rien modifier de ces fichiers)
1. Le brief : `outils\cours\notes\cours\maths_build\BRIEF_COURS_MATHS.md` (section « Le kit maths » et « Outils »).
2. Le skill `.agents\skills\simulations-au-tableau\SKILL.md`.
3. Le kit : `frontend/public/media/simulations/maths/commun/maths-tableau.js` (en-tête complet), `exposants.js`, `maths.css`,
   et `frontend/public/media/simulations/shared/tableau/tableau.js` (Craie : texte, ligne, fleche, trait, rect, cercle, point, repere, pause, direct ; couleurs blanc cyan jaune vert violet orange bleu rouge rose faible tresfaible).
4. La page MODÈLE : `frontend/public/media/simulations/maths/limites-continuite-tableau/traversee.html` — copie sa forme exacte
   (head, barre avec un seul bouton `#run` data-professor-control, bulle `#feedback`, scripts tableau.js → exposants.js →
   maths-tableau.js, puis `MathsTableau.page({...})`, puis professor-locate.js).

## Règles (toutes obligatoires)
- Fond transparent (maths.css), tout dans le cadre 760 × 420, ~60 px libres en bas (rien d'écrit sous y ≈ 360), titre de vue `K.titre(...)` en haut à gauche.
- Un seul bouton ; les réglages = poignées glissées sur le dessin (`poignees(K)` + `params`), jamais de curseur/onglet.
- Apostrophe typographique ’ dans toutes les chaînes JS françaises (ou backticks). Texte au tableau en FRANÇAIS.
- Indices : écris `x_0`, `f'_d(1)` → rendu en indice par le kit (jamais de « _ » visible). Exposants : « x² », « x³ », « f⁻¹ » (exposants.js).
- Prime : utilise ′ (U+2032) ou ' pour f′ — sois constant dans la page (préférer `f′`).
- Construction écrite pas à pas à la craie (comme la page modèle) : repère, puis courbe tracée en direct (`K.anime` + `K.courbePart`),
  puis points, droites, textes, chaque phase marquée par `K.marque('nom')` APRÈS ce qu'elle montre.
- Ce qui glisse (un point M qui s'approche, une tangente qui roule) se fait dans `K.anime(durée, p => …)` : le moment marqué juste
  après l'anime fige l'image sur la position finale de cette phase. Pour une phase « M est en 1,5 », fais un anime qui amène M de sa
  position précédente à 1,5, puis `K.marque('secante_proche')`.
- Après `fin` (construction complète) la poignée de l'élève règle le paramètre ; la vue redessine avec la valeur choisie, et `lecture(K)`
  donne une phrase avec les valeurs (ex. « M en x = 1,5 : pente de (AM) = 2,5 »). Le tuteur peut faire `set_parameters`.
- `decrire` : une phrase par moment, exacte (valeurs justes), qui dit ce qui se voit. `explication` : liste {repere, texte}.
- Rien hors programme : pas de « bijection/bijective », pas de L’Hôpital, pas d’approximation affine chiffrée, pas de division euclidienne.
  Vocabulaire : « nombre dérivé », « taux d’accroissement », « demi-tangente », « point anguleux », « asymptote verticale/horizontale/oblique »,
  « branche parabolique de direction l’axe des ordonnées / des abscisses / la droite d’équation y = x », « au voisinage de +∞ »,
  « concave (tournée vers le bas) / convexe (tournée vers le haut) », « point d’inflexion », « fonction réciproque f⁻¹ ».
- Les nombres à la française (virgule) : `K.fr(v, d)`.
- Labels jamais superposés, même aux positions extrêmes de la poignée (vérifie au min et au max).

## Vérifications (à faire toi-même, avant de rendre)
Serveur statique déjà lancé : `http://127.0.0.1:8898` (racine frontend/public). S'il ne répond pas :
`python -m http.server 8898 -d frontend/public --bind 127.0.0.1` en arrière-plan.
- `python "<maths_build>/check_js.py" <page.html>` → ok.
- `python "<maths_build>/test_page.py" --shot <dossier temporaire dans ton scratchpad> /media/simulations/maths/derivation-tableau/<page>.html?vue=<vue> …`
  pour CHAQUE vue → « AUCUN PROBLÈME », moments et repères listés = ceux du contrat. Lis les captures (Read) : lisible, rien
  de coupé, rien sous y ≈ 360 px du cadre, pas de chevauchement. Supprime tes captures ensuite (disque presque plein).
- Teste aussi une poignée au min et au max avec `?<param>=<valeur>` dans l'URL (le kit lit les paramètres de l'URL).
(`<maths_build>` = `outils\cours\notes\cours\maths_build`)

Interdits : ne modifie aucun autre fichier (ni le kit, ni maths/commun, ni d'autres dossiers), aucun commit/push/stash/reset/checkout, aucune voix.

---------------------------------------------------------------------------------------------------------------------------

## secante.html — f(x) = x², A(1 ; 1) ; puis f(x) = x + 1/x pour l'équation
### vue `secante` (diapositives : taux d'accroissement, M se rapproche, nombre dérivé)
Repère x ∈ [−1,2 ; 3,6], y ∈ [−1 ; 10] (à ajuster), parabole y = x² (cyan), A(1 ; 1) jaune fixe, M sur la courbe.
À droite (x ≥ ~480) un petit tableau « x_M | pente de (AM) » qui se remplit : 3 → 4 ; 2 → 3 ; 1,5 → 2,5 ; 1,1 → 2,1 ; 1,01 → 2,01.
Pente de (AM) = (f(x) − f(1))/(x − 1) = x + 1 (écrite en clair au-dessus du tableau : « pente de (AM) = (f(x) − f(1)) / (x − 1) »).
Moments (dans l'ordre) :
- `repere_pose`, `courbe_tracee`
- `point_a` : A(1 ; 1) placé et nommé
- `secante_loin` : M en (3 ; 9), la droite (AM) tracée (orange) un peu au-delà des deux points, « pente = 4 » écrit, ligne 3 → 4 du tableau
- `secante_proche` : M glisse jusqu'à x = 1,5 (lignes 2 → 3 puis 1,5 → 2,5 écrites au passage), la sécante pivote autour de A
- `presque_confondus` : M en 1,1 puis 1,01 (lignes 1,1 → 2,1 et 1,01 → 2,01), M et A presque confondus
- `tangente` : M arrive sur A ; la droite devient la tangente en A (jaune), écrite « tangente en A »
- `pente_lue` : « la pente se rapproche de 2 » puis encadré « f′(1) = 2 » (le nombre dérivé)
Repères : `point_a`, `point_m`, `secante`, `pente`, `tableau_pentes`, `tangente`, `nombre_derive`.
Param `x_m` (0,2..3,2, pas 0,01, défaut 3 ; poignée sur M) : après la fin, M à x_m (si |x_m − 1| < 0,005 : la tangente) et la pente affichée ;
lecture : « M en x = …, pente de (AM) = … » ou « M sur A : tangente, pente f′(1) = 2 ». M aussi À GAUCHE de A (x_m < 1) : pente < 2.

### vue `equation` (diapositives : équation de la tangente, vérifier, tangente horizontale)
f(x) = x + 1/x sur ]0 ; +∞[ (x ∈ [0,25 ; 5,5], y ∈ [−0,5 ; 6]), point de contact A(a ; f(a)), défaut a = 2 : f(2) = 5/2, f′(2) = 3/4.
f′(x) = 1 − 1/x². Tangente : y = f′(a)(x − a) + f(a) ; pour a = 2 : y = (3/4)x + 1.
Moments :
- `repere_pose`, `courbe_tracee`
- `point_contact` : A(2 ; 5/2) placé, projections pointillées sur les axes (2 et 5/2)
- `pente_tangente` : la tangente (jaune) tracée, petit triangle de pente : 1 à l'horizontale, 3/4 à la verticale (« 3/4 »)
- `equation_generale` : à droite, écrit « (T) : y = f′(x_0)(x − x_0) + f(x_0) »
- `equation_tangente` : lignes « f(2) = 5/2 », « f′(2) = 3/4 », « y = (3/4)(x − 2) + 5/2 », « y = (3/4)x + 1 » (encadrée)
- `se_confond` : un petit cercle (loupe) autour de A : « près de A, la courbe se confond avec sa tangente »
- `verification` : « (3/4) × 2 + 1 = 5/2 ✓ : A est sur (T) »
Repères : `point_contact`, `tangente`, `triangle_pente`, `equation`, `loupe`.
Param `a` (0,5..4, pas 0,05, défaut 2 ; poignée sur A) : la tangente et les valeurs se recalculent (fractions si simples, sinon décimales) ;
pour a = 1 : f′(1) = 0, tangente HORIZONTALE y = 2 (écrire « tangente horizontale : y = 2 »). lecture : « a = …, f(a) = …, f′(a) = …, (T) : y = … ».

## demi-tangentes.html
### vue `coin` — f(x) = |x² − 1| près de A(1 ; 0) (x ∈ [−0,3 ; 2,3], y ∈ [−0,6 ; 3])
- `repere_pose`, `courbe_tracee` (la courbe en V arrondi : 1 − x² à gauche de 1, x² − 1 à droite), `point_a`
- `m_a_droite` : M arrive par la DROITE (de x = 2 à x = 1,02), la sécante (orange) pivote, taux affiché 3 → 2,02
- `demi_tangente_droite` : demi-droite d'origine A vers la droite, pente 2 (jaune), écrit « f′_d(1) = 2 »
- `m_a_gauche` : M arrive par la GAUCHE (de x = 0 à 0,98), taux −1 → −1,98
- `demi_tangente_gauche` : demi-droite d'origine A vers la gauche, pente −2 (vert), « f′_g(1) = −2 »
- `point_anguleux` : petit arc d'angle en A, écrit « f′_d(1) ≠ f′_g(1) : f n’est pas dérivable en 1 » et « A est un point anguleux »
Repères : `point_a`, `point_m`, `demi_droite`, `demi_gauche`, `angle`, `conclusion`.
Param `x_m` (0,1..1,9, défaut 1,6 ; poignée M) ; lecture : côté (droite/gauche), taux = valeur.

### vue `verticale` — f(x) = √x près de O (x ∈ [−0,2 ; 2,2], y ∈ [−0,3 ; 1,6])
- `repere_pose`, `courbe_tracee`, `point_o`
- `secante_se_redresse` : M descend de x = 1 vers x = 0,01 ; la sécante (OM) se redresse ; taux 1/√x affiché : 1 ; 3,16 ; 10
- `taux_infini` : écrit « (f(x) − f(0)) / (x − 0) = 1/√x → +∞ quand x → 0⁺ »
- `demi_tangente_verticale` : flèche verticale partant de O vers le HAUT (jaune), « demi-tangente verticale dirigée vers le haut » et « f n’est pas dérivable à droite en 0 »
Repères : `point_o`, `point_m`, `secante`, `taux`, `fleche`.
Param `x_m` (0,01..2, défaut 1 ; poignée M) ; lecture : « x = …, taux = 1/√x = … ».

### vue `sens` — quatre mini-repères (2 × 2), un cas par mini-repère, chacun avec le point A, un petit arc de courbe du bon côté
et la flèche verticale qui part de A VERS la courbe :
- `droite_plus_infini` : à droite, taux → +∞ : courbe à droite AU-DESSUS de A, flèche vers le haut
- `droite_moins_infini` : à droite, taux → −∞ : courbe à droite EN DESSOUS, flèche vers le bas
- `gauche_plus_infini` : à gauche, taux → +∞ : courbe à gauche EN DESSOUS, flèche vers le bas
- `gauche_moins_infini` : à gauche, taux → −∞ : courbe à gauche AU-DESSUS, flèche vers le haut
- `regle` : en bas (au-dessus de y ≈ 355) : « la demi-tangente part du côté où est la courbe »
Chaque mini : légende courte « à droite, +∞ » / « vers le haut ». Repères : `cas_dp`, `cas_dm`, `cas_gp`, `cas_gm`, `regle`.

## variations.html — g(x) = x³ − 3x
### vue `glisse` (signe de f′ et variations, sommet et creux, tableau de variations)
En haut la courbe (x ∈ [−2,4 ; 2,4], y ∈ [−3 ; 3], cadre y ≈ 45..225), un point P (jaune) qui glisse sur la courbe avec sa tangente (orange, segment court centré sur P).
En dessous (y ≈ 245..355), ALIGNÉ avec les abscisses de la courbe, le tableau qui s'écrit au passage de P :
ligne « x » : −∞, −1, 1, +∞ ; ligne « f′(x) » : + 0 − 0 + ; ligne « f(x) » : flèche montante de −∞ à 2, descendante de 2 à −2, montante de −2 à +∞.
Moments :
- `repere_pose`, `courbe_tracee`
- `monte` : P de x = −2,2 à −1,6 ; tangente penchée vers le haut ; « + » écrit sous cette partie, petite flèche montante
- `sommet` : P en −1 ; tangente horizontale ; « 0 » sous −1, « f′(−1) = 0 », valeur 2 (maximum) en haut de la ligne f(x)
- `descend` : P de −1 à 0,4 ; « − » ; flèche descendante
- `creux` : P en 1 ; tangente horizontale ; « 0 » sous 1, « f′(1) = 0 », valeur −2 (minimum) en bas
- `remonte` : P de 1 à 2,1 ; « + » ; flèche montante
- `tableau_complet` : les bouts : −∞ (bas à gauche) et +∞ (haut à droite), la ligne x complète ; à droite du tableau ou au-dessus : « f′(x) = 3(x − 1)(x + 1) »
Repères : `point_p`, `tangente`, `ligne_signe`, `ligne_fleches`, `sommet`, `creux`, `tableau`.
Param `x_p` (−2,3..2,3, pas 0,01, défaut 1,8 ; poignée P) ; lecture : « P en x = …, pente de la tangente f′(x) = …, f′ positive/négative/nulle : f croissante/décroissante ».

## concavite.html
### vue `roule` — g(x) = x³ − 3x (x ∈ [−2,4 ; 2,4], y ∈ [−3,2 ; 3,2]) ; tangente en T(t ; g(t)) : y = g′(t)(x − t) + g(t), g′(t) = 3t² − 3, g″(x) = 6x
La tangente (orange, longue) ROULE le long de la courbe ; la zone entre la courbe et la tangente près du contact est légèrement coloriée
(raw canvas dans `c.direct`, alpha ≈ .12) : bleu si la courbe est SOUS la tangente, vert si AU-DESSUS.
Moments :
- `repere_pose`, `courbe_tracee`
- `courbe_sous_tangente` : contact de t = −2 à t = −1,2 ; la courbe reste sous sa tangente ; « ∩ concave : la courbe est sous ses tangentes » (à gauche)
- `tangente_traverse` : contact en t = 0 ; tangente y = −3x ; elle TRAVERSE la courbe ; point I(0 ; 0) entouré, « I(0 ; 0) point d’inflexion »
- `courbe_au_dessus` : contact de 0 à 1,3 ; la courbe au-dessus ; « ∪ convexe : la courbe est au-dessus de ses tangentes »
- `ligne_f_seconde` : en bas (y ≈ 300..355) une petite ligne « f″(x) = 6x » et un mini-tableau « x : −∞ 0 +∞ / f″(x) : − 0 + / (Cf) : ∩ I ∪ »
Repères : `point_contact`, `tangente`, `arc_concave`, `arc_convexe`, `point_i`, `ligne_f_seconde`.
Param `x_t` (−2..2, pas 0,01, défaut 1,3 ; poignée = point de contact) ; lecture : « contact en x = …, f″(x) = 6x = … : la courbe est sous/au-dessus de sa tangente ».

### vue `x4` — f(x) = x⁴ (x ∈ [−1,6 ; 1,6], y ∈ [−0,5 ; 4])
- `repere_pose`, `courbe_tracee`
- `tangente_en_o` : tangente en O : y = 0 (orange)
- `reste_au_dessus` : la tangente roule de −1 à 1 en passant par 0 : la courbe reste AU-DESSUS des deux côtés de O
- `ligne_f_seconde` : « f″(x) = 12x² » ; mini-tableau « x : −∞ 0 +∞ / f″(x) : + 0 + »
- `contre_exemple_x4` : « f″(0) = 0 mais f″ ne change pas de signe : O n’est pas un point d’inflexion »
Repères : `point_o`, `tangente`, `ligne_f_seconde`, `conclusion`.

## branches.html (sept vues ; dans chaque vue un point M sur la courbe qu'on envoie vers le bord ; les limites s'écrivent à droite,
zone x ≥ ~470 ; le repère à gauche x ≤ ~450). Param `x_m` dans les six premières vues (poignée M), bornes à choisir pour rester dans le cadre.
### vue `verticale` — f(x) = 1/(x − 2) + 1, x ∈ [−1 ; 5], y ∈ [−4 ; 6]
- `repere_pose`, `courbe_tracee`
- `m_part` : M glisse vers x = 2⁺ (de 3,5 à 2,1), il monte le long de la verticale ; f(x) affiché (1,67 ; 3 ; 11)
- `asymptote_verticale` : droite pointillée x = 2 (rouge), « x = 2 »
- `limite_ecrite` : « lim f(x) = +∞ quand x → 2⁺ » puis « la droite d’équation x = 2 est une asymptote verticale à (Cf) »
Repères : `point_m`, `asymptote`, `limite`.
### vue `horizontale` — même f, x ∈ [−1 ; 14], y ∈ [−2 ; 4]
- `repere_pose`, `courbe_tracee`, `droite_tracee` (y = 1 pointillée)
- `m_part` : M part à droite (de 3 à 13)
- `ecart_fond` : segment vertical M → droite, écart f(x) − 1 affiché : 1 ; 0,1 ; …
- `asymptote_horizontale` : « y = 1 » nommée
- `limite_ecrite` : « lim f(x) = 1 quand x → +∞ » puis « la droite d’équation y = 1 est une asymptote horizontale à (Cf) au voisinage de +∞ »
Repères : `point_m`, `ecart`, `asymptote`, `limite`.
### vue `oblique` — f(x) = 2x + 1 + 1/x, (Δ) : y = 2x + 1, x ∈ [−0,5 ; 6], y ∈ [−1 ; 14]
- `repere_pose`, `courbe_tracee`, `droite_tracee`
- `ecart_fond` : M part de x = 1 à 5,5 ; segment vertical entre courbe et droite ; écart f(x) − (2x + 1) = 1/x affiché : 1 ; 0,5 ; 0,2
- `ecart_nul_a_la_limite` : « f(x) − (2x + 1) = 1/x → 0 quand x → +∞ »
- `limite_ecrite` : « la droite d’équation y = 2x + 1 est une asymptote oblique à (Cf) au voisinage de +∞ »
Repères : `point_m`, `droite`, `ecart`, `limite`.
### vue `oy` — f(x) = x², x ∈ [−0,5 ; 4,5], y ∈ [−1 ; 18]
- `repere_pose`, `courbe_tracee`
- `m_part` : M part à droite (1 → 4)
- `pente_om_explose` : la droite (OM) tracée (orange) qui se redresse ; « pente de (OM) = f(x)/x = x » affichée : 1 ; 2 ; 4…
- `limite_ecrite` : « lim f(x)/x = +∞ » puis « branche parabolique de direction l’axe des ordonnées au voisinage de +∞ »
Repères : `point_m`, `droite_om`, `pente`, `limite`.
### vue `ox` — f(x) = √x, x ∈ [−0,5 ; 16], y ∈ [−0,5 ; 4,5]
- `repere_pose`, `courbe_tracee`, `m_part` (M de 1 à 15)
- `pente_om_fond` : (OM) se couche ; f(x)/x = 1/√x affichée : 1 ; 0,5 ; 0,26
- `limite_ecrite` : « lim f(x)/x = 0 » puis « branche parabolique de direction l’axe des abscisses au voisinage de +∞ »
Repères : `point_m`, `droite_om`, `pente`, `limite`.
### vue `direction` — f(x) = x + √x, droite y = x, x ∈ [−0,5 ; 16], y ∈ [−0,5 ; 21]
- `repere_pose`, `courbe_tracee`, `droite_tracee` (y = x, passant par O)
- `m_part` (M de 1 à 15)
- `pente_tend_vers_a` : f(x)/x = 1 + 1/√x affichée → 1
- `ecart_grandit` : segment vertical courbe → droite y = x ; écart f(x) − x = √x : 1 ; 2 ; 3,87 : il grandit
- `limite_ecrite` : « lim f(x)/x = 1 et lim [f(x) − x] = +∞ » puis « branche parabolique de direction la droite d’équation y = x au voisinage de +∞ »
Repères : `point_m`, `droite`, `pente`, `ecart`, `limite`.
### vue `arbre` — arbre de décision écrit pas à pas (pas de repère), avec sous chaque feuille une mini-allure (petit croquis) et la phrase type courte
- `racine` : trois départs : « lim f(x) = ±∞ quand x → a », « lim f(x) = b quand x → ±∞ », « lim f(x) = ±∞ quand x → ±∞ »
- `branche_av` : feuille « asymptote verticale x = a » + mini-allure
- `branche_ah` : feuille « asymptote horizontale y = b » + mini-allure
- `f_sur_x` : sous la 3ᵉ entrée : « on calcule lim f(x)/x »
- `feuille_oy` : « ±∞ : branche parabolique de direction (Oy) »
- `feuille_ox` : « 0 : branche parabolique de direction (Ox) »
- `f_moins_ax` : « a ≠ 0 : on calcule lim [f(x) − ax] »
- `feuille_oblique` : « b : asymptote oblique y = ax + b »
- `feuille_direction` : « ±∞ : branche parabolique de direction y = ax »
- `phrase_type` : en bas : « (Cf) admet … d’équation … au voisinage de … »
Repères : `entree_a`, `entree_finie`, `entree_infinie`, `f_sur_x`, `f_moins_ax`, `phrase`. Tout doit tenir dans 760 × 360 : petites tailles (13–15 px), mini-allures ~50 × 35 px.

## position.html — f(x) = 2x + 1 + 1/x et (Δ) : y = 2x + 1
### vue `ecart` — repère à gauche (x ∈ [−3,2 ; 3,2], y ∈ [−8 ; 9]), tableau à droite ou en bas à droite
Segment vertical à l'abscisse x entre (Δ) et (Cf) : VERT si la courbe est au-dessus, ROUGE si en dessous ; valeurs écrites :
« f(x) − y = 1/x = … ».
- `repere_pose`, `courbe_tracee`, `droite_tracee`
- `ecart_positif` : x = 1 : segment vert, « f(1) − y = 1 > 0 : (Cf) au-dessus de (Δ) »
- `ecart_negatif` : x passe à −1 : segment rouge, « f(−1) − y = −1 < 0 : (Cf) en dessous de (Δ) »
- `tableau_rempli` : tableau « x : −∞ 0 +∞ / x : − ‖ + / f(x) − y = 1/x : − ‖ + / position : (Cf) en dessous de (Δ) ‖ (Cf) au-dessus de (Δ) »
Repères : `segment`, `difference`, `tableau`, `droite`.
Param `x` (−3..3, pas 0,05, défaut 1 ; poignée ; x = 0 interdit → ±0,05) ; lecture : « x = …, f(x) − y = 1/x = … : au-dessus/en dessous ».

## symetrie.html
### vue `axe` — f(x) = x² − 4x + 5 (x ∈ [−0,8 ; 4,8], y ∈ [−0,5 ; 7]), axe x = 2
- `repere_pose`, `courbe_tracee`, `axe_trace` (droite x = 2 pointillée violette, « x = 2 »)
- `symetrique_place` : sur l'axe des abscisses x = 3 et son symétrique 1 = 4 − 3, deux flèches de même longueur depuis 2 ; écrit « 2a − x = 4 − x »
- `meme_hauteur` : points M(3 ; 2) et M′(1 ; 2) sur la courbe, segment horizontal pointillé ; « f(1) = f(3) = 2 »
- `relation_axe` : « f(2a − x) = f(x) : ici f(4 − x) = f(x) »
Repères : `axe`, `point_x`, `point_sym`, `meme_hauteur`, `relation`.
Param `x` (2,1..4,6, défaut 3 ; poignée sur x) ; lecture avec 4 − x, f(x), f(4 − x).
### vue `centre` — f(x) = (x + 1)/(x − 2) (x ∈ [−3 ; 7], y ∈ [−4 ; 6]), Ω(2 ; 1), asymptotes x = 2 et y = 1 en pointillé faible
- `repere_pose`, `courbe_tracee`, `omega_place` (Ω(2 ; 1) point violet nommé)
- `deux_points` : M(x ; f(x)) et M′(4 − x ; f(4 − x)) pour x = 3 : M(3 ; 4), M′(1 ; −2)
- `milieu_sur_omega` : segment [MM′] ; son milieu tombe sur Ω (entouré) ; « f(4 − x) + f(x) = 2 = 2 × 1 »
- `relation_ecrite` : accolade à deux lignes : « (2a − x) ∈ D_f » et « f(2a − x) + f(x) = 2b »
Repères : `omega`, `point_m`, `point_m2`, `milieu`, `relation`.
Param `x` (2,3..6,5, défaut 3 ; poignée).

## trace.html — f(x) = x + 1/x (fil rouge), puis lecture, puis l'étude de x√(x + 1)
### vue `etapes` — à GAUCHE le tableau de variations (x ≤ ~330), à DROITE le repère (x ∈ [−4,5 ; 4,5], y ∈ [−6 ; 6])
Tableau : x : −∞ −1 0 1 +∞ ; f′(x) : + 0 − ‖ − 0 + ; f(x) : −∞ ↗ −2 ↘ −∞ ‖ +∞ ↘ 2 ↗ +∞ (double barre en 0).
- `tableau_lu` : le tableau s'écrit, puis les limites s'allument une à une (encadrées)
- `asymptote_verticale` : la case « ‖ » allumée → l'axe des ordonnées repassé en pointillé rouge « x = 0 »
- `asymptote_oblique` : droite y = x pointillée (rouge) avec ses deux points (0 ; 0) et (2 ; 2) marqués, « y = x »
- `tangentes_horizontales` : petits traits horizontaux en (1 ; 2) et (−1 ; −2)
- `points_places` : les points (1 ; 2) et (−1 ; −2) et deux points de plus : (2 ; 2,5), (0,5 ; 2,5)
- `branche_droite` : la branche x > 0 tracée d'un trait (descend le long de x = 0, minimum, remonte en longeant y = x PAR-DESSUS)
- `branche_gauche_par_symetrie` : la branche x < 0 apparaît par symétrie de centre O (petit O entouré, « O centre de symétrie »)
- `courbe_complete` : « (Cf) » nommée
Repères : `tableau`, `case_double_barre`, `asymptote_v`, `asymptote_o`, `minimum`, `maximum`, `branche_droite`, `branche_gauche`, `centre_o`.
### vue `lecture` — la courbe complète de x + 1/x, la droite horizontale y = m (param `m` −5..5, pas 0,1, défaut 3, poignée)
- `repere_pose`, `courbe_complete`, `droite_m` (y = 3 jaune), `solutions_comptees` (les points d'intersection entourés, « f(x) = 3 : deux solutions »)
Le nombre de solutions se recalcule avec m : m > 2 ou m < −2 : 2 ; m = 2 ou −2 : 1 ; −2 < m < 2 : 0. Repères : `droite_m`, `solutions`.
### vue `etude` — f(x) = x√(x + 1) sur [−1 ; +∞[ (x ∈ [−1,5 ; 3,2], y ∈ [−1 ; 6]) ; à gauche/au-dessus le mini-tableau :
x : −1, −2/3, +∞ ; f′(x) = (3x + 2)/(2√(x + 1)) : ‖(−∞ à droite de −1) − 0 + ; f(x) : 0 ↘ −2√3/9 ↗ +∞ (−2√3/9 ≈ −0,38)
- `tableau_lu`
- `demi_tangente` : au point (−1 ; 0), flèche VERTICALE vers le BAS (taux → −∞ à droite)
- `minimum_place` : point (−2/3 ; −0,38) avec son petit trait horizontal
- `point_o` : la courbe passe par O (f(0) = 0)
- `courbe_tracee` : la courbe d'un trait
- `branche_oy` : « lim f(x)/x = +∞ : branche parabolique de direction l’axe des ordonnées au voisinage de +∞ »
Repères : `tableau`, `demi_tangente`, `minimum`, `point_o`, `branche`.

## miroir.html — f(x) = x² + 1 sur I = [0 ; +∞[ ; f⁻¹ sur J = [1 ; +∞[ : f⁻¹(x) = √(x − 1)
Repère orthonormé (même unité sur les deux axes !) x ∈ [−1 ; 7,5], y ∈ [−1 ; 7,5] — choisir w = h en pixels.
### vue `reflet`
- `repere_pose`, `courbe_f` (cyan, x ≥ 0), `miroir` (droite y = x, pointillé violet, « y = x »)
- `reflet_du_point` : A(2 ; 5) puis son reflet A′(5 ; 2), segment [AA′] pointillé perpendiculaire au miroir ; « f(2) = 5 ⟺ f⁻¹(5) = 2 »
- `courbe_reciproque` : la courbe de f⁻¹ (vert) tracée, reflet de celle de f ; « (C_{f⁻¹}) » nommée
Repères : `point_a`, `point_a2`, `miroir`, `courbe_f`, `courbe_reciproque`.
Param `x_a` (0..2,5, pas 0,05, défaut 2 ; poignée A) ; lecture « A(… ; …), A′(… ; …) ».
### vue `pentes`
- `repere_pose`, `courbe_f`, `miroir`, `courbe_reciproque` (rapides)
- `tangente_en_a` : tangente en A(2 ; 5), pente f′(2) = 4 (orange)
- `triangle_a` : triangle de pente en A : 1 à l'horizontale, 4 à la verticale
- `tangente_reflet` : tangente en A′(5 ; 2) (vert), reflet de la première
- `triangle_reflet` : triangle reflet : 4 à l'horizontale, 1 à la verticale
- `pentes_inverses` : « pente en A′ = 1/4 = 1 / f′(2) »
- `formule` : encadré « (f⁻¹)′(5) = 1 / f′(2) = 1/4 »
Repères : `point_a`, `point_a2`, `triangle_a`, `triangle_reflet`, `formule`.
Param `x_a` (0,3..2,5) : pentes f′(a) = 2a et 1/(2a) recalculées (lecture : produit = 1).
### vue `verticale`
- `repere_pose`, `courbe_f`, `miroir`, `courbe_reciproque`
- `a_glisse` : A glisse de (2 ; 5) vers (0 ; 1) avec sa tangente, et A′ glisse avec la sienne
- `tangente_horizontale` : en (0 ; 1) la tangente est horizontale (f′(0) = 0)
- `tangente_verticale` : son reflet en (1 ; 0) est VERTICAL
- `conclusion` : « f′(0) = 0 : f⁻¹ n’est pas dérivable en 1 ; il faut f′(x_0) ≠ 0 »
Repères : `point_a`, `point_a2`, `tangente_horizontale`, `tangente_verticale`, `conclusion`.
### vue `restriction`
- `repere_pose`, `parabole_entiere` (x² + 1 sur [−2,3 ; 2,3] en faible), `partie_sur_i` (la partie x ≥ 0 repassée en cyan épais, « I = [0 ; +∞[ »)
- `miroir`, `reflet_de_la_partie` (seulement cette partie est reflétée, vert), `points_echanges` ((0 ; 1) → (1 ; 0), (1 ; 2) → (2 ; 1), (2 ; 5) → (5 ; 2))
- `tangente_devient_verticale` : petite tangente horizontale en (0 ; 1), son reflet vertical en (1 ; 0)
- `intervalle_j` : « J = f(I) = [1 ; +∞[ »
Repères : `partie_sur_i`, `miroir`, `reflet`, `points`, `intervalle_j`.
