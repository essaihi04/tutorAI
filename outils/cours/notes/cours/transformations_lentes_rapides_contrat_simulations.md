# Contrat des simulations — transformations_lentes_rapides (cours phys_ch9_transformations_lentes_rapides)

Dossier : `frontend/public/media/simulations/chimie/transformations-lentes-rapides-tableau/`
Kit : copier `commun.js` et `exposants.js` de `physics/circuit-rlc-tableau/` (même API : `Tableau`, `Craie`, scène 760 × 420,
`Tableau.protocole`, `craie.repere`, `play_until`, `__horsCadre`) ; une feuille `tlr.css` (copie de `rlc.css`). Skill : simulations-au-tableau.
Modèle de page : `physics/circuit-rlc-tableau/circuit-lc.html` (vues par `?vue=`, moments, repères, ce_qui_se_voit, bulle « Arrêt sur image »).

Règles communes
- Fond transparent, un seul bouton en haut (Lancer → Pause → Reprendre → Rejouer), bande du bas libre (4,5 em), rien hors du cadre 760 × 420.
- Les solutions sont PEINTES (vraies couleurs, dégradé, ménisque, reflet léger) dans des béchers dessinés ; la craie écrit les textes.
  Couleurs : permanganate violet (#7b2a8c), Mn²⁺ presque incolore, diiode jaune → brun (#8a4b12 au maximum), Cu²⁺ bleu (#3a7bd5),
  dépôt de cuivre rouge-brun (#b5562b), Fe²⁺ vert très pâle, Fe³⁺ jaune-orangé, soufre : trouble blanc-jaune qui cache une croix noire.
  Craie : blanc pour le texte, jaune = surlignage, orange = piège « ⚠ », vert = réducteur / électrons cédés, rouge = oxydant / électrons captés.
- Formules chimiques avec indices et charges rendus (exposants.js) : MnO₄⁻, Mn²⁺, H₂O₂, I₂, I⁻, S₂O₈²⁻, SO₄²⁻, S₂O₃²⁻, S₄O₆²⁻,
  H₂C₂O₄, CO₂, Fe²⁺, Fe³⁺, Cu²⁺, Zn²⁺, H⁺, H₂O, e⁻. Double flèche des demi-équations : DESSINÉE (deux demi-flèches), pas le caractère ⇌.
  Flèche de la réaction : dessinée aussi (→).
- Jamais : chocs efficaces, énergie d'activation, ordre, loi de vitesse, nombre d'oxydation, « barrière », types de catalyse.
- Chaque vue émet `moments` (noms ci-dessous, EXACTS), accepte `play_until {moment}`, `set_time`, `set_parameters` (si poignée),
  `highlight {target}` ; `ce_qui_se_voit` dit l'étape, la couleur, le temps simulé et la température ; tous les repères ci-dessous
  sont déclarés (`craie.repere`) au plus tard au moment indiqué (sinon dès le début). Chaque vue a aussi le moment `fin`.

## 1. transfert.html (vues zinc | couple)
- `?vue=zinc` — bécher de sulfate de cuivre bleu, lame de zinc grise ; en temps accéléré : dépôt rouge sur la lame, le bleu pâlit ;
  loupe (cercle) : un atome Zn cède 2 e⁻ (flèches vertes) à un ion Cu²⁺ (rouge) qui devient Cu ; un Zn²⁺ part en solution.
  Moments : `depart` `depot` `palit` `loupe` `electrons` `etiquettes` `bilan` `fin`.
  (`etiquettes` : « Zn : réducteur, cède 2 e⁻ », « Cu²⁺ : oxydant, capte 2 e⁻ » ; `bilan` : Zn + Cu²⁺ → Zn²⁺ + Cu écrit à la craie.)
  Repères : `becher` `lame` `solution` `depot` `loupe` `atome_zn` `ion_cu` `fleche_electrons` `ion_zn` `etiquette_reducteur` `etiquette_oxydant` `equation`.
- `?vue=couple` — une balance : à gauche « Ox + n e⁻ », à droite « Red », la double flèche ; exemples qui défilent Cu²⁺/Cu, Zn²⁺/Zn, I₂/I⁻.
  Moments : `oxydant` `gagne` `reducteur` `perd` `couple` `exemples` `oxydation_reduction` `fin`.
  (`gagne` : flèche → « réduction : gain d'électrons » ; `perd` : flèche ← « oxydation : perte d'électrons » ; `oxydation_reduction` : les deux mots encadrés.)
  Repères : `ox` `red` `electrons` `double_fleche` `sens_reduction` `sens_oxydation` `couple_cu` `couple_zn` `couple_i` `definition`.

## 2. demi-equation.html (vues permanganate | eau_oxygenee | iode | oxalique)
Les quatre gestes, une ligne de craie par geste, les ajouts en jaune ; à droite une petite « balance des charges » (gauche / droite).
Moments (toutes les vues, dans cet ordre) : `couple` `atomes` `oxygene` `hydrogene` `charges` `verifier` `fin`.
(vue iode : `oxygene` et `hydrogene` affichent « pas d'oxygène : rien à faire » / « pas d'hydrogène : rien à faire ».)
- permanganate : MnO₄⁻ ⇌ Mn²⁺ → + 4H₂O → 8H⁺ + → charges +7 / +2 → 5e⁻ → MnO₄⁻ + 8H⁺ + 5e⁻ ⇌ Mn²⁺ + 4H₂O ; vérif +2 = +2.
- eau_oxygenee : H₂O₂ ⇌ H₂O → 2H₂O → 2H⁺ → charges +2 / 0 → 2e⁻ → H₂O₂ + 2H⁺ + 2e⁻ ⇌ 2H₂O.
- iode : I₂ ⇌ I⁻ → 2I⁻ (atomes) → charges 0 / −2 → 2e⁻ → I₂ + 2e⁻ ⇌ 2I⁻.
- oxalique : CO₂ ⇌ H₂C₂O₄ → 2CO₂ (atomes C) → O : 4 et 4, rien → 2H⁺ → charges +2 / 0 → 2e⁻ → 2CO₂ + 2H⁺ + 2e⁻ ⇌ H₂C₂O₄.
Repères : `ligne_couple` `ligne_atomes` `ligne_oxygene` `ligne_hydrogene` `ligne_charges` `charge_gauche` `charge_droite` `electrons` `resultat` `balance`.

## 3. equation.html (vues zinc_cuivre | eau_oxygenee | permanganate | fer)
Deux demi-équations l'une sous l'autre (réduction de l'oxydant en rouge, oxydation du réducteur en vert, écrite dans le sens de la réaction),
facteurs « × n » en jaune, trait d'addition, bilan, électrons barrés, H⁺ / H₂O simplifiés, vérification des charges.
Moments (toutes les vues) : `couples` `reduction` `oxydation` `multiplier` `additionner` `simplifier` `verifier` `fin`.
- zinc_cuivre : Cu²⁺ + 2e⁻ → Cu ; Zn → Zn²⁺ + 2e⁻ ; × 1 et × 1 ; Zn + Cu²⁺ → Zn²⁺ + Cu ; rien à simplifier ; charges +2 / +2.
- eau_oxygenee : H₂O₂ + 2H⁺ + 2e⁻ → 2H₂O ; 2I⁻ → I₂ + 2e⁻ ; × 1 ; H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O ; charges 0 / 0.
- permanganate : MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O (× 2) ; H₂C₂O₄ → 2CO₂ + 2H⁺ + 2e⁻ (× 5) ; 10 e⁻ ;
  2MnO₄⁻ + 16H⁺ + 5H₂C₂O₄ → 2Mn²⁺ + 8H₂O + 10CO₂ + 10H⁺ ; simplifier : 2MnO₄⁻ + 5H₂C₂O₄ + 6H⁺ → 2Mn²⁺ + 10CO₂ + 8H₂O ; charges +4 / +4.
- fer : MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O (× 1) ; Fe²⁺ → Fe³⁺ + e⁻ (× 5) ; MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O ; charges +17 / +17.
Repères : `demi_1` `demi_2` `facteur_1` `facteur_2` `electrons_1` `electrons_2` `trait` `bilan` `simplification` `charges` `oxydant` `reducteur`.

## 4. bechers.html (vues comparer | lente | soufre | echelle)
- `?vue=comparer` — deux béchers violets (permanganate acidifié) ; à gauche on verse les ions fer II : décoloré aussitôt ; à droite l'acide
  oxalique : la couleur pâlit en quelques minutes (temps accéléré, chronomètre à la craie, minutes simulées).
  Moments : `depart` `verser` `rapide_fini` `lente_continue` `lente_finie` `fin`.
  Repères : `becher_rapide` `becher_lent` `burette_fer` `burette_oxalique` `chrono` `etiquette_rapide` `etiquette_lente`.
- `?vue=lente` — un bécher d'eau oxygénée acidifiée + iodure : incolore → jaune → brun, une barre de teinte à côté ; chrono.
  Moments : `melange` `jaune` `brun` `palier` `fin`. Repères : `becher` `teinte` `chrono` `etiquette`.
- `?vue=soufre` — thiosulfate + acide sur une croix noire dessinée sous le bécher : le trouble monte, la croix disparaît.
  Moments : `melange` `trouble` `croix_cachee` `fin`. Repères : `becher` `croix` `trouble` `chrono`.
- `?vue=echelle` — une flèche du temps à la craie : « instantanée (moins d'une seconde) » — « lente (secondes → heures) » — « très lente
  (jours, années) » ; trois vignettes : bécher qui se décolore d'un coup, bécher qui brunit, portail rouillé.
  Moments : `axe` `rapide` `lente` `tres_lente` `appareils` `fin` (`appareils` : « le classement dépend des moyens d'observation »).
  Repères : `axe_temps` `case_rapide` `case_lente` `case_tres_lente` `portail` `phrase`.

## 5. facteurs.html (vues temperature | concentration | trempe | une_variable | vie | catalyseur)
- `?vue=temperature` — deux béchers du même mélange (H₂O₂ + I⁻ acidifié) dans deux bains : « 20 °C » (eau tiède) et « 40 °C » (eau chaude,
  vapeur légère) ; thermomètres ; teinte brune qui fonce ; à 40 °C la teinte finale est atteinte trois fois plus tôt ; même brun final ;
  loupe facultative : entités qui s'agitent plus vite au chaud (points qui bougent, jamais le mot « choc »).
  Moments : `melange` `depart` `chaud_avance` `chaud_fini` `froid_fini` `meme_final` `agitation` `fin`. Poignée : température du bain chaud
  (`theta_c` 30..60 °C, défaut 40) → durée ∝ 3^((20 − θ)/20) (pour l'œil, pas une loi, dit en commentaire).
  Repères : `becher_froid` `becher_chaud` `thermometre_froid` `thermometre_chaud` `chrono` `teinte_froid` `teinte_chaud` `loupe` `poignee_theta`.
- `?vue=concentration` — même température (20 °C), [I⁻]₀ = 0,1 mol/L et 0,2 mol/L (H₂O₂ limitant, même quantité) : le plus concentré brunit
  plus vite, même brun final ; loupe : plus d'entités dans le même volume.
  Moments : `melange` `depart` `concentre_avance` `concentre_fini` `dilue_fini` `meme_final` `rencontres` `fin`.
  Repères : `becher_dilue` `becher_concentre` `etiquette_dilue` `etiquette_concentre` `chrono` `loupe`.
- `?vue=trempe` — un grand bécher qui brunit ; une pipette prélève ; le prélèvement est versé dans un bécher d'eau glacée (glaçons) :
  sa teinte ne bouge plus pendant que le grand bécher continue de foncer ; puis « titrage par le thiosulfate (réaction rapide) ».
  Moments : `reaction` `prelevement` `eau_glacee` `fige` `continue` `titrage` `fin`.
  Repères : `grand_becher` `pipette` `becher_glace` `glacons` `teinte_figee` `teinte_continue` `burette` `phrase`.
- `?vue=une_variable` — un tableau à la craie de trois expériences : 1 (20 °C ; 0,1 mol/L), 2 (40 °C ; 0,1 mol/L), 3 (40 °C ; 0,2 mol/L) ;
  surlignage des colonnes ; flèches « 1 → 2 : seule la température change », « 2 → 3 : seule la concentration change », « 1 → 3 : deux
  changements, on ne conclut pas » (en orange ⚠).
  Moments : `tableau` `comparer_1_2` `comparer_2_3` `comparer_1_3` `conclusion` `fin`.
  Repères : `tableau` `ligne_1` `ligne_2` `ligne_3` `colonne_theta` `colonne_c` `fleche_12` `fleche_23` `fleche_13` `conclusion`.
- `?vue=vie` — à gauche un réfrigérateur avec une bouteille de lait (« au froid : plus lent »), à droite un autocuiseur sur le feu
  (« plus de 100 °C : plus rapide ») ; un thermomètre au milieu.
  Moments : `frigo` `lait` `autocuiseur` `vapeur` `conclusion` `fin`. Repères : `frigo` `lait` `autocuiseur` `flamme` `thermometre` `conclusion`.
- `?vue=catalyseur` — deux béchers du même mélange (peroxodisulfate + iodure, incolore), même température 20 °C ; dans le second on verse
  quelques gouttes d'une solution d'ions fer II (« catalyseur ») : il brunit beaucoup plus vite ; les deux finissent au même brun ;
  à la craie : « le catalyseur accélère », « il ne figure pas dans l'équation », « même état final ».
  Moments : `melange` `ajout` `catalyse_avance` `catalyse_fini` `sans_fini` `meme_final` `equation` `fin`.
  Repères : `becher_sans` `becher_avec` `gouttes` `chrono` `teinte_sans` `teinte_avec` `equation` `phrase`.

## 6. courbes.html (vues temperature | concentration | catalyseur | lecture)
Axes à la craie : n(I₂) en mmol (ordonnée) et t en min (abscisse) ; palier n_f = 2 mmol ; quadrillage léger.
Modèle pour l'œil : n(t) = n_f·(1 − e^(−t/τ)) avec τ = 6 min (20 °C, 0,1 mol/L), τ = 2 min (40 °C), τ = 3 min (0,2 mol/L) ; jamais de formule
écrite, jamais « exponentielle » ni τ à l'écran.
- `?vue=temperature` — Moments : `axes` `courbe_froid` `courbe_chaud` `meme_palier` `plus_raide` `fin`.
  Repères : `axe_t` `axe_n` `courbe_froid` `courbe_chaud` `palier` `debut` `etiquette_froid` `etiquette_chaud`.
- `?vue=concentration` — courbe 0,1 mol/L puis 0,2 mol/L (même palier : H₂O₂ limitant) ; puis en orange pointillé « si on double le réactif
  limitant H₂O₂ : palier double (4 mmol) » (moment `piege`).
  Moments : `axes` `courbe_dilue` `courbe_concentre` `meme_palier` `piege` `fin`.
  Repères : `axe_t` `axe_n` `courbe_dilue` `courbe_concentre` `palier` `courbe_piege`.
- `?vue=catalyseur` — comme le national 2023 N : ordonnée x en mol, palier x_f = 0,3 mol ; deux courbes C₁ (avec catalyseur, τ = 2 min) et
  C₂ (sans, τ = 8 min), même température ; puis en orange ⚠ « ne pas choisir le palier le plus haut : ici même palier ».
  Moments : `axes` `courbe_C2` `courbe_C1` `meme_palier` `plus_tot` `piege` `fin`.
  Repères : `axe_t` `axe_x` `courbe_C1` `courbe_C2` `palier` `debut` `piege`.
- `?vue=lecture` — comme le national 2025 N : ordonnée x en mol, palier commun ; trois courbes (a), (b), (c) (τ = 2, 5, 10 min) et un petit
  tableau « exp. 1 : θ₁ · exp. 2 : θ₂ > θ₁ · exp. 3 : θ₂ + quelques gouttes d'acide sulfurique (catalyseur) » ; puis le tuteur trace les
  associations (a)↔3 (deux facteurs), (b)↔2, (c)↔1, et écrit « x_f est le même : vrai ».
  Moments : `enonce` `courbes` `debut` `associer` `conclusion` `fin`.
  Repères : `axe_t` `axe_n` `courbe_a` `courbe_b` `courbe_c` `tableau` `palier` `conclusion`.

## 7. bilan.html et carte.html (modèle : physics/circuit-rlc-tableau/bilan.html, carte.html)
- bilan.html — fiche, blocs (moments) : `fiche` `oxydoreduction` `demi_equation` `equation` `rapide_lente` `facteur` `temperature`
  `concentration` `catalyseur` `trempe` `lacunes` `fin` ; repères : un par bloc (mêmes noms sans `lacunes`) + `fiche`. Page 2 de l'élève (lacunes,
  acquis, acquis_ids par `set_parameters`), comme le modèle. Compétences C1…C7 → blocs : C1 oxydoreduction, C2 demi_equation, C3 equation,
  C4 rapide_lente, C5 facteur + temperature, C6 concentration, C7 catalyseur + trempe.
- carte.html — moments : `centre` `couple` `demi_equation` `equation` `rapide` `lente` `temperature` `concentration` `catalyseur` `trempe` `national`
  `suite` `complete` `fin` ; repères : `centre` + un par branche (sans `complete`). `suite` = « chapitre suivant : suivre l'avancement x(t) ».

## Diapositives servies (cours)
o1 carte · o2 transfert?vue=couple · x1 x2 transfert?vue=zinc · x3 transfert?vue=couple · x4 x5 demi-equation?vue=permanganate ·
x6 demi-equation?vue=eau_oxygenee · x7 equation?vue=zinc_cuivre · x8 equation?vue=fer · x9 equation?vue=permanganate · x10 equation?vue=eau_oxygenee ·
r1 r2 bechers?vue=comparer · r3 bechers?vue=lente · r4 bechers?vue=soufre · r5 r6 bechers?vue=echelle · r7 equation?vue=eau_oxygenee (ou bechers?vue=lente) ·
r8 f1 facteurs?vue=une_variable · f2 f3 facteurs?vue=temperature · f4 courbes?vue=temperature · f5 f6 facteurs?vue=concentration ·
f7 courbes?vue=concentration · f8 facteurs?vue=une_variable · t1 facteurs?vue=trempe · t2 facteurs?vue=vie · t3 facteurs?vue=catalyseur ·
t4 courbes?vue=catalyseur · n1 courbes?vue=lecture (2025 N) · n2 facteurs?vue=trempe (2017 R) · bl bilan · cr carte.
