"""End-to-end: verify the atlas is reachable from all 3 injection points."""
import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ["RAG_DISABLED"] = "1"

import unittest.mock as mock
import supabase as _sb
_sb.create_client = lambda *a, **k: mock.MagicMock()
import app.config as _cfg
_fake = mock.MagicMock()
_fake.supabase_url = "http://fake"
_fake.supabase_anon_key = _fake.supabase_service_role_key = "fake"
_cfg.get_settings = lambda: _fake

from app.services.topic_atlas_service import topic_atlas

print("═" * 70)
print("1. Atlas loads successfully")
print("═" * 70)
atlas = topic_atlas._ensure_loaded()
assert "SVT" in atlas and "Physique-Chimie" in atlas and "Mathematiques" in atlas
print(f"  ✓ 3 subjects loaded: {list(atlas.keys())}")

print("\n" + "═" * 70)
print("2. predict_2026_priorities() works for all subjects")
print("═" * 70)
for subject in ["SVT", "Physique-Chimie", "Mathematiques"]:
    p = topic_atlas.predict_2026_priorities(subject)
    high = len(p["HIGH"])
    medium = len(p["MEDIUM"])
    low = len(p["LOW"])
    print(f"  {subject:20s} HIGH={high}  MEDIUM={medium}  LOW={low}")
    assert high + medium + low > 0, f"No predictions for {subject}"

print("\n" + "═" * 70)
print("3. build_historical_context_for_prompt() produces text")
print("═" * 70)
for subject in ["SVT", "Physique-Chimie", "Mathematiques"]:
    block = topic_atlas.build_historical_context_for_prompt(subject, max_years=3)
    assert "HISTORIQUE BAC" in block
    assert "PRÉDICTIONS BAC 2026" in block
    assert "RÈGLE D'ÉQUILIBRE" in block
    print(f"  ✓ {subject:20s} ({len(block)} chars, {block.count(chr(10))} lines)")

print("\n" + "═" * 70)
print("4. get_topics_not_tested_recently() for PC/Math gap analysis")
print("═" * 70)
for subject in ["Physique-Chimie", "Mathematiques"]:
    gaps = topic_atlas.get_topics_not_tested_recently(subject, min_gap_years=2)
    print(f"  {subject}: {len(gaps)} topic(s) absent depuis ≥ 2 ans")
    for g in gaps[:4]:
        level = g.get('prediction', {}).get('level', '?')
        print(f"    • {g['domain']:40s} last={g.get('last')}  gap={g['gap']}  pred={level}")

print("\n" + "═" * 70)
print("5. get_svt_format_predictions() for SVT format rotation")
print("═" * 70)
fmts = topic_atlas.get_svt_format_predictions()
for domain, pred in fmts.items():
    fmt = pred.get('format_probable', '—')
    lvl = pred.get('level', '?')
    print(f"  {domain:50s} {lvl:6s} {fmt}")

print("\n" + "═" * 70)
print("6. Modules importing topic_atlas compile cleanly")
print("═" * 70)
try:
    from app.services.diagnostic_service import DiagnosticService
    print("  ✓ diagnostic_service imports atlas")
except Exception as e:
    print(f"  ✗ diagnostic_service: {e}")
    sys.exit(1)
try:
    from app.services.study_plan_service import StudyPlanService
    print("  ✓ study_plan_service imports atlas")
except Exception as e:
    print(f"  ✗ study_plan_service: {e}")
    sys.exit(1)
try:
    from app.services.llm_service import LLMService
    print("  ✓ llm_service imports atlas")
except Exception as e:
    print(f"  ✗ llm_service: {e}")
    sys.exit(1)

print("\n" + "═" * 70)
print("✓ All integration checks passed")
print("═" * 70)
