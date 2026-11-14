# Audit « rythme et départ de zéro » — SVT (14 novembre 2026)

Règles appliquées : skill `professeur` 27, 28, 30, 32, **33** (une chose à la fois) et **34** (départ de zéro, deux explications) ; skill `cours-concentration` ; skill `voix-du-cours`. Consignes : `docs/audit-rythme/BRIEF.md`.

Les cours en ligne (`backend/data/courses/<deck>.json`) **ne sont pas touchés**. Les nouvelles versions complètes sont dans `backend/data/courses/en_attente/` :

| Cours | Copie en attente | Diapos (en ligne → en attente) | Pistes de diapo à voixer | Nouvelles questions | Observations ajoutées |
|---|---|---|---|---|---|
| ch1 Libération de l’énergie | `svt_ch1_reactions_responsables_liberation_energie.json` | 43 → 46 | 4 | 3 (15 réactions) | 0 (1 existait déjà) |
| ch2 Muscle strié squelettique | `svt_ch2_role_muscle_strie_squelettique.json` | 53 → 54 | 5 | 1 (5 réactions) | 0 (1 existait déjà) |
| ch3 Information génétique | `svt_ch3_notion_information_genetique.json` | 47 → 55 | 13 | 3 (15 réactions) | 2 (Griffith souris 4, Avery souris 3) |
| ch4 Relation gène – protéine | `svt_ch4_relation_gene_proteine.json` | 47 → 51 | 6 | 2 (10 réactions) | 1 (marquage aux acides aminés) |

Légende des constats : **⏩ trop vite** (plusieurs expériences, résultats ou idées d’un coup) · **🎯 résultat donné** (le résultat décisif est dit au lieu d’être trouvé) · **📚 prérequis supposé** · **1️⃣ une seule explication**.

---

## 1. SVT ch3 — Notion de l’information génétique (cas prioritaire)

### 1.1 Ce qui a été fait

**Départ de zéro (règle 34).** Le cours ouvrait sur « un rappel du tronc commun » qui nommait cellule, noyau et 46 chromosomes comme connus, puis utilisait mitose, chromosome, ADN, réplication et phase S avant de les enseigner.

| Diapo | Constat | Fait |
|---|---|---|
| `ig_o2_rappel` | 📚 « Vérifions deux acquis du tronc commun » : cellule et 46 chromosomes dits en deux phrases ; 1️⃣ | **Réécrite** : « La cellule : le point de départ ». Un tissu peint (le corps = des milliards de cellules), une cellule en grand, sa membrane, son cytoplasme, son noyau, figés un par un ; puis **autrement** : une maison (murs = membrane, intérieur = cytoplasme, le chef qui commande = noyau). Simulation nouvelle `bases.html?vue=cellule`. Les chromosomes sont sortis de cette diapo. |
| `ig_p1_chromosomes` (nouvelle) | 📚 chromosomes, paires, ADN utilisés sans être enseignés (`ig_n1` disait « la chromatine : l’ADN محلول ») | Dans le noyau : 46 chromosomes = 23 paires, un de la mère et un du père ; un chromosome déroulé = un long fil, l’ADN, où l’information est écrite ; **autrement** : 46 livres rangés par paires. `bases.html?vue=chromosomes`. Placée juste avant la partie « noyau », là où ces notions servent. |
| `ig_p2_mitose` (nouvelle) | 📚 la mitose citée dès `ig_n1` (« ملي الخلية ماشي ف la mitose »), enseignée seulement à `ig_m1` | La mitose comme idée simple : une cellule (4 chromosomes dessinés au lieu de 46), chaque chromosome copié, les copies partagées, deux cellules filles identiques — trois arrêts sur image. `bases.html?vue=mitose`. |
| `ig_p3_mitose_corps` (nouvelle) | 1️⃣ | La même idée **autrement** : la cellule-œuf → 2 → 4 → 8 → des milliards, toutes avec les mêmes 46 chromosomes ; et l’image du livre copié avant d’être donné à deux enfants. Question « À toi » du bloc : « Après une mitose, une cellule à 46 chromosomes donne… ». `bases.html?vue=oeuf`. |
| `ig_n1_noyau` | 📚 « des protéines, les histones » sans image | Une demi-phrase ajoutée : les histones, « بحال بكرات صغار، كيلف عليهم l’ADN بحال الخيط ». Voix à réenregistrer. |
| `ig_n3_chromatides` | 📚 « la réplication en phase S » alors que le cycle cellulaire vient après | La phrase dit maintenant : avant la mitose, la cellule copie son ADN, c’est la réplication, « غادي نشوفوها مزيان من بعد ». « Phase S » retiré de la voix, des puces, de la trace et du cahier de la diapo. |

