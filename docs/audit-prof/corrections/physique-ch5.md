## Noyaux, masse et énergie

Fichier modifié : `backend/data/courses/en_attente/phys_ch5_energie_nucleaire.json`. On part de la copie de ce matin et rien n'est perdu : on n'a retiré que les `audio` des voix changées. Le cours passe de 46 à 48 diapos. Script : `scratchpad/ch5p/patch.py`. Copie d'avant : `scratchpad/ch5p/backup_avant.json`. Contrôle : `scratchpad/ch5p/verif.py`.

### Manques corrigés
| Constat (audit) | Ce qui a été fait | Diapo(s) |
|---|---|---|
| Haute : « énergie de masse », « au repos », aucun calcul (cadre : « calculer l'énergie de masse ») | Lead, puces, cahier et voix : « toute particule de masse m, au repos, possède une énergie de masse E = m·c² », relue mot pour mot. **Nouvelle diapo** sans visuel, dans le bloc en_s1_b1b, compétence C1 : le proton en 6 lignes de centre. Calcul : E₀ = m_p·c² = 1,00728 u·c² = 1,00728 × 931,5 MeV ≈ 938,3 MeV = 938,3 × 1,6·10⁻¹³ J ≈ 1,50·10⁻¹⁰ J, avec un contrôle par le kg. Exercice de fin de cours : énergie de masse de ⁴He (3,73·10³ MeV), avec sa démonstration et 5 réactions. La fiche (bloc 1) est complétée. | en_m2_einstein, **en_m4b_energie_masse**, en_z1_bilan |
| Moyenne : applications et dangers, pénétration α/β/γ (cadre ; traité ici seulement, pas en ch4) | **Nouvelle diapo** sans visuel, placée après la réaction en chaîne, dans le bloc en_s2_b3, compétence C5. Pénétration : α arrêté par le papier, β par quelques mm d'aluminium, γ par du plomb ou du béton. Dangers : cellules abîmées, selon le type et la dose. Protection. Applications : médecine, datation, industrie, agriculture, centrales. La diapo a 5 lignes de centre, un **schéma au cahier** (source → papier / aluminium / plomb) et un QCM de fin de cours (« le plus pénétrant ») avec 5 réactions. Une ligne est ajoutée à la fiche. | **en_r3b_applications_dangers**, en_z1_bilan |
| Moyenne : forme développée E_ℓ = [Z·m_p + (A − Z)·m_n − m(X)]·c² | Écrite au centre, dans les puces, au cahier du bloc et dans la fiche (bloc 3 et formules). | en_l2_former, en_z1_bilan |
| Moyenne : définition du défaut de masse absente du cahier ; « au repos » | La phrase « différence entre la somme des masses des nucléons séparés, au repos, et la masse du noyau au repos » est ajoutée aux puces, au cahier, au cahier du bloc et à la fiche (bloc 2). La voix la relit. | en_d3_formule, en_z1_bilan |
| Moyenne : calcul de 1 u = 1,66·10⁻²⁷ kg | 5 lignes de centre : 1 u = m(¹²C)/12 ; m(¹²C) = M/N_A ; 12 g/mol = 12·10⁻³ kg/mol ; substitution ; résultat. La voix fait d'abord un rappel de la mole. | en_m3_unites |
| Moyenne : tracer le diagramme énergétique | Méthode en 4 étapes (puces et cahier) : nucléons en haut, puis niveau E_i, puis niveau E_f, puis flèche ΔE. Les paliers E_i / E_f sont ajoutés au dessin du cahier. Exercice de fin de cours (national 2019 N, Rn → Po + He) : ordonner les niveaux, démonstration en 7 lignes, 5 réactions. | en_e1_diagramme, en_e3_2023 |
| Basse : bombe A / bombe H, « pression », neutron neutre, forme de l'énergie libérée | Puces et cahier (écrit seulement) : emballement → bombe A ; fusion non contrôlée → bombe H ; « température et pression très élevées » ; « le neutron est neutre, il n'est pas repoussé » ; « énergie cinétique des produits et rayonnement γ ». | en_r3_chaine, en_r4_fusion, en_r2_fission, en_b1_masse_diminue |
| Oral seulement : « × 931,5 MeV/c² × c² » | Ligne écrite au centre (voix inchangée sur en_m4) et ligne par ligne sur en_l3. Les « MeV/u » des réactions écrites sont remplacés (9 champs). | en_m4_931, en_l3_calcul |
| Oral seulement : allure de la courbe d'Aston | Puce et cahier : « descend vite, creux vers A ≈ 56, remonte doucement ». | en_a1_courbe |
| Notations | E_i / E_f sur le diagramme. Forme à 4 noyaux Δm = [m(X₃) + m(X₄)] − [m(X₁) + m(X₂)]. ΔE = E_f − E_i dans la fiche. | en_e1, en_b2_methode, en_z1 |
| Erreur trouvée | en_n3_2025, exercice 0 : la bonne réponse « 7,6·10¹⁰ J » ne suit pas de la donnée 4,7·10²³ MeV (4,7 × 1,6 = 7,52). Les réactions disaient « 7,52 ≈ 7,6 », et deux paroles avaient des nombres en chiffres arabes écrits en lettres. Corrigé : la clé devient **7,5·10¹⁰ J**, avec une démonstration en 4 lignes et 5 réactions réécrites (aussi dans le bloc en_s4_b1). Un chiffre restait dans une parole de réaction du bloc en_s1_b3 : il est écrit en mots. | en_n3_2025, blocs |

### Non corrigés et pourquoi
- Manques signalés chez un seul professeur (définition de l'eV, équation de dissociation de Li, N = m/m(noyau), perte relative de masse) : non ajoutés, le cadre ne les exige pas.
- La fiche `cadre_reference_2bac_pc.json` (energie_nucleaire) n'a pas de capacité « applications / dangers ». La nouvelle diapo est donc rattachée à C5. **À décider** : ajouter une capacité EN9, car le PDF officiel la demande. Je n'ai pas modifié la fiche (consigne).
- Simulations non modifiées (consigne). `figures.html?fig=fig_liaison` écrit encore « 931,5 MeV/u ». `bilan.html` et `carte.html` n'affichent ni l'énergie de masse, ni la pénétration, ni la forme développée : seules les puces et le cahier de en_z1 sont à jour.
- Les deux nouvelles diapos n'ont pas de visuel (aucune vue du chapitre ne convient) : le centre seul (5 et 6 lignes) et un schéma au cahier.
- en_l4_par_nucleon, exercice de fin de cours (Ni 60) : 9 lignes, une de plus que ~8. Une seule démonstration par exercice est possible dans le format, je l'ai gardée.
- en_b5_beta, en_e4_polonium : la voix de la diapo résume le calcul, mais la démonstration de la question, juste après, le fait ligne par ligne. Je les ai gardées.

### Démonstrations
- Relues : toutes. Cela fait 21 démonstrations (questions, exercices, fin de cours, blocs), 14 diapos-preuves avec des lignes de centre, et les réactions « 2 » de calcul.
- Réécrites ou créées (17) :
  - diapos, une ligne de centre par étape sur son mot : en_m2b (voix inchangée), en_m3, en_m4b (nouvelle), en_d3, en_l2, en_l3, en_r5, en_b3, en_b4, en_e1, en_e2, en_e3, en_n1 ;
  - démonstrations : en_m4b/fin (nouvelle), en_r5/question (nouvelle), en_e3/fin (nouvelle), en_n3/e0, en_p2/question (nouvelle), bloc en_s1_b0 (nouvelle), bloc en_s3_b1 (nouvelle).
- Gardées telles quelles (complètes depuis ce matin) : en_m4 q/e0, en_d4 q, en_l3 q, en_l4 fin, en_s2 q, en_a3 q, en_b5 q/e0, en_e4 q/e0, en_n3 q, en_c2 q, bloc en_s1_b3.

Exemples avant → après :
1. en_l2 : « la masse perdue devient énergie, donc E_ℓ = Δm·c² » → E(nucléons) = [Z·m_p + (A − Z)·m_n]·c² ; E(noyau) = m(X)·c² ; E(noyau) + E_ℓ = E(nucléons) ; E_ℓ = E(nucléons) − E(noyau) ; E_ℓ = [Z·m_p + (A − Z)·m_n − m(X)]·c² ; E_ℓ = Δm·c².
2. en_e2/en_e3 : « deux routes, la même réponse » constaté → E_ℓ(X) = [m(nucléons) − m(X)]·c² ; on remplace dans ΔE ; les nucléons sont les mêmes (A et Z conservés), donc leurs masses s'annulent ; ΔE = [Σm(produits) − Σm(réactifs)]·c² = Δm·c².
3. en_b3 (2016 N) : la voix s'arrêtait à « fois 931,5 » → Σm(produits) = 5,01016 u ; Σm(réactifs) = 5,02905 u ; Δm = −0,01889 u ; ΔE = −0,01889 × 931,5 MeV ≈ −17,6 MeV ; E_lib = |ΔE| = 17,6 MeV.

### Voix à enregistrer (id)
- Pistes de diapo (14) : en_m2_einstein, en_m3_unites, **en_m4b_energie_masse**, en_d3_formule, en_l2_former, en_l3_calcul, **en_r3b_applications_dangers**, en_r5_soddy, en_b3_fusion_calcul, en_b4_fission_calcul, en_e1_diagramme, en_e2_formule, en_e3_2023, en_n1_echantillon.
- Réactions préparées : en_n3_2025 e0 (0/juste, 1/1, 1/2, 2/1, 2/2).
- Démonstrations : en_r5_soddy/q, en_p2_puissances/q, en_n3_2025/e0.
- Fin de cours (non joués aujourd'hui) : en_m4b e0, en_r3b e0, en_e3 e0 (énoncé, démonstration, 5 réactions chacun).
- Blocs (non joués aujourd'hui) : démonstrations des blocs en_s1_b0 et en_s3_b1.

### Vérifications faites (résultats)
- JSON valide. Écrit avec json.dumps(ensure_ascii=False, indent=2), en LF (0 CR). Le fichier a été relu juste avant l'écriture : il était identique à la copie de ce matin.
- Différence avec la copie de ce matin : les seules suppressions sont 12 `audio` de diapo et 5 `audio` de réaction, tous liés à une voix changée.
- `verif_attente.py` : 48 diapos, 0 mot absent, 0 hors bloc, 0 doublon, 0 compétence inconnue. 14 diapos sans voix : ce sont celles à enregistrer.
- Script maison `verif.py`, 0 problème :
  - chaque `mot` (centre, pointage, lignes) est présent, et dans l'ordre de sa voix ;
  - les nouvelles voix et paroles n'ont ni chiffre, ni symbole, ni tachkil ;
  - chaque diapo est dans un seul bloc, dans l'ordre du cours ; aucun bloc n'a plus de 4 diapos ni plus d'une question ;
  - compétences cohérentes ;
  - réactions présentes pour chaque option des nouveaux exercices.
- `verifier_figures_cahier.py` : 4 figures, 0 erreur.
- Calculs refaits en Python :
  - unités : 1 u = 1,661·10⁻²⁷ kg ; 931,49 MeV ; proton 938,28 MeV, 1,501·10⁻¹⁰ J (1,505·10⁻¹⁰ J par le kg) ;
  - hélium : E₀(⁴He) = 3727,4 MeV ; Δm(He) = 0,03038 u (4,03188 − 4,00150) ; E_ℓ = 28,299 MeV = 4,53·10⁻¹² J ;
  - réactions : Soddy 236 = 234 + x, x = 2 ; fusion 5,01016 − 5,02905 = −0,01889 u → −17,596 MeV ; fission 235,80382 − 236,00216 = −0,19834 u → −184,75 MeV, 2,96·10⁻¹¹ J ;
  - énergies de liaison : diagramme 10,841 − 28,296 = −17,455 MeV ; Rn 1707,18 / 1713,42 → −6,24 MeV ;
  - échantillon : 1/235 = 4,26·10⁻³ mol → 2,56·10²¹ noyaux ; pétrole 2 143 t et 1,8 t ; 4,7 × 1,6 = 7,52 ; C12 92,15 MeV.
