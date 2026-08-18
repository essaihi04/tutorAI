"""La balise <mode> une fois branchée sur la session.

`test_session_mode.py` couvre l'arbitre seul. Ici on vérifie les deux
jonctions qui ne se voient pas en le lisant : les ~30 lectures historiques de
`session_mode` continuent de recevoir 'coaching' / 'libre' / 'explain', et le
navigateur n'est prévenu QUE lorsque la session a réellement changé d'état.
"""
import asyncio

from app.services.session_mode import ModeSession
from app.websockets.session_handler import SessionHandler


class FauxWebSocket:
    """On ne teste pas le transport : on regarde ce qui part."""

    def __init__(self):
        self.envoyes: list[dict] = []

    async def send_json(self, message: dict):
        self.envoyes.append(message)


def _handler() -> SessionHandler:
    """Un handler réduit à ce que ces tests exercent.

    Les attributs posés ici sont ceux que `__init__` garantit toujours en
    production : les omettre ferait échouer les tests pour une raison qui
    n'existe pas dans l'application.
    """
    from app.services.lesson_phase import PhaseLesson
    from app.services.scenario_service import Alternance, Progression
    from app.services.teaching_tactics import BanditTactiques

    handler = SessionHandler.__new__(SessionHandler)
    handler.websocket = FauxWebSocket()
    handler._mode = ModeSession("cours")
    handler._phase = PhaseLesson("application")
    handler.scenario = ""
    handler.scenario_sujet = ""
    handler._progression = Progression("cours")
    handler._alternance = Alternance()
    handler._bandit = BanditTactiques()
    handler._tactique_en_cours = None
    handler._tactique_echouee = None
    return handler


def _modes_annonces(handler) -> list[str]:
    return [m["mode"] for m in handler.websocket.envoyes if m["type"] == "mode_changed"]


# ── Lecture humaine des tours courts ──────────────────────────────

def test_un_commande_passe_fait_avancer_sans_recommencer():
    guidance = SessionHandler._build_turn_guidance("passe")
    assert "passer à la suite" in guidance
    assert "ne répète pas" in guidance


def test_un_eleve_qui_signale_le_tableau_n_est_plus_reinvite_a_ecrire():
    guidance = SessionHandler._build_turn_guidance("راك كتبتيها")
    assert "déjà écrite" in guidance
    assert "ne lui demande pas de recopier" in guidance


def test_une_question_directe_passe_avant_le_quiz():
    guidance = SessionHandler._build_turn_guidance("شنو هو H3O+؟")
    assert "question directe" in guidance
    assert "Réponds d'abord" in guidance


# ── La traduction vers le code existant ───────────────────────────

def test_les_lectures_historiques_voient_toujours_leurs_valeurs():
    handler = _handler()
    assert handler.session_mode == "coaching"

    handler._mode.demander("question")
    assert handler.session_mode == "libre"

    handler._mode.demander("examen")
    assert handler.session_mode == "explain"


def test_une_ecriture_en_cours_de_seance_ne_defait_pas_le_choix_du_tuteur():
    """La propriété protège les écritures pendant la séance : « coaching »
    ne doit pas ramener à « cours » un élève mis en « exercice ».

    L'ouverture d'une session est un cas à part — `_init_session` reconstruit
    un `ModeSession` neuf, pour ne pas hériter de la séance précédente."""
    handler = _handler()
    handler._mode.demander("exercice")

    handler.session_mode = "coaching"

    assert handler._mode.courant == "exercice"
    assert ModeSession("coaching").courant == "cours"


# ── Ce qui part vers le navigateur ────────────────────────────────

def test_une_balise_valide_change_le_mode_et_previent_l_ecran():
    handler = _handler()
    nouveau = asyncio.run(handler._appliquer_mode_demande(
        'On passe à la pratique. <mode>{"mode":"exercice","raison":"Tu as compris."}</mode>'
    ))

    assert nouveau == "exercice"
    assert handler._mode.courant == "exercice"
    envoye = handler.websocket.envoyes[-1]
    assert envoye["type"] == "mode_changed"
    assert envoye["previous"] == "cours"
    assert envoye["reason"] == "Tu as compris."


