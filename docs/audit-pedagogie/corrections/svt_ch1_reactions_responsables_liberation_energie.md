# Corrections — svt_ch1_reactions_responsables_liberation_energie (audit pédagogique du 26/11/2026)

Phase 1 : cours servi `backend/data/courses/svt_ch1_reactions_responsables_liberation_energie.json` (aucun texte parlé changé).
Phase 2 : copie d'attente `backend/data/courses/en_attente/svt_ch1_reactions_responsables_liberation_energie.json`
(repartie du cours servi après la phase 1 ; l'ancienne copie d'attente, périmée, est remplacée).
Pistes à générer : `docs/audit-pedagogie/voix_a_generer/svt_ch1_reactions_responsables_liberation_energie.json`.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| | avant | après phase 1 (servi) | après phase 2 (attente) |
|---|---|---|---|
| Diapos | 63 | 63 | 67 |
| Questions dans les 6 premières | 3 | 2 | 0 |
| Première question de bloc après la diapo | 5 | 9 | 11 |
| Formules dites non écrites | 4 | 0 | 0 |
| Passages ≥ 60 mots sans geste | 1 | 0 | 0 |
| Notions clés / redites | 15 / 6 | 17 / 6 | 18 / 18 (100 %) |
| Annoncées (phrases ≠) | 0 (0) | 0 (0) | 18 (18) : 100 %, toutes différentes |
| Premier mot le plus fréquent | « دابا » 41 % | 41 % | « دابا » 9 % |
| Diapos qui suivent avec le même premier mot | 8 | 8 | 0 |
| Débuts de voix répétés | « دابا غادي » ×6 | ×6 | — |
| Réactions au même début (≥ 4) | 1 | 1 | 0 |
| Tournures recopiées ≥ 5 diapos | 4 | 4 | 4 (« N A D H, H plus » : le nom de la molécule, laissé) |

Vérifications passées sur les deux fichiers : `verifier_formules.py` (0), `verifier_parcours.py` (0 erreur),
`verifier_figures_cahier.py` (0 erreur), `verifier_pointage.py` (mêmes 83 remarques qu'avant, aucune nouvelle),
`verifier_pointage_simulations.py` (les 2 écarts PROCESSUS d'avant, `le_k3_roue` et `le_f2_alcoolique`, aucun nouveau ;
dans la copie d'attente les diapos sans piste donnent des GESTE « trop serrés » parce que leur durée est 0 : avec une
durée estimée à 0,43 s par mot, aucun écart), `nombres_fr.py` (0), `verifier_mots.py` (aucun mot rare dans les phrases ajoutées).

## Phase 1 (cours servi, commit 0df043a2)

- **Questions trop tôt** : le vrai/faux d'acquis de la diapo 3 (`le_o2_acquis`, qui demandait aussi « énergie chimique »,
  enseignée en diapo 5) → `exercices_fin_de_cours` (réactions → `reponses_fin_de_cours`). Sans ce diagnostic, les
  `rappel.si_reussi` de `le_p1_cellule` et `le_p2_glucose` sont retirés : ces rappels se jouent toujours (règle 34).
- **Bloc 1** (`le_s1_b1`, diapos 1 à 5) : son RETROUVER et son exercice tombaient avant la 6ᵉ diapo → réserve de fin de cours
  de `le_p2_glucose` ; le bloc garde son cahier.
- **Dit = écrit** (`concentration.centre` au mot exact) : FADH₂ 2 × 1 = 2 (`le_k5_fois_deux`) ; équation d'un tour de Krebs,
  écrite en deux moitiés à leur phrase (`le_k4_sorties`, qui avait 94 mots sans geste) ; chaleur 2860 − 1159 = 1701 kJ et
  1701/2860 × 100 ≈ 59,5 % (`le_r2_rendement`) ; r = 61/2860 × 100 puis 2,13 % à leur phrase (`le_r3_comparer`).
- **Écran** : titre de la partie I sans « (rappel) ».
- Les questions des diapos 5 et 6 restaient en phase 1 : la voix les pose (« سؤال : … ») ; retirées en phase 2.

## Phase 2 (copie d'attente)

### Diapos ajoutées (4)

