# Contrat des simulations — etat_equilibre (cours phys_ch12_etat_equilibre, « État d'équilibre d'un système chimique »)

Dossier : `frontend/public/media/simulations/chimie/etat-equilibre-tableau/`
Kit (déjà copié) : `commun.js`, `exposants.js` (de `chimie/transformations-deux-sens-tableau/`, même API : `Tableau`, `Craie`, scène 760 × 420,
`Tableau.protocole`, `craie.repere`, `play_until`, `__horsCadre`) ; feuille `ee.css` (copie de `tds.css`). Skill : `.agents/skills/simulations-au-tableau/SKILL.md`.
Moteur du déroulé : copier le bloc « Moteur du déroulé » (fonction `Moteur`, `construire`, `M.etape`, `calculer`) d'une page de
`chimie/transformations-deux-sens-tableau/` (par ex. `avancement.html`) : il est déjà corrigé — pour une étape `M.etape` dessinée en plusieurs
morceaux, la durée retenue est la plus longue (`HOLD[nom] = Math.max(HOLD[nom] || 0, …)`) ; ne pas reprendre le moteur de `cinetique-tableau/`.
Modèles de pages : `chimie/transformations-deux-sens-tableau/avancement.html` (tableau d'avancement à la craie, béchers peints, pH-mètre),
`conductimetrie.html` (cellule, afficheur, λ), `dilution.html` (béchers, tableau qui se remplit, barres), `equilibre.html` (loupe, compteurs),
`figures.html` (figures des nationaux), `bilan.html`, `carte.html` ; `chimie/cinetique-tableau/courbe.html` (axes, courbe, poignée).

## Règles communes
- Fond transparent, un seul bouton en haut (Lancer → Pause → Reprendre → Rejouer), bande du bas libre (4,5 em), rien hors du cadre 760 × 420
  (aucune étiquette coupée ni superposée, même aux positions extrêmes des poignées).
- Solutions PEINTES (vraies couleurs, dégradé, ménisque, reflet léger) ; la craie écrit les textes. Solutions acides incolores ; solution de
  sulfate de cuivre bleue, de sulfate de zinc incolore ; lame de zinc gris bleuté, de cuivre rouge cuivré ; pH-mètre gris à afficheur vert
  (pH au CENTIÈME dans ce chapitre : 3,41) ; conductimètre à afficheur (mS/m) ; loupe ronde pour les ions.
  Craie : blanc = texte, jaune = surlignage, orange = piège « ⚠ », vert = sens 1 (→), rose = sens 2 (←), bleu clair = courbe principale,
  violet clair = Qr (valeur qui change), jaune = K (valeur fixe, trait horizontal).
- Formules avec indices, exposants et charges rendus (exposants.js) : Qr, Qr,i, Qr,éq, K, K', [CH₃COO⁻], [H₃O⁺], [CH₃COOH], HCOOH, HCOO⁻,
  Cu²⁺, Zn²⁺, Zn(s), Cu(s), Al³⁺, I⁻, I₂, S₂O₈²⁻, SO₄²⁻, NH₃, NH₄⁺, HO⁻, CH₃NH₂, CH₃NH₃⁺, C₆H₅COOH, C₆H₅COO⁻, x_max, x_f, x_éq, τ, τ², σ, λ,
  10^(−pH), 10^(−2pH) ; puissances écrites en exposant ([C]^c → [C] avec c en exposant). Barre de fraction DESSINÉE (numérateur sur dénominateur),
  jamais de « / » dans une fraction d'au moins deux facteurs à l'écran. Flèches DESSINÉES : → (sens 1), ← (sens 2), ⇌ (deux sens).
  Virgule décimale. Unités : mol, mol/L, mol/m³, mL, L, S/m, mS/m, mS·m²·mol⁻¹ ; Qr, K et τ SANS unité.
- Jamais : Ka, pKa, Ke, pKe, constante d'acidité, produit ionique, autoprotolyse, Henderson, Hasselbalch, diagramme de prédominance, espèce prédominante, diagramme de distribution, indicateur coloré, zone de virage, activité, Le Chatelier, loi de modération, Guldberg, Waage, loi d'action de masse, enthalpie, entropie, critère d'évolution spontanée, évolution spontanée, Lewis, Arrhenius, Ostwald, degré d'ionisation, coefficient de dissociation, pouvoir tampon écrits à l'écran (les valeurs ci-dessous sont des mesures ; le modèle qui sert à tracer la courbe de facteurs.html n'est jamais écrit).
- Chaque vue émet `moments` (noms ci-dessous, EXACTS), accepte `play_until {moment}`, `set_time`, `set_parameters` (si poignée), `highlight {target}` ;
  `ce_qui_se_voit` dit l'étape, les valeurs affichées (pH, σ, concentrations, Qr, K, τ) et ce qui vient d'être écrit ; tous les repères ci-dessous
  sont déclarés (`craie.repere`) au plus tard au moment indiqué (sinon dès le début). Chaque vue a aussi le moment `fin`.

