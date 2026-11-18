# Le cahier de l'élève — Dipôle RL (`phys_ch7_dipole_RL`)

18 novembre 2026, skill `cahier-de-l-eleve`. Cours en ligne `backend/data/courses/phys_ch7_dipole_RL.json` et copie en
attente `backend/data/courses/en_attente/phys_ch7_dipole_RL.json`. Seuls `blocs[].cahier`, `blocs[].cahier_figures`,
`concentration.cahier` et `concentration.cahier_figures` ont été posés (script en un seul passage, format gardé).
Vérification : `verifier_figures_cahier.py` → 0 erreur sur les deux fichiers (1 avertissement : le montage normalisé a
20 éléments).

## Affichage et numérotation

Comme pour le RC (`phys_ch6_dipole_RC_cahier.md`) et le RLC : le lecteur écrit lui-même la partie (« IV. L'équation
différentielle ») et, quand le bloc a une ligne par diapositive, le titre numéroté de chaque diapositive au-dessus de sa
ligne. Le cahier a donc **une entrée par diapositive**, la même dans la bulle et dans l'étape de fin de bloc, sans
numéro propre (sinon il s'afficherait en double).

## Le plan parallèle RC / RL / RLC

| Squelette commun | Parties du cours RL (en ligne) |
|---|---|
| I. Le dipôle : 1. description et symbole ; 2. convention récepteur, u_b = L·di/dt + r·i ; 3. L en H | I. La bobine s'oppose aux variations du courant ; II. La tension aux bornes d'une bobine |
| II. Échelon montant : 1. montage, sens de i, flèches ; 2. équation ; 3. solution ; 4. τ ; 5. courbes | III. Le dipôle RL soumis à un échelon ; IV. L'équation différentielle ; V. La solution et la constante de temps |
| III. Échelon descendant (rupture) | VI. La rupture du courant |
| IV. Méthodes du national : 1 tangente, 2 63 %/37 %, 3 courbe sans le temps, 4 trouver r et L | VII. Lire les courbes |
| V. Énergie | VIII. L'énergie magnétique |
| (sujets, bilan) | IX. Deux sujets du national ; X. Bilan |

Les parties I à X du RL et du RC se répondent une à une ; les méthodes ont les mêmes noms et numéros que dans le RC
(« Méthode 1 (tangente) », « Méthode 2 (63 %) », « Méthode 3 (courbe sans le temps) », « Méthode 4 (r et L) »). Écart
gardé (ordre des diapositives) : la Méthode 4 vient avant la Méthode 3.

**Copie en attente** : les étapes de l'équation sont écrites une à une (Étapes 1, 2, 3) avant la rédaction ; τ et sa
lecture (Méthodes 1 et 2) viennent juste après la solution, **avant** la rupture : les lignes `rl_l1_tangente` et
`rl_l2_pourcent` n'y parlent donc pas encore de la descente, et la ligne `rl_t2_descente` y applique les Méthodes 1 et
2 à la courbe qui descend ; le national 2023 N est joué pas à pas (partie IX).

## Ce qui a été ajouté ou corrigé

- **Conventions dessinées avant usage** : schéma « Convention récepteur » (le même que dans le RC) dès la loi d'Ohm ;
  le bloc u_b montre d'abord « La bobine (L, r) » fléchée en convention récepteur, puis u_b en créneaux ; le montage est
  refait **avec K** (interrupteur), la borne + de E, le sens de i, les flèches de u_R et u_b.
- **Nouvelle courbe** (copie en attente) : « 2023 N : i(t) et la tangente (T) » (I₀ = 48 mA, τ = 2 ms, 30 mA à τ).
- **Définitions** : bobine, auto-induction ; **méthodes numérotées** : u_b sur une courbe i(t), Méthodes 1 à 4.
- **Compléments du national** (`exploration/dipole_RL.json`, `erreurs_examen`) : « Attention » sur r·i oublié, I₀ ≠ E/R,
  u_b = 0 seulement si r = 0, le second membre R·E/L en u_R, le second membre 0 à la rupture, les unités des axes
  (2024 N), le carré de l'énergie.
- **Rien avant d'être écrit** : I₀ et u_b sont définis à leur première apparition ; τ n'est plus cité dans les formes
  de l'équation ni dans l'exemple 2021 R (il n'est défini qu'en V) ; l'additivité des rappels ne cite plus u_b.
- **Taille** : une entrée par diapositive, 2 à 5 entrées et 0 à 2 dessins par bloc ; la fiche bilan tient en une ligne.

## Ce qui reste

- Pas de schéma de la rupture avec diode et R₁ (`rl_t3_diode`) : à dessiner si l'on veut (il demande ~20 éléments).
- Les blocs de 2 diapositives (copie en attente) n'ont que 2 entrées.

## Le cahier, partie par partie (cours en ligne)

### I. La bobine s'oppose aux variations du courant

1. **La carte du chapitre : une bobine qui freine le courant** — Dipôle RL : un conducteur ohmique (R) et une bobine (L, r) en série. Plan : bobine, u_b, échelon, équation, solution, τ = L/(R + r), rupture, courbes, énergie.
2. **Rappel : la loi d’Ohm** — Convention récepteur : la flèche de la tension est opposée au sens de i. Loi d'Ohm (convention récepteur) : u_R = R·i, R en ohm (Ω).
   *Dessin — Convention récepteur* : La flèche de u_AB (de B vers A) est opposée au sens de i : u_AB = R·i.
3. **Rappel : la loi d’additivité des tensions** — Loi d'additivité des tensions : u_AC = u_AB + u_BC ; en série, la tension du générateur est la somme des tensions des dipôles.
   ⟶ *fin du bloc `rl_s0_b1`*
4. **Rappel : la dérivée, c’est une pente** — Rappel : la dérivée est la pente de la tangente ; di/dt mesure la vitesse de variation de i (i constante : di/dt = 0).
5. **La bobine : un fil enroulé** — Définition : une bobine est un fil conducteur enroulé ; on la note (L, r) : L, inductance en henry (H) ; r, résistance du fil en ohm (Ω).
6. **Deux branches presque pareilles** — Expérience des deux lampes : deux branches en parallèle, identiques, sauf que la lampe L₂ est en série avec une bobine (de résistance r = R).
   ⟶ *fin du bloc `rl_s0_b2`*
7. **Deux lampes, une surprise** — Fermeture de K : la lampe en série avec la bobine s'allume en retard. Donc la bobine retarde l'établissement du courant.
8. **À la fin, le même éclat** — À la fin, même éclat : en régime permanent (i ne varie plus, i = I₀), la bobine se comporte comme un conducteur ohmique de résistance r.
9. **On ouvre K : un retard aussi** — Ouverture de K : i ne tombe pas à zéro d'un coup ; la bobine s'oppose aussi à la diminution du courant.
10. **Auto-induction et continuité de i** — Définition : l'auto-induction est l'opposition de la bobine aux variations de i. Donc l'intensité i dans une bobine est continue (fermeture : i(0) = 0).
   ⟶ *fin du bloc `rl_s1_b1`*

### II. La tension aux bornes d'une bobine

1. **Un courant en triangle** — TP (r négligeable) : i monte à vitesse constante → u_b (tension de la bobine) constante > 0 ; i descend → u_b < 0. Donc u_b dépend de di/dt, pas de i.
   *Dessin — Le courant en triangle* : i monte de 0 à 0,2 A en 10 ms, puis redescend en 10 ms, à vitesse constante.
   *Dessin — La tension en créneaux* : u_b suit la pente de i, pas sa valeur : +0,4 V pendant la montée, −0,4 V pendant la descente.
2. **u_b = L·di/dt** — Bobine idéale (r = 0), convention récepteur : u_b = L·di/dt, donc L = u_b/(di/dt) ; L en H, di/dt en A/s.
   *Dessin — Le montage du TP* : GBF, bobine et R en série ; masse en M : Y₁ donne u_b, Y₂ donne −R·i (on en tire i).
3. **La bobine réelle : u_b = L·di/dt + r·i** — Bobine réelle, convention récepteur (flèche de u_b opposée à i) : u_b = L·di/dt + r·i (bobine idéale L en série avec r).
   *Dessin — La bobine (L, r)* : Convention récepteur : la flèche de u_b est opposée à i ; u_b = L·di/dt + r·i.
   *Dessin — Le schéma équivalent* : Bobine (L, r) = bobine idéale L en série avec r : u_b = L·di/dt + r·i.
4. **Calculer u_b sur une courbe** — Méthode (u_b sur une courbe i(t)) : 1) di/dt = Δi/Δt sur le segment (Δt en s) ; 2) u_b = L·di/dt + r·i. Segment horizontal : u_b = r·i.
5. **Exercice du national : la bobine en régime permanent** — Régime permanent : di/dt = 0, donc u_b = r·I₀ et r = u_b/I₀ (2020 N : r = 1/0,1 = 10 Ω). Attention : u_b = 0 seulement si r = 0.
   ⟶ *fin du bloc `rl_s1_b3`*

