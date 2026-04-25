"""
Batch Build Physique-Chimie Pipeline — Étape B (Physique-Chimie)

Pour chaque examen de physique-chimie contenant `extraction.json` + `assets/` :

1. Scanne les assets (fig1pN, figcicontrepN, figcidessouspN, diagcicontrepN,
   fig11pN, figcicontre2pN, figsuivantepN…) et associe chaque fichier à une
   légende canonique (« Figure 1 », « Figure ci-contre », « Diagramme ci-contre »…).
2. Appelle Mistral Vision sur chaque asset pour obtenir une description.
3. Détecte la liste des exercices via DeepSeek (prompt spécifique PC).
4. Pour chaque exercice : DeepSeek structure questions + corrections en LaTeX,
   et rattache les documents pertinents (en s'appuyant sur les plages de pages).
5. Vérifie la somme des points (=20) puis écrit `exam.json`.

Conventions de nommage des assets physique-chimie:
  fig<N>p<P>.png            → Figure <N> de la page <P>
  fig<N><N>p<P>.png         → 2ème occurrence de Figure <N> sur la page <P>
  figcicontrep<P>.png       → « Figure ci-contre »
  figcicontre<K>p<P>.png    → K-ème « Figure ci-contre »
  figcidessousp<P>.png      → « Figure ci-dessous »
  figcidessous<K>p<P>.png   → K-ème « Figure ci-dessous »
  diagcicontrep<P>.png      → « Diagramme ci-contre »
  diagcidessousp<P>.png     → « Diagramme ci-dessous »
  graphcidessousp<P>.png    → « Graphique ci-dessous »
  figsuivantep<P>.png       → « Figure suivante »
  montp<P>.png              → « Montage » (page <P>)

Usage:
    python backend/scripts/batch_build_physique.py physique
    python backend/scripts/batch_build_physique.py physique/2024-normale
    python backend/scripts/batch_build_physique.py --force physique
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
DEEPSEEK_URL = "https://api.deepseek.com/chat/completions"
DEEPSEEK_MODEL = "deepseek-chat"
MISTRAL_CHAT_URL = "https://api.mistral.ai/v1/chat/completions"
MISTRAL_VISION_MODEL = "pixtral-large-latest"
MISTRAL_CHAT_MODEL = "mistral-large-latest"

# LLM provider: 'deepseek' or 'mistral'. Auto-falls back on 402 errors.
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "deepseek").lower()

EXAMS_DIR = ROOT / "backend" / "data" / "exams"

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("batch_build_physique")

SEM_VISION = asyncio.Semaphore(3)


# ─────────────────────────── Asset parsing ───────────────────────────

ASSET_RE = re.compile(
    r"^(?P<kind>[a-zA-Z]+?)"          # fig / diag / graph / mont / figcicontre / figcidessous / figsuivante
    r"(?P<num>\d*)"                     # optional number (1..9) or "11"
    r"(?P<ordinal>\d*)"                 # rarely needed
    r"p(?P<page>\d+)"                   # page
    r"\.(?:png|jpg|jpeg)$",
    re.IGNORECASE,
)


def parse_asset_name(fname: str) -> dict | None:
    """Parse an asset filename into structured metadata.

    Returns a dict with: file, caption_canonical, caption_key, page, order.
    caption_canonical = label shown to the LLM (e.g. "Figure 1", "Figure ci-contre").
    caption_key = lowercase key for matching text (e.g. "figure 1", "figure ci-contre").
    order = sort key within an exercise (page*100 + local_index).
    """
    stem = fname.rsplit(".", 1)[0].lower()
    # page
    m = re.search(r"p(\d+)$", stem)
    if not m:
        return None
    page = int(m.group(1))
    left = stem[: m.start()]

    # Try numeric fig
    m2 = re.match(r"^fig(\d+)$", left)
    if m2:
        num = m2.group(1)
        # if 2 digits with same char (e.g. "11") treat as "figure 1 (bis)"
        if len(num) == 2 and num[0] == num[1]:
            label = f"Figure {num[0]} (bis)"
        else:
            label = f"Figure {int(num)}"
        return {
            "file": fname,
            "caption_canonical": label,
            "caption_key": label.lower(),
            "page": page,
            "kind": "figure",
        }

    # figcicontre / figcicontre2 / figcidessous / figcidessous2
    patterns = [
        (r"^figcicontre(\d*)$", "Figure ci-contre"),
        (r"^figcidessous(\d*)$", "Figure ci-dessous"),
        (r"^figsuivante(\d*)$", "Figure suivante"),
        (r"^diagcicontre(\d*)$", "Diagramme ci-contre"),
        (r"^diagcidessous(\d*)$", "Diagramme ci-dessous"),
        (r"^graphcicontre(\d*)$", "Graphique ci-contre"),
        (r"^graphcidessous(\d*)$", "Graphique ci-dessous"),
        (r"^graph(\d*)$", "Graphique"),
        (r"^diag(\d*)$", "Diagramme"),
        (r"^mont(\d*)$", "Montage"),
        (r"^fig$", "Figure"),
    ]
    for pat, base_label in patterns:
        m3 = re.match(pat, left)
        if m3:
            suffix = m3.group(1) if m3.groups() else ""
            label = f"{base_label} {suffix}".strip() if suffix else base_label
            return {
                "file": fname,
                "caption_canonical": label,
                "caption_key": label.lower(),
                "page": page,
                "kind": "figure",
            }
    # Fallback: unknown pattern
    return {
        "file": fname,
        "caption_canonical": left.capitalize(),
        "caption_key": left,
        "page": page,
        "kind": "figure",
    }


def scan_assets(exam_dir: Path) -> list[dict]:
    assets_dir = exam_dir / "assets"
    if not assets_dir.exists():
        return []
    out = []
    for f in sorted(assets_dir.iterdir()):
        if f.suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            continue
        info = parse_asset_name(f.name)
        if info is None:
            continue
        info["src"] = f"assets/{f.name}"
        info["abs_path"] = f
        out.append(info)
    out.sort(key=lambda x: (x["page"], x["file"]))
    return out


# ─────────────────────────── Vision descriptions ───────────────────────────

VISION_PROMPT = """Tu es un expert en analyse de documents d'examens scientifiques marocains (Physique-Chimie).

