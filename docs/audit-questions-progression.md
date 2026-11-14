# Relecture des questions des 19 cours — règle 27 (12 novembre 2026)

Règle appliquée (skill `professeur`, règle 27) : une question ne peut utiliser que les notions **déjà
enseignées dans ce cours jusqu'à cette diapo** et dans les cours déjà faits ; les notions des années
précédentes sont permises mais rappelées en une phrase et jamais notées ; et on ne questionne pas
chaque diapo.

Méthode : pour chaque cours, chaque mot d'un énoncé et de **chaque option** (y compris les mauvaises)
est cherché dans le texte des diapos **qui précèdent**. Script : `scratchpad/audit/audit2.py`.

## 1. Notions demandées avant d'être enseignées — corrigé

| Cours | Diapo | Ce qui n'était pas encore vu | Correction |
|---|---|---|---|
| SVT 1 | 7 `le_e4_carte` | options « Le cycle de Krebs », « La chaîne respiratoire » (enseignés diapo 14) | options → « La respiration cellulaire », « La fermentation » (toutes deux dites sur la diapo) ; réactions réécrites |
| SVT 2 | 12 `ms_f3_fusion_complete` | option « un tétanos parfait » (diapo 13) | → « deux secousses bien séparées » ; réaction réécrite |
| SVT 3 | 10 `ig_c1_cycle` | option « la prophase » (diapo 17) | → « la phase S seule » (dite sur la diapo) ; réaction réécrite |
| Phys 5 | 3 `en_m4_931` (exercice) | « l'énergie de liaison » (diapo 8) | énoncé ramené à une conversion MeV → J |
| Phys 9 | 10 `tl_x9_oxalique` (exercice) | « Titrage » (diapo 13) | mot retiré de l'énoncé |

Aucune de ces corrections ne touche un texte déjà mis en voix : les réactions de ces diapos n'ont pas
de piste enregistrée (voix en direct). Rien à regénérer, rien à redéployer côté audio.

## 2. Reste à décider : deux cas qui demandent plus qu'une retouche de texte

### a) La question d'acquis notée — SVT 1, diapo 1 `le_o2_acquis`
« Dans quel organite se déroule la respiration cellulaire ? » (réponse : la mitochondrie). La
mitochondrie n'est présentée qu'à la diapo 14 de ce cours ; c'est un acquis des années précédentes,
et **beaucoup d'élèves n'ont pas fini le programme antérieur**. La règle 27 l'autorise, mais à
condition de ne pas la noter. Or le lecteur note toutes les questions.

Il manque un drapeau `non_note: true` sur la question : hors score, hors méthodes, pas de cycle de
reprise — exactement le traitement déjà existant pour une question passée (`passee`), à brancher dans
`suivi_acquis.py` et `CourseFocusStage.tsx`. Même besoin pour toutes les diapos « rappel / acquis »
des autres cours. La voix, elle, n'a pas à changer.

### b) Une question à chaque diapo

| Cours | Diapos | Diapos avec question | Questions + exercices | par diapo |
|---|---|---|---|---|
| SVT 1 | 43 | 41 | 49 | 1,14 |
| SVT 2 | 53 | 51 | 55 | 1,04 |
| SVT 3 | 47 | 45 | 48 | 1,02 |
| SVT 4 | 47 | 45 | 46 | 0,98 |
| Phys 2 | 47 | 45 | 56 | 1,19 |
| Phys 3 | 53 | 51 | 62 | 1,17 |
| Phys 4 | 52 | 52 | 55 | 1,06 |
| Phys 5 | 38 | 36 | 44 | 1,16 |
| Phys 6 (RC) | 48 | 48 | 75 | 1,56 |
| Phys 7 (RL) | 48 | 48 | 81 | 1,69 |
| Phys 8 (RLC) | 48 | 48 | 83 | 1,73 |
| Phys 9 | 36 | 36 | 58 | 1,61 |
| Math 1 | 68 | 66 | 83 | 1,22 |
| Math 2 | 64 | 62 | 80 | 1,25 |
| Math 3 | 59 | 57 | 62 | 1,05 |
| Math 4 | 44 | 44 | 110 | 2,50 |
| Math 5 | 53 | 53 | 140 | 2,64 |
| Math 6 | 48 | 48 | 141 | 2,94 |

Presque toutes les diapos portaient une question : l'élève était interrogé en permanence au lieu
d'être accompagné. La règle 27 demande une vraie question par bloc de 3–4 diapos, plus les prédictions.

