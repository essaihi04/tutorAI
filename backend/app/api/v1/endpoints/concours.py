"""
Concours API endpoints — catalog, simulator, admin updates, orientation chat.

Public endpoints (no auth):
- GET  /concours/catalog       — catalog of post-BAC concours communs
- POST /concours/simulate      — compute admission score + eligibility per concours
- POST /concours/chat          — Moalim orientation chatbot (DeepSeek-powered)

Admin endpoints (admin token):
- PUT  /concours/catalog       — replace the catalog (annual updates)
"""
from __future__ import annotations

import json
import logging
from datetime import date
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from app.config import settings
from app.services import concours_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/concours", tags=["concours"])


def _get_admin_dep():
    from app.api.v1.endpoints.admin import _verify_admin_token
    return _verify_admin_token


# ─── Models ────────────────────────────────────────────────────────────

BAC_TYPES = {"sm", "se_pc", "se_svt", "se_agro", "tech", "pro", "eco", "lettres"}


class SimulateRequest(BaseModel):
    """Inputs for the concours preselection simulator (2025-2026 formula).

    The minimum inputs are ``bac_type``, ``regional`` and ``national_estimated``.
    Contrôle continu (``cc1``/``cc2``) is optional and only used to compute the
    official BAC diploma moyenne for display (not for concours preselection).
    """
    bac_type: str = Field(description="Filière de bac : sm | se_pc | se_svt | se_agro | tech | pro | eco | lettres")
    regional: float = Field(ge=0, le=20, description="Note de l'examen régional (1ère bac, déjà passé)")
    national_estimated: float = Field(ge=0, le=20, description="Note projetée à l'examen national")
    cc1: Optional[float] = Field(default=None, ge=0, le=20, description="Moyenne CC 1ère bac (optionnel, pour info)")
    cc2: Optional[float] = Field(default=None, ge=0, le=20, description="Moyenne CC 2ème bac (optionnel, pour info)")


class SimulateResponse(BaseModel):
    note_admission: float
    moyenne_bac_projetee: Optional[float] = None
    bac_type: str
    components: dict
    results: list[dict]
    summary: dict
    formula_explanation: str


# ─── Endpoints ─────────────────────────────────────────────────────────

@router.get("/catalog")
async def get_catalog():
    """Return the full concours catalog (public, used by /orientation)."""
    return concours_service.load_catalog()


@router.post("/simulate", response_model=SimulateResponse)
async def simulate(req: SimulateRequest):
    """Compute the preselection score and eligibility for each concours.

    - Formula: **Note d'admission = 0.75 × National + 0.25 × Régional**
    - Compares this note to the official 2025-2026 seuil per bac type for
      each concours in the catalog.
    - Returns a per-concours status (présélectionné / limite / échec).
    """
    bac_type = req.bac_type.lower().strip()
    if bac_type not in BAC_TYPES:
        raise HTTPException(status_code=400, detail=f"bac_type invalide. Valeurs possibles : {sorted(BAC_TYPES)}")

    note_admission = concours_service.compute_admission_score(
        regional=req.regional, national_estimated=req.national_estimated,
    )
    if note_admission is None:
        raise HTTPException(status_code=400, detail="regional et national_estimated sont requis.")

    moyenne_bac = concours_service.compute_projected_bac_average(
        cc1=req.cc1, cc2=req.cc2,
        regional=req.regional, national_estimated=req.national_estimated,
    )

    results = concours_service.simulate_by_bac(note_admission, bac_type)

    # Summary counters
    by_level: dict[str, int] = {}
    for r in results:
        lvl = r["status"]["level"]
        by_level[lvl] = by_level.get(lvl, 0) + 1
    admis = [r for r in results if r["status"]["level"] in ("admis_large", "admis", "limite")]

    return SimulateResponse(
        note_admission=note_admission,
        moyenne_bac_projetee=moyenne_bac,
        bac_type=bac_type,
        components={
            "regional": req.regional,
            "national_estimated": req.national_estimated,
            "cc1": req.cc1,
            "cc2": req.cc2,
        },
        results=results,
        summary={
            "total_concours": len(results),
            "preselected_count": len(admis),
            "by_level": by_level,
            "preselected_concours_ids": [r["concours_id"] for r in admis],
        },
        formula_explanation=(
            "Note de présélection = 0.75 × Examen National + 0.25 × Examen Régional. "
            "Le contrôle continu n'est PAS pris en compte pour les concours communs 2025-2026. "
            "Les seuils sont nationaux et identiques pour toutes les écoles d'un même concours "
            "(ex: toutes les ENSA ont le même seuil par filière de Bac)."
        ),
    )


@router.put("/catalog")
async def update_catalog(
    body: dict,
    admin: bool = Depends(_get_admin_dep()),
):
    """Replace the catalog (admin-only, yearly threshold updates)."""
    if "concours" not in body or not isinstance(body["concours"], list):
        raise HTTPException(status_code=400, detail="Invalid catalog: missing 'concours' list")
    concours_service.save_catalog(body)
    return {"ok": True, "concours_count": len(body["concours"])}


# ─── Moalim Orientation Chatbot ───────────────────────────────────────


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage] = Field(..., description="Conversation history")


