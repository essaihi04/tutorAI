# Le cahier de l'élève : circuit RLC série (`phys_ch8_circuit_RLC`)

18 novembre 2026, skill `cahier-de-l-eleve`. Ce fichier contient le cahier idéal du chapitre, écrit d'un seul tenant.
Il a ensuite été découpé dans le cours en ligne (`backend/data/courses/phys_ch8_circuit_RLC.json`) et dans sa copie en
attente (`backend/data/courses/en_attente/phys_ch8_circuit_RLC.json`). Seuls les champs `blocs[].cahier`,
`blocs[].cahier_figures`, `concentration.cahier` et `concentration.cahier_figures` ont changé. Le script d'application
est relançable : il relit le fichier avant d'écrire et garde sa mise en forme.

## Comment le cahier s'affiche, et le choix qui en découle

Le lecteur (`frontend/src/components/course/memoire/CycleBloc.tsx`, `cahier.ts`) numérote déjà le plan :
- en entrant dans une partie, il écrit le titre de la partie (`activities[].title` : « IV. La solution du circuit LC… ») ;
- quand le bloc a **autant de lignes que de diapositives**, il écrit chaque ligne sous le titre numéroté de sa diapositive
  (« 3. Rappel : la dérivée d'un cosinus »).
  Cette numérotation continue d'un bloc à l'autre et elle est la même que dans la bulle de la diapositive.

Le cahier a donc **une ligne par diapositive**. La même ligne sert de bulle (`concentration.cahier`) et de ligne de bloc.
Le plan numéroté (I → XI ou XII, puis 1, 2, 3… dans chaque partie) est celui du cours. Il s'affiche seul, sans trou ni
doublon. Les lignes ne portent donc pas de numéro, sauf les étapes des méthodes (« 1) … 2) … »).

## Correspondance avec le plan commun RC / RL / RLC

Le cours a son propre plan, déjà affiché à l'écran (titres des parties, qu'on ne change pas ici). Il suit la même démarche
que le RC et le RL :

| Plan commun (RC, RL, RLC) | Parties du cours RLC |
|---|---|
| I. Le dipôle. 1. Montage et conventions | I. Un condensateur qui se vide dans une bobine (rappels q = C·u_C, u_b ; convention récepteur dessinée ; montage avec K ; maille fléchée) |
| I. 2. Les trois régimes | II. Les trois régimes (en attente : « Ce qu'on voit, ce qu'on règle », avec L et C au curseur) |
| II. 1. Montage, sens de i, flèches. 2. Équation différentielle | III. L'équation différentielle (en attente : écrite par l'élève, étape par étape) |
| II. 3. Solution. 4. Période propre T₀, dimension. 5. Courbes | IV. La solution du circuit LC et la période propre |
| II. 3. (suite) Constantes U_m et φ | V. Les conditions initiales : U_m et φ |
| V. Méthodes du national (T, L ou C) | VI. Lire un oscillogramme |
| III. L'énergie (échange, conservation en LC) | VII. L'échange d'énergie |
| IV. Amortissement et entretien | VIII. L'amortissement ; IX. L'entretien des oscillations |
| V. Méthodes du national (sujets) | X. Le national 2022 N, joué pas à pas (en attente seulement) ; X/XI. Deux sujets du national |
| Bilan | XI/XII. Bilan du chapitre |

**Écart avec le plan commun.** Dans le cours, les méthodes du national ne sont pas toutes regroupées à la fin. Chaque
méthode est écrite dans la partie où l'on s'en sert : φ en V, T, L et C en VI, l'énergie perdue en VIII. On n'a pas
déplacé de diapositive, puisque seul le cahier est modifié. Chaque méthode commence par « Méthode : » et ses étapes sont
numérotées.

## Le cahier idéal du chapitre

Les valeurs du cours sont : E = 6 V, C = 4 µF, L = 0,1 H, r = 10 Ω, R = 10 Ω (R + r = 20 Ω), T₀ ≈ 4 ms.
Entre crochets : les dessins.

### I. Un condensateur qui se vide dans une bobine
1. But : étudier la décharge d'un condensateur chargé dans une bobine (L, r) et une résistance R en série.
2. Rappel (convention récepteur) : q = C·u_C et i = dq/dt = C·du_C/dt ; q en C, C en F.
3. Rappel (convention récepteur) : u_b = L·di/dt + r·i ; L en henry (H), r en Ω ; i constant : u_b = r·i.
   [**La convention récepteur** : condensateur et bobine, i et la flèche de la tension en sens opposé (nouveau)]
