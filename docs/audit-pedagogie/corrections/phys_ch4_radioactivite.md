# phys_ch4_radioactivite — corrections de l'audit pédagogique (26-27/11/2026)

Phase 1 dans le cours servi `backend/data/courses/phys_ch4_radioactivite.json` (aucun texte parlé touché).
Phase 2 dans la copie d'attente `backend/data/courses/en_attente/phys_ch4_radioactivite.json` (reconstruite depuis le
cours servi après la phase 1 ; l'ancienne copie d'attente est remplacée). Rien n'est raccourci, aucune voix générée.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| | Diapos | Questions dans les 6 premières | Formules dites non écrites | Passages ≥ 60 mots sans geste | Notions clés | redites | annoncées (phrases ≠ selon le motif) | Premier mot le plus fréquent | Suites même premier mot |
|---|---|---|---|---|---|---|---|---|---|
| Avant (servi, 26/11) | 87 | 1 | 88 | 5 | 35 | 10 (29 %) | 0 (0) | « دابا » 22 % | 9 |
| Après phase 1 (servi) | 87 | 1 (voix de la diapo 5 finit sur « ? ») | 67 | 0 | 37 | 10 | 0 | « دابا » 22 % | 9 |
| Après phase 2 (attente) | 91 | 0 | 72 | 0 | 41 | 40 (98 %) | 34 (83 %) — 17 motifs | « شفنا » 4 % | 0 |

