# 📚 Ajouter des matières au Dashboard

## 🔴 Problème

La table `subjects` est vide, donc le Dashboard affiche "Chargement des matières..." indéfiniment.

## ✅ Solution

### Exécutez ce script SQL dans Supabase

1. **Allez sur** https://supabase.com/dashboard
2. **Sélectionnez** votre projet `ldeifdnczkzgtxctjlel`
3. **Allez dans** SQL Editor → New Query
4. **Copiez et exécutez le script ci-dessous:**

```sql
-- Insérer les matières pour 2ème BAC Sciences Physiques BIOF
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
```

5. **Cliquez sur "Run"** ou appuyez sur **Ctrl+Enter**

## 🧪 Tester

Après avoir exécuté le script:

1. **Rechargez le Dashboard** (F5)
2. Les 8 matières devraient apparaître:
   - 📐 Mathématiques
   - ⚛️ Physique
   - 🧪 Chimie
   - 🌱 SVT
   - 📚 Français
   - 🇬🇧 Anglais
   - 🤔 Philosophie
   - 📖 Arabe

## 📝 Matières incluses

Toutes les matières du programme **2ème BAC Sciences Physiques BIOF**:
- ✅ Matières scientifiques principales (Maths, Physique, Chimie, SVT)
- ✅ Langues (Français, Anglais, Arabe)
- ✅ Philosophie
- ✅ Noms en français ET en arabe
- ✅ Icônes et couleurs pour chaque matière

## 🎯 Prochaines étapes

Après avoir ajouté les matières, vous pourrez:
1. Voir toutes les matières sur le Dashboard
2. Cliquer sur une matière pour voir ses chapitres (quand vous les ajouterez)
3. Commencer à structurer votre contenu pédagogique

Le script complet est dans `database/insert_sample_subjects.sql` 📁
