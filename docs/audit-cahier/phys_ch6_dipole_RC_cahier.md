# Le cahier de l'élève — Dipôle RC (`phys_ch6_dipole_RC`)

18 novembre 2026, skill `cahier-de-l-eleve`. Cours en ligne `backend/data/courses/phys_ch6_dipole_RC.json` et copie en
attente `backend/data/courses/en_attente/phys_ch6_dipole_RC.json`. Seuls `blocs[].cahier`, `blocs[].cahier_figures`,
`concentration.cahier` et `concentration.cahier_figures` ont été posés (script de pose en un seul passage, format du
fichier gardé). Vérification : `verifier_figures_cahier.py` → 0 erreur sur les deux fichiers (1 avertissement : le
schéma du montage a 20 éléments, il en faut autant pour un montage normalisé avec K, E, R, C, i, u_R, u_C).

## Comment le cahier s'affiche, et donc comment il est numéroté

L'écran du cahier (`TableauCahier`, `cahier.ts`) écrit lui-même le plan : le titre du cours au premier écran, la partie
(`activities[].title`, « I. Le condensateur », « II. … ») en y entrant, puis le titre de chaque diapositive numéroté
dans sa partie (« 2. q = C·u_C »). Quand un bloc a **une ligne par diapositive**, chaque ligne s'écrit sous le titre de
sa diapositive : le plan numéroté est continu d'un bloc à l'autre, sans rien ajouter. Le cahier est donc écrit ainsi :
**une entrée par diapositive** (1 ou 2 phrases courtes), la même dans la bulle de la diapositive et dans l'étape de fin de
bloc. Les lignes ne portent pas de numéros romains à elles (ils feraient double emploi avec ceux des parties, et les
contrediraient).

## Le plan parallèle RC / RL / RLC

Les parties du cours RC et du cours RL sont déjà parallèles (I à X). Le squelette commun demandé se lit ainsi dans le
cours RC :

| Squelette commun | Parties du cours RC (en ligne) |
|---|---|
| I. Le dipôle : 1. description et symbole ; 2. convention récepteur, q = C·u_C, i = dq/dt ; 3. C et associations | I. Le condensateur ; II. Associer des condensateurs, charger à courant constant |
| II. Échelon montant : 1. montage, sens de i, flèches ; 2. équation ; 3. solution ; 4. τ ; 5. courbes | III. Le dipôle RC soumis à un échelon ; IV. L'équation différentielle ; V. La solution et les quatre courbes ; VI (début). τ |
| III. Échelon descendant (décharge) | VI (fin). La décharge |
| IV. Méthodes du national : Méthode 1 tangente, 2 63 %/37 %, 3 courbe sans le temps, 4 trouver R et C | VII. Lire les courbes |
| V. Énergie | VIII. L'énergie emmagasinée |
| (sujets, bilan) | IX. Deux sujets du national ; X. Bilan |

Les méthodes portent le même numéro dans RC, RL (et RLC pour ce qui s'y applique) : « Méthode 1 (tangente) »,
« Méthode 2 (63 %) », « Méthode 3 (courbe sans le temps) », « Méthode 4 (R et C) ». Écart : dans les deux fichiers, la
Méthode 4 est enseignée avant la Méthode 3 (ordre des diapositives, que le cahier ne change pas). Dans la partie V,
les courbes (valeurs à 0, τ, 5τ) viennent avant l'étude de τ (partie VI) : ordre du cours, gardé.

**Copie en attente** : mêmes textes, autre ordre : les étapes de l'équation sont écrites une à une (« Étape 1, 2, 3 »)
avant la rédaction complète ; τ et sa lecture (Méthodes 1 et 2) viennent juste après la solution ; la décharge vient
après les courbes sans le temps ; le national 2022 N est joué pas à pas (partie IX). Le seul texte propre à la copie
est celui de `rc_e2_etablir` (« Rédaction complète… », puisque les trois étapes sont déjà écrites).

## Ce qui a été ajouté ou corrigé

- **Conventions dessinées avant usage** : nouveau schéma « Convention récepteur » (conducteur ohmique, i, flèche de
  u_AB) dès la loi d'Ohm ; nouveau schéma « Le condensateur en convention récepteur » (i entre par A, +q / −q, flèche
  de u_C = u_AB) sur q = C·u_C ; le schéma du montage est refait **avec l'interrupteur K à deux positions** (1 : charge,
  2 : décharge), E et sa borne +, le sens de i et les flèches de u_R et u_C.
- **Nouvelles courbes** : « Influence de R sur la charge » (E = 12 V, C = 220 µF, τ = 0,22 s puis 0,44 s, les valeurs du
  cours) ; « 2022 N : u_C(t) et la tangente (T) » (τ = 50 ms, 7,56 V) dans la copie en attente.
- **Définitions encadrées** (« Définition : ») : condensateur, équation différentielle ; **méthodes numérotées** :
  lire C (courant constant), établir l'équation, vérifier une solution, Méthodes 1 à 4 du national.
- **Compléments du national** (exploration `dipole_RC`, `erreurs_examen`) : « Attention » sur la série (inverse des
  résistances), la forme demandée de l'équation, le signe de la dérivée, la projection sur la courbe et non sur la
  tangente, le carré de l'énergie, le changement de sens de i à la décharge ; unités partout (Ω, F, C, s, J).
