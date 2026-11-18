# Cahier de l'élève — SVT ch4 « Expression de l'information génétique » (`svt_ch4_relation_gene_proteine`)

18 novembre 2026, skill `cahier-de-l-eleve`. Source des lignes et des dessins : script de données
`donnees.py` + `appliquer.py` (scratchpad de la session) ; la section « Découpage » ci-dessous est générée depuis ces données.

## Plan (cours en ligne) et différences de la copie en attente

L'application écrit elle-même le titre du cours et le titre de chaque partie (I…IX, Bilan) ; les lignes portent le
sous-plan `1.`, `2.` qui repart à 1 dans chaque partie.

| Partie (en ligne) | Sous-plan du cahier en ligne | Copie en attente |
|---|---|---|
| I. Gène, allèle, mutation | 1. Rappels : l'ADN et la protéine · 2. Caractère, gène, allèle · 3. La mutation | « I. Caractère, gène, allèle, mutation » : 1. Caractère et phénotype (+ problème du chapitre, rappel ADN) · 2. Gène et allèle · 3. La mutation ; la protéine passe en II |
| II. Caractère et protéine | 1. Le phénotype à trois échelles (drépanocytose) · 2. Relation protéine – caractère (méthode, enzyme, albinisme, Beadle et Tatum) | 1. La protéine ; la drépanocytose · 2. Relation protéine – caractère (+ LDL 2023 N) · 3. Un gène, une enzyme |
| III. L'ARN, intermédiaire | 1. L'ARN, un intermédiaire (structure, 3 types, uracile radioactif) · 2. L'ARN messager | 1. Un intermédiaire : l'ARN (le problème posé en question d'abord) · 2. L'ARN messager |
| IV. La transcription | 1. La transcription (rappel brins, définition, arbre de Noël, règle) · 2. Le sens et le brin donné (méthode du barème) | 1. La transcription · 2. Base après base, et dans quel sens · 3. Écrire l'ARNm comme le barème |
| V. Le code génétique | 1. Le codon (4³, définition, Nirenberg) · 2. Lire le tableau · 3. Traduire un ARNm ; propriétés | idem (+ un exemple de traduction) |
| VI. La traduction | 1. Les acteurs (définition, ribosome, ARNt) · 2. Les trois étapes (+ polysome, schéma à légender) | 1. Les acteurs et les étapes (un seul sous-titre ; terminaison, polysome au bloc suivant) |
| VII. Les mutations | 1. Comparer les allèles · 2. La substitution (silencieuse, faux-sens, non-sens) · 3. Délétion et insertion | idem |
| VIII. Du gène au caractère | 1. Relation gène – protéine – caractère · 2. Le schéma de la synthèse des protéines · 3. Transcription ou traduction ? | idem |
| IX. L'exercice national | 1. Restitution · 2. Méthode de l'exercice national · 3. Deux exemples rédigés (2024 N, drépanocytose) | 1. Restitution · 2. Méthode · 3. Sujet 2024 N · 4. Sujet 2020 N (relation, hypothèse, vérification) · 5. Sujet 2022 N (ribosome) · 6. Retour à la drépanocytose |
| Bilan du chapitre | une ligne bilan gène → ARNm → protéine → caractère ; la bulle de la fiche reprend les parties I à IX | idem |

## Le cahier idéal (texte suivi, cours en ligne)

Le texte complet est la suite des lignes de la section « Découpage — cours en ligne » ; ses points forts :

- **Définitions mot pour mot** (« Définition : … ») : caractère héréditaire, phénotype, gène, allèle, mutation, enzyme,
  transcription, codon, traduction — les huit de la restitution sont toutes écrites avant le bloc « Restitution ».
- **Rappels du ch3 marqués « Rappel : »** là où ils servent : ADN deux brins / complémentarité (I), brins complémentaires
  et antiparallèles (IV, avant la transcription).
- **Conclusions d'expériences (« Donc … »)** : streptomycine (mutation spontanée), drépanocytose (un acide aminé), uracile
  radioactif, acides aminés radioactifs, in vitro, relation gène – protéine – caractère.
- **Méthodes du national** : relation protéine – caractère (2 lignes saine / malade, « d'où la relation ») ; écrire l'ARNm
  (nommer le brin, triplet sous triplet, aucun T) ; traduire (codon de l'ARNm, tableau, arrêt au stop sans tiret) ;
  comparer les allèles ; **méthode complète de l'exercice national en 5 étapes** (repérer → ARNm selon le brin → acides
  aminés avec le tableau → comparer les allèles → phrase de l'origine génétique qui relie protéine et phénotype).
- **Compléments** : Attention (allèle ≠ caractère, mutation ≠ maladie ; complémentarité seulement sur le brin transcrit ;
  délétion prise pour une substitution ; « l'ARN polymérase intervient dans la traduction » → faux, 2024 N), Exemple
  (2023 N LDL, 2024 N, 2025 N dans les bulles, délétion du G du triplet 3), sens 3'→5' / 5'→3'.

## Les dessins (9 ; même figure dans la diapositive qui l'enseigne et dans son bloc)

Couleurs du lexique : ARN orange, noyau violet, protéine / acides aminés violets, ribosome et ARN polymérase cyan
(turquoise), ADN blanc. Textes estimés sans chevauchement (boîtes calculées, script `bbox.py`).

| Diapositive | Dessin | Statut |
|---|---|---|
| rg_g2_allele | Un locus, deux allèles (paire de chromosomes, allèles A et O) | gardé |
| rg_p3_proteine | Hémoglobine A et S : chaîne β, le 6e acide aminé Glu → Val encadré | **ajouté** |
| rg_a3_uracile | Uracile radioactif : cellule à 5 min (noyau marqué) et à 30 min (cytoplasme marqué) | **ajouté** |
| rg_t2b_arbre_noel | Arbre de Noël : ADN, ARN orange de plus en plus longs, ARN polymérases, sens de la transcription | **ajouté** |
| rg_t4_sens | Le sens de la transcription (brin transcrit 3' TAC GCG TCA 5', ARNm 5' AUG CGC AGU 3') | corrigé : ARNm jaune → orange |
| rg_t5b_legender | Schéma de la transcription à légender (brins, ARN polymérase, ARNm, nucléotides libres) | **ajouté** |
| rg_r3_elongation | Élongation : ribosome (2 sous-unités), ARNm orange, ARNt UAC / GCG, Met – Arg, avance vers 3' | refait (ARNm, ARNt orange ; ribosome cyan ; acides aminés violets ; petite et grande sous-unité) |
| rg_m4_decalage | Délétion : cadre de lecture décalé (AUG CUG GAG UGG CAA → AUG CUG AGU GGC AAU) | **ajouté** |
| rg_s3_construire | Du gène à la protéine (noyau, pore, ribosome, protéine) | corrigé : noyau violet, ARNm orange, protéine violette |

## Découpage

### cours en ligne (`backend/data/courses/svt_ch4_relation_gene_proteine.json`)

**rg_s1_b1** (rg_d1_adn, rg_d2_proteine) — entre dans : I. Gène, allèle, mutation

- 1. Rappels : l'ADN et la protéine
- Rappel (ch. 3) : l'ADN a deux brins de nucléotides ; bases A, T, C, G.
- Rappel : les brins sont complémentaires : A en face de T, C en face de G.
- Protéine : chaîne d'acides aminés (20 sortes) enchaînés dans un ordre précis (séquence).
- L'ordre des acides aminés donne à la protéine sa forme, donc son rôle.

**rg_s1_b2** (rg_o1_caracteres, rg_g1_gene, rg_g2_allele)

- 2. Caractère, gène, allèle
- Définition : un caractère héréditaire est un caractère transmis de génération en génération.
- Définition : le phénotype est l'ensemble des caractères observables d'un individu.
- Définition : le gène est une portion d'ADN, située à un endroit précis (locus) d'un chromosome,
- qui détermine un caractère héréditaire.
- Définition : l'allèle est une des formes d'un même gène, située au même locus.
- *Figure : Un locus, deux allèles*

**rg_s1_b3** (rg_g3_mutation, rg_g3b_mutation)

- 3. La mutation
- Streptomycine : les colonies résistantes existaient avant l'antibiotique → mutation spontanée.
- Définition : la mutation est une modification de la séquence des nucléotides d'un gène.
- Elle est rare, spontanée ou provoquée (agents mutagènes : UV, rayons X), et héréditaire.
- Une mutation crée un nouvel allèle (allèle muté) ; l'allèle normal est dit « sauvage ».
- Attention : un allèle n'est pas un caractère ; une mutation n'est pas une maladie.

**rg_s2_b1** (rg_p1_organisme, rg_p2_cellule, rg_p3_proteine) — entre dans : II. Caractère et protéine

- 1. Le phénotype à trois échelles : la drépanocytose
- Phénotype macroscopique : anémie, crises douloureuses, essoufflement.
- Phénotype cellulaire : hématies en faucille, rigides, qui bouchent les petits vaisseaux.
- Phénotype moléculaire : hémoglobine S ; 6e acide aminé de la chaîne β : Glu → Val.
- Donc un seul acide aminé change : l'Hb S forme des fibres → hématies en faucille.
- *Figure : Hémoglobine A et S : la chaîne β*

**rg_s2_b1b** (rg_p4_document, rg_p4b_albinisme, rg_p5_beadle_tatum)

- 2. Relation protéine – caractère
- Protéine fonctionnelle → caractère normal ; protéine non fonctionnelle → caractère modifié.
- Méthode : saine / malade, protéine → rôle (lu dans le document) → phénotype ; « d'où la relation ».
- Définition : une enzyme est une protéine qui permet une réaction chimique précise.
- Albinisme : tyrosinase non fonctionnelle → pas de mélanine → peau et cheveux très clairs.
- Beadle et Tatum : chaque mutation rend une enzyme non fonctionnelle : un gène → une enzyme.

**rg_s2_b2** (rg_a1_arn, rg_a2_usine, rg_a3_uracile) — entre dans : III. L'ARN, intermédiaire entre l'ADN et la protéine

- 1. L'ARN, un intermédiaire
- ARN : un brin de nucléotides (acide phosphorique + ribose + base A, U, C ou G) : U remplace T.
- Trois types d'ARN : ARNm (messager), ARNt (de transfert), ARNr (des ribosomes).
- L'ADN reste dans le noyau, les protéines se font dans le cytoplasme : il faut un intermédiaire.
- Uracile radioactif (propre à l'ARN) : marquage d'abord dans le noyau, puis dans le cytoplasme.
- Donc l'ARN est synthétisé dans le noyau, puis migre au cytoplasme par les pores nucléaires.
- *Figure : Uracile radioactif : où est l'ARN ?*

**rg_s2_b2b** (rg_a4_acides_amines, rg_a5_in_vitro)

- 2. L'ARN messager (ARNm)
- Acides aminés radioactifs : marquage dans le cytoplasme, sur les ribosomes (noyau non marqué).
- Donc les protéines sont synthétisées dans le cytoplasme, au niveau des ribosomes.
- In vitro, sans ARNm : aucune protéine ; après injection d'ARNm : acides aminés incorporés.
- Donc l'ARNm est nécessaire : il porte l'information du gène, du noyau aux ribosomes.

**rg_s2_b3** (rg_t1_rappel, rg_t2_definition, rg_t2b_arbre_noel, rg_t3_bases) — entre dans : IV. La transcription

- Rappel (ch. 3) : les 2 brins d'ADN sont complémentaires (A–T, C–G) et antiparallèles.
- 1. La transcription
- Définition : la transcription est la synthèse, dans le noyau, d'un ARNm complémentaire
- du brin transcrit (ou brin matrice) d'un gène, par une enzyme, l'ARN polymérase.
- « Arbre de Noël » : plusieurs ARN polymérases sur un gène ; son début est du côté des ARN courts.
- Règle : brin transcrit → ARNm : A → U ; T → A ; C → G ; G → C (jamais de T dans l'ARN).
- *Figure : L'« arbre de Noël » (transcription)*

**rg_s3_b1** (rg_t4_sens, rg_t5_non_transcrit, rg_t5b_legender, rg_t6_bareme)

- 2. Le sens et le brin donné
- Le brin transcrit est lu de 3' vers 5' ; l'ARNm est synthétisé de 5' vers 3'.
- Brin non transcrit → ARNm : même séquence, T remplacé par U (pas de complémentarité).
- Attention : complémentarité sur le brin transcrit seulement ; entourer « non » dans l'énoncé.
- Méthode : 1) nommer le brin ; 2) ARNm sous le brin, triplet sous triplet, numérotés ; 3) aucun T.
- L'ARNm formé dans le noyau sort par les pores nucléaires vers le cytoplasme.
- *Figure : Le sens de la transcription*
- *Figure : Schéma de la transcription (à légender)*

**rg_s3_b2** (rg_c1_codon, rg_c1b_nirenberg, rg_c2_tableau, rg_c3_initiation_stop) — entre dans : V. Le code génétique

- 1. Le codon
- 4 bases, 20 acides aminés : 4² = 16 < 20, mais 4³ = 64 ≥ 20 : 3 nucléotides par acide aminé.
- Définition : un codon est une succession de trois nucléotides de l'ARNm (64 codons).
- Nirenberg et Matthaei : UUU… → Phe – Phe… ; UGUG… → Cys – Val – Cys… : lecture par 3.
- 2. Lire le tableau du code : 1re lettre en ligne, 2e en colonne, 3e dans la case.
- AUG = Met : codon d'initiation ; UAA, UAG, UGA : codons stop (aucun acide aminé).

**rg_s3_b3** (rg_c4_traduire, rg_c5_proprietes, rg_r1_acteurs) — entre dans : VI. La traduction

- 3. Traduire un ARNm ; propriétés du code
- Méthode : codons de l'ARNm (pas l'ADN) → tableau → Met – … ; au stop : arrêt, sans tiret.
- Code universel, redondant (codons synonymes), non ambigu, sans chevauchement : 61 codons + 3 stop.
- 1. Les acteurs de la traduction
- Définition : la traduction est la synthèse d'une protéine, dans le cytoplasme, à partir de l'ARNm.
- Ribosome : 2 sous-unités ; ARNt : porte un acide aminé et un anticodon complémentaire du codon.

**rg_s4_b1** (rg_r2_initiation, rg_r3_elongation, rg_r4_terminaison, rg_r5_polysome, rg_r6_legender)

- 2. Les trois étapes de la traduction
- Initiation : petite sous-unité sur AUG ; ARNt-Met (anticodon UAC) ; la grande sous-unité s'associe.
- Élongation : l'ARNt suivant apporte son acide aminé → liaison peptidique → le ribosome avance.
- Terminaison : codon stop, aucun ARNt ; la protéine est libérée, les sous-unités se séparent.
- Polysome : plusieurs ribosomes lisent le même ARNm → beaucoup de protéines identiques.
- Schéma à légender : ARNm, codon, anticodon, ARNt, acide aminé, liaison peptidique, 2 sous-unités.
- *Figure : L'élongation sur le ribosome*

**rg_s4_b2** (rg_m1_comparer, rg_m2_substitution, rg_m2b_faux_sens, rg_m3_non_sens) — entre dans : VII. Les mutations

- 1. Comparer les allèles
- Méthode : muté sous normal, triplets numérotés : brin → ARNm → acides aminés, jusqu'au bout.
- 2. La substitution : un nucléotide remplacé par un autre (un seul codon touché)
- Silencieuse : CUG (Leu) → CUA (Leu) : même acide aminé (code redondant) ; protéine inchangée.
- Faux-sens : GAG (Glu) → GUG (Val) : un autre acide aminé ; protéine modifiée (drépanocytose).
- Non-sens : UGG (Trp) → UAG (stop) : arrêt trop tôt ; protéine raccourcie (incomplète).

**rg_s4_b3** (rg_m4_decalage, rg_m5_trois, rg_m6_juger)

- 3. La délétion et l'insertion
- Délétion ou insertion d'1 nucléotide : décalage du cadre de lecture ; les codons suivants changent.
- Ex. délétion du G du triplet 3 : AUG CUG AGU GGC AAU → Met – Leu – Ser – Gly – Asn.
- Délétion (ou insertion) de 3 nucléotides : un acide aminé en moins (ou en plus), sans décalage.
- Donc l'effet d'une mutation se juge avec le code : il dépend du codon touché.
- Attention : tout change à partir d'un point → pas une substitution : chercher la lettre perdue.
- *Figure : Délétion : le cadre de lecture décalé*

**rg_s5_b1** (rg_s1_gpc, rg_s2_schema, rg_s3_construire) — entre dans : VIII. Du gène au caractère : le schéma de la synthèse des protéines

- 1. Relation gène – protéine – caractère
- Allèle normal → protéine fonctionnelle → caractère normal (HbA → hématies rondes → sain).
- Allèle muté → protéine non fonctionnelle → caractère muté (HbS → faucilles → drépanocytose).
- Donc le gène détermine la séquence des acides aminés de la protéine, qui détermine le caractère.
- 2. Le schéma de la synthèse des protéines
- Gène (ADN) → transcription (noyau) → ARNm → pore → traduction (ribosomes) → protéine → caractère.
- *Figure : Du gène à la protéine*

**rg_s5_b2** (rg_s4_trans_trad, rg_s5_etapes, rg_e1_restitution) — entre dans : IX. L'exercice national : rédiger comme le barème

- 3. Transcription ou traduction ?
- Transcription : noyau, ARN polymérase ; ADN → ARNm (nucléotides → nucléotides).
- Traduction : cytoplasme, ribosomes, ARNt ; ARNm → protéine (codons → acides aminés).
- Attention (2024 N) : « l'ARN polymérase intervient dans la traduction » → faux.
- 1. Restitution : huit définitions mot pour mot
- Caractère héréditaire, phénotype, gène, allèle, mutation, codon, transcription, traduction.

**rg_s5_b3** (rg_e2_reperages, rg_e3_lignes, rg_e4_phrase)

- 2. Méthode de l'exercice national
- 1) Repérer : la maladie, la protéine et son rôle, le brin donné, le type de mutation.
- 2) ARNm : brin transcrit → complémentarité ; brin non transcrit → même séquence, T → U.
- 3) Acides aminés avec le tableau ; 4) comparer les allèles (lignes alignées, différence encadrée).
- 5) Origine : mutation par (type) du nucléotide X par Y au triplet n du brin (non) transcrit
- → codon … devient … → acide aminé remplacé → protéine non fonctionnelle → rôle perdu → maladie.

