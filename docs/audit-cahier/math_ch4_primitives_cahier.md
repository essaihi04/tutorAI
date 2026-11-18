# Cahier de l'élève — Fonctions primitives (`math_ch4_primitives`)

18 novembre 2026. Le cahier idéal du chapitre, d'un seul tenant, tel que l'élève le recopie bloc après bloc. Les titres
de parties (I. à IX.) sont ceux des `activities[].title` : le lecteur (`TableauCahier`) les affiche lui-même en tête du
bloc qui ouvre la partie ; les lignes du cahier portent donc la numérotation à l'intérieur de la partie (1., 2., …) et ne
répètent le chiffre romain que lorsqu'un bloc change de partie en cours de route (« IV. 1. », « V. Rappel », « VI. 1. »,
« VII. 1. »). Notation : « f → F » se lit « une primitive de f est F » ; k ∈ ℝ partout. Pas de ln, pas d'exp, pas
d'intégrale : le cours ne les enseigne pas (seulement annoncés en `pr_x4`, `pr_c8`).

---

**Fonctions primitives**

## Ouverture — dériver, puis revenir

- Primitiver : on part de f et on cherche F telle que F′ = f (la dérivation à l'envers).
- Rappel 1 : f′(a) est la pente de la tangente à (C_f) au point d'abscisse a ; (k)′ = 0 (k ∈ ℝ).
- Rappel 2 : (xⁿ)′ = n·xⁿ⁻¹ (n ∈ ℕ*). Exemple : (x³)′ = 3x².
- Rappel 3 : 1/xⁿ = x⁻ⁿ ; √x = x^(1/2) ; ∛x = x^(1/3) ; d'où (1/x)′ = −1/x² (x ≠ 0), (√x)′ = 1/(2√x) (x > 0).
- Rappel 4 : (sin x)′ = cos x ; (cos x)′ = −sin x.
- Rappel 5 : (uv)′ = u′v + uv′ ; jamais facteur par facteur.

(Le cours en ligne donne ces rappels en tête, numérotés 1 à 6 ; la copie en attente les place juste avant leur usage,
numérotés 1 à 5.)

## I. Définition et vérification

**1. Définition** : F est une primitive de f sur l'intervalle I si F est dérivable sur I et si F′(x) = f(x) pour tout
x ∈ I. Exemple : x² est une primitive de 2x sur ℝ.
Attention : on écrit F′ = f, jamais f = F (deux fonctions différentes).

**2. Méthode 1 — vérifier que F est une primitive de f sur I** (11 sujets nationaux sur 20)
1) F est dérivable sur I (somme, produit… de fonctions dérivables) ;
2) pour tout x ∈ I, F′(x) = … = f(x) ;
3) donc F est une primitive de f sur I (ne pas oublier l'intervalle).
Si F = uv : écrire u, u′, v, v′ à part. Exemple : (x sin x)′ = sin x + x cos x : x sin x est une primitive de
sin x + x cos x sur ℝ.

## II. Existence, famille F + k et condition

**1. Théorème (admis)** : toute fonction continue sur un intervalle I admet des primitives sur I.
Méthode 2 — rédiger : « f est continue sur I (raison), donc f admet des primitives sur I ».
Attention : toujours sur un intervalle ; ℝ* n'en est pas un : on travaille sur ]−∞ ; 0[ ou sur ]0 ; +∞[.
Exemple : (x²)′ = (x² + 10)′ = 2x : 2x a une infinité de primitives.

**2. Propriété (ensemble des primitives)** : si F est une primitive de f sur I, les primitives de f sur I sont les
fonctions x ↦ F(x) + k, k ∈ ℝ (au bac on écrit aussi F(x) + C, C ∈ ℝ).
Preuve : (F + k)′ = f ; si G′ = f, alors (G − F)′ = 0 sur l'intervalle I, donc G − F = k.
Remarque : les courbes des primitives se déduisent l'une de l'autre par translation verticale ; au même x, même pente f(x).
*Figure : les primitives x² + k de 2x (k = −1, 0, 2) et leurs tangentes parallèles en x = 1.*

**3. Propriété (unicité avec une condition)** : pour x₀ ∈ I et y₀ ∈ ℝ, une seule primitive F de f sur I vérifie F(x₀) = y₀.
Méthode 3 : 1) F(x) = G(x) + k ; 2) F(x₀) = y₀ ⇔ G(x₀) + k = y₀ ⇔ k = y₀ − G(x₀) ; 3) écrire F(x) complète.
Exemple : f(x) = 2x, F(1) = 3 : 1 + k = 3, k = 2, F(x) = x² + 2.
Attention : k n'est pas y₀ ; on calcule G(x₀) terme par terme.
*Figure : parmi les x² + k, une seule passe par A(1 ; 3).*

