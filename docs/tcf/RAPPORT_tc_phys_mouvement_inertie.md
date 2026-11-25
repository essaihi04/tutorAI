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

- `python -I scripts/verifier_formules.py` sur le cours et sur le dossier des simulations : 0.
- `python -I backend/scripts/verifier_parcours.py <cours>` : rien.
- `python -I scripts/verifier_pointage.py <cours>` : 0 défaut (chaque `mot` trouvé dans l’ordre, chaque moment et
  repère déclaré dans la simulation).
- `python backend/scripts/verifier_figures_cahier.py <cours>` : 0 erreur.
- Chaque vue : captures Playwright de chaque moment à 760×420 et 429×250 (scripts dans le scratchpad de la session),
  regardées ; aucune erreur console.
- Le cours dans la page /TCF (serveur Vite `vite.tcf.config.ts` + un petit proxy local pour `/media`, que la
  configuration de dev ne sert pas sous `/TCF/`) : les 59 diapos ouvertes une à une (`?diapo=`) à 1280×720, chacune
  charge sa simulation (ouverture et fermeture : sans figure, comme prévu), aucune erreur console ; captures de
  quelques diapos à 1280×720 et en téléphone paysage 724×350.

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
- Vues : `masse.html` écrit les vecteurs dans les fractions par des aides locales (la flèche de `texteV` ne couvre
  que la lettre de base) ; au petit cadre, les noms M₀…M₇ sont serrés et les graduations de la règle très petites ; un peu de tableau vide
  sous la colonne de texte des vues curling et grue.
- Le lecteur coupe le bouton « Au cahier » à 724 px de large (lecteur commun, pas touché).

## Commit

Dernier commit poussé sur `tcf-cours` : voir `git log -1 -- docs/tcf/RAPPORT_tc_phys_mouvement_inertie.md` (le SHA est
aussi donné dans le compte rendu de la session).

## Finitions (25 novembre 2026, `docs/tcf/BRIEF_FINITIONS.md`)

Aucun texte parlé changé : `speech_text`, `enonce_dit`, `parole`, `dit` et chaque `mot` sont identiques (comparaison
des 639 champs avant / après) ; `lister_voix_tcf.py` réécrit `tc_phys_mouvement_inertie_voix.json` sans aucune
différence (git diff vide). La voix ne nomme que deux couleurs (« v trois » en vert, la valve « الحمرا ») : gardées.

### 1. La charte de couleurs

