# Contrat des simulations — cours « Oscillations libres d'un circuit RLC série » (phys_ch8_circuit_RLC)

Écrit le 12 novembre 2026 (routine cloud). Dossier : frontend/public/media/simulations/physics/circuit-rlc-tableau/
Déjà présents (copies de dipole-rl-tableau, ne pas modifier sauf besoin indispensable sans casser les autres pages) : commun.js
(window.OndesTableau.Scene : cadre virtuel 760 × 420, cadre()/local(), image()), exposants.js (10⁻³, T₀², π² à la craie), rlc.css.
Le cours (backend/data/courses/phys_ch8_circuit_RLC.json) pilote ces pages par `play_until {moment}` et pointe les repères : les NOMS de vues,
moments, repères et paramètres ci-dessous sont EXACTS (copie : tables MOMENTS / REPERES de outils/cours/notes/cours/circuit_RLC_build/outils.py).
On peut en ajouter, jamais en renommer. Exploration : backend/data/curriculum/exploration/circuit_RLC.json (visuels, regles_des_simulations).

## Lire d'abord (par extraits si gros)
- .agents/skills/simulations-au-tableau/SKILL.md (À SUIVRE À LA LETTRE)
- le kit : frontend/public/media/simulations/shared/tableau/tableau.js, tableau.css (et imprimer.js pour bilan/carte)
- MODÈLES DIRECTS (même chapitre d'électricité, même style ; forme seulement, ne pas modifier) : physics/dipole-rl-tableau/
  (circuit-rl.html : montage à deux positions, flèches, oscilloscope ; courbe.html : courbe, lecture ; influence.html : deux courbes
  superposées ; energie.html : barre + calcul ; figures.html : figures à étapes ?fig= ; bilan.html ; carte.html) et physics/dipole-rc-tableau/
  (condensateur.html : armatures, électrons ; circuit-rc.html ; energie.html). Partir d'une COPIE de la page modèle indiquée pour chaque page.

## Règles communes
- Chaque page : `<link>` /media/simulations/shared/tableau/tableau.css + rlc.css ; scripts /media/simulations/shared/tableau/tableau.js,
  commun.js, exposants.js, puis le script de la page, puis `<script src="/media/simulations/professor-locate.js" defer></script>`.
- Fond transparent, cadre virtuel 760 × 420, rien de coupé, pas de défilement, barre (bouton + bulle) EN HAUT, bas libre (4.5em).
  UN bouton principal qui cycle (Lancer → Pause → Reprendre → Rejouer) avec data-professor-control ; réglages = poignées glissées (Tableau.glisser).
- `Tableau.protocole({ id, commandes, config, texte, etat, progression, executer })` ; commandes : start, reset, pause, resume,
  set_time {time_s}, set_parameters {…}, play_until {moment | time_s} (rejoue depuis 0 si l'instant est passé, sinon continue, puis se fige
  avec « Arrêt sur image : … »). highlight {target} est ajouté par le kit.
- État : simulation_status, ce_qui_se_voit (phrase française qui dit TOUT ce qu'on voit, valeurs avec unités), current_variant, time_s,
  parameters, moments (nom → instant en s DE LA SIMULATION), derniere_main. Le moment `fin` existe partout. Paramètre `vue` (?vue= dans
  l'URL ET set_parameters) quand la page a des vues. Vue par défaut = la première de la liste.
- Les oscillations réelles durent quelques ms : la simulation les montre AU RALENTI (une période propre ≈ 2 à 3 s de simulation), et la bulle
  le dit (« au ralenti »). Les nombres affichés sont ceux du vrai circuit (ms).
- Repères `craie.repere(id, x, y, w, h, 'libellé')` pour TOUS les ids listés (noms exacts), et `Tableau.explication({ <vue>: [{ repere, texte }] })`.
- Rendu à la demande ; une scène figée dessine encore ce qui bouge. Apostrophe typographique ’ dans les chaînes JS françaises.
- Rendu « réel » : générateur (boîtier), interrupteur K à DEUX positions (1 : charge par le générateur ; 2 : décharge dans la bobine),
  CONDENSATEUR peint (condensateur chimique bleu, comme dipole-rc-tableau/condensateur.html) à côté de son symbole à la craie (deux traits),
  BOBINE peinte (spires de cuivre orangées sur un mandrin, comme dipole-rl-tableau) à côté de son symbole (créneaux arrondis + L, r),
  résistor (rectangle à bandes), oscilloscope (écran vert sombre, grille 10 × 8 carreaux, sensibilités écrites), boîte « G » (générateur
  d'entretien, boîtier avec « u_G = k·i »), électrons = petites sphères bleues. La craie : fils, lettres, axes, cotes, flèches, équations, courbes.
- Couleurs FIXES : ROUGE = condensateur (u_C, q, E_e), VERT = bobine (i, E_m), BLANC = énergie totale E (et la craie ordinaire),
  JAUNE = surlignage seulement. (Une seconde courbe de comparaison : même couleur en pointillés.)
- Écriture : indices jamais avec « _ » visible : u_C, u_R, u_b, u_G, U_m, I_m, E_e, E_m, T₀, Q_m rendus en indice par le kit ;
  « d²q/dt² », « d²u_C/dt² », « 2π√(LC) », « π² = 10 », « µF », « mH », « Ω », « ms », « mA », « µJ ». Virgule décimale française (0,1 H).
  Graduations rondes (1 ms, 2 V) ; l'écran ne donne pas la réponse d'une question avant son moment.
- MOTS INTERDITS (dessin, ce_qui_se_voit, explications) = hors_cadre.mots du cadre : facteur de qualité, bande passante, résonance,
  oscillations forcées, régime forcé, impédance, réactance, équation caractéristique, discriminant, racines complexes, pulsation complexe,
  décrément logarithmique, coefficient d'amortissement, enveloppe exponentielle, résistance critique, oscillateur harmonique, déphasage,
  analogie électromécanique, circuit bouchon, filtre passe-bande. Et jamais : « T₀ = 2π√(L/C) », « la pseudo-période est la période propre »,
  « la résistance crée les oscillations », α = R/2L, R_c = 2√(L/C), aucune formule du régime critique (on dit « frontière »).
- Formules écrites seulement (+ applications numériques) : q = C·u_C ; i = dq/dt = C·du_C/dt ; u_R = R·i ; u_b = L·di/dt + r·i ;
  u_b(0⁺) = −u_C(0) ; u_C + u_R + u_b = 0 ; di/dt = d²q/dt² = C·d²u_C/dt² ; L·d²q/dt² + (R + r)·dq/dt + q/C = 0 ;
  LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0 ; d²u_C/dt² + ((R + r)/L)·du_C/dt + u_C/(LC) = 0 ; d²u_C/dt² + u_C/(LC) = 0 ;
  d²q/dt² + q/(LC) = 0 ; u_C(t) = U_m·cos(2πt/T₀ + φ) ; du_C/dt = −(2π/T₀)·U_m·sin(2πt/T₀ + φ) ; d²u_C/dt² = −(2π/T₀)²·u_C ;
  (2π/T₀)² = 1/(LC) ; T₀ = 2π√(LC) ; ω₀ = 2π/T₀ = 1/√(LC) ; [L]·[C] = [T]² ; u_C(0) = U_m·cos φ ; T ≈ T₀ ; T₀² = 4π²·L·C ;
  L = T₀²/(4π²·C) ; C = T₀²/(4π²·L) ; π² = 10 ; E_e = ½·C·u_C² = q²/(2C) ; E_m = ½·L·i² ; E = ½·C·u_C² + ½·L·i² ; E = ½·C·E² = ½·L·I_m² ;
  dE/dt = −(R + r)·i² ; dE_T/dt = −r·i² (bobine seule) ; |ΔE| = ½·C·(U₁² − U₂²) ; u_G = k·i ; L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0 ; k = R + r.
- Valeurs par défaut (exactes, vérifiées en python ; même circuit partout sauf mention) : E = 6 V, C = 4 µF, L = 0,1 H, r = 10 Ω,
  R = 10 Ω (R + r = 20 Ω) →
  T₀ = 2π√(LC) = 2π√(4·10⁻⁷) ≈ 3,97 ms, écrit « T₀ ≈ 4 ms » (avec π² = 10 : T₀² = 40 × 0,1 × 4·10⁻⁶ = 1,6·10⁻⁵ s², T₀ = 4·10⁻³ s exactement) ;
  pseudo-période (R + r = 20 Ω) T ≈ 3,98 ms ≈ 4 ms ; sommets de u_C aux instants 0, T, 2T, 3T : 6 V ; 4,0 V ; 2,7 V ; 1,8 V (creux à T/2 : −4,9 V) ;
  du 1er au 4e sommet : 3·T ≈ 12 ms ; E(0) = ½·C·E² = ½ × 4·10⁻⁶ × 6² = 7,2·10⁻⁵ J (72 µJ) ; I_m (LC) = E·√(C/L) ≈ 38 mA (37,9) ;
  énergie perdue entre les sommets 0 et T : ½ × 4·10⁻⁶ × (6² − 4²) = 4·10⁻⁵ J (40 µJ) ; u_b(0⁺) = −u_C(0) = −6 V ;
  apériodique : R = 1 kΩ ; « frontière » (régime critique) : R = 300 Ω (aucune formule) ; périodique : « R + r = 0 » (LC idéal) ;
  E doublée (12 V) : U_m = 12 V, T₀ inchangée ; C × 4 (16 µF) ou L × 4 (0,4 H) : T₀ ≈ 8 ms ; décharge RC de rappel : R = 1 kΩ (τ = 4 ms) ;
  entretien : k de 0 à 40 Ω ; k = R + r = 20 Ω → amplitude constante 6 V, période T₀ ≈ 4 ms.
- Interdits : ne rien modifier hors de circuit-rlc-tableau/ (pas frontend/src, pas backend, pas le kit shared/, pas les autres cours, pas
  dipole-rl-tableau ni dipole-rc-tableau) ; aucun commit/push/stash/reset/checkout ; aucune voix ; aucun site ; pas de sous-agent.
- Vérification obligatoire : `node --check` sur chaque bloc <script> (extrait) et chaque .js. Test navigateur : serveur statique sur
  frontend/public (`python3 -m http.server <port libre, donné dans ta mission> --bind 127.0.0.1` en arrière-plan, arrêté à la fin), Playwright
  node (`require('playwright')`, `chromium.launch()`) : aucune erreur JS, encre sur le canvas, bouton présent, `window.__horsCadre` vide ;
  piloter par postMessage {type:'simulation_control', command, parameters} (forme : outils/cours/notes/cours/circuit_RLC_build/verif_sims.js)
  et relire le dernier `simulation_state` : chaque moment existe et `play_until` s'y fige, chaque repère existe (`Tableau.listeReperes()`),
  les nombres sont justes. Une capture par vue (deviceScaleFactor 1) regardée puis effacée.
- Rapport final (court) : fichiers créés, moments réels (nom → s) par vue, repères, paramètres acceptés, écarts avec la fiche, résultats.

## RÉPARTITION (3 agents, un groupe chacun)
| Groupe | Pages | Page modèle à copier |
|---|---|---|
| A — circuits | circuit-lc.html (montage, bascule, echange) | dipole-rl-tableau/circuit-rl.html (+ armatures/électrons de dipole-rc-tableau/condensateur.html, barres de dipole-rl-tableau/energie.html) |
| A | equation.html (pas de vue) | dipole-rl-tableau/circuit-rl.html (schéma, flèches) + lignes à étapes de dipole-rl-tableau/figures.html |
| A | entretien.html (pas de vue) | dipole-rl-tableau/circuit-rl.html (circuit, écran d'oscilloscope) |
| B — courbes | oscillogramme.html (periodique, pseudo, aperiodique, critique, comparer) | dipole-rl-tableau/circuit-rl.html (écran) + dipole-rl-tableau/courbe.html (lecture) |
| B | solution.html (cos, phase) | dipole-rl-tableau/courbe.html |
| B | periode.html (T0, influence_L, influence_C) | dipole-rl-tableau/influence.html |
| C — énergie, figures, fiches | energie.html (echange, amortie) | dipole-rl-tableau/energie.html (+ dipole-rc-tableau/energie.html) |
| C | figures.html?fig=… (8 figures) | dipole-rl-tableau/figures.html |
| C | bilan.html, carte.html | dipole-rl-tableau/bilan.html, dipole-rl-tableau/carte.html |

Diapositives servies (plan.diapositives → page/vue/moments) :
o1 carte (centre … national) · o2 circuit-lc montage (montage, charge, fleches) ou figures fig_prerequis · d1 circuit-lc bascule (rc_decharge) ·
d2 bascule (remplacer, bascule, descente) · d3 bascule (u_nulle_i_max, recharge_inverse) · d4 bascule (retour, periode) · d5 solution cos (signe_i) ·
d6 equation (fleches, ub_initial) · r1 oscillogramme pseudo (trace, sommets_decroissants) · r2 oscillogramme aperiodique (trace,
retour_sans_oscillation, frontiere) · r3 oscillogramme comparer · r4 fig_2021R · e1 equation (fleches, additivite) · e2 equation (remplacer) ·
e3 equation (deriver_deux_fois, equation_q) · e4 equation (equation_uc) · e5 equation (lc_ideal) · e6 solution cos (courbe, Um, T0) ·
e7 solution cos (derivee_1, derivee_2) · e8 solution cos (identification) · p1 periode T0 (unites) · p2 periode T0 (E_change) ·
p3 periode influence_C (C_fois_4) [influence_L : L_fois_4] · p4 fig_2022N · c1 solution phase (depart) · c2 solution cos (Um) ·
c3 solution phase (deux_angles) · c4 solution phase (phi_choisi) · l1 oscillogramme pseudo (mesure_nT) · l2 oscillogramme pseudo (T_voisine_T0) ·
l3 fig_carre · l4 fig_2023N · en1 circuit-lc echange · en2 energie echange (depart) · en3 energie echange (echange, tout_bobine) ·
en4 energie echange (somme_constante) · a1 energie amortie (pertes, chaleur) · a2 energie amortie (derivee) · a3 energie amortie (dE_dt) ·
a4 energie amortie (deux_sommets) · a5 energie amortie (pertes) · k1 entretien (amorti, dispositif) · k2 entretien (equation, compensation) ·
k3 entretien (entretenu, periode_T0) · n1 fig_2020N · n2 fig_2025N · bl bilan · cr carte (complete).

## Fiches — GROUPE A (circuits)

### circuit-lc.html (vues montage | bascule | echange) — RLC1, RLC6 — modèle : dipole-rl-tableau/circuit-rl.html
Montage commun : générateur E = 6 V, interrupteur K à deux positions (1 : générateur + condensateur ; 2 : condensateur + R + bobine, SANS
générateur), condensateur C = 4 µF (peint + symbole, armatures A et B), résistor R = 10 Ω, bobine (L = 0,1 H, r = 10 Ω, peinte + symbole),
oscilloscope (voie 1 aux bornes du condensateur : u_C ; masse).
montage : moments montage (le circuit se dessine, K ouvert), charge (K en 1 : des électrons quittent A ; « + » sur A, « − » sur B ; u_C monte
à E = 6 V : « condensateur chargé »), fleches (convention récepteur dans la maille 2 : flèche i, flèches u_C, u_R, u_b ; « i = dq/dt ; q = C·u_C »
écrit), oscillo (voie 1 et masse branchées, écran prêt), fin.
bascule : moments rc_decharge (RAPPEL : la maille 2 ne contient qu'un résistor de 1 kΩ ; K en 2 ; u_C(t) descend de 6 V vers 0 sans jamais
passer en dessous, courbe rouge sur l'écran ; « décharge dans R : u_C reste positive »), remplacer (le résistor de 1 kΩ est remplacé par la bobine
(L, r) en série avec R = 10 Ω ; écran effacé ; K revient en 1, condensateur rechargé à 6 V), bascule (K passe en 2 ; les électrons repartent),
descente (u_C descend de 6 V vers 0 ; ARRÊT avant 0 : on ne montre pas encore la suite), u_nulle_i_max (u_C = 0 : armatures sans signe, électrons
au plus vite, flèche i la plus épaisse, « u_C = 0 ; i maximal »), recharge_inverse (les électrons continuent : « − » sur A, « + » sur B ; u_C devient
négative jusqu'au creux ≈ −4,9 V ; « la bobine garde le courant »), retour (le courant change de sens ; u_C remonte vers un sommet ≈ 4,0 V),
periode (deux sommets successifs marqués, cote « T ≈ 4 ms » ; « oscillations électriques libres » écrit), fin.
echange : à côté du circuit (K en 2), deux barres verticales : E_e (rouge, « E_e = ½·C·u_C² ») et E_m (verte, « E_m = ½·L·i² ») ; moments
energie_condensateur (barre rouge pleine, verte vide, u_C = 6 V, i = 0), energie_bobine (u_C = 0 : rouge vide, verte pleine), echange (les barres
se vident et se remplissent tour à tour pendant une période), total (« E = ½·C·u_C² + ½·L·i² » écrit sous les barres), fin.
Paramètres : vue ; K (1 | 2, poignée sur K pour les vues montage et bascule).
Repères (toutes vues) : generateur interrupteur position_1 position_2 condensateur armature_A armature_B bobine resistance fleche_i fleche_uC
fleche_uR fleche_ub oscilloscope voie_1 masse ecran courbe electrons sommet barre_Ee barre_Em formule_total.

### equation.html (pas de vue) — RLC1, RLC3 — modèle : dipole-rl-tableau/circuit-rl.html + lignes de dipole-rl-tableau/figures.html
À gauche, la maille de décharge (K en 2, sans générateur) : condensateur, R, bobine (L, r), flèche i, flèches u_C, u_R, u_b (convention
récepteur) ; à droite, les lignes qui s'écrivent l'une sous l'autre (chaque tension remplacée sous sa flèche).
Moments : fleches (le circuit et les quatre flèches), ub_initial (« i(0⁺) = 0 : i est continue dans la bobine » ; « u_R(0⁺) = R·0 = 0 » ;
« u_b(0⁺) = −u_C(0) = −6 V »), additivite (« u_C + u_R + u_b = 0 » ; « pas de générateur : 0 »), remplacer (sous les flèches « u_C = q/C »,
« u_R = R·i », « u_b = L·di/dt + r·i » ; puis « q/C + R·i + L·di/dt + r·i = 0 »), deriver_deux_fois (« i = dq/dt ; di/dt = d²q/dt² »),
equation_q (« L·d²q/dt² + (R + r)·dq/dt + q/C = 0 » encadré), equation_uc (« q = C·u_C : i = C·du_C/dt ; di/dt = C·d²u_C/dt² » ;
« LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0 » ; puis ÷ LC : « d²u_C/dt² + ((R + r)/L)·du_C/dt + u_C/(LC) = 0 »), lc_ideal (« R + r = 0 » :
le terme du milieu barré en jaune ; « d²u_C/dt² + u_C/(LC) = 0 » encadré ; petite courbe à sommets égaux), fin.
Repères : circuit condensateur resistance bobine fleche_i fleche_uC fleche_uR fleche_ub ub_initial additivite remplacement_uC remplacement_uR
remplacement_ub derivee equation_q equation_uc terme_milieu lc_ideal.

### entretien.html (pas de vue) — RLC8 — modèle : dipole-rl-tableau/circuit-rl.html
Circuit RLC (C = 4 µF, L = 0,1 H, r = 10 Ω, R = 10 Ω) et écran d'oscilloscope (u_C, 2 V/carreau, 2 ms/carreau).
Moments : amorti (sans G : u_C oscille, les sommets baissent 6 → 4,0 → 2,7 V), dispositif (on ajoute en série la boîte G : « u_G = k·i »,
« G rend l'énergie perdue » ; fonctionnement interne non montré), equation (« u_C + u_R + u_b = u_G = k·i » puis
« L·d²q/dt² + (R + r − k)·dq/dt + q/C = 0 »), compensation (« k = R + r = 20 Ω » : le terme du milieu barré en jaune), entretenu (poignée k à
20 Ω : sinusoïde rouge d'amplitude constante 6 V ; si k < 20 Ω, les sommets baissent encore), periode_T0 (deux sommets cotés « T₀ = 2π√(LC) ≈ 4 ms »), fin.
Paramètres : k (0 → 40 Ω, défaut 0 puis 20 au moment compensation ; k > R + r non montré : poignée bornée à 20 Ω au-delà du moment entretenu,
ou amplitude qui grandit sans sortir de l'écran).
Repères : circuit generateur_G formule_uG ecran courbe equation terme_milieu poignee_k sommets T0.

## Fiches — GROUPE B (courbes)

### oscillogramme.html (vues periodique | pseudo | aperiodique | critique | comparer) — RLC2, RLC5 — modèle : dipole-rl-tableau/circuit-rl.html (écran) + courbe.html
Écran d'oscilloscope peint (grille 10 × 8 carreaux, « 2 ms/div », « 2 V/div »), u_C(t) rouge qui se trace (condensateur chargé à 6 V au départ,
C = 4 µF, L = 0,1 H) ; le régime est écrit à la craie sous l'écran.
periodique (« R + r = 0 », LC idéal) : trace (sinusoïde de 6 V), sommets_egaux (tous les sommets sur une même ligne jaune : « régime périodique »), fin.
pseudo (R + r = 20 Ω) : trace, premier_sommet (sommet à t = T marqué : ≈ 4,0 V), sommets_decroissants (6 ; 4,0 ; 2,7 ; 1,8 V marqués :
« régime pseudo-périodique ; T : pseudo-période »), mesure_nT (cote du 1er au 4e sommet : « 3T ≈ 12 ms donc T ≈ 4 ms » ; un trait barré
entre un sommet et le creux suivant : « T/2, pas T »), T_voisine_T0 (« T₀ = 2π√(LC) ≈ 4 ms ; T ≈ T₀ : amortissement faible »), fin.
aperiodique (R = 1 kΩ) : trace (u_C revient vers 0 sans changer de signe), retour_sans_oscillation (« régime apériodique »), frontiere
(la poignée R descend à 300 Ω : retour le plus rapide sans oscillation, courbe en pointillés ; « régime critique : la frontière » ; aucune formule), fin.
critique (R = 300 Ω) : trace, frontiere, fin.
comparer : trois petits écrans côte à côte, même échelle : moments pseudo (R + r = 20 Ω), aperiodique (R = 1 kΩ), periodique (R + r = 0,
écran du milieu ou premier), ordre (flèche « l'amortissement augmente avec R + r » : périodique → pseudo-périodique → apériodique ;
« L et C font osciller, R + r amortit »), fin.
Paramètres : vue ; R (0 → 2000 Ω, poignée « R », vues pseudo, aperiodique, critique).
Repères : ecran sensibilites courbe sommets premier_sommet mesure T T0 regime poignee_R courbe_periodique courbe_pseudo courbe_aperiodique ordre.

### solution.html (vues cos | phase) — RLC1, RLC4, RLC5 — modèle : dipole-rl-tableau/courbe.html
Axes t (ms, 0 à 10) et u_C (V, −8 à 8) ; LC idéal, C = 4 µF, L = 0,1 H, E = 6 V.
cos : courbe (u_C(t) rouge, départ au sommet 6 V ; « u_C(t) = U_m·cos(2πt/T₀ + φ) » écrit), Um (deux traits horizontaux sur un sommet et
un creux : « U_m = 6 V » ; l'écart sommet–creux 12 V barré « = 2·U_m »), T0 (cote entre deux sommets successifs : « T₀ ≈ 4 ms »),
signe_i (sous le graphe, i(t) verte ; zones où u_C descend → « i = C·du_C/dt < 0 », où u_C monte → « i > 0 »), derivee_1
(« du_C/dt = −(2π/T₀)·U_m·sin(2πt/T₀ + φ) »), derivee_2 (« d²u_C/dt² = −(2π/T₀)²·U_m·cos(2πt/T₀ + φ) = −(2π/T₀)²·u_C »),
identification (« [1/(LC) − (2π/T₀)²]·u_C = 0 » ; « (2π/T₀)² = 1/(LC) » ; « T₀ = 2π√(LC) » encadré ; « ω₀ = 2π/T₀ = 1/√(LC) » en petit ;
A.N. : « T₀² = 4π²·L·C = 40 × 0,1 × 4·10⁻⁶ = 1,6·10⁻⁵ ; T₀ = 4·10⁻³ s = 4 ms (π² = 10) »), fin.
phase : depart (la courbe part du sommet, tangente horizontale : « u_C(0) = U_m·cos φ = E ; i(0) = 0 → U_m = E, φ = 0 » ; « u_C = E·cos(2πt/T₀) »),
deux_angles (nouveau départ : U_m = 6 V, u_C(0) = 3 V ; « cos φ = 3/6 = 0,5 → φ = +π/3 ou φ = −π/3 » ; deux courbes en pointillés : l'une
part en montant, l'autre en descendant), phi_choisi (la courbe part de 3 V EN MONTANT ; « du_C/dt(0) = −(2π/T₀)·U_m·sin φ > 0 → sin φ < 0 →
φ = −π/3 rad » ; l'autre courbe barrée), fin.
Paramètres : vue ; phi (−π → π, poignée sur le point de départ, vue phase) ; Um (1 → 8 V).
Repères : axe_t axe_u courbe formule Um ecart T0 courbe_i signe_i derivee_1 derivee_2 identification resultat point_depart tangente_depart angles phi.

### periode.html (vues T0 | influence_L | influence_C) — RLC4, RLC5 — modèle : dipole-rl-tableau/influence.html
Axes t (ms, 0 à 16) et u_C (V, −14 à 14) ; LC idéal, E = 6 V, C = 4 µF, L = 0,1 H.
T0 : lecture_T0 (courbe rouge, cote entre deux sommets « T₀ ≈ 4 ms lue »), calcul_T0 (« T₀ = 2π√(LC) = 2π√(0,1 × 4·10⁻⁶) ≈ 4·10⁻³ s »),
unites (« [L] = [U]·[T]/[I] ; [C] = [I]·[T]/[U] ; [L]·[C] = [T]² : √(LC) est un temps ; 2π sans unité »), E_change (seconde courbe en pointillés,
condensateur chargé sous 12 V : U_m = 12 V, sommets aux MÊMES instants ; « T₀ ne dépend pas de E »), fin.
influence_C : courbe (référence C = 4 µF, T₀ ≈ 4 ms), C_fois_4 (C = 16 µF en pointillés : T₀ ≈ 8 ms ; « C × 4 → T₀ × 2 »), fin.
influence_L : courbe (référence), L_fois_4 (L = 0,4 H en pointillés : T₀ ≈ 8 ms ; « L × 4 → T₀ × 2 »), fin.
Paramètres : vue ; L (0,025 → 0,4 H) ; C (1 → 16 µF) ; E (2 → 12 V).
Repères : axe_t axe_u courbe T0 calcul unites courbe_E courbe_L courbe_C T0_double.

## Fiches — GROUPE C (énergie, figures, bilan, carte)

### energie.html (vues echange | amortie) — RLC6, RLC7 — modèle : dipole-rl-tableau/energie.html
Graphe E (µJ, 0 à 80) en fonction de t (ms, 0 à 10), à côté de deux barres (E_e rouge, E_m verte) ; C = 4 µF, L = 0,1 H, E = 6 V.
echange (LC idéal, R + r = 0) : depart (t = 0 : u_C = 6 V, i = 0 ; barre rouge pleine, verte vide ; « E = ½·C·E² = ½ × 4·10⁻⁶ × 6² = 7,2·10⁻⁵ J »),
echange (les courbes E_e(t) rouge et E_m(t) verte se tracent ; les barres suivent), tout_bobine (arrêt à u_C = 0 : E_e = 0, E_m = 72 µJ ;
« toute l'énergie est dans la bobine »), tout_condensateur (arrêt à un creux de u_C, i = 0 : « toute l'énergie est dans le condensateur » ;
« E_e est maximale deux fois par période »), somme_constante (la somme E(t) blanche : droite horizontale à 72 µJ ; « R + r = 0 : E se conserve » ;
« E_m = E − ½·C·u_C² »), fin.
amortie (R + r = 20 Ω) : pertes (E_e rouge et E_m verte qui se croisent, E blanche qui descend par marches ; E_e part de son maximum, E_m de 0),
chaleur (la résistance rougit, halo : « effet Joule dans R et dans r »), derivee (« d(½·C·u_C²)/dt = C·u_C·du_C/dt = u_C·i » ;
« d(½·L·i²)/dt = L·i·di/dt »), dE_dt (« dE/dt = i·(u_C + L·di/dt) » ; « u_C + L·di/dt = −(R + r)·i » ; « dE/dt = −(R + r)·i² ≤ 0 » encadré),
deux_sommets (deux sommets de u_C, à t = 0 et t = T ≈ 4 ms, i = 0 : « E = ½·C·u_C² » ; « |ΔE| = ½·C·(U₁² − U₂²) = ½ × 4·10⁻⁶ × (6² − 4²) = 4·10⁻⁵ J »), fin.
Paramètres : vue ; R (0 → 100 Ω, vue amortie).
Repères : axe_t axe_E barre_Ee barre_Em courbe_Ee courbe_Em courbe_E formule resistance derivee dE_dt sommet_1 sommet_2 energie_perdue.

### figures.html?fig=… — figures à étapes (comme dipole-rl-tableau/figures.html)
Un repère `figure` + un repère par étape (même nom que le moment). Moments (dans l'ordre, + fin) :
- fig_prerequis : charge (« i = dq/dt ; q = C·u_C »), bobine (« u_b = L·di/dt + r·i »), derivee (« (cos(2πt/T₀))′ = −(2π/T₀)·sin(2πt/T₀) »),
  recette (« additivité → équation → solution », comme au RC et au RL)
- fig_2021R : enonce (bobine L = 0,51 H, r = 5 Ω ; C = 100 µF ; R₃ = 10 Ω, R₄ = 100 Ω), courbes ((a) trait plein peu amorti, (b) pointillés très
  amortis), comparer (R₃ + r = 15 Ω ; R₄ + r = 105 Ω), resultat ((a) → R₃ ; (b) → R₄), periode (T = 45 ms lue sur (a) ; T₀ = 2π√(LC) ≈ 44,9 ms)
- fig_2022N : enonce (E = 12 V, C = 50 µF, bobine de résistance nulle), courbes (C₁ : cosinus de 12 V ; C₂ : cosinus de 10 V ; C₃ : amortie),
  eliminer_C3 (r = 0 : régime périodique), eliminer_C2 (u_C(0) = E = 12 V), lecture (T₀ = 10 ms), L (L = T₀²/(4π²·C) = (10⁻²)²/(40 × 5·10⁻⁵) = 0,05 H)
- fig_carre : formule (T₀ = 2π√(LC)), carre (T₀² = 4π²·L·C), isoler (C = T₀²/(4π²·L)), an (2020 N : T ≈ T₀ = 10 ms, L = 1 H, π² = 10 :
  C = (10⁻²)²/(40 × 1) = 2,5·10⁻⁶ F = 2,5 µF)
- fig_2023N : enonce (LC idéal, L = 1 H), courbe (u_C(t), flèches d'échelle 5 V et 0,5 ms ; U_m = 10 V), lecture (T₀ = 4 × 0,5 = 2 ms),
  C (C = T₀²/(4π²·L) = (2·10⁻³)²/(40 × 1) = 10⁻⁷ F = 0,1 µF), Em (à 1,8 ms, u_C = 8 V : E_m = ½·C·(10² − 8²) = 1,8·10⁻⁶ J)
- fig_2020N : enonce (bobine L = 1 H, r = 10 Ω ; R = 90 Ω), courbe_uC (u_C pseudo-périodique, T = 10 ms), regime (pseudo-périodique),
  equation (LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0), C (C = T₀²/(4π²·L) = 2,5·10⁻⁶ F), entretien (u_G = k·i ; k₀ = R + r = 100 Ω),
  courbe_i (i(t) entretenue verte, I_m = 8 mA, T₀ = 10 ms, part de 0 en descendant), phase (i(0) = 0 → φ = ±π/2 ; i descend → sin φ > 0 →
  φ = +π/2 rad), energie (E_t = ½·L·I_m² = ½ × 1 × (8·10⁻³)² = 3,2·10⁻⁵ J), Ee (à 16 ms, i = 4,8 mA : E_e = 3,2·10⁻⁵ − ½ × 1 × (4,8·10⁻³)² ≈ 2,05·10⁻⁵ J)
- fig_2025N : enonce (C₀ = 1 µF chargé à U₀ = 10 V ; bobine (L, r) seule), equation (L·C₀·d²u_C/dt² + r·C₀·du_C/dt + u_C = 0),
  courbe (u_C(t) pseudo-périodique, flèche d'échelle 7·10⁻⁵ s = 1 carreau, t_A sommet à 7 V, t_B creux suivant), periode (T = 4 × 7·10⁻⁵ = 2,8·10⁻⁴ s),
  signe_i (u_C décroît entre t_A et t_B : i = C₀·du_C/dt < 0), dE_dt (dE_T/dt = i·(u_C + L·di/dt) = −r·i²),
  energie (|E_th| = ½·C₀·(U₀² − u_C(t_A)²) = ½ × 10⁻⁶ × (10² − 7²) = 2,55·10⁻⁵ J)

### bilan.html — fiche « Ce qu'il faut retenir » (comme dipole-rl-tableau/bilan.html, imprimable)
Blocs (moments et repères du même nom) : fiche, oscillations (décharge dans la bobine ; i = dq/dt = C·du_C/dt ; u_b(0⁺) = −u_C(0)),
regimes (périodique, pseudo-périodique, apériodique ; l'amortissement augmente avec R + r), equation (L·d²q/dt² + (R + r)·dq/dt + q/C = 0 ;
LC·d²u_C/dt² + (R + r)·C·du_C/dt + u_C = 0), lc (d²u_C/dt² + u_C/(LC) = 0), solution (u_C(t) = U_m·cos(2πt/T₀ + φ)), periode (T₀ = 2π√(LC) ;
√(LC) est un temps), conditions (u_C(0) = U_m·cos φ + sens de départ), lecture (T sur plusieurs périodes ; T ≈ T₀ ; C = T₀²/(4π²·L) ; π² = 10),
energie (E = ½·C·u_C² + ½·L·i², constante si R + r = 0), amortissement (dE/dt = −(R + r)·i² ; |ΔE| = ½·C·(U₁² − U₂²)),
entretien (u_G = k·i ; k = R + r ; période T₀), lacunes (moment), fin.
Repères : fiche oscillations regimes equation lc solution periode conditions lecture energie amortissement entretien.

### carte.html — carte du chapitre (comme dipole-rl-tableau/carte.html)
Centre « Circuit RLC série : oscillations libres » + branches : depuis (« depuis le RC et le RL : q = C·u_C, u_b = L·di/dt + r·i »), decharge,
regimes, equation, solution, periode, conditions, lecture, energie, amortissement, entretien, national (« 17 sessions sur 20 : lire T et trouver
L ou C ; une énergie »), suite (« T₀ = 2π√(LC) resservira : circuit d'accord de la modulation »), complete (toutes les branches visibles,
entourées une à une ; servira à la fin du cours).
Moments : centre, puis une par branche dans cet ordre, complete, fin. Repères : les mêmes noms (sans complete ni fin).
