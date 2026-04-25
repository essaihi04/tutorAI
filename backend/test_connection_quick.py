import asyncio
import asyncpg

async def test_connection():
    """Quick test of Supabase connection with new credentials"""
    
    print("=== Test de connexion Supabase ===\n")
    
    try:
        conn = await asyncpg.connect(
            user="postgres",
            password="fYTDtYBQIsFra0Tn",
            database="postgres",
            host="db.ldeifdnczkzgtxctjlel.supabase.co",
            port=5432,
            timeout=15,
            ssl='require'
        )
        print("✅ Connexion réussie!")
        
        version = await conn.fetchval('SELECT version()')
        print(f"✅ PostgreSQL: {version[:60]}...")
        
        # Check tables
        tables = await conn.fetch("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        table_names = [t['table_name'] for t in tables]
        print(f"✅ Tables trouvées ({len(table_names)}): {table_names}")
        
        await conn.close()
        
        print("\n" + "="*70)
        print("✅ SUCCÈS! La connexion à Supabase fonctionne parfaitement!")
        print("="*70)
        print("\nVous pouvez maintenant:")
        print("1. Démarrer le backend: cd backend && python -m uvicorn app.main:app --reload")
        print("2. Démarrer le frontend: cd frontend && npm run dev")
        print("3. Tester la connexion sur http://localhost:5173/login")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print("\n💡 Vérifiez:")
        print("1. Que le mot de passe est correct")
        print("2. Que votre projet Supabase est actif")
        print("3. Votre connexion Internet")
        return False

if __name__ == "__main__":
    asyncio.run(test_connection())
