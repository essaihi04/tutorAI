-- Insérer des matières pour 2ème BAC Sciences Physiques BIOF
-- À exécuter dans le SQL Editor de Supabase Dashboard

-- Supprimer les matières existantes (si vous voulez recommencer)
-- DELETE FROM public.subjects;

-- Insérer les matières principales
INSERT INTO public.subjects (id, name_fr, name_ar, description_fr, description_ar, icon, color, order_index) VALUES
(
    gen_random_uuid(),
    'Mathématiques',
    'الرياضيات',
    'Mathématiques pour 2ème BAC Sciences Physiques BIOF',
    'الرياضيات للسنة الثانية باكالوريا علوم فيزيائية',
    '📐',
    '#3B82F6',
    1
),
(
    gen_random_uuid(),
    'Physique',
    'الفيزياء',
    'Physique pour 2ème BAC Sciences Physiques BIOF',
    'الفيزياء للسنة الثانية باكالوريا علوم فيزيائية',
    '⚛️',
    '#8B5CF6',
    2
),
(
    gen_random_uuid(),
    'Chimie',
    'الكيمياء',
    'Chimie pour 2ème BAC Sciences Physiques BIOF',
    'الكيمياء للسنة الثانية باكالوريا علوم فيزيائية',
    '🧪',
    '#10B981',
    3
),
(
    gen_random_uuid(),
    'Sciences de la Vie et de la Terre (SVT)',
    'علوم الحياة والأرض',
    'SVT pour 2ème BAC Sciences Physiques BIOF',
    'علوم الحياة والأرض للسنة الثانية باكالوريا علوم فيزيائية',
    '🌱',
    '#059669',
    4
),
(
    gen_random_uuid(),
    'Français',
    'الفرنسية',
    'Langue française pour 2ème BAC',
    'اللغة الفرنسية للسنة الثانية باكالوريا',
    '📚',
    '#F59E0B',
    5
),
(
    gen_random_uuid(),
    'Anglais',
    'الإنجليزية',
    'Langue anglaise pour 2ème BAC',
    'اللغة الإنجليزية للسنة الثانية باكالوريا',
    '🇬🇧',
    '#EF4444',
    6
),
(
    gen_random_uuid(),
    'Philosophie',
    'الفلسفة',
    'Philosophie pour 2ème BAC',
    'الفلسفة للسنة الثانية باكالوريا',
    '🤔',
    '#6366F1',
    7
),
(
    gen_random_uuid(),
    'Arabe',
    'العربية',
    'Langue arabe pour 2ème BAC',
    'اللغة العربية للسنة الثانية باكالوريا',
    '📖',
    '#EC4899',
    8
);

-- Vérifier les matières insérées
SELECT 
    name_fr,
    name_ar,
    icon,
    color,
    order_index
FROM public.subjects
ORDER BY order_index;
