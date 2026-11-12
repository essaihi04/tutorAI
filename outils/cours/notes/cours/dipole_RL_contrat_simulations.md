# Contrat des simulations — cours « Dipôle RL » (phys_ch7_dipole_RL)

Écrit le 12 novembre 2026 (routine cloud). Dossier : frontend/public/media/simulations/physics/dipole-rl-tableau/
Déjà présents (copies de dipole-rc-tableau, ne pas modifier sauf besoin indispensable sans casser les autres pages) : commun.js
(window.OndesTableau.Scene : cadre virtuel 760 × 420, cadre()/local(), image()), exposants.js (10⁻³ et e^{−t/τ} à la craie), rl.css.
Le cours (backend/data/courses/phys_ch7_dipole_RL.json) pilote ces pages par `play_until {moment}` et pointe les repères : les NOMS de vues,
moments, repères et paramètres ci-dessous sont EXACTS (copie : tables MOMENTS / REPERES de outils/cours/notes/cours/dipole_RL_build/outils.py).
On peut en ajouter, jamais en renommer.

## Lire d'abord (par extraits si gros)
- .agents/skills/simulations-au-tableau/SKILL.md (À SUIVRE À LA LETTRE)
- le kit : frontend/public/media/simulations/shared/tableau/tableau.js, tableau.css (et imprimer.js pour bilan/carte)
- MODÈLES DIRECTS (même chapitre d'électricité, même style ; forme seulement, ne pas modifier) : physics/dipole-rc-tableau/
  (circuit-rc.html : montage à deux positions, flèches, oscilloscope ; courbe-charge.html : courbe, tangente, 63 % ; continuite.html ;
  energie.html ; figures.html : figures à étapes ?fig= ; bilan.html ; carte.html). Partir d'une copie de la page RC la plus proche.

## Règles communes
- Chaque page : `<link>` /media/simulations/shared/tableau/tableau.css + rl.css ; scripts /media/simulations/shared/tableau/tableau.js,
  commun.js, exposants.js, puis le script de la page, puis `<script src="/media/simulations/professor-locate.js" defer></script>`.
- Fond transparent, cadre virtuel 760 × 420, rien de coupé, pas de défilement, barre (bouton + bulle) EN HAUT, bas libre (4.5em).
  UN bouton principal qui cycle (Lancer → Pause → Reprendre → Rejouer) avec data-professor-control ; réglages = poignées glissées.
- `Tableau.protocole({ id, commandes, config, texte, etat, progression, executer })` ; commandes : start, reset, pause, resume,
  set_time {time_s}, set_parameters {…}, play_until {moment | time_s} (rejoue depuis 0 si l'instant est passé, sinon continue, puis se fige
  avec « Arrêt sur image : … »). highlight {target} est ajouté par le kit.
- État : simulation_status, ce_qui_se_voit (phrase française qui dit TOUT ce qu'on voit, valeurs avec unités), current_variant, time_s,
  parameters, moments (nom → instant en s DE LA SIMULATION), derniere_main. Le moment `fin` existe partout. Paramètre `vue` (?vue= dans
  l'URL ET set_parameters) quand la page a des vues.
- Repères `craie.repere(id, x, y, w, h, 'libellé')` pour TOUS les ids listés (noms exacts), et `Tableau.explication({ <vue>: [{ repere, texte }] })`.
- Rendu à la demande ; une scène figée dessine encore ce qui bouge. Apostrophe typographique ’ dans les chaînes JS françaises.
- Rendu « réel » : générateur (boîtier), interrupteur K à deux positions (1 et 2), résistor (rectangle à bandes), BOBINE peinte (fil de
  cuivre enroulé en spires orangées sur un mandrin, noyau de fer gris amovible) à côté de son symbole à la craie (créneaux arrondis + L, r),
  lampes à incandescence avec halo, oscilloscope (écran vert sombre, deux voies), ohmmètre à afficheur, GBF (boîtier), diode (symbole
  triangle-barre + petit composant noir à bague). La craie : fils, lettres, axes, cotes, flèches, équations, courbes.
- Couleurs FIXES : vert = établissement du courant, bleu = rupture, jaune = surlignage seulement.
- Écriture : indices jamais avec « _ » visible : u_b, u_R, I₀, E_m, R₁ rendus en indice par le kit ; exponentielle « e^{−t/τ} » ;
  « τ », « mH », « Ω », « ms », « mA ». Virgule décimale française (0,63). Graduations rondes qui ne tombent pas sur τ.
- MOTS INTERDITS (dessin, ce_qui_se_voit, explications) : loi de Faraday, loi de Lenz, flux magnétique, force électromotrice induite,
  inductance mutuelle, transformateur, perméabilité, μ₀, réactance, déphasage, régime sinusoïdal, roue libre, second ordre.
- Formules écrites seulement (+ applications numériques) : u_b = L·di/dt + r·i ; u_b = L·di/dt ; u_b = r·I₀ ; u_R = R·i ; i = u_R/R ;
  u_R + u_b = E ; u_R + u_b = 0 ; L·di/dt + (R + r)·i = E ; di/dt + ((R + r)/L)·i = E/L ; di/dt + (1/τ)·i = E/L ;
  du_R/dt + ((R + r)/L)·u_R = R·E/L ; L·di/dt + (R + r)·i = 0 ; i(t) = I₀(1 − e^{−t/τ}) ; i(t) = A(1 − e^{−t/τ}) ; i(t) = A + B·e^{−t/τ} ;
  i(t) = I₀·e^{−t/τ} ; u_b(t) = E·e^{−t/τ} ; I₀ = E/(R + r) ; U_R = R·E/(R + r) ; τ = L/(R + r) ; τ = L/R (bobine idéale) ;
  [τ] = [L]/[R] = [T] ; i(τ) = 0,63·I₀ ; i(τ) = 0,37·I₀ (rupture) ; L = τ·(R + r) ; r = E/I₀ − R ; r = u_b/I₀ ; E_m = ½·L·i² ; E_m = ½·L·I₀².
- Valeurs par défaut (exactes) : E = 6 V, R = 50 Ω, r = 10 Ω, L = 0,12 H → I₀ = 0,1 A = 100 mA, τ = 2 ms, U_R max = 5 V,
  0,63·I₀ = 63 mA (u_R = 3,15 V), 0,37·I₀ = 37 mA, u_b(0) = 6 V, u_b(∞) = r·I₀ = 1 V, E_m max = ½ × 0,12 × 0,1² = 6·10⁻⁴ J.
- Interdits : ne rien modifier hors de dipole-rl-tableau/ (pas frontend/src, pas backend, pas le kit shared/, pas les autres cours) ;
  aucun commit/push/stash/reset/checkout ; aucune voix ; aucun site ; pas de sous-agent.
- Vérification obligatoire : `node --check` sur chaque bloc <script> (extrait) et chaque .js. Test navigateur : serveur statique sur
  frontend/public (`python3 -m http.server <port libre, donné dans ta mission> --bind 127.0.0.1` en arrière-plan, arrêté à la fin), Playwright
  node (`require('playwright')`, `chromium.launch()`) : aucune erreur JS, encre sur le canvas, bouton présent, `window.__horsCadre` vide ;
  piloter par postMessage {type:'simulation_control', command, parameters} (forme : outils/cours/notes/cours/dipole_RL_build/verif_sims.js)
  et relire le dernier `simulation_state` : chaque moment existe et `play_until` s'y fige, chaque repère existe (`Tableau.listeReperes()`),
  les nombres sont justes. Une capture par vue (deviceScaleFactor 1) regardée puis effacée.

## Les pages

### lampes.html (pas de vue) — RL2
Deux branches en parallèle sur le générateur E et l'interrupteur K : branche 1 = lampe L₁ + résistance R ; branche 2 = lampe L₂ + bobine
(L, r, avec r = R). On ferme K : L₁ s'allume aussitôt, L₂ monte doucement (éclat ∝ i²) ; les deux finissent pareilles ; à l'ouverture
L₂ s'éteint en retard (le courant de la bobine passe un instant). Poignée : noyau de fer (L grande ou petite → retard plus ou moins long).
Moments : k_ouvert, k_ferme, retard, egal, ouverture, fin. Repères : generateur interrupteur resistance bobine lampe_R lampe_L.

### bobine.html (vues objet | mesure) — RL1
objet : la bobine peinte (spires de cuivre, mandrin), puis le noyau de fer qu'on enfonce (« L augmente »), puis le symbole à la craie
avec L (henry, H) et r. Moments : objet, noyau, symbole, fin.
mesure : un ohmmètre branché aux bornes lit r = 10 Ω ; puis la convention récepteur : flèche i entrant, flèche u_b en sens contraire,
« u_b = L·di/dt + r·i » écrit sous la bobine. Moments : ohmmetre, convention, fin.
Repères (toutes vues) : vue_objet vue_mesure fil noyau symbole L r ohmmetre fleche_i fleche_ub.

### triangle.html (pas de vue) — RL1
GBF (boîtier) + bobine de résistance négligeable (L = 20 mH). Deux graphes l'un sous l'autre, même axe du temps : i(t) en dents de scie
(de 0 à 0,2 A en 10 ms, puis retour en 10 ms ; période 20 ms) ; u_b(t) en créneaux (+0,4 V pendant la montée, −0,4 V pendant la descente).
On lit la pente (20 A/s) et le palier (0,4 V) ; leur rapport = 0,02 H = L. Poignée : L (10 à 40 mH ; palier = L × 20).
Moments : courant (i se trace), pente_montee (triangle de pente coté), palier_haut, pente_descente, palier_bas, rapport (« u_b/(di/dt) = L »
écrit), fin. Repères : gbf bobine graphe_i graphe_u pente palier rapport.

### circuit-rl.html (vues montage | etablissement | rupture) — RL3, RL4
Montage : E, K à deux positions (1 : générateur dans la maille ; 2 : maille R + bobine sans générateur), R, bobine (L, r), flèches i, u_R, u_b ;
oscilloscope : voie 1 aux bornes de R (« u_R = R·i, image de i »), voie 2 aux bornes de la bobine, masse au point commun.
montage : moments montage, fleches, oscillo, fin.
etablissement : K en 1 ; sur l'écran u_R(t) monte (vert) de 0 vers 5 V ; régime transitoire puis permanent marqués.
Moments : fermeture, courbe_i, permanent, fin.
rupture : K en 2 ; u_R part de 5 V et descend (bleu) vers 0. Moments : bascule, courbe_rupture, fin.
Repères : generateur interrupteur position_1 position_2 resistance bobine fleche_i fleche_uR fleche_ub voie_1 voie_2 masse ecran courbe
regime_transitoire regime_permanent.

### courbe.html (vues trace | tangente | pourcent | ub) — RL5, RL7, RL3
Graphe i(t) en mA (0 à 120 mA), t en ms (0 à 12 ms), valeurs par défaut (I₀ = 100 mA, τ = 2 ms).
trace : la courbe se trace, asymptote I₀ = 100 mA, repère à 5τ = 10 ms (« i ≈ 0,99·I₀ »). Moments : trace, asymptote, cinq_tau, fin.
tangente : courbe, asymptote, tangente à l'origine qui coupe l'asymptote à t = τ (abscisse lue). Moments : courbe, asymptote, tangente, fin.
pourcent : courbe, horizontale 0,63·I₀ = 63 mA jusqu'à la COURBE, projection sur l'axe du temps. Moments : courbe, ligne_63, projection, fin.
ub : graphe u_b(t) (0 à 7 V) : point E = 6 V à t = 0, descente, palier r·I₀ = 1 V. Moments : ub_debut, ub_descente, ub_fin, fin.
Repères : axe_t axe_i courbe asymptote tangente ligne_63 projection tau cinq_tau courbe_ub point_E palier_rI0.

### influence.html (vues L | R) — RL6
L : courbe de référence (L = 0,12 H) puis courbe_L (L = 0,24 H) : même palier 100 mA, τ = 4 ms. Moments : courbe, L_double, fin.
R : référence puis courbe_R (R = 110 Ω, R + r = 120 Ω : I₀ = 50 mA, τ = 1 ms) ; comparer : les deux τ et les deux paliers marqués.
Moments : courbe, R_double, comparer, fin. Paramètres : L (0,06..0,48), R (20..200). Repères : axe_t axe_i courbe courbe_L courbe_R palier tau.

### rupture.html (vues descente | diode) — RL2, RL5
descente : K bascule à t = 0 ; i part de I₀ = 100 mA (continuité, point marqué) et descend (bleu) ; 0,37·I₀ = 37 mA lu à τ = 2 ms ;
tangente à l'origine qui coupe l'axe du temps à τ. Moments : bascule, descente, ligne_37, tangente, fin.
diode : interrupteur simple qu'on ouvre : étincelle peinte entre les contacts (« surtension ») ; puis on ajoute une diode et R₁ = 1 kΩ en
parallèle sur la bobine (2025 R : I₀ = 0,1 A) : le courant passe dans la diode, u_b = −R₁·I₀ = −100 V écrit avec la flèche u_b.
Moments : etincelle, diode, surtension, fin. Repères : axe_t axe_i courbe tangente ligne_37 tau interrupteur etincelle diode R1 fleche_ub.

### droite.html (pas de vue) — RL7 (2024 N)
Axes : i en mA (0 à 7), di/dt en 10³ A/s (0 à 3,5). Points mesurés qui apparaissent, puis la droite de (0 ; 3·10³ A/s) à (6 mA ; 0) ;
ordonnée à l'origine E/L = 3·10³ A/s (E = 6 V → L = 2 mH) ; pente −5·10⁵ s⁻¹ = −1/τ (τ = 2 µs) ; abscisse I₀ = 6 mA.
Moments : points, droite, ordonnee, pente, abscisse, fin. Repères : axe_i axe_didt points droite ordonnee pente abscisse.

### energie.html (vues barre | calcul) — RL8
barre : bobine + barre « E_m » qui monte avec i (∝ i²) pendant l'établissement, maximum ½·L·I₀² = 6·10⁻⁴ J, puis se vide à la rupture
pendant que la résistance rougit (chaleur, effet Joule). Moments : monte, maximum, vide, fin.
calcul : L = 0,2 H, I₀ = 0,5 A écrits, « E_m = ½·L·I₀² = ½ × 0,2 × 0,5² = 0,025 J ». Moments : donnees, calcul, resultat, fin.
Repères : bobine barre courbe formule calcul resultat resistance.

### figures.html?fig=… — figures à étapes (comme dipole-rc-tableau/figures.html)
Un repère `figure` + un repère par étape (même nom que le moment). Moments (dans l'ordre, + fin) :
- fig_prerequis : ohm (u_R = R·i), additivite (u_R + u_b = E), derivee ((e^{−t/τ})′ = −(1/τ)·e^{−t/τ})
- fig_segments : courbe i(t) en deux segments (0 → 0,2 A en 10 ms puis palier), pente_1 (20 A/s), calcul_1 (u_b = 0,1 × 20 = 2 V, L = 0,1 H, r = 0),
  pente_2 (0), calcul_2 (u_b = 0)
- fig_2020N : enonce (R = 90 Ω, bobine (L, r)), courbes (i(t) vers 100 mA et u_L(t) de 10 V vers 1 V), lecture (u_L = 1 V, I₀ = 0,1 A), calcul (r = u_L/I₀ = 10 Ω)
- fig_ed : circuit, additivite (u_R + u_b = E), remplacer (R·i + L·di/dt + r·i = E), regrouper, resultat (L·di/dt + (R + r)·i = E)
- fig_ed_formes : depart, diviser_L (di/dt + ((R + r)/L)·i = E/L), diviser_R ((L/(R + r))·di/dt + i = E/(R + r)), lecture (τ et I₀ encadrés)
- fig_ed_uR : relations (i = u_R/R ; di/dt = (1/R)·du_R/dt), remplacer, multiplier (× R/L), resultat (du_R/dt + ((R + r)/L)·u_R = R·E/L)
- fig_2021R : enonce (E = 6 V, R₂ = 95 Ω), additivite, remplacer, resultat (di/dt + (1/τ)·i = E/L), tau (τ = L/(R₂ + r))
- fig_2019R : enonce (E = 10 V, R = 40 Ω), courbes (deux courbes, l'une part de 0, l'autre de 10 V), origine (u_R(0) = 0), permanent (U_R = 8 V),
  r (r = R·(E/U_R − 1) = 10 Ω)
- fig_derivee_exp : regle, exemple, e_zero (e⁰ = 1), limite (e^{−t/τ} → 0)
- fig_resolution : forme (i = A(1 − e^{−t/τ})), deriver, remplacer, factoriser, accolade (L/τ − (R + r) = 0 ; (R + r)·A = E), resultat (τ = L/(R + r) ; A = I₀)
- fig_dimension : L ([L] = [U]·[T]/[I]), R ([R] = [U]/[I]), quotient ([τ] = [T])
- fig_ed_rupture : circuit (K en 2), additivite (u_R + u_b = 0), resultat (L·di/dt + (R + r)·i = 0)
- fig_2025R : enonce (E = 10 V, R = 100 Ω, bobine idéale, diode + R₁ = 1 kΩ), continuite (i(0⁺) = I₀ = 0,1 A), uR1 (u_R1 = 100 V),
  maille (u_b + u_R1 = 0), resultat (u_b = −100 V)
- fig_r_L : donnees (E = 6 V, R = 50 Ω, U_R max = 5 V, τ = 2 ms), I0 (I₀ = 0,1 A), r (r = 10 Ω), L (L = 0,12 H)
- fig_2022R : enonce (E = 10 V, R = 490 Ω), courbe (u_R vers U₀ = 9,8 V, tangente, τ = 1 ms), I0 (0,02 A), r (10 Ω), L (L₀ = 0,5 H),
  courbes (quatre courbes C₁…C₄ : C₂ même palier et τ = 2 ms)
- fig_2024N : enonce (E = 6 V, R₁, bobine (L, r)), droite (di/dt = f(i)), ordonnee (3·10³ A/s), L (L = E/3·10³ = 2 mH), pente (−5·10⁵ s⁻¹), tau (τ = 2 µs)

### bilan.html — fiche « Ce qu'il faut retenir » (comme dipole-rc-tableau/bilan.html, imprimable)
Blocs (moments et repères du même nom) : fiche, bobine, tension, echelon, equation, solution, tau, rupture, lecture, energie, lacunes (moment), fin.

### carte.html — carte du chapitre (comme dipole-rc-tableau/carte.html)
Centre « Dipôle RL » + branches : bobine, tension, echelon, equation, solution, tau, rupture, courbes, energie, national, suite (« vers le RLC »).
Moments : centre, puis une par branche dans cet ordre, fin. Repères : les mêmes noms (sans fin).
