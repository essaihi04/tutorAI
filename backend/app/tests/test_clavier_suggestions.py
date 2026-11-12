"""Les suggestions du clavier scientifique (aides et pièges), jamais la réponse attendue ; et la question « passée »."""
import json
from datetime import datetime, timedelta, timezone

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.services import clavier_suggestions as cs

MINI = {
    "id": "phys_ch9_mini", "title": "Mini",
    "activities": [{"id": "a", "slides": [
        {"id": "s1", "question": {"type": "open", "prompt": "Exprime la célérité v en fonction de λ et T.", "attendu": "v = λ/T"},
         "exercises": [{"type": "qcm", "prompt": "Unité de f ?", "choices": ["s", "Hz", "m"], "correct": 1},
                       {"type": "vrai_faux", "prompt": "Vrai ou faux ?", "statements": [{"text": "λ = v·T", "correct": True}]}]},
        {"id": "s2", "question": {"prompt": "Période ?", "attendu": "T = 1/f",
                                  "clavier": {"aides": ["f", " Hz ", "f", "T = 1/f", "1/f"], "pieges": ["f/1", "Hz", "s⁻¹"]}}},
    ]}],
    "seances": [{"id": "se1", "blocs": [{"id": "b1", "retrouver": {"prompt": "Cahier fermé : v = ?", "attendu": "v = d/Δt"},
                                          "exercice": {"type": "libre", "prompt": "Calcule v", "attendu": "2 m·s⁻¹"}}]}],
    "competences": [{"id": "C1", "rappels": [{"id": "C1_r1", "type": "libre", "prompt": "Formes indéterminées ?", "attendu": "0/0"}]}],
}


@pytest.fixture(autouse=True)
def cache_vide():
    cs._cache.clear()
    yield
    cs._cache.clear()


# ── Filtre ──

def test_la_reponse_attendue_et_les_relations_completes_sont_retirees():
    r = cs.filtrer(["v = λ/T", "λ/T", "λ / T", "λ", "T", "m·s⁻¹", "v=λ/T", "λ/ T·", "x" * 19, "λ"],
                   ["λ·T", "v = λT", "T/λ", "λ"], "v = λ/T")
    tout = r["aides"] + r["pieges"]
    assert "λ" in r["aides"] and "T" in r["aides"] and "m·s⁻¹" in r["aides"]
    assert not any("=" in x for x in tout)
    assert all(cs.normaliser(x) not in (cs.normaliser("v = λ/T"), cs.normaliser("λ/T")) for x in tout)
    assert r["aides"].count("λ") == 1 and "λ" not in r["pieges"]          # dédoublonné ; pas aide ET piège
    assert r["pieges"] == ["λ·T", "T/λ"]
    assert all(len(x) <= cs.LONGUEUR_MAX for x in tout)


def test_normalisation_exposants_produits_et_casse():
    assert cs.normaliser("x²") == cs.normaliser("x^2") == cs.normaliser("X ^ 2")
    assert cs.normaliser("m·s⁻¹") == cs.normaliser("m*s^-1") == cs.normaliser("m × s−1")
    assert cs.interdit("(x − 3)(x + 3)", "x² − 9 = (x − 3)(x + 3)")       # un côté de la relation attendue
    assert cs.interdit("2 m·s^-1 !", "2 m·s⁻¹")
    assert not cs.interdit("x²", "2")                                      # une réponse d'un caractère : égalité seule


def test_analyser_lit_le_json_meme_entoure():
    texte = 'Voici :\n```json\n{"aides": ["λ", "v = λ/T", "Hz"], "pieges": ["λ·T", 3, true]}\n```'
    r = cs.analyser(texte, "v = λ/T", "Exprime v")
    assert r == {"aides": ["λ", "Hz"], "pieges": ["λ·T", "3"]}
    assert cs.analyser("pas de json", "x", "") == {"aides": [], "pieges": []}


# ── Retrouver la question ──

def test_trouver_question_dans_toutes_les_formes():
    assert cs.trouver_question(MINI, "s1", "q")["attendu"] == "v = λ/T"
    assert cs.attendu_de(cs.trouver_question(MINI, "s1", "e0")) == "Hz"            # la bonne option d'un QCM
    assert cs.trouver_question(MINI, "s1", "e1s0")["prompt"] == "λ = v·T"
    assert cs.trouver_question(MINI, "b1", "retrouver")["attendu"] == "v = d/Δt"
    assert cs.trouver_question(MINI, "b1", "exercice_bloc")["attendu"] == "2 m·s⁻¹"
    assert cs.trouver_question(MINI, "C1", "C1_r1")["attendu"] == "0/0"
    assert cs.trouver_question(MINI, "s1", "e9") is None and cs.trouver_question(MINI, "zz", "q") is None


