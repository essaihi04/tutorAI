"""Le mode de session, et qui a le droit d'en changer.

Deux tests portent tout le reste :
`test_changer_de_mode_n_ecrit_jamais_la_phase` — la promesse « un seul
endroit » : revenir au cours après une digression doit rendre la leçon là où
elle était ;
`test_le_tuteur_ne_peut_pas_sortir_l_eleve_d_un_examen` — une épreuve
chronométrée ne s'annule pas sur une décision du modèle.
"""
import pytest

from app.services.lesson_phase import PhaseLesson
from app.services.session_mode import (
    LEGACY,
    MODES,
    ModeSession,
    lire_demande,
    normaliser,
    raison,
)
from app.services.tag_decoder import BALISES, extraire, retirer_balises


# ── Le vocabulaire ────────────────────────────────────────────────

def test_chaque_mode_a_une_valeur_historique():
    """La traduction vers `session_mode` est lue à ~30 endroits : un mode
    sans correspondance ferait un KeyError en pleine session."""
    assert set(LEGACY) == set(MODES)
    assert set(LEGACY.values()) <= {"coaching", "libre", "explain"}


def test_les_valeurs_historiques_font_l_aller_retour():
    """Le navigateur envoie encore 'coaching' / 'libre' / 'explain' à
    l'ouverture. Si la traduction retour n'était pas fidèle, ouvrir une
    question d'examen démarrerait un cours."""
    for ancien in ("coaching", "libre", "explain"):
        assert ModeSession(ancien).legacy == ancien


def test_les_mots_du_modele_sont_acceptes():
    """Refuser une quasi-bonne réponse laisse l'élève dans le mauvais écran."""
    assert normaliser("coaching") == "cours"
    assert normaliser("  EXAM ") == "examen"
    assert normaliser("libre") == "question"
    assert normaliser("entraînement") == "exercice"


def test_un_mot_inconnu_est_refuse_pas_stocke():
    assert normaliser("n'importe quoi") is None
    assert normaliser(None) is None
    assert normaliser({"mode": "cours"}) is None
    assert ModeSession("n'importe quoi").courant == "cours"


def test_les_trois_ecritures_du_modele_disent_la_meme_chose():
    assert lire_demande({"mode": "examen"}) == "examen"
    assert lire_demande({"mode": {"type": "examen"}}) == "examen"
    assert lire_demande("examen") == "examen"


def test_une_demande_sans_mode_lisible():
    assert lire_demande({}) is None
    assert lire_demande({"mode": "n'importe quoi"}) is None
    assert lire_demande(None) is None


def test_la_raison_est_recuperee_et_bornee():
    assert raison({"mode": "examen", "raison": "Tu es prêt."}) == "Tu es prêt."
    assert len(raison({"raison": "long " * 100})) <= 160
    assert raison({"mode": "examen"}) == ""


# ── L'arbitre ─────────────────────────────────────────────────────

def test_le_tuteur_change_de_mode():
    m = ModeSession()
    assert m.demander("examen") == "examen"
    assert m.courant == "examen"


def test_redemander_le_mode_courant_ne_bouge_rien():
    """None veut dire « ne préviens pas le navigateur » : annoncer un
    changement qui n'a pas eu lieu désynchroniserait l'écran."""
    m = ModeSession("cours")
    assert m.demander("cours") is None
    assert m.demander("coaching") is None


def test_une_demande_absurde_ne_change_pas_le_mode():
    m = ModeSession("cours")
    assert m.demander("mode ninja") is None
    assert m.courant == "cours"


def test_le_tuteur_ne_peut_pas_sortir_l_eleve_d_un_examen():
    """Un chrono tourne et une note est en jeu."""
    m = ModeSession("examen")
    assert m.demander("cours") is None
    assert m.demander("question") is None
    assert m.courant == "examen"


def test_l_eleve_sort_de_l_examen_quand_il_veut():
    """Jarvis obéit aussi : sinon le produit devient une prison."""
    m = ModeSession("examen")
    assert m.demander("cours", par="eleve") == "cours"
    assert m.courant == "cours"


def test_la_fin_de_l_epreuve_libere_la_session():
    """Sans cette sortie, la règle de l'examen enfermerait la session."""
    m = ModeSession("examen")
    assert m.terminer_examen() == "cours"
    assert m.courant == "cours"


def test_terminer_un_examen_qui_n_a_pas_lieu():
    m = ModeSession("cours")
    assert m.terminer_examen() is None
    assert m.courant == "cours"


def test_le_tuteur_peut_entrer_en_examen_depuis_partout():
    for depart in MODES:
        m = ModeSession(depart)
        if depart == "examen":
            continue
        assert m.demander("examen") == "examen"


# ── La promesse « un seul endroit » ───────────────────────────────

def test_changer_de_mode_n_ecrit_jamais_la_phase():
    """L'élève interrompt son cours pour une question, puis revient : la
    leçon doit reprendre exactement où elle était. C'est tout l'intérêt de
    ne plus changer de page."""
    phase = PhaseLesson("application")
    mode = ModeSession("cours")

    assert mode.demander("question") == "question"
    assert mode.demander("cours") == "cours"

    assert phase.courante == "application"


def test_les_parentheses_ne_font_pas_avancer_la_lecon():
    assert ModeSession("cours").dans_la_lecon is True
    assert ModeSession("exercice").dans_la_lecon is True
    assert ModeSession("examen").dans_la_lecon is False
    assert ModeSession("question").dans_la_lecon is False


def test_le_handler_lit_toujours_une_valeur_qu_il_connait():
    for mode in MODES:
        assert ModeSession(mode).legacy in ("coaching", "libre", "explain")


# ── La balise ─────────────────────────────────────────────────────

def test_la_balise_mode_existe_dans_le_vocabulaire():
    assert "mode" in BALISES


def test_la_balise_mode_est_decodee():
    texte = 'Bien. <mode>{"mode": "examen", "raison": "Tu es prêt."}</mode>'
    blocs = [b for b in extraire(texte) if b.balise == "mode"]
    assert len(blocs) == 1
    assert lire_demande(blocs[0].donnees) == "examen"
    assert raison(blocs[0].donnees) == "Tu es prêt."


def test_la_balise_mode_disparait_de_la_prose():
    """Le modèle imite tout ce qu'il voit dans l'historique : une commande
    laissée dans le texte se retrouve lue à voix haute à l'élève."""
    texte = 'On passe à la pratique. <mode>{"mode": "exercice"}</mode> Prêt ?'
    propre = retirer_balises(texte)
    assert "mode" not in propre
    assert "{" not in propre
    assert "On passe à la pratique." in propre


def test_une_balise_mode_coupee_ne_fuit_pas_dans_le_chat():
    """Flux interrompu, max_tokens atteint : un demi-JSON ne doit pas partir
    à l'élève."""
    propre = retirer_balises('Très bien. <mode>{"mode": "exam')
    assert propre.strip() == "Très bien."


def test_un_json_illisible_ne_change_pas_le_mode():
    blocs = extraire('<mode>{"mode": pas du json</mode>')
    assert blocs[0].donnees is None
    assert ModeSession("cours").demander(lire_demande(blocs[0].donnees)) is None
