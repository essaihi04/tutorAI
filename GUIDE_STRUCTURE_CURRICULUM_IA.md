# Guide d'Utilisation - Structure Curriculum SVT 2Bac PC pour l'IA

## 📚 Fichiers créés

### 1. `backend/data/curriculum_svt_2bac_pc.yaml`
Structure complète du programme officiel SVT 2Bac PC du Maroc, optimisée pour l'agent IA.

## 🎯 Structure du Programme

### Vue d'ensemble
- **4 chapitres** répartis sur 2 semestres
- **66 heures** de cours total
- **Examen National** : 3h, 20 points

### Répartition par chapitre

| Chapitre | Semestre | Heures | Poids Examen | Difficulté |
|----------|----------|--------|--------------|------------|
| Ch1: Consommation matière organique | 1 | 18h | 25% | Intermédiaire |
| Ch2: Information génétique | 1 | 20h | 30% | Avancé |
| Ch3: Utilisation matières | 2 | 12h | 20% | Débutant |
| Ch4: Phénomènes géologiques | 2 | 16h | 25% | Avancé |

## 📖 Détail des Chapitres

### Chapitre 1: Consommation de la matière organique
**Concepts clés:**
- Glycolyse (2 ATP)
- Respiration cellulaire (36-38 ATP)
- Fermentation
- Contraction musculaire

**Leçons:**
1. **Libération de l'énergie** (10h)
   - Glycolyse → Pyruvate
   - Cycle de Krebs → NADH, FADH2
   - Chaîne respiratoire → ATP
   - Comparaison respiration/fermentation

2. **Rôle du muscle** (8h)
   - Structure sarcomère
   - Mécanisme actine-myosine
   - Sources d'énergie selon effort

**Stratégies IA:**
- **Activation:** "Pourquoi la fatigue après un effort?"
- **Exploration:** Simulation respiration avec/sans O2
- **Explication:** Schémas des 3 étapes métaboliques
- **Application:** Calculs de bilans énergétiques

### Chapitre 2: Information génétique
**Concepts clés:**
- ADN (structure Watson-Crick)
- Réplication semi-conservative
- Transcription ADN→ARNm
- Traduction ARNm→Protéine
- Mitose (2 cellules 2n)
- Méiose (4 cellules n)
- Brassage génétique

**Leçons:**
1. **Notion information génétique** (10h)
   - Structure ADN
   - Réplication
   - Mitose

2. **Expression matériel génétique** (6h)
   - Transcription
   - Traduction
   - Code génétique

3. **Transfert reproduction** (4h)
   - Méiose
   - Brassage intra/interchromosomique

**Erreurs fréquentes à corriger:**
- ❌ Confusion mitose/méiose
  - ✅ Tableau: 2 vs 4 cellules, 2n vs n
- ❌ Glycolyse nécessite O2
  - ✅ Première étape commune = anaérobie
- ❌ Transcription = Traduction
  - ✅ Transcription=copie, Traduction=changement langue

### Chapitre 3: Utilisation des matières
**Concepts clés:**
- Ordures ménagères et recyclage
- Pollution (air, eau, sol)
- Énergies renouvelables
- Radioactivité

**Leçons:**
1. Ordures ménagères
2. Pollution des milieux
3. Matières radioactives

### Chapitre 4: Phénomènes géologiques
**Concepts clés:**
- Tectonique des plaques
- Subduction et collision
- Métamorphisme
- Granitisation

**Leçons:**
1. Chaînes de montagnes et tectonique
2. Métamorphisme
3. Granitisation

## 🤖 Utilisation par l'Agent IA

### 1. Chargement du curriculum

```python
import yaml

with open('backend/data/curriculum_svt_2bac_pc.yaml', 'r', encoding='utf-8') as f:
    curriculum = yaml.safe_load(f)

# Accéder aux chapitres
chapters = curriculum['chapters']

# Trouver un chapitre spécifique
ch1 = next(ch for ch in chapters if ch['id'] == 'ch1_consommation_matiere')
```

