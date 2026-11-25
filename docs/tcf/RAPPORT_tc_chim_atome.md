# Rapport — cours /TCF « Modèle de l’atome » (`tc_chim_atome`), 25/11/2026 (session cloud)

## Fichiers

- Cours : `frontend/src/publication/tcf/cours/tc_chim_atome.json` (CourseDeck, `mode: concentration`, `language: mixed`,
  `niveau: tronc_commun_sciences_biof`, `subject: chimie`, sans `audio`).
- Voix : `frontend/src/publication/tcf/cours/tc_chim_atome_voix.json` (écrit par `scripts/tcf/lister_voix_tcf.py`).
- Générateur du cours : `scripts/tcf/construire_tc_chim_atome.py` (le cours est écrit là, diapo par diapo ; il contrôle que
  chaque `mot` est un extrait exact du texte parlé, dans l’ordre, qu’aucun chiffre ni symbole n’est dit, que chaque option a
  ses réactions ; il remplace les mots rares pour la voix et décolle les nombres français de la darija). Le relancer après
  toute modification, puis `lister_voix_tcf.py`.
- Simulations : `frontend/public/media/simulations/chimie/tc_atome-tableau/`
  - gardées et corrigées (premier agent) : `commun.js`, `atome.css`, `prerequis.html` (zoom, charges, ballon, puissances,
    calculs, modele), `histoire.html` (elements, dalton, thomson, bohr, nuage), `rutherford.html` (montage, resultats,
    interpretation). Corrections : ce que la voix nomme est fini **à l’arrêt sur son moment** (la loupe et les atomes de
    `zoom`, le transfert des électrons et l’attraction du `ballon` étaient encore invisibles au moment figé) ; l’étiquette
    « écran fluorescent » sortait du cadre.
  - créées : `structure.html` (atome, electron, noyau, notation, neutralite, tableau &atome=C|O|Cl|Al), `masse.html`
    (somme, methode &atome=O|C|Cl), `dimensions.html` (rapport, stade), `element.html` (isotopes, ions, element,
    conservation), `couches.html` (couches, remplir &atome=…&q=charge), `bilan.html` (fiche, carte, imprimer / PDF).
  - ajouts à `commun.js` : `P.atome`, `P.placesNuage`, `P.noyauCompte` (compter en allumant, numéro sur chaque bille),
    `compte`, `vole` (le nombre vole dans sa case et y est posé à l’arrêt), `avant`, `?vierge=1` (scène vide au départ,
    pour les « À toi » et les questions d’observation : l’aperçu de la figure finie donnait la réponse), rattrapage ×2,2
    d’un arrêt lointain (corrections jouées après une réponse).
  - un objet, un seul dessin : proton = bille rose « + », neutron = bille grise, électron = bille bleu ciel « e− »
    (lexique commun `shared/lexique/lexique.js`). La mission disait « proton rouge » : j’ai gardé le **rose du lexique**
    (règle « le même dessin dans tout le site », le proton / H⁺ est rose partout) ; la voix ne nomme aucune couleur.

## Chiffres

38 diapos, 6 séances, 15 blocs, 8 compétences (C0 à C7, 3 rappels chacune : libre, QCM, vrai/faux), 14 questions « À toi »
(une par bloc, sauf le bloc d’ouverture et celui de la fermeture), 6 démonstrations, 2 questions d’observation
(Rutherford : où arrivent presque toutes les α ; conservation : ce qui se forme dans le bécher), 3 corrections rejouées
après la réponse (`apres_reponse` : tableau du chlore, masse du carbone, couches du chlore), 3 figures de cahier.
164 pistes de voix : 38 diapo, 14 énoncés, 68 réactions, 6 démonstrations, 14 pistes d’observation, 24 énoncés de rappels.

## Plan et méthodes

1. Ouverture ; situation problème (la pièce de cuivre grossie jusqu’aux atomes) ; ce qu’est un modèle (la Terre et le globe).
2. Prérequis de zéro : la charge (attraction / répulsion, puis le ballon frotté : neutre, gagne des électrons → négatif) ;
   les puissances de dix (le mètre divisé par dix, les dix places allumées ; règles du produit et du quotient, écriture
   scientifique).
3. Histoire animée : les quatre éléments (le bois qui brûle), Dalton, Thomson (tube, électron, pain aux raisins),
   Rutherford (montage ; résultats avec question d’observation ; interprétation : vide + noyau +), Bohr, nuage + frise.
4. Électron (q = −e, e = 1,6 × 10⁻¹⁹ C, m_e), noyau (protons et neutrons comptés), ᴬ_Z X (A, Z, N = A − Z comptés en
   allumant), neutralité (électrons comptés, +6e − 6e = 0).
5. **Méthode du tableau** : le tuteur sur ¹²₆C, puis l’élève sur ³⁵₁₇Cl (question N = 18 + correction jouée).
6. **Masse** : la balance (un proton contre un électron, rapport ≈ 1 840) → m ≈ A·m_p ; méthode par le tuteur sur ¹⁶₈O
   (2,67 × 10⁻²⁶ kg), l’élève sur ¹²₆C (2,0 × 10⁻²⁶ kg).
7. **Dimensions** : 10⁻¹⁰ m / 10⁻¹⁵ m, rapport 10⁵ calculé, structure lacunaire ; deuxième façon : la bille de 1 mm au
   centre d’un stade de 100 m (1 mm × 10⁵ = 100 m).
