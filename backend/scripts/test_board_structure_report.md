# Test multi-modes — STRUCTURATION DU TABLEAU

_Généré le 2026-05-01 13:07:34_


Objectif : vérifier que le LLM produit une réponse **STRUCTURÉE au tableau** (et non en texte brut) dans les modes `libre` et `coaching`, avec une attention particulière sur la génétique (notation diploïde double-barre).


## Score global : **30/30** — 🎉 TOUT VERT


| # | Scénario | Mode | Score | Verdict |
|---|---|---|---|---|
| 1 | A • LIBRE + Dihybride F1×F1 (échiquier 4×4) | `libre` | 9/9 | ✅ |
| 2 | B • LIBRE + Monohybride F1×F1 (2×2) | `libre` | 8/8 | ✅ |
| 3 | C • COACHING + Génétique (échiquier dihybride) | `coaching` | 9/9 | ✅ |
| 4 | D • LIBRE + Mitose (structuration pure, sans génétique) | `libre` | 4/4 | ✅ |

---

## 1. A • LIBRE + Dihybride F1×F1 (échiquier 4×4)

- **Mode** : `libre`
- **Génétique** : True  •  **Échiquier 4×4 attendu** : True
- **Temps LLM** : 22.0s  •  **Réponse** : 5081 chars  •  **Boards** : 1

**Message envoyé :**
> Je suis en 2BAC SVT BIOF. Explique-moi le croisement dihybride F1 × F1 entre deux pois doublement hétérozygotes (gènes G/g et L/l, indépendants). Je veux les phénotypes parents, les génotypes en notation chromosomique, les 4 gamètes avec leur pourcentage, l'échiquier de fécondation 4×4 complet, puis les proportions phénotypiques 9/16, 3/16, 3/16, 1/16. Mets tout dans un tableau récapitulatif au tableau.

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | Pas de boucle de padding LaTeX (\; / \, / \quad) | ✅ PASS | OK |
| 2 | Réponse STRUCTURÉE — un bloc <ui> show_board (ou <board>) est émis | ✅ PASS | 1 board(s) détecté(s) |
| 3 | Pas de `\text`/`\times`/`\frac` corrompu en tab/formfeed | ✅ PASS | OK |
| 4 | Board non vide (≥ 3 lignes) | ✅ PASS | 26 ligne(s) au total |
| 5 | Aucune notation ASCII `XY//xy` résiduelle | ✅ PASS | OK |
| 6 | Au moins une cellule contient `\dfrac` / `\frac` | ✅ PASS | OK |
| 7 | Génotypes en notation DIPLOÏDE (\overline{} = 2 barres) | ✅ PASS | 38 génotype(s) diploïde(s) détecté(s) |
| 8 | Aucun génotype à une seule barre dans les cellules d'échiquier | ✅ PASS | OK |
| 9 | Échiquier dihybride 4×4 (16 zygotes) | ✅ PASS | OK |

### Boards (après sanitizer)

**Board 1 — « Croisement Dihybride F1 × F1 — Pois (G/g, L/l) — Gènes Indépendants »**

