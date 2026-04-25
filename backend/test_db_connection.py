import asyncio
import asyncpg
from app.config import get_settings

async def test_connection():
    settings = get_settings()
    print(f"Testing connection to: {settings.database_url}")
    
    # Extract connection params from URL
    # postgresql+asyncpg://postgres:password@host:port/database
    url = settings.database_url.replace("postgresql+asyncpg://", "")
    
    try:
        # Try to connect
        conn = await asyncpg.connect(
            user="postgres",
            password="aYTGWasXrvwHdetZ",
            database="postgres",
            host="db.yzvlmulpqnovduqhhtjf.supabase.co",
            port=5432,
            timeout=10
        )
        print("✓ Connection successful!")
        
        # Test query
        version = await conn.fetchval('SELECT version()')
        print(f"✓ PostgreSQL version: {version}")
        
        # Check if students table exists
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        print(f"✓ Tables found: {[t['table_name'] for t in tables]}")
        
        await conn.close()
        print("✓ Connection closed successfully")
        
    except asyncpg.exceptions.PostgresError as e:
        print(f"✗ PostgreSQL error: {e}")
    except Exception as e:
        print(f"✗ Connection failed: {type(e).__name__}: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())
