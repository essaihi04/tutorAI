"""
Check if tables exist in Supabase and show their structure
"""
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print("=== Vérification des tables Supabase ===\n")

try:
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    
    # Check students table
    print("1. Table 'students':")
    try:
        result = supabase.table('students').select('*').limit(1).execute()
        print(f"   ✅ Table existe")
        print(f"   Nombre d'enregistrements: {len(result.data)}")
        if result.data:
            print(f"   Colonnes: {list(result.data[0].keys())}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        print("   → La table 'students' n'existe pas ou n'est pas accessible")
    
    # Check student_profiles table
    print("\n2. Table 'student_profiles':")
    try:
        result = supabase.table('student_profiles').select('*').limit(1).execute()
        print(f"   ✅ Table existe")
        print(f"   Nombre d'enregistrements: {len(result.data)}")
        if result.data:
            print(f"   Colonnes: {list(result.data[0].keys())}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        print("   → La table 'student_profiles' n'existe pas ou n'est pas accessible")
    
    print("\n" + "="*70)
    print("SOLUTION:")
    print("="*70)
    print("Si les tables n'existent pas, vous devez:")
    print("1. Aller sur https://supabase.com/dashboard")
    print("2. Sélectionner votre projet 'ldeifdnczkzgtxctjlel'")
    print("3. Aller dans SQL Editor")
    print("4. Exécuter le script 'database/init_supabase.sql'")
    print("\nOu utilisez le script simplifié ci-dessous:")
    
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")
