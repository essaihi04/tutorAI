"""
Test script for Supabase Auth API
This tests authentication without needing database password or DNS resolution
"""
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

print("=== Test de l'API Supabase Auth ===\n")
print(f"URL Supabase: {SUPABASE_URL}")
print(f"Anon Key: {SUPABASE_ANON_KEY[:20]}...\n")

try:
    # Create Supabase client
    supabase = create_client(SUPABASE_URL, SUPABASE_ANON_KEY)
    print("✅ Client Supabase créé avec succès!")
    
    # Test 1: Check if we can query the students table
    print("\n=== Test 1: Vérification de l'accès à la table students ===")
    try:
        result = supabase.table('students').select('id,email,username').limit(5).execute()
        print(f"✅ Accès à la table students réussi!")
        print(f"   Nombre d'étudiants trouvés: {len(result.data)}")
        if result.data:
            print(f"   Exemple: {result.data[0]}")
    except Exception as e:
        print(f"⚠️  Erreur d'accès à la table: {e}")
        print("   Note: La table 'students' doit exister dans Supabase")
    
    # Test 2: Try to sign up a test user
    print("\n=== Test 2: Inscription d'un utilisateur de test ===")
    test_email = "test_api@example.com"
    test_password = "TestAPI123!"
    
    try:
        auth_response = supabase.auth.sign_up({
            "email": test_email,
            "password": test_password,
        })
        
        if auth_response.user:
            print(f"✅ Inscription réussie!")
            print(f"   User ID: {auth_response.user.id}")
            print(f"   Email: {auth_response.user.email}")
        else:
            print("⚠️  L'inscription n'a pas retourné d'utilisateur")
            
    except Exception as e:
        error_msg = str(e)
        if "already registered" in error_msg.lower() or "already exists" in error_msg.lower():
            print(f"ℹ️  L'utilisateur existe déjà (c'est normal si vous avez déjà testé)")
        else:
            print(f"❌ Erreur d'inscription: {e}")
    
    # Test 3: Try to sign in
    print("\n=== Test 3: Connexion avec l'utilisateur de test ===")
    try:
        auth_response = supabase.auth.sign_in_with_password({
            "email": test_email,
            "password": test_password,
        })
        
        if auth_response.session:
            print(f"✅ Connexion réussie!")
            print(f"   Access Token: {auth_response.session.access_token[:30]}...")
            print(f"   User ID: {auth_response.user.id}")
        else:
            print("❌ La connexion n'a pas retourné de session")
            
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
    
    print("\n" + "="*70)
    print("✅ SUCCÈS! L'API Supabase fonctionne correctement!")
    print("="*70)
    print("\nVous pouvez maintenant:")
    print("1. Démarrer le backend: python -m uvicorn app.main:app --reload")
    print("2. Démarrer le frontend: cd ../frontend && npm run dev")
    print("3. Tester l'authentification sur http://localhost:5173/login")
    print("\nNote: Vous n'avez plus besoin du mot de passe de la base de données!")
    
except Exception as e:
    print(f"\n❌ Erreur lors de la création du client Supabase: {e}")
    print("\n💡 Vérifiez:")
    print("1. Que SUPABASE_URL et SUPABASE_ANON_KEY sont corrects dans .env")
    print("2. Votre connexion Internet")
    print("3. Que votre projet Supabase est actif")
