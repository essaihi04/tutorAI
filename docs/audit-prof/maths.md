# Audit des cours de maths face au cours d'un professeur (16 novembre 2026)

**Référence** : livre de cours du Prof Fayssal, 2e bac sciences BIOF (`backend/cours 2bac pc/Math/Livre-Cours-2BAC-SC-EXP.pdf`,
174 pages). Chaque manque a été vérifié dans nos cours (écran, cahier, voix, exercices) et confronté au cadre officiel de
l'examen (qui fait foi) : ce que le livre donne pour la série sciences maths (SM) est classé « hors cadre, ne pas ajouter ».
Rien de ce qui a été retiré exprès par l'audit officiel (`docs/audit-programme-officiel/maths.md` : dichotomie, suites
adjacentes, logarithme de base a…) n'est proposé. **Aucun cours n'a été modifié** : c'est un constat.

Dans le tableau qui suit, « PDF p. N » désigne la page du fichier PDF.

## Bilan

| Chapitre | Haute | Moyenne | Basse | Les manques principaux |
|---|---|---|---|---|
| ch1 Limites et continuité | 5 | 14 | 7 | continuité à droite / à gauche jamais écrite ; tableau des limites usuelles (xⁿ en −∞ selon la parité de n, 1/xⁿ, 1/x en 0⁺ / 0⁻) et règles « nombre × ∞ » ; « repère orthonormé » absent pour la symétrie de (C_f) et (C_f⁻¹) ; unicité de la solution de f(x) = k (on ne fait que k = 0) |
| ch2 Dérivation et étude | 3 | 12 | 8 | la raison de la dérivabilité n'est jamais écrite (« car c'est un polynôme », « car x² + 1 ≠ 0 ») ; définition de « dérivable sur ]a ; b[ / [a ; b] » ; phrase type « (C_f) coupe l'axe des abscisses en un point unique d'abscisse α » |
| ch3 Suites | 3 | 6 | 7 | montrer f(I) ⊂ I (f([a ; b]) = [f(a) ; f(b)]) ; « f est continue sur I **car** dérivable » ; deux solutions de f(x) = x dans I ; « n → +∞ » sous lim, « de raison q et de premier terme v₀ » |
| ch4 Primitives | 3 | 3 | 3 | la fiche à recopier `pr_b1` donne les formules **sans intervalle, sans condition (u > 0, u ≠ 0) et sans + k** ; des lignes oubliées dans cette fiche (xʳ, 1/xⁿ, sin(ax + b), 1 + tan², u′uʳ) ; aucun exemple avec u = sin x ou cos x (cos x·sin²x) |
| ch5 ln | 4 | 8 | 9 | limites de ln(u(x)) par composition ; aucune étude complète d'une fonction ln(u(x)) ; concavité par f″ ; croissances comparées seulement pour n = 1 |
| ch6 Nombres complexes (1) | 5 | 7 | 7 | partie « angles et géométrie » (arg((c − a)/(b − a)), orthogonalité, nature d'un triangle) absente et non annoncée ; ensembles de points (cercle, médiatrice) ; **aucune flèche de vecteur** dans tout le cours ; conj(z) au lieu de la barre ; conditions z ≠ 0 oubliées |
| **Total** | **23** | **50** | **41** | |

## Ce qui revient dans tous les chapitres (l'équivalent de l'« état physique » en chimie)

1. **La justification « car… » manque.** Le professeur écrit toujours *pourquoi* : « f est dérivable sur ℝ car c'est un
   polynôme », « f est continue sur I car elle est dérivable », « f([a ; b]) = [f(a) ; f(b)] car f est continue et
   strictement croissante ». Chez nous, la conclusion est écrite sans sa raison, ou la raison n'est dite qu'à l'oral.
2. **Les conditions disparaissent dans les résumés.** Les diapos donnent bien l'intervalle ou la condition, mais les fiches
   à recopier (cahier, bilan) les perdent : primitives sans « sur I » ni « u > 0 », quotients de complexes sans « z ≠ 0 »,
   symétrie sans « repère orthonormé ». C'est ce que l'élève recopie et réécrit au bac.
3. **Les notations du bac ne sont pas toujours celles qu'on écrit à l'écran** : flèche de vecteur, barre du conjugué,
   « n → +∞ » sous lim, f′_d(a) / f′_g(a), [2π] après un argument.
4. **Les phrases types d'interprétation géométrique** (asymptote, point unique d'abscisse α, ensemble des points M…) sont
   parfois seulement à l'oral ou dans une réaction préparée, pas au cahier.
5. **Les exemples restent trop simples** : u est presque toujours un polynôme (primitives, ln) ; le professeur traite
   u = sin x, ln(u(x)) et une étude complète de fonction avec ln.

## Par où commencer (priorité haute, coût faible)

- ch4 `pr_b1` : refaire la fiche en tableau à trois colonnes (fonction, primitives + k, sur I / condition).
- ch2 `df_dv6_montrer`, ch3 `su_f5_conditions`, ch1 `lc_c5_redaction` : ajouter la ligne « car … » et la phrase de conclusion.
- ch6 : flèches de vecteur et barre du conjugué à l'écran ; conditions z ≠ 0 sur les quotients.
- ch1 : « dans un repère orthonormé » sur la diapo du miroir y = x ; tableau des limites usuelles.

Les ajouts plus lourds (étude complète d'une fonction ln(u(x)), partie « angles et géométrie » des complexes, unicité de
f(x) = k) demandent de nouvelles diapos et une nouvelle voix : à décider.

---

## Limites et continuité

Sources comparées : notre cours `math_ch1_limites_continuite.json` (écran, cahier, voix, exercices, et simulations `limites-continuite-tableau/calculs-donnees.js`, `raccord.html` pour vérifier ce qui est à l'écran) ; livre de Prof Fayssal, PDF `Livre-Cours-2BAC-SC-EXP.pdf`, pages 7-26 (p. 7 rappel limites, p. 8-9 rappel dérivation, p. 11-23 cours « Page 01 à 13 », p. 24-26 résumé) ; cadre officiel SE 1.2.1-1.2.4, 1.2.11, 1.2.22. Les pages citées sont celles du fichier PDF.

### Plan comparé

| Partie du professeur (page PDF) | Où chez nous | Remarque |
|---|---|---|
| Rappel 1 : signe de ax + b et du trinôme (Δ) (p. 7) | lc_z2_signe (signe de x − a seulement) | Signe du trinôme absent (voir Manques) |
| Rappel 1 : tableaux somme / produit / quotient de limites, formes indéterminées (p. 7) | lc_l2_remplacer, lc_l4_formes, lc_l4_formes_b | Formes indéterminées complètes ; tableaux opératoires partiels |
| Rappel 1 : limites usuelles (xⁿ, x²ⁿ, x²ⁿ⁺¹, 1/xⁿ, √x, 1/√x, 1/x en 0±) (p. 7) | aucune diapo dédiée | Absent (voir Manques) |
| Rappel 1 : plus haut degré, √f, sin x/x, tan x/x, (1 − cos x)/x², comparaison, encadrement (p. 7) | lc_l7, lc_i4, lc_l12_sinus(_b) | tan x/x, (1 − cos x)/x², comparaison et encadrement absents |
| Rappel 2 : dérivabilité, tableau des dérivées (p. 8-9) | lc_z3_derivee (signe de f′ seulement) | Relève du ch2 dérivation : pas un manque ici |
| I.1 Continuité en un point : activité, définition, exemples (p. 11-12) | lc_c1_soudee, lc_c2_limite_image | Même ordre (image → définition → exemple). Condition « I ouvert, x₀ ∈ I » absente |
| I.2 Continuité à droite / à gauche : définitions + propriété (p. 12) | lc_c3, lc_c4, lc_c5_redaction | Calcul présent, mais le vocabulaire « continue à droite / à gauche en a » et la propriété ne sont jamais écrits |
| Exercices 01-02 (p. 13-14) | lc_c4_parametre (valeur de m) | Cas sin, \|x − 1\|, encadrement, changement X = x − 1 absents |
| II Continuité sur un intervalle : définitions, usuelles, opérations, √u, exercice 03 (p. 15-16) | lc_i1, lc_i2, lc_i3, lc_i4 | Définitions ]a ; b[ / [a ; b] absentes ; \|x\| et tan absentes ; pas d'étude « continuité sur D_f » |
| VI.1 Image d'un intervalle : théorème, [m ; M], tableau des 8 cas, exercice 04 (p. 17) | lc_j1 à lc_j5 | Règle « ouvert → limite » et exemples, mais ni le théorème général ni le tableau |
| VI.2 TVI, démonstration, corollaires 1 et 2, exercices 05-07 (p. 17-18) | lc_t1 à lc_t9 | Bien couvert ; corollaire 2 seulement pour 0 ∈ f(I) ; exercice « tableau de variations → nombre de solutions » absent |
| VI.3 Dichotomie (p. 19) | retirée | Hors cadre (voir dernière section) |
| A. Fonction réciproque : proposition, méthode f⁻¹(x), exercices 08-09, propriétés 1-4 (p. 19-20) | lc_r1 à lc_r9_valeur_absolue_b | Bien couvert ; propriété 4 (f⁻¹∘f, f∘f⁻¹) et « repère orthonormé » absents |
| B. Racine n-ième : définition, propriétés 1-9, exemples, exercices 10-11 (p. 21-22) | lc_n1 à lc_n7, lc_lr1 à lc_lr4 | Couvert ; nous séparons les limites avec ⁿ√ dans une partie VIII (ordre sans gêne) |
| Exercice 12, puissances rationnelles, exercice 13 (p. 23, marquée « 2 Bac SM ») | lc_p1, lc_p2, lc_p3 | Gardées par décision (voir l'audit précédent) ; la page 26 du résumé SX les reprend |
| Résumé (p. 24-26) | lc_e2_bilan, lc_e3_carte | Notre bilan ne cite pas la continuité à droite / à gauche, ni f⁻¹∘f |
| (absent du livre) | lc_o1, lc_z1, lc_z4, lc_z5, lc_l11, lc_t9, lc_r7, lc_e1_probleme | Plus chez nous (voir plus bas) |

### Manques

| Priorité | Catégorie | Ce que dit le professeur (page du PDF) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | définition / notation | « f est continue à droite de a ⇔ lim_{x→a⁺} f(x) = f(a) » (f définie sur [a ; a + r[) ; idem à gauche ; propriété « f continue en a ⇔ f continue à droite et à gauche en a ». Chaque calcul est conclu par « D'où f est continue à droite de 1 » (p. 12, 13, 24) | « continue à droite » et « continue à gauche » : 0 occurrence (écran, cahier, voix, simulation). lc_c5 écrit ① « lim = f(1) » sans la phrase de conclusion. Au national : « montrer que f est continue à droite en 0 » | lc_c5_redaction (les 2 définitions + la propriété, ① « donc f est continue à droite en 1 »), lc_e2_bilan point 2 |
| haute | formule | Tableau des limites usuelles : lim xⁿ = +∞ en +∞ ; en −∞ : x²ⁿ → +∞, x²ⁿ⁺¹ → −∞ ; lim 1/xⁿ = 0 en ±∞ ; lim 1/√x = 0 en +∞ ; lim 1/x = ±∞ en 0± ; lim 1/√x = +∞ en 0⁺ (p. 7) | Aucun tableau ; seulement des exemples (1/(x − 1) en 1±, ⁿ√x en +∞ dans lc_lr1). La parité en −∞ n'est jamais énoncée | nouvelle diapo entre lc_l2_remplacer et lc_l3 (ou dans lc_l4_formes_b) |
| haute | formule | Tableaux des opérations : L × ∞ (L ≠ 0) → ∞ par la règle des signes, ∞/L, L/L′, L/0 ; somme L + ∞ (p. 7) | lc_l4_formes_b : +∞ + ∞, produit d'infinis, k/∞, k/0. Manquent « nombre non nul × ∞ » et « ∞ / nombre » | lc_l4_formes_b (deux puces) et cahier |
| haute | propriété (condition) | « Les courbes de f et f⁻¹, dans un repère orthonormé, sont symétriques par rapport à la droite d'équation y = x » (p. 20, 25) | « orthonormé » : 0 occurrence. lc_r6_miroir, lc_r7, lc_e2_bilan énoncent la symétrie sans la condition (la simulation dit seulement « même échelle ») | lc_r6_miroir (puce + cahier), lc_r7_construire, lc_e2_bilan point 7 |
| haute | propriété | Corollaire 2 : f continue et strictement monotone sur I et k ∈ f(I) ⇒ f(x) = k admet une solution unique α dans I (p. 18, 25) ; cadre 1.2.4 : « unicité de la solution de f(x) = λ » | lc_t8 seulement « 0 ∈ f(I) » ; lc_t7 donne f(x) = k mais « au moins une ». « k ∈ f(I) » / « λ » : 0 occurrence | lc_t8_intervalle_ouvert (énoncé avec k, exemple f(x) = 1) |
| moyenne | définition | « f définie sur un intervalle ouvert I et x₀ ∈ I : f continue en x₀ ⇔ lim f(x) = f(x₀) » (p. 12, 24) | lc_c2 : « f est continue en a si lim f(x) = f(a) », sans la condition sur le domaine | lc_c2_limite_image (cahier) |
| moyenne | définition | Continue sur ]a ; b[ : continue en chaque point ; sur [a ; b] : continue sur ]a ; b[, à droite en a et à gauche en b (p. 15, 24) | Absent (« chaque point » : 0) ; lc_i1 passe directement aux fonctions usuelles | début de lc_i1_usuelles ou diapo avant |
| moyenne | méthode / exemple | Exercice 03 : déterminer D_f d'une fonction à deux expressions avec racines, étudier la continuité sur chaque morceau, au point de raccord, puis conclure sur D_f (p. 16) | « D_f » et « ensemble de définition » : 0 occurrence ; aucune étude « continuité sur D_f » | séance après lc_i3_racine_u (exercice de fin) |
| moyenne | propriété | « L'image d'un segment par une fonction continue est un segment ; l'image d'un intervalle est un intervalle » (p. 17, 24) | Absent (« est un intervalle » : 0) ; c'est ce qui justifie « J est un intervalle » | lc_j1_hauteurs ou lc_j5_non_monotone |
| moyenne | formule | Tableau des images (croissante / décroissante) : [a ; +∞[, [a ; b[, ]a ; b], ]−∞ ; b] (p. 17, 25) | Règle « ouvert → limite, fermé → image » + 3 exemples (lc_j4, lc_r3, lc_t8). Le cas décroissant sur [a ; +∞[ → ]lim ; f(a)] n'est jamais écrit | cahier de lc_j4_borne_ouverte (tableau) |
| moyenne | formule | lim tan x / x = 1 et lim (1 − cos x)/x² = 1/2 en 0, utilisées dans l'exercice 01-2 (p. 7, 13) | Absentes du cours (alors que notre fiche `cadre_reference_2bac_pc.json` les met dans `valeurs_reference`) | lc_l12_sinus (deux puces) |
| moyenne | propriété | Comparaison : g ≤ f et lim g = +∞ ⇒ lim f = +∞ (et −∞) ; encadrement g ≤ f ≤ h ⇒ lim f = l ; exemple sin x · sin(1/x) (p. 7, 14) | Absent du ch1 (présent seulement pour les suites, ch3) | après lc_l12_sinus_b |
| moyenne | propriété | (∀x ∈ I) f⁻¹∘f(x) = x ; (∀x ∈ J) f∘f⁻¹(x) = x (p. 20, 25) | Absent (aucune écriture f⁻¹(f(x)) ni ∘) | lc_r5_sens ou lc_r8_expression ; lc_e2_bilan point 6 |
| moyenne | formule | Signe de ax + b et du trinôme ax² + bx + c selon Δ (tableaux, p. 7) | lc_z2 : seulement x − a. Nécessaire pour le signe de 0⁺ / 0⁻ avec un dénominateur du second degré | lc_z2_signe (ou lc_l10_signe) |
| moyenne | propriété | Exercice 05 : f′(x) = cos x + 1 ≥ 0 ⇒ f strictement croissante (f′ nulle en des points isolés) (p. 18) | lc_z3 n'énonce que f′ > 0. Or la simulation de lc_r4_deux_lignes écrit « g′(x) = 2x − 2 ≥ 0 sur I : g est strictement croissante » sans la règle (elle n'existe qu'au ch2) | lc_z3_derivee (« f′ ≥ 0, nulle seulement en des points isolés ») |
| moyenne | formule | a³ + b³ = (a + b)(a² − ab + b²) à côté de a³ − b³ (p. 22) | Absent (« a³ + b³ » : 0) ; utile pour ∛x + 2 en −8 | lc_lr2_cle_de_trois |
| moyenne | méthode | Limite ∞/∞ avec racines d'indices différents : tout écrire avec l'indice commun (⁶√, ¹²√) (exercice 11-2 et 11-5, p. 22) | lc_lr4 traite seulement ∞ − ∞ ; l'indice commun n'est utilisé que pour comparer (lc_n5) | après lc_lr4_infini (exemple √(x + 1)/∛(x² + 3)) |
| moyenne | méthode | Équations avec ⁿ√ : ensemble de définition D_(E) d'abord ; changement d'inconnue X = ⁵√(x + 2) (équation du 2nd degré) ; ∛(1 − 2x) = √(x + 1) par élévation à la puissance 6 (exercice 10, p. 21) | lc_n7 : une seule équation simple (∛(2x³ + 11) = 3) | lc_n7_equation_racine (deuxième exemple) ou exercices de fin |
| moyenne | exemple | Exercice 07 : nombre de solutions de f(x) = 18, 0, −3, 3 lu sur un tableau de variations, puis encadrement (p. 18) | Absent | lc_t7_valeur_k ou séance TVI |
| basse | exemple | Exercice 05-2 : TVI avec une fonction trigonométrique sur [−π/6 ; 0] (p. 18) | Tous nos exemples TVI sont des polynômes (« π » : 0) | exercices de fin de lc_t6 |
| basse | exemple | Exercice 01-4 : (x² − 1)/\|x − 1\| en 1, on enlève la valeur absolue à droite et à gauche (p. 13-14) | Absent | lc_c3_deux_branches (exercice) |
| basse | méthode | Exercice 02 : sin(πx)/(x − 1) en 1, on pose X = x − 1 (p. 14) | Seulement t = ax en 0 (lc_l12_sinus_b) | lc_l12_sinus_b (exercice) |
| basse | propriété | Continuité de x ↦ \|x\| sur ℝ et de tan sur ℝ − {π/2 + kπ} ; f = αu (p. 15, 24) | lc_i1 : polynômes, 1/x, √x, sin, cos | lc_i1_usuelles |
| basse | propriété | ⁿ√x = ⁿ√y ⇔ x = y ; ¹√x = x (p. 21) | Seulement l'inégalité x < y ⇔ ⁿ√x < ⁿ√y (lc_n5) et √x = ²√x | lc_n3_regles |
| basse | définition | a^(p/q) avec p ∈ ℤ, q ∈ ℕ* ; 1/a^r = a^(−r) (p. 23, 26) | lc_p2 ne précise pas p ∈ ℤ, q ∈ ℕ* ; règle 1/x^r = x^(−r) absente | lc_p2_pq, lc_p3 |
| basse | méthode | Exercice 12 : stricte monotonie sans dériver (x < y ⇒ f(x) < f(y)) (p. 23, page « SM ») | Toujours par le signe de f′ | facultatif |

### Présent seulement à l'oral (à mettre à l'écran ou au cahier)

| Diapo | Phrase dite seulement dans la voix |
|---|---|
| lc_r8_expression | « Attention à l'ordre : c'est f de y, pas f de x » (l'erreur classique ; l'écran ne montre que la ligne pivot) |
| lc_l10_signe | « Ne jamais écrire nombre sur zéro sans le signe » (l'écran donne la règle mais pas cet interdit de rédaction) |
| lc_l11_interpreter | Sens d'une asymptote : « l'écart entre la courbe et la droite tend vers zéro » |

### Différences de notation ou de formulation

| Nous | Le professeur | À garder et pourquoi |
|---|---|---|
| « lim f(x) = 2 quand x → 1 » (cahier, student_trace) ; « lim g » sans variable (simulation lc_r4) | lim avec « x → a » sous le lim, toujours (p. 7-26) | Le professeur : c'est l'écriture exigée au bac. Au cahier, écrire « x → a » sous lim (ou au moins « lim_{x→+∞} g(x) ») |
| « u positive sur I », « le dénominateur ne s'annule pas sur I » | « (∀x ∈ I) ; u(x) ≥ 0 », « ∀x ∈ I ; v(x) ≠ 0 » (p. 15, 24) | Le professeur pour le cahier : la condition écrite avec le quantificateur et l'inégalité exacte (∀ : 0 occurrence chez nous) ; garder nos mots à l'oral |
| « continue à droite en a » (fiche, cadre) | « continue à droite de a » | Nous (« en a » : formulation des sujets nationaux) ; mais il faut l'écrire (voir Manques) |
| « la droite d'équation y = x » | « la première bissectrice (c'est-à-dire la droite d'équation y = x) » (p. 20) | Nous, en ajoutant une fois le mot « première bissectrice » (il figure dans `qualitatif_admis` de la fiche et dans des énoncés) |
| « f est continue en a si lim f(x) = f(a) » | « f continue en x₀ ⇔ lim f(x) = f(x₀) » | Équivalent ; garder le nôtre en ajoutant la condition de domaine |
| f⁻¹(x) = y ⇔ f(y) = x, « x ∈ J, y ∈ I » | système { f⁻¹(x) = y, x ∈ f(I) } ⇔ { f(y) = x, y ∈ I } | Équivalent ; le nôtre est plus lisible |
| « Donc », « D'après ① et ② » | « D'où », « Conclusion : » | Les deux sont admis |
| ℝ | IR | ℝ (écriture des sujets) |

### Ce que nous avons en plus

Utile (dans le cadre) :
- Interprétation géométrique d'une limite : asymptote verticale / horizontale avec la phrase type « la droite d'équation x = a est une asymptote verticale à (C_f) » (lc_l11) ; asymptote verticale ↔ horizontale pour (C_f⁻¹) (lc_r7).
- Rédactions modèles du national : solution unique en 4 lignes avec « Posons » (lc_t6), réciproque en 2 lignes (lc_r4), conclusion « α ∈ ]a ; b[ ».
- Méthode h(x) = f(x) − k (lc_t7) ; usage de f(α) = 0 et signe de f avant / après α (lc_t9).
- Rappels algébriques (a² − b², √(x²) = |x|, facteur (x − a)) ; forme canonique et « ai-je le droit de prendre la racine ? » (lc_r9) ; f⁻¹ ≠ 1/f ; restriction.
- Racine n-ième : règle du quotient, tableau xⁿ = a selon la parité, vérification des solutions (lc_n6, lc_n7).
- Problème national complet (lc_e1_probleme), carte du chapitre.

Hors cadre chez nous : rien trouvé.

### Hors cadre dans le livre (ne pas ajouter)

- Méthode de dichotomie, exemple et encadrement d'amplitude 0,25 (p. 19) : retirée exprès (audit précédent, `hors_cadre.mots`).
- Démonstration du TVI à partir de f([a ; b]) = [m ; M] (p. 18) : le cadre demande d'appliquer le théorème (1.2.3-1.2.4), pas de le démontrer.
- Page 13 du cours (p. 23 du PDF) marquée « 2 Bac SM » : l'exercice 12 et l'exercice 13 sont des exercices SM ; les puissances rationnelles elles-mêmes restent chez nous par décision (et sont dans le résumé SX, p. 26).
- Rappel 2 « Dérivabilité » (p. 8-9 : nombre dérivé, demi-tangentes, tableau des dérivées) : au programme, mais c'est le chapitre 2 (dérivation), pas ce chapitre.

---

## Dérivation et étude des fonctions

Sources : notre cours `math_ch2_derivation_etude_fonctions` (écran, cahier, voix, exercices, réactions préparées vérifiées dans le JSON) ; livre du Prof Fayssal, PDF `Livre-Cours-2BAC-SC-EXP.pdf` : rappel p. 7-9, « Dérivabilité » p. 27-37, « Étude des fonctions » p. 38-54. Toutes les pages lues sont marquées « 2 Bac sc / SX » (aucune page « 2 Bac SM » dans ce chapitre).

### Plan comparé

| Partie du professeur (page PDF) | Où chez nous | Remarque |
|---|---|---|
| Rappel 2 : dérivabilité, tableau des dérivées, variations (p. 8-9) | df_z3, df_dv1, df_va1 | Pas de dérivées de sin, cos, tan chez nous (voir Manques). |
| Ch. 2, I.1 Dérivabilité en un point : définition (forme x → a et forme h → 0), nombre dérivé (p. 28) | df_nd1 à df_nd4_calcul_b | Nous : seulement la forme x → x₀, sans « f définie sur un intervalle ouvert contenant a ». |
| I.1.b Interprétation géométrique : tangente, approximation affine, tracé de (T) (p. 29) | df_tg1 à df_tg3 | Approximation affine : retirée exprès (hors cadre). Tracé de (T) avec un vecteur directeur : absent. |
| I.2 Dérivabilité à droite / à gauche, équations des demi-tangentes, lien dérivable ⇒ continue (p. 30) | df_dt1 à df_dt3 | Équation de la demi-tangente absente. |
| I.3 Demi-tangente verticale (4 cas), exercice par morceaux (p. 31) | df_dt4, df_dt5, df_dt5_b, df_dt6 | Complet, et mieux expliqué chez nous (le sens se déduit du signe). |
| II. Dérivabilité sur un intervalle ; tableau des dérivées ; opérations (p. 32-33) | df_dv1 à df_dv6 | Définition « dérivable sur ]a ; b[ / [a ; b] » absente ; (1/v)′, trigonométrie absentes. |
| VI.1 Sens de variation (p. 33) ; VI.2 Extremums (p. 34) | df_va1 à df_va7 | « f′ = 0 ⇔ f constante » et « extremum ⇒ f′(a) = 0 » absents à l'écran. |
| III.1 Dérivée de la composée (p. 36) | df_dv5_racine_n (une ligne) | Hypothèses absentes. |
| III.2 Dérivée de la réciproque (formule sur J, démonstration, corollaire en un point) (p. 36-37) | df_rec1 à df_rec6 | Nous : seulement en un point. |
| Dérivée de ⁿ√x et de ⁿ√f (p. 37) | df_dv5_racine_n | Présent. |
| Ch. 3, I.1 Asymptotes horizontale, verticale, oblique (p. 40-41) | df_bi1 à df_bi3, df_bi7 | Conditions de la définition oblique incomplètes (voir Manques). |
| I.2 Branches paraboliques (p. 41-42) | df_bi4 à df_bi6_arbre_b | Complet. |
| II. Concavité, point d'inflexion (p. 43) | df_co1 à df_co4 | Ordre différent : nous mettons la concavité avant les branches infinies ; ça ne gêne pas. |
| III. Axe et centre de symétrie, domaine d'étude D_E (p. 43-44) | df_sy1 à df_sy4 | D_E absent. |
| Exercices d'étude complète : TVI + interprétation, tracé, parité, réciproque (p. 45-54) | df_ec1 à df_ec4, df_tr1 à df_tr6 | Voir Manques (interprétation de f(x) = 0, calcul de g⁻¹(a), parité ⇒ D_E). |
| (pas de partie) | df_pr1 à df_pr3 (position relative) | Le prof ne la traite que dans les exercices (p. 47, 52). |

### Manques

| Priorité | Catégorie | Ce que dit le professeur (page du PDF) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | méthode / notation | Justifier la dérivabilité avant de dériver, avec la raison : « f est dérivable sur ℝ car c'est un polynôme » ; « quotient de deux fonctions dérivables et (∀x ∈ ℝ) x² + 1 ≠ 0 » ; « √u : u dérivable et (∀x) u(x) > 0 » ; « f est dérivable sur ]1 ; +∞[ (fonction rationnelle) » (p. 32, 33, 49) | Écran : seulement « Première ligne : f est dérivable sur … », sans le « car … » ; la raison n'existe que dans une réaction préparée de df_dv6_montrer | df_dv6_montrer (écran + cahier), rappel dans df_fin1_bilan |
| haute | définition | Dérivabilité sur un intervalle : « f dérivable sur ]a ; b[ ⇔ dérivable en tout point de ]a ; b[ » ; « f dérivable sur [a ; b] ⇔ dérivable sur ]a ; b[, à droite en a et à gauche en b » ; fonction dérivée f′ (p. 32). Objectif 1.2.5 du cadre (« en un point et sur un intervalle ») | Absent (0 occurrence de « dérivable sur [ », de « fonction dérivée ») | nouvelle diapo après df_dt3_anguleux, ou en tête de df_dv1_tableau |
| haute | méthode / notation | Interprétation géométrique d'une solution : « (Cf) coupe l'axe des abscisses en un point unique d'abscisse α, avec α ∈ ]−1 ; 0[ » ; « (Cf) coupe l'axe des abscisses au point d'abscisse −3 » (p. 46, 50, 52) | Absent à l'écran, au cahier et dans la voix (seulement dans une réaction préparée de df_ec4_unique) | df_ec4_unique (écran + cahier) |
| moyenne | formule | Dérivées de sin x, cos x, tan x = 1 + tan²x, sin(ax + b), cos(ax + b) dans le tableau des dérivées (p. 8, 32) ; exercices avec cos(√x), sin(√(x² + 5)), cos x/(1 + sin x) (p. 36, 53-54) | Absent du ch2 (0 « cos ») ; (sin x)′ et (cos x)′ n'arrivent qu'au ch4 (pr_z5_cos_sin) | df_dv1_tableau (une ligne) ; à trancher, la trigonométrie est rare au national PC |
| moyenne | formule | (1/v)′ = −v′/v², v ≠ 0 (p. 8, 32, 51) | Absent (passe par la règle du quotient) | df_dv2_produit_quotient_b |
| moyenne | propriété | (∀x ∈ I) f′(x) = 0 ⇔ f constante sur I ; et la forme large f′ ≥ 0 ⇔ f croissante (p. 9, 33) | Absent : seulement f′ > 0 ⇒ strictement croissante, f′ < 0 ⇒ strictement décroissante | df_va1_monte |
| moyenne | propriété | « Si f est dérivable en a et admet un extremum en a, alors f′(a) = 0 ; la réciproque est fausse : f(x) = 2x³, f′(0) = 0, pas d'extremum » (p. 34) | Le contre-exemple x³ et la condition nécessaire ne sont que dans les réactions préparées ; à l'écran seulement « + 0 + : pas d'extremum » | df_va2_sommet_b |
| moyenne | formule | Équation de la demi-tangente : y = f′_d(a)(x − a) + f(a) avec x > a ; y = f′_g(a)(x − a) + f(a) avec x < a ; exemple « (T) : y = x + 1 ; x > 1 » (p. 30, 31, 49) | Absent : seulement « demi-tangente à droite de coefficient directeur l » | df_dt1_droite, df_dt2_gauche |
| moyenne | propriété | Réciproque sur tout l'intervalle : f continue et strictement monotone sur I, f′ ne s'annule pas sur I ⇒ f⁻¹ dérivable sur J = f(I) et (f⁻¹)′(x) = 1/f′(f⁻¹(x)), avec la démonstration par f∘f⁻¹(x) = x (p. 36) | Absent : seulement la formule en un point | df_rec3_formule (une ligne) |
| moyenne | propriété | Hypothèses de la réciproque en un point : « f continue et strictement monotone sur I, a ∈ I, b = f(a), f dérivable en a, f′(a) ≠ 0 » (p. 36) | df_rec3/df_rec5 : « f dérivable en x₀ et f′(x₀) ≠ 0 », sans « continue et strictement monotone sur I » (ce n'est que dans df_rec1) | df_rec5_national (ligne ②) |
| moyenne | propriété | Composée : « f dérivable sur I, g dérivable sur J, f(I) ⊂ J ⇒ g∘f dérivable sur I et (g∘f)′(x) = g′(f(x))·f′(x) » (p. 36) | df_dv5_racine_n : formule seule, sans hypothèses | df_dv5_racine_n |
| moyenne | définition | Conditions des définitions : « f définie sur un intervalle ouvert I, a ∈ I » ; à droite « f définie sur [a ; a + r[ », à gauche « sur ]a − r ; a] » (p. 28, 30) | Absent | df_nd3_nombre_derive, df_dt1_droite |
| moyenne | méthode | Domaine d'étude D_E = Df ∩ [a ; +∞[ quand x = a est axe ou Ω(a ; b) centre ; parité ⇒ D_E = Df ∩ [0 ; +∞[ (p. 43, 44, 46) | Absent (0 « domaine d'étude ») ; df_tr5_symetrie dit seulement « l'autre moitié sans calcul » | df_sy4_rediger ou df_tr5_symetrie |
| moyenne | notation | Tableau de concavité : lignes x | f″(x) | « convexité de (Cf) » avec ∩, ∪ et « le point A(…) est point d'inflexion » (p. 43, 45, 54) | Pas de tableau à l'écran ni au cahier (seulement une « ligne sous la courbe » dans la figure, à l'oral) | df_co3_f_seconde ou df_co4_changeant |
| moyenne | exemple | Calculer une valeur de la réciproque en résolvant g(y) = a : g⁻¹(1/2) = ³√3 (p. 50) | Nous trouvons l'antécédent seulement « à vue » (f(1) = 2) | df_rec5_national (deuxième exemple) |
| basse | définition | Asymptote oblique : « a ∈ ℝ*, b ∈ ℝ ; lim f(x) = ∞ et lim [f(x) − (ax + b)] = 0 » (p. 40) | df_bi3 : seulement lim [f(x) − (ax + b)] = 0 | df_bi3_oblique |
| basse | propriété | Concavité : « f deux fois dérivable sur I » ; « (∀x ∈ I) f″(x) ≥ 0 » (p. 43) | « f″ ≥ 0 sur I » sans l'hypothèse | df_co3_f_seconde |
| basse | formule | Deuxième forme : lim (f(a + h) − f(a))/h = l quand h → 0 (p. 8, 28) | Absent | df_nd3_nombre_derive (une ligne) |
| basse | formule | (axⁿ)′ = a·n·xⁿ⁻¹ pour n ∈ ℤ∖{−1}… (puissances négatives, p. 32) | Seulement n entier naturel et 1/x | df_dv1_tableau |
| basse | méthode | Tracer la tangente avec un vecteur directeur u(1 ; f′(a)) (p. 29) | Absent (deux points seulement, df_tr2) | df_tg2_ecrire |
| basse | notation | « Tracer (Cf) dans un repère orthonormé (O ; i⃗ ; j⃗) » (p. 45, 48, 50) | Absent (0 « repère orthonormé ») | df_tr2_droites |
| basse | exemple | Tableau de variations avec un intervalle exclu hachuré (Df = ]−∞ ; −1/3[ ∪ [0 ; +∞[, p. 34) | Seulement la double barre pour une valeur exclue (df_va5) | df_va5_double_barre |
| basse | exemple | Tracer (Cg) d'une fonction paire g déduite de f (g(x) = (3x⁴ + 1)/(3|x³|), p. 47-48) | Absent | df_tr5_symetrie (exercice) |

### Présent seulement à l'oral (à mettre à l'écran ou au cahier)

- df_dt4_infini et df_ec3_etude : écrire la raison de la limite (« le haut tend vers 1, le bas tend vers 0⁺, donc +∞ »). Le prof l'écrit toujours : « car lim 3x³ = 0⁺ » (p. 47, 51).
- df_va3_factoriser : « f est dérivable sur ℝ » n'est dit qu'à la voix ; l'écran commence directement par f′(x).
- df_dv4_racine : « le bas est positif, donc le signe de la dérivée est le signe de x ».
- df_tr3_points : « l'énoncé donne des valeurs approchées entre parenthèses : on les place toutes ».
- df_co3_f_seconde : la ligne de signe de f″ sous la courbe (pas de tableau de concavité écrit).

### Différences de notation ou de formulation

| Nous | Le professeur | À garder |
|---|---|---|
| (f∘g)′(x) = g′(x)·f′(g(x)) | (g∘f)′(x) = g′(f(x))·f′(x) (p. 36) | Une seule écriture dans tout le cours ; celle du prof (g∘f) est la plus fréquente dans les manuels marocains. |
| « pour tout x de I », « f′ > 0 sur I » | « (∀x ∈ I) : f′(x) ≥ 0 » (p. 33, 43) | Montrer au moins une fois le symbole ∀ au cahier : l'élève le lit dans les énoncés. |
| f′ > 0 ⇒ strictement croissante (sauf points isolés) | f′ ≥ 0 ⇔ croissante (p. 33) | Garder la nôtre (le national demande « strictement ») et ajouter la forme large et le cas constant. |
| « branche parabolique de direction l'axe des ordonnées » | « branche parabolique dirigée vers l'axe des ordonnées » (p. 41-42) | Garder la nôtre (formule des corrigés du national) ; signaler que les deux se disent. |
| f_d′(x₀), f_g′(x₀) | f′_d(a), f′_g(a) (p. 30) | Équivalentes ; rien à changer. |
| (f⁻¹)′(y₀) = 1/f′(x₀) | (f⁻¹)′(b) = 1/f′(a) et (f⁻¹)′(x) = 1/f′(f⁻¹(x)) (p. 36) | Garder la nôtre et ajouter la forme sur J. |
| « valeur exclue : double barre » | même chose, plus zone hachurée pour un intervalle exclu (p. 34) | Garder et ajouter le cas hachuré. |

### Ce que nous avons en plus

Utile et dans le cadre : rappels de 1re bac (df_z1 à df_z5) ; carte du chapitre (df_c1_carte, df_fin2_carte) ; nom « point anguleux » (df_dt3, le prof ne le nomme pas) ; explication du sens des demi-tangentes verticales (df_dt5, df_dt5_b) ; contre-exemple x⁴ pour l'inflexion (df_co4) ; inégalité par le minimum (df_va6, objectif 1.2.13) ; fonction auxiliaire g (df_va7) ; « montrer que f′(x) = … » (df_dv6) ; partie complète sur la position relative (df_pr1 à df_pr3) ; asymptote quand la droite est donnée (df_bi7) ; ordre du tracé (df_tr1 à df_tr5) ; lecture graphique f(x) = m (df_tr6, objectifs 1.2.9, 1.2.10) ; tangente horizontale de la réciproque devient verticale (df_rec4) ; ordre d'un problème national et usage d'un résultat donné (df_ec1, df_ec2) ; vérification de l'équation de la tangente (df_tg3).

### Hors cadre dans le livre (ne pas ajouter)

- Approximation affine f(x) ≅ f′(a)(x − a) + f(a) et valeur approchée de f(5,001) (p. 29-30) : pas dans le cadre ; retirée exprès (note du JSON « pas d'approximation affine chiffrée », audit précédent).
- Rappel « limites trigonométriques » (sin x/x, (1 − cos x)/x², p. 7) : appartient au ch1 (limites), pas à ce chapitre.

---

## Suites numériques

Sources : `math_ch3_suites_numeriques.json` (72 diapos) et le livre du Prof Fayssal, « Limite d'une suite numérique », pages 01 à 10 = **PDF p. 57 à 66** (p. 56 = couverture). Le livre ne refait pas les rappels de 1re bac (suite arithmétique, principe de récurrence). Il s'en sert dans les exercices. Les formules douteuses de l'extraction ont été relues sur le PDF.

### Plan comparé

| Partie du professeur (PDF) | Où chez nous | Remarque |
|---|---|---|
| 1) Limite infinie, limite finie, définitions par intervalles ; convergente / divergente ; (−1)ⁿ divergente (p. 57) | su_l1_converge, su_l4_qn_negatif | Chez nous, la définition est intuitive (« les termes se serrent »). Il n'y a pas de définition par intervalles. |
| 1c) Limites usuelles n, n², √n, nᵖ, 1/n, 1/n², 1/√n, 1/nᵖ (p. 57) | su_l2_reference (nᵅ) | Présent, sous une forme plus générale |
| 2) Opérations sur les limites (tableaux somme, produit, quotient) ; 4 formes indéterminées ; Ex01 FI ∞−∞, ∞/∞, conjugué (p. 58-59) | Absent du ch3. Rappel implicite dans su_l5_avec_qn (« puis les opérations »). Le ch1 traite ces règles pour les fonctions. | Voir les manques |
| Ex02-Ex03 sommes télescopiques Σ, produit Π (p. 59-60) | Absent | Basse priorité |
| 3) Comparaison (+∞ et −∞), gendarmes, sin n / n (p. 60) | su_c4_comparaison à su_c8_ecart | La version −∞ manque, ainsi que « à partir d'un certain rang » |
| 4) Majorée, minorée, bornée ; cos n, (−1)ⁿ (p. 61) | su_b1_plancher, su_b2_bornee | Présent (sans les exemples trigonométriques) |
| 5) Croissante (strict), décroissante, constante ; croissante ⇒ uₙ ≥ u₀ ; Ex04 récurrence (p. 61) | su_m1 à su_m4, su_c2_couple ; récurrence : su_r1 à su_r8 | « Strictement » et « constante » manquent à l'écran |
| 6) Convergence des suites monotones ; Ex05, Ex06 (p. 61-62) | su_c1_plafond à su_c3_plafond_limite | Présent (et plus détaillé chez nous) |
| 7) Suite géométrique : rappel, uₙ = u₀qⁿ, Ex07, lim qⁿ (Bernoulli, démonstration), somme, Ex08-Ex09 (p. 63-64) | su_a6, su_a7, su_a9b ; su_l3 à su_l5 ; su_p3 | Placée en fin de chapitre par le livre, au début chez nous. Cet ordre ne gêne pas. |
| 8) Vₙ = f(Uₙ), f continue en l (p. 65) | su_l7_f_un | Présent |
| 9) Uₙ₊₁ = f(Uₙ) : f continue sur I, f(I) ⊂ I, convergente ⇒ f(L) = L ; Ex10-Ex11 (p. 65-66) | su_f1 à su_f7 | Les conditions sont présentes. La méthode pour **prouver** f(I) ⊂ I manque, ainsi que la justification de la continuité et le choix entre deux solutions toutes deux dans I. |
| Absent du livre | su_a4, su_a5, su_a8, su_a9 (arithmétique) ; partie IV (suite auxiliaire) ; su_p1, su_p2 (rang, somme mixte) | Ces parties sont chez nous en plus. Voir « Ce que nous avons en plus ». |

Ordre : le livre suit la théorie (limites → comparaison → monotonie → géométrique → f). Nous suivons l'ordre des questions du national. L'ordre du livre n'apporte rien à reprendre. Aucune partie du livre ne manque entièrement chez nous, sauf « 2) Opérations sur les limites ».

### Manques

| Priorité | Catégorie | Ce que dit le professeur (page du PDF) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | méthode | Pour prouver f(I) ⊂ I, il calcule l'image de l'intervalle : « f([1 ; 3]) = [f(1) ; f(3)] = [√5 ; 3] ⊂ [1 ; 3] » (p. 65) et « f([0 ; 1]) = [f(0) ; f(1)] = [0 ; 1/2] ⊂ [0 ; 1] » (p. 66), car f est continue et strictement croissante. | su_f5 pose « f(I) ⊂ I » comme condition sans dire comment la prouver. su_f3 écrit seulement « [1 ; 4/3] ⊂ [1 ; 2] ». « f(I) = » : 0 occurrence. | su_f3_encadrement_f (écran et cahier) et rappel dans su_f5_conditions |
| haute | notation / rédaction | Il justifie la continuité par une phrase : « f est continue sur l'intervalle [1 ; 3] car elle est dérivable » (p. 65-66). | Nous écrivons « f est continue sur I » sans raison. « dérivable » : 0 occurrence. | su_f5_conditions, su_f7_national, su_e2_bilan (point 8) |
| haute | méthode | Ex10 : f(x) = x ⇔ x = 1 ou x = 3. **Les deux solutions sont dans [1 ; 3]**, et c'est le sens de variation qui tranche : « la suite est croissante donc la limite est 3 » (p. 65). | su_f6_choisir ne traite que le cas où une solution est hors de I. su_f7 (−1 et 3) est dans le même cas. Le cas « deux solutions dans I » est absent. | Nouveau point dans su_f6_choisir. Écrire la justification complète, car le livre est trop court ici : croissante ⇒ uₙ ≥ u₁ = √5 > 1, donc ℓ ≥ √5 et ℓ = 3. |
| moyenne | formule | Tableaux somme, produit, quotient pour les suites, et les 4 formes indéterminées « ∞ − ∞ », « 0 × ∞ », « ∞/∞ », « 0/0 » (p. 58) | « indéterminée » : 0 occurrence dans le ch3. Présent au ch1 (fonctions). su_l5 dit seulement « puis les opérations sur les limites ». | Une diapo de rappel avant su_l5_avec_qn |
| moyenne | méthode / exemple | FI avec deux puissances : 2ⁿ − 3ⁿ = 3ⁿ((2/3)ⁿ − 1) → −∞ ; −5 × 4ⁿ → −∞ ; (−2)ⁿ/3 n'a pas de limite (Ex08, p. 64) | Aucun exemple k·qⁿ avec k < 0, ni de factorisation par la puissance dominante (« 3ⁿ » : 0 occurrence) | su_l5_avec_qn ou une diapo juste après su_l4c_quatre_cas |
| moyenne | propriété | Théorème 2 : à partir d'un certain rang, uₙ ≥ vₙ et lim uₙ = −∞ ⇒ lim vₙ = −∞. Toutes les comparaisons valent « **à partir d'un certain rang** » (p. 60). | su_c4 ne donne que la version +∞. « certain rang » : 0 occurrence. | su_c4_comparaison (écran et cahier) |
| moyenne | définition | Propriété 01 : uₙ₊₁ − uₙ > 0 ⇒ strictement croissante ; < 0 ⇒ strictement décroissante ; = 0 ⇒ constante (p. 61) | su_m1 et su_m2 ne donnent que les inégalités larges. « strictement » n'apparaît que dans la réaction de la question de su_m4. « constante » n'apparaît que dans les rappels. | su_m1_pour_tout_n |
| moyenne | notation / rédaction | Phrase type : « (Vₙ) est géométrique de raison q = 2/3 et de premier terme V₀ = U₁ − U₀ = 1 » (« préciser ses caractéristiques », p. 63) | La phrase de su_x2 s'arrête à « géométrique de raison q ». v₀ n'est calculé qu'ensuite, dans su_x4. « et de premier terme » : 0 occurrence. | su_x2_geometrique (student_trace et cahier) |
| moyenne | notation | « lim uₙ » est toujours écrit avec « n→+∞ » sous le lim (p. 57 à 66) | Partout « lim uₙ », sans « n → +∞ » | Toutes les diapos de la partie V (su_l…) et de la partie VI (su_c…), à l'écran et au cahier. Au moins une fois : « lim (n→+∞) uₙ ». |
| basse | définition | Définitions de lim = +∞, −∞, L par des intervalles « à partir d'un certain rang » (p. 57) | Définition seulement intuitive (su_l1) | su_l1_converge (une ligne, si l'on veut) |
| basse | propriété | lim uₙ = −∞ ⇔ lim (−uₙ) = +∞ (p. 57) | Absent | su_l1_converge |
| basse | exemple | Les suites cos n et (−1)ⁿ sont bornées (p. 61). Gendarmes : −1/n ≤ sin n / n ≤ 1/n (p. 60). Comparaison : n² + (−1)ⁿ ≥ n² − 1 (p. 60). | Absent (aucun « sin », « cos » ni « (−1)ⁿ » à l'écran) | su_b2_bornee, su_c4_comparaison |
| basse | méthode | FI ∞ − ∞ : n² − 5n + 1 = n²(1 − 5/n + 1/n²) ; conjugué √(n+2) − √n (p. 58-59) | Seule la fraction est traitée (su_l6). Le conjugué est vu au ch1. | su_l6_fraction (un exemple polynôme) |
| basse | exemple | Sommes télescopiques 1/(k(k+1)) = 1/k − 1/(k+1), notation Σ (Ex02, p. 59 ; Ex06, p. 62) ; produit Π (Ex03, p. 59-60) | Absent (« Σ », « ∑ » : 0 occurrence) | Facultatif, partie VIII |
| basse | méthode | De uₙ ≤ 2 − 1/n, on déduit uₙ ≤ 2 : la suite est majorée par une **constante** (Ex06, p. 62) | Absent | su_c2_couple (une remarque) |
| basse | notation | Suite définie à partir d'un rang : (Uₙ)ₙ∈ℕ*, (Uₙ)ₙ≥5 (p. 62, 64) | ℕ* est cité (su_a1), mais pas la notation (uₙ)ₙ≥p | su_a1_liste |

### Présent seulement à l'oral (à mettre à l'écran ou au cahier)

- su_l2_reference : « 1/√n, c'est n puissance moins un demi ». Ce lien entre √ et nᵅ n'est dit qu'à l'oral.
- su_b1_plancher : « Les points sont isolés, on ne les relie pas » (convention du graphique d'une suite). L'image montre des points isolés, mais la règle n'est pas écrite.
- su_a7_terme_geo : « vérifie toujours ta formule avec n = 0 ». L'écran dit seulement « q⁰ = 1 ».
- su_a5_terme_arith et su_a6_geometrique : les exemples rédigés (uₙ = 2 + 3n ; uₙ₊₁ = 2uₙ, d'où raison 2) ne sont qu'à l'oral.
- su_f5_conditions : « Sans une de ces conditions, le correcteur refuse ».

### Différences de notation ou de formulation

| Nous | Le professeur | À garder |
|---|---|---|
| « pour tout n ∈ ℕ » | « (∀n ∈ ℕ) ; » | Les deux. Montrer une fois le symbole ∀, car l'élève le lit dans les énoncés. |
| Croissante : uₙ₊₁ − uₙ ≥ 0 | Propriété 01 en strict : uₙ₊₁ − uₙ > 0 ⇒ croissante (p. 61) | Garder notre définition large, qui est juste, et ajouter « strictement ». Ne pas reprendre l'implication stricte du livre comme définition. |
| « Critère de comparaison » | « Théorème des gendarmes » / « théorème d'encadrement » (p. 60) | Écrire les deux noms à l'écran. La voix « mixed » dit déjà « gendarmes ». |
| Somme géométrique : premier terme × (1 − q^(nombre de termes))/(1 − q) | Uₚ(1 − qⁿ⁻ᵖ⁺¹)/(1 − q) ; U₀(1 − qⁿ⁺¹)/(1 − q) ; 1 + q + … + qⁿ = (1 − qⁿ⁺¹)/(1 − q) (p. 64) | Garder notre version en mots, qui évite l'erreur de puissance, et ajouter la ligne 1 + q + … + qⁿ en symboles à su_a9b. |
| lim nᵅ (α > 0 ou α < 0) | nᵖ, 1/nᵖ avec p ∈ ℕ*, et √n à part | Les deux. Garder nᵅ (programme : puissances rationnelles) en citant aussi nᵖ. |
| ℓ | L | Indifférent |
| Conditions de ℓ = f(ℓ) : f continue sur I, f(I) ⊂ I, u₀ ∈ I, convergente | Les mêmes (U₀ ∈ I est dans l'hypothèse, p. 65) | Identique |
| Rédaction de la récurrence : Initialisation / Hérédité / Conclusion « d'après le principe de récurrence » | « Pour n = 0 … la propriété est vraie », « Soit n … supposons … et montrons … », « D'après le principe de récurrence » | Identique. Notre version est plus explicite. |

### Ce que nous avons en plus

- Utile et dans le cadre : suite arithmétique, son terme général et sa somme ; nombre de termes n − p + 1 (1re bac, utile en 1.1.5). Méthodes d'hérédité : affine, fraction, écriture « vérifier que », strict ou large (su_r3 à su_r7). Monotonie par le quotient uₙ₊₁/uₙ (su_m4). Toute la partie IV, suite auxiliaire géométrique ou arithmétique et suites homographiques (1.1.1, absente du livre). Lecture graphique en escalier (su_f1, su_f2). « Le plafond n'est pas la limite » (su_c3). |uₙ − ℓ| ≤ vₙ et uₙ₊₁ ≤ k·uₙ ⇒ uₙ ≤ kⁿu₀ (su_c5 à su_c8). Plus petit rang, somme mixte, limite d'une somme géométrique (1.1.5). Exercices des nationaux 2016 à 2025.
- Rien de hors cadre chez nous : pas de suites adjacentes, pas de dichotomie.

### Hors cadre dans le livre (ne pas ajouter)

- Ex07 (p. 63) : récurrence d'ordre 2, Uₙ₊₂ = (5/3)Uₙ₊₁ − (2/3)Uₙ. Le cadre 1.1.1 ne cite que uₙ₊₁ = auₙ + b et uₙ₊₁ = (auₙ + b)/(cuₙ + d).
- Inégalité de Bernoulli et démonstration de lim qⁿ (p. 63) : aucun objectif ne demande la démonstration. Le résultat suffit.
- Définitions formelles par intervalles (p. 57) : non exigées. Au plus une ligne (voir « basse » plus haut).
- La page 10 (PDF p. 66) porte l'en-tête « 2bac SM ». Son contenu est la fin de l'Ex11 (uₙ₊₁ = f(uₙ), objectif 1.1.4), donc il reste dans le cadre.
- Erreurs du livre à ne pas recopier :
  - p. 66 : « 1 ≤ uₙ ≤ 3 ⟹ f(0) ≤ f(uₙ) ≤ f(1) » au lieu de 0 ≤ uₙ ≤ 1.
  - Ex11 : l'énoncé demande 0 < uₙ < 1, mais la solution prouve 0 ≤ uₙ ≤ 1 (p. 65-66).
  - Ex10 : le choix de la limite n'est justifié que par « croissante » (p. 65).

---

## Primitives

Sources : notre cours `math_ch4_primitives` (écran, cahier, voix, exercices) ; livre Prof Fayssal, « Cours 05 : Primitives d'une fonction », PDF p. 69 (Page 01), p. 70 (Page 02), p. 71 (Page 03) ; cadre officiel 1.2.14, 1.2.15 (1.3.1 pour l'intégrale).

### Plan comparé

| Partie du professeur (page PDF) | Où chez nous | Remarque |
|---|---|---|
| I. Primitive d'une fonction : exemple, définition, remarque d'équivalence (p. 69) | pr_d1, pr_d2, pr_d3, pr_d4 | Même contenu. Nous avons en plus la rédaction en 3 lignes « vérifier une primitive ». |
| Propriété F + C et démonstration (p. 69) | pr_e3, pr_e4 | Présent, avec la démonstration. |
| Existence : f continue sur un intervalle ⇒ primitives ; remarque « forme explicite pas toujours connue » (p. 69) | pr_e1, pr_e2 | Propriété présente ; la remarque manque. |
| Exercice 01 : toutes les primitives, puis G(1) = 2 (p. 69) | pr_e6, pr_e7, pr_x2 | Équivalent présent. |
| Différence de deux primitives = constante, démonstration (p. 69) | pr_e4_b | Présent (démonstration (G − F)′ = 0). |
| II. Tableau des primitives usuelles, colonne « Sur I » (p. 70) | pr_u1 à pr_u8 | Toutes les lignes du cadre présentes, réparties sur 9 diapos ; le tableau d'ensemble n'existe qu'au bilan pr_b1, incomplet et sans intervalles (voir Manques). |
| II.2 Linéarité + démonstration (p. 70) | pr_l1, pr_u3 | Énoncé sans hypothèses ni « sur I », sans démonstration. |
| III. Opérations et fonctions composées, colonne « Condition » (p. 70) | pr_c1 à pr_c9, pr_r1, pr_r2 | Toutes les lignes du cadre présentes ; les conditions sont sur les diapos, pas au bilan. |
| Exercice 02 (10 cas) (p. 71) | pr_l3, pr_c2 à pr_c9, pr_x1 à pr_x3 | Cas 1 à 5 couverts ; cas 6 à 9 (u = sin x, cos³x, numérateur réécrit, puissances négatives) absents ; cas 10 hors cadre. |
| — | Ouverture, rappels pr_z1 à pr_z5, VI organigramme, VII graphique, VIII type national, IX bilan | En plus chez nous. L'ordre est le même que chez le professeur : rien ne gêne. |

### Manques

| Priorité | Catégorie | Ce que dit le professeur (page du PDF) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | notation / formule | Chaque ligne du tableau porte son intervalle (colonne « Sur I » : ℝ, ]0 ; +∞[ ou ]−∞ ; 0[…) et chaque forme composée sa condition (colonne « Condition » : u ≠ 0 sur I, u > 0…) ; chaque primitive est écrite « F(x) = … + C » (p. 70) | Les intervalles et les conditions sont sur les diapos (pr_u4, pr_u5, pr_u5_b, pr_c5, pr_c6, pr_c7), mais la fiche à recopier pr_b1 (points 4 et 6) n'en donne aucun : « 1/x² → −1/x ; 1/√x → 2√x ; u′/√u → 2√u ; u′/u² → −1/u », sans intervalle, sans u > 0, sans u ≠ 0 et sans + k. C'est l'équivalent de l'état physique oublié : l'élève recopie la formule sans sa condition | pr_b1 : tableau à 3 colonnes (fonction, primitives avec + k, sur I / condition) |
| haute | formule | Tableau complet des usuelles : a, xⁿ, xʳ, 1/x², 1/√x, cos, sin, 1 + tan², sin(ax + b), cos(ax + b) ; composées : u′u, u′uⁿ, u′uʳ, u′v + uv′, u′/u², (u′v − uv′)/v², u′/√u (p. 70) | La fiche pr_b1 oublie xʳ (pr_u5_b), 1/xⁿ (pr_u4_b), sin(ax + b) (pr_u7), 1 + tan²x (pr_u8), u′uʳ (pr_c5), (ax + b)ⁿ (pr_c4). Les lignes existent dans les diapos, pas dans le résumé | pr_b1 (points 4 et 6), pr_b2 |
| haute | exemple / méthode | Forme composée avec u trigonométrique : f(x) = cos x·sin²x, « de type u′u² avec u(x) = sin x → u′(x) = cos x », F(x) = (1/3)sin³x + C (p. 71, ex. 6). Forme très fréquente dans les intégrales du semestre 2 | Absent : dans toutes nos formes, u est un polynôme (x² + 1, 3x² + 1, πx² + 3…) ; aucune recherche de « sin³ », « u = sin », « u = cos » ne trouve d'exemple | pr_c2 (deuxième exemple) ou nouvelle diapo après pr_c9 ; exercice de fin à pr_r3 |
| moyenne | méthode | Faire apparaître u au numérateur : x/(x + 2)⁴ = (x + 2)/(x + 2)⁴ − 2/(x + 2)⁴ = (x + 2)⁻³ − 2(x + 2)⁻⁴, puis u′uⁿ avec n entier négatif ; x(x + 2)⁶ = [(x + 2) − 2](x + 2)⁶ (p. 71, ex. 8 et 9) | Absent. Notre u′uⁿ est limité à n ∈ ℕ* (pr_c1_b) ; puissances négatives seulement pour x seul (pr_u4_b : 1/xⁿ) et u′/u² (pr_c6) ; aucun exemple de 1/(ax + b)³ ou (ax + b)⁻ⁿ | pr_l3 (nouvelle ligne « faire apparaître u ») et pr_c4 (étendre (ax + b)ⁿ aux exposants négatifs, sur un intervalle où ax + b ≠ 0) |
| moyenne | exemple | cos³x = cos x·cos²x = cos x(1 − sin²x) = cos x − cos x·sin²x, F(x) = sin x − (1/3)sin³x + C (p. 71, ex. 7). Utilise cos² + sin² = 1, ce n'est pas la linéarisation (qui reste « plus tard », audit précédent) | Absent | Après l'exemple u = sin x (même diapo ou exercice de fin) |
| moyenne | propriété | Linéarité : « f et g sont deux fonctions continues sur un intervalle I ; si F est une primitive de f et G une primitive de g sur I, alors F + G est une primitive de f + g et kF une primitive de kf », démonstration (F + G)′ = F′ + G′ = f + g, (kF)′ = kF′ = kf (p. 70) | pr_l1 : « f + g → F + G ; αf → αF », sans hypothèse, sans « sur I », sans justification (ni écran, ni cahier, ni voix) | pr_l1 : énoncé complet au cahier + la ligne (F + G)′ = F′ + G′ |
| basse | exemple | u′u → u²/2 (cas n = 1) : (2x − 5)(x² − 5x + 4) → (1/2)(x² − 5x + 4)² + C (p. 70 et p. 71, ex. 3) | Couvert par u′uⁿ (n ∈ ℕ*) mais aucun exemple à l'écran avec n = 1 ; u²/2 n'apparaît que dans une réaction préparée | pr_c2 (exemple ou exercice de fin) |
| basse | formule | 1 + tan²x → tan x sur ]−π/2 + kπ ; π/2 + kπ[, k ∈ ℤ (p. 70) | pr_u8 : seulement ]−π/2 ; π/2[ | pr_u8 (diapo « pour mémoire ») |
| basse | définition | Remarque : « l'existence est assurée, mais la forme explicite d'une primitive n'est pas toujours connue » (p. 69) | Absent | pr_e1 (une phrase) |

### Présent seulement à l'oral (à mettre à l'écran ou au cahier)

Rien de significatif. La justification « une seule constante k car k₁ + k₂ est encore une constante » est dite dans la voix de pr_l1, mais l'écran porte déjà « Une seule constante k, à la fin ». La primitive de √x ((2/3)x√x) n'est que dans un exercice de fin de pr_u5 (pas à l'écran) : à ajouter comme ligne d'exemple sur pr_u5_b, où ∛x est déjà traité.

### Différences de notation ou de formulation

| Nous | Le professeur (page) | Laquelle garder et pourquoi |
|---|---|---|
| Constante notée k, « k ∈ ℝ » | C, « avec C ∈ ℝ », familles notées F_C, G_C (p. 69–71) | Garder k (cohérent dans tout le cours), mais dire une fois à l'écran (pr_e4_b) « on la note aussi C » : l'élève la verra sous les deux noms. |
| Flèche « f → F » dans les cahiers (pr_u2 à pr_c9, pr_b1) | Phrases « F(x) = … + C » ; « une primitive de u′u² est de la forme (1/3)u³ » (p. 70–71) | Garder la flèche comme aide-mémoire, mais la fiche pr_b1 doit montrer la rédaction de copie : « une primitive de f sur I est F(x) = … » ou « les primitives sont x ↦ … + k, k ∈ ℝ ». Une flèche n'est pas une rédaction acceptée au bac. |
| Définition : « F dérivable sur I et F′(x) = f(x) pour tout x ∈ I » (pr_d2) | « f est une fonction continue sur un intervalle I » en hypothèse (p. 69) | Garder la nôtre : elle est juste et plus générale ; la continuité sert à l'existence (pr_e1), où elle est bien dite. |
| u′uʳ : u > 0 (pr_c5) | u ≠ 0 sur I (p. 70) | Garder u > 0 : uʳ (r rationnel) n'est défini que pour u > 0 (cours ch1). La condition du livre est insuffisante. |
| xʳ sur ]0 ; +∞[ (pr_u5_b) | « ]0 ; +∞[ ou ]−∞ ; 0[ » (p. 70) | Garder ]0 ; +∞[ : même raison (xʳ défini pour x > 0). |
| u′/√u : u > 0 (pr_c7) | « v > 0 sur I » (p. 70) | Garder u > 0 (coquille du livre). |
| √x sur ]0 ; +∞[ (exercice de pr_u5) | I = ℝ⁺ (p. 71, ex. 5) | Les deux sont justes ((2/3)x√x est dérivable en 0) ; garder le nôtre, sans importance. |
| « de la forme u′uⁿ », bulle u, u′ (pr_c2) | « de type u′u² avec u(x) = sin x → u′(x) = cos x » (p. 71) | Équivalent ; garder. |

### Ce que nous avons en plus

Utile et dans le cadre (1.2.14, 1.2.15) :
- Rappels de dérivation (pr_z1 à pr_z5) et rédaction en 3 lignes « vérifier une primitive » (pr_d3, pr_x1) : la question la plus fréquente au national.
- Pourquoi toujours un intervalle, ℝ* n'en est pas un (pr_e2).
- Lecture graphique : courbes translatées (pr_e5), f = pente de F, signe de f ⇒ variations de F (pr_g1, pr_g2).
- 1/xⁿ (pr_u4_b), (ax + b)ⁿ (pr_c4), u′cos u et u′sin u (pr_c9) : absents du tableau du professeur alors qu'ils sont classiques.
- « Il manque un nombre » / « on ne prête qu'un nombre » (pr_c3, pr_c3_b), erreur du produit facteur par facteur (pr_l2), choix par le dénominateur (pr_c8), organigramme (pr_r3).
- Annonce de ln, exp et de l'intégrale (pr_x4).

Hors cadre chez nous : rien (confirmé par l'audit précédent).

### Hors cadre dans le livre (ne pas ajouter)

- 1/(1 + x²) → arctan x et u′/(1 + u²) → arctan u, lignes marquées « SM » (p. 70).
- Exercice 02, cas 10 : x²/(1 + x⁶) → (1/3)arctan(x³) (p. 71, marqué SM).

---

## Fonction logarithme népérien

Sources : notre cours `math_ch5_fonctions_ln.json` (65 diapos), livre Prof Fayssal pages 01-11 = PDF p. 74-84 (page N du livre = PDF p. 73 + N), cadre sciences expérimentales (1.2.14-1.2.19, 1.2.22). Aucune page de ce chapitre n'est marquée « 2 Bac SM ».

### Plan comparé

| Partie du professeur (PDF) | Où chez nous | Remarque |
|---|---|---|
| I.1 Définition : primitive de 1/x sur ]0;+∞[ qui s'annule en 1 (p. 74-75) | ln_partie1 (ln_n1-ln_n4) | Conforme. Le livre écrit aussi ln : ]0;+∞[ → ℝ, x ↦ ln x (absent chez nous). |
| I.2 Propriétés algébriques, corollaires, exemples (p. 75-76) | ln_partie4 (ln_a1-ln_a8) | Conforme. Chez nous la partie vient après le domaine et la courbe : ça ne gêne pas. |
| Remarque : valeurs absolues pour x, y < 0 ; ln x²ⁿ = 2n ln\|x\| (p. 76) | ln_a6_b (seulement ln x² = 2 ln\|x\|) | Partiel. |
| I.3 Équations, inéquations, signe de ln, Ex. 01-02 (p. 76-77) | ln_c2, ln_c4, ln_partie3, ln_partie5 | Conforme, et nous avons plus (systèmes, plus petit n). |
| I.4 Limites : bornes, croissances comparées avec xⁿ, limite en 1, formes indéterminées, Ex. 03 (p. 77-78) | ln_partie6 (ln_l1-ln_l8) | Il manque le cas xⁿ, le changement X = 1/x et la composée ln(u). |
| I.5 Étude de ln : domaine, variations, tableau, tangente en 1, branches infinies, nombre e (p. 79) | ln_partie2 (ln_c1-ln_c5) + ln_l1, ln_l2 | Chez nous ces éléments sont répartis entre deux parties et le tableau de variations complet de ln n'est jamais dressé. |
| I.6 Courbe de ln (p. 79) | figures de ln_c1, ln_l1, ln_l2 | Conforme. |
| Ex. 04 : domaines (ln au dénominateur, √(2 − ln x)), équation et inéquation en ln²x (p. 79-80) | ln_d3, ln_q4 | Il manque l'inéquation en ln²x. |
| Ex. 05 : variations et convexité de 3 − x + 2 ln x (p. 80) | — | Absent : pas de f″ ni de concavité dans le chapitre. |
| Ex. 06 : position de la courbe de ln et de la droite y = x (p. 81) | ln_e1 (ln x ≤ x − 1) | Équivalent. |
| 6) Dérivée de ln\|u\| (u ≠ 0) avec démonstration et exemple ln(2x − x²) (p. 81) | ln_partie7 (ln_v1-ln_v3) | Chez nous seulement u > 0. |
| Ex. 05 (bis) : étude complète de ln((x+2)/(1−x)) : domaine, limites par composition, asymptotes, f′, unique solution α, tracé (p. 81-82) | — | Absent : toutes nos études utilisent ln x, jamais ln(u(x)). |
| Ex. 08 : 0 ≤ ln(1+x) ≤ x et suite par gendarmes (p. 82) | ln_e1 (même inégalité, sans suite) | Partiel. |
| Primitives u′/u → ln\|u\| + c, Ex. 09 (p. 83) | ln_partie8 (ln_p1-ln_p3) | Il manque 1/(x ln x). |
| II.1 Logarithme de base a (p. 84) | — | Hors cadre. |
| II.2 Logarithme décimal (p. 84) | ln_partie10 (ln_g1, ln_g2) | Conforme, et nous avons plus (10ˣ = a, pH). |
| — | ln_ouverture (rappels), ln_partie9 (problèmes du national), ln_bilan | En plus chez nous. |

### Manques

| Priorité | Catégorie | Ce que dit le professeur (page du PDF) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | méthode | Limite de ln(u(x)) par composition : lim (x+2)/(1−x) = 0⁺ quand x → −2⁺, donc lim f = −∞ ; puis la phrase « la courbe admet deux asymptotes verticales d'équations x = −2 et x = 1 » (p. 81) | Absent. Aucune limite de ln(u) : toutes les limites portent sur ln x. | Nouvelle diapo après ln_l2 (ln_partie6) |
| haute | exemple / structure | Étude complète d'une fonction ln(u) : f(x) = ln((x+2)/(1−x)) (domaine par tableau de signe, limites aux bornes, f′ = u′/u > 0, tableau de variations, unique α, tracé) (p. 81-82) | Absent. Nos études (ln_e3-ln_e5_c) portent seulement sur des fonctions de ln x. | ln_partie9, nouvelle diapo ln_e6 |
| haute | méthode | Ex. 05 : f″(x) = −2/x² < 0, donc f est concave sur ]0;+∞[ (p. 80). Le cadre 1.2.22 demande la concavité et les points d'inflexion. | Absent du chapitre : aucune occurrence de f″, concave, convexe ni inflexion. | ln_partie9, après ln_e3_b |
| haute | formule | Croissances comparées : pour tout n ∈ ℕ*, lim_{x→+∞} (ln x)/xⁿ = 0 et lim_{x→0⁺} xⁿ ln x = 0 (p. 77) | Seulement n = 1 (ln_l3, ln_l4, ln_b1). | ln_l3 et ln_l4 (une ligne chacune), fiche ln_b1 point 5 |
| moyenne | méthode | Unique solution α de f(x) = 0 avec ln : f continue et strictement croissante sur [−1;0], f(−1) × f(0) < 0 (p. 82) | Absent : aucun α dans le chapitre (le théorème des valeurs intermédiaires est vu au ch1 mais jamais réutilisé avec ln). | Dans la nouvelle ln_e6 |
| moyenne | structure / formule | Tableau de variations complet de ln : 0 avec double barre, (ln x)′ = 1/x de signe +, flèche de −∞ à +∞ (p. 79) | Absent : croissance (ln_c1) et limites (ln_l1, ln_l2) ne sont jamais réunies dans un tableau. | Fin de ln_l2, ou ln_b1 |
| moyenne | propriété | ln est continue et strictement croissante sur ]0;+∞[, donc ln x = 1 admet une unique solution, notée e (p. 79) | ln_c3 : « un seul point », justifié seulement à l'oral par « ln monte toujours ». La continuité de ln n'est jamais écrite. | ln_c3 (bullet) et ln_n4 (ln dérivable donc continue) |
| moyenne | méthode | Changement de variable X = 1/x : lim x ln(1 + 1/x) = lim ln(1+X)/X = 1 ; aussi X = ∛x pour x(ln x)³ (p. 78) ; démonstration de lim_{0⁺} ln x = −∞ en posant X = 1/x (p. 77) | Seulement t = √x (ln_l7). | ln_partie6, après ln_l7 |
| moyenne | méthode | Inéquation (ln x)² − 3 ln x + 2 < 0 : factoriser (ln x − 1)(ln x − 2), tableau de signe, S = ]e ; e²[ (p. 80) | ln_q4 traite seulement l'équation. | ln_q4 (bullet ou exercice de fin) |
| moyenne | formule | Primitive de 1/(x ln x) : forme u′/u avec u = ln x, F(x) = ln\|ln x\| + C ; sur ]0;1[, ln(−ln x) + C (p. 83) | Absent. | ln_p2 |
| moyenne | formule | Cadre 1.2.18 (le livre ne le traite pas) : inéquations 10ˣ ≤ a et 10ˣ ≥ a | Seulement l'équation 10ˣ = a (ln_g2). | ln_g2 |
| moyenne | notation | Quantificateur (∀x ∈ ]0;+∞[) partout, y compris dans les énoncés (p. 74-83) | Aucun « ∀ » dans le chapitre : nous écrivons « pour tout x > 0 ». | Traces de ln_c1, ln_e1, ln_p3 |
| basse | notation | Ensemble de définition de l'équation noté D_E (D_I pour une inéquation) ; « On note S l'ensemble des solutions … Donc S = {…} » (p. 76-77) | Nous écrivons « le domaine : … » sans nom ; S est écrit (ln_q3-ln_q6). | ln_q1, ln_q1_b |
| basse | propriété | (ln\|u\|)′ = u′/u sur I si u est dérivable et ne s'annule pas sur I, avec démonstration (p. 81) | ln_v1 donne seulement le cas u > 0 ; ln\|u\| n'apparaît que pour les primitives (ln_p2). | ln_v1 |
| basse | formule | x, y < 0 : ln(xy) = ln\|x\| + ln\|y\| ; ln(x/y) = ln\|x\| − ln\|y\| ; ln x²ⁿ = 2n ln\|x\| (p. 76) | Seulement ln(x²) = 2 ln\|x\| (ln_a6_b). | ln_a6_b |
| basse | définition / notation | ln : ]0;+∞[ → ℝ, x ↦ ln x ; D_ln = ]0;+∞[ (p. 74, 79) | La définition est donnée en phrase seulement. | ln_n3 |
| basse | méthode (démonstration) | ln xⁿ = n ln x par récurrence, puis n ∈ ℤ, 1/n, r ∈ ℚ (p. 74-75) ; encadrement 0 < ln x ≤ 2√x pour démontrer lim (ln x)/x = 0 (p. 77) | Illustrations seulement (« n blocs » dans ln_a4, tableau de valeurs dans ln_l3) ; r ∈ ℚ admis. | Optionnel : ln_a4, ln_l3 |
| basse | formule | Rappel des formes indéterminées 0/0, ∞/∞, 0 × ∞, +∞ − (+∞) (p. 77) | Les formes sont nommées au cas par cas (ln_l4 à l'oral, ln_l6 à l'oral, ln_l7), sans liste. | Début de ln_partie6 |
| basse | exemple | A = ln(√6 − √5) + ln(√6 + √5) = 0 (quantité conjuguée) ; C = ln(5/3) + ln(3/7) + ln(7/5) = 0 (p. 75) | Absent. | Exercices de fin de ln_a5 |
| basse | exemple | Ex. 08 : 0 ≤ ln(1+x) ≤ x, puis encadrement d'une suite Uₙ = ln(1 + 2/(n−1)) et théorème des gendarmes (p. 82) | ln_e1 donne ln x ≤ x − 1, sans application aux suites. | Exercice de fin de ln_e1 |
| basse | propriété | e est irrationnel (p. 79) | Absent. | ln_c3 (à l'oral suffit) |

### Présent seulement à l'oral (à mettre à l'écran ou au cahier)

- ln_l6 : la factorisation x − ln x = x(1 − (ln x)/x) et la conclusion +∞ ne sont que dans la voix. L'écran n'a pas de bullets ; la trace dit seulement « on factorise par x ».
- ln_c3 : la raison de l'unicité de e (« car ln monte toujours ») n'est donnée qu'à l'oral. À écrire avec « continue et strictement croissante ».
- ln_e5_b : le calcul f′(x) = 2 ln x + 2x × 1/x − 2 = 2 ln x n'est que dans la voix (l'écran donne le résultat).
- ln_e5_c : « −2 est le minimum, donc f(x) ≥ −2 » et « on divise par 2x > 0 » ne sont que dans la voix : ce sont les deux justifications attendues.
- ln_e3 : f(1) = 1 + ½ = 3/2 est calculé seulement à l'oral.
- ln_l2 : « la courbe ne coupe pas l'axe des ordonnées car 0 ∉ ]0;+∞[ » n'est qu'à l'oral.

### Différences de notation ou de formulation

| Nous | Le professeur | À garder |
|---|---|---|
| « pour tout x > 0 » | (∀x ∈ ]0;+∞[) | Les deux : ∀ est la forme des énoncés du bac, il faut la lire et l'écrire. |
| « le domaine », D_f | D_f pour une fonction, D_E / D_I pour une équation ou une inéquation | Garder D_f ; ajouter D_E / D_I pour les équations (rédaction en trois temps : D_E, résolution, S). |
| (C), « la courbe de ln » | (C_f), (Cf) | Garder (C), comme les sujets nationaux ; dire une fois que (C_f) désigne la même chose. |
| (ln x)², ((ln x)²)′ | ln²(x) (p. 79-80) | Garder (ln x)², plus sûr ; dire que ln²x = (ln x)² et que ce n'est pas ln(x²). |
| « une primitive est ln u » (ln_p1, ln_p2) | « les primitives sont ln\|U(x)\| + c ; c ∈ ℝ » (p. 83) | Écrire « + C, C ∈ ℝ » quand la question demande « les primitives ». |
| (ln x)′ = 1/x | ln′(x) = 1/x | Les deux : ln′(1) est déjà utilisé dans ln_c5. |
| lim_{x→0⁺} | lim_{x→0⁺}, ou x → −2 avec x > −2 écrit sous la limite (p. 81) | Garder 0⁺ ; montrer une fois l'écriture « x > a » sous la limite. |
| Phrase type « la droite d'équation x = 0 est asymptote verticale à (C) » ; « branche parabolique de direction l'axe des abscisses » | Mêmes phrases (p. 79, 81) | Déjà conformes. |
| Erreurs du livre à ne pas copier : « ∀x ∈ [0;+∞[ : 0 < ln(1+x) < x » est faux en 0, il faut x > 0 ou ≤ (p. 82) ; « log_a(1) = ln(e)/ln(a) » au lieu de log_a(e) (p. 84) ; « log_a(xy) = log_a(x) + ln(y) » (p. 84) | — | — |

### Ce que nous avons en plus (utile, dans le cadre)

- Rappels de prérequis (ln_z1-ln_z5) et une construction de ln mieux motivée (ln_n1 : la règle des puissances échoue pour 1/x).
- Domaine de ln|u| (ln_d4), domaine avec quotient (ln_d2), pièges ln(a + b) (ln_a6), « trouve l'erreur » (ln_a7).
- Systèmes logarithmiques (ln_q6, cadre 1.2.17, absents du livre) ; plus petit entier n avec qⁿ < a (ln_q7).
- Continuité à droite et demi-tangente verticale en 0 (ln_l8, ln_e5) ; limite déguisée avec t = √x (ln_l7, national 2023).
- Problèmes du national : fonction auxiliaire g de la partie I (ln_e2), études 2019 et 2021 (ln_e3-ln_e5_c), position par rapport à y = x (ln_e4), vérifier une primitive H (ln_p3).
- 10ˣ = a ⇔ x = log a et le pH (ln_g2, cadre 1.2.18).
- Bilan et carte (ln_b1, ln_b2).

### Hors cadre dans le livre (ne pas ajouter)

- Logarithme de base a (log_a), ses propriétés, l'Ex. 10 (log_a(b) = 1/log_b(a), équations en log₃, log₅, log_x(2)) (p. 84) : le cadre ne cite que ln et le logarithme décimal (1.2.18), et l'audit précédent l'a retiré exprès.
- Décomposition (5x+1)/(x² + x − 2) = a/(x−1) + b/(x+2), avec un système en a et b, et division euclidienne de x³ + x + 4 par x + 1 (Ex. 09 c-d, p. 83) : les « éléments simples » sont classés hors cadre dans l'audit du ch4. À traiter seulement si l'énoncé donne la forme (« vérifier que f(x) = … »).

---

## Nombres complexes (partie 1)

Sources : notre cours `math_ch6_nombres_complexes` (écran, cahier, voix, exercices, réactions préparées du JSON) ; livre Prof Fayssal, « Cours : Nombres complexes (I) », PDF p. 86 (Page 01) à p. 100 (Page 15) (p. 85 = couverture ; Page N = p. 85 + N) ; cadre officiel 2.4.1, 2.4.2, 2.4.4, 2.4.7 ; fiches `operations_formes` (cadre_reference_2bac_pc.json) et `operations_formes` / `geometrie_complexe` (perimetre.json).

Remarque générale : la fiche `operations_formes` renvoie **exprès** à la partie 2 « la mesure des angles et l'orthogonalité (2.4.4) ». Le professeur, lui, les met dans la partie I (VI, p. 99-100). La partie 2 n'existe pas encore et `nc_b2_carte` ne les annonce pas (elle annonce seulement exponentielle, équation, rotation). Les manques H1 à H3 ci-dessous sont donc à traiter dans la partie 2 si on garde ce choix, mais il faut les y garantir.

### Plan comparé

| Partie du professeur (page PDF) | Où chez nous | Remarque |
|---|---|---|
| I.1 Introduction : x² = 2 sans solution dans ℚ, x² = −2 sans solution dans ℝ (p. 86) | nc_a1, nc_a2 | Même idée (x² = −1). |
| I.2 Définition-théorème (admis) de ℂ : contient ℝ, mêmes règles de calcul, i² = −1, écriture unique (p. 86) | nc_a2, nc_a3 | Présent. |
| Exercice 1 : x² + x + 1 = 0 avec i (p. 86) | — | Équation du second degré : partie 2 (2.4.8), pas un manque ici. |
| I.3 Forme algébrique, Re, Im, imaginaire pur, notation iℝ ; remarques (a ± ib)², (a + ib)(a − ib) (p. 86) | nc_a3, nc_a4, nc_c2, nc_c3 | Présent sauf la notation iℝ et la formule générale (a + ib)² (voir Manques). |
| I.4 Opérations : égalité, z = 0, caractérisation réel / imaginaire pur, somme, produit, inverse « si z ≠ 0 » ; Ex. 2 et 3 (j) (p. 87) | nc_a4, nc_a5, nc_c1 à nc_c4, nc_a6 | Présent ; la condition z ≠ 0 et l'exemple j manquent. Nous avons en plus les puissances de i. |
| II.1 Repère orthonormé direct, affixe d'un point, d'un vecteur, plan complexe, axe des réels / des imaginaires purs ; Ex. 4 (p. 88) | nc_p1, nc_p2 | Présent. |
| II.2 Prop. 01 (MN, u + v, ku, milieu) avec démonstration ; Prop. 02 alignement ; Prop. 03 parallélisme ; Prop. 04 barycentre ; Ex. 5, 6 (parallélogramme) (p. 89) | nc_p3, nc_p4, nc_i1 | Milieu, vecteur, alignement présents. Parallélisme, parallélogramme, affixe de ku absents. Barycentre : hors cadre. |
| II.3 Conjugué : définition, interprétation (symétrie), Ex. 7 (équations avec z̄), Prop. 1 z·z̄, Ex. 8 (p. 90) | nc_c3, nc_j1, nc_j4 | Présent, sauf la résolution d'équations avec z̄ (Ex. 7). |
| Prop. 2 et 3 du conjugué (double conjugué, z ± z̄, conj. d'opérations, conj(kz) = k z̄) ; Ex. 9, 10 (ensembles « ∈ ℝ / ∈ iℝ ») (p. 91) | nc_j2, nc_j3, nc_j3_b | Double conjugué, conj(kz), ensembles de points absents. |
| III.1 Module : définition, Prop. 01 et 02 (tableau produit, puissance, inverse, quotient, inégalité triangulaire), démonstrations, remarques, AB = \|z_B − z_A\| ; Ex. 11 (p. 92) | nc_m1 à nc_m4, nc_r3 | Présent, sauf \|z\| = 0 ⇔ z = 0, inégalité triangulaire ; \|−z\| seulement dans une correction. |
| Ex. 12 ; Prop. 04 ensembles (cercle, disques, médiatrice) ; Ex. 13, 14 (p. 93-94) | nc_m4, nc_i1 | Ensembles de points absents (voir H4). |
| III (forme trigo) 1 : argument, 2kπ, 0 sans argument, cas particuliers ℝ*₊, ℝ*₋, iℝ*₊, iℝ*₋, arg z̄, arg(−z) ; Ex. 15 (p. 95) | nc_g1, nc_g2, nc_g3, nc_r3, nc_r3_b | Présent ; écriture « θ + 2kπ, k ∈ ℤ » absente. |
| 2 Opérations sur l'argument ; Ex. 16 ; 3 forme trigonométrique, a = \|z\| cos θ, b = \|z\| sin θ, notation [\|z\|, θ] ; Ex. 17 (p. 96) | nc_g4, nc_g4_b, nc_t1 à nc_t6, nc_r1 à nc_r4 | Présent. Chez nous la forme trigo vient avant les opérations sur l'argument : ordre sans gêne. |
| 4 Opérations sur la forme trigonométrique + démonstration ; Moivre (n ∈ ℤ) ; égalité z = z′ ⇔ même module et même argument (p. 97) | nc_r1, nc_r3, nc_r3_b, nc_r6 | Égalité sous forme trigonométrique absente. |
| Ex. 18, 19 (a/b, cos π/12, a²⁰²² ∈ ℝ) (p. 98) | nc_r5, nc_r7, nc_r8, nc_n2 | Équivalent présent (cos 5π/12, puissances réelles). |
| VI Applications à la géométrie : (u, AB) ≡ arg(z_B − z_A), (AB, AC) ≡ arg((z_C − z_A)/(z_B − z_A)), parallèles, perpendiculaires, colinéaires, orthogonaux, cocycliques ; Ex. 20 (isocèle rectangle) (p. 99) | — | **Partie absente** (renvoyée à la partie 2 par la fiche). |
| Ex. 21 (équilatéral), Ex. 22 (ensembles arg), Ex. 23 (cocycliques) (p. 100) | — | Absents. |
| — | Ouverture nc_o1, rappels nc_z1 à nc_z5, quadrants nc_t3/_b, fausses formes nc_t4/_b, sujets nationaux nc_n1, nc_n2, bilan nc_b1, carte nc_b2 | En plus chez nous. |

### Manques

| Priorité | Catégorie | Ce que dit le professeur (page du PDF) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | propriété / méthode | Mesure d'angle : (u, AB) ≡ arg(z_B − z_A) [2π] ; (AB, AC) ≡ arg((z_C − z_A)/(z_B − z_A)) [2π] ; (AB, DC) ≡ arg((z_C − z_D)/(z_B − z_A)) [2π], pour A ≠ B, C ≠ D (p. 99) | Absent (cadre 2.4.4 « mesure des angles » ; renvoyé à la partie 2 par la fiche) | Partie 2 (à garantir) ou nouvelle diapo nc_i3 après nc_i1 ; l'annoncer dans nc_b2_carte |
| haute | méthode / exemple | Nature d'un triangle : (c − a)/(b − a) = −i ⇒ \|c − a\|/\|b − a\| = 1 et (AB, AC) ≡ −π/2 [2π] ⇒ AC = AB ⇒ « le triangle ABC est isocèle et rectangle en A » ; quotient de module 1 et d'argument ±π/3 ⇒ équilatéral (p. 99 Ex. 20, p. 100 Ex. 21) | Absent (perimetre `geometrie_complexe` : démonstration attendue) | Partie 2 ou nc_i3 (même diapo que la ligne précédente) |
| haute | propriété | Orthogonalité / parallélisme : (AB) ⊥ (CD) et (AB) // (CD) traduits par le quotient (z_D − z_C)/(z_B − z_A) imaginaire pur / réel (p. 89 Prop. 03, p. 99 Prop. 03, 3 et 4) | Absent du cours ; dit seulement dans les réactions préparées du rappel K8_r1 (« imaginaire pur ⇒ perpendiculaires ») | Partie 2 ou nc_i3 ; cadre 2.4.4 « orthogonalité de vecteurs » |
| haute | propriété / méthode / notation | Ensembles de points : \|z − z_A\| = r ⇒ cercle de centre A et de rayon r ; \|z − z_A\| = \|z − z_B\| ⇒ médiatrice de [AB] ; transformer d'abord (\|iz − 3\| = \|z + 3i\|, \|z̄ − 3 + i\| = \|z − (3 + i)\|) ; phrase type « L'ensemble des points M est le cercle de centre A(2i) et de rayon 3 » ; 2e méthode z = x + iy (p. 93 Prop. 04 et Ex. 13, p. 94) | Absent (seulement « les points d'un cercle de centre O ont tous le même module », écran nc_m2) ; perimetre `geometrie_complexe` : « déterminer et représenter un ensemble de points » attendu | Nouvelle diapo nc_m5 après nc_m4 |
| haute | notation | Vecteurs avec flèche : AB⃗ = k AC⃗, z_{AB⃗}, (u⃗, OM⃗), repère (O, u⃗, v⃗) (p. 88, 89, 95, 99) | Aucune flèche dans tout le JSON : « A, B, C alignés ⇔ AC = k·AB » (nc_i1) se lit comme des longueurs ; « Vecteur AB(xB − xA ; …) » (nc_z2_vecteur), « (u, OM) » (nc_g1), « z_AB » (nc_p3) | nc_z2_vecteur, nc_p1, nc_p3, nc_g1, nc_i1, nc_b1_bilan (écran et cahier) |
| moyenne | propriété (hypothèses) | Conditions de non-nullité écrites : « Si z ≠ 0 » pour 1/z (p. 87) ; conj(z/z′) « (z′ ≠ 0) » (p. 91) ; « z et z′ non nuls » pour \|z/z′\|, arg(1/z), arg(z/z′) (p. 92, 96) | Écrit seulement sur nc_r1 et nc_b1_bilan. Absent sur nc_c4 (quotient, pas de « c + id ≠ 0 »), nc_j2 (conj(z/z′)), nc_m3_b (\|z/z′\|), nc_r3 (1/z, arg z̄), nc_r3_b (arg(z/z′), arg(−z)) | nc_c4, nc_j2, nc_m3_b, nc_r3, nc_r3_b (écran et cahier) |
| moyenne | méthode | Résoudre dans ℂ une équation avec z̄ : « On pose z = x + iy, (x, y) ∈ ℝ² », regrouper partie réelle et imaginaire, système, conclure « Donc S = {3 − i} » ; ou conjuguer les deux membres (z̿ = z) (p. 90 Ex. 7) | Absent : nc_a5 traite une égalité où x et y sont déjà donnés ; jamais « résoudre dans ℂ », jamais « S = {…} » | Nouvelle diapo après nc_j3_b (ou exemple 2 de nc_a5) |
| moyenne | méthode | Ensemble des points M tels qu'une expression soit réelle / imaginaire pure : poser z = x + iy, écrire la condition Re = 0 ou Im = 0, conclure droite / cercle « privé du point A d'affixe −1 » (condition z ≠ −1) (p. 91 Ex. 9, 10) | Absent (perimetre `geometrie_complexe`, méthode « écrire z = x + iy et traduire une condition ») | Avec nc_m5 (ligne ensembles) ou partie 2 |
| moyenne | méthode / exemple | Parallélogramme ABCD : z_B − z_A = z_C − z_D (AB⃗ = DC⃗) ; centre = milieu de [AC] ; alignement D, C, E par z_DE = −2 z_DC (p. 89 Ex. 6) | Absent (seulement « z + z′ : diagonale du parallélogramme construit sur OM et OM′ », écran nc_p3) ; perimetre : « montrer qu'un quadrilatère est un parallélogramme » attendu | Nouvelle diapo après nc_p4 |
| moyenne | propriété | Égalité sous forme trigonométrique : z = z′ ⇔ \|z\| = \|z′\| et arg z ≡ arg z′ [2π] (p. 97) | Absent (nc_r5 identifie seulement les parties réelles) | nc_t5 ou nc_r5 |
| moyenne | notation | « Un complexe non nul a une infinité d'arguments arg z + 2kπ, k ∈ ℤ » ; « une mesure, en radians » (p. 95) | nc_g2 : « θ, θ + 2π et θ − 2π » ; ni k ∈ ℤ, ni radians | nc_g2 (écran et cahier) |
| moyenne | propriété | Double conjugué z̿ = z ; conj(kz) = k z̄ pour k réel (p. 91) ; utilisés dans Ex. 7 et 13 | Absents (seulement conj(iz) = −i z̄ dans un vrai/faux de nc_j2) | nc_j2 |
| basse | formule | (a + ib)² = a² − b² + 2abi ; (a − ib)² = a² − b² − 2abi (p. 86) | Seulement (1 ± i)² et (a + b)² (nc_c2, nc_z5_identites) | nc_c2 |
| basse | propriété | \|z\| = 0 ⇔ z = 0 ; Re(z) ≤ \|z\| et Im(z) ≤ \|z\| ; inégalité triangulaire \|z + z′\| ≤ \|z\| + \|z′\| (p. 92) | Absents ; nc_m3_b dit seulement \|z + z′\| ≠ \|z\| + \|z′\| (non exigés par la fiche NC5 : une ligne suffit) | nc_m3_b |
| basse | propriété | Affixe de k·u⃗ (k réel) : kz ; affixe de u⃗ + v⃗ : z + z′ (p. 89 Prop. 01 b, c) | kz absent ; z + z′ seulement à l'écran de nc_p3 | nc_p3 (cahier) |
| basse | notation | iℝ = {ib / b ∈ ℝ}, « z ∈ iℝ ⇔ z̄ = −z », ℝ*₊, iℝ*₊ (p. 86, 91, 95) | En mots seulement (« imaginaire pur ») ; iℝ apparaît seulement dans un visuel scripté de nc_j3_b | nc_a4, nc_j3_b, nc_g3 |
| basse | notation | Domaine de n : \|zⁿ\| = \|z\|ⁿ pour n ∈ ℕ* (p. 92) ; Moivre « pour tout n ∈ ℤ » (p. 97) | n jamais précisé (nc_m3_b, nc_r6) | nc_m3_b, nc_r6 |
| basse | exemple | j = −1/2 + i√3/2 : j² + j + 1 = 0, j³ = 1, j²⁰²³ = j (p. 87 Ex. 3) — sans parler de « racine cubique de l'unité » (hors cadre) | Absent | Exercice de fin de nc_a6 ou nc_c2 |
| basse | exemple | Placer un point connaissant module et argument (\|z_D\| = 2, arg z_D ≡ −2π/3 [2π]) (p. 95 Ex. 15) | Absent | Exercice de fin de nc_g3 |

### Présent seulement à l'oral (à mettre à l'écran ou au cahier)

- **Perpendiculaire ⇔ quotient imaginaire pur** : dit seulement dans les réactions préparées du rappel K8_r1 (« un quotient imaginaire pur correspond à des droites perpendiculaires ») ; jamais enseigné (voir manque H3).
- **« Plan complexe »** (nc_p1) : le mot est dans le titre et la voix (« C'est le plan complexe »), pas dans les puces ni au cahier. Le professeur le définit (p. 88).
- **z = 0 ⇔ Re(z) = 0 et Im(z) = 0** : seulement dans un vrai/faux de nc_a5 ; le professeur l'écrit comme propriété (p. 87). À mettre au cahier de nc_a5.
- **|−z| = |z|** : seulement dans la correction d'un vrai/faux de nc_m4 ; propriété du professeur (p. 92). À mettre au cahier de nc_m2 ou nc_m3_b.
- **Écran seulement, pas au cahier** : « z + z′ : diagonale du parallélogramme » (nc_p3) ; « les points d'un cercle de centre O ont tous le même module » (nc_m2) ; « zⁿ réel quand nθ multiple de π, imaginaire pur quand nθ = π/2 + kπ » (nc_r7) ; sens positif inverse des aiguilles d'une montre (nc_g1).

### Différences de notation ou de formulation

| Nous | Le professeur | Laquelle garder et pourquoi |
|---|---|---|
| conj(z + z′), conj(zz′), conj(zⁿ) (nc_j2, écran et cahier) | Grande barre sur z + z′, z × z′, zⁿ (p. 91) | **La barre** : c'est l'écriture de la copie au bac ; « conj( ) » n'existe pas au Maroc. Garder « conj » au plus à l'oral. |
| AB, (u, OM), z_AB sans flèche | AB⃗, (u⃗, OM⃗), z_{AB⃗}, (O, u⃗, v⃗) | **La flèche** (voir manque haute) : sans elle, AC = k·AB est faux (longueurs). |
| z = r(cos θ + i sin θ) partout | Aussi la notation simplifiée z = [r, θ] (p. 96-98) | **La nôtre** : le national écrit la forme complète (barème 2023 N, nc_t2). [r, θ] peut être cité à l'oral pour que l'élève la reconnaisse en classe. |
| θ + 2π, θ − 2π (nc_g2) | arg z + 2kπ, k ∈ ℤ (p. 95) | **Le professeur** : forme générale attendue. |
| « axe imaginaire » | « axe des imaginaires purs », « axe des réels » (p. 88) | Les deux sont justes ; garder la nôtre, citer celle du professeur une fois sur nc_p1. |
| « a et b réels » | « (a, b) ∈ ℝ² » / « (x, y) ∈ ℝ² » (p. 88, 90) | Les deux ; ajouter (x, y) ∈ ℝ² dans la méthode « poser z = x + iy ». |
| Alignement : « pour A ≠ B » | « A, B, C distincts deux à deux » (p. 89) | La nôtre suffit avec (c − a)/(b − a) ; rien à changer. |
| Parallèle / perpendiculaire « ≡ 0 [π] », « ≡ π/2 [π] » | (p. 99, 100 Ex. 22.1) | **Ni l'une ni l'autre telle quelle** : perimetre `geometrie_complexe` classe « modulo π » hors programme ; dire « le quotient est réel / imaginaire pur », ou ≡ ±π/2 [2π]. |
| Propriétés du module et de l'argument admises, justifiées par la figure (nc_m3, nc_r1) | Démontrées (z·z̄, \|zⁿ\| par récurrence, produit par cos(θ + θ′)) (p. 92, 97) | **La nôtre** est conforme (perimetre : propriétés « admises ») ; la démonstration par récurrence peut rester facultative. |

### Ce que nous avons en plus

Utile, dans le cadre :
- Rappels de départ (repère, vecteur, Pythagore, cercle trigonométrique, identités) nc_z1 à nc_z5.
- Puissances de i par cycle de 4 et regroupement i²ᵏ = (−1)ᵏ (nc_a6) ; « 0 est à la fois réel et imaginaire pur » (nc_a4).
- Règle des quadrants θ, π − θ, π + θ, −θ (nc_t3, nc_t3_b) et tableau des angles remarquables (nc_g4_b).
- Fausses formes trigonométriques corrigées (r < 0, « − cos ») (nc_t4, nc_t4_b).
- Critère « zⁿ réel / imaginaire pur » avec Moivre (nc_r7, nc_r8, nc_n2).
- Égalité de distances ΩA = ΩB par symétrie (nc_i2).
- Rédaction au barème et sujets nationaux 2017 à 2025 (nc_t2, nc_t6, nc_r4, nc_n1, nc_n2), vérification systématique, bilan et carte (nc_b1, nc_b2).

Hors cadre : rien (conforme à l'audit précédent).

### Hors cadre dans le livre (ne pas ajouter)

- Affixe du barycentre de (A ; α), (B ; β) (p. 89 Prop. 04) : retiré exprès (audit précédent).
- Points cocycliques et critère du quotient réel (p. 99 Prop. 03.5, p. 100 Ex. 23) : retiré exprès (audit précédent).
- Ensemble \|z − i\| = 2\|z\| (cercle d'Apollonius, p. 94 Ex. 13.4) : retiré exprès (audit précédent, k ≠ 1).
- Disque ouvert / fermé \|z − z_A\| < r, ≤ r (p. 93 Prop. 04) : la fiche ne garde que cercle et médiatrice.
- Angles de droites « modulo π » (p. 99, p. 100 Ex. 22.1) : hors programme selon perimetre (garder le contenu, pas la notation).
- Bijection f : ℂ → (P), « ∃! Z » (p. 88) et Ex. 14 (u ∉ ℝ, \|1 + uz\| = \|1 + ūz\| ⇒ z ∈ ℝ, p. 94) : formalisme et exercice de niveau 2 Bac SM.
- Exercice 1 (x² + x + 1 = 0, p. 86) : au cadre (2.4.8), mais en partie 2.

---

