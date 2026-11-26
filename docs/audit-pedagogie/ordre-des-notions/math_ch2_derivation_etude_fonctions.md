# math_ch2_derivation_etude_fonctions

## Ordre proposé des premières notions
1. Pente d'une droite (coefficient directeur) — diapo 3 (bonne porte d'entrée, à garder en premier).
2. Équation d'une droite y = ax + b — diapo 9 (à remonter juste après la diapo 3 : la question de bloc après la diapo 4 en a besoin).
3. Rappel : limite d'un quotient, forme indéterminée 0/0, factoriser un polynôme par (x − x₀), identité (a − b)(a + b) = a² − b² — absent (à ajouter avant la diapo 7).
4. Sécante et taux d'accroissement — diapo 4.
5. M se rapproche de A : limite du taux — diapo 5.
6. Nombre dérivé, dérivabilité, tangente — diapo 6 (la forme en h à part, plus tard).
7. Calcul du nombre dérivé (polynôme, puis conjugué) — diapos 7-8.
8. Rappel dérivées usuelles (polynôme, 1/x) et notion de fonction dérivée f′(x) — diapos 21-22 et 28 (à placer AVANT la diapo 11, qui calcule f′(x) = 1 − 1/x²).
9. Équation de la tangente — diapos 10-12.

