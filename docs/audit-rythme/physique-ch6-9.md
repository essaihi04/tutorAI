# Audit « rythme et départ de zéro » — physique-chimie, cours 6 à 9

14 novembre 2026. Règles appliquées : professeur **33** (une chose à la fois : le principe d'abord, une question pour le vérifier, chaque expérience sur son arrêt, le résultat décisif trouvé par l'élève) et **34** (départ de zéro : les notions des années d'avant enseignées, chaque notion dite deux fois de deux façons), avec 27 (ne demander que ce qui est enseigné), 28 (animations), 30 (question d'observation) et 32 (objets peints).

Rien n'a été modifié dans les cours en ligne. Les nouvelles versions complètes sont en attente :

| cours | fichier en attente | diapos | séances | blocs | durée |
|---|---|---|---|---|---|
| Dipôle RC | `backend/data/courses/en_attente/phys_ch6_dipole_RC.json` | 48 → 56 | 4 → 6 | 12 → 17 | 198 → 218 min |
| Dipôle RL | `backend/data/courses/en_attente/phys_ch7_dipole_RL.json` | 48 → 52 | 4 → 5 | 12 → 13 | 198 → 210 min |
| Circuit RLC | `backend/data/courses/en_attente/phys_ch8_circuit_RLC.json` | 48 → 52 | 4 → 5 | 12 → 14 | 196 → 208 min |
| Transformations lentes et rapides | `backend/data/courses/en_attente/phys_ch9_transformations_lentes_rapides.json` | 36 → 41 | 3 → 4 | 9 → 11 | 150 → 164 min |

Sur chaque diapo nouvelle ou dont la voix a changé, `audio.mixed` est retiré. Les diapos dont la voix ne change pas gardent leur piste, même quand une question d'observation y est ajoutée : la voix s'arrête sur `apres_mot` et reprend, elle n'est pas réécrite. Chaque bloc garde **une seule** question « À toi » ; quand une question devenait doublon d'une question d'observation, ou quand le principe d'une expérience prenait la place de la question du bloc, l'ancienne question passe dans la réserve de fin de cours de sa diapo (`exercices_fin_de_cours`, réactions dans `reponses_fin_de_cours`), avec son énoncé et ses réactions déjà voixés.

Légende : **vite** = plusieurs expériences, cas ou idées d'un coup ; **donné** = résultat décisif dit au lieu d'être trouvé ; **prérequis** = notion d'une année d'avant utilisée comme connue ; **une fois** = notion dite d'une seule façon.

## Ce qui est commun aux quatre cours

- La diapo d'ouverture « Trois gestes à avoir en main » (`*_o2_prerequis`, ou `tl_o2_bases`) disait trois à quatre notions en trente secondes, sans rien montrer : c'est l'exemple même de la règle 33 non tenue, et de la règle 34 (les notions sont nommées comme connues). Elle est **remplacée** dans chaque cours par des diapos de rappel, une notion par diapo, chacune avec une animation et dite deux fois (une première façon, puis « دابا بطريقة أخرى » : une image de la vie, une analogie), et relue en français mot pour mot après « نعاود نقرا ».
- Les rappels d'une notion utilisée plus loin (dérivée, exponentielle, cosinus, mole, concentration) ne sont pas tous au début : chacun est placé juste avant la diapo qui s'en sert, pour que l'élève l'ait encore en tête.
- Deux questions d'observation par cours (le maximum de la règle 30), sur les deux résultats décisifs qu'une simulation montre : la voix s'arrête juste avant de dire le résultat, la simulation tait sa conclusion (`sim_avant: {conclusions: false}`), puis la rend (`sim_apres: {conclusions: true}`) ; la phrase suivante de la voix confirme la réponse.

## 1. Dipôle RC (`phys_ch6_dipole_RC`)

### Ce qui allait trop vite (règle 33)

