"""
Check the structure of student_profiles table
"""
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("=== Structure de la table student_profiles ===\n")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    
    # Try to get one record to see the columns
    result = supabase.table('student_profiles').select('*').limit(1).execute()
    
    if result.data:
        print("Colonnes existantes:")
        print(list(result.data[0].keys()))
    else:
        print("Table vide, essayons de voir la structure autrement...")
        
        # Try to insert a minimal record to see what's required
        test_data = {
            "id": "00000000-0000-0000-0000-000000000001",
            "student_id": "00000000-0000-0000-0000-000000000002"
        }
        
        try:
            result = supabase.table('student_profiles').insert(test_data).execute()
            if result.data:
                print("Colonnes de la table:")
                print(list(result.data[0].keys()))
                # Clean up
                supabase.table('student_profiles').delete().eq('id', test_data['id']).execute()
        except Exception as e:
            print(f"Erreur lors du test d'insertion: {e}")
            
            if "could not find" in str(e).lower():
                print("\n🔴 La table student_profiles n'a pas les bonnes colonnes!")
                print("\nColonnes manquantes probables:")
                print("- diagnostic_completed")
                print("- overall_proficiency")
                print("- learning_pace")
                print("- preferred_teaching_mode")
                
except Exception as e:
    print(f"Erreur: {e}")

print("\n" + "="*70)
print("SOLUTION: Exécutez le script init_supabase.sql complet")
print("="*70)
