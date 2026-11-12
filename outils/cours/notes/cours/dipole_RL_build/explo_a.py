# -*- coding: utf-8 -*-
"""Partie A de l'exploration dipole_RL : ce qui ne dépend pas de la lecture des nationaux
(notions complexes, analogies, à ne pas dire, hors programme, visuels, cours existant)."""

notions_complexes = [
 {"id": "opposition", "notion": "la bobine s'oppose aux variations de l'intensité (retard à l'établissement)",
  "pourquoi_difficile": "l'élève connaît des dipôles qui réagissent tout de suite (résistance, lampe) ; « s'opposer à une variation » est une idée sur la DÉRIVÉE, pas sur la valeur de i ; il croit qu'une bobine diminue le courant final",
  "prerequis": ["loi_ohm_tension_intensite", "champ_magnetique_bobine"],
  "marches": [
   {"n": 1, "idee": "deux lampes identiques, une en série avec une résistance, l'autre avec une bobine", "vu": "on ferme K : la lampe de la résistance s'allume tout de suite, celle de la bobine en retard", "phrase": "la bobine retarde l'arrivée du courant", "question": "laquelle des deux lampes s'allume en retard ?"},
   {"n": 2, "idee": "à la fin, les deux brillent pareil", "vu": "quelques instants plus tard les deux lampes ont le même éclat", "phrase": "le courant final est le même : la bobine retarde, elle ne bloque pas", "question": "en régime permanent, la bobine change-t-elle l'éclat ?"},
   {"n": 3, "idee": "on ouvre K : le courant ne s'arrête pas d'un coup", "vu": "courbe i(t) qui descend doucement au lieu de tomber à zéro", "phrase": "la bobine s'oppose aussi à la diminution du courant", "question": "i peut-il sauter brusquement de I₀ à 0 dans une bobine ?"},
   {"n": 4, "idee": "le mot : auto-induction", "vu": "écrit au cahier : la bobine s'oppose aux VARIATIONS de i", "phrase": "c'est le phénomène d'auto-induction ; i est continue dans une bobine", "question": "à quoi la bobine s'oppose-t-elle : à i ou à ses variations ?"}],
  "image_mentale": "une charrette lourde (Karossa) : difficile à mettre en marche, difficile à arrêter ; une fois lancée à vitesse constante, elle ne gêne plus",
  "exemple_chiffre": "E = 6 V, R + r = 12 Ω → courant final I₀ = 0,5 A, atteint en retard (≈ 5τ) mais pas réduit par L",
  "piege": "croire que L diminue I₀ (I₀ = E/(R + r) ne contient pas L)",
  "verification": "si on double L, que devient I₀ ? (inchangé) et la durée du régime transitoire ? (doublée)"},
 {"id": "tension_bobine", "notion": "u_b = L·di/dt + r·i : la tension dépend de la VITESSE de variation de i",
  "pourquoi_difficile": "deux termes de natures différentes ; di/dt est une pente lue sur une courbe, pas une valeur ; l'élève confond i et di/dt (i grand ≠ u_b grand)",
  "prerequis": ["derivee_usuelle", "lecture_courbe_tangente"],
  "marches": [
   {"n": 1, "idee": "courant constant : la bobine est une simple résistance r", "vu": "ampèremètre et voltmètre en continu : u_b = r·i, comme un conducteur ohmique", "phrase": "en régime permanent, u_b = r·i", "question": "I = 0,2 A, r = 10 Ω : u_b = ?"},
   {"n": 2, "idee": "bobine idéale (r = 0) parcourue par un courant triangulaire", "vu": "i(t) en dents de scie, u_b(t) en créneaux : palier positif quand i monte, négatif quand i descend", "phrase": "u_b ne suit pas i, elle suit sa pente", "question": "quand i est maximal (sommet du triangle), que vaut la pente ?"},
   {"n": 3, "idee": "le palier est proportionnel à la pente : u = L·di/dt", "vu": "on lit la pente (ΔI/Δt) puis le palier ; leur rapport est le même : L", "phrase": "L est le coefficient qui relie u à di/dt, en henry", "question": "pente 20 A/s, palier 0,4 V : L = ?"},
   {"n": 4, "idee": "bobine réelle : on ajoute r·i", "vu": "le cahier : u_b = L·di/dt + r·i, flèches u_b et i en sens contraires (convention récepteur)", "phrase": "les deux termes s'ajoutent", "question": "en régime permanent, quel terme disparaît ?"}],
  "image_mentale": "le compteur d'un taxi : ce qui fait réagir la bobine n'est pas la vitesse (i), c'est l'accélération (di/dt)",
  "exemple_chiffre": "L = 0,1 H, r = 10 Ω, i = 0,2 A, di/dt = 50 A/s → u_b = 0,1 × 50 + 10 × 0,2 = 5 + 2 = 7 V",
  "piege": "écrire u_b = L·i ou oublier r·i alors que l'énoncé donne r",
  "verification": "bobine idéale, i passe de 0 à 0,3 A en 6 ms à vitesse constante : u_b = ? (L·50 A/s)"},
 {"id": "equation_differentielle", "notion": "établir L·di/dt + (R + r)·i = E puis la mettre sous la forme demandée",
  "pourquoi_difficile": "même démarche que le RC mais l'inconnue est i ; r se cache dans la bobine et s'ajoute à R ; plusieurs formes finales (en i, en u_R, divisée par L ou par R + r)",
  "prerequis": ["lois_kirchhoff", "loi_ohm_tension_intensite"],
  "marches": [
   {"n": 1, "idee": "additivité lue sur le circuit", "vu": "flèches u_R et u_b au-dessus du circuit, E du générateur", "phrase": "u_R + u_b = E", "question": "dans le circuit en série, quelle loi relie les trois tensions ?"},
   {"n": 2, "idee": "remplacer chaque tension", "vu": "u_R = R·i ; u_b = L·di/dt + r·i apparaissent sous chaque flèche", "phrase": "R·i + L·di/dt + r·i = E", "question": "quels termes contiennent i sans dérivée ?"},
   {"n": 3, "idee": "regrouper", "vu": "R·i et r·i se rassemblent en (R + r)·i", "phrase": "L·di/dt + (R + r)·i = E", "question": "quel coefficient est devant i ?"},
   {"n": 4, "idee": "la forme des énoncés", "vu": "on divise par L, ou par R + r : di/dt + ((R + r)/L)·i = E/L", "phrase": "la constante devant la dérivée (après division par R + r) est τ", "question": "en divisant par R + r, que trouve-t-on devant di/dt ?"}],
  "image_mentale": "la même recette que le RC : additivité, remplacer, ranger ; seul l'ingrédient change",
  "exemple_chiffre": "L = 0,2 H, R + r = 20 Ω, E = 10 V → 0,2·di/dt + 20·i = 10 → di/dt + 100·i = 50",
  "piege": "oublier r ; mettre le signe moins devant u_b ; diviser seulement un membre",
  "verification": "établir l'équation en u_R : u_R = R·i donne (L/(R + r))·du_R/dt + u_R = R·E/(R + r)"},
 {"id": "solution_tau", "notion": "vérifier i(t) = A(1 − e^(−t/τ)) et trouver A = E/(R + r), τ = L/(R + r)",
  "pourquoi_difficile": "dériver une exponentielle, remplacer, puis « identifier » : l'élève ne voit pas pourquoi le terme en e^(−t/τ) doit disparaître",
  "prerequis": ["derivee_usuelle", "equation_premier_degre"],
  "marches": [
   {"n": 1, "idee": "la courbe monte puis s'aplatit vers I₀", "vu": "i(t) tracé, asymptote horizontale I₀", "phrase": "la solution a la forme A(1 − e^(−t/τ))", "question": "à t = 0, que vaut A(1 − e⁰) ?"},
   {"n": 2, "idee": "dériver", "vu": "di/dt = (A/τ)·e^(−t/τ)", "phrase": "la dérivée de e^(−t/τ) est −(1/τ)·e^(−t/τ)", "question": "que vaut di/dt à t = 0 ?"},
   {"n": 3, "idee": "remplacer et ranger", "vu": "A·e^(−t/τ)·(L/τ − (R + r)) + (R + r)·A = E", "phrase": "c'est vrai à chaque instant seulement si les deux parenthèses sont bonnes", "question": "quel terme dépend du temps ?"},
   {"n": 4, "idee": "identifier", "vu": "L/τ − (R + r) = 0 → τ = L/(R + r) ; (R + r)·A = E → A = E/(R + r) = I₀", "phrase": "τ et I₀ sortent de l'équation", "question": "L = 0,5 H, R + r = 50 Ω : τ = ?"}],
  "image_mentale": "comme le RC : à t = τ on a fait 63 % du chemin",
  "exemple_chiffre": "E = 12 V, R = 40 Ω, r = 8 Ω, L = 0,24 H → I₀ = 0,25 A, τ = 5 ms, i(τ) = 0,158 A",
  "piege": "τ = L/R en oubliant r ; A = E/R",
  "verification": "même circuit avec L = 0,48 H : I₀ ? (0,25 A) τ ? (10 ms)"},
 {"id": "rupture", "notion": "rupture du courant : i(t) = I₀·e^(−t/τ) et la surtension aux bornes de la bobine",
  "pourquoi_difficile": "le circuit change (le générateur n'est plus là), le second membre devient 0 ; la tension u_b devient négative et peut être grande ; l'élève garde E dans l'équation",
  "prerequis": ["lois_kirchhoff"],
  "marches": [
   {"n": 1, "idee": "on enlève le générateur : le circuit RL se ferme sur lui-même", "vu": "K bascule ; le générateur sort du circuit", "phrase": "u_R + u_b = 0", "question": "après la bascule, quelle est la somme des tensions ?"},
   {"n": 2, "idee": "l'équation sans second membre", "vu": "L·di/dt + (R + r)·i = 0", "phrase": "même équation, second membre nul", "question": "que vaut i quand t devient grand ?"},
   {"n": 3, "idee": "la solution qui descend", "vu": "i = I₀·e^(−t/τ), même τ ; à τ il reste 37 %", "phrase": "i part de I₀ (continuité) et tend vers 0", "question": "i(τ) si I₀ = 0,2 A ?"},
   {"n": 4, "idee": "sans chemin, la bobine crée une grande tension", "vu": "interrupteur ouvert brutalement : étincelle entre les contacts (image)", "phrase": "la bobine s'oppose à l'arrêt brusque : surtension, d'où la diode ou la résistance en parallèle", "question": "pourquoi met-on une diode en parallèle sur la bobine ?"}],
  "image_mentale": "la charrette lancée qu'on lâche : elle continue puis ralentit ; si on la bloque contre un mur, le choc est violent (étincelle)",
  "exemple_chiffre": "I₀ = 0,2 A, τ = 4 ms → i(4 ms) = 0,074 A ; i(20 ms) ≈ 0,0013 A",
  "piege": "écrire L·di/dt + (R + r)·i = E à la rupture ; faire partir i de 0",
  "verification": "à la rupture, que vaut i(0) ? (I₀, la valeur juste avant)"},
 {"id": "lecture_courbes", "notion": "lire τ (tangente, 63 %), I₀, r et L sur un oscillogramme u_R(t) ou u_b(t)",
  "pourquoi_difficile": "on mesure u_R = R·i (image de i), pas i ; il faut diviser par R ; u_b à t = 0 vaut E et en régime permanent vaut r·I₀ ; deux voies, deux sensibilités",
  "prerequis": ["lecture_courbe_tangente", "loi_ohm_tension_intensite"],
  "marches": [
   {"n": 1, "idee": "u_R est l'image de i", "vu": "voie 1 sur R : la courbe a la forme de i", "phrase": "i = u_R/R", "question": "u_R = 4 V, R = 20 Ω : i = ?"},
   {"n": 2, "idee": "la tangente à l'origine coupe l'asymptote à t = τ", "vu": "tangente tracée en couleur, asymptote horizontale, abscisse lue", "phrase": "on lit τ sur l'axe du temps", "question": "où lit-on τ ?"},
   {"n": 3, "idee": "63 % de la valeur finale", "vu": "horizontale à 0,63·U_R max jusqu'à la courbe, puis verticale", "phrase": "autre méthode, même τ", "question": "U_Rmax = 5 V : à quelle hauteur trace-t-on l'horizontale ?"},
   {"n": 4, "idee": "en déduire r et L", "vu": "I₀ = U_Rmax/R → R + r = E/I₀ → r ; puis L = τ·(R + r)", "phrase": "deux lignes de calcul, toujours dans cet ordre", "question": "E = 6 V, I₀ = 0,1 A, R = 50 Ω : r = ?"}],
  "image_mentale": "le reflet dans un miroir : u_R a exactement la forme de i, à l'échelle R près",
  "exemple_chiffre": "E = 6 V, R = 50 Ω, U_Rmax = 5 V → I₀ = 0,1 A, R + r = 60 Ω, r = 10 Ω ; τ lu = 2 ms → L = 0,12 H",
  "piege": "prendre I₀ = E/R (oubli de r) ; lire τ sur la tangente à 63 %",
  "verification": "u_b en régime permanent vaut 1 V et I₀ = 0,1 A : r = ? (10 Ω)"},
 {"id": "energie", "notion": "énergie magnétique E_m = ½·L·i² emmagasinée puis rendue",
  "pourquoi_difficile": "l'énergie dépend de i (pas de u) ; l'élève mélange avec ½·C·u² ; la dissipation par effet Joule à la rupture est invisible",
  "prerequis": ["energie_electrique_joule"],
  "marches": [
   {"n": 1, "idee": "la bobine garde de l'énergie tant que i passe", "vu": "à la rupture, la lampe en parallèle brille encore un instant", "phrase": "cette énergie était dans la bobine", "question": "d'où vient l'énergie de la lampe après l'ouverture ?"},
   {"n": 2, "idee": "la formule (admise)", "vu": "E_m = ½·L·i² au cahier", "phrase": "en joule, avec L en henry et i en ampère", "question": "L = 0,2 H, i = 0,5 A : E_m = ?"},
   {"n": 3, "idee": "au régime permanent", "vu": "E_m = ½·L·I₀²", "phrase": "c'est le maximum pendant l'établissement", "question": "si I₀ double, E_m est multipliée par ?"},
   {"n": 4, "idee": "à la rupture elle devient chaleur", "vu": "les résistances chauffent, E_m descend à 0", "phrase": "effet Joule", "question": "où va l'énergie de la bobine à la rupture ?"}],
  "image_mentale": "la charrette lancée garde son élan (énergie de mouvement) ; ici l'élan, c'est le courant",
  "exemple_chiffre": "L = 0,2 H, I₀ = 0,5 A → E_m = ½ × 0,2 × 0,25 = 0,025 J = 25 mJ",
  "piege": "E_m = ½·L·i (oubli du carré) ; utiliser u_b au lieu de i",
  "verification": "L = 40 mH, i = 0,1 A : E_m ? (2·10⁻⁴ J)"},
]