### III. Le dipôle RL soumis à un échelon de tension

1. **Le montage RL** — Montage : E, K, R et la bobine (L, r) en série ; u_R et u_b fléchées en sens inverse de i. On visualise u_R = R·i : elle a la forme de i.
   *Dessin — Le montage RL fléché* : E, K (fermé à t = 0), R et la bobine (L, r) en série ; flèches de u_R et u_b opposées à i ; u_R = R·i est l'image de i.
2. **On ferme K : ce qu'on voit** — Fermeture de K (échelon montant, de 0 à E) : i part de 0, monte vite puis de plus en plus lentement vers une valeur limite I₀ : établissement du courant.
3. **Régime transitoire, régime permanent** — Régime transitoire : i varie ; régime permanent : i = I₀ constante, di/dt = 0 et u_b = r·I₀.
4. **La valeur finale I₀** — Régime permanent : R·I₀ + r·I₀ = E, donc I₀ = E/(R + r) (notée aussi I_p). Attention : pas E/R ; I₀ ne dépend pas de L.
   ⟶ *fin du bloc `rl_s2_b1`*

### IV. L'équation différentielle

1. **Loi d'additivité** — Loi d'additivité des tensions : u_R + u_b = E ; dans les sujets, u_b se note aussi u_L ou u_B.
2. **Remplacer chaque tension** — On remplace : u_R = R·i et u_b = L·di/dt + r·i, donc R·i + L·di/dt + r·i = E. Attention : ne pas oublier r·i.
3. **L'équation différentielle** — Équation différentielle vérifiée par i (établissement) : L·di/dt + (R + r)·i = E ; R + r est la résistance totale du circuit.
4. **Les formes des énoncés** — Autres écritures : di/dt + ((R + r)/L)·i = E/L (÷ L) ; (L/(R + r))·di/dt + i = E/(R + r) (÷ (R + r)). Attention : donner la forme demandée.
   ⟶ *fin du bloc `rl_s2_b2`*
