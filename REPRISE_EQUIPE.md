# Reprendre le travail sur ce PC (quand le quota Claude est fini)

Tout le travail est sur ce PC (dossier `C:\Users\HP\Desktop\ai-tutor-bac`), sur le serveur `moalim-vps` et sur la
branche `cours-en-construction`. Rien n'est lié au compte Claude : un autre membre de l'équipe peut continuer.

## 1. Changer de compte
- **Application Claude (bureau)** : en bas à gauche → profil → *Se déconnecter*, puis se connecter avec le compte du
  collègue. Ouvrir l'onglet **Code** et choisir le dossier `C:\Users\HP\Desktop\ai-tutor-bac`.
- **Terminal** : `claude` dans le dossier, puis `/logout` et `/login`.

Restent sur le PC, quel que soit le compte : les fichiers, la mémoire du projet
(`C:\Users\HP\.claude\projects\C--Users-HP-Desktop-ai-tutor-bac\memory\`), la clé SSH du serveur, git.
**La routine cloud** (construction des cours, toutes les 2 h) tourne sur le compte d'origine : elle s'arrête aussi
quand son quota est fini, et repart seule quand il revient.

## 2. Première phrase à donner à Claude
> Lis REPRISE_EQUIPE.md (d'abord le § 3 nonies, le plus récent) et la mémoire du projet, puis continue : voix des
> cours, écoutes à choisir, déploiement avec mon accord, republication du lien libre.

Les sous-agents doivent tourner avec le modèle **Opus**. La voix est toujours **Bodi**, jamais Amine. On ne déploie
le serveur **qu'avec l'accord** du responsable.

## 3. Où en est-on (12 novembre 2026)
- **19 cours** sur le lien libre : https://moalim.online/cours-ondes/?matiere=physique · `?matiere=svt` · `?matiere=maths`
  (math ch1-6, physique-chimie ch1-9, SVT ch1-4). Contrôles du skill cours-concentration : cadre OK partout.
- **Voix** : générée sur le serveur par le compte Kaggle zouhairessaihi (`/srv/corpus_v4/voix_lot/voix_compte2.log`).
  ferdaous04 : quota GPU de la semaine épuisé → relancer quand il revient :
  `ssh moalim-vps bash /srv/corpus_v4/voix_lot/lancer_compte1.sh`
- **Poser les voix prêtes** dans les cours puis republier :
  `bash <scratchpad>/voix_lot/rapatrier.sh 10 <deck> ...` puis `python -I scripts/publier_cours_ondes.py`
  (outils dans le scratchpad de la session : `C:\Users\HP\AppData\Local\Temp\claude\9269525a2680ed40\a857ffbb-cf28-4072-880f-f5ac5134ee69\scratchpad\voix_lot\`
  — à copier ailleurs si ce dossier temporaire est nettoyé).
- **Nouveau cours de la routine** (sur la branche) : réactions (`preparer_reponses.py items` + `blocs.py items` →
  `gen_lot.py` sur le serveur → `poser` / `poser_blocs.py`), énoncés lus (`enonces.py` + `gen_enonces_vps.py`),
  `exporter.py` vers la file des voix, installation sur le serveur, republication.
- **Règle d'écriture** : à l'écran, une formule s'écrit en notation (« g(x) = (2x² − 8)/(x − 2) »), jamais en toutes lettres ;
  les mots (« égale », « au carré ») ne vont que dans la voix.

## 3 bis. Lot de voix en attente (13 novembre 2026)

Les questions en trop ont été retirées des 19 cours (règle 27 : une vraie question par bloc). Quand la
voix enregistrée posait la question à la fin, la fin du texte dit a été coupée : **465 pistes de
diapositives sont à refaire**, et la file du serveur est déjà prête (cours.json à jour, pistes périmées
écartées dans `/srv/corpus_v4/voix_lot/_perimees_13nov/`).

1. allumer le GPU : `ssh moalim-vps bash /srv/corpus_v4/voix_lot/lancer_compte1.sh` (ou `lancer_compte2.sh`) ;
2. suivre : `ssh moalim-vps tail -f /srv/corpus_v4/voix_lot/voix.log` ;
3. poser : `bash <scratchpad>/voix_lot/rapatrier.sh 11 <deck> …` ;
4. republier : `python -I scripts/publier_cours_ondes.py`.

**Ne pas republier avant** : le texte dit a changé, les MP3 en ligne posent encore la question.
Détail et tableau par cours : `docs/audit-questions-progression.md`.

## 3 ter. Règles du 13 novembre 2026 (soir)
Plus de prédiction, fin de bloc = cahier seul, un seul tableau « À toi » par bloc ; les exercices en trop sont gardés
dans `exercices_fin_de_cours` pour une future étape de fin de cours. Détail : `docs/audit-questions-progression.md` § 6.
Quatre cours de chimie (ch10–ch13) ajoutés au lien libre (réactions et énoncés écrits, voix en cours).
**Relancer le lot de voix** : arrêter (`pkill -f "[l]anceur_compte2.py"`), puis `bash attendre_compte2.sh` (attend que le
kernel Kaggle s'éteigne : 2 sessions GPU au plus, sinon le push est refusé et rien ne se fait).

## 3 quater. À reprendre (14 novembre 2026, soir) — cours réécrits en attente de leurs voix

**Ce qui est en ligne** (`main` déployé, lien libre reconstruit sur le serveur) :
- animations manipulables au lieu des tableaux (règle 28) ;
- objets peints en couleur (32) ;
- une seule voix à la fois (29) ;
- questions d'observation avec micro et cartes (30), et leurs 28 voix ;
- cahier avec dessins (31) et ses 12 voix ;
- tableaux de données nés d'une animation (35) ;
- lien libre remis à zéro à chaque visite.

**Ce qui attend : les 23 cours réécrits selon les règles 33 et 34** (une chose à la fois, départ de zéro).
- Ils sont dans `backend/data/courses/en_attente/<deck>.json`, un dossier que le site ne sert pas.
- Les cours en ligne n'ont pas changé.
- Audit et listes de voix : `docs/audit-rythme/README.md` et un fichier par matière.
- Griffith (SVT ch3) : le principe, puis les expériences 1, 2 et 3 une par une, la 4ᵉ trouvée par l'élève (question d'observation), puis le bilan des quatre expériences sur un seul écran (`ig_t1f_bilan`).

### Voix (lot du VPS, compte Kaggle `ferdaous04` seul)
- Le compte 2 (`zouhairessaihi`) n'a plus de quota jusqu'au **21 novembre**, et il reste environ 5,9 h de GPU sur `ferdaous04` cette semaine.
- **Dossiers du lot** : `/srv/corpus_v4/voix_lot/att_<deck>/` ne contient que les pistes sans voix des cours en attente (891 pistes au départ). Les dossiers `<deck>/` gardent les réactions des cours en ligne.
- **Ordre de la file** (relance du 14/11 à 18 h 15) : `VOIX_D_ABORD=att_svt_ch3,svt_ch1,svt_ch2,svt_ch3,att_` (script `lancer_compte1_svt3.sh`). Le tri du lot suit l'ordre de la liste.
- **Suivre** : `ssh moalim-vps tail -f /srv/corpus_v4/voix_lot/voix_compte1.log`.
- **Compter ce qui reste** : `scp scripts/voix/compter_restant_vps.py moalim-vps:/tmp/ && ssh moalim-vps python3 /tmp/compter_restant_vps.py`.
- **Relancer le lot** :
  1. `pkill -f "[v]oix_bodi_lot_nouveau.py"` ;
  2. attendre que `kaggle kernels status ferdaous04/academy-tts-essai` ne soit plus RUNNING ;
  3. `bash lancer_compte1_svt3.sh`, qui charge `/etc/moalim/backend.env`.

  Ne jamais relancer pendant que le kernel tourne : le push est refusé et le lot finit « FIN 0 pistes ».

### Mettre un cours réécrit en ligne (un cours à la fois, SVT ch3 d'abord)
1. **Poser ses voix** : `python -X utf8 scripts/voix/attente_poser.py 12 <deck>`.
   - Le script reprend le MP3 du cours en ligne quand le texte n'a pas changé, et ne convertit que les voix neuves en `*_v12.mp3`.
   - Il lit les WAV dans `att_<deck>/`, puis `<deck>/`, puis `_observations/`, et dit ce qui manque.
   - Il faut **0 diapo manquante**. Une réaction manquante n'empêche pas la mise en ligne : la voix en direct ou l'écrit prend le relais.
2. **Vérifier dans le lecteur**, avec le panneau du navigateur visible :
   - copier la version en attente à la place du cours en ligne, en local seulement ;
   - ouvrir `http://localhost:5173/cours-ondes.html?cours=<deck>&diapo=<id>` ;
   - pour Griffith : chaque expérience à son rythme, la question avant le résultat de la 4ᵉ, puis le bilan.
3. **Mettre en ligne** : remplacer `backend/data/courses/<deck>.json` par la copie en attente, puis la supprimer de `en_attente/`. Commiter le cours et ses `*_v12.mp3`.
4. **Déployer et reconstruire le lien libre, sur le serveur** :
   - `cd /opt/moalim && bash deploy/deploy-ubuntu.sh` ;
   - `python3 scripts/publier_cours_ondes.py --sans-envoi` ;
   - puis remplacer `/var/www/moalim/cours-ondes` par `/tmp/moalim-cours-ondes`.
5. **Recommencer pour les autres cours** au fil du lot. `phys_ch1_waves_exemple` est le seul cours servi aux élèves connectés : le vérifier en dernier, avec le plus de soin.

### Pièges (vus aujourd'hui)
- **Le `main` local est en retard** et plusieurs sessions poussent. Commiter avec un index temporaire construit sur le SHA d'`origin/main`, en n'ajoutant que ses fichiers. Pas de `--force`.
- **Ne jamais commiter** :
  - `deploy/backend.env` : il contient des secrets ;
  - `backend/app/services/reponse_eleve.py` et son test : ce sont de vieilles copies locales ;
  - les copies locales plus anciennes que `main` (comparer avant).
- **Ne pas publier le lien libre depuis le PC** : le disque local contient du travail en cours. Le construire sur le serveur, à partir de ce qui est déployé.
- **Disque C: presque plein** (2 à 4 Go libres) : pas de doublons de MP3, et nettoyer les dossiers temporaires.
- **Restes signalés dans les audits** (non traités) :
  - `ln_e1` donne encore sa conclusion ;
  - le réactif limitant est utilisé en ch9 sans être enseigné ;
  - trois blocs du ch4 de physique n'ont pas de « À toi » ;
  - quelques sujets du national sont encore longs ;
  - la voix de `wx_o1_bouee` parle encore de prédiction ;
  - des réactions écrites à la main sont à faire relire par un professeur.

## 3 quinquies. Point du 14 novembre 2026 (nuit) — 21 cours réécrits en ligne

**En ligne** (déployé, lien libre reconstruit sur le serveur) : SVT ch3 (`cba669d8`), puis 20 cours (`04380ab6`) :
maths ch1-6, physique-chimie ch2-6 et ch8-13, SVT ch1, ch2, ch4. Toutes leurs diapositives ont leur voix ; il manque
encore des réactions (la voix en direct ou l'écrit prend le relais).

**Encore dans `en_attente/`** :
- `phys_ch7_dipole_RL` : sa dernière voix de diapositive (`rl_rp3_derivee`) vient d'être faite par le compte 2 →
  `python -X utf8 scripts/voix/attente_poser.py 12 phys_ch7_dipole_RL`, puis mise en ligne comme les autres ;
- `phys_ch1_waves_exemple` : diapositives complètes, mais c'est le cours servi aux élèves connectés → à vérifier en
  dernier, avec le plus de soin (procédure du § 3 quater).

> **⚠ Quota GPU bas jusqu'à la recharge (≈ samedi 21 novembre)** — relevé le 15/11 à 13 h 45 sur le site Kaggle :
> **ferdaous04 : 8 h 27 restantes**, **zouhairessaihi : 2 h 44 restantes** (le lot de la nuit du 14 au 15 a fait
> ~2 600 voix). Règles jusqu'à la recharge :
> - **ne relancer AUCUN lot de voix** (`lancer_compte1*.sh`, `lancer_compte2*.sh`) ;
> - ferdaous04 est réservé à la **voix en direct des élèves** ; zouhairessaihi ne sert qu'à une voix isolée
>   (`voix_unique_compte2.py`, `attendre_bilan.sh` dans `/srv/corpus_v4/voix_lot/`) ;
> - regarder le quota réel sur kaggle.com (profil → *Your Kaggle Quota*) avant toute génération : le compteur du backend
>   (7 jours glissants, plafond `KAGGLE_TTS_BUDGET_H_SEMAINE=30`) ne compte que la voix en direct, pas les lots ;
> - un kernel qui reste en `QUEUED` = GPU T4 de Kaggle saturés : attendre, ne pas repousser (chaque poussée refait la file).
> - ✅ **fait le 15/11 au soir** : la voix du bilan de physique ch3 (`ol_b1_bilan`, 899 caractères, 3 morceaux,
>   compte 2) est posée en v13, commitée (`ed6585ad`), déployée, et le lien libre est reconstruit. Les réactions muettes
>   de physique ch1-4 et ch11 sont posées aussi (`71f2b3a3`). `poser_en_ligne.py --compter` sur `origin/main` :
>   **0 piste muette** dans tous les cours en ligne.
> - voix isolée sur le compte 2 : `voix_unique_compte2.py <dossier> <id>` lancé avec `setsid nohup` et l'env de
>   `lancer_compte2_inverse.sh` (journal ~4 min : démarrage à froid ~190 s, puis ~20 s par morceau). Si le suivi du
>   journal renvoie `500 Server Error … logs/stream` (panne de l'API Kaggle, vue le 15/11 à 18 h 40) ou si le kernel
>   finit en `COMPLETE` avant la voix (veille de 5 min), relancer simplement plus tard : chaque essai coûte ~10 min de GPU.

**Quota Kaggle revenu sur les deux comptes** (14/11 au soir : ferdaous04 23 h 50, zouhairessaihi 14 h 52) : les
deux lots tournent ensemble, depuis les deux bouts de la file, sans se gêner (une piste déjà écrite n'est pas refaite) :
- compte 1 : `voix_compte1.log` (ordre normal) ;
- compte 2 : `bash /srv/corpus_v4/voix_lot/lancer_compte2_inverse.sh` → `voix_compte2.log` (ordre inverse).
Il restait ~2 650 réactions (≈ 20-50 s chacune). Au fil du lot : `attente_poser.py` ne sert plus que pour les cours
encore en attente ; pour les réactions des cours en ligne, poser avec `rapatrier.sh` / `poser` (§ 3) puis republier.

**Réactions muettes** (« bravo » / « pas tout à fait » sans son) : une réaction sans voix posée est demandée à
la voix en direct ; si le GPU dort, l'élève n'entend rien. Le 15/11 à 0 h : 368 posées et déployées (`f337dd17`),
2 213 encore dans la file du lot (~500/h avec les deux comptes, toutes avec le bon texte). Quand le lot avance :
1. `python -X utf8 scripts/voix/poser_en_ligne.py --compter` (muettes / prêtes par cours) ;
2. `python -X utf8 scripts/voix/poser_en_ligne.py 12 <deck…>` (pose les prêtes dans les cours en ligne) ;
3. commiter cours + `*_v12.mp3` (index temporaire), déployer, reconstruire le lien libre (§ 3 quater, étape 4).

**Vérifier un lot de cours avant mise en ligne** : contenu identique à `origin` hors champs audio, chaque URL
`/media/audio/...` présente sur `origin` ou sur le disque, page qui se charge et voix de la 1ʳᵉ diapo qui part.

## 3 sexies. Point du 15 novembre 2026 (soir, 22 h 50)

**Tout ce qui suit est sur `origin/main`, déployé (serveur sur `858af5df` à 23 h 05) et le lien libre est reconstruit
(23 h 06).** Les figures de chimie ch12-ch13 ont suivi (§ 3 septies).

### Voix
- **394 réactions** muettes de physique ch1-4 et ch11 posées en v13 (`71f2b3a3`) ; **bilan de physique ch3**
  (`ol_b1_bilan`) posé (`ed6585ad`).
- **Prononciation** (hématies, cliquer, MeV, henry, BBT/LDL/HDL, codons) : les 144 pistes touchées sont refaites et
  posées en v13 (`01d8a70c`). Les anciennes WAV sont gardées dans `/srv/corpus_v4/voix_lot/_refaire_prononciation/`.
- **Relance « Suite → »** (`frontend/public/media/audio/reactions/relance-suite.mp3`) : le modèle lisait « كليكي »
  comme « koliki ». Elle est maintenant **en français** : « On continue ? Clique sur la suite. » (`de5598d3`, compte 2,
  script `/srv/corpus_v4/voix_lot/voix_relance_compte2.py` et ses variantes `voix_relance_variantes.py`). Pour un mot
  que le modèle déforme, écrire la phrase en français ou ajouter le mot à `PRONONCIATION` dans
  `backend/kaggle_tts/texte_parle.py` : écrire la darija en lettres arabes ne suffit pas.
- ✅ **Schémas à légender de SVT ch1-ch4 : toutes leurs voix sont faites** (`858af5df`, déployé) : les 9 diapositives
  ajoutées par les sessions cloud et leurs 36 réactions (juste, partiel, faux, aide), plus les 4 réactions de
  `rg_s3_construire` (`bca6bb8f`). Script : `/srv/corpus_v4/voix_lot/voix_textes_compte2.py TEXTES.json SORTIE`
  (compte 2, coupe seul les textes de plus de ~330 caractères ; 39 textes ≈ 15 min avec le démarrage à froid).
- Kaggle à 22 h 50 : aucun lot ne tourne ; seul le kernel `ferdaous04/academy-tts-direct` sert les élèves.

### Questions à choix et schémas à légender (lecteur, déployé)
- **Questions à choix** (`3617412f`) : s'il ne reste qu'un seul choix après une erreur (vrai/faux, autres choix barrés),
  la question se ferme comme une faute avec la réponse ; après une faute, le cours attend « Suite → » (il ne passe seul
  qu'après une bonne réponse) ; au bilan, une compétence avec une question réussie seulement au 2e essai (ou ratée) est
  au mieux « partielle ».
- **Schéma à légender** (`bca6bb8f`, contrat détaillé dans le commit) : la simulation expose `legende_total`,
  `legende_places`, `legende_erreurs`, `legende_mal` et le réglage `corrige` ; la diapositive porte
  `concentration.legende.reactions`. Tant que le schéma n'est pas fini, la question ne s'ouvre pas par-dessus et le
  tuteur ne pose les étiquettes qu'après 60 s sans toucher ; le résultat compte au bilan (0 erreur = du premier coup,
  1-2 = partiel, plus = raté). Modèle : `svt/relation_gene_proteine-tableau/schema_bilan.html` vue `construire`.

### Hors programme
- Retiré et en ligne (`01d8a70c`) : la dichotomie (maths ch1) et les relations du prisme (physique ch3). Les deux
  notions sont marquées hors cadre dans la liste du programme ; seul l'examen national compte.

### Sessions cloud (autre compte de l'équipe)
- Elles ont toutes poussé sur `main` entre 21 h 47 et 22 h 37 :
  - figures agrandies en chimie ch9-ch13 (`ad2142cc` en cours, puis ch9, ch11, ch13 et ch12 jusqu'à `a9e32ded`). La
    session s'était arrêtée faute de crédits ; elle a repris après la recharge de 22 h. **Le ch10 (cinétique) n'a que
    la passe « en cours »** : à vérifier dans le lecteur, ou à finir par une nouvelle session ;
  - schémas à légender comme au bac en SVT ch1-ch4 (`93b39e93`, `886f39f2`, `4d70eeba`, `1bda0bcc`, plus
    `bca6bb8f` fait en local) ;
  - textes qui se chevauchent corrigés dans les simulations tableau de maths, physique, chimie et SVT.
- **Ramené en local** sans pull : `python scripts/recuperer_cloud.py de5598d3 --appliquer` → 135 fichiers, 0 conflit.
  Vérifié à 23 h : tout est déjà en local (`recuperer_cloud.py 3617412f .` → 0 fichier, 0 conflit). Prochaine
  récupération : base `858af5df`.
- Une session cloud qui manque de crédits ne pousse rien. La partager avec l'équipe donne seulement un accès en
  lecture : il faut attendre la recharge du forfait (22 h), puis lui demander de commiter et de pousser sur `main`.

## 3 septies. Point du 16 novembre 2026 (nuit, 2 h 40)

**Serveur sur `8f1a2901` (`main`, déployé à 2 h 16) ; lien libre reconstruit à 2 h 19. 0 piste muette dans tous
les cours** (`python -X utf8 scripts/voix/poser_en_ligne.py --compter`).

### Ce qui est en ligne
- **Figures de chimie ch12-ch13** (session cloud du 1er compte, `c29325df` → `034d20cb`, plus la correction des repères
  du montage de dosage `0d65971c`) : d'abord déployées seules, depuis une branche faite exprès
  (`deploy-figures-chimie` = `858af5df` + 12 fichiers), puis reprises par le déploiement de `main`. Pour déployer une
  partie seulement de `main` : faire une telle branche, puis lancer une copie du script avec la branche changée
  (`sed 's/^BRANCH="main"/BRANCH="<branche>"/' deploy/deploy-ubuntu.sh > /tmp/deploy_branche.sh`). Le déploiement
  normal suivant revient à `main`.
- **Audit « conformité au cadre officiel du ministère »** (sessions du 15/11, 23 h 24 → 16/11, 0 h 48) : programmes
  de maths, physique, chimie et SVT alignés sur les PDF officiels (déposés dans le dépôt, `fd27b164`, `859aa2b2` ;
  règle : le PDF officiel fait foi, AlloSchool en cas de conflit, `ca7996d3`) ; cours de maths ch1-ch6, chimie ch9-ch13,
  physique (8 cours, `d8c09306`) et SVT ch1-ch4 corrigés ; vérification ajoutée aux skills (maths, physique, chimie,
  SVT).
- **159 voix refaites après l'audit** (`8f1a2901`) : 12 diapositives, 146 réactions et énoncés, 1 démonstration, voix
  Bodi, compte 2 (`voix_textes_compte2.py`), posées en **v14** pour ne pas servir l'ancienne voix en cache.
- **Labo** : synthèse de l'acétate de linalyle (tronc commun, le savon est retiré) et CCM pour l'identifier
  (`1d4d86cc`, `9cff8b4d`).
- **Animations plus réalistes** jusqu'à 2 h 16 : chimie (lentes/rapides, deux sens, équilibre, cinétique,
  acide-base, laboratoires peints), physique (ondes, condensateurs, RC), SVT (muscle, levures, mitochondrie).

### Poussé sur `main`, pas encore en ligne (après `8f1a2901`)
- Simulations seulement, aucun cours ni voix : SVT ch1 (cellule, mitochondrie, glycolyse, chimiosmose, ATP, documents),
  ch2 (mitose au microscope), ch3 (pollution de l'air et de l'eau), ch4 (coupes géologiques) peints ; petits défauts
  visuels corrigés dans les tableaux d'ondes (ch1-ch3) ; retouches de RC, RL et RLC (légendes hors des courbes, cadres
  de la carte). Dernier commit : `12aca482` (2 h 30). À regarder dans le lecteur, puis déployer `main`.

### Récupération en local
- Tout `origin/main` jusqu'à `12aca482` est en local (fichiers identiques, 0 conflit). Prochaine récupération :
  `python scripts/recuperer_cloud.py 12aca482 --appliquer`.

## 3 octies. Point du 16 novembre 2026 (matin, 9 h 45)

**Serveur sur `main` (dernier déploiement : celui qui pousse ce point), lien libre reconstruit après chaque
déploiement.** Tout ce qui était « pas encore en ligne » au § 3 septies est en ligne.

### Mis en ligne ce matin
- `12aca482` : SVT ch1-ch4 peints (cellule, mitochondrie, mitose, pollution, coupes géologiques) ; retouches
  des tableaux d'ondes, RC, RL et RLC.
- `48a6fda7` : 2e passe « plus vif » des sessions d'animation, de 8 h 55 à 9 h 21 :
  - chimie : béchers et solutions plus vifs dans les 5 chapitres ;
  - physique : courbes nettes et lumineuses (RC, RL, RLC, radioactivité, nucléaire), ondes ch1-ch3 plus lisibles ;
  - SVT : muscle (couleurs vives, barres peintes, réticulum translucide) ;
  - skill `simulations-au-tableau`, règle 9 : remplir le tableau, écrire grand, rien qui se chevauche ni de minuscule
    (`446a72fe`).
- Puis `38309f62` et `001b7409` (9 h 41) : SVT gène-protéine (ARNt et polymérase en volume) et génétique (cellules,
  noyaux, chromosomes plus vifs, légendes hors des objets).

### Ce que l'utilisateur a remarqué
- Dans le chapitre des ondes (lien libre), seules la **corde, les micros et le sonar** ont été repeints ; ballon,
  milieux, types, carte et bilan n'ont eu que des retouches. Le début du cours paraît donc peu changé. Si l'utilisateur
  veut toutes les animations des ondes repeintes, c'est une nouvelle demande aux sessions d'animation.
- Après un déploiement, recharger avec **Ctrl+F5** avant de juger.

### Récupération en local
- Une récupération faite depuis `8f1a2901` avait raté 65 fichiers poussés entre `858af5df` et `8f1a2901`
  (dont `chimie/shared/chem-lab.js`, le matériel peint des labos de chimie, et la suppression des anciennes voix
  v10-v12 de maths ch1) : rattrapés en relançant depuis `858af5df`. **Leçon : la base de la récupération est le
  dernier commit d'origin déjà récupéré, pas le dernier commit déployé.**
- Tout `origin/main` jusqu'à `001b7409` est en local, sauf les 13 fichiers du labo 3D (`frontend/public/labo/`,
  `scripts/publier_labo.py`), modifiés localement par la session « Labo virtuel synthèse savon » : à fusionner par elle.
- Prochaine récupération : `python scripts/recuperer_cloud.py <commit de ce point> --appliquer`.
- Les autres branches d'origin n'ont rien à récupérer (`deploy-figures-chimie` est dépassée par `main`,
  `claude/tts-api-access-951ccc` date d'août).

## 3 octies. Reprise du 18 novembre 2026 (soir, 19 h 30 UTC) — à faire avec l'autre compte

**État** : la logique des 23 cours a été refaite par des sessions cloud (skills `logique-de-cours`,
`cahier-de-l-eleve`, règles 42-43 du professeur, lexique visuel `docs/lexique-visuel/`) ; les cours refaits
attendent dans `backend/data/courses/en_attente/` (rien n'est en ligne). Sessions cloud encore possibles en cours :
cahier de l'élève (SVT, maths, physique, chimie), 2ᵉ passe maths / physique ch6-ch9, lexique visuel. Elles poussent
sur `main` sans déployer.

**Lot de voix en cours sur le VPS** : 1 226 voix des copies en attente, compte Kaggle 3 (`miftahi`), voix Bodi,
lancé à 18 h 58 UTC (`/srv/corpus_v4/voix_lot/lancer_lot5.sh`, journal `voix_lot5.log`), ~2,6 voix/min →
fin vers 02 h 45 UTC le 19/11. 65 anciennes voix dont le texte avait changé ont été renommées `*.wav.ancien`.

**Une fois fini, dans l'ordre :**
1. Ramener le travail cloud en local (sans pull) : `git fetch` puis
   `python -X utf8 scripts/recuperer_cloud.py 07c02e93 --appliquer` (0 conflit attendu).
2. Vérifier la fin du lot : `ssh moalim-vps tail -3 /srv/corpus_v4/voix_lot/voix_lot5.log` (ligne `FIN`).
3. Poser les voix prêtes : `python -X utf8 scripts/voix/attente_poser.py 17` (ne pose que si le hash du texte est le
   même ; 26 voix avaient été posées en local le 18/11 mais pas poussées, la commande les reprend).
4. Lot complémentaire : les sessions ont changé des textes après la liste. Refaire `live_hash.json`
   (voir la fin de ce point), `python -X utf8 scripts/voix/attente_construire.py`, copier les `att_*` sur le VPS, et
   AVANT de relancer, renommer en `.ancien` chaque WAV de `att_<deck>/` dont le hash de `cours.json` diffère du
   nouveau texte (le lanceur saute un fichier qui existe, même si son texte a changé). Puis `lancer_lot5.sh`
   (compte 3 ; `ferdaous04` reste réservé à la voix en direct ; compte 2 épuisé jusqu'au ~21/11).
5. Écoute automatique (skill `prononciation`, `scripts/voix/refaire_verifie.py`), puis commit sur `main` par index
   temporaire (cours en attente + mp3 v17), essai dans le navigateur, mise en ligne avec l'accord de l'utilisateur.

`live_hash.json` : sur le VPS, pour chaque dossier de `/srv/corpus_v4/voix_lot/` (sauf `att_*` et `_*`, mais avec
`_observations`), `{dossier: {"<sous>/<id>": hash}}` des WAV présents ; à placer dans
`%TEMP%/moalim-voix-attente/live_hash.json`.
Environnement cloud « Default » : script corrigé le 18/11 (YOUTUBE-CHANNEL-2 et tutorAI, num2words à part).

## 3 nonies. Point du 21 novembre 2026 (soir, 19 h) — à reprendre avec un autre compte

**En production** (`moalim-vps`, `/opt/moalim`) : `main` jusqu'à `51f070f9`. Les 23 cours en mode concentration sont
servis aux élèves (`status: published`, `remplace_la_base: true`, `lecon_remplacee: <lessons.id>` ; 7871a423). Le
catalogue en ligne montre 23 cours (physique 8, chimie 5, SVT 4, maths 6).
- Déployer : `ssh moalim-vps 'cd /opt/moalim && bash deploy/deploy-ubuntu.sh'` (si la connexion SSH coupe, vérifier
  ensuite : `systemctl is-active moalim-backend`, `git log -1`, site en 200). **Seulement avec l'accord du responsable.**
- Rafraîchir le lien libre des profs après chaque déploiement :
  `ssh moalim-vps 'cd /opt/moalim && timeout 400 python3 scripts/publier_cours_ondes.py --sans-envoi > /tmp/pub.log 2>&1 && rm -rf /var/www/moalim/cours-ondes.old && mv /var/www/moalim/cours-ondes /var/www/moalim/cours-ondes.old && mv /tmp/moalim-cours-ondes /var/www/moalim/cours-ondes && echo public=ok'`
- Committer sans toucher au checkout local (des copies locales des cours diffèrent d'origin : ne jamais les écraser,
  ni pull, reset, stash ou changer de branche) : `git fetch`, index temporaire (`GIT_INDEX_FILE`) + `read-tree
  origin/main`, objets écrits avec `git hash-object -w` à partir de `git show origin/main:<fichier>`, `commit-tree`,
  `git push origin <commit>:refs/heads/main`. Vérifier avant qu'origin n'a pas changé les mêmes fichiers.

**Nouveau cette semaine (tout est en ligne sauf mention)**
- Bibliothèque en cartes presque carrées, avec image de couverture (`frontend/public/media/images/course-covers/<id>.webp`,
  `catalog.cover_image`), filtre par matière, recherche, « Reprendre » ; carte avec % vu et % de compétences ; bouton
  Détails ; bouton ▦ « Toutes les diapositives ». Plus de bandeau « Leçon terminée » ni de seconde zone voix/messages
  sous un cours en concentration.
- Profil d'apprentissage unique de l'élève (`GET /course-player/profil`), lu par le mode libre (51f070f9).
- SVT : schémas à légender du ch4 avec emplacements et traits de rappel ; extrait du tableau du code génétique à côté
  des questions de traduction (`TableauCode.tsx`, champ `tableau_code`) ; exercices en glisser-déposer
  (`GlisserCode.tsx` : traduction, transcription, brin complémentaire ; `TrousGlisser.tsx` : texte à trous) dans SVT ch1
  à ch4 (exercice de type `glisser`).
- QCM rééquilibrés : la bonne réponse n'est plus la plus longue (b9c2cb79, 0a5c3e22, 17b033fa).
- National : l'énoncé est affiché **et lu** tel qu'imprimé, introduction, remarque et données comprises, jamais un
  résumé (93b4e75b ; règle 46 du skill professeur, dcf62595). Règle 50 sur tous les cours : numéro de la question du
  sujet et figure du sujet commentée (83ad33b5).
- Voix : les nombres se disent **en français**, jamais en darija à côté du français (« deux noyaux », pas « جوج
  noyaux ») : 1 165 textes convertis (8be34bc5, 3539d167), script `scripts/voix/nombres_fr.py [--ecrire] <deck>`,
  skills voix-du-cours et prononciation § 8, consigne du tuteur en direct (`llm_service.py`).
- Prononciation choisie à l'écoute : « lim » → « la limite » (règle écrite) ; plomb inchangé ; **xénon : « le xénon »**
  (le symbole « Xe » était lu lettre par lettre). Demandé : par défaut, un symbole chimique du texte parlé se lit par le
  nom de l'élément (Xe, Sr, Cd, Ag, He, Co, Ni ; ions Cu, Zn, Ca, Al, Mn, Fe, Na, Cl), sauf « La, Ce, Si, Au, Re »
  (mots français) et « Sn » (somme Sₙ). Règle et tests en cours dans la session voix.

**Voix : où en est-on**
- Session « Énoncés par parties : physique ch6 à ch10 » (branche `claude/blissful-rosalind-5b05e6`, worktree
  `.claude/worktrees/blissful-rosalind-5b05e6`) : elle pose les voix prêtes cours par cours (version v23, un commit par
  cours, push à la fin de la boucle) ; 1 015 voix prêtes sur le serveur ; 236 dernières pistes en génération ; puis les
  pistes de la règle des symboles. **Rien de tout cela n'est déployé.**
- Écoutes encore à choisir : 38 mots, index `_ecoute_INDEX.md` dans ce worktree (mp3 dans `_ecoute_<mot>/`). C'est
  l'oreille du responsable qui choisit ; ensuite règle dans `PRONONCIATION` + test, puis régénération.
- Après le prochain déploiement : refaire les phrases du tableau du cache voix dont le texte a changé (nombres en
  français), car le backend les construit à partir des cours déployés.
- Comptes Kaggle : les 4 servent aux lots (zouhairessaihi, miftahi, ferdaous04, zahraoui). ferdaous04 n'est plus
  réservé : la voix en direct est en panne (Kaggle coupe le tunnel). zahraoui : lots sans tunnel seulement ; s'il est
  annulé, ne pas relancer en boucle. Ne jamais pousser une nouvelle version d'`academy-v5-bodi` ni
  d'`academy-moulsot-v4` (leur sortie garde les poids). Sur le PC, `~/.kaggle/credentials.json` passe avant les
  variables : lancer avec `KAGGLE_CONFIG_DIR` vide, et l'`id` de `kernel-metadata.json` doit être celui du compte.
  Changer une clé : `ssh -t moalim-vps bash /root/poser_kaggle4.sh`.
- Sorties des lots sur le serveur : `/tmp/kaggle_lot_sortie_*/` (`rapport.json` + `voix/`).

**Disque C: presque plein** : le 21/11 il est tombé à 0 Mo et a tout bloqué. Caches vidés (codex-runtimes, npm, pnpm,
Temp de plus de 2 jours) : ~780 Mo libres. Les worktrees des sessions prennent ~9 Go ; à nettoyer quand leurs
sessions sont finies (Réglages › Ce PC › Stockage). Pas de place → la pose des voix s'arrête.

## 4. Ce qui attend une décision
- Écouter et choisir les 38 mots douteux (§ 3 nonies), puis les symboles chimiques douteux.
- Déployer les voix posées par la session voix (nombres en français, règle 50, symboles), puis rafraîchir le lien libre.
- Repeindre aussi ballon, milieux, types, carte et bilan du chapitre des ondes, si l'utilisateur le veut (§ 3 octies).
- Passer le nouveau lecteur sur `main` pour les élèves connectés, après la relecture des profs.
