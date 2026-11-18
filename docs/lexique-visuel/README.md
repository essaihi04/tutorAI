# Lexique visuel commun du site

Règle de l'utilisateur, 18 novembre 2026 : « une fois qu'un élément du cours est modélisé ou représenté sous une forme,
il doit rester sous la même forme dans tout le cours », puis « généraliser pour tous les cours de toutes les matières ;
dans les prochains cours, le glucose doit garder la même forme et les mêmes couleurs », et « une lexique commune à chaque
élément ; chaque nouveau cours va vers ce lexique ». Skills : `simulations-au-tableau` règle 15, `professeur` règle 43,
`logique-de-cours` règle 10.

- **Une fiche par élément** (ce dossier) : toutes ses formes (billes d'animation, brute, semi-développée, développée,
  cyclique ; vue réaliste et symbole pour un composant), couleurs, étiquette, quand l'utiliser, fonction à appeler.
- **Un module de dessin** : `frontend/public/media/simulations/shared/lexique/lexique.js` → `window.Lexique`.
  À charger avant tout script de dessin : `<script src="/media/simulations/shared/lexique/lexique.js"></script>`.
  Toutes les fonctions prennent le contexte brut (`craie.ctx`, dans `craie.direct`) et les coordonnées du cadre virtuel
  760 × 420, peignent l'objet (règle 32 du professeur : réaliste, ombre et reflet) et renvoient sa géométrie.
- **Un nouveau cours va d'abord au lexique** : il prend les formes qui existent ; un élément ou une forme qui manque est
  ajouté à sa fiche ET au module avant sa première utilisation, jamais dessiné localement.

## Le code des couleurs (une couleur garde son sens partout)

