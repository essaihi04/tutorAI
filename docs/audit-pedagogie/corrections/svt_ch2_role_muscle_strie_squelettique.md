# Corrections — svt_ch2_role_muscle_strie_squelettique (26/11/2026)

Sources : `ordre-des-notions/svt_ch2_role_muscle_strie_squelettique.md`, `mesures.md`, règles 52 à 56 du skill professeur.
Rien n'a été raccourci. Aucune voix générée.

## Phase 1 — cours servi (`backend/data/courses/…json`, aucun texte parlé changé)

| Correction | Diapos / blocs |
|---|---|
| Règle 53 : la question de la diapo 4 rangée dans `exercices_fin_de_cours` (avec ses réactions dans `reponses_fin_de_cours`) ; le bloc 1 pose la même idée | `ms_s2_secousse` |
| Bloc 1 étendu à la latence et aux phases : la première question de bloc passe après la 6ᵉ diapo, et l'option « au temps de latence » vient après la leçon de la latence (défaut 4, corrigé sans toucher à l'option) ; deux lignes de cahier suivent | `ms_s1_b1`, `ms_s1_b2` |
| Règle 54 : la phrase « dix-huit fois » pointe sa carte | `ms_r1_reserve` |
| Cartes `centre` posées sur les mots des passages de plus de 60 mots sans geste | `ms_o1_effort`, `ms_f7_fatigue`, `ms_u2_fibre`, `ms_n2_fibres` |

## Phase 2 — copie d'attente (`backend/data/courses/en_attente/…json`, refaite depuis le cours servi après phase 1)

Le 26/11, une autre session (commit 63901db7, « revue des cahiers SVT ch1 et ch2 ») a réécrit `cahier` et `cahier_figures` dans les deux copies. La copie d'attente repart du cours servi qui porte ces cahiers ; les cahiers des blocs ne sont pas touchés (la ligne « hydrolyse de l'ATP » reste au bloc VII, où la revue l'a placée) ; seuls les cahiers des diapos coupées sont partagés entre les deux moitiés, dans le style de la revue.

### Ordre des notions (règle 52)

