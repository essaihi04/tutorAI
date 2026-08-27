"""Le rapprochement entre une séance et un schéma déjà dessiné.

Ce chemin décide si l'élève voit un schéma validé ou un croquis improvisé.
Ses erreurs sont silencieuses : personne ne remarque qu'un mot-clé n'a pas
répondu, on voit seulement un dessin à main levée à la place du bon schéma.
"""

import json
from pathlib import Path

from app.services.schema_catalog import SCHEMA_CATALOG, SCHEMA_IDS, match_schema, schema_title


PROJECT_ROOT = Path(__file__).resolve().parents[3]


def test_un_mot_cle_ne_repond_pas_au_milieu_d_un_autre_mot():
    """`exp` est dans « expansion », `ln` dans dix mots : cherchés en
    sous-chaîne, ils proposaient les fonctions exponentielles à un cours de
    géologie."""
    schema_id, _ = match_schema("la dorsale océanique et l'expansion des fonds océaniques")

    assert schema_id == "svt_dorsale_accretion"


def test_le_vrai_cours_d_exponentielle_repond_toujours():
    schema_id, score = match_schema("cours sur la fonction exponentielle et le logarithme népérien")

    assert schema_id == "math_exp_ln"
    assert score >= 2


def test_le_pluriel_et_les_accents_absents_repondent():
    """Un cours parle des « myofibrilles », un élève tape « accretion » sans
    accent : le mot-clé est au singulier et accentué, il doit répondre quand
    même."""
    avec, _ = match_schema("les myofibrilles et le réticulum sarcoplasmique de la fibre musculaire")
    sans_accent, _ = match_schema("la dorsale et l'accretion oceanique")

    assert avec == "svt_fibre_musculaire"
    assert sans_accent == "svt_dorsale_accretion"


def test_un_contexte_vide_ou_hors_sujet_ne_propose_rien():
    assert match_schema("") == (None, 0)
    assert match_schema("   ") == (None, 0)
    assert match_schema("bonjour ça va merci") == (None, 0)


def test_tout_identifiant_propose_existe_vraiment():
    """Proposer un identifiant absent de la bibliothèque afficherait du vide."""
    for entry in SCHEMA_CATALOG:
        contexte = " ".join(entry["keywords"][:3])
        schema_id, _ = match_schema(contexte)
        assert schema_id is None or schema_id in SCHEMA_IDS


def test_chaque_schema_porte_des_mots_cles_et_un_titre():
    for entry in SCHEMA_CATALOG:
        assert entry["keywords"], f"{entry['id']} n'a aucun mot-clé : introuvable"
        assert schema_title(entry["id"]) == entry["title"]


def test_le_mot_cle_le_plus_precis_l_emporte():
    """« fibre musculaire » designe une figure, « muscle » designe un chapitre.

    Sans ponderation ni depart au plus long, les deux schemas du muscle
    arrivaient a egalite et c'est l'ordre du fichier qui tranchait : un cours
    sur la fibre musculaire se voyait proposer le sarcomere.
    """
    fibre, _ = match_schema("structure du muscle strié, faisceaux et fibre musculaire")
    sarcomere, _ = match_schema("contraction musculaire, actine et myosine, strie Z")

    assert fibre == "svt_fibre_musculaire"
    assert sarcomere == "svt_muscle_sarcomere"


def test_une_demande_de_croquis_prefere_la_version_crayon():
    reference, _ = match_schema("explique la glycolyse")
    croquis, score = match_schema("dessine la glycolyse au tableau")
    darija_latin, _ = match_schema("rsem lia glycolyse f tableau")
    darija_arabe, _ = match_schema("رسم ليا بنية الميتوكندريا")

    assert reference == "svt_glycolyse"
    assert croquis == "svt_croquis_glycolyse"
    assert darija_latin == "svt_croquis_glycolyse"
    assert darija_arabe == "svt_croquis_mitochondrie"
    assert score >= 3


def test_les_croquis_des_premiers_cours_portent_les_metadonnees_llm():
    croquis = [
        entry for entry in SCHEMA_CATALOG
        if (entry.get("metadata") or {}).get("resourceRole") == "teacher_sketch"
    ]

    assert len(croquis) == 36
    assert {
        subject: len([entry for entry in croquis if entry["subject"] == subject])
        for subject in {entry["subject"] for entry in croquis}
    } == {"svt": 9, "physics": 10, "chemistry": 10, "math": 7}
    for entry in croquis:
        metadata = entry["metadata"]
        assert metadata["visualStyle"] == "pencil"
        assert metadata["lesson"]
        assert metadata["learningObjectives"]
        assert metadata["llmIntents"]
        assert metadata["drawingSteps"]

        if entry["subject"] != "svt":
            assert metadata["paletteId"] == "bac-pencil-v1"
            assert metadata["auditStatus"] in {"video_reviewed", "curriculum_reviewed"}


def test_les_croquis_audites_sur_video_conservent_leur_provenance():
    video_croquis = [
        entry for entry in SCHEMA_CATALOG
        if (entry.get("metadata") or {}).get("auditStatus") == "video_reviewed"
    ]

    assert len(video_croquis) == 14
    for entry in video_croquis:
        metadata = entry["metadata"]
        assert metadata["sourceUrl"].startswith("https://www.youtube.com/watch?v=")
        assert metadata["sourceTeacher"]
        assert metadata["sourceVideoTitle"]
        assert metadata["sourceTimecodes"]


def test_les_demandes_complexes_selectionnent_les_croquis_explications():
    signaux, _ = match_schema("dessine les deux signaux homologues et leur retard")
    catalyseur, _ = match_schema("dessine le profil énergie activation avec catalyseur régénéré")
    tvi, _ = match_schema("dessine le TVI continuité changement de signe et unicité")

    assert signaux == "phys_croquis_signaux_retard"
    assert catalyseur == "chem_croquis_catalyseur"
    assert tvi == "math_croquis_tvi"


def test_les_trois_cours_ne_referencent_que_des_schemas_enregistres():
    for relative_path in [
        "backend/data/courses/phys_ch1_waves_course_v1.json",
        "backend/data/courses/chem_ch1_kinetics_course_v1.json",
        "backend/data/courses/math_ch1_limits_course_v1.json",
    ]:
        course = json.loads((PROJECT_ROOT / relative_path).read_text(encoding="utf-8"))
        schema_ids = [
            slide["visual"]["schema_id"]
            for activity in course["activities"]
            for slide in activity["slides"]
            if (slide.get("visual") or {}).get("kind") == "schema"
        ]

        assert schema_ids
        assert set(schema_ids) <= SCHEMA_IDS
