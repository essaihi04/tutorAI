"""
Concours API endpoints — catalog, simulator, admin updates.

Public endpoints (no auth):
- GET  /concours/catalog       — catalog of post-BAC concours communs
- POST /concours/simulate      — compute admission score + eligibility per concours

Admin endpoints (admin token):
- PUT  /concours/catalog       — replace the catalog (annual updates)
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.services import concours_service

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
