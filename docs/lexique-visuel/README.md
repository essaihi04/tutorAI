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

## Les modules (un par matière, tous dans `frontend/public/media/simulations/shared/lexique/`)

| Module | Objet global | Contenu | Branché sur |
|---|---|---|---|
| `lexique.js` | `window.Lexique` | atomes et molécules (glucose, acides pyruvique et lactique, éthanol, CO₂, H₂O, O₂, H₃O⁺, HO⁻), proton, électron, neutron, modèle de l'atome (noyau, nuage, couches K L M, charge d'un ion), Ca²⁺, ATP/ADP/Pi, NAD, FAD, CoA, cellule, mitochondrie, membrane, protéine, levure, bécher simple | SVT ch1 (via `peinture.js`), chimie TC atome |
| `lexique-physique.js` | `Lexique.physique` | générateur, bornes, condensateur (réaliste, armatures, symbole), résistor, interrupteur, bobine (réaliste, symbole), noyau de fer, lampe, ampèremètre/voltmètre, ohmmètre, oscilloscope, GBF, cordons ; ondes (corde, perle, poignée, micro, écran, trace, front) ; `lumiere.couleurDe(λ)` ; `GRANDEURS` | RC, RL, RLC (15 pages) |
| `lexique-chimie.js` | `Lexique.chimie` | bécher, bain, goutte, filet, pipette, compte-gouttes, glaçon, pH-mètre et sonde, conductimètre et cellule, bulles ; `SOLUTIONS`, `BBT` ; montage à reflux (`montageReflux`, ballon, réfrigérant à boules, chauffe-ballon, potence, élévateur, tuyau, pierre ponce, vapeur, gouttelette), CCM (plaque, cuve, capillaire, lampe UV, diiode), filtration (entonnoir, flocons), éprouvette, tube, flacon, thermomètre, balance, ions (`ion`, `IONS`) ; `LIQUIDES` | chimie ch9 à ch13 (25 pages), TC synthèse (7 pages) |
| `lexique-genetique.js` | `window.Molecules` = `Lexique.genetique` | ADN, ARN, bases, nucléotides, ribosome, ARNt, acides aminés, protéine, noyau, cytoplasme, hématie | SVT ch4 (12 pages) |
| `lexique-muscle.js` | `window.MoleculesPeintes` = `Lexique.muscle` | actine, myosine, tropomyosine, troponine, Ca²⁺, pastille ATP, réticulum, cuve, fibre | SVT ch2 (4 pages) |
| `lexique-maths.js` | `Lexique.maths` | `ROLES` (courbe cyan, point jaune, tangente orange, asymptote pointillé blanc, + vert, − rouge), `tangente()`, `asymptote()`, `couleurSigne()` | les six cours de maths (chargé par `maths-tableau.js`) |

Un dessin de module est le plus répandu dans les cours, copié mot pour mot : les pages branchées ne changent pas
d'aspect, seules les variantes minoritaires prennent le dessin commun. Dans une page, la copie locale devient
`  nom(...a) { return window.Lexique.<matière>.nom(...a); }` (même nom, même signature).

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
| Ca²⁺ | [calcium.md](calcium.md) | `calcium` |
| Atome (C, H, O, N, P) | ci-dessous | `atome(ctx, x, y, 'C')`, `chaine`, `positionsChaine` |
| Atome (modèle) : noyau, nuage, couches K L M, ion | [atome.md](atome.md) | `noyau`, `nuage`, `placesNuage`, `couche`, `placesCouche`, `atomeModele`, `charge` |
| Cellule, hyaloplasme, noyau | [cellule.md](cellule.md) | `cellule` |
| Mitochondrie, membrane interne, sphère pédonculée | [mitochondrie.md](mitochondrie.md) | `mitochondrie`, `membrane`, `spherePedonculee` |
| Protéine | [proteine.md](proteine.md) | `proteine` |
| Levure | [levure.md](levure.md) | `levure` |
| Bécher | [becher.md](becher.md) | `becher` |
| Montage à reflux (ballon, réfrigérant, chauffe-ballon, potence) | [montage-reflux.md](montage-reflux.md) | `Lexique.chimie.montageReflux`, `ballon`, `refrigerant`, `chauffeBallon` |
| CCM (plaque, cuve, capillaire, lampe UV) | [ccm.md](ccm.md) | `Lexique.chimie.plaque`, `cuve`, `cuveDevant` |
| Filtration, précipité, éprouvette, flacon, ions | [filtration.md](filtration.md) | `Lexique.chimie.entonnoir`, `flocons`, `ion` |
| **Physique** | | |
| Générateur, GBF | [generateur.md](generateur.md) | `physique.generateur`, `gbf`, `borne` |
| Condensateur | [condensateur.md](condensateur.md) | `physique.condensateur`, `armatures`, `symboleCondo` |
| Bobine | [bobine.md](bobine.md) | `physique.bobine`, `noyau`, `symboleBobine` |
| Résistor | [resistor.md](resistor.md) | `physique.resistor` |
| Interrupteur | [interrupteur.md](interrupteur.md) | `physique.interrupteur`, `plot` |
| Lampe | [lampe.md](lampe.md) | `physique.lampe` |
| Ampèremètre, voltmètre, ohmmètre | [appareils-de-mesure.md](appareils-de-mesure.md) | `physique.cadran`, `ohmmetre` |
| Oscilloscope | [oscilloscope.md](oscilloscope.md) | `physique.oscillo`, `ondes.oscillo`, `ondes.trace` |
| Couleurs des grandeurs (u_C, i, u_R, u_b, E) | [grandeurs-electriques.md](grandeurs-electriques.md) | `physique.GRANDEURS` |
| Corde, perle, point M | [corde.md](corde.md) | `physique.ondes.corde`, `perle` |
| Micro | [micro.md](micro.md) | `physique.ondes.micro` |
| Lumière (λ → couleur) | [lumiere.md](lumiere.md) | `physique.lumiere.couleurDe` |
| **Chimie** | | |
| Verrerie | [verrerie.md](verrerie.md) | `chimie.becher`, `bain`, `goutte`, `pipette`… |
| pH-mètre | [ph-metre.md](ph-metre.md) | `chimie.phmetre`, `sonde` |
| Conductimètre | [conductimetre.md](conductimetre.md) | `chimie.conductimetre`, `cellule` |
| Teintes des solutions | [solutions.md](solutions.md) | `chimie.SOLUTIONS`, `BBT` |
| **SVT** | | |
| Génétique (ADN, ARN…) | [genetique.md](genetique.md) | `Molecules.*` |
| Muscle (actine, myosine…) | [muscle.md](muscle.md) | `MoleculesPeintes.*` |
| **Maths** | | |
| Rôles (courbe, point, tangente, asymptote, signes) | [maths.md](maths.md) | `Lexique.maths` |

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

