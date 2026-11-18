# Architecture — `math_ch4_primitives` (Fonctions primitives, 2e Bac PC BIOF)

Refonte de la logique du 18 novembre 2026 (skill `logique-de-cours`). Cours en ligne `backend/data/courses/math_ch4_primitives.json` **inchangé** ; nouvelle version dans `backend/data/courses/en_attente/math_ch4_primitives.json` (partie de la version en attente, plus récente que la version en ligne). Pistes à mettre en voix : `math_ch4_primitives_voix.json` (31 pistes).

## 1. La logique avant

Ouverture → **cinq rappels d'affilée** (pente, puissances, écrire en puissance, produit, cos/sin) → I. définition et vérification → II. existence, famille F + k, condition → III. tableau → IV. somme, produit, transformer → V. formes u′uⁿ… → VI. reconnaître une dérivée, organigramme → VII. f pente de F → VIII. types national → IX. bilan.

Ce qui allait déjà : l'ordre suit les profs ; le tableau naît des dérivées lues à l'envers ; la famille F + k et le parallélisme sont vus sur l'animation ; la plupart des méthodes partent d'un exemple chiffré ; plusieurs diapositives s'arrêtent avant le résultat pour laisser l'élève finir (e7, c4, c7, r1).

Ce qui n'allait pas :
1. **Les rappels arrivaient tous au début**, loin de leur usage. Ils sont dans la même séance que leur usage, mais quatre diapositives de rappel d'affilée dépassent la limite de l'élève (≈ 4 éléments). La règle 6 et la demande de l'utilisateur disent : le rappel au moment où il sert.
2. **`pr_d4` redemandait l'exemple qu'on venait de montrer** (H = x sin x montré, puis « montre que H est une primitive de h »). L'élève n'avait rien à trouver.
3. **Les exercices du national étaient dits d'un bloc**. `pr_x1` (le « vérifier » qui tombe 11 fois sur 20) et `pr_x2` donnaient toute la solution, sans aucune réponse de l'élève. La règle 5 demande : une consigne à la fois, la réponse de l'élève, puis la correction écrite comme le barème.
4. **`pr_u2` donnait la règle sans faire appliquer tout de suite** : aucune question.

## 2. Les sources et ce qu'elles disent

- **Profs en vidéo** (`exploration/primitives.json`, 10 vidéos). Ordre commun : la dérivée lue à l'envers (9 profs), puis définition sur un intervalle, existence, F + k, condition, tableau, linéarité, formes avec la bulle u′. Une seule constante à la fin. Le cercle pour cos et sin.
- **Cours écrits en ligne** (lus le 18/11) :
  - Benmoussa (moutamadris, PC-SVT) : définition → existence → F + c → condition → somme et αf → opérations puis usuelles.
  - Atmani (moutamadris, BIOF, cours et résumé) : activités → définition → existence admise → F + k démontré → unicité → linéarité → tableau → opérations.
  - Cheddadi (AlloSchool, séance 7 SPC-SVT) : définition, P1–P3 → somme, αf → opérations → usuelles (avec ln et exp).
  - Aucun ne rappelle les dérivées avant le chapitre, aucun ne démontre les lignes du tableau. Les rappels au point d'usage et les lignes tirées des dérivées viennent de nos règles 3 et 6, pas des cours écrits.
  - **Ordre commun** : définition → existence → F + k → condition → linéarité → tableau → formes. Notre ordre le suit ; le tableau vient après la linéarité chez eux et avant chez nous, parce que la linéarité s'applique à des lignes du tableau (exemple avant règle).
