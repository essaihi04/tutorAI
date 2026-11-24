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
    p = nombres_darija_fr(p)                      # 22/11/2026 : nombres et formules sans darija collée au français
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
    p = symboles_elements(p)                       # 21/11/2026 : « Xe » -> « xénon »
    return prononciation(p)


# ── Symboles des éléments (21 novembre 2026) ──────────────────────────────────────────────────────────────────────
# « Xe » était lu lettre par lettre ; l'utilisateur a choisi à l'écoute « le xénon » écrit tel quel (ecoute/xenon/2) et
# demandé qu'un symbole se lise par défaut par le NOM de l'élément. Même table que backend/app/services/speech_normalizer.py
# (_NOMS_ELEMENTS). Un symbole n'est remplacé que SEUL (« m de Xe », « A ديال Xe », « Cu deux plus ») : à côté d'un autre
# symbole ou d'une lettre capitale, c'est une formule (« Fe Cl trois », « C O deux ») et elle reste épelée.
# Jamais : les mots français et la notation maths (La, Ce, Si, Au, Re, Sn = la somme Sₙ, Ne, Se, In, As, Pa, Te…).
NOMS_ELEMENTS = {
    "He": "hélium", "Li": "lithium", "Be": "béryllium", "Na": "sodium", "Mg": "magnésium", "Al": "aluminium",
    "Cl": "chlore", "Ar": "argon", "Ca": "calcium", "Sc": "scandium", "Ti": "titane", "Cr": "chrome",
    "Mn": "manganèse", "Fe": "fer", "Co": "cobalt", "Ni": "nickel", "Cu": "cuivre", "Zn": "zinc", "Ga": "gallium",
    "Ge": "germanium", "Br": "brome", "Kr": "krypton", "Rb": "rubidium", "Sr": "strontium", "Zr": "zirconium",
    "Nb": "niobium", "Mo": "molybdène", "Ag": "argent", "Cd": "cadmium", "Sb": "antimoine", "Xe": "xénon",
    "Cs": "césium", "Ba": "baryum", "Pt": "platine", "Hg": "mercure", "Pb": "plomb", "Bi": "bismuth", "Ra": "radium",
    "Ac": "actinium", "Th": "thorium",
}
_SYMBOLE = re.compile(r"(?<![\w'’-])(" + "|".join(NOMS_ELEMENTS) + r")(?![\w'’-])")
_VOISIN_FORMULE = re.compile(r"^[A-Z][a-z]?$")


def symboles_elements(p):
    def nom(mt):
        avant = p[:mt.start()].split()
        apres = p[mt.end():].split()
        voisins = [avant[-1] if avant else "", apres[0].rstrip(",.:;،") if apres else ""]
        if any(_VOISIN_FORMULE.match(v) for v in voisins):
            return mt.group(1)                     # dans une formule : épelée comme avant
        return NOMS_ELEMENTS[mt.group(1)]
    return _SYMBOLE.sub(nom, p)


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
    # 24/11/2026 (signalé par l'utilisateur) : « أفقي » lu « afaqi » au lieu de « ofoqi » ; « أوفوقي » choisi à l'écoute
    (re.compile(r"(?<![؀-ۿ])((?:[وفبل]?ال|[وفبل])?)[أا]فقي"), lambda mt: mt.group(1) + "أوفوقي"),
    # 24/11/2026 : « برر » mal dit (doit sonner « barrir ») ; « بَرِّر » (v3) choisi à l'écoute malgré le tachkil
    (re.compile(r"(?<![؀-ۿ])([وف]?)برر(?![؀-ۿ])"), lambda mt: mt.group(1) + "بَرِّر"),
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


# ── Nombres et formules : jamais darija et français collés (22 novembre 2026) ──────────────────────────────────────
# Règle de l'utilisateur (21-22/11/2026) : dans un nombre ou une formule, jamais un mot darija et un mot français
# successifs. « جوج noyaux » -> « deux noyaux », « x زائد واحد » -> « x plus un », « dix أس ناقص خمسة » -> « dix
# puissance moins cinq », « تسعمية nanomètre » -> « neuf cents nanomètre ». Un comptage tout en darija (« جوج طرق »)
# reste. Répare aussi les mots cassés (« فالنoyau », « زéro », « Mزيان »). Appliqué EN PREMIER par `parle` : il vaut
# donc pour les cours, les réactions, les lots ET les réponses libres du tuteur (voix en direct). Outil des cours et
# tests : scripts/voix/nombres_fr.py, scripts/voix/test_nombres_fr.py.

