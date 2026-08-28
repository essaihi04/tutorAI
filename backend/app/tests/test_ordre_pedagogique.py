"""Par quoi une séance COMMENCE.

L'ordre demandé est celui de ce que l'élève peut FAIRE : il manipule d'abord,
il répond ensuite, et le tableau conclut ce qu'il a vu. Le moteur de décision
faisait l'inverse au démarrage — l'ouverture d'une séance affichait une image
fixe, et les simulations du cours, rangées en phase ``exploration`` ou
``application``, n'arrivaient jamais dans la première minute.

Ces tests verrouillent les deux points qui décident vraiment : le support
retenu à chaque phase, et le fait qu'une simulation retenue s'OUVRE sans
attendre que l'élève la réclame — il ignore qu'elle existe.
"""

from app.services.resource_decision_service import ResourceDecisionService
from app.services.session_mode import ModeSession
from app.websockets.session_handler import SessionHandler


TOUT = ["image", "simulation", "video", "exam"]


def _decide(phase: str, disponibles=None, **extra):
    return ResourceDecisionService().decide(
        phase=phase,
        student_text=extra.pop("student_text", ""),
        lesson_title="Libération de l'énergie emmagasinée dans la matière organique",
        objective="Comparer respiration et fermentation",
        proficiency="intermédiaire",
        available_resource_types=TOUT if disponibles is None else disponibles,
        **extra,
    )


def test_la_seance_ouvre_sur_ce_qui_se_manipule():
    """La phase d'activation choisissait l'image : l'élève regardait avant
    d'avoir rien touché."""
    decision = _decide("activation")

    assert decision["resource_type_for_suggestion"] == "simulation"


def test_l_explication_commence_par_la_simulation_pas_par_le_tableau():
    """Le tableau CONCLUT ce que l'élève a vu ; il ne le précède pas."""
    decision = _decide("explanation")

    assert decision["resource_type_for_suggestion"] == "simulation"


def test_la_simulation_s_ouvre_sans_qu_on_la_demande():
    """Elle n'était présentée d'elle-même qu'en phase d'exploration, et
    seulement si l'élève avait prononcé « montre » ou « tester ». Il ne sait
    pas qu'une simulation existe : il ne la réclamera pas."""
    decision = _decide("activation", student_text="je comprends pas ce chapitre")

    assert decision["auto_present_resource"] is True


def test_une_simulation_deja_ouverte_ne_se_rouvre_pas():
    """La rouvrir remettrait à zéro ce que l'élève vient de régler."""
    decision = _decide("exploration", simulation_active=True)

    assert decision["auto_present_resource"] is False


def test_sans_simulation_dans_le_cours_on_descend_d_un_cran():
    """Le cran du dessous est ce qui se regarde : image ou schéma."""
    decision = _decide("activation", disponibles=["image", "video"])

    assert decision["resource_type_for_suggestion"] == "image"


def test_une_demande_explicite_reste_servie_telle_quelle():
    """« dessine-moi ça » demande le tableau, pas une simulation — l'ordre par
    défaut ne s'applique qu'à défaut de demande."""
    decision = _decide("explanation", student_text="dessine-moi le schéma au tableau")

    assert decision["explicit_draw_request"] is True
    assert decision["should_prepare_whiteboard"] is True


# ── Le filet du premier tour ──────────────────────────────────────────
#
# Le tag `OUVRIR_SIMULATION` est une consigne au modèle, et un modèle en
# oublie une : l'élève tombait alors sur un écran nu au tour qui décide s'il
# reste. Le serveur sait, lui, ce que la leçon contient.

def _handler(mode="cours", *, ressources=None, reprise=False) -> SessionHandler:
    handler = SessionHandler.__new__(SessionHandler)
    handler._mode = ModeSession(mode)
    handler.is_resumed_session = reprise
    handler.lesson_resources = [
        {"resource_type": t} for t in (["image", "simulation"] if ressources is None else ressources)
    ]
    return handler


def test_une_ouverture_sans_rien_de_manipulable_declenche_le_filet():
    assert _handler()._faut_ouvrir_la_simulation("Bonjour Zouhair ! On commence ?") is True


def test_une_ouverture_qui_a_deja_ouvert_la_simulation_ne_declenche_rien():
    ouverture = "Bonjour Zouhair ! OUVRIR_SIMULATION Regarde ce qui se passe sans oxygène."

    assert _handler()._faut_ouvrir_la_simulation(ouverture) is False


def test_une_figure_scientifique_compte_comme_ouverture():
    """Une scène posée en `<ui>` est manipulable : le filet n'a rien à ajouter."""
    ouverture = '<ui>{"actions":[{"type":"whiteboard","action":"show_live","payload":{"steps":[{"action":"figure","scientific":{}}]}}]}</ui>'

    assert _handler()._faut_ouvrir_la_simulation(ouverture) is False


def test_sans_simulation_dans_la_lecon_le_filet_ne_fabrique_rien():
    assert _handler(ressources=["image", "video"])._faut_ouvrir_la_simulation("Bonjour !") is False


def test_une_seance_reprise_garde_l_ecran_ou_l_eleve_l_avait_laisse():
    assert _handler(reprise=True)._faut_ouvrir_la_simulation("Bon retour !") is False


def test_la_question_libre_n_a_pas_de_lecon_a_ouvrir():
    assert _handler("libre")._faut_ouvrir_la_simulation("Salut ! Pose ta question.") is False