| Id | Place | Contenu | Visuel |
|---|---|---|---|
| `le_p1b_molecule` | avant le glucose | Rappel : atome, molécule, liaison (l'énergie est dans les liaisons) | carte simple (`visual.kind: none`), 3 lignes écrites au centre à leur mot — aucune vue existante ne montre des atomes seuls |
| `le_a1b_recharge` | après `le_a1_monnaie` | La phosphorylation de l'ADP (seconde moitié de l'ancienne diapo 6), avec la question « d'où vient l'énergie de la recharge ? » | même simulation `atp.html`, ouverte figée `?depart=hydrolyse&rappel` (URL distincte, règle 39) |
| `le_t0_hydrogene` | avant `le_t1_deux_h` | Rappel : noyau, protons, électrons ; H = un proton + un électron ; H⁺ = proton | carte simple, 3 lignes au centre |
| `le_c0_ph` | avant `le_c1_pulse` | Rappel : H⁺ = proton ; plus de H⁺ → pH plus bas (acide) ; pH 4 / pH 8 | carte simple, 3 lignes au centre |

Les trois cartes sont titrées « Rappel : … » ; ajoutées à leurs blocs (`seances`) et compétences (C1, C3, C6).

### Ordre des notions (`ordre-des-notions/<deck>.md`)

| # | Défaut | Fait |
|---|---|---|
| 1 (forte) | diapo 6 : ATP, hydrolyse, phosphorylation ensemble | coupée en `le_a1_monnaie` (ATP + hydrolyse, sans question) et `le_a1b_recharge` (phosphorylation + question) |
| 2 (forte) | protons/électrons jamais rappelés (17-18) | `le_t0_hydrogene` ; `le_t2_reduit` le rappelle (« تفكر : كل hydrogène، proton و électron »). FAD laissé en `le_t2_reduit` : la question FAD applique la règle « gagner = réduit » qui vient d'être enseignée sur NAD⁺, et la simulation l'anime |
| 3 (forte) | pH jamais rappelé (30-38) | `le_c0_ph` ; `le_c6_protons` y renvoie |
| 4 | atome, molécule, liaison | `le_p1b_molecule` ; `le_p2_glucose` s'y relie |
| 5 | levure, ExAO, concentration | phrases ajoutées dans `le_e1_mesurer` |
| 6 | aérobie / anaérobie en diapo 9 | **laissé** : `le_e3b_masse_levures` (diapo suivante) s'en sert aussitôt ; les déplacer en diapo 12 casserait la 10 |
| 7 | eau de chaux | déjà dit (« كيخلي l'eau de chaux تولي بيضة ») : défaut non confirmé |
| 8 | crêtes en diapo 11 | « des plis من الداخل، غادي نسميوهم من بعد les crêtes » |
| 9 | organique / minéral jamais défini | défini dans `le_o2_acquis` (voix + écran + trace) |
| 10 | acide pyruvique « produit de la glycolyse », centrifugation | `le_m3_isolees` : « formé à partir du glucose dans le hyaloplasme » + phrase sur la centrifugation |
| 11 | décarboxylases/déshydrogénases en diapo 24 ; exercice du bloc `le_s3_b1` | noms retirés de la voix et de la trace (« des enzymes, on verra leur travail ») ; `le_m2_legender` annonce que la chaîne respiratoire sera expliquée plus loin. L'exercice du bloc est **laissé** : il reprend ce que disent `le_m2_legender` et `le_m2c_composition` (« ces protéines sont les transporteurs de la chaîne respiratoire et les sphères ») ; aucun bloc après la diapo 36 n'a de place libre sans déplacer un exercice vers un bloc où il serait trop tôt. Les questions de bloc ne sont d'ailleurs plus jouées (`FIN_DE_BLOC_COMPLETE = False`) |
| 12 | vésicules : intérieur = espace intermembranaire | dit dans `le_c10_vesicules` |
| 13 | T1-T6 / C1-C5 / 1-4 (diapos 40-42) | **laissé** : les noms sont dessinés par les simulations (`enonce.html`, `national.html`) ; unifier demande de changer la simulation, hors de ce lot |
| 14 | 1 NADH = 3 ATP, 1 FADH₂ = 2 ATP dit en passant | enseigné dans `le_c7_sphere` (image du bus, écrit au centre), rappelé dans `le_r1_compteur` |
| 15 | 36 jamais expliqué | `le_r1_compteur` : coût d'entrée des 2 NADH,H⁺ de la glycolyse, 38 − 2 = 36 (écrit au centre) |
| 16 | mole, kJ | une phrase dans `le_r2_rendement` |
| 17 | national 2016, document 2 | l'écran (`enonce.html`) et la voix darija nommaient déjà la personne devant chaque valeur ; seul `speech_text.fr` disait « 12 et 6… 2,5 et 5,5 » : corrigé (copie d'attente) |

