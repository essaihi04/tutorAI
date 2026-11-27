# phys_ch12_etat_equilibre — corrections du 26-27/11/2026

Cours servi : `backend/data/courses/phys_ch12_etat_equilibre.json` (phase 1, aucune voix changée).
Copie d'attente : `backend/data/courses/en_attente/phys_ch12_etat_equilibre.json` (phase 2, texte parlé ; partie du servi
actuel, cahiers et repères de synchronisation de l'amont gardés). Pistes à générer : `../voix_a_generer/phys_ch12_etat_equilibre.json`.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| Version | Diapos | Questions 6 premières | Formules dites non écrites | ≥ 60 mots sans geste | Notions clés | redites | annoncées (≠) | Premier mot | Suites même mot |
|---|---|---|---|---|---|---|---|---|---|
| Avant (26/11) | 58 | 3 | 69 | 6 | 17 | 8 | 0 (0) | « دابا » 40 % | 11 |
| Servi après phase 1 | 58 | 1 | 42 | 2 | 19 | 8 | 0 (0) | « دابا » 40 % | 11 |
| Attente (phase 2) | 59 | 0 | 41 | 2 | 20 | 20 | 20 (15) | « le » 5 % | 0 |

- La question restante du servi (diapo 3, voix qui finit sur « ? ») est corrigée dans l'attente.
- « annoncées (≠) » : l'audit compte le **mot-clé** trouvé (16 possibles en darija), d'où 15. Compté sur la **phrase
  d'annonce entière** : 20 annonces, 20 phrases différentes (vérifié par script). 20/20 notions clés annoncées et redites
  autrement (100 %).