analogies_validees = [
 {"notion": "auto-induction (inertie du courant)", "image": "une charrette lourde (karossa) : difficile à démarrer, difficile à arrêter, elle ne gêne plus quand elle roule à vitesse constante",
  "limite_de_l_image": "il n'y a pas de masse dans la bobine ; l'image dit seulement que la bobine s'oppose aux variations", "source": "image proposée par Moalim (vidéos non auditées)"},
 {"notion": "u_b dépend de di/dt", "image": "ce qui secoue le passager du taxi, ce n'est pas la vitesse, c'est le coup d'accélérateur ou de frein",
  "limite_de_l_image": "en régime permanent la bobine réelle garde la tension r·i (le « frottement »)", "source": "Moalim"},
 {"notion": "u_R image de i", "image": "une ombre : elle a exactement la forme de l'objet, à l'échelle près",
  "limite_de_l_image": "l'échelle est R : i = u_R/R", "source": "Moalim"},
 {"notion": "même méthode que le RC", "image": "la même recette avec un autre ingrédient : additivité, remplacer, ranger",
  "limite_de_l_image": "dans le RL l'inconnue naturelle est i (continue), dans le RC c'est u_C", "source": "Moalim, d'après renvois de l'exploration dipole_RC"},
]

a_ne_pas_dire = [
 {"terme": "loi de Faraday, loi de Lenz, flux", "motif": "loi de faraday|loi de lenz|flux magn[ée]tique|f\\.?[ée]\\.?m\\.? induite", "dire_plutot": "« on admet que la tension aux bornes de la bobine est u_b = L·di/dt + r·i »"},
 {"terme": "diode de roue libre", "motif": "roue libre", "dire_plutot": "« une diode branchée en parallèle sur la bobine laisse passer le courant à la rupture »"},
 {"terme": "la bobine diminue le courant final", "motif": "bobine (diminue|r[ée]duit) (le )?courant (final|maximal)", "dire_plutot": "« la bobine retarde l'établissement du courant ; I₀ = E/(R + r) ne dépend pas de L »"},
 {"terme": "τ = L/R quand la bobine a une résistance", "motif": "τ ?= ?L ?/ ?R\\b(?! ?\\+)", "dire_plutot": "« τ = L/(R + r), la résistance totale du circuit »"},
 {"terme": "u_b = L·i", "motif": "u_?b? ?= ?L ?· ?i\\b", "dire_plutot": "« u_b = L·di/dt + r·i »"},
 {"terme": "second ordre", "motif": "second ordre|deuxi[èe]me ordre", "dire_plutot": "« le RL est du premier ordre ; le second ordre arrive avec le RLC »"},
]

