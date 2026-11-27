# phys_ch11_transformations_deux_sens — corrections du 26-27/11/2026

Cours servi : `backend/data/courses/phys_ch11_transformations_deux_sens.json` (phase 1, aucune voix changée).
Copie d'attente : `backend/data/courses/en_attente/phys_ch11_transformations_deux_sens.json` (phase 2, texte parlé ; repartie
du servi actuel, cahiers et repères de synchronisation de l'amont gardés). Pistes à générer :
`../voix_a_generer/phys_ch11_transformations_deux_sens.json`.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| Version | Diapos | Questions 6 premières | Formules dites non écrites | ≥ 60 mots sans geste | Notions clés | redites | annoncées (≠) | Premier mot | Suites même mot |
|---|---|---|---|---|---|---|---|---|---|
| Avant (26/11) | 56 | 2 | 56 | 4 | 19 | 11 | 0 (0) | « دابا » 39 % | 8 |
| Servi après phase 1 (+ cahiers de l'amont) | 56 | 1 | 46 | 1 | 24 | 11 | 0 (0) | « دابا » 39 % | 8 |
| Attente (phase 2) | 59 | 0 | 48 | 0 | 27 | 27 | 27 (13) | « هاد » 8 % | 0 |

- La question restante du servi (diapo 6 `td_z3_puissance`, voix qui finit sur « ? ») est corrigée dans l'attente.
- Le nombre de notions clés monte (19 → 27) : nouvelles cartes `centre`, lignes de cahier « Formule / Méthode » de l'amont,
  diapos ajoutées. 27/27 annoncées et 27/27 redites autrement (100 %).
- « annoncées (≠) » : l'audit compte le **mot-clé** trouvé (16 possibles), d'où 13. Compté sur la **phrase d'annonce
  entière** : 27 annonces, 27 phrases différentes (vérifié par script).
- Formules « dites non écrites » restantes (48) : 34 dans les énoncés lus (la feuille du sujet est à l'écran) et les
  diapos de sujets du national ; les autres sont écrites par la simulation dans la phrase d'à côté (l'audit coupe aux « : »).
  Le chiffre monte de 46 à 48 parce que l'attente a trois diapos de plus et des voix plus longues ; laissé.
- Passages ≥ 60 mots sans geste : 0 (gestes vers la simulation ajoutés en `td_a5_totale` et `td_n4_dosage`).
- Tournures recopiées : « la concentration des ions H trois O plus » (×12) — c'est le nom de la grandeur, laissé.

## Phase 1 — cours servi (sans changer la voix)

- **Questions de bloc** : aucune ne porte sur une notion enseignée après son bloc (vérifié bloc par bloc dans le JSON) ;
  rien à déplacer.
- **Règle 53** : la question de `td_z1_ion` (diapo 4) passe en réserve de fin de cours (`exercices_fin_de_cours`, ses
  réactions dans `reponses_fin_de_cours.e0`) ; le bloc `td_r_b1` interroge déjà l'ion.
- **Règle 54** (cartes `centre` au mot exact) : `td_a1_tableau` (C et V de l'exemple A), `td_a3_xf` (n = C·V),
  `td_a4_taux` (totale / limitée en deux cartes, pointées à la relecture), `td_a6_relation` (« À montrer : τ = 10^(−pH)/C »),
  `td_e4_dynamique` (v₁ diminue, v₂ augmente ; chocs efficaces), `td_c2_relation` ([H₃O⁺] = x_f/V, σ = (λ₁ + λ₂)·x_f/V,
  x_f = σ·V/(λ₁ + λ₂), pointée à la relecture), `td_c3_calcul` (λ₁ + λ₂ en mS puis en S), `td_n3_proportion`
  (x_f = τ·C_A·V), `td_n4_dosage` (équation et n(H₃O⁺) final). Les autres formules « non écrites » sont écrites par la
  simulation (vérifié dans `avancement.html`, `conductimetrie.html`) : laissées.
- **Erreur d'écran (27/11, sans toucher la voix)** : l'observation de `td_n1d_dilution` se déclenchait sur « la question
  onze… », absent de la voix ; elle part maintenant sur « la question trois point trois: شنو دارت la dilution ل tau؟ ».

## Phase 2 — copie d'attente

### Ordre des notions (règle 52, `ordre-des-notions/` et référence du prof)

| Défaut | Gravité | Ce qui est fait |
|---|---|---|
| 1. Énigme des pH (diapo 3) avant le pH | forte | `td_o2_flacons` déplacée après le pH-mètre (diapo 16) ; elle rappelle « plus le pH est petit, plus c'est acide » et prépare « si totale ». |
| 2. Tableau, x_max, réactif limitant jamais rappelés | forte | Deux diapos ajoutées avant le tableau de l'acide : `td_r1_tableau` (tableau, x, état final ; simulation `cinetique-tableau/avancement.html?vue=tableau` du chapitre précédent) et `td_r2_limitant` (x_max, réactif limitant ; `cinetique-tableau/limitant.html`). Le tableau à deux lignes finales du prof est dit en `td_a3_xf` (carte) et écrit au cahier du bloc `td_s2_b1`. |
| 3. pH avant d'où viennent les ions H₃O⁺ | moyenne | Partie « réaction d'un acide / d'une base avec l'eau » (`td_p4_eau`, `td_p5_ammoniac`) placée avant le pH ; blocs `td_s1_b2` / `td_s1_b3` refaits (questions et cahier échangés en suivant les diapos). Le prof garde l'autre ordre ; les deux tiennent. |
| 4. H₃O⁺ jamais construit ; option H₃O⁺ en diapo 7 | moyenne | `td_b3b_eau` construit H₂O + H⁺ → H₃O⁺ (voix + carte + puce) ; option de `td_b1_acide` remplacée par « Le proton H⁺ seul », réactions réécrites. |
| 5. « équilibre » employé avant 27 | moyenne | En 20-23 la voix dit « la concentration finale » et annonce « éq, expliqué bientôt » (la simulation écrit [H₃O⁺]éq, non modifiable ici) ; `td_e3_etat` dit « l'équilibre, c'est ce que veut dire éq ». |
| 6. τ d'une base en 16 | moyenne | Phrase, puce et geste retirés de `td_p5_ammoniac`. |
| 7. Sens inverse avant sens direct, dilution non dite | moyenne | Ordre inversé : `td_e1b_direct` puis `td_e1_inverse` ; expérience du prof (même solution A dans deux béchers : + acide pur, puis + éthanoate de sodium). |
| 8. Dosage jamais enseigné (2024 R) | moyenne | Diapo ajoutée `td_n4_prepa_dosage` avant l'énoncé (montage `acides-bases-tableau/dosage.html?vue=montage` du ch13 ; volume V_A + V_B ; réaction de dosage rapide et totale). |
| 9. ⇌ employé de 15 à 23 sans explication | moyenne | **Laissé en partie** : les simulations (hors de mes fichiers) écrivent ⇌ dès la diapo 9. La voix annonce en 15 « pour l'instant un simple signe », en 17 « cette réaction s'arrête avant la fin : c'est le début du sens de la double flèche », en 28 « maintenant nous avons compris son sens ». |

Ajouts au passage : `td_n1_enonce_p2` et `td_n1_enonce_p3` n'étaient dans aucun bloc ; ajoutés au bloc `td_n_b1` à leur
place. Les blocs de la séance 4 (`td_s3_b2`, sujet 2019 N) restent avant ceux de la séance 5 (2021 R) alors que les diapos
sont dans l'autre ordre : c'était déjà le cas, laissé.

**Diapos ajoutées (3)** : `td_r1_tableau`, `td_r2_limitant`, `td_n4_prepa_dosage` (toutes avec une simulation déjà
existante). **Déplacées** : `td_o2_flacons` (3 → 16), `td_p4_eau` et `td_p5_ammoniac` (avant le pH), `td_e1b_direct` avant
`td_e1_inverse`. La question de `td_b1_acide` passe en réserve (sinon question en diapo 6). La diapo `td_e1_inverse`
prend la vue `equilibre.html?vue=double_fleche&depart=sens_1` (sens 2 en rose) : l'ancienne vue montrait l'expérience à
l'acide chlorhydrique, contraire à l'expérience du prof ; son observation (afficheur 2,3 → 3,6) est retirée. Une vue
« deux béchers » de la solution A serait à ajouter à `equilibre.html` (hors de cette tâche).

### Notions importantes (règle 55)

27 annonces, toutes différentes (banque et phrases du même style) ; chaque notion clé a une deuxième façon de la dire
(« بطريقة أخرى », image, exemple). Rappels ajoutés dans une diapo suivante qui l'utilise : ampholyte (`td_p4_eau`,
`td_p5_ammoniac`, fiche), réaction acido-basique (`td_p4_eau`), n = C·V (`td_a1_tableau`, `td_a3_xf`), réactif limitant
(`td_a2_xmax`), définition de τ (`td_e5_esterification`), les deux flacons (`td_p6_totale`, `td_a5_totale`), dilution
C₀V₀ = C₁V₁ et étalonnage (`td_d1_dilution`), v₁ = v₂ et la base avec l'eau (fiche), méthode des flacons (`td_n1a_equation`),
dosage (`td_n4_dosage`).

### Tuteur humain (règle 56)

- Débuts de voix : « دابا » 39 % → aucun mot au-delà de 8 % ; 0 diapo qui suit avec le même premier mot ; les cinq énoncés
  du national commencent chacun autrement.
- Liens avec la diapo d'avant (« شفنا… », « عرفنا… », « تفكر… ») et touches humaines (étonnement devant le résultat,
  « خديتي الوقت ديالك ؟ مزيان », fautes fréquentes nommées) une ou deux par bloc.
