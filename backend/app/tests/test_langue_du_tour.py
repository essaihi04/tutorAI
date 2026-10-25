"""L'oral suit la langue de l'élève (choix du 2026-10-25)."""
from app.websockets.session_handler import bloc_langue_du_tour


def test_darija_donne_une_reponse_en_darija():
    bloc = bloc_langue_du_tour("اشرح لنا كيفاش عفاك", "Physique")
    assert "PRIORITAIRE" in bloc and "EN DARIJA" in bloc and "tableau (<ui>) reste" in bloc


def test_darija_avec_termes_francais():
    assert "EN DARIJA" in bloc_langue_du_tour("ما فهمتش la célérité", "Physique")


def test_francais_reste_en_francais():
    bloc = bloc_langue_du_tour("Comment on calcule la célérité ?", "Physique")
    assert "français simple" in bloc and "EN DARIJA" not in bloc


def test_rien_pour_un_nombre_ou_la_philosophie():
    assert bloc_langue_du_tour("7", "Physique") == ""
    assert bloc_langue_du_tour("", "Physique") == ""
    assert bloc_langue_du_tour("اشرح", "Philosophie") == ""
