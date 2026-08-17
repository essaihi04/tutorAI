"""Le choix de la façon d'expliquer.

UCB1 est déterministe : ces tests vérifient donc des choix exacts, pas des
tendances statistiques. C'est la raison principale de l'avoir préféré à un
ε-greedy — un tuteur dont on ne peut pas expliquer les choix est un tuteur
qu'on ne peut pas corriger.
"""
import pytest

from app.services.teaching_tactics import (
    MARQUEUR,
    TACTIQUES,
    BanditTactiques,
    depuis_historique,
    lire_tactique,
    marquer_source,
)


def _entrainer(bandit, cle, reussites, echecs=0):
    for _ in range(reussites):
        bandit.recompenser(cle, True)
    for _ in range(echecs):
        bandit.recompenser(cle, False)
    return bandit


# ── L'exploration ─────────────────────────────────────────────────

def test_chaque_tactique_est_essayee_avant_toute_conclusion():
    """Sans ça, une bonne méthode écartée par malchance au premier essai ne
    reviendrait jamais."""
    bandit = BanditTactiques()
    essayees = []
    for _ in range(len(TACTIQUES)):
        tactique = bandit.choisir()
        essayees.append(tactique.cle)
        bandit.recompenser(tactique.cle, False)

    assert sorted(essayees) == sorted(t.cle for t in TACTIQUES)


def test_le_premier_choix_est_reproductible():
    """À égalité, l'ordre de déclaration tranche : deux élèves identiques
    reçoivent le même enseignement."""
    assert BanditTactiques().choisir().cle == BanditTactiques().choisir().cle
    assert BanditTactiques().choisir().cle == TACTIQUES[0].cle


# ── L'exploitation ────────────────────────────────────────────────

def test_ce_qui_marche_finit_par_etre_repris():
    bandit = BanditTactiques()
    for tactique in TACTIQUES:
        _entrainer(bandit, tactique.cle, reussites=0, echecs=4)
    _entrainer(bandit, "analogie", reussites=8)

    assert bandit.choisir().cle == "analogie"


def test_une_tactique_qui_echoue_est_delaissee():
    bandit = BanditTactiques()
    for tactique in TACTIQUES:
        _entrainer(bandit, tactique.cle, reussites=5)
    _entrainer(bandit, "schema", reussites=0, echecs=20)

    assert bandit.choisir().cle != "schema"


def test_une_tactique_peu_essayee_garde_sa_chance():
    """Le terme d'exploration : deux réussites sur deux ne suffisent pas à
    condamner définitivement une méthode vue une seule fois."""
    bandit = BanditTactiques()
    _entrainer(bandit, "exemple", reussites=2)
    _entrainer(bandit, "schema", reussites=1)
    for cle in ("analogie", "socratique", "contre_exemple"):
        _entrainer(bandit, cle, reussites=0, echecs=3)

    # `schema` a la même moyenne qu'`exemple` mais moins d'essais : son bonus
    # d'exploration le fait passer devant.
    assert bandit.choisir().cle == "schema"


# ── Ne pas radoter ────────────────────────────────────────────────

def test_on_ne_rejoue_pas_la_methode_qui_vient_d_echouer():
    """Réexpliquer « autrement » est le principe du retour au cours ;
    rejouer la même méthode serait ressenti comme du radotage."""
    # Chaque tactique est largement essayée : sans ça le bonus
    # d'exploration domine encore, et c'est UCB1 qui a raison — on ne
    # conclut pas sur quatre essais.
    bandit = BanditTactiques()
    for tactique in TACTIQUES:
        _entrainer(bandit, tactique.cle, reussites=1, echecs=11)
    _entrainer(bandit, "exemple", reussites=20)

    assert bandit.choisir().cle == "exemple"
    assert bandit.choisir(exclure="exemple").cle != "exemple"


def test_exclure_la_seule_tactique_ne_bloque_pas_le_tuteur():
    """Mieux vaut répéter une explication que ne rien dire."""
    bandit = BanditTactiques()
    assert bandit.choisir(exclure="tout") is not None


# ── Les garde-fous ────────────────────────────────────────────────

def test_une_tactique_inconnue_n_entre_pas_dans_les_scores():
    bandit = BanditTactiques()
    bandit.recompenser("télépathie", True)
    assert bandit.total_essais == 0


def test_le_classement_se_lit_comme_une_phrase():
    """« L'exemple résolu marche 4 fois sur 5, l'analogie 1 fois sur 4. »"""
    bandit = BanditTactiques()
    _entrainer(bandit, "exemple", reussites=4, echecs=1)
    _entrainer(bandit, "analogie", reussites=1, echecs=3)

    assert bandit.classement() == [("exemple", 4, 5), ("analogie", 1, 4)]


def test_une_tactique_jamais_essayee_n_apparait_pas_au_classement():
    assert BanditTactiques().classement() == []


# ── La mémoire entre séances ──────────────────────────────────────

def test_la_tactique_est_conservee_dans_la_source():
    marquee = marquer_source("chat_coaching", "schema")
    assert MARQUEUR in marquee
    assert marquee.startswith("chat_coaching")
    assert lire_tactique(marquee) == "schema"


def test_une_source_sans_tactique_reste_intacte():
    """L'historique existant ne doit pas être réinterprété."""
    assert marquer_source("exam", None) == "exam"
    assert marquer_source("exam", "télépathie") == "exam"
    assert lire_tactique("exam") is None
    assert lire_tactique("") is None


def test_une_tactique_disparue_du_code_est_ignoree():
    """Un jour on retirera une tactique ; l'historique, lui, restera."""
    assert lire_tactique("chat_coaching|tactique=vieille_methode") is None


def test_le_bandit_se_reconstruit_depuis_l_historique():
    """Sans cette relecture, chaque séance repartirait de zéro et le bandit
    passerait sa vie à explorer."""
    historique = [
        {"source": marquer_source("chat_coaching", "analogie"), "is_correct": True},
        {"source": marquer_source("chat_coaching", "analogie"), "is_correct": True},
        {"source": marquer_source("chat_coaching", "schema"), "is_correct": False},
        {"source": "exam", "is_correct": True},
        "pas un dict",
    ]
    bandit = depuis_historique(historique)

    assert bandit.classement() == [("analogie", 2, 2), ("schema", 0, 1)]
    assert bandit.total_essais == 3


def test_un_historique_vide_donne_un_bandit_neuf():
    assert depuis_historique(None).total_essais == 0
    assert depuis_historique([]).total_essais == 0
