# Audit des cahiers de fin de bloc (20 novembre 2026)

Branche `claude/audit-cahiers`, partie de `main` (7f545128). Périmètre : les 23 cours de `backend/data/courses/*.json`
qui ont des blocs (`seances[].blocs[]`) ; la copie `en_attente/` n'est pas touchée. Les cours sans blocs
(`chem_ch1_kinetics_course_v1`, `math_ch1_limits_course_v1`, `phys_ch1_waves_course_v1`,
`phys_ch1_waves_mixed_script_v3`, `svt_ch1_energy_course_v1`, `svt_ch1_muscle_course_v1`, `parole_prof`) n'ont pas de
cahier de fin de bloc : rien à vérifier.

## Synthèse

| Cours | Blocs touchés / blocs |
|---|---|
| `math_ch1_limites_continuite` | 24 / 25 |
| `math_ch2_derivation_etude_fonctions` | 26 / 27 |
| `math_ch3_suites_numeriques` | 22 / 23 |
| `math_ch4_primitives` | 19 / 19 |
| `math_ch5_fonctions_ln` | 23 / 23 |
| `math_ch6_nombres_complexes` | 19 / 24 |
| `phys_ch10_cinetique` | 20 / 20 |
| `phys_ch11_transformations_deux_sens` | 14 / 14 |
| `phys_ch12_etat_equilibre` | 15 / 15 |
| `phys_ch13_acides_bases` | 21 / 22 |
| `phys_ch1_waves_exemple` | 17 / 17 |
| `phys_ch2_ondes_periodiques` | 19 / 19 |
| `phys_ch3_ondes_lumineuses` | 23 / 27 |
| `phys_ch4_radioactivite` | 25 / 25 |
| `phys_ch5_energie_nucleaire` | 16 / 16 |
| `phys_ch6_dipole_RC` | 25 / 25 |
| `phys_ch7_dipole_RL` | 22 / 22 |
| `phys_ch8_circuit_RLC` | 24 / 24 |
| `phys_ch9_transformations_lentes_rapides` | 17 / 17 |
| `svt_ch1_reactions_responsables_liberation_energie` | 18 / 20 |
| `svt_ch2_role_muscle_strie_squelettique` | 17 / 21 |
| `svt_ch3_notion_information_genetique` | 24 / 25 |
| `svt_ch4_relation_gene_proteine` | 24 / 25 |

## Méthode

1. **Conformité avec les animations** : pour chaque bloc, lecture des diapositives de `slide_ids` (voix, écran,
   `concentration`, moments joués) et du code de la page `visual.url` (fonctions, valeurs, couleurs des séries,
   phases). Les courbes du cahier ont été recalculées en Python à partir du code de la simulation.
2. **Comparaison avec des cours écrits marocains** (2 ou 3 par chapitre : moutamadris, alloschool, TelmidTice,
   N. Naceiri Mrabti, kezakoo, sigmaths, dyrassa…) : architecture I. / 1. / a), définitions formulées comme au
   national, ordre logique — sans copie mot pour mot.