def test_une_reponse_sans_balise_ne_previent_personne():
    """Le cas NORMAL : neuf réponses sur dix ne changent rien."""
    handler = _handler()
    assert asyncio.run(handler._appliquer_mode_demande("Très bien, continuons.")) is None
    assert handler.websocket.envoyes == []


def test_un_refus_ne_fait_pas_basculer_l_ecran():
    """Annoncer un changement que la session a refusé désynchroniserait
    l'écran de l'état réel."""
    handler = _handler()
    handler._mode.demander("examen")

    assert asyncio.run(handler._appliquer_mode_demande('<mode>{"mode":"cours"}</mode>')) is None
    assert handler._mode.courant == "examen"
    assert _modes_annonces(handler) == []


def test_un_json_casse_laisse_la_session_intacte():
    handler = _handler()
    assert asyncio.run(handler._appliquer_mode_demande('<mode>{"mode": tronq')) is None
    assert handler._mode.courant == "cours"
    assert handler.websocket.envoyes == []


def test_le_dernier_bloc_gagne():
    """Si le modèle se ravise dans la même réponse, c'est sa conclusion qui
    compte."""
    handler = _handler()
    nouveau = asyncio.run(handler._appliquer_mode_demande(
        '<mode>{"mode":"question"}</mode> ... en fait <mode>{"mode":"examen"}</mode>'
    ))
    assert nouveau == "examen"
    assert _modes_annonces(handler) == ["examen"]


def test_la_lecon_garde_sa_place_a_travers_une_digression():
    """La promesse « un seul endroit », vue depuis la session : l'élève part
    poser une question et revient sans avoir perdu son cours."""
    handler = _handler()

    asyncio.run(handler._appliquer_mode_demande('<mode>{"mode":"question"}</mode>'))
    asyncio.run(handler._appliquer_mode_demande('<mode>{"mode":"cours"}</mode>'))

    assert handler.current_phase == "application"
    assert _modes_annonces(handler) == ["question", "cours"]
    assert all(m["phase"] == "application" for m in handler.websocket.envoyes)


# ── Les critères de sortie, une fois branchés ─────────────────────

from app.services.scenario_service import Progression


def _handler_en_seance(mode="cours") -> SessionHandler:
    handler = _handler()
    handler._mode = ModeSession(mode)
    handler._progression = Progression(mode)
    handler.scenario = "À travailler maintenant : les limites (Maths)."
    handler.scenario_sujet = "les limites (Maths)"
    return handler


def test_deux_reussites_font_avancer_la_seance_pour_de_vrai():
    handler = _handler_en_seance("cours")

    assert asyncio.run(handler._enregistrer_preuve(True)) is None
    assert asyncio.run(handler._enregistrer_preuve(True)) == "exercice"

    assert handler._mode.courant == "exercice"
    assert _modes_annonces(handler) == ["exercice"]
    assert handler.websocket.envoyes[-1]["reason"]


def test_la_consigne_est_reecrite_apres_une_etape():
    """Laisser le scénario d'ouverture ferait redémarrer le tuteur sur une
    étape déjà franchie."""
    handler = _handler_en_seance("cours")
    asyncio.run(handler._enregistrer_preuve(True))
    asyncio.run(handler._enregistrer_preuve(True))

    assert "exercices" in handler.scenario
    assert "les limites (Maths)" in handler.scenario


def test_une_reponse_ordinaire_ne_previent_personne():
    """Le cas normal : la plupart des réponses ne changent rien."""
    handler = _handler_en_seance("exercice")
    assert asyncio.run(handler._enregistrer_preuve(True)) is None
    assert handler.websocket.envoyes == []


def test_une_reussite_en_examen_ne_sort_pas_de_l_epreuve():
    """La règle du chrono tient aussi face aux preuves."""
    handler = _handler_en_seance("examen")
    for _ in range(5):
        assert asyncio.run(handler._enregistrer_preuve(True)) is None
    assert handler._mode.courant == "examen"
    assert handler.websocket.envoyes == []


