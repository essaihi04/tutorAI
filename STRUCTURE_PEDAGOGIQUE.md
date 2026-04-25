# 📚 Structure Pédagogique Complète - AI Tutor BAC

## 🎯 Vue d'ensemble

Voici la structure complète que nous avons définie pour le système d'apprentissage adaptatif.

## 📊 Hiérarchie du Contenu

```
Matière (Subject)
  └── Chapitre (Chapter)
      └── Leçon (Lesson)
          ├── Contenu théorique
          ├── Ressources média (images, simulations, vidéos)
          ├── Situations pédagogiques (scénarios d'apprentissage)
          ├── Exercices (avec 3 niveaux de difficulté)
          └── Évaluations
```

## 1️⃣ Matières (Subjects)

**Structure:**
- Nom en français et arabe
- Description bilingue
- Icône et couleur
- Ordre d'affichage

**Matières actuelles:**
- 📐 **Mathématiques** (الرياضيات)
- ⚛️ **Physique** (الفيزياء)
- 🧪 **Chimie** (الكيمياء)
- 🌱 **SVT** (علوم الحياة والأرض)

## 2️⃣ Chapitres (Chapters)

**Chaque chapitre contient:**
- Numéro de chapitre
- Titre bilingue (FR/AR)
- Description détaillée
- **Niveau de difficulté:** `beginner`, `intermediate`, `advanced`
- Durée estimée en heures
- Ordre dans la matière

**Exemple pour Mathématiques:**
```
Chapitre 1: Limites et Continuité
Chapitre 2: Dérivabilité
Chapitre 3: Étude de fonctions
Chapitre 4: Primitives et Intégrales
...
```

## 3️⃣ Leçons (Lessons)

**Types de leçons:**
- 📖 **Theory** - Cours théorique
- 🔧 **Practice** - Exercices pratiques
- 🧪 **Lab** - Travaux pratiques/simulations
- 📝 **Revision** - Révision

**Contenu de chaque leçon (JSONB):**
```json
{
  "sections": [
    {
      "title": "Introduction",
      "content": "Texte du cours...",
      "type": "text"
    },
    {
      "title": "Définition",
      "content": "...",
      "type": "definition",
      "examples": [...]
    },
    {
      "title": "Démonstration",
      "content": "...",
      "type": "proof",
      "steps": [...]
    }
  ],
  "key_concepts": ["concept1", "concept2"],
  "formulas": [
    {
      "name": "Formule de dérivée",
      "latex": "f'(x) = \\lim_{h \\to 0} \\frac{f(x+h) - f(x)}{h}",
      "explanation": "..."
    }
  ]
}
```

**Ressources média (media_resources JSONB):**
```json
[
  {
    "type": "image",
    "url": "https://...",
    "caption": "Graphique de la fonction",
    "alt": "Description"
  },
  {
    "type": "simulation",
    "url": "https://phet.colorado.edu/...",
    "title": "Simulation interactive",
    "description": "Explorez les limites de fonctions"
  },
  {
    "type": "video",
    "url": "https://...",
    "duration": 300,
    "title": "Explication vidéo"
  },
  {
    "type": "audio",
    "url": "https://...",
    "transcript": "Transcription audio...",
    "language": "fr"
  }
]
```

**Objectifs d'apprentissage:**
```json
[
  "Comprendre la notion de limite",
  "Calculer des limites simples",
  "Appliquer les théorèmes sur les limites"
]
```

## 4️⃣ Situations Pédagogiques (Pedagogical Situations)

**Scénarios d'apprentissage interactifs avec l'IA:**

```json
{
  "scenario_title_fr": "Découverte des limites par l'expérimentation",
  "scenario_title_ar": "اكتشاف النهايات من خلال التجريب",
  "scenario_description": {
    "context": "L'étudiant explore une fonction graphiquement",
    "goal": "Comprendre intuitivement la notion de limite",
    "approach": "Socratique - Questions guidées"
  },
  "context_prompt": "Tu vas explorer la fonction f(x) = 1/x. Que remarques-tu quand x s'approche de 0?",
  "expected_student_path": [
    {
      "phase": "observation",
      "ai_prompts": [
        "Regarde le graphique. Que se passe-t-il quand x devient très petit?",
        "Et si x est négatif et s'approche de 0?"
      ]
    },
    {
      "phase": "hypothesis",
      "ai_prompts": [
        "D'après tes observations, peux-tu formuler une hypothèse?",
        "Pourquoi penses-tu que la fonction se comporte ainsi?"
      ]
    },
    {
      "phase": "formalization",
      "ai_prompts": [
        "Comment pourrions-nous écrire cela mathématiquement?",
        "C'est ce qu'on appelle une limite. Veux-tu voir la notation?"
      ]
    }
  ],
  "difficulty_tier": "beginner"
}
```

## 5️⃣ Exercices (Exercises)

**3 Niveaux de difficulté:**
- 🟢 **Beginner** (Faible) - Exercices d'application directe
- 🟡 **Intermediate** (Moyen) - Exercices de réflexion
- 🔴 **Advanced** (Avancé) - Exercices de synthèse

**Types de questions:**
- `qcm` - Questions à choix multiples
- `numeric` - Réponse numérique
- `open` - Question ouverte
- `true_false` - Vrai/Faux