3. **Découpe en parties** : un titre romain sur sa propre ligne, puis une ligne « n. » qui ouvre chaque partie ;
   numérotation continue d'un bloc à l'autre ; parties de 5 lignes au plus (≤ ~90 caractères) ; champ `partie` sur
   les dessins dont la place n'est pas évidente. Les anciennes lignes du type « II — 1. », « I.1 », « Fin du III — 5. »
   (qui n'ouvraient pas de partie) ont disparu ; les questions d'examen s'écrivent « Question 1.1 » ou « Q2.1 ».
4. Seuls `blocs[].cahier` et `blocs[].cahier_figures` ont changé (contrôle champ par champ contre `main`, format du
   fichier conservé) ; `verifier_figures_cahier.py` → 0 erreur sur les 23 cours. Un commit par cours, qui liste ses
   blocs touchés.

## Exemple signalé (SVT ch1, bloc `le_s1_b2`)

La courbe « [O₂] autour des levures » ne montrait que [O₂] (départ à 7,5, épuisement à 8 min). Elle suit maintenant
`exao.html?vue=levures` : [O₂] (mg/L, cyan) 8,0 → 7,5 jusqu'à l'injection à 2 min, puis 0 à 8,25 min ; [CO₂] (UA,
orange) 1,0 → 1,3 → 6,9 UA à l'épuisement, puis croissance plus lente jusqu'à ≈ 10,4 UA ; éthanol (UA, violet) qui
n'apparaît qu'après l'épuisement (≈ 2,3 UA à 14 min) ; repères « glucose injecté » et « O₂ épuisé » ; phases
« respiration (aérobiose) » / « fermentation (anaérobiose) ». Le format n'a qu'un axe y : il est gradué en mg/L pour
[O₂], les courbes CO₂ et éthanol portent « (UA) ». La ligne « II — 1. ExAO … » est devenue un titre « II. » puis « 1. ».

## Points transversaux restés douteux

- **Bulles des diapositives** (`concentration.cahier` / `cahier_figures`) : hors périmètre, elles gardent les
  anciennes figures et couleurs dans plusieurs cours (ex. SVT ch1 levures, SVT ch2 fatigue, maths ch4-ch6, ondes) et
  sont maintenant en désaccord avec le cahier du bloc. À aligner dans un second passage.
- **Animations hors lexique visuel** : plusieurs pages colorent une même grandeur différemment (RL, RC, RLC, ondes,
  `branches.html`, bases en vert vs HO⁻ bleu ciel au ch13, ln en rouge au ch5…). Le cahier suit la page de la
  diapositive quand elle est cohérente, sinon le lexique ; les cas sont listés par cours ci-dessous. Les animations
  n'ont pas été modifiées.
- **Champ `partie` et lecteur partie par partie** (`partiesDuCahier.ts`, arrivé sur `main` pendant l'audit) :
  `partie: n` y désigne la n-ième partie du bloc ; les agents l'avaient posé comme le numéro « n. » de la ligne →
  139 dessins convertis (commit séparé). Deux corrections du lecteur (commit séparé, `partiesDuCahier.ts` et
  `CycleBloc.tsx`) : un titre romain posé juste avant « 1. » ouvre la partie avec elle (43 titres finissaient la
  partie d'avant) ; un cahier numéroté se découpe toujours par ses numéros (41 blocs avaient autant de lignes que de
  diapositives et passaient en mode « une ligne par diapositive »). Logique testée hors du site (tsc + node), pas
  dans le navigateur : `node_modules` n'est pas installé dans cette copie. `verifier_figures_cahier.py` ne contrôle
  toujours pas les clés d'une figure.
- **Blocs de fin de cours** (`*_bloc_fin_cours`) : texte commun d'environ 200 caractères sur une ligne ; coupé en
  3 lignes dans certains cours (maths ch4-6, ondes), laissé tel quel ailleurs.
- **Copies `en_attente/`** : non mises à jour (hors périmètre demandé) alors que le skill `cahier-de-l-eleve` demande
  d'appliquer le cahier aux deux.
- Aucun rendu à l'écran n'a été fait : les figures sont vérifiées par le vérificateur et par calcul, pas visuellement.

---

# Rapports par cours

## svt_ch1_reactions_responsables_liberation_energie — Libération de l'énergie emmagasinée dans la matière organique
**Blocs touchés** : le_s1_b2 : L'ATP, puis les levures avec et sans dioxygène ; le_s1_b3 : Deux voies : respiration et fermentation ; le_s2_b1 : Où le glucose est-il dégradé ? ; le_s2_b2 : Les transporteurs d'hydrogène ; le_s2_b3 : La glycolyse : lieu et bilan ; le_s3_b1 : La mitochondrie : structure et composition ; le_s3_b2 : Dans la matrice : acétyl-CoA et cycle de Krebs ; le_s4_b1 : Le dioxygène injecté, le taxi décharge ; le_s4_b2 : Le relais, le dioxygène, les protons, la sphère ; le_s4_b3 : Les preuves, puis le schéma du national ; le_s5_b1 : Les fermentations ; le_s5_b2 : Bilans et rendements ; le_s6_b1 : Restitution comme au national ; le_s6_b1b : Relier phénomènes et réactions bilans ; le_s6_b2 : Quelle voie domine ? ; le_s6_b3 : Un document : décrire, déduire… ; le_s6_b4 : Le schéma de synthèse ; le_bloc_fin_cours : Fin du cours (le_s1_b1 et le_s3_b3 relus, conformes, réécrits à l'identique)
### Écarts trouvés avec les animations
- le_s1_b2 / le_e1–le_e3 (exao.html?vue=levures, T = 2 min) : la courbe ne montrait que [O₂], partait de 7,5 à t = 0, s'annulait à 8 min, fermentation en orange → refaite d'après le code (vérifié en Python) : [O₂] cyan 8,0 → 7,5 (0–2 min, −0,25/min) puis −1,2 mg/L/min jusqu'à 0 à 8,25 min ; [CO₂] orange 1,0 → 1,3 → 6,925 (8,25 min) → 10,375 UA (14 min) ; éthanol violet 0 puis +0,4/min → 2,3 UA ; repère « glucose injecté » (2 min), limite « O₂ épuisé » (8,25 min), « respiration (aérobiose) » en vert et « fermentation (anaérobiose) » en violet comme les textes de la simulation ; axe y « [O₂] (mg/L) » gradué seulement à 7,5, courbes « CO₂ (UA) » et « éthanol (UA) » étiquetées, légende qui dit les unités. Texte : 8 min → 8,25 min, CO₂ 1,3 → 6,9 UA, « CO₂ ↑ moins vite » après l'épuisement.
- le_s1_b2 : ligne « II — 1. ExAO … » (cassait la découpe) → titre « II. Respiration et fermentation : les mettre en évidence » sur sa ligne puis « 1. ExAO … » ; titre « I. … » ajouté avant « 1. Hydrolyse ».
- le_s2_b1 / le_m3_isolees, le_m4_o2_atp (exao.html?vue=mitochondries) : ATP tracé en orange alors que la série 'atp' est verte → vert ; la séance III s'arrête au moment o2_baisse_atp_monte (8 min) : la courbe du bloc s'arrête à 8 min (le cyanure, pas encore vu, retiré) ; ajout de la valeur 100 → 96 % (acide pyruvique).
- le_s6_b3 / le_x3* : même courbe, ATP en vert, légende avec les paliers 40 % / 90 UA après le cyanure (8 min).
- le_s4_b1 / le_c1_pulse (exao.html?vue=pulse_o2) : montée tracée en droite et descente non normalisée → montée sinusoïdale 60–75 s et descente 20 + 24·(e^{−(t−75)/45} − e^{−5})/(1 − e^{−5}) jusqu'à 20 à 300 s, comme le code ; « pic (75 s) ».
- le_s1_b3 / le_e3b_masse_levures (national.html?vue=levures) : ajout des calculs 1,970/150 ≈ 0,013 et 0,255/45 ≈ 0,0057 (rapport 2,32) ; carte complétée avec les lieux (mitochondrie / hyaloplasme) comme carrefour.html.
### Améliorations du texte (architecture)
- Chaque bloc qui ouvre une partie commence par son titre romain sur sa ligne (I, II, III, IV, V, VI, VII, VIII, IX, X, XI), suivi de « 1. » ; numérotation continue dans chaque partie.
- le_s6_b4 : « Suite du X — 8. » (n'ouvrait pas de partie) → « 9. Synthèse … » puis « XI. Bilan du chapitre » / « 1. Définition … » / « 2. … ».
- Parties trop longues recoupées : glycolyse (« 4. Définition »), fermentations (« 3. Définition »), cas « chaîne en panne » (« 8. Ex. »).
- Lignes ramenées vers ≤ 90 caractères (définitions sur deux lignes) ; rendement : formule générale + 1159/2860 ; ligne de fin de cours coupée en 3.
- Plan comparé aux cours en ligne : mise en évidence des deux voies → glycolyse → mitochondrie (rôle, ultrastructure) → matrice (acétyl-CoA, Krebs) → chaîne respiratoire et phosphorylation oxydative → fermentations → rendements ; le cours suit déjà cet ordre (avec III « où se passe chaque étape » avant la glycolyse).
### Sources en ligne consultées
- Cours SVT 2Bac SP BIOF, ch1 (plan I–V, ExAO levures, chaîne respiratoire) — https://moutamadris.ma/wp-content/uploads/2020/03/cours-svt-2bac-sp-international-fr-1-1.pdf
- Réactions responsables de la libération de l'énergie (activités, plan I–IV) — https://dyrassa.com/wp-content/uploads/2022/08/Reactions-responsables-de-la-Liberation-de-lenergie-emmagasinee-dans-la-matiere-organique-PDF-4.pdf
- Alloschool, résumé (vu dans les résultats, PDF illisible en texte) — https://www.alloschool.com/element/120209/pdf
### Reste douteux
- Le champ de figure `partie` (le_s1_b2, figure ATP : `"partie": 1`) : le bloc contient deux lignes « 1. » (I.1 et II.1) ; le sens de n est ambigu dans ce cas. Le vérificateur ne contrôle pas les champs au niveau de la figure (pas d'erreur).
- [H⁺] : la simulation pulse_o2 trace la courbe en 'rouge' (la couleur de l'oxygène dans le lexique) ; le cahier garde le rose du lexique (H⁺).
- ATP « doré » du lexique : pas de craie dorée dans FigureCahier ; les schémas gardent l'orange (= Pi dans le lexique) ; la courbe mitochondries suit le vert de la simulation.
- Les bulles de diapositive (concentration.cahier_figures de le_e3_sans_o2, le_m4_o2_atp) gardent l'ancienne courbe [O₂] seule / ATP orange : hors périmètre (je n'ai touché que les blocs).


## svt_ch2_role_muscle_strie_squelettique — Rôle du muscle strié squelettique dans la conversion de l'énergie
**Blocs touchés** : ms_s1_b1 : Voir le muscle se contracter ; ms_s1_b2 : La secousse ; ms_s1_b3 : L'intensité : seuil et recrutement ; ms_s2_b1 : Deux excitations rapprochées ; ms_s2_b2 : Tétanos parfait, nommer un tracé, la fatigue ; ms_s2_b3 : Le muscle chauffe ; ms_s3_b1 : Ouvrir le muscle ; ms_s3_b2 : Les filaments et les bandes ; ms_s3_b3 : Le sarcomère raccourcit ; ms_s4_b1 : De quoi la contraction a-t-elle besoin ? ; ms_s4_b2 : Le calcium ouvre l'accès ; ms_s5_b0b : L'ATP reste constant ; ms_s5_b1 : La fermentation, la respiration, les voies se relaient ; ms_s6_b1 : Comparer les voies ; ms_s6_b2 : Décrire, comparer… ; ms_s7_b2 : Restitution et bilan ; ms_bloc_fin_cours (les autres blocs relus, conformes)
### Écarts trouvés avec les animations
- ms_s2_b2 / ms_f7_fatigue (sommation.html?vue=fatigue) : la courbe du cahier montrait 9 secousses jusqu'à l'arrêt ; la simulation joue 30 secousses à 2 Hz, amplitude 20 → 8 mm, relâchement 0,05 → 0,13 s, sans arrêt → figure refaite : 1re et 30e secousse à la même échelle (modèle de myogramme.js, comme la comparaison de la simulation) ; texte avec ces valeurs ; l'arrêt (dit seulement par la voix) reste en une ligne « si les excitations continuent ».
- ms_s1_b2 / myographe.html : relâchement en cos² → forme exacte de myogramme.js ((1 + cos πv)/2·(1 + 1,6v²)) ; couleurs de la simulation : tracé blanc, latence orange, contraction rose, relâchement bleu, amplitude vert.
- ms_s1_b3 / intensite.html (A = 20·(i − 3)/6 de 4 à 9 mV) : valeurs justes ; couleurs alignées (tracé blanc, seuil vert, amplitude maximale rose, « inefficaces » orange) ; texte : seuil 4 mV, 9 mV → 20 mm.
- ms_s2_b1, ms_s2_b2 / sommation.html : points vérifiés contre le modèle (écart 0) ; tracé blanc ; tétanos imparfait bleu / parfait rose (couleurs de phase CRAIE_PH) ; texte : 0,07 s, 20 puis 31 mm, 15 Hz / 40 Hz, ≈ 60 mm.
- ms_s2_b3 / chaleur.html : chaleur initiale en rouge → orange (une seule courbe orange dans la simulation) ; chaleur retardée u³·e^{3(1−u)} (sommet 35 s, hauteur 28/105) ; « sans O₂ : absente ».
- ms_s5_b1 / voies.html : courbes des parts recalculées avec parts(d) du code (écarts jusqu'à 3 points) ; respiration en bleu (comme voies.html, pas cyan) ; « 1 à 2 min → fermentation » → « ≈ 10 s à 1 min » (dans la frise, la respiration dépasse la fermentation vers 62 s).
### Améliorations du texte (architecture)
- « I. 1. » et « III. 1. » (ne découpaient pas) → titres romains sur leur ligne puis « 1. » ; titres II, IV à XI ajoutés en tête des blocs qui ouvrent une partie (titres des activités) ; numérotation continue (I : 1–4).
- Définitions découpées en deux lignes ≤ 90 caractères ; ms_s6_b1 recoupé (« 7. Méthode (inhibiteurs) ») ; sarcoplasme mis en une phrase sur deux lignes.
- Plan comparé : étude expérimentale (secousse, seuil/recrutement, sommation, tétanos, fatigue) → phénomènes thermiques et chimiques → structure → mécanisme (ATP, Ca²⁺) → régénération de l'ATP (alactique, lactique, aérobie) ; le cours suit cet ordre.
### Sources en ligne consultées
- Prof. Monssif el Kaoune, Chap2 : Rôle du muscle strié squelettique (BIOF) — https://moutamadris.ma/wp-content/uploads/2020/03/cours-svt-2bac-sp-international-fr-1-4.pdf
- Activités ch1 + ch2 (I. Étude expérimentale, II. Phénomènes thermiques et métaboliques) — https://dyrassa.com/wp-content/uploads/2022/08/Reactions-responsables-de-la-Liberation-de-lenergie-emmagasinee-dans-la-matiere-organique-PDF-4.pdf
- Alloschool, muscle strié (vu dans les résultats, PDF sans texte extractible) — https://www.alloschool.com/element/120214/pdf
### Reste douteux
- Voix / écran de ms_r6_relais : « une à deux minutes : fermentation lactique » alors que la frise de voies.html donne la respiration dominante dès ≈ 62 s ; le cahier suit la frise. À trancher (modèle plausible, proche des données physiologiques).
- Aérobie en bleu dans voies.html mais en cyan dans national.html (figure ms_s6_b3 gardée en cyan, comme national.html) : deux couleurs pour la même voie.
- Fatigue : la voix dit « jusqu'à l'arrêt », l'animation ne le montre pas.
- Champ `partie` posé sur des figures (ms_s1_b3 : 2, ms_s2_b2 : 5 et 6, ms_s5_b1 : 5) ; le vérificateur ne le signale pas (il ne contrôle pas les champs de la figure elle-même).
- Bulles de diapositive (ms_f7_fatigue, etc.) gardent les anciennes figures : hors périmètre.


## svt_ch3_notion_information_genetique — Notion de l'information génétique
**Blocs touchés** : ig_s1_b1 : Une information transmise ; ig_s1_b2 : L'acétabulaire ; ig_s1_b3 : Gurdon et la définition ; ig_s2_b1 : Chromatine et chromosome ; ig_s2_b2 : 46 chromosomes, la mitose en une idée ; ig_s2_b3 : Une ou deux chromatides, le cycle ; ig_s3_b1 : Courbe de la quantité d'ADN ; ig_s3_b2 : Décrire la courbe, durées ; ig_s3_b3 : Mitose, prophase, métaphase ; ig_s4_b1 : Anaphase, télophase, cellule végétale ; ig_s4_b2 : Reconnaître et légender une phase ; ig_s4_b3 : Griffith 1 et 2 ; ig_s5_b1 : Griffith 3 et 4 ; ig_s5_b2 : Avery ; ig_s5_b3 : Nucléotide, Chargaff ; ig_s6_b1 : Double hélice ; ig_s6_b2 : Meselson, G1 ; ig_s6_b3 : G2, semi-conservative ; ig_s7_b1 : Thymidine, yeux ; ig_s7_b2 : ADN polymérase ; ig_s7_b3 : Restitution ; ig_s8_b1 : Courbe, décrire / expliquer ; ig_s8_b2 : Thymidine 2017 R ; ig_s8_b3 : Bilan
### Écarts trouvés avec les animations
- ig_s3_b1 / ig_c3_courbe, ig_c4_aspect (cycle.html) : la courbe du cahier avait S de 8 à 14 h et une chute de 19 à 20 h ; l'animation trace G1 0–9 h, S 9–15 h, G2 15–19 h, M 19–20 h (chute à 19,9–20 h), q = 3 UA, 2q = 6 UA, en accord avec les durées calculées (9 / 6 / 4 / 1 h) → courbe refaite sur ces valeurs (vérifiée en Python : écart nul avec `ADN(h)`), un segment par phase dans la couleur de l'animation (G1 vert, S orange, G2 bleu, M violet), axe y gradué « q », « 2q » comme dans l'animation, étiquette « réplication ».
- ig_s3_b1 : croquis du chromosome cyan → violet (Peint.VIOLET de l'animation) ; yeux de réplication ajoutés en orange ; noms des phases dans leurs couleurs.
- ig_s8_b1 / ig_x2 (documents.html, vue courbe) : le cahier réutilisait la courbe du cycle (0–23 h) ; le document d'examen va de 0 à 30 h (3 UA jusqu'à 8 h, 3→6 UA de 8 à 14 h, 6 UA jusqu'à 19 h, 6→3 UA de 19 à 20 h, 3 UA jusqu'à 28 h, nouvelle montée), graduations de 4 h, « q = 3 UA », « 2q = 6 UA » → courbe refaite (écart nul en Python).
- ig_s8_b1 : « 2q → q = chromatides séparées (anaphase) » contredisait l'animation (« 19 à 20 h : répartition égale de l'ADN entre deux cellules filles ») et est faux (la quantité par cellule ne baisse qu'à la division) → corrigé + ligne « Attention ».
- ig_s3_b3, ig_s4_b1, ig_s4_b2 (mitose.html) : chromosomes cyan / rose → violet (paire longue) / bleu (paire courte) comme l'animation ; asters jaunes → blancs ; membrane plasmique en rose (cellule corail) ; noyaux de télophase (animale et végétale) cyan → violet (noyau du lexique) ; chromatine décondensée violette.
- ig_s4_b2 (schéma de l'anaphase, moment `schema_anaphase`) : l'animation légende aster, fibres du fuseau, chromatide, membrane plasmique, cytoplasme et « 4 chromatides à chaque pôle » ; le cahier n'avait que aster et chromatide → légendes ajoutées.
- ig_s2_b1 (zoom.html) : histones beige et étiquette blanche dans l'animation, jaune dans le cahier → blanc.
- ig_s2_b3 (zoom.html, vue chromosome) : chromatides cyan → violet.
- ig_s5_b2 (bacteries.html) : capsule claire (blanche) dans l'animation, jaune dans le cahier → blanc.
- ig_s5_b3 (adn.html) : désoxyribose = pentagone gris dans l'animation → « faible » (gris) au lieu de blanc.
- ig_s6_b3 (meselson.html) : bandes toutes bleu clair dans l'animation (pas un code rouge / jaune / cyan) → bandes cyan ; tube G3 (25 % hybride mince, 75 % légère épaisse) montré par l'animation et cité par le texte, absent du dessin → ajouté.
- ig_s2_b3 / ig_c1_cycle : l'animation écrit « interphase = G1 + S + G2 », « 19 h sur 20 h : la plus longue », G1 / G2 « croissance » → ajouté au texte.
- Vérifiés conformes : durées (2,5·10³ → 10·10³ en 40 h, 20 h ; G1 45 % = 9 h, G2 4 h, M 1 h, S 6 h), densités Meselson (1,710 / 1,717 / 1,724 ; 50/50 ; 25/75), couleurs des bases (A rouge, T jaune, C bleu, G vert), séquence 5' ATCGGA 3', brins thymidine (bleu / rouge / blanc), réplication (ancien bleu, nouveau orange, sens 5'→3'), Griffith / Avery.
### Améliorations du texte (architecture)
- Plan en parties romaines, chacune sur sa ligne avant son « 1. » : I. Localisation de l'information génétique ; II. Chromatine et chromosomes ; III. Cycle cellulaire et quantité d'ADN ; IV. La mitose ; V. L'ADN, support de l'information génétique ; VI. Composition chimique et structure de l'ADN ; VII. La réplication de l'ADN ; VIII. Comme à l'examen (ordre des cours moutamadris : localisation → noyau → mitose / cycle → nature chimique → structure → réplication).
- Chaque bloc commence par une ligne « n. » (ou un titre romain suivi de « 1. ») : Griffith suite → « 2. », Meselson G2/G3 → « 3. », Taylor « 4. », mécanisme « 5. », ADN polymérase « 6. », conservation « 7. », méthode des phases « 6. », brin complémentaire « 5. » ; numérotation continue dans chaque partie romaine.
- Acétabulaire en a) section / b) greffe ; définition de l'information génétique et de la mitose coupées en deux lignes ; restitution / association séparées ; parties ≤ 5 lignes, lignes ≤ ~90 caractères.
- Champ `"partie": n` ajouté à chaque dessin (le vérificateur ne le signale pas : 0 erreur).
### Sources en ligne consultées
- Moutamadris, cours SVT 2 Bac (chap. 1 « Notion de l'information génétique », plan I–V et définitions du cycle et de la quantité d'ADN) — https://moutamadris.ma/wp-content/uploads/2020/03/cours-svt-2bac-sp-international-fr-2-1.pdf
- Moutamadris, cours SVT 2 Bac (chap. 1, version activités : localisation, nature chimique, structure, transfert, cycle) — https://moutamadris.ma/wp-content/uploads/2020/03/cours-svt-2bac-sp-international-fr-2-2.pdf
- AlloSchool, cours « transmission de l'information génétique » (PDF image, vu dans les résultats, texte non lisible) — https://www.alloschool.com/element/120797/pdf
### Reste douteux
- Les schémas de mitose du cahier gardent un fuseau horizontal (pôles à gauche et à droite) ; l'animation le dessine vertical (pôles en haut et en bas). Les couleurs et les légendes sont alignées, l'orientation non (la refaire demande de redessiner les 5 croquis).
- Deux horaires de cycle coexistent : celui de l'animation (S 9–15 h) et celui du document d'examen (S 8–14 h, ig_c5 / ig_x2). Le cahier suit chacun à son bloc, en précisant « (document) » ; un élève peut confondre.
- Le bloc de fin de cours (ig_bloc_fin_cours) a une ligne de 204 caractères (texte commun à tous les cours), laissée telle quelle.
- Avertissements du vérificateur (pas des erreurs) : 15 à 19 éléments dans 3 dessins (chromosome au cours du cycle, anaphase légendée, Meselson à 4 tubes).
- La copie `en_attente/` n'a pas été touchée (hors périmètre).


## svt_ch4_relation_gene_proteine — Expression de l'information génétique
**Blocs touchés** : rg_s1_b1 : La question du chapitre ; rg_s1_b2 : Gène et allèle ; rg_s1_b3 : Mutation ; rg_s2_b1 : Protéine, drépanocytose ; rg_s2_b2 : La protéine en cause ; rg_s2_b3 : Albinisme, Beadle et Tatum ; rg_s3_b1 : L'ARN, uracile ; rg_s3_b2 : L'ARNm est nécessaire ; rg_s3_b3 : Transcription, arbre de Noël ; rg_s4_b1 : Base après base, sens ; rg_s4_b2 : Légender, ARNm comme le barème ; rg_s4_b3 : Codon, Nirenberg, tableau ; rg_s5_b1 : Initiation, stop, propriétés ; rg_s5_b2 : Acteurs, initiation, élongation ; rg_s5_b3 : Terminaison, polysome ; rg_s6_b1 : Substitutions ; rg_s6_b2 : Délétion, insertion ; rg_s6_b3 : Du gène au caractère ; rg_s7_b1 : Transcription ou traduction, restitution ; rg_s7_b2 : Méthode du national ; rg_s7_b3 : Sujet 2024 N ; rg_s8_b1 : 2020 N ; rg_s8_b2 : 2022 N ; rg_s8_b3 : Drépanocytose et bilan
### Écarts trouvés avec les animations
- rg_s5_b2 / rg_r3_elongation (traduction.html, lexique génétique) : ARNt dessinés en orange (couleur de l'ARNm) → vert (ARNt vert pâle du lexique) ; « Met – Arg » en violet → perles de l'animation : Met rouge, Arg bleu.
- rg_s4_b2 / rg_t5b_legender (transcription.html) : ARN polymérase cyan → rose (« ovale rose-violet », étiquette craie rose) ; brins d'ADN blancs → bleus (squelette bleu-violet).
- rg_s4_b1 / rg_t4_sens : brin transcrit blanc → bleu (ADN), ARNm orange conservé ; séquences AUG CGC AGU / TAC GCG TCA conformes à l'animation.
- rg_s3_b3 / rg_t2b_arbre_noel (documents.html) : l'animation montre le tronc (ADN) en cyan et les ARN polymérases en points verts ; le cahier avait ADN blanc et polymérases cyan → corrigé.
- rg_s1_b2 / rg_g2_allele (paire_homologues.html) : chromosome paternel violet, maternel bleu dans l'animation (cyan / rose dans le cahier) → corrigé ; légende précise « paire n° 9 ».
- rg_s3_b1 (marquage.html) : cytoplasme rosé → contour de cellule rose ; 5 min noyau / 30 min cytoplasme conformes.
- rg_s6_b3 (schema_bilan.html) : gène (ADN) en bleu ; « cytoplasme » en rose.
- Vérifiés conformes : code (AUG GAA UUU CCG UAA → Met – Glu – Phe – Pro ; CUG/CUA Leu), mutations (ATG CTG GAG TGG CAA ; silencieuse, faux-sens, non-sens, délétion du G du triplet 3 → Ser – Gly – Asn), drépanocytose (triplet 6 CTC → CAC, GAG → GUG, Glu → Val), 2024 N (CCC → CTC, Pro → Leu), 2020 N (97/8/0 % et 32/32/28 %, triplet 247 GGC → AGC), 2022 N (46 / 23 UA).
### Améliorations du texte (architecture)
- Plan en parties romaines (absentes avant ; « 1. » repartait à chaque séance) : I. Caractère, gène, allèle et mutation ; II. Relation protéine – caractère ; III. Du noyau au cytoplasme : l'ARN messager ; IV. La transcription ; V. Le code génétique ; VI. La traduction ; VII. Les mutations et leurs conséquences ; VIII. Relation gène – protéine – caractère ; IX. Comme à l'examen (ordre des cours moutamadris : notions → relation protéine/gène/caractère → mécanisme : ARNm, transcription, code, traduction).
- Lignes-titres sans contenu (« 1. Caractère et phénotype », « 3. La mutation »…) fusionnées avec leur première idée ; chaque bloc commence par « n. » ou un titre romain suivi de « 1. » ; numérotation continue (II : 1–5 ; III : 1–4 ; VI : 1–6 ; IX : 1–7).
- Parties de 6 lignes recoupées (2020 N : relation + hypothèse / vérification ; délétion 1 nucléotide / 3 nucléotides ; III. ARN / uracile) ; « Problème » placé en tête du chapitre ; propriétés du code avec l'exemple CUG/CUA de l'animation ; « 64 codons : 61 + 3 stop ».
- Champ `"partie": n` ajouté à chaque dessin (0 erreur au vérificateur).
### Sources en ligne consultées
- Moutamadris, cours SVT 2 Bac, chap. 2 « L'expression de l'information génétique » (plan I–III, transcription, code, traduction) — https://moutamadris.ma/wp-content/uploads/2020/03/cours-svt-2bac-sp-international-fr-2-7.pdf
- Moutamadris, cours SVT 2 Bac (activités : caractère, gène, allèle, mutation ; relation gène – protéine – caractère ; mécanisme d'expression) — https://moutamadris.ma/wp-content/uploads/2020/03/cours-svt-2bac-sp-international-fr-2-5.pdf
- Kartable, « L'expression du patrimoine génétique » (vu dans les résultats seulement) — https://kartable.fr/ressources/svt/cours/lexpression-du-patrimoine-genetique-2/50742
### Reste douteux
- L'ADN est dessiné en « bleu » de craie ; le lexique dit squelette indigo / bleu-violet (pas de craie indigo) ; l'arbre de Noël de l'animation, lui, nomme l'ADN en cyan : deux couleurs d'ADN coexistent dans les animations.
- Lignes de 93 à 95 caractères gardées à quelques endroits (définitions, chaînes de causalité) ; bloc de fin de cours (204 caractères, texte commun) non touché.
- Avertissement du vérificateur : 15 éléments dans le dessin de l'élongation.
- La copie `en_attente/` n'a pas été touchée (hors périmètre).


## math_ch1_limites_continuite — Limites et continuité
**Blocs touchés** : lc_s1_b1 : La carte ; où mène le chemin ; je remplace d'abord, lc_s1_b2 : 0/0 n'est pas une réponse ; les quatre formes, lc_s1_b3 : Limites usuelles ; a² − b² ; une racine donne le facteur, lc_s1_b4 : Le facteur (x − a), le conjugué, le plus haut degré, lc_s2_b1 : √(x²) = |x| ; racine à l'infini, lc_s2_b2 : Par la droite, par la gauche ; interpréter, lc_s2_b3 : sin(x)/x ; à toi : des limites, lc_s2_b4 : Continue en a : la limite égale l'image, lc_s3_b0 : Souder la courbe, à droite et à gauche, rédiger, lc_s3_b1 : Les fonctions usuelles, les opérations, √u, lc_s3_b2 : Limite d'une composée ; le signe de f′ ; les hauteurs atteintes, lc_s3_b3 : Image d'un intervalle, lc_s4_b1 : Couper l'axe…, lc_s4_b2 : Au moins une solution, puis unique ; rédiger, lc_s4_b3 : Toute valeur k ; intervalle ouvert ; f(α) = 0, lc_s5_b1 : Aller et retour ; strictement monotone ; J = f(I), lc_s5_b2 : Deux lignes au national ; même sens ; le miroir, lc_s5_b3 : Construire la courbe ; l'expression de f⁻¹, lc_s6_b1 : Défaire la puissance n…, lc_s6_b2 : Simplifier ; résoudre xⁿ = a, lc_s6_b3 : Puissances rationnelles, lc_s6_b4 : Continuité et limites avec ⁿ√u, lc_s7_b1 : Le problème national, lc_s7_b4 : Ce qu'il faut retenir, la carte (titres de bloc inchangés ; lc_bloc_fin_cours non touché)
### Écarts trouvés avec les animations
- lc_s2_b2 / approche.html?vue=deux_cotes + infini.html?vue=horizontale : le cahier dessinait 2 + 1/(x − 1), fonction absente des deux animations → deux figures : f(x) = 1/(x − 1) (x = 1 asymptote verticale, +∞ à droite, −∞ à gauche) et f(x) = (2x + 1)/(x + 1) sur [0 ; 20] (asymptote y = 2) ; asymptotes en pointillé blanc (lexique), étiquettes plus en jaune.
- lc_s2_b4 / raccord.html?vue=limite_image (fa = 3 par défaut) : la courbe générique (0,5x + 1, autre branche, « la courbe saute ») ne correspondait pas → f(x) = x + 1 trouée en (1 ; 2) (rond creux cyan), point (1 ; 3) vert ; texte : « lim = 2 ≠ f(1) = 3 » sans « la courbe saute ».
- lc_s3_b0 / raccord.html?vue=deux_branches : couleurs des branches inversées (cyan/jaune) → 3x − 1 en rouge, x² + m en vert, f(1) en jaune, comme l'animation.
- lc_s3_b3 / projections.html : la courbe 0,5x² + 0,5x + 1 sur [1 ; 3] n'existe pas dans l'animation → figure de x² − 4x + 1 sur [2 ; 5] → [−3 ; 6] (projections vertes) déplacée dans lc_s3_b2 (diapo j1) ; dans lc_s3_b3, figure de la vue decroissante g(x) = 4/x sur [1 ; 4] (g(1) = 4 vert, g(4) = 1 orange) + tableau de h = x³ − 3x conservé (valeurs vérifiées).
- lc_s4_b1 / traversee.html (fil rouge x³ + x − 1 sur [0 ; 1]) : cubique inventée, f(a) en « rose » → x³ + x − 1, f(0) = −1 rouge, f(1) = 1 vert, α ≈ 0,6823 jaune.
- lc_s4_b2 / traversee.html?vue=vague : (x − 1)(x − 2)(x − 3) sur [0,5 ; 3,5] → la vague −0,9cos(3πx) + 0,1x sur [0 ; 1], zéros recalculés α₁ ≈ 0,165, α₂ ≈ 0,506, α₃ ≈ 0,824.
- lc_s4_b3 / traversee.html?vue=droite_k (k = 0,5) : 0,25x² + 1 → x³ + x − 1 et y = 0,5, c ≈ 0,861 (calculé).
- lc_s5_b1 / miroir.html?vue=parabole : branche droite jaune, points blancs → branche gauche pâle, droite cyan, y = 4 en pointillé orange, antécédents rouges.
- lc_s5_b2 / miroir.html?vue=reflet : (C_f⁻¹) et M′ en jaune → verts, segment MM′ jaune, points (0 ; 1) ↔ (1 ; 0) ajoutés ; repère carré.
- lc_s6_b1 / racine.html?vue=reflet_racine (n = 3) : fenêtre jusqu'à 8,6 et (2 ; 8) ↔ (8 ; 2) → fenêtre [−0,2 ; 2,6] de l'animation, ∛x en vert, (0 ; 0) et (1 ; 1) en orange.
- lc_s7_b1 / national.html?vue=q3_encadrement : f(1/2) en rose → rouge, f(1) = 1 vert ajouté, fenêtre de l'animation.
- lc_s1_b1, lc_s1_b3 : trou en cyan, M jaune / M′ vert (approche.html), racines P(1) vert / P(3) jaune (rappels.html) ; points auparavant blancs (couleur par défaut du rendu).
### Améliorations du texte (architecture)
- Plan en parties romaines du cours (I. à IX., titres des activités) écrites sur leur propre ligne avant « 1. » ; chaque bloc commence par une ligne « n. » ; numérotation continue dans la partie I (1. à 13.) ; « Fin du III — 5. » supprimé (n'ouvrait pas de partie).
- Énoncés au format national (Atmani, résumé PC/SVT) : continuité à droite/à gauche, continuité sur ]a ; b[ puis [a ; b] ; image d'un segment / d'un intervalle ; TVI « cas général » (pour tout k entre f(a) et f(b), au moins un c ∈ [a ; b]) et son corollaire f(a) × f(b) < 0 → au moins une solution dans ]a ; b[, unique si strictement monotone ; réciproque : « f est une bijection de I sur J = f(I) », f⁻¹ continue, même sens, symétrie / y = x ; ⁿ√ définie comme réciproque de xⁿ sur [0 ; +∞[.
- Parties de 3 à 5 lignes, lignes ≤ ~92 caractères, champ `partie` posé sur chaque dessin ; ligne « Plan » de la carte retirée.
### Sources en ligne consultées
- Résumé Limites et continuité 2 Bac PC/SVT (Pr Atmani Najib, moutamadris) — https://moutamadris.ma/wp-content/uploads/2022/06/resume-Limites-et-continuite-2bac-Sciences-Physiques-et-svt-1.pdf
- Limites et continuité, cours 2 Bac PC (talamidi, vu dans les résultats, lien 404) — https://talamidi.com/Cours/Maroc/Lycée/2Bac/Sciences Physiques/Mathématiques (BIOF)/Limites et continuité/Cours/Talamidi.com_limites-et-continuite-cours-3.pdf
- Résumé Limites et continuité 2 Bac PC/SVT (monstremath, vu dans les résultats) — https://monstremath.com/2Bac/2eme-BAC-Sciences-Physiques-et-svt/cours-mathematique-2bac-sciences-experimentales/Résumé 01 Limites et continuité 2 BAC Sciences pc et svt modele 7.pdf
### Reste douteux
- Couleurs propres aux animations gardées dans le cahier (rouge/vert pour les branches de raccord.html et pour f(a)/f(b) de traversee.html), alors que le lexique réserve vert/rouge aux signes + / − : à trancher dans le lexique.
- Le rendu FigureCahier met les points en blanc par défaut (lexique : jaune) ; j'ai donné une couleur explicite à chaque point.
- La limite d'une composée n'est écrite que pour √u (comme la diapo) ; la forme générale lim v(u(x)) = v(ℓ) (v continue en ℓ) figure dans les cours en ligne.
- Le caractère « ᑫ » (syllabique canadien) sert d'indice q dans ᑫ√(xᵖ) : rendu à vérifier.
- lc_bloc_fin_cours : une seule ligne de ~200 caractères (texte commun à tous les cours), non touchée.
- Le vérificateur ne signale pas le champ `partie` (il ne contrôle pas les champs du niveau figure) : 0 erreur.


## math_ch2_derivation_etude_fonctions — Dérivation et étude des fonctions
**Blocs touchés** : tous les blocs de contenu (26) : df_n1_b1, df_n1_b2, df_n1_b3, df_n1_b4, df_n2_b1, df_n2_b2, df_n2_b3, df_n2_b4, df_n3_b1, df_n3_b2, df_n3_b3, df_n3_b4, df_n3_b5, df_s4_b1, df_s4_b2, df_s4_b3, df_s5_b1, df_s5_b2, df_s5_b3, df_s6_b1, df_s6_b2, df_s6_b3, df_n7_b1, df_n7_b2, df_n7_b2c, df_s7_b3 (titres inchangés ; df_bloc_fin_cours non touché)
### Écarts trouvés avec les animations
- df_s5_b1 / position.html?vue=ecart : le cahier traçait x + 1/x et (Δ) : y = x ; l'animation étudie f(x) = 2x + 1 + 1/x et (Δ) : y = 2x + 1 (f(1) = 4 contre 3, f(−1) = −2 contre −1) → figure et exemple refaits (f(x) − (2x + 1) = 1/x).
- df_n3_b5 / calculs.html?vue=aux_g : double barre en 0 dans le tableau de g (g est définie en 0, l'animation écrit « 2 » sans barre) → barre retirée ; tableau de f = x² − 3x − 2/x gardé avec sa barre (0 interdit).
- Tangentes et demi-tangentes en jaune (df_n1_b2, b3, df_n2_b1, df_n3_b2, df_s4_b1, df_s6_b2, df_n7_b2c) → orange (lexique et animations : secante.html, miroir.html) ; sécante (AM) et M en orange comme secante.html.
- Asymptotes en jaune pointillé (df_s4_b2 oblique, df_s5_b1) ou gris (df_s5_b2) → pointillé blanc (lexique) ; direction y = x (df_s4_b3) en violet comme branches.html ; √x de df_s4_b2 en violet (2ᵉ courbe).
- df_s5_b2 / symetrie.html?vue=centre : M jaune, M′ rose, Ω violet comme l'animation (M′ était blanc, Ω jaune).
- df_s6_b2 / miroir.html?vue=pentes (x_a = 2) : (C_f⁻¹) en vert comme l'animation (était cyan).
- df_s4_b1 / concavite.html : « concave » en rose → bleu (la zone sous la tangente est bleue dans l'animation).
- Ajout de deux dessins présents dans les animations et absents du cahier : x + 1/x ≥ 2 (minimum.html, df_n3_b4) et le tracé pas à pas de x + 1/x avec asymptotes x = 0 et y = x, extremums (−1 ; −2) et (1 ; 2) (trace.html?vue=etapes, df_s5_b3).
- Valeurs vérifiées conformes : pente (AM) = 3 pour M(2 ; 4) (tableau de secante.html), f′(1) = 2, tangente y = (3/4)x + 1 (a = 2 par défaut), |x² − 1| (2 et −2), x³ − 3x (2, −2, I(0 ; 0), y = −3x), 2x + 1 + 1/x, x + √x, (x + 1)/(x − 2) (M(3 ; 4), M′(1 ; −2)), x√(x + 1) (min −2√3/9 ≈ −0,385).
### Améliorations du texte (architecture)
- Plan I. à XIII. (titres des activités) sur leur propre ligne, numérotation qui repart à 1. dans chaque partie et continue d'un bloc à l'autre (ex. IV : 1.–6. sur trois blocs) ; les lignes « Rappel », « Vérifier », « Attention » en tête de bloc rattachées à une ligne « n. ».
- Énoncés au format des cours marocains (Benmoussa, 2 PC/SVT) : dérivabilité en x₀ sur un intervalle ouvert, à droite/à gauche, « dérivable ⇔ dérivable à droite et à gauche avec f_d′ = f_g′ », point anguleux, demi-tangente verticale et son sens (quatre cas sur deux lignes), concavité par le signe de f″, point d'inflexion (f″ s'annule en changeant de signe), branches infinies (arbre f(x)/x puis f(x) − ax), axe et centre (avec (2a − x) ∈ D_f), dérivée de la réciproque avec f′(x₀) ≠ 0.
- Lignes « But » et « Carte » retirées (cartes non recopiées) ; exemple de l'axe x = 2 (x² − 4x + 5, symetrie.html?vue=axe) ajouté.
### Sources en ligne consultées
- Cours Dérivation et étude des fonctions 2 PC/SVT (Pr Benmoussa, moutamadris) — https://moutamadris.ma/wp-content/uploads/2022/06/cours-Derivation-et-etude-des-fonctions-2bac-Sciences-Physiques-et-svt-1.pdf
- Dérivation et étude des fonctions — résumé de cours 2 (9rayti) — https://www.9rayti.com/doros/pdf/derivation-et-etude-des-fonctions-resume-de-cours-2
- Résumé dérivation 2 Bac PC (talamidi, vu dans les résultats, lien 404) — https://talamidi.com/Cours/Maroc/Lycée/2Bac/Sciences Physiques/Mathématiques (BIOF)/Dérivation et étude des fonctions/Cours/Talamidi.com_derivation-et-etude-des-fonctions-resume-de-cours-1.pdf
### Reste douteux
- Animations elles-mêmes hors lexique : branches.html trace l'asymptote horizontale et l'oblique en rouge (lexique : pointillé blanc) et symetrie.html l'axe x = 2 en violet ; le cahier suit le lexique (blanc). Animation non modifiée.
- Points en blanc par défaut dans FigureCahier (lexique : jaune) : couleurs mises explicitement.
- df_bloc_fin_cours : ligne unique de ~200 caractères, commune aux cours, non touchée.
- Champ `partie` non contrôlé par le vérificateur (aucune erreur signalée).


## math_ch3_suites_numeriques — Suites numériques
**Blocs touchés** : tous les blocs de contenu (22) : su_n1_b1, su_n1_b2, su_n1_b3, su_n1_b4, su_n2_b1, su_n2_b2, su_n2_b3, su_n2_b4, su_n3_b1, su_n3_b2, su_s3_b1, su_s3_b2, su_s3_b3, su_s4_b1, su_s4_b2, su_s4_b3, su_s5_b1, su_s5_b2, su_s5_b3, su_s6_b1, su_n8_b1, su_n8_b2 (titres inchangés ; su_bloc_fin_cours non touché)
### Écarts trouvés avec les animations
- su_s4_b3 / plafond.html?vue=sous_plafond : le cahier dessinait 1,5 − 1,5·0,5ⁿ (ℓ = 1,5, M = 2) ; l'animation montre uₙ = 4 − 3 × 0,6ⁿ (1 ; 2,2 ; 2,92…), ℓ = 4 et un plafond M = 6 orange → figure refaite avec ces valeurs.
- su_n3_b2 / nuage.html?vue=bornee : plafond y = 5 jaune → orange, plancher y = 0 vert ajouté, points cyan (nuage de l'animation), axe y depuis −0,6.
- su_s4_b1 / qn.html?vue=negatif : q = −1 en rose → vert comme l'animation ; q = −1/2 cyan conservé.
- Points des suites (su_s3_b3, su_s5_b1, su_n8_b1) blancs → cyan (nuages de points des animations) ; limite ℓ = 16 en jaune, plancher y = 2 vert (national.html?vue=n24_points).
- su_s5_b2 / escalier.html : point (1 ; 1) en vert comme l'animation.
- su_s3_b2 / calculs.html?vue=x3 : la relation uₙ₊₁ = (3 + uₙ)/(5 − uₙ) manquait (le « dénominateur 5 − uₙ » restait sans source) → ajoutée.
- Valeurs vérifiées conformes : u₀ = 17, ¼uₙ + 12 → 16 + (¼)ⁿ ; 5n²/(n² + 2) ; 2uₙ/(2uₙ + 5), (3/2)(2/5)ⁿ (k = 0,4) ; 2x/(x + 1), u₀ = 2, u₁ = 4/3, u₂ = 8/7 ; g(x) = (4x + 3)/(x + 2), g(1) = 7/3 ; national 2024 (u₁ = 2,8 ; u₂ ≈ 2,421 ; vₙ = (2/3)ⁿ⁺¹).
### Améliorations du texte (architecture)
- Plan I. à IX. (titres des activités) sur leur propre ligne ; « V. 1. lim… » (qui n'ouvrait pas de partie) remplacé par « V. Limites d'une suite » puis « 1. … » ; chaque bloc commence par « n. » ; numérotation continue (récurrence : 1.–10. sur cinq blocs).
- Énoncés au format national (sigmaths 2 PC 2023/2024, Atlasmaths 2 Bac SE) : récurrence Initialisation / Hérédité / Conclusion avec la preuve de l'hérédité écrite ; majorée/minorée/bornée « pour tout n » ; limite de qⁿ en quatre cas ; « croissante et majorée ⇒ convergente » ; critères de comparaison (encadrement, |uₙ − ℓ| ≤ vₙ, uₙ ≥ vₙ → +∞) ; théorème uₙ₊₁ = f(uₙ) avec ses quatre conditions (f continue sur I, f(I) ⊂ I, u₀ ∈ I, (uₙ) convergente ⇒ ℓ solution de f(x) = x dans I).
- National 2024 découpé en deux parties (Q1–Q3, puis Q4–Q5) ; méthode 3 du sens de variation renvoyée à la partie VII ; bilan en une partie.
### Sources en ligne consultées
- Étude d'une suite numérique, 2 Bac PC 2023/2024 (sigmaths) — https://www.sigmaths.net/docEtranger/maroc/4195_1707475175.pdf
- Suites numériques, fiche 2 Bac SE (Atlasmaths) — https://riyaddiyat.pages.dev/fiches/2bac-se/suites-numeriques-2bac-se.pdf
- Cours suites numériques (biologie-maroc, niveau supérieur, plan seulement) — https://biologie-maroc.com/wp-content/uploads/2022/03/math-cours-suites-numeriques.pdf
### Reste douteux
- su_s4_b2 (croquis de la règle de q) : couleurs de qn.html?vue=libre non relues en détail ; « pas de limite » mis en rouge.
- Points en blanc par défaut dans FigureCahier (lexique : jaune ; les nuages des animations de suites sont cyan) : couleurs mises explicitement.
- su_bloc_fin_cours : ligne unique de ~200 caractères, commune aux cours, non touchée.
- Champ `partie` non contrôlé par le vérificateur (aucune erreur signalée).


## math_ch4_primitives — Fonctions primitives
**Blocs touchés** : les 19 blocs (pr_s1_b1 … pr_s5_b2, pr_bloc_fin_cours) : texte du cahier ; figures redessinées dans pr_s2_b1, pr_s2_b1b, pr_s2_b3b, pr_s4_b3
### Écarts trouvés avec les animations
- pr_s2_b1 / pr_e3, pr_e5 (famille.html?vue=famille) : le cahier traçait x² − 1 (faible), x² (cyan), x² + 2 (jaune), alors que l'animation trace x² cyan, x² + 2 violet, x² − 2 rose, et la courbe x² + k jaune avec k = 3 par défaut, plus le pointillé orange x = 1 et les tangentes vertes pour k = −2, 0, 2, 3 → figure refaite avec ces courbes, ces couleurs et ces tangentes.
- pr_s2_b1b / pr_e6 (famille.html?vue=point) : la primitive choisie x² + 2 était jaune ; dans l'animation elle est cyan, l'essai x² − 1 est orange en pointillé et la famille est pâle → couleurs alignées, essai k = −1 ajouté, A(1 ; 3) jaune.
- pr_s2_b3b / pr_u6 (cercle.html) : la flèche « dériver » était jaune et ne couvrait qu'un quart de tour ; dans l'animation elle est rouge et fait presque trois quarts de tour (l'arc « primitiver » est vert, en sens inverse), les quatre points sont jaunes et les noms cyan → croquis refait.
- pr_s4_b3 / pr_g1, pr_g2 (pente.html) : les tangentes horizontales étaient vertes et les extremums de F n'étaient pas marqués ; dans l'animation F est cyan, f jaune, et F a un « max » en −1 et un « min » en 1 → tangentes orange (lexique), points max/min cyan, zéros de f blancs, repères pointillés.
- pr_s4_b3 / pr_g3 (variations.html) : la ligne s'appelait « f(x) » ; dans l'animation elle s'appelle « f(x) = F′(x) » → renommée.
### Améliorations du texte (architecture)
- Les titres romains ont maintenant leur propre ligne (I. Fonction primitive d'une fonction, II. Existence…, III. Primitives des fonctions usuelles, IV. Opérations sur les primitives, V. Primitives des fonctions composées, VI., VII. Primitive et sens de variation, VIII. Exercices type national, IX. Bilan). Avant, on trouvait des lignes comme « IV. 1. », « V. Rappel » ou « VI. 1. ».
- La numérotation est continue et chaque bloc commence par « n. », sauf le bloc d'ouverture.
- Définition écrite comme au national : « soit f définie sur un intervalle I ; F est une primitive de f sur I si F est dérivable sur I et si, pour tout x ∈ I, F′(x) = f(x) ».
- Propriété d'unicité : « il existe une unique primitive F telle que F(x₀) = y₀ ».
- Conditions complétées : u et v dérivables sur I, n ∈ ℕ*, n ≥ 2, (ax + b)ⁿ avec n ∈ ℕ*.
- Méthodes renumérotées de 1 à 5. Chaque partie fait 5 lignes au plus, et chaque ligne environ 95 caractères au plus.
- Le bloc de fin de cours (une ligne de 215 caractères) est coupé en 3 lignes.
- Le nombre de lignes ne vaut plus le nombre de diapositives (sinon le lecteur passe en mode « une ligne par diapo »).
- Le rappel « f′(a) = pente » est retiré du bloc 1 : il revient en VII. 1.
- `partie` est posé sur les figures à placer (6, 1, 2).
### Sources en ligne consultées
- Résumé de cours « Fonctions primitives », Atmani Najib, 2ᵉ Bac Sc. ex. — https://moutamadris.ma/wp-content/uploads/2022/06/resume-Fonctions-primitives-2bac-Sciences-Physiques-et-svt-1.pdf (ouvert)
- Talamidi, « fonctions primitives cours 1 » (2 Bac PC, BIOF) — https://talamidi.com/Cours/Maroc/Lycée/2Bac/Sciences Physiques/Mathématiques (BIOF)/Fonctions primitives/Cours/Talamidi.com_fonctions-primitives-cours-1.pdf (vu dans les résultats ; 404 à l'ouverture)
- Monstremath, « Cours 04 Fonctions primitives 2 BAC Sciences pc et svt » — https://monstremath.com/2Bac/2eme-BAC-Sciences-Physiques-et-svt/cours-mathematique-2bac-sciences-experimentales/ (vu dans les résultats ; 503 à l'ouverture)
### Reste douteux
- pente.html dessine les tangentes horizontales de F en blanc, alors que le lexique maths veut la tangente en orange : le cahier suit le lexique (orange).
- Les bulles de diapositive (`concentration.cahier_figures` de pr_e5, pr_e6, pr_u6, pr_g1, pr_g2) gardent les anciennes couleurs et les anciennes courbes : elles sont hors de mon périmètre et sont à aligner sur les figures de bloc. Pour pr_g2, la bulle montre le tableau de x² − 1, alors que le bloc montre maintenant celui de 3 − x (pr_g3).
- La copie `en_attente/` n'est pas touchée (hors périmètre).
- « 1 + tan²x → tan x » est gardé « pour mémoire » : il faut vérifier s'il fait partie du cadre PC.
- Le vérificateur n'a rien signalé sur le champ `partie` (0 erreur, 0 avertissement).


## math_ch5_fonctions_ln — Fonctions logarithmiques
**Blocs touchés** : les 23 blocs (ln_s0_b1 … ln_s5_b2, ln_bloc_fin_cours) : texte du cahier ; figures redessinées dans ln_s1_b2, ln_s1_b3, ln_s2_b2, ln_s3_b2, ln_s3_b3, ln_s4_b2, ln_s4_b3, ln_s5_b1e, ln_s5_b1d, ln_s5_b1b, ln_s5_b1c
### Écarts trouvés avec les animations
- Toutes les courbes de ln : elles étaient cyan dans le cahier, alors que la courbe de ln est rouge dans tout le cours (courbe.html, produit.html, limites.html, inegalite.html ; exception du lexique) → passées en rouge.
- ln_s1_b2 / ln_c2 (courbe.html?vue=signe) : la partie négative était rose ; dans l'animation elle est orange, la partie positive verte et le point (1 ; 0) jaune → corrigé.
- ln_s1_b3 / ln_c3, ln_c5 (courbe.html?vue=e, tangente) : la tangente (T) était jaune ; l'animation la trace en orange → (T) orange, (1 ; 0) et e jaunes.
- ln_s2_b2 / ln_a2 (produit.html?vue=translation) : ln(2x) était jaune et les flèches « + ln 2 » vertes ; l'animation trace ln en rouge, ln(2x) en cyan et les flèches en jaune, avec « en x = 2 : ln 4 = ln 2 + ln 2 » → corrigé, légende alignée.
- ln_s3_b2 / ln_l2 (limites.html?vue=plonge) : l'asymptote x = 0 n'était qu'un texte jaune → asymptote dessinée en pointillé blanc et flèche orange de la plongée, comme dans l'animation.
- ln_s3_b3 / ln_l4 (limites.html?vue=zero_plus) : le cahier traçait la courbe y = x ln x, que l'animation ne montre pas. L'animation construit le rectangle de côtés x et |ln x| et le tableau 0,1 → −0,23 ; 0,01 → −0,046 ; 0,001 → −0,0069 → 0 → figure remplacée par ce tableau et ce rectangle (valeurs vérifiées en Python).
- ln_s4_b2 / ln_v3 (signe.html?vue=derivee) : le tableau n'avait aucune valeur ; l'animation écrit f(e) au sommet → « f(e) » ajouté.
- ln_s4_b3 / ln_e1 (inegalite.html) : le cahier écrivait +∞ aux deux bouts de g, valeurs que l'animation n'écrit pas (seulement 0 au minimum) → +∞ retirés.
- ln_s5_b1e, ln_s5_b1d / 2019 (etude.html?vue=position, construire.html?vue=c19) : (Δ) était en pointillé ; l'animation la trace en jaune plein, avec l'asymptote x = 0 en pointillé blanc, le minimum blanc à tangente horizontale, (e ; e) vert avec sa tangente verte et I rose → corrigé. (C) passe en cyan.
- ln_s5_b1b / 2021 (construire.html?vue=c21) : y = x était jaune en pointillé et nommée (Δ) ; l'animation la trace en orange plein, nommée « y = x », avec le minimum (1 ; −2) jaune à tangente horizontale, e vert, e^{3/2} orange et la demi-tangente verticale en O → corrigé.
- ln_s5_b1c (diapositives sans animation) : asymptotes et textes passés en blanc (lexique), I en jaune.
### Améliorations du texte (architecture)
- Plan à la manière des cours marocains : I. Fonction logarithme népérien, II. La courbe de ln, III. Ensemble de définition, IV. Propriétés algébriques, V. Équations, inéquations, systèmes, VI. Limites de la fonction ln, VII. Dérivée de ln(u(x)), VIII. Primitives de u′/u, IX. Étude de fonctions, X. Le logarithme décimal, XI. Bilan. Chaque titre est sur sa propre ligne (avant : « I. 1. », « IV. 1. (suite) », « IX. 2. e) »…).
- Définition écrite comme au national : « la fonction logarithme népérien, notée ln, est la primitive de x ↦ 1/x sur ]0 ; +∞[ qui s'annule en 1 ».
- Conditions complétées : a > 0 et b > 0 ; u dérivable et u > 0 ou u ≠ 0 sur I ; primitives « x ↦ ln|u(x)| + k » ; log défini pour x > 0 ; produit nul avec x > 0 ; f″ et la concavité.
- Le problème 2021 (6 lignes) et l'étude de ln((x + 2)/(1 − x)) sont coupés en deux parties numérotées. Chaque partie fait 5 lignes au plus.
- Bloc de fin de cours coupé en 3 lignes.
### Sources en ligne consultées
- Cours « Fonctions logarithmiques », Said Cherif (I. Fonction ln : 1) Définition, 2) Premières propriétés, 3) Relations, 4) Étude ; II. Fonctions composées ; III. Logarithme de base a, log décimal) — https://moutamadris.ma/wp-content/uploads/2022/04/cours-Fonctions-logarithmiques-1.pdf (ouvert)
- Résumé « الدوال اللوغاريتمية » 2 Bac sciences expérimentales — https://www.dreamjob.ma/wp-content/uploads/2023/01/fonctions-logarithmes-cours-resume-maths-2bac.pdf (ouvert)
- Talamidi, « fonctions logarithmiques résumé de cours 4 » (2 Bac PC, BIOF) — https://talamidi.com/Cours/Maroc/Lycée/2Bac/Sciences Physiques/Mathématiques (BIOF)/Fonctions logarithmiques/Cours/Talamidi.com_fonctions-logarithmiques-resume-de-cours-4.pdf (vu dans les résultats)
### Reste douteux
- Le cahier de ln_s4_b2 écrit f′(x) = (x − 1 + ln x)/x pour le problème 2019, puis ln_s5_b1 écrit f′(x) = g(x)/x². C'est cohérent si g(x) = x(x − 1 + ln x), mais à vérifier sur l'énoncé.
- Les bulles de diapositive (`concentration.cahier_figures`) gardent les anciennes couleurs (ln en cyan, tangente jaune, courbe x ln x) : elles sont hors de mon périmètre et sont à aligner.
- La copie `en_attente/` n'est pas touchée.
- « 10ˣ » (ln_g2) est employé avant le chapitre de l'exponentielle : à vérifier dans le cadre.


## math_ch6_nombres_complexes — Nombres complexes (première partie)
**Blocs touchés** : nc_s1_b0 (figure), nc_s2_b1 (figure), nc_s2_b1b, nc_s2_b2 (figure), nc_s2_b2b, nc_s2_b3, nc_s2_b3b, nc_s2_b3c, nc_s3_b1 (figure), nc_s3_b2 (figure), nc_s3_b2b, nc_s3_b3, nc_s3_b3b (figure), nc_s4_b1, nc_s4_b2, nc_s4_b2b (figure), nc_s4_b3, nc_s4_b4, nc_bloc_fin_cours
### Écarts trouvés avec les animations
- nc_s2_b3c / nc_m5 (module.html?vue=cercle) : le cahier dessinait le cercle |z − 2i| = 3, que l'animation ne montre pas. L'animation montre le cercle de centre O et de rayon 5, avec M en 3 + 4i, −3 + 4i, 5i et −5, et « |z| = 5 » → figure refaite (|z − 0| = 5).
- nc_s3_b1 / nc_g1 (argument.html?vue=angle, t = 60° par défaut) : M était placé en (2,5 ; 1,8), soit θ ≈ 36° → M = 2(cos π/3 + i sin π/3), sur le cercle de rayon 2, |z| = 2, arc θ jaune.
- nc_s4_b2b / nc_i4 (alignement.html?vue=triangle) : le triangle isocèle rectangle était a = 1 + i, b = 3 + 2i, c = 3i ; l'animation utilise A(1,6 + 0,6i), B(3 + i), C(1,2 + 2i). Le quotient vaut i dans les deux cas (vérifié) → figure refaite avec les points de l'animation.
- nc_s3_b2 / nc_t3 (trig.html?vue=signes) : le cahier ajoutait √3 + i en pointillé et un arc vert π/6, absents de l'animation → seuls restent OM cyan, « 2 » jaune et l'arc jaune 5π/6.
- nc_s3_b2b / nc_t3_b (etapes.html?vue=quarts) : les trois autres quarts étaient tous jaunes, sans leur arc ; l'animation les distingue : π/6 cyan, 5π/6 jaune, 7π/6 vert, −π/6 orange, chacun avec son segment et son arc → corrigé, avec les étiquettes d'angle de l'animation.
- nc_s2_b1b / nc_p5 (vecteur.html?vue=vecteur) : le cahier n'avait pas OM′ (jaune) et sa diagonale était étiquetée sans le calcul ; l'animation trace OM cyan, OM′ jaune, OB vert « z + z′ » → figure corrigée, et une ligne ajoutée au texte : z_M + z_{M′} = 4 − i.
- nc_s2_b1 / nc_a3 (plan.html?vue=placer) : l'animation avance de 3 (flèche verte) puis monte de 2 (flèche orange) jusqu'à M cyan, et dessine u, v en cyan → figure refaite ainsi.
- nc_s2_b3 / nc_m1 (module.html?vue=triangle) : OM était jaune ; l'animation trace OH vert, HM orange et OM cyan → corrigé.
- nc_s4_b3 / nc_n1 (alignement.html?vue=n2023) : le cahier dessinait la droite (DB) jaune et OC⃗ cyan ; l'animation trace OA et l'arc π/4 en cyan, les flèches D→B et B→C (b − d = c) en jaune, A→B en cyan et la droite (AB) en pointillé vert passant par D → refait.
- Couleurs des points alignées sur les animations : conjugué (nc_j1 : M cyan, M′ jaune), × i (nc_r2 : 3 + i cyan), ΩA = ΩB (nc_i2 : A et B cyan, Ω jaune, pointillé A–B), i (nc_a2 : −i jaune).
### Améliorations du texte (architecture)
- Plan conforme aux résumés marocains : ensemble ℂ et forme algébrique, plan complexe, conjugué, module, argument et forme trigonométrique, interprétations géométriques. Les titres romains étaient déjà sur leur propre ligne ; « X. Deux sujets nationaux. 2023 N : … » est séparé en titre puis « 1. ».
- Numérotation rendue continue : IV. 4. à 6., V. 2. et 5. à 6., VII. 3. à 6., VIII. 6., X. 1. à 3. Les blocs qui commençaient sans numéro commencent maintenant par « n. ».
- Parties trop longues coupées : ensembles de points / « Z réel » ; sujet 2023 N.
- Conditions ajoutées : a, b réels pour z·z̄ ; [2π] sur chaque argument ; « |b| = |1 + i| × |a| ».
- Le nombre de lignes ne vaut plus le nombre de diapositives (nc_s3_b3, nc_s4_b1, nc_s4_b3, nc_s4_b4). Bloc de fin coupé en 3 lignes.
### Sources en ligne consultées
- Résumé de cours « Nombres complexes », Atmani Najib, 2ᵉ Bac Sc. ex. (A) L'ensemble ℂ ; B) Interprétation géométrique ; C) Conjugué ; D) Module ; E) Argument, forme trigonométrique ; F) Interprétations géométriques) — https://moutamadris.ma/wp-content/uploads/2022/06/resume-Nombres-complexes-12-2bac-Sciences-Physiques-et-svt-1.pdf (ouvert)
- Talamidi, « nombres complexes 1 résumé de cours 1 » (2 Bac PC, BIOF) — https://talamidi.com/Cours/Maroc/Lycée/2Bac/Sciences Physiques/Mathématiques (BIOF)/Nombres complexes (Partie 1)/Cours/Talamidi.com_nombres-complexes-1-resume-de-cours-1.pdf (vu dans les résultats)
- AlloSchool, « Nombres complexes – Partie 1 (Cours) » — https://alloschool.com/element/132806/pdf (vu dans les résultats)
### Reste douteux
- L'exemple écrit |2z − 4i| = 6 (cercle de centre 2i, de rayon 3) vient de screen_content ; l'animation de nc_m5 montre un autre cercle (|z| = 5). Je l'ai gardé dans le texte, mais le dessin suit l'animation.
- Les bulles de diapositive (`concentration.cahier_figures`) gardent les anciennes figures (cercle 2i, M en (2,5 ; 1,8), triangle 1 + i…) : elles sont hors de mon périmètre et sont à aligner.
- La copie `en_attente/` n'est pas touchée.
- Le vérificateur n'a rien signalé sur le champ `partie`.


## phys_ch1_waves_exemple — Ondes mécaniques progressives
**Blocs touchés** : wx_s1_b1 : Une perturbation qui avance sans transporter la matière, wx_s1_b2 : Transversale ou longitudinale, et le son, wx_s1_b2b : La vitesse, puis la célérité, wx_s1_b3 : Le retard, l'élongation, la durée et la longueur, wx_s1_b3b : Lire une onde : aspect ou élongation, wx_s2_b1 : Mesurer la célérité (deux micros), wx_s2_b1b : L'écho, puis rédiger, wx_s4_b1 (2022 N), wx_s4_b1b (2024 R), wx_s4_b1c (2024 N), wx_s4_b1d (2022 R), wx_s4_b2 (2021 R), wx_s4_b2b (2020 R), wx_s4_b2c (2018 N), wx_s2_b2 : Reconnaître le cas, wx_s4_b3 : Bilan, wx_bloc_fin_cours
### Écarts trouvés avec les animations
- wx_s1_b1 / corde.html?vue=point : S jaune, M vert, flèche « v » jaune, cote y faible, impulsion symétrique → S cyan, M orange (perle du lexique), « sens de propagation » vert, cote y jaune, trajet de M orange ; impulsion dissymétrique de la page (montée rapide sur 30 % de θ, descente lente), photo à t = 0,6 s.
- wx_s1_b2 / types.html : mouvement de M coté en vert → orange (flèches de M de la page) ; titres « ⊥ / ∥ » comme à l'écran.
- wx_s1_b3 / corde.html?vue=retard et ?vue=longueur : figure « aspect » sur x = 0 → 9 m avec L = 3 m (valeurs absentes de l'animation) → remplacée par la photo à t = 1,1 s (v = 1,0 m/s, θ = 0,4 s : queue 0,7 m rose, front 1,1 m jaune, L = 0,40 m, M à 0,5 m orange) ; ajout de la figure du retard que l'animation montre et que le cahier omettait : y_S(t) cyan et y_M(t) orange décalée de τ = 0,80 s (SM = 0,80 m). Courbes vérifiées en Python contre forme() de la page.
- wx_s1_b3b / corde.html?vue=aspect et ?vue=sens : film de M en cyan, axe t de 0 à 9 s, τ = 2 s → orange, M à x = 0,5 m, τ = 0,5 s, θ = 0,4 s, flèche « front : à gauche » jaune ; ajout de la figure « sens » (t = 1,1 s, A à 1,05 m monte en vert, B à 0,85 m descend en rose), montrée par l'animation.
- wx_s2_b1 / micros.html : oscillogramme avec τ = 3 ms, signaux de période 0,5 ms, M₂ jaune, cote τ orange → 0,5 ms/div, M₁ démarre à 0,25 ms (cyan), M₂ à 2,25 ms (orange), salve 4 kHz amortie (0,16 ms), τ = 4 div = 2 ms (cote jaune) ; exemple d = 0,68 m → v = 340 m/s ajouté au texte.
- wx_s1_b2b / corde.html?vue=front et milieux.html : exemple de l'animation ajouté (d = 0,80 m de front à front en 0,8 s → 1,0 m/s ; sur 1 km : 0,2 s, 0,67 s, 2,9 s).
- wx_s2_b1b / sonar.html : exemple de la page ajouté (v = 1500 m/s, τ = 40 ms → d = 30 m).
- wx_s4_b1b / national.html (2024 R) : M₂ cyan, E jaune, salves orange, ℓ et d − ℓ verts, E placé à 36 % de d → M₂ orange (voie B), émetteur blanc, salve jaune, ℓ cyan, E à ℓ/d = 1,085/2,85 = 38 %.
- wx_s4_b1d / national.html (2022 R) : courbe cyan, graduations 10/30/50 → trace orange de la page, graduations 10/25/35/45 et ±3/±6 mm, cote τ jaune ; « v = SM/τ » → « v = L/τ » (notation de l'animation et du sujet).
- wx_s4_b2 / national.html (2021 R) : droite cyan sans les mesures → droite verte, cinq points orange (10 → 50 cm), lecture (40 cm ; 0,08 ms) en jaune.
### Améliorations du texte (architecture)
- Plan lisible par le lecteur : titre romain sur sa ligne (titres des activités : I. … VIII.) puis « 1. », « 2. »… continus dans chaque partie (« I.1 », « II.0 »… ne découpaient rien) ; chaque partie ≤ 5 lignes ≤ ~90 caractères ; `partie` posé sur les figures des blocs à deux parties.
- Ordre et formulations inspirés des cours marocains : définition de l'onde « propagation d'une perturbation dans un milieu matériel élastique, avec transport d'énergie, sans transport de matière » ; transversale / longitudinale par la direction de la perturbation ; le son (bougie, cloche à vide) conclu par « Donc » ; célérité « ne dépend ni de l'amplitude ni de la forme de la perturbation » ; retard « M reproduit le mouvement de S avec le retard τ ».
- Unités regroupées avec chaque relation ; « Exemple » chiffré repris de l'animation à chaque notion ; méthodes numérotées (oscilloscope, aspect à la date t, rédaction en 4 temps) ; ligne de fin de cours coupée en trois lignes courtes.
### Sources en ligne consultées
- Chapitre I : ondes mécaniques progressives (Pr. El Kaouahi, 2e Bac international) — https://moutamadris.ma/wp-content/uploads/2022/07/cours-Ondes-mecaniques-progressives-2bac-BIOF-Sciences-Mathematiques-A%E2%80%AF%E2%80%93B-et-Sciences-Physiques-5.pdf
- Cours PC 2 Bac SP international (ondes mécaniques, activités) — https://moutamadris.ma/wp-content/uploads/2020/03/cours-pc-2bac-sp-international-fr-1-2.pdf
- Kartable, les ondes mécaniques (vu dans les résultats de recherche) — https://kartable.fr/ressources/physique-chimie/cours/les-ondes-mecaniques/51307
### Reste douteux
- Le point M est rouge dans types.html (perle orange dans corde.html et le lexique) ; le cahier suit le lexique (orange).
- La courbe y_M(t) est orange dans national.html (2022 R) mais cyan dans la même vue du chapitre 2 (ondes-periodiques-tableau/national.html) : couleur à unifier côté animations.
- Les bulles de diapositive (`concentration.cahier_figures`) n'ont pas été touchées (hors périmètre) : elles gardent les anciennes couleurs/valeurs (aspect sur 0–9 m, M vert…).
- `verifier_figures_cahier.py` ne contrôle pas les champs au niveau de la figure : `partie` n'est pas signalé (0 erreur, 0 avertissement).


## phys_ch2_ondes_periodiques — Ondes mécaniques progressives périodiques
**Blocs touchés** : op_s1_b1 : Une source qui vibre sans arrêt, op_s1_b2 : Onde périodique, sinusoïdale, et la période T, op_s1_b3 : Même période partout, et N = 1/T, op_s2_b1 : Convertir, lire T, op_s2_b2 : La longueur d'onde λ, op_s2_b3 : Les rides de la cuve, op_s3_b1 : Pendant une période, l'onde avance de λ, op_s3_b2 : En phase, en opposition de phase, op_s5_b1 : Le retard, op_s5_b1b : National 2022 R, op_s3_b3 : Le stroboscope et les deux récepteurs, op_s4_b1 : Mesurer T et λ avec deux récepteurs, op_s4_b2 : La diffraction, op_s4_b3 : Le son se diffracte ; milieu dispersif, op_s5_b2 : National 2017, op_s5_b3 : National 2020, op_s6_b1 : Le devoir sur la cuve, op_s6_b2 : Le bilan, op_bloc_fin_cours
### Écarts trouvés avec les animations
- op_s1_b2 / corde.html?vue=periode : film tracé en cyan depuis t = 0 (comme la source) → film du point M (x = 0,75 m) en rouge, au repos jusqu'à 0,75 s, crêtes 0,875 s et 1,375 s, T = 0,5 s (jaune).
- op_s2_b1 / sons.html : guitare tracée avec d'autres harmoniques (0,8 / 0,5 / 0,3, sans phase) → la fonction de la page (sin + 0,55 sin(2·+0,9) + 0,32 sin(3·+2,1))/1,55 ; titres « voie 1 / voie 2 » ; exemple de national.html?vue=oscillo ajouté (0,1 ms/div, 5 div → T = 0,5 ms, N = 2000 Hz).
- op_s2_b2 / corde.html?vue=lambda : photo avec un front à 1,1 m (corde à moitié parcourue) → photo de la page à t = 2,125 s, corde entière, crêtes 0,5 et 1,0 m (jaune), creux rose, λ = 0,5 m.
- op_s2_b3 / cuve.html?vue=compter : traits cyan → traits clairs (blanc) ; « n = 3 intervalles » en orange comme à l'écran.
- op_s3_b2 / corde.html?vue=phase : x en cm (λ = 4 cm), M et P verts → échelle de la page (λ = 0,5 m), M rouge (0,75 m), P violet (1,25 m), Q = 1er creux après M en rose (numérotés en rose par la page), photo au moment où M est sur une crête (t = 2,875 s).
- op_s5_b1 / national.html?vue=2022 : graduations 10/15/35, x jusqu'à 62 ms, τ orange → graduations 10/25/35/45 ms de la page, ±3/±6 mm, τ, T et amplitude 6 mm en jaune.
- op_s4_b2 / fente.html?vue=etroite : a non chiffrée et dessinée à 0,5 λ → a = 1 cm, λ = 1,5 cm (échelle respectée), règle « λ avant » orange et « λ après » rose comme dans la page.
- op_s4_b3 / ultrasons.html : a en jaune, « E (40 kHz) » sans couleur, arc de R orange → a orange, N = 40 kHz cyan, arc et R jaunes.
- op_s5_b1 : exemple de l'animation ajouté (SM = 0,75 m = 1,5 λ → τ = 1,5 T, opposition avec S) ; op_s5_b2 : valeurs 2017 de la page ajoutées (λ = 4 cm, N = 50 Hz, v = 2 m/s, SM = 6 cm, τ = 0,03 s).
### Améliorations du texte (architecture)
- Plan des cours marocains (onde périodique → sinusoïdale → période/fréquence → longueur d'onde et double périodicité → λ = v·T → phase/opposition → retard → mesures (stroboscope, récepteurs) → diffraction → milieu dispersif → cas types → bilan) avec les titres romains des activités et une numérotation « 1. 2. » continue par partie (les « I.1 », « VII.4 »… ne découpaient pas le cahier ; les définitions de l'onde périodique et sinusoïdale, avant sans numéro, sont maintenant I.1 et I.2).
- Définitions reformulées comme au national : onde périodique (chaque point reproduit le même mouvement à intervalles de temps égaux), période (plus petite durée pour retrouver le même état vibratoire), longueur d'onde (plus petite distance entre deux points dans le même état vibratoire), milieu dispersif (célérité dépendant de la fréquence) ; conditions a ≤ λ pour la diffraction.
- Lignes ramenées sous ~90 caractères, parties ≤ 5 lignes, `partie` posé sur chaque figure ; ligne de fin de cours coupée en trois.
### Sources en ligne consultées
- Ondes mécaniques progressives périodiques (Bendaoud, 2e Bac BIOF) — https://moutamadris.ma/wp-content/uploads/2022/07/cours-Ondes-mecaniques-progressives-periodiques-2bac-BIOF-Sciences-Mathematiques-A%E2%80%AF%E2%80%93B-et-Sciences-Physiques-2.pdf
- Cours PC 2 Bac SP international (ondes périodiques, diffraction) — https://moutamadris.ma/wp-content/uploads/2020/03/cours-pc-2bac-sp-international-fr-2-3.pdf
- Ondes mécaniques progressives périodiques, cours LaTeX (AlloSchool, vu dans les résultats ; PDF non lisible) — https://www.alloschool.com/assets/documents/course-421/ondes-mecaniques-progressives-periodiques-cours-latex.pdf
### Reste douteux
- P est violet dans corde.html?vue=phase mais orange dans methode-phase.html (même diapositive de méthode) ; M rouge ici alors que le lexique (corde.md) dit perle orange : le cahier suit corde.html.
- La courbe y_M(t) de 2022 R est cyan ici, orange dans ondes-tableau/national.html (chapitre 1).
- Bulles de diapositive (`concentration.cahier_figures`) non touchées (hors périmètre).
- `verifier_figures_cahier.py` ne signale pas le champ `partie` (pas de contrôle au niveau de la figure).


## phys_ch3_ondes_lumineuses — Propagation d'une onde lumineuse
**Blocs touchés** : ol_s1_b1 : La lumière ne va pas toujours tout droit, ol_s1_b2 : L'aspect ondulatoire, le montage, le fil, ol_s1_b3r : L'angle en radian, puis θ, ol_s1_b3 : θ = λ/a, ol_s2_bt : La tangente, le triangle du montage, ol_s2_b1 : Le petit angle, ol_s2_b2 : Calculer λ, établir L, ol_s2_b3 : Qui change ?, ol_s3_b1 : Deux expériences, le cheveu, ol_s3_b2 : La pente, ol_s3_b2b : Identifier k, ol_s3_b3r : Une radiation, c, ol_s3_b3 : λ₀ = c/ν et le spectre, ol_s4_b1 : Dans le verre, ol_s4_b2 : L'indice n, ol_s4_b3 : Le prisme, ol_s4_b4 : Milieu dispersif, ol_s5_b1 à ol_s5_b1h : le national, ol_s5_b2 : Bilan, ol_bloc_fin_cours
### Écarts trouvés avec les animations
- ol_s1_b1 / diffraction.html?vue=figure : cote L jaune et sans valeur → orange (couleur de la page), L = 2,6 cm (650 nm, a = 0,10 mm, D = 2,0 m).
- ol_s1_b2 / diffraction.html?vue=mesure : D coté en cyan → orange comme dans la page (L orange déjà).
- ol_s1_b3r / ecart-angulaire.html : rayons rouges et θ jaune → axe vers le centre blanc, rayon vers le bord jaune, bord marqué en rose, θ en orange.
- ol_s2_bt / ecart-angulaire.html?vue=triangle : triangle blanc, θ jaune, L/2 orange, angle droit faible → triangle jaune, θ orange, L/2 rose, D cyan, angle droit blanc.
- ol_s3_b2 et ol_s3_b2b / courbe.html : droites cyan → vertes (droite de la page), graduations 5/10/15/20 ; L = f(D) de courbe.html?courbe=L_D tracée avec D en cm → D en m (0,5 → 2,0 m) comme la page, k = (4·10⁻² m)/(2 m).
- ol_s5_b1e / national.html?vue=2021c : points jaunes, droite cyan → points cyan, droite verte, k en rose (D reste en cm, comme cette page).
- ol_s3_b3 / spectre.html : bandes violet/bleu/vert/jaune-orange aux bornes 450/500/570/620 nm → bornes du lexique et de la page (445, 490, 570, 590, 620 nm), jaune et orange séparés.
- ol_s4_b1 / milieu.html : onde de 600 nm dessinée en rouge → orange (couleurDe(600) et nomCouleur du lexique).
- ol_s4_b3 / prisme-dispersion.html : rayon incident horizontal (i ≈ 30°) et déviations 32° / 53° → i = 55°, A = 60°, n dessinés 1,585 (rouge) et 1,685 (violet) de la page : sorties à −20° et −30°, déviations 45° et 55° (calculées).
### Améliorations du texte (architecture)
- Titres romains des activités (I. Diffraction … X. Bilan) écrits sur leur ligne au début de chaque partie : la numérotation « 1. 2. » qui repartait à 1 sans titre devient lisible (plan proche des cours marocains : diffraction et conclusion « aspect ondulatoire » → écart angulaire θ = λ/a → L = 2λD/a → exploitation → onde électromagnétique, monochromatique / polychromatique, c, λ₀ = c/ν → indice n = c/v → dispersion par le prisme, milieu dispersif).
- Définitions coupées en lignes ≤ ~90 caractères (écart angulaire, lumière monochromatique, onde électromagnétique) ; une partie qui débordait (V.2/V.3) réordonnée ; renvoi « méthode III.7 » écrit « (III, point 7) » pour ne pas être pris pour une partie.
- Exemples tirés des animations ajoutés (L = 2,6 cm ; verre λ₀ = 600 nm → 400 nm ; eau n = 2,4/1,8) ; `partie` posé sur les figures des blocs à plusieurs parties ; ligne de fin de cours coupée en trois.
### Sources en ligne consultées
- Propagation des ondes lumineuses (Pr. Sbiro, 2e Bac BIOF) — https://moutamadris.ma/wp-content/uploads/2022/07/cours-Propagation-des-ondes-lumineuses-2bac-BIOF-Sciences-Mathematiques-A%E2%80%AF%E2%80%93B-et-Sciences-Physiques-5.pdf
- Résumé Propagation des ondes lumineuses 2 Bac BIOF (vu dans les résultats de recherche) — https://moutamadris.ma/wp-content/uploads/2022/07/resume-Propagation-des-ondes-lumineuses-2bac-BIOF-Sciences-Mathematiques-A –B-et-Sciences-Physiques-1.pdf
- Cours de N. Naceiri Mrabti, ondes lumineuses (vu dans les résultats de recherche) — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/ONDES/livre Tom 1-29-34.pdf
### Reste douteux
- D est orange dans diffraction.html mais cyan dans ecart-angulaire.html ; θ est rose dans diffraction.html, orange dans ecart-angulaire.html : le cahier suit chaque fois la page de la diapositive ; couleurs à unifier dans les animations.
- diffraction.html nomme les couleurs avec d'autres seuils (violet < 425, vert < 560 nm) que spectre.html et le lexique (445, 570) : copie de `nomCouleur` à remplacer (déjà listé dans le lexique).
- courbe.html (L = f(D), D en m) et national.html 2021c (D en cm) montrent la même courbe en deux unités.
- Bulles de diapositive (`concentration.cahier_figures`) non touchées (hors périmètre).
- `verifier_figures_cahier.py` ne signale pas le champ `partie` (pas de contrôle au niveau de la figure).


## phys_ch4_radioactivite — Décroissance radioactive
**Blocs touchés** : les 25 blocs (ra_s1_b1 … ra_s8_b3, ra_bloc_fin_cours) — texte renuméroté et découpé en parties ; figures de ra_s1_b3, ra_s3_b1, ra_s3_b3, ra_s4_b1, ra_s4_b3, ra_s5_b1, ra_s6_b1, ra_s6_b2 corrigées (champ `partie` ajouté).
### Écarts trouvés avec les animations
- ra_s1_b3 / segre.html?vue=vallee : vallée tracée en vert (l'animation : bande des noyaux stables sur halo blanc ; vert = légers N ≈ Z, orange = lourds N > Z, ²⁰⁸Pb N = 126) → vallée blanche, « légers : N ≈ Z » vert, point ²⁰⁸Pb orange (82 ; 126), graduation N = 126.
- ra_s1_b3 / segre.html?vue=isotopes : point « instable » au-dessus de la vallée en orange (orange = zone β⁺ dans l'animation ; au-dessus = β⁻ bleu) → nouvelle figure fidèle au zoom de l'animation : verticale Z = 6 jaune, ¹²C (6 ; 6) vert « stable », ¹⁴C (6 ; 8) bleu « → β⁻ ».
- ra_s3_b1 / segre.html?vue=zones : vallée verte → blanche ; « noyaux lourds » sans seuil → « Z > 82 » (repère x = 82), comme ZONE_TXT de l'animation. Flèches β⁻ bleu, β⁺ orange, α jaune : conformes.
- ra_s3_b3 (population.html) et ra_s4_b3, ra_s5_b1, ra_s6_b1 (courbe.html) : courbes N(t) et a(t) en cyan → jaune (craie jaune de l'animation) ; N₀/a₀ en vert, N₀/2 et paliers en cyan, comme la colonne « Lecture ».
- ra_s4_b3 / courbe.html?courbe=N : tangente à l'origine en jaune pointillé → orange plein (couleur de la tangente et de τ dans l'animation) ; τ marqué ; N_d orange et N jaune comme population.html?vue=restants.
- ra_s4_b1 / rappels.html?vue=exp : e^(−x) en cyan → blanc (craie blanche de l'animation), e⁰ = 1 jaune.
- ra_s6_b1 / courbe.html?courbe=ln : droite cyan → jaune, ln N₀ = 33 vert, Δt = 200 j et la pente en orange, point (200 ; 23,3) comme l'animation ; la légende citait « phosphore 32 », absent de l'animation → « 2021 R ». Méthode a(t) : « τ par la tangente ou 0,37·a₀ » retiré (l'animation activite_2022 ne le montre pas) ; λ = ln2/t½ en s⁻¹ ajouté.
- ra_s6_b2 / datation.html : courbe → jaune ; graduation a₀ = 418 Bq ajoutée.
- ra_s3_b2 / figures.html?fig=fig_soddy_systeme : notation conforme (y = nombre de α, x = nombre de β⁻) ; « Lire une flèche » conservé.
- ra_s7_b3 / national.html?vue=pu2021 : λ ≈ 2,49·10⁻¹⁰ s⁻¹ (montré par l'animation) manquait → ajouté ; Soddy A = 234, Z = 92 détaillé.
- ra_s8_b2 / national.html?vue=cd2025 : le titre annonce N₀ mais le cahier ne le donnait pas → λ ≈ 2,78·10⁻⁵ s⁻¹, N₀ = a₀/λ ≈ 4,5·10¹⁶ ajoutés (valeurs de l'animation).
- Valeurs recalculées en Python : N₀ = 8,0·10²⁰, t½ = 8 j, τ = 11,54 j, N(τ) = 2,94·10²⁰ ; 400/200/100/50 ; ln N = 33 − 0,0485 t (23,3 à 200 j) ; 2,26·10³ ans ; 45 ans ; 34,6 j ; 5,6·10¹⁵ ; vallée N = Z + 0,0065 Z² (écart ≤ 1,5 à la moyenne des noyaux stables de segre.html).
### Améliorations du texte (architecture)
- Plan à titres romains continu, comme les cours marocains consultés : I. Le noyau atomique et sa stabilité (1–6) ; II. La radioactivité (1–12 : définition, caractères, Soddy, α, β⁻, β⁺, γ, méthodes, diagramme, famille) ; III. La loi de décroissance (1–8) ; IV. L'activité (1–7) ; V. Application : la datation (1–3) ; VI. Exercices du national (1–7) ; VII. Bilan.
- Chaque bloc commence par une ligne « n. » (ou un titre romain puis « 1. ») ; numérotation reprise d'un bloc à l'autre ; aucune ligne « 1.1 ».
- Lignes ramenées à ≤ 90 caractères, parties de 1 à 5 lignes ; définitions « Définition : » (isotopes, radioactivité, famille, demi-vie, activité) formulées comme au national.
- Ajouts : unité Bq rappelée, piège « 95 % désintégrés ≠ N = 0,95·N₀ », roche : ²³⁸U (t½ = 4,5·10⁹ ans) / ²⁰⁶Pb (diapositive ra_c4_fils_pere).
### Sources en ligne consultées
- Décroissance radioactive (cours PC, plan I. Le noyau / II. Radioactivité / III. Décroissance / IV. Datation) — https://kezakoo.com/wp-content/uploads/2024/11/Decroissance-radioactive-PC.pdf
- N. Naceiri Mrabti, 2 BAC BIOF, fiches nucléaire (loi de décroissance, t½, activité) — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/nucleaires/livre%20Tom%201-41-43.pdf
- Talamidi, décroissance radioactive, exercices (vu dans les résultats) — https://talamidi.com/Cours/Maroc/Lycée/2Bac/Sciences Mathématiques A/Physique et Chimie (BIOF)/Décroissance radioactive/Exercices/Talamidi.com_decroissance-radioactive-exercices-non-corriges-4.pdf
### Reste douteux
- Le champ `partie` des figures : le vérificateur ne le signale pas (0 erreur), il n'est pas contrôlé au niveau de la figure.
- « Pénétration α/β/γ » (ra_s2_b3) n'est montrée par aucune animation du bloc ; gardée (programme).
- Le lexique (proton.md) note encore les protons rouge/rouge-orangé dans la physique nucléaire « à remplacer » : non vérifié dans chaque page (hors cahier).


## phys_ch5_energie_nucleaire — Noyaux, masse et énergie
**Blocs touchés** : les 16 blocs (en_s1_b0 … en_s4_b3, en_bloc_fin_cours) — texte renuméroté ; figures de en_s1_b3, en_s2_b2, en_s3_b3, en_s4_b2 (champ `partie` ajouté).
### Écarts trouvés avec les animations
- en_s2_b2 / aston.html : courbe d'Aston du cahier en cyan, passant par 14 points et sautant ⁴He (7,07), ⁷Li, ¹⁴C… → polyligne lisse par les 21 points exacts de l'animation (NOYAUX), en vert ; fer entouré orange (⁵⁶Fe), fission en violet (était rose), fusion orange ; flèche rose « plus stable » vers le bas ajoutée (moment plus_stable) ; graduations 20 / 56 / 190 / 238.
- en_s2_b1 / figures.html?fig=fig_stabilite : l'exemple du cahier (²³⁵U contre ⁵⁶Fe) n'est pas celui de l'animation → exemple 2017 R de l'animation : ⁶⁰Ni 526,8/60 = 8,78 > ⁵⁶Ni 8,64 MeV/nucléon ; numérotation fautive « 2. » puis « 1. » corrigée.
- en_s1_b2 / balance.html : valeurs vérifiées (4,00150 < 4,03188 u ; ¹⁴C : 14,11296 − 13,99995 = 0,11301 u) et écrites en clair.
- en_s4_b2 (pénétration, sans animation) : α orange, β cyan → α jaune, β bleu, γ violet, comme segre.html / desintegration.html du chapitre précédent.
- en_s1_b3 (liaison.html), en_s3_b3 (diagramme.html : orange « on fournit », vert « on récupère », jaune ΔE = −17,455 MeV), en_s3_b2 (balance/national : −0,19834 u ; 17,6 MeV ; 2,82 MeV), en_s4_b1 (comparaison.html : 185/236 ≈ 0,78 ; 17,6/5 ≈ 3,5 ; 2,26·10¹⁵ MeV) : conformes.
### Améliorations du texte (architecture)
- Plan des cours marocains : I. Équivalence masse-énergie (1–4) ; II. Énergie de liaison du noyau (1. constat, 2. défaut de masse, 3. énergie de liaison, 4. par nucléon) ; III. Fission et fusion (1. courbe d'Aston, 2. spontanée/provoquée, 3. fission, 4. fusion, 5. Soddy) ; IV. Bilan énergétique d'une réaction (1–5) ; V. Applications, dangers et méthodes ; VI. Bilan.
- Définitions (défaut de masse, énergie de liaison, fission, fusion) écrites « Définition : » en deux lignes courtes ; lignes ≤ 90 caractères ; chaque bloc commence par « n. » ou titre romain + « 1. ».
### Sources en ligne consultées
- Noyaux, masse et énergie (cours PC : I. Équivalence masse-énergie, II. Énergie de liaison, III. Fusion et fission, IV. Énergie de réaction) — https://kezakoo.com/wp-content/uploads/2024/11/Noyaux-masse-et-energie-PC.pdf
- M. El Founani, Noyaux, masse et énergie (cours LaTeX, alloschool) — https://alloschool.com/assets/documents/course-423/noyaux-masse-et-energie-cours-latex.pdf
- moutamadris, cours Noyaux masse et énergie 2bac BIOF (vu dans les résultats ; téléchargement refusé) — https://moutamadris.ma/wp-content/uploads/2022/07/cours-Noyaux-masse-et-energie-2bac-BIOF-Sciences-Mathematiques-A –B-et-Sciences-Physiques-3.pdf
### Reste douteux
- Aston : valeurs de l'animation (²H 1,11 ; ³H 2,83) différentes de celles du sujet 2023 N cité dans le cahier (1,183 ; 2,825) : c'est normal (données de l'énoncé), les deux sont gardées.
- La diapositive « applications et dangers » n'a pas d'animation : la figure de pénétration n'a pas de référence animée.


## phys_ch6_dipole_RC — Dipôle RC
**Blocs touchés** : les 25 blocs (rc_s0_b1 … rc_s4_b4, rc_bloc_fin_cours) — plan romain ajouté, renumérotation ; figures des 13 blocs illustrés recolorées / refaites (champ `partie` ajouté).
### Écarts trouvés avec les animations
- rc_s1_b2 / intensite.html : courbe q(t) abstraite (4(1 − e^(−t)), axes en s et C) → valeurs de l'animation : Q = 2640 µC, τ = 0,22 s, t de 0 à 1,2 s ; tangente au point t = 0,2 s (pente ≈ 4,8 mA), palier i = 0.
- rc_s1_b3 / generateur-courant.html : points lus à t = 1 s et 5 s, axe 0–6 s → points de l'animation à 2 s et 6 s, axes 0–10 s / 0–10 V ; Δt = 4 s, Δu_C = 4 V, C = 1 µF.
- rc_s1_b1 / condensateur.html?vue=charge : la valeur E = 6 V de l'expérience manquait → ajoutée ; isolant rempli en jaune → sans remplissage.
- rc_s0_b2, rc_s1_b2a, rc_s2_b1 (schémas) : i en jaune, u_R et u_C en cyan → i rouge (rappels.html, figures.html : exception du ch6 du lexique), u_R vert, u_C rouge (lexique grandeurs-electriques) ; charges + rose / − bleu (lexique condensateur).
- rc_s4_b1 / courbe-charge.html?vue=tangente : tangente jaune → cyan ; rc_s3_b2 : points 0,63·E et 5τ jaunes → cyan (lignes de lecture cyan de l'animation) ; légende complétée (R = 1 kΩ, C = 220 µF, 5τ = 1,1 s).
- rc_s3_b3a / courbe-charge.html?vue=R et tau-rc.html : R = 2 kΩ tracée en bleu (bleu = décharge dans ce cours) → rouge pointillé (rouge pâli dans l'animation).
- rc_s3_b3 / continuite.html?vue=decharge : 0,37·E en jaune → vert ; la tangente à l'origine (montrée par l'animation au moment decharge_37) manquait → ajoutée en cyan.
- rc_s3_b4 / quatre-courbes.html?vue=descente : tangente jaune → cyan, 0,37·I₀ jaune → vert.
- rc_s4_b2 / figures.html?fig=fig_du_dt : ordonnée E/(RC) = 1000 V/s en vert ; exemple q = f(u) de fig_q_u (2018 N : C_eq = 10 µF, C₂ = 2,5 µF) ajouté au texte.
- rc_np_b2 / national-pas-a-pas.html : tangente (T) jaune → blanche (craie de l'animation).
- rc_s4_b3 / figures.html fig_n1_2019, fig_n2_2021R : lectures montrées par l'animation (Q = 100 µC, τ = 1 ms ; I₀ = 50 mA, τ = 12 ms) ajoutées.
- rc_s4_b2b / energie.html?vue=calcul : exemple de l'animation ajouté (½ × 220·10⁻⁶ × 12² ≈ 1,6·10⁻² J).
- Valeurs recalculées : τ = 0,22 s, 0,63·E = 7,56 V, 0,37·E = 4,44 V, Q_m = 2,64 mC, I₀ = 12 mA ; 2022 N : R = 1 kΩ, τ = 50 ms, C = 50 µF, E_e = 3,6 mJ.
### Améliorations du texte (architecture)
- Plan des cours marocains : I. Rappels d'électricité ; II. Le condensateur (définition, charge, q = C·u_C, i = C·du_C/dt) ; III. Associations ; IV. Réponse d'un dipôle RC à un échelon (équation, solution, courbes, τ, influence de R et C, courbes sans le temps) ; V. Décharge ; VI. Énergie ; VII. National 2022 N ; VIII. Bilan. Le cahier n'avait aucune numérotation.
- « 1.1 : », « 1.2.1 : » → « Question 1.1 : » pour ne pas ouvrir de fausse partie ; lignes ≤ 90 caractères ; chaque bloc commence par « n. » ou titre romain + « 1. ».
### Sources en ligne consultées
- N. Naceiri Mrabti, 2 BAC BIOF, Dipôle RC (I. Le condensateur, II. Association, III. Réponse à un échelon, énergie) — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/electricité/livre Tom 1-52-58.pdf
- M. El Founani, Le dipôle RC (TelmidTice) — https://telmidtice.com/assets/2bac-sm-b/pc-fr/s1/6/cours/TelmidTice - Dipôle RC - Cours  LaTex .pdf
- moutamadris, cours Dipôle RC 2bac BIOF (vu dans les résultats ; téléchargement refusé) — https://moutamadris.ma/wp-content/uploads/2022/07/cours-Dipole-RC-2bac-BIOF-Sciences-Mathematiques-A%E2%80%AF%E2%80%93B-et-Sciences-Physiques-2.pdf
### Reste douteux
- Couleurs divergentes entre animations : circuit-rc.html dessine i en blanc et u_C en jaune, condensateur.html u_C en jaune, national i(t) en vert, rappels.html u_R en orange dans « additivité » ; le cahier suit le lexique (u_C rouge, u_R vert) et l'exception du ch6 (flèche de i rouge). À aligner dans les animations (le lexique le note « reste à faire »).
- Avertissement préexistant du vérificateur : le schéma du montage (rc_s2_b1) a 20 éléments.


## phys_ch7_dipole_RL — Dipôle RL
**Blocs touchés** : rl_s0_b1 : Les outils ; rl_s0_b2 : La dérivée, la bobine, les deux lampes ; rl_s1_b1 : Les deux lampes ; rl_s1_b3 : u_b = L·di/dt + r·i ; rl_s2_b1 : Échelon, ce qu'on voit ; rl_s2_b2 : L'équation, additivité ; rl_s2_b2b : Ranger l'équation ; rl_s2_b3 : Équation en u_R ; rl_s2_b3b : Deux questions du national ; rl_s3_b1 : Exponentielle, solution, τ ; rl_s3_b1b : A = I₀, condition initiale ; rl_s3_b2 : τ, 63 %, tangente ; rl_s4_b1 : L puis R, trouver r et L ; rl_s4_b2 : Droite di/dt = f(i), u_b(t) ; rl_s3_b3 : Rupture ; rl_s3_b4 : Étincelle et diode ; rl_s4_b2b : Énergie ; rl_np_b1, rl_np_b2, rl_np_b3 : 2023 N ; rl_s4_b3 : Sujets et bilan ; rl_bloc_fin_cours (les 22 blocs pour le texte ; 9 blocs avec dessins revus/ajoutés)
### Écarts trouvés avec les animations
- rl_s2_b1 / circuit-rl.html : le montage du cahier avait un K simple « fermé à t = 0 » ; l'animation a K à deux positions (1 : établissement, 2 : rupture) → K redessiné avec les plots 1 (vert) et 2 (bleu), légende et texte « K en position 1 / 2 ».
- rl_s1_b3 / triangle.html : u_b en créneaux sur une seule période, en cyan, sans la valeur de L → deux périodes (0–40 ms) comme l'animation, sauts en pointillé, violet (u_b du lexique) ; texte : L = 0,4/20 = 20 mH (valeur de la simulation).
- rl_s1_b1 / lampes.html : aucune trace de i₁ / i₂ alors que l'animation donne i₁ = 200 mA tout de suite et i₂ = 0,2·(1 − e^(−t/40 ms)) → nouvelle courbe « Fermeture de K : i₁ et i₂ ».
- Couleurs des grandeurs (lexique grandeurs-electriques) : flèches i en jaune et u_R / u_b en cyan dans 3 schémas → i et u_R en vert, u_b en violet ; u_b(t) cyan → violet (rl_s2_b3).
- Tangentes et repères 63 % / 37 % en jaune → cyan comme courbe.html et rupture.html (rl_s3_b2, rl_s3_b3) ; 2023 N : la tangente (T) est blanche dans pas-a-pas.js et va à (2,3 ms ; 55,2 mA) → (T) blanche, même segment.
- rl_s4_b2 / droite.html : il manquait le triangle de pente (Δi = 2 mA, −1·10³ A/s) → ajouté en pointillé cyan, légende avec −5·10⁵ s⁻¹ = −1/τ.
- rl_s4_b1 / influence.html : « R augmente » sans valeurs → R = 50 → 110 Ω : I₀ = 100 → 50 mA, τ = 2 → 1 ms (valeurs de la simulation) ; fig_r_L : exemple r = 10 Ω, L = 0,12 H.
- rl_s4_b2b / energie.html, energie-carre.html : E_m max = 6·10⁻⁴ J et la conversion en chaleur dans R et r ajoutées ; exemples 0,025 J / 0,1 J (× 4) / 0,05 J (× 2).
- Valeurs vérifiées en Python (I₀ = 100 mA, τ = 2 ms, 63 mA, 37 mA, 2023 N : 48 mA, 30,3 mA, L = 1 H, E_m ≈ 1,15 mJ ; 2022 R, 2024 N, 2019 R, 2025 R) : conformes.
### Améliorations du texte (architecture)
- Plan à parties romaines, comme les cours marocains (bobine → réponse à un échelon → établissement : équation, solution, τ → rupture → énergie) : I. Rappels utiles ; II. La bobine ; III. Réponse à un échelon de tension ; IV. Solution et constante de temps ; V. Rupture ; VI. Énergie ; VII. National 2023 N pas à pas ; VIII. Sujets et bilan.
- Chaque bloc commence par « n. » (ou un titre romain suivi de « 1. »), numérotation continue d'un bloc à l'autre ; parties de 1 à 5 lignes ; lignes ≤ 90 caractères (les longues lignes « Plan : … », « À retenir : … » ont été coupées).
- Définitions écrites comme au national (bobine, auto-induction et continuité de i, régimes transitoire/permanent) ; « Attention » gardés (r·i oublié, I₀ ≠ E/R, second membre R·E/L et 0, carré de l'énergie).
- Champ `partie` posé sur chaque dessin.
### Sources en ligne consultées
- N. Naceiri Mrabti, 2 BAC BIOF, cours n° 7 « Le dipôle RL » — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/electricité/livre Tom 1-65-69.pdf
- TelmidTice, « Dipôle RL — Cours » (2 Bac PC) — https://telmidtice.com/assets/2bac-pc/pc-fr/s1/7/cours/TelmidTice - Dipôle RL - Cours  LaTex .pdf
### Reste douteux
- Couleurs des animations qui s'écartent du lexique (le cahier suit le lexique) : courbe.html?vue=ub trace u_b en vert ; triangle.html : i orange, u_b rose ; circuit-rl.html : flèche i blanche, u_R orange ; pas-a-pas.js : u_R et u_L orange.
- La Méthode 4 vient avant la Méthode 3 (ordre des diapositives, gardé).
- Le montage RL a 23 éléments (avertissement du vérificateur, pas d'erreur).
- Les lampes s'appellent L₁ et L₂ (comme l'animation) alors que L est aussi l'inductance.
- Le vérificateur ne contrôle pas les champs au niveau de la figure : `partie` n'est pas signalé (ni validé).
- Copie `en_attente/` non touchée (hors périmètre).


## phys_ch8_circuit_RLC — Oscillations libres d'un circuit RLC série
**Blocs touchés** : les 24 blocs (lc_s0_b1 … lc_s4_b4, lc_np_b1 … lc_np_b4, lc_bloc_fin_cours) pour le texte ; 13 blocs pour les dessins (couleurs, valeurs, `partie`)
### Écarts trouvés avec les animations
- lc_s1_b1 / circuit-lc.html?vue=bascule : la décharge « R seule » était bleue → rouge en pointillé (u_C reste rouge dans l'animation) ; légende avec R = 1 kΩ et R + r = 20 Ω ; trait de K en jaune (couleur de surlignage) → craie normale.
- lc_s1_b3 / oscillogramme.html : courbe apériodique orange calculée pour R + r = 1000 Ω → rouge en pointillé, recalculée pour R + r = 1010 Ω (R = 1 kΩ, r = 10 Ω) : 6,159·e^(−0,2539t) − 0,159·e^(−9,846t) ; sommets 6 ; 4,0 ; 2,7 V dans la légende.
- Schémas (convention récepteur, maille de décharge, ×3) : i jaune, u_C / u_R / u_b cyan → i vert, u_C rouge (equation.html, circuit-lc.html), u_R vert, u_b violet (lexique).
- lc_s2_b3b / periode.html?vue=influence_C : courbe 4C en jaune → rouge en pointillé (la seconde courbe de l'animation).
- Texte : T₀ ≈ 4 ms pour L = 0,1 H et C = 4 µF, I_m ≈ 38 mA (solution.html), E = 12 V donne U_m = 12 V et le même T₀ (periode.html), 72 µJ (energie.html) ajoutés.
- Vérifiés en Python et conformes : T ≈ 3,98 ms, sommets 6 / 4,02 / 2,70 / 1,81 V, creux −4,91 V, |ΔE| = 40 µJ, 2022 N (3,6 mJ ; 1,39 mJ ; −2,2 mJ ; L = 0,05 H), 2020 N, 2023 N, 2025 N.
### Améliorations du texte (architecture)
- Plan comme les cours en ligne (décharge → régimes → équation → LC : solution, T₀ → énergie → entretien) : I. Rappels ; II. Décharge d'un condensateur dans une bobine ; III. Régimes ; IV. Équation différentielle ; V. Circuit LC idéal : solution et période propre ; VI. Énergie ; VII. Entretien ; VIII. National 2022 N ; IX. Sujets ; X. Bilan.
- Régimes rangés (pseudo-périodique, apériodique, périodique) avec la définition « oscillations libres / amorties » ; « période propre » nommée ; méthodes numérotées (φ, T, L ou C, énergie perdue).
- Chaque bloc commence par « n. » ; numérotation continue ; parties ≤ 5 lignes ; lignes ≤ 90 caractères ; `partie` posé sur chaque dessin.
### Sources en ligne consultées
- Moutamadris, « Oscillations libres d'un circuit RLC série », 2 bac BIOF — https://moutamadris.ma/wp-content/uploads/2022/07/cours-Oscillations-libres-dun-circuit-RLC-serie-2bac-BIOF-Sciences-Mathematiques-A%E2%80%AF%E2%80%93B-et-Sciences-Physiques-5.pdf
- N. Naceiri Mrabti, 2 BAC BIOF, série n° 8 « Les oscillations libres RLC série » — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/electricité/livre Tom 1-81-85.pdf
### Reste douteux
- equation.html et circuit-lc.html dessinent les flèches u_R et u_b en blanc (le lexique dit u_R vert, u_b violet : le cahier suit le lexique).
- Le schéma de la maille de décharge figure dans deux blocs (lc_s1_b2 et lc_s2_b0), comme avant.
- Le montage (lc_s1_b1) a 15 éléments (avertissement, pas d'erreur).
- Copie `en_attente/` non touchée.


## phys_ch9_transformations_lentes_rapides — Transformations lentes et transformations rapides
**Blocs touchés** : les 17 blocs (tl_s0_b1 … tl_s3_b3, tl_np_b1 … tl_np_b4, tl_bloc_fin_cours) pour le texte ; 6 blocs pour les dessins
### Écarts trouvés avec les animations
- tl_s3_b2 / courbes.html?vue=catalyseur : C₁ et C₂ tracées avec τ = 2,5 et 9 min, en rouge / bleu → τ = 2 et 8 min, C₁ vert, C₂ bleu (valeurs et couleurs de la simulation).
- tl_s3_b1 / courbe-reglable.html?vue=temperature : 40 °C rouge, 20 °C bleu → 40 °C orange, 20 °C cyan en pointillé (couleurs de la page jouée par tl_f4).
- tl_s3_b1b / courbe-reglable.html?vue=concentration : courbe 0,2 mol/L rouge et piège « 2 × H₂O₂ » jaune avec τ = 6 min → 0,2 mol/L violet, piège rose avec [I⁻]₀ = 0,2 mol/L (τ = 3 min, palier 4 mmol) ; 0,1 mol/L bleu.
- tl_s1_b1 / transfert.html : flèche « 2e⁻ » jaune (surlignage) → verte (électrons cédés dans l'animation).
- tl_s2_b1 / bechers.html : durées de l'animation ajoutées (acide oxalique ≈ 7 min ; H₂O₂ + I⁻ jaune puis brun, ≈ 40 min).
- Conformes : n(I₂) 2 mmol, paliers vers 10 / 30 min, national (a) τ = 3 min orange, (b) τ = 10 min jaune, x_max = 2 mmol.
### Améliorations du texte (architecture)
- Plan comme le cours de N. Bendaoud (oxydoréduction → rapides/lentes → facteurs cinétiques → applications) : I. Rappels ; II. Réactions d'oxydoréduction ; III. Transformations rapides et lentes ; IV. Facteurs cinétiques (température, concentration, trempe, catalyseur) ; V. Exercice type national ; VI. Sujets et bilan.
- La définition du facteur cinétique vient avant « donc la température est un facteur cinétique » (elle venait après) ; la méthode d'équilibrage est écrite en mots, sans formule n₂Ox₁…
- Chaque bloc commence par « n. » ; numérotation continue (les « 1) 2) » de l'exercice deviennent les parties 1. à 9.) ; parties ≤ 5 lignes ; lignes ≤ 90 caractères ; `partie` sur chaque dessin.
### Sources en ligne consultées
- N. Bendaoud, « Transformations rapides et transformations lentes », 2 bac BIOF (Moutamadris) — https://moutamadris.ma/wp-content/uploads/2022/07/cours-Transformations-lentes-et-transformations-rapides-2bac-BIOF-Sciences-Mathematiques-A%E2%80%AF%E2%80%93B-et-Sciences-Physiques-3.pdf
- Nomad Education, « Transformations lentes et rapides » (Terminale bac sciences Maroc) — https://www.nomadeducation.fr/revisions/terminale-bac-sciences-maroc-lb3a9320/transformations-lentes-et-rapides-cy6aa247
### Reste douteux
- Deux pages du même cours colorent les mêmes courbes différemment : courbes.html (20 °C bleu, 40 °C rouge ; 0,2 mol/L violet, piège orange τ = 4 min) et courbe-reglable.html (cyan / orange ; piège rose τ = 3 min) ; le cahier suit courbe-reglable, la page jouée par les diapositives.
- Le lexique dit l'électron bleu ciel ; transfert.html dessine les flèches d'électrons en vert (gardé, c'est une flèche et non une bille).
- Copie `en_attente/` non touchée.


## phys_ch10_cinetique — Suivi temporel d'une transformation chimique, vitesse de réaction
**Blocs touchés** : ci_r_b1 : Ouverture ; compter en moles, ci_r_b2 : Rappels : concentration, ion, couples, équation, ci_s1_b2 : Le tableau d'avancement…, ci_s1_b1 : La trempe ; le titrage du diiode, ci_s1_b2b : n(I₂) = x, ci_s1_b3 : La courbe x(t), ci_s2_b1 : Conductance, conductivité, ions, ci_s2_b1b : Exemple B : établir σ(x), ci_s2_b1c : De σ(t) à x ; 2016 R, ci_s2_b2 : De la pression P à x, ci_s2_b3 : Choisir sa méthode ; 2024 N, ci_s3_b1 : La pente, la tangente, la vitesse volumique, ci_s3_b1b : Le calcul au barème, ci_s3_b2 : La vitesse diminue ; la température, ci_s3_b3 : Le temps de demi-réaction, ci_s4_b1 : National : vitesse, t₁/₂, ci_s4_b2 : National : même x_f, G(t), trempe, ci_s6_b1 : 2021 N pas à pas, ci_s4_b3 : Pièges d'unités, fiche et carte, ci_bloc_fin_cours (20 blocs, champs cahier / cahier_figures seulement)
### Écarts trouvés avec les animations
- Toutes les courbes x(t) (ci_s1_b3, ci_s3_b1, ci_s3_b2, ci_s3_b3) : modèle 2·(1 − e^(−0,124·t)) et t₁/₂ gradué 5,59 min → modèle de courbe.html / vitesse.html / demi-reaction.html 2·(1 − e^(−t/8)), t₁/₂ = 8·ln 2 = 5,545 min (graduation à 5,545, écrite « 5,5 »).
- Couleurs des courbes x(t) et σ(t), σ(x) : cyan par défaut → bleu (couleur de trace de toutes les pages cinetique-tableau) ; lectures (x(8 min), t₁/₂, σ(10 min)) orange → jaune (pointillés et point jaunes de la simulation).
- ci_s3_b1 (diapo ci_v3_tangente) : tangente et points A, B jaunes → verts (tangente verte, A et B verts dans vitesse.html).
- ci_s3_b2 (ci_v5_diminue) : tangentes jaune / orange / rose → vertes, points de contact jaunes, comme vitesse.html?vue=diminue ; pentes recalculées (0,25 ; 0,092 ; 0,021 mmol/min).
- ci_s3_b2 : la figure « Plus concentré, plus vite » (courbes C₁/C₂) n'existe dans aucune animation du bloc → remplacée par la figure de temperature.html?vue=vitesse (20 °C cyan, 40 °C orange, tangentes à l'origine 0,25 et 0,75 mmol/min, même palier 2,0 mmol), qui porte les valeurs du texte (v(0) = 2,5 et 7,5).
- ci_s1_b3 (ci_a4_courbe) : la courbe x(t) ne montrait pas les points mesurés → ajout de 4 points des mesures (2 ; 0,44), (4 ; 0,79), (15 ; 1,69), (30 ; 1,95) (vérifiés : la courbe y passe à 0,01 près).
- ci_s4_b1 (fig_2023N) : courbe C₁ en e^(−0,55·t), orange → 0,3 + 0,6·2^(−t/1,7) = e^(−0,4077·t), bleue ; C₂ cyan → violette (couleurs et modèle de figures.html).
- ci_s2_b2 (ci_p1_ballon) : la valeur de P n'était pas écrite → ajout « P₀ = 101,3 kPa → P_max = 103,8 kPa » montrée par l'animation.
- ci_s4_b2 (ci_n8_trempe) : le palier de fig_2017R (n(acide) = 0,2 mol → x_f = 0,4 mol) manquait → ajouté.
- ci_s4_b1 (ci_n1_aspirine) : t₁/₂ = 70 s de 2019 R manquait → ajouté.
### Améliorations du texte (architecture)
- Plan continu en huit parties romaines (I. Suivi temporel et rappels, II. Tableau d'avancement, III. Méthode chimique : titrage, IV. Méthodes physiques, V. Vitesse volumique, VI. Temps de demi-réaction, VII. Exercices du national, VIII. Bilan), sous-parties numérotées en continu d'un bloc à l'autre ; chaque bloc commence par « n. » ou par un titre romain suivi de « 1. ».
- Définitions alignées sur les cours marocains : vitesse volumique v = (1/V)·dx/dt « V : volume du mélange réactionnel » ; t₁/₂ « durée au bout de laquelle x atteint la moitié de sa valeur finale », avec la remarque « totale : x(t₁/₂) = x_max/2 » ; méthodes physiques « en continu », chimique « ponctuelle ».
- Les rappels portent un numéro (I.1 à I.4) pour que chaque partie s'affiche ; lignes > 90 caractères recoupées ; chaque dessin porte « partie ».
### Sources en ligne consultées
- Suivi temporel d'une transformation chimique — Vitesse de réaction, Pr. H. Mahajar et Y. Tabit (moutamadris) — https://moutamadris.ma/wp-content/uploads/2020/03/cours-pc-2bac-sp-international-fr-13-1.pdf
- Cours 2 BAC PC, N. Naceiri Mrabti (partie 1 : I. Transformations rapides et lentes, II. Suivi temporel, III. Facteurs influençant la vitesse) — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/2PC-Prof-partie%201.pdf
- (vu dans les résultats seulement) Google Doc de cours/exercices sur le suivi temporel — https://docs.google.com/document/d/1C6qPXqCCPKTOuuSvscQVqREvX9Jr34Ls/export?format=pdf
### Reste douteux
- Le champ de figure `partie` n'est pas signalé par backend/scripts/verifier_figures_cahier.py (le script ne contrôle pas les clés de premier niveau d'une figure) : 0 erreur ; à vérifier côté lecteur.
- La copie `en_attente/phys_ch10_cinetique.json` n'a pas été touchée (hors périmètre) : elle garde l'ancien cahier (modèle 0,124, couleurs anciennes).
- vitesse.html?vue=vitesse (non utilisée par le bloc) trace 20 °C en bleu et 40 °C en rouge, alors que temperature.html (utilisée) les trace en cyan et orange : deux codes de couleur pour la même comparaison dans le même dossier.


## phys_ch11_transformations_deux_sens — Transformations chimiques s'effectuant dans les deux sens
**Blocs touchés** : td_r_b1 : Ouverture ; l'ion et le proton, td_r_b2 : Rappels ; l'acide, td_s1_b1 : La base, le couple, l'eau, td_s1_b2 : Réaction acido-basique, pH, td_s1_b3 : pH-mètre et réaction d'un acide avec l'eau, td_s2_b1 : x_max, x_f et τ, td_s2_b2 : Totale ou limitée ; deux sens, td_s2_b3 : L'état d'équilibre, td_s3_b1 : La conductimétrie donne τ, td_d_b1 : Diluer, td_s3_b2 : Dilution, nature de l'acide ; 2019 N, td_n_b1 : National 2021 R, td_s3_b3 : Montrer, conclure, td_bloc_fin_cours (14 blocs)
### Écarts trouvés avec les animations
- td_s2_b3 (td_e4_dynamique, td_e5_esterification) : la courbe « v₁ et v₂ en fonction de t » (valeurs et unité inventées) n'est dans aucune animation (equilibre.html montre deux compteurs égaux) → remplacée par la courbe de l'estérification de l'animation : x = 0,33·(1 − e^(−t/1,6)), t en h, x_max = 0,5 mol (violet), palier x_f = 0,33 mol (jaune), τ = 0,66.
- td_s2_b3 (fig_2017N) : t de 0 à 42 min, couleurs orange/cyan → t de 0 à 75 min comme figures.html ; courbe (1) bleue, (2) violette, repères x_f₁ = 0,2 mol (bleu) et x_max = x_f₂ = 0,3 mol (violet) ; modèles vérifiés sur les points lissés de la figure (0,1 à 8 min ; 0,194 à 40 min ; 0,15 à 2 min ; 0,247 à 5 min).
- td_s1_b2 (td_b4_reaction) : réactifs jaune/cyan → réactifs blancs, produits verts, arc du H⁺ rose en pointillé, comme acides.html?vue=reaction ; « couple 1 / couple 2 » ajoutés.
- td_n_b1 (td_n1c_courbe) : lectures orange → jaunes, points de lecture ajoutés ; courbe τ = 1/(1 + 10^(1,084·(3,68 − pH))) identique à national.html (τ(2,8) = 0,100 ; τ(3,6) = 0,450).
- td_s3_b2 (diluer.html) : barres 0,040 ; 0,126 ; 0,316 et flèche jaune conformes ; aucune correction.
### Améliorations du texte (architecture)
- Plan en dix parties comme les cours marocains (Ibn Maja, N. Naceiri) : I. Introduction et rappels, II. Acides et bases selon Brønsted, III. Le pH, IV. Réaction d'un acide ou d'une base avec l'eau, V. Taux d'avancement final, VI. Deux sens ; état d'équilibre, VII. Conductimétrie, VIII. Dilution et nature de l'acide, IX. Exercices du national, X. Bilan ; titres romains sur leur propre ligne avant le « 1. ».
- Définitions mises au format du national (« ampholyte : acide d'un couple et base d'un autre couple »).
- Rappels numérotés (I.3, I.4) pour que la première partie de chaque bloc s'ouvre par « n. ».
### Sources en ligne consultées
- Les transformations chimiques s'effectuant dans les deux sens, M. El Founani, lycée Ibn Maja (dyrassa) — https://dyrassa.com/wp-content/uploads/2022/08/transformations-chimiques-s-effectuant-dans-les-2-sens-cours-latex.pdf
- Cours 2 BAC PC, N. Naceiri Mrabti (I. Réactions acidobasiques, II. Le pH, III. Transformations totales et non totales) — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/2PC-Prof-partie%201.pdf
- (vu dans les résultats seulement ; le lien renvoie une page HTML) cours moutamadris 2 bac BIOF — https://moutamadris.ma/wp-content/uploads/2022/07/cours-Transformations-chimiques-seffectuant-dans-les-2-sens-2bac-BIOF-Sciences-Mathematiques-A%E2%80%AF%E2%80%93B-et-Sciences-Physiques-1.pdf
### Reste douteux
- Champ `partie` non contrôlé par verifier_figures_cahier.py (0 erreur).
- td_s1_b3 contient deux parties « 3. » (III.3 mesure du pH puis IV.3 « si elle était totale ») : numérotation juste par partie romaine, mais le lecteur verra deux « 3. » dans le même bloc.
- Copie en_attente non modifiée.


## phys_ch12_etat_equilibre — État d'équilibre d'un système chimique
**Blocs touchés** : ee_b01 : Les outils, ee_b02 : τ, deux concentrations, équilibre dynamique, ee_b03 : Écrire Qr, ee_b04 : Qr sans unité ; Qr,i, ee_b05 : Qr évolue ; Qr,i au national, ee_b06 : Qr,éq à partir du pH, ee_b07 : La constante d'équilibre K, ee_b08 : K = C·τ²/(1 − τ), ee_b09 : Mesurer K par la conductimétrie, ee_b09b : 2019 N (équation, tableau, σ), ee_b09c : 2019 N (τ puis K), ee_b10 : Diluer ; un autre acide, ee_b11 : τ dépend de K et de C, ee_b12 : K lue sur une courbe ; bilan, ee_bloc_fin_cours (15 blocs)
### Écarts trouvés avec les animations
- ee_b12 (ee_n5_courbe, fig_2017R) : courbe « allure » sur 0 à 10 h → l'axe de la figure du national va de 0 à 200 h (palier vers 150 h) ; nouvelle courbe 0,2 + 0,4·e^(−t/23) qui passe par les points de figures.html (0,46 à 10 h ; 0,37 à 20 h ; 0,27 à 40 h ; 0,23 à 60 h ; 0,21 à 80 h), bleue, palier jaune.
- ee_b05 (ee_i3_au_cours) : courbe Qr cyan, équilibre orange → courbe violette (Q_r violet dans quotient.html), points blancs, point d'équilibre jaune et trait jaune « Qr,éq : Qr ne bouge plus » (étape palier) ; point Q_{r,i} = 0 ajouté.
- ee_b11 (ee_f3_courbe) : éthanoïque cyan / méthanoïque orange → bleu / jaune comme facteurs.html ; ajout des points à C = 1,0·10⁻¹ mol/L (τ = 0,013 et 0,042) que l'animation lit.
- ee_b09 (conductimètre) : afficheur jaune → vert, boîtier sombre (lexique conductimetre.md).
- ee_b02 : la valeur Qr,éq et les concentrations à l'équilibre sont déjà justes (3,89·10⁻⁴ ; 9,61·10⁻³ ; 1,57·10⁻⁵) ; aucune autre valeur en écart.
### Améliorations du texte (architecture)
- Plan en six parties : I. Rappels, II. Le quotient de réaction Qr (définition, expression générale, eau et solides, sans unité, Qr,i, Qr qui évolue), III. Qr à l'équilibre, IV. La constante d'équilibre K (définition, K' = 1/K, K = C·τ²/(1 − τ), conductimétrie, 2019 N), V. De quoi dépend τ, VI. Exercice du national et bilan — même ordre que le cours de N. Naceiri (I. Le quotient de réaction, II. Facteurs influençant τ).
- Numérotation continue (II.1 → II.7, IV.1 → IV.9) au lieu de « 1. » répété à chaque bloc ; les questions du national s'écrivent « Q2.1 », « Q2.3.2 » pour ne pas ouvrir de fausse partie.
- Définition de K formulée comme au national : « K = Qr,éq ; sans unité, ne dépend que de T ».
### Sources en ligne consultées
- Cours 2 BAC PC, N. Naceiri Mrabti (I. Le quotient de réaction ; II. Facteurs influençant τ) — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/2PC-Prof-partie%201.pdf
- Cours N°C6 : Évolution spontanée d'un système chimique, N. Naceiri Mrabti (rappel du quotient de réaction, K) — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/Sens%20%C3%A9volution/Livre%20Tom%202-112-114.pdf
- (vu dans les résultats seulement) Fiche « État d'équilibre d'un système chimique » — https://docs.google.com/document/d/1eMEmJCs0SjoOd79K9bg6oZlCgv88GLBY/export?format=pdf
### Reste douteux
- ee_b07 : le schéma « Qr arrive toujours à K » (axe de Qr) n'est pas dessiné par constante.html (qui montre un tableau de trois solutions) ; gardé comme synthèse, rattaché à la partie 1.
- Champ `partie` non contrôlé par verifier_figures_cahier.py (0 erreur). Copie en_attente non modifiée.


## phys_ch13_acides_bases — Transformations associées aux réactions acido-basiques
**Blocs touchés** : ab_b01 à ab_b21 et ab_bloc_fin_cours (22 blocs : outils, autoprotolyse, Ke, solutions acide/neutre/basique, base dans l'eau, τ d'une base, Ka/pKa, comparer acides et bases, K d'une réaction acide-base, prédominance, indicateurs, dosage, tangentes et dérivée, exploitation, base dosée et conductimétrie, nationaux, 2018 N, bilan)
### Écarts trouvés avec les animations
- ab_b13/ab_b14/ab_b15 (dosage.html, exploiter.html, exemple J) : points de la courbe pH = f(V_B) faux à 2 mL (3,85 → 3,91) et 18 mL (5,75 → 5,76) ; points recalculés avec le modèle de dosage.html (phJ) et ajout de 19,9 / 20,1 / 22 mL ; courbe cyan → bleue (couleur des courbes de dosage).
- ab_b14 (ab_d5_tangentes) : tangentes de pente 0,5 qui ne touchaient pas la courbe → tangentes de pente 0,2 aux points de contact de la simulation (17,5 mL ; 5,65) et (22,1 mL ; 10,69), en pointillé jaune ; parallèle équidistante jaune pH = 4,21 + 0,2·V_B ; E jaune.
- ab_b14 (ab_d6_derivee) : pic de dpH/dV_B à 7,3 mL⁻¹ → 11,5 mL⁻¹ (valeur de la simulation) ; courbe cyan → orange (couleur de la dérivée dans dosage.html).
- ab_b11 (predominance.html) et ab_b09 (comparer.html?vue=classement) : forme basique / bases en bleu → vert (acide rose, base verte dans les animations).
- ab_b04 (eau.html?vue=solutions) : « solution basique » bleu → vert, neutre vert → blanc (COUL_MOT de la page).
- ab_b16 (ab_e5_conductimetrie) : une seule ligne brisée sans points → deux droites bleues prolongées comme dans exploiter.html (D1, D2), points mesurés (0 ; 38,8), (1 ; 25,0), (3 ; 22,5), (4 ; 33,5), rupture E (2,0 mL ; 11,4 mS/m).
- ab_b13 (montage) : pH-mètre orange → boîtier gris, « pH-mètre » vert (lexique ph-metre.md).
- ab_b13 : V_BE = 20,0 mL (calcul C_A·V_A/C_B montré par ab_d3_equivalence) ajouté au texte.
### Améliorations du texte (architecture)
- Plan en douze parties qui suit le cahier idéal et l'ordre des cours marocains (N. Naceiri : I. Produit ionique, II. Ka, III. Force des acides et des bases, IV. Domaines de prédominance, V. Titrage) : I. Rappels, II. Autoprotolyse et Ke, III. Base dans l'eau, IV. Ka et pKa, V. Force des acides et des bases, VI. K d'une réaction acide-base, VII. Prédominance, VIII. Indicateurs, IX. Dosage, X. Exploiter la courbe, XI. Exercices du national, XII. Bilan.
- Titres romains insérés sur leur propre ligne ; numérotation continue dans chaque partie romaine ; lignes > 90 caractères recoupées.
### Sources en ligne consultées
- Cours 2 BAC PC, N. Naceiri Mrabti (I. Produit ionique de l'eau, II. Constante d'acidité, III. Force d'un acide et d'une base, IV. Domaines de prédominance, V. Titrage) — https://nidal-naceiri-mrabti.github.io/MesCoursPhysiqueChimie/2bac/2PC-Prof-partie%201.pdf
- Transformations et réactions acido-basiques, Terminale bac sciences Maroc (nomadeducation) — https://www.nomadeducation.fr/revisions/terminale-bac-sciences-maroc-lb3a9320/transformations-et-reactions-acido-basiques-cy6aa548
### Reste douteux
- Couleur de HO⁻ / de la forme basique : le lexique (ho.md) donne « HO⁻ à la craie bleue », mais eau.html, predominance.html et comparer.html écrivent [HO⁻], la base et « basique » en vert ; le cahier suit les animations (vert). L'autoprotolyse garde « HO⁻ » en bleu (lexique). À trancher dans le lexique.
- exploiter.html marque E en bleu (couleur de la courbe), dosage.html en jaune : la figure de demi-équivalence garde E bleu, celle des tangentes E jaune.
- Champ `partie` non contrôlé par verifier_figures_cahier.py (0 erreur). Copie en_attente non modifiée.

