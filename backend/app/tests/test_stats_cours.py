"""Statistiques de lecture d'un cours (services/stats_cours.py) : un cours lu plusieurs fois, temps, diapos vues."""
from datetime import datetime, timezone

from app.services import stats_cours

MAINTENANT = datetime(2026, 11, 21, 12, 0, tzinfo=timezone.utc)


def ev(type_, quand, **k):
    return {"type": type_, "deck_id": "d1", "quand": quand, **k}


def test_lu_deux_fois_temps_et_jours():
    evs = [
        ev("ouverture", "2026-11-20T10:00:00+00:00"),
        ev("temps", "2026-11-20T10:00:30+00:00", secondes=30, slide_id="s1"),
        ev("temps", "2026-11-20T10:01:00+00:00", secondes=90, slide_id="s2"),
        ev("terminaison", "2026-11-20T10:02:00+00:00"),
        ev("ouverture", "2026-11-21T09:00:00+00:00"),
        ev("temps", "2026-11-21T09:00:30+00:00", secondes=60, slide_id="s1"),
        ev("terminaison", "2026-11-21T09:05:00+00:00"),
    ]
    r = stats_cours.resumer(evs, MAINTENANT)["d1"]
    assert (r["ouvertures"], r["terminaisons"], r["minutes"]) == (2, 2, 3)
    assert r["diapos_vues"] == ["s1", "s2"]
    assert r["derniere"].startswith("2026-11-21")
    jours = {j["jour"]: j["minutes"] for j in r["jours"]}
    assert len(r["jours"]) == stats_cours.JOURS and jours["2026-11-20"] == 2.0 and jours["2026-11-21"] == 1.0


def test_competences_comptees():
    deck = {"competences": [{"id": "c1", "label": "Un"}, {"id": "c2", "label": "Deux"}, {"id": "c3", "label": "Trois"}],
            "activities": [{"id": "a", "slides": [{"id": "s1", "competence_ids": ["c1"]}, {"id": "s2", "competence_ids": ["c2"]}]}]}
    evs = [{"slide_id": "s1", "cle": "q", "correct": True, "tentative": 1},
           {"slide_id": "s2", "cle": "q", "correct": False, "tentative": 1},
           {"slide_id": "s2", "cle": "q", "correct": False, "tentative": 2}]
    c = stats_cours.competences(evs, deck)
    assert (c["total"], c["acquis"], c["non_acquis"], c["non_evalue"]) == (3, 1, 1, 1)
    assert next(x for x in c["liste"] if x["id"] == "c2")["reprendre_avec"]
