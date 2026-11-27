# phys_ch5_energie_nucleaire — corrections de l'audit pédagogique (26-27/11/2026)

Règles 52 à 56 du skill professeur, sans rien raccourcir, sans générer de voix.

- **Phase 1** (cours servi `backend/data/courses/phys_ch5_energie_nucleaire.json`, aucune voix changée) : commit `7d28f05e`.
- **Phase 2** (copie d'attente `backend/data/courses/en_attente/phys_ch5_energie_nucleaire.json`, refaite à partir du
  cours servi après la phase 1 et la revue des cahiers `8b0991df` ; l'ancienne copie d'attente est remplacée).
- Pistes à générer : `docs/audit-pedagogie/voix_a_generer/phys_ch5_energie_nucleaire.json` — **259 pistes**
  (49 diapositives, 210 réactions ou énoncés), format de `scripts/voix/pistes_changees.py`.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| | Diapos | Questions 6 premières | Formules dites non écrites | Passages ≥ 60 mots sans geste | Notions clés | redites | annoncées (mots-clés ≠) | Premier mot le plus fréquent | Suites même premier mot | Tournures ≥ 5 diapos |
|---|---|---|---|---|---|---|---|---|---|---|
| Avant (servi, 26/11) | 59 | 2 | 73 | 9 | 23 | 9 (39 %) | 0 (0) | « دابا » 27 % | 3 | 6 |
| Après phase 1 (servi) | 59 | 0 | 29 | 0 | 26 | 9 | 0 (0) | « دابا » 27 % | 3 | 6 |
| Après phase 2 (attente) | 60 | **0** | 19 | **0** | 28 | **27 (96 %)** | **24 (86 %)** (15) | « هاد » **5 %** | **0** | 6 |

- Les 19 « formules dites non écrites » qui restent sont toutes dans les **lectures d'énoncés** du national : la feuille du
  sujet (`shared/examen/feuille.html`) les montre déjà ; rien à écrire en plus.
- Annonces : les 24 phrases d'annonce sont **toutes différentes** ; l'audit ne compte que 15 mots-clés distincts parce que
  sa liste de motifs n'en a que 14 en darija sans tashkil (+ 7 en français) : plusieurs phrases différentes partagent un
  mot-clé (« ركز معايا, هنا la fission بالأرقام » / « هاد الجزء كاين بزاف فle national، ركز معايا »).
- Les 6 « tournures recopiées » sont des nombres (« neuf cent trente et un virgule cinq », « un u égale ») : laissées.
- Réactions : premier mot le plus fréquent avant « مزيان » 93, « لا » 91, « شوف » 80 sur 314 ; après « قريب » 28, « خليني » 26.

## Phase 1 — cours servi, sans toucher au texte parlé
1. **Premier bloc** `en_s1_b0` (diapos 1-4, questions posées après la diapo 4) fondu dans `en_s1_b1` : la première question
   de bloc vient après la diapo 7. Ses deux questions (puissances de dix, 10⁻¹⁹ × 10⁶) remplacent le **doublon** de
   `en_s4_b3`, qui répétait mot pour mot celles de `en_s4_b2` (on garde `en_s4_b2`, placé après la leçon).
   Les autres blocs ont été vérifiés : aucune question sur une notion enseignée après (vrai-faux de `en_s1_b2` et
   `en_s2_b2` compris : ils portent sur des notions déjà vues).
2. **Aucune question dans les 6 premières diapos** : les questions de `en_p2_puissances` (diapo 4) et `en_m2b_un_gramme`
   (diapo 6) passent en `exercices_fin_de_cours` avec leurs réactions, leur énoncé dit et leur démonstration (voix gardées).
