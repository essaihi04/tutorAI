"""Texte des cours -> texte « parlé » donné au modèle de voix, écrit comme les transcriptions du corpus d'entraînement
(regles_transcription.md) : le modèle n'a appris que des phrases écrites comme le prof les dit.
Le texte affiché dans le cours ne change pas ; seule la lecture change.
- formules : CO₂ -> C O deux, C6H12O6 -> C six H douze O six, Ca²⁺ -> Ca deux plus, NADH,H⁺ -> NADH H plus ;
- nombres en lettres, toujours en FRANÇAIS (« x plus un », « مختلف على un », « glucose six phosphate ») ;
- chiffres romains des complexes : complexe I/II/III/IV -> un/deux/trois/quatre ;
- arrêts : découpage après « : » et « ; » (0,35 s) et aux virgules des phrases longues (0,22 s).
Test : python texte_parle.py (affiche chaque phrase des cours qui change)."""
import re

FR = "zéro un deux trois quatre cinq six sept huit neuf dix onze douze treize quatorze quinze seize".split()
EXPOSANTS = str.maketrans("₀₁₂₃₄₅₆₇₈₉⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻", "01234567890123456789+-")
SIGLES = ("FADH", "NADH", "NADP", "NAD", "ATP", "ADP", "GTP")
FORMULE = re.compile(r"(?<![\w])([A-Z][A-Za-z0-9₀-₉⁰-⁹²³¹]*[0-9₀-₉⁰-⁹²³¹][A-Za-z0-9₀-₉⁰-⁹²³¹]*)([+⁺⁻-]?)(?![\w])")
ARABE = re.compile("[؀-ۿ]")
LATIN = re.compile("[A-Za-zÀ-ÿ]")


def _formule(mt):
    f, morceaux = mt.group(1).translate(EXPOSANTS), []
    for sg in SIGLES:
        if f.startswith(sg):
            morceaux.append(sg); f = f[len(sg):]; break
    for t in re.findall(r"[A-Z][a-z]?|[0-9]+", f):
        morceaux.append(FR[int(t)] if t.isdigit() and int(t) < len(FR) else t)
    return " ".join(morceaux) + {"+": " plus", "-": " moins"}.get(mt.group(2).translate(EXPOSANTS), "")


def _nombre(p, mt):
    n = int(mt.group(0))
    if n >= len(FR):
        return mt.group(0)
    # Toujours en français (demande de l'utilisateur, 2026-11-04) : « حدا un », jamais « حدا واحد ».
    return FR[n]


# Écriture du corpus v4 (38 852 transcriptions, mesuré le 2026-11-04) : apostrophe droite « ' » 15 438 fois,
# « ’ » jamais ; ni guillemets ni tirets ; « : » 6 fois et « ; » jamais. Le modèle n'a donc appris ni « ’ » ni « ; ».
TYPO = str.maketrans({"’": "'", "‘": "'", "ʼ": "'", "«": "", "»": "", '"': "", "“": "", "”": "",
                      "–": ",", "—": ",", "…": "."})
# Mots d'arabe classique que le prof du corpus ne dit jamais, remplacés par ce qu'il dit à la place.
DARIJA_DU_CORPUS = {"انتبه": "رد البال", "انتبهوا": "ردو البال", "فالحين": "دغيا"}
_DARIJA_RE = re.compile(r"(?<![؀-ۿ])(" + "|".join(DARIJA_DU_CORPUS) + r")(?![؀-ۿ])")


def ponctuation_modele(q):
    """Dernière étape avant le modèle, APRÈS le découpage (qui s'est servi de « : » et « ; » pour les arrêts) :
    ces signes jamais vus à l'entraînement deviennent une virgule."""
    q = re.sub(r"\s*[:;؛]\s*", "، " if ARABE.search(q) else ", ", q).strip()
    return re.sub(r"[،,]\s*$", ".", q) if q[-1:] in "،," else q


