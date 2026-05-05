"""
Fix questions 14-19 in 2022-rattrapage PC (Exercice 2, Ex2 Physique Ondes):
ex2_q1 to ex2_q6 are QCM but labeled as open.
- Change type to 'qcm'
- Add choices[] extracted from pipe-table
- Add correct_answer (0-based index)
- Clean content (remove pipe-table row)
"""

import json, re, pathlib

PATH = pathlib.Path("c:/Users/HP/Desktop/ai-tutor-bac/backend/data/exams/physique/2022-rattrapage/exam.json")

data = json.loads(PATH.read_text(encoding="utf-8"))

# Locate Exercise 2
ex2 = data["parts"][0]["exercises"][1]
assert "Ondes" in ex2["name"], f"Mauvais exercice: {ex2['name']}"

FIXES = {
    "ex2_q1": {
        "type": "qcm",
        "choices": [
            "$N=25\\,\\mathrm{Hz}$",
            "$N=50\\,\\mathrm{Hz}$",
            "$N=100\\,\\mathrm{Hz}$",
            "$N=200\\,\\mathrm{Hz}$"
        ],
        "correct_answer": 1,  # B
    },
    "ex2_q2": {
        "type": "qcm",
        "choices": [
            "$\\tau=0{,}1\\,\\mathrm{s}$",
            "$\\tau=0{,}02\\,\\mathrm{s}$",
            "$\\tau=0{,}01\\,\\mathrm{s}$",
            "$\\tau=0{,}2\\,\\mathrm{s}$"
        ],
        "correct_answer": 2,  # C
    },
    "ex2_q3": {
        "type": "qcm",
        "choices": [
            "$v=2{,}5\\,\\mathrm{m.s^{-1}}$",
            "$v=0{,}25\\,\\mathrm{m.s^{-1}}$",
            "$v=25\\,\\mathrm{m.s^{-1}}$",
            "$v=0{,}4\\,\\mathrm{m.s^{-1}}$"
        ],
        "correct_answer": 0,  # A
    },
    "ex2_q4": {
        "type": "qcm",
        "choices": [
            "$\\lambda=5\\,\\mathrm{cm}$",
            "$\\lambda=2{,}5\\,\\mathrm{cm}$",
            "$\\lambda=0{,}5\\,\\mathrm{m}$",
            "$\\lambda=0{,}25\\,\\mathrm{cm}$"
        ],
        "correct_answer": 0,  # A
    },
    "ex2_q5": {
        "type": "qcm",
        "choices": [
            "14 protons et 6 neutrons",
            "8 protons et 6 neutrons",
            "6 protons et 8 neutrons",
            "6 protons et 14 neutrons"
        ],
        "correct_answer": 2,  # C
    },
    "ex2_q6": {
        "type": "qcm",
        "choices": [
            "$^{14}_{6}\\mathrm{C} \\rightarrow {}^{0}_{+1}\\mathrm{e} + {}^{14}_{5}\\mathrm{B}$",
            "$^{14}_{6}\\mathrm{C} \\rightarrow {}^{0}_{-1}\\mathrm{e} + {}^{14}_{7}\\mathrm{N}$",
            "$^{14}_{6}\\mathrm{C} \\rightarrow {}^{4}_{-1}\\mathrm{He} + {}^{10}_{4}\\mathrm{Be}$",
            "$^{14}_{6}\\mathrm{C} + {}^{0}_{-1}\\mathrm{e} \\rightarrow {}^{14}_{6}\\mathrm{B}$"
        ],
        "correct_answer": 1,  # B
    },
}

def strip_table_from_content(content: str) -> str:
    """Remove trailing pipe-table row(s) and surrounding blank lines."""
    lines = content.split("\n")
    # Drop trailing lines that are pipe-table rows
    while lines and re.match(r"^\s*\|", lines[-1]):
        lines.pop()
    # Drop trailing blank lines
    while lines and not lines[-1].strip():
        lines.pop()
    return "\n".join(lines)

changed = 0
for q in ex2["questions"]:
    qid = q["id"]
    if qid not in FIXES:
        continue
    fix = FIXES[qid]
    q["type"] = fix["type"]
    q["choices"] = fix["choices"]
    q["correct_answer"] = fix["correct_answer"]
    # Clean content
    q["content"] = strip_table_from_content(q["content"])
    changed += 1
    print(f"  Fixed {qid} ({q['number']}) -> qcm, correct={fix['correct_answer']}")

print(f"\nTotal fixed: {changed}/6")
PATH.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
print("Saved.")
