# Audit « animations au lieu de tableaux » — SVT (règle 28 du professeur, 14 novembre 2026)

Périmètre : les quatre cours SVT en mode concentration
(`backend/data/courses/svt_ch1…ch4*.json`) et leurs dossiers de simulations
`frontend/public/media/simulations/svt/*-tableau/`.

Critère : une diapo qui montre un **tableau**, une **liste de valeurs ou de cas**, une **comparaison**, l'**effet d'un
paramètre** ou les **étapes d'un processus**, et dont le visuel n'est pas déjà une animation qui montre ce point.
Laissés de côté par principe : la fiche bilan (`*_b1_bilan`), la carte (`*_b2_carte`), et les **données d'examen
données sous forme de tableau** (exercices type national : l'élève doit apprendre à lire le tableau tel qu'il sera
donné).

Règle de câblage : la voix enregistrée (`speech_text`, `audio`) n'est jamais modifiée ; le `pointage` est réécrit
uniquement sur des extraits exacts de `speech_text.mixed` (vérifiés par script, chacun présent une seule fois).

Constat général : ces quatre cours étaient déjà très animés (presque toutes les diapos de cours ont une simulation à
la craie). Il restait surtout des tableaux de comparaison et deux visuels fixes.

---

## Ch. 1 — Libération de l'énergie emmagasinée dans la matière organique (`svt_ch1_reactions_responsables_liberation_energie`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `le_r3_comparer` | tableau Respiration / Fermentation (O₂, lieu, dégradation, produits, bilan, rendement) + `rendement.html` (barres) | **`comparer.html`** : un glucose dans une cellule, curseur **O₂ absent / présent**, bouton Lancer. Avec O₂ : glycolyse (2 ATP), les acides pyruviques entrent dans la mitochondrie, les 6 C sortent en 6 CO₂, 6 H₂O, les ATP montent à 38, r = 40,5 %. Sans O₂ : mitochondrie à l'arrêt, 2 ATP, r = 2,13 %, acide lactique qui garde l'énergie (résidu organique). La colonne de chaque voie (lieu, dégradation, produits, ATP, rendement) s'écrit **au moment où on le voit** : le tableau devient le résultat des deux essais (« avec O₂ : 19 fois plus d'ATP »). | **Oui** — la voix (fermentation, résidu, respiration complète, « شوف le tableau ») suit l'ordre des essais. |
| `le_x2_qui_respire` | tableau Personne A / Personne B (exercice type) | — | Non : données d'examen données en tableau, à lire comme au national. |
| `le_o1_trois_vivants`, `le_m1_deux_levures` | images (plantule/levures/muscle ; électronographies) | — | Non : rien qui bouge ni paramètre ; documents à observer. |
| autres diapos | simulations existantes (atp, exao, taxi, glycolyse, krebs, chaîne, fermentations, compteur, rendement…) | — | Déjà animées. |

