# Consigne commune — dessins du cahier (14 novembre 2026)

Projet Moalim : tuteur de 2e bac marocain (PC BIOF). Les cours sont des JSON joués au tableau à la craie. Chaque bloc de
3–4 diapos se termine par l'étape « cahier » : l'élève recopie l'essentiel (mémoire à long terme). Aujourd'hui le cahier
n'est que du texte. Tu ajoutes, **là où la notion se dessine**, une courbe, un schéma ou un croquis simple et légendé.

## À lire d'abord
- `docs/audit-cahier/FORMAT.md` — le format `cahier_figures` (obligatoire, rien d'autre n'est rendu).
- `frontend/src/components/course/FigureCahier.tsx` — le rendu (SVG 400 px de large ; repère avec marges ; textes ~15 px).
- Le skill `.agents/skills/cours-concentration/SKILL.md` (une idée à la fois, formules en notation, tout tient dans l'écran).

## Ce que tu fais, pour chacun de tes fichiers
1. **Audit** : pour chaque bloc (`seances[].blocs[]`, son `cahier` et ses `slide_ids`) et chaque diapo
   (`concentration.cahier`, avec `title`, `screen_content`, `speech_text` pour comprendre ce qui est enseigné) : la notion
   gagne-t-elle à être dessinée dans le cahier ? Laquelle, pourquoi (aide à comprendre / à retenir / tombe à l'examen).
   Pas un dessin partout : en général **un dessin par bloc au plus**, souvent moins ; aucun dessin pour une définition
   purement verbale, une carte du chapitre, un bilan. Seulement des notions **déjà enseignées** à ce point du cours.
2. **Dessins** pour les cas retenus : simples (3 à 8 éléments), légendés (un `titre` court + une `legende` d'une phrase
   qui dit ce qu'il faut voir), justes scientifiquement : axes nommés **avec leur unité**, valeurs et notations du cours
   (celles du `cahier` et du `screen_content`), allure correcte (asymptotes, points remarquables, sens des flèches).
   Lisible : pas de textes qui se chevauchent (un texte prend ~8 px par caractère sur 400 px de large ; garde les
   étiquettes courtes, place-les avec `pos`), pas plus de ~6 étiquettes.
   - Le dessin va sur la diapo qui enseigne la notion : `concentration.cahier_figures: [fig]` (1 figure, 2 au plus).
   - Le bloc qui contient cette diapo reçoit la même figure : `blocs[].cahier_figures: [...]` (dans l'ordre de
     `slide_ids`, **2 au plus par bloc** — l'étape doit tenir dans un écran).
3. **Vérifie** : `python backend/scripts/verifier_figures_cahier.py backend/data/courses/<fichier>.json` → 0 erreur ;
   traite les avertissements (unité manquante : mets `"unite": ""` seulement si la grandeur est sans dimension).
   Calcule tes points à la main (ou en Python) : une courbe expr doit passer par les valeurs du cours.
4. **Écris l'audit** dans le fichier `docs/audit-cahier/<groupe>.md` qu'on t'indique : par cours, un tableau compact
   (bloc / diapo → dessin retenu ou non → pourquoi), puis la liste des dessins faits.

## Contraintes d'écriture (dépôt partagé — d'autres sessions modifient les mêmes cours EN CE MOMENT)
- Dans les cours, ne touche **que** `concentration.cahier_figures` et `blocs[].cahier_figures`. Jamais `speech_text`,
  ni `cahier`, ni `audio`, `visual`, `screen_content`, `pointage`, rien d'autre.
- Prépare d'abord tes figures dans un fichier à toi (par ex. un script Python dans ton répertoire temporaire avec un
  dict `{slide_id: [fig], bloc_id: [fig]}`), puis applique-les par un script qui, **en un seul passage** : relit le
  fichier juste avant d'écrire, pose les champs, réécrit avec `json.dumps(d, ensure_ascii=False, indent=2)`, en gardant
  les fins de ligne du fichier (CRLF si le fichier en avait) et sa fin de fichier (saut de ligne final ou non).
  Relance le script tel quel si tu corriges une figure (il remplace les champs, il n'empile pas).
- Ne commite pas, ne pousse pas, ne déploie pas. Ne modifie aucun fichier du frontend ni du backend (si le format ne
  suffit pas pour un dessin important, dis-le dans ton rapport au lieu de changer le rendu).

## Ton rapport final (court, en français)
Par cours : nombre de dessins (diapo) et de blocs illustrés, la liste « diapo → titre du dessin », ce dont tu doutes
scientifiquement, ce que le format n'a pas permis, et 2 liens de vérification
`http://localhost:5173/cours-ondes.html?cours=<deck id>&diapo=<slide id>` vers tes dessins les plus représentatifs.
