# Architecture — Suivi temporel d'une transformation chimique, vitesse de réaction (phys_ch10)

Revue de la logique du 18 novembre 2026 (skill `logique-de-cours`). Le travail part de la copie en attente, plus
récente que le cours en ligne : mêmes textes, mais des corrections écrites et les réactions des exercices de bloc.
La nouvelle version est dans `backend/data/courses/en_attente/phys_ch10_cinetique.json`. Les pistes à mettre en voix
sont dans `phys_ch10_cinetique_voix.json` : 23 pistes, dont 2 diapositives.

## 1. Sources et constats

**Profs (4 cours lus et un 5e qui en recopie un).** Le relevé est dans `sources_chimie_ch9_ch11.md`, chapitre B. Les
cours lus :
- Mahajar et Tabit (AlloSchool, Cours 1) ;
- El Founani (AlloSchool, version LaTeX) ;
- Sbiro (pc1.ma) ;
- Hadjyne (pc1.ma) ;
- Boulouiha, proche de Mahajar.

L'ordre commun :
1. un panorama des méthodes de suivi ;
2. le tableau d'avancement, rappelé **au fil de la première expérience**, pas à part ;
3. le dosage après trempe (I₂ dosé par le thiosulfate), puis la pression, puis la conductimétrie ;
4. v = (1/V)·dx/dt par la tangente, et le fait que la vitesse diminue ;
5. t½ lu sur la courbe.

Points à noter chez les profs :
- les chocs efficaces arrivent à la fin, chez un seul prof ;
- aucun prof n'explique G = k·σ, ils utilisent directement σ = Σλ[X].

**Cadre.** Fiche `cinetique`, capacités CIN1 à CIN9. Elle contient les chocs efficaces (CIN9) et le choix de la
méthode de suivi selon t½ (CIN7). La « réaction d'un ester avec les ions hydroxyde » est annoncée « étudiée plus
tard » et n'est pas nommée « saponification ».

**National.** Ce qui revient le plus :
- t½ lu sur la courbe : 9 sessions ;
- vitesse volumique par la tangente : 5 sessions (2016 R, 2019 R, 2021 N, 2024 N, 2025 R) ;
- suivi par σ ou G avec une relation donnée : 2016 R, 2018 R, 2021 N ;
- suivi par dosage : 2024 N ;
- « la vitesse diminue-t-elle ? » : 2025 R ;
- chocs efficaces en vrai ou faux : 2024 N.

Aucun national récent ne fait le suivi par la pression : nos 3 diapositives de pression restent courtes.