**rg_s6_b1** (rg_e5_national, rg_e6_drepanocytose, rg_b1_bilan, rg_b2_carte) — entre dans : Bilan du chapitre

- 3. Deux exemples rédigés comme le barème
- 2024 N (brin non transcrit) : triplet 3, CCC → CTC → codon CCC devient CUC → Pro remplacé par Leu
- → amélogénine anormale → minéralisation faible de l'émail → amélogénèse imparfaite.
- Drépanocytose : substitution du 2e nucléotide T par A au triplet 6 du brin transcrit (CTC → CAC)
- → codon GAG devient GUG → Glu remplacé par Val → Hb S en fibres → hématies en faucille.
- Bilan : gène → transcription (noyau) → ARNm → traduction (cytoplasme) → protéine → caractère.

Bulles de diapositive : une ou deux phrases (≤ 180 caractères) par diapositive ; figures sur rg_g2_allele, rg_p3_proteine, rg_a3_uracile, rg_t2b_arbre_noel, rg_t4_sens, rg_t5b_legender, rg_r3_elongation, rg_m4_decalage, rg_s3_construire , aucune ailleurs.

### copie en attente (`backend/data/courses/en_attente/svt_ch4_relation_gene_proteine.json`)

**rg_s1_b1** (rg_o1_caracteres, rg_d1_adn) — entre dans : I. Caractère, gène, allèle, mutation