- « Formules dites non écrites » remonte un peu en phase 2 parce que les diapos neuves et les phrases ajoutées disent
  des formules ; il en reste surtout dans les énoncés du national (texte lu tel quel) et dans des diapos où la
  simulation écrit la formule à l'étape d'avant (diapos 27, 33, 41, 46, 57, 64-66 : le geste précède la phrase de plus de
  12 mots, l'écriture existe).
- **Annonces** : les 34 phrases d'annonce sont toutes différentes, mais le script ne reconnaît que ~21 motifs
  (« ركز معايا », « حل عينيك »…) ; 17 motifs distincts sont employés, certains deux fois dans des phrases différentes
  (« ركز معايا، وغادي تشوف بلي ساهل » / « ركز معايا مزيان هنا، حيت هادي كيغلطو فيها بزاف »). Les motifs français
  « sois attentif », « concentre-toi », « écoute bien » et darija « تبعني » sont absents ou rares dans le corpus de la
  voix (verifier_mots) : écartés. La colonne « phrases ≠ » ne peut donc pas égaler 34.
- Réactions préparées : 0 début de 6 mots répété ≥ 4 fois (avant : « لا، هادي ماشي » ×19, « مزيان، الجواب ديالك » ×13).

## Phase 1 — cours servi (commit cd575b66)

1. **Questions de bloc après leur leçon** (défauts 1, 2, 14, 15 vérifiés dans le JSON, tous vrais) :
   - `ra_s1_b3` (vallée, diapos 9-10) demandait le type de désintégration (enseigné en 15-23) : remplacé par deux
     rappels déjà voisés de la compétence C2 (noyaux lourds stables N > Z ; « N = Z toujours stable ? » faux). La
     question sur le type reste au bloc `ra_s3_b1`, après la diapo 23.
   - `ra_s3_b3` (diapos 28-31) demandait l'équation différentielle (diapo 33) : remplacée par « la définition de la
     demi-vie, mot pour mot ».
   - `ra_s6_b1` demandait la datation (diapo 56) : remplacée par « après une demi-vie, l'activité est divisée par
     deux » (rappel C8_r3) ; la question de l'arbre reste en `ra_s6_b2`, après la diapo 56.
   - doublons `ra_s7_b1`, `ra_s7_b2`, `ra_s8_b1` (même question du plutonium, quatre fois) : gardée seulement après la
     diapo 74 (`ra_s7_b3`) ; ailleurs un rappel voisé sur ce que le bloc vient de faire (a₀ d'un bois vivant ; λ n'est
     pas en secondes ; 75 % désintégrés à 2t½). `ra_s6_b3` perd son rappel en doublon (passé à `ra_s6_b2`).
   - bilan `ra_s8_b3` : plus de question (étape 9 du skill cours-concentration).
   - diapo 6 (composition) passée dans le premier bloc, dont l'exercice demande la composition de ¹⁶₈O ; les diapos
     65-79 appartiennent chacune à un seul bloc, dans l'ordre (avant : 70 et 72 dans deux blocs, 77 dans aucun).
2. **Aucune question dans les 6 premières diapos** : la question de la diapo 5 (Z et A de ²³⁸₉₂U) devient un exercice de
   fin de cours (avec ses réactions voisées). La question de la diapo 45 (activité après une demi-vie) est posée à la
   diapo 47, après a(t) = a₀·e^(−λt) (défaut 12).
3. **Dit = écrit** : 25 cartes `centre` posées sur le mot exact qui dit la formule (A = Z + N, N = A − Z, dN = −λ·N·dt,
   ln(eˣ) = x, la vérification de la solution, τ = 1/λ, la conversion de t½ en secondes, ln N = ln N₀ − λ·t, N(fils),
   r = e^(λt) − 1, les résultats des nationaux 2021 N, 2022 N, 2025 N).
4. Écran : ordre des gestes de la diapo 22, unités des axes sans dimension (Z, A, ln N) dans les dessins du cahier.

## Phase 2 — copie d'attente

### Diapos ajoutées (4) et coupées
| Diapo | Pourquoi | Visuel |
|---|---|---|
| `ra_n2b_nucleons` « Dans le noyau : protons et neutrons » | diapo 3 coupée en deux (défaut 6) : l'atome, puis les nucléons | `noyau.html?vue=atome&depart=atome` (zoom) |
| `ra_n6b_nucleide` « Nucléide et élément chimique » | diapo 7 coupée (défaut 7, recommandation 3 du prof) : isotopes seuls, puis nucléide, élément chimique et « ion » | `noyau.html?vue=isotopes&depart=fin` |
| `ra_r2c_particules` « Écrire les particules avec A et Z » | avant Soddy (défaut 4, recommandation 4 du prof) : ¹₁p, ¹₀n, ⁰₋₁e, ⁰₁e, ⁴₂He | **carte simple** (aucune figure du cours ne montre les cinq particules) : cinq cartes `centre` écrites à leur mot |
| `ra_l2b_derivee` « Rappel : la dérivée, une vitesse de variation » | avant dN = −λ·N·dt (défauts 5 et 10, recommandation 1 du prof) : dN/dt, pente de la tangente, « équation différentielle » | `courbe.html?courbe=N&depart=t_demi`, arrêt sur la tangente |

La règle (e^(kt))′ = k·e^(kt) est dite et écrite à la diapo 36, juste avant son usage. Les blocs, les compétences
(C1, C4, C6) et les lignes du cahier suivent : une ligne ajoutée à chaque endroit dans le cahier revu le 26/11 (élément chimique, notation des particules, rappel de la dérivée, 63 % à τ, choix du nucléide), sans renumérotation.

### Ordre des notions — défauts traités
- 1, 2, 12, 14, 15 : phase 1. 4, 5, 6, 7, 10 : diapos ci-dessus.
- 3 (« instable / radioactif » avant la définition) : **solution du prof retenue** (recommandation 2) — la diapo 9 dit
  « instable, on dit aussi radioactif : il va se transformer, on voit comment juste après » ; la diapo 11 rappelle le
  carbone 14 instable. Les diapos 11-13 ne sont pas déplacées.
- 8 (Soddy abstrait) : exemple du polonium dit et écrit dans la diapo 14 (carte centre) ; la remarque « on conserve la
  charge, pas les protons » passe à la diapo 16 (voix et écran).
- 9 (puissances de dix après la diapo 3) : les ordres de grandeur 10⁻²⁷ kg et 10⁻¹⁹ C sont retirés de l'écran de la
  diapo 3 ; le rappel reste à la diapo 28, avant le premier calcul (10⁹ ans de la diapo 31 vient après).
- 11 : (e^(ln2))ⁿ = 2ⁿ dit et écrit à la diapo 42, après le tableau N₀/2, N₀/4, N₀/8.
- 13 : après la lecture des énoncés 2024 R, 2020 R, 2022 R, 2022 N, 2025 N : « les masses en u et les MeV, on les verra
  au chapitre suivant ».
- La voix de la diapo 5 ne finit plus sur une question : elle répond elle-même (Z = 92, A = 238).

### Notions importantes (règle 55)
34 diapos clés sur 41 commencent par une annonce, chaque fois une phrase différente (« حل عينيك على السبورة، هنا كاين
المهم », « سمعني مزيان، هاد الجوج كلمات… », « هنا بالضبط فين كيغلطو بزاف ديال التلاميذ »…). 40 ont une deuxième façon de
le dire (image ou autre point de vue : la vallée comme une route, le verre d'eau qu'on ne remplit plus, « nucléon = une
des particules du noyau »…). Rappels plus loin : nucléons (diapo 4), Z et A (7), isotopes (10), particule α (15),
positon (17), demi-vie (31), proportion (33), dérivée (33, 39), équation différentielle (36), tangente (39), question
d'ouverture sur l'âge du bois (56).

### Tuteur humain (règle 56)
- Débuts de voix : 0 diapo qui suit avec le même premier mot (9 avant) ; aucun premier mot sur plus de 4 % des
  diapos (« دابا » 22 % avant). Les 12 énoncés du national ne commencent plus tous par « دابا غادي نقراو l'énoncé… »,
  les corrections plus toutes par « السؤال ».
- 112 réactions préparées (diapos, blocs, rappels) : leur première phrase répétée (« مزيان! », « لا، هادي ماشي هي. »…)
  est remplacée par une phrase prise dans une liste variée (juste : « بالضبط! », « صافي، فهمتيها. »… ; fausse :
  « هادي غلطة كيديرها بزاف ديال التلاميذ، عادي. », « لا، ولكن فهمت علاش ختاريتي هادي. »…), le reste de la réaction
  (qui nomme ce qui est juste) est gardé. Une réaction qui parlait de « l'élève » à la 3ᵉ personne dit « عرفتي ».
- Touches humaines par bloc : « شوف هاد الحاجة، غريبة شوية » (famille), « أنا عارف أن هادي كتبان صعيبة فاللول »
  (équation différentielle), « عادي تغلط فيها مرة » (pourcentages), « برافو، كملتي تمرين كامل » (2021 N), « هادا آخر
  حساب فهاد الدرس، برافو عليك » (2025 N), l'image du stade et du pois chiche gardée.

### Symboles mal lus et erreurs de voix corrigées
- « N A » (risque « newton ampère », comme au ch5) → « le nombre d'Avogadro » dans toutes les voix, réactions,
  démonstrations et énoncés (diapos 49-51, bloc s5_b3, exercice de fin de la diapo 51).
- « la masse m » au lieu de « m » seul devant « gramme » (diapo 51).
- Énoncé de la diapo 21 : la voix annonçait quatre choix (A haut, B bas, C gauche, D droite) pour trois cartes
  (gauche, droite, ne bouge pas) — corrigé.
- Énoncé de la diapo 38 : « نزو zéro » → « N zéro ».
- Nombres darija collés au français : « جوج noyaux », « جوج nucléides » → « deux » ; « quatre الفوق » (diapo 15)
  supprimé ; `nombres_fr.py` : 0 reste.

### Défauts laissés
- `verifier_pointage.py` : 3 repères « inconnus » de `pourcentages.html` (ligne_trente…) — faux positif, le repère est
  construit dynamiquement (`c.repere('ligne_' + id …)`).
- `verifier_pointage_simulations.py` sur la copie d'attente : des « gestes trop serrés » sur les diapos sans piste
  (audio retiré) : le script suppose une seconde par geste sans durée réelle ; à revoir quand les voix seront posées.
- `speech_text.fr` n'est pas réécrit pour les diapos dont seule la voix darija change (les nouvelles diapos ont leur fr).
- Tournures recopiées : « un u égale neuf cent trente et un… » vient des énoncés lus mot pour mot.

## Cours de référence du prof (`reference-prof/phys_ch4_radioactivite.md`)
Ajouté (tout vérifié dans `cadre_reference_2bac_pc.json` RA1-RA10 et `perimetre.json` : rien hors du cadre) :
1. rappel de la dérivée avant la loi (diapo neuve) ; 2. « instable, on dit aussi radioactif » à la diapo 9 au lieu de
déplacer 11-13 ; 3. diapo 7 coupée (isotopes, puis nucléide et élément chimique) ; 4. notation des particules (diapo
neuve) ; 5. exemple du polonium dans la diapo 14 ; 6. « spontanée et aléatoire » dans la définition relue (diapo 11,
cahier) ; 7. diapo 37 : λ·t est l'exposant de l'exponentielle, donc sans unité (voix et écran) ; 8. diapo 40 : « à τ,
63 % des noyaux sont désintégrés » (voix, carte, écran, cahier) ; 9. diapo 56 : le carbone 14 se forme sans arrêt dans
la haute atmosphère et entre dans le dioxyde de carbone ; diapo 57 et bilan (diapo 85) : carbone 14 pour le bois, nucléide
de très grande t½ (²³⁸U) pour une roche ; 10. diapo 23 : « au-dessus » suppose N en ordonnée, sinon raisonner sur « trop
de neutrons / trop de protons » ; 11. corrections de l'audit gardées.
Laissé : ordres de grandeur d'activités (eau, lait, corps humain) — facultatif chez le prof, et des valeurs chiffrées
non sourcées ; la curie — pas dans le cadre (seul le becquerel y est) ; τ avant t½ — notre ordre est gardé (le prof le
juge meilleur chez nous).

## Pistes à générer
`docs/audit-pedagogie/voix_a_generer/phys_ch4_radioactivite.json` (format de `scripts/voix/pistes_changees.py`) :
**165 pistes** — 70 diapositives (dont 4 nouvelles), 94 réactions ou énoncés, 1 démonstration.

## Mots douteux pour la voix (verifier_mots, pistes à générer)
Nouveaux mots ou tournures à écouter avant génération : « suis bien » (annonce, diapo 8), « partie importante »,
« c'est important », « le plus important » (annonces en français), « positon » (rare, terme du programme),
« nucléide(s) », « le dioxyde de carbone », « الفوقاني », « كاس », « بلاصة فالرسم », « غريبة ». Les autres mots rares
signalés (neutron, vallée, plomb, plutonium, xénon, électron-volts, termes des énoncés) étaient déjà dans les pistes
servies.