| diapo | constat | ce qui a été fait |
|---|---|---|
| `rc_o2_prerequis` | **vite** + **prérequis** : loi d'Ohm, additivité, puissances de dix et dérivée de e^(−2t) en une diapo, sans image. | Retirée. Remplacée par `rc_rp1_courant`, `rc_rp2_tension`, `rc_rp3_ohm`, `rc_rp4_additivite`, `rc_rp5_puissances` (bloc « Les bases »), plus `rc_rp6_derivee` et `rc_rp7_exponentielle` placés avant leur usage. |
| `rc_c2_aiguilles` | **vite** : le montage, les deux appareils, la fermeture de K, le saut de l'ampèremètre, la montée du voltmètre et la conclusion en 28 s. Le principe (« que mesure chaque appareil ? ») n'était jamais posé. | Nouvelle diapo **`rc_c2a_principe`** avant : le montage seul, K ouvert, ce que mesure chaque appareil et le but de l'expérience, avec une question de vérification (« que mesure l'ampèremètre ? ») qui devient la question du bloc. `rc_c2_aiguilles` garde sa voix et reçoit une question d'observation (ci-dessous). La question de `rc_c1_plaques` passe en réserve. |
| `rc_t2_influence` | **vite** et **incomplet** : R doublée puis E en une phrase ; l'effet de C, pourtant au cadre (C6), n'était jamais montré (la simulation `tau-rc.html` avait déjà le moment `C_double`). | Question d'observation sur R doublée. Nouvelle diapo **`rc_t3_C`** : la deuxième expérience (C doublée) sur son propre arrêt, son résultat, τ = R·C relu, avec la question du bloc. |
| `rc_l7_energie` | **vite** : la lampe, l'énergie stockée, la formule, l'origine du ½ par la dérivée et l'effet du carré. | Non découpée dans ce passage : sa voix est enregistrée et la diapo suivante (`rc_l8_calcul`) reprend le carré. À découper si l'on revoice la séance (lampe seule, puis E_e = ½·C·u_C², puis le carré). |
| `rc_d2_continuite` | trois idées : u_C continue, nouvelle origine des temps, i qui saute et change de signe. | Gardée (la question du bloc y porte sur i), mais le bloc est raccourci à deux diapos (`rc_d1_decharge`, `rc_d2_continuite`) pour lui laisser le temps. |
| `rc_m4_regimes` | régime permanent puis continuité de u_C à t = 0 dans la même voix. | Signalé, non modifié (la continuité est reprise en entier dans `rc_d2_continuite`). |
| `rc_e7_tableau` | huit équations dans un tableau. | Gardé : c'est un tableau-bilan, exception prévue par la règle 28 ; chaque équation a eu sa diapo avant. |

### Résultats décisifs trouvés par l'élève (règle 30)

- **`rc_c2_aiguilles`** — après « شوف l'aiguille ديال l'ampèremètre: », la voix s'arrête : « Après son saut, que fait l'aiguille de l'ampèremètre ? » (reste en haut / **redescend vers zéro** / continue de monter). Geste : `play_until electrons` (l'aiguille finit de redescendre). `condensateur.html` tait la phrase « l'aiguille saute puis redescend » et le motif de l'arrêt sur image.
- **`rc_t2_influence`** — après « la courbe الجديدة » : « R a doublé. Compare la nouvelle courbe à l'ancienne, en pointillés » (plus vite et plus haut / **plus lentement, au même E** / la même). Geste : `highlight courbe_2`. `tau-rc.html` tait « τ × 2 : charge plus lente » et le motif « … deux fois plus lente ».

### Prérequis enseignés depuis zéro (règle 34)

| notion | diapo | première façon | deuxième façon |
|---|---|---|---|
| courant, intensité, ampèremètre en série, sens conventionnel | `rc_rp1_courant` | circuit peint, électrons qui circulent, lampe qui s'allume | l'eau qui coule : la charge qui passe en une seconde |
| tension entre deux points, voltmètre en dérivation, u = 0 sur un fil | `rc_rp2_tension` | flèche u_AB aux bornes de la lampe, voltmètre | deux réservoirs à deux hauteurs |
| loi d'Ohm, convention récepteur | `rc_rp3_ohm` | deux mesures, i double → u_R double, la droite | une résistance plus grande : droite plus raide (curseur R) |
| additivité des tensions | `rc_rp4_additivite` | trois flèches 6 = 2 + 4 | l'escalier : monter de E, redescendre de E (curseur u_C) |
| puissances de dix (milli, micro, nano) | `rc_rp5_puissances` | 47 µF = 47·10⁻⁶ F | la virgule qui recule de six rangs |
| dérivée = pente de la tangente | `rc_rp6_derivee` (avant `rc_c5_intensite`, qui disait « i = dq/dt, c'est la pente » sans l'avoir enseigné) | la corde qui devient tangente | le compteur de vitesse de la voiture |
| exponentielle e^(−t/τ) : 1, 0,37, jamais 0 ; 1 − e^(−t/τ) | `rc_rp7_exponentielle` (avant `rc_s1_derivee`, qui dérivait une fonction jamais présentée) | les deux courbes | le réservoir qui se vide |

