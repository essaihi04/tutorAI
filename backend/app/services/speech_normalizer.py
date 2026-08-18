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
_SUBSCRIPT_TRANSLATION = str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")

# ── Formules, sigles et charges : la convention du corpus d'entraînement ──
#
# Le modèle Academy a appris ses prononciations sur les transcriptions
# normalisées par `scripts/normalize_combined_dataset.py` (dépôt DARIJA TTS).
# Ce corpus est donc la RÉFÉRENCE : quand on lui envoie une forme écrite qu'il
# n'a jamais vue à l'entraînement, il improvise, et c'est là que naissent les
# mots mal dits. Les trois tables et les deux fonctions qui suivent
# reproduisent `ELEMENTS`, `ACRONYMES_MOTS`, `epeler()` et
# `developper_formule()` de ce script.
#
# Convention retenue, celle du corpus : lettres latines en capitales (le modèle
# a appris à dire « ache » en voyant « H »), chiffres et signes en FRANÇAIS
# même au milieu d'une phrase en darija. « H3O+ » se dit donc « H trois O
# plus », dans les deux langues.

# Noms des éléments, pour les IONS MONOATOMIQUES seulement : « Ca²⁺ » se dit
# « calcium deux plus » en classe, pas « cé a deux plus ». Épeler un symbole de
# deux lettres ne s'entend pas — le corpus le fait, mais c'est le seul endroit
# où on s'en écarte volontairement, et l'écart est décidé.
#
# Deux limites, tenues exprès :
#  • les symboles d'UNE lettre n'y sont pas. « H plus », « O deux moins » sont
#    ce que dit le professeur, et une lettre seule ne s'entend jamais de
#    travers ;
#  • rien ne s'applique aux formules à plusieurs éléments. « H3O+ » reste
#    « H trois O plus » : personne ne dit « hydrogène trois oxygène plus ».
_NOMS_ELEMENTS = {
    "He": "hélium", "Li": "lithium", "Be": "béryllium", "Ne": "néon",
    "Na": "sodium", "Mg": "magnésium", "Al": "aluminium", "Si": "silicium",
    "Cl": "chlore", "Ar": "argon", "Ca": "calcium", "Sc": "scandium",
    "Ti": "titane", "Cr": "chrome", "Mn": "manganèse", "Fe": "fer",
    "Co": "cobalt", "Ni": "nickel", "Cu": "cuivre", "Zn": "zinc",
    "Ga": "gallium", "Ge": "germanium", "As": "arsenic", "Se": "sélénium",
    "Br": "brome", "Kr": "krypton", "Rb": "rubidium", "Sr": "strontium",
    "Zr": "zirconium", "Nb": "niobium", "Mo": "molybdène", "Ag": "argent",
    "Cd": "cadmium", "In": "indium", "Sn": "étain", "Sb": "antimoine",
    "Te": "tellure", "Xe": "xénon", "Cs": "césium", "Ba": "baryum",
    "Pt": "platine", "Au": "or", "Hg": "mercure", "Pb": "plomb",
    "Bi": "bismuth", "Ra": "radium", "Ac": "actinium", "Th": "thorium",
    "Pa": "protactinium",
}

# Les symboles reconnus dans une formule, dérivés de la table ci-dessus pour
# qu'il n'y ait rien à tenir à jour deux fois.
#
# La liste est volontairement incomplète : « Ce », « Or », « Ni » sont aussi des
# mots français ou de la darija translittérée. Y ajouter un symbole ambigu
# abîmerait des phrases entières — la contrepartie étant qu'un élément rare
# repart en lettres, ce qui ne s'entend pas.
_ELEMENTS_DEUX_LETTRES = frozenset(_NOMS_ELEMENTS)

# Chiffres romains, qui ont la forme d'un sigle sans en être un. Le cours de
# SVT en est plein — « Prophase I », « Anaphase II », « Méiose II » — et les
# épeler donnait « Anaphase I I ». Liste explicite plutôt que règle générale :
# elle ne peut pas se tromper sur un vrai sigle.
_CHIFFRES_ROMAINS = {
    "II": 2, "III": 3, "IV": 4, "VI": 6, "VII": 7, "VIII": 8, "IX": 9,
    "XI": 11, "XII": 12, "XIII": 13, "XIV": 14, "XV": 15, "XVI": 16,
    "XVII": 17, "XVIII": 18, "XIX": 19, "XX": 20,
}

