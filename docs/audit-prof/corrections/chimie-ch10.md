## Suivi temporel d’une transformation chimique – vitesse de réaction

Fichier modifié : `backend/data/courses/en_attente/phys_ch10_cinetique.json`. Je suis parti de la copie en attente, qui contenait déjà les démonstrations reprises ce matin. Rien n’a été perdu : aucune diapo ni aucune clé n’a disparu, et les seules suppressions sont les `audio` des voix modifiées. Le cours en ligne n’a pas été touché. Le script de construction est `scratchpad/ch10/build.py`.

Le cours passe de 56 à 61 diapos, de 58 à 61 questions et exercices, et de 5 à 6 séances.

### Manques corrigés
| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| **Haute.** σ(x) donné sans démonstration ; dans l’exemple B, ni tableau, ni V, ni n₀ ; x_max sans calcul | **Nouvelle diapo** ci_g4b : données de B (V = 100 mL, [HO⁻]₀, λ), calcul n₀ = [HO⁻]₀·V avec la conversion sur sa ligne, tableau d’avancement (table), « ester en excès → HO⁻ limitant », x_max = n₀ = 1,0 mmol. La diapo ci_g5 est réécrite : σ = Σλ[X] → concentrations tirées du tableau → substitution → regroupement → σ₀ → σ = σ₀ − (λ(HO⁻) − λ(CH₃COO⁻))·x/V (« droite qui descend car λ(HO⁻) > λ(CH₃COO⁻) »). **Nouvelle diapo** ci_g5b : σ_f = 0,0501 + 0,0409 = 0,091 S/m calculé, puis le rapport (σ₀ − σ)/(σ₀ − σ_f) = x/x_max, d’où la relation de x. Chaque ligne a son entrée `centre` | ci_g4b_tableau (nouvelle), ci_g5_droite, ci_g5b_rapport (nouvelle) |
| **Haute.** Pas de vitesse calculée à partir de n(X)(t) ou [X](t) | **Nouvelle diapo** ci_v6b, placée juste après la courbe [H₂O₂](t) de ci_v6. On y établit n = n₀ − x, puis dx/dt = −dn/dt, puis v = −(1/V)·dn/dt = −d[R]/dt. Pour un produit : v = d[P]/dt. Exemple : la tangente à t = 0 donne −2,5 mmol·L⁻¹·min⁻¹, donc v(0) = 2,5 mmol·L⁻¹·min⁻¹, la même valeur que par x. Un exercice de réserve (v à 8 min = 0,92) est ajouté, avec sa démonstration et ses 5 réactions. Le libellé de C5 est étendu | ci_v6b_espece (nouvelle), C5 |
| **Haute.** Aucun couple Ox/Red, aucune demi-équation (⇌) | **Nouvelle diapo de rappel** ci_z4b, avant l’équation : couples H₂O₂/H₂O et I₂/I⁻, demi-équations, électrons égalisés, addition. Les couples I₂/I⁻ et S₄O₆²⁻/S₂O₃²⁻ sont ajoutés au titrage (centre, voix, cahier), et les couples Mg²⁺/Mg et H⁺/H₂ à l’exemple C (écrit) | ci_z4b_couples (nouvelle), ci_m3b_calcul, ci_p1_ballon |
| **Haute.** L’équivalence n’est pas définie par les proportions ; n(I₂) = C·V_E/2 est posé sans origine ; l’application numérique manque | ci_m3 : définition (« proportions stœchiométriques ») écrite et dite. ci_m3b : demi-équations → équation → n(I₂)/1 = n_E/2 → n_E = C·V_E → n(I₂) = C·V_E/2. **Nouvelle diapo** ci_m3c : conversion de V_E, substitution, 1,26·10⁻⁴ mol, ×10, 1,26 mmol = x. La démonstration de la réserve et du bloc est reprise de la même façon | ci_m3_titrage, ci_m3b_calcul, ci_m3c_calcul (nouvelle), bloc ci_s1_b2 |
| Moyenne : définition de v en mots et unité SI | Écrite (puces, cahier, centre) et dite : « quantité de matière formée par unité de temps et de volume » ; mol·m⁻³·s⁻¹ | ci_v2_definition |
| Moyenne : facteur concentration initiale | Ajouté à ci_v6, à l’écrit et à la voix : C₁ > C₂ ⇒ v₀,₁ > v₀,₂. Exemple : avec plus d’ions iodure, la tangente est plus raide et le palier ne change pas. Un dessin du cahier montre deux courbes avec leurs tangentes. Ajouté aussi au bilan et au cahier du bloc | ci_v6_epuisement, ci_bl_fiche, ci_s3_b2 |
| Moyenne : la trempe agit par refroidissement **et** dilution | Écrit et dit : ce sont deux facteurs cinétiques, température et concentration. Le mot « plongée » est cité | ci_m2_trempe, ci_n8_trempe, ci_bl_fiche, blocs ci_s1_b1 et ci_s4_b2 |
| Moyenne : démonstration de la pression | Voix et centre réécrits : l’air garde P₀ = P_atm (V et T constants), donc P = P₀ + P(H₂). Puis P(H₂)·V = n(H₂)·R·T (V : volume du gaz), n(H₂) = x, x_max, et enfin x = x_max·(P − P₀)/(P_max − P₀). L’application numérique n’est plus dans la voix, car c’est la réponse de la question de la diapo | ci_p2_relation |
| Moyenne : exercice σ croissante à partir de σ₀ ≈ 0 | Exercice de réserve ajouté : (CH₃)₃CCl(aq) + H₂O(l), avec x = x_max·σ/σ_f (σ_f est appelé aussi σ_max). Il a sa démonstration et ses 5 réactions | ci_g6_calcul (e2) |
| Moyenne : intervalle entre deux mesures ≪ t₁/₂ | Écrit et dit | ci_h4_comparer, bloc ci_s3_b3 |
| Moyenne : n = ρ·V/M | Écrit, dit, au centre, avec un exemple (36 mL d’eau → 2,0 mol) | ci_z1_mole, bloc ci_r_b1 |
| Basse : méthodes physiques et chimique ; phrase type de rédaction pour la conductimétrie | Écrit (puces et cahier) | ci_p5_choisir, bloc ci_s2_b3 |
| Basse : environ 7 à 10 t₁/₂ | Écrit comme un ordre de grandeur (exemple A : x(40 min) = 1,99 mmol) | ci_h3_pieges |
| Basse : montage du titrage et empois d’amidon | Écrit et dit : burette, agitateur, bleu → incolore | ci_m3_titrage |
| Basse : étalonnage du conductimètre | Écrit | ci_g1_cellule |
| Présent seulement à l’oral | Écrits : définition de l’avancement (a1b) ; hypothèses « Si … est le réactif limitant » (a2, avec 6 lignes au centre sur la voix existante) ; consigne « bloquer, pas seulement refroidir » (n8) ; burette (m3) ; raison de la droite (g5) | ci_a1b, ci_a2, ci_n8, ci_m3, ci_g5 |
| Notations | État final : « x_f = x_max quand un réactif est épuisé » (a1b) ; P₀ = P_atm et ΔP/ΔP_max (p1, p2) ; angle α de la tangente (v5) ; unité SI (v2) ; « plongée » (m2) | — |
| États physiques | Toutes les équations et demi-équations nouvelles portent (aq), (l), (s) ou (g). Une vérification par script sur tous les champs écrits ne trouve aucun oubli | — |

