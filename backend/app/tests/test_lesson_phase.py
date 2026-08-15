"""Les transitions de phase d'une leçon.

Le bug d'origine : le navigateur pouvait écrire n'importe quelle chaîne dans
la phase, et la progression des objectifs levait ensuite `ValueError` sur
`index()`. L'exception était avalée par un `except Exception` large, donc la
fin de leçon ne se déclenchait plus — sans erreur visible.
"""
import pytest

from app.services.lesson_phase import PHASES, PhaseLesson


def test_depart_par_defaut():
    assert PhaseLesson().courante == "activation"


def test_depart_inconnu_retombe_sur_la_premiere():
    """Jamais d'état invalide, même construit de travers."""
    assert PhaseLesson("n'importe quoi").courante == "activation"


def test_avancer_suit_l_ordre_pedagogique():
    p = PhaseLesson()
    vues = [p.courante]
    while p.avancer():
        vues.append(p.courante)
    assert tuple(vues) == PHASES


def test_avancer_s_arrete_a_la_derniere():
    p = PhaseLesson("consolidation")
    assert p.avancer() is False
    assert p.courante == "consolidation"


def test_viser_refuse_de_reculer():
    """Refaire une étape déjà terminée serait pris pour un bug par l'élève."""
    p = PhaseLesson("application")
    assert p.viser("exploration") is False
    assert p.courante == "application"


def test_viser_avance_bien():
    p = PhaseLesson("exploration")
    assert p.viser("application") is True
    assert p.courante == "application"


@pytest.mark.parametrize("valeur", ["", "banana", None, "Activation", 42])
def test_definir_refuse_les_valeurs_inconnues(valeur):
    """LE bug d'origine : ces valeurs étaient stockées telles quelles."""
    p = PhaseLesson("exploration")
    assert p.definir(valeur) is False
    assert p.courante == "exploration"


def test_definir_autorise_le_saut_explicite():
    """Une reprise de session peut légitimement revenir en arrière."""
    p = PhaseLesson("application")
    assert p.definir("activation") is True
    assert p.courante == "activation"


def test_le_mode_libre_n_a_pas_de_progression():
    p = PhaseLesson("libre")
    assert p.dans_la_progression is False
    assert p.avancer() is False
    assert p.viser("application") is False
    assert p.courante == "libre"


@pytest.mark.parametrize(
    "ratio,terminee,attendu",
    [
        (0.0, False, "exploration"),
        (0.20, False, "exploration"),
        (0.21, False, "explanation"),
        (0.70, False, "explanation"),
        (0.71, False, "application"),
        (1.0, False, "application"),
        (0.0, True, "consolidation"),
        (1.0, True, "consolidation"),
    ],
)
def test_bareme_d_avancement(ratio, terminee, attendu):
    assert PhaseLesson.pour_avancement(ratio, terminee) == attendu


def test_aucune_transition_ne_leve():
    """Le contrat central : cet état ne peut plus interrompre la session."""
    for depart in list(PHASES) + ["libre", "inconnu"]:
        p = PhaseLesson(depart)
        for valeur in ["", None, 0, "consolidation", "activation", object()]:
            p.definir(valeur)
            p.viser(valeur)
        p.avancer()
        assert p.courante in tuple(PHASES) + ("libre",)