5. **L'équation en u_R** — En u_R (i = u_R/R, di/dt = (1/R)·du_R/dt), puis × R : du_R/dt + ((R + r)/L)·u_R = R·E/L. Attention : le second membre est R·E/L.
6. **u_b au début et à la fin** — À t = 0 : i(0) = 0, donc u_R(0) = 0 et u_b(0) = E ; en régime permanent : u_R = R·I₀ et u_b = r·I₀.
   *Dessin — u_R(t) et u_b(t) à la fermeture* : u_b(0) = E = 6 V (i(0) = 0) puis u_b → r·I₀ = 1 V ; u_R part de 0 vers R·I₀ = 5 V ; u_R + u_b = E.
7. **Exercice du national : établir l'équation** — Exemple 2021 R : u_R₂ + u_b = E ; R₂·i + L·di/dt + r·i = E, donc di/dt + ((R₂ + r)/L)·i = E/L.
8. **Exercice du national : quelle courbe est u_R ?** — Exemple 2019 R : la courbe qui part de 0 est u_R (u_R(0) = R·i(0) = 0) ; régime permanent : U_R = R·E/(R + r), donc r = R·(E/U_R − 1).
   ⟶ *fin du bloc `rl_s2_b3`*

### V. La solution et la constante de temps

1. **Rappel : la fonction exponentielle** — Rappel : e⁰ = 1 ; e^(−t/τ) diminue vers 0 sans jamais s'annuler ; e⁻¹ ≈ 0,37 et 1 − e⁻¹ ≈ 0,63.
2. **La forme de la solution** — Solution proposée : i(t) = A(1 − e^(−t/τ)) : i(0) = 0, et i tend vers A quand t → +∞ (asymptote horizontale).
3. **Dériver la solution** — Dérivée : di/dt = (A/τ)·e^(−t/τ). Attention au signe : d(e^(−t/τ))/dt = −(1/τ)·e^(−t/τ).
4. **Remplacer et identifier τ** — On remplace : A·e^(−t/τ)·(L/τ − (R + r)) + (R + r)·A = E pour tout t ; donc L/τ = R + r : τ = L/(R + r).
   ⟶ *fin du bloc `rl_s3_b1`*
5. **Identifier A** — Et (R + r)·A = E : A = I₀ = E/(R + r). Solution : i(t) = I₀·(1 − e^(−t/τ)) ; u_R(t) = R·I₀·(1 − e^(−t/τ)).
6. **L'autre écriture : i(t) = A + B·e^(−t/τ)** — Forme i = A + B·e^(−t/τ) : di/dt = −(B/τ)·e^(−t/τ) ; pour tout t : τ = L/(R + r) (B ≠ 0) et A = E/(R + r) = I₀.
7. **La condition initiale donne B** — Condition initiale (i continue) : i(0) = A + B = 0, donc B = −I₀ : i(t) = I₀·(1 − e^(−t/τ)).
   ⟶ *fin du bloc `rl_s3_b1b`*
8. **τ est un temps** — τ = L/(R + r) est un temps : [L] = [U]·[T]/[I] et [R] = [U]/[I], donc [τ] = [T] ; τ en seconde (s).
9. **63 % à τ, presque tout à 5τ** — i(τ) = I₀(1 − e⁻¹) ≈ 0,63·I₀ ; i(5τ) ≈ 0,99·I₀ : le régime permanent est atteint au bout de 5τ.
   *Dessin — Établissement : i(t)* : i(τ) = 0,63·I₀ = 63 mA à τ = 2 ms ; à 5τ = 10 ms, i ≈ 0,99·I₀ : régime permanent.
10. **Si L double** — Si L double : τ = L/(R + r) double, I₀ = E/(R + r) ne change pas : même palier, montée plus lente.
   *Dessin — Si L double* : L = 0,12 H → 0,24 H : τ passe de 2 ms à 4 ms (montée plus lente), même palier I₀ = 100 mA.
11. **Si R augmente** — Si R augmente : I₀ = E/(R + r) diminue et τ = L/(R + r) diminue : palier plus bas, atteint plus vite.
   ⟶ *fin du bloc `rl_s3_b2`*

### VI. La rupture du courant

1. **La rupture du courant** — Rupture (échelon descendant, sans générateur) : u_R + u_b = 0, donc L·di/dt + (R + r)·i = 0. Attention : second membre 0.
2. **Vérifier la solution de la rupture** — Solution i = A·e^(−t/τ) + B : pour tout t, B = 0 et τ = L/(R + r), le même τ qu'à l'établissement.
3. **i descend : 37 % à τ** — i continue : i(0) = I₀, donc i(t) = I₀·e^(−t/τ) ; i(τ) ≈ 0,37·I₀ ; la tangente à l'origine coupe l'axe des temps en τ.
   *Dessin — Rupture : i(t)* : i part de I₀ = 100 mA (i est continue) ; i(τ) = 0,37·I₀ = 37 mA ; la tangente à l'origine coupe l'axe des temps à τ = 2 ms.
4. **Étincelle et diode** — Interrupteur simple : surtension à l'ouverture, étincelle. Une diode (avec R₁) en parallèle sur la bobine laisse i décroître ; u_b est alors grande et négative.
5. **Exercice du national : la rupture avec diode** — Exemple 2025 R : i(0⁺) = I₀ = 0,1 A (continuité) ; u_b + u_R1 = 0, donc u_b = −R₁·I₀ = −100 V (surtension).
   ⟶ *fin du bloc `rl_s3_b3`*

### VII. Lire les courbes