### Non corrigés et pourquoi
- **Manques chez un seul professeur :**
  - tableau d’avancement du dosage (M1) ;
  - vrai/faux « titrage non destructif » ;
  - asymptote (nous gardons « palier »).

  Seule la précision « V : volume occupé par le gaz » est écrite, parce qu’elle sert à la démonstration de la pression.
- **Exercice « vitesse à partir de n(X) » dans ci_n4_reactif :** il n’a pas été ajouté, car je n’ai pas de valeurs de tangente sûres pour le sujet 2023 N. Le savoir-faire est couvert par ci_v6b et son exercice de réserve.
- **Visuels :**
  - ci_z4b et ci_g4b sont **sans visuel** (`kind: none`). Aucune vue du chapitre ne montre les couples ni le tableau de B ; ci_g4b affiche le tableau d’avancement en `table`.
  - ci_m3c, ci_g5b et ci_v6b réutilisent des vues existantes : `suivi?vue=titrage`, `conductimetrie?vue=droite`, `vitesse?vue=concentration`.
  - La concentration initiale n’a pas de simulation : seulement un dessin au cahier.
- **Simulations bilan.html et carte.html :** elles ne sont pas modifiées. La fiche dessinée ne montre donc pas les ajouts, qui ne figurent que dans les puces et le cahier de ci_bl_fiche.
- **Réactions préparées absentes avant mon passage :**
  - les exercices de bloc qui recopient une réserve n’ont pas de `reponses` (10 blocs) ;
  - les réserves e0 de ci_v4, ci_n1 et ci_n7 non plus.

  Je ne les ai pas créées.
