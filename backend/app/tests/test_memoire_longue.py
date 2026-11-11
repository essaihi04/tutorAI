"""Mémoire longue : échelle des rappels, même matière, autre formulation, rétention, notifications, routes."""
from datetime import date, datetime, timedelta, timezone

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.services import memoire_longue as ml

ONDES = {
    "id": "phys_ch1_x", "title": "Ondes", "activities": [],
    "competences": [
        {"id": "C1", "label": "Reconnaître une onde", "rappels": [
            {"id": "r1", "type": "libre", "prompt": "Définis une onde", "attendu": "perturbation"},
            {"id": "r2", "type": "qcm", "prompt": "Une onde transporte…", "options": ["matière", "énergie"], "correct": 1},
            {"id": "r3", "type": "vrai_faux", "prompt": "Une onde transporte la matière", "correct": 1}]},
        {"id": "C2", "label": "Calculer la célérité", "rappels": [{"id": "r1", "type": "libre", "prompt": "v = ?", "attendu": "d/Δt"}]},
        {"id": "C3", "label": "Sans rappel"},
    ],
    "seances": [{"id": "s1", "titre": "Séance 1", "blocs": [
        {"id": "b1", "titre": "Bloc 1", "slide_ids": ["a"]}, {"id": "b2", "titre": "Bloc 2", "slide_ids": ["b"]}]}],
}
CHIMIE = {"id": "chem_ch1_x", "title": "Cinétique", "activities": [],
          "competences": [{"id": "C1", "label": "Vitesse", "rappels": [{"id": "r1", "prompt": "Définis v"}]}]}
SVT = {"id": "svt_ch1_x", "title": "Muscle", "activities": [],
       "competences": [{"id": "C1", "label": "Contraction", "rappels": [{"id": "r1", "prompt": "Explique"}]}]}
COURS = {"phys_ch1_x": ONDES, "chem_ch1_x": CHIMIE, "svt_ch1_x": SVT}

J0 = datetime(2026, 11, 1, 17, 0, tzinfo=timezone.utc)     # 18 h au Maroc


def q(t, deck, comps, correct=True):
    return {"deck_id": deck, "slide_id": "s", "cle": "q", "competence_ids": comps, "correct": correct, "quand": t.isoformat()}


def rappel(t, deck, comp, correct, correct_2=None, rid="r1", **kw):
    return {"evenement": "rappel", "cours_id": deck, "competence_id": comp, "rappel_id": rid, "correct": correct,
            "correct_2": correct_2, "quand": t.isoformat(), **kw}


def test_matiere_par_id_et_par_sujet():
    assert ml.matiere_de("phys_ch2") == ml.matiere_de("chem_ch1") == "physique-chimie"
    assert ml.matiere_de("svt_ch3") == "svt" and ml.matiere_de("math_ch1") == "mathematiques"
    assert ml.matiere_de("cours_x", {"subject": "Mathématiques"}) == "mathematiques"


def test_echelle_monte_descend_et_reste():
    evs = [q(J0, "phys_ch1_x", ["C1"])]
    p = ml.planning(evs, COURS)["phys_ch1_x::C1"]
    assert p["marche"] == 0 and p["due"] == "2026-11-02"                      # J+1
    evs.append(rappel(J0 + timedelta(days=1), "phys_ch1_x", "C1", True))      # réussi du premier coup → J+3
    p = ml.planning(evs, COURS)["phys_ch1_x::C1"]
    assert p["marche"] == 1 and p["due"] == "2026-11-05"
    evs.append(rappel(J0 + timedelta(days=4), "phys_ch1_x", "C1", False, True))   # 2ᵉ essai → reste, J+3 de nouveau
    p = ml.planning(evs, COURS)["phys_ch1_x::C1"]
    assert p["marche"] == 1 and p["due"] == "2026-11-08"
    evs.append(rappel(J0 + timedelta(days=7), "phys_ch1_x", "C1", False, False))  # raté → retour à J+1
    p = ml.planning(evs, COURS)["phys_ch1_x::C1"]
    assert p["marche"] == 0 and p["due"] == "2026-11-09"


