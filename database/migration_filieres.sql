-- ═══════════════════════════════════════════════════════════════════════
-- MIGRATION — Support multi-filières (2ème Bac Maroc)
-- ═══════════════════════════════════════════════════════════════════════
-- Objectif : permettre à l'application de servir plusieurs filières
-- (SP, SM A, SM B, SGC, SE) au lieu d'être câblée sur Sciences Physiques.
--
-- ⚠️ Migration ADDITIVE : aucune colonne ni table supprimée, aucune donnée
-- écrasée. Les 19 élèves existants sont rattachés à 'SP' (leur school_level
-- actuel est déjà « 2eme BAC Sciences Physiques BIOF »).
--
-- Idempotente : peut être relancée sans effet de bord.
-- ═══════════════════════════════════════════════════════════════════════

BEGIN;

-- ── 1. Table de référence des filières ───────────────────────────────
CREATE TABLE IF NOT EXISTS public.filieres (
    code            VARCHAR(10) PRIMARY KEY,
    nom_fr          VARCHAR(100) NOT NULL,
    nom_ar          VARCHAR(100) NOT NULL,
    total_coeff     INTEGER,
    is_active       BOOLEAN DEFAULT TRUE,   -- FALSE = pas encore de contenu
    order_index     INTEGER NOT NULL DEFAULT 0,
    created_at      TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

INSERT INTO public.filieres (code, nom_fr, nom_ar, total_coeff, is_active, order_index)
VALUES
    ('SP',   '2ème Bac Sciences Physiques',         'الثانية باكالوريا علوم فيزيائية',        34, TRUE,  1),
    ('SM_A', '2ème Bac Sciences Mathématiques A',   'الثانية باكالوريا علوم رياضية أ',        40, FALSE, 2),
    ('SM_B', '2ème Bac Sciences Mathématiques B',   'الثانية باكالوريا علوم رياضية ب',        40, FALSE, 3),
    ('SGC',  '2ème Bac Sciences de Gestion Comptable', 'الثانية باكالوريا علوم التدبير المحاسباتي', 45, FALSE, 4),
    ('SE',   '2ème Bac Sciences Économiques',       'الثانية باكالوريا علوم اقتصادية',        44, FALSE, 5)
ON CONFLICT (code) DO NOTHING;

-- ── 2. Rattacher chaque élève à une filière ──────────────────────────
ALTER TABLE public.students
    ADD COLUMN IF NOT EXISTS filiere VARCHAR(10) REFERENCES public.filieres(code);

-- Les comptes existants sont tous en Sciences Physiques
UPDATE public.students SET filiere = 'SP' WHERE filiere IS NULL;

ALTER TABLE public.students ALTER COLUMN filiere SET DEFAULT 'SP';

CREATE INDEX IF NOT EXISTS idx_students_filiere ON public.students(filiere);

-- ── 3. Rattacher les matières aux filières (relation N-N) ────────────
-- Une matière comme la Philosophie est commune à TOUTES les filières :
-- une simple colonne 'filiere' sur subjects ne suffirait pas.
CREATE TABLE IF NOT EXISTS public.subjects_filieres (
    subject_id      UUID NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    filiere_code    VARCHAR(10) NOT NULL REFERENCES public.filieres(code) ON DELETE CASCADE,
    coefficient     INTEGER,
    exam_type       VARCHAR(20) DEFAULT 'national',  -- national | regional | continu
    duree_minutes   INTEGER,
    order_index     INTEGER NOT NULL DEFAULT 0,
    PRIMARY KEY (subject_id, filiere_code)
);

CREATE INDEX IF NOT EXISTS idx_subjects_filieres_filiere
    ON public.subjects_filieres(filiere_code);

-- ── 4. Rattacher les 6 matières existantes à la filière SP ───────────
INSERT INTO public.subjects_filieres (subject_id, filiere_code, coefficient, exam_type, duree_minutes, order_index)
SELECT s.id, 'SP', v.coeff, 'national', v.duree, v.ord
FROM public.subjects s
JOIN (VALUES
    ('Physique',                                7, 180, 1),
    ('Chimie',                                  7, 180, 2),
    ('Mathematiques',                           7, 180, 3),
    ('Sciences de la Vie et de la Terre (SVT)', 5, 180, 4),
    ('Anglais',                                 2, 120, 5),
    ('Philosophie',                             2, 120, 6)
) AS v(name_fr, coeff, duree, ord) ON s.name_fr = v.name_fr
ON CONFLICT (subject_id, filiere_code) DO NOTHING;

-- ── 5. Philosophie et Anglais sont communes à TOUTES les filières ────
-- Leur programme est identique quelle que soit la filière scientifique
-- ou économique : on les rattache partout dès maintenant.
INSERT INTO public.subjects_filieres (subject_id, filiere_code, coefficient, exam_type, duree_minutes, order_index)
SELECT s.id, f.code, 2, 'national', 120,
       CASE WHEN s.name_fr = 'Anglais' THEN 90 ELSE 91 END
FROM public.subjects s
CROSS JOIN public.filieres f
WHERE s.name_fr IN ('Anglais', 'Philosophie')
  AND f.code <> 'SP'
ON CONFLICT (subject_id, filiere_code) DO NOTHING;

-- ── 6. Les matières scientifiques partagées par SM A / SM B ──────────
-- Maths et PC existent dans SM mais avec des coefficients différents
-- ET un programme plus large : le curriculum devra être versionné par
-- filière côté backend (mathematiques_sm.json), la matière reste la même.
INSERT INTO public.subjects_filieres (subject_id, filiere_code, coefficient, exam_type, duree_minutes, order_index)
SELECT s.id, v.fil, v.coeff, 'national', v.duree, v.ord
FROM public.subjects s
JOIN (VALUES
    ('Mathematiques',                           'SM_A', 9, 240, 1),
    ('Physique',                                'SM_A', 7, 240, 2),
    ('Chimie',                                  'SM_A', 7, 240, 3),
    ('Sciences de la Vie et de la Terre (SVT)', 'SM_A', 3, 120, 4),
    ('Mathematiques',                           'SM_B', 9, 240, 1),
    ('Physique',                                'SM_B', 7, 240, 2),
    ('Chimie',                                  'SM_B', 7, 240, 3)
) AS v(name_fr, fil, coeff, duree, ord) ON s.name_fr = v.name_fr
ON CONFLICT (subject_id, filiere_code) DO NOTHING;

COMMIT;

-- ── 7. Vérification ──────────────────────────────────────────────────
SELECT f.code, f.nom_fr, f.is_active,
       COUNT(sf.subject_id) AS nb_matieres,
       (SELECT COUNT(*) FROM public.students st WHERE st.filiere = f.code) AS nb_eleves
FROM public.filieres f
LEFT JOIN public.subjects_filieres sf ON sf.filiere_code = f.code
GROUP BY f.code, f.nom_fr, f.is_active, f.order_index
ORDER BY f.order_index;
