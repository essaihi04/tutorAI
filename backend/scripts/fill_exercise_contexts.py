"""
Fill exercise.context in exam.json by extracting intro paragraphs from sujet_text (OCR).

For each "Exercice N" header in the sujet_text, capture everything between the header
and the first numbered question ("1. ", "1- ", "1) "). This paragraph is the "énoncé"
or introductory context of the exercise.

Usage:
    python backend/scripts/fill_exercise_contexts.py svt/2019-rattrapage
    python backend/scripts/fill_exercise_contexts.py svt   # all
"""
import argparse
import json
import logging
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
EXAMS_DIR = ROOT / "backend" / "data" / "exams"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("fill_contexts")

# Matches "Exercice 1", "Exercice 1 (5 pts)", "Exercice 1 (5 points)", etc.
EXERCISE_HEADER_RE = re.compile(
    r"Exercice\s+(\d+)\s*\(?(?:\d+[\d.,]*\s*p(?:t|oint)s?)?\)?",
    re.IGNORECASE,
)
# Matches first question marker at line start: "1. ", "1- ", "1) ", "1.a", etc.
FIRST_Q_RE = re.compile(r"(?:^|\n)\s*1[.\-)]\s+\S", re.MULTILINE)


def _clean(text: str) -> str:
    """Remove image refs, headers/footers, trailing figure noise, collapse whitespace."""
    # Strip image references ![alt](path)
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", text)
    # Strip arabic header lines
    text = re.sub(r"\n\s*(?:الصفحة|RS\d+F|RR\d+F|الامتحان|مادة).*", "", text)

    # Filter lines (drop anywhere — not only trailing — OCR-noise patterns)
    # Patterns for "figure caption" style text: short, standalone labels
    FIGURE_CAPTION_RE = re.compile(
        r"^(Réaction|Courbe|Schéma|Tableau|Graphique|Représentation)\b.{0,60}$"
    )
    # Legend entry: "X : Y" where X is a short symbol (≤8 chars)
    LEGEND_RE = re.compile(r"^[A-Za-zÀ-ÿ₀-₉⁰-⁹\d]{1,8}\s*:\s*\S.{0,30}$")
    # Document/figure standalone markers
    DOC_MARKER_RE = re.compile(r"^#?\s*(?:Document|Figure)\s*\d*\s*[a-z]?$", re.IGNORECASE)

    lines = []
    for line in text.split("\n"):
        stripped = line.strip()
        if not stripped:
            lines.append(line)
            continue
        # Skip pure-arabic lines
        if not re.search(r"[a-zA-Z]", line) and re.search(r"[\u0600-\u06FF]", line):
            continue
        # Skip page-number-only lines (1-2 digits)
        if re.fullmatch(r"\d{1,2}", stripped):
            continue
        # Skip code-sheet markers ("RS 34F", "NS 34F", "RR 34F", "NS34F")
        # Optionally prefixed by a page number ("3 RS 34F", "6 NS 34F")
        if re.fullmatch(r"(?:\d{1,2}\s+)?[NR][RS]\s*\d+[A-Z]?", stripped):
            continue
        # Skip combined "# N" markdown page markers
        if re.fullmatch(r"#+\s*\d{1,2}", stripped):
            continue
        # Skip standalone Document/Figure markers (anywhere)
        if DOC_MARKER_RE.match(stripped):
            continue
        # Skip standalone figure captions like "Réaction de formation d'ozone"
        if FIGURE_CAPTION_RE.match(stripped):
            continue
        # Skip legend entries like "O₃ : Ozone"
        if LEGEND_RE.match(stripped):
            continue
        lines.append(line)
    text = "\n".join(lines)

    # Strip leading ": (N pts)" or "(N pts)" artifact (DeepSeek sometimes includes the header tail)
    text = re.sub(r"^\s*[:\-]?\s*\(\d+[\d.,]*\s*p(?:t|oint)s?\)\s*\n+", "", text)

    # Strip trailing noise after context ends:
    # "Document N", "# Document N", "Figure a/b", standalone legend blocks
    # Heuristic: remove trailing lines that start with "Document" or "# Document" or "Figure"
    # and any following short legend lines (contain ":" and ≤5 words)
    cleaned_lines = text.split("\n")
    while cleaned_lines:
        last = cleaned_lines[-1].strip()
        if not last:
            cleaned_lines.pop()
            continue
        # Trailing "Document N" / "# Document N" / "Figure X"
        if re.fullmatch(r"#?\s*Document\s*\d*", last, re.IGNORECASE):
            cleaned_lines.pop()
            continue
        if re.fullmatch(r"Figure\s+[a-z0-9]+", last, re.IGNORECASE):
            cleaned_lines.pop()
            continue
        # Trailing standalone caption like "Réaction de formation d'ozone"
        # (short caption, starts with "Réaction" / "Courbe" / "Schéma" / "Tableau", <80 chars)
        if len(last) < 80 and re.match(r"^(Réaction|Courbe|Schéma|Tableau|Graphique|Représentation)\b", last):
            cleaned_lines.pop()
            continue
        # Trailing legend block: a short line like "O₃ : Ozone", "UV : Ultra-violet"
        if len(last) < 40 and re.match(r"^[A-Za-zÀ-ÿ₀-₉⁰-⁹\d]{1,8}\s*:\s*\S", last):
            cleaned_lines.pop()
            continue
        break

    text = "\n".join(cleaned_lines)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_exercise_contexts(sujet_text: str) -> dict[int, str]:
    """Return {exercise_number: context_text} for each Exercice found in sujet_text."""
    contexts: dict[int, str] = {}
    headers = list(EXERCISE_HEADER_RE.finditer(sujet_text))
    for i, m in enumerate(headers):
        ex_num = int(m.group(1))
        # Slice from end of header to next header (or EOF)
        start = m.end()
        end = headers[i + 1].start() if i + 1 < len(headers) else len(sujet_text)
        body = sujet_text[start:end]
        # Context is everything before the first "1." question marker
        first_q = FIRST_Q_RE.search(body)
        if first_q:
            context = body[: first_q.start()]
        else:
            context = body
        context = _clean(context)
        if context:
            contexts[ex_num] = context
    return contexts


