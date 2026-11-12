# Contrat des simulations — transformations_deux_sens (cours phys_ch11_transformations_deux_sens, « Transformations chimiques s'effectuant dans les deux sens »)

Dossier : `frontend/public/media/simulations/chimie/transformations-deux-sens-tableau/`
Kit (déjà copié) : `commun.js`, `exposants.js` (de `chimie/cinetique-tableau/`, même API : `Tableau`, `Craie`, scène 760 × 420,
`Tableau.protocole`, `craie.repere`, `play_until`, `__horsCadre`) ; feuille `tds.css` (copie de `cin.css`). Skill : `.agents/skills/simulations-au-tableau/SKILL.md`.
Modèles de pages : `chimie/cinetique-tableau/avancement.html` (tableau d'avancement à la craie, poignée), `conductimetrie.html` (cellule,
afficheur, λ), `suivi.html` (béchers peints, afficheurs), `courbe.html` (axes, courbes, vues par `?vue=`), `figures.html` (figures des nationaux),
`bilan.html`, `carte.html` ; `physics/circuit-rlc-tableau/circuit-lc.html` (moments, repères, ce_qui_se_voit, bulle « Arrêt sur image »).

## Règles communes
- Fond transparent, un seul bouton en haut (Lancer → Pause → Reprendre → Rejouer), bande du bas libre (4,5 em), rien hors du cadre 760 × 420
  (aucune étiquette coupée ni superposée, même aux positions extrêmes des poignées).
- Solutions PEINTES (vraies couleurs, dégradé, ménisque, reflet léger) ; la craie écrit les textes. Solutions acides et basiques incolores
  (comme en vrai) ; flacon d'éthanoate de sodium incolore ; pH-mètre gris à afficheur vert (pH à 0,1 près), sonde de verre ; conductimètre
  à afficheur (mS/m) ; protons H⁺ dessinés comme petites boules jaunes qui sautent d'une espèce à l'autre (loupe ronde).
  Craie : blanc = texte, jaune = surlignage, orange = piège « ⚠ », vert = sens 1 (→), rose = sens 2 (←), bleu clair = courbe principale.
- Formules avec indices et charges rendus (exposants.js) : H⁺, H₂O, H₃O⁺, HO⁻, CH₃COOH, CH₃COO⁻, HCOOH, Cl⁻, Na⁺, NH₃, NH₄⁺,
  C₆H₅COOH, C₆H₅COO⁻, R–NH₂, R–NH₃⁺, x_max, x_f, [H₃O⁺], 10^(−pH), λ, σ, τ. Flèches DESSINÉES : → (sens 1), ← (sens 2), ⇌ (deux sens).
  Virgule décimale. Unités : mol, mmol, mol/L, mol/m³, mL, L, S/m, mS/m, mS·m²·mol⁻¹ ; τ sans unité (ou en %).
