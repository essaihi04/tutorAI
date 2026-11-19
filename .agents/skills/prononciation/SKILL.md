---
name: prononciation
description: Comment corriger un mot que la voix du cours dit de travers (siemens, hématies, cliquer, henry…) et chercher les autres mots du même genre dans tous les cours. À charger dès que l'utilisateur signale un mot, une unité, un sigle ou un nom mal prononcé, une phrase qui boucle ou une piste coupée, et avant de régénérer des voix. Pour écrire le texte parlé d'un cours, voir voix-du-cours.
---

# Prononciation de la voix

La voix (Chatterbox affiné sur des profs marocains, voix Bodi) dit bien ce qu'elle a entendu à l'entraînement
(`corpus_v4/selection_train.jsonl`, 38 852 phrases) et mal le reste. Un mot français vu 0 à 2 fois sort souvent
déformé, et la transcription MoulSot le confirme : « siemens », vu **une fois**, sortait « milliseconde » ou
« millimole » (signalé le 16/11/2026 en chimie ch12).

## 1. Corriger un mot signalé

1. **Trouver les pistes qui le disent**, dans tous les cours et pour tous les types de piste (diapositives,
   réactions, démonstrations, énoncés) : `scripts/voix/pistes_cours.py` les énumère toutes.
2. **Proposer des écritures à l'écoute.** Sur le VPS, kernel d'essai réveillé (`scripts/voix/reveil_essai.py`) :
   `ecoute_prononciation.py "phrase avec {} à la place du mot" écriture1 écriture2 …`. Essayer :
   - l'écriture actuelle (référence) ;
   - une ou deux écritures phonétiques françaises (« si mènsse », « kliké », « émassi », « anri ») ;
   - l'écriture des profs dans le corpus en lettres arabes (`grep` du mot dans `selection_train.jsonl`, par
     exemple « سيمانس »). **Mais** un mot français écrit en lettres arabes peut sortir pire (« كليكي » donnait
     « koliki ») : toujours l'écouter.
   Convertir les WAV en mp3, les mettre dans un dossier du dépôt non suivi par git (`_ecoute_<mot>/`), et les
   envoyer à l'utilisateur. **MoulSot ne sait pas juger** un mot rare : il ne le connaît pas non plus et entend
   un mot voisin quelle que soit l'écriture. C'est **l'oreille de l'utilisateur** qui choisit.
3. **Écrire la règle** dans `PRONONCIATION` de `backend/kaggle_tts/texte_parle.py` (le texte affiché ne change pas,
   seule la lecture change), avec en commentaire la date et ce qui sortait. Couvrir les préfixes (milli, micro),
   le pluriel et la majuscule (`re.I`). Ajouter le cas à `backend/app/tests/test_texte_parle.py`.
   Attention en écrivant la règle par un script : `\b` mal échappé devient un caractère invisible (0x08) et la règle
   ne s'applique jamais. Toujours lancer le test.
4. **Régénérer toutes les pistes concernées** (voir § 3), puis committer règle, test, cours et mp3 ensemble.
   Le kernel en direct reprend `texte_parle.py` au prochain lancement, donc les réponses du tuteur suivent aussi.

## 2. Chercher les autres mots du même genre

`python -X utf8 scripts/voix/mots_a_risque.py [transcriptions.json …]` :
- sans argument : les mots français des textes parlés vus moins de 3 fois à l'entraînement, classés selon le nombre
  de pistes qui les disent (plus de 1 000 mots : la plupart passent bien, la rareté seule ne suffit pas) ;
- avec des transcriptions MoulSot des pistes en ligne : la part des pistes où MoulSot entend chaque mot rare.
  **Un mot rare entendu dans moins de la moitié des pistes est à écouter** (16/11/2026 : millisiemens 0 %,
  siemens 7 %, équivaut 0 %, quarts 14 %, afficheur 18 %). Faire écouter ces mots à l'utilisateur, puis § 1 pour
  chaque mot qu'il juge mal dit.

