# Rapport de vérification visuelle — SVT 2023 Rattrapage

**Méthode** : lecture directe des images `pages/sujet_p{1..6}.jpg` et `pages/correction_p{1..2}.jpg`, puis comparaison avec `exam.json` (464 lignes).

**Résultat global** : **4 problèmes majeurs** identifiés (structure QCM, description hallucinée, documents manquants Ex2 & Ex4). Contenu textuel et barèmes corrects.

---

## 1. Partie I — Restitution des connaissances (5 pts)

### 1.1 Question I (1 pt) — Définitions
- **Image** (p1) : 2 définitions → (1) Glycolyse, (2) Sarcomère.
- **Corrigé officiel** (RR 34F p1) : `0.5 × 2`.
- **JSON** : 2 `sub_questions` `points=0.5` chacune → corrections `Glycolyse` et `Sarcomère`. ✓

### 1.2 Question II (1 pt) — Vrai/Faux
| # | Proposition image | Corrigé officiel | JSON | Verdict |
|---|---|---|---|---|
| 1 | CO₂ déchet minéral respiration + fermentation alcoolique | vrai | `vrai` | ✓ |
| 2 | Sphères pédonculées sur membrane **externe** | faux | `faux` | ✓ |
| 3 | Myogramme = dispositif | faux | `faux` | ✓ |
| 4 | Striation due aux myofilaments | vrai | `vrai` | ✓ |

### 1.3 Question III (2 pts) — QCM 🔴 **PROBLÈME STRUCTUREL**

**Image** (p1) : 4 propositions numérotées 1 à 4, chacune avec 4 choix `a/b/c/d` indépendants.
**Corrigé officiel** : `(1,c); (2,a); (3,d); (4,c)` — tous corrects dans le JSON.

**🔴 MAIS** la structure JSON est incorrecte :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2023-rattrapage/exam.json:79-104
          "type": "association",
          "items_left": [
            "1",
            "2",
            "3",
            "4"
          ],
          "items_right": [
            "lente permettant de régénérer l'ADP.",
            "lente permettant de régénérer la phosphocréatine.",
            "rapide permettant de régénérer l'ATP.",
            "rapide permettant de régénérer la phosphocréatine.",
            "de phosphorylation d'ADP.",
            ...
          ]
```

- `type: "association"` → devrait être `"qcm"` (comme dans 2023-normale).
- `items_right` aplatit 16 choix issus des 4 questions → **ambiguïté totale** : à quel `c` se rapporte `(1,c)` ? Le joueur ne peut pas interpréter les réponses.
- Devrait être structuré comme `sub_questions` avec chacun ses `choices` et son `correct_answer`, comme dans `svt/2023-normale/exam.json` question III.

**Action requise** : restructurer en QCM avec 4 `sub_questions`, chacune 4 `choices` + `correct_answer`.

### 1.4 Question IV (1 pt) — Schéma contraction musculaire 🟠 **CONTENU MAL RENSEIGNÉ**

**Image** (p1) : figure avec flèches 1, 2, 3 pointant vers filament d'actine et flèche 4 vers tête myosine.
**Corrigé officiel** : `1-Actine ; 2-troponine ; 3-Tropomyosine ; 4-Tête de myosine` — `0.25×4`.

**JSON** :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2023-rattrapage/exam.json:131-163
            {
              "number": "1",
              "content": "Filament d'actine",
              "correction": { "content": "Actine" }
            },
            {
              "number": "2",
              "content": "Filament de myosine",
              "correction": { "content": "troponine" }
            },
            {
              "number": "3",
              "content": "Filament de myosine",
              "correction": { "content": "Tropomyosine" }
            },
            {
              "number": "4",
              "content": "Filament de myosine",
              "correction": { "content": "Tête de myosine" }
            }
```

Le champ `content` ne décrit pas l'élément pointé, il répète « Filament de myosine » pour les items 2, 3, 4. Les corrections sont justes mais les libellés de question sont incohérents.

**Action requise** : remplacer les `content` par `"Élément n°X sur le schéma"` ou équivalent (ex. `"Élément pointé par la flèche 2"`).

---

## 2. Deuxième partie — Raisonnement scientifique (15 pts)

### 2.1 Exercice 1 — Xeroderma Pigmentosum (2.5 pts)