- Réactions : 38 débuts répétés (« لا، هادي ماشي هي », « مزيان، الجواب صحيح », « ولا يهمك »…) remplacés par des débuts
  variés (« بالضبط ! », « هادا هو ! », « قريب من الفكرة… », « هادي غلطة كيديرها بزاف ديال التلاميذ، عادي »…), le reste
  de la réaction (ce qui est juste, l'idée qui coince) gardé.

### Symboles mal lus

Aucun relevé pour ce cours. `nombres_fr.convertir` : 0 texte à convertir dans l'attente.

## Pistes à générer

77 pistes (`voix_a_generer/…json`) : 52 diapositives et 25 réactions ou énoncés (nouveaux ou au texte changé ; `audio`
retiré). En plus, non voisées aujourd'hui (fin de bloc et réserve de fin de cours) : 60 réactions de bloc
(`blocs_hors_voix`) et 2 réactions de la réserve de `td_b1_acide`.

## Mots douteux pour la voix (`verifier_mots.py` sur l'attente)

Nouveaux mots darija rares remplacés (خديها, نكتشفوه, صغرات, يتبعنا, الميزان, نحلوها, المقاس, معناه, تفاعلش, كتكملش, أداة,
كيوجد, سطور, قسنا, كيقارن, متنكر, كتتبع, كنخلطو, كنصبو, نفسروها, ضاعش, تلفنا, تبعني, كتبدلش…). Restent à écouter :
- termes du programme ou du sujet : loupe, oxonium, éthanoate, ampholyte, ammonium, iodure, soude, indicateurs colorés,
  étalonnage, flacon(s), afficheur, siemens / millisiemens (« mènsse »), benzoate, benzoïque, propanoïque, palier ;
- darija déjà dans l'ancien texte ou peu fréquent : كتسالى, كيتسالاو, أتاي, كونهم, استهلكهم, كنرينسيو, نفرضو, كيتحيدو,
  للور, كنكتبوها, كتعطي (dosage), فخ.

## Vérifications (servi et attente)

`verifier_formules.py` : 0 ; `verifier_parcours.py` : rien ; `verifier_pointage.py` : 0 défaut ;
`verifier_pointage_simulations.py` : servi 24 écarts « GESTE » (déjà là), attente 0 écart hors « GESTE » (les « GESTE » de
l'attente viennent des pistes sans audio : durée 0, recalculés à la génération) ; `verifier_figures_cahier.py` : 0 erreur.

## Cours de référence du prof

Lu : `reference-prof/README.md` et `reference-prof/phys_ch11_transformations_deux_sens.md`. Corrections recommandées :

1. Énigme des flacons après le pH : **fait** (`td_o2_flacons` en diapo 16, après le pH-mètre).
2. Rappel du tableau, x_max, réactif limitant, tableau à deux lignes finales : **fait** (deux diapos de rappel ; deux
   lignes finales dites en `td_a3_xf` avec une carte, et ajoutées au tableau du cahier du bloc `td_s2_b1`).
3. Expérience des deux sens comme le prof (même solution, acide pur puis éthanoate de sodium) : **fait** pour la voix,
   l'écran et le cahier ; la simulation ne montre que les équations (vue « béchers » à créer, hors tâche).
4. → provisoire jusqu'à 26 : **non fait** — les simulations écrivent ⇌ ; la voix explique que c'est un signe provisoire
   et le relie en 17 et 28.
5. Phrase de liaison en 27 et « éq » à partir de là : **fait** (voix, carte, puce, cahier du bloc `td_s2_b3`) ; « éq » reste
   écrit par la simulation en 20 (annoncé dans la voix).
6. Diapo 17 : pH attendu 2,0 = pH de l'acide chlorhydrique : **fait** ; repris en `td_a5_totale`.
7. Diapos 38-39 : explication par K au chapitre suivant : **fait** (`td_d2_taux`, `td_d3_nature`). Le rappel en ch12
   diapo 48 est hors de ce cours.
8. Diapo 14 : indicateurs colorés : **fait** (voix et puce de `td_p3_phmetre`).

Point où le prof ne confirme pas l'audit : H₃O⁺ avant le pH (défaut 3). Gardé (acide + eau avant le pH), les deux ordres
tenant selon la référence.