4. Décharge dans R seule (RC) : u_C descend de E vers 0 sans changer de signe.
5. K en 2, décharge dans la bobine (L, r) et R : u_C passe par 0, devient négative, remonte : elle oscille.
   [**Le montage : charge (1), puis décharge (2)** : E, K, C, R, (L, r) (nouveau)] [Décharge : dans R seule, dans une bobine]
6. u_C = 0 : i est maximale ; la bobine s'oppose à la baisse de i : C se recharge en sens inverse (u_C < 0).
7. Définition : sans générateur, u_C change de signe : oscillations libres ; sommets qui baissent : amorties.
   [La maille de décharge : sens de i, flèches u_C, u_R, u_b (déplacée ici, avant le premier usage)]
8. i = C·du_C/dt : u_C diminue → i < 0 ; u_C augmente → i > 0 ; sommet ou creux de u_C → i = 0.
9. À t = 0⁺ : i = 0 (continu dans la bobine), u_R = 0 ; u_C + u_R + u_b = 0 donne u_b(0⁺) = −u_C(0) = −E.

### II. Les trois régimes
1. Pseudo-périodique : « l'amplitude des oscillations diminue » ; T : durée entre deux sommets successifs.
2. Régime apériodique (grande résistance) : u_C revient vers 0 sans osciller. [Pseudo-périodique ou apériodique]
3. Plus R + r est grande, plus l'amortissement est fort : périodique (R + r = 0) → pseudo-périodique → apériodique.
4. Méthode : la courbe la moins amortie a la plus petite R + r (2021 R : 15 Ω → (a) ; 105 Ω → (b)).
5. *(en attente)* L ou C plus grande : oscillations plus lentes ; C × 4 ou L × 4 → T × 2 (L et C font osciller, R + r amortit).

### III. L'équation différentielle
Cours en ligne :
1. Étape 1 — additivité, sans générateur : u_C + u_R + u_b = 0 (le second membre est 0, pas E). [La maille de décharge]
2. Étape 2 — u_C = q/C ; u_R = R·i ; u_b = L·di/dt + r·i : q/C + (R + r)·i + L·di/dt = 0.
3. Étape 3 — i = dq/dt, di/dt = d²q/dt² : L·d²q/dt² + (R + r)·dq/dt + q/C = 0.

Copie en attente (une ligne « À toi », puis la correction) :
1. Étape 1 — additivité, sans générateur : u_C + u_R + u_b = 0.
2. Attention : le second membre vaut 0 et non E : il n'y a plus de générateur dans la maille. [La maille de décharge]
3. Étape 2 — u_C = q/C ; u_R = R·i (loi d'Ohm) ; u_b = L·di/dt + r·i.
4. Donc q/C + (R + r)·i + L·di/dt = 0 ; R + r est la résistance totale du circuit.
5. Étape 3 — i = dq/dt, donc di/dt = d²q/dt².
6. Équation différentielle en q : L·d²q/dt² + (R + r)·dq/dt + q/C = 0.

Puis, dans les deux fichiers :
- En u_C (q = C·u_C) : LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0.
- Circuit LC idéal (R + r = 0) : d²u_C/dt² + u_C/(LC) = 0 ; le terme d'amortissement disparaît.

### IV. La solution du circuit LC et la période propre
1. Rappel : u = U_m·cos(2πt/T) ; U_m : amplitude (hauteur d'un sommet) ; T : période ; cos 0 = 1.
2. Solution : u_C = U_m·cos(2πt/T₀ + φ) ; U_m en V ; T₀ période propre, en s ; φ phase à l'origine, en rad. [Circuit LC : u_C(t)]
3. Rappel : (cos(2πt/T))′ = −(2π/T)·sin(2πt/T) ; elle est nulle aux sommets.
4. du_C/dt = −(2π/T₀)·U_m·sin(2πt/T₀ + φ) ; d²u_C/dt² = −(2π/T₀)²·u_C.
5. Dans l'équation : (2π/T₀)² = 1/(LC), donc T₀ = 2π√(LC) (L en H, C en F, T₀ en s).
6. Dimension : [L]·[C] = [T]², donc √(LC) est un temps : T₀ s'exprime en secondes.
7. Remarque : T₀ ne dépend que de L et de C ; la tension de charge E change U_m, pas T₀.
8. T₀ augmente avec L et avec C : C × 4 (ou L × 4) → T₀ × 2 (4 ms → 8 ms). [C multipliée par 4]
9. Exemple (2022 N) : T₀² = 4π²·L·C ⇒ L = (10⁻²)²/(40 × 5·10⁻⁵) = 0,05 H (π² = 10).

### V. Les conditions initiales : U_m et φ
1. u_C(0) = E et i(0) = 0 : sin φ = 0 et cos φ > 0, donc φ = 0 et U_m = E : u_C = E·cos(2πt/T₀).
2. Lire U_m : hauteur d'un sommet au-dessus de 0. Attention : de sommet à creux, c'est 2·U_m.
3. u_C(0) = U_m·cos φ donne cos φ (3/6 = 0,5) : deux angles possibles, φ = +π/3 ou φ = −π/3.
4. Méthode φ : 1) cos φ = u_C(0)/U_m ; 2) courbe qui monte au départ : φ < 0 ; qui descend : φ > 0. [Le sens de départ choisit φ]
5. q = Q_m·cos(2πt/T₀ + φ), Q_m = C·U_m ; i = dq/dt, I_m = (2π/T₀)·Q_m ; q maximale ⇔ i = 0.

