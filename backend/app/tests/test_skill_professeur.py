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


# ── Lire et relire ────────────────────────────────────────────────

def test_une_explication_se_termine_par_la_relecture_de_la_phrase_cle():
    consigne = SkillProfesseur(tours=3).consigne("c'est quoi la période ?", "explanation")
    assert "Je relis :" in consigne and "mot pour mot" in consigne


def test_l_eleve_qui_demande_de_reentendre_recoit_la_meme_phrase():
    for demande in ("tu peux répéter ?", "relis la définition", "عاود عافاك", "ما سمعتش"):
        consigne = SkillProfesseur(tours=3, question_en_attente=True).consigne(demande, "explanation")
        assert "demande de réentendre" in consigne, demande
        assert "essai n°" not in consigne, "réentendre n'est pas un essai"


def test_se_repete_est_une_reponse_pas_une_demande():
    consigne = SkillProfesseur(tours=3, question_en_attente=True).consigne("le mouvement se répète identique", "exploration")
    assert "demande de réentendre" not in consigne and "essai n°1" in consigne


def test_je_ne_comprends_pas_change_d_angle_au_lieu_de_relire():
    consigne = SkillProfesseur(tours=3).consigne("répète, je ne comprends pas", "explanation")
    assert "demande de réentendre" not in consigne


def test_un_enonce_se_lit_deux_fois_avant_tout_calcul():
    skill = SkillProfesseur(tours=2)
    consigne = skill.consigne("donne-moi un exercice", "application")
    assert "PREMIÈRE LECTURE" in consigne and "de quoi parle" in consigne
    _repond(skill, "<eval>aucune</eval> Voici l'exercice : un condensateur se charge… De quoi parle cet exercice ?")
    consigne = skill.consigne("de la charge d'un condensateur", "application")
    assert "RELECTURE ACTIVE" in consigne and "unités" in consigne and "essai n°" not in consigne
    _repond(skill, "<eval>aucune</eval> Bien. Quelles sont les données, et que demande-t-on ?")
    consigne = skill.consigne("E = 6 V, R = 1 kΩ, on demande τ", "application")
    assert "première étape de résolution" in consigne
    _repond(skill, "<eval>aucune</eval> Exact. Quelle relation lie τ, R et C ?")
    assert "essai n°1" in skill.consigne("τ = RC", "application"), "la résolution se note normalement"


def test_sans_question_la_lecture_guidee_s_arrete():
    skill = SkillProfesseur(tours=2)
    skill.consigne("un exercice", "application")
    _repond(skill, "<eval>aucune</eval> Voici l'exercice. Prends ton temps pour le lire.")
    assert skill.lecture_enonce == 0


# ── La parenthèse de prérequis ────────────────────────────────────

from app.services.prerequis import Prerequis  # noqa: E402

DERIVEE = Prerequis(
    id="derivee_usuelle", titre="Dériver une fonction usuelle", niveau="1BAC", matiere="Mathématiques",
    source="test", rappel="La dérivée de e^(ax) est a·e^(ax).", exemple="Dérive f(t) = e^(-2t).",
    verification="Quelle est la dérivée de g(t) = e^(-3t) ?",
)
VECTEUR = Prerequis(
    id="projection_vecteur", titre="Projeter un vecteur sur un axe", niveau="TC", matiere="Physique-Chimie",
    source="test", rappel="Px = P·cos α.", exemple="Projette un poids sur un plan incliné.", verification="Vaut quoi Px ?",
)


def _skill_bloque_sur_le_cours():
    skill = SkillProfesseur(tours=4, question_en_attente=True, tentatives=1)
    skill.proposer_prerequis([DERIVEE, VECTEUR])
    return skill


def test_les_prerequis_ne_sont_proposes_qu_apres_un_premier_essai_manque():
    skill = SkillProfesseur(tours=4, question_en_attente=True)
    skill.proposer_prerequis([DERIVEE])
    assert "<prerequis>" not in skill.consigne("τ = R + C", "application")
    skill.tentatives = 1
    consigne = skill.consigne("je ne sais pas dériver", "application")
    assert "<prerequis>identifiant</prerequis>" in consigne and "derivee_usuelle" in consigne
    assert "On ouvre une parenthèse" in consigne and DERIVEE.verification in consigne


