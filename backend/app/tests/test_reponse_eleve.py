"""Le tuteur réagit à chaque réponse : indice au 1er essai, réponse au 2e, la clé connue l'emporte."""
from app.services import reponse_eleve as re_


Q = {"type": "qcm", "enonce": "M est deux fois plus loin. Le retard τ…", "choix": ["double", "reste le même", "est divisé par deux"]}


def test_premier_essai_un_indice_sans_la_reponse():
    p = re_.prompt_reponse({"title": "Retard"}, Q, "B. reste le même", 1, None)
    assert "NE DONNE PAS la bonne réponse" in p and "essai n° 1" in p and "B. reste le même" in p
    assert "A. double" in p and "jamais en chiffres" in p


def test_deuxieme_essai_la_reponse():
    p = re_.prompt_reponse({"title": "Retard"}, {**Q, "bonne": 0}, "C", 2, False)
    assert "donne la bonne réponse" in p and "Bonne réponse : A. double" in p and "VERDICT IMPOSÉ" in p


def test_la_cle_connue_l_emporte_sur_le_modele():
    r = re_.reaction_reponse('{"correct": true, "parole": "مزيان", "ecrit": "ok"}', False)
    assert r["correct"] is False and r["parole"] == "مزيان"


def test_reponse_libre_injugeable_et_json_bancal():
    assert re_.reaction_reponse('{"correct": null, "parole": "وضح ليا"}', None)["correct"] is None
    assert re_.reaction_reponse('{"correct": "oui", "parole": "x"}', None) is None
    assert re_.reaction_reponse("rien", None) is None


def test_ton_chaleureux_dans_le_prompt():
    p = re_.prompt_reponse({"title": "Retard"}, Q, "B", 1, None)
    assert "برافو عليك" in p and "ne félicite pas une réponse fausse" in p
