# Contrat des simulations — cours « Fonctions primitives » (math_ch4_primitives), 11 novembre 2026

Dossier des pages : `frontend\public\media\simulations\maths\primitives-tableau\`
(URL : `/media/simulations/maths/primitives-tableau/<page>.html?vue=<vue>`). Le cours cite EXACTEMENT les noms de vues,
de moments (`play_until`), de repères (`highlight`) et de paramètres ci-dessous : ne les renomme pas. Tu peux ajouter des
moments ou repères en plus, jamais en retirer. Le moment `fin` est ajouté par le kit.

## Règles communes (toutes les pages)
- Forme : copie `maths/limites-continuite-tableau/traversee.html` (même `<head>`, même barre avec UN bouton `#run`,
  `data-professor-control="start reset pause resume play_until set_time"` + ` set_parameters` si la vue a des params,
  `<p class="bulle" id="feedback">`, scripts `shared/tableau/tableau.js` → `maths/commun/exposants.js` → `maths/commun/maths-tableau.js`,
  puis `professor-locate.js` defer). Lis l'en-tête de `maths/commun/maths-tableau.js` (API `MathsTableau.page`, aide `K`).
  Ne modifie PAS le kit ni les pages des autres cours ; s'il te manque une fonction, écris-la dans ta page.
- Craie sur fond transparent, tout dans 760 × 420 ; RIEN sous y = 360 (la barre du lecteur couvre le bas) ; aucun texte
  hors cadre (`window.__horsCadre` doit rester vide). Écriture pas à pas : chaque moment = `K.marque('nom')` juste après ce
  qu'il montre ; `decrire` donne pour CHAQUE moment la phrase de ce qui se voit ; `motifs` courts ; `explication` (repère → phrase).