def test_donnees_preparees_prioritaires_et_nettoyees():
    q = cs.trouver_question(MINI, "s2", "q")
    r = cs.suggestions_preparees(q)
    assert r == {"aides": ["f", "Hz"], "pieges": ["f/1", "s⁻¹"]}       # « 1/f » est un côté de l'attendu
    d = cs.preparer(MINI, "phys_ch9_mini", "s2", "q", "", "physique")
    assert cs.deja_pretes(d)["source"] == "cours"


# ── Route, cache et LLM ──

@pytest.fixture()
def appels(monkeypatch):
    from app.services import llm_service as llm_mod, suivi_acquis
    vu = []

    async def chat(**kw):
        vu.append(kw)
        return json.dumps({"aides": ["λ", "T", "v = λ/T", "λ/T", "m·s⁻¹"], "pieges": ["λ·T", "T/λ"]})

    monkeypatch.setattr(llm_mod.llm_service, "chat", chat)
    monkeypatch.setattr(suivi_acquis, "charger_deck", lambda i: MINI if i in ("phys_ch9_mini", "phys_ch1_waves_exemple") else None)
    return vu


def _app(*routers):
    from app.dependencies import get_current_student
    app = FastAPI()
    for r in routers:
        app.include_router(r)
    app.dependency_overrides[get_current_student] = lambda: {"id": "eleve-1"}
    return TestClient(app)


def test_route_cache_le_llm_appele_une_fois(appels):
    from app.api.v1.endpoints import course_player
    c = _app(course_player.router)
    corps = {"deck_id": "phys_ch9_mini", "slide_id": "s1", "cle": "q", "enonce": "on m'envoie autre chose"}
    r1 = c.post("/course-player/clavier-suggestions", json=corps).json()
    r2 = c.post("/course-player/clavier-suggestions", json=corps).json()
    assert r1["source"] == "llm" and r2["source"] == "cache" and len(appels) == 1
    assert r1["aides"] == ["λ", "T", "m·s⁻¹"] and r1["pieges"] == ["λ·T", "T/λ"]
    assert "v = λ/T" in appels[0]["messages"][0]["content"]                 # l'attendu vient du cours, pas du client
    assert "autre chose" not in appels[0]["messages"][0]["content"]
    prep = c.post("/course-player/clavier-suggestions", json={"deck_id": "phys_ch9_mini", "slide_id": "s2", "cle": "q"}).json()
    assert prep["source"] == "cours" and len(appels) == 1


def test_route_question_introuvable_avec_ou_sans_enonce(appels):
    from app.api.v1.endpoints import course_player
    c = _app(course_player.router)
    r = c.post("/course-player/clavier-suggestions", json={"deck_id": "inconnu", "slide_id": "x", "cle": "q",
                                                         "enonce": "Exprime v", "matiere": "physique"}).json()
    assert r["source"] == "llm" and "v = λ/T" not in r["aides"] and "λ/T" in r["aides"]     # sans attendu : relations seules filtrées
    vide = c.post("/course-player/clavier-suggestions", json={"deck_id": "inconnu", "slide_id": "x", "cle": "q"}).json()
    assert vide == {"aides": [], "pieges": [], "source": "aucune"}


def test_route_erreur_du_llm_jamais_bloquante(monkeypatch):
    from app.api.v1.endpoints import course_player
    from app.services import llm_service as llm_mod, suivi_acquis

    async def panne(**kw):
        raise RuntimeError("panne")

    monkeypatch.setattr(llm_mod.llm_service, "chat", panne)
    monkeypatch.setattr(suivi_acquis, "charger_deck", lambda i: MINI)
    c = _app(course_player.router)
    r = c.post("/course-player/clavier-suggestions", json={"deck_id": "phys_ch9_mini", "slide_id": "s1", "cle": "q"})
    assert r.status_code == 200 and r.json() == {"aides": [], "pieges": [], "source": "aucune"}


def test_route_publique_cours_inconnu_refuse_et_plafond_seulement_pour_le_llm(appels, monkeypatch):
    from app.api.v1.endpoints import public_cours
    public_cours._appels.clear()
    c = _app(public_cours.router)
    H = {"X-Visiteur": "abcdef12-3456"}
    assert c.post("/public/cours-ondes/clavier-suggestions", json={"deck_id": "math_inconnu", "slide_id": "s1"}, headers=H).status_code == 404
    assert c.post("/public/cours-ondes/clavier-suggestions", json={"deck_id": "phys_ch1_waves_exemple", "slide_id": "s1"}).status_code == 400
    corps = {"deck_id": "phys_ch1_waves_exemple", "slide_id": "s1", "cle": "q"}
    assert c.post("/public/cours-ondes/clavier-suggestions", json=corps, headers=H).json()["source"] == "llm"
    assert c.post("/public/cours-ondes/clavier-suggestions", json=corps, headers=H).json()["source"] == "cache"
    assert c.post("/public/cours-ondes/clavier-suggestions", json={**corps, "slide_id": "s2"}, headers=H).json()["source"] == "cours"
    assert len(public_cours._appels[("llm", "v:abcdef12-3456")]) == 1          # seul l'appel au LLM a compté
    assert appels[0]["student_id"] is None
    public_cours._appels.clear()