- Jamais : Qr, quotient de réaction, constante d'équilibre, constante d'acidité, Ka, pKa, Ke, pKe, produit ionique, autoprotolyse, activité, Lewis, Arrhenius, degré d'ionisation, coefficient de dissociation, Ostwald, loi de dilution, diagramme de prédominance, diagramme de distribution, espèce prédominante, Henderson, Hasselbalch, indicateur coloré, zone de virage, pouvoir tampon écrits à l'écran (les valeurs ci-dessous sont des mesures ; aucun modèle de calcul n'est écrit).
- Chaque vue émet `moments` (noms ci-dessous, EXACTS), accepte `play_until {moment}`, `set_time`, `set_parameters` (si poignée), `highlight {target}` ;
  `ce_qui_se_voit` dit l'étape, les valeurs affichées (pH, σ, concentrations) et ce qui vient d'être écrit ; tous les repères ci-dessous sont
  déclarés (`craie.repere`) au plus tard au moment indiqué (sinon dès le début). Chaque vue a aussi le moment `fin`.

## Données communes (à reprendre telles quelles)
- **Exemple A (acide éthanoïque)** : CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺ ; C = 1,0·10⁻² mol/L ; V = 100 mL = 0,100 L ; pH mesuré = 3,4.
  [H₃O⁺] = 10^(−3,4) = 4,0·10⁻⁴ mol/L. Si la réaction était totale : [H₃O⁺] = C = 1,0·10⁻² mol/L → pH = 2,0 (attendu), mesuré 3,4.
  Tableau (mol) : état initial C·V = 1,0·10⁻³ · excès · 0 · 0 ; en cours C·V − x · excès · x · x ; état final C·V − x_f · excès · x_f · x_f.
  x_max = C·V = 1,0·10⁻³ mol ; x_f = [H₃O⁺]·V = 4,0·10⁻⁴ × 0,100 = 4,0·10⁻⁵ mol ; τ = x_f/x_max = 0,040 = 4,0 %.
  À l'équilibre : n(CH₃COOH) = 9,6·10⁻⁴ mol, n(CH₃COO⁻) = n(H₃O⁺) = 4,0·10⁻⁵ mol. Relation : τ = 10^(−pH)/C = 10^(−3,4)/1,0·10⁻² = 0,040.
- **Exemple B (acide chlorhydrique)** : HCl + H₂O → Cl⁻ + H₃O⁺ ; même C = 1,0·10⁻² mol/L, V = 100 mL ; pH mesuré = 2,0 ;
  [H₃O⁺] = 1,0·10⁻² mol/L ; x_f = 1,0·10⁻³ mol = x_max ; τ = 1 : réaction totale (flèche simple →).
- **Exemple C (conductimétrie)** : σ = Σ λᵢ·[Xᵢ] ; λ(H₃O⁺) = 35,0 mS·m²·mol⁻¹, λ(CH₃COO⁻) = 4,09 mS·m²·mol⁻¹, λ(Cl⁻) = 7,63 mS·m²·mol⁻¹ ;
  ions HO⁻ négligés. Acide éthanoïque (exemple A) : σ = 1,56·10⁻² S/m (afficheur 15,6 mS/m) ; acide chlorhydrique (exemple B) : σ = 0,426 S/m
  (afficheur 426 mS/m). [CH₃COO⁻] = [H₃O⁺] (tableau) → σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] ; [H₃O⁺] = σ/(λ(H₃O⁺) + λ(A⁻)) =
  1,56·10⁻²/(39,09·10⁻³) = 0,399 mol/m³ = 3,99·10⁻⁴ mol/L ⚠ (1 mol/L = 10³ mol/m³) → τ = 3,99·10⁻⁴/1,0·10⁻² = 0,040.
