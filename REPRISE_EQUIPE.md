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
> Lis REPRISE_EQUIPE.md et la mémoire du projet, puis continue : voix des cours, nouveaux cours de la routine,
> republication du lien libre.

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

## 4. Ce qui attend une décision
- Déployer la correction des questions de reprise (formules écrites) — commit prêt, pas encore déployé.
- Passer le nouveau lecteur sur `main` pour les élèves connectés, après la relecture des profs.