### VI. Lire un oscillogramme
1. Méthode T : 1) n pseudo-périodes entre deux sommets éloignés ; 2) diviser par n (3T ≈ 12 ms → T ≈ 4 ms). [Lire T sur plusieurs sommets]
2. Admis : si l'amortissement est faible, la pseudo-période T ≈ T₀ = 2π√(LC).
3. Méthode L ou C : 1) T₀ en s ; 2) T₀² = 4π²·L·C ; 3) C = T₀²/(4π²·L) ou L = T₀²/(4π²·C), π² = 10.
4. Exemple (2023 N) : T₀ = 4 × 0,5 ms = 2·10⁻³ s ; C = (2·10⁻³)²/(40 × 1) = 10⁻⁷ F = 0,1 µF.

### VII. L'échange d'énergie
1. E_e = ½·C·u_C² (condensateur) ; E_m = ½·L·i² (bobine) ; énergie totale E = E_e + E_m, en J.
2. À t = 0 : u_C = E, i = 0, tout est dans C : E = ½·C·E² = ½ × 4·10⁻⁶ × 6² = 7,2·10⁻⁵ J.
3. u_C = 0 : tout dans la bobine, E = ½·L·I_m² ; i = 0 : tout dans C. L'échange a la période T₀/2. [Échange d'énergie (LC idéal)]
4. LC idéal (R + r = 0) : E = ½·C·u_C² + ½·L·i² = ½·C·E² reste constante.

