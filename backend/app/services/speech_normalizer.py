"""Convert display text into a form that TTS engines can pronounce reliably.

The tutor keeps the original text for the UI.  This module is used only on
the copy sent to a speech provider.  It deliberately expands ambiguous
graphemes (``25%``, ``SVT``, ``m/s²``...) instead of asking a small TTS model
to infer their pronunciation.
"""
from __future__ import annotations

import json
import re
import unicodedata
from datetime import date
from functools import lru_cache
from pathlib import Path
from typing import Any

from num2words import num2words


_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "tts_pronunciations.json"
_ARABIC_RE = re.compile(r"[\u0600-\u06ff]")
_LATIN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]")
_NUMBER_TOKEN = r"[-+−]?\d{1,3}(?:[ .\u202f]\d{3})*(?:[,.]\d+)?|[-+−]?\d+(?:[,.]\d+)?"

_FR_DIGITS = {
    "0": "zéro", "1": "un", "2": "deux", "3": "trois", "4": "quatre",
    "5": "cinq", "6": "six", "7": "sept", "8": "huit", "9": "neuf",
}
_AR_DIGITS = {
    "0": "صفر", "1": "واحد", "2": "جوج", "3": "ثلاثة", "4": "ربعة",
    "5": "خمسة", "6": "ستة", "7": "سبعة", "8": "ثمانية", "9": "تسعود",
}
_DARIJA_SMALL = {
    0: "صفر", 1: "واحد", 2: "جوج", 3: "ثلاثة", 4: "ربعة",
    5: "خمسة", 6: "ستة", 7: "سبعة", 8: "ثمانية", 9: "تسعود",
    10: "عشرة", 11: "حداش", 12: "طناش", 13: "تلتاش", 14: "ربعتاش",
    15: "خمستاش", 16: "ستاش", 17: "سبعتاش", 18: "تمنتاش", 19: "تسعتاش",
}
_DARIJA_TENS = {
    20: "عشرين", 30: "ثلاثين", 40: "ربعين", 50: "خمسين",
    60: "ستين", 70: "سبعين", 80: "ثمانين", 90: "تسعين",
}
_DARIJA_HUNDREDS = {
    1: "مية", 2: "ميتين", 3: "ثلاثمية", 4: "ربعمية", 5: "خمسمية",
    6: "ستمية", 7: "سبعمية", 8: "ثمانمية", 9: "تسعمية",
}
_FR_MONTHS = (
    "", "janvier", "février", "mars", "avril", "mai", "juin", "juillet",
    "août", "septembre", "octobre", "novembre", "décembre",
)
_AR_MONTHS = (
    "", "يناير", "فبراير", "مارس", "أبريل", "ماي", "يونيو", "يوليوز",
    "غشت", "شتنبر", "أكتوبر", "نونبر", "دجنبر",
)
_SUPERSCRIPT_TRANSLATION = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺", "0123456789-+")

# Le modèle Academy lit caractère par caractère. Un article arabe placé juste
# devant un mot français ("الـ motif", "الـ Hertz") devient donc "al motif"
# et casse le code-switching. Cette sécurité retire uniquement ce préfixe
# devant les mots latins dans la copie envoyée au TTS, jamais dans le texte UI.
_ARABIC_ARTICLE_BEFORE_LATIN_RE = re.compile(
    r"(?<![\w\u0600-\u06ff])(?:الـ|ال|لـ|ل)\s*(?=[A-Za-zÀ-ÖØ-öø-ÿ])",
)

# ── Frontières d'écriture ────────────────────────────────────────
#
# Le tuteur parle en code-switching : darija en alphabet arabe, termes
# scientifiques en français. Trois accidents d'écriture cassent le TTS à cet
# endroit précis, et tous les trois sont invisibles à l'œil.