| Couleur | Valeur | Sens (et seulement celui-là) |
|---|---|---|
| jaune | `[250,204,21]` #facc15 | un atome de **carbone** — le glucose est une chaîne droite de 6 billes jaunes, ses produits gardent ses billes (acide pyruvique, acide lactique, éthanol, CO₂) |
| blanc | `[235,240,245]` | un atome d'**hydrogène** |
| rouge | `[235,85,70]` | un atome d'**oxygène** (O₂, H₂O, CO₂, H₃O⁺, HO⁻) |
| rose | `[244,114,182]` | un **proton = ion H⁺** (« H+ » écrit dessus) ; flèches de pompage des H⁺ en craie rose |
| bleu ciel | `[96,200,250]` | un **électron** (« e− ») ; anneau de charge négative |
| gris | `[160,168,180]` | un **neutron** ; `[150,150,150]` l'**ADP** (carte vide) |
| doré | `[250,190,60]` | l'**ATP** (carte d'énergie pleine) |
| orange | `[240,140,60]` | le **phosphate Pi** (et les P de l'ATP développé) |
| cyan | `[34,190,220]` | le transporteur **NAD⁺ / NADH,H⁺** (le « taxi ») |
| vert | `[110,200,90]` | le transporteur **FAD / FADH₂** |
| indigo | `[110,120,230]` | le **coenzyme A** |
| violet | `[160,120,240]` | une **protéine** (transporteur membranaire, enzyme) ; `[150,110,220]` le noyau cellulaire |
| milieux | hyaloplasme `[96,200,150]`, membrane `[250,204,96]`, matrice `[86,180,236]`, mitochondrie `[240,100,62]` | `Lexique.T` |

Texte écrit SUR un objet clair : sombre et gras (`#0b1f2a`, `Lexique.etiquette`) ; légendes à côté : craie.

## Index des éléments

| Élément | Fiche | Fonction |
|---|---|---|
| Glucose | [glucose.md](glucose.md) | `glucose(ctx, x, y, { forme, echelle, alpha, etat, coupe })` |
| Acide pyruvique | [acide-pyruvique.md](acide-pyruvique.md) | `acidePyruvique` |
| Acide lactique | [acide-lactique.md](acide-lactique.md) | `acideLactique` |
| Éthanol | [ethanol.md](ethanol.md) | `ethanol` |
| Molécule organique (RH₂) | [molecule-organique.md](molecule-organique.md) | `moleculeOrganique` |
| CO₂ | [co2.md](co2.md) | `co2` |
| H₂O | [h2o.md](h2o.md) | `h2o` |
| O₂ | [o2.md](o2.md) | `o2` |
| ATP / ADP / Pi | [atp.md](atp.md) | `atp`, `pi` |
| NAD⁺ / NADH,H⁺ | [nad.md](nad.md) | `nad` |
| FAD / FADH₂ | [fad.md](fad.md) | `fad` |
| Coenzyme A | [coa.md](coa.md) | `coa` |
| Électron | [electron.md](electron.md) | `electron` |
| Proton / H⁺ | [proton.md](proton.md) | `proton` |
| Neutron | [neutron.md](neutron.md) | `neutron` |
| H₃O⁺ | [h3o.md](h3o.md) | `h3o` |
| HO⁻ | [ho.md](ho.md) | `ho` |
| Atome (C, H, O, N, P) | ci-dessous | `atome(ctx, x, y, 'C')`, `chaine`, `positionsChaine` |
| Cellule, hyaloplasme, noyau | [cellule.md](cellule.md) | `cellule` |
| Mitochondrie, membrane interne, sphère pédonculée | [mitochondrie.md](mitochondrie.md) | `mitochondrie`, `membrane`, `spherePedonculee` |
| Protéine | [proteine.md](proteine.md) | `proteine` |
| Levure | [levure.md](levure.md) | `levure` |
| Bécher | [becher.md](becher.md) | `becher` |

Primitives : `bille`, `liaison`, `capsule`, `eclat`, `bulleGaz`, `etiquette`, `formule`. Les atomes : C r 12, H r 5,
O r 9 à l'échelle 1 ; pas d'une chaîne 28 px.

## Inventaire du 18 novembre 2026 : les incohérences relevées

Relevé dans les 23 cours (`frontend/public/media/simulations/**/*-tableau/`). ✅ = corrigé dans cette passe.

### SVT ch1 — Réactions responsables de la libération de l'énergie (`svt/reactions_responsables_liberation_energie-tableau/`)

| Objet | Avant | Après |
|---|---|---|
| Glucose | chaîne droite (glycolyse, fermentations) ; **deux rangées de 3** (carrefour, la carte) ; **anneau** (depart) ; **billes blanches** (comparer) ; **ellipse** (atp) ; petits hexagones au trait (depart, le sang) | ✅ chaîne droite de 6 billes jaunes partout (`Lexique.glucose`) |
| Acide pyruvique | 3 billes jaunes ; dans comparer, la seule molécule jaune (glucose blanc) | ✅ 3 billes jaunes coupées dans la chaîne |
| Acide lactique | 3 C + 2 H (fermentations) ; **billes orange** (comparer) ; 3 billes en arc (rendement) | ✅ `acideLactique` |
| « Molécule organique » | **anneau de 6 billes jaunes** (taxi) = l'ancien glucose de depart | ✅ chaîne de 4 carbones |
| CO₂ | carbone **gris** (peinture.js, krebs) ; carbone jaune (comparer) | ✅ carbone jaune partout (`Lexique.co2`) |
| Électron | **jaune** (chaine, la couleur du carbone) ; bleu ciel (taxi) | ✅ bleu ciel |
| H⁺ | rouge [225,62,62] (chaine) / [240,80,80] (exao, vesicules) — le rouge de l'oxygène | ✅ rose, flèches de pompage roses |
| O₂ | une bille bleu pâle « O2 » (chaine) ; O rouge (comparer) | ✅ deux oxygènes rouges |
| H₂O | bille **bleue** (chaine) ; O bleu + 2 H (comparer) | ✅ O rouge + 2 H blancs |
| ATP | carte dorée (glycolyse, chaine, compteur) ; bille dorée (krebs) ; **bille jaune** (vesicules) ; pastille locale (comparer) | ✅ doré partout (`Lexique.atp`, formes carte/bille) |
| Pi | orange (chaine, atp) ; **violet** (vesicules) | ✅ orange |
| FADH₂ | **orange** (taxi, krebs FADC) ; **violet** (krebs picto, compteur, chaine) | ✅ vert |
| CoA | violet (= protéines) | ✅ indigo |
| Peinture de base | `SVTPeinture` locale au dossier, réutilisée par les anciennes pages `svt/ch1_consommation_matiere_organique/` | ✅ vient du lexique ; `peinture.js` n'y garde que les fonds et cartes du cours |

### SVT ch2 — Rôle du muscle strié squelettique (`role_muscle_strie_squelettique-tableau/`)
- ATP : pastille **verte** (`MoleculesPeintes.pastille`), jauge verte (voies), barre **jaune** (consommation, national) — le lexique dit doré.
- Pi et Ca²⁺ : même jaune #facc15 dans atpase.html:63 (jaune = carbone dans le lexique) ; Ca²⁺ jaune dans molecules.js:113.
- Myosine bleue (molecules.js, filaments.js) mais **violette** dans atpase.html:59 ; actine en points orange plats dans atpase.html:58.
- Phosphocréatine orange (voies) / rose (consommation, national) ; acide lactique rose (voies) / orange (consommation, national) ; glycogène vert / cyan.
- Muscle (ventre) en 3 palettes (`peindreMuscle` recopié 4 fois + structure.html + myogramme.js) ; tendon et os en 3 versions ; fibre musculaire en 2 versions.

### SVT ch3 et ch4 — Information génétique, relation gène-protéine
- Bases A/T/C/G **permutées** dans `relation_gene_proteine-tableau/rappels.html:28` (A vert, T rouge, G jaune) contre A rouge, T jaune, C bleu, G vert partout ailleurs.
- Noyau **violet** (`Etapes.Peint.noyau`) ou **bleu** (`Molecules.noyau`, RGP) — les deux dans le même cours.
- Squelette de l'ADN en au moins 6 couleurs (indigo, #6366f1, bleu + gris, #3b82f6, violet, fil violet) ; brin neuf **orange** (replication, = la couleur de l'ARN), blanc (meselson), rouge (thymidine).
- Deux `Etapes.Peint` divergents sous le même nom (NIG/etapes.js et RGP/etapes.js) ; cellule en 3 palettes roses + une orange ; chromosomes VIOLET/BLEU en 3 palettes.
- Hématie en faucille redessinée (drepanocytose.html:79) ; tubes/cuves en 5 implémentations ; 3 sphères ombrées différentes.

