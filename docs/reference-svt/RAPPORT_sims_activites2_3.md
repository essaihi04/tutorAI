# Rapport — simulations des activités 2 et 3, carte du voyage, fiche bilan

Cours de référence SVT « Consommation de la matière organique et flux d'énergie » (contrat :
`docs/reference-svt/ARCHITECTURE.md` § 3). Dossier : `frontend/public/media/simulations/svt/reference_consommation_mo-tableau/`.
Fichiers de cette session : `reference2.js`, `glycolyse-phases.html`, `centrifugation.html`, `exao-mitochondries.html`,
`zoom.html`, `composition.html`, `voyage.html`, `bilan.html`. Rien d'autre n'a été touché (`demarche.js` est chargé, pas modifié).

## Ce qui vaut pour toutes les pages (socle `reference2.js`, `Ref2.page`)

- **Un moment = la fin de son segment.** `play_until {moment}` joue ce que la voix dit pendant le segment et se fige dessus.
  Figée sur un moment, la page ne montre RIEN du segment suivant (arrêts pour l'observation).
- **`?depart=<moment>`** ouvre la page figée sur ce moment (tout ce qui précède est dessiné, rien après).
- **Page pilotée** (pas de lancement automatique, `reset` = retour figé au départ) dès qu'elle est dans une iframe, ou que
  l'URL porte `?depart=` ou `?demarche=`. Il n'est donc pas nécessaire d'écrire `&depart=0`. Ouverte seule dans un onglet,
  sans paramètre, elle se joue toute seule (bouton Lancer → Pause → Reprendre → Rejouer).
- **Commandes** : `start`, `reset`, `pause`, `resume`, `set_time {time_s | moment}`, `play_until {moment | time_s, duree_s}`,
  `set_parameters`, `highlight {target}`, `allume {cible}`, `eteins`.
- **Paramètres communs** : `vitesse` (0,5 à 2), `legendes` (true / false : les noms écrits sur la figure).
- **État** : `ce_qui_se_voit` (à jour à chaque étape), `etape` (le moment en cours), `moments`, `parameters`, `allumes`.
- **Mode large** : le cadre va de 760 à 1596 de large, les positions s'étirent ; **téléphone en paysage** (toile de moins de
  640 × 290) : une caméra montre seulement la fenêtre de l'étape en cours, texte de 15 px au moins, et glisse d'une étape à
  la suivante.
- **Fil de la démarche** : `?demarche=1..6` (repère `demarche`), posé dans le coin haut droit, laissé libre.

## `glycolyse-phases.html` — les trois phases de la glycolyse

| Moment | t (s) | Ce qui se voit |
|---|---|---|
| `glucose_entre` | 3 | bande ① Activation ; le glucose (6 billes jaunes) dans le hyaloplasme |
| `atp1` | 7 | un 1er ATP payé (devient ADP, n° 1 allumé), un P s'accroche : glucose phosphate |
| `atp2` | 11 | un 2e ATP payé (n° 2), un 2e P |
| `fructose_dp` | 13,4 | « fructose diphosphate », « 2 ATP payés » |
| `scission` | 17,9 | bande ② Scission ; la chaîne de 6 coupée en deux chaînes de 3 (C3–P) |
| `taxi1` | 21,5 | à gauche, NAD+ prend 2 H : NADH,H+ |
| `taxi2` | 25,1 | à droite, idem |
| `pi` | 28,9 | un Pi entre sur chaque branche : P–C3–P |
| `atp_branche1` | 33,3 | bande ③ ; à gauche 2 ADP → 2 ATP (n° 1 et 2 allumés) |
| `atp_branche2` | 37,7 | à droite 2 ATP (n° 3 et 4) |
| `pyruvates` | 41,1 | « acide pyruvique », « CH₃–CO–COOH » sous chaque chaîne de 3 (comptées 1, 2) |
| `compte_atp` | 46,1 | « ATP reçus : 4 », « ATP payés : 2 », encadré « gain : 4 − 2 = 2 ATP » ; pièces rallumées une à une |
| `bilan` | 51,1 | l'équation globale |

Repères : `glucose`, `atp_payes`, `atp_paye_1`, `atp_paye_2`, `fructose_dp`, `c3_gauche`, `c3_droite`, `taxis`, `taxi_gauche`,
`taxi_droite`, `pi`, `atp_gagnes`, `atp_gagne_1`…`4`, `pyruvates`, `pyruvate_gauche`, `pyruvate_droite`, `compte`, `bilan`,
`phase1`, `phase2`, `phase3`, `hyaloplasme`. Paramètres : ceux du socle.
Diapos : `?demarche=5`, `?depart=fructose_dp&demarche=5`, `?depart=pi&demarche=5`, `?depart=pyruvates&demarche=6`.

## `centrifugation.html`