Cette image est « {name} » extraite d'un examen national de Physique-Chimie (2BAC PC/SM).

Décris PRÉCISÉMENT et BRIÈVEMENT le contenu en français :
- Type (schéma, graphique, courbe, montage électrique, dispositif expérimental, figure géométrique, chronophotographie, diagramme énergétique, etc.)
- Éléments visibles (axes et unités, valeurs clés, composants électriques, montages optiques, vecteurs, grandeurs physiques/chimiques, équations).
- En 2 à 4 phrases maximum, en conservant la terminologie physique/chimique.

Réponds directement avec la description, sans préfixe ni titre."""


async def describe_asset(client: httpx.AsyncClient, a: dict) -> None:
    """Mutate asset dict with a `description`."""
    path: Path = a["abs_path"]
    if not MISTRAL_API_KEY:
        a["description"] = f"Document '{a['caption_canonical']}' (page {a['page']})."
        return
    async with SEM_VISION:
        try:
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            mime = "image/png" if path.suffix.lower() == ".png" else "image/jpeg"
            payload = {
                "model": MISTRAL_VISION_MODEL,
                "messages": [{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": VISION_PROMPT.format(name=a["caption_canonical"])},
                        {"type": "image_url", "image_url": {"url": f"data:{mime};base64,{b64}"}},
                    ],
                }],
                "max_tokens": 400,
                "temperature": 0.15,
            }
            headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
            r = await client.post(MISTRAL_CHAT_URL, headers=headers, json=payload, timeout=90.0)
            r.raise_for_status()
            data = r.json()
            a["description"] = data["choices"][0]["message"]["content"].strip()
            logger.info(f"    VISION {path.name}: {len(a['description'])} chars")
        except Exception as e:
            logger.error(f"    VISION FAILED {path.name}: {type(e).__name__}: {e}")
            a["description"] = f"Document '{a['caption_canonical']}' (page {a['page']})."


# ─────────────────────────── DeepSeek ───────────────────────────

PHYS_RULES = r"""RÈGLES CRITIQUES POUR PHYSIQUE-CHIMIE BAC MAROCAIN (2BAC PC/SM):

