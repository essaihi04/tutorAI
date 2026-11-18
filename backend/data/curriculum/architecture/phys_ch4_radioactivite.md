# Architecture — `phys_ch4_radioactivite` (Décroissance radioactive)

Refaite le 18 novembre 2026 avec la skill `logique-de-cours`. Version en attente :
`backend/data/courses/en_attente/phys_ch4_radioactivite.json`, construite par
`scripts/voix/logique_ch4_radioactivite.py` à partir du cours en ligne (qui ne change pas). Pistes à mettre en voix :
`phys_ch4_radioactivite_voix.json` (107 pistes après la 2ᵉ passe, section 9).

## 1. La logique d'avant, et ce qui n'allait pas

Ordre d'avant (61 diapositives, 6 séances) : noyau → diagramme (N, Z) avec **toutes ses zones et ses
flèches β⁻, β⁺, α** → radioactivité → Soddy → α, β⁻, β⁺, γ → famille → proportion → équation → loi → λ, τ →
**demi-vie** → activité → puissances de dix → mole → datation → nationaux.

Défauts relevés diapositive par diapositive :

| Diapositive | Défaut | Règle |
|---|---|---|
| `ra_s3_zones`, `ra_s4_fleches`, `ra_s4b_alpha` (séance 1) | disent « β⁻ », « β⁺ », « α », « un neutron devient proton » avant que la radioactivité soit définie (`ra_r1`) et avant les désintégrations (`ra_d1`-`ra_d3`) | professeur 27 (rien d'enseigné plus loin), logique 4 |
| `ra_s5_isotopes_ligne` | finit sur « le carbone 14 fait β⁻ » : même défaut | professeur 27 |
| `ra_t1_definition` (après la loi) | la demi-vie, que l'élève peut **compter** dans la grille de 400 noyaux, n'arrive qu'après la formule ; la grille affichait déjà « N₀/2 », « t½ » et la loi | logique 3 et 4, demande du 18/11 |
| `ra_p3_puissances` | rappel des puissances de dix placé après `ra_l7b_037` (N₀ = 8,0·10²⁰) et la courbe de la demi-vie (axe en 10²⁰) | logique 6 (prérequis juste avant son usage) |
| `ra_d6_type` | l'exemple du national 2018 R s'arrêtait sur « … plus X. » sans le trouver | professeur 37 (aller au bout) |
| `ra_c3_calcul` (datation 2022 R) | la voix faisait tout le calcul, l'élève n'avait rien à faire | logique 3 et 5 |
| `ra_x2_2021N` | exercice du national sans tableau : lu, jamais joué | logique 5, professeur 41 |
| `ra_a5_masse` / `ra_a5b_masse_inverse` | deux tableaux « À toi » de suite | professeur 27 (un tableau par bloc) |
| 9 réactions préparées | « 1/6 », « 100 Bq », « ²⁸₁₃Al », « j⁻¹ », « ⁰₁e » écrits en symboles : la voix ne les lit pas | voix-du-cours § 1 |

## 2. Les sources comparées

- **Les dix profs de l'exploration** (`exploration/radioactivite.json`, convergences) : noyau ᴬ_Z X (10/10) → isotopes
  (9/10) → Soddy (10/10) → α, β⁻, β⁺, γ (10/10) → caractères aléatoire, spontané (8/10) → loi N₀·e^(−λt) (7/7) →
  t½ = ln2/λ démontrée (7/7) → τ et tangente (7/7) → rappel de maths juste avant la démonstration (6/7) → activité
  (6/6) → datation (5/5) ; diagramme Z en abscisse (5/6).
- **Quatre cours écrits en ligne** (lus le 18/11) : Ismaili-alaoui (kezakoo.com, PDF 2e Bac PC BIOF) ; El Goufifa
  (AlloSchool, séance 6) ; El Founani (AlloSchool, lycée Ibn Maja, LaTeX) ; Moutamadris (cours BIOF). Ordre commun :
  noyau/isotopes → radioactivité → diagramme de Segrè → Soddy → α, β⁻, β⁺, γ → famille → caractère aléatoire → loi
  → τ → t½ (démontrée depuis la loi) → courbe → activité → datation. Deux d'entre eux (El Founani, Moutamadris)
  montrent **chaque type avec son déplacement sur le diagramme** ; aucun n'introduit la loi par un comptage (loi
  énoncée, ou démontrée par ΔN = −λ·N·Δt).
