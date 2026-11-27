# Corrections — phys_ch8_circuit_RLC (26-27/11/2026)

Règles 52 à 56 du skill professeur ; audit `../ordre-des-notions/phys_ch8_circuit_RLC.md`, mesures `../mesures.md`,
cours de référence du prof `../reference-prof/phys_ch8_circuit_RLC.md`. Rien n'est raccourci, aucune voix générée.

- **Phase 1** (cours servi `backend/data/courses/phys_ch8_circuit_RLC.json`, voix inchangée) : commit 7c3bcd5d, plus l'écran de la diapo 8 dans 30d79718.
- **Phase 2** (copie d'attente `backend/data/courses/en_attente/phys_ch8_circuit_RLC.json`, refaite depuis le cours servi après la phase 1 et la revue des cahiers 9c751966) : commit 30d79718.
- Pistes à générer : `../voix_a_generer/phys_ch8_circuit_RLC.json` — **117 pistes** : 83 diapos (80 au texte changé + 3 nouvelles) et 34 réactions.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| | Diapos | Questions dans les 6 premières | Formules dites non écrites | Passages ≥ 60 mots sans geste | Notions clés | redites | annoncées (motifs ≠) | Premier mot le plus fréquent | Diapos de suite, même premier mot | Débuts répétés | Réactions au même début |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Avant | 93 | 2 | 182 | 22 | 29 | 9 | 0 (0) | « دابا » 25 % | 15 | « نفس التمرين » ×18 | 5 × « لا، هاد الجواب ماشي هو. شوف، » |
| Servi après phase 1 | 93 | 0 | 102 | 0 | 37 | 9 | 0 (0) | « دابا » 25 % | 15 | (voix inchangée) | (inchangé) |
| Copie d'attente | 96 | 0 | 109 | 0 | 38 | **38** | **38 (15)** | « دابا » **5 %** | **0** | — | — |

- Annonces : 38 notions clés sur 38 annoncées, **38 phrases d'annonce toutes différentes** (mesuré à part) ; le script n'en
  compte que 15 « différentes » car il compte le motif reconnu (« ركز معايا », « تبع معايا »…), pas la phrase.
- « Formules dites non écrites » : il en reste 109 ; ce sont presque tous des faux positifs du motif (voir plus bas). Le
  nombre monte de 102 à 109 parce que la phase 2 ajoute des phrases (redites, rappels) qui contiennent « égale ».
- Premiers mots : le plus fréquent est « دابا » sur 5 diapos sur 96 ; jamais deux diapos de suite avec le même premier mot.

## Phase 1 — sans changer la voix (cours servi)

1. **Questions de bloc déplacées après leur leçon** (défauts 5, 7, 10, 13 de l'audit) :
   - `lc_s2_b0.retrouver` (équation en q, enseignée diapo 23) → `lc_s2_b1` [20-23] ;
   - `lc_s2_b0.exercice` (coefficient 1/(LC), diapo 24) → `lc_s2_b1b` [24-25] ; en échange `lc_s2_b0` reçoit l'exercice
     « trois périodes durent 12 ms » (déjà enseignable : diapos 12 et 17) ;
   - `lc_s2_b1b.retrouver` (U_m et T du cosinus, diapo 26) → `lc_s2_b2a` [26-28] ;
   - `lc_s2_b3.retrouver` (« L en fonction de T₀ et C ») supprimé : **doublon** de `lc_s3_b2.retrouver`, placé après la méthode (diapo 48) ;
   - `lc_s2_b3.exercice` (2022 N, calcul de L) → `lc_s2_b3b` [33-36], après la diapo 36 qui le résout ;
   - `lc_s3_b1.exercice` (i part de 0 en descendant → φ) → `lc_s3_b1b` [40-42], après la règle du sens de départ (diapo 41).
   Une seule question « À toi » par bloc partout.
2. **Aucune question dans les 6 premières diapos** : la question de `lc_rp2_bobine` (diapo 4) va dans ses
   `exercices_fin_de_cours` (réactions dans `reponses_fin_de_cours.e0`, voix gardées) ; l'observation de `lc_d2_bobine`
   (diapo 6) est retirée : la même question est déjà dans ses `exercices_fin_de_cours`, et la voix dit la réponse juste après.
3. **Dit = écrit** : 54 cartes `centre` ajoutées sur 24 diapos (chaque relation, conversion et application numérique à la phrase
   qui la dit), 31 gestes `pointage` (17 diapos) posés sur la ligne que la simulation écrit déjà (`repere` des figures du national, de
   `equation.html`, `solution.html`, `periode.html`, `energie.html`) ou sur la carte relue (`cible: centre:N`).
   `lc_rp2_bobine` écrit maintenant u_b = L·di/dt + r·i à sa première phrase et la baguette revient dessus à la relecture.
   Plus aucun passage de 60 mots sans geste (22 avant ; `lc_e8_T0`, `lc_c5_courant`, `lc_c1_depart` compris).
4. **Écran** : diapo 8, « les oscillations sont amorties … oscillateur libre et amorti » et « le condensateur et la bobine se
   l'échangent » retirés des puces (dits à la diapo 12 et au bloc de l'énergie) ; remplacé par « Tout vient du condensateur chargé au départ ».

### Laissé en phase 1, et pourquoi
- **Formules restantes du script (~100)** : les énoncés lus du national (diapos `*_enonce*`) sont affichés en entier par la feuille
  d'examen (`feuille.html`), et la baguette pointe la question lue ; les étapes intermédiaires d'un calcul dont la ligne
  complète est déjà écrite (par une carte ou par la figure) à quelques mots près ; les simples valeurs de l'énoncé
  (« r égale zéro ») dans le national pas à pas, que la figure `national-pas-a-pas.html` écrit à son étape « rappel ».
- **Première question de bloc après la diapo 4** (`lc_s0_b1`) : c'est la question du bloc des rappels, posée après sa
  dernière diapo comme le veut la règle 27 ; la mesure « 6 premières » porte sur les diapos et vaut 0.
- **Défaut 4 (diapo 17, C ÷ 4 → T ≈ 2 ms)** : défaut partiellement faux. La diapo montre C × 4 → T × 2 juste avant, et la
  démonstration de la question raisonne par symétrie (× 4 → × 2 donc ÷ 4 → ÷ 2) sans la racine. Gardé.
- **Défaut 16 (énoncés lus par morceaux, dans le désordre)** : réordonner les feuilles d'examen demanderait de recouper les
  sujets (`feuille.html?questions=…`) et de rejouer les questions ; laissé. En phase 2, la diapo 9 dit en une phrase que
  diodes et démodulation viennent dans d'autres cours.
- Avertissements déjà présents avant nous (inchangés) : `verifier_pointage.py` ne lit pas les moments d'`entretien.html` et
  de `national-pas-a-pas.html` (ils existent dans le code, kit commun) ; `IFRAME`/`DEPART` de `verifier_pointage_simulations.py`
  sur les diapos d'entretien et de bilan ; trois blocs du cahier de plus de 19 éléments.

## Phase 2 — texte parlé (copie d'attente)

Les numéros de diapo sont ceux de l'audit (cours de 93 diapos) ; la copie d'attente en a 96.

### Ordre des notions (règle 52) — trois diapos de rappel ajoutées
| Nouvelle diapo | Place | Défaut | Visuel |
|---|---|---|---|
| `lc_rp0_periode` « Rappel : l'amplitude et la période » | après `lc_rp2_bobine` (diapo 5), bloc `lc_s0_b1` | 1 (forte avec le prof) | vue existante `dipole-rc-tableau/rappels.html?vue=sinusoide` (la formule en cos s'écrit, la voix dit « on y reviendra ») |
| `lc_rp5_derivee_seconde` « Rappel : dériver deux fois » (position → vitesse → accélération, puis q → i → d²q/dt²) | avant `lc_e0c_tout_en_q`, bloc `lc_s2_b1` | 6 (forte) | vue existante `rappels.html?vue=derivee` (voiture, compteur) |
| `lc_rp6_cercle` « Rappel : le cercle trigonométrique » (radian, sin 0 = sin π = 0, cos(±π/3) = 0,5, cos(π/2) = 0) | avant `lc_c1_depart`, bloc `lc_s3_b1` | 8, 12 | **aucune vue ne convient** (le point de `rappels.html` tourne avec la hauteur = cosinus, à l'opposé du cercle trigonométrique) : `visual.kind: none` et cinq cartes `centre` |

Autres corrections d'ordre (fortes et moyennes) :
- défaut 2 : diapo 8 ne dit plus que le condensateur et la bobine « échangent l'énergie » (« tout vient du condensateur chargé ») ;
  « amorties » est dit diapo 12 avec sa cause, l'effet Joule ;
- défaut 3 : diapo 12, règle « durée = nombre de divisions × sensibilité » avec un exemple (deux divisions × deux ms = quatre ms) ;
- défaut 8 : diapo 27, φ se mesure en radian et dit où en est la courbe à t = 0 ;
- défaut 9 : diapo 28, la dérivée du sinus est le cosinus (2π/T sort devant) ;
- défaut 11 : diapo 36, une phrase explique « élever au carré puis diviser » pour isoler L, et la diapo 48 rappelle ce calcul
  (la diapo 48 n'a pas été déplacée : elle s'appuie sur la suite de l'énoncé 2020 N lue juste avant elle) ;
- défaut 14 : la diapo 40 n'a pas été changée (énoncé lu tel qu'à l'examen) ; le générateur G est expliqué à sa place, diapo 62 ;
- défaut 15 : diapo 42, « −sin est la courbe du cosinus en avance d'un quart de période » ;
- défaut 16 (partiel) : diapo 9, « les diodes et la démodulation, on les verra dans des cours suivants ».

### Notions importantes (règle 55)
- 38 notions clés : chacune ouverte par une **annonce différente** (« وقف معايا شوية هنا… », « هادي هي القلب ديال الدرس… »,
  « جات اللحظة المهمة… », « بغيتك تحفظ هاد الجملة… », « فخ معروف، تبع معايا. »…), avec une **deuxième façon** de la dire
  (« بمعنى آخر », « بطريقة أخرى », « بكلمة أخرى », « يعني بالدارجة », « نعاودها », « عاود معايا », « نقولها بطريقة ساهلة »).
- Rappels plus loin (« تفكر… », « شفنا قبل… ») : la période (8, 26), la dérivée seconde (23), le terme d'amortissement (25, 63),
  le cercle (37, 39), T ≈ T₀ annoncé en 30 puis vérifié en 46, la méthode du carré (48), l'effet Joule (55), l'équation du circuit (58).

### Tuteur humain (règle 56)
- Débuts de voix : les 24 énoncés commencent chacun autrement (« أول مرة فهاد الدرس نقراو… », « نرجعو ل le national… »,
  « باقي التمرين ديال le national… »…) et leur fin « دابا نفهمو التمرين خطوة بخطوة » varie (8 formules) ; les fins
  « خود الوقت ديالك، ومن بعد جاوب » des questions du national pas à pas varient (8 formules) ; dans la voix, « le national
  deux mille … » remplace « الامتحان الوطني deux mille … » (plus de mot darija collé au nombre).
- Touches humaines : surprise (diapo 6 « شوف شنو وقع هنا! »), difficulté partagée (« هنا بالضبط فين بزاف ديال التلاميذ
  كيديرو الغلط »), encouragement (« ما تخافش من الطول ديالو، كل سؤال شفناه قبل », « خديتي الوقت ديالك؟ مزيان، هكا خاص »),
  raison (« هاد الدارة هي اللي كتختار la station فالراديو »).
- Réactions : 39 réactions réécrites au début, qui nomment ce qui était juste dans le choix (« فكرتي فالفرق ديال l'énergie،
  وهادا صحيح، ولكن الحساب تلف », « زوين، حيدتي les deux courbes بالمنطق »…) ; plus aucun début de 6 mots sur 4 réactions.

### Symboles et mots mal lus corrigés dans les réactions
« 0 ديال u R … 0 ديال u b » → « zéro … » ; « 5 volts » → « cinq volts » ; « dayman » → « ديما » ; « لـ nano » → « ل nano » ;
« وU deux » → « و U deux » ; « خمستاشر ohms » → « quinze ohms ». `scripts/voix/nombres_fr.py` : 0 nombre darija à côté du français.

### Mots douteux pour la voix (ajoutés, vus moins de 3 fois dans le corpus — à écouter)
« station », « كتختار » (diapo 2, la radio), « compteur » (diapo de rappel de la dérivée, déjà dit dans le cours RC),
« الخزانات » (image des réservoirs, diapo 54 — déjà dite dans le cours RC). Les mots rares déjà présents avant nous dans les
mêmes pistes (énoncés du national : « informatisé », « adéquat », « bascule »…) n'ont pas été touchés.

### Vérifications (copie d'attente)
`verifier_formules.py` 0 ; `verifier_parcours.py` rien ; `verifier_pointage.py` : aucun nouveau défaut (seulement des
« moment non lu statiquement » pour les deux nouvelles vues de `rappels.html`, qui existent) ; `verifier_pointage_simulations.py` :
nouveaux `GESTE` dus à l'absence d'audio (l'instant est estimé sans durée de piste ; à revoir quand la voix existera) et
`DEPART` sur les deux nouvelles diapos à simulation, comme la diapo de rappel du cosinus déjà en ligne ;
`verifier_figures_cahier.py` : seulement les avertissements anciens.

## Cours de référence du prof — appliqué / laissé
| # | Correction recommandée | Fait | Où |
|---|---|---|---|
| 1 | Diapo 12 : T = nombre de divisions × sensibilité avec un exemple ; « amorties » avec sa cause (effet Joule) | appliqué | voix diapo 12 (attente) |
| 2 | Diapo 8 : seulement « libres » ; retirer « amorties » et « se l'échangent » | appliqué | écran (servi + attente), voix (attente) |
| 3 | Rappel sinusoïde / amplitude / période avant la diapo 6 | appliqué (nouvelle diapo `lc_rp0_periode`, sans formule dite) | attente |
| 4 | Rappel dérivée seconde avant la diapo 22 | appliqué (`lc_rp5_derivee_seconde`) | attente |
| 5 | Le terme en dérivée première est celui de l'amortissement, dès l'équation | appliqué diapo 24 (voix + carte), rappelé diapos 25 et 63 | attente |
| 6 | Annoncer T ≈ T₀ si l'amortissement est faible | appliqué diapo 30 (voix + carte), vérifié diapo 46 qui le rappelle | attente |
| 7 | Diapo 58 : si R + r = 0, dE/dt = 0, l'énergie se conserve | appliqué (voix + carte) | attente |
| 8 | La radio comme porte d'entrée (diapo 2 ou 8) | appliqué diapo 2 (« هاد الدارة هي اللي كتختار la station فالراديو ») | attente |
| 9 | Ne pas ajouter le régime critique | respecté (rien ajouté, ni filtres) | — |
| 10 | Garder les autres corrections de l'audit | appliquées sauf diapo 48 non déplacée (voir défaut 11 ci-dessus) et énoncés non réordonnés (défaut 16) | — |
