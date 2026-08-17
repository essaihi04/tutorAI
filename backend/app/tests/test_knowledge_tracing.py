"""L'estimation de maîtrise, vérifiée au chiffre près.

Le module ne touche ni base ni session : c'est exactement ce qui permet de
tester les équations elles-mêmes plutôt que leurs effets de bord. Les valeurs
attendues sont calculées à la main depuis les paramètres par défaut — si
elles bougent, c'est que le modèle a changé, pas que le test est fragile.
"""
import pytest

from app.services.knowledge_tracing import (
    PARAMETRES_DEFAUT,
    Maitrise,
    ParametresBKT,
    SuiviMaitrise,
)


def _apres(reponses, parametres=PARAMETRES_DEFAUT) -> float:
    m = Maitrise(parametres)
    for r in reponses:
        m.observer(r)
    return m.p


# ── Les équations ─────────────────────────────────────────────────

def test_l_estimation_part_de_l_a_priori():
    assert Maitrise().p == pytest.approx(0.25)


def test_une_bonne_reponse_fait_monter_l_estimation():
    """Bayes puis transition : 0,25 → 0,60 → 0,66."""
    assert _apres([True]) == pytest.approx(0.66, abs=0.005)


def test_une_mauvaise_reponse_fait_baisser_l_estimation():
    assert _apres([False]) == pytest.approx(0.184, abs=0.005)


def test_deux_bonnes_reponses_suffisent_a_convaincre_a_85_pourcent():
    """Reproduit le seuil empirique que `Progression` utilisait déjà."""
    assert _apres([True, True]) >= 0.85


def test_il_en_faut_trois_pour_convaincre_a_95_pourcent():
    assert _apres([True, True]) < 0.95
    assert _apres([True, True, True]) >= 0.95


def test_l_estimation_ne_tombe_jamais_a_zero():
    """Le terme d'apprentissage suppose que l'enseignement sert : un élève en
    difficulté doit pouvoir remonter, pas rester enfermé à zéro."""
    p = _apres([False] * 20)
    assert 0 < p < 0.2


def test_l_estimation_ne_depasse_jamais_un():
    assert _apres([True] * 20) < 1.0


# ── Ce que le comptage de réussites ratait ────────────────────────

def test_la_chance_est_prise_en_compte():
    """Trois QCM réussis au hasard ne valent pas trois maîtrises. Avec une
    chance élevée, l'estimation monte nettement moins vite."""
    prudent = ParametresBKT(chance=0.45)
    assert _apres([True, True, True], prudent) < _apres([True, True, True])


def test_l_etourderie_protege_l_eleve_qui_sait():
    """Une erreur isolée après deux réussites ne renvoie pas à la case
    départ — le compteur consécutif, lui, effaçait tout."""
    assert _apres([True, True, False]) > _apres([False])


def test_une_erreur_precoce_n_efface_pas_quatre_reussites():
    """Le crédit est GRADUÉ : quatre réussites sur cinq restent une preuve
    solide, même avec l'échec au milieu. Une règle « consécutive » stricte
    aurait tout remis à zéro."""
    assert _apres([True, True, False, True, True]) >= 0.95


def test_un_eleve_qui_alterne_au_hasard_ne_convainc_pas():
    """La contrepartie : répondre juste une fois sur deux ne franchit aucun
    seuil, quelle que soit la longueur de la série."""
    assert _apres([True, False] * 6) < 0.85


# ── Les garde-fous ────────────────────────────────────────────────

def test_un_modele_degenere_est_refuse():
    """Au-delà de 0,5, savoir rendrait l'échec plus probable que réussir : les
    bonnes réponses FERAIENT BAISSER l'estimation, sans que rien ne le
    signale."""
    with pytest.raises(ValueError, match="dégénéré"):
        ParametresBKT(chance=0.6)
    with pytest.raises(ValueError, match="dégénéré"):
        ParametresBKT(etourderie=0.5)


def test_un_parametre_hors_bornes_est_refuse():
    with pytest.raises(ValueError):
        ParametresBKT(init=1.5)
    with pytest.raises(ValueError):
        ParametresBKT(apprentissage=-0.1)


def test_on_ne_conclut_pas_sans_observation():
    """Sans ce garde-fou, un seuil bas déclarerait acquise une compétence sur
    laquelle l'élève n'a jamais rien répondu."""
    m = Maitrise()
    assert m.acquise(seuil=0.20) is False
    m.observer(True)
    assert m.acquise(seuil=0.20) is True


# ── Le suivi par compétence ───────────────────────────────────────

def test_expliquer_et_appliquer_sont_deux_competences():
    """Confondre les deux ferait passer en examen un élève qui a seulement
    compris l'explication."""
    suivi = SuiviMaitrise()
    suivi.observer("Limites", "cours", True)
    suivi.observer("Limites", "cours", True)

    assert suivi.pour("Limites", "cours").p >= 0.85
    assert suivi.pour("Limites", "exercice").p == pytest.approx(0.25)


def test_chaque_sujet_a_sa_propre_estimation():
    suivi = SuiviMaitrise()
    suivi.observer("Limites", "exercice", True)
    assert suivi.pour("Dérivées", "exercice").p == pytest.approx(0.25)


def test_la_cle_ignore_la_casse_et_les_espaces():
    """Le sujet vient du moteur, parfois avec une majuscule, parfois sans :
    deux orthographes ne doivent pas créer deux élèves."""
    suivi = SuiviMaitrise()
    suivi.observer(" Limites ", "Exercice", True)
    assert suivi.pour("limites", "exercice").observations == 1