- 1. Caractère et phénotype
- Définition : un caractère héréditaire est un caractère transmis de génération en génération.
- Définition : le phénotype est l'ensemble des caractères observables d'un individu.
- Problème : comment l'information de l'ADN du noyau devient-elle un caractère observable ?
- Rappel (ch. 3) : l'ADN a deux brins ; bases A, T, C, G ; A en face de T, C en face de G.

**rg_s1_b2** (rg_g1_gene, rg_g2_allele)

- 2. Gène et allèle
- Définition : le gène est une portion d'ADN, située à un endroit précis (locus) d'un chromosome,
- qui détermine un caractère héréditaire.
- Définition : l'allèle est une des formes d'un même gène, située au même locus.
- Une cellule a 2 allèles de chaque gène (chromosomes homologues) : identiques ou différents.
- *Figure : Un locus, deux allèles*

**rg_s1_b3** (rg_g3_mutation, rg_g3b_mutation)

- 3. La mutation
- Streptomycine : les colonies résistantes existaient avant l'antibiotique → mutation spontanée.
- Définition : la mutation est une modification de la séquence des nucléotides d'un gène.
- Elle est rare, spontanée ou provoquée (agents mutagènes : UV, rayons X), et héréditaire.
- Une mutation crée un nouvel allèle (allèle muté) ; l'allèle normal est dit « sauvage ».
- Attention : un allèle n'est pas un caractère ; une mutation n'est pas une maladie.