def test_la_progression_reste_alignee_sur_la_session_apres_un_refus():
    """Si la session refuse la transition, la progression ne doit pas
    continuer à compter depuis un état imaginaire."""
    handler = _handler_en_seance("examen")
    handler._progression = Progression("exercice")   # désaccord volontaire

    asyncio.run(handler._enregistrer_preuve(False))
    asyncio.run(handler._enregistrer_preuve(False))   # exercice → cours, refusé

    assert handler._mode.courant == "examen"
    assert handler._progression.mode == "examen"
    assert handler.websocket.envoyes == []


def test_deux_echecs_ramenent_au_cours_et_le_disent():
    handler = _handler_en_seance("exercice")
    asyncio.run(handler._enregistrer_preuve(False))
    assert asyncio.run(handler._enregistrer_preuve(False)) == "cours"

    assert "autrement" in handler.scenario
    assert handler.websocket.envoyes[-1]["reason"]


def test_un_changement_par_balise_remet_les_compteurs_a_zero():
    """Sans ça, les réussites accumulées avant la bascule feraient franchir
    l'étape suivante immédiatement."""
    handler = _handler_en_seance("cours")
    asyncio.run(handler._enregistrer_preuve(True))    # 1 réussite en cours

    asyncio.run(handler._appliquer_mode_demande('<mode>{"mode":"exercice"}</mode>'))

    assert handler._progression.mode == "exercice"
    assert handler._progression.reussites == 0


def test_la_lecon_garde_sa_phase_a_travers_les_etapes():
    handler = _handler_en_seance("cours")
    asyncio.run(handler._enregistrer_preuve(True))
    asyncio.run(handler._enregistrer_preuve(True))
    assert handler.current_phase == "application"


# ── L'alternance, une fois branchée ───────────────────────────────

from app.services.scenario_service import Alternance


def test_l_alternance_fait_tourner_le_sujet_des_exercices():
    handler = _handler_en_seance("exercice")
    handler.scenario_sujet = "Limites"
    handler._alternance = Alternance("Limites", ["Dérivées"])

    # Deux réussites puis un échec : trois exercices, mais aucun critère de
    # sortie franchi. L'alternance est donc seule à agir.
    for resultat in (True, True, False):
        assert asyncio.run(handler._enregistrer_preuve(resultat)) is None

    assert handler._mode.courant == "exercice"
    assert handler.scenario_sujet == "Dérivées"
    assert "Dérivées" in handler.scenario


def test_on_n_alterne_pas_pendant_une_explication():
    """Alterner pendant qu'on installe une notion l'empêche au lieu de la
    consolider."""
    handler = _handler_en_seance("cours")
    handler.scenario_sujet = "Limites"
    handler._alternance = Alternance("Limites", ["Dérivées"])

    asyncio.run(handler._enregistrer_preuve(False))
    asyncio.run(handler._enregistrer_preuve(False))

    assert handler.scenario_sujet == "Limites"


def test_changer_de_sujet_ne_reprend_pas_la_serie_de_l_eleve():
    """Lui retirer ses réussites parce que le tuteur a change d'exercice
    serait une punition sans motif."""
    handler = _handler_en_seance("exercice")
    handler._alternance = Alternance("Limites", ["Dérivées"])

    asyncio.run(handler._enregistrer_preuve(True))
    asyncio.run(handler._enregistrer_preuve(True))
    assert handler._progression.reussites == 2

    # Le 3e exercice declenche l'alternance ET la 3e reussite : l'etape
    # doit quand meme etre franchie.
    assert asyncio.run(handler._enregistrer_preuve(True)) == "examen"


def test_la_regle_du_cahier_accompagne_chaque_etape():
    handler = _handler_en_seance("cours")
    asyncio.run(handler._enregistrer_preuve(True))
    asyncio.run(handler._enregistrer_preuve(True))
    assert "ATTENDS" in handler.scenario