### Notions dites une seule fois

Les sept rappels sont chacun dits deux fois. `rc_t3_C` explique τ plus grand par « un grand verre sous le même robinet » après le calcul. `rc_c2a_principe` redit le rôle des appareils d'une seconde façon (« un appareil regarde le courant qui entre, l'autre la tension entre les plaques »). Restent dites d'une seule façon, sans être touchées ici : `rc_c4_capacite` (q = C·u_C, un exemple) et `rc_s4_condition` (la constante B par la condition initiale).

## 2. Dipôle RL (`phys_ch7_dipole_RL`)

### Ce qui allait trop vite

| diapo | constat | ce qui a été fait |
|---|---|---|
| `rl_o2_prerequis` | **vite** + **prérequis** : loi d'Ohm, additivité, dérivée de e^(−t/τ) et une question de calcul sur une fonction jamais montrée. | Retirée. `rl_rp1_ohm`, `rl_rp2_additivite` (avec une bobine peinte : vue `additivite&dipole=bobine`), `rl_rp3_derivee` (la pente, puis di/dt « la vitesse à laquelle i change »), et `rl_rp4_exponentielle` avant `rl_s1_forme`. L'ancienne question (dériver e^(−t/τ)) passe dans la réserve de `rl_rp4_exponentielle`. |
| `rl_b2_lampes` | **vite** : le montage des deux branches, la seule différence (la bobine), la fermeture et les deux résultats en 30 s. | Nouvelle diapo **`rl_b2a_principe`** : les deux branches, « une seule différence, la bobine », ce qu'on va regarder ; question de vérification (« qu'est-ce qui différencie les deux branches ? »). Question d'observation sur `rl_b2_lampes`. |
| `rl_s8_R` | **vite** : deux effets à la fois (palier et τ) donnés avec leurs calculs. | Question d'observation : l'élève regarde d'abord ce qui a changé, les calculs viennent après. |
| `rl_t1_rupture` | le montage, la courbe et l'équation dans la même voix. | Signalé, non modifié (voix enregistrée ; `rl_t2_descente` reprend la courbe). |
| `rl_n1_2022R`, `rl_n2_2024N` | sujets entiers en une voix (818 et 1 095 caractères). | Signalés : à découper question par question si on les revoice. |

### Résultats décisifs trouvés par l'élève

- **`rl_b2_lampes`** — après « و la lampe ديال la bobine؟ » : « Et la lampe L₂, celle de la bobine : que fait-elle ? » (en même temps que L₁ / **en retard, peu à peu** / reste éteinte). Geste : `highlight lampe_L`. `lampes.html` tait « L₂ s'allume en retard… ».
- **`rl_s8_R`** — après « شوف la courbe الجديدة: » : « Qu'est-ce qui a changé sur la nouvelle courbe ? » (même palier, plus lente / **palier plus bas, atteint plus vite** / palier plus haut). Geste : `highlight courbe_R`. `influence.html` tait les lignes I₀’ et τ’ calculées.

### Prérequis enseignés

Loi d'Ohm (deux mesures ; la droite plus raide), additivité avec la bobine (trois flèches ; l'escalier), dérivée (la tangente ; le compteur de vitesse, puis di/dt), exponentielle (les deux courbes ; le réservoir). Le courant et la tension sont enseignés de zéro dans le cours RC, qui précède (rappels `rc_rp1`, `rc_rp2`) ; ils reviennent ici dans la loi d'Ohm.

### Autres changements

- La question de bloc de l'ancien `rl_s1_b2` (bascule à courant constant) garde sa place dans la réserve de `rl_b5_continuite` ; l'exercice des deux lampes devient celui du bloc des lampes.
- **Défaut déjà en ligne corrigé** dans la copie en attente : la voix de `rl_e7_2021R` s'arrête avant « tau égale L sur R deux plus r », mais le pointage et la formule du centre citaient encore ces mots (jamais atteints). Ils sont retirés ; la voix et sa piste ne changent pas.

