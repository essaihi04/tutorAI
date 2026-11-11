# Contrat des simulations — cours « Fonctions logarithmiques » (math_ch5_fonctions_ln), 11 novembre 2026

Dossier des pages : `frontend\public\media\simulations\maths\ln-tableau\`
(URL : `/media/simulations/maths/ln-tableau/<page>.html?vue=<vue>`). Le cours cite EXACTEMENT les noms de vues, de moments
(`play_until`), de repères (`highlight`) et de paramètres ci-dessous : ne les renomme pas. Tu peux ajouter des moments ou des
repères en plus, jamais en retirer. Le moment `fin` est ajouté par le kit. `calculs.html` (+ `calculs-vues.js`) est déjà faite
par l'agent du cours : n'y touche pas.

## Règles communes (toutes les pages)
- Forme : copie `maths/limites-continuite-tableau/traversee.html` et les pages finies de `maths/primitives-tableau/`
  (famille.html, pente.html, tableau.html, bulle.html : même `<head>`, même barre avec UN bouton `#run`,
  `data-professor-control="start reset pause resume play_until set_time"` + ` set_parameters` si la vue a des params,
  `<p class="bulle" id="feedback">`, scripts `shared/tableau/tableau.js` → `maths/commun/exposants.js` → `maths/commun/maths-tableau.js`,
  puis `professor-locate.js` defer). Lis l'en-tête de `maths/commun/maths-tableau.js` (API `MathsTableau.page`, aide `K`).
  Ne modifie PAS le kit ni les pages des autres cours ; s'il te manque une fonction, écris-la dans ta page.
- Craie sur fond transparent, tout dans 760 × 420 ; RIEN sous y = 360 (la barre du lecteur couvre le bas) ; aucun texte hors
  cadre (`window.__horsCadre` doit rester vide). Écriture pas à pas : chaque moment = `K.marque('nom')` juste après ce qu'il
  montre ; `decrire` donne pour CHAQUE moment la phrase de ce qui se voit ; `explication` (repère → phrase).
- Texte au tableau en français ; apostrophe typographique ’ dans les chaînes JS ; prime écrit ’ (f’, u’, ln’ : la police n'a
  pas ′) ; exposants avec ² ³ ⁿ ⁻ ʳ ˣ (exposants.js) ou `^{…}` ; indices `_{…}` (jamais de « _ » visible) ; nombres à la
  française (virgule : 0,69).
- Seulement le programme : JAMAIS les mots « équivalent », « bijection », « bijective », « logarithme de base », « logₐ »,
  « changement de base », « développement limité », « Taylor », « L’Hôpital », « intégrale ». Pas de fonction exponentielle
  dessinée (eʳ est seulement un NOMBRE : « le nombre dont le ln vaut r »). Jamais « ln 0 = » ni ln d'un négatif comme valeur.
- Couleurs du kit : blanc, cyan (courbes, F), rouge (la courbe de ln une fois nommée, barré), jaune (résultat, points), vert
  (juste, zone permise, positif), orange (piège, négatif, pointillés de décision), faible / tresfaible (axes, traits fins).
- Valeurs : ln 0,5 ≈ −0,69 ; ln 2 ≈ 0,69 ; ln 3 ≈ 1,10 ; ln 4 ≈ 1,39 ; ln 5 ≈ 1,61 ; ln 10 ≈ 2,30 ; ln 100 ≈ 4,61 ;
  ln 1000 ≈ 6,91 ; e ≈ 2,718 ; e² ≈ 7,39 ; 1/e ≈ 0,37 ; √e ≈ 1,65.
