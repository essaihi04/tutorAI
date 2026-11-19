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


@pytest.mark.parametrize("ecrit, dit", [
    # 19/11/2026 : « micros est lu avec s à la fin », « écho est lu avec ch », « les unités avec du texte (micro seconde) »
    ("les micros M un", "les micro M un"),
    ("le premier écho", "le premier éko"),
    ("cent microsecondes", "cent micro seconde"),
    ("dix microfarads", "dix micro farad"),
    ("vingt microcoulombs", "vingt micro coulomb"),
    ("les nanomètres", "les nanomètres"),
    ("20 Hz", "vingt hertz"),
    ("6,3 V", "six virgule trois volt"),
    ("0,001 s", "zéro virgule zéro zéro un seconde"),
    ("47 µF", "quarante-sept micro farad"),
    ("Δt = 5 × 0,5 ms", "delta t égale cinq fois zéro virgule cinq milliseconde"),
    ("v = d/Δt", "v égale d sur delta t"),
    ("x → +∞", "x tend vers plus l'infini"),
    ("Zn²⁺ → Zn", "Zn deux plus donne Zn"),
    ("√2", "racine de deux"),
    ("12,5 %", "douze virgule cinq pour cent"),
])
def test_nombres_symboles_unites(ecrit, dit):
    assert tp.parle(ecrit) == dit


@pytest.mark.parametrize("n, dit", [
    (17, "dix-sept"), (21, "vingt et un"), (71, "soixante et onze"), (80, "quatre-vingts"), (81, "quatre-vingt-un"),
    (91, "quatre-vingt-onze"), (200, "deux cents"), (201, "deux cent un"), (1000, "mille"),
    (2024, "deux mille vingt-quatre"), (80000, "quatre-vingt mille"),
])
def test_nombre_fr(n, dit):
    assert tp.nombre_fr(n) == dit


def test_aucun_caractere_invisible_dans_les_regles():
    # un « \b » mal échappé devient 0x08 et la règle ne s'applique jamais (16/11 et 19/11/2026)
    assert chr(8) not in _f.read_text(encoding="utf-8")


@pytest.mark.parametrize("ecrit, dit", [
    # 19/11/2026 : « fœtus » mal lu ; « le fétusse » choisi à l'écoute
    ("كتمشي حتى للفيتوس", "كتمشي حتى ل le fétusse"),
    ("كتمشي فالفيتوس", "كتمشي ف le fétusse"),
    ("الفيتوس", "le fétusse"),
    ("l'épaisseur du fœtus", "l'épaisseur du fétusse"),
    ("le foetus", "le fétusse"),
])
def test_foetus(ecrit, dit):
    assert tp.parle(ecrit) == dit


@pytest.mark.parametrize("ecrit, dit", [
    # 19/11/2026 : écritures sûres des mots rares (scripts/voix/ecritures_sures.py, skill prononciation § 6)
    ("dix ohms", "dix ohm"),
    ("le locus du gène", "le locuss du gène"),
    ("le chlorure de sodium", "le klorure de sodium"),
])
def test_ecritures_sures(ecrit, dit):
    assert tp.parle(ecrit) == dit


@pytest.mark.parametrize("ecrit, dit", [
    # 19/11/2026 (l'utilisateur : « parfois il dit L N, pas ln rassemblé ; appliquer aux autres symboles et fonctions »)
    ("ln2", "ln deux"),
    ("lnx", "ln x"),
    ("la courbe de l n", "la courbe de ln"),
    ("Ln(x)", "ln de (x)"),
    ("ln(e^x) = x", "ln de (e puissance x) égale x"),
    ("ln(1/2) = -ln2", "ln de (un sur deux) égale moins ln deux"),
    ("uₙ₊₁ على uₙ", "u n plus un على u n"),
    ("6x²", "six x au carré"),
    ("f⁻¹", "f moins un"),
    ("u′/u²", "u prime sur u au carré"),
    ("f'(x) = 2x + 1", "f prime de (x) égale deux x plus un"),
    ("deux√x", "deux racine de x"),
    ("L n'y est pas", "L n'y est pas"),
    ("le 3e", "le 3e"),
    ("H₂O", "H deux O"),
])
def test_notation_maths(ecrit, dit):
    assert tp.parle(ecrit) == dit
