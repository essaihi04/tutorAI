"""Le briefing que le tuteur reçoit avant que l'élève ait parlé.

Le test qui compte vraiment est `test_le_budget_est_tenu...` : sans lui, le
briefing grossira à chaque service qui voudra ajouter « juste une info utile »,
et finira par noyer un prompt qui fait déjà 82 000 caractères.
"""
import pytest

from app.services.briefing_service import (
    BUDGET_CARACTERES,
    Donnees,
    composer,
    note_sur_20,
    _derniere_seance,
    _matieres_notees,
    _prochaine_seance,
)


# ── Le budget ─────────────────────────────────────────────────────

def test_le_budget_est_tenu_meme_avec_toutes_les_sources_bavardes():
    """La garde du module. Ne pas relâcher sans mesurer le prompt entier."""
    briefing = composer(
        Donnees(
            prenom="Abdelmounaim",
            filiere="2 Bac Sciences Mathématiques B",
            jours_avant_bac=291,
            matieres=[(f"Matière au nom interminable {i}", 42.0) for i in range(12)],
            lacune={
                "topic": "Limites et continuité des fonctions composées",
                "subject": "Mathématiques",
                "score": 21.0,
            },
            tendance="declining",
            derniere_seance="Nous avons vu " + "les dérivées successives, " * 40,
            prochaine_seance="Chapitre 7 " * 30,
        )
    )
    assert len(briefing.texte) <= BUDGET_CARACTERES


def test_ce_qui_deborde_est_coupe_par_la_fin():
    """L'identité survit toujours ; le planning est sacrifié en premier."""
    donnees = Donnees(
        prenom="Youssef",
        filiere="2 Bac SM",
        jours_avant_bac=96,
        matieres=[("Mathématiques", 65.0)],
        prochaine_seance="Suites numériques",
    )
    complet = composer(donnees)
    serre = composer(donnees, budget=40)

    assert "Youssef" in serre.texte
    assert "Suites numériques" not in serre.texte
    assert "Suites numériques" in complet.texte
    assert serre.coupe is True
    assert complet.coupe is False


def test_une_premiere_ligne_trop_longue_ne_vide_pas_le_briefing():
    briefing = composer(Donnees(prenom="Youssef", jours_avant_bac=96), budget=12)
    assert briefing.texte
    assert len(briefing.texte) <= 12
    assert briefing.coupe is True


# ── Le contenu ────────────────────────────────────────────────────

def test_un_eleve_sans_aucune_donnee_ne_produit_rien():
    """Un briefing vide vaut mieux qu'un squelette de phrases sans faits."""
    briefing = composer(Donnees())
    assert briefing.texte == ""
    assert not briefing


def test_le_nouvel_inscrit_est_presente_par_ses_matieres():
    briefing = composer(
        Donnees(
            prenom="Salma",
            jours_avant_bac=291,
            matieres_sans_donnees=["Mathématiques", "Physique"],
        )
    )
    assert "Salma" in briefing.texte
    assert "Aucun résultat encore" in briefing.texte
    assert "Mathématiques, Physique" in briefing.texte


def test_les_notes_sont_en_sur_20_comme_a_l_ecran():
    """Le tableau de bord affiche /20 : deux vocabulaires pour un même chiffre
    ferait douter l'élève de l'un des deux."""
    briefing = composer(Donnees(matieres=[("Mathématiques", 65.0)]))
    assert "Mathématiques 13/20" in briefing.texte
    assert "%" not in briefing.texte


def test_note_sur_20_reste_lisible():
    assert note_sur_20(100) == "20/20"
    assert note_sur_20(65) == "13/20"
    assert note_sur_20(62.5) == "12.5/20"
    assert note_sur_20(0) == "0/20"
    assert note_sur_20(None) == "0/20"


def test_la_tendance_stable_ne_dit_rien():
    """Une ligne qui n'apprend rien coûte du budget à celles qui apprennent."""
    assert "Tendance" not in composer(Donnees(prenom="Ali", tendance="stable")).texte
    assert "en baisse" in composer(Donnees(prenom="Ali", tendance="declining")).texte