## Données communes (à reprendre telles quelles)
- **Exemple A (acide éthanoïque, état d'équilibre)** : CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺ ; C = 1,0·10⁻² mol/L ; V = 100 mL ; pH mesuré au centième
  = 3,41 (au dixième 3,4, comme au chapitre précédent). [H₃O⁺]éq = 10^(−3,41) = 3,89·10⁻⁴ mol/L ; τ = 10^(−pH)/C = 0,0389 ≈ 3,9 %.
  Tableau (mol/L) : [CH₃COO⁻]éq = [H₃O⁺]éq = 3,89·10⁻⁴ ; [CH₃COOH]éq = C − [H₃O⁺]éq = 1,0·10⁻² − 3,89·10⁻⁴ = 9,61·10⁻³.
  Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH] ; Qr,éq = (3,89·10⁻⁴)²/(9,61·10⁻³) = 1,57·10⁻⁵.
  Forme littérale : Qr,éq = 10^(−2pH)/(C − 10^(−pH)) ; avec τ : [A⁻]_éq = [H₃O⁺]_éq = C·τ, [AH]_éq = C·(1 − τ), K = C·τ²/(1 − τ)
  = 1,0·10⁻² × 0,0389²/(1 − 0,0389) = 1,57·10⁻⁵.
- **Exemple B (même acide, trois concentrations)** : C (mol/L) 1,0·10⁻² · 5,0·10⁻³ · 1,0·10⁻³ ↔ pH 3,41 · 3,56 · 3,93 ↔ [H₃O⁺]éq (mol/L)
  3,89·10⁻⁴ · 2,75·10⁻⁴ · 1,17·10⁻⁴ ↔ τ 0,039 · 0,055 · 0,117 ↔ Qr,éq 1,57·10⁻⁵ · 1,61·10⁻⁵ · 1,56·10⁻⁵ → **K = 1,6·10⁻⁵** (25 °C),
  même valeur aux erreurs de mesure près ; τ change.
- **Exemple C (on part des produits)** : 50 mL d'acide chlorhydrique (1,0·10⁻² mol/L) + 50 mL d'éthanoate de sodium Na⁺ + CH₃COO⁻
  (1,0·10⁻² mol/L) : les ions H₃O⁺ et CH₃COO⁻ réagissent (sens 2) ; pH final = 3,56 (3,6 au dixième, comme au chapitre précédent) ;
  [CH₃COO⁻]éq = [H₃O⁺]éq = 2,75·10⁻⁴ mol/L ; [CH₃COOH]éq = 5,0·10⁻³ − 2,75·10⁻⁴ = 4,72·10⁻³ mol/L ;
  Qr,éq = 10^(−7,12)/(5,0·10⁻³ − 10^(−3,56)) = 1,61·10⁻⁵ ≈ K :
  même état final que la solution d'acide éthanoïque à 5,0·10⁻³ mol/L (exemple B).
- **Exemple D (conductimétrie)** : acide éthanoïque C = 1,0·10⁻³ mol/L = 1,0 mol/m³ ; λ(H₃O⁺) = 35,0 mS·m²·mol⁻¹, λ(CH₃COO⁻) = 4,09 mS·m²·mol⁻¹ ;
  σ = 4,6·10⁻³ S/m (afficheur 4,6 mS/m) ; ions HO⁻ négligés. σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] → [H₃O⁺]_éq = σ/(λ(H₃O⁺) + λ(A⁻)) =
  4,6·10⁻³/(39,09·10⁻³) = 0,118 mol/m³ = 1,18·10⁻⁴ mol/L ⚠ (1 mol/L = 10³ mol/m³) → τ = 0,118 → K = C·τ²/(1 − τ) =
  1,0·10⁻³ × 0,118²/(1 − 0,118) = 1,58·10⁻⁵ ≈ 1,6·10⁻⁵ (même K que par le pH).
- **Exemple E (un autre acide)** : acide méthanoïque HCOOH + H₂O ⇌ HCOO⁻ + H₃O⁺ ; C = 1,0·10⁻² mol/L ; pH = 2,90 → [H₃O⁺]éq = 1,26·10⁻³ mol/L ;
  τ = 0,126 ≈ 0,13 ; Qr,éq = 10^(−5,80)/(1,0·10⁻² − 10^(−2,90)) = 1,81·10⁻⁴ → K = 1,8·10⁻⁴ (plus grand que 1,6·10⁻⁵ : τ plus grand).
