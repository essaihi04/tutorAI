# Rapport de vérification VISUELLE — 2022-normale

Vérification faite par lecture directe des images `pages/*.jpg` et comparaison avec `exam.json`.

**Titre** : Examen National du Baccalauréat - SVT 2022 Normale
**Pages sujet** : 6 | **Pages correction** : 4
**Documents** : 10 | **Questions JSON** : 17

## Structure attendue vs JSON

### Partie I : Restitution des connaissances (5 pts) — Page 1

| Élément image | Points image | JSON | Statut |
|---|---|---|---|
| I.1 Définissez : chaîne respiratoire / rendement énergétique | 1 pt | 1 pt | ✅ |
| I.2 Citez deux voies métaboliques de régénération d'ATP | 1 pt | 1 pt | ✅ |
| II.1 Dans la mitochondrie (QCM a/b/c/d) | 0.5 pt | 0.5 pt (b) | ✅ |
| II.2 Réduction de NAD⁺ en NADH (QCM) | 0.5 pt | 0.5 pt (a) | ✅ |
| II.3 Ultrastructure sarcomère (QCM) | 0.5 pt | 0.5 pt (c) | ✅ |
| II.4 Filaments fins myofibrille (QCM) | 0.5 pt | 0.5 pt (c) | ✅ |
| III Association (Ens1 × Ens2) | 1 pt | 1pt (1→c, 2→a, 3→e, 4→b) | ✅ |
| **Total Partie I** | **5 pts** | **5 pts (si I compte 2 pts)** | ⚠ |

**⚠ Problème de sommation** : la question parente `"id": "I"` n'a pas de champ `"points"` (seulement ses `sub_questions` ont 1 pt chacune). Le script `verify_exam.py` ne somme pas récursivement → reporte `P1 Σ=3 ≠ 5`.
- **Cause réelle** : Q I = 2 pts (1+1), Q II = 2 pts, Q III = 1 pt → total = 5 pts ✅ côté contenu
- **Correction à apporter** : ajouter `"points": 2` à la question parent `I`

### Partie II : Raisonnement scientifique (15 pts)

#### Exercice 1 (5 pts) — Pages 2-3 : Anémie Blackfan-Diamond + Génétique drosophile
| Question | Points image | JSON | Docs visibles | Docs JSON | Statut |
|---|---|---|---|---|---|
| Q1 comparaison ribosomes (doc 1) | 1 pt | 1 pt | D1 | doc_e1_1 (doc1p2.png) | ✅ |
| Q2 ARNm + séquences allèles (docs 2,3) | 1.5 pts | 1.5 pts | D2, D3 | doc_e1_2, doc_e1_3 | ✅ |
| Q3 mode transmission (doc 4) | 0.5 pt | 0.5 pt | D4 | doc_e1_4 | ✅ |
| Q4 génotypes lignées A,B,C (doc 4) | 1 pt | 1 pt | D4 | doc_e1_4 | ✅ |
| Q5 interprétation chromosomique (doc 4) | 1 pt | 1 pt | D4 | doc_e1_4 | ✅ |
| **Total** | **5 pts** | **5 pts** | — | — | ✅ |

#### Exercice 2 (5 pts) — Pages 4-5 : Riziculture et méthane
| Question | Points image | JSON | Docs visibles | Docs JSON | Statut |
|---|---|---|---|---|---|
| Q1 variation CH₄ (fig a doc 1) | 0.5 pt | 0.5 pt | D1 | doc_e2_1 (doc1p4.png) | ✅ |
| Q2 riziculture-réchauffement (doc 1 abc) | 1.25 pts | 1.25 pts | D1 | doc_e2_1 | ✅ |
| Q3 formation méthane rizières (fig a doc 2) | 0.5 pt | 0.5 pt | D2 | doc_e2_2 (doc2p4.png) | ✅ |
| Q4 quantité CH₄ 1950/1986 (fig b doc 2) | 1.5 pts | 1.5 pts | D2 | doc_e2_2 | ✅ |
| Q5 comparaison études + solutions (doc 3) | 1.25 pts | 1.25 pts | D3 | doc_e2_3 (doc3p5.png) | ✅ |
| **Total** | **5 pts** | **5 pts** | — | — | ✅ |

#### Exercice 3 (5 pts) — Pages 5-6 : Subduction, péridotite, métamorphisme
| Question | Points image | JSON | Docs visibles | Docs JSON | Statut |
|---|---|---|---|---|---|
| Q1 caractéristiques subduction (doc 1) | 1 pt | 1 pt | D1 | doc_e3_1 (doc1p5.png) | ✅ |
| Q2 fusion partielle péridotite (doc 2) | 1 pt | 1 pt | D2 | doc_e3_2 (doc2p6.png) | ✅ |
| Q3 conditions fusion dans subduction (doc 1) | 1 pt | 1 pt | D1 | doc_e3_1 | ✅ |
| Q4 roches A/B, métamorphisme (doc 3 a-d) | 2 pts | 2 pts | D3 | doc_e3_3 (doc3p6.png) | ✅ |
| **Total** | **5 pts** | **5 pts** | — | — | ✅ |

## Vérification des réponses QCM/Association (correction_p1.jpg)

| Question | Réponse image | JSON | Statut |
|---|---|---|---|
| II.1 | b | b | ✅ |
| II.2 | a | a | ✅ |
| II.3 | c | c | ✅ |
| II.4 | c | c | ✅ |
| III | (1,c)(2,a)(3,e)(4,b) | (1,c)(2,a)(3,e)(4,b) | ✅ |

## Vérification des assets (crops de documents)

| Asset | Référencé par | Statut |
|---|---|---|
| doc1p2.png | doc_e1_1 | ✅ |
| doc2p2.png | doc_e1_2 | ✅ |
| doc3p3.png | doc_e1_3 | ✅ |
| doc4p3.png | doc_e1_4 | ✅ |
| doc1p4.png | doc_e2_1 | ✅ |
| doc2p4.png | doc_e2_2 | ✅ |
| doc3p5.png | doc_e2_3 | ✅ |
| doc1p5.png | doc_e3_1 | ✅ |
| doc2p6.png | doc_e3_2 | ✅ |
| doc3p6.png | doc_e3_3 | ✅ |

## Conclusion

**Qualité globale** : 🟢 EXCELLENT

- **Contenu** : 17/17 questions présentes, contenu conforme aux images
- **Points** : sommation réelle correcte (20 pts), mais le JSON a un défaut mineur : la question `I` (parent) n'a pas `"points": 2` → fausse la vérification automatique de `verify_exam.py`
- **Documents** : 10/10 assets référencés correctement
- **Réponses** : toutes les corrections QCM et association sont correctes

### Correction recommandée (1 seule)

Ajouter le champ `"points": 2` à la question I pour que la somme des parties soit correctement calculée par `verify_exam.py`.
