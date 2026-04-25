import asyncio
import asyncpg
import socket

async def test_supabase_connection():
    """Test Supabase connection with different approaches"""
    
    # Approach 1: Try to get IPv4 address
    print("=== Approach 1: Resolving hostname ===")
    try:
        hostname = "db.yzvlmulpqnovduqhhtjf.supabase.co"
        addrs = socket.getaddrinfo(hostname, 5432, socket.AF_INET, socket.SOCK_STREAM)
        if addrs:
            ipv4_addr = addrs[0][4][0]
            print(f"✓ Resolved IPv4: {ipv4_addr}")
            
            # Try connecting with IP
            print(f"\n=== Approach 2: Connecting with IPv4 address ===")
            try:
                conn = await asyncpg.connect(
                    user="postgres",
                    password="aYTGWasXrvwHdetZ",
                    database="postgres",
                    host=ipv4_addr,
                    port=5432,
                    timeout=10,
                    server_settings={'jit': 'off'}
                )
                print("✓ Connection successful with IPv4!")
                version = await conn.fetchval('SELECT version()')
                print(f"✓ PostgreSQL: {version[:50]}...")
                await conn.close()
                return True
            except Exception as e:
                print(f"✗ IPv4 connection failed: {e}")
        else:
            print("✗ No IPv4 address found")
    except socket.gaierror as e:
        print(f"✗ DNS resolution failed: {e}")
    
    # Approach 3: Try with connection pooler (port 6543)
    print(f"\n=== Approach 3: Using connection pooler (port 6543) ===")
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="aYTGWasXrvwHdetZ",
            database="postgres",
            host="db.yzvlmulpqnovduqhhtjf.supabase.co",
            port=6543,
            timeout=10
        )
        print("✓ Connection successful with pooler!")
        await conn.close()
        return True
    except Exception as e:
        print(f"✗ Pooler connection failed: {e}")
    
    return False

if __name__ == "__main__":
    success = asyncio.run(test_supabase_connection())
    if not success:
        print("\n❌ All connection attempts failed.")
        print("\n💡 Solutions:")
        print("1. Start Docker Desktop and use local PostgreSQL")
        print("2. Check your firewall/antivirus settings")
        print("3. Try using a VPN")
        print("4. Contact your network administrator")
