# Configuration du Stockage Supabase pour les Ressources Pédagogiques

## Problème résolu
Les images uploadées dans les ressources pédagogiques n'apparaissaient pas après rechargement car elles n'étaient pas stockées dans Supabase Storage.

## Solution : Créer un bucket Supabase Storage

### Étape 1 : Exécuter le SQL dans Supabase

1. Connectez-vous à votre **Dashboard Supabase**
2. Allez dans **SQL Editor**
3. Copiez et exécutez le code SQL suivant :

```sql
-- Create storage bucket for pedagogical resources
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'pedagogical-resources',
    'pedagogical-resources',
    true,
    52428800, -- 50MB limit
    ARRAY['image/jpeg', 'image/png', 'image/gif', 'image/svg+xml', 'image/webp', 'video/mp4', 'video/webm', 'video/ogg']
)
ON CONFLICT (id) DO NOTHING;

-- Policy: Allow authenticated users to upload files
CREATE POLICY "Authenticated users can upload resources"
ON storage.objects FOR INSERT
TO authenticated
WITH CHECK (bucket_id = 'pedagogical-resources');

-- Policy: Allow public read access to all files
CREATE POLICY "Public read access for resources"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'pedagogical-resources');

-- Policy: Allow authenticated users to update their uploads
CREATE POLICY "Authenticated users can update resources"
ON storage.objects FOR UPDATE
TO authenticated
USING (bucket_id = 'pedagogical-resources');

-- Policy: Allow authenticated users to delete files
CREATE POLICY "Authenticated users can delete resources"
ON storage.objects FOR DELETE
TO authenticated
USING (bucket_id = 'pedagogical-resources');
```

### Étape 2 : Vérifier la création du bucket

1. Allez dans **Storage** dans le menu Supabase
2. Vous devriez voir le bucket **pedagogical-resources**
3. Le bucket doit être **public** (icône globe visible)

### Étape 3 : Redémarrer le backend

```bash
cd backend
# Arrêtez le serveur si il tourne (Ctrl+C)
# Redémarrez-le
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Comment ça fonctionne maintenant

### Upload d'images
1. L'utilisateur sélectionne une image dans l'interface admin
2. L'image est uploadée vers **Supabase Storage** (bucket `pedagogical-resources`)
3. Le chemin de stockage est : `images/lesson_XXXXXXXX/uuid.ext`
4. L'URL publique est sauvegardée dans la base de données
5. Format URL : `https://xxx.supabase.co/storage/v1/object/public/pedagogical-resources/images/lesson_xxx/file.jpg`

### Récupération des images
- Les images sont accessibles publiquement via leur URL
- Pas besoin d'authentification pour afficher les images
- Les URLs sont permanentes tant que le fichier existe

### Suppression
- Quand vous supprimez une ressource, le fichier est automatiquement supprimé du bucket Supabase

## Structure des fichiers dans le bucket

```
pedagogical-resources/
├── images/
│   ├── lesson_abc12345/
│   │   ├── uuid1.jpg
│   │   ├── uuid2.png
│   │   └── ...
│   └── lesson_def67890/
│       └── ...
└── videos/
    ├── lesson_abc12345/
    │   └── uuid.mp4
    └── ...
```

## Logs de débogage

Après l'upload, vérifiez les logs du backend pour confirmer :

```
[UPLOAD] Starting upload - type: image, lesson_id: xxx, filename: xxx
[UPLOAD] Uploading to Supabase Storage: images/lesson_xxx/uuid.ext
[UPLOAD] File uploaded successfully to Supabase Storage
[UPLOAD] Public URL: https://xxx.supabase.co/storage/v1/object/public/...
[CREATE RESOURCE] Creating resource: xxx
[CREATE RESOURCE] Success! Created resource with ID: xxx
```

## Troubleshooting

### Erreur : "Bucket not found"
→ Exécutez le SQL de création du bucket (Étape 1)

### Erreur : "Permission denied"
→ Vérifiez que les politiques RLS sont bien créées (Étape 1)

### Les images ne s'affichent pas
→ Vérifiez que le bucket est **public** dans Supabase Dashboard

### Erreur d'upload
→ Vérifiez les logs du backend pour voir l'erreur exacte
→ Vérifiez que le type MIME du fichier est autorisé