- **Le cadre** (`cadre_reference_2bac_pc.json`, `radioactivite`, RA1-RA10) et `perimetre.json`
  (`radioactivite`, `cinetique_nucleaire`) : rien n'a été ajouté hors cadre ; la diapositive nouvelle sert RA7.
- **Le national 2016-2025** (`cas_types`) : équation et noyau fils 13/13 ; λ ↔ t½ 9 fois ; activité/date 8 fois ;
  nombre de noyaux 6 fois ; pourcentages 4 fois ; datation 2 fois ; lecture de diagramme 3 fois. Le temps va là.

## 3. Les décisions et leurs raisons

1. **Le diagramme en deux temps.** Le plan, la vallée, stable / instable et les isotopes sur une verticale restent en
   séance 1 (ordre commun des profs et des cours écrits). Les **flèches et les zones** (`ra_s4_fleches`,
   `ra_s4b_alpha`, `ra_s3_zones`) passent **après** α, β⁻, β⁺, γ et avant la famille : on ne nomme plus une
   désintégration avant de l'avoir enseignée (professeur 27), l'élève voit chaque désintégration bouger le point qu'il
   connaît déjà (comme chez El Founani et Moutamadris), et la famille, qui est une suite de flèches sur ce même
   diagramme, suit aussitôt. `ra_s3_zones` devient la synthèse « trop de quoi ? → quel type » au lieu d'une affirmation
   avant la preuve (logique 4).
2. **La demi-vie comptée avant la loi** (demande du 18/11, logique 3-4). L'élève compte : 400 → 200 → 100 → 50
   noyaux, arrêt à 8, 16, 24 jours (`ra_l1b_moitie`, nouvelle), et trouve **seul** « divisé par deux tous les 8 jours »
   (question au tableau, réponse avant le mot). Le mot « demi-vie », sa définition et sa lecture sur la courbe viennent
   juste après (`ra_t1_definition`, déplacée, sa voix reste). Puis la proportion constante (`ra_l2_proportion`,
   observation déjà là), l'équation, la loi. La démonstration t½ = ln2/λ (`ra_t2_demo`) relie ensuite la formule à ce
   que l'élève a compté. Les cours écrits posent la loi d'abord : on s'en écarte ici pour nos règles 3 et 4, et on
   retrouve leur ordre dès l'équation.
3. **La simulation ne donne plus la réponse.** `population.html` accepte `conclusions=0` dans l'URL : la vue
   `grand_nombre` écrit seulement « N = 200 » et « 8 j » (pas « N₀/2 », pas « t½ », pas la loi en pointillé).
   `ra_l1_echantillon` et `ra_l1b_moitie` l'utilisent (URL distinctes, `demarrer: reset` pour la nouvelle).
   `ra_s3_zones`, qui suit maintenant `ra_s4b_alpha` sur la même page `segre.html?vue=zones` (déjà arrivée à
   « fleches »), reçoit une URL distincte (`&synthese=1`) et `demarrer: reset` : la scène se recharge et ses
   play_until repartent de la vallée (professeur 39).
4. **Chaque prérequis juste avant son usage** (logique 6) : `ra_p3_puissances` ouvre la partie « beaucoup de noyaux »
   (premier grand nombre : la courbe en 10²⁰) ; `ra_l4a_exp` et `ra_l4_rappel` restent juste avant la loi (6/7
   profs) ; `ra_p4_mole` reste juste avant N = (m/M)·N_A.
5. **Restants / désintégrés avant τ** (`ra_l8_restants` avance de deux places) : elle n'utilise que la loi, et cela
   espace les tableaux « À toi » (l4 → l8 → t3, deux diapositives au moins entre deux).
