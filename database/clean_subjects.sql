-- Nettoyer la table subjects et garder seulement Math, Physique, Chimie et SVT
-- À exécuter dans le SQL Editor de Supabase Dashboard

-- 1. Supprimer toutes les matières existantes
DELETE FROM public.subjects;

-- 2. Insérer seulement les 4 matières principales pour Sciences Physiques
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
);

-- 3. Vérifier les matières
SELECT 
    name_fr,
    name_ar,
    icon,
    color,
    order_index
FROM public.subjects
ORDER BY order_index;