- **Rien avant d'être écrit** : l'additivité des rappels ne cite plus u_C (le condensateur n'est pas encore vu) ;
  l'exemple des préfixes n'emploie plus le farad ; u_C est définie (« la tension du condensateur ») à sa première
  apparition.
- **Taille** : une entrée par diapositive (≤ ~190 caractères), 2 à 5 entrées et 0 à 2 dessins par bloc ; la bulle du
  bilan, qui faisait 6 lignes, tient en une.

## Ce qui reste

- Les blocs de 2 diapositives n'ont que 2 entrées (la règle « 3 à 6 lignes » compte alors les phrases, pas les entrées).
- La fiche bilan (`rc_b1_bilan`) n'est qu'une ligne de rappel : la vraie fiche reste celle du cours (hors cahier).
- Le rendu sur téléphone n'a pas été capturé dans l'application (les dessins ont été rendus avec `FigureCahier.tsx`
  dans Chromium et relus).

## Le cahier, partie par partie (cours en ligne)

### I. Le condensateur

1. **La carte du chapitre : un réservoir de charges** — Dipôle RC : un conducteur ohmique (R) et un condensateur (C) en série. Plan : condensateur, échelon, équation différentielle, solution, τ = R·C, courbes, énergie.
2. **Rappel : le courant électrique** — Rappel : l'intensité i (en ampère, A) se mesure avec un ampèremètre branché en série ; sens conventionnel : du + vers le − à l'extérieur du générateur.
3. **Rappel : la tension électrique** — Rappel : la tension u_AB (en volt, V) se représente par une flèche de B vers A ; voltmètre branché en dérivation. Deux points d'un même fil : u = 0.
   ⟶ *fin du bloc `rc_s0_b1`*
4. **Rappel : la loi d’Ohm** — Convention récepteur : la flèche de la tension est opposée au sens de i. Loi d'Ohm (convention récepteur) : u_R = R·i, R en ohm (Ω).
   *Dessin — Convention récepteur* : La flèche de u_AB (de B vers A) est opposée au sens de i : u_AB = R·i.
5. **Rappel : la loi d’additivité des tensions** — Loi d'additivité des tensions : u_AC = u_AB + u_BC ; en série, la tension du générateur est la somme des tensions des dipôles.
6. **Rappel : les puissances de dix** — Préfixes : m = 10⁻³ ; µ = 10⁻⁶ ; n = 10⁻⁹. Exemple : 50 ms = 50·10⁻³ s = 5·10⁻² s.
   ⟶ *fin du bloc `rc_s0_b2`*
7. **Deux plaques et un isolant** — Définition : un condensateur est formé de deux armatures conductrices séparées par un isolant (diélectrique). Symbole : deux traits parallèles.
   *Dessin — Le condensateur* : Deux armatures conductrices A et B séparées par un isolant ; dans un circuit : deux traits parallèles.
8. **Avant de fermer K : que va-t-on mesurer ?** — Expérience : générateur E, interrupteur K et condensateur en série ; ampèremètre (en série) pour i, voltmètre (en dérivation) pour u_C, la tension du condensateur. K ouvert : i = 0, u_C = 0.
9. **Fermons K : que font les aiguilles ?** — K fermé : i passe puis s'annule ; u_C monte jusqu'à E. Donc le condensateur se charge et le courant de charge ne dure pas.
   ⟶ *fin du bloc `rc_s1_b1`*
10. **Les électrons font le tour** — Les électrons ne traversent pas l'isolant : ils quittent une armature et arrivent sur l'autre. q_A = q, q_B = −q : q est la charge de l'armature par laquelle entre i.
11. **q = C·u_C** — Convention récepteur (i entre par A, u_C = u_AB) : q = C·u_C ; q en coulomb (C), C capacité en farad (F), C > 0. Exemple : 10 µF sous 2 V : q = 2·10⁻⁵ C.
   *Dessin — Le condensateur en convention récepteur* : i entre par l'armature A (charge q) ; u_C = u_AB est fléchée de B vers A : q = C·u_C.
12. **Rappel : la dérivée, c’est une pente** — Rappel : la dérivée en un point est la pente de la tangente à la courbe en ce point ; courbe plate : dérivée nulle.
   ⟶ *fin du bloc `rc_s1_b2a`*
13. **L'intensité, c'est la pente de q(t)** — i = dq/dt : i est la pente de la tangente à q(t) ; i > 0 quand q augmente (charge), i < 0 quand q diminue (décharge).
   *Dessin — i, pente de q(t)* : i = dq/dt est la pente de la tangente à q(t) : q monte, i > 0 ; à la fin la tangente est horizontale, i = 0.
14. **i = C·du_C/dt** — Comme q = C·u_C et que C est constante : i = dq/dt = C·du_C/dt (convention récepteur).
   ⟶ *fin du bloc `rc_s1_b2`*

### II. Associer des condensateurs, charger à courant constant

1. **Deux condensateurs côte à côte** — En parallèle (même tension) : q = q₁ + q₂, donc C_eq = C₁ + C₂. Intérêt : augmenter la capacité.
2. **Deux condensateurs l'un après l'autre** — En série (même charge) : u = u₁ + u₂, donc 1/C_eq = 1/C₁ + 1/C₂ ; pour deux : C_eq = C₁·C₂/(C₁ + C₂), plus petite que chacune. Attention : c'est l'inverse des résistances.
3. **Un générateur qui impose le courant** — Générateur de courant (I₀ constante), condensateur déchargé : q = I₀·t, donc u_C = (I₀/C)·t : droite passant par l'origine.
4. **Lire C sur la droite** — Méthode (lire C) : 1) pente k = Δu_C/Δt entre deux points lus ; 2) k = I₀/C, donc C = I₀/k. Exemple 2025 N : I₀ = 1 µA, k = 1 V/s : C = 1 µF.
   *Dessin — Charge à courant constant* : u_C = (I₀/C)·t : droite par l'origine ; k = Δu_C/Δt = 1 V/s, donc C = I₀/k = 10⁻⁶/1 = 1 µF (2025 N).
   ⟶ *fin du bloc `rc_s1_b3`*

### III. Le dipôle RC soumis à un échelon de tension

1. **Le montage à interrupteur K** — Échelon de tension montant : la tension passe brusquement de 0 à E (K en 1 : charge) ; échelon descendant : de E à 0 (K en 2 : décharge).
2. **Flécher et brancher l'acquisition** — Convention récepteur : u_R et u_C fléchées en sens inverse de i. Acquisition : voie à la tête de la flèche, masse à l'autre borne ; u_R = R·i a la forme de i.
   *Dessin — Le montage RC fléché* : K en 1 : charge (E, R, C en série) ; K en 2 : décharge dans R. Flèches de u_R et u_C opposées à i.
