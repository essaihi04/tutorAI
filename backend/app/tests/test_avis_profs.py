"""Relecture des cours par les profs sur le lien libre : vote et commentaire par diapositive, lus par l'admin."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints import public_cours

H = {"X-Visiteur": "prof1234-abcd"}


@pytest.fixture()
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(public_cours, "FICHIER_AVIS", tmp_path / "avis.jsonl")
    public_cours._appels.clear()
    app = FastAPI()
    app.include_router(public_cours.router)
    return TestClient(app)


def test_les_cours_refaits_sont_publics():
    ids = public_cours.cours_publics()
    assert "phys_ch1_waves_exemple" in ids and "phys_ch2_ondes_periodiques" in ids
    assert not any(i.endswith("_course_v1") for i in ids)


def test_avis_puis_relu_le_dernier_gagne(client):
    url = "/public/cours-ondes/avis"
    base = {"deck_id": "phys_ch2_ondes_periodiques", "slide_id": "op_a1", "slide_titre": "Période", "position": 3}
    assert client.post(url, json={**base, "vote": "mauvais", "commentaire": "T mal dit", "relecteur": "M. Alami"}, headers=H).status_code == 200
    assert client.post(url, json={**base, "vote": "bon", "commentaire": "corrigé, ok"}, headers=H).status_code == 200
    mes = client.get("/public/cours-ondes/avis/phys_ch2_ondes_periodiques", headers=H).json()["avis"]
    assert mes == {"op_a1": {"vote": "bon", "commentaire": "corrigé, ok"}}
    tous = public_cours.lire_avis()
    assert len(tous) == 1 and tous[0]["statut"] == "a_faire"
    public_cours.marquer_avis("prof1234-abcd", "phys_ch2_ondes_periodiques", "op_a1", "corrige")
    assert public_cours.lire_avis()[0]["statut"] == "corrige"


def test_avis_vide_ou_cours_inconnu_refuse(client):
    url = "/public/cours-ondes/avis"
    assert client.post(url, json={"deck_id": "phys_ch2_ondes_periodiques", "slide_id": "x"}, headers=H).status_code == 400
    assert client.post(url, json={"deck_id": "inconnu_xyz", "slide_id": "x", "vote": "bon"}, headers=H).status_code == 404
    assert client.post(url, json={"deck_id": "phys_ch2_ondes_periodiques", "slide_id": "x", "vote": "super"}, headers=H).status_code == 422
