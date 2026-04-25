"""
Batch Build Math Pipeline — Étape B (Mathématiques)

Pour chaque examen de mathématiques contenant `extraction.json` mais sans `exam.json` :

1. Lit le texte OCR (sujet + correction)
2. Appelle DeepSeek avec un prompt MATH spécifique qui PRÉSERVE le LaTeX
3. Structure l'examen en `parts[0].exercises[]` (ex1, ex2, ex3, ex4, problème)
4. Vérifie les points totaux (doit = 20)
5. Écrit `exam.json` + met à jour `index.json`

Usage:
    python backend/scripts/batch_build_math.py mathematiques                    # tous les dossiers math
    python backend/scripts/batch_build_math.py mathematiques/2024-rattrapage    # un seul
    python backend/scripts/batch_build_math.py --force mathematiques            # re-génère

Prérequis:
    pip install httpx python-dotenv
    MISTRAL_API_KEY + DEEPSEEK_API_KEY dans backend/.env
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

# Load env
ROOT = Path(__file__).resolve().parent.parent.parent
load_dotenv(ROOT / "backend" / ".env")

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "").strip()
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"

EXAMS_DIR = ROOT / "backend" / "data" / "exams"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("batch_build_math")


# ──────────────────────── Prompt DeepSeek (math) ────────────────────────

MATH_RULES = r"""RÈGLES CRITIQUES POUR MATHÉMATIQUES BAC MAROCAIN:

1. STRUCTURE:
   - L'examen est composé de 3 à 5 exercices + éventuellement un problème.
   - Chaque exercice vaut ses propres points. Total = 20 points.
   - Structure JSON demandée :
     {
       "parts": [
         {
           "name": "Examen",
           "points": 20,
           "exercises": [
             {
               "name": "Exercice 1 — ...",
               "points": <nombre>,
               "context": "<énoncé de mise en contexte commun à toutes les questions>",
               "questions": [
                 {
                   "id": "e1_qN",
                   "number": "1.a",
                   "type": "open",
                   "points": <nombre>,
                   "content": "<question à résoudre>",
                   "correction": { "content": "<correction détaillée>" }
                 }
               ]
             }
           ]
         }
       ]
     }

2. LATEX OBLIGATOIRE:
   - TOUTES les formules mathématiques doivent être en LaTeX inline `$...$` ou display `$$...$$`.
   - Exemples: $f(x)=e^x-x$, $\lim_{x\to+\infty}f(x)=1$, $\int_0^1 f(x)\,dx$, $\vec{AB}\cdot\vec{CD}$, $\overrightarrow{OA}$.
   - Suites: $u_{n+1}=\dfrac{4u_n-2}{1+u_n}$, $(u_n)$ convergente.
   - Complexes: $|z|=\sqrt{6}$, $\arg(z)\equiv\dfrac{-\pi}{4}[2\pi]$, $e^{i\frac{\pi}{3}}$.
   - Fractions TOUJOURS `\dfrac{a}{b}` (pas `\frac`).
   - Logs: $\ln(1+x)$, $\ln 2$.
   - Racines: $\sqrt{3}$, $\sqrt[3]{x}$.
   - Matrices/systèmes: `\begin{cases} x=2+2t \\ y=-1-2t \\ z=t \end{cases}`.

