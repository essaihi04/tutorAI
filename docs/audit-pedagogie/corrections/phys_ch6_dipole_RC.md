# phys_ch6_dipole_RC — corrections de l'audit pédagogique (26-27/11/2026)

Phase 1 dans le cours servi (`backend/data/courses/phys_ch6_dipole_RC.json`, aucun texte parlé changé) ; phase 2 dans la
copie d'attente (`backend/data/courses/en_attente/phys_ch6_dipole_RC.json`, refaite à partir du cours servi après la phase 1).
Rien n'est raccourci : 86 → 89 diapos. Aucune voix générée.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| | Avant | Après phase 1 (servi) | Après phase 2 (attente) |
|---|---|---|---|
| Diapos | 86 | 86 | 89 |
| Questions dans les 6 premières | 2 | 0 | 0 |
| Formules dites non écrites | 95 | 26 | 26 |
| Passages ≥ 60 mots sans geste | 6 | 0 | 0 |
| Notions clés / redites | 34 / 11 | 39 / 11 | 41 / 41 (100 %) |
| Notions clés annoncées | 0 | 0 | 41 (100 %) — 41 phrases d'annonce toutes différentes ; le script compte 14 « motifs » distincts (il compte le motif reconnu, pas la phrase) |
| Premier mot le plus fréquent | « دابا » 23 % | 23 % | « قبل » 7 % |
| Diapos qui suivent avec le même premier mot | 11 | 11 | 0 |
| Réactions : début le plus fréquent (2 mots) | « مزيان، الجواب » ×19 | — | « ها هو » / « قريب، ولكن » ×11 |

