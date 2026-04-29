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
    """Inputs for the concours preselection simulator.

    Primary fields (used for **all** concours communs — formule 75/25):
      * ``regional``           — note de l'Examen Régional (1ère bac, déjà passé)
      * ``national_estimated`` — note projetée à l'Examen National

    Optional fields (used **only** for CPGE / Bac officiel):
      * ``cc1``, ``cc2`` — moyennes du contrôle continu (1ère + 2ème bac)
      * ``moyenne_bac``  — passe directement la moyenne du Bac si déjà connue
    """
    moyenne_bac: Optional[float] = Field(default=None, ge=0, le=20)
    cc1: Optional[float] = Field(default=None, ge=0, le=20, description="Moyenne contrôle continu 1ère bac (CPGE seulement)")
    cc2: Optional[float] = Field(default=None, ge=0, le=20, description="Moyenne contrôle continu 2ème bac (CPGE seulement)")
    regional: Optional[float] = Field(default=None, ge=0, le=20, description="Note de l'examen régional (1ère bac)")
    national_estimated: Optional[float] = Field(default=None, ge=0, le=20, description="Note projetée à l'examen national")


class SimulateResponse(BaseModel):
    note_admission: float = Field(description="Note de présélection concours (75% National + 25% Régional)")
    moyenne_bac_projetee: Optional[float] = Field(default=None, description="Moyenne officielle du Bac (CC inclus) si CC fourni")
    components: dict
    results: list[dict]
    summary: dict
    formula_explanation: str


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
    # 1. Note d'admission concours = 75% National + 25% Régional (formule officielle 2025-2026)
    note_admission = concours_service.compute_admission_score(
        regional=req.regional, national_estimated=req.national_estimated,
    )
    if note_admission is None:
        # Fallback: if user only passed moyenne_bac, use it as admission proxy
        if req.moyenne_bac is not None:
            note_admission = round(req.moyenne_bac, 2)
        else:
            raise HTTPException(
                status_code=400,
                detail="Fournir au minimum 'regional' + 'national_estimated', ou 'moyenne_bac'.",
            )

    # 2. Moyenne officielle du Bac (CC + Régional + National) — utile pour CPGE
    moyenne_bac = concours_service.compute_projected_bac_average(
        cc1=req.cc1, cc2=req.cc2,
        regional=req.regional, national_estimated=req.national_estimated,
    )

    components = {
        "regional": req.regional,
        "national_estimated": req.national_estimated,
        "cc1": req.cc1,
        "cc2": req.cc2,
        "moyenne_bac_directe": req.moyenne_bac,
    }

    # Use the admission score for chance simulation (concours communs use this)
    results = concours_service.simulate(note_admission)
    by_level = {"forte": 0, "moyenne": 0, "faible": 0, "tres_faible": 0}
    for r in results:
        by_level[r["chance"]["level"]] += 1

    return SimulateResponse(
        note_admission=note_admission,
        moyenne_bac_projetee=moyenne_bac,
        components=components,
        results=results,
        summary={
            "total_schools": len(results),
            "by_chance": by_level,
            "top_3": results[:3],
        },
        formula_explanation=(
            "Note de présélection des concours communs (ENSA, ENSAM, ENCG, FMP, ENA) = "
            "0.75 × Examen National + 0.25 × Examen Régional. "
            "Le contrôle continu n'est PAS pris en compte dans cette formule. "
            "Pour les CPGE, la sélection se fait sur dossier (notes des 2 ans + avis du conseil de classe)."
        ),
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
