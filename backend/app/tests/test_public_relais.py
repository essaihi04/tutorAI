"""Le relais PC ↔ téléphone : code court, vue du PC suivie par le téléphone, messages pris une fois, expiration, plafonds."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints import public_relais as pr


@pytest.fixture()
def client():
    pr.CANAUX.clear()
    pr._appels.clear()
    app = FastAPI()
    app.include_router(pr.router)
    return TestClient(app)


def canal(client):
    d = client.post("/public/relais").json()
    assert len(d["code"]) == 6 and all(c in pr.ALPHABET for c in d["code"])
    assert not set(d["code"]) & set("0O1I")
    return d["code"], {"X-Pc": d["cle_pc"]}


def test_parcours_pc_telephone(client):
    code, PC = canal(client)
    assert client.get(f"/public/relais/{code}/messages", headers=PC).json() == {"messages": [], "telephone": False}
    vue = {"courante": {"id": "1-5", "texte": "Compare les deux sols.", "genre": "texte"}, "questions": [{"id": "1-5"}, {"id": "1-6"}]}
    client.post(f"/public/relais/{code}/vue", json={"vue": vue}, headers=PC)
    # le code se tape en minuscules, avec un tiret : il est reconnu
    tel = client.get(f"/public/relais/{code[:3].lower()}-{code[3:].lower()}").json()
    assert tel["vue"] == vue
    assert client.get(f"/public/relais/{code}?v={tel['version']}").json() == {"version": tel["version"], "inchange": True}
    # le téléphone change de question, tape, puis rend
    client.post(f"/public/relais/{code}/message", json={"message": {"type": "aller", "question": "1-6"}})
    client.post(f"/public/relais/{code}/message", json={"message": {"type": "texte", "texte": "Le sol A"}})
    client.post(f"/public/relais/{code}/message", json={"message": {"type": "texte", "texte": "Le sol A est sableux"}})
    client.post(f"/public/relais/{code}/message", json={"message": {"type": "texte", "texte": "Le sol A est sableux.", "rendre": True}})
    m = client.get(f"/public/relais/{code}/messages", headers=PC).json()
    assert m["telephone"] is True
    # la rafale de frappe ne garde que le dernier texte
    assert [(x["type"], x.get("texte"), x.get("rendre")) for x in m["messages"]] == [
        ("aller", None, None), ("texte", "Le sol A est sableux", None), ("texte", "Le sol A est sableux.", True)]
    assert client.get(f"/public/relais/{code}/messages", headers=PC).json()["messages"] == []   # pris une fois
    # le PC suit : nouvelle vue, nouvelle version, même canal (pas de nouveau code)
    client.post(f"/public/relais/{code}/vue", json={"vue": {**vue, "courante": {"id": "1-6"}}}, headers=PC)
    assert client.get(f"/public/relais/{code}").json()["version"] == tel["version"] + 1


def test_pc_exige(client):
    code, PC = canal(client)
    assert client.get(f"/public/relais/{code}/messages").status_code == 403
    assert client.post(f"/public/relais/{code}/vue", json={"vue": {}}, headers={"X-Pc": "faux"}).status_code == 403
    assert client.delete(f"/public/relais/{code}").status_code == 403
    assert client.delete(f"/public/relais/{code}", headers=PC).status_code == 200
    assert client.get(f"/public/relais/{code}").status_code == 404


def test_tailles_bornees(client):
    code, PC = canal(client)
    assert client.post(f"/public/relais/{code}/vue", json={"vue": {"x": "a" * 41_000}}, headers=PC).status_code == 413
    assert client.post(f"/public/relais/{code}/message", json={"message": {"type": "texte", "texte": "a" * 6000}}).status_code == 413
    assert client.post(f"/public/relais/{code}/message", json={"message": {"type": "<script>"}}).status_code == 422
    for k in range(pr.MAX_EN_ATTENTE):
        assert client.post(f"/public/relais/{code}/message", json={"message": {"type": "aller", "question": str(k)}}).status_code == 200
    assert client.post(f"/public/relais/{code}/message", json={"message": {"type": "aller", "question": "x"}}).status_code == 429
    client.get(f"/public/relais/{code}/messages", headers=PC)
    assert client.post(f"/public/relais/{code}/message", json={"message": {"type": "aller", "question": "x"}}).status_code == 200


def test_expiration_et_activite(client):
    code, PC = canal(client)
    pr.CANAUX[code].actif -= pr.EXPIRATION - 60
    client.get(f"/public/relais/{code}/messages", headers=PC)          # l'activité prolonge le canal
    assert client.get(f"/public/relais/{code}").status_code == 200
    pr.CANAUX[code].actif -= pr.EXPIRATION + 1
    assert client.get(f"/public/relais/{code}").status_code == 404
    assert code not in pr.CANAUX


def test_plafonds(client, monkeypatch):
    monkeypatch.setitem(pr.LIMITES_IP, "ouvrir", (2, 3600))
    canal(client)
    canal(client)
    assert client.post("/public/relais").status_code == 429
    pr._appels.clear()
    monkeypatch.setattr(pr, "MAX_CANAUX", 2)
    assert client.post("/public/relais").status_code == 503
    monkeypatch.setitem(pr.LIMITES_IP, "inconnu", (2, 3600))
    assert client.get("/public/relais/ZZZZZZ").status_code == 404
    assert client.get("/public/relais/abc").status_code == 404
    assert client.get("/public/relais/ZZZZZY").status_code == 429
