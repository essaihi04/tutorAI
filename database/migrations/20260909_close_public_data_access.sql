-- Apply AFTER deploying the server-only Supabase client and admin account creation.
-- The React application calls FastAPI, never the Supabase Data API directly.
-- No rows are modified or deleted. Auth sign-in remains available separately.
BEGIN;

GRANT USAGE ON SCHEMA public TO service_role;
GRANT ALL ON ALL TABLES IN SCHEMA public TO service_role;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO service_role;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO service_role;

REVOKE ALL ON ALL TABLES IN SCHEMA public FROM anon, authenticated, PUBLIC;
REVOKE ALL ON ALL SEQUENCES IN SCHEMA public FROM anon, authenticated, PUBLIC;
REVOKE EXECUTE ON ALL FUNCTIONS IN SCHEMA public FROM anon, authenticated, PUBLIC;
REVOKE CREATE ON SCHEMA public FROM anon, authenticated, PUBLIC;

DO $security$
DECLARE item record;
BEGIN
    FOR item IN
        SELECT c.relname FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p')
    LOOP
        EXECUTE format('ALTER TABLE public.%I ENABLE ROW LEVEL SECURITY', item.relname);
    END LOOP;
END;
$security$;

ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    REVOKE ALL ON TABLES FROM anon, authenticated, PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    REVOKE ALL ON SEQUENCES FROM anon, authenticated, PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    REVOKE EXECUTE ON FUNCTIONS FROM anon, authenticated, PUBLIC;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    GRANT ALL ON TABLES TO service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    GRANT ALL ON SEQUENCES TO service_role;
ALTER DEFAULT PRIVILEGES FOR ROLE postgres IN SCHEMA public
    GRANT EXECUTE ON FUNCTIONS TO service_role;

-- Student accounts previously had bucket-wide upload/update/delete policies.
-- A restrictive policy defeats those permissive policies for this app's bucket,
-- while preserving public image/video URLs and leaving unrelated buckets alone.
DROP POLICY IF EXISTS moalim_resources_server_only ON storage.objects;
CREATE POLICY moalim_resources_server_only ON storage.objects
    AS RESTRICTIVE FOR ALL TO anon, authenticated
    USING (bucket_id <> 'pedagogical-resources')
    WITH CHECK (bucket_id <> 'pedagogical-resources');

NOTIFY pgrst, 'reload schema';
COMMIT;

-- Expected: no true privilege for either untrusted role; all tables use RLS.
SELECT c.relname, c.relrowsecurity,
       has_table_privilege('anon', c.oid, 'SELECT,INSERT,UPDATE,DELETE') AS anon_access,
       has_table_privilege('authenticated', c.oid, 'SELECT,INSERT,UPDATE,DELETE') AS user_access
FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace
WHERE n.nspname = 'public' AND c.relkind IN ('r', 'p', 'v', 'm');