## Ch. 2 — Rôle du muscle strié squelettique (`svt_ch2_role_muscle_strie_squelettique`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `ms_t4_consomme` | tableau « au repos / après l'activité » (6 mesures), pas de visuel | **`consommation.html`** : un muscle qui se contracte en rythme ; une **ligne par mesure** (dans l'ordre du document, la voix dit « السطر اللول ») : la barre part de sa valeur au repos (pointillé + valeur) et va à sa valeur après l'activité, écrite au bout avec ↑ ↓ ≈ (glycogène ↓ 0,80 ; O₂ ↑ 2,5 ; CO₂ ↑ 2,2 ; acide lactique ↑ 12 ; ATP ≈ 4,8 ; phosphocréatine ↓ 10). Un seul bouton (Faire travailler). La conclusion (régénération par la phosphocréatine) reste à l'élève. | **Oui** |
| `ms_r8_inhibiteurs` | tableau témoin / glycolyse bloquée / glycolyse + créatine kinase bloquées, pas de visuel | **`inhibiteurs.html`** : trois muscles reçoivent la même série d'excitations ; chacun son myogramme et deux jauges (ATP, phosphocréatine). Témoin : tout continue, PC ↓ un peu. Glycolyse bloquée : ATP constant, PC ↓ fortement, arrêt plus tôt. Les deux bloquées : PC constante, l'ATP s'épuise, arrêt en ~3 s. Les mots du résultat s'écrivent sous les jauges quand on le voit. | **Oui** |
| `ms_r7_tableau` | tableau des trois voies (O₂, acide lactique, rapidité, ATP) + équations | Brancher `voies.html` (coureur, jauges, équations qui s'écrivent quand une voie prend le relais) avec `play_until phosphocreatine / fermentation_lactique / respiration`. | **Non — nécessite une nouvelle voix** : la voix annonce « نقارنو … ف جدول » (« comparons dans un tableau ») et la diapo sert à écrire les équations comme à l'examen ; la diapo précédente `ms_r6_relais` montre déjà `voies.html`. |
| `ms_x1_decrire_comparer`, `ms_x2_deduire_expliquer`, `ms_x3_hypothese` | tableaux de données (national 2016 N, etc.) | — | Non : données d'examen en tableau, méthode de lecture. |
| `ms_o2_atp` | rappel ATP, sans visuel | — | Non : rappel en trois lignes, pas de comparaison ni de paramètre. |
| `ms_u2_fibre`, `ms_c8_conversion` | images | — | Non : structure fixe / synthèse ; les étapes sont déjà animées (`cycle.html`, `sarcomere.html`). |
| autres diapos | myographe, intensité, sommation, chaleur, structure, sarcomère, calcium, cycle, voies… | — | Déjà animées (dont seuil/recrutement, fréquence → fusion/tétanos, avec ou sans O₂). |

## Ch. 3 — Notion de l'information génétique (`svt_ch3_notion_information_genetique`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| — | aucune diapo à tableau ; toutes les diapos (sauf bilan et carte) ont déjà une simulation qui montre leur point : noyau (amibe, acétabulaire, greffe, Gurdon), zoom (chromatine → chromosome), cycle (q → 2q, courbe), mitose (phases animale / végétale), bactéries (Griffith, Avery), ADN (construction, Chargaff, complémentaire), Meselson (expérience, prédictions), thymidine, réplication | — | Rien à construire. |
| `ig_s2_chargaff`, `ig_c5_decrire`, `ig_c6_durees`, `ig_r6_rediger` | données et méthode d'examen dans `adn.html?vue=chargaff`, `documents.html`, `meselson.html?vue=predictions` | — | Non : déjà sur simulation ; données d'examen. |

## Ch. 4 — Relation gène – protéine (`svt_ch4_relation_gene_proteine`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `rg_a1_arn` | tableau ADN / ARN (brins, sucre, bases, sortes) + `transcription.html?vue=brins` | **`adn_arn.html`** : ADN (bleu-violet, deux brins) et ARN (orange, un brin) côte à côte ; les différences apparaissent une à une sur les molécules : 2 brins / 1 brin, désoxyribose / ribose, bases A T C G / A U C G (le T attendu dans l'ARN est barré, U s'écrit à sa place), puis ARNm, ARNt, ARNr sous l'ARN. Les lignes de la comparaison s'écrivent sous chaque molécule au fil de la voix. Pas de transcription (enseignée plus tard). | **Oui** — « السطر البرتقالي » désigne le brin orange de l'ARN. |
| `rg_t2_definition` | image fixe de la transcription (étapes d'un processus) | Brancher la simulation existante `transcription.html?vue=transcription` : polymérase qui se fixe, œil, brin transcrit, nucléotides libres, ARNm qui s'allonge, chacun sur son mot. | **Oui (câblage, pas de nouveau fichier)**. La voix dit « هادي صورة ديال la transcription » : accepté (c'est bien la figure de la transcription, animée). |
| `rg_g1_gene` | image chromosome → ADN → gène | — | Non : changement d'échelle, rien qui bouge ; la voix lit l'image « de gauche à droite ». |
| `rg_o1_caracteres` | image ADN → ARNm → protéine (ouverture) | — | Non : question d'ouverture. |
| `rg_c1_codon` (4 → 16 → 64) | déjà `code_genetique.html?vue=codons` | — | Déjà animé. |
| `rg_e3_lignes`, `rg_e5_national` | méthode d'examen sur `examen.html` | — | Non : rédaction d'examen. |
| autres diapos | paire d'homologues, drépanocytose, marquage, transcription, code génétique, traduction, mutation, schéma bilan… | — | Déjà animées. |

---

## Fichiers créés

- `frontend/public/media/simulations/svt/reactions_responsables_liberation_energie-tableau/comparer.html`
  (id `svt_energie_comparer` ; curseur `set_parameters {o2: true|false}` ; moments avec O₂ : `glycolyse`, `mitochondrie`,
  `mineraux`, `rendement` ; sans O₂ : `glycolyse`, `rendement`, `residu` ; repères `glucose`, `hyaloplasme`,
  `mitochondrie`, `atp`, `mineraux`, `rendement`, `residu`, `colonne_respiration`, `colonne_fermentation`, `comparaison`).
- `frontend/public/media/simulations/svt/role_muscle_strie_squelettique-tableau/consommation.html`
  (id `muscle_tableau_consommation` ; moments `repos`, `activite`, `apres` ; repères `muscle`, `glycogene`, `o2`, `co2`,
  `lactique`, `atp`, `pc`).
- `frontend/public/media/simulations/svt/role_muscle_strie_squelettique-tableau/inhibiteurs.html`
  (id `muscle_tableau_inhibiteurs` ; moments `depart`, `atp_epuise`, `pc_basse`, `arret_glycolyse`, `fin` ; repères
  `temoin`, `glycolyse`, `double` et `<ligne>_atp`, `<ligne>_pc`).
- `frontend/public/media/simulations/svt/relation_gene_proteine-tableau/adn_arn.html`
  (id `genetique_tableau_adn_arn` ; moments `brins`, `sucre`, `bases`, `sortes` ; repères `adn`, `arn`, `adn_brins`,
  `arn_brin`, `sucre_adn`, `sucre_arn`, `bases_adn`, `bases_arn`, `uracile`, `sortes`, `comparaison`).

Toutes : cadre 760 × 420, kit `shared/tableau` + `commun.js` du cours, fond transparent, un bouton principal,
`pause` / `resume` / `reset` / `play_until`, `ce_qui_se_voit` dans l'état, script `explication`, libellés en français.

## Diapos modifiées (seulement `visual`, `screen_content`, `concentration`)

- `svt_ch1…json` — `le_r3_comparer` : visuel → `comparer.html` ; tableau et les deux puces qui le répétaient retirés
  (gardées : le calcul du rendement de la fermentation et la phrase sur le résidu) ; `pointage` réécrit
  (`set_parameters o2` + `play_until` sur « دابا la fermentation » et « أما la respiration ») ; `demarrer` retiré
  (l'essai est lancé par la voix) ; `centre` gardé.
- `svt_ch2…json` — `ms_t4_consomme` et `ms_r8_inhibiteurs` : visuel `none` → simulation ; tableau et puces retirés
  (lead et trace gardés) ; `pointage` `ligne:N` → repères de la simulation.
- `svt_ch4…json` — `rg_a1_arn` : visuel → `adn_arn.html` ; tableau et puces retirés ; `demarrer` retiré ;
  `pointage` réécrit. `rg_t2_definition` : image → `transcription.html?vue=transcription`, `pointage` réécrit.

Vérifications : chaque `mot` est un extrait exact (et unique) de `speech_text.mixed` ; `speech_text` et `audio`
identiques avant/après ; diff JSON : seules ces diapos changent ; scripts vérifiés par `node --check` ; chaque animation
jouée en navigateur sans tête (Chromium) avec ses `play_until` / `set_parameters` : rendu dans le cadre
(`__horsCadre` vide), aucune erreur de script.

Reste à faire (hors de ce lot) : `python preparer_reponses.py verifier` sur les trois cours, puis écoute dans le
lecteur, voix visible, pour régler finement les instants (la voix n'a pas été rejouée ici).