def test_derniere_marche_avant_l_examen():
    assert ml.due_apres(4, date(2027, 5, 1)) == ml.DATE_EXAMEN - timedelta(days=ml.AVANCE_EXAMEN)
    assert ml.due_apres(4, date(2026, 12, 1)) == date(2026, 12, 31)
    assert [ml.due_apres(m, date(2026, 11, 1)).day for m in range(4)] == [2, 4, 8, 22]


def test_rappels_meme_matiere_les_plus_en_retard_d_abord():
    evs = [q(J0, "phys_ch1_x", ["C1"]), q(J0 + timedelta(days=2), "phys_ch1_x", ["C2", "C3"]),
           q(J0, "svt_ch1_x", ["C1"]), q(J0, "chem_ch1_x", ["C1"])]
    r = ml.rappels_du_jour(evs, "physique-chimie", J0 + timedelta(days=5), COURS)
    cles = [(x["cours_id"], x["competence_id"]) for x in r["questions"]]
    assert ("svt_ch1_x", "C1") not in cles                                    # jamais une autre matière
    assert cles[:2] in ([("phys_ch1_x", "C1"), ("chem_ch1_x", "C1")], [("chem_ch1_x", "C1"), ("phys_ch1_x", "C1")])
    assert ("phys_ch1_x", "C3") not in cles                                   # sans question de rappel : ignorée
    assert len(cles) == 3 and r["minutes"] == 3
    assert ml.rappels_du_jour(evs, "svt", J0 + timedelta(days=5), COURS)["questions"][0]["cours_id"] == "svt_ch1_x"


def test_rien_de_du_rien_a_rappeler_et_complement_en_avance():
    evs = [q(J0, "phys_ch1_x", ["C1"])]
    assert ml.rappels_du_jour(evs, "physique-chimie", J0, COURS)["questions"] == []          # le jour même : rien
    evs.append(q(J0 + timedelta(days=1), "phys_ch1_x", ["C2"]))
    r = ml.rappels_du_jour(evs, "physique-chimie", J0 + timedelta(days=1), COURS)
    assert [(x["competence_id"], x["en_avance"]) for x in r["questions"]] == [("C1", False), ("C2", True)]
    # un rappel fait en avance et réussi ne fait pas monter la marche
    evs.append(rappel(J0 + timedelta(days=1), "phys_ch1_x", "C2", True, en_avance=True))
    assert ml.planning(evs, COURS)["phys_ch1_x::C2"]["marche"] == 0


def test_une_autre_formulation_que_la_derniere_fois():
    qs = ONDES["competences"][0]["rappels"]
    assert ml.choisir_question(qs, [])["id"] == "r1"
    assert ml.choisir_question(qs, ["r1"])["id"] == "r2"
    assert ml.choisir_question(qs, ["r1", "r2", "r3"])["id"] == "r1"
    assert ml.choisir_question(qs, ["r2", "r3", "r1"])["id"] == "r2"


def test_enrichir_un_rappel_marche_jours_et_suite():
    evs = [q(J0, "phys_ch1_x", ["C1"])]
    e = ml.enrichir_rappel(evs, {"evenement": "rappel", "cours_id": "phys_ch1_x", "competence_id": "C1", "correct": True},
                           J0 + timedelta(days=2), COURS)
    assert e["marche"] == 0 and e["jours_depuis"] == 2 and e["age_jours"] == 2
    assert e["marche_apres"] == 1 and e["prochaine"] == "2026-11-06" and e["matiere"] == "physique-chimie"


