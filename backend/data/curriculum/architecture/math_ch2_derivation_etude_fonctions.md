# Architecture — Dérivation et étude des fonctions (`math_ch2_derivation_etude_fonctions`)

Skill `logique-de-cours`, 18 novembre 2026. Cours en ligne inchangé ; nouvelle version :
`backend/data/courses/en_attente/math_ch2_derivation_etude_fonctions.json`, produite par
`scripts/logique/ch2_derivation.py` (rejouable) et `scripts/logique/reordonner.py`.

## La logique avant

Séance 0 de cinq rappels de 1re bac (pente, équation de droite, dériver un polynôme, signe d'un produit, 1/x près de
0) → I. nombre dérivé → II. tangente → III. demi-tangentes → IV. calcul des dérivées → V. signe de f′ et variations →
VI. concavité → VII. branches infinies → VIII. position relative → IX. symétrie → X. tracé → XI. réciproque → XII.
problème d'analyse (étude complète en 3 diapositives : étapes 1-2 dites avec leurs résultats, une seule question,
étapes 4-5 dites avec leurs résultats) → bilan.

Défauts : les rappels 3, 4 et 5 arrivent 30 à 60 minutes avant leur usage (le signe d'un produit sert en séance 3) ;
l'étude complète, cœur du national (Analyse 55 %), ne laisse répondre l'élève qu'une fois sur cinq étapes.

## Les sources

- **Exploration** (`exploration/derivation_etude_fonctions.json`) et **cas types du national** : montrer que f′(x) = …
  20/20 ; signe de f′ et variations 18/20 ; tracer la courbe 17/20 ; branche parabolique 16/20 ; point d'inflexion
  11/20 ; position relative 10/20 ; fonction auxiliaire 9/20 ; asymptotes 8/20 et 5/20 ; réciproque 8/20 et
  (f⁻¹)′ 6/20 ; symétrie 1/20.
- **Cinq cours écrits** : Benmoussa (Moutamadris, AlloSchool 100260), Cheddadi (AlloSchool 122862-122863), Atmani
  (Moutamadris), Belkhyr (AlloSchool 78087), fiche Atlasmaths ; plus le livre du Prof Fayssal (`docs/audit-prof/maths.md`).
  **Ordre commun** : dérivabilité en un point, à droite, à gauche → interprétation (tangente, demi-tangente) →
  dérivable sur un intervalle, fonction dérivée → opérations, uⁿ, √u, composée → réciproque et ⁿ√u → monotonie,
  extremums → f″, concavité → symétries → branches infinies. Le plan d'étude n'est écrit que dans la fiche Atlas.
- **Le cadre** : `perimetre.json`, etude_fonction 1.2.5 à 1.2.22 et fonction_reciproque 1.2.11 ; approximation affine
  retirée exprès (hors cadre).

## Les grandes décisions

1. **Les rappels au moment où ils servent** (règle 6) : la pente reste devant la sécante, l'équation de droite passe
   devant la tangente, dériver un polynôme devant le tableau des dérivées, le signe d'un produit devant « factoriser
   f′ », 1/x près de 0 devant le taux qui part à l'infini. Deux voix à refaire pour les mots de liaison (`df_z5`,
   `df_dv1`).
2. **L'ordre des profs est gardé** pour le reste ; un écart écrit : la réciproque reste après le tracé (au national,
   (f⁻¹)′ et la courbe de f⁻¹ viennent après l'étude, et `df_rec6` a besoin du tracé).
3. **L'étude complète jouée étape par étape** : étape 1 (domaine) demandée à l'élève ; étape 2 (bord −1) montrée sur
   la courbe ; étape 3 (signe de f′, minimum) demandée ; étape 5 (branche infinie) demandée ; la courbe animée
   (`trace.html?vue=etude`, tableau puis courbe qui se construisent) arrête chaque étape. Exception écrite à « un seul
   À toi par bloc » pour ce bloc (règle 41, demande du 18 novembre).
4. **Rien retiré** : aucune diapositive hors cadre ; la symétrie (1/20) reste en 4 diapositives courtes, présente
   dans tous les cours écrits.