1. **τ par la tangente à l'origine** — Méthode 1 (tangente) : la tangente à l'origine coupe l'asymptote i = I₀ en t = τ (rupture : elle coupe l'axe des temps en τ).
   *Dessin — τ par la tangente à l'origine* : La tangente à l'origine coupe l'asymptote i = I₀ au point d'abscisse t = τ (ici 2 ms, I₀ = 100 mA).
2. **τ par les 63 %** — Méthode 2 (63 %) : 0,63 de la valeur finale lue (I₀ ou U_R max), horizontale jusqu'à la courbe, projection sur l'axe des temps : τ. Descente : 37 %.
3. **Trouver r** — Méthode 4 (r et L) — r : I₀ lu (I₀ = U_R max/R), puis I₀ = E/(R + r) donne r = E/I₀ − R (ou r = u_b/I₀ en régime permanent).
4. **Trouver L** — L : τ = L/(R + r), donc L = τ·(R + r) (τ en s, L en H) ; bobine idéale : L = τ·R.
   ⟶ *fin du bloc `rl_s4_b1`*
5. **La droite di/dt = f(i)** — Méthode 3 (courbe sans le temps) : di/dt = −((R + r)/L)·i + E/L : droite de pente −1/τ, d'ordonnée à l'origine E/L ; elle coupe l'axe des i en I₀.
   *Dessin — La droite di/dt = f(i)* : Ordonnée à l'origine E/L ; pente −1/τ < 0 ; elle coupe l'axe des i en I₀, où di/dt = 0 (ici 3·10³ A/s et 6 mA).
6. **La courbe u_b(t)** — u_b = E − R·i = r·I₀ + R·I₀·e^(−t/τ) : u_b(0) = E, puis u_b tend vers r·I₀ ; bobine idéale : u_b = E·e^(−t/τ).

### VIII. L'énergie magnétique

1. **L'énergie de la bobine** — Énergie magnétique emmagasinée : E_m = ½·L·i² (E_m en J, L en H, i en A) ; maximale en régime permanent : ½·L·I₀². Elle est rendue à la rupture.
2. **Si I₀ double** — Attention au carré : si I₀ double, E_m est multipliée par 4 ; si L double, E_m double.
   ⟶ *fin du bloc `rl_s4_b2`*

### IX. Deux sujets du national

1. **Sujet national 2022 R** — 2022 R : I₀ = U₀/R = 0,02 A ; r = E/I₀ − R = 10 Ω ; L₀ = τ·(R + r) = 0,5 H ; si L double : même palier, τ double.
2. **Sujet national 2024 N : la droite** — 2024 N : droite di/dt = f(i) : l'ordonnée à l'origine E/L donne L = 2 mH ; la pente −1/τ donne τ = 2 µs. Attention aux unités (mA, 10³ A/s).

### X. Bilan du chapitre

1. **Ce qu'il faut retenir** — À retenir : u_b = L·di/dt + r·i ; L·di/dt + (R + r)·i = E ; I₀ = E/(R + r) ; i = I₀(1 − e^(−t/τ)) ; rupture : i = I₀·e^(−t/τ) ; τ = L/(R + r) ; E_m = ½·L·i².
2. **La carte du dipôle RL** — Carte : u_b = L·di/dt + r·i → équation → solution → τ = L/(R + r) → lire τ → énergie. Suite : le circuit RLC.
   ⟶ *fin du bloc `rl_s4_b3`*

## Découpage en blocs — cours en ligne

| Bloc | Diapositives | Lignes | Dessins |
|---|---|---|---|
| `rl_s0_b1` | rl_o1_carte, rl_rp1_ohm, rl_rp2_additivite | 3 | Convention récepteur |
| `rl_s0_b2` | rl_rp3_derivee, rl_b1_bobine, rl_b2a_principe | 3 | — |
| `rl_s1_b1` | rl_b2_lampes, rl_b3_egal, rl_b4_ouverture, rl_b5_continuite | 4 | — |
| `rl_s1_b3` | rl_b6_triangle, rl_b7_inductance, rl_b8_reelle, rl_b9_segments, rl_b10_national | 5 | La bobine (L, r) ; La tension en créneaux |
| `rl_s2_b1` | rl_m1_montage, rl_m2_fermeture, rl_m3_regimes, rl_m4_I0 | 4 | Le montage RL fléché |
| `rl_s2_b2` | rl_e1_additivite, rl_e2_remplacer, rl_e3_equation, rl_e4_formes | 4 | — |
| `rl_s2_b3` | rl_e5_uR, rl_e6_ub, rl_e7_2021R, rl_e8_2019R | 4 | u_R(t) et u_b(t) à la fermeture |
| `rl_s3_b1` | rl_rp4_exponentielle, rl_s1_forme, rl_s2_deriver, rl_s3_tau | 4 | — |
| `rl_s3_b1b` | rl_s4_A, rl_s4b_forme, rl_s4c_condition | 3 | — |
| `rl_s3_b2` | rl_s5_dimension, rl_s6_pourcent, rl_s7_L, rl_s8_R | 4 | Établissement : i(t) ; Si L double |
| `rl_s3_b3` | rl_t1_rupture, rl_t2a_verifier, rl_t2_descente, rl_t3_diode, rl_t4_national | 5 | Rupture : i(t) |
| `rl_s4_b1` | rl_l1_tangente, rl_l2_pourcent, rl_l3_r, rl_l4_L | 4 | τ par la tangente à l'origine |
| `rl_s4_b2` | rl_l5_droite, rl_l6_ub, rl_l7_energie, rl_l8_double | 4 | La droite di/dt = f(i) |
| `rl_s4_b3` | rl_n1_2022R, rl_n2_2024N, rl_bl_fiche, rl_cr_carte | 4 | — |

