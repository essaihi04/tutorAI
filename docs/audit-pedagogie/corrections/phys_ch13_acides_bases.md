# phys_ch13_acides_bases — corrections de l'audit pédagogique (26-27/11/2026)

Cours servi : `backend/data/courses/phys_ch13_acides_bases.json` (phase 1 : aucun texte parlé changé).
Copie d'attente : `backend/data/courses/en_attente/phys_ch13_acides_bases.json` (phase 2 : texte parlé ; 83 diapos).
Pistes à générer : `docs/audit-pedagogie/voix_a_generer/phys_ch13_acides_bases.json`.
La phase 2 a été refaite sur le cours servi qui contient la phase 1 et les changements de l'amont (revue des cahiers,
repères de synchronisation) : les cahiers et les repères de l'amont sont gardés.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| Version | Diapos | Questions dans les 6 premières | Formules dites non écrites | Passages ≥ 60 mots sans geste | Notions clés | redites | annoncées (mots-clés ≠) | Premier mot le plus fréquent | Suites même premier mot | Débuts répétés |
|---|---|---|---|---|---|---|---|---|---|---|
| Avant (servi, 26/11) | 78 | 1 | 97 | 11 | 31 | 13 | 0 (0) | « دابا » 26 % | 7 | « دابا غادي » ×9, « le national » ×7 |
| Servi après phase 1 | 78 | 0 | 91 | 7 | 35 | 13 | 0 (0) | « دابا » 26 % | 7 | idem |
| Attente (phase 2) | 83 | 0 | 86 | 3 | 38 | 38 (100 %) | 36 (95 %) — 13 mots-clés | « هاد » 5 % | 0 | — |

« annoncées (phrases ≠) » : la colonne de l'audit compte les **mots-clés** distincts de la regex `ATTENTION`
(« ركز معايا », « تبع معايا », « حل عينيك »… une quinzaine au plus), pas les phrases. Compté phrase par phrase
(petit script sur la phrase qui contient le mot-clé) : **36 annonces, 36 phrases entières toutes différentes**.
Les deux notions clés sans annonce : `ab_e3_indicateur` (application) et `ab_d1_montage` (montage), les deux redites.

Réactions préparées : 114 ; premiers mots avant « لا » 33, « شوف » 31, « مزيان » 31 ; après « مزيان » 17, « لا » 14,
« ماشي » 13, puis 15 débuts différents ; aucune suite de 6 mots répétée ≥ 4 fois.

