# Pistes nouvelles (lot A) : Ondes mécaniques progressives

*2026-11-07. Matériau : `extraits_A.md` (mises en garde, renvois au bac, questions aux élèves), contexte vérifié dans les transcriptions `transcripts/<videoId>.ar-orig.txt`. Comparé à `experience_profs.json` (ondes_mecaniques) et à `experience-profs-ondes-synthese.md`.*

## 0. Avertissements sur le matériau

**Noms des profs** : la première version de `extraits_A.md` avait des en-têtes décalés. Le coordinateur l'a régénéré depuis, et la correspondance qu'il a confirmée est exactement celle du tableau ci-dessous, que j'avais établie de mon côté en retrouvant chaque phrase dans les fichiers. Ce document utilise partout les vrais noms et donne toujours l'identifiant de la vidéo. Le tableau sert seulement à relire une ancienne copie de `extraits_A.md` :

| Étiquette dans extraits_A | Vidéo | Prof selon la 1re analyse |
|---|---|---|
| « TOP » | 00vbZrDiky0 | Driss DOTCOM |
| « Chargui » | 27FyalYEXhg | Taousse |
| « Noureddine live » | W9XwPFD0sMU | Laksabi (la vidéo dit d'ailleurs « بروف قصابي ») |
| « Laksabi » | lyiJmLP67Dk | Chargui |
| « Driss » | XLQdN4C9L5g | AdrarPhysic |
| « Taousse » | YCzE0EZvsC8 | TOP (cours) |
| « BacFacile » | vG-rfo1TLAA | TOP (série) |
| « AdrarPhysic » | iCQNAgZZors | bacfacile |
| « Noureddine » | GW-FyuY-rpA | Noureddine (en classe) |

**Rendement honnête** : environ 380 lignes, dont près de la moitié est du bruit : publicité pour des lives et des abonnements, « ركز معايا » sans contenu, ou transcription illisible (Noureddine en classe, Maria). La grande majorité des mises en garde et des renvois au bac **redisent ce qui est déjà dans la fiche** : conversions, front, 2d, retard positif, barème, 1/v. Les pistes vraiment nouvelles sont une quinzaine ; elles sont listées ci-dessous, de la plus forte à la plus faible.

Légende : **NOUVEAU** = absent de la fiche ; **AFFINE** = précise une entrée existante (nommée).

---

## 1. Erreurs et confusions d'élèves (nouvelles ou mieux formulées)

### 1.1 QCM d'élongation : distracteur de conversion et forme « + τ » sur le point en retard
- **Piste** : au QCM, le national propose à la fois y_M(t) = y_S(t − 0,04) (vrai), y_M(t) = y_S(t − 0,4) (faux : 40 ms mal convertis), y_M(t) = y_S(t + 0,04) (faux) **et** y_S(t) = y_M(t + 0,04), qui est **vraie** : c'est la même relation, écrite depuis le point en retard. Les élèves qui ne reconnaissent que la forme « (t − τ) » rejettent cette dernière.
- **Source** : AdrarPhysic (XLQdN4C9L5g) [31:00–31:30] ; Driss (00vbZrDiky0) [30:00–31:00], dans le corrigé d'un national.
- **Citation** : « ا ام د تي كساوي ا اس ب 04 هذ خطا حيت ماش الزائد » ; « ا اس د تي كساوي ا ام ... هذ صحيحه ».
- **Statut** : AFFINE le piège « signe ± de l'élongation appliqué par une règle apprise ». Deux idées sont nouvelles : (a) le distracteur 0,4 / 0,04 ; (b) la forme y_tôt(t) = y_tard(t + τ) est juste.
- **Programme** : au programme.

### 1.2 « Dimension » définie par le mouvement du point : à ne pas dire
- **Piste** : Laksabi définit « bidimensionnelle » par le fait que le point M bouge selon x **et** y, et dit même que M « va sortir du seau ». C'est **faux** deux fois. La dimension compte les directions de **propagation** (corde : 1, surface : 2, son dans l'air : 3). Et le point ne quitte pas sa place : cela contredit « énergie oui, matière non ».
- **Source** : Laksabi (W9XwPFD0sMU) [29:30–31:00].
- **Citation** : « هاديك النقطة إم غتخرج على برا ... تبدلات بالنسبة لإكس وتبدلات بالنسبة لإغريك كنقولو بي ديمونسيونيل ».
- **Statut** : NOUVEAU. La fiche n'a aucune entrée sur les dimensions, ni dans `pieges` ni dans `a_ne_pas_dire`.
- **Programme** : au programme (perimetre : « onde à une, deux ou trois dimensions »). À ajouter dans `a_ne_pas_dire` ; dire plutôt : « la dimension, c'est le nombre de directions dans lesquelles l'onde se propage ».