**Griffith pas à pas (règle 33) — la demande de l’utilisateur.** Avant : une seule diapo de 33 s, quatre injections et quatre résultats enchaînés, puis le résultat décisif (souris 4 morte, S vivants dans le sang) et la conclusion, sans pause ni question. Après : **cinq diapos**.

| Diapo | Contenu | Animation (`bacteries.html`, vues nouvelles) |
|---|---|---|
| `ig_t1_griffith` (réécrite) | **Le principe seul** : les pneumocoques, forme S (capsule = « غطا » autour, virulente, tue la souris), forme R (sans capsule, non virulente) ; ce qu’on fait (injecter, attendre quelques jours) et ce qu’on regarde (la souris vit ou meurt ?) ; redit autrement (« S عندها الغطا، وخطيرة… »). **Question de vérification** (« À toi » du bloc) : « Ce qui distingue S de R… ». | `?vue=griffith_principe` : S peints avec capsule, R sans, une seringue et une souris, « puis on regarde : la souris vit ou meurt ? ». Aucun résultat. |
| `ig_t1b_exp1` (nouvelle) | Expérience 1 seule : S vivants, injection, attente, **résultat : la souris meurt**, « خلي هاد النتيجة ف بالك ». | `?vue=griffith_1` : la scène en grand, figée à chaque étape (bactéries → injection → horloge « on attend quelques jours » → souris morte) ; à droite « Déjà vu » (vide). |
| `ig_t1c_exp2` (nouvelle) | Expérience 2 seule : R vivants → la souris vit ; comparaison avec la 1 sur le récapitulatif. | `?vue=griffith_2` ; « Déjà vu » : 1. |
| `ig_t1d_exp3` (nouvelle) | Expérience 3 seule : on chauffe les S (ils deviennent gris), on injecte → la souris vit ; puis l’élève relit le tableau des trois résultats. | `?vue=griffith_3` : flammes, S qui grisent, puis l’injection ; « Déjà vu » : 1, 2. |
| `ig_t1e_exp4` (nouvelle) | Expérience 4 : on mélange R vivants + S tués (rappel : seuls, aucun ne tue), on injecte, on attend… **la voix s’arrête** : question d’observation (règle 30). Énoncé : « R vivants + S tués : que devient la souris 4, et que trouve-t-on dans son sang ? » ; silence 10 s, deux indices (le tableau « Déjà vu » ; « seuls les S vivants tuent »), puis trois cartes ; micro de réponse. **Après la réponse seulement** : la souris meurt, la loupe sur son sang montre des S vivants, « on n’a injecté aucun S vivant ! » → des R ont été transformés en S : le principe transformant. | `?vue=griffith_4&conclusions=false` + `sim_avant {conclusions:false}` : la souris reste sous un « ? », ni résultat, ni sang, ni principe écrits, ni bulle qui trahit ; `sim_apres {conclusions:true}` puis la voix rejoue la suite (`g4_resultat`, `g4_sang`, `g4_principe`). |

**Avery (même défaut).** Avant : une diapo qui posait les trois tubes et donnait d’un coup les trois résultats, dont le décisif. 🎯 ⏩