Les 26 « formules non écrites » restantes : 22 dans les énoncés du national lus sur la feuille du sujet (le texte lu est
à l'écran : faux défaut), 2 à la diapo `rc_np0_sujet` (relecture des données, écrites par la vue « sujet »), 1 à
`rc_s4_condition` (ligne de remplacement écrite par la figure `fig_condition_initiale` au moment « equation »), 1 à
`rc_np6_pourcent` (consigne « calcule 0,63·E » : l'écrire donnerait la réponse).

## Phase 1 (commit 8972d18d)

- Questions de bloc déplacées après la diapo qui enseigne leur notion : 1/RC (→ `rc_s2_b2b`, après la diapo 30) ;
  équation de la décharge ↔ équation de q échangées entre `rc_s2_b3` et `rc_s4_b3` ; u_C à τ en décharge et l'exercice
  « décharge, u_C(τ) » → `rc_s3_b4` (après les 37 %) ; i(t) de la décharge et l'énergie → `rc_s4_b2b` (après la diapo 63).
  Doublon retiré : l'exercice de `rc_s3_b1` était celui de la diapo 40 (même bloc) ; il reste en `rc_s4_b3`.
- Questions des diapos 4 et 6 → `exercices_fin_de_cours` (réactions gardées avec leur voix).
- Dit = écrit : ~60 cartes `centre` et pointages `cible: centre:N` posés sur les mots exacts (relectures, données,
  lignes de calcul), toutes les diapos de plus de 60 mots sans geste ont maintenant un geste.
- Écran : diapo 10 « (q = 0, …) » → « (i = 0, …) » (q n'est expliquée qu'après) ; diapo 57 : i(t) « démontré à la
  diapo suivante » retiré ; légende du cahier « 4 V / 4 s » en fraction.
- Laissé : défaut 17 (exercice 2022 N « R puis C » après la diapo 47) — i(0) = E/R (diapo 23) et τ = RC (diapo 38) sont
  déjà enseignés : la question est faisable là où elle est.

## Phase 2 — ordre des notions (`ordre-des-notions/phys_ch6_dipole_RC.md`)

| # | Défaut | Fait |
|---|---|---|
| 1 | additivité avec C avant le condensateur | `rc_c1_plaques` placée avant `rc_rp4_additivite` (blocs, lignes du cahier et « retrouver » suivis) |
| 2 | puissances de dix avant la capacité, sans pico | `rc_rp5_puissances` placée juste avant `rc_c4_capacite`, « capacités » retiré de la voix, pico ajouté (voix, carte, cahier) |
| 3 | coulomb jamais dit | diapo 3 : q en coulomb, i = q/t, 1 A = 1 C/s (voix + carte + écran) |
| 4 | « chargé » avant l'explication | diapo 10 : « on dit chargé ; pourquoi, on le voit juste après » |
| 5 | « i < 0 en décharge » trop tôt | résolu comme le prof : nouvelle diapo `rc_c2b_lampe` (décharge vue sur une lampe) avant ; la phrase de la diapo 14 est gardée et renvoie à la lampe |
| 6 | R_eq jamais rappelé | diapo 17 : R_eq = R₁ + R₂ avec un exemple (voix + carte) |
| 7 (forte) | acquisition : cinq notions d'un bloc | coupée en deux : `rc_m2_acquisition` (flèches, ce qu'est le système d'acquisition, entrée Y, masse, sans la règle) puis nouvelle `rc_m2b_brancher` (règle « tête de flèche → entrée Y », la question 2017 R) |
| 8 | continuité de u_C noyée dans les régimes | nouvelle diapo `rc_m4b_continuite` (vue `continuite.html?vue=enchaine`, moment « charge ») ; rappel à la diapo de la bascule |
| 9 | question sur u_C + RC·du_C/dt = E avant l'équation | la question porte sur f + 4f′ = 2 (énoncé, options, 5 réactions réécrites) |
| 10 | 1/RC sans unité | diapo 30 : « 1/RC en s⁻¹ » (voix + carte) |
| 11 | dérivée d'une constante / d'une somme | ajoutée au rappel de la dérivée (diapo 13), rappelée à la diapo 32 |
| 13 | τ sans sens dans le rappel de l'exponentielle | une phrase : τ est le RC devant la dérivée, une durée fixe (pas de réécriture en e^(−t) : la simulation affiche τ) |
| 14 | vérifier après trouver | `rc_s5_verifier` placée avant `rc_s2_remplacer` |
| 21 | puissance jamais rappelée | p = u·i (watt) dit et écrit avant la formule de l'énergie |
| 22 | énoncés : chapitres suivants | phrase « bobine, RL, AM : cours suivants » (2023 R), « la bobine plus tard » (2019 N) ; l'ordre de lecture des énoncés n'est pas changé (déplacer 13 diapos d'énoncé changerait tous les blocs « national » : laissé) |
| 12, 15-20 | | phase 1 |

Notions dites une seule fois, maintenant rappelées plus loin : entrée Y (diapo de la charge), continuité de u_C (bascule),
équations de u_R et i (tableau des huit équations), dimension de τ (influence de R), parallèle (q = f(u)), 5τ (calcul de
l'énergie), i = pente (décharge). Pas de rappel ajouté pour le générateur de courant ni pour du_C/dt = f(u_C) (aucune diapo
suivante ne les emploie avant le bilan).

## Phase 2 — règles 55 et 56

- 41 notions clés : chacune annoncée par une phrase différente juste avant (banque de phrases et nouvelles du même
  style), redite autrement dans la diapo (« بطريقة أخرى », « بمعنى آخر », « بكلمة أخرى » suivis d'une vraie deuxième façon).
- Débuts de voix : liens avec la diapo d'avant (« عرفنا… », « شفنا… », « تفكر… ») ; les 9 suites d'énoncé ne commencent
  plus toutes par « نفس التمرين ديال الامتحان الوطني » et finissent par des phrases différentes ; « خود الوقت ديالك، ومن
  بعد جاوب » varié sur les 8 étapes du 2022 N.
- Réactions : 280 réactions (diapos, réserve de fin de cours, rappels des compétences) ont un premier mot varié (juste :
  « بالضبط », « زوين », « تبارك الله »… ; faux : « قريب، ولكن », « فهمت علاش ختاريتي هادا », « التفكير ديالك مزيان »…).
  Ce changement d'ouverture est mécanique : la suite de la réaction (ce qui est juste dans le choix) est celle d'avant ;
  seules les 5 réactions de la question f + 4f′ = 2 sont entièrement nouvelles. À écouter.

## Cours de référence du prof (`reference-prof/phys_ch6_dipole_RC.md`)

| Correction recommandée | Appliqué / laissé |
|---|---|
| 1. Acquisition (entrée Y, masse) avant la diapo 21 | appliqué : diapo 21 coupée, l'acquisition enseignée seule, la règle sur la diapo suivante |
| 2. Coulomb, i = q/t (diapo 3) | appliqué |
| 3. Décharge qualitative ; l'isolant coupe le circuit ; « i < 0 » gardé | appliqué : nouvelle diapo `rc_c2b_lampe` (vue `energie.html?vue=lampe`, une lampe et non une DEL : c'est ce que montre la simulation) ; phrase « l'isolant coupe le circuit » à la diapo des aiguilles ; diapo 14 garde i < 0 et renvoie à la lampe |
| 4. Additivité après le condensateur | appliqué (déplacement) |
| 5. Intérêt de la série + R_eq | appliqué (voix + carte) |
| 6. « environ 5τ » dès les régimes | appliqué (une phrase, τ annoncé comme une durée à venir) |
| 7. p = u·i avant l'énergie | appliqué (dit et écrit avant E_e) ; la dérivée d'un carré reste citée sans rappel (laissé, signalé) |
| 8. Le flash comme usage | appliqué dans la diapo de la lampe (pas à la diapo 2 : la voix de la carte reste) |
| 9. τ sur u_C en décharge (37 %, tangente ∩ axe) | appliqué à la diapo 61 (voix + carte) |
| 10. Garder les corrections des questions trop tôt | gardées (phase 1) |

Rien hors du cadre (pas de régime critique, pas de filtres).

## Diapos ajoutées ou déplacées

- Ajoutées (sans `audio`) : `rc_c2b_lampe` (après les aiguilles), `rc_m2b_brancher` (après l'acquisition, URL
  `circuit-rc.html?etape=regle&vue=montage` pour recharger la scène), `rc_m4b_continuite` (après les régimes).
- Déplacées : `rc_c1_plaques` avant l'additivité, `rc_rp5_puissances` avant q = C·u_C, `rc_s5_verifier` avant
  `rc_s2_remplacer`. Blocs (`slide_ids`, lignes du cahier, deux « retrouver ») mis à jour en conséquence.
- Effet de bord utile : l'avertissement IFRAME des diapos 10-11 (même URL de suite) disparaît.

## Vérifications

- `verifier_formules` 0 ; `verifier_parcours` rien ; `verifier_figures_cahier` 0 erreur.
- `verifier_pointage` : mêmes défauts qu'avant, plus `rc_m2b_brancher` « moment inconnu fleches / acquisition » — faux
  défaut déjà présent sur `rc_m2_acquisition` (le lecteur statique ne lit pas les `ETAPES` de `circuit-rc.html`).
- `verifier_pointage_simulations --ecarts` : les « GESTE trop serrés » viennent des diapos sans piste (durée inconnue
  tant que la voix n'est pas générée) ; les nouvelles diapos ont « DEPART demarrer=start » comme leurs voisines.
- `nombres_fr` : 0 nombre darija à côté du français.

## Pistes à générer

`docs/audit-pedagogie/voix_a_generer/phys_ch6_dipole_RC.json` : 222 pistes — 73 diapositives, 149 réactions ou énoncés
(dont les énoncés dits des questions changées) ; les réactions des blocs ne sont pas mises en voix (FIN_DE_BLOC_COMPLETE).

## Mots douteux pour la voix (`verifier_mots`, nouveaux par rapport au cours servi)

Termes gardés exprès : « flash », « watt ». Formes darija rares (vues 0-2 fois), à écouter : كتفهمنا، يقدروش، خزن،
كتطفا، كيخزنو، شعلات، والفايدة، كيتعمر، كيقارن، وكيرسمها، يورينا، كيدوم، كتحل، نقزات، يقدرش، الحيلة، جنب،
كنخليوهم، تخدمك، بوحدنا، كيطيح / كتطيح / كيطيحو، تولف، كترسم، كيطلبوهم / كيطلبوها، كيتعطل، نحلوه، غريبة،
كيتلفو، تزربش، كيكملو، وكتقاس، روبيني. Remplacés avant écriture : « تبعني », « ما ضاعش », « ما عليش », « غلطة »,
« أداة », « كنخويوه », « كيتربط », « كيصب ».