# 1. La TATWEEL (U+0640), ce trait d'étirement typographique que le modèle
#    colle aux prépositions courtes : « فـ le noyau », « بـ la méthode ». Ce
#    n'est pas une lettre — c'est une décoration. Le TTS, lui, la traite
#    comme un caractère et la prononce, ce qui donne un raclement au milieu
#    du mot. On la retire partout : « فـ » redevient « ف ».
_TATWEEL = "ـ"

# 2. Le collage arabe/latin sans espace : « وla protéine », « فle cytoplasme ».
#    Le moteur voit un seul token hybride qu'il ne sait lire dans aucune des
#    deux langues. Un espace suffit à lui rendre deux mots prononçables ;
#    il ne change rien au sens, et le texte affiché à l'élève n'est pas touché.
_FRONTIERE_ECRITURES = re.compile(
    "(?<=[؀-ۿ])(?=[A-Za-zÀ-ÖØ-öø-ÿ])"
    "|"
    "(?<=[A-Za-zÀ-ÖØ-öø-ÿ])(?=[؀-ۿ])"
)


def _separer_ecritures(text: str) -> str:
    """Rend lisible la frontière entre les deux alphabets."""
    return _FRONTIERE_ECRITURES.sub(" ", text.replace(_TATWEEL, ""))


def _ouvrir_pause_apres_deux_points(text: str) -> str:
    """Le deux-points d'annonce mérite une respiration, pas celui d'un ratio.

    Appliqué TÔT, tant que les chiffres sont encore des chiffres : plus loin
    dans la chaîne, « 1:2 » est déjà devenu « un:deux » et le garde-fou
    numérique ne voit plus rien à protéger. Une heure (« 14:30 ») doit elle
    aussi rester intacte, sinon `_replace_times` ne la reconnaît plus.
    """
    return re.sub(r"(?<!\d):(?!\d)(?=\S)", ": ", text)


# Formules que le modèle laisse parfois passer dans le canal oral malgré les
# consignes. Elles sont reformulées en phrases, plutôt que de laisser le TTS
# lire « N égal 1 slash T ».
_KNOWN_SPOKEN_FORMULAS = (
    (re.compile(r"(?i)(?<!\w)(?:la\s+fréquence\s+est\s+)?N\s*=\s*1\s*/\s*T(?!\w)"),
     "la fréquence est égale à un sur la période"),
    (re.compile(r"(?i)(?<!\w)(?:la\s+vitesse\s+est\s+)?v\s*=\s*λ\s*(?:×|x|\*)\s*N(?!\w)"),
     "la vitesse est égale à la longueur d'onde fois la fréquence"),
    (re.compile(r"(?i)(?<!\w)(?:la\s+tension\s+est\s+)?U\s*=\s*R\s*(?:×|x|\*)\s*I(?!\w)"),
     "la tension est égale à la résistance fois l'intensité"),
)