3. **Dit = écrit** : 56 gestes (cartes `centre` écrites au mot, `play_until` déplacés sur le mot de la formule, `highlight`
   sur la ligne déjà écrite) sur 22 diapos : `en_p2_puissances`, `en_m2_einstein` (E = m·c² s'écrit à son mot, plus au
   nom d'Einstein), `en_m2b_un_gramme`, `en_m3_unites`, `en_m3b_electronvolt`, `en_m4b_energie_masse` (6 cartes au mot,
   la diapo n'a pas de figure), `en_d3_formule` (la formule s'écrit à « إذن delta m égale »), `en_l2_former`,
   `en_l3_calcul`, `en_s2_piege`, `en_a2_zones`, `en_a3_comparer`, `en_r5_soddy`, `en_b2b_energie`, `en_b4_fission_calcul`,
   `en_b5_beta`, `en_e2_formule`, `en_e4_polonium`, `en_n1_echantillon`, `en_n1b_energie_totale`, `en_n3_2025`,
   `en_c2_qcm2019`, `en_fermeture_cours`. 73 → 29 formules non écrites (énoncés seulement), 9 → 0 passages sans geste.
4. **Erreurs d'écran** : tous les calculs des écrans et des cartes ont été refaits (u, 931,5, E₀ du proton, Δm, E_ℓ,
   E_ℓ/A, bilans 2016 N, 2017 R, 2020 N, 2022 N, 2023 N, 2019 N, 2025 N, échantillon) : aucune erreur.

