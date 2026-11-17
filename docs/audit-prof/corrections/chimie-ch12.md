## État d’équilibre d’un système chimique

Fichier modifié : `backend/data/courses/en_attente/phys_ch12_etat_equilibre.json`. J'ai repris la copie en attente du matin et je n'ai rien supprimé. Le cours en ligne n'est pas touché. Le cours passe de 40 à 41 diapos. Scripts : `scratchpad/corr/ch12/build.py` et `build2.py`, journal `ch12/log.json`.

### Manques corrigés

| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| H1 : G et σ = Σλᵢ[Xᵢ] absents (exigés par le cadre, EE5) | Nouvelle diapo « Rappel : le conductimètre, G et σ » : cellule, G = k·σ (k en m, σ en S·m⁻¹), σ = Σλᵢ·[Xᵢ] (λᵢ en S·m²·mol⁻¹, [Xᵢ] en mol·m⁻³). Elle a une voix, 4 entrées centre, un cahier, et figure dans le bloc et dans C5. Diapo m2 : « σ = Σλᵢ·[Xᵢ] avec les deux ions », la raison de [CH₃COO⁻] = [H₃O⁺] et les unités du résultat. Fiche bilan : G = k·σ et σ = Σλᵢ[Xᵢ] avec leurs unités | ee_m2a_conductance (nouvelle), ee_m2_conductimetrie, ee_bl_fiche, ee_s2_b2/b3 |
| H2 : tableau à 2 lignes ; x_max = C·V non justifié | Tableau à 3 lignes (initial / en cours x / équilibre x_éq). On écrit « eau en excès, CH₃COOH limitant : C·V − x_max = 0 », puis x_éq = n_éq(H₃O⁺) = [H₃O⁺]éq·V et x_f = x_éq. Écran, cahier et bloc ; voix réécrite ; 8 entrées centre. Rappel de x_max = C·V (eau en excès) dans k5, n2, n6 et la fiche | ee_r1_taux, ee_s1_b1, ee_k5_tau, ee_n2_base, ee_n6_taux |
| H3 : calcul par σ sans unités ni λ séparées | Calcul en 8 lignes centre : conversion de σ (mS·m⁻¹ → S·m⁻¹), λ(H₃O⁺) = 35,0·10⁻³ et λ(CH₃COO⁻) = 4,09·10⁻³ S·m²·mol⁻¹, puis la somme, [H₃O⁺] en mol·m⁻³, la conversion ÷ 10³, τ et K avec l'étape intermédiaire. 2019 N : λ₁ = 35·10⁻³, λ₂ = 3,23·10⁻³, C = 1,0 mol·m⁻³ sur sa ligne, τ = 8,6·10⁻³/(1,0 × 38,23·10⁻³) ≈ 0,22, puis K. Les voix sont réécrites | ee_m3_calcul, ee_m4_national, ee_s2_b3 |
| M : Qr en fonction de x | Tableau [CH₃COO⁻] = [H₃O⁺] = x/V, [CH₃COOH] = C − x/V, Qr = (x/V)²/(C − x/V), « Qr dépend de l'avancement x ». Exemple calculé ligne par ligne (9,9·10⁻³ puis 1,01·10⁻⁶) et [CH₃COOH] écrite pour chaque point ; voix et 4 entrées centre | ee_i3_au_cours, ee_s1_b3 |
| M : définition de Qr | « Grandeur qui caractérise un système chimique dans un état donné » + « concentrations molaires effectives » sur l'écran, au cahier et au bloc. La voix relit la définition en français | ee_q1_quotient, ee_s1_b2 |
| M : forme générale de K | K = [C]éq^c·[D]éq^d/([A]éq^a·[B]éq^b) sur l'écran, au cahier, au bloc et dans la fiche ; voix + entrée centre | ee_k3_constante, ee_bl_fiche |
| M : conversions µS·cm⁻¹ / mS·cm⁻¹ → S·m⁻¹ | Ligne écrite (1 µS·cm⁻¹ = 10⁻⁴ S·m⁻¹ car 1 cm = 10⁻² m ; 1 mS·cm⁻¹ = 10⁻¹ S·m⁻¹) + une phrase de voix | ee_m3_calcul, ee_s2_b3 |
| M : mesure faite à l'équilibre | « Réaction rapide : l'équilibre est atteint quand on mesure, le pH (ou σ) lu est celui de l'équilibre » : écran, cahier, bloc, voix | ee_e1_concentrations, ee_m2a_conductance, ee_s2_b1 |
| B : Qr d'une précipitation | Fe³⁺(aq) + 3HO⁻(aq) ⇌ Fe(OH)₃(s) : Qr = 1/([Fe³⁺]·[HO⁻]³), ajout écrit seulement | ee_q4_solides, ee_s1_b2 |
| B : K > 10⁴ ⇒ réaction pratiquement totale | Ligne écrite ; k4 : K' = 6,25·10⁴ > 10⁴ ; fiche | ee_k3_constante, ee_k4_inverse, ee_bl_fiche |
| Présent seulement à l'oral | Ligne « en cours » et x_max (r1) ; cellule du conductimètre (m2a) ; eau « en très large excès » (q3, bloc) ; mélange V = 100 mL, C = 1,0·10⁻² × 50/100 (k2) ; « palier = courbe horizontale = état d'équilibre » (n5) | ee_r1, ee_m2a, ee_q3, ee_k2, ee_n5 |
| États physiques | Estérification en (l) partout : écran, cahier, bloc, centre, exercice e0, démonstration et réaction 0.1. k2 : CH₃COO⁻(aq) + H₃O⁺(aq) | ee_n5_courbe, ee_s3_b3, ee_k2_produits |
| Notations | x_f = x_éq écrit (r1) ; mol·L⁻¹, S·m⁻¹, S·m²·mol⁻¹ écrits (m2a, m3, m4) ; chiffres significatifs d'une concentration tirée d'un pH (e1) ; « xf / xmax », « [H₃O⁺]f » → x_f/x_max, [H₃O⁺]_f (réaction m1) | ee_r1, ee_m2a, ee_m3, ee_m4, ee_e1, ee_m1 |
| Erreur de convention (réactions) | « Qr sans unité car les unités se simplifient » → « par convention, concentrations en mol/L, Qr sans unité » : 6 réactions réécrites (parole + écrit), sans leur audio | ee_i2_melange e1s2 (0.juste, 1.1, 1.2), ee_n3_melange e1s2 (idem) |

