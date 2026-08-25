import asyncio
import hashlib
import json
import re
from pathlib import Path
from types import SimpleNamespace

import app.services.course_player_service as course_player_module
from app.services.course_player_service import CoursePlayerService


BACKEND_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_ROOT.parent
COURSE_DIR = BACKEND_ROOT / "data" / "courses"
SVT_MANIFEST_PATHS = (
    COURSE_DIR / "svt_ch1_energy_course_v1.json",
    COURSE_DIR / "svt_ch1_muscle_course_v1.json",
)
MANIFEST_PATHS = tuple(sorted(COURSE_DIR.glob("*_course_v1.json")))
SCHEMA_REGISTRY_DIR = PROJECT_ROOT / "frontend/src/components/session/schemas"


def _manifests(paths=MANIFEST_PATHS):
    return [json.loads(path.read_text(encoding="utf-8")) for path in paths]


def test_full_chapter_has_sixteen_timed_activities_and_microquestions():
    manifests = _manifests(SVT_MANIFEST_PATHS)
    activities = [activity for manifest in manifests for activity in manifest["activities"]]

    assert len(activities) == 16
    assert sum(activity["duration_minutes"] for activity in activities) == 295
    assert all(15 <= activity["duration_minutes"] <= 20 for activity in activities)
    for activity in activities:
        assert activity["objective_ids"]
        assert len(activity["slides"]) >= 2
        for slide in activity["slides"]:
            assert slide["speech_text"]["fr"].strip()
            assert slide["question"]["prompt"].strip()
            assert slide["question"]["advance_on_timeout"] is True
            assert 10 <= slide["question"]["timeout_seconds"] <= 30


def test_all_manifest_file_visuals_exist_in_frontend_public():
    for manifest in _manifests():
        for activity in manifest["activities"]:
            for slide in activity["slides"]:
                visual = slide.get("visual") or {}
                url = visual.get("url")
                if url and url.startswith("/media/"):
                    media_path = url.split("?", 1)[0]
                    assert (PROJECT_ROOT / "frontend" / "public" / media_path.lstrip("/")).exists(), url


def test_each_course_has_a_complete_catalog_cover():
    for manifest in _manifests():
        catalog = manifest.get("catalog") or {}
        cover = catalog.get("cover_image") or ""

        assert catalog.get("summary", "").strip()
        assert len(catalog.get("essential_topics") or []) >= 4
        assert cover.startswith("/media/images/course-covers/")
        assert (PROJECT_ROOT / "frontend" / "public" / cover.lstrip("/")).exists()


def test_all_manifest_schema_visuals_exist_in_validated_registry():
    declared_ids = set()
    for path in SCHEMA_REGISTRY_DIR.glob("schemas_*.ts"):
        declared_ids |= set(re.findall(r"\bid:\s*'([^']+)'", path.read_text(encoding="utf-8")))
    referenced_ids = {
        slide["visual"]["schema_id"]
        for manifest in _manifests()
        for activity in manifest["activities"]
        for slide in activity["slides"]
        if (slide.get("visual") or {}).get("kind") == "schema"
    }

    assert {
        "svt_cellule_mitochondrie",
        "svt_mitochondrie_structure",
        "svt_fibre_musculaire",
        "svt_muscle_sarcomere",
    }.issubset(declared_ids)
    assert referenced_ids <= declared_ids


def test_first_physics_chemistry_and_math_courses_are_complete_and_timed():
    expected = {"phys_ch1_waves", "chem_ch1_kinetics", "math_ch1_limits"}
    manifests = [manifest for manifest in _manifests() if manifest.get("stable_id") in expected]

    assert {manifest["stable_id"] for manifest in manifests} == expected
    assert sum(len(manifest["activities"]) for manifest in manifests) == 14
    assert sum(len(activity["slides"]) for manifest in manifests for activity in manifest["activities"]) == 28
    for manifest in manifests:
        assert manifest["status"] == "draft"
        assert manifest["lesson_match"]
        assert manifest["intent_aliases"]
        for activity in manifest["activities"]:
            assert 15 <= activity["duration_minutes"] <= 20
            assert activity["objective_ids"]
            assert len(activity["slides"]) >= 2
            for slide in activity["slides"]:
                assert slide["speech_text"]["fr"].strip()
                assert slide["speech_text"]["mixed"].strip()
                assert slide["question"]["prompt"].strip()
                assert slide["question"]["advance_on_timeout"] is True
                assert 10 <= slide["question"]["timeout_seconds"] <= 30


def test_all_declarative_course_visuals_pass_the_server_normaliser():
    from app.services.scientific_visual_skill import normalize_scientific_visual

    for manifest in _manifests():
        for activity in manifest["activities"]:
            for slide in activity["slides"]:
                visual = slide.get("visual") or {}
                if visual.get("kind") == "scientific":
                    assert normalize_scientific_visual(visual.get("scientific")) is not None, slide["id"]