**rg_s2_b1** (rg_d2_proteine, rg_p1_organisme, rg_p2_cellule) — entre dans : II. Caractère et protéine

- 1. La protéine ; la drépanocytose
- Protéine : chaîne d'acides aminés (20 sortes) enchaînés dans un ordre précis (séquence).
- L'ordre des acides aminés donne à la protéine sa forme, donc son rôle.
- Phénotype macroscopique : anémie, crises douloureuses, essoufflement.
- Phénotype cellulaire : hématies en faucille, rigides, qui bouchent les petits vaisseaux.

**rg_s2_b2** (rg_p3_proteine, rg_p4_document)

- Phénotype moléculaire : hémoglobine S ; 6e acide aminé de la chaîne β : Glu → Val.
- Donc un seul acide aminé change : l'Hb S forme des fibres → hématies en faucille.
- 2. Relation protéine – caractère
- Protéine fonctionnelle → caractère normal ; protéine non fonctionnelle → caractère modifié.
- Méthode : saine / malade, protéine → rôle (lu dans le document) → phénotype ; « d'où la relation ».
- Ex. 2023 N : récepteur LDL anormal → les LDL n'entrent plus → cholestérol accumulé dans le sang.
- *Figure : Hémoglobine A et S : la chaîne β*

**rg_s2_b3** (rg_p4b_albinisme, rg_p5_beadle_tatum)

