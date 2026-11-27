# Rapport — le cours de référence SVT (session « cours »)

27 novembre 2026. Contrat : `docs/reference-svt/ARCHITECTURE.md`.

## Ce qui est livré

| Fichier | Rôle |
|---|---|
| `backend/data/courses/svt_ch1_reference_consommation_mo.json` | le cours (brouillon, lien libre, sans `audio`) |
| `scripts/reference/cours_diapos.py`, `cours_questions.py`, `construire_cours.py` | la source du cours et son générateur : **on modifie ces fichiers, puis on relance** `python -I scripts/reference/construire_cours.py` (il réécrit le cours, la liste des voix et les lots, et refait les contrôles) |
| `docs/reference-svt/voix_a_generer.json` | toutes les pistes de voix |
| `docs/reference-svt/voix_parties/partie_01…07.json` | les mêmes pistes en 7 lots (≤ 50 pistes, ≤ 12 000 caractères) pour Colab |
| `scripts/reference/dossier_inspecteur.py` → `frontend/public/media/simulations/svt/reference_consommation_mo-tableau/dossier.html` | le dossier de l'inspecteur (148 Ko, autonome, imprimable) |

Dans `cours_diapos.py`, les gestes sont des balises posées dans le texte dit, juste devant le mot : `<m:moment>`
(`play_until`), `<r:repere>` (baguette), `<c:texte>` (carte au centre). Le générateur calcule l'extrait exact (`mot`) :
changer un nom de moment ou de repère = changer un mot dans une balise.

## Le cours en nombres

- 41 diapositives, 5 séances, 11 blocs, 8 compétences (25 rappels : 3 chacune, 4 pour C2).
- 8 questions de bloc : 6 QCM, 1 association (bloc 4, règle 47), 1 calcul avec démonstration jouée sur la figure
  (glycolyse : `lignes[].allume` → `atp_payes`, `atp_gagnes`, `bilan`) ; plus le schéma à légender (bloc 9).
  Le bloc 1 (5 premières diapos) et le bloc 11 (bilan) n'en ont pas.
- 6 questions d'observation (diapos 8, 13, 15, 22, 31, 32), chacune avec énoncé dit, 2 indices, 3 choix, un retour
  par choix et la solution. Pour 13 et 32, le tuteur joue le moment à l'arrêt (`gestes`) et l'élève lit la courbe ;
  pour 8, 22 et 31, la page reste arrêtée avant le résultat et l'élève raisonne à partir de l'hypothèse.
- 361 gestes de pointage et 26 cartes au centre ; 4 000 mots dits (98 par diapo en moyenne).
- Cahier : plan I, II, III, 5 définitions encadrées, 3 équations, 2 tableaux, 3 dessins (carte du voyage, trois phases
  de la glycolyse, mitochondrie légendée — celle du cours voisin, même dessin).
