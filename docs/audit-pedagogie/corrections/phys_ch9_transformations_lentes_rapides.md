# phys_ch9_transformations_lentes_rapides — corrections du 26-27/11/2026

Sources : `ordre-des-notions/phys_ch9_transformations_lentes_rapides.md`, `mesures.md`,
`reference-prof/phys_ch9_transformations_lentes_rapides.md`, règles 52 à 56 du skill professeur.
Rien n'est raccourci, aucune voix n'est générée.

## Phase 1 — cours servi (`backend/data/courses/phys_ch9_transformations_lentes_rapides.json`), sans changer la voix

- **Questions dans les 6 premières diapos : 2 → 0.**
  - Diapo 2 `tl_o1_carte` : la question « quelle question revient au national ? » (options pleines de mots encore
    inconnus) est rangée dans `exercices_fin_de_cours` de la même diapo, avec ses réactions (`reponses_fin_de_cours.e0`).
  - Diapo 5 `tl_x1_zinc` : l'observation « que voit-on sur la lame ? » est retirée (la voix dit tout de suite le dépôt rouge).
  - La question du bloc `tl_s0_b1` (l'ion, après la diapo 4) est gardée : c'est la question du premier bloc qui
    enseigne (rappel de l'ion), posée après sa dernière diapo, comme le veut la règle 53.
- **Questions de bloc à leur place.**
  - L'exercice « palier atteint vers 30 min à 20 °C, 10 min à 40 °C » (bloc `tl_s2_b3`) portait sur les courbes de
    `tl_f4_courbes` (bloc suivant) : déplacé au bloc `tl_s3_b1`.
  - Le bloc `tl_s3_b1` avait en double le retrouver et l'exercice du bloc `tl_s3_b1b` ; l'exercice « on double l'eau
    oxygénée : palier ? » demande x_max, enseigné en `tl_rp5_avancement` (bloc `tl_s3_b1b`) : il ne reste qu'au bloc
    `tl_s3_b1b`, et le retrouver « effet de la concentration et de l'état final » ne reste qu'au bloc `tl_s3_b1`
    (enseigné en `tl_f5_concentre`, « même brun final »). Défaut 14 (fort) corrigé.
- **Dit = écrit.** Cartes `centre` posées sur les mots déjà dits : `C = n/V` à la relecture de `tl_rp4_concentration` ;
  dans `tl_rp5_avancement` (aucune figure) les données V = 100 mL et n(H₂O₂)₀ = 2 mmol, les tables et les chaises, la
  définition du réactif limitant, et un pointage sur n(I₂)_f = x_max ; dans `tl_r7_titrage` l'équivalence et « une
  réaction de titrage doit être rapide ». Formules dites non écrites : 6 → 2 ; passages ≥ 60 mots sans geste : 2 → 0.
- **Écran.** États physiques ajoutés aux équations écrites de l'exercice national pas à pas (10 champs : `attendu`,
  `student_trace`, lignes de démonstration). Ligne « transfert d'électrons … d'un autre couple » retirée de la diapo 6
  (le mot couple y venait avant sa définition) et redite à l'écran de `tl_x7_equation` ; à l'écran aussi : la lecture
  de droite à gauche (Red → Ox + n e⁻, `tl_x7_equation`), « l'oxydation forme l'oxydant du couple ; la réduction forme
  le réducteur » (`tl_x3_couple`), la flamme du gaz en exemple de transformation rapide (`tl_r5_echelle`).

Défauts « dits sans être écrits » laissés : les deux phrases de `tl_n2_enonce` (diapo 53) sont la lecture de
l'énoncé du national 2017 R, affiché par la page d'examen elle-même : faux positif.

## Phase 2 — copie d'attente (`backend/data/courses/en_attente/phys_ch9_transformations_lentes_rapides.json`)

Copie refaite depuis le cours servi après la phase 1 (l'ancienne copie d'attente est remplacée). 57 → 60 diapos.

### Ordre des notions (règle 52) — défauts de `ordre-des-notions/` traités

| # | Gravité | Ce qui a été fait |
|---|---|---|
| 1 | forte | Question de la diapo 2 retirée (phase 1) ; la carte s'ouvre maintenant sur la flamme et le portail (cours du prof). |
| 2 | moyenne | `tl_rp2_conservation` : (s), (aq), (l), (g) dits en mots (la voix ne lit pas « aq ») et écrits sur une carte. |
| 3 | moyenne | Ligne « d'un autre couple » retirée de la diapo 6, redite à l'équation (cours servi). |
| 4 | moyenne | Diapo 8 coupée en deux : `tl_x3b_couple` (le couple, Cu²⁺/Cu, Zn²⁺/Zn, qui est oxydé) et **nouvelle** `tl_x3c_demi` (la demi-équation, Cu²⁺, Zn²⁺, H⁺/H₂, les deux sens), vue `transfert.html?vue=couple&depart=exemples`. I₂/I⁻ gardé pour sa diapo. |
| 5 | forte | Demi-équations du plus simple au plus long : `tl_x6b_diiode` (les quatre gestes énoncés, puis I₂/I⁻), `tl_x5b_acide`, `tl_x6_eau` (O avec H₂O, H avec H⁺, expliqués ici la première fois), `tl_x4_oxygene` + `tl_x5_charges` (MnO₄⁻). Cahier du bloc remis dans le même ordre. |
| 6 | moyenne | **Nouvelle** `tl_x5b_acide` « Rappel : le milieu acide » (H⁺ = H₃O⁺, on dispose de H₂O et H⁺) avant le premier couple qui en a besoin. Aucune vue de simulation ne convenait (`rappels.html` n'a que ion, conservation, mole, concentration) : `visual.kind: none` + 4 cartes. |
| 7 | moyenne | `tl_x10_verifier` (H₂O₂ + I⁻) placée avant `tl_x8_fer`, qui s'y réfère ; Fe³⁺/Fe²⁺ présenté avec sa demi-équation. |
| 8 | moyenne | `tl_x9_oxalique` : couple CO₂/H₂C₂O₄ construit par les quatre gestes, puis lu dans l'autre sens. |
| 9 | moyenne | `tl_r2_rapide` : thiosulfate et acide-base retirés ; un seul autre exemple, AgCl, avec le mot « précipité » expliqué. |
| 10 | moyenne | `tl_r4_indices` : « deux rôles du thiosulfate » retiré (voix, carte, écran). |
| 11 | moyenne | **Nouvelle** `tl_r7a_titrage` « Rappel : le titrage et l'équivalence » avant `tl_r7_titrage`, vue `bechers.html?vue=comparer` (burette, goutte à goutte). |
| 12 | moyenne | `tl_rp4_concentration` : [I⁻] et l'indice 0 dits et écrits. |
| 13 | moyenne | `tl_f1_facteur` : la voix servie ne nommait déjà que la température ; ajouté « la vitesse, c'est la rapidité : plus rapide = durée plus courte » (carte). |
| 14 | forte | Phase 1. |
| 15 | moyenne | `tl_rp5_avancement` déplacée juste après la concentration (avant les courbes et le palier de 2 mmol) ; lignes de cahier déplacées au bloc `tl_s1_b4`, numéros de la partie IV refaits. |
| 16 | moyenne | Le tableau d'avancement (état initial / en cours / état final) dit et écrit dans `tl_rp5_avancement` (carte, pas de dessin de tableau). |
| 17 | moyenne | `tl_n2_glacee` : « les données de masse et le dosage ne servent pas ici ; on regarde l'eau glacée ». |

Défauts vérifiés faux ou déjà corrigés : 13 (la voix servie ne nomme déjà que la température).

### Notions importantes (règle 55) et tuteur humain (règle 56)

- 26 annonces avant les notions clés, **26 phrases toutes différentes** (15 motifs différents au sens du script, qui
  compte le motif trouvé et non la phrase) ; deuxième façon de dire ajoutée aux 11 diapos clés qui n'en avaient pas ;
  rappels plus loin : demi-équation lue dans les deux sens (`tl_x7_equation`), demi-équations déjà vues
  (`tl_x10_verifier`, `tl_x8_fer`), milieu acide (`tl_x4_oxygene`), transformation rapide (`tl_r3_lente`), facteur
  cinétique (`tl_t3_catalyseur`, `tl_t1_trempe`), équivalence (`tl_r7_titrage`), réactif limitant (`tl_f7_palier`).
- Débuts de voix : « دابا » 19 % → premier mot le plus fréquent « هاد » 8 % ; 0 diapo qui suit avec le même premier mot.
- Exercice pas à pas : « خود الوقت ديالك، ومن بعد جاوب. » recopié 9 fois → 8 phrases différentes.
- Réactions : 26 réactions reformulées au début (« لا، هادي ماشي هي » ×11, « مزيان، الجواب ديالك صحيح » ×6,
  « الجواب الصحيح: » ×6 remplacés par des débuts variés de la banque) ; « السخانة » → « الحرارة » (4 réactions).
- Touches humaines : le métal qui apparaît (`tl_x1_zinc`), « je sais que ce couple paraît long » (`tl_x4_oxygene`),
  « c'est un peu étrange » (`tl_r1_bechers`), « prends ton temps » (`tl_r6_classer`), « bien, tu avances » (`tl_np5_limitant`),
  « c'est normal d'hésiter » (`tl_f8_variable`).

## Cours de référence du prof (`reference-prof/phys_ch9_transformations_lentes_rapides.md`)

| Correction recommandée | Fait | Où |
|---|---|---|
| 1. Porte d'entrée : flamme de gaz (rapide) et portail qui rouille (lent), deux oxydoréductions | Appliqué | Voix et 3 cartes au début de `tl_o1_carte` (copie d'attente) ; la question du national est déjà rangée (phase 1). |
| 2. Demi-équations I₂/I⁻ → H₂O₂ → MnO₄⁻ | Appliqué | Défaut 5 ci-dessus. |
| 3. Le réducteur se lit de droite à gauche, Red → Ox + n e⁻ | Appliqué | Écran (cours servi) et voix + carte (copie d'attente) de `tl_x7_equation`. |
| 4. Oxydation = formation de l'oxydant ; réduction = formation du réducteur | Appliqué | Écran de `tl_x3_couple` (servi) ; voix + carte dans `tl_x3c_demi` (attente). |
| 5. Ligne « d'un autre couple » retirée de la diapo 6 | Appliqué | Cours servi. |
| 6. Flamme du gaz en exemple rapide, à côté de la rouille | Appliqué | Écran (servi) et voix (attente) de `tl_r5_echelle`. |
| 7. Ne nommer que la température en 28 | Déjà fait | La voix servie ne nommait déjà que la température. |
| 8. La trempe utilise les deux facteurs (froid, eau ajoutée) | Appliqué | Voix + carte de `tl_t1_trempe` (attente). |
| 9. « Autres facteurs : la lumière, le solvant » | Laissé | Hors du cadre de référence de ce chapitre (consigne : rien hors du cadre) ; le national ne les demande pas. |

## Pistes à générer

`docs/audit-pedagogie/voix_a_generer/phys_ch9_transformations_lentes_rapides.json` : **71 pistes** — 42 diapos au
texte changé, 3 diapos nouvelles (`tl_x3c_demi`, `tl_x5b_acide`, `tl_r7a_titrage`), 26 réactions. Leur `audio` est
retiré dans la copie d'attente.

## Mesures (`audit_pedagogie.py`)

| | Diapos | Questions 6 premières | Formules non écrites | ≥ 60 mots sans geste | Clés | redites | annoncées (motifs ≠) | Premier mot | Suites |
|---|---|---|---|---|---|---|---|---|---|
| Avant (servi, 26/11) | 57 | 2 | 6 | 2 | 25 | 12 | 0 (0) | « دابا » 19 % | 3 |
| Après phase 1 (servi) | 57 | 0 | 2 | 0 | 26 | 12 | 0 (0) | « دابا » 19 % | 3 |
| Copie d'attente | 60 | 0 | 2 | 0 | 28 | 26 (93 %) | 26 (15), 26 phrases ≠ | « هاد » 8 % | 0 |

Vérifications sur les deux fichiers : `verifier_formules` 0, `verifier_parcours` rien, `verifier_figures_cahier`
0 erreur, `nombres_fr` 0 texte. `verifier_pointage` : 3 repères (`donnees`, `tableau`, `copie`) de
`national-pas-a-pas.html` déjà signalés avant ces corrections (construits par `pas-a-pas.js`). `verifier_pointage_simulations` :
5 écarts GESTE déjà présents au cours servi ; sur la copie d'attente, tous les écarts sont des GESTE dus aux pistes
sans voix (durée 0), à revoir quand la voix existera.

## Mots douteux pour la voix (`verifier_mots.py`, corpus < 3)

Nouveaux dans les textes écrits ici : flamme, portail, crochets, titrer, entièrement ; darija : اتجاهات, كنزيدوها,
تبعني / وتبعني (banque), كيتسال, غريبة, وقتك, فوقو, كنقيسو, عييتي (banque), تحير, كيقرر, كنتسناك, راحتك, كيخدموناش,
نصححوها, ضاعش (banque), كنغلطو, الطبالي (déjà là). Les termes de chimie (diiode, iodure, permanganate, thiosulfate,
entités…) étaient déjà signalés avant : termes du programme gardés. À écouter avant de publier.