| Diapo | Fait |
|---|---|
| `ig_t2_avery` (réécrite) | Le principe seul : la question d’Avery (protéine, ARN ou ADN ?), l’extrait de S tués partagé en trois tubes, chaque enzyme dite avec ce qu’elle détruit, un tube par arrêt, redit autrement (« كل tube، خاصو نوع واحد ») ; les R ajoutés et l’injection. 📚 l’ARN (pas encore vu) est présenté d’une phrase, « غادي نشوفوه ف le chapitre الجاي ». Animation `avery&resultats=0` : aucune souris ne montre son sort. |
| `ig_t2b_avery_resultats` (nouvelle) | Les résultats **souris par souris** (`set_parameters {resultats: 1}`, puis `2`) ; la souris 3 (désoxyribonucléase) est **trouvée par l’élève** : question d’observation « Tube 3 : l’ADN a été détruit. Que devient la souris 3 ? », indices, cartes ; puis « la souris بقات عايشة ! » et la conclusion : le principe transformant est l’ADN. |
| `ig_t3_support` | Voix inchangée (piste gardée). Une question « À toi » ajoutée pour le bloc : « Le support de l’information génétique est… ». |

**Blocs et séances.** Une seule question « À toi » par bloc (vérifié). Nouveaux blocs : « Les chromosomes et la mitose, depuis zéro » (p1–p3), « Griffith pas à pas : le principe, puis trois expériences » (t1–t1d, la question sur la diapo du principe, comme le veut la règle 33), « La souris 4, Avery » (t1e, t2, t2b, t3). Le bloc nucléotide/Chargaff/hélice a été recoupé en deux. Séances refaites (6) pour que Griffith 1 → 4 et Avery tiennent dans **la même séance**. Chaque nouveau bloc a ses lignes de cahier, son `retrouver` et son exercice (avec réactions).

### 1.2 Audit diapo par diapo (ce qui reste, sans modification)

| Diapo | Constat | Décision |
|---|---|---|
| `ig_o1_ressemblance` | Annonce les quatre questions du chapitre ; image fixe. | Rien. |
| `ig_l1_amibe` | Deux fragments et leurs deux devenirs dans une diapo, mais figés un par un ; « la mérotomie » dite une fois. | Gardée (la question porte dessus). |
| `ig_l2`–`ig_l5` | ⏩ `ig_l3_section` : trois fragments et leurs trois devenirs d’affilée ; 🎯 `ig_l4_greffe` : le chapeau qui repousse est **dit** (c’est le résultat décisif de l’acétabulaire). | **À faire plus tard** : `ig_l4_greffe` est le meilleur candidat d’une 3ᵉ question d’observation (la règle 30 en limite le nombre à deux par cours ; Griffith et Avery ont été jugés prioritaires). `noyau.html` devrait alors accepter `conclusions:false`. |
| `ig_n2_condensation` | Bien : une idée, et l’image « même fil, déroulé ou enroulé ». | Rien. |
| `ig_c1_cycle` | ⏩ G1, S, G2, interphase et mitose dans une seule diapo (gelées une à une, mais cinq idées nouvelles). | **À faire** : couper en deux (interphase G1-S-G2, puis le cycle complet). Non fait ici pour ne pas réenregistrer une partie bien rythmée. |
| `ig_c2`–`ig_c6` | `ig_c2` donne la seconde explication (le livre copié) — bien. `ig_c5`/`ig_c6` : méthode d’examen, valeurs nombreuses mais lues une par une. | Rien. |
| `ig_m1`–`ig_m7` | Une phase par diapo : bon rythme. La mitose est maintenant préparée par `ig_p2`/`ig_p3`. | Rien. |
| `ig_s1`–`ig_s5` | Une notion par diapo ; Chargaff : 🎯 le rapport A/T est calculé par la voix (une observation serait possible, mais limite de deux). | Rien. |
| `ig_r1`–`ig_r12` | Meselson-Stahl déjà une génération par diapo ; 🎯 la bande hybride de la génération 1 (qui élimine la conservative) est dite. | **À faire plus tard** : en faire la question d’observation si l’on en autorise une troisième. |
| `ig_x1`, `ig_x2`, bilan, carte | Méthode et bilan. | Rien. |

---

## 2. SVT ch1 — Libération de l’énergie emmagasinée dans la matière organique

### 2.1 Ce qui a été fait

