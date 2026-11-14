# Les dessins du cahier — format `cahier_figures`

14 novembre 2026. Le cahier (« 📓 À écrire dans le cahier ») porte, sous le texte, une courbe, un schéma ou un croquis
légendé quand la notion se dessine. Rendu : `frontend/src/components/course/FigureCahier.tsx` (SVG à la craie).

## Où

- **Diapo** : `activities[].slides[].concentration.cahier_figures` — bulle du cahier de la diapo (0 ou 1 figure, 2 au plus).
- **Bloc** : `seances[].blocs[].cahier_figures` — étape cahier de fin de bloc (1 ou 2 figures au plus : tout doit tenir
  dans l'écran sans défiler). En pratique : les figures des diapos du bloc, dans l'ordre de `slide_ids`, en gardant les 2
  plus utiles.

## Une figure

```json
{
  "type": "courbe",               // courbe | schema | croquis | variations
  "titre": "Charge du condensateur",
  "legende": "u_C monte vers E ; à t = τ, u_C = 0,63·E.",
  "axes": {                       // repère (courbe) : flèches, noms, unités, graduations
    "x": { "min": 0, "max": 5, "nom": "t", "unite": "ms", "graduations": [[1, "τ"], [5, "5τ"]] },
    "y": { "min": 0, "max": 6.5, "nom": "u_C", "unite": "V", "graduations": [[6, "E"], [3.78, "0,63E"]] }
  },
  "elements": [
    { "f": "courbe", "expr": "6*(1-exp(-x/1))", "couleur": "cyan" },
    { "f": "repere", "y": 6, "t": "asymptote u_C = E" },
    { "f": "repere", "x": 1, "y": 3.78 },
    { "f": "ligne", "pts": [[0,0],[1,6]], "trait": "pointille", "couleur": "jaune" }
  ]
}
```

Sans axes (schéma, croquis) : `"cadre": { "l": 10, "h": 6 }` — coordonnées de (0,0) en bas à gauche à (l,h) en haut à
droite ; le dessin garde les proportions l × h. `ratio` (hauteur/largeur) change la forme d'un repère (défaut 0,6).

### Éléments (`elements[]`, coordonnées des données)

| `f` | champs | usage |
|---|---|---|
| `courbe` | `expr` (en x), `de`, `a`, `couleur`, `trait`, `texte`, `texte_x`, `pos` | y = f(x) ; fonctions `exp ln log sqrt sin cos tan abs atan floor sign`, `pi`, `^` ; coupée hors du cadre (asymptotes) |
| `ligne` | `pts` [[x,y]…], `ferme`, `lisse`, `fleche`, `remplir`, `epais`, `trait` | polyligne ; `lisse` = courbe passant par les points (croquis) |
| `fleche` | `de`, `a`, `texte`, `pos` | flèche (vecteur, sens, transformation) |
| `cote` | `de`, `a`, `t`, `pos` | double flèche de mesure (λ, T, d) |
| `cercle` | `c`, `r` (unités de x), `remplir` | |
| `ellipse` | `c`, `rx`, `ry` | |
| `rect` | `de`, `a`, `remplir`, `arrondi` | |
| `arc` | `c`, `r`, `de`, `a` (degrés), `fleche` | angle, cercle trigonométrique |
| `texte` | `at`, `t`, `taille` (petit/normal/grand), `ancre` (gauche/centre/droite) | légende posée sur le dessin |
| `point` | `at`, `t`, `pos`, `creux` | point nommé |
| `repere` | `x` et/ou `y`, `t` | pointillés vers les axes (les deux) ; asymptote verticale (x seul) ou horizontale (y seul) — seulement avec `axes` |

`couleur` : `blanc` (défaut), `cyan` (défaut des courbes), `jaune`, `vert`, `orange`, `rose`, `rouge`, `bleu`, `violet`,
`faible`. `trait` : `plein` | `pointille`. `pos` : `n s e o ne no se so centre`.
Textes : `u_C`, `x_{M}`, `10^{-3}` s'écrivent en indice / exposant ; préférez les caractères Unicode (², ⁺, →, ∞, τ, λ).

### Tableau de variations (`type: "variations"`)

```json
{ "type": "variations", "titre": "Variations de f(x) = x·e^{−x}",
  "variations": { "x": ["−∞", "1", "+∞"], "signe": ["+", "−"], "zeros": [1],
    "f": [ { "v": "−∞", "niveau": "bas" }, { "v": "1/e", "niveau": "haut" }, { "v": "0", "niveau": "bas" } ],
    "nom_derivee": "f′(x)", "nom_f": "f" } }
```
`barre: true` sur une valeur de `f` : valeur interdite (double barre). Au milieu du tableau, `v` s'écrit à gauche de la
barre et `v2` (au niveau `niveau2`) à droite : `{ "v": "+∞", "niveau": "haut", "barre": true, "v2": "−∞", "niveau2": "bas" }`.

## Règles

- Un dessin seulement là où la notion se dessine (courbe d'évolution, forme d'un objet, schéma d'un montage, d'une
  structure, axe des pH, cercle, tableau de variations) ; pas un dessin partout.
- L'essentiel : 3 à 8 éléments ; axes nommés **avec leur unité** ; les valeurs du cours ; une légende d'une phrase qui
  dit ce qu'il faut voir.
- Juste scientifiquement : allure, asymptotes, points remarquables, sens des flèches.
- Vérifier : `python backend/scripts/verifier_figures_cahier.py backend/data/courses/<fichier>.json`.