### Chimie ch9 à ch13 (`chimie/*-tableau/`)
- **H₃O⁺ en 4 apparences** : `Rendu.MODELES.H3O` (O + 3 H blancs), eau + H⁺ **jaune** (tds/acides, ab/eau, ab/base), sphère **orange** (ab/exploiter, ab/figures), jaune (tds/diluer).
- **HO⁻** : modèle O+H, sphère **bleue** (ab/exploiter), sphère **rouge** (cin/conductimetrie, tds/dilution).
- **Électron** bleu (prérequis, tlr/rappels) / **vert** (tlr/transfert:395) ; **H⁺ jaune** (`Rendu.EL.Hp`) mais proton **rouge** dans les prérequis.
- Carbone **gris** dans toutes les palettes CPK (6 palettes divergentes : commun.js, deroule.js, tds/acides, tds/avancement, ab/base, tlr/rencontres) — le lexique dit jaune.
- Cl⁻ vert / cyan ; Na violet / noyau orange ; Cu²⁺ bleu / Cu orangé.
- pH-mètre en 4 apparences (anthracite `Peinture.phmetre` contre 12 copies grises à écran vert) ; bécher : 25 copies de `Peint.becher` + `Peinture.becher` + 3 variantes ; burette en 5 versions ; thermomètre en 3 tailles ; solution « incolore » en 6 valeurs ; BBT en 4 jeux ; diiode en 3 dégradés.

