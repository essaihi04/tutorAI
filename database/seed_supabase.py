"""
Seed script for Supabase database
Populates the database with initial data from JSON files
"""
import asyncio
import json
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

# Import models
import sys
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from app.models.content import Subject, Chapter, Lesson, Exercise, PedagogicalSituation
from app.models.prompt import AIPrompt

# Supabase connection string
# Replace YOUR_DB_PASSWORD with your actual Supabase database password
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://postgres.yzvlmulpqnovduqhhtjf:YOUR_DB_PASSWORD@aws-0-us-east-1.pooler.supabase.com:6543/postgres"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def load_json(filepath: str):
    """Load JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_json_sync(filepath: str):
    """Load JSON file synchronously"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


async def seed_subjects(session: AsyncSession):
    """Seed subjects table"""
    print("\n📚 Seeding subjects...")
    subjects_data = await load_json("seed_data/subjects.json")
    
    for data in subjects_data:
        subject = Subject(
            name_fr=data["name_fr"],
            name_ar=data["name_ar"],
            description_fr=data["description_fr"],
            description_ar=data["description_ar"],
            icon=data["icon"],
            color=data["color"],
            order_index=data["order_index"]
        )
        session.add(subject)
    
    await session.commit()
    print(f"✅ Seeded {len(subjects_data)} subjects")


async def seed_chapters(session: AsyncSession):
    """Seed chapters table"""
    print("\n📖 Seeding chapters...")
    
    # Get subjects
    result = await session.execute(text("SELECT id, name_fr FROM subjects ORDER BY order_index"))
    subjects = {row[1]: row[0] for row in result}
    
    chapter_files = [
        ("physics_chapters.json", "Physique"),
        ("chemistry_chapters.json", "Chimie"),
        ("svt_chapters.json", "SVT"),
        ("math_chapters.json", "Mathematiques")
    ]
    
    total_chapters = 0
    for filename, subject_name in chapter_files:
        filepath = f"seed_data/{filename}"
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            continue
            
        chapters_data = await load_json(filepath)
        subject_id = subjects.get(subject_name)
        
        if not subject_id:
            print(f"⚠️  Subject not found: {subject_name}")
            continue
        
        for data in chapters_data:
            chapter = Chapter(
                subject_id=subject_id,
                chapter_number=data["chapter_number"],
                title_fr=data["title_fr"],
                title_ar=data["title_ar"],
                description_fr=data["description_fr"],
                description_ar=data["description_ar"],
                difficulty_level=data["difficulty_level"],
                estimated_hours=data["estimated_hours"],
                order_index=data["order_index"]
            )
            session.add(chapter)
            total_chapters += 1
    
    await session.commit()
    print(f"✅ Seeded {total_chapters} chapters")


async def seed_lessons(session: AsyncSession):
    """Seed lessons table"""
    print("\n📝 Seeding lessons...")
    
    # Get chapters
    result = await session.execute(text("SELECT id, title_fr FROM chapters"))
    chapters = {row[1]: row[0] for row in result}
    svt_chapters_data = load_json_sync("seed_data/svt_chapters.json")
    
    lesson_files = [
        ("lessons/phys_ch1_l1.json", "Ondes mecaniques progressives"),
    ]

    # Auto-discover SVT and Math lesson files
    auto_discover = [
        ("svt", "seed_data/svt_chapters.json"),
        ("math", "seed_data/math_chapters.json"),
    ]

    for prefix, chapters_json_path in auto_discover:
        if not os.path.exists(chapters_json_path):
            print(f"⚠️  File not found: {chapters_json_path}")
            continue

        subject_chapters_data = load_json_sync(chapters_json_path)
        discovered_files = sorted(
            filename
            for filename in os.listdir("seed_data/lessons")
            if filename.startswith(f"{prefix}_ch") and filename.endswith(".json")
        )

        for filename in discovered_files:
            try:
                chapter_number = int(filename.split("_")[1].replace("ch", ""))
            except (IndexError, ValueError):
                print(f"⚠️  Invalid {prefix} lesson filename: {filename}")
                continue

            chapter_title = next(
                (
                    ch["title_fr"]
                    for ch in subject_chapters_data
                    if ch["chapter_number"] == chapter_number
                ),
                None,
            )

            if not chapter_title:
                print(f"⚠️  Chapter title not found for {prefix} lesson file: {filename}")
                continue

            lesson_files.append((f"lessons/{filename}", chapter_title))
    
    total_lessons = 0
    for filename, chapter_title in lesson_files:
        filepath = f"seed_data/{filename}"
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            continue
            
        lesson_data = await load_json(filepath)
        chapter_id = chapters.get(chapter_title)
        
        if not chapter_id:
            print(f"⚠️  Chapter not found: {chapter_title}")
            continue
        
        lesson = Lesson(
            chapter_id=chapter_id,
            title_fr=lesson_data["title_fr"],
            title_ar=lesson_data["title_ar"],
            lesson_type=lesson_data["lesson_type"],
            content=lesson_data["content"],
            learning_objectives=lesson_data["learning_objectives"],
            duration_minutes=lesson_data["duration_minutes"],
            media_resources=lesson_data.get("media_resources", []),
            order_index=0
        )
        session.add(lesson)
        total_lessons += 1
    
    await session.commit()
    print(f"✅ Seeded {total_lessons} lessons")


