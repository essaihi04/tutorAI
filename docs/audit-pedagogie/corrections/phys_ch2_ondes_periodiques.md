# phys_ch2_ondes_periodiques — corrections de l'audit pédagogique (26-27/11/2026)

Cours servi : `backend/data/courses/phys_ch2_ondes_periodiques.json` (phase 1, voix inchangée).
Copie d'attente : `backend/data/courses/en_attente/phys_ch2_ondes_periodiques.json` (phase 2, texte parlé réécrit ; 70 diapos).
Pistes à générer : `docs/audit-pedagogie/voix_a_generer/phys_ch2_ondes_periodiques.json` (137 pistes). Aucune voix générée.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| Version | Diapos | Questions 6 premières | Formules dites non écrites | ≥ 60 mots sans geste | Notions clés | redites | annoncées (déclencheurs ≠) | 1er mot le plus fréquent | Suites même 1er mot | Débuts répétés | Tournures ≥ 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Avant (servi, 26/11) | 65 | 1 | 45 | 1 | 34 | 7 (21 %) | 0 (0) | « دابا » 31 % | 4 | « دابا غادي » ×8 | 1 |
| Après phase 1 (servi) | 65 | 1 (la voix de la diapo 5 finit sur « ? ») | 26 | 0 | 35 | 7 | 0 (0) | « دابا » 31 % | 4 | « دابا غادي » ×8 | 1 |
| Après phase 2 (attente) | 70 | **0** | 26 | **0** | 42 | **42 (100 %)** | **40 (95 %)**, 17 déclencheurs | « قبل » **6 %** | **0** | — | **0** |

- Les 38 phrases d'annonce placées en tête des diapos clés sont **toutes différentes** (une seule phrase par diapo) ; le compteur
  du script ne voit que le mot-déclencheur (17 différents sur les 21 qu'il connaît : « ركز معايا », « حل عينيك », « تبع معايا »…
  reviennent, chaque fois dans une phrase différente). Diapos clés non annoncées : 3 et 4 (rappels du chapitre 1).
- Les 26 « formules dites non écrites » qui restent sont fausses à l'œil : énoncés du national (la feuille du sujet est à
  l'écran : diapos 33, 35, 37, 54, 56, 58), bilan et carte (la simulation écrit chaque ligne à son `play_until`), données
  d'une question dite juste avant que le tableau de questions s'ouvre (« T = 0,02 s, que vaut N ? »), « deux fois » (pas une formule).
- Réactions des questions de diapos (celles que le script mesure, 99) : plus aucun début de 6 mots répété ≥ 4 fois.

## Phase 1 — cours servi (commit 2055147c, sur main)

1. **Blocs** : `op_o4_definition` rejoint `op_s1_b1` (la question « laquelle produit une onde progressive périodique ? »
   vient après sa définition, défaut 1 fort) ; cahier des blocs `op_s1_b1`/`op_s1_b2` réparti en conséquence.
   `op_s5_b1` listait aussi les diapos 35 et 37 (déjà dans `op_s5_b1b`) : retirées.
2. **Questions dans les 6 premières diapos** : la question de `op_o3_periodique` (le soleil) passe en exercice de fin de
   cours de la même diapo (énoncé, réactions et voix gardés). Il restait la voix qui finit sur la question : réglé en phase 2.
3. **Dit = écrit** : `op_t5_convertir` écrit ses quatre conversions chacune à sa phrase et montre la ligne du tableau des
   préfixes (`ligne_ms`, `ligne_us`, `ligne_cm`, `ligne_mm`) ; cartes du centre ajoutées ou déplacées sur leur mot dans
   `op_t3_frequence`, `op_t6_film`, `op_c3_rediger`, `op_c4_photo_datee`, `op_r3_trois_lectures`, `op_d3_justifier`,
   `op_d4_ultrasons`, `op_x1_national_2017`, `op_x2_national_2020` ; pointage sur la carte à la relecture
   (`op_c2_relation`, `op_r3c_periode`) ; pointage remis dans l'ordre de la voix (`op_t8`, `op_d4`) : `verifier_pointage.py` 3 → 0 défaut.
4. Erreurs d'écran : aucune trouvée (`verifier_formules.py` 0).