### 1.3 Sens de conversion inversé au retour vers l'unité de la figure
- **Piste** : la conversion cm → m (×10⁻²) est bien sue. L'erreur arrive au retour : pour dessiner sur la figure ou répondre dans l'unité de l'énoncé, il faut ×10⁺² (m → cm) ou ×10⁺³ (s → ms, m → mm). Le prof se trompe lui-même devant la classe, puis se corrige.
- **Source** : Laksabi (W9XwPFD0sMU) [1:38:00–1:38:30] et [2:53:30] ; Driss (00vbZrDiky0) [28:30] (47,5 ms) et [29:30] (« 4 cm » pour dessiner).
- **Citation** : « علاش ضربت في بلوس دو وماشي موان دو ... أنا خربقتها الوغ رجعت بالعكس ».
- **Statut** : AFFINE l'insistance « conversions dites avant le calcul ». Il manque à la fiche le geste inverse et le changement de signe de l'exposant.
- **Programme** : au programme.

### 1.4 Lecture du sens de déplacement : les QCM « monte puis descend »
- **Piste** : la question type demande de choisir, pour un point M, entre « monte puis redescend », « descend puis remonte » et « avance puis revient ». Le piège est le déplacement horizontal : le point ne bouge pas selon x.
- **Source** : TOP série (vG-rfo1TLAA), passages [1:30] et [6:30–7:00] repérés dans les extraits.
- **Citation** : « واش غادي تطلع وترجع تهبط ولا تهبط وترجع تطلع ولا تمشي وترجع ».
- **Statut** : AFFINE le cas type `etat_vibratoire` : c'est une question diagnostique prête à l'emploi.
- **Programme** : au programme.

### 1.5 Règle raccourcie « corde donc transversale, eau toujours transversale »
- **Piste** : un prof enseigne une règle de reconnaissance par l'exemple (« corde → transversale directement »). Un autre rappelle que le ressort transversal est rare au national et dans les exercices, mais qu'il faut le connaître.
- **Source** : TOP série (vG-rfo1TLAA) [31:00–31:30] ; Taousse (27FyalYEXhg) [21:30].
- **Citation** : « بما انه تكلمي على لاكورد مباشره ... ترونسفيرسال » ; « قليل عمري شفت أنايا فالوطني ... لكن خاصكم تعرفوها ».
- **Statut** : AFFINE le piège « le ressort est toujours longitudinal ». Il montre que des profs **enseignent** ce raccourci : le tuteur doit s'attendre à le voir chez l'élève.
- **Programme** : au programme.

## 2. Comment le bac demande les choses

### 2.1 Caméra à N images par seconde : le retard se compte en intervalles d'images
- **Piste** : situation où une caméra filme la corde à 25 images/s. « Donner le retard entre l'image n° 8 et l'image n° 12 » : 12 − 8 = 4 intervalles, donc τ = 4/25 = 0,16 s. Pièges : compter les images au lieu des intervalles, et ne pas voir que 1/25 s est la durée entre deux images.
- **Source** : Laksabi (W9XwPFD0sMU) [0:54:30–1:00:00]. Il dit que c'est tombé au national, sans savoir lequel. Ce n'est pas l'un des 10 nationaux déjà dépouillés : **à vérifier**.
- **Citation** : « كتضرب 25 تصويرة في الثانية ... ما بين ثمانية و12 هي أربعة التصاور ».
- **Statut** : NOUVEAU cas type (chronophotographie ou vidéo). Indices : « images par seconde », « image n° ».
- **Programme** : au programme (exploiter une photographie ou un enregistrement).

### 2.2 Libellés exacts et ce qui rapporte le point
- **« Répondre par vrai ou faux »** : on écrit seulement V ou F.
- **« Quelle est la nature de l'onde ? Quelle est sa dimension ? »** : on répond « transversale, à une dimension » sans justifier, sauf si la question dit « justifier ».
- **« Identifier les points qui se dirigent vers le haut / vers le bas à l'instant t »** : libellé du national cité mot pour mot.
- **Source** : Driss (00vbZrDiky0) [17:00], [22:30–24:00], dans le corrigé du national 2022 N.
- **Citation** : « ما قالش لك جوستيفي ماديرش جوستيفيكاسيون ... قال ليا فقط أعطيني لا ناتوغ دو لوند ».
- **Statut** : AFFINE l'erreur « justifier ce qui n'est pas demandé » de la synthèse (§C), qui n'est pas encore dans la fiche JSON. Les libellés « nature » et « dimension » sont nouveaux.
- **Programme** : au programme.

