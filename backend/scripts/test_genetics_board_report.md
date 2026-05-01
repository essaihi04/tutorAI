# Test : Échiquier de croisement — SVT 2025 Normale (Q20)

_Généré le 2026-05-01 12:46:55_


**Temps LLM** : 26.8s — **Réponse** : 5374 chars

**Boards détectés** : 1


## Checks

| # | Vérification | Statut | Détail |
|---|---|---|---|
| 1 | Pas de boucle de padding LaTeX dans la réponse brute | ✅ PASS | OK |
| 2 | Un bloc <ui> show_board (ou <board>) est émis | ✅ PASS | 1 board(s) détecté(s) |
| 3 | Au moins une ligne `type=table` (échiquier de fécondation) | ✅ PASS | 1 table(s) trouvée(s) |
| 4 | Échiquier dihybride 4×4 (16 zygotes) | ✅ PASS | table(s) 4×4 : True |
| 5 | Aucune notation ASCII `XY//xy` résiduelle (post-sanitizer) | ✅ PASS | fuites : [] |
| 6 | Au moins une cellule contient `\dfrac` / `\frac` | ✅ PASS | OK |
| 7 | Pas de `\text`/`\times`/`\frac` corrompu en tab/formfeed | ✅ PASS | OK |
| 8 | Les 4 phénotypes F2 apparaissent : [G,L] [G,ℓ] [g,L] [g,ℓ] | ✅ PASS | trouvés : ['[G,L]', '[G,ℓ]', '[g,L]', '[g,ℓ]'] |
| 9 | Proportions 9/16, 3/16, 1/16 mentionnées | ✅ PASS | trouvées : ['9/16', '3/16', '1/16'] |
| 10 | Double barre `//` entre paires homologues (dihybride indépendant) | ✅ PASS | séparateurs `}\,//\,\dfrac` trouvés : 30 |

**Score : 10/10** — 🎉 TOUT VERT


## Contenu des boards (après sanitizer)


### Board 1 — « Interprétation chromosomique du 2e croisement »

```json
[
  {
    "type": "subtitle",
    "content": "1️⃣ Parents : F1 × F1"
  },
  {
    "type": "math",
    "content": "\\text{Phénotypes : }\\;[G,L]\\;\\times\\;[G,L]"
  },
  {
    "type": "math",
    "content": "\\text{Génotypes : }\\;\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;\\times\\;\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "2️⃣ Gamètes produits par chaque parent (équiprobables)"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 1 : }\\;\\dfrac{G}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 2 : }\\;\\dfrac{G}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 3 : }\\;\\dfrac{g}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)"
  },
  {
    "type": "math",
    "content": "\\text{Gamète 4 : }\\;\\dfrac{g}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)"
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "3️⃣ Échiquier de fécondation F1 × F1"
  },
  {
    "type": "table",
    "content": "",
    "headers": [
      "♀ \\\\ ♂",
      "\\dfrac{G}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)",
      "\\dfrac{G}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
      "\\dfrac{g}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)",
      "\\dfrac{g}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)"
    ],
    "rows": [
      [
        "\\dfrac{G}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)",
        "\\dfrac{G}{G}\\,//\\,\\dfrac{L}{L}\\;[G,L]",
        "\\dfrac{G}{G}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{L}\\;[G,L]",
        "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]"
      ],
      [
        "\\dfrac{G}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
        "\\dfrac{G}{G}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{G}{G}\\,//\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]",
        "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{G}{g}\\,//\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]"
      ],
      [
        "\\dfrac{g}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)",
        "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{L}\\;[G,L]",
        "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{g}{g}\\,//\\,\\dfrac{L}{L}\\;[g,L]",
        "\\dfrac{g}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[g,L]"
      ],
      [
        "\\dfrac{g}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
        "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{G}{g}\\,//\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]",
        "\\dfrac{g}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[g,L]",
        "\\dfrac{g}{g}\\,//\\,\\dfrac{\\ell}{\\ell}\\;[g,\\ell]"
      ]
    ]
  },
  {
    "type": "separator",
    "content": ""
  },
  {
    "type": "subtitle",
    "content": "4️⃣ Résultats F2 — Proportions phénotypiques"
  },
  {
    "type": "box",
    "content": "[G,L] = 9/16 = 56,25 %  |  [G,ℓ] = 3/16 = 18,75 %  |  [g,L] = 3/16 = 18,75 %  |  [g,ℓ] = 1/16 = 6,25 %",
    "color": "green"
  },
  {
    "type": "box",
    "content": "Les résultats théoriques (9:3:3:1) sont conformes aux résultats expérimentaux → gènes indépendants",
    "color": "orange"
  }
]
```

## Réponse brute LLM