```json
[
  {
    "type": "title",
    "content": "1️⃣ Parents P1 × P2 (génération parentale)"
  },
  {
    "type": "text",
    "content": "P1 : pois jaunes lisses [G,L] — P2 : pois verts ridés [g,l]"
  },
  {
    "type": "math",
    "content": "\\text{Génotypes : }\\;\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{L}}\\;\\times\\;\\dfrac{g}{\\overline{g}}\\,\\dfrac{l}{\\overline{l}}"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "title",
    "content": "2️⃣ F1 — 100 % [G,L] double hétérozygote"
  },
  {
    "type": "math",
    "content": "\\text{Génotype F1 : }\\;\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{l}}"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "title",
    "content": "3️⃣ Gamètes produits par F1 (équiprobables — gènes indépendants)"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 1 : }\\;\\dfrac{G}{}\\,\\dfrac{L}{}\\;(25\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 2 : }\\;\\dfrac{G}{}\\,\\dfrac{l}{}\\;(25\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 3 : }\\;\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 4 : }\\;\\dfrac{g}{}\\,\\dfrac{l}{}\\;(25\\,\\%)"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "title",
    "content": "4️⃣ Échiquier de fécondation F1 × F1 (16 cases)"
  },
  {
    "type": "table",
    "content": "",
    "headers": [
      "♀ \\\\ ♂",
      "\\dfrac{G}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
      "\\dfrac{G}{}\\,\\dfrac{l}{}\\;(25\\,\\%)",
      "\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
      "\\dfrac{g}{}\\,\\dfrac{l}{}\\;(25\\,\\%)"
    ],
    "rows": [
      [
        "\\dfrac{G}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
        "\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{L}}\\;[G,L]",
        "\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{l}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{L}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{l}}\\;[G,L]"
      ],
      [
        "\\dfrac{G}{}\\,\\dfrac{l}{}\\;(25\\,\\%)",
        "\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{l}}\\;[G,L]",
        "\\dfrac{G}{\\overline{G}}\\,\\dfrac{l}{\\overline{l}}\\;[G,l]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{l}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{l}{\\overline{l}}\\;[G,l]"
      ],
      [
        "\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{L}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{l}}\\;[G,L]",
        "\\dfrac{g}{\\overline{g}}\\,\\dfrac{L}{\\overline{L}}\\;[g,L]",
        "\\dfrac{g}{\\overline{g}}\\,\\dfrac{L}{\\overline{l}}\\;[g,L]"
      ],
      [
        "\\dfrac{g}{}\\,\\dfrac{l}{}\\;(25\\,\\%)",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{l}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{l}{\\overline{l}}\\;[G,l]",
        "\\dfrac{g}{\\overline{g}}\\,\\dfrac{L}{\\overline{l}}\\;[g,L]",
        "\\dfrac{g}{\\overline{g}}\\,\\dfrac{l}{\\overline{l}}\\;[g,l]"
      ]
    ]
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "title",
    "content": "5️⃣ Proportions phénotypiques F2"
  },
  {
    "type": "box",
    "content": "[G,L] jaune lisse : 9/16 = 56,25 %",
    "color": "green"
  },
  {
    "type": "box",
    "content": "[G,l] jaune ridé : 3/16 = 18,75 %",
    "color": "orange"
  },
  {
    "type": "box",
    "content": "[g,L] vert lisse : 3/16 = 18,75 %",
    "color": "orange"
  },
  {
    "type": "box",
    "content": "[g,l] vert ridé : 1/16 = 6,25 %",
    "color": "red"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "📝 À NOTER POUR LE BAC"
  },
  {
    "type": "warning",
    "content": "⚠️ Piège : Ne confonds pas [G,l] et [g,L] — ils ont la MÊME proportion 3/16 mais des phénotypes DIFFÉRENTS !"
  },
  {
    "type": "tip",
    "content": "💡 Astuce : 9:3:3:1 → somme = 16. Vérifie toujours que 9+3+3+1 = 16."
  },
  {
    "type": "box",
    "content": "✅ Règle d'or : Gènes indépendants → 4 gamètes équiprobables (25 % chacun) → 16 cases dans l'échiquier.",
    "color": "blue"
  }
]
```

---

## 2. B • LIBRE + Monohybride F1×F1 (2×2)

- **Mode** : `libre`
- **Génétique** : True  •  **Échiquier 4×4 attendu** : False
- **Temps LLM** : 17.6s  •  **Réponse** : 3885 chars  •  **Boards** : 1

