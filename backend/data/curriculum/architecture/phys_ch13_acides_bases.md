# Architecture — Transformations liées aux réactions acide-base (`phys_ch13_acides_bases`)

Logique refaite le 18 novembre 2026, avec la skill `logique-de-cours`. Elle est appliquée dans `backend/data/courses/en_attente/phys_ch13_acides_bases.json`. Le cours en ligne n'a pas été touché.

J'ai ajouté une vue de simulation : `frontend/public/media/simulations/chimie/acides-bases-tableau/eau.html?vue=ke_mesures`. Les autres vues de la page ne changent pas.

Les pistes à mettre en voix sont dans `phys_ch13_acides_bases_voix.json` : 126 pistes (64 de la logique, 62 de la 2ᵉ passe, § 6).

## 1. Sources

### Les profs

Ce chapitre n'a pas de fichier d'exploration. J'ai relevé le plan de 4 cours complets en ligne :

1. **N. Naceiri Mrabti**, livre 2BAC BIOF, p. 159-175.
   - Ordre : autoprotolyse et Ke, avec l'activité « pH de l'eau pure = 7 → [H₃O⁺], tableau, τ, Ke ».
   - Puis : Ka, pKa, pH = pKa + log ; K d'une réaction acide-base ; comparaison des acides puis des bases ; prédominance et distribution ; indicateurs colorés (BBT).
   - Puis le titrage : méthodes, équivalence, montage pH-métrique, tangentes, dérivée, choix de l'indicateur, τ du titrage ≈ 1.
