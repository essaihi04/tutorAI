-- Remplace la ressource PNG annoncée comme « 3D » par la scène Three.js
-- versionnée. Le PNG reste lié comme repli accessible si WebGL est absent.
UPDATE public.lesson_resources
SET resource_type = 'simulation',
    description = 'Modèle 3D manipulable : rotation, zoom et mise en évidence des membranes, crêtes et matrice.',
    trigger_text = 'observe et manipule mitochondrie 3d',
    concepts = jsonb_build_array('mitochondrie', 'crêtes', 'matrice', 'ADN mitochondrial'),
    metadata = COALESCE(metadata, '{}'::jsonb) || jsonb_build_object(
        'visual_kind', 'scientific',
        'scientific', jsonb_build_object(
            'engine', 'three',
            'model', 'mitochondrion',
            'title', 'Mitochondrie 3D interactive',
            'description', 'Double membrane, crêtes, matrice et ADN mitochondrial circulaire.',
            'autoplay', true,
            'labels', true,
            'focus', 'all'
        ),
        'caption', 'Modèle pédagogique manipulable',
        'source_type', 'versioned_scientific_model',
        'interaction', 'rotate_zoom_focus',
        'library_status', 'published'
    )
WHERE file_path = '/media/images/svt/ch1_consommation_matiere_organique/lesson_1_liberation_energie/respiration/mitochondrie_3d_sans_legendes.png'
   OR title = 'Mitochondrie 3D à observer';
