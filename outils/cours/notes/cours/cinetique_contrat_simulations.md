# Contrat des simulations — cinetique (cours phys_ch10_cinetique, « Suivi temporel d'une transformation, vitesse de réaction »)

Dossier : `frontend/public/media/simulations/chimie/cinetique-tableau/`
Kit (déjà copié) : `commun.js`, `exposants.js` (de `chimie/transformations-lentes-rapides-tableau/`, même API : `Tableau`, `Craie`, scène 760 × 420,
`Tableau.protocole`, `craie.repere`, `play_until`, `__horsCadre`) ; feuille `cin.css` (copie de `tlr.css`). Skill : `.agents/skills/simulations-au-tableau/SKILL.md`.
Modèles de pages : `chimie/transformations-lentes-rapides-tableau/courbes.html` (axes, courbes, vues par `?vue=`) et `facteurs.html` (béchers peints,
chrono, bains), `physics/circuit-rlc-tableau/circuit-lc.html` (moments, repères, ce_qui_se_voit, bulle « Arrêt sur image »).

## Règles communes
- Fond transparent, un seul bouton en haut (Lancer → Pause → Reprendre → Rejouer), bande du bas libre (4,5 em), rien hors du cadre 760 × 420
  (aucune étiquette coupée ni superposée, même aux positions extrêmes des poignées).
- Solutions PEINTES (vraies couleurs, dégradé, ménisque, reflet léger) ; la craie écrit les textes. Couleurs : diiode jaune → brun (#8a4b12 au
  maximum), thiosulfate incolore, empois d'amidon bleu-noir à l'équivalence (seulement si on le montre), magnésium gris métal, bulles de H₂.
  Craie : blanc = texte, jaune = surlignage, orange = piège « ⚠ », vert = tangente / pente, bleu clair = courbe principale.
- Formules avec indices et charges rendus (exposants.js) : H₂O₂, I⁻, I₂, H⁺, H₂O, S₂O₃²⁻, S₄O₆²⁻, CH₃COOC₂H₅, HO⁻, CH₃COO⁻, C₂H₅OH, Na⁺,
  Mg, Mg²⁺, H₂, x_max, x_f, t₁/₂, n₀, σ₀, σ_f, λ. Flèche de réaction DESSINÉE (→). Virgule décimale. Unités : mmol, mol, mol/L, min, mL, L,
  S/m (ou S·m⁻¹), mS·m²·mol⁻¹, Pa, kPa, K ; vitesse en mmol·L⁻¹·min⁻¹.
- Jamais : chocs efficaces, énergie d'activation, ordre de réaction, loi de vitesse, constante de vitesse, mécanisme, Arrhenius,
  Beer-Lambert, « exponentielle » ou τ écrits à l'écran (les modèles ci-dessous servent seulement au calcul des courbes).
- Chaque vue émet `moments` (noms ci-dessous, EXACTS), accepte `play_until {moment}`, `set_time`, `set_parameters` (si poignée), `highlight {target}` ;
  `ce_qui_se_voit` dit l'étape, le temps simulé (min) et les valeurs lues ; tous les repères ci-dessous sont déclarés (`craie.repere`) au plus tard
  au moment indiqué (sinon dès le début). Chaque vue a aussi le moment `fin`.

