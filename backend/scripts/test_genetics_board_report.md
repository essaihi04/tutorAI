# Test : Échiquier de croisement — SVT 2025 Normale (Q20)

_Généré le 2026-05-01 12:34:04_


**Temps LLM** : 22.1s — **Réponse** : 5188 chars

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

**Score : 9/9** — 🎉 TOUT VERT


## Contenu des boards (après sanitizer)


### Board 1 — « Échiquier de croisement F1 × F1 (Gènes indépendants) »

```json
[
  {
    "type": "table",
    "content": "",
    "headers": [
      "♀ \\\\ ♂",
      "\\dfrac{G}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
      "\\dfrac{G}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
      "\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
      "\\dfrac{g}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)"
    ],
    "rows": [
      [
        "\\dfrac{G}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
        "\\dfrac{G}{G}\\,\\dfrac{L}{L}\\;[G,L]",
        "\\dfrac{G}{G}\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{G}{g}\\,\\dfrac{L}{L}\\;[G,L]",
        "\\dfrac{G}{g}\\,\\dfrac{L}{\\ell}\\;[G,L]"
      ],
      [
        "\\dfrac{G}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
        "\\dfrac{G}{G}\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{G}{G}\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]",
        "\\dfrac{G}{g}\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{G}{g}\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]"
      ],
      [
        "\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
        "\\dfrac{G}{g}\\,\\dfrac{L}{L}\\;[G,L]",
        "\\dfrac{G}{g}\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{g}{g}\\,\\dfrac{L}{L}\\;[g,L]",
        "\\dfrac{g}{g}\\,\\dfrac{L}{\\ell}\\;[g,L]"
      ],
      [
        "\\dfrac{g}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
        "\\dfrac{G}{g}\\,\\dfrac{L}{\\ell}\\;[G,L]",
        "\\dfrac{G}{g}\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]",
        "\\dfrac{g}{g}\\,\\dfrac{L}{\\ell}\\;[g,L]",
        "\\dfrac{g}{g}\\,\\dfrac{\\ell}{\\ell}\\;[g,\\ell]"
      ]
    ]
  },
  {
    "type": "box",
    "content": "Résultats F2 : [G,L] = 9/16 ; [G,ℓ] = 3/16 ; [g,L] = 3/16 ; [g,ℓ] = 1/16. Soit une proportion 9:3:3:1.",
    "color": "orange"
  }
]
```

## Réponse brute LLM

