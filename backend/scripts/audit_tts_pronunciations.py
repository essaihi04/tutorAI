"""Find pronunciation-risk tokens in the tutor's real content.

Examples:
    python scripts/audit_tts_pronunciations.py
    python scripts/audit_tts_pronunciations.py data/exams app/data --language fr
    python scripts/audit_tts_pronunciations.py --json --limit 200

The command is read-only. It prints the raw token, frequency, category and the
spoken form produced by the same normalizer used in production.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

BACKEND = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BACKEND))

from app.services.speech_normalizer import normalize_for_speech  # noqa: E402


PATTERNS = {
    "percentage": re.compile(r"(?<!\w)[-+−]?\d+(?:[,.]\d+)?\s*%"),
    "scientific": re.compile(r"(?<!\w)\d+(?:[,.]\d+)?\s*(?:×|x|\*)\s*10(?:\^?[-−⁻+⁺]?\d+|[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+)", re.I),
    "fraction": re.compile(r"(?<![\w/])\d+\s*/\s*\d+(?![\w/])"),
    "unit": re.compile(r"(?<!\w)[-+−]?\d+(?:[,.]\d+)?\s*(?:mol[·.]?L⁻¹|mol/L|km/h|m/s²?|mg/L|g/L|°C|kg|mg|km|cm|mm|mL|Hz|Pa|Ω)(?!\w)"),
    "abbreviation": re.compile(r"(?<!\w)(?:2BAC|BIOF|BAC|SVT|QCM|ADN|ARN|ATP|PC|pH|F[12]|H2O|CO2|O2|NaCl|HCl)(?!\w)"),
    "number": re.compile(r"(?<![\w])[-+−]?\d+(?:[,.]\d+)?(?![\w])"),
}

TEXT_SUFFIXES = {".json", ".jsonl", ".md", ".txt", ".csv", ".py"}


def iter_files(paths: list[Path]):
    for path in paths:
        if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
            yield path
        elif path.is_dir():
            yield from (
                candidate for candidate in path.rglob("*")
                if candidate.is_file() and candidate.suffix.lower() in TEXT_SUFFIXES
            )


def audit(paths: list[Path], language: str) -> list[dict[str, object]]:
    counts: Counter[tuple[str, str]] = Counter()
    for path in iter_files(paths):
        try:
            content = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        occupied: list[tuple[int, int]] = []
        # Specific patterns run before generic numbers to avoid duplicate rows.
        for category, pattern in PATTERNS.items():
            for match in pattern.finditer(content):
                span = match.span()
                if category == "number" and any(a <= span[0] < b for a, b in occupied):
                    continue
                counts[(category, match.group(0).strip())] += 1
                if category != "number":
                    occupied.append(span)
    rows = [
        {
            "category": category,
            "token": token,
            "count": count,
            "spoken": normalize_for_speech(token, language),
        }
        for (category, token), count in counts.most_common()
    ]
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    parser.add_argument("--language", choices=("fr", "mixed", "ar"), default="fr")
    parser.add_argument("--limit", type=int, default=100)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    paths = args.paths or [BACKEND / "data" / "exams", BACKEND / "app" / "data"]
    rows = audit([p if p.is_absolute() else BACKEND / p for p in paths], args.language)
    rows = rows[: max(args.limit, 0)]
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for row in rows:
            print(f"{row['count']:>6}  {row['category']:<13} {row['token']!r} -> {row['spoken']}")
        print(f"\n{len(rows)} formes affichées. Langue: {args.language}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