### 2. Adapter l'enseignement selon la phase

```python
def get_teaching_strategy(phase):
    strategies = curriculum['ai_teaching_strategies']['phases']
    return strategies[phase]

# Exemple pour phase exploration
exploration = get_teaching_strategy('exploration')
# {
#   'duration': '15-20 min',
#   'actions': ['Simulation interactive', 'Observation guidée', ...]
# }
```

### 3. Détecter et corriger les erreurs

```python
common_errors = curriculum['ai_teaching_strategies']['common_errors']

for error_info in common_errors:
    if detect_error_in_student_response(student_text, error_info['error']):
        correction = error_info['correction']
        # Appliquer la stratégie de correction
```

### 4. Sélectionner le vocabulaire prioritaire

```python
vocab = curriculum['ai_teaching_strategies']['vocabulary_priority']
# ['ATP', 'Mitochondrie', 'Glycolyse', 'ADN/ARN', ...]

# Définir ces termes lors de la première utilisation
```

## 🎓 Phases d'Apprentissage

### 1. Activation (5-10 min)
**Objectif:** Activer connaissances antérieures

**Actions IA:**
- Poser question ouverte quotidienne
- Rappeler prérequis
- Présenter situation-problème

**Exemple:**
> "Avant de commencer, dis-moi: que se passe-t-il dans tes muscles quand tu cours?"

### 2. Exploration (15-20 min)
**Objectif:** Découvrir par manipulation

**Actions IA:**
- Proposer simulation interactive
- Guider observation
- Encourager hypothèses

**Exemple:**
> "Utilise cette simulation. Clique d'abord 'Avec O2', observe le résultat. Puis essaie 'Sans O2'. Que remarques-tu?"

### 3. Explication (20-30 min)
**Objectif:** Structurer les connaissances

**Actions IA:**
- Formaliser concepts
- Introduire vocabulaire scientifique
- Créer schémas

**Exemple:**
> "Maintenant, résumons: avec O2, combien d'ATP? Sans O2? Pourquoi cette différence?"

### 4. Application (15-20 min)
**Objectif:** Appliquer dans contextes variés

**Actions IA:**
- Exercices progressifs
- Situations nouvelles
- Problèmes concrets

**Exemple:**
> "Un coureur de marathon utilise quelle voie métabolique? Et un sprinter?"

### 5. Consolidation (10-15 min)
**Objectif:** Renforcer et évaluer

**Actions IA:**
- Synthèse points clés
- QCM rapide
- Identifier lacunes

**Exemple:**
> "Récapitule en 3 points ce que tu as appris aujourd'hui."

## 📊 Structure Examen National

### Composition
- **QCM:** 4 points (8 questions)
- **QROC:** 6 points (3 questions)
- **Exercices:** 10 points (2 exercices de synthèse)

### Compétences évaluées
1. Restitution de connaissances
2. Analyse de documents
3. Raisonnement scientifique
4. Schématisation
5. Résolution de problèmes

## 🔧 Intégration Backend

### Modifier `session_handler.py`

```python
import yaml

class SessionHandler:
    def __init__(self, ...):
        # Charger curriculum
        with open('backend/data/curriculum_svt_2bac_pc.yaml', 'r', encoding='utf-8') as f:
            self.curriculum = yaml.safe_load(f)
    
    def _build_system_prompt_with_curriculum(self, lesson_id):
        # Trouver la leçon dans le curriculum
        lesson = self._find_lesson(lesson_id)
        
        if lesson:
            # Enrichir le prompt avec:
            # - Objectifs de la leçon
            # - Concepts clés
            # - Stratégies pédagogiques
            # - Erreurs fréquentes à surveiller
            
            curriculum_context = f"""
LEÇON ACTUELLE: {lesson['title']}

OBJECTIFS:
{chr(10).join('- ' + obj for obj in lesson['objectives'])}

CONCEPTS CLÉS À ABORDER:
{chr(10).join('- ' + concept for concept in lesson.get('key_concepts', []))}

STRATÉGIES PÉDAGOGIQUES:
Phase {self.current_phase}:
{self._get_phase_strategy(self.current_phase)}

ERREURS FRÉQUENTES À SURVEILLER:
{self._get_common_errors_for_lesson(lesson_id)}
"""
            return curriculum_context
        return ""
    
    def _find_lesson(self, lesson_id):
        for chapter in self.curriculum['chapters']:
            for lesson in chapter.get('lessons', []):
                if lesson['id'] == lesson_id:
                    return lesson
        return None
```

