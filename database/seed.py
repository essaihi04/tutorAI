"""
Database Seed Script
Populates the database with initial content: subjects, chapters, lessons, exercises, prompts.
"""
import json
import uuid
import asyncio
from pathlib import Path
from sqlalchemy import text
from app.database import engine, async_session
from app.models.content import Subject, Chapter, Lesson, Exercise
from app.models.prompt import AIPrompt

SEED_DIR = Path(__file__).parent / "seed_data"


async def seed_database():
    async with async_session() as session:
        # Check if already seeded
        result = await session.execute(text("SELECT COUNT(*) FROM subjects"))
        count = result.scalar()
        if count > 0:
            print("Database already seeded. Skipping.")
            return

        print("Seeding database...")

        # 1. Seed Subjects
        with open(SEED_DIR / "subjects.json") as f:
            subjects_data = json.load(f)

        subject_map = {}  # name_fr -> id
        for s in subjects_data:
            subject = Subject(id=uuid.uuid4(), **s)
            session.add(subject)
            subject_map[s["name_fr"]] = subject.id

        await session.flush()
        print(f"  Seeded {len(subjects_data)} subjects")

        # 2. Seed Chapters
        chapter_files = {
            "Physique": "physics_chapters.json",
            "Chimie": "chemistry_chapters.json",
            "SVT": "svt_chapters.json",
            "Mathematiques": "math_chapters.json",
        }

        chapter_map = {}  # (subject_name, chapter_number) -> id
        total_chapters = 0
        for subject_name, filename in chapter_files.items():
            with open(SEED_DIR / filename) as f:
                chapters_data = json.load(f)
            for ch in chapters_data:
                chapter = Chapter(
                    id=uuid.uuid4(),
                    subject_id=subject_map[subject_name],
                    **ch,
                )
                session.add(chapter)
                chapter_map[(subject_name, ch["chapter_number"])] = chapter.id
                total_chapters += 1

        await session.flush()
        print(f"  Seeded {total_chapters} chapters")

        # 3. Seed Lessons (Physics Ch.1 as example)
        lesson_files = list((SEED_DIR / "lessons").glob("*.json"))
        total_lessons = 0
        lesson_map = {}
        for lf in lesson_files:
            with open(lf) as f:
                lesson_data = json.load(f)
            # Determine chapter from filename: phys_ch1_l1.json
            parts = lf.stem.split("_")
            if len(parts) >= 2:
                subj_code = parts[0]  # phys, chim, svt
                ch_num = int(parts[1].replace("ch", ""))
                subj_name = {"phys": "Physique", "chim": "Chimie", "svt": "SVT", "math": "Mathematiques"}.get(subj_code, "Physique")
                chapter_id = chapter_map.get((subj_name, ch_num))
                if chapter_id:
                    lesson = Lesson(
                        id=uuid.uuid4(),
                        chapter_id=chapter_id,
                        title_fr=lesson_data["title_fr"],
                        title_ar=lesson_data["title_ar"],
                        lesson_type=lesson_data.get("lesson_type", "theory"),
                        content=lesson_data.get("content", {}),
                        learning_objectives=lesson_data.get("learning_objectives", []),
                        duration_minutes=lesson_data.get("duration_minutes", 50),
                        order_index=0,
                    )
                    session.add(lesson)
                    lesson_map[lf.stem] = lesson.id
                    total_lessons += 1

        await session.flush()
        print(f"  Seeded {total_lessons} lessons")

        # 4. Seed Exercises
        exercise_files = list((SEED_DIR / "exercises").glob("*.json"))
        total_exercises = 0
        for ef in exercise_files:
            with open(ef) as f:
                exercises_data = json.load(f)
            # Determine lesson from filename: ex_phys_ch1.json
            parts = ef.stem.split("_")
            if len(parts) >= 3:
                subj_code = parts[1]  # phys, chim, svt
                ch_code = parts[2]  # ch1
                lesson_key = f"{subj_code}_{ch_code}_l1"
                lesson_id = lesson_map.get(lesson_key)
                if lesson_id:
                    for ex_data in exercises_data:
                        ex = Exercise(
                            id=uuid.uuid4(),
                            lesson_id=lesson_id,
                            question_text_fr=ex_data["question_text_fr"],
                            question_text_ar=ex_data["question_text_ar"],
                            question_type=ex_data["question_type"],
                            difficulty_tier=ex_data["difficulty_tier"],
                            options=ex_data.get("options", []),
                            correct_answer=ex_data["correct_answer"],
                            explanation_fr=ex_data["explanation_fr"],
                            explanation_ar=ex_data["explanation_ar"],
                            hints=ex_data.get("hints", []),
                            estimated_time_seconds=ex_data.get("estimated_time_seconds", 120),
                            order_index=ex_data.get("order_index", 0),
                        )
                        session.add(ex)
                        total_exercises += 1

        await session.flush()
        print(f"  Seeded {total_exercises} exercises")

        # 5. Seed AI Prompts
        with open(SEED_DIR / "prompts.json") as f:
            prompts_data = json.load(f)
        for p in prompts_data:
            prompt = AIPrompt(
                id=uuid.uuid4(),
                name=p["name"],
                prompt_category=p["prompt_category"],
                template_text=p["template_text"],
                variables=p.get("variables", []),
                language=p.get("language", "fr"),
            )
            session.add(prompt)

        await session.flush()
        print(f"  Seeded {len(prompts_data)} AI prompts")

        await session.commit()
        print("Database seeding complete!")


if __name__ == "__main__":
    asyncio.run(seed_database())
