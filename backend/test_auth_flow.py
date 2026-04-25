"""
Test complete authentication flow
"""
import requests
import json

print("=== Test Complet Authentification ===\n")

BASE_URL = "http://localhost:8000/api/v1"

# Test 1: Login
print("1. Test Login...")
login_data = {
    "email": input("Email: "),
    "password": input("Password: ")
}

try:
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"   Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get("access_token")
        print(f"   ✅ Login réussi")
        print(f"   Token: {token[:30]}...")
        
        # Test 2: Profile avec token
        print("\n2. Test Profile avec token...")
        headers = {"Authorization": f"Bearer {token}"}
        profile_response = requests.get(f"{BASE_URL}/sessions/profile", headers=headers)
        print(f"   Status: {profile_response.status_code}")
        
        if profile_response.status_code == 200:
            print(f"   ✅ Profile récupéré")
            print(f"   Data: {json.dumps(profile_response.json(), indent=2)}")
        else:
            print(f"   ❌ Erreur Profile")
            print(f"   Response: {profile_response.text}")
        
        # Test 3: Start Session avec token
        print("\n3. Test Start Session...")
        print("   Note: Vous devez avoir des leçons dans la base")
        lesson_id = input("   Entrez un lesson_id (ou Enter pour skip): ")
        
        if lesson_id:
            session_data = {"lesson_id": lesson_id, "is_review": False}
            session_response = requests.post(
                f"{BASE_URL}/sessions/start",
                json=session_data,
                headers=headers
            )
            print(f"   Status: {session_response.status_code}")
            
            if session_response.status_code == 200:
                print(f"   ✅ Session créée")
                print(f"   Data: {json.dumps(session_response.json(), indent=2)}")
            else:
                print(f"   ❌ Erreur Session")
                print(f"   Response: {session_response.text}")
        
        # Test 4: Subjects (pas besoin d'auth normalement)
        print("\n4. Test Subjects...")
        subjects_response = requests.get(f"{BASE_URL}/content/subjects")
        print(f"   Status: {subjects_response.status_code}")
        
        if subjects_response.status_code == 200:
            subjects = subjects_response.json()
            print(f"   ✅ {len(subjects)} matières trouvées")
            for s in subjects:
                print(f"      - {s.get('name_fr', 'N/A')}")
        else:
            print(f"   ❌ Erreur Subjects")
            print(f"   Response: {subjects_response.text}")
            
    else:
        print(f"   ❌ Login échoué")
        print(f"   Response: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("   ❌ Impossible de se connecter au backend")
    print("   Vérifiez que le backend est démarré sur http://localhost:8000")
except Exception as e:
    print(f"   ❌ Erreur: {e}")

print("\n" + "="*50)
print("Test terminé")
