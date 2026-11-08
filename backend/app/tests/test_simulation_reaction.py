"""Le tuteur réagit au résultat que l'élève a obtenu lui-même dans la simulation."""
import json

from app.services import simulation_reaction as sr


def test_le_type_de_question_suit_la_comprehension():
    assert sr.type_de_question([]) == "qcm"
    assert sr.type_de_question([{"type": "qcm", "correct": False}]) == "vrai_faux"
    assert sr.type_de_question([{"type": "qcm", "correct": True}]) == "directe"
    assert sr.type_de_question([{"type": "directe", "correct": True}]) == "qcm"


def test_le_prompt_compare_avant_et_apres_et_impose_les_regles_de_la_voix():
    prompt, genre = sr.prompt_interpretation({"title": "TP micros", "speech": "..."},
                                             {"parameters": {"d_m": 0.68}, "tau_ms": 2.0},
                                             {"parameters": {"d_m": 1.02}, "tau_ms": 3.0}, [])
    assert genre == "qcm" and "0.68" in prompt and "1.02" in prompt
    assert "jamais en chiffres" in prompt and "tashkil" in prompt and '"type": "qcm"' in prompt


def test_une_reaction_valide_est_gardee_et_nettoyee():
    llm = "```json\n" + json.dumps({
        "parole": "**مزيان**، بعدتي M deux.", "ecrit": "d passe à 1,02 m : τ = 3,0 ms.",
        "question": {"type": "qcm", "enonce": "Si d double, τ…", "choix": ["double", "reste", "diminue"], "bonne": 0, "explication": "τ = d / v"},
    }, ensure_ascii=False) + "\n```"
    r = sr.reaction_depuis(llm, "qcm")
    assert r["parole"] == "مزيان، بعدتي M deux." and r["question"]["bonne"] == 0 and len(r["question"]["choix"]) == 3


def test_une_reaction_bancale_est_refusee():
    assert sr.reaction_depuis("pas de json", "qcm") is None
    mauvais = json.dumps({"parole": "x", "question": {"type": "qcm", "enonce": "?", "choix": ["a"], "bonne": 3}})
    assert sr.reaction_depuis(mauvais, "qcm") is None
    sans_attendu = json.dumps({"parole": "x", "question": {"enonce": "Pourquoi ?"}})
    assert sr.reaction_depuis(sans_attendu, "directe") is None


def test_le_tashkil_est_retire_de_la_parole():
    assert sr.parole_propre("مَزْيان") == "مزيان"


def test_la_correction_d_une_reponse_directe():
    r = sr.correction_depuis('{"correct": false, "parole": "ماشي هي هادي", "ecrit": "τ double."}')
    assert r == {"correct": False, "parole": "ماشي هي هادي", "ecrit": "τ double."}
    assert sr.correction_depuis('{"parole": "x"}') is None