**Structure** : 3 questions Q1 (0.5) + Q2 (1.5) + Q3 (0.5) = 2.5 pts ✓

🟠 **Problème** : les questions n'ont **pas de champ `number`** (contrairement à 2023-normale). Cela brise la cohérence avec les autres examens et peut poser problème côté frontend.

🔴 **Problème** — **Description hallucinée** `doc_e1_2` :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2023-rattrapage/exam.json:222
              "description": "Ce document est composé de deux figures (a) et (b). La figure (a) montre une comparaison entre un fragment d'allèle normal et un fragment d'allèle anormal, avec une mutation ponctuelle à la position 2450, où un nucléotide T est remplacé par un G. La figure (b) présente un tableau des codons et des acides aminés correspondants, indiquant que la mutation entraîne un changement d'acide aminé de la cystéine (Cys) à un codon non-sens (UGA)."
```

**Réalité** (image p2 + corrigé officiel RR 34F p1) :
- Fragment normal `ACG-CTC-CTT-AAG-TTT-CTG` → ARNm `UGC GAG GAA UUC AAA GAC` → `Cys-Glu-Glu-Phe-Lys-Asp`
- Fragment anormal `ACG-CTC-CTT-AAG-GTT-CTG` → ARNm `UGC GAG GAA UUC CAA GAC` → `Cys-Glu-Glu-Phe-Gln-Asp`
- Mutation : `T → G` en position **2452** (corrigé officiel) du brin transcrit, aboutissant à **Lys → Gln** (pas un codon stop !).

**Action requise** : corriger la description pour dire « la mutation entraîne un changement d'acide aminé de la lysine (Lys) à la glutamine (Gln) » et non « Cys à un codon non-sens ».

### 2.2 Exercice 2 — Drosophile (2.5 pts) 🔴 **DOCUMENT MANQUANT**

**Structure** : Q1 (0.75) + Q2.a (0.75) + Q2.b (0.5) + Q3 (0.5) = 2.5 pts ✓
**Corrigé officiel** (RR 34F p2) : `0.25 + 0.25 + 0.25 + 0.25 + 0.25 + 0.25 + 0.25 + 0.25 + 0.5 = 2.5 pts` ✓

🔴 **Problème** — l'exercice a `documents: []` (vide) :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2023-rattrapage/exam.json:285
          "documents": [],
```

**Mais** les questions Q2.a et Q2.b référencent `doc_g4` :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2023-rattrapage/exam.json:256-258
                  "documents": [
                    "doc_g4"
                  ],
```

**Référence orpheline** → `doc_g4` n'est défini nulle part. L'image (sujet p3) montre clairement **Document 1 = carte factorielle du chromosome 2** (Taille antennes 0 cM, Forme ailes 13 cM, Tarses 31 cM, Couleur corps 48 cM).

**Action requise** : ajouter un document `doc_e2_1` (ou renommer `doc_g4`) avec description de la carte factorielle du chromosome 2, et mettre à jour les références.

### 2.3 Exercice 3 — Pollution plastique (5 pts) ✓

**Structure** : Q1 (1) + Q2 (1) + Q3 (1) + Q4 (2) = 5 pts ✓
**Documents** : 5 documents image → `doc_e3_1` à `doc_e3_5` JSON, titres alignés ✓
**Descriptions** : fidèles aux images (Document 1 texte caractéristiques, Document 2 graph production/consommation, Document 3 chaîne alimentaire aquatique, Document 4 schéma fragmentation + santé, Document 5 tableau comparatif bioplastique/pétrochimique).

🟠 **Mineur** : questions sans champ `number`.

### 2.4 Exercice 4 — Ophiolites Alpes (5 pts) 🔴 **PROBLÈME MAJEUR**

**Structure** : Q1 (0.5) + Q2 (1.25) + Q3.a (1) + Q3.b (1) + Q4 (1.25) = 5 pts ✓

**Documents dans les images** (p5–p6) :
1. **Document 1** = carte Alpes + coupe géologique (p5)
2. **Document 2** = 4 schémas microscopiques a-b-c-d des gabbros (p6)
3. **Document 3** = diagramme P-T des faciès + réactions chimiques (p6)
4. **Document 4** = modèle 3 phases : subduction / obduction / collision (p6)

**Documents JSON** : seulement **2 objets** (`doc_e4_1`, `doc_e4_2`) :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2023-rattrapage/exam.json:443-457
          "documents": [
            {
              "id": "doc_e4_1",
              "type": "figure",
              "title": "Document 1",
              "description": "Ce document est composé de deux figures : une carte géographique (Figure a) et un schéma en coupe géologique (Figure b)...",
            },
            {
              "id": "doc_e4_2",
              "type": "figure",
              "title": "Document 2",
              "description": "Ce document est un schéma illustrant les différentes phases de la tectonique des plaques entre la plaque eurasienne et la plaque africaine. Il montre trois phases principales : la subduction (Phase 1), l'obduction (Phase 2) et la collision (Phase 3)..."
            }
          ]
```

