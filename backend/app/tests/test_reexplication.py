"""Le cycle de reprise : réexpliquer autrement, gestes dans la simulation, question jumelle, 3 cycles au plus."""
import json

from app.services import reexplication as rx

CTX = {"title": "Le retard", "speech": "…", "cycle": 1, "question": {"type": "qcm", "enonce": "M deux fois plus loin : τ…", "choix": ["reste", "double"], "bonne": 1},
       "reponses_fausses": "reste", "methodes_essayees": ["simulation"], "moments": {"m_atteint": 0.8, "m_revenu": 1.25}, "reperes": {"point_m": "le point M", "retard_tau": "le retard τ"}}


def test_le_prompt_change_d_entree_a_chaque_cycle_et_borne_les_gestes():
    p1, n1 = rx.prompt_reexplication(CTX)
    p3, n3 = rx.prompt_reexplication({**CTX, "cycle": 3})
    assert n1 == 1 and "SIMULATION" in p1 and "m_atteint" in p1 and "point_m" in p1 and "reponse_finale" not in p1
    assert n3 == 3 and "RÉPONSE" in p3 and "reponse_finale" in p3 and "cahier" in p3
    assert rx.prompt_reexplication({**CTX, "cycle": 9})[1] == 3


def test_les_gestes_inconnus_sont_ecartes_et_la_question_jumelle_validee():
    llm = json.dumps({"parole": "شوف", "ecrit": "τ = SM/v", "gestes": [{"commande": "play_until", "parametres": {"moment": "m_atteint"}}, {"repere": "retard_tau"}, {"repere": "inconnu"}, {"commande": "play_until", "parametres": {"moment": "nope"}}],
                      "question": {"type": "qcm", "enonce": "M trois fois plus loin : τ…", "choix": ["triple", "reste"], "bonne": 0, "explication": "τ = SM/v"}}, ensure_ascii=False)
    r = rx.reexplication_depuis(llm, CTX, 1)
    assert r["gestes"] == [{"commande": "play_until", "parametres": {"moment": "m_atteint"}}, {"repere": "retard_tau"}]
    assert r["question"]["type"] == "qcm" and r["dernier"] is False


def test_le_dernier_cycle_porte_la_reponse_finale():
    llm = json.dumps({"parole": "x", "gestes": [], "question": {"type": "vrai_faux", "enonce": "?", "affirmations": [{"texte": "τ double", "vrai": True}]},
                      "reponse_finale": "الجواب هو double", "cahier": "τ = SM / v : si SM double, τ double."})
    r = rx.reexplication_depuis(llm, {**CTX, "cycle": 3}, 3)
    assert r["dernier"] and r["reponse_finale"] == "الجواب هو double" and r["cahier"].startswith("τ")
    assert rx.reexplication_depuis('{"parole": "x"}', CTX, 1) is None