_nd_U = {'زيرو': 0, 'صفر': 0, 'واحد': 1, 'وحدة': 1, 'جوج': 2, 'زوج': 2, 'اثنان': 2, 'اثنين': 2, 'جوجة': 2, 'تلاتة': 3, 'ثلاثة': 3, 'تلت': 3, 'ثلاث': 3,
     'ربعة': 4, 'أربعة': 4, 'اربعة': 4, 'ربع': None, 'خمسة': 5, 'خمس': 5, 'ستة': 6, 'ست': 6, 'سبعة': 7, 'سبع': 7,
     'تمنية': 8, 'ثمانية': 8, 'ثمان': 8, 'تمن': 8, 'تسعة': 9, 'تسع': 9, 'عشرة': 10, 'عشر': 10,
     'حداش': 11, 'طناش': 12, 'تلطاش': 13, 'ربعطاش': 14, 'خمسطاش': 15, 'سطاش': 16, 'سبعطاش': 17, 'تمنطاش': 18, 'تسعطاش': 19}
_nd_U = {k: v for k, v in _nd_U.items() if v is not None}
_nd_D = {'عشرين': 20, 'تلاتين': 30, 'ثلاثين': 30, 'ربعين': 40, 'أربعين': 40, 'اربعين': 40, 'خمسين': 50, 'ستين': 60,
     'سبعين': 70, 'تمانين': 80, 'ثمانين': 80, 'تسعين': 90}
_nd_C = {'مية': 100, 'ميا': 100, 'مائة': 100, 'مئة': 100, 'ميتين': 200}
# centaines en un seul mot (« تسعمية nanomètre ») : 22/11/2026
_nd_CENTS = {p + s: v * 100 for p, v in (('تلت', 3), ('ثلاث', 3), ('ربع', 4), ('أربع', 4), ('اربع', 4), ('خمس', 5), ('ست', 6),
                                      ('سبع', 7), ('تمن', 8), ('ثمان', 8), ('تسع', 9)) for s in ('مية', 'ميا', 'مائة', 'مئة')}
_nd_M = {'ألف': 1000, 'الف': 1000, 'آلاف': 1000, 'الاف': 1000, 'ألفين': 2000, 'مليون': 10 ** 6}
_nd_NOMBRE = set(_nd_U) | set(_nd_D) | set(_nd_C) | set(_nd_CENTS) | set(_nd_M)
_nd_LAT = re.compile(r"[A-Za-zÀ-ÿœŒ]")
_nd_ARA = re.compile(r'[؀-ۿ]')
_nd_MATHS = {'virgule', 'fois', 'puissance', 'au', 'sur', 'plus', 'moins', 'égale', 'divisé', 'racine', 'pour', 'cent', 'mille',
         'zéro', 'un', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze', 'treize',
         'quatorze', 'quinze', 'seize', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'cents', 'x', 'n'}
# « واحد virgule », « moins واحد » : le nombre ; « كل واحد zéro… » ou « وحدة: deux » : pas un nombre
_nd_MATHS_APRES = {'virgule', 'fois', 'puissance', 'au', 'sur', 'pour', 'divisé', 'mille', 'cent', 'cents', 'égale', 'plus', 'moins'}
_nd_MATHS_AVANT = {'virgule', 'fois', 'puissance', 'sur', 'plus', 'moins', 'égale', 'divisé', 'racine', 'de', 'à', 'et'}
_nd_SEP = {'فاصلة': 'virgule', 'فاصل': 'virgule', 'في': 'fois', 'أس': 'puissance'}


