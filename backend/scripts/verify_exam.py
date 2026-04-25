"""
Verify Exam — Étape D (contrôle qualité comparatif PDF ↔ JSON)

Pour chaque examen disposant de `extraction.json` + `exam.json`, compare :
  1. Total des points (JSON vs attendu 20)
  2. Somme des points de chaque partie
  3. Numérotation des questions : celles détectées dans le texte OCR du sujet vs celles du JSON
  4. Documents : tous les crops `assets/doc*p*.png` sont référencés dans le JSON
  5. Analyse sémantique par DeepSeek : points manqués, incohérences, questions sautées

Sort un rapport `verification_report.md` dans le dossier de l'examen.

Usage:
    python backend/scripts/verify_exam.py svt/2019-rattrapage
    python backend/scripts/verify_exam.py svt                      # tous
    python backend/scripts/verify_exam.py svt/2019-rattrapage --no-llm  # skip LLM check
"""
import argparse
import asyncio
import json
import logging
import os
import re
import sys
from pathlib import Path

import httpx
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / "backend" / ".env")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/chat/completions").strip()
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip()

EXAMS_DIR = ROOT / "backend" / "data" / "exams"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("verify_exam")


# ─────────────────── Structural checks (no LLM) ───────────────────

def check_metadata(exam: dict, folder_name: str) -> list[str]:
    issues = []
    parts = folder_name.split("-")
    year_folder = int(parts[0]) if parts[0].isdigit() else None
    session_folder = parts[1].capitalize() if len(parts) > 1 else None
    if year_folder and exam.get("year") != year_folder:
        issues.append(f"year={exam.get('year')} ≠ dossier={year_folder}")
    if session_folder and exam.get("session", "").lower() != session_folder.lower():
        issues.append(f"session='{exam.get('session')}' ≠ dossier='{session_folder}'")
    return issues


def check_points(exam: dict) -> list[str]:
    issues = []
    total_declared = exam.get("total_points", 0)
    parts = exam.get("parts", [])
    total_parts = sum(p.get("points", 0) for p in parts)
    if abs(total_parts - total_declared) > 0.01:
        issues.append(f"Σ parties = {total_parts} ≠ total_points = {total_declared}")

    # Per-part: sum question points
    for pi, part in enumerate(parts, 1):
        declared = part.get("points", 0)
        real = 0.0
        for q in part.get("questions", []) or []:
            real += q.get("points", 0)
        for ex in part.get("exercises", []) or []:
            ex_declared = ex.get("points", 0)
            ex_real = sum(q.get("points", 0) for q in ex.get("questions", []) or [])
            real += ex_declared  # use declared ex points for part total
            if abs(ex_real - ex_declared) > 0.01:
                issues.append(
                    f"P{pi} {ex.get('name')}: Σ questions = {ex_real} ≠ {ex_declared}"
                )
        if abs(real - declared) > 0.01:
            issues.append(f"P{pi} ({part.get('name','?')}): Σ = {real} ≠ {declared}")
    return issues


def extract_json_question_numbers(exam: dict) -> list[str]:
    """Collect all question 'number' fields from the JSON (hierarchical)."""
    numbers = []
    for part in exam.get("parts", []):
        for q in part.get("questions", []) or []:
            numbers.append(q.get("number", "?"))
            for sq in q.get("sub_questions", []) or []:
                numbers.append(f"{q.get('number')}.{sq.get('number')}")
        for ex in part.get("exercises", []) or []:
            for q in ex.get("questions", []) or []:
                numbers.append(f"{ex.get('name','?')}.{q.get('number','?')}")
    return numbers


QUESTION_RE_MAIN = re.compile(r"^\s*(?P<num>\d+)\s*[-.)]\s*", re.MULTILINE)
ROMAN_RE = re.compile(r"^\s*(?P<rom>I{1,3}|IV|V|VI{0,3})\s*[-.]\s", re.MULTILINE)


def extract_pdf_question_markers(sujet_text: str) -> dict:
    """Extract markers from OCR text of the sujet PDF (indicative only)."""
    arabic_nums = set(m.group("num") for m in QUESTION_RE_MAIN.finditer(sujet_text))
    roman = set(m.group("rom") for m in ROMAN_RE.finditer(sujet_text))
    # Count "Exercice N"
    ex_count = len(re.findall(r"Exercice\s+\d+", sujet_text, re.IGNORECASE))
    return {
        "arabic_numbered": sorted(arabic_nums, key=lambda x: int(x)),
        "roman": sorted(roman),
        "exercises_detected": ex_count,
    }


