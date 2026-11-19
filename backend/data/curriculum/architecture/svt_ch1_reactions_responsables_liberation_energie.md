# Architecture — SVT ch1 « Libération de l'énergie emmagasinée dans la matière organique »

Deck : `svt_ch1_reactions_responsables_liberation_energie` · notion du cadre : `perimetre.json` →
`SVT / chapitres / reactions_responsables_liberation_energie` (CDR-SVT-SP, domaine 1, 1.1) · cadre : `svt.json` LE1 à LE10.
Nouvelle version : `backend/data/courses/en_attente/svt_ch1_reactions_responsables_liberation_energie.json`
(le cours en ligne n'est pas touché). Pistes à mettre en voix : `svt_ch1_reactions_responsables_liberation_energie_voix.json`.
Skill suivie : `.agents/skills/logique-de-cours/SKILL.md` (18 novembre 2026).

## Sources

- **Les profs (vidéos)** : les 10 vidéos de l'exploration (`exploration/reactions_responsables_liberation_energie.json`,
  `comparaison.convergences`) : Faress, Mousstaid, Driss DOTCOM, Lamsaf, Dr Ikram, Mouhib… Ordre commun (9 profs sur 10) :
  glucose et ATP → mise en évidence respiration / fermentation → glycolyse → mitochondrie → acétyl-CoA, Krebs → chaîne
  respiratoire et phosphorylation oxydative → fermentations → bilans et rendement.