| Diapo | Constat | Fait |
|---|---|---|
| `le_p1_cellule` (nouvelle) | 📚 la cellule, le hyaloplasme et la mitochondrie employés dès `le_e4_carte` et `le_g1_ou` sans être présentés (la mitochondrie n’est étudiée qu’en `le_m2`) | Une cellule peinte : membrane, hyaloplasme (« le liquide intérieur »), noyau, mitochondries (« leur rôle : plus loin », pour ne pas donner le résultat de `le_m1`) ; **autrement** : une petite ville (le noyau = le chef, les rues = hyaloplasme, de petites usines = mitochondries). Simulation nouvelle `depart.html?vue=cellule`. |
| `le_p2_glucose` (nouvelle) | 📚 glucose, molécule, énergie chimique, liaisons : supposés connus dès `le_o1` et `le_a1` | Du pain (amidon) au glucose du sang ; la molécule C₆H₁₂O₆, six carbones ; l’énergie rangée dans les liaisons (énergie chimique) ; liaisons cassées → énergie libérée ; **autrement** : le bois qui brûle d’un coup, la cellule qui avance pas à pas. Question « À toi » : « L’énergie du glucose se trouve… ». `depart.html?vue=glucose`. |
| `le_c10_vesicules` | ⏩ trois expériences (pH égaux, intérieur acide, sans sphères) et la conclusion dans une diapo | **Coupée** : `le_c10_vesicules` = le principe (fabriquer les vésicules, changer le pH dedans/dehors) + le cas 1 seul ; `le_c10b_vesicules_cas` (nouvelle) = cas 2, puis cas 3, puis la conclusion et la question existante. |
| `le_c9_poison` | Bloc c7–c10 trop long avec une seule question en fin | Voix inchangée ; question ajoutée (« le cyanure bloque T4 : la consommation de dioxygène… ») pour le bloc c7–c9. |

### 2.2 Audit diapo par diapo (le reste)

| Diapo | Constat | Décision |
|---|---|---|
| `le_o1`, `le_o2_acquis` | `le_o2` : photosynthèse et amidon « déjà vus » (rappel d’un an antérieur, en une phrase) | Gardées ; le glucose est maintenant enseigné avant (`le_p2`). |
| `le_a1_monnaie`, `le_a2_recharge` | L’ATP est expliqué deux fois (hydrolyse + « petite monnaie » ; recharge + « carte vide ») — conforme à la règle 34. 📚 « mole », « kJ » cités sans être expliqués. | Gardées ; à surveiller à l’écoute. |
| `le_e1`–`le_e3` | `le_e3` a déjà sa question d’observation (l’éthanol). | Rien. |
| `le_e4_carte`, `le_t1`, `le_t2` | ⏩ `le_t2_reduit` : réduction, oxydation, NAD⁺ et FAD dans la même diapo. | **À faire** : séparer FAD → FADH₂ (il ne sert qu’au cycle de Krebs) ; non fait. |
| `le_g1`–`le_g3` | Une étape par arrêt (2 ATP dépensés, coupure, taxis, 4 ATP). | Rien. |
| `le_m1`–`le_m4` | 🎯 `le_m3_isolees` : « glucose : rien ; acide pyruvique : le dioxygène baisse » est dit. La baisse simulée est faible (100 → 96 %), pas assez visible pour une question d’observation. | **À faire** : accentuer la baisse dans `exao.html?vue=mitochondries` (nouveau paramètre), puis observation. |
| `le_k1`–`le_k5` | ⏩ `le_k4_sorties` : cinq sorties d’un tour, mais au compteur, une par arrêt ; `le_k5` : bilan « fois deux » chiffré. | Rien (lecture comptée). |
| `le_c1`–`le_c8` | `le_c6_protons` explique l’expérience de `le_c1` (bien : décrire avant d’expliquer). | Rien. |
| `le_f1`, `le_f2`, `le_r1`–`le_r3` | ⏩ `le_r1_compteur` : toute la caisse des ATP d’un trait (2 + 2 + 30 + 4). | **À faire** : un arrêt par ligne dans `compteur.html` (moments par étape). |
| `le_x1`–`le_x4`, bilan, carte | Méthode et synthèse. | Rien. |

---

## 3. SVT ch2 — Rôle du muscle strié squelettique

### 3.1 Ce qui a été fait

