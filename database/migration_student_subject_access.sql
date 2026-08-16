-- ═══════════════════════════════════════════════════════════════════════
-- MIGRATION — Abonnements et accès par matière
-- Dépend de la table students et de la table subjects.
-- Compatible avec migration_filieres.sql, mais ne l'exige pas.
-- ═══════════════════════════════════════════════════════════════════════

BEGIN;

-- FALSE conserve le comportement historique. Une fois l'abonnement d'un
-- élève configuré, le backend passe ce champ à TRUE et applique strictement
-- les lignes actives de student_subject_access.
ALTER TABLE public.students
    ADD COLUMN IF NOT EXISTS subject_access_managed BOOLEAN NOT NULL DEFAULT FALSE;

CREATE TABLE IF NOT EXISTS public.student_subject_access (
    student_id UUID NOT NULL REFERENCES public.students(id) ON DELETE CASCADE,
    subject_id UUID NOT NULL REFERENCES public.subjects(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active', 'suspended', 'expired')),
    source VARCHAR(30) NOT NULL DEFAULT 'manual',
    starts_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    ends_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    PRIMARY KEY (student_id, subject_id),
    CHECK (ends_at IS NULL OR ends_at > starts_at)
);

CREATE INDEX IF NOT EXISTS idx_student_subject_access_active
    ON public.student_subject_access(student_id, status, ends_at);

ALTER TABLE public.student_subject_access ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS student_read_own_subject_access ON public.student_subject_access;
CREATE POLICY student_read_own_subject_access
    ON public.student_subject_access
    FOR SELECT
    USING (auth.uid() = student_id);

-- Les écritures restent réservées au backend utilisant la service-role.
-- Aucun backfill n'est nécessaire : les comptes actuels restent en mode
-- legacy jusqu'à l'activation explicite de subject_access_managed.

COMMIT;