**`?vue=principe`** (défaut) — `manege` (5 s : l'essoreuse à salade tourne, l'eau chassée vers le bord) → `tube` (10 : un tube
tourne très vite, grains lourds et légers) → `culot` (14,6 : « culot », « surnageant », encadré « le plus lourd va au fond »).
Repères : `essoreuse`, `bord`, `tube`, `culot`, `surnageant`, `conclusion`.

**`?vue=etapes`**

| Moment | t (s) | Ce qui se voit |
|---|---|---|
| `foie` | 4 | fragments de foie dans la solution de saccharose |
| `broyage` | 9,5 | le piston broie ; loupe : cellules éclatées, noyaux (violets) et mitochondries libérés |
| `centri1` | 14,5 | la centrifugeuse tourne, faible vitesse, compteur à 1 000 tr/min (figée en pleine rotation) |
| `culot_noyaux` | 19,5 | les noyaux se déposent grain par grain : « culot riche en noyaux ». **Arrêt pour l'observation** : rien n'est écrit sur le liquide ni sur les mitochondries |
| `surnageant` | 25 | le surnageant est versé dans un nouveau tube ; le mot s'écrit à la fin |
| `centri2` | 30 | grande vitesse, compteur à 12 000 tr/min |
| `culot_mitochondries` | 35 | « culot riche en mitochondries » |
| `bilan` | 39 | les deux culots allumés et comptés 1, 2 ; encadré « du plus lourd (noyaux) au plus léger (mitochondries) » |

Repères : `foie`, `broyeur`, `loupe`, `cle`, `centrifugeuse`, `compteur`, `vitesse`, `culot_noyaux`, `surnageant`,
`culot_mitochondries`, `conclusion`. Paramètres : ceux du socle.

## `exao-mitochondries.html`

| Moment | t (s) | Ce qui se voit |
|---|---|---|
| `axes` | 4,5 | l'écran s'allume : O₂ en µmol/L (65 à 315), temps de 0 à 5 min |
| `t0` | 8,5 | palier à 275 µmol/L jusqu'à 0,6 min, « 275 » écrit |
| `glucose_injecte` | 12,1 | seringue de glucose poussée, flèche « glucose » à 0,6 min. **Arrêt pour l'observation** : la courbe s'arrête à 0,6 min |
| `rien` | 16,1 | le palier continue jusqu'à 1,3 min |
| `pyruvate_injecte` | 19,7 | 2e seringue, flèche « acide pyruvique » à 1,3 min, courbe arrêtée là |
| `o2_baisse` | 28,7 | 265 à 2 min, 250 à 3 min, 232 à 4 min, 215 à 5 min ; les mitochondries avalent les O₂ un à un ; « 215 » écrit |
| `decrire` | 34,2 | deux phrases : avant t₂, après t₂ |
| `deduire` | 38,2 | encadré vert : « La mitochondrie utilise l'acide pyruvique, pas le glucose. » |