exclus_hors_programme = [
 {"element": "flux magnétique, lois de Faraday et de Lenz, f.é.m. induite", "raison": "perimetre.json dipole_RL.termes_hors_programme"},
 {"element": "inductance mutuelle, transformateur", "raison": "perimetre.json"},
 {"element": "calcul de L par la géométrie (μ₀, solénoïde)", "raison": "perimetre.json ; L est toujours une donnée ou se déduit de τ"},
 {"element": "régime sinusoïdal, réactance, déphasage", "raison": "perimetre.json"},
 {"element": "le mot « roue libre »", "raison": "perimetre.json (motif) ; la diode en parallèle est seulement décrite si un énoncé la met"},
 {"element": "courbe ln i = f(t)", "raison": "aucun national 2016-2025 ; même décision que le RC"},
]

cours_existant = {
 "fichier": "aucun cours RL dans backend/data/courses ; database/seed_data/lessons/phys_ch7_l1.json (« Laboratoire guidé — Dipôle RL » : objectifs, parcours observer → prédire → manipuler → mesurer → expliquer, trois cartes : auto-induction uL = L di/dt, établissement 63 % à τ = L/R, énergie ½Li² ; pas de diapositives, pas d'images)",
 "a_garder": ["l'ordre observer → prédire → mesurer → expliquer", "la question guide : comment une bobine s'oppose-t-elle aux variations du courant ?", "faire prévoir l'effet de L puis de R sur τ et sur I₀"],
 "images": [],
 "a_corriger": ["τ = L/R écrit sans r : le cours écrit τ = L/(R + r) (R total)", "« uL » : le cours écrit u_b ou u_L comme l'énoncé"],
 "a_ajouter": ["u_b = L·di/dt + r·i (convention récepteur)", "équation différentielle, solution, rupture, lecture d'oscillogramme, r et L déduits", "cas types des nationaux"],
 "a_retirer": [],
 "simulations_a_recreer": [{"ancienne": "frontend/public/media/simulations/physics/advanced/electricity (CircuitLab, mode RL)", "montrait": "établissement du courant dans un RL, curseurs L et R", "devient": "v_circuit_rl et v_influence (craie, moments nommés)"}],
}

