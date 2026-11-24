"""Le mode classe : séance en mémoire, question projetée, réponses au mur (anonymes), plafonds — sans OCR ni LLM réels."""
import base64
import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints import public_classe as pc

JPEG = b"\xff\xd8\xff\xe0" + b"0" * 2000
IMG = "data:image/jpeg;base64," + base64.b64encode(JPEG).decode()
T1 = {"X-Telephone": "tel-aaaaaaaa"}
T2 = {"X-Telephone": "tel-bbbbbbbb"}


@pytest.fixture()
def client(monkeypatch):
    from app.services import llm_service as llm_mod, ocr_service

    async def chat(**kw):
        assert kw.get("student_id") is None          # pas de compte : rien au suivi des tokens
        return json.dumps({"correct": False, "partiel": True, "parole": "قريب.", "ecrit": "Il manque la justification.", "note": 0.5,
                           "details": [{"element": "Comparaison", "sur": 0.5, "obtenu": 0.5}, {"element": "Justification", "sur": 0.5, "obtenu": 0, "perte": "absente"}]})

    async def ocr(image_b64, mime_type="image/png", correct_math=True, subject="", contexte=""):
        assert "Tronc Commun" in contexte and "Question posée : Définis" in contexte
        return {"text": "Le point de flétrissement est le $%$ d'eau du sol"}

    monkeypatch.setattr(llm_mod.llm_service, "chat", chat)
    monkeypatch.setattr(ocr_service, "extract_text_from_image", ocr)
    pc.SEANCES.clear()
    pc._appels.clear()
    app = FastAPI()
    app.include_router(pc.router)
    return TestClient(app)


def seance(client):
    d = client.post("/public/classe").json()
    assert len(d["code"]) == 4 and d["code"].isdigit() and len(d["cle_prof"]) > 20
    return d["code"], {"X-Prof": d["cle_prof"]}


def test_creation_et_question(client):
    code, P = seance(client)
    e = client.get(f"/public/classe/{code}").json()
    assert e["question"] == "" and e["reponses"] == [] and e["correction"] is False
    assert client.post(f"/public/classe/{code}/question", json={"question": "1-5"}, headers=P).status_code == 200
    e2 = client.get(f"/public/classe/{code}").json()
    assert e2["question"] == "1-5" and e2["version"] > e["version"]
    # rien de neuf : réponse courte
    assert client.get(f"/public/classe/{code}?v={e2['version']}").json() == {"version": e2["version"], "inchange": True}
    client.post(f"/public/classe/{code}/correction", json={"montrer": True}, headers=P)
    assert client.get(f"/public/classe/{code}").json()["correction"] is True
    # changer de question cache la correction
    client.post(f"/public/classe/{code}/question", json={"question": "1-6"}, headers=P)
    assert client.get(f"/public/classe/{code}").json()["correction"] is False


def test_prof_exige(client):
    code, P = seance(client)
    assert client.post(f"/public/classe/{code}/question", json={"question": "1"}).status_code == 403
    assert client.post(f"/public/classe/{code}/question", json={"question": "1"}, headers={"X-Prof": "faux"}).status_code == 403
    assert client.post(f"/public/classe/{code}/correction", json={"montrer": True}).status_code == 403
    assert client.delete(f"/public/classe/{code}").status_code == 403
    assert client.delete(f"/public/classe/{code}", headers=P).status_code == 200
    assert client.get(f"/public/classe/{code}").status_code == 404


def test_reponse_au_mur_et_remplacement(client):
    code, P = seance(client)
    client.post(f"/public/classe/{code}/question", json={"question": "1-5"}, headers=P)
    rep = {"question": "1-5", "texte": "A plus perméable", "note": 0.5, "sur": 1, "verdict": "partiel",
           "pertes": ["Justification : absente"], "bien": ["Comparaison"], "retour": "Il manque…", "image_b64": IMG}
    a = client.post(f"/public/classe/{code}/reponse", json=rep, headers=T1).json()
    b = client.post(f"/public/classe/{code}/reponse", json={**rep, "texte": "autre", "image_b64": None}, headers=T2).json()
    assert (a["numero"], b["numero"]) == (1, 2)
    # le même téléphone remplace sa réponse (même numéro), sans empiler
    c = client.post(f"/public/classe/{code}/reponse", json={**rep, "texte": "corrigée", "note": 1, "verdict": "juste"}, headers=T1).json()
    assert c["remplace"] is True and c["numero"] == 1
    e = client.get(f"/public/classe/{code}", headers=T1).json()
    assert [(r["numero"], r["texte"], r["mien"]) for r in e["reponses"]] == [(1, "corrigée", True), (2, "autre", False)]
    assert e["par_question"] == {"1-5": 2}
    assert "telephone" not in e["reponses"][0]                     # rien qui identifie le téléphone
    img = client.get(f"/public/classe/{code}/image/{c['id']}")
    assert img.status_code == 200 and img.content == JPEG and img.headers["content-type"] == "image/jpeg"
    assert client.get(f"/public/classe/{code}/image/{a['id']}").status_code == 404   # l'ancienne est partie
    # « autre feuille » (le prof photographie plusieurs copies) : une nouvelle réponse
    d = client.post(f"/public/classe/{code}/reponse", json={**rep, "nouvelle": True}, headers=T1).json()
    assert d["numero"] == 3 and d["remplace"] is False
    # la réponse d'une autre question n'est pas au mur de la question projetée
    client.post(f"/public/classe/{code}/reponse", json={**rep, "question": "2-1"}, headers=T1)
    assert len(client.get(f"/public/classe/{code}").json()["reponses"]) == 3
    # le prof retire une réponse
    assert client.delete(f"/public/classe/{code}/reponse/{d['id']}").status_code == 403
    assert client.delete(f"/public/classe/{code}/reponse/{d['id']}", headers=P).status_code == 200
    assert len(client.get(f"/public/classe/{code}").json()["reponses"]) == 2