### Non corrigés et pourquoi

- Les 4 manques chez un seul professeur (C = m/(M·V), K = τ²/(1 − τ)², trois K de M2, H₂O₂ + I⁻ + H⁺) : aucun n'est exigé par le cadre.
- Les simulations ne sont pas modifiées (consigne). Le tableau de `rappel.html?vue=taux` montre encore 2 lignes : la 3ᵉ ligne (en cours) est écrite sur l'écran et au cahier. L'estérification de `figures.html?fig=fig_2017R` et les alt restent sans état (les champs alt sont exclus de la règle).
- ee_m2a_conductance réutilise `conductimetrie.html?vue=relation`, arrêté au moment `mesure` (cellule et afficheur 4,6 mS/m), avec `demarrer: reset`. Aucune vue ne dessine G = k·σ : ces formules passent par le centre.
- Blocs ee_s2_b3 (nouvelle diapo), ee_s1_b3 et ee_s3_b1 : 5 diapos, avec toujours un seul tableau « À toi » par bloc.
- La fiche (`bilan.html`) et sa voix ne changent pas. G, σ et la forme générale de K sont ajoutés aux puces et au cahier seulement.
- m4 : τ = 0,225 est arrondi à 0,22, comme dans le sujet. Avec 0,225 on trouverait K = 6,5·10⁻⁵ : à décider si on veut le signaler.
- Les autres réactions préparées (≈ 150) n'ont pas été réécrites en démonstrations complètes. Leurs équations écrites ont déjà leurs états (vérifié par script).

### Démonstrations

Toutes les démonstrations ont été relues : questions, exercices, blocs, rappels, preuves de diapo, cahiers et fiche. Il y a 12 démonstrations réécrites ou nouvelles :
- réécrites : r1 e0 + bloc ee_s1_b1, e3 question (audio retiré), k5 question, m1 e0, m4 e0 + bloc ee_s2_b3 ;
- nouvelles : bloc ee_r_b1, rappels C2_r2, C3_r1, C5_r3, C7_r1.

Neuf preuves de diapo sont passées à une entrée centre par ligne : r1 (8), m3 (8), m4 (7), k2 (8), n5 (7), i3 (4), e3 (+5), k5 (+3), n4 (+3).

Gardées telles quelles car déjà complètes : z1, q5 e0, i2 (question, e0, bloc), e1 e0 + bloc, k2 e0 + bloc, n1 e0 + bloc, n2 e0, n3 (question et e0), n4 e0, n5 e0, f4 e0 + bloc, n6 e0 + bloc, m4 question.