**Structure d'un exercice:**
```json
{
  "question_text_fr": "Calculer la limite de f(x) = (x² - 1)/(x - 1) quand x → 1",
  "question_text_ar": "احسب نهاية الدالة...",
  "question_type": "numeric",
  "difficulty_tier": "intermediate",
  "options": null,
  "correct_answer": {
    "value": 2,
    "tolerance": 0.01,
    "unit": null
  },
  "explanation_fr": "On factorise le numérateur: x² - 1 = (x-1)(x+1). Donc f(x) = (x-1)(x+1)/(x-1) = x+1 pour x ≠ 1. La limite est donc 1+1 = 2.",
  "explanation_ar": "...",
  "hints": [
    {
      "level": 1,
      "text": "Essaie de factoriser le numérateur"
    },
    {
      "level": 2,
      "text": "x² - 1 = (x-1)(x+1)"
    },
    {
      "level": 3,
      "text": "Simplifie la fraction avant de calculer la limite"
    }
  ],
  "estimated_time_seconds": 180
}
```

## 6️⃣ Interaction IA (AI Prompts)

**Modes d'enseignement:**
- 🤔 **Socratique** - Questions guidées pour faire découvrir
- 📢 **Directif** - Explications directes et structurées
- 🤝 **Collaboratif** - Résolution de problèmes ensemble
- 🎯 **Autonome** - Ressources et exercices en autonomie

**Prompts IA stockés dans `ai_prompts` table:**
```json
{
  "prompt_type": "explanation",
  "phase": "introduction",
  "template_text": "Bonjour {student_name}! Aujourd'hui nous allons explorer {topic}. As-tu déjà entendu parler de ce concept?",
  "variables": ["student_name", "topic"],
  "language": "fr",
  "teaching_mode": "Socratique"
}
```

## 7️⃣ Sessions d'Apprentissage

**Suivi de progression:**
```json
{
  "student_id": "uuid",
  "lesson_id": "uuid",
  "start_time": "2026-03-07T10:00:00Z",
  "end_time": "2026-03-07T10:45:00Z",
  "duration_minutes": 45,
  "phases_completed": [
    "introduction",
    "theory",
    "practice",
    "evaluation"
  ],
  "final_phase": "evaluation",
  "session_notes": "Étudiant a bien compris les limites finies"
}
```

## 8️⃣ Logs de Conversation

**Enregistrement des interactions:**
```json
{
  "session_id": "uuid",
  "speaker": "ai",
  "message_text": "Excellent! Tu as bien compris. Maintenant, essayons un exercice plus difficile.",
  "phase": "practice",
  "timestamp": "2026-03-07T10:30:00Z"
}
```

## 9️⃣ Profil Étudiant Adaptatif

**Données de personnalisation:**
```json
{
  "proficiency_level": "intermediate",
  "learning_style": "Socratique",
  "strengths": ["algèbre", "calcul"],
  "weaknesses": ["géométrie", "démonstrations"],
  "total_study_time_minutes": 1200,
  "sessions_completed": 24,
  "exercises_completed": 156,
  "average_score": 0.78
}
```

## 🔟 Répétition Espacée

**Système de révision intelligent:**
```json
{
  "student_id": "uuid",
  "lesson_id": "uuid",
  "next_review_date": "2026-03-14",
  "repetition_number": 3,
  "ease_factor": 2.5,
  "interval_days": 7,
  "last_reviewed": "2026-03-07T10:00:00Z"
}
```

## 🎨 Fonctionnalités Interactives

### Audio et Écrit
- ✅ **Texte bilingue** (FR/AR) pour tout le contenu
- ✅ **Audio** pour les explications (text-to-speech)
- ✅ **Transcriptions** pour l'accessibilité
- ✅ **Chat vocal** avec l'IA (speech-to-text)

### Média Enrichi
- 🖼️ **Images** explicatives
- 🎬 **Vidéos** de démonstration
- 🔬 **Simulations** interactives (PhET, GeoGebra)
- 📊 **Graphiques** dynamiques

### Adaptation
- 📈 **3 rythmes** prédéfinis (faible/moyen/avancé)
- 🎯 **Exercices adaptés** au niveau
- 💡 **Indices progressifs** (3 niveaux)
- 🔄 **Révisions espacées** automatiques

## 📝 Exemple Complet: Chapitre de Mathématiques

```
Matière: Mathématiques
  └── Chapitre 1: Limites et Continuité
      ├── Leçon 1.1: Introduction aux limites (Theory)
      │   ├── Contenu: Définition intuitive, exemples graphiques
      │   ├── Média: Graphiques interactifs, simulation GeoGebra
      │   ├── Situation: Découverte par l'expérimentation
      │   └── Exercices: 5 QCM (beginner), 3 numériques (intermediate)
      │
      ├── Leçon 1.2: Calcul de limites (Practice)
      │   ├── Contenu: Techniques de calcul, théorèmes
      │   ├── Média: Vidéos de résolution, images de méthodes
      │   ├── Situation: Résolution guidée de problèmes
      │   └── Exercices: 10 exercices (tous niveaux)
      │
      ├── Leçon 1.3: Limites et asymptotes (Theory)
      │   ├── Contenu: Asymptotes verticales, horizontales
      │   ├── Média: Graphiques animés, simulations
      │   ├── Situation: Analyse de fonctions
      │   └── Exercices: 8 exercices (intermediate/advanced)
      │
      └── Leçon 1.4: Évaluation du chapitre (Revision)
          ├── Contenu: Synthèse du chapitre
          ├── Exercices: 15 exercices variés (tous niveaux)
          └── Évaluation: Test adaptatif
```

## 🚀 Prochaines Étapes

Pour implémenter cette structure:

1. **Créer les chapitres** pour chaque matière
2. **Ajouter les leçons** avec contenu riche
3. **Intégrer les ressources média** (images, simulations)
4. **Créer les exercices** pour les 3 niveaux
5. **Configurer les prompts IA** pour l'interaction
6. **Tester le parcours** d'apprentissage complet

Cette structure permet un apprentissage **adaptatif**, **interactif** et **multimodal** (audio/écrit) avec l'IA ! 🎓
