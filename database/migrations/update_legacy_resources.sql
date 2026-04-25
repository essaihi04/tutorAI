-- Script pour identifier et mettre à jour les ressources avec des chemins locaux obsolètes
-- Ces ressources doivent être re-uploadées vers Supabase Storage

-- 1. Lister toutes les ressources avec des chemins locaux
SELECT 
    id,
    title,
    resource_type,
    file_path,
    lesson_id,
    created_at
FROM lesson_resources
WHERE file_path LIKE '/media/%'
ORDER BY created_at DESC;

-- 2. Option A: Marquer ces ressources comme obsolètes (ajouter un flag dans metadata)
-- UPDATE lesson_resources
-- SET metadata = jsonb_set(
--     COALESCE(metadata, '{}'::jsonb),
--     '{legacy_path}',
--     'true'::jsonb
-- )
-- WHERE file_path LIKE '/media/%';

-- 3. Option B: Supprimer les ressources obsolètes (ATTENTION: destructif!)
-- Décommentez seulement si vous voulez supprimer définitivement
-- DELETE FROM lesson_resources WHERE file_path LIKE '/media/%';

-- 4. Compter les ressources par type de chemin
SELECT 
    CASE 
        WHEN file_path LIKE '/media/%' THEN 'Local (obsolète)'
        WHEN file_path LIKE '%supabase%' THEN 'Supabase Storage'
        ELSE 'Autre'
    END as storage_type,
    COUNT(*) as count
FROM lesson_resources
WHERE file_path IS NOT NULL
GROUP BY storage_type;