- **Les cours écrits marocains** (lus avec l'utilisateur pour ce plan) : Moutamadris, unité 1, parties 1 et 2 ; Dyrassa.
  Les trois placent la comparaison des deux levures (mitochondries développées avec O₂, rares sans O₂) dans leur
  partie I, avec la mise en évidence de la respiration et de la fermentation, et définissent les deux voies juste après.
- **Le cadre** : `svt.json` (LE1 ATP … LE10 schéma de synthèse), `perimetre.json` (notions et termes hors programme :
  complexes I-IV nommés, ubiquinone… ne sont jamais enseignés ; CI…CV seulement « lus » sur un document, `le_c8_national`).
- **Le national** (20 sujets, `exploration.cas_types`) : hypothèse à vérifier 8/20, voie dominante 7/20, mitochondries
  isolées 5/20, inhibiteur (cyanure, CO, canal de l'ATP synthase) 3/20, restitution chaque année, légender 2017 N,
  calculs 2019 R et 2022. Près de 75 % des points sont du raisonnement sur documents.
- **Les difficultés** (`notions_complexes`, `commentaires_eleves`) : oxydation / réduction et le taxi NAD+ ; « où se
  passe quoi » ; le sens des protons ; « pourquoi 38 et pas 36 » ; la rédaction en flèches.

## La logique avant → après, en une phrase

Avant : on affirmait d'abord (la carte des lieux en séance 2, la glycolyse « dans le hyaloplasme » avant les preuves,
l'ATP rechargé « par la respiration ou la fermentation » avant les expériences), puis on montrait les expériences de
localisation après la glycolyse et la mitochondrie ; la chaîne était légendée « comme au national » avant les preuves
(vésicules) ; deux synthèses finales se répétaient. Après : **le problème, puis les preuves, puis le mécanisme, puis la
synthèse** — chaque lieu est déduit par l'élève d'une expérience avant d'être nommé, chaque preuve précède le schéma
qu'elle fonde, une seule synthèse ferme le chapitre.

## Les séances (40 à 50 min, trois blocs, une compétence principale par bloc)

### Séance 1 — Le problème et les deux voies (C1, C2)

| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| s1_b1 « De l'énergie, tout le temps : d'où vient-elle ? » | `le_o1_trois_vivants` (gardée) | Le problème d'abord (tous les profs ouvrent sur le besoin d'énergie). |
| | `le_o2_acquis` (déplacée, gardée) | Le diagnostic « d'où vient la matière organique ? » passe AVANT les rappels : il dit ce que l'élève sait déjà (photosynthèse, amidon) ; les rappels qui suivent ne servent qu'à celui qui a oublié (règle 6). |
| | `le_p1_cellule`, `le_p2_glucose` (gardées) | Rappels de zéro (cellule, organites, glucose, énergie chimique) juste avant que l'ATP et les levures s'en servent. **Fait le 18 novembre 2026** (format `concentration.rappel`) : `le_o2_acquis` porte le diagnostic (vrai/faux en trois affirmations : photosynthèse, cellule et noyau, énergie du glucose) ; `le_p1_cellule` et `le_p2_glucose` sont sautés quand les trois sont justes du premier coup (le cahier du bloc vient quand même). Voix à faire : énoncés et réactions du diagnostic. |
| s1_b2 « L'ATP, puis les levures avec et sans dioxygène » | `le_a1_monnaie` (**fusion** de `le_a1_monnaie` + `le_a2_recharge`, réécrite) | **Une seule diapo de rappel** : la monnaie (le glucose est un gros billet), l'hydrolyse ATP + H₂O → ADP + Pi + énergie, la carte de recharge ADP + Pi + énergie → ATP, le cycle. Sortent : la structure (adénine, ribose), l'ATPase et les 30,5 kJ : ils ne servent qu'au rendement (`le_r2_rendement` les donne) et au chapitre du muscle (SVT ch2, qui les traite déjà). On n'affirme plus « respiration ou fermentation » : l'énergie vient « de la dégradation de la matière organique, comme le glucose » ; la diapo finit sur la question du chapitre, à laquelle les expériences vont répondre (règle 4). La simulation `atp.html` reçoit `?rappel` (ni adénosine nommée, ni 30,5 kJ, « dégradation du glucose » au lieu de « respiration ou fermentation ») ; sans ce paramètre, le cours en ligne la voit comme avant. |
| | `le_e1_mesurer`, `le_e2_decrire`, `le_e3_sans_o2` (gardées) | L'expérience ExAO avec puis sans dioxygène. **La méthode décrire → déduire commence ici, dès la première courbe** (`le_e2_decrire` : « je dis ce que je vois avec les valeurs, puis j'écris donc »), et non au bloc des cas du bac ; `le_e3_sans_o2` garde sa question d'observation (l'élève voit seul la courbe d'éthanol). |
| s1_b3 « Deux voies : respiration et fermentation » | `le_e3b_masse_levures` (gardée) | Deuxième preuve, sans ExAO : la masse de levures (2,3 fois plus avec O₂) dit que la respiration libère plus d'énergie. |
| | `le_m1_deux_levures` (**déplacée** de la partie mitochondrie) | Les trois cours écrits la placent dans leur partie I : c'est une preuve de plus que les deux voies existent (mitochondries développées avec O₂, rares sans O₂), et elle prépare « la respiration est liée à la mitochondrie » sans encore dire où se passe chaque étape. Texte inchangé (sa voix reste). |
| | `le_e5_definitions` (**nouvelle**) | Les définitions viennent quand les trois preuves sont là (ExAO, masse, levures au microscope), pas avant (règle 4) : respiration = dégradation complète, avec O₂, CO₂ + H₂O, beaucoup d'énergie ; fermentation = dégradation incomplète, sans O₂, résidu organique (l'éthanol), peu d'énergie. Deux façons de le dire (règle 6) : « des déchets minéraux » / « l'éthanol brûle encore, il garde de l'énergie ». Question : pourquoi « incomplète » ? Le lieu (hyaloplasme, mitochondrie) n'y est PAS : il sera déduit en séance 2. |
| | `le_e4_carte` (gardée de place, une phrase ajoutée) | La carte du chapitre ferme la séance 1 : l'élève sait maintenant qu'il y a deux voies ; la carte annonce le chemin. Phrase ajoutée : « ces lieux ne sont pour l'instant qu'un plan ; à la séance suivante, on les vérifie par les expériences » (sinon elle affirmerait les lieux avant leur preuve). |

### Séance 2 — Où se passe chaque étape ? puis la glycolyse (C4 puis C3)

| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| s2_b1 « Où le glucose est-il dégradé ? » | `le_m3a_glucose_marque` (réécrite : la fin) | Les expériences de localisation passent AVANT la glycolyse, pour que l'élève **déduise lui-même** le lieu (règles 3 et 4). Le tuteur lit le tableau T0 → T4 sans conclure, puis pose la question « où le glucose devient-il acide pyruvique ? » ; la réponse vient de l'élève, la réaction la confirme. « Matrice » disparaît (pas encore enseignée : séance 3) ; les « composés du cycle de Krebs » sont nommés comme le document du bac les nomme, « on les verra plus loin ». |
| | `le_m3_isolees` (gardée) | Deuxième preuve : des mitochondries seules n'utilisent pas le glucose, mais l'acide pyruvique (mitochondries isolées : 5 sujets sur 20). |
| | `le_m4_o2_atp` (gardée) | Dioxygène consommé et ATP produit ensemble : la respiration fait l'ATP dans la mitochondrie ; c'est le document de la « chaîne en panne » qu'on retrouvera en séance 5. |
| s2_b2 « Les transporteurs d'hydrogène » | `le_t1_deux_h`, `le_t2_reduit` (gardées) | Le taxi juste avant la glycolyse, qui en a besoin (prérequis juste avant son usage). |
| s2_b3 « La glycolyse : lieu et bilan » | `le_g1_ou` (réécrite) | Elle n'affirme plus le lieu comme une découverte : elle **rappelle ce que les expériences ont montré** (glucose ¹⁴C devenu acide pyruvique dans le hyaloplasme ; les mitochondries seules n'utilisent pas le glucose), puis montre le glucose dans le hyaloplasme. |
| | `le_g2_six_carbones`, `le_g3_bilan` (gardées) | Le mécanisme et le bilan après le lieu. |

### Séance 3 — La mitochondrie et la matrice (C4, C5)

| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| s3_b1 « La mitochondrie : structure et composition » | `le_m2_legender`, `le_m2b_construire`, `le_m2c_composition` (gardées) | L'ultrastructure à légender puis la composition, juste avant la matrice et la membrane interne qui s'en servent (8 profs : un petit dessin de mitochondrie avant le zoom). |
| s3_b2 « Dans la matrice : acétyl-CoA et cycle de Krebs » | `le_k1_pyruvate`, `le_k2_acetyl`, `le_k3_roue` (gardées) | Ordre commun des profs. |
| s3_b3 « Un tour, cinq sorties, fois deux » | `le_k4_sorties`, `le_k5_fois_deux` (gardées) | Le compte d'un tour, puis × 2 : le piège n° 1 des bilans, à part dans son bloc. |

### Séance 4 — La membrane interne (C6)

| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| s4_b1 « Le dioxygène injecté, le taxi décharge » | `le_c1_pulse`, `le_c2_membrane`, `le_c3_decharge` (gardées) | L'expérience (injection de dioxygène, décrite seulement) avant le mécanisme qui l'explique. |
| s4_b2 « Le relais, le dioxygène, les protons, la sphère » | `le_c4_relais`, `le_c5_o2`, `le_c6_protons`, `le_c7_sphere` (gardées) | Relais des électrons → dioxygène accepteur final → protons pompés (le pic de l'expérience s'explique) → sphère pédonculée (la descente s'explique). |
| s4_b3 « Les preuves, puis le schéma du national » | `le_c10_vesicules`, `le_c10b_vesicules_cas` (déplacées avant le poison et le schéma) | **Preuve par les vésicules** : la synthèse d'ATP demande les sphères ET le gradient. Elle passe avant le poison (dont la question s'appuie sur elle) et avant le schéma du national. |
| | `le_c9_poison` (réécrite) | **Déroulé maillon par maillon** : le cyanure bloque T4, les électrons s'arrêtent ; *question d'observation* : « et le dioxygène, que devient-il ? » (l'élève le voit seul, la voix s'arrête) ; puis chaque maillon a son moment au tableau : plus de pompage → plus de gradient → plus d'ATP (`chaine.html?maillons` écrit la chaîne causale une flèche à la fois ; sans ce paramètre, le cours en ligne la voit d'un coup comme avant). La question de fin porte sur le dernier maillon (« la synthèse d'ATP… ») et rappelle les vésicules. La phrase « dans l'expérience des mitochondries, après le cyanure… » renvoyait à une expérience non encore vue : elle devient « à l'examen, si on ajoute du cyanure… » (préparation de `le_x3_chaine_en_panne`). |
| | `le_c8_national`, `le_c8b_construire` (déplacées à la fin, gardées) | **Le schéma du national à légender en synthèse**, quand tout le mécanisme et ses preuves sont acquis (légender : 1,5 point, 2017 N). Textes inchangés (« le même schéma » reste vrai : c'est le schéma de la chaîne du tableau). |

### Séance 5 — Fermentations, bilans, cas du bac, synthèse (C7, C8, C9, C10)

| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| s5_b1 « Les fermentations » | `le_f1_lactique`, `le_f2_alcoolique` (gardées) | « Et sans dioxygène ? » a été posé dès la séance 1 (ExAO, éthanol) : ici on en donne le mécanisme, avec le taxi qu'il faut rendre. |
| s5_b2 « Bilans et rendements » | `le_r1_compteur`, `le_r2_rendement`, `le_r3_comparer` (gardées) | 38 ATP, 40 % / 2 %, le tableau : après les deux voies complètes (calculs : 2019 R, 2022 R/N). Les 30,5 kJ de l'ATP arrivent ici, où ils servent. |
| s5_b3 « Cas du bac et schéma de synthèse » | `le_x1_restitution`, `le_x2_qui_respire`, `le_x3_chaine_en_panne` (gardées) | Restitution, voie dominante (7/20), hypothèse à vérifier (8/20) : la méthode décrire → déduire → expliquer → vérifier, déjà pratiquée depuis la séance 1, appliquée au document entier. |
| | `le_x4_synthese` (**fusion** de `le_x4_synthese` + `le_b2_carte`, réécrite) | **Une seule synthèse** : la carte de la séance 1 complétée (trajet du glucose, lieux, produits, 38 / 2 ATP) avec, au centre, la phrase de la carte conceptuelle : « la cellule dégrade le glucose et met une partie de son énergie dans l'ATP ». La carte conceptuelle `carte.html` faisait doublon avec le schéma et avec la fiche : `le_b2_carte` sort. |
| | `le_b1_bilan` (gardée) | La fiche bloc par bloc puis la page de l'élève (ce qu'il lui reste à revoir) : la dernière diapositive. |

## Les parties (activités)

Ouverture · I. L'ATP (rappel) · II. Respiration et fermentation : les mettre en évidence · III. Où se passe chaque
étape ? · IV. Les transporteurs d'hydrogène et la glycolyse · V. La mitochondrie : structure et composition ·
VI. Les oxydations dans la matrice · VII. La chaîne respiratoire et la phosphorylation oxydative · VIII. Les
fermentations · IX. Bilans et rendements · X. Cas types du bac et schéma de synthèse · XI. Bilan du chapitre.
Chaque partie relève de la notion `reactions_responsables_liberation_energie` de `perimetre.json` (aucune partie hors
cadre, aucune « pour les devoirs »).

## Animations et exercices animés

- `atp.html?rappel` : la recharge montre « dégradation du glucose » ; adénosine et 30,5 kJ non écrits.
- `chaine.html?poison=cyanure&maillons` : moments `o2_non`, `pas_pompage`, `pas_gradient`, `pas_d_atp`, chaque flèche
  de la chaîne causale écrite à son moment.
- `exao.html?vue=levures&depart=anaerobie` pour `le_e5_definitions` (les deux phases, l'éthanol, aérobie / anaérobie).
- Questions d'observation : 2 dans le cours (`le_e3_sans_o2`, `le_c9_poison`), le maximum de la règle 30.
- ~~Non fait~~ → fait en 2ᵉ passe (voir la section « 2ᵉ passe » en fin de fichier) : `le_x1_restitution` et
  `le_x2_qui_respire` sont joués pas à pas sur `national.html`.

## Ce qui change, ce qui reste

- **Déplacées, texte et voix gardés** : `le_o2_acquis`, `le_m1_deux_levures`, `le_m3a…` (ordre), `le_m3_isolees`,
  `le_m4_o2_atp`, `le_c10_vesicules`, `le_c10b_vesicules_cas`, `le_c8_national`, `le_c8b_construire`.
- **Réécrites** : `le_a1_monnaie` (fusion ATP), `le_e4_carte` (une phrase), `le_m3a_glucose_marque` (conclusion →
  question), `le_g1_ou` (rappel des preuves), `le_c9_poison` (maillons, observation, question), `le_x4_synthese` (fusion).
- **Nouvelle** : `le_e5_definitions`. **Retirées** : `le_a2_recharge` (fondue dans `le_a1_monnaie`), `le_b2_carte`
  (fondue dans `le_x4_synthese`).
- **Gardé tel quel, avec sa raison** : le taxi et la carte de recharge comme fils rouges (plan de l'exploration) ;
  la mitochondrie légendée avant la matrice (ordre des profs) ; les fermentations après la respiration (9 profs : le
  taxi à rendre ne se comprend qu'après la chaîne).
- Séances et blocs renumérotés (`le_s1_b1` … `le_s5_b3`) ; compétences recoupées sur le nouvel ordre.

## Voix à faire (VPS, voix Bodi)

37 pistes, listées dans `svt_ch1_reactions_responsables_liberation_energie_voix.json` : 7 diapositives (`le_a1_monnaie`,
`le_e4_carte`, `le_e5_definitions`, `le_m3a_glucose_marque`, `le_g1_ou`, `le_c9_poison`, `le_x4_synthese`), 20 réactions,
3 énoncés de questions, 7 pistes de la question d'observation de `le_c9_poison`. L'énoncé de la question de
`le_a1_monnaie` garde sa voix (même texte que l'ancienne `le_a2_recharge`). `verifier_mots.py` : plus aucun mot darija
rare ; restent des mots à écouter (champ `a_ecouter`) : *photosynthèse*, *vésicules* (termes du programme et du bac),
*poison*, *balise*, *marqué*, *carrefour* (déjà dits par les anciennes voix de ces diapositives).

Contrôle voix ↔ simulation (`backend/scripts/verifier_pointage_simulations.py` sur la version en attente) : aucun écart
nouveau ; les « gestes trop serrés » des diapositives réécrites viennent de l'absence de voix (durée inconnue) et
disparaîtront avec elle ; les deux écarts restants (`le_k3_roue`, `le_f2_alcoolique`) existent déjà dans le cours en ligne.

## Relecture contre les règles 1 à 9

1. Raison écrite : chaque ligne ci-dessus. 2. Mots : `verifier_mots.py` passé sur toutes les pistes réécrites (voir le
rapport de session). 3. Ne pas tout donner : lieu de la glycolyse et effet du cyanure trouvés par l'élève ; bilan des
expériences après la dernière. 4. Expérience avant mécanisme : définitions après les preuves, localisation avant la
glycolyse, vésicules avant le schéma du national. 5. Exercices pas à pas : poison en maillons ; x1/x2 à animer (besoin
noté). 6. Départ de zéro : rappels cellule et glucose, taxi avant la glycolyse. 7. Une idée par diapositive : l'ATP
réduite à son rôle. 8. Rien hors cadre : CI…CV seulement lus sur un document. 9. Écran : formules en notation à
l'écran, mots dans la voix ; les simulations modifiées gardent leurs tailles (≥ 15 px pour les ajouts).

## 2ᵉ passe (18 novembre 2026) : chaque cas type du national joué pas à pas

Demande : « simple, animé, expliqué ; ne pas tout donner au départ ; laisser à l'élève le temps de trouver seul ; une
raison derrière chaque choix ». Script reproductible : `python3 scripts/logique/deuxieme_passe_svt_ch1.py` (relit la
version en attente, idempotent, contrôle chaque `mot`), puis `python3 -X utf8 scripts/logique/lister_voix.py <deck>`.

### Le schéma d'un exercice joué (le même pour les trois)

Une diapositive = **une consigne** du sujet. La voix fait apparaître le document par l'animation (les valeurs naissent
de ce qu'on voit, puis le tableau : règle 35), pose la consigne et se tait ; la question (QCM) vient après la voix, avec
une réaction préparée pour chaque option (juste / indice / réponse) ; la **correction écrite comme le barème** la lit
(`question.demonstration.lignes`) n'apparaît qu'après la réponse. La diapositive suivante **rejoue la correction au
tableau** (la simulation l'écrit à son moment) avant la consigne suivante. Dans la simulation, tout ce qui appartient à
la correction reste caché tant que l'élève n'a pas répondu (`?cacher=<moment>` dans `national.html`,
`?conclusions=false` dans `exao.html`). Raison : règles 3, 5 et 33 (le résultat après la réponse de l'élève) et la
méthode du barème (décrire → déduire → expliquer / vérifier).

### Ce qui a été ajouté, par cas type

| Cas type (exploration) | Diapositives | Ce qui est joué, et pourquoi |
|---|---|---|
| `definition`, `sens_protons`, `qcm_vrai_faux` (restitution, chaque année) | `le_x1_restitution` (réécrite), `le_x1b_protons`, `le_x1c_qcm` (nouvelles) | **2024 R** « définir la fermentation lactique » : trois cadres vides (nature, lieu et conditions, produits), l'élève choisit la définition à 0,5 pt ; puis les cadres se remplissent (correction) et la membrane interne est refaite de mémoire (peinte) pour le **sens des H⁺** ; puis les flèches (correction) et le **QCM 2022 N** (1, b) : la méthode « chercher le mot faux » est montrée sur a (rayée : le sens), l'élève tranche b, c, d ; la démonstration raye c et d (« externe ») et écrit « (1, b) ». Avant : une diapositive de texte qui disait la méthode sans la faire. |
| `voie_dominante` (7 sujets sur 20) | `le_x2_qui_respire` (réécrite), `le_x2b_fatigue` (nouvelle) | **2016 N, documents 1 et 2** (valeurs du sujet ; avant : des valeurs inventées, 3,5 / 2,0 L/min) : deux muscles peints font le même effort, les jauges d'O₂ (5,5 / 2,5 L/min) et d'acide lactique (6 / 12 mmol/L) montent, la coupe des fibres montre les mitochondries (11 % / 5 %, enzymes importante / faible), puis le tableau. Consigne 1 : comparer (la comparaison du barème, critère par critère avec les valeurs). Consigne 2 (diapositive suivante, après la comparaison écrite au tableau) : expliquer la fatigabilité (fermentation lactique → 2 ATP → fatigue). |
| `mitochondries_isolees` (5/20), `hypothese` (8/20), `inhibiteur` | `le_x3_chaine_en_panne` (réécrite), `le_x3b_deduire`, `le_x3c_hypothese` (nouvelles) | Avant, une seule diapositive DISAIT la description, la déduction, l'hypothèse et sa vérification d'un coup, sans question. Maintenant trois consignes : **décrire** (la courbe se trace ajout par ajout, sans note écrite ; QCM « après ADP + Pi ») → **déduire** (pyruvate, pas glucose ; O₂ couplé à l'ATP) → **hypothèse au conditionnel** puis vérification en flèches (démonstration). `exao.html` reçoit `?conclusions=false` : les notes sous le graphique, l'hypothèse écrite, la bulle d'arrêt (« [O₂] reste à 40 % ») et le message de fin se taisent ; sans ce paramètre, le cours en ligne voit la page comme avant. |
| `levures` (2019 R) | `le_e3b_masse_levures` (texte et voix gardés) | Le tableau naît de l'animation : deux béchers peints (culture aérée / fermée), les levures se multiplient, les compteurs (glucose consommé, levures formées) montent, l'éthanol s'écrit ; puis le tableau et le rapport par gramme de glucose en vraies fractions (≈ 2,3 fois plus avec O₂). Seul le `pointage` change (les mots déjà dits) : la voix reste. |
| (localisation, document du bac) | `le_m3a_glucose_marque` (deux phrases retouchées, déjà sans voix) | Le tableau T0 → T4 devient une cellule peinte où les molécules radioactives (billes) passent du milieu au hyaloplasme puis à la mitochondrie ; les « + » s'écrivent à droite à chaque temps, puis le tableau. Aucune conclusion écrite : l'élève déduit le lieu de la glycolyse (question gardée). |
| `pulse_o2` | `le_c1_pulse` (inchangée) | Déjà joué : la courbe se trace, la description seulement ; l'explication vient à `le_c6_protons` (règle 4). |
| `legender` | `le_c8_national`, `le_c8b_construire` (inchangées) | Déjà joué (schéma à légender du national). |
| `calcul`, `tableau_comparatif` | `le_r1_compteur`, `le_r2_rendement`, `le_r3_comparer` (inchangées) | Déjà joués (compteur d'ATP, rendement calculé au tableau, comparaison animée). |
| `equation` (2017 N, 2020 R, 2021 N, 2022 N) | `le_x1d_reactions`, `le_x1e_reactions_c`, `le_x1f_reactions_krebs` (nouvelles, ajoutées après la 2ᵉ passe) ; `le_g3_bilan`, `le_k5_fois_deux`, `le_f1_lactique`, `le_f2_alcoolique` (inchangées) | **2020 R, restitution III** « reliez chaque phénomène à la réaction bilan qui lui convient » (1 pt, cinq réactions pour quatre phénomènes : d est l'intrus). Vue `national.html?vue=reactions` : les phénomènes puis les réactions s'écrivent ; une réaction à la fois, ce qu'elle donne est **souligné** (où regarder), puis le lien est tracé. Trois consignes : (1) le tuteur montre la méthode sur a (éthanol + CO₂ → (4 ; a)), l'élève fait b ; (2) l'élève fait c (d'où elle part, ce qu'elle donne) ; (3) l'élève départage d et e (cycle de Krebs). Le nom du produit et le lien restent cachés (`?cacher=`) jusqu'à la réponse ; `concentration.apres_reponse` (format du lecteur, commit b4a6a36c) les joue au tableau juste après la réponse (`set_parameters {conclusions: true}` puis `play_until`), puis la démonstration au barème ; la diapositive suivante part de là (`?depart=`). Avant : les équations étaient seulement écrites au tableau dans le cours, jamais reliées comme le demande le sujet. Bloc à part `le_s6_b1b` (cahier : le produit qui signe chaque voie ; « retrouver » ; exercice jumeau). |

Simulation nouvelle : `reactions_responsables_liberation_energie-tableau/national.html` (vues `sportifs`,
`restitution`, `levures`, `marquage`, puis `reactions`), sur le kit du dossier (`commun.js`, `peinture.js`) : moments nommés,
`ce_qui_se_voit`, repères, `?depart=`, `?cacher=` et `set_parameters {conclusions}`. Contrôlée dans Chromium à
1280 × 640, 1024 × 560 et 724 × 350 (aucune erreur, chaque moment atteint par `play_until`, rien de coupé).

### Séances

Les cas du bac deviennent une **séance 6** (« Les cas du national joués pas à pas, puis la synthèse »), quatre blocs :
restitution (`le_x1…`), voie dominante (`le_x2…`), document des mitochondries (`le_x3…`), schéma de synthèse
(`le_x4_synthese`, `le_b1_bilan`). Raison : huit diapositives à question ne tiennent pas dans un bloc de la séance 5
(règle 7, 40 à 50 min) ; un exercice du national a plusieurs consignes, donc plusieurs « À toi » dans son bloc (c'est
voulu : une consigne, une réponse, une correction). La séance 5 garde fermentations, bilans et rendements. Chaque
nouveau bloc a son cahier, son « retrouver » et un exercice jumeau (vrai/faux 2023 R ; fibres B ; canal des sphères
bouché, 2023 N) ; l'ancien exercice de bloc qui reprenait `le_x2_qui_respire/e0` (supprimé) est remplacé.
Durée estimée : 275 min, puis 285 min avec le bloc `le_s6_b1b` (appariement 2020 R, trois diapositives, inséré après
`le_s6_b1` : un bloc de restitution à six diapositives dépasserait la limite de quatre éléments nouveaux).

### Mots

Les nouveaux textes passent par la règle de `verifier_mots.py` (via `lister_voix.py`, qui lit la version en attente ;
`verifier_mots.py` lit le cours en ligne). Remplacés : critère → واحد بواحد ; barème → la correction ديال الامتحان ;
la note → النقطة ; restitution → أسئلة الدرس ; fatigabilité (consigne lue) → la fatigue كتجي بالزربة ; كتعيا, متعود,
نشطبو, مشطبة, كيسد, كيوقفو, كتربط, كتجاوب, كتستعملش, كنقيسو, كنوصفو, كيضويو, balise, كنتبعوه… par des mots courants
vérifiés (نحيدوها, سد, ما بقاش كيدوزو, كتعطي السبب, نقيسو, نوصفو, العلامة, نتبعو…). **Restent, à écouter** : *bloquerait*
(la phrase d'hypothèse à écrire), *conditionnel* (méthode du bac), *quatre-vingt-seize* (valeur du document), *marqué*
(glucose marqué) — et ceux de la 1ʳᵉ passe. Appariement 2020 R : *relier* → نربطو, كثر من اللازم → زايدة, نقراوش →
ما غاديش نقراو, كتعطيش / كتعطيهم → ما فيهاش / فيها, كيتقطع → كيولي ; les formules ne sont pas lues (« CH trois CHOH
COOH » → « l'acide lactique ») ; les lettres des réactions dites en majuscules (A, B…), comme `le_x1c_qcm` ; plus aucun
mot rare dans ces pistes (*photosynthèse*, *poison*, *vésicules*, *carrefour*).

### Voix

`svt_ch1_reactions_responsables_liberation_energie_voix.json` : 101 pistes (15 diapositives, 60 réactions, 8
démonstrations, 11 énoncés, 7 pistes d'observation) à la fin de la 2ᵉ passe ; **134** après l'appariement 2020 R
(+ 24 : 3 diapositives, 15 réactions, 3 démonstrations, 3 énoncés ; + 9 réactions de `le_o2_acquis`, ajoutées entre-temps
par le commit 5bc776f0, sans voix). Nouvelles de cette passe : 8 diapositives d'exercice et leurs
réactions, énoncés et démonstrations ; `le_m3a_glucose_marque` retouchée. `le_e3b_masse_levures` garde sa voix.

### Contrôles

`verifier_pointage_simulations.py --ecarts` : aucune ligne « introuvable » (en attente et en ligne) ; les seuls écarts
nouveaux sont des « gestes trop serrés » sur les diapositives sans voix (durée inconnue, ils disparaîtront avec elle).
`verifier_mots_pointes.py` : 0 mot introuvable. `verifier_formules.py` : rien pour le dossier.

### Ce qui reste, et pourquoi

- Les voix (VPS, voix Bodi) : quota Kaggle épuisé dans cette session.
- `le_e3b_masse_levures` dit encore « شوف le tableau » au moment où la scène montre les deux béchers (le tableau vient
  ensuite) : la voix enregistrée est gardée ; à corriger quand la diapositive sera de nouveau mise en voix.
- Le lecteur ne savait pas enchaîner une correction « au tableau » sur la même diapositive que la question : la
  correction animée est donc au début de la diapositive suivante. Le lecteur a depuis reçu `concentration.apres_reponse`
  (commit b4a6a36c) ; seules les trois diapositives de l'appariement 2020 R l'utilisent. Les huit autres exercices
  joués pourraient y passer (leur correction se jouerait sur la même diapositive).


Appariement 2020 R : `python3 scripts/logique/svt_ch1_appariement.py` (idempotent ; à relancer après `deuxieme_passe_svt_ch1.py`), puis `python3 -X utf8 scripts/logique/lister_voix.py svt_ch1_reactions_responsables_liberation_energie`.

## 3ᵉ passe (19 novembre 2026) : démonstration sur le document, compter en allumant

- **Allumer** (`simulations-au-tableau` règles 16-17, `professeur` 44-45) : `commun.js` reçoit `SVTTableau.Allumage` (commandes
  `allume {cible}` / `eteins`, lueur jaune qui reste, la dernière plus vive, numéro courant des comptes ; `reset` éteint).
  Pages qui l'exécutent elles-mêmes : `national.html`, `exao.html`, `compteur.html`, `glycolyse.html`, `krebs.html`.
- **`allume` sur les lignes de démonstration** : `le_x1_restitution` (cadres nature / lieu / produits), `le_x1b_protons`
  (flèches chaîne, sphère), `le_x1c_qcm` (propositions a, c, d rayées, b), `le_x1d/e/f` (ce que donne la réaction, le
  phénomène, le lien), `le_x2_qui_respire` et `le_x2b_fatigue` (lignes du tableau 2016 N), `le_x3*` (bandes des périodes entre
  deux ajouts, nouveaux repères `periode_glucose|pyruvate|adp|cyanure` d'`exao.html`), `le_g3_bilan` (les taxis, la réaction).
  Textes dits inchangés.
- **Compter en allumant** : `le_r1_compteur` (les 4 ATP directs, les 10 NADH,H⁺, les 2 FADH₂ comptés un à un ; chaque total
  s'écrit dans la ligne « total » à la fin de son compte ; pointages `compte_atp`, `compte_nadh`, `compte_fadh` au rythme de
  « نجمعو… ») ; `le_g2_six_carbones` (les 6 carbones du glucose, `compte_carbones`, avant la coupure) ; `le_k4_sorties` (les
  5 sorties d'un tour numérotées à leur cran, « un tour : 5 sorties » écrit une fois). Les moments qui suivaient un compte
  sont décalés dans la page (mêmes noms).
- **L'énoncé du national d'abord** : en attente du gabarit commun `shared/examen/feuille.html` (feuille d'examen refaite en
  code) ; la préparation (sujets, questions, points, figures à redessiner) est dans `docs/audit-national/svt.md`, section ch1.
