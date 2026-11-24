"""Le lien libre /2bacpcf : une seule fiche par élève, deux examens suivis séparément, le bilan que lit l'admin."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints import public_2bacpcf as b2
from app.api.v1.endpoints import public_tronc_commun as tc


@pytest.fixture()
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(b2, "DOSSIER", tmp_path)
    monkeypatch.setattr(b2, "ELEVES", tmp_path / "eleves.jsonl")
    monkeypatch.setattr(b2, "SUIVI", tmp_path / "suivi.jsonl")
    tc._appels.clear()
    app = FastAPI()
    app.include_router(b2.router)
    return TestClient(app)


FICHE = {"nom": "El Amrani", "prenom": "Yassine", "classe": "3", "pere": "Karim El Amrani", "telephone": "0661234567"}
U = "/public/2bacpcf"


def test_fiche_unique_et_classe(client):
    a = client.post(f"{U}/inscription", json=FICHE).json()
    b = client.post(f"{U}/inscription", json={**FICHE, "nom": "el  amrani", "classe": "2bac pc 3"}).json()
    assert a["eleve_id"] == b["eleve_id"] and b["deja"] is True
    assert a["classe"] == "2BACPCF 3"
    assert b2.classe_normale("2BAC PC F-12") == "2BACPCF 12" and b2.classe_normale("prof") == "prof"


def test_deux_examens_separes_une_reponse(client):
    H = {"X-Eleve": client.post(f"{U}/inscription", json=FICHE).json()["eleve_id"]}
    for cours in ("examen_physique", "examen_chimie"):
        assert client.post(f"{U}/suivi", headers=H, json={"type": "examen_debut", "cours": cours}).json()["deja"] is False
    q = {"type": "examen_question", "cours": "examen_physique", "question_id": "1-1", "note": 2, "sur": 3.25, "pertes": ["Unité"]}
    assert client.post(f"{U}/suivi", headers=H, json=q).json()["deja"] is False
    assert client.post(f"{U}/suivi", headers=H, json={**q, "note": 3.25}).json()["deja"] is True
    # la même question de l'autre examen compte à part
    assert client.post(f"{U}/suivi", headers=H, json={**q, "cours": "examen_chimie"}).json()["deja"] is False
    assert client.post(f"{U}/suivi", headers=H, json={"type": "examen_debut", "cours": "examen"}).status_code in (404, 422)
    phy = client.get(f"{U}/examen?cours=examen_physique", headers=H).json()
    assert phy["debut"] and phy["ouvert"] and list(phy["questions"]) == ["1-1"]
    client.post(f"{U}/suivi", headers=H, json={"type": "diapo", "cours": "phys_ch4_radioactivite", "slide_id": "x"})
    client.post(f"{U}/suivi", headers=H, json={"type": "temps", "cours": "rev_chim_deux_sens_equilibre", "secondes": 30})
    assert client.post(f"{U}/suivi", headers=H, json={"type": "temps", "cours": "tc_svt_revision", "secondes": 30}).status_code == 404
    b = b2.bilan()[0]
    assert b["examens"]["examen_physique"]["note"] == 2 and b["examens"]["examen_chimie"]["faites"] == 1
    assert b["progression"]["phys_ch4_radioactivite"] == {"vues": 1, "total": 87}
    assert b["temps"]["rev_chim_deux_sens_equilibre"] == 30
    assert any("Physique Q1-1 : Unité" == l for l in b["lacunes"])
    assert b["test"] is False


def test_suivi_sans_fiche_refuse(client):
    assert client.post(f"{U}/suivi", json={"type": "temps", "cours": "phys_ch3_ondes_lumineuses", "secondes": 30}).status_code == 401


def test_reprise_du_cours(client):
    H = {"X-Eleve": client.post(f"{U}/inscription", json=FICHE).json()["eleve_id"]}
    assert client.get(f"{U}/reprise", headers=H).json() == {"cours": {}}
    for k, sid in enumerate(["a", "b", "c", "b"], 1):
        client.post(f"{U}/suivi", headers=H, json={"type": "diapo", "cours": "phys_ch4_radioactivite", "slide_id": sid, "position": k, "total": 87})
    r = client.get(f"{U}/reprise", headers=H).json()["cours"]["phys_ch4_radioactivite"]
    assert r["derniere"] == "b" and r["vues"] == ["a", "b", "c"] and r["total"] == 87
    assert client.get(f"{U}/reprise").status_code == 401
