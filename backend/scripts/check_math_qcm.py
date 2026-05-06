import json, pathlib

math_dir = pathlib.Path('backend/data/exams/mathematiques')
found = 0
for year_dir in sorted(math_dir.iterdir()):
    exam = year_dir / 'exam.json'
    if not exam.exists():
        continue
    data = json.loads(exam.read_text(encoding='utf-8'))
    for part in data.get('parts', []):
        for ex in part.get('exercises', []):
            for q in ex.get('questions', []):
                if q.get('type') == 'qcm':
                    found += 1
                    print(f"{year_dir.name}: {q.get('content','')[:80]}")
                    print(f"  choices: {[c.get('letter','') + ') ' + c.get('text','')[:40] for c in q.get('choices', [])]}")
                    print(f"  correct: {q.get('correct_answer','')}")

print(f'\nTotal QCM in math: {found}')
