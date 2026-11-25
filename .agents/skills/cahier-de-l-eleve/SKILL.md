---
name: cahier-de-l-eleve
description: Ce que l'élève écrit dans son cahier, cours par cours — le texte, les schémas et les graphiques de l'étape « 📓 À écrire dans le cahier » (fin de bloc et bulle de diapositive) : quoi écrire, combien, dans quel ordre, avec quels compléments et quels dessins, pour que le cahier se lise du début à la fin comme celui d'un bon professeur et serve à réviser le bac. À charger pour créer, revoir ou corriger le cahier d'un cours, ses figures, sa numérotation ou son enchaînement.
---

# Le cahier de l'élève

Demande de l'utilisateur (18 novembre 2026) : « un agent spécialisé pour le texte et les schémas à écrire dans le
cahier : taille, informations, compléments, graphiques…, tout d'une manière intelligente ; corriger l'enchaînement et
tout ce qui sera nécessaire aux élèves ». Le cahier est ce qui reste quand le cours est fini : l'élève le recopie
(mémoire longue), le relit avant un contrôle et le revoit avant le national. Il doit donc se suffire à lui-même.

Données : `seances[].blocs[].cahier` (liste de `{texte}`) et `blocs[].cahier_figures` (étape de fin de bloc),
`activities[].slides[].concentration.cahier` et `concentration.cahier_figures` (bulle de la diapositive). Format des
figures : `docs/audit-cahier/FORMAT.md`, rendu `frontend/src/components/course/FigureCahier.tsx`, vérificateur
`backend/scripts/verifier_figures_cahier.py`. Le cahier est écrit à l'écran, **pas lu par la voix** : le modifier ne
coûte aucune voix (il peut donc être corrigé dans le cours en ligne comme dans sa copie en attente).

## 1. Le cahier entier se lit comme celui d'un professeur

- **Un plan numéroté continu**, celui du cours : `I. …`, `1. …`, `a) …` ; chaque bloc reprend la numérotation là où
  le bloc précédent l'a laissée. En lisant tous les blocs à la suite, on obtient le cours complet, dans l'ordre, sans
  trou et sans doublon.
- **Rien n'est utilisé avant d'être écrit** : une notion, un symbole, une formule cités dans un bloc ont été écrits
  dans un bloc d'avant (ou dans un rappel du même bloc, marqué « Rappel : »).
- **L'enchaînement se voit** : la première ligne d'un bloc dit d'où l'on vient quand c'est utile (« On a vu que… ;
  on cherche maintenant… ») ; une conclusion d'expérience dit ce qu'elle prouve (« Donc… »).
- La « fiche bilan » et la carte du chapitre reprennent les mêmes mots et la même numérotation que le cahier.

## 2. Quoi écrire (et ne pas écrire)

À écrire, en **français** (la langue du bac), comme au tableau :
- **le titre** de la partie ;
- **les définitions à savoir par cœur**, mot pour mot comme le cours les a construites, encadrées par « Définition : » ;
- **les lois et formules** en notation (« v = d/Δt »), **avec leurs conditions et leurs unités** (« θ = λ/a,
  θ en rad, valable pour θ petit ») ; les équations de chimie avec l'état physique de chaque espèce ;
- **la conclusion de chaque expérience** en une phrase (« Donc la glycolyse se fait dans le hyaloplasme. ») ;
- **une méthode** pour chaque cas type fréquent au national (exploration, `cas_types`) : les étapes numérotées, comme
  le barème les lit (« Méthode : 1) … 2) … 3) … ») ;
- **les compléments utiles à l'examen**, chacun en une ligne : « Attention : » (l'erreur fréquente des élèves et des
  copies du national), « Remarque : » (une condition, un cas limite), « Exemple : » (une application numérique courte
  avec son unité), les phrases types que le bac attend (« le régime permanent est atteint au bout de 5τ »).

À ne pas écrire : la darija, les phrases de la voix (« شوف », « دابا »…), les questions de la diapositive, ce qui
est seulement une image pour comprendre (l'analogie du taxi peut rester en un mot entre parenthèses si elle aide à
retenir), une chose hors du cadre, une notion pas encore enseignée.

## 2 bis. Le cours en général, jamais les données d'un exercice (24 novembre 2026)

