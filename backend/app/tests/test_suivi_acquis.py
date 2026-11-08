"""Le suivi des acquis par compétence : statut, trajet, méthodes qui marchent, lacunes et bloc du mode libre."""
from app.services import suivi_acquis as sa

DECK = {
    "id": "d1", "title": "Ondes",
    "competences": [{"id": "C1", "label": "Reconnaître une onde"}, {"id": "C4", "label": "Le retard"}],
    "activities": [{"id": "a", "slides": [
        {"id": "s1", "competence_ids": ["C1"]}, {"id": "s2", "competence_ids": ["C1"]}, {"id": "s3", "competence_ids": ["C4"]}]}],
}


def ev(slide, cle, tentative, correct, **meth):
    return {"deck_id": "d1", "slide_id": slide, "slide_title": slide.upper(), "cle": cle, "type": "qcm", "tentative": tentative,
            "correct": correct, "reponse": "x", "methodes": {"visuel": "simulation", "formules_au_centre": 1, "tuteur_a_montre": 3, **meth}}


def test_score_et_statut_d_une_question():
    assert sa.score_question([ev("s1", "q", 1, True)]) == 1.0
    assert sa.score_question([ev("s1", "q", 1, False), ev("s1", "q", 2, True)]) == 0.5
    assert sa.score_question([ev("s1", "q", 1, False), ev("s1", "q", 2, False)]) == 0.0
    assert sa.score_question([ev("s1", "q", 1, None)]) is None
    assert sa.statut(1.0) == "acquis" and sa.statut(0.5) == "partiel" and sa.statut(0.0) == "non_acquis" and sa.statut(None) == "non_evalue"


def test_bilan_par_competence_avec_trajet_et_methode_de_reprise():
    evs = [ev("s1", "q", 1, True), ev("s2", "e0", 1, True, exercice=True),           # C1 acquis
           ev("s3", "q", 1, False, visuel="image"), ev("s3", "q", 2, False, visuel="image")]   # C4 non acquis, expliqué par image
    b = sa.bilan(evs, DECK)
    c1, c4 = b["competences"]
    assert c1["statut"] == "acquis" and c4["statut"] == "non_acquis"
    assert len(c4["trajet"]) == 1 and "non_acquis" in c4["trajet"][0]
    assert "image" in c4["methodes_qui_ont_echoue"]
    # ce qui a marché chez lui (simulation, exercice…) est proposé pour reprendre, jamais l'image qui a échoué
    assert c4["a_reprendre_avec"] and "image" not in c4["a_reprendre_avec"]
    assert set(b["resume"]["acquis"]) == {"Reconnaître une onde"} and b["resume"]["non_acquis"] == ["Le retard"]
    assert b["taux_par_methode"]["simulation"] == 1.0 and b["taux_par_methode"]["image"] == 0.0


def test_lacunes_et_bloc_pour_le_mode_libre():
    evs = [ev("s1", "q", 1, True), ev("s3", "q", 1, False, visuel="image"), ev("s3", "q", 2, True, visuel="image")]
    b = sa.bilan(evs, DECK)
    lac = sa.lacunes(b)
    assert [x["label"] for x in lac] == ["Le retard"] and lac[0]["statut"] == "partiel" and lac[0]["reprendre_avec"]
    bloc = sa.bloc_prompt(b, "Ondes")
    assert bloc.startswith("[ACQUIS DE L'ÉLÈVE — Ondes]") and "PARTIEL : Le retard" in bloc and "Reconnaître une onde" in bloc
    assert "nouvelle question" in bloc


def test_sans_competences_declarees_une_par_activite():
    deck = {"activities": [{"id": "act", "title": "Partie 1", "slides": [{"id": "s"}]}]}
    comps, par = sa.competences_du_cours(deck)
    assert comps == [{"id": "act", "label": "Partie 1"}] and par == {"s": ["act"]}


def test_enregistrer_et_relire(tmp_path, monkeypatch):
    monkeypatch.setattr(sa, "DOSSIER", tmp_path)
    sa.enregistrer("eleve-1", ev("s1", "q", 1, True))
    sa.enregistrer("eleve-1", {**ev("s3", "q", 1, False), "deck_id": "autre"})
    assert len(sa.lire("eleve-1")) == 2 and len(sa.lire("eleve-1", "d1")) == 1 and sa.lire("eleve-2") == []
    assert sa.lire("eleve-1")[0]["quand"]
