# Audit « rythme et départ de zéro » — chimie (cours 10 à 13)

14 novembre 2026. Règles appliquées : professeur 33 (une chose à la fois, le principe d'abord, le résultat décisif trouvé par l'élève) et 34 (départ de zéro, chaque notion dite deux fois de deux façons), avec 27, 28, 30 et 32.

Rien n'a été modifié dans les cours en ligne. Les nouvelles versions complètes sont en attente :

- `backend/data/courses/en_attente/phys_ch10_cinetique.json` (48 → 56 diapos, 4 → 5 séances, 15 blocs)
- `backend/data/courses/en_attente/phys_ch11_transformations_deux_sens.json` (36 → 42 diapos, 3 → 4 séances, 12 blocs)
- `backend/data/courses/en_attente/phys_ch12_etat_equilibre.json` (36 → 40 diapos, 3 → 4 séances, 10 blocs)
- `backend/data/courses/en_attente/phys_ch13_acides_bases.json` (48 → 52 diapos, 4 → 5 séances, 13 blocs)

Sur chaque diapo nouvelle ou dont la voix a changé, `audio.mixed` est retiré (la voix Bodi sera enregistrée plus tard). Les diapos dont la voix n'a pas changé gardent leur piste, même quand une question d'observation y est ajoutée (la voix s'arrête sur `apres_mot`, elle n'est pas réécrite).

Légende : **vite** = plusieurs expériences, cas ou idées d'un coup ; **donné** = résultat décisif dit au lieu d'être trouvé ; **prérequis** = notion des années d'avant utilisée comme connue ; **une fois** = notion dite d'une seule façon.

## Ce qui est commun aux quatre cours

### Simulation nouvelle : `prerequis.html` (copie identique dans les 4 dossiers)

`frontend/public/media/simulations/chimie/{cinetique-tableau, transformations-deux-sens-tableau, etat-equilibre-tableau, acides-bases-tableau}/prerequis.html` — même fichier (même empreinte md5), même kit (`tableau.js`, `commun.js`, `exposants.js`, `deroule.js`), cadre 760 × 420, un bouton, un curseur par vue, objets peints en couleur sous la craie (règle 32). Huit vues, chacune avec ses moments (`play_until`) et un repère par étape :