Demande de l'utilisateur : « donner seulement les cas en général, pas les données des exercices : quand il révise,
l'élève n'a pas les énoncés ». Le cahier se relit SANS le cours ni les documents :
- **jamais** les nombres, les noms ou les résultats d'un document ou d'un exercice : pas de « S1 : P = 80/8 = 10 ml/min »,
  pas de « Maâmora : I : 2 espèces », pas de « Nereis : F ≈ 83 % », pas de « zone A (0 à 50 cm) : échec », pas de
  « azote ×5 », pas de « R1 (20 ; 40 ; 40) : limon ». Une ligne qui n'a de sens qu'avec l'énoncé sous les yeux est fausse ;
- **à la place, la règle générale** que le document a montrée, écrite pour tous les cas : « un sol sableux est très
  perméable et retient peu d'eau ; un sol argileux, l'inverse », « les déjections des lombrics sont plus riches en
  éléments minéraux que le sol », « trop peu de sable : asphyxie des racines ; trop de sable : manque d'eau » ;
- **les valeurs de référence du cours restent** (elles servent à tous les exercices) : les seuils des indices de
  fréquence, l'échelle de Braun-Blanquet, les classes de taille de la faune, les zones de pH… de préférence en tableau ;
- un **exemple** n'est permis que s'il est inventé, court et complet en une ligne, sans renvoyer à un document
  (« Exemple : 6 relevés sur 10 → F = 60 % → indice IV ») ;
- le nom d'un lieu ou d'une espèce étudiés en classe reste seulement s'il est une connaissance du programme (le
  chêne-liège calcifuge), pas une donnée d'exercice.

## 3. Combien (la taille)

- **Un bloc : 3 à 6 lignes de texte et 0 à 2 figures**, qui tiennent dans UN écran, téléphone en paysage compris
  (~724 × 350 px CSS), sans défilement. Plus long → couper en deux blocs ou garder l'essentiel.
- **Une ligne : une idée**, phrase courte (≤ ~90 caractères), pas de paragraphe.
- **Une bulle de diapositive** (`concentration.cahier`) : 1 ou 2 lignes, la trace de CETTE diapositive ; le bloc
  rassemble les traces de ses diapositives sans les répéter mot pour mot si une ligne de synthèse suffit.
- **Un chapitre entier** : de l'ordre de 2 à 4 pages de cahier ; au-delà, l'élève recopie sans retenir.

## 4. Les dessins (schémas, graphiques, croquis)