- **Cadre** (`cadre_reference_2bac_pc.json`, PR1 à PR8 ; `perimetre.json`, integration 1.2.14–1.2.15). Chaque compétence K1–K8 cite ses capacités. Rien hors cadre : pas d'arctan, pas de changement de variable, pas de ∫ sans bornes, ln et exp seulement annoncés (x4), aucune partie « pour les devoirs ».
- **National** (cas types de l'exploration) :

  | Cas type | Fréquence | Où dans le cours |
  |---|---|---|
  | Vérifier une primitive | 11 sujets sur 20 | d3, d4, x1 — x1 joué pas à pas |
  | Primitive usuelle dans une intégrale | 20 sur 20 (semestre 2) | u1–u7, l1 |
  | u′uⁿ | 2 sujets, très fréquent en devoir | c1–c5, x2 |
  | Ensemble des primitives, condition | 0 au national, 10 profs en devoir | e1–e7, dans le cadre (PR2–PR4) |

## 3. Les décisions et leurs raisons

| Décision | Raison |
|---|---|
| Rappels déplacés : z1 reste avant d1 ; z2 et z3 juste avant d3 ; z5 et z4 juste avant d4 | Règle 6 : chaque rappel sert à la diapositive suivante. d3 est le premier usage de (x³)′ et de (1/x)′ ; d4 le premier usage de (sin x)′ et de (uv)′. Les rappels ne sont plus jamais plus de deux d'affilée (règle 7). |
| `pr_d4` : l'élève fait l'exemple suivant, G = x cos x | Règle 3 : méthode montrée, puis l'exemple suivant fait par l'élève. L'ancien exercice devient la question, avec sa démonstration et ses réactions déjà voisées. |
| `pr_x1` joué pas à pas | 11 sujets sur 20. Énoncé, puis ligne 1 dite. L'élève calcule H′(x) (question, réactions préparées), puis met au même dénominateur (exercice). Chaque correction est la démonstration écrite comme le barème (dérivable, u, u′, v, v′, formule, même dénominateur, conclusion avec l'intervalle). |
| `pr_x2` : la voix s'arrête avant k | L'élève trouve k ; la démonstration donne F complète. |
| `pr_u2` : question « une primitive de x² » | Application immédiate de la règle. La question et ses réactions viennent des exercices de fin de cours. |
| Ordre des parties II à IX gardé | Il suit l'ordre commun des profs et les règles 3 à 6. |
| Le lien graphique (g1, g2) gardé | Il est dans le cadre (PR8) et prépare l'intégrale du semestre 2. |
| `pr_u8` (1 + tan²) gardé, « pour mémoire » | Dans le cadre (1.2.14) mais jamais au national : une seule diapositive. |

## 4. Ce qui ne change pas, et pourquoi
Les 51 autres diapositives gardent leur id, leur texte et leur voix : elles sont seulement déplacées, ou ne bougent pas. Elles respectent déjà les règles : exemple avant règle (u1 → u2, c1 → c1_b), arrêt avant le résultat (e7, c4, c7, r1), animations qui produisent ce qui est dit (famille, cercle, pente).

## 5. Animations
Aucune simulation n'est modifiée. Les diapositives réécrites gardent leurs vues (`calculs.html?vue=x1`, `x2`, `d4`) ; seul le pointage est raccourci jusqu'au moment où la voix s'arrête. La suite est écrite par la démonstration de la question.

Besoin noté, pas fait car hors de ce lot : une vue `x1` qui s'arrête avant le moment `calcul` et le rejoue après la réponse. Le lecteur ne le fait pas encore (fichier partagé `frontend/src/`).

## 6. Mots et voix
Chaque texte réécrit a été vérifié par `scripts/voix/verifier_mots.py`.
- Mots rares remplacés : « كندريفيوش » → « ما كنحسبو la dérivée من الراس » ; « البرتقالي » → « بلون orange » (pointage mis à jour) ; « كيطيح » → « كيجي » ; « وضربتيهم » → « ومن بعد ضربتي جوج » ; « كنحيدوه » → « كنحيدو ».
- Gardés et à écouter : « dérivables », « bulle », « telle », termes du programme ou du cours déjà dits par la voix.
- Pistes à faire : 3 diapositives (d4, x1, x2), 4 démonstrations, 24 réactions et énoncés.

## 7. Le plan, diapositive par diapositive
Légende : ↕ déplacée (texte et voix gardés) · ✎ réécrite (voix à refaire) · ＋❓ question ajoutée.

### Séance 1 — La définition, et chaque rappel quand il sert


