"""Voix ↔ simulation : ce que dit le professeur se voit, la baguette va sur l'objet nommé (17 novembre 2026).

Le contrôle est `backend/scripts/verifier_pointage_simulations.py` ; il est rejoué ici sur un cours inventé (il doit
repérer chaque défaut) puis sur le cours de SVT « Libération de l'énergie », qui doit être sans écart.
"""
import importlib.util
import json
import sys
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "verifier_pointage_simulations.py"
_spec = importlib.util.spec_from_file_location("verifier_pointage_simulations", SCRIPT)
vp = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = vp            # les dataclasses du script cherchent leur module ici
_spec.loader.exec_module(vp)

URL = "/media/simulations/svt/reactions_responsables_liberation_energie-tableau/chaine.html"


def _cours(*diapos):
    return {"activities": [{"slides": list(diapos)}]}


def _diapo(ident, parole, pointage, url=URL + "?depart=0", demarrer="reset"):
    return {"id": ident, "visual": {"kind": "simulation", "url": url},
            "speech_text": {"mixed": parole}, "audio": {"mixed": {"duration_ms": 30000}},
            "concentration": {"pointage": pointage, "demarrer": demarrer}}


def test_la_baguette_sur_un_voisin_est_signalee():
    parole = "شوف: طيح deux protons فla matrice، و deux électrons فT un. " + "هادي جملة طويلة باش يكون الوقت. " * 6
    r = vp.verifier(_cours(_diapo("d", parole, [
        {"mot": "شوف: طيح deux", "commande": "play_until", "parametres": {"moment": "taxi_decharge"}},
        {"mot": "و deux électrons", "repere": "sphere"},
    ])))
    assert any("REPERE" in e and "sphere" in e for e in r.ecarts)


def test_un_processus_dit_sans_animation_est_signale():
    parole = "شوف: جا N A D H, H plus من la matrice، ووقف عند T un. " + "هادي جملة طويلة باش يكون الوقت. " * 6
    r = vp.verifier(_cours(_diapo("d", parole, [{"mot": "ووقف عند T un", "repere": "t1"}])))
    assert any("PROCESSUS" in e and "taxi_arrive" in e for e in r.ecarts)
    assert not any("REPERE" in e for e in r.ecarts)


def test_meme_url_et_depart_libre_sont_signales():
    parole = "شوف: جا N A D H, H plus من la matrice. " + "هادي جملة طويلة باش يكون الوقت. " * 6
    pt = [{"mot": "شوف: جا N", "commande": "play_until", "parametres": {"moment": "taxi_arrive"}}]
    r = vp.verifier(_cours(_diapo("a", parole, pt, url=URL, demarrer="start"), _diapo("b", parole, pt, url=URL, demarrer="start")))
    assert any(e.startswith("b IFRAME") for e in r.ecarts)
    assert any(e.startswith("a DEPART") for e in r.ecarts)


def test_un_moment_absent_de_la_simulation_est_signale():
    parole = "شوف: جا N A D H, H plus من la matrice. " + "هادي جملة طويلة باش يكون الوقت. " * 6
    r = vp.verifier(_cours(_diapo("d", parole, [{"mot": "شوف: جا N", "commande": "play_until", "parametres": {"moment": "moment_imaginaire"}}])))
    assert any("MOMENT" in e for e in r.ecarts)


def test_le_cours_de_svt_liberation_de_l_energie_est_sans_ecart():
    cours = json.loads(vp.COURS_DEFAUT.read_text(encoding="utf-8"))
    r = vp.verifier(cours)
    assert r.ecarts == []
