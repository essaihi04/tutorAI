"""Règles de prononciation de la voix (backend/kaggle_tts/texte_parle.py, skill prononciation).
Chaque mot corrigé à l'écoute garde ici son test : une règle cassée referait dire le mot de travers à tous les cours."""
import importlib.util
from pathlib import Path

import pytest

_f = Path(__file__).resolve().parents[2] / "kaggle_tts" / "texte_parle.py"
_spec = importlib.util.spec_from_file_location("texte_parle", _f)
tp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tp)


@pytest.mark.parametrize("ecrit, dit", [
    # 15/11/2026 : « les hématies, il lit t au lieu de si », « cliquer est mal prononcé »
    ("les hématies", "les émassi"),
    ("clique sur la suite", "klik sur la suite"),
    ("cliquer", "kliké"),
    ("deux MeV", "deux méga électron-volts"),
    ("dix millihenrys", "dix millianri"),
    # 16/11/2026 : « siemens » sortait « milliseconde » ; « si mènsse » choisi à l'écoute
    ("quatre virgule six millisiemens par mètre", "quatre virgule six millisi mènsse par mètre"),
    ("huit siemens par mètre", "huit si mènsse par mètre"),
    ("un Siemens", "un si mènsse"),
])
def test_mot_ecrit_comme_il_se_dit(ecrit, dit):
    assert tp.parle(ecrit) == dit


def test_le_texte_sans_mot_corrige_ne_change_pas():
    assert tp.prononciation("la célérité de l'onde") == "la célérité de l'onde"