1. STRUCTURE DE L'EXAMEN (total = 20 points, 3h):
   - L'examen comporte TYPIQUEMENT 5 exercices (parfois 3-4):
     * 1 exercice de CHIMIE (~7 pts) — souvent en 2 parties (dosage, cinétique, pile, pH…)
     * Plusieurs exercices de PHYSIQUE:
       – Ondes (mécaniques, lumineuses, radioactivité)
       – Électricité (RC, RL, RLC, oscillations)
       – Mécanique (chute, translation, rotation, pendule, satellites)
       – Parfois Nucléaire (désintégration radioactive)

2. LATEX OBLIGATOIRE:
   - Toutes les formules en LaTeX inline $...$ ou display $$...$$.
   - Vecteurs: $\vec{F}$, $\overrightarrow{AB}$, $\vec{v}_G$.
   - Unités en \mathrm: $\mathrm{mol \cdot L^{-1}}$, $\mathrm{m \cdot s^{-1}}$, $\mathrm{J \cdot kg^{-1}}$, $\Omega$, $\mu\mathrm{F}$, $\mathrm{mH}$, $\mathrm{Bq}$.
   - Formules chimiques: $\mathrm{C_6H_8O_6}$, $\mathrm{AH_{(aq)}}$, $\mathrm{A^-_{(aq)}}$, $\mathrm{H_3O^+}$, $\mathrm{OH^-}$.
   - Constantes: $K_e = 10^{-14}$, $K_a$, $pK_a$, $\lambda$ (longueur d'onde ou désintégration), $\tau$ (temps caractéristique).
   - Dérivées: $\dfrac{\mathrm{d}i}{\mathrm{d}t}$, $\dfrac{\mathrm{d}q}{\mathrm{d}t}$, $\dfrac{\mathrm{d}u_C}{\mathrm{d}t}$.
   - Puissances de 10: $3{,}0 \times 10^{-5}$, $2{,}5 \cdot 10^8\,\mathrm{m/s}$.
   - Fractions: TOUJOURS $\dfrac{a}{b}$.
   - Équations différentielles: $\dfrac{\mathrm{d}i}{\mathrm{d}t} + \dfrac{R}{L} i = \dfrac{E}{L}$.
   - Équations chimiques: $\mathrm{AH_{(aq)} + H_2O_{(l)} \rightleftharpoons A^-_{(aq)} + H_3O^+_{(aq)}}$.

3. DISTINCTION SUJET vs CORRECTION:
   - `content` = la QUESTION du sujet. JAMAIS la réponse.
   - `correction.content` = démonstration/calculs officiels avec résultat encadré \boxed{...}.

4. SOUS-QUESTIONS: « 1- », « 1.1 », « 1.a », « 2-a » → questions séparées avec `number` = "1.1", "1.a", "1.b"…

5. POINTS:
   - Points entre parenthèses dans le sujet (0,5pt), (0,75pt), (1pt) → reporter EXACTEMENT.
   - Somme des points des questions = points de l'exercice.
   - Somme des points des exercices = 20.

6. DOCUMENTS (figures/schémas):
   - Chaque question peut référencer un ou plusieurs docs via `"documents": ["doc_eN_M"]`.
   - Ne mentionne un doc que si la question y fait VRAIMENT appel (cherche "figure 1", "ci-contre", "diagramme", "montage"…).

7. TYPE: pour la physique-chimie, utilise quasi toujours `"type": "open"`.
   Les rares VRAI/FAUX → `"type": "vrai_faux"` avec sub_questions.

8. CONTEXT de l'exercice (clé `context`):
   - Introduction thématique commune, énoncé des données, définition des symboles.
   - Utilise le LaTeX pour les valeurs numériques et unités.
"""


def _clean(text: str, limit: int = 30000) -> str:
    return re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f]", "", text)[:limit]


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


_PROVIDER_STATE = {"current": LLM_PROVIDER}


async def _call_llm_once(client: httpx.AsyncClient, provider: str, prompt: str, max_tokens: int) -> tuple[str, str]:
    """Call the requested provider once. Returns (content, finish_reason)."""
    system_msg = (
        "Expert en structuration d'examens de Physique-Chimie du BAC marocain. "
        "Tu DOIS préserver LaTeX ($...$ et $$...$$) dans toutes les formules physiques et chimiques. "
        "Tu réponds UNIQUEMENT avec un objet JSON valide."
    )
    messages = [{"role": "system", "content": system_msg}, {"role": "user", "content": prompt}]
    if provider == "mistral":
        url = MISTRAL_CHAT_URL
        headers = {"Authorization": f"Bearer {MISTRAL_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": MISTRAL_CHAT_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
    else:
        url = DEEPSEEK_URL
        headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}", "Content-Type": "application/json"}
        payload = {
            "model": DEEPSEEK_MODEL,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.1,
            "response_format": {"type": "json_object"},
        }
    r = await client.post(url, headers=headers, json=payload, timeout=300.0)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"], data["choices"][0].get("finish_reason", "")


async def call_deepseek(client: httpx.AsyncClient, prompt: str, label: str, max_tokens: int = 8000) -> dict:
    """LLM call with provider fallback. Name kept for backward compat."""
    last_exc = None
    providers_to_try = [_PROVIDER_STATE["current"]]
    if _PROVIDER_STATE["current"] == "deepseek":
        providers_to_try.append("mistral")  # auto-fallback

    for provider in providers_to_try:
        for attempt in range(1, 4):
            try:
                content, finish = await _call_llm_once(client, provider, prompt, max_tokens)
                logger.info(f"    [{label}/{provider}] {len(content)} chars, finish={finish}")
                return _parse_json_safe(content)
            except httpx.HTTPStatusError as e:
                # On 402 (payment required) or 401, switch provider immediately
                if e.response is not None and e.response.status_code in (401, 402, 403):
                    logger.warning(f"    [{label}/{provider}] {e.response.status_code} → switching provider")
                    if provider == "deepseek" and _PROVIDER_STATE["current"] == "deepseek":
                        _PROVIDER_STATE["current"] = "mistral"
                    last_exc = e
                    break  # break retry loop, try next provider
                last_exc = e
                wait = 2 ** attempt
                logger.warning(f"    [{label}/{provider}] HTTP {e.response.status_code if e.response else '?'}, retry {attempt}/3 in {wait}s…")
                await asyncio.sleep(wait)
            except Exception as e:
                last_exc = e
                wait = 2 ** attempt
                logger.warning(f"    [{label}/{provider}] error ({type(e).__name__}: {e}), retry {attempt}/3 in {wait}s…")
                await asyncio.sleep(wait)
    raise last_exc if last_exc else RuntimeError(f"{label}: all retries failed")


async def list_exercises(client: httpx.AsyncClient, sujet_text: str) -> list[dict]:
    sujet = _clean(sujet_text, 22000)
    prompt = f"""Identifie la LISTE DES EXERCICES de cet examen BAC marocain de Physique-Chimie (2BAC PC/SM).

SUJET OCR:
{sujet}

Typiquement 3 à 5 exercices : 1 de chimie (~7pts) + 2 à 4 de physique (ondes, électricité, mécanique, nucléaire).

Réponds UNIQUEMENT avec ce JSON:
{{
  "exercises": [
    {{
      "key": "ex1",
      "name": "Exercice 1 — Chimie : <sujet court>",
      "points": <nombre>,
      "topic": "Chimie" | "Ondes" | "Électricité" | "Mécanique" | "Nucléaire" | "Physique",
      "page_start": <numéro de page OCR où commence l'exercice>,
      "page_end": <numéro de page OCR où finit l'exercice>
    }},
    …
  ]
}}

La somme des `points` doit valoir EXACTEMENT 20. Respecte les valeurs annoncées dans l'entête du sujet (ex : « Exercice 1 : (7 points) »).
"""
    result = await call_deepseek(client, prompt, "LIST_EX", max_tokens=1500)
    return result.get("exercises", [])


def _filter_docs_for_exercise(ex_info: dict, assets: list[dict]) -> list[dict]:
    """Select docs whose page falls in [page_start, page_end] of the exercise."""
    ps = ex_info.get("page_start") or 0
    pe = ex_info.get("page_end") or 99
    docs = [a for a in assets if ps <= a["page"] <= pe]
    # Ensure docs are sorted and unique
    return docs


async def build_exercise(
    client: httpx.AsyncClient,
    ex_info: dict,
    sujet_text: str,
    correction_text: str,
    exercise_assets: list[dict],
) -> dict:
    sujet = _clean(sujet_text, 30000)
    correction = _clean(correction_text, 28000)

    key = ex_info.get("key", "ex1")
    name = ex_info.get("name", "Exercice")
    points = ex_info.get("points", 0)
    topic = ex_info.get("topic", "")

    # Map each asset to a per-exercise doc id
    docs_lines = []
    doc_map: list[dict] = []
    for i, a in enumerate(exercise_assets, 1):
        doc_id = f"doc_{key}_{i}"
        doc_map.append({
            "id": doc_id,
            "type": "figure",
            "title": a["caption_canonical"],
            "description": a.get("description", ""),
            "src": a["src"],
            "page": a["page"],
            "caption_key": a["caption_key"],
        })
        docs_lines.append(
            f'  {doc_id}: légende="{a["caption_canonical"]}" | page_sujet={a["page"]} | '
            f'fichier="{a["src"]}" | description="{a.get("description", "")[:200]}"'
        )
    docs_block = "\n".join(docs_lines) if docs_lines else "  (aucun document visuel pour cet exercice)"

    prompt = f"""Structure UNIQUEMENT l'exercice « {name} » ({points} points, thème: {topic}) de cet examen de Physique-Chimie BAC marocain.

SUJET OCR (extrait complet):
{sujet}

CORRECTION OCR (extrait complet):
{correction}

DOCUMENTS DISPONIBLES POUR CET EXERCICE (tu peux les référencer via leur id):
{docs_block}

{PHYS_RULES}

PRÉFIXE des IDs de question: utilise `{key}_qN` (ex: {key}_q1, {key}_q1a, {key}_q2…).

Chaque question qui s'appuie sur une figure DOIT inclure `"documents": ["doc_{key}_X", …]`.

Réponds avec UN SEUL objet JSON (sans autre clé de premier niveau):
{{
  "name": "{name}",
  "points": {points},
  "context": "<énoncé de mise en contexte de l'exercice, en LaTeX>",
  "questions": [
    {{
      "id": "{key}_q1",
      "number": "1",
      "type": "open",
      "points": <nombre>,
      "content": "<question en LaTeX>",
      "documents": ["doc_{key}_1"],
      "correction": {{ "content": "<correction détaillée en LaTeX>" }}
    }}
  ]
}}

IMPORTANT:
- La somme des `points` des questions DOIT valoir {points}.
- N'invente AUCUN document; utilise uniquement ceux listés ci-dessus.
- Si un exercice est en plusieurs parties (Partie 1 / Partie 2), garde une liste PLATE de questions et utilise `number`="1.1", "1.2", "2.1"… pour signaler la partie.
"""
    result = await call_deepseek(client, prompt, f"EX[{key}]", max_tokens=8000)
    # Attach doc definitions to the exercise (keep only the ids referenced by questions)
    referenced: set[str] = set()
    for q in result.get("questions", []) or []:
        for did in q.get("documents", []) or []:
            referenced.add(did)
    docs_final = [
        {k: v for k, v in d.items() if k not in ("page", "caption_key")}
        for d in doc_map if d["id"] in referenced
    ]
    if docs_final:
        result["documents"] = docs_final
    return result


# ─────────────────────────── Main structuring ───────────────────────────

async def structure_physique_exam(
    client: httpx.AsyncClient,
    extraction: dict,
    assets: list[dict],
    meta: dict,
) -> dict:
    sujet_text = extraction.get("sujet_text", "")
    correction_text = extraction.get("correction_text", "")

    # Step 1: vision descriptions (parallel)
    logger.info(f"  Step 1/3: describing {len(assets)} assets with Mistral Vision…")
    await asyncio.gather(*(describe_asset(client, a) for a in assets))

    # Step 2: list exercises
    logger.info("  Step 2/3: listing exercises…")
    ex_list = await list_exercises(client, sujet_text)
    if not ex_list:
        logger.error("  Aucun exercice détecté")
        return {"title": meta["title"], "parts": []}
    logger.info(f"    → {len(ex_list)} exercices: {[e.get('key') for e in ex_list]}")

    # Step 3: build each exercise in parallel
    logger.info(f"  Step 3/3: building {len(ex_list)} exercises in parallel…")
    tasks = []
    for ex in ex_list:
        ex_docs = _filter_docs_for_exercise(ex, assets)
        tasks.append(build_exercise(client, ex, sujet_text, correction_text, ex_docs))
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

    return {
        "title": meta["title"],
        "subject": "Physique-Chimie",
        "subject_full": meta["title"],
        "year": meta["year"],
        "session": meta["session"],
        "duration_minutes": 180,
        "coefficient": 7,
        "total_points": 20,
        "note": "L'usage de la calculatrice scientifique non programmable est autorisé. Les expressions littérales doivent être établies avant les applications numériques. Les exercices peuvent être traités dans l'ordre choisi par le candidat.",
        "parts": [
            {
                "name": "Examen",
                "points": 20,
                "exercises": exercises,
            }
        ],
    }


def _verify_points(exam_json: dict) -> tuple[bool, str]:
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


async def process_exam(exam_dir: Path, force: bool = False) -> bool:
    extraction_file = exam_dir / "extraction.json"
    exam_file = exam_dir / "exam.json"

    if not extraction_file.exists():
        logger.warning(f"[SKIP] {exam_dir.name}: extraction.json manquant (lancer batch_ocr.py)")
        return False
    if exam_file.exists() and not force:
        logger.info(f"[SKIP] {exam_dir.name}: exam.json existe déjà (--force pour re-générer)")
        return False

    logger.info(f"[GO] {exam_dir.name}")
    extraction = json.loads(extraction_file.read_text(encoding="utf-8"))

    assets = scan_assets(exam_dir)
    logger.info(f"  {len(assets)} assets détectés: {[a['file'] for a in assets]}")

    meta = {
        "title": extraction.get("title", f"Physique-Chimie {extraction.get('year')} {extraction.get('session')}"),
        "year": extraction.get("year"),
        "session": extraction.get("session"),
    }

    async with httpx.AsyncClient() as client:
        exam_json = await structure_physique_exam(client, extraction, assets, meta)

    ok, details = _verify_points(exam_json)
    logger.info(f"  Vérification:\n{details}")
    if not ok:
        logger.warning(f"  [WARN] Total ≠ 20 pour {exam_dir.name}. JSON écrit tout de même.")

    exam_file.write_text(json.dumps(exam_json, ensure_ascii=False, indent=2), encoding="utf-8")
    logger.info(f"  [OK] exam.json écrit ({exam_file.stat().st_size} bytes)")
    return True


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="'physique' ou 'physique/2024-normale'")
    parser.add_argument("--force", action="store_true")
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