def test_retention_j7_j30():
    evs = [q(J0, "phys_ch1_x", ["C1", "C2"]),
           rappel(J0 + timedelta(days=8), "phys_ch1_x", "C1", True, jours_depuis=8, age_jours=8),
           rappel(J0 + timedelta(days=9), "phys_ch1_x", "C2", False, False, jours_depuis=9, age_jours=9),
           rappel(J0 + timedelta(days=31), "phys_ch1_x", "C1", True, jours_depuis=23, age_jours=31),
           rappel(J0 + timedelta(days=31), "phys_ch1_x", "C2", True, jours_depuis=0, age_jours=31),     # le même jour : ne compte pas
           {"evenement": "seance_fin", "cours_id": "phys_ch1_x", "duree_s": 1800, "quand": J0.isoformat()},
           {"evenement": "saturation", "cours_id": "phys_ch1_x", "cause": "deux_fausses", "action": "cahier", "quand": J0.isoformat()}]
    r = ml.retention({"e1": evs}, J0 + timedelta(days=31), COURS)
    c = r["par_cours"][0]
    assert c["j7"] == {"n": 2, "reussis": 1, "taux": 0.5} and c["j30"] == {"n": 1, "reussis": 1, "taux": 1.0}
    comp = {x["competence_id"]: x for x in r["par_competence"]}
    assert comp["C1"]["rappels"]["taux"] == 1.0 and comp["C2"]["rappels"]["taux"] == 0.0
    el = r["par_eleve"][0]
    assert el["seances"] == 1 and el["duree_moyenne_min"] == 30.0 and el["saturations"] == {"deux_fausses": 1}


def test_progression_des_blocs_et_reprise():
    evs = [{"evenement": "cahier", "cours_id": "phys_ch1_x", "bloc_id": "b1"},
           {"evenement": "retrouver", "cours_id": "phys_ch1_x", "bloc_id": "b1", "correct": True},
           {"evenement": "exercice_bloc", "cours_id": "phys_ch1_x", "bloc_id": "b1", "correct": False, "correct_2": True},
           {"evenement": "cahier", "cours_id": "phys_ch1_x", "bloc_id": "b2"}]
    p = ml.progression(evs, ONDES)
    assert p["reprise"] == {"seance": 0, "bloc": 1, "seance_id": "s1", "bloc_id": "b2", "etape": "retrouver"}
    assert p["blocs"]["b1"]["exercice"] == "second_essai" and not p["termine"]


def test_notification_a_l_heure_une_par_jour_et_discrete():
    evs = [q(J0, "phys_ch1_x", ["C1", "C2"]), q(J0 - timedelta(days=1), "svt_ch1_x", ["C1"])]
    tot = J0 + timedelta(days=2) - timedelta(hours=10)          # 8 h au Maroc : avant son heure (18 h)
    a = ml.accueil(evs, tot, COURS)
    assert a["badge"] == 3 and a["notification"] is None and a["heure"] == 18
    a = ml.accueil(evs, J0 + timedelta(days=2), COURS)
    n = a["notification"]
    assert n["matiere"] == "physique-chimie" and n["texte"] == "2 rappels de physique-chimie t'attendent (2 min)"
    assert n["niveau"] == "banniere" and n["nouvelle"]
    # coupées d'un geste
    assert ml.accueil([*evs, {"evenement": "preferences", "heure": None, "coupees": True, "quand": J0.isoformat()}],
                      J0 + timedelta(days=2), COURS)["notification"] is None
    # trois ignorées de suite → discrète
    ignorees = [{"evenement": "notification", "action": "envoyee", "quand": (J0 + timedelta(days=d)).isoformat()} for d in (-3, -2, -1)]
    assert ml.accueil([*evs, *ignorees], J0 + timedelta(days=2), COURS)["notification"]["niveau"] == "discret"
    # rien de dû : aucune
    assert ml.accueil([q(J0, "phys_ch1_x", ["C1"])], J0 + timedelta(hours=3), COURS)["notification"] is None


def test_heure_habituelle_apprise_des_seances():
    evs = [{"evenement": "seance_debut", "quand": datetime(2026, 11, d, 20, 10, tzinfo=timezone.utc).isoformat()} for d in (1, 2, 3)]
    assert ml.heure_habituelle(evs) == 21          # 20 h UTC = 21 h au Maroc
    assert ml.heure_habituelle(evs[:1]) is None


# ── Les routes (élève connecté, lien libre, admin) ──