async def seed_exercises(session: AsyncSession):
    """Seed exercises table"""
    print("\n✏️  Seeding exercises...")
    
    # Get lessons
    result = await session.execute(text("SELECT id, title_fr FROM lessons"))
    lessons = {row[1]: row[0] for row in result}
    
    exercise_files = [
        ("exercises/ex_phys_ch1.json", "Introduction aux ondes mecaniques progressives")
    ]
    
    total_exercises = 0
    for filename, lesson_title in exercise_files:
        filepath = f"seed_data/{filename}"
        if not os.path.exists(filepath):
            print(f"⚠️  File not found: {filepath}")
            continue
            
        exercises_data = await load_json(filepath)
        lesson_id = lessons.get(lesson_title)
        
        if not lesson_id:
            print(f"⚠️  Lesson not found: {lesson_title}")
            continue
        
        for data in exercises_data:
            exercise = Exercise(
                lesson_id=lesson_id,
                question_text_fr=data["question_text_fr"],
                question_text_ar=data["question_text_ar"],
                question_type=data["question_type"],
                difficulty_tier=data["difficulty_tier"],
                options=data["options"],
                correct_answer=data["correct_answer"],
                explanation_fr=data["explanation_fr"],
                explanation_ar=data["explanation_ar"],
                hints=data["hints"],
                estimated_time_seconds=data["estimated_time_seconds"],
                order_index=data["order_index"]
            )
            session.add(exercise)
            total_exercises += 1
    
    await session.commit()
    print(f"✅ Seeded {total_exercises} exercises")


async def seed_prompts(session: AsyncSession):
    """Seed AI prompts table"""
    print("\n🤖 Seeding AI prompts...")
    
    filepath = "seed_data/prompts.json"
    if not os.path.exists(filepath):
        print(f"⚠️  File not found: {filepath}")
        return
    
    prompts_data = await load_json(filepath)
    
    for data in prompts_data:
        prompt = AIPrompt(
            prompt_type=data["prompt_type"],
            phase=data.get("phase"),
            template_text=data["template_text"],
            variables=data.get("variables", []),
            language=data.get("language", "fr")
        )
        session.add(prompt)
    
    await session.commit()
    print(f"✅ Seeded {len(prompts_data)} AI prompts")


async def main():
    """Main seeding function"""
    print("🌱 Starting Supabase database seeding...")
    print(f"📍 Database: {DATABASE_URL.split('@')[1].split('/')[0]}")
    
    async with async_session() as session:
        try:
            # Seed in order (respecting foreign key constraints)
            await seed_subjects(session)
            await seed_chapters(session)
            await seed_lessons(session)
            await seed_exercises(session)
            await seed_prompts(session)
            
            print("\n✅ Database seeding completed successfully!")
            print("\n📊 Summary:")
            
            # Count records
            result = await session.execute(text("SELECT COUNT(*) FROM subjects"))
            print(f"   - Subjects: {result.scalar()}")
            
            result = await session.execute(text("SELECT COUNT(*) FROM chapters"))
            print(f"   - Chapters: {result.scalar()}")
            
            result = await session.execute(text("SELECT COUNT(*) FROM lessons"))
            print(f"   - Lessons: {result.scalar()}")
            
            result = await session.execute(text("SELECT COUNT(*) FROM exercises"))
            print(f"   - Exercises: {result.scalar()}")
            
            result = await session.execute(text("SELECT COUNT(*) FROM ai_prompts"))
            print(f"   - AI Prompts: {result.scalar()}")
            
        except Exception as e:
            print(f"\n❌ Error during seeding: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(main())