def parle(p):
    p = _DARIJA_RE.sub(lambda m: DARIJA_DU_CORPUS[m.group(1)], p.translate(TYPO))
    p = re.sub(r"\s+([,،.])", r"\1", p)          # « important , » (tiret retiré) -> « important, »
    p = re.sub(r"NADH\s*,\s*H\s*(?:[+⁺]|plus\b)", "NADH H plus", p)
    p = re.sub(r"\b([A-Z][a-z]?)([+⁺⁻])(?!\w)", lambda mt: mt.group(1) + (" plus" if mt.group(2) in "+⁺" else " moins"), p)   # H⁺ -> H plus
    p = FORMULE.sub(_formule, p)
    p = notation_maths(p)                          # 19/11/2026 : uₙ₊₁, x², f⁻¹, u′, ln2, deuxracine…
    p = re.sub(r"\b(NADP|NAD)\s*[+⁺]", r"\1 plus", p)
    p = re.sub(r"(?<=[A-Za-z])-([0-9]{1,2})-(?=[A-Za-z])", r" \1 ", p)          # glucose-6-phosphate
    p = re.sub(r"(?<!\w)(?<![0-9][,.])[0-9]{1,2}(?!\w)(?![,.][0-9])", lambda mt: _nombre(p, mt), p)   # pas les décimaux (1,70)
    p = nombres_symboles_unites(p)                 # 19/11/2026 : grands nombres, décimaux, symboles, unités
    p = re.sub(r"\b(complexe)\s+I\b", r"\1 un", p)
    p = re.sub(r"\b(IV|III|II)\b", lambda mt: {"II": "deux", "III": "trois", "IV": "quatre"}[mt.group(1)], p)
    return prononciation(p)


# ── Notations des maths (19 novembre 2026) ─────────────────────────────────────────────────────────────────────────
# Demande de l'utilisateur : « parfois il dit L N, pas ln rassemblé ; appliquer pour toutes les générations, et autres
# symboles ou fonctions ». Inventaire des textes lus après parle() : indices et exposants (uₙ₊₁ 10 fois, uₙ 50, x² …),
# f⁻¹, le prime « ′ », « deuxracine » collé. Chacun est écrit comme le prof le dit.
_SUP = str.maketrans("⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁻⁺", "0123456789n-+")
_SUB = str.maketrans({"₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7", "₈": "8",
                      "₉": "9", "ₙ": "n", "ₖ": "k", "ₚ": "p", "ₘ": "m", "ₓ": "x", "₊": " plus ", "₋": " moins "})


def _exposant(mt):
    e = mt.group(2).translate(_SUP)
    if e == "2":
        return mt.group(1) + " au carré"
    if e == "3":
        return mt.group(1) + " au cube"
    if e == "-1" and mt.group(1) in "fgh":
        return mt.group(1) + " moins un"
    return mt.group(1) + " puissance " + e.replace("-", "moins ").replace("+", "plus ")


def notation_maths(p):
    for motif, dit in _FONCTIONS:                  # ln2, Ln, l n -> « ln » détaché (avant les nombres en lettres)
        p = motif.sub(dit, p)
    # indice collé à une lettre minuscule (uₙ, uₙ₊₁, x₀, y₀ ; les formules chimiques H₂O sont déjà traitées) -> « u n plus un »
    p = re.sub(r"(?<=[a-zα-ω])([₀-₉ₙₖₚₘₓ₊₋]+)", lambda mt: " " + re.sub(r"\s+", " ", mt.group(1).translate(_SUB)).strip(), p)
    # exposant collé (x², x³, x⁴, qⁿ, f⁻¹, e⁻¹) ; les unités (m², s⁻¹) sont traitées plus loin par UNITES
    p = re.sub(r"(?<![^\W\d_])([a-zα-ω)])([⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁻⁺]+)", _exposant, p)
    p = re.sub(r"(?<![\w,.])(\d+)(?=[a-df-zA-Z](?![a-zA-Z]))", r"\1 ", p)      # 6x -> 6 x (puis six x) ; pas « 3e »
    p = re.sub(r"(?<=\w)′", " prime ", p)                                      # u′ -> u prime
    p = re.sub(r"(?<![^\W\d_])([a-zA-Z])'(?=\s?\()", r"\1 prime ", p)           # f'(x) -> f prime (x)
    p = re.sub(r"(?<=[^\W\d_])(?=racine)", " ", p)
    p = re.sub(r"(?:(?<=\s)|^)-(?=[a-zA-Zα-ω√(])", "moins ", p)               # = -ln 2 : moins devant une lettre
    # f(x), ln(x), F(x₀), f prime (x) -> « f de (x) » : le prof dit « f de x »
    p = re.sub(r"(?<![^\W\d_])([a-zA-Z]|ln|exp|sin|cos|tan|prime)\s?\((?=[^()]{1,25}\))", r"\1 de (", p)                             # deuxracine, وracine -> deux racine
    return re.sub(r"[ \t]{2,}", " ", p)


