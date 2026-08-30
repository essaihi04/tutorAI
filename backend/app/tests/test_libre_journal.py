"""Ce que le journal du mode libre doit savoir dire.

Il existe pour une question et une seule : quand l'élève dit « ça ne marche
toujours pas », le tuteur a-t-il ignoré une ressource, ou n'y en avait-il
aucune ? Sans lui, il n'y a rien à regarder — la conversation n'est stockée
nulle part, et les deux autres journaux ne notent que ce qui a manqué.

Chaque test verrouille l'un des trois défauts qu'il doit rendre visibles, plus
le cas normal, qui ne doit RIEN signaler : un journal qui crie à chaque tour
ne se lit plus.
"""
import asyncio

from app.services import libre_journal
from app.services.session_mode import ModeSession
from app.websockets.session_handler import SessionHandler


def _tour(demande, actions, reponse="D'accord.", carte=None, route=None):
    """Un tour complet : l'offre, puis l'envoi, comme en séance."""
    libre_journal.retenir_offre(
        "eleve-test",
        demande,
        carte if carte is not None else {"reference": ("svt_glycolyse", 4)},
        route if route is not None else {"source": "schema", "engine": None},
    )
    return libre_journal.noter_tour("eleve-test", reponse, actions)


# ── Les trois défauts ─────────────────────────────────────────────────

def test_une_ressource_offerte_et_non_envoyee_est_signalee():
    """Le défaut qui a motivé tout le câblage de la bibliothèque : elle
    couvrait la notion, et le tuteur a répondu en prose."""
    ligne = _tour("c'est quoi la glycolyse", actions=[])

    assert ligne["ressource_ignoree"] is True


def test_un_tableau_promis_sans_bloc_est_signale():
    """« شوف le tableau » sans bloc : l'élève regarde un écran vide et croit
    que son application est cassée. Il ne peut pas savoir d'où ça vient."""
    ligne = _tour(
        "c'est quoi la glycolyse",
        actions=[],
        reponse="شوف le tableau، كتبت ليك les trois etapes.",
    )

    assert ligne["promesse_non_tenue"] is True


def test_la_promesse_se_reconnait_aussi_en_francais():
    ligne = _tour("explique", actions=[], reponse="Je vais te dessiner le cycle.")

    assert ligne["promesse_non_tenue"] is True


def test_je_vais_lancer_une_scene_est_journalise_comme_promesse():
    ligne = _tour(
        "explique la propagation d'une onde",
        actions=[],
        reponse="Je vais lancer une scène animée. Regarde comment l'onde avance.",
    )

    assert ligne["promesse_non_tenue"] is True


def test_un_identifiant_invente_est_signale():
    """Le modèle nomme un schéma qui n'existe pas : rien ne s'affiche, et le
    serveur n'en disait rien non plus."""
    ligne = _tour(
        "c'est quoi la glycolyse",
        actions=[{"action": "show_schema", "schema_id": "svt_glycolyse_v2"}],
    )

    assert ligne["identifiants_inconnus"] == ["svt_glycolyse_v2"]


# ── Le cas normal ─────────────────────────────────────────────────────

def test_un_tour_correct_ne_signale_rien():
    ligne = _tour(
        "c'est quoi la glycolyse",
        actions=[{"action": "show_schema", "schema_id": "svt_glycolyse"}],
        reponse="Regarde le tableau.",
    )

    assert ligne["envoi"]["schemas"] == ["svt_glycolyse"]
    assert ligne["ressource_ignoree"] is False
    assert ligne["promesse_non_tenue"] is False
    assert ligne["identifiants_inconnus"] == []


def test_rien_a_offrir_n_est_pas_une_ressource_ignoree():
    """Répondre en texte quand la bibliothèque ne couvre pas la notion est
    exactement ce qu'il faut faire. Le signaler noierait les vrais défauts."""
    ligne = _tour("parle-moi du bac", actions=[], carte={})

    assert ligne["ressource_ignoree"] is False


# ── La lecture des envois ─────────────────────────────────────────────