## Phase 2 — copie d'attente
### Ordre des notions (règle 52, `ordre-des-notions/phys_ch5_energie_nucleaire.md`)
| # | Défaut | Fait |
|---|---|---|
| 1 (forte) | Diapos 25, 44, 51 : N_A lu « newton ampère », m lu « mètre », ᴬ_Z e lu « Ag », N_d sans « sur » ni « ln » | Lectures refaites (voix et `fr`) : « le nombre d'Avogadro، N A، égale six virgule zéro deux fois dix puissance vingt-trois par mole », « la masse de Cd cent sept », « une particule e، de nombre de masse A et de nombre de charge Z », « N d égale a zéro fois t un demi، sur huit ln deux » ; aussi « g.mol puissance moins un » → « grammes par mole », « E ell (MeV) » → « en méga électron volt », « MeV.c puissance moins deux » → « méga électron volt par c au carré », « t un sur deux » → « t un demi », « gamma (gamma) », « \ a- ». Un « E ell » dans une réaction de rappel (C7_r3) corrigé aussi. |
| 2 | Nucléon et ᴬ_Z X utilisés (diapos 7, 10) avant le rappel du noyau (diapo 11) | `en_d1_composition` **déplacée** juste après `en_m2b_un_gramme` (bloc `en_s1_b1`, une ligne de cahier « Rappel : ᴬ_Z X… »), et rappelée au début de la balance (« تفكر: النواة فيها Z protons… »). |
| 3 | Diapo 8 : eV, MeV et MeV/c² ensemble | **Coupée** : `en_m3b_electronvolt` garde eV et MeV ; **nouvelle diapo** `en_m3c_mev_c2` (MeV/c² unité de masse, m = E/c², redite et relecture), sur la vue existante `figures.html?fig=fig_unites&depart=MeV`. |
| 4 | Énoncé 2022 R (diapo 14) demande E_ℓ avant sa définition | La voix dit que la question 2 sera faite après l'énergie de liaison ; la diapo 15 dit « غادي نعرفوها فالجزء الجاي، دابا غير الخطوة اللولة ». |
| 5 | 23-24 : fusion/fission nommées sans cause | Phrase-cause (« le noyau الجديد مربوط كثر: l'énergie de liaison اللي ربح هي اللي كتخرج ») et annonce « بالتفصيل من بعد ». |
| 6 | Diapo 28 parle du neutron non repoussé avant le rappel des charges (diapo 30) | `en_p3_charges` **déplacée** avant `en_r2_fission` (bloc `en_s2_b3`, ligne de cahier déplacée) ; elle finit sur le neutron sans charge ; `en_r2_fission` et `en_r4_fusion` le rappellent. |
| 7 | Kelvin jamais présenté | « dix puissance huit kelvins، يعني environ cent millions de degrés Celsius. le kelvin هو وحدة أخرى ديال la température » (+ « réaction thermonucléaire », voir le cours du prof). |
| 8 | Δm d'une réaction confondu avec le défaut de masse | Dit dès la ligne 2 de `en_b2_methode`. |
| 9 | Diapo 47 : paliers d'énergie de masse non expliqués ; passage MeV → u → kg jamais montré | La voix dit que chaque niveau porte l'énergie de masse m·c², pas une énergie de liaison, et montre une fois Δm = E_ℓ/931,5 (en u) puis × 1,66·10⁻²⁷ (en kg), écrit au mot (carte) avant l'exercice. |

Défaut trouvé en passant : la voix et l'écran de `en_a3_comparer` et `en_e3_2023` numérotaient le sujet 2023 N « 2-1 a,
2-1 b, 2-2 » alors que la feuille du sujet (`exams/physique/2023-normale/exam.json`) dit **5.a, 5.b, 6** : corrigé dans la
copie d'attente (voix, titre, écran, cahier), pas dans le cours servi pour ne pas contredire sa voix.

### Notions importantes (règle 55)
- **Annonce** avant 24 des 28 notions clés, chaque fois une phrase différente (banque + nouvelles : « والجاي هو القلب ديال
  الدرس كامل », « حل عينيك مزيان على السبورة », « سمعني مزيان، هادي غادي تحتاجها ديما », « وقف معايا شوية، حيت الجاي
  جديد », « بغيتك تحفظ هاد العدد مزيان », « جات اللحظة المهمة ديال هاد الجزء », « خلي كلشي على جنب شوية، وتبع معايا »,
  « هاد السؤال مهم بزاف فle national », « هنا المهم فهاد الجزء كامل », « c'est important », « le plus important فهاد
  السطر », « إلى كانت شي حاجة غادي تبقى فراسك من هاد الجزء »…). Non annoncées (applications) : `en_m4b_energie_masse`,
  `en_l3_calcul`, `en_b1_masse_diminue`, `en_n1b_energie_totale`.
- **Deuxième façon de dire** ajoutée dans 18 diapos clés (27/28 en ont une) : image (la part de chaque nucléon d'un pain
  partagé, monter pour casser / descendre pour construire), contre-exemple (un gros noyau a une grande E_ℓ parce qu'il a
  beaucoup de nucléons) ou relecture « نعاود نقرا » de la formule, écrite à son mot.
- **Rappel plus tard** (« تفكر… », « اللي لقينا قبل شوية ») : noyau (balance), nucléon (u), u et MeV (931,5), MeV/c²,
  931,5 (calcul de E_ℓ), définition de E_ℓ (E_ℓ/A), règle de stabilité (Aston), charges (fission, fusion), définitions
  fission/fusion (Soddy, balance), ΔE = Δm·c² (balance), méthode des masses (fission), |ΔE| (2016 N), ordre des E_ℓ (2023 N),
  N de l'échantillon. Pas de rappel ajouté pour le pouvoir de pénétration (une seule diapo l'utilise ; il reste au bilan écrit).

### Tuteur humain (règle 56)
- Débuts de voix : plus aucun mot sur plus de 5 % des diapos, aucune diapo qui suit avec le même premier mot ; les huit
  lectures d'énoncés commencent et finissent chacune autrement (« خود معايا الورقة… », « تفكر الموضوع… »,
  « آخر l'énoncé فهاد الدرس… »).
- Liens et touches humaines : « شوف هاد الحاجة، غريبة شوية! » (balance), « أنا عارف أن هاد الحساب كيبان طويل، ولكن
  الخلاصة ساهلة » (E_ℓ = Δm·c²), « فهمتي la formule؟ مزيان » (calcul de E_ℓ), « النتيجة كتبان بالمقلوب » (fission ou fusion).