visuels = {
 "_note": "Simulations à la craie à créer dans frontend/public/media/simulations/physics/dipole-rl-tableau/ (kit shared/tableau, skill simulations-au-tableau, comme dipole-rc-tableau) ; moments nommés pilotés par la voix (play_until), highlight, ce_qui_se_voit. Code couleur : vert = établissement, bleu = rupture (rouge/bleu déjà pris par charge/décharge au RC ; à valider), jaune = surlignage.",
 "simulations": [
  {"id": "v_carte", "fichier": "carte.html", "ce_que_ca_montre": "carte du chapitre puis carte finale (bobine → u_b → échelon → ED → solution → τ → rupture → courbes → énergie)", "capacite": "toutes", "moments": ["centre", "branches", "complete"], "poignees": []},
  {"id": "v_lampes", "fichier": "lampes.html", "ce_que_ca_montre": "deux branches en parallèle (lampe + résistance, lampe + bobine), K ; la lampe de la bobine s'allume en retard puis égale l'autre ; à l'ouverture elle s'éteint en retard", "capacite": "RL2", "moments": ["k_ouvert", "k_ferme", "retard", "egal", "ouverture"], "poignees": ["K", "L"]},
  {"id": "v_bobine", "fichier": "bobine.html", "ce_que_ca_montre": "une bobine réelle (fil de cuivre enroulé, noyau de fer amovible), son symbole, L et r, ohmmètre qui lit r", "capacite": "RL1", "moments": ["objet", "symbole", "noyau", "ohmmetre", "convention"], "poignees": ["noyau"]},
  {"id": "v_triangle", "fichier": "triangle.html", "ce_que_ca_montre": "GBF courant triangulaire dans une bobine idéale : i(t) en dents de scie, u_b(t) en créneaux, pente lue, rapport u/pente = L", "capacite": "RL1", "moments": ["courant", "pente_montee", "palier_haut", "pente_descente", "palier_bas", "rapport"], "poignees": ["fréquence", "L"]},
  {"id": "v_circuit_rl", "fichier": "circuit-rl.html", "ce_que_ca_montre": "montage E, K deux positions, R, bobine (L, r), oscilloscope voie 1 = u_R (image de i), voie 2 = u_b ; flèches u_R, u_b, i ; établissement puis rupture", "capacite": "RL3, RL4", "moments": ["montage", "fleches", "etablissement", "permanent", "rupture", "oscillo"], "poignees": ["K"]},
  {"id": "v_courbe", "fichier": "courbe.html", "ce_que_ca_montre": "i(t) qui se trace, asymptote I₀, tangente à l'origine, 63 %, 5τ ; puis u_b(t) qui descend de E à r·I₀", "capacite": "RL5, RL7", "moments": ["trace", "asymptote", "tangente", "pourcent", "cinq_tau", "ub"], "poignees": ["t"]},
  {"id": "v_influence", "fichier": "influence.html", "ce_que_ca_montre": "trois courbes i(t) pour trois L (même I₀) puis trois R (I₀ et τ changent)", "capacite": "RL6", "moments": ["L_double", "R_double", "comparer"], "poignees": ["L", "R"]},
  {"id": "v_rupture", "fichier": "rupture.html", "ce_que_ca_montre": "K bascule : i descend de I₀ (continuité), 37 % à τ ; interrupteur simple ouvert : étincelle ; diode en parallèle qui donne un chemin", "capacite": "RL2, RL5", "moments": ["bascule", "descente", "trente_sept", "etincelle", "diode"], "poignees": ["K"]},
  {"id": "v_droite", "fichier": "droite.html", "ce_que_ca_montre": "la courbe di/dt = f(i) (ou u_b = f(di/dt)) : une droite ; ordonnée à l'origine E/L, pente −1/τ, intersection avec l'axe = I₀", "capacite": "RL7", "moments": ["points", "droite", "ordonnee", "pente", "abscisse"], "poignees": []},
  {"id": "v_energie", "fichier": "energie.html", "ce_que_ca_montre": "barre E_m = ½·L·i² qui monte avec i, puis se vide en chaleur à la rupture", "capacite": "RL8", "moments": ["monte", "maximum", "vide", "calcul"], "poignees": ["i"]},
  {"id": "v_figures", "fichier": "figures.html", "ce_que_ca_montre": "figures fixes des nationaux redessinées (?fig=)", "capacite": "RL7", "moments": [], "poignees": []},
  {"id": "v_bilan", "fichier": "bilan.html", "ce_que_ca_montre": "fiche « Ce qu'il faut retenir » (blocs)", "capacite": "toutes", "moments": [], "poignees": []},
 ],
 "manips_labo_3d": "aucune manip RL dans labo-3d (seulement rc) : non créée ce passage ; à proposer plus tard (mesurer τ pour deux L).",
}

regles_des_simulations = ("Aucune ancienne simulation n'est reprise : physics/advanced/electricity (CircuitLab) est un ancien labo, à recréer à la craie. "
  "Chaque simulation : craie sur tableau transparent, moments nommés, play_until, highlight, ce_qui_se_voit ; rien hors cadre (pas de flux, pas de Lenz) ; "
  "écriture des formules comme au cahier (u_b, L·di/dt, τ = L/(R + r)) ; unités et nombres lisibles ; même kit et même style que dipole-rc-tableau.")
