# Architecture — `phys_ch5_energie_nucleaire` (Noyaux, masse et énergie)

Refaite le 18 novembre 2026 avec la skill `logique-de-cours`. Version en attente :
`backend/data/courses/en_attente/phys_ch5_energie_nucleaire.json`, construite par
`scripts/voix/logique_ch5_energie_nucleaire.py` à partir du cours en ligne (inchangé). Pistes à mettre en voix :
`phys_ch5_energie_nucleaire_voix.json` (77 pistes après la 2ᵉ passe, § 8).

## 1. La logique d'avant, et ce qui n'allait pas

Ordre d'avant (48 diapositives, 5 séances) : le Soleil perd de la masse → rappels (énergie, puissances de dix) →
E = m·c² → u, eV, MeV, 1 u = 931,5 MeV/c² → composition du noyau (fin de séance 1) → balance, défaut de masse →
énergie de liaison → E_ℓ/A, stabilité → Aston → spontanée/provoquée, fission, chaîne, **applications et dangers**,
rappel des charges, fusion, Soddy → énergie libérée par les masses → par les énergies de liaison → échantillon →
cas types → bilan.

L'ordre des notions suivait déjà l'ordre commun. Les défauts étaient dans la **manière** :

| Diapositive | Défaut | Règle |
|---|---|---|
| `en_l3_calcul`, `en_s2_piege`, `en_a3_comparer`, `en_b5_beta`, `en_e4_polonium`, `en_c2_qcm2019` | la voix fait tout le calcul (ou dit « le fer est plus stable », « le tritium est plus stable »), **puis** pose au tableau la question dont elle vient de dire la réponse | logique 3, professeur 33 |
| `en_b3_fusion_calcul` (2016 N), `en_e3_2023` (2023 N) | exercice du national entièrement fait par la voix, sans aucun tableau : l'élève regarde | logique 5, professeur 41 |
| ces huit diapositives | `demarrer: start` : la scène courait seule et écrivait les résultats (points de lecture, flèche ΔE, « résultat ») avant l'élève | professeur 39 |
| `en_r3b_applications_dangers` | coupait la suite fission → réaction en chaîne → **fusion** (posée entre la chaîne et le rappel des charges) | logique 7 (une idée à la fois, une suite qui se tient) |
| `en_d1_composition` | rappel de la composition placé en fin de séance 1, une séance avant la balance qui s'en sert | logique 6 (prérequis juste avant son usage) |
| 4 réactions préparées | « 1,77·10²⁰ », « 0,97 », « 185 MeV », « ⁵⁶Ni / ⁶⁰Ni » en chiffres et symboles : la voix ne les lit pas | voix-du-cours § 1 |

## 2. Les sources comparées

- **Les dix profs de l'exploration** (`exploration/energie_nucleaire.json`, convergences) : Δm (10/10), E_ℓ = Δm·c²
  avec 1 u·c² = 931,5 MeV, u gardé puis remplacé (10/10, 8/10), E_ℓ/A et stabilité (10/10), bilan par les masses
  (10/10), par les E_ℓ (9/10), diagramme à trois niveaux (8/10), Aston (7/10), échantillon (7/10).