def test_une_scene_animee_cachee_dans_une_ligne_de_tableau_est_vue():
    """Une figure de moteur voyage dans `show_board`, dans `show_live` ou
    seule. La chercher à un seul endroit ferait passer un tour réussi pour un
    tour muet — et le journal accuserait le tuteur à tort."""
    ligne = _tour(
        "montre le cycle ATP",
        actions=[{
            "action": "show_board",
            "payload": {"lines": [
                {"type": "text", "content": "Le cycle"},
                {"type": "scientific", "scientific": {
                    "engine": "preset", "presetId": "svt_ch1_cycle_atp",
                }},
            ]},
        }],
    )

    assert ligne["envoi"]["presets"] == ["svt_ch1_cycle_atp"]
    assert ligne["envoi"]["moteurs"] == ["preset"]
    assert ligne["ressource_ignoree"] is False


def test_une_figure_posee_dans_un_pas_de_show_live_est_vue():
    ligne = _tour(
        "trace la courbe",
        actions=[{
            "action": "show_live",
            "payload": {"steps": [
                {"action": "write", "line": {"type": "title", "content": "Courbe"}},
                {"action": "figure", "scientific": {"engine": "jsxgraph", "elements": []}},
            ]},
        }],
    )

    assert ligne["envoi"]["moteurs"] == ["jsxgraph"]


def test_le_bilan_compte_les_defauts_sans_rejouer_la_seance():
    """« Est-ce toujours le même problème ? » doit se répondre par un nombre,
    pas par une impression."""
    avant = libre_journal.bilan()["defauts"].get("ressource_ignoree", 0)
    _tour("c'est quoi la glycolyse", actions=[])

    assert libre_journal.bilan()["defauts"]["ressource_ignoree"] == avant + 1


def test_une_offre_sans_reponse_ne_bloque_pas_la_suivante():
    """Une session qui se ferme au milieu d'un tour laisse son offre derrière
    elle. La suivante ne doit pas hériter de la précédente."""
    libre_journal.retenir_offre(
        "eleve-abandon", "la mitochondrie",
        {"reference": ("svt_mitochondrie_structure", 4)},
        {"source": "schema"},
    )
    ligne = _tour("autre chose", actions=[])

    assert ligne["demande"] == "autre chose"


def test_le_journal_n_interrompt_jamais_une_seance():
    """Une trace ne vaut pas une séance : une entrée absurde rend None au
    lieu de lever, et l'élève ne voit rien passer."""
    assert libre_journal.noter_tour("inconnu", None, "pas une liste") is not None


def test_un_geste_qui_n_ouvre_rien_ne_compte_pas_comme_un_envoi():
    """Le cas mesuré en séance, et le pire pour un journal : il le taisait.

    Le tuteur emet un `media/open` alors que la table des ressources est
    vide. Le serveur repond « aucune ressource ouverte », l'ecran de l'eleve
    ne bouge pas — et le journal declarait le tour servi parce qu'un geste
    avait eu lieu. Quatre ressources proposees, rien montre, aucun defaut
    signale.
    """
    ligne = _tour(
        "explique-moi la respiration cellulaire",
        actions=[{"type": "media", "action": "open"}],
    )

    assert ligne["ressource_ignoree"] is True


def test_un_geste_qui_ecrit_au_tableau_compte_bien_comme_un_envoi():
    """La reserve de la regle precedente : `show_live` montre vraiment
    quelque chose, meme sans identifiant de bibliotheque."""
    ligne = _tour(
        "explique-moi la respiration cellulaire",
        actions=[{"action": "show_live", "payload": {"steps": [
            {"action": "write", "line": {"type": "title", "content": "Respiration"}},
        ]}}],
    )

    assert ligne["ressource_ignoree"] is False


def test_le_handler_journalise_aussi_une_reponse_sans_bloc_ui(monkeypatch):
    """Le point d'accroche ne doit plus vivre à l'intérieur de `if ui_blocks`."""
    appels = []

    class FauxWebSocket:
        async def send_json(self, _message):
            return None

    handler = SessionHandler(FauxWebSocket(), "eleve-prose")
    handler._mode = ModeSession("libre")
    monkeypatch.setattr(
        libre_journal,
        "noter_tour",
        lambda *args, **kwargs: appels.append((args, kwargs)),
    )

    asyncio.run(handler._execute_ai_commands("Une réponse purement orale."))

    assert len(appels) == 1
    assert appels[0][0][2] == []
