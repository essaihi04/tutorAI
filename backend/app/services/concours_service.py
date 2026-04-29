"""
Concours service — orientation logic for post-BAC competitive exams.

Implements the **official 2025-2026 preselection formula** used by
``cursussup.gov.ma`` for concours communs (ENSA, ENSAM, ENCG, FMP, ENA):

    Note de présélection = 0.75 × Examen National + 0.25 × Examen Régional

The contrôle continu is **NOT** included in this formula (contrary to the
official BAC diploma moyenne, which is 0.25 CC + 0.25 R + 0.50 N).

Seuils are **national** per bac type, not per school. All schools in a
concours commun share the same preselection threshold (e.g., every ENSA
uses the same seuil for SM, SE-PC, SE-SVT, etc.).
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "concours"
CATALOG_PATH = DATA_DIR / "catalog.json"


# --------------------------------------------------------------------------- #
#  Catalog I/O
# --------------------------------------------------------------------------- #

def load_catalog() -> dict:
    """Load the concours catalog. Returns an empty stub if missing."""
    if not CATALOG_PATH.exists():
        logger.warning("Concours catalog not found at %s", CATALOG_PATH)
        return {"year": 0, "concours": []}
    with open(CATALOG_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def save_catalog(data: dict) -> None:
    """Persist the catalog (admin yearly updates)."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(CATALOG_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# --------------------------------------------------------------------------- #
#  Formulas
# --------------------------------------------------------------------------- #

def compute_admission_score(
    regional: Optional[float],
    national_estimated: Optional[float],
) -> Optional[float]:
    """Compute the concours preselection score (official 2025-2026 formula).

        Note d'admission = 0.75 × National + 0.25 × Régional
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
    """Compute the official BAC diploma moyenne (with contrôle continu).

        Moyenne BAC = 0.25 × CC + 0.25 × Régional + 0.50 × National

    Shown for reference only; NOT used for concours preselection.
    """
    cc_values = [v for v in (cc1, cc2) if v is not None]
    if not cc_values or regional is None or national_estimated is None:
        return None
    cc = sum(cc_values) / len(cc_values)
    return round(0.25 * cc + 0.25 * regional + 0.50 * national_estimated, 2)


# Backward-compat alias (do not remove — older callers may still import this)
compute_projected_average = compute_projected_bac_average


# --------------------------------------------------------------------------- #
#  Simulation — per concours, per bac type
# --------------------------------------------------------------------------- #

def _status_for_margin(note: float, seuil: float) -> dict:
    """Return a structured status dict based on the note/threshold gap."""
    margin = round(note - seuil, 2)
    if margin >= 2.0:
        return {
            "level": "admis_large",
            "label": "Présélectionné largement",
            "color": "emerald",
            "margin": margin,
            "score": 95,
        }
    if margin >= 0.5:
        return {
            "level": "admis",
            "label": "Présélectionné",
            "color": "green",
            "margin": margin,
            "score": 80,
        }
    if margin >= 0:
        return {
            "level": "limite",
            "label": "À la limite — présélectionné de justesse",
            "color": "amber",
            "margin": margin,
            "score": 60,
        }
    if margin >= -1.0:
        return {
            "level": "proche",
            "label": "Proche du seuil — à retenter",
            "color": "orange",
            "margin": margin,
            "score": 35,
        }
    return {
        "level": "echec",
        "label": "Non présélectionné",
        "color": "red",
        "margin": margin,
        "score": 10,
    }


def simulate_by_bac(note_admission: float, bac_type: str) -> list[dict]:
    """Return the preselection status of each concours for a given bac type.

    Sorted by score descending so the best matches appear first.
    """
    catalog = load_catalog()
    results: list[dict] = []
    for concours in catalog.get("concours", []):
        cid = concours.get("id", "")
        # Check if this bac type is eligible
        eligible = concours.get("eligible_bacs", [])
        if bac_type not in eligible:
            results.append({
                "concours_id": cid,
                "concours_name": concours.get("name", ""),
                "type": concours.get("type", ""),
                "tagline": concours.get("tagline", ""),
                "seuil": None,
                "status": {
                    "level": "non_eligible",
                    "label": f"Bac {bac_type.upper()} non éligible",
                    "color": "gray",
                    "margin": None,
                    "score": 0,
                },
                "schools_count": len(concours.get("schools", [])),
                "registration_site": concours.get("registration", {}).get("site", ""),
                "places_total": concours.get("places_total", 0),
            })
            continue

        # Get seuil for this bac type
        seuils = concours.get("seuils_preselection_2025", {})
        seuil = seuils.get(bac_type)

        if seuil is None:
            # Fallback: use the max of known seuils for this concours
            seuil_values = [v for v in seuils.values() if isinstance(v, (int, float))]
            seuil = max(seuil_values) if seuil_values else 15.0

        status = _status_for_margin(note_admission, seuil)

        results.append({
            "concours_id": cid,
            "concours_name": concours.get("name", ""),
            "type": concours.get("type", ""),
            "tagline": concours.get("tagline", ""),
            "seuil": seuil,
            "status": status,
            "schools_count": len(concours.get("schools", [])),
            "registration_site": concours.get("registration", {}).get("site", ""),
            "places_total": concours.get("places_total", 0),
        })

    results.sort(key=lambda r: r["status"]["score"], reverse=True)
    return results
