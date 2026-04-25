-- Registration requests (pre-inscriptions)
-- Prospective students fill a public form; admin reviews and contacts them via WhatsApp
-- to manually create their account.

create table if not exists registration_requests (
    id uuid primary key default gen_random_uuid(),
    nom text not null,
    prenom text not null,
    phone text not null,
    ville text not null,
    email text,
    niveau text,              -- e.g. "2 BAC SP BIOF"
    message text,             -- optional free text from the student
    status text not null default 'pending',   -- pending | contacted | activated | rejected
    admin_notes text,
    contacted_at timestamptz,
    activated_at timestamptz,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now()
);

create index if not exists idx_registration_requests_status on registration_requests(status);
create index if not exists idx_registration_requests_created_at on registration_requests(created_at desc);

-- Updated_at trigger
create or replace function set_registration_requests_updated_at()
returns trigger as $$
begin
    new.updated_at = now();
    return new;
end;
$$ language plpgsql;

drop trigger if exists trg_registration_requests_updated_at on registration_requests;
create trigger trg_registration_requests_updated_at
before update on registration_requests
for each row execute function set_registration_requests_updated_at();

-- RLS: block direct client access; only service role (used by backend) can read/write
alter table registration_requests enable row level security;

-- No policies defined => public/anon role has no access
-- Backend uses the service role key which bypasses RLS
