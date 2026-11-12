# Contrat des simulations — cours « Dipôle RC » (phys_ch6_dipole_RC)

Écrit le 12 novembre 2026 (routine cloud). Dossier : frontend/public/media/simulations/physics/dipole-rc-tableau/
Déjà présents (copies, ne pas modifier sauf besoin indispensable sans casser les autres pages) : commun.js (window.OndesTableau.Scene :
cadre virtuel 760 × 420, cadre()/local(), image()), exposants.js (10⁻³ et e^{−t/τ} à la craie), rc.css (fond transparent, barre en haut).
Le cours (backend/data/courses/phys_ch6_dipole_RC.json) pilote ces pages par `play_until {moment}` et pointe les repères : les NOMS de vues,
moments, repères et paramètres ci-dessous sont EXACTS. On peut en ajouter, jamais en renommer.

## Lire d'abord (par extraits si gros)
- .agents/skills/simulations-au-tableau/SKILL.md (À SUIVRE À LA LETTRE), docs/design/labos-au-tableau.md s'il existe
- le kit : frontend/public/media/simulations/shared/tableau/tableau.js, tableau.css (et imprimer.js pour bilan/carte)
- modèles (forme seulement, ne pas modifier) : physics/radioactivite-tableau/ (courbe.html : courbe, tangente, lecture, ?courbe= ;
  figures.html : figures à étapes ?fig= ; bilan.html ; carte.html ; population.html : deux vues) et physics/energie-nucleaire-tableau/.

## Règles communes
- Chaque page : `<link>` /media/simulations/shared/tableau/tableau.css + rc.css ; scripts /media/simulations/shared/tableau/tableau.js,
  commun.js, exposants.js, puis le script de la page, puis `<script src="/media/simulations/professor-locate.js" defer></script>`.
- Fond transparent, cadre virtuel 760 × 420, rien de coupé, pas de défilement, barre (bouton + bulle) EN HAUT, bas libre (4.5em).
  UN bouton principal qui cycle (Lancer → Pause → Reprendre → Rejouer) avec data-professor-control ; réglages = poignées glissées
  (Tableau.glisser) quand la fiche en donne.
- `Tableau.protocole({ id, commandes, config, texte, etat, progression, executer })` ; commandes : start, reset, pause, resume,
  set_time {time_s}, set_parameters {…} (schéma avec plages et pas), play_until {moment | time_s} (rejoue depuis 0 si l'instant est passé,
  sinon continue, puis se fige avec « Arrêt sur image : … » dans la bulle). highlight {target} est ajouté par le kit.
