# Audit : les questions d'association des 23 cours

19 novembre 2026. Demande de l'utilisateur, sur SVT ch1, national 2020 rattrapage, question III « Reliez chaque
phénomène à la réaction bilan qui lui convient… », découpée en trois QCM : « pour les questions d'association, ne pas les
transformer en QCM ; les mettre en association avec un feedback à chaque réponse, correcte ou fausse ».
Règle : skill `professeur` règle 47, skill `logique-de-cours` règle 11.

## Le contrat du lecteur

Une diapositive pose une association avec `question.type: "association"` et `question.association`
(`frontend/src/components/course/types.ts`, `AssociationQuestion`) ; un exercice de diapositive aussi
(`exercises[i].type: "association"` + `association`, clé `e<i>`). Rendu : `AssociationDiapo.tsx`, branché dans
`UneQuestion` (`CourseFocusStage.tsx`).

```json
"question": {
  "type": "association",
  "prompt": "Reliez chaque phénomène à la réaction bilan qui lui convient. (2020 R, 1 pt)",
  "enonce_dit": "…",
  "association": {
    "gauche": [{"id": "1", "texte": "La glycolyse"}, …],
    "droite": [{"id": "a", "texte": "C₆H₁₂O₆ + … → …"}, …, {"id": "e", "texte": "…"}],
    "couples": {"1": "c", "2": "e", "3": "b", "4": "a"},
    "melanger": false,
    "essais": 2,
    "retours": {
      "1-c": {"juste": true, "texte": "écrit : juste, et pourquoi", "dit": "darija dite par la voix", "audio": "(piste, quand elle existe)"},
      "1-b": {"juste": false, "texte": "ce qui ne va pas + un indice", "dit": "…"},
      "1-*": {"texte": "retour par défaut d'une paire fausse de l'élément 1", "dit": "…"}
    },
    "bilan": {"texte": "d est la réaction de trop…", "dit": "…", "audio": "…"}
  }
}
```

- **Relier** : glisser un élément sur un élément de l'autre colonne (souris ou doigt), ou toucher l'un puis l'autre,
  dans les deux sens ; clavier : Entrée / Espace.