🔴 **Trois problèmes** :

1. **Document 2 (gabbros microscopiques) totalement ABSENT** du JSON — pourtant essentiel pour Q3.a et Q3.b.
2. **Document 3 (diagramme P-T + réactions) totalement ABSENT** du JSON — pourtant essentiel pour Q3.a, Q3.b et Q4.
3. **`doc_e4_2` mal nommé** : le titre JSON dit « Document 2 » mais la description correspond en réalité au **Document 4** de l'image (phases tectoniques).

**Référence orpheline** :
```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2023-rattrapage/exam.json:409-412
                  "documents": [
                    "doc_g12",
                    "doc_g13"
                  ],
```
`doc_g12` et `doc_g13` n'existent nulle part.

**Actions requises** :
1. Ajouter deux nouveaux documents :
   - `doc_e4_2` titre « Document 2 » = 4 schémas microscopiques des gabbros (Gabbro dorsale / Métagabbro Chenaillet / Métagabbro Queyras / Métagabbro Viso) avec minéraux légende.
   - `doc_e4_3` titre « Document 3 » = diagramme P-T + légende faciès + 4 réactions minéralogiques.
2. Renommer l'actuel `doc_e4_2` → `doc_e4_4` avec titre « Document 4 ».
3. Remplacer les références orphelines :
   - Q3.a et Q3.b : `["doc_g12", "doc_g13"]` → `["doc_e4_2", "doc_e4_3"]`
   - Q4 : `["doc_e4_2"]` → `["doc_e4_4"]`

---

## 3. Totaux

| Partie | Somme questions | Déclaré | Verdict |
|---|---|---|---|
| Partie I | 1 + 1 + 2 + 1 = **5** | 5 | ✓ |
| Exercice 1 | 0.5 + 1.5 + 0.5 = **2.5** | 2.5 | ✓ |
| Exercice 2 | 0.75 + 1.25 + 0.5 = **2.5** | 2.5 | ✓ |
| Exercice 3 | 1 + 1 + 1 + 2 = **5** | 5 | ✓ |
| Exercice 4 | 0.5 + 1.25 + 2 + 1.25 = **5** | 5 | ✓ |
| **Total** | **20** | 20 | ✓ |

---

## 4. Résumé des actions

| Priorité | Localisation | Action |
|---|---|---|
| 🔴 Haute | Partie I / Question III | Restructurer de `association` vers `qcm` avec 4 sub_questions + choices |
| 🔴 Haute | Exercice 2 / `documents` | Ajouter `doc_e2_1` (carte factorielle chromosome 2) + corriger références `doc_g4` |
| 🔴 Haute | Exercice 4 / `documents` | Ajouter Documents 2 et 3 (gabbros + diagramme P-T), renommer existant en Document 4, corriger références `doc_g12`, `doc_g13` |
| 🔴 Haute | Exercice 1 / `doc_e1_2` | Corriger description hallucinée (Lys → Gln, pas Cys → stop) |
| 🟠 Moyenne | Partie I / Question IV | Corriger `content` des sub_questions 2, 3, 4 (ne pas répéter « Filament de myosine ») |
| 🟠 Moyenne | Ex1/2/3/4 questions | Ajouter champ `number` à toutes les questions (uniformité) |

**Contenu textuel (énoncés, barèmes, réponses)** : fidèle aux images et corrigé RR 34F.
**Contenu structurel** : 4 corrections majeures indispensables (QCM Partie I, documents Ex2 et Ex4, hallucination Ex1 Doc 2).