Les transcriptions se font sur le VPS avec MoulSot v4 (kernel d'essai, `/stt`) :
- découper chaque piste en morceaux de 25 s (le décodeur du kernel s'arrête à **60 s** et le modèle tronque les
  textes longs : une piste longue envoyée entière n'est pas écoutée jusqu'au bout) ;
- l'ordinateur local ne résout pas `trycloudflare.com` : envoyer les morceaux au VPS et transcrire depuis le VPS ;
- le kernel en direct (`academy-tts-direct`) s'endort quand aucun élève ne parle : utiliser le kernel d'essai ;
- deux appels à la fois au plus ; le quota GPU est de 30 h par semaine et par compte (compter ~10 pistes par
  minute) ; prévenir l'utilisateur avant d'entamer le quota de la voix en direct.

## 3. Les autres défauts trouvés à l'écoute

- **Boucle** : le modèle répète un mot ou un groupe (« T trois, T trois, T trois »). Repérée quand la transcription
  répète un groupe de mots qui n'est pas répété dans le texte. Remède : régénérer le morceau (autre tirage) ; si ça
  persiste, reformuler (liste « T un، ل T deux، من بعد ل T trois »).
- **Mot remplacé par un autre** : « la sphère C V » donnait « C quatre ». Écrire le nombre en lettres et isoler
  le mot dans une phrase courte (« و la sphère pédonculée مكتوبة C cinq »).
- **Fin manquante** : la voix s'arrête avant la fin du texte (énoncé de chimie ch12, 16/11/2026). Repérée quand
  la moitié des 10 derniers mots du texte manquent dans la transcription. Remède : générer en morceaux de
  ~300 caractères coupés aux fins de phrase, vérifier chaque morceau.

Régénération vérifiée : chaque morceau est généré, transcrit et refait (3 essais au plus) tant qu'il boucle ou que
sa fin manque ; on garde le meilleur essai, on assemble avec 0,3 s de silence, puis on pose en montant la version
du fichier (`_v<N>.mp3`) pour que le navigateur ne rejoue pas l'ancienne voix en cache.

## 4. Générer avec le bon script : tout le texte passe par `texte_parle.parle`

Demande de l'utilisateur (19/11/2026) : « les voix doivent être générées avec le script correct, qui donne le meilleur
résultat : micros est lu avec le s à la fin, écho est lu parfois avec ch ; vérifier et régénérer, aussi pour les
unités avec du texte (micro seconde…) ». Le modèle n'a appris que des phrases écrites **comme le prof les dit** : des
nombres en lettres, aucun symbole, aucune unité en symbole. Donc :

- **Chaque voix** (diapositive, réaction, démonstration, énoncé, réponse en direct du tuteur) est générée à partir de
  `parle(texte)` de `backend/kaggle_tts/texte_parle.py`. Le serveur du kernel l'applique (`serveur.py`, embarqué au
  push) ; un script qui appelle `/tts` lui-même avec un texte déjà travaillé applique la version du **dépôt** avant
  d'envoyer (le kernel peut tourner avec une version plus ancienne). Jamais de texte brut envoyé sans `parle`.
- **Ce que `parle` écrit en mots** (19/11/2026, `nombres_symboles_unites`) :
  - tous les nombres, entiers et décimaux (« 1,15 » → « un virgule quinze », « 2024 » → « deux mille vingt-quatre ») ;
  - les unités en symbole après un nombre, au singulier (« 20 Hz » → « vingt hertz », « 47 µF » → « quarante-sept
    micro farad », « 0,5 ms » → « zéro virgule cinq milliseconde ») ;
  - les mots « micro / nano / pico + unité » collés, jamais entendus à l'entraînement, en deux mots connus
    (« microfarads » → « micro farad », « microsecondes » → « micro seconde » ; « nanomètre » est gardé) ;
  - les symboles : Δ delta, λ lambda, α, β, π, ω oméga, σ, τ, θ, √ racine de, = égale, × fois, / sur, % pour cent,
    ≈ environ, ≤ ≥ < >, « x → +∞ » tend vers plus l'infini, « A → B » donne ;
  - mots signalés : « micros » → « micro » (le s s'entendait), « écho » → « éko » (lu avec « ch »).
- **En écrivant un texte parlé**, écrire déjà les unités en mots au singulier quand c'est possible ; `parle` rattrape
  le reste.
- **Après chaque nouvelle règle** : lister les pistes dont `parle(texte)` change (comparer l'ancienne et la nouvelle
  version de `texte_parle.py` sur toutes les pistes de `pistes_cours.py`), les régénérer avec
  `refaire_verifie.py` (clés `deck/type/id`, contrôle MoulSot des boucles et des fins), poser en montant la version
  du mp3, puis déployer pour que le kernel en direct reprenne les règles.
