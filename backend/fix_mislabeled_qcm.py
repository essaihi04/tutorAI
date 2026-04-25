"""
Détecte et corrige les questions QCM mal étiquetées comme "open" dans tous les
fichiers exam.json sous backend/data/exams/.

Un QCM mal étiqueté se reconnaît à :
  - type == "open"
  - content contient une table markdown avec des lignes commençant par
    |A|, |B|, |C|, |D| (ou a/b/c/d) — au moins 3 options.
  - typiquement une phrase d'intro : "Choisir ..." / "l'affirmation juste" /
    "la proposition juste" / "la réponse correcte" / "la bonne réponse" / etc.

Conversion :
  - type         → "qcm"
  - choices      → [{letter, text}, ...] extraits du tableau markdown
  - content      → énoncé d'intro sans le tableau
  - correct_answer est laissé inchangé (il est stocké dans correction.content
    sous forme libre "L'affirmation juste est : C ..."). Le backend
    exam_service.py extrait déjà cette lettre à l'exécution.

Usage:
    python fix_mislabeled_qcm.py            # dry-run : affiche les changements
    python fix_mislabeled_qcm.py --apply    # applique et réécrit les fichiers
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

EXAMS_DIR = Path(__file__).resolve().parent / "data" / "exams"

# Lignes du tableau markdown : |  A | texte | (ou minuscule)
_ROW_RE = re.compile(
    r"^\s*\|\s*([A-Fa-f])\s*\|\s*(.+?)\s*\|\s*$",
    re.MULTILINE,
)
# Séparateur markdown : | --- | --- |
_SEP_RE = re.compile(r"^\s*\|[\s\-:|]+\|\s*$", re.MULTILINE)

# Phrases typiques indiquant un QCM
_QCM_INTRO_RE = re.compile(
    r"(choisir|cochez|indiquez|sélectionnez|l['’]affirmation\s+juste|"
    r"la\s+proposition\s+(juste|correcte|exacte)|la\s+réponse\s+(juste|correcte|exacte)|"
    r"la\s+bonne\s+(réponse|proposition|affirmation)|"
    r"affirmation\s+(juste|correcte|exacte)|proposition\s+(juste|correcte|exacte))",
    re.IGNORECASE,
)


def extract_choices(content: str) -> tuple[list[dict], str] | None:
    """
    Si le contenu contient un tableau markdown de choix A/B/C/D (ou a/b/c/d),
    retourne (choices, content_sans_tableau). Sinon None.
    """
    rows = _ROW_RE.findall(content)
    if len(rows) < 3:  # il faut au moins 3 options pour un QCM
        return None

    # Vérifier l'unicité des lettres (éliminer les doublons dus à d'autres tableaux)
    letters_seen: list[str] = []
    unique: list[tuple[str, str]] = []
    for letter, text in rows:
        L = letter.upper()
        if L in letters_seen:
            continue
        letters_seen.append(L)
        unique.append((L, text.strip()))

    if len(unique) < 3:
        return None

    # Normaliser : toujours en majuscules A/B/C/D
    choices = [{"letter": L, "text": t} for L, t in unique]

    # Retirer les lignes du tableau + séparateur du contenu
    cleaned = _ROW_RE.sub("", content)
    cleaned = _SEP_RE.sub("", cleaned)
    # Compacter les sauts de lignes multiples
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned).strip()

    return choices, cleaned


def looks_like_qcm(q: dict) -> bool:
    """Heuristique : tableau de choix + indice linguistique dans l'intro."""
    content = q.get("content", "") or ""
    result = extract_choices(content)
    if result is None:
        return False
    # Intro must mention a QCM-style instruction
    return bool(_QCM_INTRO_RE.search(content))


# Extract "juste est : X" / "juste est X" / "la proposition X est" / etc.
_ANSWER_RE = re.compile(
    r"(?:juste|correcte|exacte|bonne)\s*(?:réponse|proposition|affirmation)?\s*"
    r"(?:est|:)\s*(?:est\s*)?[:\-]?\s*\**\s*\$?\s*([A-Fa-f])\b",
    re.IGNORECASE,
)


def extract_correct_answer(correction: dict | None, valid_letters: list[str]) -> str | None:
    if not correction:
        return None
    text = correction.get("content", "") or ""
    if not text:
        return None
    m = _ANSWER_RE.search(text)
    if not m:
        return None
    letter = m.group(1).upper()
    return letter if letter in valid_letters else None


def fix_question(q: dict) -> bool:
    """Transforme la question en QCM. Retourne True si modifiée."""
    if q.get("type") == "qcm":
        return False
    content = q.get("content", "") or ""
    result = extract_choices(content)
    if result is None:
        return False
    if not _QCM_INTRO_RE.search(content):
        return False
    choices, cleaned = result
    q["type"] = "qcm"
    q["content"] = cleaned
    q["choices"] = choices
    # Essayer d'extraire la bonne réponse depuis la correction
    valid_letters = [c["letter"] for c in choices]
    correct = extract_correct_answer(q.get("correction"), valid_letters)
    if correct:
        q["correct_answer"] = correct
    return True


def walk_questions(part: dict):
    """Itère sur toutes les questions et sous-questions d'une part."""
    for q in part.get("questions", []) or []:
        yield q
        for sq in q.get("sub_questions", []) or []:
            yield sq
    for ex in part.get("exercises", []) or []:
        for q in ex.get("questions", []) or []:
            yield q
            for sq in q.get("sub_questions", []) or []:
                yield sq


def process_exam(path: Path, apply: bool) -> int:
    """Retourne le nombre de questions corrigées."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"  ⚠️  Erreur lecture {path}: {e}")
        return 0

    fixed = 0
    for part in raw.get("parts", []) or []:
        for q in walk_questions(part):
            if q.get("type") != "open":
                continue
            if not looks_like_qcm(q):
                continue
            q_id = q.get("id", q.get("number", "?"))
            if fix_question(q):
                fixed += 1
                preview = (q.get("content", "") or "").replace("\n", " ")[:80]
                letters = ",".join(c["letter"] for c in q.get("choices", []))
                ans = q.get("correct_answer", "?")
                print(f"    → Q {q_id}: open → qcm ({letters}) answer={ans}  « {preview}… »")

    if fixed and apply:
        # Re-sérialiser en conservant l'indentation et l'ordre des clés
        path.write_text(
            json.dumps(raw, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
    return fixed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true",
                        help="Applique les corrections (sinon dry-run)")
    args = parser.parse_args()

    index_path = EXAMS_DIR / "index.json"
    if not index_path.exists():
        print(f"❌ {index_path} introuvable")
        sys.exit(1)

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== Fix QCM mal étiquetés — mode: {mode} ===\n")

    catalog = json.loads(index_path.read_text(encoding="utf-8"))
    total_fixed = 0
    files_affected = 0
    for meta in catalog:
        exam_path = EXAMS_DIR / meta["path"] / "exam.json"
        if not exam_path.exists():
            continue
        print(f"[{meta['subject']}] {meta['path']}")
        n = process_exam(exam_path, apply=args.apply)
        if n:
            files_affected += 1
            total_fixed += n

    print(
        f"\n=== Résumé : {total_fixed} question(s) corrigée(s) dans "
        f"{files_affected} fichier(s) ==="
    )
    if not args.apply and total_fixed:
        print("→ Relance avec --apply pour écrire les changements.")


if __name__ == "__main__":
    main()
