# Rapport de vérification visuelle — SVT 2024 Normale

**Méthode** : lecture directe des images `pages/sujet_p{1..6}.jpg` et `pages/correction_p{1..2}.jpg`, puis comparaison avec `exam.json` (376 lignes).

**Résultat global** : contenus textuels et barèmes globalement conformes. **1 problème majeur** (contexte Exercice 2 incomplet) + **2 problèmes structurels** (QCM Partie I et items_right par lettre au lieu de texte).

---

## 1. Partie I — Restitution des connaissances (5 pts)

### 1.1 Question I (1 pt) — Définitions ✓

| # | Image (sujet p1) | Corrigé (NR 34F p1) | JSON | Verdict |
|---|---|---|---|---|
| 1 | Décomposition aérobie déchets organiques → fertilisants | Compostage | ✓ | ✓ |
| 2 | Séparer ordures selon nature | Tri | ✓ | ✓ |
| 3 | Décomposition anaérobie → biogaz | Méthanisation | ✓ | ✓ |
| 4 | Rétention IR par gaz atmosphère | Effet de serre | ✓ | ✓ |

🟠 **Mineur** : les 4 définitions ne sont pas décomposées en `sub_questions` avec `points=0.25` chacune. Cela rend l'autocorrection granulaire moins précise. Le corrigé officiel attribue 0.25×4.

### 1.2 Question II (2 pts) — QCM 🟠 **STRUCTURE**

**Image** (p1) : 4 propositions avec 4 choix a-d chacune. Thèmes : dégradation glucose, glycolyse, fermentations, contraction musculaire.
**Corrigé officiel** : `(1,a); (2,a); (3,c); (4,a)`.
**JSON** : `type: "association"` avec `items_right: ["a","b","c","d"]` — les choix ne sont **que des lettres**, pas leur texte.

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2024-normale/exam.json:26-38
          "type": "association",
          "items_left": [
            "1",
            "2",
            "3",
            "4"
          ],
          "items_right": [
            "a",
            "b",
            "c",
            "d"
          ],
```

Les énoncés complets des 16 choix se trouvent dans `content` (multiligne), ce qui permet de lire la question. Mais l'interface d'autocorrection ne peut pas présenter les choix comme QCM. Idéalement : restructurer en `type: "qcm"` avec 4 `sub_questions` ayant chacune 4 `choices` + `correct_answer`.

### 1.3 Question III (1 pt) — V/F ✓

| # | Image | Corrigé | JSON | Verdict |
|---|---|---|---|---|
| a | Méiose → 4 cellules filles identiques | Faux | `faux` | ✓ |
| b | Réplication ADN en phase S | Vrai | `vrai` | ✓ |
| c | Division équationnelle précédée par réplication | Faux | `faux` | ✓ |
| d | ARN polymérase → traduction ARNm | Faux | `faux` | ✓ |

### 1.4 Question IV (1 pt) — Association 🟠 **STRUCTURE**

**Image** (p1) : Ensemble A (1-4) associé à Ensemble B (a-e). Corrigé : `(1,e); (2,d); (3,a); (4,b)` — JSON match ✓.

🟠 **Mineur** : `items_right` contient seulement les lettres `["a", "b", "c", "d", "e"]` au lieu du texte des propositions. Les textes sont présents dans `content` (multiligne) mais pas séparés.

**Action suggérée** :
```json
"items_right": [
  "Complexe formé par l'association Histones –ADN.",
  "Complexe moléculaire participant à la synthèse des protéines.",
  "Complexe protéique assurant la synthèse de l'ARNm.",
  "Structure reliant les deux chromatides du même chromosome.",
  "Enzyme qui intervient dans la réplication de l'ADN."
]
```

---

## 2. Deuxième partie — Raisonnement scientifique (15 pts)

### 2.1 Exercice 1 — Obésité / souris Cox6A (5 pts) ✓

| Question | Image | JSON points | Verdict |
|---|---|---|---|
| Q1 Comparer WT vs Cox6A + hypothèse | p2 | 1.5 | ✓ |
| Q2 Différences UCP + déduction | p3 | 1 | ✓ |
| Q3 Expliquer relation + vérifier hypothèse | p3 | 2 | ✓ |
| Q4 Proposer solution | p3 | 0.5 | ✓ |

**Somme : 1.5 + 1 + 2 + 0.5 = 5 pts ✓** — match parfait avec corrigé NR 34F.

**Documents** : 4 docs image (Document 1 poids, Document 2 activité enzymatique, Document 3 température+UCP, Document 4 chaîne respiratoire+UCP) → JSON `doc_e1_1..4` titres alignés ✓ descriptions fidèles ✓.

### 2.2 Exercice 2 — Amélogénine + Drosophile (6 pts) 🔴 **CONTEXTE INCOMPLET**

**Structure** : 2 parties (I. Amélogénèse + II. Drosophile) mais JSON context ne contient que la partie I.

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2024-normale/exam.json:290
          "context": "Dans le cadre de l'étude des mécanismes de l'expression de l'information génétique et de la transmission de certains caractères héréditaires, on propose l'exploitation des données suivantes :\n\nI. L'émail dentaire est un tissu minéralisé dur...\n\n- Donnée 1 : Le document 1 représente la relation entre l'amélogénine et l'état de l'émail dentaire..."
```

