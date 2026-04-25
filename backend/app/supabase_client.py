from supabase import create_client, Client
from app.config import get_settings

settings = get_settings()

# Public client for auth flows bound to anon key
supabase: Client = create_client(settings.supabase_url, settings.supabase_anon_key)

# Admin client for server-side database operations that should bypass RLS
supabase_admin: Client = create_client(settings.supabase_url, settings.supabase_service_role_key)

def get_supabase() -> Client:
    """Get Supabase client instance"""
    return supabase

def get_supabase_admin() -> Client:
    """Get Supabase admin client instance."""
    return supabase_admin