# ── Nombres, symboles et unités (19 novembre 2026) ─────────────────────────────────────────────────────────────────
# Demande de l'utilisateur : « micros est lu avec s à la fin, écho est lu parfois avec ch ; les unités avec du texte,
# par exemple micro seconde ». Le corpus d'entraînement n'a que des nombres en lettres, aucun symbole (Δ, λ, √, =…),
# aucune unité en symbole (Hz, V, J) et presque aucun mot « micro… » collé (microfarad 0 fois, microcoulomb 0,
# microseconde 5) : on écrit tout comme le prof le dit, avec des mots que le modèle connaît.
_DIZ = {2: "vingt", 3: "trente", 4: "quarante", 5: "cinquante", 6: "soixante"}


def _cent_fr(n):
    """0..99 en français (soixante-dix, quatre-vingts, vingt et un…)."""
    if n < len(FR):
        return FR[n]
    if n < 20:
        return "dix-" + FR[n - 10]
    d, u = divmod(n, 10)
    if d == 7:
        return "soixante" + (" et " if u == 1 else "-") + _cent_fr(10 + u)
    if d == 9:
        return "quatre-vingt-" + _cent_fr(10 + u)
    if d == 8:
        return "quatre-vingts" if u == 0 else "quatre-vingt-" + FR[u]
    return _DIZ[d] + ("" if u == 0 else " et un" if u == 1 else "-" + FR[u])


def nombre_fr(n):
    """Entier 0..999 999 999 en lettres françaises."""
    if n < 100:
        return _cent_fr(n)
    if n < 1000:
        c, r = divmod(n, 100)
        tete = "cent" if c == 1 else FR[c] + (" cents" if r == 0 else " cent")
        return tete + (" " + _cent_fr(r) if r else "")
    if n < 1_000_000:
        m, r = divmod(n, 1000)
        tete = "mille" if m == 1 else re.sub(r"(cent|vingt)s$", r"\1", nombre_fr(m)) + " mille"
        return tete + (" " + nombre_fr(r) if r else "")
    m, r = divmod(n, 1_000_000)
    return nombre_fr(m) + (" million" if m == 1 else " millions") + (" " + nombre_fr(r) if r else "")


def _decimal_fr(mt):
    entier, dec = mt.group(1), mt.group(2)
    reste = dec.lstrip("0")
    zeros = len(dec) - len(reste)
    return nombre_fr(int(entier)) + " virgule" + " zéro" * zeros + (" " + nombre_fr(int(reste)) if reste else "")


# Unité écrite en symbole juste après un nombre -> le mot, au singulier (le « s » ne s'entend pas, et le modèle, qui
# ne l'a presque jamais vu écrit, le prononçait).
UNITES = {
    "Hz": "hertz", "kHz": "kilohertz", "MHz": "méga hertz", "V": "volt", "mV": "millivolt", "kV": "kilo volt",
    "J": "joule", "kJ": "kilojoule", "mJ": "millijoule", "µJ": "micro joule", "μJ": "micro joule",
    "A": "ampère", "mA": "milliampère", "µA": "micro ampère", "μA": "micro ampère",
    "Ω": "ohm", "kΩ": "kilo ohm", "W": "watt", "ms": "milliseconde", "µs": "micro seconde", "μs": "micro seconde",
    "s": "seconde", "min": "minute", "km": "kilomètre", "cm": "centimètre", "mm": "millimètre", "nm": "nanomètre",
    "µm": "micro mètre", "μm": "micro mètre", "m": "mètre", "kg": "kilogramme", "mg": "milligramme",
    "µg": "micro gramme", "μg": "micro gramme", "g": "gramme", "mol": "mole", "mL": "millilitre", "L": "litre",
    "µF": "micro farad", "μF": "micro farad", "nF": "nano farad", "pF": "pico farad", "F": "farad",
    "mH": "millianri", "H": "anri", "°C": "degré Celsius", "%": "pour cent", "eV": "électron volt",
}
_UNITE_RE = re.compile(r"(?<![\w,.])(\d+(?:[,.]\d+)?)\s?("
                       + "|".join(sorted(map(re.escape, UNITES), key=len, reverse=True))
                       + r")(?![\wµμΩ°%])")
