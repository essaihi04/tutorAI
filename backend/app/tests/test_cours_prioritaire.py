"""Un cours refait (`remplace_la_base`) passe avant le deck publié en base, pour SA leçon seulement (9 novembre 2026)."""
import asyncio

from app.services import course_player_service as cps

LECON_ONDES = "8804f569-4ef7-4d94-b197-d9c700d4e414"
LECON_PERIODIQUES = "a43b43b0-45a1-486a-b33a-e696a9659075"


class _BaseIndisponible:
    def table(self, *_):
        raise RuntimeError("pas de base dans les tests")


def test_la_lecon_des_ondes_recoit_le_cours_refait(monkeypatch):
    monkeypatch.setattr(cps, "get_supabase_admin", lambda: _BaseIndisponible())
    deck = asyncio.run(cps.CoursePlayerService().get_deck(LECON_ONDES))
    assert deck["stable_id"] == "phys_ch1_waves_exemple"
    assert deck["mode"] == "concentration"
    assert deck["lesson_id"] == LECON_ONDES
    # ce qui fait le mode concentration voyage avec le deck
    diapo = deck["activities"][1]["slides"][0]
    assert diapo["concentration"] and diapo["competence_ids"] and deck["competences"]


def test_le_cours_refait_ne_prend_pas_une_autre_lecon(monkeypatch):
    service = cps.CoursePlayerService()
    # « ondes mécaniques progressives » se lit aussi dans la leçon des ondes périodiques
    m = service._load_local_manifest("Laboratoire guidé — Ondes mécaniques progressives périodiques", "")
    assert m is None or m.get("stable_id") != "phys_ch1_waves_exemple"
    monkeypatch.setattr(cps, "get_supabase_admin", lambda: _BaseIndisponible())
    monkeypatch.setattr(service, "_titres_lecon", lambda _id: ("Laboratoire guidé — Ondes mécaniques progressives périodiques", ""))
    deck = asyncio.run(service.get_deck(LECON_PERIODIQUES))
    assert deck is None or deck.get("stable_id") != "phys_ch1_waves_exemple"


def test_sans_le_drapeau_la_base_reprend_la_main():
    assert cps._prioritaire({"remplace_la_base": True, "status": "published", "lecon_remplacee": "x"}) == "x"
    assert cps._prioritaire({"status": "published", "lecon_remplacee": "x"}) == ""
    assert cps._prioritaire({"remplace_la_base": True, "status": "draft", "lecon_remplacee": "x"}) == ""
