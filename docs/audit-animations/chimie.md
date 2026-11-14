# Audit « animations au lieu de tableaux » — chimie (ch. 10 à 13)

Règle (14 novembre 2026, professeur règle 28, cours-concentration étape 3) : une diapo qui compare des valeurs, montre l'effet d'un
paramètre ou décrit des étapes montre une petite animation à la craie que l'élève manipule (un bouton, au plus deux curseurs) ;
les valeurs sont le RÉSULTAT de ce qu'on voit. La voix enregistrée (`speech_text`) n'a pas été modifiée : les `pointage` sont
réécrits sur des extraits exacts du texte parlé (vérifiés un par un).

Constat général : les quatre cours n'ont aucune diapo avec `screen_content.table`. Toutes les diapos ont déjà une simulation à la
craie. Les candidates sont donc les diapos dont la simulation **déroule une liste ou un tableau dessiné sans rien à manipuler**
(pas de poignée) alors que la notion est l'effet d'un paramètre (température, concentration, pH, quantité initiale).
Écartées d'office : les fiches bilan (`*_bl_fiche`), les cartes (`*_o1_carte`, `*_cr_carte`), les figures des nationaux
(`*_n*`, `*_p4_*`, `*_p6_*` : figures données par le sujet).

## Moteur commun

`deroule.js` (copie identique dans les quatre dossiers `chimie/<cours>-tableau/`) : étapes nommées = `moments`,
`play_until {moment}` joue jusqu'à la fin de l'étape et s'y fige (une étape déjà montrée ne rejoue pas, pour suivre la voix),
`set_parameters` change le curseur sans rembobiner, `set_time`, `start`, `pause` (garde la cible), `resume`, `reset`,
`ce_qui_se_voit` dans l'état, écriture à la craie de chaque élément au moment où son étape commence, formules H₃O⁺, HO⁻, SO₄²⁻
rendues avec indices et charges. Dans les diapos câblées, `concentration.demarrer` passe de `start` à `reset` (la scène se
remet à zéro quand la voix commence, puis chaque `play_until` montre ce que la voix dit) et une `variante` est ajoutée.