- **Le lexique de la mécanique** (nouveau, pour tous les cours de mécanique) : `Lexique.physique.MECANIQUE` dans
  `shared/lexique/lexique-physique.js` — v⃗ vert, P⃗ rouge, R⃗ bleu, T⃗ orange, F⃗ violet, OM⃗ rose, i⃗ j⃗ k⃗ cyan,
  G point rose, points d'enregistrement jaunes (= `Lexique.maths.ROLES.point`), trajectoire cyan en pointillé [9, 6]
  (= `ROLES.courbe`), repères blanc, éclateurs A rouge / B orange ; `Lexique.physique.mecanique` : les dessins nés dans
  ce cours (point d'enregistrement, G, étincelle, table à coussin d'air, autoporteur de dessus et de côté, règle,
  chronomètre, flèche d'un vecteur dans la couleur de sa grandeur) ; `Lexique.physique.ECRITURE` : le code de la craie.
  Fiche `docs/lexique-visuel/mecanique.md`, index du README, renvoi depuis `craie.md`.
- **Le cours lit le lexique** : les 14 pages chargent `lexique-physique.js` et `lexique-maths.js` ; `commun.js` n'a
  plus de table de couleurs ni de copie des dessins (`Mvt.COUL` ← `MECANIQUE`, `ROLES`, `ECRITURE` ; `Mvt.P.point`,
  `table`, `autoporteur`… appellent le lexique ; `Mvt.HEX` = `Tableau.COULEURS`). Graphes x(t) et droite : courbe
  `ROLES.courbe`, points `ROLES.point`, triangle de pente Δx/Δt `ROLES.tangente` (orange ; Δt était vert), signe de
  v_x `ROLES.positif` / `negatif` ; tangente du vecteur vitesse orange (était cyan) et flèche « sens » blanche.
- **Trajectoire** : cyan en pointillé partout (le ballon l'était ; rectiligne / circulaire / curviligne étaient
  cyan / vert / orange, la valve jaune, le cercle du MCU sarcelle et orange) ; sur la feuille claire du MCU, encre cyan
  foncée. F⃗₂ du dynamomètre violet (était orange, la couleur de T⃗).
- **La craie** (même code que les cours atome et synthèse et que 2ᵉ Bac) : titres, mots-clés, relations générales
  jaune ; légendes et valeurs données blanc (τ, R, m, d, Δt, MᵢMᵢ₊₁ lus : étaient orange, cyan ou jaune) ; résultats
  calculés et conclusions vert (P = 20 N, v₃ = 1 m/s, T = 80 N, ω, T, f, « elles se compensent », « pseudo-isolé »,
  « le mouvement est relatif », « G est à 30 cm de A » : étaient jaune, cyan, rose ou orange) ; pièges rose (« ⚠ » de la
  fiche bilan) ; noms des axes blanc. Les « Système : {…} » et la question du curling en jaune.
- **Cahier** (blocs et traces des diapos, via `scripts/tcf/mi_donnees_*.py` puis `mi_construire.py`) : une idée par
  ligne, avec son début de la charte — « Le poids P⃗ est vertical… » sorti de la ligne Formule, « Donc le mouvement est
  relatif », « Donc la pente a est la vitesse v », « Attention : v_x = −v si l'axe est orienté contre le mouvement »,
  « Définition : un référentiel galiléen est… » + « Exemple : … », centre de masse en Définition / Remarque / Exemple,
  « Bilan : principe d'inertie… », méthodes en 1) 2) 3) ; traces des diapos découpées en lignes (`\n`). Les cartes
  `centre` (rendues d'une seule couleur par le lecteur) n'ont pas changé.
- Corrigé en passant : « M_iM_{i+1} », « M_4M_6 » s'écrivaient « Mᵢₘ_{i+1} » (l'indice avalait la lettre suivante) →
  `M_{i}M_{i+1}` (table et MCU) ; l'étiquette « feuille » (jaune sur papier crème) et « éclateur » (à cheval sur le cadre)
  en encre foncée sur la feuille.

### 2. Les vues remplissent leur cadre

- Dans le lecteur à 1280×720, l'iframe fait ~800-900 × 565 : le cadre virtuel 760×420 y prend toute la largeur ; le
  vide à droite de l'iframe est la place du lecteur (cartes, professeur), pas celle de la simulation.
- Enregistrements agrandis pour remplir la largeur : vues « lire » (règle de 14 cm sur toute la largeur, texte dessous),
  « instant », « élève », « comparer » (v₅ à gauche, v_m à droite, la conclusion en bas sur toute la largeur — elle
  sortait du cadre), vecteur vitesse « échelle » et « élève » (1 cm = 44 px au lieu de 30 : le vecteur se voit).
- Téléphone (429×250) : données du vecteur vitesse remises en haut à gauche (elles touchaient le nom v⃗₄).

### Captures regardées

Chaque vue à la fin de son animation, à 760×420 et 429×250 (57 vues × 2, avant et après), aucune erreur console ;
le lecteur /TCF entier (Vite `vite.tcf.config.ts`, `?diapo=`, « Commencer le cours », simulation menée à sa fin) pour
les 57 diapos à simulation, à 1280×720 et 724×350.

### Vérifications

`verifier_formules.py` (cours et simulations) : 0 ; `verifier_parcours.py` : rien ; `verifier_pointage.py` : 0 défaut ;
`verifier_figures_cahier.py` : 0 erreur ; `lister_voix_tcf.py` : `_voix.json` inchangé.

### Ce qui reste

- Les cartes `centre` et le bandeau d'un bloc restent de la seule couleur du lecteur (lecteur commun, pas touché).
- Vues encore un peu vides sous leur colonne de texte : curling, grue (déjà signalé) ; dans `bus/tableau` le petit bus
  à gauche est petit à côté du tableau.
- Les lueurs de comptage sur la feuille claire du MCU restent orange (le jaune ne se voit pas sur le papier).
- Les pages des autres cours de mécanique (1ʳᵉ / 2ᵉ Bac, s'il y en a) ne lisent pas encore `MECANIQUE`.