**Message envoyé :**
> Explique-moi un croisement monohybride simple : pois lisse (L) dominant × pois ridé (r) récessif, F1 hétérozygote, puis F1×F1. Je veux le tableau de fécondation 2×2 avec les génotypes diploïdes et les proportions 3/4 dominant, 1/4 récessif. Au tableau.

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | Pas de boucle de padding LaTeX (\; / \, / \quad) | ✅ PASS | OK |
| 2 | Réponse STRUCTURÉE — un bloc <ui> show_board (ou <board>) est émis | ✅ PASS | 1 board(s) détecté(s) |
| 3 | Pas de `\text`/`\times`/`\frac` corrompu en tab/formfeed | ✅ PASS | OK |
| 4 | Board non vide (≥ 3 lignes) | ✅ PASS | 31 ligne(s) au total |
| 5 | Aucune notation ASCII `XY//xy` résiduelle | ✅ PASS | OK |
| 6 | Au moins une cellule contient `\dfrac` / `\frac` | ✅ PASS | OK |
| 7 | Génotypes en notation DIPLOÏDE (\overline{} = 2 barres) | ✅ PASS | 10 génotype(s) diploïde(s) détecté(s) |
| 8 | Aucun génotype à une seule barre dans les cellules d'échiquier | ✅ PASS | OK |

### Boards (après sanitizer)

**Board 1 — « Croisement monohybride — Pois lisse × Pois ridé »**

```json
[
  {
    "type": "title",
    "content": "1er croisement : P1 [L] × P2 [r] (Parents purs)"
  },
  {
    "type": "math",
    "content": "\\text{Phénotypes : }[L]\\;\\times\\;[r]"
  },
  {
    "type": "math",
    "content": "\\text{Génotypes : }\\dfrac{L}{\\overline{L}}\\;\\times\\;\\dfrac{r}{\\overline{r}}"
  },
  {
    "type": "subtitle",
    "content": "Gamètes produits"
  },
  {
    "type": "math",
    "content": "P1\\to\\;\\dfrac{L}{}\\;(100\\,\\%)"
  },
  {
    "type": "math",
    "content": "P2\\to\\;\\dfrac{r}{}\\;(100\\,\\%)"
  },
  {
    "type": "subtitle",
    "content": "Fécondation → F1"
  },
  {
    "type": "table",
    "content": "",
    "headers": [
      "♀ \\\\ ♂",
      "\\dfrac{r}{}\\;(100\\,\\%)"
    ],
    "rows": [
      [
        "\\dfrac{L}{}\\;(100\\,\\%)",
        "\\dfrac{L}{\\overline{r}}\\;[L]"
      ]
    ]
  },
  {
    "type": "box",
    "content": "F1 : 100 % [L] — tous hétérozygotes \\dfrac{L}{\\overline{r}}",
    "color": "green"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "title",
    "content": "2e croisement : F1 × F1 (autofécondation)"
  },
  {
    "type": "math",
    "content": "\\text{Phénotypes : }[L]\\;\\times\\;[L]"
  },
  {
    "type": "math",
    "content": "\\text{Génotypes : }\\dfrac{L}{\\overline{r}}\\;\\times\\;\\dfrac{L}{\\overline{r}}"
  },
  {
    "type": "subtitle",
    "content": "Gamètes produits par chaque F1"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 1 : }\\dfrac{L}{}\\;(50\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 2 : }\\dfrac{r}{}\\;(50\\,\\%)"
  },
  {
    "type": "subtitle",
    "content": "Échiquier de fécondation F1 × F1"
  },
  {
    "type": "table",
    "content": "",
    "headers": [
      "♀ \\\\ ♂",
      "\\dfrac{L}{}\\;(50\\,\\%)",
      "\\dfrac{r}{}\\;(50\\,\\%)"
    ],
    "rows": [
      [
        "\\dfrac{L}{}\\;(50\\,\\%)",
        "\\dfrac{L}{\\overline{L}}\\;[L]",
        "\\dfrac{L}{\\overline{r}}\\;[L]"
      ],
      [
        "\\dfrac{r}{}\\;(50\\,\\%)",
        "\\dfrac{L}{\\overline{r}}\\;[L]",
        "\\dfrac{r}{\\overline{r}}\\;[r]"
      ]
    ]
  },
  {
    "type": "box",
    "content": "Résultats F2 — [L] : 3/4 = 75 %  |  [r] : 1/4 = 25 %",
    "color": "orange"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "📝 À NOTER — Points clés"
  },
  {
    "type": "text",
    "content": "• Allèle L (lisse) dominant sur r (ridé) → L > r"
  },
  {
    "type": "text",
    "content": "• F1 hétérozygote = phénotype [L] car L domine r"
  },
  {
    "type": "text",
    "content": "• F2 : 3 génotypes possibles : LL (25%), Lr (50%), rr (25%)"
  },
  {
    "type": "text",
    "content": "• Rapport phénotypique 3:1 = signature du monohybridisme"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "⚠️ Piège BAC"
  },
  {
    "type": "warning",
    "content": "Ne confonds pas génotype et phénotype ! [L] peut être LL ou Lr. Seul le test-cross (F1 × [r]) permet de distinguer."
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "💡 Astuce mémoire"
  },
  {
    "type": "tip",
    "content": "3:1 = 3 carrés sur 4 = 75% lisses, 1 carré sur 4 = 25% ridés. Visualise l'échiquier 2×2 !"
  }
]
```