| Diapo | Constat | Fait |
|---|---|---|
| `ms_o2_atp` | 📚 1️⃣ l’ATP rappelé en trois phrases, sans animation (image vide) | **Réécrite** avec l’animation `reactions_responsables_liberation_energie-tableau/atp.html` (adénosine, trois phosphates, liaison rompue, énergie, ADP + Pi, recharge), un arrêt par étape ; **autrement** : le glucose = un gros billet, l’ATP = la petite monnaie avec laquelle la cellule paie. |
| `ms_c1_exigences` | ⏩ 🎯 principe de la fibre glycérinée + quatre essais + conclusion dans une diapo ; la page lançait seule l’essai « Ca²⁺ + ATP » (le résultat sous les yeux avant d’être dit) | **Coupée** : `ms_c1_exigences` = le principe seul (fibre vidée de ses réserves, levier, ce qu’on ajoute, ce qu’on regarde ; redit autrement) ; `ms_c1b_essais` (nouvelle) = un essai par arrêt, puis le tableau, la conclusion et une question « À toi ». `exigences.html?attente=1` : la page attend le tuteur (paramètre nouveau, sans effet sans lui). |
| `ms_c2_calcium` | 📚 « le réticulum sarcoplasmique » jamais défini | Défini dans la voix : « واحد الشبكة ديال الشكاير الصغار داخل la fibre، فيها le calcium مخبي ». |
| `ms_t4_consomme` | 📚 « glycogène » et « phosphocréatine » utilisés avant d’être définis (la phosphocréatine n’est enseignée qu’en `ms_r2`) ; ⏩ six valeurs dans une diapo | Définis d’une phrase chacun (« le glucose mis en réserve dans le muscle » ; « une molécule du muscle qui porte un phosphate, son rôle plus loin »). Le découpage ligne par ligne reste à faire (voir 3.2). |
| `ms_t1_chaleur_initiale`, `ms_u6_legender` | Défaut trouvé à la vérification : un `mot` du pointage absent de la voix (ancienne question retirée le 13 novembre) | Repère obsolète retiré ; voix inchangée. Le même défaut est dans la copie en ligne. |

### 3.2 Audit diapo par diapo (le reste)

| Diapo | Constat | Décision |
|---|---|---|
| `ms_o1`, `ms_s1`–`ms_s6` | Une idée par diapo (montage, une secousse, latence, phases, mesures, définition construite en trois questions). | Rien. |
| `ms_i1`, `ms_i2` | Bien rythmé ; l’image du « 9,99 / 10 au bac » est une 2ᵉ explication du seuil. | Rien. |
| `ms_f1`–`ms_f7` | Une fréquence par diapo ; `ms_f3` ajoute « et si on rapproche encore » (3ᵉ cas dans la même diapo). | Acceptable (variante dite). |
| `ms_t1`–`ms_t3` | `ms_t3_sans_dioxygene` porte déjà la question d’observation de référence. | Rien. |
| `ms_t4_consomme` | ⏩ six lignes de tableau d’un coup. | **À faire** : un paramètre `lignes` dans `consommation.html` pour révéler les lignes une à une. |
| `ms_u1`–`ms_u7`, `ms_g1`–`ms_g3` | Une échelle par diapo ; le glissement redit avec les deux peignes. | Rien. |
| `ms_c3`–`ms_c8` | Une étape du cycle par diapo. | Rien. |
| `ms_r1`–`ms_r8` | ⏩ 🎯 `ms_r8_inhibiteurs` : trois muscles et leurs résultats d’un coup. | **À faire** : une diapo par muscle, ou une question d’observation (le cours en a une seule). |
| `ms_x1`–`ms_x4`, bilan, carte | Méthode. | Rien. |

La séance 4 compte maintenant 4 blocs (le bloc des exigences est devenu deux blocs) : à rééquilibrer si l’on veut des séances de 3 blocs strictes.

---

## 4. SVT ch4 — Relation gène – protéine

### 4.1 Ce qui a été fait

