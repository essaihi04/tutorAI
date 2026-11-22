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


def test_reponse_libre_partielle_et_matiere():
    q = {"type": "open", "enonce": "Justifier", "attendu": "la matrice", "matiere": "svt"}
    p = re_.prompt_reponse({"title": "Vésicules"}, q, "matrice", 1, None)
    assert "professeur de SVT" in p and "« partiel »" in p
    r = re_.reaction_reponse('{"correct": false, "partiel": true, "parole": "مزيان", "ecrit": "il manque la justification"}', None)
    assert r["partiel"] is True and r["correct"] is False
    assert re_.reaction_reponse('{"correct": true, "partiel": true, "parole": "x"}', None)["partiel"] is False


def test_bareme_par_element():
    q = {"type": "open", "enonce": "Justifier", "attendu": "x", "matiere": "svt", "bareme": 0.75,
         "elements": ["face extérieure = côté matrice", "intérieur = espace intermembranaire", "justification par les sphères"]}
    assert [e["sur"] for e in re_.elements_bareme(q)] == [0.25, 0.25, 0.25]
    assert "Barème de la question" in re_.prompt_reponse({"title": "V"}, q, "r", 1, None)
    r = re_.reaction_reponse('{"correct": false, "partiel": true, "parole": "x", "ecrit": "y", "details": '
                             '[{"n": 1, "cite": "", "obtenu": 0.25, "perte": "face extérieure absente"}, {"n": 2, "cite": "espace intermembranaire", "obtenu": 0.25}, {"n": 3, "cite": "", "obtenu": 0, "perte": "pas de justification"}]}', None, q)
    assert r["note"] == 0.25 and r["bareme"] == 0.75 and r["details"][0]["perte"] == "face extérieure absente"
    assert [e["sur"] for e in re_.elements_bareme({"bareme": 0.5, "elements": ["a", "b", "c", "d"]})] == [0.25, 0.25]
    assert re_.reaction_reponse('{"correct": true, "parole": "x", "details": []}', None, q)["note"] == 0.75