🔴 **Problème** : la section **II. Drosophile** et les **deux croisements** (pages 4-5 du sujet) sont **TOTALEMENT ABSENTS** du contexte JSON. Les questions Q3 et Q4 portent sur ces croisements !

**Textes manquants** (sujet p4 bas + p5) :

> **II.** Pour comprendre le mode de transmission de deux caractères héréditaires chez la drosophile : la couleur du corps et l'aspect des nervures des ailes. On propose l'exploitation des résultats des croisements suivants :
>
> **Premier croisement** : entre des femelles de race pure à corps gris et aux ailes avec nervures transversales et des mâles de race pure à corps jaune et aux ailes sans nervures transversales. La génération F₁ obtenue est composée d'individus à corps gris et aux ailes avec nervures transversales.
>
> **Deuxième croisement** : entre des femelles de race pure à corps jaune et aux ailes sans nervures transversales et des mâles de race pure à corps gris et aux ailes avec nervures transversales. La génération F₁ obtenue est composée de femelles à corps gris et aux ailes avec nervures transversales et de mâles à corps jaune et aux ailes sans nervures transversales.

**Action requise** : ajouter cette partie II + les deux croisements dans `context` de l'Exercice 2.

**Structure des questions** :

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Relation protéine-caractère | p4 | 1 | ✓ |
| Q2 ARNm + aa + origine génétique | p4 | 2 | ✓ |
| Q3 Mode de transmission + justification | p5 | 1.5 | ✓ |
| Q4 Résultats attendus F₁×F₁ (distance 13.4 cM) | p5 | 1.5 | ✓ |

**Somme : 1 + 2 + 1.5 + 1.5 = 6 pts ✓**

**Documents** : Document 1 (amélogénèse), Document 2 (fragments triplets), Document 3 (code génétique) = 3 docs image → `doc_e2_1..3` JSON ✓ descriptions fidèles ✓.

**Correction Q2 vérifiée** : Mutation C→T en position 2 du 3ème triplet → ARNm CCC→CUC → Pro→Leu ✓ (conforme NR 34F p2).

### 2.3 Exercice 3 — Réchauffement climatique / CO₂ (4 pts) ✓

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Différence émissions/absorption + problème | p5 | 0.75 | ✓ |
| Q2 Lieu final stockage CO₂ | p6 | 1 | ✓ |
| Q3 Expliquer variation | p6 | 1 | ✓ |
| Q4 Différence scénarios + captage artificiel | p6 | 1.25 | ✓ |

**Somme : 0.75 + 1 + 1 + 1.25 = 4 pts ✓**

**Documents** : 4 docs image (Document 1 émissions+absorption, Document 2 cycle carbone+réservoirs, Document 3 température+dissolution, Document 4 scénarios GIEC) → `doc_e3_1..4` JSON ✓ descriptions fidèles ✓.

---

## 3. Totaux

| Partie | Somme questions | Déclaré | Verdict |
|---|---|---|---|
| Partie I | 1 + 2 + 1 + 1 = **5** | 5 | ✓ |
| Exercice 1 | 1.5 + 1 + 2 + 0.5 = **5** | 5 | ✓ |
| Exercice 2 | 1 + 2 + 1.5 + 1.5 = **6** | 6 | ✓ |
| Exercice 3 | 0.75 + 1 + 1 + 1.25 = **4** | 4 | ✓ |
| **Total** | **20** | 20 | ✓ |

---

## 4. Résumé des actions

| Priorité | Localisation | Action |
|---|---|---|
| 🔴 Haute | Exercice 2 / `context` | Ajouter la section **II. Drosophile** + les deux croisements (actuellement totalement absents) |
| 🟠 Moyenne | Partie I / Question II | Restructurer de `association` vers `qcm` avec 4 sub_questions + 4 choices chacune |
| 🟠 Moyenne | Partie I / Question IV | Remplacer `items_right: ["a".."e"]` par le texte complet des 5 propositions |
| 🟠 Moyenne | Partie I / Question I | Décomposer en 4 sub_questions avec `points=0.25` chacune |
| 🟢 Faible | — | Contenu textuel, descriptions des documents et corrections officielles conformes |

**Contenu textuel (énoncés, barèmes, réponses)** : fidèle aux images et au corrigé NR 34F.
**Contenu structurel** : 1 correction majeure (Ex2 context) + 3 améliorations structurelles recommandées.