# Sigles qui se disent comme un mot, jamais lettre par lettre.
# Reprise EXACTE de `ACRONYMES_MOTS` du corpus. Ne rien y ajouter au jugé :
# mesuré sur les 9 997 transcriptions du corpus, y mettre « PIB » faisait dire
# « Pib » 183 fois, alors que le professeur épelle « P I B ».
_SIGLES_LUS_COMME_MOTS = frozenset({
    "MASI", "SIDA", "OPEP", "OTAN", "ONU", "UNESCO", "OCDE", "SMIG", "SMAG",
    "OPCVM", "ADEME", "AMO", "RAMED",
})

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
        "kHz": ("كيلوهرتز", "كيلوهرتز"), "MHz": ("ميغاهرتز", "ميغاهرتز"),
        "GHz": ("غيغاهرتز", "غيغاهرتز"), "hPa": ("هيكتوباسكال", "هيكتوباسكالات"),
        "nm": ("نانومتر", "نانومترات"), "µm": ("ميكرومتر", "ميكرومترات"),
        "μm": ("ميكرومتر", "ميكرومترات"), "kJ": ("كيلوجول", "كيلوجولات"),
        "kW": ("كيلوواط", "كيلوواطات"), "mV": ("ميليفولت", "ميليفولتات"),
        "mA": ("ميلي أمبير", "ميلي أمبيرات"), "Pa": ("باسكال", "باسكالات"),
        "°F": ("درجة فهرنهايت", "درجات فهرنهايت"),
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
        # Une charge COLLÉE appartient à l'espèce chimique, pas au voisinage :
        # l'entrée « O2 » du lexique avalait « O2-» et laissait le tiret
        # orphelin (« o deux-»). Mais le signe ne compte comme charge que s'il
        # n'ouvre pas un mot : « pH-mètre » et « ADN-polymérase » doivent
        # continuer de passer par le lexique.
        pattern = (
            rf"(?<![\w]){re.escape(source)}"
            rf"(?![\w])(?![+-](?![A-Za-zÀ-ÖØ-öø-ÿ]))"
        )
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
    """Expand units written without a number, for example ``(Hz)``.

    Les unités COMPOSÉES y passent aussi. « la concentration est en mol/L » n'a
    pas de nombre devant, donc `_replace_units` ne la voyait pas et le repli
    générique la lisait « mol sur L ». Le corpus d'entraînement, lui, développe
    ces unités sans condition — d'où l'alignement.

    Restreint aux symboles composés (une barre ou un point médian) : un « m »
    ou un « L » seul est le plus souvent une grandeur ou une variable, pas une
    unité, et l'étendre casserait les formules.
    """
    replacements = {
        "Hz": "هرتز" if lang == "ar" else "hertz",
        "Hertz": "هرتز" if lang == "ar" else "hertz",
        "kHz": "كيلوهرتز" if lang == "ar" else "kilohertz",
        "MHz": "ميغاهرتز" if lang == "ar" else "mégahertz",
        "GHz": "غيغاهرتز" if lang == "ar" else "gigahertz",
    }
    for source, spoken in replacements.items():
        text = re.sub(rf"(?<![\w]){re.escape(source)}(?![\w])", spoken, text)

    units = _UNITS_AR if lang == "ar" else _UNITS_FR
    composees = [symbole for symbole in units if any(c in symbole for c in "/·.")]
    for symbole in sorted(composees, key=len, reverse=True):
        text = re.sub(
            rf"(?<![\w]){re.escape(symbole)}(?![\w])", units[symbole][1], text
        )
    return text


def _epeler_code(code: str) -> str:
    """« ADN » → « A D N ». Copie de `epeler()` du corpus d'entraînement."""
    morceaux: list[str] = []
    for caractere in code:
        if caractere.isdigit():
            morceaux.append(num2words(int(caractere), lang="fr"))
        elif caractere.isalpha():
            morceaux.append(caractere.upper())
    return " ".join(morceaux)


def _developper_formule(code: str) -> str:
    """« H3O » → « H trois O » ; « C6H12O6 » → « C six H douze O six ».

    Copie de `developper_formule()` du corpus d'entraînement. Les chiffres
    consécutifs forment un seul nombre — « H12 » se dit « H douze », pas
    « H un deux ».
    """
    morceaux: list[str] = []
    i = 0
    while i < len(code):
        caractere = code[i]
        if caractere.isalpha():
            duo = code[i:i + 2]
            if duo in _ELEMENTS_DEUX_LETTRES:
                morceaux.append(_epeler_code(duo))
                i += 2
                continue
            morceaux.append(caractere.upper())
            i += 1
        elif caractere.isdigit():
            j = i
            while j < len(code) and code[j].isdigit():
                j += 1
            morceaux.append(num2words(int(code[i:j]), lang="fr"))
            i = j
        else:
            i += 1
    return " ".join(morceaux)


