#!/usr/bin/env python3
"""
Test simple de connexion à l'auth Supabase
"""
import asyncio
import httpx
import sys

async def test_supabase_auth():
    """Test direct connection to Supabase auth"""
    url = "https://ldeifdnczkzgtxctjlel.supabase.co/auth/v1/token?grant_type=password"
    headers = {
        "apikey": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImxkZWlmZG5jemt6Z3R4Y3RqbGVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjMwNTcxMTUsImV4cCI6MjA3ODYzMzExNX0._6t-wGotwy00NafsRnvXdmX7SXg6z5Cd6B98889Ic1o",
        "Content-Type": "application/json",
    }
    data = {
        "email": "test@test.com",
        "password": "test123"
    }
    
    print("🔍 Test de connexion Supabase...")
    print(f"URL: {url}")
    print(f"Email: {data['email']}")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            print("⏳ Envoi de la requête...")
            response = await client.post(url, headers=headers, json=data)
            
            print(f"Status: {response.status_code}")
            print(f"Headers: {dict(response.headers)}")
            
            if response.text:
                print(f"Response: {response.text}")
            
            if response.status_code == 200:
                print("✅ Connexion réussie!")
                return True
            else:
                print(f"❌ Erreur: {response.status_code}")
                return False
                
    except asyncio.TimeoutError:
        print("❌ Timeout - la requête a pris trop de temps")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_supabase_auth())
    sys.exit(0 if result else 1)
