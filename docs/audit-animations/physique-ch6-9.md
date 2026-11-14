# Audit « animations au lieu de listes » — physique ch. 6 à 9

Règle 28 du professeur (14 novembre 2026) et étape 3 du skill `cours-concentration` : une diapo qui compare des valeurs, montre l'effet d'un paramètre ou décrit des étapes montre une petite manip à la craie (un bouton, au plus deux curseurs), les valeurs s'écrivent comme résultat de ce qu'on voit.

Constat général : dans ces quatre cours, **aucune diapo n'a de `screen_content.table`**, et **toutes ont déjà une simulation à la craie**. Les candidates sont donc les diapos dont la simulation montre une comparaison **figée** (deux courbes imposées, trois écrans fixes, un calcul écrit) alors que la diapo parle de l'effet d'un paramètre. Les fiches bilan (`*_bl_fiche`, `rc_b1_bilan`) et les cartes (`*_cr_carte`, `rc_o1_carte`, `rc_b2_carte`) sont laissées de côté.

La voix n'a été changée nulle part : seuls `visual`, `screen_content.bullets` (puces que l'animation montre maintenant) et `concentration.pointage` (sur des extraits exacts de `speech_text.mixed`) ont bougé.

## Ch. 6 — Dipôle RC (`phys_ch6_dipole_RC.json`)

| Diapo | À l'écran avant | Animation | Faite ? |
|---|---|---|---|
| `rc_t2_influence` « Plus de R, plus lent » | `courbe-charge.html?vue=R` : deux courbes imposées (R puis 2R), aucune manip ; puces avec les valeurs de τ | `tau-rc.html` : curseurs R et C, « Fermer K » trace u_C(t), τ s'écrit là où la courbe passe à 63 % de E, la courbe d'avant reste en pointillés, « τ × 2 : charge plus lente » s'écrit | **oui** (priorité 1) |
| `rc_a1_parallele` « Deux condensateurs côte à côte » | `figures.html?fig=fig_parallele` : figure statique + formule | `associations.html?vue=parallele` : curseurs C₁ et C₂, « Charger » couvre les armatures de charges (largeur ∝ C), u₁ = u₂, q₁, q₂, q = q₁ + q₂, C_eq calculée, condensateur équivalent plus grand | **oui** |
| `rc_a2_serie` « Deux condensateurs l'un après l'autre » | `figures.html?fig=fig_serie` : figure statique + formule | `associations.html?vue=serie` : même charge, u₁ = q/C₁, u₂ = q/C₂, u₁ + u₂ = u, C_eq plus petite | **oui** |
| `rc_s6_tableau` « Le tableau avant la courbe » | `courbe-charge.html?vue=tableau` : tableau de valeurs → points → courbe | non : le tableau est ici la méthode enseignée (valeurs à 0, τ, 5τ avant de tracer), la manip existante le transforme déjà en courbe | non |
| `rc_l8_calcul` « Calculer l'énergie » | `energie.html?vue=calcul` (poignée u_C déjà là) | déjà manipulable | non |
| `rc_m4_regimes`, `rc_s7_q_i`, `rc_s8_quatre` | simulations animées existantes | elles montrent déjà le phénomène | non |

## Ch. 7 — Dipôle RL (`phys_ch7_dipole_RL.json`)

| Diapo | À l'écran avant | Animation | Faite ? |
|---|---|---|---|
| `rl_l8_double` « Si I₀ double » | `energie.html?vue=calcul` : le calcul 0,025 J écrit, rien à manipuler ; puces avec deux calculs | `energie-carre.html` : curseurs I₀ et L ; « Établir le courant » fait grandir le carré de côté i (aire i²) sur des carreaux de 0,5 A et remplit la barre E_m ; I₀ double → 4 carreaux, « × 4 » ; L double → « × 2 seulement » | **oui** |
| `rl_s7_L` « Si L double », `rl_s8_R` « Si R augmente » | `influence.html` : déjà une poignée glissée sur la courbe (L′ ou R′) | déjà manipulable | non |
| `rl_m4_I0` « La valeur finale I₀ » | `courbe.html?vue=trace` | une manip R et L (I₀ = E/(R + r), L ne change pas le palier) ferait doublon avec `influence.html` de `rl_s7_L` | non (doublon) |
| `rl_b6_triangle`, `rl_b7_inductance` | `triangle.html` avec poignée | déjà manipulable | non |

## Ch. 8 — Circuit RLC (`phys_ch8_circuit_RLC.json`)

| Diapo | À l'écran avant | Animation | Faite ? |
|---|---|---|---|
| `lc_r3_ordre` « La résistance totale décide du régime » | `oscillogramme.html?vue=comparer` : trois petits écrans figés ; deux puces qui listent les trois cas | `regimes.html` : un seul curseur R + r (0 → 1500 Ω) ; « Basculer K » trace u_C(t) au ralenti, les sommets s'écrivent quand le spot y passe, le nom du régime s'écrit comme résultat ; les traces d'avant restent en pointillés ; « ordre » range les trois. Mêmes noms de moments et de repères que l'ancienne vue : le pointage existant reste valable | **oui** |
| `lc_p3_influence` « Si C (ou L) est multipliée par 4 » | `periode.html?vue=influence_C` : poignée sur le sommet de la courbe en pointillés | déjà manipulable | non |
| `lc_p2_charge` | `periode.html?vue=T0` : poignée E′ | déjà manipulable | non |
| `lc_k3_T0`, `lc_k2_k` | `entretien.html` : poignée k | déjà manipulable | non |
| `lc_r1_pseudo`, `lc_r2_aperiodique` | `oscillogramme.html` : poignée R | déjà manipulable | non |