## Découpage en blocs — copie en attente

| Bloc | Diapositives | Lignes | Dessins |
|---|---|---|---|
| `rl_s0_b1` | rl_o1_carte, rl_rp1_ohm, rl_rp2_additivite | 3 | Convention récepteur |
| `rl_s0_b2` | rl_rp3_derivee, rl_b1_bobine, rl_b2a_principe | 3 | — |
| `rl_s1_b1` | rl_b2_lampes, rl_b3_egal, rl_b4_ouverture, rl_b5_continuite | 4 | — |
| `rl_s1_b3` | rl_b6_triangle, rl_b7_inductance, rl_b8_reelle, rl_b9_segments, rl_b10_national | 5 | La bobine (L, r) ; La tension en créneaux |
| `rl_s2_b1` | rl_m1_montage, rl_m2_fermeture, rl_m3_regimes, rl_m4_I0, rl_m5_observer | 5 | Le montage RL fléché |
| `rl_s2_b2` | rl_e0a_additivite, rl_e1_additivite, rl_e0b_remplacer, rl_e2_remplacer | 4 | — |
| `rl_s2_b2b` | rl_e0c_ranger, rl_e3_equation, rl_e4_formes | 3 | — |
| `rl_s2_b3` | rl_e5_uR, rl_e6_ub | 2 | u_R(t) et u_b(t) à la fermeture |
| `rl_s2_b3b` | rl_e7_2021R, rl_e8_2019R | 2 | — |
| `rl_s3_b1` | rl_rp4_exponentielle, rl_s1_forme, rl_s2_deriver, rl_s3_tau | 4 | — |
| `rl_s3_b1b` | rl_s4_A, rl_s4b_forme, rl_s4c_condition | 3 | — |
| `rl_s3_b2` | rl_s5_dimension, rl_s6_pourcent, rl_l1_tangente, rl_l2_pourcent | 4 | Établissement : i(t) ; τ par la tangente à l'origine |
| `rl_s4_b1` | rl_s7_L, rl_s8_R, rl_l3_r, rl_l4_L | 4 | Si L double |
| `rl_s4_b2` | rl_l5_droite, rl_l6_ub | 2 | La droite di/dt = f(i) |
| `rl_s3_b3` | rl_t1_rupture, rl_t2a_verifier, rl_t2_descente | 3 | Rupture : i(t) |
| `rl_s3_b4` | rl_t3_diode, rl_t4_national | 2 | — |
| `rl_s4_b2b` | rl_l7_energie, rl_l8_double | 2 | — |
| `rl_np_b1` | rl_np0_sujet, rl_np1_equation, rl_np2_remplacer, rl_np3_constantes | 4 | — |
| `rl_np_b2` | rl_np4_lire, rl_np5_tangente, rl_np6_pourcent, rl_np7_L | 4 | 2023 N : i(t) et la tangente (T) |
| `rl_np_b3` | rl_np8_ub, rl_np9_energie, rl_np10_copie | 3 | — |
| `rl_s4_b3` | rl_n1_2022R, rl_n2_2024N, rl_bl_fiche, rl_cr_carte | 4 | — |

## La copie en attente, dans son ordre

### I. Les outils, la bobine et les deux lampes

1. **La carte du chapitre : une bobine qui freine le courant** — Dipôle RL : un conducteur ohmique (R) et une bobine (L, r) en série. Plan : bobine, u_b, échelon, équation, solution, τ = L/(R + r), rupture, courbes, énergie.
2. **Rappel : la loi d’Ohm** — Convention récepteur : la flèche de la tension est opposée au sens de i. Loi d'Ohm (convention récepteur) : u_R = R·i, R en ohm (Ω).
   *Dessin — Convention récepteur* : La flèche de u_AB (de B vers A) est opposée au sens de i : u_AB = R·i.
3. **Rappel : la loi d’additivité des tensions** — Loi d'additivité des tensions : u_AC = u_AB + u_BC ; en série, la tension du générateur est la somme des tensions des dipôles.
   ⟶ *fin du bloc `rl_s0_b1`*
4. **Rappel : la dérivée, c’est une pente** — Rappel : la dérivée est la pente de la tangente ; di/dt mesure la vitesse de variation de i (i constante : di/dt = 0).
5. **La bobine : un fil enroulé** — Définition : une bobine est un fil conducteur enroulé ; on la note (L, r) : L, inductance en henry (H) ; r, résistance du fil en ohm (Ω).
6. **Deux branches presque pareilles** — Expérience des deux lampes : deux branches en parallèle, identiques, sauf que la lampe L₂ est en série avec une bobine (de résistance r = R).
   ⟶ *fin du bloc `rl_s0_b2`*
7. **Deux lampes, une surprise** — Fermeture de K : la lampe en série avec la bobine s'allume en retard. Donc la bobine retarde l'établissement du courant.
8. **À la fin, le même éclat** — À la fin, même éclat : en régime permanent (i ne varie plus, i = I₀), la bobine se comporte comme un conducteur ohmique de résistance r.
9. **On ouvre K : un retard aussi** — Ouverture de K : i ne tombe pas à zéro d'un coup ; la bobine s'oppose aussi à la diminution du courant.
10. **Auto-induction et continuité de i** — Définition : l'auto-induction est l'opposition de la bobine aux variations de i. Donc l'intensité i dans une bobine est continue (fermeture : i(0) = 0).
   ⟶ *fin du bloc `rl_s1_b1`*

