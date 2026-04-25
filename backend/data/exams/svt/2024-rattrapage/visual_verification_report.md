# Rapport de vérification visuelle — SVT 2024 Rattrapage

**Méthode** : lecture directe des images `pages/sujet_p{1..6}.jpg` et `pages/correction_p{1..3}.jpg`, puis comparaison avec `exam.json` (484 lignes).

**Résultat global** : structure très bien faite pour Partie I (QCM, V/F, Association tous corrects). **1 bug critique** (barème Q3 Ex2) + **2 problèmes** (contextes manquants Ex1 et Ex2).

---

## 1. Partie I — Restitution des connaissances (5 pts)

### 1.1 Question I (1 pt) — Définition + déplacement H⁺ ✓

| Sous-question | Image | Corrigé (RR 34F) | JSON | Verdict |
|---|---|---|---|---|
| 1. Définir fermentation lactique | p1 | 0.5 pt | `points: 0.5` | ✓ |
| 2.a H⁺ chaîne respiratoire | p1 | 0.25 pt | `points: 0.25` | ✓ |
| 2.b H⁺ sphère pédonculée | p1 | 0.25 pt | `points: 0.25` | ✓ |

**Somme : 0.5 + 0.25 + 0.25 = 1 pt ✓** — Structure hiérarchique parfaite.

### 1.2 Question II (2 pts) — QCM ✓ **EXEMPLAIRE**

JSON utilise `type: "qcm"` avec 4 `sub_questions`, chacune avec 4 `choices` complets + `correct_answer`. C'est le format **correct** (contrairement à 2023-rattrapage et 2024-normale).

| # | Question image | Corrigé | JSON `correct_answer` | Verdict |
|---|---|---|---|---|
| 1 | Crossing-over lors de | a. prophase I | `a` | ✓ |
| 2 | Chromosomes en G₁ | b. monochromatidien non condensé | `b` | ✓ |
| 3 | Méiose → | a. 4 haploïdes monochromatidiens | `a` | ✓ |
| 4 | Fin de phase S | a. bichromatidiens sans yeux de réplication | `a` | ✓ |

**Somme : 4 × 0.5 = 2 pts ✓**

### 1.3 Question III (1 pt) — V/F ✓

| # | Image | Corrigé | JSON | Verdict |
|---|---|---|---|---|
| 1 | Effet serre par absorption UV | Faux | `faux` | ✓ |
| 2 | Ordures Maroc humides + organiques | Vrai | `vrai` | ✓ |
| 3 | Incinération réduit volume + électricité | Vrai | `vrai` | ✓ |
| 4 | ENR = gaz naturel, pétrole, charbon | Faux | `faux` | ✓ |

### 1.4 Question IV (1 pt) — Association ✓

**Image** (p2) : Ensemble 1 (4 actions) × Ensemble 2 (5 effets a-e).

JSON `items_left` et `items_right` contiennent bien les **textes complets** (pas seulement lettres) — ✓ structure recommandée.

| Action | Effet attendu | JSON `correct_pairs` | Verdict |
|---|---|---|---|
| 1. Fixation Ca²⁺ troponine | d. Libération sites myosine | `(1,d)` | ✓ |
| 2. Hydrolyse ATP | a. Énergie rotation têtes myosine | `(2,a)` | ✓ |
| 3. Fixation ATP têtes myosine | e. Séparation myofilaments | `(3,e)` | ✓ |
| 4. Hydrolyse phosphocréatine | b. Régénération rapide ATP | `(4,b)` | ✓ |

---

## 2. Deuxième partie — Raisonnement scientifique (15 pts)

### 2.1 Exercice 1 — Endurance sportive (5 pts) 🟠 **CONTEXTE MANQUANT**

**Structure** :

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Comparer VMA/O₂/lactate + hypothèse | p2 | 1.25 | ✓ |
| Q2 Relation entraînement-voie métabolique | p3 | 1.5 | ✓ |
| Q3 Effet sur vitesse production ATP | p3 | 1.25 | ✓ |
| Q4 Effet sur amélioration endurance | p3 | 1 | ✓ |

