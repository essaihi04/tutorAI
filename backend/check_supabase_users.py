"""
Check if users exist in Supabase Auth
"""
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

print("=== Vérification des utilisateurs Supabase ===\n")

try:
    # Use service role key to access auth.users
    supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
    
    # Check students table
    print("1. Utilisateurs dans la table 'students':")
    students = supabase.table('students').select('id, email, username, full_name').execute()
    
    if students.data:
        print(f"   Nombre: {len(students.data)}")
        for student in students.data:
            print(f"   - {student['email']} ({student['username']}) - {student['full_name']}")
    else:
        print("   ❌ Aucun utilisateur dans la table students")
    
    print("\n2. Test de connexion avec Supabase Auth:")
    email = input("\nEntrez l'email pour tester: ")
    password = input("Entrez le mot de passe: ")
    
    try:
        # Try to sign in
        auth_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password,
        })
        
        if auth_response.session:
            print("\n✅ Connexion Supabase Auth réussie!")
            print(f"   User ID: {auth_response.user.id}")
            print(f"   Email: {auth_response.user.email}")
            print(f"   Access Token: {auth_response.session.access_token[:50]}...")
        else:
            print("\n❌ Pas de session retournée")
            
    except Exception as e:
        print(f"\n❌ Erreur de connexion Supabase Auth: {e}")
        
        if "invalid" in str(e).lower() or "credentials" in str(e).lower():
            print("\n💡 Possible raisons:")
            print("   1. Email ou mot de passe incorrect")
            print("   2. L'utilisateur n'existe pas dans Supabase Auth")
            print("   3. L'utilisateur n'est pas confirmé")
            print("\n💡 Solution:")
            print("   Allez dans Supabase Dashboard → Authentication → Users")
            print("   Vérifiez que l'utilisateur existe et est confirmé")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
