"""
Batch fix: convert open questions with QCM pipe-tables to type=qcm.
Covers: 2020-normale ex2 (Q1-Q5), 2021-normale ex2 (Q1), 2022-normale ex1 (Q2.1, Q2.2) + ex4 (Q1.1).
"""
import json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ── Correct answer map (0-based A=0 B=1 C=2 D=3) ────────────────────────────
ANSWER_MAP = {
    # 2020-normale
    ('2020-normale', 'ex2_q1'): 1,  # B
    ('2020-normale', 'ex2_q2'): 2,  # C
    ('2020-normale', 'ex2_q3'): 2,  # C
    ('2020-normale', 'ex2_q4'): 3,  # D
    ('2020-normale', 'ex2_q5'): 3,  # D
    # 2021-normale
    ('2021-normale', 'ex2_q1'): 2,  # C
    # 2022-normale
    ('2022-normale', 'ex1_q2a'): 0,  # A
    ('2022-normale', 'ex1_q2b'): 1,  # B
    ('2022-normale', 'ex4_q5'):  1,  # B
}


def parse_qcm_table(content: str) -> tuple[list[str], str]:
    """
    Extract [choice_A, choice_B, choice_C, choice_D] from the pipe-table at the
    bottom of the content string, and return (choices, content_without_table).

    Handles:
      • Single row:  | A | ... | B | ... | C | ... | D | ... |
      • Two rows:    | A | ... | C | ... |
                     | B | ... | D | ... |
      • Three choices: | A | ... | B | ... | C | ... |
    """
    lines = content.split('\n')
    table_lines = []
    # Collect trailing pipe-table rows
    for line in reversed(lines):
        if re.match(r'^\s*\|', line.strip()):
            table_lines.insert(0, line.strip())
        elif table_lines:
            break   # stop at first non-table line from the bottom

    # Remove table lines from content
    clean_lines = lines[:len(lines) - len(table_lines)]
    while clean_lines and not clean_lines[-1].strip():
        clean_lines.pop()
    clean_content = '\n'.join(clean_lines)

    # Parse the table to collect cell pairs (label, text)
    cells: dict[str, str] = {}
    for row in table_lines:
        # Remove outer |
        inner = row.strip().lstrip('|').rstrip('|')
        # Split on | but preserve LaTeX \| inside – naïve split is usually fine
        parts = [p.strip() for p in inner.split('|')]
        # pairs: label, value, label, value, ...
        i = 0
        while i + 1 < len(parts):
            lbl = parts[i].strip().upper()
            val = parts[i + 1].strip()
            if re.match(r'^[A-D]$', lbl):
                cells[lbl] = val
            i += 2

    # Build ordered choices [A, B, C, D] (skip missing labels for 3-choice QCMs)
    choices = [cells[k] for k in sorted(cells.keys()) if k in cells]
    return choices, clean_content


def fix_file(session: str, fpath: str):
    path = ROOT / fpath
    d = json.loads(path.read_text(encoding='utf-8'))
    changed = 0

    for ex in d['parts'][0]['exercises']:
        for q in ex.get('questions', []):
            key = (session, q.get('id', ''))
            if key not in ANSWER_MAP:
                continue
            if q['type'] != 'open':
                print(f'  SKIP {q["id"]}: already type={q["type"]}')
                continue

            choices, clean_content = parse_qcm_table(q['content'])
            if not choices:
                print(f'  ERROR {q["id"]}: could not parse table')
                continue

            q['type'] = 'qcm'
            q['choices'] = choices
            q['correct_answer'] = ANSWER_MAP[key]
            q['content'] = clean_content
            changed += 1
            print(f'  Fixed {q["id"]} Q{q["number"]}: {len(choices)} choices, correct={ANSWER_MAP[key]} ({chr(65+ANSWER_MAP[key])})')

    if changed:
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')
        print(f'  -> Saved ({changed} questions)\n')
    else:
        print(f'  -> Nothing changed\n')


def main():
    targets = [
        ('2020-normale', 'backend/data/exams/physique/2020-normale/exam.json'),
        ('2021-normale', 'backend/data/exams/physique/2021-normale/exam.json'),
        ('2022-normale', 'backend/data/exams/physique/2022-normale/exam.json'),
    ]
    for session, fpath in targets:
        print(f'=== {session}')
        fix_file(session, fpath)


if __name__ == '__main__':
    main()
