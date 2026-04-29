"""
Concours API endpoints — catalog, simulator, admin updates.

Public endpoints (no auth):
- GET  /concours/catalog       — list of post-BAC concours communs
- POST /concours/simulate      — compute projected BAC average + ranked chances

Admin endpoints (admin token):
- PUT  /concours/catalog       — replace the catalog (annual updates)
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.services import concours_service

router = APIRouter(prefix="/concours", tags=["concours"])


# ─── Auth helper (reuse admin token check) ────────────────────────────

def _get_admin_dep():
    from app.api.v1.endpoints.admin import _verify_admin_token
    return _verify_admin_token


# ─── Models ────────────────────────────────────────────────────────────

class SimulateRequest(BaseModel):
    """Either pass a precomputed ``moyenne_bac`` OR the four components."""
    moyenne_bac: Optional[float] = Field(default=None, ge=0, le=20)
    cc1: Optional[float] = Field(default=None, ge=0, le=20, description="Moyenne contrôle continu 1ère bac")
    cc2: Optional[float] = Field(default=None, ge=0, le=20, description="Moyenne contrôle continu 2ème bac (en cours)")
    regional: Optional[float] = Field(default=None, ge=0, le=20, description="Note de l'examen régional (1ère bac)")
    national_estimated: Optional[float] = Field(default=None, ge=0, le=20, description="Note projetée à l'examen national")


class SimulateResponse(BaseModel):
    moyenne_bac_projetee: float
    components: dict
    results: list[dict]
    summary: dict


# ─── Endpoints ─────────────────────────────────────────────────────────

@router.get("/catalog")
async def get_catalog():
    """Return the full concours catalog (public, used by /orientation page)."""
    return concours_service.load_catalog()


@router.post("/simulate", response_model=SimulateResponse)
async def simulate(req: SimulateRequest):
    """Compute the projected BAC average and rank all schools by chance.

    Two usage modes:
    1. **Quick** — pass ``moyenne_bac`` directly (the student already has an estimate).
    2. **Detailed** — pass ``cc1, cc2, regional, national_estimated`` and we apply
       the official Moroccan formula (CC 25 % + Régional 25 % + National 50 %).
    """
    if req.moyenne_bac is not None:
        moyenne = round(req.moyenne_bac, 2)
        components = {"moyenne_bac": moyenne, "method": "direct"}
    else:
        moyenne = concours_service.compute_projected_average(
            cc1=req.cc1, cc2=req.cc2,
            regional=req.regional, national_estimated=req.national_estimated,
        )
        if moyenne is None:
            raise HTTPException(
                status_code=400,
                detail="Fournir soit moyenne_bac, soit (cc1 ou cc2) + regional + national_estimated.",
            )
        components = {
            "cc1": req.cc1, "cc2": req.cc2,
            "regional": req.regional, "national_estimated": req.national_estimated,
            "method": "formule_officielle",
        }

    results = concours_service.simulate(moyenne)
    by_level = {"forte": 0, "moyenne": 0, "faible": 0, "tres_faible": 0}
    for r in results:
        by_level[r["chance"]["level"]] += 1

    return SimulateResponse(
        moyenne_bac_projetee=moyenne,
        components=components,
        results=results,
        summary={
            "total_schools": len(results),
            "by_chance": by_level,
            "top_3": results[:3],
        },
    )


@router.put("/catalog")
async def update_catalog(
    body: dict,
    admin: bool = Depends(_get_admin_dep()),
):
    """Replace the catalog. Admin-only — used to update yearly thresholds."""
    if "concours" not in body or not isinstance(body["concours"], list):
        raise HTTPException(status_code=400, detail="Invalid catalog: missing 'concours' list")
    concours_service.save_catalog(body)
    return {"ok": True, "concours_count": len(body["concours"])}
