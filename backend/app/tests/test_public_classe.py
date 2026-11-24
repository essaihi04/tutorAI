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


def inscrire(client, code, H, prenom, nom="Alaoui", classe=""):
    r = client.post(f"/public/classe/{code}/participant", json={"nom": nom, "prenom": prenom, "classe": classe}, headers=H)
    assert r.status_code == 200, r.text
    return r.json()["id"]


def telephone_prof(client, code, P):
    j = client.post(f"/public/classe/{code}/jeton-prof", headers=P).json()["jeton"]
    return {"X-Telephone": "tel-prof0000", "X-Prof-Tel": client.post(f"/public/classe/{code}/prof-telephone", json={"jeton": j}).json()["cle"]}


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
    # sans nom : refusé
    assert client.post(f"/public/classe/{code}/reponse", json=rep, headers=T1).status_code == 409
    inscrire(client, code, T1, "Salma")
    inscrire(client, code, T2, "Yassine")
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
    # « feuille d'un autre élève » (le prof photographie une copie) : un nouveau nom, une nouvelle réponse
    assert client.post(f"/public/classe/{code}/reponse", json={**rep, "nouvel_eleve": {"nom": "Bennani", "prenom": "Omar"}}, headers=T1).status_code == 403
    d = client.post(f"/public/classe/{code}/reponse", json={**rep, "nouvel_eleve": {"nom": "Bennani", "prenom": "Omar"}}, headers=telephone_prof(client, code, P)).json()
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
    inscrire(client, code, T1, "Salma")
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
    for t, n in ((T1, "A"), (T2, "B"), ({"X-Telephone": "tel-cccccccc"}, "C")):
        inscrire(client, code, t, n)
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


def test_participants_et_reponses_nominatives(client, monkeypatch):
    code, P = seance(client)
    client.post(f"/public/classe/{code}/question", json={"question": "1"}, headers=P)
    sa = inscrire(client, code, T1, "Salma", "El Idrissi", "TCSF 2")
    # un téléphone = un élève : redonner son nom le corrige, sans doublon
    assert inscrire(client, code, T1, "Salma", "El Idrissy") == sa
    ya = inscrire(client, code, T2, "Yassine", "Amrani")
    assert client.post(f"/public/classe/{code}/participant", json={"nom": "x" * 61, "prenom": "y"}, headers={"X-Telephone": "tel-dddddddd"}).status_code == 422
    rep = {"question": "1", "verdict": "partiel", "note": 1, "sur": 2, "pertes": ["d) : −0,5"]}
    client.post(f"/public/classe/{code}/reponse", json=rep, headers=T1)
    client.post(f"/public/classe/{code}/reponse", json={**rep, "verdict": "juste", "note": 2}, headers=T2)
    # un élève ne rend pas la feuille d'un autre
    assert client.post(f"/public/classe/{code}/reponse", json={**rep, "eleve": sa}, headers=T2).status_code == 403
    # le téléphone du prof rend la feuille de Salma : elle remplace celle de Salma
    TP = telephone_prof(client, code, P)
    r = client.post(f"/public/classe/{code}/reponse", json={**rep, "note": 1.5, "eleve": sa}, headers=TP).json()
    assert r["eleve"] == sa and r["remplace"] is True
    assert client.post(f"/public/classe/{code}/reponse", json={**rep, "eleve": "deadbeef"}, headers=TP).status_code == 404
    # un élève sans téléphone, ajouté par le prof (le même nom tapé deux fois = un seul élève)
    assert client.post(f"/public/classe/{code}/eleve", json={"nom": "Bennani", "prenom": "Omar"}, headers=T2).status_code == 403
    o1 = client.post(f"/public/classe/{code}/eleve", json={"nom": "Bennani", "prenom": "Omar", "classe": "TCSF 2"}, headers=TP).json()["id"]
    o2 = client.post(f"/public/classe/{code}/reponse", json={**rep, "nouvel_eleve": {"nom": "bennani", "prenom": "OMAR"}}, headers=TP).json()["eleve"]
    assert o1 == o2
    assert client.get(f"/public/classe/{code}", headers=TP).json()["prof"] is True
    # le téléphone : les noms, son élève, le mur sans noms
    t = client.get(f"/public/classe/{code}", headers=T1).json()
    assert t["moi"]["id"] == sa and {p["prenom"] for p in t["participants"]} == {"Salma", "Yassine", "Omar"}
    assert all("eleve" not in x for x in t["reponses"]) and "toutes" not in t
    # l'écran du prof : l'élève de chaque réponse, toutes les réponses, les questions posées
    client.post(f"/public/classe/{code}/question", json={"question": "2"}, headers=P)
    client.post(f"/public/classe/{code}/reponse", json={**rep, "question": "2"}, headers=T1)
    e = client.get(f"/public/classe/{code}", headers=P).json()
    assert e["posees"] == ["1", "2"]
    assert {(x["question"], x["eleve"], x["note"]) for x in e["toutes"]} == {("1", sa, 1.5), ("1", ya, 2), ("1", o1, 1), ("2", sa, 1)}
    # le prof retire un élève : ses réponses partent avec lui
    assert client.delete(f"/public/classe/{code}/participant/{o1}").status_code == 403
    assert client.delete(f"/public/classe/{code}/participant/{o1}", headers=P).status_code == 200
    assert len(client.get(f"/public/classe/{code}", headers=P).json()["toutes"]) == 3
    # nombre d'élèves borné
    monkeypatch.setattr(pc, "MAX_PARTICIPANTS", 2)
    assert client.post(f"/public/classe/{code}/participant", json={"nom": "N", "prenom": "P"}, headers={"X-Telephone": "tel-eeeeeeee"}).status_code == 507


