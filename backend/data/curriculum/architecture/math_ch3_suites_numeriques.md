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
4. **Rien retiré** : aucune diapositive hors cadre.

## L'architecture, diapositive par diapositive

77 diapositives (2ᵉ passe : + `su_f7b_limite`, + `su_e1_q5a`), 7 séances, 22 blocs, durée prévue 209 min. « ✏️ » : la diapositive porte le « À toi » du bloc ; « 🔊 » : sa voix est gardée ; « 🆕 voix » : à enregistrer.

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
| `su_f3_encadrement_f` | L'encadrement vient des variations de f | ✏️ 🆕 voix | L'encadrement vient des variations de f ; l'élève répond. 2ᵉ PASSE : la voix et la scène s'arrêtent après f(1) = 1 et f(2) = 4/3 (moment `images`) ; avant, la voix disait « f(uₙ) est entre f(1) et f(2) » et la scène écrivait « x dans [1 ; 2] ⇒ f(x) dans [1 ; 4/3] » (`boite_y`) : la réponse de la question. Le principe « une fonction croissante garde l'ordre » reste dit (rappel de 1ʳᵉ année), l'application est trouvée par l'élève. |

**Sens de variation, conditions, puis ℓ = f(ℓ)** (`su_s5_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `su_f4_sens_f` | Le sens de variation vient de f(x) − x | 🔊 | Le sens de variation vient de f(x) − x. |
| `su_f5_conditions` | Les conditions avant ℓ = f(ℓ) | 🔊 | Les conditions avant ℓ = f(ℓ). |
| `su_f6_choisir` | Choisir la bonne solution | 🔊 | Choisir la bonne solution. |
| `su_f7_national` | À toi : la suite du problème du national, étape 1 : le sens de variation | ✏️ 🆕 voix | 2ᵉ PASSE, COUPÉE EN DEUX (demande de l'architecture : « croissante, puis la limite » en une question). Étape 1 seule (monotonie par f(x) − x, 10 sujets) : la courbe de g et y = x, puis g(x) − x au même dénominateur, factorisé, et un tableau de signes VIDE sur [1 ; 3] (`national.html?vue=g_signe`, arrêt `tableau`). L'élève donne le signe et le sens ; la correction remplit le tableau ligne par ligne, colore la bande où la courbe est au-dessus de la droite, puis l'escalier monte. Avant : l'escalier qui monte et le point (3 ; 3) étaient montrés et dits avant la question. |
| `su_f7b_limite` | À toi : la suite du problème du national, étape 2 : la limite | ✏️ 🆕 voix | NOUVELLE. Étape 2 (ℓ = f(ℓ), 10 sujets ; convergence monotone bornée, 17 sujets) : les conditions écrites une à une comme au barème (convergente, g continue car dérivable, g(I) = [7/3 ; 3] ⊂ I, u₀ ∈ I), puis « ℓ = g(ℓ), ℓ ∈ [1 ; 3] — ℓ = ? » (`national.html?vue=g_limite`, arrêt `equation`). La correction entoure (−1 ; −1) et (3 ; 3), barre −1 ∉ I, puis l'escalier monte vers (3 ; 3). Exception à « un seul À toi par bloc » : les deux étapes du même exercice national (règle 41). |

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
| `su_e1_q3` | National 2024, question 3 : la convergence | ✏️ 🆕 voix | Question 3, la convergence. 2ᵉ PASSE : sur la VRAIE suite du sujet (`national.html?vue=n24_points`) : les points (n ; uₙ) descendent (question 2), la droite verte y = 2 passe sous tous (question 1), arrêt sur « décroissante + minorée ⇒ ? ». Avant : l'animation générique des deux bons couples, et la voix disait la règle avant la question. |
| `su_e1_q4` | National 2024, question 4 : la suite auxiliaire | ✏️ 🆕 voix | NOUVELLE : question 4, la suite auxiliaire ; question reprise de l'ancien exercice (réactions et démonstration gardent leur voix). |
| `su_e1_q5a` | National 2024, question 5 : vₙ, puis uₙ en fonction de n | ✏️ 🆕 voix | NOUVELLE (2ᵉ passe) : la question 5 demandait en un coup vₙ, uₙ et la limite. Ici v₀, puis vₙ = v₀ × qⁿ = (2/3)ⁿ⁺¹, puis « vₙ = (uₙ − 2)/(uₙ − 1) ⇒ uₙ = ? » (`national.html?vue=n24_un`, arrêt `isoler`) ; la correction écrit le produit en croix, le regroupement, uₙ = (2 − vₙ)/(1 − vₙ). Cas type « suite auxiliaire géométrique » (8 sujets) joué jusqu'à uₙ en fonction de n. |
| `su_e1_q5` | National 2024, question 5 : la limite par qⁿ | ✏️ 🆕 voix | Question 5, la limite seule (limite par qⁿ, 10 sujets). 2ᵉ PASSE : vue `national.html?vue=n24_limite` : uₙ = (2 − vₙ)/(1 − vₙ), vₙ = (2/3)ⁿ⁺¹ dont les points descendent vers l'axe, « −1 < 2/3 < 1 », arrêt sur « lim uₙ = ? » ; la correction écrit lim vₙ = 0, trace les points uₙ qui se serrent sur y = 2, puis lim uₙ = (2 − 0)/(1 − 0) = 2. Question, réactions et démonstration gardées (avec leur voix). |

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
- 2ᵉ passe (18 novembre 2026) : une page nouvelle, `national.html` (mode large, figure à gauche, écriture à droite,
  fractions à la craie en ⟦num|dén⟧), cinq vues ; chacune s'arrête sur la question, la suite de la vue est la correction :
  - `g_signe` (`su_f7_national`) : courbe_et_droite, difference, factorise, tableau [question] | signe_3mx, signe_xp1,
    signe_xp2, signe_g (le tableau de signes se remplit ligne par ligne), zone (bande verte : courbe au-dessus de y = x),
    escalier (il monte depuis u₀ = 1), conclusion.
  - `g_limite` (`su_f7b_limite`) : converge, continue, stable, u0, equation [question] | resoudre (points (3 ; 3) et
    (−1 ; −1) entourés), choix (−1 ∉ I, ℓ = 3), escalier.
  - `n24_points` (`su_e1_q3`) : enonce, points (les termes 4 ; 2,8 ; 2,42… tombent un à un), plancher (y = 2), question
    [question] | converge.
  - `n24_un` (`su_e1_q5a`) : donnees, v0, vn, isoler [question] | croix, regrouper, factoriser, un.
  - `n24_limite` (`su_e1_q5`) : un, vn (points vₙ vers 0), condition, question [question] | qn, limite (points uₙ sur y = 2).
  Aucune vue utilisée par le cours en ligne n'a changé (vues ajoutées dans un fichier nouveau). Les pages s'écrivent seules au
  chargement : chaque diapositive part sur un `play_until` dès ses premiers mots, et la correction vient tard dans
  l'écriture (≥ 13 s), pour qu'elle ne passe pas à l'écran avant la question.
- Question 3 (1ʳᵉ passe) : `plafond.html?vue=couple` ; remplacée en 2ᵉ passe par `national.html?vue=n24_points`.

## 2ᵉ passe (18 novembre 2026) : les cas types du national joués pas à pas

### Inventaire cas type → diapositive(s)

| Cas type (fréquence) | Avant | Après |
|---|---|---|
| Récurrence, minoration affine (2016 R, 2017 R) | `su_r3_heredite_affine` (calcul joué, sans question) + `su_z3_ordre_inverse` ✏️ | inchangé |
| Récurrence, suite homographique (10) | `su_r4`/`su_r4b` ✏️, `su_r8_national` ✏️, `su_e1_complet` ✏️ (sans réactions) | `su_e1_complet` : réactions préparées écrites |
| Récurrence, f croissante (10) | `su_f3_encadrement_f` ✏️ : la voix et la scène donnaient la réponse | `su_f3` arrêtée sur f(1), f(2) (moment `images`) ; voix réécrite |
| Vérifier une écriture donnée (8) | `su_r6_ecriture_donnee`, `su_m3_egalite_donnee` | inchangé |
| Monotonie par la différence (7) | `su_m2`, `su_m3`, `su_e1_q2` ✏️ (sans réactions) | `su_e1_q2` : réactions écrites |
| Monotonie par le quotient (1) | `su_m4_quotient` ✏️ | inchangé |
| Monotonie par f(x) − x (10) | `su_f4_sens_f`, `su_f7_national` (avec la limite, d'un trait) | `su_f7_national` étape 1 seule, tableau de signes animé |
| Convergence monotone bornée (17) | `su_c1`, `su_c2`, `su_e1_q3` (animation générique) | `su_e1_q3` sur la vraie suite (`n24_points`) ; `su_f7b_limite` |
| Suite auxiliaire géométrique (8) | `su_x2`, `su_x3` ✏️, `su_x4`, `su_e1_q4` ✏️, `su_e1_q5` (vₙ, uₙ et la limite en une question) | + `su_e1_q5a` (v₀, vₙ, puis uₙ) |
| Suite auxiliaire arithmétique (3) | `su_x5` | inchangé |
| Limite par qⁿ (10) | `su_l3`, `su_l4`, `su_l5`, `su_e1_q5` | `su_e1_q5` : la limite seule, vₙ → 0 animé (`n24_limite`) |
| Majoration kⁿ, comparaison (3) | `su_c5` → `su_c8` ✏️ | inchangé (voir ci-dessous) |
| uₙ₊₁ = f(uₙ) et ℓ = f(ℓ) (10) | `su_f1`, `su_f2`, `su_f5`, `su_f6`, `su_f7` | + `su_f7b_limite` (conditions une à une, ℓ = ?, escalier après la réponse) |
| Limite de f(uₙ) (1) | `su_l7_f_un` ✏️ | inchangé (voir ci-dessous) |
| Plus petit rang (2) | `su_p1_rang` (joué, sans question) | inchangé (voir ci-dessous) |
| Somme et sa limite (2) | `su_p2_somme_mixte`, `su_p3_limite_somme` ✏️ (jumeau : raison 1/3) | inchangé |

### Questions dont la vue (ou la voix) montrait la réponse

- `su_f3_encadrement_f` : arrêt `boite_y` (« x dans [1 ; 2] ⇒ f(x) dans [1 ; 4/3] ») → arrêt `images` ; la phrase de
  la voix qui disait la réponse est retirée (voix à refaire).
- `su_f7_national` : l'escalier qui monte et « la courbe coupe la droite en (3 ; 3) » étaient joués et dits avant la
  question « croissante, puis la limite » → vue `g_signe`, rien de la conclusion avant la question.
- `su_e1_q3` : la voix disait la règle des bons couples avant la question → la voix montre les deux faits (décroissante,
  au-dessus de y = 2), l'élève cite la règle.
- Revues sans changement : `su_x3_fraction` (« cible : vₙ₊₁ = (1/2)vₙ » est donné par l'énoncé du national), `su_p3`
  (exemple raison 1/2, question raison 1/3), `su_c4`, `su_r4b`, `su_r8`, `su_e1_complet`, `su_e1_q2`, `su_e1_q4`.

### Rejeu après la réponse

| Diapositive | URL de la vue | Moment(s) à rejouer |
|---|---|---|
| `su_f3_encadrement_f` | `escalier.html?vue=boite` | `boite_y` |
| `su_f7_national` | `national.html?vue=g_signe` | `signe_3mx`, `signe_xp1`, `signe_xp2`, `signe_g`, `zone`, `escalier`, `conclusion` |
| `su_f7b_limite` | `national.html?vue=g_limite` | `resoudre`, `choix`, `escalier` |
| `su_e1_q3` | `national.html?vue=n24_points` | `converge` |
| `su_e1_q5a` | `national.html?vue=n24_un` | `croix`, `regrouper`, `factoriser`, `un` |
| `su_e1_q5` | `national.html?vue=n24_limite` | `qn`, `limite` |

**Écrit dans le cours (18 novembre 2026)** : chaque diapositive de cette liste porte `concentration.apres_reponse` (une étape `play_until` par moment, dans l'ordre), débloqué par sa première question (`q`). Le lecteur ne joue ces moments qu'après la réponse, même si un pointage les demandait ; contrôle : `python -I backend/scripts/verifier_parcours.py` (rien d'imprimé). Chaque moment a été vérifié dans Chromium : présent dans la vue de la diapositive, après le dernier moment de son pointage.

### Mots

- Remplacés (rares pour la voix) : « كنسقطو » → « من la courbe كنقراو » ; « la fraction » → « le quotient » ; « صالح »,
  « استعملو », « استعملها », « كتعطيها », « بفضل » → « كاين لكل n », « خدم بيه », « منها », « حيت » ; « قبلو »,
  « يساويه », « ماكتبقاش », « داخلو », « فوقو », « ماتقدرش », « كتدوز » → tournures courantes ; « la convergence »
  (vu 1 fois) → « واش la suite convergente ».
- Gardés, à écouter : « l'initialisation » (terme du programme, déjà dans `su_e1_complet`) ; « auxiliaire »,
  « factorise », « regroupe », « isole » (réactions et démonstration de `su_e1_q5`, voix déjà faite, non réécrites).

## Ce qui reste à faire

- Fusion du 18 novembre 2026 : une autre session (commit `e8d20fdd`, `scripts/logique/ch3_suites.py`) avait coupé `su_f7_national` en `su_f7_national` + `su_f7_national_b` sur `escalier`. La 2ᵉ passe fait la même coupure avec une vue dédiée (`national.html?vue=g_signe` puis `g_limite`, `su_f7b_limite`) et des réactions préparées ; elle est gardée, `su_f7_national_b` n'existe donc pas. Le script `ch3_suites.py` ne la réapplique pas (sa garde teste l'ancien énoncé « croissante, puis… »).

- Voix : `math_ch3_suites_numeriques_voix.json` (52 pistes : diapositives, démonstrations, énoncés et les réactions
  écrites à la main en 2ᵉ passe pour `su_e1_complet`, `su_e1_q2`, `su_e1_q3`, `su_f7_national`, `su_f7b_limite`,
  `su_e1_q5a`).
- `national.html` est une page nouvelle (pas de build) ; `calculs-vues.js` n'a pas changé en 2ᵉ passe. Les vues
  `e1_q1`, `e1_q2`, `e1_q4`, `e1_q5` ajoutées à la main en 1ʳᵉ passe restent à reporter dans les sources du build
  (`e1_q5` n'est plus utilisée par la copie en attente) ; leurs lignes sont des fractions à plat (« (4uₙ − 2)/(uₙ + 1) ») :
  à réécrire en ⟦num|dén⟧ dans le build.
- La voix donne encore la réponse avant la question (exemple identique à la question) : `su_l7_f_un` (√(uₙ + 7) → 3,
  1 sujet), `su_c8_ecart` (la limite 2, 3 sujets), `su_l1_converge` (16) : à couper comme `su_f3` (voix à refaire) ou à
  doter d'une question jumelle (autres valeurs) à la prochaine passe.
- Plus petit rang (`su_p1_rang`, 2 sujets) : joué pas à pas mais sans question à l'élève ; un exercice jumeau (même
  méthode, autres valeurs) serait à ajouter.
- Les écarts DEPART (`demarrer: start`) et GESTE déjà présents restent ; les diapositives nouvelles ou refaites en
  2ᵉ passe n'ont plus de `demarrer` (la scène part au chargement, le premier `play_until` sur les premiers mots).
