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

5. **Choisir par une page d'écoute en lot** (24/11/2026) : quand le kernel d'essai n'est pas allumé, mettre les écritures dans un petit lot Kaggle (une clé par écriture, v1 = l'écriture actuelle, dans une phrase courte du cours) et publier la page groupée par mot (skill voix-du-cours, § 3 quater). Exemples choisis : « أفقي » → « أوفوقي » (ofoqi), « برر » → « بَرِّر » (barrir). Écrire la règle avec `lambda mt: mt.group(1) + "…"` : un `r""` passé par un heredoc devient l'octet 0x01. Déployer avant de régénérer les pistes : le lot lit `texte_parle.py` dans `/opt/moalim`.

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

## 5. Les mots compliqués : les faire écouter AVANT de générer

Demande de l'utilisateur (19/11/2026, après « fœtus ») : « ajouter au skill, pour générer des voix, les mots pareils
ou tous les mots compliqués ». Avant de générer les voix d'un cours (nouvelles pistes ou textes changés) :

1. **Lister les mots à risque** des textes à générer : `python -X utf8 scripts/voix/verifier_mots.py <deck> [ids]`
   (mots vus moins de 3 fois à l'entraînement) et, en plus, à l'œil : termes scientifiques rares (fœtus,
   échographie, siemens…), mots français écrits en lettres arabes (« للفيتوس »), unités et préfixes collés, sigles,
   noms propres, symboles.
2. **Pour chacun, 2 à 4 écritures à l'écoute** (`ecoute_prononciation.py`, § 1) dans une phrase réelle du cours :
   l'écriture actuelle, une écriture phonétique française (« le fétusse », « éko », « si mènsse »), le mot arabe que
   les profs disent quand il existe dans le corpus (« الجنين », 8 fois), et le mot coupé en mots connus
   (« micro farad »). Envoyer les mp3 à l'utilisateur ; **son oreille choisit** (MoulSot aide seulement à éliminer).
3. **Écrire la règle choisie** dans `PRONONCIATION` (+ test), puis seulement générer les voix.
4. Garder ici la liste des écritures choisies, pour ne pas reposer la question :

| Mot écrit | Dit par la voix | Date |
|---|---|---|
| hématies | émassi | 15/11/2026 |
| cliquer, clique | kliké, klik | 15/11/2026 |
| siemens (milli, micro) | si mènsse | 16/11/2026 |
| henry (unité) | anri | 16/11/2026 |
| micros | micro | 19/11/2026 |
| écho | éko | 19/11/2026 |
| microfarad, microseconde… | micro farad, micro seconde | 19/11/2026 |
| fœtus, للفيتوس, فالفيتوس | le fétusse | 19/11/2026 |
| lim | la limite | 21/11/2026 |
| Xe, xénon | le xénon | 21/11/2026 |

**Symboles des éléments, règle par défaut (21/11/2026).** Un symbole d'élément SEUL se lit par le nom de l'élément,
comme « Xe » → « xénon » choisi à l'écoute (`texte_parle.symboles_elements`, même table que `speech_normalizer.py`) :
« m de Xe », « A ديال Sr », « Cu deux plus » → « cuivre deux plus ». Dans une formule (voisin = autre symbole ou lettre
capitale : « Fe Cl trois », « C O deux ») il reste épelé. Jamais pour les mots français et la notation maths : La, Ce,
Si, Au, Re, Sn (la somme Sₙ), Ne, Se, In, As, Pa, Te ; Po et Rn gardés quand ils sont dits exprès (« de symbole Po »).
Un nouveau symbole douteux à l'oreille : le faire écouter (§ 5) avant de l'ajouter.

## 6. Écrire d'office les mots rares de la manière la plus sûre

Demande de l'utilisateur (19/11/2026) : « nous avons déjà quelques mots avec leur erreur et leur correction ; les
prochains mots avec le même problème, ou dont on n'est pas certain qu'ils soient bien prononcés, il vaut mieux les
écrire de la manière la plus sûre, comme micros et fœtus ; généraliser cette règle ». On n'attend plus qu'un mot soit
signalé : **tout mot vu moins de 3 fois à l'entraînement reçoit d'office l'écriture sûre** quand un cas déjà corrigé
s'applique :

| Cas déjà vu | Écriture sûre | Exemples |
|---|---|---|
| « s » final muet, le mot sans « s » est connu | retirer le « s » (le son est le même) | micros → micro, ohms → ohm, codons → codon |
| mot latin en « -us » dont le « s » se dit | « -uss » | fœtus → fétusse, locus → locuss, stimulus → stimuluss |
| « ch » dit « k » (mots grecs) | « k » | écho → éko, chlorure → klorure, chronomètre → kronomètre |
| mot collé préfixe + unité | deux mots connus | microfarad → micro farad, microseconde → micro seconde |
| unité, nombre ou symbole | en mots | 20 Hz → vingt hertz, Δ → delta, √ → racine de |
| mot français écrit en lettres arabes | le mot français en écriture sûre | للفيتوس → ل le fétusse |

Comment : `python -X utf8 scripts/voix/ecritures_sures.py` liste les écritures proposées pour tous les cours ;
`--ecrire` les met dans `texte_parle.py` (bloc `ECRITURES_SURES`, généré, à ne pas modifier à la main ; les mots
choisis à l'écoute dans `PRONONCIATION` passent avant). **À relancer à chaque nouveau cours ou texte changé, avant de
générer ses voix**, puis régénérer les pistes dont le texte parlé change (§ 4). Seuls les mots rares pour lesquels
aucun cas ne s'applique, ou dont l'écriture sûre reste douteuse, passent à l'écoute de l'utilisateur (§ 5).

## 7. Les notations : symboles, fonctions, indices et exposants

Règle de l'utilisateur (19 novembre 2026, sur « Rappel : ln enlève e » du ch4 : « parfois il dit L N, pas ln
rassemblé ; vérifier tous les cas, et l'appliquer pour toutes les générations, et aux autres symboles ou fonctions »).
Une notation n'est jamais envoyée telle quelle à la voix : elle est écrite comme le prof la dit, d'un seul bloc.
`notation_maths()` et `_FONCTIONS` dans `backend/kaggle_tts/texte_parle.py` (appelés par `parle()`, donc par toute
génération) font :
- **fonctions notées en lettres** : `ln`, `exp`, `sin`, `cos`, `tan` toujours détachées (« ln2 » → « ln deux »,
  « lnx » → « ln x ») ; « l n », « Ln », « LN » → « ln » (l'écriture « ln » est celle choisie à l'écoute,
  `_ecoute_ln/ecoute_1_ln.mp3`) ; appel de fonction « f(x) », « ln(x) », « F(x₀) » → « f de (x) » ;
- **prime** : « u′ », « f'(x) » → « u prime », « f prime de (x) » ;
- **indices** : « uₙ₊₁ » → « u n plus un », « x₀ » → « x zéro » (les formules chimiques H₂O gardent leur règle) ;
- **exposants** : « x² » → « x au carré », « x³ » → « x au cube », « x⁴ » → « x puissance quatre », « qⁿ » →
  « q puissance n », « f⁻¹ » → « f moins un » ; « ^ » → « puissance » ;
- **nombre collé à une lettre** : « 6x » → « six x » (pas « 3e ») ; « deux√x » → « deux racine de x » ;
- **signes** : « + » entre espaces → « plus », « -ln » après une espace → « moins ln » (les autres : § 4, `SYMBOLES`).

Avant de générer un cours, inventorier ce qui reste après `parle()` : tout caractère hors lettres, chiffres et
ponctuation simple (indices, exposants, ′, |, [ ], ^) et toute suite de lettres qui n'est pas un mot (pH, pKa, Qr,
Ka, lim, arg, max) ; une notation nouvelle reçoit sa règle et son test (`test_notation_maths`) avant la génération.
Une notation dont la lecture est douteuse passe à l'écoute (§ 5). Après un changement de règle, la liste des pistes
dont le texte parlé change se calcule en comparant l'ancien et le nouveau `parle()` sur toutes les pistes
(`scripts/voix/pistes_cours.py`), et ces pistes sont régénérées (le 19/11/2026 : 49 pistes). Sur le VPS, la copie
`_stt_tous/texte_parle_depot.py` (lue par `refaire_verifie.py`) est remplacée par le nouveau fichier à chaque fois.

## 8. Les nombres toujours en français, même dans une phrase en darija

Règle de l'utilisateur (21 novembre 2026) : « ne pas dire les chiffres en arabe + le mot en français ; c'est mieux de
dire le tout en français ; par exemple pour 2 noyaux il dit جوج noyaux ». Un nombre qui touche un mot français, une
unité ou une opération est écrit en français dans le texte parlé : « deux noyaux », « trois courbes » (pas « تلاتة ديال
les courbes »), « les deux courbes » (pas « بجوج »), « deux fois » (pas « جوج مرات »), « zéro virgule zéro six mètre »,
« six virgule cinq fois dix puissance moins sept ». « واحد » article (« واحد la courbe ») n'est pas un nombre et reste.
Avant de générer : `python -X utf8 scripts/voix/nombres_fr.py <deck…>` liste ce qui reste, `--ecrire` le convertit dans
les fichiers des cours (les deux copies ; les mots du pointage sont réalignés). Les pistes dont le texte change sont
régénérées (§ 4). Le 21/11/2026 : 1 165 phrases converties, 687 pistes à refaire dans les 23 cours.

**Élargie le 22/11/2026** (l'utilisateur : « ne pas mélanger arabe et français dans deux mots successifs ») :
- les **opérateurs** d'une formule aussi : « x plus un », « k égale trois », « dix puissance moins cinq », « deux sur
  sept », « supérieur ou égal à », jamais « x زائد واحد », « k يساوي trois », « dix أس ناقص خمسة », « deux على sept »,
  « كبر ولا يساوي » ; les **centaines en un mot** (« تسعمية nanomètre » → « neuf cents nanomètre ») ; les **décimales
  chiffre par chiffre** après « virgule » (« un virgule خمسة سبعة » → « un virgule cinq sept ») ;
- les **mots cassés** : un mot français entièrement en lettres latines, un mot darija entièrement en lettres arabes
  (« فالنoyau » → « فالnoyau », « زéro » → « zéro », « مètre » → « mètre », « Mزيان » → « مزيان », « fين » → « فين ») ;
- un comptage tout en darija (« جوج طرق ») reste : la règle ne vise que deux mots successifs, l'un darija, l'autre
  français.
**Forcée dans le code** : `parle` applique `nombres_darija_fr` (dans `backend/kaggle_tts/texte_parle.py`) en premier, pour
toutes les voix, y compris les **réponses libres du tuteur** (voix en direct) ; le prompt du tuteur (`llm_service.py`)
donne la même consigne. Tests : `backend/app/tests/test_texte_parle.py` et `scripts/voix/test_nombres_fr.py`. Après
une modification, repousser le kernel en direct (il embarque `texte_parle.py`) et copier le fichier dans
`/srv/corpus_v4/voix_lot/_stt_tous/texte_parle_depot.py` (§ 7). Le 22/11/2026 : 833 pistes corrigées et revoisées (v25).
- **Contrôle après génération** : comparer les nombres du texte et ceux de la transcription (MoulSot). La voix peut
  déformer un nombre pourtant bien écrit (« huit cents » entendu « deux cent vingt » dans `ol_l8_ordre_grandeur`) :
  une piste dont les nombres entendus diffèrent est écoutée, puis régénérée.
