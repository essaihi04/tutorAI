# Cahier de l'élève — Transformations associées aux réactions acido-basiques (`phys_ch13_acides_bases`)

18 novembre 2026. Cahier idéal du chapitre, d'un seul tenant, dans l'ordre de la version **en attente** (`backend/data/courses/en_attente/phys_ch13_acides_bases.json`, 7 séances, 21 blocs). C'est exactement le texte des `blocs[].cahier` lus à la suite ; la version en ligne reprend les mêmes lignes dans son propre ordre et sa propre numérotation (voir la table de découpage). Méthode : skill `cahier-de-l-eleve`. Environ 100 lignes, 12 dessins : 3 à 4 pages de cahier.

Les titres de partie (## ci-dessous) sont les `activities[].title` du cours : l'écran du cahier les affiche lui-même quand un bloc entre dans la partie ; ils ne sont donc pas écrits dans `blocs[].cahier`. Les sous-titres 1., 2., 3. se suivent d'un bloc à l'autre dans chaque partie. Les blocs `ab_b19` et `ab_b20` (2018 N) ont une ligne par diapo, dans l'ordre (l'écran range chaque ligne sous sa diapo) ; ailleurs, nombre de lignes ≠ nombre de diapos.

Notations : [X]éq en mol/L ; Ke, Ka, K, Qr sans unité ; V en mL ou L (la même unité des deux côtés de C_A·V_A = C_B·V_BE) ; valeurs à 25 °C sauf mention.

<!-- bloc ab_b01 -->

## Les outils depuis zéro : log, acide, base, couple, pH

1. Puissances de dix : 10⁻³ = 0,001 ; 4,0·10⁻⁴ = 0,00040 ; log(10ⁿ) = n.  
Pour a, b > 0 : log(a·b) = log a + log b ; log(a/b) = log a − log b ; log(a²) = 2·log a.  
2. Définition : un acide est une espèce chimique capable de céder un proton H⁺ ;  
une base est capable de capter un proton H⁺. Couple AH/A⁻ : AH(aq) ⇌ A⁻(aq) + H⁺(aq).  
3. L'eau : couples H₃O⁺/H₂O et H₂O/HO⁻. pH = −log[H₃O⁺] ; [H₃O⁺] = 10^(−pH) en mol/L.  

<!-- bloc ab_b02 -->

## I. L'autoprotolyse de l'eau et le produit ionique Ke

1. Constat : eau pure pH = 7,00 ; vinaigre dilué 3,41 ; ammoniac dilué 10,60.  
2. Définition : l'autoprotolyse de l'eau est la réaction entre deux molécules d'eau :  
2H₂O(l) ⇌ H₃O⁺(aq) + HO⁻(aq) ; eau pure à 25 °C : [H₃O⁺] = [HO⁻] = 1,0·10⁻⁷ mol/L.  
3. Pour 1,0 L : n₀ = ρ·V/M = 55,6 mol ; x_max = n₀/2 = 27,8 mol ; x_éq = 1,0·10⁻⁷ mol.  
τ = x_éq/x_max = 3,6·10⁻⁹ ≪ 1 : très limitée (l'eau pure conduit à peine le courant).  
*Dessin — L'autoprotolyse : le proton passe* : Une molécule d'eau cède un proton H⁺ à une autre : il se forme HO⁻ et H₃O⁺ (réaction très limitée).  

<!-- bloc ab_b03 -->
4. Mesures (25 °C) : soude NaOH(s) → Na⁺(aq) + HO⁻(aq), totale, donc [HO⁻] = C.  
Eau pure, soude 10⁻⁴ puis 10⁻³ mol/L : pH 7, 10, 11 ; toujours [H₃O⁺]·[HO⁻] = 1,0·10⁻¹⁴.  
5. Définition : produit ionique de l'eau Ke = [H₃O⁺]·[HO⁻], constante de l'autoprotolyse.  
Ke ne dépend que de la température ; 25 °C : Ke = 1,0·10⁻¹⁴ (sans unité), toute solution.  
pKe = −log Ke = 14 à 25 °C ; Ke = 10^(−pKe).  

<!-- bloc ab_b04 -->
6. À 25 °C : acide [H₃O⁺] > [HO⁻], pH < 7 ; neutre pH = 7 ; basique [HO⁻] > [H₃O⁺], pH > 7.  
7. Neutre : [H₃O⁺] = [HO⁻] ⇒ Ke = [H₃O⁺]² ⇒ pH = pKe/2 (7 à 25 °C ; 7,5 à 0 °C).  
Remarque : acide si pH < pKe/2 ; basique si pH > pKe/2.  
8. [HO⁻] = Ke/[H₃O⁺] = 10^(pH − pKe) ; ex. pH = 10,60 → [HO⁻] = 3,98·10⁻⁴ mol/L.  
Attention : [HO⁻] n'est pas 10^(−pH) (10^(−pH) donne [H₃O⁺]).  
*Dessin — Acide, neutre, basique (25 °C)* : À 25 °C : pH < 7 si [H₃O⁺] > [HO⁻] (acide), pH = 7 neutre, pH > 7 si [HO⁻] > [H₃O⁺] (basique).  

<!-- bloc ab_b05 -->

## II. Une base dans l'eau : pH et taux d'avancement final

1. Rappel : AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq) : [A⁻]éq = [H₃O⁺]éq = C·τ ; [AH]éq = C(1−τ).  
K = Qr,éq = C·τ²/(1 − τ) ne dépend que de la température (acide éthanoïque : 1,6·10⁻⁵).  
2. Soude C = 1,0·10⁻² mol/L (totale) : [HO⁻] = C ; [H₃O⁺] = Ke/C = 10⁻¹² mol/L ; pH = 12,00.  
3. Ammoniac : NH₃(aq) + H₂O(l) ⇌ NH₄⁺(aq) + HO⁻(aq) ; C = 1,0·10⁻² mol/L, pH = 10,60.  
[HO⁻]éq = Ke/[H₃O⁺]éq = 3,98·10⁻⁴ mol/L, bien plus petit que C.  

Tableau d'avancement modèle (acide AH dans l'eau, volume V) :

| Équation | AH(aq) | + H₂O(l) | ⇌ A⁻(aq) | + H₃O⁺(aq) |
|---|---|---|---|---|
| État initial (x = 0) | C·V | excès | 0 | 0 |
| État d'équilibre (x_éq) | C·V − x_éq | excès | x_éq | x_éq |

x_max = C·V ; x_éq = [H₃O⁺]éq·V = 10^(−pH)·V ; τ = x_éq/x_max = 10^(−pH)/C (pour une base : τ = [HO⁻]éq/C).


