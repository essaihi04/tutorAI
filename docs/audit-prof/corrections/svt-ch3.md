## Notion de l’information génétique

Fichier modifié : `backend/data/courses/en_attente/svt_ch3_notion_information_genetique.json`. Je suis parti de la copie en attente, rien n'est perdu (toutes les diapos, réactions, observations et démonstrations de ce matin sont là). Le cours en ligne n'a pas été touché. Le cours passe de 59 à 60 diapos.
Script de la passe : `scratchpad/svt3c/build.py` (+ `figs.py` pour les dessins du cahier). Copie d'avant : `scratchpad/svt3c/avant.json`.

### Manques corrigés

| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| H : télophase incomplète | Écrit et dit : décondensation, l'enveloppe nucléaire et le nucléole réapparaissent, le fuseau disparaît, étranglement. Puces, cahier, cahier du bloc, voix, bilan. | ig_m4_anaphase, bloc ig_s3_b1, ig_b1_bilan |
| H : un schéma titré et légendé par phase | 4 dessins au cahier, chacun avec un titre « … (2n = 4) » et ses légendes : prophase, métaphase, télophase animale, télophase végétale. La consigne de légendes est aussi écrite au cahier. Le bloc ig_s3_b1 reprend métaphase + télophase, le bloc ig_s3_b2 la végétale. | ig_m2, ig_m3, ig_m4, ig_m5 |
| H : mécanisme de la transformation | 5 étapes, une ligne au centre par étape : fragments d'ADN, entrée dans R, intégration à l'ADN de R, capsule, bactéries filles S (caractère héréditaire). Puis la conclusion. Voix réécrite, schéma légendé au cahier (diapo et bloc ig_s4_b2). | ig_t3_support |
| H : relation chromosome–ADN | **Nouvelle diapo**. Réaction de Feulgen (colorant spécifique de l'ADN : noyaux et chromosomes rouges, « or… donc… »). Chromosome sans ses histones : charpente de protéines + long fil d'ADN. D'où chromosome = ADN + protéines. 5 lignes au centre, croquis au cahier, bloc ig_s2_b1, C2. **Sans visuel** : aucune vue existante ne convient. | **ig_n1b_feulgen** |
| H : Taylor | Taylor nommé. Autoradiographie (film, points noirs) et colchicine (arrêt en métaphase), écrites et dites. 3ᵉ cycle ajouté : 8 lignes au centre, du 1ᵉʳ cycle à la conclusion. | ig_r7_thymidine1, ig_r8_thymidine2 |
| M : Chargaff (A+G)/(T+C) et (A+T)/(G+C) | Ce qui est fait : (A+G)/(T+C) = 1 est déduit de A = T et G = C. (A+T)/(G+C) est calculé pour 3 espèces : 1,52 / 1,36 / 1,38, il est caractéristique de l'espèce. 6 lignes au centre, puces, cahier, bloc, bilan. | ig_s2_chargaff |
| M : exercice des 24 nucléotides | 2 exercices libres en réserve de fin de cours, chacun avec sa démonstration. (1) Le fragment a deux brins : 24 × 0,34 = 8,16 nm ≠ 4,08 nm, alors que 12 × 0,34 = 4,08 nm. (2) Les bases : T/G = 1,4, T + G = 12, donc G = C = 5 et A = T = 7. | ig_s4_helice (exercices_fin_de_cours) |
| M : dimensions de la double hélice | 0,34 nm entre deux paires, 3,4 nm par tour (10 paires), 2 nm de diamètre : centre, puces, cahier, voix, bloc. | ig_s4_helice |
| M : rupture des liaisons H, matrice | Écrit et dit, avec une ligne au centre. | ig_r9_yeux, bloc ig_s6_b1 |
| M : 2n, diploïde, homologues | 2n = 46 (n = 23 paires de chromosomes homologues), cellule diploïde : centre, puces, cahier, voix. Rappel écrit dans ig_m1 : 2n = 4 = 2 paires. | ig_p1_chromosomes, ig_m1_mitose, bloc ig_s1_b3 |
| M : nucléofilaments, collier de perles | Écrit et dit. | ig_n1_noyau, bloc ig_s2_b1 |
| M : acide désoxyribonucléique | Écrit et dit, avec aussi polynucléotide et bases puriques / pyrimidiques (basse). | ig_s1_nucleotide, bloc ig_s4_b3 |
| M : fibres polaires / chromosomiques | Puce et légende du dessin. | ig_m3_metaphase |
| B : conclusion écrite de la mérotomie | « Le noyau est indispensable à la vie de la cellule et à sa division » : écrit au cahier de la diapo et du bloc. | ig_l1_amibe |
| B : smooth / rough, dates, Avery-MacLeod-McCarty, ADNase, lipides et glucides retirés | Écrit. | ig_t1_griffith, ig_t2_avery, ig_r2_experience |
| B : sang des souris 2 et 3 | « Pas de pneumocoques dans son sang » : écrit. | ig_t1c, ig_t1d, bloc ig_s4_b1 |
| B : méristème, classement chronologique | Écrit. | ig_m6_photo |
| B : bras du chromosome | Puce. | ig_n3_chromatides |
| B : centrosome ≠ centromère | Piège ⚠ écrit. | ig_m5_vegetale |
| B : E. coli, Franklin, définition écrite du cycle | Écrit. | ig_r2, ig_s4, ig_c1 (+ bloc) |
| Présent seulement à l'oral | Tout est maintenant écrit : l'azote dans les bases (ig_r2) ; l'enveloppe qui se reforme (ig_m4) ; les prévisions des 3 hypothèses au cahier (ig_r6 + bloc) ; le calcul 30,9/29,4 ≈ 1,05 (ig_s2) ; G2 = 4 h et M = 1 h (ig_c6) ; « car la cellule a une paroi » (ig_m5) ; plus d'yeux en fin de S « car » (ig_c4) ; la métaphase est la phase où l'on compte (ig_m3). | voir colonne 1 |
| Notations | Q accepté (« q, notée aussi Q »), chromosome fils, xénope, ADNase, fuseau de division, duplication / matrice. | ig_c3, ig_m4, ig_l5, ig_t2, ig_m2, ig_r9 |
| Formules (`verifier_formules`) | 12 barres à plat corrigées, par exemple « (1,710 + 1,724)/2 » et « (% de cellules dans la phase)/100 ». | partout |

### Non corrigés et pourquoi

- **« À toi de légender » la métaphase et la transformation** : pas faits. Il faudrait une nouvelle vue de simulation (`mitose.html`, `bacteries.html`), ce que la consigne interdit. Les dessins légendés du cahier remplacent ces exercices.
- **Les simulations ne montrent pas tout ce que la voix dit maintenant** (règle 39, à faire dans les simulations) :
  - `bacteries.html?vue=avery` : ni l'intégration, ni les bactéries filles (ig_t3) ;
  - `thymidine.html` : pas de 3ᵉ cycle (ig_r8) ;
  - ig_n1b_feulgen est sans visuel.
- **Manques chez un seul professeur** : non faits, le cadre n'en exige aucun. Ce sont : l'extraction de l'ADN, l'idée de Gurdon sur la cellule différenciée, 2ⁿ cellules, interphase 18 h / 2 h, tracer la courbe, la définition de l'extrémité 5'.
- **Hors cadre** : non ajoutés. Hershey-Chase, hélicase, fragments d'Okazaki, formules chimiques, caryotype, gène.
- **« Ne pas dire repos »** : non écrit. Pour l'expliquer, il faudrait la réplication, qui vient plus tard.
- **Voix non changées** alors que leur écran a reçu un ajout mineur : ig_m1, ig_m2, ig_m3, ig_m5, ig_m6, ig_t1, ig_t2, ig_r2, ig_c1, ig_c3, ig_c4, ig_n3, ig_b1. La voix y reste juste, l'écran en dit seulement un peu plus.
- **Fiche `bilan.html`** (simulation) : non mise à jour. Seuls les puces et le cahier du bilan sont à jour.
- **Équations bilans, ATP, localisation** : sans objet dans ce chapitre.
- **Erreurs** : l'audit n'en signale aucune dans notre cours. Les deux erreurs de K (polymérase 3'→5', « conservative » chez Taylor) ne sont pas reprises.

### Démonstrations

- Je les ai toutes relues : 6 `question.demonstration`, 5 démonstrations de bloc, les preuves écrites au centre des diapos et au cahier.
- **Réécrites** : ig_n3 (q), ig_c6 (q), ig_r3 (q). Preuves des diapos, une ligne au centre par étape : ig_c6, ig_s2, ig_r3, ig_r4, ig_r5, ig_r8, ig_t3, ig_n1b.
- **Créées** pour les questions de calcul ou de déduction qui n'en avaient pas :
  - questions des diapos : ig_p3 (q), ig_r6 (q), ig_r12 (q) ;
  - exercices de bloc : s1_b1, s1_b3, s2_b1, s2_b2, s3_b1, s4_b1, s4_b2, s4_b3, s5_b2 ;
  - rappels : C3_r2, C6_r2, C7_r4 ;
  - 2 exercices de fin de cours (ig_s4_helice).
- **Gardées** (déjà complètes) : ig_m7 (q), ig_s5 (q), ig_x2 (q), blocs s1_b2, s2_b3, s3_b2, s5_b1, s5_b3, s6_b2.
- Exemples :
  - ig_c6 : avant, « G1 = 45 % × 20 h = 9 h ; S = 20 − (9 + 4 + 1) = 6 h ». Après, 8 lignes : 2 cycles → 40 h/2 = 20 h → relation → G1 = 45/100 × 20 h = 0,45 × 20 h = 9 h → G2 = 4 h → M = 1 h → S = 20 h − 14 h = 6 h → « La phase S dure 6 h ».
  - ig_r4 : avant, « Seule la semi-conservative explique : 2 hybrides, 2 légères ». Après, 7 lignes : G1 = 2 hybrides → brin ¹⁵N + nouveau = hybride → brin ¹⁴N + nouveau = légère → 2 + 2 → 2/4 = 50 % / 50 % → dispersive rejetée → conclusion.
  - ig_r3 (q) : avant, 3 lignes qui finissent par « hypothèse rejetée ». Après, 5 lignes : G0 lourd → la molécule mère reste lourde → la fille est légère → « la conservative prévoyait 2 bandes : une lourde et une légère » (la réponse) → or 1 bande à 1,717.
- Tous les calculs sont refaits en python : 20 h, 9, 4, 1, 6 h ; 1,05 ; 0,99 ; 1,52 / 1,36 / 1,38 ; 8,16 et 4,08 nm ; G = 5, T = 7 ; 3,434/2 = 1,717 ; 50 %, 25 %, 75 % ; 0,25 × 24 = 6 h ; 92 ; 12 UA.

### Voix à enregistrer (id)

- **Diapos (15, audio retiré)** :
  - voix changée : ig_p1_chromosomes, ig_n1_noyau, ig_c6_durees, ig_m4_anaphase, ig_t3_support, ig_s1_nucleotide, ig_s2_chargaff, ig_s4_helice, ig_r3_g1, ig_r4_g2, ig_r5_semi, ig_r7_thymidine1, ig_r8_thymidine2, ig_r9_yeux ;
  - nouvelle : ig_n1b_feulgen.
- **Démonstrations (parole)** :
  - questions des diapos : ig_n3, ig_c6, ig_r3, ig_p3, ig_r6, ig_r12 ;
  - blocs : ig_s1_b1, ig_s1_b3, ig_s2_b1, ig_s2_b2, ig_s3_b1, ig_s4_b1, ig_s4_b2, ig_s4_b3, ig_s5_b2 ;
  - rappels : C3_r2, C6_r2, C7_r4.
- **Exercices de fin de cours** : ig_s4_helice, 2 énoncés (`enonce_dit`) et 2 démonstrations (réserve, pas joués aujourd'hui).

### Vérifications faites (résultats)

- `json.load` : OK. Écriture avec ensure_ascii=False, indent=2, LF (0 CR). Le fichier a été relu juste avant chaque écriture (contenu identique à la lecture).
- Script de contrôle :
  - chaque `mot` des démonstrations est dans sa `parole`, dans l'ordre de la première apparition ;
  - chaque `mot` du centre et du pointage est dans `speech_text.mixed` ;
  - voix et paroles nouvelles : aucun chiffre ni symbole, pas de tachkil.
- `verif_attente.py` : 60 diapos, 0 mot absent, 0 hors bloc, 0 doublon, 0 compétence inconnue, 15 diapos sans voix (celles listées ci-dessus).
- `verifier_formules.py` : 0 relation à reprendre (12 avant).
- `verifier_figures_cahier.py` : 12 figures, 0 erreur, 0 avertissement.
- `verifier_pointage.py` : 26 remarques, exactement les mêmes qu'avant (moments calculés à l'exécution, que l'analyse statique ne voit pas). Les nouveaux moments utilisés existent bien : `capsule`, `conclusion`, `especes`.
- `git status` : seul le fichier en attente du ch3 est modifié de mon côté. `national.html` vient d'une autre session.