3. **K en position 1 : que fait u_C ?** — Charge : u_C monte de 0 vers E, vite au début puis de plus en plus lentement ; u_C ne dépasse pas E.
4. **Régime transitoire, régime permanent** — Régime transitoire : u_C varie ; régime permanent : u_C = E et i = 0. Remarque : u_C est continue, u_C(0) = 0 ; i peut sauter : i(0) = E/R.
   ⟶ *fin du bloc `rc_s2_b1`*

### IV. L'équation différentielle

1. **Une équation avec une dérivée** — Définition : une équation différentielle est une relation entre une fonction (ici u_C(t)) et sa dérivée (du_C/dt).
2. **Établir l'équation de u_C** — Méthode (établir l'équation) : 1) additivité : u_R + u_C = E ; 2) Ohm : u_R = R·i ; 3) i = C·du_C/dt ; 4) RC·du_C/dt + u_C = E.
3. **Deux écritures de la même équation** — Autre écriture (on divise par RC) : du_C/dt + (1/RC)·u_C = E/(RC). Attention : donner la forme demandée par l'énoncé.
4. **L'équation de q** — En q (u_C = q/C et i = dq/dt) : R·dq/dt + q/C = E, soit RC·dq/dt + q = C·E.
   ⟶ *fin du bloc `rc_s2_b2`*
5. **Les équations de u_R et de i** — On dérive u_R + u_C = E (E constante), avec du_C/dt = i/C : RC·du_R/dt + u_R = 0 ; puis u_R = R·i : RC·di/dt + i = 0.
6. **La décharge : sans générateur** — Décharge (K en 2, sans générateur) : u_R + u_C = 0, donc RC·du_C/dt + u_C = 0 ; i = C·du_C/dt < 0.
7. **Le tableau des huit équations** — Second membre — charge : E pour u_C, C·E pour q, 0 pour u_R et i ; décharge : 0 pour les quatre grandeurs.
8. **Au national : établir une ED** — Exemple 2023 R : E = R·i + q/C et i = dq/dt, donc RC·dq/dt + q = C·E.
   ⟶ *fin du bloc `rc_s2_b3`*

### V. La solution et les quatre courbes

1. **Rappel : la fonction exponentielle** — Rappel : e⁰ = 1 ; e^(−t/τ) diminue vers 0 sans jamais s'annuler ; e⁻¹ ≈ 0,37 et 1 − e⁻¹ ≈ 0,63.
2. **Dériver une exponentielle** — Dérivée : d(e^(−t/τ))/dt = −(1/τ)·e^(−t/τ). Attention au signe − et au facteur 1/τ.
3. **Trouver A et τ : dériver, remplacer** — On cherche u_C = A(1 − e^(−t/τ)) : du_C/dt = (A/τ)·e^(−t/τ) ; on remplace : RC·(A/τ)·e^(−t/τ) + A − A·e^(−t/τ) = E.
   ⟶ *fin du bloc `rc_s3_b0`*
4. **Factoriser et conclure** — A·e^(−t/τ)·(RC/τ − 1) + A = E pour tout t, donc τ = R·C et A = E. Solution de la charge : u_C(t) = E·(1 − e^(−t/τ)).
5. **La forme A + B·e^(−αt)** — Forme u_C = A + B·e^(−αt) : pour tout t, α = 1/(RC) et A = E ; condition initiale u_C(0) = A + B = 0, donc B = −E.
6. **Vérifier qu'une expression est solution** — Méthode (vérifier une solution) : 1) dériver ; 2) remplacer dans l'équation ; 3) obtenir une égalité vraie pour tout t ; 4) conclure.
   ⟶ *fin du bloc `rc_s3_b1`*
7. **Le tableau avant la courbe** — u_C(0) = 0 ; u_C(τ) = E(1 − e⁻¹) ≈ 0,63·E ; u_C(5τ) ≈ 0,99·E : le régime permanent est atteint au bout de 5τ.
   *Dessin — Charge : u_C(t)* : E = 12 V, τ = R·C = 0,22 s : u_C(τ) = 0,63·E = 7,56 V ; à 5τ, u_C ≈ 0,99·E : régime permanent.
8. **q(t) et i(t) pendant la charge** — Charge : q(t) = C·E·(1 − e^(−t/τ)) ; i = C·du_C/dt = (E/R)·e^(−t/τ), car τ = R·C ; I₀ = i(0) = E/R.
9. **u_R(t) et les quatre courbes** — u_R = R·i = E·e^(−t/τ) ; u_R + u_C = E : u_C et q montent vers leur valeur finale, u_R et i descendent vers 0.
   ⟶ *fin du bloc `rc_s3_b2`*

### VI. La constante de temps et la décharge

1. **τ est un temps** — τ = R·C est un temps : [R] = [U]/[I] et [C] = [I]·[T]/[U], donc [τ] = [T] ; τ en seconde (s).
2. **Plus de R, plus lent** — Si R augmente, τ = R·C augmente : la charge est plus lente. Exemple : R = 2 kΩ, C = 220 µF : τ = 2·10³ × 220·10⁻⁶ = 0,44 s.
   *Dessin — Influence de R sur la charge* : E = 12 V, C = 220 µF : R = 1 kΩ (τ = 0,22 s) puis 2 kΩ (τ = 0,44 s) ; la charge est plus lente, la valeur finale reste E.
3. **Plus de C, plus lent aussi** — Si C double (R fixe), τ double : la charge et la décharge sont plus lentes ; la valeur finale ne change pas.
   ⟶ *fin du bloc `rc_s3_b3a`*
4. **La décharge : u_C = E·e^(−t/τ)** — Décharge : u_C = A·e^(−t/τ) dans RC·du_C/dt + u_C = 0 donne τ = R·C ; u_C(0) = E donne A = E : u_C(t) = E·e^(−t/τ).
   *Dessin — Décharge : u_C(t)* : u_C part de E (u_C est continue) et tend vers 0 : u_C = E·e^(−t/τ) ; u_C(τ) = 0,37·E.
