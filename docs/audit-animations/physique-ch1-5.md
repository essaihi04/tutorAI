# Audit des animations — physique, chapitres 1 à 5

Règle 28 du professeur (14 novembre 2026) : une diapo qui compare des valeurs, montre l'effet d'un paramètre ou décrit des étapes montre une petite animation à la craie que l'élève manipule (un bouton, au plus deux curseurs) ; les valeurs sont le résultat de ce qu'on voit. Modèle : `ondes-tableau/milieux.html` sur `wx_c2_facteurs` (non modifié).

Méthode : chaque diapo des cinq cours a été relue (titre, `screen_content`, visuel, voix `speech_text.mixed`). Ne sont pas candidates : la fiche bilan (`*_bl_fiche`, `wx_b3_bilan`, `*_b1_bilan`, `*_z1_bilan`), la carte (`*_cr_carte`, `wx_b4_carte`, `*_b2_carte`, `*_z2_carte`), les diapos dont la simulation montre déjà le point, les énoncés d'examen (`*_x*`), les diapos de rédaction et les conversions d'unités (rien qui bouge).

Pour chaque animation construite : cadre 760 × 420, kit `shared/tableau` + `commun.js` du dossier, `repere` sur chaque élément nommé par la voix, `moments` nommés + `play_until`, `set_parameters` pour chaque curseur, `pause` / `resume` / `reset`, `ce_qui_se_voit` dans l'état. La voix (`speech_text`) n'a pas été modifiée : le `pointage` est réécrit sur des extraits exacts de la voix (chaque `mot` vérifié, unique dans le texte, sauf les `centre:N` déjà existants), les entrées `centre` (formules écrites) sont gardées.

Classement : ★★★ forte valeur, ★★ moyenne, ★ faible.

## Chapitre 1 — Ondes mécaniques progressives (`phys_ch1_waves_exemple`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `wx_i3_types` ★★★ | Tableau « onde / perturbation-propagation / type / dimensions », aucun visuel | Quatre cases jouées tour à tour : corde (M monte et descend, l'onde va à droite → ⊥ transversale), ressort (M avance et recule → ∥ longitudinale), son dans l'air (grains d'air qui vont et viennent → longitudinale, « pas dans le vide »), eau vue de dessus (cercles) ; à la fin les dimensions 1, 1, 3, 2 s'écrivent | **Oui** — `ondes-tableau/types.html` ; tableau retiré |
| `wx_l1_aspect` ★ | Tableau « graphe / axe / front » + simulation `corde.html?vue=aspect` | La simulation montre déjà les deux graphes et le front | Non — déjà couvert ; le tableau pourrait être retiré de l'écran (à décider) |
| `wx_b2_national` ★ | Tableau « mot-code / cas / relation » | — | Non — méthode d'examen, pas un phénomène |
| `wx_i2_definition`, `wx_b1_redaction` | Puces (définition, rédaction) | — | Non — rien qui bouge |

## Chapitre 2 — Ondes progressives périodiques (`phys_ch2_ondes_periodiques`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `op_s3_dispersif` ★★★ | Tableau « milieu / N / λ / v » + puces de valeurs, aucun visuel | Eau à 20 Hz puis N′, air à 1000 Hz puis N′ : l'onde remplit la rangée, la règle se pose sur λ, v = λ·N s'écrit ; « v′ ≠ v » (eau) / « v′ = v » (air), puis « eau : milieu dispersif » / « air : non dispersif ». Deux curseurs : N′ de l'eau (22–40 Hz), N′ de l'air (1500–4000 Hz) | **Oui** — `ondes-periodiques-tableau/dispersif.html` ; tableau et puces de valeurs retirés (définition et méthode gardées) |
| `op_p3_methode` ★★★ | Liste en quatre étapes, aucun visuel | Corde qui vibre (λ = 4 cm), M et P avec leur sens de mouvement ; λ posée, puis d, les λ comptées, d / λ, la conclusion. Curseur d (1–14 cm) ; la voix règle d = 12 cm (« trois : en phase ») puis 9,2 cm (« deux virgule trois ») | **Oui** — `ondes-periodiques-tableau/methode-phase.html` ; liste retirée |
| `op_t4_inverse` ★★ | Puces « T = 0,5 s, N = 2 Hz, 1/0,5 = 2 », aucun visuel | Un point M vibre, son film y(t) se trace pendant une seconde, les périodes sont numérotées : 2 périodes en 1 s → N = 2 Hz, puis 1 / T = 2. Curseur T (0,1–1 s, jamais 0,02 s : la question de la diapo reste à faire) | **Oui** — `ondes-periodiques-tableau/frequence.html` ; deux puces retirées, « N = 1 / T (et T = 1 / N) » gardée |
| `op_t7_oscillo` ★★ | Figure fixe + quatre étapes de lecture | Oscilloscope dont on règle la sensibilité horizontale : le nombre de divisions change, T reste la même | Non — la voix lit des nombres fixes (5 div, 0,1 ms/div) ; faisable plus tard sur la même voix |
| `op_c2_relation` ★ | Puces de formules, aucun visuel | `corde.html?vue=avance` montre déjà « une période, un λ » (diapo `op_c1_avance`) | Non — **nécessite une nouvelle voix** (la voix ne lit que des formules) |
| `op_c3_rediger`, `op_t5_convertir` | Rédaction, conversions | — | Non — rien qui bouge |