---

## 3. C • COACHING + Génétique (échiquier dihybride)

- **Mode** : `coaching`
- **Chapitre** : Génétique humaine — transmission de deux gènes
- **Leçon** : Brassage interchromosomique — dihybridisme
- **Génétique** : True  •  **Échiquier 4×4 attendu** : True
- **Temps LLM** : 15.5s  •  **Réponse** : 3302 chars  •  **Boards** : 1

**Message envoyé :**
> Donne-moi un exemple complet d'échiquier de croisement dihybride entre deux F1 hétérozygotes (gènes A/a et B/b indépendants) avec les 16 zygotes, les 4 phénotypes et leurs proportions. Mets tout au tableau.

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | Pas de boucle de padding LaTeX (\; / \, / \quad) | ✅ PASS | OK |
| 2 | Réponse STRUCTURÉE — un bloc <ui> show_board (ou <board>) est émis | ✅ PASS | 1 board(s) détecté(s) |
| 3 | Pas de `\text`/`\times`/`\frac` corrompu en tab/formfeed | ✅ PASS | OK |
| 4 | Board non vide (≥ 3 lignes) | ✅ PASS | 15 ligne(s) au total |
| 5 | Aucune notation ASCII `XY//xy` résiduelle | ✅ PASS | OK |
| 6 | Au moins une cellule contient `\dfrac` / `\frac` | ✅ PASS | OK |
| 7 | Génotypes en notation DIPLOÏDE (\overline{} = 2 barres) | ✅ PASS | 40 génotype(s) diploïde(s) détecté(s) |
| 8 | Aucun génotype à une seule barre dans les cellules d'échiquier | ✅ PASS | OK |
| 9 | Échiquier dihybride 4×4 (16 zygotes) | ✅ PASS | OK |

### Boards (après sanitizer)

**Board 1 — « Échiquier de croisement F1 × F1 — Gènes indépendants »**