### 2.3 Source déclenchée à t₀ ≠ 0
- **Piste** : quand la source démarre à t₀ et non à 0, la date d'arrivée en M est t_M = SM/v + t₀. Certains énoncés ne donnent pas de figure : seulement la source, la date de départ et la position du front.
- **Source** : TOP cours (YCzE0EZvsC8) [16:00–16:30] ; Taousse (27FyalYEXhg) [24:00–24:30] pour Δt = t_final − t_initial.
- **Citation** : « طي ان ك تساوينا اس ام على في زائد طي 0 ».
- **Statut** : AFFINE le cas type `photo` (t₁ inconnu).
- **Programme** : au programme.

### 2.4 Droite et identification « par analogie »
- **Piste** : quand le national trace une grandeur en fonction d'une autre (par exemple L en fonction de τ entre deux milieux), la méthode est la suivante :
  1. écrire la relation théorique sous la forme y = A·x ;
  2. identifier A à son expression littérale, ici A = 1/(1/v_air − 1/v_eau) ;
  3. calculer la pente avec l'origine et **un seul** point bien lisible ;
  4. convertir cm et ms sur la pente ;
  5. en déduire la célérité inconnue.
- **Source** : Laksabi (W9XwPFD0sMU) [3:33:30–3:39:00].
- **Citation** : « غناخد نقطة وحدة ماشي جوج نقط لأن النقطة الأخرى كتكون معلومة ».
- **Statut** : AFFINE les cas types `droite` et `deux_milieux`. L'étape « identifier A à une expression littérale » manque dans la fiche, qui ne connaît que les pentes v et 1/v.
- **Programme** : au programme. Attention : l'exemple vient en partie de **Sciences Maths 2016** [3:55:00]. C'est une autre filière, à ne pas présenter comme un national PC.

### 2.5 Même eau, deux profondeurs
- **Piste** : la célérité est donnée par v = √(g·h) ; elle change entre deux zones de profondeur h₁ et h_N. On relit le schéma pour savoir quelle profondeur va avec quelle zone, et on prend les distances sur la figure.
- **Source** : Laksabi (W9XwPFD0sMU) [3:02:30–3:04:00].
- **Citation** : « هو داك الارتفاع ديال البغوفوندوغ ديال الميليو الاول ... واش انت عندك الفيتيس في لي دوني ».
- **Statut** : AFFINE `homogeneite` et `deux_milieux`. La fiche ne cite √(g·h) que pour l'homogénéité.
- **Programme** : au programme si l'énoncé donne la formule (perimetre : « profondeur de l'eau »). Elle n'est jamais à retenir.

### 2.6 Deux voies pour τ, puis comparer et conclure
- **Piste** : la série enchaîne trois questions. D'abord τ lu sur l'oscillogramme en µs (×10⁻⁶) **ou** calculé par d/v. Ensuite « quel capteur reçoit le signal en premier ? ». Enfin, pour la même distance (40 cm) dans l'air et dans un métal : comparer les τ et en conclure que v_métal > v_air.
- **Source** : TOP série (vG-rfo1TLAA) [17:00–22:00].
- **Citation** : « لو غوط اللي دوزو في الميتال صغر من لوغوطار ... بسرعه اكبر ».
- **Statut** : AFFINE `oscillogramme`. La question « comparer puis conclure » est nouvelle.
- **Programme** : au programme.

### 2.7 Homogénéité : rédiger en dimensions
- **Piste** : un prof affirme que la méthode « équation aux dimensions » est celle qui est comptée juste au bac et au contrôle, et que remplacer les unités est une autre méthode.
- **Source** : Chargui (lyiJmLP67Dk) [46:30].
- **Citation** : « هذه هي الطريقه اللي غ تحسب لك صحيحه في الامتحان و في الفرض ».
- **Statut** : AFFINE `homogeneite`. L'affirmation n'est pas vérifiée : il faut répondre avec l'outil que la question nomme (« équation aux dimensions » ou « unité »).
- **Programme** : au programme.

## 3. Questions diagnostiques reprises par le tuteur (avec le moment)