Formules « dites non écrites » (86) : presque toutes sont écrites par la simulation au moment joué (`motif` des
`ETAPES` d'`acides-bases-tableau/*.html`) ou lues sur la feuille d'examen (diapos d'énoncé) ; l'audit ne voit que les
`mot` à moins de 12 mots. Les vrais manques ont été corrigés (liste plus bas).

## Phase 1 (cours servi, voix inchangée)

1. Questions de bloc (vérifiées dans le JSON) :
   - `ab_b02` (Ke avant la diapo qui le définit) : retiré, doublon de `ab_b03` placé après la leçon. **Confirmé.**
   - `ab_b05` (τ d'une base avant la diapo 16) : retiré, doublon de `ab_b06`. **Confirmé.**
   - `ab_b07` : l'exercice (pKa par Ka = Ke/Qr,éq, enseigné en 22) passe dans `ab_b08` ; `ab_b07` garde « écris Ka ».
     `ab_b08` perd ses questions (comparer aussi les bases, enseigné en 25 ; doublon de `ab_b09`). **Confirmé.**
   - `ab_b12` (réaction de dosage, enseignée en 41-42) : ses questions passent dans `ab_b13` (dont les questions étaient
     le doublon de `ab_b14`). **Confirmé.**
   - `ab_b17` : doublon de `ab_b16`, retiré (garder le premier placé après la leçon).
2. Question de la diapo 2 (−log 10⁻⁵) déplacée, avec ses réactions (et leurs voix), vers `ab_w3b_neutre` (qui
   passe par −log). 0 question dans les 6 premières diapos.
3. Dit = écrit : cartes `centre` ajoutées ou précisées : conversion V et m = ρ·V (`ab_w1b_limitee`), étape
   −log Ke = −2·log[H₃O⁺] (`ab_w3b_neutre`), calcul des deux τ (`ab_c1_acides`), rapports 1/10 et 10 de la zone de virage
   (`ab_i2b_regle`), V_total = V_A + V_B (`ab_d2_reaction`), n(AH)₀ et n(HO⁻) de la demi-équivalence (`ab_e2_demi`) ;
   gestes de baguette sur un repère déjà écrit dans les longs passages (`ab_r1b_eau_ph`, `ab_p1_relation`,
   `ab_a5_eau`, `ab_b3_national`, `ab_e5b_pourquoi`).
4. Écran : `ab_cr_carte` démarre figée (`reset`) ; unités vides des axes pH, % des figures de cahier (l'amont a
   ensuite refait ces figures) ; `observation.apres_mot` de `ab_w2a_mesures` ne se trouvait pas dans la voix
   (« … colonne. » au lieu de « … colonne، ») : corrigé ; carte « Base + eau : K = Ke/Ka » sur `ab_a4_ammonium`
   (référence du prof, correction 9 ; ajoutée le 27/11, sans voix).

## Phase 2 (copie d'attente)

### Ordre des notions (règle 52) — `ordre-des-notions/phys_ch13_acides_bases.md`
| # | Défaut | Fait |
|---|---|---|
| 1, 2, 3, 5 | questions de bloc trop tôt | phase 1 |
| 4 | Ke « constante d'équilibre » avant le rappel de K | `ab_r2_constante` avancée en 5ᵉ diapo (bloc `ab_b01`, ses lignes de cahier aussi) ; Ke la rappelle |
| 6 | fort / faible jamais définis | définis par la réaction totale ou limitée avec l'eau en 26 (acides, puis Ka entre deux faibles) et 27 (bases), dits dès l'ammoniac (17), redits en 50 (`ab_e1_phe`) |
| 7 | soude utilisée avant d'être présentée | nouvelle diapo `ab_r3_soude` avant les mesures (vue `soude` de la simulation du cours) |
| 8 | rappel de la tangente après son usage | `ab_z2_pente` placée avant `ab_d5_tangentes` (bloc et cahier) |
| 9 | mole, n = m/M, ρ non rappelés | nouvelle diapo `ab_r0_mole` avant le calcul de τ (vue `mole` de la simulation du cours) |
| 10 | BBT avant d'être expliqué | porte d'entrée sans BBT (voir référence du prof) ; les trois béchers et le BBT restent en `ab_i1_indicateur` |
| 11 | τ = % de A⁻ jamais montré | phrase et carte ajoutées dans `ab_p4_national` |
| 12 | dilution non rappelée | nouvelle diapo `ab_r4_dilution` avant le national 2023 R (vue `dilution` de la simulation du cours) |
| 13 | C_m ajoutée à une diapo chargée | nouvelle diapo `ab_e4b_massique` (**carte simple** : aucune figure du cours ne la montre) |

### Diapos ajoutées / déplacées
- Ajoutées : `ab_r0_mole`, `ab_r3_soude`, `ab_r4_dilution` (vues existantes de `acides-bases-tableau/`),
  `ab_e4b_massique` et `ab_d3b_totale` (cartes simples, `visual.kind: none`).
- Déplacées : `ab_r2_constante` (13 → 5), `ab_z2_pente` (45 → avant `ab_d5_tangentes`).

### Notions importantes (règle 55)
Annonce avant chaque notion clé (36 phrases toutes différentes), deuxième façon de la dire dans la diapo (38/38),
rappels plus loin (« تفكر… ») : K rappelée dans Ke et Ka, la mole dans τ de l'eau, la soude dans les mesures et
le pH de la soude, les règles du log dans pH = pKe/2, la relation pH = pKa + log dans la zone de virage et la
demi-équivalence, la tangente dans la dérivée, la zone de virage dans le choix de l'indicateur, fort/faible dans pH_E,
la dilution dans le national 2023 R.

### Tuteur humain (règle 56)
Débuts de voix tous réécrits là où ils se répétaient (« دابا » 26 % → aucun mot au-dessus de 5 %, 0 suite) ; les
neuf diapos d'énoncé et les sept corrigés de national commencent chacun autrement ; liens avec la diapo d'avant ;
touches humaines (surprise devant l'eau pure qui conduit, « كيغلطو فيها بزاف، عادي », encouragement en fin d'exercice,
« علاش كنديرو le dosage ؟ ») ; réactions : débuts variés qui gardent ce qui est juste dans le choix.

### Symboles et mots mal lus corrigés (voix)
« pH », « pKa », « Ka », « Ke », « pH-mètre », « BBT » écrits collés → « p H », « p K a », « K a », « K e »,
« p H mètre », « B B T » ; nombres en chiffres dans des réactions (« 6,10 », « 1,26 », « 0,80 », « 24 pour cent ») ;
« trois virgule nine » (anglais), « quatre virgule sept neuf », « un virgule seize » (faux : 1,6) ; arabizi « m3a »,
« dyal », « فوا » ; « بارakallah » ; « [HO moins] » ; « la croisement », « nous divisons » ; « البروم تيمول بلو » ;
« تذكر الراجل » ; « الcours », « فالburette »… ; `ab_x4_indicateur` disait « le rouge de crésol zéro » (→ jaune) ;
fermeture « pH égale pKa » (→ p H, p K a).

### Défauts laissés (et pourquoi)
- Questions des blocs `ab_b02`, `ab_b05`, `ab_b12`, `ab_b17` : ces blocs n'ont plus de question « À toi » (doublons
  retirés ; aucune nouvelle question écrite, elle demanderait une voix d'énoncé non prévue).
- `IFRAME` (même URL de simulation que la diapo d'avant) : 4 restent (5 avant : la mole a séparé les deux diapos
  d'autoprotolyse) ; les séparer demanderait une vue nouvelle de simulation, hors cadre.
- `DEPART demarrer=start` sur les diapos du cours : façon de faire du cours entier, non touchée.
- `GESTE` (gestes trop serrés) : 34 sur le servi ; ~600 sur la copie d'attente, parce que les diapos réécrites n'ont
  plus de piste (durée estimée) ; à revoir après génération des voix.
- 3 passages de 60-61 mots sans geste (`ab_w1b_limitee`, `ab_a5_eau`, `ab_n1_2016n`) : à la limite.
- Défaut « pH = pKa + log cité dès la diapo 20 » de la référence : noté « rien d'obligatoire », non fait.

## Cours de référence du prof (`reference-prof/phys_ch13_acides_bases.md`)
| Correction recommandée | Fait |
|---|---|
| 1. Base titrée : extremum de dpH/dV = minimum (diapo 50) | voix + carte + ligne de cahier dans `ab_e4_base` |
| 2. Fort / faible par la réaction totale ou limitée avec l'eau (24-25), redit en 47 | `ab_c1_acides`, `ab_c2_bases` (+ cartes), `ab_e1_phe` ; formulation du programme, pas celle du prof |
| 3. Porte d'entrée : l'eau pure, pH 7, conduit un peu : d'où viennent ses ions ? sans BBT | `ab_o2_trois_ph` réécrite (le geste BBT retiré) ; `ab_i1_indicateur` reprend les trois béchers |
| 4. Rappel de K avant 5, soude avant 8 | fait (défauts 4 et 7) |
| 5. Diapo « la réaction de titrage est totale, vérifiée sur la courbe » après 42 | nouvelle diapo `ab_d3b_totale` (V_B = 10,0 mL, pH 4,80 → [HO⁻] = 6,3·10⁻¹⁰ mol/L → τ ≈ 1), carte simple ; `ab_d2_reaction` y renvoie |
| 6. Annoncer les trois repérages de l'équivalence (42) | voix + carte de `ab_d3_equivalence`, ligne de cahier |
| 7. Pour chaque zone de la courbe : ce qui est en excès, acide ou basique (43) | `ab_d4_courbe` |
| 8. Tangente rappelée avant la méthode | fait (défaut 8) |
| 9. K(base + eau) = Ke/Ka à l'écran (22) ; Ke dans toute solution (9) | carte sur `ab_a4_ammonium` (servi et attente) ; l'écran de `ab_w2_ke` le disait déjà (« Vrai dans TOUTE solution aqueuse ») |

## Pistes à générer
179 pistes (73 diapositives, 106 réactions ou énoncés ; 5 nouvelles diapos) dans
`docs/audit-pedagogie/voix_a_generer/phys_ch13_acides_bases.json`. `lister_voix_attente.py` liste en plus les pistes
des blocs jamais mises en voix (fin de bloc non jouée, `FIN_DE_BLOC_COMPLETE = False`) : non ajoutées.

## Mots douteux pour la voix (`verifier_mots.py` sur la copie, mots nouveaux par rapport au servi)
douzaine, entités, millième (rappel de la mole), fiole, jaugée, pipette, soluté (rappel de la dilution) — termes du
programme déjà dits dans ch10 et ch11 ; « غريبة », « كيغلطو » (phrases de la banque) ; aussi à écouter les tournures
nouvelles « كتجي بزاف فle national », « تبع معايا ».

## Vérifications (copie d'attente)
`verifier_formules` 0 ; `verifier_parcours` rien ; `verifier_pointage` 0 défaut ; `verifier_figures_cahier`
0 erreur, 0 avertissement ; `verifier_pointage_simulations` : aucun MOMENT, REPERE inconnu ou PROCESSUS nouveau
(remarques de lexique identiques au servi), IFRAME 4 ; nombres français collés au darija : 0.
