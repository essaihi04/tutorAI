"""La parenthèse de prérequis, vue depuis la séance : le chapitre est reconnu,
l'écran est prévenu, la fermeture laisse une trace dans l'historique."""
import asyncio

from app.services.skill_professeur import SkillProfesseur
from app.tests.test_session_mode_handler import _handler


def _seance(subject, titre):
    handler = _handler()
    handler.skill_prof = SkillProfesseur()
    handler.session_context = {"subject": subject, "chapter_title": titre}
    handler.student_id = "00000000-0000-0000-0000-000000000001"
    return handler


def test_le_chapitre_reconnu_donne_ses_prerequis_au_skill_prof():
    handler = _seance("Physique", "Le dipôle RC : charge d'un condensateur")
    handler._proposer_prerequis_du_chapitre()
    ids = [c.id for c in handler.skill_prof.candidats]
    assert "derivee_usuelle" in ids and "lois_kirchhoff" in ids
    assert all(c.niveau in ("college", "TC", "1BAC") for c in handler.skill_prof.candidats)


def test_un_titre_inconnu_ne_propose_rien():
    handler = _seance("Physique", "Révision générale")
    handler._proposer_prerequis_du_chapitre()
    assert handler.skill_prof.candidats == []


def test_la_proposition_n_est_refaite_que_si_la_seance_change(monkeypatch):
    handler = _seance("SVT", "Les lois de Mendel")
    appels = []
    monkeypatch.setattr(handler.skill_prof, "proposer_prerequis", lambda c: appels.append(c))
    handler._proposer_prerequis_du_chapitre()
    handler._proposer_prerequis_du_chapitre()
    assert len(appels) == 1
    handler.session_context["chapter_title"] = "L'hérédité liée au sexe"
    handler._proposer_prerequis_du_chapitre()
    assert len(appels) == 2


def test_le_chapitre_reconnu_injecte_aussi_son_perimetre():
    handler = _seance("Physique", "Le dipôle RC : charge d'un condensateur")
    handler._proposer_prerequis_du_chapitre()
    assert handler._chapitre_reconnu == "dipole_RC"
    assert "[PÉRIMÈTRE DU PROGRAMME — Dipôle RC]" in handler._bloc_perimetre
    handler.session_context["chapter_title"] = "Dipôle RL"
    handler._proposer_prerequis_du_chapitre()
    assert handler._bloc_perimetre == "", "pas de fiche, pas de bloc"


def test_l_observation_du_perimetre_journalise_sans_corriger(monkeypatch, tmp_path):
    from app.services import perimetre

    monkeypatch.setattr(perimetre, "JOURNAL", tmp_path / "perimetre.jsonl")
    handler = _seance("Physique", "Le dipôle RC")
    handler._proposer_prerequis_du_chapitre()
    handler._observer_perimetre("<eval>aucune</eval> On peut voir ça comme un filtre passe-bas, avec l'impédance du condensateur. Tu me suis ?")
    assert handler._depassements_perimetre == 2
    lignes = (tmp_path / "perimetre.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(lignes) == 1 and "passe-bas" in lignes[0]
    assert handler.websocket.envoyes == [], "observation : rien n'est envoyé à l'élève"
    handler._observer_perimetre("<eval>correct</eval> Oui : τ = RC. Et si R double ?")
    assert handler._depassements_perimetre == 2


def test_la_fermeture_previent_l_ecran_et_entre_dans_l_historique(monkeypatch):
    handler = _seance("Physique", "Le dipôle RC")
    enregistre = {}

    async def faux_record(**kw):
        enregistre.update(kw)

    from app.services import student_proficiency_service as sps
    monkeypatch.setattr(sps.proficiency_service, "record_answer", faux_record)

    asyncio.run(handler._signaler_parenthese({"etat": "ouverte", "id": "derivee_usuelle", "titre": "Dériver", "niveau": "1re bac"}))
    assert enregistre == {}, "ouvrir n'est pas une réponse"
    asyncio.run(handler._signaler_parenthese({"etat": "fermee", "id": "derivee_usuelle", "titre": "Dériver", "niveau": "1re bac", "reussite": True, "essais": 0}))

    types = [m["type"] for m in handler.websocket.envoyes]
    assert types == ["parenthese", "parenthese"]
    assert handler.websocket.envoyes[1]["etat"] == "fermee"
    assert enregistre["source"] == "parenthese" and enregistre["is_correct"] is True
    assert enregistre["subject"] == "Mathématiques", "le prérequis est compté dans SA matière d'origine"
    assert enregistre["topic"].startswith("Prérequis (1re bac)")