- **Exemple D (dilution et nature de l'acide)** : acide éthanoïque dilué 10 fois puis encore 10 fois :
  C (mol/L) 1,0·10⁻² · 1,0·10⁻³ · 1,0·10⁻⁴ ↔ pH mesuré 3,4 · 3,9 · 4,5 ↔ τ = 10^(−pH)/C = 0,040 · 0,13 · 0,32.
  Même C = 1,0·10⁻² mol/L, trois acides : acide chlorhydrique pH 2,0, τ = 1 ; acide méthanoïque HCOOH pH 2,9, τ = 0,13 ; acide éthanoïque
  pH 3,4, τ = 0,040.
- **Exemple E (le sens 2 existe)** : 50 mL d'acide chlorhydrique (1,0·10⁻² mol/L) + 50 mL d'eau → pH 2,3 ; 50 mL du même acide + 50 mL
  d'éthanoate de sodium Na⁺ + CH₃COO⁻ (1,0·10⁻² mol/L) → pH 3,6 : les ions H₃O⁺ ont été consommés : CH₃COO⁻ + H₃O⁺ → CH₃COOH + H₂O.
- **Exemple F (estérification, 2016 N)** : acide propanoïque + éthanol ⇌ propanoate d'éthyle + eau ; n₀ = 0,5 mol de chaque ; à la fin
  n(ester) = 0,33 mol ; x_max = 0,5 mol ; x_f = 0,33 mol ; τ = 0,66 : lente et limitée (« étudiée plus tard »). Courbe x(t) d'allure : montée
  lente (heures), palier 0,33 mol, pointillé x_max = 0,5 mol.

## 1. acides.html (vues ouverture | acide | base | couple | reaction)
- `?vue=ouverture` — deux flacons de même étiquette « C = 1,0·10⁻² mol/L » : acide éthanoïque et acide chlorhydrique ; la sonde du pH-mètre
  plonge dans l'un (3,4) puis dans l'autre (2,0) ; à la craie : « même concentration… pas le même pH : pourquoi ? ».
  Moments : `deux_flacons` `meme_concentration` `mesure_1` `mesure_2` `question` `fin`.
  Repères : `flacon_ethanoique` `flacon_chlorhydrique` `etiquette_1` `etiquette_2` `afficheur_1` `afficheur_2` `question`.
- `?vue=acide` — loupe : une molécule CH₃COOH ; un proton H⁺ (boule jaune) s'en détache → CH₃COO⁻ ; à la craie « acide : espèce chimique capable
  de céder un proton H⁺ » ; « CH₃COOH → CH₃COO⁻ + H⁺ ».
  Moments : `molecule` `proton` `cede` `definition` `fin`. Repères : `molecule` `proton` `base_conjuguee` `definition`.
- `?vue=base` — loupe : une molécule NH₃ capte un proton H⁺ → NH₄⁺ ; « base : espèce chimique capable de capter un proton H⁺ » ;
  « NH₃ + H⁺ → NH₄⁺ ».
  Moments : `molecule` `proton` `capte` `definition` `fin`. Repères : `molecule` `proton` `acide_conjugue` `definition`.
- `?vue=couple` — « couple acide/base : AH/A⁻ » ; demi-équation « AH ⇌ A⁻ + H⁺ » ; exemples écrits un à un : CH₃COOH/CH₃COO⁻, NH₄⁺/NH₃,
  H₃O⁺/H₂O, H₂O/HO⁻ ; « l'eau appartient à deux couples : acide dans H₂O/HO⁻, base dans H₃O⁺/H₂O ».
  Moments : `notation` `demi_equation` `exemples` `eau` `fin`. Repères : `notation` `demi_equation` `exemple_1` `exemple_2` `eau`.
- `?vue=reaction` — deux couples CH₃COOH/CH₃COO⁻ et NH₄⁺/NH₃ ; le proton passe de CH₃COOH à NH₃ (flèche jaune) ;
  « CH₃COOH + NH₃ → CH₃COO⁻ + NH₄⁺ » ; « réaction acido-basique : un proton passe de l'acide d'un couple à la base de l'autre couple ».
  Moments : `couple_1` `couple_2` `transfert` `equation` `phrase` `fin`. Repères : `couple_1` `couple_2` `proton` `equation` `phrase`.

## 2. ph.html (vues definition | calcul | phmetre)
- `?vue=definition` — bécher de l'exemple A, loupe sur quelques ions H₃O⁺ ; « pH = −log[H₃O⁺] » ([H₃O⁺] en mol/L, solution aqueuse diluée) ;
  puis la relation inverse « [H₃O⁺] = 10^(−pH) » ; « plus [H₃O⁺] est grande, plus le pH est petit ».
  Moments : `ions` `concentration` `formule` `inverse` `sens` `fin`. Repères : `becher` `ions_h3o` `formule` `inverse` `sens`.
- `?vue=calcul` — poignée pH (1,0 à 13,0, défaut 3,4) : la ligne « [H₃O⁺] = 10^(−pH) = … mol/L » se recalcule (2 chiffres significatifs) ;
  à 3,4 : 4,0·10⁻⁴ mol/L ; à 2,0 : 1,0·10⁻² mol/L ; ⚠ « le signe moins ».
  Moments : `donnee` `relation` `calcul` `resultat` `piege` `fin`. Poignée `pH` (`set_parameters {pH}`).
  Repères : `poignee_pH` `relation` `calcul` `resultat` `piege`.
- `?vue=phmetre` — pH-mètre et sonde ; étalonnage avec deux solutions étalons (pH 4,0 puis 7,0), rinçage à l'eau distillée, mesure dans
  l'exemple A : l'afficheur se stabilise à 3,4 ; « la sonde mesure le pH à 0,1 près ».
  Moments : `appareil` `etalonnage` `rincage` `mesure` `lecture` `fin`.
  Repères : `phmetre` `sonde` `etalon_4` `etalon_7` `becher` `afficheur`.

## 3. avancement.html (vues acide_eau | base_eau | attendu | tableau | x_max | x_f | taux | totale | relation | proportion | dosage)
Tableau d'avancement à la craie de l'exemple A (colonnes CH₃COOH · H₂O · CH₃COO⁻ · H₃O⁺ ; H₂O « excès » ; lignes « état initial (x = 0) »,
« en cours (x) », « état final (x_f) » ; quantités en mol).
- `?vue=acide_eau` — bécher de l'exemple A, loupe : CH₃COOH cède un proton à H₂O qui devient H₃O⁺ ; « CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺ » ;
  couples CH₃COOH/CH₃COO⁻ et H₃O⁺/H₂O soulignés ; « l'eau joue le rôle de base » ; forme générale « AH + H₂O ⇌ A⁻ + H₃O⁺ ».
  Moments : `becher` `loupe` `transfert` `equation` `couples` `fin`.
  Repères : `becher` `loupe` `molecule_acide` `molecule_eau` `equation` `couples`.
- `?vue=base_eau` — loupe : NH₃ capte un proton cédé par H₂O qui devient HO⁻ ; « NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ » ; « l'eau joue le rôle d'acide » ; forme générale « B + H₂O ⇌ BH⁺ + HO⁻ » ;
  `renvoi` : « τ d'une base : au chapitre des réactions acide-base ».
  Moments : `becher` `loupe` `transfert` `equation` `renvoi` `fin`. Repères : `becher` `loupe` `equation` `couples` `renvoi`.
- `?vue=attendu` — « si la réaction était totale : [H₃O⁺] = C = 1,0·10⁻² mol/L → pH = 2,0 » ; le pH-mètre affiche 3,4 ;
  « pH mesuré > pH attendu : il y a moins de H₃O⁺ que prévu : la réaction n'est pas totale ».
  Moments : `hypothese` `calcul_attendu` `mesure` `comparer` `conclusion` `fin`.
  Repères : `hypothese` `ph_attendu` `afficheur` `ph_mesure` `conclusion`.
- `?vue=tableau` — Moments : `equation` `etat_initial` `en_cours` `etat_final` `fin`.
  (`etat_initial` : C·V · excès · 0 · 0 ; `en_cours` : C·V − x · excès · x · x ; `etat_final` : C·V − x_f · excès · x_f · x_f.)
  Repères : `equation` `ligne_initial` `ligne_en_cours` `ligne_final` `colonne_h3o`.
- `?vue=x_max` — « si la réaction était totale : C·V − x_max = 0 » → « x_max = C·V = 1,0·10⁻² × 0,100 = 1,0·10⁻³ mol ».
  Moments : `hypothese` `relation` `application` `resultat` `fin`. Repères : `hypothese` `relation` `application` `resultat`.
- `?vue=x_f` — colonne H₃O⁺ surlignée : « n(H₃O⁺) = x_f » ; « x_f = [H₃O⁺]_éq·V = 10^(−pH)·V » ; « x_f = 4,0·10⁻⁴ × 0,100 = 4,0·10⁻⁵ mol » ;
  deux barres : x_f (petite) et x_max (25 fois plus haute).
  Moments : `colonne` `relation` `application` `resultat` `comparer` `fin`.
  Repères : `colonne_h3o` `relation` `application` `resultat` `barres`.
- `?vue=taux` — « τ = x_f/x_max » ; « τ = 4,0·10⁻⁵/1,0·10⁻³ = 0,040 = 4,0 % » ; barre x_f posée contre la barre x_max ; « τ < 1 : réaction limitée ».
  Moments : `definition` `application` `resultat` `barres` `limitee` `fin`.
  Repères : `definition` `application` `resultat` `barre_xf` `barre_xmax` `limitee`.
- `?vue=totale` — exemple B : « HCl + H₂O → Cl⁻ + H₃O⁺ » ; pH = 2,0 → [H₃O⁺] = 1,0·10⁻² mol/L → x_f = 1,0·10⁻³ mol = x_max ; « τ = 1 :
  réaction totale » ; flèche simple → (et ⇌ pour l'exemple A, côte à côte).
  Moments : `donnees` `x_f` `taux` `totale` `fleches` `fin`. Repères : `donnees` `calcul_xf` `taux` `totale` `fleche_simple` `double_fleche`.
- `?vue=relation` — démonstration : « τ = x_f/x_max = [H₃O⁺]·V/(C·V) » ; V barré deux fois ; « τ = 10^(−pH)/C » ; vérification
  « 10^(−3,4)/1,0·10⁻² = 0,040 ».
  Moments : `depart` `remplacer` `simplifier` `relation` `verifier` `fin`. Repères : `depart` `remplacer` `simplifier` `relation` `verifier`.
- `?vue=proportion` — national 2023 N (1.2, 0,75 pt) : C_A = 5,0·10⁻² mol/L, pH = 3,05 ; « α(CH₃COOH) = [CH₃COOH]/([CH₃COOH] + [CH₃COO⁻]) » ;
  tableau : [CH₃COOH] = C_A(1 − τ), [CH₃COO⁻] = C_A·τ ; « α = 1 − τ » ; τ = 10^(−3,05)/5,0·10⁻² = 0,0178 → α = 0,982 = 98,2 %.
  Moments : `donnees` `definition_alpha` `tableau` `relation` `application` `fin`.
  Repères : `donnees` `definition_alpha` `tableau` `relation` `application` `resultat`.
- `?vue=dosage` — national 2024 R (2.3-2.4, 1,5 pt) : V_B = 10,0 mL d'amine R–NH₂ (C_B = 9,0·10⁻² mol/L) ; V_A = 16,0 mL d'acide chlorhydrique
  (C_A = 4,5·10⁻² mol/L) ; pH = 10,2 ; « R–NH₂ + H₃O⁺ → R–NH₃⁺ + H₂O » ; « x_f = C_A·V_A − 10^(−pH)·(V_A + V_B) = 7,2·10⁻⁴ mol » ;
  H₃O⁺ limitant : « x_max = C_A·V_A = 7,2·10⁻⁴ mol » ; « τ = 1 : la réaction de dosage est totale ».
  Moments : `donnees` `tableau` `x_f` `x_max` `taux` `fin`. Repères : `donnees` `tableau` `x_f` `x_max` `taux`.

## 4. equilibre.html (vues inverse | double_fleche | etat | dynamique | esterification)
- `?vue=inverse` — exemple E : bécher d'acide chlorhydrique dilué (afficheur 2,3) ; on verse l'éthanoate de sodium : l'afficheur MONTE à 3,6 ;
  « CH₃COO⁻ + H₃O⁺ → CH₃COOH + H₂O » ; « la réaction se fait aussi dans l'autre sens (sens 2) ».
  Moments : `acide_seul` `ajout` `ph_monte` `equation_inverse` `conclusion` `fin`.
  Repères : `becher` `afficheur` `flacon_ethanoate` `equation_inverse` `conclusion`.
- `?vue=double_fleche` — l'équation du sens 1 (vert, →) et celle du sens 2 (rose, ←) se superposent en « CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺ » ;
  « une réaction limitée se fait dans les deux sens : on écrit ⇌ ».
  Moments : `sens_1` `sens_2` `double_fleche` `phrase` `fin`. Repères : `equation_1` `equation_2` `double_fleche` `phrase`.
- `?vue=etat` — exemple A : chrono de 0 à 10 min, l'afficheur reste à 3,4 ; trois barres de quantités constantes (CH₃COOH 9,6·10⁻⁴ mol ;
  CH₃COO⁻ et H₃O⁺ 4,0·10⁻⁵ mol) ; « état d'équilibre : les quantités de matière ne changent plus ; réactifs et produits sont tous présents ».
  Moments : `chrono` `afficheur_stable` `barres` `coexistent` `phrase` `fin`.
  Repères : `becher` `afficheur` `chrono` `barres` `phrase`.
- `?vue=dynamique` — loupe : à chaque instant des CH₃COOH cèdent un proton à H₂O (flèches vertes) et autant de CH₃COO⁻ reprennent un proton
  à H₃O⁺ (flèches roses) ; deux compteurs « sens 1 » et « sens 2 » avancent ensemble (12, 24, 36…) ; « équilibre dynamique : les deux
  réactions continuent, à la même vitesse ; les quantités ne changent pas ».
  Moments : `loupe` `sens_1` `sens_2` `compteurs` `egalite` `phrase` `fin`.
  Repères : `loupe` `compteur_1` `compteur_2` `egalite` `phrase`.
- `?vue=esterification` — exemple F : ballon chauffé à reflux ; « acide + alcool ⇌ ester + eau » ; courbe x(t) qui monte lentement vers un palier
  0,33 mol sous le pointillé x_max = 0,5 mol ; « τ = 0,33/0,5 = 0,66 » ; « lente et limitée (étudiée plus tard) ».
  Moments : `melange` `equation` `courbe` `palier` `taux` `limitee` `fin`.
  Repères : `ballon` `equation` `courbe` `palier` `ligne_x_max` `taux` `phrase`.

## 5. conductimetrie.html (vues ions | relation | calcul | national)
- `?vue=ions` — deux béchers de même C (exemple C) avec la même cellule : acide éthanoïque (afficheur 15,6 mS/m) puis acide chlorhydrique
  (afficheur 426 mS/m) ; loupe : peu d'ions dans le premier, beaucoup dans le second ; « σ vient des ions : moins d'ions → réaction limitée ».
  Moments : `deux_bechers` `afficheur_1` `afficheur_2` `loupe` `conclusion` `fin`.
  Repères : `becher_ethanoique` `becher_chlorhydrique` `afficheur_1` `afficheur_2` `loupe` `conclusion`.
- `?vue=relation` — « σ = Σ λᵢ·[Xᵢ] » ; « σ = λ(H₃O⁺)·[H₃O⁺] + λ(CH₃COO⁻)·[CH₃COO⁻] » (HO⁻ négligés) ; tableau : « [CH₃COO⁻] = [H₃O⁺] » ;
  « σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] ».
  Moments : `formule` `deux_ions` `egalite` `factoriser` `fin`. Repères : `formule` `deux_ions` `egalite` `relation`.