## 3. Circuit RLC (`phys_ch8_circuit_RLC`)

### Ce qui allait trop vite

| diapo | constat | ce qui a été fait |
|---|---|---|
| `lc_o2_prerequis` | **vite** : i = dq/dt = C·du_C/dt, u_b = L·di/dt + r·i, dérivée d'un cosinus et la « recette » en une diapo. | Retirée. `lc_rp1_condensateur` (la pente de q(t) avec `intensite.html` ; le verre sous le robinet), `lc_rp2_bobine` (le courant en triangle avec `triangle.html` ; la charrette lourde), puis `lc_rp3_cosinus` avant `lc_e6_sinusoide` et `lc_rp4_dcos` avant `lc_e7_deriver`. |
| `lc_r2_aperiodique` | **vite** : deux expériences dans la même voix (R = 1 kΩ, puis 300 Ω et le régime critique). | Coupée en deux : `lc_r2_aperiodique` (1 kΩ seulement, voix réécrite et relue) et **`lc_r2b_critique`** (300 Ω sur son propre écran, `oscillogramme.html?vue=critique`). |
| `lc_d2_bobine` | **donné** : la voix posait la question (« quand elle arrive à zéro, est-ce qu'elle s'arrête ? ») et répondait aussitôt ; le QCM d'après demandait la même chose, au futur (une prédiction). | Question d'observation à cet endroit ; l'ancien QCM passe en réserve. La question du bloc va sur `lc_d3_courant` (« quand u_C = 0, i est… ? »), qui l'enseigne. |
| `lc_r3_ordre` | trois écrans à la fois. | Gardée : synthèse, chaque régime a eu son expérience avant ; la voix montre un écran après l'autre. |
| `lc_en3_echange`, `lc_c1_depart`, `lc_n1_2020N`, `lc_n2_2025N` | voix longues (échange + I_m + retour + remarque ; conditions initiales ; sujets entiers). | Signalés, non modifiés dans ce passage. |

### Résultats décisifs trouvés par l'élève

- **`lc_d2_bobine`** — après « واش غادي توقف؟ » : « u_C est arrivée à zéro. Qu'a-t-elle fait ensuite ? » (arrêtée à zéro / **passée sous zéro** / remontée tout de suite). Geste : `play_until recharge_inverse` (le même que le pointage suivant : fait une seule fois). `circuit-lc.html` tait les lignes « « − » sur A, « + » sur B : u_C < 0… » et le motif.
- **`lc_r2_aperiodique`** — après « شوف u C كترسم: » : « Avec R = 1 kΩ, que fait u_C ? » (oscille / **descend vers zéro sans passer en dessous** / reste à 6 V). Geste : `play_until retour_sans_oscillation`. `oscillogramme.html` tait « revient vers 0 sans changer de signe », « aucune oscillation » et le nom du régime.

### Prérequis enseignés

q = C·u_C et i = dq/dt (pente de q(t) ; le verre sous le robinet), u_b de la bobine (le triangle ; la charrette), le cosinus et la sinusoïde (le point qui tourne ; la balançoire), la dérivée d'un cosinus (la pente à chaque instant ; la même sinusoïde décalée d'un quart de période). La dérivée d'un carré (`lc_a2_derivee`) est rappelée sur sa diapo, comme avant.

## 4. Transformations lentes et rapides (`phys_ch9_transformations_lentes_rapides`)

### Ce qui allait trop vite