## L'architecture, diapositive par diapositive

83 diapositives, 7 séances, 26 blocs, durée prévue 236 min (2ᵉ passe : + 6 diapositives, + 2 blocs). « ✏️ » : la diapositive porte le « À toi » du bloc ; « 🔊 » : sa voix est gardée ; « 🆕 voix » : à enregistrer.

### Séance 1 — Du taux d'accroissement à la tangente

**La carte ; la pente d'une droite ; la pente d'une sécante** (`df_n1_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_c1_carte` | La carte du chapitre : cinq questions sur une courbe | 🔊 | Pourquoi dériver, avant de calculer : cinq questions sur une courbe ; l'élève sait où va le chapitre. |
| `df_z1_pente` | Rappel 1 : la pente d'une droite | 🔊 | Rappel de la pente d'une droite, gardé juste avant la sécante qui en a besoin (déjà à sa place). |
| `df_nd1_secante` | Entre deux points : la pente d'une sécante | ✏️ 🔊 | Le taux comme pente d'une sécante, vu sur la parabole ; l'élève calcule la pente de (AM). |

**Le nombre dérivé ; le calcul, un polynôme puis une racine** (`df_n1_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_nd2_rapprocher` | M se rapproche de A | 🔊 | M glisse vers A : la tangente naît de la sécante (animation, valeurs lues dans le tableau qui naît du glissement). |
| `df_nd3_nombre_derive` | Le nombre dérivé et la tangente | 🔊 | La définition après l'avoir vue (ordre commun : dérivabilité en un point d'abord). |
| `df_nd4_calcul` | Le calcul, ligne par ligne : un polynôme | 🔊 | Le calcul rédigé sur x² en 1 : exemple chiffré simple. |
| `df_nd4_calcul_b` | Avec une racine : le conjugué | ✏️ 🔊 | Avec une racine (conjugué, outil du ch1) ; l'élève répond. |

**L'équation d'une droite ; la tangente** (`df_n1_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_z2_equation_droite` | Rappel 2 : l'équation d'une droite | ✏️ 🔊 | Rappel y = ax + b juste avant l'équation de la tangente. |
| `df_tg1_equation` | L'équation de la tangente | 🔊 | La tangente, un point et une pente (interprétation géométrique, ordre commun). |
| `df_tg2_ecrire` | Écrire une tangente | 🔊 | Écrire une tangente, les trois nombres (2016 R, 2024 R, 2025 N, 2025 R). |

**Vérifier sa tangente ; arriver par la droite, par la gauche** (`df_n1_b4`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_tg3_verifier` | Vérifier sa tangente ; tangente horizontale | ✏️ 🔊 | Le contrôle de la tangente et la tangente horizontale ; l'élève vérifie. |
| `df_dt1_droite` | Arriver par la droite | 🔊 | Dérivabilité à droite vue sur un coin (|x² − 1|). |
| `df_dt2_gauche` | Arriver par la gauche | 🔊 | À gauche, même coin. |

### Séance 2 — Demi-tangentes ; calculer une dérivée

**Point anguleux ; 1/x près de 0 ; le taux part à l'infini** (`df_n2_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_dt3_anguleux` | Dérivable ou point anguleux | ✏️ 🔊 | Point anguleux : la règle après les deux côtés ; l'élève conclut. |
| `df_z5_un_sur_x` | Rappel 5 : 1 sur un tout petit nombre | 🆕 voix | DÉPLACÉ (était en séance 0) : 1/x près de 0 rappelé juste avant le taux qui part à l'infini ; « Un rappel » au lieu de « Dernier rappel » ; sa question va dans la réserve (un seul À toi par bloc). |
| `df_dt4_infini` | Quand le taux part à l'infini | 🔊 | Le taux part à l'infini (√x en 0) : demi-tangente verticale ; utilise le rappel précédent. |

**Demi-tangente vers le haut ou le bas ; deux morceaux** (`df_n2_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_dt5_sens` | Vers le haut ou vers le bas : à droite | 🔊 | Le sens de la demi-tangente à droite, deux cas. |
| `df_dt5_sens_b` | Vers le haut ou vers le bas : à gauche | 🔊 | À gauche, deux cas : une idée par diapositive. |
| `df_dt6_morceaux` | Une fonction en deux morceaux, comme au national | ✏️ 🔊 | Fonction en deux morceaux comme au national (2021 N, 2022 R, 2023 R) ; l'élève répond. |

**Dériver un polynôme ; le tableau ; produit et quotient** (`df_n2_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_z3_deriver_polynome` | Rappel 3 : dériver un polynôme | 🔊 | DÉPLACÉ : dériver un polynôme rappelé juste avant le tableau des dérivées. |
| `df_dv1_tableau` | Le tableau des dérivées : 1/x, √x, sin, cos | 🆕 voix | Le tableau des dérivées (1/x, √x, sin, cos) ; première phrase réécrite (« On vient de dériver les polynômes »). |
| `df_dv2_produit_quotient` | La dérivée d'un produit | 🔊 | (uv)′ vu sur un rectangle avant la formule. |
| `df_dv2_produit_quotient_b` | La dérivée d'un quotient | 🔊 | (u/v)′, exemple chiffré. |

**Puissance, racine, racine n-ième d'une expression** (`df_n2_b4`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_dv3_puissance` | Une puissance d'une expression | ✏️ 🔊 | uⁿ : on nomme la parenthèse ; l'élève dérive. |
| `df_dv4_racine` | La racine d'une expression | 🔊 | √u, même geste. |
| `df_dv5_racine_n` | La racine n-ième et la composée | 🔊 | ⁿ√u (Atmani, cadre 1.2.22) : une formule de plus, même idée. |

### Séance 3 — La fonction dérivée et le sens de variation

**Dérivable sur un intervalle ; « montrer que f′(x) = … » ; la courbe monte** (`df_n3_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_dv5b_intervalle` | Dérivable sur un intervalle ; la fonction dérivée | 🔊 | Dérivable sur un intervalle et fonction dérivée (manque relevé par l'audit, ordre commun). |
| `df_dv6_montrer` | « Montrer que f'(x) = … » | ✏️ 🔊 | « Montrer que f′(x) = … » : 20 sujets sur 20 ; l'élève fait la question. |
| `df_va1_monte` | La courbe monte : f' est positive | 🔊 | Signe de f′ et monotonie vus avec la tangente qui glisse. |

**Le sommet, le creux ; le signe d'un produit** (`df_n3_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_va2_sommet` | Au sommet | 🔊 | Au sommet, f′ = 0 : l'élève voit lui-même la tangente horizontale (observation). |
| `df_va2_sommet_b` | Au creux ; la règle de l'extremum | 🔊 | Au creux, et la règle de l'extremum. |
| `df_z4_signe_produit` | Rappel 4 : le signe d'un produit | 🔊 | DÉPLACÉ : le signe d'un produit rappelé juste avant « factoriser pour lire le signe de f′ ». |

**Factoriser f′ ; le tableau de variations ; la valeur exclue** (`df_n3_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_va3_factoriser` | Factoriser pour lire le signe | 🔊 | Factoriser f′ (18 sujets sur 20 : signe de f′). |
| `df_va4_tableau` | Le tableau de variations | ✏️ 🔊 | Le tableau de variations à trois lignes ; l'élève le remplit. |
| `df_va5_double_barre` | La valeur exclue et le contrôle des flèches | 🔊 | La valeur exclue et la double barre, sur le fil rouge x + 1/x. |

**Lire un extremum ; le signe venu d'une autre fonction** (`df_n3_b4`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_va6_extremum` | Lire un extremum, un signe, une inégalité | 🔊 | Lire un extremum, un signe, une inégalité dans le tableau (2021 N, 2021 R). |
| `df_va7_auxiliaire` | Quand le signe vient d'une autre fonction | ✏️ 🆕 voix | La fonction auxiliaire g (9 sujets sur 20) : le principe. 2ᵉ PASSE : la voix ne dit plus « donc f est croissante » avant la question (la phrase est retirée, la vue s'arrête sur `lien`, plus sur `conclusion`). |

**Exercice : la fonction auxiliaire, une question à la fois** (`df_n3_b5`, 2ᵉ passe)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_va8_aux_a` | Exercice, partie I : le signe de g′ | ✏️ 🆕 voix | NOUVELLE. Le cas type « fonction auxiliaire » (9/20) joué comme au national, juste après son principe : g(x) = 2x³ − 3x² + 2 sur ]0 ; +∞[, g′(x) = 6x(x − 1) ; la vue `calculs.html?vue=aux_g` s'arrête sur le cadre du tableau (ligne x) : l'élève donne le signe de g′ sur ]0 ; 1[. |
| `df_va8_aux_b` | Exercice, partie I : le signe de g, lu dans son tableau | ✏️ 🆕 voix | NOUVELLE. La ligne de g′ puis les flèches se construisent ; g(1) = 1 calculé ; la conclusion « g(x) > 0 » est cachée : l'élève la déduit du minimum (méthode de l'exploration : lire le minimum dans le tableau de g). |
| `df_va8_aux_c` | Exercice, partie II : montrer que f′(x) = g(x)/x² | ✏️ 🆕 voix | NOUVELLE. « Montrer que f′(x) = … » (20/20) sur f(x) = x² − 3x − 2/x : « f est dérivable sur … car … », la dérivée, puis l'élève trouve le numérateur au même dénominateur (la vue `aux_f` s'arrête avant `forme`). |
| `df_va8_aux_d` | Exercice, partie II : le tableau de variations de f | ✏️ 🆕 voix | NOUVELLE. f′ a le signe de g (partie I) : la ligne f′(x) « + » s'écrit ; l'élève donne la limite en 0⁺ avant que les flèches et −∞, +∞ s'écrivent. |

### Séance 4 — Concavité et branches infinies

**Concavité et point d'inflexion** (`df_s4_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_co1_sous` | La courbe sous sa tangente | 🔊 | Concavité vue avec la tangente qui roule (11 sujets sur 20 : point d'inflexion). |
| `df_co2_traverse` | Le point où la tangente traverse | 🔊 | Le point où la tangente traverse. |
| `df_co3_f_seconde` | Le signe de f'' | 🔊 | Le signe de f″, la règle après l'avoir vue. |
| `df_co4_changeant` | « En changeant de signe » | ✏️ 🔊 | Le piège x⁴ : « en changeant de signe » ; l'élève tranche. |

**Les asymptotes** (`df_s4_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_bi1_verticale` | La courbe longe une droite verticale | 🔊 | Asymptote verticale (8/20). |
| `df_bi2_horizontale` | La courbe longe une droite horizontale | 🔊 | Asymptote horizontale (5/20). |
| `df_bi3_oblique` | La courbe longe une droite penchée | 🔊 | Asymptote oblique (8/20, droite donnée). |
| `df_bi4_pente_om` | Aucune droite à longer : la pente de (OM) | ✏️ 🔊 | Aucune droite à longer : la pente de (OM) ; l'élève répond. |

**Branches paraboliques et phrases types** (`df_s4_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_bi5_direction` | Une direction sans asymptote | 🔊 | Branche parabolique (16/20). |
| `df_bi6_arbre` | L'arbre des branches infinies (1) | 🔊 | L'arbre des branches infinies (1). |
| `df_bi6_arbre_b` | L'arbre des branches infinies (2) : la limite vaut a | 🔊 | L'arbre (2) : la limite vaut a. |
| `df_bi7_droite_donnee` | Quand l'énoncé donne la droite | ✏️ 🔊 | Au national la droite est donnée : une seule limite ; l'élève répond. |

### Séance 5 — Position relative, symétrie, préparer le tracé

**Position relative d'une courbe et d'une droite** (`df_s5_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_pr1_dessus` | Au-dessus ou en dessous | 🔊 | Position relative (10/20) vue avec le segment entre courbe et droite. |
| `df_pr2_signe` | Le signe de la différence | 🔊 | Le signe de la différence. |
| `df_pr3_tableau` | Le tableau de position relative | ✏️ 🔊 | Le tableau de position ; l'élève répond. |

**Axe et centre de symétrie** (`df_s5_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_sy1_symetrique` | Le point de l'autre côté | 🔊 | Axe de symétrie vu point par point (1/20, gardé court : 4 diapositives, chez tous les cours écrits). |
| `df_sy2_axe` | Un axe de symétrie | 🔊 | f(a − x) = f(a + x) lu sur la courbe. |
| `df_sy3_centre` | Un centre de symétrie | 🔊 | Centre de symétrie, même méthode. |
| `df_sy4_rediger` | Rédiger : deux conditions | ✏️ 🔊 | Rédiger : deux conditions ; l'élève répond. |

**Préparer le tracé** (`df_s5_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_tr1_tableau_lu` | Ce que le tableau annonce | 🔊 | Le tracé (17/20) : lire le tableau d'abord. |
| `df_tr2_droites` | D'abord les droites | 🔊 | Les droites d'abord. |
| `df_tr3_points` | Puis les points | ✏️ 🔊 | Puis les points ; l'élève répond. |

### Séance 6 — Lire une courbe ; la fonction réciproque

**Tracer d'un seul trait et lire la courbe** (`df_s6_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_tr4_branche` | La courbe, d'un seul trait | 🔊 | La courbe d'un seul trait. |
| `df_tr5_symetrie` | L'autre moitié par symétrie | 🔊 | L'autre moitié par symétrie. |
| `df_tr6_lire` | Lire une courbe déjà tracée | ✏️ 🔊 | Lire une courbe déjà tracée (parties I de 2024, 2025) ; l'élève répond. |

**La réciproque dans le miroir y = x** (`df_s6_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_rec1_miroir` | Le miroir y = x | 🔊 | Réciproque : gardée après le tracé, car la question (f⁻¹)′ vient au national après l'étude et rec6 a besoin du tracé (les cours écrits la mettent avec la composée : écart écrit ici). |
| `df_rec2_pente` | La pente dans le miroir | 🔊 | La pente dans le miroir (observation de l'élève). |
| `df_rec3_formule` | La formule | ✏️ 🔊 | La formule 1/f′(f⁻¹(y)) après l'avoir vue ; l'élève répond. |

**Rédiger comme au national et tracer la réciproque** (`df_s6_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_rec4_condition` | Pourquoi f'(x₀) ≠ 0 | 🔊 | Pourquoi f′(x₀) ≠ 0 : tangente verticale. |
| `df_rec5_national` | Trois lignes, comme au national | 🔊 | Trois lignes comme au national (6/20). |
| `df_rec6_courbe` | Tracer la courbe de la réciproque | ✏️ 🔊 | Tracer la courbe de f⁻¹ (4 sujets) ; l'élève répond. |

### Séance 7 — Le problème d'analyse, étape par étape ; le bilan

**L'ordre du problème ; la forme demandée ; l'ensemble de définition** (`df_n7_b1`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_ec1_ordre` | L'ordre d'un problème d'analyse | 🔊 | L'ordre du problème d'analyse au national. |
| `df_ec2_forme` | Lire la forme demandée | 🔊 | Lire la forme demandée (« montrer que » donne le chemin). |
| `df_ec3_etude` | Une étude complète, pas à pas : l'ensemble de définition | ✏️ 🆕 voix | 2ᵉ PASSE : vue `trace.html?vue=etude_pas`, arrêtée sur le titre seul (l'ancienne vue écrivait « sur [−1 ; +∞[ » dans son titre et −1 dans le tableau : la réponse avant la question). RÉÉCRIT : l'étude complète commence par l'étape 1 seule ; l'élève donne l'ensemble de définition avant la correction (question reprise de la réserve, réactions et démonstration gardent leur voix). Avant, la voix donnait les étapes 1 et 2 avec leurs résultats. |

**Le bord, le signe de f′, la branche infinie** (`df_n7_b2`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_ec3_etude_a2` | Une étude complète, pas à pas : le bord −1 | ✏️ 🆕 voix | 2ᵉ PASSE, RÉÉCRITE en question (dérivabilité à droite + interprétation, cas types 2021 N, 2022 R, 2023 R) : la voix calcule le taux jusqu'à −∞, la vue s'arrête sur `taux` ; l'élève conclut (pas dérivable, demi-tangente verticale) avant que la double barre et la phrase s'écrivent. |
| `df_ec3_etude_b` | Une étude complète, pas à pas : le signe de f′ | ✏️ 🔊 | Étape 3, le signe de f′ : l'élève trouve le minimum. Voix gardée ; 2ᵉ PASSE : la vue `etude_pas&depart=demi_tangente` écrit la dérivée, la phrase du signe et la ligne f′ (− 0 +) à leurs mots, et s'arrête avant les flèches et le minimum. |
| `df_ec3_etude_c` | Une étude complète, pas à pas : le minimum, O, la branche infinie | ✏️ 🆕 voix | 2ᵉ PASSE : `etude_pas&depart=ligne_signe` : les flèches et le minimum, f(0) = 0, puis f(x)/x → +∞ ; l'interprétation (branche) n'est écrite qu'après la réponse ; la courbe n'est plus tracée ici (elle se construit en d et e). RÉÉCRIT : le minimum confirmé, f(0) = 0, puis l'étape 5 posée à l'élève (lim f(x)/x = +∞ : quelle branche ?) avant la correction ; la courbe se trace avec l'animation. Avant, la réponse était dite. |

**Construire la courbe de l'étude, pas à pas ; une solution unique** (`df_n7_b2c`, 2ᵉ passe)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_ec3_etude_d` | Construire la courbe, pas à pas : les points | ✏️ 🆕 voix | NOUVELLE. Le tracé (17/20) joué sur l'étude qu'on vient de finir : le repère, A et sa demi-tangente, le minimum, O, B(1 ; √2), chacun sur son moment, la case du tableau qui l'annonce s'allume ; l'élève dit comment est la tangente au minimum avant qu'elle soit tracée. |
| `df_ec3_etude_e` | Construire la courbe, pas à pas : d'un seul trait | 🆕 voix | NOUVELLE. La tangente horizontale, puis la courbe d'un trait en suivant le tableau, puis la branche ; l'ordre à retenir. Pas de question (une par bloc suffit). |
| `df_ec4_unique` | Rappel : une solution unique au milieu de l'étude | ✏️ 🔊 | La solution unique au milieu de l'étude (7/20), rappel du ch1 au moment où il sert. Passe dans le bloc `df_n7_b2c` avec son « retrouver » et son exercice ; `df_n7_b2` reçoit un « retrouver » et un exercice sur la demi-tangente verticale. |

**Le bilan et la carte** (`df_s7_b3`)

| Diapositive | Titre | | Pourquoi ici |
|---|---|---|---|
| `df_fin1_bilan` | Ce qu'il faut retenir | 🔊 | La fiche du chapitre. |
| `df_fin2_carte` | La carte du chapitre | 🔊 | La carte du chapitre. |

## Animations et exercices animés

- Étude complète (2ᵉ passe) : `trace.html?vue=etude_pas` (NOUVELLE vue ; `etude` reste pour le cours en ligne). Moments, dans
  l'ordre : `enonce`, `domaine` (D_f et le cadre du tableau, bornes seules), `taux`, `demi_tangente` (double barre, phrase),
  `derivee`, `signe_phrase` (et −2/3 dans la ligne x), `ligne_signe`, `fleches` (minimum −2√3/9), `point_o`, `limite_f_sur_x`,
  `branche`, puis la construction : `repere_pose`, `trace_a`, `trace_minimum`, `trace_o`, `points_places` (B(1 ; √2)),
  `tangente_min`, `courbe_tracee`, `courbe_finie`. Chaque diapositive l'ouvre figée là où la précédente s'est arrêtée
  (`&depart=<moment>`, `depart.js`, `demarrer: reset`) : l'étude continue sur le même tableau, sans tout réécrire.
- Fonction auxiliaire (2ᵉ passe) : `calculs.html?vue=aux_g` (moments `enonce`, `derivee`, `phrase`, `ligne_x`, `ligne_signe`,
  `ligne_fleches`, `valeur_min`, `conclusion_g`) et `calculs.html?vue=aux_f` (`enonce`, `derivee`, `forme`, `lien`, `ligne_x_f`,
  `ligne_signe_f`, `ligne_fleches_f`, `conclusion_f`) : le tableau de variations se construit ligne par ligne (une ligne =
  un moment). Ajoutées À LA MAIN dans `calculs-vues.js` : à reporter dans les sources du build (`maths_build/…`, hors dépôt).
- Fichiers ajoutés au dossier : `depart.js` (ouvrir figé sur un moment ; sans `depart` rien ne change) et `fractions.js`
  (une phrase avec ⟦num|dén⟧ ET un exposant : `exposants.js` du commun écrivait les crochets ; sans ⟦ rien ne change) ;
  chargés par `trace.html` et `calculs.html`. Vues du cours en ligne vérifiées sans erreur (va5, dv6, etapes, etude, lecture).
- Les autres animations sont gardées : sécante qui glisse, demi-tangentes, rectangle du produit, tangente qui glisse et
  qui roule, branches, position, symétrie, tracé, miroir.

## 2ᵉ passe (18 novembre 2026) : les cas types joués pas à pas

| Cas type (fréquence) | Avant | Après |
|---|---|---|
| Dérivabilité en un point (3/20) | `df_nd4_calcul`, `df_nd4_calcul_b` (calculs joués ligne par ligne) | inchangé |
| Droite / gauche, interprétation (2021 N, 2022 R, 2023 R) | `df_dt1`…`df_dt6_morceaux` ; `df_ec3_etude_a2` montré | `df_ec3_etude_a2` devient une question : le taux est joué, l'élève conclut avant la phrase |
| Tangente (4 sujets) | `df_tg1`…`df_tg3_verifier` | inchangé ; tangente au minimum demandée en `df_ec3_etude_d` |
| Montrer f′(x) = … (20/20) | `df_dv6_montrer` (question de méthode) | + `df_va8_aux_c` : l'élève fait l'étape du même dénominateur |
| Signe de f′, tableau qui se construit (18/20) | `df_va3`…`df_va5`, `df_ec3_etude_b` (tableau écrit d'un coup) | `etude_pas` : ligne x, puis f′, puis f(x), chacune à son moment ; `aux_g`, `aux_f` de même |
| Fonction auxiliaire (9/20) | `df_va7_auxiliaire` lu d'un bloc, réponse dite avant la question | `df_va7` (principe, réponse retirée) + `df_va8_aux_a` → `_d` (quatre questions, un tableau par partie) |
| Extremum → inégalité (2021 N, R) | `df_va6_extremum` + exercice du bloc `df_n3_b4` | inchangé |
| Asymptotes, branche parabolique (8/20, 16/20) | `df_bi1`…`df_bi7` ; `df_ec3_etude_c` | `df_ec3_etude_c` : l'interprétation n'est plus écrite avant la réponse |
| Position relative (10/20) | `df_pr1`…`df_pr3_tableau` | inchangé |
| Construire la courbe (17/20) | `df_tr1`…`df_tr5` (x + 1/x, montré) ; courbe de l'étude tracée d'un coup en `df_ec3_etude_c` | + `df_ec3_etude_d` (points un par un, question) et `df_ec3_etude_e` (tangente, trait, branche) |
| Point d'inflexion (11/20) | `df_co1`…`df_co4_changeant` | inchangé |
| Réciproque : J, (f⁻¹)′, courbe (8, 6, 4 sujets) | `df_rec1`…`df_rec6_courbe` | inchangé |

**Questions dont la vue ou la voix montrait la réponse** : `df_ec3_etude` (titre de la vue « sur [−1 ; +∞[ » et −1 au
tableau → arrêt sur le titre seul) ; `df_ec3_etude_c` (la vue traçait déjà la courbe qui monte à la verticale
avant « quelle branche ? » → la courbe vient après, arrêt sur la limite) ; `df_va7_auxiliaire` (la voix disait « f est croissante »
→ phrase retirée, arrêt sur `lien`) ; `df_ec3_etude_b` (`start` sans `play_until` → la vue écrit jusqu'à la ligne f′ seulement).

### Rejeu après la réponse

| Diapositive | URL de la vue | Moment(s) à rejouer |
|---|---|---|
| `df_va7_auxiliaire` | `calculs.html?vue=va7` | `conclusion` |
| `df_va8_aux_a` | `calculs.html?vue=aux_g` | `ligne_signe` |
| `df_va8_aux_b` | `calculs.html?vue=aux_g&depart=ligne_x` | `conclusion_g` |
| `df_va8_aux_c` | `calculs.html?vue=aux_f` | `forme` |
| `df_va8_aux_d` | `calculs.html?vue=aux_f&depart=derivee` | `ligne_fleches_f`, `conclusion_f` |
| `df_ec3_etude` | `trace.html?vue=etude_pas` | `domaine` |
| `df_ec3_etude_a2` | `trace.html?vue=etude_pas&depart=domaine` | `demi_tangente` |
| `df_ec3_etude_b` | `trace.html?vue=etude_pas&depart=demi_tangente` | `fleches` |
| `df_ec3_etude_c` | `trace.html?vue=etude_pas&depart=ligne_signe` | `branche` |
| `df_ec3_etude_d` | `trace.html?vue=etude_pas&depart=branche` | `tangente_min` |

**Écrit dans le cours (18 novembre 2026)** : chaque diapositive de cette liste porte `concentration.apres_reponse` (une étape `play_until` par moment, dans l'ordre), débloqué par sa première question (`q`). Le lecteur ne joue ces moments qu'après la réponse, même si un pointage les demandait ; contrôle : `python -I backend/scripts/verifier_parcours.py` (rien d'imprimé). Chaque moment a été vérifié dans Chromium : présent dans la vue de la diapositive, après le dernier moment de son pointage.

### Mots (2ᵉ passe)

Remplacés : « dérivables » (0) → « un polynôme, et un sur x dérivable » ; « معطي » (1) → « كاين » ; « الأطراف » (0) →
« les bornes » ; « lim » (1) → « la limite » ; « trait » (0) → « خط صغير » ; « droites », « tangentes » (1) → « le repère,
les points et la tangente » ; « مستوية » (0) → « la tangente horizontale » ; « conclure » (2) → « نستنتجو » ;
« trace-t-on » (0) → « كيفاش كتكون ». Gardé, à écouter : « demi-tangente » (2, terme du programme).

## Ce qui reste à faire

- 2ᵉ passe : voix de 8 diapositives (`df_va7_auxiliaire`, `df_va8_aux_a` → `_d`, `df_ec3_etude_a2`, `_d`, `_e`), 6
  démonstrations et 6 énoncés (`_voix.json`, 31 pistes en tout) ; réactions préparées des 6 nouvelles questions
  (`reactions_a_preparer`). Le rejeu après la réponse (tableau ci-dessus) est écrit dans `apres_reponse`.
- Questions de rappel dont la VOIX dit la réponse juste avant (pas touchées, voix enregistrées) : `df_nd1_secante`,
  `df_tg3_verifier`, `df_dt6_morceaux`, `df_va4_tableau`, `df_tr3_points`, `df_tr6_lire`. À reprendre si on refait leurs voix.
- Sur téléphone en paysage (724 × 350), les notes de `etude_pas` (comme celles de `etude`) sont plus petites que 15 px :
  le plan de `large.js` donne la moitié du cadre au repère. À revoir dans `large.js` pour toutes les vues « repère à droite ».

- Voix (1ʳᵉ passe) : `math_ch2_derivation_etude_fonctions_voix.json` (12 pistes, dont 5 diapositives ; 31 après la 2ᵉ passe).
- Réactions préparées : la question d'étape 5 (`df_ec3_etude_c`) reprend des réactions de la réserve ; celles qui n'ont
  pas de voix sont dans la liste. `df_tg3_verifier/e0` n'avait déjà pas de réactions.
- Le contrôle `verifier_pointage_simulations.py` : aucune ligne MOMENT ni REPERE ; les lignes IFRAME/DEPART de l'étude
  complète ont disparu (URL distinctes avec `depart`, `demarrer: reset`) ; restent des GESTE « trop serrés » calculés sur
  les pistes sans voix (durée inconnue), à revoir une fois les voix faites.