- **268 pistes de voix** : 41 diapositives, 8 énoncés, 35 réactions de questions, 9 retours d'association,
  1 démonstration, 4 réactions du schéma à légender, 30 pistes d'observation + 12 indices, 65 pistes de rappels,
  63 pistes de fin de bloc (non jouées aujourd'hui : dernier lot).

## Contrôles

| Contrôle | Résultat |
|---|---|
| `scripts/verifier_formules.py` | 0 relation à remettre |
| `backend/scripts/verifier_parcours.py` | rien (bon) |
| `backend/scripts/verifier_figures_cahier.py` | 0 erreur ; 1 avertissement (carte du voyage : 20 éléments, à cause des billes) |
| `scripts/audit/audit_pedagogie.py` | 0 question dans les 6 premières · 0 formule dite non écrite · 0 passage ≥ 60 mots sans geste · notions clés 13, redites 13, annoncées 13 (13 phrases différentes) · premier mot le plus fréquent « هاد » 7 % · 0 diapo qui suit avec le même premier mot · 0 début répété · 0 tournure recopiée |
| Générateur | chaque `mot` est un extrait exact, pointage dans l'ordre, aucun passage de plus de 40 mots sans geste, aucun chiffre ni symbole dans un texte dit |
| `scripts/voix/nombres_fr.py` | 0 texte avec un nombre darija à côté du français |
| `scripts/verifier_pointage.py` | pages présentes (`glycolyse-phases.html`, `bilan.html`, pages de rappel) : moments et repères trouvés ; le reste = « simulation introuvable » (pages pas encore poussées) |
| `backend/scripts/verifier_pointage_simulations.py` | 0 MOMENT, 0 IFRAME, 0 DEPART ; 1 REPERE (faux positif de lexique sur « donne A T P ») ; les GESTE ne se mesurent qu'avec les pistes (durée 0 aujourd'hui) |
| Lecteur de développement (Chromium, 1280 × 720) | les 41 diapos se chargent, le titre s'affiche, chaque diapo ouvre l'URL de sa page ; seules erreurs de console : des 404 (pas de serveur d'API en local, pages pas encore poussées) |

Captures (8 diapos, 1280 × 720 et 724 × 350) : `rf_ouverture_cours`, `rf_r1_cellule`, `rf_r2_glucose`, `rf_g0_atp`,
`rf_g1_activation`, `rf_g4_bilan`, `rf_m3_legender`, `rf_b1_bilan` — choisies parmi les pages déjà présentes ; prises
dans le dossier de travail de la session (non commitées). À refaire sur les autres pages quand elles arrivent.

## Écarts assumés

- **Longueur** : la consigne était 50 à 90 mots ; les diapos ★ (annonce + notion + image + relecture) en ont 95 à
  123, la fiche bilan 140 (neuf blocs), la fermeture 129. Minimum 73.
- **11 blocs** comme le contrat : la fermeture est dans le bloc 11 avec le bilan (le skill la met seule dans un bloc
  final).
- `rf_m1_principe` (centrifugation) est traitée en notion importante (annonce, redite, relecture) : 13 au lieu de 12.
- Rappel du glucose : la page voisine montre une bûche (`g_buche`…) ; le cours s'arrête à `g_casser` et dit l'image du
  contrat (le billet de 100 dirhams) avec une carte au centre.
- Rappel de la mitochondrie : la voix s'arrête à `spheres_pedonculees` (la suite de la page nomme Krebs et la chaîne).

## Mots douteux pour la voix (à écouter avant de générer — skill prononciation § 5)

110 mots vus moins de 3 fois par la voix (`verifier_mots.py`). Les darija rares courants ont été remplacés ; restent :

- **Termes du programme, gardés** : centrifugation, centrifugeuse, fractionnée, culot, surnageant, broyeur, foie,
  saccharose, oxymètre, agitateur, seringue, unicellulaire, champignon, amidon, marqué, dégradé, déchet, constituants,
  absorbent / absorption, rejettent, retirent, micromètre / millième, étiquettes, replis.
- **Mots découpés** (à faire écouter en priorité) : « aéro », « an » (aérobie, anaérobie), « glyco », « lyse »,
  « dé », « carboxyl ».
- **Images du contrat** : « l'essoreuse ديال la salade », « des étagères », « G P S » (écrit en lettres épelées).
- **Sigles et formules** : « l'ExAO » (dit une fois avec « l'expérience assistée par ordinateur »), « N A D H, H plus »,
  « C H trois, C O, C O O H », « C deux H cinq O H », « Pi ».
- **Énoncés en français** : écris, cite, voit-on, utilise-t-elle, devient-il, fait-elle, a-t-elle, le gain.
- **Darija en forme négative ou rare** : كتحتاجش، كينتجوش، استعملوش، كيخرجش، نعزلوهم، كنحولوه، تقسمات، عامرين.

## Ce qui reste à aligner avec les simulations

Pages présentes sur `main` au moment du rapport : `glycolyse-phases.html`, `bilan.html` (+ `demarche.js`,
`reference2.js`) — **alignées sur leurs noms réels** (fiche en neuf blocs : `respiration`, `fermentation`,
`localisation`, `devenir`, `glycolyse`, `centrifugation`, `pyruvate`, `ultrastructure`, `composition`, `lacunes`).
Aucun `RAPPORT_sims_*.md` n'était encore poussé.

Pages attendues, pilotées pour l'instant avec les noms du contrat (§ 3) : `pate.html`, `levure.html`,
`exao-levures.html` (3 vues), `equation.html` (2 vues), `deux-levures.html`, `comparer.html`, `marquage.html`,
`centrifugation.html` (2 vues), `exao-mitochondries.html`, `zoom.html`, `composition.html`, `voyage.html`.

**Noms inventés, absents du contrat (à remplacer en premier)** — `voyage.html` : moments `entree`, `glycolyse`,
`pyruvate`, `avec_o2`, `sans_o2` (étape 1) et en plus `detail_glycolyse`, `detail_mitochondrie`, `a_suivre` (étape 4) ;
repères `glucose`, `glycolyse`, `pyruvate`, `mitochondrie`, `ethanol`.

Quand les pages arrivent :
1. `python scripts/verifier_pointage.py backend/data/courses/svt_ch1_reference_consommation_mo.json` liste chaque
   moment ou repère inconnu ; corriger la balise dans `cours_diapos.py`, relancer `construire_cours.py`.
2. Vérifier que chaque `?depart=<moment>` existe et que le repère pointé est déjà dessiné à ce mot (un titre de bande
   n'apparaît qu'avec son moment : c'était le cas de `phase2` et `phase3`, corrigé).
3. Observations : les pages qui écrivent leur conclusion doivent la retenir pendant la question (diapos 8, 13, 32).
4. Rejouer le cours et refaire les captures, puis `python -I scripts/reference/dossier_inspecteur.py`.

## Voix

Aucune voix générée dans cette session. Après la pose des pistes : relancer `dossier_inspecteur.py` (les lecteurs
audio apparaissent d'eux-mêmes), puis `verifier_pointage_simulations.py` pour les gestes trop serrés.