## Données communes (à reprendre telles quelles)
- **Exemple A (titrage)** : H₂O₂ + 2I⁻ + 2H⁺ → I₂ + 2H₂O ; V = 100 mL de mélange ; n₀(H₂O₂) = 2,0 mmol (limitant) ; n₀(I⁻) = 10,0 mmol ; H⁺ en excès.
  x_max = 2,0 mmol. Modèle : x(t) = 2,0·(1 − e^(−t/8)) mmol, t en min (20 °C). Tableau des mesures (à afficher arrondi à 0,01) :
  t (min) 0 · 2 · 4 · 6 · 8 · 10 · 15 · 20 · 30 · 40 ↔ x (mmol) 0 · 0,44 · 0,79 · 1,06 · 1,26 · 1,43 · 1,69 · 1,84 · 1,95 · 1,99.
  t₁/₂ ≈ 5,5 min. Pente à t = 0 : 0,25 mmol/min → v(0) = 2,5 mmol·L⁻¹·min⁻¹ ; la tangente à l'origine passe par (8 min ; 2,0 mmol).
  v(8 min) ≈ 0,92 mmol·L⁻¹·min⁻¹ ; v(20 min) ≈ 0,21 mmol·L⁻¹·min⁻¹. À 40 °C : x(t) = 2,0·(1 − e^(−3t/8)), t₁/₂ ≈ 1,8 min, v(0) = 7,5 mmol·L⁻¹·min⁻¹.
  Titrage : prélèvement V_p = 10,0 mL versé dans l'eau glacée, diiode titré par le thiosulfate C = 0,020 mol/L : I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻.
  n(I₂) dans le prélèvement = C·V_E/2 ; dans le mélange : n(I₂) = 10 × C·V_E/2 ; x = n(I₂). Exemple : à t = 8 min, V_E = 12,6 mL → n(I₂) = 1,26 mmol.