- Formules « dites non écrites » restantes (41) : 22 dans les énoncés lus (la feuille du sujet est à l'écran), les autres
  sont écrites par la simulation dans la même phrase (le découpage de l'audit coupe aux « : ») ou une phrase plus loin
  (`ee_e1_concentrations` : C écrit par la sonde) ; laissées.
- Passages ≥ 60 mots sans geste : `ee_z5_ph` (66, voix inchangée) et `ee_k2_produits` (66, trois calculs de suite,
  aucun repère de la simulation ne les nomme) ; laissés.

## Phase 1 — cours servi (sans changer la voix)

- **Questions de bloc** : `ee_b05` vidé (retrouver = doublon exact de `ee_b06`, exercice Qr,éq = toujours présent dans la
  réserve `ee_n1_national/exercices_fin_de_cours[0]`) — rien n'est perdu ; `ee_b10` retrouver « de quoi dépend τ »
  retiré (gardé dans `ee_b11`, après 50-51) ; `ee_b11` exercice retiré (doublon exact de celui de `ee_b10`, gardé où la
  dilution est enseignée). Les blocs vidés reçoivent de nouvelles questions dans l'attente (ci-dessous).
- **Aucune question dans les 6 premières** : la question de `ee_z1_concentration` passe dans ses
  `exercices_fin_de_cours` (réactions dans `reponses_fin_de_cours`) ; l'observation « τ = 0,039 : totale ? » de
  `ee_r1_taux` est retirée du servi (diapo 6) et **remise telle quelle, avec ses voix, dans l'attente**, où cette diapo
  devient la 8ᵉ.
- **Exercice avant la méthode** : l'exercice « Calcule Qr,i » de `ee_i2_melange` passe sur `ee_i2b_calcul` (le calcul
  y est montré) ; `ee_b04.exercice.reprend` mis à jour.
- **Dit = écrit** : 21 entrées de pointage (22 gestes : repère ou `play_until` au mot qui dit la formule) et 10 cartes `centre` sur 17 diapos (plus la carte « G = k·σ » recoupée)
  (`ee_r1_taux`, `ee_i3_au_cours`, `ee_e3_expression` — les concentrations étaient dites avant d'être écrites —,
  `ee_n1_national`, `ee_k2_produits`, `ee_m2a_conductance` — « G = k·σ ; σ = Σλᵢ[Xᵢ] » coupé en deux cartes, chacune à
  son mot —, `ee_m3_calcul`, `ee_n5_courbe`…).
- **Simulations** : `demarrer` start → reset sur 37 diapos pilotées par `play_until` (la scène courait seule) ;
  `&depart=` sur `ee_z5_ph`, `ee_i2b_calcul`, `ee_m2_conductimetrie` (même page que la diapo d'avant, scène pas
  rechargée). `verifier_pointage_simulations` : 73 → 33 écarts (restent 25 GESTE d'avant et 8 « flacon_n » construits à
  l'exécution, faux positifs).
- **Écran** : la précipitation Fe(OH)₃ retirée des puces de `ee_q4_solides` (diapo qui introduit les solides) ; le
  cahier de cette diapo est celui de l'amont après fusion.

## Phase 2 — copie d'attente (texte parlé)

### Ordre des notions (`ordre-des-notions/phys_ch12_etat_equilibre.md`)

| # | Défaut | Fait |
|---|---|---|
| 1 | `ee_b05` interroge Qr,éq avant 23-24 | phase 1 + nouvelles questions : retrouver « comment évolue Qr », exercice Qr,i d'une pile (repris de la réserve de `ee_n4_pile`) |
| 2 | Diapo 6 : quatre rappels, x_éq avant l'équilibre | `ee_r2_equilibre` avancé en tête de partie (il présente l'exemple A, sa question passe à `ee_o2_flacons`, fin du bloc) ; diapo 6 coupée : **`ee_r1a_tableau` (nouvelle)** = tableau, x_max, x_éq (même simulation, moments tableau → x_eq) ; `ee_r1_taux` = τ (simulation ouverte figée à x_eq) |
| 3 | Exercice Qr,i avant le calcul | phase 1 |
| 4 | K nommé en 18 avant sa définition | phrase ajoutée en 18 : « K, on la verra plus loin dans ce cours ; ici, seulement Qr,i » |
| 5 | Ke non enseigné (2022 R) | `ee_n2_base` : « Ke, expliqué au cours suivant ; ici on utilise seulement la relation qu'il donne » |
| 6 | « réaction du chapitre de cinétique » | exemple gardé, rattaché au bon chapitre (ch9, le catalyseur) — voir la référence du prof |
| 7 | `ee_b10` pose la question de `ee_b11` | phase 1 + `ee_b10` reçoit un retrouver sur la dilution (C₀V₀ = C₁V₁) et `ee_b11` un exercice (τ de l'acide méthanoïque, repris de la réserve) |
| 8 | « concentration effective » non expliquée | phrase ajoutée en `ee_q1_quotient` |
| 9 | Précipitation dans la diapo des solides | phase 1 (écran) |
| — | `ee_f1_dilution` : « l'exemple B » jamais nommé | remplacé par le rappel des trois béchers |

`ee_b12` (doublon exact de `ee_b08`) reçoit des questions sur ce qu'il enseigne : l'eau dans K de l'estérification,
K' = 1/K (repris de la réserve de `ee_n5_courbe`). Les questions de bloc ne sont pas mises en voix
(`FIN_DE_BLOC_COMPLETE = False`) : listées à part dans `voix_a_generer`.

### Notions importantes (règle 55)
20 annonces, toutes différentes, avant chaque notion clé (`ee_q1` … `ee_bl_fiche`, plus `ee_k5_tau`) ; une deuxième façon
de la dire dans la diapo (« بطريقة أخرى : … » : photo de la solution, la maison et ses habitants, la boutique pleine,
« si tu retournes l'équation, retourne K », « K est comme le numéro de la réaction »…) ; rappels dans une diapo suivante
(« تفكر … ») : Qr en `ee_i1_initial`, l'eau solvant en `ee_q4_solides` et `ee_x1_equation`, « Qr monte puis s'arrête »
en `ee_e2_quotient`, la relation Qr,éq(C, pH) en `ee_n1_national`, τ = x_éq/x_max en `ee_k5_tau`, pH lu = équilibre en
`ee_m1_methanoique` et dans la fiche, les trois béchers en `ee_f1_dilution` et `ee_m2_conductimetrie`.

### Tuteur humain (règle 56)
- Débuts de voix : premier mot le plus fréquent 5 % (« le »), 0 diapo qui suit avec le même premier mot ; les sept
  énoncés du national ont chacun leur ouverture et le lien avec la diapo d'avant.
- Touches humaines par bloc : « ما تخافش من هاد les nombres الصغار », « شوف هاد الحاجة، غريبة شوية! » (τ change,
  Qr,éq non), « أنا عارف أن الحساب كيبان طويل », « هادي كيغلطو فيها بزاف ديال التلاميذ، عادي » (mol/m³),
  « خديتي الوقت ديالك ف هاد السؤال؟ مزيان », « ب جوج قواعد ساهلين، جاوبنا على سؤال ديال الامتحان ».
- Réactions des questions des diapos (69, voix) : premiers mots variés (le plus fréquent : 5 fois sur 69), qui nomment ce
  qui est juste (« la forme صحيحة… », « زوين، فكرتي ف le mélange قبل ما تحسب ») ; corrigés : « l'élève عكس le
  quotient » (3ᵉ personne), « فزيرو فاصلة واحد » et « مول » (nombres et unités en darija), « 4 » en chiffre.
- Réserve de fin de cours : 5 nombres écrits en chiffres dans des paroles, remis en mots.

## Cours de référence du prof (`reference-prof/phys_ch12_etat_equilibre.md`)
Corrections recommandées : 1 (diapo 6 coupée, équilibre avant), 2 (`ee_b05`, `ee_b10`), 3 (K annoncé en 18) — déjà
faites ; en plus :
- 4 : « مثال : la réaction ديال le catalyseur، اللي شفنا فle chapitre ديال les transformations lentes et rapides » (diapo 10).
- 5 : G = I/U dit et écrit (carte, cahier de la diapo et du bloc `ee_b09`) avant G = k·σ (`ee_m2a_conductance`).
- 6 : `ee_q3_eau` : « elle n'y entre pas parce qu'elle est le solvant ; on verra un cas où l'eau n'est pas le solvant, et là elle entre ».
- 7 : `ee_f1_dilution` commence par le constat du ch11 (« quand on ajoute de l'eau, τ augmente ; on va comprendre pourquoi, avec K ») ; `ee_f3_courbe` : « K > 10⁴ : τ ≈ 1, réaction pratiquement totale » (dit, carte, cahier du bloc `ee_b11`).
- 8 : `ee_m2_conductimetrie` : « même idée que les trois béchers, avec un autre appareil ».
- Non fait (hors des corrections recommandées) : une diapo d'exercices de réactions hétérogènes ; « l'eau vaut 1 ».

## Voix
- 112 pistes à générer : 44 diapositives (43 changées + `ee_r1a_tableau`), 68 réactions/énoncés ; plus 26 textes de
  blocs et de réserve, non mis en voix aujourd'hui (`blocs_hors_voix`). `audio` retiré de chaque texte changé (111).
- `nombres_fr` passé (une correction : « جوج courbes » → « deux courbes »).
- Mots douteux à faire écouter (nouveaux, rares dans le corpus Bodi) : effective, تلفنا, جنب, ضاعش, غريبة, غلطة,
  كتطيح / كيطيح, كتقيس… (phrases de la banque) ; « ركّز » et « حلّ » écrits avec la chadda (non signalés par
  `verifier_mots.py`). Rares d'avant, gardés : benzoïque, méthylamine, conductimètre, soluté, flacons…

## Vérifications (attente)
`verifier_formules` 0 ; `verifier_parcours` 0 erreur ; `verifier_pointage` 6 (moments de `diluer.html` déclarés dans
`etapes`, faux positifs d'avant) ; `verifier_figures_cahier` 0 erreur ; `verifier_pointage_simulations` : 8 « flacon_n »
(faux positifs) et 13 GESTE d'avant sur des diapos à voix gardée ; les GESTE des 44 diapos sans voix sont des estimations
sans durée, à refaire une fois la voix générée.