def _nd_valeur(mots):
    """Valeur d'une suite de mots-nombres (sans « و »), ou None si la suite n'est pas un nombre bien formé."""
    total, courant = 0, 0
    for i, m in enumerate(mots):
        if m in _nd_U:
            v = _nd_U[m]
            if courant % 100 and v < 10 and m not in ('عشر',):
                # « خمسة عشر » : unité puis عشر = 15 ; sinon deux unités de suite : pas un nombre
                return None
            courant += v
        elif m == 'عشر' or m == 'عشرة':
            courant += 10
        elif m in _nd_D:
            courant += _nd_D[m]
        elif m in _nd_C:
            courant = (courant or 1) * 100 if _nd_C[m] == 100 else courant + 200
        elif m in _nd_CENTS:
            if courant:
                return None
            courant = _nd_CENTS[m]
        elif m in _nd_M:
            total += (courant or 1) * _nd_M[m] if _nd_M[m] in (1000, 10 ** 6) and m not in ('ألفين',) else 2000
            courant = 0
        else:
            return None
    return total + courant


def _nd_un_seul_(parties):
    return [m for p in parties for m in p] in (['واحد'], ['وحدة'])


def _nd_fr(v):
    return nombre_fr(v)


_nd_JETON = re.compile(r'\S+|\s+')


#: Opérateurs darija d'une formule (22/11/2026, règle de l'utilisateur : jamais un mot darija et un mot français
#: successifs dans un nombre ou une formule) : traduits quand ils touchent un mot français (ou un nombre déjà traduit).
_nd_OPERATEURS = {'زائد': 'plus', 'ناقص': 'moins', 'سالب': 'moins', 'يساوي': 'égale', 'أس': 'puissance', 'فاصلة': 'virgule',
              'فاصل': 'virgule'}
#: « على » (sur) est aussi une préposition (« Pi على l'ADP ») : traduit seulement entre un mot français et un nombre
#: ou un symbole (« croissante على I », « millimole على une minute ») ; « في » (fois) : voir la fin de `_convertir_nombres`.
_nd_ENTRE_DEUX = {'على': 'sur'}
#: Mots darija juste AVANT un nombre français (22/11/2026 : « تقريبا huit minutes » était dit « thuit », « كيساوي un »
#: dit « واحد ») : traduits quand le mot suivant est un nombre ; « كيساوي » seulement entre un mot français et un nombre (« deux كتساوي un »
#: -> « deux égale un », mais « شحال كتساوي g » reste : « شحال égale » serait un autre mélange).
_nd_AVANT_NOMBRE = {'تقريبا': 'environ', 'تقريباً': 'environ'}
_nd_EGALE = {'كيساوي': 'égale', 'كتساوي': 'égale', 'تيساوي': 'égale', 'تتساوي': 'égale', 'كيساويو': 'égalent',
             'كتساوى': 'égale', 'كيسوى': 'égale'}
_nd_NOMBRES_FR = {'zéro', 'un', 'une', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze',
              'treize', 'quatorze', 'quinze', 'seize', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'cent', 'mille'}
_nd_COMPARAISON = re.compile(r"(و)?(?:أ?كبر|أ?صغر|أقل|أكثر)(?: من)? (?:ولا|أو|او) يساوي(?= [A-Za-zÀ-ÿ])")


_nd_ARTICLES = {'le', 'la', 'l', "l'", 'de', 'du', 'des', 'en', 'et', 'au', 'à', 'un', 'une', 'les'}


def _nd__nombre_ou_symbole(j):
    """« trois », « R », « x » : oui ; « le », « la », « un » (articles) : non."""
    n = _nd__nu(j)[0]
    return _nd__latin(j) and n.lower() not in _nd_ARTICLES and (n.lower() in _nd_NOMBRES_FR or len(n) <= 2)


def _nd__latin(j):
    n = _nd__nu(j)[0]
    return bool(n) and bool(_nd_LAT.search(n)) and not _nd_ARA.search(n)


