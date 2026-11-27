# phys_ch3_ondes_lumineuses — corrections de l'audit pédagogique (26-27/11/2026)

Cours servi : `backend/data/courses/phys_ch3_ondes_lumineuses.json` (phase 1, aucune voix changée).
Copie d'attente : `backend/data/courses/en_attente/phys_ch3_ondes_lumineuses.json` (phase 2, texte parlé ; remplace l'ancienne copie périmée).
Pistes à mettre en voix : `docs/audit-pedagogie/voix_a_generer/phys_ch3_ondes_lumineuses.json` — **152 pistes** (58 voix de diapo dont 3 nouvelles, 94 réactions préparées). Aucune voix générée.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| Version | Diapos | Questions dans les 6 premières | Formules dites non écrites | Passages ≥ 60 mots sans geste | Notions clés | redites | annoncées (phrases ≠ selon le script) | Premier mot le plus fréquent | Diapos qui suivent avec le même premier mot | Réactions au même début (≥ 4) |
|---|---|---|---|---|---|---|---|---|---|---|
| Avant (servi, 26/11) | 68 | 2 | 51 | 1 | 30 | 8 (27 %) | 0 (0) | « دابا » 16 % | 3 | 3 (34, 28, 5) |
| Servi après phase 1 | 68 | 1 (voix de la diapo 4 qui finit sur « ? ») | 37 | 0 | 34 | 9 | 0 (0) | « دابا » 16 % | 3 | 3 |
| Copie d'attente (phase 2) | 71 | **0** | 36 | **0** | 37 | **37 (100 %)** | **35 (95 %)** (15) | « تفكر » **8 %** | **0** | **0** |

- Les 36 « formules dites non écrites » qui restent : 16 dans les diapos d'énoncé du national (la feuille du sujet est à l'écran), le reste des phrases écrites juste avant par la simulation ou par une carte posée une phrase plus tôt (le script ne regarde que ~12 mots en arrière), et les relectures « نعاود نقرا ».
- **Annonces : 35 phrases d'annonce, toutes différentes** (aucune n'est répétée mot pour mot). Le script n'en compte que 15 « distinctes » parce qu'il compte le fragment reconnu (sa liste n'a que 16 crochets en darija sans chadda : ركز معايا، حل عينيك، تبع معايا، سمعني مزيان، هادي مهمة…) ; au-delà de 16 notions annoncées, ce nombre ne peut plus monter. « تبعني » a été retiré (inconnu de la voix, 0 fois dans le corpus) au profit de « تبع معايا ».

## Phase 1 — cours servi (commit 46d0834b, plus l'écran de la diapo 5 dans le commit de phase 2)

- Règle 53 : l'observation de la diapo 3 (`ol_d2_fente_fine`) et la question de la diapo 4 (`ol_d3_figure`) passées en réserve `exercices_fin_de_cours` avec leurs réactions et leurs voix (la même idée est demandée par l'exercice du bloc `ol_s1_b1`). La voix de la diapo 4 finit encore sur une question : corrigée dans la copie d'attente.
- Règle 54 : 17 cartes `centre` posées au mot qui dit la formule (`ol_l4_petit_angle`, `ol_l5_egalite`, `ol_c4_cheveu`, `ol_g3_pente`, `ol_g4_identifier`, `ol_g6_theta`, `ol_g5_autres`, `ol_r2_vide`, `ol_r2b_celerite`, `ol_r4_spectre`, `ol_n1_ralentit`, `ol_n6_cuve` — fin du passage de 62 mots sans geste).
- Gestes réparés : `ol_l8_ordre_grandeur` (mot « بين quatre cents و » disparu de la voix depuis la conversion des nombres : le geste partait à t = 0), `ol_x3_enonce_p2` (geste sur « Question trois point un », question non lue sur cette feuille), `ol_n5_lambda_n` (pointage dans le désordre). `verifier_pointage.py` : 3 → 0 défaut.
- Écran de la diapo 5 (`ol_d4_onde`) : retiré « l'onde diffractée garde la même longueur d'onde, la même fréquence et la même célérité » (défaut 4 : λ, ν, c pas encore enseignés).
- Questions de bloc : aucune à déplacer (voir « défauts laissés »).

## Phase 2 — copie d'attente