**Retiré le 12 novembre 2026.** Sur 876 questions, 714 sont annoncées par la voix elle-même
(« …سؤال : »), déjà enregistrée : les retirer obligerait à réécrire la fin du `speech_text` et à
refaire la piste (voix Bodi, quota GPU Kaggle). Les 162 autres étaient retirables sans toucher à la
voix ; **118 ont été retirées**, les 44 restantes sont gardées comme porte d'entrée : chaque bloc
conserve sa prédiction (la question posée AVANT l'explication, cours-concentration), et aucun bloc ne
reste sans question. Script : `scratchpad/audit/alleger.py`.

| Cours | Questions retirées | Reste (questions + exercices / diapos) |
|---|---|---|
| SVT 4 | 1 | 44 + 1 pour 47 |
| Phys 4 (radioactivité) | 21 | 31 + 3 pour 52 |
| Phys 5 (énergie nucléaire) | 1 | 35 + 8 pour 38 |
| Phys 6 (RC) | 19 | 29 + 27 pour 48 |
| Phys 7 (RL) | 23 | 25 + 33 pour 48 |
| Phys 8 (RLC) | 28 | 20 + 35 pour 48 |
| Phys 9 (transformations) | 25 | 11 + 22 pour 36 |
| Math 4 (primitives) | 0 | 44 + 66 pour 44 |

Chaque retrait enlève la `question` de la diapo et sa clé `concentration.reponses.q` ; les pistes des
réactions préparées restent sur le serveur, inutilisées. Vérifié : aucune réaction orpheline, aucune
question sans réaction, aucun bloc sans question.

### Les 714 autres — retirées le 13 novembre 2026 (lot de voix préparé)

Règle appliquée telle quelle : **une vraie question par bloc** (les blocs font déjà 3 ou 4 diapositives),
plus les prédictions authentiques. Dans chaque bloc on garde la **dernière** question — celle qui vient
après l'explication, juste avant l'exercice du bloc — et les questions marquées `prediction` (leur voix
ne les repose pas). Tout le reste part.

**478 questions retirées**, 291 gardées (dont les 47 prédictions). Aucun bloc ne reste sans question.

| Cours | Diapos | Blocs | Questions | Exercices | Pistes à refaire |
|---|---|---|---|---|---|
| svt_ch1_reactions_responsables_liberation_energie | 43 | 12 | 41 → **12** | 8 | 29 |
| svt_ch2_role_muscle_strie_squelettique | 53 | 15 | 51 → **15** | 4 | 36 |
| svt_ch3_notion_information_genetique | 47 | 14 | 45 → **15** | 3 | 30 |
| svt_ch4_relation_gene_proteine | 47 | 14 | 44 → **15** | 1 | 29 |
| phys_ch1_waves_exemple | 16 | 5 | 11 → **6** | 4 | 3 |
| phys_ch2_ondes_periodiques | 47 | 15 | 45 → **15** | 11 | 30 |
| phys_ch3_ondes_lumineuses | 53 | 15 | 51 → **15** | 11 | 36 |
| phys_ch4_radioactivite | 52 | 14 | 31 → **17** | 3 | 13 |
| phys_ch5_energie_nucleaire | 38 | 11 | 35 → **16** | 8 | 19 |
| phys_ch6_dipole_RC | 48 | 12 | 29 → **18** | 27 | 9 |
| phys_ch7_dipole_RL | 48 | 12 | 25 → **20** | 33 | 1 |
| phys_ch8_circuit_RLC | 48 | 12 | 20 → **16** | 35 | 0 |
| phys_ch9_transformations_lentes_rapides | 36 | 9 | 11 → **10** | 22 | 1 |
| math_ch1_limites_continuite | 68 | 21 | 66 → **21** | 17 | 45 |
| math_ch2_derivation_etude_fonctions | 64 | 20 | 62 → **20** | 18 | 42 |
| math_ch3_suites_numeriques | 59 | 17 | 57 → **18** | 5 | 39 |
| math_ch4_primitives | 44 | 14 | 44 → **15** | 66 | 29 |
| math_ch5_fonctions_ln | 53 | 14 | 53 → **14** | 87 | 39 |
| math_ch6_nombres_complexes | 48 | 12 | 48 → **13** | 93 | 35 |

**La voix.** Quand la piste enregistrée posait la question à la fin (« …سؤال : … »), la fin du texte dit
est coupée : le tuteur termine sur son explication et ne pose plus rien. La coupe enlève les phrases
finales qui interrogent (« ؟ », marqueur « سؤال », consigne à l'impératif en français). Deux garde-fous :
on ne coupe pas plus de 3 phrases, ni plus de 300 caractères, ni plus de 40 % du texte — sinon la
diapositive garde sa question (4 cas : des listes de questions directrices et des corrections de
national qui se terminent par des « ? »). Le texte français, qui n'est pas mis en voix, est nettoyé par
une seconde passe (30 consignes du type « Calcule cette limite. ») ; un conseil du professeur
(« Vérifie toujours : … ») est laissé.

**465 pistes de diapositives sont donc à refaire.** Scripts : `scratchpad/lot/preparer.py`,
`couper.py`, `fr2.py`, journal `pistes_a_refaire.json`.

### Le lot de voix, prêt sur le serveur (13 novembre 2026)

- les 19 `cours.json` de `/srv/corpus_v4/voix_lot/<deck>/` sont à jour (`exporter.py`) ;
- les **464 pistes périmées** sont écartées dans `/srv/corpus_v4/voix_lot/_perimees_13nov/` (une
  introuvable : phys_ch9 n'a aucune piste de diapositive sur le serveur) ; elles ne sont pas effacées,
  rien n'est perdu ;
- la file compte **505 pistes de diapositives** à faire (les 465 refaites + 40 jamais faites) ;
  `voix_bodi_lot.py` les prend en premier (priorité `mixed`), avant les énoncés lus, les démonstrations
  et les réactions.

Il reste à **allumer le GPU** : `ssh moalim-vps bash /srv/corpus_v4/voix_lot/lancer_compte1.sh` (ou
`lancer_compte2.sh`), puis à poser les pistes prêtes :
`bash <scratchpad>/voix_lot/rapatrier.sh 11 <deck> …` et `python -I scripts/publier_cours_ondes.py`.

**Tant que les pistes ne sont pas refaites, on ne republie pas** : le texte dit a changé mais les MP3
en ligne posent encore la question. Les cours gardent leur `audio.mixed` actuel, et `poser_voix.py` ne
remplacera que les pistes dont le texte correspond (contrôle par empreinte).

## 3. La même question posée deux fois (12 novembre 2026)

Cas signalé : la question s'affiche et l'élève y répond, **puis** vient la diapo et son explication,
**puis** le tuteur repose la même question à l'oral.

Cause : la question portait `prediction: true` (posée AVANT la voix, cours-concentration), alors que
le `speech_text` déjà enregistré se termine en la reposant (« …سؤال : »). L'élève l'entend donc une
seconde fois, après l'explication.

**303 questions sur 350 étaient dans ce cas.** Correction : `prediction` retiré sur ces questions. La
question s'ouvre maintenant après l'explication, à l'endroit même où la voix la pose, et le tuteur en
lit l'énoncé (`enonce_dit`) quand le tableau s'ouvre : une seule fois, à l'oral après l'écrit.

Les **47 prédictions restantes** sont les vraies : leur voix ne repose pas la question (Phys 1 : 3,
Phys 4 : 5, Phys 5 : 5, Phys 6 : 8, Phys 7 : 9, Phys 8 : 9, Phys 9 : 7, Math 4 : 1). Les cours de SVT
et de maths n'en ont donc plus : pour leur en rendre, il faut réécrire la fin de leur `speech_text`
(enlever la question reposée) et refaire la piste — à grouper avec la prochaine fenêtre de quota GPU.
Script : `scratchpad/succession.py`.

## 4. Republication

- **12 novembre 2026** : publié. Les 5 questions hors progression, les 118 questions retirables sans
  voix et les 303 doublons écrit/oral sont en ligne.
- **13 novembre 2026** : les 478 questions en trop sont retirées dans les cours du disque, mais **rien
  n'est republié** : il faut d'abord les 465 nouvelles pistes (voir ci-dessus).

## 5. Ce qui reste

- **Les prédictions de SVT et de maths** : ces cours n'en ont plus aucune. Les rendre, ce n'est pas
  remettre un drapeau : il faut **écrire** de vraies questions de prédiction (« que prévois-tu ? »,
  avant l'explication) à l'ouverture de chaque bloc, avec leurs réactions préparées. Travail de contenu,
  une par bloc, soit environ 150 questions.
- **Le drapeau `non_note`** des questions de rappel d'acquis (§ 2a) : du code, pas de voix.

## 6. Soir du 13 novembre 2026 : moins de questions, et espacées

Trois décisions du responsable, appliquées aux 23 cours (les 19 en ligne + les 4 de chimie de la routine) :

1. **Plus d'étape « prédiction »** (« 🔮 Avant d'expliquer : que prévois-tu ? »). Le lecteur ne pose plus rien avant
   l'explication (`PREDICTIONS_AVANT_LA_VOIX = false`, `CourseFocusStage.tsx`). Dans les cours (un agent par matière) :
   89 prédictions → 70 supprimées, 19 gardées comme questions normales (seule question de leur bloc), réécrites sans
   « Avant de voir ». Plus aucun `prediction: true`.
2. **Fin de bloc : le cahier seulement** (`ETAPES_FIN_DE_BLOC = ['cahier']`, `CycleBloc.tsx`). « Retrouver » et l'exercice
   de bloc restent dans les cours pour l'étape de fin de cours, ne sont plus joués ni mis en voix.
3. **Un seul tableau « ✏️ À toi » par bloc** : la question du bloc + au plus un exercice, sur la même diapositive.
   488 exercices des diapositives passent dans `exercices_fin_de_cours` (réactions dans `reponses_fin_de_cours`) :
   gardés pour l'étape de fin de cours, ni affichés ni mis en voix. Avant : un tableau sur 576 diapositives sur 1 080
   (jusqu'à 100 % en maths ch4–ch6) ; après : 300 tableaux, un par bloc.

Voix : les phrases qui invitaient à un exercice ou à une question disparus (« Réponds au QCM au tableau », « À toi : … »,
« سؤال: … ») sont coupées — 28 pistes de diapositives refaites. En maths, la plupart de ces invitations n'étaient que
dans le texte français (non mis en voix) : coupées sans piste à refaire.

Les formules du centre ne recouvrent plus la simulation : elles vont dans une bande sous la figure.

Reste : **l'étape de fin de cours** qui reprendra `bloc.retrouver`, `bloc.exercice` et `exercices_fin_de_cours`.