- Une vue avec `params` a des `poignees` (l'élève glisse un point du dessin) et une `lecture` (phrase des valeurs actuelles).
- Vérifie : `python <maths_build>\check_js.py <pages>` → ok ; serveur `python -m http.server 8898 -d frontend/public --bind 127.0.0.1`
  (en arrière-plan, seulement pendant les tests, ARRÊTÉ ensuite), puis `python <maths_build>\test_page.py [--shot <dossier temporaire>] <url…>`
  sur chaque vue : pas d'erreur, encre, moments et repères attendus, aucun hors cadre. Regarde UNE capture par vue avec Read puis
  EFFACE-la aussitôt (disque C: presque plein ; aucun autre fichier, aucun téléchargement ; navigateurs headless fermés).
  `<maths_build>` = `outils\cours\notes\cours\maths_build`.

## VAGUE 1 — ouverture, naissance, courbe, limites, domaine, signe

### ouverture.html (id `ln_ouverture`)
- vue `carte` — « Fonctions logarithmiques : la carte du chapitre ». Moments, dans l'ordre : `courbe` (au centre, un petit repère
  et la courbe de ln en rouge, nommée « ln », le point (1 ; 0)) ; puis des bulles autour, une par moment : `domaine` (« Où existe-t-elle ?
  u(x) > 0 ») ; `regles` (« ln(ab) = ln a + ln b ») ; `equations` (« Équations, inéquations ») ; `limites` (« Limites : ln x → +∞ ;
  (ln x)/x → 0 ») ; `derivee` (« (ln u)’ = u’/u ») ; `etude` (« Le problème : étude d’une fonction ») ; `primitives` (« u’/u → ln|u| ») ;
  `log` (« log et pH ») ; `national` (bandeau jaune en bas : « ln dans 18 sujets sur 20 ; un problème avec ln dans 12 »).
  Repères : `courbe`, `regles`, `etude`, `national`.

### naissance.html (id `ln_naissance`)
- vue `tableau` — « La règle des puissances bute sur 1/x ». Moments : `regle` (en haut, encadré « xⁿ → xⁿ⁺¹/(n + 1) ») ;
  `x2` (« x² → x³/3 ») ; `x1` (« x → x²/2 ») ; `inv2` (« 1/x² = x⁻² → x⁻¹/(−1) = −1/x ») ; `inv1` (« 1/x = x⁻¹ → x⁰/0 » :
  le « 0 » du bas entouré en rouge, la ligne barrée en rouge, « division par zéro ! ») ; `question` (en jaune « 1/x → ? »).
  Repères : `regle`, `inv2`, `zero`, `question`.