(Le 26/11 une autre session a ensuite revu le cahier des deux copies, commit d7d9e8fe ; la copie d'attente est repartie de ce cours servi.)

## Phase 2 — copie d'attente

### Ordre des notions (`ordre-des-notions/phys_ch2_ondes_periodiques.md`)
| # | Défaut | Fait |
|---|---|---|
| 1 | question de bloc après la diapo 5 (forte) | phase 1 (bloc) |
| 2 | diapo 8 : crête, creux, amplitude ensemble | crête et creux sortis de `op_o5_sinusoidale` (voix, écran, pointage) et définis au début de `op_t6_film`, juste avant de lire T entre deux crêtes |
| 3 | diapo 20 : cuve, deux vues, deux formes, hypothèses | découpée : `op_l4_rides` (cuve, deux vues, trait clair = crête, λ) puis **nouvelle** `op_l4b_formes` (circulaire / rectiligne, sans amortissement ni réflexion ; vue existante `cuve.html?vue=rectiligne`) |
| 4 | diapo 24 : changement de milieu dans la diapo de la formule | retiré de `op_c2_relation` (voix, carte, écran, cahier) ; dit dans `op_d2_invariants` (« ويلا تبدل le milieu ؟ ») avec sa carte, l'écran et le cahier |
| 5 | diapo 40 : immobilité et N = k·N_e ensemble | découpée : `op_m2_immobile` (N_e = N) puis **nouvelle** `op_m2b_condition` (N_e = N/2, N = k·N_e, la plus grande N_e, on pose la règle ; vue `stroboscope.html?vue=immobile&depart=immobilite`) |
| 6 | diapo 41 : « en phase » à l'écran pas expliqué | `op_m3_recepteurs` : « en phase على الشاشة، يعني deux courbes كيطلعو وكيهبطو مع بعضياتهم… » |
| 7 | diapo 46 : quatre mots nouveaux | découpée : `op_d1_ouverture` (incidente, ouverture large → onde diaphragmée, nouveau `play_until quatre_arcs`) puis **nouvelle** `op_d1b_diffraction` (étroite → diffraction, onde diffractée ; l'observation et ses réactions y passent ; vue `fente.html?vue=large&depart=onde_arrive`) |
| 8 | diapo 58 : « célérité nu » | « célérité v » (voix et texte français) |

Notions « dites une seule fois » : rappelées plus loin — sinusoïdale ⇒ périodique (début de `op_l1_photo`), photo datée
(`op_x1_national_2017`), onde circulaire (`op_x2_national_2020`), y_M(t) = y_S(t − τ) (`op_r4_source`, `op_x1b`),
en phase d = k·λ (`op_x3_devoir`), le n-ième point en opposition k = n − 1 (dit et écrit dans `op_p4_troisieme`).

### Notions importantes (règle 55) et tuteur (règle 56)
- Chaque diapo clé : une phrase d'annonce (38 phrases différentes), une deuxième façon de la dire (« بطريقة أخرى : … »,
  image ou exemple), et un rappel dans une diapo suivante qui l'utilise (« تفكر… », « شفنا… »).
- Débuts de voix : plus aucun « دابا » en tête (31 % avant) ; le mot le plus fréquent en tête est à 6 % ; aucune paire de
  diapos voisines avec le même premier mot. Énoncés du national : six ouvertures et six fins différentes au lieu de
  « دابا غادي نقراو… / دابا نفهمو التمرين خطوة بخطوة ». Touches humaines : « ما تخافش من هاد التمرين… », « غادي تشوف بلي
  ساهل », l'image du cœur qui bat, des deux enfants qui marchent du même pas, de la roue de la fête foraine…
- Réactions : 75 débuts changés (seulement le début ; la suite, qui nomme déjà ce qui est juste, est gardée) dans les
  réactions des questions de diapos et des rappels de compétences. Les réactions des exercices de fin de cours et des blocs
  ne sont pas dans la chaîne de voix (`scripts/voix/pistes_cours.py`) : laissées telles quelles pour ne pas perdre leur voix
  (13 commencent encore par « شوف، الجواب الصحيح »).

### Cours de référence du prof (`reference-prof/phys_ch2_ondes_periodiques.md`)
| Correction recommandée | Fait |
|---|---|
| 1. Diapo 40 en trois diapos, avec le mouvement apparent ralenti | `op_m2_immobile`, `op_m2b_condition`, **nouvelle** `op_m2c_ralenti` (vue existante `stroboscope.html?vue=ralenti` : éclairs à 19 Hz ; voix : un peu moins fréquents → les rides semblent avancer lentement, un peu plus → reculer ; « montré seulement, on ne calcule rien », comme le cadre de référence le dit) ; cahier du bloc `op_s3_b3` |
| 2. Diapo 41, en phase à l'écran | fait (défaut 6) |
| 3. Diapo 24 → 47, changement de milieu | fait (défaut 4) ; cahier des blocs `op_s3_b1` → `op_s4_b2` |
| 4. Diapo 46 : source secondaire, onde circulaire incidente, découpage | `op_d1b_diffraction` dit « source secondaire » ; **nouvelle** `op_d1c_circulaire` (vue existante `fente.html?vue=circulaire_incidente` : cercles centrés sur S → cercles centrés sur l'ouverture, source secondaire de même fréquence) ; cahier du bloc `op_s4_b2` |
| 5. Diapo 23 : 2ᵉ définition de λ, redite au bilan | `op_c1_avance` (voix, carte, écran, cahier, cahier du bloc `op_s3_b1`) ; bilan `op_b1_bilan` point 3 (voix et écran) |
| 6. Diapo 8 : crête et creux avant la diapo 14 | fait (défaut 2) |
| 7. y(t) = Ym·cos(2πt/T + φ) « à vérifier » | **laissé** : `cadre_reference_2bac_pc.json` dit seulement « reconnaître une onde progressive sinusoïdale » et `perimetre.json` ne donne aucune expression pour ce chapitre (les cos(2πt/T₀ + φ) du périmètre sont ceux du LC et du solide-ressort) : hors du cadre ici |
| 8. Question de bloc après la diapo 5 | fait (phase 1) |
| « Garder la nôtre » (a ≤ λ, k selon le cas, même état = même position et même sens) | gardé |

### Diapos ajoutées (5, toutes avec une vue de simulation existante du cours)
`op_l4b_formes` (après `op_l4_rides`), `op_m2b_condition` et `op_m2c_ralenti` (après `op_m2_immobile`),
`op_d1b_diffraction` et `op_d1c_circulaire` (après `op_d1_ouverture`). Chacune a voix, écran, cartes du centre, pointage
sur les repères et moments de sa simulation, cahier, et sa place dans le bloc et dans les compétences de la diapo d'origine.
Aucune diapo déplacée.

### Défauts laissés
- Les 26 « formules non écrites » listées plus haut (fausses à l'œil).
- 11 gestes « trop serrés » existaient avant (même liste avant / après, estimés avec le débit moyen des pistes en ligne,
  397 ms par mot, car les diapos réécrites n'ont plus de piste).
- Réactions des exercices de fin de cours et des blocs : débuts non variés (hors chaîne de voix, voir plus haut).

## Vérifications (copie d'attente et cours servi)
`verifier_formules.py` 0 ; `verifier_parcours.py` rien ; `verifier_pointage.py` 0 défaut ; `verifier_pointage_simulations.py`
aucun MOMENT / IFRAME / DEPART / REPERE nouveau (11 GESTE d'avant) ; `verifier_figures_cahier.py` 0 erreur ;
`scripts/voix/nombres_fr.py` 0 ; aucun chiffre ni symbole dans les voix réécrites.

## Mots douteux pour la voix (corpus v4, vus moins de 3 fois)
- termes du programme gardés : « ralenti », « apparent » (`op_m2c_ralenti`), « datée » (`op_x1_national_2017`),
  « source secondaire » (`op_d1b_diffraction`, `op_d1c_circulaire`) ;
- « السطور » (`op_c3_rediger`, vu 2 fois), « جنب » (« خلي كلشي على جنب », `op_p2_opposition`, vu 2 fois) ;
- annonces en français dans une phrase darija : « suis bien » (`op_m6b_deja_ecartes`), « c'est important » (`op_l3_axe`),
  « le plus important » (`op_p4_troisieme`), « partie importante » (`op_d1b_diffraction`) — à faire écouter.
Les autres mots rares nouveaux ont été remplacés (`نبنيوها`, `كيمشيها`, `نحلوه`, `مقدار`, `كيصور`, `كتسنى`, `نصححوها`…).