| vue | moments | curseur | ce qui est peint |
|---|---|---|---|
| `mole` | entites · douzaine · paquet · millimole · masse | `masse_g` 9 → 90 g | molécules d'eau, boîte d'œufs (la douzaine), caisse en bois (la mole), balance à affichage |
| `concentration` | solute · dissoudre · relation · plus_eau · n_cv | `volume_ml` 50 → 250 mL | verre de montre et cristaux, deux béchers dont la couleur suit C |
| `ion` | atome · perd · gagne · proton · solution | — | atomes Na, Cl, H et leurs électrons qui partent ou arrivent, bécher d'ions qui bougent |
| `equation` | equation · coefficients · une_fois · trois_fois · recette | `fois` 1 → 5 | molécules H₂O₂, I⁻, I₂, H₂O qui réagissent une fois puis n fois |
| `pente` | droite · triangle · pente · courbe · tangente | `date_min` 0 → 30 min | droite + triangle Δt, Δx ; courbe x(t) = 2(1 − e^(−t/8)) (pente 0,25 mmol/min à t = 0, comme l'exemple A) et sa tangente qui glisse |
| `gaz` | ballon · chocs · plus · relation · unites | `molecules` 10 → 60 | ballon fermé, bouchon, manomètre à aiguille, molécules qui rebondissent |
| `puissance` | dix · negatif · ecriture · log · moins_log | `exposant` −7 → 0 | règle en bois graduée de 10⁰ à 10⁻⁷ ; point qui glisse, log et −log écrits |
| `dilution` | mere · prelever · fiole · completer · meme_quantite · facteur | `volume_fiole_ml` 20 → 500 mL | bécher, pipette, fiole jaugée et trait de jauge, gouttes d'eau, couleur qui pâlit |

### Simulations existantes enrichies (additif : le comportement par défaut ne change pas)

Nouveau paramètre `conclusions` (défaut `true`) pour les questions d'observation (règle 30) :

- `cinetique-tableau/limitant.html` : `conclusions: false` tait « épuisé », le cercle et « on garde la plus petite », « x ne peut plus avancer » et l'encadré du réactif limitant ; la bulle après réglage ne nomme plus le limitant. Les barres et leurs valeurs restent (c'est ce que l'élève doit lire).
- `transformations-deux-sens-tableau/equilibre.html` (vue `inverse`) : tait « le pH MONTE… » et sa ligne écrite ; la bulle d'arrêt dit « regarde l'afficheur » au lieu de « l'afficheur MONTE de 2,3 à 3,6 ». L'afficheur, lui, monte.
- `etat-equilibre-tableau/constante.html` (vue `trois_c`) : à l'étape `comparer`, les deux colonnes sont encadrées pareil, sans surlignage jaune ni « ne change pas » ; la bulle d'arrêt ne dit plus la réponse.

Les 4 copies de `deroule.js` n'ont pas été touchées (toujours identiques).

### Repères de pointage déjà désaccordés dans les cours en ligne

Ces mots ne sont plus dans la voix en ligne (la voix a été raccourcie, le pointage non) : ils ne se déclenchaient jamais. Ils sont retirés des copies en attente, la voix n'est pas touchée.

- ch10 : `ci_m1_mesures` « شوف: فالبداية » ; `ci_n1_aspirine` « السؤال التالت », « t un demi égale soixante-dix secondes » (pointage et centre) ; `ci_n2_diminue` « السؤال اللخر », « t un demi égale quatre minutes ».
- ch11 : `td_o2_flacons` « علاش؟ », « هادا هو السؤال ».
- ch12 : `ee_o2_flacons` « واش كاين شي عدد » (deux fois).
- ch13 : `ab_o2_trois_ph` « إذن شنو كاين » (deux fois).

---

## Cours 10 — Suivi temporel, vitesse de réaction (`phys_ch10_cinetique`)

### Audit diapo par diapo

| diapo | constat | fait |
|---|---|---|
| ci_o1_carte | carte d'ouverture, une branche à la fois : correct | — |
| ci_o2_methodes | trois méthodes d'un coup, mais c'est une annonce (chaque méthode a sa partie) | — |
| (avant ci_m1) | **prérequis** : mole, millimole, quantité de matière, concentration, ion (I⁻, H⁺, S₂O₃²⁻), coefficients d'une équation — tous utilisés dès ci_m1 sans être enseignés | 4 rappels de zéro avec animation : `ci_z1_mole`, `ci_z2_concentration`, `ci_z3_ion`, `ci_z4_equation` ; chacun dit deux fois (définition + douzaine / sucre dans un verre ou une bouteille / charge = électrons perdus ou gagnés / recette de gâteau) |
| ci_m1_mesures | une série de mesures, rythme correct (un arrêt par ligne) | repère mort retiré |
| ci_m2_trempe | une idée (la trempe), expliquée deux fois (photo) : correct | — |
| ci_m3_titrage | **vite** : principe du titrage, équivalence, équation du titrage, relation n = C·V_E/2, facteur 10 et résultat dans une seule voix ; **prérequis** : dosage, équivalence (1re bac) supposés connus | coupée : `ci_m3_titrage` (principe : on verse une solution connue jusqu'à ce que tout le diiode ait réagi, équivalence redite d'une autre façon) + question de vérification du principe ; `ci_m3b_calcul` (équation, relation, ×10, redit « un dixième du mélange ») |
| ci_a1_tableau | **vite** : le tableau entier (équation, trois lignes, quatre colonnes) d'un coup | coupée : `ci_a1_tableau` (équation + état initial, x défini comme « le nombre de fois que la recette est faite ») ; `ci_a1b_en_cours` (en cours et état final, le 2x redit par la recette) + question « combien d'ions iodure restent à x = 1,0 mmol » |
| ci_a2_limitant | **donné** : les deux hypothèses puis « on garde la plus petite » ; l'élève ne voit pas lui-même quelle barre se vide | question d'observation : la voix s'arrête sur « شمن وحدة ناخدو؟ », x avance, la simulation tait les conclusions ; « quelle barre de réactif arrive à zéro la première ? » |
| ci_a3_lien | une idée (n(I₂) = x) : correct | — |
| ci_a4_courbe à ci_a7_palier | points placés un à un, lecture, composition, palier : rythme correct, une idée par diapo | — |
| ci_g1_cellule, ci_g2_ions | une idée chacune ; l'ion est maintenant enseigné avant (`ci_z3_ion`) | — |
| ci_g3_formule | formule + exemple + conversion d'unités : dense, mais la formule est montrée pièce par pièce | non coupée (voir « non fait ») |
| ci_g4_descend à ci_g6_calcul | une idée par diapo, arrêts par étape | — |
| ci_p1_ballon | une expérience, bien découpée | — |
| ci_p2_relation | **prérequis** : loi des gaz parfaits (1re bac) utilisée comme connue | rappel `ci_z6_gaz` juste avant (chocs des molécules = pression ; P·V = n·R·T ; unités ; redit par le ballon de foot qu'on gonfle) |
| ci_p3 à ci_p6 | une méthode ou un sujet par diapo | — |
| ci_v1_pente | triangles successifs, correct | — |
| ci_v2_definition, ci_v3_tangente | **prérequis** : pente, coefficient directeur, tangente (mathématiques) | rappel `ci_z5_pente` entre v1 et v2 (droite, triangle Δx/Δt, courbe, tangente qui touche en un point ; redit « en agrandissant la courbe, elle ressemble à une petite droite ») |
| ci_v4_bareme | calcul au barème, une ligne à la fois : correct | — |
| ci_v5_diminue | **donné** : les trois valeurs puis « la vitesse diminue » dit tout de suite | question d'observation : la voix s'arrête après la 3ᵉ valeur, « comment évoluent les trois valeurs de v ? » ; la phrase suivante (« القيم كينقصو ») confirme |
| ci_v6 à ci_v8, ci_h1 à ci_h4 | une idée par diapo, arrêts par tangente ou par geste | — |
| ci_n1 à ci_n8 | sujets du national : longs (800 à 1 200 caractères), plusieurs questions d'un même sujet enchaînées | non coupés (voir « non fait ») |
| ci_r1, ci_r2, ci_bl, ci_cr | pièges, bilan, carte | — |

### Questions et blocs

Nouvelles questions « À toi » (une par bloc) : `ci_z4_equation` (coefficients), `ci_m3_titrage` (principe de l'équivalence), `ci_a1b_en_cours` (ligne en cours). Chacune a ses réactions préparées juste / faux 1 / faux 2 (`parole` et `ecrit`) et, pour les calculs, sa démonstration.

Blocs refaits : `ci_r_b1` [o1, o2, z1], `ci_r_b2` [z2, z3, z4], `ci_s1_b1` [m1, m2, m3], `ci_s1_b2` [m3b, a1, a1b], `ci_s1_b2b` [a2, a3], puis les blocs d'origine (`ci_s2_b2` reçoit `ci_z6_gaz`, `ci_s3_b1` reçoit `ci_z5_pente` : 5 diapos, dont un rappel court). Nouveaux blocs avec leur `cahier`, `retrouver` et `exercice` (réactions comprises). Compétences mises à jour (C2 : z1, z2, z4, a1b ; C3 : z3, m3b, z6 ; C5 : z5).

---

## Cours 11 — Transformations dans les deux sens (`phys_ch11_transformations_deux_sens`)

### Audit diapo par diapo

| diapo | constat | fait |
|---|---|---|
| td_o1_carte, td_o2_flacons | ouverture, une question posée : correct | repères morts retirés (o2) |
| (avant td_b1) | **prérequis** : ion, proton H⁺ (« un acide cède un proton »), concentration, n = C·V, puissances de dix et log (pH = −log[H₃O⁺]) | rappels `td_z1_ion` (centré sur H⁺ = un proton seul, + question), `td_z2_concentration`, `td_z3_puissance` (règle des puissances de dix, log = l'exposant ; redit « dix puissance combien donne ce nombre ? ») |
| td_b1_acide, td_b2_base | une idée chacune, la base redite par le ballon qu'on se passe : correct | — |
| td_b3_couple | **vite** : notation, demi-équation, double flèche, quatre couples, et l'eau dans deux couples d'un coup | coupée : `td_b3_couple` (AH/A⁻, deux exemples, redit « la seule différence est un proton ») ; `td_b3b_eau` (l'eau dans deux couples, redit « elle vend et elle achète le proton ») + question « rôle de l'eau dans H₃O⁺/H₂O » |
| td_b4_reaction | une idée : correct | — |
| td_p1_ph, td_p2_calcul | le log était supposé connu | enseigné avant (`td_z3_puissance`) |
| td_p3 à td_p6 | une manip ou un raisonnement par diapo | — |
| td_a1 à td_a6 | tableau, x_max, x_f, τ, totale, relation : une étape par diapo | — |
| td_e1_inverse | **donné** : « le pH monte » dit en même temps que l'afficheur | question d'observation : la voix s'arrête sur « شوف l'afficheur الثاني: », la simulation tait « le pH MONTE », « que fait le pH ? » |
| td_e2 à td_e6 | une idée par diapo | — |
| td_c1 à td_c3 | conductimétrie, une étape par diapo | — |
| (avant td_d1) | **prérequis** : le geste de la dilution (pipette, fiole jaugée, C₀·V₀ = C₁·V₁, TC) | rappel `td_z4_dilution` (redit : dix personnes dans une petite ou une grande pièce) |
| td_d1_dilution | **vite** : trois béchers, deux dilutions et le tableau dans une seule voix | coupée : `td_d1_dilution` (bécher 1, la première dilution, bécher 2) ; `td_d1b_mesures` (la seconde dilution, bécher 3, tableau, redit « chaque dilution diminue H₃O⁺ par litre ») + question de calcul de C₁ |
| td_d2_taux | **donné** : « τ augmente » dit après les trois lignes | question d'observation sur « شوف les barres: » : « plus la solution est diluée, que font les barres de τ ? » |
| td_d3_nature | trois acides d'un coup, mais un arrêt par bécher | non coupée |
| td_n1 à td_n4 | sujets du national longs (770 à 935 caractères) | non coupés |

### Questions et blocs

Nouvelles questions : `td_z1_ion`, `td_b3b_eau`, `td_d1b_mesures` (avec démonstration). Blocs : `td_r_b1` [o1, o2, z1], `td_r_b2` [z2, z3, b1], `td_s1_b1` [b2, b3, b3b], `td_s1_b2` [b4, p1, p2], …, `td_s3_b1` [c1, c2, c3], `td_d_b1` [z4, d1, d1b], … Compétences : C1 (z1, b3b), C2 (z3), C3 (z2), C6 (z4, d1b).

---

## Cours 12 — État d'équilibre d'un système chimique (`phys_ch12_etat_equilibre`)

### Audit diapo par diapo

| diapo | constat | fait |
|---|---|---|
| ee_o1_carte, ee_o2_flacons | ouverture | repères morts retirés (o2) |
| (avant ee_r1) | **prérequis** : concentration (le cours ne parle que de concentrations), puissances de dix (Qr = 10^(−2pH)/…), log | `ee_z1_concentration` (+ question C = n/V), `ee_z2_puissance` |
| ee_r1_taux, ee_r2_equilibre | rappels du chapitre 11, déjà là ; denses (800 caractères) mais une notion chacun | — |
| ee_q1 à ee_q5 | une règle par diapo (produits en haut, eau, solides, unité) | — |
| ee_i1_initial | une idée | — |
| ee_i2_melange | **vite** : quatre flacons, le mélange, V_T, la règle des concentrations, Qr,i, la simplification et le calcul dans une seule voix (1 061 caractères) | coupée : `ee_i2_melange` (flacons, mélange, concentrations après mélange, redit « chaque espèce est répartie dans 300 mL ») garde sa question ; `ee_i2b_calcul` (Qr,i, V_T se simplifie, calcul) |
| ee_i3_au_cours | points successifs, correct | — |
| ee_e1 à ee_e3 | une étape par diapo | — |
| ee_k1_trois | **donné** : « Qr,éq ne dépend pas de C » dit dès les trois lignes posées | question d'observation après la 3ᵉ ligne : « laquelle des colonnes τ ou Qr,éq garde presque la même valeur ? » ; la simulation tait le surlignage |
| ee_k2_produits | expérience dense (1 045 caractères) mais une seule expérience, arrêts par étape | non coupée |
| ee_k3 à ee_m4 | une idée par diapo | — |
| (avant ee_f1) | **prérequis** : dilution | `ee_z3_dilution` |
| ee_f1 à ee_f4 | une comparaison par diapo, barres une à une | — |
| ee_n1 à ee_n6 | sujets du national | non coupés |

### Questions et blocs

Nouvelle question : `ee_z1_concentration` (avec démonstration). Blocs : `ee_r_b1` [o1, o2, z1], `ee_s1_b1` [z2, r1, r2], `ee_s1_b3` [q5, i1, i2, i2b, i3], `ee_s3_b1` [z3, f1, f2, f3, f4] (5 diapos, dont un rappel court), les autres inchangés. Compétences : C2 (z1, i2b), C3 (z2), C6 (z3).

---

## Cours 13 — Réactions acido-basiques (`phys_ch13_acides_bases`)

### Audit diapo par diapo

| diapo | constat | fait |
|---|---|---|
| ab_o1_carte, ab_o2_trois_ph | ouverture | repères morts retirés (o2) |
| (avant ab_r1) | **prérequis** : puissances de dix et log (Ke = 10⁻¹⁴, pKe, Ka, pKa partout) | `ab_z1_puissance` + question « −log(10⁻⁵) » |
| ab_r1_rappel | **vite** : acide, base, couple, exemples, l'eau dans deux couples et le pH dans un seul rappel | coupée : `ab_r1_rappel` (acide, base, couple ; redit par le ballon) ; `ab_r1b_eau_ph` (l'eau, le pH ; redit « le pH est l'exposant sans le signe moins ») |
| ab_r2_constante | rappel du chapitre 12 | — |
| ab_w1 à ab_w5, ab_b1 à ab_b3 | une notion par diapo | — |
| ab_a1 à ab_a5, ab_c1 à ab_c3, ab_k1 à ab_k4 | une notion par diapo ; c1 et c2 comparent deux solutions avec un arrêt chacune | — |
| ab_p1 à ab_p4, ab_i1, ab_i2 | une notion par diapo | — |
| ab_d1 à ab_d5 | dosage, une étape par diapo | — |
| (avant ab_d6) | **prérequis** : dérivée = pente de la tangente (mathématiques) | `ab_z2_pente` (même animation que le cours 10, la voix part de « avant la courbe dérivée » et finit par « dpH/dV_B est la pente de la courbe du pH ») |
| ab_e1_phe | **vite** + **donné** : trois courbes et trois pH_E dans une voix ; arrêt par courbe déjà là | question d'observation sur la 3ᵉ courbe : « son point E est-il au-dessus ou au-dessous de 7 ? » |
| ab_e2 à ab_e4 | une idée par diapo | — |
| ab_e5_conductimetrie | **vite** : montage, mesures, deux droites, pourquoi (loupe), équivalence et calcul (1 053 caractères) | coupée : `ab_e5_conductimetrie` (les deux droites, redit « comme la lettre V ») ; `ab_e5b_pourquoi` (la loupe, la rupture de pente, le calcul) |
| ab_n1 à ab_n5 | sujets du national longs | non coupés |

### Questions et blocs

Nouvelle question : `ab_z1_puissance`. Blocs : `ab_r_b1` [o1, o2, z1], `ab_s1_b1` [r1, r1b, r2], `ab_s3_b3` [d3, d4, d5, z2, d6], `ab_s4_b2` [e5, e5b, n1, n2, n3] (5 diapos chacun : un rappel court ou une coupe), les autres inchangés. Compétences : C1 (z1, r1b), C7 (e5b), C8 (z2).

---

## Voix à enregistrer (voix Bodi, kernel d'essai)

Toutes les voix nouvelles suivent la skill `voix-du-cours` (darija simple, termes du programme en français, nombres et unités en mots, ni chiffre ni symbole ni tachkil) ; contrôle automatique fait : aucun chiffre ni symbole dans `speech_text.mixed`, `enonce_dit`, `parole`, `dit`. Le contrôle du corpus (`verifier_texte_corpus.py`) a été passé sur toutes les voix nouvelles ; les mots darija absents du corpus que j'avais écrits ont été remplacés ; restent des mots déjà présents dans les voix en ligne (« نعايرو », « كنقيسو », « الخليط »…) et des termes du programme rares (diiode, iodure, fiole jaugée…).

### Cours 10 — 44 pistes

- Diapos (voix complète) : `ci_z1_mole`, `ci_z2_concentration`, `ci_z3_ion`, `ci_z4_equation`, `ci_m3_titrage`, `ci_m3b_calcul`, `ci_a1_tableau`, `ci_a1b_en_cours`, `ci_z5_pente`, `ci_z6_gaz` (10).
- Questions nouvelles (énoncé + 5 réactions, + démonstration quand il y a un calcul) :
  - `ci_z4_equation` « combien d'ions iodure pour 3 molécules d'eau oxygénée ? » (énoncé, 5 réactions, démonstration) ;
  - `ci_m3_titrage` « que signifie la disparition de la couleur brune ? » (énoncé, 5 réactions) ;
  - `ci_a1b_en_cours` « combien d'ions iodure restent à x = 1,0 mmol ? » (énoncé, 5 réactions, démonstration).
- Observations (énoncé, 2 indices, 3 retours, solution = 7 pistes chacune) : `ci_a2_limitant` « quelle barre de réactif arrive à zéro la première ? » ; `ci_v5_diminue` « comment évoluent les trois valeurs de v ? ».

### Cours 11 — 41 pistes

- Diapos : `td_z1_ion`, `td_z2_concentration`, `td_z3_puissance`, `td_b3_couple`, `td_b3b_eau`, `td_z4_dilution`, `td_d1_dilution`, `td_d1b_mesures` (8).
- Questions : `td_z1_ion` « que reste-t-il quand H perd son électron ? » (énoncé, 5 réactions) ; `td_b3b_eau` « rôle de l'eau dans H₃O⁺/H₂O » (énoncé, 5 réactions) ; `td_d1b_mesures` « nouvelle concentration après dilution » (énoncé, 5 réactions, démonstration).
- Observations : `td_e1_inverse` « que fait le pH ? » ; `td_d2_taux` « que font les barres de τ ? » (7 pistes chacune).

### Cours 12 — 19 pistes

- Diapos : `ee_z1_concentration`, `ee_z2_puissance`, `ee_i2_melange`, `ee_i2b_calcul`, `ee_z3_dilution` (5). La question d'`ee_i2_melange` est celle d'aujourd'hui, déjà voixée.
- Question : `ee_z1_concentration` « que vaut C ? » (énoncé, 5 réactions, démonstration).
- Observation : `ee_k1_trois` « laquelle des colonnes garde la même valeur ? » (7 pistes).

### Cours 13 — 19 pistes

- Diapos : `ab_z1_puissance`, `ab_r1_rappel`, `ab_r1b_eau_ph`, `ab_z2_pente`, `ab_e5_conductimetrie`, `ab_e5b_pourquoi` (6).
- Question : `ab_z1_puissance` « que vaut −log(10⁻⁵) ? » (énoncé, 5 réactions).
- Observation : `ab_e1_phe` « point E au-dessus ou au-dessous de 7 ? » (7 pistes).

**Total : 123 pistes** (29 voix de diapo, 8 questions nouvelles avec leurs réactions et 5 démonstrations, 6 questions d'observation). Les `retrouver` et `exercice` des nouveaux blocs ont leurs réactions écrites ; ils ne sont pas voixés aujourd'hui (fin de bloc = cahier seulement, `FIN_DE_BLOC_COMPLETE = False`).

## Vérifications faites

- JSON valide (écrit par `json.dump`, `ensure_ascii=False`, `indent=2`, fin de ligne LF).
- Chaque `mot` de pointage et du centre est dans sa voix ; chaque `apres_mot` est trouvé une seule fois ; chaque mot de démonstration est dans sa parole.
- Chaque `play_until` cite un moment qui existe (moments de `prerequis.html`, ou moments déjà utilisés par le cours en ligne pour les autres simulations) ; chaque repère de `prerequis.html` cité existe.
- Chaque bloc a exactement une question « À toi » ; les blocs suivent l'ordre des diapos ; chaque diapo est dans une compétence.
- `node --check` sur le script de `prerequis.html`, `limitant.html`, `equilibre.html`, `constante.html` : OK.
- Navigateur sans écran (Chromium de Playwright, serveur Vite) : les huit vues de `prerequis.html` jouées jusqu'à la fin et regardées (une erreur de dessin de la fiole jaugée corrigée) ; `limitant.html`, `equilibre.html?vue=inverse` et `constante.html?vue=trois_c` avec `conclusions: false` : la conclusion n'est plus écrite.

## Ce qui n'est pas fait ou pas vérifié

- Les sujets du national (`ci_n*`, `td_n*`, `ee_n*`, `ab_n*`, 800 à 1 300 caractères) enchaînent plusieurs questions d'un même sujet ; ils ne sont pas coupés (ce sont des corrigés, pas des expériences). À reprendre si l'on veut une question par arrêt.
- `ci_g3_formule`, `ee_k2_produits`, `td_d3_nature` restent denses ; non coupées.
- Les voix nouvelles ne sont pas enregistrées (pas de GPU Kaggle ici) : pas de vérification de murmure ni de transcription.
- Le lecteur complet (`/dev/course-player`) n'a pas été rejoué avec les copies en attente (elles ne sont pas servies) : l'arrêt de la voix sur `apres_mot` et le moment exact des gestes n'ont pas été vus en vrai. Sur `ci_a2_limitant` et `td_e1_inverse`, le repère de pointage suivant part 0,9 s avant son mot, donc juste avant l'arrêt : c'est pour cela que ces deux simulations taisent la conclusion par `sim_avant`.
- `controler_cadre.py` (cadre de référence) et `preparer_reponses.py verifier` n'ont pas été passés (ce dernier échouera tant que les pistes manquent).