- vue `famille` — « 1/x a quand même des primitives ». Params `k` {min −2, max 2, pas 0.25, defaut 1, sens « hauteur de la courbe F + k »}.
  Deux repères l'un au-dessus de l'autre (même échelle en x, de 0 à 5 environ) : en haut 1/x (jaune), en bas les primitives.
  Moments : `inverse` (courbe de 1/x pour x > 0 tracée sans lever la craie, « continue sur ]0 ; +∞[ ») ; `existe` (à droite, en vert :
  « continue sur un intervalle ⇒ des primitives existent », dessous en orange « mais aucune formule connue ») ; `famille` (en bas,
  les courbes F + k, k = −2 … 2, traits fins (ce sont les courbes de ln x + k, NON nommées ln), étiquette « F + k ») ; `glisse` (une
  courbe épaisse cyan F + k glisse verticalement jusqu'à k = valeur du paramètre). Poignée `k` : le point d'abscisse 1 de la courbe épaisse.
  Repères : `inverse`, `existe`, `famille`.
- vue `choix` — « La primitive qui passe par (1 ; 0) s’appelle ln ». Params `k` {min −2, max 2, pas 0.25, defaut 1}. Moments :
  `famille` (F + k en traits fins) ; `point` (le point (1 ; 0) en jaune, nommé) ; `glisse` (une courbe épaisse cyan descend de k = 1
  à k = 0) ; `trouve` (elle passe par (1 ; 0) : repassée en ROUGE, nommée « ln ») ; `definition` (à droite, encadré : « ln : la primitive
  de x ↦ 1/x sur ]0 ; +∞[ qui s’annule en 1 »). Poignée `k` ; `lecture` dit si la courbe passe par (1 ; 0) (k = 0).
  Repères : `point`, `ln`, `definition`.
- vue `pente` — « Deux faits : ln 1 = 0 et (ln x)’ = 1/x ». Params `x` {min 0.3, max 5, pas 0.1, defaut 2}. Moments : `courbe`
  (la courbe de ln en rouge, le point (1 ; 0)) ; `ln1` (« ln 1 = 0 » écrit près du point) ; `tangentes` (tangentes en x = 1, 2, 4 avec
  leurs pentes écrites « 1 », « 0,5 », « 0,25 ») ; `derivee` (encadré « (ln x)’ = 1/x sur ]0 ; +∞[ ») ; `curseur` (un point glisse
  sur la courbe jusqu'à x = paramètre avec sa tangente ; « pente = 1/x = … »). Poignée `x`. Repères : `ln1`, `tangentes`, `derivee`.

### courbe.html (id `ln_courbe`) — la courbe de ln (rouge), repère x de 0 à 8 environ, y de −3 à 2,5 environ (à régler)
- vue `monte` — « ln monte toujours ». Params `x` {min 0.2, max 6, pas 0.1, defaut 4}. Moments : `points` (points (0,5 ; −0,69),
  (1 ; 0), (2 ; 0,69), (4 ; 1,39) placés, valeurs écrites) ; `trace` (la courbe se dessine en continu) ; `glisse` (un point glisse
  de x = 0,3 jusqu'à x = paramètre, sa hauteur ln x affichée, sa petite tangente montante) ; `croissante` (encadré
  « 1/x > 0 sur ]0 ; +∞[ : ln est strictement croissante »). Poignée `x`. Repères : `points`, `point_mobile`, `croissante`.
- vue `signe` — « Négatif avant 1, positif après 1 ». Moments : `courbe` ; `negatif` (le morceau sur ]0 ; 1[ repassé en orange,
  « ln x < 0 ») ; `zero` (le point (1 ; 0), « ln 1 = 0 ») ; `positif` (le morceau x > 1 repassé en vert, « ln x > 0 ») ; `tableau`
  (petit tableau de signe : x | 0 ‖ 1 +∞ ; ln x | − 0 + ; double barre en 0) ; `exemple` (« ln(3/4) < 0 car 3/4 < 1 »).
  Repères : `negatif`, `positif`, `tableau`.
- vue `e` — « Le nombre e : là où ln vaut 1 ». Moments : `courbe` ; `hauteur1` (droite horizontale y = 1 en pointillés jaunes) ;
  `lecture` (le point de la courbe à la hauteur 1, pointillé vertical jusqu'à l'axe : « e ≈ 2,718 ») ; `encadrement` (« ln 2 ≈ 0,69 < 1 »
  et « ln 3 ≈ 1,10 > 1 », points en x = 2 et x = 3 ; « donc 2 < e < 3 » encadré). Repères : `droite`, `e`, `encadrement`.
- vue `compare` — « ln compare comme x compare ». Moments : `courbe` ; `deux_points` (a = 2 et b = 5 sur l'axe, leurs hauteurs
  ln 2 et ln 5 en pointillés) ; `ordre` (« a < b ⇔ ln a < ln b » écrit, deux petites flèches dans le même ordre) ; `egal` (« ln a = ln b
  ⇔ a = b » : une seule hauteur, un seul x) ; `exemple` (« ln x < ln 5 ⇔ 0 < x < 5 », segment ]0 ; 5[ colorié vert sur l'axe, 0 et 5
  ronds vides). Repères : `deux_points`, `ordre`, `exemple`.
- vue `tangente` — « La tangente en 1 : y = x − 1 ». Moments : `courbe` ; `point` (le point (1 ; 0)) ; `tangente` (droite y = x − 1
  tracée en jaune, « pente ln’(1) = 1 ») ; `equation` (encadré « (T) : y = x − 1 ») ; `dessous` (l'écart entre (T) et la courbe hachuré
  très fin ; « la courbe reste sous (T) »). Repères : `tangente`, `equation`, `dessous`.
- vue `puissances_e` — « ln(eʳ) = r ». Repère x jusqu'à 8. Moments : `courbe` ; `e` (point (e ; 1), « ln e = 1 ») ; `e2` (point
  (e² ≈ 7,4 ; 2), « ln(e²) = 2 ») ; `inv_e` (point (1/e ≈ 0,37 ; −1), « ln(1/e) = −1 ») ; `racine_e` (point (√e ≈ 1,6 ; 0,5),
  « ln √e = ½ ») ; `regle` (encadré « ln(eʳ) = r » et dessous « eʳ : le nombre dont le ln vaut r »). Repères : `e2`, `inv_e`, `regle`.

### limites.html (id `ln_limites`)
- vue `lente` — « ln x → +∞, mais lentement ». L'échelle se dézoome. Moments : `zoom_10` (courbe sur [0 ; 10], « ln 10 ≈ 2,3 ») ;
  `zoom_100` (échelle [0 ; 100], « ln 100 ≈ 4,6 ») ; `zoom_1000` (échelle [0 ; 1000], « ln 1000 ≈ 6,9 ») ; `fois_dix` (« x × 10 ⇒
  ln x + 2,3 ») ; `limite` (encadré « lim_{x→+∞} ln x = +∞ ») ; `branche` (« branche parabolique de direction l’axe des abscisses »).
  Repères : `zoom_1000`, `limite`, `branche`.
- vue `plonge` — « En 0 à droite : ln x → −∞ ». Moments : `courbe` ; `zoom_0` (points x = 0,1 → −2,3 ; x = 0,01 → −4,6 ; la courbe
  plonge le long de l'axe des ordonnées) ; `asymptote` (la droite x = 0 en pointillés orange, « asymptote verticale : x = 0 ») ;
  `limite` (encadré « lim_{x→0⁺} ln x = −∞ ») ; `jamais` (« la courbe ne coupe jamais l’axe des ordonnées : 0 ∉ ]0 ; +∞[ »).
  Repères : `asymptote`, `limite`, `jamais`.
- vue `course` — « (ln x)/x → 0 : x l’emporte ». Params `x` {min 1, max 1000, pas 1, defaut 1000}. Les courbes ln x (rouge),
  √x (cyan), x (blanc) ensemble. Moments : `trois_courbes` (les trois tracées et nommées) ; `rapport` (un curseur x avance de 1 à la
  valeur du paramètre : trois hauteurs affichées et « (ln x)/x = … » (0,23 en 10 ; 0,0069 en 1000)) ; `limite` (encadré
  « lim_{x→+∞} (ln x)/x = 0 »). Poignée `x`. Repères : `trois_courbes`, `rapport`, `limite`.
- vue `zero_plus` — « x ln x → 0 en 0 à droite ». Moments : `tableau` (trois lignes de valeurs : x = 0,1 → −0,23 ; 0,01 → −0,046 ;
  0,001 → −0,0069) ; `rectangle` (un rectangle de côtés x et |ln x| qui s'écrase quand x → 0 : largeur de plus en plus fine) ;
  `signe` (« pour 0 < x < 1 : x ln x < 0 ») ; `limite` (encadré « lim_{x→0⁺} x ln x = 0 »). Repères : `tableau`, `rectangle`, `limite`.
- vue `nombre_derive` — « Deux limites qui sont un nombre dérivé ». Params `x` {min 1.05, max 3, pas 0.05, defaut 1.2}.
  Moments : `courbe` (ln et le point A(1 ; 0)) ; `secante` (un point M(x ; ln x), la sécante (AM), « (ln x − ln 1)/(x − 1) ») ;
  `approche` (M glisse vers A, x de 2,5 jusqu'à la valeur du paramètre ; la pente de (AM) s'affiche et tend vers 1 ; la tangente y = x − 1
  apparaît en pointillés) ; `limite` (encadré « lim_{x→1} (ln x)/(x − 1) = 1 ») ; `seconde` (dessous « x = 1 + h : lim_{x→0} ln(1 + x)/x = 1 »).
  Poignée `x`. Repères : `secante`, `limite`, `seconde`.

### domaine.html (id `ln_domaine`) — un axe gradué à la craie, des zones colorées, des ronds vides pour les bornes exclues
- vue `une` — « Une condition par ln : u(x) > 0 ». « f(x) = ln(2x − 6) ». Moments : `entoure` (2x − 6 entouré, flèche « > 0 ») ;
  `condition` (« x ∈ D_f ⇔ 2x − 6 > 0 ⇔ x > 3 ») ; `zone` (sur l'axe, ]3 ; +∞[ colorié vert, rond vide en 3) ; `resultat`
  (encadré « D_f = ]3 ; +∞[ »). Repères : `entoure`, `zone`, `resultat`.
- vue `et` — « Plusieurs conditions : et ». « f(x) = (1 + ln x)/ln x ». Moments : `conditions` (« x > 0 (ln existe) » et
  « ln x ≠ 0 ⇔ x ≠ 1 (dénominateur) ») ; `zones` (sur l'axe : x > 0 colorié vert, un rond vide rouge en 1) ; `et` (le mot « et »
  entouré ; « ou » écrit puis barré en rouge) ; `resultat` (encadré « D_f = ]0 ; 1[ ∪ ]1 ; +∞[ »). Repères : `et`, `trou`, `resultat`.
- vue `valeur_absolue` — « ln|u| : une condition, u ≠ 0 ». « f(x) = ln|x − 2| ». Moments : `entoure` (« |x − 2| > 0 ⇔ x ≠ 2 ») ;
  `axe` (tout l'axe colorié vert sauf un rond vide en 2) ; `resultat` (encadré « D_f = ]−∞ ; 2[ ∪ ]2 ; +∞[ ») ; `piege` (en orange,
  à côté : « ln(x − 2) : seulement x > 2 », un petit axe où seul ]2 ; +∞[ est colorié). Repères : `axe`, `resultat`, `piege`.
- vue `tri` — « ln a = ln b : le domaine d’abord ». « ln(x − 1) + ln(x + 2) = ln 4 ». Moments : `conditions` (deux demi-droites
  colorées : x > 1 en vert, x > −2 en cyan) ; `intersection` (la partie commune ]1 ; +∞[ repassée épaisse ; « D = ]1 ; +∞[ ») ;
  `solutions` (−3 et 2 posés sur l'axe en jaune ; « x² + x − 6 = 0 ⇔ x = 2 ou x = −3 ») ; `tri` (−3 hors de la zone : barré en
  rouge ; 2 entouré en vert) ; `resultat` (encadré « S = {2} »). Repères : `intersection`, `barre`, `resultat`.
- vue `inequation` — « Inéquation : ln garde le sens ». « ln(2x − 1) < 0 ». Moments : `domaine` (x > ½ colorié cyan) ; `resoudre`
  (« ln(2x − 1) < ln 1 ⇔ 2x − 1 < 1 ⇔ x < 1 » ; x < 1 colorié vert) ; `intersection` (]½ ; 1[ repassé épais jaune) ; `resultat`
  (encadré « S = ]½ ; 1[ »). Repères : `domaine`, `intersection`, `resultat`.
- vue `produit_nul` — « Produit nul avec ln ». « 2x ln x − 2x = 0 sur ]0 ; +∞[ ». Moments : `factoriser` (« 2x(ln x − 1) = 0 ») ;
  `deux` (« x = 0 ou ln x = 1 ⇔ x = 0 ou x = e ») ; `axe` (]0 ; +∞[ colorié vert, rond vide en 0) ; `tri` (0 barré en rouge, e entouré
  en vert) ; `resultat` (encadré « S = {e} »). Repères : `axe`, `barre`, `resultat`.

### signe.html (id `ln_signe`) — tableaux de signe et de variations à la craie, case par case
- vue `quotient` — « Un quotient dans ln : tableau de signe ». « f(x) = ln(5x/(3 − x)) ». Moments : `condition` (« x ∈ D_f ⇔
  5x/(3 − x) > 0 et 3 − x ≠ 0 ») ; `racines` (« 5x = 0 ⇔ x = 0 ; 3 − x = 0 ⇔ x = 3 ») ; `tableau` (x : −∞ 0 3 +∞ ; 5x : − 0 + + ;
  3 − x : + + 0 − ; 5x/(3 − x) : − 0 + ‖ −, double barre sous 3) ; `zone` (la colonne entre 0 et 3 surlignée en vert) ;
  `resultat` (encadré « D_f = ]0 ; 3[ »). Repères : `tableau`, `double_barre`, `resultat`.
- vue `derivee` — « Le signe de f’ : celui de 1 − ln x ». « f’(x) = (1 − ln x)/x² ». Moments : `denominateur` (« x² > 0 : f’(x) a le
  signe de 1 − ln x ») ; `resoudre` (« 1 − ln x > 0 ⇔ ln x < 1 ⇔ 0 < x < e ») ; `tableau` (x : 0 ‖ e +∞ ; 1 − ln x : + 0 − ;
  f’(x) : + 0 −) ; `double_barre` (la double barre sous 0 entourée en orange : « x > 0 : le tableau commence à 0 ») ; `variations`
  (ligne f : flèche montante puis descendante). Repères : `resoudre`, `tableau`, `double_barre`.
- vue `auxiliaire` — « La partie I donne le signe de f’ ». Moments : `g` (le tableau de signe de g donné : x : 0 ‖ 1 +∞ ;
  g(x) : − 0 +) ; `quotient` (« f’(x) = g(x)/x² et x² > 0 : f’(x) a le signe de g(x) ») ; `fprime` (ligne f’(x) : − 0 +) ;
  `variations` (ligne f : flèche descendante puis montante). Repères : `g`, `fprime`, `variations`.
- vue `variations` — « Limites aux bornes et tableau ». « f(x) = x + ½ − ln x + ½(ln x)² ». Moments : `tableau_vide`
  (x : 0 ‖ 1 +∞ ; f’(x) : − 0 +) ; `fleches` (ligne f : descend jusqu'à 3/2 en 1, puis monte ; « f(1) = 3/2 ») ; `limite_0`
  (+∞ en haut à gauche ; « lim_{x→0⁺} f(x) = +∞ ») ; `asymptote` (« x = 0 : asymptote verticale ») ; `limite_inf` (+∞ en haut à droite).
  Repères : `limite_0`, `minimum`, `limite_inf`.

## VAGUE 2 — produit, inegalite, etude, uprime, log, bilan, carte

### produit.html (id `ln_produit`)
- vue `translation` — « Multiplier x par a, c’est monter la courbe de ln a ». Params `a` {min 0.5, max 4, pas 0.5, defaut 2}.
  Moments : `deux_courbes` (ln x en rouge et ln(2x) en cyan, nommées) ; `fleches` (flèches verticales de même longueur entre les
  deux courbes en x = 1, 2, 4 : « + ln 2 ») ; `empile` (en x = 2 : la hauteur de ln(2 × 2) = ln 4 faite de deux segments empilés,
  ln 2 (rouge) puis ln 2 (jaune)) ; `parametre` (la courbe ln(ax) glisse jusqu'à a = paramètre ; pour a < 1 elle descend ; « + ln a ») ;
  `formule` (encadré « ln(ab) = ln a + ln b, a > 0, b > 0 »). Poignée `a`. Repères : `fleches`, `empile`, `formule`.

### inegalite.html (id `ln_inegalite`)
- vue `ecart` — « Prouver ln x ≤ x − 1 ». Params `x` {min 0.2, max 5, pas 0.1, defaut 3}. Moments : `courbe` (ln en rouge) ;
  `tangente` (y = x − 1 en jaune) ; `ecart` (segment vertical entre la droite et la courbe en x = paramètre ;
  « g(x) = x − 1 − ln x = … », valeur ≥ 0) ; `tableau` (à droite, tableau de g : x : 0 ‖ 1 +∞ ; g’(x) : − 0 + ; g : descend à 0 en 1, monte) ;
  `minimum` (encadré « g(1) = 0 minimum ⇒ g(x) ≥ 0 ⇒ ln x ≤ x − 1 »). Poignée `x`. Repères : `ecart`, `tableau`, `minimum`.

### etude.html (id `ln_etude`)
- vue `position` — « Position par rapport à y = x ». f(x) = x + ½ − ln x + ½(ln x)² (2019 N). Moments : `repere` ; `asymptote`
  (x = 0 en pointillés orange) ; `droite` ((Δ) : y = x, nommée) ; `ecart` (« f(x) − x = ½(ln x − 1)² ≥ 0 » écrit ; petits segments
  verticaux entre (Δ) et (C)) ; `contact` (le point (e ; e) en jaune, « contact en x = e ») ; `courbe` ((C) tracée au-dessus de (Δ),
  minimum (1 ; 3/2) marqué). Repères : `droite`, `contact`, `courbe`.
- vue `national` — « Un problème du national, 2021 ». f(x) = 2x ln x − 2x sur [0 ; +∞[, f(0) = 0. Moments : `repere` ; `origine`
  (le point O, « f(0) = 0 », demi-tangente verticale en 0) ; `minimum` (le point (1 ; −2), « minimum f(1) = −2 ») ; `zero` (le point
  (e ; 0)) ; `courbe` ((C) tracée) ; `inegalite` (encadré « ln x ≥ (x − 1)/x pour x > 0 »). Repères : `minimum`, `courbe`, `inegalite`.

### uprime.html (id `ln_uprime`)
- vue `tableau` — « À l’envers : u’/u a pour primitive ln u ». Moments : `ancien` (le tableau f → F du chapitre des primitives :
  « xⁿ → xⁿ⁺¹/(n + 1) » ; « u’uⁿ → uⁿ⁺¹/(n + 1) » ; « u’/u² → −1/u ») ; `nouveau` (lignes nouvelles en vert : « 1/x → ln x (x > 0) » ;
  « u’/u → ln u (u > 0) ») ; `exemple` (« 2x/(x² + 1) : u = x² + 1, u’ = 2x » puis « → ln(x² + 1) ») ; `verifier`
  (« (ln(x² + 1))’ = 2x/(x² + 1) ✓ »). Repères : `nouveau`, `exemple`, `verifier`.
- vue `miroir` — « ln|u| quand u est négatif ». Moments : `inverse` (courbe de 1/x sur les deux intervalles) ; `ln` (la courbe de
  ln x pour x > 0, en rouge) ; `miroir` (la courbe de ln(−x) pour x < 0, symétrique par rapport à l'axe des ordonnées, en cyan,
  pointillé sur l'axe « miroir ») ; `valeur_absolue` (encadré « 1/x → ln|x| sur chaque intervalle » et « u’/u → ln|u| ») ;
  `exemple` (« sur ]−∞ ; 3[ : 1/(x − 3) → ln|x − 3| = ln(3 − x) »). Repères : `miroir`, `valeur_absolue`, `exemple`.

### log.html (id `ln_log`)
- vue `regle` — « Le logarithme décimal ». Moments : `deux_courbes` (ln et log = ln / ln 10, plus aplatie, sur [0 ; 12]) ;
  `points` ((10 ; 1) sur log, (1 ; 0) commun) ; `regle` (une règle graduée : en haut 1, 10, 100, 1000 ; en bas 0, 1, 2, 3 ;
  « × 10 ⇒ + 1 ») ; `formule` (encadré « log x = ln x / ln 10 » ; dessous « log 1 = 0 ; log 10 = 1 ; log(10ⁿ) = n »).
  Repères : `deux_courbes`, `regle`, `formule`.
- vue `ph` — « 10ˣ = a ; le pH ». Moments : `equation` (« 10ˣ = 5 ⇔ x = log 5 ≈ 0,70 ») ; `regle` (une règle : 10⁻¹, 10⁻², 10⁻³,
  10⁻⁴ en face de pH 1, 2, 3, 4) ; `ph` (encadré « pH = −log[H₃O⁺] » ; « pH = 3 ⇒ [H₃O⁺] = 10⁻³ mol/L »). Repères : `equation`, `regle`, `ph`.

### bilan.html (id `ln_bilan`) — copie `maths/primitives-tableau/bilan.html` (fiche « Ce qu’il faut retenir », page 2 de l'élève,
set_parameters {lacunes, acquis, acquis_ids}, imprimer) ; un moment par bloc (ids ci-dessous), `fiche`, `lacunes`. Neuf blocs
(deux pages de fiche si besoin, mais RIEN sous y = 360) :
  1. `definition` · Définition, courbe — K1, K8 — def « ln est la primitive de x ↦ 1/x sur ]0 ; +∞[ qui s’annule en 1 ; elle est
     strictement croissante. » — formules « ln 1 = 0 ; (ln x)’ = 1/x », « ln e = 1 (e ≈ 2,718) », « y = x − 1 (tangente en 1) » —
     attention « ln x < 0 sur ]0 ; 1[ : x > 0 ne suffit pas. »
  2. `domaine` · Ensemble de définition — K2 — def « Chaque ln demande ce qu’il contient strictement positif ; les conditions se
     relient par « et ». » — formules « x ∈ D_f ⇔ u(x) > 0 » — attention « Le tableau de signe commence à 0 si x > 0 ; ln|u| : u ≠ 0. »
  3. `regles` · Règles de calcul — K3 — def « ln transforme un produit en somme (a > 0, b > 0). » — formules « ln(ab) = ln a + ln b »,
     « ln(a/b) = ln a − ln b », « ln(aⁿ) = n ln a ; ln √a = ½ ln a », « ln(eʳ) = r » — attention « ln(a + b) ≠ ln a + ln b ; ln(x²) = 2 ln|x|. »
  4. `equations` · Équations, inéquations — K4 — def « D’abord le domaine, puis on enlève les ln, puis on trie les solutions. » —
     formules « ln a = ln b ⇔ a = b », « ln a < ln b ⇔ a < b », « ln x = r ⇔ x = eʳ » — attention « Une solution hors du domaine
     n’est pas une solution. »
  5. `limites` · Limites de base — K5 — def « x l’emporte sur ln x. » — formules « lim_{x→+∞} ln x = +∞ ; lim_{x→0⁺} ln x = −∞ »,
     « lim_{x→+∞} (ln x)/x = 0 ; lim_{x→0⁺} x ln x = 0 », « lim_{x→0} ln(1 + x)/x = 1 » — attention « (ln x)/x ne tend pas vers 1 ;
     x = 0 est asymptote verticale. »
  6. `derivee` · Dérivée de ln u — K6 — def « La dérivée de ln u, c’est la dérivée de l’intérieur sur l’intérieur. » — formules
     « (ln u)’ = u’/u (u > 0 sur I) » — attention « ((ln x)²)’ = 2 ln x / x, pas 2 ln x. »
  7. `primitives` · Primitives u’/u — K7 — def « Quand le haut est la dérivée du bas, la primitive est ln du bas. » — formules
     « u’/u → ln|u| », « 1/x → ln x sur ]0 ; +∞[ » — attention « 1/(x² + 1) n’est pas de la forme u’/u. »
  8. `etude` · Étude, inégalités — K8 — def « Le signe de f’ vient de g ; une inégalité se prouve par une fonction auxiliaire. » —
     formules « ln x ≤ x − 1 pour tout x > 0 » — attention « Interpréter chaque limite : asymptote ou branche. »
  9. `log` · Logarithme décimal — K9 — def « log x = ln x / ln 10 : mêmes règles que ln, log 10 = 1. » — formules
     « log x = ln x / ln 10 », « 10ˣ = a ⇔ x = log a (a > 0) » — attention « pH = −log[H₃O⁺] : le moins devant. »

### carte.html (id `ln_carte`) — copie `maths/primitives-tableau/carte.html` ; centre « ln : la primitive de 1/x sur ]0 ; +∞[ qui
s’annule en 1 » (moment `centre`), puis neuf branches, une par moment, dans cet ordre, chacune avec sa notion, sa formule et sa
compétence (pour l'anneau « à reprendre ») : `courbe` (« ln 1 = 0, ln e = 1, croissante » — K1) ; `domaine` (« u(x) > 0 » — K2) ;
`regles` (« ln(ab) = ln a + ln b » — K3) ; `equations` (« ln a = ln b ⇔ a = b » — K4) ; `limites` (« (ln x)/x → 0 » — K5) ;
`derivee` (« (ln u)’ = u’/u » — K6) ; `primitives` (« u’/u → ln|u| » — K7) ; `etude` (« ln x ≤ x − 1 » — K8) ; `log`
(« log x = ln x / ln 10 » — K9).