def test_limit_course_does_not_teach_lhopital_outside_the_reference_methods():
    math_manifest = COURSE_DIR / "math_ch1_limits_course_v1.json"
    math_schema = SCHEMA_REGISTRY_DIR / "schemas_math.ts"
    content = math_manifest.read_text(encoding="utf-8") + math_schema.read_text(encoding="utf-8")

    assert "hospital" not in content.casefold()


def test_answer_keys_are_removed_from_student_payload():
    service = CoursePlayerService()
    source = {
        "id": "slide",
        "question": {
            "type": "qcm",
            "answer_key": "A",
            "accepted_answers": ["A"],
            "evaluation_regex": "^A$",
        },
    }
    public = service._public_slide(source, [])

    assert public["question"] == {"type": "qcm"}
    assert source["question"]["answer_key"] == "A"


def test_only_published_audio_matching_current_speech_is_exposed():
    service = CoursePlayerService()
    speech = "Texte vérifié."
    source = {"id": "slide", "speech_text": {"fr": speech}, "question": {}}
    current_hash = hashlib.sha256(speech.encode("utf-8")).hexdigest()
    public = service._public_slide(source, [
        {"language": "fr", "file_path": "/old.mp3", "speech_hash": "old", "status": "published"},
        {"language": "mixed", "file_path": "/current.mp3", "speech_hash": current_hash, "status": "published"},
        {"language": "ar", "file_path": "/draft.mp3", "speech_hash": current_hash, "status": "generated"},
    ])

    assert public["audio"] == {
        "mixed": {
            "url": "/current.mp3",
            "duration_ms": None,
            "version": 1,
            "speech_hash": current_hash,
            "status": "published",
        }
    }


def test_local_answer_evaluation_and_timeout_feedback():
    service = CoursePlayerService()
    correct, _, requeue = asyncio.run(service.evaluate_attempt({
        "slide_id": "energy_a02_s01",
        "answer": "Faux",
        "outcome": "answered",
    }))
    skipped, _, skipped_requeue = asyncio.run(service.evaluate_attempt({
        "slide_id": "energy_a02_s01",
        "outcome": "skipped_timeout",
    }))

    assert correct is True
    assert requeue is False
    assert skipped is None
    assert skipped_requeue is True


def test_explicit_natural_language_requests_resolve_to_the_expected_course():
    service = CoursePlayerService()

    energy = service.match_manifest_intent("Je veux un cours sur l'ATP")
    typo_energy = service.match_manifest_intent(
        "Donne-moi un curs sur la consomation de la matière organique"
    )
    muscle = service.match_manifest_intent("Je veux réviser la contraction musculaire")
    waves = service.match_manifest_intent("Je veux commencer le cours sur les ondes mécaniques progressives")
    kinetics = service.match_manifest_intent("Donne-moi un cours sur les facteurs cinétiques")
    limits = service.match_manifest_intent("Je veux réviser le cours sur les limites et continuité")

    assert energy and energy["stable_id"] == "svt_ch1_energy"
    assert typo_energy and typo_energy["stable_id"] == "svt_ch1_energy"
    assert muscle and muscle["stable_id"] == "svt_ch1_muscle"
    assert waves and waves["stable_id"] == "phys_ch1_waves"
    assert kinetics and kinetics["stable_id"] == "chem_ch1_kinetics"
    assert limits and limits["stable_id"] == "math_ch1_limits"


def test_ordinary_topic_question_does_not_open_the_full_course():
    service = CoursePlayerService()

    assert service.match_manifest_intent("C'est quoi l'ATP ?") is None
    assert service.match_manifest_intent("Pourquoi le muscle se contracte ?") is None
    assert service.match_manifest_intent("Aide-moi") is None


def test_tutor_recognises_a_course_published_only_from_the_admin_editor(monkeypatch):
    rows = [{
        "id": "deck-admin",
        "lesson_id": "lesson-admin",
        "title": "Équilibre chimique",
        "status": "published",
        "metadata": {
            "stable_id": "chem_equilibre_admin",
            "intent_aliases": ["cours sur l'équilibre chimique"],
            "lesson_match": ["équilibre chimique"],
        },
    }]

    class FakeQuery:
        def select(self, *_args, **_kwargs):
            return self

        def eq(self, key, value):
            assert (key, value) == ("status", "published")
            return self

        def execute(self):
            return SimpleNamespace(data=rows)

    class FakeAdmin:
        def table(self, name):
            assert name == "course_decks"
            return FakeQuery()

    monkeypatch.setattr(course_player_module, "get_supabase_admin", lambda: FakeAdmin())

    matched = CoursePlayerService().match_course_intent(
        "Je veux commencer le cours sur l'équilibre chimique"
    )

    assert matched and matched["stable_id"] == "chem_equilibre_admin"
    assert matched["_lesson_id"] == "lesson-admin"