| Diapo | Constat | Fait |
|---|---|---|
| `rg_d1_adn` (nouvelle) | 📚 l’ADN, ses brins et ses bases supposés retenus du chapitre précédent ; `rg_g1` dit « comme au chapitre précédent » | Rappel animé : un chromosome déroulé en fil d’ADN, deux brins, les bases A T C G, A en face de T et C en face de G, un arrêt par étape ; **autrement** : une fermeture éclair. Simulation nouvelle `rappels.html?vue=adn`. |
| `rg_d2_proteine` (nouvelle) | 📚 « protéine » nommée dès `rg_o1` alors qu’elle n’est définie qu’en `rg_p3` | Des perles (acides aminés, 20 sortes) enfilées en chaîne ; l’ordre fait la protéine ; **autrement** : des lettres (CHAT / TACH) ; la chaîne se replie : une forme, donc un rôle. Question « À toi » sur l’ordre. `rappels.html?vue=proteine`. |
| `rg_g2_allele` | Bloc gène/allèle sans question | Voix inchangée ; question « À toi » ajoutée (« A et O sont… »). |
| `rg_g3_mutation` | ⏩ 🎯 l’expérience, sa conclusion (« elles étaient déjà là ») et la définition de la mutation dans une diapo | **Coupée** : `rg_g3_mutation` = l’expérience seule, l’élève prend le temps de regarder et répond à la question existante (« étaient-elles là avant ? ») — la voix ne donne plus la réponse ; `rg_g3b_mutation` (nouvelle) = la réponse, le nucléotide changé, la définition relue, **autrement** : une lettre qui change dans un mot. |
| `rg_a4_acides_amines` | 🎯 « où sont les grains ? » posé puis répondu dans la même phrase ; la page écrivait la réponse | Voix inchangée (piste gardée). **Question d’observation** après « فين كيبانو النقط الكحلين؟ » : l’élève regarde les grains, indices (noyau / ribosomes), cartes. `marquage.html` accepte `conclusions:false` (n’écrit ni « grains sur les ribosomes » ni « synthèse des protéines » ni la conclusion, ni la bulle) ; défaut inchangé. |
| `rg_m2_substitution` | ⏩ deux mutations (silencieuse, faux-sens) dans une diapo | **Coupée** : `rg_m2_substitution` = la substitution et le cas silencieux, redit autrement (deux mots qui veulent dire la même chose) ; `rg_m2b_faux_sens` (nouvelle) = le cas faux-sens, redit autrement. |

### 4.2 Audit diapo par diapo (le reste)

| Diapo | Constat | Décision |
|---|---|---|
| `rg_o1_caracteres` | Image fixe qui montre tout le chemin (ADN → ARNm → protéine) dès l’ouverture, termes non expliqués. | Gardée comme annonce ; « protéine » et « ADN » sont maintenant enseignés juste avant. |
| `rg_g1_gene` | Bonne définition relue. | Rien. |
| `rg_p1`–`rg_p4` | Une échelle par diapo (organisme, cellule, molécule) ; `rg_p3` redit la protéine (collier de perles) — c’est maintenant sa 3ᵉ explication. | Rien. |
| `rg_a1`–`rg_a3` | ⏩ `rg_a1_arn` : tableau ADN/ARN en une fois (brins, sucre, bases, trois ARN) ; `rg_a3_uracile` : 5, 15 et 30 min d’affilée mais figés un par un. | **À faire** : `rg_a1` en animation (règle 28) plutôt qu’un tableau. |
| `rg_t1`–`rg_t6` | Rythme correct ; `rg_t5_non_transcrit` dense (deux chemins + piège). | Rien. |
| `rg_c1`–`rg_c5` | `rg_c5_proprietes` : trois propriétés d’un coup. | **À faire** : une propriété par arrêt. |
| `rg_r1`–`rg_r5` | Une étape de traduction par diapo. | Rien. |
| `rg_m1`, `rg_m3`–`rg_m6` | Une mutation par diapo après le découpage. | Rien. |
| `rg_s1`–`rg_s5`, `rg_e1`–`rg_e6`, bilan, carte | Méthode et synthèse ; `rg_e5_national` : un sujet entier en une diapo (assumé : c’est la démonstration finale). | Rien. |

---

## 5. Simulations créées ou étendues

