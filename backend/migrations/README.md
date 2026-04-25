# Instructions pour appliquer les migrations Supabase

## Méthode 1: Via le Dashboard Supabase (Recommandé)

1. Allez sur https://supabase.com/dashboard
2. Sélectionnez votre projet `ldeifdnczkzgtxctjlel`
3. Dans le menu de gauche, cliquez sur **SQL Editor**
4. Cliquez sur **New Query**
5. Copiez-collez le contenu de `001_create_coaching_tables.sql`
6. Cliquez sur **Run** (ou Ctrl+Enter)
7. Répétez pour `002_create_libre_mode_tables.sql`

## Méthode 2: Via psql (si vous avez accès direct)

```bash
# Connection string depuis Supabase Dashboard → Settings → Database
psql "postgresql://postgres:[PASSWORD]@db.ldeifdnczkzgtxctjlel.supabase.co:5432/postgres"

# Puis exécutez:
\i 001_create_coaching_tables.sql
\i 002_create_libre_mode_tables.sql
```

## Vérification

Après avoir appliqué les migrations, vérifiez que les tables existent :

```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_name IN ('study_plans', 'study_plan_sessions', 'diagnostic_results', 'libre_conversations', 'libre_messages')
ORDER BY table_name;
```

Vous devriez voir 5 tables.

## Tables créées

### Migration 001 (Coaching Mode)
- `study_plans` - Plans d'étude personnalisés
- `study_plan_sessions` - Sessions individuelles du plan
- `diagnostic_results` - Résultats des évaluations
- Colonnes ajoutées à `student_profiles`:
  - `coaching_mode_active`
  - `current_plan_id`
  - `overall_progress`
  - `subject_progress`

### Migration 002 (Libre Mode)
- `libre_conversations` - Conversations en mode libre
- `libre_messages` - Messages individuels
