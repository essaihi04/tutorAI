"""
Test login endpoint with the registered user
"""
import requests
import json

# Test with the user you registered
test_credentials = {
    "email": input("Enter your email: "),
    "password": input("Enter your password: ")
}

print("\n=== Test de connexion ===\n")
print(f"URL: http://localhost:8000/api/v1/auth/login")
print(f"Email: {test_credentials['email']}\n")

try:
    response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        json=test_credentials,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        print("✅ Connexion réussie!")
        data = response.json()
        print(f"Access Token: {data.get('access_token', '')[:50]}...")
    else:
        print(f"❌ Erreur {response.status_code}")
        try:
            error_data = response.json()
            print(f"Error: {json.dumps(error_data, indent=2)}")
        except:
            print(f"Response: {response.text}")
            
except requests.exceptions.ConnectionError:
    print("❌ Backend non accessible")
except Exception as e:
    print(f"❌ Erreur: {e}")