| diapo | constat | ce qui a été fait |
|---|---|---|
| `tl_o2_bases` | **vite** + **prérequis** : l'ion, la conservation des éléments et des charges, et cinq couleurs en une diapo. | Retirée. `tl_rp1_ion` (l'atome neutre, Cu²⁺, I⁻ ; les jetons + et −) et `tl_rp2_conservation` (compter atomes et charges ; la balance). Les couleurs sont dites dans chaque expérience (bleu de Cu²⁺ dans `tl_x1_zinc`, violet de MnO₄⁻ dans `tl_r1_bechers`, brun de I₂ dans `tl_r3_lente`). |
| `tl_x3_couple` | **vite** : la balance, réduction, oxydation, couple, demi-équation, trois exemples, la conclusion sur le zinc et deux définitions (909 caractères). | Coupée : `tl_x3_couple` réécrite (réduction et oxydation seulement, dites deux fois : la balance, puis « celui qui donne le ballon l'a perdu ») et **`tl_x3b_couple`** (le couple, sa demi-équation, les exemples, le zinc oxydé), avec la question du bloc. |
| `tl_x6_eau` | deux couples d'un coup (H₂O₂/H₂O puis I₂/I⁻). | Coupée : `tl_x6_eau` (eau oxygénée seule) et **`tl_x6b_diiode`** (diiode, `demi-equation.html?vue=iode`). |
| `tl_f1_facteur` | la définition et trois comparaisons de tableau d'un coup, refaites ensuite par `tl_f8_variable`. | Réécrite : la définition relue, puis dite une deuxième fois (« le feu quand on cuisine »), et une seule comparaison (1 → 2) ; les autres restent à `tl_f8_variable`, une par une. |
| `tl_r1_bechers` | deux béchers en parallèle : la comparaison est voulue, mais le résultat était dit, puis demandé après coup. | Question d'observation ; l'ancien QCM passe en réserve ; la question du bloc va sur `tl_r4_indices`. |
| `tl_r8_duree`, `tl_x9_oxalique` | tableau de trois expériences d'un coup ; équation longue. | Signalés : `tl_f1_facteur` et `tl_f8_variable` reprennent le tableau une comparaison à la fois. |

### Résultats décisifs trouvés par l'élève

- **`tl_r1_bechers`** — après « دابا نصبو فبجوج فنفس الوقت. » : « Dans quel bécher le violet disparaît-il tout de suite ? » (à droite / **à gauche, avec les ions fer II** / les deux). Geste : `play_until rapide_fini`. `bechers.html` tait « décoloré aussitôt », « réaction rapide » et le motif.
- **`tl_t3_catalyseur`** — après « شوف: » : « Lequel des deux brunit le plus vite ? » (sans ions fer II / **avec les ions fer II** / les deux). Geste : `play_until catalyse_avance`. `facteurs.html` tait les lignes « avec Fe²⁺, le diiode apparaît beaucoup plus vite », « teinte finale vers 10 min », « le catalyseur accélère ».

### Prérequis enseignés

L'atome, l'électron, l'ion ; la conservation des éléments et des charges ; la quantité de matière et la mole (`tl_rp3_mole` : la douzaine d'œufs, puis la mole ; la millimole) et la concentration (`tl_rp4_concentration` : trois béchers ; le sirop), ces deux derniers dans un bloc à eux, juste avant la partie « rapide ou lente » qui parle de mol/L et de mmol.

### Reste à faire (non traité ici)