# Longest symbols must be matched first.  Values are (singular, plural).
_UNITS_FR = {
    "mol·L⁻¹": ("mole par litre", "moles par litre"),
    "mol.L⁻¹": ("mole par litre", "moles par litre"),
    "mol/L": ("mole par litre", "moles par litre"),
    "km/h": ("kilomètre par heure", "kilomètres par heure"),
    "m/s²": ("mètre par seconde carrée", "mètres par seconde carrée"),
    "m/s2": ("mètre par seconde carrée", "mètres par seconde carrée"),
    "m/s": ("mètre par seconde", "mètres par seconde"),
    "g/L": ("gramme par litre", "grammes par litre"),
    "mg/L": ("milligramme par litre", "milligrammes par litre"),
    "°C": ("degré Celsius", "degrés Celsius"),
    "°F": ("degré Fahrenheit", "degrés Fahrenheit"),
    "kHz": ("kilohertz", "kilohertz"), "MHz": ("mégahertz", "mégahertz"),
    "GHz": ("gigahertz", "gigahertz"), "hPa": ("hectopascal", "hectopascals"),
    "km": ("kilomètre", "kilomètres"), "cm": ("centimètre", "centimètres"),
    "mm": ("millimètre", "millimètres"), "nm": ("nanomètre", "nanomètres"),
    "µm": ("micromètre", "micromètres"), "μm": ("micromètre", "micromètres"),
    "kg": ("kilogramme", "kilogrammes"), "mg": ("milligramme", "milligrammes"),
    "mL": ("millilitre", "millilitres"), "kJ": ("kilojoule", "kilojoules"),
    "kW": ("kilowatt", "kilowatts"), "mV": ("millivolt", "millivolts"),
    "mA": ("milliampère", "milliampères"), "Hz": ("hertz", "hertz"),
    "Pa": ("pascal", "pascals"), "mol": ("mole", "moles"),
    "m": ("mètre", "mètres"), "s": ("seconde", "secondes"),
    "L": ("litre", "litres"), "g": ("gramme", "grammes"),
    "J": ("joule", "joules"), "W": ("watt", "watts"),
    "V": ("volt", "volts"), "A": ("ampère", "ampères"),
    "Ω": ("ohm", "ohms"),
}
_UNITS_AR = {
    key: (singular, plural) for key, (singular, plural) in {
        "mol·L⁻¹": ("مول لكل لتر", "مولات لكل لتر"),
        "mol.L⁻¹": ("مول لكل لتر", "مولات لكل لتر"),
        "mol/L": ("مول لكل لتر", "مولات لكل لتر"),
        "km/h": ("كيلومتر فالساعة", "كيلومترات فالساعة"),
        "m/s²": ("متر فالثانية مربعة", "أمتار فالثانية مربعة"),
        "m/s2": ("متر فالثانية مربعة", "أمتار فالثانية مربعة"),
        "m/s": ("متر فالثانية", "أمتار فالثانية"),
        "g/L": ("غرام فاللتر", "غرامات فاللتر"),
        "mg/L": ("ميليغرام فاللتر", "ميليغرامات فاللتر"),
        "°C": ("درجة مئوية", "درجات مئوية"),
        "km": ("كيلومتر", "كيلومترات"), "cm": ("سنتيمتر", "سنتيمترات"),
        "mm": ("مليمتر", "مليمترات"), "kg": ("كيلوغرام", "كيلوغرامات"),
        "mg": ("ميليغرام", "ميليغرامات"), "mL": ("ميليلتر", "ميليلترات"),
        "Hz": ("هرتز", "هرتز"), "mol": ("مول", "مولات"),
        "m": ("متر", "أمتار"), "s": ("ثانية", "ثواني"),
        "L": ("لتر", "لترات"), "g": ("غرام", "غرامات"),
        "J": ("جول", "جولات"), "W": ("واط", "واطات"),
        "V": ("فولت", "فولتات"), "A": ("أمبير", "أمبيرات"),
        "Ω": ("أوم", "أومات"),
    }.items()
}


@lru_cache(maxsize=1)
def _load_lexicon() -> dict[str, Any]:
    try:
        data = json.loads(_DATA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"fr": {}, "ar": {}}
    return data if isinstance(data, dict) else {"fr": {}, "ar": {}}


def reload_pronunciation_lexicon() -> None:
    """Clear the lexicon cache after an administrator edits its JSON file."""
    _load_lexicon.cache_clear()


def _speech_language(language: str, text: str) -> str:
    if language == "fr":
        return "fr"
    if language in {"ar", "ma", "darija"}:
        return "ar"
    # A mixed segment written mainly in Latin characters generally contains a
    # French scientific explanation, whereas Arabic script calls for Arabic
    # number/unit words.
    return "ar" if len(_ARABIC_RE.findall(text)) > len(_LATIN_RE.findall(text)) else "fr"


def _clean_number_token(raw: str) -> str:
    value = raw.replace("\u202f", "").replace(" ", "").replace("−", "-")
    # A dot between groups of three digits is a thousands separator; otherwise
    # dots and commas are decimal separators in the tutor's corpus.
    if re.fullmatch(r"[-+]?\d{1,3}(?:\.\d{3})+", value):
        value = value.replace(".", "")
    return value.replace(",", ".")


