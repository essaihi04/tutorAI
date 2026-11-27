# phys_ch10_cinetique — corrections de l'audit pédagogique (26-27/11/2026)

Cours servi : `backend/data/courses/phys_ch10_cinetique.json` (phase 1, sans toucher la voix ; poussée en f7b7fda4,
puis fusionnée avec la revue du cahier et les repères de synchro de l'amont).
Copie d'attente : `backend/data/courses/en_attente/phys_ch10_cinetique.json` (phase 2, texte parlé ; refaite sur le
servi actuel, cahiers et repères de l'amont gardés). Pistes à générer : `docs/audit-pedagogie/voix_a_generer/phys_ch10_cinetique.json`.
Rien n'est raccourci : 85 diapos → 87 (deux diapos ajoutées), aucune phrase de contenu retirée.

## Mesures (`scripts/audit/audit_pedagogie.py`)

| Version | Diapos | Questions 6 premières | Formules dites non écrites | ≥ 60 mots sans geste | Notions clés | redites | annoncées (mots-clés ≠) | Premier mot | Suites même 1ᵉʳ mot | Débuts répétés | Tournures ≥ 5 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Départ (servi d'origin/main) | 85 | 1 | 80 | 9 | 34 | 13 | 0 (0) | « دابا » 33 % | 13 | « دابا غادي » ×11, « نفس التمرين » ×9 | 6 |
| Servi après phase 1 | 85 | 0 | 49 | 1 | 35 | 13 | 0 (0) | « دابا » 33 % | 13 | idem | 6 |
| Copie d'attente (phase 2) | 87 | **0** | 49 | 1 | 37 | **37 (100 %)** | **37 (14)** | « ها » **6 %** | **0** | — | 6 |

- **Annonces toutes différentes** : 37 notions clés, 37 phrases d'annonce entières toutes différentes (vérifié par un
  script : la phrase qui contient l'annonce, dans les 25 premiers mots de la diapo). La colonne de l'audit affiche 14 :
  elle compte le *mot-clé* reconnu par la regex `ATTENTION` (« ركز معايا », « تبعني », « هادي مهمة »…, une quinzaine
  possibles), pas la phrase ; deux annonces différentes qui contiennent toutes deux « ركز معايا » y comptent pour une.
- Les 49 « formules dites non écrites » restantes sont surtout dans les énoncés du national (la feuille d'examen les
  écrit déjà : faux positifs), et des données lues dans les diapos d'exercice déjà à 4 cartes.
- Les 6 « tournures recopiées » restantes viennent des textes officiels des sujets (« T représente la tangente à la »,
  « l'avancement x en fonction du temps ») et des unités (« millimoles par litre et par minute ») : on ne les change pas.
- Le passage ≥ 60 mots restant : `ci_n8_trempe` (sujet 2017 R), inchangé.

## Phase 1 — cours servi, sans changer la voix

1. **Questions de bloc** : `ci_s1_b2` (après le tableau, diapo 11) et `ci_s1_b2b` (après le titrage, diapo 17)
   échangent leurs questions : x_max / réactif limitant après le tableau, titrage n(I₂) = C·V_E/2 après le titrage.
   Doublons : `ci_s2_b1b`/`ci_s2_b1c` et `ci_s3_b1`/`ci_s3_b1b` posaient la même question ; l'exercice (qui reprend
   la diapo suivante, 29 et 44) reste dans le bloc placé après cette diapo, le « retrouver » dans le bloc d'avant
   (notion déjà enseignée) : une seule question par bloc, jamais avant la leçon.
2. **Aucune question dans les 6 premières** : la question de la carte (diapo 2, t₁/₂ au national) passe dans la
   réserve de fin de cours de la carte finale (`ci_cr_carte.exercices_fin_de_cours`, réactions dans
   `reponses_fin_de_cours.e0`, voix et audios gardés).
3. **Dit = écrit** : cartes `centre` ajoutées au mot exact (m = ρ·V et l'exemple de l'eau ; n_E = C·V_E ; calcul du
   prélèvement et × 10 ; σ = Σλ[X] développée ; σ_f ; application numérique de x ; x_max par la pression ;
   V(H₂) = 24 mL ; 2016 R x = x_max/2 au mot dit ; dx/dt = −dn/dt et pente → v(0) ; règle des mesures ≪ t₁/₂ ;
   V = 10 mL = 0,010 L ; 10⁻³ − x_max = 0 au mot dit ; t₁/₂ = 4 min ; v₁ ≈ 0,78 ; conversions de λ et de C) et
   pointages vers une carte ou un repère déjà écrit pour les relectures. Mot faux corrigé : `ci_p2_relation` pointait
   la relation x = (P − P₀)V/RT sur « deu**x égale P moins P zéro** » (P(H₂) = P − P₀) ; le repère `lecture_VE` de
   `ci_m3b_calcul` passe sur « V E égale douze virgule six millilitres ». Passages sans geste : 9 → 1.
4. **Erreurs d'écran** : deux questions d'observation partaient sur un `apres_mot` absent de la voix
   (`ci_n2_diminue`, `ci_n6b_demi`) : remis sur la phrase réelle. Les 2 erreurs « 4 et 3 figures par bloc »
   (`ci_s4_b1`, `ci_s4_b2`) ont disparu avec la revue du cahier de l'amont.

## Phase 2 — copie d'attente (texte parlé)

### Ordre des notions (`ordre-des-notions/phys_ch10_cinetique.md`)
| # | Défaut | Fait |
|---|---|---|
| 1 | `ci_s1_b2` interroge sur le titrage | phase 1 |
| 2 | 2016 R (30-32) lit t₁/₂ et la tangente avant de les enseigner | Les sujets **2016 R (30-32) et 2024 N (38-39)** passent après « comparer deux t₁/₂ » (53), en tête des sujets du national (nouveau bloc `ci_s4_b0`, avec l'exercice 2016 R σ = 207 mS/m de l'ancien bloc `ci_s2_b3`). 2024 N avait le même défaut (sa question est t₁/₂, et « la tangente, on l'utilisera plus tard ») : ajouté. Les renvois « on verra plus tard » deviennent des rappels (« t un demi اللي تعلمنا »). |
| 3 | Palier sous x_max et « équilibre » jamais expliqués | Nouvelle diapo `ci_n2b_non_totale` avant 2017 N (carte simple, sans figure : aucune vue existante ne montre un palier sous x_max avant le sujet) ; rappels en 2017 N et 2017 R. |
| 4 | Rappel de la pression après le ballon | `ci_z6_gaz` avant `ci_p1_ballon`. |
| 5 | Catalyseur jamais défini | Phrase + carte en `ci_v8_temperature` (accélère, absent de l'équation, même état final) ; rappel en 2023 N. |
| 6 | « facteurs cinétiques » en 12 sans rappel | Phrase en `ci_m2_trempe`. |
| 7 | Diapo 3 explique avec x, dosage, σ | `ci_o2_methodes` déplacée après le réactif limitant, en tête de la séance 2 (voir aussi la référence du prof). |
| 8 | Question à l'ouverture | phase 1 |
| 9 | x_max en 10 avant son calcul | La diapo 10 nomme seulement x_max (« la valeur maximale… on la calcule à la diapo suivante ») ; laissé partiel : la simulation `avancement.html` écrit « x_max » sur la ligne état final, la voix doit dire ce qui est écrit. |
| 10 | Couples + addition dans la même diapo | Coupée : `ci_z4b_couples` (couples, demi-équations) puis nouvelle `ci_z4c_addition` (addition ; carte simple, comme la diapo d'origine qui n'avait pas de figure). |
| 11 | V_m jamais expliqué | Phrase et carte en `ci_p3_volume`, avant son usage. |
| 12 | Conductance avant « ions → courant » | `ci_g2_ions` avant `ci_g1_cellule` ; `ci_g2_ions` parle de « conductivité » sans σ (σ est posé à la diapo suivante). |
| 13 | « totale » sans son contraire | Phrase en `ci_a7_palier`. |

### Notions importantes (règle 55)
37/37 notions clés : annonce différente avant, deuxième façon de le dire dans la diapo (« بمعنى آخر », « بعبارة أخرى »,
« بكلمة أخرى », « نقولها بطريقة ساهلة »…), rappel dans une diapo suivante qui l'utilise (« تفكر la relation
ديال l'équivalence », « la loi des gaz parfaits اللي تفكرنا », « تفكر la trempe », « تفكر le palier », « تفكر les deux
courbes », « تفكر l'exemple B », etc.).

### Tuteur humain (règle 56)
- Débuts de voix : « دابا » 33 % → premier mot le plus fréquent « ها » 6 % ; 0 diapo de suite avec le même premier mot ;
  les énoncés ne commencent plus tous par « دابا غادي نقراو l'énoncé… » ni les suites par « نفس التمرين… » / « دابا نقراو
  الجزء الموالي » ; chaque diapo s'ouvre par un lien avec la précédente ou par ce qu'on voit.
- Touches humaines (une ou deux par bloc) : « أنا عارف أن هاد الحساب كيبان طويل… », « شوف هاد الحاجة، غريبة شوية »,
  « deux pièges كيطيحو فيهم بزاف ديال التلاميذ، عادي، ولكن نتا لا », « واخا يكون الدرس طويل شوية… ».
- Réactions : 75 réactions changent leurs premiers mots (« لا، هادي ماشي هي » ×70 → cinq ouvertures ; « مزيان، » juste →
  « بالضبط / صافي / زوين / هو هادا » ; « شوف، الجواب ديالك » → « سمع، … » une fois sur deux) ; la suite, qui nomme déjà ce
  qui est juste dans le choix, est gardée. « Mzyan » écrit en lettres latines corrigé.
- Symboles mal lus : aucun relevé pour ce cours. Nombres darija collés au français : passés par `nombres_fr.convertir`
  (« جوج demi-équations » → « deux demi-équations », etc.) ; 0 restant.

## Cours de référence du prof (`reference-prof/phys_ch10_cinetique.md`)
| Correction recommandée | Fait |
|---|---|
| 1. 2016 R : t₁/₂ après la diapo 53 | Fait (tout le sujet, et 2024 N). |
| 2. Définir le choc efficace en 47 | `ci_v6_epuisement` : « deux entités doivent se heurter assez fort pour casser leurs liaisons : choc efficace ; trop faible, elles se séparent : choc inefficace », carte au mot, puce d'écran ; redit en 49. |
| 3. Température : plus de chocs ET plus énergiques | `ci_v8_temperature` : voix, puce d'écran. La phrase pour ch9 diapo 29 n'est pas faite (autre cours, autre session). |
| 4. Diapo 3 : noms des méthodes en tête, explication après 11 | Les noms des trois méthodes restent annoncés en tête par la carte (diapo 2) ; leur explication (`ci_o2_methodes`) est après la diapo 11. |
| 5. Définir « cinétique chimique » | Diapo 2 (carte), avec la porte d'entrée du prof : « certaines réactions sont lentes, on veut savoir où elles en sont ». |
| 6. Rappel « facteur cinétique » en 12 | Fait. |
| 7. 33 ↔ 34, V_m avant 36 | Fait. |
| 8. Cas « σ augmente » | `ci_p5_choisir` (diapo 37) : phrase + carte « si des ions se forment : σ monte depuis ≈ 0, x = x_max·σ/σ_f ». |
| 9. Temps de réponse des appareils, rappel de la diapo 37 en 53 | `ci_h4_comparer` : phrase + carte ; `ci_p5_choisir` annonce « on affinera ce choix avec t₁/₂ ». |
| 10. Carte catalyseur avec 49 | Fait (voir défaut 5). |
| (hors liste) question « à quoi sert l'empois d'amidon ? » en 13 | Laissée : la diapo 13 a déjà la question de son bloc (une seule par bloc, règle 27). |

## Diapos ajoutées / déplacées
- Ajoutées : `ci_z4c_addition` (après `ci_z4b_couples`), `ci_n2b_non_totale` (avant `ci_n3_enonce`).
- Déplacées : `ci_o2_methodes` (3 → 12, bloc `ci_s1_b1`) ; `ci_g2_ions` ↔ `ci_g1_cellule` ; `ci_z6_gaz` ↔ `ci_p1_ballon` ;
  `ci_p4_enonce`, `ci_p4_enonce_p2`, `ci_p4_2016R`, `ci_p6_enonce`, `ci_p6_2024N` → après `ci_h4_comparer`.
- Blocs : `ci_s2_b1c` fusionné dans `ci_s2_b1b` (avec `ci_g6_calcul` et son exercice) ; `ci_s2_b3` fusionné dans
  `ci_s2_b2` (avec `ci_p5_choisir`) ; nouveau `ci_s4_b0` (2016 R, 2024 N) en tête de la séance 6. Le « retrouver »
  de `ci_s2_b3` (x = V(H₂)/V_m) est retiré : son bloc garde déjà le « retrouver » de la pression. Cahiers de l'amont
  gardés, renumérotés (I. Rappels ; III. Suivre une transformation au cours du temps, qui reçoit le principe et le
  tableau des méthodes ; VII. commence au bloc `ci_s4_b0` avec la méthode « t₁/₂ par une relation du sujet ») ;
  `partie` des figures recalée.

## Pistes à générer
152 pistes (`voix_a_generer/phys_ch10_cinetique.json`) : 77 diapositives, 21 réactions de diapos, 54 réactions de
réserve de fin de cours ou de bloc (texte changé, pas jouées aujourd'hui). `audio` retiré de chacune.

## Vérifications (copie d'attente)
`verifier_formules` 0 ; `verifier_parcours` 0 erreur ; `verifier_pointage` 0 défaut ; `verifier_pointage_simulations` :
0 écart hors GESTE (les GESTE sont tous dus à l'absence de piste : sans `duration_ms`, le script place chaque mot à
0 s ; à revoir après la génération) ; `verifier_figures_cahier` 0 erreur, 0 avertissement ; tous les `mot` présents dans
la voix et dans l'ordre.

## Mots douteux pour la voix (`verifier_mots`, mots nouveaux rares dans le corpus)
Termes à garder : « inefficace », « barème », « bulle », « monte » (français). Darija (formes conjuguées de verbes
courants, à écouter) : تبعني، كتطيح، كيطيح، كيطيحو، كيغلطو، كتزرب، كيزرب، يتلاقاو، يتكسرو، يتفاعلو، كيكثرو،
كيتفارقو، كيبانش، كيبدلش، كيبينش، كيطلبهاش، محتاجهاش، نقيسوه، نقراوه، نفهموه، نوضحو، كنكملو، كتعرفها، كتفسر،
كتربح، تفكرنا، حفظنا، غريبة، جنب، أضعف، وحدها. Remplacés car trop rares : سميتك، ودنيك، عييتي، فخاخ، ساليناها،
بطيئات، جاتش، كتطور، زربانة، تزربش، كافياش، باقيين، نلعبوه، العداد، جوابنا، كتبطا، كيتراجعو.