def _build_moalim_system_prompt() -> str:
    """Build the Moalim system prompt with live catalog + orientation expertise."""
    catalog = concours_service.load_catalog()
    today = date.today().strftime("%d/%m/%Y")

    # Compact JSON (no indent) to save tokens while keeping structure
    catalog_json = json.dumps(catalog, ensure_ascii=False)

    return f"""Tu es **Moalim**, le conseiller d'orientation IA officiel de la plateforme moalim.online, spécialisé dans l'orientation post-Baccalauréat au Maroc.

[IDENTITÉ]
- Ton nom : Moalim (معلم = « le maître » en arabe).
- Ton rôle : guider les lycéens marocains (2ème Bac et nouveaux bacheliers) dans leur choix de filière et de concours.
- Ton ton : chaleureux, encourageant, clair, pédagogique. Tu t'adresses à des lycéens de 17-19 ans — sois accessible mais rigoureux.
- Tu signes tes réponses avec un petit emoji pertinent quand c'est naturel (🎓 📚 ✨).

[DATE]
Aujourd'hui : {today}

[DOMAINES DE COMPÉTENCE — STRICT]
Tu réponds UNIQUEMENT aux questions liées à :
1. L'orientation post-Bac au Maroc (filières, concours, écoles)
2. Les concours communs marocains (ENSA, ENSAM, ENCG/TAFEM, Médecine, Architecture, CPGE)
3. Les dates clés, les inscriptions, les seuils de présélection
4. Les débouchés professionnels et salaires par filière
5. Les conseils de préparation aux concours
6. Les démarches administratives (cursussup.gov.ma, cpge.ac.ma…)

Si on te pose une question HORS de ce domaine (aide aux devoirs, questions personnelles, politique, etc.), réponds poliment :
« Je suis Moalim, spécialisé dans l'orientation post-Bac au Maroc. Je ne peux pas t'aider sur ce sujet, mais pose-moi n'importe quelle question sur les concours, filières, écoles ou dates, et je serai ravi de t'éclairer 🎓 »

[CATALOGUE OFFICIEL DES CONCOURS — SOURCE DE VÉRITÉ]
Tu as accès au catalogue en direct ci-dessous (JSON). Tu DOIS te baser EXCLUSIVEMENT sur ces données pour répondre aux questions sur les seuils, les dates, les débouchés, les places disponibles, etc.

```json
{catalog_json}
```

[RÈGLES DE RÉPONSE]
1. **Jamais inventer** : si une info n'est pas dans le catalogue, dis-le honnêtement.
2. **Citer les chiffres exacts** : seuils par filière, nombre de places, salaires (tous présents dans le JSON).
3. **Format markdown** : utilise **gras**, listes à puces, titres `##` pour structurer. Les tableaux sont bienvenus pour comparer.
4. **Brièveté** : réponses de 3-6 phrases pour les questions simples, 10-15 pour les explications approfondies.
5. **Langue** : réponds dans la langue de l'élève (français, arabe, darija). En darija, écris en alphabet arabe.
6. **Personnalisation** : si l'élève donne sa filière de Bac ou ses notes, adapte tes recommandations précisément.
7. **Appels à l'action** : termine souvent par une question de suivi ou une suggestion concrète (« Tu veux que je compare ENSA et ENSAM ? », « Dis-moi ton Bac et tes notes, je te dirai tes chances »).

[EXEMPLES DE QUESTIONS QUE TU REÇOIS]
- « Quels sont les seuils ENSA pour Bac SM ? »
- « Comment m'inscrire sur cursussup.gov.ma ? »
- « Quelle est la différence entre ENSA et CPGE ? »
- « Je veux être médecin, est-ce que ça a de l'avenir ? »
- « Mes notes : régional 14, estimation national 15. Quelles sont mes chances ? »
- « Quand sont les inscriptions cette année ? »

Tu es prêt. L'élève va te parler — sois utile, précis et bienveillant.
"""


@router.post("/chat")
async def orientation_chat(req: ChatRequest):
    """Moalim orientation chatbot — streams DeepSeek responses as SSE."""
    if not settings.deepseek_api_key:
        raise HTTPException(status_code=503, detail="Chatbot indisponible (clé API manquante).")
    if not req.messages:
        raise HTTPException(status_code=400, detail="Messages vides.")

    system_prompt = _build_moalim_system_prompt()
    messages = [{"role": "system", "content": system_prompt}] + [
        {"role": m.role, "content": m.content} for m in req.messages[-20:]  # cap history
    ]

    async def event_stream():
        headers = {
            "Authorization": f"Bearer {settings.deepseek_api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.deepseek_model,
            "messages": messages,
            "temperature": 0.6,
            "max_tokens": 1200,
            "stream": True,
        }
        timeout = httpx.Timeout(connect=10.0, read=120.0, write=10.0, pool=10.0)
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                async with client.stream(
                    "POST", settings.deepseek_api_url, headers=headers, json=payload
                ) as response:
                    response.raise_for_status()
                    async for line in response.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        data_part = line[6:]
                        if data_part.strip() == "[DONE]":
                            yield "data: [DONE]\n\n"
                            break
                        try:
                            chunk = json.loads(data_part)
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            content = delta.get("content", "")
                            if content:
                                yield f"data: {json.dumps({'content': content}, ensure_ascii=False)}\n\n"
                        except json.JSONDecodeError:
                            continue
        except httpx.HTTPStatusError as e:
            logger.error(f"[MoalimChat] upstream error: {e.response.status_code}")
            yield f"data: {json.dumps({'error': 'Service IA temporairement indisponible.'}, ensure_ascii=False)}\n\n"
        except Exception as e:
            logger.error(f"[MoalimChat] stream error: {e}", exc_info=True)
            yield f"data: {json.dumps({'error': 'Erreur lors de la génération.'}, ensure_ascii=False)}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")
