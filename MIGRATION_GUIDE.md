# Guide de Migration des Ressources vers Supabase Storage

## Problème

Certaines ressources pédagogiques utilisent encore des chemins locaux obsolètes comme :
```
/media/images/svt/ch2_energie_cellulaire/glycolyse_schema.png
```

Ces fichiers n'existent plus et doivent être migrés vers Supabase Storage.

## Solution

### 1. Identifier les ressources obsolètes

Exécutez ce SQL dans Supabase pour voir toutes les ressources avec des chemins locaux :

```sql
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
```

### 2. Re-uploader les ressources

Pour chaque ressource obsolète :

1. **Allez dans l'interface Admin** (`/admin-resources`)
2. **Trouvez la ressource** dans la liste
3. **Cliquez sur "Modifier"**
4. **Uploadez à nouveau l'image** via le champ de fichier
5. **Sauvegardez**

L'image sera automatiquement uploadée vers Supabase Storage avec une URL comme :
```
https://xxx.supabase.co/storage/v1/object/public/pedagogical-resources/images/lesson_xxx/uuid.jpg
```

### 3. Ou supprimer les ressources obsolètes

Si vous ne voulez pas conserver ces ressources, vous pouvez les supprimer :

```sql
-- ATTENTION: Cette commande est DESTRUCTIVE et IRRÉVERSIBLE
-- Vérifiez d'abord avec la requête SELECT ci-dessus
DELETE FROM lesson_resources WHERE file_path LIKE '/media/%';
```

## Comportement actuel

Le frontend gère maintenant les deux types de chemins :

### ✅ URLs Supabase (nouvelles ressources)
- S'affichent correctement
- Format : `https://xxx.supabase.co/storage/v1/object/public/pedagogical-resources/...`

### ⚠️ Chemins locaux (anciennes ressources)
- Affichent un message d'erreur explicite
- Message : "Cette ressource utilise un ancien chemin local"
- Suggestion : "Veuillez re-uploader cette image via l'interface admin"

## Statistiques

Pour voir la répartition des ressources par type de stockage :

```sql
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
```

## Prévention

Pour éviter ce problème à l'avenir :

1. ✅ Le backend upload automatiquement vers Supabase Storage
2. ✅ Les URLs sont nettoyées (pas de `?` à la fin)
3. ✅ Le frontend gère les erreurs de chargement
4. ✅ Messages d'erreur explicites pour guider les utilisateurs

## Fichiers modifiés

- `backend/app/api/resources.py` - Upload vers Supabase Storage
- `frontend/src/components/session/MediaViewer.tsx` - Gestion des deux types de chemins
- `database/migrations/create_storage_bucket.sql` - Création du bucket
- `database/migrations/update_legacy_resources.sql` - Script d'identification
