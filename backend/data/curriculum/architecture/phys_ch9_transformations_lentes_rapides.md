# Architecture — Transformations lentes et transformations rapides (phys_ch9)

Revue de la logique du 18 novembre 2026 (skill `logique-de-cours`). La nouvelle version se trouve dans
`backend/data/courses/en_attente/phys_ch9_transformations_lentes_rapides.json`. Le cours en ligne n'est pas touché.
Les pistes à mettre en voix sont dans `phys_ch9_transformations_lentes_rapides_voix.json` : 34 pistes, dont 1 diapositive.

## 1. Sources et constats

**Profs (5 cours lus).** Le relevé complet est dans `sources_chimie_ch9_ch11.md`, chapitre A. Les cours lus :
- Mahajar et Tabit (AlloSchool, Cours 1, aussi sur pc1.ma) ;
- un cours sans auteur (AlloSchool, Cours 2) ;
- Bendaoud (AlloSchool, Cours 3) ;
- Sbiro (pc1.ma, repris par El Goufifa) ;
- Karzazi (résumé de sa vidéo).

L'ordre commun des profs :
1. rappel d'oxydoréduction : définitions, demi-équations, combinaison des deux couples ;
2. transformations rapides puis lentes, chaque fois une définition et un exemple. Pour les lentes, H₂O₂ + I⁻ revient dans les 5 cours et le thiosulfate en milieu acide dans 4 ;
3. facteurs cinétiques : la température, la concentration ;
4. applications : la trempe, le réfrigérateur, l'autocuiseur.

Ce que font peu de profs : le catalyseur n'est qu'une remarque chez 3 profs sur 5, et le tableau d'avancement n'apparaît que dans un exercice.

**Cadre.** Fiche `transformations_lentes_rapides`, capacités TLR1 à TLR7. Le sous-domaine 1 donne comme facteurs officiels
la température et la concentration ; le catalyseur relève du sous-domaine 4, il est présenté ici sans types de catalyse.
« Chocs efficaces » est hors de ce cours : c'est la capacité CIN9 du ch10.

**National (2016-2025, `backend/data/exams/physique`).**
- Demi-équations et couples Ox/Red : environ 17 sessions sur 20. On les écrit surtout dans les parties piles et électrolyse.
- Facteurs cinétiques ou catalyseur, demandés explicitement :
  - 2018 N : deux facteurs pour accélérer ;
  - 2023 N : la courbe avec catalyseur ;
  - 2024 N : vrai ou faux sur la concentration ;
  - 2025 N : trois expériences.
- Trempe : 2017 R.

La carte d'ouverture dit « facteurs cinétiques dans dix sessions » (voix déjà faite). Notre relevé par mots-clés n'en
trouve qu'environ 5 de façon explicite : **chiffre à vérifier** avant la prochaine voix de `tl_o1_carte`.

**Logique du cours en ligne : ce qui n'allait pas.**
1. La mole, la concentration et le réactif limitant (`rp3`–`rp5`) étaient enseignés avant « rapide ou lente », qui
   n'en a pas besoin. Pourtant `rp3` commence lui-même par « قبل les facteurs cinétiques » (« avant les facteurs
   cinétiques »). La règle 6 veut un prérequis enseigné quand il sert.
2. `tl_f1_facteur` affirmait « la température et la concentration sont des facteurs cinétiques » avant les deux
   expériences qui le montrent (`f2`, `f5`). Cela va contre la règle 4 : l'expérience vient avant le résultat.
3. `r8` (Peut-on changer la durée ?) et `f1` étaient deux diapositives de suite avec la même simulation (`facteurs.html?vue=une_variable`).
   Les `play_until` de `f1` étaient alors refusés, puisque la scène était déjà jouée.
4. Le bloc de `r8` et des bains portait deux questions qui demandaient la même chose : la prédiction de `r8`, puis
   « quel bécher finit le premier » de `f2`, posée après que la voix l'avait dit.
5. Pour la concentration, le cas décisif était donné par la voix sans laisser l'élève le voir lui-même (`f5`). Il n'y
   avait pas de question au bon moment.
6. Le national 2025 N (`n1`) était entièrement dit, sans question avant la réponse (règle 5).
7. `r6_classer` s'appelle « À toi de trier » mais n'avait aucun tableau « À toi ».