- **À décider :**
  - la séance 3 est **coupée en deux** (Conductimétrie : 2 blocs ; Pression et méthodes : 2 blocs). Il y a désormais 6 séances, pour éviter une séance de 4 blocs ;
  - le bloc ci_s3_b2 compte 5 diapos.
- **Voix non contrôlée contre le corpus :** `verifier_texte_corpus.py` est sur le poste Windows. À vérifier : « stœchiométriques », « l’empois d’amidon », « l’agitateur magnétique », « rho », « affine », « le système international ».

### Démonstrations (relues, réécrites)
- **Relues :** toutes, soit 41 démonstrations de questions et exercices, plus les exemples écrits sur les diapos.
- **Réécrites ou complétées (11) :**
  - ci_m3_titrage/f0 et le bloc ci_s1_b2 ;
  - ci_g6_calcul/f0 et le bloc ci_s2_b1b ;
  - ci_p2_relation/q et e0 ;
  - ci_n6_sigma/f0 et le bloc ci_s4_b2 ;
  - ci_r1_litres/f0.
- **Nouvelles (8) :**
  - ci_g6 q et e2, ci_v6b e0 ;
  - blocs ci_s2_b2, ci_r_b1, ci_r_b2 et ci_s1_b2b, qui n’avaient pas de démonstration.
- **Exemples écrits sur les diapos, une entrée `centre` par ligne :**
  - **voix réécrite (16) :** m2, m3, m3b, m3c, g4b, g5, g5b, g6, p2, p4, v2, v6, v6b, n2, n6, n7 ;
  - **voix inchangée, lignes posées sur les mots existants (9) :** a2, a6, v3, v4, v8, n3, n4, n5, r1.

Trois exemples avant → après :
1. ci_m3b : « n(I₂) = C·V_E/2 → 10 × C·V_E/2 = 1,26 mmol » → demi-équations, équation, n(I₂)/1 = n_E/2, n_E = C·V_E, n(I₂) = C·V_E/2 ; puis, sur ci_m3c, V_E = 12,6·10⁻³ L, 0,020 × 12,6·10⁻³/2 = 1,26·10⁻⁴ mol, ×10 = 1,26 mmol = x.
2. ci_n6 : « dσ/dt = −160·dx/dt → v₁ = 0,78 » → dx/dt = −(1/160)·dσ/dt, pente = (0,17 − 0,22)/4 = −0,0125, 160·V₀ = 1,6·10⁻², v₁ = −(1/(1,6·10⁻²)) × (−0,0125) = 0,78 mol·m⁻³·min⁻¹.
3. ci_p4 : « on calcule σ = 0,170 » → σ isolé = (1,57·10⁻³ − x)/(6,3·10⁻³), x = 5·10⁻⁴, substitution, 1,07·10⁻³/(6,3·10⁻³), 0,170 S·m⁻¹ = 170 mS·m⁻¹, t ≈ 17 min.