def _suite_d_elements(code: str) -> str | None:
    """« NaCl » → « N A C L ». `None` si ce n'est pas une suite de symboles.

    Le refus est essentiel : « Newton » commence par « Ne », qui EST un
    élément. Un mot ordinaire finit toujours par une minuscule que la boucle
    ne sait pas consommer, et c'est ce qui le protège de l'épellation.
    """
    morceaux: list[str] = []
    i = 0
    while i < len(code):
        if code[i:i + 2] in _ELEMENTS_DEUX_LETTRES:
            morceaux.append(_epeler_code(code[i:i + 2]))
            i += 2
        elif code[i].isupper():
            morceaux.append(code[i].upper())
            i += 1
        else:
            return None
    return " ".join(morceaux) if len(morceaux) >= 2 else None


# Un jeton candidat : un mot latin, suivi d'une charge ionique éventuelle. Le
# motif attrape TOUS les mots ; c'est `_epeler_formules_et_sigles` qui décide,
# en Python, lesquels sont des formules — une condition lisible valant mieux
# ici qu'une expression rationnelle que personne ne saura relire.
#
# La charge s'écrit de deux façons, et de deux seulement : collée au symbole
# (« Cl-», « Fe3+ ») ou détachée avec son compte (« SO4 2-»). Accepter une
# espace SANS compte suffirait à prendre un tiret de ponctuation pour une
# charge : « Ne - regarde » devenait « néon moins regarde ».
_JETON_LATIN = re.compile(
    r"(?<![\w])([A-Za-z][A-Za-z0-9]*)"        # 1 : le code
    r"(?:\s*(\d+)\s*([+-])|([+-]))?"          # 2,3 : charge comptée · 4 : collée
    r"(?![\w])"
)

# Charge écrite en exposant : « Ca²⁺ », « SO₄²⁻ ». Ramenée en ASCII AVANT
# `_replace_powers`, sans quoi « Ca²⁺ » se disait « Ca au carré » suivi d'un
# « ⁺ » muet : une charge n'est pas une puissance.
#
# Ce qui distingue les deux, c'est la POSITION du signe. Dans une charge il
# termine l'exposant (« ²⁺ ») ; dans une puissance négative il l'ouvre
# (« 10⁻³ »). Sans le garde-fou de fin, « 10⁻³ » devenait « dix-³ » — un
# exposant perdu au milieu d'un calcul de concentration.
#
# L'espace devant la charge est nécessaire elle aussi : sans elle, le chiffre
# de la charge se collait à celui de la formule et « SO₄²⁻ » devenait
# « SO42- », prononcé « S O quarante-deux moins ».
_CHARGE_EXPOSANT = re.compile(
    r"(?<=[A-Za-z0-9])([⁰¹²³⁴⁵⁶⁷⁸⁹]*)([⁺⁻])(?![⁰¹²³⁴⁵⁶⁷⁸⁹])"
)


def _ramener_charges_en_ascii(text: str) -> str:
    text = text.translate(_SUBSCRIPT_TRANSLATION)
    return _CHARGE_EXPOSANT.sub(
        lambda m: (" " if m.group(1) else "")
        + m.group(1).translate(_SUPERSCRIPT_TRANSLATION)
        + ("+" if m.group(2) == "⁺" else "-"),
        text,
    )