- **Quatre cours écrits en ligne** lus le
  18/11 (Ismaili-alaoui, kezakoo.com ; El Goufifa, AlloSchool séance 7 ; El Founani, AlloSchool LaTeX ; Moutamadris,
  cours BIOF). Ordre commun : E = m·c² → unités (u, eV/MeV, 1 u = 931,5 MeV/c²) → défaut de masse → E_ℓ → E_ℓ/A →
  Aston → fission → fusion → bilan ΔE par les masses puis par les E_ℓ → diagramme énergétique → applications
  (désintégration spontanée, fission, fusion, échantillon). Variantes : Aston après fission/fusion (El Founani) ;
  perte de masse concrète avant E = m·c² (El Goufifa — c'est notre ouverture par le Soleil) ; radioprotection à la
  fin (El Goufifa, Moutamadris). Calcul type commun : défaut de masse et E_ℓ d'un noyau (C14, deutérium, U235).
- **Le cadre** (`cadre_reference_2bac_pc.json`, `energie_nucleaire`, EN1-EN9) : chaque compétence garde ses
  `cadre_ids` ; aucune notion ajoutée.
- **Le national** : énergie libérée par les masses (2016 N, 2017 R, 2022 N), par les E_ℓ (2019 N, 2023 N), diagramme
  (2020 N), défaut de masse (2022 R), échantillon (2025 N), stabilité par E_ℓ/A (2017, 2023 N). Ce sont les
  diapositives jouées en étapes.

## 3. Les décisions et leurs raisons

1. **On garde l'ordre des notions** : il est déjà l'ordre commun des profs et des quatre cours écrits (l'élève le
   retrouve chez son prof). On ne déplace que deux diapositives.
2. **La voix pose, l'élève calcule** (logique 3 et 5). Sur les huit diapositives de calcul, la voix lit les données
   et nomme la méthode (la relation, « les produits moins les réactifs », « arrivée moins départ », « multiplie par
   A »), puis s'arrête : « دابا نتا ». Le tableau « À toi » donne **une étape à la fois** ; chaque réponse a sa réaction
   préparée, chaque étape sa démonstration écrite comme le barème la lit (relation, application numérique, résultat
   avec l'unité dite en mots : « méga électron volt »).
   - `en_l3_calcul` : le modèle (relation, 1 u·c² = 931,5 MeV, les c² se simplifient) puis l'élève fait la
     multiplication (question déjà là, sa voix et ses réactions restent).
   - `en_s2_piege` et `en_a3_comparer` : les E_ℓ sont données, « la stabilité se lit sur E_ℓ/A », l'élève divise et
     compare (questions existantes, gardées). La courbe d'Aston s'arrête sur `courbe_tracee` : les points de lecture
     (qui écrivent E_ℓ/A) ne sont plus montrés avant la réponse.
   - `en_b3_fusion_calcul` (2016 N) : 3 étapes nouvelles — Δm (piège : oublier le neutron), ΔE en MeV (piège :
     u × c² en m²/s²), E_lib = |ΔE| (piège : « la masse se conserve »).
   - `en_b5_beta` (2017 R) : la voix prévient « l'électron a une masse, il entre dans Δm » ; l'élève calcule (question
     et exercice 2022 N gardés).
   - `en_e3_2023` (2023 N) : 2 étapes nouvelles — ΔE = ΣE_ℓ(réactifs) − ΣE_ℓ(produits) (pièges : ordre inversé, tout
     additionner), puis E_lib comparée aux 17,6 MeV trouvés par les masses (deux méthodes, la même énergie).
   - `en_e4_polonium` (2020 N) : la voix lit les trois paliers, la règle « arrivée moins départ » et le piège du
     facteur 10⁵ ; le diagramme s'arrête sur le palier des produits ; l'élève calcule E_lib, puis Δm en kg.
   - `en_c2_qcm2019` (2019 N) : étape 1 nouvelle (E_ℓ = A·(E_ℓ/A) pour le radon), étape 2 l'ancienne question
     (énergie libérée ; le piège 7,11 MeV reste dans les choix).
3. **Les scènes s'ouvrent figées** (`demarrer: reset`) sur ces huit diapositives : la voix pilote, rien n'est écrit
   avant son mot ni avant la réponse de l'élève (professeur 39 ; le vérificateur de pointage ne signale plus de
   « DEPART » sur ces huit diapositives ; les 36 autres sont corrigées au § 9).
4. **`en_d1_composition` ouvre la séance 2**, juste avant la balance qui compte protons et neutrons (logique 6).
5. **`en_r3b_applications_dangers` va après l'échantillon** (`en_n3_2025`), au début du bloc des cas types :
   fission → réaction en chaîne → charges → fusion → équation se suivent sans coupure ; les dangers et la protection
   (EN9) viennent quand l'élève sait d'où vient l'énergie et combien elle vaut (comme la radioprotection en fin de
   cours chez El Goufifa et Moutamadris).
