"""La boîte à erreurs : seule une nouvelle réussite, plus tard, la vide."""
from datetime import datetime, timedelta, timezone

from app.services.boite_erreurs import a_revoir, depuis_historique

T0 = datetime(2026, 10, 19, 9, 0, tzinfo=timezone.utc)


def _ligne(minutes, correct, question, notion="Ondes progressives", sujet="Physique"):
    return {
        "created_at": (T0 + timedelta(minutes=minutes)).isoformat(),
        "subject": sujet,
        "topic": notion,
        "question_content": question,
        "student_answer": "réponse",
        "is_correct": correct,
    }


def test_une_erreur_reste_dans_la_boite():
    erreurs = depuis_historique([_ligne(0, False, "Transversale ou longitudinale ?")])
    assert len(erreurs) == 1 and erreurs[0].notion == "Ondes progressives"


def test_la_question_jumelle_de_la_foulee_ne_vide_pas_la_boite():
    erreurs = depuis_historique([
        _ligne(0, False, "Transversale ou longitudinale ?"),
        _ligne(3, True, "Et sur un ressort, quelle onde ?"),
    ])
    assert len(erreurs) == 1


def test_reussir_la_meme_question_plus_tard_ne_vide_pas_la_boite():
    erreurs = depuis_historique([
        _ligne(0, False, "Transversale ou longitudinale ?"),
        _ligne(24 * 60, True, "Transversale ou longitudinale ?"),
    ])
    assert len(erreurs) == 1


def test_une_nouvelle_question_reussie_plus_tard_vide_la_boite():
    erreurs = depuis_historique([
        _ligne(0, False, "Transversale ou longitudinale ?"),
        _ligne(24 * 60, True, "Que vaut la célérité si λ = 2 m et T = 0,5 s ?"),
    ])
    assert erreurs == []


def test_une_reussite_sur_une_autre_notion_ne_compte_pas():
    erreurs = depuis_historique([
        _ligne(0, False, "Transversale ou longitudinale ?"),
        _ligne(24 * 60, True, "Une autre question", notion="Diffraction"),
    ])
    assert len(erreurs) == 1


def test_les_notions_vagues_ne_vont_pas_dans_la_boite():
    assert depuis_historique([_ligne(0, False, "Question ?", notion="Conversation")]) == []


def test_on_revoit_d_abord_les_notions_les_plus_ratees():
    erreurs = depuis_historique([
        _ligne(0, False, "q1", notion="Diffraction"),
        _ligne(10, False, "q2", notion="Ondes progressives"),
        _ligne(20, False, "q3", notion="Ondes progressives"),
    ])
    notions = a_revoir(erreurs)
    assert [n.notion for n in notions] == ["Ondes progressives", "Diffraction"]
    assert len(notions[0].erreurs) == 2
