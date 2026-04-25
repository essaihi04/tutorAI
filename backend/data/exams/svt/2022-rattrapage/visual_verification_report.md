# Rapport de vérification VISUELLE — 2022-rattrapage

**Titre** : Examen National du Baccalauréat - SVT 2022 Rattrapage
**Pages sujet** : 5 | **Pages correction** : 4
**Documents** : 10 | **Questions JSON** : 17

## Structure vs images

### Partie I : Restitution des connaissances (5 pts) — Pages 1-2

| Élément image | Points image | JSON | Statut |
|---|---|---|---|
| I. Définissez : Prisme d'accrétion - Métamorphisme | 1pt | 1pt | ✅ |
| II.1 Le Gneiss (QCM a/b/c/d) | 0.5pt | 0.5pt → d | ✅ |
| II.2 Séquence métamorphique argile (QCM) | 0.5pt | 0.5pt → c | ✅ |
| II.3 Faille inverse (QCM) | 0.5pt | 0.5pt → a | ✅ |
| II.4 Refroidissement magma subduction (QCM) | 0.5pt | 0.5pt → c | ✅ |
| III Association Ens1(4)×Ens2(5) | 1pt | 1pt → (1,c)(2,a)(3,d)(4,b) | ✅ |
| IV Coupe ophiolite 1,2,3,4 (doc) | 1pt | 1pt → (1,a)(2,b)(3,c)(4,d) | ✅ |
| **Total Partie I** | **5 pts** | **5 pts** | ✅ |

### Partie II : Raisonnement scientifique (15 pts)

#### Exercice 1 (5 pts) — Pages 2-3 : Myopathie et voies métaboliques
| Question | Points image | JSON | Docs visibles | Docs JSON | Statut |
|---|---|---|---|---|---|
| Q1a hypothèse intolérance | 0.75 | 0.75 | D1 | doc_e1_1 (doc1p2) | ✅ |
| Q1b tableau voies anaérobie/aérobie | 0.75 | 0.75 | D1 | doc_e1_1 | ✅ |
| Q2a concentrations glycogène | 0.5 | 0.5 | D2 | doc_e1_2 (doc2p2) | ✅ |
| Q2b variations lactate | 0.5 | 0.5 | D2 | doc_e1_2 | ✅ |
| Q3 voie non fonctionnelle | 1 | 1 | D1, D2 | doc_e1_1, doc_e1_2 | ✅ |
| Q4 Myophosphorylase (doc 3) | 0.5 | 0.5 | D3 | doc_e1_3 (doc3p3) | ✅ |
| Q5 origine intolérance + vérif | 1 | 1 | D1, D2, D3 | doc_e1_1,2,3 | ✅ |
| **Total** | **5 pts** | **5 pts** | — | — | ✅ |

#### Exercice 2 (5 pts) — Pages 3-4 : Mélanine MCR1 + Génétique souris
| Question | Points image | JSON | Docs visibles | Docs JSON | Statut |
|---|---|---|---|---|---|
| Q1 relation caractère-protéine | 1 | 1 | D1 | doc_e2_1 (doc1p3) | ✅ |
| Q2 séquences ARNm + origine génétique | 1.5 | 1.5 | D2, D3 | doc_e2_2 (doc2p4), doc_e2_3 (doc3p4) | ✅ |
| Q3 déduction croisement 1 | 0.75 | 0.75 | — | — | ✅ |
| Q4 gènes liés/indépendants | 0.5 | 0.5 | — | — | ✅ |
| Q5 interprétation croisement 2 + échiquier | 1.25 | 1.25 | — | — | ✅ |
| **Total** | **5 pts** | **5 pts** | — | — | ✅ |

#### Exercice 3 (5 pts) — Pages 4-5 : Lixiviats et pollution
| Question | Points image | JSON | Docs visibles | Docs JSON | Statut |
|---|---|---|---|---|---|
| Q1a évolution DBO5/DCO/O2 + qualité | 1.5 | 1.5 | D1 (fig a,b,c) | doc_e3_1 (doc1p5) | ✅ |
| Q1b différence concentration O2 | 1 | 1 | D1 | doc_e3_1 | ✅ |
| Q2 comparaison métaux lourds + composition | 1.5 | 1.5 | D2, D3 | doc_e3_2 (doc2p5), doc_e3_3 (doc3p5) | ✅ |
| Q3 deux procédures | 1 | 1 | — | — | ✅ |
| **Total** | **5 pts** | **5 pts** | — | — | ✅ |

## Vérification des réponses QCM/Association (correction_p1.jpg)

| Question | Réponse image | JSON | Statut |
|---|---|---|---|
| II.1 | d | d | ✅ |
| II.2 | c | c | ✅ |
| II.3 | a | a | ✅ |
| II.4 | c | c | ✅ |
| III | (1,c)(2,a)(3,d)(4,b) | (1,c)(2,a)(3,d)(4,b) | ✅ |
| IV | (1,a)(2,b)(3,c)(4,d) | (1,a)(2,b)(3,c)(4,d) | ✅ |

## ⚠ Problèmes détectés

### 🔴 Problème majeur (1)

**`doc_g3` (coupe ophiolite) : description COMPLÈTEMENT FAUSSE**

Le JSON contient :
```json
"id": "doc_g3",
"title": "Document (coupe ophiolite)",
"description": "Ce document est un schéma représentant la structure d'un **tissu végétal**. Il montre quatre couches distinctes : l'épiderme (1), le parenchyme chlorophyllien (2), le parenchyme de réserve (3) et le parenchyme aérifère (4)."
```

**Mais l'image p2 montre clairement une coupe d'un complexe ophiolitique** avec :
1 → Basalte en coussinets (pillow lavas)
2 → Filons de Dolérite
3 → Gabbro
4 → Péridotite

→ La description Pixtral Vision a complètement halluciné un schéma végétal.
→ Impact : la description est utilisée par le RAG et pour les questions IA → risque d'induire en erreur.

### 🟡 Problèmes mineurs (2)

1. **Nommage non-standard de l'asset** : `doc22p2.png` devrait être `doc4p2.png` (convention `docXpY.png` = document X sur page Y). L'irrégularité est compensée par le `src` dans le JSON, mais casse la convention de nommage du projet.

2. **Q1 et Q2 Exercice 1 : structure redondante** — points déclarés à la fois sur la question parent ET sur les sub_questions. Somme correcte (1.5 + 1.0) mais risque de double comptage selon le consommateur du JSON.

## Conclusion

**Qualité globale** : 🟡 BON avec 1 correction URGENTE

- **Contenu** : 17 questions, conformes aux images ✓
- **Points** : 20 pts total, sommation correcte ✓
- **Réponses** : toutes les corrections QCM/association sont exactes ✓
- **Documents** : 10/10 assets référencés, mais `doc_g3` a une **description halluciné** à corriger

### Correction à apporter

Remplacer la description de `doc_g3` par :
```
Ce document est un schéma représentant une coupe verticale schématique d'un complexe ophiolitique, structure typique d'une ancienne lithosphère océanique. Il montre quatre niveaux numérotés de haut en bas : (1) Basalte en coussinets (pillow lavas) en surface, (2) Filons de Dolérite formant un complexe filonien, (3) Gabbro à structure grenue constituant la croûte profonde, (4) Péridotite correspondant au manteau supérieur.
```
