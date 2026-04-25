"""
Verify if RLS is disabled on Supabase tables
"""
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("=== Vérification du statut RLS ===\n")

try:
    # Use service role key to bypass RLS
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    
    # Check RLS status using a direct query
    result = supabase.rpc('exec_sql', {
        'query': """
        SELECT 
            schemaname,
            tablename,
            rowsecurity
        FROM pg_tables
        WHERE schemaname = 'public' 
        AND tablename IN ('students', 'student_profiles')
        ORDER BY tablename;
        """
    }).execute()
    
    print("Statut RLS des tables:")
    print(result.data)
    
except Exception as e:
    print(f"Erreur: {e}")
    print("\nEssayons une autre méthode...")
    
    # Try direct insert test
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
        
        test_data = {
            "id": "00000000-0000-0000-0000-000000000001",
            "username": "rls_test",
            "email": "rls_test@example.com",
            "full_name": "RLS Test",
            "preferred_language": "fr",
            "is_active": True
        }
        
        print("\nTest d'insertion avec service_role key...")
        result = supabase.table('students').insert(test_data).execute()
        
        if result.data:
            print("✅ Insertion réussie avec service_role!")
            print("RLS est probablement désactivé OU les policies permettent l'insertion")
            
            # Clean up
            supabase.table('students').delete().eq('id', test_data['id']).execute()
        else:
            print("❌ Insertion échouée")
            
    except Exception as e2:
        print(f"❌ Erreur d'insertion: {e2}")
        
        if "row-level security" in str(e2).lower():
            print("\n🔴 RLS EST TOUJOURS ACTIVÉ!")
            print("\nVous devez exécuter ce script dans le SQL Editor de Supabase:")
            print("="*70)
            print("ALTER TABLE public.students DISABLE ROW LEVEL SECURITY;")
            print("ALTER TABLE public.student_profiles DISABLE ROW LEVEL SECURITY;")
            print("="*70)
        else:
            print(f"\nAutre erreur: {e2}")