def _epeler_formules_et_sigles(text: str) -> str:
    """Dit les formules chimiques et les sigles inconnus, à la façon du corpus.

    Ce qui n'est reconnu ni comme formule, ni comme suite d'éléments, ni comme
    sigle repart intact : un mot français ou darija ne doit jamais être épelé.
    """
    def traiter(match: re.Match[str]) -> str:
        code, nombre = match.group(1), match.group(2)
        signe = match.group(3) or match.group(4)

        # « Fe3+ » : le chiffre collé au signe compte les CHARGES, il n'est pas
        # un indice de formule. On le détache quand ce qui reste est un symbole
        # d'élément — « H3O+ » ne finit pas par un chiffre, il n'est donc pas
        # concerné, et « SO4-» non plus puisque « SO » n'est pas un symbole.
        if signe is not None and not nombre:
            tronc = code.rstrip("0123456789")
            if tronc != code and tronc in _NOMS_ELEMENTS:
                code, nombre = tronc, code[len(tronc):]

        # Une charge signe une espèce chimique : « Cl⁻ », « Na⁺ » n'ont qu'un
        # symbole, et sans cette exception ils repartaient bruts alors que le
        # même symbole dans « NaCl » était bien dit.
        espece_chargee = signe is not None and re.fullmatch(r"(?:[A-Z][a-z]?)+", code)

        if code in _CHIFFRES_ROMAINS and not espece_chargee:
            dit = num2words(_CHIFFRES_ROMAINS[code], lang="fr")
        elif re.fullmatch(r"[A-Z]{2,5}", code) and not espece_chargee:
            dit = code.capitalize() if code in _SIGLES_LUS_COMME_MOTS else _epeler_code(code)
        elif espece_chargee and code in _NOMS_ELEMENTS:
            # Un ion monoatomique se nomme, il ne s'épelle pas.
            dit = _NOMS_ELEMENTS[code]
        elif re.search(r"\d", code) and code[0].isupper():
            dit = _developper_formule(code)
        elif espece_chargee:
            dit = _developper_formule(code)
        else:
            dit = _suite_d_elements(code) if re.fullmatch(r"(?:[A-Z][a-z]?){2,5}", code) else None

        if dit is None:
            return match.group(0)
        if signe is None:
            return dit
        # La charge se dit après le symbole : « calcium deux plus ».
        charge = "plus" if signe == "+" else "moins"
        if nombre:
            charge = f"{num2words(int(nombre), lang='fr')} {charge}"
        return f"{dit} {charge}"

    return _JETON_LATIN.sub(traiter, text)


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
    # Table complétée d'après `SYMBOLES` du corpus d'entraînement : tout ce qui
    # restait ici passait brut au modèle, qui inventait alors une lecture.
    if lang == "ar":
        replacements = {
            "≈": " تقريبا يساوي ", "≠": " لا يساوي ", "≤": " أصغر أو يساوي ",
            "≥": " أكبر أو يساوي ", "=": " يساوي ", "+": " زائد ", "×": " في ",
            "*": " في ", "÷": " على ", "→": " يعطي ", "⇒": " يستلزم ",
            "↔": " يكافئ ", "∈": " ينتمي إلى ", "∉": " لا ينتمي إلى ",
            "⊂": " مشمول في ", "∞": " ما لا نهاية ", "√": " الجذر المربع ل ",
            "∑": " مجموع ", "Σ": " مجموع ", "∫": " تكامل ", "±": " زائد أو ناقص ",
            "‰": " فالألف ", "°C": " درجة سيلزيوس ", "°": " درجة ",
            "Δ": " دلتا ", "∆": " دلتا ", "λ": " لامبدا ",
            "π": " پي ", "µ": " ميكرو ", "α": " ألفا ", "β": " بيتا ",
            "γ": " غاما ", "θ": " تيتا ", "ρ": " رو ", "σ": " سيغما ",
            "ω": " أوميغا ", "Ω": " أوم ",
        }
    else:
        replacements = {
            "≈": " environ égal à ", "≠": " différent de ",
            "≤": " inférieur ou égal à ", "≥": " supérieur ou égal à ",
            "=": " égal ", "+": " plus ", "×": " fois ", "*": " fois ",
            "÷": " divisé par ", "→": " donne ", "⇒": " implique ",
            "↔": " équivaut à ", "∈": " appartient à ",
            "∉": " n'appartient pas à ", "⊂": " inclus dans ",
            "∞": " l'infini ", "√": " racine carrée de ", "∑": " somme de ",
            "Σ": " somme de ", "∫": " intégrale de ", "±": " plus ou moins ",
            "‰": " pour mille ", "°C": " degrés Celsius ", "°": " degrés ",
            "Δ": " delta ", "∆": " delta ",
            "λ": " lambda ", "π": " pi ", "µ": " micro ", "α": " alpha ",
            "β": " bêta ", "γ": " gamma ", "θ": " thêta ", "ρ": " rho ",
            "σ": " sigma ", "ω": " oméga ", "Ω": " ohm ",
        }
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
    # Avant les puissances : « Ca²⁺ » est une charge, pas un carré.
    text = _ramener_charges_en_ascii(text)
    text = _replace_powers(text, lang)
    text = _replace_percentages_and_fractions(text, lang)
    text = _replace_ordinals(text, lang)
    # Avant les nombres nus : dans « SO4 2- » le « 2 » est le compte de la
    # charge, pas un nombre du discours. Converti trop tôt, il devenait
    # « deux » et la charge repartait sans son compte.
    text = _epeler_formules_et_sigles(text)
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
