"""
Check if subjects table has data
"""
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print("=== Vérification de la table subjects ===\n")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    # Check subjects
    result = supabase.table('subjects').select('*').execute()
    
    print(f"Nombre de matières: {len(result.data)}")
    
    if result.data:
        print("\nMatières trouvées:")
        for subject in result.data:
            print(f"  - {subject.get('name_fr', 'N/A')} ({subject.get('name_ar', 'N/A')})")
    else:
        print("\n❌ La table 'subjects' est vide!")
        print("\n💡 Solution: Vous devez ajouter des matières à la base de données")
        print("   Exécutez le script SQL pour insérer des matières de test")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    
    if "could not find" in str(e).lower() or "does not exist" in str(e).lower():
        print("\n❌ La table 'subjects' n'existe pas!")
        print("\n💡 Solution: Exécutez le script init_supabase.sql complet")
