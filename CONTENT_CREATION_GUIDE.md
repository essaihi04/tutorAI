# 📚 Guide de Création de Contenu Pédagogique

## Structure d'une Leçon

Chaque leçon suit le format JSON défini dans `database/seed_data/lessons/`.

### Template de Leçon

```json
{
  "title_fr": "Titre de la leçon en français",
  "title_ar": "عنوان الدرس بالعربية",
  "lesson_type": "theory",
  "duration_minutes": 50,
  "learning_objectives": [
    "Objectif 1",
    "Objectif 2",
    "Objectif 3"
  ],
  "content": {
    "phases": {
      "activation": {
        "duration_minutes": 5,
        "ai_prompts": [
          "Demande à l'étudiant ce qu'il sait déjà sur...",
          "Relie le concept à une expérience quotidienne"
        ],
        "media": []
      },
      "exploration": {
        "duration_minutes": 10,
        "scenario": {
          "title_fr": "Titre du scénario",
          "title_ar": "عنوان السيناريو",
          "description": "Description détaillée de la situation",
          "guiding_questions": [
            {
              "fr": "Question 1 en français?",
              "ar": "السؤال 1 بالعربية؟"
            }
          ],
          "discovery_path": [
            "Étape 1 de découverte",
            "Étape 2 de découverte"
          ]
        }
      },
      "explanation": {
        "duration_minutes": 15,
        "key_concepts": [
          {
            "term_fr": "Terme français",
            "term_ar": "المصطلح العربي",
            "definition_fr": "Définition en français",
            "definition_ar": "التعريف بالعربية"
          }
        ],
        "formulas": [
          {
            "name": "Nom de la formule",
            "expression": "F = m × a",
            "spoken": "F égale m fois a",
            "units": "N (Newton)",
            "variables": {
              "F": "Force en Newton",
              "m": "Masse en kg",
              "a": "Accélération en m/s²"
            }
          }
        ]
      },
      "application": {
        "duration_minutes": 15,
        "exercises": ["ex_phys_ch1_001", "ex_phys_ch1_002"]
      },
      "consolidation": {
        "duration_minutes": 5,
        "summary_points": [
          {
            "fr": "Point clé 1",
            "ar": "النقطة الأساسية 1"
          }
        ],
        "next_lesson": "Aperçu de la prochaine leçon",
        "schedule_review_days": 1
      }
    }
  },
  "media_resources": [
    {
      "type": "image",
      "url": "/media/images/subject/chapter/image.png",
      "caption": "Légende bilingue",
      "trigger": "regarde ce schéma",
      "phase": "explanation"
    }
  ]
}
```

---

## Structure d'un Exercice

Chaque exercice suit le format JSON défini dans `database/seed_data/exercises/`.

### Template Exercice QCM

```json
{
  "id": "ex_phys_ch1_001",
  "question_text_fr": "Question en français?",
  "question_text_ar": "السؤال بالعربية؟",
  "question_type": "qcm",
  "difficulty_tier": "beginner",
  "options": [
    {"id": "A", "text_fr": "Option A", "text_ar": "الخيار أ"},
    {"id": "B", "text_fr": "Option B", "text_ar": "الخيار ب"},
    {"id": "C", "text_fr": "Option C", "text_ar": "الخيار ج"},
    {"id": "D", "text_fr": "Option D", "text_ar": "الخيار د"}
  ],
  "correct_answer": "B",
  "explanation_fr": "Explication détaillée en français",
  "explanation_ar": "شرح مفصل بالعربية",
  "hints": [
    {"level": 1, "text_fr": "Indice 1", "text_ar": "تلميح 1"},
    {"level": 2, "text_fr": "Indice 2", "text_ar": "تلميح 2"}
  ],
  "estimated_time_seconds": 60,
  "order_index": 0
}
```

### Template Exercice Numérique

```json
{
  "id": "ex_phys_ch1_004",
  "question_text_fr": "Calcule la valeur de X sachant que...",
  "question_text_ar": "احسب قيمة X علما أن...",
  "question_type": "numeric",
  "difficulty_tier": "intermediate",
  "options": [],
  "correct_answer": 8.0,
  "explanation_fr": "Calcul: X = ...",
  "explanation_ar": "الحساب: X = ...",
  "hints": [
    {"level": 1, "text_fr": "Utilise la formule...", "text_ar": "استخدم العلاقة..."}
  ],
  "estimated_time_seconds": 120,
  "order_index": 3
}
```

---

## Bonnes Pratiques

### 1. Phase Activation (5 min)
**Objectif** : Activer les connaissances antérieures

✅ **À faire** :
- Poser des questions sur le vécu de l'étudiant
- Relier à des concepts déjà vus
- Créer un lien émotionnel avec le sujet

