# Cinétique (suivi temporel, vitesse, t₁/₂) : ce que demandent les nationaux (2016-2025)

Source : `backend/data/exams/physique/<année>-<session>/` (exam.json = énoncé et corrigé ; extraction.json = texte du sujet
officiel et grille du barème ; assets/*.png = figures). 20 sessions relues (normale N et rattrapage R).
Lecture : questions et corrigés dans exam.json ; barème et texte officiel dans extraction.json quand exam.json est vide ou douteux ;
**chaque figure de suivi a été regardée** (assets) et les graduations relevées à l'œil (pixels → valeurs), puis
recalculées avec python (pentes, t₁/₂, vitesses, modèles qui passent par les points lus).
**Vidéos non auditées** (YouTube bloqué depuis le cloud).

À savoir avant de lire :
- 10 sessions sur 20 ont un exercice de suivi temporel : 2016 R, 2017 N, 2017 R, 2018 R, 2019 R, 2021 N, 2023 N, 2024 N, 2025 N, 2025 R.
  Rien en 2016 N, 2018 N, 2019 N, 2020 N et R, 2021 R, 2022 N et R, 2023 R, 2024 R.
- Méthodes de suivi au national : **conductimétrie** 3 fois (2016 R σ(t), 2018 R G(t), 2021 N σ(t)), toutes sur la saponification de
  l'éthanoate d'éthyle (ou de méthyle) par la soude ; **titrage** (dosage) 2 fois (2017 R après eau glacée, 2024 N vitamine C) ;
  courbe x(t) ou n(t) **donnée sans méthode** 5 fois (2017 N, 2019 R, 2023 N, 2025 N, 2025 R).
- **Aucun suivi par mesure de pression ni par volume de gaz** en 10 ans (recherche « manomètre », « pression du gaz », « P₀ » : 0 résultat ;
  les 2019 R aspirine + HCO₃⁻ dégagent CO₂ mais la courbe x(t) est donnée). La pression reste au programme (OP-PC-2007, perimetre.json).
- Réactions supports : saponification (2016 R, 2018 R, 2021 N, 2025 R), estérification (2017 N, 2017 R, 2023 N, 2025 N), aspirine + HCO₃⁻
  (2019 R), oxydation de la vitamine C par O₂ (2024 N). Les réactions du manuel (H₂O₂ + I⁻, S₂O₈²⁻ + I⁻…) ne tombent jamais :
  nos exemples A (titrage), B (conductimétrie), C (pression) servent à voir ; les nationaux n1…n8 servent à s'entraîner.
- Grille officielle (extraction.json 2024 N) : capacités citées « Connaître l'expression de la vitesse volumique de réaction »,
  « Déterminer graphiquement la valeur de la vitesse volumique », « Définir le temps de demi-réaction », « Déterminer le temps de
  demi-réaction graphiquement ou en exploitant des résultats expérimentaux », « Connaître l'influence de la concentration des réactifs et de
  la température sur la vitesse volumique », « Dresser le tableau d'avancement d'une réaction et l'exploiter », « Exploiter la courbe ou
  les résultats du dosage » ; et aussi « Interpréter l'influence … sur le nombre de **chocs efficaces** par unité de temps » (⚠ contredit
  perimetre.json qui met les chocs efficaces hors programme : décision à faire valider).

---

## 1. Par session

Barème = points du sujet officiel. « x » = avancement.

### 2016 R — saponification de l'éthanoate d'éthyle, conductimétrie σ(t) (partie II.2)
- Données : n₀(ester) = n₀(HO⁻) = n₀, c₀ = 10 mol·m⁻³, V ≈ V₀ = 10⁻⁴ m³ → n₀ = 10⁻³ mol = x_max. Relation donnée :
  x(t) = −6,3·10⁻³·σ(t) + 1,57·10⁻³ (σ en S·m⁻¹, x en mol). Figure σ(t) en **mS·m⁻¹** (250 → ≈ 90) avec tangente (T) à l'origine.
- Questions : 2.1 nom et formule de A⁻ (0,5) ; 2.2 tableau d'avancement (0,5) ; 2.3.1 σ₁/₂ quand x = x_max/2 (0,5) → 0,170 S·m⁻¹ ;
  2.3.2 t₁/₂ en minutes (0,5) → ≈ 17 min ; 2.3.3 v(0) en mol·m⁻³·min⁻¹ (0,5) → tangente (0 ; 0,250) et (18 ; 0,100) :
  dσ/dt = −8,33·10⁻³ S·m⁻¹·min⁻¹ ; dx/dt = 6,3·10⁻³ × 8,33·10⁻³ = 5,25·10⁻⁵ mol·min⁻¹ ; v(0) = 5,25·10⁻⁵/10⁻⁴ = **0,525 mol·m⁻³·min⁻¹**.
  (Partie II.1 : rôle de H₂SO₄, « lente et limitée », K : autres chapitres.)
- Pièges : σ lue en **mS·m⁻¹** sur la figure, à passer en S·m⁻¹ dans la relation ; V en **m³** ici (unité demandée mol·m⁻³·min⁻¹) ;
  la pente est négative (σ baisse) mais v est positive.
- Dépôt : corrigé juste. Données générales : « Cℓ₂/Cℓ » sans le signe − (déjà relevé).

### 2017 N — acide butanoïque + éthanol (1) et anhydride butanoïque + éthanol (2), courbes x(t) (partie 2)
- Figure : x (mol) 0 → 0,3 (pas 0,1), t (min) 0 → 60 (pas 20) ; courbe (1) palier 0,2 mol, courbe (2) palier 0,3 mol ; x_max = 0,3 mol.
- Questions : 2.1 intérêt du chauffage à reflux (0,5) ; 2.2 t₁/₂ de chaque expérience, la plus rapide (0,75) → 8 min et 2 min, (2) plus rapide ;
  2.3 taux d'avancement final (0,75) → 0,67 et 1 (chapitre suivant).
- Piège : t₁/₂ se lit à **x_f/2 de chaque courbe** (0,1 mol pour (1), 0,15 mol pour (2)), pas à x_max/2 = 0,15 pour les deux.
- Dépôt : description de la figure fausse (« courbe (2) constante »), réponses justes.

### 2017 R — estérification acide éthanoïque + éthanol, tubes scellés à 100 °C, dosage de l'acide restant après eau glacée (partie II)
- Données (corrigé du sujet) : n₀(acide) = n₀(éthanol) = 0,6 mol ; figure n(acide) (mol) en fonction de t (h), 0 → 200 h, palier 0,2 mol.
- Questions (barème officiel, voir 4) : 1 rôle de l'eau glacée (**0,25**) → bloquer la réaction (trempe) avant le dosage ; 3 mélange
  équimolaire (0,5) ; 5 composition à l'équilibre (1) → n_f = 0,2 mol → x_f = 0,4 mol ; K = 4 (0,5).
- Piège : la courbe est celle d'un **réactif** (elle descend) : x = n₀ − n(acide).
- Dépôt : énoncé et barème faux dans exam.json (déjà relevé au chapitre précédent) ; **l'image assets/figcidessousp3.png part vers
  0,5 mol au lieu de 0,6** (haut coupé ?) — à revoir sur pages/ avant de dessiner.

### 2018 R — hydrolyse basique (saponification) de l'éthanoate de méthyle, conductance G(t) (partie II.2)
- Données : C₀ = 10⁻² mol·L⁻¹, V₀ = 0,1 L → x_max = 10⁻³ mol ; relation donnée x(t) = −6,3·10⁻²·G(t) + 1,57·10⁻³ (G en S) ;
  figure G (mS) 25 → ≈ 9, t (min) 0 → 65.
- Questions : 2.2.1 G₁/₂ (0,75) → (1,57·10⁻³ − 5·10⁻⁴)/6,3·10⁻² = 0,017 S = 17 mS ; 2.2.2 t₁/₂ en minutes (0,5) → ≈ 17 min.
- Piège : G lue en **mS** sur la figure, relation en S ; ne pas confondre G (en S) et σ (en S·m⁻¹) : G = k·σ.
- Dépôt : expérience II.1 absente, montage du reflux faux (déjà relevé).

### 2019 R — aspirine C₉H₈O₄ + HCO₃⁻ → C₉H₇O₄⁻ + CO₂ + H₂O, courbe x(t) (partie 2)
- Données : n₀(aspirine) = 2,8 mmol, n₀(HCO₃⁻) = 5 mmol, V = 10 mL ; figure x (mmol) 0 → 3 (pas 1), t (s) 0 → 500 (pas 100),
  tangente (T) à t = 100 s passant par (0 ; 0,75) et (75 ; 1,5).
- Questions : 2 tableau d'avancement (0,5) ; 3 x_max (0,5) → 2,8 mmol (aspirine limitante) ; 4 v à t = 100 s en mol·L⁻¹·s⁻¹ (0,75)
  → pente (1,5 − 0,75)/75 = 0,01 mmol·s⁻¹ ; v = 0,01·10⁻³/10·10⁻³ = **1,0·10⁻³ mol·L⁻¹·s⁻¹** ; 5 t₁/₂ (0,75) → x = 1,4 mmol → **70 s**.
- Pièges : V = 10 mL = 10·10⁻³ L ; mmol → mol ; le temps est en **secondes** ; deux hypothèses pour le limitant.
- Dépôt : titre « Partie 2 » collé à la question de pile (déjà relevé). Corrigé juste.

### 2021 N — saponification de l'éthanoate d'éthyle, conductimétrie σ(t) (partie 1)
- Données : ester en excès, n₀(HO⁻) = 10⁻³ mol, V₀ = 100 mL ; relation donnée σ = 0,25 − 160·x (σ en S·m⁻¹, x en mol) ;
  figure σ (S·m⁻¹) 0 → 0,25 (pas 0,05), t (min) 0 → 24 (pas 4), tangente (T) à t₁ = 4 min.
- Questions : 1 tableau et x_f (0,75) → x_f = x_max = 10⁻³ mol (réaction totale) ; 2.1 définir t₁/₂ (0,25) ; 2.2 t₁/₂ (0,25) →
  σ₁/₂ = 0,25 − 160 × 5·10⁻⁴ = 0,17 S·m⁻¹ → **4 min** ; 2.3 montrer v = −(1/(160·V₀))·dσ/dt (0,75) ; 2.4 v₁ en mol·m⁻³·min⁻¹ (0,75)
  → tangente (0 ; 0,22) et (4 ; 0,17) : pente −0,0125 ; v₁ = 0,0125/(160 × 10⁻⁴) = **0,78 mol·m⁻³·min⁻¹**.
- Pièges : V₀ en **m³** (10⁻⁴) ; le signe − de la relation ; « montrer » = dériver la relation donnée puis remplacer dans v = (1/V)·dx/dt.
- Dépôt : « Partie 2 » collé à la question 2.1 (déjà relevé) ; les numéros 2.1-2.4 de la cinétique sont ceux de la partie 1.

### 2023 N — estérification acide éthanoïque + méthanol, n_A(t) avec et sans catalyseur (partie 3)
- Données : n₀(acide) = n₀(méthanol) = 0,9 mol ; figure n_A (mol) 0 → 0,9 (pas 0,2), t (h) 0 → 30 (pas 5), courbes C₁ et C₂, palier 0,3 mol.
- Questions : 3.2 courbe avec catalyseur (0,5) → C₁ (palier atteint plus tôt) ; 3.3 composition à l'équilibre (0,5) → x_f = 0,6 mol ;
  3.4 t₁/₂ de C₂ (0,5) → n_A = 0,9 − 0,6/2 = **0,6 mol** → **3,5 h** ; 3.5 rendement (0,75) → 67 %.
- Piège : la courbe est n(réactif) : à t₁/₂, n_A = n₀ − x_f/2 = 0,6 mol, **pas** 0,45 (moitié de n₀) ni 0,3.
- Dépôt : description de la figure fausse (« vers zéro ») ; corrigé juste.

### 2024 N — oxydation de la vitamine C d'un jus d'orange par O₂, suivi par dosage, x(t) en heures (partie 1)
- Données (extraction.json) : V = 200 mL ; figure x (mmol) 0 → 0,5 (pas 0,1), t (h) 0 → 200 (pas 40), tangente (T) à t₁ = 60 h.
- Questions : 1 vrai/faux (0,75 = 3 × 0,25) : a concentration initiale = facteur cinétique (vrai) ; b « toujours terminée au bout de
  2·t₁/₂ » (**faux**) ; c chocs efficaces (vrai) ; 2 t₁/₂ (0,5) → **24 h** ; 3 v(t₁) en mmol·L⁻¹·h⁻¹ (1) → **1,25·10⁻² mmol·L⁻¹·h⁻¹**.
- Vérification : pente de (T) lue (0 ; 0,25) → (60 ; 0,40) : 2,5·10⁻³ mmol·h⁻¹ ; /0,200 L = 1,25·10⁻² ✓ ; x_f ≈ 0,5 mmol, x_f/2 = 0,25 → 24 h ✓.
- Pièges : temps en **heures** ; V = 0,200 L ; à 2·t₁/₂ = 48 h, x ≈ 0,38 mmol, pas fini.
- Dépôt : **corrigés vides** (« Démarche ; t₁/₂ = 24 h »), items 1.a-c sans id, et **V = 200 mL et t₁ = 60 h absents d'exam.json**
  (seulement dans extraction.json) : sans eux la question 3 est impossible.

### 2025 N — estérification acide éthanoïque + propan-1-ol, trois expériences, x(t) (partie 2)
- Données : 0,200 mol + 0,200 mol ; exp. 1 à θ₁, exp. 2 à θ₂ > θ₁, exp. 3 à θ₂ + H₂SO₄ ; figure x (mmol) 0 → ≈ 140 (graduations 26,6 et 53,2),
  t (min) 0 → ≈ 430 (pas 30) ; courbes (a), (b), (c).
- Questions : 2.2 courbe de l'exp. 3 (0,5) → (a) ; 2.3 vrai/faux « x_f le même » (0,75) → vrai ; 2.4 t₁/₂ de l'exp. 2 (0,75) →
  x_f = 133 mmol, x_f/2 = 66,5 mmol → **90 min** sur (b) ; 2.5 rendement exp. 3 (0,5) → 133/200 = 66,5 %.
- Pièges : l'exp. 2 est la courbe (b) (pas la plus lente) ; x_f se lit sur (a) qui a atteint son palier (même x_f pour toutes) ;
  graduation 26,6 = x_f/5.

### 2025 R — saponification de l'éthanoate d'éthyle, x(t) (partie 3)
- Données : V = 50 mL ; x_f = x_max = 0,8 mmol ; figure x (mmol) 0 → 0,6 (pas 0,10), t (min) 0 → 8 (pas 1), tangente (T) au point × de t = 3 min.
- Questions : 3.1 équation (0,5) ; 3.2 vrai/faux justifié « v diminue au cours du temps » (0,5) → vrai, la pente diminue ;
  3.3 t₁/₂ (0,5) → x = 0,4 mmol → **4 min** ; 3.4 v(3 min) en mmol·L⁻¹·min⁻¹ (0,75) → (T) par (0 ; 0,08) et (1 ; 0,16) :
  0,08 mmol·min⁻¹ ; v = 0,08/0,050 = **1,6 mmol·L⁻¹·min⁻¹**.
- Pièges : la figure s'arrête avant le palier (x_f est donné par le texte, réaction totale) ; V = 50 mL = 0,050 L.

---

## 2. Bilan des cas types (10 sessions)

| Cas type | Sessions | Points |
|---|---|---|
| Lire t₁/₂ sur x(t) (ou n(t), σ(t), G(t)) à x_f/2 | 2016 R, 2017 N, 2018 R, 2019 R, 2021 N, 2023 N, 2024 N, 2025 N, 2025 R (9 sessions) | 0,25-0,75 |
| Vitesse volumique par la tangente | 2016 R (t = 0), 2019 R, 2021 N, 2024 N, 2025 R (5 sessions) | 0,5-1 |
| Tableau d'avancement, x_max, limitant | 2016 R, 2019 R, 2021 N (3) | 0,5-0,75 |
| Relation σ(x) ou G(x) donnée : σ₁/₂, G₁/₂, ou montrer v en fonction de dσ/dt | 2016 R, 2018 R, 2021 N (3) | 0,5-0,75 |
| Composition / x_f lue sur le palier | 2017 R, 2023 N, 2025 N (3) | 0,5-1 |
| Courbe la plus rapide (t₁/₂ plus petit, catalyseur, température) | 2017 N, 2023 N, 2025 N (3) | 0,5-0,75 |
| Vrai/faux : v diminue / fini à 2·t₁/₂ / concentration facteur | 2024 N, 2025 R | 0,25-0,5 |
| Définir t₁/₂ | 2021 N | 0,25 |
| Trempe (eau glacée) | 2017 R | 0,25 |

Unités de vitesse demandées : mol·m⁻³·min⁻¹ (2016 R, 2021 N), mol·L⁻¹·s⁻¹ (2019 R), mmol·L⁻¹·h⁻¹ (2024 N), mmol·L⁻¹·min⁻¹ (2025 R).
Valeurs de t₁/₂ : 70 s, 2 min, 4 min (deux fois), 8 min, 17 min (deux fois), 90 min, 3,5 h, 24 h.

## 3. Pièges où l'élève perd des points
- V en mL dans v = (1/V)·dx/dt (5 sessions sur 5 ont V en mL dans l'énoncé) ; ou V en L quand l'unité demandée est en mol·m⁻³.
- Lire t₁/₂ à t_final/2 (milieu de l'axe des temps) au lieu de x_f/2 ; ou à x_max/2 quand x_f < x_max (2017 N, 2025 N).
- Sur une courbe de réactif (2017 R, 2023 N) ou de σ décroissante (2016 R, 2021 N), lire « la moitié de la valeur initiale ».
- Lire σ en mS·m⁻¹ ou G en mS et l'utiliser comme S·m⁻¹ ou S (2016 R, 2018 R).
- Prendre la pente de la corde (deux points de la courbe) au lieu de la tangente ; prendre deux points de la tangente trop proches.
- Oublier le signe : dσ/dt < 0 mais v > 0 (2016 R, 2021 N).
- Croire que la réaction est finie à 2·t₁/₂ (2024 N 1.b).
- Unité de temps du graphe (s, min, h) recopiée de travers.

## 4. Erreurs du dépôt (exam.json) qui touchent ce chapitre
1. **2024 N** : corrigés réduits à « Démarche ; t₁/₂ = 24 h », « Démarche v(t₁) = 1,25·10⁻² » ; V = 200 mL et t₁ = 60 h **absents** de
   l'énoncé d'exam.json (présents dans extraction.json) ; items 1.a-c sans id. Réponses V, F, V et valeurs justes (vérifiées sur la figure).
2. **2017 R** : énoncé et barème faux (eau glacée 0,25 et non 0,5 ; acide sulfurique, reflux inventés) ; figure du dépôt dont le haut
   paraît coupé (départ ≈ 0,5 mol au lieu de 0,6 mol).
3. **2018 R** : expérience II.1 absente ; montage du reflux (c) et non (a).
4. **2021 N** : titre « Partie 2 » collé à la question 2.1 (définir t₁/₂), qui est de la partie 1.
5. **2019 R** : titre « Partie 2 : acide acétylsalicylique » collé à une question de pile.
6. **Descriptions de figures fausses** : 2017 N (courbe (2) « constante »), 2023 N (« vers zéro »), 2021 N (« 0,1 S·m⁻¹ à environ
   12 minutes » : c'est 0,11). Les réponses n'en dépendent pas.

---

## 5. Figures pour figures.html

Lecture : graduations relevées sur assets/*.png ; « points » = valeurs (t ; y) qui permettent de tracer la courbe comme le sujet (lues sur
l'image à ± une demi-petite division, ou calculées par le modèle indiqué, qui passe par les valeurs du corrigé — le modèle sert au calcul,
il n'est jamais écrit à l'écran). Tangente = deux points donnés par le corrigé. Tous les nombres ont été recalculés avec python.

| Clé | Diapositive | Session | Méthode |
|---|---|---|---|
| fig_2016R | p4 | 2016 R | conductimétrie σ(t) |
| fig_2024N | p6 | 2024 N | titrage (dosage), vitamine C |
| fig_2019R | n1 | 2019 R | x(t), tangente, t₁/₂ |
| fig_2025R | n2 | 2025 R | x(t), v diminue, tangente |
| fig_2017N | n3 | 2017 N | deux x(t), t₁/₂ comparés |
| fig_2023N | n4 | 2023 N | n(réactif), catalyseur |
| fig_2025N | n5 | 2025 N | trois x(t), même x_f |
| fig_2021N | n6 | 2021 N | conductimétrie σ(t), tangente |
| fig_2018R | n7 | 2018 R | conductance G(t) |
| fig_2017R | n8 | 2017 R | titrage après trempe, n(acide) |

### fig_2016R (p4) — 2016 R, σ(t) d'une saponification
- Ordonnée : σ (mS·m⁻¹), 0 → 250, pas 50 (petites divisions 10). Abscisse : t (min), 0 → 65, graduations 15, 30 (petites divisions 2,5).
- Points lus : (0 ; 250) (5 ; 207) (10 ; 190) (15 ; 174) (20 ; 163) (30 ; 144) (45 ; 112) (60 ; 94) (63 ; 91). Asymptote ≈ 90 mS·m⁻¹.
- Tangente (T) à l'origine : (0 ; 250) et (18 ; 100) mS·m⁻¹ (tracée en pointillés jusqu'à ≈ (20 ; 84)).
- À lire : σ₁/₂ = 170 mS·m⁻¹ → t₁/₂ ≈ 17 min ; pente à l'origine −8,33 mS·m⁻¹·min⁻¹.
- Question posée (2.3.1-2.3.3, 0,5 + 0,5 + 0,5) : relation x = −6,3·10⁻³·σ + 1,57·10⁻³ ; calculer σ₁/₂, trouver t₁/₂, v(0) en mol·m⁻³·min⁻¹.
- Réponse au barème : σ₁/₂ = (1,57·10⁻³ − 5·10⁻⁴)/6,3·10⁻³ = 0,170 S·m⁻¹ ; t₁/₂ ≈ 17 min ;
  v(0) = (1/V)·(dx/dt)₀ = 6,3·10⁻³ × 8,33·10⁻³ / 10⁻⁴ = 0,525 mol·m⁻³·min⁻¹.

### fig_2024N (p6) — 2024 N, x(t) de l'oxydation de la vitamine C (suivi par dosage)
- Ordonnée : x (mmol), 0 → 0,55, pas 0,1 (petites divisions 0,02). Abscisse : t (h), 0 → 230, pas 40 (petites divisions 8).
- Modèle (passe par les valeurs du corrigé) : x = 0,5·(1 − e^(−t·ln2/24)). Points : (0 ; 0) (24 ; 0,25) (40 ; 0,343) (60 ; 0,412)
  (80 ; 0,450) (120 ; 0,484) (160 ; 0,495) (220 ; 0,499).
- Tangente (T) à t₁ = 60 h (point × sur la courbe) : (0 ; 0,25) et (60 ; 0,40) mmol (pente 2,5·10⁻³ mmol·h⁻¹ ; modèle : 2,55·10⁻³).
- À lire : x_f ≈ 0,5 mmol ; x_f/2 = 0,25 mmol → t₁/₂ = 24 h ; à 2·t₁/₂ = 48 h, x ≈ 0,38 mmol (pas fini).
- Question posée (1.b 0,25 ; 2 0,5 ; 3 1) : vrai/faux « terminée au bout de 2·t₁/₂ » ; t₁/₂ ; v(t₁) en mmol·L⁻¹·h⁻¹, V = 200 mL.
- Réponse au barème : faux ; t₁/₂ = 24 h ; v(t₁) = (1/V)·(Δx/Δt) = (0,40 − 0,25)/(60 × 0,200) = 1,25·10⁻² mmol·L⁻¹·h⁻¹.

### fig_2019R (n1) — 2019 R, aspirine + HCO₃⁻
- Ordonnée : x (mmol), 0 → 3, pas 1 (petites divisions 0,1). Abscisse : t (s), 0 → 500, pas 100 (petites divisions 10).
- Modèle : x = 2,8·(1 − e^(−t·ln2/70)). Points : (0 ; 0) (50 ; 1,09) (70 ; 1,40) (100 ; 1,76) (150 ; 2,17) (200 ; 2,41) (300 ; 2,66) (500 ; 2,78).
- Tangente (T) à t = 100 s : (0 ; 0,75) et (75 ; 1,5) mmol (pente 0,010 mmol·s⁻¹ ; modèle 0,0103).
- À lire : x_max = 2,8 mmol ; x = 1,4 mmol → t₁/₂ = 70 s.
- Question posée (3 0,5 ; 4 0,75 ; 5 0,75) : x_max (n₀ = 2,8 et 5 mmol) ; v à 100 s en mol·L⁻¹·s⁻¹ (V = 10 mL) ; t₁/₂.
- Réponse au barème : x_max = 2,8 mmol (aspirine limitante) ; v = (1/V)·(Δx/Δt) = 0,01·10⁻³/10·10⁻³ = 1,0·10⁻³ mol·L⁻¹·s⁻¹ ; t₁/₂ = 70 s.

### fig_2025R (n2) — 2025 R, saponification x(t)
- Ordonnée : x (mmol), 0 → 0,6, graduations 0,10 et 0,20 (petites divisions 0,02). Abscisse : t (min), 0 → 8, pas 1 (petites divisions 0,2).
- Modèle : x = 0,8·(1 − e^(−t·ln2/4)). Points : (0 ; 0) (1 ; 0,127) (2 ; 0,234) (3 ; 0,324) (4 ; 0,400) (6 ; 0,517) (8 ; 0,600).
  La figure s'arrête à 8 min, avant le palier (x_f = 0,8 mmol donné par le texte).
- Tangente (T) au point × (3 min ; 0,32) : (0 ; 0,08) et (1 ; 0,16) mmol (pente 0,08 mmol·min⁻¹ ; modèle 0,082).
- À lire : x_f/2 = 0,4 mmol → t₁/₂ = 4 min ; la pente diminue (v diminue).
- Question posée (3.2 0,5 ; 3.3 0,5 ; 3.4 0,75) : vrai/faux justifié « v diminue » ; t₁/₂ ; v(3 min) en mmol·L⁻¹·min⁻¹, V = 50 mL.
- Réponse au barème : vrai, la pente de la tangente à x(t) diminue ; t₁/₂ = 4 min ; v(3) = 0,08/0,050 = 1,6 mmol·L⁻¹·min⁻¹.

### fig_2017N (n3) — 2017 N, deux estérifications
- Ordonnée : x (mol), 0 → 0,35, pas 0,1 (petites divisions 0,01). Abscisse : t (min), 0 → 75, pas 20 (petites divisions 2).
- Modèles : (1) x = 0,2·(1 − e^(−t·ln2/8)) ; (2) x = 0,3·(1 − e^(−t·ln2/2)).
  Points (t ; x₁ ; x₂) : (0 ; 0 ; 0) (2 ; 0,032 ; 0,150) (5 ; 0,070 ; 0,247) (8 ; 0,100 ; 0,281) (10 ; 0,116 ; 0,291) (20 ; 0,165 ; 0,300)
  (40 ; 0,194 ; 0,300) (60 ; 0,199 ; 0,300).
- Pas de tangente.
- À lire : x_f(1) = 0,2 mol → x = 0,1 → t₁/₂ = 8 min ; x_f(2) = 0,3 mol → x = 0,15 → t₁/₂ = 2 min.
- Question posée (2.2, 0,75) : t₁/₂ de chaque expérience, la plus rapide.
- Réponse au barème : 8 min et 2 min ; l'expérience (2) (anhydride) est la plus rapide (t₁/₂ plus petit).

### fig_2023N (n4) — 2023 N, n(acide) avec et sans catalyseur
- Ordonnée : n_A (mol), 0 → 1,0, graduations 0,2 et 0,4 (petites divisions 0,02). Abscisse : t (h), 0 → 35, pas 5 (petites divisions 1).
- Modèles : C₁ n = 0,3 + 0,6·e^(−t·ln2/1,7) ; C₂ n = 0,3 + 0,6·e^(−t·ln2/3,5).
  Points (t ; C₁ ; C₂) : (0 ; 0,90 ; 0,90) (1 ; 0,70 ; 0,79) (1,7 ; 0,60 ; 0,73) (3,5 ; 0,44 ; 0,60) (5 ; 0,38 ; 0,52) (10 ; 0,31 ; 0,38)
  (20 ; 0,30 ; 0,31) (30 ; 0,30 ; 0,30).
- Pas de tangente.
- À lire : palier 0,3 mol → x_f = 0,6 mol ; sur C₂, n_A = 0,9 − 0,3 = 0,6 mol → t₁/₂ = 3,5 h.
- Question posée (3.2 0,5 ; 3.4 0,5) : courbe avec catalyseur ; t₁/₂ de C₂.
- Réponse au barème : C₁, elle atteint l'équilibre plus tôt (même palier) ; t₁/₂ ≈ 3,5 h.

### fig_2025N (n5) — 2025 N, trois estérifications
- Ordonnée : x (mmol), 0 → 140, graduations 26,6 et 53,2 (pas 26,6 = x_f/5 ; petites divisions 5,32). Abscisse : t (min), 0 → 430, pas 30
  (petites divisions 6).
- Modèles d'allure (approchés sur l'image) : (a) x = 133·t/(t + 40) ; (b) x = 133·t/(t + 90) ; (c) x = 133·t/(t + 190).
  Points (t ; a ; b ; c) : (0 ; 0 ; 0 ; 0) (30 ; 57 ; 33 ; 18) (60 ; 80 ; 53 ; 32) (90 ; 92 ; 66,5 ; 43) (150 ; 105 ; 83 ; 59) (240 ; 114 ; 97 ; 74)
  (330 ; 119 ; 105 ; 84) (420 ; 121 ; 110 ; 92). Sur l'image, (a) atteint ≈ 130 mmol vers 400 min : dessiner (a) avec un palier à 133.
- Pas de tangente.
- À lire : x_f = 133 mmol (même pour les trois) ; x_f/2 = 66,5 mmol → t₁/₂ (b) = 90 min.
- Question posée (2.2 0,5 ; 2.3 0,75 ; 2.4 0,75) : courbe de l'expérience 3 ; vrai/faux « x_f le même » ; t₁/₂ de l'expérience 2.
- Réponse au barème : (a) (température θ₂ et catalyseur : la plus rapide) ; vrai (mêmes quantités initiales, les facteurs cinétiques ne
  changent pas l'état final) ; t₁/₂ = 90 min.

### fig_2021N (n6) — 2021 N, σ(t) d'une saponification
- Ordonnée : σ (S·m⁻¹), 0 → 0,25, pas 0,05 (petites divisions 0,01). Abscisse : t (min), 0 → 26, pas 4 (petites divisions 0,8).
- Points lus (± 0,005) : (0 ; 0,250) (2 ; 0,200) (4 ; 0,170) (8 ; 0,130) (12 ; 0,110) (16 ; 0,100) (20 ; 0,095) (24 ; 0,093). Asymptote σ_f = 0,25 − 0,16 = 0,09.
- Tangente (T) à t₁ = 4 min : (0 ; 0,22) et (4 ; 0,17) S·m⁻¹ (pente −0,0125 S·m⁻¹·min⁻¹ ; coupe l'axe des t vers 17,6 min).
- À lire : σ₁/₂ = 0,25 − 160 × 5·10⁻⁴ = 0,17 S·m⁻¹ → t₁/₂ = 4 min.
- Question posée (2.2 0,25 ; 2.3 0,75 ; 2.4 0,75) : t₁/₂ ; montrer v = −(1/(160·V₀))·dσ/dt ; v₁ en mol·m⁻³·min⁻¹.
- Réponse au barème : t₁/₂ = 4 min ; dσ/dt = −160·dx/dt donc v = (1/V₀)·dx/dt = −(1/(160·V₀))·dσ/dt ;
  v₁ = 0,0125/(160 × 10⁻⁴) = 0,78 mol·m⁻³·min⁻¹.

### fig_2018R (n7) — 2018 R, G(t) d'une saponification
- Ordonnée : G (mS), 0 → 28, pas 5 (petites divisions 1). Abscisse : t (min), 0 → 65, graduations 15, 30 (petites divisions 1,5).
- Points lus : (0 ; 25,0) (5 ; 21,7) (10 ; 19,3) (15 ; 17,7) (20 ; 16,4) (30 ; 14,2) (45 ; 11,5) (60 ; 9,5) (64 ; 9,2).
- Pas de tangente.
- À lire : G₁/₂ = 17 mS → t₁/₂ ≈ 17 min.
- Question posée (2.2.1 0,75 ; 2.2.2 0,5) : relation x = −6,3·10⁻²·G + 1,57·10⁻³ ; G₁/₂ quand x = x_max/2 ; t₁/₂ en minutes.
- Réponse au barème : x_max = C₀·V₀ = 10⁻³ mol ; G₁/₂ = (1,57·10⁻³ − 5·10⁻⁴)/6,3·10⁻² = 0,017 S = 17 mS ; t₁/₂ ≈ 17 min.

### fig_2017R (n8) — 2017 R, n(acide) dosé après trempe
- Ordonnée : n (mol), 0 → 0,6, pas 0,2 (petites divisions 0,01). Abscisse : t (h), 0 → 200, pas 40 (petites divisions 4).
- Points (départ 0,6 mol d'après les données ; le reste lu sur l'image) : (0 ; 0,60) (10 ; 0,43) (20 ; 0,37) (40 ; 0,31) (80 ; 0,245)
  (120 ; 0,215) (160 ; 0,203) (200 ; 0,200). ⚠ l'image du dépôt part vers 0,5 mol : vérifier sur pages/ (sujet_p3) avant de dessiner.
- Pas de tangente.
- À lire : palier n_f = 0,2 mol → x_f = 0,6 − 0,2 = 0,4 mol.
- Question posée (1 0,25 ; 5 1) : rôle de l'eau glacée ; composition du mélange à l'équilibre.
- Réponse au barème : trempe — refroidir brusquement pour bloquer la réaction et doser l'acide présent à cette date ; acide 0,2 mol,
  alcool 0,2 mol, ester 0,4 mol, eau 0,4 mol.
