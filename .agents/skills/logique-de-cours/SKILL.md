---
name: logique-de-cours
description: Revoir puis refaire la LOGIQUE d'un cours existant (ordre des séances, parties, diapositives, expériences, animations et exercices d'examen), en justifiant chaque choix par les cours en ligne des profs, le cadre officiel et le national, avec les mots les plus simples et les mieux dits par la voix. À charger dès qu'on demande si un cours est logique, de réorganiser un cours, de penser son architecture, ou de refaire un cours de SVT, maths, physique ou chimie. Pour écrire un cours neuf : exploration-de-cours puis cours-concentration ; cette skill les complète.
---

# Logique d'un cours

Demande de l'utilisateur (18 novembre 2026), après l'analyse du cours SVT ch1 : « il y a une pensée derrière
chaque choix ; ne pas mettre les animations et les diapositives au hasard ». Un cours se juge à ce que l'élève sait
encore plus tard, pas à sa beauté.

## Les règles de l'utilisateur, à tenir partout

1. **Une raison pour chaque choix.** Chaque séance, partie, diapositive, animation et exercice a sa place pour une
   raison écrite (§ 3). Rien n'est mis parce que « c'est joli » ou « on l'avait déjà ».
2. **Les mots les plus simples et les mieux dits.** La darija courante des profs, des phrases courtes, une idée
   par phrase ; les mots du programme et des examens en français (skill voix-du-cours, § 1). Chaque texte que la voix
   dira passe par `python -X utf8 scripts/voix/verifier_mots.py <deck> <ids>` : un mot vu moins de 3 fois par la voix
   à l'entraînement se remplace par un mot courant (le vérifier aussi). Un terme du programme rare se garde, mais il
   va dans la liste des voix à écouter (skill prononciation).
3. **Ne pas tout donner au départ ; laisser le temps à l'élève de trouver seul.** Principe → question → chaque cas
   joué seul, arrêté, avec un temps pour regarder → le cas décisif posé en question → le résultat et la conclusion
   seulement après la réponse de l'élève (skill professeur, règles 33-34). Le bilan de toutes les expériences vient
   après la dernière, pas avant.
4. **L'expérience avant le mécanisme qu'elle prouve.** L'élève tire le résultat du document ; on ne lui affirme pas
   un résultat qu'une expérience montrera plus loin (au national, près de 75 % des points sont du raisonnement sur
   documents).
5. **Démonstrations et exercices d'examen simples, animés, expliqués pas à pas.** Un exercice type du national se
   joue en étapes : le document apparaît, une seule consigne à la fois (décrire, puis déduire, puis expliquer), la
   réponse de l'élève avant la correction, la correction écrite comme le barème la lit. Une valeur comparée, l'effet
   d'un paramètre, une suite d'étapes → petite animation au tableau que l'élève manipule (≤ 2 curseurs), pas un
   tableau à lire ; un tableau de données naît de l'animation qui produit ses valeurs (skill professeur, règles 28 et
   35). Un vivant ou un objet réel est peint en couleur, réaliste (règle 32).
   **Pour expliquer une activité dont le résultat change** (dans le temps, d'un compartiment à l'autre, avant /
   après, avec / sans), **l'animation autant que possible**, pas un tableau de résultats suivi d'encadrés de texte :
   ce qui bouge se voit bouger, chaque temps est un moment arrêté, la conclusion s'écrit après la réponse de l'élève.
   **Mais pas « jamais de tableau »** : quand le bac donne ce genre de résultats en tableau, l'animation se change
   ensuite en ce tableau, à la manière de l'examen, et l'élève apprend à le lire lui-même. **Combiner texte, tableau
   et animation selon le besoin, avec une raison écrite** : le texte pour ce qui se dit une fois et se recopie,
   l'animation pour ce qui change et doit se comprendre, le tableau pour ce que l'examen donne en tableau ou ce qui se
   compare d'un coup d'œil (skill professeur, règle 42 ; exemple : le glucose marqué au ¹⁴C de SVT ch1, 18/11).
   Toujours vérifié à la taille d'un téléphone en paysage (~724 × 350) : rien sous la barre du lecteur.
6. **Départ de zéro.** Les notions des années d'avant (mitose, mole, vecteur, dérivée…) sont enseignées au moment
   où elles servent, jamais supposées connues ; chaque notion difficile est expliquée deux fois, de deux façons.
7. **La limite de l'élève.** Mémoire de travail ≈ 4 éléments : une idée nouvelle par diapositive ; quand la limite
   est atteinte, on arrête d'expliquer → cahier (avec dessin si la notion se dessine) → exercice qui fixe. Séances de
   40 à 50 min.
8. **Rien hors du cadre.** Chaque partie cite sa notion de `backend/data/curriculum/perimetre.json` ; jamais de
   partie « pour les devoirs » ; ne jamais élargir le cadre pour faire passer un contenu.
9. **L'écran.** Formules écrites en notation à l'écran (« v = d/Δt »), les mots seulement dans la voix ; aucun texte
   sous 15 px ; tout tient dans un écran sans défilement, y compris sur téléphone en paysage (~724 × 350 px).

