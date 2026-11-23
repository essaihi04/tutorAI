"""Le lien libre du Tronc Commun : une seule fiche par élève, son suivi, et le bilan que lit l'admin."""
import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints import public_tronc_commun as tc


@pytest.fixture()
def client(monkeypatch, tmp_path):
    from app.services import llm_service as llm_mod

    async def chat(**kw):
        assert kw.get("student_id") is None          # pas de compte : rien au suivi des tokens
        return json.dumps({"correct": True, "partiel": False, "parole": "مزيان.", "ecrit": "Juste."})

    monkeypatch.setattr(llm_mod.llm_service, "chat", chat)
    monkeypatch.setattr(tc, "DOSSIER", tmp_path)
    monkeypatch.setattr(tc, "ELEVES", tmp_path / "eleves.jsonl")
    monkeypatch.setattr(tc, "SUIVI", tmp_path / "suivi.jsonl")
    tc._appels.clear()
    app = FastAPI()
    app.include_router(tc.router)
    return TestClient(app)


FICHE = {"nom": "Salma El Idrissi", "classe": "TC2", "pere": "Ahmed El Idrissi", "telephone": "+212 6 12 34 56 78"}


def test_une_seule_fiche_par_eleve(client):
    a = client.post("/public/tronc-commun/inscription", json=FICHE).json()
    b = client.post("/public/tronc-commun/inscription", json={**FICHE, "nom": "salma  el-idrissi", "telephone": "0612345678"}).json()
    assert a["eleve_id"] == b["eleve_id"] and b["deja"] is True
    assert len(tc.lire_eleves()) == 1
    assert tc.lire_eleves()[a["eleve_id"]]["telephone"] == "0612345678"


def test_telephone_invalide(client):
    r = client.post("/public/tronc-commun/inscription", json={**FICHE, "telephone": "12345678"})
    assert r.status_code == 422


def test_suivi_sans_fiche_refuse(client):
    assert client.post("/public/tronc-commun/suivi", json={"type": "temps", "cours": "tc_svt_revision", "secondes": 30}).status_code == 401


def test_bilan_temps_examen_lacunes(client):
    eid = client.post("/public/tronc-commun/inscription", json=FICHE).json()["eleve_id"]
    H = {"X-Eleve": eid}
    for _ in range(3):
        assert client.post("/public/tronc-commun/suivi", headers=H, json={"type": "temps", "cours": "tc_svt_sortie_ecologique", "secondes": 30}).status_code == 200
    client.post("/public/tronc-commun/suivi", headers=H, json={"type": "diapo", "cours": "tc_svt_sortie_ecologique", "slide_id": "se_a1_outils", "total": 35})
    client.post("/public/tronc-commun/suivi", headers=H, json={"type": "reponse_cours", "cours": "tc_svt_sortie_ecologique", "slide_id": "s", "enonce": "F ?", "correct": False})
    client.post("/public/tronc-commun/suivi", headers=H, json={"type": "examen_debut", "cours": "examen"})
    client.post("/public/tronc-commun/suivi", headers=H, json={"type": "examen_question", "cours": "examen", "question_id": "1-1", "note": 0.75, "sur": 1, "pertes": ["Unité du résultat : unité manquante"]})
    client.post("/public/tronc-commun/suivi", headers=H, json={"type": "examen_fin", "cours": "examen", "note": 0.75, "sur": 20})
    assert client.post("/public/tronc-commun/suivi", headers=H, json={"type": "temps", "cours": "autre", "secondes": 30}).status_code == 404
    b = tc.bilan()[0]
    assert b["nom"] == "Salma El Idrissi" and b["pere"] == "Ahmed El Idrissi"
    assert b["temps"]["tc_svt_sortie_ecologique"] == 90
    assert b["progression"]["tc_svt_sortie_ecologique"] == {"vues": 1, "total": 35}
    assert b["reponses_cours"]["fausses"] == 1
    assert b["examens"][0]["note"] == 0.75 and "1-1" in b["examens"][0]["questions"]
    assert any("unité manquante" in l for l in b["lacunes"])