- Réactions : 283 réactions (diapos, fin de cours, rappels des compétences, blocs) commencent autrement — ouvertures de la
  banque tournantes (« بالضبط! », « هادا هو! », « قريب، ولكن ماشي هو. », « فهمت علاش ختاريتي هادا، ولكن شوف معايا. »,
  « هادي غلطة كيديرها بزاف ديال التلاميذ، عادي. »…) ; le corps de chaque réaction est gardé : les réactions « 1 » nommaient
  déjà ce qui est juste dans le choix, les réactions « 2 » donnent la réponse et sa raison. Les réactions de blocs (non mises
  en voix pour l'instant, `FIN_DE_BLOC_COMPLETE = False`) ne sont pas dans la liste des pistes.

## Cours de référence du prof (`reference-prof/phys_ch5_energie_nucleaire.md`)
Ajouté (copie d'attente, voix et écran) :
1. Lectures fautives des diapos 25, 44, 51 (correction 1).
2. Rappel du noyau avant u : diapo déplacée (solution de l'audit, équivalente à celle du prof) (correction 2).
3. Diapo 6 : le sens inverse « masse qui augmente → énergie reçue Δm·c² », dit et écrit (carte, écran) (correction 3).
4. Diapo 8 coupée en deux (correction 4).
5. Diapo 17 : « E_ℓ ديما positive : هي l'énergie اللي كنعطيوها للنواة باش نفرقوها » (correction 5).
6. Diapos 23-24 : phrase-cause et annonce (correction 6, ordre gardé comme chez le prof).
7. Rappel des charges avant la fission (correction 7).
8. Diapo 31 : kelvin expliqué et nom **« réaction thermonucléaire »** (voix et écran) (correction 8). Contrôle : le mot
   n'est ni dans `cadre_reference_2bac_pc.json` ni dans `perimetre.json`, ni dans leur liste hors cadre ; c'est un autre nom
   de la fusion (notion du cadre, EN5) ; aucun sujet du national de la banque ne l'emploie. Le kelvin n'est pas hors cadre.
9. Diapo 35 : Δm d'une réaction ≠ défaut de masse (correction 9).
10. Diapo 41 : l'électron entre dans Δm et son énergie de liaison est nulle (correction 10).
11. Bilan (diapo 57) : réaction en chaîne (centrale / bombe) et zones de la courbe d'Aston, dites et écrites (correction 11).

Laissé : l'effet biologique propre à chaque rayonnement (le prof le dit lui-même facultatif, absent des sujets) ; la
plage 8-9 MeV/nucléon (notre plafond de contrôle 8,8 est juste) ; le découpage du bilan d'énergie (le nôtre, plus lent, est
gardé, comme le recommande la comparaison).

## Laissé, et pourquoi
- Les 19 formules d'énoncés « non écrites » : écrites sur la feuille du sujet.
- `verifier_pointage.py` : les 9 défauts du départ (moments de `rappels.html` construits à l'exécution, ils existent bien) ;
  aucun nouveau.
- `verifier_pointage_simulations.py` sur la copie d'attente : 112 « gestes trop serrés » — sans piste audio, le script
  place un geste par seconde ; à relancer quand les voix seront posées (le cours servi en a 1, celui du départ).
- Énoncé 2022 R : la question 2 reste lue à son endroit (la feuille du sujet la montre) ; la voix renvoie à plus tard.

## Mots douteux pour la voix (`verifier_mots.py`, mots ajoutés par la phase 2)
« bombe » (0), « thermonucléaire » (0), « Einstein » (1), « خبزة » (1), « غريبة » (1), « جنب » (2), « نفرقوها » (2) ;
à écouter aussi : « kelvins », « c'est important », « le plus important » (français dans une phrase darija). Les autres mots
rares listés par le script étaient déjà dans les mêmes pistes avant.

## Vérifications (copie d'attente et cours servi)
`verifier_formules.py` 0 · `verifier_parcours.py` rien · `verifier_figures_cahier.py` 0 erreur · `verifier_pointage.py`
9 (départ) · `nombres_fr.py` 0 · ordre des diapos = ordre des blocs (60/60).
