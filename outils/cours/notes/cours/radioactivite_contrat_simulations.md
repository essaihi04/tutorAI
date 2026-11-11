# Contrat des simulations — cours « Décroissance radioactive » (phys_ch4_radioactivite)

Dépôt : C:\Users\HP\Desktop\ai-tutor-bac (partagé : d'autres sessions y travaillent en parallèle, dont un agent qui fait
energie_nucleaire dans son propre dossier). Dossier à remplir : frontend/public/media/simulations/physics/radioactivite-tableau/
Déjà présents (ne les modifie pas ; si un changement est indispensable, ne casse pas les autres pages) :
- commun.js (window.OndesTableau.Scene : cadre virtuel 760 × 420, cadre()/local(), image()) ; exposants.js (10⁻³ à la craie) ;
  radio.css (fond transparent, barre en haut, bas libre) — copies du cours ondes_lumineuses ;
- **noyaux.js** : notation des noyaux à la craie. `craie.nucleide('U', 238, 92, x, y, o)`, `craie.noyaux('[238,92]U → [234,90]Th + [4,2]He', x, y, o)`
  (texte libre entre les [A,Z]Symbole, `o.align: 'center'` possible), `craie.largeurNoyaux(s, taille)`. ÉCRIS TOUS LES NOYAUX AVEC CE MODULE
  (A en haut à gauche, Z en bas à gauche), jamais « U-238 » ni « 238U » collés. Électron [0,-1]e, positon [0,1]e, hélium [4,2]He,
  neutron [1,0]n, proton [1,1]p.

## Lire d'abord (par extraits si gros)
- .agents/skills/simulations-au-tableau/SKILL.md (À SUIVRE À LA LETTRE), docs/design/labos-au-tableau.md
- le kit : frontend/public/media/simulations/shared/tableau/tableau.js, tableau.css, imprimer.js
- modèles (forme seulement, ne les modifie pas) : physics/ondes-lumineuses-tableau/ (diffraction.html : protocole, moments, play_until,
  repères, explication, ?vue= ; courbe.html : courbe point par point, pente ; figures.html : figures à étapes ?fig= ; bilan.html ; carte.html)
  et physics/ondes-tableau/ballon.html pour le rendu « réel ».

## Règles communes
- Chaque page : `<link>` /media/simulations/shared/tableau/tableau.css + radio.css ; scripts /media/simulations/shared/tableau/tableau.js,
  commun.js, exposants.js, noyaux.js, puis le script de la page, puis `<script src="/media/simulations/professor-locate.js" defer>`.
- Fond transparent, cadre virtuel 760 × 420, rien de coupé, pas de défilement, barre (bouton + bulle) EN HAUT, bas libre (4.5em). UN bouton
  principal qui cycle (Lancer → Pause → Reprendre → Rejouer) avec data-professor-control ; réglages = poignées glissées (Tableau.glisser).
- `Tableau.protocole({ id, commandes, config, texte, etat, progression, executer })` ; commandes : start, reset, pause, resume,
  set_time {time_s}, set_parameters {…} (schéma avec plages et pas), play_until {moment | time_s} (rejoue depuis 0 si l'instant est passé,
  sinon continue, puis se fige avec « Arrêt sur image : … » dans la bulle). highlight {target} est ajouté par le kit.