def test_la_preuve_est_creditee_au_sujet_travaille_pas_au_suivant():
    """L'alternance change le sujet du PROCHAIN exercice. Créditer la réponse
    qui vient d'arriver au nouveau sujet ferait progresser l'élève sur un
    chapitre qu'il n'a pas encore vu."""
    handler = _handler_en_seance("exercice")
    handler.scenario_sujet = "Limites"
    handler._progression = Progression("exercice", "Limites")
    handler._alternance = Alternance("Limites", ["Dérivées"])

    for resultat in (True, True, False):
        asyncio.run(handler._enregistrer_preuve(resultat))

    assert handler.scenario_sujet == "Dérivées"
    assert handler._progression.sujet == "Dérivées"
    # Les trois réponses sont allées sur Limites, pas sur Dérivées.
    assert handler._progression.suivi.pour("Limites", "exercice").observations == 3
    assert handler._progression.suivi.pour("Dérivées", "exercice").observations == 0


def test_la_maitrise_survit_a_un_aller_retour_de_mode():
    """Ce que l'élève a prouvé en cours reste vrai quand il y revient."""
    handler = _handler_en_seance("cours")
    handler.scenario_sujet = "Limites"
    handler._progression = Progression("cours", "Limites")

    asyncio.run(handler._enregistrer_preuve(True))
    acquis = handler._progression.suivi.pour("Limites", "cours").p

    asyncio.run(handler._appliquer_mode_demande('<mode>{"mode":"question"}</mode>'))
    asyncio.run(handler._appliquer_mode_demande('<mode>{"mode":"cours"}</mode>'))

    assert handler._progression.maitrise == acquis


# ── Le bandit de tactiques, une fois branché ──────────────────────

from app.services.teaching_tactics import BanditTactiques, lire_tactique


def test_la_tactique_entre_dans_la_consigne_du_cours():
    handler = _handler_en_seance("cours")
    handler._bandit = BanditTactiques()
    handler._adopter_consigne("cours")

    assert handler._tactique_en_cours is not None
    assert len(handler.scenario.splitlines()) >= 4


def test_aucune_tactique_pendant_les_exercices():
    """Imposer une forme de raisonnement pendant qu'il cherche reviendrait à
    lui souffler la méthode qu'on lui demande de choisir."""
    handler = _handler_en_seance("exercice")
    handler._bandit = BanditTactiques()
    handler._adopter_consigne("exercice")

    assert handler._tactique_en_cours is None


def test_la_reponse_suivante_note_la_tactique():
    handler = _handler_en_seance("cours")
    handler._bandit = BanditTactiques()
    handler._adopter_consigne("cours")
    employee = handler._tactique_en_cours

    asyncio.run(handler._enregistrer_preuve(True))

    assert handler._bandit.classement() == [(employee, 1, 1)]
    assert handler._tactique_en_cours is None


def test_une_tactique_qui_echoue_n_est_pas_rejouee_telle_quelle():
    handler = _handler_en_seance("cours")
    handler._bandit = BanditTactiques()
    handler._adopter_consigne("cours")
    ratee = handler._tactique_en_cours

    asyncio.run(handler._enregistrer_preuve(False))
    assert handler._tactique_echouee == ratee

    handler._adopter_consigne("cours")
    assert handler._tactique_en_cours != ratee


def test_une_reussite_libere_la_tactique():
    """Elle a marché : rien n'interdit de la reprendre."""
    handler = _handler_en_seance("cours")
    handler._bandit = BanditTactiques()
    handler._adopter_consigne("cours")

    asyncio.run(handler._enregistrer_preuve(True))
    assert handler._tactique_echouee is None


def test_une_tactique_n_est_notee_qu_une_fois():
    """Sans remise à zéro, une seule explication serait créditée par toutes
    les réponses qui suivent."""
    handler = _handler_en_seance("cours")
    handler._bandit = BanditTactiques()
    handler._adopter_consigne("cours")

    asyncio.run(handler._enregistrer_preuve(True))
    asyncio.run(handler._enregistrer_preuve(True))

    assert handler._bandit.total_essais == 1


def test_la_tactique_voyage_avec_la_reponse_enregistree():
    """C'est ce qui permet au bandit de renaître à la séance suivante."""
    from app.services.teaching_tactics import marquer_source

    marquee = marquer_source("chat_coaching", "analogie")
    assert lire_tactique(marquee) == "analogie"