**Bloc `pr_s1_b1` — Primitiver ; la pente ; la marche arrière ; la définition** · fin de bloc : cahier (4 lignes), retrouver « Cahier fermé : écris la définition complète de « F est une primitive de f sur I ». », exercice « La dérivée d'une constante k est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_o1` La carte du chapitre : dériver, puis revenir | Ouverture | — | Le but avant le détail : la carte dériver ↔ primitiver, avec la fréquence au national (vérifier 11/20, intégrale 20/20). Les 9 profs sur 10 partent de la dérivée lue à l'envers. |
|  | `pr_z1_pente` Rappel : la dérivée, c'est la pente | Ouverture | — | Rappel (règle 6) juste avant la marche arrière : d1–d2 parlent de la pente et e3–e5 de (k)′ = 0. Expliqué deux fois (tangente, puis route). |
|  | `pr_d1` La marche arrière : de la dérivée vers la fonction | I. Définition et vérification (chaque rappel juste avant son usage) | — | Exemple chiffré d'abord (x² → 2x, puis 2x → ?) : la méthode montrée avant la définition (règle 3). Analogie validée « marche arrière » (Aderdour). |
|  | `pr_d2` Définition : une primitive de f sur un intervalle | I. Définition et vérification (chaque rappel juste avant son usage) | — | La définition construite par trois questions sur l'exemple de d1 (profs : définition sur un intervalle, PR1). Deux façons : formelle, puis « route et pente ». |