- 3. Un gène, une enzyme
- Définition : une enzyme est une protéine qui permet une réaction chimique précise.
- Albinisme : tyrosinase non fonctionnelle → pas de mélanine → peau et cheveux très clairs.
- Beadle et Tatum : précurseur → ornithine → citrulline → arginine (enzymes E1, E2, E3).
- Chaque mutation rend une seule enzyme non fonctionnelle : un gène → une enzyme (une protéine).

**rg_s3_b1** (rg_a2_usine, rg_a1_arn, rg_a3_uracile) — entre dans : III. L'ARN, intermédiaire entre l'ADN et la protéine

- 1. Un intermédiaire : l'ARN
- Problème : l'ADN ne quitte pas le noyau ; où se font les protéines, et comment l'information y va ?
- ARN : un brin de nucléotides (acide phosphorique + ribose + base A, U, C ou G) : U remplace T.
- Trois types d'ARN : ARNm (messager), ARNt (de transfert), ARNr (des ribosomes).
- Uracile radioactif (propre à l'ARN) : marquage d'abord dans le noyau, puis dans le cytoplasme.
- Donc l'ARN est synthétisé dans le noyau, puis migre au cytoplasme par les pores nucléaires.
- *Figure : Uracile radioactif : où est l'ARN ?*

**rg_s3_b2** (rg_a4_acides_amines, rg_a5_in_vitro)

- 2. L'ARN messager (ARNm)
- Acides aminés radioactifs : marquage dans le cytoplasme, sur les ribosomes (noyau non marqué).
- Donc les protéines sont synthétisées dans le cytoplasme, au niveau des ribosomes.
- In vitro, sans ARNm : aucune protéine ; après injection d'ARNm : acides aminés incorporés.
- Donc l'ARNm est nécessaire : il porte l'information du gène, du noyau aux ribosomes.

**rg_s3_b3** (rg_t1_rappel, rg_t2_definition, rg_t2b_arbre_noel) — entre dans : IV. La transcription

- Rappel (ch. 3) : les 2 brins d'ADN sont complémentaires (A–T, C–G) et antiparallèles.
- 1. La transcription
- Définition : la transcription est la synthèse, dans le noyau, d'un ARNm complémentaire
- du brin transcrit (ou brin matrice) d'un gène, par une enzyme, l'ARN polymérase.
- « Arbre de Noël » : plusieurs ARN polymérases sur un gène ; son début est du côté des ARN courts.
- *Figure : L'« arbre de Noël » (transcription)*

**rg_s4_b1** (rg_t3_bases, rg_t4_sens, rg_t5_non_transcrit)

- 2. Base après base, et dans quel sens
- Règle : brin transcrit → ARNm : A → U ; T → A ; C → G ; G → C (jamais de T dans l'ARN).
- Le brin transcrit est lu de 3' vers 5' ; l'ARNm est synthétisé de 5' vers 3'.
- Brin non transcrit → ARNm : même séquence, T remplacé par U (pas de complémentarité).
- Attention : complémentarité sur le brin transcrit seulement ; entourer « non » dans l'énoncé.
- *Figure : Le sens de la transcription*

**rg_s4_b2** (rg_t5b_legender, rg_t6_bareme)

- 3. Écrire l'ARNm comme le barème
- Schéma à légender : brin transcrit, brin non transcrit, ARN polymérase, ARNm, nucléotides libres.
- Méthode : 1) nommer le brin ; 2) ARNm sous le brin, triplet sous triplet, numérotés ; 3) aucun T.
- L'ARNm formé dans le noyau sort par les pores nucléaires vers le cytoplasme.
- *Figure : Schéma de la transcription (à légender)*

