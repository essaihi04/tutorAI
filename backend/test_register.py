"""Test script to debug registration endpoint"""
import asyncio
import sys
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.models.student import Student, StudentProfile
from app.utils.security import get_password_hash

# Database URL from .env
DATABASE_URL = "postgresql+asyncpg://postgres.yzvlmulpqnovduqhhtjf:aYTGWasXrvwHdetZ@aws-0-us-east-1.pooler.supabase.com:6543/postgres"

async def test_registration():
    """Test student registration"""
    print("🔍 Testing database connection...")
    
    engine = create_async_engine(DATABASE_URL, echo=True)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with async_session() as session:
        try:
            print("\n✅ Database connected!")
            
            # Create student
            print("\n📝 Creating student...")
            student = Student(
                username="testuser_debug",
                email="testdebug@example.com",
                hashed_password=get_password_hash("password123"),
                full_name="Test Debug User",
                preferred_language="fr",
            )
            session.add(student)
            await session.flush()
            print(f"✅ Student created with ID: {student.id}")
            
            # Create profile
            print("\n📝 Creating profile...")
            profile = StudentProfile(student_id=student.id)
            session.add(profile)
            
            # Commit
            print("\n💾 Committing to database...")
            await session.commit()
            await session.refresh(student)
            
            print(f"\n🎉 SUCCESS! Student registered:")
            print(f"   - ID: {student.id}")
            print(f"   - Username: {student.username}")
            print(f"   - Email: {student.email}")
            
        except Exception as e:
            print(f"\n❌ ERROR: {type(e).__name__}")
            print(f"   Message: {str(e)}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
        finally:
            await engine.dispose()

if __name__ == "__main__":
    asyncio.run(test_registration())