5. **u_C ne saute pas, i change de sens** — À la bascule, nouvelle origine t = 0. u_C est continue : u_C(0) = E ; i saute : i(0) = −E/R. Attention : le courant change de sens.
6. **q(t), i(t) et u_R(t) pendant la décharge** — Décharge : q = C·E·e^(−t/τ) ; i = −(E/R)·e^(−t/τ) ; u_R = −E·e^(−t/τ) ; u_C(τ) ≈ 0,37·E.
   ⟶ *fin du bloc `rc_s3_b3`*

### VII. Lire les courbes

1. **τ par la tangente à l'origine** — Méthode 1 (tangente) : la tangente à l'origine coupe l'asymptote u_C = E au point d'abscisse t = τ ; lire τ avec l'unité de l'axe.
   *Dessin — τ par la tangente à l'origine* : La tangente à l'origine coupe l'asymptote u_C = E au point d'abscisse t = τ (ici 0,22 s).
2. **τ par les 63 %** — Méthode 2 (63 %) : 1) calculer 0,63·E ; 2) horizontale jusqu'à la courbe ; 3) projeter sur l'axe des temps : τ. Attention : sur la courbe, pas sur la tangente.
3. **Courbes qui descendent : 37 %** — Courbe qui descend (décharge, i, u_R) : la tangente à l'origine coupe l'axe des temps en t = τ ; à τ, il reste 37 % de la valeur initiale.
   *Dessin — Courbe qui descend : i(t)* : I₀ = E/R = 12 mA ; la tangente à l'origine coupe l'axe des temps à τ ; i(τ) = 0,37·I₀ = 4,44 mA.
4. **De τ à R et C** — Méthode 4 (R et C) : R = E/I₀ (I₀ lu à t = 0) ou C = Q_m/E ; puis C = τ/R ou R = τ/C ; expression, application numérique, unité.
   ⟶ *fin du bloc `rc_s4_b1`*
5. **Une courbe sans le temps : du_C/dt = f(u_C)** — Méthode 3 (courbe sans le temps) : du_C/dt = −u_C/(RC) + E/(RC), droite de pente a = −1/(RC), donc C = −1/(R·a) ; elle coupe l'axe des u_C en E.
   *Dessin — La droite du_C/dt = f(u_C)* : Pente a = −1/(RC) < 0 : a = −1000/12 ≈ −83,3 s⁻¹ ; R = 1 kΩ, donc C = −1/(R·a) = 12 µF (2021 N).
6. **q = f(u) : la pente est C** — q = f(u) : droite de pente C = Δq/Δu ; en parallèle, C_eq = C₁ + C₂ donne C₂ = C_eq − C₁.

### VIII. L'énergie emmagasinée

1. **L'énergie du condensateur** — Énergie électrique emmagasinée : E_e = ½·C·u_C² (E_e en J, C en F, u_C en V). Usage : flash d'appareil photo.
2. **Calculer l'énergie** — E_e = ½·C·u_C² = q²/(2C) ; fin de charge : E_e = ½·C·E². Attention au carré : si u_C double, E_e est multipliée par 4.
   ⟶ *fin du bloc `rc_s4_b2`*

### IX. Deux sujets du national

1. **Un sujet complet : la charge (2019 N)** — 2019 N : RC·dq/dt + q = C·E ; q = A(1 − e^(−αt)) avec A = C·E, α = 1/(RC) ; C = Q/E = 10⁻⁴/10 = 10 µF ; R = τ/C = 100 Ω.
2. **Un sujet complet : l'intensité (2021 R)** — 2021 R : R₁C·di/dt + i = 0 ; i = I₀·e^(−t/τ) avec τ = R₁C ; R₁ = E/i(0) = 6/0,05 = 120 Ω ; C = τ/R₁ = 100 µF.

### X. Bilan du chapitre

1. **Ce qu'il faut retenir** — À retenir : q = C·u_C ; i = C·du_C/dt ; RC·du_C/dt + u_C = E ; u_C = E(1 − e^(−t/τ)) ; τ = R·C ; 63 % / 37 % ; E_e = ½·C·u_C².
2. **La carte du chapitre et la suite** — Carte : q = C·u_C → équation → solution → τ = R·C → lire τ → énergie. Suite : dipôle RL (τ = L/R), puis circuit RLC.
   ⟶ *fin du bloc `rc_s4_b3`*

## Découpage en blocs — cours en ligne

| Bloc | Diapositives | Lignes | Dessins |
|---|---|---|---|
| `rc_s0_b1` | rc_o1_carte, rc_rp1_courant, rc_rp2_tension | 3 | — |
| `rc_s0_b2` | rc_rp3_ohm, rc_rp4_additivite, rc_rp5_puissances | 3 | Convention récepteur |
| `rc_s1_b1` | rc_c1_plaques, rc_c2a_principe, rc_c2_aiguilles | 3 | Le condensateur |
| `rc_s1_b2a` | rc_c3_electrons, rc_c4_capacite, rc_rp6_derivee | 3 | Le condensateur en convention récepteur |
| `rc_s1_b2` | rc_c5_intensite, rc_c6_relation | 2 | i, pente de q(t) |
| `rc_s1_b3` | rc_a1_parallele, rc_a2_serie, rc_g1_generateur, rc_g2_pente | 4 | Charge à courant constant |
| `rc_s2_b1` | rc_m1_montage, rc_m2_acquisition, rc_m3_charge, rc_m4_regimes | 4 | Le montage RC fléché |
| `rc_s2_b2` | rc_e1_equation, rc_e2_etablir, rc_e3_formes, rc_e4_q | 4 | — |
| `rc_s2_b3` | rc_e5_uR_i, rc_e6_decharge, rc_e7_tableau, rc_e8_national | 4 | — |
| `rc_s3_b0` | rc_rp7_exponentielle, rc_s1_derivee, rc_s2_remplacer | 3 | — |
| `rc_s3_b1` | rc_s3_factoriser, rc_s4_condition, rc_s5_verifier | 3 | — |
| `rc_s3_b2` | rc_s6_tableau, rc_s7_q_i, rc_s8_quatre | 3 | Charge : u_C(t) |
| `rc_s3_b3a` | rc_t1_dimension, rc_t2_influence, rc_t3_C | 3 | Influence de R sur la charge |
| `rc_s3_b3` | rc_d1_decharge, rc_d2_continuite, rc_d3_decharge_qi | 3 | Décharge : u_C(t) |
| `rc_s4_b1` | rc_l1_tangente, rc_l2_pourcent, rc_l3_descente, rc_l4_deduire | 4 | τ par la tangente à l'origine ; Courbe qui descend : i(t) |
| `rc_s4_b2` | rc_l5_pente, rc_l6_capacite, rc_l7_energie, rc_l8_calcul | 4 | La droite du_C/dt = f(u_C) |
| `rc_s4_b3` | rc_n1_2019, rc_n2_2021R, rc_b1_bilan, rc_b2_carte | 4 | — |