<!-- bloc ab_b06 -->
4. Base : x_max = C·V ; x_éq = [HO⁻]éq·V ⇒ τ = [HO⁻]éq/C ; ammoniac : τ = 0,040 < 1.  
Attention : pour une base, τ n'est pas 10^(−pH)/C ; passer par [HO⁻]éq = 10^(pH − 14).  
Méthode : 1) [HO⁻]éq = 10^(pH − 14) ; 2) τ = [HO⁻]éq/C ; 3) Qr,éq = C·τ²/(1 − τ).  
Exemple (2022 R) : méthylamine C = 1,0·10⁻² mol/L, pH = 11,30 : τ = 0,20 ; Qr,éq = 5,0·10⁻⁴.  

<!-- bloc ab_b07 -->

## III. La constante d'acidité Ka et le pKa

1. Définition : constante d'acidité du couple AH/A⁻ : Ka = [A⁻]éq·[H₃O⁺]éq/[AH]éq.  
Ka : constante de AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq) ; sans unité, dépend de T seule.  
2. pKa = −log Ka ; Ka = 10^(−pKa) ; Ka grand ⇔ pKa petit (CH₃COOH : 4,8 ; HCOOH : 3,75).  
Méthode : 1) [A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; 2) [AH]éq = C − 10^(−pH) ; 3) Ka puis pKa.  
Exemple : acide éthanoïque C = 1,0·10⁻² mol/L, pH = 3,41 : Ka = 1,57·10⁻⁵ ; pKa = 4,8.  

<!-- bloc ab_b08 -->

## IV. Comparer des acides et des bases

3. Couple d'une base : NH₃(aq) + H₂O(l) ⇌ NH₄⁺(aq) + HO⁻(aq) a Qr,éq = Ke/Ka.  
Ka = Ke/Qr,éq = 10⁻¹⁴/1,65·10⁻⁵ = 6,06·10⁻¹⁰ ; pKa(NH₄⁺/NH₃) = 9,2. Attention : Ka ≠ Qr,éq.  
4. Couples de l'eau : pKa(H₃O⁺/H₂O) = 0 ; pKa(H₂O/HO⁻) = pKe = 14 (pKa étudiés : 0 à 14).  
1. Deux acides, même C : τ = 10^(−pH)/C ; pKa plus petit ⇒ τ plus grand, pH plus petit.  
Cet acide est plus fort : HCOOH (pKa 3,75 ; τ = 0,126) > CH₃COOH (pKa 4,8 ; τ = 0,039).  

<!-- bloc ab_b09 -->
2. Deux bases, même C : pKa du couple plus grand ⇒ base plus forte (τ et pH plus grands).  
Exemple : CH₃NH₂ (pKa 10,7 ; τ = 0,20) plus forte que NH₃ (pKa 9,2 ; τ = 0,040).  
3. Axe des pKa : l'acide est plus fort quand pKa diminue, la base quand pKa augmente.  
*Dessin — Classer les couples sur l'axe des pKa* : Acides à gauche (pKa entre parenthèses), bases conjuguées à droite : l'acide est plus fort quand le pKa diminue, la base plus forte quand il augmente.  

<!-- bloc ab_b10 -->

## V. La constante d'équilibre d'une réaction acide-base

1. AH₁(aq) + A₂⁻(aq) ⇌ A₁⁻(aq) + AH₂(aq) : K = Ka₁/Ka₂ (Ka₁ : couple de l'acide qui réagit).  
2. K = 10^(pKa₂ − pKa₁) ; ex. CH₃COOH(aq) + NH₃(aq) ⇌ CH₃COO⁻(aq) + NH₄⁺(aq) : K = 2,5·10⁴.  
3. CH₃COOH(aq) + HO⁻(aq) → CH₃COO⁻(aq) + H₂O(l) : K = Ka/Ke = 10^(14 − 4,8) = 1,6·10⁹.  
Remarque : K > 10⁴ : réaction pratiquement totale (flèche →) ; c'est la réaction de dosage.  
Attention (2020 R) : lire qui est Ka₁ ; le Ka du couple de l'acide qui réagit va en haut.  

<!-- bloc ab_b11 -->

## VI. Domaines de prédominance et diagramme de distribution

1. De Ka et log(a·b) = log a + log b : pH = pKa + log([A⁻]éq/[AH]éq).  
2. pH < pKa : AH prédomine ; pH > pKa : A⁻ prédomine ; pH = pKa : [AH] = [A⁻].  
Exemple : acide éthanoïque à pH = 3,41 < pKa = 4,8 : CH₃COOH prédomine.  
3. Distribution : %AH = [AH]/([AH] + [A⁻]) × 100 ; croisement des courbes à 50 % : pH = pKa.  
Méthode (2025 R) : pKa = pH du croisement ; au-dessus de 50 % pour pH < pKa : forme AH.  
*Dessin — Domaines de prédominance* : pH < pKa : CH₃COOH prédomine ; pH > pKa : CH₃COO⁻ prédomine. À pH = 3,41 < 4,8, c'est CH₃COOH.  
*Dessin — Diagramme de distribution* : Les deux courbes se croisent à 50 % pour pH = pKa = 4,8 ; à gauche, la forme acide CH₃COOH est au-dessus.  

<!-- bloc ab_b12 -->

## VII. Les indicateurs colorés

1. Définition : un indicateur coloré est un couple HInd/Ind⁻ dont les deux formes  
n'ont pas la même couleur (BBT : HInd jaune, Ind⁻ bleu) ; on voit la forme qui prédomine.  
2. Zone de virage : domaine de pH de la teinte sensible (deux formes en quantités voisines).  
BBT 6,0–7,6 ; hélianthine 3,1–4,4 ; rouge de méthyle 4,2–6,2 ; rouge de crésol 7,2–8,8.  
Règle : teinte acide si pH ≤ pKa − 1, teinte basique si pH ≥ pKa + 1 (zone autour du pKa).  
*Dessin — Zone de virage du BBT* : BBT : jaune (forme HInd) si pH < 6,0, vert dans la zone de virage 6,0 – 7,6 (autour de pKa ≈ 7,0), bleu (Ind⁻) au-delà.  

<!-- bloc ab_b13 -->

## VIII. Le dosage acido-basique : réaction, équivalence, courbe

1. Doser (titrer) : trouver C_A inconnue grâce à une solution titrante de C_B connue.  
2. Dosage : CH₃COOH(aq) + HO⁻(aq) → CH₃COO⁻(aq) + H₂O(l) ; réaction rapide, totale, unique.  
3. Définition : à l'équivalence, les réactifs sont dans les proportions stœchiométriques.  
Donc C_A·V_A = C_B·V_BE (V_BE versé à l'équivalence) ; avant E, HO⁻ est limitant.  
4. Courbe pH = f(V_B) : montée douce, saut de pH autour de V_BE, puis presque plat.  
*Dessin — Le montage du dosage* : La burette verse la soude (C_B connue) dans V_A d'acide ; l'agitateur mélange, le pH-mètre mesure le pH après chaque ajout.  
*Dessin — La courbe de dosage* : Le pH monte doucement, puis brusquement autour de 20 mL (saut de pH : l'équivalence), puis presque plus.  

Tableau d'avancement modèle du dosage (réaction totale) :

| Équation | CH₃COOH(aq) | + HO⁻(aq) | → CH₃COO⁻(aq) | + H₂O(l) |
|---|---|---|---|---|
| État initial | C_A·V_A | C_B·V_B | 0 | excès |
| État final (avant E) | C_A·V_A − C_B·V_B | 0 (limitant) | C_B·V_B | excès |
| À l'équivalence | C_A·V_A − x_E = 0 | C_B·V_BE − x_E = 0 | x_E | excès |

Exemple J : C_A = C_B = 1,0·10⁻² mol/L, V_A = 20,0 mL → V_BE = 20,0 mL, n(CH₃COOH)initial = 2,0·10⁻⁴ mol.


<!-- bloc ab_b14 -->
5. Méthode des tangentes : 1) deux tangentes parallèles de part et d'autre du saut ;  
2) la parallèle équidistante coupe la courbe en E ; 3) lire V_BE = 20,0 mL, pH_E = 8,3.  
Attention : les tracés doivent se voir sur la figure.  
Rappel : la pente en un point est celle de la tangente ; dpH/dV_B = pente de pH = f(V_B).  
6. Méthode de la dérivée : V_BE = abscisse du maximum (pic) de dpH/dV_B ; ici 20,0 mL.  
*Dessin — Méthode des tangentes parallèles* : Deux tangentes parallèles de part et d'autre du saut ; la parallèle à égale distance coupe la courbe en E (20,0 mL ; 8,3).  
*Dessin — Courbe dérivée : un pic en E* : dpH/dV_B est presque nulle loin de l'équivalence ; son maximum est à V_BE = 20,0 mL.  