- **Exemple F (Qr au cours de la transformation, exemple A)** : Qr,i = 0 (pas de produit au départ) ; [H₃O⁺] = [CH₃COO⁻] = 1,0·10⁻⁴ → Qr = 1,01·10⁻⁶ ;
  2,0·10⁻⁴ → 4,08·10⁻⁶ ; 3,0·10⁻⁴ → 9,28·10⁻⁶ ; 3,89·10⁻⁴ → 1,57·10⁻⁵ = Qr,éq : Qr ne bouge plus (état d'équilibre).
- **Exemple G (Qr,i d'un mélange)** : HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH ; 100 mL d'acide méthanoïque (0,10 mol/L) + 100 mL d'éthanoate de sodium
  (0,10 mol/L) + 50 mL d'acide éthanoïque (0,10 mol/L) + 50 mL de méthanoate de sodium (0,10 mol/L) ; V_T = 300 mL ;
  n (mol) : HCOOH 1,0·10⁻² ; CH₃COO⁻ 1,0·10⁻² ; CH₃COOH 5,0·10⁻³ ; HCOO⁻ 5,0·10⁻³ ; [X]ᵢ = n/V_T (ex. [HCOOH]ᵢ = 3,33·10⁻² mol/L) ;
  Qr,i = [HCOO⁻]ᵢ·[CH₃COOH]ᵢ/([HCOOH]ᵢ·[CH₃COO⁻]ᵢ) = (5,0·10⁻³ × 5,0·10⁻³)/(1,0·10⁻² × 1,0·10⁻²) = 0,25 (V_T se simplifie).
- **Exemple H (solides)** : Cu²⁺ + Zn(s) ⇌ Cu(s) + Zn²⁺ ; Qr = [Zn²⁺]/[Cu²⁺] ; [Cu²⁺]ᵢ = 0,10 mol/L, [Zn²⁺]ᵢ = 0,010 mol/L → Qr,i = 0,10.
- **Exemple I (coefficients)** : 2I⁻ + S₂O₈²⁻ ⇌ I₂ + 2SO₄²⁻ (réaction du chapitre cinétique) : Qr = [I₂]·[SO₄²⁻]²/([I⁻]²·[S₂O₈²⁻]).
  Forme générale : aA + bB ⇌ cC + dD → Qr = [C]^c·[D]^d/([A]^a·[B]^b).
- **Exemple J (réaction inverse)** : CH₃COO⁻ + H₃O⁺ ⇌ CH₃COOH + H₂O ; K' = 1/K = 1/(1,6·10⁻⁵) = 6,25·10⁴ ≈ 6,3·10⁴.
- **Exemple K (facteurs de τ)** : courbe τ en fonction de C (1,0·10⁻⁴ à 1,0·10⁻¹ mol/L, échelle des puissances de dix) pour K = 1,6·10⁻⁵ et
  K = 1,8·10⁻⁴ (points tracés, modèle jamais écrit) : C = 1,0·10⁻⁴ → τ 0,33 · 0,72 ; 1,0·10⁻³ → 0,12 · 0,34 ; 1,0·10⁻² → 0,039 · 0,13 ;
  1,0·10⁻¹ → 0,013 · 0,042.

## 1. rappel.html (vues ouverture | taux | equilibre)
- `?vue=ouverture` — deux flacons d'acide éthanoïque, étiquettes « C = 1,0·10⁻² mol/L » et « C = 1,0·10⁻³ mol/L » ; la sonde du pH-mètre plonge
  dans l'un (3,41) puis dans l'autre (3,93) ; à la craie sous chaque flacon « τ = 0,039 » et « τ = 0,117 » ; « τ change avec C…
  un nombre ne change-t-il pas ? ».
  Moments : `deux_flacons` `mesure_1` `mesure_2` `taux` `question` `fin`.
  Repères : `flacon_1` `flacon_2` `afficheur_1` `afficheur_2` `taux_1` `taux_2` `question`.
- `?vue=taux` — rappel du chapitre précédent, exemple A : tableau à la craie (CH₃COOH · H₂O · CH₃COO⁻ · H₃O⁺ ; initial C·V · excès · 0 · 0 ;
  équilibre C·V − x_éq · excès · x_éq · x_éq) ; « x_max = C·V » ; « x_éq = [H₃O⁺]éq·V » ; « τ = 10^(−pH)/C = 10^(−3,41)/1,0·10⁻² = 0,039 » ;
  « τ < 1 : réaction limitée ».
  Moments : `tableau` `x_max` `x_eq` `taux` `limitee` `fin`. Repères : `tableau` `x_max` `x_eq` `taux` `limitee`.
- `?vue=equilibre` — rappel : bécher de l'exemple A, chrono 0 → 10 min, afficheur toujours 3,41 ; loupe : deux compteurs « sens 1 » et « sens 2 »
  qui avancent ensemble ; trois barres constantes ([CH₃COOH]éq 9,61·10⁻³ ; [CH₃COO⁻]éq et [H₃O⁺]éq 3,89·10⁻⁴ mol/L) ; « état d'équilibre
  dynamique : concentrations constantes » ; « quel nombre relie ces trois concentrations ? ».
  Moments : `chrono` `compteurs` `barres` `phrase` `question` `fin`.
  Repères : `becher` `afficheur` `compteur_1` `compteur_2` `barres` `phrase` `question`.

## 2. quotient.html (vues definition | generale | eau | solides | sans_unite | initial | melange | au_cours | national | pile)
- `?vue=definition` — équation de l'exemple A ; flèches de craie : les produits montent au numérateur, les réactifs descendent au dénominateur ;
  « Qr = [CH₃COO⁻]·[H₃O⁺]/[CH₃COOH] » (barre de fraction dessinée) ; « quotient de réaction : produits en haut, réactifs en bas ».
  Moments : `equation` `produits` `reactifs` `quotient` `phrase` `fin`. Repères : `equation` `numerateur` `denominateur` `quotient` `phrase`.
- `?vue=generale` — « aA + bB ⇌ cC + dD » ; « Qr = [C]^c·[D]^d/([A]^a·[B]^b) » ; les coefficients glissent en exposants ; exemple I :
  « 2I⁻ + S₂O₈²⁻ ⇌ I₂ + 2SO₄²⁻ » → « Qr = [I₂]·[SO₄²⁻]²/([I⁻]²·[S₂O₈²⁻]) ».
  Moments : `forme` `exposants` `exemple` `qr_exemple` `fin`. Repères : `forme` `formule` `exposants` `exemple` `qr_exemple`.
- `?vue=eau` — exemple A : la molécule d'eau du membre de gauche est entourée puis barrée dans le quotient ; « l'eau est le solvant : elle
  n'apparaît pas dans Qr » ; ⚠ « pas de concentration pour l'eau solvant ».
  Moments : `equation` `eau` `barree` `phrase` `piege` `fin`. Repères : `equation` `eau` `quotient` `phrase` `piege`.
- `?vue=solides` — bécher bleu de Cu²⁺ avec une lame de zinc (exemple H) ; « Cu²⁺ + Zn(s) ⇌ Cu(s) + Zn²⁺ » ; Zn(s) et Cu(s) barrés ;
  « Qr = [Zn²⁺]/[Cu²⁺] » ; « les solides n'apparaissent pas dans Qr ».
  Moments : `becher` `equation` `solides` `quotient` `phrase` `fin`. Repères : `becher` `lame` `equation` `solides` `quotient` `phrase`.
- `?vue=sans_unite` — un état de l'exemple A en cours de transformation : [H₃O⁺] = [CH₃COO⁻] = 2,0·10⁻⁴ mol/L, [CH₃COOH] = 9,8·10⁻³ mol/L ;
  « Qr = (2,0·10⁻⁴ × 2,0·10⁻⁴)/(9,8·10⁻³) = 4,08·10⁻⁶ » ; « concentrations en mol/L ; Qr sans unité ».
  Moments : `donnees` `remplacer` `resultat` `unite` `fin`. Repères : `donnees` `remplacer` `resultat` `unite`.
- `?vue=initial` — exemple A au moment où l'acide est versé dans l'eau : « [CH₃COO⁻]ᵢ = [H₃O⁺]ᵢ = 0 » (H₃O⁺ de l'eau négligés) ;
  « Qr,i = 0 » ; « Qr,i : quotient de réaction dans l'état initial ».
  Moments : `versement` `concentrations` `qr_i` `phrase` `fin`. Repères : `becher` `concentrations` `qr_i` `phrase`.
- `?vue=melange` — exemple G : quatre flacons versés dans un grand bécher ; « V_T = 300 mL » ; « [X]ᵢ = n/V_T » ;
  « Qr,i = [HCOO⁻]ᵢ·[CH₃COOH]ᵢ/([HCOOH]ᵢ·[CH₃COO⁻]ᵢ) » ; V_T barré ; « Qr,i = (5,0·10⁻³ × 5,0·10⁻³)/(1,0·10⁻² × 1,0·10⁻²) = 0,25 ».
  Moments : `flacons` `melange` `concentrations` `quotient` `simplifier` `resultat` `fin`.
  Repères : `flacons` `becher` `volume_total` `concentrations` `quotient` `resultat`.
- `?vue=au_cours` — exemple F : axe horizontal [H₃O⁺] (0 → 4,0·10⁻⁴ mol/L) et axe vertical Qr (0 → 2,0·10⁻⁵) ; quatre points qui montent
  (0 ; 1,01·10⁻⁶ ; 4,08·10⁻⁶ ; 9,28·10⁻⁶) puis le dernier 1,57·10⁻⁵ ; un tableau de valeurs se remplit ; « Qr augmente de Qr,i = 0 jusqu'à
  Qr,éq = 1,57·10⁻⁵, puis ne bouge plus ». Poignée `x` (avancement relatif 0 → 1, défaut 0) qui déplace le point (`set_parameters {x}`).
  Moments : `axes` `depart` `points` `arrivee` `palier` `phrase` `fin`. Repères : `axe_h3o` `axe_qr` `poignee_x` `tableau` `point_eq` `phrase`.
- `?vue=national` — national 2020 R (II.2.3, 0,5 pt) : quatre flacons de 100 mL à 0,1 mol/L (HCOOH, CH₃COO⁻, CH₃COOH, HCOO⁻) ;
  « V_T = 400 mL » ; « Qr,i = (C₃V₃·C₄V₄)/(C₁V₁·C₂V₂) = 1 » ; « Qr,i se calcule avec les concentrations APRÈS mélange ».
  Moments : `donnees` `volume_total` `quotient` `resultat` `phrase` `fin`. Repères : `donnees` `volume_total` `quotient` `resultat` `phrase`.
- `?vue=pile` — national 2017 N (I.1, 0,5 pt) : deux béchers (Cu²⁺ bleu + lame de cuivre ; Al³⁺ incolore + lame d'aluminium) ;
  « 3Cu²⁺ + 2Al(s) ⇌ 3Cu(s) + 2Al³⁺ » ; « Qr,i = [Al³⁺]ᵢ²/[Cu²⁺]ᵢ³ » ; « = (6,5·10⁻¹)²/(6,5·10⁻¹)³ = 1,5 » ; « la suite (piles) : au semestre 2 ».
  Moments : `bechers` `equation` `quotient` `application` `renvoi` `fin`. Repères : `becher_cuivre` `becher_aluminium` `equation` `quotient` `resultat` `renvoi`.

## 3. equilibre.html (vues concentrations | qr_eq | expression | national_2017 | base | national_2021)
- `?vue=concentrations` — exemple A : afficheur 3,41 ; « [H₃O⁺]éq = 10^(−pH) = 3,89·10⁻⁴ mol/L » ; tableau : « [CH₃COO⁻]éq = [H₃O⁺]éq » ;
  « [CH₃COOH]éq = C − [H₃O⁺]éq = 9,61·10⁻³ mol/L » ; trois barres.
  Moments : `mesure` `h3o` `base` `acide` `barres` `fin`. Repères : `afficheur` `h3o` `base` `acide` `barres`.
- `?vue=qr_eq` — « Qr,éq = [CH₃COO⁻]éq·[H₃O⁺]éq/[CH₃COOH]éq » ; « = (3,89·10⁻⁴)²/(9,61·10⁻³) = 1,57·10⁻⁵ » ; « Qr,éq : quotient de réaction
  dans l'état d'équilibre ».
  Moments : `definition` `application` `resultat` `phrase` `fin`. Repères : `definition` `application` `resultat` `phrase`.
- `?vue=expression` — démonstration littérale : « [CH₃COO⁻]éq = [H₃O⁺]éq = 10^(−pH) » ; « [CH₃COOH]éq = C − 10^(−pH) » ;
  « Qr,éq = 10^(−2pH)/(C − 10^(−pH)) » ; vérification « 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = 1,57·10⁻⁵ ».
  Moments : `depart` `remplacer` `relation` `verifier` `fin`. Repères : `depart` `remplacer` `relation` `verifier`.
- `?vue=national_2017` — national 2017 N (II.1.2, 0,75 pt) : acide butanoïque C = 1,0·10⁻² mol/L, pH = 3,41 ;
  « Qr,éq = 10^(−2pH)/(C − 10^(−pH)) » ; « Qr,éq = 1,57·10⁻⁵ ».
  Moments : `donnees` `relation` `application` `resultat` `fin`. Repères : `donnees` `relation` `application` `resultat`.
- `?vue=base` — national 2022 R (1.4, 0,5 pt) : méthylamine C_b = 1,0·10⁻² mol/L, τ = 0,20 (donné) ; « CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + HO⁻ » ;
  « [CH₃NH₃⁺]éq = [HO⁻]éq = C_b·τ » ; « [CH₃NH₂]éq = C_b(1 − τ) » ; « Qr,éq = C_b·τ²/(1 − τ) = 1,0·10⁻² × 0,20²/0,80 = 5,0·10⁻⁴ ».
  Moments : `donnees` `equation` `tableau` `relation` `resultat` `fin`. Repères : `donnees` `equation` `tableau` `relation` `resultat`.
- `?vue=national_2021` — national 2021 N (II.2.2-2.3, 1,5 pt) : C_a = 1,0·10⁻¹ mol/L, pH = 2,88 ; « τ = 10^(−2,88)/0,10 = 0,0132 » ;
  « Qr,éq = C_a·τ²/(1 − τ) » ; « = 0,10 × 0,0132²/(1 − 0,0132) = 1,77·10⁻⁵ ».
  Moments : `donnees` `taux` `relation` `application` `resultat` `fin`. Repères : `donnees` `taux` `relation` `application` `resultat`.

## 4. constante.html (vues trois_c | produits | definition | inverse | c_tau | autre_acide)
- `?vue=trois_c` — exemple B : trois béchers (1,0·10⁻² ; 5,0·10⁻³ ; 1,0·10⁻³ mol/L) ; trois mesures (3,41 ; 3,56 ; 3,93) ; un tableau C · pH ·
  τ · Qr,éq se remplit ligne à ligne ; colonne τ : 0,039 · 0,055 · 0,117 (change) ; colonne Qr,éq : 1,57 · 1,61 · 1,56 ·10⁻⁵ (surlignée en jaune) ;
  « Qr,éq ne dépend pas de C ».
  Moments : `bechers` `mesures` `ligne_1` `ligne_2` `ligne_3` `comparer` `conclusion` `fin`.
  Repères : `becher_1` `becher_2` `becher_3` `tableau` `colonne_taux` `colonne_qr` `conclusion`.
- `?vue=produits` — exemple C : bécher d'acide chlorhydrique ; on verse l'éthanoate de sodium (flèche rose, sens 2) ; l'afficheur se stabilise
  à 3,56 ; « [CH₃COO⁻]éq = [H₃O⁺]éq = 2,75·10⁻⁴ mol/L » ; « Qr,éq = 10^(−7,12)/(5,0·10⁻³ − 10^(−3,56)) = 1,61·10⁻⁵ » ; « même valeur en partant des produits ».
  Moments : `acide` `ajout` `ph` `calcul` `conclusion` `fin`. Repères : `becher` `flacon` `afficheur` `calcul` `conclusion`.
- `?vue=definition` — encadré jaune « K = Qr,éq » ; « constante d'équilibre : ne dépend que de la température » ; « acide éthanoïque + eau :
  K = 1,6·10⁻⁵ à 25 °C » ; « K ne dépend pas de l'état initial » ; un thermomètre à côté de l'encadré.
  Moments : `encadre` `temperature` `valeur` `etat_initial` `fin`. Repères : `encadre` `thermometre` `valeur` `phrase`.
- `?vue=inverse` — exemple J : sens 1 « CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺ : K = 1,6·10⁻⁵ » ; sens 2 « CH₃COO⁻ + H₃O⁺ ⇌ CH₃COOH + H₂O » ; le quotient
  se retourne (numérateur et dénominateur échangés) ; « K' = 1/K » ; « K' = 1/(1,6·10⁻⁵) = 6,25·10⁴ ».
  Moments : `sens_1` `sens_2` `retourner` `relation` `application` `fin`. Repères : `equation_1` `equation_2` `quotient` `relation` `application`.
- `?vue=c_tau` — démonstration : tableau en concentrations « [A⁻]_éq = [H₃O⁺]_éq = C·τ » ; « [AH]_éq = C·(1 − τ) » ; « K = (C·τ)²/(C·(1 − τ)) » ;
  un C barré ; « K = C·τ²/(1 − τ) » ; vérification exemple A : « 1,0·10⁻² × 0,0389²/(1 − 0,0389) = 1,57·10⁻⁵ ».
  Moments : `tableau` `remplacer` `simplifier` `relation` `verifier` `fin`. Repères : `tableau` `remplacer` `simplifier` `relation` `verifier`.
- `?vue=autre_acide` — exemple E : bécher d'acide méthanoïque (1,0·10⁻² mol/L), afficheur 2,90 ; « [H₃O⁺]éq = 1,26·10⁻³ mol/L » ;
  « Qr,éq = 10^(−5,80)/(1,0·10⁻² − 10^(−2,90)) = 1,81·10⁻⁴ » ; « K = 1,8·10⁻⁴ » à côté de « K = 1,6·10⁻⁵ » (acide éthanoïque) ;
  « chaque réaction a sa constante K ».
  Moments : `becher` `mesure` `calcul` `comparer` `phrase` `fin`. Repères : `becher` `afficheur` `calcul` `k_ethanoique` `k_methanoique` `phrase`.

## 5. conductimetrie.html (vues relation | calcul | national)
- `?vue=relation` — exemple D : cellule dans l'acide éthanoïque à 1,0·10⁻³ mol/L, afficheur 4,6 mS/m ; « σ = λ(H₃O⁺)·[H₃O⁺] + λ(CH₃COO⁻)·[CH₃COO⁻] »
  (HO⁻ négligés) ; « [CH₃COO⁻] = [H₃O⁺] » ; « σ = (λ(H₃O⁺) + λ(A⁻))·[H₃O⁺] » ; « [H₃O⁺]_éq = σ/(λ(H₃O⁺) + λ(A⁻)) ».
  Moments : `mesure` `formule` `egalite` `factoriser` `isoler` `fin`. Repères : `cellule` `afficheur` `formule` `egalite` `relation`.
- `?vue=calcul` — « [H₃O⁺]_éq = 4,6·10⁻³/(39,09·10⁻³) = 0,118 mol/m³ » ; ⚠ « ÷ 10³ : 1,18·10⁻⁴ mol/L » ; « τ = 1,18·10⁻⁴/1,0·10⁻³ = 0,118 » ;
  « K = C·τ²/(1 − τ) = 1,0·10⁻³ × 0,118²/(1 − 0,118) = 1,58·10⁻⁵ » ; « ≈ 1,6·10⁻⁵ : même K que par le pH ».
  Moments : `donnees` `concentration` `conversion` `taux` `constante` `comparer` `fin`.
  Repères : `donnees` `concentration` `conversion` `taux` `constante` `comparer`.
- `?vue=national` — national 2019 N (3.2-3.3, 1,5 pt) : acide benzoïque C₆H₅COOH, C = 1,0·10⁻³ mol/L = 1,0 mol/m³, σ = 8,6·10⁻³ S/m,
  λ₁ = 35·10⁻³ et λ₂ = 3,23·10⁻³ S·m²·mol⁻¹ ; « τ = σ/(C·(λ₁ + λ₂)) = 0,22 » ; « K = C·τ²/(1 − τ) » ; « = 1,0·10⁻³ × 0,22²/(1 − 0,22) = 6,2·10⁻⁵ » ;
  ⚠ « dans K, C en mol/L ».
  Moments : `donnees` `taux` `relation` `application` `resultat` `fin`. Repères : `donnees` `taux` `relation` `application` `resultat` `piege`.

## 6. facteurs.html (vues dilution | nature | courbe | bilan_dilution)
- `?vue=dilution` — exemple B : trois barres τ qui montent quand C baisse (0,039 · 0,055 · 0,117) ; à côté, trois étiquettes « K = 1,6·10⁻⁵ »
  identiques ; « même K : plus C est petite, plus τ est grand ».
  Moments : `barres` `taux_1` `taux_2` `taux_3` `constante` `conclusion` `fin`.
  Repères : `barre_1` `barre_2` `barre_3` `constante` `conclusion`.
- `?vue=nature` — même C = 1,0·10⁻² mol/L : acide éthanoïque (K = 1,6·10⁻⁵, τ = 0,039) et acide méthanoïque (K = 1,8·10⁻⁴, τ = 0,13) ;
  deux barres ; « même C : plus K est grande, plus τ est grand ».
  Moments : `deux_acides` `constantes` `taux` `barres` `conclusion` `fin`.
  Repères : `becher_1` `becher_2` `constantes` `barres` `conclusion`.
- `?vue=courbe` — exemple K : axes τ (0 → 1) et C (1,0·10⁻⁴ → 1,0·10⁻¹ mol/L) ; deux courbes (acide éthanoïque, bleu clair ; acide méthanoïque,
  jaune) ; poignée `C` (`set_parameters {C}`, défaut 1,0·10⁻²) : deux points glissent sur les courbes et leurs τ s'affichent ;
  « τ dépend de K (nature de la réaction) et de l'état initial (C) ».
  Moments : `axes` `courbe_1` `courbe_2` `lecture` `phrase` `fin`. Poignée `C`.
  Repères : `axe_taux` `axe_c` `courbe_1` `courbe_2` `poignee_C` `phrase`.
- `?vue=bilan_dilution` — tableau à deux colonnes « quand on dilue » : C ↓ ; [H₃O⁺] ↓ ; pH ↑ ; τ ↑ ; K = (inchangée, encadrée en jaune) ;
  ⚠ « τ dépend de l'état initial ; K non ».
  Moments : `titre` `ligne_c` `ligne_ph` `ligne_taux` `ligne_k` `piege` `fin`.
  Repères : `titre` `ligne_c` `ligne_ph` `ligne_taux` `ligne_k` `piege`.

## 7. figures.html (?fig=…) — figures des nationaux
Écrites d'après `outils/cours/notes/cours/etat_equilibre_build/nationaux.md` (section « Figures pour figures.html ») : une figure par clé
`fig_<session>`, dessinée comme le sujet (axes, graduations, unités, courbe, points marqués). Pour chaque figure, moments :
`axes` `courbe` `lecture` `calcul` `fin` ; repères : `axe_x` `axe_y` `courbe` `point` `valeur` `calcul`.
- `fig_2017R` (n5) — n(acide) (mol) 0 → 0,6 en fonction de t (h) 0 → 200 ; palier 0,2 mol ; `lecture` : « n_éq(acide) = 0,2 mol → x_éq = 0,4 mol » ;
  `calcul` : « K = [ester]·[eau]/([acide]·[alcool]) = (0,4 × 0,4)/(0,2 × 0,2) = 4 » et « ici l'eau est un produit, pas le solvant :
  elle figure (estérification : semestre 2) ».

## 8. bilan.html et carte.html (modèle : chimie/transformations-deux-sens-tableau/bilan.html, carte.html)
- bilan.html — fiche, blocs (moments) : `fiche` `quotient` `etat_initial` `equilibre` `constante` `mesures` `facteurs` `redaction` `lacunes` `fin` ;
  repères : un par bloc (mêmes noms sans `lacunes`) + `fiche`. Page 2 de l'élève (lacunes, acquis, acquis_ids par `set_parameters`), comme le modèle.
  Compétences → blocs : C1 quotient, C2 etat_initial, C3 equilibre, C4 constante, C5 mesures, C6 facteurs, C7 redaction.
  Contenu : quotient (Qr = [C]^c·[D]^d/([A]^a·[B]^b) ; eau solvant et solides absents ; mol/L ; sans unité) ; etat_initial (Qr,i ;
  mélange : concentrations après mélange) ; equilibre (Qr,éq ; Qr,éq = 10^(−2pH)/(C − 10^(−pH))) ; constante (K = Qr,éq ; ne dépend que de
  la température ; réaction inverse K' = 1/K) ; mesures (K = C·τ²/(1 − τ) ; pH ou σ ; ⚠ mol/m³ → mol/L) ; facteurs (τ dépend de K et de C ;
  diluer : τ ↑, K inchangée) ; redaction (expression littérale, tableau, application numérique, résultat sans unité).
- carte.html — moments : `centre` `rappel` `quotient` `etat_initial` `equilibre` `constante` `inverse` `mesures` `facteurs` `national` `suite` `complete` `fin` ;
  repères : `centre` + un par branche (sans `complete`). Centre : « à l'équilibre : Qr,éq = K ». `suite` = « chapitre suivant : réactions
  acide-base ; semestre 2 : piles (Qr,i comparé à K) ».

## Diapositives servies (cours)
o1 carte
o2 rappel?vue=ouverture
r1 rappel?vue=taux
r2 rappel?vue=equilibre
q1 quotient?vue=definition
q2 quotient?vue=generale
q3 quotient?vue=eau
q4 quotient?vue=solides
q5 quotient?vue=sans_unite
i1 quotient?vue=initial
i2 quotient?vue=melange
i3 quotient?vue=au_cours
e1 equilibre?vue=concentrations
e2 equilibre?vue=qr_eq
e3 equilibre?vue=expression
k1 constante?vue=trois_c
k2 constante?vue=produits
k3 constante?vue=definition
k4 constante?vue=inverse
k5 constante?vue=c_tau
m1 constante?vue=autre_acide
m2 conductimetrie?vue=relation
m3 conductimetrie?vue=calcul
m4 conductimetrie?vue=national
f1 facteurs?vue=dilution
f2 facteurs?vue=nature
f3 facteurs?vue=courbe
f4 facteurs?vue=bilan_dilution
n1 equilibre?vue=national_2017
n2 equilibre?vue=base
n3 quotient?vue=national
n4 quotient?vue=pile
n5 figures?fig=fig_2017R
n6 equilibre?vue=national_2021
bl bilan
cr carte