- `?vue=calcul` — « [H₃O⁺] = σ/(λ(H₃O⁺) + λ(A⁻)) » ; « = 1,56·10⁻²/(39,09·10⁻³) = 0,399 mol/m³ » ; ⚠ « ÷ 10³ : 3,99·10⁻⁴ mol/L » ;
  « τ = 3,99·10⁻⁴/1,0·10⁻² = 0,040 » (même τ qu'avec le pH).
  Moments : `donnees` `relation` `application` `conversion` `taux` `fin`.
  Repères : `donnees` `relation` `application` `conversion` `taux`.
- `?vue=national` — national 2019 N (3.1-3.2, 1,5 pt) : acide benzoïque C₆H₅COOH, C = 1,0·10⁻³ mol/L, σ = 8,6·10⁻³ S/m, λ₁ = 35·10⁻³ et
  λ₂ = 3,23·10⁻³ S·m²·mol⁻¹ ; « σ = (λ₁ + λ₂)·[H₃O⁺] » ; « τ = σ/(C·(λ(H₃O⁺) + λ(A⁻))) » ; ⚠ « C = 1,0·10⁻³ mol/L = 1,0 mol/m³ » ;
  « τ = 8,6·10⁻³/(1,0 × 38,23·10⁻³) = 0,22 ».
  Moments : `donnees` `relation` `conversion` `application` `resultat` `fin`.
  Repères : `donnees` `relation` `conversion` `application` `resultat`.

## 6. dilution.html (vues mesures | taux | nature)
- `?vue=mesures` — exemple D : bécher 1 (1,0·10⁻² mol/L, pH 3,4) ; pipette 10 mL → fiole de 100 mL complétée à l'eau : bécher 2 (1,0·10⁻³,
  pH 3,9) ; même geste : bécher 3 (1,0·10⁻⁴, pH 4,5) ; un tableau C · pH se remplit.
  Moments : `solution_1` `dilution_1` `solution_2` `dilution_2` `solution_3` `tableau` `fin`.
  Repères : `becher_1` `becher_2` `becher_3` `fiole` `afficheur` `tableau`.