```
# Analyse détaillée de ta réponse — Question BAC SVT 2025

## 🔍 Décorticage phrase par phrase

| Ta réponse | Correction officielle | Analyse |
|---|---|---|
| « Le croisement F1 × F1 donne la F2 » | ✅ F1 × F1 → F2 | **Correct.** Bonne identification du croisement |
| « Les parents F1 sont [G,L] × [G,L] » | ✅ F1 : [G,L] × [G,L] | **Correct.** Phénotypes bien notés |
| « Les génotypes sont GgLl × GgLl » | ✅ G//g L//ℓ × G//g L//ℓ | **❌ Erreur de notation.** Tu as écrit `GgLl` en notation linéaire. La correction officielle exige `\dfrac{G}{g}\,//\,\dfrac{L}{\ell}` (deux fractions avec double barre `//` pour gènes indépendants) |
| « Les gamètes sont GL, Gl, gL, gl » | ✅ ¼ G/L/ ; ¼ G/ℓ/ ; ¼ g/L/ ; ¼ g/ℓ/ | **❌ Notation incorrecte.** Tu as écrit les gamètes en lettres collées `GL`. Il faut `\dfrac{G}{}\,//\,\dfrac{L}{}` (un allèle au-dessus, vide en dessous) |
| « Je n'ai pas fait l'échiquier » | ❌ Échiquier 4×4 obligatoire | **❌ Erreur majeure.** La question dit explicitement « en vous aidant d'un échiquier de croisement ». Tu as perdu 0,5 pt ici |
| « Je sais qu'on obtient 9:3:3:1 » | ✅ [G,L]=9/16, [G,ℓ]=3/16, [g,L]=3/16, [g,ℓ]=1/16 | **Correct sur le fond** mais tu n'as pas détaillé les proportions en fractions |
| « qui prouve que les gènes sont indépendants » | ✅ Conforme aux résultats expérimentaux | **Correct.** Bonne conclusion |

## 📊 Bilan de ta réponse

| Critère | Points gagnés | Points perdus |
|---|---|---|
| Identification du croisement | ✅ 0,25 pt | — |
| Génotypes des parents | — | ❌ -0,25 pt (notation) |
| Gamètes | — | ❌ -0,25 pt (notation) |
| Échiquier de croisement | — | ❌ -0,50 pt (absent) |
| Proportions 9:3:3:1 | ✅ 0,25 pt | — |
| Conclusion (gènes indépendants) | ✅ 0,25 pt | — |
| **Total** | **0,75/1,5** | **-0,75 pt** |

## ✍️ Version modèle — ce qu'il fallait écrire sur ta copie BAC

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Interprétation chromosomique du 2e croisement","lines":[
  {"type":"subtitle","content":"1️⃣ Parents : F1 × F1"},
  {"type":"math","content":"\\text{Phénotypes : }\\;[G,L]\\;\\times\\;[G,L]"},
  {"type":"math","content":"\\text{Génotypes : }\\;\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;\\times\\;\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"2️⃣ Gamètes produits par chaque parent (équiprobables)"},
  {"type":"math","content":"\\text{Gamète 1 : }\\;\\dfrac{G}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)"},
  {"type":"math","content":"\\text{Gamète 2 : }\\;\\dfrac{G}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)"},
  {"type":"math","content":"\\text{Gamète 3 : }\\;\\dfrac{g}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)"},
  {"type":"math","content":"\\text{Gamète 4 : }\\;\\dfrac{g}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)"},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"3️⃣ Échiquier de fécondation F1 × F1"},
  {"type":"table","content":"","headers":[
    "♀ \\\\ ♂",
    "\\dfrac{G}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)",
    "\\dfrac{G}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
    "\\dfrac{g}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)",
    "\\dfrac{g}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)"
  ],"rows":[
    ["\\dfrac{G}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)",
     "\\dfrac{G}{G}\\,//\\,\\dfrac{L}{L}\\;[G,L]",
     "\\dfrac{G}{G}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{L}\\;[G,L]",
     "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]"],
    ["\\dfrac{G}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
     "\\dfrac{G}{G}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{G}{G}\\,//\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]",
     "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{G}{g}\\,//\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]"],
    ["\\dfrac{g}{}\\,//\\,\\dfrac{L}{}\\;(25\\,\\%)",
     "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{L}\\;[G,L]",
     "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{g}{g}\\,//\\,\\dfrac{L}{L}\\;[g,L]",
     "\\dfrac{g}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[g,L]"],
    ["\\dfrac{g}{}\\,//\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
     "\\dfrac{G}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{G}{g}\\,//\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]",
     "\\dfrac{g}{g}\\,//\\,\\dfrac{L}{\\ell}\\;[g,L]",
     "\\dfrac{g}{g}\\,//\\,\\dfrac{\\ell}{\\ell}\\;[g,\\ell]"]
  ]},
  {"type":"separator","content":""},
  {"type":"subtitle","content":"4️⃣ Résultats F2 — Proportions phénotypiques"},
  {"type":"box","content":"[G,L] = 9/16 = 56,25 %  |  [G,ℓ] = 3/16 = 18,75 %  |  [g,L] = 3/16 = 18,75 %  |  [g,ℓ] = 1/16 = 6,25 %","color":"green"},
  {"type":"box","content":"Les résultats théoriques (9:3:3:1) sont conformes aux résultats expérimentaux → gènes indépendants","color":"orange"}
]}}]}</ui>

## 🎯 Ce que tu dois retenir pour le BAC

| Point | Ta force | À améliorer |
|---|---|---|
| **Raisonnement** | ✅ Tu as compris la logique du dihybridisme | — |
| **Proportions** | ✅ Tu connais 9:3:3:1 | — |
| **Notation génotype** | ❌ `GgLl` → `\dfrac{G}{g}\,//\
…[tronqué]
```