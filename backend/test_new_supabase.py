import asyncio
import asyncpg

async def test_new_supabase():
    """Test connection to new Supabase project"""
    
    project_ref = "ldeifdnczkzgtxctjlel"
    hostname = f"db.{project_ref}.supabase.co"
    
    print(f"=== Test de connexion au nouveau projet Supabase ===")
    print(f"Projet: {project_ref}")
    print(f"Hostname: {hostname}\n")
    
    # You need to get the database password from Supabase Dashboard
    print("⚠️  IMPORTANT: Vous devez obtenir le mot de passe de la base de données")
    print("   1. Allez sur https://supabase.com/dashboard")
    print("   2. Sélectionnez votre projet 'ldeifdnczkzgtxctjlel'")
    print("   3. Allez dans Settings > Database")
    print("   4. Copiez le mot de passe de la base de données")
    print()
    
    password = input("Entrez le mot de passe de la base de données: ").strip()
    
    if not password:
        print("❌ Mot de passe requis!")
        return False
    
    print("\n=== Test de connexion ===")
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
        print(f"✅ Tables trouvées: {[t['table_name'] for t in tables]}")
        
        await conn.close()
        
        print(f"\n{'='*70}")
        print("✅ SUCCÈS! Mettez à jour votre fichier .env avec:")
        print(f"{'='*70}")
        print(f"DATABASE_URL=postgresql+asyncpg://postgres:{password}@{hostname}:5432/postgres")
        print(f"DATABASE_URL_SYNC=postgresql://postgres:{password}@{hostname}:5432/postgres")
        print(f"{'='*70}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        print("\n💡 Vérifiez:")
        print("1. Que le mot de passe est correct")
        print("2. Que votre projet Supabase est actif")
        print("3. Votre connexion Internet")
        return False

if __name__ == "__main__":
    asyncio.run(test_new_supabase())
