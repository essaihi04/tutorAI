import asyncio
import asyncpg
import socket

async def test_direct_connection():
    """Test direct connection to Supabase with different approaches"""
    
    # Configuration
    project_ref = "yzvlmulpqnovduqhhtjf"
    password = "aYTGWasXrvwHdetZ"
    
    # Test 1: Try to resolve and get IPv4
    print("=== Test 1: Checking DNS resolution ===")
    hostname = f"db.{project_ref}.supabase.co"
    
    try:
        # Force IPv4 resolution
        addr_info = socket.getaddrinfo(
            hostname, 
            5432, 
            socket.AF_INET,  # Force IPv4
            socket.SOCK_STREAM
        )
        if addr_info:
            ipv4 = addr_info[0][4][0]
            print(f"✓ Found IPv4 address: {ipv4}")
            
            # Try connecting with IPv4
            print(f"\n=== Test 2: Connecting with IPv4 ({ipv4}) ===")
            try:
                conn = await asyncpg.connect(
                    user="postgres",
                    password=password,
                    database="postgres",
                    host=ipv4,
                    port=5432,
                    timeout=15,
                    ssl='require'
                )
                print("✓ Connection successful!")
                
                version = await conn.fetchval('SELECT version()')
                print(f"✓ PostgreSQL: {version[:60]}...")
                
                tables = await conn.fetch("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    ORDER BY table_name
                """)
                print(f"✓ Tables: {[t['table_name'] for t in tables]}")
                
                await conn.close()
                
                print(f"\n✅ SUCCESS! Update your .env with:")
                print(f"DATABASE_URL=postgresql+asyncpg://postgres:{password}@{ipv4}:5432/postgres?ssl=require")
                return True
                
            except Exception as e:
                print(f"✗ IPv4 connection failed: {e}")
    except socket.gaierror as e:
        print(f"✗ No IPv4 address found: {e}")
    
    # Test 3: Try with hostname and SSL
    print(f"\n=== Test 3: Direct connection with hostname and SSL ===")
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password=password,
            database="postgres",
            host=hostname,
            port=5432,
            timeout=15,
            ssl='require'
        )
        print("✓ Connection successful with SSL!")
        await conn.close()
        
        print(f"\n✅ SUCCESS! Update your .env with:")
        print(f"DATABASE_URL=postgresql+asyncpg://postgres:{password}@{hostname}:5432/postgres?ssl=require")
        return True
        
    except Exception as e:
        print(f"✗ Direct connection failed: {e}")
    
    # Test 4: Try without SSL
    print(f"\n=== Test 4: Direct connection without SSL ===")
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password=password,
            database="postgres",
            host=hostname,
            port=5432,
            timeout=15,
            ssl=False
        )
        print("✓ Connection successful without SSL!")
        await conn.close()
        
        print(f"\n✅ SUCCESS! Update your .env with:")
        print(f"DATABASE_URL=postgresql+asyncpg://postgres:{password}@{hostname}:5432/postgres")
        return True
        
    except Exception as e:
        print(f"✗ Connection without SSL failed: {e}")
    
    return False

if __name__ == "__main__":
    success = asyncio.run(test_direct_connection())
    if not success:
        print("\n❌ Toutes les tentatives ont échoué.")
        print("\n💡 Solutions possibles:")
        print("1. Vérifiez que votre projet Supabase est actif sur https://supabase.com/dashboard")
        print("2. Vérifiez le mot de passe dans Settings > Database")
        print("3. Essayez de redémarrer votre routeur/connexion Internet")
        print("4. Contactez votre FAI - il peut bloquer les connexions PostgreSQL")
        print("5. Utilisez un VPN pour contourner les restrictions réseau")
