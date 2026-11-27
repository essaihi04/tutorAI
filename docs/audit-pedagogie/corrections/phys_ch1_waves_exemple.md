# phys_ch1_waves_exemple — corrections de l'audit pédagogique (26-27/11/2026)

Règles 52 à 56 du skill professeur ; audit `../ordre-des-notions/phys_ch1_waves_exemple.md` et `../mesures.md` ;
cours de référence du prof `../reference-prof/phys_ch1_waves_exemple.md`. Rien n'est raccourci, aucune voix générée.

## Phase 1 — cours servi `backend/data/courses/phys_ch1_waves_exemple.json` (aucun texte parlé changé)

- **Aucune question avant la 7ᵉ diapo** : la question ouverte de la diapo 4 (« redis la définition ») est retirée (elle
  doublait le « retrouver » du bloc). Le bloc `wx_s1_b1` (diapos 1-4) garde son cahier mais plus de question : son
  « retrouver » (la définition) passe au bloc `wx_s1_b2` (après la diapo 7), son exercice (le bouchon : énergie sans
  matière) passe au bloc bilan `wx_s4_b3`.
- **Doublon de bloc** : l'exercice du bloc bilan `wx_s4_b3` était mot pour mot celui de `wx_s4_b1c` (placé après la
  leçon, gardé) ; remplacé par le bouchon. Le « retrouver » du bilan (retard + condition, déjà demandé en `wx_s1_b3`)
  est remplacé par l'ancien « retrouver » de `wx_s1_b2` (transversale / longitudinale).
- Les autres questions de bloc portent sur des notions déjà enseignées dans le bloc ou avant : vérifié, rien à déplacer.
- **Dit = écrit** : cartes ajoutées à leur mot (`wx_r2b_dates` τ = SM/v ; `wx_m1b_lecture` 1 ms = 10⁻³ s ;
  `wx_m2_sonar` aller d + retour d → 2d) ; baguette sur la carte à la relecture (`wx_c1_celerite`, `wx_r1b_elongation`,
  `wx_fermeture_cours`).
- Défauts « dit sans être écrit » laissés car faux : les 11 diapos d'énoncé (la feuille du sujet affiche le texte lu),
  les corrections des nationaux (`national.html` écrit les lignes de calcul au `play_until` qui précède la phrase),
  le bilan (`bilan.html` écrit chaque point à son `play_until`).
