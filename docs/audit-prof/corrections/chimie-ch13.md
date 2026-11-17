## Transformations liées aux réactions acido-basiques

Fichier modifié : `backend/data/courses/en_attente/phys_ch13_acides_bases.json`. J'ai repris la copie en attente du matin, sans rien perdre : tout ce qui manque entre les deux versions, ce sont les 14 pistes `audio` des diapos dont la voix a changé. Le cours en ligne n'est pas touché. Le cours passe de 52 à 55 diapos et de 14 à 15 blocs. Scripts : `scratchpad/c13/py/` (apply.py, apply2.py, demos_ch13.py) ; journal : `scratchpad/c13/py/log.json`.

### Manques corrigés

| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| H. États physiques absents de réactions écrites | (aq)/(l) ajoutés dans les réactions écrites : a1 e0s0 « AH(aq) + H₂O(l) ⇌ A⁻(aq) + H₃O⁺(aq) », n1 e0.0.2 et e0.2.2 « C₂H₅COOH(aq) + HO⁻(aq) → C₂H₅COO⁻(aq) + H₂O(l) », a4 e1s1 « NH₃(aq) ». Le cahier du bloc s2_b1 portait « NH₃ + H₂O(l) » : NH₃(aq) ajouté. Dans 28 champs `ecrit`, les formules ASCII ont été passées en notation du bac (H3O+ → H₃O⁺, 10^-14 → 10⁻¹⁴, etc.) | ab_a1_ka, ab_n1_2016n, ab_a4_ammonium, réactions de 10 diapos |
| H. ab_w5_soude : « Na⁺ + HO⁻ » sans équation | Écrit à l'écran : NaOH(s) → Na⁺(aq) + HO⁻(aq), dissolution totale, donc [HO⁻] = C (« car une mole de NaOH donne une mole de HO⁻ »). Ajouté aussi au cahier, au bloc, au centre et à la voix | ab_w5_soude |
| H. Ke n'est pas présenté comme « constante d'équilibre de l'autoprotolyse » (exigé par le cadre) | Puce, cahier, bloc, entrée centre, voix (avec relecture « Je relis ») ; notation Ke = [H₃O⁺]_éq·[HO⁻]_éq. Question « À toi » du nouveau bloc : « Ke est la constante d'équilibre de quelle réaction ? », avec ses réactions juste / faux 1 / faux 2 | ab_w2_ke |
| H. Ke ne dépend que de T ; Ke = 10^(−pKe) | Puce, cahier, centre, voix. Exercice du bloc : pKe à 60 °C (Ke = 9,6·10⁻¹⁴, donc pKe = 13,0), avec sa démonstration | ab_w2_ke, bloc ab_s1_b2 |
| H. Solution neutre à pH = pKe/2, avec sa démonstration | Nouvelle diapo : [H₃O⁺] = [HO⁻] ⇒ Ke = [H₃O⁺]² ⇒ pKe = 2·pH ⇒ pH = pKe/2 ; 7,0 à 25 °C, 7,5 à 0 °C ; inégalités pour une solution acide ou basique. 8 entrées centre, une par ligne. Elle réutilise la vue `eau.html?vue=solutions` | ab_w3b_neutre (nouvelle) |
| M. Indicateur : équation et règle pKa ± 1 démontrée | Équation HInd(aq) + H₂O(l) ⇌ Ind⁻(aq) + H₃O⁺(aq) (écran, cahier, centre, voix). Nouvelle diapo : teinte acide si [HInd] ≥ 10·[Ind⁻] ⇒ pH ≤ pKa − 1 ; teinte basique ⇒ pH ≥ pKa + 1 ; zone de virage ≈ [pKa − 1 ; pKa + 1] ; exemple du BBT. 7 entrées centre. Vue `indicateurs.html` | ab_i1_indicateur, ab_i2b_regle (nouvelle) |
| M. Tableau d'avancement de l'autoprotolyse et τ | Nouvelle diapo : V = 1,0 L ; m = ρ·V ; n₀ = m/M = 55,6 mol ; x_max = n₀/2 = 27,8 mol ; x_éq = 1,0·10⁻⁷ mol ; τ = 3,6·10⁻⁹ ≪ 1. 8 entrées centre. Vue `eau.html?vue=autoprotolyse` | ab_w1b_limitee (nouvelle) |
| B. Conductivité de l'eau pure | Écrit et dit sur la nouvelle diapo (σ ≈ 5,5 µS/m : l'eau pure contient des ions) | ab_w1b_limitee |
| B. Ke = 10^(−pKe) | Fait (voir plus haut) | ab_w2_ke, fiche bilan |
| B. « titrage », « pH-métrique » (cadre) | Puces, cahier, bloc, une phrase dans la voix | ab_d1_montage, fiche bilan |
| Seulement à l'oral : [H₃O⁺] = [HO⁻] « car chaque réaction forme un H₃O⁺ et un HO⁻ » | Écrit à l'écran et au cahier | ab_w1_autoprotolyse, bloc s1_b2 |
| Seulement à l'oral : rapide, totale, unique ; τ ≈ 1 absent du cahier | Le sens de chaque mot est écrit (« unique, dite aussi sélective »). La méthode τ ≈ 1 est écrite à l'écran, au cahier et au centre (5 lignes). Le calcul chiffré complet est devenu l'exercice du bloc (8 lignes) | ab_d2_reaction, bloc s3_b2 |
| Seulement à l'oral : tableau de l'acide dans l'eau | Tableau, concentrations et K = (C·τ)²/(C·(1 − τ)) écrits | ab_r2_constante, bloc s1_b1 |
| Seulement à l'oral : tableau de dosage | Tableau état initial / état final, C_A·V_A − x_E = 0 et C_B·V_BE − x_E = 0 (écran, cahier, 6 entrées centre, voix) | ab_d3_equivalence, bloc s3_b3 |
| Seulement à l'oral : zone de virage (« formes à égalité », liste des 4 zones) | Écrits | ab_i2_virage |
| Seulement à l'oral : « la méthode doit se voir sur le dessin » | Puce et cahier | ab_d5_tangentes |
| Notations : [HO⁻] = 10^(pH − pKe), K_A, α(AH)/α(A⁻), « sélective » | Écrites | ab_w4_ho, ab_a1_ka, ab_p3_distribution, ab_d2_reaction, fiche bilan |
| Fiche : C_m = C·M jamais enseignée (piège du skill chimie) | C_m = m/V = n·M/V = C·M, avec l'exemple de l'ammoniac (0,17 g/L) : écran, centre, voix | ab_e4_base |
| Outil : propriétés du log, utilisées par les preuves | log(a·b), log(a/b), log(a²), log 1 (écran, cahier, centre, voix) | ab_z1_puissance |

