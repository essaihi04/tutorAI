# Architecture — Transformations chimiques s'effectuant dans les deux sens (phys_ch11)

Revue de la logique du 18 novembre 2026 (skill `logique-de-cours`). Le travail part de la copie en attente, plus
récente que le cours en ligne. La nouvelle version est dans
`backend/data/courses/en_attente/phys_ch11_transformations_deux_sens.json`. Les pistes à mettre en voix sont dans
`phys_ch11_transformations_deux_sens_voix.json` : 14 pistes, toutes celles des deux questions d'observation ajoutées.

## 1. Sources et constats

**Profs (4 cours lus).** Le relevé est dans `sources_chimie_ch9_ch11.md`, chapitre C. Les cours lus :
- Mahajar et Tabit (AlloSchool, Cours 1) ;
- El Founani (AlloSchool, version LaTeX) ;
- Sbiro (pc1.ma, repris par El Goufifa) ;
- Hadjyne (pc1.ma).

L'ordre commun :
1. Brønsted : couple, demi-équation, l'eau ampholyte ; puis la réaction acide-base ;
2. le pH : rappel du log, pH-mètre étalonné ;
3. la réaction d'un acide avec l'eau et son tableau d'avancement ;
4. τ = x_f/x_max ;
5. l'expérience des deux sens : on ajoute de l'acide pur (le pH baisse) ou de l'éthanoate de sodium (le pH monte), d'où ⇌ ;
6. l'équilibre dynamique.