| Fichier | Nature | Comportement par défaut |
|---|---|---|
| `svt/notion_information_genetique-tableau/bases.html` | **Nouveau.** Vues `cellule`, `chromosomes`, `mitose`, `oeuf` ; vivant peint (cellules, noyau, chromosomes, une maison, une bibliothèque) ; moments `c_*`, `k_*`, `m_*`, `o_*` ; attendent le tuteur. | — |
| `svt/notion_information_genetique-tableau/bacteries.html` | **Étendu.** Vues `griffith_principe`, `griffith_1` … `griffith_4` (une expérience en grand + récapitulatif « Déjà vu »), paramètre `conclusions` (vue 4, aussi `?conclusions=false`), paramètre `resultats` 0–3 (vue avery, aussi `?resultats=`), moment `av_injection` ajouté à avery. | Vues `griffith` et `avery` inchangées (`resultats` = 3, `conclusions` = true). |
| `svt/notion_information_genetique-tableau/etapes.js` | Option de vue `autoDepart: false` (la page attend le premier geste du tuteur) ; crochets facultatifs `auDepart(P)` et `auReglage(P, cles)`. | Inchangé pour les pages qui ne les déclarent pas. |
| `svt/reactions_responsables_liberation_energie-tableau/depart.html` | **Nouveau.** Vues `cellule` (membrane, hyaloplasme, noyau, mitochondries peintes ; une petite ville) et `glucose` (pain, sang, molécule, liaisons, éclairs, bûche). Moteur `etapes.js` de la génétique. | — |
| `svt/relation_gene_proteine-tableau/rappels.html` | **Nouveau.** Vues `adn` (chromosome, fil, deux brins, bases face à face, fermeture éclair) et `proteine` (perles, chaîne, lettres, chaîne repliée). | — |
| `svt/relation_gene_proteine-tableau/marquage.html` | **Étendu.** Paramètre `conclusions` (vue acides_amines) : n’écrit pas où sont les grains. | Inchangé (true). |
| `svt/role_muscle_strie_squelettique-tableau/exigences.html` | **Étendu.** `?attente=1` : pas d’essai lancé tout seul au chargement. | Inchangé sans le paramètre. |

**Attention** : un serveur Vite déjà lancé ne voit pas les nouveaux fichiers de `public/` (il renvoie la page de l’application) : le redémarrer avant d’essayer les cours en attente.

---

## 6. Voix à enregistrer (voix Bodi, kernel d’essai)

### ch1 — `svt_ch1_reactions_responsables_liberation_energie`
- **Pistes de diapo (4)** : `le_p1_cellule`, `le_p2_glucose`, `le_c10_vesicules`, `le_c10b_vesicules_cas`.
- **Énoncés + réactions (3 questions, 15 réactions)** : `le_p2_glucose` (« L’énergie du glucose se trouve… » : juste + 2 × (indice, réponse)) ; `le_c9_poison` (« Le cyanure bloque T4… ») ; `le_c10b_vesicules_cas` (question existante, son énoncé est à revoixer car la voix de la diapo change ; ses réactions gardent leurs pistes).
- **Blocs** : `retrouver` et exercice du nouveau bloc `le_s1_b1` (non joués aujourd’hui, `ETAPES_FIN_DE_BLOC = ['cahier']`).

### ch2 — `svt_ch2_role_muscle_strie_squelettique`
- **Pistes de diapo (5)** : `ms_o2_atp`, `ms_t4_consomme`, `ms_c1_exigences`, `ms_c1b_essais`, `ms_c2_calcium`.
- **Énoncés + réactions (1 question, 5 réactions)** : `ms_c1b_essais` (« Une fibre glycérinée reçoit de l’ATP, mais pas d’ions Ca²⁺… »).

### ch3 — `svt_ch3_notion_information_genetique`
- **Pistes de diapo (13)** : `ig_o2_rappel`, `ig_p1_chromosomes`, `ig_p2_mitose`, `ig_p3_mitose_corps`, `ig_n1_noyau`, `ig_n3_chromatides`, `ig_t1_griffith`, `ig_t1b_exp1`, `ig_t1c_exp2`, `ig_t1d_exp3`, `ig_t1e_exp4`, `ig_t2_avery`, `ig_t2b_avery_resultats`.
- **Énoncés + réactions (3 questions, 15 réactions)** : `ig_p3_mitose_corps` (mitose : 46 chromosomes), `ig_t1_griffith` (S et R), `ig_t3_support` (le support : l’ADN).
- **Observations (2 × 7 pistes : énoncé, 2 indices, 3 retours, solution)** : `ig_t1e_exp4` (la souris 4 et son sang), `ig_t2b_avery_resultats` (la souris 3).
- `ig_n3_chromatides` garde sa question et la piste de son énoncé.