### II. La tension aux bornes d'une bobine

1. **Un courant en triangle** — TP (r négligeable) : i monte à vitesse constante → u_b (tension de la bobine) constante > 0 ; i descend → u_b < 0. Donc u_b dépend de di/dt, pas de i.
   *Dessin — Le courant en triangle* : i monte de 0 à 0,2 A en 10 ms, puis redescend en 10 ms, à vitesse constante.
   *Dessin — La tension en créneaux* : u_b suit la pente de i, pas sa valeur : +0,4 V pendant la montée, −0,4 V pendant la descente.
2. **u_b = L·di/dt** — Bobine idéale (r = 0), convention récepteur : u_b = L·di/dt, donc L = u_b/(di/dt) ; L en H, di/dt en A/s.
   *Dessin — Le montage du TP* : GBF, bobine et R en série ; masse en M : Y₁ donne u_b, Y₂ donne −R·i (on en tire i).
3. **La bobine réelle : u_b = L·di/dt + r·i** — Bobine réelle, convention récepteur (flèche de u_b opposée à i) : u_b = L·di/dt + r·i (bobine idéale L en série avec r).
   *Dessin — La bobine (L, r)* : Convention récepteur : la flèche de u_b est opposée à i ; u_b = L·di/dt + r·i.
   *Dessin — Le schéma équivalent* : Bobine (L, r) = bobine idéale L en série avec r : u_b = L·di/dt + r·i.
4. **Calculer u_b sur une courbe** — Méthode (u_b sur une courbe i(t)) : 1) di/dt = Δi/Δt sur le segment (Δt en s) ; 2) u_b = L·di/dt + r·i. Segment horizontal : u_b = r·i.
5. **Exercice du national : la bobine en régime permanent** — Régime permanent : di/dt = 0, donc u_b = r·I₀ et r = u_b/I₀ (2020 N : r = 1/0,1 = 10 Ω). Attention : u_b = 0 seulement si r = 0.
   ⟶ *fin du bloc `rl_s1_b3`*

### III. Le montage : ce qu'on voit, ce qu'on règle

1. **Le montage RL** — Montage : E, K, R et la bobine (L, r) en série ; u_R et u_b fléchées en sens inverse de i. On visualise u_R = R·i : elle a la forme de i.
   *Dessin — Le montage RL fléché* : E, K (fermé à t = 0), R et la bobine (L, r) en série ; flèches de u_R et u_b opposées à i ; u_R = R·i est l'image de i.
2. **On ferme K : ce qu'on voit** — Fermeture de K (échelon montant, de 0 à E) : i part de 0, monte vite puis de plus en plus lentement vers une valeur limite I₀ : établissement du courant.
3. **Régime transitoire, régime permanent** — Régime transitoire : i varie ; régime permanent : i = I₀ constante, di/dt = 0 et u_b = r·I₀.
4. **La valeur finale I₀** — Régime permanent : R·I₀ + r·I₀ = E, donc I₀ = E/(R + r) (notée aussi I_p). Attention : pas E/R ; I₀ ne dépend pas de L.
5. **L et R au curseur : le courant plus lent ou plus rapide ?** — Observation : L plus grande → établissement plus lent, même palier I₀ ; R plus grande → palier plus bas, atteint plus vite.
   ⟶ *fin du bloc `rl_s2_b1`*

### IV. L'équation différentielle, écrite pas à pas