6. **La famille** : `ra_f1_famille` (l'uranium 238 jusqu'au plomb, 8 α et 6 β⁻ annoncés) → `ra_f3_famille2024`
   (lire chaque flèche d'une famille du national) → `ra_f2_systeme` (calculer y puis x, d'où viennent 8 et 6). On lit
   avant de calculer ; l'ordre espace aussi les tableaux.
7. **Les exercices du national joués étape par étape** (logique 5, professeur 37 et 41). Une séance à part (séance 7)
   où chaque diapositive est un exercice : la voix pose les données et la méthode, sans le résultat ; le tableau
   « À toi » donne une étape à la fois (question puis exercices du carrousel), l'élève répond, la réaction préparée
   le corrige, la démonstration écrit l'étape comme le barème la lit. Datation 2022 R (`ra_c3_calcul`, déplacée ici,
   texte réécrit) : 1. la relation, 2. λ en an⁻¹, 3. t. National 2021 N (`ra_x2_2021N`) : 1. λ en s⁻¹ (piège de
   l'unité), 2. N₀ = a₀/λ, 3. l'âge pour 30 % désintégrés (étape tirée de la réserve). Dans cette séance les tableaux
   se suivent : c'est voulu, chaque diapositive y est un exercice d'examen (la règle « un tableau par bloc » vise les
   questions de cours).
8. **Aller au bout** : `ra_d6_type` trouve X par Soddy (A = 0, Z = −1, électron, β⁻), avec les trois lignes au centre.
9. **Un tableau par bloc** : la question de `ra_a5b_masse_inverse` passe en réserve de fin de cours (sa voix ne
   finissait pas sur une question) ; elle collait à celle de `ra_a5_masse`.

## 4. Séances, blocs et diapositives — pourquoi ici

Légende : ✏️ tableau « À toi » ; 👀 question d'observation ; 🆕 nouvelle ; ✍️ texte réécrit (voix à refaire) ;
↕ déplacée (texte et voix gardés).

### Séance 1 — Le noyau, sa notation et le diagramme (N, Z)
- **B1 L'atome, le noyau et sa notation**
  - `ra_n1_ouverture` — la question du bois ancien : le but du chapitre avant les outils (convergence des profs : ouverture par une application).
  - `ra_n2_atome` — départ de zéro : l'atome, le noyau, protons et neutrons (logique 6, rien supposé de la 1re année).
  - `ra_n3_compter` — compter sur le carbone 14 avant de nommer Z, N, A (la chose vue, puis le mot).
  - `ra_n4_notation` ✏️ — ᴬ_Z X (10/10 profs) ; la question vérifie A et Z sur l'uranium 238.
- **B2 Composition, isotopes, diagramme**
  - `ra_n5_composition` — la rédaction d'examen en deux lignes (2011 N, 2012 N, 2024 N).
  - `ra_n6_isotopes` — isotopes juste après la composition (9/10 profs, 4/4 cours écrits) : ils servent dès la diapositive du diagramme et pour le carbone 14.
  - `ra_s1_diagramme` ✏️ — un noyau = un point, Z en abscisse (5/6 profs, manuels).
- **B3 La vallée, les isotopes sur le diagramme**
  - `ra_s2_vallee` — stable / instable par la position (RA2) ; piège « N = Z suffit ».
  - `ra_s5_isotopes_ligne` ✍️ — les isotopes sur une verticale (QCM 2025 N) ; le carbone 14 au-dessus, **instable** : la question « que fait-il ? » ouvre la séance 2 (plus de « β⁻ » avant son heure).

### Séance 2 — La radioactivité et les désintégrations
- **B1** `ra_r1_definition` ✏️ (le carbone 14 instable se transforme : définition) → `ra_r2_caracteres` (aléatoire, 12 noyaux) → `ra_r2b_spontanee` (inéluctable, on chauffe) : les trois caractères du cadre (RA3), chacun vu.
- **B2** `ra_r3_soddy` (conservation de A et Z avant tout type, 10/10) → `ra_d1_alpha` → `ra_d2_beta_moins` ✏️ (d'où sort l'électron : question d'élèves fréquente).
- **B3** `ra_d3_beta_plus` → `ra_d4_gamma` → `ra_d5_inconnu` (méthode d'examen A, Z, tableau : 13/13 nationaux) → `ra_d6_type` ✍️ (trouver la particule puis le type, 2018 R, jusqu'au bout).

### Séance 3 — Le diagramme, la famille, puis compter les noyaux
- **B1 Chaque désintégration sur le diagramme**
  - `ra_s4_fleches` ✏️ ↕ — β⁻ et β⁺ maintenant connus : le point bouge (Z ± 1, N ∓ 1).
  - `ra_s4b_alpha` ↕ — « la troisième flèche » : α, deux pas à gauche, deux en bas.
  - `ra_s3_zones` ↕ — synthèse : au-dessus β⁻, au-dessous β⁺, lourds α (RA2 « prévoir le type ») ; c'est maintenant une conclusion de ce qui a été vu.
- **B2 La famille radioactive**
  - `ra_f1_famille` — uranium 238 → plomb 206, flèche après flèche sur le diagramme qu'il vient d'utiliser.
  - `ra_f3_famille2024` ✏️ ↕ — lire chaque flèche d'une famille du national 2024 R.
  - `ra_f2_systeme` ↕ — calculer y (A) puis x (Z), national 2012 N : d'où viennent les 8 α et 6 β⁻ de f1.
- **B3 Beaucoup de noyaux : on compte**
  - `ra_p3_puissances` ✍️ ↕ — rappel des puissances de dix juste avant le premier grand nombre (logique 6).
  - `ra_l1_echantillon` — 400 noyaux, la courbe se trace (simulation sans « N₀/2 » ni « t½ » écrits).
  - `ra_l1b_moitie` 🆕 ✏️ — l'élève compte 400, 200, 100, 50 à 8, 16, 24 jours et trouve seul « divisé par deux » (demande du 18/11).
  - `ra_t1_definition` ↕ — le mot « demi-vie », sa définition relue, sa lecture sur une courbe (deuxième façon, logique 6).

### Séance 4 — La loi de décroissance
- **B1** `ra_l2_proportion` 👀 (chaque jour la même proportion : l'élève le remarque) → `ra_l3_equation` (dN = −λ·N·dt établie, professeur 37) → `ra_l4a_exp` (rappel e^(−x), juste avant la solution).
- **B2** `ra_l4_rappel` ✏️ (ln enlève e) → `ra_l5_loi` (solution vérifiée dans l'équation, condition initiale) → `ra_l6_lambda` (unité, sens de λ).
- **B3** `ra_l8_restants` ✏️ ↕ (restants / désintégrés : 3 nationaux, n'a besoin que de la loi) → `ra_l7_tau` (tangente à l'origine, établie) → `ra_l7b_037` (N(τ) calculé, pas affirmé).

### Séance 5 — La demi-vie par la loi, l'activité
- **B1** `ra_t2_demo` (t½ = ln2/λ, 2023 N : la formule rejoint ce qui a été compté) → `ra_t3_paliers` ✏️ (N₀/2ⁿ calculé) → `ra_t4_pourcentages` (piège « x % désintégrés », 4 nationaux).
- **B2** `ra_a1_compteur` (on ne voit pas les noyaux : on compte les particules) → `ra_a2_definition` ✏️ → `ra_a3_demo` (a = −dN/dt = λ·N) → `ra_a3b_loi_activite`.
- **B3** `ra_a4_unites` (λ en s⁻¹ pour des Bq : piège fréquent) → `ra_p4_mole` (rappel juste avant son usage) → `ra_a5_masse` ✏️ (N = (m/M)·N_A, 2023 N).

### Séance 6 — Masse, courbes du national, datation
- **B1** `ra_a5b_masse_inverse` (sens inverse ; sa question va en réserve) → `ra_a6_courbe_a` (2022 N) → `ra_a7_droite_ln` (2021 R).
- **B2** `ra_c1_principe` 👀 (l'arbre coupé : la jauge baisse, l'élève le voit) → `ra_c2_demo` (t = (1/λ)·ln(a₀/a), établie ligne à ligne).
- **B3** `ra_c4_fils_pere` → `ra_c4b_rapport` ✏️ (roche : r = e^(λt) − 1, 2020 R).

### Séance 7 — Exercices du national joués, bilan et carte (remplacée par la 2ᵉ passe : séances 7 et 8, section 9)
- **B1** `ra_x1_cas_types` (le mot de la question donne la méthode) → `ra_c3_calcul` ✍️ ↕ ✏️ (datation 2022 R en 3 étapes, datation.html arrêtée sur la mesure) → `ra_x2_2021N` ✏️ (stimulateur cardiaque en 3 étapes).
- **B2** `ra_x3_2022N` ✏️ (95 %) → `ra_x4_2025N` ✏️ (β⁺, entre 2t½ et 3t½, vrai/faux).
- **B3** `ra_z1_bilan` → `ra_z2_carte`.

## 5. Ce qui reste comme avant, et pourquoi
- Les textes et voix de 57 diapositives sur 62 : leur contenu était juste, seul l'ordre posait problème.
- Les deux observations (`ra_l2_proportion`, `ra_c1_principe`) : c'est déjà la règle 30 (deux par cours au plus) ; la
  nouvelle étape de comptage passe donc par un tableau « À toi » et non par une troisième observation.
- Le bilan et la carte : ils suivent les blocs, pas l'ordre des diapositives.

## 6. Pistes à mettre en voix (voir `phys_ch4_radioactivite_voix.json`)
5 diapositives (1 nouvelle, 4 réécrites), 7 démonstrations, 51 réactions et énoncés (dont 9 réactions déjà écrites
remises en mots). Mots rares gardés exprès (`verifier_mots.py`) : « vallée », « positon », « plutonium »,
« américium », « becquerels » (termes du programme et des énoncés : à écouter) ; les nombres composés
(« quatre-vingt-treize »…) sont des nombres.

## 7. Ce qui n'a pas pu être fait ici
- Rejouer les simulations dans un navigateur (`verifier-pointage-navigateur.mjs`) : à faire avec la voix posée.
- Les voix (quota Kaggle épuisé jusqu'à samedi) : sur le VPS, avec la liste.
- `test_pointage_simulations.py::test_le_cours_de_svt_liberation_de_l_energie_est_sans_ecart` échoue déjà sur `main`
  sans ces changements (cours SVT d'une autre session).

## 8. Scènes figées pour de vrai (18 novembre 2026)
Dans `population.html`, `datation.html` et `segre.html`, `reset` n'était qu'un autre nom de `start` : `ra_l1b_moitie`,
`ra_c3_calcul` et `ra_s3_zones` (en `demarrer: reset`) auraient couru seules devant la voix. `reset` fige maintenant
la scène (à zéro ou sur `?depart=<moment>`), seule la voix la fait avancer ; `start` ne change pas (cours en ligne
inchangés). Vérifié dans Chromium : figées, puis arrêtées sur `un_t_demi`, `mesure`, `vallee`, sans erreur JS.

## 9. 2ᵉ passe (18 novembre 2026) : les exercices du national joués pas à pas

**Ce qui n'allait pas après la 1ʳᵉ passe.** Les quatre exercices du national (`ra_c3_calcul`, `ra_x2_2021N`,
`ra_x3_2022N`, `ra_x4_2025N`) étaient une seule diapositive chacun, sur une figure fixe (`figures.html?fig=fig_enonce_*`,
`datation.html` qui écrit tout le calcul), avec deux ou trois étapes dans le carrousel « À toi » : la correction n'était
qu'écrite sur l'ardoise de démonstration, jamais rejouée dans l'animation. `ra_x3_2022N` disait même dans sa voix le
type et le noyau fils (« كيدير bêta moins وكيعطي le xénon ») que son exercice demandait ; `ra_x4_2025N` disait « N₀/4 »
et « N₀/8 » avant la question (règles logique 3 et 5, professeur 33, 37, 41). Les quatre pages démarraient avec `start`
(la scène courait seule, sans la voix).

**Ce qui est fait.**
- **Nouvelle page `radioactivite-tableau/national.html`**, une vue par exercice, avec les valeurs du sujet :
  `datation` (2022 R), `pu2021` (2021 N), `iode2022` (2022 N), `cd2025` (2025 N). À gauche le document peint (mêmes
  dessins que le reste du cours, règle 43 : compteur Geiger et bois de `datation.html`, fiole d'iode violette
  d'`activite.html`, stimulateur, noyau en grappe, positon et onde γ de `figures.html`), l'équation à compléter (« ᴬ_Z X »
  en rose) et le tableau des Z, puis la liste des résultats déjà trouvés ; en haut à droite la courbe a(t) ou N(t)
  **tracée dans le temps** ; en bas à droite l'étape en cours, écrite comme le barème (relation, application numérique,
  résultat encadré avec l'unité). Un moment nommé par étape (`play_until`), une correction **n'apparaît qu'à son moment** ;
  `?depart=<moment>` ouvre la page figée sur ce moment et `reset` y revient figé (plus de scène qui court seule).
  Les lectures se font sur la courbe : a₀/2 puis la verticale (t½ = 88 ans), 0,70·a₀ (t_max ≈ 45 ans), 0,05·a₀
  (t₁ ≈ 34,6 j), N₀/4 et N₀/8 avec l'écart N_d, l'abscisse du point a₁ = 318 Bq (t₁ ≈ 2,26·10³ ans).
- **Une diapositive par étape** (15 diapositives au lieu de 4) : chaque diapositive rejoue d'abord, sur la voix, la
  correction de l'étape d'avant dans l'animation, puis donne **une seule consigne** ; la question (QCM, réaction
  préparée par option, démonstration ligne à ligne) vient à la fin de la voix, avant toute correction.
  - Datation 2022 R : `ra_c3_calcul` ✍️ (document, point d'abscisse « t₁ = ? » ; ① la relation) → `ra_c3b_lambda` 🆕
    (correction ① ; ② λ en an⁻¹) → `ra_c3c_age` 🆕 (correction ② ; ③ t₁) → `ra_c3d_verif` 🆕 (correction ③ et
    **vérification** : a₁ > a₀/2 donc t₁ < t½, professeur 11). La voix ne fait plus aucun calcul avant la réponse de l'élève.
  - 2021 N : `ra_x2_2021N` ✍️ (① noyau fils, Soddy — question nouvelle, cas « équation » 13/13) → `ra_x2b_2021N` 🆕
    (② **lire t½** sur la courbe : la droite a₀/2 n'est tracée qu'après) → `ra_x2c_2021N` 🆕 (③ λ en s⁻¹ avec
    « 1 an = 365 jours » comme le sujet, puis N₀) → `ra_x2d_2021N` 🆕 (④ t_max pour 30 %) → `ra_x2e_2021N` 🆕
    (correction et vérification t_max < t½).
  - 2022 N : `ra_x3_2022N` ✍️ (① noyau fils ; la voix ne le dit plus) → `ra_x3b_2022N` 🆕 (② 95 % désintégrés ; t½ = 8 j
    déjà lue en `ra_a6_courbe_a`) → `ra_x3c_2022N` 🆕 (correction et encadrement 4t½ < t₁ < 5t½).
  - 2025 N : `ra_x4_2025N` ✍️ (① la particule et le type, β⁺ — question nouvelle ; la voix ne le dit plus) →
    `ra_x4b_2025N` 🆕 (② N₀ — question nouvelle —, ③ N_d entre 2t½ et 3t½) → `ra_x4c_2025N` 🆕 (corrections sur la
    courbe, puis le vrai/faux de cours du même sujet, dont « isotopes sur une perpendiculaire à l'axe des Z » : Segrè).
- **Séances** : la séance 7 devient « National joué pas à pas : datation 2022 R, stimulateur 2021 N » (3 blocs) et une
  séance 8 « iode 2022 N, cadmium 2025 N ; bilan » (3 blocs, le bilan et la carte à la fin). Comme en 1ʳᵉ passe, dans
  ces deux séances plusieurs tableaux « À toi » se suivent : chaque diapositive y est une étape d'examen.
- **Mots** (`verifier_mots.py` appliqué à la copie en attente) : « becquerels » → « becquerel » (corpus 3, pluriel 0) ;
  « خشب » → « le bois » ; « stimulateur cardiaque » dit « جهاز صغير كيعاون القلب » (le nom reste écrit) ; « demi-vies »
  dit « t un demi » (« quatre t un demi ») ; « numéro atomique » → « Z égale … » ; « فالطب » → « ف la médecine » ;
  « كيفوتوش », « باقيين », « كنتأكدو », « مشاش » remplacés ; l'énoncé français « au bout de combien … sont-ils » réécrit
  en darija. Gardés exprès (termes du programme ou des sujets, à écouter) : plutonium, uranium, iode, xénon, tellure,
  césium, positon, rayonnement ; les nombres composés (« quatre-vingt-huit »…) sont des nombres.

**Vérifications.** JSON chargé ; `verifier_pointage_simulations.py` : aucune nouvelle erreur « introuvable » (seule
`lambda_carbone` de `lambda.html`, déjà là, sur la copie et sur le cours en ligne) ; les trois écarts DEPART de x2-x4
ont disparu ; les écarts GESTE des nouvelles diapositives viennent de l'absence de piste (durée 0) et disparaissent avec
une durée estimée (13 caractères/s) ; `verifier_formules.py` : 0 sur le cours, rien sur `national.html` ;
`verifier_figures_cahier.py` : 0 erreur ; pytest « course or cours or concentration » : 88 passés, 1 échec SVT déjà là.
`national.html` : `node --check`, Chromium à 1280 × 640 et 724 × 350 (téléphone paysage) : chaque moment atteint,
encre sur le canvas, aucune erreur console, aucun texte hors cadre. **15 px partout, même au téléphone** : la page garde son propre plancher de 15 px à l'écran (comme `ondes-lumineuses-tableau/national.html`), indices, exposants, étages de fraction et A/Z des noyaux compris, sur sa craie seulement ; les hauteurs de ligne se calculent sur les tailles réellement écrites, l'étape 1 de la datation tient en trois lignes, les étiquettes de la courbe sont « 0,5·a₀ », « 0,25·N₀ »… Contrôle Playwright à chaque moment des quatre vues, à 724 × 350, 1024 × 560 et 1280 × 640 (taille de chaque texte dessiné, chevauchements, sorties de cadre) : 0 problème. Proton rose et neutron gris-bleu du lexique (`docs/lexique-visuel/README.md`, palettes clair / couleur / ombre) ; positon orange de `figures.html`.

**Ce qui reste.**
- Les voix : `phys_ch4_radioactivite_voix.json` (107 pistes, régénéré par `pistes_changees.py`) — dont 15 diapositives
  du national, leurs réactions préparées et démonstrations, les énoncés.
- Les réactions des quatre questions nouvelles sont écrites ici (règle 20), pas générées sur le VPS : à relire à l'écoute.
- `figures.html` (`fig_enonce_2021/2022/2025`) et l'ancienne vue de `datation.html` restent pour le cours en ligne ;
  `fig_enonce_2022` peint l'iode en jaune alors que le reste du cours (et `national.html`) le peint violet
  (`activite.html`) : à aligner quand la copie en attente remplacera le cours en ligne (règle 43). Aucun module commun
  `shared/lexique/` n'existe encore pour la radioactivité : les dessins sont copiés page à page.
- `ra_d6_type` (2018 R) reste un exemple dit par la voix (leçon de méthode), et `ra_f3_famille2024` (Segrè, 2024 R)
  garde sa forme (flèches jouées, question finale) ; `ra_x1_cas_types`, `ra_z1_bilan`, `ra_z2_carte` démarrent encore
  avec `start` (pages non pilotées par `?depart=`).
