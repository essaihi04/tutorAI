# Rapport de vérification visuelle — SVT 2025 Normale

**Méthode** : lecture directe des images `pages/sujet_p{1..6}.jpg` et `pages/correction_p{1..6}.jpg`, puis comparaison avec `exam.json` (491 lignes).

**Résultat global** : barèmes et corrections conformes. **1 problème majeur** (titres de documents Ex1 désalignés avec l'image) + **2 problèmes** (contextes Ex2 et Ex3 incomplets).

---

## 1. Partie I — Restitution des connaissances (5 pts) ✓

### 1.1 Question I (2 pts) — QCM ✓ **EXEMPLAIRE**

Structure `type: "qcm"` avec 4 `sub_questions`, chacune avec 4 `choices` complets.

| # | Thème | Corrigé (NR 34F p1) | JSON `correct_answer` | Verdict |
|---|---|---|---|---|
| 1 | Faille inverse | c. oblique + rapprochement | `c` | ✓ |
| 2 | Métamorphisme de contact | a. haute T + basse P | `a` | ✓ |
| 3 | Magma zones subduction | c. péridotite hydratée plaque chevauchante | `c` | ✓ |
| 4 | Anatexie collision | d. magma granitique | `d` | ✓ |

### 1.2 Question II (1 pt) — Questions ouvertes ✓

- **II.a** (0.5 pt) Caractéristiques géophysiques zones subduction → correction `Anomalies thermiques` + `Plan de Bénioff` ✓
- **II.b** (0.5 pt) Définition faciès métamorphique → correction alignée ✓

🟠 **Mineur** : II.a et II.b sont deux objets `question` séparés au lieu d'une question avec sub_questions. Fonctionnellement OK.

### 1.3 Question III (1 pt) — V/F ✓

| # | Image | Corrigé | JSON | Verdict |
|---|---|---|---|---|
| a | Nappes charriage + forces extensives | Faux | `faux` | ✓ |
| b | Auréole métamorphisme thermique | Vrai | `vrai` | ✓ |
| c | Obduction = enfouissement océanique | Faux | `faux` | ✓ |
| d | Foliation = métamorphisme fort | Vrai | `vrai` | ✓ |

### 1.4 Question IV (1 pt) — Association ✓

`items_right` contient les 5 textes complets (pas que les lettres) ✓.

| Élément A | Effet attendu (B) | JSON | Verdict |
|---|---|---|---|
| 1. Éclogite | d. Roche métamorphique profondeur haute P | `(1,d)` | ✓ |
| 2. Granodiorite | c. Roche magmatique plutonique croûte continentale | `(2,c)` | ✓ |
| 3. Andésite | e. Roche magmatique volcanique zone subduction | `(3,e)` | ✓ |
| 4. Schiste | a. Roche métamorphique pressions et températures faibles | `(4,a)` | ✓ |

🟠 **Mineur** : questions I à IV n'ont pas de champ `number` (contrairement à 2023-normale/2024). Le préfixe est dans `content` seulement.

---

## 2. Deuxième partie — Raisonnement scientifique (15 pts)

### 2.1 Exercice 1 — Chou puant / thermogénèse (5 pts) 🔴 **TITRES DE DOCUMENTS DÉCALÉS**

**Structure** :

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1.a Décrire O₂ + déduire effet KCN | p2 | 1.5 | ✓ |
| Q1.b Hypothèse effet KCN en B | p2 | 0.5 | ✓ |
| Q2 Différences phosphorylation oxydative | p3 | 1.5 | ✓ |
| Q3 Mécanisme chaleur + vérifier hypothèse | p3 | 1.5 | ✓ |

**Somme : 1.5 + 0.5 + 1.5 + 1.5 = 5 pts ✓**

🔴 **Problème majeur — Documents désalignés** :

| JSON ID | Titre JSON | `src` | Description JSON | Réalité image |
|---|---|---|---|---|
| `doc_e1_1` | « Document 1 » | `doc2p2.png` | 2 graphiques O₂ suspensions A/B | = **Document 2** de l'image (p2) |
| `doc_e1_2` | « Document 2 » | `doc3p3.png` | schémas chaîne transport électrons + AOX | = **Document 3** de l'image (p3) |
| `doc_e1_3` | « Document 3 » | `doc1p2.png` | schéma fleur chou puant | = **Document 1** de l'image (p2) |

**Conséquences** :
- Contexte JSON dit « Les figures a et b du document 2 présentent les résultats » → vrai dans l'image, mais JSON pointe vers `doc_e1_1` (titré « Document 1 ») pour ces graphiques.
- Q1 JSON référence `doc_e1_1` avec titre « Document 1 » mais l'énoncé Q1 parle des « données du document 2 ».
- Q2 JSON référence `doc_e1_2` avec titre « Document 2 » mais l'énoncé Q2 parle du « document 3 ».
- Q3 JSON référence `doc_e1_3, doc_e1_1, doc_e1_2` → cycles mélangés.

**Action requise** : réaligner les titres avec les `src` (qui eux sont corrects) :
- `doc_e1_1` (src `doc2p2.png`) → titre **« Document 2 »**
- `doc_e1_2` (src `doc3p3.png`) → titre **« Document 3 »**
- `doc_e1_3` (src `doc1p2.png`) → titre **« Document 1 »**

### 2.2 Exercice 2 — ALD + Cobayes (5 pts) 🔴 **CONTEXTE INCOMPLET**

**Structure** :

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Relation protéine-caractère | p3 | 0.75 | ✓ |
| Q2 ARNm + aa + origine génétique | p4 | 1.75 | ✓ |
| Q3 Allèles dominants (1ᵉʳ croisement) | p4 | 0.5 | ✓ |
| Q4 Indépendance gènes (2ᵉ croisement) | p4 | 0.5 | ✓ |
| Q5 Échiquier 2ᵉ croisement | p5 | 1.5 | ✓ |

**Somme : 0.75 + 1.75 + 0.5 + 0.5 + 1.5 = 5 pts ✓**

**Documents** : 4 docs image (ALDP ; fragment gène ABCD1 ; code génétique ; cobayes F₁) → 4 docs JSON `doc_e2_1..4` ✓ titres alignés ✓ descriptions fidèles ✓.

🔴 **Problème — Contexte incomplet** :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2025-normale/exam.json:386
          "context": "...\nI. L'adrénoleucodystrophie (ALD)...\n- Donnée 1 : L'ALDP est une protéine..."
```

**Manque** :
1. **Donnée 2** (p4 haut) : « La protéine ALDP est codée par le gène ABCD1 qui existe sous deux formes alléliques : un allèle normal qui code pour une ALDP fonctionnelle et un allèle muté qui code pour une ALDP non fonctionnelle. Le document 2 présente un fragment du brin non transcrit de chacun des deux allèles du gène ABCD1 et le document 3 présente le tableau du code génétique. »
2. **Partie II + Donnée sur cobayes** (p4 bas) : « II. Dans le cadre de l'étude de la transmission de deux caractères héréditaires non liés au sexe chez le cobaye : la couleur du pelage et son aspect, on réalise les croisements suivants... »
3. **Croisement 1** : ♂ gris lisse × ♀ blanc rude → F₁ gris lisse.
4. **Croisement 2** : ♂F₁ × ♀F₁ → F₂ (80 gris lisse ; 25 gris rude ; 26 blanc lisse ; 9 blanc rude).

**Action requise** : enrichir `context` de l'Exercice 2 avec Donnée 2, section II, et les deux croisements.

### 2.3 Exercice 3 — Pollution eaux puits Triffa (5 pts) 🟠 **CONTEXTE PARTIEL**

**Structure** :

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Relation engrais azotés-santé | p5 | 1.5 | ✓ |
| Q2 Impact fosses septiques | p6 | 1 | ✓ |
| Q3.a Comparer paramètres STEP | p6 | 1.5 | ✓ |
| Q3.b Eaux STEP non réutilisables | p6 | 0.5 | ✓ |
| Q4 Mesures préservation | p6 | 0.5 | ✓ |

**Somme : 1.5 + 1 + 1.5 + 0.5 + 0.5 = 5 pts ✓**

**Documents** : 4 docs image → 4 docs JSON ✓ titres et descriptions alignés ✓.

🟠 **Problème — Contexte incomplet** :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2025-normale/exam.json:486
          "context": "...Donnée 1 : Dans certaines zones rurales... Méthémoglobinémie... 8,6% décédées...\n\n## Document 2"
```

Le contexte se termine par `## Document 2` sans inclure :
1. **Donnée 2** (p5 bas) : « Une étude publiée en 2019 a montré que 81% de la population de la commune de Madagh, située au centre de la plaine de Triffa, utilise les fosses septiques à cause de la faible couverture par le réseau d'assainissement. Le document 3 présente les résultats d'une étude bactériologique... »
2. **Donnée 3** (p6) : « Le Maroc a mis en place les stations d'épuration des eaux usées (STEP) pour réduire l'impact de la pollution par les eaux usées et leur réutilisation possible dans l'irrigation. Le document 4 présente les résultats de la mesure de certains paramètres à l'entrée et à la sortie d'une STEP dans la région orientale du Maroc. »

**Action requise** : ajouter Donnée 2 et Donnée 3 dans `context` de l'Exercice 3 ; supprimer le « ## Document 2 » résiduel.

---

## 3. Totaux

| Partie | Somme questions | Déclaré | Verdict |
|---|---|---|---|
| Partie I | 2 + 0.5 + 0.5 + 1 + 1 = **5** | 5 | ✓ |
| Exercice 1 | 1.5 + 0.5 + 1.5 + 1.5 = **5** | 5 | ✓ |
| Exercice 2 | 0.75 + 1.75 + 0.5 + 0.5 + 1.5 = **5** | 5 | ✓ |
| Exercice 3 | 1.5 + 1 + 1.5 + 0.5 + 0.5 = **5** | 5 | ✓ |
| **Total** | **20** | 20 | ✓ |

---

## 4. Résumé des actions

| Priorité | Localisation | Action |
|---|---|---|
| 🔴 Haute | Exercice 1 / `documents` | Réaligner les titres : `doc_e1_1` → "Document 2", `doc_e1_2` → "Document 3", `doc_e1_3` → "Document 1" |
| 🔴 Haute | Exercice 2 / `context` | Ajouter Donnée 2 (gène ABCD1) + Section II (cobayes) + Croisement 1 + Croisement 2 |
| 🟠 Moyenne | Exercice 3 / `context` | Ajouter Donnée 2 (Madagh) + Donnée 3 (STEP) ; nettoyer `## Document 2` résiduel |
| 🟠 Mineure | Partie I I-IV | Ajouter champ `number` explicite |
| 🟢 — | Partie I QCM/Association | Structure exemplaire (choices complets, items_right texte intégral) |

**Points forts** : Partie I remarquablement bien structurée ; barèmes parfaits ; corrections conformes au NR 34F.
**Points faibles** : Exercice 1 titres désalignés (impact sur la lecture des questions) ; contextes des Exercices 2 et 3 tronqués.