- Écran : « une modification **locale** et temporaire » dans la carte « Perturbation » de la diapo 3 (cours du prof).
- Vérifié : `verifier_formules` 0, `verifier_parcours` rien, `verifier_pointage` 8 défauts (les mêmes qu'au départ),
  `verifier_pointage_simulations` sans nouveau défaut, `verifier_figures_cahier` 0 erreur.

## Phase 2 — copie d'attente `backend/data/courses/en_attente/phys_ch1_waves_exemple.json`

Repartie du cours servi après la phase 1 (l'ancienne copie d'attente, périmée, est remplacée).

### Ordre des notions (règle 52) — défauts de `ordre-des-notions`
| # | Défaut | Fait |
|---|---|---|
| 1 (fort) | courbes y(t), y(x) lues avant d'être enseignées | `wx_l1_aspect` déplacée AVANT le retard (début de la partie III, bloc `wx_s1_b3`) ; elle ne parle plus de τ et θ comme acquis (« on les lira ensuite ») ; sa question en voix sans widget est retirée |
| 2 (fort) | diapo 6 : cinq notions | diapo 6 = ressort + exception seulement (redite « file de personnes ») ; le son reste à la diapo 7 ; **nouvelle diapo `wx_i3d_dimension`** (vue `types.html?depart=corde`, repères dim_corde / dim_eau / dim_son déjà existants) |
| 3 (fort) | pente k = 1/v jamais rappelée | **nouvelle diapo `wx_n4_rappel_droite`** avant l'énoncé 2021 R (carte simple : aucune vue existante ne montre une droite par l'origine hors de l'exercice lui-même) ; la correction reprend « Δt = d/v donc k = 1/v » |
| 4 | élongation dans la 1ʳᵉ diapo | retirée de la diapo 3 (et de son cahier de bloc), définie au début de `wx_l1_aspect`, juste avant le retard (carte « Élongation y ») |
| 5 | « homogène » jamais expliqué | phrase ajoutée diapo 9 (« pareil partout : même matière, même tension ») |
| 6 | amplitude employée avant d'être définie ; élasticité / inertie | amplitude définie au moment où on frappe plus fort ; une image par notion (l'élastique, l'objet lourd) |
| 7 | y_S(t − τ) sans exemple ; M₁M₂ dans la même diapo | exemple chiffré (τ = 0,2 s : à 0,5 s M fait ce que S faisait à 0,3 s) + réciproque dite et écrite ; **nouvelle diapo `wx_r1c_deux_points`** (vue `corde.html?vue=retard`, M₁ joue le rôle de S) |
| 8 | oscilloscope jamais présenté | **nouvelle diapo `wx_p3_oscilloscope`** avant le TP (carte simple : la seule vue d'oscillogramme est celle du TP lui-même) |
| 9 | diapo 21 : hertz, audible, ultrasons, salve, réflexion | **nouvelle diapo `wx_m2a_ultrasons`** (hertz, 20 Hz – 20 kHz, ultrasons ; carte simple) ; le sonar garde réflexion et 2d, « salve = un court paquet d'ultrasons » dit et écrit |
| 10 | « sinusoïdale de fréquence N » (énoncé 2022 R) | phrase ajoutée après la lecture : « on les verra au prochain chapitre ; ici seulement le retard » |

Notions dites une seule fois, maintenant redites ou rappelées : domaine audible (nouvelle diapo + rappel au sonar),
réciproque y_S(t) = y_M(t + τ) (dite), méthode de l'aspect à une date t (rappelée en `wx_l2_sens`), r = v·t
(relu à la correction 2024 N), toutes les directions offertes (diapo dimension), distance réelle = mesurée × échelle
(dite et écrite diapo 9), le son ne se propage pas dans le vide (relu diapo 7, bilan, carte).

### Notions importantes (règle 55) et tuteur humain (règle 56)
- 38 diapos clés : chacune annoncée juste avant par une phrase différente (38 phrases, toutes distinctes ; 13 « noyaux »
  différents au sens du motif de `audit_pedagogie.py`), redite autrement dans la diapo (« بطريقة أخرى … », exemple,
  image) et relue (« نعاود نقرا ») ; rappel dans une diapo suivante (« تفكر … », « شفنا … », « كيف شفنا فle rappel »).
- Débuts de voix variés : plus aucun premier mot au-dessus de 10 % (« شفنا » et « قبل » 5 diapos sur 58), aucune diapo
  qui suit avec le même premier mot ; les 11 énoncés et les 7 corrections ont chacun leur ouverture et leur fin.
- Réactions : 77 réactions préparées et 54 énoncés dits de questions avaient des débuts recopiés (« شوف هاد السؤال »,
  « الجواب الصحيح هو », « مزيان، صحيح. », « ما تقلقش ») : débuts variés (banque de phrases).
  Limite : seul le début change ; le corps de chaque réaction (ce qui est juste dans le choix) reste celui des réactions
  préparées, qui le nommaient déjà en général.
- Touches humaines ajoutées (une ou deux par bloc) : « أنا عارف أن هاد الكتابة كتبان صعيبة… », « شوف هاد الحاجة،
  غريبة شوية… », « علاش كنقراو هادي؟ … », « هادي كتخلط بزاف ديال التلاميذ ».
- Symboles mal lus : aucun relevé dans ce cours (les erreurs de lecture signalées concernent ch2, ch3, ch5).

### Cours de référence du prof (`reference-prof/phys_ch1_waves_exemple.md`)
| Correction recommandée | Fait |
|---|---|
| 1. couper la diapo 6 en trois | fait (voir défaut 2 ci-dessus) |
| 2. diapo « superposition » | **laissée** : hors cadre. `perimetre.json` (motif « superposition de deux ondes » → « hors programme : on étudie une onde unique ») et la fiche ondes de `cadre_reference_2bac_pc.json` la rangent dans les mots hors cadre. Pas ajoutée au bilan ni à la carte non plus |
| 3. tableau des deux directions côte à côte | **nouvelle diapo `wx_i3e_comparer`** après les expériences du son : `types.html` (corde, ressort, son, eau), chaque case jouée et pointée à son mot, tableau à l'écran, relecture de la méthode. Pas de question ajoutée (une seule question par bloc : celle du bloc `wx_s1_b2`) |
| 4. élongation avant le retard ; « locale » | fait (voir défaut 4) ; « locale » dans la voix et la carte de la diapo 3 |
| 5. pourquoi « célérité » ; homogène | fait (diapo 9 : « rien de matériel n'avance, seule la perturbation ») |
| 6. diapo 11 : la règle générale d'abord ; amplitude | la règle (ni la forme, ni la durée, ni la force) est dite en ouverture, puis les facteurs du milieu ; la démonstration de la manip reste à sa place (ordre des `play_until` de `milieux.html`) |
| 7. « l'air se comprime puis se dilate, tranche après tranche » | fait (diapo 7, voix) |
| 8. « densité » de l'énoncé 2018 N | phrase ajoutée après la lecture : c'est la règle solide > liquide > gaz |
| 9. bilan et carte : le son pas dans le vide (+ superposition) | le vide : ajouté au bilan et à la carte ; superposition : non (hors cadre) |
| v = √(T/µ) (remarque du prof) | non ajoutée : hors cadre (`cadre_reference_2bac_pc.json`, mots hors cadre de la fiche ondes) |

### Diapos ajoutées ou déplacées (52 → 58)
Ajoutées : `wx_i3e_comparer`, `wx_i3d_dimension`, `wx_r1c_deux_points`, `wx_p3_oscilloscope`, `wx_m2a_ultrasons`,
`wx_n4_rappel_droite`. Déplacée : `wx_l1_aspect` (de la partie IV au début de la partie III). Blocs et cahiers de
blocs mis à jour (ligne « Élongation » et lignes de lecture des courbes passées au bloc du retard, ligne dimension
après le son, lignes oscilloscope et droite ajoutées).

## Pistes à générer
`docs/audit-pedagogie/voix_a_generer/phys_ch1_waves_exemple.json` (format de `scripts/voix/pistes_changees.py`) :
**123 pistes** — 54 diapositives (6 nouvelles, 48 au texte changé : ouvertures, annonces, redites) et 69 réactions /
énoncés de questions de diapo. L'`audio` de chaque diapo et réaction changée est retiré. Les énoncés et réactions des
blocs ont aussi des débuts variés mais ne sont pas mis en voix (`pistes_cours.FIN_DE_BLOC_COMPLETE = False`).

## Mesures (`scripts/audit/audit_pedagogie.py`)
| | Diapos | Questions 6 premières | Formules dites non écrites | Passages ≥ 60 mots sans geste | Clés | redites | annoncées (noyaux ≠) | Premier mot | Suites même premier mot | Tournures recopiées |
|---|---|---|---|---|---|---|---|---|---|---|
| avant | 52 | 1 | 41 | 0 | 30 | 12 (40 %) | 1 (1) | « دابا » 48 % | 13 | 5 |
| servi après phase 1 | 52 | 0 | 34 | 0 | 31 | 12 | 1 (1) | « دابا » 48 % | 13 | 5 |
| attente après phase 2 | 58 | 0 | 25 (toutes des énoncés lus sur la feuille) | 0 | 38 | 38 (100 %) | 38 (13), 38 phrases différentes | « شفنا » 9 % | 0 | 1 (« l'énoncé ديال الامتحان الوطني deux mille ») |

Vérifications de la copie d'attente : `verifier_formules` 0, `verifier_parcours` rien, `verifier_pointage` 0 défaut,
`verifier_figures_cahier` 0 erreur, `nombres_fr.py` 0. `verifier_pointage_simulations` : aucun défaut REPERE / MOMENT /
IFRAME / DEPART ; ses « gestes trop serrés » viennent de l'absence de piste (durée 0 sur les 54 diapos sans voix),
à recontrôler une fois la voix posée.

## Mots douteux pour la voix (nouveaux dans les textes changés, `verifier_mots.py` sur la copie d'attente)
Vus 0 à 2 fois dans le corpus : الثقيلة (1), بعضياتو (1), بقاتش (2), تعطلات (2), تلفنا (2), جبدناه (2), دفع (1),
طبقة (2), عليش (2), غريبة (1), فالسبيطار (1), كتخلط (2), كتسنى (1), كتطيح (2), كتنفعك (1), كيطيحو (2), نحتاجوه (2),
نفهموه (2), والدفعة (1), وللور (2). Termes du programme gardés exprès : salve, ultrasons, amplitude, oscilloscope.
Phrases nouvelles à faire écouter à l'utilisateur (règle de la banque de phrases).
