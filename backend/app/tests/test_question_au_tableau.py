"""La question libre classée par rapport au cours (9 novembre 2026) : expliquée au tableau, annoncée pour une
diapositive suivante, notion de base après la brosse, ou hors cours sans réponse."""
import json

from app.services import question_eleve as qe

DECK = {"title": "Ondes", "activities": [
    {"slides": [{"id": "a", "title": "Ouverture"}, {"id": "b", "title": "Définition"}]},
    {"slides": [{"id": "c", "title": "La célérité", "screen_content": {"lead": "v = d / Δt"}}, {"id": "d", "title": "Le retard"}]},
]}


def test_plan_du_cours():
    plan, idx = qe.plan_du_cours(DECK, "b")
    assert [s["id"] for s in plan] == ["a", "b", "c", "d"] and idx == 1
    assert "c" in qe.prompt_question({"title": "Définition"}, {"texte": "c'est quoi v ?", "transcription": "", "image_texte": ""}, plan, idx, "Ondes")


def _r(d, idx=1):
    plan, _ = qe.plan_du_cours(DECK, "b")
    return qe.reponse_depuis(json.dumps(d), {}, plan, idx)


def test_diapo_au_tableau():
    r = _r({"categorie": "diapo", "parole": "شوف la perturbation.", "tableau": ["onde = perturbation", "", "pas de matière"], "ecrit": "x"})
    assert r["categorie"] == "diapo" and r["tableau"] == ["onde = perturbation", "pas de matière"] and r["parole"]


def test_suivante_donne_la_diapo():
    r = _r({"categorie": "suivante", "notion": "la célérité", "diapo_id": "c"})
    assert r["categorie"] == "suivante" and r["diapo_suivante"] == {"id": "c", "title": "La célérité"} and not r["parole"]


def test_diapo_deja_faite_est_expliquee():
    assert _r({"categorie": "suivante", "diapo_id": "a", "parole": "شوف."})["categorie"] == "diapo"


def test_prerequis_et_hors_cours_sans_reponse():
    p = _r({"categorie": "prerequis", "notion": "vitesse moyenne", "parole": "..."})
    assert p["categorie"] == "prerequis" and p["notion"] == "vitesse moyenne" and not p["parole"]
    assert _r({"categorie": "hors_cours", "notion": "la mitose"})["categorie"] == "hors_cours"


def test_diapo_sans_parole_est_rejetee():
    assert _r({"categorie": "diapo"}) is None


def test_explication_du_prerequis():
    r = qe.explication_depuis(json.dumps({"parole": "مزيان.", "tableau": "v = d / Δt\nen m/s", "ecrit": "e"}))
    assert r["tableau"] == ["v = d / Δt", "en m/s"]
    assert "vitesse moyenne" in qe.prompt_prerequis({"title": "Retard"}, "c'est quoi la vitesse ?", "vitesse moyenne")


def test_exercice_apres_l_explication():
    q = qe.valider_exercice({"type": "QCM", "enonce": "τ = ?", "choix": ["SM / v", "v / SM", ""], "bonne": 0, "parole_juste": "**مزيان**"})
    assert q["type"] == "qcm" and q["choix"] == ["SM / v", "v / SM"] and q["parole_juste"] == "مزيان"
    assert qe.valider_exercice({"type": "qcm", "choix": ["a", "b"], "bonne": 5}) is None
    vf = qe.valider_exercice({"type": "vrai-faux", "affirmations": [{"texte": "a", "vrai": True}, {"texte": "b", "vrai": False}, {"texte": "c", "vrai": "oui"}]})
    assert vf["type"] == "vrai_faux" and len(vf["affirmations"]) == 2
    a = qe.valider_exercice({"type": "association", "paires": [{"gauche": "v", "droite": "m/s"}, {"gauche": "τ", "droite": "s"}]})
    assert a["paires"][1] == {"gauche": "τ", "droite": "s"}
    assert qe.valider_exercice({"type": "association", "paires": [{"gauche": "a", "droite": "s"}, {"gauche": "b", "droite": "s"}]}) is None
    assert qe.valider_exercice("rien") is None


def test_l_explication_porte_son_exercice():
    ex = {"type": "vrai_faux", "affirmations": [{"texte": "a", "vrai": True}, {"texte": "b", "vrai": False}]}
    assert _r({"categorie": "diapo", "parole": "شوف.", "exercice": ex})["exercice"]["type"] == "vrai_faux"
    assert qe.explication_depuis(json.dumps({"parole": "مزيان.", "exercice": {"type": "x"}}))["exercice"] is None
    assert "association" in qe.prompt_prerequis({"title": "R"}, "q", "n")