def test_reponse_bornee(client):
    code, _ = seance(client)
    rep = {"question": "1", "verdict": "juste", "note": 2, "sur": 2}
    assert client.post(f"/public/classe/{code}/reponse", json=rep).status_code == 400            # sans téléphone
    gros = "data:image/jpeg;base64," + base64.b64encode(b"\xff\xd8\xff" + b"0" * 160_000).decode()
    assert client.post(f"/public/classe/{code}/reponse", json={**rep, "image_b64": gros}, headers=T1).status_code == 422  # > 200 000 caractères
    moyen = base64.b64encode(b"\xff\xd8\xff" + b"0" * 125_000).decode()[:199_000]
    assert client.post(f"/public/classe/{code}/reponse", json={**rep, "image_b64": moyen}, headers=T1).status_code == 413
    html = base64.b64encode(b"<html><script>alert(1)</script>").decode()
    assert client.post(f"/public/classe/{code}/reponse", json={**rep, "image_b64": html}, headers=T1).status_code == 422
    assert client.post(f"/public/classe/{code}/reponse", json={**rep, "verdict": "bof"}, headers=T1).status_code == 422


def test_memoire_bornee_lache_les_vieilles_images(client, monkeypatch):
    monkeypatch.setattr(pc, "MAX_OCTETS_SEANCE", 5000)
    code, P = seance(client)
    rep = {"question": "1", "verdict": "juste", "note": 2, "sur": 2, "image_b64": IMG}
    client.post(f"/public/classe/{code}/question", json={"question": "1"}, headers=P)
    a = client.post(f"/public/classe/{code}/reponse", json=rep, headers=T1).json()
    client.post(f"/public/classe/{code}/reponse", json=rep, headers=T2).json()
    # question 1 projetée : une 3ᵉ image ne tient pas
    assert client.post(f"/public/classe/{code}/reponse", json=rep, headers={"X-Telephone": "tel-cccccccc"}).status_code == 507
    # question suivante : les images de la question 1 sont lâchées, leur texte reste
    client.post(f"/public/classe/{code}/question", json={"question": "2"}, headers=P)
    assert client.post(f"/public/classe/{code}/reponse", json={**rep, "question": "2"}, headers=T1).status_code == 200
    assert client.get(f"/public/classe/{code}/image/{a['id']}").status_code == 404
    client.post(f"/public/classe/{code}/question", json={"question": "1"}, headers=P)
    assert len(client.get(f"/public/classe/{code}").json()["reponses"]) == 2


def test_expiration(client, monkeypatch):
    code, _ = seance(client)
    pc.SEANCES[code].actif -= pc.EXPIRATION + 1
    assert client.get(f"/public/classe/{code}").status_code == 404
    assert code not in pc.SEANCES


def test_plafond_creations_et_seances(client, monkeypatch):
    monkeypatch.setitem(pc.LIMITES_IP, "creer", (3, 3600))
    for _ in range(3):
        assert client.post("/public/classe").status_code == 200
    assert client.post("/public/classe").status_code == 429
    pc._appels.clear()
    monkeypatch.setattr(pc, "MAX_SEANCES", 3)
    assert client.post("/public/classe").status_code == 503


def test_lire_et_corriger_plafonnes_par_seance(client, monkeypatch):
    code, _ = seance(client)
    lecture = {"image_b64": "aGVsbG8gd29ybGQ=", "question": "3-a", "enonce": "Définis le point de flétrissement."}
    r = client.post(f"/public/classe/{code}/lire", json=lecture)
    assert r.status_code == 200 and r.json()["texte"] == "Le point de flétrissement est le % d'eau du sol"
    corps = {"diapo": {"title": "P1", "speech": "…"}, "question": {"type": "open", "enonce": "Compare", "attendu": "…", "bareme": 1,
             "elements": ["Comparaison", "Justification"]}, "reponse": "A plus perméable", "tentative": 1}
    c = client.post(f"/public/classe/{code}/corriger", json=corps).json()
    assert c["partiel"] is True and c["note"] == 0.5
    monkeypatch.setitem(pc.LIMITES_SEANCE, "lire", (2, 3600))
    assert client.post(f"/public/classe/{code}/lire", json=lecture).status_code == 200
    assert client.post(f"/public/classe/{code}/lire", json=lecture).status_code == 429
    # une autre séance (même adresse : même wifi) n'est pas bloquée par la première
    code2, _ = seance(client)
    assert client.post(f"/public/classe/{code2}/lire", json=lecture).status_code == 200


def test_code_inconnu_plafonne(client, monkeypatch):
    monkeypatch.setitem(pc.LIMITES_IP, "inconnue", (3, 3600))
    for _ in range(3):
        assert client.get("/public/classe/0000").status_code == 404
    assert client.get("/public/classe/0001").status_code == 429
