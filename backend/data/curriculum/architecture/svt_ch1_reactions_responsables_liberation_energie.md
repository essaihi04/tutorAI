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
| | `le_p1_cellule`, `le_p2_glucose` (gardées) | Rappels de zéro (cellule, organites, glucose, énergie chimique) juste avant que l'ATP et les levures s'en servent. **Besoin noté** : le lecteur ne sait pas encore sauter un rappel quand le diagnostic est réussi ; à faire dans `frontend/src/` (fichier partagé, hors de cette session). |
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
- **Non fait, noté comme besoin** : `le_x1_restitution` et `le_x2_qui_respire` n'ont pas d'animation (tableau à lire).
  Une petite scène où le tableau des deux sportifs naît de l'effort (consommation d'O₂, acide lactique qui monte) et où
  chaque consigne (comparer, puis conclure) vient l'une après l'autre serait la suite logique (règle 5, règle 35).

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
