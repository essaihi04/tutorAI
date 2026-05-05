"""Verify that all qcm questions have the correct choices/correct_answer format."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FILES = [
    ROOT / "backend/data/exams/physique/2022-rattrapage/exam.json",
    ROOT / "backend/data/exams/physique/2020-normale/exam.json",
    ROOT / "backend/data/exams/physique/2021-normale/exam.json",
    ROOT / "backend/data/exams/physique/2022-normale/exam.json",
]

errors = []
ok = 0

for fpath in FILES:
    d = json.loads(fpath.read_text(encoding="utf-8"))
    for part in d.get("parts", []):
        for ex in part.get("exercises", []):
            for q in ex.get("questions", []):
                if q.get("type") != "qcm":
                    continue
                qid = q.get("id", "?")
                choices = q.get("choices", [])
                ca = q.get("correct_answer")
                # choices must be list of dicts with 'text'
                if not choices:
                    errors.append(f"{fpath.parent.name} {qid}: choices empty")
                elif not isinstance(choices[0], dict):
                    errors.append(f"{fpath.parent.name} {qid}: choices are strings, not dicts")
                elif "text" not in choices[0]:
                    errors.append(f"{fpath.parent.name} {qid}: no 'text' key in choices[0]")
                # correct_answer must be a string letter
                if not isinstance(ca, str):
                    errors.append(f"{fpath.parent.name} {qid}: correct_answer={ca!r} not a string")
                else:
                    ok += 1
                    print(f"  OK {qid}: {len(choices)} choices, correct='{ca}', letter={choices[0].get('letter')}")

print()
if errors:
    print(f"ERRORS ({len(errors)}):")
    for e in errors:
        print(f"  {e}")
else:
    print(f"All {ok} qcm questions are correctly formatted.")
