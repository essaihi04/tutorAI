# Rapport de vérification visuelle — SVT 2023 Normale

**Méthode** : lecture directe des images `pages/sujet_p{1..6}.jpg` et `pages/correction_p{1..4}.jpg`, puis comparaison ligne par ligne avec `exam.json` (514 lignes).

**Résultat global** : structure globalement fidèle. **2 problèmes majeurs** identifiés (Exercice 3 et Exercice 4 — documents manquants / mal numérotés).

---

## 1. Partie I — Restitution des connaissances (5 pts)

| Élément | Image (sujet p1–p2) | JSON | Verdict |
|---|---|---|---|
| Question I (définitions, 1 pt) | 4 définitions → 4 termes | 4 items, 4 corrections `Eutrophisation / Effet de serre / Lixiviat / Energies renouvelables` | ✓ OK |
| Question II (V/F, 1 pt) | 4 propositions | 4 sub_questions, réponses `faux / vrai / vrai / vrai` | ✓ OK — cohérent avec barème 0.25×4 du corrigé |
| Question III (QCM, 2 pts) | 4 QCM | 4 sub_questions, réponses `a / d / c / c` | ✓ OK — identiques au corrigé `4×0.5` |
| Question IV (association, 1 pt) | 4 paires | pairs `(1-e, 2-c, 3-a, 4-b)` | ✓ OK |

**Partie I : parfaitement conforme.**

---

## 2. Deuxième partie — Raisonnement scientifique (15 pts)

### 2.1 Exercice 1 — Syndrome NARP (5 pts)

| Question | Image | JSON | Verdict |
|---|---|---|---|
| Contexte + Donnée 1 + Doc 1 (fig a, b, c) | p2 | context complet + `doc_e1_1` description fidèle | ✓ |
| Donnée 2 + Doc 2 (tableau milieux 1 et 2) | p2 | `doc_e1_2` description fidèle | ✓ |
| Donnée 3 + Doc 3 (chaîne respiratoire) | p3 | `doc_e1_3` description fidèle | ✓ |
| Q1.a Comparer (1 pt) | p2 | `sub_questions[0].letter=a, points=1` | ✓ |
| Q1.b Expliquer (1.25 pt) | p2 | `sub_questions[1].letter=b, points=1.25` | ✓ |
| Q2 Différences mitochondries (0.75 pt) | p2 | `points=0.75` | ✓ |
| Q3 Expliquer individu malade (1 pt) | p3 | `points=1` | ✓ |
| Q4 Relation symptômes NARP (1 pt) | p3 | `points=1` | ✓ |

**Somme : 1 + 1.25 + 0.75 + 1 + 1 = 5 pts ✓**
Corrections parfaitement alignées avec correction_p1.jpg / p2.jpg.

---

### 2.2 Exercice 2 — HCF (2.5 pts)

| Question | Image | JSON | Verdict |
|---|---|---|---|
| Contexte + Donnée 1 + Doc 1 (particule LDL, fig a/b/c) | p3 | context + `doc_e2_1` fidèle | ✓ |
| Donnée 2 + Doc 2 (récepteurs sain/malade) | p4 | `doc_e2_2` fidèle | ✓ |
| Donnée 3 + Doc 3 (fragments ADN) + Doc 4 (codons) | p4 | `doc_e2_3`, `doc_e2_4` fidèles | ✓ |
| Q1 Comparer (0.5 pt) | p4 | `points=0.5` | ✓ |
| Q2 Relation protéine-caractère (0.5 pt) | p4 | `points=0.5` | ✓ |
| Q3 ARNm + acides aminés + origine (1.5 pts) | p4 | `points=1.5` | ✓ |

**Somme : 0.5 + 0.5 + 1.5 = 2.5 pts ✓**

---

### 2.3 Exercice 3 — Génétique chats (2.5 pts) — 🟠 **PROBLÈME**

| Question | Image | JSON | Verdict |
|---|---|---|---|
| Contexte + Croisement 1 | p4 | context contient Croisement 1 | ✓ |
| **Croisement 2** (tableau avec parents ♂ bicolore × ♀ orange → 50% mâles orange poils ras / 50% femelles bicolores poils ras) | **p5 (haut)** | **ABSENT du `context`** | 🔴 **ERREUR** |
| Q1 Dominance (0.5 pt) | p4 | `points=0.5` | ✓ |
| Q2 Indépendance + hypothèses (1 pt) | p5 | `points=1` — **renvoie aux deux croisements** mais le Croisement 2 n'existe pas dans les données JSON | 🔴 Incohérence |
| Q3 Échiquier Croisement 2 (1 pt) | p5 | `points=1`, correction présente l'échiquier | 🟠 La question demande « du croisement 2 », mais le croisement 2 n'est pas dans le contexte JSON |

**🔴 Action requise** : enrichir `context` de l'Exercice 3 avec le tableau du Croisement 2 :

