-- Add expires_at to students table for test accounts (1-day trials).
-- NULL = permanent account, non-NULL = account expires at that timestamp.

alter table students
    add column if not exists expires_at timestamptz default null,
    add column if not exists created_from_request_id uuid default null;

-- Also store the created user_id back on the registration_request row
alter table registration_requests
    add column if not exists created_user_id uuid default null;

comment on column students.expires_at is 'NULL = permanent. Non-NULL = account disabled after this timestamp (test accounts).';
comment on column students.created_from_request_id is 'FK back to registration_requests if account was created from a pre-inscription.';
comment on column registration_requests.created_user_id is 'The students.id created when the admin activated this request.';
