"""
Batch Build exam.json — Étape C

Pour chaque examen disposant de `extraction.json` ET d'images découpées dans `assets/doc*p*.png` :

1. Lit les images découpées (nommées docXpY.png = doc X de page Y)
2. Appelle Mistral Vision (pixtral-large-latest) sur chaque image en parallèle → description
3. Appelle DeepSeek avec texte OCR + liste docs → exam.json structuré (P1 + P2)
4. Met à jour index.json (ajoute/remplace l'entrée)

Usage:
    python backend/scripts/batch_build_json.py svt                    # tous
    python backend/scripts/batch_build_json.py svt/2019-rattrapage    # un seul
    python backend/scripts/batch_build_json.py --force svt            # re-traiter même si exam.json existe

Prérequis:
    pip install httpx python-dotenv
"""
import argparse
import asyncio
import base64
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

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "").strip()
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_URL = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/chat/completions").strip()
DEEPSEEK_MODEL = os.getenv("DEEPSEEK_MODEL", "deepseek-chat").strip()

MISTRAL_CHAT_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_VISION_MODEL = "pixtral-large-latest"

EXAMS_DIR = ROOT / "backend" / "data" / "exams"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("batch_build")

MAX_CONCURRENT_VISION = 3
SEM_VISION = asyncio.Semaphore(MAX_CONCURRENT_VISION)

DOC_RE = re.compile(r"^doc(\d+)p(\d+)\.(png|jpg|jpeg)$", re.IGNORECASE)


# ─────────────────────────── Vision ────────────────────────────

VISION_PROMPT_TEMPLATE = """Tu es un expert en analyse de documents d'examens scientifiques marocains (SVT).

Cette image est le document « {name} » extrait d'un examen national.

Décris PRÉCISÉMENT et BRIÈVEMENT le contenu de ce document en français :
- Type : graphique, courbe, tableau, schéma, figure, diagramme, carte, etc.
- Contenu : axes, légendes, valeurs clés, structures, étapes, relations, symboles.
- En 2 à 4 phrases maximum.

Réponds directement avec la description, sans préfixe ni titre."""


async def describe_doc(client: httpx.AsyncClient, img_path: Path, doc_name: str) -> str:
    """Appelle Mistral Vision pour décrire un document."""
    async with SEM_VISION:
        with open(img_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        mime = "image/png" if img_path.suffix.lower() == ".png" else "image/jpeg"
        payload = {
            "model": MISTRAL_VISION_MODEL,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": VISION_PROMPT_TEMPLATE.format(name=doc_name)},
                    {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                ],
            }],
            "max_tokens": 400,
            "temperature": 0.15,
        }
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
        try:
            r = await client.post(MISTRAL_CHAT_URL, headers=headers, json=payload, timeout=90.0)
            r.raise_for_status()
            data = r.json()
            desc = data["choices"][0]["message"]["content"].strip()
            logger.info(f"    VISION {img_path.name}: {len(desc)} chars")
            return desc
        except Exception as e:
            logger.error(f"    VISION FAILED {img_path.name}: {type(e).__name__}: {e}")
            return f"Document visuel de l'examen ({img_path.name})."


# ─────────────────────── DeepSeek structuring ──────────────────

def _parse_json_safe(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Best effort: find outermost {}
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        return {}


async def call_deepseek(client: httpx.AsyncClient, prompt: str, label: str) -> dict:
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {"role": "system", "content": "Expert en structuration d'examens marocains. 'content' = QUESTION du SUJET, 'correction.content' = RÉPONSE. Réponds uniquement en JSON valide."},
            {"role": "user", "content": prompt},
        ],
        "max_tokens": 8192,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }
    last_exc: Exception | None = None
    for attempt in range(1, 4):
        try:
            r = await client.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=300.0)
            r.raise_for_status()
            data = r.json()
            content = data["choices"][0]["message"]["content"]
            finish = data["choices"][0].get("finish_reason", "")
            logger.info(f"    [{label}] {len(content)} chars, finish={finish}")
            return _parse_json_safe(content)
        except (httpx.ReadError, httpx.ReadTimeout, httpx.RemoteProtocolError, httpx.ConnectError) as e:
            last_exc = e
            wait = 2 ** attempt
            logger.warning(f"    [{label}] network error ({type(e).__name__}), retry {attempt}/3 in {wait}s...")
            await asyncio.sleep(wait)
    raise last_exc if last_exc else RuntimeError(f"{label}: all retries failed")


