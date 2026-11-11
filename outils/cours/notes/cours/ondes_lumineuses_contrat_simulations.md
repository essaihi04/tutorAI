# Contrat des simulations — cours « Propagation d'une onde lumineuse » (phys_ch3_ondes_lumineuses)

Dépôt : C:\Users\HP\Desktop\ai-tutor-bac (partagé : d'autres sessions y travaillent en parallèle).
Dossier à créer/remplir : frontend/public/media/simulations/physics/ondes-lumineuses-tableau/
(déjà présents : commun.js = window.OndesTableau.Scene, exposants.js, lumiere.css — copies du cours témoin ; ne les modifie pas
sans nécessité, et si tu dois les changer, ne casse pas l'usage des autres pages du dossier).

## Lire d'abord (par extraits si gros)
- .agents/skills/simulations-au-tableau/SKILL.md (À SUIVRE À LA LETTRE), docs/design/labos-au-tableau.md
- le kit : frontend/public/media/simulations/shared/tableau/tableau.js, tableau.css, imprimer.js
- les modèles du cours témoin (forme seulement, ne les modifie pas) : frontend/public/media/simulations/physics/ondes-periodiques-tableau/
  fente.html (protocole, moments, play_until, repères, explication, ?vue=), corde.html, figures.html (figures à étapes ?fig=),
  bilan.html, carte.html. Et ondes-tableau/ballon.html pour le rendu « réel ».

## Règles communes
- Chaque page : `<link>` /media/simulations/shared/tableau/tableau.css + lumiere.css ; scripts /media/simulations/shared/tableau/tableau.js,
  commun.js, exposants.js (si exposants), puis le script de la page, puis `<script src="/media/simulations/professor-locate.js" defer>`.
- Fond transparent (lumiere.css), cadre virtuel 760 × 420 (OndesTableau.Scene, cadre()/local()), rien de coupé, pas de défilement,
  barre (bouton + bulle) EN HAUT, bas libre (4.5em). UN bouton principal qui cycle (Lancer → Pause → Reprendre → Rejouer) avec
  data-professor-control ; les réglages = poignées glissées sur le dessin (Tableau.glisser), pas de curseurs.
- `Tableau.protocole({ id, commandes, config, texte, etat, progression, executer })` ; commandes : start, reset, pause, resume,
  set_time {time_s}, set_parameters {…} (schéma avec plages et pas), play_until {moment | time_s} (rejoue depuis 0 si l'instant est
  passé, sinon continue, puis se fige avec « Arrêt sur image : … » dans la bulle). highlight {target} est ajouté par le kit.
- État : simulation_status, ce_qui_se_voit (phrase française qui dit TOUT ce qu'on voit : vues, valeurs avec unités, phase en cours),
  current_variant, time_s, parameters, moments (objet nom → instant en s, recalculé quand un paramètre change), derniere_main (kit).
  Émis à chaque événement et toutes les 500 ms pendant que ça tourne.
- Repères `craie.repere(id, x, y, w, h, 'libellé')` pour TOUS les ids listés ci-dessous (le cours pointe dessus par ces noms exacts),
  et `Tableau.explication({ <vue>: [{ repere, texte }] })`.
- Une scène figée dessine encore ce qui bouge (running || pause).
- Apostrophe typographique ’ dans toute chaîne JS en français (ou backticks). Déclarer la scène avant la boucle.
- Rendu « réel » (règle 7) : salle sombre DANS le cadre de la vue (pas toute la page : le tableau du cours reste visible autour),
  faisceau laser peint (dégradé lumineux + halo, couleur de la radiation : fonction couleurDe(λ nm) réaliste), taches peintes en
  dégradé d'intensité, verre peint (teinte légère, reflets, arêtes éclairées), objets ombrés. La craie : lettres, cotes, pointillés,
  flèches, axes. Le peint ne change jamais la physique (valeurs exactes dans ce_qui_se_voit et les cotes). Rendu à la demande.
- Texte du tableau en français, indices jamais avec « _ » visible (Craie.segments rend y_M en indice), exposants via exposants.js.
- MOTS INTERDITS sur le dessin, dans ce_qui_se_voit et les explications : interférences, fentes de Young, interfrange, différence de
  marche, réseau, Huygens, Fresnel, Fraunhofer, sinus cardinal, polarisation, loi de Cauchy, minimum de déviation, 1,22, réflexion
  totale, angle limite, photon, Doppler. Formules écrites seulement : θ = λ/a ; tan θ = L/(2D) ; θ = L/(2D) ; λ/a = L/(2D) ;
  L = 2λD/a (et λ = aL/(2D), a = 2λD/L, d = 2λD/L, D = aL/(2λ)) ; λ₀ = c/ν (ν = c/λ₀) ; v = λ·ν ; n = c/v (v = c/n) ; λ = λ₀/n ;
  n = L/L' ; λ₂/λ₁ = L₂/L₁ ; sin i = n·sin r ; sin i' = n·sin r' ; A = r + r' ; D = i + i' − A ; et des applications numériques.
- Valeurs de référence : c = 3,00·10⁸ m/s ; visible 400 nm (violet) – 800 nm (rouge) ; indices air 1, eau 1,33, verre 1,5.
- Noms de moments, de repères, de paramètres et de vues : EXACTEMENT ceux de ta fiche ci-dessous (le cours est écrit en parallèle
  avec ces noms). Tu peux en ajouter, jamais en renommer. Si un nom est impossible, dis-le dans ton rapport.
- Interdits : ne modifie rien hors de ce dossier (pas frontend/src, pas backend, pas le cours témoin ni ses simulations, pas le kit
  shared/) ; aucun commit/push/stash/reset/checkout ; aucune voix ; ne lis aucun fichier d'identifiants.
- Vérification obligatoire : extraire chaque bloc <script> inline et `node --check` dessus ; relire les libellés aux positions
  extrêmes des poignées (pas de chevauchement, rien hors du cadre). Si tu as des outils de navigateur, ouvre la page (serveur
  statique local sur frontend/public, ex. `python -m http.server` lancé en arrière-plan sur un port libre, puis arrêté) : aucune
  erreur console, encre sur le canvas, bouton présent ; pilote-la par postMessage {type:'simulation_control', command, parameters}
  depuis la console si possible et relis current_state.
- Rapport final (court) : fichiers créés, moments réels (nom → s) par vue, repères, paramètres acceptés, écarts avec la fiche,
  résultat des node --check et du test navigateur.

## Fiches

### diffraction.html — laser, fente / fil / trou, écran
Deux vues étiquetées à la craie : « Vue de dessus » (laser ombré, faisceau, fente = deux lèvres, éventail de lumière jusqu'à l'écran,
cote D, angle θ du centre au bord de la tache, angle exagéré pour l'œil : l'écrire) et « Écran vu de face » (la figure peinte :
tache centrale très lumineuse, extinctions sombres, taches secondaires plus pâles et deux fois plus étroites ; règle graduée en cm ;
cote L). Intensité réaliste en fonction de la position (minima nuls à x = k·λ·D/a), couleur = couleur de la radiation.
La figure s'étale PERPENDICULAIREMENT à la fente (fente verticale → taches en ligne horizontale).
Paramètres (set_parameters) : a_mm 0.04..0.40 pas 0.01 ; D_m 1.0..3.0 pas 0.1 ; lambda_nm 400..800 pas 10 (pastilles : 400 violet,
450 bleu, 520 vert, 580 jaune, 650 rouge) ; objet fente|fil|trou (fil : diamètre d = a_mm, même figure ; trou : tache ronde et
anneaux, qualitatif, sans formule) ; milieu air|eau (eau : une cuve entre fente et écran, n = 1,33, λ = λ₀/n, la tache se
resserre L' = L/n) ; orientation verticale|horizontale (fente horizontale → figure verticale) ; source laser|blanche (blanche :
superposition des couleurs, centre blanc, bords colorés, qualitatif).
Poignées élève : lèvre de la fente (a), écran (D), pastille de couleur (touche = couleur suivante).
L = 2·λ·D/(n·a) affichée en cm (2 décimales), θ = λ/(n·a) en rad (ex. « θ = 6,5·10⁻³ rad »).
Vues ?vue= (préréglages) :
- ouverture (défaut) : pas de fente au départ, 650 nm, D = 2,0 m. Moments : laser_allume, point_sur_ecran (le faisceau nu fait un
  point net sur l'écran), fente_placee (fente a = 0,40 mm posée), fente_se_ferme (a diminue de 0,40 à 0,05 mm, animé),
  tache_s_etale (a = 0,05 mm atteint, la tache est large), tache_centrale (tache centrale entourée), extinctions (extinctions
  marquées), mesure_L (cote L et valeur), fin.
- figure : fente a = 0,10 mm, 650 nm, D = 2,0 m déjà posée. Moments : laser_allume, tache_s_etale, tache_centrale, extinctions,
  mesure_L, fin. (variante du cours : set_parameters {orientation:'horizontale'} puis play_until mesure_L.)
- reglage : comme figure mais a = 0,20 mm au départ (le cours passe à 0,10 puis change la couleur 650 → 450).
- mesure : a = 0,10 mm, D = 2,0 m, 650 nm → L = 2,60 cm, θ = 6,5·10⁻³ rad, règle bien lisible. Mêmes moments que figure.
- fil : objet fil, d = 0,08 mm, 600 nm, D = 2,0 m → L = 3,00 cm. Mêmes moments (+ variante objet 'trou').
- cuve : 600 nm, a = 0,10 mm, D = 2,0 m. Moments : laser_allume, tache_s_etale, mesure_L (L = 2,40 cm dans l'air), cuve_se_remplit
  (la cuve se remplit d'eau entre la fente et l'écran), tache_se_resserre, mesure_L_prime (L' = 1,80 cm, n = L/L' = 1,33), fin.
- blanche : source blanche, a = 0,10 mm, D = 2,0 m. Moments : laser_allume (lampe), tache_s_etale, tache_centrale (centre blanc),
  bords_colores, fin.
Repères : laser, fente (aussi pour fil/trou), ecran, tache_centrale, extinction, L, D, a, theta, poignee_a, poignee_D,
pastille_couleur, vue_dessus, vue_ecran, cuve (vue cuve), regle.
ce_qui_se_voit : vue, objet, a ou d (mm), D (m), λ (nm) et couleur, milieu, L (cm), θ (rad), direction de la figure, phase.

### ecart-angulaire.html — où est θ, le triangle, tan θ ≈ θ
Deux vues : « Montage vu de dessus » (même rendu lumineux : faisceau, fente, éventail, écran, tache) et « Le triangle seul »
(triangle rectangle fente – centre de la tache – bord de la tache, tracé à la craie, agrandi). Angle exagéré pour l'œil (l'écrire).
Valeurs : λ = 650 nm, a = 0,10 mm, D = 2,0 m → θ = 6,5·10⁻³ rad, L = 2,6 cm, L/2 = 1,3 cm.
Moments (vue montage, défaut) : rayon_centre (le rayon qui va au centre de la tache), rayon_bord (le rayon qui va au bord de la
tache centrale = première extinction), angle_theta (arc et lettre θ entre les deux : du centre au bord, PAS d'un bord à l'autre),
demi_largeur (cote L/2 du centre au bord, et L entière en pointillé pour comparer), triangle_isole (le triangle sort dans « Le
triangle seul » : θ, L/2 en face (côté opposé), D collé à θ (côté adjacent), angle droit), tan_ecrit (s'écrit : tan θ = (L/2)/D =
L/(2D)), petit_angle (s'écrit : θ = 6,5·10⁻³ rad ; tan θ = 6,5·10⁻³ ; « θ petit, en radian : tan θ ≈ θ », et θ = L/(2D)), fin.
?vue=triangle : la même suite mais la scène s'ouvre directement figée sur tan_ecrit (pour la diapositive de l'égalité :
continuer jusqu'à petit_angle puis écrire λ/a = L/(2D) au moment egalite ; ajoute le moment egalite après petit_angle).
Paramètres : D_m 1.0..3.0 (poignée : l'écran ; L change, θ ne change pas : le dire dans ce_qui_se_voit), a_mm 0.05..0.40,
lambda_nm 400..800.
Repères : theta, L_sur_2, L, D, angle_droit, fente, centre_tache, bord_tache, vue_montage, vue_triangle, formule_tan, poignee_D.

### courbe.html — la courbe point par point, pente, identification
Deux vues : « L'expérience » (petite vue du montage en haut à gauche : la fente changée, la tache peinte qui change de largeur) et
« La courbe » (axes avec noms ET unités, points à la craie, droite, triangle de pente). Paramètre courbe (?courbe= et
set_parameters {courbe}) :
- L_inverse_a (défaut) : D = 2,0 m, 650 nm ; a = 0,40 ; 0,20 ; 0,10 ; 0,05 mm → 1/a = 2,5 ; 5 ; 10 ; 20 mm⁻¹ → L = 6,5 ; 13 ;
  26 ; 52 mm. Axe x « 1/a (mm⁻¹) », axe y « L (mm) ». Moments : point_1, point_2, point_3, point_4, droite (droite passant par
  l'origine : « fonction linéaire : L = k·(1/a) »), pente (triangle de pente depuis l'origine jusqu'au point (10 ; 26) :
  k = 26 mm / 10 mm⁻¹ = 2,6 mm² = 2,6·10⁻⁶ m²), identification (« L = 2λD·(1/a) donc k = 2λD ; λ = k/(2D) = 6,5·10⁻⁷ m = 650 nm »), fin.
- L_a : mêmes mesures, axe x « a (mm) » : points 1 à 4 et moment courbe (« ce n'est pas une droite »), fin.
- theta_inverse_a : θ = λ·(1/a) : axe x « 1/a (m⁻¹) » ×10³, axe y « θ (rad) » ×10⁻³ ; k = λ. Mêmes moments que L_inverse_a.
- L_D : (national 2021 N) a = 0,06 mm, λ = 600 nm ; D = 0,5 ; 1,0 ; 1,5 ; 2,0 m → L = 1 ; 2 ; 3 ; 4 cm ; axe x « D (m) », axe y
  « L (cm) » ; k = 4·10⁻² m / 2 m = 2·10⁻² (sans unité) ; L = (2λ/a)·D donc k = 2λ/a, λ = a·k/2 = 6·10⁻⁷ m = 600 nm. Mêmes moments.
Poignée élève : un point de lecture qu'on fait glisser sur la droite (coordonnées affichées avec les unités des axes).
Repères : axe_x, axe_y, droite, origine, pente, point_lu, point_1..point_4, vue_experience, vue_courbe, identification.
ce_qui_se_voit : courbe, unités des axes, points tracés, coordonnées du point lu, k avec unité et en SI, conclusion.

### spectre.html — le spectre visible, λ₀ et ν
Une vue « Le spectre » : bande horizontale de 300 à 900 nm ; zone « ultraviolet » (< 400 nm, sombre) | « visible » (dégradé
continu peint, réaliste) | « infrarouge » (> 800 nm, sombre) ; graduations en nm à la craie (400, 500, 600, 700, 800) ; curseur
(poignée) de longueur d'onde ; sous la bande, affiché : λ₀ en nm et en m (6,5·10⁻⁷ m), la couleur, ν = c/λ₀ en Hz (·10¹⁴), et
« visible » ou « non visible (ultraviolet / infrarouge) ».
Paramètre : lambda_nm 100..100000 (hors de 300..900 : curseur collé au bord avec une flèche « bien plus loin : pas visible » ; ex.
6,5·10⁻⁵ m = 65 000 nm).
Moments : bande_peinte, violet_400, vert_520, rouge_800, ultraviolet (curseur à 350 nm), infrarouge (curseur à 900 nm), valeur
(curseur va à lambda_nm courant), fin.
Repères : spectre, visible, uv, ir, curseur, borne_400, borne_800, valeur_m, frequence.

### milieu.html — l'onde passe de l'air au verre (incidence normale)
Vue « Air | Verre » (de côté) : un train d'onde sinusoïdal coloré (couleur de la radiation, lumineux) avance de gauche à droite,
entre dans un bloc de verre peint (incidence normale, aucune déviation), puis ressort à droite dans l'air. Mouvement « ralenti
énormément » (l'écrire). Dans le verre : le front avance moins vite (v = c/n), les crêtes se resserrent (λ = λ₀/n), même nombre de
crêtes par seconde (même ν), même couleur. Vue « Compteurs » : crêtes comptées par seconde (ralentie) de chaque côté, chrono du front.
Valeurs : λ₀ = 600 nm, ν = 5,0·10¹⁴ Hz ; verre n = 1,5 : v = 2,0·10⁸ m/s, λ = 400 nm ; eau n = 1,33 : v = 2,26·10⁸ m/s, λ = 451 nm.
Paramètres : n 1.0..2.0 pas 0.01 (poignée : glisser l'étiquette « eau / verre » sur le bloc), lambda0_nm 400..800, vue.
Vues ?vue= : verre (défaut), eau, deux (deux radiations dans le même verre, national 2021 N : rouge λ₀ = 767 nm, ν = 3,91·10¹⁴ Hz,
v = 1,85·10⁸ m/s (n = 1,62) ; jaune λ₀ = 589 nm, ν = 5,09·10¹⁴ Hz, v = 1,81·10⁸ m/s (n = 1,66) : deux trains l'un au-dessus de
l'autre, le front jaune prend du retard sur le rouge dans le verre).
Moments (verre/eau) : onde_dans_air (cote λ₀, c), front_entre (le front entre et ralentit), lambda_serree (crêtes resserrées dans
le verre), compte_frequence (les deux compteurs donnent le même nombre), mesure_lambda (cotes λ₀ = 600 nm et λ = 400 nm),
ressort_dans_air, fin. Vue deux : onde_dans_air, front_entre, fronts_ecartes (le jaune en retard), mesure_vitesses (v rouge et v
jaune écrites), fin.
Repères : air, bloc, front, lambda0, lambda, compteur_air, compteur_verre, vue_onde, vue_compteurs, front_rouge, front_jaune (vue deux).
ce_qui_se_voit : c, v, λ₀, λ, ν des deux côtés, n, phase.

### prisme-dispersion.html — lumière blanche ou laser sur un prisme
Deux vues : « Vue de dessus » (source + fente, faisceau, prisme de verre peint, éventail, écran) et « Écran » (bande : le spectre
continu peint, ou un seul point). Réfraction réelle aux deux faces (loi sin i = n sin r dans le code), indice qui dépend de la
couleur (valeurs d'un verre courant, n rouge ≈ 1,61, n violet ≈ 1,66 ; l'écart peut être un peu agrandi pour l'œil, le dire en
commentaire). Le violet est le plus dévié, le rouge le moins.
Paramètre source (?source= et set_parameters) : blanche (défaut) | rouge | verte.
Moments blanche : blanc_arrive, entre_dans_verre, couleurs_se_separent, spectre_sur_ecran, rouge_moins_devie (rayon rouge souligné
+ arc de sa déviation), violet_plus_devie, fin. Moments laser (rouge/verte) : rayon_arrive, rayon_sort (un seul rayon, une seule
couleur, pas d'éventail), point_sur_ecran, fin.
Poignée élève : la source (touche = blanche → rouge → verte).
Repères : source, faisceau, prisme, ecran, spectre, rouge, violet, point (laser), vue_dessus, vue_ecran.
ce_qui_se_voit : la source, ce qui sort du prisme, ce qui arrive sur l'écran, l'ordre des couleurs (violet le plus dévié).

### prisme-angles.html — le trajet d'un rayon, les quatre relations (partie « pour le devoir »)
Deux vues : « Le prisme » (grand, verre peint, rayon laser rouge lumineux ; normales en pointillé, arcs d'angles et lettres à la
craie, une couleur de craie par face) et « Les calculs » (colonne : les relations qui s'écrivent une à une avec les nombres).
Valeurs : A = 60°, n = 1,5, i = 30° → r = 19,47°, r' = 40,53°, i' = 77,10°, D = 47,10° (calculer, 2 décimales).
Moments : rayon_arrive, normale_1, refraction_1 (r dans le verre ; « sin i = n·sin r » puis « sin r = sin 30° / 1,5 = 0,333 ;
r = 19,47° »), trajet_dans_verre (le rayon va tout droit jusqu'à la 2e face), A_r_rprime (« A = r + r' » ; r' = 60 − 19,47 =
40,53°), normale_2, refraction_2 (« sin i' = n·sin r' » ; i' = 77,10°), sortie (le rayon sort et s'écarte de la normale),
deviation_D (prolongements pointillés des rayons d'entrée et de sortie, arc D ; « D = i + i' − A = 47,10° »), fin.
Si n·sin r' > 1 : le rayon ne sort pas par la deuxième face (l'écrire ainsi, sans autre mot).
Paramètres : i_deg 20..70 (poignée : faire pivoter le laser), n 1.3..1.8 pas 0.01, A_deg 30..70.
Repères : rayon, face_1, face_2, normale_1, normale_2, i, r, r_prime, i_prime, A, D, calculs, laser, vue_prisme, vue_calculs.
ce_qui_se_voit : i, r, r', i', A, D en degrés, n, phase.

### figures.html — figures à étapes (?fig=), comme ondes-periodiques-tableau/figures.html
Chaque figure s'écrit à la craie, étape par étape (moments = noms des étapes, play_until {moment}). Liste :
- fig_eau_lumiere : deux panneaux « Eau : ouverture étroite » (ondes planes peintes qui repartent en arcs derrière l'ouverture) |
  « Lumière : fente fine » (faisceau qui s'étale, taches). Étapes : eau, lumiere, conclusion (« Seules les ondes se diffractent :
  la lumière a un aspect ondulatoire »), fin.
- fig_unites : l'escalier des longueurs vers le mètre : 1 cm = 10⁻² m ; 1 mm = 10⁻³ m ; 1 µm = 10⁻⁶ m ; 1 nm = 10⁻⁹ m. Étapes :
  trace, exemples (0,10 mm = 1,0·10⁻⁴ m ; 650 nm = 6,5·10⁻⁷ m ; 2,6 cm = 2,6·10⁻² m), retour (6,5·10⁻⁷ m = 650 nm : × 10⁹), fin.
- fig_isoler : λ/a = L/(2D) écrit, produit en croix animé (flèches), puis les quatre formes. Étapes : egalite, croix, L
  (L = 2λD/a), lambda (λ = aL/(2D)), a (a = 2λD/L), D (D = aL/(2λ)), fin.
- fig_montage_examen : schéma type document d'examen (laser, fente a, écran à D, tache L, θ) puis les quatre lignes. Étapes :
  trace, ligne1 (D'après la figure : tan θ = (L/2)/D = L/(2D)), ligne2 (θ petit : tan θ ≈ θ, donc θ = L/(2D)), ligne3 (or θ = λ/a),
  ligne4 (donc λ/a = L/(2D) et L = 2λD/a), fin.
- fig_deux_experiences : tableau Expérience 1 | Expérience 2 (national 2023 R : 580 nm, L₁ = 2,7 cm ; L₂ = 3,4 cm). Étapes : trace,
  exp1 (λ₁/a = L₁/(2D)), exp2 (λ₂/a = L₂/(2D)), barre (a et 2D barrés : les mêmes), rapport (λ₂/λ₁ = L₂/L₁ ; λ₂ = L₂·λ₁/L₁ =
  3,4 × 580 / 2,7 ≈ 730 nm), fin.
- fig_soleil_vide : Soleil — vide — Terre (la lumière arrive) | une sonnette sous une cloche vide (on ne l'entend plus). Étapes :
  lumiere, son, conclusion (« La lumière se propage dans le vide : ce n'est pas une onde mécanique. Dans le vide : c = 3,00·10⁸ m/s »), fin.
- fig_vide_milieu : tableau à deux colonnes « Vide (ou air) » | « Milieu d'indice n ». Étapes : trace, celerite (c → v),
  indice (n = c/v, n ≥ 1, donc v = c/n), longueur (λ₀ → λ = λ₀/n), frequence (ν → ν : la même), fin.
- fig_trois_phenomenes : trois petits dessins : diffraction (fente : la lumière s'étale), réfraction (le rayon se casse en
  changeant de milieu), dispersion (le prisme sépare les couleurs). Étapes : diffraction, refraction, dispersion, definition
  (« Un milieu est dispersif si la célérité de la lumière dépend de sa fréquence »), fin.
- fig_cas_types : tableau « Le mot de la question → la méthode ». Étapes (une ligne chacune) : trace, nommer (« nommer, que met en
  évidence » → diffraction, aspect ondulatoire), etablir (« établir L, montrer que » → les quatre lignes), fil (« on remplace la
  fente par un fil, un cheveu » → d à la place de a), rapport (« on remplace la source, mêmes conditions » → écrire deux fois,
  diviser), courbe (« la courbe L = f(…) » → droite, pente, identification), milieu (« dans un liquide, milieu d'indice n » →
  v = c/n, λ = λ₀/n, n = L/L'), frequence (« calculer la fréquence » → ν = c/λ₀, λ₀ en m), fin.
- fig_enonce_2023 : énoncé et figure type national 2023 R (source jaune λ₀ = 580 nm dans l'air, fente HORIZONTALE de largeur a,
  écran à D = 1,4 m, taches sur une ligne verticale, L = 2,7 cm ; c = 3·10⁸ m/s). Étapes : trace, donnees, fin.
- fig_enonce_2021 : national 2021 N : fente a = 0,06 mm, courbe L = f(D) (points (0,5 m ; 1 cm), (1 ; 2), (1,5 ; 3), (2 ; 4)),
  puis cheveu, D₁ = 2 m, L₁ = 3 cm. Étapes : trace, courbe, donnees, fin.
- fig_enonce_2025 : national 2025 R : laser, fente a, écran à D, L = 2,4 cm ; même expérience dans un liquide : L' = 1,8 cm ;
  c = 3·10⁸ m/s. Étapes : trace, liquide, donnees, fin.
Repères : le repère `figure` sur chaque figure, plus un repère par étape (même nom que l'étape) sur ce qu'elle écrit.

### bilan.html et carte.html — même forme que ondes-periodiques-tableau/bilan.html et carte.html (imprimer.js, acquis)
bilan.html : la fiche « Ce qu'il faut retenir » sur UNE page (deux au plus), page 2 = la page de l'élève (lacunes, acquis,
acquis_ids reçus par set_parameters). Blocs (id, titre, définition mot pour mot, formule encadrée, piège orange « ⚠ », comps) :
1 diffraction (C1) : « La diffraction de la lumière par une fente fine ou un fil met en évidence l'aspect ondulatoire de la
  lumière. » ; la figure s'étale perpendiculairement à la fente ; ⚠ diffraction, pas réfraction ; ondulatoire, pas monochromatique.
2 ecart (C2) : θ = λ/a (θ en rad, λ et a en m) ; θ : du centre de la tache centrale à la première extinction ; ⚠ a diminue → θ augmente.
3 largeur (C3) : tan θ = L/(2D) ; θ petit : tan θ ≈ θ ; L = 2λD/a ; ⚠ le côté opposé est L/2 ; tout en mètre.
4 comparer (C4) : fil : d à la place de a ; deux expériences : λ₂/λ₁ = L₂/L₁ ; liquide : n = L/L' ; ⚠ λ appartient à la source.
5 courbes (C5) : droite par l'origine : y = k·x ; L = f(1/a) → k = 2λD ; θ = f(1/a) → k = λ ; L = f(D) → k = 2λ/a ; ⚠ convertir les unités des axes.
6 radiation (C6) : « Une lumière monochromatique est constituée d'une seule radiation, caractérisée par sa fréquence ν. » ;
  λ₀ = c/ν, c = 3,00·10⁸ m/s ; visible : 400 nm à 800 nm ; ⚠ nm, pas µm ; λ₀ en m dans le calcul.
7 milieu (C7) : n = c/v ; λ = λ₀/n ; ν ne change pas ; ⚠ n ≥ 1, donc v < c et λ < λ₀.
8 dispersion (C8) : « Un milieu est dispersif si la célérité de la lumière dépend de sa fréquence. » ; la lumière blanche est
  polychromatique ; le violet est le plus dévié ; ⚠ dispersion ≠ diffraction.
9 prisme (C9, « pour le devoir ») : sin i = n·sin r ; sin i' = n·sin r' ; A = r + r' ; D = i + i' − A ; ⚠ angles mesurés depuis la normale.
Moments : fiche, diffraction, ecart, largeur, comparer, courbes, radiation, milieu, dispersion, prisme, lacunes.
carte.html : au centre « La lumière : une onde » (« la diffraction prouve son aspect ondulatoire »), 8 branches dessinées une à
une : diffraction (fente, fil : la lumière s'étale), ecart (θ = λ/a), largeur (L = 2λD/a, deux expériences, n = L/L'), courbes
(droite : k = 2λD, λ, 2λ/a), radiation (monochromatique : ν ; λ₀ = c/ν), spectre (400 – 800 nm, UV, IR), milieu (n = c/v,
λ = λ₀/n, ν la même), dispersion (prisme, violet le plus dévié ; relations du prisme : pour le devoir). Moments : definition +
les 8 ids de branche + fin. Le même drapeau acquis entoure les branches à reprendre (comps : diffraction C1, ecart C2, largeur
C3 C4, courbes C5, radiation C6, spectre C6, milieu C7, dispersion C8 C9). Tout dans 760 × 420. Bouton « 🖨️ Imprimer / PDF » sur les deux.