8. Isotopes (¹²C, ¹³C, ¹⁴C), ions (Na perd un électron → cation ; Cl en gagne un → anion), élément chimique (¹⁶O, ¹⁷O, O²⁻),
   conservation (sulfate de cuivre bleu + soude → précipité bleu Cu(OH)₂ animé, question d’observation).
9. **Structure électronique** : couches K, L, M et leurs places comptées, règles 1 et 2 ; le tuteur sur O (électrons qui
   tombent couche par couche, saturée, couche externe), l’élève sur Cl ((K)²(L)⁸(M)⁷, correction jouée) ; un ion (Na⁺ par
   le tuteur, O²⁻ en question).
10. Bilan « Ce qu’il faut retenir » (7 blocs, `acquis`), carte du chapitre, fermeture (conseils, pas de pourcentage du national).

Exemples choisis pour ne pas reprendre ceux de l’évaluation (²⁴₁₂Mg).

## Vérifié (et comment)

- `python -I scripts/verifier_formules.py <cours> <dossier>` : rien. `python -I backend/scripts/verifier_parcours.py` :
  rien. `python backend/scripts/verifier_figures_cahier.py` : 0 erreur.
- `scripts/verifier_pointage.py` : il signale « moment inconnu » pour `rutherford.html?vue=resultats` et `interpretation`
  (sa lecture statique ne lit que la première vue) ; contrôle à l’exécution (Playwright, chaque simulation de chaque diapo,
  jouée moment par moment) : **0 moment inconnu, 0 repère jamais dessiné, 0 `allume` inconnu**.
- Chaque `<script>` : `node --check`. Chaque vue et chaque moment capturés à 760×420 et 429×250, regardés ; corrigé ce qui
  débordait ou se chevauchait (fiche : fraction sur la ligne ⚠ ; élément : cadre et texte ; ions : électron perdu sur le
  texte ; Z allumé mal placé ; Cu²⁺ entassés ; étiquettes de la balance). Aucune erreur console.
- Le cours dans la page /TCF (Vite, Playwright) : les 38 diapos se chargent, chaque diapo à simulation affiche la sienne,
  aucune erreur console, à 1280×720 et 724×350. Remarque : avec `base: '/TCF/'`, le serveur de dev ne sert pas `/media/…`
  à la racine (simulations et avatar en 404 pour tous les cours) ; j’ai testé avec
  `npx vite --config vite.tcf.config.ts --port 5174 --base /` puis `/tcf.html?cours=tc_chim_atome`.
- Mots de la voix : `python -X utf8 scripts/voix/verifier_mots.py ../../../frontend/src/publication/tcf/cours/tc_chim_atome`
  (le chemin relatif contourne `backend/data/courses`) ; 60 mots darija rares remplacés ; `scripts/voix/nombres_fr.py`
  (convertir) : plus de darija collée devant un nombre français (« environ », « jusqu’à », « égale », « en mille… »).

## Reste douteux

- **Mots à faire écouter** (termes du programme ou noms rares dans le corpus, gardés exprès) : couche(s), saturée, nuage
  électronique, cation, anion, lacunaire, positivement / négativement, chargé(e)s, se repoussent / s’attirent, neutres,
  élémentaire, atomique, orbites, éclair(s), fluorescent, plomb, précipité, soude, compte-gouttes, sulfate de cuivre,
  hydroxyde, tribunes, grains, loupe, globe, frise, boules, déviation ; noms propres : Dalton, Thomson, Rutherford, Bohr,
  Schrödinger, De Broglie ; lectures : « C l », « H O moins », « Cu deux plus », « Na plus », « O deux moins »,
  « soixante-douze », « mille huit cent quarante » ; « chlore » est réécrit « klore » par les écritures sûres.
  Darija encore peu vue : الزبيب، يخسر، وكيطيح، نقربو، كيعاونا، كنكتبوها، كنقسموه، فهمش، ضغط، زمان، رقيقة، بقاتش.
- Science : m_p/m_e ≈ 1 840 (1 838) ; « la bille de 1 mm au centre d’un stade de 100 m » est une image (ordre de grandeur
  10⁵) ; l’équation est écrite avec HO⁻ (usage marocain) quand le livre écrit OH⁻.
- Vues : sur téléphone, la balance de `masse.html?vue=somme` laisse de la place vide ; le noyau du chlore (35 billes) a
  des numéros petits quand on compte (lisibles à 760×420, serrés à 429×250).
- Au départ d’une diapo (avant la première commande de la voix), une simulation montre sa figure finie (convention du kit,
  `S.t <= 0`) ; les diapos à question l’évitent avec `&vierge=1`.
- Non fait (fichier partagé, hors de mes fichiers) : remplir `REVOIR_TCF` de `frontend/src/publication/tcf/revoir.ts` pour
  la partie Chimie 2 de l’évaluation. Proposition : 2-1 → `at_s1_atome`, `at_s3_noyau`, `at_d1_rapport`, `at_e1_isotopes` ;
  2-2 → `at_s4_notation`, `at_s6_methode` ; 2-3 → `at_m1_masse`, `at_m2_methode` ; 2-4 → `at_c1_couches`,
  `at_c2_methode` ; 2-5 → `at_e2_ions`, `at_e3_element` ; 2-6 → `at_e2_ions`, `at_c4_ion`.
- Les voix ne sont pas générées (lot Kaggle sans tunnel, plus tard).

Dernier commit poussé sur `tcf-cours` : voir `git log origin/tcf-cours -- docs/tcf/RAPPORT_tc_chim_atome.md`.
