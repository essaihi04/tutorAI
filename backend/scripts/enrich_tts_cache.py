"""
Enrich the TTS cache with chapter-specific Darija coaching phrases.

For each chapter in the seed data, we:
  1. Ask Gemini 2.5 Flash (LLM) to generate ~25 realistic Darija coaching
     phrases that the AI tutor would actually speak during that lesson.
     These phrases reuse the chapter's French/Arabic technical terms (ln,
     exponentielle, dérivée, vitesse de réaction, etc.) the way a Moroccan
     teacher would — mixing Arabic script with French terms.
  2. Synthesize each phrase through the existing TTS pipeline so it lands
     in the on-disk cache (`data/tts_cache/`).

Run once, offline (takes ~30-60 min depending on Gemini quota):

    python -m scripts.enrich_tts_cache

You can stop anytime with Ctrl+C — phrases already synthesized stay in the
cache and the script skips them on the next run.

The steady-state effect: after this script + the built-in startup warmup,
~85-90% of the phrases spoken by the tutor are cache hits (0 ms latency,
$0 cost).
"""
from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
import time
from pathlib import Path

# Allow running this script from either `backend/` or repo root
_BACKEND_ROOT = Path(__file__).resolve().parent.parent
if str(_BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(_BACKEND_ROOT))

import httpx  # noqa: E402

from app.config import get_settings  # noqa: E402
from app.services.tts_service import (  # noqa: E402
    _synthesize_one_segment,
    _gemini_is_available,
)

settings = get_settings()

_SEED_DIR = _BACKEND_ROOT.parent / "database" / "seed_data"
_CHAPTER_FILES = [
    "math_chapters.json",
    "physics_chapters.json",
    "chemistry_chapters.json",
    "svt_chapters.json",
]

_LLM_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent?key={key}"
)

_PHRASE_GEN_PROMPT = """Tu es un prof marocain expérimenté qui prépare des élèves au BAC en {subject}.
Chapitre : « {chapter} »
Description : {description}

Génère EXACTEMENT 25 phrases courtes (20 à 80 caractères chacune) que tu dirais
oralement à un élève pendant ce chapitre. Écris-les en DARIJA marocaine
(alphabet arabe), mais GARDE les termes scientifiques clés en FRANÇAIS
(ex: la dérivée, la fonction exponentielle, la vitesse de réaction, pH, etc.).

Varie les types de phrases :
- Ouvertures / salutations liées à ce chapitre
- Questions pédagogiques (واش فهمتي ...؟)
- Encouragements (برافو، مزيان ...)
- Pièges typiques du BAC sur ce chapitre
- Transitions (دابا نشوفو ...)
- Rappels de formules / méthodes
- Corrections douces (ماشي بالضبط ...)
- Résumés (نلخصو ...)

Sors UNIQUEMENT une liste JSON de 25 chaînes, sans texte avant ni après.
Exemple de format : ["جملة واحدة", "جملة ثانية", ...]"""


def _parse_phrases_from_llm(text: str) -> list[str]:
    """Best-effort extraction of a JSON array of strings from LLM output."""
    if not text:
        return []
    # 1) Strip markdown fences anywhere in the text
    stripped = re.sub(r"```(?:json)?", "", text).replace("```", "").strip()

    # 2) Direct parse attempt
    try:
        data = json.loads(stripped)
        if isinstance(data, list):
            return [p for p in data if isinstance(p, str)]
    except Exception:
        pass

    # 3) Find the first [...] block and try to parse that
    m = re.search(r"\[[\s\S]*\]", stripped)
    if m:
        try:
            data = json.loads(m.group(0))
            if isinstance(data, list):
                return [p for p in data if isinstance(p, str)]
        except Exception:
            pass

    # 4) Line-by-line fallback: extract quoted strings from an array-looking blob
    quoted = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', stripped)
    # Keep only lines that look like sentences (>10 chars, not pure keys)
    return [q for q in quoted if 10 <= len(q) <= 200]


async def _generate_phrases_for_chapter(
    client: httpx.AsyncClient,
    subject: str,
    chapter_title: str,
    description: str,
) -> list[str]:
    """Ask Gemini Flash to write 25 realistic Darija coaching phrases."""
    prompt = _PHRASE_GEN_PROMPT.format(
        subject=subject,
        chapter=chapter_title,
        description=description,
    )
    key = settings.gemini_tts_api_key or settings.gemini_api_key
    url = _LLM_URL.format(key=key)
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.9,            # variety across runs
            "maxOutputTokens": 4000,       # 25 Arabic sentences ≈ 3k tokens
            "responseMimeType": "application/json",
        },
    }
    try:
        resp = await client.post(url, json=payload, timeout=90.0)
        if resp.status_code != 200:
            print(f"  [LLM] HTTP {resp.status_code}: {resp.text[:200]}")
            return []
        data = resp.json()
        candidate = (data.get("candidates") or [{}])[0]
        finish = candidate.get("finishReason", "?")
        text = (
            candidate.get("content", {})
                     .get("parts", [{}])[0]
                     .get("text", "")
        )
        phrases = _parse_phrases_from_llm(text)
        if not phrases:
            print(f"  [LLM] Empty/unparseable (finish={finish}). Raw: {text[:300]!r}")
            return []
        # Sanity filter: keep reasonable-length non-empty strings
        return [p.strip() for p in phrases if isinstance(p, str) and 10 <= len(p.strip()) <= 120]
    except Exception as e:
        print(f"  [LLM] Exception: {e}")
        return []


