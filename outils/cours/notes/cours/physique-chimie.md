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
- Étapes 3-4 (même passage) : cours p1..p4.py et 12 pages de simulation confiés à 7 sous-agents (voir suite ci-dessous).

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
