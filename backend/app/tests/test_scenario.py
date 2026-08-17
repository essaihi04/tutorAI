"""La directive que le tuteur reçoit à chaque ouverture.

Le moteur de décision est déjà testé par son propre usage en production : ce
qui est vérifié ici, c'est la TRADUCTION — une décision devient une consigne
suivable et un mode que la session peut adopter, sans jamais inventer un
chapitre que le moteur n'a pas nommé.
"""
import pytest

from app.services.scenario_service import (
    BUDGET_CARACTERES,
    Directive,
    composer,
)
from app.services.session_mode import MODES, mode_pour_seance


def _decision(**extra):
    base = {
        "recommendation": "zpd_optimal",
        "subject": "Mathématiques",
        "topic": "Limites",
        "chapter_title": "Limites et continuité",
        "reason": "Score de 34% en Limites (Mathématiques).",
        "session_type": "exercices",
        "zpd_strategy": "Exercices progressifs avec étayage",
    }
    base.update(extra)
    return base


# ── Le budget ─────────────────────────────────────────────────────

def test_le_budget_est_tenu_meme_avec_un_moteur_bavard():
    directive = composer(
        _decision(
            reason="Erreur récurrente détectée : " + "échec consécutif, " * 60,
            zpd_strategy="Remédiation ciblée " * 30,
            topic="Un chapitre au nom particulièrement long " * 3,
        )
    )
    assert len(directive.texte) <= BUDGET_CARACTERES


def test_ce_qui_deborde_est_coupe_par_la_fin():
    """Ce qu'il faut travailler survit toujours ; la méthode part en premier."""
    serre = composer(_decision(), budget=60)
    assert "Limites" in serre.texte
    assert "Méthode" not in serre.texte


# ── La traduction en mode ─────────────────────────────────────────

def test_chaque_type_de_seance_donne_un_mode_connu():
    for session_type in ("cours", "revision", "lacunes", "exercices", "examen_blanc"):
        assert mode_pour_seance(session_type) in MODES


def test_un_type_de_seance_inconnu_donne_un_cours():
    """Le mode le moins risqué quand on ne sait pas : on explique."""
    assert mode_pour_seance("n'importe quoi") == "cours"
    assert mode_pour_seance(None) == "cours"


def test_reviser_c_est_expliquer_pas_tester():
    """L'élève qui a oublié n'a pas besoin qu'on le teste d'abord."""
    assert composer(_decision(session_type="revision")).mode == "cours"


def test_un_examen_blanc_passe_en_mode_examen():
    directive = composer(
        _decision(
            recommendation="exam_practice",
            session_type="examen_blanc",
            topic="Examen blanc",
        )
    )
    assert directive.mode == "examen"
    assert "chronomètre" in directive.texte


def test_des_exercices_passent_en_mode_exercice():
    assert composer(_decision(session_type="exercices")).mode == "exercice"


# ── Le contenu ────────────────────────────────────────────────────

def test_la_consigne_dit_quoi_faire_et_pourquoi():
    directive = composer(_decision())
    assert "Limites" in directive.texte
    assert "Mathématiques" in directive.texte
    assert "Pourquoi :" in directive.texte
    assert directive.recommandation == "zpd_optimal"


def test_chaque_recommandation_du_moteur_a_sa_consigne():
    """Une recommandation sans consigne laisserait le tuteur deviner comment
    s'y prendre — c'est exactement ce qu'on veut lui retirer."""
    for recommandation in (
        "erreur_recurrente",
        "lacune_critique",
        "zpd_optimal",
        "spaced_review",
        "plan_next",
        "exam_practice",
    ):
        directive = composer(_decision(recommendation=recommandation))
        assert directive.texte, recommandation
        assert len(directive.texte.splitlines()) >= 2, recommandation


def test_une_erreur_recurrente_est_traitee_des_le_debut():
    directive = composer(_decision(recommendation="erreur_recurrente", session_type="cours"))
    assert "DÈS LE DÉBUT" in directive.texte


# ── Les refus ─────────────────────────────────────────────────────

def test_sans_decision_pas_de_scenario():
    assert not composer(None)
    assert not composer({})
    assert composer(None).texte == ""


def test_sans_sujet_pas_de_scenario():
    """Une consigne qui dit « travaille » sans dire quoi ferait inventer le
    chapitre au modèle."""
    assert not composer(_decision(topic="", chapter_title=""))


def test_l_examen_blanc_n_a_pas_besoin_de_chapitre():
    """Seule exception : « entraîne-toi sur un sujet complet » se suffit."""
    directive = composer(
        _decision(recommendation="exam_practice", session_type="examen_blanc",
                  topic="", chapter_title="Entraînement BAC complet")
    )
    assert directive.texte


def test_une_decision_absurde_ne_casse_rien():
    directive = composer({"recommendation": 42, "topic": None, "session_type": []})
    assert isinstance(directive, Directive)
    assert directive.mode == "cours"
