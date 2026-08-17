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


# ── Les critères de sortie ────────────────────────────────────────

from app.services.scenario_service import CRITERES, Progression, consigne_de_mode


def _suite(progression, resultats):
    """Joue une suite de réponses et renvoie les transitions déclenchées."""
    return [t for r in resultats if (t := progression.enregistrer(r))]


def test_deux_reussites_font_passer_du_cours_a_l_exercice():
    p = Progression("cours")
    assert p.enregistrer(True) is None
    transition = p.enregistrer(True)
    assert transition.mode == "exercice"
    assert transition.raison


def test_trois_reussites_font_passer_de_l_exercice_a_l_examen():
    p = Progression("exercice")
    assert _suite(p, [True, True]) == []
    assert p.enregistrer(True).mode == "examen"


def test_un_eleve_qui_alterne_au_hasard_ne_passe_pas_en_examen():
    """Répondre juste une fois sur deux n'est pas maîtriser. C'était la
    raison d'être de la règle « consécutive » ; le modèle la conserve, mais
    sans son effet de bord."""
    p = Progression("exercice")
    assert _suite(p, [True, False] * 5) == []
    assert p.mode == "exercice"


def test_une_erreur_precoce_n_efface_plus_quatre_reussites():
    """Ce que le comptage consécutif ratait : il remettait tout à zéro au
    premier faux pas, donc quatre réussites sur cinq ne valaient rien. Le
    crédit est maintenant GRADUÉ — c'est le gain du modèle, pas un
    relâchement."""
    p = Progression("exercice")
    transitions = _suite(p, [True, True, False, True, True])
    assert [t.mode for t in transitions] == ["examen"]


def test_la_maitrise_estimee_est_lisible():
    """Le modèle doit rester inspectable : quand il se trompe, on veut
    pouvoir lire pourquoi."""
    p = Progression("exercice")
    assert p.maitrise == pytest.approx(0.25)
    p.enregistrer(True)
    assert 0.6 < p.maitrise < 0.7


def test_deux_sujets_ne_partagent_pas_leur_maitrise():
    """Sans ça, l'alternance ferait passer en examen un élève sur un
    chapitre qu'il vient d'ouvrir."""
    p = Progression("exercice", "Limites")
    _suite(p, [True, True])
    p.sujet = "Dérivées"
    assert p.maitrise == pytest.approx(0.25)


def test_ce_qui_est_prouve_survit_au_changement_d_etape():
    """La maîtrise est une connaissance de l'élève, pas un compteur de
    séance : revenir au cours ne l'efface pas."""
    p = Progression("cours", "Limites")
    _suite(p, [True, True])          # cours → exercice
    acquis = p.suivi.pour("Limites", "cours").p

    p.mode, p.sujet = "cours", "Limites"
    assert p.maitrise == pytest.approx(acquis)


def test_une_erreur_isolee_ne_fait_pas_reculer():
    """Un faux pas est une inattention ; reculer dessus serait humiliant."""
    p = Progression("exercice")
    assert p.enregistrer(False) is None
    assert p.mode == "exercice"


def test_deux_echecs_de_suite_ramenent_au_cours():
    p = Progression("exercice")
    p.enregistrer(False)
    transition = p.enregistrer(False)
    assert transition.mode == "cours"
    assert "reprend" in transition.raison.lower()


def test_une_reussite_annule_la_serie_d_echecs():
    p = Progression("exercice")
    assert _suite(p, [False, True, False]) == []
    assert p.mode == "exercice"


def test_les_compteurs_repartent_a_zero_apres_une_transition():
    """Sinon l'élève traverserait trois modes sur une seule bonne réponse."""
    p = Progression("cours")
    _suite(p, [True, True])          # → exercice
    assert p.mode == "exercice"
    assert _suite(p, [True, True]) == []   # il en faut trois, pas une
    assert p.enregistrer(True).mode == "examen"


def test_aucune_preuve_ne_fait_sortir_d_un_examen():
    """Une épreuve chronométrée ne s'interrompt pas sur une bonne réponse —
    ni sur une mauvaise. Seul l'élève, ou la fin du sujet."""
    p = Progression("examen")
    assert _suite(p, [True, True, True, True, False, False, False]) == []
    assert p.mode == "examen"


def test_une_question_libre_n_est_pas_une_etape():
    p = Progression("question")
    assert _suite(p, [True, True, True]) == []
    assert p.mode == "question"


def test_un_mode_inconnu_retombe_sur_le_cours():
    assert Progression("n'importe quoi").mode == "cours"


def test_le_parcours_complet_d_une_seance():
    """Cours → exercice → examen, sur des preuves uniquement."""
    p = Progression("cours")
    transitions = _suite(p, [True, True, True, True, True])
    assert [t.mode for t in transitions] == ["exercice", "examen"]