## Ch. 10 — Suivi temporel, vitesse de réaction (`phys_ch10_cinetique`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `ci_v8_temperature` | `vitesse.html?vue=temperature` : deux courbes 20/40 °C tracées, puces avec les pentes 0,25/0,75 et v(0) = 7,5 | Deux béchers qui brunissent (20 °C témoin, θ réglable 10–60 °C), leurs courbes x(t) qui se tracent, tangentes, pentes et v(0) écrites sur place, même palier | **Oui** — `cinetique-tableau/temperature.html?vue=vitesse` (valeur la plus forte : la demande « changer la température et voir les changements ») |
| `ci_h4_comparer` | `demi-reaction.html?vue=comparer` : deux t₁/₂ lus (5,5 / 1,8 min), puces | Même manip, vue « demi » : x_f/2, les deux verticales, t₁/₂ écrits ; curseur θ | **Oui** — `temperature.html?vue=demi` |
| `ci_a2_limitant` | `avancement.html?vue=limitant` : les deux hypothèses écrites (calcul), pas de mouvement | Trois barres H₂O₂ / I⁻ / I₂ qui bougent quand x avance ; les deux hypothèses marquées sur l'axe des x ; la barre de H₂O₂ se vide la première ; curseur n₀(I⁻) qui rend I⁻ limitant | **Oui** — `cinetique-tableau/limitant.html` (les hypothèses restent écrites : le barème les demande) |
| `ci_v6_epuisement` | loupe sur les entités de réactif | — | Non : déjà animée (loupe qui se vide) |
| `ci_v5_diminue` | trois tangentes à 0, 8, 20 min | Tangente glissante | Non : `vitesse.html` a déjà une poignée de date (vue tangente) ; gain faible |
| `ci_m1_mesures` | liste t → x | — | Non : `suivi.html` déroule déjà la mesure ; les valeurs servent au tracé suivant |
| `ci_g2_ions` | deux afficheurs, on ajoute des ions | — | Non : déjà une manip (l'afficheur monte) |
| `ci_a1_tableau`, `ci_a6_composition` | tableau d'avancement | — | Non : l'examen demande d'écrire le tableau ; `composition` a déjà une poignée t |

## Ch. 11 — Transformations dans les deux sens (`phys_ch11_transformations_deux_sens`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `td_d2_taux` | `dilution.html?vue=taux` : colonne τ ajoutée au tableau C · pH, barres | Un bécher dilué 10 fois puis encore 10 fois, pH-mètre qui se stabilise, **loupe sur 25 molécules** (1, 3, puis 8 ont réagi), les trois lignes τ = 10^(−pH)/C écrites au moment de la mesure, barres ; curseur C (1,0·10⁻¹ à 1,0·10⁻⁵) pour préparer sa solution | **Oui** — `transformations-deux-sens-tableau/diluer.html` |
| `td_d1_dilution` | `dilution.html?vue=mesures` : protocole de dilution animé, puis tableau C · pH | Même manip que `td_d2` | Non — **nécessite une nouvelle voix** : le texte dicte le protocole pipette/fiole et finit par « نكتبو كلشي ف le tableau » ; la vue actuelle montre déjà le protocole pas à pas |
| `td_d3_nature` | trois béchers, trois acides, barres τ | Curseur « acide » | Non — **nécessite une nouvelle voix** (le texte suit les trois béchers et « le tableau ») ; la vue actuelle compare déjà en barres ; un curseur à trois crans n'apporte pas de lien de cause à effet |
| `td_c1_ions` | deux béchers, deux conductivités | — | Non : comparaison déjà montrée par deux afficheurs |
| `td_p1_ph`, `td_p2_calcul` | pH ↔ [H₃O⁺] | — | Non : `ph.html?vue=calcul` a déjà une poignée pH |
| `td_e5_esterification` | courbe x(t) vers le palier | — | Non : déjà une courbe qui monte |

## Ch. 12 — État d'équilibre (`phys_ch12_etat_equilibre`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `ee_f4_bilan` | `facteurs.html?vue=bilan_dilution` : « le tableau à retenir » (C, [H₃O⁺], pH, τ, K) | On dilue sous les yeux de l'élève : le pH-mètre monte, puis quatre lignes **avant → après** avec flèche (C ↓, [H₃O⁺] ↓ et pH ↑, τ ↑, K = 1,6·10⁻⁵ inchangée dans le cadre jaune), puis le piège ; curseur « diluer jusqu'à C » (5·10⁻³ à 1·10⁻⁵) : τ grandit, K reste | **Oui** — `etat-equilibre-tableau/diluer.html` |
| `ee_k1_trois` | `constante.html?vue=trois_c` : trois béchers, colonnes τ et Qr,éq | Curseur C, τ change, Qr,éq reste | Non — **nécessite une nouvelle voix** : le texte lit « السطر اللول… la colonne ديال tau… la colonne ديال Q r » ligne par ligne ; la manip équivalente est déjà sur `ee_f4_bilan` |
| `ee_f1_dilution` | `facteurs.html?vue=dilution` : trois barres τ, même K | — | Non : barres déjà dessinées, et la manip C ↔ τ existe sur `ee_f3_courbe` (poignée C) et `ee_f4_bilan` |
| `ee_i3_au_cours` | Qr qui monte jusqu'à Qr,éq | — | Non : `quotient.html?vue=au_cours` a déjà une poignée d'avancement |
| `ee_f2_nature` | deux acides, deux K, deux τ | — | Non : deux valeurs fixes, la comparaison est déjà en barres |

## Ch. 13 — Réactions acide-base (`phys_ch13_acides_bases`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `ab_i2_virage` | `predominance.html?vue=virage` : bande du BBT puis **liste** des quatre zones de virage | L'axe des pH, la bande du BBT peinte (jaune, vert, bleu), sa zone de virage encadrée, pKa ≈ 7,0, puis les trois autres bandes en escalier ; **curseur pH** (aussi glissé sur l'axe) : une pastille par indicateur prend sa couleur à ce pH | **Oui** — `acides-bases-tableau/indicateurs.html` |
| `ab_e3_indicateur` | courbe de dosage J + bandes de quatre indicateurs | Même bandes + curseur sur le saut de pH | Non : il faudrait la courbe de dosage dans la manip ; la vue actuelle (`exploiter.html`) montre déjà bandes, choix et couleur du bécher |
| `ab_c1_acides` / `ab_c2_bases` | deux béchers, tableau pKa · Ka · pH · τ, barres | Curseur pKa : pH et τ suivent | Non — **nécessite une nouvelle voix** : le texte dit « le tableau كيتعمر: p K a، K a، p H، و tau » |
| `ab_w3_solutions` | axe des pH, barres [H₃O⁺] / [HO⁻] | — | Non : `eau.html?vue=solutions` a déjà la poignée pH |
| `ab_p2_domaines`, `ab_p3_distribution` | domaines, distribution | — | Non : `predominance.html` a déjà la poignée pH |
| `ab_c3_classement` | axe des pKa des six couples | — | Non : un classement (pas un paramètre) déjà dessiné sur un axe |
| `ab_d4_courbe` | courbe pH = f(V_B) avec points | — | Non : `dosage.html?vue=courbe` a déjà la poignée V_B |

## Fichiers créés

- `frontend/public/media/simulations/chimie/cinetique-tableau/deroule.js` (et copies identiques dans `transformations-deux-sens-tableau/`, `etat-equilibre-tableau/`, `acides-bases-tableau/`)
- `frontend/public/media/simulations/chimie/cinetique-tableau/temperature.html` (vues `vitesse`, `demi` ; curseur θ 10–60 °C)
- `frontend/public/media/simulations/chimie/cinetique-tableau/limitant.html` (curseur n₀(I⁻) 1,0–10,0 mmol)
- `frontend/public/media/simulations/chimie/transformations-deux-sens-tableau/diluer.html` (curseur C 1,0·10⁻¹ – 1,0·10⁻⁵ mol/L)
- `frontend/public/media/simulations/chimie/etat-equilibre-tableau/diluer.html` (curseur C après dilution 5,0·10⁻³ – 1,0·10⁻⁵ mol/L)
- `frontend/public/media/simulations/chimie/acides-bases-tableau/indicateurs.html` (curseur pH 0–14)

## Diapos modifiées (visual, puces retirées, pointage, demarrer → reset, variante)

| Cours | Diapo | Simulation | Puces gardées |
|---|---|---|---|
| `phys_ch10_cinetique` | `ci_v8_temperature` | `temperature.html?vue=vitesse` | « Rappel : la température est un facteur cinétique. » |
| `phys_ch10_cinetique` | `ci_h4_comparer` | `temperature.html?vue=demi` | le piège « paliers différents » |
| `phys_ch10_cinetique` | `ci_a2_limitant` | `limitant.html` | « H₂O₂ est le réactif limitant… » |
| `phys_ch11_transformations_deux_sens` | `td_d2_taux` | `diluer.html` | « Plus la solution est diluée, plus τ est grand. » |
| `phys_ch12_etat_equilibre` | `ee_f4_bilan` | `diluer.html` | le piège « τ dépend de l'état initial ; K ne dépend pas de l'état initial » |
| `phys_ch13_acides_bases` | `ab_i2_virage` | `indicateurs.html` | la définition de la zone de virage et « encadre le pKa » |

`speech_text` et `audio` inchangés (vérifié par comparaison JSON avec les originaux) ; seules ces six diapos diffèrent.

## Non vérifié

- La lecture dans le lecteur du cours (voix + gestes du tuteur) : le panneau du navigateur était caché, l'animation du tuteur 3D
  (qui transmet les commandes) ne tourne pas dans ce cas. Vérifié : la diapo charge bien la nouvelle simulation dans l'iframe, et
  chaque simulation répond à `reset`, `play_until` (tous les moments), `set_parameters`, `start` via `executeAICommand`
  (captures d'écran à chaque étape, aucun texte hors cadre, aucune erreur de chargement).
- Le contrôle `preparer_reponses.py verifier` (hors du dépôt) n'a pas été lancé ; chaque `mot` a été vérifié comme extrait exact
  de `speech_text.mixed`.