- Quand la notion se dessine (courbe, schéma d'expérience, montage, structure, tableau de variations…), le bloc a sa
  figure ; **un dessin par bloc au plus en général, deux au maximum** ; aucun pour une définition verbale, une carte
  ou un bilan (skill professeur, règle 31 ; mémoire « cahier avec dessins »).
- **Le même dessin que dans tout le site** : chaque objet a la forme du lexique visuel commun
  (`docs/lexique-visuel/`, skill simulations-au-tableau règle 15) — le glucose est la chaîne de 6 billes jaunes, la
  mitochondrie a la même coupe légendée, un condensateur a son symbole normalisé.
- Juste et lisible : axes nommés **avec leur unité**, valeurs du cours, allure correcte (asymptotes, points
  remarquables, sens des flèches) ; un `titre` court et une `legende` d'une phrase qui dit quoi voir ; 6 étiquettes au
  plus, courtes, qui ne se chevauchent pas.
- Un schéma que le bac fait légender (mitochondrie, chaîne respiratoire, sarcomère, ADN…) est dessiné comme au bac,
  avec ses légendes.

## 5. La méthode de travail

1. **Lire** le cours en entier (titres, `screen_content`, `speech_text` pour comprendre ce qui est enseigné, questions,
   exercices), son architecture `backend/data/curriculum/architecture/<deck>.md` s'il y en a une, l'exploration
   (`cas_types`, `erreurs_examen`, `commentaires_eleves`), l'audit existant `docs/audit-cahier/<groupe>.md`.
2. **Écrire d'abord le cahier idéal du chapitre en entier**, d'un seul tenant (plan numéroté, définitions, formules,
   conclusions, méthodes, compléments, dessins prévus), dans `docs/audit-cahier/<deck>_cahier.md`. C'est ce texte qu'on
   relit pour juger l'enchaînement, la taille et les manques.
3. **Le découper** en blocs (`blocs[].cahier`, `blocs[].cahier_figures`) et en bulles de diapositive
   (`concentration.cahier`, `cahier_figures`), dans l'ordre des `slide_ids`.
4. **Vérifier** : `python backend/scripts/verifier_figures_cahier.py <cours>` → 0 erreur ; chaque bloc tient dans un
   écran ; rien n'est utilisé avant d'être écrit ; la numérotation est continue ; les formules sont en notation avec
   leurs conditions et unités ; aucune darija.
5. **Écrire sans écraser le travail des autres** (d'autres sessions modifient les mêmes cours) : ne toucher que
   `blocs[].cahier`, `blocs[].cahier_figures`, `concentration.cahier`, `concentration.cahier_figures` ; relire le
   fichier juste avant d'écrire, poser les champs en un seul passage, garder la mise en forme du fichier
   (`json.dumps(d, ensure_ascii=False, indent=2)`, mêmes fins de ligne, même fin de fichier) ; appliquer au cours en
   ligne ET à sa copie en attente (`backend/data/courses/en_attente/<deck>.json`) quand elle existe, en suivant les
   `slide_ids` et les blocs de chacun (la copie en attente peut avoir un autre découpage).

## 6. Mise en page et charte de couleurs (24 novembre 2026)

Demande de l'utilisateur : « le cahier doit être plus organisé : les définitions de côté, les explications bien
écrites, pas de texte non rassemblé, pas de texte écrit partout ; des tableaux, des graphes ; le titre au milieu, le
début de paragraphe à gauche… ; penser à la charte de couleurs ». Le lecteur (`memoire/LignesCahier.tsx`, bloc ET bulle de
diapositive) met en forme chaque ligne d'après son début ; écrire donc chaque ligne avec le bon début :

| Début de ligne | Rendu | Couleur (craie sur tableau vert) |
|---|---|---|
| `I. Titre` (romain) | titre de partie, **au milieu**, souligné | jaune craie `#fde68a` |
| `1. Sous-titre` (seul sur sa ligne, sans « : ») | à gauche, souligné | cyan `#67e8f9` |
| `a) Sous-partie` (seule sur sa ligne) | à gauche, en retrait | vert clair `#86efac` |
| `Définition : …` | **encadré à part**, étiquette « Définition » | vert `#34d399` |
| `Formule : …` | encadré, formule au milieu, avec unités | ambre `#fbbf24` |
| `Méthode : 1) … 2) … 3) …` | encadré, une étape par ligne | bleu `#60a5fa` |
| `Attention : …` | l'erreur à éviter | rose `#fda4af` |
| `Remarque : …` / `Exemple : …` | en retrait, plus petit (exemple en italique) | gris clair `#d4d4d8` |
| `Donc …` / `Conclusion : …` / `Bilan : …` | ⇒ en gras | orange `#fdba74` |
| `\| a \| b \|` (lignes qui se suivent) | **un tableau** ; la 1ʳᵉ ligne est l'en-tête | en-tête jaune |
| le reste | un paragraphe qui commence à gauche | blanc craie `#f5f1dc` |

Cette charte est la 3ᵉ surface de la charte de couleurs des cours (skill `simulations-au-tableau`, règle 19 : objets aux
couleurs du lexique, craie selon `docs/lexique-visuel/craie.md`, cahier selon ce tableau).

Règles d'organisation :
- **un titre seul sur sa ligne** (« 2. La texture du sol »), puis le contenu ; jamais « 1. Outils : carte, boussole… »
  (titre et contenu collés) ;
- **une définition par encadré**, mot pour mot, le terme défini en tête (« Définition : la texture est… ») ;
- **dès qu'il y a une liste de cas qui se comparent** (formes de l'eau, structures, indices, classes de taille, pH, clé
  de détermination), un **tableau** plutôt qu'une phrase pleine de « ; » ; 2 à 4 colonnes, 6 lignes au plus ;
- **dès que la notion se dessine** (courbe, histogramme, triangle, schéma), une figure (`cahier_figures`, § 4) ;
- les formules dans « Formule : » avec le sens de chaque lettre et l'unité ;
- jamais deux idées collées par « ; » quand elles se lisent mieux en deux lignes ; jamais de ligne de plus de ~90
  caractères hors tableau.

## 7. Le niveau de la classe (24 novembre 2026)

Le cahier est celui d'UNE classe : son vocabulaire, son programme, son examen. Le Tronc Commun n'est pas le 2ᵉ Bac :
- **Tronc Commun** (contrôles continus, examen local) : phrases simples, vocabulaire du programme de TC, pas de notion
  de 1ʳᵉ ou de 2ᵉ Bac, calculs simples (%, rapports, moyennes) ; les méthodes visent les questions du contrôle
  (décrire → déduire → expliquer, calculer, construire un histogramme, lire le triangle des textures) ;
- **1ʳᵉ Bac** : examen régional ; **2ᵉ Bac** : national, ses formules, ses phrases types et son barème (§ 2) ;
- lire le niveau dans le cours (`niveau`) et ne jamais utiliser une notion qu'une classe n'a pas encore vue.