**rg_s4_b3** (rg_c1_codon, rg_c1b_nirenberg, rg_c2_tableau) — entre dans : V. Le code génétique

- 1. Le codon
- 4 bases, 20 acides aminés : 4² = 16 < 20, mais 4³ = 64 ≥ 20 : 3 nucléotides par acide aminé.
- Définition : un codon est une succession de trois nucléotides de l'ARNm (64 codons).
- Nirenberg et Matthaei : UUU… → Phe – Phe… ; UGUG… → Cys – Val – Cys… : lecture par 3.
- 2. Lire le tableau du code : 1re lettre en ligne, 2e en colonne, 3e dans la case.

**rg_s5_b1** (rg_c3_initiation_stop, rg_c4_traduire, rg_c5_proprietes)

- AUG = Met : codon d'initiation ; UAA, UAG, UGA : codons stop (aucun acide aminé).
- 3. Traduire un ARNm ; propriétés du code
- Méthode : codons de l'ARNm (pas l'ADN) → tableau → Met – … ; au stop : arrêt, sans tiret.
- Ex. AUG GAA UUU CCG UAA → Met – Glu – Phe – Pro.
- Code universel, redondant (codons synonymes), non ambigu, sans chevauchement : 61 codons + 3 stop.

**rg_s5_b2** (rg_r1_acteurs, rg_r2_initiation, rg_r3_elongation) — entre dans : VI. La traduction

