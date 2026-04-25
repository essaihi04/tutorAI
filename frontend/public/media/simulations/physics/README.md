# Simulations Interactives - Physique

## Simulations requises pour Chapitre 1 : Ondes Mécaniques

### 1. onde_corde.html
**Description** : Simulation interactive d'une onde sur une corde
**Fonctionnalités** :
- Curseur pour ajuster l'amplitude de l'onde
- Curseur pour ajuster la fréquence
- Bouton play/pause
- Affichage de la célérité calculée
- Mode transversal/longitudinal

**Technologies** : HTML5 Canvas + JavaScript
**Bibliothèques recommandées** : p5.js ou Three.js

**Utilisation** : Phase d'exploration et application
**Trigger IA** : "essaie cette simulation", "manipule les paramètres de l'onde"

---

### 2. pendule.html
**Description** : Simulation d'un pendule simple (pour concepts d'oscillation)
**Fonctionnalités** :
- Curseur pour longueur du fil
- Curseur pour angle initial
- Affichage de la période
- Graphique position vs temps

**Utilisation** : Leçons sur oscillations mécaniques

---

## Ressources pour créer des simulations

### Option 1 : Utiliser PhET (Recommandé)
PhET propose des simulations scientifiques gratuites et open-source :
- https://phet.colorado.edu/en/simulations/filter?subjects=physics&type=html
- Télécharger les simulations HTML5
- Les intégrer directement dans le dossier

**Simulations pertinentes** :
- "Wave on a String" : https://phet.colorado.edu/en/simulations/wave-on-a-string
- "Waves Intro" : https://phet.colorado.edu/en/simulations/waves-intro

### Option 2 : Créer avec p5.js
Template de base pour onde sur corde :

```html
<!DOCTYPE html>
<html>
<head>
    <title>Onde sur une Corde</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.4.0/p5.js"></script>
</head>
<body>
    <script>
        let amplitude = 50;
        let frequency = 0.05;
        let phase = 0;
        
        function setup() {
            createCanvas(800, 400);
        }
        
        function draw() {
            background(240);
            stroke(59, 130, 246);
            strokeWeight(3);
            noFill();
            
            beginShape();
            for (let x = 0; x < width; x++) {
                let y = height/2 + amplitude * sin(frequency * x + phase);
                vertex(x, y);
            }
            endShape();
            
            phase += 0.1;
        }
    </script>
</body>
</html>
```

### Option 3 : Utiliser des simulations externes
Intégrer via iframe des simulations hébergées :
- GeoGebra : https://www.geogebra.org/
- Algodoo : https://www.algodoo.com/
- Walter Fendt Simulations : https://www.walter-fendt.de/html5/phen/

---

## Placeholder temporaire

En attendant les vraies simulations, créer un fichier HTML simple :

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Simulation - Onde sur Corde</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .container {
            background: white;
            padding: 40px;
            border-radius: 10px;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🌊 Simulation : Onde sur une Corde</h1>
        <p>Cette simulation sera disponible prochainement.</p>
        <p>En attendant, imagine une corde que tu agites verticalement...</p>
    </div>
</body>
</html>
```

---

## Format et intégration

- **Format** : HTML5 standalone (pas de dépendances externes si possible)
- **Responsive** : S'adapter à différentes tailles d'écran
- **Contrôles** : Simples et intuitifs (curseurs, boutons)
- **Bilingue** : Labels en français et arabe
- **Performance** : Optimisé pour navigateurs modernes