## Découpage en blocs — copie en attente

| Bloc | Diapositives | Lignes | Dessins |
|---|---|---|---|
| `rc_s0_b1` | rc_o1_carte, rc_rp1_courant, rc_rp2_tension | 3 | — |
| `rc_s0_b2` | rc_rp3_ohm, rc_rp4_additivite, rc_rp5_puissances | 3 | Convention récepteur |
| `rc_s1_b1` | rc_c1_plaques, rc_c2a_principe, rc_c2_aiguilles | 3 | Le condensateur |
| `rc_s1_b2a` | rc_c3_electrons, rc_c4_capacite, rc_rp6_derivee | 3 | Le condensateur en convention récepteur |
| `rc_s1_b2` | rc_c5_intensite, rc_c6_relation | 2 | i, pente de q(t) |
| `rc_s1_b3` | rc_a1_parallele, rc_a2_serie, rc_g1_generateur, rc_g2_pente | 4 | Charge à courant constant |
| `rc_s2_b1` | rc_m1_montage, rc_m2_acquisition, rc_m3_charge, rc_m4_regimes, rc_m5_observer | 5 | Le montage RC fléché |
| `rc_s2_b2` | rc_e1_equation, rc_e2a_additivite, rc_e2b_uR, rc_e2c_equation | 4 | — |
| `rc_s2_b2b` | rc_e2_etablir, rc_e3_formes, rc_e4_q | 3 | — |
| `rc_s2_b3` | rc_e5_uR_i, rc_e8_national | 2 | — |
| `rc_s3_b0` | rc_rp7_exponentielle, rc_s1_derivee, rc_s2_remplacer | 3 | — |
| `rc_s3_b1` | rc_s3_factoriser, rc_s4_condition, rc_s5_verifier | 3 | — |
| `rc_s3_b2` | rc_s6_tableau, rc_s7_q_i, rc_s8_quatre | 3 | Charge : u_C(t) |
| `rc_s4_b1` | rc_t1_dimension, rc_l1_tangente, rc_l2_pourcent | 3 | τ par la tangente à l'origine |
| `rc_s3_b3a` | rc_t2_influence, rc_t3_C, rc_l4_deduire | 3 | Influence de R sur la charge |
| `rc_s4_b2` | rc_l5_pente, rc_l6_capacite | 2 | La droite du_C/dt = f(u_C) |
| `rc_s3_b3` | rc_d2_continuite, rc_e6_decharge, rc_d1_decharge | 3 | Décharge : u_C(t) |
| `rc_s3_b4` | rc_d3_decharge_qi, rc_l3_descente, rc_e7_tableau | 3 | Courbe qui descend : i(t) |
| `rc_s4_b2b` | rc_l7_energie, rc_l8_calcul | 2 | — |
| `rc_np_b1` | rc_np0_sujet, rc_np1_equation, rc_np2_courant, rc_np3_lire | 4 | — |
| `rc_np_b2` | rc_np4_R, rc_np5_tangente, rc_np6_pourcent | 3 | 2022 N : u_C(t) et la tangente (T) |
| `rc_np_b3` | rc_np7_C, rc_np8_energie, rc_np9_copie | 3 | — |
| `rc_s4_b3` | rc_n1_2019, rc_n2_2021R | 2 | — |
| `rc_s4_b4` | rc_b1_bilan, rc_b2_carte | 2 | — |

## La copie en attente, dans son ordre

### I. Les outils et le condensateur

1. **La carte du chapitre : un réservoir de charges** — Dipôle RC : un conducteur ohmique (R) et un condensateur (C) en série. Plan : condensateur, échelon, équation différentielle, solution, τ = R·C, courbes, énergie.
2. **Rappel : le courant électrique** — Rappel : l'intensité i (en ampère, A) se mesure avec un ampèremètre branché en série ; sens conventionnel : du + vers le − à l'extérieur du générateur.
3. **Rappel : la tension électrique** — Rappel : la tension u_AB (en volt, V) se représente par une flèche de B vers A ; voltmètre branché en dérivation. Deux points d'un même fil : u = 0.
   ⟶ *fin du bloc `rc_s0_b1`*
4. **Rappel : la loi d’Ohm** — Convention récepteur : la flèche de la tension est opposée au sens de i. Loi d'Ohm (convention récepteur) : u_R = R·i, R en ohm (Ω).
   *Dessin — Convention récepteur* : La flèche de u_AB (de B vers A) est opposée au sens de i : u_AB = R·i.
5. **Rappel : la loi d’additivité des tensions** — Loi d'additivité des tensions : u_AC = u_AB + u_BC ; en série, la tension du générateur est la somme des tensions des dipôles.
6. **Rappel : les puissances de dix** — Préfixes : m = 10⁻³ ; µ = 10⁻⁶ ; n = 10⁻⁹. Exemple : 50 ms = 50·10⁻³ s = 5·10⁻² s.
   ⟶ *fin du bloc `rc_s0_b2`*
