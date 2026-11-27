# Cours de référence SVT — « Consommation de la matière organique et flux d'énergie », parties 1 et 2 réunies

Demande de l'utilisateur (27/11/2026) : à partir des deux diaporamas d'un professeur de SVT (2ᵉ Bac PC BIOF, parties 1
et 2 du chapitre), construire UN cours de référence qui sera montré à un **inspecteur de SVT** : manipulations bien
réalistes, tous les skills et toutes les règles de génération de cours, ce qui est dit montré et écrit au même instant,
les deux parties en un seul cours, une simplification plus poussée, sur un lien libre, avec les audios et le texte du
script. « Surprenez-moi. »

Ce document est le **contrat** : plan, données, vues de simulation (URL, moments, repères), questions, cahier. Les
diaporamas du professeur ne sont pas dans le dépôt (dépôt public) : tout est réécrit avec nos mots, toute figure est
**recréée en animation peinte** (aucune image du professeur ni du manuel).

- Deck : `backend/data/courses/svt_ch1_reference_consommation_mo.json` — `id` = `svt_ch1_reference_consommation_mo`,
  `mode: "concentration"`, `language: "mixed"`, `status: "draft"` (lien libre seulement, **pas** de `remplace_la_base`),
  préfixe des diapos `rf_`.
- Simulations : `frontend/public/media/simulations/svt/reference_consommation_mo-tableau/` (nouveau dossier). Il charge
  le kit `shared/tableau/`, le lexique `shared/lexique/lexique.js`, et **réutilise** `commun.js`, `peinture.js`, `svt.css`
  du dossier voisin `../reactions_responsables_liberation_energie-tableau/` (ne pas les copier ; si une fonction manque,
  l'ajouter dans un `reference.js` du nouveau dossier). Les vues « rappel » réutilisent telles quelles les pages du
  dossier voisin (`depart.html`, `atp.html`, `taxi.html`, `mitochondrie.html`).
- Lexique visuel (règle 43, un objet = un seul dessin) : glucose = chaîne de 6 billes jaunes ; acide pyruvique = chaîne
  de 3 ; CO₂, O₂, éthanol (2 billes de carbone), ATP (monnaie), NAD⁺/NADH,H⁺ (taxi vide / chargé), mitochondrie, levure :
  les dessins et couleurs de `Lexique` et `SVTPeinture`. Rien de redessiné autrement.

## 1. Ce qui fait de ce cours une référence (à tenir partout)

1. **La démarche d'investigation, visible.** Chaque diapo d'activité porte son étape : Problème → Hypothèse →
   Expérience → Résultats → Analyse → Conclusion. Les nouvelles pages dessinent en haut à droite un **fil de la démarche**
   (six pastilles, celle de l'étape en cours allumée, les précédentes cochées), piloté par `?demarche=<1..6>` et écrit
   dans un `demarche.js` du dossier. La voix nomme l'étape (« دابا l'hypothèse… », « نشوفو les résultats »).
2. **Décrire, puis déduire** (méthode du bac) : devant chaque courbe ou tableau, on lit d'abord les axes (règle 12), on
   décrit (« avant…, après… », avec les valeurs), puis seulement on déduit. Les deux temps sont deux moments distincts.
3. **Le résultat décisif est trouvé par l'élève** (règles 30 et 33) : la manip s'arrête avant le résultat, une question
   d'observation est posée, puis l'animation montre le résultat.
4. **Le fil conducteur : le voyage d'une molécule de glucose.** La même chaîne de 6 billes jaunes est suivie de la cuve
   jusque dans la mitochondrie. Une **carte du voyage** (`voyage.html`) se complète à la fin de chaque activité : c'est
   le schéma bilan du professeur, construit pas à pas.
5. **Simplification poussée** : une idée par diapo ; chaque mot nouveau est découpé et expliqué (aéro-bie, an-aéro-bie,
   glyco-lyse, dé-carboxyl-ase, dé-hydrogén-ase) ; chaque notion dite une première fois, puis redite avec une image du
   quotidien (liste § 5) ; prérequis enseignés avant usage.
6. **Manipulations réalistes** (règle 32) : verrerie avec reflets, liquide visible, agitateur qui tourne, bulles, sondes,
   câbles, interface, écran d'ordinateur où la courbe se trace **en même temps** que le phénomène dans la cuve ; la
   centrifugeuse tourne réellement, les culots se déposent grain par grain.
7. Règles 52 à 56 : ordre des notions, aucune question dans les 6 premières diapos, dit = écrit au mot, notions
   importantes annoncées (phrase différente à chaque fois, `docs/audit-pedagogie/banque-de-phrases.md`), dites, redites,
   rappelées ; tuteur humain (débuts variés, liens, réactions précises).

## 2. Données des documents (à reproduire exactement dans les animations)

**Expérience 1 — levures, cuve bien oxygénée, injection de glucose (ExAO).** Temps en min (0 à 7). Deux axes à gauche :
O₂ dissous en mg/L (2,0 ; 4,0 ; 6,0) en rouge, CO₂ en mmol/L (0,20 ; 0,40) en violet. Injection du glucose à 1,8 min.
- O₂ : ≈ 5,3 mg/L stable de 0 à 1,8 min (léger maximum 5,4 vers 2 min), puis baisse régulière : ≈ 4,7 à 3 min, 3,8 à
  4 min, 2,6 à 5 min, 1,2 à 6 min, 0 à ≈ 6,8 min.
- CO₂ : ≈ 0,16 mmol/L stable jusqu'à ≈ 3 min, puis monte : 0,18 à 4 min, 0,20 à 5 min, 0,25 à 6 min, ≈ 0,31 à 6,8 min.

**Expérience 2 — levures, cuve privée d'O₂ (fermée), glucose déjà présent.** Temps en s (0 à 700). Axe gauche en mg/mL
(O₂, CO₂, éthanol : 0, 10, 20, 30, 40), axe droit glucose en unités arbitraires.
- O₂ : 6 → 0 entre 0 et ≈ 190 s, puis 0.
- Glucose : 42 → 28 à ≈ 175 s (pente forte), puis 22 à 400 s, 19 à 500 s, ≈ 15,5 à 700 s (pente faible).
- CO₂ : ≈ 3 jusqu'à 60 s, 5 à 100 s, 10 à 200 s, 20 à 400 s, 30 à 500 s, ≈ 44 à 700 s.
- Éthanol : 0 jusqu'à ≈ 190 s, puis droite : 10 à 300 s, 20 à 480 s, ≈ 34 à 700 s.
- Lecture : tant qu'il reste de l'O₂ (≈ 3 min) les levures respirent ; ensuite fermentation : CO₂ > 40, éthanol > 30.

**Document « deux levures » (microscope électronique, × ≈ 20 000, barre 0,6 µm).** Milieu aérobie : noyau, vacuole,
hyaloplasme, **mitochondries nombreuses et bien développées**. Milieu anaérobie : noyau, vacuoles, hyaloplasme,
mitochondries rares et réduites.

**Document « glucose marqué au ¹⁴C » (le nombre de + suit la quantité de molécules radioactives).**
G = glucose, P = acide pyruvique, K = acides du cycle de Krebs, E = éthanol.

| Temps | Sans O₂, dehors | Sans O₂, dedans | Avec O₂, dehors | Avec O₂, dedans |
|---|---|---|---|---|
| T0 | G+++ | | G+++ | |
| T1 | G++ | G++ | G++ | G++ |
| T2 | | P++++ | | P++++ |
| T3 | | E++, P++, CO₂++ | | CO₂+, K+, P++ |
| T4 | E+, CO₂++ | E+, CO₂+ | CO₂+ | CO₂+, K+ |
| T5 | E++, CO₂++ | | CO₂++++ | |

**Document « phases de la glycolyse » (hyaloplasme).** (1) Activation : glucose C6 → glucose phosphate C6-P (1 ATP → ADP)
→ fructose diphosphate P-C6-P (1 ATP → ADP). (2) Scission : P-C6-P → 2 glycéraldéhyde phosphate C3-P ; chacun :
NAD⁺ → NADH,H⁺ et un phosphate inorganique entre → acide glycérique diphosphate P-C3-P. (3) Oxydation et formation
d'énergie : chaque P-C3-P → acide pyruvique C3 (CH₃-CO-COOH) avec 2 ADP → 2 ATP. Bilan :
C₆H₁₂O₆ + 2 ADP + 2 Pi + 2 NAD⁺ → 2 CH₃-CO-COOH + 2 ATP + 2 NADH,H⁺.

**Document « centrifugation fractionnée ».** Fragments de foie dans une solution de saccharose → broyage mécanique →
1re centrifugation à faible vitesse → culot riche en noyaux (le surnageant est repris) → 2e centrifugation à grande
vitesse → culot riche en mitochondries.

**Document « mitochondries isolées » (ExAO, bioréacteur, solution oxygénée).** O₂ en µmol/L (65 à 315), temps 0 à 5 min.
t0 : mitochondries seules, O₂ ≈ 275 stable. t1 ≈ 0,6 min : glucose → rien ne change. t2 ≈ 1,3 min : acide pyruvique →
O₂ baisse régulièrement : 265 à 2 min, 250 à 3 min, 232 à 4 min, 215 à 5 min.

**Document « ultrastructure ».** Bâtonnet de quelques µm, diamètre 0,5 à 1 µm ; double membrane ; espace
intermembranaire ≈ 10 nm ; la membrane interne forme des crêtes qui portent des sphères pédonculées ; matrice ; ADN
mitochondrial. Vues : cellule × 8 000 → mitochondrie × 45 000 → sphères pédonculées.

**Document « composition ».** Membrane externe : 40 % lipides, 60 % protéines, comparable à la membrane cellulaire.
Membrane interne : 20 % lipides, 80 % protéines : enzymes d'oxydoréduction, transporteurs d'électrons, ATP synthase
(sphères pédonculées). Matrice : acide pyruvique, transporteurs d'hydrogène (TH₂), ATP, ADP, Pi ; déshydrogénases et
décarboxylases ; pas de glucose.

## 3. Les pages de simulation à créer (dossier `reference_consommation_mo-tableau/`)

Toutes : cadre 760 × 420, mode large, téléphone paysage 429 × 250 (étape en cours seule, texte ≥ 15 px), `moments` nommés,
`play_until`, `set_parameters`, `repere` sur chaque objet que la voix nomme, `?depart=<moment>` pour ouvrir figée (deux
diapos de suite sur la même page ont des URL distinctes), `ce_qui_se_voit`, fil de la démarche `?demarche=`.
Compter = allumer un à un avec le numéro (règle 44). Données tabulées : l'animation d'abord, puis les valeurs volent
dans le tableau (règle 35). Vérification : captures Playwright de chaque moment à 760 × 420 et 429 × 250, console vide.

| Page | Vues / moments (dans l'ordre) | Repères |
|---|---|---|
| `pate.html` | La pâte à pain. `bol` (pâte plate, sachet de levure de boulanger) → `levure_ajoutee` → `gonfle` (la pâte double, bulles) → `zoom` (loupe : des levures et des bulles de CO₂ dans la pâte) → `question` (« d'où la levure tire-t-elle son énergie ? » écrite) | `pate`, `sachet`, `bulles`, `levures`, `question` |
| `levure.html` | La levure. `microscope` (microscope peint, lame) → `champ` (levures bourgeonnantes, barre d'échelle 1,5 µm) → `une_cellule` (une levure agrandie : paroi, membrane, noyau, vacuole, hyaloplasme, mitochondries) → `aerobie` (bocal ouvert, bulles d'air, mot « aérobie » découpé aéro·bie) → `anaerobie` (bocal fermé, mot an·aéro·bie) | `microscope`, `echelle`, `noyau`, `vacuole`, `hyaloplasme`, `mitochondrie`, `bocal_ouvert`, `bocal_ferme` |
| `exao-levures.html?vue=montage` | Le montage, un élément à la fois : `bioreacteur` → `suspension` → `agitateur` (le barreau tourne) → `sonde_o2` → `sonde_co2` → `seringue` → `interface` → `ordinateur` (écran allumé, axes vides) → `complet` | un par élément |
| `exao-levures.html?vue=exp1` | `axes` (les deux axes lus : unités, graduations allumées) → `avant` (0 à 1,8 min : deux paliers, valeurs écrites 5,3 mg/L et 0,16 mmol/L) → `injection` (la seringue est poussée, nuage dans la cuve, flèche « injection glucose » à 1,8 min) → **arrêt pour l'observation** → `o2_baisse` (jusqu'à 6,8 min : O₂ → 0 ; les levures de la cuve « avalent » des bulles d'O₂) → `co2_monte` (0,16 → 0,31) → `decrire` (phrases de description écrites) → `deduire` (« respiration cellulaire » écrit) | `sonde_o2`, `sonde_co2`, `seringue`, `courbe_o2`, `courbe_co2`, `fleche_injection`, `axe_temps`, `axe_o2`, `axe_co2`, `conclusion` |
| `exao-levures.html?vue=exp2` | Cuve fermée par un bouchon. `axes` (temps en secondes, rappel 60 s = 1 min ; axe gauche mg/mL, axe droit glucose) → `depart_valeurs` (O₂ 6, glucose 42, CO₂ 3, éthanol 0) → `phase1` (0 → 190 s : O₂ → 0, CO₂ presque constant, pas d'éthanol) → `o2_zero` (190 s ≈ 3 min allumé) → **arrêt pour l'observation** → `co2_monte` → `ethanol_apparait` → `glucose_continue` → `fin` (700 s : CO₂ 44, éthanol 34) → `decrire` → `deduire` (« fermentation alcoolique ») | `bouchon`, `courbe_o2`, `courbe_glucose`, `courbe_co2`, `courbe_ethanol`, `instant_190`, `conclusion` |
| `equation.html?vue=respiration` | Modèles moléculaires peints. `glucose` (6 billes jaunes + formule C₆H₁₂O₆) → `o2` (6 O₂ arrivent, comptés en allumant) → `fleche` → `co2` (6 CO₂ sortent, comptés : les 6 carbones du glucose partent un par un) → `eau` (6 H₂O) → `energie` (éclat « beaucoup d'énergie ») → `equation` (l'équation écrite entière, équilibrée) | `glucose`, `o2`, `co2`, `eau`, `energie`, `equation` |
| `equation.html?vue=fermentation` | `glucose` → `fleche` → `ethanol` (2 éthanol C₂H₅OH : 2 billes chacun) → `co2` (2 CO₂) → `compte` (2 × 2 + 2 × 1 = 6 carbones, allumés) → `energie` (petit éclat « peu d'énergie ») → `reste` (l'éthanol garde de l'énergie : halo) → `equation` | `glucose`, `ethanol`, `co2`, `energie`, `equation` |
| `deux-levures.html` | Deux coupes peintes façon microscope électronique, côte à côte. `aerobie` (levure du milieu 1 seule) → `anaerobie` (levure du milieu 2) → **arrêt pour l'observation** (« quelle différence ? ») → `mitochondries` (les mitochondries s'allument une à une et se comptent des deux côtés) → `legendes` (noyau, vacuole, hyaloplasme, mitochondrie) → `conclusion` (respiration ↔ mitochondrie ; fermentation ↔ hyaloplasme) | `levure_aerobie`, `levure_anaerobie`, `mitochondries_aerobie`, `mitochondries_anaerobie`, `hyaloplasme`, `conclusion` |
| `comparer.html` | Le tableau bilan construit en animation, ligne par ligne, chaque ligne illustrée d'une vignette animée avant d'entrer dans le tableau : `milieu` → `gaz` → `glucose` → `energie` → `lieu` → `definitions` (oxydation complète / incomplète) | `ligne_milieu`, `ligne_gaz`, `ligne_glucose`, `ligne_energie`, `ligne_lieu`, `colonne_respiration`, `colonne_fermentation` |
| `marquage.html` | Le glucose marqué. `principe` (un glucose « avec une balise » : un carbone qui clignote ; compteur de radioactivité) → `deux_cultures` (sans O₂ / avec O₂) → `t0` → `t1` (le glucose entre) → `t2` (acide pyruvique dans l'hyaloplasme, des deux côtés : la chaîne de 6 coupée en deux chaînes de 3) → `glycolyse` (mot écrit, découpé glyco·lyse) → `t3_sans` → `t4_sans` → `t5_sans` → `t3_avec` (dans la mitochondrie : acides de Krebs + CO₂) → `t4_avec` → `t5_avec` → `tableau` (les + volent dans le tableau du document) | `glucose`, `pyruvate`, `ethanol`, `co2`, `krebs`, `mitochondrie`, `hyaloplasme`, `dehors`, une par ligne `t0`…`t5` |
| `voyage.html?etape=1..4` | La carte du voyage du glucose (schéma bilan), cumulative. Étape 1 (fin activité 1) : dehors → dedans → glycolyse → acide pyruvique → deux routes (avec O₂ : mitochondrie, acides de Krebs + CO₂ ; sans O₂ : éthanol + CO₂). Étape 2 (fin activité 2) : la glycolyse détaillée (2 ATP, 2 NADH,H⁺). Étape 3 (fin activité 3) : la mitochondrie détaillée (membranes, matrice, enzymes). Étape 4 (bilan) : tout, avec « à suivre » sur la matrice. Moments : un par flèche. Bouton imprimer. | un par nœud |
| `glycolyse-phases.html` | Trois bandes colorées (activation, scission, oxydation). `glucose_entre` → `atp1` (une pièce ATP payée, un P s'accroche) → `atp2` → `fructose_dp` (P-C6-P) → `scission` (coupé en deux C3-P) → `taxi1`, `taxi2` (NAD⁺ → NADH,H⁺, un taxi par branche) → `pi` (un Pi entre sur chaque branche : P-C3-P) → `atp_branche1` (2 ATP) → `atp_branche2` (2 ATP) → `pyruvates` (2 acides pyruviques, formule CH₃-CO-COOH) → `compte_atp` (4 gagnés − 2 payés = 2, allumés) → `bilan` (équation globale) | `glucose`, `atp_payes`, `fructose_dp`, `c3_gauche`, `c3_droite`, `taxis`, `atp_gagnes`, `pyruvates`, `bilan`, `phase1`, `phase2`, `phase3` |
| `centrifugation.html?vue=principe` | `manege` (image du quotidien : une essoreuse à salade / un manège, ce qui est lourd part au bord) → `tube` (un tube qui tourne, grains lourds et légers) → `culot` (les lourds au fond = culot, le reste = surnageant, mots écrits) | `tube`, `culot`, `surnageant` |
| `centrifugation.html?vue=etapes` | `foie` (fragments de foie dans la solution de saccharose) → `broyage` (le piston broie : les cellules éclatent, noyaux et mitochondries libérés, dessinés) → `centri1` (la centrifugeuse tourne à faible vitesse, compteur de tours) → `culot_noyaux` → **arrêt pour l'observation** (« où sont les mitochondries ? ») → `surnageant` (versé dans un nouveau tube) → `centri2` (grande vitesse) → `culot_mitochondries` → `bilan` | `foie`, `broyeur`, `centrifugeuse`, `culot_noyaux`, `surnageant`, `culot_mitochondries` |
| `exao-mitochondries.html` | Bioréacteur réaliste (seringue, thermomètre, agitateur, oxymètre, interfaces, ordinateur). `axes` → `t0` (275 µmol/L, palier) → `glucose_injecte` (t1) → **arrêt pour l'observation** → `rien` (palier continue) → `pyruvate_injecte` (t2) → `o2_baisse` (jusqu'à 215 à 5 min ; dans la cuve les mitochondries « avalent » l'O₂) → `decrire` → `deduire` | `seringue`, `oxymetre`, `mitochondries`, `courbe`, `t1`, `t2`, `conclusion` |
| `zoom.html` | `cellule` (cellule × 8 000, mitochondries roses) → `cadre` (un cadre rouge sur une mitochondrie) → `mitochondrie` (zoom animé × 45 000 : double membrane, crêtes) → `taille` (0,5 à 1 µm, rappel 1 µm = un millième de mm) → `cadre2` → `spheres` (zoom : sphères pédonculées sur une crête) | `cellule`, `mitochondrie`, `cretes`, `spheres` |
| `composition.html` | Coupe peinte : hyaloplasme, membrane externe, espace, membrane interne, matrice. `externe` (40 / 60, deux barres qui se remplissent) → `comme_cellule` → `interne` (20 / 80) → `enzymes_interne` (trois familles, chacune dessinée dans la membrane) → `atp_synthase` (la sphère pédonculée s'allume) → `matrice` (ce qu'elle contient, pas de glucose : un glucose barré) → `enzymes_matrice` (décarboxylase : un CO₂ retiré ; déshydrogénase : des H retirés vers un taxi) → `hypothese` | `membrane_externe`, `membrane_interne`, `matrice`, `sphere`, `decarboxylase`, `deshydrogenase` |
| `bilan.html` | Fiche « Ce qu'il faut retenir », écrite point par point, page de l'élève, imprimer (modèle : `bilan.html` du dossier voisin) | un par point |

## 4. Plan du cours (41 diapos, 5 séances, 11 blocs)

`D` = étape de la démarche (P problème, H hypothèse, E expérience, R résultats, A analyse, C conclusion). `★` = notion
importante : annonce d'attention (phrase différente à chaque fois), dite, écrite au mot, redite autrement, relue, puis
rappelée dans une diapo suivante. `Obs` = question d'observation (résultat trouvé par l'élève).

### Séance 1 — Une question et trois rappels (bloc 1, aucune question : règle 53)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 1 | `rf_ouverture_cours` | Consommation de la matière organique et flux d'énergie | — | Ouverture (règle 49) : bienvenue, nom du chapitre, ce qu'on apprend (respiration, fermentation, glycolyse, mitochondrie), poids au national, comment on travaille. |
| 2 | `rf_o1_pate` | Pourquoi la pâte à pain gonfle-t-elle ? | `pate.html` | D = P. La levure de boulanger fait gonfler la pâte : elle vit, elle a besoin d'énergie. Problème écrit : d'où une cellule tire-t-elle son énergie ? |
| 3 | `rf_r1_cellule` | Rappel : la cellule | `depart.html?vue=cellule` | Membrane, hyaloplasme (le liquide de la cellule), noyau, organites. |
| 4 | `rf_r2_glucose` | Rappel : le glucose, de l'énergie rangée | `depart.html?vue=glucose` | Matière organique, C₆H₁₂O₆, 6 carbones = chaîne de 6 billes ; image : un billet de 100 dirhams. |
| 5 | `rf_r3_levure` | La levure : une seule cellule | `levure.html` | Champignon unicellulaire ; avec O₂ (aérobie) ou sans (anaérobie) ; mots découpés. |

### Séance 2 — Activité 1 : mettre en évidence la respiration et la fermentation

Bloc 2 (diapos 6 à 10)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 6 | `rf_a1_montage` | Le montage ExAO | `exao-levures.html?vue=montage&demarche=3` | Chaque élément nommé quand il arrive ; à quoi sert chaque sonde. |
| 7 | `rf_a1_exp1_avant` | Expérience 1 : avant le glucose | `…?vue=exp1&depart=0&demarche=3` | Lire les axes, puis les deux paliers. Hypothèse dite : si la levure utilise le glucose avec O₂, alors O₂ doit baisser. |
| 8 | `rf_a1_exp1_injection` | On injecte le glucose | `…?vue=exp1&depart=avant&demarche=4` | Injection. **Obs** : « O₂ va monter, rester stable ou baisser ? ». Puis O₂ → 0, CO₂ ↑. |
| 9 | `rf_a1_exp1_deduire` | Décrire, puis déduire ★ | `…?vue=exp1&depart=co2_monte&demarche=5` | Description en deux phrases avec les valeurs ; déduction : absorption d'O₂ + rejet de CO₂ = **respiration cellulaire**. |
| 10 | `rf_a1_equation_respi` | L'équation de la respiration ★ | `equation.html?vue=respiration&demarche=6` | C₆H₁₂O₆ + 6 O₂ → 6 CO₂ + 6 H₂O + énergie ; les 6 carbones comptés. Image : le billet entièrement changé en monnaie. |

Question du bloc 2 (après 10) : QCM « Dans l'expérience 1, après l'injection du glucose… » (description correcte parmi 3).
Retrouver : écrire l'équation de la respiration.

Bloc 3 (diapos 11 à 14)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 11 | `rf_a1_exp2_axes` | Expérience 2 : une cuve sans dioxygène | `exao-levures.html?vue=exp2&depart=0&demarche=3` | Cuve fermée ; quatre courbes ; lire les deux axes ; secondes ↔ minutes. |
| 12 | `rf_a1_exp2_phase1` | Les trois premières minutes | `…?vue=exp2&depart=depart_valeurs&demarche=4` | O₂ 6 → 0 en ≈ 190 s ; pas d'éthanol : les levures respirent encore. |
| 13 | `rf_a1_exp2_phase2` | Plus de dioxygène : et après ? ★ | `…?vue=exp2&depart=o2_zero&demarche=4` | **Obs** : « sans O₂, les levures s'arrêtent-elles ? ». CO₂ > 40, éthanol > 30, le glucose baisse encore : **fermentation alcoolique**. |
| 14 | `rf_a1_equation_ferm` | L'équation de la fermentation ★ | `equation.html?vue=fermentation&demarche=6` | C₆H₁₂O₆ → 2 C₂H₅OH + 2 CO₂ + énergie (peu) ; l'éthanol garde de l'énergie. Image : le billet changé à moitié. |

Question du bloc 3 : vrai/faux ou QCM sur ce qui apparaît seulement sans O₂ (l'éthanol). Retrouver : équation de la fermentation.

### Séance 3 — Activité 1 (suite) : où, et que devient le glucose ?

Bloc 4 (diapos 15 à 18)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 15 | `rf_a2_deux_levures` | Deux levures au microscope | `deux-levures.html?demarche=4` | **Obs** : « quelle différence entre les deux ? » ; les mitochondries comptées. |
| 16 | `rf_a2_localisation` | Où se passe chaque réaction ? ★ | `deux-levures.html?depart=legendes&demarche=6` | Respiration ↔ mitochondries ; fermentation ↔ hyaloplasme (elle n'a pas besoin de mitochondries). |
| 17 | `rf_a2_tableau` | Respiration ou fermentation : le tableau | `comparer.html?demarche=6` | Cinq lignes construites une à une. |
| 18 | `rf_a2_definitions` | Les deux définitions ★ | `comparer.html?depart=lieu&demarche=6` | Oxydation complète (milieu aérobie, mitochondries, beaucoup d'énergie) / incomplète (anaérobie, hyaloplasme, peu d'énergie, déchet organique encore riche en énergie). Construites par trois questions (règle 14), relues. |

Question du bloc 4 : associer chaque caractéristique à respiration ou fermentation (association, règle 47) ou QCM.
Retrouver : définition de la fermentation.

Bloc 5 (diapos 19 à 23)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 19 | `rf_a3_marquage` | Suivre le glucose à la trace | `marquage.html?demarche=3` | Principe du marquage au ¹⁴C (une balise sur le glucose) ; deux cultures. |
| 20 | `rf_a3_glycolyse` | Le début est le même : la glycolyse ★ | `marquage.html?depart=deux_cultures&demarche=4` | T0, T1, T2 : dehors, dedans, acide pyruvique dans l'hyaloplasme, **dans les deux milieux**. |
| 21 | `rf_a3_sans_o2` | Sans dioxygène : éthanol et CO₂ | `marquage.html?depart=glycolyse&demarche=4` | T3 à T5 sans O₂. |
| 22 | `rf_a3_avec_o2` | Avec dioxygène : la mitochondrie ★ | `marquage.html?depart=t5_sans&demarche=4` | T3 à T5 avec O₂ : acides de Krebs + CO₂ dans la mitochondrie ; **Obs** avant T3 : « où va l'acide pyruvique ? ». |
| 23 | `rf_a3_voyage1` | La carte du voyage du glucose | `voyage.html?etape=1&demarche=6` | Schéma bilan de l'activité 1, construit flèche par flèche. |

Question du bloc 5 : QCM « quelle étape est commune à la respiration et à la fermentation ? ». Retrouver : ce qu'est la glycolyse et où elle a lieu.

### Séance 4 — Activité 2 : la glycolyse

Bloc 6 (diapos 24 et 25, rappels juste avant leur usage)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 24 | `rf_g0_atp` | Rappel : l'ATP, la monnaie de la cellule | `atp.html?depart=0&rappel=1` | ATP ⇄ ADP + Pi ; l'ATP = les pièces de monnaie. |
| 25 | `rf_g0_taxi` | Rappel : le transporteur d'hydrogène | `taxi.html?depart=0` | NAD⁺ + 2 H⁺ + 2 e⁻ → NADH,H⁺ ; taxi vide / chargé ; « réduit » = chargé. |

Bloc 7 (diapos 26 à 29)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 26 | `rf_g1_activation` | Phase 1 : activer le glucose | `glycolyse-phases.html?demarche=5` | 2 ATP payés → fructose diphosphate. Image : payer pour entrer. |
| 27 | `rf_g2_scission` | Phase 2 : couper en deux | `…?depart=fructose_dp&demarche=5` | C6 → 2 C3 ; un taxi chargé par branche ; un Pi entre. |
| 28 | `rf_g3_oxydation` | Phase 3 : l'énergie récupérée | `…?depart=pi&demarche=5` | 2 ATP par branche ; 2 acides pyruviques. |
| 29 | `rf_g4_bilan` | Le bilan de la glycolyse ★ | `…?depart=pyruvates&demarche=6` | 4 − 2 = 2 ATP ; 2 NADH,H⁺ ; 2 acides pyruviques ; dans l'hyaloplasme, sans O₂ ; équation globale ; carte du voyage rappelée. |

Question du bloc 7 : calcul « combien d'ATP gagnés pour une molécule de glucose ? » avec démonstration jouée sur la figure.
Retrouver : équation globale de la glycolyse.

### Séance 5 — Activité 3 : la mitochondrie, siège de la respiration

Bloc 8 (diapos 30 à 33)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 30 | `rf_m1_principe` | Comment isoler des mitochondries ? | `centrifugation.html?vue=principe&demarche=3` | La centrifugation : séparer selon la densité en tournant vite. |
| 31 | `rf_m1_etapes` | La centrifugation fractionnée | `centrifugation.html?vue=etapes&demarche=3` | Les étapes ; **Obs** après la 1re centrifugation : « les mitochondries sont dans le culot ou dans le surnageant ? ». |
| 32 | `rf_m2_glucose` | Des mitochondries seules : on ajoute du glucose | `exao-mitochondries.html?demarche=4` | Hypothèse : si la mitochondrie utilise le glucose, O₂ baisse. **Obs**. Résultat : rien. |
| 33 | `rf_m2_pyruvate` | On ajoute l'acide pyruvique ★ | `…?depart=rien&demarche=5` | O₂ : 275 → 215 µmol/L ; la mitochondrie utilise l'acide pyruvique, pas le glucose ; rappel : il vient de la glycolyse. |

Question du bloc 8 : QCM « quel métabolite la mitochondrie utilise-t-elle ? » avec justification par la courbe.

Bloc 9 (diapos 34 à 36)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 34 | `rf_m3_zoom` | De la cellule à la mitochondrie | `zoom.html?demarche=4` | Deux zooms ; tailles. |
| 35 | `rf_m3_legender` | La mitochondrie : six mots ★ | `mitochondrie.html?depart=0` | Membrane externe, espace intermembranaire, membrane interne, crêtes, matrice, sphères pédonculées (+ ADN mitochondrial dit). |
| 36 | `rf_m3_construire` | À toi de légender | `mitochondrie.html?vue=construire&depart=0` | Schéma à légender par l'élève (contrat `legende_*`), compté au bilan. |

Bloc 10 (diapos 37 et 38)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 37 | `rf_m4_membranes` | De quoi sont faites les deux membranes ? | `composition.html?demarche=5` | 40/60 et 20/80 ; membrane externe = échanges ; membrane interne = enzymes d'oxydoréduction, transporteurs d'électrons, ATP synthase. |
| 38 | `rf_m4_matrice` | La matrice : deux familles d'enzymes ★ | `composition.html?depart=atp_synthase&demarche=6` | Acide pyruvique présent, pas de glucose ; décarboxylases (retirent du CO₂), déshydrogénases (retirent des H, donnés aux taxis) ; hypothèse pour la suite. |

Question du bloc 10 : QCM relation structure-fonction (« pourquoi la membrane interne est-elle si riche en protéines ? »).

Bloc 11 (diapos 39 à 41)

| # | id | Titre | Page | Contenu |
|---|---|---|---|---|
| 39 | `rf_b1_bilan` | Ce qu'il faut retenir | `bilan.html` | La fiche, point par point. |
| 40 | `rf_b2_voyage` | La carte complète du voyage | `voyage.html?etape=4` | Tout le chapitre en une image ; « à suivre : que devient l'acide pyruvique dans la matrice ? ». |
| 41 | `rf_fermeture_cours` | Ce qu'il faut retenir, et comment réviser | — | Fermeture (règle 49). |

## 5. Les images du quotidien (une par notion, toujours la même)

- Glucose = un billet de 100 dirhams ; ATP = les pièces de monnaie (on ne paie rien avec le billet entier).
- Respiration = le billet entièrement changé en pièces ; fermentation = seulement une petite partie changée, le reste
  (l'éthanol) repart avec sa valeur.
- Glycolyse = couper le billet en deux ; il faut payer 2 pièces pour passer au guichet, on en reçoit 4.
- NAD⁺ = un taxi vide ; NADH,H⁺ = le taxi chargé de deux hydrogènes.
- Mitochondrie = la centrale électrique de la cellule ; les crêtes = des étagères qui donnent plus de place.
- Marquage au ¹⁴C = une balise GPS sur le glucose.
- Centrifugation = l'essoreuse à salade.

## 6. Compétences (suivi des acquis, 8, avec 3 à 4 rappels chacune)

C1 Analyser un résultat d'ExAO (lire les axes, décrire, déduire). C2 Définir la respiration et la fermentation et écrire
leurs équations. C3 Localiser respiration (mitochondrie) et fermentation (hyaloplasme). C4 Retracer le devenir du
glucose (glycolyse commune, acide pyruvique au carrefour). C5 Décrire les trois phases et le bilan de la glycolyse.
C6 Montrer que la mitochondrie utilise l'acide pyruvique (centrifugation, ExAO). C7 Légender l'ultrastructure de la
mitochondrie. C8 Relier la composition des membranes et de la matrice à leur rôle.

## 7. Le cahier (skill cahier-de-l-eleve)

Général et organisé, jamais les valeurs d'une expérience : titres I, II, III (= activités), définitions encadrées
(respiration cellulaire, fermentation, glycolyse, milieu aérobie / anaérobie, centrifugation), les trois équations
encadrées, le tableau respiration / fermentation, `cahier_figures` : la carte du voyage, le schéma des trois phases de
la glycolyse, le schéma légendé de la mitochondrie.

## 8. Pour l'inspecteur : le dossier du cours

`frontend/public/media/simulations/svt/reference_consommation_mo-tableau/dossier.html` (généré par
`scripts/reference/dossier_inspecteur.py` à partir du deck) : fiche pédagogique (niveau, place dans le programme,
objectifs, compétences, prérequis, durée, démarche), tableau de correspondance « diaporama du professeur → nos diapos »,
puis pour chaque diapo : titre, étape de la démarche, ce que montre l'animation, le texte dit (français et darija),
le lecteur audio de sa piste, la question et ses réactions, les lignes du cahier. Imprimable.
