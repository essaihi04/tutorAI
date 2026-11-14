# Audit « animations au lieu de tableaux » — mathématiques (ch. 1 à 6)

Règle (14 novembre 2026, professeur règle 28, cours-concentration étape 3) : une diapo qui compare des valeurs, montre l'effet
d'un paramètre ou décrit des étapes montre une petite animation à la craie que l'élève manipule (un bouton, au plus deux
curseurs) ; les valeurs sont le RÉSULTAT de ce qu'on voit. La voix enregistrée (`speech_text`, `audio`) n'a pas été touchée :
les `pointage` sont réécrits sur des extraits exacts du texte mixte (chaque `mot` vérifié comme sous-chaîne par le script de
câblage), et une `variante` (le tuteur change le curseur 5 s après la voix, puis montre le repère) est ajoutée.

## Constat général

- Les six cours n'ont **aucune** diapo avec `screen_content.table`, et **toutes** les diapos ont déjà une simulation à la craie.
- Les diapos-concepts ont déjà leurs constructions manipulables (poignées) : approche, projections, traversée, sécante,
  famille de primitives, pente, plan complexe, argument, Moivre…
- Les candidates sont donc les diapos dont la simulation est `calculs.html` (une rédaction écrite ligne par ligne) alors que
  la notion est une comparaison, l'effet d'un paramètre ou une suite d'étapes, **et** dont la voix décrit le phénomène plutôt
  que les lignes écrites. Quand la voix lit la rédaction (« السطر اللول », « بالأحمر »…), l'animation contredirait la voix :
  ces diapos sont notées « nécessite une nouvelle voix » ou laissées (rédaction exigée par le barème).
- Écartées d'office : fiches bilan, cartes du chapitre, rappels « trois gestes », sujets nationaux rédigés.

## Kit commun : curseurs