- **Exemple B (conductimétrie)** : CH₃COOC₂H₅ + HO⁻ → CH₃COO⁻ + C₂H₅OH (« réaction d'un ester avec les ions hydroxyde, étudiée plus tard ») ;
  V = 100 mL = 1,00·10⁻⁴ m³ ; n₀(ester) = n₀(HO⁻) = 1,0 mmol (soude Na⁺ + HO⁻, C₀ = 1,0·10⁻² mol/L) ; x_max = 1,0 mmol.
  λ(Na⁺) = 5,01 mS·m²·mol⁻¹, λ(HO⁻) = 19,9 mS·m²·mol⁻¹, λ(CH₃COO⁻) = 4,09 mS·m²·mol⁻¹.
  σ₀ = 0,249 S/m (≈ 0,25), σ_f = 0,091 S/m ; σ = σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V ; x = x_max·(σ₀ − σ)/(σ₀ − σ_f).
  Modèle : x(t) = 1,0·t/(t + 10) mmol (t en min) ; t₁/₂ = 10 min ; σ(t) = σ₀ − (σ₀ − σ_f)·x/x_max (σ à 10 min = 0,170 S/m).
- **Exemple C (gaz)** : Mg + 2H⁺ → Mg²⁺ + H₂ ; n₀(Mg) = 1,0 mmol (limitant), acide en excès ; ballon fermé, volume de gaz V = 1,0 L, T = 300 K,
  P₀ = 1,013·10⁵ Pa ; R = 8,31 Pa·m³·mol⁻¹·K⁻¹ ; (P − P₀)·V = x·R·T ; x = (P − P₀)·V/(R·T) ; P_max − P₀ ≈ 2,49·10³ Pa ;
  modèle x(t) = 1,0·(1 − e^(−t/4)) mmol. Volume recueilli (éprouvette retournée) : V(H₂) = x·V_m, V_m = 24 L/mol → 24 mL à la fin.

## 1. suivi.html (vues methodes | mesures | prelevement | titrage)
- `?vue=methodes` — trois vignettes côte à côte : (1) bécher + pipette + burette « titrage d'un prélèvement » ; (2) bécher + cellule + conductimètre
  (afficheur) « conductimétrie » ; (3) ballon fermé + manomètre « pression d'un gaz » ; sous chacune : « mesure → avancement x ».
  Moments : `titre` `titrage` `conductimetrie` `pression` `point_commun` `fin` (`point_commun` : « on mesure une grandeur à des dates, on en déduit x(t) »).
  Repères : `vignette_titrage` `vignette_conductimetrie` `vignette_pression` `phrase` `afficheur` `manometre`.
- `?vue=mesures` — un bécher de l'exemple A qui brunit (temps accéléré, chrono) ; à chaque date du tableau, une ligne s'écrit « t = … min : x = … mmol ».
  Moments : `melange` `premiere_mesure` `mesures` `tableau_fini` `fin`. Repères : `becher` `chrono` `tableau` `ligne_premiere` `ligne_derniere`.
- `?vue=prelevement` — le grand bécher brunit ; une pipette prélève 10 mL ; le prélèvement est versé dans un bécher d'eau glacée (glaçons) :
  sa teinte ne bouge plus, le grand bécher continue de foncer ; à la craie : « trempe : on bloque la réaction pour mesurer x à cette date ».
  Moments : `reaction` `prelevement` `eau_glacee` `fige` `continue` `phrase` `fin`.
  Repères : `grand_becher` `pipette` `becher_glace` `glacons` `teinte_figee` `teinte_continue` `phrase`.
- `?vue=titrage` — burette de thiosulfate (C = 0,020 mol/L) au-dessus du prélèvement brun ; on verse : brun → jaune pâle → incolore (équivalence),
  lecture V_E = 12,6 mL ; à la craie : I₂ + 2S₂O₃²⁻ → 2I⁻ + S₄O₆²⁻ ; « à l'équivalence : n(I₂) = C·V_E/2 » ; « dans le mélange : × 10 » ;
  « x = n(I₂) = 1,26 mmol ».
  Moments : `burette` `verser` `equivalence` `equation` `relation` `resultat` `fin`.
  Repères : `burette` `becher` `lecture_VE` `equation` `relation` `resultat`.

## 2. avancement.html (vues tableau | limitant | lien | composition)
Tableau d'avancement à la craie de l'exemple A (colonnes H₂O₂ · I⁻ · H⁺ · I₂ · H₂O ; H⁺ « excès », H₂O « solvant » ; lignes « état initial (x = 0) »,
« en cours (x) », « état final (x_max) » ; quantités en mmol).
- `?vue=tableau` — Moments : `equation` `etat_initial` `en_cours` `etat_final` `fin`.
  (`en_cours` : 2,0 − x · 10,0 − 2x · excès · x ; `etat_final` : 2,0 − x_max · 10,0 − 2x_max · excès · x_max.)
  Repères : `equation` `ligne_initial` `ligne_en_cours` `ligne_final` `colonne_h2o2` `colonne_iodure` `colonne_i2`.
- `?vue=limitant` — les deux hypothèses écrites : « 2,0 − x_max = 0 → x_max = 2,0 mmol » ; « 10,0 − 2x_max = 0 → x_max = 5,0 mmol » ;
  « on garde la plus petite : x_max = 2,0 mmol ; H₂O₂ limitant ».
  Moments : `tableau` `hypothese_1` `hypothese_2` `plus_petite` `limitant` `fin`.
  Repères : `hypothese_1` `hypothese_2` `x_max` `limitant` `ligne_final`.
- `?vue=lien` — à côté du tableau, la colonne I₂ surlignée : « n(I₂) = x » ; un bécher et une flèche « on mesure n(I₂) → on connaît x ».
  Moments : `tableau` `colonne_i2` `egalite` `mesure` `fin`. Repères : `colonne_i2` `egalite` `becher` `fleche`.
- `?vue=composition` — poignée sur la date t (0 à 40 min, défaut 8) : x(t) lu sur une petite courbe à droite, puis la ligne « en cours » remplie avec
  les nombres (à 8 min : x = 1,26 ; H₂O₂ 0,74 ; I⁻ 7,48 ; I₂ 1,26 mmol).
  Moments : `date` `lecture` `remplir` `verifier` `fin` (`verifier` : « 2,0 − 1,26 = 0,74 mmol »). Poignée `t` (`set_parameters {t}`).
  Repères : `poignee_t` `courbe` `point_lu` `ligne_en_cours` `case_h2o2` `case_iodure` `case_i2`.

## 3. courbe.html (vues points | lecture | palier)
Axes à la craie : x (mmol) en ordonnée (0 à 2,5), t (min) en abscisse (0 à 40) ; quadrillage léger ; exemple A.
- `?vue=points` — les points du tableau se placent un à un, puis la courbe lisse passe par eux.
  Moments : `axes` `premiers_points` `tous_points` `courbe` `allure` `fin` (`allure` : « monte vite au début, puis de moins en moins »).
  Repères : `axe_t` `axe_x` `points` `courbe` `debut` `fin_courbe`.
- `?vue=lecture` — poignée sur la date t (défaut 8) : pointillés t → courbe → axe x, valeur lue (« x(8 min) ≈ 1,26 mmol »).
  Moments : `axes` `courbe` `date` `lecture` `valeur` `fin`. Poignée `t`. Repères : `axe_t` `axe_x` `courbe` `poignee_t` `pointilles` `valeur`.
- `?vue=palier` — la courbe jusqu'à 40 min, palier horizontal x_f = 2,0 mmol, trait pointillé x_max = 2,0 mmol confondus ; « x_f = x_max : transformation
  totale » ; « à partir d'environ 30 min, x ne change plus : état final ».
  Moments : `axes` `courbe` `palier` `x_max` `egalite` `etat_final` `fin`. Repères : `axe_t` `axe_x` `courbe` `palier` `ligne_x_max` `phrase`.

## 4. conductimetrie.html (vues cellule | ions | formule | saponification | droite | calcul)
- `?vue=cellule` — bécher, cellule à deux plaques (surface S, écart L), conductimètre (afficheur de G en mS) ; à la craie : « G = k·σ »,
  « k : constante de cellule », « σ en S/m » ; « σ vient des ions de la solution ».
  Moments : `montage` `plaques` `afficheur` `relation` `ions` `fin`. Repères : `becher` `cellule` `plaques` `afficheur` `relation`.
- `?vue=ions` — deux béchers : eau presque pure (afficheur faible) et solution d'ions (afficheur fort) ; puis on ajoute des ions : l'afficheur monte.
  Moments : `eau` `solution` `ajout` `monte` `conclusion` `fin` (`conclusion` : « plus d'ions → σ plus grande ; des ions qui changent → σ change »).
  Repères : `becher_eau` `becher_ions` `afficheur_1` `afficheur_2` `conclusion`.
- `?vue=formule` — « σ = Σ λᵢ·[Xᵢ] » écrit ; exemple soude : σ₀ = λ(Na⁺)·[Na⁺] + λ(HO⁻)·[HO⁻] ; unités (λ en S·m²·mol⁻¹, [X] en mol/m³ ; 1 mol/L = 10³ mol/m³ ⚠).
  Moments : `formule` `exemple` `unites` `piege` `fin`. Repères : `formule` `exemple` `unites` `piege`.
- `?vue=saponification` — bécher de l'exemple B, afficheur de σ qui DESCEND de 0,249 à 0,091 S/m (temps accéléré, chrono) ; loupe : un HO⁻ (rapide,
  grand λ) remplacé par un CH₃COO⁻ (lent, petit λ) ; Na⁺ ne change pas.
  Moments : `melange` `descend` `loupe` `remplace` `na_spectateur` `final` `fin`.
  Repères : `becher` `afficheur` `chrono` `loupe` `ion_ho` `ion_acetate` `ion_na` `equation`.
- `?vue=droite` — graphe σ (S/m) en fonction de x (mmol) : droite de (0 ; σ₀ = 0,249) à (1,0 ; σ_f = 0,091) ; à la craie la relation
  « σ = σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V », puis « x = x_max·(σ₀ − σ)/(σ₀ − σ_f) ».
  Moments : `axes` `point_initial` `point_final` `droite` `relation` `inverse` `fin`.
  Repères : `axe_x` `axe_sigma` `point_initial` `point_final` `droite` `relation` `inverse`.
- `?vue=calcul` — à gauche la courbe σ(t) (décroissante, 0 à 40 min) ; poignée t (défaut 10) : σ lue (0,170 S/m), puis le calcul écrit
  « x = 1,0 × (0,249 − 0,170)/(0,249 − 0,091) = 0,50 mmol » et le point reporté sur une petite courbe x(t) à droite.
  Moments : `courbe_sigma` `date` `lecture` `calcul` `report` `fin`. Poignée `t`.
  Repères : `courbe_sigma` `poignee_t` `valeur_sigma` `calcul` `courbe_x` `point_x`.

## 5. pression.html (vues ballon | relation | volume)
- `?vue=ballon` — ballon fermé (bouchon) relié à un manomètre (afficheur en kPa), acide chlorhydrique + ruban de magnésium ; bulles ; P monte de
  101,3 à environ 103,8 kPa puis palier (exemple C, temps accéléré).
  Moments : `montage` `ruban` `bulles` `monte` `palier` `equation` `fin`.
  Repères : `ballon` `bouchon` `manometre` `afficheur` `ruban` `bulles` `equation`.
- `?vue=relation` — à la craie : « (P − P₀)·V = n(H₂)·R·T », tableau d'avancement réduit « n(H₂) = x », puis « x = (P − P₀)·V/(R·T) » ;
  ⚠ « V en m³, P en Pa, T en K » ; application : à la fin P − P₀ = 2,49·10³ Pa → x = 1,0·10⁻³ mol.
  Moments : `gaz_parfait` `hydrogene` `relation` `unites` `application` `fin`.
  Repères : `gaz_parfait` `ligne_h2` `relation` `unites` `application`.
- `?vue=volume` — éprouvette graduée retournée sur une cuve à eau, le gaz chasse l'eau (0 → 24 mL) ; « x = V(H₂)/V_m », V_m = 24 L/mol.
  Moments : `montage` `gaz` `lecture` `relation` `fin`. Repères : `eprouvette` `cuve` `graduation` `relation`.

## 6. vitesse.html (vues pente | definition | tangente | calcul | diminue | concentration | fin | temperature)
Courbe x(t) de l'exemple A (axes comme courbe.html).
- `?vue=pente` — poignée t (0 à 40 min, défaut 2) : un petit triangle « Δx en Δt » sur la courbe ; « au début : x monte vite ; à la fin : presque plus ».
  Moments : `courbe` `debut_raide` `milieu` `fin_plate` `phrase` `fin`. Poignée `t`.
  Repères : `courbe` `triangle` `poignee_t` `phrase`.
- `?vue=definition` — « v(t) = (1/V)·dx/dt » écrit en grand ; sous chaque morceau : « 1/V : par litre de mélange », « dx/dt : la pente de la tangente
  à la courbe x(t) à la date t » ; « unité : mol·L⁻¹·min⁻¹ (ou mmol·L⁻¹·min⁻¹) ».
  Moments : `formule` `volume` `derivee` `unite` `fin`. Repères : `formule` `morceau_V` `morceau_dx` `unite`.
- `?vue=tangente` — poignée t (défaut 0) : tangente verte à la courbe ; deux points de la tangente marqués (à t = 0 : (0 ; 0) et (8 ; 2,0)) ;
  « pente = Δx/Δt = (2,0 − 0)/(8 − 0) = 0,25 mmol/min ».
  Moments : `courbe` `point` `tangente` `deux_points` `pente` `fin`. Poignée `t`.
  Repères : `courbe` `point_contact` `tangente` `point_A` `point_B` `pente`.
- `?vue=calcul` — le calcul au barème : « v(0) = (1/V)·(dx/dt)₀ = (1/0,100) × 0,25 = 2,5 mmol·L⁻¹·min⁻¹ » ; ⚠ « V en litres ».
  Moments : `relation` `pente` `application` `resultat` `piege` `fin`. Repères : `relation` `pente` `application` `resultat` `piege`.
- `?vue=diminue` — trois tangentes successives (t = 0, 8, 20 min) de plus en plus plates ; une petite colonne « v(0) = 2,5 · v(8) ≈ 0,92 · v(20) ≈ 0,21 ».
  Moments : `courbe` `tangente_0` `tangente_8` `tangente_20` `conclusion` `fin` (`conclusion` : « la vitesse diminue au cours du temps »).
  Repères : `courbe` `tangente_0` `tangente_8` `tangente_20` `colonne` `conclusion`.
- `?vue=concentration` — à gauche la courbe [H₂O₂] (mmol/L) qui baisse de 20 à 0 ; à droite une loupe : de moins en moins d'entités de réactif,
  elles se rencontrent moins souvent ; « les réactifs s'épuisent → v diminue ».
  Moments : `courbe_reactif` `debut` `plus_tard` `loupe` `conclusion` `fin`.
  Repères : `courbe_reactif` `loupe` `entites` `conclusion`.
- `?vue=fin` — la courbe au palier ; tangente horizontale à t = 40 min ; « pente nulle → v = 0 : la transformation est finie » ; « v est maximale à t = 0 ».
  Moments : `courbe` `palier` `tangente_horizontale` `vitesse_nulle` `maximale_debut` `fin`.
  Repères : `courbe` `palier` `tangente_horizontale` `phrase_nulle` `phrase_max`.
- `?vue=temperature` — deux courbes 20 °C et 40 °C (même palier 2,0 mmol), tangentes à l'origine (pentes 0,25 et 0,75 mmol/min) ;
  « à 40 °C, v(0) = 7,5 mmol·L⁻¹·min⁻¹, trois fois plus » ; « même état final ».
  Moments : `axes` `courbe_20` `courbe_40` `tangentes` `comparer` `meme_final` `fin`.
  Repères : `courbe_20` `courbe_40` `tangente_20` `tangente_40` `palier` `phrase`.

## 7. demi-reaction.html (vues definition | lecture | piege | comparer)
Courbe x(t) de l'exemple A.
- `?vue=definition` — « t₁/₂ : durée au bout de laquelle l'avancement atteint la moitié de sa valeur finale » ; « x(t₁/₂) = x_f/2 ».
  Moments : `courbe` `palier` `moitie` `definition` `relation` `fin`. Repères : `courbe` `palier` `moitie` `definition` `relation`.
- `?vue=lecture` — les gestes : 1) x_f = 2,0 mmol sur le palier ; 2) x_f/2 = 1,0 mmol marqué sur l'axe x ; 3) horizontale jusqu'à la courbe ;
  4) verticale jusqu'à l'axe t : t₁/₂ ≈ 5,5 min.
  Moments : `x_f` `moitie` `horizontale` `verticale` `valeur` `fin`. Repères : `x_f` `moitie` `horizontale` `point` `verticale` `valeur`.