3. DISTINCTION SUJET vs CORRECTION:
   - `content` = la QUESTION du sujet (ce que l'élève doit faire). JAMAIS la réponse.
   - `correction.content` = la réponse/démonstration officielle.
   - Les points dans la marge du sujet ({0.25, 0.5, 0.75, 1, ...}) doivent être reportés dans `points`.

4. QUESTIONS IMBRIQUÉES (1.a, 1.b, 2.a, 2.b, 2.c) :
   - Toujours séparer en questions distinctes avec `number` = "1.a", "1.b", etc.
   - `id` = `e<N>_q<Na>` : e1_q1a, e1_q1b, e1_q2a, etc.

5. CONTEXT:
   - Le champ `context` contient l'énoncé commun qui introduit l'exercice (définition des suites, données initiales, figure, etc.).
   - Il est affiché UNE SEULE FOIS avant toutes les questions.

6. CORRECTION:
   - Concise mais complète (les étapes de calcul clés + résultat final encadré avec `\boxed{...}`).
   - Préserver TOUS les calculs importants du corrigé officiel.

7. TYPE:
   - Pour les maths, toujours `"type": "open"`.

8. TOTAL DES POINTS:
   - Vérifie que la somme des `points` des questions de chaque exercice = `points` de l'exercice.
   - Vérifie que la somme des `points` des exercices = 20.
"""


def _parse_json_safe(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        m = re.search(r"\{[\s\S]*\}", text)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                pass
        return {}


async def call_deepseek(client: httpx.AsyncClient, prompt: str, label: str, max_tokens: int = 8192) -> dict:
    headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": DEEPSEEK_MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Expert en structuration d'examens de mathématiques du BAC marocain. Tu DOIS préserver LaTeX ($...$ et $$...$$) dans les énoncés et corrections. Tu réponds UNIQUEMENT avec un objet JSON valide.",
            },
            {"role": "user", "content": prompt},
        ],
        "max_tokens": max_tokens,
        "temperature": 0.1,
        "response_format": {"type": "json_object"},
    }
    last_exc = None
    for attempt in range(1, 4):
        try:
            r = await client.post(DEEPSEEK_URL, headers=headers, json=payload, timeout=300.0)
            r.raise_for_status()
            data = r.json()
            content = data["choices"][0]["message"]["content"]
            finish = data["choices"][0].get("finish_reason", "")
            logger.info(f"    [{label}] {len(content)} chars, finish={finish}")
            return _parse_json_safe(content)
        except Exception as e:
            last_exc = e
            wait = 2 ** attempt
            logger.warning(f"    [{label}] error ({type(e).__name__}: {e}), retry {attempt}/3 in {wait}s...")
            await asyncio.sleep(wait)
    raise last_exc if last_exc else RuntimeError(f"{label}: all retries failed")


async def list_exercises(
    client: httpx.AsyncClient,
    sujet_text: str,
    meta: dict,
) -> list[dict]:
    """Première passe DeepSeek : liste des exercices (name, points, topic) sans détails."""
    sujet_clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", sujet_text)[:20000]
    prompt = f"""Identifie la LISTE DES EXERCICES de cet examen de mathématiques BAC marocain {meta['year']} {meta['session']}.

SUJET OCR:
{sujet_clean}

Réponds UNIQUEMENT avec ce JSON:
{{
  "exercises": [
    {{"key": "ex1", "name": "Exercice 1 — <thème>", "points": <nombre>, "topic_hint": "<mot-clé principal, ex: Suites, Complexes, Géométrie, Probabilités, Fonctions, Problème>"}},
    ...
  ]
}}

La somme des `points` doit valoir exactement 20. Typiquement 3-5 exercices (ex1, ex2, ex3, ex4) + un "problème" éventuel (appelé `probleme` dans `key`).
"""
    result = await call_deepseek(client, prompt, "LIST_EX", max_tokens=1500)
    return result.get("exercises", [])


async def build_exercise(
    client: httpx.AsyncClient,
    ex_info: dict,
    sujet_text: str,
    correction_text: str,
    meta: dict,
) -> dict:
    """Deuxième passe : structure UN exercice complet avec LaTeX + corrections."""
    sujet_clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", sujet_text)[:30000]
    correction_clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", correction_text)[:30000]

    key = ex_info.get("key", "ex1")
    name = ex_info.get("name", "Exercice")
    points = ex_info.get("points", 0)
    topic_hint = ex_info.get("topic_hint", "")

    prompt = f"""Structure UNIQUEMENT l'exercice « {name} » ({points} points, thème: {topic_hint}) de cet examen de mathématiques BAC marocain.

SUJET OCR (extrait complet):
{sujet_clean}

CORRECTION OCR (extrait complet):
{correction_clean}

{MATH_RULES}

PRÉFIXE des IDs: utilise `{key}_qN` (ex: {key}_q1a, {key}_q1b, ...).

Réponds avec UN SEUL objet JSON:
{{
  "name": "{name}",
  "points": {points},
  "context": "<énoncé commun en LaTeX>",
  "questions": [
    {{
      "id": "{key}_q1a",
      "number": "1.a",
      "type": "open",
      "points": <nombre>,
      "content": "<question en LaTeX>",
      "correction": {{ "content": "<correction détaillée en LaTeX>" }}
    }}
  ]
}}

IMPORTANT:
- La somme des `points` des questions DOIT valoir {points}.
- N'inclus AUCUNE autre clé de premier niveau.
- Si c'est un grand problème avec plusieurs parties, les questions peuvent être préfixées "I.1", "II.2.a", etc.
"""
    return await call_deepseek(client, prompt, f"EX[{key}]", max_tokens=8000)


async def structure_math_exam(
    client: httpx.AsyncClient,
    sujet_text: str,
    correction_text: str,
    meta: dict,
) -> dict:
    """Structure un examen de mathématiques en 2 étapes :
    1. Liste les exercices
    2. Structure chaque exercice en parallèle
    """
    # Step 1: liste des exercices
    logger.info("  Step 1/2: listing exercises...")
    ex_list = await list_exercises(client, sujet_text, meta)
    if not ex_list:
        logger.error("  Aucun exercice détecté")
        return {"title": meta["title"], "parts": []}
    logger.info(f"    → {len(ex_list)} exercices: {[e.get('key') for e in ex_list]}")

    # Step 2: construire chaque exercice en parallèle
    logger.info(f"  Step 2/2: building {len(ex_list)} exercises in parallel...")
    tasks = [build_exercise(client, ex, sujet_text, correction_text, meta) for ex in ex_list]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    exercises = []
    for ex_info, res in zip(ex_list, results):
        if isinstance(res, Exception):
            logger.warning(f"    {ex_info.get('key')}: FAILED ({type(res).__name__}: {res})")
            continue
        if not res or not res.get("questions"):
            logger.warning(f"    {ex_info.get('key')}: empty result")
            continue
        exercises.append(res)

    exam_json = {
        "title": meta["title"],
        "subject": "Mathematiques",
        "subject_full": meta["title"],
        "year": meta["year"],
        "session": meta["session"],
        "duration_minutes": 180,
        "coefficient": 7,
        "total_points": 20,
        "note": "L'utilisation de la calculatrice non programmable est autorisée. Le candidat peut traiter les exercices suivant l'ordre qui lui convient. $\\ln$ désigne la fonction logarithme népérien.",
        "parts": [
            {
                "name": "Examen",
                "points": 20,
                "exercises": exercises,
            }
        ],
    }
    return exam_json


def _verify_points(exam_json: dict) -> tuple[bool, str]:
    """Vérifie que la somme des points = 20."""
    total = 0.0
    qcount = 0
    details = []
    for part in exam_json.get("parts", []):
        for ex in part.get("exercises", []):
            ex_sum = sum(q.get("points", 0) for q in ex.get("questions", []))
            declared = ex.get("points", 0)
            details.append(f"    {ex.get('name', '?')}: {ex_sum}pts (déclaré={declared})")
            total += ex_sum
            qcount += len(ex.get("questions", []))
    details.append(f"    TOTAL: {total}pts | {qcount} questions")
    ok = abs(total - 20) < 0.01
    return ok, "\n".join(details)


# ──────────────────────── Pipeline ────────────────────────

async def process_exam(exam_dir: Path, force: bool = False) -> bool:
    extraction_file = exam_dir / "extraction.json"
    exam_file = exam_dir / "exam.json"

    if not extraction_file.exists():
        logger.warning(f"[SKIP] {exam_dir.name}: extraction.json manquant (lancer batch_ocr.py d'abord)")
        return False

    if exam_file.exists() and not force:
        logger.info(f"[SKIP] {exam_dir.name}: exam.json existe déjà (utilisez --force)")
        return False

    logger.info(f"[GO] {exam_dir.name}")
    extraction = json.loads(extraction_file.read_text(encoding="utf-8"))

    meta = {
        "title": extraction.get("title", f"Math {extraction.get('year')} {extraction.get('session')}"),
        "year": extraction.get("year"),
        "session": extraction.get("session"),
    }

    async with httpx.AsyncClient() as client:
        exam_json = await structure_math_exam(
            client,
            extraction.get("sujet_text", ""),
            extraction.get("correction_text", ""),
            meta,
        )

    # Verify
    ok, details = _verify_points(exam_json)
    logger.info(f"  Vérification:\n{details}")
    if not ok:
        logger.warning(f"  [WARN] Total ≠ 20 pour {exam_dir.name}. Le JSON est écrit quand même.")

    exam_file.write_text(json.dumps(exam_json, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"  [OK] exam.json écrit ({exam_file.stat().st_size} bytes)")
    return True


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="subject folder ('mathematiques') or specific exam ('mathematiques/2023-normale')")
    parser.add_argument("--force", action="store_true", help="Re-generate even if exam.json exists")
    args = parser.parse_args()

    if not DEEPSEEK_API_KEY:
        logger.error("DEEPSEEK_API_KEY manquante dans backend/.env")
        sys.exit(1)

    target = EXAMS_DIR / args.target
    if not target.exists():
        logger.error(f"Cible introuvable: {target}")
        sys.exit(1)

    if (target / "extraction.json").exists() or (target / "exam.json").exists():
        exam_dirs = [target]
    else:
        exam_dirs = sorted([d for d in target.iterdir() if d.is_dir()])

    logger.info(f"Exams à traiter: {len(exam_dirs)}")
    processed = 0
    for d in exam_dirs:
        try:
            ok = await process_exam(d, force=args.force)
            if ok:
                processed += 1
        except Exception as e:
            logger.error(f"[FAIL] {d.name}: {type(e).__name__}: {e}")

    logger.info(f"\nDONE: {processed}/{len(exam_dirs)} examens générés")


if __name__ == "__main__":
    asyncio.run(main())