def _nd__operateurs(texte):
    texte = _nd_COMPARAISON.sub(lambda m: ('و ' if m.group(1) else '')
                            + ('supérieur' if ('كبر' in m.group(0) or 'أكثر' in m.group(0)) else 'inférieur')
                            + ' ou égal à', texte)
    jetons = _nd_JETON.findall(texte)
    mots = [i for i, j in enumerate(jetons) if not j.isspace()]
    for k, i in enumerate(mots):
        nu, p = _nd__nu(jetons[i])
        w = nu[1:] if nu.startswith('و') and nu[1:] in _nd_OPERATEURS else nu
        coupe_av = k == 0 or bool(_nd__nu(jetons[mots[k - 1]])[1])
        av = jetons[mots[k - 1]] if not coupe_av else ''
        ap = jetons[mots[k + 1]] if k + 1 < len(mots) and not p else ''
        if w in _nd_OPERATEURS and (_nd__latin(av) or _nd__latin(ap)):
            jetons[i] = ('و ' if w != nu else '') + _nd_OPERATEURS[w] + p
        elif nu in _nd_AVANT_NOMBRE and ap and _nd__nu(ap)[0].lower().split('-')[0] in _nd_NOMBRES_FR:
            jetons[i] = _nd_AVANT_NOMBRE[nu] + p
        elif nu in _nd_EGALE and ap and _nd__latin(av) and _nd__nu(ap)[0].lower().split('-')[0] in _nd_NOMBRES_FR:
            jetons[i] = _nd_EGALE[nu] + p
        elif nu in _nd_ENTRE_DEUX and _nd__latin(av) and (_nd__nombre_ou_symbole(ap)
                                                  or (_nd__nu(av)[0].lower() in _nd_NOMBRES_FR - _nd_ARTICLES and _nd__latin(ap))):
            jetons[i] = _nd_ENTRE_DEUX[nu] + p
        elif (nu.startswith('و') and nu[1:] in _nd_NOMBRE and nu not in _nd_NOMBRE and nu[1:] not in ('واحد', 'وحدة')
              and (_nd__latin(ap) or _nd__latin(av))):
            # « وجوج récepteurs » : « و » à part, puis le nombre est traduit (« و deux récepteurs »)
            jetons[i] = 'و ' + nu[1:] + p
    # décimales dites chiffre par chiffre après « virgule » : « un virgule خمسة سبعة » -> « un virgule cinq sept »
    k = 0
    while k < len(mots):
        if _nd__nu(jetons[mots[k]])[0] == 'virgule' and not _nd__nu(jetons[mots[k]])[1]:
            t = k + 1
            while t < len(mots):
                nu, p = _nd__nu(jetons[mots[t]])
                if nu in _nd_U and _nd_U[nu] < 10:
                    jetons[mots[t]] = _nd_fr(_nd_U[nu]) + p
                    if p:
                        break
                    t += 1
                else:
                    break
            k = t
        k += 1
    return ''.join(jetons)


#: Mots cassés (22/11/2026) : première lettre d'un mot français écrite en arabe (« فالنoyau », « زéro », « مètre »),
#: ou d'un mot darija écrite en latin (« Mزيان », « fين »). Les verbes français conjugués en darija (« نétablir »,
#: « كيprédomine ») et les articles collés (« فla », « الcourbe ») sont le style du corpus : on n'y touche pas.
_nd_TRANSLIT = {'م': 'm', 'د': 'd', 'ن': 'n', 'ف': 'f', 'ت': 't', 'ر': 'r', 'ه': 'h', 'ب': 'b', 'ز': 'z', 'ل': 'l',
            'س': 's', 'ك': 'c', 'ق': 'q', 'ج': 'j'}
_nd__PRE_AL = re.compile(r"(?<![\wء-ي])([وفبلك]?(?:ال|لل))([مدنفترهبزلسكقج])([a-zàâéèêîôûç][a-zàâäéèêëîïôöùûüç'’-]+)")
_nd_CASSES = {'زéro': 'zéro', 'زero': 'zéro', 'زeroو': 'zéro', 'مètre': 'mètre', 'نul': 'nul', 'دyal': 'ديال',
          'fـ': 'فـ', 'ghير': 'غير', 'tتأكد': 'تتأكد', 'Mزيان': 'مزيان', 'mزيانة': 'مزيانة', 'fين': 'فين',
          'yلا': 'يلا', 'nفسها': 'نفسها', 'dاما': 'ديما', 'dtملي': 'dt ملي'}
_nd__CASSES = re.compile(r"(?<![\wء-ي])(" + "|".join(sorted(map(re.escape, _nd_CASSES), key=len, reverse=True))
                     + r")(?![\wء-ي])")