## 2. Nouvelle architecture, diapositive par diapositive

La colonne « Voix » vaut **=** quand la diapositive garde son id, son texte et donc sa voix, **D** quand elle est
seulement déplacée (sa voix est gardée), **R** quand son texte est réécrit (sa voix est à refaire). **Obs** signale
une question d'observation ajoutée.

### Séance 1 — Les bases ; oxydants, réducteurs, demi-équations (inchangée)

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `tl_o1_carte` | = | Carte du chapitre : l'élève sait où il va. |
| `tl_rp1_ion` | = | L'ion, enseigné de zéro, sert dès l'expérience du zinc (règle 6). |
| `tl_rp2_conservation` | = | La conservation des atomes et des charges sert à toutes les demi-équations qui suivent. |
| `tl_x1_zinc` | = + **Obs** | Première expérience du chapitre, jouée avant les mots oxydant et réducteur (règle 4). Nouvelle question d'observation : « Que voit-on apparaître sur la lame ? ». La voix s'arrête après « دابا كنخليو الوقت يدوز » (« on laisse le temps passer ») et la scène va jusqu'au dépôt. La voix reprend ensuite et confirme : « un dépôt rouge ». Chez les profs, l'expérience d'ouverture est Cu dans Ag⁺ ; nous gardons Zn + Cu²⁺ (Bendaoud), dont la simulation et la voix existent déjà. |
| `x2` → `x3b` | = | Oxydant, réducteur, oxydation, réduction et couple, une idée par diapositive. Ordre des profs. |
| `x4` → `x6b` | = | Les demi-équations en quatre gestes : permanganate, puis eau oxygénée et diiode, qui sont les couples du national. |

### Séance 2 — L'équation d'oxydoréduction ; rapide ou lente

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `x7` → `x10` | = | De deux demi-équations à l'équation, puis la vérification. Ordre des profs et du cadre (TLR3). |
| `tl_r1_bechers` | = | Rapide et lente, vues ensemble dans une même expérience. La question d'observation existante demande quel bécher se décolore tout de suite, avant que la voix le dise. |
| `r2`, `r3`, `r4` | = | Chaque transformation est montrée seule, puis vient sa définition (règle 33). |
| `r5`, `r6`, `r7` | D | L'échelle des durées, le tri, puis le titrage (une réaction rapide utile, qui resservira au ch10). **Nouveau :** l'exercice de tri qui était en réserve monte au tableau de `r6`, avec ses réactions, pour qu'« À toi de trier » le soit vraiment. Bloc renommé : « Classer ; le titrage, une réaction rapide utile ». |

### Séance 3 — Compter ; la température et la concentration, facteurs cinétiques

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `tl_rp3_mole` | D | La mole, enseignée juste avant son premier usage : le tableau des expériences de `r8` en mol/L. Son propre texte dit « قبل les facteurs cinétiques » (« avant les facteurs cinétiques »). |
| `tl_rp4_concentration` | D | C = n/V, juste avant les expériences où seule la concentration change. Sa question (C = 0,02/0,5) devient la question du bloc. |
| `tl_r8_duree` | D | Le tableau des trois expériences, puis une prédiction : « dans un bain plus chaud ? ». C'est la question posée **avant** de voir. |
| `tl_f2_bains` | D | L'expérience qui répond à la prédiction : chaud et froid, même état final. Sa question, qui redemandait ce que la voix venait de dire, part dans la réserve de fin de cours (texte, réactions et voix gardés). Elle ne répète plus `r8`, et il n'y a plus qu'un tableau par bloc. |
| `tl_f1_facteur` | **R** | Le nom « facteur cinétique » vient **après** l'expérience qui le montre. Le texte est réécrit en 5 étapes : 1) « on a vu : seule la température a changé, et la durée a changé » ; 2) la définition, lue mot à mot ; 3) une deuxième façon de le dire, la nourriture sur le feu (mots du corpus vérifiés, plus de « النار » ni de « كتطيب », vus 0 ou 1 fois) ; 4) la règle d'une seule variable, avec la flèche 1 → 2 du tableau ; 5) l'annonce de la concentration. Placée entre `f2` et `f3`, elle n'a plus la même simulation que la diapositive d'avant. |
| `tl_f3_agitation` | = | Pourquoi la chaleur accélère : l'agitation et les rencontres. Le mot « chocs efficaces » est gardé pour le ch10, comme le veut le cadre. |
| `tl_f4_courbes` | = | Les courbes à deux températures : même palier, montée plus raide au chaud. |
| `tl_f5_concentre` | = + **Obs** | La concentration, seule variable qui change. Nouvelle question d'observation : « Lequel brunit le premier ? ». La voix s'arrête après « دابا نخلطو، ونطلقو le chronomètre » (« on mélange et on lance le chronomètre »). La simulation cache sa conclusion (`conclusions: false`) jusqu'à la réponse. La question écrite, qui demandait la même chose après la voix, part dans la réserve. |
| `tl_f6_rencontres` | = | Pourquoi la concentration accélère, après l'expérience. |
| `tl_rp5_avancement` | D | L'avancement et le réactif limitant, juste avant la diapositive qui s'en sert (le palier vaut la quantité initiale de H₂O₂). Avant, il venait 15 diapositives plus tôt. |
| `tl_f7_palier` | = | Les courbes à deux concentrations : même palier, car H₂O₂ est le réactif limitant. |
| `tl_f8_variable` | = | La règle d'une seule variable à la fois. **Nouveau :** l'exercice en réserve « pour étudier la concentration, on compare… » monte au tableau. C'est la question du bloc. |

