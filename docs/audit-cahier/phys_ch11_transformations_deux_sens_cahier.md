# Cahier de l'élève — Transformations chimiques s'effectuant dans les deux sens (phys_ch11)

18 novembre 2026. Le cahier idéal du chapitre, d'un seul tenant (ordre des blocs de la copie en attente ; le cours en
ligne diffère seulement au VIII, voir la table). Chaque ligne ci-dessous est une ligne d'un bloc : lus à la suite, les
blocs redonnent ce texte. Les titres I. à IX. ne sont pas dans `blocs[].cahier` : l'écran les affiche
déjà (titres des activités, `planDuCahier`), au bloc qui contient la première diapo de la partie. Script de découpage : `scratchpad/phys_ch11_transformations_deux_sens/cahier.py`.


## Ouverture et rappels

- Constat : deux acides de même C = 1,0·10⁻² mol/L n'ont pas le même pH.
- Acide éthanoïque : pH = 3,4 ; acide chlorhydrique : pH = 2,0. Pourquoi ?
- Rappel : ion = atome (ou groupe d'atomes) qui a perdu ou gagné des électrons.
- Ex. : Na⁺ (1 e⁻ perdu), Cl⁻ (1 e⁻ gagné) ; H⁺ = un proton. Les ions portent le courant.
- Rappel : solution aqueuse = soluté dissous dans l'eau ; C = n/V (mol/L) ; n = C·V.
- Rappel : 10⁻² = 0,01 ; 10⁻³ = 0,001 ; log(10ⁿ) = n ; y = 10ˣ ⇔ x = log y.
- log(a·b) = log a + log b ; log(a/b) = log a − log b ; log 1 = 0 ; log 10 = 1.

## I. Acides et bases selon Brønsted

- 1. Définition : un acide est une espèce chimique capable de céder un proton H⁺.
- Ex. : CH₃COOH(aq) → CH₃COO⁻(aq) + H⁺(aq).
- 2. Définition : une base est une espèce chimique capable de capter un proton H⁺.
- Ex. : NH₃(aq) + H⁺(aq) → NH₄⁺(aq).
- 3. Couple acide/base AH/A⁻ ; demi-équation : AH(aq) ⇌ A⁻(aq) + H⁺(aq).
- Ex. : CH₃COOH/CH₃COO⁻ ; NH₄⁺/NH₃ (⇌ : le proton peut être cédé ou repris).
- 4. L'eau est un ampholyte : base dans H₃O⁺/H₂O, acide dans H₂O/HO⁻.
- Définition : ampholyte = espèce qui est l'acide d'un couple et la base d'un autre.
- 5. Réaction acido-basique : H⁺ passe de l'acide d'un couple à la base d'un autre couple.
- Ex. : CH₃COOH(aq) + NH₃(aq) → CH₃COO⁻(aq) + NH₄⁺(aq).
- *Dessin* : Le proton passe d'un couple à l'autre — schéma : CH₃COOH cède H⁺ (rose) à NH₃ ; CH₃COO⁻ et NH₄⁺ se forment.

## II. pH d'une solution aqueuse

- 1. Définition : pH = −log[H₃O⁺] ([H₃O⁺] en mol/L ; le pH n'a pas d'unité).
- Condition : solution diluée, [H₃O⁺] ≤ 5·10⁻² mol/L. [H₃O⁺] plus grande → pH plus petit.
- 2. [H₃O⁺] = 10^(−pH). Ex. : pH = 3,4 → [H₃O⁺] = 4,0·10⁻⁴ mol/L (attention au signe −).
- 3. Mesure : étalonner le pH-mètre (pH 4,0 puis 7,0) ; rincer la sonde à l'eau distillée.

## III. Réaction d'un acide avec l'eau

- 1. AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq) : l'eau joue le rôle de base.
- Ex. A : CH₃COOH(aq) + H₂O(l) ⇌ CH₃COO⁻(aq) + H₃O⁺(aq) ; C = 1,0·10⁻² mol/L.
- 2. Base : B(aq) + H₂O(l) ⇌ BH⁺(aq) + HO⁻(aq). Attention : il se forme HO⁻, pas H₃O⁺.
- 3. Si elle était totale : [H₃O⁺] = C, pH = 2,0 ; mesuré 3,4 > 2,0 : elle n'est pas totale.