```
Pour vérifier les hypothèses proposées, un deuxième croisement entre des parents de races pures a été réalisé. Le tableau ci-dessous présente les résultats obtenus.

| Croisement 2 | Parents | | Descendance |
| --- | --- | --- | --- |
|  | Mâle de couleur noire et à poils ras × Femelle de couleur orange et à poils longs | | - 50% mâles de couleur orange à poils ras - 50% femelles bicolores à poils ras |
```

**Somme : 0.5 + 1 + 1 = 2.5 pts ✓** (barème OK, seul le contexte est incomplet)

---

### 2.4 Exercice 4 — Géologie massif de l'Arize (5 pts) — 🔴 **PROBLÈME MAJEUR**

**Documents dans les images (p5 bas + p6)** :
1. **Document 1** = coupe géologique (p5)
2. **Document 2** = carte géologique simplifiée du massif (Schiste R1, Micashiste 1 R2, Micashiste 2 R3, Gneiss R4, Migmatite R5) (p5)
3. **Document 3** = tableau présence/absence des minéraux index (Chlorite, Biotite, Andalousite, Muscovite, Sillimanite, Feldspath K) (p5)
4. **Document 4** = diagramme P-T des domaines de stabilité (p6)
5. **Document 5** = géothermes (p6)

**Documents dans le JSON** : seulement **4 objets** (`doc_e4_1` à `doc_e4_4`), numérotation décalée :

| ID JSON | Titre JSON | Description réelle | Image correspondante |
|---|---|---|---|
| `doc_e4_1` | « Document 1 » | coupe géologique | ✓ = Document 1 image |
| `doc_e4_2` | **« Document 2 »** | **tableau présence/absence minéraux** | 🔴 = Document **3** image (tableau) |
| `doc_e4_3` | **« Document 3 »** | **diagramme P-T stabilité** | 🔴 = Document **4** image |
| `doc_e4_4` | **« Document 4 »** | **géothermes** | 🔴 = Document **5** image |

**🔴 Le Document 2 (carte géologique simplifiée avec R1-R5) est totalement absent du JSON.**

**Conséquences sur les questions** :

| Question | Texte JSON | Référence `documents` | Problème |
|---|---|---|---|
| Q1 | « données du document 1 » | `doc_e4_1` | ✓ |
| Q2 | « données du **document 3** » | `doc_e4_2` (titre « Document 2 ») | 🔴 Incohérence : le texte dit doc 3 mais le JSON pointe sur doc titré « Document 2 » — alors qu'il s'agit bien du tableau minéraux (doc 3 de l'image) |
| Q3 | « documents 3 et 4 » | `doc_e4_2, doc_e4_3` (titres « Document 2, Document 3 ») | 🔴 Même décalage |
| Q4 | « document 4 » | `doc_e4_3` (titre « Document 3 ») | 🔴 Même décalage |
| Q5 | « documents 4 et 5 » | `doc_e4_3, doc_e4_4` (titres « Document 3, Document 4 ») | 🔴 Même décalage |

**🔴 Actions requises** :
1. **Ajouter** un nouveau document `doc_e4_2_map` (carte géologique simplifiée montrant les affleurements R1=Schiste, R2=Micashiste 1, R3=Micashiste 2, R4=Gneiss, R5=Migmatite) et **renuméroter** les références.
2. **Corriger les titres** :
   - `doc_e4_2` → titre « Document 3 »
   - `doc_e4_3` → titre « Document 4 »
   - `doc_e4_4` → titre « Document 5 »
3. Re-mapper `documents` dans chaque question selon la numérotation réelle.

**Somme barème : 0.5 + 1 + 1.5 + 1 + 1 = 5 pts ✓** (barème OK malgré les problèmes de numérotation)

---

## 3. Totaux

| Partie | Somme questions | Déclaré `points` | Verdict |
|---|---|---|---|
| Partie I | 1 + 1 + 2 + 1 = **5 pts** | 5 | ✓ |
| Exercice 1 | 1 + 1.25 + 0.75 + 1 + 1 = **5 pts** | 5 | ✓ |
| Exercice 2 | 0.5 + 0.5 + 1.5 = **2.5 pts** | 2.5 | ✓ |
| Exercice 3 | 0.5 + 1 + 1 = **2.5 pts** | 2.5 | ✓ |
| Exercice 4 | 0.5 + 1 + 1.5 + 1 + 1 = **5 pts** | 5 | ✓ |
| **Total** | **20 pts** | 20 | ✓ |

---

## 4. Résumé des actions

| Priorité | Localisation | Action |
|---|---|---|
| 🔴 Haute | Exercice 4 `documents` | Ajouter la carte géologique (Document 2 image) + renommer les titres `doc_e4_2..4` en Document 3/4/5 |
| 🔴 Haute | Exercice 3 `context` | Ajouter le tableau Croisement 2 |
| 🟢 Faible | — | Aucun autre correctif |

**Contenu textuel (énoncés, corrections, barèmes)** : fidèle aux images et au corrigé officiel NR 34F.
**Contenu structurel (documents, numérotation)** : nécessite 2 corrections ciblées sur Exercices 3 et 4.