<!-- bloc ab_b15 -->

## IX. Exploiter une courbe de dosage

1. pH_E = 7 : acide fort + base forte ; pH_E > 7 : acide faible + base forte (8,3 : A⁻) ;  
pH_E < 7 : base faible + acide fort (5,7 : l'acide NH₄⁺ est présent).  
2. À V_B = V_BE/2 : n(AH)restant = n(A⁻)formé ⇒ [AH] = [A⁻] ⇒ pH = pKa (ici 4,8).  
Attention : pH_E = 8,3 au point E n'est pas le pKa.  
3. Indicateur : sa zone de virage contient pH_E ; ici rouge de crésol (7,2–8,8), pas le BBT.  
*Dessin — Demi-équivalence : pH = pKa* : À V_B = V_BE/2 = 10,0 mL, [AH] = [A⁻] : pH = pKa = 4,8. Au point E (20,0 mL), pH_E = 8,3 n'est pas le pKa.  

<!-- bloc ab_b16 -->
4. Base dosée : NH₃(aq) + H₃O⁺(aq) → NH₄⁺(aq) + H₂O(l) ; C_B·V_B = C_A·V_AE ; pH descend.  
pH_E = 5,7 < 7 ; à V_AE/2 : pH = pKa = 9,2. Concentration massique : C_m = C·M (g/L).  
5. Dosage conductimétrique : σ = f(V_B) forme deux droites ; E à la rupture de pente.  
H₃O⁺(aq) + HO⁻(aq) → 2H₂O(l) ; σ = Σλᵢ[Xᵢ] : avant E, Na⁺ (λ petite) remplace H₃O⁺ : σ ↓.  
Après E, Na⁺ et HO⁻ s'ajoutent : σ ↑ ; ex. V_BE = 2,0 mL ⇒ C_A = 1,0·10⁻² mol/L.  
*Dessin — Dosage conductimétrique* : σ descend (H₃O⁺ remplacé par Na⁺) puis remonte (Na⁺ et HO⁻ en excès) : l'équivalence est à la rupture de pente, V_BE = 2,0 mL.  

<!-- bloc ab_b17 -->

## X. Sujets du national

Méthode : 1) équation (→) ; 2) lire E ; 3) C_A·V_A = C_B·V_BE ; 4) zone de virage ∋ pH_E.  
2016 N : E (6 mL ; 8,7) ; C_A = 5·10⁻² × 6/5 = 6·10⁻² mol/L ; bleu de thymol (8 – 9,6).  
2022 R (base dosée) : E (15 mL ; 6,6), pH_E < 7 ; C_b = C_a·V_aE/V_b = 10⁻² mol/L ; BBT.  
2022 N : %AH = 1/(1 + [A⁻]/[AH]), [A⁻]/[AH] = 10^(pH − pKa) = 0,316 → 76 %.  
Attention : le pourcentage n'est pas le rapport [A⁻]/[AH].  

<!-- bloc ab_b18 -->
2024 R : pKa = pH au croisement = 10,8 ; 80 % d'acide : pH = 10,8 + log(20/80) = 10,2.  
2023 R : au point Q (V_A = V_AE/2 = 10 mL), pH = pKa = 9,9 ; pH_E = 5,8 : rouge de méthyle.  
Attention : solution diluée 10 fois ⇒ C₀ = 10·C_B = 0,4 mol/L.  

<!-- bloc ab_b19 -->

## XI. Un national joué pas à pas : 2018 N

Q1.1 : AH(aq) + HO⁻(aq) → A⁻(aq) + H₂O(l), une seule flèche ; Na⁺ est spectateur.  
Q1.2 : tangentes parallèles et parallèle équidistante : V_BE = 10 mL ; pH_E ≈ 8.  
Q1.3 : C_A = C_B·V_BE/V_A = 3·10⁻² × 10/15 = 2·10⁻² mol/L (V en mêmes unités).  

<!-- bloc ab_b20 -->
Q1.4 : rouge de crésol, car sa zone de virage [7,2 ; 8,8] contient pH_E ≈ 8.  
Q1.5 : [A⁻]/[AH] = 10^(pH − pKa) = 10^(8 − 3,9) ≈ 1,3·10⁴ > 1 : A⁻ prédomine.  
En plus : à V_BE/2 = 5 mL, pH = 3,9 = pKa : on retrouve K_A = 10^(−3,9).  