7. **Deux plaques et un isolant** — Définition : un condensateur est formé de deux armatures conductrices séparées par un isolant (diélectrique). Symbole : deux traits parallèles.
   *Dessin — Le condensateur* : Deux armatures conductrices A et B séparées par un isolant ; dans un circuit : deux traits parallèles.
8. **Avant de fermer K : que va-t-on mesurer ?** — Expérience : générateur E, interrupteur K et condensateur en série ; ampèremètre (en série) pour i, voltmètre (en dérivation) pour u_C, la tension du condensateur. K ouvert : i = 0, u_C = 0.
9. **Fermons K : que font les aiguilles ?** — K fermé : i passe puis s'annule ; u_C monte jusqu'à E. Donc le condensateur se charge et le courant de charge ne dure pas.
   ⟶ *fin du bloc `rc_s1_b1`*
10. **Les électrons font le tour** — Les électrons ne traversent pas l'isolant : ils quittent une armature et arrivent sur l'autre. q_A = q, q_B = −q : q est la charge de l'armature par laquelle entre i.
11. **q = C·u_C** — Convention récepteur (i entre par A, u_C = u_AB) : q = C·u_C ; q en coulomb (C), C capacité en farad (F), C > 0. Exemple : 10 µF sous 2 V : q = 2·10⁻⁵ C.
   *Dessin — Le condensateur en convention récepteur* : i entre par l'armature A (charge q) ; u_C = u_AB est fléchée de B vers A : q = C·u_C.
12. **Rappel : la dérivée, c’est une pente** — Rappel : la dérivée en un point est la pente de la tangente à la courbe en ce point ; courbe plate : dérivée nulle.
   ⟶ *fin du bloc `rc_s1_b2a`*
13. **L'intensité, c'est la pente de q(t)** — i = dq/dt : i est la pente de la tangente à q(t) ; i > 0 quand q augmente (charge), i < 0 quand q diminue (décharge).
   *Dessin — i, pente de q(t)* : i = dq/dt est la pente de la tangente à q(t) : q monte, i > 0 ; à la fin la tangente est horizontale, i = 0.
14. **i = C·du_C/dt** — Comme q = C·u_C et que C est constante : i = dq/dt = C·du_C/dt (convention récepteur).
   ⟶ *fin du bloc `rc_s1_b2`*

### II. Associer des condensateurs, charger à courant constant

1. **Deux condensateurs côte à côte** — En parallèle (même tension) : q = q₁ + q₂, donc C_eq = C₁ + C₂. Intérêt : augmenter la capacité.
2. **Deux condensateurs l'un après l'autre** — En série (même charge) : u = u₁ + u₂, donc 1/C_eq = 1/C₁ + 1/C₂ ; pour deux : C_eq = C₁·C₂/(C₁ + C₂), plus petite que chacune. Attention : c'est l'inverse des résistances.
3. **Un générateur qui impose le courant** — Générateur de courant (I₀ constante), condensateur déchargé : q = I₀·t, donc u_C = (I₀/C)·t : droite passant par l'origine.
4. **Lire C sur la droite** — Méthode (lire C) : 1) pente k = Δu_C/Δt entre deux points lus ; 2) k = I₀/C, donc C = I₀/k. Exemple 2025 N : I₀ = 1 µA, k = 1 V/s : C = 1 µF.
   *Dessin — Charge à courant constant* : u_C = (I₀/C)·t : droite par l'origine ; k = Δu_C/Δt = 1 V/s, donc C = I₀/k = 10⁻⁶/1 = 1 µF (2025 N).
   ⟶ *fin du bloc `rc_s1_b3`*

### III. Le montage : ce qu'on voit, ce qu'on règle

1. **Le montage à interrupteur K** — Échelon de tension montant : la tension passe brusquement de 0 à E (K en 1 : charge) ; échelon descendant : de E à 0 (K en 2 : décharge).
2. **Flécher et brancher l'acquisition** — Convention récepteur : u_R et u_C fléchées en sens inverse de i. Acquisition : voie à la tête de la flèche, masse à l'autre borne ; u_R = R·i a la forme de i.
   *Dessin — Le montage RC fléché* : K en 1 : charge (E, R, C en série) ; K en 2 : décharge dans R. Flèches de u_R et u_C opposées à i.
3. **K en position 1 : que fait u_C ?** — Charge : u_C monte de 0 vers E, vite au début puis de plus en plus lentement ; u_C ne dépasse pas E.
4. **Régime transitoire, régime permanent** — Régime transitoire : u_C varie ; régime permanent : u_C = E et i = 0. Remarque : u_C est continue, u_C(0) = 0 ; i peut sauter : i(0) = E/R.
5. **R et C au curseur : la charge plus lente ou plus rapide ?** — Observation : si R ou si C augmente, la charge est plus lente ; la valeur finale reste E.
   ⟶ *fin du bloc `rc_s2_b1`*

### IV. L'équation différentielle, écrite pas à pas