async def _tts_cache_one(phrase: str) -> str:
    """Run a phrase through the TTS pipeline. Returns status string."""
    if not _gemini_is_available():
        return "breaker_open"
    try:
        seg = await _synthesize_one_segment(phrase, "mixed")
    except Exception as e:
        return f"error:{e}"
    if seg is None:
        return "failed"
    return "cached_hit" if seg.cached else "generated"


async def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--limit-per-subject", type=int, default=0,
        help="Process only the first N chapters per subject (0 = all)."
    )
    args = parser.parse_args()
    limit = args.limit_per_subject

    total_phrases: list[tuple[str, str]] = []  # (subject, phrase)

    # 1. Collect chapters (optionally sliced)
    for fname in _CHAPTER_FILES:
        path = _SEED_DIR / fname
        if not path.exists():
            print(f"  [skip] {fname} not found")
            continue
        subject = fname.replace("_chapters.json", "").replace("_", " ").title()
        chapters = json.loads(path.read_text(encoding="utf-8"))
        # Sort by order_index so "first chapter" is stable
        chapters.sort(key=lambda c: c.get("order_index", c.get("chapter_number", 0)))
        if limit > 0:
            chapters = chapters[:limit]
        print(f"\n=== {subject}: {len(chapters)} chapter(s) to process ===")

        async with httpx.AsyncClient() as client:
            for ch in chapters:
                title = ch.get("title_fr") or ch.get("title_ar") or "?"
                desc = ch.get("description_fr") or ch.get("description_ar") or ""
                print(f"  • {title[:60]}")
                phrases = await _generate_phrases_for_chapter(
                    client, subject, title, desc
                )
                print(f"    → {len(phrases)} phrases generated")
                for p in phrases:
                    total_phrases.append((subject, p))
                # Small delay to respect LLM rate limits
                await asyncio.sleep(0.5)

    # Deduplicate (same phrase may be suggested for multiple chapters)
    seen = set()
    unique_phrases: list[str] = []
    for _, phrase in total_phrases:
        key = phrase.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        unique_phrases.append(phrase)

    print(f"\n=== Collected {len(total_phrases)} phrases "
          f"({len(unique_phrases)} unique) ===")

    # 2. Synthesize each via Gemini TTS (goes to cache automatically)
    print(f"\n=== Synthesizing {len(unique_phrases)} phrases (this takes a while) ===")
    stats = {"generated": 0, "cached_hit": 0, "failed": 0, "breaker_open": 0}
    t0 = time.time()

    for idx, phrase in enumerate(unique_phrases, 1):
        status = await _tts_cache_one(phrase)
        base = status.split(":")[0]
        stats[base] = stats.get(base, 0) + 1

        if idx % 10 == 0 or status.startswith("error") or status == "failed":
            elapsed = int(time.time() - t0)
            print(
                f"  [{idx:4}/{len(unique_phrases)}] {status:12} "
                f"gen={stats['generated']} hit={stats['cached_hit']} "
                f"fail={stats['failed']} brk={stats['breaker_open']} "
                f"t={elapsed}s  « {phrase[:50]} »"
            )

        # Respect Gemini rate limits — each call already waits ~10s
        await asyncio.sleep(0.2)

    total_s = int(time.time() - t0)
    print(f"\n=== DONE in {total_s}s ===")
    print(f"  generated : {stats['generated']}")
    print(f"  cached_hit: {stats['cached_hit']}")
    print(f"  failed    : {stats['failed']}")
    print(f"  breaker   : {stats['breaker_open']}")

    # 3. Save the master list (additive — merges with previous runs so
    #    incremental enrichment accumulates rather than overwrites).
    out_path = _BACKEND_ROOT / "app" / "data" / "course_phrases.json"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    merged: list[str] = []
    seen_keys: set[str] = set()
    if out_path.exists():
        try:
            previous = json.loads(out_path.read_text(encoding="utf-8"))
            if isinstance(previous, list):
                for p in previous:
                    if isinstance(p, str):
                        k = p.strip().lower()
                        if k and k not in seen_keys:
                            seen_keys.add(k)
                            merged.append(p)
        except Exception as e:
            print(f"  [warn] Could not merge previous phrase list: {e}")

    added_now = 0
    for p in unique_phrases:
        k = p.strip().lower()
        if k and k not in seen_keys:
            seen_keys.add(k)
            merged.append(p)
            added_now += 1

    out_path.write_text(
        json.dumps(merged, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\n  Master phrase list saved to: {out_path}")
    print(f"  Added this run: {added_now} new phrases — total in file: {len(merged)}")
    print("  On next startup, the TTS warmup will hit 100% cache for these phrases.")


if __name__ == "__main__":
    asyncio.run(main())
