# Contrat des simulations — cours « Noyaux, masse et énergie » (phys_ch5_energie_nucleaire)

Dépôt : C:\Users\HP\Desktop\ai-tutor-bac (partagé : d'autres sessions y travaillent en parallèle).
Dossier à remplir : frontend/public/media/simulations/physics/energie-nucleaire-tableau/
(déjà présents : commun.js = window.OndesTableau.Scene, exposants.js, nucleaire.css — copies du cours des ondes lumineuses ;
ne les modifie pas ; si tu as besoin d'une aide commune, mets-la DANS ta page).

## Lire d'abord (par extraits si gros)
- .agents/skills/simulations-au-tableau/SKILL.md (À SUIVRE À LA LETTRE), docs/design/labos-au-tableau.md
- le kit : frontend/public/media/simulations/shared/tableau/tableau.js, tableau.css, imprimer.js
- modèles (forme seulement, ne les modifie pas) : frontend/public/media/simulations/physics/ondes-lumineuses-tableau/
  diffraction.html (protocole, moments, play_until, repères, explication, ?vue=), courbe.html (axes, points, droite, poignée de
  lecture), figures.html (figures à étapes ?fig=), bilan.html, carte.html ; et ondes-tableau/ballon.html pour le rendu « réel ».

## Règles communes
- Chaque page : `<link>` /media/simulations/shared/tableau/tableau.css + nucleaire.css ; scripts /media/simulations/shared/tableau/tableau.js,
  commun.js, exposants.js, puis le script de la page, puis `<script src="/media/simulations/professor-locate.js" defer>`.
- Fond transparent, cadre virtuel 760 × 420 (OndesTableau.Scene, cadre()/local()), rien de coupé, pas de défilement, barre (bouton +
  bulle) EN HAUT, bas libre (4.5em). UN bouton principal qui cycle (Lancer → Pause → Reprendre → Rejouer) avec
  data-professor-control ; les réglages = poignées glissées / touchées sur le dessin (Tableau.glisser), pas de curseurs.
- `Tableau.protocole({ id, commandes, config, texte, etat, progression, executer })` ; commandes : start, reset, pause, resume,
  set_time {time_s}, set_parameters {…} (schéma avec plages / valeurs), play_until {moment | time_s} (rejoue depuis 0 si l'instant
  est passé, sinon continue, puis se fige avec « Arrêt sur image : … » dans la bulle). highlight {target} est ajouté par le kit.
- État : simulation_status, ce_qui_se_voit (phrase française qui dit TOUT ce qu'on voit : vues, valeurs avec unités, phase en cours),
  current_variant, time_s, parameters, moments (objet nom → instant en s, recalculé quand un paramètre change), derniere_main (kit).
  Émis à chaque événement et toutes les 500 ms pendant que ça tourne. Le moment `fin` existe partout.
- Repères `craie.repere(id, x, y, w, h, 'libellé')` pour TOUS les ids listés ci-dessous (le cours pointe dessus par ces noms exacts ;
  un repère doit exister au plus tard quand la scène est jouée jusqu'à `fin`), et `Tableau.explication({ <vue>: [{ repere, texte }] })`.
- Une scène figée dessine encore ce qui bouge (running || pause).
- Apostrophe typographique ’ dans toute chaîne JS en français (ou backticks). Déclarer la scène avant la boucle.
- ÉCRITURE D'UN NOYAU ᴬ_Z X : A en haut à gauche, Z en bas à gauche, alignés à droite contre le symbole, taille 0,6 × celle du
  symbole (A monté de ≈ 0,45 × taille, Z descendu de ≈ 0,3 × taille). Écris une petite fonction `noyauTexte(craie, A, Z, X, x, y, o)`
  dans ta page (pas de fichier commun). Particules : ¹₀n (neutron), ¹₁p (proton), ⁰₋₁e (électron), ⁰₁e (positon), ⁴₂He.
- Rendu « réel » (règle 7) : les nucléons sont des sphères ombrées (dégradé radial, reflet, petite ombre) : PROTON rouge
  (#d9534f), NEUTRON gris-bleu (#8fa3b8) — mêmes couleurs dans toutes les pages ; un noyau = un amas compact de sphères qui se
  touchent ; l'énergie libérée = un éclair / rayonnement peint (halo jaune-orangé qui s'étend puis s'efface) ; un plateau de balance
  en métal ombré. La craie : lettres, cotes, flèches, axes, valeurs. Le peint ne change jamais la physique (valeurs exactes dans
  ce_qui_se_voit et sur la craie). Tout ce qui est exagéré pour l'œil (inclinaison de la balance, écarts de niveaux du diagramme
  « échelle non respectée ») est ÉCRIT au tableau. Rendu à la demande.
- Texte du tableau en français, indices jamais avec « _ » visible (Craie.segments rend m_p en indice), exposants via exposants.js
  (« 10⁻²⁷ »). Virgule décimale française (4,00150 u). Notation : E_ℓ (indice ℓ), E_ℓ/A, Δm, ΔE, E_lib = |ΔE|, m_p, m_n,
  1 u = 931,5 MeV/c², 1 MeV = 1,6·10⁻¹³ J.
- MOTS INTERDITS sur le dessin, dans ce_qui_se_voit et les explications : interaction forte, interaction faible, quark, gluon,
  section efficace, barn, neutron thermique, modérateur, barre de contrôle, masse critique, facteur de multiplication, Weizsäcker,
  goutte liquide, formule semi-empirique, modèle en couches, nombres magiques, facteur de Lorentz, masse relativiste, relativité,
  Lawson, tokamak, confinement, photon, E = hν, effet tunnel.
- Formules écrites autorisées seulement : E = m·c² ; ΔE = Δm·c² ; 1 u = 1,66·10⁻²⁷ kg ; 1 u = 931,5 MeV/c² ; 1 eV = 1,6·10⁻¹⁹ J ;
  1 MeV = 1,6·10⁻¹³ J ; N = A − Z ; Δm = Z·m_p + (A − Z)·m_n − m(ᴬ_ZX) ; E_ℓ = Δm·c² ; E_ℓ/A ; Δm = Σm(produits) − Σm(réactifs) ;
  ΔE = Σ E_ℓ(réactifs) − Σ E_ℓ(produits) ; E_lib = |ΔE| ; E_ℓ = A·(E_ℓ/A) ; N = m·N_A/M ; E = N·E_lib ; et des applications numériques.
- Valeurs de référence (n'en invente pas d'autres) : m_p = 1,00728 u ; m_n = 1,00866 u ; m(e) = 0,00055 u ; 1 u = 931,5 MeV/c² =
  1,66·10⁻²⁷ kg ; 1 MeV = 1,6·10⁻¹³ J ; c = 3,00·10⁸ m/s ; N_A = 6,02·10²³ mol⁻¹.
  Noyaux (masse du noyau, Δm, E_ℓ, E_ℓ/A) :
  ²H 2,01355 u (E_ℓ = 2,23 MeV ; 1,11 MeV/nucléon) ; ³H 3,01550 u (E_ℓ = 8,48 MeV ; 2,83) ; ⁴He 4,00150 u (Δm = 0,03038 u ;
  E_ℓ = 28,30 MeV ; 7,07) ; ¹²C 11,99671 u (Δm = 0,09893 u ; 92,15 MeV ; 7,68) ; ¹⁴C 13,99995 u (0,11301 u ; 105,27 MeV ; 7,52) ;
  ⁵⁶Fe 55,92067 u (0,52841 u ; 492,2 MeV ; 8,79) ; ⁶⁰Ni 59,91543 u (0,56553 u ; 526,8 MeV ; 8,78) ; ⁹⁴Sr 93,8945 u (8,59) ;
  ¹⁴⁰Xe 139,8920 u (8,29) ; ²³⁵U 234,9935 u (1,91464 u ; 1783,5 MeV ; 7,59). Autres points de la courbe (E_ℓ/A en MeV/nucléon) :
  ⁶Li 5,33 ; ⁷Li 5,61 ; ⁹Be 6,46 ; ¹⁶O 7,98 ; ²⁰Ne 8,03 ; ⁴⁰Ca 8,55 ; ⁹⁰Zr 8,71 ; ¹²⁰Sn 8,50 ; ¹⁶⁵Ho 8,15 ; ²⁰⁸Pb 7,87 ; ²³⁸U 7,57.
  Fusion (national 2016 N) : ²₁H + ³₁H → ⁴₂He + ¹₀n ; Σm réactifs = 5,02905 u ; Σm produits = 5,01016 u ; Δm = −0,01889 u ;
  ΔE = −17,6 MeV ; E_lib = 17,6 MeV. Par les E_ℓ (national 2023 N) : E_ℓ(²H) = 2,366 ; E_ℓ(³H) = 8,475 ; E_ℓ(⁴He) = 28,296 MeV →
  ΔE = 10,841 − 28,296 = −17,455 MeV ; E_lib ≈ 17,5 MeV.
  Fission : ²³⁵₉₂U + ¹₀n → ⁹⁴₃₈Sr + ¹⁴⁰₅₄Xe + 2 ¹₀n ; Σm réactifs = 236,00216 u ; Σm produits = 235,80382 u ; Δm = −0,19834 u ;
  ΔE ≈ −184,8 MeV ; E_lib ≈ 185 MeV ≈ 2,96·10⁻¹¹ J.
  Diagramme du ²¹⁰Po (national 2020 N) : 126 ¹₀n + 84 ¹₁p : 1,971820·10⁵ MeV ; ²¹⁰₈₄Po : 1,955372·10⁵ MeV ;
  ²⁰⁶₈₂Pb + ⁴₂He : 1,955318·10⁵ MeV → E_ℓ(Po) = 1644,8 MeV ; E_lib = 5,4 MeV.
- Noms de moments, de repères, de paramètres et de vues : EXACTEMENT ceux de ta fiche ci-dessous (le cours est écrit en parallèle
  avec ces noms). Tu peux en ajouter, jamais en renommer. Si un nom est impossible, dis-le dans ton rapport.
- Interdits : ne modifie rien hors de ce dossier (pas frontend/src, pas backend, pas le kit shared/, pas les autres cours) ; aucun
  commit/push/stash/reset/checkout ; aucune voix ; ne lis aucun fichier d'identifiants ; ne te connecte à aucun site.
- Vérification obligatoire : extraire chaque bloc <script> inline et `node --check` dessus ; relire les libellés aux positions
  extrêmes des poignées. Test navigateur headless : serveur statique local sur frontend/public (`python -m http.server <port libre>
  --bind 127.0.0.1` lancé en arrière-plan, puis arrêté), Playwright (python, `from playwright.sync_api import sync_playwright`,
  Chrome : executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe', args=['--headless=new']) : aucune erreur JS, encre
  sur le canvas, bouton présent, `window.__horsCadre` vide ; pilote-la par `postMessage({type:'simulation_control', command,
  parameters}, '*')` et relis le dernier message `simulation_state` (current_state) : chaque moment de ta fiche existe, play_until
  se fige dessus, chaque repère existe (`Tableau.listeReperes()`), ce_qui_se_voit donne les bonnes valeurs. Modèle de script :
  outils\cours\notes\cours\ondes_lumineuses_build\verif_sims.py
  (copie-le dans le scratchpad et adapte-le, ne le modifie pas).
- Rapport final (court) : fichiers créés, moments réels (nom → s) par vue, repères, paramètres acceptés, écarts avec la fiche,
  résultat des node --check et du test navigateur.

## Fiches

### balance.html — la masse du noyau et celle de ses nucléons ; la masse avant et après une réaction
Une vue « La balance » (grande balance à deux plateaux, métal ombré, fléau qui penche — inclinaison exagérée pour l'œil : l'écrire)
et un panneau « Les masses » à droite (colonne de craie : les masses qui s'additionnent, puis Δm, puis l'énergie).
Paramètre vue (?vue= et set_parameters {vue}) :
- helium (défaut) : plateau gauche « nucléons séparés » : 2 protons + 2 neutrons, sphères écartées ; plateau droit « noyau ⁴₂He »
  (amas). Moments : plateaux_vides, nucleons_poses (les 4 nucléons tombent un à un sur le plateau gauche, masses écrites :
  2 m_p + 2 m_n = 4,03188 u), noyau_pose (le noyau sur le plateau droit : m(⁴₂He) = 4,00150 u), balance_penche (le fléau penche
  du côté des nucléons séparés : « m(noyau) < masse des nucléons séparés »), delta_m (cote Δm = 4,03188 − 4,00150 = 0,03038 u,
  « défaut de masse »), energie (« E_ℓ = Δm·c² = 0,03038 × 931,5 = 28,30 MeV »), fin.
- noyau : le même déroulé pour un noyau choisi : paramètre noyau = helium | carbone12 | carbone14 | fer56 | nickel60 | uranium235
  (valeurs de la liste ; pour les gros noyaux, les nucléons sont représentés par deux tas « Z protons » et « N neutrons » avec leur
  nombre écrit, pas des centaines de sphères). Poignée élève : l'étiquette du noyau sur le plateau droit (touche = noyau suivant).
  Mêmes moments que helium, plus par_nucleon (« E_ℓ/A = … MeV/nucléon »).
- fusion : plateau gauche « réactifs » ²₁H + ³₁H, plateau droit « produits » ⁴₂He + ¹₀n. Moments : plateaux_vides, reactifs_poses
  (5,02905 u), produits_poses (5,01016 u), balance_penche (les produits sont plus légers : « la masse diminue »), delta_m
  (« Δm = Σm(produits) − Σm(réactifs) = −0,01889 u »), energie (« ΔE = Δm·c² = −17,6 MeV ; E_lib = |ΔE| = 17,6 MeV », éclair peint
  sur le plateau des produits), fin.
- fission : réactifs ²³⁵₉₂U + ¹₀n ; produits ⁹⁴₃₈Sr + ¹⁴⁰₅₄Xe + 2 ¹₀n. Mêmes moments que fusion (Δm = −0,19834 u ;
  ΔE ≈ −184,8 MeV ; E_lib ≈ 185 MeV).
Repères : balance, plateau_gauche, plateau_droit, fleau, nucleons, noyau, reactifs, produits, delta_m, energie, colonne_masses,
vue_balance, vue_masses, etiquette_noyau (vue noyau), par_nucleon (vue noyau).
ce_qui_se_voit : vue, ce qui est sur chaque plateau avec sa masse (u), de quel côté penche le fléau, Δm (u), énergie (MeV), phase.

### liaison.html — séparer un noyau coûte E_ℓ ; le former libère E_ℓ
Deux vues : « Le noyau » (au centre, un noyau ⁴₂He en sphères ombrées au repos) et « L'énergie » (une barre verticale de niveaux,
à droite : en bas « noyau au repos », en haut « nucléons séparés au repos », la flèche E_ℓ entre les deux).
Paramètre sens (?sens= et set_parameters) : separer (défaut) | former.
- separer : moments : noyau_repos, energie_fournie (un faisceau d'énergie peint entre dans le noyau ; la flèche E_ℓ monte), noyau_se_casse
  (les nucléons s'écartent), nucleons_separes (4 nucléons immobiles, loin les uns des autres ; « il a fallu fournir
  E_ℓ = 28,30 MeV »), definition (s'écrit : « E_ℓ : énergie à fournir à un noyau au repos pour le séparer en ses nucléons au
  repos »), fin.
- former : moments : nucleons_separes, nucleons_s_approchent, noyau_forme (l'amas se forme, éclair peint qui sort : « E_ℓ est
  libérée »), masse_diminue (s'écrit : « la masse diminue de Δm : E_ℓ = Δm·c² »), fin.
Paramètre noyau : helium (défaut) | deuterium (²H : E_ℓ = 2,23 MeV) | tritium (³H : 8,48 MeV) — touche sur le noyau = noyau suivant.
Repères : noyau, nucleons, fleche_El, niveau_noyau, niveau_nucleons, energie, definition, vue_noyau, vue_energie.
ce_qui_se_voit : sens, noyau, E_ℓ en MeV, état (lié / séparé), phase.

### aston.html — la courbe d'Aston −E_ℓ/A = f(A)
Une vue « La courbe » : axe x « A (nombre de nucléons) » de 0 à 240 ; axe y « −E_ℓ/A (MeV/nucléon) » de 0 (en haut) à −9 (en bas),
graduations −1 … −9 ; points des noyaux de la liste (petites sphères ombrées, nom ᴬX à côté pour ²H, ⁴He, ¹²C, ⁵⁶Fe, ²³⁵U, et
les autres sans étiquette si la place manque) ; la courbe lisse passe par eux (pic du ⁴He visible) ; le creux vers A ≈ 56–60
(fer, −8,8). Zones peintes légèrement : « fusion » (A < 20, flèche vers le creux), « noyaux stables » (20 < A < 190), « fission »
(A > 190, flèche vers le creux) — bornes approchées, l'écrire « environ ».
Paramètre vue : courbe (défaut) | comparer.
- courbe : moments : axes, points, courbe_tracee, fer (point ⁵⁶Fe entouré, « les plus stables : −E_ℓ/A le plus bas »), plus_stable
  (flèche « plus stable » vers le bas de l'axe y), zone_fusion, zone_fission, zone_stable, fleches (deux flèches vers le creux :
  « fusion » depuis les légers, « fission » depuis les lourds), fin.
- comparer : deux points de lecture (poignées élève qu'on glisse sur la courbe ; coordonnées affichées « A = … ; −E_ℓ/A = …
  MeV/nucléon ») ; préréglage noyau1 = ²H, noyau2 = ³H (set_parameters {noyau1, noyau2} parmi les noyaux de la liste, par
  symbole « H2 », « H3 », « He4 », « C12 », « Fe56 », « Ni60 », « Sr94 », « Xe140 », « U235 »…). Moments : axes, courbe_tracee,
  noyau1, noyau2, comparaison (« le plus stable : celui qui a la plus grande E_ℓ/A, donc le point le plus bas »), fin.
Repères : axe_x, axe_y, courbe, fer, zone_fusion, zone_fission, zone_stable, fleche_fusion, fleche_fission, point_1, point_2,
poignee_1, poignee_2, helium, uranium.
ce_qui_se_voit : vue, axes et unités, ce qui est tracé, coordonnées des points de lecture, le plus stable des deux, phase.

### reactions.html — réaction spontanée, fission, réaction en chaîne, fusion
Paramètre vue (?vue=) : fission (défaut) | chaine | fusion | spontanee.
- spontanee : un noyau ²¹⁰₈₄Po seul, rien ne le touche ; à un instant il émet une particule α (⁴₂He) et devient ²⁰⁶₈₂Pb : « réaction
  spontanée : le noyau se transforme seul (radioactivité) ». Moments : noyau_seul, emission, produits, legende, fin.
- fission : vue « La fission » : un neutron lent (sphère gris-bleu avec traînée) arrive de gauche sur un noyau ²³⁵₉₂U (gros amas) ;
  le noyau s'allonge (en cacahuète), se coupe en deux noyaux moyens ⁹⁴₃₈Sr et ¹⁴⁰₅₄Xe qui s'écartent vite, 2 neutrons partent,
  éclair d'énergie ; l'équation s'écrit en dessous à la craie, terme par terme. Moments : neutron_arrive, choc, noyau_deforme, coupure,
  produits_partent, energie, equation (« ²³⁵₉₂U + ¹₀n → ⁹⁴₃₈Sr + ¹⁴⁰₅₄Xe + 2 ¹₀n »), definition (« La fission : un noyau lourd,
  frappé par un neutron, se scinde en deux noyaux plus légers »), fin.
- chaine : vue « La réaction en chaîne » (qualitative) : 1 fission → 2 neutrons → 2 fissions → 4 neutrons → 4 fissions (petits
  noyaux, arbre qui s'ouvre de gauche à droite), compteur « fissions : 1, 2, 4 ». Moments : premiere_fission, deux_fissions,
  quatre_fissions, legende (« chaque fission libère des neutrons qui provoquent d'autres fissions : réaction en chaîne »), fin.
- fusion : vue « La fusion » : deux noyaux légers ²₁H et ³₁H (petits amas) arrivent l'un vers l'autre ; à basse température ils se
  repoussent (rebond, « ils se repoussent : deux charges positives ») ; on chauffe (thermomètre peint « température très élevée,
  ≈ 10⁸ K ») ; ils se touchent et fusionnent en ⁴₂He + ¹₀n, éclair d'énergie ; équation à la craie. Moments : approche, repulsion,
  chauffage, fusion, produits, energie, equation (« ²₁H + ³₁H → ⁴₂He + ¹₀n »), definition (« La fusion : deux noyaux légers
  s'unissent pour former un noyau plus lourd »), fin.
Paramètre temperature (vue fusion) : basse | haute (poignée : le thermomètre).
Repères : neutron, noyau_uranium, produits, energie, equation, definition, compteur (chaine), deuterium, tritium, helium,
thermometre, noyau_polonium, particule_alpha, vue_fission, vue_chaine, vue_fusion, vue_spontanee (un repère de vue par vue).
ce_qui_se_voit : vue, ce qui se passe (phase), les noyaux présents, l'équation écrite.

### diagramme.html — le diagramme énergétique d'une réaction nucléaire
Vue « Diagramme d'énergie » : axe vertical E (MeV) sans graduation régulière (échelle non respectée : l'écrire) ; trois paliers
horizontaux à la craie, étiquetés à droite, valeurs à gauche ; flèches verticales cotées. Le niveau le plus haut = nucléons séparés.
Paramètre vue (?vue=) : fusion (défaut) | polonium.
- fusion : paliers « 2 ¹₁p + 3 ¹₀n » (en haut), « ²₁H + ³₁H » (milieu), « ⁴₂He + ¹₀n » (en bas). Petites sphères peintes à côté de
  chaque palier (les nucléons séparés, les deux petits noyaux, le noyau d'hélium et le neutron). Moments : axe, niveau_nucleons,
  niveau_reactifs, fleche_El_reactifs (flèche du palier réactifs au palier nucléons : « E_ℓ(²H) + E_ℓ(³H) = 10,841 MeV » ; on
  fournit), niveau_produits, fleche_El_produits (du palier produits au palier nucléons : « E_ℓ(⁴He) = 28,296 MeV » ; on récupère),
  fleche_delta_E (flèche du palier réactifs DESCENDANT au palier produits : « ΔE = 10,841 − 28,296 = −17,455 MeV »), resultat
  (« ΔE < 0 : énergie libérée ; E_lib = |ΔE| ≈ 17,5 MeV » ; « ΔE = Σ E_ℓ(réactifs) − Σ E_ℓ(produits) »), fin.
- polonium (national 2020 N) : paliers « 126 ¹₀n + 84 ¹₁p » 1,971820·10⁵ MeV ; « ²¹⁰₈₄Po » 1,955372·10⁵ MeV ; « ²⁰⁶₈₂Pb + ⁴₂He »
  1,955318·10⁵ MeV. Moments : axe, niveau_nucleons, niveau_reactifs, niveau_produits, fleche_El_reactifs (« E_ℓ(Po) =
  1,971820·10⁵ − 1,955372·10⁵ = 1644,8 MeV »), fleche_delta_E (« ΔE = 1,955318·10⁵ − 1,955372·10⁵ = −5,4 MeV »), resultat
  (« E_lib = |ΔE| = 5,4 MeV »), fin.
Le palier touché (poignée élève) s'entoure et affiche son nom complet.
Repères : axe_E, niveau_nucleons, niveau_reactifs, niveau_produits, fleche_El_reactifs, fleche_El_produits, fleche_delta_E,
resultat, echelle.
ce_qui_se_voit : vue, paliers et valeurs, flèches tracées avec leurs valeurs, signe de ΔE, phase.

### figures.html — figures à étapes (?fig=), comme ondes-lumineuses-tableau/figures.html
Chaque figure s'écrit à la craie, étape par étape (moments = noms des étapes + fin, play_until {moment}). Repère `figure` sur chaque
figure, plus un repère par étape (même nom que l'étape) sur ce qu'elle écrit.
- fig_soleil : le Soleil peint (disque lumineux) qui rayonne ; étapes : soleil (« Le Soleil rayonne de l'énergie depuis des
  milliards d'années »), masse (« Chaque seconde, sa masse diminue d'environ 4 millions de tonnes »), question (« D'où vient cette
  énergie ? »), fin.
- fig_einstein : étapes : relation (« E = m·c² », cadre), termes (E en joule (J), m en kilogramme (kg), c = 3,00·10⁸ m/s),
  exemple (« m = 1 g = 10⁻³ kg → E = 10⁻³ × (3,00·10⁸)² = 9·10¹³ J »), sens (« Toute masse correspond à une énergie : si la masse
  d'un système diminue de Δm, il libère ΔE = Δm·c² »), fin.
- fig_unites : l'escalier des unités ; étapes : u (« 1 u = 1,66·10⁻²⁷ kg : un douzième de la masse d'un atome de carbone 12 »),
  eV (« 1 eV = 1,6·10⁻¹⁹ J »), MeV (« 1 MeV = 10⁶ eV = 1,6·10⁻¹³ J »), MeV_c2 (« MeV/c² : une unité de masse, car m = E/c² »),
  fin.
- fig_931 : démonstration ; étapes : E (« E = m·c² avec m = 1 u = 1,66054·10⁻²⁷ kg »), joule (« E = 1,66054·10⁻²⁷ ×
  (2,99792·10⁸)² = 1,4924·10⁻¹⁰ J »), mev (« E = 1,4924·10⁻¹⁰ / 1,60218·10⁻¹³ = 931,5 MeV »), resultat (« 1 u·c² = 931,5 MeV ;
  donc 1 u = 931,5 MeV/c² »), fin.
- fig_composition : un noyau ᴬ_ZX : Z protons, N = A − Z neutrons, A nucléons ; exemples ⁴₂He (2 p, 2 n), ²³⁵₉₂U (92 p, 143 n).
  Étapes : noyau, protons, neutrons, exemples, fin.
- fig_defaut : étapes : formule (« Δm = Z·m_p + (A − Z)·m_n − m(ᴬ_ZX) »), signe (« Δm > 0 : le noyau est plus léger que ses
  nucléons séparés »), calcul (⁴₂He : « Δm = 2 × 1,00728 + 2 × 1,00866 − 4,00150 = 0,03038 u »), kg (« Δm = 0,03038 × 1,66·10⁻²⁷
  = 5,04·10⁻²⁹ kg »), fin.
- fig_liaison : étapes : formule (« E_ℓ = Δm·c² »), calcul (« E_ℓ = 0,03038 u × 931,5 MeV/u = 28,30 MeV »), par_nucleon (« E_ℓ/A
  = 28,30 / 4 = 7,07 MeV/nucléon »), joule (« E_ℓ = 28,30 × 1,6·10⁻¹³ = 4,53·10⁻¹² J »), fin.
- fig_stabilite : tableau deux noyaux ⁶⁰Ni et ⁵⁶Ni (national 2017 R) ; étapes : trace, calcul (« E_ℓ(⁶⁰Ni)/A = 526,8 / 60 =
  8,78 MeV/nucléon »), compare (« 8,78 > 8,64 »), conclusion (« ⁶⁰Ni est plus stable : la plus grande énergie de liaison par
  nucléon »), piege (« ⚠ comparer E_ℓ/A, jamais E_ℓ »), fin.
- fig_spontanee_provoquee : tableau « Réaction spontanée (radioactivité α, β⁻, β⁺) » | « Réaction provoquée (fission, fusion) » ;
  étapes : trace, spontanee (« le noyau se transforme seul »), provoquee (« il faut un neutron (fission) ou une température très
  élevée (fusion) »), soddy (« dans toutes : conservation de A et conservation de Z (lois de Soddy) »), fin.
- fig_soddy : trouver x neutrons : « ²³⁵₉₂U + ¹₀n → ⁹⁴₃₈Sr + ¹⁴⁰₅₄Xe + x ¹₀n » ; étapes : equation, A (« 235 + 1 = 94 + 140 + x
  donc x = 2 »), Z (« 92 + 0 = 38 + 54 + 0 : vérifié »), fin.
- fig_methode_masses : quatre lignes ; étapes : equation (l'équation de la réaction, toutes les particules), delta_m (« Δm =
  Σm(produits) − Σm(réactifs) »), delta_E (« ΔE = Δm·c² (Δm en u × 931,5 → MeV) »), E_lib (« ΔE < 0 : E_lib = |ΔE| »), fin.
- fig_methode_liaison : étapes : formule (« ΔE = Σ E_ℓ(réactifs) − Σ E_ℓ(produits) »), A_fois (« E_ℓ = A·(E_ℓ/A) pour chaque
  noyau »), nucleon_libre (« un nucléon seul (¹₀n, ¹₁p) : E_ℓ = 0 »), E_lib (« E_lib = |ΔE| »), fin.
- fig_echantillon : étapes : un_noyau (« fission d'un noyau d'²³⁵U : E_lib ≈ 185 MeV »), nombre (« dans m = 1 g : N = m·N_A/M =
  1 × 6,02·10²³ / 235 = 2,56·10²¹ noyaux »), total (« E = N·E_lib = 2,56·10²¹ × 185 = 4,7·10²³ MeV »), joule (« E = 4,7·10²³ ×
  1,6·10⁻¹³ = 7,6·10¹⁰ J »), petrole (« ≈ l'énergie de la combustion de 1,8 tonne de pétrole »), fin.
- fig_comparaison : tableau « Fission de l'²³⁵U » | « Fusion ²H + ³H » ; étapes : trace, par_reaction (185 MeV | 17,6 MeV),
  par_nucleon (185 / 236 ≈ 0,78 MeV | 17,6 / 5 ≈ 3,5 MeV), conclusion (« à masse égale, la fusion libère plus d'énergie que la
  fission »), fin.
- fig_cas_types : tableau « Le mot de la question → la méthode » ; étapes (une ligne chacune) : trace, liaison (« énergie de
  liaison d'un noyau » → Δm = Z·m_p + (A − Z)·m_n − m, E_ℓ = Δm·c²), stabilite (« le plus stable » → comparer E_ℓ/A), masses
  (« énergie libérée, masses données » → Δm = Σm(produits) − Σm(réactifs), E_lib = |ΔE|), energies (« tableau d'E_ℓ » →
  ΔE = Σ E_ℓ(réactifs) − Σ E_ℓ(produits)), diagramme (« diagramme d'énergie » → lire les paliers), echantillon (« énergie d'un
  échantillon, de m grammes » → N = m·N_A/M, E = N·E_lib), equation (« déterminer A et Z, x neutrons » → lois de Soddy), fin.
- fig_enonce_2016 : énoncé type national 2016 N (fusion ²₁H + ³₁H → ᴬ_ZHe + ¹₀n ; données : m(²H) = 2,01355 u ; m(³H) =
  3,01550 u ; m(He) = 4,00150 u ; m(n) = 1,00866 u ; 1 u = 931,5 MeV/c²). Étapes : trace, donnees, fin.
- fig_enonce_2017 : national 2017 R : ⁶⁰₂₇Co → ⁶⁰₂₈Ni + X ; m(Co) = 59,91901 u ; m(Ni) = 59,91543 u ; m(e) = 0,00055 u ;
  m_p = 1,00728 u ; m_n = 1,00866 u ; E_ℓ/A(⁵⁶Ni) = 8,64 MeV/nucléon. Étapes : trace, donnees, fin.
- fig_enonce_2023 : national 2023 N : tableau E_ℓ (MeV) ²H 2,366 ; ³H 8,475 ; ⁴He 28,296 ; réaction ³₁H + ²₁H → ⁴₂He + ¹₀n.
  Étapes : trace, donnees, fin.
- fig_enonce_2025 : national 2025 N : ¹⁰⁷₄₈Cd → ¹⁰⁷₄₇Ag + ⁰₁e ; m(Cd) = 106,88045 u ; m(Ag) = 106,87947 u ; m(e) = 5,486·10⁻⁴ u ;
  1 u = 931,49 MeV/c² ; nombre de noyaux désintégrés entre t₁ et t₂ : N_d ≈ 5,62·10¹⁵. Étapes : trace, donnees, fin.

### bilan.html et carte.html — même forme que ondes-lumineuses-tableau/bilan.html et carte.html (imprimer.js, acquis)
bilan.html : la fiche « Ce qu'il faut retenir » sur UNE page (deux au plus), page 2 = la page de l'élève (lacunes, acquis,
acquis_ids reçus par set_parameters). Blocs (id, titre, définition mot pour mot, formule encadrée, piège orange « ⚠ », comps) :
1 masse_energie (C1) : E = m·c² ; 1 u = 1,66·10⁻²⁷ kg = 931,5 MeV/c² ; 1 MeV = 1,6·10⁻¹³ J ; ⚠ Δm en u × 931,5 → MeV.
2 defaut (C2) : « La masse d'un noyau est inférieure à la somme des masses de ses nucléons séparés. » ; Δm = Z·m_p + (A − Z)·m_n − m(ᴬ_ZX) ;
  ⚠ Δm > 0 ; N = A − Z.
3 liaison (C3) : « L'énergie de liaison E_ℓ est l'énergie qu'il faut fournir à un noyau au repos pour le séparer en ses nucléons au
  repos. » ; E_ℓ = Δm·c² ; E_ℓ/A en MeV/nucléon.
4 stabilite (C4) : « Un noyau est d'autant plus stable que son énergie de liaison par nucléon E_ℓ/A est grande. » ; courbe d'Aston
  −E_ℓ/A = f(A) : creux vers le fer (A ≈ 56) ; ⚠ comparer E_ℓ/A, pas E_ℓ.
5 reactions (C5) : fission : un noyau lourd frappé par un neutron se scinde en deux noyaux plus légers ; fusion : deux noyaux légers
  s'unissent en un noyau plus lourd ; conservation de A et de Z ; ⚠ ne pas oublier les neutrons.
6 bilan_masses (C6) : Δm = Σm(produits) − Σm(réactifs) ; ΔE = Δm·c² ; E_lib = |ΔE| ; ⚠ toutes les particules (e⁻, e⁺, n) entrent dans Δm.
7 bilan_liaison (C7) : ΔE = Σ E_ℓ(réactifs) − Σ E_ℓ(produits) ; diagramme : nucléons séparés en haut ; ⚠ E_ℓ = A·(E_ℓ/A).
8 echantillon (C8) : N = m·N_A/M ; E = N·E_lib ; à masse égale, la fusion libère plus que la fission ; ⚠ m en g si M en g/mol.
Moments : fiche, masse_energie, defaut, liaison, stabilite, reactions, bilan_masses, bilan_liaison, echantillon, lacunes.
carte.html : au centre « Noyaux, masse et énergie » (« la masse peut devenir énergie : E = m·c² »), 8 branches dessinées une à une :
masse_energie (E = m·c², u, MeV), defaut (Δm > 0), liaison (E_ℓ = Δm·c², E_ℓ/A), stabilite (courbe d'Aston, fer), reactions (fission,
fusion, Soddy), bilan_masses (Δm, E_lib = |ΔE|), bilan_liaison (Σ E_ℓ, diagramme), echantillon (N = m·N_A/M, E = N·E_lib).
Moments : definition + les 8 ids de branche + fin. Le même drapeau acquis entoure les branches à reprendre (comps : masse_energie C1,
defaut C2, liaison C3, stabilite C4, reactions C5, bilan_masses C6, bilan_liaison C7, echantillon C8 ; C9 « rédiger » : aucune
branche propre, montrée sur la page 2 du bilan). Tout dans 760 × 420. Bouton « 🖨️ Imprimer / PDF » sur les deux.
Compétences du cours (pour la page de l'élève) : C1 Utiliser E = m·c² et convertir les unités ; C2 Calculer le défaut de masse d'un
noyau ; C3 Calculer l'énergie de liaison et l'énergie de liaison par nucléon ; C4 Comparer la stabilité de noyaux, lire la courbe
d'Aston ; C5 Reconnaître et écrire une fission et une fusion ; C6 Calculer l'énergie libérée à partir des masses ; C7 Calculer
l'énergie libérée à partir des énergies de liaison, exploiter un diagramme énergétique ; C8 Calculer l'énergie libérée par un
échantillon et comparer ; C9 Rédiger comme le barème.
