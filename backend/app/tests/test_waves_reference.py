import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs

ROOT = Path(__file__).resolve().parents[3]


def test_waves_preserves_existing_progress_and_covers_reference_experiments():
    course = json.loads((ROOT / 'backend/data/courses/phys_ch1_waves_course_v1.json').read_text(encoding='utf-8'))
    slides = [s for a in course['activities'] for s in a['slides']]
    ids = [s['id'] for s in slides]
    assert len(set(ids)) == len(ids)
    for a in range(5):
        for s in range(1, 3):
            assert f'waves_a{a:02d}_s{s:02d}' in ids
    variants = {
        parse_qs(urlparse(s['visual'].get('url', '')).query).get('variant', [''])[0]
        for s in slides if s['visual']['kind'] == 'simulation'
    }
    assert variants == {'cord', 'spring', 'water', 'sound', 'vacuum', 'superposition', 'medium', 'progressive'}
    assert all(not s['question']['advance_on_timeout'] for s in slides)
    assert any(s['question']['type'] == 'open' for s in slides)
    assert any('table' in s['screen_content'] for s in slides)
    assert course['pedagogical_reference']['classroom_minutes'] == 300
    assert course['estimated_minutes'] == sum(a['duration_minutes'] for a in course['activities'])
