"""
Audit de la banque d'examens BAC : valide que chaque question dispose d'une
correction officielle non-vide et conforme au niveau 2BAC PC BIOF.

Sortie : scripts/audit_exam_bank_report.md

Aucune latence runtime — script offline pur.

Usage :
    python scripts/audit_exam_bank.py [--strict]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

# Same path as ExamBankService.EXAMS_DIR — backend/data/exams/
EXAMS_DIR = Path(__file__).resolve().parent.parent / "data" / "exams"
REPORT_PATH = Path(__file__).resolve().parent / "audit_exam_bank_report.md"

# ──────────────────────────────────────────────────────────────────────
#  Détection de jargon HORS-NIVEAU 2BAC PC BIOF
#  Mots-clés qui ne doivent PAS apparaître dans une correction officielle
#  destinée à un lycéen marocain.
# ──────────────────────────────────────────────────────────────────────
OFF_LEVEL_KEYWORDS_BY_SUBJECT: dict[str, list[str]] = {
    "Mathematiques": [
        # Algèbre linéaire (hors programme)
        r"\bespace[s]?\s+vectoriel", r"\bbase\s+canonique", r"\bendomorphisme",
        # 'déterminant' as NOUN only (matrix determinant), not the gerund
        # « en déterminant les probabilités… » which is at-program.
        r"\bd[ée]terminant\s+(d['e ]une\s+matrice|de\s+la\s+matrice|\d+\s*[×x]\s*\d+|nul\b|non\s+nul)",
        r"\bmatrice[s]?\b(?![- ]?[0-9])",
        r"\bdiagonalis", r"\bvaleur[s]?\s+propre", r"\bpolyn[ôo]me\s+caract[ée]ristique",
        r"\bnoyau\s+et\s+image", r"\brang\s+d['e ]une\s+matrice", r"\bapplication\s+lin[ée]aire",
        # Topologie/analyse sup
        r"\bespace\s+m[ée]trique", r"\bcompl[ée]tude", r"\bconvergence\s+uniforme",
        r"\bcrit[èe]re\s+de\s+(Cauchy|d['Aa]lembert|Leibniz)",
        r"\bs[ée]rie\s+enti[èe]re", r"\bint[ée]grale\s+impropre",
        # Notations sup
        r"\bjacobien", r"\bgradient[- ]+d\b", r"\bdivergence\b", r"\brotationnel",
        r"\b∇·", r"\b∇×", r"\bdiff[ée]omorphisme",
    ],
    "Physique": [
        r"\bformalisme\s+lagrangien", r"\b[ée]quation[s]?\s+d['e ]Euler-Lagrange",
        r"\bhamiltonien", r"\btransform[ée]e\s+de\s+Fourier",
        r"\bchamp\s+tensoriel", r"\b[ée]quation\s+de\s+la\s+chaleur",
        r"\b[ée]quations?\s+de\s+Maxwell", r"\bth[ée]or[èe]me\s+d['e ]Amp[èe]re",
        r"\b[ée]quation\s+de\s+Schr[ôö]dinger", r"\bdilatation\s+du\s+temps",
        r"\b[ée]quation\s+de\s+Bernoulli", r"\brelativit[ée]\s+restreinte",
        r"\bm[ée]canique\s+quantique", r"\boptique\s+g[ée]om[ée]trique",
    ],
    "Chimie": [
        r"\b[ée]quation\s+de\s+Nernst", r"\bHenderson[- ]?Hasselbalch",
        r"\bloi\s+de\s+Hess", r"\benthalpie\s+standard",
        r"\bm[ée]canisme\s+SN[12]", r"\bm[ée]canisme\s+E[12]",
        r"\bspectre\s+RMN", r"\bIR\s+infrarouge", r"\bnomenclature\s+IUPAC",
        r"\bmaille\s+cubique", r"\bcristallographie",
        r"\borbital[e]?[s]?\s+hybrid", r"\bth[ée]orie\s+VSEPR",
        r"\bΔG\b", r"\bΔS\b", r"\bdiagramme\s+E-pH",
    ],
    "SVT": [
        # Hors programme PC (mais peut être au programme SVT track)
        # On les flag uniquement si présents dans un exam dont le subject est PC
    ],
}

# Matières mappées vers la clé du dict ci-dessus (normalisation)
SUBJECT_NORM = {
    "math": "Mathematiques", "mathematiques": "Mathematiques",
    "mathématiques": "Mathematiques", "maths": "Mathematiques",
    "physique": "Physique", "physique-chimie": "Physique-Chimie",
    "physique chimie": "Physique-Chimie", "pc": "Physique-Chimie",
    "chimie": "Chimie",
    "svt": "SVT", "sciences de la vie et de la terre": "SVT",
}


def _norm_subject(s: str) -> str:
    return SUBJECT_NORM.get((s or "").strip().lower(), s or "")


# Single-letter QCM answers (case-insensitive) — used to detect QCMs whose
# `type` field is wrongly set to "open" (frequent in physique_2020_normale).
_QCM_LETTER_RE = re.compile(r"^\s*[A-E]\.?\s*$", re.IGNORECASE)
_VRAI_FAUX_RE = re.compile(r"^\s*(vrai|faux|true|false)\s*$", re.IGNORECASE)


def _looks_like_qcm_answer(text: str) -> bool:
    """A correction reduced to a single letter A-E (or vrai/faux) is in fact
    a QCM/vrai-faux answer — even if the JSON declared type='open'."""
    if not text:
        return False
    t = text.strip()
    return bool(_QCM_LETTER_RE.match(t) or _VRAI_FAUX_RE.match(t))


@dataclass
class QuestionAudit:
    exam_id: str
    subject: str
    year: int
    session: str
    part_name: str
    exercise_name: str
    question_id: str
    question_number: str
    points: float
    question_type: str
    has_content: bool
    has_correction: bool
    correction_length: int
    is_qcm_like: bool = False  # type='open' but correction is single letter A-E
    is_wrapper: bool = False  # parent question whose answer lives in sub_questions
    off_level_hits: list[str] = field(default_factory=list)


@dataclass
class ExamAudit:
    file_path: Path
    exam_id: str
    subject: str
    year: int
    session: str
    questions: list[QuestionAudit] = field(default_factory=list)
    parse_error: str | None = None


def _walk_questions(node, exam_meta, part_name: str, exercise_name: str,
                    audits: list[QuestionAudit], off_level_patterns: list[re.Pattern]):
    """Recursively collect questions from a part / exercise / sub_questions tree."""
    if isinstance(node, dict):
        # If this node looks like a question (has content + id/number/correction key)
        has_q_shape = (
            "content" in node
            and ("id" in node or "number" in node or "correction" in node)
            and "questions" not in node
            and "exercises" not in node
        )
        if has_q_shape:
            content = node.get("content") or ""
            corr = node.get("correction")
            if isinstance(corr, dict):
                # QCM sub-questions store the answer in `correct_answer`
                # (e.g. {"correct_answer": "c"}) instead of `content`.
                # Both forms are valid corrections.
                corr_text = (corr.get("content") or corr.get("correct_answer") or "")
                if isinstance(corr_text, (list, dict)):
                    corr_text = json.dumps(corr_text, ensure_ascii=False)
                corr_text = str(corr_text)
            elif isinstance(corr, str):
                corr_text = corr
            else:
                corr_text = ""

            # Also accept top-level `correct_answer` field (used by some
            # vrai_faux and association questions).
            if not corr_text.strip() and node.get("correct_answer") is not None:
                corr_text = str(node.get("correct_answer"))

            # For association questions, `correct_pairs` is the correction.
            if not corr_text.strip() and node.get("correct_pairs"):
                corr_text = json.dumps(node.get("correct_pairs"), ensure_ascii=False)

            off_hits = []
            for pat in off_level_patterns:
                m = pat.search(corr_text)
                if m:
                    off_hits.append(m.group(0))

            # A "wrapper" question is a parent whose REAL answers are in
            # sub_questions (e.g. "QII. Pour chacune des propositions..." +
            # 4 sub-QCMs). Such wrappers don't need their own correction.
            sub_qs = node.get("sub_questions") or []
            has_answered_subs = (
                isinstance(sub_qs, list)
                and len(sub_qs) > 0
                and any(
                    isinstance(sq, dict) and (
                        (sq.get("correction") or {}).get("content")
                        or (sq.get("correction") or {}).get("correct_answer")
                        or sq.get("correct_answer") is not None
                        or sq.get("correct_pairs")
                    )
                    for sq in sub_qs
                )
            )

            audits.append(QuestionAudit(
                exam_id=exam_meta["exam_id"],
                subject=exam_meta["subject"],
                year=exam_meta["year"],
                session=exam_meta["session"],
                part_name=part_name,
                exercise_name=exercise_name,
                question_id=str(node.get("id", "")),
                question_number=str(node.get("number", "")),
                points=float(node.get("points") or 0),
                question_type=str(node.get("type", "open") or "open").lower(),
                has_content=bool(content.strip()),
                has_correction=bool(corr_text.strip()),
                correction_length=len(corr_text.strip()),
                is_qcm_like=_looks_like_qcm_answer(corr_text),
                is_wrapper=has_answered_subs,
                off_level_hits=off_hits,
            ))

        # Recurse ONLY into known container keys. NEVER descend into
        # `correction` (otherwise its inner {content:...} dict is mistaken
        # for another question, generating ~90 false positives).
        for child_key in ("parts", "exercises", "questions", "sub_questions"):
            children = node.get(child_key)
            if isinstance(children, list):
                # If this child container has a name (exercise), use it
                next_part = part_name
                next_ex = exercise_name
                if child_key == "exercises":
                    next_part = node.get("name", part_name) or part_name
                if child_key == "questions" and "name" in node:
                    next_ex = node.get("name", exercise_name) or exercise_name
                for child in children:
                    if isinstance(child, dict) and child_key == "exercises":
                        next_ex_for_child = child.get("name") or exercise_name
                        _walk_questions(child, exam_meta, next_part, next_ex_for_child,
                                        audits, off_level_patterns)
                    else:
                        _walk_questions(child, exam_meta, next_part, next_ex,
                                        audits, off_level_patterns)
    elif isinstance(node, list):
        for child in node:
            _walk_questions(child, exam_meta, part_name, exercise_name,
                            audits, off_level_patterns)


def audit_exam(exam_path: Path, meta: dict) -> ExamAudit:
    exam_id = meta.get("id", exam_path.parent.name)
    subject_raw = meta.get("subject") or ""
    subject = _norm_subject(subject_raw)
    audit = ExamAudit(
        file_path=exam_path,
        exam_id=exam_id,
        subject=subject_raw,
        year=int(meta.get("year") or 0),
        session=meta.get("session") or "",
    )
    try:
        with open(exam_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        audit.parse_error = f"JSON parse error: {e}"
        return audit

    patterns = [re.compile(p, re.IGNORECASE) for p in
                OFF_LEVEL_KEYWORDS_BY_SUBJECT.get(subject, [])]
    exam_meta = {
        "exam_id": exam_id, "subject": subject_raw,
        "year": audit.year, "session": audit.session,
    }
    _walk_questions(data, exam_meta, "", "", audit.questions, patterns)
    return audit


def main(strict: bool = False) -> int:
    index_path = EXAMS_DIR / "index.json"
    if not index_path.exists():
        print(f"[ERROR] {index_path} not found", file=sys.stderr)
        return 2

    with open(index_path, "r", encoding="utf-8") as f:
        catalog = json.load(f)

    print(f"[AUDIT] Scanning {len(catalog)} exam(s) listed in index.json …")
    audits: list[ExamAudit] = []
    for meta in catalog:
        exam_path = EXAMS_DIR / meta["path"] / "exam.json"
        if not exam_path.exists():
            print(f"[WARN] Missing file: {exam_path}")
            continue
        audits.append(audit_exam(exam_path, meta))

    # ── Coverage by subject ─────────────────────────────────────────
    # In the Moroccan BAC, "Physique-Chimie" is a UNIFIED subject covering
    # both Physique AND Chimie sub-domains. So a "Physique-Chimie" exam
    # counts for BOTH Physique and Chimie coverage. Don't flag Chimie as
    # missing just because no exam is labeled "Chimie" alone.
    raw_subjects = [_norm_subject(m.get("subject", "")) for m in catalog]
    subjects_in_catalog: Counter = Counter()
    for s in raw_subjects:
        if s == "Physique-Chimie":
            subjects_in_catalog["Physique"] += 1
            subjects_in_catalog["Chimie"] += 1
        else:
            subjects_in_catalog[s] += 1
    expected_subjects = ["Mathematiques", "Physique", "Chimie", "SVT"]
    missing_subjects = [s for s in expected_subjects if subjects_in_catalog.get(s, 0) == 0]

    # ── Aggregate stats ─────────────────────────────────────────────
    all_questions = [q for a in audits for q in a.questions]
    total_q = len(all_questions)
    # Wrapper questions also legitimately have empty content (the real
    # statement lives in sub_questions).
    no_content = [q for q in all_questions if not q.has_content and not q.is_wrapper]
    # Wrapper questions (parent of sub_questions whose answers are filled)
    # don't need their own correction — exclude from "no_correction" warning.
    no_correction = [q for q in all_questions
                     if q.has_correction is False and not q.is_wrapper]
    # QCM / vrai_faux / association legitimately have very short corrections
    # ("Réponse correcte : b"). Exclude them from the short-correction warning.
    # Some files declare type='open' but the correction content is just a
    # single letter A-E or vrai/faux — also exclude those.
    SHORT_OK_TYPES = {"qcm", "vrai_faux", "association"}
    short_correction = [
        q for q in all_questions
        if q.has_correction
        and q.correction_length < 30
        and q.question_type not in SHORT_OK_TYPES
        and not q.is_qcm_like
    ]
    off_level = [q for q in all_questions if q.off_level_hits]

    # ── Build report ────────────────────────────────────────────────
    lines = []
    lines.append("# Audit de la banque d'examens BAC")
    lines.append("")
    lines.append(f"- **Examens listés dans `index.json`** : {len(catalog)}")
    lines.append(f"- **Examens chargés avec succès** : {len([a for a in audits if not a.parse_error])}")
    lines.append(f"- **Total questions analysées** : {total_q}")
    lines.append("")

    lines.append("## Couverture par matière")
    lines.append("")
    lines.append("| Matière | Examens | Statut |")
    lines.append("|---|---|---|")
    for subj in expected_subjects:
        cnt = subjects_in_catalog.get(subj, 0)
        emoji = "✅" if cnt >= 4 else ("⚠️" if cnt > 0 else "❌")
        lines.append(f"| {subj} | {cnt} | {emoji} {'manquant' if cnt == 0 else ('insuffisant (<4)' if cnt < 4 else 'OK')} |")
    lines.append("")
    if missing_subjects:
        lines.append(f"🚨 **Matières SANS aucun examen indexé** : {', '.join(missing_subjects)}.")
        lines.append("Le LLM doit improviser pour ces matières — ajoute des examens BAC nationaux pour ancrer ses réponses.")
        lines.append("")

    lines.append("## Qualité des corrections officielles")
    lines.append("")
    lines.append(f"- ❌ **Questions sans énoncé** : {len(no_content)} / {total_q}")
    lines.append(f"- ❌ **Questions sans correction officielle** : {len(no_correction)} / {total_q}")
    lines.append(f"- ⚠️  **Corrections suspectes (< 30 caractères)** : {len(short_correction)} / {total_q}")
    lines.append(f"- 🚨 **Corrections avec jargon hors-niveau 2BAC** : {len(off_level)} / {total_q}")
    lines.append("")

    if no_correction:
        lines.append("### Questions sans correction officielle")
        lines.append("")
        for q in no_correction[:30]:
            lines.append(f"- `{q.exam_id}` — {q.part_name or '(part?)'} — {q.exercise_name or '(ex?)'} — Q{q.question_number or q.question_id}")
        if len(no_correction) > 30:
            lines.append(f"- … et {len(no_correction) - 30} autres")
        lines.append("")

    if short_correction:
        lines.append("### Corrections suspectes (trop courtes)")
        lines.append("")
        for q in short_correction[:20]:
            lines.append(f"- `{q.exam_id}` — Q{q.question_number or q.question_id} — {q.correction_length} chars")
        lines.append("")

    if off_level:
        lines.append("### Corrections avec jargon hors-niveau 2BAC")
        lines.append("")
        lines.append("> Ces termes ne devraient pas apparaître dans une correction officielle 2BAC. Vérifie qu'ils ne sont pas issus d'un copier-coller universitaire.")
        lines.append("")
        by_subject: dict[str, list[QuestionAudit]] = defaultdict(list)
        for q in off_level:
            by_subject[q.subject].append(q)
        for subj, qs in sorted(by_subject.items()):
            lines.append(f"#### {subj} ({len(qs)})")
            for q in qs[:15]:
                hits = ", ".join(set(q.off_level_hits))
                lines.append(f"- `{q.exam_id}` — Q{q.question_number or q.question_id} — termes : *{hits}*")
            if len(qs) > 15:
                lines.append(f"- … et {len(qs) - 15} autres")
            lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"[AUDIT] Rapport : {REPORT_PATH}")

    # ── Exit codes ──────────────────────────────────────────────────
    error_count = len(no_content) + len(no_correction)
    warning_count = len(short_correction) + len(off_level) + len(missing_subjects)
    print(f"[AUDIT] Erreurs : {error_count}  |  Avertissements : {warning_count}")
    if strict and (error_count > 0 or warning_count > 0):
        return 1
    if error_count > 0:
        return 1
    return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true",
                        help="Exit code 1 si avertissements aussi (utile en CI).")
    args = parser.parse_args()
    sys.exit(main(strict=args.strict))