RULES = """RÈGLES CRITIQUES:

1. DISTINCTION SUJET vs CORRECTION:
   - "content" = texte de la QUESTION du SUJET (ce que l'élève doit faire). JAMAIS la réponse.
   - "correction.content" = RÉPONSE officielle uniquement.

2. TYPES (examens marocains):
   - QCM: items numérotés avec a,b,c,d → type="qcm" avec sub_questions. Chaque sub_question a "points", "choices":[{"letter":"a","text":"..."}], "correction":{"correct_answer":"c"}.
   - ASSOCIATION: "Recopiez les couples..." → type="association" avec "items_left":[...], "items_right":[...], "correct_pairs":[{"left":"1","right":"b"}].
   - VRAI_FAUX: → type="vrai_faux" avec sub_questions ayant correction.correct_answer ("vrai"/"faux").
   - OPEN: toute autre question.

3. SOUS-QUESTIONS: 1.a, 1.b = sub_questions SÉPARÉES.
4. Recopier le TEXTE ORIGINAL du sujet. Pas de résumé.
5. Corrections concises mais complètes."""


async def structure_exam(client: httpx.AsyncClient, sujet_text: str, correction_text: str, docs: list[dict], meta: dict) -> dict:
    """Appelle DeepSeek en 2 parties (P1 + P2) et fusionne."""
    docs_lines = []
    for i, d in enumerate(docs, 1):
        docs_lines.append(
            f'  GLOBAL_DOC_{i}: nom="{d["name"]}" | type={d["type"]} | page_pdf={d["page"]} | '
            f'fichier="{d["src"]}" | description="{d["description"]}"'
        )
    docs_block = "\n".join(docs_lines) if docs_lines else "  (aucun document)"

    sujet_clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", sujet_text)[:30000]
    correction_clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", correction_text)[:30000]

    # Part 1
    prompt_p1 = f"""Structure UNIQUEMENT la "Première partie" (Restitution des connaissances, ~5pts) de cet examen BAC marocain en JSON.

SUJET:
{sujet_clean}

CORRECTION:
{correction_clean}

DOCUMENTS:
{docs_block}

{RULES}

Réponds avec un seul objet JSON ayant "name", "points", "questions"."""

    # Part 2
    prompt_p2 = f"""Structure UNIQUEMENT la "Deuxième partie" (Exploitation des documents, ~15pts) de cet examen BAC marocain en JSON.

SUJET:
{sujet_clean}

CORRECTION:
{correction_clean}

DOCUMENTS:
{docs_block}

{RULES}

Chaque question peut référencer des documents via "documents":["doc_gN"].

Réponds avec un seul objet JSON ayant "name", "points", "exercises"."""

    p1, p2 = await asyncio.gather(
        call_deepseek(client, prompt_p1, "P1"),
        call_deepseek(client, prompt_p2, "P2"),
    )

    exam_json = {
        "title": meta["title"],
        "subject": "SVT",
        "subject_full": meta["title"],
        "year": meta["year"],
        "session": meta["session"],
        "duration_minutes": 180,
        "coefficient": 5,
        "total_points": 20,
        "parts": [p1, p2],
    }

    # Post-process: embed full doc objects at exercise level
    _enrich_exercise_documents(exam_json, docs)
    return exam_json


