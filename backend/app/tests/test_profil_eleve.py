"""Profil de l'élève (services/profil_eleve.py) : ce qu'il doit faire, dans l'ordre, et le texte pour le tuteur."""
from app.services import profil_eleve, stats_cours

DECK = {"id": "d1", "stable_id": "d1", "title": "Ondes", "competences": [
    {"id": "c1", "label": "Célérité"}, {"id": "c2", "label": "Retard"}, {"id": "c3", "label": "Longueur d'onde"}],
    "activities": [{"id": "a", "slides": [
        {"id": "s1", "title": "Intro", "competence_ids": ["c1"]},
        {"id": "s2", "title": "Retard", "competence_ids": ["c2"]},
        {"id": "s3", "title": "Lambda", "competence_ids": ["c3"]}]}]}


def _tableau(student_id, avec_vues=False):
    return {
        "d1": {"titre": "Ondes", "diapos": 3, "vu_pourcent": 67, "diapos_vues": ["s1", "s2"],
               "stats": {"ouvertures": 2, "terminaisons": 0, "minutes": 30, "derniere": "2026-11-21T10:00:00+00:00"},
               "competences": {"total": 3, "acquis": 1, "partiel": 0, "non_acquis": 1, "non_evalue": 1, "liste": [
                   {"id": "c1", "label": "Célérité", "statut": "acquis", "score": 1.0, "reprendre_avec": []},
                   {"id": "c2", "label": "Retard", "statut": "non_acquis", "score": 0.0, "reprendre_avec": ["un vrai/faux"]},
                   {"id": "c3", "label": "Longueur d'onde", "statut": "non_evalue", "score": None, "reprendre_avec": []}]}},
        "d2": {"titre": "Jamais ouvert", "diapos": 5, "vu_pourcent": 0, "diapos_vues": [], "stats": None,
               "competences": {"total": 2, "acquis": 0, "partiel": 0, "non_acquis": 0, "non_evalue": 2, "liste": []}},
    }


def test_a_faire_dans_l_ordre(monkeypatch):
    monkeypatch.setattr(stats_cours, "tableau", _tableau)
    monkeypatch.setattr(stats_cours, "cours_alleges", lambda: {"d1": DECK})
    p = profil_eleve.profil("x")
    assert list(p["cours"]) == ["d1"]                       # un cours jamais ouvert n'est pas dans le profil
    assert [a["type"] for a in p["a_faire"]] == ["exercice", "cours", "element"]
    assert p["a_faire"][0]["competence"] == "c2" and p["a_faire"][0]["diapos"][0]["id"] == "s2"
    assert p["a_faire"][1]["diapo"]["id"] == "s3"           # cours à entendre : la prochaine diapositive non vue
    assert p["global"]["pourcent_acquis"] == 33
    texte = profil_eleve.bloc_prompt(p)
    assert "PROFIL DE L'ÉLÈVE" in texte and "Retard" in texte and "à reprendre avec un vrai/faux" in texte
