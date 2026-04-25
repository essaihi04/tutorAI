import asyncio
import asyncpg

async def test_pooler():
    """Test connection using Supabase connection pooler (port 6543)"""
    
    print("=== Test 1: Connection Pooler (Transaction Mode - Port 6543) ===")
    try:
        # Supabase connection pooler uses port 6543 in transaction mode
        conn = await asyncpg.connect(
            user="postgres",
            password="aYTGWasXrvwHdetZ",
            database="postgres",
            host="aws-0-eu-central-1.pooler.supabase.com",
            port=6543,
            timeout=15
        )
        print("✓ Connection successful with pooler!")
        
        version = await conn.fetchval('SELECT version()')
        print(f"✓ PostgreSQL: {version[:60]}...")
        
        # Check tables
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        print(f"✓ Tables: {[t['table_name'] for t in tables]}")
        
        await conn.close()
        print("\n✓ SUCCESS! Use this connection string:")
        print("postgresql+asyncpg://postgres:aYTGWasXrvwHdetZ@aws-0-eu-central-1.pooler.supabase.com:6543/postgres")
        return True
        
    except Exception as e:
        print(f"✗ Pooler connection failed: {e}")
    
    print("\n=== Test 2: Session Pooler (Port 5432) ===")
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="aYTGWasXrvwHdetZ",
            database="postgres",
            host="aws-0-eu-central-1.pooler.supabase.com",
            port=5432,
            timeout=15
        )
        print("✓ Connection successful with session pooler!")
        await conn.close()
        print("\n✓ SUCCESS! Use this connection string:")
        print("postgresql+asyncpg://postgres:aYTGWasXrvwHdetZ@aws-0-eu-central-1.pooler.supabase.com:5432/postgres")
        return True
        
    except Exception as e:
        print(f"✗ Session pooler failed: {e}")
    
    return False

if __name__ == "__main__":
    success = asyncio.run(test_pooler())
    if not success:
        print("\n❌ All connection attempts failed.")
        print("\n💡 Vérifiez:")
        print("1. Que votre projet Supabase est actif")
        print("2. Que le mot de passe est correct")
        print("3. Votre connexion Internet")
