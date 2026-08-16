from app.services.subject_access_service import (
    build_exam_subject_keys,
    canonical_subject_key,
    is_exam_subject_allowed,
)


def test_canonical_subject_key_handles_current_labels():
    assert canonical_subject_key("Mathématiques") == "mathematiques"
    assert canonical_subject_key("Mathematiques") == "mathematiques"
    assert canonical_subject_key("Sciences de la Vie et de la Terre (SVT)") == "svt"
    assert canonical_subject_key("Physique-Chimie") == "physique-chimie"


def test_combined_pc_exam_requires_both_content_subjects():
    physique_only = [{"name_fr": "Physique"}]
    both = [{"name_fr": "Physique"}, {"name_fr": "Chimie"}]

    assert "physique-chimie" not in build_exam_subject_keys(physique_only)
    assert "physique-chimie" in build_exam_subject_keys(both)


def test_exam_authorization_uses_canonical_keys():
    allowed = ["mathematiques", "svt"]
    assert is_exam_subject_allowed("Mathématiques", allowed)
    assert is_exam_subject_allowed("SVT", allowed)
    assert not is_exam_subject_allowed("Physique-Chimie", allowed)
