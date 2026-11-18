# Architecture — `phys_ch5_energie_nucleaire` (Noyaux, masse et énergie)

Refaite le 18 novembre 2026 avec la skill `logique-de-cours`. Version en attente :
`backend/data/courses/en_attente/phys_ch5_energie_nucleaire.json`, construite par
`scripts/voix/logique_ch5_energie_nucleaire.py` à partir du cours en ligne (inchangé). Pistes à mettre en voix :
`phys_ch5_energie_nucleaire_voix.json` (54 pistes).

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
   « DEPART » sur ces huit diapositives ; les autres diapositives du chapitre, non touchées, en gardent 36 : à
   reprendre quand leurs voix seront refaites, chaque changement de `demarrer` demandant de rejouer la diapositive).
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