2. **El Goufifa**, AlloSchool, séance 15.
   - Ordre : introduction (l'aquarium), autoprotolyse, Ke, Ka, pH–pKa, K acide-base, comparaison des acides puis des bases, prédominance, distribution, indicateurs.
   - Pas de dosage : il est à part.
3. **Fiche pédagogique 2BAC PC**, 5 h.
   - Ordre : autoprotolyse, Ke, Ka, pH–pKa, K acide-base, prédominance, distribution.
   - Pas de dosage.
4. **Prof Bazhar**, vidéos.
   - Partie 1 : autoprotolyse, rappel du logarithme, Ke, pH/pKe, neutre/acide/basique, Ka (acide + eau, puis base + eau), pH–Ka, K acide-base.
   - Partie 2 : force des acides et des bases, distribution, indicateurs.
   - Vidéo à part sur le dosage : principe, équivalence, dosage d'un acide puis d'une base, colorimétrie, choix de l'indicateur, τ du titrage.

**Ordre commun** : autoprotolyse → Ke → Ka/pKa → (pH = pKa + log) → K d'une réaction acide-base → comparer acides et bases → prédominance et distribution → indicateurs colorés → dosage. Les indicateurs passent toujours avant le dosage ; le choix de l'indicateur vient après la courbe.

**Divergence** : le dosage est dans le chapitre chez Naceiri, à part chez Bazhar et Moutamadris. Ici il reste dans le cours : `perimetre.json` met la clé `dosage` dans ce chapitre, et c'est le cas le plus fréquent au national.

### Le cadre

`cadre_reference_2bac_pc.json`, clé `acides_bases`, capacités AB1 à AB10, sous-domaine 2 du cadre officiel. Hors cadre et absents du cours : Kb, pKb, pOH, solution tampon, Henderson-Hasselbalch par son nom, activité, c°.

### Le national

20 sujets, de 2016 à 2025, exercice de chimie, recherche par mots-clés :

| Cas type | Sujets |
|---|---|
| Ka / pKa | 16/20 |
| Dosage | 14/20 |
| Équivalence | 13/20 |
| Base dans l'eau, HO⁻ | 12/20 |
| Prédominance | 7/20 |
| Indicateur, zone de virage | 6/20 |
| Ke | 5/20 |
| Tangentes | 5/20 |
| Courbe dérivée dpH/dV | 4/20 |
| Distribution | 3/20 |
| K avec Ka₁ et Ka₂ | 2/20 |

Le dosage et le pKa portent l'essentiel des points : c'est là que l'élève fait lui-même les étapes.

## 2. La logique avant

Ordre : ouverture (la carte du chapitre, puis trois pH) → rappels → Ke → base dans l'eau → Ka → comparer → K acide-base → prédominance → indicateurs → dosage → exploiter la courbe → 5 nationaux → bilan.

Défauts relevés :

- **La carte d'ouverture (`ab_o1_carte`) donnait tout le chapitre d'un coup** (règle 3) : Ka, pKa, Ke et « C_A·V_A = C_B·V_BE », avant la première idée.
- **`ab_o2_trois_ph` lisait trois pH avant le rappel du pH** (règle 6). Elle venait avant `ab_z1` et `ab_r1b`.
- **Ke était donné, pas tiré de mesures** (règle 5, demande de l'utilisateur). `ab_w2_ke` posait « Ke = [H₃O⁺]·[HO⁻] » puis le calculait seulement dans l'eau pure. L'élève ne voyait jamais que le produit reste le même quand [HO⁻] change.
- **`ab_r2_constante` (rappel de K) était entre les rappels et l'autoprotolyse**, alors que sa dernière phrase (« et une base dans l'eau ? ») annonce la base. Cette phrase tombait dans le vide.
- **Le dosage et les nationaux étaient racontés.** La voix donnait chaque lecture (V_BE, pKa, espèce qui prédomine) ; l'élève n'en faisait aucune avant la correction (demande de l'utilisateur, règles 3 et 5).
- **Les blocs avaient jusqu'à 5 diapos**, et des séances en avaient 15 (règle 7).

## 3. La logique après

Elle suit l'ordre commun des profs, à deux écarts près, écrits avec leur raison :

1. **Comparer les acides et les bases** reste avant la K d'une réaction acide-base. L'axe des pKa (`ab_c3_classement`) rend lisible K = 10^(pKa₂ − pKa₁) : on lit sur l'axe qui est au-dessus. Chez les profs, la K vient juste après Ka.
2. **pH = pKa + log** reste juste avant les domaines de prédominance, et non juste après Ka : un prérequis vient juste avant son usage (règle 6).

Il y a 6 séances de 3 blocs, de 2 à 4 diapos par bloc.

### Séance 1 — Les outils depuis zéro ; ce que contient l'eau ; Ke tiré des mesures

**Bloc ab_b01 — Les outils : log, acide, base, couple, pH**

| Diapo | Pourquoi ici |
|---|---|
| `ab_z1_puissance` [Q] | Puissances de dix et log, de zéro. Ils servent dès la diapo suivante (pH, Ke = 10⁻¹⁴). Bazhar fait aussi un « rappel du logarithme ». |
| `ab_r1_rappel` | Acide, base, couple, avec l'image de la balle qu'on donne. |
| `ab_r1b_eau_ph` | L'eau dans deux couples, et pH = −log[H₃O⁺]. Il passe avant toute mesure de pH (avant : `ab_o2` le précédait). |

**Bloc ab_b02 — Ce que contient l'eau : l'autoprotolyse**

| Diapo | Pourquoi ici |
|---|---|
| `ab_o2_trois_ph` **(déplacée)** | La situation-problème : trois liquides incolores, trois pH. Tous les profs ouvrent par une situation (l'aquarium, le lait). Placée ici, chaque pH lu est déjà compris. Sa question (« qu'y a-t-il dans l'eau ? ») ouvre l'autoprotolyse. |
| `ab_w1_autoprotolyse` | Deux molécules d'eau échangent un proton, à la loupe. |
| `ab_w1b_limitee` | τ de l'autoprotolyse ≈ 3,6·10⁻⁹. C'est l'activité de Naceiri : pH = 7, tableau, x_max, τ. |

**Bloc ab_b03 — Un produit qui ne change pas : Ke**

| Diapo | Pourquoi ici |
|---|---|
| `ab_w2a_mesures` **(nouvelle)** [OBS] | Ke vu dans des mesures avant d'être nommé (demande de l'utilisateur : « construits à partir de mesures que l'élève voit, animation qui produit les valeurs, puis tableau »). Voir le détail sous ce tableau. |
| `ab_w2_ke` [Q] | Seulement maintenant, le nom et la définition : Ke = [H₃O⁺]·[HO⁻], 10⁻¹⁴ à 25 °C, pKe = 14, vrai dans toute solution aqueuse. Sa voix commence par « on multiplie les deux concentrations » : elle continue la diapo d'avant. Voix gardée. |

Ce que fait `ab_w2a_mesures`, dans la vue `eau.html?vue=ke_mesures` :

1. Trois béchers : eau pure, soude 10⁻⁴ mol/L, soude 10⁻³ mol/L.
2. La sonde passe dans chacun : le pH-mètre lit 7,00, puis 10,00, puis 11,00.
3. Le tableau naît ligne par ligne : solution, pH, [H₃O⁺], [HO⁻], [H₃O⁺]·[HO⁻].
4. La voix ne dit pas les produits. L'**observation** fait comparer la dernière colonne : [HO⁻] monte, [H₃O⁺] descend, le produit reste 1,0·10⁻¹⁴.
5. La conclusion ne s'écrit qu'après la réponse (`sim_avant: {conclusions: false}`, `sim_apres: {conclusions: true}`).

Pourquoi ces mesures-là :

- [HO⁻] = C vient de la soude, qui donne tous ses ions HO⁻ (dissolution totale d'un solide ionique, vue au tronc commun).
- [HO⁻] dans l'eau pure vient de l'autoprotolyse (diapo `ab_w1`).
- Rien n'est donc supposé.
- `ab_w5_soude` (plus loin) refait le chemin dans l'autre sens, de Ke vers le pH : c'est la deuxième façon (règle 6).

### Séance 2 — Acide, neutre, basique ; une base dans l'eau

**Bloc ab_b04 — Solution acide, neutre, basique ; [HO⁻] avec Ke**

| Diapo | Pourquoi ici |
|---|---|
| `ab_w3_solutions` | Comparer [H₃O⁺] et [HO⁻], avec une poignée pH : l'élève manipule. Ordre de Bazhar : Ke, puis neutre/acide/basique. |
| `ab_w3b_neutre` | pH = pKe/2, démontré (Naceiri : comparer à pKe/2). |
| `ab_w4_ho` [Q] | [HO⁻] = Ke/[H₃O⁺], avec le piège « jamais 10^(−pH) ». |

**Bloc ab_b05 — Une base dans l'eau : soude et ammoniac**

| Diapo | Pourquoi ici |
|---|---|
| `ab_r2_constante` **(déplacée)** | Rappel du ch12 : le tableau en C·τ, K = C·τ²/(1 − τ). Placé juste avant la base, il sert à `ab_b2` (le même tableau). Sa dernière phrase, « et une base dans l'eau ? », y mène enfin. **Sa question** (K et la dilution, déjà travaillée au ch12) **passe dans la réserve de fin de cours**, avec ses réactions, pour qu'il n'y ait qu'une ardoise par bloc. Voix de la diapo gardée. |
| `ab_w5_soude` | Une base totale : le pH par Ke. C'est la deuxième façon de dire Ke. |
| `ab_b1_ammoniac` | Une base faible : NH₃ capte un proton de l'eau. |

**Bloc ab_b06 — Le taux d'avancement final d'une base**

| Diapo | Pourquoi ici |
|---|---|
| `ab_b2_taux` | τ = [HO⁻]_éq/C, par Ke (12/20 sujets ont une base). |
| `ab_b3_national` [Q] | National 2022 R (méthylamine), juste après sa notion. |

### Séance 3 — Ka et pKa ; comparer des acides et des bases

**Bloc ab_b07 — La constante d'acidité Ka et le pKa**

| Diapo | Pourquoi ici |
|---|---|
| `ab_a1_ka` | Ka = la K de l'acide avec l'eau : elle découle du ch12, donc de mesures déjà vues. Ordre des 4 profs. |
| `ab_a2_pka` | pKa = −log Ka : un nombre simple. |
| `ab_a3_mesure` [Q] | Mesurer un pKa avec le pH (16/20 sujets), avec la démonstration. |

**Bloc ab_b08 — Ka d'un couple de base, couples de l'eau ; comparer deux acides**

| Diapo | Pourquoi ici |
|---|---|
| `ab_a4_ammonium` | Le Ka de NH₄⁺/NH₃ à partir de la réaction de NH₃ avec l'eau (Bazhar : Ka de l'acide, puis de la base). |
| `ab_a5_eau` | Les pKa des couples de l'eau : 0 et 14. |
| `ab_c1_acides` [OBS] | Deux acides, même C : deux pH, puis le tableau, puis les barres de τ. **Observation** : après la règle « Ka grand → τ grand », l'élève dit lequel est le plus fort ; la voix confirme. La commande « conclusion » est déplacée sur « هو الأقوى ». |

**Bloc ab_b09 — Comparer deux bases ; l'axe des pKa**

| Diapo | Pourquoi ici |
|---|---|
| `ab_c2_bases` | Même démarche pour deux bases (Naceiri : méthylamine et ammoniac). |
| `ab_c3_classement` [Q] | Classer les couples sur l'axe des pKa. Cet axe sert ensuite à la K d'une réaction (écart 1 ci-dessus). |

### Séance 4 — Constante d'une réaction acide-base ; prédominance ; indicateurs colorés

**Bloc ab_b10 — La constante d'une réaction acide-base**

| Diapo | Pourquoi ici |
|---|---|
| `ab_k1_reaction` | K = Ka₁/Ka₂. |
| `ab_k2_puissance` | K = 10^(pKa₂ − pKa₁). |
| `ab_k3_totale` | L'acide avec HO⁻ : K = Ka/Ke, presque totale. Elle prépare la réaction de dosage. |
| `ab_k4_national` [Q] | National 2020 R : qui est Ka₁ dans le sujet. |

**Bloc ab_b11 — pH, pKa et prédominance**

| Diapo | Pourquoi ici |
|---|---|
| `ab_p1_relation` | pH = pKa + log([A⁻]/[AH]), établi juste avant son usage (écart 2). |
| `ab_p2_domaines` [OBS] | Les domaines sur l'axe des pH. **Observation** : « à gauche du pKa (pH < pKa), qui prédomine ? ». L'élève utilise la relation de la diapo d'avant ; la voix confirme (« log négatif, donc AH »). La commande « domaine_acide » est déplacée sur « هنا l'acide éthanoïque prédomine ». Le nom de l'espèce ne s'écrit donc qu'après la réponse. |
| `ab_p3_distribution` | Les pourcentages, et le croisement à pKa. Pas d'observation : la simulation écrit « 50 % : pH = pKa » au moment même où la voix commence la phrase. Il faudrait `conclusions: false` dans `predominance.html` (voir § 5). |
| `ab_p4_national` [Q] | National 2025 R, juste après la distribution. |

**Bloc ab_b12 — Les indicateurs colorés**

| Diapo | Pourquoi ici |
|---|---|
| `ab_i1_indicateur` | Le BBT dans les trois solutions de l'ouverture : jaune, vert, bleu. La question de la diapo `ab_o2` trouve sa réponse. |
| `ab_i2_virage` | La zone de virage. |
| `ab_i2b_regle` | pKa − 1 à pKa + 1, démontré. Les indicateurs passent avant le dosage, comme chez tous les profs. |

### Séance 5 — Le dosage pas à pas : équivalence, tangentes, demi-équivalence, indicateur

**Bloc ab_b13 — Le dosage : montage, réaction, équivalence**

| Diapo | Pourquoi ici |
|---|---|
| `ab_d1_montage` [Q] | Le but et le montage : burette, bécher, agitateur, sonde. |
| `ab_d2_reaction` | La réaction de dosage : rapide, totale (K = Ka/Ke), unique. |
| `ab_d3_equivalence` [OBS] | Le tableau d'avancement du dosage. **Observation** : « avant l'équivalence, quel réactif est limitant ? » (HO⁻), avant la voix. La commande « avant » est déplacée pour que « HO⁻ limitant » ne s'écrive qu'après. |
| `ab_d4_courbe` | La courbe pH = f(V_B), tracée goutte à goutte : les trois zones et le saut. |

**Bloc ab_b14 — Trouver l'équivalence : tangentes et dérivée**

| Diapo | Pourquoi ici |
|---|---|
| `ab_d5_tangentes` [OBS] | Les tangentes, en trois étapes tracées une à une. **Observation** : E est placé ; l'élève lit V_BE (20,0 mL, en se méfiant de 8,3 = pH_E), puis la voix lit. La commande « lecture » est déplacée. |
| `ab_z2_pente` | Rappel de zéro : la pente, juste avant la dérivée. |
| `ab_d6_derivee` [Q] | dpH/dV_B : le pic à l'équivalence. |

**Bloc ab_b15 — pH à l'équivalence, demi-équivalence, indicateur**

| Diapo | Pourquoi ici |
|---|---|
| `ab_e1_phe` [OBS] | Trois dosages, trois pH_E. L'observation était déjà là. |
| `ab_e2_demi` [OBS] | La demi-équivalence : le tableau, puis pH = pKa. **Observation** : « lis le pH à 10,0 mL : que vaut le pKa ? » (4,8 ; pièges : 8,3 et 3,4). La commande « lecture » est déplacée. |
| `ab_e3_indicateur` [Q] | La zone de virage qui contient pH_E. Le choix vient après la courbe, comme chez Naceiri et Bazhar. |

### Séance 6 — Doser une base ; dosage conductimétrique ; nationaux et bilan

**Bloc ab_b16 — Doser une base ; le dosage conductimétrique**

| Diapo | Pourquoi ici |
|---|---|
| `ab_e4_base` | Doser une base par un acide (Bazhar : le dosage d'une base). |
| `ab_e5_conductimetrie` | σ = f(V) : deux droites (capacité AB9). |
| `ab_e5b_pourquoi` | Pourquoi les droites, et où est l'équivalence. |

**Bloc ab_b17 — Nationaux : tangentes, base dosée, dérivée**

| Diapo | Pourquoi ici |
|---|---|
| `ab_n1_2016n` [OBS] | National 2016 N. **Observation** : après la construction des tangentes, l'élève lit V_BE = 6 mL (pièges : pH_E = 8,7 et V_A = 5 mL). La commande « lecture » est déplacée. |
| `ab_n2_2022r` | National 2022 R : une base dosée par un acide. |
| `ab_n3_2022n` [Q] | National 2022 N : la dérivée et le pourcentage, avec la démonstration. |

**Bloc ab_b18 — Nationaux : distribution et demi-équivalence ; bilan**

| Diapo | Pourquoi ici |
|---|---|
| `ab_n4_2024r` [OBS] | National 2024 R. **Observation** : après le trait à 50 %, l'élève lit le pKa au croisement (10,8 ; pièges : 11,88 et 50). |
| `ab_n5_2023r` [OBS] | National 2023 R. **Observation** : au point Q (demi-équivalence), que vaut le pKa ? (9,9 ; pièges : 5,8 et 7). |
| `ab_bl_fiche` | La fiche « Ce qu'il faut retenir ». |
| `ab_cr_carte` [Q] | La carte complète : la seule carte du cours, quand tout a été vu. |

**Retirée** : `ab_o1_carte`, la carte d'ouverture. Elle donnait tout le chapitre avant la première idée, et elle doublait la carte finale.

**Les nationaux restent groupés en fin de cours, contrairement au ch12.** Ce sont des exercices de dosage complets : ils mêlent tangentes, indicateur, demi-équivalence et distribution, donc ils ne peuvent venir qu'après tout le dosage. Les nationaux d'une seule notion sont déjà placés juste après elle : `ab_b3`, `ab_a3` (exercice 2023 N), `ab_k4`, `ab_p4`.

## 4. Ce qui change, ce qui reste

**Ce qui reste.** Les ids et les textes dits de toutes les diapos gardées sont inchangés : leur voix reste.

**Les nouveaux textes à dire.**

- Une seule diapo à enregistrer : `ab_w2a_mesures`. Sa voix en darija passe `verifier_mots` ; restent trois termes du programme à écouter : « béchers », « soude », « autoprotolyse ».
- Les champs des 9 nouvelles questions d'observation (`ab_w2a_mesures`, `ab_c1_acides`, `ab_p2_domaines`, `ab_d3_equivalence`, `ab_d5_tangentes`, `ab_e2_demi`, `ab_n1_2016n`, `ab_n4_2024r`, `ab_n5_2023r`) : 63 pistes.
- Des mots darija peu connus de la voix ont été remplacés : « كتذوب » → « كتعطي كاع… », « طيحنا » → « زدنا », « كيساليو » → « ما بقاوش ».
- Termes du programme gardés, à écouter : « méthanoïque », « demi-équivalence », « quatre-vingt-huit ».

**Les pointages.** Les mots de 6 commandes sont déplacés plus loin dans la même phrase, pour qu'aucune réponse ne s'écrive avant l'arrêt de la voix :

| Diapo | Commande |
|---|---|
| `ab_c1_acides` | conclusion |
| `ab_p2_domaines` | domaine_acide |
| `ab_d3_equivalence` | avant |
| `ab_d5_tangentes` | lecture |
| `ab_e2_demi` | lecture |
| `ab_n1_2016n` | lecture |

Pour `ab_n4_2024r` et `ab_n5_2023r`, l'écart avec l'arrêt suffisait déjà. Le contrôle est fait par script, avec la durée réelle des pistes et l'avance de 0,9 s du lecteur.

**Les ardoises.** La question de `ab_r2_constante` passe dans la réserve de fin de cours. Ensuite, chaque bloc a au plus une ardoise, séparée de la suivante par au moins deux diapos (vérifié par script).

**Les séances.** Elles passent de 5 séances de 14 blocs (jusqu'à 5 diapos) à 6 séances de 18 blocs de 2 à 4 diapos. Les cahiers et les compétences sont recoupés comme au ch12. La nouvelle diapo appartient à la compétence C1 (Ke).

**Les réactions écrites.** J'ai fait aussi une correction hors logique : 5 réactions écrites portaient « tau » en lettres ; il est remplacé par « τ ».

**La simulation.** `eau.html` reçoit la vue `ke_mesures` (béchers peints, sonde, pH-mètre, tableau à la craie ; texte ≥ 15 px dans le cadre 760 × 420). Ses moments sont `bechers`, `mesure_1..3`, `ligne_1..3`, `comparer`, `conclusion`. Ses repères sont `becher_1..3`, `afficheur`, `tableau`, `colonne_produit`, `conclusion`. Le paramètre `conclusions` tait la comparaison pendant la question. Vérifiée dans Chromium, sans erreur.

## 5. Ce qui n'a pas pu être fait, et les besoins

- **Fait à la 2ᵉ passe (§ 6)** : les observations de `ab_b2_taux` (x_éq) et de `ab_p3_distribution` (le croisement), et le curseur de `ab_p2_domaines`, grâce au paramètre `conclusions` ajouté à `base.html` et `predominance.html`.
- **Les voix.** Les 126 pistes sont à faire sur le VPS (voix Bodi), avec `scripts/voix/attente_construire.py` puis `attente_poser.py`. Les diapos nouvelles n'ont pas de durée de voix : le contrôle de pointage les signale « GESTE » (tous les gestes à 0 s) tant qu'elles ne sont pas enregistrées. Avec une durée estimée (66 ms par caractère, médiane du cours), il ne reste aucun écart.
- **Mots à changer à la prochaine voix** (diapos déjà enregistrées, non réécrites pour garder leur voix) : « l'afficheur » (`ab_o2_trois_ph`, `ab_w5_soude`, `ab_a3_mesure` et ses réactions) → « l'écran du pH-mètre » ou « le pH-mètre كيعطي » ; « béchers » (`ab_o2_trois_ph`) → « trois solutions » ; « محدودة » (`ab_w1`, `ab_w1b`, `ab_b1`, `ab_b2`) → « ماشي كاملة » ; « كتذوب » (`ab_w5_soude`) ; « كتتبدل » (`ab_r2_constante`). Termes du programme gardés : autoprotolyse, éthanoate, méthylamine, soude, loupe.
- **Les questions d'observation.** Elles sont 18 dans le cours (10 de la logique, 8 de la 2ᵉ passe), à la demande de l'utilisateur du 18 novembre (« laisser à l'élève le temps de trouver seul »). Aucune ne demande de calcul : lecture de courbe, relation à choisir, espèce qui prédomine, indicateur. Les calculs s'écrivent ensuite comme le barème les lit.
- **Taille des indices.** Dans la nouvelle page `national.html`, tout texte fait au moins 15 px à l'écran en 724 × 350 (mesuré) ; les indices, exposants et états physiques (« _A », « ⁻² », « (aq) ») sont écrits par le kit à environ 62 % de la ligne (≈ 9 px). C'est le kit partagé (`shared/tableau/tableau.js`) ; besoin noté, non modifié.
- **Fichiers partagés.** Aucun n'a été modifié (`shared/`, lecteur `frontend/src/`), ni `commun.js`, `deroule.js`, `exploiter.html`, `figures.html` de ce dossier.

## 6. 2ᵉ passe du 18 novembre : un national joué pas à pas, rien de décisif avant la réponse

Demande de l'utilisateur : « simple, animé, expliqué, ne pas tout donner au départ, laisser à l'élève le temps de trouver seul, une raison derrière chaque choix ».

### Le sujet choisi : national 2018, session normale (exercice 1, partie 2)

L'acide lactique AH (V_A = 15 mL) dosé par la soude (C_B = 3·10⁻² mol/L) ; K_A = 10^(−3,9) ; trois indicateurs (hélianthine 3 – 4,4 ; BBT 6 – 7,6 ; rouge de crésol 7,2 – 8,8). **Pourquoi lui** : ses cinq questions couvrent, sur une seule courbe, l'équation de dosage, l'équivalence par les tangentes, C_A par la relation d'équivalence, le choix de l'indicateur et l'espèce qui prédomine (rapport [A⁻]/[AH]) ; il n'était pas encore dans le cours (2016 N, 2022 R/N, 2023 R, 2024 R, 2025 R y sont déjà) ; sa courbe se calcule exactement (pH 2,82 au départ, 3,91 à 5 mL, 7,99 à 10 mL), donc la figure animée est celle du sujet. Une 6ᵉ diapo, « en plus », lit le pKa à la demi-équivalence sur la même courbe (Ka / pKa, cas de 16 sujets sur 20) et retrouve la donnée K_A = 10^(−3,9).

### La page `acides-bases-tableau/national.html?ex=2018N&vue=q1 … q6` (nouvelle)

Une vue par question, une URL par diapo (pas d'écart IFRAME). À gauche, le montage peint (potence, burette graduée dont le niveau descend, bécher sur l'agitateur, pH-mètre qui affiche le pH du mélange) ; au centre, le graphe ; à droite, la question, « Déjà trouvé » (la seule réponse d'avant dont la question a besoin) puis la correction écrite comme le barème la lit. Les valeurs naissent du montage : en q2, la burette verse millilitre par millilitre, le pH-mètre lit, chaque mesure devient un point, puis la courbe passe par les points ; ensuite les deux tangentes, la parallèle, E. `set_parameters {conclusions: false}` cache la réponse et la correction de la question (et la bulle « Arrêt sur image » ne la dit pas) ; `true` (défaut) les écrit. Aucun départ seul : la première commande de la voix lance la scène. Cadre large, toutes les tailles ≥ 21 dans le cadre : plus petit texte 15 px en 724 × 350, 25 px en 1024 × 560 (mesuré dans Chromium) ; captures regardées à 724 × 350 et 1024 × 560, sans chevauchement.

### Les diapos nouvelles (activité `ab_partie12`, séance 7)

| Diapo | Question | Ce que l'élève fait avant la correction (observation) | Correction (barème) |
|---|---|---|---|
| `ab_x1_equation` | 1.1 | La soude coule ; à la loupe HO⁻ s'approche de AH : il choisit l'équation (pièges : AH + H₂O, Na⁺). | AH + HO⁻ → A⁻ + H₂O, totale. |
| `ab_x2_tangentes` | 1.2 | La courbe naît des mesures, les tangentes donnent E : il lit les coordonnées (pièges : inversées, 12 = fin). | V_BE = 10 mL ; pH_E ≈ 8. |
| `ab_x3_concentration` | 1.3 | Deux barres, n(AH)₀ et n(HO⁻) versé, s'égalisent en E : il choisit la relation (piège : volumes croisés). | C_A = C_B·V_BE/V_A = 2·10⁻² mol/L. |
| `ab_x4_indicateur` | 1.4 | Les trois zones de virage debout sur le graphe, la droite pH = 8 partie de E : il choisit. | Rouge de crésol, 8 ∈ [7,2 ; 8,8] ; il vire au labo. |
| `ab_x5_predominance` | 1.5 | pH ≈ 8 à 10 mL, pKa = 3,9 : il dit qui prédomine. | [A⁻]/[AH] = 10^(8 − 3,9) ≈ 1,26·10⁴ > 1 : A⁻ ; diagramme de prédominance. |
| `ab_x6_pka` | en plus | Verticale à V_BE/2 = 5 mL : il lit le pKa (pièges : 8 = pH_E, 2,8 = départ). | pH = pKa = 3,9 ; K_A = 10^(−3,9). |

**Pourquoi après le bilan des nationaux et avant la fiche** : l'exercice reprend toutes les notions du dosage ; il vient quand chacune a été vue seule, et il prépare la fiche « Ce qu'il faut retenir ». Les nationaux existants (`ab_n1` … `ab_n5`, `ab_b3`, `ab_a3`, `ab_k4`, `ab_p4`) restent tels quels, avec leurs observations.

**Les séances.** Séance 6 : `ab_b16`, `ab_b17`, `ab_b18` (`ab_n4`, `ab_n5`, avec leur cahier). Séance 7 (nouvelle) : `ab_b19` (x1 – x3), `ab_b20` (x4 – x6), `ab_b21` (la fiche et la carte, avec les deux lignes de cahier de bilan qui étaient dans `ab_b18`). Les blocs `ab_b19` et `ab_b20` n'ont pas d'ardoise : leurs six observations la remplacent. Compétences : x1, x3 → C7 ; x2, x6 → C8 ; x4, x5 → C6.

### Rien de décisif avant la réponse (besoins du § 5 de la logique)

- **`ab_b2_taux`** : nouvelle observation « à l'équilibre, comment s'écrit x_éq ? » après « ولكن فالتوازن: » ; `base.html?vue=taux` accepte `conclusions` (défaut `true`, rendu du cours en ligne inchangé) : `false` tait x_éq, τ, l'application et « limitée », et la bulle d'arrêt.
- **`ab_p3_distribution`** : nouvelle observation « à quel pH les deux courbes se croisent-elles ? » ; `predominance.html` tait le croisement « 50 % : pH = pKa » avec `conclusions: false`.
- **`ab_p2_domaines`** : son observation reçoit `sim_avant`/`sim_apres` : les barres [CH₃COOH] / [CH₃COO⁻] du curseur à 3,41, leurs pourcentages et « … prédomine » sont tus pendant la question (ils donnaient la réponse).
- Relu par script : aucune ligne `centre` ne s'affiche avant l'arrêt avec la bonne réponse ; les autres observations du cours étaient déjà protégées (commandes déplacées à la logique).

### Mots

Mots des pistes nouvelles, vérifiés sur la copie en attente (`verifier_mots.py en_attente/phys_ch13_acides_bases <ids>` : sans le préfixe `en_attente/`, le script lit le cours en ligne et ne voit pas les pistes nouvelles). Mots darija rares remplacés : « فوقو » → « الفوق »، « الخليط » → « المحلول »، « كتطيح » → « كنزيدو »، « بالloupe » → « من قريب »، « ما كيتفاعلوش » → « ما كيديرو والو »، « كتصب » → « كتزيد »، « قياس » → « mesure »، « مستوية » → « ثابتة »، « le barème » → « خاصك تكتب فالامتحان »، « ما خاصناش » → « ما كاين علاش »، « المناسب » → « اللي مزيان »، « نجرو » → « نرسمو »، « زيادة على » → « سؤال زايد »، « قلبتيهم » → « بدلتي البلاصة »، « صبعك » → « شوف فين » ; « trois béchers » → « trois solutions » (`ab_w2a_mesures`, pas encore en voix). Restent des termes du programme, à écouter : soude, saut, tangentes, indicateur coloré, virage, hélianthine, crésol, demi-équivalence, autoprotolyse. Les diapos voicées non réécrites gardent leurs mots ; la liste à changer est au § 5.

> Fusion (18 novembre, soir) : une autre session avait poussé en parallèle le même besoin (`bd37fa2d` :
> `predominance.html` accepte `conclusions`, observation sur `ab_p3_distribution`). La version gardée est celle de
> cette 2ᵉ passe, qui couvre aussi la bulle d'arrêt et `base.html` ; les pistes en double de `ab_p3` sont retirées.
