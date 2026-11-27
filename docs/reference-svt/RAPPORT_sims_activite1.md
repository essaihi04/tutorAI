# Rapport — simulations de l'activité 1 (cours de référence SVT « Consommation de la matière organique »)

Dossier : `frontend/public/media/simulations/svt/reference_consommation_mo-tableau/`. Contrat : `docs/reference-svt/ARCHITECTURE.md` § 2 et § 3.
Ce rapport liste, pour chaque page, les moments, les repères et les paramètres réellement en place (relevés par un script
dans un navigateur, pas recopiés du contrat).

## Fichiers

| Fichier | Rôle |
|---|---|
| `demarche.js` | Le fil de la démarche : `window.Demarche.dessiner(c)`, `?demarche=1..6`, repère `demarche`. |
| `reference.js` | `Ref.page` (page racontée : moments, `?depart=`, `play_until`, `set_time`, `set_parameters`, `allume`, téléphone avec foyer et bandeau), `Ref.pchip` (courbes passant par les points du document), matériel d'ExAO peint (`cuve`, `barreau`, `agitateur`, `sonde`, `seringue`, `cable`, `boitier`, `ordinateur`, `loupe`, `bulles`). |
| `pate.html`, `levure.html`, `exao-levures.html` (`?vue=montage` \| `exp1` \| `exp2`), `equation.html` (`?vue=respiration` \| `fermentation`), `deux-levures.html`, `comparer.html`, `marquage.html` | Les pages. |

## Ce qui vaut pour toutes les pages

- Un moment = l'instant (en secondes de la scène) où l'animation de son étape est finie ; l'animation occupe l'intervalle
  depuis le moment précédent. Figée sur un moment, la page ne montre rien de l'étape suivante.
- Commandes : `start`, `reset`, `pause`, `resume`, `set_time {time_s | moment}`, `play_until {moment | time_s, duree_s}`,
  `set_parameters`, `allume {cible}`, `eteins`, `highlight {target}`. `?depart=<moment>` ouvre la page figée ; `?depart=0`
  l'ouvre figée au début.