- `?vue=piege` — à t = 2·t₁/₂ = 11 min : x ≈ 1,5 mmol, PAS 2,0 : « à 2·t₁/₂ la transformation n'est pas finie » ⚠ ; « ⚠ x_f/2, jamais t_final/2 ».
  Moments : `courbe` `t_demi` `double` `pas_fini` `piege_axe` `fin`. Repères : `courbe` `t_demi` `double` `valeur_double` `piege`.
- `?vue=comparer` — deux courbes (20 °C : t₁/₂ ≈ 5,5 min ; 40 °C : t₁/₂ ≈ 1,8 min), même palier ; « plus t₁/₂ est petit, plus la transformation est rapide ».
  Moments : `axes` `courbe_lente` `courbe_rapide` `deux_t_demi` `conclusion` `fin`.
  Repères : `courbe_lente` `courbe_rapide` `t_demi_lente` `t_demi_rapide` `conclusion`.

## 8. figures.html (?fig=…) — figures des nationaux
Écrites d'après `outils/cours/notes/cours/cinetique_build/nationaux.md` (section « Figures pour figures.html ») : une figure par clé `fig_<session>`,
dessinée comme le sujet (axes, graduations, unités, courbe, tangente donnée, points marqués). Pour chaque figure, moments :
`axes` `courbe` `tangente` (si le sujet en donne une) `lecture` `fin` ; repères : `axe_t` `axe_y` `courbe` `tangente` `point` `valeur`.