def test_jeton_du_telephone_prof(client):
    code, P = seance(client)
    assert client.post(f"/public/classe/{code}/jeton-prof").status_code == 403
    j = client.post(f"/public/classe/{code}/jeton-prof", headers=P).json()["jeton"]
    faux = f"{(int(j) + 1) % 10000:04d}"
    assert client.post(f"/public/classe/{code}/prof-telephone", json={"jeton": faux}).status_code == 403
    assert client.post(f"/public/classe/{code}/prof-telephone", json={"jeton": j}).status_code == 200
    # une seule fois
    assert client.post(f"/public/classe/{code}/prof-telephone", json={"jeton": j}).status_code == 403
    # expiré
    j2 = client.post(f"/public/classe/{code}/jeton-prof", headers=P).json()["jeton"]
    s = pc.SEANCES[code]
    s.jeton = (j2, s.jeton[1] - pc.DUREE_JETON - 1)
    assert client.post(f"/public/classe/{code}/prof-telephone", json={"jeton": j2}).status_code == 403


def test_telephone_prof_sans_code(client):
    """« Je suis le professeur » sans code : l'écran du prof accepte d'un clic (24/11/2026)."""
    code, P = seance(client)
    T = {"X-Telephone": "tel-prof-direct1"}
    assert client.post(f"/public/classe/{code}/demande-prof", headers=T).json()["statut"] == "attente"
    assert client.get(f"/public/classe/{code}/demande-prof", headers=T).json()["statut"] == "attente"
    # seul l'écran du prof voit et décide
    assert "demandes_prof" not in client.get(f"/public/classe/{code}", headers=T).json()
    assert client.get(f"/public/classe/{code}", headers=P).json()["demandes_prof"] == ["tel-prof-direct1"]
    d = {"telephone": "tel-prof-direct1", "accepter": True}
    assert client.post(f"/public/classe/{code}/demande-prof/decision", json=d, headers=T).status_code == 403
    assert client.post(f"/public/classe/{code}/demande-prof/decision", json=d, headers=P).status_code == 200
    r = client.get(f"/public/classe/{code}/demande-prof", headers=T).json()
    assert r["statut"] == "accepte"
    assert client.get(f"/public/classe/{code}", headers=T | {"X-Prof-Tel": r["cle"]}).json()["prof"] is True
    # la clé ne se donne qu'une fois
    assert client.get(f"/public/classe/{code}/demande-prof", headers=T).json()["statut"] == "aucune"
    # refus
    E = {"X-Telephone": "tel-eleve-farceur"}
    client.post(f"/public/classe/{code}/demande-prof", headers=E)
    client.post(f"/public/classe/{code}/demande-prof/decision", json={"telephone": "tel-eleve-farceur", "accepter": False}, headers=P)
    assert client.get(f"/public/classe/{code}/demande-prof", headers=E).json()["statut"] == "refuse"
    assert client.get(f"/public/classe/{code}", headers=E).json()["prof"] is False
