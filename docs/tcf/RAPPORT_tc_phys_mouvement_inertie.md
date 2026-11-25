# Rapport — cours /TCF « Le mouvement et le principe d’inertie » (`tc_phys_mouvement_inertie`)

25 novembre 2026, session cloud, branche `tcf-cours` (rien sur `main`, aucun déploiement).

## Fichiers

- Cours : `frontend/src/publication/tcf/cours/tc_phys_mouvement_inertie.json` (ajouté avec `git add -f`), et sa liste de
  voix `tc_phys_mouvement_inertie_voix.json` (écrite par `scripts/tcf/lister_voix_tcf.py`).
- Source du cours : `scripts/tcf/mi_construire.py` (construit le JSON et contrôle chaque `mot`, chaque réaction, l’absence
  de chiffre et de symbole dans les textes parlés) et ses données `scripts/tcf/mi_donnees_{tete,1,2,3,4}.py`.
  **Pour modifier le cours : changer les données, puis `python -X utf8 scripts/tcf/mi_construire.py` et relancer
  `lister_voix_tcf.py`.**
- Architecture (ordre, raisons, lexique visuel, contrat moments/repères de chaque vue) :
  `docs/tcf/ARCHITECTURE_tc_phys_mouvement_inertie.md`.
- Simulations : `frontend/public/media/simulations/physics/tc_mouvement_inertie-tableau/`
  - gardées du premier agent, relues et complétées : `commun.js` (+ `window.__S/__M` pour les captures), `mvt.css`,
    `forces.html` (+ vue `compense` : anneau tenu par deux dynamomètres peints), `maths.html`, `bus.html` (tableau à
    quatre lignes : par rapport à A, à B, au bus, à la route, comme le livre plus la route), `repere.html`,
    `trajectoire.html`, `vitesse.html`, `table.html` ;
  - nouvelles : `vecteur.html` (3 vues), `mru.html` (6 vues), `mcu.html` (5 vues), `inertie.html` (8 vues),
    `grue.html` (2 vues), `masse.html` (4 vues), `bilan.html` (fiche en pages et carte à neuf branches, imprimer).

## Chiffres

- 59 diapos, 7 séances, 20 blocs (3 à 4 diapos, cahier organisé par bloc, 6 figures de cahier), 9 compétences
  (C1 prérequis … C9 centre de masse, 3 rappels chacune), 18 questions « À toi » (une par bloc, sauf bilan et fin),
  10 démonstrations, 2 questions d’observation (la valve vue par le piéton ; l’autoporteur lancé en tournant),
  réactions préparées pour chaque option.
- 214 pistes de voix : 59 diapos, 18 énoncés, 10 démonstrations, 86 réactions, 14 pistes d’observation, 27 énoncés
  de rappel.

## Méthodes couvertes (montrées par le tuteur, puis refaites par l’élève avec démonstration)

P = m·g (valise) ; forces qui se compensent (deux fois : livre, anneau) ; coordonnées d’un vecteur ; lire un graphique ;
droite x = a·t + b ; vitesse moyenne et conversion km/h ↔ m/s ; lire un enregistrement (Δt = n·τ) ; vitesse
instantanée v_i = Mᵢ₋₁Mᵢ₊₁/(2τ) ; vecteur vitesse à l’échelle ; MRU : tableau produit par l’animation, courbe point
par point, pente = v, équation horaire, signe de v_x, application du livre (τ = 50 ms → x(t) = 0,4·t + 0,04) ; MCU :
v, ω = v/R, T = 2π/ω, f = 1/T (application du livre, puis l’élève) ; centre d’inertie ; principe d’inertie (grue,
T = P = 1,5 × 10⁴ N, puis le seau du puits, 80 N) ; relation barycentrique, méthode du marteau (O en G₁ → 20 cm),
puis l’élève (tige, 30 cm).

## Vérifié, et comment

- `python -I scripts/verifier_formules.py <cours>` : 0 ; sur le dossier des simulations : voir la fin du rapport.
- `python -I backend/scripts/verifier_parcours.py <cours>` : rien.
- `python -I scripts/verifier_pointage.py <cours>` : 0 défaut (chaque `mot` trouvé dans l’ordre, chaque moment et
  repère déclaré dans la simulation).
- `python backend/scripts/verifier_figures_cahier.py <cours>` : 0 erreur.
- Chaque vue : captures Playwright de chaque moment à 760×420 et 429×250 (scripts dans le scratchpad de la session),
  regardées ; aucune erreur console.
- Le cours dans la page /TCF (serveur Vite `vite.tcf.config.ts` + un petit proxy local pour `/media`, que la
  configuration de dev ne sert pas sous `/TCF/`) : chargement, une simulation par diapo, aucune erreur ; captures à
  1280×720 et 724×350.

## Ce qui reste douteux

- **Mots à faire écouter** (vus 0 à 2 fois par la voix ; termes du programme gardés) : autoporteur, compensent,
  pseudo-isolé, isolé, barycentrique, indéformable, éclateur(s), étincelle, coussin, soufflerie, impulsions, valve,
  piéton, cycliste, arches, boucles, carreau(x), dynamomètre(s), haltère, curling, grue, béton, câble, seau, manche,
  marteau, symétrie, faces, instantanée, relatif, terrestre, soixante-douze ; darija rares : الرويضة, كنلوحو / كيلوحها
  (lancer), كيتزلق, متتابعين, السطل, البير, الجليد, معلقة, كيحبس, متوازن, كيتعادلو, كيجبدوه.
- « oméga » est écrit tel quel (le corpus dit « omega » ?) ; « teta », « tau », « delta » suivent le corpus.
- Science : l’enregistrement du cours prend τ = 20 ms et 2 cm (v = 1 m/s) au lieu de 40 ms (0,5 m/s) pour des nombres
  simples ; le MCU garde T ≈ 0,63 s et f ≈ 1,6 Hz (π) ; dans la vue « translation », A (au centre) et G sont confondus :
  deux rangées de points, pas trois (la voix le dit).
- Vues : au petit cadre, les noms M₀…M₇ sont serrés et les graduations de la règle très petites ; un peu de tableau vide
  sous la colonne de texte des vues curling et grue.
- Le lecteur coupe le bouton « Au cahier » à 724 px de large (lecteur commun, pas touché).