1. **Une équation avec une dérivée** — Définition : une équation différentielle est une relation entre une fonction (ici u_C(t)) et sa dérivée (du_C/dt).
2. **À toi : la première ligne** — Étape 1 (loi d'additivité des tensions) : u_R + u_C = E.
3. **À toi : u_R avec u_C** — Étape 2 (loi d'Ohm, puis i = C·du_C/dt) : u_R = R·i = RC·du_C/dt.
4. **À toi : l'équation de u_C** — Étape 3 : RC·du_C/dt + u_C = E, l'équation différentielle de la charge.
   ⟶ *fin du bloc `rc_s2_b2`*
5. **La rédaction complète, comme le corrigé** — Rédaction complète : u_R + u_C = E ; u_R = R·i et i = C·du_C/dt ; donc RC·du_C/dt + u_C = E. Attention : toutes les lignes sont exigées.
6. **Deux écritures de la même équation** — Autre écriture (on divise par RC) : du_C/dt + (1/RC)·u_C = E/(RC). Attention : donner la forme demandée par l'énoncé.
7. **L'équation de q** — En q (u_C = q/C et i = dq/dt) : R·dq/dt + q/C = E, soit RC·dq/dt + q = C·E.
   ⟶ *fin du bloc `rc_s2_b2b`*
8. **Les équations de u_R et de i** — On dérive u_R + u_C = E (E constante), avec du_C/dt = i/C : RC·du_R/dt + u_R = 0 ; puis u_R = R·i : RC·di/dt + i = 0.
9. **Au national : établir une ED** — Exemple 2023 R : E = R·i + q/C et i = dq/dt, donc RC·dq/dt + q = C·E.
   ⟶ *fin du bloc `rc_s2_b3`*

### V. La solution et les quatre courbes

1. **Rappel : la fonction exponentielle** — Rappel : e⁰ = 1 ; e^(−t/τ) diminue vers 0 sans jamais s'annuler ; e⁻¹ ≈ 0,37 et 1 − e⁻¹ ≈ 0,63.
2. **Dériver une exponentielle** — Dérivée : d(e^(−t/τ))/dt = −(1/τ)·e^(−t/τ). Attention au signe − et au facteur 1/τ.
3. **Trouver A et τ : dériver, remplacer** — On cherche u_C = A(1 − e^(−t/τ)) : du_C/dt = (A/τ)·e^(−t/τ) ; on remplace : RC·(A/τ)·e^(−t/τ) + A − A·e^(−t/τ) = E.
   ⟶ *fin du bloc `rc_s3_b0`*
4. **Factoriser et conclure** — A·e^(−t/τ)·(RC/τ − 1) + A = E pour tout t, donc τ = R·C et A = E. Solution de la charge : u_C(t) = E·(1 − e^(−t/τ)).
5. **La forme A + B·e^(−αt)** — Forme u_C = A + B·e^(−αt) : pour tout t, α = 1/(RC) et A = E ; condition initiale u_C(0) = A + B = 0, donc B = −E.
6. **Vérifier qu'une expression est solution** — Méthode (vérifier une solution) : 1) dériver ; 2) remplacer dans l'équation ; 3) obtenir une égalité vraie pour tout t ; 4) conclure.
   ⟶ *fin du bloc `rc_s3_b1`*
7. **Le tableau avant la courbe** — u_C(0) = 0 ; u_C(τ) = E(1 − e⁻¹) ≈ 0,63·E ; u_C(5τ) ≈ 0,99·E : le régime permanent est atteint au bout de 5τ.
   *Dessin — Charge : u_C(t)* : E = 12 V, τ = R·C = 0,22 s : u_C(τ) = 0,63·E = 7,56 V ; à 5τ, u_C ≈ 0,99·E : régime permanent.
8. **q(t) et i(t) pendant la charge** — Charge : q(t) = C·E·(1 − e^(−t/τ)) ; i = C·du_C/dt = (E/R)·e^(−t/τ), car τ = R·C ; I₀ = i(0) = E/R.
9. **u_R(t) et les quatre courbes** — u_R = R·i = E·e^(−t/τ) ; u_R + u_C = E : u_C et q montent vers leur valeur finale, u_R et i descendent vers 0.
   ⟶ *fin du bloc `rc_s3_b2`*

### VI. La constante de temps : la calculer, la lire

1. **τ est un temps** — τ = R·C est un temps : [R] = [U]/[I] et [C] = [I]·[T]/[U], donc [τ] = [T] ; τ en seconde (s).
2. **τ par la tangente à l'origine** — Méthode 1 (tangente) : la tangente à l'origine coupe l'asymptote u_C = E au point d'abscisse t = τ ; lire τ avec l'unité de l'axe.
   *Dessin — τ par la tangente à l'origine* : La tangente à l'origine coupe l'asymptote u_C = E au point d'abscisse t = τ (ici 0,22 s).
3. **τ par les 63 %** — Méthode 2 (63 %) : 1) calculer 0,63·E ; 2) horizontale jusqu'à la courbe ; 3) projeter sur l'axe des temps : τ. Attention : sur la courbe, pas sur la tangente.
   ⟶ *fin du bloc `rc_s4_b1`*
4. **Plus de R, plus lent** — Si R augmente, τ = R·C augmente : la charge est plus lente. Exemple : R = 2 kΩ, C = 220 µF : τ = 2·10³ × 220·10⁻⁶ = 0,44 s.
   *Dessin — Influence de R sur la charge* : E = 12 V, C = 220 µF : R = 1 kΩ (τ = 0,22 s) puis 2 kΩ (τ = 0,44 s) ; la charge est plus lente, la valeur finale reste E.
5. **Plus de C, plus lent aussi** — Si C double (R fixe), τ double : la charge et la décharge sont plus lentes ; la valeur finale ne change pas.
6. **De τ à R et C** — Méthode 4 (R et C) : R = E/I₀ (I₀ lu à t = 0) ou C = Q_m/E ; puis C = τ/R ou R = τ/C ; expression, application numérique, unité.
   ⟶ *fin du bloc `rc_s3_b3a`*
7. **Une courbe sans le temps : du_C/dt = f(u_C)** — Méthode 3 (courbe sans le temps) : du_C/dt = −u_C/(RC) + E/(RC), droite de pente a = −1/(RC), donc C = −1/(R·a) ; elle coupe l'axe des u_C en E.
   *Dessin — La droite du_C/dt = f(u_C)* : Pente a = −1/(RC) < 0 : a = −1000/12 ≈ −83,3 s⁻¹ ; R = 1 kΩ, donc C = −1/(R·a) = 12 µF (2021 N).
8. **q = f(u) : la pente est C** — q = f(u) : droite de pente C = Δq/Δu ; en parallèle, C_eq = C₁ + C₂ donne C₂ = C_eq − C₁.
   ⟶ *fin du bloc `rc_s4_b2`*

### VII. La décharge : voir, écrire, résoudre