## 💡 Exemples d'Utilisation

### Exemple 1: Démarrer une leçon

```python
# L'IA détecte qu'on commence "Libération de l'énergie"
lesson = curriculum.find_lesson('lesson_1_1')

# Phase activation
activation_prompt = f"""
Tu enseignes: {lesson['title']}

Objectif principal: {lesson['objectives'][0]}

Commence par la phase ACTIVATION:
- Pose une question ouverte liée au quotidien
- Exemple suggéré: "Pourquoi ressens-tu de la fatigue après un effort intense?"
- Rappelle les prérequis: structure cellule, notion métabolisme
"""
```

### Exemple 2: Corriger une erreur

```python
# L'étudiant dit: "La glycolyse a besoin d'oxygène"
error_detected = "Glycolyse nécessite O2"

correction = curriculum.find_error_correction(error_detected)
# → "Première étape commune, donc anaérobie"

ai_response = f"""
Attention, petite confusion! La glycolyse est en fait la première étape 
de TOUTES les voies de dégradation du glucose. Elle ne peut donc pas 
dépendre de l'oxygène, sinon la fermentation ne pourrait pas exister!

La glycolyse est ANAÉROBIE (sans O2).
C'est après, selon la présence d'O2, qu'on a:
- Avec O2 → Respiration (cycle de Krebs + chaîne respiratoire)
- Sans O2 → Fermentation
"""
```

### Exemple 3: Adapter selon difficulté

```python
lesson_difficulty = lesson['difficulty']  # 'intermediate'

if student_proficiency == 'beginner' and lesson_difficulty == 'advanced':
    # Simplifier l'approche
    ai_note = "Leçon avancée pour étudiant débutant → décomposer en étapes simples"
elif student_proficiency == 'advanced' and lesson_difficulty == 'beginner':
    # Approfondir
    ai_note = "Leçon facile pour étudiant avancé → ajouter des approfondissements"
```

## 📝 Prochaines Étapes

### 1. Intégrer au backend
- [ ] Charger YAML au démarrage de `SessionHandler`
- [ ] Enrichir `build_system_prompt` avec contexte curriculum
- [ ] Ajouter détection erreurs fréquentes
- [ ] Adapter stratégies selon phase

### 2. Créer ressources pédagogiques
- [ ] Simulations pour chaque chapitre
- [ ] Schémas fonctionnels
- [ ] Exercices progressifs
- [ ] QCM par leçon

### 3. Tester et affiner
- [ ] Tester avec étudiants réels
- [ ] Ajuster stratégies selon feedback
- [ ] Enrichir erreurs fréquentes
- [ ] Optimiser durées par phase

## 🎯 Avantages de cette Structure

### Pour l'IA
✅ Contexte pédagogique complet
✅ Stratégies adaptées par phase
✅ Détection erreurs automatique
✅ Vocabulaire prioritaire défini
✅ Objectifs clairs par leçon

### Pour l'Étudiant
✅ Progression structurée
✅ Correction ciblée des erreurs
✅ Adaptation au niveau
✅ Ressources appropriées
✅ Préparation examen optimale

### Pour le Développeur
✅ Structure YAML lisible
✅ Facile à maintenir
✅ Extensible (autres matières)
✅ Séparation données/code
✅ Versionnable (Git)