## Ch. 9 — Transformations lentes et rapides (`phys_ch9_transformations_lentes_rapides.json`)

| Diapo | À l'écran avant | Animation | Faite ? |
|---|---|---|---|
| `tl_f7_palier` « Les courbes à deux concentrations » | `courbes.html?vue=concentration` : courbes imposées, aucune manip | `courbe-reglable.html?vue=concentration` : curseurs [I⁻]₀ et n(H₂O₂)₀ ; plus d'iodure → palier atteint plus tôt, même palier ; plus d'eau oxygénée (limitante) → palier plus haut ; « palier vers … min » et le palier en mmol s'écrivent ; bécher qui brunit. Mêmes moments et repères : pointage gardé | **oui** |
| `tl_f4_courbes` « Les courbes à deux températures » | `courbes.html?vue=temperature` : courbes imposées | `courbe-reglable.html?vue=temperature` : curseur θ (20 → 60 °C). Mêmes moments et repères : pointage gardé | **oui** |
| `tl_f3_agitation` « Pourquoi la chaleur accélère » | `facteurs.html?vue=temperature` : loupe animée, rien de compté | `rencontres.html?vue=temperature` : deux loupes (20 °C et θ réglable), une étoile à chaque rencontre I⁻–H₂O₂, « N rencontres par seconde » écrit sous chaque loupe, « même nombre d'entités : même état final » | **oui** |
| `tl_f6_rencontres` « Pourquoi la concentration accélère » | `facteurs.html?vue=concentration` : loupe, rien de compté | `rencontres.html?vue=concentration` : [I⁻]₀ réglable à droite, rencontres comptées ; le tuteur dilue lui-même (`set_parameters c_iodure 0,05`) sur « يعني درنا la dilution » | **oui** |
| `tl_f8_variable` « Une seule variable à la fois » | tableau des trois expériences | le tableau est la donnée que l'examen fournit (règle 28 : il reste) | non |
| `tl_r5_echelle` « Rapide ou lente, selon nos yeux » | `bechers.html?vue=echelle` | une échelle de durées : pas un paramètre à régler | non |
| `tl_f2_bains`, `tl_f5_concentre` | `facteurs.html` (béchers animés, poignée thermomètre) | déjà animés, avec la voix qui suit les béchers | non |
| `tl_t4_courbes`, `tl_n1_lecture` | `courbes.html` (catalyseur, sujet national) | courbes de l'énoncé du national : à lire telles quelles | non |

Aucune diapo n'a demandé de nouvelle voix : toutes les animations construites suivent le texte déjà enregistré.

## Fichiers créés

- `frontend/public/media/simulations/physics/dipole-rc-tableau/tau-rc.html` → `rc_t2_influence`
- `frontend/public/media/simulations/physics/dipole-rc-tableau/associations.html` (`?vue=parallele` | `serie`) → `rc_a1_parallele`, `rc_a2_serie`
- `frontend/public/media/simulations/physics/dipole-rl-tableau/energie-carre.html` → `rl_l8_double`
- `frontend/public/media/simulations/physics/circuit-rlc-tableau/regimes.html` → `lc_r3_ordre`
- `frontend/public/media/simulations/chimie/transformations-lentes-rapides-tableau/courbe-reglable.html` (`?vue=temperature` | `concentration`) → `tl_f4_courbes`, `tl_f7_palier`
- `frontend/public/media/simulations/chimie/transformations-lentes-rapides-tableau/rencontres.html` (`?vue=temperature` | `concentration`) → `tl_f3_agitation`, `tl_f6_rencontres`

Chaque manip : cadre 760 × 420 (kit `shared/tableau` + `commun.js` du dossier), un bouton principal, un ou deux curseurs, `repere` sur chaque élément nommé par la voix, `moments` nommés + `play_until`, `set_parameters`, `pause` / `resume` / `reset`, `ce_qui_se_voit` dans l'état.

## Fichiers modifiés

- `backend/data/courses/phys_ch6_dipole_RC.json` : `rc_t2_influence`, `rc_a1_parallele`, `rc_a2_serie` (visual, puces montrées par l'animation retirées, pointage réécrit).
- `backend/data/courses/phys_ch7_dipole_RL.json` : `rl_l8_double` (idem).
- `backend/data/courses/phys_ch8_circuit_RLC.json` : `lc_r3_ordre` (visual, deux puces retirées ; pointage inchangé).
- `backend/data/courses/phys_ch9_transformations_lentes_rapides.json` : `tl_f4_courbes`, `tl_f7_palier` (visual, puces ; pointage inchangé), `tl_f3_agitation`, `tl_f6_rencontres` (visual, puces, pointage complété).

Les quatre JSON étaient en fins de ligne CRLF sur le disque : ils sont réécrits en LF (`ensure_ascii=False`, `indent=2`, saut de ligne final gardé). Diff structurel : seules les diapos ci-dessus ont changé.