_nd__NB_COLLE = re.compile(r"(?<![\wء-ي])([وفلب])(" + "|".join(sorted(
    ['zéro', 'un', 'une', 'deux', 'trois', 'quatre', 'cinq', 'six', 'sept', 'huit', 'neuf', 'dix', 'onze', 'douze',
     'treize', 'quatorze', 'quinze', 'seize', 'vingt', 'trente', 'quarante', 'cinquante', 'soixante', 'cent', 'mille',
     'moins', 'plus'], key=len, reverse=True)) + r")(?![A-Za-zÀ-ÿ])")


def _nd_reparer_mots(texte):
    """« فالنoyau » -> « فالnoyau », « Mزيان » -> « مزيان », « وtrois » -> « و trois »."""
    texte = _nd__CASSES.sub(lambda m: _nd_CASSES[m.group(1)], texte)
    texte = _nd__PRE_AL.sub(lambda m: m.group(1) + _nd_TRANSLIT[m.group(2)] + m.group(3), texte)
    return _nd__NB_COLLE.sub(r"\1 \2", texte)


def nombres_darija_fr(texte):
    """Nombres et opérateurs darija qui touchent du français -> français, jusqu'à ce que plus rien ne change
    (« dix أس ناقص خمسة » -> « dix puissance moins خمسة » -> « dix puissance moins cinq »)."""
    texte = _nd_reparer_mots(texte)
    for _ in range(6):
        neuf = _nd__convertir_nombres(_nd__operateurs(texte))
        if neuf == texte:
            return neuf
        texte = neuf
    return texte


