# Revue des cahiers de 2ᵉ Bac — brief commun (24 novembre 2026)

## La demande de l'utilisateur (Moalim, tuteur IA marocain, 2ᵉ Bac PC BIOF)
« Faire une revue des cahiers de 2ᵉ Bac en appliquant toutes ces améliorations » :
- **seulement le cours en général** : jamais les données d'un exercice ou d'un document. Quand l'élève révise, il n'a
  pas les énoncés ;
- **un cahier organisé** : le titre au milieu, le début de paragraphe à gauche, les définitions à part, des tableaux
  et des graphes, pas de « texte écrit partout » ni de texte non rassemblé ;
- **une charte de couleurs** ;
- **le niveau de la classe** : 2ᵉ Bac (examen national), pas le Tronc Commun.

## À lire d'abord (obligatoire)
`<WT>/.agents/skills/cahier-de-l-eleve/SKILL.md`, en entier, et surtout :
- § 2 : quoi écrire ;
- § 2 bis : le cours en général, jamais les données d'un exercice ;
- § 3 : la taille ;
- § 4 : les dessins ;
- § 6 : mise en page et charte, avec le **tableau des débuts de ligne** ;
- § 7 : le niveau de la classe.

Le rendu se fait dans `<WT>/frontend/src/components/course/memoire/LignesCahier.tsx`. Lis-le pour savoir exactement
quel début de ligne donne quelle forme. Les parties à recopier se découpent selon
`<WT>/frontend/src/components/course/memoire/partiesDuCahier.ts` : une ligne `1. …` ouvre une partie, et un titre
romain `I. …` posé juste avant elle va avec elle.

`<WT>` = le worktree git sur origin/main où se fait la revue (au 25/11/2026 :
`C:\Users\HP\AppData\Local\Temp\claude\9269525a2680ed40\1e9c1767-17b1-498d-845f-3ca11b660834\scratchpad\wt-tc` ; s'il a
disparu, en créer un neuf sur origin/main avec `backend/data/courses/` dans le sparse-checkout). D'autres agents
travaillent sur d'AUTRES cours dans ce même worktree.

## Ce que tu fais, pour chacun de tes cours
1. **Lire** le cours : les titres des diapositives, `screen_content`, `speech_text` (pour comprendre ce qui est
   enseigné), les blocs (`seances[].blocs[]` avec leurs `slide_ids`), le cahier actuel (`blocs[].cahier`, une liste de
   `{"texte": …}`), les bulles (`activities[].slides[].concentration.cahier`, une chaîne) et les dessins
   (`cahier_figures`).
2. **Écrire le cahier idéal du chapitre en entier**, d'un seul tenant, dans ton dossier de travail. Garde le plan
   numéroté continu (I., 1., a)…) d'un bloc à l'autre. Ensuite, découpe-le par bloc, dans l'ordre des `slide_ids`.
3. **Réécrire** :
   - `blocs[].cahier` : 3 à 8 lignes par bloc ; les lignes d'un tableau comptent pour une ;
   - **chaque bulle existante** (`concentration.cahier`) : 1 ou 2 lignes, séparées par `\n`, ou un petit tableau.
     Ne crée pas de bulle là où il n'y en a pas ;
   - les dessins (`cahier_figures`) : seulement pour retirer les données d'un document (titre, légende, étiquettes),
     ou retirer un dessin qui n'est qu'une donnée d'exercice. Ne redessine pas de figure ; si tu en changes une,
     `python -I <WT>/backend/scripts/verifier_figures_cahier.py <cours.json>` doit rester sans erreur.
4. **Les deux copies** : le cours en ligne `backend/data/courses/<deck>.json` ET sa copie en attente
   `backend/data/courses/en_attente/<deck>.json`. La copie en attente peut avoir un autre découpage en blocs et
   d'autres diapositives : suis SES `slide_ids` et SES blocs. Le texte du cahier est le même là où les diapositives
   sont les mêmes.
   Pour les révisions de /2bacpcf, il n'y a qu'une seule copie : `frontend/src/publication/bac2pcf/cours/<deck>.json`.

