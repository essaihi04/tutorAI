# Audit « rythme et départ de zéro » — consignes communes (14 novembre 2026)

Demande de l'utilisateur, à partir de l'expérience de Griffith (SVT ch3, diapo `ig_t1_griffith`) :

> il donne tout d'une manière rapide, l'élève ne peut pas le suivre ; à chaque expérience il doit donner le temps nécessaire pour voir la manip et la comprendre, et ensuite les résultats ; plusieurs infos successives risquent de ne pas être suivies. D'abord expliquer le principe de l'expérience et poser une question pour vérifier s'il a compris ; les 4 expériences, chacune expliquée doucement en laissant le temps à l'élève de suivre ; et la dernière expérience, ne pas donner le résultat directement : une question libre (comme nous l'avons conçue), le laisser réfléchir. […] Considérer que l'élève ne connaît rien : on commence dès zéro, chaque notion doit être expliquée et réexpliquée d'une autre manière pour être ancrée. Par exemple, le cours a commencé par la mitose et les chromosomes alors que la plupart des élèves ne connaissent pas encore ces notions, malgré qu'ils les aient étudiées. Une audit complète détaillée de tous les cours de toutes les matières ; écrire les nouveaux scripts et les mettre en attente ; s'il y a des simulations à rajouter, les créer.

## Les règles à appliquer (à lire en entier)

- `.agents/skills/professeur/SKILL.md` : règles **33** (une chose à la fois) et **34** (départ de zéro, deux explications), et aussi 27 (ne demander que ce qui est enseigné), 28 (animations), 30 (question d'observation), 32 (réalisme).
- `.agents/skills/cours-concentration/SKILL.md` : la construction d'un cours (données, `pointage`, `concentration`, blocs de 3–4 diapos, une seule question « À toi » par bloc).
- Skill `voix-du-cours` (dans `.agents/skills/`) pour écrire `speech_text.mixed` : darija simple, termes du programme en français, nombres et unités en mots, pas de chiffres ni de symboles, pas de tachkil.

## Exemple de question d'observation (règle 30), déjà en ligne

`backend/data/courses/svt_ch2_role_muscle_strie_squelettique.json`, diapo `ms_t3_sans_dioxygene`, champ `concentration.observation`. Il contient :
- `apres_mot` : mot de la voix où la question se pose ;
- `sim_avant` / `sim_apres` : paramètres envoyés à la simulation, par exemple `conclusions: false`, puis `true` ;
- `gestes` : commandes du tuteur ;
- `enonce` / `enonce_dit` : la question écrite et la question dite ;
- `silence_s` : le temps laissé à l'élève pour regarder ;
- `indices` : les aides données si l'élève ne trouve pas ;
- `choix` : les trois cartes ;
- les réactions.

Le lecteur : `frontend/src/components/course/CourseFocusStage.tsx` ; les types : `frontend/src/components/course/types.ts` (`QuestionObservation`).

## Où écrire — très important

- **Ne pas modifier les cours en ligne** (`backend/data/courses/<deck>.json`). Leur voix enregistrée doit rester juste.
- Écrire la nouvelle version complète du cours dans **`backend/data/courses/en_attente/<deck>.json`**. Ce dossier n'est servi ni par le site ni par le lien libre. Partir de la copie en ligne.
  - Sur chaque diapo dont `speech_text.mixed` change, ou qui est nouvelle : retirer `audio.mixed` (la voix Bodi sera enregistrée plus tard, quand un GPU Kaggle sera libre).
  - Mettre à jour `pointage` (des extraits exacts de la nouvelle voix), `cahier`, `seances[].blocs[]` (une seule question « À toi » par bloc) et `competences[].slide_ids`.
  - Pour chaque nouvelle question : ses réactions préparées (`concentration.reponses`, juste / faux 1 / faux 2, avec `parole` et `ecrit`), sans `audio`.
- **Simulations** :
  - Créer de nouveaux fichiers à côté de ceux du cours.
  - Une simulation existante peut être enrichie **sans casser ce qu'elle fait aujourd'hui**, car le cours en ligne l'utilise encore : nouvelle vue `?vue=…`, nouveaux `moments`, nouveau paramètre comme `conclusions`. Tout ce qui existe doit garder le même comportement par défaut.
  - Style : craie et objets réels peints en couleur (règle 32), cadre 760 × 420, `repere`, `moments`, `play_until`, `set_parameters`, `ce_qui_se_voit`.
- Écrire en JSON avec `ensure_ascii=False` et `indent=2`, fins de ligne LF.

## Ce qu'il faut rendre

1. **`docs/audit-rythme/<matière>.md`** : l'audit détaillé, cours par cours et diapo par diapo, en français :
   - ce qui va trop vite (plusieurs expériences, résultats ou idées d'un coup) ;
   - le résultat décisif donné au lieu d'être trouvé ;
   - les prérequis supposés connus ;
   - les notions expliquées une seule fois ;
   - et pour chaque point, ce qui a été fait.
2. Les copies en attente dans `backend/data/courses/en_attente/`.
3. Dans l'audit, la **liste des voix à enregistrer** : pour chaque cours, les id des diapos à voixer, les énoncés et les réactions.
4. La vérification :
   - `node --check` sur les simulations nouvelles ou modifiées ;
   - chaque `mot` du pointage est bien dans sa voix ;
   - chaque `moment` et chaque `repere` cités existent ;
   - le JSON est valide.
   - Si possible, ouvrir les simulations dans un navigateur sans écran (Playwright) : le serveur Vite tourne sur http://localhost:5173 ; ou servir `frontend/public` avec `python -m http.server`.

Ne jamais commiter, pousser ni déployer.
