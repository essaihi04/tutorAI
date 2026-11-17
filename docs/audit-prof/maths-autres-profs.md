# Contre-vérification de l'audit maths avec deux autres professeurs (16 novembre 2026)

Suite de `docs/audit-prof/maths.md` (audit face au livre du Prof Fayssal). Chaque constat de cet audit a été vérifié dans
les cours d'autres professeurs de 2e bac **sciences physiques / SVT**, lus page par page en image :

| Chapitre | Sources |
|---|---|
| Limites et continuité | Pr Benmoussa Mohammed (cours, 10 p.), Pr Atmani Najib (résumé, 4 p.), atlasmaths (fiche SE, 3 p.) |
| Dérivation et étude | Pr Benmoussa (cours, 15 p. ; résumé, 4 p.) |
| Suites | Pr Benmoussa (cours, 11 p.), Pr Atmani (résumé), atlasmaths, sigmaths (fiche sciences physiques), AlloSchool (cours SM : seulement pour uₙ₊₁ = f(uₙ)) |
| Primitives | Pr Benmoussa (cours, 2 p.), Pr Atmani (résumé) |
| ln | Pr Benmoussa (cours, 13 p.), Pr Atmani (résumé), atlasmaths |
| Nombres complexes (1) | Pr Atmani (cours et exercices 2 BAC PC et SVT, 19 p. ; résumé, 3 p.) |

Documents téléchargés depuis moutamadris.ma, riyaddiyat.pages.dev (atlasmaths), sigmaths.net, alloschool.com.
Verdicts : **confirmé** (un autre professeur l'écrit aussi), **propre au Prof Fayssal** (les autres ne l'écrivent pas : à
garder si le cadre officiel le demande, sinon à baisser), **à revoir**. Rien n'a été modifié dans les cours.

## Bilan

| Chapitre | Constats du 1er audit | Confirmés | Propres au Prof Fayssal | À revoir | Nouvelles pistes (haute / moyenne / basse) |
|---|---|---|---|---|---|
| ch1 Limites et continuité | 26 | 16 | 9 | 1 | 0 / 4 / 6 |
| ch2 Dérivation et étude | 23 | 19 (dont 6 en partie) | 4 | 0 | 0 / 2 / 7 |
| ch3 Suites | 16 | 13 (dont 1 en partie) | 2 | 2 erreurs du 1er audit | 1 / 2 / 7 |
| ch4 Primitives | 9 | 4 (dont 1 en partie) | 5 | 0 | 0 / 3 / 2 |
| ch5 ln | 22 | 12 | 9 | 1 | 1 / 3 / 6 |
| ch6 Nombres complexes | 19 | 15 | 3 | 1 | 1 / 6 / 7 |
| **Total** | **115** | **79** | **32** | **5** | **3 / 20 / 35** |

**Ce qui est sûr** : les grandes familles de manques sont confirmées par les autres professeurs : conditions et hypothèses
oubliées dans les fiches (primitives sans intervalle ni condition, quotients sans z ≠ 0), tableau des limites usuelles,
continuité à droite / à gauche, définition de « dérivable sur un intervalle », f(I) ⊂ I pour les suites, limites de
ln(u(x)), flèches de vecteur et ensembles de points en complexes.

**Nuances** : la rédaction « … car … » n'a pas pu être confirmée en dérivation (le cours de Benmoussa n'a pas d'exercice
rédigé) ; « dans un repère orthonormé » pour la symétrie de C_f et C_f⁻¹ n'est écrit que par le Prof Fayssal (à garder,
en priorité moyenne). L'inégalité triangulaire, donnée par Atmani, reste hors de notre fiche (classée hors cadre).