Trois exemples avant → après :
- e3 question : 4 lignes, seul le numérateur était démontré → 7 lignes : définition, [H₃O⁺]éq = 10^(−pH) (définition du pH), [CH₃COO⁻]éq = [H₃O⁺]éq (même x_éq, même V), numérateur, dénominateur C − x_éq/V, relation, conclusion « car ».
- k2 (en partant des produits) : « [CH₃COO⁻]éq = [H₃O⁺]éq = 2,75·10⁻⁴ » sans raison → C après mélange, puis le sens 2, puis 10^(−3,56) = 2,75·10⁻⁴. Ensuite « mêmes quantités, consommées une à une », « acide formé = H₃O⁺ consommé », l'expression, 7,59·10⁻⁸/4,72·10⁻³ et 1,61·10⁻⁵.
- r1 e0 : « τ = x_f/x_max = [H₃O⁺]éq·V/(C·V) = 10^(−pH)/C » sur une seule ligne, sans x_max justifié → 7 lignes : définition, x_max = C·V (eau en excès, acide limitant), x_f = [H₃O⁺]éq·V, V se simplifie, 10^(−3,93) = 1,17·10⁻⁴ mol/L, substitution, τ = 0,117.

### Voix à enregistrer (id)

- Diapos sans audio (voix changée ou nouvelle) : ee_r1_taux, ee_q1_quotient, ee_i3_au_cours, ee_e1_concentrations, ee_k2_produits, ee_k3_constante, ee_m2a_conductance (nouvelle), ee_m3_calcul, ee_m4_national, ee_n4_pile, ee_n5_courbe.
- Démonstrations (parole nouvelle) : ee_r1_taux e0, bloc ee_s1_b1 exercice, ee_e3_expression question, ee_k5_tau question, ee_m1_methanoique e0, ee_m4_national e0, bloc ee_s2_b3 exercice, bloc ee_r_b1 exercice, rappels C2_r2, C3_r1, C5_r3, C7_r1.
- Réactions : ee_i2_melange e1s2 (0.juste, 1.1, 1.2), ee_n3_melange e1s2 (0.juste, 1.1, 1.2).

### Vérifications faites

- JSON valide, écrit avec `json.dumps(ensure_ascii=False, indent=2)`, en LF avec une fin de ligne. Le fichier a été relu juste avant chaque écriture (on compare le contenu).
- `verif_attente.py` : 41 diapos, 0 mot absent, 0 hors bloc, 0 doublon, 0 compétence inconnue. 11 diapos sans voix, celles de la liste.
- Script maison :
  - chaque `mot` de démonstration est dans sa parole, et dans l'ordre des lignes (0 hors ordre) ;
  - chaque `mot` de centre et de pointage est dans la voix ;
  - aucune voix ni parole nouvelle ne contient de chiffre, de symbole ou de tachkil ;
  - chaque bloc a un seul tableau « À toi » ;
  - par rapport à la copie du matin, aucun champ n'est perdu en dehors des audio, des centres et des puces remplacés.
- Scan des états : il ne reste que de faux positifs (flèches « → » entre valeurs, lettres générales aA + bB). `verifier_figures_cahier.py` : 3 figures, 0 erreur.
- Calculs refaits en Python :
  - 10^(−3,41) = 3,89·10⁻⁴ et τ = 0,039 ; 10^(−3,93) = 1,17·10⁻⁴ et τ = 0,117 ; 10^(−2,90) = 1,26·10⁻³ et τ = 0,126 ;
  - 1,58·10⁻⁶/8,74·10⁻³ = 1,81·10⁻⁴ ; 1,0·10⁻⁸/9,9·10⁻³ = 1,01·10⁻⁶ ; 1,51·10⁻⁷/9,61·10⁻³ = 1,57·10⁻⁵ ;
  - 10^(−7,12) = 7,59·10⁻⁸ et 7,59·10⁻⁸/4,72·10⁻³ = 1,61·10⁻⁵ ; 1,0·10⁻² × 1,51·10⁻³/0,961 = 1,57·10⁻⁵ ;
  - 35,0 + 4,09 = 39,09 ; 4,6/39,09 = 0,118 ; 1,0·10⁻³ × 1,39·10⁻²/0,882 = 1,58·10⁻⁵ ;
  - 35 + 3,23 = 38,23 ; 8,6/38,23 = 0,225 ; 1,0·10⁻³ × 0,0484/0,78 = 6,2·10⁻⁵ ;
  - 1/0,65 = 1,54 ; 0,16/0,04 = 4 ; 0,10 × 1,742·10⁻⁴/0,9868 = 1,77·10⁻⁵ ; 1,0·10⁻² × 0,040/0,80 = 5,0·10⁻⁴ ;
  - 1 µS·cm⁻¹ = 10⁻⁴ S·m⁻¹.