## Chapitre 3 — Propagation d'une onde lumineuse (`phys_ch3_ondes_lumineuses`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `ol_n4_indice` ★★★ | Figure fixe « tableau vide / milieu » + puces « air ≈ 1 ; eau 1,33 ; verre 1,5 » | Le vide à gauche, le milieu à droite : trois éclairs partent ensemble à c, entrent dans l'air, l'eau, le verre, ralentissent (leur onde se resserre) ; à l'arrivée v puis n = c / v s'écrivent ; « v < c », « n sans unité, n ≥ 1 ». Curseur : indice du 3ᵉ bloc (1,00–2,40) | **Oui** — `ondes-lumineuses-tableau/indice.html` ; puces de valeurs retirées. La voix dit « هادا هو الجدول » (voici le tableau) : elle désigne maintenant les deux colonnes vide / milieu de l'animation |
| `ol_t2_fente_plus_fine`, `ol_t3_couleur`, `ol_c2_haut_bas` | Puces de comparaison | `diffraction.html` règle déjà a, λ, D par la voix | Non — déjà couvert |
| `ol_n5_lambda_n` ★ | Figure fixe `fig_vide_milieu` | `milieu.html` (ou `indice.html`) montre l'onde qui se resserre | Non — la voix suit la démonstration écrite, gain faible |
| `ol_p4_dispersif` ★★ | Figure fixe des trois phénomènes | Fente / prisme / bloc côte à côte | Non — **nécessite une nouvelle voix** (la voix compare par des mots, pas par ce qu'on voit) |
| `ol_l1_metre`, `ol_l6_isoler`, `ol_x*` | Conversions, algèbre, énoncés | — | Non |

## Chapitre 4 — Décroissance radioactive (`phys_ch4_radioactivite`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `ra_t4_pourcentages` ★★★ | Figure fixe : trois lignes écrites | Cent noyaux en grille : 30 se désintègrent → « il reste 70 %, N = 0,70·N₀ » ; 90 → « il reste 10 % » ; nouvel échantillon, deux demi-vies : 100 → 50 → 25 → « 75 % désintégrés ». Curseur « désintégrés : x % » : la grille se colore, la traduction s'écrit | **Oui** — `radioactivite-tableau/pourcentages.html` ; trois puces retirées, « Puis t = (1/λ)·ln(N₀/N) » gardée |
| `ra_l6_lambda` ★★ | Figure fixe des unités + quatre puces | Deux échantillons de 64 noyaux : iode 131 (λ en j⁻¹ et s⁻¹) et carbone 14 (λ en an⁻¹ et s⁻¹), λ·t sans unité, puis 40 jours passent : l'iode se vide, le carbone 14 reste. Curseur λ de l'échantillon de gauche | **Oui** — `radioactivite-tableau/lambda.html` ; puces retirées |
| `ra_r2_caracteres` ★★★ | `population.html?vue=hasard` (12 noyaux) | Ajouter un curseur de température / pression qui ne change rien au rythme (la voix le dit : « واخا نزيدو الحرارة ولا la pression، ما كيتبدل والو ») | Non — `population.html` sert quatre diapos (563 lignes) ; à faire en priorité ensuite, sans nouvelle voix |
| `ra_c4_fils_pere` ★★ | Figure fixe : père, fils, rapport | Échantillon père → fils, r = N(fils)/N(père) qui grandit | Non — la question de la diapo (« autant de fils que de pères : combien de demi-vies ? ») serait donnée par l'animation ; il faudrait s'arrêter avant |
| `ra_l2_proportion` | Tableau jour par jour **dans** `population.html` | Les valeurs y sont déjà le résultat du tirage en direct | Non — déjà conforme |
| `ra_a4_unites`, `ra_a5_masse`, `ra_x*` | Conversions, énoncés | — | Non |

## Chapitre 5 — Noyaux, masse et énergie (`phys_ch5_energie_nucleaire`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `en_n2_comparaison` ★★★ | Figure fixe : tableau à deux colonnes | Une fission et une fusion, une jauge d'énergie (0–900 MeV) dans chaque case : 185 contre 17,6 MeV ; par nucléon 0,78 contre 3,5 MeV ; à masse égale, 47 fusions (≈ 827 MeV) contre une fission | **Oui** — `energie-nucleaire-tableau/comparaison.html` ; deux puces de valeurs retirées, la conclusion gardée |
| `en_s1_stabilite` ★★ | Figure fixe : ⁶⁰Ni / ⁵⁶Ni | Partage de E_ℓ entre les nucléons, ou la courbe d'Aston | Non — `aston.html` n'a pas ⁵⁶Ni et l'écart 8,78 / 8,64 est invisible sur la courbe ; une animation dédiée apporterait peu |
| `en_m2_einstein` ★ | Figure fixe E = m·c² | Curseur m → E | Non — la voix suit un calcul pour 1 g, gain faible |
| `en_n1_echantillon` ★ | Figure fixe : lignes du calcul | Curseur m → N → E, comparé au pétrole | Non — même raison |
| `en_m3_unites`, `en_m4_931`, `en_b2_methode`, `en_e2_formule`, `en_c*` | Conversions, méthodes, cas types | — | Non |

## Fichiers créés

- `frontend/public/media/simulations/physics/ondes-tableau/types.html` (`wx_i3_types`)
- `frontend/public/media/simulations/physics/ondes-periodiques-tableau/dispersif.html` (`op_s3_dispersif`)
- `frontend/public/media/simulations/physics/ondes-periodiques-tableau/methode-phase.html` (`op_p3_methode`)
- `frontend/public/media/simulations/physics/ondes-periodiques-tableau/frequence.html` (`op_t4_inverse`)
- `frontend/public/media/simulations/physics/ondes-lumineuses-tableau/indice.html` (`ol_n4_indice`)
- `frontend/public/media/simulations/physics/radioactivite-tableau/pourcentages.html` (`ra_t4_pourcentages`)
- `frontend/public/media/simulations/physics/radioactivite-tableau/lambda.html` (`ra_l6_lambda`)
- `frontend/public/media/simulations/physics/energie-nucleaire-tableau/comparaison.html` (`en_n2_comparaison`)

## Fichiers modifiés

Seuls `visual`, `screen_content` et `concentration` (pointage, variante ; `demarrer: start` retiré là où il existait, le premier `play_until` lance la scène) des huit diapos ci-dessus ont changé ; `speech_text`, `audio`, questions et exercices sont intacts (vérifié diapo par diapo contre une copie d'avant).

- `backend/data/courses/phys_ch1_waves_exemple.json` — `wx_i3_types`
- `backend/data/courses/phys_ch2_ondes_periodiques.json` — `op_t4_inverse`, `op_p3_methode`, `op_s3_dispersif`
- `backend/data/courses/phys_ch3_ondes_lumineuses.json` — `ol_n4_indice`
- `backend/data/courses/phys_ch4_radioactivite.json` — `ra_l6_lambda`, `ra_t4_pourcentages`
- `backend/data/courses/phys_ch5_energie_nucleaire.json` — `en_n2_comparaison`

Fins de ligne : `phys_ch1` était en LF et le reste ; `phys_ch2` à `phys_ch5` étaient en CRLF et le restent (les réécrire en LF aurait changé toutes les lignes). Retour à la ligne final gardé.

## Vérifications faites

- `node --check` du script de chaque page : OK.
- Chaque page jouée en Chrome sans tête, servie localement, en appelant les commandes du tuteur (`play_until` sur chaque moment, `set_parameters`) : images vérifiées, aucun texte hors cadre (`__horsCadre` vide).
- Lecteur : `cours-ondes.html?cours=phys_ch2_ondes_periodiques&diapo=op_s3_dispersif` charge bien `dispersif.html` et la piste `op_s3_dispersif_v11.mp3` (les erreurs 500 viennent de l'API absente en local).
- Non vérifié : la lecture complète voix + animation dans le lecteur (le panneau du navigateur était masqué, les animations ne tournent pas), donc le calage réel des `play_until` sur la voix ; `preparer_reponses.py verifier` n'a pas été lancé.