def test_le_resume_de_la_derniere_seance_est_coupe_a_la_source():
    briefing = composer(
        Donnees(prenom="Ali", derniere_seance="Les dérivées. " * 50)
    )
    ligne = [s for s in briefing.sections if s.startswith("Dernière séance")][0]
    assert ligne.endswith("…")
    assert len(ligne) < 200


def test_aucun_conseil_pedagogique_dans_le_briefing():
    """Les stratégies (ZPD, Bloom, urgence) restent dans `adaptation_hints`.
    Les refaire ici, c'est reconstruire le prompt de 82 000 caractères."""
    briefing = composer(
        Donnees(
            prenom="Ali",
            jours_avant_bac=7,
            tendance="declining",
            lacune={"topic": "limites", "subject": "Maths", "score": 20.0},
        )
    )
    for mot in ("→", "Stratégie", "Propose", "URGENCE", "prérequis"):
        assert mot not in briefing.texte


# ── L'extraction ──────────────────────────────────────────────────

def test_une_matiere_a_deux_reponses_n_a_pas_de_note():
    """« Physique 4/20 » sur deux réponses est faux, et décourageant."""
    notees = _matieres_notees(
        {
            "subjects": {
                "Physique": {"score": 20.0, "total": 2},
                "Mathématiques": {"score": 65.0, "total": 12},
            }
        }
    )
    assert notees == [("Mathématiques", 65.0)]


def test_les_matieres_les_plus_faibles_passent_devant():
    notees = _matieres_notees(
        {
            "subjects": {
                "Mathématiques": {"score": 65.0, "total": 12},
                "Physique": {"score": 45.0, "total": 8},
                "SVT": {"score": 80.0, "total": 5},
            }
        }
    )
    assert [nom for nom, _ in notees] == ["Physique", "Mathématiques", "SVT"]


def test_derniere_seance_prend_le_resume_le_plus_recent():
    assert _derniere_seance(
        [
            {"last_ai_summary": "  ", "topics_covered": []},
            {"last_ai_summary": "Les limites en l'infini"},
            {"last_ai_summary": "Une séance plus ancienne"},
        ]
    ) == "Les limites en l'infini"


def test_derniere_seance_retombe_sur_les_sujets_couverts():
    assert _derniere_seance([{"topics_covered": ["Dérivées", "Tangentes"]}]) == (
        "Dérivées, Tangentes"
    )


def test_derniere_seance_sans_historique():
    assert _derniere_seance([]) == ""
    assert _derniere_seance(None) == ""


def test_prochaine_seance_ignore_ce_qui_est_deja_fait():
    seances = [
        {"status": "completed", "chapters": {"title_fr": "Suites"}},
        {
            "status": "pending",
            "chapters": {"title_fr": "Limites"},
            "subjects": {"name_fr": "Mathématiques"},
            "duration_minutes": 45,
        },
    ]
    assert _prochaine_seance(seances) == "Limites (Mathématiques, 45 min)"


def test_prochaine_seance_quand_tout_est_fait():
    assert _prochaine_seance([{"status": "completed", "chapters": {"title_fr": "x"}}]) == ""


def test_prochaine_seance_sans_titre_est_ignoree():
    """Une séance sans chapitre ni matière n'a rien à annoncer."""
    assert _prochaine_seance([{"status": "pending", "duration_minutes": 30}]) == ""


# ── L'exemple complet ─────────────────────────────────────────────

def test_le_briefing_type_d_un_eleve_reel():
    briefing = composer(
        Donnees(
            prenom="Youssef",
            filiere="2 Bac SM",
            jours_avant_bac=96,
            matieres=[("Physique", 45.0), ("Mathématiques", 65.0)],
            lacune={"topic": "limites", "subject": "Mathématiques", "score": 34.0},
            tendance="improving",
            derniere_seance="Dérivées : la définition est acquise, le calcul reste fragile.",
            prochaine_seance="Continuité (Mathématiques, 45 min)",
        )
    )
    assert len(briefing.texte) <= BUDGET_CARACTERES
    assert briefing.coupe is False
    assert briefing.texte.splitlines()[0] == "Youssef, 2 Bac SM. J-96 avant le BAC."