## IV. Taux d'avancement final

- 1. Tableau (mol), ex. A : initial C·V | excès | 0 | 0 ; en cours C·V − x | excès | x | x
- final C·V − x_f | excès | x_f | x_f ; donc n(H₃O⁺)_f = x_f. Ex. A : V = 0,100 L.
- 2. x_max = C·V (si totale ; eau en excès, acide limitant). Ex. A : x_max = 1,0·10⁻³ mol.
- 3. x_f = [H₃O⁺]_f·V = 10^(−pH)·V (mesuré). Ex. A : x_f = 4,0·10⁻⁵ mol < x_max.
- 4. Définition : τ = x_f/x_max (sans unité, 0 ≤ τ ≤ 1). Ex. A : τ = 0,040 = 4,0 %.

Tableau d'avancement modèle (quantités en mol ; ex. A : C = 1,0·10⁻² mol/L, V = 0,100 L) :

| Équation | CH₃COOH(aq) | + H₂O(l) | ⇌ CH₃COO⁻(aq) | + H₃O⁺(aq) |
|---|---|---|---|---|
| État initial (x = 0) | C·V | excès | 0 | 0 |
| En cours (x) | C·V − x | excès | x | x |
| État final (x_f) | C·V − x_f | excès | x_f | x_f |

- Totale : un réactif disparaît, x_f = x_max, τ = 1 (→). Limitée : x_f < x_max, τ < 1 (⇌).
- 5. Ex. B : HCl(g) + H₂O(l) → Cl⁻(aq) + H₃O⁺(aq), pH = 2,0 : x_f = x_max, τ = 1 : totale.
- 6. Montrer que τ = 10^(−pH)/C : τ = x_f/x_max = [H₃O⁺]_f·V/(C·V) = 10^(−pH)/C.

## V. Transformations dans les deux sens, état d'équilibre

- 1. Ajout d'ions éthanoate : le pH monte (2,3 → 3,6), H₃O⁺ consommé : sens inverse (2).
- Sens inverse : CH₃COO⁻(aq) + H₃O⁺(aq) → CH₃COOH(aq) + H₂O(l).
- Ajout d'acide éthanoïque pur : le pH baisse : sens direct (1). Donc deux sens : ⇌.
- 2. Définition : à l'état d'équilibre, les quantités ne changent plus ; tout coexiste.
- Réaction limitée : état final = état d'équilibre : x_f = x_éq et [X]_f = [X]_éq.
- 3. Équilibre dynamique : les deux sens continuent, à la même vitesse : v₁ = v₂.
- *Dessin* : Équilibre dynamique : v₁ = v₂ — v₁(t) décroît, v₂(t) croît, même valeur non nulle à l'équilibre (allure).
- Remarque : autant de chocs efficaces par unité de temps dans chaque sens.
- 4. 2016 N (estérification) : τ = 0,33/0,5 = 0,66 < 1 : lente et limitée.
- Méthode 2017 N : x_f lu sur le palier ; τ₁ = 0,2/0,3 = 0,67 (limitée) ; τ₂ = 1 (totale).
- *Dessin* : Totale ou limitée ? — x(t) de 2017 N : paliers 0,2 mol (τ₁ = 0,67) et 0,3 mol = x_max (τ₂ = 1).

## VI. Conductimétrie : trouver τ