def test_catalog_cards_and_tutor_requests_use_the_same_manifests(monkeypatch):
    subject_id = "subject-svt"
    lessons = [
        {
            "id": "lesson-energy",
            "title_fr": "Consommation de la matière organique",
            "chapter_id": "chapter-energy",
            "chapters": {
                "id": "chapter-energy",
                "title_fr": "Libération de l'énergie",
                "subject_id": subject_id,
                "subjects": {"id": subject_id, "name_fr": "SVT"},
            },
        },
        {
            "id": "lesson-muscle",
            "title_fr": "Rôle du muscle strié squelettique",
            "chapter_id": "chapter-muscle",
            "chapters": {
                "id": "chapter-muscle",
                "title_fr": "Conversion de l'énergie",
                "subject_id": subject_id,
                "subjects": {"id": subject_id, "name_fr": "SVT"},
            },
        },
    ]

    class FakeQuery:
        def __init__(self, rows):
            self.rows = rows

        def select(self, *_args, **_kwargs):
            return self

        def execute(self):
            return SimpleNamespace(data=self.rows)

    class FakeAdmin:
        def table(self, name):
            return FakeQuery(lessons if name == "lessons" else [])

    monkeypatch.setattr(course_player_module, "get_supabase_admin", lambda: FakeAdmin())
    monkeypatch.setattr(
        course_player_module.subject_access_service,
        "get_context",
        lambda _student: {
            "subjects": [{
                "id": subject_id,
                "name_fr": "Sciences de la Vie et de la Terre",
                "name_ar": "",
                "catalog_key": "svt",
            }],
        },
    )

    service = CoursePlayerService()
    catalog = asyncio.run(service.get_catalog({"id": "student"}))
    courses = catalog["subjects"][0]["courses"]

    assert catalog["total_courses"] == 2
    assert {course["lesson_id"] for course in courses} == {"lesson-energy", "lesson-muscle"}
    for course in courses:
        matched = service.match_manifest_intent(course["tutor_request"])
        assert matched and matched["stable_id"] == course["stable_id"]


def test_first_courses_are_sorted_into_their_subject_folders(monkeypatch):
    subjects = [
        {"id": "subject-physics", "name_fr": "Physique", "catalog_key": "physique"},
        {"id": "subject-chemistry", "name_fr": "Chimie", "catalog_key": "chimie"},
        {"id": "subject-math", "name_fr": "Mathématiques", "catalog_key": "mathematiques"},
    ]
    lessons = [
        {
            "id": "lesson-waves", "title_fr": "Laboratoire guidé — Ondes mécaniques progressives",
            "chapters": {"id": "chapter-waves", "title_fr": "Ondes mécaniques progressives", "subject_id": "subject-physics", "subjects": subjects[0]},
        },
        {
            "id": "lesson-kinetics", "title_fr": "Transformations lentes et transformations rapides",
            "chapters": {"id": "chapter-kinetics", "title_fr": "Transformations lentes et rapides", "subject_id": "subject-chemistry", "subjects": subjects[1]},
        },
        {
            "id": "lesson-limits", "title_fr": "Limites et continuite",
            "chapters": {"id": "chapter-limits", "title_fr": "Limites et continuite", "subject_id": "subject-math", "subjects": subjects[2]},
        },
    ]

    class FakeQuery:
        def __init__(self, rows):
            self.rows = rows

        def select(self, *_args, **_kwargs):
            return self

        def execute(self):
            return SimpleNamespace(data=self.rows)

    class FakeAdmin:
        def table(self, name):
            return FakeQuery(lessons if name == "lessons" else [])

    monkeypatch.setattr(course_player_module, "get_supabase_admin", lambda: FakeAdmin())
    monkeypatch.setattr(
        course_player_module.subject_access_service,
        "get_context",
        lambda _student: {"subjects": subjects},
    )

    catalog = asyncio.run(CoursePlayerService().get_catalog({"id": "student"}))
    courses_by_subject = {
        folder["catalog_key"]: {course["stable_id"] for course in folder["courses"]}
        for folder in catalog["subjects"]
    }

    assert catalog["total_courses"] == 3
    assert courses_by_subject == {
        "physique": {"phys_ch1_waves"},
        "chimie": {"chem_ch1_kinetics"},
        "mathematiques": {"math_ch1_limits"},
    }