1. **u_C ne saute pas, i change de sens** — À la bascule, nouvelle origine t = 0. u_C est continue : u_C(0) = E ; i saute : i(0) = −E/R. Attention : le courant change de sens.
2. **La décharge : sans générateur** — Décharge (K en 2, sans générateur) : u_R + u_C = 0, donc RC·du_C/dt + u_C = 0 ; i = C·du_C/dt < 0.
3. **La décharge : u_C = E·e^(−t/τ)** — Décharge : u_C = A·e^(−t/τ) dans RC·du_C/dt + u_C = 0 donne τ = R·C ; u_C(0) = E donne A = E : u_C(t) = E·e^(−t/τ).
   *Dessin — Décharge : u_C(t)* : u_C part de E (u_C est continue) et tend vers 0 : u_C = E·e^(−t/τ) ; u_C(τ) = 0,37·E.
   ⟶ *fin du bloc `rc_s3_b3`*
4. **q(t), i(t) et u_R(t) pendant la décharge** — Décharge : q = C·E·e^(−t/τ) ; i = −(E/R)·e^(−t/τ) ; u_R = −E·e^(−t/τ) ; u_C(τ) ≈ 0,37·E.
5. **Courbes qui descendent : 37 %** — Courbe qui descend (décharge, i, u_R) : la tangente à l'origine coupe l'axe des temps en t = τ ; à τ, il reste 37 % de la valeur initiale.
   *Dessin — Courbe qui descend : i(t)* : I₀ = E/R = 12 mA ; la tangente à l'origine coupe l'axe des temps à τ ; i(τ) = 0,37·I₀ = 4,44 mA.
6. **Le tableau des huit équations** — Second membre — charge : E pour u_C, C·E pour q, 0 pour u_R et i ; décharge : 0 pour les quatre grandeurs.
   ⟶ *fin du bloc `rc_s3_b4`*

### VIII. L'énergie emmagasinée

1. **L'énergie du condensateur** — Énergie électrique emmagasinée : E_e = ½·C·u_C² (E_e en J, C en F, u_C en V). Usage : flash d'appareil photo.
2. **Calculer l'énergie** — E_e = ½·C·u_C² = q²/(2C) ; fin de charge : E_e = ½·C·E². Attention au carré : si u_C double, E_e est multipliée par 4.
   ⟶ *fin du bloc `rc_s4_b2b`*

### IX. Le national 2022 N, joué pas à pas

1. **Le national 2022 N : lire le sujet deux fois** — National 2022 N : E = 12 V, condensateur déchargé, K en (1) à t = 0 ; courbes u_C(t), i(t) et tangente (T) à t = 0.
2. **2022 N, étape 1 : l'équation différentielle** — 1.1 : u_R + u_C = E ; u_R = R·i = RC·du_C/dt, donc du_C/dt + u_C/(RC) = E/(RC).
3. **2022 N, étape 2 : l'expression de i(t)** — 1.2.1 : i = C·du_C/dt = (E/R)·e^(−t/(RC)).
4. **2022 N, étape 3 : lire E et i(0)** — Lecture (l'unité de l'axe d'abord) : E = 12 V (régime permanent de u_C) ; i(0) = 12 mA.
   ⟶ *fin du bloc `rc_np_b1`*
5. **2022 N, étape 4 : la valeur de R** — 1.2.2 : i(0) = E/R, donc R = E/i(0) = 12/(12·10⁻³) = 1,0·10³ Ω.
6. **2022 N, étape 5 : τ par la tangente** — Méthode 1 : (T) coupe l'asymptote u_C = E à t = τ : τ = 50 ms.
   *Dessin — 2022 N : u_C(t) et la tangente (T)* : (T) coupe l'asymptote u_C = E = 12 V à t = τ = 50 ms ; u_C(τ) = 0,63·E = 7,56 V : même τ.
7. **2022 N, étape 6 : τ par les 63 %** — Méthode 2 : 0,63·E = 7,56 V est atteint à t = 50 ms = τ ; les deux méthodes concordent.
   ⟶ *fin du bloc `rc_np_b2`*
8. **2022 N, étape 7 : montrer que C = 50 µF** — 1.2.3 : τ = R·C, donc C = τ/R = 50·10⁻³/10³ = 5·10⁻⁵ F = 50 µF.
9. **2022 N, étape 8 : l'énergie emmagasinée** — Énergie : E_e = ½·C·E² = ½ × 50·10⁻⁶ × 12² = 3,6·10⁻³ J.
10. **2022 N : la copie complète** — Copie : chaque réponse = relation, application numérique, résultat avec unité (R = 1 kΩ ; τ = 50 ms ; C = 50 µF ; E_e = 3,6 mJ).
   ⟶ *fin du bloc `rc_np_b3`*

### X. Deux sujets complets du national

1. **Un sujet complet : la charge (2019 N)** — 2019 N : RC·dq/dt + q = C·E ; q = A(1 − e^(−αt)) avec A = C·E, α = 1/(RC) ; C = Q/E = 10⁻⁴/10 = 10 µF ; R = τ/C = 100 Ω.
2. **Un sujet complet : l'intensité (2021 R)** — 2021 R : R₁C·di/dt + i = 0 ; i = I₀·e^(−t/τ) avec τ = R₁C ; R₁ = E/i(0) = 6/0,05 = 120 Ω ; C = τ/R₁ = 100 µF.
   ⟶ *fin du bloc `rc_s4_b3`*

### XI. Bilan du chapitre

1. **Ce qu'il faut retenir** — À retenir : q = C·u_C ; i = C·du_C/dt ; RC·du_C/dt + u_C = E ; u_C = E(1 − e^(−t/τ)) ; τ = R·C ; 63 % / 37 % ; E_e = ½·C·u_C².
2. **La carte du chapitre et la suite** — Carte : q = C·u_C → équation → solution → τ = R·C → lire τ → énergie. Suite : dipôle RL (τ = L/R), puis circuit RLC.
   ⟶ *fin du bloc `rc_s4_b4`*