def _enrich_exercise_documents(exam_json: dict, docs: list[dict]) -> None:
    """Post-process exam JSON after DeepSeek structuring:

    1. Collect per-exercise the global docs referenced by its questions (in first appearance).
    2. Renumber docs PER EXERCISE starting at "Document 1" with new IDs `doc_eN_M`.
    3. Rewrite all question.documents[] refs to use the new per-exercise IDs.
    4. Embed full doc objects at the exercise level (required by the UI).
    5. Normalize association items_left/items_right to plain string arrays.

    This way E1 shows "Document 1, 2, 3", E2 resets to "Document 1, 2, 3", matching the
    original PDF convention. The backend's `_extract_referenced_docs` will then filter
    correctly because doc numeric suffixes match the question text mentions.
    """
    docs_by_global_id = {d["id"]: d for d in docs}

    for part in exam_json.get("parts", []):
        # Normalize any association questions directly in Première partie
        for q in part.get("questions", []) or []:
            _normalize_association_items(q)
            for sq in q.get("sub_questions", []) or []:
                _normalize_association_items(sq)

        ex_idx = 0
        for ex in part.get("exercises", []) or []:
            ex_idx += 1

            # 1+2. Collect unique global refs in appearance order
            order: list[str] = []
            seen: set[str] = set()
            for q in ex.get("questions", []) or []:
                for ref in q.get("documents") or []:
                    rid = ref if isinstance(ref, str) else (ref.get("id") if isinstance(ref, dict) else None)
                    if rid and rid not in seen and rid in docs_by_global_id:
                        seen.add(rid)
                        order.append(rid)

            # Build mapping global_id → local_id (Document 1, 2, 3... for this exercise)
            id_map = {gid: f"doc_e{ex_idx}_{i+1}" for i, gid in enumerate(order)}

            # 3. Rewrite question.documents refs
            for q in ex.get("questions", []) or []:
                _normalize_association_items(q)
                for sq in q.get("sub_questions", []) or []:
                    _normalize_association_items(sq)
                new_refs = []
                for ref in q.get("documents") or []:
                    rid = ref if isinstance(ref, str) else (ref.get("id") if isinstance(ref, dict) else None)
                    if rid and rid in id_map:
                        new_refs.append(id_map[rid])
                if new_refs:
                    q["documents"] = new_refs

            # 4. Embed full doc objects with new IDs + clean per-exercise titles
            ex["documents"] = [
                {
                    "id": id_map[gid],
                    "type": docs_by_global_id[gid].get("type", "figure"),
                    "title": f"Document {i+1}",  # Per-exercise numbering, no page info
                    "description": docs_by_global_id[gid].get("description", ""),
                    "src": docs_by_global_id[gid]["src"],
                }
                for i, gid in enumerate(order)
            ]


def _normalize_association_items(q: dict) -> None:
    """Convert items_left/items_right from [{number, text}] / [{letter, text}] to plain strings.

    The UI AnswerInput expects string[] and crashes if items are objects.
    """
    if q.get("type") != "association":
        return
    for key in ("items_left", "items_right"):
        items = q.get(key) or []
        if items and isinstance(items[0], dict):
            q[key] = [
                (it.get("text") or it.get("label") or str(it))
                for it in items
                if isinstance(it, dict)
            ]


# ─────────────────────────── Pipeline ──────────────────────────

