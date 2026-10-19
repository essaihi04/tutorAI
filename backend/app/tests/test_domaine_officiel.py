"""Chaque réponse porte un domaine du cadre de référence, ou « Non classé »."""
import asyncio
from types import SimpleNamespace

from app.services.topic_atlas_service import NON_CLASSE, SUBJECT_DOMAINS, domaine_officiel


def test_une_question_de_mecanique_va_en_mecanique():
    domaine = domaine_officiel("Physique", "Mouvement d'un projectile", "Appliquer la deuxième loi de Newton")
    assert "Mécanique" in domaine


def test_les_noms_de_matiere_varies_sont_reconnus():
    for matiere in ("Physique-Chimie", "PC", "physique chimie"):
        assert domaine_officiel(matiere, "deuxième loi de Newton") != NON_CLASSE
    assert "Nombres complexes" in domaine_officiel("Maths", "Calculer le module du nombre complexe z")


def test_le_domaine_rendu_vient_toujours_de_la_liste_officielle():
    domaine = domaine_officiel("SVT", "Expliquer le rôle de l'ARN messager dans la traduction")
    assert domaine in SUBJECT_DOMAINS["SVT"]


def test_rien_n_est_devine():
    assert domaine_officiel("Philosophie", "la liberté") == NON_CLASSE
    assert domaine_officiel("Général", "deuxième loi de Newton") == NON_CLASSE
    assert domaine_officiel("Physique", "Bonjour, on commence ?") == NON_CLASSE
    assert domaine_officiel("Physique", "", "") == NON_CLASSE


def test_deux_domaines_a_egalite_donnent_non_classe():
    # Un mot de chaque domaine, sans rien pour départager.
    from app.services.topic_atlas_service import PHYSIQUE_DOMAINS
    mots = [next(m for m in mots if " " not in m) for mots in list(PHYSIQUE_DOMAINS.values())[:2]]
    assert domaine_officiel("Physique", " ".join(mots)) == NON_CLASSE


def test_le_decompte_separe_les_reponses_classees_des_anciennes():
    import importlib.util
    from pathlib import Path

    chemin = Path(__file__).resolve().parents[2] / "scripts" / "decompte_domaines.py"
    spec = importlib.util.spec_from_file_location("decompte_domaines", chemin)
    script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script)

    enregistrees, reclassees = script.decompte([
        {"subject": "Physique", "chapter": "Physique — Sous-domaine 4 : Mécanique (27%)"},
        {"subject": "Physique", "chapter": NON_CLASSE},
        {"subject": "Physique", "chapter": "", "topic": "Chute libre", "question_content": "deuxième loi de Newton"},
    ])
    assert sum(enregistrees.values()) == 2 and enregistrees[("Physique", NON_CLASSE)] == 1
    assert sum(reclassees.values()) == 1


def test_record_answer_enregistre_le_domaine():
    from app.services import student_proficiency_service as module

    lignes = []

    class Table:
        def insert(self, row):
            lignes.append(row)
            return self

        def execute(self):
            return SimpleNamespace(data=[lignes[-1]])

    service = module.StudentProficiencyService()
    service._supabase = SimpleNamespace(table=lambda nom: Table())
    asyncio.run(service.record_answer(
        student_id="00000000-0000-0000-0000-000000000000",
        subject="Physique", topic="Chute verticale",
        question_content="Appliquer la deuxième loi de Newton au centre d'inertie",
        student_answer="ma = mg", correct_answer="", is_correct=True, skip_update=True,
    ))
    assert "Mécanique" in lignes[0]["chapter"]
    assert lignes[0]["topic"] == "Chute verticale"