Organisation : le bloc s1_b2 (w1, w1b, w2) a une nouvelle question « À toi » sur w2 et un nouvel exercice (pKe à 60 °C). Le nouveau bloc **ab_s1_b2b** (w3, w3b, w4) garde l'ancien exercice ([HO⁻] au national 2020 R) et reçoit un nouveau « retrouver » (pH = pKe/2). Le bloc s3_b2 passe à 5 diapos (ajout de i2b) et son exercice devient le calcul de τ du dosage ; l'exercice sur l'indicateur reste en réserve sur i2. Compétences : C1 reçoit w1b et w3b, C6 reçoit i2b.

### Non corrigés et pourquoi

- **États physiques dans les simulations** (eau, base, dosage, exploiter, acidite, comparer .html) : la consigne interdit de toucher autre chose que le cours en attente. C'est à faire dans une passe sur les simulations.
- **États dans les `attendu`** (C1 r1, C7 r0, `seances[2].blocs[2].retrouver`) : la règle du skill cours-concentration dit « never … in `alt` or `attendu` ». À trancher si on veut que la correction écrite du « retrouver » les montre.
- **Manques chez un seul professeur** (hors cadre exigé) : relation générale C_A·V_A/a = C_B·V_BE/b (N), « maximum ou minimum » de la dérivée, titrage colorimétrique détaillé, pipette et étalonnage, lecture à V_B = 0, mot « ampholyte » sur a5.
- **K = Ka/Ke (ab_k3_totale, écran)** : laissé tel quel. L'écran le tire de K = Ka₁/Ka₂ avec Ka₂ = Ke, ce qui est une ligne d'origine. Les démonstrations de k3 et k4 écrivent le produit des deux fractions.
- **Pas de nouvelle simulation** : les 3 nouvelles diapos réutilisent des vues existantes. Elles n'animent pas le calcul : il s'écrit au centre.

### Démonstrations

29 démonstrations relues et réécrites, dont 2 nouvelles (exercices des blocs s1_b2 et s3_b2). Les 13 autres sont restées telles quelles car déjà complètes (w4, w5, b2, b3, c3, p1, n2 f1, n3 q, n4…). Toutes font 8 lignes ou moins, chaque calcul est vérifié en Python. Sur les diapos, 17 preuves ont maintenant une entrée centre par ligne : r2, z1, w1b, w2, w3b, a3, a4, a5, c1, k1, p1, i2b, d2, d3, e2, e4, e5b.