- 1. Les acteurs et les étapes
- Définition : la traduction est la synthèse d'une protéine, dans le cytoplasme, à partir de l'ARNm.
- Ribosome : 2 sous-unités ; ARNt : porte un acide aminé et un anticodon complémentaire du codon.
- Initiation : petite sous-unité sur AUG ; ARNt-Met (anticodon UAC) ; la grande sous-unité s'associe.
- Élongation : l'ARNt suivant apporte son acide aminé → liaison peptidique → le ribosome avance.
- *Figure : L'élongation sur le ribosome*

**rg_s5_b3** (rg_r4_terminaison, rg_r5_polysome, rg_r6_legender)

- Terminaison : codon stop, aucun ARNt ; la protéine est libérée, les sous-unités se séparent.
- Polysome : plusieurs ribosomes lisent le même ARNm → beaucoup de protéines identiques.
- Schéma à légender : ARNm, codon, anticodon, ARNt, acide aminé, liaison peptidique, 2 sous-unités.
- Retenir : initiation, élongation, terminaison = les trois étapes de la traduction.

**rg_s6_b1** (rg_m1_comparer, rg_m2_substitution, rg_m2b_faux_sens, rg_m3_non_sens) — entre dans : VII. Les mutations

- 1. Comparer les allèles
- Méthode : muté sous normal, triplets numérotés : brin → ARNm → acides aminés, jusqu'au bout.
- 2. La substitution : un nucléotide remplacé par un autre (un seul codon touché)
- Silencieuse : CUG (Leu) → CUA (Leu) : même acide aminé (code redondant) ; protéine inchangée.
- Faux-sens : GAG (Glu) → GUG (Val) : un autre acide aminé ; protéine modifiée (drépanocytose).
- Non-sens : UGG (Trp) → UAG (stop) : arrêt trop tôt ; protéine raccourcie (incomplète).

**rg_s6_b2** (rg_m4_decalage, rg_m5_trois, rg_m6_juger)

- 3. La délétion et l'insertion
- Délétion ou insertion d'1 nucléotide : décalage du cadre de lecture ; les codons suivants changent.
- Ex. délétion du G du triplet 3 : AUG CUG AGU GGC AAU → Met – Leu – Ser – Gly – Asn.
- Délétion (ou insertion) de 3 nucléotides : un acide aminé en moins (ou en plus), sans décalage.
- Donc l'effet d'une mutation se juge avec le code : il dépend du codon touché.
- Attention : tout change à partir d'un point → pas une substitution : chercher la lettre perdue.
- *Figure : Délétion : le cadre de lecture décalé*

**rg_s6_b3** (rg_s1_gpc, rg_s2_schema, rg_s3_construire) — entre dans : VIII. Du gène au caractère : le schéma de la synthèse des protéines

- 1. Relation gène – protéine – caractère
- Allèle normal → protéine fonctionnelle → caractère normal (HbA → hématies rondes → sain).
- Allèle muté → protéine non fonctionnelle → caractère muté (HbS → faucilles → drépanocytose).
- Donc le gène détermine la séquence des acides aminés de la protéine, qui détermine le caractère.
- 2. Le schéma de la synthèse des protéines
- Gène (ADN) → transcription (noyau) → ARNm → pore → traduction (ribosomes) → protéine → caractère.
- *Figure : Du gène à la protéine*

**rg_s7_b1** (rg_s4_trans_trad, rg_s5_etapes, rg_e1_restitution) — entre dans : IX. L'exercice national : rédiger comme le barème, une consigne à la fois

- 3. Transcription ou traduction ?
- Transcription : noyau, ARN polymérase ; ADN → ARNm (nucléotides → nucléotides).
- Traduction : cytoplasme, ribosomes, ARNt ; ARNm → protéine (codons → acides aminés).
- Attention (2024 N) : « l'ARN polymérase intervient dans la traduction » → faux.
- 1. Restitution : huit définitions mot pour mot
- Caractère héréditaire, phénotype, gène, allèle, mutation, codon, transcription, traduction.

**rg_s7_b2** (rg_e2_reperages, rg_e3_lignes, rg_e4_phrase)

