alter table students
    add column if not exists promo_code text default null;

alter table registration_requests
    add column if not exists promo_code text default null;

create table if not exists promo_codes (
    id uuid primary key default gen_random_uuid(),
    code text not null unique,
    label text,
    is_active boolean not null default true,
    created_at timestamptz not null default now()
);

create index if not exists idx_students_promo_code on students(promo_code);
create index if not exists idx_registration_requests_promo_code on registration_requests(promo_code);
create index if not exists idx_promo_codes_code on promo_codes(code);
create index if not exists idx_promo_codes_is_active on promo_codes(is_active);

comment on column students.promo_code is 'Code promo/source used to identify where the student came from.';
comment on column registration_requests.promo_code is 'Code promo entered during pre-inscription.';
