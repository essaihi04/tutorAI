# Guide du Tableau Blanc 3D avec Structures Biologiques

## 🎨 Nouvelles Fonctionnalités

### 1. Écriture Manuscrite
- Tous les textes utilisent automatiquement une **police manuscrite** (Caveat)
- Effet d'écriture naturelle comme un vrai professeur au tableau
- Léger tremblement pour un rendu authentique

### 2. Structures Biologiques en 3D Simulé

#### `mitochondria` - Mitochondrie
Dessine une mitochondrie avec cristae et effet 3D
```json
{
  "type": "mitochondria",
  "x": 100,
  "y": 100,
  "width": 120,
  "height": 60,
  "color": "orange",
  "fill": "orange",
  "label": "Mitochondrie"
}
```
**Caractéristiques:**
- Membrane externe avec dégradé radial
- Cristae (membrane interne) avec lignes ondulées
- Effet de profondeur 3D

#### `cell` - Cellule
Dessine une cellule complète avec membrane bicouche
```json
{
  "type": "cell",
  "x": 300,
  "y": 200,
  "radius": 100,
  "color": "blue",
  "label": "Cellule eucaryote"
}
```
**Caractéristiques:**
- Membrane plasmique double couche
- Dégradé pour effet de volume
- Cytoplasme translucide

#### `nucleus` - Noyau
Dessine un noyau avec enveloppe nucléaire et chromatine
```json
{
  "type": "nucleus",
  "x": 300,
  "y": 200,
  "radius": 50,
  "color": "purple",
  "label": "Noyau"
}
```
**Caractéristiques:**
- Dégradé sphérique 3D (violet foncé → clair)
- Enveloppe nucléaire double
- Chromatine visible à l'intérieur

#### `dna` - ADN Double Hélice
Dessine une double hélice d'ADN
```json
{
  "type": "dna",
  "x": 400,
  "y": 100,
  "width": 40,
  "height": 120,
  "color": "red",
  "label": "ADN"
}
```
**Caractéristiques:**
- Deux brins hélicoïdaux (bleu et rouge)
- Paires de bases connectées
- Animation en spirale

#### `membrane` - Membrane Plasmique
Dessine une bicouche phospholipidique détaillée
```json
{
  "type": "membrane",
  "x": 100,
  "y": 50,
  "width": 200,
  "height": 30,
  "color": "pink",
  "label": "Membrane plasmique"
}
```
**Caractéristiques:**
- Têtes hydrophiles (cercles rouges)
- Queues hydrophobes (lignes cyan)
- Bicouche phospholipidique réaliste

### 3. Effets Visuels Améliorés

#### Ombres et Profondeur
- Toutes les formes ont des ombres subtiles
- Dégradés radiaux pour effet 3D
- Épaisseur de trait augmentée pour meilleure visibilité

#### Flèches Améliorées
- Têtes de flèches remplies
- Labels avec fond semi-transparent
- Meilleure lisibilité

#### Rectangles et Cercles
- Coins arrondis pour les rectangles
- Remplissage avec transparence (20%)
- Contours avec effet main levée

## 📝 Exemple Complet : Cellule Eucaryote

```json
[{
  "title": "Structure de la Cellule Eucaryote",
  "elements": [
    {"id":"title","type":"text","x":150,"y":15,"text":"LA CELLULE EUCARYOTE","color":"black","fontSize":20},
    {"id":"cell","type":"cell","x":300,"y":200,"radius":130,"color":"blue","label":"Cellule"},
    {"id":"nucleus","type":"nucleus","x":300,"y":200,"radius":50,"color":"purple","label":"Noyau"},
    {"id":"mito1","type":"mitochondria","x":400,"y":140,"width":90,"height":45,"color":"orange","fill":"orange","label":"Mitochondrie"},
    {"id":"mito2","type":"mitochondria","x":200,"y":250,"width":80,"height":40,"color":"orange","fill":"orange","label":""},
    {"id":"dna","type":"dna","x":480,"y":80,"width":35,"height":100,"color":"red","label":"ADN"},
    {"id":"membrane","type":"membrane","x":120,"y":40,"width":150,"height":28,"color":"pink","label":"Membrane"},
    {"id":"arrow1","type":"arrow","points":[{"x":350,"y":200},{"x":400,"y":160}],"color":"green","label":"Production ATP"},
    {"id":"note","type":"text","x":50,"y":350,"text":"La mitochondrie produit l'énergie (ATP)","color":"black","fontSize":14}
  ]
}]
```

## 🎯 Conseils d'Utilisation

### Pour l'AI
1. **Utilise les types biologiques** pour les structures cellulaires au lieu de cercles/rectangles basiques
2. **Combine plusieurs types** : cellule + noyau + mitochondries + ADN
3. **Ajoute des annotations** avec type "text" en police manuscrite
4. **Utilise des couleurs cohérentes** : orange pour mitochondries, purple pour noyau, blue pour cellules

### Dimensions Recommandées
- **Cellule**: radius 80-150
- **Noyau**: radius 40-60
- **Mitochondrie**: width 70-120, height 35-60
- **ADN**: width 30-40, height 80-120
- **Membrane**: width 100-200, height 25-35

## 🔄 Migration depuis l'Ancien Système

**Avant:**
```json
{"type":"circle","x":300,"y":200,"radius":100,"color":"blue","label":"Cellule"}
```

**Maintenant:**
```json
{"type":"cell","x":300,"y":200,"radius":100,"color":"blue","label":"Cellule"}
```

Les anciens types (rect, circle, arrow, text) fonctionnent toujours, mais les nouveaux types biologiques offrent un rendu bien plus réaliste et professionnel !

## 🎨 Palette de Couleurs Biologiques

- **Cellules**: blue, cyan
- **Noyau**: purple
- **Mitochondries**: orange
- **ADN**: red, pink
- **Membranes**: pink
- **Annotations**: black
- **Processus/Flux**: green, red (selon production/consommation)

---

**Note**: Le système charge automatiquement les polices manuscrites (Caveat, Patrick Hand) au démarrage du tableau blanc.
