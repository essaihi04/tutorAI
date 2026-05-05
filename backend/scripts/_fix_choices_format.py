"""
Migrate choices from plain strings to {"letter": "a", "text": "..."}
and correct_answer from integer index to lowercase letter string.

Affected files introduced by the QCM batch fix scripts:
  - physique/2022-rattrapage  (ex2_q1 – ex2_q6)
  - physique/2020-normale     (ex2_q1 – ex2_q5)
  - physique/2021-normale     (ex2_q1)
  - physique/2022-normale     (ex1_q2a, ex1_q2b, ex4_q5)
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LETTERS = "abcd"

FILES = [
    ROOT / "backend/data/exams/physique/2022-rattrapage/exam.json",
    ROOT / "backend/data/exams/physique/2020-normale/exam.json",
    ROOT / "backend/data/exams/physique/2021-normale/exam.json",
    ROOT / "backend/data/exams/physique/2022-normale/exam.json",
]


def fix_question(q: dict) -> bool:
    """Return True if any change was made."""
    changed = False
    choices = q.get("choices")
    if not choices:
        return False

    # Already in dict format?
    if isinstance(choices[0], dict):
        return False

    # Convert plain strings → {"letter": "a", "text": "..."}
    new_choices = [
        {"letter": LETTERS[i], "text": str(text)}
        for i, text in enumerate(choices)
        if i < len(LETTERS)
    ]
    q["choices"] = new_choices
    changed = True

    # Convert integer correct_answer → letter string
    ca = q.get("correct_answer")
    if isinstance(ca, int):
        letter = LETTERS[ca] if ca < len(LETTERS) else LETTERS[0]
        q["correct_answer"] = letter
        # Also store in correction dict for completeness
        if isinstance(q.get("correction"), dict):
            q["correction"]["correct_answer"] = letter
        changed = True
    elif isinstance(ca, str) and ca.upper() in "ABCD" and ca.isupper():
        # Uppercase letter → lowercase
        q["correct_answer"] = ca.lower()
        if isinstance(q.get("correction"), dict):
            q["correction"]["correct_answer"] = ca.lower()
        changed = True

    return changed


def fix_file(path: Path):
    d = json.loads(path.read_text(encoding="utf-8"))
    total = 0

    for part in d.get("parts", []):
        for ex in part.get("exercises", []):
            for q in ex.get("questions", []):
                if fix_question(q):
                    total += 1
                    print(f"  Fixed {q.get('id','?')} Q{q.get('number','?')}: "
                          f"{len(q['choices'])} choices, correct='{q['correct_answer']}'")
                for sq in q.get("sub_questions", []):
                    if fix_question(sq):
                        total += 1
        for q in part.get("questions", []):
            if fix_question(q):
                total += 1

    if total:
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  -> Saved {total} question(s) in {path.name}\n")
    else:
        print(f"  -> Nothing to fix in {path.name}\n")


def main():
    for f in FILES:
        print(f"=== {f.parent.name}")
        fix_file(f)


if __name__ == "__main__":
    main()