# ── Question passée (bouton « Passer ») ──

def test_bilan_question_passee_ni_erreur_ni_acquise():
    from app.services import suivi_acquis as sa
    deck = {"id": "d1", "competences": [{"id": "C1", "label": "A"}, {"id": "C2", "label": "B"}],
            "activities": [{"id": "a", "slides": [{"id": "s1", "competence_ids": ["C1"]}, {"id": "s2", "competence_ids": ["C2"]}]}]}
    evs = [{"deck_id": "d1", "slide_id": "s1", "cle": "q", "tentative": 1, "correct": None, "passee": True},
           {"deck_id": "d1", "slide_id": "s2", "cle": "q", "tentative": 1, "correct": True},
           {"deck_id": "d1", "slide_id": "s2", "cle": "e0", "tentative": 1, "correct": None, "passee": True}]
    b = sa.bilan(evs, deck)
    c1, c2 = b["competences"]
    assert c1["questions"][0]["statut"] == "passee" and c1["score"] is None and c1["statut"] == "non_evalue"
    assert c1["passees"] == 1 and c2["passees"] == 1
    assert c2["statut"] == "acquis" and c2["score"] == 1.0                # la question passée ne tire pas le score vers le bas
    assert sa.lacunes(b) == [] and "A" not in b["resume"]["acquis"]       # pas d'erreur, pas de reprise, pas acquis
    assert all(v == 1.0 for v in b["taux_par_methode"].values())         # hors méthodes


def test_rappel_passe_revient_bientot():
    from app.services import memoire_longue as ml
    cours = {"phys_ch1_x": {"id": "phys_ch1_x", "title": "Ondes", "activities": [],
                            "competences": [{"id": "C1", "label": "X", "rappels": [{"id": "r1", "prompt": "?"}]}]}}
    j0 = datetime(2026, 11, 1, 17, 0, tzinfo=timezone.utc)
    evs = [{"deck_id": "phys_ch1_x", "slide_id": "s", "cle": "q", "competence_ids": ["C1"], "correct": True, "quand": j0.isoformat()}]
    for k, d in enumerate((1, 4)):        # deux rappels réussis : marche 2 (J+7)
        evs.append({"evenement": "rappel", "cours_id": "phys_ch1_x", "competence_id": "C1", "correct": True,
                    "quand": (j0 + timedelta(days=d)).isoformat()})
    assert ml.planning(evs, cours)["phys_ch1_x::C1"]["marche"] == 2
    t = j0 + timedelta(days=11)
    passe = {"evenement": "rappel", "cours_id": "phys_ch1_x", "competence_id": "C1", "correct": None, "passee": True,
             "quand": t.isoformat()}
    p = ml.planning([*evs, passe], cours)["phys_ch1_x::C1"]
    assert p["marche"] == 0 and p["due"] == (ml.jour_local(t) + timedelta(days=1)).isoformat()
    assert p["rappels"][-1]["resultat"] == "passe"
    e = ml.enrichir_rappel(evs, {k: v for k, v in passe.items() if k != "quand"}, maintenant=t, cours=cours)
    assert e["marche_apres"] == 0 and e["prochaine"] == (ml.jour_local(t) + timedelta(days=1)).isoformat()


def test_une_reponse_enumeree_ne_se_redonne_pas_morceau_par_morceau():
    from app.services import clavier_suggestions as cs
    attendu = "Quatre formes indéterminées : 0/0, ∞/∞, +∞ − ∞, 0 × ∞."
    r = cs.filtrer(["0/0", "∞/∞", "0 × ∞", "+∞ − ∞", "∞", "→"], ["0 + 0", "1/∞"], attendu)
    assert r["aides"] == ["∞", "→"]
    assert r["pieges"] == ["0 + 0", "1/∞"]
    # une relation n'est pas une énumération : ses grandeurs restent proposables
    assert cs.filtrer(["v", "T", "Hz"], [], "λ = v·T")["aides"] == ["v", "T", "Hz"]


def test_les_facteurs_d_une_factorisation_attendue_sont_retires():
    from app.services import clavier_suggestions as cs
    r = cs.filtrer(["(x + 3)", "(x − 3)", "x²", "−9"], ["(x + 9)", "(x² + 3)"], "x² − 9 = (x − 3)(x + 3)")
    assert "(x + 3)" not in r["aides"] and "(x − 3)" not in r["aides"]
    assert r["aides"] == ["x²", "−9"] and r["pieges"] == ["(x + 9)", "(x² + 3)"]