- **Colonne de droite** : battue par défaut (les étiquettes « a- », « b- » restent) ; `melanger: false` garde l'ordre
  du sujet. Elle peut avoir des éléments de trop (l'intrus du sujet).
- **Retour à chaque paire**, écrit sous les colonnes et dit par la voix (`audio`, sinon `dit` par la voix en direct) :
  juste → la paire reste reliée, même couleur des deux côtés ; fausse → les deux éléments rougissent, se délient, le
  retour dit ce qui ne va pas et donne un indice, jamais la lettre. Après `essais` erreurs (2 par défaut) sur le même
  élément de gauche, la bonne paire est posée pour lui avec son retour (« ➜ La bonne paire : … »), et compte comme
  donnée.
- **Bilan** : toutes les paires posées → « 📝 Les couples : (1 ; c) (2 ; e) (3 ; b) (4 ; a) — » + `bilan.texte`,
  puis `bilan.dit` après le retour de la dernière paire. Ensuite, comme une question ordinaire : rejeu de la
  simulation (`apres_reponse`), démonstration s'il y en a une, suite.
- **Suivi des acquis** : une réponse par question (`correct` : aucune paire donnée ; `tentative` 1 sans erreur, 2 avec
  erreurs ; la réponse liste les couples et les erreurs par élément).
- **État gardé** : `localStorage` `reponse:<deck>:<diapo>:<cle>:association` (paires posées, erreurs, paires données).
- **Voix** : `scripts/voix/pistes_cours.py` énumère les `dit` (`<diapo>__<cle>_assoc_<g>-<d>`, « * » écrit « autre »,
  et `…_assoc_bilan`) et pose leur piste dans `audio` ; `scripts/logique/association_voix.py <deck> <diapos…>` met à jour
  `<deck>_voix.json` sans toucher aux autres pistes.
- Les QCM, vrai/faux, réponses libres et les exercices du tableau du tuteur (`ExerciceDuTableau`, `paires`) ne changent pas.

## Les associations du national et les cours

Recherche dans les 23 cours (en ligne et en attente) : questions, exercices, rappels, exercices de bloc ; mots
« Reliez », « Associez », « Recopiez les couples », « appari », « va avec », « correspond », « couple (n ; x) » ; puis
toutes les questions `type: association` des sujets (`backend/data/exams/*/*/exam.json`) comparées aux cours.

| Cours | National | Avant | Après |
|---|---|---|---|
| `svt_ch1_reactions_responsables_liberation_energie` | 2020 R, question III (phénomène ↔ réaction bilan, 4 + 5, d de trop) | 3 QCM : `le_x1d_reactions` (« la réaction b correspond à quel phénomène ? »), `le_x1e_reactions_c`, `le_x1f_reactions_krebs` | **1 association** sur `le_x1d_reactions` (4 paires, la réaction d de trop comme au sujet), 20 retours de paire + bilan ; `le_x1e…` et `le_x1f…` retirées (compétences C3, C5 → `le_x1d_reactions`, bloc `le_s6_b1b`). Script : `scripts/logique/svt_ch1_association_2020r.py` |
| `svt_ch3_notion_information_genetique` | 2024 N, question IV (ADN polymérase, centromère, nucléosome ↔ propositions) | 2 QCM : `ig_x1e_associer` (« l'ADN polymérase va avec quelle proposition ? »), `ig_x1f_associer_couples` (« les couples de 2 et 3 ») | **1 association** sur `ig_x1e_associer` (3 paires, propositions a, d, e : le cadre du chapitre, comme la simulation `documents.html?vue=associer` ; le ribosome (4, b) et c relèvent du chapitre 4), 9 retours + bilan ; `ig_x1f…` retirée (compétence C2 → `ig_x1e_associer`, bloc). Script : `scripts/logique/svt_ch3_association_2024n.py` |

Vérifiées, laissées telles quelles :

- `svt_ch2_role_muscle_strie_squelettique` / `ms_x4_restitution` « La chaleur retardée est liée à… » : un QCM de
  restitution (trois propositions qui ne sont pas celles du sujet 2021 N), pas la reproduction d'une association ;
  déjà mis en voix.
- Les associations des sujets que les cours ne reprennent pas : 2018 N (myogrammes ↔ stimulations), 2021 N (chaleurs,
  gradient H⁺, CO₂ ↔ réactions), 2022 N (O₂, Ca²⁺, NADH,H⁺, ATP ↔ actions), 2024 R (troponine, hydrolyse ↔ effets) ;
  et celles hors des quatre chapitres SVT (géologie, pollution, déchets : 2016 N, 2017 R, 2019 R, 2020 N, 2022 R,
  2023 N, 2025 N). À poser en association si un cours les reprend un jour.
- Physique-chimie et mathématiques : aucune association au sujet ni dans les cours ; les « quelle courbe correspond
  à… » sont des choix uniques au national aussi.
- 2023 R, question II : marquée `association` dans `exam.json`, c'est en fait un QCM (une suggestion par proposition).

## Voix à générer

| Cours | Pistes nouvelles | Textes changés (jamais mis en voix) |
|---|---|---|
| svt ch1 | 21 : `le_x1d_reactions__q_assoc_<1-4>-<a-e>`, `…_assoc_bilan` | `le_x1d_reactions` (diapositive), `enonce_le_x1d_reactions_q` |
| svt ch3 | 10 : `ig_x1e_associer__q_assoc_<1-3>-<a,d,e>`, `…_assoc_bilan` | `ig_x1e_associer` (diapositive), `enonce_ig_x1e_associer_q` |

Les pistes des anciens QCM (réactions, démonstrations, énoncés de `le_x1d/e/f`, `ig_x1e/f`) sont retirées des
`_voix.json` : aucune n'avait encore de voix. Mots darija vérifiés sur le corpus (`frequences_corpus_v4.json`) :
« ربط » et « كتعطيهم » (jamais entendus) remplacés par « مع أشمن … كيمشي » et « كيجيو من ».
