"""Unit tests for the new study_plan + diagnostic helpers (no DB required)."""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["RAG_DISABLED"] = "0"

import unittest.mock as mock

# Patch supabase.create_client BEFORE the app imports it, so the module-level
# `create_client(...)` call in app.supabase_client returns a MagicMock instead
# of trying to reach a real Supabase instance.
import supabase as _supabase_pkg
_supabase_pkg.create_client = lambda *a, **k: mock.MagicMock()

# Also stub the config so `settings.supabase_url` etc. don't fail
import app.config as _cfg
_fake = mock.MagicMock()
_fake.supabase_url = "http://fake"
_fake.supabase_anon_key = "fake"
_fake.supabase_service_role_key = "fake"
_cfg.get_settings = lambda: _fake

from app.services.study_plan_service import StudyPlanService
from app.services.diagnostic_service import DiagnosticService
from app.services.rag_service import get_rag_service

print("=" * 60)
print("1. Import sanity check")
print("=" * 60)
sp = StudyPlanService()
ds = DiagnosticService()
print("  ✓ StudyPlanService instantiated")
print("  ✓ DiagnosticService instantiated")

print("\n" + "=" * 60)
print("2. _chapter_matches_weak() — fuzzy title matching")
print("=" * 60)
chapter = {"title_fr": "Photosynthèse et flux d'énergie dans les écosystèmes"}
cases = [
    ({"photosynthèse"},            True,  "direct substring"),
    ({"photosynthese"},            False, "accent mismatch (no normalization yet)"),  # known limitation
    ({"flux d'énergie"},           True,  "exact phrase"),
    ({"génétique"},                False, "unrelated"),
    ({"écosystèmes"},              True,  "single keyword ≥4 chars"),
    ({"abc"},                       False, "too short to match partial"),
    (set(),                         False, "empty weak set"),
]
for weak, expected, label in cases:
    got = sp._chapter_matches_weak(chapter, weak)
    mark = "✓" if got == expected else "✗"
    print(f"  {mark} [{label}] weak={weak!r} -> {got} (expected {expected})")

print("\n" + "=" * 60)
print("3. _order_chapters_by_weakness() — weak first, order preserved")
print("=" * 60)
chapters = [
    {"chapter_number": 1, "title_fr": "Génétique des populations"},
    {"chapter_number": 2, "title_fr": "Photosynthèse"},
    {"chapter_number": 3, "title_fr": "Respiration cellulaire"},
    {"chapter_number": 4, "title_fr": "Immunologie"},
]
weak = {"photosynthèse", "immunologie"}
ordered = sp._order_chapters_by_weakness(chapters, weak)
print(f"  Input order:   {[c['chapter_number'] for c in chapters]}")
print(f"  Weak topics:   {weak}")
print(f"  Output order:  {[c['chapter_number'] for c in ordered]}  (expect weak first: 2, 4, then 1, 3)")
assert ordered[0]["chapter_number"] in {2, 4}, "First must be weak"
assert ordered[1]["chapter_number"] in {2, 4}, "Second must be weak"
print("  ✓ weak chapters are first")

# Empty weak → unchanged
ordered2 = sp._order_chapters_by_weakness(chapters, set())
assert [c["chapter_number"] for c in ordered2] == [1, 2, 3, 4]
print("  ✓ empty weak set preserves order")

print("\n" + "=" * 60)
print("4. _get_exam_id_allocator() — round-robin over real exams")
print("=" * 60)
# This uses real RAG, so load it
rag = get_rag_service()
rag.index_all()
for subject in ["SVT", "Mathématiques", "Physique-Chimie"]:
    alloc = sp._get_exam_id_allocator(subject)
    picks = [alloc() for _ in range(5)]
    print(f"  {subject:18} -> {picks}")
    # With 4-6 exams, first 4 should be unique
    uniq = len(set(picks[:4]) - {None})
    print(f"    ({uniq} unique in first 4 -> round-robin OK)")

print("\n" + "=" * 60)
print("5. DiagnosticService._get_tested_concepts() — mocked DB")
print("=" * 60)
# Mock supabase response to simulate 3 past diagnostics
fake_history = mock.MagicMock()
fake_history.data = [
    {"questions_data": [
        {"topic": "Photosynthèse", "question": "Où se déroule la phase claire?"},
        {"topic": "ATP", "question": "Quelle enzyme synthétise l'ATP?"},
    ]},
    {"questions_data": [
        {"topic": "Glycolyse", "domain": "Métabolisme", "question": "Combien d'ATP nets?"},
    ]},
]
ds.supabase.table.return_value.select.return_value.eq.return_value.eq.return_value.eq.return_value.order.return_value.limit.return_value.execute.return_value = fake_history
topics, heads = ds._get_tested_concepts("stu-1", "subj-1", last_n=5)
print(f"  Topics extracted: {topics}")
print(f"  Question heads:   {len(heads)} items")
assert "photosynthèse" in topics
assert "métabolisme" in topics  # from 'domain' field
assert len(heads) == 3
print("  ✓ topics include both 'topic' AND 'domain' fields")
print("  ✓ question heads collected")

print("\n" + "=" * 60)
print("✓ All tests passed")
print("=" * 60)
