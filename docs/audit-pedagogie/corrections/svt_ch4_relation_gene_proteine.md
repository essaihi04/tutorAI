# svt_ch4_relation_gene_proteine — corrections du 26-27/11/2026

Cours servi : `backend/data/courses/svt_ch4_relation_gene_proteine.json` (phase 1, aucun texte parlé changé).
Copie d'attente : `backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json` (phase 2, refaite depuis le cours servi après la phase 1).
Pistes à générer : `docs/audit-pedagogie/voix_a_generer/svt_ch4_relation_gene_proteine.json` (format de `scripts/voix/pistes_changees.py`).

## Mesures (`scripts/audit/audit_pedagogie.py`)

| | avant | servi (phase 1) | attente (phase 2) |
|---|---|---|---|
| Diapos | 70 | 70 | 73 |
| Questions dans les 6 premières | 2 | 1 | **0** |
| Formules dites non écrites | 1 | 0 | 0 |
| Passages ≥ 60 mots sans geste | 1 | 0 | 0 |
| Notions clés / redites | 30 / 9 | 30 / 9 | 33 / **33** (100 %) |
| Annoncées (phrases ≠ selon l'audit) | 0 (0) | 0 (0) | **33 (18)** |
| Premier mot le plus fréquent | « دابا » 13 % | 13 % | « قبل » 4 diapos (5 %) |
| Diapos qui suivent avec le même premier mot | 9 | 9 | **0** |
| Débuts de voix répétés | « ف le » ×7, « دابا غادي » ×4 | idem | — |
| Réactions au même début (≥ 4) | 3 motifs (11, 10, 6) | 3 | **0** |

Annonces : les 33 phrases d'annonce sont toutes différentes, mais l'audit ne reconnaît qu'une liste fermée de
21 tournures (`ATTENTION`) et compte la tournure trouvée, pas la phrase. Trois tournures françaises de cette liste
(« écoute bien », « sois attentif », « concentre-toi ») ont été remplacées par du darija car absentes du corpus de la
voix (risque de mauvaise prononciation) : il reste 18 tournures distinctes pour 33 annonces. Le compte « 18 » est
donc un plafond de la mesure, pas une répétition de phrase. (Ajouter les phrases de la banque §1 absentes de la
regex — « خلي كلشي على جنب », « بغيتك تكون معايا »… — à `audit_pedagogie.py` réglerait la mesure ; hors périmètre.)

## Phase 1 — cours servi (commit 437b3a8d)

- **Questions de bloc avant leur leçon / doublons** (vérifiés dans le JSON) :
  - `rg_s1_b1` « qu'est-ce qu'une protéine ? » (protéine enseignée en `rg_d2_proteine`) → `rg_s2_b1` (phase 2 : revient à `rg_s1_b1`, la diapo protéine y étant déplacée) ;
  - `rg_s2_b1` doublon exact de `rg_s2_b2` (niveau moléculaire pas encore vu) → retiré ;
  - exercice « brin transcrit → ARNm » de `rg_s3_b3` (règle en `rg_t3_bases`, sens en `rg_t4_sens`) → `rg_s4_b2`, dont le retrouver/exercice était un doublon exact de `rg_s4_b1` ;
  - `rg_s4_b3` codon d'initiation / codons stop (enseignés en `rg_c3_initiation_stop`) → retrouver vers `rg_s5_b2`, exercice AUG GCA UAG CCU vers `rg_s5_b3` ; `rg_s5_b2`/`rg_s5_b3` étaient doublons : `rg_s5_b2` garde l'exercice anticodon, `rg_s5_b3` le retrouver des trois étapes (terminaison vue en `rg_r4`). `rg_s4_b3` reste sans question.
- **Règle 53** : la question de `rg_g2_allele` (diapo 5) va dans `exercices_fin_de_cours` (réactions et voix gardées). Celle de `rg_g3_mutation` (diapo 6) est **laissée** dans le cours servi : sa voix finit sur la question ; la retirer sans changer la voix laisserait une question parlée sans tableau. Réglé en phase 2 (la diapo devient la 7ᵉ).
- **Règle 54** : `rg_c1_codon` écrit au centre la définition du codon et 4³ = 64 à leur mot (le pointage visait un `centre:0` absent) ; `rg_g1_gene` écrit la définition du gène à « نعاود نقرا » et pointe l'image au mot « gène » (85 mots sans geste avant).
- Écran : « (locus) » retiré de la trace de `rg_g1_gene` (locus enseigné à la diapo suivante).

## Phase 2 — copie d'attente

### Diapos déplacées, ajoutées, coupées (règle 52)
- `rg_d2_proteine` (la protéine) déplacée juste après le rappel de l'ADN (diapo 4) ; sa question va dans la réserve de fin de cours ; sa voix ne finit plus sur une question ; définition écrite au centre. Bloc 1 : la diapo et le retrouver « protéine » y reviennent, les lignes de cahier aussi.
- Beadle et Tatum coupé en trois : **`rg_p5a_chaine`** (nouvelle : chaîne de réactions, milieu minimum, souche sauvage), **`rg_p5b_mutant1`** (nouvelle : mutant 1 raisonné ensemble, règle « pousse avec le produit après la réaction bloquée »), `rg_p5_beadle_tatum` (mutants 2 et 3, conclusion « un gène → une enzyme » dite et écrite, puis la question). Visuel existant `documents.html?vue=beadle`, URL distinctes (`&partie=chaine`, `&partie=mutant1`) pour recharger la scène ; la simulation n'a pas de `?depart=` : les diapos b et c rejouent la scène depuis le début jusqu'au moment visé (`play_until`), dès leur premier mot.
- Délétion et insertion séparées : `rg_m4_decalage` (délétion) et **`rg_m4b_insertion`** (nouvelle), même simulation que la série des mutations, `set_time 25.2` (début du segment insertion) puis `play_until insertion`, comme ses voisines. Pas de question ajoutée après la délétion (le bloc a déjà sa question en `rg_m6_juger`, règle 27).

### Notions avant leur leçon (règle 52)
- Hématie = globule rouge dit en `rg_o1` ; nucléotide (sucre + phosphate + base) ajouté au rappel de l'ADN, écrit au centre ; LDL et récepteur (« la porte ») expliqués en `rg_p4_document`.
- `rg_g3_mutation` : le repiquage (velours, même place) est expliqué avant la question ; les options et les cinq réactions ne disent plus « mutation » (définie à la diapo suivante).
- Triplet / codon : la simulation de `rg_t6_bareme` écrit déjà « un codon sous chaque triplet » ; plutôt que de contredire l'écran, la voix y nomme les deux (triplet sur l'ADN, codon en face sur l'ARNm, « pourquoi trois : juste après ») et `rg_c1_codon` les redit. La réaction juste de `rg_t6` ne parle plus de codon initiateur/stop.
- Anticodon retiré de `rg_c2_tableau` (voix et écran) et le piège « on cherche le codon, jamais l'anticodon » placé en `rg_r1_acteurs`.
- `rg_c3` : « notre ARNm » → « cet ARNm écrit en bas » ; « la traduction s'arrête » → « la lecture s'arrête ».
- Laissé : `rg_e7_moustiques` « site actif » (le document du national le nomme et la voix explique ce que fait le carbamate ; une phrase de définition reste à ajouter si l'on refait cette diapo) ; `rg_t3` « la transcription n'est pas la traduction » (mise en garde, mot du programme).

### Notions importantes (règle 55) et tuteur humain (règle 56)
- 33 diapos clés : chacune a une annonce différente dans ses premiers mots, une deuxième façon de dire (« بطريقة أخرى / بمعنى آخر / بعبارة أخرى / يعني بالدارجة », image du quotidien : livre et phrase, adresse, cuisinier, photocopie, carte, phrase coupée…) et un rappel dans une diapo suivante (« تفكر… » : phénotype en `rg_p1`, protéine en `rg_p3`, chaîne en `rg_p5b`, mutation en `rg_m1`, triplet en `rg_c1`, photocopie en `rg_t2`/`rg_s2`…).
- Débuts de voix : plus aucune paire de diapos consécutives au même premier mot (9 avant) ; « دابا » ne domine plus (13 % → 3 diapos sur 73 ouvrent par « دابا ») ; les énoncés du national ne s'ouvrent plus tous par « دابا غادي نقراو ».
- Touches humaines : « شوف هاد الحاجة، غريبة شوية! » (arbre de Noël, délétion), « هنا بالضبط فين كيغلطو بزاف ديال التلاميذ » (barème), « علاش كنقراو هاد la diapo؟ », « خلي كلشي على جنب شوية ».
- Réactions : 79 débuts réécrits (« شوف، الجواب الصحيح هو… », « شوف، اللي قلتي فيه… », « مزيان، جوابك صحيح… ») par des ouvertures variées de la banque (§5, §6) ; aucun début de 6 mots répété 4 fois.

## Pistes à générer
129 pistes : 45 voix de diapositive (dont 3 nouvelles diapos), 84 réactions. Aucune voix générée.

## Mots douteux pour la voix (corpus < 3, nouveaux dans cette copie)
Français : chercher, découper, s'arrêter, diapo. Darija : الثوب, الطباخ, خريطة, ذكية, لغة, المحبوسة, كافياش, صاوبهمش,
مقاوماش, كنضغطو, كيزحلقو, تزحلقات, كتتصاوب, كيتصاوبو, كتطيبش, كتخليه, كنقارنوهم, مقابلهم, يرافقونا, كيهزو,
كتأكد, نصلحوها, كنغلط, قتل, تبعني (tournure d'annonce de la banque), ضاعش. Plus les mots déjà signalés du cours
(streptomycine, neurospora, ornithine, citrulline, tyrosinase…). À écouter après génération.

## Vérifications
- `verifier_formules.py`, `verifier_parcours.py`, `verifier_figures_cahier.py` : sans nouveau défaut (1 avertissement ancien de taille de figure).
- La copie d'attente part du cours servi à jour sur `main` (phase 1 + revue des cahiers da226b37) ; les lignes de cahier des diapos et blocs touchés suivent ce nouveau format.
- `verifier_pointage.py` : sortie identique au cours servi.
- `verifier_pointage_simulations.py` : seuls écarts nouveaux = « GESTE » sur les diapos sans piste (durée 0 tant que la voix n'est pas générée) et « IFRAME » de `rg_m4b_insertion`, du même type que toute la série des mutations (même URL, `set_time` en tête).
- `nombres_fr.py` : 0 nombre darija à côté du français.