- Paramètre commun : `set_parameters {demarche: 0..6}` (et `?demarche=` dans l'URL). Aucune page n'a d'autre paramètre.
- Repère commun : `demarche` (présent seulement avec `?demarche=`).
- Sur téléphone (cadre sous 560 × 300), la page zoome sur l'objet de l'étape et écrit la phrase de l'étape dans un bandeau
  en bas ; les repères de phrases pointent alors ce bandeau.

## Vérifications faites

- Captures Playwright regardées pour chaque page et chaque vue à 760 × 420, 1366 × 560 et 429 × 250 (tous les moments à
  760 × 420 ; les moments principaux aux deux autres tailles ; des milieux d'étape pour les pages animées). 1100 × 560 :
  regardé sur `exao-levures.html?vue=exp1` et `deux-levures.html` seulement.
- Console sans erreur et aucun texte « hors cadre » sur toutes les pages.
- `python -I scripts/verifier_formules.py` sur le dossier : 0 relation à reprendre.
- Pilotage comme le lecteur, sur les 10 pages / vues : depuis `?depart=0`, `play_until` de chaque moment dans l'ordre
  arrive figé sur l'instant exact ; `highlight` entoure les repères ; `set_parameters {demarche}` est pris ; `reset`
  revient au départ ; `?depart=<moment>` ouvre figé ; un `play_until` vers un moment passé ne rembobine pas. 0 écart.
- Cohérence avec le cours (`backend/data/courses/svt_ch1_reference_consommation_mo.json`) : tous les moments, repères et
  `depart=` que les diapos appellent sur ces pages existent : 19 diapos, 76 appels (`play_until`, `highlight`…), 0 nom
  inconnu.
- Données du § 2 : les courbes passent exactement par les points du document (5,3 mg/L et 0,16 mmol/L avant 1,8 min ;
  O₂ nul à 6,8 min ; 0,31 mmol/L ; 190 s ; 44 et 34 mg/mL à 700 s ; tableau du ¹⁴C case par case).

## Ce qui n'a pas pu être vérifié

- **Le minutage voix ↔ animation.** `frontend/scripts/verifier-pointage-navigateur.mjs --sim exao-levures.html` a tourné,
  mais les pistes de voix n'existent pas encore (durée lue : 0 s) : ses « moments jamais atteints » viennent de là. À
  relancer quand les voix seront générées. Les durées des étapes (3 à 10 s) sont à comparer alors aux phrases ;
  `play_until {duree_s}` permet de les ajuster sans toucher aux pages.
- L'ouverture dans le lecteur de cours (`/dev/course-player`) n'a pas été faite ; les largeurs 1024 et 1280 non plus.
- La police Patrick Hand vient de Google Fonts : si elle ne se charge pas, les largeurs de texte changent un peu.


## `pate.html`

Diapo `rf_o1_pate`. Scène de cuisine peinte ; aucune réponse à la question n'est écrite.

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `bol` | 4 | un bol, une pâte plate, un sachet de levure de boulanger | `pate`, `bol`, `sachet` |
| `levure_ajoutee` | 11,5 | la levure est versée dans la pâte, puis mélangée | — |
| `gonfle` | 21 | une heure plus tard : la pâte a doublé de volume, des bulles affleurent | `horloge`, `bulles` |
| `zoom` | 27,5 | à la loupe : dans la pâte, des levures et des bulles de CO2 | `levures` |
| `question` | 32 | le problème : d’où la levure tire-t-elle son énergie ? | `question` |

Points imparfaits : Rien n'écrit « × 2 » : le doublement se lit par le dôme et l'horloge (10 h → 11 h).

## `levure.html`

Diapo `rf_r3_levure`. Trois tableaux qui se remplacent : microscope + champ, la cellule légendée, les deux bocaux.

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `microscope` | 9 | le microscope optique ; une goutte de suspension de levures sur la lame | `microscope`, `lame` |
| `champ` | 15 | le champ du microscope : des levures bourgeonnantes ; barre d’échelle 1,5 µm | `champ`, `echelle` |
| `leg_paroi` | 21 | une levure agrandie, en coupe : la paroi | `nom_paroi`, `cellule`, `paroi`, `membrane`, `noyau`, `vacuole`, `hyaloplasme`, `mitochondrie`, `mitochondrie_2`, `mitochondrie_3` |
| `leg_membrane` | 24,5 | la membrane | `nom_membrane` |
| `leg_noyau` | 28 | le noyau | `nom_noyau` |
| `leg_vacuole` | 31,5 | la vacuole | `nom_vacuole` |
| `leg_hyaloplasme` | 35 | le hyaloplasme | `nom_hyaloplasme` |
| `leg_mitochondrie` | 39 | les mitochondries | `nom_mitochondrie` |
| `une_cellule` | 43 | la levure : une seule cellule (unicellulaire) | `unicellulaire` |
| `aerobie` | 52 | bocal ouvert : aéro·bie, vit avec dioxygène | `bocal_ouvert`, `mot_aerobie`, `sens_aerobie` |
| `anaerobie` | 61 | bocal fermé : an·aéro·bie, vit sans dioxygène | `bocal_ferme`, `mot_anaerobie`, `sens_anaerobie` |

Points imparfaits : La barre « 1,5 µm » imposée par le contrat fait paraître les levures plus petites qu'en réalité (≈ 5 µm) : un inspecteur peut le relever ; à corriger dans le contrat si l'on veut (une valeur de 5 µm serait juste). Les noms des pièces du microscope s'écrivent d'un bloc à la fin de `microscope`.

## `exao-levures.html?vue=montage`

Diapo `rf_a1_montage`. Un élément par moment, son nom et son rôle écrits sous le montage (la phrase précédente est remplacée).

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `bioreacteur` | 2,6 | le bioréacteur : une cuve en verre | `agitateur`, `bioreacteur`, `legende` |
| `suspension` | 6,2 | la suspension de levures (la loupe les montre de près) | `suspension`, `levures` |
| `agitateur` | 9,4 | l’agitateur magnétique : le barreau tourne | — |
| `sonde_o2` | 12,6 | la sonde à dioxygène | `sonde_o2` |
| `sonde_co2` | 15,8 | la sonde à dioxyde de carbone | `sonde_co2` |
| `seringue` | 19 | la seringue de glucose | `seringue` |
| `interface` | 22,6 | l’interface, reliée aux sondes | `interface` |
| `ordinateur` | 26,6 | l’ordinateur : écran allumé, axes vides | `ordinateur`, `ecran` |
| `complet` | 30 | le montage complet : ExAO | — |

Points imparfaits : Le socle de l'agitateur est présent dès le départ, à l'arrêt ; il s'allume à son moment.

## `exao-levures.html?vue=exp1`

Diapos `rf_a1_exp1_avant` (`depart=0`), `rf_a1_exp1_injection` (`depart=avant`), `rf_a1_exp1_deduire` (`depart=co2_monte`). Arrêt pour l'observation = figé sur `injection` : les courbes s'arrêtent à 1,8 min. Après l'arrêt, les voies sont montrées une à une : le curseur de temps revient à 1,8 min au début de `co2_monte`.

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `axe_temps` | 3,6 | l’axe horizontal : le temps, en minutes | `bioreacteur`, `suspension`, `agitateur`, `sonde_o2`, `sonde_co2`, `seringue`, `levures`, `interface`, `ordinateur`, `ecran`, `axe_temps` |
| `axe_o2` | 7,6 | l’axe du dioxygène dissous, en mg/L | `axe_o2` |
| `axes` | 11,4 | l’axe du CO2, en mmol/L : les deux axes sont lus | `axe_co2` |
| `avant` | 17 | avant le glucose : deux paliers, 5,3 mg/L et 0,16 mmol/L | `courbe_o2`, `courbe_co2`, `valeur_o2`, `valeur_co2`, `valeurs_lues` |
| `injection` | 21 | injection du glucose à 1,8 min | `fleche_injection` |
| `o2_baisse` | 31 | le dioxygène baisse jusqu’à 0 vers 6,8 min | `o2_nul` |
| `co2_monte` | 39 | le CO2 monte de 0,16 à 0,31 mmol/L | `valeur_finale_co2` |
| `decrire_avant` | 43,5 | description : avant l’injection | `description_avant` |
| `decrire` | 48,5 | description : après l’injection | `description_apres` |
| `deduire` | 53 | déduction : respiration cellulaire | `conclusion` |

Points imparfaits : Axes choisis : O₂ de 0 à 7 mg/L, CO₂ de 0 à 0,5 mmol/L (le document ne donne que les graduations).

## `exao-levures.html?vue=exp2`

Diapos `rf_a1_exp2_axes` (`depart=0`), `rf_a1_exp2_phase1` (`depart=depart_valeurs`), `rf_a1_exp2_phase2` (`depart=o2_zero`). Arrêt pour l'observation = figé sur `o2_zero` : tout s'arrête à 190 s. Ensuite CO₂, éthanol, glucose l'un après l'autre (le curseur revient à 190 s à chaque fois).

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `axe_temps` | 4,2 | l’axe horizontal : le temps, en secondes (60 s = 1 min) | `bioreacteur`, `suspension`, `agitateur`, `sonde_o2`, `sonde_co2`, `bouchon`, `levures`, `interface`, `ordinateur`, `ecran`, `axe_temps`, `rappel_temps` |
| `axe_gauche` | 7,8 | l’axe de gauche, en mg/mL | `axe_gauche` |
| `axes` | 11,4 | l’axe de droite : le glucose ; les axes sont lus | `axe_droit` |
| `depart_valeurs` | 18 | les valeurs de départ : O2 6, glucose 42, CO2 3, éthanol 0 | `depart_o2`, `depart_glu`, `depart_co2`, `depart_eth`, `valeurs_lues` |
| `phase1` | 27 | de 0 à 190 s : O2 tombe à 0, CO2 presque constant, pas d’éthanol | `courbe_glucose`, `courbe_co2`, `courbe_ethanol`, `courbe_o2` |
| `o2_zero` | 30 | à 190 s (environ 3 min) : plus de dioxygène | `instant_190` |
| `co2_monte` | 38 | après 190 s, le CO2 monte jusqu’à 44 mg/mL | — |
| `ethanol_apparait` | 46 | l’éthanol apparaît et monte jusqu’à 34 mg/mL | — |
| `glucose_continue` | 53 | le glucose continue de baisser | — |
| `fin` | 57 | à 700 s : CO2 44, éthanol 34 | `final_co2`, `final_eth` |
| `decrire_avant` | 61,5 | description : de 0 à 190 s | `description_avant` |
| `decrire` | 66,5 | description : après 190 s | `description_apres` |
| `deduire` | 71 | déduction : fermentation alcoolique | `conclusion` |

Points imparfaits : Le rappel « 60 s = 1 min » est effacé quand la description commence. L'axe du glucose (unités arbitraires) a la même échelle que l'axe de gauche.

## `equation.html?vue=respiration`

Diapo `rf_a1_equation_respi`.

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `glucose` | 4,5 | le glucose : une chaîne de 6 carbones, C6H12O6 | `glucose`, `carbone_1`, `carbone_2`, `carbone_3`, `carbone_4`, `carbone_5`, `carbone_6` |
| `o2` | 13,5 | 6 molécules de dioxygène, comptées : 6 O2 | `o2_1`, `o2_2`, `o2_3`, `o2_4`, `o2_5`, `o2_6`, `o2` |
| `fleche` | 16 | la flèche de la réaction : la respiration | `fleche` |
| `co2` | 26 | 6 CO2 sortent : les 6 carbones du glucose partent un par un | `co2_1`, `co2_2`, `co2_3`, `co2_4`, `co2_5`, `co2_6`, `co2` |
| `eau` | 35 | 6 molécules d’eau : 6 H2O | `eau_1`, `eau_2`, `eau_3`, `eau_4`, `eau_5`, `eau_6`, `eau` |
| `energie` | 39 | beaucoup d’énergie libérée | `energie` |
| `equation` | 46 | l’équation : C6H12O6 + 6 O2 → 6 CO2 + 6 H2O + énergie | `equation` |

Points imparfaits : Avant le moment `equation`, le bas du cadre est vide. Un seul oxygène vole de chaque O₂ vers chaque H₂O (choix : ne pas montrer l'oxygène du dioxygène partir dans le CO₂).

## `equation.html?vue=fermentation`

Diapo `rf_a1_equation_ferm`. Même disposition que la respiration pour comparer ; petit éclat (≈ moitié du rayon).

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `glucose` | 4,5 | le glucose : une chaîne de 6 carbones, C6H12O6 | `glucose`, `carbone_1`, `carbone_2`, `carbone_3`, `carbone_4`, `carbone_5`, `carbone_6` |
| `fleche` | 7,5 | la flèche de la réaction : la fermentation, sans dioxygène | `fleche` |
| `ethanol` | 14,5 | 2 molécules d’éthanol, 2 carbones chacune | `ethanol_1`, `ethanol_2`, `ethanol` |
| `co2` | 19,5 | 2 molécules de CO2 | `co2_1`, `co2_2`, `co2` |
| `compte` | 27,5 | les carbones comptés : 2 × 2 + 2 × 1 = 6, rien n’est perdu | `c_1`, `c_2`, `c_3`, `c_4`, `c_5`, `c_6`, `compte` |
| `energie` | 31 | peu d’énergie libérée | `energie` |
| `reste` | 35 | l’éthanol garde de l’énergie | `reste` |
| `equation` | 42 | l’équation : C6H12O6 → 2 C2H5OH + 2 CO2 + énergie (peu) | `equation` |

Points imparfaits : En mode large, peu de molécules : de l'air autour.

## `deux-levures.html`

Diapos `rf_a2_deux_levures` et `rf_a2_localisation` (`depart=legendes`). Arrêt pour l'observation = figé sur `anaerobie` : rien d'allumé, compté ni légendé.

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `aerobie` | 3,6 | le cliché de la levure du milieu aérobie | `echelle`, `levure_aerobie`, `noyau`, `vacuole`, `hyaloplasme_aerobie`, `titre_aerobie` |
| `anaerobie` | 7,2 | le cliché de la levure du milieu anaérobie : les deux clichés côte à côte | `echelle_anaerobie`, `levure_anaerobie`, `noyau_anaerobie`, `vacuole_anaerobie_1`, `vacuole_anaerobie_2`, `vacuole_anaerobie_3`, `hyaloplasme`, `titre_anaerobie` |
| `mitochondries_aerobie` | 19,2 | milieu aérobie : 8 mitochondries, grandes | `mito_a1`, `mito_a2`, `mito_a3`, `mito_a4`, `mito_a5`, `mito_a6`, `mito_a7`, `mito_a8`, `mitochondries_aerobie`, `total_aerobie` |
| `mitochondries` | 24,6 | milieu anaérobie : 2 mitochondries, petites | `mito_b1`, `mito_b2`, `mitochondries_anaerobie`, `total_anaerobie` |
| `leg_noyau` | 27,4 | légende : noyau | `legende_noyau` |
| `leg_vacuole` | 30,2 | légende : vacuole | `legende_vacuole` |
| `leg_hyaloplasme` | 33 | légende : hyaloplasme | `legende_hyaloplasme` |
| `legendes` | 36 | les quatre légendes : noyau, vacuole, hyaloplasme, mitochondrie | `legende_mitochondrie` |
| `conclusion_respiration` | 40,4 | respiration ↔ mitochondries | `conclusion_respiration` |
| `conclusion` | 45,4 | fermentation ↔ hyaloplasme (pas besoin de mitochondries) | `conclusion` |

Points imparfaits : Sur téléphone, dans la vue des deux clichés ensemble, les crêtes ne se lisent plus (≈ 17 px par mitochondrie). Trois numéros du cliché aérobie sont posés sur la paroi.

## `comparer.html`

Diapos `rf_a2_tableau` et `rf_a2_definitions` (`depart=lieu`). Deux moments ajoutés par ligne (`<ligne>_respiration`, `<ligne>_fermentation`) avant le moment imposé où les mots entrent dans le tableau.

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `milieu_respiration` | 4 | milieu aérobie : bocal ouvert, O2 présent | `colonne_respiration`, `colonne_fermentation`, `tableau`, `vignette_respiration`, `vignette_fermentation`, `ligne_milieu` |
| `milieu_fermentation` | 8 | milieu anaérobie : bocal fermé, pas d’O2 | — |
| `milieu` | 11 | ligne « milieu » : aérobie / anaérobie | `case_milieu_respiration`, `case_milieu_fermentation` |
| `gaz_respiration` | 15 | O2 absorbé, CO2 rejeté | `ligne_gaz` |
| `gaz_fermentation` | 19 | pas d’O2 absorbé, CO2 rejeté | — |
| `gaz` | 22 | ligne « gaz » | `case_gaz_respiration`, `case_gaz_fermentation` |
| `glucose_respiration` | 27 | dégradation complète : il ne reste que CO2 et H2O | `ligne_glucose` |
| `glucose_fermentation` | 32 | dégradation incomplète : il reste l’éthanol | — |
| `glucose` | 35 | ligne « glucose » : complète / incomplète | `case_glucose_respiration`, `case_glucose_fermentation` |
| `energie_respiration` | 39 | beaucoup d’énergie | `ligne_energie` |
| `energie_fermentation` | 43 | peu d’énergie : l’éthanol en garde | — |
| `energie` | 46 | ligne « énergie » : beaucoup / peu | `case_energie_respiration`, `case_energie_fermentation` |
| `lieu_respiration` | 51 | hyaloplasme puis mitochondries | `ligne_lieu` |
| `lieu_fermentation` | 55 | hyaloplasme seulement | — |
| `lieu` | 58 | ligne « lieu » | `case_lieu_respiration`, `case_lieu_fermentation` |
| `definition_respiration` | 67 | la définition de la respiration | `definition_respiration` |
| `definitions` | 79 | les deux définitions : respiration, fermentation | `definition_fermentation` |

Points imparfaits : La vignette « lieu » montre une seule mitochondrie alors que la case dit « mitochondries ».

## `marquage.html`

Diapos `rf_a3_marquage`, `rf_a3_glycolyse` (`depart=deux_cultures`), `rf_a3_sans_o2` (`depart=glycolyse`), `rf_a3_avec_o2` (`depart=t5_sans`). Arrêt pour l'observation = figé sur `t5_sans` : la culture avec O₂ est restée à T2. Les deux cultures avancent ensemble de T0 à T2. Les repères `glucose`, `pyruvate`, `ethanol`, `co2`, `krebs`, `dehors`, `hyaloplasme` suivent la culture en cours ; `*_sans` / `*_avec` désignent toujours un côté.

| Moment | Instant (s) | Ce qu'il montre | Repères qui apparaissent |
|---|---|---|---|
| `principe` | 6 | le principe : un glucose dont un carbone est radioactif (¹⁴C), repéré par le compteur | `glucose`, `carbone_marque`, `compteur` |
| `deux_cultures` | 11 | deux cultures de levures : sans dioxygène, avec dioxygène | `culture_sans`, `dehors_sans`, `hyaloplasme_sans`, `mitochondrie_sans`, `dehors`, `hyaloplasme`, `culture_avec`, `dehors_avec`, `hyaloplasme_avec`, `mitochondrie_avec`, `mitochondrie` |
| `t0` | 14,5 | T0 : le glucose marqué est dehors, dans les deux cultures (G+++) | `horloge_sans`, `lecture_sans`, `horloge_avec`, `lecture_avec` |
| `t1` | 18,5 | T1 : le glucose entre dans la cellule (dehors G++, dedans G++) | — |
| `t2` | 23 | T2 : dans le hyaloplasme, chaque glucose est coupé en deux acides pyruviques (P++++), des deux côtés | `pyruvate` |
| `glycolyse` | 28 | la glycolyse : glucose → 2 acides pyruviques, dans le hyaloplasme | `glycolyse`, `definition_glycolyse` |
| `t3_sans` | 33 | T3 sans O2 : éthanol ++, acide pyruvique ++, CO2 ++, dans la cellule | `ethanol`, `co2` |
| `t4_sans` | 37,5 | T4 sans O2 : l’éthanol et le CO2 sortent (dehors E+, CO2++ ; dedans E+, CO2+) | — |
| `t5_sans` | 43 | T5 sans O2 : dehors éthanol ++ et CO2 ++ ; plus rien dedans | `conclusion_sans` |
| `t3_avec` | 48 | T3 avec O2 : l’acide pyruvique entre dans la mitochondrie (CO2+, acides de Krebs +, P++) | `krebs` |
| `t4_avec` | 52,5 | T4 avec O2 : dehors CO2+ ; dedans CO2+ et acides de Krebs + | — |
| `t5_avec` | 58 | T5 avec O2 : dehors CO2 ++++ ; plus rien dedans | `conclusion_avec` |
| `tableau` | 68 | le tableau du document, de T0 à T5 | `t0`, `t1`, `t2`, `t3`, `t4`, `t5`, `tableau`, `colonne_sans`, `colonne_avec` |

Points imparfaits : Le document ne conserve pas le compte des molécules d'un temps au suivant : les molécules en trop s'estompent. Les acides de Krebs sont dessinés comme une chaîne de 4 carbones (`Lexique.moleculeOrganique`). Les conclusions « sans O₂ » / « avec O₂ » s'écrivent dans le dernier tiers de `t5_sans` / `t5_avec`.

## Points imparfaits communs

- En mode large, la hauteur du cadre reste 420 : les pages s'élargissent (écran de l'ordinateur plus long, clichés plus
  larges, objets espacés) mais les objets grossissent peu.
- Les repères listés « qui apparaissent » sont relevés page figée sur chaque moment ; quelques repères n'existent que
  pendant leur étape (les noms des molécules de `marquage.html`, par exemple) et ne sont plus là ensuite.
- CO₂ en violet et éthanol en bleu clair sur les courbes et dans les textes d'`exao-levures.html`, `equation.html` et
  `comparer.html` : une voix qui nomme ces couleurs doit s'y tenir.