def _darija_integer_words(value: int) -> str:
    """Natural Moroccan forms for the ranges most common in BAC content."""
    if value < 0:
        return f"ناقص {_darija_integer_words(-value)}"
    if value < 20:
        return _DARIJA_SMALL[value]
    if value < 100:
        tens, unit = divmod(value, 10)
        tens_word = _DARIJA_TENS[tens * 10]
        return tens_word if unit == 0 else f"{_DARIJA_SMALL[unit]} و{tens_word}"
    if value < 1000:
        hundreds, rest = divmod(value, 100)
        prefix = _DARIJA_HUNDREDS[hundreds]
        return prefix if rest == 0 else f"{prefix} و{_darija_integer_words(rest)}"
    if value < 1_000_000:
        thousands, rest = divmod(value, 1000)
        if thousands == 1:
            prefix = "ألف"
        elif thousands == 2:
            prefix = "ألفين"
        elif thousands < 11:
            prefix = f"{_darija_integer_words(thousands)} آلاف"
        else:
            prefix = f"{_darija_integer_words(thousands)} ألف"
        return prefix if rest == 0 else f"{prefix} و{_darija_integer_words(rest)}"
    # Very large values are rare in spoken tutoring. num2words still gives a
    # deterministic Arabic form instead of leaving raw digits to the model.
    return num2words(value, lang="ar")


def _number_words(raw: str, lang: str) -> str:
    value = _clean_number_token(raw)
    sign = ""
    if value.startswith(("-", "+")):
        sign, value = value[0], value[1:]
    if not value or not re.fullmatch(r"\d+(?:\.\d+)?", value):
        return raw

    integer, dot, decimal = value.partition(".")
    try:
        spoken = (
            _darija_integer_words(int(integer))
            if lang == "ar"
            else num2words(int(integer), lang="fr")
        )
    except (NotImplementedError, OverflowError, ValueError):
        spoken = " ".join((_AR_DIGITS if lang == "ar" else _FR_DIGITS)[d] for d in integer)

    if dot:
        digits = _AR_DIGITS if lang == "ar" else _FR_DIGITS
        separator = "فاصلة" if lang == "ar" else "virgule"
        spoken = f"{spoken} {separator} {' '.join(digits[d] for d in decimal)}"
    if sign == "-":
        spoken = f"سالب {spoken}" if lang == "ar" else f"moins {spoken}"
    elif sign == "+":
        spoken = f"موجب {spoken}" if lang == "ar" else f"plus {spoken}"
    return spoken.replace(" , ", " ")


def _is_one(raw: str) -> bool:
    try:
        return float(_clean_number_token(raw)) in {1.0, -1.0}
    except ValueError:
        return False


def _replace_lexicon(text: str, lang: str) -> str:
    section = _load_lexicon().get(lang, {})
    if not isinstance(section, dict):
        return text
    entries: list[tuple[str, str]] = []
    for category in ("formulas", "abbreviations", "names"):
        values = section.get(category, {})
        if isinstance(values, dict):
            entries.extend((str(k), str(v)) for k, v in values.items() if k and v)
    for source, spoken in sorted(entries, key=lambda item: len(item[0]), reverse=True):
        flags = re.IGNORECASE if source in section.get("names", {}) else 0
        pattern = rf"(?<![\w]){re.escape(source)}(?![\w])"
        text = re.sub(pattern, lambda _m, replacement=spoken: replacement, text, flags=flags)
    return text