- `?vue=taux` — colonne τ = 10^(−pH)/C ajoutée au tableau : 0,040 · 0,13 · 0,32 ; trois barres qui montent ; « plus la solution est diluée,
  plus τ est grand » ; ⚠ « le pH monte aussi (moins acide) : moins de H₃O⁺ par litre, mais une plus grande part de l'acide a réagi ».
  Moments : `relation` `taux_1` `taux_2` `taux_3` `barres` `conclusion` `fin`.
  Repères : `relation` `ligne_1` `ligne_2` `ligne_3` `barres` `conclusion`.
- `?vue=nature` — trois béchers de même C = 1,0·10⁻² mol/L : acide chlorhydrique (pH 2,0, τ = 1), acide méthanoïque (pH 2,9, τ = 0,13),
  acide éthanoïque (pH 3,4, τ = 0,040) ; trois barres ; « à même concentration, τ dépend de l'acide ».
  Moments : `trois_acides` `mesures` `taux` `barres` `conclusion` `fin`.
  Repères : `becher_1` `becher_2` `becher_3` `tableau` `barres` `conclusion`.

## 7. figures.html (?fig=…) — figures des nationaux
Écrites d'après `outils/cours/notes/cours/transformations_deux_sens_build/nationaux.md` (section « Figures pour figures.html ») : une figure par clé
`fig_<session>`, dessinée comme le sujet (axes, graduations, unités, courbes, points marqués). Pour chaque figure, moments :
`axes` `courbe` `lecture` `calcul` `fin` ; repères : `axe_x` `axe_y` `courbe` `point` `valeur` `calcul`.
- `fig_2017N` (e6) — x (mol) 0 → 0,35 ; t (min) 0 → 75 ; courbes (1) palier 0,2 mol et (2) palier 0,3 mol ; pointillé x_max = 0,3 mol ;
  `calcul` : « τ₁ = 0,2/0,3 = 0,67 ; τ₂ = 0,3/0,3 = 1 : (2) est totale ».