def _nd__convertir_nombres(texte):
    jetons = _nd_JETON.findall(texte)
    mots = [(i, j) for i, j in enumerate(jetons) if not j.isspace()]
    out = list(jetons)
    k = 0
    while k < len(mots):
        i, j = mots[k]
        nu, ponct = _nd__nu(j)
        prefixe_b = False
        if nu.startswith('ب') and nu[1:] in ('جوج', 'زوج'):
            prefixe_b = True
        if not (nu in _nd_NOMBRE or prefixe_b or nu in ('فاصلة', 'فاصل')):
            k += 1
            continue
        # étendre la suite : nombres, « و » collé (« وستين »), « فاصلة »
        fin = k
        parties = []  # liste de (mots_du_nombre) séparés par فاصلة
        cour = []
        seps = []
        t = k
        while t < len(mots):
            w, p = _nd__nu(mots[t][1])
            ww = w[1:] if (w.startswith('و') and w[1:] in _nd_NOMBRE and w not in _nd_NOMBRE) else w
            if t == k and prefixe_b:
                cour.append(w[1:]); fin = t
                if p: break
                t += 1; continue
            if ww in _nd_NOMBRE:
                cour.append(ww); fin = t
            elif w == 'و' and cour and t + 1 < len(mots) and _nd__nu(mots[t + 1][1])[0] in _nd_NOMBRE:
                pass
            elif w in _nd_SEP and cour and t + 1 < len(mots) and _nd__nu(mots[t + 1][1])[0] in _nd_NOMBRE:
                parties.append(cour); seps.append(_nd_SEP[w]); cour = []; fin = t
            else:
                break
            if p:
                break
            t += 1
        if cour:
            parties.append(cour)
        if not parties or not all(parties):
            k = fin + 1
            continue
        vals = [_nd_valeur(p) for p in parties]
        if any(v is None for v in vals):
            k = fin + 1
            continue
        seq = [m for p in parties for m in p]
        _, pfin = _nd__nu(mots[fin][1])
        # contexte (une ponctuation coupe le contexte : « فجهة وحدة: deux » n'est pas un nombre de deux)
        apres = mots[fin + 1][1] if fin + 1 < len(mots) and not pfin else ''
        apres2 = mots[fin + 2][1] if fin + 2 < len(mots) and not pfin else ''
        avant = mots[k - 1][1] if k > 0 else ''
        if _nd__nu(avant)[1]:
            avant = ''
        an_, ap_ = _nd__nu(avant)[0].lower(), _nd__nu(apres)[0].lower()
        dial = ap_ == 'ديال'
        cible = apres2 if dial else apres
        cn = _nd__nu(cible or '')[0]
        lat_apres = bool(_nd_LAT.match(cn)) and not _nd_ARA.search(cn)
        arabe_apres = bool(_nd_ARA.search(cn)) or (dial and not lat_apres)
        lat_avant = bool(_nd_LAT.search(an_)) and not _nd_ARA.search(an_) and not arabe_apres
        maths = ap_ in _nd_MATHS_APRES or an_ in _nd_MATHS_AVANT or (ap_ == 'مرات' and not _nd_un_seul_(parties))
        un_seul = seq in (['واحد'], ['وحدة'])
        # « جوج بجوج » : deux par deux
        if seq in (['جوج'], ['زوج']) and not prefixe_b and _nd__nu(apres)[0] in ('بجوج', 'بزوج'):
            i0, i1 = mots[k][0], mots[fin + 1][0]
            for x in range(i0, i1 + 1): out[x] = ''
            out[i0] = 'deux par deux' + _nd__nu(apres)[1]
            k = fin + 2
            continue
        if un_seul and not (maths or len(parties) > 1):
            k = fin + 1
            continue
        if not (lat_apres or lat_avant or maths or len(parties) > 1):
            k = fin + 1
            continue
        morceaux = [_nd_fr(vals[0])]
        for sep_, p_, v_ in zip(seps, parties[1:], vals[1:]):
            zeros = 0
            if sep_ == 'virgule':
                for m_ in p_:
                    if m_ in ('زيرو', 'صفر'): zeros += 1
                    else: break
            morceaux.append(sep_ + ' ' + ' '.join(['zéro'] * zeros + ([_nd_fr(v_)] if len(p_) > zeros else [])))
        texte_fr = ' '.join(morceaux)
        if prefixe_b:
            texte_fr = 'les ' + texte_fr
        # « جوج les voies » : « les deux voies » ; « جوج مرات » : « deux fois »
        if not dial and not pfin and ap_ in ('les', 'des') and not prefixe_b:
            texte_fr = 'les ' + texte_fr
            j_ = mots[fin + 1][0]; out[j_] = ''; out[j_ - 1] = ''
        elif not dial and not pfin and ap_ == 'مرات':
            j_ = mots[fin + 1][0]; out[j_] = 'fois' + _nd__nu(mots[fin + 1][1])[1]
        # remplacer les jetons k..fin
        i0, i1 = mots[k][0], mots[fin][0]
        for x in range(i0, i1 + 1):
            out[x] = ''
        # « ديال les X » / « ديال des X » / « ديال l'X » après le nombre : « deux X »
        if dial and not pfin:
            jd = mots[fin + 1][0]
            art = mots[fin + 2] if fin + 2 < len(mots) else None
            if art and _nd__nu(art[1])[0].lower() in ('les', 'des') and fin + 3 < len(mots):
                out[jd] = ''; out[jd - 1] = ''
                out[art[0]] = ''; out[art[0] - 1] = ''
            elif art and _nd_LAT.match(art[1]):
                out[jd] = ''; out[jd - 1] = ''
        out[i0] = texte_fr + pfin
        k = fin + 1
    r = re.sub(r'[ ]{2,}', ' ', ''.join(out))
    # « dix أس moins trois » : l'exposant dit en français entre deux mots français
    r = re.sub(r"(?<=[A-Za-zÀ-ÿ]) أس (?=[A-Za-zÀ-ÿ])", ' puissance ', r)
    # « six virgule cinq في dix » : « في » entre deux nombres français = fois
    nb = r"(?:zéro|un|deux|trois|quatre|cinq|six|sept|huit|neuf|dix|onze|douze|treize|quatorze|quinze|seize|vingt|trente|quarante|cinquante|soixante|cent|cents|mille)"
    r = re.sub(r"(\b" + nb + r") في (?=" + nb + r"\b)", r"\1 fois ", r)
    return r


_nd_PONCT = '،,.:;!?)»؟'


def _nd__nu(j):
    p = ''
    while j and j[-1] in _nd_PONCT:
        p = j[-1] + p; j = j[:-1]
    return j, p
