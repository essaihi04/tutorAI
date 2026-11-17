## Rôle du muscle strié squelettique dans la conversion de l’énergie

Fichier modifié : `backend/data/courses/en_attente/svt_ch2_role_muscle_strie_squelettique.json`. Je suis parti de la copie en attente et je n'ai rien perdu de ce qu'elle contenait. Le cours en ligne n'a pas été touché. Le cours passe de 55 à 60 diapos.
Script de la passe : `scratchpad/svt2c/build.py`. Copie d'avant : `scratchpad/svt2c/avant.json`.

### Manques corrigés

| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| H : myofibrilles isolées avec salyrgan et chélateur (MSS9) | Nouvelle diapo. Principe, T₁ Ca²⁺ + ATP, T₂ salyrgan, T₂ chélateur : une ligne au centre par étape avec son « car », puis la conclusion. Courbe de tension au cahier (diapo et bloc). | **ms_c1c_myofibrille** (bloc ms_s4_b1, C6) |
| H : preuve que l'excitation libère le Ca²⁺ | Nouvelle diapo avant ms_c2. Tableau ⁴⁵Ca²⁺ (lot relâché / lot contracté, d'après 2016 N), puis l'équorine comme 2ᵉ preuve. Le réticulum sarcoplasmique est défini. Conclusion écrite. | **ms_c2a_calcium_libere** (bloc ms_s4_b2, C6) |
| H : la tête de myosine est une ATPase, plus active dans l'actomyosine | ms_u7 : « site ATPasique » écrit et dit. ms_c4 : 3 lignes au centre (actine seule : 0 ; myosine seule : faible ; actomyosine : forte), voix, puces, cahier et cahier du bloc. | ms_u7_molecules, ms_c4_rotation |
| H : Chauveau et Kaufmann (sang entrant / sortant) | Nouvelle diapo avant ms_t4, avec le tableau des valeurs de K p6 (sang, O₂, CO₂, glucose, lipides 0, protides 0). Rapports calculés, « car oxydation du glucose », conclusion, origine du glucose (sang et glycogène, avec l'équation). | **ms_t4a_sang** (bloc ms_s2_b3, C3) |
| H : schéma de synthèse (cadre 1.3) | Nouvelle diapo après la carte. Figure « schema » au cahier (Ca²⁺ → actomyosine → ATP → ADP + Pi ; PC ; glycogène → acide pyruvique → acide lactique ; mitochondrie), avec les lieux et les bilans d'ATP. | **ms_b3_synthese** (bloc ms_s5_b3, C9) |
| H : réserve d'ATP chiffrée | Valeurs de A p13 (vérifiées sur la page) : 4 à 6 mmol/kg = 0,17 à 0,25 kJ/kg ; 100 m = 4,4 kJ/kg ; 4,4/0,25 ≈ 17,6 ; marche 0,31 kJ/kg. Centre ligne par ligne, voix, puces, cahier. | ms_r1_reserve |
| M : chaleur de contraction + chaleur de relâchement ; thermopile | Ajoutées aux puces, au cahier, au cahier du bloc et à la voix. | ms_t1_chaleur_initiale |
| M : sommation (et les mots « partielle / totale ») | Écrit dans les puces, le cahier, le cahier du bloc et l'`attendu` du retrouver. | ms_f2, ms_f3 |
| M : excitabilité et contractilité | Puce, cahier, cahier du bloc et une phrase de voix. | ms_s2_secousse |
| M : contenu de la fibre (sarcolemme, sarcoplasme, mitochondries, glycogène, RS, myoglobine), striation longitudinale, tailles | Puces, cahier, voix, et un schéma de la fibre légendé au cahier (diapo et bloc ms_s3_b1). | ms_u2_fibre |
| M : erreur « une tête » → « une tige et deux têtes » | Corrigé dans le titre, le sous-titre, les puces, la voix et le cahier. Le pointage passe sur « و deux têtes. ». ms_u8 : puce « une tige + deux têtes ». | ms_u7, ms_u8 |
| M : Ca²⁺ repompé par transport actif | Puce, cahier, voix et `attendu` du retrouver de ms_s4_b3 (« le relâchement consomme aussi de l'ATP »). | ms_c6_relachement |
| M : hydrolyse du glycogène | (C₆H₁₀O₅)ₙ + n H₂O → n C₆H₁₂O₆ : dite et écrite en ms_t4a, écrite en ms_r4, au bilan et au cahier du bloc. | ms_t4a, ms_r4, ms_b1 |
| M : reconstitution de la PC après l'effort | C + ATP → PC + ADP, avec l'ATP qui vient de la respiration : centre, voix, puce, cahier et bilan. | ms_r6_relais, ms_b1 |
| M : effort d'intensité croissante | Nouvelle diapo après ms_r6, avec le tableau de K p6-7. Le O₂ plafonne à 3,04 L/min, puis l'acide lactique monte (1,985 → 37,66 g/L), et le « car » de chaque déduction. Les mots « VO₂max » et « seuil anaérobie » ne sont pas écrits. | **ms_r6b_intensite** (bloc ms_s5_b1, C8) |
| M : courbe de fatigue et sa cause | Puces, cahier et voix (arrêt ; acide lactique, pH, 2 ATP). Courbe de fatigue au cahier (diapo et bloc ms_s2_b2). | ms_f7_fatigue |
| B : pivotement, pont actomyosine, attachement | Synonymes entre parenthèses. | ms_c3, ms_c4, ms_c7 |
| B : supraliminaire / infraliminaire | Puces, cahier et cahier du bloc. | ms_i1_seuil |
| B : striation longitudinale, tailles (fibre 10-100 µm, myosine 16 nm, actine 5 nm) | Ajoutées à l'écrit. | ms_u2, ms_u4, ms_u1 |
| B : les trois tracés M, S et T (chronographe) | Puce, cahier et cahier du bloc ; « signal du temps » est dit en ms_s5. | ms_s1, ms_s5 |
| Notions dites seulement à l'oral | Écrites : « unité structurale et fonctionnelle » (ms_u3) ; valeurs du dosage et définitions du glycogène et de la PC (ms_t4) ; thermopile (ms_t1) ; réticulum sarcoplasmique (ms_u2, ms_c2a) ; reconstitution de la PC (ms_r6) ; « assez forte pour faire répondre le muscle » (ms_s6) ; « la contraction la plus forte » (ms_f5) ; ordres de grandeur (ms_u1) ; la rupture de la liaison du dernier phosphate est déjà au cahier de ms_o2. | voir colonne 1 |
| Notations | « zone H (ou bande H) », « PC (ou CP) », « fusion partielle / totale », « pivotement », « pont actomyosine ». | ms_u5, ms_r2, ms_f2, ms_f3, ms_c3, ms_c4, ms_c7 |
| Bilans écrits en entier, avec le lieu et l'ATP | Fermentation : hyaloplasme, 2 ATP par glucose. Respiration : hyaloplasme puis mitochondrie, « 36 ou 38 ATP par glucose ». PC : hyaloplasme, 1 ATP par PC. Le tableau de ms_r7 a une colonne « Lieu ». Les formules du bilan et du bloc sont complètes. Rappel C7_r4 : « 36 ou 38 ». | ms_r2, ms_r4, ms_r5, ms_r7, ms_b1, ms_b3, blocs |
| Formules (`verifier_formules`) | « 5 / 2 » → « 5/2 » (explication et réactions de ms_s4_b4). | bloc ms_s4_b4 |

### Non corrigés et pourquoi

- **Manques chez un seul professeur** : non faits. Aucun n'est exigé par le cadre. L'expérience de Hopkins est déjà couverte par ms_r8 (muscle 3).
- **Angle ≈ 45° des têtes** : non écrit. L'audit le classe lui-même hors cadre (« angles 90° → 50° → 45° »).
- **Simulations non modifiées** (consigne « pas de nouvelle simulation ») :
  - `chaleur.html` montre une seule bosse. La voix de ms_t1 dit qu'elle couvre la contraction puis le relâchement.
  - `calcium.html?vue=etiquettes` (ms_u8) n'a pas d'étiquette « tige » : la tige n'est écrite que dans les puces.
  - Les 5 nouvelles diapos sont **sans visuel**. Elles utilisent un tableau, les lignes du centre et une figure du cahier, car aucune vue existante ne convient. Pour ms_c2a, `calcium.html?vue=acces` aurait gardé la même iframe que ms_c2.
- **ms_r8** : « glycogène et acide lactique inchangés » n'est pas écrit. Notre document reconstitué (`inhibiteurs.html`) ne donne pas ces valeurs.
- **ms_c1c** vient après ms_c1b, qui porte la question du bloc ms_s4_b1 : la question n'est donc plus sur la dernière diapo du bloc. Je ne l'ai pas déplacée, car son énoncé et ses réactions sont enregistrés.
- **« 36 ou 38 »** : les voix de ms_r5 et ms_r7 et les paroles des réactions de C7_r4 disent encore « trente-six ». Ce n'est pas faux, mais c'est incomplet. Je ne les ai pas changées (l'écran suffit) : à décider.
- **Hors audit, à signaler** : l'exercice du bloc ms_s4_b2 est la copie exacte de celui de ms_s4_b1.
- **⁴⁵Ca (2016 N)** : le corrigé recopié chez K dit « faible radioactivité au niveau du sarcoplasme » pour le lot contracté, ce qui contredit sa propre déduction. Notre tableau écrit la version cohérente : forte dans le sarcoplasme. C'est qualitatif, sans valeurs.

### Démonstrations

- **Relues : les 6 `demonstration` existantes, plus toutes les preuves écrites sur les diapos et au cahier. Réécrites ou créées : 10 `demonstration`.**
  - Réécrites : t4 (q), r8 (q), blocs s1_b2, s4_b3, s4_b4.
  - Créées pour des questions de calcul ou de déduction qui n'en avaient pas : blocs s2_b1, s2_b2, s2_b3, s3_b3, s5_b1.
  - Preuves écrites ligne par ligne au centre, une entrée par ligne : ms_s5, ms_g2, ms_c1b, ms_r1, ms_x3, et les nouvelles ms_t4a, ms_c1c, ms_c2a, ms_r6b, ms_b3.
  - Gardées telles quelles : bloc s3_b2 (demi-bande claire, déjà complète).
- Exemples avant → après :
  - ms_t4 : « muscle a travaillé → ATP constant → PC baisse → régénéré » devient : ATP consommé, « car » hydrolyse (équation) ; ATP 5,0 → 4,8 ; glycogène ↓ et acide lactique ↑ = fermentation ; O₂ ↑ et CO₂ ↑ = respiration ; PC ↓ ; consommé mais constant ; conclusion = réponse « correct ».
  - ms_r8 : « glycolyse bloquée → PC chute → alactique » (3 lignes) devient 7 lignes : méthode (témoin) ; ni fermentation ni respiration du glucose ; PC ↓ fortement et ATP constant ; car PC + ADP → C + ATP ; le muscle 3 confirme (ATP épuisé, arrêt) ; l'ATP est la source directe ; réponse.
  - ms_s5 : « latence 0,01 s ; contraction 0,04 s ; relâchement 0,05 s » devient : instants lus ; durée = fin − début ; 0,01 − 0 ; 0,05 − 0,01 ; 0,10 − 0,05 ; 0,10 − 0, chaque fois avec l'unité (même chose pour ms_g2 : 2,5 − 2,0, 1,0 − 0,5, 0,5 − 0 et 1,5 − 1,5, puis la chaîne « A constante car longueur de la myosine »).
- Tous les calculs sont refaits en python : 4,61 ; 16,8 ; 27,0 ; 4,13 ; 17,6 ; 25,9 ; 0,04 ; 0,05 ; 0,06 ; 0,5 ; 0,4 ; 2,5 ; 0,01 < 0,03 < 0,05 ; 0,05 < 0,08 < 0,11.

### Voix à enregistrer (id)

- **Diapos (18, audio retiré)** :
  - voix changée : ms_s2_secousse, ms_s5_mesures, ms_f7_fatigue, ms_t1_chaleur_initiale, ms_u2_fibre, ms_u7_molecules, ms_g2_mesures, ms_c1b_essais, ms_c4_rotation, ms_c6_relachement, ms_r1_reserve, ms_r6_relais, ms_x3_hypothese ;
  - nouvelles : ms_t4a_sang, ms_c1c_myofibrille, ms_c2a_calcium_libere, ms_r6b_intensite, ms_b3_synthese.
- **Démonstrations (parole)** : ms_t4_consomme (q), ms_r8_inhibiteurs (q), blocs ms_s1_b2, ms_s2_b1, ms_s2_b2, ms_s2_b3, ms_s3_b3, ms_s4_b3, ms_s4_b4, ms_s5_b1.
- **Énoncé** : rappel C7_r4 (`enonce_dit` changé, `enonce_audio` retiré).

### Vérifications faites (résultats)

- `json.load` : OK. Écriture avec ensure_ascii=False, indent=2, LF (0 CR). Le fichier a été relu juste avant l'écriture (hash identique à la lecture).
- Chaque `mot` des lignes de démonstration est dans sa `parole`, dans l'ordre. Chaque `mot` de pointage et de centre est dans `speech_text.mixed` : 0 absent.
- Chaque diapo est dans exactement un bloc : 0 hors bloc, 0 doublon. Chaque competence_id existe.
- `verif_attente.py` : 60 diapos, 0 mot absent, 0 hors bloc, 18 diapos sans voix (celles listées ci-dessus).
- `verifier_formules.py` : 0 relation à reprendre (5 avant).
- `verifier_figures_cahier.py` : 13 figures, 0 erreur, 0 avertissement.
- `verifier_pointage.py` : 0 défaut.
- Voix et paroles nouvelles : aucun chiffre, aucun symbole (= + / → × % ² ₂ ⁺), pas de tachkil.
- `git status` : seul le fichier en attente du ch2 est modifié de mon côté.
