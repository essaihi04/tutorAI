# Rapport de vérification visuelle — SVT 2025 Rattrapage

**Méthode** : lecture directe des images `pages/sujet_p{1..6}.jpg` et `pages/correction_p{1..5}.jpg`, puis comparaison avec `exam.json` (389 lignes).

**Résultat global** : barèmes et corrections conformes au corrigé officiel RR-34F. **1 problème structurel majeur** (QCM de Partie I mal modélisé) + **2 problèmes mineurs** (absence de `number` et incohérence `id`).

---

## 1. Partie I — Restitution des connaissances (5 pts)

### 1.1 Question I (1 pt) — Définitions ✓

**Image** (p1) : Définir Incinération et Lixiviat.
**Corrigé** (RR-34F p1) : 0.5 × 2.
**JSON** : question unique `points: 1`, correction contient les deux définitions concaténées.

🟠 **Mineur** : pas de décomposition en sub_questions (0.5 chacune). Cela rend la notation granulaire impossible côté frontend.

### 1.2 Question II (1 pt) — Citer deux solutions CO₂ ✓

**Image** (p1) : Citer deux solutions pour réduire la pollution par le CO₂.
**Corrigé** : 0.5 × 2 (énergies renouvelables + plantation d'arbres).
**JSON** : question unique `points: 1` ✓.

### 1.3 Question III (2 pts) — QCM 🔴 **STRUCTURE INCORRECTE**

**Image** (p1) : 4 propositions, chacune avec 4 choix `a/b/c/d` **indépendants** :
- 1. Production biogaz (a-d)
- 2. Enfouissement déchets (a-d)
- 3. IBQS (a-d)
- 4. Ordre chronologique eutrophisation (a-d)

**Corrigé officiel** : `(1,a); (2,c); (3,b); (4,c)`.

**JSON** : `type: "association"` avec `items_right` aplati contenant **16 choix** de toutes les questions mélangés :

```@c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/svt/2025-rattrapage/exam.json:44-61
          "items_right": [
            "a. la matière organique par fermentation.",
            "b. la matière inorganique par fermentation.",
            "c. la matière organique par respiration.",
            "d. la matière inorganique par respiration.",
            "a. la valorisation des déchets plastiques.",
            "b. la valorisation des déchets en produisant du compost.",
            ...
          ]
```

→ **Ambiguïté** : les `correct_pairs: (1,a); (2,c); (3,b); (4,c)` renvoient à quelle occurrence de `a`, `c` ou `b` parmi les 4 blocs de 4 ? La structure est incorrecte.

**Action requise** : restructurer en `type: "qcm"` avec 4 `sub_questions`, chacune avec 4 `choices` (lettre + texte) + `correct_answer` individuel, comme dans le JSON 2024-rattrapage ou 2025-normale.

### 1.4 Question IV (1 pt) — V/F ✓

| # | Image (p1) | Corrigé (RR-34F) | JSON | Verdict |
|---|---|---|---|---|
| 1 | Ozone troposphérique = GES | Vrai | `vrai` | ✓ |
| 2 | Pollution organique → augmentation O₂ | Faux | `faux` | ✓ |
| 3 | Compostage → diminution volume + fertilisants | Vrai | `vrai` | ✓ |
| 4 | Déchets nucléaires classés selon activité + durée | Vrai | `vrai` | ✓ |

🟠 **Mineur** : sub_questions utilisent le champ `id: "IV.1"` au lieu de `number: "1"` (incohérence avec d'autres examens).

---

## 2. Deuxième partie — Raisonnement scientifique (15 pts)

### 2.1 Exercice 1 — Asthénozoospermie (5 pts) ✓

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Comparer + cause infertilité | p2 | 1 | ✓ |
| Q2.a Relation enzymes-mobilité | p3 | 1 | ✓ |
| Q2.b Expliquer infertilité | p3 | 1.5 | ✓ |
| Q3 Effet succinate sur mobilité | p3 | 1.5 | ✓ |

**Somme : 1 + 2.5 + 1.5 = 5 pts ✓**

**Documents** : 2 docs image (Doc 1 tableau sperme ; Doc 2 = 4 figures a-b-c-d combinées) → 2 docs JSON `doc_e1_1`, `doc_e1_2` ✓ descriptions fidèles ✓.

🟠 **Mineur** : aucune question n'a de champ `number` (ni `Q1`, ni `Q2`, ni `Q3`).

### 2.2 Exercice 2 — Marfan (2.5 pts) ✓

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Génotype détermine phénotype | p3 | 1 | ✓ |
| Q2 ARNm + aa + origine génétique | p4 | 1.5 | ✓ |

**Somme : 1 + 1.5 = 2.5 pts ✓**

**Documents** : 3 docs image (Doc 1 génotype-FIB-1-phénotype ; Doc 2 fragments allèles triplets 476-481 ; Doc 3 code génétique) → 3 docs JSON ✓ descriptions fidèles ✓.

**Correction Q2** : mutation G→A au 2ᵉ nucléotide du triplet 479 → codon UGU→UAU → Cys→Tyr. ✓ Conforme à l'image (triplet 479 : TGT→TAT) et à la correction officielle RR-34F.

🟠 **Mineur** : questions sans champ `number`.

### 2.3 Exercice 3 — Tomate (2.5 pts) ✓

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Interprétation chromosomique Croisements 1 & 2 | p5 | 2 | ✓ |
| Q2 Croisement optimal poils+ronds | p5 | 0.5 | ✓ |

**Somme : 2 + 0.5 = 2.5 pts ✓**

**Documents** : 2 docs image (Doc 1 chromosomes 1 & 7 avec gènes ; Doc 2 tableau croisements tests) → 2 docs JSON ✓ descriptions fidèles ✓.

🟠 **Mineur** : questions sans champ `number`.

### 2.4 Exercice 4 — Géologie Andlau (5 pts) ✓

| Question | Image | Points | Verdict |
|---|---|---|---|
| Q1 Changements minéralogiques + métamorphisme | p5 | 1.5 | ✓ |
| Q2 Conditions P-T + type métamorphisme | p6 | 1.5 | ✓ |
| Q3 Formation granite Andlau + relation R1,R2,R3 | p6 | 2 | ✓ |

**Somme : 1.5 + 1.5 + 2 = 5 pts ✓**

**Documents** : 6 docs image (Doc 1 carte géologique ; Doc 2 tableau minéraux R1/R2/R3 ; Doc 3 diagramme P-T minéraux index ; Doc 4 types métamorphisme ; Doc 5 collision+granite ; Doc 6 trajet PTt) → 6 docs JSON `doc_e4_1..6` ✓ descriptions fidèles ✓.

🟠 **Mineur** : questions sans champ `number`.

---

## 3. Totaux

| Partie | Somme questions | Déclaré | Verdict |
|---|---|---|---|
| Partie I | 1 + 1 + 2 + 1 = **5** | 5 | ✓ |
| Exercice 1 | 1 + 2.5 + 1.5 = **5** | 5 | ✓ |
| Exercice 2 | 1 + 1.5 = **2.5** | 2.5 | ✓ |
| Exercice 3 | 2 + 0.5 = **2.5** | 2.5 | ✓ |
| Exercice 4 | 1.5 + 1.5 + 2 = **5** | 5 | ✓ |
| **Total** | **20** | 20 | ✓ |

---

## 4. Résumé des actions

| Priorité | Localisation | Action |
|---|---|---|
| 🔴 Haute | Partie I / Question III | Restructurer de `type: "association"` vers `type: "qcm"` avec 4 sub_questions × 4 choices, supprimer le aplati `items_right` 16 éléments |
| 🟠 Moyenne | Partie I (I, II) | Décomposer en sub_questions avec `points: 0.5` chacune (pour granularité autocorrection) |
| 🟠 Moyenne | Partie I sub_questions IV | Remplacer `id: "IV.1"` par `number: "1"` (cohérence inter-examens) |
| 🟠 Moyenne | Exercices 1-4 / questions | Ajouter champ `number` à toutes les questions (Q1, Q2, Q3, Q4) |
| 🟢 — | Barèmes et corrections | Conformes intégralement au RR-34F officiel |

**Points forts** : Partie I (IV V/F) et tous les Exercices 1-4 ont des contenus textuels fidèles aux images, corrections alignées au corrigé RR-34F, documents correctement identifiés et titrés, contextes complets.
**Point faible unique** : Question III de Partie I mal modélisée en `association` (même problème que 2023-rattrapage et 2024-normale).