def test_une_declaration_legitime_ouvre_la_parenthese_et_suspend_la_question():
    skill = _skill_bloque_sur_le_cours()
    skill.consigne("euh", "application")
    _repond(skill, "<eval>faux</eval> On ouvre une parenthèse : dériver. <prerequis>derivee_usuelle</prerequis> "
                   "Je relis : la dérivée de e^(ax) est a·e^(ax). Quelle est la dérivée de g(t) = e^(-3t) ?")
    assert skill.parenthese is not None and skill.parenthese.id == "derivee_usuelle"
    assert skill.parenthese.question_suspendue
    assert skill.evenement_parenthese["etat"] == "ouverte"
    consigne = skill.consigne("-3e^(-3t)", "application")
    assert "parenthèse sur « Dériver une fonction usuelle »" in consigne and "essai n°1" in consigne
    assert "REPOSE telle quelle la question du cours" in consigne
    assert "<prerequis>identifiant</prerequis>" not in consigne, "pas de parenthèse dans la parenthèse"


def test_un_identifiant_hors_liste_ou_hors_moment_est_ignore():
    skill = _skill_bloque_sur_le_cours()
    _repond(skill, "<eval>faux</eval> <prerequis>theoreme_de_thales</prerequis> Regarde l'exposant. Alors ?")
    assert skill.parenthese is None and skill.evenement_parenthese is None
    # Le tour compte normalement sur le cours : c'était le dernier essai, la
    # réponse a été donnée et la question jumelle repart de zéro.
    assert skill.derniere_evaluation == "faux" and skill.tentatives == 0


def test_la_verification_reussie_ferme_et_rend_des_essais_neufs():
    skill = _skill_bloque_sur_le_cours()
    _repond(skill, "<eval>faux</eval> <prerequis>derivee_usuelle</prerequis> Je relis : … Quelle est la dérivée de g ?")
    _repond(skill, "<eval>correct</eval> Oui. On ferme la parenthèse. Reprenons : que vaut τ ici ?")
    assert skill.parenthese is None and skill.parentheses_faites == ["derivee_usuelle"]
    assert skill.evenement_parenthese == {"etat": "fermee", "id": "derivee_usuelle", "titre": DERIVEE.titre,
                                          "niveau": "1re bac", "reussite": True, "essais": 0}
    assert skill.tentatives == 0 and skill.question_en_attente
    assert skill.reussites == 0, "réussir le prérequis n'est pas réussir la question du cours"
    assert "essai n°1" in skill.consigne("τ = RC", "application")


def test_deux_echecs_sur_le_prerequis_ferment_quand_meme_la_parenthese():
    skill = _skill_bloque_sur_le_cours()
    _repond(skill, "<eval>faux</eval> <prerequis>derivee_usuelle</prerequis> Quelle est la dérivée de g ?")
    _repond(skill, "<eval>faux</eval> Pense au coefficient de t. Quelle est la dérivée de g ?")
    assert skill.parenthese.essais == 1
    assert "dernier essai" in skill.consigne("e^(-3t)", "application")
    _repond(skill, "<eval>faux</eval> C'est -3e^(-3t). On ferme la parenthèse. Que vaut τ ici ?")
    assert skill.parenthese is None and skill.evenement_parenthese["reussite"] is False
    assert skill.evenement_parenthese["essais"] == 2


def test_un_prerequis_deja_traite_n_est_plus_propose_et_trois_au_plus():
    skill = _skill_bloque_sur_le_cours()
    skill.parentheses_faites = ["derivee_usuelle"]
    consigne = skill.consigne("euh", "application")
    assert "derivee_usuelle" not in consigne and "projection_vecteur" in consigne
    skill.parentheses_faites = ["a", "b", "c"]
    assert "<prerequis>identifiant</prerequis>" not in skill.consigne("euh", "application")


def test_demander_a_reentendre_marche_aussi_dans_la_parenthese():
    skill = _skill_bloque_sur_le_cours()
    _repond(skill, "<eval>faux</eval> <prerequis>derivee_usuelle</prerequis> Quelle est la dérivée de g ?")
    assert "demande de réentendre" in skill.consigne("répète la question", "application")


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
