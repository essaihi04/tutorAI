"""Le vérificateur des formats `apres_reponse` (rejeu après la réponse) et `rappel` (rappel déjà su), 18 novembre 2026."""
import importlib.util
from pathlib import Path

_spec = importlib.util.spec_from_file_location("verifier_parcours", Path(__file__).resolve().parents[2] / "scripts" / "verifier_parcours.py")
vp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(vp)


def deck(*slides):
    return {"id": "d", "activities": [{"id": "a", "slides": list(slides)}]}


X1 = {"id": "pr_x1", "question": {"prompt": "H′(x) ?", "options": ["a", "b"], "correct": 0},
      "concentration": {"pointage": [{"mot": "m", "commande": "play_until", "parametres": {"moment": "derivable"}}],
                        "apres_reponse": {"etapes": [{"commande": "play_until", "parametres": {"moment": "calcul"}}]}}}


def test_cles_comme_le_lecteur():
    s = {"question": {"prompt": "p"}, "exercises": [{"type": "qcm", "choices": ["a", "b"]}, {"type": "vrai_faux", "statements": [{}, {}]}]}
    assert vp.cles_des_questions(s) == ["q", "e0", "e1s0", "e1s1"]


def test_un_rejeu_bien_ecrit_passe():
    assert vp.verifier(deck(X1)) == ([], [])


def test_rejeu_mal_ecrit():
    mauvais = {**X1, "concentration": {"apres_reponse": {"question": "e3", "duree_s": -1, "etapes": [{"commande": "play_until"}, {}]}}}
    erreurs, _ = vp.verifier(deck(mauvais))
    assert any("e3" in e for e in erreurs) and any("duree_s" in e for e in erreurs)
    assert any("sans moment" in e for e in erreurs) and any("ni commande ni repere" in e for e in erreurs)
    assert any("sans question" in e for e in vp.verifier(deck({"id": "v", "concentration": {"apres_reponse": {"etapes": [{"repere": "r"}]}}}))[0])


def test_le_resultat_joue_avant_la_reponse_est_signale():
    s = {**X1, "concentration": {**X1["concentration"], "pointage": [{"mot": "m", "commande": "play_until", "parametres": {"moment": "calcul"}}]}}
    erreurs, remarques = vp.verifier(deck(s))
    assert not erreurs and remarques and "calcul" in remarques[0]


def test_rappel():
    diag = {"id": "le_o2_acquis", "question": {"prompt": "?", "options": ["a", "b"]}}
    rappel = {"id": "le_p1_cellule", "concentration": {"rappel": {"si_reussi": "le_o2_acquis"}}}
    assert vp.verifier(deck(diag, rappel)) == ([], [])
    assert vp.verifier(deck(diag, {**rappel, "concentration": {"rappel": {"si_reussi": ["le_o2_acquis"]}}})) == ([], [])
    assert any("AVANT" in e for e in vp.verifier(deck(rappel, diag))[0])
    assert any("introuvable" in e for e in vp.verifier(deck({**rappel, "concentration": {"rappel": {"si_reussi": "zz"}}}))[0])
    assert any("pas de question" in e for e in vp.verifier(deck({"id": "le_o2_acquis"}, rappel))[0])
    assert any("nommer" in e for e in vp.verifier(deck(diag, {**rappel, "concentration": {"rappel": {}}}))[0])


def test_un_cours_sans_ces_formats_ne_dit_rien():
    assert vp.verifier(deck({"id": "a", "question": {"prompt": "p"}}, {"id": "b"})) == ([], [])


def test_une_liste_de_rejeux():
    s = {**X1, "exercises": [{"type": "qcm", "choices": ["a", "b"]}], "concentration": {"apres_reponse": [
        {"etapes": [{"commande": "play_until", "parametres": {"moment": "derivee"}}]},
        {"question": "e0", "etapes": [{"commande": "play_until", "parametres": {"moment": "calcul"}}]}]}}
    assert vp.verifier(deck(s)) == ([], [])
    sans_nom = {**s, "concentration": {"apres_reponse": [s["concentration"]["apres_reponse"][0], {"etapes": [{"repere": "r"}]}]}}
    assert any("nomme sa question" in e for e in vp.verifier(deck(sans_nom))[0])
    double = {**s, "concentration": {"apres_reponse": [s["concentration"]["apres_reponse"][0], {"question": "q", "etapes": [{"repere": "r"}]}]}}
    assert any("deux rejeux" in e for e in vp.verifier(deck(double))[0])