def test_correction_par_eleve(client):
    eid = client.post("/public/tronc-commun/inscription", json=FICHE).json()["eleve_id"]
    r = client.post("/public/tronc-commun/answer-reaction", headers={"X-Eleve": eid}, json={
        "diapo": {"title": "t", "speech": "s"}, "question": {"type": "open", "enonce": "Définis…", "attendu": "…", "matiere": "svt"},
        "reponse": "…", "tentative": 2})
    assert r.status_code == 200 and r.json()["correct"] is True
    assert client.post("/public/tronc-commun/answer-reaction", json={"reponse": "x"}).status_code == 401


def test_une_seule_reponse_par_question(client):
    eid = client.post("/public/tronc-commun/inscription", json={**FICHE, "nom": "El Idrissi", "prenom": "Salma"}).json()["eleve_id"]
    H = {"X-Eleve": eid}
    q = {"type": "examen_question", "cours": "examen", "question_id": "1-1", "note": 1, "sur": 1, "etat": {"fait": True, "note": 1, "verdict": "juste"}}
    assert client.post("/public/tronc-commun/suivi", headers=H, json=q).json()["deja"] is False
    r = client.post("/public/tronc-commun/suivi", headers=H, json={**q, "note": 0, "etat": {"fait": True, "note": 0}}).json()
    assert r["deja"] is True                      # la deuxième réponse n'est pas gardée
    d = client.get("/public/tronc-commun/examen", headers=H).json()
    assert d["questions"]["1-1"]["note"] == 1 and d["fini"] is False
    for _ in range(2):
        client.post("/public/tronc-commun/suivi", headers=H, json={"type": "examen_fin", "cours": "examen", "note": 1, "sur": 20})
    assert client.get("/public/tronc-commun/examen", headers=H).json()["fini"] is True
    assert len(tc.bilan()[0]["examens"]) == 1
    assert tc.lire_eleves()[eid]["prenom"] == "Salma" and tc.lire_eleves()[eid]["nom"] == "El Idrissi Salma"


def test_premiere_reponse_du_cours_seulement(client):
    eid = client.post("/public/tronc-commun/inscription", json=FICHE).json()["eleve_id"]
    H = {"X-Eleve": eid}
    r = {"type": "reponse_cours", "cours": "tc_svt_revision", "slide_id": "s1", "enonce": "Q ?", "correct": False}
    client.post("/public/tronc-commun/suivi", headers=H, json=r)
    client.post("/public/tronc-commun/suivi", headers=H, json={**r, "correct": True})
    assert tc.bilan()[0]["reponses_cours"] == {"total": 1, "justes": 0, "fausses": 1}


def test_classe_ouverture_tests_doublons(client):
    assert [tc.classe_normale(c) for c in ("Tc 12", "TCSF-12", "13", "prof")] == ["TCSF 12", "TCSF 12", "TCSF 13", "prof"]
    a = client.post("/public/tronc-commun/inscription", json={**FICHE, "classe": "12"}).json()["eleve_id"]
    client.post("/public/tronc-commun/inscription", json={**FICHE, "telephone": "0611111111"})          # même nom, autre téléphone
    client.post("/public/tronc-commun/inscription", json={**FICHE, "nom": "test", "classe": "prof", "telephone": "0622222222"})
    H = {"X-Eleve": a}
    assert client.get("/public/tronc-commun/examen", headers=H).json()["ouvert"] is False
    for k in range(12):
        client.post("/public/tronc-commun/suivi", headers=H, json={"type": "diapo", "cours": "tc_svt_revision", "slide_id": f"s{k}", "total": 15})
    assert client.get("/public/tronc-commun/examen", headers=H).json()["ouvert"] is True      # 12/15 = 80 %
    b = {e["id"]: e for e in tc.bilan()}
    assert b[a]["classe"] == "TCSF 12" and not b[a]["test"] and not b[a]["doublon_de"]
    assert sum(1 for e in b.values() if e["doublon_de"] == a) == 1
    assert sum(1 for e in b.values() if e["test"]) == 1
