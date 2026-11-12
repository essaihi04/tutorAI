# Contrat des simulations — acides_bases (cours phys_ch13_acides_bases, « Transformations liées aux réactions acide-base »)

Dossier : `frontend/public/media/simulations/chimie/acides-bases-tableau/`
Kit (déjà copié) : `commun.js`, `exposants.js` (de `chimie/etat-equilibre-tableau/`, même API : `Tableau`, `Craie`, scène 760 × 420,
`Tableau.protocole`, `craie.repere`, `play_until`, `__horsCadre`) ; feuille `ab.css` (copie de `ee.css`). Skill : `.agents/skills/simulations-au-tableau/SKILL.md`.
Moteur du déroulé : copier le bloc « Moteur du déroulé » (fonction `Moteur`, `construire`, `M.etape`, `calculer`) d'une page de
`chimie/etat-equilibre-tableau/` (par ex. `constante.html`) : il est déjà corrigé — pour une étape `M.etape` dessinée en plusieurs
morceaux, la durée retenue est la plus longue (`HOLD[nom] = Math.max(HOLD[nom] ?? 0, …)`) ; ne pas reprendre le moteur de `cinetique-tableau/`.
Modèles de pages : `chimie/etat-equilibre-tableau/rappel.html` (béchers peints, pH-mètre au centième), `constante.html` (tableau qui se remplit),
`conductimetrie.html` (cellule, afficheur, λ), `facteurs.html` (axes, courbes, poignée `C`), `figures.html` (figures des nationaux),
`bilan.html`, `carte.html` ; `chimie/transformations-deux-sens-tableau/avancement.html` (tableau d'avancement à la craie).

## Règles communes
- Fond transparent, un seul bouton en haut (Lancer → Pause → Reprendre → Rejouer), bande du bas libre (4,5 em), rien hors du cadre 760 × 420
  (aucune étiquette coupée ni superposée, même aux positions extrêmes des poignées).
- Solutions PEINTES (vraies couleurs, dégradé, ménisque, reflet léger) ; la craie écrit les textes. Solutions acides, basiques et eau
  incolores ; avec un indicateur : BBT jaune (pH < 6,0), vert (6,0 à 7,6), bleu (pH > 7,6) ; hélianthine rouge / orange / jaune ;
  rouge de méthyle rouge / jaune ; rouge de crésol jaune / rouge ; pH-mètre gris à afficheur vert (pH au CENTIÈME pour une solution
  mesurée : 3,41 ; 10,60 ; courbes de dosage lues au dixième : 8,3) ; burette graduée (0 → 25 mL ou 0 → 50 mL) avec robinet et goutte,
  agitateur magnétique (barreau qui tourne), conductimètre à afficheur (mS/m) ; loupe ronde pour les ions et molécules.
  Craie : blanc = texte, jaune = surlignage et constante (Ka, pKa, K, Ke : trait ou encadré), orange = piège « ⚠ », bleu clair = courbe principale,
  vert = forme basique A⁻ / domaine de la base, rose = forme acide AH / domaine de l'acide, violet clair = point qui bouge (poignée).
- Formules avec indices, exposants et charges rendus (exposants.js) : H₃O⁺, HO⁻, H₂O, CH₃COOH, CH₃COO⁻, HCOOH, HCOO⁻, NH₃, NH₄⁺, CH₃NH₂, CH₃NH₃⁺,
  C₂H₅COOH, C₂H₅COO⁻, (CH₃)₃N, (CH₃)₃NH⁺, R–NH₂, R–NH₃⁺, Na⁺, Cl⁻, AH, A⁻, HInd, Ind⁻, Ke, pKe, Ka, pKa, Ka₁, Ka₂, pKa₁, pKa₂, K, Qr,éq,
  [X]_éq, C_A, V_A, C_B, V_B, V_BE, V_AE, pH_E, τ, σ, λ, 10^(−pH), 10^(pH − 14), 10^(pKa₂ − pKa₁) ; barre de fraction DESSINÉE (numérateur
  sur dénominateur), jamais de « / » dans une fraction d'au moins deux facteurs à l'écran (un couple « AH/A⁻ » s'écrit avec « / »).
  Flèches DESSINÉES : ⇌ (réaction limitée, acide ou base avec l'eau, réaction acide-base générale), → (réaction de DOSAGE, totale).
  Virgule décimale. Unités : mol, mol/L, mL, L, g/L, S/m, mS/m, mS·m²·mol⁻¹ ; Ke, Ka, pKa, K, pH et τ SANS unité.
- Jamais : Henderson, Hasselbalch, diagramme de Flood, Flood, Lewis, Arrhenius, Ostwald, loi de dilution, degré d'ionisation, coefficient de dissociation, activité chimique, coefficient d'activité, pouvoir tampon, capacité tampon, Le Chatelier, loi de modération, Guldberg, loi d'action de masse, enthalpie, entropie, dosage potentiométrique, potentiométrique, méthode de Gran, droite de Gran, dérivée seconde, normalité, équivalent-gramme, polyacide, diacide, deux sauts de pH, propagation des incertitudes, incertitude-type, Kb, pKb, pOH, constante de basicité, critère d'évolution spontanée, évolution spontanée écrits à l'écran (les valeurs ci-dessous sont des mesures ; le modèle qui sert à tracer les courbes de dosage et de distribution n'est jamais écrit).
- Chaque vue émet `moments` (noms ci-dessous, EXACTS), accepte `play_until {moment}`, `set_time`, `set_parameters` (si poignée), `highlight {target}` ;
  `ce_qui_se_voit` dit l'étape, les valeurs affichées (pH, concentrations, Ka, pKa, K, V_B, σ) et ce qui vient d'être écrit ; tous les repères
  ci-dessous sont déclarés (`craie.repere`) au plus tard au moment indiqué (sinon dès le début). Chaque vue a aussi le moment `fin`.

## Données communes (à reprendre telles quelles)
- **Exemple A (autoprotolyse, eau pure à 25 °C)** : 2H₂O ⇌ H₃O⁺ + HO⁻ ; pH-mètre dans l'eau pure : 7,00 ; [H₃O⁺] = [HO⁻] = 1,0·10⁻⁷ mol/L ;
  Ke = [H₃O⁺]·[HO⁻] = 1,0·10⁻¹⁴ (produit ionique de l'eau, 25 °C, sans unité) ; pKe = −log Ke = 14.
- **Exemple B (trois solutions, 25 °C)** : acide éthanoïque 1,0·10⁻² mol/L : pH 3,41, [H₃O⁺] = 3,89·10⁻⁴, [HO⁻] = Ke/[H₃O⁺] = 2,57·10⁻¹¹ mol/L
  (acide : [H₃O⁺] > [HO⁻], pH < 7) ; eau pure : 7,00, [H₃O⁺] = [HO⁻] (neutre) ; ammoniac 1,0·10⁻² mol/L : pH 10,60, [H₃O⁺] = 2,51·10⁻¹¹,
  [HO⁻] = 10^(pH − 14) = 3,98·10⁻⁴ mol/L (basique : [HO⁻] > [H₃O⁺], pH > 7).
- **Exemple C (soude)** : solution d'hydroxyde de sodium Na⁺ + HO⁻, C = 1,0·10⁻² mol/L (réaction totale) : [HO⁻] = 1,0·10⁻² mol/L ;
  [H₃O⁺] = Ke/[HO⁻] = 1,0·10⁻¹⁴/1,0·10⁻² = 1,0·10⁻¹² mol/L ; pH = 12,00.
- **Exemple D (base faible dans l'eau, national 2020 N)** : NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ ; C = 1,0·10⁻² mol/L ; pH = 10,60 ;
  [HO⁻]_éq = Ke/[H₃O⁺]_éq = 10^(−14)/10^(−10,60) = 3,98·10⁻⁴ mol/L ; tableau : [NH₄⁺]_éq = [HO⁻]_éq ; τ = [HO⁻]_éq/C = 3,98·10⁻² ≈ 0,040 ;
  Qr,éq = [HO⁻]²/(C − [HO⁻]) = 1,65·10⁻⁵. Méthylamine (national 2022 R) : CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + HO⁻ ; C = 1,0·10⁻² mol/L ; pH = 11,30 ;
  [HO⁻]_éq = 10^(11,30 − 14) = 2,0·10⁻³ mol/L ; τ = 0,20 ; Qr,éq = C·τ²/(1 − τ) = 5,0·10⁻⁴.
- **Exemple E (constante d'acidité)** : AH + H₂O ⇌ A⁻ + H₃O⁺ ; Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq (= K de la réaction de l'acide avec l'eau) ;
  pKa = −log Ka ; Ka = 10^(−pKa). Acide éthanoïque (chapitre précédent : C = 1,0·10⁻² mol/L, pH = 3,41) : Ka = Qr,éq = 1,57·10⁻⁵ ≈ 1,6·10⁻⁵ ;
  pKa = −log(1,57·10⁻⁵) = 4,80 → **pKa = 4,8**. Couples : CH₃COOH/CH₃COO⁻ pKa 4,8 (Ka 1,6·10⁻⁵) ; HCOOH/HCOO⁻ pKa 3,75 (Ka 1,8·10⁻⁴) ;
  NH₄⁺/NH₃ pKa 9,2 (Ka 6,3·10⁻¹⁰) ; CH₃NH₃⁺/CH₃NH₂ pKa 10,7 (Ka 2,0·10⁻¹¹) ; H₃O⁺/H₂O : Ka = 1, pKa(H₃O⁺/H₂O) = 0 ;
  H₂O/HO⁻ : Ka = Ke, pKa(H₂O/HO⁻) = 14.
  Couple d'une base (exemple D) : Ka = [NH₃]_éq·[H₃O⁺]_éq/[NH₄⁺]_éq ; Qr,éq de NH₃ + H₂O = Ke/Ka, donc Ka = Ke/Qr,éq = 10⁻¹⁴/1,65·10⁻⁵
  = 6,06·10⁻¹⁰ ; pKa = 9,22 ≈ 9,2.
- **Exemple F (comparer, même C = 1,0·10⁻² mol/L)** : acides : acide éthanoïque (pKa 4,8) pH 3,41, τ = 0,039 ; acide méthanoïque (pKa 3,75)
  pH 2,90, τ = 0,126 → plus Ka est grand (pKa petit), plus τ est grand et plus le pH est petit : l'acide méthanoïque est le plus fort.
  Bases : ammoniac (pKa 9,2) pH 10,60, τ = 0,040 ; méthylamine (pKa 10,7) pH 11,30, τ = 0,20 → plus le pKa du couple est grand, plus la base
  est forte (τ et pH plus grands). Classement sur un axe des pKa : 0 (H₃O⁺/H₂O) · 3,75 · 4,8 · 9,2 · 10,7 · 14 (H₂O/HO⁻).
- **Exemple G (constante d'une réaction acide-base)** : AH₁ + A₂⁻ ⇌ A₁⁻ + AH₂ ; K = [A₁⁻]_éq·[AH₂]_éq/([AH₁]_éq·[A₂⁻]_éq) ; on multiplie
  en haut et en bas par [H₃O⁺]_éq : **K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁)** (Ka₁ : couple de l'acide qui réagit ; Ka₂ : couple de la base qui réagit).
  HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH : K = 10^(4,8 − 3,75) = 10^(1,05) = 11,2 ≈ 11. Sens inverse (CH₃COOH + HCOO⁻) : K = 1/11,2 = 8,9·10⁻².
  CH₃COOH + NH₃ ⇌ CH₃COO⁻ + NH₄⁺ : K = 10^(9,2 − 4,8) = 10^(4,4) = 2,5·10⁴. Réaction avec HO⁻ (couple H₂O/HO⁻, Ka = Ke) :
  CH₃COOH + HO⁻ → CH₃COO⁻ + H₂O : **K = Ka/Ke** = 10^(14 − 4,8) = 10^(9,2) = 1,6·10⁹ « K > 10⁴ : réaction pratiquement totale ».
  National 2020 R : HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH ; pKa(CH₃COOH/CH₃COO⁻) = 4,8 (Ka₁ du sujet) ; pKa(HCOOH/HCOO⁻) = 3,8 (Ka₂ du sujet) ;
  K = Ka₂/Ka₁ (notation du sujet) = 10^(4,8 − 3,8) = 10.
- **Exemple H (prédominance, distribution, acide éthanoïque pKa = 4,8)** : **pH = pKa + log([A⁻]_éq/[AH]_éq)** (de l'expression de Ka) ;
  [A⁻] = [AH] → pH = pKa = 4,8 ; [A⁻]/[AH] = 10 → pH = 5,8 ; [A⁻]/[AH] = 0,1 → pH = 3,8. Domaines : pH < pKa : AH prédomine ;
  pH > pKa : A⁻ prédomine ; pH = pKa : [AH] = [A⁻]. Distribution (% AH / % A⁻) : pH 2,8 → 99,0 / 1,0 ; 3,8 → 90,9 / 9,1 ; 4,8 → 50 / 50 ;
  5,8 → 9,1 / 90,9 ; 6,8 → 1,0 / 99,0 ; les deux courbes se croisent à pH = pKa (50 %). Solution de l'exemple B (pH 3,41 < 4,8) : AH prédomine.
- **Exemple I (indicateurs colorés)** : un indicateur est un couple HInd/Ind⁻ dont les deux formes ont des couleurs différentes ;
  teinte acide si HInd prédomine, teinte basique si Ind⁻ prédomine ; zone de virage : teinte « sensible » (mélange des deux couleurs),
  elle encadre le pKa de l'indicateur. Tableau : hélianthine 3,1 – 4,4 (rouge / jaune) ; rouge de méthyle 4,2 – 6,2 (rouge / jaune) ;
  BBT 6,0 – 7,6 (jaune / bleu, vert dans la zone ; pKa ≈ 7,0) ; rouge de crésol 7,2 – 8,8 (jaune / rouge). BBT dans l'exemple B : jaune (3,41),
  vert (7,00), bleu (10,60).
- **Exemple J (dosage d'un acide faible par une base forte)** : V_A = 20,0 mL d'acide éthanoïque C_A = 1,0·10⁻² mol/L (pKa 4,8) par la soude
  C_B = 1,0·10⁻² mol/L ; burette 0 → 40 mL. Réaction de dosage (rapide, totale, unique) : CH₃COOH + HO⁻ → CH₃COO⁻ + H₂O (K = 1,6·10⁹).
  n_A = C_A·V_A = 2,0·10⁻⁴ mol. Équivalence : réactifs dans les proportions stœchiométriques : **C_A·V_A = C_B·V_BE** → V_BE = 20,0 mL.
  Courbe pH = f(V_B) (points calculés, modèle jamais écrit) : V_B (mL) 0 · 2 · 5 · 10 · 15 · 18 · 19 · 19,5 · 20 · 20,5 · 21 · 22 · 25 · 30 · 40
  ↔ pH 3,41 · 3,91 · 4,34 · 4,80 · 5,28 · 5,76 · 6,08 · 6,39 · 8,25 · 10,09 · 10,39 · 10,68 · 11,05 · 11,30 · 11,52.
  Point d'équivalence E (20,0 mL ; 8,3) par la méthode des tangentes (deux tangentes parallèles de part et d'autre du saut, leur parallèle
  équidistante coupe la courbe en E) ou au maximum de la courbe dérivée dpH/dV_B (pic à 20,0 mL : dpH/dV_B ≈ 11,5 mL⁻¹ entre 19,9 et 20,1 mL).
  pH_E = 8,3 > 7 (à l'équivalence, la solution contient des ions CH₃COO⁻, une base). Demi-équivalence V_B = V_BE/2 = 10,0 mL : [CH₃COOH] = [CH₃COO⁻]
  → pH = pKa à V_B = V_BE/2 : pH = 4,8. Indicateur : rouge de crésol (7,2 – 8,8 contient 8,3) ; BBT et hélianthine non.
- **Exemple K (acide fort par base forte)** : V_A = 20,0 mL d'acide chlorhydrique C_A = 1,0·10⁻² mol/L par la soude C_B = 1,0·10⁻² mol/L ;
  H₃O⁺ + HO⁻ → 2H₂O ; V_BE = 20,0 mL ; pH : 0 → 2,00 ; 5 → 2,22 ; 10 → 2,48 ; 15 → 2,85 ; 18 → 3,28 ; 19 → 3,59 ; 19,5 → 3,90 ; 20 → 7,00 ;
  20,5 → 10,09 ; 21 → 10,39 ; 25 → 11,05 ; 30 → 11,30 ; 40 → 11,52 ; **pH_E = 7,0** ; indicateur : BBT.
- **Exemple L (base faible par acide fort)** : V_B = 20,0 mL d'ammoniac C_B = 1,0·10⁻² mol/L par l'acide chlorhydrique C_A = 1,0·10⁻² mol/L ;
  NH₃ + H₃O⁺ → NH₄⁺ + H₂O ; **C_B·V_B = C_A·V_AE** → V_AE = 20,0 mL ; pH (V_A en mL) : 0 → 10,59 ; 2 → 10,09 ; 5 → 9,66 ; 10 → 9,20 ; 15 → 8,72 ;
  18 → 8,24 ; 19 → 7,92 ; 19,5 → 7,61 ; 20 → 5,75 ; 20,5 → 3,91 ; 21 → 3,61 ; 22 → 3,32 ; 25 → 2,95 ; 30 → 2,70 ; 40 → 2,48 ;
  **pH_E = 5,7 < 7** (NH₄⁺, un acide) ; demi-équivalence 10 mL : pH = 9,2 = pKa(NH₄⁺/NH₃) ; indicateur : rouge de méthyle (4,2 – 6,2).
- **Exemple M (dosage conductimétrique)** : V_A = 20,0 mL d'acide chlorhydrique C_A = 1,0·10⁻² mol/L + 200 mL d'eau (pour garder des droites)
  par la soude C_B = 1,0·10⁻¹ mol/L ; V_BE = C_A·V_A/C_B = 2,0 mL ; λ (mS·m²·mol⁻¹) : H₃O⁺ 35,0 ; HO⁻ 19,9 ; Na⁺ 5,01 ; Cl⁻ 7,63 ;
  σ (mS/m) : V_B = 0 → 38,8 ; 0,5 → 31,9 ; 1,0 → 25,0 ; 1,5 → 18,2 ; 2,0 → 11,4 ; 2,5 → 17,0 ; 3,0 → 22,5 ; 4,0 → 33,5 ;
  avant E : chaque H₃O⁺ (λ = 35,0) est remplacé par un Na⁺ (λ = 5,01) : σ diminue ; après E : Na⁺ et HO⁻ s'ajoutent : σ augmente ;
  équivalence à la rupture de pente (intersection des deux droites) : V_BE = 2,0 mL.
- **Exemple N (rédaction)** : concentration massique C_m = C·M ; dilution F fois : C₀ = F·C (national 2025 N : C_A = 0,10 × 9,6/20,0
  = 4,8·10⁻² mol/L, C₀ = 100·C_A = 4,80 mol/L, C_m = 4,80 × 104 = 499 g/L ≈ 500 g/L).

## 1. eau.html (vues ouverture | rappel | autoprotolyse | ke | solutions | ho | soude)
- `?vue=ouverture` — trois béchers incolores identiques (« vinaigre dilué », « eau pure », « ammoniac dilué ») ; le pH-mètre plonge dans chacun :
  3,41 · 7,00 · 10,60 ; une goutte de BBT dans chacun : jaune · vert · bleu ; à la craie « même aspect, trois pH : qu'y a-t-il dans l'eau ? ».
  Moments : `trois_bechers` `mesure_1` `mesure_2` `mesure_3` `indicateur` `question` `fin`.
  Repères : `becher_1` `becher_2` `becher_3` `afficheur` `couleurs` `question`.
- `?vue=rappel` — rappel des chapitres précédents : « acide : donneur de proton H⁺ ; base : accepteur de proton H⁺ » ; couple « AH/A⁻ :
  AH ⇌ A⁻ + H⁺ » ; exemples CH₃COOH/CH₃COO⁻, NH₄⁺/NH₃, H₃O⁺/H₂O, H₂O/HO⁻ (l'eau dans deux couples) ; « pH = −log[H₃O⁺] ;
  [H₃O⁺] = 10^(−pH) » ; « pH = 3,41 → [H₃O⁺] = 3,89·10⁻⁴ mol/L ».
  Moments : `acide_base` `couple` `exemples` `eau_deux_couples` `ph` `fin`. Repères : `definition` `couple` `exemples` `eau` `ph`.
- `?vue=autoprotolyse` — loupe dans l'eau pure : deux molécules H₂O se rencontrent, un proton H⁺ passe de l'une à l'autre (flèche jaune) :
  un H₃O⁺ et un HO⁻ apparaissent ; rarement (une paire pour plusieurs centaines de millions de molécules) ; à la craie « 2H₂O ⇌ H₃O⁺ + HO⁻ » ;
  « autoprotolyse de l'eau : réaction entre deux molécules d'eau » ; « eau pure : [H₃O⁺] = [HO⁻] = 1,0·10⁻⁷ mol/L (pH 7,00) ».
  Moments : `loupe` `transfert` `ions` `equation` `phrase` `concentrations` `fin`.
  Repères : `loupe` `proton` `equation` `phrase` `concentrations`.
- `?vue=ke` — « Ke = [H₃O⁺]·[HO⁻] » (encadré jaune) ; « produit ionique de l'eau » ; eau pure : « 1,0·10⁻⁷ × 1,0·10⁻⁷ = 1,0·10⁻¹⁴ » ;
  « à 25 °C : Ke = 1,0·10⁻¹⁴ (sans unité) » ; « pKe = −log Ke = 14 » ; thermomètre à 25 °C ; « vrai dans TOUTE solution aqueuse ».
  Moments : `produit` `calcul` `valeur` `pke` `toute_solution` `fin`. Repères : `encadre` `calcul` `valeur` `pke` `thermometre` `phrase`.
- `?vue=solutions` — axe des pH 0 → 14, repère 7 ; trois béchers de l'exemple B placés sur l'axe (3,41 · 7,00 · 10,60) ; sous chacun deux barres
  [H₃O⁺] et [HO⁻] (échelle des puissances de dix) ; « acide : [H₃O⁺] > [HO⁻], pH < 7 » ; « neutre : [H₃O⁺] = [HO⁻], pH = 7 » ;
  « basique : [HO⁻] > [H₃O⁺], pH > 7 » (à 25 °C). Poignée `pH` (`set_parameters {pH}`, 0 → 14, défaut 3,41) : un quatrième bécher glisse
  sur l'axe, ses deux barres et le mot (acide / neutre / basique) changent.
  Moments : `axe` `acide` `neutre` `basique` `regle` `fin`. Poignée `pH`.
  Repères : `axe_ph` `becher_acide` `becher_neutre` `becher_basique` `barres` `regle` `poignee_ph`.
- `?vue=ho` — « [HO⁻] = Ke/[H₃O⁺] » ; acide éthanoïque pH 3,41 : « [HO⁻] = 1,0·10⁻¹⁴/3,89·10⁻⁴ = 2,57·10⁻¹¹ mol/L » ; ammoniac pH 10,60 :
  « [HO⁻] = 10^(pH − 14) = 10^(−3,40) = 3,98·10⁻⁴ mol/L » ; ⚠ « [HO⁻] n'est pas 10^(−pH) ».
  Moments : `relation` `acide` `base` `forme_ph` `piege` `fin`. Repères : `relation` `acide` `base` `forme_ph` `piege`.
- `?vue=soude` — exemple C : flacon de soude (Na⁺ + HO⁻, 1,0·10⁻² mol/L) versé dans un bécher ; « [HO⁻] = C = 1,0·10⁻² mol/L » ;
  « [H₃O⁺] = Ke/[HO⁻] = 1,0·10⁻¹² mol/L » ; « pH = −log[H₃O⁺] = 12,00 » ; afficheur 12,00.
  Moments : `flacon` `ho` `h3o` `ph` `afficheur` `fin`. Repères : `flacon` `ho` `h3o` `ph` `afficheur`.

## 2. base.html (vues constante | ammoniac | taux | national)
- `?vue=constante` — rappel du chapitre précédent : acide AH dans l'eau, tableau en concentrations « [A⁻]_éq = [H₃O⁺]_éq = C·τ ;
  [AH]_éq = C·(1 − τ) » ; « K = C·τ²/(1 − τ) » ; « K = Qr,éq ne dépend que de la température » ; acide éthanoïque « K = 1,6·10⁻⁵ » ;
  « et une base dans l'eau ? » (point d'interrogation jaune).
  Moments : `tableau` `relation` `constante` `valeur` `question` `fin`. Repères : `tableau` `relation` `constante` `valeur` `question`.
- `?vue=ammoniac` — exemple D : bécher d'ammoniac 1,0·10⁻² mol/L, afficheur 10,60 ; « NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ » (l'eau joue l'acide) ;
  loupe : NH₃ capte un H⁺ de H₂O ; « [H₃O⁺]_éq = 10^(−10,60) = 2,51·10⁻¹¹ mol/L » ; « [HO⁻]_éq = Ke/[H₃O⁺]_éq = 3,98·10⁻⁴ mol/L ».
  Moments : `becher` `mesure` `equation` `loupe` `h3o` `ho` `fin`. Repères : `becher` `afficheur` `equation` `loupe` `h3o` `ho`.
- `?vue=taux` — tableau d'avancement (NH₃ · H₂O · NH₄⁺ · HO⁻ ; initial C·V · excès · 0 · 0 ; équilibre C·V − x_éq · excès · x_éq · x_éq) ;
  « x_max = C·V » ; « x_éq = [HO⁻]_éq·V » ; « τ = [HO⁻]_éq/C » ; « τ = 3,98·10⁻⁴/1,0·10⁻² = 0,040 » ; « τ < 1 : réaction limitée » ;
  ⚠ « pour une base, τ passe par [HO⁻], donc par Ke ».
  Moments : `tableau` `x_max` `x_eq` `relation` `application` `limitee` `fin`.
  Repères : `tableau` `x_max` `x_eq` `relation` `application` `piege`.
- `?vue=national` — national 2022 R (1.3, 0,5 pt) : méthylamine C_b = 1,0·10⁻² mol/L, pH = 11,30 ; « CH₃NH₂ + H₂O ⇌ CH₃NH₃⁺ + HO⁻ » ;
  « [HO⁻]_éq = 10^(pH − 14) = 2,0·10⁻³ mol/L » ; « τ = 2,0·10⁻³/1,0·10⁻² = 0,20 » ; « Qr,éq = C·τ²/(1 − τ) = 5,0·10⁻⁴ » (1.4).
  Moments : `donnees` `equation` `ho` `taux` `quotient` `fin`. Repères : `donnees` `equation` `ho` `taux` `quotient`.

## 3. acidite.html (vues definition | pka | mesure | ammonium | eau)
- `?vue=definition` — « AH + H₂O ⇌ A⁻ + H₃O⁺ » ; la constante d'équilibre de CETTE réaction reçoit un nom : « constante d'acidité du couple AH/A⁻ » ;
  « Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq » (encadré jaune, barre dessinée) ; « Ka ne dépend que de la température ; sans unité ».
  Moments : `equation` `nom` `expression` `phrase` `fin`. Repères : `equation` `nom` `expression` `phrase`.
- `?vue=pka` — « pKa = −log Ka » ; « Ka = 10^(−pKa) » ; acide éthanoïque « Ka = 1,6·10⁻⁵ → pKa = 4,8 » ; acide méthanoïque « Ka = 1,8·10⁻⁴ →
  pKa = 3,75 » ; deux flèches : « Ka plus grand ⇔ pKa plus petit ».
  Moments : `definition` `inverse` `ethanoique` `methanoique` `sens` `fin`. Repères : `definition` `inverse` `ethanoique` `methanoique` `sens`.
- `?vue=mesure` — exemple E : bécher d'acide éthanoïque 1,0·10⁻² mol/L, afficheur 3,41 ; « Ka = Qr,éq = 10^(−2pH)/(C − 10^(−pH)) » ;
  « Ka = 10^(−6,82)/(1,0·10⁻² − 10^(−3,41)) = 1,57·10⁻⁵ » ; « pKa = −log(1,57·10⁻⁵) = 4,8 » ; encart « national 2017 N : acide butanoïque,
  Qr,éq = 1,57·10⁻⁵ → pKa = 4,8 (0,5 pt) ».
  Moments : `becher` `mesure` `relation` `application` `pka` `national` `fin`.
  Repères : `becher` `afficheur` `relation` `application` `pka` `national`.
- `?vue=ammonium` — couple NH₄⁺/NH₃ : « Ka = [NH₃]_éq·[H₃O⁺]_éq/[NH₄⁺]_éq » ; réaction de la base avec l'eau « NH₃ + H₂O ⇌ NH₄⁺ + HO⁻ :
  Qr,éq = [NH₄⁺]_éq·[HO⁻]_éq/[NH₃]_éq » ; on multiplie en haut et en bas par [H₃O⁺]_éq ; « Qr,éq = Ke/Ka » ; « Ka = Ke/Qr,éq » ;
  national 2020 N : « Ka = 1,0·10⁻¹⁴/1,65·10⁻⁵ = 6,06·10⁻¹⁰ » ; « pKa = 9,2 ».
  Moments : `ka` `quotient` `multiplier` `relation` `application` `pka` `fin`.
  Repères : `ka` `quotient` `multiplier` `relation` `application` `pka`.
- `?vue=eau` — l'eau dans deux couples : « H₃O⁺/H₂O : Ka = 1 ; pKa(H₃O⁺/H₂O) = 0 » ; « H₂O/HO⁻ : Ka = [HO⁻]·[H₃O⁺] = Ke ; pKa(H₂O/HO⁻) = 14 » ;
  deux étiquettes jaunes posées aux bouts d'un axe des pKa (0 et 14) ; « les couples étudiés en solution aqueuse ont un pKa entre 0 et 14 ».
  Moments : `couple_1` `couple_2` `axe` `phrase` `fin`. Repères : `couple_1` `couple_2` `axe` `phrase`.

## 4. comparer.html (vues acides | bases | classement | reaction | puissance | totale | national)
- `?vue=acides` — exemple F : deux béchers 1,0·10⁻² mol/L, acide éthanoïque (pKa 4,8) et acide méthanoïque (pKa 3,75) ; afficheurs 3,41 et 2,90 ;
  un tableau se remplit (pKa · Ka · pH · τ) ; deux barres τ (0,039 et 0,126) ; « même C : plus Ka est grand (pKa petit), plus τ est grand,
  plus le pH est petit » ; « l'acide méthanoïque est le plus fort ».
  Moments : `bechers` `mesures` `tableau` `barres` `regle` `conclusion` `fin`.
  Repères : `becher_1` `becher_2` `tableau` `barres` `regle` `conclusion`.
- `?vue=bases` — exemple F : ammoniac (pKa 9,2) et méthylamine (pKa 10,7), 1,0·10⁻² mol/L ; afficheurs 10,60 et 11,30 ; barres τ 0,040 et 0,20 ;
  « même C : plus le pKa du couple est grand, plus la base est forte (τ et pH plus grands) ».
  Moments : `bechers` `mesures` `tableau` `barres` `regle` `fin`. Repères : `becher_1` `becher_2` `tableau` `barres` `regle`.
- `?vue=classement` — axe vertical des pKa 0 → 14 ; les couples s'y posent : H₃O⁺/H₂O (0), HCOOH/HCOO⁻ (3,75), CH₃COOH/CH₃COO⁻ (4,8),
  NH₄⁺/NH₃ (9,2), CH₃NH₃⁺/CH₃NH₂ (10,7), H₂O/HO⁻ (14) ; acides à gauche, bases à droite ; flèche « acide de plus en plus fort » vers le bas,
  « base de plus en plus forte » vers le haut.
  Moments : `axe` `couples` `acides` `bases` `fleches` `fin`. Repères : `axe` `couples` `fleche_acides` `fleche_bases`.
- `?vue=reaction` — exemple G : « AH₁ + A₂⁻ ⇌ A₁⁻ + AH₂ » ; « K = [A₁⁻]_éq·[AH₂]_éq/([AH₁]_éq·[A₂⁻]_éq) » ; « × [H₃O⁺]_éq/[H₃O⁺]_éq » (craie jaune) ;
  les deux fractions se séparent : « Ka₁ » et « 1/Ka₂ » ; « K = Ka₁/Ka₂ ».
  Moments : `equation` `quotient` `multiplier` `separer` `relation` `fin`.
  Repères : `equation` `quotient` `multiplier` `separer` `relation`.
- `?vue=puissance` — « K = Ka₁/Ka₂ » ; « K = 10^(pKa₂ − pKa₁) » ; HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH : « K = 10^(4,8 − 3,75) = 11 » ;
  sens inverse : « K = 1/11,2 = 8,9·10⁻² » ; CH₃COOH + NH₃ ⇌ CH₃COO⁻ + NH₄⁺ : « K = 10^(9,2 − 4,8) = 2,5·10⁴ » ;
  ⚠ « Ka₁ : couple de l'acide qui réagit ».
  Moments : `relation` `exemple_1` `inverse` `exemple_2` `piege` `fin`.
  Repères : `relation` `exemple_1` `inverse` `exemple_2` `piege`.
- `?vue=totale` — « CH₃COOH + HO⁻ → CH₃COO⁻ + H₂O » ; couple H₂O/HO⁻ : Ka = Ke ; « K = Ka/Ke = 10^(14 − 4,8) = 1,6·10⁹ » ;
  « K > 10⁴ : réaction pratiquement totale » ; « elle servira au dosage ».
  Moments : `equation` `couple_eau` `relation` `application` `totale` `fin`.
  Repères : `equation` `couple_eau` `relation` `application` `totale`.
- `?vue=national` — national 2020 R (2.2, 0,5 pt) : 400 mL (HCOOH, CH₃COO⁻, CH₃COOH, HCOO⁻) ; « HCOOH + CH₃COO⁻ ⇌ HCOO⁻ + CH₃COOH » ;
  « Ka₁ : CH₃COOH/CH₃COO⁻, pKa₁ = 4,8 ; Ka₂ : HCOOH/HCOO⁻, pKa₂ = 3,8 » (notation du sujet) ; « K = Ka₂/Ka₁ = 10^(pKa₁ − pKa₂) = 10 » ;
  ⚠ « lire qui est Ka₁ dans le sujet ».
  Moments : `donnees` `equation` `couples` `relation` `resultat` `piege` `fin`.
  Repères : `donnees` `equation` `couples` `relation` `resultat` `piege`.

## 5. predominance.html (vues relation | domaines | distribution | indicateur | virage)
- `?vue=relation` — « Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq » ; on prend −log des deux côtés ; « −log Ka = −log[H₃O⁺]_éq − log([A⁻]_éq/[AH]_éq) » ;
  « pH = pKa + log([A⁻]_éq/[AH]_éq) » (encadré) ; vérification « [A⁻] = [AH] → pH = pKa = 4,8 » ; « [A⁻]/[AH] = 10 → pH = 5,8 ».
  Moments : `ka` `log` `relation` `egalite` `exemple` `fin`. Repères : `ka` `log` `relation` `egalite` `exemple`.
- `?vue=domaines` — axe horizontal des pH 0 → 14 ; trait jaune à pKa = 4,8 ; à gauche « CH₃COOH prédomine » (rose), à droite « CH₃COO⁻ prédomine »
  (vert) ; « pH < pKa : AH ; pH > pKa : A⁻ ; pH = pKa : [AH] = [A⁻] ». Poignée `pH` (`set_parameters {pH}`, 0 → 14, défaut 3,41) : un curseur
  glisse sur l'axe ; deux barres [AH] et [A⁻] (proportions de l'exemple H) et le nom de l'espèce qui prédomine changent.
  Moments : `axe` `pka` `domaine_acide` `domaine_base` `regle` `fin`. Poignée `pH`.
  Repères : `axe_ph` `pka` `domaine_acide` `domaine_base` `regle` `poignee_ph`.
- `?vue=distribution` — exemple H : axes % (0 → 100) et pH (0 → 14) ; courbe rose « % CH₃COOH » (décroît) et courbe verte « % CH₃COO⁻ » (croît),
  points 2,8 · 3,8 · 4,8 · 5,8 · 6,8 ; croisement marqué « 50 % : pH = pKa = 4,8 » ; « diagramme de distribution ». Poignée `pH`
  (`set_parameters {pH}`, défaut 3,8) : deux points glissent, leurs % s'affichent (à 3,8 : 90,9 % et 9,1 %).
  Moments : `axes` `courbe_acide` `courbe_base` `croisement` `lecture` `phrase` `fin`. Poignée `pH`.
  Repères : `axe_pourcent` `axe_ph` `courbe_acide` `courbe_base` `croisement` `poignee_ph` `phrase`.
- `?vue=indicateur` — un flacon de BBT ; trois béchers de l'exemple B ; une goutte dans chacun : jaune (3,41), vert (7,00), bleu (10,60) ;
  à la craie « indicateur coloré : couple HInd/Ind⁻ ; HInd et Ind⁻ n'ont pas la même couleur » ; « BBT : HInd jaune, Ind⁻ bleu ».
  Moments : `flacon` `gouttes` `couleurs` `couple` `phrase` `fin`. Repères : `flacon` `becher_1` `becher_2` `becher_3` `couple` `phrase`.
- `?vue=virage` — axe des pH ; bande colorée du BBT : jaune jusqu'à 6,0, vert de 6,0 à 7,6 (« zone de virage »), bleu après ; pKa(BBT) ≈ 7,0
  marqué dans la zone ; « la zone de virage encadre le pKa de l'indicateur » ; tableau des quatre indicateurs de l'exemple I (bandes colorées
  posées sur le même axe).
  Moments : `axe` `bande` `zone` `pka` `tableau` `fin`. Repères : `axe` `bande` `zone` `pka` `tableau`.

## 6. dosage.html (vues montage | reaction | equivalence | courbe | tangentes | derivee)
- `?vue=montage` — montage peint : burette graduée (soude C_B = 1,0·10⁻² mol/L, « solution titrante ») sur potence ; bécher de V_A = 20,0 mL
  d'acide éthanoïque (« solution titrée ») ; barreau aimanté qui tourne sur l'agitateur ; sonde du pH-mètre (afficheur 3,41) ; étiquettes à la
  craie : « burette » « solution titrante » « solution titrée » « agitateur magnétique » « pH-mètre » ; « but : trouver C_A ».
  Moments : `burette` `becher` `agitateur` `ph_metre` `noms` `but` `fin`.
  Repères : `burette` `becher` `agitateur` `sonde` `afficheur` `noms` `but`.
- `?vue=reaction` — loupe : chaque HO⁻ qui tombe arrache un H⁺ à CH₃COOH ; « CH₃COOH + HO⁻ → CH₃COO⁻ + H₂O » (flèche simple) ; « K = 1,6·10⁹ » ;
  trois cases cochées à la craie : « rapide » « totale » « unique » ; « réaction de dosage ».
  Moments : `loupe` `equation` `constante` `rapide` `totale` `unique` `fin`.
  Repères : `loupe` `equation` `constante` `conditions`.
- `?vue=equivalence` — tableau d'avancement de la réaction de dosage (CH₃COOH · HO⁻ ; initial C_A·V_A · C_B·V_B) ; trois instantanés : avant
  (HO⁻ limitant), à l'équivalence (les deux épuisés), après (HO⁻ en excès) ; « équivalence : réactifs dans les proportions stœchiométriques » ;
  « n(CH₃COOH)_initial = n(HO⁻)_versé » ; « C_A·V_A = C_B·V_BE » (encadré) ; « V_BE = 1,0·10⁻² × 20,0/1,0·10⁻² = 20,0 mL ».
  Moments : `tableau` `avant` `a_equivalence` `apres` `definition` `relation` `application` `fin`.
  Repères : `tableau` `avant` `a_equivalence` `apres` `definition` `relation` `application`.
- `?vue=courbe` — exemple J : axes pH (0 → 14) et V_B (0 → 40 mL) ; la burette verse, l'afficheur et un point montent ensemble ; points de
  l'exemple J tracés à la craie bleu clair ; trois zones nommées : « pH monte doucement » · « saut de pH » · « pH presque constant ».
  Poignée `V_B` (`set_parameters {V_B}`, 0 → 40, défaut 0) : le point et l'afficheur suivent la courbe.
  Moments : `axes` `debut` `zone_1` `saut` `zone_3` `phrase` `fin`. Poignée `V_B`.
  Repères : `axe_ph` `axe_v` `courbe` `saut` `afficheur` `poignee_vb` `phrase`.
- `?vue=tangentes` — la courbe de l'exemple J ; deux tangentes parallèles (pointillés jaunes) de part et d'autre du saut ; leur parallèle
  équidistante (trait jaune plein) coupe la courbe en E ; lecture « V_BE = 20,0 mL ; pH_E = 8,3 » ; « méthode des tangentes parallèles ».
  Moments : `courbe` `tangente_1` `tangente_2` `mediane` `point_e` `lecture` `fin`.
  Repères : `courbe` `tangente_1` `tangente_2` `mediane` `point_e` `lecture`.
- `?vue=derivee` — sous la courbe, la courbe dérivée dpH/dV_B (orange clair) : presque nulle, puis un pic fin à 20,0 mL ; un trait vertical
  relie le pic au saut de la courbe ; « V_BE = abscisse du maximum de dpH/dV_B = 20,0 mL » ; national 2022 N, 2024 N.
  Moments : `courbe` `derivee` `pic` `lecture` `national` `fin`. Repères : `courbe` `derivee` `pic` `lecture` `national`.

## 7. exploiter.html (vues trois_courbes | demi | indicateur | base | conductimetrie | national_2023)
- `?vue=trois_courbes` — mêmes axes : courbe K (acide chlorhydrique, blanche), courbe J (acide éthanoïque, bleu clair) ; leurs points E :
  « pH_E = 7,0 » et « pH_E = 8,3 » ; « acide fort + base forte : pH_E = 7 » ; « acide faible + base forte : pH_E > 7 (la solution contient
  la base CH₃COO⁻) » ; puis la courbe L (ammoniac par l'acide chlorhydrique, verte, qui descend) : « base faible + acide fort : pH_E < 7 (5,7) ».
  Moments : `axes` `courbe_fort` `courbe_faible` `comparer` `courbe_base` `regle` `fin`.
  Repères : `axes` `courbe_fort` `courbe_faible` `point_e_fort` `point_e_faible` `courbe_base` `regle`.
- `?vue=demi` — courbe J ; V_BE/2 = 10,0 mL marqué ; tableau : « n(CH₃COOH) = n(CH₃COO⁻) = 1,0·10⁻⁴ mol » ; « [AH] = [A⁻] » ;
  « pH = pKa + log 1 » ; « pH = pKa à V_B = V_BE/2 » ; lecture « pH = 4,8 = pKa ».
  Moments : `courbe` `demi_volume` `tableau` `egalite` `relation` `lecture` `fin`.
  Repères : `courbe` `demi_volume` `tableau` `egalite` `relation` `lecture`.
- `?vue=indicateur` — courbe J ; les bandes des quatre indicateurs (exemple I) glissent sur l'axe des pH ; celle qui contient pH_E = 8,3 est
  entourée : « rouge de crésol (7,2 – 8,8) » ; ⚠ « BBT : vire avant le saut » ; « la zone de virage doit contenir pH_E » ; le bécher passe du
  jaune au rouge à la goutte de l'équivalence.
  Moments : `courbe` `bandes` `choix` `piege` `regle` `couleur` `fin`.
  Repères : `courbe` `bandes` `choix` `piege` `regle` `becher`.
- `?vue=base` — exemple L : bécher d'ammoniac (20,0 mL), burette d'acide chlorhydrique ; « NH₃ + H₃O⁺ → NH₄⁺ + H₂O » ;
  « C_B·V_B = C_A·V_AE » → « V_AE = 20,0 mL » ; la courbe descend (10,59 → 2,48) ; E (20,0 mL ; 5,7) ; demi-équivalence « pH = 9,2 = pKa(NH₄⁺/NH₃) » ;
  « indicateur : rouge de méthyle ».
  Moments : `montage` `equation` `relation` `courbe` `point_e` `demi` `indicateur` `fin`.
  Repères : `burette` `becher` `equation` `relation` `courbe` `point_e` `demi` `indicateur`.
- `?vue=conductimetrie` — exemple M : cellule conductimétrique dans l'acide chlorhydrique dilué ; afficheur 38,8 mS/m ; points σ = f(V_B) (0 → 4,0 mL)
  tracés un à un : une droite qui descend, puis une droite qui monte ; loupe : H₃O⁺ remplacé par Na⁺ (avant), Na⁺ et HO⁻ ajoutés (après) ;
  « équivalence : rupture de pente » ; intersection des deux droites « V_BE = 2,0 mL » ; « C_A = C_B·V_BE/V_A = 1,0·10⁻² mol/L ».
  Moments : `cellule` `points` `droite_1` `droite_2` `loupe` `intersection` `calcul` `fin`.
  Repères : `cellule` `afficheur` `droite_1` `droite_2` `loupe` `intersection` `calcul`.
- `?vue=national_2023` — national 2023 R (2.3-2.8, 3,25 pts) : triméthylamine V_B = 20 mL (urine diluée 10 fois), acide chlorhydrique
  C_A = 4·10⁻² mol/L ; courbe calculée (pKa 9,9) avec Q (10 mL ; 9,9) et E (20 mL ; 5,8) marqués ; « C_B = C_A·V_AE/V_B = 4·10⁻² mol/L » ;
  « C₀ = 10·C_B = 0,4 mol/L » ; « pH_E < 7 : l'acide (CH₃)₃NH⁺ est présent » ; « rouge de méthyle (4,2 – 6,2) » ; « V_A = V_AE/2 :
  [(CH₃)₃NH⁺] = [(CH₃)₃N] → pKa = 9,9 ».
  Moments : `donnees` `courbe` `concentration` `nature` `indicateur` `demi` `pka` `fin`.
  Repères : `donnees` `courbe` `point_q` `point_e` `concentration` `indicateur` `pka`.

## 8. figures.html (?fig=…) — figures des nationaux
Écrites d'après `outils/cours/notes/cours/acides_bases_build/nationaux.md` (section « Figures pour figures.html ») : une figure par clé
`fig_<session>`, dessinée comme le sujet (axes, graduations, unités, quadrillage léger, courbe, points marqués). Pour chaque figure, moments :
`axes` `courbe` `construction` `lecture` `calcul` `fin` ; repères : `axe_x` `axe_y` `courbe` `construction` `point` `valeur` `calcul`.
- `fig_2025R` (p4) — distribution CH₃COOH / CH₃COO⁻ (pH 0 → 14, % 0 → 100) ; courbe 1 (acide) et courbe 2 (base) ; `construction` : trait à 50 % ;
  `lecture` : « croisement : pH = pKa = 4,8 » et « courbe 1 > 50 % pour pH < pKa : forme acide » ; `calcul` : « pH₁ = 4,2 : 20 % de CH₃COO⁻ →
  τ₁ = 0,20 ».
- `fig_2016N` (n1) — dosage de l'acide propanoïque (V_B 0 → 12 mL, pH 3 → 12) ; `construction` : deux tangentes parallèles et leur parallèle
  équidistante ; `lecture` : « E (6 mL ; 8,7) » ; `calcul` : « C_A = C_B·V_BE/V_A = 5·10⁻² × 6/5 = 6·10⁻² mol/L » et « bleu de thymol (8 – 9,6) ».
- `fig_2022R` (n2) — dosage de la méthylamine par l'acide chlorhydrique (V_a 0 → 24 mL, pH 0 → 14) ; `construction` : tangentes ;
  `lecture` : « E (15 mL ; 6,6) » ; `calcul` : « C_b = C_a·V_aE/V_b = 10⁻² mol/L » et « BBT (6,0 – 7,6) ».
- `fig_2022N` (n3) — dosage de l'acide propanoïque avec dpH/dV_b (V_b 0 → 30 mL, pH 0 → 14) ; `construction` : pic de la dérivée ;
  `lecture` : « V_bE = 20 mL » et « V_b = 5 mL : pH = 4,4 » ; `calcul` : « [A⁻]/[AH] = 10^(4,4 − 4,9) = 0,316 → 76 % de forme acide ».
- `fig_2024R` (n4) — distribution R–NH₃⁺ / R–NH₂ (pH 0 → 14, % 0 → 100) ; `construction` : trait à 50 % ; `lecture` : « pKa = 10,8 » et
  « pH = 11,88 > pKa : R–NH₂ prédomine » ; `calcul` : « 80 % d'acide : [base]/[acide] = 0,25 → pH = 10,8 + log 0,25 = 10,2 ».

## 9. bilan.html et carte.html (modèle : chimie/etat-equilibre-tableau/bilan.html, carte.html)
- bilan.html — fiche, blocs (moments) : `fiche` `eau` `base` `acidite` `comparer` `reaction` `predominance` `dosage` `exploiter` `redaction` `lacunes` `fin` ;
  repères : un par bloc (mêmes noms sans `lacunes`) + `fiche`. Page 2 de l'élève (lacunes, acquis, acquis_ids par `set_parameters`), comme le modèle.
  Compétences → blocs : C1 eau, C2 base, C3 acidite, C4 comparer, C5 reaction, C6 predominance, C7 dosage, C8 exploiter, C9 redaction.
  Contenu : eau (2H₂O ⇌ H₃O⁺ + HO⁻ ; Ke = [H₃O⁺]·[HO⁻] = 1,0·10⁻¹⁴ à 25 °C ; pKe = 14 ; acide / neutre / basique) ; base ([HO⁻] = Ke/[H₃O⁺] ;
  τ = [HO⁻]_éq/C) ; acidite (Ka = [A⁻]_éq·[H₃O⁺]_éq/[AH]_éq ; pKa = −log Ka ; Ka = Ke/Qr,éq pour la réaction d'une base ; pKa 0 et 14 pour l'eau) ;
  comparer (même C : Ka grand → τ grand, pH petit ; pKa grand → base forte) ; reaction (K = Ka₁/Ka₂ = 10^(pKa₂ − pKa₁) ; K = Ka/Ke) ;
  predominance (pH = pKa + log([A⁻]_éq/[AH]_éq) ; pH < pKa : AH ; pH > pKa : A⁻ ; indicateur : zone de virage) ; dosage (rapide, totale, unique ;
  C_A·V_A = C_B·V_BE ; tangentes, dérivée) ; exploiter (pH_E = 7, > 7, < 7 ; pH = pKa à V_B = V_BE/2 ; indicateur dont la zone contient pH_E) ;
  redaction (équation → ; relation littérale ; application numérique ; unité ; lecture graphique justifiée).
- carte.html — moments : `centre` `rappel` `eau` `base` `acidite` `comparer` `reaction` `predominance` `indicateur` `dosage` `exploiter` `national` `suite` `complete` `fin` ;
  repères : `centre` + un par branche (sans `complete`). Centre : « couple AH/A⁻ : Ka, pKa ; dosage : C_A·V_A = C_B·V_BE ». `suite` = « semestre 2 :
  piles, électrolyse, estérification ».

## Diapositives servies (cours)
o1 carte
o2 eau?vue=ouverture
r1 eau?vue=rappel
r2 base?vue=constante
w1 eau?vue=autoprotolyse
w2 eau?vue=ke
w3 eau?vue=solutions
w4 eau?vue=ho
w5 eau?vue=soude
b1 base?vue=ammoniac
b2 base?vue=taux
b3 base?vue=national
a1 acidite?vue=definition
a2 acidite?vue=pka
a3 acidite?vue=mesure
a4 acidite?vue=ammonium
a5 acidite?vue=eau
c1 comparer?vue=acides
c2 comparer?vue=bases
c3 comparer?vue=classement
k1 comparer?vue=reaction
k2 comparer?vue=puissance
k3 comparer?vue=totale
k4 comparer?vue=national
p1 predominance?vue=relation
p2 predominance?vue=domaines
p3 predominance?vue=distribution
p4 figures?fig=fig_2025R
i1 predominance?vue=indicateur
i2 predominance?vue=virage
d1 dosage?vue=montage
d2 dosage?vue=reaction
d3 dosage?vue=equivalence
d4 dosage?vue=courbe
d5 dosage?vue=tangentes
d6 dosage?vue=derivee
e1 exploiter?vue=trois_courbes
e2 exploiter?vue=demi
e3 exploiter?vue=indicateur
e4 exploiter?vue=base
e5 exploiter?vue=conductimetrie
n1 figures?fig=fig_2016N
n2 figures?fig=fig_2022R
n3 figures?fig=fig_2022N
n4 figures?fig=fig_2024R
n5 exploiter?vue=national_2023
bl bilan
cr carte