def test_chaque_mode_avec_critere_sait_ou_il_va():
    for mode, critere in CRITERES.items():
        assert critere.vers, mode
        assert critere.motif_avance, mode
        if critere.apres_echecs:
            assert critere.retour and critere.motif_recul, mode


# ── La consigne qui remplace le scénario ──────────────────────────

def test_la_consigne_suit_le_nouveau_mode():
    """Laisser le scénario d'ouverture ferait redémarrer le tuteur sur une
    étape déjà franchie."""
    assert "exercices" in consigne_de_mode("exercice", "les limites")
    assert "chronomètre" in consigne_de_mode("examen")
    assert "les limites" in consigne_de_mode("exercice", "les limites")


def test_le_retour_au_cours_dit_de_ne_pas_repeter():
    consigne = consigne_de_mode("cours", "les limites")
    assert "autrement" in consigne


def test_une_question_libre_n_a_pas_de_consigne():
    assert consigne_de_mode("question") == ""


# ── Le cahier (effet de génération) ───────────────────────────────

from app.services.scenario_service import (
    Alternance,
    MODES_AVEC_CAHIER,
    REGLE_CAHIER,
    _alternatives,
)


def test_le_tuteur_fait_ecrire_avant_de_corriger():
    """Produire sa réponse avant de la voir la fait retenir mieux que la
    lire. C'est le geste le moins cher de tout le projet."""
    for mode in MODES_AVEC_CAHIER:
        assert REGLE_CAHIER in consigne_de_mode(mode, "les limites")


def test_la_regle_du_cahier_interdit_de_repondre_a_sa_propre_question():
    """Sans ça, le modèle pose la question et enchaîne la réponse dans le
    même message — ce qui supprime exactement l'effet recherché."""
    assert "ATTENDS" in REGLE_CAHIER
    assert "même message" in REGLE_CAHIER


def test_pas_de_rappel_du_cahier_pendant_une_epreuve():
    """L'élève rédige déjà ; le lui rappeler sous chronomètre est du bruit."""
    assert REGLE_CAHIER not in consigne_de_mode("examen")


# ── L'alternance (interleaving) ───────────────────────────────────

def test_on_ne_fait_pas_dix_exercices_du_meme_type():
    """Enchaîner des exercices identiques entraîne à reconnaître un patron,
    pas à choisir une méthode — or c'est choisir qu'on demande au BAC."""
    a = Alternance("Limites", ["Dérivées", "Suites"])
    assert a.enregistrer() is None
    assert a.enregistrer() is None
    assert a.enregistrer() == "Dérivées"
    assert a.sujet == "Dérivées"


def test_l_ancien_sujet_revient_plus_tard():
    """Alterner n'est pas abandonner : le retour espacé est ce qui
    consolide."""
    a = Alternance("Limites", ["Dérivées"])
    assert [a.enregistrer() for _ in range(3)][-1] == "Dérivées"
    assert [a.enregistrer() for _ in range(3)][-1] == "Limites"


def test_le_compteur_repart_apres_chaque_bascule():
    a = Alternance("Limites", ["Dérivées", "Suites"])
    for _ in range(3):
        a.enregistrer()
    assert a.consecutifs == 0


def test_sans_second_sujet_on_n_alterne_pas():
    """Proposer un changement vers rien ferait inventer un chapitre."""
    a = Alternance("Limites", [])
    assert [a.enregistrer() for _ in range(9)] == [None] * 9
    assert a.sujet == "Limites"
    assert a.possible is False


def test_le_sujet_courant_n_est_pas_sa_propre_alternative():
    a = Alternance("Limites", ["Limites", "Dérivées"])
    for _ in range(3):
        resultat = a.enregistrer()
    assert resultat == "Dérivées"


def test_les_alternatives_viennent_des_lacunes_du_moteur():
    lacunes = [
        {"topic": "Limites"},
        {"topic": "Dérivées"},
        {"topic": "Suites"},
        {"topic": "Intégrales"},
        {"topic": "Complexes"},
    ]
    assert _alternatives(lacunes, "Limites") == ("Dérivées", "Suites", "Intégrales")


def test_les_alternatives_ignorent_les_doublons_et_le_bruit():
    lacunes = [{"topic": "Dérivées"}, "pas un dict", {"topic": "Dérivées"}, {"topic": ""}]
    assert _alternatives(lacunes, "Limites") == ("Dérivées",)


def test_la_directive_porte_ses_alternatives():
    directive = composer(_decision(), lacunes=[{"topic": "Limites"}, {"topic": "Dérivées"}])
    assert directive.alternatives == ("Dérivées",)


def test_une_directive_sans_lacunes_n_alterne_pas():
    assert composer(_decision()).alternatives == ()