**Bloc `pr_s1_b1b` — Rappels : puissances, écrire en puissance ; vérifier une primitive** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris la dérivée de xⁿ. », exercice « G(x) = x⁴ + 5 est-elle une primitive de g(x) = 4x³ sur ℝ ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ↕ | `pr_z2_puissances` Rappel : dériver une puissance | I. Définition et vérification (chaque rappel juste avant son usage) | ❓ Quelle est la dérivée de x⁵ ? | DÉPLACÉE (était en ouverture) : (xⁿ)′ sert pour la première fois en d3 ((x³)′ = 3x²). Question : (x⁵)′. |
| ↕ | `pr_z3_ecrire` Rappel : écrire en puissance | I. Définition et vérification (chaque rappel juste avant son usage) | — | DÉPLACÉE : (1/x)′ = −1/x² sert en d3, et 1/x² = x⁻² en e2 ; u4 la reprend plus loin (« comme on l'a vu au début »), donc deux passages. |
|  | `pr_d3` Vérifier une primitive : on dérive | I. Définition et vérification (chaque rappel juste avant son usage) | — | La question du national n° 1 (PR1, 11 sujets sur 20) : rédaction en trois lignes, sur un exemple chiffré. |

**Bloc `pr_s1_b2` — Rappels : cos, sin, produit ; vérifier quand F est un produit** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris la dérivée d'un produit u·v. », exercice « Quelle est la dérivée de cos x ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ↕ | `pr_z5_cos_sin` Rappel : cos, sin et leurs dérivées | I. Définition et vérification (chaque rappel juste avant son usage) | ❓ Quelle est la pente de la courbe de sin au point d'abscisse π ? | DÉPLACÉE : (sin x)′ = cos x sert en d4 (H = x sin x), puis au cercle u6. |
| ↕ | `pr_z4_produit` Rappel : dériver un produit | I. Définition et vérification (chaque rappel juste avant son usage) | — | DÉPLACÉE : (uv)′ sert en d4 et dans tous les « vérifier » du national (presque toujours un produit). |
| ✎ | `pr_d4` Vérifier quand F est un produit | I. Définition et vérification (chaque rappel juste avant son usage) | ❓ G(x) = x cos x est une primitive sur ℝ de : | RÉÉCRITE (fin de la voix + question) : l'exemple H = x sin x est montré, puis l'élève fait l'exemple SUIVANT (G = x cos x : primitive de quoi ?) ; avant, la question redemandait l'exemple qu'on venait de donner. |

### Séance 2 — Existence, toutes les primitives, la condition


**Bloc `pr_s1_b3` — Existence ; toujours un intervalle ; une infinité** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris la propriété qui garantit l'existence de primitives. », exercice « g(x) = √x + cos x admet des primitives sur : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_e1` Quand une fonction a-t-elle des primitives ? | II. Existence, famille F + k et condition | — | Existence (PR2) : la phrase à écrire à chaque exercice (5 profs) ; vient après « vérifier » car elle répond à « existe-t-elle ? » avant de chercher. |
|  | `pr_e2` Toujours sur un intervalle | II. Existence, famille F + k et condition | — | Piège des profs (Aderdour : « ℝ* ») : toujours un intervalle, vu sur l'axe troué. |
|  | `pr_e3` Une infinité de primitives | II. Existence, famille F + k et condition | ❓ Quelle est la dérivée de x² + 10 ? · ✏️ Laquelle de ces fonctions n'est PAS une primitive de 2x sur ℝ ? | La famille construite par l'élève (2x, 2x + 10…, 6 profs) avant la propriété : exemple avant règle. |

**Bloc `pr_s2_b1` — F + k : une primitive, et toutes les primitives** · fin de bloc : cahier (2 lignes, 1 figure(s)), retrouver « Cahier fermé : G et F sont deux primitives de f sur I ; écris G(x) en fonction de F(x). », exercice « F et G sont deux primitives de f sur un intervalle I. Alors : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_e4` F + k est encore une primitive | II. Existence, famille F + k et condition | — | F + k est une primitive : preuve en une ligne (dérivée d'une constante, vue en z1). |
|  | `pr_e4_b` Toutes les primitives : F + k, et pas d'autres | II. Existence, famille F + k et condition | — | Et seulement celles-là : (G − F)′ = 0 (Math & Phys) ; deux façons (calcul, « deux marcheurs »). Réponse à la plainte n° 1 des commentaires (« + C »). |
|  | `pr_e5` Ce qu'on voit : des courbes translatées, mêmes pentes | II. Existence, famille F + k et condition | 👀 observation | Ce qu'on voit : translation verticale, même pente (aucun prof ne le dessine) ; une observation laisse l'élève trouver le parallélisme. |

**Bloc `pr_s2_b1b` — La condition F(x₀) = y₀** · fin de bloc : cahier (2 lignes), retrouver « Cahier fermé : comment trouve-t-on k avec la condition F(x₀) = y₀ ? », exercice « f(x) = 3x² sur ℝ : la primitive F telle que F(0) = 5 est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_e6` La primitive qui passe par un point | II. Existence, famille F + k et condition | — | La condition F(x₀) = y₀ (PR4, 3 profs) montrée sur la courbe qui glisse jusqu'au point, puis le calcul. |
|  | `pr_e7` À toi : une condition avec un calcul plus long | II. Existence, famille F + k et condition | ❓ f(x) = 2x² + x + 1 + 1/x² sur ]0 ; +∞[ et F(1) = 3. La constante k vaut : · ✏️ f(x) = 4x³ − 2x + 3 sur ℝ : la primitive F telle que F(1) = 0 est : | L'élève fait seul l'exemple suivant, plus long ; la voix s'arrête avant k (règle 3). |

### Séance 3 — Le tableau des primitives usuelles


**Bloc `pr_s2_b2` — Le tableau : k, xⁿ, le coefficient devant** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris une primitive de xⁿ (n ∈ ℕ*). », exercice « Sachant que (x³)′ = 3x², une primitive de 3x² sur ℝ est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_u1` Le tableau des primitives : les dérivées à l'envers | III. Le tableau des primitives usuelles | — | Le tableau naît des dérivées lues à l'envers (convergence n° 1 des profs) : des exemples avant la règle de u2. |
| ＋❓ | `pr_u2` k et xⁿ : monter l'exposant, diviser | III. Le tableau des primitives usuelles | ❓ Une primitive de x² sur ℝ est : | La règle xⁿ → xⁿ⁺¹/(n + 1) tirée des exemples de u1. AJOUT : question « une primitive de x² » (l'élève applique tout de suite, avec ses réactions déjà écrites). |
|  | `pr_u3` Le coefficient reste devant | III. Le tableau des primitives usuelles | ❓ Une primitive de 2x³ sur ℝ est : · ✏️ Une primitive de (1/4)x³ sur ℝ est : | Le coefficient reste (piège des commentaires : « pourquoi 1/4 devant ? »). |

**Bloc `pr_s2_b3` — 1/x², puis 1/xⁿ** · fin de bloc : cahier (1 lignes), retrouver « Cahier fermé : écris une primitive de 1/x² sur ]0 ; +∞[. », exercice « Une primitive de 1/x³ sur ]0 ; +∞[ est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_u4` 1/x² : le moins qui apparaît | III. Le tableau des primitives usuelles | — | 1/x² : le moins qui apparaît (plainte des commentaires) ; passe par x⁻² (rappel z3). |
|  | `pr_u4_b` 1/xⁿ : la règle générale | III. Le tableau des primitives usuelles | — | 1/xⁿ : la règle générale, après le cas simple. |

**Bloc `pr_s2_b3b` — Racines ; cos et sin** · fin de bloc : cahier (2 lignes, 1 figure(s)), retrouver « Cahier fermé : écris une primitive de 1/√x sur ]0 ; +∞[. », exercice « Une primitive de 1/x² sur ]0 ; +∞[ est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_u5` 1/√x : deux racine de x | III. Le tableau des primitives usuelles | — | 1/√x : deux façons (dérivée de √x ; puissance −1/2). Plainte : « d'où vient le 2 ». |
|  | `pr_u5_b` xʳ et les racines : passer en puissance | III. Le tableau des primitives usuelles | — | xʳ et les racines (PR5). |
|  | `pr_u6` cos et sin : le cercle | III. Le tableau des primitives usuelles | ❓ Une primitive de sin x sur ℝ est : · ✏️ Vrai ou faux ? | cos et sin : le cercle (7 profs, même disposition) ; l'élève suit la flèche pour sin. |

**Bloc `pr_s3_b1` — cos(ax + b), 1 + tan²x, une somme** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris la règle des primitives d'une somme et d'un produit par un réel α. », exercice « Une primitive de sin(3x + 2) sur ℝ est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_u7` cos(ax + b) : diviser par le nombre collé à x | III. Le tableau des primitives usuelles | — | cos(ax + b) : diviser par le nombre collé à x (cas le plus fréquent dans les intégrales du national). |
|  | `pr_u8` Pour mémoire : 1 + tan²x | III. Le tableau des primitives usuelles | — | 1 + tan²x « pour mémoire » : dans le cadre (1.2.14) mais 0 sujet ; une seule diapositive, sans compétence à part. |
|  | `pr_l1` Une somme : chaque terme sa primitive, une seule constante | IV. Somme, produit, transformer l'écriture | ❓ Les primitives de f(x) = 5x⁴ + 3x + 1 sur ℝ sont les fonctions : · ✏️ Les primitives de f(x) = 4x³ − 2x + 3 sur ℝ sont les fonctions : | Linéarité, une seule constante (PR6, 8 profs). |

### Séance 4 — Somme, produit et la forme u′uⁿ


**Bloc `pr_s3_b2` — Pas facteur par facteur ; transformer ; dériver uⁿ** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris la dérivée de uⁿ. », exercice « Les primitives de f(x) = (x + 1)² sur ℝ, après avoir développé, sont les fonctions : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_l2` Un produit : la primitive ne se fait pas facteur par facteur | IV. Somme, produit, transformer l'écriture | — | Le produit ne se primitive pas facteur par facteur : on dérive la réponse fausse (piège vivant des commentaires). |
|  | `pr_l3` Transformer l'écriture avant de primitiver | IV. Somme, produit, transformer l'écriture | — | Transformer l'écriture avant de primitiver (PR6). |
|  | `pr_c1` Rappel : dériver une puissance d'une expression | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | ❓ Quelle est la dérivée de (x² + 1)⁴ ? | Rappel (uⁿ)′ au moment où il sert : juste avant la forme u′uⁿ (plainte « il faut faire descendre la puissance »). |

**Bloc `pr_s3_b2b` — D'où vient u′uⁿ ; la bulle** · fin de bloc : cahier (2 lignes), retrouver « Cahier fermé : écris une primitive de u′uⁿ (n ∈ ℕ*). », exercice « Vrai ou faux ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_c1_b` La forme u′uⁿ : la dérivée lue à l'envers | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | ✏️ Une primitive de u′u⁴ est : | La forme u′uⁿ tirée de la dérivée de c1 (primitive = dérivée lue à l'envers). |
|  | `pr_c2` Repérer u et sa dérivée : la bulle | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | — | La bulle u′ (convergence des profs) sur un exemple où u′ est déjà là. |

