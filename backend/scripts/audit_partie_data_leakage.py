"""Detect "Données générales" bullets in ex.context that are actually
specific to a single Partie.

Rationale: when an exercise has ≥ 2 Parties, ex.context is displayed on
every question (all Parties). If a bullet in ex.context references a
symbol/quantity used ONLY in one Partie, it leaks irrelevant data onto
the other Parties.

Heuristic (reports potential leakage, not always a bug):
  For each data bullet in ex.context, extract the LaTeX symbols (content
  inside $...$). For each symbol, check which Parties mention it in
  their questions/corrections. If a symbol appears in exactly one
  Partie (and the exercise has ≥ 2 Parties), flag the bullet.

Usage:
    python backend/scripts/audit_partie_data_leakage.py [-v]
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXAMS_DIR = ROOT / 'backend' / 'data' / 'exams'
VERBOSE = '-v' in sys.argv

PARTIE_START = re.compile(r'^\s*\*\*Partie\s+(\d)[^*]*\*\*', re.MULTILINE)
BULLET_LINE = re.compile(r'^\s*-\s+(.+)$', re.MULTILINE)
MATH_INLINE = re.compile(r'\$([^$]+)\$')
# Extract "symbol-like" fragments: greek/latex commands + subscripted identifiers
SYMBOL_FRAG = re.compile(r'\\mathrm\{([A-Za-z][A-Za-z0-9_()]*)\}|([A-Za-z]+)_\{[^}]+\}|\b(K_[A-Za-z0-9]+|pK_[A-Za-z0-9]+|C_[A-Za-z0-9]+|V_[A-Za-z0-9]+|M\([^)]*\))')

STOPWORDS = {
    'T', 'V', 'M', 'K', 'C', 'n', 'g', 'L', 'mol', 'cdot', 'circ', 'times',
    'mathrm', 'Delta', 'alpha', 'beta', 'theta', 'lambda', 'mu', 'pi',
    'eta', 'rho', 'phi', 'omega', 'infty', 'approx', 'neq', 'leq', 'geq',
}


def extract_symbols(text: str) -> set[str]:
    symbols = set()
    for m in MATH_INLINE.finditer(text):
        frag = m.group(1)
        # Get compound symbols
        for sm in SYMBOL_FRAG.finditer(frag):
            sym = next((g for g in sm.groups() if g), None)
            if sym and sym not in STOPWORDS and len(sym) >= 2:
                symbols.add(sym)
    return symbols


def partition_questions_by_partie(questions: list) -> dict[int, list]:
    """Walk questions; group by the active Partie number (from preamble)."""
    groups: dict[int, list] = {}
    active = 0
    for q in questions:
        content = q.get('content', '') or ''
        m = PARTIE_START.match(content.lstrip())
        if m:
            active = int(m.group(1))
        if active:
            groups.setdefault(active, []).append(q)
    return groups


def audit_file(path: Path, findings: list):
    rel = str(path.relative_to(ROOT))
    try:
        d = json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception:
        return
    for part in d.get('parts', []):
        for ei, ex in enumerate(part.get('exercises', [])):
            ctx = ex.get('context', '') or ''
            if '**Données' not in ctx:
                continue
            qs = ex.get('questions', []) or []
            partie_groups = partition_questions_by_partie(qs)
            if len(partie_groups) < 2:
                continue  # single-Partie exercise → no leakage possible

            # Build per-Partie text blob (all questions + corrections)
            partie_texts: dict[int, str] = {}
            for pn, qlist in partie_groups.items():
                buf = []
                for q in qlist:
                    buf.append(q.get('content', '') or '')
                    corr = q.get('correction')
                    if isinstance(corr, dict):
                        buf.append(corr.get('content', '') or '')
                partie_texts[pn] = '\n'.join(buf)

            # Check each bullet in ex.context
            bullets = BULLET_LINE.findall(ctx)
            for bullet in bullets:
                syms = extract_symbols(bullet)
                if not syms:
                    continue
                hit_parties = set()
                for pn, txt in partie_texts.items():
                    for sym in syms:
                        if sym in txt:
                            hit_parties.add(pn)
                            break
                if len(hit_parties) == 1:
                    pn = next(iter(hit_parties))
                    findings.append((
                        rel, f'ex{ei+1} ({ex.get("name","")[:50]})',
                        pn, bullet[:120], sorted(syms)
                    ))


def main():
    findings: list = []
    n = 0
    for f in sorted(EXAMS_DIR.rglob('exam.json')):
        audit_file(f, findings)
        n += 1
    print(f'Scanned {n} exam files\n')
    if not findings:
        print('✓ No Partie-data leakage detected.')
        return
    # Group by file+ex
    from collections import defaultdict
    grouped: dict[tuple, list] = defaultdict(list)
    for rel, exlabel, pn, bullet, syms in findings:
        grouped[(rel, exlabel)].append((pn, bullet, syms))
    print(f'Found leakage in {len(grouped)} exercise(s) across {len(findings)} bullet(s):\n')
    for (rel, exlabel), items in grouped.items():
        print(f'### {rel}  →  {exlabel}')
        for pn, bullet, syms in items:
            print(f'  [Partie {pn} only] {bullet}')
            if VERBOSE:
                print(f'      symbols: {syms}')
        print()


if __name__ == '__main__':
    main()