async def process_exam(exam_dir: Path, force: bool = False) -> bool:
    extraction_file = exam_dir / "extraction.json"
    exam_file = exam_dir / "exam.json"
    assets_dir = exam_dir / "assets"

    if not extraction_file.exists():
        logger.warning(f"[SKIP] {exam_dir.name}: extraction.json manquant (lancer batch_ocr.py d'abord)")
        return False

    if exam_file.exists() and not force:
        logger.info(f"[SKIP] {exam_dir.name}: exam.json existe déjà (utilisez --force)")
        return False

    logger.info(f"[GO] {exam_dir.name}")
    extraction = json.loads(extraction_file.read_text(encoding="utf-8"))

    # Scan assets for docXpY.png
    doc_files = []
    if assets_dir.exists():
        for f in sorted(assets_dir.iterdir()):
            m = DOC_RE.match(f.name)
            if m:
                doc_idx, page_idx = int(m.group(1)), int(m.group(2))
                doc_files.append({"path": f, "doc": doc_idx, "page": page_idx})
    # Sort: page then doc index
    doc_files.sort(key=lambda x: (x["page"], x["doc"]))

    if not doc_files:
        logger.warning(f"  ATTENTION: aucun asset 'docXpY.png' dans {assets_dir.name}/")

    # Vision descriptions in parallel
    async with httpx.AsyncClient() as client:
        if doc_files:
            tasks = [describe_doc(client, d["path"], f"Document {i}") for i, d in enumerate(doc_files, 1)]
            descriptions = await asyncio.gather(*tasks)
        else:
            descriptions = []

        docs = []
        for i, (d, desc) in enumerate(zip(doc_files, descriptions), 1):
            docs.append({
                "id": f"doc_g{i}",
                "name": f"Document {i}",
                "type": "figure",
                "page": d["page"],
                "src": f"assets/{d['path'].name}",
                "description": desc,
            })

        # Call DeepSeek to structure
        meta = {
            "title": extraction.get("title", f"SVT {extraction.get('year')} {extraction.get('session')}"),
            "year": extraction.get("year"),
            "session": extraction.get("session"),
        }
        logger.info(f"  Structuring with DeepSeek...")
        exam_json = await structure_exam(
            client,
            extraction.get("sujet_text", ""),
            extraction.get("correction_text", ""),
            docs,
            meta,
        )

    # Write exam.json
    exam_file.write_text(json.dumps(exam_json, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"  [OK] exam.json écrit ({exam_file.stat().st_size} bytes)")

    # Update extraction.json with docs
    extraction["documents"] = docs
    extraction_file.write_text(json.dumps(extraction, ensure_ascii=False, indent=2), encoding="utf-8")

    # Update index.json
    _update_index(exam_dir, meta)

    # Fill missing exercise contexts (énoncés) extracted from sujet OCR
    try:
        from fill_exercise_contexts import apply_contexts  # type: ignore
        apply_contexts(exam_dir, overwrite=False)
    except Exception as e:
        logger.warning(f"  Context fill failed (non-blocking): {type(e).__name__}: {e}")

    # Final verification step (PDF OCR ↔ JSON comparison + DeepSeek semantic check)
    try:
        from verify_exam import verify_one  # type: ignore
        logger.info(f"  Running verification...")
        await verify_one(exam_dir, use_llm=True)
    except Exception as e:
        logger.warning(f"  Verification step failed (non-blocking): {type(e).__name__}: {e}")

    return True


def _update_index(exam_dir: Path, meta: dict):
    index_path = EXAMS_DIR / "index.json"
    data = []
    if index_path.exists():
        data = json.loads(index_path.read_text(encoding="utf-8-sig"))
    exam_id = f"svt_{meta['year']}_{meta['session'].lower()}"
    data = [e for e in data if e.get("id") != exam_id]
    data.append({
        "id": exam_id,
        "subject": "SVT",
        "year": meta["year"],
        "session": meta["session"],
        "path": f"svt/{exam_dir.name}",
        "title": meta["title"],
        "subject_full": meta["title"],
        "duration_minutes": 180,
        "coefficient": 5,
        "total_points": 20,
        "note": "",
    })
    data.sort(key=lambda e: (-e.get("year", 0), e.get("session", ""), e.get("subject", "")))
    index_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"  [OK] index.json mis à jour ({exam_id})")


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="subject folder (e.g. 'svt') or specific exam (e.g. 'svt/2019-rattrapage')")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()

    if not MISTRAL_API_KEY or not DEEPSEEK_API_KEY:
        logger.error("MISTRAL_API_KEY ou DEEPSEEK_API_KEY manquante dans backend/.env")
        sys.exit(1)

    target = EXAMS_DIR / args.target
    if not target.exists():
        logger.error(f"Cible introuvable: {target}")
        sys.exit(1)

    if (target / "extraction.json").exists() or (target / "pdfs").exists():
        exam_dirs = [target]
    else:
        exam_dirs = sorted([d for d in target.iterdir() if d.is_dir()])

    processed = 0
    for d in exam_dirs:
        try:
            ok = await process_exam(d, force=args.force)
            if ok:
                processed += 1
        except Exception as e:
            logger.error(f"[FAIL] {d.name}: {type(e).__name__}: {e}", exc_info=True)

    logger.info(f"\nDONE: {processed}/{len(exam_dirs)} examens structurés")


if __name__ == "__main__":
    asyncio.run(main())