**Bloc `pr_s3_b3` — Il manque un nombre ; (ax + b)ⁿ** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : quelle forme reconnais-tu quand la dérivée de la parenthèse est devant ? Écris sa primitive. », exercice « f(x) = 2x(x² + 5)⁴ sur ℝ. Une primitive de f est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_c3` Il manque un nombre : multiplier et diviser | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | — | Il manque un nombre : × 2/2 (9 profs). |
|  | `pr_c3_b` On ne prête qu'un nombre | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | — | On ne prête qu'un nombre, jamais x (piège). |
|  | `pr_c4` (ax + b)ⁿ : le cas le plus fréquent | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | ❓ Une primitive de f(x) = (2x − 1)³ sur ℝ est : · ✏️ Une primitive de (3x + 2)⁴ sur ℝ est : | (ax + b)ⁿ : le cas le plus fréquent ; la voix s'arrête avant le résultat, l'élève le trouve. |

### Séance 5 — Les autres formes, les dérivées reconnues, le lien graphique


**Bloc `pr_s4_b1` — u′uʳ, u′/u², u′/√u** · fin de bloc : cahier (4 lignes), retrouver « Cahier fermé : écris une primitive de u′/u². », exercice « Sur ]−1/2 ; +∞[, une primitive de f(x) = 1/√(2x + 1) est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_c5` u′uʳ : avec une racine | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | — | u′uʳ avec une racine (PR7). |
|  | `pr_c6` u′/u² : un carré en bas | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | — | u′/u² : tirée de (−1/u)′, puis un exemple. |
|  | `pr_c6_b` u′/uⁿ : la règle générale | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | — | u′/uⁿ : la règle générale (après le cas carré). |
|  | `pr_c7` u′/√u : une racine en bas | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | ❓ Une primitive de f(x) = x/√(x² + 1) sur ℝ est : · ✏️ Vrai ou faux ? | u′/√u : tirée de (√u)′ ; l'élève finit l'exemple. |