Trois exemples :
- ab_a4_ammonium f0 : avant, « Ka·Qr,éq = [H₃O⁺]·[HO⁻] » arrivait sans calcul. Après : Qr,éq, puis Ka, puis le produit écrit en entier, puis la simplification, d'où Ka = Ke/Qr,éq, l'application numérique et pKa = 10,7 (8 lignes).
- ab_d3_equivalence f0 (et les 8 démonstrations du même type) : avant, « n(acide) = n(base) versée, donc C_A·V_A = C_B·V_BE ». Après : l'équation de dosage avec ses états, puis C_A·V_A − x_E = 0 et C_B·V_BE − x_E = 0, puis n(acide)initial = C_A·V_A = C_B·V_BE, puis le rapport des volumes « sans unité », la substitution et le résultat.
- ab_k2_puissance f0 (et k2 f1, k3, k4 q et f0, n1) : avant, « on multiplie par [H₃O⁺] : K = Ka₁/Ka₂ ». Après : la ligne du produit des deux fractions, puis « le premier facteur est Ka₁, le second 1/Ka₂ », puis 10^(pKa₂ − pKa₁) et le calcul.

Autres reprises : a3 (q, e0) part du tableau ([A⁻] = [H₃O⁺] = x_éq/V = 10^(−pH), [AH] = C − 10^(−pH)) ; a3 f0 a son « car » ; p4 e0 écrit la définition du pourcentage et la conservation de la matière ; e2 f0 donne la preuve littérale n(AH)restant = C_A·V_A/2 ; r1 f0 dit d'où vient 10^(−pH).

### Voix à enregistrer (id)

- **Diapos (speech_text.mixed, `audio` retiré)** : ab_z1_puissance, ab_w1b_limitee*, ab_w2_ke, ab_w3b_neutre*, ab_w5_soude, ab_a3_mesure, ab_a5_eau, ab_c1_acides, ab_p1_relation, ab_i1_indicateur, ab_i2b_regle*, ab_d1_montage, ab_d2_reaction, ab_d3_equivalence, ab_e2_demi, ab_e4_base, ab_e5b_pourquoi (17, * = nouvelles). Le `fr` est mis à jour pour chacune.
- **Réactions préparées** : ab_w2_ke q (0.1, 0.2, 1.juste, 2.1, 2.2).
- **Énoncés dits** : ab_w2_ke q, ab_s1_b2 exercice, ab_s3_b2 exercice, ab_s1_b2b retrouver.
- **Démonstrations (parole)** : les 29 de la liste ci-dessus. Aucune n'avait de piste.

### Vérifications faites (résultats)

- JSON valide, fins de ligne LF, `ensure_ascii=False`, `indent=2`. Le fichier a été relu juste avant l'écriture : identique à la copie du matin.
- `verif_attente.py` : 55 diapos, **0 mot absent, 0 hors bloc**, 0 doublon, 0 compétence inconnue, 17 diapos sans voix (celles listées ci-dessus).
- Script : chaque `mot` de demonstration.lignes est dans sa parole, dans l'ordre. Chaque pointage et chaque centre est dans speech_text.mixed. Chaque diapo est dans un seul bloc, et chaque bloc a au plus un tableau « À toi ». Aucun chiffre ni symbole dans les voix et paroles nouvelles.
- Différence avec la copie du matin : rien de supprimé, sauf les 14 `audio` des voix changées.
- Calculs vérifiés en Python : 55,6 / 27,8 mol, τ = 3,6·10⁻⁹ ; pKe(60 °C) = 13,0 ; Ka = 1,57·10⁻⁵ (pKa 4,8) et 1,62·10⁻⁵ (4,79) ; 2,0·10⁻¹¹ (10,7) ; 6,06·10⁻¹⁰ (9,2) ; τ = 0,039 et 0,126 ; K = 11, 8,9·10⁻², 2,5·10⁴, 9,1·10⁻², 7,9·10⁵, 1,26·10⁹, 8,13·10⁹ ; [HO⁻] = 6,3·10⁻¹⁰ mol/L, n restant = 1,9·10⁻¹¹ mol, τ ≈ 1 ; C_m = 0,17 g/L ; 4,9 pour 1,28·10⁻⁵.
- Aucun mot hors cadre ajouté (liste `hors_cadre` de acides_bases).
