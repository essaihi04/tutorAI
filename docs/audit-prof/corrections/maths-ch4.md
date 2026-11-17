## Primitives

Copie en attente : `backend/data/courses/en_attente/math_ch4_primitives.json` (aucune copie en attente avant : partie du cours en ligne). Cours en ligne non touché.

### Manques corrigés

| Constat | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Fiche : « + C » sur chaque primitive (haute, confirmé) | Chaque formule de la fiche porte « + k (k ∈ ℝ) » ; rappel « f → F se lit : une primitive de f est F » | pr_b1 (bullets 4 à 7, cahier, student_trace), bloc pr_s5_b2 (cahier) |
| Fiche : intervalle et condition par ligne (haute ; propre au Prof Fayssal, gardé car sans condition xʳ et u′/√u sont faux, et la règle 38 l'exige) | ℝ, ]0 ; +∞[ ou ]−∞ ; 0[, ]−π/2 ; π/2[, u ≠ 0 sur I, u > 0 sur I, v ≠ 0 sur I, a ≠ 0, conditions sur n et r | pr_b1, bloc pr_s5_b2 |
| Fiche incomplète : xʳ, 1/xⁿ, sin(ax + b), 1 + tan²x, u′uʳ, (ax + b)ⁿ (haute, confirmé) | Toutes ces lignes ajoutées à la fiche, avec leur condition | pr_b1, bloc pr_s5_b2 |
| u′uⁿ avec n entier négatif et u′/uⁿ (moyenne, confirmé pour la formule) | Nouvelle diapo « u′/uⁿ : la règle générale » (u′/uⁿ = u′·u⁻ⁿ, règle −1/((n − 1)uⁿ⁻¹), n ≥ 2, u ≠ 0 sur I ; exemple 2x/(x² + 1)³ → −1/(2(x² + 1)²) ; 2e explication : vérification par la dérivée et cas u = x) ; fiche : u′uⁿ pour n ∈ ℤ, n ≠ −1 | pr_c6_b (nouvelle, bloc pr_s4_b1, K6), pr_b1 |
| Linéarité avec ses hypothèses « sur I » (moyenne, confirmé pour l'énoncé) | Énoncé complet à l'écran et au cahier (F, G primitives de f, g sur un même I, α ∈ ℝ) + « car (F + G)′ = F′ + G′ = f + g, (αF)′ = αF′ = αf » (règle 38) ; même énoncé dans la fiche | pr_l1 (bullets, cahier), bloc pr_s3_b1, pr_b1 point 5 |
| Constante notée aussi C (désaccord C : « dire une fois on la note aussi C ») | Une ligne à l'écran et au cahier | pr_e4_b, bloc pr_s2_b1 |
| Exemples travaillés qui sautaient une étape (règle 37 sur les diapos) | Étape intermédiaire écrite : ½ × (−1/(x² + 1)), u^(4/3)/(4/3), ½ × (2x − 1)⁴/4, (3/4)x^(4/3), u′v − uv′ = x² + 2x, 2x√x = 4x²/(2√x), F(0) calculé, pr_x3 mené jusqu'à F complète | pr_c6, pr_c5, pr_c4, pr_u5_b, pr_r2, pr_x1, pr_x2, pr_x3 (+ cahiers des blocs pr_s3_b3, pr_s4_b1, pr_s4_b3) |

### Non corrigés et pourquoi

- Exemple u = sin x (cos x·sin²x → (1/3)sin³x) et cos³x : propres au Prof Fayssal, non exigés par le cadre (1.2.14–1.2.15). À décider (forme utile pour les intégrales).
- Méthode « faire apparaître u au numérateur » (x/(x + 2)⁴) : propre au Prof Fayssal.
- Démonstration (F + G)′ en exemple séparé : seule la ligne « car » a été écrite (règle 38).
- Basses non confirmées : exemple u′u → u²/2, 1 + tan²x sur ]−π/2 + kπ ; π/2 + kπ[, remarque « forme explicite pas toujours connue ».
- Nouvelles pistes (aucune haute) : unicité F(x₀) = y₀ avec x₀ ∈ I, règle (1/a)F(ax + b), « continuité suffisante non nécessaire », u′ × (g′ ∘ u) : moyennes/basses, non faites.
- √x → (2/3)x√x à l'écran de pr_u5_b (signalé « à l'oral seulement ») : non confirmé, non fait.
- La simulation `primitives-tableau/bilan.html` (fiche à la craie de pr_b1) garde les anciennes formules sans + k ni condition : fichier frontend, non modifié. À mettre à jour (blocs « tableau » et « formes ») pour que la fiche dessinée suive le cahier.
- Voix de pr_b1, pr_l1, pr_e4_b non changées : l'écran ajoute des conditions mais ne contredit pas la voix.
- Les réactions préparées (`ecrit`/`parole`) n'ont pas été relues pour la règle 37.

### Démonstrations

- Relues : 59 (questions, exercices de diapo, exercices de fin de cours, exercices de bloc).
- Réécrites : 22 (16 textes différents ; 6 sont des copies de bloc). Aucune ne dépasse 8 lignes ; toutes vérifiées avec sympy (la valeur trouvée est celle de `correct`).
- Exemples :
  - pr_e7 (k = 11/6) : « 7/6 + k = 3 ⇔ k = 11/6 » → primitive terme par terme, F(1) écrit, 2/3 + 1/2 = 4/6 + 3/6 = 7/6, 3 − 7/6 = 18/6 − 7/6 = 11/6, puis F complète (7 lignes).
  - pr_c6 efc (1/(3x − 2)²) : « Une primitive : −1/(3(3x − 2)) » → règle u′/u² → −1/u (u ≠ 0), puis (1/3) × (−1/(3x − 2)), puis −1/(3(3x − 2)).
  - pr_d3 efc (H = x² + 1/x) : « H′ ≠ h » → H dérivable car somme, (1/x)′ = −1/x², H′(1) = 1 et h(1) = 3, conclusion avec l'intervalle.

### Voix à enregistrer

- Diapo nouvelle : pr_c6_b (`speech_text.mixed`, sans audio). Aucune voix de diapo existante modifiée.
- Démonstrations (parole nouvelle, aucune n'avait d'audio) : pr_d3/efc[1], pr_d4/ex[0], pr_e1/efc[0], pr_e6/efc[0], pr_e7/question, pr_e7/ex[0], pr_u5/efc[1], pr_c5/efc[0], pr_c6/efc[0], pr_c9/efc[0], pr_r3/efc[0], pr_x1/efc[0], pr_x2/efc[0], pr_x2/efc[1], pr_x3/ex[0], blocs pr_s1_b3, pr_s2_b1b, pr_s2_b3, pr_s4_b1, pr_s4_b2, pr_s4_b3, pr_s5_b1 (exercice).
- Réactions : aucune nouvelle (pr_c6_b ne porte pas de question).

### Vérifications faites

- `json.load` : OK ; fins de ligne LF (0 CR) ; écrit avec `ensure_ascii=False, indent=2`.
- Chaque `mot` des 59 démonstrations trouvé dans sa parole, dans l'ordre, première occurrence à sa place ; pas de chiffre ni de symbole dans les paroles : 0 erreur.
- Chaque `mot` de pointage et de centre dans `speech_text.mixed` : 0 erreur.
- 54 diapos, chacune dans exactement un bloc ; toutes les competence_ids existent ; K6 contient pr_c6_b.
- `verifier_figures_cahier.py` : 3 figures, 0 erreur, 0 avertissement.
- sympy : toutes les formules ajoutées (u′/uⁿ pour n = 2 à 5, u′uⁿ pour n = −2 et −3, (ax + b)ⁿ, cos/sin(ax + b), tan, xʳ) et tous les calculs des démonstrations et des exemples : justes.
- Nouvelle diapo sans visuel (`kind: none`) : aucune vue existante ne montre u′/uⁿ ; seules les formules du centre s'écrivent.
