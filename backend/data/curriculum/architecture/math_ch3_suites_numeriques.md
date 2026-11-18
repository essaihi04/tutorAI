# Architecture — Suites numériques (`math_ch3_suites_numeriques`)

Skill `logique-de-cours`, 18 novembre 2026. Cours en ligne inchangé ; nouvelle version :
`backend/data/courses/en_attente/math_ch3_suites_numeriques.json`, produite par `scripts/logique/ch3_suites.py`
(rejouable) et `scripts/logique/reordonner.py`. Exploration : `exploration/suites_definition.json`.

## La logique avant

Séance 1 ouverte par cinq rappels (puissances, ordre gardé, ordre inversé, signe d'une différence, même dénominateur)
→ suites, arithmétique, géométrique, sommes → récurrence → bornée, sens de variation → suite auxiliaire → limites
(nᵅ, qⁿ, opérations, fraction, f(uₙ)) → convergence et comparaison → uₙ₊₁ = f(uₙ) → rang, somme → un exercice national
complet en **une** diapositive (les cinq questions dites avec leurs réponses, une question finale) → bilan.

Défauts : les rappels 2 à 5 servent dans la récurrence, 40 à 60 minutes plus tard ; l'exercice national, qui
rassemble les cas les plus fréquents (récurrence avec fraction 10/20, convergence monotone bornée 17/20, suite
auxiliaire géométrique 8/20, limite par qⁿ 10/20), était lu et non joué.

## Les sources

- **Exploration** et **cas types** : voir ci-dessus ; uₙ₊₁ = f(uₙ) et ℓ = f(ℓ) 10/20 ; majoration kⁿ 3/20.
- **Cours écrits** : Benmoussa (Moutamadris, AlloSchool 100300), Cheddadi (AlloSchool 122864), Atmani (Moutamadris),
  fiche Atlasmaths ; livre du Prof Fayssal (`docs/audit-prof/maths.md`). **Ordre commun** : rappels (bornée,
  monotone, arithmétique, géométrique, récurrence) → limite, convergence → opérations → comparaison, monotone bornée →
  qⁿ et nʳ → f(uₙ) → uₙ₊₁ = f(uₙ). Les rappels sont toujours en tête ; la récurrence est intégrée aux exemples
  (Atlas en fait une section, comme nous).
- **Le cadre** : `perimetre.json`, suites_definition (1.1.1, 1.1.5) et suite_dans_probleme (1.1.3, 1.1.4).

## Les grandes décisions

1. **Les rappels au moment où ils servent** (règle 6) : les puissances devant la suite géométrique ; le sens d'une
   inégalité devant l'hérédité affine ; le signe d'une différence et le même dénominateur devant l'hérédité avec une
   fraction. Une voix à refaire pour la liaison (`su_r4_heredite_fraction`).
2. **L'ordre des profs est gardé** : suites et rappels → récurrence → bornée et monotone → (suite auxiliaire) →
   limites → convergence → uₙ₊₁ = f(uₙ). La suite auxiliaire reste avant les limites : au national elle mène à uₙ en
   fonction de n, puis à la limite par qⁿ, dans cet ordre.
3. **L'exercice du national 2024 joué question par question** : cinq diapositives, chacune une question posée avant
   sa correction, chacune écrite à la craie ligne par ligne, la convergence sur l'animation des deux bons couples.
   Exception écrite à « un seul À toi par bloc » pour ce bloc (règle 41, demande du 18 novembre).
4. **La suite du problème uₙ₊₁ = g(uₙ) en deux étapes** (10 sujets sur 20 : signe de f(x) − x et ℓ = f(ℓ)) :
   le sens de variation, puis la convergence et la limite, chacune avant sa correction, sur l'escalier animé.
5. **Rien retiré** : aucune diapositive hors cadre.

## L'architecture, diapositive par diapositive

76 diapositives, 7 séances, 23 blocs, durée prévue 210 min. « ✏️ » : la diapositive porte le « À toi » du bloc ; « 🔊 » : sa voix est gardée ; « 🆕 voix » : à enregistrer.

### Séance 1 — Une suite ; arithmétique et géométrique

**La carte ; une liste numérotée ; uₙ₊₁ n'est pas uₙ + 1** (`su_n1_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_o1_questions` | La carte du chapitre : une liste de nombres et cinq questions | 🔊 | La carte : une liste de nombres et cinq questions ; l'élève sait où va le chapitre. |
| `su_a1_liste` | Une suite, c'est une liste numérotée | 🔊 | Une suite = une liste numérotée : le départ de zéro (rappels en tête chez tous les cours écrits). |
| `su_a2_indice` | uₙ₊₁ n'est pas uₙ + 1 | ✏️ 🔊 | Le piège uₙ₊₁ ≠ uₙ + 1, tout de suite ; l'élève répond. |

**Par une formule, par récurrence ; suite arithmétique** (`su_n1_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_a3_termes` | Une suite donnée par une formule en n | 🔊 | Suite donnée par une formule en n : calculer des termes (2020 N, 2021 N). |
| `su_a3b_recurrence` | Une suite par récurrence : la machine | 🔊 | Suite par récurrence : la machine, avant la notion de récurrence. |
| `su_a4_arithmetique` | Suite arithmétique : on ajoute toujours la même chose | 🔊 | Arithmétique vue sur l'axe (sauts égaux) avant la formule. |
| `su_a5_terme_arith` | Le terme général d'une suite arithmétique | ✏️ 🔊 | Son terme général ; l'élève calcule. |

**Les puissances ; suite géométrique** (`su_n1_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_z1_puissances` | Rappel : les puissances | 🔊 | DÉPLACÉ (était en séance 0) : les puissances rappelées juste avant la suite géométrique qui en a besoin. |
| `su_a6_geometrique` | Suite géométrique : on multiplie toujours par le même nombre | 🔊 | Géométrique vue sur l'axe (on multiplie) avant la formule. |
| `su_a7_terme_geo` | Le terme général d'une suite géométrique | 🔊 | Son terme général u₀·qⁿ. |

**Nombre de termes ; les deux sommes** (`su_n1_b4`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_a8_nombre_termes` | Combien de termes dans une somme ? | 🔊 | Le nombre de termes, prérequis des deux sommes. |
| `su_a9_sommes` | La somme arithmétique | 🔊 | La somme arithmétique (2022 R, 2023 R). |
| `su_a9b_somme_geo` | La somme géométrique | ✏️ 🔊 | La somme géométrique ; l'élève calcule. |

### Séance 2 — Le raisonnement par récurrence

**Les dominos ; l'annonce, l'initialisation, l'hérédité** (`su_n2_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_r1_dominos` | Les dominos : le principe de récurrence | 🔊 | Le principe de récurrence avec les dominos (10 sujets sur 20 font une récurrence avec fraction). |
| `su_r2_trois_titres` | Les trois titres d'une récurrence : l'annonce et l'initialisation | 🔊 | L'annonce et l'initialisation. |
| `su_r2b_heredite` | Hérédité : supposer pour UN n, montrer au rang n + 1 | 🔊 | L'hérédité : supposer pour un n. |

**La conclusion ; le sens d'une inégalité** (`su_n2_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_r2c_conclusion` | Conclusion, et la phrase interdite | 🔊 | La conclusion et la phrase interdite. |
| `su_z2_ordre_garde` | Rappel : ce qui garde le sens d'une inégalité | 🔊 | DÉPLACÉ : ce qui garde le sens d'une inégalité, juste avant l'hérédité affine qui fait ces opérations. |
| `su_z3_ordre_inverse` | Rappel : ce qui change le sens d'une inégalité | ✏️ 🔊 | DÉPLACÉ : ce qui inverse le sens ; l'élève répond (sa question est l'À toi du bloc). |

**Hérédité affine ; comparer par la différence ; même dénominateur** (`su_n2_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_r3_heredite_affine` | Hérédité affine : on fait à l'inégalité ce que la formule fait à uₙ | 🔊 | Hérédité affine : on fait à l'inégalité ce que la formule fait à uₙ (2016 R, 2017 R). |
| `su_z4_difference` | Rappel : comparer avec le signe de la différence | 🔊 | DÉPLACÉ : comparer par le signe de la différence, juste avant l'hérédité avec une fraction qui l'utilise. |
| `su_z5_denominateur` | Rappel : le même dénominateur | 🔊 | DÉPLACÉ : le même dénominateur, juste avant le calcul de l'hérédité avec une fraction. |

**Hérédité avec une fraction ; choisir sa méthode** (`su_n2_b4`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_r4_heredite_fraction` | Hérédité avec une fraction : pourquoi ça bloque, et l'idée | 🆕 voix | Hérédité avec une fraction : pourquoi ça bloque ; voix réécrite (« la règle qu'on vient de voir » au lieu de « vue au début », et trois mots rares remplacés). |
| `su_r4b_calcul` | Le calcul : même dénominateur, puis deux signes | ✏️ 🔊 | Le calcul : même dénominateur, deux signes ; l'élève répond. |
| `su_r5_choisir` | Choisir sa méthode d'hérédité | 🔊 | Choisir sa méthode d'hérédité. |

### Séance 3 — Récurrence du national ; bornée ; sens de variation

**L'écriture donnée ; strict ou large ; une récurrence du national** (`su_n3_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_r6_ecriture_donnee` | Encadrement avec l'écriture donnée par l'énoncé | 🔊 | Avec l'écriture donnée par l'énoncé (8 sujets : vérifier une égalité). |
| `su_r7_strict_large` | Strict ou large : ce que la conclusion doit dire | 🔊 | Strict ou large dans la conclusion. |
| `su_r8_national` | À toi : une récurrence du national | ✏️ 🔊 | Une récurrence du national faite par l'élève. |

**Majorée, minorée, bornée ; croissante pour tout n** (`su_n3_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_b1_plancher` | Majorée, minorée : un plafond, un plancher | 🔊 | Majorée, minorée : plafond et plancher. |
| `su_b2_bornee` | Bornée : coincée entre deux | 🔊 | Bornée. |
| `su_m1_pour_tout_n` | Croissante, décroissante : pour tout n | ✏️ 🔊 | Croissante pour tout n ; l'élève répond. |

**Le sens de variation : différence et quotient** (`su_s3_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_m2_difference` | Outil 1 : le signe de uₙ₊₁ − uₙ | 🔊 | Outil 1 : signe de uₙ₊₁ − uₙ (7 sujets). |
| `su_m3_egalite_donnee` | Outil 1 avec une égalité donnée | 🔊 | Avec l'égalité donnée. |
| `su_m4_quotient` | Outil 2 : le quotient, si les termes sont positifs | ✏️ 🔊 | Outil 2 : le quotient (1 sujet) ; l'élève répond. |

### Séance 4 — La suite auxiliaire ; les limites de référence

**Montrer qu'une suite auxiliaire est géométrique** (`su_s3_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_x1_pourquoi` | Pourquoi une suite auxiliaire ? | 🔊 | Pourquoi une suite auxiliaire (8 sujets géométrique, 3 arithmétique). |
| `su_x2_geometrique` | Montrer que vₙ est géométrique | 🔊 | Montrer que vₙ est géométrique. |
| `su_x3_fraction` | Une suite auxiliaire en fraction | ✏️ 🔊 | Suite auxiliaire en fraction ; l'élève répond. |

**Revenir à uₙ ; une suite qui se rapproche d'un nombre** (`su_s3_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_x4_retour` | De vₙ à uₙ : le cas simple | 🔊 | De vₙ à uₙ. |
| `su_x4b_fraction` | Revenir à uₙ quand vₙ est une fraction | 🔊 | Revenir à uₙ quand vₙ est une fraction. |
| `su_x5_arithmetique` | Suite auxiliaire arithmétique | 🔊 | Suite auxiliaire arithmétique. |
| `su_l1_converge` | Une suite qui se rapproche d'un nombre | ✏️ 🔊 | Une suite qui se rapproche d'un nombre : la limite vue avant d'être définie (ordre commun : limites après les rappels). |

**Les limites de référence : nᵅ et qⁿ** (`su_s4_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_l2_reference` | Les suites de référence : nᵅ | 🔊 | Les suites de référence nᵅ. |
| `su_l3_qn_positif` | qⁿ quand q est entre 0 et 1, puis plus grand que 1 | 🔊 | qⁿ, q positif (limite par qⁿ : 10 sujets). |
| `su_l4_qn_negatif` | qⁿ quand q est négatif | 🔊 | qⁿ, q négatif : l'élève observe. |
| `su_l4c_quatre_cas` | Les quatre cas de qⁿ | ✏️ 🔊 | Les quatre cas ; l'élève répond. |

### Séance 5 — Limites d'une suite et convergence

**Limite avec qⁿ, d'une fraction en n, de f(uₙ)** (`su_s4_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_l4b_glisse_q` | Glisse q : le bon cas en un coup d'œil | 🔊 | Glisser q : le bon cas en un coup d'œil (animation manipulée). |
| `su_l5_avec_qn` | Limite d'une suite écrite avec qⁿ | 🔊 | Limite d'une suite écrite avec qⁿ. |
| `su_l5b_formes_indeterminees` | Opérations sur les limites et formes indéterminées | 🔊 | Opérations et formes indéterminées. |
| `su_l6_fraction` | Limite d'une fraction en n | 🔊 | Limite d'une fraction en n. |
| `su_l7_f_un` | La limite de f(uₙ) | ✏️ 🔊 | Limite de f(uₙ) (1 sujet) ; l'élève répond. |

**Converger : le bon couple et la comparaison** (`su_s4_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_c1_plafond` | Monter avec un plafond, c'est converger | 🔊 | Monter avec un plafond, c'est converger (17 sujets sur 20). |
| `su_c2_couple` | Le bon couple : monte + plafond, descend + plancher | 🔊 | Le bon couple. |
| `su_c3_plafond_limite` | Le plafond n'est pas forcément la limite | 🔊 | Le plafond n'est pas forcément la limite. |
| `su_c4_comparaison` | Coincée entre deux : le critère de comparaison | ✏️ 🔊 | Le critère de comparaison ; l'élève répond. |

**Chaque terme au plus k fois le précédent** (`su_s5_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_c5_deux_cinquiemes` | Chaque terme est au plus les 2/5 du précédent | 🔊 | Chaque terme au plus k fois le précédent (3 sujets). |
| `su_c6_recurrence_kn` | En déduire uₙ ≤ (3/2)(2/5)ⁿ : une récurrence courte | 🔊 | En déduire uₙ ≤ kⁿu₀ par récurrence. |
| `su_c7_conclure` | Conclure par comparaison | 🔊 | Conclure par comparaison. |
| `su_c8_ecart` | L'écart à la limite se resserre | ✏️ 🔊 | L'écart à la limite se resserre ; l'élève répond. |

### Séance 6 — La suite uₙ₊₁ = f(uₙ) ; rang et somme

**L'escalier et l'encadrement par f** (`su_s5_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_f1_escalier` | Voir les termes sur la courbe : l'escalier | 🔊 | uₙ₊₁ = f(uₙ) vue en escalier (10 sujets : point fixe). |
| `su_f2_place_u0` | La place de u₀ change l'escalier | 🔊 | La place de u₀ change l'escalier. |
| `su_f3_encadrement_f` | L'encadrement vient des variations de f | ✏️ 🔊 | L'encadrement vient des variations de f ; l'élève répond. |

**Sens de variation par f(x) − x ; les conditions ; choisir ℓ** (`su_n6_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_f4_sens_f` | Le sens de variation vient de f(x) − x | 🔊 | Le sens de variation vient de f(x) − x. |
| `su_f5_conditions` | Les conditions avant ℓ = f(ℓ) | 🔊 | Les conditions avant ℓ = f(ℓ). |
| `su_f6_choisir` | Choisir la bonne solution | 🔊 | Choisir la bonne solution. |

**La suite du problème, en deux étapes : ta réponse avant la correction** (`su_n6_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_f7_national` | À toi : la suite du problème, étape 1 — le sens de variation | ✏️ 🆕 voix | RÉÉCRIT : la suite du problème coupée en deux étapes. Étape 1 seule : le sens de variation par le signe de g(x) − x, sur l'escalier animé ; l'élève répond avant la correction. Avant, une seule question demandait « croissante, puis la limite ». |
| `su_f7_national_b` | À toi : la suite du problème, étape 2 — convergente, puis ℓ = g(ℓ) | ✏️ 🆕 voix | NOUVELLE : étape 2, convergente (croissante et majorée), les conditions de ℓ = g(ℓ) (g continue car dérivable, g(I) ⊂ I, u₀ ∈ I), puis l'élève donne la limite ; même scène que l'étape 1 (le professeur montre les deux points d'intersection). |

**Plus petit rang, somme et sa limite** (`su_s6_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_p1_rang` | À partir de quel rang ? | 🔊 | À partir de quel rang (2 sujets). |
| `su_p2_somme_mixte` | La somme d'une suite qui n'est pas géométrique | 🔊 | La somme d'une suite qui n'est pas géométrique. |
| `su_p3_limite_somme` | La limite d'une somme | ✏️ 🔊 | La limite d'une somme ; l'élève répond. |

### Séance 7 — Un exercice national, question par question ; le bilan

**National 2024 : cinq questions, ta réponse avant la correction** (`su_n8_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_e1_complet` | National 2024, question 1 : l'encadrement par récurrence | ✏️ 🆕 voix | RÉÉCRIT : l'exercice du national 2024 commence par la question 1 seule ; la voix fait l'initialisation et pose l'hérédité, l'élève donne le signe de uₙ₊₁ − 2 avant la correction. Avant, les cinq questions étaient dites avec leurs réponses. |
| `su_e1_q2` | National 2024, question 2 : le sens de variation | ✏️ 🆕 voix | NOUVELLE : question 2, le sens de variation ; uₙ₊₁ − uₙ écrit à la craie, l'élève conclut avec la question 1. |
| `su_e1_q3` | National 2024, question 3 : la convergence | ✏️ 🆕 voix | NOUVELLE : question 3, la convergence, sur l'animation des deux bons couples (décroissante et minorée). |
| `su_e1_q4` | National 2024, question 4 : la suite auxiliaire | ✏️ 🆕 voix | NOUVELLE : question 4, la suite auxiliaire ; question reprise de l'ancien exercice (réactions et démonstration gardent leur voix). |
| `su_e1_q5` | National 2024, question 5 : uₙ en fonction de n, puis la limite | ✏️ 🆕 voix | NOUVELLE : question 5, uₙ en fonction de n et la limite ; question reprise de l'ancienne (réactions et démonstration gardées). |

**Ce qu'il faut retenir ; la carte** (`su_n8_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_e2_bilan` | Ce qu'il faut retenir | 🔊 | La fiche du chapitre. |
| `su_e3_carte` | La carte du chapitre | 🔊 | La carte du chapitre. |

## Vérification des calculs de l'exercice national

- uₙ₊₁ − 2 = (4uₙ − 2 − 2uₙ − 2)/(uₙ + 1) = 2(uₙ − 2)/(uₙ + 1) ; uₙ₊₁ − 4 = −6/(uₙ + 1) ; uₙ₊₁ − 1 = 3(uₙ − 1)/(uₙ + 1).
- uₙ₊₁ − uₙ = (−uₙ² + 3uₙ − 2)/(uₙ + 1) = −(uₙ − 1)(uₙ − 2)/(uₙ + 1).
- vₙ₊₁ = (2/3)vₙ, v₀ = 2/3, vₙ = (2/3)ⁿ⁺¹, uₙ = 1 + 1/(1 − vₙ) → 2.

## Animations et exercices animés

- Questions 1, 2, 4 et 5 : quatre vues nouvelles de `calculs.html` (`e1_q1`, `e1_q2`, `e1_q4`, `e1_q5`, ajoutées à la
  main dans `calculs-vues.js` : le build `maths_build/suites_definition/build.py` n'est pas dans le dépôt ; à reporter
  dans ses sources).
- Question 3 : `plafond.html?vue=couple` (les deux bons couples), arrêtée sur « décroissante et minorée ».

## Ce qui reste à faire

- Voix : `math_ch3_suites_numeriques_voix.json` (18 pistes, dont 8 diapositives).
- Réactions préparées pour les cinq questions nouvelles (`su_e1_complet`, `su_e1_q2`, `su_e1_q3`, `su_f7_national`,
  `su_f7_national_b`).
- La suite du problème (`su_f7_national`, `su_f7_national_b`) est coupée en deux étapes, chacune posée avant sa
  correction ; ses deux questions sont nouvelles et attendent leurs réactions préparées (les anciennes réactions
  répondaient aux deux étapes à la fois). Bloc `su_n6_b3` : deux « À toi » à la suite, même exception que l'exercice
  national.