- 2. Méthode de l'exercice national
- 1) Repérer : la maladie, la protéine et son rôle, le brin donné, le type de mutation.
- 2) ARNm : brin transcrit → complémentarité ; brin non transcrit → même séquence, T → U.
- 3) Acides aminés avec le tableau ; 4) comparer les allèles (lignes alignées, différence encadrée).
- 5) Origine : mutation par (type) du nucléotide X par Y au triplet n du brin (non) transcrit
- → codon … devient … → acide aminé remplacé → protéine non fonctionnelle → rôle perdu → maladie.

**rg_s7_b3** (rg_e5a_document, rg_e5_national)

- 3. Sujet 2024 N (amélogénèse imparfaite), une consigne à la fois
- 1) Saine : amélogénine normale → minéralisation normale → émail normal ;
- malade : amélogénine anormale → minéralisation faible → émail atteint ; d'où la relation.
- 2) Brin non transcrit, triplet 3 : CCC → CTC ; ARNm : CCC (Pro) → CUC (Leu).
- 3) Substitution du 2e nucléotide C par T au triplet 3 du brin non transcrit du gène AMELX
- → CCC devient CUC → Pro remplacé par Leu → amélogénine anormale → amélogénèse imparfaite.

**rg_s8_b1** (rg_e7_moustiques, rg_e7b_hypothese, rg_e7c_verifier)

- 4. Sujet 2020 N : relation, hypothèse, vérification
- Relation : S : AChE bloquée par le carbamate (97 → 0 %) → mortalité 100 % dès 1 mg/L ;
- R : activité de l'AChE presque stable (32 → 28 %) → mortalité seulement vers 2·10² mg/L.
- Hypothèse (au conditionnel) : une mutation du gène de l'AChE modifierait son site actif.
- Vérification : triplet 247, GGC (Gly) → AGC (Ser) : substitution G par A → AChE modifiée
- → le carbamate ne s'y fixe plus → résistance : l'hypothèse est vérifiée.

**rg_s8_b2** (rg_e8_ribosomes, rg_e8b_hemoglobine)

- 5. Sujet 2022 N : le ribosome (anémie de Blackfan-Diamond)
- Comparer : sain : petites = grandes sous-unités (46 UA) ; malade : petites (23 UA) = moitié.
- Expliquer : manque de petites sous-unités → peu de ribosomes fonctionnels
- → faible traduction de l'ARNm de l'hémoglobine → peu d'hémoglobine → anémie.

**rg_s8_b3** (rg_e6_drepanocytose, rg_b1_bilan, rg_b2_carte) — entre dans : Bilan du chapitre

- 6. Retour à la drépanocytose
- Substitution du 2e nucléotide T par A au triplet 6 du brin transcrit du gène β (CTC → CAC)
- → codon GAG devient GUG → Glu remplacé par Val → Hb S en fibres → hématies en faucille.
- Bilan : gène → transcription (noyau) → ARNm → traduction (cytoplasme) → protéine → caractère.

Bulles de diapositive : une ou deux phrases (≤ 180 caractères) par diapositive ; figures sur rg_g2_allele, rg_p3_proteine, rg_a3_uracile, rg_t2b_arbre_noel, rg_t4_sens, rg_t5b_legender, rg_r3_elongation, rg_m4_decalage, rg_s3_construire , aucune ailleurs.


## Ce qui reste / doutes

- **Blocs à cheval sur deux parties** (en ligne : `rg_s3_b3` V→VI, `rg_s5_b2` VIII→IX, `rg_s6_b1` IX→Bilan ; en attente :
  `rg_s7_b1`, `rg_s8_b3`) : l'application écrit le titre de la nouvelle partie au-dessus de TOUTES les lignes du bloc ;
  les lignes de la fin de l'ancienne partie se lisent donc sous le titre de la suivante (la numérotation, elle, est juste).
  À corriger dans `CycleBloc.tsx` (titre de partie posé avant la première ligne de cette partie) ou en redécoupant les blocs.
- Quelques définitions tiennent sur deux lignes (gène, transcription) pour rester mot pour mot sous ~100 caractères.
- Les boîtes de texte des dessins sont estimées (0,56 × taille de police par caractère) : à revoir à l'écran, surtout
  l'alignement des acides aminés sous les ARNt (élongation) et la flèche « G perdu » (délétion).
- Ribosome et ARN polymérase en cyan (turquoise du cours) : ces deux objets n'ont pas encore de fiche au lexique visuel.
- Le cours en ligne affirme à `rg_a2_usine` que les protéines se font dans le cytoplasme avant l'expérience `rg_a4` ; le
  cahier en ligne suit le cours (la copie en attente pose la question à la place).