## 9. bilan.html et carte.html (modèle : chimie/transformations-lentes-rapides-tableau/bilan.html, carte.html)
- bilan.html — fiche, blocs (moments) : `fiche` `suivi` `avancement` `mesure_x` `courbe` `vitesse` `evolution` `demi_reaction` `redaction` `lacunes` `fin` ;
  repères : un par bloc (mêmes noms sans `lacunes`) + `fiche`. Page 2 de l'élève (lacunes, acquis, acquis_ids par `set_parameters`), comme le modèle.
  Compétences → blocs : C1 suivi, C2 avancement, C3 mesure_x, C4 courbe, C5 vitesse, C6 evolution, C7 demi_reaction, C8 redaction.
  Contenu : suivi (trempe ; titrage, conductimétrie, pression) ; avancement (tableau, x_max, limitant) ; mesure_x (n(I₂) = x ; x = x_max·(σ₀ − σ)/(σ₀ − σ_f) ;
  x = (P − P₀)·V/(R·T)) ; courbe (lire x, composition, x_f) ; vitesse (v(t) = (1/V)·dx/dt, tangente, ⚠ V en L) ; evolution (v diminue : réactifs
  consommés ; plus chaud → plus vite ; v = 0 à la fin) ; demi_reaction (x(t₁/₂) = x_f/2 ; ⚠ x_f/2, pas t/2 ; à 2·t₁/₂ pas fini) ; redaction (relation,
  application numérique, résultat avec unité).