### Voix à enregistrer (id)
- **Diapos (19) :**
  - nouvelles : ci_z4b_couples, ci_m3c_calcul, ci_g4b_tableau, ci_g5b_rapport, ci_v6b_espece ;
  - modifiées : ci_z1_mole, ci_m2_trempe, ci_m3_titrage, ci_m3b_calcul, ci_g5_droite, ci_g6_calcul, ci_p2_relation, ci_p4_2016R, ci_v2_definition, ci_v6_epuisement, ci_h4_comparer, ci_n2_diminue, ci_n6_sigma, ci_n7_conductance.
- **`parole` de démonstration :**
  - ci_m3_titrage/f0, ci_g6_calcul/q, f0 et e2, ci_p2_relation/q et e0, ci_n6_sigma/f0, ci_r1_litres/f0, ci_v6b_espece/e0 ;
  - blocs ci_r_b1, ci_r_b2, ci_s1_b2, ci_s1_b2b, ci_s2_b1b, ci_s2_b2, ci_s4_b2.
- **Énoncés (`enonce_dit`) :** ci_g6_calcul/q (même texte que la réserve f0), ci_g6_calcul/e2, ci_v6b_espece/e0, exercice et retrouver du bloc ci_s2_b2.
- **Réactions préparées (sans audio) :** ci_g6_calcul e2 (5), ci_v6b_espece e0 (5), bloc ci_s2_b2 (5). Les réactions `q` de ci_g6 sont recopiées de sa réserve e0 : même texte, mêmes pistes.

### Vérifications faites (résultats)
- JSON valide, écrit en `json.dumps(ensure_ascii=False, indent=2)`, fins de ligne LF (0 CR). Le fichier a été relu juste avant l’écriture et il était identique à la copie de départ.
- `verif_attente.py` : 61 diapos, **0 mot absent, 0 hors bloc**, 0 doublon, 0 compétence inconnue, 19 diapos sans voix (les 19 ci-dessus).
- Script maison :
  - chaque `mot` de `centre`, `pointage` et des démonstrations est présent **et dans l’ordre** ;
  - chaque diapo est dans un seul bloc, et les blocs suivent l’ordre des diapos ;
  - au plus un tableau « À toi » par bloc ;
  - nouvelles voix et paroles : ni chiffre, ni symbole, ni tachkil ;
  - `audio` retiré partout où le texte a changé ;
  - états physiques présents dans toutes les équations écrites ;
  - aucune diapo ni aucune clé perdue.
- Les 33 erreurs que signale encore ce script existaient déjà dans la copie de départ : ce sont les réactions préparées absentes citées plus haut.
- `verifier_figures_cahier.py` : 10 figures, 0 erreur.
- Calculs refaits en Python :
  - titrage : 1,26·10⁻⁴ et 1,26·10⁻³ mol ; réserve 1,69·10⁻³ mol ;
  - conductimétrie : σ₀ = 0,2491 S/m ; σ_f = 0,091 S/m, retrouvé aussi par la droite σ(x) (0,0909) ; x = 0,500 et 0,797 mmol ; exercice σ croissante 0,50 mmol ;
  - pression : x = 9,99·10⁻⁴ et 5,01·10⁻⁴ mol ; bloc pression 0,249 mmol ;
  - nationaux : σ = 0,1698 S·m⁻¹ (2016 R) ; G = 0,01698 S (2018 R) ; v₁ = 0,781 mol·m⁻³·min⁻¹ (2021 N) ; 1,6 mmol·L⁻¹·min⁻¹ (2025 R) ; v(0) = 0,525 mol·m⁻³·min⁻¹ (ci_r1) ;
  - vitesse : d[H₂O₂]/dt(0) = −2,5 mmol·L⁻¹·min⁻¹, identique au modèle de la simulation ; tangente à 8 min (14,7 ; 16), pente −0,919 ;
  - t₁/₂ : 40 min ≈ 7,2·t₁/₂.
- Les `moment` et `repere` cités existent dans les simulations : resultat, relation, point_final, inverse, courbe_reactif.