**Erreurs du premier audit corrigées** : en suites, ∀ figure déjà dans trois démonstrations rédigées (mais jamais à
l'écran ni au cahier) et la somme géométrique en symboles est déjà au cahier de su_p2 et su_p3 ; en ln, le domaine avec
√(… ln x) n'est en fait pas couvert par ln_d3.

## Les nouvelles pistes les plus importantes

| Priorité | Chapitre | Piste | Source | Où |
|---|---|---|---|---|
| haute | ch3 | Passage à la limite dans une inégalité (uₙ ≥ 0 ⇒ ℓ ≥ 0 ; l'inégalité stricte devient large) : c'est ce qui justifie « ℓ ∈ I » | Atmani p. 1 | su_f6, su_c3 |
| haute | ch5 | Justifier la branche parabolique de ln par lim (ln x)/x = 0 (aujourd'hui affirmée sans preuve) | Benmoussa p. 4, 7 | ln_l3 (ln_l1) |
| haute | ch6 | Nature d'une figure avec les seules distances (AB = AC = BC ⇒ équilatéral ; losange) | Atmani p. 9, 15-16 | nc_i2 |
| moyenne | ch1 | Continuité de la composée g∘f, de sin(ax + b), cos(ax + b) ; limite d'une composée lim v(u(x)) = v(ℓ) si v continue en ℓ | Benmoussa p. 5, Atmani p. 2, atlasmaths | lc_i4 |
| moyenne | ch2 | Hypothèses des règles de calcul : « u et v dérivables sur I », « v ne s'annule pas sur I » | Benmoussa | df_dv2_produit_quotient_b, df_fin1_bilan |
| moyenne | ch2 | Parité et variations : impaire → même sens sur I et −I ; paire → sens contraires (Benmoussa l'écrit à l'envers : ne pas recopier) | Benmoussa | df_tr5_symetrie |
| moyenne | ch3 | Convergente ⇒ bornée, mais bornée ⇏ convergente ((−1)ⁿ) ; croissante et non majorée ⇒ +∞ | Atmani p. 1, atlasmaths p. 2 | su_c1, su_c2 |
| moyenne | ch4 | Unicité de la primitive telle que F(x₀) = y₀ ; u′/uⁿ ; règle (1/a)F(ax + b) | Benmoussa p. 1-2, Atmani p. 1 | pr_e6, pr_c6, pr_u7 |
| moyenne | ch5 | lim ln(x + 2)/x par changement de variable ; x ∈ D_f ⇔ x ∈ D_u et u(x) > 0 | Benmoussa p. 1, 5, 12 | ln_l7, ln_d1, ln_d3 |
| moyenne | ch6 | Cube par identité remarquable ((1 + i√3)³ = −8) ; montrer qu'un nombre est réel (S̄ = S) ou imaginaire pur (S + S̄ = 0) sans le calculer | Atmani p. 2, 6-8 | nc_c2, nc_c4 |

Deux erreurs repérées chez les autres professeurs, à ne pas reprendre : Benmoussa, primitives p. 2 (« 3x → 6x² + c » au
lieu de (3/2)x²) et la règle parité / variations inversée.

---

## Limites et continuité

Sources lues : Pr Benmoussa Mohammed, `ch1_moutamadris.pdf` (cours 2 PC + 2 SVT, p. 1-10, toutes lues en image) ; Pr Atmani Najib, `m_resume-Limites-et-continuite-…pdf` (résumé 2 BIOF PC/SVT, p. 1-4, toutes lues en image) ; atlasmaths, `ch1_atlas.pdf` (fiche SE, p. 1-3, toutes lues en image). Notre cours : texte de chaque diapo + recherche dans le JSON complet (écran, cahier, voix fr/mixed, questions, réactions). Cadre : SE 1.2.1-1.2.4, 1.2.11, 1.2.22. Pages = pages du PDF.
Abréviations : **Ben** = Benmoussa, **Atm** = Atmani, **Atl** = atlasmaths.

### A. Les constats du premier audit, contre-vérifiés

| Constat (court) | Priorité | Verdict | Preuve (prof, page) |
|---|---|---|---|
| Continuité à droite / à gauche : 2 définitions + propriété « continue ⇔ à droite et à gauche » + phrase « donc f est continue à droite en a » | haute | **confirmé** | Ben p. 1 (définitions avec I_d = [x₀ ; x₀ + r[, I_g), p. 2 (propriété), p. 2-3 (« Donc : f est continue à gauche de x₀ = 0 ») ; Atm p. 1 (II.2, deux définitions) ; Atl p. 2 (piège 5 « confondre limite à gauche et à droite »). Chez nous toujours 0 occurrence (vérifié dans le JSON) |
| Tableau des limites usuelles | haute | **confirmé** (en partie) | Atl p. 1 : lim xⁿ = +∞ en +∞, lim 1/xⁿ = 0 en ±∞, lim 1/x = ±∞ en 0±. La parité de n en −∞ (x²ⁿ, x²ⁿ⁺¹) et 1/√x ne sont que chez Fayssal. Ben n'a aucun rappel de limites |
| Tableaux des opérations (L × ∞ par la règle des signes, ∞/L, L/0) | haute | **confirmé** | Atm p. 1 : tableaux somme, produit (ℓ > 0 × +∞ = +∞, ℓ < 0 × +∞ = −∞, 0 × ∞ = FI), inverse (1/0⁺ = +∞, 1/0⁻ = −∞), quotient (±∞/ℓ → ±∞) |
| « Dans un repère orthonormé » pour la symétrie (C_f) / (C_f⁻¹) | haute | **à revoir (priorité)** : aucun autre prof ne l'écrit | Ben p. 8 : « (C_f⁻¹) et (C_f) sont symétriques par rapport à la 1ʳᵉ bissectrice (D) : y = x », sans repère ; Atm p. 3 : « symétriques par rapport à (Δ) y = x », sans repère. La précision reste juste (Fayssal) : la garder, mais en moyenne |
| Unicité de f(x) = k (pas seulement k = 0) | haute | **confirmé** | Ben p. 6 (remarque : continue et strictement monotone ⇒ c unique avec f(c) = k) ; Atm p. 2 (« T.V.I cas strictement monotone » : « l'équation f(x) = λ admet une solution unique dans [a, b] ») ; Atl p. 2 (corollaire : un unique c tel que f(c) = k). Les trois l'écrivent avec k entre f(a) et f(b) sur [a, b], pas avec k ∈ f(I) (voir C) |
| Condition « I ouvert contenant x₀ » dans la définition de la continuité en x₀ | moyenne | **confirmé** | Ben p. 1 (« I_x₀ est un intervalle ouvert et contient x₀ et inclus dans D_f ») ; Atm p. 1 (« définie sur un intervalle de centre a ») |
| Continue sur ]a ; b[ (en chaque point) / sur [a ; b] (+ à droite en a, à gauche en b) | moyenne | **confirmé** | Ben p. 3 (4 cas : ]a,b[, [a,b[, ]a,b], [a,b]) ; Atm p. 2 (III.1, 3 cas) ; Atl p. 1 (« continue en tout point de I ») |
| Exercice « D_f puis ensemble de continuité » | moyenne | **confirmé** (forme plus simple) | Ben p. 4 : f(x) = (x² + 3x − 2)·√x et g(x) = (2x + 1)/(x − 1) + cos x : « déterminer ensemble de définition et ensemble de la continuité ». Pas de fonction à deux expressions |
| « L'image d'un segment est un segment ; d'un intervalle est un intervalle » | moyenne | **confirmé** | Ben p. 4 (V, f([a,b]) = [m, M] avec m, M plus petite / plus grande image) ; Atm p. 2 (IV.1 « théorème (admis) » et 2.1) |
| Tableau des images (croissante / décroissante, bornes ouvertes ou infinies) | moyenne | **confirmé** | Ben p. 5 : tableau de 18 cas (dont f(ℝ), f(]−∞ ; a])) ; Atm p. 2 : 8 cas sur [a ; b], [a ; b[, ]a ; b], ]a ; b[ |
| lim tan x / x = 1 et lim (1 − cos x)/x² = 1/2 en 0 | moyenne | **confirmé** | Atm p. 1 (n° 8, 10 tan(ax)/(ax) = 1, 11) ; Atl p. 1 ((1 − cos x)/x² = 1/2) |
| Comparaison et encadrement pour les fonctions | moyenne | **propre au Prof Fayssal** | Absent de Ben, Atm, Atl |
| f⁻¹∘f(x) = x sur I ; f∘f⁻¹(x) = x sur J | moyenne | **confirmé** | Ben p. 7 (encadré « relation entre f et f⁻¹ ») ; Atm p. 3 |
| Signe de ax + b et du trinôme (Δ) | moyenne | **propre au Prof Fayssal** | Aucun des trois (rappel de 1re) |
| f′ ≥ 0 nulle en des points isolés ⇒ strictement croissante | moyenne | **propre au Prof Fayssal** (énoncé) | Pas énoncé ailleurs ; mais Ben p. 7 l'utilise sans le dire (x ↦ 2x « positive sur [0, +∞[ donc x² strictement croissante », alors que 2x = 0 en 0) : même faille que notre simulation lc_r4 |
| a³ + b³ = (a + b)(a² − ab + b²) | moyenne | **confirmé** | Atm p. 4 (3.3 : a³ + b³ et formule ∛x + ∛y = (x + y)/(…)) |
| ∞/∞ avec racines d'indices différents : indice commun | moyenne | **propre au Prof Fayssal** | Ben p. 9 utilise l'indice commun seulement pour simplifier un produit (comme notre lc_n4) |
| Équations avec ⁿ√ (D_(E), changement d'inconnue, puissance 6) | moyenne | **propre au Prof Fayssal** | Atm p. 3 ne résout que xⁿ = a (x⁵ = 32, x⁷ = −128, x⁴ = 3, x⁶ = −8) : déjà chez nous (lc_n6) |
| Nombre de solutions de f(x) = k lu sur un tableau de variations | moyenne | **propre au Prof Fayssal** | Ben p. 6 a seulement une activité graphique (c tel que f(c) = k sur une courbe) |
| TVI avec une fonction trigonométrique | basse | propre au Prof Fayssal | — |
| Limite avec valeur absolue, à droite et à gauche | basse | **confirmé** (à remonter en moyenne) | Ben p. 1 et p. 3 ((x² − \|x\|)/(\|x\| − 1) en 1) ; Atm p. 1 ((x + 1)²/\|x² − 1\| en −1, limites à droite et à gauche) |
| Changement X = x − 1 dans sin(πx)/(x − 1) | basse | propre au Prof Fayssal | Atm p. 1 donne seulement sin(ax)/(ax) en 0 (déjà chez nous) |
| Continuité de \|x\|, tan, αf | basse | **confirmé** | Ben p. 4 (tan sur ℝ \ {π/2 + kπ}, αf) ; Atm p. 1 (lim tan x = tan x₀) et p. 2 (\|f\| continue) |
| ⁿ√x = ⁿ√y ⇔ x = y ; ¹√x = x | basse | **confirmé** | Ben p. 9 (tableau et « cas n = 1 ») ; Atm p. 3 (5) et remarque 2 |
| a^(p/q) avec p ∈ ℤ, q ∈ ℕ* ; a^(−r) = 1/a^r | basse | **confirmé** | Atm p. 4 (4.2) ; Ben p. 10 (« m ∈ ℤ, n ∈ ℕ* », a^(−r) = 1/a^r) |
| Stricte monotonie sans dériver | basse | propre au Prof Fayssal | — |
| *Oral seulement* — lc_r8 « c'est f de y, pas f de x » | — | **à revoir** | Ben p. 7 donne deux méthodes, dont la 1ʳᵉ « f(x) = y » avec x ∈ I, y ∈ J (puis renomme y en x). L'erreur n'est pas d'écrire f(x) = y, mais de mélanger les rôles : reformuler « garde x ∈ J à droite, y ∈ I à trouver » |
| *Oral seulement* — lc_l10 « jamais nombre sur 0 sans le signe » | — | **confirmé** | Atm p. 1 (tableau des inverses 0⁺ / 0⁻) ; Ben p. 10 (« lim (x − 5) = 0⁺ » écrit à chaque fois) |
| *Oral seulement* — sens de l'asymptote (écart → 0) | — | pas chez les autres | — |
| *Notation* — x → a sous lim | — | **confirmé** | Ben, Atm, Atl : partout, sous le lim |
| *Notation* — quantificateur ∀ dans les conditions | — | **confirmé** | Atm p. 3-4 (« (∀x ∈ ℝ+) » à chaque règle) ; Ben p. 7 (∀x ∈ I) |
| *Notation* — « continue à droite de a » / « en a » | — | désaccord (voir C) | Ben p. 1-2 « à droite du point x₀ / de x₀ » ; Atm p. 1 « à droite de a » |
| *Notation* — « 1ʳᵉ bissectrice » | — | **confirmé** | Ben p. 8 |
| *Notation* — ℝ et non IR | — | **confirmé** | Ben et Atm écrivent ℝ |

Vérification de notre cours : aucune erreur du premier audit trouvée sur ce qui est présent ou absent (« continue à droite », « orthonormé », « ∀ », « tan », « ∘ », « a³ + b³ », « λ », « chaque point » : toujours 0 dans le JSON).

### B. Nouvelles pistes

| Priorité | Catégorie | Ce que dit le professeur (prof, page) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| moyenne | propriété | Continuité de la composée : f continue en x₀ et g continue en f(x₀) ⇒ g∘f continue en x₀ ; f continue sur I et g continue sur f(I) ⇒ g∘f continue sur I. Applications : sin(ax + b), cos(ax + b) continues sur ℝ ; tan(ax + b) là où ax + b ≠ π/2 + kπ (Ben p. 5 ; Atm p. 2 III.3 ; Atl p. 1 « composée de fonctions continues = continue ») | lc_i4 ne traite que √(u) et seulement pour une limite ; « ∘ », « sin(ax » : 0. Le cadre 1.2.22 parle de « composées de fonctions » | lc_i4_composee (une puce + cahier), ou diapo après lc_i3_racine_u |
| moyenne | propriété | Limite d'une composée : lim u(x) = ℓ en x₀ et v continue en ℓ ⇒ lim v(u(x)) = v(ℓ) (Atm p. 2 III.4) | Seulement pour √ (lc_i4) et ⁿ√ (lc_lr1). Règle générale utile pour cos(1/x), plus tard ln(u), e^u | lc_i4_composee (énoncé général, √ comme exemple) |
| moyenne | méthode | Forme 0 × ∞ : « transformer en 0/0 ou ∞/∞ » (Atl p. 1, tableau des 4 FI avec un outil pour chacune) | lc_l4 nomme 0 × ∞, mais aucun outil n'est donné (lc_l13 : facteur, conjugué, plus haut degré, sin, même dénominateur) | lc_l13_devoir (liste des outils) ou lc_l4_formes |
| moyenne | rédaction | Deuxième forme de la conclusion : « il existe un unique α ∈ ]a ; b[ tel que f(α) = 0 », équivalente à « l'équation f(x) = 0 admet une solution unique » (Ben p. 6 remarque ; Atm p. 2 remarque ; Atl p. 2) | « il existe » : jamais pour le TVI (1 occurrence, dans une réaction sur les FI) | lc_t6_rediger (« on peut aussi écrire… ») et lc_t4 |
| basse | propriété | ⁿ√x ≤ a ⇔ 0 ≤ x ≤ aⁿ ; ⁿ√x ≥ a ⇔ x ≥ aⁿ (Atm p. 3, 6-7) ; ⁿ√a ≤ ⁿ√b ⇔ a ≤ b (Ben p. 9) | lc_n5 : seulement l'inégalité stricte x < y ⇔ ⁿ√x < ⁿ√y ; aucune inéquation avec ⁿ√ | lc_n5_comparer ou lc_n7 |
| basse | formule | (x/y)^r = x^r/y^r ; a^r > 0 ; a^r = a^(r′) ⇔ r = r′ (Ben p. 10 ; Atm p. 4 n° 6) | lc_p3 : produit, puissance, quotient x^r/x^s, (xy)^r ; pas (x/y)^r | lc_p3_regles_puissances |
| basse | remarque / piège | « I et f(I) n'ont pas nécessairement la même forme » (Atm p. 2, remarque 2.1) | Absent ; lc_j5 montre [−2 ; 2] → [−2 ; 2] sans le dire | lc_j5_non_monotone |
| basse | méthode | Lire sur un graphique la continuité à droite / à gauche (point plein, point vide, saut) (Ben p. 1 fig. 1-2, p. 3 exemple 2 fig. 3) | lc_c1 : trois dessins, mais sans « à droite / à gauche » | lc_c1_soudee ou exercice après lc_c3 |
| basse | exemple | Fonction à trois expressions, deux paramètres a et b, continuité en deux points (avec conjugué dans une branche) (Ben p. 2-3) | Un seul paramètre m, un seul point (lc_c4) | exercice de fin après lc_c5_redaction |
| basse | exemple | Limite de ⁿ√ d'un quotient avec 0⁺ : ∛((8x + 8)/(x − 5)) en 5⁺ → +∞, en −1⁻ → 0 (Ben p. 9-10) | lc_lr1 : règle générale (u → +∞ ou ℓ) avec une somme seulement | exercice après lc_lr1_continuite |

Écarté (hors cadre ou décision) : prolongement par continuité (Atm p. 1, Atl p. 2 : retiré exprès, voir audit officiel) ; « bijection » (Atm p. 3, Atl p. 2 « TVI strict / bijection ») ; exp dans la liste des continues (Atl p. 1 : chapitre suivant) ; 0^r = 0 (Ben p. 10 : nous gardons x > 0).

### C. Désaccords entre professeurs

- **« Continue à droite de a » ou « en a »** : Fayssal, Ben (p. 1-2) et Atm (p. 1) écrivent « de a » ; nous et les sujets nationaux « en a ». Garder « en a », dire une fois que « de a » est la même chose.
- **Intervalle de la solution** : Atm (TVI, corollaire 1, p. 2) et Atl (énoncé p. 2) écrivent c ∈ [a ; b] ; Ben (p. 6, corollaires) et Atl (méthode p. 2) écrivent ]a ; b[ quand f(a)·f(b) < 0. Garder ]a ; b[ (juste, car f(a) ≠ 0 et f(b) ≠ 0 ; c'est ce que demande le national).
- **Énoncé de l'unicité** : Ben, Atm, Atl avec k (ou λ) entre f(a) et f(b) sur [a ; b] ; Fayssal avec k ∈ f(I) sur un intervalle quelconque. Garder la forme de Fayssal (k ∈ f(I) / λ, comme le cadre 1.2.4) : elle couvre les bornes infinies (lc_t8), et la forme [a ; b] en est un cas particulier.
- **Nom du théorème** : Atl « TVI strict », Atm parle de « bijection » ; Ben et Fayssal « théorème des valeurs intermédiaires » + « strictement monotone ». Garder notre écriture (pas de « bijection », hors cadre ; pas de « TVI strict », qui n'est pas un nom officiel).
- **Expression de f⁻¹** : Ben p. 7 donne deux méthodes (1ʳᵉ : f(x) = y, x ∈ I, puis on renomme y en x ; 2ᵉ : f(y) = x, y ∈ I) et écrit f⁻¹ : J → I, x ↦ f⁻¹(x) ; Atm p. 3 et Fayssal : système { f(y) = x, y ∈ I } ⇔ { f⁻¹(x) = y, x ∈ J }. Garder notre ligne pivot (2ᵉ méthode, pas de renommage) ; on peut ajouter en conclusion l'écriture « f⁻¹ : J → I, x ↦ … ».
- **Nom de la droite y = x** : « 1ʳᵉ bissectrice (D) » (Ben p. 8), « (Δ) : y = x » (Atm p. 3), « droite d'équation y = x » (nous). Garder la nôtre et citer « première bissectrice » une fois ; « repère orthonormé » seulement chez Fayssal.
- **Indice n de ⁿ√** : n ∈ ℕ* (Atm p. 3, Ben p. 8) ou n ∈ ℕ \ {0, 1} (Ben p. 9, dans le même cours). Nous ne précisons pas : écrire « n ∈ ℕ* » (n = 1 donne x).
- **Puissance rationnelle** : Ben p. 10 x ∈ ℝ+* dans la définition mais 0^r = 0 ; Atm p. 4 « x réel positif ». Garder x > 0 (décision, évite 0^r).
- **Ordre** : Ben n'a aucun rappel de limites (commence par la continuité) ; Atm met la composée (continuité et limite) avant l'image d'un intervalle ; Atl n'a ni image d'un intervalle ni réciproque. Notre ordre (limites → continuité → image → TVI → réciproque → ⁿ√) est celui de Ben et Atm : à garder.

Bilan : 26 constats du premier audit (5 hautes, 14 moyennes, 7 basses) : 16 confirmés, 9 propres au Prof Fayssal, 1 à revoir (« repère orthonormé », absent chez Ben et Atm : à baisser en moyenne) ; + 1 phrase orale à reformuler (lc_r8). Nouvelles pistes : 0 haute, 4 moyennes, 6 basses.

---

## Dérivation et étude des fonctions

Sources lues : Pr Benmoussa Mohammed, cours complet 2 PC + 2 SVT `ch2_moutamadris.pdf` (15 p., **toutes lues en image**, p. 1-15) ; Pr Benmoussa, résumé 2 PC - SVT `m_resume-…-svt-1.pdf` (4 p., **toutes lues en image**). Le seul autre professeur disponible est donc Benmoussa (deux documents). Pas d'exercices rédigés de bout en bout dans ces documents : la rédaction type (« car… », interprétation de α) ne peut pas y être confirmée. Notre cours : texte des diapos plus recherche dans le JSON complet (écran, cahier, voix, réactions). Cadre officiel : objectifs 1.2.5 à 1.2.13 et 1.2.22.

### A. Les constats du premier audit, contre-vérifiés

| Constat (court) | Priorité | Verdict | Preuve (prof, page) |
|---|---|---|---|
| Justifier la dérivabilité avec la raison (« car polynôme », « quotient, x² + 1 ≠ 0 », « √u : u > 0 ») | haute | **confirmé** pour les propriétés ; la phrase rédigée « car… » reste propre au Prof Fayssal (Benmoussa n'a pas d'exercice rédigé). Vérifié chez nous : l'écran dit seulement « f est dérivable sur … », la raison n'est que dans une réaction préparée de df_dv6_montrer | Benmoussa cours p. 4 (« toute fonction polynomiale est dérivable sur ℝ » ; « rationnelle dérivable sur son Df » ; f/g dérivable sur I si ∀x ∈ I, g(x) ≠ 0) ; p. 5 et résumé p. 2 ((√f)′ avec f(x) > 0) |
| Définition « dérivable sur ]a ; b[, [a ; b[, ]a ; b], [a ; b] » et fonction dérivée f′ | haute | **confirmé** | cours p. 3 (4 cas + « la fonction g : x ↦ f′(x) s'appelle la fonction dérivée ») ; résumé p. 1 |
| Phrase « (Cf) coupe l'axe des abscisses en un point unique d'abscisse α » | haute | **pas chez les autres** (Benmoussa ne traite pas le TVI dans ce chapitre) ; reste propre au Prof Fayssal, mais garde sa priorité (phrase des corrigés) | — |
| Dérivées de sin, cos, tan, sin(ax + b), cos(ax + b) | moyenne | **confirmé** | cours p. 4 (sin, cos, tan = 1 + tan² = 1/cos²), p. 5 (ax + b), p. 6 (tableau) ; résumé p. 2 |
| (1/v)′ = −v′/v², v ≠ 0 | moyenne | **confirmé** | cours p. 4 ; résumé p. 1 (« ∀x ∈ I, g(x) ≠ 0 ») |
| f′ = 0 sur I ⇒ f constante ; forme large f′ ≥ 0 ⇔ croissante | moyenne | **confirmé** pour « f′ nulle sur I tout entier ⇒ f constante » ; la forme large est **propre au Prof Fayssal** : Benmoussa donne la forme stricte « même si f′ s'annule en un nombre fini de points », comme nous (df_va1) | cours p. 7 ; résumé p. 2 |
| Extremum ⇒ f′(a) = 0, réciproque fausse (2x³) | moyenne | **confirmé**, même contre-exemple 2x³, avec l'hypothèse « I intervalle ouvert, a ∈ I ». Vérifié chez nous : la phrase n'est que dans une réaction préparée (df_va2_sommet_b) | cours p. 7 (propriété, remarque, exemple et courbe de 2x³) ; résumé p. 2 |
| Équation de la demi-tangente avec x ≥ x₀ / x ≤ x₀ | moyenne | **confirmé** | cours p. 2 ((T_d) : y = (x − x₀)f′_d(x₀) + f(x₀) avec x ≥ x₀, idem à gauche avec x ≤ x₀ ; exemple en −2) |
| (f⁻¹)′ sur tout J : (f⁻¹)′(y) = 1/f′(f⁻¹(y)) | moyenne | **confirmé** (forme générale donnée, sans démonstration) | cours p. 5 ; résumé p. 2 |
| Hypothèses de la réciproque : f continue et strictement monotone sur I, J = f(I), f′(x₀) ≠ 0 | moyenne | **confirmé** | cours p. 5 ; résumé p. 2 |
| Hypothèses de la composée | moyenne | **confirmé sous la forme « en un point »** : f dérivable en x₀, g dérivable en f(x₀) ⇒ g∘f dérivable en x₀. La forme « sur I, f(I) ⊂ J » est propre au Prof Fayssal | cours p. 5 ; résumé p. 2 |
| Conditions des définitions (f définie sur un intervalle ouvert contenant x₀) | moyenne | **confirmé** pour le nombre dérivé (« Df contient un intervalle ouvert I et x₀ ∈ I ») ; les intervalles [a ; a + r[ et ]a − r ; a] à droite et à gauche sont propres au Prof Fayssal | cours p. 1 |
| Domaine d'étude D_E | moyenne | **confirmé** pour la parité (D_E = Df ∩ ℝ⁺, « ensemble d'étude ») ; D_E = Df ∩ [a ; +∞[ pour un axe ou un centre est propre au Prof Fayssal | résumé p. 3 |
| Tableau de concavité x / f″(x) / concavité avec ∪ ∩ | moyenne | **confirmé** (deux tableaux) | cours p. 8 (exemple 2) et p. 9 (exemple 2) |
| Calculer g⁻¹(a) en résolvant g(y) = a | moyenne | **pas chez les autres** | — |
| Asymptote oblique : a ∈ ℝ*, b ∈ ℝ | basse | **confirmé** (en plus, la condition [a ; +∞[ ⊂ Df : voir B) | cours p. 12 ; p. 15 (le schéma part de lim f(x) = ±∞) |
| Concavité : « f deux fois dérivable sur I », « ∀x ∈ I » | basse | **confirmé** (Benmoussa écrit f″(x) > 0, inégalité stricte : voir C) | cours p. 8 et p. 9 ; résumé p. 2-3 |
| Forme h → 0 du nombre dérivé | basse | **confirmé** | cours p. 1 (les trois définitions) ; résumé p. 1 |
| (xⁿ)′ pour n entier négatif | basse | **confirmé** | cours p. 6 (tableau : n ∈ ℤ*∖{1}, Df′ = ℝ*) ; p. 4 (fᵖ, p ∈ ℤ*, f(x) ≠ 0) ; résumé p. 1 |
| Tracer la tangente avec un vecteur directeur u(1 ; f′(a)) | basse | **confirmé** (point B tel que AB = 1·i, puis C tel que BC = 4·j ; segment centré en A) | cours p. 2 (f(x) = 2x², figure) |
| « dans un repère orthonormé (O ; i ; j) » | basse | **confirmé** | cours p. 6 (remarque avant les applications), p. 9-10 (symétries) |
| Intervalle exclu hachuré dans le tableau de variations | basse | **pas chez les autres** | — |
| Tracer (Cg) pour une fonction paire g déduite de f | basse | **pas chez les autres** | — |

« Présent seulement à l'oral » : Benmoussa ne l'écrit pas non plus (cours p. 3 : « lim … = ∞ » donné sans dire ce que deviennent le haut et le bas). Rien à confirmer ni à infirmer.

Remarque : le premier audit dit que le prof ne nomme pas le « point anguleux ». Benmoussa le nomme (cours p. 2, résumé p. 1) : le nom que nous employons est donc confirmé.

### B. Nouvelles pistes

Chaque absence a été vérifiée dans le JSON complet (écran, cahier, voix, réactions), avec plusieurs écritures.

| Priorité | Catégorie | Ce que dit le professeur (prof, page) | Chez nous | Où l'ajouter (id de diapo) |
|---|---|---|---|---|
| moyenne | propriété (hypothèses) | Hypothèses des règles de calcul : « Soient f et g deux fonctions dérivables sur I » ; f/g et 1/g dérivables sur I si ∀x ∈ I, g(x) ≠ 0 (Benmoussa cours p. 4 ; résumé p. 1) | (u·v)′ et (u/v)′ données sans « u, v dérivables sur I » et sans « v ne s'annule pas sur I » (0 « v ≠ 0 », 0 « v(x) ≠ 0 », 0 « dérivables sur ») | df_dv2_produit_quotient_b (écran et cahier) ; df_fin1_bilan point 3 |
| moyenne | propriété / méthode | Parité et variations : « si f est paire ou impaire, il suffit d'étudier f sur I = Df ∩ ℝ⁺ » ; on en déduit les variations sur I′ (Benmoussa résumé p. 3). **Attention, Benmoussa inverse la règle** (« paire : même monotonie ; impaire : opposées ») : la règle juste est « impaire : même sens de variation sur I et I′ ; paire : sens contraires » (exemples : x³, x²) | Absent (df_tr5_symetrie dit seulement que la branche x < 0 est la symétrique de l'autre ; 0 « même sens ») | df_tr5_symetrie (une ligne, avec la règle corrigée) |
| basse | méthode (cadre 1.2.22) | Fonction périodique de période T : D_E = Df ∩ [0 ; T] ou Df ∩ [−T/2 ; T/2] (Benmoussa résumé p. 3) | Absent (0 « périod ») ; déjà signalé dans l'audit face au cadre (« à décider »), pas dans le premier audit | df_sy4_rediger (une ligne), à trancher : la trigonométrie est rare au national PC |
| basse | définition (hypothèse) | Asymptote horizontale ou oblique en +∞ : « Df contient un intervalle [a ; +∞[ » (ou ]−∞ ; a] en −∞) (Benmoussa cours p. 11, p. 12) | Absent (0 « ⊂ Df ») | df_bi2_horizontale, df_bi3_oblique |
| basse | définition | Branche infinie : « si au moins une des coordonnées d'un point M de (Cf) tend vers l'infini, (Cf) admet une branche infinie » (Benmoussa cours p. 11) | Le mot est employé mais jamais défini (seulement dans deux réactions) | df_bi6_arbre (première ligne) |
| basse | hypothèse / notation | Axe et centre de symétrie énoncés « dans un repère orthonormé (O ; i ; j) » (Benmoussa cours p. 9, p. 10). Pour un axe x = a, il faut au moins un repère orthogonal | Absent (0 « orthonorm » ; le premier audit ne le demandait que pour le tracé) | df_sy2_axe |
| basse | formule (cadre 1.2.22, gardée sur décision) | (xʳ)′ = r·xʳ⁻¹ et ((f(x))ʳ)′ = r·f′(x)·(f(x))ʳ⁻¹, r ∈ ℚ*, f strictement positive ; ⁿ√x = x^(1/n) pour dériver ⁵√((x² + 1)⁷) (Benmoussa cours p. 5-6 ; résumé p. 2) | Absent du ch2 (seulement (ⁿ√u)′ ; 0 « ʳ ») | df_dv5_racine_n (une ligne), si les puissances rationnelles restent au programme du cours |
| basse | propriété (hypothèse) | Critère d'extremum : « f dérivable sur un intervalle **ouvert** I, a ∈ I, f′(a) = 0 et f′ change de signe au voisinage de a » (Benmoussa cours p. 8 ; résumé p. 2) | df_va2_sommet_b : sans « intervalle ouvert » ni « a ∈ I » | df_va2_sommet_b |
| basse | notation / vocabulaire | Deux formulations à reconnaître dans les énoncés : « concavité dans le sens des ordonnées positives / négatives » (= convexe / concave) ; demi-tangente « parallèle à l'axe des ordonnées » (= verticale), tangente « parallèle à l'axe des abscisses » (Benmoussa cours p. 1, p. 3, p. 8 ; résumé p. 2-3) | Absent (0 « ordonnées positives », 0 « parallèle à l'axe ») ; nous disons « tournée vers le haut/bas » et « verticale » | df_co1_sous (une mention) ; df_dt4_infini (une mention) |

Écarté (hors cadre ou déjà présent) : approximation affine et fonction affine tangente (Benmoussa cours p. 13-14, « complément » ; résumé p. 1) : retirée exprès ; dérivée n-ième f⁽ⁿ⁾ (cours p. 3) : le cadre ne demande que f′ et f″ ; colonne « domaine de f′ » du tableau (cours p. 6) : déjà couverte (√x non dérivable en 0, df_dt4) ; « f′(x₀) = 0 ⇒ tangente horizontale », position relative par le signe de f(x) − (ax + b), les trois cas de branche parabolique : déjà présents.

### C. Désaccords entre professeurs

| Point | Prof Fayssal | Pr Benmoussa | Nous | À garder |
|---|---|---|---|---|
| Composée | (g∘f)′(x) = g′(f(x))·f′(x), sur I | (g∘f)′(x₀) = f′(x₀)·g′(f(x₀)), en un point (cours p. 5) | (f∘g)′(x) = g′(x)·f′(g(x)) | Nommer g∘f comme les deux profs (u à l'intérieur = f) ; l'ordre des facteurs importe peu |
| Concavité | f″ ≥ 0 sur I | ∀x ∈ I, f″(x) > 0 (stricte) (cours p. 8) | f″ ≥ 0 / f″ ≤ 0 | Garder la nôtre (plus générale) ; ajouter « f deux fois dérivable sur I » |
| Monotonie | forme large f′ ≥ 0 ⇔ croissante | stricte « même si f′ s'annule en un nombre fini de points » (cours p. 7) | stricte « sauf en des points isolés » | Garder la nôtre (c'est ce que demande le national) ; ajouter seulement « f′ = 0 ⇒ constante » |
| Demi-tangente | x > a (strict) | x ≥ x₀ / x ≤ x₀ (cours p. 2) | (absente) | Les deux se lisent ; choisir x ≥ x₀ (la demi-droite part du point) et s'y tenir |
| Branche parabolique | « dirigée vers l'axe des ordonnées » | « de direction l'axe des ordonnées » (B.P.D, cours p. 12-15) | « de direction » | Garder la nôtre : Benmoussa et les corrigés disent comme nous |
| Notation du nombre dérivé à droite | f′_d(a) | f′_d(x₀) et f_d′(x₀), les deux (cours p. 1-2) | f_d′(x₀) | Rien à changer |
| Approximation affine | dans le livre (hors cadre) | « complément » (cours p. 13-14) | retirée exprès | Ne pas l'ajouter |
| Parité et variations | parité ⇒ D_E = Df ∩ [0 ; +∞[ | règle des variations **inversée** (résumé p. 3) | rien | Si on l'ajoute, donner la règle juste (impaire : même sens ; paire : sens contraires) |

Erreurs relevées chez Benmoussa, à ne pas recopier : « nombre dérivé à gauche » écrit pour la dérivée à droite (cours p. 1, résumé p. 1) ; « demi-tangente à droite » écrit pour la gauche (cours p. 2) ; « f(x₀) ≠ 0 » au lieu de « f′(x₀) ≠ 0 » dans le théorème de la réciproque (cours p. 5) ; « x₁ = 2 n'est pas un point d'inflexion car f″ change de signe » au lieu de « ne change pas » (cours p. 9) ; asymptote verticale définie avec « lim à droite = ±∞ **et** lim à gauche = ±∞ » au lieu de « ou » (cours p. 11). Notre cours est juste sur tous ces points.

---

## Suites numériques

Sources lues : Pr Benmoussa Mohammed, cours complet 2 PC + 2 SVT `m_cours-Suites-numeriques-…-svt-1.pdf` (11 p., **toutes lues en image**) ; Pr Atmani Najib, résumé 2 SVT + PC `m_resume-…-svt-1.pdf` (2 p., **lues en image**) ; Atlasmaths, fiche 2e bac SE `ch3_atlas.pdf` (3 p., **lues en image**) ; « Prof Abdel 1 » (sigmaths), fiche « Étude d'une suite numérique », 2e bac sciences physiques `ch3_sigmaths.pdf` (3 p., **lues en image**) ; Mr Cheddadi Haitam (AlloSchool) `ch3_alloschool.pdf` (2 p., **lues en image**). Ce dernier est un cours **2Bac SMA-SMB** (sciences maths) : seules ses propositions 12 et 13 (uₙ₊₁ = f(uₙ), vₙ = f(uₙ)) sont dans notre cadre ; ses suites adjacentes sont hors cadre. Notre cours : texte des diapos, plus recherche dans tout le JSON (écran, cahier, voix fr et mixed, réactions, démonstrations). Cadre : objectifs 1.1.1 à 1.1.5.

### A. Les constats du premier audit, contre-vérifiés

| Constat (court) | Priorité | Verdict | Preuve (prof, page) |
|---|---|---|---|
| Prouver f(I) ⊂ I en calculant f(I) = [f(a) ; f(b)] (f continue et croissante) | haute | **confirmé** | Benmoussa p. 10 : « f(I) = f([0 ; 3]) = [f(0), f(3)] (car l'image d'un intervalle est un intervalle et puisque f est croissante) = [√6 ; 3] ⊂ [0 ; 3] ». Chez nous « f(I) = » : 0 occurrence (vérifié). Attention : Benmoussa écrit ensuite « [√3, 3] » dans sa conclusion (coquille, ne pas recopier). |
| Justifier la continuité de f par une raison | haute | **confirmé** (la raison change selon le prof) | Benmoussa p. 10 : « f est continue sur son domaine de définition D_f = [−6, +∞[ donc f est continue sur I = [0 ; 3] ». Atlas p. 2, piège n° 3 : « Conclure ℓ = f(ℓ) sans justifier la continuité ». La raison « car dérivable » reste propre au Prof Fayssal. Chez nous : « dérivable » et « car f est » : 0 occurrence. |
| Cas « deux solutions de f(x) = x dans I » : le sens de variation tranche | haute | **pas chez les autres** (propre au Prof Fayssal) | Benmoussa p. 11 ne traite que le cas « x = 3 ∈ [0 ; 3] ou x = −2 ∉ [0 ; 3] ». Les autres fiches n'ont pas d'exemple. Le point reste juste et utile ; la justification par passage à la limite (piste B1) le rend rigoureux. |
| Tableaux des opérations (somme, produit, inverse, quotient) et formes indéterminées | moyenne | **confirmé** | Atmani p. 1 (E : quatre tableaux, cases « Formes indéterminées ») ; Benmoussa p. 5 (« les propriétés des opérations des limites des suites sont les mêmes que celles des fonctions »). Chez nous « indétermin » : 0. |
| FI avec deux puissances : factoriser ou diviser par la puissance dominante | moyenne | **confirmé** | Benmoussa p. 7 : lim (2ⁿ − 8ⁿ)/7ⁿ = lim [(2/7)ⁿ − (8/7)ⁿ]. **Son calcul est faux** : il écrit « −1 < 8/7 < 1 » et trouve 0, alors que 8/7 > 1 donne −∞. Exemple à reprendre corrigé. Chez nous « 3ⁿ » : 0. |
| Comparaison version −∞ et « à partir d'un certain rang » | moyenne | **confirmé** | Atmani p. 1-2 (F.3 et F.4 : « (∃N ∈ ℕ)(∀n > N) vₙ ≤ uₙ et lim uₙ = −∞ alors lim vₙ = −∞ ») ; Sigmaths p. 3 (« Si lim vₙ = −∞ alors lim uₙ = −∞ ») ; Benmoussa p. 5 (« à partir d'un rang p » ; son point 3 écrit « lim vₙ = ℓ » au lieu de −∞, coquille). Chez nous « certain rang » : 0. |
| « Strictement » croissante / décroissante, « constante » | moyenne | **confirmé** | Benmoussa p. 1 : définitions de strictement croissante (uₙ < uₙ₊₁), strictement décroissante, constante (uₙ = uₙ₊₁). Chez nous « strictement croissante » : 0. |
| Phrase « géométrique de raison q et de premier terme v₀ = … » | moyenne | **confirmé** | Benmoussa p. 1 et p. 2 : « géométrique de raison q et de premier terme uₙ₀ » (même tournure pour l'arithmétique). Sigmaths p. 2 ne cite que la raison. |
| Écrire « n → +∞ » sous lim | moyenne | **confirmé** (tous) | Benmoussa p. 2 à 11 ; Sigmaths p. 3 ; Atlas p. 1 ; Atmani p. 1-2. Chez nous, les 3 occurrences de « n → +∞ » sont des flèches (« n, n², √n → +∞ »), jamais sous lim. |
| Définitions de la limite par intervalles | basse | **confirmé** | Benmoussa p. 3 (intervalle ouvert de centre ℓ ; ]A, +∞[ « à partir d'un certain rang »). Sa définition de −∞ écrit « ]−∞, A[ pour tout A de ℝ⁺ » (il faut −A) : ne pas recopier. Hors exigence, une ligne au plus. |
| lim uₙ = −∞ ⇔ lim (−uₙ) = +∞ | basse | **confirmé** | Atmani p. 1 (D.1). |
| Exemples cos n, (−1)ⁿ, sin n / n, n² + (−1)ⁿ | basse | **confirmé** | Benmoussa p. 4 ((−1)ⁿ sans limite), p. 6 ((−1)ⁿ/n − 5 → −5 ; 2n + cos n → +∞ ; cos n / n → 0 par |vₙ − 0| ≤ 1/n), p. 8 (cos n / n) ; Atlas p. 2 ((−1)ⁿ bornée non convergente). Chez nous, (−1)ⁿ n'est que dans le texte alternatif d'une image. |
| FI ∞ − ∞ d'un polynôme ; conjugué | basse | **confirmé en partie** | Atmani p. 1, remarque 1 : « la limite d'une suite polynôme est la limite de son plus grand terme ». Le conjugué n'est chez aucun autre. Chez nous « polyn » : 0. |
| Sommes télescopiques, notation Σ, produit Π | basse | **en partie** : la notation Σ est confirmée ; télescopiques et Π restent propres au Prof Fayssal | Benmoussa p. 1-2 : Sₙ = Σ_{i=p}^{n} uᵢ dans les formules de somme. Chez nous « Σ » : 0. |
| De uₙ ≤ 2 − 1/n, majorée par une constante | basse | **pas chez les autres** | Aucun des cinq documents. |
| Notation (uₙ)ₙ≥ₙ₀ | basse | **confirmé, et partout** : à monter en moyenne | Benmoussa p. 1 à 11 ; Sigmaths p. 1 à 3 ; AlloSchool p. 1 ; Atlas p. 2 (« pour tout n ≥ n₀ »). Formules uₙ = uₙ₀ + (n − n₀)r et uₙ = uₙ₀·qⁿ⁻ⁿ⁰ (Benmoussa p. 1-2, Sigmaths p. 2). Chez nous « n₀ » : 0 (nous avons uₚ, ce qui suffit pour la formule). |
| Notation : montrer une fois ∀ | (notation) | **confirmé, mais le premier audit se trompe en partie sur notre cours** | Tous l'utilisent (Benmoussa p. 1, Atmani p. 1, Sigmaths p. 1). Chez nous, ∀ apparaît déjà 3 fois, dans les démonstrations rédigées (« d'après le principe de récurrence, ∀n ∈ ℕ, uₙ > 1 »), mais jamais à l'écran ni au cahier. |
| Notation : écrire « théorème des gendarmes » à l'écran | (notation) | **confirmé** | Atlas p. 1 (« Théorème des gendarmes ») ; Benmoussa p. 5 dit « critères de convergence ». Chez nous, le nom est déjà dans une réaction écrite (« critère de comparaison (théorème des gendarmes) ») et dans la voix mixed, pas à l'écran. |
| Notation : ajouter la somme en symboles 1 + q + … + qⁿ = (1 − qⁿ⁺¹)/(1 − q) | (notation) | **à revoir** : la forme en symboles existe déjà chez nous | su_p2 et su_p3 écrivent déjà v₀(1 − qⁿ⁺¹)/(1 − q) au cahier. Il manque seulement la forme générale à su_a9b : uₚ(1 − qⁿ⁻ᵖ⁺¹)/(1 − q) (Atmani p. 1, Sigmaths p. 2, Atlas p. 1 avec u₀). |
| Oral seulement (points isolés, vérifier avec n = 0, exemples rédigés, « le correcteur refuse ») | (oral) | aucun autre prof ne les traite | Rien à confirmer ni à contredire. |

### B. Nouvelles pistes

| Priorité | Catégorie | Ce que dit le professeur (prof, page) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | propriété / rédaction | Passage à la limite dans une inégalité : si (uₙ) converge vers L et uₙ ≥ 0 à partir d'un rang, alors L ≥ 0 ; si vₙ ≤ uₙ et les deux convergent, lim vₙ ≤ lim uₙ (Atmani p. 1, F.1 et F.2 ; Benmoussa p. 5). C'est la propriété qui justifie « tous les uₙ sont dans I, donc ℓ ∈ I ». Une inégalité stricte devient large à la limite. | su_f6 écrit « Tous les uₙ sont dans [1 ; 2], donc ℓ ∈ [1 ; 2] » sans nommer la propriété. su_c3 donne ℓ ≤ M pour un majorant seulement. « ℓ ≥ » : 0. Le mot « strict devient large » : absent. | su_f6_choisir (la raison de ℓ ∈ I) et su_c3_plafond_limite (une ligne : a ≤ uₙ ≤ b ⇒ a ≤ ℓ ≤ b, même si les inégalités sont strictes) |
| moyenne | remarque / piège | « Toute suite convergente est bornée », mais bornée n'entraîne pas convergente : (−1)ⁿ est bornée et sans limite (Atmani p. 1 ; Atlas p. 2, piège n° 2). | Absent. Le catalogue écrit « Monotone et bornée ⇒ convergente » ; rien ne dit que « monotone » est indispensable. | su_c2_couple (à côté du « mauvais couple ») |
| moyenne | propriété | « Toute suite croissante et non majorée tend vers +∞ ; toute suite décroissante et non minorée tend vers −∞ » (Atmani p. 1). | su_c1 dit seulement « Sans plafond, elle **peut** partir vers +∞ (exemple : n²) ». « non majorée » : 0. | su_c1_plafond ou su_c2_couple |
| basse | propriété | Si une suite a une limite, cette limite est **unique** (Benmoussa p. 3, qui s'en sert p. 4 pour (−1)ⁿ ; Atmani p. 1). | « unique » : 0. | su_l1_converge |
| basse | propriété | lim (uₙ − ℓ) = 0 ⇔ lim uₙ = ℓ (Benmoussa p. 3) ; lim |uₙ| = 0 ⇔ lim uₙ = 0 (Atmani p. 1). | su_c8 utilise « lim (2 − uₙ) = 0, donc lim uₙ = 2 » sans énoncer la règle. « |uₙ| » : 0. | su_c8_ecart (une ligne) |
| basse | définition | Bornée ⇔ il existe A > 0 tel que |uₙ| ≤ A pour tout n (Benmoussa p. 1 ; Atmani p. 1). | Absent (« |uₙ| » : 0). | su_b2_bornee (facultatif) |
| basse | formule | Somme géométrique avec q = 1 : Sₙ = (n − p + 1)uₚ (Benmoussa p. 2 ; Atmani p. 1). | Nous écrivons seulement « q ≠ 1 ». | su_a9b_somme_geo |
| basse | formule | Trois termes consécutifs : arithmétique a + c = 2b ; géométrique a × c = b² (Benmoussa p. 1-2). | « moyenne » : 0. | su_a4 / su_a6 (facultatif, utile en problème 1.1.5) |
| basse | méthode | Résoudre ℓ = f(ℓ) **avant** la convergence pour avoir la limite candidate, qui donne souvent la borne à prouver par récurrence (Atlas p. 3). | su_f2 conjecture avec le dessin seulement. « candidat » : 0. | su_f2_place_u0 (une phrase, comme conjecture) |
| basse | exemple | nʳ avec r ∈ ℚ* : lim ⁷√(n³) = lim n^(3/7) = +∞ (Benmoussa p. 7). | nᵅ présent, mais aucun exemple avec une racine n-ième (« ∛ » : 0). | su_l2_reference |

Écartés : suites adjacentes (AlloSchool, cours SM : hors cadre) ; suite périodique (Benmoussa p. 1 : aucun objectif du cadre ne la demande).

### C. Désaccords entre professeurs

- **Nom de la suite** : (uₙ)ₙ≥ₙ₀ (Benmoussa, Sigmaths, AlloSchool), (uₙ)ₙ∈I (Atmani), (uₙ) (Atlas, nous). Garder (uₙ) et montrer une fois (uₙ)ₙ≥ₙ₀.
- **Lettre de la limite** : ℓ (Benmoussa, Atlas), l (Sigmaths, Atmani, AlloSchool), L (Atmani F.1). Garder ℓ.
- **Comparaison** : « à partir d'un certain rang » (∃N)(∀n > N) chez Atmani, « à partir d'un rang p » chez Benmoussa, « ∀n ≥ n₀ » chez Sigmaths, rien chez Atlas. Garder « à partir d'un certain rang ». Nom : « critères de convergence » (Benmoussa), « théorème des gendarmes » (Atlas). Garder « critère de comparaison (théorème des gendarmes) ».
- **Passage à la limite** : Benmoussa p. 5 écrit « si lim uₙ = ℓ et uₙ > 0 alors ℓ > 0 ». C'est **faux** (1/n > 0 et la limite est 0). Atmani p. 1 a la bonne forme : uₙ ≥ 0 ⇒ L ≥ 0. Garder la forme large.
- **Sens de variation de uₙ₊₁ = f(uₙ)** : Atlas p. 2 dit « comparer u₁ et u₀, puis raisonner ». Notre su_m1 dit « u₁ > u₀ ne suffit pas » et Benmoussa p. 10 étudie le signe de uₙ₊₁ − uₙ. La méthode d'Atlas ne vaut que si f est croissante sur I, avec une récurrence. Garder notre méthode (signe de uₙ₊₁ − uₙ ou de f(x) − x).
- **Limite de qⁿ** : Atlas p. 3 écrit « |q| > 1 : uₙ → ±∞ », ce qui contredit sa propre p. 1 (q ≤ −1 : pas de limite). Benmoussa p. 7, Sigmaths p. 3 et Atmani p. 2 donnent les quatre cas. Garder nos quatre cas.
- **Justifier la continuité** : « continue sur son domaine de définition » (Benmoussa p. 10) ou « car dérivable » (Prof Fayssal). Les deux sont acceptables. Garder une phrase avec « car ».
- **Somme géométrique** : uₚ(1 − q^(n−p+1))/(1 − q) (Atmani, Sigmaths, Atlas) ou uₚ(q^(n−p+1) − 1)/(q − 1) (Benmoussa p. 2). Les deux formes sont égales. Garder notre forme en mots, plus la forme en (1 − q).
- **Titres de la récurrence** : Initialisation (Atlas) ou Vérification (Sigmaths). Sigmaths écrit l'hérédité « à un rang n > n₀ » : il faut n ≥ n₀. Garder Initialisation / Hérédité / Conclusion.
- **Monotonie stricte** : Benmoussa la définit par uₙ < uₙ₊₁ ; le Prof Fayssal passe par le signe de la différence. Garder notre définition large et ajouter « strictement » avec l'inégalité stricte.
- **Équation f(x) = x avec une racine** : Benmoussa p. 11 écrit « √(x + 6) = x ⇔ x + 6 = x² ». L'équivalence est fausse sans x ≥ 0. Chez nous, la démonstration écrit « on élève au carré … donc », puis élimine −1 avec ℓ ∈ [0 ; 2]. C'est juste : garder notre version.
- **Coquilles de Benmoussa à ne pas recopier** : p. 1, « minorée … uₙ ≤ M » et « bornée si majorée et bornée » ; p. 2, géométrique « ou encore uₙ₊₁ = uₙ + r » ; p. 7, « −1 < 8/7 < 1 » ; p. 10, f(I) = [√6 ; 3] puis [√3, 3].

---

## Primitives

Sources lues : Pr Benmoussa Mohammed, « Fonctions primitives », cours 2 PC + 2 SV, PDF p. 1 et p. 2 (lues en image) ; Pr Atmani Najib, « Résumé de cours Fonctions primitives », 2e Bac Sciences ex, PDF p. 1 (lue en image). Notre cours : texte complet de math_ch4_primitives (écran, cahier, voix, exercices). Cadre : 1.2.14, 1.2.15 (1.3.1 pour l'intégrale).

Vérification de notre cours : les constats du premier audit sur notre texte sont exacts (pr_b1 points 4 et 6 sans intervalle, sans condition et sans + k ; pr_b1 sans xʳ, 1/xⁿ, sin(ax + b), 1 + tan²x, u′uʳ, (ax + b)ⁿ ; pr_l1 sans hypothèse ; u toujours polynôme ; aucun « sin³ », « cos³ », « sin² » ; u′uⁿ limité à n ∈ ℕ* en pr_c1_b). Aucune erreur du premier audit trouvée.

### A. Les constats du premier audit, contre-vérifiés

| Constat (court) | Priorité | Verdict | Preuve (prof, page) |
|---|---|---|---|
| Fiche pr_b1 : chaque formule avec son intervalle / sa condition et « + C » | haute | Confirmé en partie. « + C, C ∈ ℝ » : confirmé (les deux tableaux l'écrivent à chaque ligne). Intervalle et condition par ligne : pas chez les autres (aucun des deux tableaux n'a de colonne « Sur I » ni « u > 0 ») ; reste propre au Prof Fayssal, mais à garder (sans condition, f′/√f ou xʳ sont faux sur ℝ) | Atmani p. 1 (« + C, C ∈ ℝ » sur chaque ligne, aucun intervalle) ; Benmoussa p. 2 (colonne « F primitives de f (c ∈ ℝ) », aucun intervalle, aucune condition) |
| Fiche pr_b1 incomplète (xʳ, 1/xⁿ, sin(ax + b), 1 + tan²x, u′uʳ, (ax + b)ⁿ) | haute | Confirmé : un résumé complet contient ces lignes | Benmoussa p. 2 (xʳ, sin(ax + b), cos(ax + b), 1 + tan²x = 1/cos²x, f′fʳ, f′(ax + b)) ; Atmani p. 1 (1/xⁿ, n ∈ ℕ \ {0, 1} ; xⁿ, n ∈ ℤ \ {−1}) |
| Exemple avec u trigonométrique (cos x·sin²x → (1/3)sin³x) | haute | Pas chez les autres (aucun exemple de forme composée) ; reste propre au Prof Fayssal. À garder quand même : forme fréquente dans les intégrales | Benmoussa p. 1–2 et Atmani p. 1 : formules seulement, aucun exemple composé |
| Puissances négatives : faire apparaître u, (x + 2)⁻³, u′uⁿ avec n < 0 | moyenne | Confirmé pour la formule : u′uⁿ avec n ∈ ℤ \ {−1} et f′/fⁿ. La méthode « faire apparaître u au numérateur » reste propre au Prof Fayssal | Atmani p. 1 (f′fⁿ, n ∈ ℤ \ {−1} ; f′/fⁿ, n ∈ ℕ \ {0, 1} → −1/((n − 1)fⁿ⁻¹)) ; Benmoussa p. 2 (xⁿ, n ∈ ℤ \ {−1}) |
| cos³x = cos x − cos x·sin²x | moyenne | Pas chez les autres ; propre au Prof Fayssal | — |
| Linéarité avec hypothèses « sur I » | moyenne | Confirmé pour l'énoncé (F primitive de f et G de g sur le même I) ; la démonstration (F + G)′ = F′ + G′ reste propre au Prof Fayssal | Atmani p. 1 (« Si F est une primitive de f sur I et G une primitive de g sur I et α un réel… sur I ») ; Benmoussa p. 2 (« F et G sont les primitives respectivement de f et g sur I ») |
| Exemple u′u → u²/2 (n = 1) | basse | Pas chez les autres (aucun exemple) | — |
| 1 + tan²x sur ]−π/2 + kπ ; π/2 + kπ[ | basse | Pas chez les autres (Benmoussa donne la ligne sans intervalle) | Benmoussa p. 2 |
| Remarque « forme explicite pas toujours connue » | basse | Pas chez les autres (Atmani a une autre remarque, voir B) | — |

### B. Nouvelles pistes

| Priorité | Catégorie | Ce que dit le professeur (prof, page) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| moyenne | propriété | Unicité énoncée avec ses hypothèses : « soit x₀ ∈ I et y₀ ∈ ℝ ; il existe une seule (unique) primitive G de f sur I telle que G(x₀) = y₀ » (Benmoussa p. 1, f ; Atmani p. 1) | Seulement une méthode sur un exemple (pr_e6, pr_e7 : « une seule primitive vérifie la condition ») ; jamais « x₀ ∈ I » ni l'énoncé général (recherché : « x₀ ∈ I », « unique ») | pr_e6 : cahier, propriété en une ligne avant la méthode ; pr_b1 point 3 |
| moyenne | formule | u′/uⁿ (n ≥ 2) → −1/((n − 1)uⁿ⁻¹) + C (Atmani p. 1 : f′/fⁿ, n ∈ ℕ \ {0, 1}) | Seulement u′/u² (pr_c6) et 1/xⁿ pour x seul (pr_u4_b) ; aucun « u′/uⁿ », « /uⁿ », « u′/u³ » | pr_c6 (ligne générale après u′/u², avec u ≠ 0 sur I) ; pr_b1 point 6. Va avec le constat « puissances négatives » de A |
| moyenne | formule / méthode | Règle générale f(ax + b) : si F est une primitive de f, alors x ↦ (1/a)F(ax + b) est une primitive de x ↦ f(ax + b), a ≠ 0 (Benmoussa p. 2, « h = f′(ax + b), a ≠ 0 → H = (1/a)f(ax + b) ») | Seulement des cas : cos(ax + b), sin(ax + b) (pr_u7), (ax + b)ⁿ (pr_c4) ; aucune règle générale (recherché : « f(ax + b) », « (1/a)F ») | pr_u7 ou pr_c4 : une ligne « diviser par a, le nombre collé à x » dite comme règle générale ; sert aussi pour 1/(ax + b)², 1/√(ax + b) |
| basse | remarque | « La continuité dans le théorème précédent est une condition suffisante qui n'est pas nécessaire » (Atmani p. 1) | Absent (recherché : « suffisant », « nécessaire » : seul un « nécessaire » sans rapport, voix de pr_c5) | pr_e1 (une phrase, voix ou exercice vrai/faux) |
| basse | formule | Règle générale des composées : u′ × (g′ ∘ u) → g ∘ u (Benmoussa p. 2, « h = f′ × g′∘f → H = g∘f ») | Seulement des cas (u′uⁿ, u′cos u, u′sin u…) ; aucun « ∘ » | pr_r3 (organigramme) ou pr_c9 : une phrase « toutes les formes sont (g ∘ u)′ = u′ × g′(u) lue à l'envers » |

Écartés : f′/f → ln f, eˣ, f′eᶠ (Atmani p. 1) : chapitres ln et exp, déjà annoncés en pr_x4. « Les seules opérations sont la somme et le produit par un réel » (Atmani p. 1) : déjà chez nous (pr_l2, pr_r2). f(x) = 0 → c et f(x) = x → x²/2 (Benmoussa p. 2) : déjà couverts (pr_e4_b, pr_u2).

### C. Désaccords entre professeurs

| Point | Benmoussa | Atmani | Fayssal (premier audit) | À garder |
|---|---|---|---|---|
| Définition | « ∀x ∈ I : F′(x) = f(x) », sans « F dérivable sur I » (p. 1) | « F est dérivable sur I » et « (∀x ∈ I) F′(x) = f(x) » (p. 1) | f continue sur I en hypothèse | La nôtre (= Atmani) : dérivable + pour tout x ∈ I |
| Nom de la constante | c, c′ (p. 1–2) | C, et λ pour l'écart de deux primitives (p. 1) | C | Garder k ; dire une fois « on la note aussi C » (pr_e4_b) |
| Nom de la fonction intérieure | f (f′fⁿ, f′/√f, g∘f) (p. 2) | f (f′fⁿ, f′/fⁿ) (p. 1) | u | Garder u : « f » désigne déjà la fonction qu'on primitive |
| Conditions | aucune pour xʳ (r ∈ ℚ \ {−1}), f′fʳ, f′/√f, xⁿ (n ∈ ℤ) (p. 2) | aucune pour f′/√f ni xⁿ (n ∈ ℤ \ {−1}) (p. 1) | u ≠ 0 pour uʳ, « v > 0 » pour u′/√u | Garder nos conditions (x > 0, u > 0, u ≠ 0 sur I) : les deux résumés sont incomplets |
| Puissances n | xⁿ, n ∈ ℤ \ {−1} en une ligne | xⁿ (n ∈ ℕ), puis 1/xⁿ, puis n ∈ ℤ \ {−1} | xⁿ et 1/x² | Garder n ∈ ℕ* puis 1/xⁿ (pr_u4_b) ; ajouter u′/uⁿ (B) |
| Ordre | Opérations (linéarité, dérivées reconnues) avant/à côté du tableau | Tableau, puis opérations | Tableau, puis linéarité | Garder le nôtre (tableau, puis linéarité, puis formes) |
| ln et exp | absents | dans le même tableau (ln(f), sans valeur absolue) | absents | Garder « plus tard » (pr_x4), avec ln\|u\| |

Erreur dans un document : Benmoussa p. 2, exemple de linéarité « f(x) = 3x … F(x) = 6x² + c » est faux (une primitive de 3x est (3/2)x²). Ne pas reprendre.

---

## Fonction logarithme népérien

Sources lues : Pr Benmoussa Mohammed, cours complet « Fonctions logarithmes » 2 PC/SVT (13 p., toutes lues en image) ; Pr Atmani Najib, résumé de cours (1 p., lue en image) ; atlasmaths, fiche de cours SE (3 p., lues en image). Notre cours : texte de chaque diapo et recherche dans le JSON complet (écran, voix, exercices, réactions). Cadre officiel : 1.2.13, 1.2.16 à 1.2.19, 1.2.22.

### A. Les constats du premier audit, contre-vérifiés

| Constat (court) | Priorité | Verdict | Preuve (prof, page) |
|---|---|---|---|
| Limite de ln(u(x)) par composition + phrase « asymptote verticale x = a » | haute | confirmé | Benmoussa p.12 : lim_{x→−1⁺} ln(x+1) = −∞ « car lim x+1 = 0⁺ », donc asymptote verticale x = −1 ; p.5 : limite de ln(x+2) en posant t = x+2 |
| Étude complète d'une fonction ln(u) | haute | confirmé | Benmoussa p.12-13 : étude de ln(x+1)/ln 5 (domaine, limites par composition, asymptote, branche, f′, tableau, courbe). Le support est log₅ (hors cadre) : prendre la même démarche avec ln(x+1) ou ln(u) |
| Concavité par f″ | haute | pas chez les autres (reste propre au Prof Fayssal) | Aucun f″ chez Benmoussa, Atmani, atlas. À garder quand même : cadre 1.2.13 et 1.2.22 (concavité, points d'inflexion) |
| Croissances comparées avec xⁿ (n ∈ ℕ*) | haute | confirmé | Benmoussa p.4 (tableau : lim ln x / xⁿ = 0 ; lim_{0⁺} xⁿ ln x = 0⁻) ; Atmani p.1 (limites 4 et 5, avec r ∈ ℚ*₊). Atlas : n = 1 seulement |
| Unique solution α (TVI) avec ln | moyenne | pas chez les autres (propre au Prof Fayssal) | Aucun α chez les trois. Garder en moyenne : le TVI est au cadre (1.2.2-1.2.4) et le geste revient au national |
| Tableau de variations complet de ln | moyenne | confirmé | Benmoussa p.7 : double barre en 0, f′ +, −∞ → 0 (en 1) → +∞, puis la courbe avec e |
| ln continue et strictement croissante ⇒ e unique | moyenne | confirmé | Benmoussa p.1 (« continue car dérivable ») et p.8 (« continue, strictement croissante, f(]0,+∞[) = ℝ, donc f(x) = 1 admet une solution et une seule, notée e ») ; Atmani p.1 (« continue et strictement croissante ») |
| Changement de variable X = 1/x | moyenne | pas chez les autres pour X = 1/x ; un autre changement (t = x + a) est confirmé, voir B2 | Benmoussa p.5, p.12 |
| Inéquation en (ln x)² | moyenne | pas chez les autres (propre au Prof Fayssal) | — |
| Primitive de 1/(x ln x) | moyenne | pas chez les autres (propre au Prof Fayssal) | Benmoussa p.5 a seulement la limite de 1/(x ln x) |
| 10ˣ ≤ a, 10ˣ ≥ a | moyenne | confirmé | Atmani p.1 : log x = r ⇔ x = 10ʳ ; log x > r ⇔ x > 10ʳ. Cadre 1.2.18 |
| Quantificateur ∀ | moyenne | confirmé | Benmoussa p.1 (∀a,b ∈ ]0,+∞[ : a < b ⇔ ln a < ln b), p.6 (∀x ∈ I : u(x) ≠ 0) ; Atmani p.1 partout (∀x > 0 ; ∀y > 0 ; ∀r ∈ ℚ). Atlas : non |
| D_E / D_I, « S = … » | basse | confirmé (passer en moyenne : 2 professeurs sur 3 l'écrivent) | Benmoussa p.2 et p.11 : « On détermine D_E », « On résout l'équation dans D_E », « Conclusion : S = … » |
| (ln\|u\|)′ = u′/u si u ≠ 0 sur I | basse | confirmé (passer en moyenne) | Benmoussa p.5-6 (démonstration en deux cas + exemple ln\|x² − x\|) ; Atmani p.1 (c'est sa seule forme du théorème). Atlas : u > 0 seulement |
| x, y < 0 : ln(xy) = ln\|x\| + ln\|y\| ; ln x²ⁿ | basse | pas chez les autres (propre au Prof Fayssal) | — |
| ln : ]0;+∞[ → ℝ | basse | confirmé | Atlas p.2 (« ln : ]0,+∞[ → ℝ ») ; Benmoussa p.8 (f(]0,+∞[) = ℝ) |
| Démonstrations (récurrence ln xⁿ, encadrement 2√x) | basse | pas chez les autres | Benmoussa p.3 démontre seulement ln(1/a) et ln(a/b) à partir du produit admis, ce que nous faisons déjà (ln_a3, ln_a3_b) |
| Liste des formes indéterminées | basse | pas chez les autres | — |
| Exemples avec quantité conjuguée | basse | confirmé | Benmoussa p.4 : ln²(3−√2) − ln²(3+√2) par a² − b² et (3−√2)(3+√2) = 7 |
| 0 ≤ ln(1+x) ≤ x et suite par gendarmes | basse | pas chez les autres | — |
| e irrationnel | basse | confirmé | Benmoussa p.8 (« un nombre irrationnel ») |
| Plan comparé : domaines de l'Ex. 04 (√(2 − ln x)) « couverts par ln_d3 » | — | à revoir : le premier audit s'est trompé | Notre cours n'a aucun domaine avec une racine de ln (recherche « √( » et « √ln » : 0 occurrence). Benmoussa p.1-2 le traite aussi : voir B4 |

Oral seulement : l'unicité de e (ln_c3) est écrite chez Benmoussa p.8 avec « continue et strictement croissante » : le constat est confirmé. Les autres points « à l'oral » ne sont pas traités par les autres professeurs.

### B. Nouvelles pistes

| Priorité | Catégorie | Ce que dit le professeur (prof, page) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | rédaction | Justifier la branche parabolique : « lim ln x = +∞ et lim (ln x)/x = 0, donc (C_f) admet une branche parabolique de direction l'axe des abscisses » (Benmoussa p.4 et p.7) | ln_l1 donne la branche avant d'avoir vu lim (ln x)/x (ln_l3), justifiée seulement par « elle monte lentement ». Aucun « f(x)/x » pour ln dans le chapitre (seul f(x)/x : ln_l8, en 0) | ln_l3 (une ligne qui conclut la branche) ; renvoi dans la trace de ln_l1 |
| moyenne | méthode | lim_{x→+∞} ln(x+2)/x : écrire ln(x+2)/(x+2) × (x+2)/x, poser t = x + 2, donc 0 × 1 = 0 (Benmoussa p.5) ; même geste pour f(x)/x avec ln(x+1) (p.12) | Absent : nos limites portent sur ln x ; seul changement de variable t = √x (ln_l7) | ln_partie6, après ln_l7 (avec le X = 1/x du premier audit) |
| moyenne | définition / rédaction | x ∈ D_f ⇔ x ∈ D_u et u(x) > 0 (Benmoussa p.5) | ln_d1 écrit seulement « x ∈ D_f ⇔ u(x) > 0 » ; la condition « u existe » n'apparaît que dans ln_d2 (3 − x ≠ 0) | Trace de ln_d1 |
| moyenne | exemple / méthode | Domaine de √(ln x) : x > 0 et ln x ≥ 0 ⇔ x ≥ 1, D_f = [1;+∞[ (Benmoussa p.1-2 ; le Prof Fayssal a √(2 − ln x)) | Absent (0 occurrence) | Exercice de fin de ln_d3 |
| basse | exemple | Domaine de 1/(3 − ln x) : ln x ≠ 3 = ln e³ ⇔ x ≠ e³ (Benmoussa p.8) | ln_d3 traite seulement ln x ≠ 0 | Exercice de fin de ln_d3 |
| basse | méthode | lim_{x→0⁺} 1/(x ln x) = −∞ parce que x ln x → 0⁻ (Benmoussa p.4-5) | ln_l4 écrit x ln x < 0 pour 0 < x < 1, sans l'utiliser | Exercice de fin de ln_l4 |
| basse | méthode | lim_{x→0} ln(x+1)/x³ = lim ln(x+1)/x × 1/x² = +∞ (Benmoussa p.5) | ln_l5 a seulement ln(1+3x)/(2x) | Exercice de fin de ln_l5 |
| basse | formule | ln x < r ⇔ 0 < x < eʳ ; ln x > r ⇔ x > eʳ, écrites comme règles (atlas p.2 ; Atmani p.1 pour r = 0) | Seulement à travers des exercices (ln_q3 : ln x > ln e²) ; ln_b1 point 4 donne ln x = r seulement | Trace de ln_q3, ln_b1 point 4 |
| basse | formule | ln ∛a = ⅓ ln a (Benmoussa p.3) | Seulement ln(aʳ) = r ln a ; aucun ∛ | ln_a4_b (une ligne) |
| basse | vocabulaire | u′/u s'appelle la « dérivée logarithmique » de u (Benmoussa p.6) | Absent. Mot absent du cadre : à dire seulement à l'oral | ln_v1 (voix), facultatif |

Vérifié présent chez nous, donc pas de piste : ln x = ln y et ln x ≤ ln y (ln_c4, exercice de ln_q3), pièges d'atlas (ln_a6, ln_v1, ln_c2, ln_q2), f(x) = x ln x − x (ln_p3, ln_e5), primitive 5/(x−2) sur ]2;+∞[ sans valeur absolue (ln_p2, cas ]−∞;3[), valeurs approchées à partir de ln 2 et ln 3 (ln_a1). Écarté (hors cadre ou hors chapitre) : log_a et ses exercices (Benmoussa p.8-13, Atmani), e^(ln x) = x (chapitre exponentielle), décibels (atlas p.2).

### C. Désaccords entre professeurs

| Point | Ce que disent les professeurs | À garder |
|---|---|---|
| Définition de ln | Primitive de 1/x qui s'annule en 1 (Benmoussa p.1, Fayssal, nous) ; « l'unique fonction dérivable avec ln 1 = 0 et (ln x)′ = 1/x » (Atmani) ; atlas met ln e = 1 dans la définition (c'est une conséquence) | Notre définition |
| Exposant des croissances comparées | n (Benmoussa), n ∈ ℕ* (Fayssal), r ∈ ℚ*₊ (Atmani), n = 1 seulement (atlas) | n ∈ ℕ* |
| lim_{0⁺} x ln x | 0⁻ (Benmoussa p.4) ; 0 (Atmani, atlas, nous) | Écrire 0 ; dire que c'est 0⁻ quand on divise par x ln x |
| Dérivée de ln u | u > 0 (atlas, nous) ; ln\|u\| avec u ≠ 0 (Atmani) ; les deux (Benmoussa) | Les deux : u > 0, puis ln\|u\| |
| Primitives de u′/u | « F(x) = ln\|u(x)\| + c avec c ∈ ℝ » (Benmoussa p.6) ; « + Cte » (Atmani) ; nous « une primitive est ln u » | « + C, C ∈ ℝ » quand on demande les primitives |
| Domaine d'une équation / inéquation | D_E et D_E′ (Benmoussa) ; D_E et D_I (Fayssal) ; rien (nous, atlas) | D_E et D_I |
| Carré de ln | ln²(x), lnⁿ x (Benmoussa p.3) ; (ln x)² (nous) | (ln x)², en disant que ln²x = (ln x)². Attention : une réaction de ln_e3 (reponses_fin_de_cours e1s0) écrit déjà « ½ ln²x », à aligner |
| Logarithme décimal | « Log » et log₁₀ (Benmoussa p.8) ; « log » (Atmani, atlas, nous) | log |
| Ordre | Benmoussa : définition, conséquences, domaines, équations, signe, règles, limites, ln(u), puis étude complète de ln en dernier ; Atmani et atlas : définition, règles, limites, dérivée ; nous : courbe, domaine, règles… | Garder notre ordre ; ajouter le tableau de variations complet de ln après les limites (comme Benmoussa p.7) |

Erreurs des autres professeurs à ne pas copier : Benmoussa p.12, « branche parabolique de direction l'axe des ordonnées » alors que lim f(x)/x = 0 (c'est l'axe des abscisses) ; p.12, inéquation « ≥ » résolue en « > », donc S = ]1;+∞[ au lieu de [1;+∞[ ; p.10, f′ « + » dans le tableau pour 0 < a < 1 ; p.2, (E′) écrite « = 0 » mais résolue « ≤ 0 » ; p.4, « donc ln 8 = 2,1 » à la place de ln ∛2 ; p.11, 10²⁰¹³ devenu 10²⁰¹⁹.

---

## Nombres complexes (partie 1)

Sources lues : Pr Atmani Najib, « Cours et exercices… nombres complexes (Partie 1) », 2 BAC PC et SVT (ch6_moutamadris.pdf), pages 1 à 19 lues en image ; Pr Atmani Najib, « Résumé de cours sur les nombres complexes » (m_resume-Nombres-complexes-12…pdf), pages 1 à 3 lues en image (p. 3 = partie 2 : exponentielle, équations, transformations). Notre cours : texte des diapos + JSON (recherches par mots). Cadre : objectifs 2.4.1 à 2.4.9 ; fiche `operations_formes` (hors_cadre, decisions) et perimetre `geometrie_complexe`.
Notation des pages : « A p. N » = cours Atmani, page N ; « A-rés. p. N » = résumé Atmani.

### A. Les constats du premier audit, contre-vérifiés

Aucune erreur du premier audit sur notre cours : chaque absence a été revérifiée dans le JSON (0 flèche de vecteur ; pas de « c + id ≠ 0 », « k ∈ ℤ », « radian », « médiatrice », « ensemble des points », « z̿ », « kz », « inégalité »).

| Constat (court) | Priorité | Verdict | Preuve (prof, page) |
|---|---|---|---|
| Mesure d'angle (u⃗, AB⃗) ≡ arg(z_B − z_A), (AB⃗, AC⃗) ≡ arg((c − a)/(b − a)), (AB⃗, CD⃗) | haute | confirmé | A p. 14-15 (démonstration par Chasles + propriété 1 à 4) ; A-rés. p. 2 (F 1 à 4) |
| Nature d'un triangle par le quotient (isocèle rectangle, équilatéral) | haute | confirmé | A p. 15 : (z_B − z_C)/(z_A − z_C) = 2i ⇒ (CA⃗, CB⃗) ≡ π/2 [2π] ⇒ « ABC est rectangle en C » et \|2i\| = 2 ⇒ BC = 2AC ; équilatéral par les distances A p. 9 (voir B1) |
| Orthogonalité / parallélisme par le quotient | haute | confirmé | A p. 17 (corollaires 2.2, 2.3) ; A-rés. p. 2 (6, 7) ; écrit avec arg ≡ 0 ou π [2π], ≡ π/2 ou −π/2 [2π] (pas « imaginaire pur ») |
| Ensembles de points : cercle \|z − z_A\| = r, médiatrice \|z − z_A\| = \|z − z_B\|, transformer d'abord, 2 méthodes | haute | confirmé | A p. 9-10 (Ex. 2, Ex. 8, 9, 10 : « Méthode géométrique » / « Méthode algébrique » ; \|iz + 3\| = \|i\|·\|z − 3i\|) ; A p. 18 (Ex. 20) ; phrase « L'ensemble cherché est le cercle de centre A et de rayon 5 » (A p. 9) |
| Flèches de vecteurs AB⃗, (u⃗, OM⃗), (O, u⃗, v⃗) | haute | confirmé | A p. 3-4 (aff(AB⃗), AC⃗ = αAB⃗), p. 9 (‖AB⃗‖ = AB), p. 10, 14-15 ; A-rés. p. 1-2 |
| Conditions « z ≠ 0 », « z′ ≠ 0 », « non nuls » écrites | moyenne | confirmé | A p. 2 (quotient « z′ ≠ 0 »), p. 5 (conj(1/z), conj(z′/z) « si z ≠ 0 »), p. 8 (\|1/z\|, \|z′/z\| « si z ≠ 0 »), p. 13 (« z et z′ non nuls ») |
| Résoudre dans ℂ une équation avec z̄ ; conclure « S = {…} » | moyenne | confirmé | A p. 7 Ex. 3 : 2z + iz̄ = 5 − 4i ⇒ « Donc : S = {14/3 − 13/3 i} » ; Ex. 5 A (3 équations) |
| Ensemble des M tels qu'une expression soit réelle / imaginaire pure ; « privé du point » | moyenne | confirmé | A p. 7 Ex. 4 (U = (z − 2i)(z̄ − 1) : droite, cercle), Ex. 5 B ; A p. 8 Ex. 7 ; A p. 17-18 Ex. 19 (« le cercle (C) privé de A », condition z ≠ 1) |
| Parallélogramme : AB⃗ = DC⃗ ⇔ z_B − z_A = z_C − z_D | moyenne | confirmé | A p. 4 (Ex. 2.6 : z_D = z_C + z_A − z_B), p. 5 (Ex. 1.4, rédaction complète) ; losange A p. 15-16 |
| Égalité sous forme trigo : z = z′ ⇔ même module et même argument | moyenne | pas chez les autres (propre au Prof Fayssal) | A p. 12 donne seulement « z = r(cos θ + i sin θ), r > 0 ⇒ \|z\| = r et arg z ≡ θ [2π] » (déjà dans nc_t1) |
| « arg z + 2kπ, k ∈ ℤ » ; « une mesure, en radians » | moyenne | confirmé pour « en radian » ; 2kπ propre au Prof Fayssal | A p. 10 et A-rés. p. 2 : « une mesure (en radian) de l'angle (u⃗, OM⃗) » ; Atmani écrit seulement [2π] |
| Double conjugué z̿ = z ; conj(λz) = λz̄ (λ réel) | moyenne | confirmé | A p. 5 (propriétés 2 et 12 « ∀λ ∈ ℝ ») ; A-rés. p. 2 (b, n) ; utilisé p. 6 (« Car ū̄ = u ») |
| (a + ib)² = a² − b² + 2abi | basse | pas chez les autres | Atmani développe au cas par cas (A p. 2-3) |
| \|z\| = 0 ⇔ z = 0 ; inégalité triangulaire | basse | à revoir | \|z\| = 0 ⇔ z = 0 confirmé (A p. 8 prop. 4 ; A-rés. p. 2). \|z + z′\| ≤ \|z\| + \|z′\| est chez Atmani (A p. 9 prop. 8) MAIS notre fiche `operations_formes` la classe hors cadre (hors_cadre.mots, decisions « pas d'inégalité triangulaire ») : ne pas l'ajouter (le premier audit proposait « une ligne ») ; garder seulement \|z\| = 0 ⇔ z = 0 |
| Affixe de ku⃗ et de u⃗ + v⃗ | basse | confirmé | A p. 3 (aff(αu⃗) = α·aff(u⃗), aff(u⃗ + v⃗)) ; A-rés. p. 1 |
| Notation iℝ, ℝ*₊, ℝ*₋ | basse | confirmé | A p. 1 (iℝ = {iy / y ∈ ℝ}), p. 5 (z ∈ iℝ ⇔ z + z̄ = 0), p. 11 (z ∈ ℝ*₋ ⇔ arg z ≡ π [2π]) |
| Domaine de n (ℕ*, ℤ) | basse | confirmé | A p. 2 (« ∀n ∈ ℕ* »), p. 6 (conj(zⁿ), n ∈ ℤ), p. 8 (\|zⁿ\| « si z ≠ 0 et ∀n ∈ ℤ ») |
| Exemple j = −1/2 + i√3/2 | basse | confirmé (variante) | A p. 6 Ex. 2 : j² = j̄ et S = j²ⁿ − jⁿ ∈ iℝ |
| Placer un point connaissant module et argument | basse | pas chez les autres | Atmani fait l'inverse : placer, puis lire l'argument (A p. 10-11) |
| Oral seulement : « plan complexe » | — | confirmé | A p. 3 (« Le plan (P) s'appelle un plan complexe ») |
| Oral seulement : z = 0 ⇔ Re = Im = 0 | — | confirmé | A p. 1 (Remarque 1 : x + iy = 0 ⇔ x = 0 et y = 0) |
| Oral seulement : \|−z\| = \|z\| | — | confirmé | A p. 8 prop. 1 ; A-rés. p. 2 |
| Oral seulement : perpendiculaires par le quotient | — | confirmé | A p. 17 |

### B. Nouvelles pistes

Toutes vérifiées absentes de notre JSON (recherches entre parenthèses) et absentes du premier audit.

| Priorité | Catégorie | Ce que dit le professeur (prof, page) | Chez nous | Où l'ajouter |
|---|---|---|---|---|
| haute | méthode / exemple | Nature d'une figure avec les SEULES distances (faisable en partie 1, 2.4.4/2.4.7) : « il suffit de montrer que AC = AB = BC » ⇒ triangle équilatéral (A p. 9 Ex. 1, z_A = 2, z_B = 1 + i√3, z_C = 3 + i√3) ; c = a + b ⇒ OBCA parallélogramme, puis OA = OB ⇒ « OBCA est un losange » (A p. 15-16) | Absent : nc_i2 fait seulement ΩA = ΩB ; « isocèle », « équilatéral », « losange » : 0 occurrence. Le premier audit renvoie la nature d'un triangle à la partie 2 (méthode du quotient) | nc_i2 (2e exemple ou exercice : AB = AC ⇒ isocèle ; trois distances ⇒ équilatéral) |
| moyenne | formule | Cube par identité remarquable : (1 + i√3)³ = 1 + 3√3 i − 9 − 3√3 i = −8 (A p. 2, Application z₂) ; la fiche NC2 demande « carré et cube » | Absent : pas de (a + b)³ (0 occurrence) ; les cubes passent seulement par Moivre (nc_r8) | nc_c2 (et la formule dans nc_z5_identites) |
| moyenne | méthode | Montrer qu'un nombre est réel sans le calculer : on montre S̄ = S ; imaginaire pur : S + S̄ = 0 (A p. 6 Ex. 1 S = (1 + i)⁵ + (1 − i)⁵ ; Ex. 2 ; A p. 7-8 Ex. 6) | Le critère z̄ = z est en nc_j3 mais jamais appliqué à une expression (« S̄ » : 0) | Exercice de fin de nc_j3_b |
| moyenne | exemple type | Conjugué d'une expression en fonction de z̄ : conj(2z + 5i) = 2z̄ − 5i ; conj((z − 1)/(−3z + i)) = (z̄ − 1)/(−3z̄ − i) (A p. 6-7 Ex. 2) | Seulement conj(iz) = −i z̄ dans un vrai/faux de nc_j2 | nc_j2 (exercice), avec le manque « z̿, conj(kz) » |
| moyenne | propriété | \|z\| = 1 ⇔ z·z̄ = 1, donc z̄ = 1/z (A p. 8 prop. 3 ; A p. 18 Ex. 21 ; A-rés. p. 2 D 3) | Absent (« \|z\| = 1 », « = 1/z » : 0) | nc_r3 (inverse : si \|z\| = 1, 1/z = z̄) ou cahier de nc_m2 |
| moyenne | propriété | zz′ = 0 ⇔ z = 0 ou z′ = 0 (A p. 2 règle 1 ; A-rés. p. 1 a) — outil des équations factorisées (2.4.9) | Absent (0) | nc_c1 (cahier), ou partie 2 avant les équations |
| moyenne | propriété | (OM⃗, OM′⃗) ≡ arg(z′/z) [2π] (A p. 14, propriété 1 p. 15 ; A-rés. p. 2 F 1) — non listé par le premier audit dans H1 | Absent | Même diapo que H1 (partie 2 ou nc_i3) |
| basse | remarque / piège | « L'ensemble des nombres complexes n'est pas ordonné » : on ne compare pas deux complexes (A p. 1 §1.3 ; A-rés. p. 1) | Absent (« ordonné » : 0, hors « ordonnée ») | nc_a4 (une puce : « z > 0 n'a de sens que si z est réel ») |
| basse | méthode | sin θ + i cos θ = cos(π/2 − θ) + i sin(π/2 − θ) (A p. 12, Exemple 1) | nc_t4/nc_t4_b traitent −cos, π ± θ, pas π/2 − θ (0) | nc_t4_b |
| basse | méthode | Forme trigo avec paramètre : 1 − cos θ − i sin θ = 2 sin(θ/2)(…), signe de 2 sin(θ/2) selon θ (A p. 12-13) | Absent | Facultatif (exercice d'approfondissement, nc_t4_b) |
| basse | exemple | Ensembles simples Re(z) = 2, Im(z) = 3, Re(z) = Im(z) : des droites, avec figure (A p. 3 Exemple 1) | Absent | nc_a4 (après les axes) ou ouverture de nc_m5 (ensembles) |
| basse | exemple | Angle non remarquable : calculer cos α, sin α puis tan α de (AB⃗, AC⃗) à partir du quotient (A p. 16 Ex. 16) | Absent | Partie 2 (après H1) |
| basse | formule | Règles des puissances : z⁰ = 1, z⁻ⁿ = 1/zⁿ, zⁿ⁺ᵐ, (zⁿ)ᵐ (A p. 2) | Seulement i⁰ = 1 (nc_a6) ; « z⁻ » : 0 | nc_a6 (une ligne) |
| basse | formule | 1 + z + … + zⁿ = (1 − zⁿ⁺¹)/(1 − z) si z ≠ 1 (A p. 2 ; A-rés. p. 1 g) | Absent | Facultatif (lien avec les suites géométriques) |

Écartés (hors cadre ou fiche) : barycentre (A p. 3-4), points cocycliques (A p. 17), formule du binôme avec Cₙᵏ (A-rés. p. 1 h), factorisation zⁿ − z₁ⁿ (A p. 2), inégalité triangulaire (A p. 9), Ex. « u ∉ ℝ, \|1 + uz\| = \|1 + ūz\| » (A p. 6, niveau SM), Ex. 21 avec [π/2] (A p. 18-19), bijection ℂ → (P) (A p. 3).

### C. Désaccords entre professeurs

| Point | Prof Fayssal | Pr Atmani | Ce que nous gardons |
|---|---|---|---|
| Notation [r, θ] | l'utilise (p. 96-98) | l'utilise beaucoup (A p. 13 « Règles de calculs » ; A-rés. p. 2) | Notre fiche dit « jamais [r ; θ] » ; le premier audit proposait de la citer à l'oral. Les deux profs l'emploient : la citer UNE fois à l'oral (« tu la verras en classe »), ne jamais l'écrire dans la copie (forme complète au barème). Décision à trancher dans la fiche. |
| Alignement par l'argument | quotient réel | « alignés ⇔ arg((c − a)/(b − a)) ≡ 0 [2π] » (A p. 17 corollaire ; A-rés. p. 2 F 5) : incomplet (oublie ≡ π, C de l'autre côté de A) ; sa propre preuve donne kπ | Garder « (c − a)/(b − a) ∈ ℝ » (nc_i1). Ne jamais écrire la version d'Atmani. |
| Angles « modulo π » | parallèles ≡ 0 [π], perpendiculaires ≡ π/2 [π] (p. 99-100) | évite [π] dans le cours : « ≡ 0 [2π] ou ≡ π [2π] », « ≡ π/2 [2π] ou ≡ −π/2 [2π] » (A p. 17) ; mais [π] et [π/2] dans l'Ex. 21 (A p. 19) | L'écriture à deux cas modulo 2π d'Atmani (conforme à perimetre : « modulo π » hors programme), ou mieux « quotient réel / imaginaire pur ». |
| Repère | orthonormé direct (O, u⃗, v⃗) | « orthonormé » sans « direct », et change de nom : (O; u⃗; v⃗), (O; e⃗₁; e⃗₂) p. 14, (O; i⃗; j⃗) p. 15 | Le nôtre (orthonormé direct (O, u⃗, v⃗)), celui des sujets nationaux ; ajouter les flèches. |
| Imaginaire pur | z̄ = −z | z ∈ iℝ ⇔ z + z̄ = 0 (A p. 5) | Équivalents ; garder z̄ = −z, citer z + z̄ = 0 comme variante. |
| Domaine de n | Moivre n ∈ ℤ ; \|zⁿ\| n ∈ ℕ* | \|zⁿ\| et conj(zⁿ) n ∈ ℤ (z ≠ 0) ; Moivre « ∀n ∈ ℕ » (A-rés. p. 3) | Écrire « n ∈ ℕ » (suffit au bac) ; ℤ seulement avec « z ≠ 0 ». |
| Poser z = x + iy | « (x, y) ∈ ℝ² » | « z ∈ ℂ donc ∃x ∈ ℝ et ∃y ∈ ℝ / z = x + yi » (A p. 7, 9) | « On pose z = x + iy, avec x et y réels » (le plus simple), ℝ² en variante. |
| Notation de l'affixe | z_M | aff(M), aff(u⃗) et z_M (A p. 3) | z_M (celle des sujets). |
| Nom de l'axe vertical | axe des imaginaires purs | « axe des imaginaires » (A p. 3, déf.) et « axe des imaginaires purs » (A p. 3, remarques) | « axe imaginaire » (nous) ; citer « axe des imaginaires purs » une fois. |
| Ordre | alignement juste après les affixes (p. 89) | alignement juste après les affixes (A p. 4), avant le conjugué | Nous le mettons à la fin (IX). Ordre sans gêne ; les deux profs s'accordent, mais pas besoin de déplacer. |

---

