from supabase import create_client, Client, ClientOptions
from app.config import get_settings

settings = get_settings()

# Server-only database client. Never sign in/up on a shared client.
supabase: Client = create_client(settings.supabase_url, settings.supabase_service_role_key,
    options=ClientOptions(auto_refresh_token=False, persist_session=False))

# Admin client for server-side database operations that should bypass RLS
supabase_admin: Client = supabase

def get_supabase() -> Client:
    """Get Supabase client instance"""
    return supabase

def get_supabase_admin() -> Client:
    """Get Supabase admin client instance."""
    return supabase_admin