Questions dans les 6 premières : la question de `le_p2_glucose` part en réserve de fin de cours (sa voix ne la pose plus) ;
celle de l'ancienne diapo 6 est maintenant en diapo 8 (`le_a1b_recharge`).

### Notions importantes (règle 55)

Les 18 diapos clés (dont `le_m2_legender`, devenue clé avec le cahier revu le 26/11 : « هاد le schéma مهم بزاف ») ont chacune une annonce différente en tête (« هاد الجزء مهم فالامتحان », « حل عينيك على le tableau »,
« جات اللحظة المهمة », « تبعني بالشوية », « وقف معايا شوية هنا », « سمعني مزيان », « ركّز معايا », « هنا المهم ديال le cycle de Krebs »,
« بزاف ديال التلاميذ كيغلطو هنا، تبع معايا », « القلب ديال الدرس », « ركز مزيان », « بغيتك تحفظ », « وهادي مهمة »,
« c'est important », « le plus important », « ركز معايا », « حلّ عينيك مزيان ») et une redite (« بطريقة أخرى », « بمعنى آخر »,
« بعبارة أخرى », « عاود معايا », « بكلمة أخرى », « نعاودها بكلمة خرى », « يعني بالدارجة », « نقولها بطريقة أخرى »…).
Rappels ajoutés plus loin : l'ATP (`le_m4_o2_atp`), la chaîne respiratoire (`le_c9_poison`), la phosphorylation par les sphères
(`le_c10_vesicules`), la règle 3/2 ATP (`le_r1_compteur`), la relation du rendement (`le_r3_comparer`), le pH (`le_c6_protons`).

### Tuteur humain (règle 56)

- Débuts de voix : « دابا » passe de 26 diapos à 6 ; les cinq lectures d'énoncé du national ne commencent plus toutes par
  « دابا غادي نقراو السؤال كيف جا فالامتحان » ; liens avec la diapo d'avant (« شفنا شنو هي une molécule… », « عرفنا الطاكسيات… »,
  « مزيان، فهمنا la décarboxylation… »).
- Touches humaines : « شوف هاد الحاجة، غريبة شوية » (levures sans O₂), « أنا عارف بلي بزاف ديال الأرقام » (composition),
  « بزاف ديال التلاميذ كيغلطو هنا » (fois deux), images (pile, briques et ciment, bus, compteur à l'envers).
- Réactions : 68 réactions jouées réécrites dans leurs premiers mots (« شوف، الجواب الصحيح هو » ×…, « مزيان، جوابك صحيح. »,
  « الجواب هو », « شوف، اللي قلتي… » remplacés par des ouvertures variées qui reconnaissent l'effort ou ce qui est juste) ;
  plus aucun début identique sur 4 réactions. Les réactions des blocs et de la réserve de fin de cours (non jouées) sont laissées.

## Pistes à générer : 109

41 diapositives (dont 4 nouvelles) et 68 réactions — `docs/audit-pedagogie/voix_a_generer/svt_ch1_reactions_responsables_liberation_energie.json`
(chaque piste dont le texte change n'a plus d'`audio`).

## Mots à écouter

Aucun mot rare (corpus < 3) dans les phrases ajoutées. Nouveaux mots darija à écouter quand même : « الياجور », « السيمة »
(`le_p1b_molecule`), « عداد مقلوب » (`le_c0_ph`), « كنطحنو », « la centrifugation » (`le_m3_isolees`), « ExAO » et
« champignon » (`le_e1_mesurer`), « le bus » (`le_c7_sphere`). Mots rares déjà présents avant : chaux, bombe calorimétrique, éthanal, iodée.

## Après la revue des cahiers (commit 63901db7, autre session)

La copie d'attente a été refaite à partir du cours servi qui porte déjà les cahiers revus ; les cahiers des diapos
touchées ici (`le_a1_monnaie`, `le_a1b_recharge`, `le_o2_acquis`, `le_c7_sphere`, cartes de rappel) suivent le même style
(une idée par ligne). Deux formules du cahier revu étaient écrites à plat (« (nombre d'ATP × 30,5) / 2860 », diapo
`le_r2_rendement` et cahier du bloc `le_s5_b2`) : remises « 30,5)/2860 » dans les deux copies (écran seulement).
