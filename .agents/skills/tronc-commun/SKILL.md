---
name: tronc-commun
description: Règles pour créer ou modifier un cours, une révision ou une évaluation de Tronc Commun (TC Sciences BIOF), à partir des diaporamas d'un professeur, publiés sur le lien libre /tronc-commun. À charger avant tout travail sur un cours de Tronc Commun, en plus de cours-concentration, simulations-au-tableau et cahier-de-l-eleve.
---

# Tronc Commun : cours, révision et évaluation

Premier skill du Tronc Commun (22 novembre 2026). Il complète les skills du 2ᵉ Bac (`cours-concentration`,
`simulations-au-tableau`, `cahier-de-l-eleve`, `logique-de-cours`, `suivi-des-acquis`, `exercices`), qui s'appliquent tous ;
il ajoute ce qui est propre au Tronc Commun et les règles données par l'utilisateur sur les premiers cours (SVT :
« La sortie écologique », « Les facteurs édaphiques » activités 1 à 3, et leur révision).

## Où vit le Tronc Commun

- Hors du site : **ni dans la base des élèves, ni dans l'application, ni dans `backend/data/courses/`**. Un lien libre à part :
  https://moalim.online/tronc-commun/ (accueil, `?cours=<id>`, `?cours=<id>&diapo=<id>`, `?examen`).
- Page : `frontend/tronc-commun.html`, `frontend/src/publication/troncCommun.tsx` (accueil, liste `COURS`, lecteur), construite
  par `frontend/vite.tronc-commun.config.ts`.
- Cours : `frontend/src/publication/tronc-commun/cours/tc_<matière>_<clé>.json` (CourseDeck, `mode: "concentration"`,
  `language: "mixed"`) et `tc_<…>_voix.json` (textes à dire, pour la voix par lot). Un nouveau cours : ajouter sa carte dans
  `COURS` de `troncCommun.tsx`.
- Simulations : `frontend/public/media/simulations/<matière>/tc_<clé>-tableau/`. Le script de publication copie ces dossiers
  (liste `DOSSIERS` de `scripts/publier_tronc_commun.py`) : un nouveau dossier s'y ajoute.
- Évaluation : `frontend/src/publication/tronc-commun/sujet.ts` (le sujet) et `Examen.tsx` (la page).
- Publication : `python -I scripts/publier_tronc_commun.py [--sans-envoi]` → `/var/www/moalim/tronc-commun` sur moalim-vps.
  Aucun déploiement du site, aucun changement nginx. Demander l'accord de l'utilisateur avant d'envoyer.
- Le tuteur passe par les routes publiques déjà en ligne (`/api/v1/public/cours-ondes/…`) ; le serveur ne connaît pas les
  cours de TC : la page retire `deck_id` des demandes et ajoute `matiere`. Pas de voix en direct, pas de suivi des acquis.
  Plafond des routes publiques : 40 appels au LLM par heure, par visiteur ET par adresse IP (une classe sur le même wifi
  les partage).

## Règles de l'utilisateur (à appliquer partout : simulations, voix, tableau, cahier, fiche, évaluation)

1. **Des nombres simples, sans virgule.** Choisir des données qui donnent des résultats entiers (bocal de 50 mm :
   10 / 15 / 25 mm → 20 % / 30 % / 50 % ; perméabilité 80 ml en 8 min → 10 ml/min). Si un document du prof donne des
   décimales (46,15 %), on change les données pour des valeurs simples, en gardant la méthode.
2. **Pas de photocopie.** Aucune diapo ne montre l'image d'un document du prof (tableau, coupe, profil, outils, herbier…) :
   tout est recréé au tableau et animé ; un être vivant ou un objet réel = croquis peint (mémoire `croquis-realistes`).
   Un tableau de données est dessiné vide puis **rempli en animation** : les cases s'allument et se comptent, chaque nombre
   vole dans sa case, l'élève calcule une partie des cases.
3. **Triangle des textures.** La ligne du sable est parallèle au côté du limon ; la ligne du limon parallèle au côté de
   l'argile ; la ligne de l'argile parallèle au côté du sable. Le titre de chaque axe est écrit au-dessus de son axe, le long
   de l'axe, à l'extérieur du triangle. Le tuteur dit la règle au moment où chaque ligne se trace. Chaque domaine porte
   son nom et une couleur par grande famille (argileuse, limoneuse, sableuse, équilibrée) avec sa légende ; dans un petit
   cadre : couleurs + légende, et le nom du domaine du point écrit en grand quand la zone s'allume.
4. **Histogramme.** D'abord les comptes sont rangés dans un petit tableau (indice de fréquence I à V / nombre d'espèces),
   rempli case par case ; puis le tableau se transforme en graphe (chaque case devient la barre de son indice). Les
   rectangles sont collés les uns aux autres, sans espace ; une classe vide garde sa place ; la courbe de fréquence relie
   les milieux des sommets. Même dessin dans l'animation, le cahier et la fiche.
5. **Méthodes pas à pas.** Chaque savoir-faire (tracer dans le triangle, calculer une perméabilité, une fréquence, une
   densité, tracer un histogramme et sa courbe, lire une aire minimale) est montré lentement par le tuteur sur un exemple,
   puis refait par l'élève sur un autre ; explication simple, une idée à la fois, animations agréables.
6. **Téléphone en paysage.** Sur un écran de 724×350, le cadre de la simulation dans le lecteur fait environ 429×250 px.
   Quand le cadre fait moins de 520 px de large ou 320 px de haut : seulement l'étape en cours, en grand, texte ≥ 15 px à
   l'écran, panneaux de texte raccourcis ou cachés (la voix les dit). Tester chaque vue à 429×250 et à 1100×560.
7. **Rester dans le programme du prof.** Convertir ce que le diaporama couvre, jusqu'où l'utilisateur le dit (ex.
   « jusqu'à l'activité 3 incluse ») ; rien de « à faire à la maison » (mémoire `programme-hors-cadre`).
8. **Révision du tuteur.** Un petit cours (12 à 16 diapos, environ 30 min) qui reprend les deux chapitres et refait chaque
   méthode sur de nouveaux exemples, en réutilisant les simulations des cours (un objet, un seul dessin).

## L'évaluation formative

- Préparation à la vraie évaluation, **sans chronomètre** : 20 points prévus pour 50 minutes au plus, durée affichée comme
  repère, temps conseillé par partie.
- Chaque réponse est corrigée dès qu'elle est rendue, en un seul essai : QCM, vrai/faux et calculs dans le navigateur (la
  clé est connue ; −0,25 si l'unité manque) ; rédactions par le tuteur (`answer-reaction`, `tentative: 2`, `bareme` et
  `elements`), avec le verdict, les points par élément du barème et la correction rédigée.
- Rien n'est gardé d'une visite à l'autre (règle du lien libre). À la fin : note sur 20, note par partie, questions à revoir.

## La voix

Voix Bodi (academy-v5-bodi), jamais Amine, générée par lot sans tunnel (`/srv/corpus_v4/voix_lot/lancer_lot.sh`) à partir
des fichiers `*_voix.json`. Le lecteur joue une diapo sans voix au temps de lecture, avec les sous-titres.
Le vocabulaire de SVT du Tronc Commun (texture, limon, perméabilité…) est presque absent du corpus de voix : faire écouter
après la génération et passer par le lexique (skill `prononciation`).