### VIII. L'amortissement
1. Circuit RLC : E diminue, dissipée en chaleur par effet Joule dans R et r : c'est l'amortissement.
2. d(½·C·u_C²)/dt = u_C·i ; d(½·L·i²)/dt = L·i·di/dt (car d(x²)/dt = 2x·dx/dt).
3. dE/dt = i·(u_C + L·di/dt) = −(R + r)·i² ≤ 0 : E diminue (bobine seule : dE/dt = −r·i²).
4. Méthode : aux sommets i = 0, E = ½·C·u_C² ; |ΔE| = ½·C·(U₁² − U₂²) = 4·10⁻⁵ J de 6 V à 4 V. [L'énergie perdue entre deux sommets]
5. Courbes : E_e part de ½·C·E², E_m part de 0 ; énergie dissipée = E(début) − E(fin).

### IX. L'entretien des oscillations
1. Entretien : un générateur G en série délivre u_G = k·i ; il compense l'énergie perdue par effet Joule.
2. u_C + u_R + u_b = k·i ⇒ L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0 : amortissement nul si k = R + r.
3. k = R + r : oscillations sinusoïdales entretenues, d'amplitude constante, de période T₀ = 2π√(LC). [Oscillations entretenues]

### X. Le national 2022 N, joué pas à pas (copie en attente seulement)
1. 2022 N : C = 50 µF chargé sous 12 V, déchargé dans une bobine (L, r) ; r = 0, puis r ≠ 0.
2. 2.1.1 (r = 0) : u_b + u_C = 0 ⇒ d²u_C/dt² + u_C/(LC) = 0.
3. 2.1.2 : r = 0 → amplitude constante ; u_C(0) = 12 V → c'est la courbe (C₁).
4. 2.1.3.a : d²u_C/dt² = −(2π/T₀)²·u_C ⇒ (2π/T₀)² = 1/(LC) ⇒ T₀ = 2π√(LC).
5. Lecture sur (C₁) : 2T₀ = 20 ms, donc T₀ = 10 ms = 10⁻² s. [**2022 N : la courbe (C₁)** (nouveau)]
6. 2.1.3.b : L = T₀²/(4π²·C) = (10⁻²)²/(40 × 50·10⁻⁶) = 0,05 H.
7. 2.2.1 : E_t = E_e + E_m = ½·C·u_C² + ½·L·i².
8. Lectures : t₀ = 0 : u_C = 12 V, i = 0 ; t₁ = 9 ms : u_C = 6 V, i = 140 mA.
9. 2.2.2 : E₀ = 3,6 mJ ; E₁ ≈ 0,90 + 0,49 = 1,39 mJ ; ΔE = E₁ − E₀ ≈ −2,2 mJ (effet Joule).
10. Entretien : u_G = k·i, k = résistance totale du circuit ; oscillations sinusoïdales, T₀ = 10 ms.
11. Copie : équation ; (C₁) ; T₀ = 2π√(LC) = 10 ms ; L = 0,05 H ; E_t ; ΔE ≈ −2,2 mJ ; u_G = k·i.

### Deux sujets du national
1. 2020 N : T ≈ T₀ = 10 ms ⇒ C = 2,5·10⁻⁶ F ; k₀ = R + r = 100 Ω ; E_t = ½·L·I_m² = 3,2·10⁻⁵ J.
2. 2025 N : T = 4 × 7·10⁻⁵ = 2,8·10⁻⁴ s ; u_C décroît ⇒ i < 0 ; |E_th| = ½·C₀·(U₀² − u_C²) = 2,55·10⁻⁵ J.

### Bilan du chapitre
1. À retenir : u_C + u_R + u_b = 0 ; T₀ = 2π√(LC) ; E = ½·C·u_C² + ½·L·i² ; dE/dt = −(R + r)·i² ; k = R + r.
2. La démarche : régimes → équation → u_C(t) → T₀ → U_m et φ → énergie → amortissement → entretien.

## Découpage en blocs

| Bloc (en ligne) | Lignes | Dessins | Bloc (en attente) | Lignes | Dessins |
|---|---|---|---|---|---|
| lc_s0_b1 | 3 | convention récepteur | lc_s0_b1 | 3 | convention récepteur |
| lc_s1_b1 | 3 | montage ; décharge R / bobine | lc_s1_b1 | 3 | montage ; décharge R / bobine |
| lc_s1_b2 | 3 | maille de décharge | lc_s1_b2 | 3 | maille de décharge |
| lc_s1_b3 | 4 | pseudo / apériodique | lc_s1_b3 | 4 | pseudo / apériodique |
| lc_s2_b1 | 4 | maille de décharge | lc_s2_b0 | 3 | maille de décharge |
| lc_s2_b2a | 3 | u_C(t) du LC | lc_s2_b1 | 4 | — |
| lc_s2_b2 | 3 | — | lc_s2_b1b | 2 | — |
| lc_s2_b3 | 4 | C × 4 | lc_s2_b2a | 3 | u_C(t) du LC |
| lc_s3_b1 | 5 | sens de départ (φ) | lc_s2_b2 | 2 | — |
| lc_s3_b2 | 4 | lire T | lc_s2_b3 | 2 | — |
| lc_s3_b3 | 4 | échange d'énergie | lc_s2_b3b | 2 | C × 4 |
| lc_s4_b1 | 4 | énergie perdue | lc_s3_b1 | 3 | — |
| lc_s4_b2 | 4 | entretenues | lc_s3_b1b | 2 | sens de départ (φ) |
| lc_s4_b3 | 4 | — | lc_s3_b2, lc_s3_b3, lc_s4_b1, lc_s4_b2 | 4 | comme en ligne |
| | | | lc_np_b1, b2, b3 | 3 | 2022 N (C₁) dans b2 |
| | | | lc_np_b4, lc_s4_b3, lc_s4_b4 | 2 | — |

Les lignes font de 50 à 112 caractères, et un bloc de 150 à 460 caractères. Avant, un bloc faisait de 300 à plus de
900 caractères : une ligne du bilan à elle seule en comptait 700.

## Ce qui a été ajouté ou corrigé

- **Une ligne par diapositive**, courte (une idée), qui s'affiche sous le titre numéroté de sa diapositive. Avant, les
  blocs reprenaient le texte complet de chaque diapositive : des lignes de 200 à 700 caractères. La numérotation ne
  s'affichait pas pour les blocs du national et du bilan, dont le nombre de lignes différait du nombre de diapositives.
- **Les conventions sont dessinées avant d'être utilisées.**
  - Nouveau dessin « La convention récepteur » (rappels, bloc lc_s0_b1).
  - La maille fléchée (sens de i, flèches u_C, u_R, u_b) est posée dès le bloc lc_s1_b2. Ce bloc utilise
    i = C·du_C/dt et u_C + u_R + u_b = 0. Le dessin n'apparaissait avant qu'à la partie III.
- **Nouveau dessin du montage** du bac : générateur E, interrupteur K avec ses positions 1 (charge) et 2 (décharge), C,
  R, (L, r).
- **Rien n'est utilisé avant d'être écrit.**
  - L'additivité apparaît en I.9 dans la même ligne que u_b(0⁺), avec la maille dessinée.
  - En IV.9 (2022 N), T₀² = 4π²·L·C est écrit avant d'en tirer L. La formule L = T₀²/(4π²·C) n'arrive qu'en VI.
- **Méthodes numérotées** : régime selon R + r (II.4), φ par la valeur et le sens de départ (V.4), mesure de T
  (VI.1), L ou C depuis T₀ (VI.3), énergie perdue entre deux sommets (VIII.4).
- **Compléments** :
  - « Attention » : 2·U_m de sommet à creux ; le second membre 0 et non E (en attente).
  - « Remarque » : T₀ ne dépend pas de E.
  - « Exemple » : 2022 N, 2023 N.
  - Phrase du bac pour le régime pseudo-périodique.
- **Unités** de L (H), C (F), T₀ (s), U_m (V), φ (rad), E (J).
- **Copie en attente** : les lignes « À toi » de l'équation et leurs corrections ne se répètent plus. La première donne
  l'étape, la seconde le piège ou le résultat. Le national 2022 N joué pas à pas a sa courbe (C₁), qui est un nouveau
  dessin.
- **Doublons supprimés** : le dessin « Circuit LC : u_C(t) » était répété dans le bloc lc_s2_b2. La ligne « Plus R + r
  est grande… » était écrite deux fois dans lc_s1_b3.

## Ce qui reste

- **Blocs de 2 lignes dans la copie en attente** : lc_s2_b1b, lc_s2_b2, lc_s2_b3, lc_s2_b3b, lc_s3_b1b, lc_np_b4,
  lc_s4_b3 et lc_s4_b4. Ces blocs n'ont que deux diapositives. Ajouter une ligne ferait perdre l'affichage « une ligne
  sous chaque titre numéroté ». À l'écran, chaque bloc reste lisible : 2 titres, 2 lignes et parfois un dessin. Si l'on
  veut 3 lignes, il faut regrouper ces blocs, ce qui touche au découpage du cours.
- **Le montage avec le générateur d'entretien G (u_G = k·i)** n'est pas dessiné. Le format ne dessine pas bien ce
  générateur, comme l'avait déjà noté l'audit `physique-ch6-9.md`. Le dessin « Le montage » a 15 éléments ; le
  vérificateur l'accepte avec un avertissement, car un circuit complet ne tient pas en 8.
- **Le rendu sur téléphone n'a pas été contrôlé dans le vrai lecteur.** Le frontend n'est pas installé dans ce conteneur.
  Les dessins ont été relus dans un aperçu SVG. Le bloc le plus chargé est lc_s3_b1 en ligne (5 lignes, 1 dessin,
  457 caractères). Il est deux fois plus court qu'avant, mais reste à regarder en premier.
- Les titres des parties, que le lecteur affiche, ne sont pas ceux du plan commun RC/RL/RLC. Les renommer touche
  `activities[].title`, qui n'est pas un champ du cahier. La correspondance est dans le tableau plus haut.
