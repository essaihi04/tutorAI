# Test : Échiquier de croisement — SVT 2025 Normale (Q20)

_Généré le 2026-05-01 12:55:11_


**Temps LLM** : 29.1s — **Réponse** : 6797 chars

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
| 10 | Génotypes en notation diploïde (\overline{} = 2 barres) | ✅ PASS | 32 génotype(s) diploïde(s) détecté(s) |
| 11 | Aucun génotype à une seule barre dans les cellules d'échiquier | ✅ PASS | OK |

**Score : 11/11** — 🎉 TOUT VERT


## Contenu des boards (après sanitizer)


### Board 1 — « Échiquier de croisement F1 × F1 »

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
        "\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{L}}\\;[G,L]",
        "\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{L}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]"
      ],
      [
        "\\dfrac{G}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
        "\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
        "\\dfrac{G}{\\overline{G}}\\,\\dfrac{\\ell}{\\overline{\\ell}}\\;[G,\\ell]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{\\ell}{\\overline{\\ell}}\\;[G,\\ell]"
      ],
      [
        "\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{L}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
        "\\dfrac{g}{\\overline{g}}\\,\\dfrac{L}{\\overline{L}}\\;[g,L]",
        "\\dfrac{g}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[g,L]"
      ],
      [
        "\\dfrac{g}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
        "\\dfrac{G}{\\overline{g}}\\,\\dfrac{\\ell}{\\overline{\\ell}}\\;[G,\\ell]",
        "\\dfrac{g}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[g,L]",
        "\\dfrac{g}{\\overline{g}}\\,\\dfrac{\\ell}{\\overline{\\ell}}\\;[g,\\ell]"
      ]
    ]
  },
  {
    "type": "box",
    "content": "Résultats F2 : [G,L] = 9/16 ; [G, ℓ] = 3/16 ; [g,L] = 3/16 ; [g, ℓ] = 1/16.",
    "color": "green"
  }
]
```

## Réponse brute LLM

```
Excellent ! C'est une excellente démarche. Décortiquer sa propre copie pour comprendre où on a perdu des points, c'est la clé pour progresser. On va analyser ta réponse phrase par phrase, la comparer à la correction officielle, et je vais te montrer la version modèle à rédiger sur ta copie.

### Analyse détaillée de ta réponse

**Ta phrase :** « Le croisement F1 × F1 donne la F2. Les parents F1 sont [G,L] × [G,L]. Les génotypes sont GgLl × GgLl. »

*   **✅ Points forts :** Tu as parfaitement identifié le type de croisement (F1 × F1), les phénotypes des parents `[G,L]` et leur génotype hétérozygote pour les deux gènes (`GgLl`). C'est la base correcte.
*   **❌ Erreur / Oubli :** La notation `GgLl` est une notation abrégée, acceptable pour un brouillon, mais **pas pour la rédaction finale au BAC**. La correction officielle exige la **notation chromosomique** avec les deux barres horizontales pour représenter les paires de chromosomes homologues : `\dfrac{G}{\overline{g}}\,\dfrac{L}{\overline{\ell}}`. C'est un point de méthode important.

**Ta phrase :** « Les gamètes sont GL, Gl, gL, gl. »

*   **✅ Points forts :** Tu as listé les 4 types de gamètes possibles pour un double hétérozygote à gènes indépendants. C'est juste.
*   **❌ Erreur / Oubli :** Encore une fois, la notation n'est pas celle attendue. Il faut écrire les gamètes avec **une seule barre** (car haploïde) : `\dfrac{G}{}\dfrac{L}{}`. De plus, tu n'as pas mentionné la **proportion** de chaque gamète (1/4 ou 25%). Dans un échiquier, c'est essentiel pour le calcul des probabilités.

**Ta phrase :** « Je n'ai pas fait l'échiquier mais je sais qu'on obtient la proportion 9 : 3 : 3 : 1 qui prouve que les gènes sont indépendants. »

*   **✅ Points forts :** Tu connais la proportion phénotypique caractéristique du dihybridisme à gènes indépendants (9:3:3:1). C'est une bonne connaissance théorique.
*   **❌ Erreur / Oubli :** C'est l'erreur la plus grave. **La question demande explicitement de « s'aider d'un échiquier de croisement ».** Ne pas le faire, c'est perdre la moitié des points (0.75 pt sur 1.5). L'échiquier n'est pas un détail, c'est l'outil de démonstration obligatoire. Tu as donné la conclusion, mais pas la démonstration qui y mène.

### Bilan de ta réponse

*   **Note :** 0.75 / 1.5
*   **Points forts :** Bonne compréhension du concept de dihybridisme, identification correcte des génotypes parentaux et de la proportion finale.
*   **Points à améliorer :**
    1.  **Rédaction :** Utiliser la notation chromosomique officielle (`\dfrac{G}{\overline{g}}` au lieu de `Gg`).
    2.  **Précision :** Indiquer les proportions des gamètes (1/4).
    3.  **Méthode :** **Toujours construire l'échiquier de croisement** quand la question le demande. C'est la preuve de ton raisonnement.

---

### Version modèle pour la copie BAC

Voici comment tu aurais dû rédiger ta réponse pour obtenir la note maximale. Lis attentivement la structure et la notation.

**Interprétation chromosomique du deuxième croisement :**

*   **Parents (F1) :** `[G,L]` × `[G,L]`
*   **Génotypes :** `\dfrac{G}{\overline{g}}\,\dfrac{L}{\overline{\ell}}` × `\dfrac{G}{\overline{g}}\,\dfrac{L}{\overline{\ell}}`
*   **Gamètes :**
    *   `\dfrac{G}{}\dfrac{L}{}` (1/4)
    *   `\dfrac{G}{}\dfrac{\ell}{}` (1/4)
    *   `\dfrac{g}{}\dfrac{L}{}` (1/4)
    *   `\dfrac{g}{}\dfrac{\ell}{}` (1/4)

*   **Échiquier de fécondation :**

<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Échiquier de croisement F1 × F1","lines":[
  {"type":"table","content":"","headers":[
    "♀ \\\\ ♂",
    "\\dfrac{G}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
    "\\dfrac{G}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
    "\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
    "\\dfrac{g}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)"
  ],"rows":[
    ["\\dfrac{G}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
     "\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{L}}\\;[G,L]",
     "\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
     "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{L}}\\;[G,L]",
     "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]"],
    ["\\dfrac{G}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
     "\\dfrac{G}{\\overline{G}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
     "\\dfrac{G}{\\overline{G}}\\,\\dfrac{\\ell}{\\overline{\\ell}}\\;[G,\\ell]",
     "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
     "\\dfrac{G}{\\overline{g}}\\,\\dfrac{\\ell}{\\overline{\\ell}}\\;[G,\\ell]"],
    ["\\dfrac{g}{}\\,\\dfrac{L}{}\\;(25\\,\\%)",
     "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{L}}\\;[G,L]",
     "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
     "\\dfrac{g}{\\overline{g}}\\,\\dfrac{L}{\\overline{L}}\\;[g,L]",
     "\\dfrac{g}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[g,L]"],
    ["\\dfrac{g}{}\\,\\dfrac{\\ell}{}\\;(25\\,\\%)",
     "\\dfrac{G}{\\overline{g}}\\,\\dfrac{L}{\\overline{\\ell}}\\;[G,L]",
     "\\dfrac{G}{\\overline{g}}\\,\\dfra
…[tronqué]
```