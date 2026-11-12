# Avancement — agent PHYSIQUE-CHIMIE (10 novembre 2026)

Brief : BRIEF.md (même dossier). Témoin : phys_ch2_ondes_periodiques (ne pas toucher).
Organisation : un sous-agent Opus par cours (deux en parallèle au plus), chacun tient sa section ci-dessous.
Étapes par cours : 1 exploration · 2 ancien cours · 3 cours JSON · 4 simulations · 5 cadre OK · 6 réactions (texte) · 7 vérifications.

## Décisions à faire valider
- ondes_lumineuses — relations du prisme (sin i = n·sin r, sin i' = n·sin r', A = r + r', D = i + i' − A) :
  tranché par l'agent principal physique-chimie. Elles sont au programme (OP-PC-2007) mais aucun national PC 2016-2025
  ne les demande et le cadre de référence de l'examen ne retient du prisme que la dispersion (milieu dispersif, n dépend
  de la fréquence). Donc : la dispersion est traitée en entier dans le corps du cours (C8) ; les quatre relations forment une
  courte partie finale (C9, 3-4 diapositives), annoncée « pour les devoirs, pas demandée au national », capacité OL11
  marquée dans la fiche du cadre avec statut « programme, hors examen national ».
- ondes_lumineuses (agent du cours) : appliqué tel quel (C9 = 4 diapositives finales, avant le bilan). Autres choix à valider :
  bilan et carte rattachés à C1 (comme le témoin) ; dispersion du prisme dessinée ×2 pour l'œil ; cuve : fente et écran dans l'eau ;
  axe D en cm sur la figure 2021 N (comme l'examen) ; les « dit » du cadre écrits teta / nu / lambda zéro (corpus de la voix).

## Organisation (agent principal, 11 novembre 2026, soir)
- radioactivite (agent a485116da3e8ce287) et energie_nucleaire (agent a9ce952a9eeac6b1f) relancés avec les NOUVELLES RÈGLES :
  méthode des blocs (methode_blocs/BRIEF_AGENTS.md : seances, rappels, prediction, blocs.py verifier « blocs : OK »),
  réactions = seulement items.json dans <clé>_build/ (pas de SSH, le coordinateur les écrit), images en flux seulement.
- Ensuite, deux à la fois : dipole_RC, dipole_RL, circuit_RLC, puis chimie (transformations_lentes_rapides, cinetique,
  transformations_deux_sens, etat_equilibre, acides_bases).
- DISQUE C: 256 Mo libres le 11/11 au soir (Temp/claude fait 2,1 Go, dont 1,4 Go dans une session youtube-channel
  6be32ec57d3abeb1/fd624a13… qui n'est pas la nôtre : à faire nettoyer par l'utilisateur / le coordinateur). Puis 107 Mo seulement : URGENT, risque
  d'échec d'écriture des fichiers de cours.

- energie_nucleaire (agent du cours) : fission de l'²³⁵U et courbe d'Aston enseignées dans le corps du cours (au programme) alors
  qu'aucun national PC 2016-2025 ne les pose (exercice de fission construit, dit « pas tombé au national ces dernières années ») ;
  E = hν (2016 seulement) et rendement de centrale non retenus ; E_ℓ/A écrit ainsi (ξ admis) ; Δm pour le noyau ET la réaction
  (comme les énoncés), le cours dit lequel ; bornes d'Aston « environ 20 » et « environ 190 » ; « exothermique/endothermique »
  évités (mis en hors cadre) ; bilan et carte rattachés à C9 « rédiger » ; aucune vidéo filmée en vraie classe (toutes en studio) ;
  capacités EN1-EN8 du cadre à collationner avec le texte officiel.

## Cours

(chaque sous-agent ajoute / met à jour sa section : étape faite, fichiers, nb diapositives, compétences, simulations,
décisions, problèmes, « prêt pour la voix : oui/non »)

## ondes_lumineuses
- Étape 1 exploration : déjà faite (backend/data/curriculum/exploration/ondes_lumineuses.json), reprise telle quelle.
- Étape 2 ancien cours : aucun (cours_existant.fichier = null, dossier images ch3_ondes_lumineuses vide) ; aucune ancienne simu reprise.
- Étape 4 simulations : FAITES (6 sous-agents Opus), dossier frontend/public/media/simulations/physics/ondes-lumineuses-tableau/ :
  commun.js, exposants.js, lumiere.css (copies du témoin), diffraction.html (vues ouverture|figure|reglage|mesure|fil|cuve|blanche),
  ecart-angulaire.html (montage|triangle), courbe.html (L_inverse_a|L_a|theta_inverse_a|L_D), spectre.html, milieu.html
  (verre|eau|deux), prisme-dispersion.html (blanche|rouge|verte), prisme-angles.html, figures.html (12 ?fig=), bilan.html, carte.html.
  Contrat (noms de moments/repères) : cours/ondes_lumineuses_contrat_simulations.md (même dossier que ce fichier). node --check OK
  partout, testées en headless par les sous-agents.
- Étape 3 cours : ÉCRIT → backend/data/courses/phys_ch3_ondes_lumineuses.json (53 diapositives, 51 questions à clé, 11 exercices,
  demonstration sur chaque calcul). Généré par des scripts python : cours/ondes_lumineuses_build/ (outils.py, p1..p5.py = contenu,
  build.py → écrit le JSON ; `python build.py --garder-reponses` garde les réactions déjà posées). Modifier le contenu dans p*.py,
  jamais à la main dans le JSON (sinon le refaire depuis les p*.py).
  verifier_texte_corpus : darija 0 mot rare ; restent ~140 mots français rares = termes du programme gardés exprès (radiation,
  spectre, dispersion, nanomètres, ultraviolet, infrarouge, violet, extinction, vue de dessus…).
- Étape 5 cadre : FAIT. Fiche chapitres.ondes_lumineuses ajoutée par cours/ondes_lumineuses_build/cadre_ol.py (relit, remplace la
  seule clé, réécrit). Lectures écrites comme le corpus (teta, nu, lambda zéro). controler_cadre → « cadre : OK » (≈50 « à relire »
  non bloquants : applications numériques dites en lettres, distracteurs faux des QCM).
- Étape 6 réactions (texte) : FAIT. items 319 → gen_reponses_vps.py sur moalim-vps (/tmp/gen_rep_ol, nettoyé) 319/319 → posées
  (concentration.reponses). Deux paroles corrigées à la main (θ et « 2D » écrits). Liste des pistes à dire : scratchpad pistes.json
  (régénérable : `preparer_reponses.py poser` refait la liste).
- Étape 7 vérifications : node --check OK sur les 10 pages + commun.js/exposants.js ; preparer_reponses verifier : seules
  manquent les voix (53 pistes de diapositives + 319 réactions) ; vérif. navigateur headless (Playwright, Chrome) de chaque
  diapositive à simulation (ondes_lumineuses_build/verif_sims.py) : aucune erreur JS, encre, chaque moment play_until et chaque
  repère du cours existent dans la simulation. Petit défaut : ecart-angulaire et courbe signalent 1 texte « hors cadre » au tout
  premier dessin (avant le chargement de la police), plus rien ensuite.
- programme_semestre1.json : ondes_lumineuses → statut « construit », cours phys_ch3_ondes_lumineuses (petit script prog.py).
- PRÊT POUR LA VOIX : OUI (Bodi, par la session principale) : 53 pistes speech_text.mixed + 319 réactions (+ démonstrations).
- Reste : voix ; publier_labo / ressources de leçon seulement après validation ; manips labo 3D P4 et P5 non construites
  (planifiées dans l'exploration) ; lecture dans le lecteur /dev/course-player non faite (seulement les pages seules).
- À valider (ondes_lumineuses) : C9 prisme en 4 diapositives finales « pour le devoir » ; le bilan et la carte rattachés à C1
  comme dans le témoin ; fig_enonce_2021 garde l'axe D en cm comme l'examen ; la vue de gauche de diffraction s'appelle « Vue de
  côté » quand la fente est horizontale ; dans la cuve la fente ET l'écran sont dans l'eau (pour L' = L/n exact) ; dispersion du
  prisme dessinée ×2 pour l'œil (écrit au tableau) ; mot « électromagnétique » non employé (« n'est pas une onde mécanique »).
  Plan : I diffraction (6, C1) · II θ = λ/a (4, C2) · III L = 2λD/a (9, C3) · IV comparer (5, C4) · V courbes (5, C5) ·
  VI radiation (4, C6) · VII milieu n (5, C7) · VIII dispersion (5, C8) · IX cas types + nationaux 2023 R, 2021 N, 2025 R (4) ·
  X pour le devoir : relations du prisme (4, C9) · XI bilan + carte (2).
- Décision appliquée : relations du prisme en partie finale courte C9 (4 diapositives) annoncée « pour le devoir, pas au national ».

## dipole_RC
(sous-agent Opus du cours phys_ch6_dipole_RC, « Dipôle RC » ; outils : cours/dipole_RC_build/ ; audits : dipole_RC_build/audits/)
- 11/11 : démarré, briefs et skills lus. Disque C: 2,1 Go libres.
- Étape 1 exploration : EN COURS. 10 vidéos choisies (une à la fois, brief dipole_RC_build/audit_brief.md, images en flux) :
  kzF1OzfrQ2w Noureddine (FAIT, sans sous-titres : images), sOQaDQkAY94+1xgsRm7SQI8 TOP PHYSIQUE (FAIT, transcription seule),
  AOK4FfniVZA Driss DOTCOM (FAIT), mi1PcyGfR64 Zakaria Taousse, LUDX35FMJmY Hassan El Omrani, 0xCZvA5Wl-0 Laksabi,
  GVSldw4rz8c Ridouan, hstTUKPqT5s Atif, gm5vLzAjBms Cours du Soir (B. Mouslim), OSLLzhxUtp0 Lahoucine Hajji (nationaux corrigés).

- 12 nov. (routine cloud) : Étape 1 FAITE → backend/data/curriculum/exploration/dipole_RC.json (sous-agent, ≈ 125 Ko, mêmes clés que
  operations_formes.json) : 9 audits (Laksabi, Driss, Ridouan, El Omrani, Mouslim, Atif, Noureddine, Taousse, TOP PHYSIQUE) + les 20 nationaux PC
  2016-2025 du dépôt (RC dans 11/20). 10e vidéo (OSLLzhxUtp0) NON auditée : YouTube bloqué depuis le cloud (yt-dlp absent) → « vidéos non auditées ».
  Plan : 48 diapositives (25 prédictions), 4 séances × 3 blocs × 4, compétences C1–C8 (3–4 rappels), cadre RC1–RC9 provisoire, 8 simulations
  à créer (moments nommés), labo-3d/rc gardé comme manip. Ancien matériel : seed phys_ch6_l1.json, image circuits_lab.webp (pas d'ancien cours).
  Décisions à valider : associations de condensateurs gardées (2018 N) ; charge à courant constant gardée (3 sujets, à ajouter à perimetre.json) ;
  RC·du_C/dt + u_C = E puis forme des corrigés ; pas de ln u_C = f(t) ; énergie ½ C u_C² admise ; analyse dimensionnelle de τ (1 diapo) ; en décharge
  i < 0 avec le sens de la charge (2018 N fait l'autre choix) ; prérequis « fonction_exponentielle » à ajouter. Erreurs dans 2 corrigés du dépôt :
  2024 R (10⁻⁴ F = 0,10 µF) et 2023 R (7,2·10⁻⁶ J = 0,72 mJ). Reste : cadre, contrat + simulations, cours JSON, blocs, items, contrôles.
- 12 nov. (routine cloud, 2ᵉ passage) : COURS CONSTRUIT → backend/data/courses/phys_ch6_dipole_RC.json (draft, concentration) : 48 diapositives
  (plan de l'exploration, préfixe rc_), 48 questions, 25 prédictions, 27 exercices, démonstration sur chaque calcul ; 10 parties (I condensateur,
  II associations + courant constant, III échelon, IV équation différentielle, V solution, VI τ et décharge, VII lire les courbes, VIII énergie,
  IX deux nationaux 2019 N / 2021 R, X bilan + carte) ; compétences C1-C8 (cadre RC1-RC9). Build : dipole_RC_build/ (p1…p4.py écrits par 4
  sous-agents, check_part.py ; refaire : `python3 dipole_RC_build/build.py --garder-reponses` puis ajouts.py + `blocs.py appliquer`).
- Cadre : chapitres.dipole_RC ajoutée (dipole_RC_build/cadre_rc.py : RC1-RC9, 24 formules, 20 mots hors cadre, 7 décisions).
  controler_cadre → « cadre : OK » (471 « à relire » non bloquants : applications numériques, lectures dites). programme_semestre1 : construit.
- Simulations (frontend/public/media/simulations/physics/dipole-rc-tableau/, contrat cours/dipole_RC_contrat_simulations.md, 3 sous-agents) :
  condensateur (plaques|charge), intensite, generateur-courant, circuit-rc (montage|charge|decharge), courbe-charge (tableau|R|tangente|pourcent),
  quatre-courbes (q_i|uC_uR|quatre|descente), continuite (enchaine|decharge), energie (lampe|calcul), figures (23 ?fig=), bilan (8 blocs), carte.
  node --check OK ; chaque page testée en headless par son agent (moments, repères, rien hors cadre).
  verif_sims.js (Playwright node, headless) sur les 48 diapositives : 48 ok, « AUCUN PROBLÈME » (moments play_until joués, repères, encre, pas d'erreur JS, rien hors cadre).
- Méthode des blocs : ajouts.py (blocs_s1..s4.json des agents + rappels du plan de l'exploration, C2_r4 réécrit pour ne pas écrire « I₀ = q/C »)
  → methode_blocs/ajouts/phys_ch6_dipole_RC.json : 4 séances × 3 blocs × 4 diapositives, 29 rappels, 25 prédictions / 48. blocs.py verifier →
  « cadre : OK », « blocs : OK ». preparer_reponses verifier : seulement voix et réactions manquantes.
- Réactions : items seulement → dipole_RC_build/items_cours.json (403), items_blocs.json (89), demos_blocs.json (3). À écrire sur le serveur.
- verifier_texte_corpus : 272 mots à revoir ; darija rare surtout des formes conjuguées ou négatives (كتنقزش, كيدوزش, فالطلوع…) une ou deux fois
  chacune, et termes du programme (additivité, échelon, transitoire, microfarads…) : gardés, à écouter au contrôle des murmures.
- PRÊT POUR LA VOIX : OUI (48 pistes speech_text.mixed + démonstrations) ; réactions à écrire d'abord (items).
- Reste : réactions (serveur), voix, validation ; manip labo 3D rc non reliée ; lecture dans le lecteur /dev/course-player non faite. Cours suivant : dipole_RL (exploration à faire).
- À valider (en plus des décisions de l'exploration et du cadre) : bilan et carte en slide_type « evaluation », rattachés à C1 ; e8 (2023 R) répond
  « dq/dt + (1/RC)·q = E/R » et la case décharge de q écrit « RC·dq/dt + q = 0 » (formes hors de la liste du cadre, « à relire ») ; questions de
  prédiction changées pour ne pas être soufflées par la simulation (s6 : u_C à 2τ ; s8 : quelle courbe a la forme de i ; t2 : C doublé) ; c2 « qu'indique » ;
  g2 « que vaut C ? » ; exercice 2018 N placé sur a2 ; fig_energie_2023R non utilisée (l8 garde energie?vue=calcul) ; quelques lectures d'équations
  dites > 10 mots sans virgule (comme le « dit » du cadre).
- Note dépôt : les fichiers *.json hors backend/data sont ignorés par .gitignore : les items, ajouts et blocs_s*.json sont ajoutés avec `git add -f`.
  Les items de radioactivite et operations_formes (perdus aux passages précédents) ont été régénérés et commités ce passage.

## dipole_RL
(routine cloud du 12 nov., cours phys_ch7_dipole_RL, « Dipôle RL » ; outils : cours/dipole_RL_build/ ; contrat : cours/dipole_RL_contrat_simulations.md)
- Étape 1 exploration : FAITE → backend/data/curriculum/exploration/dipole_RL.json (dipole_RL_build/explo.py = explo_a.py + explo_b.py + nationaux).
  VIDÉOS NON AUDITÉES : YouTube bloqué depuis le cloud (yt-dlp absent, pip refusé). Appui : les 20 nationaux PC 2016-2025 du dépôt
  (analyse complète : dipole_RL_build/nationaux.md ; RL dans 10 sessions sur 20, une par année, 1,5 à 4 pts ; équation différentielle et valeur
  de L dans les 10), perimetre.json, exploration dipole_RC (même méthode). À compléter par 10 audits vidéo depuis le PC avant validation.
  Plan : 48 diapositives, 4 séances × 3 blocs × 4, 19 prédictions, compétences C1-C8 (28 rappels), toutes les capacités RL1-RL8 couvertes.
  Ancien matériel : seed phys_ch7_l1.json (labo guidé, τ = L/R sans r) ; CircuitLab advanced/electricity (à ne pas reprendre).
- Étape 5 cadre : chapitres.dipole_RL ajoutée (dipole_RL_build/cadre_rl.py : RL1-RL8, 17 formules, 12 mots hors cadre). programme_semestre1 : explore.
- Erreurs relevées dans le dépôt (nationaux.md § 6) : corrigé 2024 N 2.2.2 faux (τ = 6,7·10⁻⁴ s au lieu de 2 µs : axe i en mA lu en A) ;
  données manquantes dans exam.json (2016 R, 2017 N, 2018 R, 2020 N, 2024 N : seulement dans extraction.json) ; 2022 R : questions RL liées aux
  figures RLC/mécanique ; hors RL : 2021 R III.1 courbes inversées, 2024 R C = 0,10 µF incohérent, 2023 R µJ écrits mJ.
- À valider (exploration) : analyse dimensionnelle de τ et influence de R gardées (1 diapo chacune) alors que jamais au national ; étincelle en une
  phrase, diode + R₁ par l'exercice 2025 R, « roue libre » jamais dit ; courant triangulaire (GBF) pour faire voir u = L·di/dt (b6-b7) ;
  I₀ écrit (I_p annoncé), u_b écrit (u_L, u_B annoncés) ; couleurs vert = établissement, bleu = rupture.
- COURS CONSTRUIT (même passage) → backend/data/courses/phys_ch7_dipole_RL.json (draft, concentration) : 48 diapositives (préfixe rl_),
  48 questions, 22 prédictions, 33 exercices, démonstration sur chaque calcul ; 10 parties (I bobine, II tension, III échelon, IV équation,
  V solution et τ, VI rupture, VII lire les courbes, VIII énergie, IX nationaux 2022 R et 2024 N, X bilan + carte) ; C1-C8 (cadre RL1-RL8).
  Build : dipole_RL_build/ (p1…p4.py écrits par 4 sous-agents, check_part.py « AUCUNE ERREUR » chacun ; refaire : `python3 dipole_RL_build/build.py
  --garder-reponses` puis ajouts.py + `blocs.py appliquer`).
- Méthode des blocs : ajouts.py → methode_blocs/ajouts/phys_ch7_dipole_RL.json : 4 séances × 3 blocs × 4 diapositives, 28 rappels,
  22 prédictions / 48. blocs.py verifier → « cadre : OK », « blocs : OK ». controler_cadre → « cadre : OK » (295 « à relire » : applications
  numériques et lectures dites). preparer_reponses verifier : seulement réactions et pistes audio manquantes.
- Réactions : items seulement → dipole_RL_build/items_cours.json (435), items_blocs.json (97), demos_blocs.json (2). À écrire sur le serveur.
- verifier_texte_corpus (texte_parle.py copié de backend/kaggle_tts dans le scratchpad, il manque dans outils/cours/voxtts) : 317 mots à revoir ;
  darija rare = formes conjuguées ou négatives (كتعارض, الكروسة, كتأخر, كنحلو, بقاتش…) une à cinq fois, et termes du programme (henry, palier,
  échelon, rupture, transitoire, millihenry…) : gardés, à écouter au contrôle des murmures.
- Simulations (frontend/public/media/simulations/physics/dipole-rl-tableau/, contrat cours/dipole_RL_contrat_simulations.md, 3 sous-agents) :
  lampes, bobine (objet|mesure), triangle, circuit-rl (montage|etablissement|rupture), courbe (trace|tangente|pourcent|ub), influence (L|R),
  rupture (descente|diode), droite, energie (barre|calcul), figures (16 ?fig=), bilan (9 blocs), carte. node --check OK ; chaque page testée en
  headless par son agent. verif_sims.js (Playwright node, headless) sur les 48 diapositives : 48 ok, « AUCUN PROBLÈME ».
- À valider (cours) : prédictions ajoutées sur e3, b8, l1 (une par bloc) ; t1 sur circuit-rl?vue=rupture (fig_ed_rupture non utilisée) ;
  lampes : à l'ouverture les DEUX lampes s'éteignent en retard (le courant de la bobine passe aussi par R et L₁ — physique juste, le tableau le dit) ;
  oscilloscope : voie 2 donne −u_b avec la masse au point commun, seule u_R est tracée ; couleurs u_R orange, u_b violet ; question de la carte
  remplacée (« quelle grandeur ne peut jamais sauter ? ») ; énergie : rupture et effet Joule en l7 (pas l8) ; s5 dit que l'analyse dimensionnelle
  tombe rarement ; s8 met en garde (RC : τ augmente avec R ; RL : τ diminue).
- PRÊT POUR LA VOIX : OUI (48 pistes speech_text.mixed + démonstrations) ; réactions à écrire d'abord (items). Reste : audits vidéo (PC),
  réactions (serveur), voix, validation, lecture dans /dev/course-player. Cours suivant : circuit_RLC (exploration à faire).

## circuit_RLC
(routine cloud du 12 nov., cours phys_ch8_circuit_RLC, « Oscillations libres d'un circuit RLC série » ; outils : cours/circuit_RLC_build/ ;
contrat : cours/circuit_RLC_contrat_simulations.md)
- Étape 1 exploration : FAITE → backend/data/curriculum/exploration/circuit_RLC.json (explo.py = explo_a.py + explo_b.py + nationaux.md).
  VIDÉOS NON AUDITÉES : YouTube bloqué depuis le cloud (connexion refusée par le proxy, yt-dlp absent). Appui : les 20 nationaux PC 2016-2025
  (circuit_RLC_build/nationaux.md : RLC dans 17 sessions sur 20, 2,1 pts en moyenne, de 0,5 à 3,5 ; jamais de RLC forcé, de résonance,
  de régime critique ni d'homogénéité demandés), perimetre.json, explorations RC/RL. À compléter par 10 audits vidéo depuis le PC avant validation.
  Ancien matériel : plan de TP database/seed_data/lessons/phys_ch8_l1.json (α = R/2L et R critique hors programme, « périodique avec R presque
  nulle » faux) ; ancienne simu advanced/electricity?variant=rlc (facteur de qualité, R critique) : non reprises.
- Erreurs relevées dans le dépôt (nationaux.md) : 2023 R 1.3/2.3 (q lu 12 µC et 8 µC au lieu de 120 et 40 µC ; bonnes valeurs 0,72 mJ et 0,64 mJ,
  la note RL plus haut sur 2023 R est donc fausse : la grille officielle avait raison) ; 2024 R 2.3 (axe u_R en mV ignoré) ; 2024 N 1.4
  (u_C(t₂) = −4,4 V, pas 4 V : 1,83·10⁻⁹ J) ; 2021 R III.1 courbes inversées ; 2019 N barème faux dans exam.json ; figures mal liées
  (2022 N, 2022 R, 2023 R, 2024 N) ; données absentes d'exam.json (C = 0,22 nF en 2024 N, L = 1 H en 2022 R, R = 90 Ω en 2020 N).
- Étape 5 cadre : chapitres.circuit_RLC ajoutée (cadre_rlc.py : RLC1-RLC8, 21 formules, 20 mots hors cadre). controler_cadre → « cadre : OK »
  (242 « à relire » non bloquants : applications numériques, valeurs de L lues). programme_semestre1 : circuit_RLC → construit.
- COURS CONSTRUIT → backend/data/courses/phys_ch8_circuit_RLC.json (draft, concentration) : 48 diapositives (préfixe lc_), 48 questions,
  23 prédictions, 35 exercices, démonstration sur chaque calcul ; 10 parties (décharge, régimes, équation, solution et T₀, conditions initiales,
  lecture des oscillogrammes, énergie, amortissement, entretien, nationaux 2020 N et 2025 N, bilan + carte) ; compétences C1-C8.
  Build : circuit_RLC_build/ (p1…p4.py par 4 sous-agents, check_part « AUCUNE ERREUR » chacun ; refaire : `python3 circuit_RLC_build/build.py
  --garder-reponses` puis ajouts.py + `blocs.py appliquer`).
- Méthode des blocs : methode_blocs/ajouts/phys_ch8_circuit_RLC.json : 4 séances × 3 blocs × 4 diapositives, 32 rappels, 23 prédictions / 48.
  blocs.py verifier → « cadre : OK », « blocs : OK ». preparer_reponses verifier : seulement réactions et pistes audio manquantes.
- Réactions : items seulement → circuit_RLC_build/items_cours.json (451), items_blocs.json (94), demos_blocs.json (0). À écrire sur le serveur.
- Simulations (frontend/public/media/simulations/physics/circuit-rlc-tableau/, 3 sous-agents) : circuit-lc (montage|bascule|echange), equation,
  entretien, oscillogramme (periodique|pseudo|aperiodique|critique|comparer), solution (cos|phase), periode (T0|influence_L|influence_C),
  energie (echange|amortie), figures (7 ?fig=), bilan (11 blocs), carte. Valeurs : E = 6 V, C = 4 µF, L = 0,1 H, R + r = 20 Ω → T₀ ≈ 4 ms.
  node --check OK ; chaque page testée en headless par son agent ; verif_sims.js (Playwright, 4 lots) sur les 48 diapositives : 48 ok, « AUCUN PROBLÈME ».
- verifier_texte_corpus (copie avec backend/kaggle_tts/texte_parle.py) : 362 mots à revoir : termes du programme (apériodique, pseudo,
  henry, microfarads, microjoules, sinusoïde…) et darija rare une fois chacune (المرجيحة/المرجوحة, كتسخن, شارجي…) : gardés, à écouter au contrôle des murmures.
- PRÊT POUR LA VOIX : OUI (48 pistes speech_text.mixed + démonstrations) ; réactions à écrire d'abord (items). Reste : audits vidéo (PC),
  réactions (serveur), voix, validation, lecture dans /dev/course-player.
- À valider : entretien écrit u_G = k·i (comme les sujets), « résistance négative » jamais dite ; homogénéité de √(LC) en une diapo (p1) ;
  régime critique en une phrase sans formule ; ω₀ une ligne (e8) ; φ en 4 diapositives (c1-c4) alors qu'une seule session le demande (2020 N) ;
  nationaux choisis 2020 N et 2025 N ; couleurs rouge = condensateur, vert = bobine, blanc = énergie totale ; question de la carte remplacée
  (« qui fait osciller, qui amortit ? ») ; « les sujets écrivent aussi u_L » dit en o2 ET en e2 (en enlever un) ; d2 joue la simulation jusqu'au
  retour, ce qui montre déjà « u_C = 0, i maximal » avant la prédiction de d3 ; c4 cite 2020 N (entretien) avant la séance 4 ; formules écrites
  hors liste du brief : du_C/dt(0) = −(2π/T₀)·U_m·sin φ, T₀² = 4π²·L·C, E_e = q²/(2C) ; 2020 N i = 4,8 mA lu (calcul 4,70) ; vue echange de
  circuit-lc en LC idéal (pas de résistor dessiné) ; entretien : k > R + r non montré ; fig_2021R/2022N/2025N recopiées des figures du sujet.
  Cours suivant : transformations_lentes_rapides (chimie, exploration à faire).

## energie_nucleaire
(sous-agent Opus du cours phys_ch5_energie_nucleaire, « Noyaux, masse et énergie » ; outils : cours/energie_nucleaire_build/)
- Démarré. Outils copiés depuis ondes_lumineuses_build (outils.py, build.py, verif_sims.py, prog.py, cadre_ol.py → à adapter).
- Étape 1 exploration : EN COURS (audits vidéo par sous-agents, un à la fois → energie_nucleaire_build/audits/).
- Reprise 11/11 après la limite d'usage. Audits faits : F3zMlBg7xDg Noureddine, iluYXYGxjsI El Omrani (sans sous-titres : images
  seules). Transcriptions déjà téléchargées (scratchpad/transcr) pour : Ng_45GhSl0w + oaaWBeKPMM8 TOP PHYSIQUE (2 parties),
  TYpJZdkU76U Driss DOTCOM, yGeLyz2bHXI Marwane Chargui, y6Kq9jbFKG0 prof Oualid, QhMCnEeG-0c Prof Bazhar (national 2020 N),
  5pPrYuWaND8 prof FIKRI (diagramme d'énergie), S2YFzigj-Gk + 5OkzbgzOu1A Prof Ridouan (cours + série), qUxsDrak79g prof.ghaloumi
  = 10 professeurs. Images en flux (energie_nucleaire_build/images_flux.py, copie de celui de radioactivite).
- Nationaux PC 2016-2025 lus : energie_nucleaire_build/nationaux.md (12 sessions sur 20 ; cas types ; pas de fission ni Aston au national).
- Étape 4 : contrat écrit cours/energie_nucleaire_contrat_simulations.md (balance, liaison, aston, diagramme, reactions, figures,
  bilan, carte) ; premiers sous-agents coupés par la limite (bilan.html/carte.html partiels) → relancés le 11/11.
- Étape 4 simulations : FAITES (sous-agents Opus, testées en headless par eux) : frontend/public/media/simulations/physics/
  energie-nucleaire-tableau/ balance.html (vues helium|noyau|fusion|fission), liaison.html (sens separer|former), aston.html
  (courbe|comparer), diagramme.html (fusion|polonium), reactions.html (fission|chaine|fusion|spontanee), figures.html (19 ?fig=),
  bilan.html, carte.html (+ commun.js, exposants.js, nucleaire.css). Noms = contrat cours/energie_nucleaire_contrat_simulations.md.
- Audit TOP PHYSIQUE (Ng_45GhSl0w + oaaWBeKPMM8) fait. Restent : Driss, Chargui, Oualid, Bazhar, FIKRI, Ridouan, ghaloumi.
- Règles du 11/11 (coordinateur) : disque ≈ 250 Mo → images en flux seulement ; PAS de SSH/VPS → réactions : seulement
  items_cours.json et items_blocs.json/demos_blocs.json dans energie_nucleaire_build/ ; méthode des blocs (seances, rappels,
  prediction) via methode_blocs/blocs.py.
- Audits : 10 professeurs FAITS (audits/ : F3zMlBg7xDg Noureddine, iluYXYGxjsI El Omrani, Ng_45GhSl0w TOP PC (2 parties),
  TYpJZdkU76U Driss, y6Kq9jbFKG0 Oualid, yGeLyz2bHXI Chargui (condensé : disque plein), QhMCnEeG-0c Bazhar (national 2020 N),
  5pPrYuWaND8 FIKRI, S2YFzigj-Gk Ridouan (cours + série), qUxsDrak79g ghaloumi). Aucun filmé en vraie classe (limite notée).
  Prochaine étape : exploration/energie_nucleaire.json (script energie_nucleaire_build/explo.py), puis cadre, puis cours p*.py.
- Étape 1 exploration : FAITE → backend/data/curriculum/exploration/energie_nucleaire.json (explo.py + plan.json ; 10 profs, nationaux,
  6 notions complexes, cas types, pièges, questions d'élèves). Étape 2 ancien cours : aucun (pas d'images, pas d'ancienne simu).
- Étape 5 cadre : FAIT. chapitres.energie_nucleaire (cadre_en.py : relit, remplace la seule clé, réécrit ; EN1-EN8, 16 formules avec
  « dit »). controler_cadre → « cadre : OK » (61 « à relire » non bloquants : applications numériques négatives, Δm de l'exemple).
- Étape 3 cours : ÉCRIT → backend/data/courses/phys_ch5_energie_nucleaire.json (draft, concentration) : 38 diapositives, 36 questions
  à clé (13 prédictions), 8 exercices, démonstration sur chaque calcul, 9 compétences C1-C9 (cadre_ids, dit), bilan + carte (C9).
  Généré par energie_nucleaire_build/build.py (p1..p4.py = contenu). Si on refait : `python build.py --garder-reponses` (garde
  réactions, seances, rappels, prédictions) PUIS `blocs.py appliquer` de nouveau (les 2 énoncés réécrits des prédictions ne sont
  pas dans p*.py). verifier_texte_corpus : darija presque propre (restent الميزان, خفاف, كتكبر… gardés) ; ~260 mots français rares
  = termes du programme (fission, nucléons, deutérium, tritium, méga électron volt, polonium, strontium…).
- Méthode des blocs : FAITE. methode_blocs/ajouts/phys_ch5_energie_nucleaire.json : 4 séances (3+3+3+2 blocs, 11 blocs de 3-4
  diapositives), 31 rappels, 13 prédictions / 38, 2 énoncés réécrits (en_b4_fission_calcul, en_c1_cas_types). blocs.py verifier →
  « cadre : OK », « blocs : OK » (avis : séance 4 = 2 blocs).
- Étape 6 réactions : items seulement (pas de SSH) : energie_nucleaire_build/items_cours.json (230 réactions),
  items_blocs.json (112) + demos_blocs.json (1 démonstration nouvelle). À faire écrire par le coordinateur puis `poser`.
- Étape 7 vérifications : node --check OK (8 pages + commun.js + exposants.js) ; verif_sims.py (Playwright headless, serveur arrêté)
  → AUCUN PROBLÈME sur les 38 diapositives (moments, repères, encre, pas d'erreur JS, rien hors cadre) ; preparer_reponses verifier :
  seuls manquent 38 pistes audio et 230 réactions (+ celles des blocs).
- programme_semestre1.json : energie_nucleaire → « construit », cours phys_ch5_energie_nucleaire (prog.py).
- PRÊT POUR LA VOIX : OUI pour les 38 pistes speech_text.mixed (Bodi) ; les réactions d'abord à écrire (items) puis à dire.
- À valider : voir « Décisions à faire valider » (energie_nucleaire).
- 12 nov. (routine cloud) : état réel vérifié : 38 diapositives, draft ; blocs.py verifier → « cadre : OK », « blocs : OK » ; preparer_reponses
  verifier : seulement voix et réactions manquantes ; node --check OK. Rien à finir côté texte : cours construit, en attente des réactions (items) et de la voix.

## radioactivite
- Sous-agent Opus démarré (10 novembre 2026). Clé radioactivite, cours phys_ch4_radioactivite. Outils : cours/radioactivite_build/
  (outils.py, verif_sims.py copiés d'ondes_lumineuses_build), audits vidéo dans radioactivite_build/audits/.
- Étape 1 exploration : EN COURS. Vidéos choisies (une à la fois, brief radioactivite_build/audit_brief.md) : 19802wryS34 Noureddine
  (FAIT, pas de sous-titres : images seules), iAbkXrexALk TOP PHYSIQUE, 9XYFQ1p7w7A Driss DOTCOM (cours + nationaux), wjhWYaWid3A
  Hassan El Omrani, A3i7AFtVtok Prof othmane, UJzcGpTqf2E Prof Ridouan, 78rQkfYycMs Zakaria Taousse, PPfYofXMSNw prof Oualid,
  aQrb1VHDdqs Amine Laaouani, HqIwcFleDY8 El-Morabite. Audits faits = fichiers présents dans radioactivite_build/audits/.
  Images sans téléchargement (disque C: ≈ 1,5 Go) : radioactivite_build/images_flux.py (ffmpeg lit le flux YouTube).
  Nationaux PC 2016-2025 lus : radioactivite_build/nationaux.md (cas types, écritures, pièges).
- Étape 4 simulations : LANCÉES (5 sous-agents Opus) d'après le contrat cours/radioactivite_contrat_simulations.md ; dossier
  frontend/public/media/simulations/physics/radioactivite-tableau/ (commun.js, exposants.js, radio.css copiés ; noyaux.js écrit :
  notation ᴬ_Z X à la craie). Pages : noyau, segre, desintegration, population, courbe, activite, datation, figures, bilan, carte.
  (11 nov.) Relancées après la coupure : FAITES et testées (rapports reçus) noyau, segre, population, courbe, figures, bilan, carte ;
  desintegration.html et activite.html écrites, datation.html en cours (agent a0710a1f4b91563fa repris).
  Audits faits : 19802wryS34, iAbkXrexALk (+CW3eEUpr7q0), 9XYFQ1p7w7A ; suite une vidéo à la fois.
  (11 nov., nuit) Disque C: tombé à 0 octet pendant ~1 h : tout bloqué. Reprise quand 2,1 Go libres, sur ordre du coordinateur.
  Audits faits : 19802wryS34, iAbkXrexALk (+CW3eEUpr7q0), 9XYFQ1p7w7A, wjhWYaWid3A (aucune n'a de sous-titres arabes : images + commentaires).
  Othmane A3i7AFtVtok arrêté à 26:15 (sous-titres en 429), sans fichier d'audit. Restent : A3i7AFtVtok, UJzcGpTqf2E, 78rQkfYycMs,
  PPfYofXMSNw, aQrb1VHDdqs, HqIwcFleDY8. exploration/radioactivite.json PAS encore écrit.
  Étape 2 : aucun ancien cours de ce chapitre dans backend/data/courses/.
  Plan du cours (prêt, pas encore écrit) : ~50 diapositives, préfixe ra_, 5 séances (4 × 3 blocs + 2 blocs : cas types, puis
  bilan et carte), compétences C1 noyau, C2 diagramme (N,Z), C3 radioactivité + Soddy, C4 α β⁻ β⁺ γ, C5 famille, C6 loi N(t),
  C7 demi-vie, C8 activité, C9 datation ; cadre RA1 à RA10.
  Décisions à faire valider : le chapitre couvre radioactivite + cinetique_nucleaire de perimetre.json (énergie → energie_nucleaire :
  MeV, énergie de liaison, fission, fusion interdits ici) ; t½ (variante t₁/₂) ; e^(−λt) écrit tel quel (le lecteur ne rend pas
  les exposants : manque à signaler) ; pas de neutrino/antineutrino ; α = « noyaux lourds », pas de seuil chiffré (les profs
  écrivent 150, 185, 195 ou 200).
  Ordre de reprise : simus desintegration/activite/datation (rapport agent a0710a1f4b91563fa) → 6 audits → exploration JSON →
  cours JSON + blocs → cadre → programme_semestre1 → items réactions → blocs.py verifier + controler_cadre.
  (11 nov., reprise) desintegration (6 types), activite, datation : testées en headless (moments du contrat tous présents, play_until fin OK, pas d'erreur JS, rendu vérifié sur capture). Étape 4 FAITE.
  Audit A3i7AFtVtok FAIT (images + 120 commentaires ; partie 1 seulement : noyau → α β γ, pas de décroissance).
  Audit UJzcGpTqf2E FAIT (551 lignes de transcription, 46 images, 85 commentaires ; partie 1 : jusqu'à la famille).
  Audit 78rQkfYycMs FAIT (images 54 + 150 commentaires ; décroissance : t½ par l'inverse, τ deux méthodes, datation démontrée).
  Audit PPfYofXMSNw FAIT (1212 lignes, 59 images, 143 commentaires ; outils ln/exp, λt½ = ln2, N₀/2ⁿ, a = −dN/dt, K-Ar).
  Audit aQrb1VHDdqs FAIT (66 images, 150 commentaires ; a = −dN/dt dérivée, deux colonnes courbe/calcul, « héritage incomplet »).
  Audit HqIwcFleDY8 FAIT (images + 36 commentaires ; N, N_d, λ, τ, t½, deux courbes). LES 10 AUDITS SONT FAITS.
  Étape 1 FAITE : backend/data/curriculum/exploration/radioactivite.json (171 Ko ; 15 cas types, 23 pièges, 9 notions complexes,
  21 questions d'élèves, plan de 52 diapositives ra_ en 5 séances 11/12/12/11/6). Décisions nouvelles à valider : positon ⁰₁e (⁰₊₁e admis),
  « photon » toléré (E = hν hors cadre), t½ démontrée par ln(1/2) = −ln2, analogie des 400 élèves qui lancent une pièce,
  prérequis à créer exponentielle_ln_neperien + conversion_durees_secondes, perimetre.json écrit A(t)/t₁/₂ (à harmoniser : a, t½).
  Note : population.html vue proportion montre ≈ 0,083 (= 1 − 2^(−1/8)) ; λ·Δt = 0,087 → dire « environ λ·Δt ».
  Étape 5 (fiche) : chapitres.radioactivite ajouté au cadre (10 capacités RA1-RA10, 23 formules, 31 mots hors cadre, decisions). programme_semestre1 : statut explore, cours phys_ch4_radioactivite.
  (12 nov., routine cloud) Étape 3 cours : ÉCRIT → backend/data/courses/phys_ch4_radioactivite.json (draft, concentration) : 52 diapositives
  (plan de l'exploration, préfixe ra_), 52 questions à clé, 20 prédictions, 3 exercices (2021 N, 2022 N, VF 2025 N), démonstration sur chaque
  calcul ; 6 parties ; compétences C1-C9 (cadre RA1-RA10, avec « dit »). Généré par radioactivite_build/build.py (p1..p4.py = contenu ;
  outils.py contrôle mots, moments, repères, noyaux, équations équilibrées, voix sans chiffre/symbole, mots hors cadre).
  Refaire : `python build.py --garder-reponses` (garde réactions, séances, rappels, prédictions) puis `blocs.py appliquer`.
  Méthode des blocs : methode_blocs/ajouts/phys_ch4_radioactivite.json : 5 séances (3+3+3+3+2 blocs, 14 blocs de 3-4 diapositives), 29 rappels,
  20 prédictions / 52, 12 exercices de blocs écrits (9 avec démonstration) + 2 repris. blocs.py verifier → « cadre : OK », « blocs : OK »
  (avis : séance 5 = 2 blocs). controler_cadre → « cadre : OK » (107 « à relire » non bloquants : applications numériques, Soddy ligne à ligne).
  preparer_reponses verifier : seulement pistes audio et réactions manquantes. verifier_texte_corpus : darija nettoyée (restent تحبسها, نحبسوه) ;
  ~260 mots français rares = termes du programme (désintégration, nucléide, becquerel, positon, polonium, tritium…), gardés.
  Réactions : items seulement → radioactivite_build/items_cours.json (275), items_blocs.json (142), demos_blocs.json (9 démonstrations).
  node --check : OK (scripts des 10 pages + commun.js, exposants.js, noyaux.js). programme_semestre1 : radioactivite → « construit ».
  Navigateur headless (Playwright/Chromium, script node de la routine) sur les 52 diapositives : AUCUN PROBLÈME (chaque moment play_until
  existe et se joue, chaque repère cité existe, encre, pas d'erreur JS, rien hors cadre).
  Exploration : déjà faite (10 audits) ; vidéos non réauditées depuis le cloud.
  PRÊT POUR LA VOIX : OUI (52 pistes speech_text.mixed + démonstrations) ; réactions à écrire d'abord sur le serveur (items) puis à dire.
  À valider (radioactivite, en plus des décisions de l'exploration) : 6 parties (I noyau 11, II désintégrations 12, III loi 12, IV activité
  et datation 11, V cas types 4, VI bilan + carte 2) ; ra_x1 rattachée à C9 ; ra_a7 (droite ln N) rattachée à C6 ; « x % désintégrés :
  N = (1 − x/100)·N₀ » écrit au cahier (pas une formule du cadre) ; bilan et carte rattachés à C1 (comme le témoin).

## transformations_lentes_rapides
(routine cloud du 12 nov., cours phys_ch9_transformations_lentes_rapides, « Transformations lentes et transformations rapides » ; outils :
cours/transformations_lentes_rapides_build/ ; contrat : cours/transformations_lentes_rapides_contrat_simulations.md)
- Étape 1 exploration : FAITE → backend/data/curriculum/exploration/transformations_lentes_rapides.json (explo.py = explo_a.py + explo_b.py).
  VIDÉOS NON AUDITÉES (YouTube bloqué depuis le cloud). Appui : les 20 nationaux PC 2016-2025 (transformations_lentes_rapides_build/nationaux.md :
  le chapitre tombe dans 10 sessions sur 20, 17 questions, 8 pts au total, 0,25 à 1,25 pt ; rien de 2019 à 2022 ; toujours sur l'estérification /
  saponification ; catalyseur H₂SO₄ 6 questions dans 5 sessions ; trempe 1 fois (2017 R) ; demi-équations seulement dans les parties piles),
  perimetre.json (clé cinetique), ancien cours chem_ch1_kinetics_course_v1 (croquis et ancienne simu chimie/labs/cinetique NON repris).
  Erreurs du dépôt relevées (nationaux.md § 4) : 2018 R 1.3 (reflux = montage (c), pas (a)), 2017 R partie 2 (énoncé réécrit, barèmes faux),
  2023 R figure non liée, 2019 R schéma de pile faux, 2024 R potentiel standard (hors programme).
- Cadre : chapitres.transformations_lentes_rapides ajoutée (cadre_tlr.py : TLR1-TLR7, 17 formules, 24 mots hors cadre). perimetre.json NON modifié.
- COURS CONSTRUIT → backend/data/courses/phys_ch9_transformations_lentes_rapides.json (draft, concentration) : 36 diapositives (préfixe tl_),
  36 questions, 16 prédictions, 22 exercices, 19 démonstrations ; 11 parties (ouverture, oxydants/réducteurs, demi-équations, équation,
  rapides/lentes, voir/classer/titrer, température, concentration, trempe/vie/catalyseur, nationaux 2025 N et 2017 R, bilan + carte) ;
  compétences C1-C7. Build : p1…p3.py (3 sous-agents, check_part « AUCUNE ERREUR ») ; refaire : `python3 …/build.py --garder-reponses`
  puis ajouts.py + `blocs.py appliquer`.
- Méthode des blocs : methode_blocs/ajouts/phys_ch9_transformations_lentes_rapides.json : 3 séances × 3 blocs × 4 diapositives, 28 rappels,
  16 prédictions / 36. blocs.py verifier → « cadre : OK », « blocs : OK » (avis : parties ouverture et V sans prédiction, leurs blocs en ont).
  controler_cadre → « cadre : OK » (20 « à relire »). preparer_reponses verifier : seulement réactions et pistes audio manquantes.
  La photo base/ a été refaite après le nettoyage de la darija (rien n'était voisé).
- Réactions : items seulement → items_cours.json (330), items_blocs.json (89), demos_blocs.json (0). À écrire sur le serveur.
- Simulations (frontend/public/media/simulations/chimie/transformations-lentes-rapides-tableau/, 4 sous-agents) : transfert (zinc|couple),
  demi-equation (permanganate|eau_oxygenee|iode|oxalique), equation (zinc_cuivre|eau_oxygenee|permanganate|fer), bechers (comparer|lente|soufre|echelle),
  facteurs (temperature[theta_c]|concentration|trempe|une_variable|vie|catalyseur), courbes (temperature|concentration|catalyseur|lecture), bilan, carte.
  Formules chimiques : petit traducteur par page (⁺ et indices), ⇌ et → dessinés au trait. node --check OK ; chaque page testée en headless
  par son agent ; verif_sims.js (Playwright, 2 lots) sur les 36 diapositives : 36 ok, « AUCUN PROBLÈME » (moments, repères, encre, pas d'erreur JS, rien hors cadre).
- verifier_texte_corpus : ≈ 420 mots à revoir, surtout les termes de chimie absents du corpus (permanganate, diiode, iodure, thiosulfate, manganèse,
  bécher, palier, trempe…) gardés ; darija rare remplacée (قهوي → brun, البيشر → le bécher, كتزرب → كتمشي بالزربة, قطرات → شي نقط, الثلاجة →
  le réfrigérateur…) ; restent des darija rares une fois chacune (بلوكاو, كيبلوكي, السخون, اللاعب…) : à écouter au contrôle des murmures.
- PRÊT POUR LA VOIX : OUI (36 pistes speech_text.mixed + démonstrations) ; réactions à écrire d'abord (items).
- À valider : catalyseur gardé dans ce chapitre (t3, t4 : question de facteur la plus posée au national) ; « chocs efficaces » jamais dit
  (perimetre) alors que le vrai/faux de 2024 N l'emploie ; 10 diapositives d'oxydoréduction alors que le national ne la demande que dans les
  piles ; exemples classiques (iodure, permanganate) pour voir, nationaux sur l'estérification (n1 2025 N, n2 2017 R) ; ⇌ dans les demi-équations,
  → dans les équations ; demi-équations d'oxydation écrites dans le sens de la réaction (Zn ⇌ Zn²⁺ + 2e⁻) en x7-x9 ; identifiant phys_ch9 (chimie
  sous le préfixe phys, ordre 9 du programme) ; durées des simulations pour l'œil (30 min à 20 °C, 10 min à 40 °C, 15 min à 0,2 mol/L,
  catalyseur 10 min contre 40 min ; « autocuiseur ≈ 120 °C ») ; vue soufre sans équation ; r7 (titrage) sur bechers?vue=lente ; bilan et carte
  rattachés à C3 ; définition du facteur cinétique « paramètre qui modifie la vitesse d'évolution (la durée) », sans « même état final ».
- Reste : audits vidéo (PC), réactions (serveur), voix, validation, lecture dans /dev/course-player. Cours suivant : cinetique (exploration à faire).

## cinetique
(routine cloud du 12 nov., après-midi ; cours phys_ch10_cinetique, « Suivi temporel d'une transformation chimique, vitesse de réaction » ;
outils : cours/cinetique_build/ ; contrat : cours/cinetique_contrat_simulations.md)
- Étape 1 exploration : FAITE → backend/data/curriculum/exploration/cinetique.json (explo.py = explo_a.py + explo_b.py). VIDÉOS NON AUDITÉES
  (YouTube bloqué depuis le cloud). Appui : nationaux PC 2016-2025 (cinetique_build/nationaux.md) : suivi temporel dans 10 sessions sur 20
  (2016 R, 2017 N, 2017 R, 2018 R, 2019 R, 2021 N, 2023 N, 2024 N, 2025 N, 2025 R) ; conductimétrie 3 fois (toujours une saponification),
  titrage 2 fois, courbe seule 5 fois ; t₁/₂ dans 9 sessions, vitesse par la tangente dans 5 ; AUCUN national par la pression.
  Erreurs du dépôt : 2024 N corrigés vides, V = 200 mL et t₁ = 60 h absents de exam.json (seulement dans extraction.json) ; 2017 R figure
  qui part vers 0,5 mol au lieu de 0,6 mol.
- Cadre : chapitres.cinetique ajoutée (cadre_cin.py : CIN1-CIN8 provisoires, 11 formules, 10 mots hors cadre). perimetre.json NON modifié.
- COURS CONSTRUIT → backend/data/courses/phys_ch10_cinetique.json (draft, concentration) : 48 diapositives (préfixe ci_), 48 questions,
  31 prédictions, 43 exercices ; 11 parties (ouverture, suivre au cours du temps, avancement et courbe, conductimétrie, pression et choix de
  méthode, vitesse, évolution de la vitesse, t₁/₂, 8 sujets du national, pièges de rédaction, bilan + carte) ; compétences C1-C8.
  Build : p1…p4.py (4 sous-agents, check_part « AUCUNE ERREUR ») ; refaire : `python3 …/cinetique_build/build.py` puis ajouts.py,
  `blocs.py appliquer` (supprimer d'abord methode_blocs/base/phys_ch10_cinetique.json si la voix a changé : rien n'est voisé).
- Méthode des blocs : methode_blocs/ajouts/phys_ch10_cinetique.json : 4 séances × 3 blocs × 4 diapositives, 28 rappels, 31 prédictions / 48.
  blocs.py verifier → « cadre : OK », « blocs : OK ». controler_cadre → « cadre : OK » (120 « à relire » : applications numériques, x_max = C₀·V₀,
  relation de 2016 R x = −6,3·10⁻³·σ + 1,57·10⁻³ donnée par le sujet). preparer_reponses verifier : seulement réactions et pistes audio manquantes.
- Réactions : items seulement → cinetique_build/items_cours.json (519), items_blocs.json (74), demos_blocs.json (1). À écrire sur le serveur.
- verifier_texte_corpus (copie avec backend/kaggle_tts/texte_parle.py, il manque toujours dans outils/cours/voxtts) : ≈ 414 mots à revoir, surtout
  des termes de chimie absents du corpus (diiode, iodure, thiosulfate, titrage, prélèvement, conductimétrie, manomètre, palier…) gardés ; darija
  rare remplacée (كنغطسو → كندخلو, كنعايرو → كنديرو le titrage ديال, كيغمق → كيولي brun, مبطوح → plat, كتمس → touche…) ; restent une fois
  chacune (كتسالى, كيهزو, كيتبدلوش, كنقيسو, سالاتش, كتتأكسد, وكيسولنا…) : à écouter au contrôle des murmures.
- Simulations (frontend/public/media/simulations/chimie/cinetique-tableau/, 5 sous-agents) : suivi (methodes|mesures|prelevement|titrage),
  avancement (tableau|limitant|lien|composition[t]), courbe (points|lecture[t]|palier), conductimetrie (cellule|ions|formule|saponification|droite|
  calcul[t]), pression (ballon|relation|volume), vitesse (pente[t]|definition|tangente[t]|calcul|diminue|concentration|fin|temperature),
  demi-reaction (definition|lecture|piege|comparer), figures (?fig= 10 nationaux), bilan, carte. node --check OK (10 pages + commun.js, exposants.js) ;
  chaque page testée en headless par son agent ; verif_sims.js (Playwright) sur les 48 diapositives : 48 ok, « AUCUN PROBLÈME ».
  Choix des simulations à valider : valeurs ajoutées hors contrat (G = 2,49 mS pour la soude avec k = 10⁻² m, eau 0,01 mS, NaCl 1,26 mS) ;
  saponification : afficheur porté à 0,091 S/m à « final » ; vue volume avec erlenmeyer ; titrage : teinte qui pâlit en racine carrée ;
  pente : triangle Δt = 4 min à 2, 16, 34 min ; figures retouchées d'une demi-division (2016 R, 2018 R, 2024 N, 2025 N) pour que la tangente
  du corrigé touche la courbe ; 2017 R : le cadre du sujet officiel s'arrête aussi à 0,5 mol, dessin selon le texte (départ 0,6 mol).
- PRÊT POUR LA VOIX : OUI (48 pistes speech_text.mixed + démonstrations) ; réactions à écrire d'abord (items).
- Reste : audits vidéo (PC), réactions (serveur), voix, validation, lecture dans /dev/course-player. Cours suivant : transformations_deux_sens
  (exploration à faire).
- À valider : conductimétrie en 6 diapositives (g1-g6) ; pression en 3 courtes (p1-p3, au programme, jamais au national) ; exemple B
  (saponification) annoncé « étudiée plus tard », voix « ion acétate » ; facteurs cinétiques seulement rappelés (v8, h4) ; « chocs efficaces » :
  la grille officielle 2024 N les cite, perimetre.json les exclut → non dits (« les entités se rencontrent moins souvent ») ; t₁/₂ défini par
  x(t₁/₂) = x_f/2 partout (2016 R et 2018 R écrivent x_max/2) ; p4 nomme t₁/₂ avant la séance 3 ; p6 (2024 N) sans la question de vitesse ;
  nationaux aussi dans les exercices de v4, h3, h4 (doublons possibles avec n1-n8) ; n2 et n6 : la tangente avant t₁/₂ (ordre des moments) ;
  valeurs inventées hors contrat pour des exercices (V_E = 16,9 mL à 15 min ; n₀(H₂O₂) = 3,0 et n₀(I⁻) = 4,0 mmol) ; n8 (2017 R) sur le texte du
  sujet (0,6 mol → 0,2 mol, x_f = 0,4 mol) ; identifiant phys_ch10 ; bilan et carte : C1… (voir build).
