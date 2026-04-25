#!/usr/bin/env python3
"""
Test des endpoints content
"""
import requests
import json

def test_content_endpoints():
    base_url = "http://127.0.0.1:8000/api/v1"
    
    print("🔍 Test des endpoints content...")
    
    # Test subjects
    try:
        print("\n1. Test /subjects")
        response = requests.get(f"{base_url}/content/subjects", timeout=5)
        print(f"Status: {response.status_code}")
        if response.text:
            data = response.json()
            print(f"Subjects: {len(data)} items")
            if data:
                print(f"Premier subject: {data[0]}")
            else:
                print("❌ Aucun subject trouvé - la table est vide!")
        else:
            print("❌ Response vide")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test profile
    try:
        print("\n2. Test /sessions/profile")
        response = requests.get(f"{base_url}/sessions/profile", timeout=5)
        print(f"Status: {response.status_code}")
        if response.status_code == 401:
            print("❌ Non authentifié - normal sans token")
        else:
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Erreur: {e}")

if __name__ == "__main__":
    test_content_endpoints()
