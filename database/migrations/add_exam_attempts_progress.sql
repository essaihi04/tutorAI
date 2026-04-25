-- Track exam progress (in-progress attempts)
-- Uses existing exam_attempts table. completed_at IS NULL => in progress.
-- Adds: current_question_index for resume UX.

alter table exam_attempts
    add column if not exists current_question_index integer default 0,
    add column if not exists exam_id text;     -- raw exam identifier (e.g. "physique-2024-normale")

-- Helpful index for "my in-progress" and "my latest" lookups
create index if not exists idx_exam_attempts_student_completed
    on exam_attempts(student_id, completed_at);