## Défauts
| # | Diapo | Type (1 notion avant / 2 trop vite / 4 question tôt) | Ce qui est dit (citation courte) | Pourquoi ça perturbe | Correction proposée (déplacer, ajouter un rappel avant la diapo N, reformuler…) | Gravité (forte/moyenne) |
|---|---|---|---|---|---|---|
| 1 | 11 (et 10, 12) | 1 notion avant | « f prime de x égale un moins un sur x au carré » | La fonction dérivée f′(x) et la dérivée de 1/x sont utilisées alors que (xⁿ)′, (1/x)′ ne sont rappelées qu'aux diapos 21-22 et la « fonction dérivée » définie qu'à la diapo 28. Jusque-là l'élève ne sait calculer f′(x₀) que par la limite du taux. La pente 3/4 de la diapo 10 tombe donc du ciel. | Déplacer les rappels 21-22 (dériver un polynôme, 1/x) et la définition de la fonction dérivée (fin de la diapo 28) avant la diapo 10 ; ou bien, aux diapos 10-12, calculer f′(2) par la limite du taux. | forte |
| 2 | bloc après 4 | 4 question tôt | « Dans y = ax + b, que représente a ? » | y = ax + b n'est enseigné qu'à la diapo 9. | Déplacer cette question après la diapo 9 (ou la diapo 9 avant la diapo 4). | forte |
| 3 | bloc après 17 | 4 question tôt | « Cahier fermé : dérive 3x² − 5x + 4 » | Dériver un polynôme n'est vu qu'à la diapo 21 ; « cahier fermé » suppose une notion déjà écrite. | Déplacer après la diapo 21 (bloc df_n2_b1 mal placé). | forte |
| 4 | bloc après 17 | 4 question tôt | « Sur quel intervalle (x − 1)(x + 1) est-il négatif ? » | Le signe d'un produit (tableau de signe) n'est rappelé qu'à la diapo 33. | Déplacer après la diapo 33. | forte |
| 5 | bloc après 76 | 4 question tôt | « Pourquoi f admet-elle un minimum en −2/3 ? » | La valeur −2/3 et le signe de f′ de x√(x + 1) n'apparaissent qu'aux diapos 78-79 ; à la diapo 76 on n'a fait que l'ensemble de définition. | Déplacer cette question après la diapo 79. | forte |
| 6 | 8 | 1 notion avant | « On multiplie en haut et en bas par le conjugué » | « Conjugué » et (a − b)(a + b) = a² − b² (collège / tronc commun) ne sont jamais rappelés ; la question de la même diapo porte dessus après un seul exemple. | Ajouter avant la diapo 8 un rappel : identités remarquables, (√A − B)(√A + B) = A − B², avec un exemple numérique. | moyenne |
| 7 | 7 | 1 notion avant | « Polynôme : on factorise par x − 1, il reste x + 1 » | Factoriser un polynôme par (x − x₀) quand x₀ est racine (1ʳᵉ Bac) et la forme indéterminée 0/0 (chap. 1) sont supposés sus. L'exercice de la diapo 8 (x² − 3x + 2 = (x − 1)(x − 2)) l'exige aussi. | Ajouter avant la diapo 7 un rappel « si P(x₀) = 0, P(x) = (x − x₀)·Q(x) » avec un exemple, et le sens de « 0/0 ». | moyenne |
| 8 | 11 | 1 notion avant | « un vecteur directeur u⃗(1 ; f′(x₀)) » | Vecteur directeur d'une droite jamais rappelé. | Supprimer de l'écran ou dire simplement « depuis A, on avance de 1 et on monte de f′(x₀) » (déjà vu à la diapo 3). | moyenne |
| 9 | 13 | 1 notion avant | « celle de valeur absolue de x au carré moins un » | La valeur absolue (et pourquoi la courbe a un coin) n'est jamais rappelée ; le taux « se rapproche de deux » est affirmé sans calcul. | Rappel court avant la diapo 13 : |A| = A si A ≥ 0, −A sinon ; écrire f(x) = x² − 1 pour x ≥ 1, puis le taux x + 1 → 2. | moyenne |
| 10 | 27 | 1 notion avant | « la règle générale de la composée : g′(x)·f′(g(x)) » | La composée f∘g (1ʳᵉ Bac) n'est jamais expliquée ; nouvelle formule + nouvelle notion dans la même diapo que la racine n-ième. | Ajouter une ligne de rappel « f∘g(x) = f(g(x)) » avec un exemple, ou séparer en une diapo. | moyenne |
| 11 | 61, 66 | 1 notion avant | « Et la parité, c'est le cas a égale zéro » ; « la fonction est impaire » | Parité (paire/impaire, tronc commun) seulement nommée à l'écran 61, puis utilisée pour tracer à la diapo 66 avec D_E = Df ∩ [0 ; +∞[ jamais expliqué. | Ajouter un rappel parité (définition + dessin symétrique) avant la diapo 66 ; expliquer le domaine d'étude. | moyenne |
| 12 | 76 | 1 notion avant | « quel est l'ensemble de définition de f ? » | L'ensemble de définition (Df, conditions racine / dénominateur) n'est jamais rappelé ; Df est utilisé dès les diapos 36 et 61 (« (2a − x) ∈ Df »). | Ajouter un rappel « ensemble de définition » avant la diapo 36 (ou 61). | moyenne |
| 13 | 62 | 1 notion avant | « on sait déjà que la droite y égale x est une asymptote oblique » | Pour x + 1/x ce n'a jamais été montré (la diapo 49 traitait 2x + 1 + 1/x) ; « on sait déjà » est faux pour l'élève. | Montrer en une ligne : f(x) − x = 1/x → 0. | moyenne |
| 14 | 68 | 1 notion avant | « continue et strictement croissante… donc elle admet une fonction réciproque » | Le théorème de la bijection et l'intervalle image J = f(I) du chapitre 1 sont seulement affirmés, sans rappel de ce qu'est f⁻¹. | Diapo de rappel avant la 68 : f bijective de I sur J, f(a) = b ⟺ f⁻¹(b) = a, calcul de J. | moyenne |
| 15 | 6 | 2 trop vite | Écran : « Autre écriture (x = x₀ + h) » | Deuxième forme de la définition ajoutée dans la diapo qui introduit déjà nombre dérivé, dérivable et tangente ; jamais reprise. | Retirer de la diapo 6 et la présenter plus tard avec un exemple. | moyenne |

## Notions importantes dites une seule fois
- Définition avec h : f′(x₀) = lim (f(x₀ + h) − f(x₀))/h — diapo 6
- Méthode du conjugué pour le taux avec racine — diapo 8
- Équation d'une demi-tangente (T_d), (T_g) avec x ≥ x₀ / x ≤ x₀ — diapos 13-14 (écran seulement)
- Dérivable ⟹ continue (réciproque fausse) — diapo 15
- Dérivées usuelles 1/x, √x, sin, cos, tan, sin(ax + b), cos(ax + b) — diapo 22 (absentes du bilan)
- (1/v)′ = −v′/v² — diapo 24
- Racine n-ième et dérivée d'une composée — diapo 27
- Dérivabilité sur un intervalle fermé [a ; b] ; fonction dérivée — diapo 28
- Extremum en a sur un ouvert ⟹ f′(a) = 0 (réciproque fausse) — diapo 32
- Parité et domaine d'étude D_E — diapos 61 et 66 (une fois chacune)
- Résolution graphique de f(x) = m — diapo 67
- (f⁻¹)′(x) = 1/f′(f⁻¹(x)) sur J ; f⁻¹ non dérivable si f′(x₀) = 0 — diapos 70-71
- Tracé de la courbe de f⁻¹ (restriction, asymptote symétrisée) — diapo 73