**Bloc `pr_s4_b2` — Choisir la forme ; u′cos u ; reconnaître u′v + uv′** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : écris une primitive de u′·cos u et une primitive de u′·sin u. », exercice « Une primitive de f(x) = x·sin(3x²) sur ℝ est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_c8` Même numérateur, trois dénominateurs | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | — | Même numérateur, trois dénominateurs : choisir la forme (une seule prof, Prof fati ; difficulté des élèves). |
|  | `pr_c9` u′·cos u et u′·sin u | V. Les formes composées u′uⁿ, u′/u², u′/√u, u′cos u | — | u′cos u (commentaire : « quelle propriété pour πx·cos(πx² + 3) ? »). |
|  | `pr_r1` Reconnaître la dérivée d'un produit | VI. Reconnaître une dérivée ; choisir la méthode | ❓ Les primitives de f(x) = sin x + x cos x sur ℝ sont les fonctions : · ✏️ Une primitive de f(x) = 2x·cos x − x²·sin x sur ℝ est : | Reconnaître (uv)′ : réponse au piège de l2 ; l'élève donne les primitives. |

**Bloc `pr_s4_b3` — Quotient reconnu, organigramme, f pente de F** · fin de bloc : cahier (4 lignes, 1 figure(s)), retrouver « Cahier fermé : que dit le signe de f sur les primitives de f ? », exercice « Pour f(x) = x²(x³ + 1)⁴ sur ℝ, une primitive est : »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_r2` Reconnaître la dérivée d'un quotient | VI. Reconnaître une dérivée ; choisir la méthode | — | (u′v − uv′)/v² → u/v : dans le cadre (1.2.15), une seule diapositive. |
|  | `pr_r3` Choisir la méthode : l'organigramme | VI. Reconnaître une dérivée ; choisir la méthode | — | L'organigramme : par quoi commencer (synthèse des méthodes, avant les exercices du national). |
|  | `pr_g1` La courbe de f est la pente de F | VII. La courbe de f est la pente de F | — | f est la pente de F (PR8) : prépare l'intégrale ; animation à deux repères. |
|  | `pr_g2` Signe de f, variations de F | VII. La courbe de f est la pente de F | ❓ f(x) = x² − 1 et F est une primitive de f sur ℝ. F est décroissante sur : · ✏️ f(x) = 3 − x et F est une primitive de f sur ℝ. F est croissante sur : · 👀 observation | Signe de f → variations de F (PR8) ; l'élève trouve par l'observation, puis la question. |