### Séance 4 — La trempe, le catalyseur, deux nationaux et le bilan

| Diapo | Voix | Pourquoi ici |
|---|---|---|
| `t1` → `t4` | = | La trempe, la vie quotidienne, puis le catalyseur, montré en expérience avant sa définition (sans types de catalyse) et suivi de la courbe du national 2023 N. |
| `tl_n1_lecture` | = + **Obs** | National 2025 N, joué pas à pas. Après « فيه تلاتة courbes: a، b، و c » (« il y a trois courbes : a, b et c »), une question avant la réponse : « Laquelle correspond à l'expérience 3 (θ₂ et le catalyseur) ? ». La voix enchaîne ensuite sur la lecture du début des courbes, qui confirme la réponse. |
| `tl_n2_glacee` | = | National 2017 R : la trempe rédigée comme le barème, puis deux facteurs. |
| `tl_bl_fiche`, `tl_cr_carte` | = | Bilan. |

**Compétences :** C1 à C7 sont inchangées. Les identifiants de toutes les diapositives sont gardés.

## 3. Ce qui reste, et pourquoi

- **L'ordre des profs est gardé** pour l'oxydoréduction, puis rapide/lente, puis les facteurs et les applications.
  L'élève le retrouve chez son prof.
- **Le catalyseur garde une expérience** (`t3`), alors que chez les profs ce n'est qu'une remarque. Le national 2023 N
  et le 2025 N demandent de reconnaître sa courbe, et la décision de la fiche du cadre le prévoyait.
- **Les profs commencent par Cu + Ag⁺, nous par Zn + Cu²⁺** : la simulation et la voix existent déjà, et cette réaction est celle des piles du national.
- **Trois questions d'observation de plus** (cinq au total pour 43 diapositives), alors que l'ancienne limite était de
  0 à 2 par cours. La demande du 18 novembre (« laisser à l'élève le temps de trouver seul », règle 3 de
  `logique-de-cours`) l'emporte. Chacune est placée sur un cas décisif où la simulation montre la chose à remarquer.

## 4. Besoins hors de ce cours (fichiers partagés, non modifiés)

- `tl_x2`, `x3b`, `x5`, `r2`, `r6` ont la même simulation que la diapositive d'avant. C'est voulu : elles continuent
  la scène. Mais le lecteur refuse les `play_until` déjà passés. Il faudrait l'ouverture figée `?depart=<moment>`
  dans le kit partagé (`shared/tableau/tableau.js`), qui ne l'a pas encore.
- `tl_cr_carte` : `demarrer = start`. Il faudrait passer en `reset` avec `?depart=`, ce qui demande le même ajout au kit.
- `facteurs.html` : à vérifier dans le navigateur que `conclusions: false` cache bien la conclusion de la vue
  `concentration` (`f5`) jusqu'à la réponse.