- 1. σ (S/m) vient des ions. Même C : acide éthanoïque 15,6 mS/m ≪ HCl 426 mS/m.
- 2. σ = Σ λᵢ·[Xᵢ] ; AH + eau (HO⁻ négligés) : σ = (λ₁ + λ₂)·[H₃O⁺], λ₁ = λ(H₃O⁺).
- Car [A⁻] = [H₃O⁺] = x_f/V. Unités : σ en S/m, λ en S·m²·mol⁻¹, [X] en mol/m³.
- Méthode : 1) [H₃O⁺] = σ/(λ₁ + λ₂) ; 2) 1 mol/m³ = 10⁻³ mol/L ; 3) τ = [H₃O⁺]/C.
- Ex. A : [H₃O⁺] = 1,56·10⁻²/(39,09·10⁻³) = 0,399 mol/m³ = 3,99·10⁻⁴ mol/L ; τ = 0,040.

## VII. Dilution et nature de l'acide

- 1. Rappel : diluer ne change pas n : C₀·V₀ = C₁·V₁ ; facteur F = V₁/V₀ = C₀/C₁.
- Ex. : 10 mL (pipette) dans une fiole jaugée de 100 mL, complétée d'eau distillée : F = 10.
- 2. Acide éthanoïque, C (mol/L) : 1,0·10⁻² ; 1,0·10⁻³ ; 1,0·10⁻⁴ → pH : 3,4 ; 3,9 ; 4,5.
- Plus la solution est diluée, plus le pH est grand (moins d'ions H₃O⁺ par litre).
- 3. τ = 10^(−pH)/C : 0,040 ; 0,13 ; 0,32 : plus la solution est diluée, plus τ est grand.
- *Dessin* : La dilution augmente τ — barres τ = 0,040 ; 0,13 ; 0,32 pour C = 10⁻² ; 10⁻³ ; 10⁻⁴ mol/L.
- 4. Même C = 1,0·10⁻² mol/L : τ = 1 (HCl), 0,13 (méthanoïque), 0,040 (éthanoïque).
- Donc, à même concentration, τ dépend de la nature de l'acide.
- 2019 N (σ) : τ = σ/(C·(λ₁ + λ₂)) = 8,6·10⁻³/(1,0 × 38,23·10⁻³) = 0,22 < 1 : limitée.
- Attention : λ en S·m²·mol⁻¹, donc C = 1,0·10⁻³ mol/L = 1,0 mol/m³.

## VIII. Sujets du national

- 1. 2021 R : acide méthanoïque, C_a = 1,0·10⁻¹ mol/L, pH = 2,38.
- Q5 : pH si totale = 1,0 < 2,38 : limitée ; HCOOH(aq) + H₂O(l) ⇌ HCOO⁻(aq) + H₃O⁺(aq).
- Q9 : x_max = C·V (eau en excès) ; x_f = 10^(−pH)·V ; τ = 10^(−pH)/C = 0,042.
- Q10 : lire τ sur la courbe (axe de 0 à 1) : pH 2,8 → τ₁ ≈ 0,10 ; pH 3,6 → τ₂ ≈ 0,45.
- *Dessin* : τ en fonction du pH (2021 R) — lectures pH 2,8 → 0,10 et pH 3,6 → 0,45 (courbe passant par ces deux points).
- Q11 : C = 10^(−pH)/τ : C₁ = 1,58·10⁻² mol/L ; C₂ = 5,58·10⁻⁴ mol/L.
- Conclusion : C₂ < C₁ et τ₂ > τ₁ : la dilution augmente τ.
- 2. 2023 N : [CH₃COO⁻] = C_A·τ ; [CH₃COOH] = C_A(1 − τ) ; α = 1 − τ = 0,982.
- 3. 2024 R (dosage) : x_f = C_A·V_A − 10^(−pH)·(V_A + V_B) ≈ C_A·V_A = x_max : τ = 1.
- Attention : [H₃O⁺]_f = 10^(−pH) dans le volume du mélange V_A + V_B.
- Remarque : une réaction de dosage est totale (τ = 1) : flèche simple →.

## IX. Bilan du chapitre

- Méthode : 1) équation avec l'eau (⇌) ; 2) tableau ; 3) x_max et x_f ; 4) τ = x_f/x_max ;
- 5) application numérique avec unités ; 6) conclure : « τ < 1 : la réaction est limitée ».