### Séance 6 — Types national, bilan et carte


**Bloc `pr_s5_b1` — Trois exercices type national** · fin de bloc : cahier (3 lignes), retrouver « Cahier fermé : comment justifies-tu que f admet des primitives sur I ? », exercice « Montre que G(x) = (x − 1)√x est une primitive de g(x) = (3x − 1)/(2√x) sur ]0 ; +∞[. Quelle expression de G′(x) écris-tu d'abord ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
| ✎ | `pr_x1` Type national : montrer que H est une primitive de h | VIII. Exercices type national | ❓ H(x) = (x² + 1)√x sur ]0 ; +∞[ : que vaut H′(x) ? · ✏️ Sur le dénominateur 2√x : 2x√x + (x² + 1)/(2√x) = ? | RÉÉCRITE : le « vérifier » du national joué pas à pas — la voix dit l'énoncé et la ligne « dérivable », puis l'élève calcule H′(x) (question), puis met au même dénominateur (exercice) ; chaque correction est la démonstration écrite comme le barème. Avant : tout était dit d'un bloc. |
| ✎ | `pr_x2` Type national : forme u′uⁿ et condition | VIII. Exercices type national | ❓ F(x) = (x² + x + 1)³/3 + k et F(0) = 1. Alors : | RÉÉCRITE : forme u′u² puis condition ; la voix s'arrête avant k, l'élève le trouve (question + démonstration). |
|  | `pr_x3` Exercice bilan | VIII. Exercices type national | ❓ Pour une somme de deux termes, combien de constantes k écrit-on dans les primitives ? · ✏️ f(x) = x/(x² + 1)² + cos(2x) : la primitive F de f sur ℝ telle que F(0 | Exercice bilan (existence, forme, cos(2x), condition) ; question sur la seule constante. |

**Bloc `pr_s5_b2` — Ce qui viendra ; ce qu'il faut retenir ; la carte** · fin de bloc : cahier (4 lignes), retrouver « Cahier fermé : écris une primitive de sin x (attention au signe). », exercice « Vrai ou faux ? »

| # | Diapositive | Partie | Ce qu'elle apprend · élève | Pourquoi ici (source) |
|---|---|---|---|---|
|  | `pr_x4` Ce qui viendra : ln, exp et l'intégrale | VIII. Exercices type national | — | Ce qui viendra (ln, exp, intégrale) : annoncé, pas enseigné (hors cadre du chapitre pour l'instant). |
|  | `pr_b1` Ce qu'il faut retenir | IX. Bilan et carte du chapitre | — | Ce qu'il faut retenir (fiche, une page) — règle du bilan. |
|  | `pr_b2` La carte du chapitre | IX. Bilan et carte du chapitre | ❓ Pour vérifier que F est une primitive de f sur I, la première chose à faire est : | La carte du chapitre — règle du bilan. |