SYMBOLES = [
    (re.compile(r"Δ\s?"), "delta "), (re.compile(r"λ"), "lambda"), (re.compile(r"β"), "bêta"),
    (re.compile(r"α"), "alpha"), (re.compile(r"π"), "pi"), (re.compile(r"ω"), "oméga"), (re.compile(r"σ"), "sigma"),
    (re.compile(r"τ"), "tau"), (re.compile(r"θ"), "theta"), (re.compile(r"(?<!\w)[µμ](?!\w)"), "mu"),
    (re.compile(r"(?<=\b[a-z])\s?→\s?|\s?→\s?(?=[+\-−]?\s?∞)"), " tend vers "),    # limites : x → +∞, n → 0
    (re.compile(r"\+\s?∞"), "plus l'infini"), (re.compile(r"[\-−]\s?∞"), "moins l'infini"),
    (re.compile(r"\s?∞"), " l'infini"), (re.compile(r"(?<=\w)\s?√\s?"), " racine de "), (re.compile(r"√\s?"), "racine de "), (re.compile(r"\s?≈\s?"), " environ "),
    (re.compile(r"\s?≤\s?"), " inférieur ou égal à "), (re.compile(r"\s?≥\s?"), " supérieur ou égal à "),
    (re.compile(r"\s<\s"), " inférieur à "), (re.compile(r"\s>\s"), " supérieur à "),
    (re.compile(r"\s?=\s?"), " égale "), (re.compile(r"\s\+\s"), " plus "), (re.compile(r"\s?\^\s?"), " puissance "), (re.compile(r"\s?×\s?"), " fois "), (re.compile(r"\s?→\s?"), " donne "),
    (re.compile(r"\s?[−–]\s?(?=\w)"), " moins "),
    (re.compile(r"(?<=\w)\s?/\s?(?=\w)"), " sur "),
]
# Mot « micro / nano / pico + unité » collé (jamais entendu à l'entraînement) -> deux mots connus, au singulier.
# « nanomètre(s) » est gardé : le corpus le dit 41 fois.
_PREFIXE_UNITE = re.compile(
    r"\b(micro|nano|pico)(farad|coulomb|seconde|joule|gramme|mètre|ampère|volt|watt|litre|mole)s?\b", re.I)


def nombres_symboles_unites(p):
    p = _UNITE_RE.sub(lambda mt: mt.group(1) + " " + UNITES[mt.group(2)], p)
    for motif, dit in SYMBOLES:
        p = motif.sub(dit, p)
    p = _PREFIXE_UNITE.sub(lambda mt: mt.group(0) if mt.group(0).lower().startswith("nanomètre")
                           else mt.group(1) + " " + mt.group(2), p)
    p = re.sub(r"(?<![\w,.])(\d+)[,.](\d+)(?!\w)(?![,.]\d)", _decimal_fr, p)      # 1,15 -> un virgule quinze
    p = re.sub(r"(?<![\w,.])\d{1,9}(?!\w)(?![,.]\d)", lambda mt: nombre_fr(int(mt.group(0))), p)
    return re.sub(r"[ \t]{2,}", " ", p)