```
Excellent ! Décortiquons ta réponse en détail pour que tu comprennes exactement ce qui a été bien fait et ce qui a manqué pour obtenir la note maximale. C'est une excellente méthode pour progresser.

### Analyse détaillée de ta réponse

**1. Points forts (ce qui t'a rapporté 0.75 pt) :**

*   **Identification correcte du croisement :** Tu as bien écrit « Le croisement F1 × F1 donne la F2. Les parents F1 sont [G,L] × [G,L]. » C'est la base.
*   **Génotypes corrects :** Tu as noté « Les génotypes sont GgLl × GgLl ». C'est juste.
*   **Gamètes corrects :** Tu as listé « Les gamètes sont GL, Gl, gL, gl ». C'est parfait.
*   **Conclusion juste :** Tu as déduit « on obtient la proportion 9 : 3 : 3 : 1 qui prouve que les gènes sont indépendants. » C'est la conclusion attendue.

**2. Points faibles (ce qui t'a coûté 0.75 pt) :**

*   **Absence de l'échiquier de croisement :** La question était explicite : « on vous aidant d'un échiquier de croisement ». C'est l'outil central de l'interprétation chromosomique. En ne le faisant pas, tu as perdu la moitié des points.
*   **Notation non conforme au BAC :** Tu as utilisé `GgLl` (notation dite "en ligne"). La correction officielle exige une **représentation chromosomique** avec des fractions LaTeX `\dfrac{G}{g}\;\dfrac{L}{\ell}` pour montrer les deux paires de chromosomes homologues. C'est un détail visuel très important pour le correcteur.
*   **Proportions des gamètes manquantes :** Tu as listé les gamètes mais sans indiquer leurs proportions (¼ ou 25% chacun). Dans un échiquier, c'est essentiel pour calculer les résultats finaux.

### Version Modèle (rédigée comme sur une copie BAC)

Voici comment tu aurais dû rédiger ta réponse pour obtenir la note maximale. Lis attentivement la structure et la notation.

**Interprétation chromosomique du deuxième croisement :**

**1. Parents :** F1 [G,L] × F1 [G,L]
**2. Génotypes :** `\dfrac{G}{g}\;\dfrac{L}{\ell}` × `\dfrac{G}{g}\;\dfrac{L}{\ell}`
**3. Gamètes :** Chaque parent produit 4 types de gamètes équiprobables (car gènes indépendants) :
    *   `\dfrac{G}{}\;\dfrac{L}{}` (25%)
    *   `\dfrac{G}{}\;\dfrac{\ell}{}` (25%)
    *   `\dfrac{g}{}\;\dfrac{L}{}` (25%)
    *   `\dfrac{g}{}\;\dfrac{\ell}{}` (25%)

**4. Échiquier de croisement (Fécondation) :**

Voici l'échiquier complet, comme tu dois le présenter.

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Échiquier de croisement F1 × F1 (Gènes indépendants)","lines":[
  {"type":"table","content":"","headers":[
    "♀ \\\\ ♂",
    "\\dfrac{G}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
    "\\dfrac{G}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
    "\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
    "\\dfrac{g}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)"
  ],"rows":[
    ["\\dfrac{G}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
     "\\dfrac{G}{G}\\,\\dfrac{L}{L}\\;[G,L]",
     "\\dfrac{G}{G}\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{G}{g}\\,\\dfrac{L}{L}\\;[G,L]",
     "\\dfrac{G}{g}\\,\\dfrac{L}{\\ell}\\;[G,L]"],
    ["\\dfrac{G}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
     "\\dfrac{G}{G}\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{G}{G}\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]",
     "\\dfrac{G}{g}\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{G}{g}\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]"],
    ["\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
     "\\dfrac{G}{g}\\,\\dfrac{L}{L}\\;[G,L]",
     "\\dfrac{G}{g}\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{g}{g}\\,\\dfrac{L}{L}\\;[g,L]",
     "\\dfrac{g}{g}\\,\\dfrac{L}{\\ell}\\;[g,L]"],
    ["\\dfrac{g}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
     "\\dfrac{G}{g}\\,\\dfrac{L}{\\ell}\\;[G,L]",
     "\\dfrac{G}{g}\\,\\dfrac{\\ell}{\\ell}\\;[G,\\ell]",
     "\\dfrac{g}{g}\\,\\dfrac{L}{\\ell}\\;[g,L]",
     "\\dfrac{g}{g}\\,\\dfrac{\\ell}{\\ell}\\;[g,\\ell]"]
  ]},
  {"type":"box","content":"Résultats F2 : [G,L] = 9/16 ; [G,ℓ] = 3/16 ; [g,L] = 3/16 ; [g,ℓ] = 1/16. Soit une proportion 9:3:3:1.","color":"orange"}
]}}]}</ui>

**5. Conclusion :** Les résultats théoriques (9:3:3:1) sont conformes aux résultats expérimentaux, ce qui confirme que les gènes responsables de la couleur (G/g) et de l'aspect (L/ℓ) du pelage sont **indépendants** (portés par deux paires de chromosomes différentes).

### 💡 Leçon à retenir pour le BAC

*   **Lis la question deux fois :** Si on te demande un échiquier, tu DOIS le dessiner. C'est non-négociable.
*   **Sois un "robot" de la notation :** Utilise TOUJOURS la notation `\dfrac{}{}` pour les génotypes. C'est la signature du BAC SVT.
*   **Structure ta réponse :** Parents → Génotypes → Gamètes (avec %) → Échiquier → Résultats. C'est une recette qui marche à tous les coups.

Maintenant que tu as vu la version modèle, je te propose de t'entraîner sur un cas similaire pour être sûr d'avoir bien compris.

<suggestions>[
  {"label":"✅ Oui, c'est clair !","prompt":"Oui, j'ai compris la différence. Je veux un autre exercice pour m'entraîner.","icon":"✅"},
  {"label":"❓ Pourquoi ¼ pour chaque gamète ?","prompt":"Je ne comprends pas pourquoi chaque g
…[tronqué]
```