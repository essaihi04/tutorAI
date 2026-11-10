"""La page publique du cours des ondes : sans compte, mais bornée (visiteur, cours, plafonds), micro par Gemini."""
import json

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.v1.endpoints import public_cours


@pytest.fixture()
def client(monkeypatch, tmp_path):
    from app.services import llm_service as llm_mod, suivi_acquis
    import app.services.stt_service as stt_mod

    async def chat(**kw):
        assert kw.get("student_id") is None          # un visiteur n'a pas de compte : rien au suivi des tokens
        return json.dumps({"parole": "مزيان، شوف la figure.", "ecrit": "τ = SM / v", "gestes": []})

    vu = {}

    async def transcrire(self, data, language="fr", gemini_seul=False):
        vu["gemini_seul"] = gemini_seul
        return "علاش tau"

    monkeypatch.setattr(llm_mod.llm_service, "chat", chat)
    monkeypatch.setattr(stt_mod.STTService, "transcribe_audio", transcrire)
    monkeypatch.setattr(suivi_acquis, "DOSSIER", tmp_path)
    public_cours._appels.clear()
    app = FastAPI()
    app.include_router(public_cours.router)
    c = TestClient(app)
    c.vu = vu
    return c


H = {"X-Visiteur": "abcdef12-3456"}


def test_sans_visiteur_refuse(client):
    assert client.post("/public/cours-ondes/question-eleve", json={"texte": "?"}).status_code == 400


def test_question_au_micro_passe_par_moulsot(client):
    r = client.post("/public/cours-ondes/question-eleve", headers=H,
                    json={"deck_id": "phys_ch1_waves_exemple", "title": "Retard", "audio_b64": "data:audio/webm;base64,AAAA"})
    assert r.status_code == 200, r.text
    assert client.vu["gemini_seul"] is False      # MoulSot v4 d'abord (kernel de la voix), Gemini en secours
    assert r.json()["question_comprise"] == "علاش tau"


def test_un_autre_cours_est_refuse(client):
    r = client.post("/public/cours-ondes/question-eleve", headers=H, json={"deck_id": "svt_ch1_energy", "texte": "?"})
    assert r.status_code == 404


def test_plafond_par_visiteur(client, monkeypatch):
    monkeypatch.setitem(public_cours.LIMITES, "llm", (2, 3600))
    corps = {"deck_id": "phys_ch1_waves_exemple", "texte": "pourquoi ?"}
    assert [client.post("/public/cours-ondes/question-eleve", headers=H, json=corps).status_code for _ in range(3)] == [200, 200, 429]


def test_suivi_des_acquis_du_visiteur(client):
    e = {"deck_id": "phys_ch1_waves_exemple", "slide_id": "wx_r1_retard", "cle": "q", "type": "qcm", "correct": False, "tentative": 1}
    assert client.post("/public/cours-ondes/acquis", headers=H, json=e).status_code == 200
    b = client.get("/public/cours-ondes/acquis/phys_ch1_waves_exemple", headers=H).json()
    assert any(c["id"] == "C4" and c["statut"] == "non_acquis" for c in b["competences"])


def test_micro_pas_encore_pret(client, monkeypatch):
    import app.services.stt_service as stt_mod

    async def rien(self, data, language="fr", gemini_seul=False):
        return None
    monkeypatch.setattr(stt_mod.STTService, "transcribe_audio", rien)
    from app.services import kaggle_tts
    reveils = []
    monkeypatch.setattr(kaggle_tts.pilote, "besoin_de_voix", lambda raison="parole": reveils.append(raison))   # pas de vrai GPU
    r = client.post("/public/cours-ondes/question-eleve", headers=H,
                    json={"deck_id": "phys_ch1_waves_exemple", "audio_b64": "data:audio/webm;base64,AAAA"})
    assert reveils == ["stt"]
    assert r.status_code == 409 and "micro se prépare" in r.json()["detail"]


def test_explication_d_une_notion_de_base(client):
    r = client.post("/public/cours-ondes/question-eleve/explication", headers=H,
                    json={"deck_id": "phys_ch1_waves_exemple", "question": "c'est quoi la vitesse ?", "notion": "vitesse moyenne"})
    assert r.status_code == 200, r.text
    assert r.json()["parole"] and "tableau" in r.json()
    assert client.post("/public/cours-ondes/question-eleve/explication", headers=H,
                       json={"deck_id": "svt_ch1", "notion": "x"}).status_code == 404


def test_question_classee_avec_le_plan_du_cours(client):
    r = client.post("/public/cours-ondes/question-eleve", headers=H,
                    json={"deck_id": "phys_ch1_waves_exemple", "slide_id": "wx_i1_corde", "texte": "comment ?"})
    assert r.status_code == 200 and r.json()["categorie"] == "diapo"


def test_transcription_seule_pour_verifier_avant_d_envoyer(client):
    r = client.post("/public/cours-ondes/transcrire", headers=H, json={"audio_b64": "data:audio/webm;base64,AAAAAAAA"})
    assert r.status_code == 200 and r.json() == {"texte": "علاش tau"}
    assert client.vu["gemini_seul"] is False


def test_photo_de_la_feuille_lue_avec_le_contexte_de_la_diapositive(client, monkeypatch):
    """« 📷 Photo » : Mistral OCR + DeepSeek avec le contexte ; le texte revient au champ (jamais envoyé seul)."""
    import app.services.ocr_service as ocr
    vu = {}

    async def lire(image_b64, mime_type="image/png", correct_math=True, subject="", contexte=""):
        vu.update(subject=subject, contexte=contexte, mime=mime_type)
        return {"text": "$\lambda$ = v·T = 0,40 m", "success": True}

    monkeypatch.setattr(ocr, "extract_text_from_image", lire)
    r = client.post("/public/cours-ondes/ocr-reponse", headers=H, json={
        "image_b64": "data:image/jpeg;base64,AAAA", "deck_id": "phys_ch1_waves_exemple", "title": "Le retard",
        "lead": "τ = d / v", "enonce": "Calcule λ."})
    assert r.status_code == 200, r.text
    assert r.json() == {"texte": "\lambda = v·T = 0,40 m"}            # jamais de $ dans le champ
    assert vu["subject"] == "physique" and "Le retard" in vu["contexte"] and "Calcule λ." in vu["contexte"]
    assert "ne corrige NI ses erreurs" in vu["contexte"]


def test_photo_illisible_dit_pourquoi(client, monkeypatch):
    import app.services.ocr_service as ocr

    async def rien(*a, **k):
        return {"text": "", "success": False}

    monkeypatch.setattr(ocr, "extract_text_from_image", rien)
    r = client.post("/public/cours-ondes/ocr-reponse", headers=H, json={"image_b64": "data:image/png;base64,AAAA"})
    assert r.status_code == 422 and "photo" in r.json()["detail"]
    assert client.post("/public/cours-ondes/ocr-reponse", headers=H,
                       json={"image_b64": "AAAAAAAAAAAA", "deck_id": "autre_cours"}).status_code == 404


def test_matiere_et_chapitre_deduits_du_cours():
    from app.api.v1.endpoints import course_player as cp
    assert cp.matiere_du_cours("chim_ch3_acides", None) == "chimie"
    assert cp.matiere_du_cours("x", {"subject": "Mathématiques"}) == "math"
    m, ctx = cp.contexte_ocr(cp.OcrReponseRequest(image_b64="AAAAAAAAAAAA", title="Diapo"), {"title": "Ondes périodiques"})
    assert m == "physique" and "Chapitre : Ondes périodiques." in ctx and "« Diapo »" in ctx
