"""Le geste de prof : quand expliquer, quand questionner, quand donner la réponse.

Ce qui est vérifié ici, c'est la MACHINE — les essais comptés, la question en
attente, la consigne qui change avec eux — pas la prose du modèle.
"""
from app.websockets.session_handler import _StreamTagFilter
from app.services.skill_professeur import (
    ESSAIS_AVANT_REPONSE,
    SkillProfesseur,
    retirer_balise_eval,
    se_termine_par_une_question,
)


def _repond(skill, brute, affiche=None):
    return skill.lire_reponse(brute, affiche if affiche is not None else retirer_balise_eval(brute))


# ── La consigne suit la situation ─────────────────────────────────

def test_premier_tour_salue_et_accroche():
    consigne = SkillProfesseur().consigne("bonjour", "activation")
    assert "premier tour" in consigne and "question d'accroche" in consigne
    assert "<eval>" in consigne and "5 à 8 phrases" in consigne


def test_une_notion_a_expliquer_se_fait_en_bloc_puis_reformulation():
    skill = SkillProfesseur(tours=3)
    consigne = skill.consigne("c'est quoi une onde progressive ?", "explanation")
    assert "bloc complet" in consigne and "reformulation" in consigne.lower()
    assert "REFORMULATION" in consigne


def test_une_demande_d_exercice_pose_un_seul_exercice():
    consigne = SkillProfesseur(tours=4).consigne("donne-moi un exercice", "application")
    assert "UN exercice" in consigne and "sans la solution" in consigne


# ── Les essais : indice, indice, puis la réponse ──────────────────

def test_premier_essai_faux_donne_un_indice_jamais_la_reponse():
    skill = SkillProfesseur(tours=2, question_en_attente=True)
    consigne = skill.consigne("c'est parallèle à la propagation", "exploration")
    assert "essai n°1" in consigne
    assert "ne donne pas la réponse" in consigne.lower()
    assert "UN indice" in consigne


def test_apres_deux_essais_manques_la_reponse_est_donnee_avec_une_question_jumelle():
    skill = SkillProfesseur(tours=2, question_en_attente=True)
    _repond(skill, "<eval>faux</eval> Pas tout à fait : regarde le point orange. Il monte ou il avance ?")
    assert skill.tentatives == 1 and skill.question_en_attente
    consigne = skill.consigne("il avance", "exploration")
    assert f"essai n°{ESSAIS_AVANT_REPONSE}" in consigne
    assert "dernier essai" in consigne and "question jumelle" in consigne
    _repond(skill, "<eval>faux</eval> La réponse : il monte puis redescend, c'est transversal. Et sur un ressort ?")
    assert skill.tentatives == 0, "la question jumelle repart de zéro"
    assert skill.question_en_attente


def test_une_bonne_reponse_remet_les_essais_a_zero_et_compte_une_reussite():
    skill = SkillProfesseur(tours=2, question_en_attente=True, tentatives=1)
    evaluation = _repond(skill, "**<eval>Correct</eval>** Bravo, c'est transversal. On passe au ressort : ça change quoi ?")
    assert evaluation == "correct"
    assert skill.tentatives == 0 and skill.reussites == 1 and skill.question_en_attente


def test_l_eleve_qui_ne_sait_pas_est_rassure_et_recoit_l_indice():
    skill = SkillProfesseur(tours=2, question_en_attente=True)
    consigne = skill.consigne("je ne sais pas", "exploration")
    assert "ne pas savoir" in consigne and "rassure" in consigne


def test_une_reponse_incertaine_demande_de_preciser_sans_compter_d_essai():
    skill = SkillProfesseur(tours=2, question_en_attente=True)
    consigne = skill.consigne("euh c'est le truc qui", "exploration")
    assert "préciser" in consigne and "« incertain »" in consigne
    evaluation = _repond(skill, "<eval>incertain</eval> Tu veux dire le point orange ou toute la corde ?")
    assert evaluation == "incertain"
    assert skill.tentatives == 0 and skill.incertains == 1 and skill.question_en_attente


def test_apres_une_precision_le_prof_doit_trancher():
    skill = SkillProfesseur(tours=3, question_en_attente=True, incertains=1)
    consigne = skill.consigne("le truc", "exploration")
    assert "cette fois tranche" in consigne
    evaluation = _repond(skill, "<eval>incertain</eval> Je ne vois toujours pas. Il monte ou il avance ?")
    assert evaluation == "faux", "rester flou deux fois compte un essai"
    assert skill.tentatives == 1 and skill.incertains == 0


def test_une_reponse_tranchee_efface_la_demande_de_precision():
    skill = SkillProfesseur(tours=3, question_en_attente=True, incertains=1)
    _repond(skill, "<eval>correct</eval> Oui, il monte : c'est transversal. Et sur un ressort ?")
    assert skill.incertains == 0 and skill.reussites == 1


def test_sans_balise_ni_question_rien_n_est_compte():
    skill = SkillProfesseur(tours=2, question_en_attente=True, tentatives=1)
    evaluation = _repond(skill, "Reprenons calmement la définition d'une onde.")
    assert evaluation == "aucune"
    assert skill.tentatives == 1, "une réponse sans jugement ne compte pas un essai"
    assert not skill.question_en_attente


# ── La balise ne sort jamais ──────────────────────────────────────

def test_la_balise_est_retiree_du_texte_lu():
    assert retirer_balise_eval("<eval>partiel</eval> Presque : il manque l'unité.") == "Presque : il manque l'unité."
    assert retirer_balise_eval("**<eval>aucune</eval>**\nBonjour !") == "Bonjour !"
    assert retirer_balise_eval("Sans balise.") == "Sans balise."


def test_la_question_en_attente_se_lit_sur_la_derniere_phrase():
    assert se_termine_par_une_question("Bien. Et maintenant, que vaut v ?")
    assert se_termine_par_une_question("واش فهمتي ؟")
    assert not se_termine_par_une_question("Que vaut v ? Je te le dis : 4 m/s.")
    assert not se_termine_par_une_question("")


def test_la_balise_n_atteint_jamais_le_fil_de_chat_meme_coupee_en_tokens():
    filtre = _StreamTagFilter()
    reponse = "**<eval>partiel</eval>** Presque : il manque l'unité.\nQuelle est-elle ?\n"
    acc, sorti = "", ""
    for i in range(0, len(reponse), 3):
        acc += reponse[i:i + 3]
        sorti += filtre.feed(acc)
    sorti += filtre.flush(acc)
    assert "eval" not in sorti and "partiel" not in sorti
    assert "Presque : il manque l'unité." in sorti and "Quelle est-elle ?" in sorti