10. **Un objet, un seul dessin, dans tout le cours.** Une molécule, un organite, un ion, un composant gardent la même
   forme, la même couleur et la même étiquette sur toutes les diapositives et dans toutes les simulations (le glucose
   de SVT ch1 : une chaîne droite de 6 billes jaunes, jamais deux rangées de 3) ; ce qu'il devient se dessine à partir
   de lui. **Le même dessin dans tous les cours et toutes les matières, y compris les prochains** : le lexique visuel
   commun est `docs/lexique-visuel/` (une fiche par élément avec toutes ses formes : brute, développée,
   semi-développée, cyclique, forme simplifiée des animations ; la forme se choisit selon le besoin), et chaque objet
   se dessine par la fonction du module partagé `frontend/public/media/simulations/shared/lexique/` ; un nouveau
   cours va d'abord au lexique (skill simulations-au-tableau, règle 15 ; skill professeur, règle 43).

## La procédure

### 1. Lire
Les skills `cours-concentration`, `professeur`, `exploration-de-cours`, `voix-du-cours`, `prononciation`,
`simulations-au-tableau`, `scientific-course-visuals`, `suivi-des-acquis` ; le cours (`backend/data/courses/<deck>.json`
et, s'il existe et diffère, `backend/data/courses/en_attente/<deck>.json` : la version en attente est la plus
récente, on part d'elle) ; son exploration (`backend/data/curriculum/exploration/<clé>.json`) ; le cadre
(`backend/data/curriculum/<matière>.json`, `perimetre.json`, `cadre_reference_2bac_pc.json`) ; les nationaux
(`backend/data/exams/`).

### 2. Voir la logique actuelle
Extraire le plan : séances → blocs → parties → diapositives (id, type, titre, compétence), questions et exercices.
Pour chaque diapositive : ce qu'elle apprend, ce qu'elle suppose déjà su, si elle affirme un résultat qu'une
expérience ne prouve que plus loin, si elle donne tout d'un coup, si son animation sert une étape ou décore.

### 3. Comparer, puis décider avec une raison
- **Les profs** : l'exploration (10 vidéos) donne l'ordre commun (« convergences ») ; si elle manque, chercher au
  moins 3 à 5 cours complets en ligne du chapitre (vidéos et cours écrits marocains : Moutamadris, Dyrassa,
  AlloSchool…) et relever leur plan. Un PDF dont le texte ne sort pas se lit avec PyMuPDF (`fitz`).
- **Le cadre** : l'ordre des notions et les capacités ; chaque capacité est travaillée, rien en dehors.
- **Le national** : la fréquence de chaque cas type (exploration, `cas_types`) dit où mettre du temps et quels
  exercices animer.
- **Les difficultés des élèves** (`commentaires_eleves`, `notions_complexes`) : où couper en petites marches.
Règle de décision : on suit l'ordre commun des profs (l'élève le retrouve chez son prof et dans ses livres), sauf
quand nos règles 3 à 6 demandent autre chose (une preuve avant son résultat, un prérequis juste avant son usage) ;
on écrit alors pourquoi.

Écrire l'architecture dans `backend/data/curriculum/architecture/<deck>.md` : les séances et leurs parties, chaque
diapositive avec **pourquoi ici** (la source : profs, cadre, national, difficulté), les animations et exercices
animés prévus, ce qui change par rapport au cours en ligne et ce qui reste (avec la raison), les sources consultées.

### 4. Appliquer
- Travailler dans `backend/data/courses/en_attente/<deck>.json` (copie du cours en ligne, ou de la version en attente
  si elle est plus récente). **Ne jamais modifier le cours en ligne** `backend/data/courses/<deck>.json` : il reste
  servi aux élèves avec toutes ses voix jusqu'à ce que la nouvelle version ait les siennes.
- Déplacer plutôt que réécrire : une diapositive qui garde son id et son texte garde sa voix (`speech_hash`).
  Réécrire seulement ce qui doit l'être (liaisons, phrases qui renvoient à une diapositive déplacée, diapositives
  fusionnées ou nouvelles, exercices animés) ; un texte changé perd sa voix (retirer son `audio` pour qu'il soit
  compté dans les voix à faire).
- Recouper `seances` (blocs de 40 à 50 min, une compétence principale par bloc) et `competences` selon le nouvel ordre.
- Une animation nouvelle ou modifiée suit `simulations-au-tableau` (mode large, ≥ 15 px, téléphone en paysage).
  Ne pas modifier les fichiers partagés (`frontend/public/media/simulations/shared/`, le lecteur `frontend/src/`) :
  noter le besoin dans l'architecture.

### 5. Vérifier
- Le JSON se charge ; `cd backend && python -m pytest -q app/tests -k "course or cours or concentration"` passe.
- `scripts/voix/verifier_mots.py` sur chaque piste réécrite : aucun mot rare sans raison écrite.
- Liste des pistes à mettre en voix dans `backend/data/curriculum/architecture/<deck>_voix.json`
  (`{"deck", "pistes": [{"type", "id", "texte"}]}`) ; les voix se font plus tard sur le VPS (Kaggle, voix Bodi).
- Relire l'architecture contre les règles 1 à 9 ci-dessus, diapositive par diapositive.

### 6. Livrer
Commits clairs sur `main` (sans `--force`, après `git pull --rebase` ; si un fichier a bougé entre-temps, fusionner
à la main en gardant les deux travaux) ; ne jamais déployer. Le rapport final dit : la logique avant et après, les
grandes décisions et leurs raisons, le nombre de pistes à mettre en voix, ce qui n'a pas pu être fait.