6. **Les blocs « exercices du national joués »** (séance 4, blocs 2 et 3) : les tableaux s'y suivent
   (`en_b3_fusion_calcul` → `en_b5_beta` ; `en_e3_2023` → `en_e4_polonium`), parce que chaque diapositive y est un
   exercice d'examen. `en_b4_fission_calcul` (la fission faite par le prof, pas au national) passe avant 2016 N :
   l'élève voit une fois la méthode entière, puis la fait seul.

## 4. Séances, blocs et diapositives — pourquoi ici

Légende : ✏️ tableau « À toi » ; 🪜 exercice joué en étapes ; ✍️ texte réécrit (voix à refaire) ; ↕ déplacée.

### Séance 1 — Les outils, puis E = m·c²
- **B0** `en_m1_soleil` (la masse qui devient énergie : le phénomène avant la formule) → `en_p1_energie` (départ de zéro : l'énergie, le joule) → `en_p2_puissances` ✏️ (outil juste avant c = 3·10⁸).
- **B1** `en_m2_einstein` → `en_m2b_un_gramme` ✏️ (ordre de grandeur, ΔE = Δm·c²) → `en_m3_unites` (u, avec la mole rappelée en une phrase).
- **B1b** `en_m3b_electronvolt` (« méga électron volt » dit en mots) → `en_m4_931` ✏️ (1 u = 931,5 MeV/c² établi) → `en_m4b_energie_masse`.

### Séance 2 — Défaut de masse, énergie de liaison, stabilité
- **B2** `en_d1_composition` ↕ (rappel au moment où il sert) → `en_d2_balance` (on pèse : le noyau est plus léger, vu avant d'être nommé) → `en_d3_formule` (Δm défini, relu, calculé une fois par le prof sur l'hélium) → `en_d4_carbone` ✏️ (national 2022 R : la voix donne la composition, l'élève calcule Δm).
- **B3** `en_l1_separer` (fournir E_ℓ, vu) → `en_l2_former` (E_ℓ = Δm·c² démontré par les énergies de masse) → `en_l3_calcul` ✍️ ✏️ (le modèle, puis l'élève multiplie).
- **B4** `en_l4_par_nucleon` (E_ℓ/A) → `en_s1_stabilite` (la règle sur 2017) → `en_s2_piege` ✍️ ✏️ (l'élève tombe ou non dans le piège E_ℓ, avant la courbe).

### Séance 3 — La courbe d'Aston, la fission, la fusion
- **B1** `en_a1_courbe` → `en_a2_zones` (fusion à gauche) → `en_a2b_fission` (fission à droite) → `en_a3_comparer` ✍️ ✏️ (2023 N : l'élève divise et compare).
- **B2** `en_r1_spontanee` (rappel du chapitre 4, puis provoquée) → `en_r2_fission` → `en_r3_chaine` ✏️.
- **B3** `en_p3_charges` (rappel juste avant la fusion : pourquoi il faut chauffer) → `en_r4_fusion` → `en_r5_soddy` ✏️.

### Séance 4 — L'énergie libérée
- **B1** `en_b1_masse_diminue` (la balance, vue) → `en_b2_methode` → `en_b2b_energie` ✏️ (signe de ΔE).
- **B2 (exercices du national joués)** `en_b4_fission_calcul` ↕ (méthode entière faite par le prof, une fois) → `en_b3_fusion_calcul` ✍️ 🪜 (2016 N, 3 étapes) → `en_b5_beta` ✍️ ✏️ (2017 R puis 2022 N).
- **B3 (exercices du national joués)** `en_e1_diagramme` → `en_e2_formule` (ΔE par les E_ℓ démontré) → `en_e3_2023` ✍️ 🪜 (2 étapes) → `en_e4_polonium` ✍️ ✏️ (2020 N : E_lib, puis Δm en kg).

### Séance 5 — L'échantillon, les dangers, les cas types et le bilan
- **B1** `en_n1_echantillon` (la mole, le paquet) → `en_n1b_energie_totale` → `en_n2_comparaison` (fission ou fusion) → `en_n3_2025` ✏️ (lié au chapitre 4).
- **B2** `en_r3b_applications_dangers` ↕ (EN9 : pénétration α, β, γ ; protection) → `en_c1_cas_types` → `en_c2_qcm2019` ✍️ 🪜 (2 étapes).
- **B3** `en_z1_bilan` → `en_z2_carte`.

## 5. Ce qui reste comme avant, et pourquoi
- 40 diapositives sur 48 gardent texte et voix ; l'ordre des notions est celui des profs et des cours écrits.
- Les ouvertures concrètes (Soleil, balance, séparer/former) restent avant chaque formule : c'est déjà « la chose vue
  d'abord » (logique 4).
- `en_n3_2025` garde sa voix : elle rappelle l'énergie d'un noyau (étape précédente de l'énoncé) et l'élève fait
  l'étape suivante (N noyaux).

## 6. Pistes à mettre en voix (voir `phys_ch5_energie_nucleaire_voix.json`)
8 diapositives réécrites, 6 démonstrations, 40 réactions et énoncés. Mot rare gardé exprès : « méga » (0 fois dans le
corpus de la voix ; c'est l'unité que l'élève doit entendre, « méga électron volt », et `texte_parle.py` lit déjà
« MeV » ainsi) — **à écouter en priorité** (skill prononciation). Gardés aussi : deutérium, tritium, polonium, radon
(termes des énoncés).

## 7. Ce qui n'a pas pu être fait ici
- Rejouer les diapositives dans le navigateur (`verifier-pointage-navigateur.mjs`) : à faire quand les voix seront
  posées (sans piste, le vérificateur estime les instants et signale des gestes « trop serrés » qui viennent de
  l'absence d'audio).
- Les voix : sur le VPS (quota Kaggle épuisé jusqu'à samedi).

## 8. 2ᵉ passe (18 novembre 2026) : les exercices du national joués, rien de décisif avant la réponse

**Ce que l'évaluation de la 1ʳᵉ passe a relevé.** Les questions étaient bien coupées en étapes, mais cinq exercices du
national restaient des **énoncés fixes** lus sur `figures.html?fig=fig_enonce_*` (2016 N, 2017 R, 2023 N, 2025 N) ou sur
la fiche de méthode (`fig_methode_liaison`, 2019 N) : rien ne bougeait, l'élève lisait un tableau. Au 2025 N, la voix
donnait encore le résultat d'un noyau (0,402 MeV) et l'élève ne faisait que la dernière multiplication ; au 2022 R
(`en_d4_carbone`), la balance écrivait la somme 14,11296 u puis Δm = 0,11301 u **avant** la question.

**Nouvelle page `energie-nucleaire-tableau/national.html`** (une vue par sujet, valeurs du sujet) — pourquoi : professeur
règles 33, 37, 41, 42 ; simulations-au-tableau règle 14. Pour chaque sujet : l'équation s'écrit (`equation`), les noyaux
peints réagissent sous les yeux de l'élève (`noyaux`, `reaction` : les réactifs restent à leur place, pâlis, règle 13),
chaque donnée se pose **sous le noyau qu'elle décrit** (`donnees` : la masse, l'énergie de liaison ou E_ℓ/A là où elle
sert, au lieu d'un encadré « Données » à lire), puis les étapes s'écrivent avec un « ? » rose à la place de chaque
résultat (`etapes`). Les résultats n'existent qu'aux moments `rep_1…rep_3`, que la voix de la diapositive ne joue jamais :
ils servent au cycle de reprise, après la réponse de l'élève ; le bouton Lancer s'arrête aussi sur `etapes`. Vues :
`fusion_2016`, `cobalt_2017`, `liaison_2023`, `radon_2019`, `cadmium_2025` (l'échantillon : N_d noyaux pères violets
deviennent fils gris avec un petit éclair, comme `population.html` du chapitre 4).
Un objet, un dessin (professeur 43) : protons rouges et neutrons gris-bleu de `balance.html` / `figures.html`, électron bleu
et positon ambré de `desintegration.html` (chapitre 4). Vérifié dans Chromium à 724 × 350, 1024 × 560 et 1280 × 560 :
aucune erreur, chaque moment atteint, « ? » tant que `rep_k` n'est pas joué, rien sous la barre du lecteur.

| Diapositive | Avant | Après (et pourquoi) |
|---|---|---|
| `en_b3_fusion_calcul` (2016 N) | énoncé fixe | `national.html?vue=fusion_2016` ; voix réécrite sur les quatre moments ; les trois étapes au tableau inchangées |
| `en_b5_beta` (2017 R) | énoncé fixe ; une seule question (E_lib) faisait tout le calcul | vue `cobalt_2017` ; **étape 1 nouvelle** Δm (pièges : oublier l'électron −0,00358 u, le signe) puis étape 2 E_lib (l'ancienne question, ses réactions voisées gardées) ; l'iode 131 (2022 N) va en `exercices_fin_de_cours` (une ardoise par bloc) |
| `en_e3_2023` (2023 N) | tableau d'E_ℓ fixe | vue `liaison_2023` : chaque E_ℓ sous son noyau, « le neutron seul : 0 » ; étapes inchangées |
| `en_c2_qcm2019` (2019 N) | fiche de méthode générale | vue `radon_2019` : E_ℓ/A sous chaque noyau, étape 1 « 222 × 7,69 = ? » |
| `en_n3_2025` (2025 N) | la voix donnait 0,402 MeV ; une étape pour l'élève ; « combien » dans l'énoncé dit | vue `cadmium_2025` ; voix réécrite sans aucun résultat ; **trois étapes** : Δm avec le positon (nouvelle), E_lib d'un noyau (nouvelle, pièges 0,913 MeV sans positon et 4,314·10⁻⁴ MeV sans × 931,49), E = N_d·E_lib (l'ancienne question, réactions voisées gardées, énoncé dit réécrit) ; l'uranium en joule va en fin de cours |
| `en_d4_carbone` (2022 R) | la balance écrivait la somme puis Δm avant la question | `balance.html?…&somme=0` (paramètre nouveau, absent = comme avant : le cours en ligne ne change pas) : la colonne pose « 6 × 1,00728 + 8 × 1,00866 = ? » ; le pointage s'arrête sur `balance_penche` au lieu de `delta_m`. **Voix gardée** (le texte ne change pas) |

Le `centre` des cinq diapositives jouées est retiré : la simulation écrit déjà la relation de chaque étape (l'écran ne
répète pas ce que l'animation montre, professeur 42). Toutes les réactions des étapes nouvelles sont écrites (juste /
indice / réponse), chaque étape a sa démonstration écrite comme le barème la lit (relation, application numérique,
résultat avec l'unité dite en mots).

**Mots** (`verifier_mots.py en_attente/phys_ch5_energie_nucleaire <pistes>`) : remplacés « نسيتيش » → « حسبتي حتى »,
« légers » → « la masse des produits أصغر من… », « عطاش » → « ما فيهش… فيه », « استعملتي » → « ديالك », « combien » →
« شحال ». Gardés (termes du programme ou des énoncés, à écouter en priorité) : méga, positon, deutérium, tritium,
neutron, polonium, radon, et les nombres des sujets (soixante-deux, quatre-vingt-seize…).

**Vérifications** : JSON chargé ; chaque `mot` de pointage et de démonstration trouvé ; chaque réaction couvre toutes les
options ; `verifier_pointage_simulations.py` : aucun « introuvable » (copie en attente et cours en ligne ; le cours en
ligne donne exactement le même rapport qu'avant) ; il signale 11 « GESTE trop serrés » nouveaux, faux écarts dus à
l'absence de piste (sans durée, tous les gestes tombent à 0 s) ; un « DEPART » en moins (`en_n3_2025` ouvre figée) ;
`verifier_formules.py` : rien sur le cours, rien sur `national.html` ; pytest « course or cours or concentration » :
88 passés, 1 échec SVT préexistant.

**Ce qui reste.** Les voix (77 pistes, VPS) ; rejouer les cinq diapositives dans le lecteur avec leur voix
(`verifier-pointage-navigateur.mjs`) ; les anciennes figures `fig_enonce_2016/2017/2023/2025` restent dans `figures.html`
(le cours en ligne s'en sert) et seront retirées quand la copie en attente le remplacera. Le lexique visuel commun
(`docs/lexique-visuel/`, `shared/lexique/`) n'existe pas encore dans le dépôt : proton, neutron, électron et positon y
seront à inscrire (fichiers partagés, hors de cette passe) ; les teintes du proton diffèrent légèrement entre ce cours
(`#d9534f`) et `population.html` du chapitre 4 (`#f06a3a`) : à unifier par le lexique.

## 9. Toutes les scènes s'ouvrent figées (18 novembre 2026, demande de l'utilisateur)

- **Le défaut trouvé** : dans les pages du chapitre (`figures`, `rappels`, `aston`, `balance`, `diagramme`, `liaison`,
  `reactions` de `energie-nucleaire-tableau/`), `reset` n'était qu'un autre nom de `start`, et chaque page démarrait
  seule au chargement. Une diapositive en `demarrer: reset` courait donc quand même seule, devant la voix — y compris
  les huit du § 3. Écrire `reset` dans le cours ne suffisait pas.
- **La correction des pages** : `reset` fige maintenant la scène, à zéro ou sur `?depart=<moment>` (tout ce qui
  précède déjà écrit) ; une page ouverte avec `?depart=` se fige dès son chargement ; ensuite seule la voix la fait
  avancer (`play_until`). `start` ne change pas : les cours en ligne, tous en `start`, gardent leur comportement.
  Vérifié dans Chromium (10 cas : figée 1,5 s sans bouger, puis arrêtée sur le moment demandé, aucune erreur JS).
- **Le cours** : les 36 diapositives restées en `demarrer: start` passent en `reset` (leurs textes et voix ne changent
  pas). Six reprenaient la page de la diapositive précédente (même URL : la scène n'était pas rechargée) ; elles
  s'ouvrent maintenant figées là où la précédente s'est arrêtée : `en_m2b_un_gramme` (`&depart=termes`),
  `en_m3b_electronvolt` (`u`), `en_a2_zones` (`plus_stable`), `en_a2b_fission` (`zone_fusion`), `en_b2b_energie`
  (`delta_m`), `en_n1b_energie_totale` (`nombre`).
- **Résultat** : `verifier_pointage_simulations.py` ne signale plus aucun « DEPART » ni « IFRAME » sur ce chapitre
  (il reste 14 « gestes trop serrés », dus aux pistes pas encore enregistrées, plus un sur `en_n2_comparaison`).
  Rejouées avec la minuterie du lecteur (`verifier-pointage-navigateur.mjs`) : chaque moment des diapositives reprises
  est atteint sur son mot. L'écart de `en_r2_fission` (la voix dit sept étapes plus vite que la scène) existait déjà
  dans le cours en ligne.
- **À savoir** : quatre diapositives ont leur premier `play_until` après le premier quart de la voix (`en_d4_carbone`,
  `en_l1_separer`, `en_l4_par_nucleon`, `en_e4_polonium`) ; d'ici là la scène montre son état de départ (balance vide,
  noyau au repos, paliers vides).