# Mots que le modèle n'a jamais entendus (absents des 38 852 transcriptions d'entraînement) et dont l'orthographe le
# trompe : on les écrit comme ils se disent (signalé par l'utilisateur le 15 novembre 2026 : « les hématies, il lit
# t au lieu de si », « cliquer est mal prononcé »). Le texte affiché ne change pas.
PRONONCIATION = [
    (re.compile(r"\bh[ée]maties?\b", re.I), "émassi"),                 # t prononcé s
    (re.compile(r"\bcliqu(?:er|ez|é|ée|és|ées)\b", re.I), "kliké"),     # jamais « cliquer » au corpus
    (re.compile(r"\bcliques?\b", re.I), "klik"),
    (re.compile(r"\bMeV\b"), "méga électron-volts"),
    # 19/11/2026 (signalé par l'utilisateur) : « micros » lu avec le s final ; « écho » lu parfois avec « ch »
    (re.compile(r"\bmicros\b", re.I), "micro"),
    (re.compile(r"\b[ée]chos?\b", re.I), "éko"),
    # 19/11/2026 : « fœtus » (jamais entendu, écrit aussi للفيتوس) sortait « météorite », « le vitre » ;
    # « le fétusse » choisi à l'écoute par l'utilisateur (« الجنين » aussi essayé)
    (re.compile(r"(?<![\u0600-\u06ff])([فبلو]?)(?:ال|ل)فيتوس(?![\u0600-\u06ff])"),
     lambda mt: (mt.group(1) + " " if mt.group(1) else "") + "le fétusse"),
    (re.compile(r"\bf(?:œ|oe)tus\b", re.I), "fétusse"),
    # « siemens » (vu une fois à l'entraînement) sortait « milliseconde » ; « si mènsse » choisi à l'écoute (16/11/2026)
    (re.compile(r"\b(milli|micro)?siemens\b", re.I), lambda mt: (mt.group(1) or "") + "si mènsse"),
    (re.compile(r"\b(milli)?henrys?\b"), lambda mt: (mt.group(1) or "") + "anri"),   # unité (H, mH) ; pas le nom propre
    # 21/11/2026 : « lim » (vu une fois à l'entraînement) ; « la limite » choisi à l'écoute par l'utilisateur
    # (`_ecoute_lim/ecoute_3.mp3` ; « lim » et « limite » seuls écoutés aussi)
    (re.compile(r"\b(?:la\s+)?lim\b"), "la limite"),
    (re.compile(r"\b(BBT|LDL|HDL)\b"), lambda mt: " ".join(mt.group(1))),   # sigles lus lettre par lettre
    (re.compile(r"\b([AUGC]{3})\b"), lambda mt: " ".join(mt.group(1))),     # codons : UAA -> U A A
]