Repères : `seringue` (celle en cours), `seringue_glucose`, `seringue_pyruvate`, `sonde_o2`, `oxymetre`, `interface`,
`thermometre`, `agitateur`, `mitochondries`, `montage`, `ordinateur`, `axe_o2`, `axe_temps`, `courbe`, `palier`, `t1`, `t2`,
`valeur_finale`, `description`, `conclusion`. Paramètre de la page : `conclusions` (true / false, aussi
`?conclusions=false` : `decrire` et `deduire` n'écrivent rien). L'état porte `valeurs: { t_min, o2_umol_L }`.
Diapos : `?demarche=4`, `?depart=rien&demarche=5`.

## `zoom.html`

`cellule` (4 s : cellule × 8 000) → `cadre` (6,5 : cadre rouge sur une mitochondrie) → `mitochondrie` (12 : zoom continu
jusqu'à × 45 000) → `taille` (16,5 : cote, « diamètre : 0,5 à 1 µm », « 1 µm = un millième de millimètre ») → `cadre2`
(19 : cadre rouge sur une crête) → `spheres` (25 : membrane interne en bicouche, sphères pédonculées côté matrice).
Repères : `cellule`, `mitochondrie`, `cretes`, `spheres`, `cadre`, `cadre2`, `taille`, `cote`, `champ`, `grossissement`,
`echelle`, `membrane_interne`, `legende_l1a`…`l3c`. `legendes: false` donne un schéma muet.

## `composition.html`

`externe` (5,5 s : 40 % lipides, 60 % protéines) → `comme_cellule` (9,5) → `interne` (15 : 20 % / 80 %) → `enzymes_interne`
(23 : trois familles allumées et numérotées) → `atp_synthase` (26,5 : la sphère pédonculée s'allume) → `matrice` (34 : acide
pyruvique, TH₂, ATP, ADP, Pi ; glucose barré « pas de glucose ») → `enzymes_matrice` (44 : dé·carboxyl·ase puis
dé·hydrogén·ase) → `hypothese` (49,5 : au conditionnel).
Repères : `membrane_externe`, `membrane_interne`, `matrice`, `sphere`, `decarboxylase`, `deshydrogenase`, `barres_externe`,
`barres_interne`, `glucose_barre`, `hypothese`, `hyaloplasme`, `espace`, `famille_1`…`3`, `nom_famille_1`…`3`, `nom_sphere`,
`titre_externe`, `titre_interne`, `comme_cellule`, `acide_pyruvique`, `th2`, `atp_adp_pi`.
Diapos : `?demarche=5`, `?depart=atp_synthase&demarche=6`.

## `voyage.html?etape=1..4` — la carte du voyage (cumulative)

L'étape n s'ouvre figée sur la fin de l'étape n − 1 (mêmes dessins, déjà au tableau) et joue ses propres moments ;
`?depart=` l'emporte. Bouton « Imprimer / PDF ».

| Étape | Moments (t en s) |
|---|---|
| 1 | `dehors` 2,4 · `entree` 5 · `glycolyse` 8 · `pyruvate` 11 · `route_o2` 13,8 · `krebs_co2` 17 · `route_sans_o2` 19,8 · `ethanol_co2` 23 |
| 2 | `atp` 26 · `nadh` 29 · `hyaloplasme` 32 |
| 3 | `membranes` 35,4 · `matrice` 38,4 · `enzymes` 41,8 |
| 4 | `tout` 47,8 (les nœuds s'allument un à un) · `a_suivre` 51,3 (« à suivre… » dans la matrice) |

Repères (un par nœud) : `dehors`, `dedans`, `membrane`, `glucose_dehors`, `glucose`, `glycolyse`, `pyruvates`, `carrefour`,
`route_o2`, `mitochondrie`, `krebs`, `route_sans_o2`, `ethanol`, `atp`, `nadh`, `hyaloplasme`, `membranes`, `matrice`,
`enzymes`, `a_suivre`. Paramètre de la page : `etape` (1 à 4 : la page se recharge sur cette étape).

## `bilan.html` — « Ce qu'il faut retenir »

Reprise de la fiche du dossier voisin. Neuf blocs, moments = repères : `respiration`, `fermentation`, `localisation`,
`devenir`, `glycolyse`, `centrifugation`, `pyruvate`, `ultrastructure`, `composition` ; puis `fiche` (tout) et `lacunes` (la
page de l'élève). Commandes : `play_until {moment}`, `set_parameters {lacunes, acquis, acquis_ids}` (compétences C1 à C8),
`next`, `previous`, `start`, `reset`. Bouton « Imprimer / PDF ». Sur un tableau moyen (760 × 420) les trois blocs de la
partie en cours sont seuls affichés ; au téléphone, le bloc en cours seul ; à partir de 1000 px de large, les neuf.

## Ce qui a été vérifié

- Captures Playwright de chaque moment de chaque page et vue (et du milieu de chaque segment) à 760 × 420, 1366 × 560 et
  429 × 250, regardées : rien ne déborde ni ne se chevauche ; console sans erreur ni texte hors cadre.
- Pilotage dans une iframe, comme le lecteur (`simulation_control`) : ouverture figée (`?depart=`), `play_until` arrivé sur
  l'instant exact du moment, `highlight` (anneau posé), `set_parameters`, sur les dix cas (toutes les pages et vues).
- `python -I scripts/verifier_formules.py` sur le dossier : 0 relation à reprendre.
- Non fait : `frontend/scripts/verifier-pointage-navigateur.mjs` (il rejoue le `pointage` des diapos ; le fichier du cours ne
  référençait pas encore ces pages au moment du contrôle).

## Points imparfaits

- **Centrifugation** : le document ne donne pas de vitesse ; l'afficheur montre 1 000 puis 12 000 tr/min comme ordres de
  grandeur. À ne pas faire dire à la voix comme des données. Le tube conique et le broyeur sont peints dans la page (le
  lexique n'a qu'un tube à essais droit).
- **Zoom** : le document ne donne pas de grossissement pour les sphères pédonculées ; la plaque écrit « encore plus près »,
  la barre d'échelle indique 10 nm.
- **Composition** : le transporteur TH₂ est dessiné avec le taxi du lexique (marqué « NADH,H+ »), légendé « TH₂ » dessous.
- **Glycolyse** : les intermédiaires sont notés C3–P et P–C3–P sur la figure (leurs noms complets, glycéraldéhyde phosphate
  et acide glycérique diphosphate, ne tiennent pas à 15 px) ; le repère `pyruvates` entoure les deux chaînes jusqu'au compte,
  puis seulement celle de gauche (le compte s'écrit entre les deux).
- **Mode large** : les positions s'étirent, les objets gardent leur taille ; il reste de l'espace entre les postes.
- **Téléphone** : la fenêtre de la caméra coupe parfois un objet voisin, jamais le texte de l'étape ; le fil de la démarche
  recouvre le coin haut droit de la fenêtre.
- **Fiche bilan** : sur un tableau moyen, les neuf blocs ne sont jamais tous visibles ensemble (trois à la fois).