```json
[
  {
    "type": "subtitle",
    "content": "Parents : F1 [A,B] × F1 [A,B] (doubles hétérozygotes)"
  },
  {
    "type": "math",
    "content": "\\text{Génotypes : }\\;\\dfrac{A}{\\overline{a}}\\,\\dfrac{B}{\\overline{b}}\\;\\times\\;\\dfrac{A}{\\overline{a}}\\,\\dfrac{B}{\\overline{b}}"
  },
  {
    "type": "subtitle",
    "content": "Gamètes (4 types équiprobables : 25 % chacun)"
  },
  {
    "type": "math",
    "content": "\\dfrac{A}{}\\,\\dfrac{B}{}\\;(25\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\dfrac{A}{}\\,\\dfrac{b}{}\\;(25\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\dfrac{a}{}\\,\\dfrac{B}{}\\;(25\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\dfrac{a}{}\\,\\dfrac{b}{}\\;(25\\,\\%)"
  },
  {
    "type": "subtitle",
    "content": "Échiquier de fécondation (16 cases)"
  },
  {
    "type": "table",
    "content": "",
    "headers": [
      "♀ \\\\ ♂",
      "\\dfrac{A}{}\\,\\dfrac{B}{}\\;(25\\,\\%)",
      "\\dfrac{A}{}\\,\\dfrac{b}{}\\;(25\\,\\%)",
      "\\dfrac{a}{}\\,\\dfrac{B}{}\\;(25\\,\\%)",
      "\\dfrac{a}{}\\,\\dfrac{b}{}\\;(25\\,\\%)"
    ],
    "rows": [
      [
        "\\dfrac{A}{}\\,\\dfrac{B}{}\\;(25\\,\\%)",
        "\\dfrac{A}{\\overline{A}}\\,\\dfrac{B}{\\overline{B}}\\;[A,B]",
        "\\dfrac{A}{\\overline{A}}\\,\\dfrac{B}{\\overline{b}}\\;[A,B]",
        "\\dfrac{A}{\\overline{a}}\\,\\dfrac{B}{\\overline{B}}\\;[A,B]",
        "\\dfrac{A}{\\overline{a}}\\,\\dfrac{B}{\\overline{b}}\\;[A,B]"
      ],
      [
        "\\dfrac{A}{}\\,\\dfrac{b}{}\\;(25\\,\\%)",
        "\\dfrac{A}{\\overline{A}}\\,\\dfrac{B}{\\overline{b}}\\;[A,B]",
        "\\dfrac{A}{\\overline{A}}\\,\\dfrac{b}{\\overline{b}}\\;[A,b]",
        "\\dfrac{A}{\\overline{a}}\\,\\dfrac{B}{\\overline{b}}\\;[A,B]",
        "\\dfrac{A}{\\overline{a}}\\,\\dfrac{b}{\\overline{b}}\\;[A,b]"
      ],
      [
        "\\dfrac{a}{}\\,\\dfrac{B}{}\\;(25\\,\\%)",
        "\\dfrac{A}{\\overline{a}}\\,\\dfrac{B}{\\overline{B}}\\;[A,B]",
        "\\dfrac{A}{\\overline{a}}\\,\\dfrac{B}{\\overline{b}}\\;[A,B]",
        "\\dfrac{a}{\\overline{a}}\\,\\dfrac{B}{\\overline{B}}\\;[a,B]",
        "\\dfrac{a}{\\overline{a}}\\,\\dfrac{B}{\\overline{b}}\\;[a,B]"
      ],
      [
        "\\dfrac{a}{}\\,\\dfrac{b}{}\\;(25\\,\\%)",
        "\\dfrac{A}{\\overline{a}}\\,\\dfrac{B}{\\overline{b}}\\;[A,B]",
        "\\dfrac{A}{\\overline{a}}\\,\\dfrac{b}{\\overline{b}}\\;[A,b]",
        "\\dfrac{a}{\\overline{a}}\\,\\dfrac{B}{\\overline{b}}\\;[a,B]",
        "\\dfrac{a}{\\overline{a}}\\,\\dfrac{b}{\\overline{b}}\\;[a,b]"
      ]
    ]
  },
  {
    "type": "subtitle",
    "content": "Proportions phénotypiques F2",
    "color": "blue"
  },
  {
    "type": "math",
    "content": "[A,B]\\;:\\;\\dfrac{9}{\\overline{16}}=56,25\\,\\%"
  },
  {
    "type": "math",
    "content": "[A,b]\\;:\\;\\dfrac{3}{\\overline{16}}=18,75\\,\\%"
  },
  {
    "type": "math",
    "content": "[a,B]\\;:\\;\\dfrac{3}{\\overline{16}}=18,75\\,\\%"
  },
  {
    "type": "math",
    "content": "[a,b]\\;:\\;\\dfrac{1}{\\overline{16}}=6,25\\,\\%"
  },
  {
    "type": "box",
    "content": "Rapport 9:3:3:1 — caractéristique du dihybridisme à gènes indépendants",
    "color": "green"
  }
]
```

---

## 4. D • LIBRE + Mitose (structuration pure, sans génétique)