# >>> ÉCRITURES SÛRES (générées par scripts/voix/ecritures_sures.py, ne pas modifier à la main)
ECRITURES_SURES = {
 "achromatique": "akromatique",
 "activités": "activité",
 "affixes": "affixe",
 "amplitudes": "amplitude",
 "ampères": "ampère",
 "angles": "angle",
 "appareils": "appareil",
 "appelées": "appelée",
 "approchées": "approchée",
 "aqueuses": "aqueuse",
 "arcs": "arc",
 "arguments": "argument",
 "associations": "association",
 "asymptotes": "asymptote",
 "atteintes": "atteinte",
 "atteints": "atteint",
 "aérobies": "aérobie",
 "becquerels": "becquerel",
 "bichromatidien": "bikromatidien",
 "bilans": "bilan",
 "bleues": "bleue",
 "bobines": "bobine",
 "bornées": "bornée",
 "béchers": "bécher",
 "capacités": "capacité",
 "carrés": "carré",
 "cartes": "carte",
 "cases": "case",
 "causes": "cause",
 "centrales": "centrale",
 "chaleurs": "chaleur",
 "chlore": "klore",
 "chlorophylle": "klorophylle",
 "chlorophyllienne": "klorophyllienne",
 "chlorophylliens": "klorophylliens",
 "chlorure": "klorure",
 "chocs": "choc",
 "choisis": "choisi",
 "chronomètre": "kronomètre",
 "cinquièmes": "cinquième",
 "circulaires": "circulaire",
 "codons": "codon",
 "coenzymes": "coenzyme",
 "cohérentes": "cohérente",
 "colonnes": "colonne",
 "complets": "complet",
 "complémentaires": "complémentaire",
 "conducteurs": "conducteur",
 "conductivités": "conductivité",
 "conjuguées": "conjuguée",
 "conjugués": "conjugué",
 "contenus": "contenu",
 "contraires": "contraire",
 "contrôles": "contrôle",
 "contrôlées": "contrôlée",
 "conversions": "conversion",
 "correspondantes": "correspondante",
 "cubes": "cube",
 "cycles": "cycle",
 "célérités": "célérité",
 "côtés": "côté",
 "demi-bandes": "demi-bande",
 "demi-vies": "demi-vie",
 "demis": "demi",
 "dentaires": "dentaire",
 "diodes": "diode",
 "dipôles": "dipôle",
 "directs": "direct",
 "dispersifs": "dispersif",
 "donnés": "donné",
 "droites": "droite",
 "durées": "durée",
 "débuts": "début",
 "dénominateurs": "dénominateur",
 "déplacements": "déplacement",
 "dérivables": "dérivable",
 "dérivées": "dérivée",
 "dérivés": "dérivé",
 "ensembles": "ensemble",
 "essentiels": "essentiel",
 "extrémités": "extrémité",
 "fentes": "fente",
 "fermentations": "fermentation",
 "fins": "fin",
 "fissions": "fission",
 "fonctionnels": "fonctionnel",
 "générations": "génération",
 "imaginaires": "imaginaire",
 "impairs": "impair",
 "inconnues": "inconnue",
 "inférieures": "inférieure",
 "interdits": "interdit",
 "inverses": "inverse",
 "ioniques": "ionique",
 "joules": "joule",
 "kelvins": "kelvin",
 "kilomètres": "kilomètre",
 "lactates": "lactate",
 "lames": "lame",
 "largeurs": "largeur",
 "lettres": "lettre",
 "leurs": "leur",
 "libres": "libre",
 "liées": "liée",
 "locus": "locuss",
 "longueurs": "longueur",
 "lourds": "lourd",
 "légères": "légère",
 "majorées": "majorée",
 "milliampères": "milliampère",
 "milligrammes": "milligramme",
 "minorées": "minorée",
 "modules": "module",
 "modulées": "modulée",
 "molaires": "molaire",
 "moles": "mole",
 "monochromatidien": "monokromatidien",
 "monochromatiques": "monochromatique",
 "mutants": "mutant",
 "mutés": "muté",
 "mélanges": "mélange",
 "noms": "nom",
 "nucléofilaments": "nucléofilament",
 "numérateurs": "numérateur",
 "numéros": "numéro",
 "négatifs": "négatif",
 "obstacles": "obstacle",
 "ohmiques": "ohmique",
 "ohms": "ohm",
 "ordres": "ordre",
 "oxydants": "oxydant",
 "oxydatives": "oxydative",
 "paires": "paire",
 "pascals": "pascal",
 "pentes": "pente",
 "pertes": "perte",
 "photos": "photo",
 "places": "place",
 "polymérases": "polymérase",
 "portées": "portée",
 "positions": "position",
 "possibilités": "possibilité",
 "premiers": "premier",
 "proches": "proche",
 "proportionnelles": "proportionnelle",
 "proportionnels": "proportionnel",
 "proposées": "proposée",
 "présentes": "présente",
 "puissances": "puissance",
 "purs": "pur",
 "pères": "père",
 "périodicités": "périodicité",
 "quarts": "quart",
 "quelles": "quelle",
 "quotients": "quotient",
 "radians": "radian",
 "radiations": "radiation",
 "radioactifs": "radioactif",
 "rationnelles": "rationnelle",
 "reliés": "relié",
 "rencontres": "rencontre",
 "représentées": "représentée",
 "repères": "repère",
 "retours": "retour",
 "réalisés": "réalisé",
 "réducteurs": "réducteur",
 "réelles": "réelle",
 "réels": "réel",
 "rôles": "rôle",
 "sauvages": "sauvage",
 "segments": "segment",
 "sessions": "session",
 "seuls": "seul",
 "sixièmes": "sixième",
 "sommes": "somme",
 "sommets": "sommet",
 "sons": "son",
 "spectateurs": "spectateur",
 "sportifs": "sportif",
 "sportives": "sportive",
 "stables": "stable",
 "stimulus": "stimuluss",
 "stoechiométriques": "stoechiométrique",
 "successifs": "successif",
 "successives": "successive",
 "sujets": "sujet",
 "supports": "support",
 "supérieures": "supérieure",
 "surfaces": "surface",
 "synthases": "synthase",
 "systèmes": "système",
 "séries": "série",
 "tangentes": "tangente",
 "technicien": "teknicien",
 "tels": "tel",
 "températures": "température",
 "tendons": "tendon",
 "tends": "tend",
 "théorèmes": "théorème",
 "tissus": "tissu",
 "tours": "tour",
 "traces": "trace",
 "transformés": "transformé",
 "trouves": "trouve",
 "tubes": "tube",
 "unes": "une",
 "utilisées": "utilisée",
 "utilisés": "utilisé",
 "vacuoles": "vacuole",
 "verres": "verre",
 "vraies": "vraie",
 "vérifications": "vérification",
 "zones": "zone",
 "zéros": "zéro",
 "échelles": "échelle",
 "échographie": "ékographie",
 "écrans": "écran",
 "électrodes": "électrode",
 "électroniques": "électronique",
 "émetteurs": "émetteur",
 "êtres": "être"
}
# <<< ÉCRITURES SÛRES