- Texte au tableau en français ; apostrophe typographique ’ dans les chaînes JS ; prime écrit ’ (f’, u’ : la police n'a pas ′) ;
  exposants avec les caractères ² ³ ⁴ ⁿ ⁻ (rendus par exposants.js) ou `^{…}` ; jamais de « _ » visible.
- Seulement le programme : pas d'intégrale indéfinie, pas de « ∫ f(x)dx » sans bornes, pas de « changement de variable »,
  pas d'Arctan, pas de linéarisation, pas de primitive par morceaux. La constante s'écrit k (« x ↦ x² + k, k ∈ ℝ »).
- Couleurs du kit : blanc, cyan (courbes, F), jaune (résultat, points), vert (juste, primitiver), rouge (barré, dériver),
  orange (piège, pointillés de décision), faible / tresfaible (axes, traits fins).
- Une vue avec `params` a des `poignees` (l'élève glisse un point du dessin) et une `lecture` (phrase des valeurs actuelles).
- Vérifie : `python <maths_build>\check_js.py <pages>` → ok ; serveur `python -m http.server 8898 -d frontend/public --bind 127.0.0.1`
  (en arrière-plan s'il ne répond pas), puis `python <maths_build>\test_page.py [--shot <dossier temporaire>] <url…>` sur chaque vue :
  pas d'erreur, encre, moments et repères attendus, aucun hors cadre. Regarde UNE capture par vue avec Read puis EFFACE-la
  aussitôt (disque C: presque plein : < 300 Mo libres ; aucun autre fichier, aucun téléchargement). `<maths_build>` =
  `outils\cours\notes\cours\maths_build`.

## AGENT A — ouverture.html, marche.html, famille.html, intervalle.html, pente.html

### ouverture.html (id `pr_ouverture`)
- vue `carte` — « Fonctions primitives : la carte du chapitre ». Moments, dans l'ordre :
  `centre` (au milieu « F » à gauche et « f » à droite ; flèche du haut F → f « dériver » en rouge ; flèche du bas f → F
  « primitiver » en vert) ; `verifier` (bulle « Vérifier que F est une primitive de f — 11 sujets nationaux sur 20 ») ;
  `famille` (bulle « Toutes les primitives : F(x) + k ») ; `condition` (bulle « La primitive telle que F(x₀) = y₀ ») ;
  `tableau` (bulle « Le tableau des primitives usuelles ») ; `formes` (bulle « Les formes u’uⁿ, u’/u², u’/√u, u’cos u… ») ;
  `integrale` (en bas, bulle jaune « Semestre 2 : l’intégrale — 20 sujets sur 20 »). Repères : `centre`, `verifier`, `integrale`.
- vue `plus_tard` — « Ce qui viendra ». Moments : `tableau` (trois lignes du tableau du chapitre : xⁿ → xⁿ⁺¹/(n + 1) ;
  1/√x → 2√x ; cos x → sin x) ; `ln` (« Plus tard, chapitre ln : 1/x → ln|x| ; u’/u → ln|u| », en orange) ; `exp`
  (« Plus tard, chapitre exp : eˣ → eˣ ; u’eᵘ → eᵘ ») ; `integrale` (« Semestre 2 : ∫ₐᵇ f(x)dx = F(b) − F(a) » encadré,
  avec les bornes a et b écrites). Repères : `ln`, `exp`, `integrale`.

### marche.html (id `pr_marche`)
- vue `marche` — « La marche arrière ». Moments : `avancer` (« x² » à gauche, flèche rouge « dériver » vers « 2x » à droite) ;
  `reculer` (dessous : « 2x » à droite, « ? » à gauche, une flèche verte repart de droite à gauche) ; `verifier` (le « ? »
  devient « x² » ; à côté « (x²)’ = 2x » et une coche verte) ; `nommer` (le mot « primitive » s'écrit sur la flèche verte ;
  « F » majuscule sous la gauche, « f » minuscule sous la droite ; « F’(x) = f(x) » encadré) ; `pas_egal` (« f = F » écrit
  puis barré en rouge, « on dit : F’ = f »). Repères : `fleche_deriver`, `fleche_retour`, `reponse`, `mot_primitive`, `pas_egal`.

### famille.html (id `pr_famille`)
- vue `famille` — « Une infinité de primitives ». Params `k` {min −3, max 5, pas 0.5, defaut 3, sens « hauteur de la courbe x² + k »}.
  Repère : x de −2,5 à 2,5 environ, y de −3 à 8 environ (à toi de régler). Moments : `une_primitive` (courbe de x² tracée,
  nommée « x² ») ; `trois_courbes` (x² + 2 et x² − 2 tracées en traits plus fins, nommées) ; `translation` (une courbe épaisse
  x² + k glisse verticalement d'un bloc jusqu'à k = valeur du paramètre, avec une flèche verticale et « + k ») ;
  `pentes` (en x = 1 : un pointillé vertical ; sur chaque courbe un petit segment de tangente, tous parallèles ; « même pente : 2 ») ;
  `famille` (à droite : « (x² + k)’ = 2x » puis « x ↦ x² + k, k ∈ ℝ » encadré). Poignée `k` : le sommet (0 ; k) de la courbe épaisse.
  Repères : `courbe_x2`, `trois_courbes`, `courbe_k`, `tangentes`, `legende`.
- vue `point` — « La primitive qui passe par A ». Params `k` {min −2, max 5, pas 0.5, defaut −1}. Moments : `famille_fine`
  (x² + k pour k = −2…5 en traits très fins) ; `point` (A(1 ; 3) en jaune, nommé) ; `glisser` (une courbe épaisse x² + k monte
  de k = −1 à k = 2, k affiché) ; `trouve` (elle passe par A : la courbe s'épaissit, « k = 2 ») ; `calcul` (à droite, trois lignes :
  « F(1) = 3 », « ⇔ 1² + k = 3 », « ⇔ k = 2 ») ; `une_seule` (les traits fins s'effacent ou pâlissent ; « F(x) = x² + 2 » encadré).
  Poignée `k` (sommet) ; `lecture` dit si la courbe passe par A. Repères : `point_A`, `courbe_choisie`, `calcul`, `resultat`.

### intervalle.html (id `pr_intervalle`)
- vue `trou` — « Toujours sur un intervalle ». Moments : `axe` (axe gradué de −3 à 3) ; `trou` (en 0 un rond rouge vide,
  « 1/x² n’existe pas en 0 ») ; `deux_intervalles` (]−∞ ; 0[ colorié orange, ]0 ; +∞[ colorié vert, avec leurs noms) ;
  `phrase` (« sur ℝ* » écrit puis barré en rouge ; dessous « sur ]0 ; +∞[ : x ↦ −1/x + k, k ∈ ℝ » en vert).
  Repères : `trou`, `gauche`, `droite`, `phrase`.

### pente.html (id `pr_pente`)
- vue `pente` — « La courbe de f est la pente de F ». f(x) = x² − 1 ; F(x) = x³/3 − x. Deux repères l'un au-dessus de
  l'autre, même échelle en x (−2,5 à 2,5) : en haut F (cyan), en bas f (jaune). Params `x` {min −2.4, max 2.4, pas 0.1, defaut 1.5}.
  Moments : `deux_courbes` (les deux courbes tracées et nommées « F » et « f = F’ ») ; `curseur` (un trait vertical au même x
  traverse les deux repères et glisse de −2 jusqu'à la valeur du paramètre ; la tangente à F s'y dessine ; « pente de F = f(x) = … »
  avec la valeur) ; `signes` (morceaux de f au-dessus de l'axe en vert, en dessous en orange ; au-dessus, la courbe de F repassée
  des mêmes couleurs ; « f > 0 : F monte », « f < 0 : F descend ») ; `extremums` (en x = −1 et x = 1 : f s'annule ; sommet de F
  en −1 « max », creux en 1 « min » ; tangentes horizontales). Poignée `x` (sur l'axe du bas). Repères : `courbe_F`, `courbe_f`,
  `tangente`, `signes`, `extremums`.

## AGENT B — tableau.html, cercle.html, bulle.html, organigramme.html

### tableau.html (id `pr_tableau`)
- vue `derivees` — « Ce qu’on sait : les dérivées ». Un tableau à deux colonnes « F » | « F’ » qui se remplit. Moments :
  `puissances` (x² | 2x ; x³ | 3x² ; xⁿ | nxⁿ⁻¹) ; `racine` (√x | 1/(2√x)) ; `inverse` (1/x | −1/x²) ; `trigo` (sin x | cos x ;
  cos x | −sin x). Repères : `puissances`, `racine`, `inverse`, `trigo`.
- vue `envers` — « Le tableau à l’envers ». Moments : `derivees` (à gauche, F → F’ : x² → 2x ; x³ → 3x² ; x⁴ → 4x³, flèches
  rouges « dériver ») ; `retournement` (à droite, les mêmes lignes lues à l'envers, flèches vertes « primitive » : 2x → x² ;
  3x² → x³ ; 4x³ → x⁴) ; `lecture` (la ligne 4x³ → x⁴ entourée ; « une primitive de 4x³ est x⁴ »). Repères : `gauche`, `droite`, `lecture`.
- vue `puissance` — « Monter l’exposant, diviser ». Moments : `regle` (« xⁿ → xⁿ⁺¹/(n + 1) » encadré, n ∈ ℕ*) ; `exemple`
  (« x⁵ → x⁶/6 » : l'exposant qui monte entouré en orange, le 6 du bas souligné) ; `verification` (« (x⁶/6)’ = 6x⁵/6 = x⁵ » coche
  verte) ; `constante` (« k → kx » ; « 7 → 7x »). Repères : `regle`, `exemple`, `verification`, `constante`.
- vue `inverse` — « 1/xⁿ : un moins apparaît ». Moments : `ecriture_puissance` (« 1/x² = x⁻² ») ; `pont` (« x⁻² → x⁻¹/(−1) = −1/x »,
  un pont rouge au-dessus de la flèche, le moins entouré) ; `exemple` (« 1/x⁴ = x⁻⁴ → x⁻³/(−3) = −1/(3x³) ») ; `regle`
  (« 1/xⁿ → −1/((n − 1)xⁿ⁻¹), n ≥ 2, sur ]0 ; +∞[ » encadré). Repères : `pont`, `exemple`, `regle`.
- vue `racine` — « Racines : passer en puissance ». Moments : `derivee_racine` (« (√x)’ = 1/(2√x) ») ; `fois_deux`
  (« (2√x)’ = 1/√x », donc « 1/√x → 2√x » encadré) ; `puissance_r` (« xʳ → xʳ⁺¹/(r + 1) », r ∈ ℚ*, r ≠ −1, x > 0) ;
  `exemple_cubique` (« ∛x = x^{1/3} → x^{4/3}/(4/3) = (3/4)∛(x⁴) »). Repères : `fois_deux`, `puissance_r`, `exemple_cubique`.
- vue `trigo` — « Pour mémoire : 1 + tan²x ». Moments : `derivee_tan` (« (tan x)’ = 1 + tan²x = 1/cos²x ») ; `envers`
  (« 1 + tan²x → tan x » et « 1/cos²x → tan x », flèche verte) ; `intervalle` (« sur ]−π/2 ; π/2[ » ; petite étiquette
  « pour mémoire »). Repères : `derivee_tan`, `envers`, `intervalle`.

### cercle.html (id `pr_cercle`)
- vue `cercle` — « cos et sin : le cercle ». Moments : `quatre_points` (un cercle ; « sin x » en haut, « cos x » à droite,
  « −sin x » en bas, « −cos x » à gauche) ; `deriver` (flèche rouge qui tourne dans le sens des aiguilles d'une montre,
  « dériver ») ; `primitiver` (flèche verte qui tourne dans l'autre sens, « primitiver ») ; `exemple` (à droite :
  « une primitive de sin x : −cos x » et « une primitive de cos x : sin x », encadrés). Repères : `haut`, `fleche_deriver`,
  `fleche_primitiver`, `exemple`.
- vue `ax_plus_b` — « cos(ax + b) : diviser par a ». Moments : `expression` (« cos(2x − 1) ») ; `entoure` (le 2 collé à x
  entouré en orange ; le −1 barré d'un « non » rouge) ; `divise` (« → (1/2)sin(2x − 1) ») ; `verifie`
  (« ((1/2)sin(2x − 1))’ = (1/2) × 2cos(2x − 1) = cos(2x − 1) » coche) ; `bloc` (« sin(2x − 1) est un bloc » ; une fausse
  simplification « sin(x − 1/2) » barrée en rouge). Repères : `nombre_a`, `resultat`, `verification`, `piege`.

### bulle.html (id `pr_bulle`)
- vue `bulle` — « Voir u et sa dérivée ». f(x) = (2x + 1)(x² + x − 4)³. Moments : `souligner` (x² + x − 4 souligné en rouge,
  « u ») ; `bulle` (une bulle « (x² + x − 4)’ = 2x + 1 » reliée par une flèche au facteur 2x + 1) ; `reecrire`
  (« f(x) = (x² + x − 4)’(x² + x − 4)³ » ; en face « forme u’uⁿ, n = 3 » en couleur) ; `primitive`
  (« F(x) = (x² + x − 4)⁴/4 + k » encadré). Repères : `u`, `bulle`, `forme`, `primitive`.
- vue `facteur` — « Il manque un nombre ». f(x) = (x + 1)(x² + 2x − 6)². Moments : `souligner` ; `bulle`
  (« (x² + 2x − 6)’ = 2x + 2 = 2(x + 1) ») ; `facteur` (« × 2/2 » en vert, « ½ » gardé devant) ; `reecrire`
  (« f(x) = ½(x² + 2x − 6)’(x² + 2x − 6)² ») ; `primitive` (« F(x) = ½ × (x² + 2x − 6)³/3 = (1/6)(x² + 2x − 6)³ » encadré) ;
  `manque_x` (petit encadré à part : « (x² + 1)³ : il manque 2x, pas un nombre » et une croix rouge ; « on ne prête qu’un nombre »).
  Repères : `bulle`, `facteur`, `primitive`, `manque_x`.
- vue `trois` — « Même numérateur, trois dénominateurs ». Trois colonnes : (2x + 3)/(x² + 3x − 4)², (2x + 3)/√(x² + 3x − 4),
  (2x + 3)/(x² + 3x − 4). Moments : `trois_fractions` ; `bulle` (une seule bulle « (x² + 3x − 4)’ = 2x + 3 ») ; `formes`
  (au-dessus : « u’/u² », « u’/√u », « u’/u ») ; `resultats` (dessous : « −1/(x² + 3x − 4) », « 2√(x² + 3x − 4) », et sur la
  troisième un rideau « plus tard : chapitre ln ») ; `intervalle` (un petit axe : racines −4 et 1 marquées, ]1 ; +∞[ surligné,
  « x² + 3x − 4 > 0 sur ]1 ; +∞[ »). Repères : `carre`, `racine`, `rien`, `intervalle`.

### organigramme.html (id `pr_organigramme`)
- vue `organigramme` — « Par quoi commencer ? ». En haut « je regarde f », puis quatre branches écrites l'une après l'autre :
  `somme` (« une somme de fonctions du tableau ? → chaque terme sa primitive, une seule constante k ») ; `formes_composees`
  (« u’uⁿ, u’/u², u’/√u, u’cos u, u’sin u ? (u’ à un nombre près) → la forme ») ; `produit` (« u’v + uv’ ? → uv ;
  (u’v − uv’)/v² ? → u/v ») ; `transformer` (« sinon : je transforme l’écriture : développer, séparer, puissance ») ;
  `exemple` (en bas : « 3(3x + 1)⁴ = (3x + 1)’(3x + 1)⁴ → (3x + 1)⁵/5 », une flèche vers la branche formes).
  Repères : `somme`, `formes`, `produit`, `transformer`, `exemple`.
