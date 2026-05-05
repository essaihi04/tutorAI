"""Batch split of Partie I/II preambles bundled in ex.context across
8 PC exercises. Each exercise's context is split at the "**Partie N**"
markers; the corresponding preamble is prepended to the owner question
(first question of that Partie, before a '---' separator).

Roman "Partie I/II/III" headers are renamed to Arabic "Partie 1/2/3"
so the frontend propagation regex matches.

For exercises whose questions restart at "1" for Partie II (duplicate
numbering is invalid in the UI), the second block is renumbered by
prepending the Partie index: Q1 → Q2.1, Q2 → Q2.2, etc.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

DRY = '--apply' not in sys.argv
EXAMS = Path('backend/data/exams')
PARTIE_RE = re.compile(r'\*\*Partie\s+[IVX\d][^*\n]*\*\*')

# ── Per-case spec ────────────────────────────────────────────────────
# Each case: {
#   "path": "<exam_dir>",
#   "ex_idx": <exercise index>,
#   "parties": [
#     {"owner_q": "<question number owning this Partie>",
#      "renumber_prefix": "<optional, rename every question in this block
#                          to prepend this prefix, e.g. '2.' for Partie II
#                          whose questions restart at 1>"},
#     ...
#   ],
# }
CASES = [
    # 2016-normale Ex1 Chimie — Partie II has 2 sub-sections with questions
    # 1.1-1.5 and 2.1-2.4. Treat the 2 sub-sections as separate Parties to
    # avoid bundling the whole acide-propanoïque preamble on every question.
    {
        'path': 'physique/2016-normale', 'ex_idx': 0,
        'parties': [
            {'owner_q': '1'},
            {'owner_q': '1.1'},
        ],
    },
    # 2016-normale Ex4 — two blocks, second block restarts at "1"
    {
        'path': 'physique/2016-normale', 'ex_idx': 3,
        'parties': [
            # First block: '1','2','3','4','5'
            {'owner_q': '1', 'block_start': 0, 'block_end': 5},
            # Second block: '1','2.1','2.2','2.3','3'  → renumber with '2.' prefix
            {'owner_q': '1', 'block_start': 5, 'block_end': 10, 'renumber_prefix': 'II.'},
        ],
    },
    # 2018-rattrapage Ex4 — questions 1-9 sequential. Need to find boundary.
    # From the PDF: Partie I = Lorentz (questions 1-? about force magnétique,
    # particle chargée), Partie II = pendule. We'll specify by index.
    # Read PDF pages to confirm — but visible from content patterns: Q1-Q4
    # are charged particle dynamics, Q5-Q9 are pendule. Partie II owner = Q5.
    {
        'path': 'physique/2018-rattrapage', 'ex_idx': 3,
        'parties': [
            {'owner_q': '1', 'block_start': 0, 'block_end': 4},
            {'owner_q': '5', 'block_start': 4, 'block_end': 9},
        ],
    },
    # 2023-normale Ex4 — two blocks: '1.1','1.2.1','1.2.2','2.1','2.2','2.3' then '1','2.1','2.2','3'
    {
        'path': 'physique/2023-normale', 'ex_idx': 3,
        'parties': [
            {'owner_q': '1.1', 'block_start': 0, 'block_end': 6},
            # Second block restarts: renumber with 'B.' prefix to disambiguate
            {'owner_q': '1', 'block_start': 6, 'block_end': 10, 'renumber_prefix': 'II.'},
        ],
    },
    # 2023-rattrapage Ex1 Chimie — clean numbering 1.1-1.4 then 2.1-2.8
    {
        'path': 'physique/2023-rattrapage', 'ex_idx': 0,
        'parties': [
            {'owner_q': '1.1'},
            {'owner_q': '2.1'},
        ],
    },
    # 2023-rattrapage Ex4 — '1','2','3','4' then '1','2','3','4' (duplicates!)
    {
        'path': 'physique/2023-rattrapage', 'ex_idx': 3,
        'parties': [
            {'owner_q': '1', 'block_start': 0, 'block_end': 4},
            {'owner_q': '1', 'block_start': 4, 'block_end': 8, 'renumber_prefix': 'II.'},
        ],
    },
    # 2025-rattrapage Ex3 — mixed: '1.1-1.4','2.1-2.3','3.1','3.2','II.1','II.2'
    # From the question numbers, Partie II starts at 'II.1'. So Partie I
    # includes 1.1-3.2 (9 questions).
    {
        'path': 'physique/2025-rattrapage', 'ex_idx': 2,
        'parties': [
            {'owner_q': '1.1', 'block_start': 0, 'block_end': 9},
            {'owner_q': 'II.1', 'block_start': 9, 'block_end': 11},
        ],
    },
    # 2025-rattrapage Ex4 — '1','2','3','1','2.1','2.2','2.3','3.1','3.2'
    {
        'path': 'physique/2025-rattrapage', 'ex_idx': 3,
        'parties': [
            {'owner_q': '1', 'block_start': 0, 'block_end': 3},
            {'owner_q': '1', 'block_start': 3, 'block_end': 9, 'renumber_prefix': 'II.'},
        ],
    },
]


def split_context(ctx: str) -> tuple[str, list[str]]:
    """Return (lead_in, [partie_chunks])."""
    matches = list(PARTIE_RE.finditer(ctx))
    if len(matches) < 2:
        return ctx, []
    lead = ctx[:matches[0].start()].strip()
    chunks = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(ctx)
        chunks.append(ctx[m.start():end].strip())
    return lead, chunks


def rename_partie_header(chunk: str, new_index: int) -> str:
    """Rename '**Partie I ...**' or '**Partie II ...**' → '**Partie 1 ...**' etc."""
    return re.sub(
        r'(\*\*Partie\s+)[IVX\d]+',
        lambda m: f'{m.group(1)}{new_index}',
        chunk,
        count=1,
    )


def fix(case):
    path_rel = case['path']
    ex_idx = case['ex_idx']
    parties = case['parties']
    path = EXAMS / path_rel / 'exam.json'
    d = json.loads(path.read_text(encoding='utf-8-sig'))
    ex = d['parts'][0]['exercises'][ex_idx]
    ctx = ex.get('context', '') or ''
    qs = ex['questions']

    lead, chunks = split_context(ctx)
    assert len(chunks) == len(parties), \
        f'{path_rel} Ex{ex_idx+1}: {len(chunks)} Partie chunks vs {len(parties)} specified'

    print(f'=== {path_rel}  Ex{ex_idx+1}')

    # Renumber blocks with renumber_prefix first (before locating owners)
    for p in parties:
        if 'renumber_prefix' in p and 'block_start' in p and 'block_end' in p:
            prefix = p['renumber_prefix']
            for i in range(p['block_start'], p['block_end']):
                old = str(qs[i].get('number'))
                qs[i]['number'] = f'{prefix}{old}'

    # After renumbering, locate the owner of each Partie.
    def find_owner(target_num: str, block_start: int = 0, block_end: int | None = None):
        end = block_end if block_end is not None else len(qs)
        for i in range(block_start, end):
            if str(qs[i].get('number')) == target_num:
                return qs[i]
        return None

    # Inject preambles
    for pi, (chunk, pspec) in enumerate(zip(chunks, parties), start=1):
        renamed_chunk = rename_partie_header(chunk, pi)
        block_start = pspec.get('block_start', 0)
        block_end = pspec.get('block_end')
        # After renumbering, the owner target number for renumbered blocks
        # is prefix + original
        target = pspec['owner_q']
        if 'renumber_prefix' in pspec:
            target = pspec['renumber_prefix'] + target
        owner = find_owner(target, block_start, block_end)
        assert owner is not None, \
            f'  Owner Q{target} not found in block [{block_start},{block_end})'
        content = owner.get('content', '') or ''
        if not content.lstrip().startswith('**Partie'):
            owner['content'] = renamed_chunk + '\n\n---\n\n' + content
        print(f'  Partie {pi} → owner Q{target} (renamed header): {renamed_chunk.split(chr(10),1)[0][:80]}')

    # Reset context to lead-in
    ex['context'] = lead if lead else f'Les {len(parties)} parties sont indépendantes.'

    if not DRY:
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding='utf-8')


for c in CASES:
    fix(c)

print('\n' + ('[APPLIED]' if not DRY else '[DRY RUN] Re-run with --apply'))