❌ **À éviter** :
- Donner de nouvelles informations
- Être trop théorique
- Ignorer les réponses de l'étudiant

**Exemple** :
```
"As-tu déjà observé les vagues à la plage? Que remarques-tu?"
"Te souviens-tu de ce qu'est l'énergie?"
```

---

### 2. Phase Exploration (10 min)
**Objectif** : Découverte guidée du concept

✅ **À faire** :
- Présenter une situation concrète
- Poser des questions Socratiques
- Laisser l'étudiant découvrir par lui-même
- Utiliser des médias visuels

❌ **À éviter** :
- Donner la réponse directement
- Être trop abstrait
- Ignorer les erreurs de l'étudiant

**Exemple de scénario** :
```
"Tu jettes une pierre dans un lac calme. Observe les cercles qui se forment.
Est-ce que l'eau se déplace avec les cercles, ou seulement la perturbation?"
```

---

### 3. Phase Explication (15 min)
**Objectif** : Structurer et formaliser le concept

✅ **À faire** :
- Définir les termes techniques (bilingue)
- Présenter les formules avec explications
- Utiliser des analogies
- Montrer des schémas/images
- Vérifier la compréhension

❌ **À éviter** :
- Être trop rapide
- Utiliser un jargon complexe
- Oublier les exemples concrets

**Structure recommandée** :
1. Définition du concept principal
2. Distinction entre types/catégories
3. Formules mathématiques (si applicable)
4. Exemples concrets
5. Vérification compréhension

---

### 4. Phase Application (15 min)
**Objectif** : Pratiquer et consolider

✅ **À faire** :
- Commencer par des exercices faciles
- Augmenter progressivement la difficulté
- Donner un feedback immédiat
- Identifier les misconceptions
- Féliciter les réussites

❌ **À éviter** :
- Exercices trop difficiles d'emblée
- Pas de feedback
- Ignorer les erreurs répétées

**Progression recommandée** :
1. QCM simple (concept de base)
2. QCM intermédiaire (application directe)
3. Numérique simple (calcul direct)
4. Numérique complexe (plusieurs étapes)
5. Problème ouvert (synthèse)

---

### 5. Phase Consolidation (5 min)
**Objectif** : Résumer et ancrer les apprentissages

✅ **À faire** :
- Résumer 3-5 points clés
- Demander à l'étudiant ce qu'il a retenu
- Faire le lien avec la suite
- Encourager et féliciter
- Programmer une révision

❌ **À éviter** :
- Introduire de nouveaux concepts
- Être trop long
- Oublier de féliciter

---

## Création de Médias

### Images
**Outils recommandés** :
- Canva (templates scientifiques)
- Excalidraw (schémas simples)
- Inkscape (vectoriel gratuit)
- DALL-E / Midjourney (génération IA)

**Spécifications** :
- Format : PNG (transparence) ou SVG (vectoriel)
- Résolution : 1200x800px minimum
- Poids : < 500KB
- Texte : Bilingue français/arabe
- Style : Clair, éducatif, contrasté

**Nommage** :
```
onde_transversale.png
celerite_schema.svg
pierre_eau_animation.gif
```

---

### Simulations
**Options** :
1. **PhET** (gratuit, open-source) : https://phet.colorado.edu/
2. **GeoGebra** : https://www.geogebra.org/
3. **p5.js** (créer soi-même)

**Spécifications** :
- Format : HTML5 standalone
- Responsive : S'adapter aux écrans
- Contrôles : Curseurs, boutons simples
- Bilingue : Labels FR/AR
- Performance : Optimisé navigateurs

---

### Vidéos
**Recommandations** :
- Durée : < 2 minutes
- Format : MP4 (H.264)
- Résolution : 1280x720 (720p)
- Sous-titres : Français + Arabe
- Poids : < 10MB

**Sources** :
- Créer avec OBS Studio (gratuit)
- Animations avec Manim (Python)
- Vidéos libres : YouTube Creative Commons

---

## Checklist Création de Leçon

### Avant de commencer
- [ ] Identifier le chapitre et le numéro de leçon
- [ ] Lister les objectifs d'apprentissage
- [ ] Définir la durée totale (généralement 50 min)
- [ ] Identifier les prérequis

### Phase Activation
- [ ] 2-3 questions d'accroche
- [ ] Lien avec connaissances antérieures
- [ ] Durée : 5 minutes

### Phase Exploration
- [ ] Scénario concret et engageant
- [ ] 3-5 questions guidées
- [ ] Chemin de découverte clair
- [ ] Durée : 10 minutes
- [ ] Média visuel (optionnel)