### Ordre des notions (règle 52) et cours du prof
- **Partie « Radiation, fréquence et spectre » avancée juste après la diffraction** (devient la partie II ; ancienne VI) : monochromatique/polychromatique, le vide et c, « Tout en mètre » (déplacée juste avant λ₀ = c/ν, pour que les nanomètres soient convertis avant le premier calcul), λ₀ = c/ν, le spectre visible. Elle arrive maintenant **avant** θ = λ/a, la couleur (rouge/bleu), le contrôle « est-ce visible ? » et la question « laser violet » : défauts 1, 6, 8 corrigés. Titres des parties, en-têtes du cahier (II → III…), blocs (`ol_s3_b3r`, `ol_s3_b3` passent en séance 1 ; `ol_s1_b3r` passe en séance 2) et titres des séances renumérotés ; le tableau des conversions suit sa diapo dans le cahier.
- **Diapo 34 coupée en deux** (défaut 9) : `ol_r1_monochromatique` (le laser ; le prisme décrit : deux faces non parallèles, l'arête, l'angle A ; « dans le vide, une radiation a une longueur d'onde λ₀ » ; la fréquence rappelée du chapitre 2) puis **nouvelle** `ol_r1b_polychromatique` (la lumière blanche dans le prisme, simulation existante `prisme-dispersion.html`).
- **Nouvelle diapo `ol_n0_refraction`** « Rappel : la réfraction » avant l'indice (défaut 3), simulation existante `prisme-dispersion.html?source=verte` (le rayon vert change de direction en entrant et en sortant) ; rappel redit en une phrase au début de `ol_p2_violet` et de `ol_n4_indice`.
- **Nouvelle diapo `ol_g1b_droite`** « Rappel : une droite qui passe par l'origine » (y = k·x, k = y/x, exemple du lait) avant « Pourquoi 1/a » (défaut 2). **Carte simple, sans figure** : aucune vue de simulation existante ne montre une droite sans les grandeurs du cours (la courbe `courbe.html` aurait aussi répété l'URL de la diapo voisine).
- Diapo 3 : la diffraction de l'eau (chapitre 2) rappelée **avant** la fente, sous forme de question à laquelle l'expérience répond (cours du prof, recommandation 3) ; diapo 5 : « la lumière est une onde électromagnétique », renvoyée à la partie II.
- Diapo 4 : la question finale de la voix devient une redite (fente horizontale → figure verticale).
- Diapo 19 (`ol_l6_isoler`) : le produit en croix rappelé sur un exemple chiffré (2/3 = 4/6), écrit à son mot (défaut 7, partie « produit en croix »).
- Diapo 25 : « تفكر le spectre: le violet عندو lambda صغيرة » avant la question du laser violet.
- `ol_p2_violet` : les indices du verre de la simulation dits et écrits (n(rouge) = 1,61 ; n(violet) = 1,66), recommandation 4 du prof.
- Ouverture : les deux questions du chapitre (la lumière va-t-elle tout droit ? d'où viennent les couleurs de l'arc-en-ciel ?) ; réponse dans la fermeture (les gouttes de pluie dispersent la lumière blanche), écrite à son mot.
- `ol_n5_lambda_n` et `ol_n1_ralentit` : λ₀ = c/ν et c rappelés à leur ancienne place (recommandation 1).