**Logique de la copie en attente : ce qui n'allait pas.**
1. `ci_m1_mesures` (« des mesures à des dates ») venait en premier. Il donnait les valeurs de **x** avant que x soit
   défini (tableau d'avancement, plus loin) et avant de dire comment on le mesure (trempe et titrage, juste après).
   Cela va contre les règles 4 et 6, et la règle 27 du professeur (rien d'utilisé avant d'être enseigné).
2. `ci_m3c_calcul` concluait « x = n(I₂) » avant la diapositive qui établit ce lien (`a3`) et avant le tableau
   d'avancement.
3. `ci_p4_2016R`, un national de **conductimétrie**, était rangé au milieu de la séance sur la **pression**, loin de la
   conductimétrie qu'il fait pratiquer.
4. `ci_v6b_espece` (calculer v à partir de n(X) ou [X], une méthode de calcul) coupait l'histoire de l'évolution de la
   vitesse : elle diminue, pourquoi, puis elle est nulle. Elle avait aussi la même simulation que `v6` juste avant,
   donc ses `play_until` étaient refusés.
5. `ci_m3c_calcul` avait la même simulation que `m3b`, et `m3b` la même que `m3`. Les trois étaient de suite.
6. Le tableau d'avancement était dit tout entier par la voix : l'élève ne construisait aucune ligne lui-même.

## 2. Nouvelle architecture, diapositive par diapositive

La colonne « Voix » vaut **=** quand la diapositive est inchangée, **D** quand elle est seulement déplacée (sa voix
est gardée), **R** quand son texte est réécrit (sa voix est à refaire). **Obs** signale une question d'observation ajoutée.

### Séance 1 — Les bases depuis zéro ; le tableau d'avancement

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `ci_o1_carte`, `ci_o2_methodes` | = | La carte, puis la question « où en est la réaction à chaque instant ? » et les trois méthodes. C'est le panorama par lequel commencent tous les profs. |
| `z1` → `z4` | = | La mole, la concentration, l'ion, les couples et l'équation de l'exemple A, enseignés de zéro juste avant le tableau (règle 6). |
| `ci_a1_tableau` | D | Le tableau d'avancement (état initial) vient **avant** toute mesure de x : x doit être défini avant d'être mesuré. |
| `ci_a1b_en_cours` | D + **Obs** | La ligne « en cours », **construite par l'élève**. La voix s'arrête après la définition de x (« combien de fois on a fait la recette »), puis demande « combien reste-t-il d'ions iodure ? » (10,0 − x / 10,0 + 2x / 10,0 − 2x). La voix reprend avec « السطر التاني » (« la deuxième ligne »), qui confirme 10,0 − 2x. La question écrite (x = 1,0 → 8,0 mmol) reste la question du bloc. |
| `ci_a2_limitant` | D | x_max et le réactif limitant. La question d'observation existante demande quelle barre arrive à zéro. |

### Séance 2 — Mesurer x : trempe et titrage ; la courbe x(t)

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `ci_m2_trempe` | D | Le problème : la réaction continue pendant le dosage. La trempe est montrée au labo animé, avec le prélèvement figé à côté du grand bécher qui continue de brunir. Ordre des profs (dosage après trempe en premier). |
| `ci_m3_titrage` | D | Le titrage jusqu'à l'équivalence (question du bloc). |
| `ci_m3b_calcul` | D | n(I₂) = C·V_E/2, établi par l'équation du titrage. |
| `ci_a3_lien` | D | « Mesurer n(I₂), c'est connaître x », lu dans le tableau. Placé juste avant le calcul qui s'en sert. Le titrage, déjà connu, est cité sans être utilisé avant sa diapositive. |
| `ci_m3c_calcul` | D | Le calcul complet à 8 min : relation, conversion, prélèvement × 10, x. Il n'a plus la même simulation que la diapositive d'avant. |
| `ci_m1_mesures` | **R** | Le tableau des mesures arrive **après** la manière de les obtenir. Le texte est réécrit : « on refait la trempe et le titrage à chaque date… à 8 min, 1,26 mmol, comme on l'a calculé ». Les valeurs ne changent pas. Le sous-titre est réécrit aussi. |
| `a4` → `a7` | = | La courbe x(t) : tracer, lire, composition, palier. |

### Séance 3 — Conductimétrie : établir σ(x) et en tirer x

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `ci_g1_cellule` | = | L'appareil (G = k·σ), nécessaire pour lire l'afficheur dans l'expérience suivante. |
| `ci_g2_ions` | = + **Obs** | L'expérience avant la loi. La voix s'arrête après « دابا نزيدو les ions فهاد المحلول » (« on ajoute des ions dans cette solution ») et la scène joue jusqu'à `monte`. Question : « que fait l'afficheur ? ». La voix reprend et confirme : « l'afficheur كيطلع » (« l'afficheur monte »). |
| `g3`, `g4` | = | σ = Σλ[X], puis pourquoi σ baisse dans l'exemple B (« un ester avec les ions hydroxyde, étudié plus tard »). |
| `g4b`, `g5`, `g5b` | = | Le tableau de l'exemple B, σ(x) établie comme une droite, puis x = x_max·(σ₀ − σ)/(σ₀ − σ_f). Bloc à part : c'est une démonstration en trois marches. |
| `ci_g6_calcul` | = | De la courbe σ(t) à x (question du bloc). |
| `ci_p4_2016R` | D + **R** (une phrase) | Le national 2016 R de conductimétrie suit directement la conductimétrie : l'exercice fixe ce qui vient d'être appris. Dans le texte, « la tangente, on s'en sert **la séance prochaine** » devient « **plus tard** », car la vitesse n'arrive plus à la séance suivante. |

