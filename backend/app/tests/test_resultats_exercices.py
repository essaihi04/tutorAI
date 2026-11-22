from app.services import resultats_exercices as rx


CAT = [{"id": "e1", "cours": "svt_ch1_x", "matiere": "svt", "niveau": "moyen", "questions": 2},
       {"id": "e2", "cours": "svt_ch1_x", "matiere": "svt", "niveau": "facile", "questions": 1}]


def test_par_exercice_dernier_essai_et_statut():
    evs = [{"exercice_id": "e1", "mode": "exercice", "question_id": "1", "note": 0, "sur": 1, "pertes": ["unité"]},
           {"exercice_id": "e1", "mode": "exercice", "question_id": "1", "note": 1, "sur": 1},
           {"exercice_id": "e1", "mode": "exercice", "question_id": "2", "note": 0.5, "sur": 1, "pertes": ["justification"]},
           {"exercice_id": "e2", "mode": "exercice", "question_id": "1", "note": 0.25, "sur": 1}]
    p = rx.par_exercice(evs, CAT)
    assert p["e1"]["exercice"]["note"] == 1.5 and p["e1"]["exercice"]["sur"] == 2 and p["e1"]["statut"] == "reussi"
    assert p["e1"]["exercice"]["pertes"] == ["justification"]
    assert p["e2"]["statut"] == "a_revoir" and not p["e1"]["acquis"]


def test_progression_croise_cours_et_exercices(tmp_path, monkeypatch):
    monkeypatch.setattr(rx, "DOSSIER", tmp_path)
    monkeypatch.setattr(rx, "catalogue", lambda: CAT)
    from app.services import stats_cours
    monkeypatch.setattr(stats_cours, "tableau", lambda sid, avec_vues=False: {"svt_ch1_x": {
        "titre": "Énergie", "vu_pourcent": 80,
        "competences": {"total": 4, "acquis": 2, "partiel": 0, "non_acquis": 2, "non_evalue": 0,
                        "liste": [{"label": "glycolyse", "statut": "acquis"}, {"label": "Krebs", "statut": "non_acquis"}]}}})
    rx.enregistrer("s1", {"exercice_id": "e1", "mode": "exercice", "question_id": "1", "note": 1, "sur": 1})
    rx.enregistrer("s1", {"exercice_id": "e1", "mode": "exercice", "question_id": "2", "note": 1, "sur": 1})
    p = rx.progression("s1")
    c = p["cours"]["svt_ch1_x"]
    assert c["cours_pourcent"] == 0.5 and c["exercices_pourcent"] == 1.0
    assert c["pourcent"] == 0.8 and c["note20"] == 16.0 and c["lacunes_cours"] == ["Krebs"]
    assert p["matieres"]["svt"]["note20"] == 16.0 and p["global"]["exercices_faits"] == 1
    assert p["forces"][0]["cours"] == "svt_ch1_x"
