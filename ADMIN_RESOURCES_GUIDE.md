# Guide d'utilisation - Interface Admin Ressources

## Accès

Depuis le **Dashboard**, clique sur le bouton **⚙️ Gestion des ressources** en haut à droite.

URL directe : `http://localhost:5173/admin/resources`

## Fonctionnalités

### 7 types de ressources gérables

1. **📸 Images** - Schémas, illustrations, graphiques
2. **🎥 Vidéos** - Vidéos explicatives courtes
3. **🔬 Simulations** - Simulations HTML interactives
4. **✏️ Exercices** - Exercices d'application
5. **📝 Évaluations** - Évaluations rapides
6. **📋 Examens** - Extraits d'examens nationaux
7. **📖 Définitions** - Fiches de définition

### Ajouter une ressource

1. Sélectionne le **type de ressource** dans les onglets
2. Clique sur **+ Ajouter [Type]**
3. Remplis le formulaire :
   - **Leçon** : choisis la leçon concernée
   - **Section** : nom de la section (ex: "La glycolyse")
   - **Titre** : titre de la ressource
   - **Description** : description pédagogique
   - **Phase** : activation, exploration, explication, application, consolidation
   - **Niveau** : débutant, intermédiaire, avancé
   - **Texte déclencheur** : phrase que l'agent peut utiliser (ex: "regarde ce schéma glycolyse")
   - **Concepts** : mots-clés séparés par des virgules (ex: "glycolyse, ATP, cytoplasme")

4. **Pour les images et vidéos** :
   - Soit **upload un fichier** directement
   - Soit **spécifie un chemin manuel** si le fichier existe déjà

5. **Pour les simulations** :
   - Spécifie le chemin du fichier `index.html`

6. **Pour les examens** :
   - Spécifie le chemin du fichier `.md`

7. Clique sur **Ajouter**

### Modifier une ressource

1. Dans la liste des ressources, clique sur **Modifier**
2. Modifie les champs souhaités
3. Clique sur **Modifier**

### Supprimer une ressource

1. Dans la liste des ressources, clique sur **Supprimer**
2. Confirme la suppression

## Backend API

### Endpoints disponibles

- `GET /api/v1/admin/resources?type={type}&lesson_id={lesson_id}` - Liste des ressources
- `GET /api/v1/admin/resources/{id}` - Détail d'une ressource
- `POST /api/v1/admin/resources` - Créer une ressource
- `PUT /api/v1/admin/resources/{id}` - Modifier une ressource
- `DELETE /api/v1/admin/resources/{id}` - Supprimer une ressource
- `POST /api/v1/admin/upload` - Upload de fichier (image/vidéo)
- `GET /api/v1/admin/lessons` - Liste des leçons

### Upload de fichiers

Les fichiers uploadés sont automatiquement placés dans :
- Images : `/media/images/svt/ch1_consommation_matiere_organique/lesson_{id}/`
- Vidéos : `/media/videos/svt/ch1_consommation_matiere_organique/lesson_{id}/`

## Structure de la base de données

Table : `lesson_resources`

Colonnes principales :
- `id` : UUID
- `lesson_id` : UUID (référence à `lessons`)
- `section_title` : VARCHAR(200)
- `resource_type` : VARCHAR(30)
- `title` : VARCHAR(200)
- `description` : TEXT
- `file_path` : TEXT
- `trigger_text` : VARCHAR(200)
- `phase` : VARCHAR(30)
- `difficulty_tier` : difficulty_level
- `concepts` : JSONB
- `metadata` : JSONB
- `order_index` : INTEGER

## Comment l'agent utilise ces ressources

L'agent peut maintenant :

1. **Lire les métadonnées** de chaque ressource
2. **Filtrer par** :
   - concept (ex: "glycolyse")
   - phase pédagogique (ex: "explanation")
   - niveau (ex: "beginner")
   - type (ex: "image")
3. **Choisir automatiquement** la ressource la plus pertinente selon :
   - la question de l'élève
   - le concept abordé
   - la phase de la leçon
   - le niveau de difficulté
4. **Afficher** la ressource avec la commande appropriée :
   - `MONTRER_IMAGE:{file_path}`
   - `SIMULATION:{file_path}`
   - `EXERCICE:{exercise_id}`

## Exemple de flux

**Élève** : "Je ne comprends pas la glycolyse"

**Agent** :
1. Détecte le concept : `glycolyse`
2. Cherche dans `lesson_resources` :
   - `concepts` contient `glycolyse`
   - `phase` = `explanation`
   - `resource_type` = `image`
3. Trouve : "Schéma de la glycolyse"
4. Répond : "Regarde ce schéma pour mieux comprendre. MONTRER_IMAGE:/media/images/svt/.../schema_glycolyse.svg"
5. Le frontend affiche l'image automatiquement

## Prochaines étapes recommandées

1. **Remplir la base** avec toutes les ressources du chapitre 1
2. **Brancher l'agent** pour qu'il lise `lesson_resources` automatiquement
3. **Tester** le flux complet avec un élève
4. **Étendre** aux autres chapitres SVT
5. **Créer** une interface similaire pour Physique et Chimie

## Fichiers créés

### Frontend
- `frontend/src/pages/AdminResources.tsx` - Interface admin complète

### Backend
- `backend/app/api/resources.py` - Routes API CRUD + upload

### Base de données
- `database/migrations/add_lesson_resources.sql` - Table dédiée
- `database/schema.sql` - Schéma mis à jour

### Médias
- `frontend/public/media/images/svt/ch1_consommation_matiere_organique/` - Images SVG exemples
- `frontend/public/media/simulations/svt/ch1_consommation_matiere_organique/` - Simulations HTML
- `frontend/public/media/exams/svt/ch1_consommation_matiere_organique/` - Examens MD

## Support

Pour toute question ou problème, vérifie :
1. Les logs backend dans le terminal
2. La console navigateur (F12)
3. Que la table `lesson_resources` existe bien dans Supabase
4. Que les chemins de fichiers sont corrects