def apply_contexts(exam_dir: Path, *, overwrite: bool = False) -> bool:
    extraction_file = exam_dir / "extraction.json"
    exam_file = exam_dir / "exam.json"
    if not extraction_file.exists() or not exam_file.exists():
        logger.warning(f"[SKIP] {exam_dir.name}: extraction.json ou exam.json manquant")
        return False

    extraction = json.loads(extraction_file.read_text(encoding="utf-8"))
    exam = json.loads(exam_file.read_text(encoding="utf-8"))
    contexts = extract_exercise_contexts(extraction.get("sujet_text", ""))

    if not contexts:
        logger.warning(f"[SKIP] {exam_dir.name}: aucun 'Exercice N' détecté dans le sujet")
        return False

    changed = 0
    for part in exam.get("parts", []):
        ex_idx = 0
        for ex in part.get("exercises", []) or []:
            ex_idx += 1
            # Parse "Exercice N" from name or infer by index
            m = re.search(r"(\d+)", ex.get("name", ""))
            key = int(m.group(1)) if m else ex_idx
            new_ctx = contexts.get(key) or contexts.get(ex_idx)
            if not new_ctx:
                continue
            if ex.get("context") and not overwrite:
                continue
            ex["context"] = new_ctx
            changed += 1
            logger.info(f"  {ex.get('name','?')} ← context ({len(new_ctx)} chars)")

    if changed:
        exam_file.write_text(json.dumps(exam, ensure_ascii=False, indent=2), encoding="utf-8")
        logger.info(f"[OK] {exam_dir.name}: {changed} exercice(s) enrichis")
        return True
    logger.info(f"[NOOP] {exam_dir.name}: tous les contextes sont déjà présents")
    return False


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="subject ou chemin d'examen (ex: 'svt' ou 'svt/2019-rattrapage')")
    parser.add_argument("--overwrite", action="store_true", help="Ecrase les contextes existants")
    args = parser.parse_args()

    target = EXAMS_DIR / args.target
    if not target.exists():
        logger.error(f"Cible introuvable: {target}")
        sys.exit(1)

    if (target / "exam.json").exists():
        dirs = [target]
    else:
        dirs = sorted(d for d in target.iterdir() if d.is_dir() and (d / "exam.json").exists())

    logger.info(f"Exams à traiter: {len(dirs)}")
    for d in dirs:
        apply_contexts(d, overwrite=args.overwrite)


if __name__ == "__main__":
    main()