## Décision du 18 novembre 2026 : le proton est rose partout

Règle de l'utilisateur : « le proton en rose partout ». Un ion H⁺ est un proton : bille rose `[244,114,182]` en SVT, en
chimie (H⁺, H acide, H₃O⁺, flèches de transfert du proton) et en physique (proton du noyau). Le carbone est jaune dans
toutes les matières (la chimie l'avait gris).

Les deux phrases de voix qui nommaient l'ancienne couleur sont réécrites (cours en ligne ET copie en attente) :
- chimie ch11, diapositive `td_b1_acide` : « Regarde cette petite boule rose : c'est le proton, H plus » /
  « شوف هاد الكورة الصغيرة اللي باللون rose » ; et la réaction préparée `q/1/1` (« رجع للكورة اللي باللون rose ») ;
- physique ch5, diapositive `en_d1_composition` : « Z, c'est le nombre de protons, les sphères roses » /
  « الكورات اللي باللون rose ».
Leurs pistes enregistrées (qui disaient « jaune » / « rouges ») sont retirées : `python -I backend/scripts/lister_voix_attente.py
phys_ch11_transformations_deux_sens phys_ch5_energie_nucleaire` les liste pour le lot Bodi (skill voix-du-cours §3) ; d'ici
là le lecteur lit ces textes avec la voix en direct. Textes `alt` mis à jour.

## Fait en chimie (18 novembre 2026)

- O et H des modèles (`Rendu.EL` des 5 `commun.js`, `Peinture.CPK` des 4 `deroule.js`) : valeurs du lexique.
- HO⁻ : une seule couleur, bleu ciel (charge −) — il était rouge dans cin/conductimetrie, cin/pression,
  tds/conductimetrie, tds/dilution et bleu foncé dans ab/exploiter, ab/figures ; nom écrit en bleu.
- Électron de tlr/transfert : vert → bleu ciel.

## Fait en physique nucléaire (18 novembre 2026)

- Proton : une seule teinte dans les deux cours, le rouge #d9534f de l'énergie nucléaire (la radioactivité avait un
  rouge-orangé #f2683a / #f06a3a / [228,96,54]) ; étiquette « proton » rouge (était orange) ; textes « rouge-orangé » → « rouge ».
- Neutron : gris-bleu #8fa3b8 partout (la radioactivité en avait 4 plus clairs) ; électron : bleu ciel du lexique.
- Le rose du lexique n'est pas appliqué : la voix de ch5 dit « les protons, les sphères rouges » (voir la décision ci-dessus).

## Reste à faire

Les modules existent pour toutes les matières ; ce qui reste, ce sont des pages qui gardent encore un dessin à elles :

1. **SVT** : une seule palette pour muscle, tendon, os (`peindreMuscle` recopié 4 fois, structure.html, myogramme.js) ; SVT ch3 : `Etapes.Peint` de NIG (cellule, noyau, chromosomes) à aligner sur `lexique-genetique.js` (RGP/etapes.js en a une 2ᵉ version) ; brins de réplication dits par la voix (bleu / orange / blanc / rouge) : à reprendre avec une nouvelle voix si l'on veut l'orange réservé à l'ARN.
2. **Chimie** : pH-mètres minoritaires (anthracite de deroule.js, tds/acides, tds/ph, tds/avancement, `Peint.phmetre` de 5 pages), burettes (5 versions), thermomètres (3), loupes (6), fioles, `Peinture.*` de deroule.js ; solutions « incolores », BBT et diiode encore écrits en dur ; Cl⁻ vert / cyan.
3. **Physique** : condensateurs, bobines, résistors, générateurs et lampes peints localement dans carte, figures, energie, rupture, energie-carre (fonctions `condensateurPeint`, `bobinePeinte`, `peindreBobine`, `peindreResistor`, `generateurPeint`…) ; bobine à spires empilées d'observer ; écran bleu-noir de circuit-rc ; couleurs des grandeurs qui s'écartent du code (i blanc / bleu / rose, u_C jaune de circuit-rc) ; ondes : corde torsadée (types, methode-phase), point M rouge / jaune, haut-parleurs (4), micros (3), lasers (4), écrans clair / sombre, 6 copies de `couleurDe` ; nucléons : les 12 fonctions `sphere()` locales (même teinte maintenant, pas encore le module).
4. **Maths** : les autres tangentes, asymptotes et signes passent par `Lexique.maths` au prochain passage sur chaque page ; la courbe de ln reste rouge (objet nommé du cours ln).
5. **Voix** : réenregistrer `td_b1_acide` (+ réaction `q/1/1`) en chimie ch11 et `en_d1_composition` en physique ch5 (`lister_voix_attente.py`).