- État : simulation_status, ce_qui_se_voit (phrase française qui dit TOUT ce qu'on voit : vue, valeurs avec unités, phase en cours),
  current_variant, time_s, parameters, moments (nom → instant en s DE LA SIMULATION, recalculés quand un paramètre change), derniere_main.
  Le moment `fin` existe partout. Paramètre `vue` (?vue= dans l'URL ET set_parameters) quand la page a des vues.
- Repères `craie.repere(id, x, y, w, h, 'libellé')` pour TOUS les ids listés (noms exacts), et `Tableau.explication({ <vue>: [{ repere, texte }] })`.
- Rendu à la demande ; une scène figée dessine encore ce qui bouge (running || pause). Apostrophe typographique ’ dans les chaînes JS françaises.
- Rendu « réel » (règle 7 du skill) : appareils qui ressemblent aux vrais : générateur (boîtier), interrupteur K à deux positions (1 et 2),
  résistor (rectangle de couleur avec bandes), condensateur chimique bleu peint à côté du symbole à la craie, ampèremètre et voltmètre à
  cadran avec aiguille, lampe qui s'allume (halo), électrons = petites sphères bleues. La craie : fils, lettres, axes, cotes, flèches,
  équations, courbes. Le peint ne change jamais la physique. Légère, une boucle, pas de calcul pixel par pixel.
- Couleurs FIXES : rouge = charge, bleu = décharge, jaune = surlignage seulement.
- Écriture : indices jamais avec « _ » visible : u_C, u_R, C_eq, I₀, Q_m, E_e rendus en indice par le kit (Craie.segments) ;
  exponentielle « e^{−t/τ} » (exposants.js) ; « τ », « µF », « kΩ », « ms ». Virgule décimale française (0,63).
  Les graduations de l'axe des temps sont « rondes » et ne tombent pas sur τ (on ne donne pas la réponse).
- MOTS INTERDITS (dessin, ce_qui_se_voit, explications) : filtre, filtrage, passe-bas, passe-haut, régime sinusoïdal, déphasage, impédance,
  Laplace, séparation des variables, primitive, intégration, résistance de fuite, condensateur réel, ESR, courant de déplacement,
  permittivité, ε, champ électrique, densité d'énergie, « constante d'intégration ».
- Formules écrites seulement (+ applications numériques) : q_A = q ; q_B = −q ; q = C·u_C ; i = dq/dt = C·du_C/dt ; C_eq = C₁ + C₂ ;
  1/C_eq = 1/C₁ + 1/C₂ ; C_eq = C₁·C₂/(C₁ + C₂) ; q = I₀·t ; u_C = (I₀/C)·t ; k = Δu_C/Δt ; C = I₀/k ; u_R = R·i ; u_R + u_C = E ;
  RC·du_C/dt + u_C = E ; du_C/dt + (1/RC)·u_C = E/(RC) ; RC·du_C/dt + u_C = 0 ; RC·dq/dt + q = C·E ; RC·du_R/dt + u_R = 0 ;
  RC·di/dt + i = 0 ; u_C(t) = E(1 − e^{−t/τ}) ; u_C(t) = A + B·e^{−t/τ} ; u_C(t) = E·e^{−t/τ} ; q(t) = C·E(1 − e^{−t/τ}) ;
  i(t) = (E/R)·e^{−t/τ} ; I₀ = E/R ; u_R(t) = E·e^{−t/τ} ; i(t) = −(E/R)·e^{−t/τ} (décharge) ; τ = R·C ; [τ] = [T] ;
  u_C(τ) = 0,63·E ; u_C(τ) = 0,37·E (décharge) ; u_C(5τ) ≈ 0,99·E ; E_e = ½·C·u_C² = q²/(2C) ; E_e = ½·C·E².
- Valeurs (exactes, à utiliser) : courbe de charge par défaut E = 12 V, R = 1 kΩ, C = 220 µF → τ = 0,22 s ; 0,63·E = 7,56 V ;
  0,37·E = 4,44 V ; I₀ = E/R = 12 mA. Nationaux : 2025 N I₀ = 1 µA, pente k = 1 V/s → C = 1 µF ; 2018 N C₁ = 7,5 µF, pente de q = f(u) =
  C_eq = 10 µF → C₂ = 2,5 µF ; 2019 N E = 10 V, Q = 100 µC, τ = 1 ms → C = 10 µF, R = 100 Ω ; 2021 R E = 6 V, i(0) = 50 mA, τ = 12 ms →
  R₁ = 120 Ω, C = 100 µF ; 2021 N E = 12 V, R = 1 kΩ, droite du_C/dt = f(u_C) de (0 ; 1000 V/s) à (12 V ; 0) → a ≈ −83,3 s⁻¹, C = 12 µF ;
  2023 R Q_max = 12 µC, C = 10 µF → E = 1,2 V, E_e = 7,2·10⁻⁶ J.
- Interdits : ne rien modifier hors de dipole-rc-tableau/ (pas frontend/src, pas backend, pas le kit shared/, pas les autres cours) ;
  aucun commit/push/stash/reset/checkout ; aucune voix ; aucun site ; pas de sous-agent.
- Vérification obligatoire : chaque bloc <script> (inline extrait, ou fichier .js) passe `node --check`. Test navigateur : serveur
  statique local sur frontend/public (`python3 -m http.server <port libre 8900-8999> --bind 127.0.0.1` en arrière-plan, arrêté à la fin),
  Playwright node (`require('playwright')`, `chromium.launch()` sans option) : aucune erreur JS, encre sur le canvas, bouton présent,
  `window.__horsCadre` vide ; piloter par postMessage {type:'simulation_control', command, parameters} (voir le modèle ou
  outils/cours/notes/cours/radioactivite_build/verif_sims.py pour la forme) et relire le dernier `simulation_state` : chaque moment de la
  fiche existe et `play_until` s'y fige, chaque repère existe (`Tableau.listeReperes()`), les nombres sont justes. Une capture par vue
  (deviceScaleFactor 1) regardée à l'œil puis effacée.
- Rapport final (court) : fichiers créés, moments réels (nom → s) par vue, repères, paramètres acceptés, écarts avec la fiche, résultats.

## Fiches — GROUPE A (appareils)

### condensateur.html — deux plaques, un isolant ; la charge vue sur les appareils
Vues ?vue= :
- plaques (défaut) : deux armatures métalliques peintes face à face, un isolant (diélectrique) entre elles, puis le symbole à la craie
  (deux traits parallèles) avec « armature A », « armature B », « isolant ». Moments : plaques, isolant, symbole, fin.
- charge : circuit peint et à la craie : générateur E = 6 V, interrupteur K, ampèremètre à cadran, condensateur (armatures A et B),
  voltmètre à cadran aux bornes du condensateur. Moments : k_ouvert (K ouvert : aiguilles à 0), k_ferme (K se ferme : l'aiguille de
  l'ampèremètre saute puis redescend ; celle du voltmètre monte), electrons (des électrons bleus quittent A, font le tour par le
  générateur et s'entassent sur B ; AUCUN ne traverse l'isolant ; texte « aucun électron ne traverse l'isolant »), signes_armatures
  (des « + » apparaissent sur A, des « − » sur B ; « q_A = q ; q_B = −q »), saturation (ampèremètre à 0, voltmètre = 6 V :
  « i = 0 ; u_C = E : le condensateur est chargé »), fin.
Paramètres : vue ; K (0 ouvert | 1 fermé, poignée sur K).
Repères : vue_plaques, vue_charge, armature_A, armature_B, isolant, symbole, generateur, interrupteur, amperemetre, voltmetre,
aiguille_A, aiguille_V, electrons, charge_A, charge_B.

### intensite.html — i est la pente de q(t)
Une courbe q(t) de charge à la craie rouge (axes « t (s) », « q (µC) »), puis :
Moments : courant_constant (d'abord une droite q = I₀·t en pointillé : « si I₀ est constant : I₀ = q/t »), corde (sur la vraie
courbe, une corde entre t et t + Δt : « Δq/Δt »), tangente (Δt rapetisse, la corde devient la tangente : « i = dq/dt »),
pente_nulle (au palier, tangente horizontale : « pente nulle : i = 0 »), decharge_negative (une courbe de décharge en bleu à droite ;
tangente qui descend : « q diminue : i < 0 »), fin.
Paramètres : instant t_s (0 → fin de l'axe, poignée sur le point de tangence).
Repères : axe_t, axe_q, courbe, droite_I0, corde, tangente, point, pente_nulle, courbe_decharge, signe_i.

### generateur-courant.html — charge à courant constant (2025 N)
Moments : carte_generateurs (deux cartes côte à côte : « générateur de tension : E constante, i varie » / « générateur de courant :
I₀ constant, u_C varie »), droite (circuit I₀ + condensateur ; u_C(t) se trace : une droite par l'origine ; « q = I₀·t ;
u_C = (I₀/C)·t »), deux_points (deux points lus sur la droite, coordonnées écrites), pente (« k = Δu_C/Δt = 1 V/s »),
C_deduite (« I₀/C = k donc C = I₀/k = 10⁻⁶/1 = 10⁻⁶ F = 1 µF »), fin.
Paramètres : I0_uA (1 → 10, défaut 1), C_uF (0,5 → 5, défaut 1) : la pente et les nombres suivent.
Repères : generateur_tension, generateur_courant, condensateur, axe_t, axe_u, droite, point_1, point_2, pente, resultat.

### circuit-rc.html — le montage RC, l'acquisition, la charge et la décharge
Montage à la craie (et appareils peints) : générateur E, interrupteur K à deux positions (1 : charge avec E ; 2 : R et C seuls),
résistor R, condensateur C ; à droite un écran d'acquisition (axes « t (s) », « u_C (V) »). Valeurs : E = 12 V, R = 1 kΩ, C = 220 µF.
Vues ?vue= :
- montage (défaut) : moments montage (le circuit se dessine, positions 1 et 2 marquées), fleches (i, puis u_R et u_C en convention
  récepteur : flèches de tension opposées à i), acquisition (« entrée Y » reliée à la borne de la tête de flèche de u_C, « masse » à
  l'autre borne ; texte « tête de flèche → entrée ; l'autre borne → masse »), echelon (petit graphe : tension appliquée 0 puis E à t = 0 :
  « échelon de tension montant » ; puis E puis 0 : « échelon descendant »), fin.
- charge : montage déjà dessiné. Moments : bascule_1 (K passe en position 1, la flèche i s'allume en rouge), courbe_charge (u_C(t) rouge
  s'enregistre : montée rapide puis de plus en plus lente), regime_permanent (palier E : « régime permanent : u_C = E ; i = 0 » ;
  avant : « régime transitoire »), fin.
- decharge : condensateur chargé (u_C = E). Moments : bascule_2 (K passe en position 2 : R et C seuls), courbe_decharge (u_C(t) bleue
  descend de E vers 0), fin.
Paramètres : vue ; K (1 | 2) ; R_ohm (100 → 10000) ; C_uF (10 → 1000) ; E (1 → 12).
Repères : generateur, interrupteur, position_1, position_2, resistance, condensateur, fleche_i, fleche_uR, fleche_uC, entree_Y, masse,
ecran, courbe, echelon, palier_E, regime_transitoire, regime_permanent.

## Fiches — GROUPE B (courbes)

### courbe-charge.html — u_C(t) de la charge : valeurs, tangente, 63 %
Axes « t (s) » (graduations 0,1 s ; de 0 à 1,4 s) et « u_C (V) » (0 → 14), courbe rouge E(1 − e^{−t/τ}) avec E = 12 V, R = 1 kΩ,
C = 220 µF (τ = 0,22 s).
Vues ?vue= :
- tableau (défaut) : moments tableau_valeurs (un tableau à la craie : t = 0 | τ | 5τ ; u_C = 0 | 0,63·E = 7,56 V | 0,99·E ≈ 12 V),
  points (les trois points se placent), courbe (la courbe passe par les points), cinq_tau (repère à 5τ : « à 5τ : régime permanent »), fin.
- R : moments courbe, R_double (R passe à 2 kΩ : une deuxième courbe rouge plus pâle, plus lente ; « τ = R·C double »),
  C_double (on revient à R = 1 kΩ et on double C : même deuxième courbe), fin.
- tangente : moments courbe, asymptote (droite horizontale u_C = E en pointillé), tangente (la tangente à l'origine coupe l'asymptote ;
  verticale vers l'axe : « t = τ »), fin.
- pourcent : moments courbe, ligne_63 (« 0,63 × 12 = 7,56 V » : horizontale jusqu'à la COURBE), projection (verticale vers l'axe des
  temps : « τ ≈ 0,22 s »), fin.
Paramètres : vue ; R_ohm (100 → 10000) ; C_uF (10 → 1000) ; E (1 → 12).
Repères : axe_t, axe_u, courbe, courbe_2, tableau, point_0, point_tau, point_5tau, asymptote, tangente, ligne_63, projection, tau,
cinq_tau.

### quatre-courbes.html — u_C, q, u_R, i pendant la charge
Quatre petits graphes (même axe des temps, mêmes valeurs E = 12 V, R = 1 kΩ, C = 220 µF) : u_C et q montent (rouge), u_R et i
descendent (rouge), chacun avec son expression écrite à côté.
Vues ?vue= :
- q_i : moments q (q(t) = C·E(1 − e^{−t/τ}) ; « Q_m = C·E »), i (i(t) = (E/R)·e^{−t/τ} ; « i(0) = E/R = 12 mA »), fin.
- uC_uR : moments uC, uR (u_R(t) = E·e^{−t/τ}), somme (un instant marqué : « u_C + u_R = E à chaque instant »), fin.
- quatre (défaut) : moments uC, q, uR, i, fin.
- descente : grand graphe i(t) seul. Moments i, tangente_descente (tangente à l'origine qui coupe l'axe des temps à t = τ),
  ligne_37 (« 0,37 × 12 mA = 4,44 mA » horizontale jusqu'à la courbe, puis verticale : « τ »), fin.
Paramètres : vue ; R_ohm ; C_uF.
Repères : graphe_uC, graphe_q, graphe_uR, graphe_i, expression_uC, expression_q, expression_uR, expression_i, somme, tangente,
ligne_37, tau.

### continuite.html — u_C ne saute pas, i change de sens
Deux graphes l'un au-dessus de l'autre : u_C(t) (en haut) et i(t) (en bas), même axe des temps.
Vues ?vue= :
- enchaine (défaut) : moments charge (charge rouge jusqu'au palier E), bascule (trait vertical : « K passe en position 2 »),
  nouvelle_origine (un nouvel axe « t = 0 » à la bascule), uC_continue (u_C reste à E juste après la bascule puis descend en bleu :
  « u_C est continue »), saut_i (i saute de 0 à −E/R puis remonte vers 0 en bleu : « i change de sens : i < 0 »), fin.
- decharge : seulement la décharge (nouvelle origine) : moments decharge (u_C = E·e^{−t/τ} bleue), decharge_37 (« 0,37 × E » →
  τ ; et la tangente à l'origine qui coupe l'axe des temps), fin.
Paramètres : vue ; R_ohm ; C_uF ; E.
Repères : graphe_uC, graphe_i, bascule, nouvelle_origine, uC_continue, saut_i, ligne_37, tangente, tau.

### energie.html — l'énergie du condensateur
Vues ?vue= :
- lampe (défaut) : un condensateur chargé relié à une petite lampe peinte. Moments : decharge_lampe (K se ferme : la lampe s'allume
  puis faiblit ; « le condensateur rend l'énergie stockée »), barre (à côté de la courbe u_C, une barre « E_e » ; « E_e = ½·C·u_C² »),
  carre (u_C double : la barre est ×4 ; « u_C × 2 → E_e × 4 »), fin.
- calcul : C = 220 µF, E = 12 V. Moments : regime_permanent (« E_e = ½·C·E² = ½ × 220·10⁻⁶ × 12² ≈ 1,6·10⁻² J »),
  a_tau (« à t = τ : u_C = 0,63·E ; E_e = ½·C·(0,63·E)² ≈ 0,40 × ½·C·E² »), reste_70 (« l'énergie diminue de 30 % : il en reste 70 % »),
  fin.
Paramètres : vue ; u_C (0 → 12, poignée) ; C_uF.
Repères : lampe, condensateur, barre, courbe, formule, calcul, resultat.

## Fiches — GROUPE C (figures, bilan, carte)

### figures.html?fig=… — figures à la craie qui se construisent ligne par ligne
Chaque figure : un titre court, des lignes qui s'écrivent au rythme des moments ; un repère par moment (même nom) + `figure`.
- fig_prerequis : ohm (« u_R = R·i : convention récepteur »), additivite (« u_R + u_C = E »), puissances (« 47 µF = 47·10⁻⁶ F »),
  derivee (« (e^{−2t})’ = −2·e^{−2t} : séance 3 »), fin.
- fig_unites : bulle (« q = C·u_C » dans une bulle), unites (trois bulles : q en coulomb (C), C en farad (F), u_C en volt (V)),
  sous_multiples (« 1 µF = 10⁻⁶ F ; 1 nF = 10⁻⁹ F ; 1 pF = 10⁻¹² F »), fin.
- fig_boite : la boîte des relations (cadre dans un coin) : ohm (« u_R = R·i »), charge (« q = C·u_C »), intensite (« i = C·du_C/dt »),
  additivite (« u_R + u_C = E »), fin.
- fig_parallele : circuit (deux condensateurs en parallèle, même tension u), charges (« q = q₁ + q₂ »), formule (« C_eq = C₁ + C₂ »),
  interet (« le parallèle augmente la capacité »), fin.
- fig_serie : circuit (deux condensateurs en série, même charge q), tensions (« u = u₁ + u₂ »), formule (« 1/C_eq = 1/C₁ + 1/C₂ »),
  deux (« C_eq = C₁·C₂/(C₁ + C₂) »), interet (« la série diminue la capacité »), fin.
- fig_ed_charge : circuit (petit circuit E, R, C avec flèches), additivite (« u_R + u_C = E »), ohm (« u_R = R·i »), intensite
  (« i = C·du_C/dt »), remplacer (« R·C·du_C/dt + u_C = E »), resultat (cadre autour), fin.
- fig_ed_formes : depart (« RC·du_C/dt + u_C = E »), diviser (« ÷ RC »), forme (« du_C/dt + (1/RC)·u_C = E/(RC) »), lecture
  (« devant la dérivée : τ ; à droite : la valeur finale »), fin.
- fig_ed_q : relations (« u_C = q/C ; i = dq/dt »), remplacer (« R·dq/dt + q/C = E »), multiplier (« × C »), resultat
  (« RC·dq/dt + q = C·E »), fin.
- fig_ed_uR_i : deriver (« du_R/dt + du_C/dt = 0 »), relation (« du_C/dt = i/C = u_R/(RC) »), uR (« RC·du_R/dt + u_R = 0 »),
  i (« RC·di/dt + i = 0 »), fin.
- fig_ed_decharge : circuit (R et C seuls), additivite (« u_R + u_C = 0 »), resultat (« RC·du_C/dt + u_C = 0 »), fin.
- fig_tableau_ed : charge (tableau 4 cases u_C | q | u_R | i, colonne charge, rouge), decharge (colonne décharge, bleue), remarque
  (« u_R et i : second membre nul dans les deux cas »), fin.
- fig_derivee_exp : regle (« (e^{at})’ = a·e^{at} »), exemple (« (e^{−t/τ})’ = −(1/τ)·e^{−t/τ} »), e_zero (« e⁰ = 1 »), limite
  (« e^{−t/τ} → 0 sans jamais s’annuler »), fin.
- fig_resolution : forme (« u_C = A(1 − e^{−t/τ}) »), deriver (« du_C/dt = (A/τ)·e^{−t/τ} »), remplacer
  (« RC·(A/τ)·e^{−t/τ} + A − A·e^{−t/τ} = E »), factoriser (« A·e^{−t/τ}(RC/τ − 1) + A = E »), accolade (« RC/τ − 1 = 0 et A = E »),
  reecrire (« τ = RC ; u_C(t) = E(1 − e^{−t/RC}) » encadré), fin.
- fig_condition_initiale : forme (« u_C = A + B·e^{−αt} »), equation (« l’équation donne A = E et α = 1/RC »), condition
  (« u_C(0) = 0 : A + B = 0 »), resultat (« B = −E »), fin.
- fig_verifier : solution (« u_C = E(1 − e^{−t/RC}) »), derivee (« du_C/dt = (E/RC)·e^{−t/RC} »), remplacer
  (« RC·(E/RC)·e^{−t/RC} + E − E·e^{−t/RC} »), egalite (« = E : vérifiée »), fin.
- fig_dimension : R (« [R] = [U]/[I] »), C (« [C] = [I]·[T]/[U] »), produit (« [R]·[C] = [T] : τ est un temps »), fin.
- fig_decharge_solution : forme (« u_C = A·e^{−t/τ} »), deriver (« du_C/dt = −(A/τ)·e^{−t/τ} »), remplacer
  (« A·e^{−t/τ}(1 − RC/τ) = 0 »), tau (« τ = RC »), condition (« u_C(0) = E : A = E »), resultat (« u_C(t) = E·e^{−t/τ} »), fin.
- fig_r_et_c (2021 R) : donnees (« E = 6 V ; i(0) = 50 mA ; τ = 12 ms »), R (« R₁ = E/i(0) = 6/(50·10⁻³) = 120 Ω »),
  C (« C = τ/R₁ = 12·10⁻³/120 = 10⁻⁴ F = 100 µF »), fin.
- fig_du_dt (2021 N) : equation (« du_C/dt = −(1/RC)·u_C + E/(RC) »), droite (axes u_C (V) et du_C/dt (V/s), droite de (0 ; 1000) à
  (12 ; 0)), pente (« a = (0 − 1000)/(12 − 0) ≈ −83,3 s⁻¹ »), ordonnee (« E/(RC) = 1000 V/s »), resultat
  (« C = −1/(R·a) = 1,2·10⁻⁵ F = 12 µF »), fin.
- fig_q_u (2018 N) : courbe (axes u (V), q (µC), droite par l'origine), pente (« pente = C_eq = 10 µF »), C_eq (« C_eq = C₁ + C₂ »),
  C2 (« C₂ = 10 − 7,5 = 2,5 µF »), fin.
- fig_n1_2019 : enonce (« ED de q ; q = A(1 − e^{−αt}) »), courbe (q(t) avec asymptote Q = 100 µC et tangente à l'origine qui coupe
  l'asymptote à 1 ms), Q (« Q = 100 µC »), tau (« τ = 1 ms »), C (« C = Q/E = 100·10⁻⁶/10 = 10 µF »), R (« R = τ/C = 10⁻³/10⁻⁵ = 100 Ω »),
  fin.
- fig_n2_2021R : enonce (« i + R₁C·di/dt = 0 ; i = I₀·e^{−t/τ} »), courbe (i(t) qui part de 50 mA, tangente à l'origine qui coupe
  l'axe à 12 ms), equation (« I₀·e^{−t/τ}(1 − R₁C/τ) = 0 »), tau (« τ = R₁C »), R1 (« R₁ = E/I₀ = 120 Ω »), C (« C = 100 µF »), fin.
- fig_energie_2023R : donnees (« Q_max = 12 µC ; C = 10 µF »), E (« E = Q_max/C = 1,2 V »), energie
  (« E_e = ½·C·E² = ½ × 10⁻⁵ × 1,2² = 7,2·10⁻⁶ J »), fin.
Paramètre : fig. Repères : figure + un repère par moment (même nom que le moment).

### bilan.html — « Ce qu'il faut retenir » (fiche imprimable, page 2 de l'élève avec ses lacunes)
Modèle : radioactivite-tableau/bilan.html (même protocole, mêmes paramètres de lacunes). Huit blocs, un par compétence :
condensateur (C1 : q = C·u_C ; i = C·du_C/dt ; q_A = q, q_B = −q), associations (C2 : C_eq = C₁ + C₂ ; 1/C_eq = 1/C₁ + 1/C₂ ; C = I₀/k),
echelon (C3 : régime transitoire / permanent, u_C continue, i = 0 au régime permanent), equation (C4 : RC·du_C/dt + u_C = E ; décharge = 0),
solution (C5 : u_C = E(1 − e^{−t/τ}) ; décharge E·e^{−t/τ} ; i = (E/R)·e^{−t/τ}), tau (C6 : τ = R·C, un temps, 5τ),
lecture (C7 : tangente à l'origine, 63 %, 37 %), energie (C8 : E_e = ½·C·u_C²).
Moments : fiche, condensateur, associations, echelon, equation, solution, tau, lecture, energie, lacunes, fin.
Repères : fiche + un par bloc (mêmes noms). Tout tient dans le cadre (rien sous y = 360).

### carte.html — la carte du chapitre (ouverture o1 et fin b2)
Au centre « Dipôle RC » ; branches qui se dessinent : condensateur (q = C·u_C), echelon (échelon de tension), equation (équation
différentielle), solution (u_C(t)), tau (τ = R·C), courbes (lire τ), energie (E_e = ½·C·u_C²), puis national (petit encadré :
« une partie RC dans 11 sujets sur 20 ; lire τ dans 8 »), suite (« après : dipôle RL, puis circuit RLC »).
Moments : centre, condensateur, echelon, equation, solution, tau, courbes, energie, national, suite, fin.
Repères : centre, condensateur, echelon, equation, solution, tau, courbes, energie, national, suite.