**Somme : 1.25 + 1.5 + 1.25 + 1 = 5 pts ✓**

**Documents** : 5 docs image (VMA, fibres I/II, caractéristiques, enzymes+ATP, voies métaboliques) → 5 docs JSON `doc_e1_1..5` ✓ descriptions fidèles ✓.

🟠 **Mineur** :
1. Nom `"Exercice I"` (chiffre romain) tandis que les autres utilisent `"Exercice 2"`, `"Exercice 3"` (chiffres arabes) → incohérence à uniformiser.
2. **Pas de champ `context`** dans l'objet exercice — pourtant l'image p2 contient 2 paragraphes d'introduction + Donnée 1 :

> L'endurance est définie comme la capacité d'un sportif à résister à la fatigue et à maintenir un effort physique prolongé. L'entraînement joue un rôle important dans l'amélioration de l'endurance des athlètes de longues distances en favorisant certaines voies métaboliques de production d'énergie dans les muscles. Afin d'étudier l'effet de l'entraînement sur l'amélioration de l'endurance chez les athlètes de longues distances, on propose les données suivantes :
>
> Donnée 1 : Le test d'endurance permet le calcul de la Vitesse Maximale Aérobie (VMA exprimée en Km/h) qui correspond à la vitesse de course à partir de laquelle la consommation du dioxygène est maximale...

**Action requise** : ajouter un champ `context` avec ce texte + Donnée 2 (fibres type I/II) + Donnée 3 (enzymes + voies métaboliques).

### 2.2 Exercice 2 — DLFT + Génétique souris (6 pts) 🔴 **BARÈME Q3 INCORRECT + CONTEXTE VIDE**

**Structure image** :

| Question | Image | Points image | JSON points | Verdict |
|---|---|---|---|---|
| Q1 Progranuline + taux plasmatique | p4 | 0.75 | 0.75 | ✓ |
| Q2 Origine génétique DLFT | p4 | 1.25 | 1.25 | ✓ |
| **Q3.a Dominance + génotypes + justification** | **p5** | **1.5** | *(pas spécifié sur sous-question)* | 🔴 |
| **Q3.b Échiquier de croisement** | **p5** | **1.5** | *(pas spécifié sur sous-question)* | 🔴 |
| **Q3 TOTAL** | — | **3** | **1.5** | 🔴 **BUG** |
| Q4 Croisement 2 + 3ᵉ loi Mendel | p5 | 1 | 1 | ✓ |

🔴 **Bug critique** :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2024-rattrapage/exam.json:366-386
            {
              "number": "3",
              "content": "Selon l'hypothèse des chercheurs et à partir des résultats du croisement 1 :\na. Déterminer...\nb. Expliquer...",
              "points": 1.5,
              "type": "open",
              "sub_questions": [
                {
                  "letter": "a",
                  "content": "Déterminer le type de dominance...",
                  "correction": { ... }
                },
                {
                  "letter": "b",
                  "content": "Expliquer les résultats...",
                  "correction": { ... }
                }
              ]
            },
```

**Problèmes** :
- Q3 déclaré `points: 1.5` mais devrait être **3** (= 1.5 + 1.5).
- Les sub_questions `a` et `b` n'ont **pas** de champ `points` (devrait être `1.5` chacune d'après l'image).

**Conséquence** : Somme Ex2 = 0.75 + 1.25 + **1.5** + 1 = **4.5** au lieu de **6**. Le total `"points": 6` de l'exercice devient incohérent avec la somme des questions.

**Action requise** :
```json
{
  "number": "3",
  "points": 3,
  "sub_questions": [
    { "letter": "a", "points": 1.5, ... },
    { "letter": "b", "points": 1.5, ... }
  ]
}
```

🔴 **Problème 2** — **Contexte quasi vide** :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2024-rattrapage/exam.json:413
          "context": "Afin d'étudier les mécanismes de l'expression de l'information génétique et de la transmission de certains caractères héréditaires, on propose l'exploitation des données suivantes :"
```