- **Mode** : `libre`
- **Génétique** : False  •  **Échiquier 4×4 attendu** : False
- **Temps LLM** : 14.8s  •  **Réponse** : 3545 chars  •  **Boards** : 1

**Message envoyé :**
> Résume-moi les 4 phases de la mitose dans un TABLEAU au tableau : prophase, métaphase, anaphase, télophase. Pour chaque phase : événements clés et schéma simplifié.

### Checks
| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | Pas de boucle de padding LaTeX (\; / \, / \quad) | ✅ PASS | OK |
| 2 | Réponse STRUCTURÉE — un bloc <ui> show_board (ou <board>) est émis | ✅ PASS | 1 board(s) détecté(s) |
| 3 | Pas de `\text`/`\times`/`\frac` corrompu en tab/formfeed | ✅ PASS | OK |
| 4 | Board non vide (≥ 3 lignes) | ✅ PASS | 31 ligne(s) au total |

### Boards (après sanitizer)

**Board 1 — « Les 4 phases de la mitose »**

```json
[
  {
    "type": "title",
    "content": "🔬 MITOSE : Division cellulaire (2n → 2 cellules filles 2n)"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "1️⃣ PROPHASE"
  },
  {
    "type": "text",
    "content": "• Condensation de la chromatine en chromosomes visibles (2 chromatides sœurs)"
  },
  {
    "type": "text",
    "content": "• Disparition de l'enveloppe nucléaire et du nucléole"
  },
  {
    "type": "text",
    "content": "• Formation du fuseau achromatique (microtubules) à partir du centrosome"
  },
  {
    "type": "text",
    "content": "🧑‍🎨 Schéma : chromosomes en bâtonnets, noyau qui disparaît, fuseau qui apparaît"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "2️⃣ MÉTAPHASE"
  },
  {
    "type": "text",
    "content": "• Alignement des chromosomes sur la plaque équatoriale (métaphasique)"
  },
  {
    "type": "text",
    "content": "• Chaque chromosome est attaché aux fibres du fuseau par son centromère"
  },
  {
    "type": "text",
    "content": "🧑‍🎨 Schéma : chromosomes alignés au centre, fuseau de part et d'autre"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "3️⃣ ANAPHASE"
  },
  {
    "type": "text",
    "content": "• Séparation des chromatides sœurs au niveau du centromère"
  },
  {
    "type": "text",
    "content": "• Migration des chromatides vers les pôles opposés (tirées par les microtubules)"
  },
  {
    "type": "text",
    "content": "🧑‍🎨 Schéma : deux groupes de chromatides s'éloignant vers les pôles"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "4️⃣ TÉLOPHASE"
  },
  {
    "type": "text",
    "content": "• Arrivée des chromatides aux pôles → décondensation en chromatine"
  },
  {
    "type": "text",
    "content": "• Reformation de l'enveloppe nucléaire autour de chaque lot"
  },
  {
    "type": "text",
    "content": "• Disparition du fuseau achromatique"
  },
  {
    "type": "text",
    "content": "🧑‍🎨 Schéma : deux noyaux reformés, cytoplasme prêt à se diviser"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "box",
    "content": "📝 À RETENIR : P-M-A-T (Prophase → Métaphase → Anaphase → Télophase). La mitose conserve le nombre de chromosomes (2n → 2n).",
    "color": "orange"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "⚠️ PIÈGE BAC"
  },
  {
    "type": "warning",
    "content": "Ne confonds pas ANAPHASE (séparation des chromatides) et ANAPHASE I de méiose (séparation des chromosomes homologues). Dans la mitose, ce sont les chromatides sœurs qui se séparent."
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "💡 ASTUCE MÉMOIRE"
  },
  {
    "type": "tip",
    "content": "Pense au mot « PAMAT » : Prophase (Prépare), Anaphase (Arrache), Métaphase (Milieu), Télophase (Termine). Ou retiens la phrase : « Pendant Ma Tante Annette Téléphone »."
  }
]
```

---

**Score final : 30/30** — 🎉 TOUT VERT
