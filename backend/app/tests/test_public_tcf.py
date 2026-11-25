"""Le lien libre /TCF (Tronc Commun physique-chimie) : une seule fiche par élève, classe TCSF, cours et évaluations suivis."""
import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints import public_tcf as tcf
from app.api.v1.endpoints import public_tronc_commun as tc


@pytest.fixture()
def client(monkeypatch, tmp_path):
    monkeypatch.setattr(tcf, "DOSSIER", tmp_path)
    monkeypatch.setattr(tcf, "ELEVES", tmp_path / "eleves.jsonl")
    monkeypatch.setattr(tcf, "SUIVI", tmp_path / "suivi.jsonl")
    tc._appels.clear()
    app = FastAPI()
    app.include_router(tcf.router)
    return TestClient(app)


FICHE = {"nom": "Benali", "prenom": "Salma", "classe": "tcsf 4", "pere": "Ahmed Benali", "telephone": "0661234567"}
U = "/public/tcf"


def test_fiche_unique_et_classe(client):
    a = client.post(f"{U}/inscription", json=FICHE).json()
    b = client.post(f"{U}/inscription", json={**FICHE, "nom": "benali ", "classe": "4"}).json()
    assert a["eleve_id"] == b["eleve_id"] and b["deja"] is True
    assert a["classe"] == "TCSF 4" and tcf.classe_normale("prof") == "prof"


def test_cours_et_evaluations(client):
    H = {"X-Eleve": client.post(f"{U}/inscription", json=FICHE).json()["eleve_id"]}
    assert client.post(f"{U}/suivi", headers=H, json={"type": "diapo", "cours": "tc_chim_atome", "slide_id": "x"}).json()["ok"]
    assert client.post(f"{U}/suivi", headers=H, json={"type": "temps", "cours": "tc_phys_mouvement_inertie", "secondes": 30}).json()["ok"]
    # un cours d'un autre lien est refusé
    assert client.post(f"{U}/suivi", headers=H, json={"type": "temps", "cours": "tc_svt_revision", "secondes": 30}).status_code == 404
    q = {"type": "examen_question", "cours": "examen_tcf", "question_id": "1", "note": 2, "sur": 3, "pertes": ["Unité"]}
    assert client.post(f"{U}/suivi", headers=H, json=q).json()["deja"] is False
    assert client.post(f"{U}/suivi", headers=H, json=q).json()["deja"] is True
    b = tcf.bilan()[0]
    assert b["classe"] == "TCSF 4" and b["progression"]["tc_chim_atome"]["vues"] == 1
    assert b["temps"]["tc_phys_mouvement_inertie"] == 30 and b["examens"]["examen_tcf"]["note"] == 2


def test_suivi_sans_fiche_refuse(client):
    assert client.post(f"{U}/suivi", json={"type": "temps", "cours": "tc_chim_synthese", "secondes": 30}).status_code == 401


def test_refaire_l_examen_ecrase_l_ancienne_copie(client):
    """25/11/2026 : un examen terminé se refait ; seule la dernière tentative compte (page, admin, à retravailler)."""
    H = {"X-Eleve": client.post(f"{U}/inscription", json=FICHE).json()["eleve_id"]}
    q = {"type": "examen_question", "cours": "examen_tcf", "question_id": "1", "note": 1, "sur": 3, "pertes": ["Unité"]}
    client.post(f"{U}/suivi", headers=H, json=q)
    client.post(f"{U}/suivi", headers=H, json={"type": "examen_fin", "cours": "examen_tcf", "note": 1, "sur": 20})
    assert client.get(f"{U}/examen", headers=H).json()["fini"] is True
    assert client.post(f"{U}/suivi", headers=H, json={"type": "examen_reprise", "cours": "examen_tcf"}).json()["deja"] is False
    m = client.get(f"{U}/examen", headers=H).json()
    assert m["fini"] is False and m["questions"] == {} and m["debut"] is True
    # la même question se rend de nouveau, une seule fois dans cette tentative
    assert client.post(f"{U}/suivi", headers=H, json={**q, "note": 3, "pertes": []}).json()["deja"] is False
    assert client.post(f"{U}/suivi", headers=H, json={**q, "note": 0}).json()["deja"] is True
    client.post(f"{U}/suivi", headers=H, json={"type": "examen_fin", "cours": "examen_tcf", "note": 3, "sur": 20})
    x = tcf.bilan()[0]["examens"]["examen_tcf"]
    assert x["note"] == 3 and x["fini"] is True and x["tentative"] == 2 and x["questions"]["1"]["note"] == 3
    assert client.get(f"{U}/a-retravailler", headers=H).json()["questions"] == []