1. **À toi : la première ligne** — Étape 1 (loi d'additivité des tensions) : u_R + u_b = E.
2. **Loi d'additivité** — Loi d'additivité des tensions : u_R + u_b = E ; dans les sujets, u_b se note aussi u_L ou u_B.
3. **À toi : remplacer u_R et u_b** — Étape 2 (loi d'Ohm et bobine réelle) : R·i + L·di/dt + r·i = E. Attention : ne pas oublier r·i.
4. **Remplacer chaque tension** — Rédaction : u_R = R·i et u_b = L·di/dt + r·i, remplacés dans u_R + u_b = E.
   ⟶ *fin du bloc `rl_s2_b2`*
5. **À toi : ranger l'équation** — Étape 3 (on regroupe les termes en i) : L·di/dt + (R + r)·i = E.
6. **L'équation différentielle** — Équation différentielle vérifiée par i (établissement) : L·di/dt + (R + r)·i = E ; R + r est la résistance totale du circuit.
7. **Les formes des énoncés** — Autres écritures : di/dt + ((R + r)/L)·i = E/L (÷ L) ; (L/(R + r))·di/dt + i = E/(R + r) (÷ (R + r)). Attention : donner la forme demandée.
   ⟶ *fin du bloc `rl_s2_b2b`*
8. **L'équation en u_R** — En u_R (i = u_R/R, di/dt = (1/R)·du_R/dt), puis × R : du_R/dt + ((R + r)/L)·u_R = R·E/L. Attention : le second membre est R·E/L.
9. **u_b au début et à la fin** — À t = 0 : i(0) = 0, donc u_R(0) = 0 et u_b(0) = E ; en régime permanent : u_R = R·I₀ et u_b = r·I₀.
   *Dessin — u_R(t) et u_b(t) à la fermeture* : u_b(0) = E = 6 V (i(0) = 0) puis u_b → r·I₀ = 1 V ; u_R part de 0 vers R·I₀ = 5 V ; u_R + u_b = E.
   ⟶ *fin du bloc `rl_s2_b3`*
10. **Exercice du national : établir l'équation** — Exemple 2021 R : u_R₂ + u_b = E ; R₂·i + L·di/dt + r·i = E, donc di/dt + ((R₂ + r)/L)·i = E/L.
11. **Exercice du national : quelle courbe est u_R ?** — Exemple 2019 R : la courbe qui part de 0 est u_R (u_R(0) = R·i(0) = 0) ; régime permanent : U_R = R·E/(R + r), donc r = R·(E/U_R − 1).
   ⟶ *fin du bloc `rl_s2_b3b`*

### V. La solution

1. **Rappel : la fonction exponentielle** — Rappel : e⁰ = 1 ; e^(−t/τ) diminue vers 0 sans jamais s'annuler ; e⁻¹ ≈ 0,37 et 1 − e⁻¹ ≈ 0,63.
2. **La forme de la solution** — Solution proposée : i(t) = A(1 − e^(−t/τ)) : i(0) = 0, et i tend vers A quand t → +∞ (asymptote horizontale).
3. **Dériver la solution** — Dérivée : di/dt = (A/τ)·e^(−t/τ). Attention au signe : d(e^(−t/τ))/dt = −(1/τ)·e^(−t/τ).
4. **Remplacer et identifier τ** — On remplace : A·e^(−t/τ)·(L/τ − (R + r)) + (R + r)·A = E pour tout t ; donc L/τ = R + r : τ = L/(R + r).
   ⟶ *fin du bloc `rl_s3_b1`*
5. **Identifier A** — Et (R + r)·A = E : A = I₀ = E/(R + r). Solution : i(t) = I₀·(1 − e^(−t/τ)) ; u_R(t) = R·I₀·(1 − e^(−t/τ)).
6. **L'autre écriture : i(t) = A + B·e^(−t/τ)** — Forme i = A + B·e^(−t/τ) : di/dt = −(B/τ)·e^(−t/τ) ; pour tout t : τ = L/(R + r) (B ≠ 0) et A = E/(R + r) = I₀.
7. **La condition initiale donne B** — Condition initiale (i continue) : i(0) = A + B = 0, donc B = −I₀ : i(t) = I₀·(1 − e^(−t/τ)).
   ⟶ *fin du bloc `rl_s3_b1b`*

### VI. La constante de temps : la calculer, la lire

1. **τ est un temps** — τ = L/(R + r) est un temps : [L] = [U]·[T]/[I] et [R] = [U]/[I], donc [τ] = [T] ; τ en seconde (s).
2. **63 % à τ, presque tout à 5τ** — i(τ) = I₀(1 − e⁻¹) ≈ 0,63·I₀ ; i(5τ) ≈ 0,99·I₀ : le régime permanent est atteint au bout de 5τ.
   *Dessin — Établissement : i(t)* : i(τ) = 0,63·I₀ = 63 mA à τ = 2 ms ; à 5τ = 10 ms, i ≈ 0,99·I₀ : régime permanent.
3. **τ par la tangente à l'origine** — Méthode 1 (tangente) : la tangente à l'origine coupe l'asymptote i = I₀ au point d'abscisse t = τ ; lire τ avec l'unité de l'axe.
   *Dessin — τ par la tangente à l'origine* : La tangente à l'origine coupe l'asymptote i = I₀ au point d'abscisse t = τ (ici 2 ms, I₀ = 100 mA).
4. **τ par les 63 %** — Méthode 2 (63 %) : 0,63 de la valeur finale lue (I₀ ou U_R max), horizontale jusqu'à la courbe, projection sur l'axe des temps : τ.
   ⟶ *fin du bloc `rl_s3_b2`*
5. **Si L double** — Si L double : τ = L/(R + r) double, I₀ = E/(R + r) ne change pas : même palier, montée plus lente.
   *Dessin — Si L double* : L = 0,12 H → 0,24 H : τ passe de 2 ms à 4 ms (montée plus lente), même palier I₀ = 100 mA.
6. **Si R augmente** — Si R augmente : I₀ = E/(R + r) diminue et τ = L/(R + r) diminue : palier plus bas, atteint plus vite.
7. **Trouver r** — Méthode 4 (r et L) — r : I₀ lu (I₀ = U_R max/R), puis I₀ = E/(R + r) donne r = E/I₀ − R (ou r = u_b/I₀ en régime permanent).
8. **Trouver L** — L : τ = L/(R + r), donc L = τ·(R + r) (τ en s, L en H) ; bobine idéale : L = τ·R.
   ⟶ *fin du bloc `rl_s4_b1`*
9. **La droite di/dt = f(i)** — Méthode 3 (courbe sans le temps) : di/dt = −((R + r)/L)·i + E/L : droite de pente −1/τ, d'ordonnée à l'origine E/L ; elle coupe l'axe des i en I₀.
   *Dessin — La droite di/dt = f(i)* : Ordonnée à l'origine E/L ; pente −1/τ < 0 ; elle coupe l'axe des i en I₀, où di/dt = 0 (ici 3·10³ A/s et 6 mA).
10. **La courbe u_b(t)** — u_b = E − R·i = r·I₀ + R·I₀·e^(−t/τ) : u_b(0) = E, puis u_b tend vers r·I₀ ; bobine idéale : u_b = E·e^(−t/τ).
   ⟶ *fin du bloc `rl_s4_b2`*

### VII. La rupture du courant : voir, écrire, résoudre

1. **La rupture du courant** — Rupture (échelon descendant, sans générateur) : u_R + u_b = 0, donc L·di/dt + (R + r)·i = 0. Attention : second membre 0.
2. **Vérifier la solution de la rupture** — Solution i = A·e^(−t/τ) + B : pour tout t, B = 0 et τ = L/(R + r), le même τ qu'à l'établissement.
3. **i descend : 37 % à τ** — i continue : i(0) = I₀, donc i(t) = I₀·e^(−t/τ) ; Méthodes 1 et 2 sur une descente : tangente ∩ axe des temps en τ ; i(τ) ≈ 0,37·I₀.
   *Dessin — Rupture : i(t)* : i part de I₀ = 100 mA (i est continue) ; i(τ) = 0,37·I₀ = 37 mA ; la tangente à l'origine coupe l'axe des temps à τ = 2 ms.
   ⟶ *fin du bloc `rl_s3_b3`*
4. **Étincelle et diode** — Interrupteur simple : surtension à l'ouverture, étincelle. Une diode (avec R₁) en parallèle sur la bobine laisse i décroître ; u_b est alors grande et négative.
5. **Exercice du national : la rupture avec diode** — Exemple 2025 R : i(0⁺) = I₀ = 0,1 A (continuité) ; u_b + u_R1 = 0, donc u_b = −R₁·I₀ = −100 V (surtension).
   ⟶ *fin du bloc `rl_s3_b4`*

### VIII. L'énergie magnétique

1. **L'énergie de la bobine** — Énergie magnétique emmagasinée : E_m = ½·L·i² (E_m en J, L en H, i en A) ; maximale en régime permanent : ½·L·I₀². Elle est rendue à la rupture.
2. **Si I₀ double** — Attention au carré : si I₀ double, E_m est multipliée par 4 ; si L double, E_m double.
   ⟶ *fin du bloc `rl_s4_b2b`*

### IX. Le national 2023 N, joué pas à pas

1. **Le national 2023 N : lire le sujet deux fois** — National 2023 N : E = 24 V, bobine (L, r négligeable) et R en série, K fermé à t = 0 ; courbe i(t) et sa tangente (T) en t = 0.
2. **2023 N, étape 1 : l'équation différentielle** — 1-1 : u_R + u_b = E ; R·i + L·di/dt = E, donc di/dt + (R/L)·i = E/L.
3. **2023 N, étape 2 : dériver et remplacer** — i = A + B·e^(−t/τ) : di/dt = −(B/τ)·e^(−t/τ) ; on remplace : B·e^(−t/τ)·(R/L − 1/τ) + (R/L)·A − E/L = 0.
4. **2023 N, étape 3 : τ, A et B** — 1-2-1 : pour tout t, τ = L/R et A = E/R ; i(0) = 0 donne B = −E/R : i(t) = (E/R)·(1 − e^(−t/τ)).
   ⟶ *fin du bloc `rl_np_b1`*
5. **2023 N, étape 4 : lire I₀** — Lecture (l'unité de l'axe d'abord) : I₀ = A = E/R = 48 mA.
6. **2023 N, étape 5 : τ par la tangente** — Méthode 1 : (T) coupe l'asymptote i = I₀ à t = τ : τ = 2 ms.
   *Dessin — 2023 N : i(t) et la tangente (T)* : (T) coupe l'asymptote i = I₀ = 48 mA à t = τ = 2 ms ; i(τ) = 0,63·I₀ ≈ 30 mA : même τ.
7. **2023 N, étape 6 : τ par les 63 %** — Méthode 2 : 0,63·I₀ ≈ 30 mA est atteint à t = 2 ms = τ ; les deux méthodes concordent.
8. **2023 N, étape 7 : montrer que L = 1 H** — 1-2-2 : τ = L/R et R = E/I₀, donc L = τ·E/I₀ = 2·10⁻³ × 24/(48·10⁻³) = 1 H.
   ⟶ *fin du bloc `rl_np_b2`*
9. **2023 N, étape 8 : l'expression de u_b(t)** — 1-3 : u_b = L·di/dt = E·e^(−t/τ), soit u_b(t) = 24·e^(−500·t) (t en s).
10. **2023 N, étape 9 : l'énergie de la bobine** — Énergie : E_m = ½·L·I₀² = ½ × 1 × (48·10⁻³)² ≈ 1,2·10⁻³ J.
11. **2023 N : la copie complète** — Copie : relation, application numérique, résultat avec unité (I₀ = 48 mA ; τ = 2 ms ; L = 1 H ; E_m ≈ 1,2 mJ), dans l'ordre du RC.
   ⟶ *fin du bloc `rl_np_b3`*

### X. Deux sujets du national

1. **Sujet national 2022 R** — 2022 R : I₀ = U₀/R = 0,02 A ; r = E/I₀ − R = 10 Ω ; L₀ = τ·(R + r) = 0,5 H ; si L double : même palier, τ double.
2. **Sujet national 2024 N : la droite** — 2024 N : droite di/dt = f(i) : l'ordonnée à l'origine E/L donne L = 2 mH ; la pente −1/τ donne τ = 2 µs. Attention aux unités (mA, 10³ A/s).

### XI. Bilan du chapitre

1. **Ce qu'il faut retenir** — À retenir : u_b = L·di/dt + r·i ; L·di/dt + (R + r)·i = E ; I₀ = E/(R + r) ; i = I₀(1 − e^(−t/τ)) ; rupture : i = I₀·e^(−t/τ) ; τ = L/(R + r) ; E_m = ½·L·i².
2. **La carte du dipôle RL** — Carte : u_b = L·di/dt + r·i → équation → solution → τ = L/(R + r) → lire τ → énergie. Suite : le circuit RLC.
   ⟶ *fin du bloc `rl_s4_b3`*