Ce que les profs font peu :
- la conductimétrie n'apparaît qu'en exercice ;
- aucun cours ne traite la dilution dans ce chapitre (Sbiro la place au chapitre « État d'équilibre »).

**Cadre.** Fiche `transformations_deux_sens`, capacités TD1 à TD8. TD7 (influence de la dilution et de la nature de
l'acide sur τ) est bien dans ce chapitre. Qr, K, Ka et pKa sont exclus (hors cadre de ce cours).

**National.** Ce qui revient le plus :
- τ calculé : 11 sessions sur 20 (par le pH, ou par σ en 2019 N) ;
- « montrer que τ = 10^(−pH)/C » : 2021 R ;
- la dilution augmente τ : 2021 R et 2025 R ;
- un dosage est total, τ ≈ 1 : 2024 R ;
- Brønsted et l'équation avec l'eau : presque chaque sujet d'acide.

**Logique de la copie en attente.** Elle suit déjà l'ordre commun des profs : Brønsted, pH, acide + eau, τ, deux
sens, équilibre dynamique. Les rappels de zéro sont en place (ion, concentration, puissances de dix et log, dilution
juste avant les dilutions). Deux manques au regard des règles du 18 novembre :
1. le tableau d'avancement est dit entièrement par la voix : l'élève ne construit aucune ligne lui-même ;
2. l'élève n'est jamais invité à **prévoir** ce que fait le pH quand on dilue : la voix donne 3,9 aussitôt.

Les deux questions d'observation existantes (`td_e1_inverse` : le pH monte ; `td_d2_taux` : les barres de τ) sont bien placées.

## 2. Architecture (ordre gardé), diapositive par diapositive

**=** : inchangée (voix gardée). **Obs** : question d'observation ajoutée.

### Séance 1 — Les bases depuis zéro ; acide, base, couple

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `td_o1_carte` | = | La carte du chapitre. |
| `td_o2_flacons` | = | L'énigme de départ : même concentration, pas le même pH. Elle donne envie de comprendre ; la réponse viendra avec τ. |
| `z1`, `z2`, `z3` | = | L'ion et le proton, la concentration, les puissances de dix et le log, enseignés de zéro juste avant le pH et Brønsted (règle 6). |
| `b1` → `b3b` | = | L'acide cède un proton, la base le capte, le couple, l'eau dans deux couples. Chaque fois l'animation d'abord, la définition lue ensuite. Ordre des profs. |

### Séance 2 — Réaction acido-basique, pH, réaction d'un acide avec l'eau

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `b4`, `p1`, `p2`, `p3` | = | La réaction acide-base, puis le pH (relation et sens), le calcul de [H₃O⁺] et le pH-mètre étalonné. |
| `p4`, `p5`, `p6` | = | L'acide puis la base avec l'eau. « Si la réaction était totale, le pH serait 2,0 ; on mesure 3,4 » : la conclusion « pas totale » est tirée d'une mesure, pas affirmée. |
| `td_a1_tableau` | = + **Obs** | Le tableau construit par l'élève. La voix s'arrête après l'état initial (« zéro et zéro ») et demande : « en cours, combien d'ions H₃O⁺ se sont formés ? » (C·V − x / x / 0). La voix reprend avec « السطر الثاني، en cours » (« la deuxième ligne, en cours »), qui confirme x. |
| `a2`, `a3`, `a4` | = | x_max calculé, x_f mesuré par le pH, τ = x_f/x_max. |

### Séance 3 — Taux d'avancement final, deux sens, état d'équilibre

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `a5`, `a6` | = | HCl (τ = 1), puis « montrer que τ = 10^(−pH)/C » (2021 R), démontré ligne par ligne et vérifié sur l'exemple A. |
| `e1`, `e1b`, `e2` | = | Les deux sens au labo animé, puis la double flèche. |
| `e3`, `e4` | = | L'état d'équilibre (le pH ne bouge plus), puis l'équilibre dynamique au niveau des entités (chocs dans les deux sens, TD5). |
| `e5`, `e6` | = | L'estérification (2016 N, annoncée « étudiée plus tard ») et 2017 N : τ décide entre totale et limitée. |
| `c1`, `c2`, `c3` | = | La conductimétrie donne τ. L'expérience des deux acides de même concentration vient d'abord, puis la relation, puis le calcul. |

### Séance 4 — Conductimétrie, dilution, questions du national, bilan

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `td_z4_dilution` | = | Le geste de dilution, enseigné juste avant de s'en servir. |
| `td_d1_dilution` | = + **Obs** | La voix s'arrête après « المحلول ولا dilué dix fois » (« la solution est diluée dix fois ») et la scène montre le deuxième bécher. Question : « que montre le pH-mètre ? » (diminue / augmente / ne change pas). La voix reprend avec « le pH égale trois virgule neuf ». C'est la prédiction du cas décisif du national 2021 R et 2025 R. |
| `d1b`, `d2`, `d3` | = | La 3ᵉ dilution, le tableau des τ (l'observation des barres existe déjà), puis la nature de l'acide. |
| `n1` → `n4b` | = | Nationaux 2021 R, 2019 N, 2023 N et 2024 R (méthode, puis calcul ligne par ligne). |
| `td_bl_fiche`, `td_cr_carte` | = | Bilan. |

## 3. Ce qui reste, et pourquoi

- **L'ordre n'est pas changé.** Il est déjà celui des profs, et chaque prérequis est enseigné juste avant son usage.
  Déplacer des diapositives coûterait des voix sans gain pour l'élève.
- **Le sens inverse (`e1`) est joué avant le sens direct (`e1b`)**, alors que les profs font l'inverse. Le texte de
  `e1b` renvoie à l'expérience de `e1` (« dans l'expérience d'avant, le pH a monté »). Les inverser obligerait à
  réécrire deux voix. Pédagogiquement, la surprise (le pH qui monte) ouvre bien la question des deux sens.
- **`a5` écrit déjà ⇌ pour l'acide éthanoïque**, avant l'expérience des deux sens. La double flèche est annoncée dès
  `b3` (pour le couple) et `p4`, avec « on la comprendra plus tard ». C'est une annonce, pas une preuve affirmée ; on la garde.
- **La dilution reste dans ce chapitre** (TD7 du cadre, deux nationaux), même si les profs la mettent ailleurs.
- **Brønsted, la base avec l'eau** (`p5`) : son τ est renvoyé au ch13 (Ka) ; ce cours n'en dit rien.

## 4. Besoins hors de ce cours (fichiers partagés, non modifiés)

- `td_b3b_eau`, `td_d1b_mesures`, `td_e2_fleche` et `td_n4b_calcul` continuent la scène de la diapositive d'avant
  (même URL). Il faudrait `?depart=<moment>` dans le kit partagé.
- `td_cr_carte` : un geste part 0,7 s après son mot (gestes trop serrés). À corriger à la prochaine voix de la carte.
