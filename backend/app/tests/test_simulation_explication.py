"""Le professeur montre la simulation du doigt et réagit aux vérifications (simulation_explication)."""
from app.services import simulation_explication as se

MANIFESTE = {
    "id": "physics_waves_advanced_lab",
    "capabilities": {
        "commands": ["start", "set_variant", "fire_pulse", "check", "reset", "highlight"],
        "command_schema": {"highlight": {"target": "source | capteur_a"}},
        "reperes": {"source": "source S", "capteur_a": "capteur A", "capteur_b": "capteur B"},
        "explication": {
            "progressive": [
                {"repere": "source", "texte": "La source lance une impulsion."},
                {"repere": "capteur_a", "texte": "A note tA."},
            ],
            "cord": [{"repere": "source", "texte": "La source déforme la corde."}],
        },
    },
    "page_text": "Huit expériences.",
}


def test_le_doublon_du_manifeste_apporte_les_reperes_et_le_script():
    existant = {"id": "x", "capabilities": {"commands": ["start", "check"], "globals": ["executeAICommand"]}, "page_text": ""}
    assert se.fusionner_manifeste(existant, MANIFESTE) is True
    caps = existant["capabilities"]
    assert caps["reperes"]["capteur_a"] == "capteur A"
    assert caps["explication"]["progressive"][0]["repere"] == "source"
    assert "highlight" in caps["commands"] and "start" in caps["commands"]
    assert caps["command_schema"]["highlight"]["target"] == "source | capteur_a"
    assert existant["page_text"] == "Huit expériences."
    # Une seconde fois, rien de neuf.
    assert se.fusionner_manifeste(existant, MANIFESTE) is False


def test_le_script_suit_la_variante_courante():
    assert [p["repere"] for p in se.script_explication(MANIFESTE, "progressive")] == ["source", "capteur_a"]
    assert se.script_explication(MANIFESTE, "cord")[0]["texte"] == "La source déforme la corde."
    assert se.script_explication(MANIFESTE, "inconnue") == []
    plat = {"capabilities": {"explication": [{"repere": "a", "texte": "A"}, {"repere": "b", "texte": "B", "variante": "v2"}]}}
    assert [p["repere"] for p in se.script_explication(plat, "v1")] == ["a"]
    assert [p["repere"] for p in se.script_explication(plat, "v2")] == ["a", "b"]


def test_le_bloc_du_prompt_donne_les_reperes_le_script_et_la_regle_de_relance():
    bloc = se.bloc_prompt(MANIFESTE, "progressive")
    assert "capteur_a = capteur A" in bloc
    assert "1. [source] La source lance une impulsion." in bloc
    assert '"command": "highlight"' in bloc and '"target": "source"' in bloc
    assert "fire_pulse" in bloc, "le labo sait rejouer l'impulsion : c'est la commande de relance"
    assert "non de la tête" in bloc
    assert se.bloc_prompt({"capabilities": {}}, None) == ""


def test_la_relance_prend_la_commande_du_labo():
    assert se.commande_relance(MANIFESTE) == "fire_pulse"
    assert se.commande_relance({"capabilities": {"commands": ["start", "check"]}}) == "start"
    assert se.commande_relance({}) == "start"


def test_une_verification_ratee_donne_un_indice_puis_une_relance():
    orch: dict = {}
    etat = {"current_variant": "progressive", "correct": False}
    actions = [{"action": "fire_pulse"}, {"action": "check"}]
    assert se.decider_reaction(orch, etat, actions, maintenant=100.0) == "indice"
    # Le même état renvoyé une seconde fois ne fait rien.
    assert se.decider_reaction(orch, etat, actions, maintenant=101.0) is None
    actions.append({"action": "check"})
    # Trop tôt : le tuteur vient de parler.
    assert se.decider_reaction(orch, etat, actions, maintenant=104.0) is None
    actions.append({"action": "check"})
    assert se.decider_reaction(orch, etat, actions, maintenant=120.0) == "relance"
    assert se.nombre_echecs(orch, "progressive") == 3


def test_une_bonne_reponse_ne_declenche_rien_et_remet_les_echecs_a_zero():
    orch: dict = {}
    actions = [{"action": "check"}]
    assert se.decider_reaction(orch, {"current_variant": "cord", "correct": False}, actions, maintenant=0.0) == "indice"
    actions.append({"action": "check"})
    assert se.decider_reaction(orch, {"current_variant": "cord", "correct": True}, actions, maintenant=50.0) is None
    assert se.nombre_echecs(orch, "cord") == 0
    # Un état sans vérification (le labo tourne) est ignoré même s'il porte correct.
    assert se.decider_reaction(orch, {"correct": False}, [{"action": "step"}], maintenant=99.0) is None


def test_le_serveur_ne_reagit_pas_plus_de_trois_fois_par_variante():
    orch: dict = {}
    actions: list = []
    reactions = []
    for i in range(6):
        actions.append({"action": "check"})
        reactions.append(se.decider_reaction(orch, {"current_variant": "v", "correct": False}, list(actions), maintenant=i * 100.0))
    assert reactions == ["indice", "relance", "relance", None, None, None]


def test_le_prompt_de_reexplication_relance_et_pointe():
    ctx = {"subject": "Physique", "lesson_title": "Ondes"}
    p1 = se.prompt_reexplication(ctx, MANIFESTE, "progressive", {"correct": False}, echecs=1)
    assert "échec n°1" in p1 and "UN indice" in p1 and '"target": "source"' in p1 and "fire_pulse" not in p1
    p2 = se.prompt_reexplication(ctx, MANIFESTE, "progressive", {"correct": False}, echecs=2)
    assert '"command":"fire_pulse"' in p2 and "AUTREMENT" in p2
    p3 = se.prompt_reexplication(ctx, MANIFESTE, "progressive", {}, echecs=0, demande_eleve=True)
    assert "n'a pas compris" in p3 and '"command":"fire_pulse"' in p3


def test_l_eleve_qui_ne_comprend_pas_est_reconnu_en_francais_et_en_darija():
    assert se.eleve_ne_comprend_pas("je ne comprends pas le retard")
    assert se.eleve_ne_comprend_pas("j'ai pas compris")
    assert se.eleve_ne_comprend_pas("ما فهمت")
    assert se.eleve_ne_comprend_pas("mafhemtch")
    assert se.eleve_ne_comprend_pas("tu peux réexpliquer ?")
    assert not se.eleve_ne_comprend_pas("tau = 1,25 s")
    assert not se.eleve_ne_comprend_pas("je comprends mieux maintenant")
