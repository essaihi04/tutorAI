"""
Test session start endpoint with authentication
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get token from a test login
print("=== Test Session Start ===\n")

# First login to get token
login_data = {
    "email": input("Email: "),
    "password": input("Password: ")
}

try:
    # Login
    login_response = requests.post(
        "http://localhost:8000/api/v1/auth/login",
        json=login_data
    )
    
    if login_response.status_code != 200:
        print(f"❌ Login failed: {login_response.status_code}")
        print(login_response.text)
        exit(1)
    
    token = login_response.json()["access_token"]
    print(f"✅ Login successful, token: {token[:20]}...")
    
    # Get a lesson ID (you'll need to provide one)
    lesson_id = input("\nEnter a lesson ID (or press Enter to skip): ")
    
    if lesson_id:
        # Start session
        headers = {"Authorization": f"Bearer {token}"}
        session_data = {
            "lesson_id": lesson_id,
            "is_review": False
        }
        
        session_response = requests.post(
            "http://localhost:8000/api/v1/sessions/start",
            json=session_data,
            headers=headers
        )
        
        print(f"\nStatus: {session_response.status_code}")
        print(f"Response: {session_response.text}")
        
        if session_response.status_code == 200:
            print("\n✅ Session started successfully!")
        else:
            print(f"\n❌ Failed to start session")
    
except Exception as e:
    print(f"❌ Error: {e}")