| Moment | Question | Source |
|---|---|---|
| Avant d'écrire y_M(t) | « Est-ce que la hauteur de la bosse change entre S et M ? » Réponse : non (pas d'amortissement), donc M refait le mouvement de S, plus tard. | Driss (00vbZrDiky0) [30:00] « واش ال إكريك ديالها كيتبدل؟ » |
| Après deux exemples d'élongation | « Alors, quand est-ce qu'on met le plus ? » | Laksabi (W9XwPFD0sMU) [1:07:00] « دابا فهمتي إمتى كدير البلوس؟ » |
| Lecture d'un oscillogramme à deux capteurs | « Quel capteur reçoit le signal en premier ? » | TOP série (vG-rfo1TLAA) [17:30] |
| Après un calcul de v | « 333 au lieu de 340, est-ce grave ? » Réponse : non, c'est une valeur approchée. | Laksabi (W9XwPFD0sMU) [1:37:30] « بارفوا تقدر تلقى 333.33 ... عادي جدا » |
| Après avoir isolé une grandeur | « Ton expression a un signe moins : est-elle positive ? Compare v_air et v_eau. » | Laksabi (W9XwPFD0sMU) [3:53:30–3:54:30] |
| Dimensions | QCM « l'onde le long de la corde est tridimensionnelle » : faux. | Laksabi (W9XwPFD0sMU) [31:30] |
| Retard sur vidéo | « Combien d'intervalles entre l'image 8 et l'image 12 ? » | Laksabi (W9XwPFD0sMU) [0:58:30] |

Les autres questions des extraits sont déjà dans la synthèse : « pourquoi j'ai multiplié par 10⁻² ? », « la Lune : pourquoi tu n'entends pas ? », les 3 questions de la définition, « فهمتي منين جات ».

## 4. Autres éléments pour imiter ces profs

- **Les hypothèses dites à voix haute** : « milieu homogène » (le même matériau partout) et « pas d'amortissement » (la hauteur ne diminue pas). Ce sont les conditions de y_M(t) = y_S(t − τ) et d'une célérité constante. AdrarPhysic (XLQdN4C9L5g) [16:30–18:30] : « ال بقى ذا الارتفاع ينقص ديك الساعه حاجه اخرى ». Maria (RrCM2o1dgC4) [19:00] : « non amorti ». **NOUVEAU**, au programme : l'énoncé dit souvent « on néglige l'amortissement ».
- **Une formulation correcte des facteurs de la célérité** chez AdrarPhysic [17:00–17:30] : la célérité ne dépend pas de la forme de la perturbation, mais de la nature du milieu (« الصلابه ... القصور ... درجه الحراره »). **AFFINE** `a_ne_pas_dire` (densité). **Contradiction interne à trancher** : la synthèse (§F, §H.3) recommande « rigidité et inertie », alors que la fiche JSON classe « rigidité » dans `exclus_hors_programme`. Perimetre ne cite que tension et masse linéique, profondeur et température. Le plus sûr est d'en rester à ces facteurs.
- **Le son « tridimensionnel » expliqué par l'expérience** : « je parle, celui d'à côté m'entend, celui d'en haut et celui d'en bas aussi ». Laksabi (W9XwPFD0sMU) [32:00] : « لي فجنبي كيسمعني لي فوق مني كيسمعني لي تحت مني ». **NOUVELLE analogie** pour `analogies_validees`, au programme.
- **Dire quand on dépasse le national** : Laksabi prévient que beaucoup des situations traitées ne sont jamais tombées, et qu'il prend le national « comme prétexte pour apprendre à réfléchir » ([3:57:30], [2:25:30]). Le tuteur doit faire de même : signaler qu'une variante est un entraînement et non un format du bac.
- **Calcul de tête comme vérification** : « si tu peux, calcule-le de tête » ([0:52:30]). C'est mineur.

## 5. Affirmations des profs à ne pas reprendre (nouvelles)

- **Le point « sort du seau »** et la dimension définie par le mouvement du point (Laksabi, W9XwPFD0sMU [30:00–31:00]) : faux, voir 1.2.
- **« √(T/μ) et μ = m/L tombent au national »** (Taousse, 27FyalYEXhg [35:30]) : les 10 nationaux dépouillés ne le confirment pas. Seule l'homogénéité de √(g·h) est tombée (2024 N). La formule de la corde reste fournie par l'énoncé.
- **L'exemple Sciences Maths 2016** présenté au milieu des nationaux PC (Laksabi [3:55:00]) : ne pas le citer comme un « national ».
- **L'analogie des fuseaux horaires** pour y_M(t + τ) (TOP cours, YCzE0EZvsC8 [24:30]) : elle est confuse dans la transcription et ne vaut pas la peine d'être reprise ; « qui est atteint en premier ? » suffit.

## 6. Ce que le matériau n'apporte pas

Il n'apporte rien de neuf sur l'écho, le front, le barème en 4 éléments, l'algèbre 1/v, les conversions de base ou les valeurs repères : tout cela est déjà dans la fiche. Il n'apporte rien non plus d'exploitable sur les ultrasons ou le sonar au-delà de l'écho. Les extraits « Noureddine en classe » et « Maria » sont presque illisibles.
