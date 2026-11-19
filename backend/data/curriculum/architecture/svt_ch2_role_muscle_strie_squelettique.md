# Architecture — SVT ch2 « Rôle du muscle strié squelettique dans la conversion de l'énergie »

Skill `logique-de-cours`, 18 novembre 2026. Cours en ligne : `backend/data/courses/svt_ch2_role_muscle_strie_squelettique.json`
(non modifié). Nouvelle version : `backend/data/courses/en_attente/svt_ch2_role_muscle_strie_squelettique.json`
(construite à partir du cours en ligne, aucune copie en attente plus récente n'existait). Pistes à mettre en voix :
`svt_ch2_role_muscle_strie_squelettique_voix.json` (72 pistes après la 2ᵉ passe, § 8).

## 1. Sources consultées

- **Les profs (vidéos)** : exploration `backend/data/curriculum/exploration/role_muscle_strie_squelettique.json`
  (10 professeurs, `comparaison.convergences`, `variantes_admises`, `meilleures_explications`).
- **Les cours écrits en ligne** (plans relevés avec PyMuPDF) :
  - AlloSchool, Mr Bahsina, séances 6 et 7 : I-III manifestations mécaniques, puis IV structure, V régénération de l'ATP,
    VI mécanisme (la régénération avant le mécanisme).
  - Dyrassa, « Activités chapitre 2 » (fiche d'activités de classe) : myogrammes → seuil et recrutement → chaleur →
    structure, myofilaments → conditions nécessaires à la contraction (fibre glycérinée) → importance de l'ATP →
    légender le sarcomère → **ATP et glycogène avant et après la contraction** → importance du calcium → étapes →
    voies de régénération (phosphocréatine, etc.) → voie et type d'effort.
  - Dyrassa, cours du Pr Taha : I étude expérimentale (myogrammes), II phénomènes thermiques et énergétiques, III structure
    et ultrastructure, IV mécanisme (glissement puis expériences), V renouvellement de l'ATP.
  - Moutamadris (cours SP international) : PDF bloqué par Cloudflare depuis le conteneur, non lu.
- **Le cadre** : cadre officiel SVT PC (`backend/cours 2bac pc/cadres de references 2BAC PC/…svt-sciences-physiques (1).json`),
  sous-domaine 1.2, connaissances dans cet ordre : myogramme ; phénomènes thermiques et chimiques ; structure et
  ultrastructure ; structure moléculaire des myofilaments ; **origine de l'énergie nécessaire à la contraction** ;
  mécanisme de la contraction ; voies métaboliques de régénération de l'ATP ; 1.3 schéma de synthèse.
  `backend/data/curriculum/svt.json` (chapitre « 1.2 et 1.3 »), capacités MSS1-MSS13 de l'exploration.
- **Le national** (`cas_types` de l'exploration, sujets de `backend/data/exams/svt`) : le cas le plus fréquent est
  « entraînement, maladie, fibres I/II et voie dominante » (2016 N, 2017 R, 2018 R, 2019 N, 2020 N, 2022 R, 2023 N,
  2024 R ; 5 à 7 points), puis « tableau de métabolites avant / après l'effort » (2017 R, 2020 R, 2022 R), les
  inhibiteurs (2020 R, 2021 R), l'ordre des étapes (2018 N), légender (2021 N, 2023 R). Valeurs reprises des figures :
  2017 R documents 1 et 2, 2020 N document 2 (BPCO).

## 2. La logique avant (cours en ligne, 60 diapositives, 5 séances)

Ouverture (effort ; **rappel de l'ATP qui enseignait l'hydrolyse** et affirmait « l'ATP donne directement l'énergie »)
→ I secousse → II intensité → III fusions, tétanos, fatigue → IV chaleur, sang, **dosage ATP / phosphocréatine**
(« le muscle a consommé de l'ATP ») → V structure (u7 : « la tête de myosine est une ATPase ») → VI glissement →
VII Ca²⁺ et ATP (fibre glycérinée, myofibrille, puis le cycle ; c4 : « la myosine seule hydrolyse peu, fixée à l'actine
beaucoup ») → VIII régénération → IX rédiger (x1-x3 en texte) → X bilan.

Défauts relevés (règles de la skill) :
1. **L'ATP affirmé avant d'être prouvé** (règle 4) : à l'ouverture, « l'ATP donne directement l'énergie » et l'hydrolyse
   sont posés comme un acquis du chapitre 1 ; or l'hydrolyse et les voies de régénération sont au programme de ce
   chapitre (le ch1 n'en garde qu'un rappel), et le cadre place « l'origine de l'énergie » juste avant le mécanisme.
2. **Le dosage ATP / phosphocréatine en séance 2** dit « le muscle a consommé de l'ATP » trois séances avant les
   expériences qui le montrent (fibre glycérinée, salyrgan), et parle de la phosphocréatine 4 séances avant son rôle.
3. **Deux résultats sans leur expérience** : u7 (« la tête est une ATPase ») et c4 (« myosine seule : peu ; fixée à
   l'actine : beaucoup ; actine seule : rien ») affirment le résultat de l'expérience de l'activité ATPasique, jamais montrée.
4. **Règle 27** : une option de la question de u7 (« le Ca²⁺ et la troponine ») employait le Ca²⁺ une séance avant
   qu'il soit enseigné.
5. **Le national n'est pas joué** : x1-x3 sont des textes et des tableaux ; le cas le plus fréquent (fibres I/II,
   maladie) n'a aucune diapositive ; le document 2 du 2017 R (part de chaque voie) n'est pas montré.
6. Séance 4 trop lourde (4 blocs, 15 diapositives) et séance 5 qui mêle trois sujets.

## 3. La logique après (64 diapositives, 7 séances, 20 blocs)

Règle de décision : ordre commun des profs et du manuel (ce qui se voit → la structure → ce qui l'explique), qui est
aussi celui du cadre ; on s'en écarte seulement pour mettre une preuve avant son résultat. Pour la place de
l'énergie, trois sources s'accordent (cadre officiel, activités Dyrassa, Pr Taha) : l'ATP comme source d'énergie
et son hydrolyse sont enseignés **après la structure, avec les expériences qui les montrent, juste avant le
mécanisme** ; la régénération vient après le mécanisme (AlloSchool la met avant : variante écartée, car la question
« pourquoi l'ATP reste constant ? » n'a de sens qu'une fois prouvé que la contraction le consomme).

### Séance 1 — Le muscle répond : la secousse et le seuil
| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| b1 | `ms_o1_effort` (gardée) | 10/10 profs partent du lien avec le ch1 : « la cellule a fait l'ATP, le muscle l'utilise : comment ? ». Pose le problème sans l'affirmer comme résultat. |
| | `ms_s1_myographe`, `ms_s2_secousse` (Q) | Le montage avant le tracé (règle 33 : principe d'abord). Ordre de toutes les sources. |
| b2 | `ms_s3_latence` → `ms_s6_definition` (Q) | Une phase par diapositive, puis la mesure, puis la définition construite (MSS1, « définir » 5 sessions). |
| b3 | `ms_i1_seuil`, `ms_i2_recrutement`, `ms_f1_isolees` (Q) | Intensité avant fréquence (cadre MSS2, 7/10 profs). |

Changement : la diapositive `ms_o2_atp` (rappel qui enseignait l'hydrolyse) quitte l'ouverture ; le cahier du bloc 1 perd
la ligne de l'hydrolyse ; son « retrouver » devient myographe / myogramme.

### Séance 2 — La fréquence, la fatigue, la chaleur (inchangée sauf le dernier bloc)
| Bloc | Diapositives | Pourquoi |
|---|---|---|
| b1 | `ms_f2`, `ms_f3`, `ms_f4` (Q) | Deux excitations, puis une série (grille de Elboukhari, 8/10). |
| b2 | `ms_f5`, `ms_f6_nomme`, `ms_f7_fatigue` (Q) | Nommer les tracés (national 2017 N, 2018 N, 2020 R). |
| b3 | `ms_t1`, `ms_t2`, `ms_t3_sans_dioxygene` (observation), `ms_t4a_sang` (**Q nouvelle**) | Les phénomènes thermiques puis chimiques (cadre). Le dosage du muscle (ATP, PC) part en séance 5 ; le bloc garde le sang (O₂, glucose, CO₂ → respiration), qui ne suppose rien de l'ATP. La question du bloc passe sur `ms_t4a_sang` (déduire la respiration). |

### Séance 3 — Du muscle au sarcomère, et le glissement (même ordre)
`ms_u1` → `ms_u8` (deux schémas à légender, `ms_u6_legender` et `ms_u8_legender_molecules`, contrat `legende_*`
vérifié dans `sarcomere.html` et `calcium.html` via `etiquettes.js`, réactions juste / partiel / faux / aide présentes),
puis `ms_g1` → `ms_g3`. Pourquoi : 10/10 profs ; le glissement se déduit des mesures (expérience avant le mécanisme).
**Réécrite : `ms_u7_molecules`** — la phrase « la tête de myosine est une ATPase » est retirée (le résultat vient en
séance 4 avec son expérience) ; l'option « le Ca²⁺ et la troponine » devient « la troponine et la tropomyosine »
(règle 27), deux réactions réécrites.

### Séance 4 — L'origine de l'énergie, puis le calcium et la tête de myosine
| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| b1 | `ms_c1_exigences`, `ms_c1b_essais` (Q) | Le principe, puis les quatre essais un par un (règle 33) : l'ATP **et** le Ca²⁺ sont nécessaires. N'a besoin que du mot « ATP » (ch1). |
| b1b | **`ms_e1_hydrolyse` (nouvelle)** | L'hydrolyse est enseignée **au moment où elle sert** (règle 6) : juste avant l'expérience du salyrgan, qui « bloque l'hydrolyse ». Deux façons : l'animation de la molécule (`atp.html` du ch1) puis la petite monnaie. Remplace `ms_o2_atp`. |
| | `ms_c1c_myofibrille` | Salyrgan et chélateur : l'hydrolyse et le Ca²⁺ sont indispensables (MSS9). |
| | **`ms_e2_atpase` (nouvelle, Q)** | L'expérience des trois tubes (actine / myosine / actine + myosine, Pi mesuré), animée tube par tube (`atpase.html`), **avant** que `ms_c4_rotation` dise « la tête est une ATPase, activée par l'actine ». Une enzyme est redéfinie en une phrase (prérequis). |
| b2 | `ms_c2a_calcium_libere` → `ms_c4_rotation` (Q) | Le calcium : l'expérience (calcium radioactif, équorine) avant son rôle ; puis attachement, rotation (ordre du QCM national 2018 N). |

### Séance 5 — La fin du cycle, puis l'ATP se refait
| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| b0 | `ms_c5`, `ms_c6`, `ms_c7_ordre`, `ms_c8_conversion` (Q) | Détachement, relâchement, l'ordre des étapes (exercice type), la conversion (MSS12). |
| b0b | `ms_t4_consomme` (Q, **déplacée**) | Le dosage avant / après l'activité ouvre la régénération (comme la fiche Dyrassa) : maintenant que la consommation de l'ATP est prouvée, « l'ATP reste presque constant » se **déduit** : il est régénéré. La phosphocréatine qui baisse annonce la diapositive suivante. |
| | `ms_r1_reserve`, `ms_r2_phosphocreatine`, `ms_r3_deux_chaleurs` | `ms_r1` dit « tu te rappelles le tableau » : le tableau est maintenant juste avant. Le retour aux deux chaleurs (association national 2021 N). |
| b1 | `ms_r4_fermentation` (Q), `ms_r5_respiration`, `ms_r6_relais`, `ms_r6b_intensite` | Les deux autres voies, puis leur relais selon la durée et l'intensité (MSS10-11). |

### Séance 6 — Comparer les voies, lire les documents du national
| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| b1 | `ms_r7_tableau`, `ms_r8_inhibiteurs` (Q) | La comparaison écrite (« dégagez sous forme d'un tableau », 2022 R), puis une voie bloquée (2020 R, déjà animée). |
| b2 | `ms_x1_decrire_comparer`, `ms_x2_deduire_expliquer` | La méthode des verbes avant de jouer les exercices du national (15 points sur 20). |
| b3 | `ms_x3_hypothese` (Q, **animée**) | Voix gardée ; le document 1 du 2017 R naît maintenant d'une animation (`national.html?vue=nageurs` : les jauges des quatre métabolites bougent au repos, après 100 m, après 1500 m, puis deviennent le tableau du sujet ; règle 35). Unités du sujet corrigées à l'écrit (10⁻⁶ mol/g = mmol/kg). |
| | **`ms_n1_voies` (nouvelle, observation)** | Le document 2 du même sujet : la barre du 1500 m d'abord (93 % respiration), puis celle du 100 m — **le cas décisif est posé en question d'observation** (règles 30 et 33) : la voix s'arrête, l'élève dit quelle voie domine, puis la voix confirme (85 % phosphocréatine). |

### Séance 7 — Fibres de type I et II (national 2020 N), restitution et bilan
| Bloc | Diapositive | Pourquoi ici |
|---|---|---|
| b1 | **`ms_n2_fibres` (nouvelle, Q)** | Le cas le plus fréquent du national. Le document est joué pas à pas (`national.html?vue=fibres`) : les barres de la personne saine, puis de la malade, la comparaison dite comme au barème, puis le tableau des fibres une ligne à la fois ; « les fibres I/II se lisent, on ne les apprend pas » (hors cadre comme savoir). La consigne « déduire » est la question ; la démonstration écrit la réponse comme le barème. |
| | **`ms_n3_chaine` (nouvelle)** | La consigne suivante, « expliquer » : la chaîne des causes, une case par moment (`?vue=chaine`), jusqu'au mot de la question. |
| b2 | `ms_x4_restitution` (Q), `ms_b1_bilan`, `ms_b2_carte`, `ms_b3_synthese` | Restitution (partie I du sujet), puis la fiche, la carte et le schéma de synthèse (1.3). |

Une seule question « À toi » par bloc (le bloc `ms_s6_b2` n'en a pas : deux diapositives de méthode). Deux
questions d'observation dans le cours (`ms_t3_sans_dioxygene`, `ms_n1_voies`), la limite de la règle 30.

## 4. Compétences

C3 garde `ms_t4_consomme` (MSS4, dosages). C6 : `ms_o2_atp` remplacée par `ms_e1_hydrolyse`, `ms_e2_atpase` ajoutée,
libellé élargi à l'origine de l'énergie. C8 : `ms_n1_voies`, `ms_n2_fibres`, `ms_n3_chaine` ajoutées, libellé élargi
au type de fibres. Les rappels existants n'ont pas changé.

## 5. Animations nouvelles (dossier du chapitre, aucun fichier partagé modifié)

- `recit.js` : la ligne de temps pilotable (Chrono, Apparitions), copie de celle du ch1 pour les pages nouvelles.
- `atpase.html` : trois tubes peints (verre, liquide, actine, myosine, Pi qui apparaît), un tube après l'autre ;
  moments `principe`, `tube1`, `tube2`, `tube3`, `conclusion` ; `conclusions: false` cache le dernier résultat.
- `national.html` : vues `nageurs` (2017 R doc 1), `voies` (2017 R doc 2), `fibres` (2020 N doc 2), `chaine`
  (2020 N question 3) ; un moment par étape du raisonnement, un repère par objet nommé, valeurs des sujets.
- Vérifiées dans Chromium à 1280 × 640 et 1024 × 560 (aucune erreur, rien de coupé, textes ≥ 15 px).

## 6. Ce qui reste, et pourquoi

- Les 56 autres diapositives gardent id, texte et voix : seul leur ordre a changé (et le pointage de `ms_x3_hypothese`).
- `ms_f7_fatigue` explique déjà la fatigue par la fermentation lactique (notion du ch1) : gardé, la voix est faite.
- Pas de nouvelle animation pour `ms_r6b_intensite` et `ms_x1`/`ms_x2` (texte et tableau) : à faire (vue `intensite`
  et `entraine` de `national.html`, en gardant leur voix).
- Écarts du contrôle de pointage déjà présents en ligne (repères calculés de `ms_u6_legender` et `ms_r8_inhibiteurs`,
  même URL sur des diapositives qui se suivent) ; les gestes « trop serrés » des diapositives sans voix disparaîtront
  quand leur durée réelle sera connue.

## 7. Mots à écouter (termes du programme ou des sujets, rares dans le corpus de la voix)

« A T P ase » (déjà dit dans `ms_c4_rotation`), « glycolytiques », « oxydatives » (lus dans le document 2020 N),
« quatre-vingt-cinq », « quatre-vingt-treize », « protides » (déjà dit dans `ms_t4a_sang`), « tubes ».

## 8. 2ᵉ passe (18 novembre 2026) : chaque cas type du national joué pas à pas

Demande de l'utilisateur : simple, animé, expliqué ; ne pas tout donner au départ ; laisser à l'élève le temps de
trouver ; une raison derrière chaque choix. Règle appliquée (skill `logique-de-cours`, règle 5) : le document apparaît
par une animation qui produit ses valeurs, **une consigne par diapositive** (comparer → déduire → expliquer), la
réponse de l'élève (question) avant la correction, la correction écrite comme le barème la lit.

### Ce qui a été ajouté, et pourquoi

| Cas type (exploration) | Diapositives | Ce qui change, et pourquoi |
|---|---|---|
| `entrainement_maladie` (8 sujets sur 20, le plus fréquent) | `ms_x1_decrire_comparer`, `ms_x2_deduire_expliquer` (réécrites), **`ms_x2b_expliquer`**, **`ms_x2c_rediger`** (nouvelles) | x1/x2 étaient deux textes de méthode sur un tableau « reconstitué ». Ils deviennent l'exercice du **2016 N** (documents 1 et 2, valeurs du sujet : mitochondries 11 % / 5 %, O₂ 5,5 / 2,5 L/min, acide lactique 6 / 12 mmol/L) joué en quatre consignes sur `national.html?vue=entraine` : x1 lit les documents (fibres peintes et leurs mitochondries, puis les barres) et **demande** la comparaison (QCM « rédigée comme le barème ») ; x2 écrit la comparaison, puis demande la déduction (quelle voie domine) ; x2b écrit la déduction, puis demande la chaîne qui explique la fatigabilité ; x2c écrit la réponse du barème, une flèche par moment. Chaque diapositive repart du moment où la précédente s'est arrêtée (`depart=`) et cache la suite (`cacher=`) : rien de décisif au tableau avant la réponse. Les fourchettes reconstituées (« 4 à 6 / 12 à 16 ») sont remplacées par les valeurs du sujet. |
| `tableau_metabolites`, `hypothese` | `ms_x3_hypothese` (inchangée) | Déjà jouée : `?vue=nageurs` (2017 R, doc. 1) fait naître le tableau, la question vient après. |
| (même famille) | `ms_n1_voies`, `ms_n2_fibres`, `ms_n3_chaine` (inchangées) | Déjà jouées (barres, fibres I/II, chaîne), l'observation ou la question avant la conclusion. |
| Effort d'intensité croissante (MSS11, document des manuels) | `ms_r6b_intensite` (réécrite) | Avant : un tableau lu et la conclusion dite. Après : `?vue=intensite` — un muscle qui travaille plus vite, trois compteurs (intensité, O₂, acide lactique), un point par mesure, le **palier** du O₂, puis le tableau (règle 35). La voix décrit seulement ; la déduction est la **question**, puis la démonstration l'écrit comme le barème ; la conclusion de la simulation reste cachée (`cacher=conclusion`). |
| `tableau_comparatif` des voies (2022 R) | `ms_r7_tableau` (voix gardée) | Avant : un tableau sans animation. Après : `?vue=trois_voies` — la part de chaque voie au cours de l'effort (phosphocréatine, puis fermentation, puis respiration), une courbe et sa fiche par voie au mot de la voix, puis « à l'examen : le nom + l'équation avec ADP et Pi ». Seuls `visual` et `pointage` changent (mots déjà dits) : la voix reste. |
| `definir`, `qcm_sarcomere` (restitution) | `ms_x4_restitution` (voix gardée), **`ms_x4b_eliminer`** (nouvelle) | x4 écrit son QCM au tableau (`?vue=restitution`, propositions seules). x4b le corrige par la méthode : se redire le cours, puis chaque proposition rayée avec sa raison (b, c), a entourée ; puis un vrai ou faux du sarcomère (« la bande sombre raccourcit ») avec son mot qui décide souligné, posé en question ; la règle et le verdict ne s'écrivent qu'après (`cacher=verdict2`) et la démonstration les écrit. |
| `ordre_etapes` | `ms_c7_ordre` (inchangée) | Déjà joué (`cycle.html?vue=etapes`). |
| `nommer_myogrammes`, `myogramme_document` | `ms_f1` → `ms_f7`, `ms_f6_nomme` (inchangées) | Les tracés se construisent excitation par excitation (`sommation.html`) ; nommer est la question. |
| `legender` | `ms_u6_legender`, `ms_u8_legender_molecules` (inchangées) | Schéma à légender déjà interactif. |
| `inhibiteurs` | `ms_r8_inhibiteurs` (inchangée) | L'expérience est jouée (`inhibiteurs.html`), la voix décrit muscle par muscle, la déduction est la question ; la simulation n'écrit pas la conclusion. |
| `associer_roles`, `voies_equations` | série de fin de `ms_x4_restitution`, `ms_r1`…`ms_r5` | Restitution couverte par la série de fin et par les diapositives des voies (équations écrites). |

### La simulation

`national.html` reçoit quatre vues nouvelles — `entraine`, `intensite`, `trois_voies`, `restitution` — et un paramètre
`?cacher=<moment>` qui tait tout ce qui s'écrit à partir de ce moment jusqu'à `set_parameters {conclusions: true}`.
Les vues `nageurs`, `voies`, `fibres`, `chaine` et le cours en ligne ne changent pas (sans `cacher`, rien n'est caché).
Peinture (règle 32) : fibres musculaires striées, mitochondries à deux membranes et crêtes, muscle qui se contracte.
Vérifiée dans Chromium à 1280 × 640, 1024 × 560 et 724 × 350 : chaque moment atteint par `play_until`, aucune erreur,
aucun texte hors cadre ; `ce_qui_se_voit` suit ce qui est caché ou montré ; `node --check` et
`scripts/verifier_formules.py` sans remarque pour ce fichier.

### Questions par bloc

Les blocs `ms_s5_b1` (r4, r6b), `ms_s6_b2` (x1, x2, x2b) et `ms_s7_b2` (x4, x4b) ont maintenant plusieurs questions :
voulu, un exercice du national joué pas à pas pose **une question par consigne** au lieu de donner la réponse. Aucune
observation ajoutée (le cours en garde deux, la limite de la règle 30).

### Voix et mots

36 → 72 pistes (`_voix.json`) : 6 diapositives (`ms_r6b`, `ms_x1`, `ms_x2`, `ms_x2b`, `ms_x2c`, `ms_x4b`), leurs
réactions, énoncés et 2 démonstrations ; `ms_r7_tableau` et `ms_x4_restitution` gardent leur voix (texte inchangé).
`verifier_mots.py` (même règle, appliquée à la copie en attente) : darija rare remplacé (كنقيسو → كنشوفو شحال,
مستوية → ثابتة, كتستنتج → نقدرو نقولو, كتعوضهاش → ماشي بلاصتها, كتشارك → كتعطي أكثر, كتعيا → la fatigue كتجي بالزربة,
نلعبو → نديرو, غالبة → اللي كتعطي كثر, كتجدد → كتصاوب, كتحسم → المهمة, نشطبوها → نحيدوها, كيقصرو → كيوليو قصار…).
Restent, **à écouter** (termes du sujet ou du programme) : « barème », « fatigabilité », « palier », « traces »,
« raccourcit », « aérobies », et les nombres des données (quarante-quatre, soixante-huit, soixante-dix-neuf,
quatre-vingt-cinq).

### Ce qui reste

- Les voix des pistes nouvelles (VPS, voix Bodi) : rien ne peut être enregistré ici.
- `ms_e2_atpase` : sa question demande la conclusion que la voix vient de dire (`atpase.html` sait la cacher,
  `conclusions: false`) ; la reformuler demande de réécrire une voix déjà faite : laissé pour une prochaine passe.
- Le contrôle de pointage garde ses 5 « introuvable » d'avant (`ms_u6_legender`, `ms_r8_inhibiteurs`), déjà présents
  en ligne ; aucun nouveau.

## Passe du 19 novembre 2026 — compter en allumant, démonstration sur le document

- `national.html` : `allume {cible}` / `eteins` dans toutes les vues (lueur jaune qui reste sur le repère, la dernière
  plus vive ; `commun.js` : `lueur`, `Allumage`). Lignes `allume` sur les démonstrations de `ms_n2_fibres`,
  `ms_r6b_intensite`, `ms_x4b_eliminer`. `?vue=fibres` : le tableau s'allume ligne par ligne ; `?vue=chaine` : les
  six cases s'allument, numérotées 1 à 6.
- `ms_f6_nomme` (`sommation.html?vue=nomme`) : les stimulations comptées une à une (moments `stim_1` … `stim_n`, numéro
  sous chaque créneau, total écrit à la fin) ; pointage « شحال من excitation؟ » → `stim_1`.
- `ms_c7_ordre` (`cycle.html?vue=etapes`) : chaque étape écrite s'allume, repères `etape_1` … `etape_6`.
- Énoncé du national d'abord (professeur, règle 46) : `ms_x1_enonce` (2016 N), `ms_x3_enonce` (2017 R), `ms_n2_enonce`
  (2020 N), chacune en tête de son bloc, sur une feuille d'examen refaite en code
  (`shared/examen/sujets/svt-<année>-<session>-ex<n>.html`) ; voix à enregistrer (3 pistes au `_voix.json`).