<!-- bloc ab_b21 -->

## XII. Bilan du chapitre

À retenir : Ke = [H₃O⁺]·[HO⁻] ; pKa = −log Ka ; K = 10^(pKa₂ − pKa₁) ; τ = [HO⁻]éq/C.  
pH = pKa + log([A⁻]/[AH]) ; dosage : C_A·V_A = C_B·V_BE ; pH = pKa à V_BE/2.  
Attention : [HO⁻] ≠ 10^(−pH) ; Ka ≠ Qr,éq pour une base ; pH_E ≠ pKa ; dosage écrit avec →.  


---

## Dessins (`cahier_figures`)

| Diapo | Dessin | Données |
|---|---|---|
| `ab_w1_autoprotolyse` | L'autoprotolyse : le proton passe | nouveau : schéma du transfert du proton (H⁺ en rose, comme le lexique visuel), équation en dessous |
| `ab_w3_solutions` | Acide, neutre, basique (25 °C) | repris : axe des pH, 7 neutre (25 °C) |
| `ab_c3_classement` | Classer les couples sur l'axe des pKa | repris : axe vertical des pKa, 3,75 ; 4,8 ; 9,2 ; 10,7 |
| `ab_p2_domaines` | Domaines de prédominance | repris : pKa = 4,8, point pH = 3,41 |
| `ab_p3_distribution` | Diagramme de distribution | repris : 100/(1 + 10^(pH − 4,8)), croisement 50 % à 4,8 ; 90,9 % à 3,8 |
| `ab_i2_virage` | Zone de virage du BBT | repris : BBT 6,0 – 7,6 |
| `ab_d1_montage` | Le montage du dosage | repris : burette, bécher, agitateur, pH-mètre |
| `ab_d4_courbe` | La courbe de dosage | repris : points du cours 3,41 ; 4,34 ; 4,80 ; 5,28 ; 6,08 ; 8,25 ; 10,39 ; 11,30 |
| `ab_d5_tangentes` | Méthode des tangentes parallèles | repris : E (20,0 mL ; 8,3) |
| `ab_d6_derivee` | Courbe dérivée : un pic en E | nouveau : dpH/dV_B calculé sur la même courbe (bilan des charges, pKa 4,8 ; pas de 0,2 mL à E : pic 7,3 mL⁻¹ à 20,0 mL) |
| `ab_e2_demi` | Demi-équivalence : pH = pKa | repris : (10,0 mL ; 4,8) et E (20,0 mL ; 8,3) |
| `ab_e5_conductimetrie` | Dosage conductimétrique | repris : 38,8 → 11,4 (2,0 mL) → 33,5 mS/m (4,0 mL) |

## Table de découpage — version en ligne (`backend/data/courses/phys_ch13_acides_bases.json`, 14 blocs)