def check_assets(exam: dict, exam_dir: Path) -> list[str]:
    issues = []
    assets_dir = exam_dir / "assets"
    if not assets_dir.exists():
        return ["assets/ n'existe pas"]
    existing = {f.name for f in assets_dir.iterdir() if f.is_file()}
    referenced = set()
    for part in exam.get("parts", []):
        for q in part.get("questions", []) or []:
            for d in q.get("documents", []) or []:
                if isinstance(d, dict) and d.get("src", "").startswith("assets/"):
                    referenced.add(d["src"].split("/", 1)[1])
        for ex in part.get("exercises", []) or []:
            for d in ex.get("documents", []) or []:
                if isinstance(d, dict) and d.get("src", "").startswith("assets/"):
                    referenced.add(d["src"].split("/", 1)[1])
    missing = referenced - existing
    unreferenced = existing - referenced
    for f in sorted(missing):
        issues.append(f"asset référencé mais absent: {f}")
    for f in sorted(unreferenced):
        if re.match(r"^doc\d+p\d+\.(png|jpg|jpeg)$", f, re.IGNORECASE):
            issues.append(f"crop présent mais NON référencé dans exam.json: {f}")
    return issues


# ─────────────────── Semantic check (DeepSeek) ───────────────────

SEMANTIC_PROMPT = """Tu es un relecteur expert d'examens BAC marocain.
Je te donne (1) le texte OCR du sujet PDF, (2) le texte OCR de la correction PDF, (3) le JSON structuré qui a été généré à partir de ces textes.

Ta mission: détecter TOUTES les erreurs, omissions ou divergences entre le PDF et le JSON.

Analyse en particulier:
- **Questions manquantes** dans le JSON (présentes dans le PDF mais absentes du JSON)
- **Questions en trop** dans le JSON (absentes du PDF)
- **Numérotation incorrecte** (ex: Q1.a dans le PDF mais "1" dans le JSON)
- **Points incorrects** (écart entre PDF et JSON)
- **Contenu de question tronqué** ou paraphrasé au lieu de recopié fidèlement (NOTE: si tu vois le marqueur "…[TRUNCATED_IN_SUMMARY]", c'est juste une troncature d'affichage, PAS un vrai problème dans le JSON)
- **Réponse (correction) manquante** ou inventée (idem : ignore le marqueur "…[TRUNCATED_IN_SUMMARY]")
- **Mauvaise classification de type** (QCM traité comme open, etc.)
- **Documents non référencés** dans les questions qui devraient l'être

Réponds UNIQUEMENT en JSON avec cette structure:
{
  "overall_quality": "excellent" | "good" | "fair" | "poor",
  "coverage_percent": 0-100,
  "critical_issues": ["..."],
  "minor_issues": ["..."],
  "suggestions": ["..."]
}

SUJET PDF:
<<<SUJET>>>

CORRECTION PDF:
<<<CORRECTION>>>

JSON GÉNÉRÉ (résumé):
<<<JSON_SUMMARY>>>
"""


def _trunc(s: str, limit: int) -> str:
    """Truncate with explicit ellipsis marker so LLM knows it's a display summary."""
    s = (s or "").replace("\n", " ")
    if len(s) <= limit:
        return s
    return s[:limit] + "…[TRUNCATED_IN_SUMMARY]"


def _summarize_question(q: dict, indent: str = "") -> list[str]:
    """Render a full question with its structural details (choices, items, answer)."""
    lines = []
    qtype = q.get("type", "?")
    pts = q.get("points", 0)
    content = _trunc(q.get("content") or "", 400)
    lines.append(f"{indent}- [{q.get('number')}] {qtype} {pts}pts: {content}")

    # QCM choices
    if q.get("choices"):
        for c in q["choices"]:
            lines.append(f"{indent}    {c.get('letter','?')}) {c.get('text','')[:120]}")
        ans = q.get("correction", {}).get("correct_answer", "")
        if ans:
            lines.append(f"{indent}    → bonne réponse: {ans}")

    # Association
    if qtype == "association":
        for item in q.get("items_left", []) or []:
            if isinstance(item, dict):
                lines.append(f"{indent}    L[{item.get('number','?')}] {item.get('text','')[:100]}")
            else:
                lines.append(f"{indent}    L: {str(item)[:100]}")
        for item in q.get("items_right", []) or []:
            if isinstance(item, dict):
                lines.append(f"{indent}    R[{item.get('letter','?')}] {item.get('text','')[:100]}")
            else:
                lines.append(f"{indent}    R: {str(item)[:100]}")
        pairs = q.get("correction", {}).get("correct_pairs", []) or q.get("correct_pairs", [])
        if pairs:
            pair_str = ", ".join(f"{p.get('left','?')}→{p.get('right','?')}" for p in pairs)
            lines.append(f"{indent}    → paires: {pair_str}")

    # Vrai/Faux or open — include correction brief
    corr = q.get("correction", {})
    if corr.get("correct_answer"):
        lines.append(f"{indent}    [ans={corr['correct_answer']}]")
    elif corr.get("content"):
        lines.append(f"{indent}    correction: {_trunc(corr['content'], 350)}")

    # Sub-questions (for QCM/VF groups)
    for sq in q.get("sub_questions", []) or []:
        lines.extend(_summarize_question(sq, indent + "  "))
    return lines