`frontend/public/media/simulations/maths/commun/maths-tableau.js` : une vue peut déclarer `curseurs: ['p', …]` (au plus deux).
Chaque paramètre listé reçoit un curseur à la craie dans la barre, à côté du bouton ; l'élève le glisse et la construction se
réécrit aussitôt (`set_parameters` par l'élève, bulle de lecture) ; quand le tuteur envoie `set_parameters` ou `reset`, le
curseur suit. Options du paramètre : `label`, `unite`, `decimales`, `affiche(v)` (valeur affichée, ex. un indice → « 1000 »).
Les vues sans `curseurs` ne changent pas (vérifié sur `suites-tableau/plafond.html`).

## Ch. 1 — Limites et continuité (`math_ch1_limites_continuite`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `lc_l7_plus_lourd` | `calculs.html?vue=l7_lourd` : calcul écrit, 4 puces (règle, exemple, « seulement à l'infini ») | Deux barres : le haut partagé entre 3x² et 1, le bas entre x² et x ; x grandit de 2 à 1000, 3x² et x² mangent toute la barre (part du terme léger écrite : 1 : 0,00003 %), f(x) ≈ 3,003 écrit ; en orange, en un point on remplace (13/2). Curseur x = 2 … 10 000 | **Oui** — `limites-continuite-tableau/lourd.html?vue=lourd` (puces 3–4 retirées, les deux règles gardées) |
| `lc_l12_sinus` | `calculs.html?vue=l12_sinus` | sin(kx)/(kx) → 1 avec un curseur x qui rétrécit | Non : la voix est une chaîne algébrique (3/2 × …, on pose t = 3x) — **nécessite une nouvelle voix** |
| `lc_l4_formes` | liste des quatre formes | — | Non : catalogue à mémoriser, aucun paramètre |
| `lc_d4_recommencer` | puces « étape 2, étape 3, le tableau » | — | Non : `dichotomie.html?vue=etapes` déroule déjà les étapes en animation |
| `lc_l2`, `l5`, `l6`, `l13`, `c5`, `t6`, `r4`, `r8`, `r9`, `n3`–`n7`, `p1`–`p3`, `lr2`–`lr4`, `e1` | `calculs.html` | — | Non : rédactions demandées au national, la voix lit les lignes |
| `lc_o1_carte`, `lc_o2_bases`, `lc_e2_bilan`, `lc_e3_carte` | — | — | Exclues (carte, rappels, bilan) |

## Ch. 2 — Dérivation et étude de fonctions (`math_ch2_derivation_etude_fonctions`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `df_va6_extremum` | `calculs.html?vue=va6` : tableau de x + 1/x, puis l'inégalité écrite | Le tableau de variations à droite ; un point descend la courbe de x + 1/x jusqu'à (1 ; 2) puis remonte, ses valeurs écrites ; la droite y = 2 sous toute la courbe ; un point d'essai (curseur x de 0,2 à 5) avec « f(x) = … ≥ 2 » ; x + 1/x ≥ 2 encadré | **Oui** — `derivation-tableau/minimum.html?vue=minimum` (puces 1–2 retirées, la règle « minimum positif » gardée) |
| `df_va3_factoriser`, `df_va5_double_barre` | tableau de signe écrit | Point qui glisse sur la courbe de f′ et allume + / − | Non : le tableau de signe est une sortie exigée et la voix lit ses lignes — **nécessite une nouvelle voix** pour l'animation « pourquoi » |
| `df_va7_auxiliaire` | partie I → partie II | Signe de g lu sur sa courbe, reporté sur f′ | Non : **nécessite une nouvelle voix** |
| `df_dv1_tableau` | tableau des dérivées | — | Non : formulaire à mémoriser |
| `df_nd4`, `tg2`, `dt6`, `dv2`–`dv6`, `bi7`, `sy4`, `rec5`, `ec1`–`ec4` | `calculs.html` | — | Non : rédactions |
| `df_c1_carte`, `df_c2_bases` | — | — | Exclues |

## Ch. 3 — Suites numériques (`math_ch3_suites_numeriques`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `su_a5_terme_arith` | `calculs.html?vue=a5` : la formule encadrée et ses deux cas | Une rangée de cases u₀ … u₈ ; des sauts « + r » de la case p à la case n, puis de u₀, puis de u₁ ; « de u₂ à u₆ : n − p = 4 sauts » écrit quand le dernier saut arrive ; exemple u₀ = 2, r = 3 : les valeurs s'écrivent dans les cases, u₆ = 20. Curseurs n et r | **Oui** — `suites-tableau/sauts.html?vue=arith` (les trois puces retirées) |
| `su_a7_terme_geo` | `calculs.html?vue=a7` | Mêmes cases, sauts « × q » ; n = 0 : aucun saut, q⁰ = 1 encadré, on retrouve u₀. Curseur n | **Oui** — `suites-tableau/sauts.html?vue=geo` (les quatre puces retirées) |
| `su_p3_limite_somme` | `calculs.html?vue=p3` | Des morceaux 1, 1/2, 1/4… se posent bout à bout sur une règle ; Sₙ écrit sous le bout (S₇ = 1,9921) ; « il manque … » fond vers 0 ; le mur en 2 ; la formule, la condition, lim Sₙ = 2 encadré. Curseur q (0,1 à 0,9), le mur bouge | **Oui** — `suites-tableau/somme.html?vue=somme` (les trois puces retirées) |
| `su_x5_arithmetique` | différence constante / multiplication constante | Réutiliser `sauts.html` (+ r contre × q) | Non : la voix déroule le calcul du national 2021 — **nécessite une nouvelle voix** |
| `su_p1_rang` | inéquation, produit en croix, n ≥ 197 | Points qui franchissent le seuil 0,99 au rang 197 | Non : la voix résout l'inéquation — **nécessite une nouvelle voix** |
| `su_l5_avec_qn` | condition, puis limite | — | Non : `qn.html` existe déjà pour qⁿ ; la voix porte sur la rédaction de la condition |
| `su_a9_sommes` | les deux formules de 1re bac | — | Non : formulaire de rappel |
| `su_r2`–`r8`, `m2`–`m4`, `x2`–`x4`, `c5`, `f5`, `e1`, `o2` | `calculs.html` | — | Non : rédactions de récurrence, de monotonie, de suite auxiliaire |

## Ch. 4 — Primitives (`math_ch4_primitives`)

Aucune animation construite : les notions qui bougent ont déjà leurs constructions manipulables (`famille.html` pour
F + k et la primitive qui passe par un point, `pente.html` pour f = pente de F, `marche.html`, `cercle.html`, `bulle.html`,
`organigramme.html`) ; les 18 diapos sur `calculs.html` sont des rédactions (vérifier une primitive, formes u′uⁿ, u′/u², u′/√u,
u′cos u) dont la voix lit les lignes et les couleurs.

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `pr_e7` | « à toi » : toutes les primitives, F(1) = 3, k = 11/6 | La famille F + k et le curseur k jusqu'à passer par (1 ; 3) | Non : `famille.html?vue=point` le montre déjà sur `pr_e6` ; ici la voix est un calcul long — **nécessite une nouvelle voix** |
| `pr_u3` | le coefficient reste devant, la faute barrée | — | Non : la voix porte sur l'écriture et la faute barrée |
| `pr_e4` | F + k et pas d'autres (démonstration) | — | Non : démonstration ; la famille est déjà animée sur `pr_e3`, `pr_e5` |
| `pr_d3`, `d4`, `e1`, `l2`, `l3`, `c1`, `c4`–`c7`, `c9`, `r2`, `x1`–`x3` | `calculs.html` | — | Non : rédactions |

## Ch. 5 — Fonctions logarithmiques (`math_ch5_fonctions_ln`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `ln_a1` | `calculs.html?vue=a1` : calculatrice dessinée, l'addition, la règle | Trois barres ln 2 ≈ 0,69, ln 3 ≈ 1,10, ln 6 ≈ 1,79 ; ln 2 et ln 3 s'empilent et tombent juste à la hauteur de ln 6 ; 6 = 2 × 3 ; ln(ab) = ln a + ln b encadré. Curseurs a et b (1 à 5) | **Oui** — `ln-tableau/barres.html?vue=produit` (une puce gardée : « Le logarithme d'un produit est la somme des logarithmes. ») |
| `ln_a4` | `calculs.html?vue=a4` | Un bloc = ln a : ln(a²) deux blocs, ln(aⁿ) n blocs, un bloc coupé en deux moitiés (ln √a = ½ ln a), ln(aʳ) = r ln a, puis ln(√2 × 8) = un demi-bloc + trois blocs ln 2 = (7/2) ln 2. Curseurs a (2 à 9) et n (1 à 6) | **Oui** — `ln-tableau/barres.html?vue=puissance` (la puce « ln(aʳ) = r ln a (r ∈ ℚ) » gardée) |
| `ln_l6` | `calculs.html?vue=l6` | Deux barres à la même échelle, x et ln x : les deux grandissent (→ +∞) mais ln x fond à côté de x ; factorisation, (ln x)/x ≈ 0,0069 écrit, la parenthèse → 1, x × (presque 1) → +∞, conclusion en vert. Curseur x = 10 … 1 000 000 | **Oui** — `ln-tableau/plus-fort.html?vue=plus_fort` (les quatre puces retirées) |
| `ln_a6` | ln(a + b) ≠ ln a + ln b ; ln(x²) = 2 ln|x| | Vue « somme » de `barres.html` (ln 2 contre ln 1 + ln 1 = 0) | Non : la moitié de la voix (le carré, la valeur absolue, le domaine) n'aurait pas de support dans l'animation — **nécessite une nouvelle voix** ou une vue mixte |
| `ln_q7` | le plus petit n avec (1/4)ⁿ < 10⁻⁴ | Points (1/4)ⁿ qui passent sous le seuil au rang 7 | Non : la voix déroule le passage au ln — **nécessite une nouvelle voix** |
| `ln_a5`, `a7`, `q2`, `q4`, `q6`, `l7`, `l8`, `v1`, `v2`, `p3`, `o2` | `calculs.html` | — | Non : rédactions (simplifier, résoudre, dériver) |

## Ch. 6 — Nombres complexes (`math_ch6_nombres_complexes`)

| Diapo | À l'écran avant | Animation proposée | Construite ? |
|---|---|---|---|
| `nc_m3` | `calculs.html?vue=m3` : règles, calcul 2017 N, piège barré | En haut, en vert, les trois règles ; dans le plan, a = √3 + i sur le cercle de rayon 2, 1 + i sur celui de rayon √2, le produit (1 + i)a se pose sur le cercle de rayon 2√2 ; à droite |a| = 2, |1 + i| = √2, |(1 + i)a| = 2√2 encadré en jaune, « sans développer » ; en bas, en orange, |1 + (−1)| = 0 mais |1| + |−1| = 2, la phrase |z + z′| = |z| + |z′| barrée. Curseurs : angle de a (le produit tourne, le rayon reste) et |a| | **Oui** — `operations-formes-tableau/modules.html?vue=produit` (les quatre puces retirées ; la mise en page respecte « en haut / en bas » et les couleurs dites par la voix) |
| `nc_c1` | somme puis produit développé | Vecteurs bout à bout pour la somme | Non : la seconde moitié de la voix développe le produit ligne par ligne — **nécessite une nouvelle voix** (ou une vue mixte) |
| `nc_c3`, `nc_j4` | (a + ib)(a − ib) = a² + b² développé | z et z̄ en miroir, a² + b² = |z|² sur l'axe réel, curseurs a, b | Non : la voix suit le développement et ses couleurs — **nécessite une nouvelle voix** |
| `nc_g4` | `angles.html?vue=tableau` (quart de cercle + colonnes) | Point qui glisse sur le quart de cercle | Non : déjà animé ; le tableau des angles est à mémoriser |
| `nc_a5`, `c2`, `c4`, `j2`, `t2`, `t6`, `r5`, `r8`, `n1`, `o2` | `calculs.html` | — | Non : rédactions du national |

## Fichiers créés ou modifiés

Créés (frontend/public/media/simulations/maths/) :
- `limites-continuite-tableau/lourd.html` → `lc_l7_plus_lourd`
- `derivation-tableau/minimum.html` → `df_va6_extremum`
- `suites-tableau/sauts.html` (vues `arith`, `geo`) → `su_a5_terme_arith`, `su_a7_terme_geo`
- `suites-tableau/somme.html` → `su_p3_limite_somme`
- `ln-tableau/barres.html` (vues `produit`, `puissance`) → `ln_a1`, `ln_a4`
- `ln-tableau/plus-fort.html` → `ln_l6`
- `operations-formes-tableau/modules.html` → `nc_m3`

Modifiés :
- `frontend/public/media/simulations/maths/commun/maths-tableau.js` : option `curseurs` (au plus deux curseurs dans la barre).
- `backend/data/courses/math_ch1_limites_continuite.json` (`lc_l7_plus_lourd`), `math_ch2_derivation_etude_fonctions.json`
  (`df_va6_extremum`), `math_ch3_suites_numeriques.json` (`su_a5_terme_arith`, `su_a7_terme_geo`, `su_p3_limite_somme`),
  `math_ch5_fonctions_ln.json` (`ln_a1`, `ln_a4`, `ln_l6`), `math_ch6_nombres_complexes.json` (`nc_m3`) : seulement `visual`,
  `screen_content.bullets` et `concentration.pointage` / `concentration.variante` de ces diapos (comparaison objet par objet
  avant / après : aucune autre diapo, aucune clé de premier niveau changée ; `speech_text` et `audio` identiques).
  Les fichiers gardent leurs fins de ligne CRLF d'origine (copie de travail Windows, `text=auto` normalise au commit).
- `math_ch4_primitives.json` : inchangé.

## Vérifications

- `node --check` sur le script de chaque page et sur `maths-tableau.js` : OK.
- Chaque page chargée dans le navigateur (serveur Vite) : aucun message d'erreur, aucun texte hors du cadre 760 × 420
  (garde-fou `__horsCadre`), y compris aux valeurs extrêmes des curseurs ; tous les `moment` et `repere` utilisés par les
  `pointage` et les `variante` existent dans la page ; captures de la construction complète relues.
- Lecteur de cours (`cours-ondes.html?cours=math_ch3_suites_numeriques&diapo=su_a5_terme_arith`) : la diapo charge la nouvelle
  animation, le professeur pointe les cases au mot dit, les sauts se dessinent. Le volet du navigateur était caché pendant les
  essais (animations ralenties), donc le calage fin voix / arrêts sur image reste à regarder volet visible.