def test_new_simulations_expose_platform_bridge_contract():
    simulation_sources = [
        (PROJECT_ROOT / "frontend/public/media/simulations/svt/ch1_consommation_matiere_organique/atp-adp/index.html").read_text(encoding="utf-8"),
        (PROJECT_ROOT / "frontend/public/media/simulations/svt/ch1_consommation_matiere_organique/chimiosmose/index.html").read_text(encoding="utf-8"),
        (PROJECT_ROOT / "frontend/public/media/simulations/svt/ch1_consommation_matiere_organique/muscle/contraction/index.html").read_text(encoding="utf-8"),
        (PROJECT_ROOT / "frontend/public/media/simulations/svt/ch2_information_genetique/expression/index.html").read_text(encoding="utf-8"),
        (PROJECT_ROOT / "frontend/public/media/simulations/physics/advanced/waves/index.html").read_text(encoding="utf-8"),
        (
            PROJECT_ROOT / "frontend/public/media/simulations/chimie/labs/cinetique/index.html"
        ).read_text(encoding="utf-8") + (
            PROJECT_ROOT / "frontend/public/media/simulations/chimie/shared/chem-lab.js"
        ).read_text(encoding="utf-8"),
    ]
    for source in simulation_sources:
        assert "simulation_manifest" in source
        assert "simulation_state" in source
        assert "postMessage" in source
        assert "set_variant" in source
        assert "reset" in source


def test_gene_expression_simulation_exposes_automatic_step_by_step_demo():
    simulation_dir = (
        PROJECT_ROOT
        / "frontend/public/media/simulations/svt/ch2_information_genetique/expression"
    )
    source = (simulation_dir / "index.html").read_text(encoding="utf-8")

    assert "const STEPS = [" in source
    assert "three.module.min.js" in source
    assert (simulation_dir / "vendor/three.module.min.js").is_file()
    assert (simulation_dir / "vendor/three.core.min.js").is_file()
    assert (simulation_dir / "vendor/THREE-LICENSE.txt").is_file()
    assert "dna_open" in source
    assert "rna_base_" in source
    assert "mrna_export" in source
    assert "small_subunit" in source
    assert "initiator_trna" in source
    assert "large_subunit" in source
    assert "trna_glu" in source
    assert "peptide_release" in source
    assert "protein_fold" in source
    assert "TAC CTT AAA GGC ATT" in source
    assert "['AUG', 'GAA', 'UUU', 'CCG', 'UAA']" in source
    assert "Adénine" in source
    assert "Méthionine" in source
    assert "Phénylalanine" in source
    assert "pauseSimulation" in source
    assert "nextStep" in source
    assert "previousStep" in source
    assert "getSimulationState" in source
    assert "simulation_manifest" in source
    assert "simulation_state" in source
    assert 'id="startButton"' in source
    assert 'id="pauseButton"' in source
    assert 'id="restartButton"' in source


def test_slide_scientific_visual_is_normalised_before_reaching_the_browser():
    """Une figure de diapositive passe le même filtre que celles du tableau."""
    slide = {
        "visual": {
            "kind": "scientific",
            "scientific": {
                "engine": "cytoscape",
                "title": "Respiration",
                "nodes": [{"id": "glucose", "label": "Glucose"}, {"id": "pyruvate", "label": "Pyruvate"}],
                "edges": [{"from": "glucose", "to": "pyruvate", "label": "Glycolyse"}],
            },
        },
        "question": {"prompt": "?", "answer_key": "secret"},
    }

    public = CoursePlayerService._public_slide(slide, [])

    assert public["visual"]["scientific"]["engine"] == "cytoscape"
    assert len(public["visual"]["scientific"]["nodes"]) == 2
    assert "answer_key" not in public["question"]


def test_slide_scientific_visual_refuses_an_unknown_engine():
    slide = {
        "visual": {"kind": "scientific", "scientific": {"engine": "javascript", "code": "alert(1)"}},
        "question": {},
    }

    public = CoursePlayerService._public_slide(slide, [])

    # La diapositive part quand même : le lecteur retombe sur le texte essentiel.
    assert public["visual"]["scientific"] is None


def test_schema_catalog_matches_the_browser_registry():
    """Le catalogue serveur nomme EXACTEMENT les schémas que le front sait rendre.

    Sans cette égalité, le tuteur cite des identifiants qui n'affichent rien —
    ou ignore des schémas déjà dessinés. Régénérer avec
    `python tools/generate_schema_catalog.py`.
    """
    from app.services.schema_catalog import SCHEMA_IDS

    declared = set()
    for path in (PROJECT_ROOT / "frontend/src/components/session/schemas").glob("schemas_*.ts"):
        declared |= set(re.findall(r"\bid:\s*'([a-z]+_[a-z0-9_]+)',\s*\n?\s*title:", path.read_text(encoding="utf-8")))

    assert declared, "aucun schéma trouvé dans la bibliothèque du navigateur"
    assert declared == set(SCHEMA_IDS)
