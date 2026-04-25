"""
Test the registration endpoint directly to see the exact error
"""
import requests
import json

# Test data
test_user = {
    "username": "testuser123",
    "email": "testuser123@example.com",
    "password": "TestPass123!",
    "full_name": "Test User",
    "preferred_language": "fr"
}

print("=== Test de l'endpoint d'inscription ===\n")
print(f"URL: http://localhost:8000/api/v1/auth/register")
print(f"Data: {json.dumps(test_user, indent=2)}\n")

try:
    response = requests.post(
        "http://localhost:8000/api/v1/auth/register",
        json=test_user,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response Headers: {dict(response.headers)}\n")
    
    if response.status_code == 201:
        print("✅ Inscription réussie!")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"❌ Erreur {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error detail: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Response text: {response.text}")
            
except requests.exceptions.ConnectionError:
    print("❌ Impossible de se connecter au backend")
    print("Vérifiez que le backend est démarré: python -m uvicorn app.main:app --reload")
except Exception as e:
    print(f"❌ Erreur: {e}")