- `tl_f7_palier` utilise le **réactif limitant** (notion de 1ère année, tableau d'avancement) sans l'enseigner ; `tl_r2_rapide` et `tl_r6_classer` citent la **précipitation** ; `tl_r7_titrage` l'**équivalence** d'un titrage. À enseigner de zéro au prochain passage (le cours de cinétique qui suit en a besoin aussi).
- **Défaut déjà en ligne corrigé** dans la copie en attente : la voix de `tl_n1_lecture` s'arrête avant « السؤال اللخر », mais le pointage et le centre le citaient. Retirés ; la piste reste juste.

## Simulations

### Nouvelles

- **`frontend/public/media/simulations/physics/dipole-rc-tableau/rappels.html`** — servie aussi aux cours RL et RLC. Neuf vues, cadre 760 × 420, un bouton, au plus un curseur, moteur et appareils peints repris de `condensateur.html` (mêmes commandes : `start`, `pause`, `resume`, `reset`, `set_time`, `set_parameters`, `play_until`, `highlight`), `ce_qui_se_voit`, un `repere` par élément dit :

| vue | moments | curseur | peint (règle 32) |
|---|---|---|---|
| `courant` | circuit · ferme · sens · amperemetre · eau | — | pile, interrupteur, lampe qui s'allume, ampèremètre, électrons, eau qui coule |
| `tension` | circuit · fleche · voltmetre · niveaux · fil | — | lampe, voltmètre, deux réservoirs d'eau |
| `ohm` | montage · mesure_1 · mesure_2 · droite · convention | R (50 → 200 Ω) | résistor à bandes, ampèremètre, voltmètre |
| `additivite` (+ `&dipole=bobine`) | circuit · tensions · somme · escalier | u_C ou u_b (0 → 6 V) | générateur, résistor, condensateur ou bobine, escalier en bois |
| `puissances` | milli · micro · nano · exemple · decoupe | — | (craie : la virgule qui recule) |
| `derivee` | courbe · corde · tangente · pente_nulle · voiture | t (0 → 10 s) | voiture, route, compteur de vitesse |
| `exponentielle` | depart · tau · jamais_zero · montee · reservoir | t/τ (0 → 5) | réservoir d'eau qui se vide |
| `sinusoide` | cercle · courbe · amplitude · periode · balancoire | — | point qui tourne, balançoire |
| `derivee_cos` | courbe · sommet · descente · derivee · decalage | t (0 → 8 ms) | (craie : tangentes et courbe de la pente) |

- **`frontend/public/media/simulations/chimie/transformations-lentes-rapides-tableau/rappels.html`** — quatre vues : `ion` (atome · perd · gagne · jetons ; atomes peints, électrons, jetons), `conservation` (equation · atomes · charges · balance ; balance en laiton), `mole` (douzaine · mole · milli · exemple ; boîte d'œufs), `concentration` (becher · double_n · formule · dilution · sirop ; béchers dont la teinte suit C, verres de sirop ; curseur V).

### Enrichies (additif : sans le paramètre, rien ne change)

Paramètre **`conclusions`** (`set_parameters {conclusions: false|true}` ou `?conclusions=0`), qui tait les phrases d'une étape et le motif de son arrêt sur image, sans relancer la scène :

| simulation | ce qui est tu |
|---|---|
| `physics/dipole-rc-tableau/condensateur.html` | étape `k_ferme` : « l'aiguille de l'ampèremètre saute puis redescend » |
| `physics/dipole-rc-tableau/tau-rc.html` | « τ × 2 : charge plus lente » et la fin du motif du préréglage |
| `physics/dipole-rl-tableau/lampes.html` | étape `retard` : « L₂ s'allume en retard » |
| `physics/dipole-rl-tableau/influence.html` | vue R : les lignes I₀’ et τ’ calculées |
| `physics/circuit-rlc-tableau/circuit-lc.html` | étape `recharge_inverse` : lignes et cote « ≈ −4,9 V » |
| `physics/circuit-rlc-tableau/oscillogramme.html` | vue aperiodique : « revient vers 0 sans changer de signe », « aucune oscillation », nom du régime |
| `chimie/transformations-lentes-rapides-tableau/bechers.html` | étapes `rapide_fini`, `lente_continue` et l'étiquette « réaction rapide » |
| `chimie/transformations-lentes-rapides-tableau/facteurs.html` | étapes `catalyse_avance`, `catalyse_fini` (et « • le catalyseur accélère ») |

## Voix à enregistrer (voix Bodi, plus tard)

Énoncés et réactions sont écrits et dits par la voix en direct en attendant leurs pistes. Les réactions des questions nouvelles sont préparées (`concentration.reponses.q` : `juste` pour la bonne carte, `1` et `2` pour chaque mauvaise, avec `parole` et `ecrit`, sans `audio`).

### Dipôle RC (`phys_ch6_dipole_RC`)

**Pistes de diapo — 9 :** `rc_rp1_courant`, `rc_rp2_tension`, `rc_rp3_ohm`, `rc_rp4_additivite`, `rc_rp5_puissances`, `rc_c2a_principe`, `rc_rp6_derivee`, `rc_rp7_exponentielle`, `rc_t3_C`.

- `rc_rp2_tension` — « À toi » : *Pour mesurer la tension aux bornes d'une lampe, comment branche-t-on le voltmètre ?* ; 5 réactions.
- `rc_rp4_additivite` — « À toi » : *Dans un circuit série, E = 6 V et u_C = 4,5 V. Que vaut u_R ?* ; 5 réactions + démonstration.
- `rc_c2a_principe` — « À toi » : *Dans ce montage, que mesure l'ampèremètre ?* ; 5 réactions.
- `rc_c2_aiguilles` — observation : *Après son saut, que fait l'aiguille de l'ampèremètre ?* ; `enonce_dit`, 2 indices, 3 retours, solution.
- `rc_rp6_derivee` — « À toi » : *À l'endroit où la courbe devient plate, la dérivée vaut :* ; 5 réactions.
- `rc_rp7_exponentielle` — « À toi » : *Que vaut e^(−t/τ) à t = 0 ?* ; 5 réactions.
- `rc_t2_influence` — observation : *R a doublé. Compare la nouvelle courbe à l'ancienne* ; `enonce_dit`, 2 indices, 3 retours, solution.
- `rc_t3_C` — « À toi » : *Si on double C (R ne change pas), τ :* ; 5 réactions + démonstration.
- Blocs nouveaux (`rc_s0_b1`, `rc_s0_b2`, `rc_s1_b2a`, `rc_s3_b0`, `rc_s3_b3a`) et blocs recomposés (`rc_s1_b2`, `rc_s3_b3`) : `retrouver.enonce_dit` et `exercice` avec réactions, gardés pour l'étape de fin de cours (non voixés aujourd'hui, comme les autres blocs).

### Dipôle RL (`phys_ch7_dipole_RL`)

**Pistes de diapo — 5 :** `rl_rp1_ohm`, `rl_rp2_additivite`, `rl_rp3_derivee`, `rl_b2a_principe`, `rl_rp4_exponentielle`.

- `rl_rp2_additivite` — « À toi » : *E = 6 V, u_R = 5 V. Que vaut u_b ?* ; 5 réactions + démonstration.
- `rl_b2a_principe` — « À toi » : *Qu'est-ce qui différencie les deux branches ?* ; 5 réactions.
- `rl_b2_lampes` — observation : *Et la lampe L₂, celle de la bobine : que fait-elle ?* ; `enonce_dit`, 2 indices, 3 retours, solution.
- `rl_s8_R` — observation : *Qu'est-ce qui a changé sur la nouvelle courbe ?* ; `enonce_dit`, 2 indices, 3 retours, solution.
- Blocs nouveaux `rl_s0_b1`, `rl_s0_b2` : `retrouver` et `exercice` (fin de cours).

### Circuit RLC (`phys_ch8_circuit_RLC`)

**Pistes de diapo — 6 :** `lc_rp1_condensateur`, `lc_rp2_bobine`, `lc_r2_aperiodique` (voix réécrite), `lc_r2b_critique`, `lc_rp3_cosinus`, `lc_rp4_dcos`.

- `lc_rp2_bobine` — « À toi » : *Bobine idéale, courant constant : que vaut u_b ?* ; 5 réactions + démonstration.
- `lc_d2_bobine` — observation : *u_C est arrivée à zéro. Qu'a-t-elle fait ensuite ?* ; `enonce_dit`, 2 indices, 3 retours, solution.
- `lc_d3_courant` — « À toi » (voix de la diapo inchangée) : *Quand u_C = 0, l'intensité i est :* ; 5 réactions.
- `lc_r2_aperiodique` — observation : *Avec R = 1 kΩ, que fait u_C ?* ; `enonce_dit`, 2 indices, 3 retours, solution.
- `lc_rp4_dcos` — « À toi » : *Au sommet de u_C(t), que vaut du_C/dt ?* ; 5 réactions.
- Blocs nouveaux `lc_s0_b1`, `lc_s2_b2a` et bloc recomposé `lc_s1_b1` (nouveau `retrouver`) : fin de cours.

### Transformations lentes et rapides (`phys_ch9_transformations_lentes_rapides`)

**Pistes de diapo — 9 :** `tl_rp1_ion`, `tl_rp2_conservation`, `tl_x3_couple` (réécrite), `tl_x3b_couple`, `tl_x6_eau` (raccourcie), `tl_x6b_diiode`, `tl_rp3_mole`, `tl_rp4_concentration`, `tl_f1_facteur` (réécrite).

- `tl_x3b_couple` — « À toi » : *Dans Zn + Cu²⁺ → Zn²⁺ + Cu, le zinc :* ; 5 réactions.
- `tl_rp4_concentration` — « À toi » : *n = 0,02 mol dans V = 0,5 L : que vaut C ?* ; 5 réactions + démonstration.
- `tl_r1_bechers` — observation : *Dans quel bécher le violet disparaît-il tout de suite ?* ; `enonce_dit`, 2 indices, 3 retours, solution.
- `tl_r4_indices` — « À toi » (voix inchangée) : *Comment voit-on que la transformation lente continue ?* ; 5 réactions.
- `tl_t3_catalyseur` — observation : *Lequel des deux brunit le plus vite ?* ; `enonce_dit`, 2 indices, 3 retours, solution.
- Blocs nouveaux `tl_s0_b1`, `tl_s1_b4` : fin de cours.

**Total : 29 pistes de diapo, 14 énoncés de questions « À toi » nouvelles (5 démonstrations), 8 questions d'observation (énoncé, indices, retours, solution) ; 118 textes de réaction, d'indice et de solution.**

## Vérifications faites

- `node --check` sur chaque `<script>` des deux pages nouvelles et des huit pages enrichies : sans erreur.
- Script de contrôle des copies en attente (JSON valide ; chaque `mot` du pointage et du centre dans sa voix ; chaque `apres_mot` trouvé une seule fois ; chaque `moment` cité existe dans la simulation, vue par vue pour les rappels ; chaque `repere` cité existe ; chaque diapo dans un seul bloc, dans l'ordre ; au plus une question « À toi » par bloc ; réactions juste / 1 / 2 complètes ; mots des démonstrations dans leur `parole` ; aucune piste gardée sur une voix changée ; pas de chiffre, symbole ni tachkil dans les textes dits nouveaux) : **OK pour les quatre cours**.
- `backend/scripts/verifier_figures_cahier.py` sur les quatre copies : 0 erreur, 0 avertissement.
- Navigateur sans écran (Playwright, serveur Vite sur http://localhost:5173) : les 13 vues des deux pages de rappels s'ouvrent sans erreur, ont de l'encre, aucun texte hors cadre (`__horsCadre` vide) ; captures relues (dérivée, sinusoïde, dérivée d'un cosinus, ion, concentration, additivité avec bobine). Pour les huit simulations enrichies : `conclusions: false` → `play_until` sur le moment de la question → arrêt sur image avec motif neutre et phrase tue ; `conclusions: true` → la phrase réapparaît **sans relancer** la scène (bouton resté « Reprendre ») ; aucune erreur de page.
- `voxtts/corpus_v4/controler_cadre.py` sur les quatre copies : « cadre : OK » pour RC, RL et RLC (comme en ligne ; les nouveaux points « à relire » sont des lectures de relations, u_R = R·i, i = dq/dt…, déjà au cadre). Transformations lentes et rapides : les 3 fautes sont celles du cours en ligne (« chocs efficaces », hors cadre, dans les réactions de `tl_n2_glacee` : réserve de fin de cours et question d'exercice) — **non corrigées ici**, à remplacer par « rencontres » avec leurs pistes.
- `voxtts/corpus_v4/verifier_texte_corpus.py` sur les textes dits nouveaux : les mots darija rares remplaçables l'ont été (الصبيب, مسطحة, بانتظام, متأخرة, الباكية, كنذوبو, غامق, الطنجرة…). Restent signalés et gardés exprès : les termes du programme en français (ampèremètre, voltmètre, dérivation, exponentielle, sinusoïde, iodure…) et quelques mots de la vie courante des deuxièmes explications (الدروج, الخزانات, الكروسة, المرجيحة, الميزان, السيرو, طافية, شاعلة), absents d'un corpus de leçons mais connus de tous ; à écouter après génération (`detecter_murmures.py`).

## Ce qui n'a pas pu être vérifié

- Les voix : aucune piste Bodi n'est générée (GPU Kaggle) ; la prononciation des mots signalés ci-dessus reste à écouter.
- Le jeu complet dans le lecteur de cours (`/dev/course-player`) : les copies en attente ne sont pas servies ; l'arrêt de la voix sur `apres_mot`, l'ordre gestes / pointage (dédoublonnage) et la reprise ont été lus dans `CourseFocusStage.tsx`, pas joués.
- `preparer_reponses.py verifier` n'a pas été lancé : il exige les pistes, absentes par construction.
