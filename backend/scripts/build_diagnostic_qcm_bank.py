"""
Build a QCM bank from real BAC exam JSON files (SVT + Physique-Chimie).
Extracts:
  - SVT Part 1 QCM sub_questions (4 choices, correct_answer)
  - SVT Part 1 Vrai/Faux sub_questions (converted to 2-choice QCM)
  - PC QCM questions (already converted from open in previous sessions)

Output: backend/data/diagnostic_qcm_bank.json
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMS_DIR = ROOT / "backend/data/exams"
OUTPUT = ROOT / "backend/data/diagnostic_qcm_bank.json"


def detect_svt_domain(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["géologie", "faille", "subduction", "métamorphisme", "magma",
                              "collision", "plaque", "sismique", "lithosphère", "obduction",
                              "nappe de charriage", "ophiolite", "péridotite", "basalte", "granite",
                              "anatexie", "auréole"]):
        return "Géologie"
    if any(k in t for k in ["génétique", "gène", "allèle", "chromosom", "adn", "arn",
                              "protéine", "mutation", "hérédité", "phénotype", "génotype",
                              "dihybridisme", "test cross", "électrophorèse", "drépanocytose"]):
        return "Génétique"
    if any(k in t for k in ["déchet", "environnement", "biogaz", "lixiviat", "compostage",
                              "pollution", "effet de serre", "décharge", "recyclage", "tri"]):
        return "Environnement"
    if any(k in t for k in ["glycolyse", "atp", "mitochondrie", "fermentation", "pyruvate",
                              "glucose", "krebs", "muscle", "contraction", "énergie", "nadh",
                              "respiration cellulaire", "éthanol", "acide lactique", "bilan"]):
        return "Métabolisme énergétique"
    if any(k in t for k in ["neurone", "synapse", "influx", "réflexe", "nerf", "arc réflexe",
                              "intégration", "stimulus"]):
        return "Neurophysiologie"
    if any(k in t for k in ["hormone", "immunologie", "anticorps", "lymphocyte", "sida",
                              "système immunitaire", "antigène"]):
        return "Immunologie"
    return "SVT"


def detect_pc_domain(exercise_name: str, content: str = "") -> str:
    txt = (exercise_name + " " + content).lower()
    if any(k in txt for k in ["chimie", "acide", "base", "ph", "électrolyse", "oxydation",
                                "réduction", "solution", "dosage", "titrage", "estérification"]):
        return "Chimie"
    if any(k in txt for k in ["mécanique", "mouvement", "force", "pendule", "ressort",
                                "énergie cinétique", "dynamique", "trajectoire"]):
        return "Mécanique"
    if any(k in txt for k in ["électricité", "circuit", "condensateur", "bobine", "courant",
                                "tension", "résistance", "inductance", "capacité"]):
        return "Électricité"
    if any(k in txt for k in ["optique", "lumière", "réfraction", "lentille", "diffraction"]):
        return "Optique"
    if any(k in txt for k in ["ondes", "signal", "propagation", "période", "fréquence",
                                "ultrason", "célérité"]):
        return "Ondes"
    if any(k in txt for k in ["nucléaire", "radioactivité", "désintégration", "isotope"]):
        return "Physique nucléaire"
    return "Physique-Chimie"


def extract_svt_qcm(exam_path: Path, year: int, session: str) -> list:
    """Extract QCM and Vrai/Faux sub_questions from SVT Part 1."""
    try:
        data = json.loads(exam_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ERROR {exam_path}: {e}")
        return []

    questions = []
    for part in data.get("parts", []):
        part_name = part.get("name", "")
        is_part1 = ("restitution" in part_name.lower()
                    or "première partie" in part_name.lower()
                    or part_name.lower().startswith("part"))
        if not is_part1:
            continue

        for q in part.get("questions", []):
            q_type = q.get("type", "")
            parent_content = q.get("content", "")

            if q_type == "qcm":
                for sq in q.get("sub_questions", []):
                    choices = sq.get("choices", [])
                    corr = sq.get("correction", {})
                    correct = corr.get("correct_answer", "")
                    if not choices or not correct:
                        continue
                    sq_content = sq.get("content", parent_content).strip()
                    if not sq_content:
                        continue
                    domain = detect_svt_domain(sq_content + " " + parent_content)
                    questions.append({
                        "subject": "SVT",
                        "domain": domain,
                        "year": year,
                        "session": session,
                        "content": sq_content,
                        "choices": [{"letter": c["letter"], "text": c["text"]}
                                    for c in choices if "letter" in c and "text" in c],
                        "correct_answer": correct.lower(),
                        "type": "qcm",
                    })

            elif q_type == "vrai_faux":
                for sq in q.get("sub_questions", []):
                    corr = sq.get("correction", {})
                    correct = corr.get("correct_answer", "")
                    if not correct:
                        continue
                    sq_content = sq.get("content", "").strip()
                    if not sq_content:
                        continue
                    domain = detect_svt_domain(sq_content + " " + parent_content)
                    questions.append({
                        "subject": "SVT",
                        "domain": domain,
                        "year": year,
                        "session": session,
                        "content": sq_content,
                        "choices": [
                            {"letter": "a", "text": "Vrai"},
                            {"letter": "b", "text": "Faux"},
                        ],
                        "correct_answer": "a" if correct.lower() == "vrai" else "b",
                        "type": "vrai_faux",
                    })

    return questions


def extract_pc_qcm(exam_path: Path, year: int, session: str) -> list:
    """Extract QCM questions from PC exams (only already-typed qcm)."""
    try:
        data = json.loads(exam_path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ERROR {exam_path}: {e}")
        return []

    questions = []
    for part in data.get("parts", []):
        for ex in part.get("exercises", []):
            ex_name = ex.get("name", "")
            for q in ex.get("questions", []):
                if q.get("type") != "qcm":
                    continue
                choices = q.get("choices", [])
                correct = q.get("correct_answer", "")
                content = q.get("content", "").strip()
                if not choices or not correct or not content:
                    continue
                # Skip if choices are not dicts with 'text'
                if not isinstance(choices[0], dict) or "text" not in choices[0]:
                    continue
                domain = detect_pc_domain(ex_name, content)
                questions.append({
                    "subject": "Physique-Chimie",
                    "domain": domain,
                    "year": year,
                    "session": session,
                    "source_exercise": ex_name,
                    "content": content,
                    "choices": [{"letter": c.get("letter", chr(97 + i)), "text": c["text"]}
                                for i, c in enumerate(choices)],
                    "correct_answer": correct.lower() if isinstance(correct, str) else str(correct),
                    "type": "qcm",
                })
    return questions


MATH_MANUAL_PATH = ROOT / "backend/data/math_qcm_manual.json"


def load_math_manual() -> list:
    """Load handcrafted Math QCM questions."""
    questions = json.loads(MATH_MANUAL_PATH.read_text(encoding="utf-8"))
    for q in questions:
        q["source"] = "entrainement"
    return questions


def main():
    all_questions = []

    # ── SVT ──────────────────────────────────────────────────────────────────
    svt_dir = EXAMS_DIR / "svt"
    SVT_DIR_NAMES = {
        (2021, "rattrapage"): "2021-ratrrapage",  # known typo
    }
    for year in range(2017, 2026):
        for session in ["normale", "rattrapage"]:
            dir_name = SVT_DIR_NAMES.get((year, session), f"{year}-{session}")
            exam_path = svt_dir / dir_name / "exam.json"
            if not exam_path.exists():
                continue
            qs = extract_svt_qcm(exam_path, year, session.capitalize())
            if qs:
                print(f"  SVT {year} {session}: {len(qs)} questions")
            all_questions.extend(qs)

    # ── PC ───────────────────────────────────────────────────────────────────
    pc_dir = EXAMS_DIR / "physique"
    for year in range(2016, 2026):
        for session in ["normale", "rattrapage"]:
            exam_path = pc_dir / f"{year}-{session}" / "exam.json"
            if not exam_path.exists():
                continue
            qs = extract_pc_qcm(exam_path, year, session.capitalize())
            if qs:
                print(f"  PC {year} {session}: {len(qs)} questions")
            all_questions.extend(qs)

    # ── Math (manual QCM) ────────────────────────────────────────────────────
    math_qs = load_math_manual()
    print(f"  Math manuel: {len(math_qs)} questions")
    all_questions.extend(math_qs)

    # ── Deduplicate (by first 80 chars of content) ───────────────────────────
    seen: set[str] = set()
    unique: list[dict] = []
    for q in all_questions:
        key = re.sub(r"\s+", " ", q["content"][:80]).lower().strip()
        if key not in seen:
            seen.add(key)
            unique.append(q)

    # ── Assign clean IDs ─────────────────────────────────────────────────────
    for i, q in enumerate(unique, 1):
        q["id"] = f"q{i:03d}"

    # ── Stats ────────────────────────────────────────────────────────────────
    subjects = {}
    domains: dict[str, int] = {}
    for q in unique:
        subjects[q["subject"]] = subjects.get(q["subject"], 0) + 1
        domains[q["domain"]] = domains.get(q["domain"], 0) + 1

    bank = {
        "version": "1.0",
        "total": len(unique),
        "by_subject": subjects,
        "by_domain": domains,
        "questions": unique,
    }

    OUTPUT.write_text(json.dumps(bank, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ {len(unique)} questions → {OUTPUT.name}")
    for s, n in subjects.items():
        print(f"   {s}: {n}")
    print("   Domains:")
    for d, n in sorted(domains.items(), key=lambda x: -x[1]):
        print(f"     {d}: {n}")


if __name__ == "__main__":
    main()
