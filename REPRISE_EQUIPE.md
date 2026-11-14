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

## 4. Ce qui attend une décision
- Déployer la correction des questions de reprise (formules écrites) — commit prêt, pas encore déployé.
- Passer le nouveau lecteur sur `main` pour les élèves connectés, après la relecture des profs.