### Notions importantes (règle 55) et tuteur humain (règle 56)
- 35 annonces différentes (banque de phrases et phrases du même style), une deuxième façon de dire (« بطريقة أخرى / بمعنى آخر / يعني بالدارجة », image ou exemple) dans les 37 diapos clés, rappels « تفكر… / شفنا… / رجع معايا… » dans les diapos qui réutilisent une notion (radian en 17, tangente en 15, spectre en 21, 25, n5 ; réfraction en 43 et 48 ; diffraction en 51 ; c en 39 ; λ₀ = c/ν en 44).
- Débuts de voix variés : plus aucune diapo ne commence par « دابا » (16 % avant), « دابا غادي نقراو l'énoncé » (7 diapos) remplacé par sept débuts différents ; le premier mot le plus fréquent est sur 8 % des diapos ; aucune diapo ne suit une diapo de même premier mot.
- Touches humaines par bloc : « شفتي؟ الفتحة كتصغار… », « أنا عارف أن هاد الحساب كيبان صعيب… », « واخا تكون عيان شوية… », « فهمتي اللي فات؟ مزيان », « شوف هاد الحاجة، زوينة: الحساب عطانا بالضبط lambda… », « هنا كيغلطو بزاف ديال التلاميذ… ».
- Réactions : 102 réactions dont le début figé (« ما تقلقش، راه غلطة كيديروها بزاف… », « ماشي مشكل، حنا هنا باش نتعلمو », « برافو عليك، هادا هو الجواب », « الجواب هو… ») est remplacé par un début varié (12 ouvertures pour un premier essai faux, 12 pour la réponse donnée, 8 pour une bonne réponse) ; le reste de chaque réaction, qui nomme ce qui est juste dans le choix, est gardé. 94 sont des réactions de diapo (à revoicer) ; les autres sont des réactions de bloc (non mises en voix aujourd'hui, `FIN_DE_BLOC_COMPLETE = False`).

### Voix mal lues
- `ol_x2_enonce` (national 2023 R) : « pour prendre teta environ teta » → « pour prendre tangente teta environ égale à teta » ; « lambda zéro R égale L R lambda zéro j L j » → « lambda zéro R égale L R fois lambda zéro j، sur L j » ; « c égale trois virgule dix puissance huit mètre، par seconde » (lu « trois virgule… ») → « c égale trois fois dix puissance huit mètres par seconde ».

## Défauts laissés (et pourquoi)
- Défaut 10 (vrai-faux du bloc après la diapo 38 contenant « la vitesse dans le verre » et « la fréquence ne dépend pas du milieu ») : **faux dans le JSON actuel** — le vrai-faux n'a que deux phrases (limites du visible en nm, monochromatique caractérisée par sa fréquence), toutes deux enseignées avant.
- Défaut 11 / recommandation 5 du prof (énoncé 2021 N lu avant les diapos du prisme) : laissé à sa place. La question 1 du national est elle-même la diapo qui montre la lumière blanche dans le prisme ; la déplacer après « milieu dispersif » casserait les diapos 48-50 qui s'appuient sur ce spectre. L'énoncé ne contient plus de mot inconnu : le prisme est décrit, la lumière blanche et « polychromatique » sont enseignés dans la partie II (avancée).
- Défaut 5 (diapo 4 chargée) : la question finale est retirée (règle 53), la diapo n'est pas coupée (une seule simulation, la direction de la figure suit directement la tache centrale).
- Défaut 7, deuxième moitié (isoler L puis λ en deux étapes) : laissé, la diapo écrit déjà chaque forme à son mot.
- Blocs `ol_s5_b1c` et `ol_s5_b1g` : leur liste contient aussi la diapo de suite d'énoncé du bloc suivant ; sans effet pour le lecteur (le bloc se déclenche sur sa dernière diapo), laissé.
- `verifier_pointage_simulations.py` sur la copie d'attente affiche ~160 « gestes trop serrés » : artefact des diapos sans piste (`audio` retiré, durée inconnue, le script place les gestes à 1 s d'écart). À revoir une fois la voix générée. Sur le cours servi : 3 écarts déjà présents avant l'audit, aucun ajouté.

## Cours de référence du prof (`reference-prof/phys_ch3_ondes_lumineuses.md`)
Ajouté :
1. λ₀ = c/ν, le spectre visible (et monochromatique/polychromatique, le vide, c) avant les calculs de diffraction — partie avancée (rec. 1, 7).
2. Rappel de la réfraction avant l'indice, redit avant la diapo du violet (rec. 2).
3. Rappel de la diffraction de l'eau avant la fente ; ligne « même λ, ν, c » retirée ; « onde électromagnétique » dite en diapo 5 (rec. 3).
4. Indices du verre pour le rouge et le violet (valeurs de la simulation) dits et écrits ; description du prisme (faces, arête, angle A) à sa première apparition (rec. 4).
5. Ouverture sur l'arc-en-ciel, réponse dans la fermeture (rec. 6).
6. Diapo 34 coupée en deux, « dans le vide, une radiation a une longueur d'onde λ₀ » (rec. 7).

Laissé :
- Relations du prisme et loi de Descartes en calcul (rec. 8) : **hors cadre** — `perimetre.json` les liste dans « hors cadre officiel (retiré le 15/11/2026) » et `cadre_reference_2bac_pc.json` note « Relations du prisme (OL11) : hors cadre officiel » ; la dispersion reste interprétée qualitativement (diapo 50). Rien ajouté, pas même n₁ sin i₁ = n₂ sin i₂.
- Tableau d'indices « rempli en animation » à trois couleurs (rec. 4) : la simulation du prisme ne connaît que le rouge et le violet ; deux cartes écrites au mot, sans troisième valeur inventée.
- Énoncé 2021 N après les diapos 47-50 (rec. 5) : voir défaut 11 ci-dessus.
- L'expérience de la paille (rec. 2) : pas de figure existante ; le rayon vert dans le prisme montre le même changement de direction.

## Mots douteux pour la voix (`verifier_mots.py`, mots nouveaux vus moins de 3 fois dans le corpus)
centi, nano, faces, l'arête (termes à garder), السطور، جربنا، كتطيح، كيطيح، كتقرب، كيسبق، كيغلطو، للضو، للور (banque de phrases), et « violet » (vu 1 fois, terme du programme déjà présent partout dans le cours). « قوس قزح » n'est pas signalé. À faire écouter : les 35 phrases d'annonce et les ouvertures de réactions, nouvelles pour la voix.