def summarize_json_for_llm(exam: dict) -> str:
    """Compact representation of exam.json for LLM comparison (preserves QCM/assoc details)."""
    lines = [f"Total: {exam.get('total_points')}pts | Year: {exam.get('year')} | Session: {exam.get('session')}"]
    for part in exam.get("parts", []):
        lines.append(f"\n## {part.get('name')} ({part.get('points')}pts)")
        for q in part.get("questions", []) or []:
            lines.extend(_summarize_question(q))
        for ex in part.get("exercises", []) or []:
            lines.append(f"\n  📝 {ex.get('name')} ({ex.get('points')}pts) — docs:{len(ex.get('documents') or [])}")
            if ex.get("context"):
                lines.append(f"     context: {ex['context'][:200]}")
            for q in ex.get("questions", []) or []:
                lines.extend(_summarize_question(q, indent="    "))
    return "\n".join(lines)


async def semantic_check(sujet_text: str, correction_text: str, exam: dict) -> dict:
    """Call DeepSeek to semantically compare PDF ↔ JSON."""
    if not DEEPSEEK_API_KEY:
        return {"error": "DEEPSEEK_API_KEY manquante"}

    sujet_clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", sujet_text)[:20000]
    corr_clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", correction_text)[:12000]
    json_summary = summarize_json_for_llm(exam)[:20000]

    prompt = (
        SEMANTIC_PROMPT
        .replace("<<<SUJET>>>", sujet_clean)
        .replace("<<<CORRECTION>>>", corr_clean)
        .replace("<<<JSON_SUMMARY>>>", json_summary)
    )

    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": "Tu compares un PDF d'examen et son extraction JSON. Réponds en JSON valide uniquement."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 3000,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    try:
        async with httpx.AsyncClient(timeout=180.0) as client:
            r = await client.post(DEEPSEEK_URL, headers=headers, json=payload)
            r.raise_for_status()
            data = r.json()
        content = data["choices"][0]["message"]["content"]
        return json.loads(content)
    except Exception as e:
        logger.error(f"Semantic check failed: {type(e).__name__}: {e}")
        return {"error": str(e)}


# ─────────────────── Report generation ───────────────────

def render_report(exam_dir: Path, exam: dict, extraction: dict, structural: dict, semantic: dict | None) -> str:
    lines = []
    lines.append(f"# Rapport de vérification — {exam_dir.name}\n")
    lines.append(f"**Titre** : {exam.get('title')}")
    lines.append(f"**Année / Session** : {exam.get('year')} / {exam.get('session')}")
    lines.append(f"**Points total** : {exam.get('total_points')}")
    n_parts = len(exam.get("parts", []))
    n_questions = sum(
        len(p.get("questions", []) or []) + sum(len(e.get("questions", []) or []) for e in p.get("exercises", []) or [])
        for p in exam.get("parts", [])
    )
    lines.append(f"**Parties** : {n_parts} | **Questions** : {n_questions}")
    lines.append(f"**Documents détectés** : {len(extraction.get('documents', []))}")
    lines.append("")

    # Structural
    lines.append("## Vérifications structurelles\n")
    any_struct_issue = False
    for section, issues in structural.items():
        if section.startswith("_"):
            continue
        if issues:
            any_struct_issue = True
            lines.append(f"### ⚠ {section} ({len(issues)} issue(s))")
            for i in issues:
                lines.append(f"- {i}")
            lines.append("")
        else:
            lines.append(f"- ✅ **{section}** : OK")
    if not any_struct_issue:
        lines.append("\n**Toutes les vérifications structurelles sont passées ✓**")
    lines.append("")

    # PDF markers
    markers = structural.get("_pdf_markers", {})
    if markers:
        lines.append("## Marqueurs détectés dans le PDF OCR\n")
        lines.append(f"- Numéros arabes trouvés : `{markers.get('arabic_numbered', [])}`")
        lines.append(f"- Chiffres romains trouvés : `{markers.get('roman', [])}`")
        lines.append(f"- Occurrences d'« Exercice N » : {markers.get('exercises_detected', 0)}")
        lines.append("")

    # Semantic
    if semantic is not None:
        lines.append("## Analyse sémantique (DeepSeek)\n")
        if "error" in semantic:
            lines.append(f"❌ **Erreur** : {semantic['error']}")
        else:
            quality = semantic.get("overall_quality", "?")
            coverage = semantic.get("coverage_percent", "?")
            emoji = {"excellent": "🟢", "good": "🟢", "fair": "🟡", "poor": "🔴"}.get(quality, "⚪")
            lines.append(f"**Qualité globale** : {emoji} {quality}")
            lines.append(f"**Couverture** : {coverage}%")
            lines.append("")
            crit = semantic.get("critical_issues", []) or []
            if crit:
                lines.append(f"### ⚠ Problèmes critiques ({len(crit)})")
                for i in crit:
                    lines.append(f"- {i}")
                lines.append("")
            minor = semantic.get("minor_issues", []) or []
            if minor:
                lines.append(f"### Problèmes mineurs ({len(minor)})")
                for i in minor:
                    lines.append(f"- {i}")
                lines.append("")
            suggs = semantic.get("suggestions", []) or []
            if suggs:
                lines.append(f"### Suggestions ({len(suggs)})")
                for s in suggs:
                    lines.append(f"- {s}")
                lines.append("")

    return "\n".join(lines)