def _replace_oral_formula_fragments(text: str, lang: str) -> str:
    """Turn common symbolic relations into complete spoken sentences."""
    for pattern, french_phrase in _KNOWN_SPOKEN_FORMULAS:
        if lang == "ar":
            phrase = {
                "la fréquence est égale à un sur la période":
                    "la fréquence كتساوي واحد على la période",
                "la vitesse est égale à la longueur d'onde fois la fréquence":
                    "la vitesse كتساوي la longueur d'onde ف la fréquence",
                "la tension est égale à la résistance fois l'intensité":
                    "la tension كتساوي la résistance ف l'intensité",
            }.get(french_phrase, french_phrase)
        else:
            phrase = french_phrase
        text = pattern.sub(phrase, text)
    return text


def _replace_standalone_units(text: str, lang: str) -> str:
    """Expand units written without a number, for example ``(Hz)``."""
    replacements = {
        "Hz": "هرتز" if lang == "ar" else "hertz",
        "Hertz": "هرتز" if lang == "ar" else "hertz",
        "kHz": "كيلوهرتز" if lang == "ar" else "kilohertz",
        "MHz": "ميغاهرتز" if lang == "ar" else "mégahertz",
        "GHz": "غيغاهرتز" if lang == "ar" else "gigahertz",
    }
    for source, spoken in replacements.items():
        text = re.sub(rf"(?<![\w]){re.escape(source)}(?![\w])", spoken, text)
    return text


def _replace_generic_fraction_bar(text: str) -> str:
    """Make a remaining algebraic slash audible as « sur ».

    Unit expressions such as m/s and mol/L are expanded earlier. This rule is
    limited to short alphanumeric formula fragments so URLs and ordinary prose
    are not changed.
    """
    return re.sub(
        r"(?<![\w/])([A-Za-zα-ωΑ-Ω0-9]+)\s*/\s*([A-Za-zα-ωΑ-Ω0-9]+)(?![\w/])",
        r"\1 sur \2",
        text,
    )