- `fig_2021R` (n1) — τ (0 → 1) en fonction du pH (0 → 7) ; lectures pH 2,8 → τ ≈ 0,10 et pH 3,6 → τ ≈ 0,45 ;
  `calcul` : « C = 10^(−pH)/τ : C₁ = 1,58·10⁻² mol/L ; C₂ = 5,58·10⁻⁴ mol/L ; plus diluée → τ plus grand ».

## 8. bilan.html et carte.html (modèle : chimie/cinetique-tableau/bilan.html, carte.html)
- bilan.html — fiche, blocs (moments) : `fiche` `bronsted` `ph` `taux` `deux_sens` `conductimetrie` `dilution` `redaction` `lacunes` `fin` ;
  repères : un par bloc (mêmes noms sans `lacunes`) + `fiche`. Page 2 de l'élève (lacunes, acquis, acquis_ids par `set_parameters`), comme le modèle.
  Compétences → blocs : C1 bronsted, C2 ph, C3 taux, C4 deux_sens, C5 conductimetrie, C6 dilution, C7 redaction.
  Contenu : bronsted (acide cède H⁺, base capte H⁺, couple AH/A⁻, AH ⇌ A⁻ + H⁺) ; ph (pH = −log[H₃O⁺], [H₃O⁺] = 10^(−pH), pH-mètre étalonné) ;
  taux (tableau ; x_max = C·V ; x_f = [H₃O⁺]·V ; τ = x_f/x_max ; τ = 10^(−pH)/C ; τ = 1 totale, τ < 1 limitée) ; deux_sens (⇌ ; état d'équilibre :
  quantités constantes ; équilibre dynamique) ; conductimetrie (σ = Σ λᵢ·[Xᵢ] ; σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] ; ⚠ mol/m³) ; dilution (plus diluée →
  τ plus grand ; τ dépend de l'acide) ; redaction (équation avec ⇌, tableau, relation littérale, application numérique, conclusion τ < 1).
- carte.html — moments : `centre` `bronsted` `ph` `acide_eau` `taux` `deux_sens` `equilibre` `conductimetrie` `dilution` `national` `suite` `complete` `fin` ;
  repères : `centre` + un par branche (sans `complete`). Centre : « réaction limitée : τ < 1 ». `suite` = « chapitre suivant : état d'équilibre
  d'un système chimique ».

## Diapositives servies (cours)
o1 carte
o2 acides?vue=ouverture
b1 acides?vue=acide
b2 acides?vue=base
b3 acides?vue=couple
b4 acides?vue=reaction
p1 ph?vue=definition
p2 ph?vue=calcul
p3 ph?vue=phmetre
p4 avancement?vue=acide_eau
p5 avancement?vue=base_eau
p6 avancement?vue=attendu
a1 avancement?vue=tableau
a2 avancement?vue=x_max
a3 avancement?vue=x_f
a4 avancement?vue=taux
a5 avancement?vue=totale
a6 avancement?vue=relation
e1 equilibre?vue=inverse
e2 equilibre?vue=double_fleche
e3 equilibre?vue=etat
e4 equilibre?vue=dynamique
e5 equilibre?vue=esterification
e6 figures?fig=fig_2017N
c1 conductimetrie?vue=ions
c2 conductimetrie?vue=relation
c3 conductimetrie?vue=calcul
d1 dilution?vue=mesures
d2 dilution?vue=taux
d3 dilution?vue=nature
n1 figures?fig=fig_2021R
n2 conductimetrie?vue=national
n3 avancement?vue=proportion
n4 avancement?vue=dosage
bl bilan
cr carte