**Manque totalement** :
- **Partie I : DLFT** (p3 bas → p4) : « La dégénérescence lobaire fronto-temporale (DLFT) est une maladie neurodégénérative... une protéine nommée Progranuline codée par le gène PRG dans le tissu nerveux du cortex cérébral... »
- **Partie II : Génétique souris** (p5) : « Pour comprendre le mode de transmission de deux caractères héréditaires non liés au sexe chez les souris : la couleur du corps (jaune ou gris) et la longueur des poils (courts ou longs)... »
- **Croisement 1** (tableau Parents/F₁) : « Souris femelles jaunes à poils courts × Souris mâles jaunes à poils longs → 102 souris jaunes à poils longs, 49 souris grises à poils longs »
- **Croisement 2** (tableau Parents/F'₂) : « Souris femelles jaunes à poils longs F₁ × Souris mâles grises à poils courts → 110+114+114+114 répartition 4 phénotypes »

**Action requise** : enrichir considérablement `context` avec tous ces éléments.

**Documents** : Document 1 (progranuline) + Document 2 (gène PRG) = 2 docs image → `doc_e2_1`, `doc_e2_2` JSON ✓ descriptions fidèles ✓.

### 2.3 Exercice 3 — Pollution margines (4 pts) ✓

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Eutrophisation + explication périodes 2, 4 | p6 | 1.5 | ✓ |
| Q2 Comparer réactifs + impact coût | p6 | 1.5 | ✓ |
| Q3 Importance traitement environnement + économie | p6 | 1 | ✓ |

**Somme : 1.5 + 1.5 + 1 = 4 pts ✓**

**Documents** : 3 docs image (Sahla + eutrophisation ; réactifs M'kansa ; électrocoagulation) → `doc_e3_1..3` JSON ✓ descriptions fidèles ✓.

**Contexte** : présent, complet (Donnée 1 inclus). ✓

---

## 3. Totaux

| Partie | Somme questions | Déclaré | Verdict |
|---|---|---|---|
| Partie I | 1 + 2 + 1 + 1 = **5** | 5 | ✓ |
| Exercice 1 | 1.25 + 1.5 + 1.25 + 1 = **5** | 5 | ✓ |
| Exercice 2 (si Q3=3 corrigé) | 0.75 + 1.25 + **3** + 1 = **6** | 6 | 🔴 Actuellement Q3=1.5 → somme 4.5 ≠ 6 |
| Exercice 3 | 1.5 + 1.5 + 1 = **4** | 4 | ✓ |
| **Total attendu** | **20** | 20 | ✓ |

---

## 4. Résumé des actions

| Priorité | Localisation | Action |
|---|---|---|
| 🔴 Critique | Exercice 2 / Q3 | `points: 1.5` → `points: 3` + ajouter `points: 1.5` à chaque `sub_question` a et b |
| 🔴 Haute | Exercice 2 / `context` | Remplir le contexte (introduction DLFT + partie II souris + données des deux croisements) |
| 🟠 Moyenne | Exercice 1 / `context` | Ajouter champ `context` avec introduction endurance + Donnée 1 VMA + Donnée 2 fibres + Donnée 3 enzymes |
| 🟠 Moyenne | Exercice 1 / `name` | Renommer `"Exercice I"` → `"Exercice 1"` (cohérence avec Ex2, Ex3) |
| 🟢 — | Partie I | Déjà exemplaire (QCM bien structuré, V/F correct, Association avec textes complets) |

**Points forts** : Partie I très bien structurée (QCM avec `choices` complets, Association avec `items_right` texte intégral) ; contenu textuel des corrections fidèle au RR 34F.
**Points faibles** : Barème Q3 d'Exercice 2 incorrect (ABSENT = 1.5 au lieu de 3) ; contextes d'Exercices 1 et 2 largement incomplets.