## Les règles d'écriture (résumé : le skill fait foi)
- **Jamais de données d'exercice ni de document** :
  - pas les valeurs d'un énoncé (« R = 2 kΩ, C = 10 µF → τ = 20 ms » tirés d'un exercice), pas « la courbe du
    document 3 », pas les noms de solutions ou de flacons d'un exercice (S1, S2, flacon A), pas les résultats
    numériques d'une activité ;
  - à la place : la loi, la règle, la méthode générale, la conclusion valable pour tous les cas ;
  - **restent** : les formules et les lois du programme, les constantes et valeurs de référence (c, h, N_A, Ke = 10⁻¹⁴
    à 25 °C, demi-vies classiques si le cours les donne comme connaissance), les phrases types du national et les
    unités ;
  - un exemple est permis s'il est **court, inventé, complet en une ligne**, et marqué `Exemple :`.
- **Un titre seul sur sa ligne** : `I. Titre`, `1. Sous-titre`, `a) Sous-partie`. Jamais « 1. Titre : contenu ».
- **Une définition par ligne** `Définition : le terme est…`.
- **Une formule par ligne** `Formule : …` : la formule d'abord, puis, après ` ; `, le sens des lettres et les unités
  (« Formule : τ = R·C ; τ en s, R en Ω, C en F »). Le lecteur coupe au premier ` ; ` : il ne faut aucun ` ; ` à
  l'intérieur de la formule elle-même, ni dans des parenthèses.
- **Méthode** : `Méthode : 1) … ; 2) … ; 3) …`, comme le barème du national les lit.
- **Tableaux** : dès que des cas se comparent (régimes, types de désintégration, acide ou base, réactions,
  propriétés…), des lignes `| a | b | c |` qui se suivent ; la première est l'en-tête. 2 à 5 colonnes, 6 lignes au
  plus, cellules courtes. Deux tableaux qui se suivent doivent être séparés par une ligne de texte (sinon ils se
  fondent en un seul).
- **Attention :** pour l'erreur fréquente des copies, **Remarque :** pour une condition ou un cas limite,
  **Donc …** pour une conclusion.
- Une ligne : une idée, phrase courte (≤ ~90 caractères hors tableau, formule ou méthode). Pas de « ; » qui colle
  deux idées qui se lisent mieux en deux lignes.
- **Notation** : garde la notation du cours, car le composant `Formule` l'affiche ; regarde comment les lignes
  actuelles écrivent indices, exposants, fractions et symboles, et fais pareil. En français, pas de darija.
- **Niveau 2ᵉ Bac** : le vocabulaire et les phrases types du national, les formules avec leurs conditions de validité ;
  rien hors du programme national, rien d'une notion pas encore vue dans le cours.

## Ne pas toucher (vérifié automatiquement)
Seuls `cahier` et `cahier_figures` (dans `blocs[]` et dans `concentration`) peuvent changer. Ne touche pas aux voix,
aux textes dits, aux id, à l'audio, aux questions, aux titres des blocs ni au reste du fichier. Garde la mise en forme
du fichier telle quelle : même indentation (lis-la dans le fichier), mêmes fins de ligne (CRLF ou LF), même fin de
fichier, `ensure_ascii=False`. Écris avec un script Python (`python -I`), par exemple :

```python
brut = p.read_text(encoding="utf-8"); d = json.loads(brut)
ind = 1 if brut.lstrip("{").lstrip("\r\n")[:2] == ' "' else 2
texte = json.dumps(d, ensure_ascii=False, indent=ind) + ("\n" if brut.endswith("\n") else "")
if "\r\n" in brut: texte = texte.replace("\n", "\r\n")
p.write_text(texte, encoding="utf-8", newline="")
```

Relis le fichier juste avant d'écrire, et écris chaque fichier en un seul passage. Puis lance :
`python -I <WT>\scripts\revue_cahier\verifier_seul_cahier.py <WT> <chemins relatifs de tes fichiers…>`
Il doit afficher `OK` pour chaque fichier. Sinon, corrige.

**Ne fais ni commit, ni push, ni git checkout, reset, stash ou pull.** Ne touche à aucun autre cours que les tiens,
ni au dossier `C:\Users\HP\Desktop\ai-tutor-bac`. Mets tes scripts et brouillons dans ton dossier de travail :
un dossier à toi HORS du dépôt (ton scratchpad), un par groupe.

## Ton rapport (court)
Pour chaque cours :
- nombre de blocs et de bulles réécrits (en ligne et en attente) ;
- le nombre de tableaux posés ;
- 3 à 5 exemples de données d'exercice retirées (avant → après) ;
- les dessins changés ou retirés ;
- le résultat de verifier_seul_cahier.py ;
- tout doute, en particulier une valeur dont tu ne sais pas si c'est une connaissance du cours ou une donnée
  d'exercice.