def _normalize_sentence_spacing(text: str) -> str:
    """Give the acoustic model visible pauses after punctuation.

    Le modèle acoustique ne respire que là où il voit une ponctuation. Un
    tuteur qui explique enchaîne naturellement des propositions longues ;
    sans marque, elles sortent d'un seul souffle et deviennent
    incompréhensibles pour un élève qui découvre la notion.
    """
    text = re.sub(r"([.!?;،؛。！？])(?=\S)", r"\1 ", text)

    # Une énumération dictée à l'oral est écrite par le modèle avec des
    # retours à la ligne et sans ponctuation finale. Sans point, les éléments
    # se collent : « la période la fréquence la longueur d'onde ».
    text = re.sub(r"([^\s.!?:;،؛])\s*\n+\s*(?=\S)", r"\1. ", text)

    text = re.sub(r"\s+([,;:،؛])", r"\1", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


def _replace_latex(text: str) -> str:
    text = re.sub(r"\\frac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r"\1/\2", text)
    text = re.sub(r"\\sqrt\s*\{([^{}]+)\}", r" racine carrée de \1 ", text)
    text = re.sub(r"\\text\s*\{([^{}]+)\}", r"\1", text)
    text = text.replace(r"\times", "×").replace(r"\cdot", "·")
    text = text.replace(r"\Delta", "Δ").replace(r"\lambda", "λ")
    text = re.sub(r"([A-Za-z])_\{?(\d+)\}?", r"\1\2", text)
    text = re.sub(r"\^\{([^{}]+)\}", r"^\1", text)
    return text.replace("$$", " ").replace("$", " ").replace(r"\[", " ").replace(r"\]", " ").replace(r"\(", " ").replace(r"\)", " ")


def _replace_dates(text: str, lang: str) -> str:
    months = _AR_MONTHS if lang == "ar" else _FR_MONTHS

    def repl(match: re.Match[str]) -> str:
        day, month, year = map(int, match.groups())
        try:
            date(year, month, day)
        except ValueError:
            return match.group(0)
        return f"{_number_words(str(day), lang)} {months[month]} {_number_words(str(year), lang)}"

    return re.sub(r"(?<!\d)(\d{1,2})[/-](\d{1,2})[/-](\d{4})(?!\d)", repl, text)


def _replace_times(text: str, lang: str) -> str:
    def repl(match: re.Match[str]) -> str:
        hour = match.group(1)
        minute = match.group(2) or match.group(3)
        hour_word = _number_words(hour, lang)
        if not minute or int(minute) == 0:
            return f"{hour_word} heures" if lang == "fr" else f"{hour_word} ساعة"
        minute_word = _number_words(minute, lang)
        return f"{hour_word} heures {minute_word}" if lang == "fr" else f"{hour_word} ساعة و {minute_word} دقيقة"

    return re.sub(
        r"(?<!\w)([01]?\d|2[0-3])(?:\s*[hH](?:\s*([0-5]\d))?(?![A-Za-z])|:([0-5]\d))(?!\d)",
        repl,
        text,
    )


def _replace_units(text: str, lang: str) -> str:
    units = _UNITS_AR if lang == "ar" else _UNITS_FR
    for symbol, (singular, plural) in sorted(units.items(), key=lambda item: len(item[0]), reverse=True):
        pattern = rf"(?<![\w])({_NUMBER_TOKEN})\s*{re.escape(symbol)}(?![\w])"

        def repl(match: re.Match[str], one=singular, many=plural) -> str:
            raw = match.group(1)
            return f"{_number_words(raw, lang)} {one if _is_one(raw) else many}"

        text = re.sub(pattern, repl, text)
    return text


def _replace_scientific_notation(text: str, lang: str) -> str:
    pattern = rf"(?<!\w)({_NUMBER_TOKEN})\s*(?:×|x|\*)\s*10\s*(?:\^\s*)?([⁻⁺−\-+]?\s*[⁰¹²³⁴⁵⁶⁷⁸⁹\d]+)"

    def repl(match: re.Match[str]) -> str:
        coefficient = _number_words(match.group(1), lang)
        exponent = match.group(2).replace(" ", "").replace("−", "-").translate(_SUPERSCRIPT_TRANSLATION)
        power = _number_words(exponent, lang)
        if lang == "ar":
            return f"{coefficient} في عشرة أس {power}"
        return f"{coefficient} fois dix puissance {power}"

    return re.sub(pattern, repl, text, flags=re.IGNORECASE)


def _replace_powers(text: str, lang: str) -> str:
    def superscript_repl(match: re.Match[str]) -> str:
        base, exponent = match.groups()
        exp = exponent.translate(_SUPERSCRIPT_TRANSLATION)
        if exp == "2":
            return f"{base} au carré" if lang == "fr" else f"{base} مربع"
        if exp == "3":
            return f"{base} au cube" if lang == "fr" else f"{base} مكعب"
        label = "أس" if lang == "ar" else "puissance"
        return f"{base} {label} {_number_words(exp, lang)}"

    text = re.sub(r"([\wα-ωΑ-Ω]+)([⁻⁺]?[⁰¹²³⁴⁵⁶⁷⁸⁹]+)", superscript_repl, text)

    def caret_repl(match: re.Match[str]) -> str:
        base, exponent = match.groups()
        label = "أس" if lang == "ar" else "puissance"
        return f"{base} {label} {_number_words(exponent, lang)}"

    return re.sub(r"([\wα-ωΑ-Ω]+)\s*\^\s*([-+]?\d+)", caret_repl, text)


def _replace_percentages_and_fractions(text: str, lang: str) -> str:
    percent_label = "فالمية" if lang == "ar" else "pour cent"
    text = re.sub(
        rf"(?<!\w)({_NUMBER_TOKEN})\s*%",
        lambda m: f"{_number_words(m.group(1), lang)} {percent_label}",
        text,
    )
    fraction_label = "على" if lang == "ar" else "sur"
    return re.sub(
        r"(?<![\w/])([-+]?\d+)\s*/\s*(\d+)(?![\w/])",
        lambda m: f"{_number_words(m.group(1), lang)} {fraction_label} {_number_words(m.group(2), lang)}",
        text,
    )


def _replace_ordinals(text: str, lang: str) -> str:
    if lang != "fr":
        return text

    def repl(match: re.Match[str]) -> str:
        value = int(match.group(1))
        suffix = match.group(2).lower()
        if value == 1:
            return "première" if suffix in {"re", "ère"} else "premier"
        try:
            return num2words(value, lang="fr", to="ordinal")
        except (NotImplementedError, ValueError):
            return f"{_number_words(str(value), 'fr')}ième"

    return re.sub(r"(?<!\w)(\d+)\s*(er|re|ère|e|ème)(?!\w)", repl, text, flags=re.IGNORECASE)


def _replace_remaining_numbers(text: str, lang: str) -> str:
    return re.sub(rf"(?<![\w])({_NUMBER_TOKEN})(?![\w])", lambda m: _number_words(m.group(1), lang), text)


def _replace_math_symbols(text: str, lang: str) -> str:
    if lang == "ar":
        replacements = {"≈": " تقريبا يساوي ", "≠": " لا يساوي ", "≤": " أصغر أو يساوي ", "≥": " أكبر أو يساوي ", "=": " يساوي ", "+": " زائد ", "×": " في ", "*": " في ", "÷": " على ", "→": " يعطي ", "Δ": " دلتا ", "λ": " لامبدا ", "α": " ألفا ", "β": " بيتا ", "γ": " غاما ", "ω": " أوميغا "}
    else:
        replacements = {"≈": " environ égal à ", "≠": " différent de ", "≤": " inférieur ou égal à ", "≥": " supérieur ou égal à ", "=": " égal ", "+": " plus ", "×": " fois ", "*": " fois ", "÷": " divisé par ", "→": " donne ", "Δ": " delta ", "λ": " lambda ", "α": " alpha ", "β": " bêta ", "γ": " gamma ", "ω": " oméga "}
    for symbol, spoken in replacements.items():
        text = text.replace(symbol, spoken)
    return text


def normalize_for_speech(text: str, language: str = "fr") -> str:
    """Return a speakable copy of ``text`` for Academy and cloud TTS engines."""
    if not text:
        return ""
    # NFC keeps semantic superscripts (10⁻³, m/s²) intact. NFKC would flatten
    # them into ambiguous plain characters before we can identify a power.
    text = unicodedata.normalize("NFC", text)
    lang = _speech_language(language, text)
    # En premier : les règles suivantes reconnaissent des MOTS (unités,
    # abréviations, nombres). Une tatweel ou un collage d'alphabets les fait
    # toutes échouer silencieusement.
    text = _separer_ecritures(text)
    text = _ouvrir_pause_apres_deux_points(text)
    text = _replace_latex(text)
    text = _replace_oral_formula_fragments(text, lang)
    # Ne jamais laisser l'article arabe « al » s'accrocher à un terme
    # scientifique français : « la période », pas « الـ période ».
    text = _ARABIC_ARTICLE_BEFORE_LATIN_RE.sub("", text)
    text = _replace_lexicon(text, lang)
    text = _replace_dates(text, lang)
    text = _replace_times(text, lang)
    text = _replace_scientific_notation(text, lang)
    text = _replace_units(text, lang)
    text = _replace_standalone_units(text, lang)
    text = _replace_powers(text, lang)
    text = _replace_percentages_and_fractions(text, lang)
    text = _replace_ordinals(text, lang)
    text = _replace_remaining_numbers(text, lang)
    text = _replace_math_symbols(text, lang)
    text = _replace_generic_fraction_bar(text)
    # Braces and stray TeX commands are not meaningful after the known math
    # constructs above have been expanded.
    text = re.sub(r"\\[A-Za-z]+", " ", text)
    text = text.translate(str.maketrans({"{": " ", "}": " ", "_": " "}))
    text = _normalize_sentence_spacing(text)
    text = re.sub(r"\s+([,.;:!?،])", r"\1", text)
    return text.strip()