@pytest.fixture()
def client(monkeypatch, tmp_path):
    from app.api.v1.endpoints import memoire, public_cours
    from app.dependencies import get_current_student
    from app.services import suivi_acquis
    monkeypatch.setattr(suivi_acquis, "DOSSIER", tmp_path)
    monkeypatch.setattr(ml, "tous_les_cours", lambda: COURS)
    monkeypatch.setattr(public_cours, "cours_publics", lambda: {"phys_ch1_x"})
    public_cours._appels.clear()
    app = FastAPI()
    app.include_router(memoire.router)
    app.include_router(public_cours.router)
    app.dependency_overrides[get_current_student] = lambda: {"id": "eleve-1"}
    return TestClient(app)


def test_routes_du_cycle_et_des_rappels(client):
    from app.services import suivi_acquis
    suivi_acquis.enregistrer("eleve-1", {"deck_id": "phys_ch1_x", "slide_id": "s", "cle": "q", "competence_ids": ["C1"], "correct": True})
    r = client.post("/course-player/memoire/evenement", json={"evenement": "cahier", "cours_id": "phys_ch1_x", "bloc_id": "b1", "bloc_index": 0, "duree_s": 95})
    assert r.status_code == 200, r.text
    e = suivi_acquis.lire("eleve-1")[-1]
    assert e["evenement"] == "cahier" and e["bloc_index"] == 0 and e["matiere"] == "physique-chimie" and "deck_id" not in e
    # le bilan du cours ne voit pas ces événements
    assert len(suivi_acquis.lire("eleve-1", "phys_ch1_x")) == 1
    r = client.post("/course-player/memoire/evenement", json={"evenement": "rappel", "cours_id": "phys_ch1_x", "competence_id": "C1", "rappel_id": "r1", "correct": True})
    assert r.json()["marche"] == 1
    s = client.get("/course-player/memoire/seance/phys_ch1_x").json()
    assert s["matiere"] == "physique-chimie" and s["progression"]["reprise"]["etape"] == "retrouver"
    assert client.get("/course-player/memoire/rappels/inconnue").status_code == 404
    assert client.post("/course-player/memoire/evenement", json={"evenement": "notification", "action": "envoyee"}).status_code == 400
    assert client.post("/course-player/memoire/preferences", json={"heure": 20}).json()["heure"] == 20
    assert client.get("/course-player/memoire/accueil").json()["heure"] == 20


def test_accueil_note_la_notification_envoyee_une_fois(client):
    import json
    from app.services import suivi_acquis
    avant = (datetime.now(timezone.utc) - timedelta(days=2)).isoformat()
    with suivi_acquis._fichier("eleve-1").open("a", encoding="utf-8") as f:     # une réponse du cours, il y a deux jours
        f.write(json.dumps({"deck_id": "phys_ch1_x", "slide_id": "s", "cle": "q", "competence_ids": ["C1"], "correct": True, "quand": avant}) + chr(10))
    client.post("/course-player/memoire/preferences", json={"heure": 0})            # son heure : minuit, donc déjà passée
    a = client.get("/course-player/memoire/accueil").json()
    assert a["notification"]["nombre"] == 1 and a["notification"]["nouvelle"]
    assert client.get("/course-player/memoire/accueil").json()["notification"]["nouvelle"] is False
    envoyees = [e for e in suivi_acquis.lire("eleve-1") if e.get("evenement") == "notification"]
    assert len(envoyees) == 1
    client.post("/course-player/memoire/evenement", json={"evenement": "notification", "action": "ouverte", "matiere": "physique-chimie"})
    assert client.get("/course-player/memoire/accueil").json()["ignorees"] == 0


def test_lien_libre(client):
    H = {"X-Visiteur": "abcdef12-3456"}
    assert client.get("/public/cours-ondes/memoire/seance/phys_ch1_x", headers=H).status_code == 200
    assert client.get("/public/cours-ondes/memoire/seance/svt_ch1_x", headers=H).status_code == 404
    r = client.post("/public/cours-ondes/memoire/evenement", headers=H, json={"evenement": "cahier", "cours_id": "phys_ch1_x", "bloc_id": "b1"})
    assert r.status_code == 200, r.text
    assert client.post("/public/cours-ondes/memoire/evenement", headers=H, json={"evenement": "notification", "action": "ouverte"}).status_code == 400
