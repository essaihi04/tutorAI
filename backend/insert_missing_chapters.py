"""
Insert missing Physics and Chemistry chapters into the database.
Run this script to fix the missing chapters issue.
"""
import json
import os
from supabase import create_client

# Get Supabase credentials from environment or use defaults
SUPABASE_URL = os.getenv("SUPABASE_URL", "https://yzvlmulpqnovduqhhtjf.supabase.co")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "YOUR_SERVICE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def insert_chapters():
    print("🔧 Inserting missing chapters for Physique and Chimie...")
    
    # Get subject IDs
    result = supabase.table('subjects').select('id, name_fr').execute()
    subjects = {s['name_fr']: s['id'] for s in result.data}
    
    print(f"Found subjects: {subjects}")
    
    chapter_files = [
        ("database/seed_data/physics_chapters.json", "Physique"),
        ("database/seed_data/chemistry_chapters.json", "Chimie"),
    ]
    
    for filename, subject_name in chapter_files:
        if not os.path.exists(filename):
            print(f"⚠️ File not found: {filename}")
            continue
            
        chapters_data = load_json(filename)
        subject_id = subjects.get(subject_name)
        
        if not subject_id:
            print(f"⚠️ Subject not found: {subject_name}")
            continue
        
        print(f"\n📚 Processing {subject_name} (ID: {subject_id})")
        
        # Check existing chapters for this subject
        existing = supabase.table('chapters').select('chapter_number').eq('subject_id', subject_id).execute()
        existing_numbers = {ch['chapter_number'] for ch in existing.data}
        
        print(f"   Existing chapters: {existing_numbers}")
        
        inserted = 0
        for data in chapters_data:
            chapter_num = data['chapter_number']
            if chapter_num in existing_numbers:
                print(f"   Chapter {chapter_num} already exists, skipping")
                continue
                
            chapter_data = {
                'subject_id': subject_id,
                'chapter_number': data['chapter_number'],
                'title_fr': data['title_fr'],
                'title_ar': data['title_ar'],
                'description_fr': data['description_fr'],
                'description_ar': data['description_ar'],
                'difficulty_level': data['difficulty_level'],
                'estimated_hours': data['estimated_hours'],
                'order_index': data['order_index']
            }
            
            result = supabase.table('chapters').insert(chapter_data).execute()
            if result.data:
                inserted += 1
                print(f"   ✓ Inserted chapter {chapter_num}: {data['title_fr']}")
        
        print(f"✅ Inserted {inserted} new chapters for {subject_name}")
    
    print("\n🎉 Done!")

if __name__ == "__main__":
    insert_chapters()
