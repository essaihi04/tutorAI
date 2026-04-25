"""Quick script to regenerate study plan with session_type support."""
import os, dotenv, asyncio, sys
sys.path.insert(0, '.')
dotenv.load_dotenv('.env')

from app.services.study_plan_service import study_plan_service
from supabase import create_client

url = os.environ['SUPABASE_URL']
key = os.environ['SUPABASE_SERVICE_ROLE_KEY']
sb = create_client(url, key)

async def main():
    # Find the student who has diagnostic results
    diag_check = sb.table('diagnostic_results').select('student_id').limit(1).execute()
    if not diag_check.data:
        print('No diagnostic results found at all')
        return
    student_id = diag_check.data[0]['student_id']
    print(f"Student: {student_id}")
    
    # Get latest diagnostic scores
    diag = sb.table('diagnostic_results').select(
        'score, subjects(name_fr)'
    ).eq('student_id', student_id).eq(
        'evaluation_type', 'diagnostic'
    ).order('created_at', desc=True).execute()
    
    scores = {}
    seen = set()
    for r in diag.data:
        subj = r.get('subjects', {}).get('name_fr')
        if subj and subj not in seen:
            scores[subj] = float(r.get('score', 0))
            seen.add(subj)
    print(f"Scores: {scores}")
    
    if not scores:
        print("No diagnostic scores found!")
        return
    
    # Regenerate plan
    result = await study_plan_service.generate_plan(student_id, scores)
    plan_id = result['plan_id']
    print(f"Plan generated: {result['sessions_count']} sessions")
    print(f"Phase split: {result.get('phase_split', {})}")
    
    # Check session types
    sessions = sb.table('study_plan_sessions').select(
        'session_type'
    ).eq('plan_id', plan_id).execute()
    
    types = {}
    for r in sessions.data:
        t = r.get('session_type', '?')
        types[t] = types.get(t, 0) + 1
    print(f"Session types distribution: {types}")

asyncio.run(main())