| Bloc | Lignes (début) | Figures | Diapos → bulle |
|---|---|---|---|
| `ab_r_b1` (4 l.) | Plan : l'eau (Ke) → une base dans l'ea… / 1. Constat : eau pure pH = 7,00 ; vina… / 2. Puissances de dix : 10⁻³ = 0,001 ; … / Pour a, b > 0 : log(a·b) = log a + log… | — | `ab_o1_carte` → Plan : l'eau (Ke) → une base dans l'eau → Ka, pKa …<br>`ab_o2_trois_ph` → Eau pure : pH = 7,00 (BBT vert) ; vinaigre dilué :…<br>`ab_z1_puissance` → 10⁻³ = 0,001 ; 4,0·10⁻⁴ = 0,00040 ; log(10ⁿ) = n ;… |
| `ab_s1_b1` (5 l.) | 1. Définition : un acide est une espèc… / une base est capable de capter un prot… / 2. L'eau : couples H₃O⁺/H₂O et H₂O/HO⁻… / 3. Rappel : AH(aq) + H₂O(l) ⇌ A⁻(aq) +… / K = Qr,éq = C·τ²/(1 − τ) ne dépend que… | — | `ab_r1_rappel` → Acide : espèce chimique capable de céder un proton…<br>`ab_r1b_eau_ph` → L'eau : H₃O⁺/H₂O (H₂O base) et H₂O/HO⁻ (H₂O acide)…<br>`ab_r2_constante` → Rappel : AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq) : [A⁻… |
| `ab_s1_b2` (6 l.) | 1. Définition : l'autoprotolyse de l'e… / 2H₂O(l) ⇌ H₃O⁺(aq) + HO⁻(aq) ; eau pur… / 2. Pour 1,0 L : n₀ = ρ·V/M = 55,6 mol … / τ = x_éq/x_max = 3,6·10⁻⁹ ≪ 1 : très l… / 3. Définition : produit ionique de l'e… / Ke dépend de T seule ; 25 °C : Ke = 1,… | L'autoprotolyse : le proton passe | `ab_w1_autoprotolyse` → Autoprotolyse de l'eau : réaction entre deux moléc… [dessin]<br>`ab_w1b_limitee` → Pour 1,0 L : n₀ = ρ·V/M = 55,6 mol ; x_max = n₀/2 …<br>`ab_w2_ke` → Ke = [H₃O⁺]·[HO⁻] : constante d'équilibre de l'aut… |
| `ab_s1_b2b` (5 l.) | 4. À 25 °C : acide [H₃O⁺] > [HO⁻], pH … / 5. Neutre : [H₃O⁺] = [HO⁻] ⇒ Ke = [H₃O… / Remarque : acide si pH < pKe/2 ; basiq… / 6. [HO⁻] = Ke/[H₃O⁺] = 10^(pH − pKe) ;… / Attention : [HO⁻] n'est pas 10^(−pH) (… | Acide, neutre, basique (25 °C) | `ab_w3_solutions` → À 25 °C : acide [H₃O⁺] > [HO⁻], pH < 7 ; neutre pH… [dessin]<br>`ab_w3b_neutre` → Neutre : [H₃O⁺] = [HO⁻] ⇒ Ke = [H₃O⁺]² ⇒ pH = pKe/…<br>`ab_w4_ho` → [HO⁻] = Ke/[H₃O⁺] = 10^(pH − pKe) ; ex. pH = 10,60… |
| `ab_s1_b3` (6 l.) | 7. Soude C = 1,0·10⁻² mol/L (totale) :… / 1. Ammoniac : NH₃(aq) + H₂O(l) ⇌ NH₄⁺(… / 2. Base : x_max = C·V ; x_éq = [HO⁻]éq… / Attention : pour une base, τ n'est pas… / Méthode : 1) [HO⁻]éq = 10^(pH − 14) ; … / Exemple (2022 R) : méthylamine C = 1,0… | — | `ab_w5_soude` → Soude C = 1,0·10⁻² mol/L (totale) : [HO⁻] = C ; [H…<br>`ab_b1_ammoniac` → Ammoniac : NH₃(aq) + H₂O(l) ⇌ NH₄⁺(aq) + HO⁻(aq) ;…<br>`ab_b2_taux` → Base : x_max = C·V ; x_éq = [HO⁻]éq·V ⇒ τ = [HO⁻]é…<br>`ab_b3_national` → Méthode : 1) [HO⁻]éq = 10^(pH − 14) ; 2) τ = [HO⁻]… |
| `ab_s2_b1` (6 l.) | 1. Définition : constante d'acidité du… / Ka : constante de AH(aq) + H₂O(l) ⇌ A⁻… / 2. pKa = −log Ka ; Ka = 10^(−pKa) ; Ka… / Méthode : 1) [A⁻]éq = [H₃O⁺]éq = 10^(−… / Exemple : acide éthanoïque C = 1,0·10⁻… / 3. Couple d'une base : NH₃ + H₂O ⇌ NH₄… | — | `ab_a1_ka` → Définition : constante d'acidité du couple AH/A⁻ :…<br>`ab_a2_pka` → pKa = −log Ka ; Ka = 10^(−pKa) ; Ka grand ⇔ pKa pe…<br>`ab_a3_mesure` → Méthode : 1) [A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; 2) [AH…<br>`ab_a4_ammonium` → Couple d'une base : NH₃(aq) + H₂O(l) ⇌ NH₄⁺(aq) + … |
| `ab_s2_b2` (5 l.) | 4. Couples de l'eau : pKa(H₃O⁺/H₂O) = … / 1. Deux acides, même C : τ = 10^(−pH)/… / Cet acide est plus fort : HCOOH (pKa 3… / 2. Même C : pKa du couple plus grand ⇒… / 3. Axe des pKa : l'acide est plus fort… | Classer les couples sur l'axe des pKa | `ab_a5_eau` → Couples de l'eau : pKa(H₃O⁺/H₂O) = 0 ; pKa(H₂O/HO⁻…<br>`ab_c1_acides` → Deux acides, même C : τ = 10^(−pH)/C ; pKa plus pe…<br>`ab_c2_bases` → Deux bases, même C : pKa du couple plus grand ⇒ ba…<br>`ab_c3_classement` → Axe des pKa : l'acide est plus fort quand pKa dimi… [dessin] |
| `ab_s2_b3` (5 l.) | 1. AH₁(aq) + A₂⁻(aq) ⇌ A₁⁻(aq) + AH₂(a… / 2. K = 10^(pKa₂ − pKa₁) ; ex. CH₃COOH(… / 3. CH₃COOH(aq) + HO⁻(aq) → CH₃COO⁻(aq)… / Remarque : K > 10⁴ : réaction pratique… / Attention (2020 R) : lire qui est Ka₁ … | — | `ab_k1_reaction` → AH₁(aq) + A₂⁻(aq) ⇌ A₁⁻(aq) + AH₂(aq) : K = Ka₁/Ka…<br>`ab_k2_puissance` → K = 10^(pKa₂ − pKa₁) ; ex. CH₃COOH(aq) + NH₃(aq) ⇌…<br>`ab_k3_totale` → CH₃COOH(aq) + HO⁻(aq) → CH₃COO⁻(aq) + H₂O(l) : K =…<br>`ab_k4_national` → Attention (2020 R) : lire qui est Ka₁ ; le Ka du c… |
| `ab_s3_b1` (5 l.) | 1. De Ka et log(a·b) = log a + log b :… / 2. pH < pKa : AH prédomine ; pH > pKa … / Exemple : acide éthanoïque à pH = 3,41… / 3. Distribution : %AH = [AH]/([AH] + [… / Méthode (2025 R) : pKa = pH du croisem… | Domaines de prédominance, Diagramme de distribution | `ab_p1_relation` → De Ka et log(a·b) = log a + log b : pH = pKa + log…<br>`ab_p2_domaines` → pH < pKa : AH prédomine ; pH > pKa : A⁻ prédomine … [dessin]<br>`ab_p3_distribution` → Distribution : %AH = [AH]/([AH] + [A⁻]) × 100 ; cr… [dessin]<br>`ab_p4_national` → Méthode (2025 R) : pKa = pH du croisement ; au-des… |
| `ab_s3_b2` (6 l.) | 1. Définition : un indicateur coloré e… / n'ont pas la même couleur (BBT : HInd … / 2. Zone de virage : domaine de pH de l… / BBT 6,0–7,6 ; hélianthine 3,1–4,4 ; ro… / 1. Doser (titrer) : trouver C_A inconn… / 2. Dosage : CH₃COOH(aq) + HO⁻(aq) → CH… | Zone de virage du BBT, Le montage du dosage | `ab_i1_indicateur` → Définition : un indicateur coloré est un couple HI…<br>`ab_i2_virage` → Zone de virage : domaine de pH de la teinte sensib… [dessin]<br>`ab_i2b_regle` → Règle : teinte acide si pH ≤ pKa − 1, teinte basiq…<br>`ab_d1_montage` → Doser : trouver C_A inconnue avec une solution tit… [dessin]<br>`ab_d2_reaction` → Dosage : CH₃COOH(aq) + HO⁻(aq) → CH₃COO⁻(aq) + H₂O… |
| `ab_s3_b3` (6 l.) | 3. Définition : à l'équivalence, les r… / Donc C_A·V_A = C_B·V_BE (V_BE versé à … / 4. Courbe pH = f(V_B) : montée douce, … / 5. Méthode des tangentes : la parallèl… / Ici V_BE = 20,0 mL ; pH_E = 8,3 (atten… / 6. Méthode de la dérivée : V_BE = absc… | Méthode des tangentes parallèles, Courbe dérivée : un pic en E | `ab_d3_equivalence` → Équivalence : réactifs dans les proportions stœchi…<br>`ab_d4_courbe` → Courbe pH = f(V_B) : montée douce, saut de pH auto… [dessin]<br>`ab_d5_tangentes` → Deux tangentes parallèles de part et d'autre du sa… [dessin]<br>`ab_z2_pente` → Rappel : la pente en un point est celle de la tang…<br>`ab_d6_derivee` → Méthode de la dérivée : V_BE = abscisse du maximum… [dessin] |
| `ab_s4_b1` (6 l.) | 1. pH_E = 7 : acide fort + base forte … / pH_E < 7 : base faible + acide fort (5… / 2. À V_B = V_BE/2 : n(AH)restant = n(A… / Attention : pH_E = 8,3 au point E n'es… / 3. Indicateur : sa zone de virage cont… / 4. Base dosée : NH₃(aq) + H₃O⁺(aq) → N… | Demi-équivalence : pH = pKa | `ab_e1_phe` → pH_E = 7 : acide fort + base forte ; pH_E > 7 : ac…<br>`ab_e2_demi` → À V_B = V_BE/2 : n(AH)restant = n(A⁻)formé, donc [… [dessin]<br>`ab_e3_indicateur` → Indicateur : sa zone de virage contient pH_E ; ici…<br>`ab_e4_base` → Base dosée : NH₃(aq) + H₃O⁺(aq) → NH₄⁺(aq) + H₂O(l… |
| `ab_s4_b2` (6 l.) | 5. Dosage conductimétrique : σ = f(V_B… / Avant E, Na⁺ remplace H₃O⁺ (λ plus pet… / Méthode : 1) équation (→) ; 2) lire E … / 2022 R (base dosée) : E (15 mL ; 6,6),… / 2022 N : %AH = 1/(1 + [A⁻]/[AH]), [A⁻]… / Attention : le pourcentage n'est pas l… | Dosage conductimétrique | `ab_e5_conductimetrie` → Dosage conductimétrique : σ = f(V_B) forme deux dr… [dessin]<br>`ab_e5b_pourquoi` → Avant E, Na⁺ remplace H₃O⁺ (λ plus petite) : σ dim…<br>`ab_n1_2016n` → 2016 N : E (6 mL ; 8,7) par les tangentes ; C_A = …<br>`ab_n2_2022r` → 2022 R (base dosée) : E (15 mL ; 6,6), pH_E < 7 ; …<br>`ab_n3_2022n` → 2022 N : %AH = 1/(1 + [A⁻]/[AH]), [A⁻]/[AH] = 10^(… |
| `ab_s4_b3` (6 l.) | 2024 R : pKa = pH au croisement = 10,8… / 2023 R : au point Q (V_A = V_AE/2 = 10… / Attention : solution diluée 10 fois ⇒ … / À retenir : Ke = [H₃O⁺]·[HO⁻] ; pKa = … / pH = pKa + log([A⁻]/[AH]) ; dosage : C… / Attention : [HO⁻] ≠ 10^(−pH) ; Ka ≠ Qr… | — | `ab_n4_2024r` → 2024 R : pKa = pH au croisement = 10,8 ; 80 % d'ac…<br>`ab_n5_2023r` → 2023 R : au point Q (V_A = V_AE/2 = 10 mL), pH = p…<br>`ab_bl_fiche` → À retenir : Ke = [H₃O⁺]·[HO⁻] ; pKa = −log Ka ; K …<br>`ab_cr_carte` → Attention : [HO⁻] ≠ 10^(−pH) ; Ka ≠ Qr,éq pour une… |

En ligne, les lignes sont les mêmes que ci-dessus, numérotées dans les parties de cette version (Ouverture, puis I. Rappels … XII. Bilan, titres affichés par l'écran). Lignes plus courtes (même contenu) dans les blocs de 4 ou 5 diapos ; non recopiées dans le bloc mais gardées dans la bulle : `ab_i2b_regle` (bloc `ab_s3_b2`), `ab_z2_pente` (`ab_s3_b3`), `ab_n2_2022r` (`ab_s4_b2`).

## Table de découpage — version en attente (`backend/data/courses/en_attente/phys_ch13_acides_bases.json`, 21 blocs)

| Bloc | Lignes (début) | Figures | Diapos → bulle |
|---|---|---|---|
| `ab_b01` (5 l.) | 1. Puissances de dix : 10⁻³ = 0,001 ; … / Pour a, b > 0 : log(a·b) = log a + log… / 2. Définition : un acide est une espèc… / une base est capable de capter un prot… / 3. L'eau : couples H₃O⁺/H₂O et H₂O/HO⁻… | — | `ab_z1_puissance` → 10⁻³ = 0,001 ; 4,0·10⁻⁴ = 0,00040 ; log(10ⁿ) = n ;…<br>`ab_r1_rappel` → Acide : espèce chimique capable de céder un proton…<br>`ab_r1b_eau_ph` → L'eau : H₃O⁺/H₂O (H₂O base) et H₂O/HO⁻ (H₂O acide)… |
| `ab_b02` (5 l.) | 1. Constat : eau pure pH = 7,00 ; vina… / 2. Définition : l'autoprotolyse de l'e… / 2H₂O(l) ⇌ H₃O⁺(aq) + HO⁻(aq) ; eau pur… / 3. Pour 1,0 L : n₀ = ρ·V/M = 55,6 mol … / τ = x_éq/x_max = 3,6·10⁻⁹ ≪ 1 : très l… | L'autoprotolyse : le proton passe | `ab_o2_trois_ph` → Eau pure : pH = 7,00 (BBT vert) ; vinaigre dilué :…<br>`ab_w1_autoprotolyse` → Autoprotolyse de l'eau : réaction entre deux moléc… [dessin]<br>`ab_w1b_limitee` → Pour 1,0 L : n₀ = ρ·V/M = 55,6 mol ; x_max = n₀/2 … |
| `ab_b03` (5 l.) | 4. Mesures (25 °C) : soude NaOH(s) → N… / Eau pure, soude 10⁻⁴ puis 10⁻³ mol/L :… / 5. Définition : produit ionique de l'e… / Ke ne dépend que de la température ; 2… / pKe = −log Ke = 14 à 25 °C ; Ke = 10^(… | — | `ab_w2a_mesures` → Mesures (25 °C) : soude NaOH(s) → Na⁺(aq) + HO⁻(aq…<br>`ab_w2_ke` → Ke = [H₃O⁺]·[HO⁻] : constante d'équilibre de l'aut… |
| `ab_b04` (5 l.) | 6. À 25 °C : acide [H₃O⁺] > [HO⁻], pH … / 7. Neutre : [H₃O⁺] = [HO⁻] ⇒ Ke = [H₃O… / Remarque : acide si pH < pKe/2 ; basiq… / 8. [HO⁻] = Ke/[H₃O⁺] = 10^(pH − pKe) ;… / Attention : [HO⁻] n'est pas 10^(−pH) (… | Acide, neutre, basique (25 °C) | `ab_w3_solutions` → À 25 °C : acide [H₃O⁺] > [HO⁻], pH < 7 ; neutre pH… [dessin]<br>`ab_w3b_neutre` → Neutre : [H₃O⁺] = [HO⁻] ⇒ Ke = [H₃O⁺]² ⇒ pH = pKe/…<br>`ab_w4_ho` → [HO⁻] = Ke/[H₃O⁺] = 10^(pH − pKe) ; ex. pH = 10,60… |
| `ab_b05` (5 l.) | 1. Rappel : AH(aq) + H₂O(l) ⇌ A⁻(aq) +… / K = Qr,éq = C·τ²/(1 − τ) ne dépend que… / 2. Soude C = 1,0·10⁻² mol/L (totale) :… / 3. Ammoniac : NH₃(aq) + H₂O(l) ⇌ NH₄⁺(… / [HO⁻]éq = Ke/[H₃O⁺]éq = 3,98·10⁻⁴ mol/… | — | `ab_r2_constante` → Rappel : AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq) : [A⁻…<br>`ab_w5_soude` → Soude C = 1,0·10⁻² mol/L (totale) : [HO⁻] = C ; [H…<br>`ab_b1_ammoniac` → Ammoniac : NH₃(aq) + H₂O(l) ⇌ NH₄⁺(aq) + HO⁻(aq) ;… |
| `ab_b06` (4 l.) | 4. Base : x_max = C·V ; x_éq = [HO⁻]éq… / Attention : pour une base, τ n'est pas… / Méthode : 1) [HO⁻]éq = 10^(pH − 14) ; … / Exemple (2022 R) : méthylamine C = 1,0… | — | `ab_b2_taux` → Base : x_max = C·V ; x_éq = [HO⁻]éq·V ⇒ τ = [HO⁻]é…<br>`ab_b3_national` → Méthode : 1) [HO⁻]éq = 10^(pH − 14) ; 2) τ = [HO⁻]… |
| `ab_b07` (5 l.) | 1. Définition : constante d'acidité du… / Ka : constante de AH(aq) + H₂O(l) ⇌ A⁻… / 2. pKa = −log Ka ; Ka = 10^(−pKa) ; Ka… / Méthode : 1) [A⁻]éq = [H₃O⁺]éq = 10^(−… / Exemple : acide éthanoïque C = 1,0·10⁻… | — | `ab_a1_ka` → Définition : constante d'acidité du couple AH/A⁻ :…<br>`ab_a2_pka` → pKa = −log Ka ; Ka = 10^(−pKa) ; Ka grand ⇔ pKa pe…<br>`ab_a3_mesure` → Méthode : 1) [A⁻]éq = [H₃O⁺]éq = 10^(−pH) ; 2) [AH… |
| `ab_b08` (5 l.) | 3. Couple d'une base : NH₃(aq) + H₂O(l… / Ka = Ke/Qr,éq = 10⁻¹⁴/1,65·10⁻⁵ = 6,06… / 4. Couples de l'eau : pKa(H₃O⁺/H₂O) = … / 1. Deux acides, même C : τ = 10^(−pH)/… / Cet acide est plus fort : HCOOH (pKa 3… | — | `ab_a4_ammonium` → Couple d'une base : NH₃(aq) + H₂O(l) ⇌ NH₄⁺(aq) + …<br>`ab_a5_eau` → Couples de l'eau : pKa(H₃O⁺/H₂O) = 0 ; pKa(H₂O/HO⁻…<br>`ab_c1_acides` → Deux acides, même C : τ = 10^(−pH)/C ; pKa plus pe… |
| `ab_b09` (3 l.) | 2. Deux bases, même C : pKa du couple … / Exemple : CH₃NH₂ (pKa 10,7 ; τ = 0,20)… / 3. Axe des pKa : l'acide est plus fort… | Classer les couples sur l'axe des pKa | `ab_c2_bases` → Deux bases, même C : pKa du couple plus grand ⇒ ba…<br>`ab_c3_classement` → Axe des pKa : l'acide est plus fort quand pKa dimi… [dessin] |
| `ab_b10` (5 l.) | 1. AH₁(aq) + A₂⁻(aq) ⇌ A₁⁻(aq) + AH₂(a… / 2. K = 10^(pKa₂ − pKa₁) ; ex. CH₃COOH(… / 3. CH₃COOH(aq) + HO⁻(aq) → CH₃COO⁻(aq)… / Remarque : K > 10⁴ : réaction pratique… / Attention (2020 R) : lire qui est Ka₁ … | — | `ab_k1_reaction` → AH₁(aq) + A₂⁻(aq) ⇌ A₁⁻(aq) + AH₂(aq) : K = Ka₁/Ka…<br>`ab_k2_puissance` → K = 10^(pKa₂ − pKa₁) ; ex. CH₃COOH(aq) + NH₃(aq) ⇌…<br>`ab_k3_totale` → CH₃COOH(aq) + HO⁻(aq) → CH₃COO⁻(aq) + H₂O(l) : K =…<br>`ab_k4_national` → Attention (2020 R) : lire qui est Ka₁ ; le Ka du c… |
| `ab_b11` (5 l.) | 1. De Ka et log(a·b) = log a + log b :… / 2. pH < pKa : AH prédomine ; pH > pKa … / Exemple : acide éthanoïque à pH = 3,41… / 3. Distribution : %AH = [AH]/([AH] + [… / Méthode (2025 R) : pKa = pH du croisem… | Domaines de prédominance, Diagramme de distribution | `ab_p1_relation` → De Ka et log(a·b) = log a + log b : pH = pKa + log…<br>`ab_p2_domaines` → pH < pKa : AH prédomine ; pH > pKa : A⁻ prédomine … [dessin]<br>`ab_p3_distribution` → Distribution : %AH = [AH]/([AH] + [A⁻]) × 100 ; cr… [dessin]<br>`ab_p4_national` → Méthode (2025 R) : pKa = pH du croisement ; au-des… |
| `ab_b12` (5 l.) | 1. Définition : un indicateur coloré e… / n'ont pas la même couleur (BBT : HInd … / 2. Zone de virage : domaine de pH de l… / BBT 6,0–7,6 ; hélianthine 3,1–4,4 ; ro… / Règle : teinte acide si pH ≤ pKa − 1, … | Zone de virage du BBT | `ab_i1_indicateur` → Définition : un indicateur coloré est un couple HI…<br>`ab_i2_virage` → Zone de virage : domaine de pH de la teinte sensib… [dessin]<br>`ab_i2b_regle` → Règle : teinte acide si pH ≤ pKa − 1, teinte basiq… |
| `ab_b13` (5 l.) | 1. Doser (titrer) : trouver C_A inconn… / 2. Dosage : CH₃COOH(aq) + HO⁻(aq) → CH… / 3. Définition : à l'équivalence, les r… / Donc C_A·V_A = C_B·V_BE (V_BE versé à … / 4. Courbe pH = f(V_B) : montée douce, … | Le montage du dosage, La courbe de dosage | `ab_d1_montage` → Doser : trouver C_A inconnue avec une solution tit… [dessin]<br>`ab_d2_reaction` → Dosage : CH₃COOH(aq) + HO⁻(aq) → CH₃COO⁻(aq) + H₂O…<br>`ab_d3_equivalence` → Équivalence : réactifs dans les proportions stœchi…<br>`ab_d4_courbe` → Courbe pH = f(V_B) : montée douce, saut de pH auto… [dessin] |
| `ab_b14` (5 l.) | 5. Méthode des tangentes : 1) deux tan… / 2) la parallèle équidistante coupe la … / Attention : les tracés doivent se voir… / Rappel : la pente en un point est cell… / 6. Méthode de la dérivée : V_BE = absc… | Méthode des tangentes parallèles, Courbe dérivée : un pic en E | `ab_d5_tangentes` → Deux tangentes parallèles de part et d'autre du sa… [dessin]<br>`ab_z2_pente` → Rappel : la pente en un point est celle de la tang…<br>`ab_d6_derivee` → Méthode de la dérivée : V_BE = abscisse du maximum… [dessin] |
| `ab_b15` (5 l.) | 1. pH_E = 7 : acide fort + base forte … / pH_E < 7 : base faible + acide fort (5… / 2. À V_B = V_BE/2 : n(AH)restant = n(A… / Attention : pH_E = 8,3 au point E n'es… / 3. Indicateur : sa zone de virage cont… | Demi-équivalence : pH = pKa | `ab_e1_phe` → pH_E = 7 : acide fort + base forte ; pH_E > 7 : ac…<br>`ab_e2_demi` → À V_B = V_BE/2 : n(AH)restant = n(A⁻)formé, donc [… [dessin]<br>`ab_e3_indicateur` → Indicateur : sa zone de virage contient pH_E ; ici… |
| `ab_b16` (5 l.) | 4. Base dosée : NH₃(aq) + H₃O⁺(aq) → N… / pH_E = 5,7 < 7 ; à V_AE/2 : pH = pKa =… / 5. Dosage conductimétrique : σ = f(V_B… / H₃O⁺(aq) + HO⁻(aq) → 2H₂O(l) ; σ = Σλᵢ… / Après E, Na⁺ et HO⁻ s'ajoutent : σ ↑ ;… | Dosage conductimétrique | `ab_e4_base` → Base dosée : NH₃(aq) + H₃O⁺(aq) → NH₄⁺(aq) + H₂O(l…<br>`ab_e5_conductimetrie` → Dosage conductimétrique : σ = f(V_B) forme deux dr… [dessin]<br>`ab_e5b_pourquoi` → Avant E, Na⁺ remplace H₃O⁺ (λ plus petite) : σ dim… |
| `ab_b17` (5 l.) | Méthode : 1) équation (→) ; 2) lire E … / 2016 N : E (6 mL ; 8,7) ; C_A = 5·10⁻²… / 2022 R (base dosée) : E (15 mL ; 6,6),… / 2022 N : %AH = 1/(1 + [A⁻]/[AH]), [A⁻]… / Attention : le pourcentage n'est pas l… | — | `ab_n1_2016n` → 2016 N : E (6 mL ; 8,7) par les tangentes ; C_A = …<br>`ab_n2_2022r` → 2022 R (base dosée) : E (15 mL ; 6,6), pH_E < 7 ; …<br>`ab_n3_2022n` → 2022 N : %AH = 1/(1 + [A⁻]/[AH]), [A⁻]/[AH] = 10^(… |
| `ab_b18` (3 l.) | 2024 R : pKa = pH au croisement = 10,8… / 2023 R : au point Q (V_A = V_AE/2 = 10… / Attention : solution diluée 10 fois ⇒ … | — | `ab_n4_2024r` → 2024 R : pKa = pH au croisement = 10,8 ; 80 % d'ac…<br>`ab_n5_2023r` → 2023 R : au point Q (V_A = V_AE/2 = 10 mL), pH = p… |
| `ab_b19` (3 l.) | Q1.1 : AH(aq) + HO⁻(aq) → A⁻(aq) + H₂O… / Q1.2 : tangentes parallèles et parallè… / Q1.3 : C_A = C_B·V_BE/V_A = 3·10⁻² × 1… | — | `ab_x1_equation` → Q1.1 : AH(aq) + HO⁻(aq) → A⁻(aq) + H₂O(l), une seu…<br>`ab_x2_tangentes` → Q1.2 : tangentes parallèles et parallèle équidista…<br>`ab_x3_concentration` → Q1.3 : C_A = C_B·V_BE/V_A = 3·10⁻² × 10/15 = 2·10⁻… |
| `ab_b20` (3 l.) | Q1.4 : rouge de crésol, car sa zone de… / Q1.5 : [A⁻]/[AH] = 10^(pH − pKa) = 10^… / En plus : à V_BE/2 = 5 mL, pH = 3,9 = … | — | `ab_x4_indicateur` → Q1.4 : rouge de crésol, car sa zone de virage [7,2…<br>`ab_x5_predominance` → Q1.5 : [A⁻]/[AH] = 10^(pH − pKa) = 10^(8 − 3,9) ≈ …<br>`ab_x6_pka` → En plus : à V_BE/2 = 5 mL, pH = 3,9 = pKa : on ret… |
| `ab_b21` (3 l.) | À retenir : Ke = [H₃O⁺]·[HO⁻] ; pKa = … / pH = pKa + log([A⁻]/[AH]) ; dosage : C… / Attention : [HO⁻] ≠ 10^(−pH) ; Ka ≠ Qr… | — | `ab_bl_fiche` → À retenir : Ke = [H₃O⁺]·[HO⁻] ; pKa = −log Ka ; K …<br>`ab_cr_carte` → Attention : [HO⁻] ≠ 10^(−pH) ; Ka ≠ Qr,éq pour une… |

Script de découpage (relançable, remplace les champs) : `cahier.py` du dossier de travail de la session ; il ne touche que `blocs[].cahier`, `blocs[].cahier_figures`, `concentration.cahier`, `concentration.cahier_figures`.