## III. Le tableau des primitives usuelles

Le tableau des dérivées lu à l'envers : (x⁴)′ = 4x³, donc 4x³ → x⁴. Toutes les primitives = celle du tableau + k.

| f(x) | une primitive F(x) | sur |
|---|---|---|
| 1. a (a ∈ ℝ) | ax | ℝ |
| xⁿ (n ∈ ℕ*) | xⁿ⁺¹/(n + 1) | ℝ |
| 2. αf (α ∈ ℝ) | αF : le coefficient reste devant (2x³ → x⁴/2) | I |
| 3. 1/x² | −1/x | ]−∞ ; 0[ ou ]0 ; +∞[ |
| 1/xⁿ (n ≥ 2) | −1/((n − 1)xⁿ⁻¹) | ]−∞ ; 0[ ou ]0 ; +∞[ |
| 4. 1/√x | 2√x | ]0 ; +∞[ |
| 5. xʳ (r ∈ ℚ*, r ≠ −1) | xʳ⁺¹/(r + 1) | ]0 ; +∞[ |
| 6. cos x ; sin x | sin x ; −cos x | ℝ |
| 7. cos(ax + b) ; sin(ax + b) (a ≠ 0) | (1/a)sin(ax + b) ; −(1/a)cos(ax + b) | ℝ |
| 8. 1 + tan²x = 1/cos²x (pour mémoire) | tan x | ]−π/2 ; π/2[ |

Attention : 1/x² ↛ 1/x³ (ça, c'est dériver) ; 1/√x → 2√x (ne pas oublier le 2) ; sin x → −cos x (le signe) ;
cos(2x − 1) → ½ sin(2x − 1) (diviser par a, le nombre collé à x). On vérifie toujours en dérivant.
*Figure : le cercle sin / cos / −sin / −cos (dériver dans un sens, primitiver dans l'autre).*

## IV. Somme, produit, transformer l'écriture

**1. Linéarité** : si F et G sont des primitives de f et g sur I, et α ∈ ℝ, alors F + G est une primitive de f + g et αF
une primitive de αf sur I ; une seule constante k à la fin.
Exemple : les primitives de 5x⁴ + 3x + 1 sur ℝ sont les fonctions x ↦ x⁵ + (3/2)x² + x + k, k ∈ ℝ.
**2. Attention** : pas facteur par facteur : ((x²/2)·sin x)′ = x sin x + (x²/2)cos x ≠ x cos x.
**3. Hors du tableau** : transformer l'écriture (séparer, développer, puissance).
Exemple : (x² + 1)/x² = 1 + 1/x² → x − 1/x + k, k ∈ ℝ, sur ]0 ; +∞[.

## V. Les formes composées (u dérivable sur I)

Rappel : (uⁿ)′ = n·u′·uⁿ⁻¹ ; ((x² + 1)³)′ = 6x(x² + 1)².
**1. Forme u′uⁿ (n ∈ ℕ*)** : u′uⁿ → uⁿ⁺¹/(n + 1), car (uⁿ⁺¹)′ = (n + 1)u′uⁿ.
Méthode 4 : 1) souligner u ; 2) bulle : u′ ; 3) écrire f = u′uⁿ ; 4) F = uⁿ⁺¹/(n + 1).
Exemple : (2x + 1)(x² + x − 4)³ = u′u³ (u = x² + x − 4) → (x² + x − 4)⁴/4.
**2. Il manque un nombre a** : f = (1/a) × u′uⁿ, on garde 1/a devant jusqu'à F.
Exemple : (x + 1)(x² + 2x − 6)² = ½(x² + 2x − 6)′(x² + 2x − 6)² → (1/6)(x² + 2x − 6)³.
Attention : on ne prête qu'un nombre ; s'il manque x, ce n'est pas la forme u′uⁿ.
**3. (ax + b)ⁿ → (ax + b)ⁿ⁺¹/(a(n + 1))** (a ≠ 0). Exemple : (2x − 1)³ → (2x − 1)⁴/8.
**4. u′uʳ → uʳ⁺¹/(r + 1)** (r ∈ ℚ*, r ≠ −1), avec u > 0 sur I. Exemple : 6x·∛(3x² + 1) → (3/4)(3x² + 1)^(4/3).
**5. u′/u² → −1/u** et **u′/uⁿ → −1/((n − 1)uⁿ⁻¹)** (n ≥ 2), avec u ≠ 0 sur I (c'est u′uᵐ avec m = −n entier, m ≠ −1).
Exemple : x/(x² + 1)² = ½(x² + 1)′/(x² + 1)² → −1/(2(x² + 1)), sur ℝ car x² + 1 ≠ 0.
**6. u′/√u → 2√u**, avec u > 0 sur I. Exemple : x/√(x² + 1) → √(x² + 1), sur ℝ.
Attention : le dénominateur choisit la forme : u² → −1/u ; √u → 2√u ; u seul : aucune des deux.
**7. u′·cos u → sin u ; u′·sin u → −cos u.** Exemple : πx·cos(πx² + 3) = ½(πx² + 3)′cos(πx² + 3) → ½ sin(πx² + 3).

## VI. Reconnaître une dérivée ; choisir la méthode

**1. u′v + uv′ → uv.** Exemple : sin x + x cos x = (x)′·sin x + x·(sin x)′ : primitives x ↦ x sin x + k, k ∈ ℝ.
**2. (u′v − uv′)/v² → u/v** (v ≠ 0 sur I). Exemple : (x² + 2x)/(x + 1)² → x²/(x + 1) sur ]−1 ; +∞[ (deux
primitives trouvées autrement diffèrent d'une constante).
**3. Méthode 5 — choisir** : 1) somme de fonctions du tableau → linéarité ; 2) u′ à un nombre près → la forme ;
3) u′v + uv′ → uv, (u′v − uv′)/v² → u/v ; 4) sinon, transformer l'écriture.