### Séance 4 — Pression, volume de gaz ; choisir sa méthode

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `p1`, `z6`, `p2`, `p3` | = | L'exemple C au labo (bulles et manomètre), puis le rappel des gaz parfaits juste avant la relation, puis le volume de gaz. |
| `ci_p5_choisir`, `ci_p6_2024N` | D | Choisir la méthode selon l'espèce (titrable, ions, gaz), puis le national 2024 N par dosage. Son « la tangente, la séance prochaine » reste vrai. |

### Séance 5 — Vitesse volumique et temps de demi-réaction

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `v1`, `z5`, `v2`, `v3` | = | D'abord ce qu'on voit (les triangles rapetissent), puis le rappel de la pente et de la tangente juste avant, puis la définition, puis la tangente à t = 0. |
| `ci_v4_bareme`, `ci_v6b_espece` | D | Le calcul au barème, puis la même vitesse à partir d'une courbe de réactif ou de [X]. `v6b` termine en retrouvant « la même valeur qu'avec x », celle de `v4`. Les deux sont regroupées : ce sont deux méthodes de calcul. |
| `v5`, `v6`, `v7`, `v8` | = | L'évolution de la vitesse d'un seul tenant : elle diminue (observation existante), pourquoi (réactifs consommés, chocs efficaces, CIN9), nulle sur le palier, puis le rappel de la température. |
| `h1` → `h4` | = | t½ : définition, lecture en quatre gestes, pièges (à 2·t½, la réaction n'est pas finie), puis comparer et choisir la méthode (CIN7). |

### Séance 6 — Sujets du national et bilan

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `ci_n1`, `ci_n2` | = | 2019 R et 2025 R : x_max, vitesse, la vitesse diminue. |
| `ci_n3_deux` | = + **Obs** | 2017 N, le piège le plus fréquent de t½ (x_f/2 de chaque courbe, pas x_max/2). Après « جوج paliers مختلفين » (« deux paliers différents »), une question : « à quelle valeur de x lit-on t½ de la courbe 1 ? » (0,15 / 0,10 / 0,20 mol). La voix confirme ensuite 0,1 mol. |
| `n4` → `n8`, `r1`, `r2`, bilan | = | Inchangés. |

## 3. Ce qui reste, et pourquoi

- **Le tableau d'avancement reste une partie à part** (`a1`, `a1b`, `a2`). Chez les profs, il est rappelé dans la
  première expérience. Nous le plaçons juste avant la mesure de x, ce qui revient au même ordre : le tableau, puis
  la mesure, puis la courbe. L'élève le construit maintenant ligne par ligne (observation de `a1b`).
- **L'ordre conductimétrie puis pression est gardé.** Les profs font pression puis conductimétrie, mais le national
  pratique la conductimétrie (3 sujets) et jamais la pression ces dernières années. On met donc le temps là où
  l'examen le demande.
- **G = k·σ est expliqué** (`g1`), alors qu'aucun prof ne le fait. Le cadre (CIN3) le cite, et l'élève lit G en mS au
  national 2018 R.
- **Les chocs efficaces** sont en `v6` et `v8`, après l'observation de la vitesse qui diminue (CIN9 et 2024 N).
- **La carte d'ouverture** (`ci_o1_carte`) nomme encore la trempe avant le tableau d'avancement. Sa voix et sa
  simulation sont gardées : c'est un aperçu, pas un ordre d'enseignement. À aligner quand la carte sera revoicée.

## 4. Besoins hors de ce cours (fichiers partagés, non modifiés)

- `ci_a1b_en_cours`, `ci_m3b_calcul` et `ci_g5b_rapport` continuent la scène de la diapositive d'avant (même URL).
  Il faudrait `?depart=<moment>` dans le kit partagé `shared/tableau/tableau.js`, qui ne l'a pas encore.
- `ci_cr_carte` : `demarrer = start`. Même ajout au kit nécessaire.
- Correction faite au passage : une réaction écrite d'un exercice de bloc (`ci_s2_b1`) écrivait « lambda » en
  lettres ; elle écrit maintenant le symbole λ (`verifier_formules.py` : 0).