---

## Table de découpage


### Copie en attente (`en_attente/phys_ch11_transformations_deux_sens.json`)

| Bloc | Diapos | Lignes du bloc | Figures du bloc |
|---|---|---|---|
| `td_r_b1` | `td_o1_carte`, `td_o2_flacons`, `td_z1_ion` | 4 (« Constat : deux acides de même C = 1,0·… ») | — |
| `td_r_b2` | `td_z2_concentration`, `td_z3_puissance`, `td_b1_acide` | 5 (« Rappel : solution aqueuse = soluté dis… ») | — |
| `td_s1_b1` | `td_b2_base`, `td_b3_couple`, `td_b3b_eau` | 6 (« 2. Définition : une base est une espèc… ») | — |
| `td_s1_b2` | `td_b4_reaction`, `td_p1_ph`, `td_p2_calcul` | 5 (« 5. Réaction acido-basique : H⁺ passe d… ») | Le proton passe d'un couple à l'autre |
| `td_s1_b3` | `td_p3_phmetre`, `td_p4_eau`, `td_p5_ammoniac`, `td_p6_totale` | 5 (« 3. Mesure : étalonner le pH-mètre (pH … ») | — |
| `td_s2_b1` | `td_a1_tableau`, `td_a2_xmax`, `td_a3_xf`, `td_a4_taux` | 5 (« 1. Tableau (mol), ex. A : initial C·V … ») | — |
| `td_s2_b2` | `td_a5_totale`, `td_a6_relation`, `td_e1_inverse`, `td_e1b_direct`, `td_e2_fleche` | 6 (« Totale : un réactif disparaît, x_f = x… ») | — |
| `td_s2_b3` | `td_e3_etat`, `td_e4_dynamique`, `td_e5_esterification`, `td_e6_national` | 6 (« 2. Définition : à l'état d'équilibre, … ») | Équilibre dynamique : v₁ = v₂ ; Totale ou limitée ? |
| `td_s3_b1` | `td_c1_ions`, `td_c2_relation`, `td_c3_calcul` | 5 (« 1. σ (S/m) vient des ions. Même C : ac… ») | — |
| `td_d_b1` | `td_z4_dilution`, `td_d1_dilution`, `td_d1b_mesures` | 4 (« 1. Rappel : diluer ne change pas n : C… ») | — |
| `td_s3_b2` | `td_d2_taux`, `td_d3_nature`, `td_n2_conductivite` | 5 (« 3. τ = 10^(−pH)/C : 0,040 ; 0,13 ; 0,3… ») | La dilution augmente τ |
| `td_n_b1` | `td_n1a_equation`, `td_n1b_montrer`, `td_n1c_courbe`, `td_n1d_dilution` | 6 (« 1. 2021 R : acide méthanoïque, C_a = 1… ») | τ en fonction du pH (2021 R) |
| `td_s3_b3` | `td_n3_proportion`, `td_n4_dosage`, `td_n4b_calcul`, `td_bl_fiche`, `td_cr_carte` | 6 (« 2. 2023 N : [CH₃COO⁻] = C_A·τ ; [CH₃CO… ») | — |

Diapo → bulle (`concentration.cahier`, une chaîne d'1 ou 2 phrases ; figure entre crochets) :

- `td_o1_carte` : Plan : Brønsted → pH → acide + eau → τ = x_f/x_max → deux sens (⇌) → équilibre → σ → dilution.
- `td_o2_flacons` : Même C = 1,0·10⁻² mol/L : acide éthanoïque pH = 3,4 ; acide chlorhydrique pH = 2,0. Pourquoi ?
- `td_z1_ion` : Ion : atome (ou groupe d'atomes) qui a perdu ou gagné des électrons. H⁺ = un proton seul.
- `td_z2_concentration` : Solution aqueuse : soluté dissous dans l'eau (le solvant). C = n/V (mol/L) ; n = C·V.
- `td_z3_puissance` : 10⁻³ = 0,001 ; 4,0·10⁻⁴ = 0,00040. log(10ⁿ) = n ; y = 10ˣ ⇔ x = log y.
- `td_b1_acide` : Acide (Brønsted) : espèce chimique capable de céder un proton H⁺. CH₃COOH(aq) → CH₃COO⁻(aq) + H⁺(aq).
- `td_b2_base` : Base (Brønsted) : espèce chimique capable de capter un proton H⁺. NH₃(aq) + H⁺(aq) → NH₄⁺(aq).
- `td_b3_couple` : Couple AH/A⁻ : AH(aq) ⇌ A⁻(aq) + H⁺(aq). Ex. : CH₃COOH/CH₃COO⁻ ; NH₄⁺/NH₃.
- `td_b3b_eau` : L'eau est un ampholyte : base dans H₃O⁺/H₂O, acide dans H₂O/HO⁻.
- `td_b4_reaction` : Réaction acido-basique : H⁺ passe de l'acide d'un couple à la base d'un autre. CH₃COOH(aq) + NH₃(aq) → CH₃COO⁻(aq) + NH₄⁺(aq). [Le proton passe d'un couple à l'autre]
- `td_p1_ph` : pH = −log[H₃O⁺] ([H₃O⁺] en mol/L ; solution diluée, [H₃O⁺] ≤ 5·10⁻² mol/L). Ex. : [H₃O⁺] = 1,0·10⁻² mol/L → pH = 2,0.
- `td_p2_calcul` : [H₃O⁺] = 10^(−pH). pH = 3,4 → [H₃O⁺] = 4,0·10⁻⁴ mol/L (attention au signe −).
- `td_p3_phmetre` : pH-mètre : étalonner (pH 4,0 puis 7,0), rincer la sonde à l'eau distillée, lire à 0,1 près. Papier pH : moins précis.
- `td_p4_eau` : AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq) (l'eau = base). Ex. A : CH₃COOH(aq) + H₂O(l) ⇌ CH₃COO⁻(aq) + H₃O⁺(aq).
- `td_p5_ammoniac` : B(aq) + H₂O(l) ⇌ BH⁺(aq) + HO⁻(aq) (l'eau = acide). Ex. : NH₃(aq) + H₂O(l) ⇌ NH₄⁺(aq) + HO⁻(aq).
- `td_p6_totale` : Si la réaction était totale : [H₃O⁺] = C, pH = 2,0. Mesuré : 3,4 > 2,0 : la réaction n'est pas totale.
- `td_a1_tableau` : Tableau (mol) : initial C·V | excès | 0 | 0 ; en cours C·V − x | excès | x | x ; final C·V − x_f | excès | x_f | x_f.
- `td_a2_xmax` : x_max = C·V (l'eau en excès : l'acide est le réactif limitant). Ex. A : x_max = 1,0·10⁻² × 0,100 = 1,0·10⁻³ mol.
- `td_a3_xf` : x_f = [H₃O⁺]_f·V = 10^(−pH)·V. Ex. A : x_f = 4,0·10⁻⁴ × 0,100 = 4,0·10⁻⁵ mol < x_max.
- `td_a4_taux` : τ = x_f/x_max (sans unité, 0 ≤ τ ≤ 1). Ex. A : τ = 4,0·10⁻⁵/1,0·10⁻³ = 0,040 < 1 : réaction limitée.
- `td_a5_totale` : Ex. B : HCl(g) + H₂O(l) → Cl⁻(aq) + H₃O⁺(aq) ; x_f = x_max = 1,0·10⁻³ mol, τ = 1 : réaction totale (→).
- `td_a6_relation` : τ = x_f/x_max = [H₃O⁺]_f·V/(C·V) = 10^(−pH)/C. Ex. A : τ = 10^(−3,4)/1,0·10⁻² = 0,040.
- `td_e1_inverse` : Éthanoate de sodium ajouté : le pH monte (2,3 → 3,6). CH₃COO⁻(aq) + H₃O⁺(aq) → CH₃COOH(aq) + H₂O(l) : sens inverse (2).
- `td_e1b_direct` : Acide éthanoïque pur ajouté : le pH baisse, des ions H₃O⁺ se forment : sens direct (1), de gauche à droite.
- `td_e2_fleche` : Réaction limitée (τ < 1) : deux sens, double flèche ⇌ ; réaction totale (τ = 1) : flèche simple →.
- `td_e3_etat` : État d'équilibre : quantités constantes, réactifs et produits présents. Ex. A : n(CH₃COOH)_éq = 9,6·10⁻⁴ mol ; n(H₃O⁺)_éq = 4,0·10⁻⁵ mol.
- `td_e4_dynamique` : Équilibre dynamique : les deux sens continuent à la même vitesse (v₁ = v₂), donc les quantités ne changent plus. [Équilibre dynamique : v₁ = v₂]
- `td_e5_esterification` : 2016 N : x_max = 0,5 mol, x_f = 0,33 mol ; τ = 0,66 < 1 : l'estérification est lente et limitée.
- `td_e6_national` : 2017 N : x_f se lit sur le palier ; τ₁ = 0,2/0,3 = 0,67 < 1 (limitée) ; τ₂ = 0,3/0,3 = 1 (totale). [Totale ou limitée ?]
- `td_c1_ions` : σ (S/m) est due aux ions. Même C = 1,0·10⁻² mol/L : acide éthanoïque 15,6 mS/m ; acide chlorhydrique 426 mS/m.
- `td_c2_relation` : σ = Σ λᵢ·[Xᵢ] ; [A⁻] = [H₃O⁺] = x_f/V, donc σ = (λ₁ + λ₂)·[H₃O⁺] ([X] en mol/m³).
- `td_c3_calcul` : [H₃O⁺] = σ/(λ₁ + λ₂) = 0,399 mol/m³ = 3,99·10⁻⁴ mol/L ; τ = [H₃O⁺]/C = 0,040 < 1.
- `td_z4_dilution` : Dilution : la quantité de soluté se conserve : C₀·V₀ = C₁·V₁ ; facteur F = V₁/V₀ = C₀/C₁.
- `td_d1_dilution` : Dilué 10 fois : C = 1,0·10⁻² → 1,0·10⁻³ mol/L ; le pH passe de 3,4 à 3,9.
- `td_d1b_mesures` : C = 1,0·10⁻⁴ mol/L : pH = 4,5. Plus la solution est diluée, plus le pH est grand.
- `td_d2_taux` : τ = 10^(−pH)/C : 0,040 ; 0,13 ; 0,32 pour C = 1,0·10⁻² ; 1,0·10⁻³ ; 1,0·10⁻⁴ mol/L : la dilution augmente τ. [La dilution augmente τ]
- `td_d3_nature` : Même C = 1,0·10⁻² mol/L : τ = 1 (HCl) ; 0,13 (acide méthanoïque) ; 0,040 (acide éthanoïque) : τ dépend de l'acide.
- `td_n1a_equation` : 2021 R, Q5 : pH = 2,38 > 1,0 (pH si totale) : limitée ; HCOOH(aq) + H₂O(l) ⇌ HCOO⁻(aq) + H₃O⁺(aq).
- `td_n1b_montrer` : Q9 : x_max = C·V ; x_f = 10^(−pH)·V ; τ = x_f/x_max = 10^(−pH)/C. S_a : τ = 0,042 < 1.
- `td_n1c_courbe` : Q10 : pH 2,8 → τ₁ ≈ 0,10 ; pH 3,6 → τ₂ ≈ 0,45 (axe de τ de 0 à 1, pas en %). [τ en fonction du pH (2021 R)]
- `td_n1d_dilution` : Q11 : C = 10^(−pH)/τ ; C₁ = 1,58·10⁻² mol/L, C₂ = 5,58·10⁻⁴ mol/L : la dilution augmente τ.
- `td_n2_conductivite` : 2019 N : τ = σ/(C·(λ₁ + λ₂)) avec C = 1,0·10⁻³ mol/L = 1,0 mol/m³ ; τ = 0,22 < 1 : réaction limitée.
- `td_n3_proportion` : 2023 N : [CH₃COOH] = C_A(1 − τ), [CH₃COO⁻] = C_A·τ, donc α = 1 − τ ; τ = 0,0178, α = 0,982.
- `td_n4_dosage` : 2024 R : R–NH₂(aq) + H₃O⁺(aq) → R–NH₃⁺(aq) + H₂O(l) ; x_f = C_A·V_A − 10^(−pH)·(V_A + V_B).
- `td_n4b_calcul` : x_max = C_A·V_A = 7,2·10⁻⁴ mol ; H₃O⁺ restant 1,6·10⁻¹² mol, négligeable : x_f = x_max, τ = 1 : dosage total.
- `td_bl_fiche` : pH = −log[H₃O⁺] ; τ = x_f/x_max = 10^(−pH)/C ; τ < 1 : limitée (⇌), équilibre dynamique ; σ = (λ₁ + λ₂)·[H₃O⁺].
- `td_cr_carte` : Réaction limitée (τ < 1) : deux sens (⇌), état d'équilibre dynamique ; la dilution augmente τ.

### Cours en ligne (`phys_ch11_transformations_deux_sens.json`)

Mêmes blocs et mêmes bulles que la copie en attente, sauf : pas de bloc `td_n_b1` ; le bloc `td_s3_b2` porte
`td_d2_taux`, `td_d3_nature`, `td_n1_figure`, `td_n2_conductivite` et ses lignes (titre VIII affiché par l'écran) deviennent :

- 3. τ = 10^(−pH)/C : 0,040 ; 0,13 ; 0,32 : plus la solution est diluée, plus τ est grand.
- 4. À même C, τ dépend de l'acide : HCl 1 ; méthanoïque 0,13 ; éthanoïque 0,040.
- 1. 2021 R : τ lu sur τ(pH) ; C = 10^(−pH)/τ : C₁ = 1,58·10⁻², C₂ = 5,58·10⁻⁴ mol/L.
- C₂ < C₁ et τ₂ > τ₁ : la dilution augmente τ.
- 2019 N (σ) : τ = σ/(C·(λ₁ + λ₂)) avec C en mol/m³ : τ = 0,22 < 1 : limitée.

Figures du bloc : La dilution augmente τ ; τ en fonction du pH (2021 R). Bulle de `td_n1_figure` : 2021 R : τ lu sur la courbe (pH 2,8 → 0,10 ; pH 3,6 → 0,45) ; C = 10^(−pH)/τ : la dilution augmente τ. [τ en fonction du pH (2021 R)]

Dans les deux versions, le VIII s'ouvre là où l'écran l'affiche (bloc de `td_n1a_equation` en attente, de
`td_n1_figure` en ligne) : 1. 2021 R, 2. 2023 N, 3. 2024 R ; 2019 N, joué juste avant (en attente) ou après 2021 R
(en ligne), est écrit sans numéro (« 2019 N (σ) : … »). Numérotation romaine : celle des titres d'activités, identique
dans les deux versions (Ouverture sans numéro, puis I. à IX.).