## VII. La courbe de f est la pente de F

**1.** F′ = f : f(a) est la pente de la tangente à (C_F) au point d'abscisse a ; f(a) = 0 ⇒ tangente horizontale.
*Figure : F(x) = x³/3 − x et f(x) = x² − 1, tangentes horizontales en −1 et 1.*
**2.** f ≥ 0 sur I ⇒ F croissante sur I ; f ≤ 0 sur I ⇒ F décroissante sur I (on étudie le signe de f, pas celui de F).
*Figure (cours en ligne) : tableau de variations de F(x) = x³/3 − x à partir du signe de f(x) = x² − 1.*
Méthode 6 (copie en attente, `pr_g3`) : signe de f = F′, puis les flèches de F. Exemple : f(x) = 3 − x : F croît sur
]−∞ ; 3], décroît sur [3 ; +∞[, maximum en 3.
*Figure (copie en attente) : tableau de variations de F, primitive de 3 − x.*

## VIII. Exercices type national (rédaction attendue)

1. Vérifier : H(x) = (x² + 1)√x est dérivable sur ]0 ; +∞[ (produit) ;
   H′(x) = 2x√x + (x² + 1)/(2√x) = (4x² + x² + 1)/(2√x) = (5x² + 1)/(2√x) = h(x) ; donc H est une primitive de h sur ]0 ; +∞[.
2. Forme puis condition : (2x + 1)(x² + x + 1)² = u′u² → F(x) = (x² + x + 1)³/3 + k ; F(0) = 1 ⇔ 1/3 + k = 1 ⇔ k = 2/3 ;
   F(x) = (x² + x + 1)³/3 + 2/3.
3. Existence, somme, condition : f(x) = x/(x² + 1)² + cos(2x) est continue sur ℝ (x² + 1 ≠ 0), donc admet des primitives ;
   F(x) = −1/(2(x² + 1)) + ½ sin(2x) + k (une seule constante) ; F(0) = 0 ⇔ −1/2 + k = 0 ⇔ k = 1/2.

## IX. Bilan et carte du chapitre

Fiche (sur un intervalle I, k ∈ ℝ) : vérifier = dériver ; f continue sur I ⇒ primitives ; toutes : F(x) + k ;
F(x₀) = y₀ donne k ; somme : une seule k.
xⁿ → xⁿ⁺¹/(n + 1) (n ∈ ℕ*) ; 1/xⁿ → −1/((n − 1)xⁿ⁻¹) (n ≥ 2, x ≠ 0) ; 1/√x → 2√x (x > 0) ;
cos(ax + b) → (1/a)sin(ax + b) ; sin(ax + b) → −(1/a)cos(ax + b) (a ≠ 0) ;
u′uⁿ → uⁿ⁺¹/(n + 1) (n ≠ −1) ; u′/u² → −1/u (u ≠ 0) ; u′/√u → 2√u (u > 0) ;
u′cos u → sin u ; u′sin u → −cos u ; u′v + uv′ → uv ; (u′v − uv′)/v² → u/v (v ≠ 0).

---
## Découpage

Script d'application (hors dépôt) : `/tmp/claude-0/-home-user-tutorAI/02f8f400-8fae-5359-a79d-1358639cc2d0/scratchpad/math_ch4_primitives/appliquer.py`. Bulles de diapositive : une chaîne d'une à deux lignes par diapositive (voir le script).

### Cours en ligne (`backend/data/courses/math_ch4_primitives.json`)

| Bloc | Diapositives | Lignes du cahier | Figures |
|---|---|---|---|
| `pr_s1_b1` | pr_o1, pr_z1_pente, pr_z2_puissances | 4 : Primitiver / Rappel 1 / Rappel 2 / Rappel 3 | — |
| `pr_s1_b1b` | pr_z3_ecrire, pr_z4_produit, pr_z5_cos_sin | 4 : Rappel 4 / D'où (1/x)′ = −1/x² (x ≠ 0)  / Rappel 5 / Rappel 6 | — |
| `pr_s1_b2` | pr_d1, pr_d2, pr_d3, pr_d4 | 6 : 1. Définition / et si F′(x) = f(x) pour tout / Attention / 2. Méthode 1 — vérifier / 3) donc F est une primitive  / Si F = uv | — |
| `pr_s1_b3` | pr_e1, pr_e2, pr_e3 | 4 : 1. Théorème (admis) / Méthode 2 — rédiger / Attention / Exemple | — |
| `pr_s2_b1` | pr_e4, pr_e4_b, pr_e5 | 4 : 2. Propriété / les fonctions x ↦ F(x) + k,  / Preuve / Remarque | Les primitives de 2x : x ↦ x² + k |
| `pr_s2_b1b` | pr_e6, pr_e7 | 4 : 3. Propriété / Méthode 3 / 3) écrire F(x) complète. Ex. / Attention | La primitive de 2x telle que F(1) = 3 |
| `pr_s2_b2` | pr_u1, pr_u2, pr_u3 | 4 : Dérivées lues à l'envers / 1. a → ax (a ∈ ℝ) ; xⁿ → xⁿ⁺ / 2. αf → αF / Remarque | — |
| `pr_s2_b3` | pr_u4, pr_u4_b | 3 : 3. 1/x² → −1/x, sur ]−∞ ; 0[ / 1/xⁿ → −1/((n − 1)xⁿ⁻¹) (n ≥ / Attention | — |
| `pr_s2_b3b` | pr_u5, pr_u5_b, pr_u6 | 4 : 4. 1/√x → 2√x sur ]0 ; +∞[,  / 5. xʳ → xʳ⁺¹/(r + 1) (r ∈ ℚ* / 6. cos x → sin x ; sin x → − / Attention au signe | Le cercle de sin et cos |
| `pr_s3_b1` | pr_u7, pr_u8, pr_l1 | 6 : 7. cos(ax + b) → (1/a)sin(ax / Ex. / 8. Pour mémoire / IV. 1. Linéarité / F + G est une primitive de f / Ex. | — |
| `pr_s3_b2` | pr_l2, pr_l3, pr_c1 | 4 : 2. Attention / 3. Hors du tableau / Ex. / V. Rappel | — |
| `pr_s3_b2b` | pr_c1_b, pr_c2 | 3 : 1. Forme u′uⁿ (n ∈ ℕ*, u dér / Méthode 4 / Ex. | — |
| `pr_s3_b3` | pr_c3, pr_c3_b, pr_c4 | 4 : 2. S'il manque un nombre a / Ex. / Attention / 3. (ax + b)ⁿ → (ax + b)ⁿ⁺¹/( | — |
| `pr_s4_b1` | pr_c5, pr_c6, pr_c6_b, pr_c7 | 5 : 4. u′uʳ → uʳ⁺¹/(r + 1) (r ∈  / Ex. / 5. u′/u² → −1/u et u′/uⁿ → − / Ex. / 6. u′/√u → 2√u, avec u > 0 s | — |
| `pr_s4_b2` | pr_c8, pr_c9, pr_r1 | 4 : Attention / 7. u′·cos u → sin u ; u′·sin / VI. 1. Dérivée d'un produit  / Ex. | — |
| `pr_s4_b3` | pr_r2, pr_r3, pr_g1, pr_g2 | 5 : 2. (u′v − uv′)/v² → u/v (v ≠ / 3. Méthode 5 — choisir / 3) u′v + uv′ → uv, (u′v − uv / VII. 1. F′ = f / 2. f ≥ 0 sur I ⇒ F croissant | f donne la pente de F, Signe de f, variations de F |
| `pr_s5_b1` | pr_x1, pr_x2, pr_x3 | 5 : 1. Vérifier / H′(x) = 2x√x + (x² + 1)/(2√x / 2. (2x + 1)(x² + x + 1)² = u / 3. f(x) = x/(x² + 1)² + cos( / F(x) = −1/(2(x² + 1)) + ½ si | — |
| `pr_s5_b2` | pr_x4, pr_b1, pr_b2 | 6 : Fiche (sur un intervalle I,  / Toutes / xⁿ → xⁿ⁺¹/(n + 1) (n ∈ ℕ*) ; / cos(ax + b) → (1/a)sin(ax +  / u′uⁿ → uⁿ⁺¹/(n + 1) (n ≠ −1) / u′cos u → sin u ; u′sin u →  | — |

Figures de diapositive : `pr_e5` → Les primitives de 2x : x ↦ x² + k ; `pr_e6` → La primitive de 2x telle que F(1) = 3 ; `pr_u6` → Le cercle de sin et cos ; `pr_g1` → f donne la pente de F ; `pr_g2` → Signe de f, variations de F.

### Copie en attente (`backend/data/courses/en_attente/math_ch4_primitives.json`)

| Bloc | Diapositives | Lignes du cahier | Figures |
|---|---|---|---|
| `pr_s1_b1` | pr_o1, pr_z1_pente, pr_d1, pr_d2 | 5 : Primitiver / Rappel 1 / 1. Définition / et si F′(x) = f(x) pour tout / Attention | — |
| `pr_s1_b1b` | pr_z2_puissances, pr_z3_ecrire, pr_d3 | 4 : Rappel 2 / Rappel 3 / 2. Méthode 1 — vérifier / 3) donc F est une primitive  | — |
| `pr_s1_b2` | pr_z5_cos_sin, pr_z4_produit, pr_d4 | 4 : Rappel 4 / Rappel 5 / Si F = uv / Ex. | — |
| `pr_s1_b3` | pr_e1, pr_e2, pr_e3 | 4 : 1. Théorème (admis) / Méthode 2 — rédiger / Attention / Exemple | — |
| `pr_s2_b1` | pr_e4, pr_e4_b, pr_e5 | 4 : 2. Propriété / les fonctions x ↦ F(x) + k,  / Preuve / Remarque | Les primitives de 2x : x ↦ x² + k |
| `pr_s2_b1b` | pr_e6, pr_e7 | 4 : 3. Propriété / Méthode 3 / 3) écrire F(x) complète. Ex. / Attention | La primitive de 2x telle que F(1) = 3 |
| `pr_s2_b2` | pr_u1, pr_u2, pr_u3 | 4 : Dérivées lues à l'envers / 1. a → ax (a ∈ ℝ) ; xⁿ → xⁿ⁺ / 2. αf → αF / Remarque | — |
| `pr_s2_b3` | pr_u4, pr_u4_b | 3 : 3. 1/x² → −1/x, sur ]−∞ ; 0[ / 1/xⁿ → −1/((n − 1)xⁿ⁻¹) (n ≥ / Attention | — |
| `pr_s2_b3b` | pr_u5, pr_u5_b, pr_u6 | 4 : 4. 1/√x → 2√x sur ]0 ; +∞[,  / 5. xʳ → xʳ⁺¹/(r + 1) (r ∈ ℚ* / 6. cos x → sin x ; sin x → − / Attention au signe | Le cercle de sin et cos |
| `pr_s3_b1` | pr_u7, pr_u8, pr_l1 | 6 : 7. cos(ax + b) → (1/a)sin(ax / Ex. / 8. Pour mémoire / IV. 1. Linéarité / F + G est une primitive de f / Ex. | — |
| `pr_s3_b2` | pr_l2, pr_l3, pr_c1 | 4 : 2. Attention / 3. Hors du tableau / Ex. / V. Rappel | — |
| `pr_s3_b2b` | pr_c1_b, pr_c2 | 3 : 1. Forme u′uⁿ (n ∈ ℕ*, u dér / Méthode 4 / Ex. | — |
| `pr_s3_b3` | pr_c3, pr_c3_b, pr_c4 | 4 : 2. S'il manque un nombre a / Ex. / Attention / 3. (ax + b)ⁿ → (ax + b)ⁿ⁺¹/( | — |
| `pr_s4_b1` | pr_c5, pr_c6, pr_c6_b, pr_c7 | 5 : 4. u′uʳ → uʳ⁺¹/(r + 1) (r ∈  / Ex. / 5. u′/u² → −1/u et u′/uⁿ → − / Ex. / 6. u′/√u → 2√u, avec u > 0 s | — |
| `pr_s4_b2` | pr_c8, pr_c9, pr_r1 | 4 : Attention / 7. u′·cos u → sin u ; u′·sin / VI. 1. Dérivée d'un produit  / Ex. | — |
| `pr_s4_b3` | pr_r2, pr_r3, pr_g1, pr_g2, pr_g3 | 6 : 2. (u′v − uv′)/v² → u/v (v ≠ / 3. Méthode 5 — choisir / 3) u′v + uv′ → uv, (u′v − uv / VII. 1. F′ = f / 2. f ≥ 0 sur I ⇒ F croissant / Méthode 6 | f donne la pente de F, F, primitive de f(x) = 3 − x |
| `pr_s5_b1` | pr_x1, pr_x1_b, pr_x2, pr_x2_b, pr_x3, pr_x3_b | 5 : 1. Vérifier / H′(x) = 2x√x + (x² + 1)/(2√x / 2. (2x + 1)(x² + x + 1)² = u / 3. f(x) = x/(x² + 1)² + cos( / F(x) = −1/(2(x² + 1)) + ½ si | — |
| `pr_s5_b2` | pr_x4, pr_b1, pr_b2 | 6 : Fiche (sur un intervalle I,  / Toutes / xⁿ → xⁿ⁺¹/(n + 1) (n ∈ ℕ*) ; / cos(ax + b) → (1/a)sin(ax +  / u′uⁿ → uⁿ⁺¹/(n + 1) (n ≠ −1) / u′cos u → sin u ; u′sin u →  | — |

Figures de diapositive : `pr_e5` → Les primitives de 2x : x ↦ x² + k ; `pr_e6` → La primitive de 2x telle que F(1) = 3 ; `pr_u6` → Le cercle de sin et cos ; `pr_g1` → f donne la pente de F ; `pr_g2` → Signe de f, variations de F ; `pr_g3` → F, primitive de f(x) = 3 − x.

