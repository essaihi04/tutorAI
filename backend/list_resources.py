import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from app.supabase_client import get_supabase

s = get_supabase()
r = s.table("lesson_resources").select("id,title,resource_type,lesson_id").execute()

print(f"Total resources: {len(r.data)}")
for x in r.data:
    title = x.get("title", "?")[:40]
    rtype = x.get("resource_type", "?")
    lesson = x.get("lesson_id", "?")[:8] if x.get("lesson_id") else "None"
    print(f"  {title} | {rtype} | lesson={lesson}...")