| Défaut de l'audit | Fait |
|---|---|
| 2 (fort) ATP rappelé seulement en diapo 35 | `ms_e1_hydrolyse` déplacée juste après la diapo 2 (titre « Rappel : … », voix « قبل ما نبداو… », URL `atp.html?rappel=1`) ; rappel en une phrase dans `ms_c1c_myofibrille` et `ms_c4_rotation` (« نفس l'hydrolyse اللي تفكرنا ف البداية ») |
| 1 (fort) recrutement avant la fibre | **diapo ajoutée** `ms_i1b_fibres` (« Rappel : le muscle est fait de fibres ») avant `ms_i2_recrutement`, sur la simulation existante `structure.html` (`&rappel=1`, mêmes moments que `ms_u1_ouvrir`) ; `ms_i2_recrutement` et `ms_u1_ouvrir` y renvoient |
| 3 fermentation/pH utilisés comme cause (diapo 17) | rappel du chapitre 1 en une phrase dans `ms_f7_fatigue` + « on y reviendra à la fin du cours » (pas de diapo ajoutée) |
| 4 option « latence » du bloc après 4 | corrigé en phase 1 (bloc étendu) |
| 5 option « fusion » du bloc après 11 | option remplacée par « l'allongement des fibres excitées », ses deux réactions réécrites, la réaction juste ne cite plus la fusion |
| 6 diapo 21 trop chargée | coupée : `ms_t4a_sang` (le tableau → glucose) puis **diapo ajoutée** `ms_t4b_glycogene` (glycogène, sa formule écrite au mot) ; la question du bloc passe sur `ms_t4b_glycogene` (dernière diapo du bloc), avec ses réactions et leur voix |
| 7 diapo 23 (8 mots nouveaux) | coupée : `ms_u2_fibre` (cellule, noyaux, sarcolemme, sarcoplasme, rappel du cytoplasme) puis **diapo ajoutée** `ms_u2b_contenu` (myofibrilles, réticulum, striation), même image |
| 8 Ca²⁺ jamais rappelé | une phrase dans `ms_c1_exigences` et `ms_c2a_calcium_libere` (ion = atome qui porte une charge électrique) |
| 9 deux expériences dans une diapo | coupée : `ms_c2a_calcium_libere` (calcium radioactif) puis **diapo ajoutée** `ms_c2a2_equorine` (carte simple, sans visuel, comme la diapo d'origine). **Pas de question ajoutée** entre les deux : le bloc a déjà sa question (règle 27, une par bloc) |
| 10 transport actif | une phrase dans `ms_c6_relachement` |
| 11 glycolyse non rappelée | une phrase dans `ms_r8_inhibiteurs` |
| 12 document 2 du national 2016 dans l'ordre inverse | `ms_x1_enonce` nomme la personne devant chaque valeur (12 / 2,5 chez la non entraînée, 6 / 5,5 chez l'entraînée) ; l'écran (sujet) était juste |
| — (trouvé) exercice du bloc `ms_s4_b2` = double exact de celui de `ms_s4_b1` | nouvel exercice sur le rôle du Ca²⁺ (troponine / tropomyosine), réponse B, réactions écrites pour chaque choix |

Défauts vérifiés et laissés : aucun défaut faux dans le rapport. Restent « dites une seule fois » : excitabilité / contractilité, myokinase, reconstitution de la phosphocréatine, palier d'O₂, fibres I / II (lues dans un document) — non reprises faute de diapo qui les réutilise naturellement.

### Notions importantes (règle 55) et tuteur humain (règle 56)

- 30 diapos clés (la revue des cahiers a fait de `ms_s3_latence` et `ms_i1_seuil` des notions clés, « Définition : … » ; elles ont reçu une annonce et une redite) : chacune a une deuxième façon de dire (« بطريقة أخرى / بمعنى آخر », une image : peignes, corde, marcheur, moteur, relais) ; 23 ont une annonce mesurable, toutes différentes ; les 7 autres (`ms_s3_latence`, `ms_i1_seuil`, `ms_c2a2_equorine`, `ms_r2_phosphocreatine`, `ms_r4_fermentation`, `ms_r7_tableau`, `ms_r8_inhibiteurs`) ont une annonce elle aussi différente (« هادي كلمة جديدة، خليك معايا », « خلي معايا هاد الكلمة », « خلي كلشي على جنب شوية », « بغيت عينيك معايا », « إلى كانت شي حاجة غادi تبقى ف راسك… », « خليك معايا فيها ») que le motif de l'audit ne reconnaît pas — l'audit n'a que 23 formules possibles : avec 30 notions clés, la mesure plafonne à 23 / 30 = 77 % (objectif 80 % non atteignable sans répéter une formule, ce qui violerait « annonces toutes différentes »).
- Rappels plus tard : ATP (`ms_c1c`, `ms_c4`), fibres (`ms_i2`, `ms_u1`), réticulum (`ms_c2_calcium`), glycolyse (`ms_r8`).
- Débuts de voix : « دابا » passe de 19 % à 1 diapo ; plus aucune diapo qui suit avec le même premier mot ; liens avec la diapo d'avant (« شفنا… », « عرفنا دابا… », « تفكر… »).
- Réactions : les 37 « ما تقلقش، راه غلطة كيديروها بزاف… », 37 « ماشي مشكل، حنا هنا باش نتعلمو » et 21 « برافو عليك، هادا هو الجواب » (diapos, blocs, réserve de fin de cours) commencent maintenant par 31 ouvertures différentes (« قريب، », « فهمت علاش ختاريتي هادا. », « صافي، نشوفوها مع بعض. », « بالضبط! »…), suivies de la phrase existante qui nomme ce qui est juste dans le choix.
- La diapo 5 (`ms_s2_secousse`) ne finit plus sur une question (règle 53).

## Mesures (`scripts/audit/audit_pedagogie.py`)

| | Avant (servi, 26/11) | Après phase 1 (servi) | Après phase 2 (attente) |
|---|---|---|---|
| Diapos | 72 | 72 | 76 |
| Questions dans les 6 premières | 1 | 1 (voix qui finit sur ?) | **0** |
| Première question de bloc après la diapo | 4 | 6 | 7 |
| Formules dites non écrites | 1 | 0 | 0 |
| Passages ≥ 60 mots sans geste | 4 | 0 | 0 |
| Notions clés / redites | 23 / 4 | 25 / 4 (27 après la revue des cahiers) | 30 / **30 (100 %)** |
| Annoncées (phrases ≠) | 0 (0) | 0 (0) | **23 (23) = 77 %** (plafond de l'audit, voir plus haut ; 30 / 30 annoncées en réalité) |
| Premier mot le plus fréquent | « دابا » 19 % | | « هادي » **8 %** |
| Diapos qui suivent avec le même premier mot | 6 | | **0** |
| Débuts de voix répétés / tournures recopiées | « دابا غادي » ×5 / 2 | | — / 0 |
| Réactions au même début (≥ 4) | 30, 27, 4 | | **0** |

Scripts : `verifier_formules` 0, `verifier_parcours` 0 erreur, `verifier_pointage` inchangé, `verifier_figures_cahier` 0 erreur (14 figures).
`verifier_pointage_simulations` : les 36 écarts d'avant restent (IFRAME, repères construits à l'exécution) ; s'ajoutent des « GESTE » sur toutes les diapos sans voix (le script estime l'instant de chaque geste avec la durée de la piste, absente tant que la voix n'est pas générée) — à relancer après la génération.

## Pistes à générer

`docs/audit-pedagogie/voix_a_generer/svt_ch2_role_muscle_strie_squelettique.json` (format de `scripts/voix/pistes_changees.py`) :
**125 pistes** — 53 diapositives (dont 4 nouvelles : `ms_i1b_fibres`, `ms_t4b_glycogene`, `ms_u2b_contenu`, `ms_c2a2_equorine`) et 72 réactions. Les réactions et l'énoncé des blocs (retrouver / exercice) ont changé aussi mais ne sont pas mis en voix (`FIN_DE_BLOC_COMPLETE = False`).

## Mots douteux pour la voix (rares dans le corpus, `verifier_mots.py`)

- Annonces en français (seules formules de l'audit encore libres) : « concentre-toi » (`ms_c2a_calcium_libere`), « Sois attentif » (`ms_c8_conversion`), « Écoute bien » (`ms_r1_reserve`), « Suis bien » (`ms_c1c_myofibrille`) — à écouter.
- Termes du programme gardés : glycogène, striation, équorine, glycérinée, sarcolemme, chélateur, électronographie.
- Darija nouveau, peu vu : كيتسنى (`ms_s3_latence`), تبعني (`ms_g2_mesures`), حليتي, الطايب (`ms_i1b_fibres`), نبنيوها (`ms_s6_definition`), كيجبد (`ms_c4_rotation`), قربنا (`ms_u7_molecules`), واجد (`ms_s2_secousse`).
