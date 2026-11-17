## Nombres complexes (partie 1)

Copie en attente : `backend/data/courses/en_attente/math_ch6_nombres_complexes.json` (partie du cours en ligne, pas de copie en attente avant). Script : `scratchpad/corr/ch6/apply.py`. 58 → 64 diapos, 7 → 8 séances.

### Manques corrigés

| Constat | Ce qui a été fait | Diapo(s) |
|---|---|---|
| H1 Mesure d'angle (u⃗, AB⃗), (AB⃗, AC⃗), (AB⃗, CD⃗) (haute) | Nouvelle diapo : (u⃗, AB⃗) ≡ arg(b − a), (AB⃗, AC⃗) ≡ arg((c − a)/(b − a)) [2π] avec « car » (Chasles + arg(z/z′)), cas (AB⃗, CD⃗) au cahier, exemple a = 1 + i, b = 3 + 2i, c = 3i | nc_i3 (nouvelle) |
| H3 Orthogonalité / parallélisme par le quotient (haute) + oral « imaginaire pur ⇒ perpendiculaires » | Quotient réel ⇒ alignés / (AB) // (CD) ; imaginaire pur ⇒ perpendiculaires (écrit avec ≡ ±π/2 [2π], jamais « modulo π ») | nc_i3 |
| H2 Nature d'un triangle par le quotient (haute) | Nouvelle diapo : \|i\| = 1 ⇒ AC = AB, arg i ≡ π/2 ⇒ rectangle ⇒ « isocèle et rectangle en A » ; question du bloc (quotient 2i ⇒ rectangle, pas isocèle) avec démonstration et 5 réactions | nc_i4 (nouvelle) |
| Piste haute : nature par les seules distances (équilatéral, losange) | Exemple Atmani a = 2, b = 1 + i√3, c = 3 + i√3 : AB = AC = BC = 2 ⇒ équilatéral ; ligne « parallélogramme + AB = AD ⇒ losange » au cahier | nc_i4 |
| H4 Ensembles de points : cercle, médiatrice, transformer d'abord, phrase type (haute) | Nouvelle diapo : \|z − z_A\| = r ⇒ cercle, \|z − z_A\| = \|z − z_B\| ⇒ médiatrice, \|2z − 4i\| = 6 ⇔ \|z − 2i\| = 3, phrase « l'ensemble des points M est le cercle de centre A(2i) et de rayon 3 », figure du cahier, exercice de bloc + réactions | nc_m5 (nouvelle) |
| H5 Flèches de vecteurs (haute) | AB⃗, z_{AB⃗}, (O, u⃗, v⃗), (u⃗, OM⃗), AC⃗ = k·AB⃗ à l'écran, au cahier, dans les centres, rappels « retrouver », énoncés, explications et 42 champs écrits des réactions | nc_z2_vecteur, nc_p1, nc_p3, nc_m4, nc_g1, nc_i1, nc_n1, nc_b1_bilan, blocs |
| Conditions z ≠ 0 (moyenne) | c + id ≠ 0 (nc_c4, bilan), z′ ≠ 0 (nc_j2, nc_m3_b), z ≠ 0 (nc_r3), z et z′ non nuls (nc_r3_b) | nc_c4, nc_j2, nc_m3_b, nc_r3, nc_r3_b, nc_b1_bilan |
| Résoudre dans ℂ une équation avec z̄, conclure S = {…} (moyenne) | Nouvelle diapo : z + 2z̄ = 9 + i, on pose z = x + iy, S = {3 − i}, vérification | nc_j5 (nouvelle) |
| Ensemble des M tels que Z soit réel / imaginaire pur, « privé du point » (moyenne) | Nouvelle diapo : Z = (1 + i)z − 2i = (x − y) + i(x + y − 2) ; Z réel ⇔ droite y = −x + 2 ; question du bloc (imaginaire pur ⇒ droite y = x) + 5 réactions ; remarque « privé du point » | nc_m6 (nouvelle) |
| Parallélogramme AB⃗ = DC⃗ ⇔ z_B − z_A = z_C − z_D (moyenne) | Nouvelle diapo sur la figure existante OMBM′ ; seconde explication : même milieu des diagonales ; figure du cahier | nc_p5 (nouvelle) |
| « une mesure, en radians » (moyenne, partie confirmée) | Écran et cahier ; + sens positif écrit au cahier (était à l'écran seulement) | nc_g1 |
| Double conjugué, conj(kz) (moyenne) | z̿ = z et k̅z̅ = k·z̄ (k réel) au cahier ; la barre remplace « conj( ) » (z̅+̅z̅′̅, z̅z̅′̅, z̅ⁿ̅) | nc_j2 |
| \|z\| = 0 ⇔ z = 0 (basse) | Cahier | nc_m2 |
| Affixe de k·u⃗ et u⃗ + v⃗ (basse) | Cahier | nc_p3 |
| Notations iℝ, ℝ*₊, ℝ*₋ (basse) | z ∈ iℝ (nc_a4, nc_j3_b), z ∈ ℝ*₊ / ℝ*₋ (nc_g3) | nc_a4, nc_j3_b, nc_g3 |
| Domaine de n (basse) | n ∈ ℕ pour z̅ⁿ̅, \|zⁿ\|, Moivre | nc_j2, nc_m3_b, nc_r6 |
| Oral seulement : « plan complexe », « axe des imaginaires purs » | Écran et cahier | nc_p1 |
| Oral seulement : z = 0 ⇔ Re = Im = 0 | Cahier (« a + ib = 0 ⇔ a = 0 et b = 0 ») | nc_a5 |
| Oral seulement : \|−z\| = \|z\| | Cahier (\|z̄\| = \|−z\| = \|z\|) | nc_m3_b |
| Écran seulement → cahier | diagonale z + z′ (nc_p3), cercle de centre O (nc_m2), zⁿ réel / imaginaire pur (nc_r7), sens positif (nc_g1) | idem |

Aussi : étape manquante de l'exemple du quotient au cahier (nc_c4), « car » à l'alignement (nc_i1), bilan (puces 2, 3, 4, 8) complété. Blocs : nc_s2_b1 coupé (p1–p3 / p4–p5), j5 ajouté au bloc du module, nouveaux blocs nc_s2_b1b, nc_s2_b3c, nc_s4_b2b (cahier, figure, retrouver, exercice repris d'une réserve), nouvelle séance nc_s3b, titres de séances renumérotés. Compétences : K3 + nc_p5, K4 + nc_j5, K8 + nc_m5, nc_m6, nc_i3, nc_i4 (libellés mis à jour).

### Non corrigés et pourquoi

- Égalité sous forme trigonométrique, « arg z + 2kπ, k ∈ ℤ », (a + ib)², placer un point par module et argument : propres au Prof Fayssal (non exigés par le cadre).
- Inégalité triangulaire : hors de notre fiche `operations_formes` (hors_cadre). Gardé seulement |z| = 0 ⇔ z = 0.
- Exemple j = −1/2 + i√3/2 (basse) : c'est un exercice avec démonstration et 5 réactions, pas un simple ajout écrit.
- Nouvelles pistes moyennes et basses : hors consigne.
- Notation [r, θ] : désaccord entre profs, à trancher dans la fiche.
- **À décider** : la fiche `operations_formes` (cadre_reference_2bac_pc.json) renvoie angles, orthogonalité, nature d'un triangle et ensembles de points à la partie 2 (« seulement annoncés »). Ils sont au cadre officiel (2.4.4, 2.4.7) et la partie 2 n'existe pas : ils sont maintenant enseignés ici. Il faut ajouter à la fiche les capacités et formules correspondantes (sinon `controler_cadre.py` peut signaler ces formules) — fichier hors en_attente, non modifié.
- Simulations non modifiées (frontend) : la fiche `bilan.html` ne montre pas les ajouts du bilan ; les 6 nouvelles diapos réutilisent une vue existante en rappel (nc_p5 vecteur/somme, nc_j5 calculs a5 « regle », nc_m5 module/cercle, nc_m6 plan/purs, nc_i3 alignement/alignes, nc_i4 vecteur/distance) : pour nc_j5, nc_m6 et nc_i4 la vue montre le rappel, pas l'exemple de la diapo (une vue dédiée serait mieux).
- Voix des diapos existantes inchangées (l'écran ajoute, ne contredit pas). Réactions de réserve existantes avec des chiffres dans la parole (≈ 23, sans audio) : préexistant, non traité.

### Démonstrations

- 69 relues (toutes celles du cours), 34 réécrites (27 + 7 copies de blocs), 6 nouvelles (4 + 2 copies de blocs). Audio retiré des réécrites.
- nc_c4 q : 4 lignes « … /(1 + 1) » → 7 lignes : méthode (conjugué), dénominateur 1² + 1² = 2, développement, i² = −1, quotient, résultat −1 + 2i.
- nc_r6 q : « 2⁶(cos 6π/6…) = −64 » sans forme trigo → module 2, forme 2(cos π/6 + i sin π/6), Moivre, 2⁶ = 64 et 6 × π/6 = π, cos π = −1 et sin π = 0, −64.
- nc_i2 q (« sans calculer, pourquoi ») : calcul seul → b = ā (symétrique), ω réel (Ω sur l'axe), la symétrie conserve les distances, puis vérification |a − ω| = |b − ω| = 5/2.

### Voix à enregistrer

- Diapos nouvelles (speech_text.mixed) : nc_p5, nc_j5, nc_m5, nc_m6, nc_i3, nc_i4.
- Démonstrations réécrites : nc_a4/f0, nc_a5/f0, nc_a6/e0, nc_c1/f0, nc_c2/f0, nc_c3/f0, nc_c4/q, nc_c4/e0, nc_c4/f0, nc_j2/f0, nc_m1/f0, nc_m2/f0, nc_g2/f0, nc_t3/f0, nc_t4/e0, nc_t5/f0, nc_r2/q, nc_r5/f0, nc_r6/q, nc_r6/e0, nc_r7/f0, nc_r8/f0, nc_i1/f0, nc_i2/q, nc_n1/f0, nc_n2/f0, nc_s1_b0/exercice (+ copies de blocs s1_b3, s2_b2, s2_b3, s3_b1, s3_b3, s4_b2, s4_b3).
- Démonstrations nouvelles : nc_m6/q, nc_i4/q, nc_m5/f0, nc_i3/f0.
- Énoncés lus (enonce_dit) : nc_m6/q, nc_i4/q, nc_m5/f0, nc_i3/f0.
- Réactions nouvelles (20) : nc_m6 q (0.1, 0.2, 1.juste, 2.1, 2.2), nc_i4 q (0.1, 0.2, 1.juste, 2.1, 2.2), nc_m5 e0 (0.1, 0.2, 1.juste, 2.1, 2.2), nc_i3 e0 (0.1, 0.2, 1.1, 1.2, 2.juste).

### Vérifications faites

- `json.load` : OK. Écrit avec json.dumps(ensure_ascii=False, indent=2), LF.
- Script mots (ch2_verif.py) : 64 diapos, 75 démonstrations, 0 erreur (chaque `mot` de démonstration dans sa parole et dans l'ordre, chaque pointage/centre dans speech_text.mixed, pas de chiffre ni symbole dans les voix sans audio, chaque diapo dans exactement un bloc et dans l'ordre, chaque competence_id existe).
- `verifier_figures_cahier.py` : 0 erreur, 0 avertissement (3 nouvelles figures).
- Réactions des nouvelles questions : une par option (juste / 1 / 2) ; une seule « À toi » par bloc.
- Calculs vérifiés avec sympy (S = {3 − i}, a + c = b + d, (c − a)/(b − a) = i pour les deux exemples, AB = AC = BC = 2, Z = (x − y) + i(x + y − 2), −1 + 2i, 1/2 − i/2, −i/2, −64, 64, 27, (√6 + √2)/4).
- Non lancés (outils absents ici) : verifier_texte_corpus.py, controler_cadre.py, preparer_reponses.py verifier, lecture dans le navigateur.
