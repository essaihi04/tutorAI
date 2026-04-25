"""Smoke tests for get_chapter_stats across all BAC subjects.

Verifies that chapter-stats queries return non-zero, plausible counts for
every major chapter in every subject. Run:

    python scripts/test_chapter_stats_all_subjects.py
"""
from __future__ import annotations

import sys
sys.path.insert(0, "backend")

from app.services.exam_bank_service import ExamBankService  # noqa: E402


# (subject, chapter query, expect_min_matched)
# expect_min_matched is a soft floor — we expect at least this many matches
# across 10 years of exams. If we get 0, the alias expansion is broken.
TESTS: list[tuple[str, str, int]] = [
    # ── SVT ──
    ("SVT", "combien de fois génétique est tombé", 50),
    ("SVT", "combien de fois immunologie est tombé", 20),
    ("SVT", "combien de fois géologie est tombé", 30),
    ("SVT", "combien de fois écologie est tombé", 15),
    ("SVT", "combien de fois respiration cellulaire est tombé", 20),
    ("SVT", "combien de fois système nerveux est tombé", 10),

    # ── Physique ──
    ("Physique", "combien de fois mécanique est tombé", 20),
    ("Physique", "combien de fois ondes est tombé", 20),
    ("Physique", "combien de fois nucléaire est tombé", 15),
    ("Physique", "combien de fois radioactivité est tombé", 10),
    ("Physique", "combien de fois RC est tombé", 5),
    ("Physique", "combien de fois RLC est tombé", 5),
    ("Physique", "combien de fois pendule est tombé", 5),
    ("Physique", "combien de fois satellite est tombé", 3),

    # ── Chimie ──
    ("Chimie", "combien de fois cinétique est tombé", 5),
    ("Chimie", "combien de fois acide base est tombé", 10),
    ("Chimie", "combien de fois dosage est tombé", 5),
    ("Chimie", "combien de fois pile est tombé", 5),
    ("Chimie", "combien de fois estérification est tombé", 3),

    # ── Maths ──
    ("Mathematiques", "combien de fois suites est tombé", 10),
    ("Mathematiques", "combien de fois complexes est tombé", 10),
    ("Mathematiques", "combien de fois intégrale est tombé", 10),
    ("Mathematiques", "combien de fois logarithme est tombé", 5),
    ("Mathematiques", "combien de fois exponentielle est tombé", 5),
    ("Mathematiques", "combien de fois probabilités est tombé", 5),
    ("Mathematiques", "combien de fois géométrie dans l'espace est tombé", 5),
    ("Mathematiques", "combien de fois équations différentielles est tombé", 3),
    ("Mathematiques", "combien de fois arithmétique est tombé", 3),
    ("Mathematiques", "combien de fois structures algébriques est tombé", 3),
]


def main() -> None:
    svc = ExamBankService()
    fails: list[str] = []
    print(f"{'Subject':<15} {'Query':<52} {'matched':>8} {'part I':>8} {'part II':>9}  status")
    print("-" * 100)
    for subject, query, floor in TESTS:
        r = svc.get_chapter_stats(query, subject)
        matched = r["matched"]
        p1 = r["by_part"].get("restitution", 0)
        p2 = r["by_part"].get("raisonnement", 0)
        ok = matched >= floor
        status = "OK " if ok else "LOW"
        if not ok:
            fails.append(f"{subject} / {query!r}: matched={matched} < floor={floor}")
        # Trim query for column width
        q_disp = query.replace("combien de fois ", "").replace(" est tombé", "")[:50]
        print(f"{subject:<15} {q_disp:<52} {matched:>8} {p1:>8} {p2:>9}  {status}")

    print()
    if fails:
        print(f"⚠️  {len(fails)} test(s) under the minimum threshold:")
        for f in fails:
            print(f"   - {f}")
        sys.exit(1)
    print("✅ All chapter-stats queries return plausible counts.")


if __name__ == "__main__":
    main()