- État : simulation_status, ce_qui_se_voit (phrase française qui dit TOUT ce qu'on voit : vues, valeurs avec unités, phase en cours),
  current_variant, time_s, parameters, moments (nom → instant en s DE LA SIMULATION, recalculés quand un paramètre change), derniere_main.
  Émis à chaque événement et toutes les 500 ms pendant que ça tourne. Le moment `fin` existe partout.
- Repères `craie.repere(id, x, y, w, h, 'libellé')` pour TOUS les ids listés (noms exacts), et `Tableau.explication({ <vue>: [{ repere, texte }] })`.
- Une scène figée dessine encore ce qui bouge (running || pause). Rendu à la demande.
- Apostrophe typographique ’ dans toute chaîne JS en français (ou backticks). Déclarer la scène avant la boucle.
- Rendu « réel » (règle 7) : les noyaux sont des grappes de petites sphères ombrées (protons rouge-orangé, neutrons gris-bleu clair, dégradé
  radial + reflet), la particule α une petite grappe 2 + 2 qui part vite, l'électron β⁻ une petite sphère bleue avec « e⁻ » à la craie,
  le positon β⁺ une petite sphère jaune-orangé avec « e⁺ », le rayonnement γ une onde lumineuse peinte (sinusoïde violette brillante + halo).
  Un échantillon = une fiole/un petit tas peint ; un noyau qui se désintègre fait un petit éclair bref. Compteur Geiger peint (boîtier,
  tube, aiguille ou chiffres), le « clic » est visuel (petit éclat). La craie : lettres, axes, cotes, flèches, équations. Le peint ne
  change jamais la physique. Légère, une boucle, pas de calcul pixel par pixel.
- Texte du tableau en français. Indices jamais avec « _ » visible (Craie.segments rend t_1/2 ? NON : écris la demi-vie « t½ » ou « t₁/₂ »
  — choisis « t½ » partout, plus lisible à la craie), N₀ (« N_0 » rendu en indice par le kit), a₀, λ, τ, e^(−λt) écrit « e^{−λt} »
  (exposants.js), ln.
- MOTS INTERDITS (dessin, ce_qui_se_voit, explications) : interaction forte, interaction faible, quark, gluon, capture électronique,
  neutrino, antineutrino, section efficace, modèle en couches, nombres magiques, goutte liquide, effet tunnel, Gamow, spin, Bateman,
  équilibre séculaire, sievert, gray, dose absorbée, Poisson, fluctuation, isochrone, vie moyenne, énergie de liaison, défaut de masse,
  fission, fusion, MeV (l'énergie est le chapitre suivant : n'en parle pas).
- Formules écrites seulement : N = A − Z ; A = A₁ + A₂ et Z = Z₁ + Z₂ (lois de Soddy) ; ¹₀n → ¹₁p + ⁰₋₁e ; ¹₁p → ¹₀n + ⁰₁e ;
  N(t) = N₀·e^{−λt} ; dN = −λ·N·dt ; dN/dt + λ·N = 0 ; τ = 1/λ ; t½ = ln2/λ ; t½ = τ·ln2 ; N(t½) = N₀/2 ; N = N₀/2ⁿ (t = n·t½) ;
  N_d = N₀ − N(t) = N₀(1 − e^{−λt}) ; a = −dN/dt ; a = λ·N ; a₀ = λ·N₀ ; a(t) = a₀·e^{−λt} ; N = (m/M)·N_A ; ln N = ln N₀ − λ·t ;
  ln a = ln a₀ − λ·t ; t = (1/λ)·ln(a₀/a) ; t = (1/λ)·ln(N₀/N) ; t = (t½/ln2)·ln(a₀/a) ; r = N(fils)/N(père) = e^{λt} − 1 ;
  1 Bq = 1 désintégration par seconde ; et des applications numériques.
- Valeurs de référence (exactes, utilise-les) : ²³⁸₉₂U (t½ = 4,5·10⁹ ans) ; ¹⁴₆C → ¹⁴₇N + β⁻ (t½ = 5730 ans) ; ¹²₆C stable ;
  ²¹⁰₈₄Po → ²⁰⁶₈₂Pb + α (t½ = 138 jours) ; ³²₁₅P → ³²₁₆S + β⁻ (t½ = 14,3 jours) ; ¹³¹₅₃I → ¹³¹₅₄Xe + β⁻ (t½ = 8 jours) ;
  ³⁰₁₅P → ³⁰₁₄Si + β⁺ ; ¹⁰⁷₄₈Cd → ¹⁰⁷₄₇Ag + β⁺ + γ ; ⁶⁰₂₇Co → ⁶⁰₂₈Ni + β⁻ (+ γ) ; ²²⁶₈₈Ra → ²²²₈₆Rn + α ; ²³⁸₉₄Pu → ²³⁴₉₂U + α (t½ = 88 ans) ;
  ²²²₈₆Rn → ²¹⁸₈₄Po + α (t½ = 3,8 jours) ; ¹₁H, ²₁H, ³₁H ; ²³⁸₉₂U → ²⁰⁶₈₂Pb : 8 α et 6 β⁻. N_A = 6,02·10²³ mol⁻¹. 1 an = 3,16·10⁷ s.
- Noms de moments, de repères, de paramètres et de vues : EXACTEMENT ceux de ta fiche. Tu peux en ajouter, jamais en renommer.
- Interdits : ne modifie rien hors de ce dossier (pas frontend/src, pas backend, pas le kit shared/, pas les autres cours) ; aucun
  commit/push/stash/reset/checkout ; aucune voix ; ne lis aucun fichier d'identifiants ; ne te connecte à aucun site ; pas de sous-agent.
- Vérification obligatoire : extraire chaque bloc <script> inline et `node --check` ; relire les libellés aux positions extrêmes des poignées.
  Test navigateur : serveur statique local sur frontend/public (`python -m http.server <port libre 8900-8999> --bind 127.0.0.1` en arrière-plan,
  arrêté à la fin), Playwright (python) avec Chrome `C:/Program Files/Google/Chrome/Application/chrome.exe` `--headless=new` : aucune erreur JS,
  encre sur le canvas, bouton présent, `window.__horsCadre` vide ; pilote par postMessage {type:'simulation_control', command, parameters} et
  relis le dernier `simulation_state` (current_state) : chaque moment de ta fiche existe et `play_until` s'y fige, chaque repère existe
  (`Tableau.listeReperes()`), les nombres sont justes.
- Rapport final (court) : fichiers créés, moments réels (nom → s) par vue, repères, paramètres acceptés, écarts avec la fiche, résultats.

## Fiches

### noyau.html — de l'atome au noyau, la notation, les isotopes
Vues ?vue= :
- atome (défaut) : un atome peint (nuage d'électrons léger), zoom sur le noyau (grappe de sphères), protons et neutrons séparés et comptés.
  Exemple ¹⁴₆C. Moments : atome, zoom_noyau, protons (6 protons s'allument, « Z = 6 protons »), neutrons (8 neutrons, « N = 8 neutrons »),
  nucleons (« A = 14 nucléons : protons + neutrons »), fin.
- notation : la notation ᴬ_Z X s'écrit lettre par lettre avec ses flèches : X symbole, A nombre de masse (nombre de nucléons), Z numéro
  atomique, nombre de charge (nombre de protons), puis N = A − Z. Exemple ²³⁸₉₂U : N = 238 − 92 = 146. Moments : symbole, nombre_A, nombre_Z,
  formule_N, exemple_U, fin. Paramètre noyau (pastille touchée = suivant) : U238 | C14 | Ir192 (Z = 77, N = 115) | Co60.
- isotopes : trois noyaux d'hydrogène ¹₁H, ²₁H, ³₁H peints côte à côte (1 proton chacun, 0/1/2 neutrons), puis ¹²₆C et ¹⁴₆C.
  Moments : hydrogene, meme_Z (« même Z : même élément »), A_different (« A différents : neutrons différents »), carbone, definition
  (« Isotopes : noyaux de même Z et de A différents »), fin.
Repères : atome, noyau, proton, neutron, symbole, A, Z, N, formule_N, isotope_1, isotope_2, isotope_3, carbone_12, carbone_14,
vue_atome, vue_notation, vue_isotopes.

### segre.html — le diagramme (N, Z), la vallée de stabilité, les zones, la famille
Axes : Z en abscisse (0 → 100), N en ordonnée (0 → 150), noms ET graduations ; la droite N = Z en pointillé ; la vallée de stabilité peinte
(bande sombre de petits carrés « stables » qui suit N ≈ Z pour Z < 20 puis s'écarte au-dessus, jusqu'à ²⁰⁸₈₂Pb ; forme réaliste) ; les
noyaux instables en couleur selon la zone : au-dessus de la vallée (trop de neutrons) bleu → β⁻ ; au-dessous (trop de protons) orange → β⁺ ;
noyaux lourds (A > 200 environ, Z > 82) jaune → α. Poignée élève : un noyau-curseur qu'on fait glisser ; la bulle donne Z, N, A, la zone et
le type prévu.
Vues ?vue= :
- vallee (défaut) : moments axes, droite_N_egal_Z, vallee (la bande se peint), legers (« noyaux légers stables : N ≈ Z »), lourds
  (« noyaux lourds stables : N > Z »), fin.
- zones : moments vallee, zone_beta_moins (zone bleue + « excès de neutrons → β⁻ »), zone_beta_plus (zone orange + « excès de protons → β⁺ »),
  zone_alpha (zone jaune + « noyaux lourds → α »), fleches (trois flèches de déplacement depuis un même noyau : β⁻ vers (Z+1, N−1),
  β⁺ vers (Z−1, N+1), α vers (Z−2, N−2), chacune étiquetée), fin.
- isotopes : moments vallee, ligne_isotopes (une ligne VERTICALE à Z = 6 : ¹²C stable dans la vallée, ¹⁴C au-dessus → β⁻ ; texte
  « isotopes : même Z, sur une ligne perpendiculaire à l'axe des Z »), fin.
- famille : la famille de l'uranium 238 jusqu'au plomb 206 dessinée flèche par flèche sur un zoom du diagramme (Z 80 → 93, N 122 → 147) :
  ²³⁸U →α ²³⁴Th →β⁻ ²³⁴Pa →β⁻ ²³⁴U →α ²³⁰Th →α ²²⁶Ra →α ²²²Rn →α ²¹⁸Po →α ²¹⁴Pb →β⁻ ²¹⁴Bi →β⁻ ²¹⁴Po →α ²¹⁰Pb →β⁻ ²¹⁰Bi →β⁻ ²¹⁰Po →α ²⁰⁶Pb.
  Compteurs « α : n » et « β⁻ : n » qui montent. Moments : depart, premiere_alpha, premiere_beta, milieu (après ²²²Rn), arrivee (²⁰⁶Pb
  stable), bilan (« 8 α et 6 β⁻ »), fin.
- famille2024 : schéma type national 2024 R (axes A en ordonnée et Z en abscisse, quelques nucléides de la famille du thorium : ²¹²₈₄Po,
  ²¹²₈₃Bi, ²⁰⁸₈₁Tl, ²¹²₈₂Pb, X = ²⁰⁸₈₂Pb, flèches numérotées (1) ²¹²Bi(83) → ²¹²Po(84) β⁻, (2) ²¹²Bi → ²⁰⁸Tl α). Moments : trace, fleche_1
  (« A ne change pas, Z augmente de 1 : β⁻ »), fleche_2 (« A diminue de 4, Z de 2 : α »), nucleide_X, fin.
Paramètres : vue, noyau_Z 1..100 et noyau_N 0..150 (le curseur).
Repères : axe_Z, axe_N, droite_N_Z, vallee, zone_beta_moins, zone_beta_plus, zone_alpha, curseur, fleche_alpha, fleche_beta_moins,
fleche_beta_plus, ligne_isotopes, carbone_12, carbone_14, uranium_238, plomb_206, compteur_alpha, compteur_beta, fleche_1, fleche_2,
nucleide_X, vue_diagramme.
ce_qui_se_voit : vue, axes, ce qui est peint, la position du curseur (Z, N, A, zone, type prévu), les compteurs, la phase.

### desintegration.html — un noyau se désintègre : α, β⁻, β⁺, γ, et les lois de Soddy
Une vue « Le noyau » (à gauche, peint : noyau père qui tremble, puis éclate en noyau fils + particule qui part) et une vue « L'équation »
(à droite, à la craie : l'équation s'écrit avec noyaux.js, puis les deux lignes de Soddy : « A : 210 = 206 + 4 » et « Z : 84 = 82 + 2 »
cochées). Paramètre type (?type= et set_parameters, pastille touchée = suivant) :
- alpha (défaut) : ²¹⁰₈₄Po → ²⁰⁶₈₂Pb + ⁴₂He. Moments : noyau_pere, emission (la particule α part), noyau_fils, equation, soddy_A, soddy_Z,
  conclusion (« désintégration α : émission d'un noyau d'hélium ⁴₂He »), fin.
- beta_moins : ¹⁴₆C → ¹⁴₇N + ⁰₋₁e. En plus, dans le noyau, un neutron devient proton : petite ligne « ¹₀n → ¹₁p + ⁰₋₁e ». Mêmes moments +
  transformation (le neutron change de couleur et l'électron sort) entre noyau_pere et emission.
- beta_plus : ³⁰₁₅P → ³⁰₁₄Si + ⁰₁e ; « ¹₁p → ¹₀n + ⁰₁e ». Mêmes moments que beta_moins.
- gamma : ⁶⁰₂₇Co → ⁶⁰₂₈Ni* + ⁰₋₁e puis ⁶⁰₂₈Ni* → ⁶⁰₂₈Ni + γ (le noyau fils excité, marqué *, brille puis émet l'onde γ et se calme).
  Moments : noyau_pere, emission, noyau_excite, emission_gamma, equation, conclusion (« γ : A et Z ne changent pas »), fin.
- soddy : équation générale ᴬ_Z X → ᴬ¹_Z¹ Y + ᴬ²_Z² x écrite à la craie, puis A = A₁ + A₂ (« conservation du nombre de nucléons ») et
  Z = Z₁ + Z₂ (« conservation du nombre de charge »). Moments : pere, fils, particule, loi_A, loi_Z, fin.
- inconnu : exercice type national 2021 R : ³²₁₅P → ᴬ_Z X + ⁰₋₁e ; le tableau des symboles (Z 13 Al, 14 Si, 15 P, 16 S) ; les lignes
  « 32 = A + 0 ⇒ A = 32 », « 15 = Z − 1 ⇒ Z = 16 », X = S entouré dans le tableau. Moments : equation, ligne_A, ligne_Z, tableau, fils, fin.
Repères : noyau_pere, noyau_fils, particule, equation, soddy_A, soddy_Z, transformation, gamma, tableau_Z, vue_noyau, vue_equation.
ce_qui_se_voit : type, l'équation écrite, A et Z de chaque côté, ce qui sort, la phase.

### population.html — beaucoup de noyaux : le hasard, la loi, la demi-vie
Deux vues : « L'échantillon » (à gauche : une grille de N₀ noyaux peints, petites sphères ; un noyau désintégré devient un noyau fils d'une
autre couleur après un petit éclair ; compteur « N = … noyaux restants ») et « La courbe » (à droite : axes « t (jours) » et
« N (noyaux) », la courbe N(t) se trace en direct avec la simulation, points). Le tirage est aléatoire mais avec une graine fixée par vue
(reproductible) ; la courbe théorique N₀·e^{−λt} peut s'afficher en pointillé (moment loi).
Iode 131 : t½ = 8 jours. Le temps de la simulation : 1 jour simulé = 0,25 s réelles (affiché « t = … jours »).
Vues ?vue= :
- hasard (défaut) : N₀ = 12 gros noyaux ; on ne sait pas lequel part : la bulle le dit. Moments : depart, premier (le premier se
  désintègre : pas celui qu'on attendait — un noyau au hasard), deuxieme, plusieurs, fin. Variante : set_parameters {graine} → autre ordre.
- grand_nombre : N₀ = 400. Moments : depart, un_t_demi (t = 8 j : N = 200, cote « N₀/2 »), deux_t_demi (16 j : 100, « N₀/4 »),
  trois_t_demi (24 j : 50, « N₀/8 »), loi (la courbe théorique en pointillé + « N(t) = N₀·e^{−λt} »), fin (t = 40 j). Les nombres affichés
  aux paliers sont EXACTEMENT 200, 100, 50 (le tirage est guidé pour coller à la loi aux paliers, le dire en commentaire).
- proportion : N₀ = 400 ; tableau à la craie « Δt = 1 jour : N avant | désintégrés | proportion » sur trois lignes : la proportion reste
  ≈ 0,083 = λ·Δt. Moments : depart, ligne_1, ligne_2, ligne_3, conclusion (« la même proportion par unité de temps : λ »), fin.
- restants : N₀ = 400 ; deux courbes : N(t) restants (décroît) et N_d(t) désintégrés (croît), qui se croisent à t½. Moments : depart,
  croisement (t = 8 j, 200 et 200), deux_t_demi (100 restants, 300 désintégrés : « 75 % désintégrés »), formule (« N_d = N₀ − N(t) »), fin.
Paramètres : vue, t_demi_j 2..20 pas 1 (poignée sur l'axe du temps : la courbe et les paliers se recalculent), graine.
Repères : echantillon, noyau_desintegre, compteur, courbe, axe_t, axe_N, palier_1, palier_2, palier_3, N0, N0_sur_2, t_demi, loi,
tableau, courbe_restants, courbe_desintegres, croisement, vue_echantillon, vue_courbe.
ce_qui_se_voit : vue, t en jours, N restants, désintégrés, t½, palier atteint, ce que dit la bulle.

### courbe.html — lire une courbe de décroissance
Une vue « La courbe » (axes avec noms ET unités, courbe à la craie, lectures en pointillé) et, à droite, une colonne « Lecture » qui
s'écrit. Paramètre courbe (?courbe= et set_parameters {courbe}) :
- N (défaut) : N(t) = N₀·e^{−λt}, N₀ = 8,0·10²⁰ noyaux (écrit « N₀ »), t½ = 8 jours, axe t 0 → 40 jours. Moments : axes, courbe,
  N0 (N₀ lu sur l'axe), moitie (N₀/2 sur l'axe, pointillé horizontal jusqu'à la courbe puis vertical vers t), t_demi (« t½ = 8 jours »),
  tangente (tangente à l'origine tracée, elle coupe l'axe des temps en τ = t½/ln2 = 11,5 jours), tau (« τ = 1/λ = 11,5 jours »), fin.
- paliers : même courbe ; N₀ → N₀/2 → N₀/4 → N₀/8 aux dates t½, 2t½, 3t½ (escalier en pointillé). Moments : axes, courbe, palier_1,
  palier_2, palier_3, formule (« t = n·t½ : N = N₀/2ⁿ »), fin.
- ln : droite ln N = f(t), national 2021 R : ln N de 33 à t = 0 à 23,3 à t = 200 jours ; axe « t (jours) », « ln N ». Moments : axes,
  droite, ordonnee (ln N₀ = 33), pente (triangle : k = (23,3 − 33)/(200 − 0) = −0,0485 jour⁻¹), identification (« ln N = ln N₀ − λ·t donc
  λ = −k = 0,0485 jour⁻¹ »), fin.
- activite_2021 : a(t) du national 2021 N : a₀ = 1,0·10¹¹ Bq, t½ = 88 ans, axe 0 → 300 ans, « a (10¹⁰ Bq) ». Moments : axes, courbe, a0,
  moitie, t_demi (« t½ = 88 ans »), fin.
- activite_2022 : a(t) du national 2022 N : a₀ = 4·10⁶ Bq, t½ = 8 jours, axe 0 → 40 jours, « a (10⁶ Bq) ». Mêmes moments.
Poignée élève : un point de lecture qu'on fait glisser sur la courbe (coordonnées affichées avec les unités).
Repères : axe_t, axe_N (ou axe_a, axe_ln), courbe, N0, a0, moitie, t_demi, tangente, tau, palier_1, palier_2, palier_3, droite, ordonnee,
pente, identification, point_lu, lecture.
ce_qui_se_voit : courbe, unités des axes, lectures faites (valeurs + unités), point lu, conclusion.

### activite.html — le compteur Geiger : l'activité
Une vue « L'échantillon et le compteur » (fiole peinte de phosphore 32 ou d'iode 131, tube du compteur Geiger devant, petits éclats à
chaque désintégration détectée, affichage « désintégrations en 1 s ») et une vue « a(t) » (petit graphe qui reçoit un point par mesure).
Moments : echantillon, compteur, une_seconde (on compte pendant 1 s : « a = 400 désintégrations par seconde = 400 Bq »), definition
(« activité a : nombre de désintégrations par seconde ; 1 Bq = 1 désintégration par seconde »), plus_tard (on avance de t½ : « a = 200 Bq »),
proportionnelle (« a = λ·N : moitié des noyaux, moitié de l'activité »), fin. Valeurs : activité de départ 400 Bq, t½ = 8 jours (iode 131).
Paramètre t_j 0..40 (poignée : le calendrier ; a = 400·2^{−t/8} affiché).
Repères : echantillon, compteur, affichage, definition, graphe_a, point_a, vue_compteur, vue_graphe.

### datation.html — dater un objet au carbone 14
Trois temps peints : un arbre vivant (échanges avec l'air : flèches CO₂ ; « vivant : la proportion de ¹⁴C reste constante, a₀ ») → l'arbre
coupé (« mort : plus d'échanges, le ¹⁴C se désintègre ») → un morceau de bois ancien mesuré (compteur : a = 318 Bq ; bois récent de même
masse : a₀ = 418 Bq). À droite, la colonne « Calcul » s'écrit : a = a₀·e^{−λt} ; t = (1/λ)·ln(a₀/a) ; λ = ln2/t½ ; t = (t½/ln2)·ln(a₀/a) ;
t = (5730/0,693)·ln(418/318) ≈ 2,26·10³ ans (national 2022 R).
Moments : vivant, echanges, mort, desintegration, mesure, formule, application, resultat, fin.
Paramètre a_Bq 100..418 (poignée : l'activité mesurée ; l'âge recalculé et affiché).
Repères : arbre, air, bois_ancien, compteur, a0, a, formule, application, resultat, vue_temps, vue_calcul.

### figures.html — figures à étapes (?fig=), comme ondes-lumineuses-tableau/figures.html
Chaque figure s'écrit à la craie, étape par étape (moments = noms des étapes, play_until {moment}), repère `figure` + un repère par étape.
- fig_soddy_systeme : national 2012 N : ²³⁸₉₂U → ²⁰⁶₈₂Pb + x ⁰₋₁e + y ⁴₂He. Étapes : equation, systeme (« Lois de Soddy : 238 = 206 + 0·x + 4y ;
  92 = 82 − x + 2y »), y (« y = (238 − 206)/4 = 8 »), x (« x = 82 + 2y − 92 = 6 »), conclusion (« 8 désintégrations α et 6 désintégrations β⁻ »), fin.
- fig_rappel_exp_ln : rappel de maths : e⁰ = 1 ; e^{−x} décroît ; ln(e^x) = x ; ln(1/2) = −ln2 ; ln2 ≈ 0,693 ; « ln enlève e ». Étapes :
  exp, decroit, ln, ln_demi, valeur, fin.
- fig_equation_diff : Étapes : pendant (« pendant dt : dN noyaux désintégrés, proportionnels à N et à dt »), relation (« dN = −λ·N·dt »,
  le signe moins : N diminue), equation (« dN/dt + λ·N = 0 »), solution (« N(t) = N₀·e^{−λt} »), verification (« dN/dt = −λ·N₀·e^{−λt} = −λ·N »), fin.
- fig_demo_t_demi : Étapes : loi (N(t) = N₀·e^{−λt}), condition (« à t = t½ : N(t½) = N₀/2 »), egalite (N₀·e^{−λt½} = N₀/2, N₀ barrés),
  ln (−λ·t½ = ln(1/2) = −ln2), resultat (t½ = ln2/λ encadré ; t½ = τ·ln2), fin.
- fig_unites : « λ et t½ : la même unité de temps » ; Étapes : trace (s, min, h, jour, an), conversion (138 jours = 138 × 24 × 3600 s =
  1,19·10⁷ s), bq (« a en Bq : λ en s⁻¹ »), fin.
- fig_masse_N : Étapes : quantite (n = m/M), nombre (N = n·N_A = (m/M)·N_A), exemple (national 2023 N : m₀ = 2 µg = 2·10⁻⁶ g de tritium,
  M = 3 g/mol → N₀ = 4,0·10¹⁷), piege (« m en g, comme M en g/mol »), fin.
- fig_activite_demo : Étapes : definition (a = −dN/dt), derivee (a = −d(N₀·e^{−λt})/dt = λ·N₀·e^{−λt}), resultat (a = λ·N ; a₀ = λ·N₀ ;
  a(t) = a₀·e^{−λt}), fin.
- fig_datation_demo : Étapes : loi (a = a₀·e^{−λt}), rapport (a/a₀ = e^{−λt}), ln (ln(a₀/a) = λ·t), resultat (t = (1/λ)·ln(a₀/a)), fin.
- fig_pourcentages : « restants » ↔ « désintégrés » ; Étapes : trace, trente (30 % désintégrés → N = 0,70·N₀), quatre_vingt_dix (90 % → N = 0,10·N₀),
  deux_t_demi (t = 2t½ : N = N₀/4 → 75 % désintégrés), fin.
- fig_rapport_fils_pere : national 2020 R : Étapes : pere (N(U) = N₀·e^{−λt}), fils (N(Th) = N₀ − N(U) = N₀(1 − e^{−λt})), rapport
  (r = N(Th)/N(U) = e^{λt} − 1), fin.
- fig_cas_types : tableau « Le mot de la question → la méthode ». Étapes (une ligne chacune) : trace, composition (« composition du noyau » →
  Z protons, N = A − Z), equation (« écrire l'équation, identifier » → Soddy A puis Z, tableau des Z), type (« type de désintégration » →
  la particule : ⁴₂He α, ⁰₋₁e β⁻, ⁰₁e β⁺), famille (« nombre de α et β⁻ » → système en x et y), t_demi (« demi-vie graphiquement » → N₀/2
  ou a₀/2), lambda (« constante radioactive » → λ = ln2/t½, unité), nombre (« nombre de noyaux » → N = (m/M)·N_A ou N₀ = a₀/λ, λ en s⁻¹),
  date (« à quelle date, âge » → t = (1/λ)·ln(a₀/a)), pourcentage (« x % désintégrés » → N = (1 − x)·N₀), fin.
- fig_enonce_2021 : national 2021 N (pacemaker, ²³⁸₉₄Pu α, tableau des symboles Pa 91, U 92, Np 93, Pu 94 ; courbe a(t) a₀ = 10¹¹ Bq,
  t½ = 88 ans ; 30 %). Étapes : trace, donnees, fin.
- fig_enonce_2025 : national 2025 N (¹⁰⁷₄₈Cd → ¹⁰⁷₄₇Ag + ᴬ_Z e + γ ; t½ = 6,93 heures ; a₀ = 1,25·10¹² Bq ; t₁ = 2t½, t₂ = 3t½). Étapes : trace, donnees, fin.
- fig_enonce_2022 : national 2022 N (¹³¹₅₃I β⁻ ; tableau Te, Xe, Cs ; courbe a(t), a₀ = 4·10⁶ Bq, t½ = 8 jours ; 95 % désintégrés). Étapes : trace, donnees, fin.

### bilan.html et carte.html — même forme que ondes-lumineuses-tableau/bilan.html et carte.html (imprimer.js, acquis)
bilan.html : la fiche « Ce qu'il faut retenir » sur UNE page (deux au plus), page 2 = la page de l'élève (lacunes, acquis, acquis_ids reçus
par set_parameters). Blocs (id, titre, définition mot pour mot, formule encadrée, piège orange « ⚠ », comps) :
1 noyau (C1) : ᴬ_Z X : Z protons, N = A − Z neutrons, A nucléons ; « Des isotopes sont des noyaux qui ont le même nombre de protons Z et des
  nombres de nucléons A différents. » ; ⚠ Z = protons, pas neutrons.
2 stabilite (C2) : diagramme (N, Z) : vallée de stabilité ; au-dessus : excès de neutrons → β⁻ ; au-dessous : excès de protons → β⁺ ;
  lourds → α ; ⚠ isotopes : une ligne perpendiculaire à l'axe des Z.
3 radioactivite (C3) : « La radioactivité est une transformation nucléaire naturelle, spontanée et aléatoire, au cours de laquelle un noyau
  instable se transforme en un noyau plus stable avec émission d'une particule. » ; lois de Soddy : conservation de A et de Z ; ⚠ on
  conserve A et Z, pas le nombre de protons.
4 desintegrations (C4) : α : ⁴₂He ; β⁻ : ⁰₋₁e (n → p) ; β⁺ : ⁰₁e (p → n) ; γ : Y* → Y + γ ; ⚠ γ ne change ni A ni Z.
5 famille (C5) : système en x et y (A puis Z) ; ⚠ β ne change pas A : y d'abord.
6 loi (C6) : N(t) = N₀·e^{−λt} ; λ en s⁻¹ (ou jour⁻¹, an⁻¹) ; τ = 1/λ (tangente à l'origine) ; ⚠ N(t) = noyaux restants.
7 demi_vie (C7) : « La demi-vie t½ est la durée au bout de laquelle la moitié des noyaux initialement présents se sont désintégrés. » ;
  t½ = ln2/λ ; N(n·t½) = N₀/2ⁿ ; ⚠ à 2t½ il reste 25 %, 75 % sont désintégrés.
8 activite (C8) : « L'activité a est le nombre de désintégrations par seconde ; elle s'exprime en becquerel (Bq). » ; a = λ·N ;
  a(t) = a₀·e^{−λt} ; N = (m/M)·N_A ; ⚠ λ en s⁻¹ pour a en Bq.
9 datation (C9) : t = (1/λ)·ln(a₀/a) ; carbone 14 (t½ = 5730 ans) ; ⚠ a₀ : même masse d'un échantillon vivant (récent).
Moments : fiche, noyau, stabilite, radioactivite, desintegrations, famille, loi, demi_vie, activite, datation, lacunes.
carte.html : au centre « La décroissance radioactive » (« un noyau instable se désintègre au hasard ; un grand nombre suit une loi »),
8 branches dessinées une à une : noyau (ᴬ_Z X, isotopes), stabilite (diagramme (N, Z), vallée), desintegrations (α, β⁻, β⁺, γ ; Soddy),
famille (x α, y β⁻), loi (N = N₀·e^{−λt}, τ = 1/λ), demi_vie (t½ = ln2/λ, N₀/2ⁿ), activite (a = λN, Bq, N = (m/M)·N_A),
datation (t = (1/λ)·ln(a₀/a), carbone 14). Moments : definition + les 8 ids de branche + fin. Le même drapeau acquis entoure les branches à
reprendre (comps : noyau C1, stabilite C2, desintegrations C3 C4, famille C5, loi C6, demi_vie C7, activite C8, datation C9).
Tout dans 760 × 420. Bouton « 🖨️ Imprimer / PDF » sur les deux.