- carte.html — moments : `centre` `methodes` `trempe` `tableau` `mesure` `courbe` `vitesse` `diminue` `demi_reaction` `national` `suite` `complete` `fin` ;
  repères : `centre` + un par branche (sans `complete`). Centre : « suivre x(t) ». `suite` = « chapitre suivant : transformations dans les deux sens ».

## Diapositives servies (cours)
o1 carte · o2 suivi?vue=methodes · m1 suivi?vue=mesures · m2 suivi?vue=prelevement · m3 suivi?vue=titrage · a1 avancement?vue=tableau ·
a2 avancement?vue=limitant · a3 avancement?vue=lien · a4 courbe?vue=points · a5 courbe?vue=lecture · a6 avancement?vue=composition · a7 courbe?vue=palier ·
g1 conductimetrie?vue=cellule · g2 conductimetrie?vue=ions · g3 conductimetrie?vue=formule · g4 conductimetrie?vue=saponification ·
g5 conductimetrie?vue=droite · g6 conductimetrie?vue=calcul · p1 pression?vue=ballon · p2 pression?vue=relation · p3 pression?vue=volume ·
p4 figures (national, conductimétrie) · p5 suivi?vue=methodes · p6 figures (national) ·
v1 vitesse?vue=pente · v2 vitesse?vue=definition · v3 vitesse?vue=tangente · v4 vitesse?vue=calcul · v5 vitesse?vue=diminue · v6 vitesse?vue=concentration ·
v7 vitesse?vue=fin · v8 vitesse?vue=temperature · h1 demi-reaction?vue=definition · h2 demi-reaction?vue=lecture · h3 demi-reaction?vue=piege ·
h4 demi-reaction?vue=comparer · n1…n8 figures?fig=… (nationaux) · r1 vitesse?vue=calcul · r2 conductimetrie?vue=formule (pièges d'unités) · bl bilan · cr carte.
