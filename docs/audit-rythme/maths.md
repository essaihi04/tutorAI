# Audit « rythme et départ de zéro » — mathématiques (14 novembre 2026)

Consignes : `docs/audit-rythme/BRIEF.md` ; règles 33 (une chose à la fois) et 34 (départ de zéro, deux explications) du skill `professeur`, avec 27, 28, 30 et 32.

En maths :
- « trop vite » : une diapo ou une voix qui enchaîne plusieurs étapes d'un raisonnement, plusieurs cas ou plusieurs propriétés d'un coup ;
- « résultat décisif donné » : la voix dit la conclusion que l'élève pouvait trouver (signe d'une dérivée, limite d'une suite, résultat d'une étape de calcul) ;
- « prérequis supposés » : des notions des années d'avant utilisées comme connues.

Les cours en ligne ne sont pas modifiés. Les nouvelles versions complètes sont dans `backend/data/courses/en_attente/<deck>.json`. Sur chaque diapo dont la voix change ou qui est nouvelle, `audio.mixed` est retiré.

## Constat commun aux six cours

1. **Les prérequis tenaient en une diapo de trois lignes.**
   - Le constat : la diapo « Trois gestes à avoir en main » (« Ce qu'on sait déjà » en primitives) donnait trois notions des années d'avant en une phrase chacune, sans image. D'autres prérequis n'étaient jamais rappelés : √(x²) = |x|, la forme canonique, le second degré, le cercle trigonométrique, les règles des inégalités…
   - Ce qui a été fait : dans chaque cours, cette diapo est remplacée par **cinq diapos de rappel** (`<préfixe>_z1…z5`), une notion chacune. Chaque rappel a sa petite animation à la craie (nouvelle page `rappels.html` dans le dossier du cours) et se déroule en trois temps : la définition avec l'animation, puis une deuxième explication différente (« دابا نشوفوها بطريقة أخرى » : image de tous les jours, contre-exemple ou autre vue), puis la relecture (« نعاود نقرا »).
2. **La voix calculait la réponse de la question qu'elle posait juste après.**
   - Le constat : c'est le défaut le plus fréquent en maths, de 6 à 10 diapos par cours.
   - Ce qui a été fait : la voix s'arrête avant le résultat et la simulation se fige avant la ligne du résultat. Quand la vue de calcul écrivait tout, une nouvelle page `etapes.html` la remplace. L'élève termine lui-même, et la démonstration de la question donne la fin.
3. **Plusieurs cas ou plusieurs règles dans une seule voix.**
   - Le constat : les quatre cas de qⁿ, les quarts du plan, les règles de ln, une étude complète ou un problème national tenaient chacun en une seule diapo.
   - Ce qui a été fait : ces diapos sont coupées, une idée par diapo (`<id>_b`, `<id>_c`), avec un arrêt sur image par étape.
4. **Questions d'observation (règle 30) : deux par cours.**
   - On ne les pose que là où la simulation montre elle-même le résultat décisif.
   - Pendant la question, la simulation cache sa conclusion grâce à un nouveau paramètre `conclusions`. Il vaut 1 par défaut, donc le cours en ligne n'est pas touché.
5. **Une seule question « À toi » par bloc.** C'est vérifié sur les six copies ; les blocs qui grossissaient ont été coupés.

## Récapitulatif

| Cours | Diapos | Blocs | Rappels de prérequis | Diapos ajoutées par découpage | Observations | Pistes de voix à enregistrer |
|---|---|---|---|---|---|---|
| 1 Limites et continuité | 68 → 80 | 21 → 25 | 5 | 8 | 2 | 54 |
| 2 Dérivation, étude de fonctions | 64 → 75 | 20 → 24 | 5 | 7 | 2 | 56 |
| 3 Suites numériques | 59 → 70 | 17 → 20 | 5 | 7 | 2 | 43 |
| 4 Primitives | 44 → 53 | 14 → 18 | 5 | 5 | 2 | 51 |
| 5 Fonctions logarithmes | 53 → 65 | 14 → 19 | 5 | 8 | 2 | 51 |
| 6 Nombres complexes | 48 → 58 | 12 → 19 | 5 | 6 | 2 | 49 |
| **Total** | 336 → 401 | 98 → 125 | 30 | 41 | 12 | **304** |

Les pistes de voix comptent :
- les diapos ;
- pour chaque observation : l'énoncé, les indices, les retours et la solution ;
- pour chaque nouvelle question : l'énoncé, la démonstration et les réactions.

Le détail est dans la section de chaque cours.

## Vérification (commune aux six cours)

- **`verif_maths.py --sims`** a été passé sur chaque copie. Il contrôle :
  - le JSON et les fins de ligne LF ;
  - les blocs : chaque diapo une fois, dans l'ordre, au plus une diapo « À toi » par bloc ;
  - les compétences ;
  - chaque `mot` du pointage, du centre et de `apres_mot`, qui doit être dans sa voix ;
  - les lignes des démonstrations ;
  - l'absence d'audio dont le hash est périmé ;
  - les réactions juste / 1 / 2 de chaque option ;
  - les retours et la solution de chaque observation ;
  - avec `--sims` : chaque simulation est ouverte sans écran (Chromium par Playwright, `frontend/public` servi en statique), les moments et repères cités doivent exister et aucune erreur JS ne doit apparaître.
- **Erreurs restantes** : seulement celles qui existent déjà dans les cours en ligne. Il s'agit de repères des pages de bilan, qui ne s'écrivent qu'au fil de la voix :
  - le repère `continuite_point` de `limites-continuite-tableau/bilan.html` ;
  - les repères `centre`, `branches` et `partie2` de `operations-formes-tableau/carte.html`.
- **`node --check`** passe sur toutes les pages créées ou modifiées (scripts en ligne extraits).
- **`verifier_texte_corpus.py`** a été passé sur chaque copie : les mots rares ajoutés sont remplacés, les termes du programme sont gardés exprès.
- **Non vérifié, pour les six cours :**
  - aucune voix n'a été générée ;
  - rien n'a été joué dans le lecteur réel (`CourseFocusStage`) : ni l'arrêt de la voix sur `apres_mot`, ni l'envoi de `sim_avant` / `sim_apres` ;
  - `controler_cadre.py` n'a pas été lancé, ni `preparer_reponses.py verifier`, qui demande les pistes.
- Vite (5173) doit être relancé pour servir les nouvelles pages (`rappels.html`, `etapes.html`, `derivation-tableau/produit.html`).

---

## Cours 1 — Limites et continuité (`math_ch1_limites_continuite`)

Copie en attente : `backend/data/courses/en_attente/math_ch1_limites_continuite.json` (68 → 80 diapos, 21 → 25 blocs), construite par `build_math_ch1_limites_continuite.py` (scratchpad de la session) à partir du cours en ligne, qui n'est pas modifié.
Simulations : nouvelles `limites-continuite-tableau/rappels.html` (vues `factoriser`, `signe`, `derivee`, `valeur_absolue`, `racine_facteur`, `sinus`) et `etapes.html` (vues `regles`, `l8_facteur`, `e1_enonce`) ; `miroir.html` enrichie (vue `parabole` : paramètre `conclusions`, défaut 1 = comportement d'avant ; à 0 la phrase « deux antécédents » garde sa durée mais reste invisible, les moments ne bougent pas).

Constat général : en maths le cours avançait déjà par arrêts sur image (une ligne de calcul = un `play_until`), et la plupart des diapos ne portent qu'une idée. Les trois défauts réels étaient : (1) les bases des années précédentes données en une diapo de trois lignes (« Trois gestes ») ou supposées en cours de route ; (2) **la voix calculait le résultat exact de la question qu'elle posait juste après** (7 diapos) ; (3) quelques diapos qui enchaînaient deux cas ou deux méthodes.

### Diapo par diapo

| Diapo | Constat | Ce qui a été fait |
|---|---|---|
| `lc_o2_bases` « Trois gestes » | Prérequis supposés : factorisation, signe de x − a, f′ > 0 ⇒ croissante, dits en une phrase chacun, sans image ; et d'autres prérequis jamais rappelés (√(x²) = \|x\|, facteur (x − a) d'un trinôme, utilisés en l5, l8, r9). | Supprimée, remplacée par 5 rappels enseignés depuis zéro, chacun animé, dit deux fois de deux façons, puis relu : `lc_z1_factoriser` (a² − b² vu avec des blocs de bois peints, puis vérifié avec des nombres), `lc_z2_signe` (x glisse vers 1 des deux côtés, puis la flèche de 1 vers x, puis le tableau de signe), `lc_z3_derivee` (la tangente glisse, sa pente f′ s'écrit ; puis la route qui monte et le tableau de variations), `lc_z4_valeur_absolue` (distance à 0, puis la machine « au carré puis racine » : √(x²) = \|x\|), `lc_z5_racine_facteur` (la parabole coupe l'axe en 1 et 3 → facteurs, puis on développe pour vérifier). Nouvelle séance 0 (2 blocs), une question « À toi » par bloc (z2 : signe de x − 3 pour x = 2,99 ; z5 : factoriser x² − 5x + 6). |
| `lc_l1_chemin` | Résultat donné : la voix dit « la limite égale deux » puis demande « f(x) s'approche de quel nombre ? » ; la simulation écrivait « lim f(x) = 2 » avant la question. | La voix s'arrête sur « regarde la valeur écrite » ; la simulation reste figée sur le trou (`trou_vide`), l'élève lit 0,99 → 1,99 et 1,01 → 2,01 et trouve 2. Deuxième façon ajoutée : la route avec un trou. Centre « lim f(x) = ? ». |
| `lc_l4_formes` | Trop vite : les 4 formes indéterminées + 4 règles qui n'en sont pas + la question, dans une voix ; et la voix disait « (+∞) × (−∞) = −∞ » juste avant de le demander. Notion « indéterminée » jamais expliquée. | Découpée. `lc_l4_formes` : les 4 formes, pourquoi « indéterminée », deuxième façon par un contre-exemple (x/x → 1 et x²/x → +∞ sont deux « ∞/∞ »). `lc_l4_formes_b` (nouvelle vue `etapes.html?vue=regles`, une règle par arrêt) : ce qui n'est pas indéterminé, enseigné avec (−∞) × (−∞) ; la question (+∞) × (−∞) et son exercice y passent (inchangés, leurs réactions gardent leur voix) : l'élève applique la règle des signes lui-même. |
| `lc_l5_facteur`, `lc_l6_conjugue` | Prérequis supposés : x² − 4x + 3 = (x − 3)(x − 1) et (a − b)(a + b). Rythme correct (un arrêt par ligne). | Rien changé à la voix : les prérequis sont désormais enseignés en z5 et z1 (même exemple x² − 4x + 3). |
| `lc_l7_plus_lourd` | Résultat donné : « 3x²/x² : trois », puis la question demande la même limite. | La voix s'arrête à la règle (garder le plus haut degré) ; plus d'arrêt sur `resultat`. Deuxième façon : x = 100, 3x² = 30 000, le 1 ne se voit plus. |
| `lc_l8_racine_infini` | Trop vite : deux cas (même poids → conjugué ; poids différents → facteur x avec √(x²) = \|x\|) en une voix ; prérequis √(x²) = \|x\| supposé. | Découpée : `lc_l8_racine_infini` (même poids, l'écart → 1/2, le conjugué) et `lc_l8_racine_infini_b` (nouvelle vue `etapes.html?vue=l8_facteur`, 6 lignes, 6 arrêts ; rappel de z4 au moment de sortir x). |
| `lc_l9_deux_cotes` | Résultat décisif donné : la branche de gauche plonge vers −∞, alors que la simulation le montre (−10, puis −100). | **Question d'observation** après « … zéro virgule quatre-vingt-dix-neuf. » : « Par la gauche de 1, que devient f(x) ? » (3 cartes, 2 indices, retours, solution). La phrase suivante de la voix (inchangée) confirme. Voix de la diapo inchangée : sa piste reste valable. |
| `lc_l11_interpreter` | Notion dite une seule fois : l'asymptote. | Deuxième façon ajoutée dans la voix : l'écart courbe-droite devient tout petit sans jamais s'annuler. |
| `lc_l12_sinus` | Prérequis supposé (« خاصك تحفظها ») : lim sin(x)/x = 1, donnée sans image, puis enchaînée avec le changement de variable. | Découpée. `lc_l12_sinus` : la limite de référence animée (nouvelle vue `rappels.html?vue=sinus` : M glisse vers 0, sin(x)/x vaut 0,84 puis 0,96 puis ≈ 1 ; deuxième façon : près de 0 la courbe de sin colle à y = x). `lc_l12_sinus_b` : le changement de variable t = 3x (ancienne vue, un arrêt par ligne). |
| `lc_l13_devoir` | Résultat donné : la voix calcule 1/2 puis demande de calculer la même limite. | La voix s'arrête au même dénominateur ; « termine : simplifie, puis remplace » ; la démonstration de la question donne la fin. |
| `lc_i4_composee` | Résultat donné (√4 = 2 dit avant la question identique). | La voix s'arrête à u → 4 et à la règle ; plus d'arrêt sur `racine_limite`. |
| `lc_j3`, `lc_t1`–`lc_t5` | Rythme correct (un arrêt par cas, questions sur d'autres valeurs). Le théorème est déjà dit deux fois (la rivière à traverser, puis la relecture). | Rien. |
| `lc_d4_recommencer` | Trop vite et résultat donné : étapes 2 et 3 de la dichotomie dans une voix, puis la question « combien d'étapes pour 0,125 ? » alors que la voix venait de les faire. | Découpée : `lc_d4_recommencer` (étape 2 seule, « l'amplitude est divisée par deux », puis la question et l'exercice f(3/8) : l'élève fait l'étape 3 lui-même) ; `lc_d4_recommencer_b` (étape 3, « deux étapes », on s'arrête). Bloc de la dichotomie coupé en deux. |
| `lc_r2_strictement_monotone` | Résultat décisif donné : « 4 a deux antécédents » se voit sur la simulation. | **Question d'observation** après « شوف la droite y égale quatre. » : « Combien de nombres x ont pour image 4 ? » ; `sim_avant {conclusions: 0}` cache la phrase écrite « deux antécédents » ; `sim_apres {conclusions: 1}`. Voix inchangée : piste valable. |
| `lc_r9_valeur_absolue` | Trop vite et prérequis supposé : f(y) = x, forme canonique (jamais expliquée), droit de prendre la racine, √(A²) = \|A\|, signe de y + 1, conclusion. | Découpée : `lc_r9_valeur_absolue` (la forme canonique expliquée : (y + 1)² = y² + 2y + 1 ; deuxième façon « on ajoute et on retire 1 ») et `lc_r9_valeur_absolue_b` (la racine, la valeur absolue, la conclusion). Même vue, arrêts répartis. |
| `lc_n6_equation` | Trop vite : les quatre cas de xⁿ = a dans une voix. | Découpée : `lc_n6_equation` (n pair, deux cas ; deuxième façon : 2⁴ = (−2)⁴ = 16) et `lc_n6_equation_b` (n impair, deux cas, le tableau). |
| `lc_n7_equation_racine` | Résultat donné : la voix résout (x = 2) puis demande de résoudre la même équation. | La voix nomme les quatre étapes, fait les deux premières, laisse la résolution et la vérification à l'élève. |
| `lc_lr4_infini` | Résultat donné (−∞) avant la même question ; un deuxième cas (en −∞, t = −x) enchaîné. | La voix s'arrête au facteur x ; « regarde chaque morceau » ; le cas −∞ retiré de la voix et de l'écran. |
| `lc_e1_probleme` | Trop vite : un problème national entier (5 questions) en une voix, puis la question 1 dont la voix venait de donner la réponse. | Découpée en trois : `lc_e1_probleme` (nouvelle vue `etapes.html?vue=e1_enonce` : l'énoncé et ses 5 questions, rappel « plus haut degré », la question 1 posée sans réponse), `lc_e1_probleme_b` (questions 1 à 3), `lc_e1_probleme_c` (questions 4 et 5). Bilan et carte dans un bloc à part. |
| Bilan, carte (`lc_e2`, `lc_e3`) | — | Rien. |

Structure : séance 0 nouvelle (2 blocs de rappels) ; séances 5 et 7 ont maintenant 4 blocs (dichotomie coupée en deux, bilan séparé du problème). Une seule diapo « À toi » par bloc partout ; compétences mises à jour (rappels dans K1).

### Voix à enregistrer (voix Bodi)

- **27 diapos** (`audio.mixed` retiré) : `lc_z1_factoriser`, `lc_z2_signe`, `lc_z3_derivee`, `lc_z4_valeur_absolue`, `lc_z5_racine_facteur`, `lc_l1_chemin`, `lc_l4_formes`, `lc_l4_formes_b`, `lc_l7_plus_lourd`, `lc_l8_racine_infini`, `lc_l8_racine_infini_b`, `lc_l11_interpreter`, `lc_l12_sinus`, `lc_l12_sinus_b`, `lc_l13_devoir`, `lc_i4_composee`, `lc_d4_recommencer`, `lc_d4_recommencer_b`, `lc_r9_valeur_absolue`, `lc_r9_valeur_absolue_b`, `lc_n6_equation`, `lc_n6_equation_b`, `lc_n7_equation_racine`, `lc_lr4_infini`, `lc_e1_probleme`, `lc_e1_probleme_b`, `lc_e1_probleme_c`.
- **2 nouvelles questions** : `lc_z2_signe/q` « x est un peu plus petit que 3 (x = 2,99). Alors x − 3 est : » ; `lc_z5_racine_facteur/q` « x² − 5x + 6 s'annule pour x = 2 et x = 3. Sa factorisation : » — 2 énoncés (`enonce_dit`), 10 réactions (`concentration.reponses.q` : 1 juste + 2 × (1, 2) chacune), 1 démonstration (z5).
- **2 questions d'observation** : `lc_l9_deux_cotes` (« Par la gauche de 1, que devient f(x) ? ») et `lc_r2_strictement_monotone` (« Combien de nombres x ont pour image 4 par x ↦ x² ? ») — chacune 1 énoncé, 2 indices, 3 retours, 1 solution, soit 14 pistes.
- Questions déplacées sans changement (`lc_l4_formes` → `lc_l4_formes_b`, avec leurs réactions) : pistes existantes gardées.
- **Total : 54 pistes** (27 diapos + 2 énoncés + 10 réactions + 1 démonstration + 14 pour les observations).

### Non vérifié

- Pas d'écoute ni de génération de voix (pas de GPU) ; `verifier_texte_corpus.py` passé : les mots rares restants sont des termes du programme (côté, pente, second degré, indéterminées, pair/impair, dichotomie) ou des mots déjà présents dans la voix en ligne.
- Le cours n'a pas été joué dans le lecteur (`CourseFocusStage`) : vérifiés seulement par script (mots du pointage, moments et repères ouverts dans un navigateur sans écran, JSON, blocs). L'arrêt de la voix des observations (`apres_mot`) et le masquage `conclusions` de `miroir.html` n'ont pas été vus dans le lecteur.
- Le rendu visuel des nouvelles vues a été regardé en capture fixe (construction complète) seulement, pas en mouvement ; `rappels.html?vue=factoriser` peint les blocs en dessin direct (ils apparaissent d'un coup, pas à la craie).
- `cadre : OK` (`controler_cadre.py`) non lancé ; `preparer_reponses.py verifier` non lancé (il exigerait les pistes).
- Erreur préexistante (cours en ligne aussi) : le repère `continuite_point` de `bilan.html` n'est pas trouvé hors lecteur.

---

## Cours 2 — Dérivation et étude des fonctions (`math_ch2_derivation_etude_fonctions`)

Copie en attente : `backend/data/courses/en_attente/math_ch2_derivation_etude_fonctions.json` (75 diapos au lieu de 64, 24 blocs au lieu de 20). Script reproductible : `build_math_ch2_derivation_etude_fonctions.py` (scratchpad de la session).

### Diapo par diapo (seulement celles qui posaient problème)

| Diapo | Constat | Ce qui a été fait |
|---|---|---|
| `df_c2_bases` « Trois gestes à avoir en main » | **Prérequis supposés, et trop vite** : trois notions de 1re bac (dériver un polynôme, signe d'un produit, 1/x en 0⁺) dites en une phrase chacune, sans animation, comme déjà sues. Le cours utilise aussi, sans les enseigner, la pente d'une droite (sécante, tangente, triangle de pente) et l'équation y = ax + b (tangente, asymptote oblique, vérifier un point). | Diapo supprimée, remplacée par **5 rappels enseignés de zéro**, une notion chacun, chacun expliqué deux fois de deux manières, avec animation (`rappels.html`) : `df_z1_pente` (on avance de 2, on monte de 4 ; puis l'escalier « 1 à droite, 2 en haut »), `df_z2_equation_droite` (a et b lus sur la droite ; puis l'équation comme test d'un point : (2 ; 3) oui, (1 ; 3) non), `df_z3_deriver_polynome` (l'exposant descend ; puis la dérivée vue comme la pente de y = 4 et de y = −5x), `df_z4_signe_produit` (tableau facteur par facteur ; puis trois nombres essayés), `df_z5_un_sur_x` (la courbe et les valeurs 10, 100 ; puis une barre de bois de longueur 1 coupée en 10 puis 100 morceaux, peinte). Deux blocs de rappel (nouvelle séance 0), une question « À toi » chacun : pente de y = −3x + 2 (`df_z2`), 1/0,001 (`df_z5`). |
| `df_nd3_nombre_derive` | **Notion expliquée une seule fois** : le nombre dérivé (la définition la plus importante du chapitre) dit une fois. | Deuxième manière ajoutée : le taux est une vitesse moyenne ; en rapprochant les deux instants, on obtient la vitesse à un instant, comme le nombre dérivé est la pente en un seul point. |
| `df_nd4_calcul` | **Trop vite** : deux exemples complets (polynôme factorisé, racine et conjugué) dans une seule voix, puis la question. | Découpé : `df_nd4_calcul` (polynôme seul, relié à la pente vue sur la parabole) et `df_nd4_calcul_b` (racine et conjugué), même construction figée exemple par exemple. La question et l'exercice passent sur `df_nd4_calcul_b` (inchangés, leurs pistes restent valables). |
| `df_dt5_sens` | **Trop vite** : quatre cas de demi-tangente verticale dans une seule voix, et le cas « à gauche » (où le sens s'inverse) passe en une demi-phrase. | Découpé : `df_dt5_sens` (les deux cas à droite) et `df_dt5_sens_b` (les deux cas à gauche, avec la raison : x − x₀ négatif, donc le haut du taux aussi). Un arrêt sur image par cas. |
| `df_dv1_tableau` | **Trop vite** : cinq dérivées et deux règles en une voix (« le tableau »). | Les polynômes sont enseignés dans `df_z3` ; la diapo ne garde que (1/x)′ et (√x)′, chacune expliquée par la pente (1/x descend : un moins ; √x monte de moins en moins vite). |
| `df_dv2_produit_quotient` | **Trop vite** : deux formules (produit, quotient) et un exemple dans une voix ; le produit n'a pas d'explication (« pourquoi deux termes ? »). | Découpé : `df_dv2_produit_quotient` = le produit seul, avec une **nouvelle animation** (`produit.html` : un rectangle de bois u × v qui grandit, bande u′v à droite, bande uv′ en haut), l'exemple x²(x + 1), et la vérification en développant (deuxième manière) ; `df_dv2_produit_quotient_b` = le quotient avec l'exemple existant. |
| `df_va2_sommet` | **Trop vite et résultat décisif donné** : sommet, creux, règle de l'extremum et contre-exemple en une voix ; « au sommet la tangente est horizontale, f′(−1) = 0 » est dit alors que l'élève peut le voir lui-même sur la construction. | Découpé : `df_va2_sommet` (le sommet seul, **question d'observation** : « Au sommet, comment est la tangente ? », la construction tait f′(−1) = 0 pendant la question) puis une deuxième manière (en haut d'une route qui monte puis descend, la route est plate) ; `df_va2_sommet_b` (le creux, la règle relue, « + 0 + »). |
| `df_bi6_arbre` | **Trop vite** : l'arbre entier (sept feuilles, deux étages de limites) dit d'un souffle. | Découpé : `df_bi6_arbre` (asymptote verticale, horizontale, puis f(x)/x : directions (Oy), (Ox)) et `df_bi6_arbre_b` (f(x)/x → a ≠ 0, puis f(x) − ax : asymptote oblique ou direction y = ax). Un arrêt par feuille. |
| `df_rec2_pente` | **Résultat décisif donné** : la pente reflétée 1/4 est dite, alors que le triangle vert la montre. | **Question d'observation** : « Quelle est la pente de la tangente en A′ ? » (la construction tait « 1/4 » pendant la question) ; deuxième manière ajoutée (une tangente très raide devient presque horizontale). |
| `df_ec3_etude` | **Trop vite et résultat donné** : « une étude complète » (domaine, demi-tangente, dérivée, minimum, point O, branche) en une voix, puis la question demandait le domaine que la voix venait de dire (et que le titre de la construction affichait). | Découpé en trois : `df_ec3_etude` (domaine expliqué + bord −1), `df_ec3_etude_b` (f′ et le signe de 3x + 2, **sans conclure**), `df_ec3_etude_c` (minimum confirmé, O, branche, tracé). La question « À toi » est sur `df_ec3_etude_b` : l'élève trouve lui-même le minimum en −2/3 ; la construction (`trace.html?vue=etude&conclusions=0`) tait le signe de f′, le minimum et la courbe sur ces deux diapos. L'ancienne question (domaine) et l'ancien exercice (minimum) passent en réserve (`exercices_fin_de_cours`, réactions gardées). |
| `df_ec1_ordre`, `df_ec2_forme` | Pointage en ligne visant des mots absents de la voix (déjà faux en ligne). | Corrigé sans toucher à la voix (repère final sur « رقم سبعة: », repère orphelin retiré). |

Non modifiées, jugées au bon rythme : les diapos de la tangente (`tg1–tg3`, une étape par arrêt), des demi-tangentes à droite / à gauche (`dt1–dt3`), de la concavité (`co1–co4`, deux images déjà données : le bol, la voiture), des asymptotes (`bi1–bi5`), de la position relative, de la symétrie, du tracé et de la réciproque (hors `rec2`). `df_va1_monte` donne le signe de f′ en le montrant, mais une seule observation par bloc suffit (celle du sommet, juste après).

### Blocs et compétences

- Nouvelle séance 0 « Les rappels de 1re bac, de zéro » : `df_s0_b1` (carte, pente, équation de droite) et `df_s0_b2` (polynôme, signe, 1/x), avec cahier, figure (pente de y = 2x − 1 ; 1/x près de 0), retrouver et exercice.
- `df_s1_b1` = nd1–nd3 ; `df_s1_b2` = nd4 + nd4_b ; `df_s2_b2` et `df_s2_b3` passent à 4 diapos ; `df_s3_b2` coupé en `df_s3_b2` (va1, va2, va2_b) et `df_s3_b2b` (va3, va4) ; `df_s4_b3` à 4 diapos ; `df_s7` : `b1` (ec1, ec2, ec3, ec3_b), `b2` (ec3_c, ec4), `b3` (bilan, carte).
- Une seule diapo « À toi » par bloc (vérifié). La séance 3 a désormais 4 blocs.
- Compétences : rappels pente, équation, 1/x → K1 ; polynôme → K3 ; signe → K4 ; les diapos découpées suivent leur diapo d'origine.

### Simulations

- Créées : `derivation-tableau/rappels.html` (vues `pente`, `equation`, `derivee`, `signe`, `inverse`) et `derivation-tableau/produit.html` (vue `rectangle`).
- Enrichies sans changer le défaut (paramètre `conclusions`, défaut 1) : `variations.html?vue=glisse` (tait « 0 » et « f′(−1) = 0 » au sommet et au creux, et la lecture en direct), `miroir.html?vue=pentes` (tait la pente en A′ et la formule), `trace.html?vue=etude` (tait le signe de f′, le minimum, la courbe et la branche).

### Voix à enregistrer (voix Bodi)

**Pistes de diapos (21)** : `df_z1_pente`, `df_z2_equation_droite`, `df_z3_deriver_polynome`, `df_z4_signe_produit`, `df_z5_un_sur_x`, `df_nd3_nombre_derive`, `df_nd4_calcul`, `df_nd4_calcul_b`, `df_dt5_sens`, `df_dt5_sens_b`, `df_dv1_tableau`, `df_dv2_produit_quotient`, `df_dv2_produit_quotient_b`, `df_va2_sommet`, `df_va2_sommet_b`, `df_bi6_arbre`, `df_bi6_arbre_b`, `df_rec2_pente`, `df_ec3_etude`, `df_ec3_etude_b`, `df_ec3_etude_c`.

**Nouvelles questions (3)** — énoncé (`enonce_dit`), démonstration (`demonstration.parole`) et réactions (juste + 1 + 2 pour chaque mauvaise option) :
- `df_z2_equation_droite` / q : « Quelle est la pente de la droite y = −3x + 2 ? » — 1 énoncé, 1 démonstration, 5 réactions.
- `df_z5_un_sur_x` / q : « Combien vaut 1/0,001 ? » — 1 énoncé, 1 démonstration, 5 réactions.
- `df_ec3_etude_b` / q : « Le signe de f′(x) est celui de 3x + 2 : que se passe-t-il en −2/3 ? » — 1 énoncé, 1 démonstration, 5 réactions.

**Questions d'observation (2)** — énoncé, 2 indices, 3 retours, 1 solution chacune :
- `df_va2_sommet` : « Au sommet, comment est la tangente ? » (cartes : vers le haut / horizontale / vers le bas).
- `df_rec2_pente` : « Quelle est la pente de la tangente en A′ ? » (cartes : 4 / 1/4 / −4).

**Énoncés des nouveaux exercices de bloc** (non joués aujourd'hui, `enonce_dit` écrit) : `df_s0_b1`, `df_s1_b1`, `df_s3_b2`, `df_s7_b3` (exercice) et `df_s0_b1`, `df_s0_b2`, `df_s1_b2`, `df_s3_b2b`, `df_s7_b3` (retrouver).

Total à voixer pour ce cours : 21 pistes de diapos + 3 énoncés + 3 démonstrations + 15 réactions + 2 × (1 énoncé + 2 indices + 3 retours + 1 solution) = **56 pistes** (hors exercices de bloc non joués).

### Non vérifié

- La voix : rien n'est enregistré (pas de GPU) ; les mots ont été passés à `verifier_texte_corpus.py` (restent des termes du programme rares dans le corpus : la pente, l'extremum, s'annule, d'équation, l'horizontale… déjà présents dans le cours en ligne).
- Le passage dans le lecteur (`CourseFocusStage`) : questions d'observation, arrêts sur image sur leurs mots, `sim_avant`/`sim_apres` sur `conclusions` — vérifiés seulement dans les simulations ouvertes sans écran (Playwright : moments, repères, aucune erreur JS, paramètre `conclusions` qui tait bien les valeurs).
- `controler_cadre.py` et `preparer_reponses.py verifier` non lancés (le second exige les pistes audio).
- La police de craie ne s'affiche pas sans écran (le « ′ » de f′ apparaît vide sur les captures, comme dans les simulations existantes).

---

## Cours 3 — Suites numériques (`math_ch3_suites_numeriques`)

Copie en attente : `backend/data/courses/en_attente/math_ch3_suites_numeriques.json` (59 → 70 diapos, 17 → 20 blocs, 6 → 7 séances). Script reproductible : `build_math_ch3_suites_numeriques.py` (bloc-notes de la session). Simulations : nouvelle `suites-tableau/rappels.html` (5 vues) ; `qn.html` (vue `negatif`) et `escalier.html` (vue `national`) enrichies d'un paramètre `conclusions` (défaut 1 = comportement inchangé).

### Audit diapo par diapo (seules les diapos avec un constat)

| Diapo | Constat | Ce qui a été fait |
|---|---|---|
| `su_o2_bases` « Trois gestes de 1re bac » | **Prérequis supposés, trop vite** : trois notions (terme géométrique, signe d'un quotient, même dénominateur) dites en une voix, chacune une fois, sans animation. Les règles des inégalités (sens gardé / inversé), que toute la récurrence utilise (r3, r6, m4), ne sont jamais enseignées ; les puissances (q⁰ = 1) non plus. | Remplacée par **cinq rappels**, un prérequis chacun, animés (`rappels.html`), expliqués deux fois (« دابا نشوفوها بطريقة أخرى ») puis relus (« نعاود نقرا ») : `su_z1_puissances` (blocs peints 2, 4, 8 ; on recule en divisant par 2 → 2⁰ = 1), `su_z2_ordre_garde` (deux points qui glissent : + 2, × 2 ; image de la file d'élèves), `su_z3_ordre_inverse` (miroir en 0 pour × (−1) ; pain coupé en 2 ou en 4 pour l'inverse ; **question « À toi »** −6 > −15), `su_z4_difference` (a > b ⇔ a − b > 0, flèche de b vers a ; application uₙ₊₁ − 1 > 0), `su_z5_denominateur` (barres peintes 1/2 + 1/3 = 5/6, puis 4 − 6/(1 + x)). |
| `su_a3_termes` | **Trop vite** : deux façons de définir une suite (explicite, récurrence) d'un souffle. | Découpée : `su_a3_termes` (formule en n) + `su_a3b_recurrence` (la machine), chacune ses arrêts sur image. |
| `su_a9_sommes` | **Trop vite** : deux formules de somme d'un coup ; la somme arithmétique dite une seule fois. | Découpée : `su_a9_sommes` (arithmétique, **deuxième explication** : les paires de Gauss 1 + 10, 2 + 9…) + `su_a9b_somme_geo` (géométrique ; la question et ses réactions y passent, inchangées). |
| `su_r1_dominos` | **Notion dite une fois** (le principe de récurrence). | Deuxième façon ajoutée : l'échelle (premier barreau, puis de chaque barreau au suivant), puis relecture des trois mots. |
| `su_r2_trois_titres` | **Trop vite** : les trois titres d'une récurrence, l'hypothèse, la cible et la phrase interdite en une voix (exemple cité par la consigne). | Découpée en trois : `su_r2_trois_titres` (annonce + Initialisation), `su_r2b_heredite` (hypothèse pour UN n, cible ; deuxième façon : le domino n et le suivant), `su_r2c_conclusion` (Conclusion + phrase barrée). Même vue `calculs.html?vue=r2`, un arrêt par titre. |
| `su_r3_heredite_affine` | Donnée fausse : le `centre` citait un mot absent de la voix (et l'exemple uₙ > 16, alors que la voix fait uₙ > 1 avec 1/16). | `centre` corrigé (uₙ > 1 ⇒ (1/16)uₙ > 1/16 ⇒ … > 1) sur un mot de la voix ; voix inchangée. |
| `su_r4_heredite_fraction` | **Trop vite** : l'échec de l'essai, l'idée (uₙ₊₁ − 1), le même dénominateur et les deux signes dans la même voix. Prérequis : signe d'une différence, même dénominateur (désormais en z4, z5). | Découpée : `su_r4_heredite_fraction` (pourquoi ça bloque + l'idée, renvoi au rappel z4) + `su_r4b_calcul` (le calcul, la question y passe). |
| `su_x4_retour` | **Trop vite** : deux cas (vₙ = uₙ − 16, puis vₙ fraction avec produit en croix) d'un coup. | Découpée : `su_x4_retour` (cas simple) + `su_x4b_fraction` (produit en croix, regrouper, factoriser). |
| `su_l1_converge` | **Notion dite une fois** (converger). Résultat dit avant la question (16). | Deuxième façon : la distance entre uₙ et 16 qui devient aussi petite qu'on veut. La question reste (lecture), voir « non fait ». |
| `su_l4_qn_negatif` | **Trop vite** : trois valeurs de q négatives puis le tableau des quatre cas, puis la question. **Résultat décisif donné** : « les points se rapprochent de 0 » pour q = −1/2, que l'élève voit lui-même. | Découpée : `su_l4_qn_negatif` (q négatif) avec **question d'observation** (« q = −1/2 : où vont les points ? », silence, 2 indices, 3 cartes ; `qn.html?vue=negatif` tait « → 0 » avec `conclusions: 0`) ; `su_l4c_quatre_cas` (le tableau des quatre cas, la question y passe). |
| `su_c1_plafond` | **Résultat décisif donné** : la voix dit que la suite se tasse et converge pendant que l'élève pourrait le voir. | **Question d'observation** après « la suite est majorée par cinq. » (la simulation n'a encore tracé ni ℓ ni « converge ») ; la phrase suivante de la voix confirme. Voix inchangée (piste gardée). |
| `su_c4_comparaison` | **Notion dite une fois** (critère de comparaison). | Deuxième façon : quelqu'un qui marche entre deux amis qui arrivent au même endroit. |
| `su_e1_complet` | **Résultat à l'écran** : les puces donnaient « lim uₙ = 2 », la réponse de la question. | Puces sans les résultats (décroissante, raison, limite) ; voix inchangée. |
| `su_f7_national` | **Résultat donné** : la voix, les puces et la construction écrivaient « croissante, vers 3 », la réponse de la question. | Voix sans la conjecture ; puces = l'ordre de travail ; `escalier.html?vue=national&conclusions=0` écrit « conjecture : ? ». |

Constats notés sans changement (pour ne pas multiplier les voix ni les questions d'observation, 2 au plus par cours) :
- `su_l3_qn_positif`, `su_l2_reference` : trois cas chacun, mais un arrêt sur image par cas (`play_until`) et une phrase par cas : rythme acceptable.
- `su_f2_place_u0` : l'effet de u₀ < 1 (l'escalier monte) est dit au lieu d'être trouvé ; candidat à une observation si l'on en veut une troisième.
- `su_m2_difference`, `su_l5_avec_qn`, `su_l6_fraction` : exemples résolus (le résultat est la démonstration du geste), gardés.
- `su_l1_converge` : la question « vers quel nombre ? » suit une voix qui dit 16 ; à réécrire si l'on revoxe la diapo une deuxième fois.
- `su_e1_complet` : la voix enchaîne les cinq questions du national (c'est un plan de travail, pas une explication) ; gardée.

### Rythme et blocs
Séances refaites (3 blocs chacune, la dernière 2) ; un seul tableau « À toi » par bloc (vérifié par script) :
S1 `su_s0_b1` [o1, z1, z2, z3 ✏️] · `su_s0_b2` [z4, z5, a1, a2 ✏️] · `su_s1_b2` [a3, a3b, a4, a5 ✏️] — S2 `su_s1_b3` [a6, a7, a8] · `su_s1_b4` [a9, a9b ✏️] · `su_s2_b1` [r1, r2, r2b, r2c] — S3 `su_s2_b1b` [r3, r4, r4b ✏️] · … (suite inchangée, `su_s3_b3` + x4b, `su_s4_b1` + l4c).
Nouveaux blocs : cahier, `retrouver` et `exercice` écrits (non joués). Compétences mises à jour (rappels → K1).

### Voix à enregistrer (voix Bodi)
**22 pistes de diapo** (audio retiré) : `su_z1_puissances`, `su_z2_ordre_garde`, `su_z3_ordre_inverse`, `su_z4_difference`, `su_z5_denominateur`, `su_a3_termes`, `su_a3b_recurrence`, `su_a9_sommes`, `su_a9b_somme_geo`, `su_r1_dominos`, `su_r2_trois_titres`, `su_r2b_heredite`, `su_r2c_conclusion`, `su_r4_heredite_fraction`, `su_r4b_calcul`, `su_x4_retour`, `su_x4b_fraction`, `su_l1_converge`, `su_l4_qn_negatif`, `su_l4c_quatre_cas`, `su_c4_comparaison`, `su_f7_national`.

**Nouvelle question** `su_z3_ordre_inverse` / `q` (« 2 < 5, × (−3) ») : énoncé (`enonce_dit`) 1, démonstration 1, réactions 5 (`0/1`, `0/2`, `1/juste`, `2/1`, `2/2`) → 7 pistes.

**Questions d'observation** (2) :
- `su_l4_qn_negatif` : énoncé « q = −1/2 : où vont les points quand n grandit ? », 2 indices, 3 retours, 1 solution → 7 pistes.
- `su_c1_plafond` : énoncé « Les points montent sans traverser y = 5. Que font-ils quand n grandit ? », 2 indices, 3 retours, 1 solution → 7 pistes.

Questions déplacées sans changement (a9 → a9b, r4 → r4b, l4 → l4c) : leurs énoncés et réactions gardent leurs pistes.
Blocs nouveaux (`retrouver`, `exercice`) : non joués aujourd'hui, pas de voix (comme tous les blocs).

**Total : 22 + 7 + 14 = 43 pistes.**

### Vérification
- `node --check` : `rappels.html`, `qn.html`, `escalier.html` (scripts en ligne extraits) : OK.
- `verif_maths.py math_ch3_suites_numeriques --sims` : **OK** (70 diapos, 20 blocs ; JSON LF, blocs, un « À toi » par bloc, chaque mot du pointage / centre / apres_mot dans sa voix, chaque moment et repère cité trouvé en ouvrant les simulations dans Chromium sans écran, aucune erreur JS ; seuls avertissements : bilan.html et carte.html, déjà présents dans le cours en ligne). L'erreur du cours en ligne (`su_r3_heredite_affine`, mot du centre absent) est corrigée.
- `verifier_texte_corpus.py` : les mots darija rares introduits ont été remplacés (ضربة, التلاميذ, الخبز, كنقسمو…) ; restent des termes du programme en français (inégalité, fractions, numérateurs, sixièmes, multiplier, additionner) gardés exprès, et des formes verbales darija déjà présentes dans tout le cours.

### Non vérifié
- Le son : aucune piste générée (pas de GPU) ; le rendu de la voix sur les nouveaux termes (« inégalité », « sixièmes », « numérateurs ») reste à écouter.
- Le lecteur réel (`CourseFocusStage`) n'a pas été lancé : les questions d'observation et les arrêts des diapos découpées (sans `demarrer`, premier `play_until` au premier mot) sont vérifiés par données et par la simulation seule.
- Le contrôle du cadre (`controler_cadre.py`) et `preparer_reponses.py verifier` (qui exige les pistes) n'ont pas été passés.

---

## Cours 4 — Fonctions primitives (`math_ch4_primitives`)

Copie en attente : `backend/data/courses/en_attente/math_ch4_primitives.json` (44 → 53 diapos, 14 → 18 blocs, 5 → 6 séances, 138 → 162 min). Script de construction reproductible : `build_math_ch4_primitives.py` (dossier de travail de la session).

### Ouverture

- **pr_o2 « Ce qu'on sait déjà : le tableau des dérivées »** — *trop vite* : puissances, racine, inverse, sinus et cosinus enchaînés dans une seule voix ; *prérequis supposés* : la dérivée elle-même (pente), (xⁿ)′, l'écriture en puissance (1/x², √x), la dérivée d'un produit (utilisée dès pr_d4), cos/sin (pr_u6) ; *résultat donné* : la voix dit « x cube donne trois x carré », puis la question demande la dérivée de x³.
  **Fait :** pr_o2 retiré, remplacé par cinq rappels, une notion chacun, chacun expliqué deux fois (définition + animation, puis « بطريقة أخرى ») et relu (« نعاود نقرا ») :
  - `pr_z1_pente` — la dérivée est la pente de la tangente (point qui glisse, tangente qui monte / descend) ; 2ᵉ façon : la route qui monte, descend, plate → (k)′ = 0 (utilisé ensuite pour F + k).
  - `pr_z2_puissances` — (xⁿ)′ = n xⁿ⁻¹ (le 3 de x³ descend devant) ; 2ᵉ façon : l'escalier des exposants. Question nouvelle : dérivée de x⁵ (la voix ne la dit pas) ; l'ancienne question (x³) part en réserve de fin de cours.
  - `pr_z3_ecrire` — 1/xⁿ = x⁻ⁿ (x² monte du bas vers le haut), √x = x^(1/2) ; 2ᵉ façon : √x·√x = x, deux demis font un ; puis (1/x)′ et (√x)′ redonnés par la règle des puissances (prérequis de pr_u4, pr_u5).
  - `pr_z4_produit` — (uv)′ = u′v + uv′ ; 2ᵉ façon : le contre-exemple x·x (facteur par facteur donne 1, la règle donne 2x).
  - `pr_z5_cos_sin` — cos x et sin x sur le cercle, leurs dérivées ; 2ᵉ façon : la pente de la courbe de sin se lit dans cos (1 en 0, 0 au sommet). Question nouvelle : la pente de sin en π (cos π = −1) ; l'ancien exercice (dérivée de cos x) part en réserve.
  Simulation nouvelle : `primitives-tableau/rappels.html` (vues `pente`, `puissances`, `ecrire_puissance`, `produit`, `cos_sin`, `puissance_u`).

### I. Définition

- **pr_d2** — *notion expliquée une seule fois* (la définition, la plus importante du chapitre). **Fait :** deuxième explication ajoutée (F est la route, f la pente de la route en chaque point ; connaître la pente partout permet de redessiner la route) et relecture de la définition. Pointage inchangé.

### II. Existence, famille, condition

- **pr_e4** — *trop vite* : deux démonstrations dans une même voix (F + k est une primitive ; il n'y en a pas d'autres). **Fait :** coupé en `pr_e4` (F + k, avec la vue coupée `etapes.html?vue=e4_plus_k` ; 2ᵉ façon : k déplace la courbe sans changer sa pente) et `pr_e4_b` (G − F constante ; 2ᵉ façon : deux personnes qui marchent à la même vitesse gardent le même écart).
- **pr_e5** — *résultat décisif donné* : « les tangentes sont toutes parallèles » est dit pendant que l'élève pourrait le voir. **Fait :** question d'observation (voix inchangée, elle s'arrête après « فكل courbe، طرف صغير ديال la tangente: » et reprend sur « كاملين متوازيين ») ; `famille.html` reçoit le paramètre `conclusions` (défaut 1, comportement d'avant) qui tait « même pente : 2 » pendant la question.
- **pr_e7** — *résultat décisif donné* : la voix calcule k = 11/6 puis demande « combien trouves-tu pour k ? ». **Fait :** la voix s'arrête au remplacement ; la vue `etapes.html?vue=e7_remplacer` n'écrit pas la suite ; l'élève regroupe et résout (la démonstration de la question, déjà voixée, donne le calcul après sa réponse).

### III. Le tableau des primitives usuelles

- **pr_u3** — *résultat donné* : la voix calcule x⁴/2, puis la question demande une primitive de 2x³. **Fait :** voix arrêtée à « le coefficient reste devant » (vue `etapes.html?vue=u3_devant`) ; 2ᵉ façon : comme pour la dérivée, le 2 reste devant.
- **pr_u4** — *trop vite* : 1/x², 1/x⁴ et la règle générale d'un coup. **Fait :** `pr_u4` (1/x² seul, vérifié en dérivant : deuxième façon) et `pr_u4_b` (1/x⁴ puis la règle 1/xⁿ).
- **pr_u5** — *trop vite* : 1/√x, la règle xʳ et ∛x d'un coup ; *prérequis supposé* : (√x)′ (enseigné maintenant en pr_z3). **Fait :** `pr_u5` (1/√x → 2√x, retrouvé une 2ᵉ fois par les puissances) et `pr_u5_b` (xʳ et ∛x).
- **pr_u6** — *résultat donné* : « une primitive de sin x est −cos x » dit avant la question. **Fait :** la voix montre le sens de la flèche verte sur cos x → sin x, puis laisse l'élève partir de sin x.

### IV. Somme, produit

- **pr_l1** — *résultat donné* : la voix calcule exactement les primitives de 5x⁴ + 3x + 1 que la question demande. **Fait :** exemple différent dit à voix (2x + 3) ; 2ᵉ façon pour « une seule constante » (k₁ + k₂ est encore une constante).
- pr_l3 nomme d'autres gestes (développer, puissance) sans les détailler : laissé tel quel (simple annonce, la puissance est maintenant enseignée en pr_z3).

### V. Formes composées

- **pr_c1** — *prérequis supposé* : la dérivée de uⁿ (« dérivée qu'on connaît ») ; *trop vite* : dérivée de uⁿ⁺¹, division, règle et exemple d'un coup ; *résultat donné* : l'exemple dit ((x² + 1)⁴)′ = 8x(x² + 1)³, la question de la diapo. **Fait :** `pr_c1` devient le rappel « dériver une puissance d'une expression » (exemple (x² + 1)³, autre que celui de la question ; 2ᵉ façon : une boîte dans une boîte, dehors puis dedans ; vue `rappels.html?vue=puissance_u`), la question reste ; `pr_c1_b` = la forme u′uⁿ lue à l'envers (2ᵉ façon : comme xⁿ, si u′ est là), avec l'exercice « primitive de u′u⁴ » qui y passe (il demandait la forme avant qu'elle soit enseignée, règle 27).
- **pr_c3** — *trop vite* : « il manque 2 » et le piège « il manque x » dans la même voix. **Fait :** `pr_c3` (multiplier et diviser par 2 ; 2ᵉ façon : ajouter puis enlever la même chose ne change pas f) et `pr_c3_b` (on ne prête qu'un nombre, jamais x).
- **pr_c4**, **pr_c7** — *résultat donné* : la primitive est calculée dans la voix, puis demandée au tableau. **Fait :** voix arrêtée après la réécriture (vues `etapes.html?vue=c4_reecrire`, `c7_reecrire`) ; l'élève applique la règle.
- pr_c8 (trois dénominateurs), pr_c9, pr_r3 (organigramme) : plusieurs cas sur une diapo, mais ce sont des diapos de synthèse après que chaque cas a été vu, avec un arrêt par colonne / branche : laissées telles quelles.

### VI–VIII. Reconnaître, graphique, types national

- **pr_r1** — *résultat donné* : « les primitives sont x sin x + k » dit avant la même question. **Fait :** la voix repère u et v et s'arrête avant la conclusion.
- **pr_g2** — *résultat décisif donné* : « où f est négative, F descend ». **Fait :** question d'observation (voix inchangée, arrêt après « شوف الفوق: la courbe de F تعاودات بنفس الألوان. », reprise sur « فين f positive، F كتطلع ») ; `pente.html` reçoit le paramètre `conclusions` (défaut 1) qui tait « f > 0 : F monte / f < 0 : F descend ».
- pr_x1–pr_x3 : rédactions complètes, mais ligne par ligne avec un arrêt par ligne (règle 33 respectée) : inchangées.

### Simulations

- Nouvelles : `primitives-tableau/rappels.html` (6 vues) ; `primitives-tableau/etapes.html` (vues `e4_plus_k`, `e7_remplacer`, `u3_devant`, `c4_reecrire`, `c7_reecrire` : les calculs de `calculs-vues.js`, non modifié, coupés avant le résultat).
- Enrichies sans changer le comportement par défaut : `famille.html` (vue `famille`) et `pente.html` (vue `pente`) : paramètre `conclusions` 0/1, défaut 1.

### Voix à enregistrer (Bodi) — cours 4

- **Diapos (23)** : pr_z1_pente, pr_z2_puissances, pr_z3_ecrire, pr_z4_produit, pr_z5_cos_sin, pr_d2, pr_e4, pr_e4_b, pr_e7, pr_u3, pr_u4, pr_u4_b, pr_u5, pr_u5_b, pr_u6, pr_l1, pr_c1, pr_c1_b, pr_c3, pr_c3_b, pr_c4, pr_c7, pr_r1.
- **Questions nouvelles (2)** : pr_z2_puissances `q` (« Quelle est la dérivée de x⁵ ? ») et pr_z5_cos_sin `q` (« la pente de la courbe de sin en π ») : énoncé `enonce_dit` + démonstration + 5 réactions chacune (juste, 1, 2) → 2 énoncés, 2 démonstrations, 10 réactions.
- **Questions d'observation (2)** : pr_e5 (« En x = 1, compare les petites tangentes… ») et pr_g2 (« Là où la courbe de f est orange… ») : chacune 1 énoncé, 2 indices, 3 retours, 1 solution → 14 pistes.
- Total : 23 + 2 + 2 + 10 + 14 = **51 pistes**. Les questions gardées (pr_c1 q, pr_u3 q, pr_c4 q, pr_c7 q, pr_e7 q, pr_l1 q, pr_r1 q, pr_u6 q, pr_g2 q) n'ont pas changé : leurs pistes restent valables. Les blocs nouveaux (`pr_s1_b1b`, `pr_s2_b1b`, `pr_s2_b3b`, `pr_s3_b2b`) ont leurs `retrouver` / `exercice` écrits mais non joués (pas de voix à faire maintenant).

### Non vérifié

- Le rendu dans le lecteur (`CourseFocusStage`) : timings des arrêts sur les mots, ouverture des deux questions d'observation, `sim_avant` qui tait la conclusion au chargement ; seules les simulations ont été ouvertes sans écran (Playwright : aucune erreur JS, moments et repères présents) ; `verif_maths.py --sims` : OK (les avertissements bilan/carte existaient déjà sur le cours en ligne).
- Le compte des mots rares (`verifier_texte_corpus.py`) : les mots rares introduits ont été remplacés ; restent des termes du programme de maths (pente, tiers, quarts, bulle, rationnel…) et des formes déjà présentes dans le cours en ligne (كندريفيو…).
- `controler_cadre.py` et `preparer_reponses.py verifier` non lancés (pistes absentes par construction) ; pas de `cahier_figures` nouvelles.

---

## Chapitre 5 — Fonctions logarithmiques (`math_ch5_fonctions_ln`)

Copie en attente : `backend/data/courses/en_attente/math_ch5_fonctions_ln.json` (65 diapos au lieu de 53, 19 blocs au lieu de 14, 7 séances au lieu de 5 ; 192 min au lieu de 165). Script reproductible : `build_math_ch5_fonctions_ln.py` (scratchpad de la session).

### Ouverture

- **ln_o2 « Trois gestes à avoir en main »**
  - *Trop vite* : trois prérequis enchaînés dans une seule voix (une primitive de x³, le signe d'un quotient, le sens d'une inégalité).
  - *Prérequis supposés* : le cours utilise aussi, sans les enseigner, la définition d'une primitive (n1 à n3), les puissances négatives et x^(1/2) (n1, a4), le signe d'une expression affine (d2, v3, e2), le second degré (q1, q4).
  - *Fait* : ln_o2 est supprimée. À sa place, cinq rappels, un prérequis par diapo. Chacun est expliqué d'une première façon (définition + animation, un arrêt par étape), puis d'une seconde façon (« دابا نشوفوها بطريقة أخرى »), puis relu (« نعاود نقرا »). Ils utilisent une nouvelle simulation, `ln-tableau/rappels.html` :
    - `ln_z1_primitive` (vue `primitive`) : un point glisse sur la courbe de x² avec sa tangente, et la pente 2x s'écrit, donc F′ = f. Seconde façon : la courbe montée de 3 garde les mêmes pentes.
    - `ln_z2_puissances` (vue `puissances`) : des blocs peints de hauteurs 8, 4, 2, 1 et 1/2 ; chaque marche divise par 2, d'où 2⁰ = 1 et 2⁻¹ = 1/2. Seconde façon : la règle xⁿ·xᵐ = xⁿ⁺ᵐ, qui donne x⁻¹ = 1/x et √x = x^(1/2).
    - `ln_z3_signe` (vue `signe`) : un point glisse sur l'axe et x − 1 s'écrit en rouge, puis en vert ; ensuite le tableau de signe. Seconde façon : la droite y = x − 1, sous l'axe puis au-dessus.
    - `ln_z4_sens` (vue `sens`) : on multiplie par −1, et 2 et 3 passent de l'autre côté de 0. Seconde façon : un contre-exemple (« −2 < −3 serait faux »). Exemple : −2x > 4. **Question « À toi » nouvelle** : « −3x < 6 ⇔ ? », avec ses réactions juste / 1 / 2 et sa démonstration.
    - `ln_z5_second_degre` (vue `second_degre`) : Δ, puis les deux solutions de x² + x − 6 = 0. Seconde façon : la parabole coupe l'axe en −3 et en 2, plus une vérification par substitution. C'est l'équation que l'élève retrouve en ln_q1_b.
  - L'exercice de réserve de ln_o2 (une primitive de x⁵) passe sur ln_z1. La question écrite pour ln_z2 (x⁻² = ?) est mise en réserve (`exercices_fin_de_cours`) : sinon, deux tableaux « À toi » n'auraient été séparés que par une seule diapo.

### I–II. Naissance de ln, courbe

- **ln_n1 / ln_q6** : le pointage du cours en ligne contient un repère mort (« بالأصفر، السؤال باقي: » et « سؤال: شنو هو le couple solution؟ » ne sont pas dans la voix). Ce repère est retiré ; la voix ne change pas.
- **ln_n3** (définition de ln) : *notion expliquée une seule fois*. Une seconde façon est ajoutée : on connaît la pente en chaque point (1/x) et le point de départ (1 ; 0), et cela suffit pour tracer la courbe. La définition est ensuite relue.
- **ln_c2** (signe de ln) : *résultat décisif donné*. Le signe se lit sur la courbe, mais la voix le disait avant que l'élève ait regardé, puis elle donnait l'exemple ln(3/4) < 0 juste avant la question sur ln(3/4).
  - *Fait* : une **question d'observation** (« Entre 0 et 1, où est la courbe par rapport à l'axe ? »). La voix s'arrête sur la courbe seule (moment `courbe`, avant que la partie orange et « ln x < 0 » ne s'écrivent). Il y a deux indices, trois cartes, un retour par carte et une solution.
  - La phrase suivante de la voix confirme la réponse (« إيه، تحت l'axe »). L'exemple ln(3/4) n'est plus dit : c'est la question. Une seconde explication est ajoutée (ln est croissante et vaut 0 en 1).
- **ln_d1** (domaine) : *résultat donné*. La voix calculait D_f = ]3 ; +∞[, puis posait exactement cette question.
  - *Fait* : la voix s'arrête à la condition 2x − 6 > 0. Une seconde façon est ajoutée : ln est une porte qui ne laisse passer qu'un nombre positif, et ln(−1) et ln 0 n'existent pas. La règle est relue, puis vient la question.

### IV. Règles de calcul

- **ln_a1** (règle du produit) : *résultat décisif donné*. « La pile tombe juste sous ln 6 » était dit à la place de l'élève.
  - *Fait* : une **question d'observation** (« ln 3 posé sur ln 2 : jusqu'où arrive la pile ? »). `barres.html?vue=produit` reçoit le paramètre `conclusions`, qui vaut 1 par défaut, donc la simulation se comporte comme avant. À 0, il cache les pointillés et la somme écrite pendant la question.
  - Une seconde façon est ajoutée : ln change les produits en sommes, comme les zéros (10 × 100 = 1000, un zéro plus deux zéros donnent trois zéros).
- **ln_a3** : *trop vite* (l'inverse et le quotient, plus un exemple, dans une même voix). Découpée en `ln_a3` (l'inverse, avec en seconde façon ln(1/2) = −ln 2 lu comme un nombre négatif) et `ln_a3_b` (le quotient et l'exemple ln(1/8)).
- **ln_a4** : *trop vite* (puissance, racine, cas général et exemple). Découpée en `ln_a4` (la puissance, avec en seconde façon a⁴ comme quatre blocs ln a) et `ln_a4_b` (la racine, le cas général, l'exemple), avec un arrêt par étape.
- **ln_a5** : *résultat donné*. A = (5/2) ln 2 − 2 ln 3 était dit, puis demandé. *Fait* : la voix s'arrête après le développement ; le regroupement est laissé à l'élève.
- **ln_a6** : *deux pièges d'un coup*. Découpée en `ln_a6` (la somme) et `ln_a6_b` (le carré et la valeur absolue, avec une phrase sur ce que fait |·|).

### V. Équations

- **ln_q1** : *trop vite et résultat donné*. Domaine, rassemblement, second degré, tri, puis S = {2}, et ensuite la même question.
  - *Fait* : découpée en `ln_q1` (domaine, puis « on enlève les ln ») et `ln_q1_b` (le second degré, appuyé sur le rappel ln_z5). La voix s'arrête avant le tri : choisir les solutions est la question. La question, l'exercice et les réactions passent sur ln_q1_b ; ils ne changent pas et gardent leurs pistes.
- **ln_q5** : *résultat donné*. Le tri et S = {e} étaient dits avant la question. *Fait* : la voix s'arrête sur l'axe des x permis.

### VI. Limites

- **ln_l2** : *résultat donné*. « La courbe ne coupe jamais l'axe des ordonnées » était dit juste avant la question qui le demande. Cette phrase est retirée.
- **ln_l6** : *résultat donné*. La conclusion +∞ était dite avant la question. *Fait* : la voix s'arrête à la limite de base (ln x)/x → 0.
- **ln_l5** : deux limites, mais la seconde se déduit en une phrase et chaque étape a son arrêt. Laissée telle quelle.

### VII–VIII. Dérivée, primitives

- **ln_v1** : *résultat donné* (la voix dérivait exactement la fonction de la question) et *notion expliquée une seule fois*.
  - *Fait* : une seconde façon est ajoutée. ln(2x) = ln 2 + ln x a pour dérivée 1/x, et la règle donne aussi 2/(2x) = 1/x.
  - La voix s'arrête à u′ = 2x ; le tableau s'arrête au moment `u`, avant `resultat`.
- **ln_v2** : *trop vite* ((ln x)², x ln x, puis un problème du national). Découpée en `ln_v2` et `ln_v2_b` (le national 2019, terme par terme).
- **ln_p1** : *résultat donné*. La primitive de l'exemple était dite et écrite, puis demandée. *Fait* : la voix s'arrête à « u′ = 2x, c'est le haut » ; le tableau s'arrête au moment `nouveau`.

### IX. Étude, type national

- **ln_e3** : *trop vite* (tableau, minimum, deux limites, asymptote). Découpée en `ln_e3` (les flèches et le minimum) et `ln_e3_b` (les limites aux bornes et la phrase qu'elles donnent).
  - Le cours en ligne avait aussi un `play_until {minimum}` vers un moment qui n'existe pas (minimum est un repère de la vue `variations`) : il est corrigé en `repere`.
- **ln_e5** : *trop vite et résultat donné*. Tout le problème du national 2021 était dit en une seule voix, f′ compris, puis la question demandait f′.
  - *Fait* : découpée en trois diapos.
    - `ln_e5` : le point O, puis l'annonce de la dérivée. C'est la question, qui ne change pas.
    - `ln_e5_b` : f′ = 2 ln x, ce qui confirme la réponse, puis le signe, le minimum et f(e) = 0.
    - `ln_e5_c` : la courbe, puis l'inégalité.
- **ln_e1** : la conclusion est dite avant la question QCM, mais la question porte sur la reconnaissance du raisonnement. Laissée, à revoir avec le professeur.

### Blocs et séances

- Séance 0 nouvelle, « Ce qu'il faut savoir avant ln » : `ln_s0_b1` (o1, z1, z2) et `ln_s0_b2` (z3, z4, z5).
- Nouveaux blocs, chacun avec son cahier, son « retrouver » et son exercice :
  - `ln_s2_b2b` (a4, a4_b, a5) ;
  - `ln_s2_b4` (a8, q1, q1_b) ;
  - `ln_s5_b1b` (e5, e5_b, e5_c).
- Le bloc `ln_s1_b1` demandait la définition de ln avant ln_n3 (règle 27) : son « retrouver » demande maintenant pourquoi la règle des puissances échoue pour 1/x.
- Il y a au plus un tableau « À toi » par bloc, et au moins deux diapos sans rien entre deux tableaux.
- Compétences mises à jour : z1 et z2 vont en K1, z3 et z4 en K2, z5 et q1_b en K4, les découpes de règles en K3, v2_b en K6, e3_b, e5_b et e5_c en K8.

### Voix à enregistrer (Bodi)

- **30 pistes de diapo** (`audio.mixed` retiré) :
  - rappels : ln_z1_primitive, ln_z2_puissances, ln_z3_signe, ln_z4_sens, ln_z5_second_degre ;
  - naissance, courbe et domaine : ln_n3, ln_c2, ln_d1 ;
  - règles : ln_a1, ln_a3, ln_a3_b, ln_a4, ln_a4_b, ln_a5, ln_a6, ln_a6_b ;
  - équations : ln_q1, ln_q1_b, ln_q5 ;
  - limites : ln_l2, ln_l6 ;
  - dérivée et primitives : ln_v1, ln_v2, ln_v2_b, ln_p1 ;
  - étude : ln_e3, ln_e3_b, ln_e5, ln_e5_b, ln_e5_c.
- **Question nouvelle de ln_z4_sens** (« −3x < 6 ⇔ ? ») : l'énoncé dit, la démonstration et 5 réactions (option 1 juste ; options 0 et 2 avec 1 et 2), soit **7 pistes**.
- **Observation de ln_c2** (« Entre 0 et 1, où est la courbe de ln par rapport à l'axe ? ») : l'énoncé dit, 2 indices, 3 retours et la solution, soit **7 pistes**.
- **Observation de ln_a1** (« ln 3 posé sur ln 2 : jusqu'où arrive la pile ? ») : l'énoncé dit, 2 indices, 3 retours et la solution, soit **7 pistes**.
- **Total à enregistrer : 51 pistes** (30 + 7 + 7 + 7).
- En réserve, non joués aujourd'hui :
  - l'exercice x⁻² de ln_z2, avec 5 réactions écrites et sans audio ;
  - les « retrouver » et exercices des blocs nouveaux, qui ne sont pas voixés (`FIN_DE_BLOC_COMPLETE = False`).
- Les questions déjà en ligne (c2, d1, a1, a5, q1 → q1_b, q5, l2, l6, v1, p1, e5) ne changent pas et gardent leurs pistes d'énoncé et de réactions.

### Non vérifié

- La voix réelle (Bodi) : rien n'a été généré. `verifier_texte_corpus.py` ne signale plus de mot darija rare parmi ceux ajoutés. Restent des termes du programme rares dans le corpus, gardés exprès : discriminant, parabole, l'inégalité.
- Le jeu dans le lecteur concentration (`CourseFocusStage`) : l'arrêt sur `apres_mot`, l'envoi de `{conclusions: 0/1}` à `barres.html` et la reprise de la voix n'ont pas été rejoués dans le navigateur avec le cours.
  - Vérifié sans écran : les moments, les repères, l'absence d'erreur JS des vues nouvelles et le rendu à la craie (captures).
- Les dessins du cahier (`cahier_figures`) n'ont pas été ajoutés pour les blocs de rappel. `verifier_figures_cahier.py` n'a pas été lancé.
- `controler_cadre.py` n'a pas été lancé sur la copie en attente.

---

## Cours 6 — Nombres complexes (première partie) · `math_ch6_nombres_complexes`

Copie en attente : `backend/data/courses/en_attente/math_ch6_nombres_complexes.json` (58 diapos au lieu de 48, 19 blocs au lieu de 12, 7 séances au lieu de 4). Construite par un script reproductible à partir du cours en ligne (non modifié).

### Ce qui a été trouvé, diapo par diapo, et ce qui a été fait

**Ouverture**
- `nc_o2` « Trois gestes à avoir en main » — *trop vite + prérequis supposés* : le discriminant, cos/sin de π/3 et (a − b)(a + b) donnés d'un seul souffle, comme déjà connus, sans image. Le discriminant ne sert pas dans cette première partie. Par contre, le cours suppose connus, sans les enseigner, le repère et les coordonnées (`nc_a3`, `nc_p1`), le vecteur et « arrivée moins départ » (`nc_p3`, `nc_p4`, `nc_m4`, `nc_i1`), Pythagore (`nc_m1`), le cercle trigonométrique, les radians et cos/sin (`nc_g1` à `nc_t6`), et le développement avec les identités remarquables (`nc_c1` à `nc_c3`, `nc_j4`).
  → **Diapo supprimée, remplacée par cinq rappels enseignés de zéro**, un prérequis par diapo. Chacun a une animation à la craie, une première explication (définition et animation, avec un arrêt sur image par étape), puis « دابا نشوفوها بطريقة أخرى » (une autre image), puis « نعاود نقرا » :
  - `nc_z1_repere` : les axes, M(3 ; 2), on avance puis on monte ; la deuxième façon est le rang et la place en classe : (3 ; 2) ≠ (2 ; 3).
  - `nc_z2_vecteur` : la flèche AB, le déplacement +3 et −3, AB(xB − xA ; yB − yA) ; la deuxième façon est un chemin, le même déplacement parti de O.
  - `nc_z3_pythagore` : le triangle OHM, OM² = 9 + 16, OM = 5 ; la deuxième façon est une échelle **peinte** contre un mur de briques (3 m, 4 m, 5 m), selon la règle 32.
  - `nc_z4_cercle` : le rayon 1 ; un tour vaut 2π, un demi-tour π, un quart de tour π/2 ; M(cos θ ; sin θ) ; la deuxième façon est la lumière d'en haut : la projection de M sur l'axe, c'est cos θ.
  - `nc_z5_identites` : chaque terme fois chaque terme, (a + b)², (a − b)(a + b) ; la deuxième façon est l'aire d'un carré de côté a + b coupé en a², ab, ab, b².
  - Les exercices de réserve de `nc_o2` passent sur `nc_z5_identites`.

**I. Le nombre i**
- `nc_a3` (forme algébrique) — *notion expliquée une seule fois.* → Deuxième explication ajoutée : z comme une adresse sur une carte (a pour aller à droite, b pour monter).
- `nc_a6` (puissances de i) — *résultat décisif donné* (i⁴ = 1, le retour au départ), alors que la simulation le montre. → **Question d'observation n° 1** : la voix s'arrête après « i cube égale moins i » et le tuteur fige la simulation sur `tours`. Pendant la question, la simulation écrit « i⁴ = ? » (nouveau paramètre `conclusions` de `nombre-i.html?vue=cycle`) ; le tuteur demande sur quel nombre le point se pose (−i, **1**, i). La phrase suivante de la voix confirme la réponse. La voix est inchangée, donc la piste en ligne est gardée.

**II. Calcul algébrique** — rien à changer : les diapos `c1` à `c4` sont déjà découpées ligne par ligne, avec un arrêt sur image par ligne. Le prérequis (développer) est maintenant enseigné en `nc_z5`.

**III. Plan complexe**
- `nc_p4` (milieu) — *résultat donné* : la voix calculait p = 1, puis posait la question « p = ? ». → La voix donne la règle (moyenne des affixes, comme pour les coordonnées du milieu) et s'arrête avant le calcul ; l'arrêt sur `milieu`, qui écrit p = 1, est retiré.

**IV. Conjugué**
- `nc_j3` — *trop vite* : z réel ⇔ z̄ = z, z + z̄ = 2a, z − z̄ = 2ib et le cas imaginaire pur, tout d'un coup. → **Coupée en deux** : `nc_j3` (z réel ⇔ z̄ = z, avec la démonstration −b = b) et `nc_j3_b` (z + z̄ et z − z̄, puis le cas imaginaire pur), chacune avec son arrêt sur image.
- `nc_j4` — *résultat donné* : c·c̄ = 4 était calculé juste avant la question. → La voix s'arrête sur les données de c (« استعمل la règle »).

**V. Module**
- `nc_m1` — *une seule explication.* → Deuxième explication : le module est la longueur du fil tendu de O à M.
- `nc_m3` — *trop vite* : trois règles (produit, quotient, puissance), l'exemple du national et le piège de la somme, dans une seule voix. → **Coupée en deux** : `nc_m3` (le module d'un produit, l'exemple de 2017, et une deuxième façon : le produit reste sur le même cercle jaune quand a tourne) et `nc_m3_b` (quotient et puissance, avec l'exemple |(1 + i)⁴| = 4, puis le piège de la somme).
- `nc_m4` — *résultat donné* : AB = 2√10 était dit avant « calcule AB ». → La voix s'arrête à « la distance AB est le module de b − a ».

**VI. Argument**
- `nc_g1` — *une seule explication.* → Deuxième explication : une aiguille de montre qui tourne à l'envers ; l'argument dit où regarder, le module à quelle distance.
- `nc_g4` — *trop vite* : a = r cos θ, cos θ = a/r, le tableau des angles et l'astuce √k/2, dans une même voix. *Résultat donné* : la colonne π/4 s'allumait (« قرا… بجوج متساويين ») juste avant la question. → **Coupée en deux** : `nc_g4` (a = r cos θ, b = r sin θ, puis cos θ = a/r ; **nouvelle simulation** `etapes.html?vue=cos_sin`, avec une deuxième façon de le dire) et `nc_g4_b` (le tableau et l'astuce, sur `angles.html` ; elle porte la question et l'exercice d'origine, avec leurs réactions). L'arrêt sur `pi_4` est retiré.

**VII. Forme trigonométrique**
- `nc_t1` — *une seule explication.* → Deuxième explication : a + ib dit « combien à droite, combien en haut » ; r(cos θ + i sin θ) dit « dans quelle direction, et jusqu'où ».
- `nc_t3` — *trop vite* : l'exemple −√3 + i, puis les trois règles π − θ, π + θ et −θ récitées d'un trait à la fin. → **Coupée en deux** : `nc_t3` (le seul cas « à gauche en haut ») et `nc_t3_b` (**nouvelle simulation** `etapes.html?vue=quarts` : √3 + i comme angle de départ, puis −√3 + i, −√3 − i et √3 − i, un cas par arrêt sur image).
- `nc_t4` — *trop vite + résultat donné* : deux fausses formes corrigées, puis la question demande exactement la première correction. → **Coupée en deux** : `nc_t4` (le module négatif et la règle « le moins rentre dans l'angle », sans le résultat ; l'élève corrige au tableau « À toi ») et `nc_t4_b` (la correction confirmée, puis la seconde fausse forme −cos θ).

**VIII. Produit, quotient, Moivre**
- `nc_r1` — *résultat décisif donné* : la règle « les arguments s'additionnent ». → **Question d'observation n° 2** : la simulation pose le deuxième arc π/4 et le point tourne jusqu'à 2i ; la voix s'arrête, la simulation écrit « angle : ? » et « longueur : ? » (nouveau paramètre `conclusions` de `produit.html?vue=carre`). Le tuteur demande l'angle de (1 + i)² (π/4 ; **π/4 + π/4 = π/2** ; π/4 × π/4), puis la voix confirme.
- `nc_r2` — *résultat donné* : « elle arrive en −1 + 3i » était dit, puis demandé. → La voix donne la règle (module 1, plus π/2) et s'arrête sur le point de départ ; l'animation qui fait tourner le point n'est plus lancée pendant la voix.
- `nc_r3` — *trop vite* : conjugué, inverse, quotient et opposé dans une même voix. → **Coupée en deux** : `nc_r3` (conjugué et inverse : l'angle change de signe) et `nc_r3_b` (le quotient fait l'inverse du produit ; l'opposé est un demi-tour).
- `nc_r6` — *résultat donné* : la spirale écrit (1 + i)⁸ = 16, et la question demandait (1 + i)⁸. → **Nouvelle question** : (√3 + i)⁶ = ? (64 ; **−64** ; 64i), avec sa démonstration et ses cinq réactions préparées.

**IX. Géométrie**
- `nc_i2` — *résultat donné* : « donc ΩA et ΩB ont la même longueur » était dit avant la question « pourquoi ? ». → La voix s'arrête sur les deux faits à relier (b = ā ; Ω est sur l'axe réel).

**X, bilan, carte** — rien à changer.

### Blocs et séances
Il y a 19 blocs de 2 à 4 diapos, chacun avec **une seule question « À toi » au plus**, posée en dernier. Les blocs de rappels n'ont pas de question. Les nouveaux blocs ont tous leur cahier, leur `retrouver` et leur exercice (non joués). Les sept séances sont : bases et nombre i ; calcul algébrique et affixes ; conjugué et module ; argument ; signes, retour et produit ; quotient, Moivre et géométrie ; sujets nationaux et bilan. Les diapos de rappel vont dans la compétence K1 ; les moitiés de diapo coupée gardent la compétence de la diapo d'origine.

### Simulations
- **Nouvelles :**
  - `operations-formes-tableau/rappels.html`. Vues et moments : `repere` (axes, point, coordonnees, ordre), `vecteur` (points, fleche, deplacement, coordonnees, glisse), `pythagore` (triangle, carres, calcul, echelle, avec l'échelle et le mur peints), `cercle` (cercle, tours, point, cos_sin, ombre), `identites` (distributivite, carre, difference, aire).
  - `operations-formes-tableau/etapes.html`. Vues et moments : `cos_sin` (point, projections, formules, division), `quarts` (reference, haut_gauche, bas_gauche, bas_droite, regle).
- **Enrichies, par ajout seulement :** `nombre-i.html?vue=cycle` et `produit.html?vue=carre` reçoivent un paramètre `conclusions` (1 par défaut, comportement d'avant inchangé ; 0 écrit « ? » à la place du résultat).

### Voix à enregistrer (voix Bodi)
- **28 pistes de diapo**, sur les diapos qui n'ont plus d'`audio.mixed` : nc_z1_repere, nc_z2_vecteur, nc_z3_pythagore, nc_z4_cercle, nc_z5_identites, nc_a3, nc_p4, nc_j3, nc_j3_b, nc_j4, nc_m1, nc_m3, nc_m3_b, nc_m4, nc_g1, nc_g4, nc_g4_b, nc_t1, nc_t3, nc_t3_b, nc_t4, nc_t4_b, nc_r1, nc_r2, nc_r3, nc_r3_b, nc_r6, nc_i2. La voix de `nc_a6` n'a pas changé : sa piste est gardée.
- **Observation `nc_a6`** : l'énoncé (« ربع دورة رابعة. شوف فين وصلات النقطة. على شمن عدد طاحت؟ »), 2 indices, 3 retours et la solution, soit 7 pistes.
- **Observation `nc_r1`** : l'énoncé (« شوف جوج القوسات. شنو هي الزاوية ديال un plus i، au carré؟ »), 2 indices, 3 retours et la solution, soit 7 pistes.
- **Nouvelle question `nc_r6`** (q) : l'énoncé dit, la démonstration, et les réactions 0/1, 0/2, 1/juste, 2/1, 2/2, soit 7 pistes.
- **Total : 49 pistes** (28 + 14 + 7). Les autres questions sont inchangées et gardent leurs pistes ; elles sont seulement déplacées : la question et l'exercice de `nc_g4` sont maintenant sur `nc_g4_b`.
- L'exercice du nouveau bloc `nc_s1_b0` (distance AB) n'est pas joué aujourd'hui ; ses réactions sont à préparer avec la fin de cours.

### Vérifications
- `node --check` passe sur `rappels.html`, `etapes.html`, `nombre-i.html` et `produit.html` (scripts extraits du HTML).
- `verif_maths.py math_ch6_nombres_complexes --sims` : JSON valide, chaque diapo dans un seul bloc, au plus un tableau « À toi » par bloc, chaque `mot` présent dans sa voix, chaque `apres_mot` trouvé une seule fois, aucun hash d'audio périmé, toutes les réactions présentes ; les moments et les repères ont été vérifiés dans les simulations. Il ne reste que les 3 erreurs déjà présentes dans le cours en ligne : les repères `centre`, `branches` et `partie2` de `carte.html`, que le vérificateur ne lit pas.
- Les 9 nouvelles vues ont été ouvertes dans un navigateur sans écran : aucune erreur JS, captures relues.
- `verifier_texte_corpus.py` : les mots rares que j'avais introduits ont été remplacés (الطاولة, الظل, السلم, مستطيلات, تحركنا…). Il reste seulement des termes du programme (Pythagore, l'hypoténuse, coordonnées, modules…) ou des mots déjà présents dans le cours en ligne.

### Non vérifié
- La voix n'est pas générée : la prononciation et les murmures (`detecter_murmures.py`) restent à contrôler sur les 49 pistes.
- Le cours n'a pas été joué dans le lecteur (`CourseFocusStage`). À vérifier dans le lecteur : le moment exact de l'arrêt de la voix pour les deux observations, et l'effet de `sim_avant {conclusions: 0}` pendant la question.
- `controler_cadre.py` n'a pas été lancé sur la copie en attente.
- Les réactions écrites à la main (nouvelle question de `nc_r6`, observations) n'ont pas été passées par `preparer_reponses.py`.