def _sures(p):
    """Mots rares écrits de la manière la plus sûre (scripts/voix/ecritures_sures.py, skill prononciation § 6)."""
    if not ECRITURES_SURES:
        return p
    rx = re.compile(r"(?<![\w-])(" + "|".join(sorted(map(re.escape, ECRITURES_SURES), key=len, reverse=True))
                    + r")(?![\w-])", re.I)
    return rx.sub(lambda mt: ECRITURES_SURES.get(mt.group(1).lower(), mt.group(1)), p)


# « ln » se dit d'un bloc, comme dans l'extrait choisi par l'utilisateur (19/11/2026, ecoute_1_ln) ; collé à un chiffre,
# une lettre ou une parenthèse (« ln2 », « lnx », « ln(x) »), écrit « l n », « Ln » ou « LN », la voix l'épelait « L N ».
# On le ramène toujours à « ln » suivi d'une espace. Même règle pour les fonctions notées en lettres (exp, sin, cos, tan).
_FONCTIONS = [
    (re.compile(r"(?<![^\W\d_])l n(?![^\W\d_]|['’])"), "ln"),
    (re.compile(r"(?<![^\W\d_])(?:Ln|LN)(?![^\W\d_]|['’])"), "ln"),
    (re.compile(r"(?<![^\W\d_])(ln|exp|sin|cos|tan)(?=[(|\d√]|[a-zA-Zα-ωπ](?![^\W\d_]))"), r"\1 "),
]


def prononciation(p):
    for motif, dit in PRONONCIATION:
        p = motif.sub(dit, p)
    for motif, dit in _FONCTIONS:
        p = motif.sub(dit, p)
    return _sures(p)


COUPE = re.compile(r"\s*([:;؛])\s+|\s*([,،])\s+")
# expressions du prof suivies d'une virgule : on s'arrête après, même si le morceau est court
EXPRESSION = re.compile(r"^(?:و|ف)?(?:إذن|اذن|يعني|بمعنى|دابا|أولا|ثانيا|من بعد|ومن بعد|بالتالي|برافو|donc|alors|ensuite|"
                        r"maintenant|bon|bravo|attention|d'abord|c'est-à-dire|autrement dit)\s*[,،]$", re.I)


def segments(p):
    """Phrase -> [(morceau, pause après en s)] ; on ne coupe jamais un morceau de moins de 10 caractères."""
    out, cur, pos, longue = [], "", 0, len(p) > 90
    for mt in COUPE.finditer(p):
        cur = (cur + " " + p[pos:mt.end()].strip()).strip(); pos = mt.end()
        fort = bool(mt.group(1))
        if len(p) - pos >= 15 and EXPRESSION.match(cur):
            out.append((cur, 0.28)); cur = ""
        elif len(cur) >= 10 and len(p) - pos >= 15 and (fort or (longue and len(cur) >= 25)):
            out.append((cur, 0.35 if fort else 0.22)); cur = ""
    cur = (cur + " " + p[pos:].strip()).strip()
    if cur:
        out.append((cur, 0.0))
    return out


if __name__ == "__main__":
    import sys, json, glob
    sys.stdout.reconfigure(encoding="utf-8")
    sys.path.insert(0, r"C:/Users/HP/Desktop/ai-tutor-bac/backend")
    from scripts.generate_course_audio import load_manifest, manifest_slides
    FIN = re.compile(r"(?<=[.!?؟…])\s+")
    n = 0
    for f in sorted(glob.glob(r"C:/Users/HP/Desktop/ai-tutor-bac/backend/data/courses/*_course_v1.json")):
        _, m = load_manifest(json.load(open(f, encoding="utf-8"))["stable_id"])
        for s in manifest_slides(m):
            for ph in FIN.split(((s.get("speech_text") or {}).get(sys.argv[1] if len(sys.argv) > 1 else "mixed") or "").strip()):
                q = parle(ph)
                if q != ph:
                    n += 1; print("-", ph, "\n+", q, "\n")
    print(n, "phrases changées")
