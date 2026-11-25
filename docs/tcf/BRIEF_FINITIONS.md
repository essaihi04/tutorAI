# Finitions des cours de /TCF : charte de couleurs et simulations qui remplissent le cadre (25/11/2026)

Les trois cours sont écrits (branche `tcf-cours`, `docs/tcf/RAPPORT_<deck>.md`). Relecture à l'écran (lecteur /TCF à
1280×720 et téléphone 724×350) : deux défauts à corriger partout, plus la demande de l'utilisateur
« veuillez prendre en considération la charte de couleur adéquate ».

## Interdit

- **Ne change aucun texte parlé** : `speech_text.mixed`, `enonce_dit`, `parole`, `dit` des questions, réactions,
  démonstrations, observations, rappels. Leurs voix Bodi sont en cours de génération sur Kaggle à partir de ces textes.
  Si une voix nomme une couleur (« la boule rose »), le dessin garde CETTE couleur. Un `mot` de `pointage` / `centre`
  reste un extrait exact du texte parlé.
- Pas de commit sur `main`, pas de `--force`, pas de déploiement. Les `.json` sont ignorés : `git add -f`.
  Commits fréquents : `git fetch origin && git rebase origin/tcf-cours && git push origin HEAD:tcf-cours`.

## 1. La charte de couleurs

- **Le lexique du site d'abord** (skill `simulations-au-tableau`, règle « un objet, un seul dessin » ;
  `frontend/public/media/simulations/shared/lexique/` : `lexique.js`, `lexique-chimie.js`, `lexique-physique.js`,
  `lexique-maths.js`, et `docs/lexique-visuel.md`) : chaque objet qui existe dans le lexique est dessiné PAR le lexique
  (proton rose, électron, neutron, molécules, verrerie, solutions, appareils, courbes et points des graphes avec
  `Lexique.maths.ROLES` : courbe cyan, point jaune, tangente orange…). Une copie locale d'un dessin du lexique est un
  défaut : remplace-la par l'appel au lexique.
- **Ce qui manque au lexique y entre** (pour tous les cours futurs) : en physique, ajoute à `lexique-physique.js` une
  table des couleurs de la mécanique (`Lexique.physique.MECANIQUE` : vecteur vitesse, poids, réaction, tension, force
  quelconque, vecteur position, vecteurs unitaires, centre d'inertie, points de l'enregistrement, trajectoire), en
  gardant les couleurs déjà dites et montrées dans le cours mouvement (v⃗ vert, P⃗ rouge, R⃗ bleu, T⃗ orange, F⃗
  violet, OM⃗ rose, i⃗ j⃗ cyan, points jaunes) sauf si elles contredisent le lexique ; documente-la dans
  `docs/lexique-visuel.md` ; les simulations du cours la lisent au lieu de leur table locale. En chimie, même chose pour
  un objet nouveau dessiné dans le cours (montage à reflux, réfrigérant, plaque de CCM, cuve, atome / noyau, couches
  K L M) : il entre dans `lexique-chimie.js` ou `lexique.js` s'il servira à d'autres cours.
- **La craie suit un code fixe**, le même dans les trois cours (et celui des cours de 2ᵉ Bac — regarde
  `physics/ondes-tableau/` et `chimie/*-tableau/`) : titres et mots-clés en jaune craie, légendes en blanc craie,
  valeurs données en blanc, résultats calculés et conclusions en vert ou orange (une seule règle, partout), erreurs /
  pièges en rose, flèches et repères dans la couleur de l'objet qu'ils désignent. Les cartes `concentration.centre`
  et le cahier gardent la charte du cahier (skill `cahier-de-l-eleve` § 6 : `I.` jaune centré, `1.` cyan,
  `Définition :` vert, `Formule :` ambre, `Méthode :` bleu, `Attention :` rose, `Remarque/Exemple` gris,
  `Donc/Conclusion` orange, tableaux) : relis chaque ligne de `cahier` (blocs et diapos) et corrige son début si besoin.
- Contraste : tout texte lisible sur le tableau vert foncé (pas de bleu foncé, de noir ou de gris foncé sur le vert).

## 2. La simulation remplit son cadre (règle « simulation d'abord », ~70 % de la scène)

Dans le lecteur à 1280×720, plusieurs vues dessinent un petit objet à gauche et laissent la moitié droite du tableau
vide (ex. le tube de Thomson, les deux ballons « sans / avec éthanol »). Chaque vue doit occuper tout son cadre :
l'objet principal grand et centré, la colonne d'écriture à côté s'il y en a une, rien de minuscule ; et en téléphone
paysage (cadre ~429×250) seulement l'étape en cours, en grand, texte ≥ 15 px. Vérifie CHAQUE vue de chaque page
(captures Playwright du cadre seul à 760×420 et 429×250, et du lecteur entier à 1280×720 et 724×350 :
`npx vite --config vite.tcf.config.ts` puis `http://localhost:5173/TCF/tcf.html?cours=<id>&diapo=<id>`, cliquer
« Commencer le cours », attendre ~12 s) et regarde les captures. Corrige aussi les petits défauts vus (texte coupé ou
qui déborde, étiquette parasite dans un coin, chevauchements).

## 3. À la fin

`python -I scripts/verifier_formules.py <cours.json>` et `python -I backend/scripts/verifier_parcours.py <cours.json>` :
rien ; `python -X utf8 scripts/tcf/lister_voix_tcf.py <cours.json>` ne doit PAS changer `<id>_voix.json` (git diff vide
dessus : preuve que la voix n'a pas bougé). Ajoute une section « Finitions » à `docs/tcf/RAPPORT_<deck>.md` (ce qui a
changé, captures regardées, ce qui reste) et pousse.