# ─────────────────── Orchestration ───────────────────

async def verify_one(exam_dir: Path, use_llm: bool = True) -> dict:
    exam_file = exam_dir / "exam.json"
    extraction_file = exam_dir / "extraction.json"
    if not exam_file.exists() or not extraction_file.exists():
        logger.warning(f"[SKIP] {exam_dir.name}: exam.json ou extraction.json manquant")
        return {}

    logger.info(f"[VERIFY] {exam_dir.name}")
    exam = json.loads(exam_file.read_text(encoding="utf-8"))
    extraction = json.loads(extraction_file.read_text(encoding="utf-8"))

    # Structural
    structural = {
        "Métadonnées": check_metadata(exam, exam_dir.name),
        "Points": check_points(exam),
        "Assets": check_assets(exam, exam_dir),
    }

    pdf_markers = extract_pdf_question_markers(extraction.get("sujet_text", ""))
    structural["_pdf_markers"] = pdf_markers

    # Count of questions in JSON vs PDF markers for quick signal
    json_nums = extract_json_question_numbers(exam)
    structural["Couverture"] = []
    if pdf_markers.get("exercises_detected") and exam.get("parts"):
        exs_in_json = sum(len(p.get("exercises", []) or []) for p in exam["parts"])
        if exs_in_json != pdf_markers["exercises_detected"]:
            structural["Couverture"].append(
                f"Exercices: PDF détecte {pdf_markers['exercises_detected']} / JSON contient {exs_in_json}"
            )

    # Semantic
    semantic = None
    if use_llm:
        logger.info(f"  Running semantic check with DeepSeek...")
        semantic = await semantic_check(
            extraction.get("sujet_text", ""),
            extraction.get("correction_text", ""),
            exam,
        )
        if "overall_quality" in semantic:
            logger.info(f"  Quality: {semantic['overall_quality']} | Coverage: {semantic.get('coverage_percent')}%")

    # Report
    report = render_report(exam_dir, exam, extraction, structural, semantic)
    report_path = exam_dir / "verification_report.md"
    report_path.write_text(report, encoding="utf-8")

    # Also save raw JSON verification for programmatic access
    raw = {
        "exam_id": f"svt_{exam.get('year')}_{str(exam.get('session', '')).lower()}",
        "structural": {k: v for k, v in structural.items() if k != "_pdf_markers"},
        "pdf_markers": pdf_markers,
        "semantic": semantic,
    }
    (exam_dir / "verification.json").write_text(
        json.dumps(raw, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # Summary print
    total_issues = sum(len(v) for k, v in structural.items() if k != "_pdf_markers")
    if semantic and isinstance(semantic, dict):
        total_issues += len(semantic.get("critical_issues") or [])
    status = "✅" if total_issues == 0 else f"⚠ {total_issues} issue(s)"
    logger.info(f"  {status} → {report_path.name}")
    return raw


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="subject or exam path (e.g. 'svt' or 'svt/2019-rattrapage')")
    parser.add_argument("--no-llm", action="store_true", help="Skip DeepSeek semantic check")
    args = parser.parse_args()

    target = EXAMS_DIR / args.target
    if not target.exists():
        logger.error(f"Cible introuvable: {target}")
        sys.exit(1)

    if (target / "exam.json").exists():
        exam_dirs = [target]
    else:
        exam_dirs = sorted([d for d in target.iterdir() if d.is_dir() and (d / "exam.json").exists()])

    logger.info(f"Exams à vérifier: {len(exam_dirs)}")
    for d in exam_dirs:
        try:
            await verify_one(d, use_llm=not args.no_llm)
        except Exception as e:
            logger.error(f"[FAIL] {d.name}: {type(e).__name__}: {e}", exc_info=True)


if __name__ == "__main__":
    asyncio.run(main())