### ch4 — `svt_ch4_relation_gene_proteine`
- **Pistes de diapo (6)** : `rg_d1_adn`, `rg_d2_proteine`, `rg_g3_mutation`, `rg_g3b_mutation`, `rg_m2_substitution`, `rg_m2b_faux_sens`.
- **Énoncés + réactions (2 questions, 10 réactions)** : `rg_d2_proteine` (l’ordre des acides aminés), `rg_g2_allele` (A et O, deux allèles).
- **Observation (7 pistes)** : `rg_a4_acides_amines` (où sont les grains noirs ?).
- `rg_g3_mutation` garde sa question, ses réactions et la piste de son énoncé.

Total : **28 pistes de diapo**, **9 nouvelles questions** (9 énoncés, 45 réactions), **3 observations** (21 pistes).

---

## 7. Vérifications faites

- JSON des quatre copies valide, écrit en UTF-8 (`ensure_ascii=False`, `indent=2`, fins de ligne LF).
- Chaque `mot` du pointage est dans sa voix ; chaque `apres_mot` apparaît une seule fois ; aucun chiffre dans les voix réécrites ; une seule question « À toi » par bloc ; chaque diapo dans un bloc et une compétence, dans l’ordre du cours ; chaque option de chaque nouvelle question a ses réactions (juste, ou indice + réponse).
- Moments : lus **dans un navigateur sans écran** (Chromium via Playwright, `frontend/public` servi par `python -m http.server`) pour toutes les diapos nouvelles ou modifiées — tous les `play_until` (pointage et gestes) existent ; repères vérifiés dans le code des pages.
- `node --check` sur `bases.html`, `bacteries.html`, `etapes.js`, `depart.html`, `rappels.html`, `marquage.html`, `exigences.html` : OK. Captures prises : principe de Griffith, expériences 3 et 4 (avec et sans `conclusions`), Avery `resultats=1/2`, cellule, chromosomes, mitose, œuf, glucose, ADN, protéine, marquage `conclusions:false`.
- Voix : `verifier_texte_corpus.py` passé sur les diapos réécrites ; les mots darija les plus rares ont été remplacés par des mots du corpus. Restent, à **écouter** après génération (vus 0 à 2 fois) : « ماتت », « عايشة », « كتقتل », « بقاوش », « كيقتلو », « وبدلاتهم », « الخليط », « حلينا » (ch3) ; « كيتقطع », « كيشعل », « نعرفوه » (ch1) ; « كتخلص », « الشكاير », « طلعش » (ch2) ; « حليناه », « نكبروه », « كتطوى », « الجاكيطة », « صاوبهم » (ch4). Termes du programme gardés en français malgré leur rareté : pneumocoques, capsule, virulente, désoxyribonucléase, glycérinée, levier, streptomycine, redondance…

## 8. Ce qui n’a pas pu être vérifié

- La voix : aucune piste générée (pas de GPU Kaggle dans cette session) ; ni murmures ni transcription contrôlés.
- Le déroulé complet dans le lecteur (`CourseFocusStage`) : les copies en attente ne sont pas servies ; les cues 0,9 s avant le mot, l’enchaînement voix → question d’observation → reprise n’ont été vérifiés que par la structure des données et les pages seules.
- `preparer_reponses.py verifier` et `controler_cadre.py` : non lancés (ils demandent les pistes audio et la fiche du chapitre).
- Les réactions préparées ont été écrites à la main (pas par le prompt du tuteur sur le VPS) ; à relire par un professeur.
- Le comportement de `exigences.html?attente=1` dans le lecteur (premier essai lancé par le pointage) n’a pas été rejoué de bout en bout.
