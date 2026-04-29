"""
Concours service — orientation logic for post-BAC competitive exams.

Provides:
- Catalog loading (from data/concours/catalog.json)
- Projected BAC average computation (CC 25% + Régional 25% + National 50%)
- Chance estimation per school based on threshold ranges
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "concours"
CATALOG_PATH = DATA_DIR / "catalog.json"


def load_catalog() -> dict:
    """Load the concours catalog. Returns ``{}`` if missing."""
    if not CATALOG_PATH.exists():
        logger.warning("Concours catalog not found at %s", CATALOG_PATH)
        return {"year": 0, "concours": []}
    with open(CATALOG_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_catalog(data: dict) -> None:
    """Persist the catalog (admin edits)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def compute_admission_score(
    regional: Optional[float],
    national_estimated: Optional[float],
) -> Optional[float]:
    """Compute the **concours admission preselection score** (2025-2026 formula).

    Used by ENSA, ENSAM, ENCG/TAFEM, FMP, ENA and most concours communs
    administered via ``cursussup.gov.ma``:

        Note d'admission = 0.75 * Examen National + 0.25 * Examen Régional

    ⚠️ This is **NOT** the official BAC moyenne (which includes contrôle
    continu at 25 %). The contrôle continu is **NOT** used in concours
    preselection — only the national & regional exam grades count.

    All inputs are on a /20 scale. Returns ``None`` if data is missing.
    """
    if regional is None or national_estimated is None:
        return None
    return round(0.75 * national_estimated + 0.25 * regional, 2)


def compute_projected_bac_average(
    cc1: Optional[float] = None,
    cc2: Optional[float] = None,
    regional: Optional[float] = None,
    national_estimated: Optional[float] = None,
) -> Optional[float]:
    """Compute the **official BAC moyenne** (used on the diploma, NOT for
    concours preselection).

        Moyenne BAC = 0.25 * CC + 0.25 * Régional + 0.50 * National

    Kept for reference and for CPGE (whose selection partially relies on
    the official BAC moyenne via its N2 component).
    """
    cc_values = [v for v in (cc1, cc2) if v is not None]
    if not cc_values or regional is None or national_estimated is None:
        return None
    cc = sum(cc_values) / len(cc_values)
    return round(0.25 * cc + 0.25 * regional + 0.50 * national_estimated, 2)


# Backward-compat alias (older code may still call the previous name)
compute_projected_average = compute_projected_bac_average


def _chance_label(moyenne: float, threshold_min: float, threshold_strong: float) -> dict:
    """Return a chance dict for a single school given the projected average."""
    if moyenne >= threshold_strong:
        return {"level": "forte", "label": "Chance forte", "color": "green", "score": 90}
    if moyenne >= threshold_min:
        # Linear interpolation between min and strong
        ratio = (moyenne - threshold_min) / max(threshold_strong - threshold_min, 0.1)
        score = int(50 + 40 * ratio)
        return {"level": "moyenne", "label": "Chance moyenne", "color": "amber", "score": score}
    if moyenne >= threshold_min - 1.0:
        return {"level": "faible", "label": "Chance faible — à tenter", "color": "orange", "score": 30}
    return {"level": "tres_faible", "label": "Très peu probable", "color": "red", "score": 10}


def simulate(moyenne_bac: float) -> list[dict]:
    """Return a ranked list of all schools across all concours with chance levels.

    Sorted by chance score descending so the student sees their best fits first.
    """
    catalog = load_catalog()
    results: list[dict] = []
    for concours in catalog.get("concours", []):
        cid = concours.get("id", "")
        cname = concours.get("name", "")
        for school in concours.get("schools", []):
            tmin = school.get("threshold_min")
            tmax = school.get("threshold_strong")
            if tmin is None or tmax is None:
                continue
            chance = _chance_label(moyenne_bac, tmin, tmax)
            results.append({
                "concours_id": cid,
                "concours_name": cname,
                "school_name": school.get("name", ""),
                "city": school.get("city", ""),
                "threshold_min": tmin,
                "threshold_strong": tmax,
                "chance": chance,
            })
    results.sort(key=lambda r: r["chance"]["score"], reverse=True)
    return results
