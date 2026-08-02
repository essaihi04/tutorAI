-- ═══════════════════════════════════════════════════════════════════════
-- Ajout des matières ANGLAIS et PHILOSOPHIE — 2ème BAC Sciences Physiques
-- Programme officiel MEN Maroc (BIOF)
-- À exécuter dans le SQL Editor de Supabase Dashboard
-- ═══════════════════════════════════════════════════════════════════════
-- Script IDEMPOTENT : peut être relancé sans créer de doublons.

-- ── 1. Insérer les matières si elles n'existent pas déjà ──────────────
INSERT INTO public.subjects (id, name_fr, name_ar, description_fr, description_ar, icon, color, order_index)
SELECT gen_random_uuid(),
       'Anglais',
       'الإنجليزية',
       'Anglais 2ème BAC Sciences Physiques — Examen national 2h, coefficient 2 (Reading 15 / Language 15 / Writing 10)',
       'اللغة الإنجليزية للسنة الثانية باكالوريا علوم فيزيائية',
       '🇬🇧',
       '#EF4444',
       4
WHERE NOT EXISTS (SELECT 1 FROM public.subjects WHERE name_fr = 'Anglais');

INSERT INTO public.subjects (id, name_fr, name_ar, description_fr, description_ar, icon, color, order_index)
SELECT gen_random_uuid(),
       'Philosophie',
       'الفلسفة',
       'Philosophie 2ème BAC filières scientifiques — Examen national 2h, coefficient 2 (4 مجزوءات, un sujet au choix)',
       'الفلسفة للسنة الثانية باكالوريا الشعب العلمية',
       '🤔',
       '#6366F1',
       5
WHERE NOT EXISTS (SELECT 1 FROM public.subjects WHERE name_fr = 'Philosophie');

-- ── 2. Chapitres ANGLAIS : les 10 units du programme officiel ─────────
INSERT INTO public.chapters (subject_id, chapter_number, title_fr, title_ar, description_fr, difficulty_level, order_index)
SELECT s.id, v.num, v.title_fr, v.title_ar, v.descr, v.diff::difficulty_level, v.num
FROM public.subjects s
CROSS JOIN (VALUES
    (1,  'Formal, informal and non-formal education', 'التعليم النظامي وغير النظامي', 'Types of education, lifelong learning, distance learning, literacy', 'beginner'),
    (2,  'Gifts of youth',                            'مواهب الشباب',                'Talents, creativity, volunteering, youth challenges', 'beginner'),
    (3,  'Cultural issues and values',                'القضايا الثقافية والقيم',      'Cultural identity, traditions, diversity, tolerance', 'intermediate'),
    (4,  'Humour',                                    'الفكاهة',                     'Types of humour, humour across cultures, benefits of laughter', 'beginner'),
    (5,  'Science and technology',                    'العلوم والتكنولوجيا',          'Inventions, internet, AI, advantages and drawbacks', 'intermediate'),
    (6,  'Sustainable development',                   'التنمية المستدامة',            'Three pillars, renewable energy, pollution, recycling', 'intermediate'),
    (7,  'Women and power',                           'المرأة والسلطة',              'Gender equality, women rights, empowerment, Moudawana', 'intermediate'),
    (8,  'Brain drain',                               'هجرة الأدمغة',                'Causes, consequences, brain gain, solutions', 'advanced'),
    (9,  'International organizations',               'المنظمات الدولية',             'UN, UNESCO, UNICEF, WHO, NGOs, humanitarian aid', 'intermediate'),
    (10, 'Citizenship',                               'المواطنة',                    'Rights and duties, civic behaviour, solidarity, human rights', 'intermediate')
) AS v(num, title_fr, title_ar, descr, diff)
WHERE s.name_fr = 'Anglais'
  AND NOT EXISTS (SELECT 1 FROM public.chapters c WHERE c.subject_id = s.id AND c.chapter_number = v.num);

-- ── 3. Chapitres PHILOSOPHIE : 4 مجزوءات × concepts (filières scientifiques) ──
-- ⚠️ Programme allégé : PAS de التاريخ / العلوم الإنسانية / العنف / السعادة
INSERT INTO public.chapters (subject_id, chapter_number, title_fr, title_ar, description_fr, difficulty_level, order_index)
SELECT s.id, v.num, v.title_fr, v.title_ar, v.descr, v.diff::difficulty_level, v.num
FROM public.subjects s
CROSS JOIN (VALUES
    (1, 'La condition humaine — La personne',        'مجزوءة الوضع البشري : مفهوم الشخص',        'Identité, valeur de la personne, nécessité et liberté (Descartes, Locke, Kant, Spinoza)', 'intermediate'),
    (2, 'La condition humaine — Autrui',             'مجزوءة الوضع البشري : مفهوم الغير',        'Existence, connaissance et relation avec autrui (Sartre, Hegel, Merleau-Ponty)', 'intermediate'),
    (3, 'La connaissance — Théorie et expérience',   'مجزوءة المعرفة : النظرية والتجربة',        'Méthode expérimentale, rationalisme scientifique, falsifiabilité (Claude Bernard, Bachelard, Popper)', 'advanced'),
    (4, 'La connaissance — La vérité',               'مجزوءة المعرفة : مفهوم الحقيقة',           'Opinion et vérité, critères de vérité, vérité comme valeur (Platon, Descartes, Nietzsche)', 'advanced'),
    (5, 'La politique — L''État',                    'مجزوءة السياسة : مفهوم الدولة',            'Légitimité, finalités, État entre droit et violence (Hobbes, Rousseau, Weber, Marx)', 'intermediate'),
    (6, 'La politique — Le droit et la justice',     'مجزوءة السياسة : مفهوم الحق والعدالة',     'Droit naturel/positif, justice, égalité et équité (Aristote, Rawls, Alain)', 'intermediate'),
    (7, 'La morale — Le devoir',                     'مجزوءة الأخلاق : مفهوم الواجب',            'Devoir et contrainte, conscience morale, devoir et société (Kant, Rousseau, Durkheim, Nietzsche)', 'advanced'),
    (8, 'La morale — La liberté',                    'مجزوءة الأخلاق : مفهوم الحرية',            'Liberté et déterminisme, libre arbitre, liberté et loi (Spinoza, Sartre, Montesquieu)', 'advanced')
) AS v(num, title_fr, title_ar, descr, diff)
WHERE s.name_fr = 'Philosophie'
  AND NOT EXISTS (SELECT 1 FROM public.chapters c WHERE c.subject_id = s.id AND c.chapter_number = v.num);

-- ── 4. Vérification ──────────────────────────────────────────────────
SELECT s.name_fr, s.name_ar, s.icon, s.order_index, COUNT(c.id) AS nb_chapitres
FROM public.subjects s
LEFT JOIN public.chapters c ON c.subject_id = s.id
WHERE s.name_fr IN ('Anglais', 'Philosophie')
GROUP BY s.id, s.name_fr, s.name_ar, s.icon, s.order_index
ORDER BY s.order_index;