### Physique (`physics/*-tableau/`)
- **Proton rouge #d9534f** (énergie nucléaire) contre **rouge-orangé #f2683a** (radioactivité) ; neutron gris-bleu de deux clartés ; étiquette « proton » rouge / orange / faible.
- Électron : #3b9cff, #3b82f6, #5b9cf5 (même sens, teintes voisines).
- Grandeurs à la craie : `i` vert / blanc / rouge / bleu / rose ; `u_C` rouge / jaune / cyan / blanc ; `u_R`, `u_b` idem — et la trace de `u_C` change de couleur dans circuit-rc.html.
- Charges des armatures : + rose / − cyan (rc/condensateur) ; + et − rouges (rlc/circuit-lc) ; sphères rouge / bleue (associations).
- Condensateur réaliste en 2 bleus et 3 tailles ; symbole à armatures rouges ou blanches ; bobine en 4 rendus réalistes et 5 palettes de cuivre ; générateur en 4 rendus ; lampe en 6 versions ; pile noire / verte ; oscilloscope à écran vert partout sauf circuit-rc (bleu-noir).
- Ondes : point M orange / rouge / jaune ; haut-parleur en 4 rendus, micro en 3 ; eau turquoise / bleu vif ; 7 copies de la conversion λ → couleur avec des seuils de nom différents ; écran d'observation clair / sombre ; laser en 4 boîtiers.
- `Peint` recopié dans 15 pages ; 12 fonctions `sphere()` de nucléons ; aucun module ne dessine les composants.

### Maths (`maths/*-tableau/`)
- Tangente **jaune** (secante, ln/courbe, primitives/pente) / **orange** (variations, concavite, trace).
- Asymptote **rouge** (branches, trace) / **orange** (lc/approche, ln/limites, ln/signe) / `faible` (symetrie, lc/miroir).
- Zone f < 0 rouge / orange ; flèches de variation vert-rouge / cyan ; point M jaune (K.rond) mais vert, cyan, rouge ou orange ailleurs.

## Reste à faire

Ordre conseillé : d'abord les objets qui ont plusieurs dessins dans un même cours.

1. **SVT ch2 (muscle)** : ATP → `Lexique.atp` (doré) dans `MoleculesPeintes.pastille`, voies, consommation, national ; Ca²⁺ → une couleur à lui (pas le jaune du carbone) ajoutée au lexique ; myosine/actine d'atpase.html → `MoleculesPeintes` ; une seule palette pour muscle, tendon, os (`peindreMuscle` dans `myogramme.js`) ; couleurs des métabolites dans les jauges.
2. **SVT ch3/ch4 (génétique)** : ajouter au lexique ADN (squelette, bases A rouge / T jaune / C bleu / G vert), ARN (orange), nucléotide, ribosome, ARNt, acide aminé, chromosome, noyau (violet), hématie ; brancher `Molecules`, `Etapes.Peint` (une seule version) ; corriger rappels.html (bases permutées) et le brin neuf orange de replication.html.
3. **Chimie** : `Rendu.EL` / `MODELES` / `Peinture.CPK` → couleurs du lexique (C jaune, H⁺ rose) ; H₃O⁺, HO⁻, électron → `Lexique.h3o`, `ho`, `electron` ; un seul bécher, pH-mètre, conductimètre, burette, thermomètre au lexique, à la place des `const Peint` recopiés dans 27 pages.
4. **Physique** : nucléons → `Lexique.proton` / `neutron` (12 `sphere()`), électron → `Lexique.electron` ; ajouter au lexique condensateur (réaliste + symbole), bobine, résistor, générateur, interrupteur, lampe, oscilloscope, ampèremètre/voltmètre (à partir de `Peint` des circuits) ; une couleur par grandeur (i, u_C, u_R, u_b) ; haut-parleur, micro, laser, écran, λ → couleur (une seule fonction).
5. **Maths** : une aide commune (tangente, asymptote, tableau de variations) avec une seule couleur par rôle.