### Phase Explication
- [ ] 3-5 concepts clés définis (bilingue)
- [ ] Formules avec explications
- [ ] 2-3 médias visuels
- [ ] Durée : 15 minutes

### Phase Application
- [ ] 5+ exercices variés
- [ ] Progression facile → difficile
- [ ] Mix QCM (60%) + Numériques (40%)
- [ ] Durée : 15 minutes

### Phase Consolidation
- [ ] 3-5 points clés résumés
- [ ] Lien avec prochaine leçon
- [ ] Durée : 5 minutes

### Médias
- [ ] 3-5 images/schémas
- [ ] 1-2 simulations (optionnel)
- [ ] Triggers définis pour chaque média
- [ ] Fichiers créés et placés dans dossiers

### Exercices
- [ ] 5+ exercices créés
- [ ] IDs uniques (ex_phys_ch1_001)
- [ ] Explications détaillées
- [ ] Indices progressifs
- [ ] Fichier JSON créé

---

## Exemple Complet : Leçon Chimie

### Sujet : Cinétique Chimique - Vitesse de Réaction

**Fichier** : `database/seed_data/lessons/chim_ch1_l1.json`

```json
{
  "title_fr": "Introduction à la cinétique chimique",
  "title_ar": "مدخل إلى الحركية الكيميائية",
  "lesson_type": "theory",
  "duration_minutes": 50,
  "learning_objectives": [
    "Définir la vitesse d'une réaction chimique",
    "Identifier les facteurs influençant la vitesse",
    "Calculer une vitesse de réaction"
  ],
  "content": {
    "phases": {
      "activation": {
        "duration_minutes": 5,
        "ai_prompts": [
          "As-tu déjà observé du fer rouiller? Pourquoi certains métaux rouillent vite et d'autres lentement?",
          "Que se passe-t-il quand tu mets un comprimé effervescent dans l'eau?"
        ]
      },
      "exploration": {
        "duration_minutes": 10,
        "scenario": {
          "title_fr": "Le comprimé effervescent",
          "title_ar": "القرص الفوار",
          "description": "Tu as deux verres d'eau: un froid et un chaud. Tu mets un comprimé effervescent dans chaque verre.",
          "guiding_questions": [
            {"fr": "Dans quel verre le comprimé se dissout-il plus vite?", "ar": "في أي كأس يذوب القرص بسرعة أكبر؟"},
            {"fr": "Pourquoi penses-tu que c'est plus rapide?", "ar": "لماذا تعتقد أنه أسرع؟"}
          ]
        }
      },
      "explanation": {
        "duration_minutes": 15,
        "key_concepts": [
          {
            "term_fr": "Vitesse de réaction",
            "term_ar": "سرعة التفاعل",
            "definition_fr": "Variation de concentration d'un réactif ou produit par unité de temps",
            "definition_ar": "تغير تركيز متفاعل أو ناتج في وحدة الزمن"
          }
        ],
        "formulas": [
          {
            "name": "Vitesse moyenne",
            "expression": "v = Δ[A] / Δt",
            "spoken": "v égale delta A sur delta t",
            "units": "mol/L/s"
          }
        ]
      },
      "application": {
        "duration_minutes": 15,
        "exercises": ["ex_chim_ch1_001", "ex_chim_ch1_002"]
      },
      "consolidation": {
        "duration_minutes": 5,
        "summary_points": [
          {"fr": "La vitesse mesure la rapidité d'une réaction", "ar": "السرعة تقيس سرعة التفاعل"}
        ]
      }
    }
  },
  "media_resources": [
    {
      "type": "image",
      "url": "/media/images/chemistry/cinetique_schema.png",
      "caption": "Graphique concentration vs temps",
      "trigger": "regarde ce graphique",
      "phase": "explanation"
    }
  ]
}
```

---

## Ressources Utiles

### Contenu Pédagogique
- **Programme BAC Marocain** : https://men.gov.ma/
- **Khan Academy** (inspiration) : https://fr.khanacademy.org/
- **AlloSchool Maroc** : https://www.alloschool.com/

### Médias Scientifiques
- **PhET Simulations** : https://phet.colorado.edu/
- **Wikimedia Commons** : https://commons.wikimedia.org/
- **OpenStax** : https://openstax.org/

### Outils de Création
- **Canva** : https://www.canva.com/
- **Excalidraw** : https://excalidraw.com/
- **GeoGebra** : https://www.geogebra.org/
- **p5.js** : https://p5js.org/

---

## Support

Pour toute question sur la création de contenu :
1. Consulter les exemples existants dans `database/seed_data/lessons/`
2. Utiliser les templates fournis
3. Tester avec l'application avant de finaliser

**Bon courage dans la création de contenu ! 📚**
