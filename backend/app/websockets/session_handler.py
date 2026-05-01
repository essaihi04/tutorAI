"""
WebSocket Session Handler
Orchestrates the real-time voice pipeline: STT -> LLM -> TTS
"""
import json
import re
import base64
import asyncio
import sys
from typing import Optional
from fastapi import WebSocket, WebSocketDisconnect
from app.services.llm_service import llm_service
from app.services.resource_decision_service import resource_decision_service
from app.services.stt_service import stt_service
from app.services.tts_service import tts_service
from app.services.prompt_builder import prompt_builder
from app.services.exercise_evaluator import exercise_evaluator
from app.services.session_progress_service import session_progress_service
from app.websockets.connection_manager import manager
from app.supabase_client import get_supabase


def _safe_log(*parts):
    """Log safely on Windows consoles that may not support UTF-8."""
    message = " ".join(str(part) for part in parts)
    try:
        print(message)
    except UnicodeEncodeError:
        safe_message = message.encode(sys.stdout.encoding or 'utf-8', errors='replace').decode(sys.stdout.encoding or 'utf-8', errors='replace')
        print(safe_message)


# ─────────────────────────────────────────────────────────────────────
# Shared JSON repair helpers (used by both <board> and <ui> parsers)
# ─────────────────────────────────────────────────────────────────────
_VALID_JSON_ESC_RE = re.compile(r'\\(["\\/bfnrt]|u[0-9a-fA-F]{4})')


def _strip_md_fence(s: str) -> str:
    """Remove ```json ... ``` fences the LLM sometimes wraps around JSON."""
    t = s.strip()
    if t.startswith("```"):
        t = re.sub(r"^```[a-zA-Z]*\s*\n?", "", t, count=1)
        if t.endswith("```"):
            t = t[:-3]
    return t.strip()


def _normalize_smart_quotes(s: str) -> str:
    """Replace curly quotes that may have leaked into JSON keys/values."""
    return (s
            .replace("\u201c", '"').replace("\u201d", '"')
            .replace("\u2018", "'").replace("\u2019", "'"))


def _remove_trailing_commas(s: str) -> str:
    """Strip `,` right before a closing `}` or `]`."""
    return re.sub(r",(\s*[}\]])", r"\1", s)


def _escape_bare_backslashes(s: str) -> str:
    r"""
    LLMs often output LaTeX like ``\\vec{AB}`` as ``\vec{AB}`` in JSON,
    which is invalid (``\v`` is not a JSON escape). Double any backslash
    that is NOT already part of a valid JSON escape.

    🚨 Important: in board / UI contexts, LLMs also emit LaTeX commands
    whose first letter collides with JSON single-char escapes —
    ``\text``, ``\times``, ``\to`` (\t → TAB), ``\neq``, ``\nabla``
    (\n → newline), ``\frac``, ``\forall`` (\f → formfeed), ``\binom``,
    ``\boxed`` (\b → backspace), ``\rangle`` (\r → carriage return).
    Treating those as valid JSON escapes silently corrupts every
    formula on the whiteboard (``\text{Phénotypes}`` renders as
    ``⇥ext{Phénotypes}``).  Heuristic: when ``\X`` is followed by a
    letter, assume it is a LaTeX command and double the backslash.
    """
    out = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch == "\\" and i + 1 < n:
            nxt = s[i + 1]
            # Unicode escape \uXXXX — always treat as JSON escape.
            if nxt == 'u' and _VALID_JSON_ESC_RE.match(s, i):
                out.append(s[i:i + 6])
                i += 6
                continue
            # Unambiguous JSON escapes (quote / backslash / solidus).
            if nxt in '"\\/':
                out.append(s[i:i + 2])
                i += 2
                continue
            # Ambiguous single-char escapes also used as LaTeX command
            # starts: \t, \n, \r, \f, \b.  If the following character
            # is a letter, this is almost certainly a LaTeX command
            # like \text, \nabla, \frac, \boxed — double the backslash
            # to survive JSON parsing as a literal ``\X…`` sequence.
            if nxt in 'tbfnr':
                after = s[i + 2] if i + 2 < n else ''
                if after.isalpha():
                    out.append("\\\\")
                    i += 1
                    continue
                out.append(s[i:i + 2])
                i += 2
                continue
            out.append("\\\\")
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


# ─────────────────────────────────────────────────────────────────────
# Anti-padding loop sanitizer
# ─────────────────────────────────────────────────────────────────────
# Some LLM turns enter a degenerate generation loop where they emit
# hundreds of ``\;`` (LaTeX thin spaces) in a single cell to align
# gametes visually.  This eats the entire ``max_tokens`` budget and the
# closing ``</ui>`` is never reached → JSON unparseable → board never
# displayed.  We collapse any run of ≥4 LaTeX padding tokens to 2.
# Applied BOTH to the raw JSON text (before parsing, in case the run
# happens inside a string value) AND to the parsed cell strings.
_RAW_LATEX_SPACE_RUN = re.compile(r"(?:\\\\;){4,}")
_RAW_LATEX_THIN_RUN = re.compile(r"(?:\\\\,){10,}")
_RAW_LATEX_QUAD_RUN = re.compile(r"(?:\\\\quad){4,}")
_PARSED_LATEX_SPACE_RUN = re.compile(r"(?:\\;){4,}")
_PARSED_LATEX_THIN_RUN = re.compile(r"(?:\\,){10,}")
_PARSED_LATEX_QUAD_RUN = re.compile(r"(?:\\quad){4,}")


def _collapse_latex_padding_raw(s: str) -> str:
    """Compress runs of ``\\;`` / ``\\,`` / ``\\quad`` inside the raw
    JSON text (each backslash is doubled because we're pre-parse).

    Example: ``\\;\\;\\;\\;\\;\\;`` (12 raw chars → 6 LaTeX spaces)
    collapses to ``\\;\\;`` (4 raw chars → 2 LaTeX spaces).
    """
    if not s:
        return s
    s = _RAW_LATEX_SPACE_RUN.sub(r"\\\\;\\\\;", s)
    s = _RAW_LATEX_THIN_RUN.sub(r"\\\\,\\\\,", s)
    s = _RAW_LATEX_QUAD_RUN.sub(r"\\\\quad\\\\quad", s)
    return s


def _collapse_latex_padding_parsed(s: str) -> str:
    """Same collapse, but on already-parsed strings (single backslash).

    Used as defense-in-depth inside ``_sanitize_genetics_cells``.
    Note: replacement strings double every backslash because ``re.sub``
    interprets ``\\X`` in replacements (``\\q`` would raise bad-escape).
    """
    if not s:
        return s
    s = _PARSED_LATEX_SPACE_RUN.sub(r"\\;\\;", s)
    s = _PARSED_LATEX_THIN_RUN.sub(r"\\,\\,", s)
    s = _PARSED_LATEX_QUAD_RUN.sub(r"\\quad\\quad", s)
    return s


def _json_cleanup_variants(s: str):
    """Yield successive cleaned variants of the input to try parsing."""
    base = _strip_md_fence(s)
    base = _collapse_latex_padding_raw(base)
    yield base
    cleaned = _remove_trailing_commas(_normalize_smart_quotes(base))
    yield cleaned
    yield _escape_bare_backslashes(cleaned)


# ─────────────────────────────────────────────────────────────────────
# Genetics ASCII → LaTeX sanitizer
# ─────────────────────────────────────────────────────────────────────
# Defense in depth: even with the strictest prompt, some LLM turns
# still emit Moroccan BAC SVT genetics notation in ASCII form like
# ``DO//dø``, ``dø//dø``, ``DO/`` instead of the required ``\dfrac``
# LaTeX blocks.  This leaves the whiteboard rendering unreadable
# (fractions collapsed onto a single line).  We rewrite every cell /
# content string in board payloads before sending them to the frontend.
#
# Supported patterns (most specific first):
#   •  Dihybride zygote  ``XY//xy``   → ``$\dfrac{X}{x}\,\dfrac{Y}{y}$``
#   •  Monohybride       ``X//x``     → ``$\dfrac{X}{x}$``
#   •  Dihybride gamète  ``XY/`` / ``XY //`` → ``$\dfrac{X}{}\,\dfrac{Y}{}$``
#   •  Monohybride gamète ``X/``      → ``$\dfrac{X}{}$``
# Allele alphabet includes accented Moroccan notations: ``ø``, ``ù``,
# ``é``, plus ``+``/``-`` for wild-type markers.
# Existing ``$...$`` blocks are preserved untouched so we don't
# double-wrap cells the LLM already rendered correctly.
_ALLELE = r"[A-Za-zøùéÉØ+\-]"
# Match dihybride zygote XY//xy (letters × 2 // letters × 2).
_RE_DIHYB_ZYGOTE = re.compile(
    rf"(?<![A-Za-z${{\\]){_ALLELE}{_ALLELE}\s*//\s*{_ALLELE}{_ALLELE}(?![A-Za-z}}])"
)
# Match monohybride zygote X//x (letters × 1 // letters × 1).
_RE_MONOHYB_ZYGOTE = re.compile(
    rf"(?<![A-Za-z${{\\]){_ALLELE}\s*//\s*{_ALLELE}(?![A-Za-z}}])"
)
# Match dihybride gamete XY/ (letters × 2 /) — one slash only, no second letter.
_RE_DIHYB_GAMETE = re.compile(
    rf"(?<![A-Za-z${{\\/]){_ALLELE}{_ALLELE}\s*/(?!/)(?![A-Za-z}}])"
)
# Match monohybride gamete X/ (letters × 1 /) — last resort, narrow context.
_RE_MONOHYB_GAMETE = re.compile(
    rf"(?<![A-Za-z${{\\/]){_ALLELE}\s*/(?!/)(?![A-Za-z}}])"
)


def _to_latex_dihyb_zygote(m: re.Match) -> str:
    s = m.group(0)
    top, bot = s.split("//")
    top = top.strip()
    bot = bot.strip()
    return rf"$\dfrac{{{top[0]}}}{{{bot[0]}}}\,\dfrac{{{top[1]}}}{{{bot[1]}}}$"


def _to_latex_monohyb_zygote(m: re.Match) -> str:
    s = m.group(0)
    top, bot = s.split("//")
    top = top.strip()
    bot = bot.strip()
    return rf"$\dfrac{{{top}}}{{{bot}}}$"


def _to_latex_dihyb_gamete(m: re.Match) -> str:
    s = m.group(0).rstrip("/").strip()
    return rf"$\dfrac{{{s[0]}}}{{}}\,\dfrac{{{s[1]}}}{{}}$"


def _to_latex_monohyb_gamete(m: re.Match) -> str:
    s = m.group(0).rstrip("/").strip()
    return rf"$\dfrac{{{s}}}{{}}$"


def _rewrite_ascii_genetics(text: str) -> str:
    """Rewrite ASCII genetics notation (DO//dø, dø/) to LaTeX \\dfrac blocks.

    Applied cell-by-cell to board contents before they hit the frontend.
    Protects existing ``$...$`` segments so we don't re-wrap them.
    """
    if not text or not isinstance(text, str):
        return text or ""
    if "//" not in text and "/" not in text:
        return text

    # Split on existing $...$ / $$...$$ so we don't rewrite inside LaTeX.
    segments = re.split(r"(\$\$[^$]+\$\$|\$[^$]+\$)", text)
    out = []
    for seg in segments:
        if seg.startswith("$"):
            out.append(seg)
            continue
        # Order matters: dihybride zygote first (2+2 letters),
        # then monohybride zygote, then dihybride gamete, then monohybride gamete.
        seg = _RE_DIHYB_ZYGOTE.sub(_to_latex_dihyb_zygote, seg)
        seg = _RE_MONOHYB_ZYGOTE.sub(_to_latex_monohyb_zygote, seg)
        seg = _RE_DIHYB_GAMETE.sub(_to_latex_dihyb_gamete, seg)
        # Monohybride gamete is dangerous (would match any ``X/`` in French
        # prose like ``et/ou``).  Only apply when the line already contains
        # a genetics marker — zygote or phénotype bracket.
        if "\\dfrac" in seg or re.search(r"\[[A-Za-zøùéÉØ,+\- ]+\]", seg):
            seg = _RE_MONOHYB_GAMETE.sub(_to_latex_monohyb_gamete, seg)
        out.append(seg)
    return "".join(out)


# ─────────────────────────────────────────────────────────────────────
# Diploid genotype promoter — single-bar → double-bar
# ─────────────────────────────────────────────────────────────────────
# BAC SVT convention: a genotype represents a PAIR of homologous
# chromosomes (diploid) and must be drawn with TWO horizontal bars
# between the alleles, not one. The LaTeX trick is to wrap the
# denominator in \overline{...}: the fraction bar + the overline render
# as two parallel lines.
#
#   `\dfrac{L}{L}`            (one bar — haploid, WRONG for genotype)
#   `\dfrac{L}{\overline{L}}` (two bars — diploid, BAC-compliant)
#
# Gametes use `\dfrac{X}{}` (empty denominator) and stay haploid → we
# skip them. We also skip cells whose denominator already contains an
# `\overline`, `\underline`, or any nested brace so we never double-wrap.
# Allele content allowed inside the denominator: letters, digits, `+`,
# `-`, `'`, accented chars, optional `\;` separators (linked dihybride
# `\dfrac{J\;L}{J\;L}` → `\dfrac{J\;L}{\overline{J\;L}}`).
_DENOM_ALLELE_CONTENT = r"[A-Za-zøùéÉØ0-9+\-'\s;\\]+"
_RE_DFRAC_GENOTYPE = re.compile(
    r"\\dfrac\{([^{}]+)\}\{(" + _DENOM_ALLELE_CONTENT + r")\}"
)


def _promote_diploid_genotype(text: str) -> str:
    """Rewrite single-bar `\\dfrac{A}{a}` → double-bar `\\dfrac{A}{\\overline{a}}`.

    Skips:
      • gametes (empty denominator `\\dfrac{A}{}`),
      • already-promoted cells (denominator contains `\\overline` /
        `\\underline` — caught by `[^{}]+` rejecting nested braces).
    """
    if not text or not isinstance(text, str) or "\\dfrac" not in text:
        return text or ""

    def _repl(m: re.Match) -> str:
        num = m.group(1)
        denom = m.group(2).strip()
        if not denom:                          # gamete → keep haploid
            return m.group(0)
        if "\\overline" in denom or "\\underline" in denom:
            return m.group(0)
        # Only promote if denominator looks like a plain allele token
        # (letters / digits / +/- / `\;` separators). If it contains
        # any other LaTeX command we leave it alone (safety).
        if re.fullmatch(r"[A-Za-zøùéÉØ0-9+\-'\s]+(?:\\;[A-Za-zøùéÉØ0-9+\-'\s]+)*", denom) is None:
            return m.group(0)
        return r"\dfrac{" + num + r"}{\overline{" + denom + r"}}"

    return _RE_DFRAC_GENOTYPE.sub(_repl, text)


def _clean_cell(s):
    """Normalize a single cell: ASCII genetics → LaTeX, collapse padding,
    promote single-bar genotypes to double-bar (diploid)."""
    if not isinstance(s, str):
        return s
    s = _rewrite_ascii_genetics(s)
    s = _collapse_latex_padding_parsed(s)
    s = _promote_diploid_genotype(s)
    return s


def _sanitize_genetics_cells(lines):
    """In-place rewrite ASCII genetics notation + collapse LaTeX padding
    inside a board ``lines`` list.

    Covers text content, table headers / rows, and step / box labels.
    """
    if not isinstance(lines, list):
        return lines
    for line in lines:
        if not isinstance(line, dict):
            continue
        if isinstance(line.get("content"), str):
            line["content"] = _clean_cell(line["content"])
        if isinstance(line.get("explanation"), str):
            line["explanation"] = _clean_cell(line["explanation"])
        headers = line.get("headers")
        if isinstance(headers, list):
            line["headers"] = [_clean_cell(h) for h in headers]
        rows = line.get("rows")
        if isinstance(rows, list):
            new_rows = []
            for row in rows:
                if isinstance(row, list):
                    new_rows.append([_clean_cell(c) for c in row])
                else:
                    new_rows.append(row)
            line["rows"] = new_rows
    return lines


class SessionHandler:
    """Handles a single tutoring session's voice pipeline."""

    def __init__(self, websocket: WebSocket, student_id: str):
        self.websocket = websocket
        self.student_id = student_id
        self.conversation_history: list[dict] = []
        self.session_context: dict = {}
        self.current_phase: str = "activation"
        self.session_mode: str = "coaching"  # 'coaching' or 'libre'
        self.language: str = "fr"
        self.lesson_resources: list[dict] = []  # Cached lesson resources
        self.current_lesson_id: str = None
        self.simulation_state: dict = {}  # Track current simulation state
        self.simulation_history: list[dict] = []  # Track all simulation actions
        self.recent_resource_modes: list[str] = []
        self.simulation_orchestration: dict = {}
        # Currently-open exam panel view (kept in sync by frontend).
        # Used to inject accurate exam metadata into the LLM system prompt
        # so the model never hallucinates the wrong year/session/exercise/question.
        self.current_exam_view: dict | None = None

    def _sanitize_history_content(self, content: str) -> str:
        """Remove heavy command payloads before re-sending history to the LLM."""
        if not content:
            return ""

        cleaned = content
        # CRITICAL: Strip ALL UI command blocks completely — leave NO replacement
        # text at all. The LLM mimics ANY text it sees in its history (whether
        # [ui], (contenu affiché), or anything else). Removing them silently is
        # the only safe approach.
        cleaned = re.sub(r'<ui>[\s\S]*?</ui>', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<ui>[\s\S]*', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<board>[\s\S]*?</board>', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<board>[\s\S]*', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<draw>[\s\S]*?</draw>', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<draw>[\s\S]*', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<schema>[\s\S]*?</schema>', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<schema>[\s\S]*', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<exam_exercise>[\s\S]*?</exam_exercise>', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<exam_exercise>[\s\S]*', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<suggestions>[\s\S]*?</suggestions>', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'<suggestions>[\s\S]*', '', cleaned, flags=re.DOTALL)
        cleaned = re.sub(r'DESSINER_SCHEMA:.*?(\n|$)', '', cleaned)
        cleaned = re.sub(r'\[CMD:[^\]]+\]', '', cleaned)
        # Also remove any leftover placeholder-like patterns the AI might have generated
        cleaned = re.sub(r'\(contenu affiché[^)]*\)', '', cleaned)
        cleaned = re.sub(r'\(dessin affiché[^)]*\)', '', cleaned)
        cleaned = re.sub(r'\(schéma affiché[^)]*\)', '', cleaned)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()

        # Keep context compact to avoid progressively overloading the LLM.
        if len(cleaned) > 1200:
            cleaned = cleaned[:1200].rsplit(' ', 1)[0].strip() + ' …'

        return cleaned

    def _append_history(self, role: str, content: str):
        """Append compact conversation history and keep only recent turns."""
        sanitized = self._sanitize_history_content(content)
        self.conversation_history.append({"role": role, "content": sanitized})

        # Keep only last 10 exchanges (20 messages)
        if len(self.conversation_history) > 20:
            self.conversation_history = self.conversation_history[-20:]

    def _speech_language(self) -> str:
        """Language code for STT & TTS. Darija is Arabic-based."""
        if self.language == "mixed":
            return "ar"
        return self.language

    def _prompt_language(self) -> str:
        if self.language == "mixed":
            return (
                "darija marocaine ÉCRITE EN ALPHABET ARABE (pas de lettres latines, "
                "pas d'Arabizi type '3la' ou 'ghadi'). "
                "Tu DOIS répondre en darija marocaine naturelle, écrite uniquement en caractères arabes "
                "(أ ب ت ث ج ح خ د ذ ر ز س ش ص ض ط ظ ع غ ف ق ك ل م ن ه و ي ء آ ة), "
                "SAUF pour les termes techniques/scientifiques qui RESTENT EN FRANÇAIS écrits en lettres latines "
                "(ex : la vitesse, l'accélération, la force, l'énergie cinétique, la dérivée, la fonction, "
                "le vecteur, la molécule, la mitose, le pH, l'équation). "
                "N'utilise JAMAIS la traduction arabe classique de ces termes (السرعة، التسارع، القوة…). "
                "Exemples corrects :\n"
                "  « واخا! دابا غادي نشوفو la vitesse initiale. واش عرفتي شنو هي la force؟ »\n"
                "  « مزيان خويا، la dérivée ديال هاد la fonction كتساوي 2x. »\n"
                "  « صافي، خلينا نحسبو l'énergie cinétique ديال هاد l'objet. »"
            )
        return "français" if self.language == "fr" else "arabe"

    def _detect_subject_from_text(self, text: str) -> Optional[str]:
        """Detect subject from a text string using **scored** keyword matching.

        Instead of a waterfall (first-match wins), we count how many keywords
        from each subject appear in the text. Multi-word phrases are weighted
        by their word count so that specific compound terms like
        "matière organique" (SVT, 2 words → +2) beat the single word
        "organique" (Chimie, 1 word → +1). The subject with the highest
        cumulative score wins; ties are broken by list order (rare).
        """
        if not text:
            return None
        t = text.lower()

        math_kw = [
            "math", "maths", "mathématique", "mathématiques", "limite", "limites",
            "continuité", "continuite", "dérivation", "derivation", "dérivée", "derivee",
            "dérivées", "derivees", "fonction", "fonctions", "suite", "suites",
            "numérique", "numériques", "série", "séries", "primitive", "primitives",
            "intégrale", "intégrales", "integrale", "integrales", "logarithme", "logarithmes",
            "logarithmique", "exponentielle", "exponentielles", "exponentiel", "probabilité",
            "probabilités", "probabilite", "probabilites", "complexe", "complexes",
            "nombre complexe", "nombres complexes", "équation différentielle",
            "équations différentielles", "equation differentielle", "equations differentielles",
            "géométrie", "geometrie", "dénombrement", "denombrement", "combinatoire",
            "trigonométrie", "trigonometrie", "polynôme", "polynome",
        ]
        phys_kw = [
            "physique", "phys", "mécanique", "mecanique", "onde", "ondes", "newton", "rc", "rlc",
            "électricité", "electricite", "dipôle", "dipole", "condensateur", "inductance",
            "bobine", "résistance", "resistance", "circuit", "oscillateur", "pendule",
            "vitesse", "accélération", "acceleration", "force", "énergie cinétique",
            "energie cinetique", "travail", "puissance", "thermodynamique", "chaleur",
            "température", "électrique", "electrique", "électromagnétique",
            "electromagnetique", "magnétique", "magnetique", "champ", "lorentz",
            "ampère", "ampere", "faraday", "lenz", "induction", "optique",
            "interférence", "diffraction", "lentille", "miroir", "quantique", "photons",
            "photoélectrique", "radioactivité", "radioactivite", "noyau atomique",
            "fission", "fusion nucléaire", "fusion nucleaire",
        ]
        chem_kw = [
            "chimie", "chim", "acide", "base", "ph", "titrage", "réaction", "reaction",
            "cinétique chimique", "cinetique chimique", "esterification", "molécule",
            "moleculaire", "atome", "atomique", "liaison", "covalente", "ionique",
            "métallique", "orbitale", "électron", "electron", "proton", "neutron",
            "concentration", "molarité", "solution", "oxydoréduction", "oxydo", "redox",
            "potentiel", "pile", "électrolyse", "electrolyse", "électrode", "electrode",
            "anode", "cathode", "catalyse", "catalyseur", "ordre", "équilibre chimique",
            "equilibre chimique", "avancement", "ester", "saponification", "alcool",
            "aldéhyde", "aldehyde", "cétone", "cetone", "acide carboxylique", "amine",
            "amide", "chimie organique", "isomérie", "isomerie", "stéréochimie",
            "stereochimie", "chiralité", "chiralite",
        ]
        svt_kw = [
            "svt", "biologie", "vie", "terre", "géologie", "geologie",
            # ── Compound disambiguation phrases (high weight) ──
            "matière organique", "matiere organique", "matières organiques",
            "matieres organiques", "consommation de la matière",
            "consommation de la matiere", "consommation de matière",
            "consommation de matiere", "utilisation de la matière",
            "utilisation de matiere", "respiration cellulaire",
            "bilan énergétique", "bilan energetique",
            "chaîne respiratoire", "chaine respiratoire",
            "cycle de krebs", "noyau cellulaire",
            # ── Écologie / environnement (programme SVT 2BAC) ──
            "écosystème", "ecosysteme",
            "déchet", "déchets", "dechet", "dechets", "pollution", "polluant", "polluants",
            "polluante", "polluantes", "environnement", "environnemental", "environnementale",
            "écologie", "ecologie", "écologique", "ecologique",
            "biodégradable", "biodegradable", "recyclage", "recycler",
            "atmosphère", "atmosphere", "climat", "climatique",
            "réchauffement", "rechauffement", "effet de serre", "ozone",
            "ressource naturelle", "ressources naturelles",
            "gestion des déchets", "gestion des dechets", "gestion des ressources",
            "développement durable", "developpement durable",
            "eau usée", "eau usées", "eau usee", "eau usees",
            "lixiviat", "compost", "compostage", "incinération", "incineration",
            "tri sélectif", "tri selectif", "valorisation",
            # ── Biologie cellulaire / métabolisme ──
            "cellule", "cellulaire", "membrane", "cytoplasme",
            "mitochondrie", "chloroplaste", "ribosome", "adn", "arn", "nucléotide",
            "nucleotide", "génétique", "genetique", "chromosome", "gène", "gene",
            "allèle", "allele", "mutation", "réplication", "replication", "transcription",
            "traduction", "protéine", "proteine", "enzyme", "métabolisme", "metabolisme",
            "glycolyse", "respiration", "fermentation", "krebs",
            "respiratoire", "atp", "mitose", "méiose",
            "meiose", "interphase", "prophase", "métaphase",
            "metaphase", "anaphase", "télophase", "telophase", "cytocinèse", "cytocinese",
            "photosynthèse", "photosynthese", "autotrophe", "hétérotrophe", "heterotrophe",
            # ── Immunologie ──
            "plasmide", "clonage", "bacterie", "bactérie", "virus", "vaccin", "immunité",
            "immunite", "anticorps", "antigène", "antigene", "lymphocyte", "macrophage",
            "phagocytose", "inflammation", "immunitaire",
            # ── Écologie / chaînes alimentaires ──
            "population", "communauté", "communaute", "habitat", "niche", "trophique",
            "alimentaire", "producteur", "consommateur", "décomposeur",
            "decomposeur", "biomasse", "pyramide",
            "biogéochimique", "biogeochimique", "succession",
            "biodiversité", "biodiversite", "endémisme",
            "endemisme", "évolution", "evolution", "darwin", "sélection naturelle",
            "selection naturelle", "spéciation", "speciation", "adaptation",
            # ── Géologie ──
            "tectonique", "plaque", "subduction", "dorsale", "faille",
            "séisme", "seisme", "volcan", "magma", "lave", "roche",
            "sédimentaire", "sedimentaire", "métamorphique", "metamorphique",
            "magmatique", "fossile", "datation", "stratigraphie",
        ]

        # ── Score each subject: count matches, weighted by word count ──
        # CRITICAL: use word-boundary matching, NOT plain substring, otherwise
        # short keywords like "rc" (RC circuit) would falsely match inside
        # "exe**rc**ice", "ph" inside "ph**ph**enomenon", etc., giving every
        # query containing "exercice" a phantom Physique point that beats
        # SVT (1 vs 1, ties broken by iteration order favouring Physique).
        # Accent-stripped comparison so "génétique" matches "genetique".
        import unicodedata as _ud
        def _strip(s: str) -> str:
            return "".join(c for c in _ud.normalize("NFD", s) if _ud.category(c) != "Mn")
        t_norm = _strip(t)

        def _kw_matches(kw: str, haystack: str) -> bool:
            kw_norm = _strip(kw.lower())
            # Multi-word phrases: substring match is safe because spaces act as
            # natural boundaries.
            if " " in kw_norm or "-" in kw_norm:
                return kw_norm in haystack
            # Single token: require word boundaries.
            return re.search(rf"(?<![a-zA-Z0-9]){re.escape(kw_norm)}(?![a-zA-Z0-9])", haystack) is not None

        _subjects = {
            "Mathématiques": math_kw,
            "Physique": phys_kw,
            "Chimie": chem_kw,
            "SVT": svt_kw,
        }
        scores: dict[str, int] = {}
        for subj, kw_list in _subjects.items():
            scores[subj] = sum(
                len(kw.split()) for kw in kw_list if _kw_matches(kw, t_norm)
            )
        best_score = max(scores.values()) if scores else 0
        if best_score <= 0:
            return None
        # On ties, prefer SVT > Chimie > Mathématiques > Physique because the
        # Physique list contains very common words ("force", "champ", "circuit",
        # "résistance") that easily appear in SVT/Chimie texts.
        priority = ["SVT", "Chimie", "Mathématiques", "Physique"]
        for subj in priority:
            if scores.get(subj, 0) == best_score:
                return subj
        return None

    def _infer_subject_from_context(self, fallback: Optional[str] = "SVT") -> Optional[str]:
        ctx = self.session_context or {}
        explicit_subject = (ctx.get("subject") or "").strip()
        if explicit_subject and explicit_subject.lower() not in {"général", "general", "mode libre"}:
            return explicit_subject

        text_parts = []
        for key in ["lesson_title", "chapter_title", "objective", "scenario"]:
            value = ctx.get(key)
            if isinstance(value, str) and value.strip():
                text_parts.append(value.lower())
        for msg in self.conversation_history[-6:]:
            if isinstance(msg, dict) and msg.get("role") == "user":
                content = msg.get("content", "")
                if isinstance(content, str):
                    text_parts.append(content.lower())

        text = " ".join(text_parts)
        _safe_log(f"[SubjectDetect] infer_from_context: text_len={len(text)} text='{text[:200]}'")

        # Delegate to the canonical word-boundary + accent-insensitive detector
        # so we avoid the "rc" inside "exercice" / "ph" inside "phenomene"
        # phantom-match pitfall.
        detected = self._detect_subject_from_text(text)
        best_subject = detected or fallback

        _safe_log(f"[SubjectDetect] infer_from_context result: best_subject={best_subject}")
        return best_subject

    def _try_fix_ui_json(self, s: str):
        try:
            return json.loads(s)
        except json.JSONDecodeError:
            pass

        stripped = str(s).strip()
        if not stripped:
            return None

        first_brace = stripped.find('{')
        last_brace = stripped.rfind('}')
        if first_brace >= 0 and last_brace > first_brace:
            try:
                return json.loads(stripped[first_brace:last_brace + 1])
            except json.JSONDecodeError:
                pass

        candidate = stripped[first_brace:] if first_brace >= 0 else stripped
        if candidate.count('"') % 2 != 0:
            candidate += '"'
        candidate += ']' * max(0, candidate.count('[') - candidate.count(']'))
        candidate += '}' * max(0, candidate.count('{') - candidate.count('}'))

        try:
            return json.loads(candidate)
        except (json.JSONDecodeError, ValueError):
            return None

    def _get_structured_response_issue(self, ai_response: str, expected_structured: bool = False):
        text = (ai_response or "").strip()
        if not text:
            return "empty_response"

        placeholder_markers = ['[tableau]', '[dessin]', '[schema]', '[board]', '[ui]']
        if any(marker in text.lower() for marker in placeholder_markers):
            return "placeholder_detected"

        structured_tags = ["ui", "draw", "schema", "board", "exam_exercise"]
        for tag in structured_tags:
            open_count = text.count(f"<{tag}>")
            close_count = text.count(f"</{tag}>")
            if open_count != close_count:
                return f"unbalanced_{tag}_tag"

        ui_blocks = re.findall(r'<ui>(.*?)</ui>', text, re.DOTALL)
        if not ui_blocks:
            fallback_ui = re.search(r'<ui>(.*)', text, re.DOTALL)
            if fallback_ui:
                ui_blocks = [fallback_ui.group(1)]

        if ui_blocks:
            valid_ui_found = False
            for ui_json_str in ui_blocks:
                ui_data = self._try_fix_ui_json(str(ui_json_str).strip().replace('</ui>', '').strip())
                if isinstance(ui_data, dict):
                    valid_ui_found = True
                    break
            if not valid_ui_found:
                return "invalid_ui_json"

        has_structured_content = any(
            marker in text
            for marker in [
                "<ui>", "<draw>", "<schema>", "<board>", "<exam_exercise>",
                "OUVRIR_IMAGE", "OUVRIR_SIMULATION", "OUVRIR_EXERCICE",
                "DESSINER_SCHEMA:", "EXERCICE:"
            ]
        )
        if expected_structured and not has_structured_content:
            return "missing_structured_block"

        return None

    def _extract_display_text(self, ai_response: str) -> str:
        text = ai_response or ""
        text = re.sub(r'<ui>[\s\S]*?</ui>', '', text, flags=re.DOTALL)
        text = re.sub(r'<ui>[\s\S]*', '', text, flags=re.DOTALL)
        text = re.sub(r'<board>[\s\S]*?</board>', '', text, flags=re.DOTALL)
        text = re.sub(r'<board>[\s\S]*', '', text, flags=re.DOTALL)
        text = re.sub(r'<draw>[\s\S]*?</draw>', '', text, flags=re.DOTALL)
        text = re.sub(r'<draw>[\s\S]*', '', text, flags=re.DOTALL)
        text = re.sub(r'<schema>[\s\S]*?</schema>', '', text, flags=re.DOTALL)
        text = re.sub(r'<schema>[\s\S]*', '', text, flags=re.DOTALL)
        text = re.sub(r'<exam_exercise>[\s\S]*?</exam_exercise>', '', text, flags=re.DOTALL)
        text = re.sub(r'<exam_exercise>[\s\S]*', '', text, flags=re.DOTALL)
        text = re.sub(r'<suggestions>[\s\S]*?</suggestions>', '', text, flags=re.DOTALL)
        text = re.sub(r'<suggestions>[\s\S]*', '', text, flags=re.DOTALL)
        text = re.sub(r'\[CMD:[^\]]+\]', '', text)

        command_keywords = [
            "FERMER_TABLEAU", "OUVRIR_IMAGE", "FERMER_IMAGE", "CACHER_MEDIA",
            "OUVRIR_SIMULATION", "FERMER_SIMULATION", "OUVRIR_EXERCICE",
            "FERMER_EXERCICE", "TOUT_FERMER", "PHASE_SUIVANTE",
            "DESSINER_SCHEMA:", "EXERCICE:"
        ]
        for cmd in command_keywords:
            text = text.replace(cmd, "")

        text = re.sub(r'[ \t]+\n', '\n', text)
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r'[ \t]{2,}', ' ', text)
        return text.strip()

    async def _extract_and_send_suggestions(self, ai_response: str) -> None:
        """Parse <suggestions>[{"label":"...","prompt":"..."}]</suggestions>
        from the AI response and send the list to the frontend as contextual
        quick-reply buttons aligned on the question the AI just asked."""
        if not ai_response or "<suggestions>" not in ai_response:
            return
        m = re.search(r'<suggestions>\s*(\[[\s\S]*?\])\s*</suggestions>', ai_response, re.DOTALL)
        if not m:
            m = re.search(r'<suggestions>\s*(\[[\s\S]*)', ai_response, re.DOTALL)
        if not m:
            return
        raw = m.group(1).strip()
        # Best-effort close of truncated JSON arrays
        try:
            data = json.loads(raw)
        except Exception:
            try:
                candidate = raw
                open_braces = candidate.count('{')
                close_braces = candidate.count('}')
                open_brackets = candidate.count('[')
                close_brackets = candidate.count(']')
                if candidate.count('"') % 2 != 0:
                    candidate += '"'
                candidate += '}' * max(0, open_braces - close_braces)
                candidate += ']' * max(0, open_brackets - close_brackets)
                data = json.loads(candidate)
            except Exception:
                return
        if not isinstance(data, list):
            return
        cleaned: list[dict] = []
        for idx, item in enumerate(data[:6]):
            if not isinstance(item, dict):
                continue
            label = str(item.get("label", "")).strip()
            prompt = str(item.get("prompt") or item.get("text") or label).strip()
            if not label or not prompt:
                continue
            if len(label) > 40:
                label = label[:37] + "…"
            cleaned.append({
                "id": f"ctx_{idx}",
                "icon": str(item.get("icon", "💬")),
                "label": label,
                "prompt": prompt,
                "mode": "send",
            })
        if cleaned:
            try:
                await self.websocket.send_json({
                    "type": "quick_suggestions",
                    "suggestions": cleaned,
                })
            except Exception as e:
                _safe_log(f"[AI Commands] Failed to send quick_suggestions: {e}")

    async def _send_ai_response_text(self, ai_response: str):
        display_text = self._extract_display_text(ai_response)
        if display_text:
            # Send entire text in ONE chunk — the full response is already available
            # (not streaming), so chunking only adds network round-trip latency.
            await self.websocket.send_json({
                "type": "ai_response_chunk",
                "token": display_text,
            })
        await self.websocket.send_json({"type": "ai_response_done"})
        # Contextual quick-reply buttons aligned on what the AI just asked
        await self._extract_and_send_suggestions(ai_response)

    async def _generate_validated_ai_response(
        self,
        messages: list[dict],
        system_prompt: str,
        max_tokens: int,
        expected_structured: bool = False,
        context_label: str = "chat",
    ) -> str:
        attempt_messages = [dict(message) for message in messages]
        last_response = ""

        for attempt in range(3):
            attempt_max_tokens = max_tokens if attempt == 0 else max(max_tokens + 600 * attempt, 1800 if expected_structured else max_tokens)
            temperature = 0.7 if attempt == 0 else 0.2
            last_response = await llm_service.chat(
                messages=attempt_messages,
                system_prompt=system_prompt,
                temperature=temperature,
                max_tokens=attempt_max_tokens,
            )

            issue = self._get_structured_response_issue(last_response, expected_structured=expected_structured)
            if not issue:
                if attempt > 0:
                    _safe_log(f"[LLM Guard] {context_label} repaired on attempt {attempt + 1}")
                return last_response

            _safe_log(f"[LLM Guard] {context_label} invalid on attempt {attempt + 1}: {issue}")
            if attempt == 2:
                return last_response

            repair_instruction = (
                "Ta réponse précédente est invalide ou incomplète. Regénère UNE réponse finale complète et exploitable. "
                f"Problème détecté: {issue}. "
                "Règles obligatoires: aucun placeholder comme [ui] ou [tableau]; si tu utilises <ui>, le JSON doit être complet, valide et fermé par </ui>; "
                "si un affichage structuré est attendu, fournis-le entièrement dans cette même réponse; ne coupe pas le JSON; garde aussi le texte pédagogique utile."
            )
            attempt_messages = attempt_messages + [
                {"role": "assistant", "content": last_response},
                {"role": "user", "content": repair_instruction},
            ]

        return last_response

    def _build_explain_scenario_block(self) -> str:
        """Build a high-priority block injected at the TOP of the system prompt
        for explain mode (mode entraînement after BAC exam). Persists the
        official correction + student answer + evaluator feedback across ALL
        follow-up turns so the LLM never drifts from the official correction
        when the student asks "et pourquoi cette étape ?", "donne un autre
        exemple", etc.
        """
        ctx = self.session_context
        scenario_raw = ctx.get("scenario", "") or ""
        if not scenario_raw:
            return ""
        try:
            data = json.loads(scenario_raw) if isinstance(scenario_raw, str) else dict(scenario_raw)
        except Exception:
            return ""

        q_content = (data.get("questionContent") or "").strip()
        q_type = (data.get("questionType") or "open").strip()
        q_points = data.get("points") or 0
        q_correction = (data.get("correction") or "").strip()
        student_answer = (data.get("studentAnswer") or "").strip()
        student_score = data.get("studentScore")
        student_points_max = data.get("studentPointsMax")
        evaluator_feedback = (data.get("evaluatorFeedback") or "").strip()
        has_answer = bool(data.get("hasAnswer"))
        subject = (data.get("subject") or "").strip()
        exam_title = (data.get("examTitle") or "").strip()

        if not q_content and not q_correction:
            return ""

        # Cap heavy fields so the system prompt stays small enough.
        def _trim(s: str, n: int) -> str:
            s = s.strip()
            return s if len(s) <= n else s[:n].rstrip() + " […]"

        lines = [
            "[CONTEXTE EXAMEN — MODE ENTRAÎNEMENT / EXPLICATION DE CORRECTION]",
            "⚠️ L'étudiant travaille sur UNE question d'examen BAC précise. "
            "Tu DOIS baser TOUTE ta correction et tes explications sur la "
            "CORRECTION OFFICIELLE ci-dessous, et non sur tes connaissances "
            "générales. NE T'ÉLOIGNE JAMAIS de cette question.",
            "",
            "🎓 [VERROU NIVEAU 2BAC PC BIOF — APPLICABLE AU CHAT ET AUX TABLEAUX <ui>/<board>]",
            "Tu enseignes à un LYCÉEN 17-18 ans qui passe l'examen national marocain. "
            "TOUTE explication, TOUTE formule, TOUTE notation, TOUTE démonstration "
            "doit rester strictement dans les limites du programme officiel 2BAC PC BIOF.",
            "",
            "✓ AUTORISÉ : méthodes/formules/notations qui apparaissent dans la "
            "correction officielle ci-dessous OU dans le manuel marocain officiel.",
            "✗ INTERDIT (jargon supérieur — JAMAIS dans le chat NI dans le tableau) :",
            "  • Maths : espace vectoriel, endomorphisme, polynôme caractéristique, "
            "diagonalisation, dérivées partielles, séries entières, transformée "
            "de Laplace/Fourier, jacobien, Hilbert, opérateur linéaire, ε-δ.",
            "  • Physique : équation de Schrödinger, lagrangien, hamiltonien, "
            "Euler-Lagrange, équations de Maxwell, transformations de Lorentz, "
            "relativité restreinte, ∇·, ∇×, opérateurs vectoriels avancés.",
            "  • Chimie : équation de Nernst, Henderson-Hasselbalch, énergie libre "
            "de Gibbs, ΔG/ΔS, mécanismes SN1/SN2/E1/E2, RMN, VSEPR, orbitales "
            "hybrides, diagramme E-pH, cristallographie.",
            "  • SVT : photosynthèse, cycle de Calvin, immunologie, cycle menstruel, "
            "PCR/CRISPR, Hardy-Weinberg, sélection naturelle.",
            "",
            "🔒 RÈGLE D'OR — la correction officielle ci-dessous est PLAFOND ET PLANCHER :",
            "- Tu ne donnes JAMAIS une démonstration plus rigoureuse / générale / "
            "élégante que la correction officielle. Si la correction utilise une "
            "méthode lycée, tu utilises CETTE méthode-là, pas une variante sup.",
            "- Tu ne réécris pas la formule en notation plus avancée (ex : ne "
            "remplace pas $\\frac{dy}{dx}$ par $\\partial_x y$, ne remplace pas "
            "$\\vec{F}$ par $F^\\mu$, ne remplace pas $K_a$ par une activité "
            "thermodynamique).",
            "- Si la correction est silencieuse sur un détail, tu DIS qu'elle est "
            "silencieuse — tu ne complètes PAS avec une dérivation universitaire.",
            "- Si l'élève demande une « méthode plus générale / plus rigoureuse », "
            "tu refuses poliment : « Pour le BAC tu ne dois maîtriser QUE cette "
            "méthode du programme. La version plus générale est universitaire et "
            "te ferait perdre du temps le jour J. »",
            "",
        ]
        if exam_title:
            lines.append(f"📚 Examen : {exam_title}" + (f" ({subject})" if subject else ""))
        lines.append(f"❓ Question ({q_type}, {q_points} pt) :")
        lines.append(_trim(q_content, 1200))
        lines.append("")
        lines.append("✅ CORRECTION OFFICIELLE (source de vérité — tu te bases sur ce contenu) :")
        lines.append(_trim(q_correction, 1500) if q_correction else "(non fournie)")

        if has_answer:
            lines.append("")
            if student_answer:
                lines.append("📝 RÉPONSE DE L'ÉLÈVE (à citer textuellement entre guillemets) :")
                lines.append(f"« {_trim(student_answer, 800)} »")
            else:
                lines.append("📝 L'élève n'a pas écrit de texte (peut-être un schéma uniquement).")
            if student_score is not None and student_points_max:
                lines.append(f"🔢 Note évaluateur automatique : {student_score}/{student_points_max}")
            if evaluator_feedback:
                lines.append("🧮 Feedback évaluateur (référence interne, NE PAS citer mot-à-mot) :")
                lines.append(_trim(evaluator_feedback, 800))

        lines.append("")
        lines.append("RÈGLES STRICTES POUR CETTE SESSION :")
        lines.append("- Reste TOUJOURS sur cette question — ne change pas de sujet sauf demande explicite.")
        lines.append("- Quand l'élève demande « pourquoi », « explique cette étape », « un autre exemple », tu réponds en t'appuyant DIRECTEMENT sur la correction officielle ci-dessus.")
        lines.append("- Tu cites la réponse de l'élève entre guillemets avant de la critiquer ou féliciter.")
        lines.append("- Tu n'inventes JAMAIS d'éléments absents de la correction officielle ; si la correction est silencieuse sur un détail, dis-le.")
        lines.append("- Le contenu des tableaux <ui>/<board> doit OBLIGATOIREMENT respecter le verrou niveau 2BAC ci-dessus (formules, notations, vocabulaire).")
        lines.append("- Une « version modèle » ou « rédaction parfaite » que tu donnes ne doit JAMAIS être plus avancée que la correction officielle. C'est un copier-coller stylisé du programme, pas une généralisation.")
        lines.append("")
        lines.append("✍️ RÈGLE DE RÉDACTION (style copie BAC) — APPLICABLE À TOUTE « réponse modèle / éléments de réponse / version idéale » que tu produis dans cette session :")
        lines.append("- PHRASES COMPLÈTES avec connecteurs scientifiques, JAMAIS de mots-clés télégraphiques.")
        lines.append("- Comparaison → commence par « On remarque que… », « On constate que… », « En comparant X et Y, on note que… ».")
        lines.append("- Déduction → « On en déduit que… », « Par conséquent… », « Il en résulte que… ».")
        lines.append("- Observation → « D'après le document N°…, on observe que… ».")
        lines.append("- Justification → « Cela s'explique par le fait que… », « En effet,… », « Car… ».")
        lines.append("- Dans un TABLEAU comparatif, chaque cellule « Réponse modèle » est UNE PHRASE COMPLÈTE (sujet + verbe + complément). Mots-clés isolés (« mitose », « prophase », « plus rapide ») = INTERDIT.")
        lines.append("- Chaque ligne du tableau traite UN critère DIFFÉRENT — interdit de répéter le même élément de réponse sur plusieurs lignes.")
        lines.append("- COMPLÉTUDE TABLEAU : la cellule « Réponse modèle » contient la RÉDACTION COMPLÈTE du critère (mêmes phrases que celles que tu écrirais dans le chat) — JAMAIS « Idem », « Voir ci-dessus », « cf. chat », « Mêmes éléments », ou une version raccourcie. Le tableau doit pouvoir se lire tout seul, sans le chat, et donner à l'élève une copie BAC complète.")
        lines.append("")
        lines.append("🧬 RÈGLE GÉNÉTIQUE (si la question porte sur un croisement / hérédité) :")
        lines.append("- L'interprétation chromosomique va OBLIGATOIREMENT dans un bloc <ui> show_board, avec : phénotypes, génotypes en `\\\\dfrac`, gamètes, ÉCHIQUIER de fécondation en `type=table`, résultats. Cf. PROTOCOLE_GÉNÉTIQUE en haut.")
        lines.append("- INTERDIT dans le texte parlé OU dans les cellules : notations ASCII type `DO//dø`, `D O / d o`, `J/J;L/L`. Uniquement du LaTeX `\\\\dfrac{D}{\\\\overline{d}}\\\\,\\\\dfrac{O}{\\\\overline{o}}` (2 backslashes JSON).")
        lines.append("- 🧬 GÉNOTYPE = DIPLOÏDE → DEUX BARRES horizontales obligatoires : `\\\\dfrac{A}{\\\\overline{a}}` (la barre de fraction + l'overline simulent la paire de chromosomes homologues). JAMAIS `\\\\dfrac{A}{a}` (une seule barre = haploïde, FAUX pour un génotype). Les GAMÈTES, eux, restent en UNE seule barre `\\\\dfrac{A}{}` (dénominateur vide, sans overline) car ils sont haploïdes.")
        lines.append("- La rédaction texte (« On constate que… », « On en déduit que… ») COEXISTE avec l'échiquier <ui> ; elle ne le remplace pas.")
        return "\n".join(lines)

    def _build_session_system_prompt(self, user_query: str = "", prof_ctx: dict = None) -> str:
        ctx = self.session_context
        if self.session_mode in ("libre", "explain"):
            # Build user_query from recent conversation for RAG lookup
            if not user_query:
                user_query = " ".join(
                    msg.get("content", "")
                    for msg in self.conversation_history[-4:]
                    if isinstance(msg, dict) and msg.get("role") == "user" and isinstance(msg.get("content"), str)
                ).strip()

            # ── Explain mode: enrich user_query with the exam question +
            #    correction content so keyword-driven prompt blocks (RAG,
            #    genetics rendering protocol, exam stats…) fire on the
            #    actual exam topic and not only on what the student typed.
            #    Without this, a SVT genetics exam question would NOT
            #    trigger GENETICS_BOARD_PROTOCOL because the student's
            #    follow-ups ("explique-moi", "pourquoi ?") don't contain
            #    any genetics keyword.
            if self.session_mode == "explain":
                try:
                    scenario_raw = ctx.get("scenario", "") or ""
                    if scenario_raw:
                        sdata = (json.loads(scenario_raw)
                                 if isinstance(scenario_raw, str)
                                 else dict(scenario_raw))
                        scenario_kw = " ".join(filter(None, [
                            sdata.get("subject", ""),
                            sdata.get("questionContent", ""),
                            sdata.get("correction", ""),
                        ]))[:1500]
                        if scenario_kw:
                            user_query = (user_query + " " + scenario_kw).strip()
                except Exception:
                    pass

            # Libre mode: use the multi-subject libre prompt (covers Math, Physics, Chemistry, SVT)
            base_prompt = llm_service.build_libre_prompt(
                language=self._prompt_language(),
                student_name=ctx.get("student_name", "l'étudiant"),
                proficiency=prof_ctx["proficiency"] if prof_ctx else ctx.get("proficiency", "intermédiaire"),
                user_query=user_query,
            )

            # ── EXPLAIN MODE: persist exam-question scenario (official correction
            #    + student answer + evaluator feedback) in the SYSTEM prompt for
            #    EVERY turn, not just the opening. Without this, follow-up
            #    questions (the most common case) lose the correction context
            #    and the LLM falls back to its general/university-level knowledge
            #    instead of grounding feedback on the official correction.
            if self.session_mode == "explain":
                scenario_block = self._build_explain_scenario_block()
                if scenario_block:
                    base_prompt = scenario_block + "\n\n" + base_prompt
            return base_prompt
        return llm_service.build_system_prompt(
            subject=ctx.get("subject", "Physique"),
            language=self._prompt_language(),
            chapter_title=ctx.get("chapter_title", ""),
            lesson_title=ctx.get("lesson_title", ""),
            objective=ctx.get("objective", ""),
            scenario_context=ctx.get("scenario", ""),
            student_name=ctx.get("student_name", "l'étudiant"),
            proficiency=prof_ctx["proficiency"] if prof_ctx else ctx.get("proficiency", "intermédiaire"),
            struggles=prof_ctx["struggles"] if prof_ctx else ctx.get("struggles", "aucune identifiée"),
            mastered=prof_ctx["mastered"] if prof_ctx else ctx.get("mastered", "aucun"),
            teaching_mode=ctx.get("teaching_mode", "Socratique"),
            user_query=user_query,  # Pass user_query for RAG context
        )

    async def handle_connection(self):
        """Main WebSocket handler loop."""
        await manager.connect(self.student_id, self.websocket)

        try:
            # Send ready signal
            await self.websocket.send_json({
                "type": "connected",
                "message": "AI Tutor connected and ready"
            })

            while True:
                data = await self.websocket.receive()

                if "text" in data:
                    await self._handle_text_message(data["text"])
                elif "bytes" in data:
                    await self._handle_audio_message(data["bytes"])

        except WebSocketDisconnect:
            manager.disconnect(self.student_id)
        except RuntimeError:
            manager.disconnect(self.student_id)
        except Exception as e:
            try:
                await self.websocket.send_json({
                    "type": "error",
                    "message": f"An error occurred: {str(e)}"
                })
            except Exception:
                pass
            manager.disconnect(self.student_id)

    async def _handle_text_message(self, raw_text: str):
        """Handle text-based messages (commands, text input)."""
        try:
            message = json.loads(raw_text)
        except json.JSONDecodeError:
            message = {"type": "text_input", "text": raw_text}

        msg_type = message.get("type", "text_input")

        if msg_type == "init_session":
            await self._init_session(message)
        elif msg_type == "text_input":
            student_text = message.get("text", "")
            exam_context = message.get("exam_context", False)
            exam_question_number = message.get("exam_question_number")
            exam_total_questions = message.get("exam_total_questions")
            # When student submits an answer for verification from the exam panel,
            # the frontend sets suppress_whiteboard=True so the correction stays
            # in the chat/panel instead of opening the whiteboard.
            suppress_whiteboard_flag = bool(message.get("suppress_whiteboard", False))
            student_image = message.get("student_image")
            # If a drawing/photo was attached, run it through the vision service
            # so the LLM can "see" and correct what the student drew.
            if student_image:
                try:
                    from app.services.vision_service import analyze_student_image
                    q_content = message.get("question_content", "") or student_text[:300]
                    q_correction = message.get("question_correction", "")
                    subject = message.get("subject", "") or self.session_context.get("subject", "")
                    await self.websocket.send_json({"type": "processing", "stage": "vision"})
                    _safe_log(f"[Vision] Analyzing student drawing (subject={subject}, q_len={len(q_content)})")
                    vision_result = await analyze_student_image(
                        image_base64=student_image,
                        question_content=q_content,
                        correction_content=q_correction,
                        question_type="open",
                        subject=subject,
                    )
                    extracted = (vision_result or {}).get("extracted_text", "").strip()
                    diagram = (vision_result or {}).get("diagram_description", "").strip()
                    vision_error = (vision_result or {}).get("error")
                    if vision_error:
                        _safe_log(f"[Vision] Error: {vision_error}")
                        student_text += f"\n\n[Note: analyse du dessin partielle - {vision_error}]"
                    else:
                        vision_block = []
                        if extracted:
                            vision_block.append(f"Texte manuscrit extrait du dessin:\n{extracted}")
                        if diagram:
                            vision_block.append(f"Description du schéma/courbe dessinée:\n{diagram}")
                        if vision_block:
                            student_text += "\n\n=== CONTENU DU DESSIN DE L'ÉLÈVE ===\n" + "\n\n".join(vision_block)
                            _safe_log(f"[Vision] Extracted {len(extracted)} chars text + {len(diagram)} chars diagram")
                except Exception as e:
                    _safe_log(f"[Vision] Unexpected error analyzing drawing: {type(e).__name__}: {e}")
            await self._process_student_input(
                student_text,
                exam_context=exam_context,
                force_suppress_whiteboard=suppress_whiteboard_flag,
                exam_question_number=exam_question_number,
                exam_total_questions=exam_total_questions,
            )
        elif msg_type == "exam_answer":
            await self._handle_exam_answer(message)
        elif msg_type == "set_exam_panel_view":
            # Frontend tells us which exam/exercise/question is currently visible
            # in the exam panel. We store it so any subsequent free-form message
            # (voice, "Aide au tableau", etc.) is grounded in the real metadata
            # and the LLM cannot hallucinate the year/session/exercise.
            view = message.get("view") or {}
            if isinstance(view, dict) and view:
                self.current_exam_view = view
                _safe_log(
                    f"[Exam View] Updated: {view.get('subject','?')} {view.get('year','?')} "
                    f"{view.get('session','?')} | {view.get('exercise_name','?')} | "
                    f"Q{view.get('question_number','?')}/{view.get('question_total','?')}"
                )
        elif msg_type == "clear_exam_panel_view":
            if self.current_exam_view is not None:
                _safe_log("[Exam View] Cleared (panel closed)")
            self.current_exam_view = None
        elif msg_type == "simulation_manifest":
            await self._handle_simulation_manifest(message)
        elif msg_type == "simulation_update":
            await self._handle_simulation_update(message)
        elif msg_type == "change_phase":
            self.current_phase = message.get("phase", self.current_phase)
            await self.websocket.send_json({
                "type": "phase_changed",
                "phase": self.current_phase
            })
        elif msg_type == "set_language":
            self.language = message.get("language", "fr")

    async def _handle_exam_answer(self, message: dict):
        """Handle structured exam answer from the exam panel for proficiency tracking."""
        try:
            from app.services.student_proficiency_service import proficiency_service

            answer_data = message.get("answer", {})
            subject = answer_data.get("subject", self.session_context.get("subject", ""))
            topic = answer_data.get("topic", "")
            question_content = answer_data.get("question_content", "")
            student_answer = answer_data.get("student_answer", "")
            correct_answer = answer_data.get("correct_answer", "")
            question_type = answer_data.get("question_type", "open")
            max_points = float(answer_data.get("max_points", 1))
            exam_id = answer_data.get("exam_id", "")
            exercise_name = answer_data.get("exercise_name", "")
            part_name = answer_data.get("part_name", "")
            year = answer_data.get("year", "")

            # Auto-evaluate for deterministic types (QCM, vrai/faux)
            is_correct, score = proficiency_service.evaluate_answer(
                question_type=question_type,
                student_answer=student_answer,
                correct_answer=correct_answer,
                max_points=max_points,
            )

            # For open/schema questions, use LLM-provided evaluation if available
            if question_type in ("open", "schema") and "is_correct" in answer_data:
                is_correct = answer_data["is_correct"]
                score = float(answer_data.get("score", max_points if is_correct else 0))

            await proficiency_service.record_answer(
                student_id=self.student_id,
                subject=subject,
                topic=topic,
                question_content=question_content,
                student_answer=student_answer,
                correct_answer=correct_answer,
                is_correct=is_correct,
                question_type=question_type,
                score=score,
                max_score=max_points,
                source="exam",
                exam_id=exam_id,
                exercise_name=exercise_name,
                part_name=part_name,
                year=year,
            )

            # Send confirmation back to frontend
            await self.websocket.send_json({
                "type": "answer_recorded",
                "is_correct": is_correct,
                "score": score,
                "max_score": max_points,
            })

            _safe_log(f"[ExamAnswer] Recorded: subject={subject} topic={topic} "
                      f"type={question_type} correct={is_correct} score={score}/{max_points}")
        except Exception as e:
            _safe_log(f"[ExamAnswer] Error: {e}")

    async def _detect_and_record_chat_answer(
        self, student_text: str, ai_response: str, prof_ctx: dict = None
    ):
        """
        Detect when a student answers a question during libre/coaching chat
        and record it in the proficiency agent. Runs as background task.

        Detection logic:
        1. Look back at the previous AI message — did it ask a question?
        2. Does the current AI response contain evaluation keywords (correct/incorrect)?
        3. If both true → extract subject/topic from context and record.
        """
        try:
            # Skip very short exchanges or non-answer patterns
            if len(student_text.strip()) < 3 or len(ai_response) < 20:
                return

            # ── EXPLICIT NAVIGATION INTENT ──
            # If student explicitly asks to advance, treat as successful progression
            student_lower = student_text.lower().strip()
            advance_intents = [
                "objectif suivant", "passer à la suite", "passer a la suite",
                "j'ai compris", "j'ai bien compris", "c'est clair",
                "continuer", "passons à", "passons a",
                "étape suivante", "etape suivante",
                "question suivante",
            ]
            is_explicit_advance = any(p in student_lower for p in advance_intents)
            
            if is_explicit_advance and self.session_mode == "coaching" \
               and hasattr(self, 'lesson_objectives') and self.lesson_objectives:
                _safe_log(f"[ChatDetect] Explicit advance intent detected: '{student_text[:60]}'")
                await self._advance_next_objective()
                return

            # Check if previous AI message contained a question
            prev_ai = None
            for msg in reversed(self.conversation_history[:-1]):
                if isinstance(msg, dict) and msg.get("role") == "assistant":
                    prev_ai = msg.get("content", "")
                    break
            if not prev_ai or "?" not in prev_ai:
                return  # AI didn't ask a question → not an exercise

            ai_lower = ai_response.lower()

            # Detect evaluation patterns in AI response — use STRICT multi-word patterns
            # to avoid false positives (e.g. "correct" alone can appear in explanations)
            correct_patterns = [
                "c'est correct", "bonne réponse", "réponse correcte",
                "c'est juste", "bien joué", "c'est exact",
                "bravo !", "bravo!", "bravo,", "exactement !",
                "très bien !", "excellente réponse", "tu as raison",
            ]
            incorrect_patterns = [
                "ce n'est pas correct", "réponse incorrecte", "pas tout à fait",
                "la bonne réponse est", "la réponse correcte est",
                "pas exactement", "ce n'est pas la bonne",
                "malheureusement", "pas correct", "tu as fait une erreur",
                "la réponse attendue", "il fallait répondre",
            ]

            is_correct = any(p in ai_lower for p in correct_patterns)
            is_wrong = any(p in ai_lower for p in incorrect_patterns)

            if not is_correct and not is_wrong:
                return  # AI didn't evaluate → not an exercise exchange

            # Additional guard: response must be short-ish (evaluation, not lecture)
            # A 2000+ char response is likely a lesson, not an evaluation
            if len(ai_response) > 2000 and not is_wrong:
                return

            # Determine subject from session context
            ctx = self.session_context
            subject = ctx.get("subject", "")
            if not subject and self.session_mode in ("libre", "explain"):
                subject = self._detect_subject(student_text + " " + prev_ai)
            topic = ctx.get("chapter_title", ctx.get("lesson_title", ""))

            from app.services.student_proficiency_service import proficiency_service
            await proficiency_service.record_answer(
                student_id=self.student_id,
                subject=subject or "Général",
                topic=topic or "Conversation",
                question_content=prev_ai[:300] if prev_ai else "",
                student_answer=student_text[:300],
                correct_answer="",  # Not always available in chat
                is_correct=is_correct and not is_wrong,
                question_type="open",
                score=1.0 if (is_correct and not is_wrong) else 0.0,
                max_score=1.0,
                source="chat_" + self.session_mode,
            )
            _safe_log(f"[ChatDetect] Recorded chat answer: subject={subject} "
                      f"correct={is_correct and not is_wrong} mode={self.session_mode}")

            # ── AUTO-ADVANCE PROGRESS BAR ──
            # In coaching mode, advance objective after correct answers
            if (is_correct and not is_wrong and
                self.session_mode == "coaching" and
                hasattr(self, 'lesson_objectives') and self.lesson_objectives):

                # Initialize per-objective correct answer counter
                if not hasattr(self, '_correct_answers_counter'):
                    self._correct_answers_counter = 0
                if not hasattr(self, '_completed_objective_indices'):
                    self._completed_objective_indices = set()

                self._correct_answers_counter += 1

                # After 2 correct answers, advance to next objective
                if self._correct_answers_counter >= 2:
                    await self._advance_next_objective()
                    self._correct_answers_counter = 0  # Reset for next objective
        except Exception as e:
            _safe_log(f"[ChatDetect] Error: {e}")

    async def _advance_next_objective(self):
        """Mark the next uncompleted objective as done, save to DB, notify frontend."""
        try:
            if not hasattr(self, '_completed_objective_indices'):
                self._completed_objective_indices = set()
            if not hasattr(self, 'lesson_objectives') or not self.lesson_objectives:
                return
            
            # Find the next uncompleted objective
            next_idx = None
            for i in range(len(self.lesson_objectives)):
                if i not in self._completed_objective_indices:
                    next_idx = i
                    break
            
            if next_idx is None:
                # All objectives already done — nothing to do
                return
            
            self._completed_objective_indices.add(next_idx)
            total_objectives = len(self.lesson_objectives)
            is_lesson_complete = len(self._completed_objective_indices) >= total_objectives
            
            # Save to database
            lesson_id = getattr(self, 'current_lesson_id', None)
            try:
                if lesson_id:
                    await session_progress_service.create_or_update_progress(
                        student_id=self.student_id,
                        lesson_id=lesson_id,
                        objectives_total=total_objectives,
                        objectives_completed=list(self._completed_objective_indices),
                        current_objective_index=next_idx + 1,
                        status="completed" if is_lesson_complete else "in_progress",
                    )
                    _safe_log(f"[Progress] Saved objective {next_idx} to DB (lesson_id={lesson_id[:8]}..), complete={is_lesson_complete}")
                else:
                    _safe_log(f"[Progress][WARN] No current_lesson_id - progress NOT saved!")
            except Exception as e:
                _safe_log(f"[Progress] Error saving objective {next_idx}: {e}")
            
            # Notify frontend
            await self.websocket.send_json({
                "type": "objective_completed",
                "objective_index": next_idx,
                "objective": self.lesson_objectives[next_idx],
            })
            _safe_log(f"[Progress] Advanced objective {next_idx} ({len(self._completed_objective_indices)}/{total_objectives})")
            
            # Lesson completion
            if is_lesson_complete:
                self._lesson_completed = True
                await self.websocket.send_json({
                    "type": "lesson_completed",
                    "lesson_id": lesson_id,
                    "objectives_total": total_objectives,
                    "message": "Félicitations ! Tu as complété tous les objectifs de cette leçon."
                })
                _safe_log(f"[Progress] 🎉 LESSON COMPLETED: {lesson_id[:8] if lesson_id else '?'}..")
                
                # ── PROPAGATE TO CALENDAR & GLOBAL PROGRESS ──
                # Find matching study_plan_session (chapter-level) and mark it completed.
                if lesson_id:
                    try:
                        from app.supabase_client import get_supabase_admin
                        from app.services.study_plan_service import study_plan_service
                        sb = get_supabase_admin()
                        # Get chapter_id for this lesson
                        lesson_row = sb.table("lessons").select("chapter_id").eq("id", lesson_id).execute()
                        if lesson_row.data:
                            chapter_id = lesson_row.data[0].get("chapter_id")
                            if chapter_id:
                                # Find earliest pending study_plan_session for this chapter + student
                                sps_result = sb.table("study_plan_sessions").select("id, plan_id, status").eq(
                                    "chapter_id", chapter_id
                                ).neq("status", "completed").order("scheduled_date").limit(1).execute()
                                
                                # Must also check it belongs to this student via the plan
                                if sps_result.data:
                                    sps = sps_result.data[0]
                                    plan_row = sb.table("study_plans").select("student_id").eq(
                                        "id", sps["plan_id"]
                                    ).execute()
                                    if plan_row.data and plan_row.data[0]["student_id"] == self.student_id:
                                        await study_plan_service.mark_session_completed(
                                            session_id=sps["id"],
                                            student_id=self.student_id,
                                        )
                                        _safe_log(f"[Progress] ✅ Marked study_plan_session {sps['id'][:8]}.. as completed (chapter={chapter_id[:8]}..)")
                                    else:
                                        _safe_log(f"[Progress] Plan session found but belongs to different student")
                                else:
                                    _safe_log(f"[Progress] No pending study_plan_session found for chapter {chapter_id[:8]}..")
                    except Exception as prop_err:
                        _safe_log(f"[Progress] Error propagating completion to calendar: {prop_err}")
        except Exception as e:
            _safe_log(f"[Progress] _advance_next_objective error: {e}")

    def _detect_subject(self, text: str) -> str:
        """Detect subject from text content using keyword matching."""
        text_lower = text.lower()
        subject_keywords = {
            "Mathématiques": ["math", "fonction", "dérivée", "intégral", "suite", "complexe",
                              "probabilit", "limite", "logarithm", "exponentiel", "géométrie"],
            "Physique": ["physique", "onde", "newton", "force", "énergie", "mécanique",
                         "électri", "magnéti", "optique", "noyau", "radioactiv"],
            "Chimie": ["chimie", "réaction", "acide", "base", "pH", "oxydation",
                       "ester", "pile", "électrolyse", "cinétique", "mole"],
            "SVT": ["svt", "biologie", "cellule", "ADN", "génétique", "enzyme",
                    "mitose", "immunolog", "glycolyse", "respiration cellulaire",
                    "fermentation", "géologie", "plaque", "subduction"],
        }
        scores = {}
        for subj, keywords in subject_keywords.items():
            scores[subj] = sum(1 for kw in keywords if kw.lower() in text_lower)
        best = max(scores, key=scores.get)
        return best if scores[best] > 0 else ""

    async def _handle_audio_message(self, audio_bytes: bytes):
        """Handle audio input: STT -> process -> TTS."""
        _safe_log(f"[STT] Received audio ({len(audio_bytes)} bytes, lang={self.language})")
        # Notify frontend that processing started
        await self.websocket.send_json({"type": "processing", "stage": "stt"})

        # Step 1: Speech-to-Text via Gemini (supports Darija natively)
        # Pass the RAW session language (fr/ar/mixed) so the STT prompt
        # can produce Darija in Arabic script for 'mixed'.
        try:
            transcript = await stt_service.transcribe_audio(audio_bytes, self.language or "fr")
        except Exception as e:
            _safe_log(f"[STT] Exception: {e}")
            await self.websocket.send_json({
                "type": "ai_response",
                "text": "Je n'ai pas bien entendu, peux-tu répéter ?",
                "error": "stt_failed"
            })
            return

        if not transcript:
            _safe_log("[STT] Empty transcript returned")
            await self.websocket.send_json({
                "type": "ai_response",
                "text": "Je n'ai pas bien entendu, peux-tu répéter ?",
            })
            return

        _safe_log(f"[STT] Transcript: {transcript[:100]}")

        # Send transcription to frontend
        await self.websocket.send_json({
            "type": "transcription",
            "text": transcript
        })

        # Step 2: Process through LLM
        await self._process_student_input(transcript)

    async def _process_student_input(self, student_text: str, exam_context: bool = False, force_suppress_whiteboard: bool = False, exam_question_number: int = None, exam_total_questions: int = None):
        """Process student text through streaming LLM and return TTS audio."""
        # Check if a simulation is waiting for student answer
        handled = await self.handle_simulation_student_answer(student_text)
        if handled:
            return  # Simulation orchestration handled this input

        # ── PROACTIVE EXAM BANK SEARCH ──
        # If student explicitly asks for exam exercises, detect intent and let LLM decide
        # BUT skip if exam_context=True (follow-up question from exam panel like hint/method/course)
        # force_suppress_whiteboard=True when the student clicked "Vérifier ma réponse"
        # in the exam panel — the correction must stay in the chat, not open the board.
        exam_sent = bool(force_suppress_whiteboard)
        is_exam_request = False
        if not exam_context:
            student_lower = student_text.lower()
            # Keywords that indicate user wants exam exercises
            exam_keywords = ["examen", "bac", "question bac", "exercice bac", 
                             "national", "exercice d'examen", "exercice de examen",
                             "entraîne", "entraine", "évaluation", "evaluation",
                             "teste moi", "tester", "exercice svt", "exercice physique",
                             "exercice chimie", "exercice math"]
            is_exam_request = any(kw in student_lower for kw in exam_keywords)
        else:
            _safe_log(f"[Exam Context] Follow-up question from exam panel, skipping exam search. AI free to use whiteboard/media.")
        
        if is_exam_request:
            _safe_log(f"[Exam Request] Detected exam intent for '{student_text}', delegating display mode choice to LLM")
            exam_sent = True  # suppress whiteboard to avoid old-format exercise display

        # Notify frontend
        await self.websocket.send_json({"type": "processing", "stage": "llm"})

        # Add to conversation history
        self._append_history("user", student_text)

        # ── FETCH STUDENT PROFICIENCY (from answer history agent) ──
        ctx = self.session_context
        prof_ctx = None
        try:
            from app.services.student_proficiency_service import proficiency_service
            prof_ctx = await proficiency_service.get_llm_context(self.student_id)
        except Exception as e:
            _safe_log(f"[Proficiency] Error fetching context: {e}")

        # Build system prompt based on mode, using live proficiency data
        if self.session_mode in ("libre", "explain"):
            system_prompt = self._build_session_system_prompt(user_query=student_text, prof_ctx=prof_ctx)
        else:
            system_prompt = llm_service.build_system_prompt(
                subject=ctx.get("subject", "Physique"),
                language=self._prompt_language(),
                chapter_title=ctx.get("chapter_title", ""),
                lesson_title=ctx.get("lesson_title", ""),
                phase=self.current_phase,
                objective=ctx.get("objective", ""),
                scenario_context=ctx.get("scenario", ""),
                student_name=ctx.get("student_name", "l'étudiant"),
                proficiency=prof_ctx["proficiency"] if prof_ctx else ctx.get("proficiency", "intermédiaire"),
                struggles=prof_ctx["struggles"] if prof_ctx else ctx.get("struggles", "aucune identifiée"),
                mastered=prof_ctx["mastered"] if prof_ctx else ctx.get("mastered", "aucun"),
                teaching_mode=ctx.get("teaching_mode", "Socratique"),
                user_query=student_text,  # Pass user query for RAG context
                adaptation_hints=prof_ctx.get("adaptation_hints", "") if prof_ctx else "",
            )
        
        # ── INJECT CURRENT EXAM PANEL VIEW (anti-hallucination) ──
        # When the exam panel is open on the frontend, we attach the exact
        # exam/exercise/question the student is looking at. This prevents the
        # LLM from inventing a different year/session/exercise (e.g. saying
        # "Rattrapage 2025" while the UI shows "Rattrapage 2023").
        if self.current_exam_view:
            v = self.current_exam_view
            subject = str(v.get("subject", "") or "").strip()
            year = str(v.get("year", "") or "").strip()
            session = str(v.get("session", "") or "").strip()
            exam_title = str(v.get("exam_title", "") or "").strip()
            exercise_name = str(v.get("exercise_name", "") or "").strip()
            ex_idx = v.get("exercise_index")
            ex_total = v.get("exercise_total")
            q_num = v.get("question_number")
            q_total = v.get("question_total")
            q_content = str(v.get("question_content", "") or "").strip()
            q_correction = str(v.get("question_correction", "") or "").strip()
            q_points = v.get("question_points")

            session_label = session.capitalize() if session else ""
            header_bits = [b for b in [subject, session_label, year] if b]
            header = " — ".join(header_bits) if header_bits else (exam_title or "Examen")

            ex_ref = exercise_name or (f"Exercice {ex_idx + 1}" if isinstance(ex_idx, int) else "")
            if isinstance(ex_idx, int) and isinstance(ex_total, int) and ex_total > 1:
                ex_ref = f"{ex_ref} ({ex_idx + 1}/{ex_total})"

            q_ref = ""
            if q_num is not None:
                q_ref = f"Question {q_num}" + (f"/{q_total}" if q_total else "")
                if q_points is not None:
                    q_ref += f" ({q_points} pt)"

            exam_view_block = f"""
[CONTEXTE — EXAMEN ACTUELLEMENT AFFICHÉ À L'ÉTUDIANT]
⚠️ L'étudiant a CE PANNEAU D'EXAMEN ouvert en ce moment. Tu DOIS te baser EXCLUSIVEMENT sur ces informations. NE JAMAIS inventer une autre année, session, exercice ou question.

📚 Examen : {header}
📖 {ex_ref}
❓ {q_ref}

ÉNONCÉ EXACT DE LA QUESTION AFFICHÉE :
{q_content if q_content else '(non disponible)'}
"""
            if q_correction:
                exam_view_block += f"\nCORRECTION OFFICIELLE DE CETTE QUESTION :\n{q_correction}\n"
            exam_view_block += """
RÈGLES STRICTES :
- Si l'étudiant parle de "cette question", "la question N°X", "l'exercice", "l'examen", il parle TOUJOURS de CE qui est affiché ci-dessus.
- Tu cites l'année et la session EXACTES indiquées ci-dessus. JAMAIS d'autres.
- Tu ne mentionnes JAMAIS un examen/année différent à moins que l'étudiant ne te le demande explicitement.

🔄 BASCULE VERS UN AUTRE EXERCICE BAC :
- Si l'étudiant demande explicitement « un AUTRE exercice », « un nouvel exercice », « ferme et ouvre », « différent », « autre année », « autre session » (même thème ou thème différent), tu DOIS :
  1. Émettre IMMÉDIATEMENT un nouveau `<exam_exercise>mots-clés du thème demandé</exam_exercise>` afin que le SYSTÈME charge un VRAI exercice depuis la banque officielle BAC.
  2. NE PAS fabriquer un faux énoncé d'examen sur le tableau (`<ui>` whiteboard). NE JAMAIS inventer un titre comme « BAC National 2022 — Session Normale » avec un énoncé que tu rédigerais toi-même : seuls les exercices ouverts via `<exam_exercise>` sont des VRAIS exercices BAC.
  3. NE PAS citer une année/session précise dans ta phrase d'introduction — laisse le système choisir l'exercice et afficher les vraies métadonnées dans le panneau.
  4. Annonce simplement : « D'accord, je t'ouvre un autre exercice BAC sur [thème] » puis émets le tag.
- Si l'étudiant veut continuer sur l'exercice actuel, reste sur celui affiché ci-dessus.
"""
            system_prompt = (system_prompt or "") + "\n\n" + exam_view_block

        # Add exam correction instruction when student submits answer in exam panel
        if exam_context:
            question_ref = ""
            if exam_question_number is not None:
                total_str = f"/{exam_total_questions}" if exam_total_questions else ""
                question_ref = f" **QUESTION {exam_question_number}{total_str}**"

            exam_correction_instruction = f"""
[MODE CORRECTION D'EXAMEN — RÉPONSE SPÉCIFIQUE À LA{question_ref}]
⚠️ L'étudiant vient de soumettre sa réponse à la{question_ref} d'un exercice BAC.
CE N'EST PAS une conversation libre — c'est une RÉPONSE SPÉCIFIQUE À ÉVALUER.

TU DOIS OBLIGATOIREMENT:
1. COMMENCER par référencer la question: "Pour la **question {exam_question_number or 'posée'}**..."
2. ÉVALUER précisément la réponse (✅ correcte / ⚠️ partiellement / ❌ incorrecte)
3. COMPARER la réponse de l'étudiant à la correction officielle attendue
4. EXPLIQUER point par point les erreurs (s'il y en a)
5. DONNER la bonne méthode/approche avec rigueur
6. UTILISER le tableau blanc <board> avec les rubriques pédagogiques (définition, piège, à noter, astuce BAC)
7. ÊTRE ENCOURAGEANT et constructif
8. TERMINER en demandant si c'est clair ou s'il veut passer à la question suivante

❌ INTERDIT:
- Ne traite PAS cette réponse comme une conversation libre
- Ne propose PAS d'autres exercices (l'élève est déjà dans un examen)
- Ne change PAS de sujet
- N'ignore PAS le numéro de la question

✅ Ta correction doit être CIBLÉE sur la{question_ref} uniquement.
"""
            system_prompt += exam_correction_instruction

        # ── LESSON COMPLETION CLOSURE ──
        # When all objectives are done, instruct AI to conclude this lesson (not propose other subjects)
        if (self.session_mode == "coaching"
            and getattr(self, '_lesson_completed', False)):
            closure_instruction = f"""

[🎉 LEÇON TERMINÉE — MODE CLÔTURE]
⚠️ L'étudiant a complété TOUS les objectifs de cette leçon ({ctx.get('lesson_title','')}).
La session est en cours de CLÔTURE.

TU DOIS OBLIGATOIREMENT:
1. FÉLICITER chaleureusement l'étudiant pour avoir terminé la leçon
2. FAIRE un récapitulatif des points clés maîtrisés via <board> (rubrique "Bilan")
3. DONNER des conseils pour consolider (fiches, exercices BAC sur ce chapitre)
4. TERMINER par une phrase de clôture: "Tu peux maintenant fermer la session. Cette leçon est marquée comme terminée dans ton tableau de bord."

❌ STRICTEMENT INTERDIT:
- Ne propose PAS de passer à une autre matière
- Ne propose PAS un autre chapitre ou une autre leçon
- Ne pose PAS d'autres questions de contrôle
- Ne change PAS de sujet
- Ne relance PAS la discussion

✅ Reste centré sur la clôture de CETTE leçon uniquement.
"""
            system_prompt += closure_instruction

        decision = resource_decision_service.decide(
            phase=self.current_phase,
            student_text=student_text,
            lesson_title=ctx.get("lesson_title", ""),
            objective=ctx.get("objective", ""),
            proficiency=prof_ctx["proficiency"] if prof_ctx else ctx.get("proficiency", "intermédiaire"),
            available_resource_types=self._available_resource_types(),
            recent_modes=self.recent_resource_modes,
            simulation_active=bool(self.simulation_state.get("id")),
        )
        # If decision engine chose exam mode, also suppress whiteboard
        if decision.get("primary_mode") == "exam" or decision.get("resource_type_for_suggestion") == "exam":
            exam_sent = True
        preferred_resource_type = decision.get("preferred_resource_type")
        explicit_media_request = decision.get("explicit_media_request", False)
        needs_drawing = decision.get("should_prepare_whiteboard", False)
        max_tokens = decision.get("max_tokens", 800)  # Minimum 800 to avoid truncated JSON

        # Board/whiteboard triggers that need more tokens for JSON content
        board_triggers = ["démontr", "demonstr", "montre-moi", "écris", "ecris", "tableau",
                          "formule", "équation", "equation", "exercice", "corrig", "calcul",
                          "résou", "resou", "dérive", "derive", "intégr", "integr", "limit",
                          "dessine", "dessin", "schéma", "schema", "interpréta", "interpreta",
                          "punnet", "punnett", "échiquier", "echiquier", "croisement",
                          "cellule", "chromosome", "mitose", "méiose", "meiose",
                          "exemple", "donner", "donner moi", "montrer", "montre", "suite", "fonction",
                          "bac", "examen", "question bac", "entraîne", "entraine", "évaluation", "evaluation",
                          "teste", "tester", "national", "chrah", "fhem", "expliqu", "vas y", "continue"]

        # Both libre and coaching modes need enough tokens for JSON board content
        if self.session_mode in ("libre", "coaching"):
            max_tokens = max(max_tokens, 1200)
            if any(t in student_text.lower() for t in board_triggers):
                max_tokens = max(max_tokens, 2000)

        if needs_drawing or preferred_resource_type == "whiteboard":
            max_tokens = max(max_tokens, 2000)

        _safe_log(
            f"[Decision] primary={decision.get('primary_mode')} resource={decision.get('resource_type_for_suggestion')} "
            f"reason={decision.get('reason_code')} confidence={decision.get('confidence')} max_tokens={max_tokens}"
        )

        should_force_schema = needs_drawing or self.session_mode == "coaching"
        expected_structured_response = should_force_schema or preferred_resource_type in {"whiteboard", "image", "simulation", "exam"}

        # ── STREAMING RESPONSE (FAST UX) ──
        # Stream tokens to chat as they arrive, filter out tag content (board/draw/ui/schema)
        # so the user sees the pedagogical text immediately while the full response builds up.
        ai_response = ""
        try:
            _tag_names = ['board', 'draw', 'ui', 'schema', 'exam_exercise', 'suggestions']
            _safe_log(f"[LLM Stream] Starting streamed response (max_tokens={max_tokens})")
            async for token in llm_service.chat_stream(
                messages=self.conversation_history,
                system_prompt=system_prompt,
                max_tokens=max_tokens,
                session_type=self.session_mode or "coaching",
            ):
                ai_response += token
                # Detect if we're currently inside a tag block
                _inside_tag = False
                for tname in _tag_names:
                    if f'<{tname}>' in ai_response and f'</{tname}>' not in ai_response:
                        _inside_tag = True
                        break
                # Stream displayable tokens only when outside tag blocks
                if not _inside_tag:
                    clean = token
                    for tname in _tag_names:
                        clean = clean.replace(f'</{tname}>', '')
                    # Strip opening tag markers that might be in this token
                    for tname in _tag_names:
                        idx = clean.find(f'<{tname}>')
                        if idx >= 0:
                            clean = clean[:idx]
                    if clean:
                        await self.websocket.send_json({
                            "type": "ai_response_chunk",
                            "token": clean,
                        })
            await self.websocket.send_json({"type": "ai_response_done"})
            _safe_log(f"[LLM Stream] Completed ({len(ai_response)} chars)")
        except Exception as e:
            _safe_log(f"[LLM Stream] Error: {type(e).__name__}: {str(e)}")
            if not ai_response:
                ai_response = "Laisse-moi réfléchir un instant... Peux-tu reformuler ta question ?"
                await self._send_ai_response_text(ai_response)

        # Contextual quick-reply buttons aligned on what the AI just asked
        asyncio.create_task(self._extract_and_send_suggestions(ai_response))

        # Single TTS call on full text (non-blocking, reliable)
        asyncio.create_task(self.generate_and_send_audio_chunks(ai_response))

        # Add AI response to history
        self._append_history("assistant", ai_response)

        # ── Chat-based exercise detection: feed proficiency agent ──
        # Detect if the LLM was evaluating a student answer in conversation
        asyncio.create_task(self._detect_and_record_chat_answer(
            student_text, ai_response, prof_ctx
        ))

        media_already_sent = False
        resource_type_for_suggestion = decision.get("resource_type_for_suggestion")
        # Skip auto-suggest for exams - use exam panel system instead (exam_exercise WebSocket messages)
        if decision.get("auto_present_resource") and resource_type_for_suggestion and resource_type_for_suggestion != "exam":
            await self.websocket.send_json({"type": "hide_whiteboard"})
            await self._auto_suggest_resource(preferred_resource_type=resource_type_for_suggestion)
            media_already_sent = True

        # ── Execute UI commands (board/schema/draw/exam) ──
        # Text already streamed above, just process the commands.
        self._last_system_prompt = system_prompt
        await self._execute_ai_commands(
            ai_response,
            suppress_draw=not needs_drawing,
            suppress_media=media_already_sent,
            force_schema=should_force_schema,
            student_text=student_text,
            suppress_whiteboard=exam_sent,
            exam_context=exam_context,
            force_exam_panel=(decision.get("primary_mode") == "exam" or resource_type_for_suggestion == "exam"),
        )

    async def _tts_and_send(self, text: str, index: int):
        """Deprecated chunk-level entry — kept for backward compatibility."""
        _safe_log(f"[TTS] _tts_and_send deprecated, use generate_and_send_audio_chunks (chunk {index})")
        return

    async def generate_and_send_audio_chunks(self, ai_response: str):
        """
        Intelligent hybrid TTS pipeline.

        The AI response is split into sentence-level segments. Each segment
        is independently routed (Gemini for short/key Darija phrases, Google
        Cloud ar-XA / fr-FR for the rest) and synthesised in parallel.
        Audio is streamed back to the frontend as successive audio_chunk
        messages so the student starts hearing the first sentence while
        later ones are still being generated.

        No Web Speech API fallback — all audio is server-generated.
        """
        if not ai_response or not ai_response.strip():
            return

        lang = self._speech_language_for_tts()

        try:
            await self.websocket.send_json({"type": "processing", "stage": "tts"})
        except Exception:
            pass

        # Progressive streaming: each segment is launched in parallel server-side
        # and forwarded to the client as soon as it is ready, in reading order.
        any_sent = False
        try:
            async for i, total, seg in tts_service.stream_synthesize_segments(
                ai_response, language=lang
            ):
                try:
                    await self.websocket.send_json({
                        "type": "audio_chunk",
                        "chunk_index": i,
                        "total_chunks": total,
                        "audio": seg.audio_b64,
                        "format": seg.mime,
                        "provider": seg.provider,
                        "cached": seg.cached,
                        "language": seg.language,
                        "text": seg.text,
                    })
                    any_sent = True
                except Exception as e:
                    _safe_log(f"[TTS] Failed to send audio_chunk {i}/{total}: {e}")
                    return
        except Exception as e:
            _safe_log(f"[TTS] stream_synthesize_segments() failed: {e}")
            return

        if not any_sent:
            _safe_log("[TTS] No segments produced (empty or all failed)")

    def _speech_language_for_tts(self) -> str:
        """Map the session language to the TTS router input."""
        lang = getattr(self, "language", "fr") or "fr"
        if lang in ("fr", "ar", "mixed"):
            return lang
        return "fr"

    async def _init_session(self, message: dict):
        """Initialize session context from lesson data."""
        _safe_log(f"[Session Init] _init_session called with message keys: {list(message.keys())}")
        self.session_mode = message.get("mode", "coaching")
        _safe_log(f"[Session Init] Mode: {self.session_mode}")
        self.session_context = {
            "subject": message.get("subject", "Physique"),
            "chapter_title": message.get("chapter_title", ""),
            "lesson_title": message.get("lesson_title", ""),
            "objective": message.get("objective", ""),
            "scenario": message.get("scenario", ""),
            "student_name": message.get("student_name", "l'étudiant"),
            "proficiency": message.get("proficiency", "intermédiaire"),
            "struggles": message.get("struggles", ""),
            "mastered": message.get("mastered", ""),
            "teaching_mode": message.get("teaching_mode", "Socratique"),
        }
        self.current_phase = message.get("phase", "activation") if self.session_mode == "coaching" else "libre"
        self.language = message.get("language", "fr")
        self.conversation_history = []
        self.simulation_state = {}
        self.simulation_history = []
        self.simulation_orchestration = {}
        
        # Load lesson resources if lesson_id provided
        lesson_id = message.get("lesson_id")
        _safe_log(f"[Session Init] lesson_id received: {lesson_id}")
        
        # Track lesson progress for coaching mode
        self.lesson_progress = None
        self.lesson_objectives = message.get("learning_objectives", [])
        self.is_resumed_session = False
        
        if lesson_id:
            self.current_lesson_id = lesson_id
            await self._load_lesson_resources(lesson_id)
            
            # Load previous progress for this lesson (coaching mode memory)
            if self.session_mode == "coaching":
                try:
                    self.lesson_progress = await session_progress_service.get_resume_context(
                        student_id=self.student_id,
                        lesson_id=lesson_id
                    )
                    if self.lesson_progress and self.lesson_progress.get("has_previous_progress"):
                        self.is_resumed_session = True
                        # Restore completed objectives from database
                        self._completed_objective_indices = set(
                            self.lesson_progress.get("objectives_completed", [])
                        )
                        self._correct_answers_counter = 0  # Reset counter for new session
                        # Restore completion flag
                        self._lesson_completed = (
                            self.lesson_progress.get("status") == "completed"
                            or (self.lesson_objectives and
                                len(self._completed_objective_indices) >= len(self.lesson_objectives))
                        )
                        _safe_log(f"[Session Init] Resuming session: {self.lesson_progress.get('completion_percent', 0)}% complete, objectives completed: {self._completed_objective_indices}, lesson_completed={self._lesson_completed}")
                        
                        # Backfill: if lesson is completed but study_plan_session isn't marked, fix it now
                        if self._lesson_completed:
                            try:
                                from app.supabase_client import get_supabase_admin
                                from app.services.study_plan_service import study_plan_service
                                sb = get_supabase_admin()
                                lesson_row = sb.table("lessons").select("chapter_id").eq("id", lesson_id).execute()
                                if lesson_row.data:
                                    chapter_id = lesson_row.data[0].get("chapter_id")
                                    if chapter_id:
                                        sps_result = sb.table("study_plan_sessions").select("id, plan_id, status").eq(
                                            "chapter_id", chapter_id
                                        ).neq("status", "completed").order("scheduled_date").limit(1).execute()
                                        if sps_result.data:
                                            sps = sps_result.data[0]
                                            plan_row = sb.table("study_plans").select("student_id").eq("id", sps["plan_id"]).execute()
                                            if plan_row.data and plan_row.data[0]["student_id"] == self.student_id:
                                                await study_plan_service.mark_session_completed(
                                                    session_id=sps["id"],
                                                    student_id=self.student_id,
                                                )
                                                _safe_log(f"[Session Init][Backfill] ✅ Marked pending study_plan_session for already-completed lesson")
                            except Exception as bf_err:
                                _safe_log(f"[Session Init][Backfill] Error: {bf_err}")
                    else:
                        # Initialize new progress
                        self._completed_objective_indices = set()
                        self._correct_answers_counter = 0
                        self._lesson_completed = False
                        objectives_count = len(self.lesson_objectives) if self.lesson_objectives else 4
                        await session_progress_service.create_or_update_progress(
                            student_id=self.student_id,
                            lesson_id=lesson_id,
                            objectives_total=objectives_count,
                        )
                        _safe_log(f"[Session Init] New session started with {objectives_count} objectives")
                except Exception as e:
                    _safe_log(f"[Session Init] Progress load error (non-fatal): {e}")
                    
        elif self.session_mode in ("libre", "explain"):
            # Libre/Explain mode: load ALL available resources so AI can reference official curriculum
            _safe_log(f"[Session Init] {self.session_mode} mode - loading all available resources")
            await self._load_all_resources()
        else:
            _safe_log("[Session Init] WARNING: No lesson_id provided - resources won't be loaded")

        # Send session_initialized with progress info
        _safe_log(f"[Session Init] Sending session_initialized message to frontend")
        init_message = {
            "type": "session_initialized",
            "phase": self.current_phase,
            "context": self.session_context,
            "learning_objectives": self.lesson_objectives,
            "progress": self.lesson_progress if self.lesson_progress else {
                "is_new_session": True,
                "has_previous_progress": False,
                "objectives_completed": [],
                "objectives_total": len(self.lesson_objectives) if self.lesson_objectives else 4,
                "completion_percent": 0,
            },
            "is_resumed": self.is_resumed_session,
        }
        await self.websocket.send_json(init_message)
        _safe_log(f"[Session Init] session_initialized sent")

        # Stream opening message with tag filtering, single TTS at end
        _safe_log(f"[Session Init] Streaming opening message for phase: {self.current_phase}")
        opening = ""

        try:
            ctx = self.session_context
            # Fetch live proficiency for session opening
            _init_prof = None
            try:
                from app.services.student_proficiency_service import proficiency_service
                _init_prof = await proficiency_service.get_llm_context(self.student_id)
            except Exception:
                pass

            if self.session_mode in ("libre", "explain"):
                system_prompt = self._build_session_system_prompt(prof_ctx=_init_prof)
            else:
                system_prompt = llm_service.build_system_prompt(
                    subject=ctx.get("subject", "Physique"),
                    language=self._prompt_language(),
                    chapter_title=ctx.get("chapter_title", ""),
                    lesson_title=ctx.get("lesson_title", ""),
                    phase=self.current_phase,
                    objective=ctx.get("objective", ""),
                    scenario_context=ctx.get("scenario", ""),
                    student_name=ctx.get("student_name", "l'étudiant"),
                    proficiency=_init_prof["proficiency"] if _init_prof else ctx.get("proficiency", "intermédiaire"),
                    struggles=_init_prof["struggles"] if _init_prof else ctx.get("struggles", "aucune identifiée"),
                    mastered=_init_prof["mastered"] if _init_prof else ctx.get("mastered", "aucun"),
                    teaching_mode=ctx.get("teaching_mode", "Socratique"),
                    user_query=ctx.get("chapter_title", ""),  # Use chapter for initial RAG context
                    adaptation_hints=_init_prof.get("adaptation_hints", "") if _init_prof else "",
                )

            # Build opening prompt based on whether this is a resumed session
            if self.is_resumed_session and self.lesson_progress:
                # RESUMED SESSION: Start with recap + mini-diagnostic
                topics_covered = self.lesson_progress.get("topics_covered", [])
                key_points = self.lesson_progress.get("key_points_learned", [])
                last_summary = self.lesson_progress.get("last_ai_summary", "")
                completion = self.lesson_progress.get("completion_percent", 0)
                current_obj_idx = self.lesson_progress.get("current_objective_index", 0)
                
                _next_obj = self.lesson_objectives[current_obj_idx] if current_obj_idx < len(self.lesson_objectives) else 'Continuer'
                recap_context = f"""
L'élève REPREND cette leçon (déjà {completion}% complété).

SUJETS DÉJÀ COUVERTS: {', '.join(topics_covered) if topics_covered else 'Aucun enregistré'}
POINTS CLÉS APPRIS: {', '.join(key_points[:5]) if key_points else 'Non enregistrés'}
DERNIER RÉSUMÉ: {last_summary[:200] if last_summary else 'Pas de résumé'}
PROCHAIN OBJECTIF (index {current_obj_idx}): {_next_obj}

CONSIGNES POUR LA REPRISE:
1. Salue l'élève brièvement: "Content de te revoir !"
2. Fais un BREF rappel textuel (1-2 phrases) de ce qui a été vu la dernière fois.
3. Affiche IMMÉDIATEMENT un tableau <board> RICHE et STRUCTURÉ en rubriques pédagogiques (format obligatoire ci-dessous).
4. Pose UNE question rapide pour vérifier la mémoire (mini-diagnostic).
5. TERMINE par un bloc <suggestions> avec 3 boutons de réponse.

⚠️ STRUCTURE OBLIGATOIRE DU TABLEAU DE RAPPEL — utilise AU MOINS 4 rubriques différentes:

<board>{{"title":"📚 Rappel : {_next_obj}","lines":[
  {{"type":"subtitle","content":"📖 Définition","color":"blue"}},
  {{"type":"box","content":"[Définition précise du concept clé déjà vu]","color":"blue"}},
  {{"type":"subtitle","content":"🔑 Formule / Relation clé","color":"purple"}},
  {{"type":"math","content":"[Formule en LaTeX]"}},
  {{"type":"subtitle","content":"⚠️ Piège à éviter","color":"orange"}},
  {{"type":"note","content":"[Erreur fréquente que les élèves font sur ce point]","color":"orange"}},
  {{"type":"subtitle","content":"📝 À noter dans ton cahier","color":"green"}},
  {{"type":"box","content":"[2-3 points essentiels à retenir pour le BAC]","color":"green"}},
  {{"type":"subtitle","content":"💡 Astuce BAC","color":"purple"}},
  {{"type":"note","content":"[Conseil pratique ou type de question qui tombe]","color":"purple"}}
]}}</board>

RÈGLES STRICTES:
- Tu DOIS inclure AU MINIMUM 4 des 5 rubriques ci-dessus (Définition, Formule, Piège, À noter, Astuce BAC)
- NE te contente PAS de "Définition" + "Interprétation" seulement — c'est trop pauvre pour un rappel utile
- Remplace TOUS les [...] par du contenu réel tiré du programme BAC marocain
- Le rappel doit permettre à l'élève de RÉVISER SANS SON COURS — donne le maximum de valeur
"""
                opening_user_msg = recap_context
            else:
                # NEW SESSION: Standard opening prompts
                # For coaching/lesson phases, ALWAYS open with a structured lesson
                # plan grounded on the cadre de référence (what we will study).
                _lesson_topic = ctx.get('lesson_title') or ctx.get('chapter_title') or 'cette leçon'
                # Extract first name from student_name (registered full_name) for a personal greeting
                _full_name = (self.session_context.get("student_name") or "").strip()
                _first_name = _full_name.split()[0] if _full_name and _full_name != "l'étudiant" else "mon ami"

                lesson_plan_opening = f"""Ouvre la séance par un PLAN DE LEÇON clair pour : « {_lesson_topic} ».

⚠️ STRUCTURE OBLIGATOIRE — respecte-la SANS exception :

1) SALUTATION BRÈVE (1 phrase hors balise) qui commence par le prénom de l'élève « {_first_name} » et situe le sujet du jour (ex. : « Salut {_first_name} ! Aujourd'hui on va étudier ... »).

2) AFFICHE IMMÉDIATEMENT le plan de la leçon dans un tableau <ui>show_board</ui>.
   Le tableau DOIT contenir EXACTEMENT cette structure (pas les exemples génériques du template) :

<ui>{{"actions":[{{"type":"whiteboard","action":"show_board","payload":{{"title":"🎯 Plan de la leçon : {_lesson_topic}","lines":[
  {{"type":"subtitle","content":"📚 Ce que nous allons étudier aujourd'hui"}},
  {{"type":"step","label":"1","content":"[Titre du point 1 — tiré du cadre de référence] — 📝 À noter (type d'évaluation : QCM / calcul / raisonnement / schéma)"}},
  {{"type":"step","label":"2","content":"[Titre du point 2 — tiré du cadre de référence] — 📝 À noter / 💡 Culture (type d'évaluation)"}},
  {{"type":"step","label":"3","content":"[Titre du point 3 — tiré du cadre de référence] — 📝 À noter (type d'évaluation)"}},
  {{"type":"step","label":"4","content":"[Titre du point 4 — optionnel — tiré du cadre de référence]"}},
  {{"type":"separator","content":""}},
  {{"type":"tip","content":"Objectif final : [compétence mesurable à atteindre à la fin de la leçon]"}}
]}}}}]}}</ui>

   RÈGLES STRICTES POUR LE PLAN :
   - 3 à 5 étapes "step" numérotées, PAS MOINS. Une seule étape = REFUSÉ.
   - Chaque "content" commence par un TITRE DE POINT (ex. "Définition d'une transformation lente", "Facteurs cinétiques"), PAS par "Objectif :" ou "À noter".
   - Les titres viennent STRICTEMENT du programme officiel / [ÉLÉMENTS PRIORITAIRES DU CADRE DE RÉFÉRENCE] fourni dans ton contexte. N'INVENTE rien.
   - Indique pour chaque étape le marqueur 📝 À noter (examen) ou 💡 Culture (hors examen) ET le type d'évaluation attendu.
   - Ne mets PAS les subtitles "📝 À NOTER DANS TON CAHIER" ni "💡 Pense à ton quotidien" dans CE tableau d'ouverture — ces sections sont réservées aux tableaux d'explication qui viendront ensuite, point par point.

3) APRÈS le tableau (hors balises), pose UNE seule question d'accroche courte (1 phrase) pour démarrer l'étape 1 du plan.

4) TERMINE par un bloc <suggestions> contenant 3 boutons de réponse alignés sur ta question d'accroche (ex. deux réponses plausibles + "❓ Je ne sais pas").

5) N'avance pas dans l'explication du premier point tant que l'élève n'a pas répondu."""

                opening_prompt = {
                    "activation": lesson_plan_opening,
                    "exploration": lesson_plan_opening,
                    "explanation": lesson_plan_opening,
                    "application": f"Salue {_first_name} puis propose-lui le premier exercice d'application.",
                    "consolidation": f"Félicite {_first_name} par son prénom et résume les points clés de la leçon.",
                    "libre": (
                        f"Salue l'étudiant PAR SON PRÉNOM ({_first_name}) "
                        "et dis-lui qu'il peut poser n'importe quelle question sur les matières du BAC "
                        "(Math, Physique, Chimie, SVT). Sois bref, 1-2 phrases max, chaleureux et encourageant."
                    ),
                }
                opening_user_msg = opening_prompt.get(self.current_phase, lesson_plan_opening)

            # EXPLAIN MODE: inject exam question context into opening
            if self.session_mode == "explain":
                scenario_raw = ctx.get("scenario", "")
                try:
                    import json as _json
                    explain_data = _json.loads(scenario_raw) if scenario_raw else {}
                except Exception:
                    explain_data = {}
                q_content = explain_data.get("questionContent", "")
                q_type = explain_data.get("questionType", "open")
                q_points = explain_data.get("points", 0)
                q_parent = explain_data.get("parentContent", "")
                q_exercise_ctx = explain_data.get("exerciseContext", "")
                q_correction = explain_data.get("correction", "")
                has_answer = explain_data.get("hasAnswer", False)
                # Student artefacts (only present when hasAnswer=True)
                student_answer = (explain_data.get("studentAnswer") or "").strip()
                student_score = explain_data.get("studentScore")
                student_points_max = explain_data.get("studentPointsMax")
                evaluator_feedback = (explain_data.get("evaluatorFeedback") or "").strip()
                student_has_image = bool(explain_data.get("studentHasImage"))

                context_parts = [f"Question ({q_type}, {q_points} pts) : {q_content}"]
                if q_parent:
                    context_parts.append(f"Énoncé parent : {q_parent}")
                if q_exercise_ctx:
                    context_parts.append(f"Contexte de l'exercice : {q_exercise_ctx}")
                q_block = "\n".join(context_parts)

                if has_answer:
                    # ── MODE "APRÈS" — Diagnostique + correctif ──
                    # The AI MUST decorticate the student's specific answer:
                    # cite their phrases, point out missing elements, link to course.
                    score_line = ""
                    if student_score is not None and student_points_max:
                        score_line = f"Note obtenue par l'évaluateur automatique : {student_score}/{student_points_max}\n"

                    student_block = (
                        f"RÉPONSE DE L'ÉLÈVE (à analyser, citer textuellement) :\n«{student_answer}»\n"
                        if student_answer
                        else "L'élève n'a pas écrit de texte (peut-être uniquement un schéma/dessin).\n"
                    )
                    if student_has_image and not student_answer:
                        student_block += "Il a soumis une image (schéma ou photo de copie manuscrite).\n"

                    eval_block = ""
                    if evaluator_feedback:
                        eval_block = f"\nRetour de l'évaluateur automatique (référence interne, NE PAS le citer mot pour mot) :\n{evaluator_feedback}\n"

                    opening_user_msg = f"""L'élève a répondu à une question d'examen et veut comprendre EN PROFONDEUR ses points forts et ses erreurs.

{q_block}

{student_block}{score_line}
Correction officielle : {q_correction}{eval_block}

TU ES UN PROFESSEUR EXPÉRIMENTÉ qui corrige une copie. Ne fais PAS un cours générique — décortique la réponse spécifique de cet élève.

STRUCTURE OBLIGATOIRE (texte HORS des balises) :

1. **Salutation brève** — adresse-toi à l'élève comme un prof bienveillant.

2. **Ce qui fonctionne** ✅ — cite TEXTUELLEMENT entre guillemets une ou deux phrases JUSTES de l'élève et explique pourquoi c'est bon. Si rien n'est juste, dis-le honnêtement mais avec tact.

3. **Ce qui manque ou ce qui est imprécis** ⚠️❌ — pour chaque élément ATTENDU dans la correction officielle :
   - dis si l'élève l'a écrit (cite ses mots) ou pas
   - explique pourquoi c'est important pour la note BAC
   - si l'élève a écrit quelque chose de FAUX, cite la phrase et corrige-la AVEC son explication

4. **Comment rédiger pour avoir tous les points** — donne UNE version modèle ENTIÈREMENT RÉDIGÉE, telle qu'un correcteur BAC l'attend sur la copie d'un élève. Pas un copier-coller de la correction : reformule en utilisant le vocabulaire du cours.

   🚨 EXIGENCE DE RÉDACTION (style copie BAC SVT/PC) — la version modèle DOIT contenir des PHRASES COMPLÈTES avec connecteurs scientifiques, JAMAIS des mots-clés télégraphiques.
   - Comparaison : commence par « On remarque que… », « On constate que… », « On observe que… », « En comparant X et Y, on note que… ».
   - Déduction/conclusion : « On en déduit que… », « Ceci permet de conclure que… », « Par conséquent… », « Il en résulte que… ».
   - Observation/description : « D'après le document N°…, on observe que… », « Le document montre que… ».
   - Justification : « Cela s'explique par le fait que… », « En effet,… », « Car… ».
   - Chaque idée = une phrase complète sujet + verbe + complément. PAS de listes de mots-clés type « mitose, prophase, fuseau ».
   - Si la question demande une COMPARAISON, structure la rédaction en 2 temps : (a) « On remarque que [élément 1] présente … alors que [élément 2] présente … », (b) « On en déduit que … ».
   - Si la question demande d'EXPLIQUER un mécanisme, rédige un paragraphe enchaîné de 3 à 5 phrases, pas une liste à puces sans verbes.

   🧬 EXCEPTION GÉNÉTIQUE — si la question concerne un CROISEMENT (monohybridisme, dihybridisme, test-cross, gènes liés, carte factorielle, F1/F2, échiquier de fécondation) :
   - Ta rédaction texte reste OBLIGATOIRE (« On constate que… », « On en déduit que… »)
   - MAIS elle DOIT être ACCOMPAGNÉE d'un bloc `<ui>{{"actions":[{{"type":"whiteboard","action":"show_board","payload":{{...}}}}]}}</ui>` contenant l'interprétation chromosomique COMPLÈTE — Parents → Génotypes en `\\\\dfrac` → Gamètes → Échiquier de fécondation en `type=table` → Résultats — conformément au PROTOCOLE_GÉNÉTIQUE injecté en haut de ton contexte.
   - JAMAIS de notation ASCII inline type `DO//dø`, `dø/`, `D O / d o` — UNIQUEMENT du LaTeX `\\\\dfrac{{D}}{{d}}\\\\,\\\\dfrac{{O}}{{o}}` (échappement JSON `\\\\dfrac`) dans les cellules du tableau.
   - Le texte parlé décrit ; le tableau VISUALISE. Les deux sont REQUIS.

5. **Concept du cours à retenir** — relie les erreurs à un mécanisme/définition/loi précis. Pas de vague.

6. **Piège typique** — mentionne UN piège que beaucoup d'élèves font sur ce genre de question.

7. **Action suivante concrète** — UNE phrase : que doit-il refaire / réviser maintenant ?

8. **APRÈS** ton texte, mets dans `<board>...</board>` (ou `<ui>` show_board) un tableau comparatif "Ta réponse vs Réponse modèle".

   🚨 RÈGLE CRITIQUE — COMPLÉTUDE DU TABLEAU (ce point a été signalé défaillant) :
   - La colonne « Réponse modèle » du tableau DOIT contenir la RÉPONSE COMPLÈTE RÉDIGÉE — pas un résumé, pas des mots-clés, pas « voir ci-dessus », pas « cf. chat ».
   - Si ta version modèle du point 4 fait 5 phrases, la cellule « Réponse modèle » contient CES 5 PHRASES intégralement (ou réparties sur plusieurs lignes du tableau, une phrase par critère).
   - INTERDIT : cellule qui dit « Idem », « Voir rédaction », « Comme expliqué », « Mêmes éléments », ou qui ne contient qu'un fragment.
   - Si le tableau a 3 lignes (Observation / Déduction / Justification), chaque ligne contient la PHRASE RÉDIGÉE complète correspondante, pas un mot-clé.

   🚨 RÈGLE STYLE — chaque cellule « Réponse modèle » est une PHRASE COMPLÈTE avec connecteur scientifique :
   - ❌ MAUVAIS  : « mitose / prophase / fuseau »
   - ✅ BON     : « On observe que la cellule entre en prophase : les chromosomes se condensent et le fuseau mitotique se met en place. »
   - ❌ MAUVAIS  : « plus rapide / plus lent »
   - ✅ BON     : « On remarque que la réaction A est plus rapide que la réaction B car la concentration en ions H⁺ est plus élevée. »
   - ❌ MAUVAIS  : « Voir réponse modèle ci-dessus » / « Idem » / cellule vide
   - ✅ BON     : la phrase rédigée complète, même si elle apparaît aussi dans le texte chat
   Chaque ligne du tableau traite UN critère DIFFÉRENT — ne JAMAIS répéter le même élément de réponse dans plusieurs lignes.

RÈGLES :
- La RÉDACTION DU MODÈLE (point 4) prime sur la concision : 4 à 7 phrases bien construites pour la version modèle, pas des mots-clés.
- Le reste du texte (points 1-3, 5-7) reste CONCIS : 8 à 12 phrases max au total.
- Tu CITES toujours l'élève entre guillemets « … » avant de critiquer ou féliciter.
- Tu n'utilises PAS de jargon vague (« il faut bien », « c'est important ») — sois précis et technique.
- L'élève peut ensuite poser des questions de suivi."""
                else:
                    # ── MODE "AVANT" — Socratique strict ──
                    # The AI must guide WITHOUT revealing the answer.
                    opening_user_msg = f"""L'élève demande de l'aide AVANT de répondre. Ton rôle : un professeur socratique qui guide SANS jamais donner la réponse.

{q_block}

INTERDICTION ABSOLUE :
- Ne révèle JAMAIS la réponse, ni partiellement, ni en exemple, ni en reformulation.
- Ne dis pas « la réponse est… », ni « il faut répondre que… », ni « la bonne option est… ».
- Pour un QCM/Vrai-Faux/Association : ne désigne aucune lettre/option comme correcte.

STRUCTURE OBLIGATOIRE (texte HORS des balises) :

1. **Reformulation** — « En clair, on te demande de… » dans des mots simples.

2. **Le verbe-clé** — identifie le verbe-action de la consigne (décrire / justifier / comparer / démontrer / déduire / interpréter…) et explique en UNE phrase ce que ce verbe impose comme type de rédaction.

3. **Notions du cours à mobiliser** — liste 2 à 4 notions/définitions/lois/mécanismes nécessaires (sans les appliquer à la question).

4. **Plan vide à remplir** — propose un canevas en étapes numérotées (« Étape 1 : … / Étape 2 : … ») avec ce qu'il faut FAIRE à chaque étape, pas le contenu.

5. **Heuristique selon le type de question** :
   - QCM → comment éliminer les distracteurs (chercher le mot piège, comparer 2 options proches…)
   - Vrai/Faux → chercher un contre-exemple ou une exception
   - Association → identifier le critère discriminant qui distingue les éléments
   - Question ouverte → structure attendue (intro courte → développement → conclusion / déduction)

6. **Question socratique de relance** — termine par UNE question ouverte qui aide l'élève à démarrer (« Avant de te lancer, qu'est-ce que tu observes en premier dans le document ? » ou similaire adapté).

7. **APRÈS** ton texte, mets dans `<board>...</board>` un schéma de la MÉTHODE (étapes visuelles, mind-map des notions à mobiliser, ou tableau « ce que je sais / ce que je dois trouver »).

RÈGLES :
- Sois CONCIS : 6 à 10 phrases max au total dans le texte (hors board).
- Sois ENCOURAGEANT mais EXIGEANT — l'élève doit faire l'effort de chercher.
- Si l'élève insiste pour avoir la réponse, refuse poliment et propose un nouvel indice."""

            messages = [{"role": "user", "content": opening_user_msg}]

            # More tokens for resumed sessions; explain mode: concise but rich
            opening_max_tokens = 1200 if (self.is_resumed_session or self.session_mode == "explain") else 800

            # 🧬 Boost for genetics questions: a full dihybride explain
            # response includes a 4×4 crossing grid (16 cells, each with
            # a \dfrac + phenotype), plus parents / gametes / phenotype
            # sections, plus the pedagogical analysis of the student's
            # answer.  1200 tokens is NOT enough — the <ui> block gets
            # truncated mid-table and the student sees no board at all.
            if self.session_mode == "explain":
                genetics_blob = (opening_user_msg + " " +
                                 (self.session_context.get("examQuestion") or "") + " " +
                                 (self.session_context.get("examCorrection") or "")).lower()
                _GENETICS_HINTS = (
                    "croisement", "échiquier", "echiquier", "dihybrid",
                    "monohybrid", "genotype", "génotype", "gamète", "gamete",
                    "allèle", "allele", "f1 ", "f2 ", "mendel", "brassage",
                    "dominant", "récessif", "recessif", "hérédité", "heredite",
                )
                if any(h in genetics_blob for h in _GENETICS_HINTS):
                    opening_max_tokens = max(opening_max_tokens, 3500)
                    _safe_log(f"[Session Init] Genetics question detected — "
                              f"boosting opening max_tokens to {opening_max_tokens}")

            if self.session_mode == "explain":
                # STREAM explain opening — tokens appear on screen within 1-2 seconds
                opening = ""
                _inside_tag = False
                _tag_names = ['board', 'draw', 'ui', 'schema', 'exam_exercise', 'suggestions']
                _safe_log("[Session Init] Streaming explain opening via chat_stream")
                async for token in llm_service.chat_stream(
                    messages=messages,
                    system_prompt=system_prompt,
                    max_tokens=opening_max_tokens,
                    session_type="explain",
                ):
                    opening += token
                    # Track if we're inside a tag block — don't send tag content to chat
                    for tname in _tag_names:
                        if f'<{tname}>' in opening and f'</{tname}>' not in opening:
                            _inside_tag = True
                            break
                    else:
                        _inside_tag = False
                    # Send displayable tokens only when outside tags
                    if not _inside_tag:
                        clean = token
                        for tname in _tag_names:
                            clean = clean.replace(f'</{tname}>', '')
                        if clean:
                            await self.websocket.send_json({
                                "type": "ai_response_chunk",
                                "token": clean,
                            })
                await self.websocket.send_json({"type": "ai_response_done"})
            else:
                opening = await self._generate_validated_ai_response(
                    messages=messages,
                    system_prompt=system_prompt,
                    max_tokens=opening_max_tokens,
                    expected_structured=(self.session_mode == "coaching" or self.is_resumed_session),
                    context_label=f"opening_{self.session_mode}",
                )
                await self._send_ai_response_text(opening)

        except Exception as e:
            _safe_log(f"[Session Init] ERROR in streaming opening: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            if not opening:
                opening = "Bienvenue ! Commençons notre leçon."
                await self._send_ai_response_text(opening)

        if opening:
            self._append_history("assistant", opening)
            _safe_log(f"[Session Init] Opening streamed ({len(opening)} chars)")

            # Execute any AI commands (whiteboard, schemas, media, etc.) in the opening
            try:
                await self._execute_ai_commands(
                    opening,
                    force_schema=(self.session_mode in ("coaching", "explain")),
                )
            except Exception as cmd_err:
                _safe_log(f"[Session Init] Command execution error (non-fatal): {cmd_err}")

            # Single TTS on full text (non-blocking, reliable)
            asyncio.create_task(self.generate_and_send_audio_chunks(opening))

    async def _execute_ai_commands(self, ai_response: str, suppress_draw: bool = False, suppress_media: bool = False, force_schema: bool = False, student_text: str = "", suppress_whiteboard: bool = False, exam_context: bool = False, force_exam_panel: bool = False):
        """Detect and execute commands in AI response (media, phase transitions, exercises)."""
        
        _safe_log(f"[AI Commands] Checking AI response for commands... (force_schema={force_schema})")
        _safe_log(f"[AI Commands] Response preview: {ai_response[:200]}...")
        # PERF: build system_prompt lazily — it's only needed inside rare retry
        # branches (placeholder / malformed UI JSON). Eager build was causing a
        # duplicate RAG load on EVERY response (visible in logs as a second
        # "[LLM] RAG context loaded" line ≈ 0.5–1 s wasted per turn).
        _cached_system_prompt: list = [None]
        def _get_system_prompt() -> str:
            if _cached_system_prompt[0] is None:
                _cached_system_prompt[0] = self._build_session_system_prompt()
            return _cached_system_prompt[0]
        # Legacy variable kept for minimal diff: only resolves if .__call__ is used.
        class _LazyPrompt:
            def __str__(_self):
                return _get_system_prompt()
        system_prompt = _get_system_prompt  # callable — retries invoke system_prompt()
        
        # Debug: log the raw response around draw commands
        if '<draw>' in ai_response or '[draw]' in ai_response:
            draw_start = ai_response.find('<draw>') if '<draw>' in ai_response else ai_response.find('[draw]')
            if draw_start >= 0:
                _safe_log(f"[AI Commands] Raw draw tag found at position {draw_start}: {repr(ai_response[draw_start:draw_start+100])}")
        
        # Detect AI using placeholder markers instead of actual JSON content
        placeholder_markers = ['[tableau]', '[dessin]', '[schema]', '[board]', '[ui]']
        placeholder_detected = False
        for marker in placeholder_markers:
            if marker in ai_response.lower():
                _safe_log(f"[AI Commands] WARNING: AI used placeholder '{marker}' instead of actual JSON content!")
                placeholder_detected = True
        
        # Auto-correction: if placeholder detected, inject correction message and retry ONCE
        if placeholder_detected and not hasattr(self, '_placeholder_retry_count'):
            self._placeholder_retry_count = 0
        
        if placeholder_detected and self._placeholder_retry_count < 1:
            self._placeholder_retry_count += 1
            _safe_log(f"[AI Commands] Auto-correction: injecting reminder to generate actual JSON (retry {self._placeholder_retry_count}/1)")
            
            # Add AI's faulty response to history
            self.conversation_history.append({"role": "assistant", "content": ai_response})
            
            # Inject correction message
            correction_msg = "⚠️ ERREUR: Tu as utilisé un placeholder au lieu de générer le JSON complet. Tu DOIS générer le JSON complet maintenant. Pas de [ui], pas de [tableau], pas d'excuses - génère le <ui>{...}</ui> avec le payload complet immédiatement."
            self.conversation_history.append({"role": "user", "content": correction_msg})
            
            # Retry generation with higher token limit
            try:
                ai_response = ""
                async for token in llm_service.chat_stream(
                    messages=self.conversation_history,
                    system_prompt=getattr(self, '_last_system_prompt', ''),
                    max_tokens=2500,  # Extra tokens for retry
                ):
                    ai_response += token
                
                _safe_log(f"[AI Commands] Retry response preview: {ai_response[:200]}...")
                # Remove the correction exchange from history (keep only the corrected response)
                self.conversation_history = self.conversation_history[:-2]
            except Exception as e:
                _safe_log(f"[AI Commands] Retry failed: {e}")
                self._placeholder_retry_count = 0
        elif placeholder_detected:
            _safe_log(f"[AI Commands] Placeholder detected but retry limit reached")
            self._placeholder_retry_count = 0
        
        # NEW: Unified UI control block — prioritized over legacy tags when present.
        ui_blocks = re.findall(r'<ui>(.*?)</ui>', ai_response, re.DOTALL)
        if not ui_blocks:
            fallback_ui = re.search(r'<ui>(.*)', ai_response, re.DOTALL)
            if fallback_ui:
                ui_blocks = [fallback_ui.group(1)]

        if ui_blocks:
            def try_fix_ui_json(s):
                """Try to repair a truncated UI control JSON block."""
                # ── First pass: cleanup variants (fences, smart quotes,
                # trailing commas, bare LaTeX backslashes). This fixes the most
                # common LLM issue where \vec{AB}, \parallel, \frac are emitted
                # with single backslashes inside JSON strings.
                for variant in _json_cleanup_variants(s):
                    try:
                        return json.loads(variant)
                    except json.JSONDecodeError:
                        continue
                # Use the most-cleaned variant for downstream truncation repair
                s = _escape_bare_backslashes(
                    _remove_trailing_commas(
                        _normalize_smart_quotes(_strip_md_fence(s))
                    )
                )

                stripped = s.strip()
                if stripped:
                    first_brace = stripped.find('{')
                    last_brace = stripped.rfind('}')
                    if first_brace >= 0 and last_brace > first_brace:
                        try:
                            return json.loads(stripped[first_brace:last_brace + 1])
                        except json.JSONDecodeError:
                            pass

                # Extended suffix combinations for deeply nested structures
                suffixes = [
                    '}',
                    ']}',
                    '"}',
                    '"]}}',
                    '"}]}',
                    '"}]}}',
                    '"}}]}',
                    '"}]}]}',
                    '"}}]}}',
                    '"}]}]}}',
                    '"}}]}]}}',
                    '"}]}}]}}',
                ]
                for suffix in suffixes:
                    try:
                        return json.loads(s + suffix)
                    except json.JSONDecodeError:
                        continue

                # Keep only the JSON object from first { and close any missing quotes/brackets/braces.
                try:
                    start = s.find('{')
                    if start >= 0:
                        candidate = s[start:].strip()
                        if candidate.count('"') % 2 != 0:
                            candidate += '"'
                        open_brackets = candidate.count('[')
                        close_brackets = candidate.count(']')
                        open_braces = candidate.count('{')
                        close_braces = candidate.count('}')
                        candidate += ']' * max(0, open_brackets - close_brackets)
                        candidate += '}' * max(0, open_braces - close_braces)
                        return json.loads(candidate)
                except (json.JSONDecodeError, ValueError):
                    pass

                # Smart truncation: find last complete object
                try:
                    # Count opening/closing brackets and braces
                    open_braces = s.count('{')
                    close_braces = s.count('}')
                    open_brackets = s.count('[')
                    close_brackets = s.count(']')
                    open_quotes = s.count('"')
                    
                    # Build closing sequence
                    closing = ''
                    if open_quotes % 2 != 0:
                        closing += '"'
                    
                    # Close arrays first, then objects
                    closing += ']' * (open_brackets - close_brackets)
                    closing += '}' * (open_braces - close_braces)
                    
                    return json.loads(s + closing)
                except (json.JSONDecodeError, ValueError):
                    pass
                
                # Last resort: truncate to last valid brace
                try:
                    last_brace = s.rfind('}')
                    if last_brace > 0:
                        candidate = s[:last_brace + 1]
                        if candidate.count('"') % 2 != 0:
                            candidate += '"'
                        candidate += ']}'
                        return json.loads(candidate)
                except json.JSONDecodeError:
                    pass
                return None

            ui_actions = []

            for block_idx, ui_json_str in enumerate(ui_blocks):
                ui_json_str = str(ui_json_str).strip().replace('</ui>', '').strip()
                # Fix encoding issues (é -> �)
                if isinstance(ui_json_str, bytes):
                    ui_json_str = ui_json_str.decode('utf-8', errors='replace')
                _safe_log(f"[AI Commands] UI control block detected #{block_idx + 1}: {len(ui_json_str)} chars")
                ui_data = try_fix_ui_json(ui_json_str)

                if not isinstance(ui_data, dict):
                    diag = ""
                    try:
                        json.loads(_strip_md_fence(ui_json_str))
                    except json.JSONDecodeError as e:
                        pos = getattr(e, "pos", 0) or 0
                        start = max(0, pos - 60)
                        end = min(len(ui_json_str), pos + 60)
                        diag = f" | err={e.msg} at pos={pos} ctx=…{ui_json_str[start:end]!r}…"
                    _safe_log(
                        f"[AI Commands][ERROR] Failed to parse UI control JSON "
                        f"block #{block_idx + 1}.{diag} Preview: {ui_json_str[:200]}"
                    )
                    # Last resort: try to extract board content via regex
                    title_match = re.search(r'"title"\s*:\s*"([^"]*)"', ui_json_str)
                    
                    # Try to extract mindmap nodes (mindmapNodes or nodes with level/parent)
                    is_mindmap = '"mindmap"' in ui_json_str or '"mindmapNodes"' in ui_json_str
                    nodes_key = "mindmapNodes" if '"mindmapNodes"' in ui_json_str else "nodes"
                    nodes_match = re.search(rf'"{nodes_key}"\s*:\s*\[', ui_json_str, re.DOTALL)
                    
                    if nodes_match and '"id"' in ui_json_str:
                        # Extract individual node objects with all fields
                        nodes = []
                        node_pattern = r'\{[^{}]*"id"\s*:\s*"([^"]*)"[^{}]*"label"\s*:\s*"([^"]*)"[^{}]*\}'
                        for nm in re.finditer(node_pattern, ui_json_str):
                            node_str = nm.group(0)
                            node_id = nm.group(1)
                            node_label = nm.group(2).strip()
                            # Clean label
                            node_label = re.sub(r'^[-•·]\s*', '', node_label)
                            if len(node_label) > 40:
                                node_label = node_label[:37] + "..."
                            
                            # Extract level
                            level_m = re.search(r'"level"\s*:\s*(\d+)', node_str)
                            level = int(level_m.group(1)) if level_m else 1
                            
                            # Extract parent
                            parent_m = re.search(r'"parent"\s*:\s*"([^"]*)"', node_str)
                            parent = parent_m.group(1) if parent_m else None
                            
                            node = {"id": node_id, "label": node_label, "level": level}
                            if parent:
                                node["parent"] = parent
                            nodes.append(node)
                        
                        if nodes:
                            diagram_title = title_match.group(1) if title_match else "Carte Mentale"
                            
                            # Determine center node
                            center_m = re.search(r'"centerNode"\s*:\s*"([^"]*)"', ui_json_str)
                            center_node = center_m.group(1) if center_m else ""
                            if not center_node:
                                for cn in nodes:
                                    if cn.get("level") == 0:
                                        center_node = cn["id"]
                                        break
                                if not center_node:
                                    center_node = nodes[0]["id"]
                            
                            if is_mindmap or any(n.get("level", 1) == 0 for n in nodes):
                                # Build as mindmap type
                                _safe_log(f"[AI Commands] Regex fallback: extracted mindmap with {len(nodes)} nodes, center={center_node}")
                                lines = [{
                                    "type": "mindmap",
                                    "content": diagram_title,
                                    "centerNode": center_node,
                                    "mindmapNodes": nodes,
                                }]
                            else:
                                # Build as diagram type
                                _safe_log(f"[AI Commands] Regex fallback: extracted diagram with {len(nodes)} nodes")
                                lines = [
                                    {"type": "title", "content": diagram_title},
                                    {"type": "diagram", "content": "", "nodes": nodes, "edges": []}
                                ]
                            
                            ui_actions.append({
                                "type": "whiteboard",
                                "action": "show_board",
                                "payload": {"title": diagram_title, "lines": lines}
                            })
                            continue
                    
                    # Fallback to text extraction
                    content_matches = re.findall(r'"content"\s*:\s*"([^"]*)"', ui_json_str)
                    if title_match and content_matches:
                        _safe_log(f"[AI Commands] Regex fallback: extracted title + {len(content_matches)} content items")
                        lines = [{"type": "title", "content": title_match.group(1)}]
                        for c in content_matches[:10]:
                            lines.append({"type": "text", "content": c})
                        ui_actions.append({
                            "type": "whiteboard",
                            "action": "show_board",
                            "payload": {"title": title_match.group(1), "lines": lines}
                        })
                    continue

                actions = ui_data.get("actions", [])
                if isinstance(actions, dict):
                    actions = [actions]
                elif isinstance(actions, list):
                    actions = actions
                else:
                    actions = [ui_data] if ui_data.get("type") else []

                if not actions and ui_data.get("type"):
                    actions = [ui_data]

                if not actions:
                    _safe_log(f"[AI Commands][WARN] UI block #{block_idx + 1} produced no executable actions. Keys={list(ui_data.keys())}")

                ui_actions.extend([action for action in actions if isinstance(action, dict)])

            _safe_log(f"[AI Commands] UI actions parsed: {len(ui_actions)}")
            if not ui_actions and ui_blocks:
                _safe_log("[AI Commands][WARN] UI control block(s) were present but no valid actions were extracted")
                # Trigger retry if force_schema is True and we have malformed UI blocks
                if force_schema:
                    retry_count = getattr(self, '_ui_parse_retry_count', 0)
                    if retry_count < 2:
                        self._ui_parse_retry_count = retry_count + 1
                        _safe_log(f"[AI Commands] UI parse failed, triggering retry ({self._ui_parse_retry_count}/2)")
                        retry_messages = list(self.conversation_history)
                        retry_messages.append({"role": "assistant", "content": self._sanitize_history_content(ai_response)})
                        retry_messages.append({
                            "role": "user",
                            "content": (
                                "ERREUR JSON CRITIQUE: Le bloc <ui> est malformé ou tronqué. "
                                "Génère un nouveau bloc <ui> COMPLET avec la STRUCTURE CORRECTE:\n"
                                '<ui>{"actions":[{"type":"whiteboard","action":"show_board","payload":{"title":"Titre","lines":[{"type":"title","content":"..."},{"type":"text","content":"..."}]}}]}</ui>\n'
                                "RÈGLES ESSENTIELLES:\n"
                                '1. "lines" doit être un TABLEAU d\'OBJETS: [{"type":"...", "content":"..."}]\n'
                                '2. Chaque ligne DOIT avoir "type" (title/text/math/step/box) ET "content"\n'
                                "3. NE METS JAMAIS de texte brut dans lines - uniquement des objets JSON\n"
                                "4. Tous les guillemets et accolades doivent être fermés correctement"
                            )
                        })
                        try:
                            retried_response = ""
                            async for token in llm_service.chat_stream(
                                messages=retry_messages,
                                system_prompt=getattr(self, '_last_system_prompt', ''),
                                max_tokens=2400,
                            ):
                                retried_response += token
                            _safe_log(f"[AI Commands] UI parse retry response: {retried_response[:200]}...")
                            self._ui_parse_retry_count = 0
                            await self._execute_ai_commands(
                                retried_response,
                                suppress_draw=suppress_draw,
                                suppress_media=suppress_media,
                                force_schema=True,
                                student_text=student_text,
                                suppress_whiteboard=suppress_whiteboard,
                                exam_context=exam_context,
                                force_exam_panel=force_exam_panel,
                            )
                            return
                        except Exception as e:
                            _safe_log(f"[AI Commands] UI parse retry failed: {e}")
                            self._ui_parse_retry_count = 0
            ui_actions_handled = False

            # Collect all board payloads to merge them into one combined board
            # This prevents multiple show_board actions from replacing each other
            collected_board_payloads = []

            def normalize_board_payload(payload):
                def sanitize_board_text(value, *, inline_math=True):
                    if not isinstance(value, str):
                        return value
                    cleaned = value.strip()
                    cleaned = re.sub(r'\*\*(.+?)\*\*', r'\1', cleaned)
                    cleaned = re.sub(r'__(.+?)__', r'\1', cleaned)
                    cleaned = re.sub(r'`(.+?)`', r'\1', cleaned)
                    cleaned = re.sub(r'\\\((.+?)\\\)', r'$\1$', cleaned)
                    if not inline_math:
                        cleaned = re.sub(r'\$(.+?)\$', r'\1', cleaned)
                    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
                    return cleaned

                if not isinstance(payload, dict):
                    return None
                lines = payload.get("lines", [])
                if not isinstance(lines, list) or not lines:
                    return None
                normalized_lines = []
                for line in lines:
                    if not isinstance(line, dict):
                        continue
                    normalized = dict(line)
                    if "content" not in normalized and "text" in normalized:
                        normalized["content"] = normalized.pop("text")
                    elif "content" not in normalized:
                        normalized["content"] = ""
                    line_type = str(normalized.get("type", "text")).lower().strip()
                    normalized["content"] = sanitize_board_text(
                        normalized.get("content", ""),
                        inline_math=line_type not in {"title", "subtitle"},
                    )
                    if isinstance(normalized.get("label"), str):
                        normalized["label"] = sanitize_board_text(normalized["label"], inline_math=False)
                    if line_type == "table":
                        if isinstance(normalized.get("headers"), list):
                            normalized["headers"] = [sanitize_board_text(h, inline_math=True) for h in normalized["headers"]]
                        if isinstance(normalized.get("rows"), list):
                            normalized_rows = []
                            for row in normalized["rows"]:
                                if isinstance(row, list):
                                    normalized_rows.append([sanitize_board_text(cell, inline_math=True) for cell in row])
                                else:
                                    normalized_rows.append(row)
                            normalized["rows"] = normalized_rows
                    # Normalize mindmap lines — ensure mindmapNodes and centerNode are present
                    if line_type == "mindmap":
                        nodes = normalized.get("mindmapNodes") or normalized.get("nodes") or []
                        center = normalized.get("centerNode") or normalized.get("center_node") or ""
                        if isinstance(nodes, list) and nodes:
                            cleaned_nodes = []
                            for n in nodes:
                                if not isinstance(n, dict):
                                    continue
                                label = str(n.get("label", "")).strip()
                                # Clean label: remove bullet prefixes, limit length
                                label = re.sub(r'^[-•·]\s*', '', label)
                                if len(label) > 40:
                                    label = label[:37] + "..."
                                cleaned_nodes.append({
                                    "id": str(n.get("id", f"n{len(cleaned_nodes)}")),
                                    "label": label,
                                    "level": int(n.get("level", 1)) if str(n.get("level", "")).isdigit() or isinstance(n.get("level"), int) else 1,
                                    **({"parent": str(n["parent"])} if n.get("parent") else {}),
                                    **({"color": str(n["color"])} if n.get("color") else {}),
                                })
                            if cleaned_nodes:
                                normalized["mindmapNodes"] = cleaned_nodes
                                # Auto-detect center node if not specified
                                if not center:
                                    for cn in cleaned_nodes:
                                        if cn.get("level") == 0:
                                            center = cn["id"]
                                            break
                                    if not center:
                                        center = cleaned_nodes[0]["id"]
                                normalized["centerNode"] = center
                                _safe_log(f"[AI Commands] Mindmap normalized: {len(cleaned_nodes)} nodes, center={center}")
                        else:
                            _safe_log(f"[AI Commands][WARN] Mindmap line has no valid nodes")
                    normalized_lines.append(normalized)
                if not normalized_lines:
                    return None
                return {
                    "title": sanitize_board_text(payload.get("title", "Tableau"), inline_math=False),
                    "lines": normalized_lines,
                }

            def normalize_draw_steps(payload):
                if isinstance(payload, dict):
                    steps = payload.get("steps")
                    title = payload.get("title", "Schema")
                elif isinstance(payload, list):
                    steps = payload
                    title = "Schema"
                else:
                    steps = None
                    title = "Schema"

                if not isinstance(steps, list) or not steps:
                    return None, None

                # Ensure each step has an 'elements' array as expected by the frontend
                normalized = []
                for step in steps:
                    if not isinstance(step, dict):
                        continue
                    # Already has elements array — keep as-is
                    if isinstance(step.get("elements"), list) and step["elements"]:
                        normalized.append(step)
                        continue
                    # Convert non-standard step formats to {elements, title, clear}
                    elements = []
                    step_title = step.get("title", "")
                    # If step has 'lines' (board-like format inside draw), convert each line to a text element
                    if isinstance(step.get("lines"), list):
                        y = 30
                        for line in step["lines"]:
                            if isinstance(line, dict):
                                text = line.get("content") or line.get("text") or ""
                                line_type = line.get("type", "text")
                                font_size = 18 if line_type in ("title", "subtitle") else 14
                                color = "#FFD700" if line_type == "title" else "#FFFFFF"
                                elements.append({
                                    "id": f"l{y}",
                                    "type": "text",
                                    "x": 20,
                                    "y": y,
                                    "text": text,
                                    "color": color,
                                    "strokeWidth": 1,
                                    "fontSize": font_size,
                                })
                                y += font_size + 8
                            elif isinstance(line, str):
                                elements.append({
                                    "id": f"l{y}",
                                    "type": "text",
                                    "x": 20,
                                    "y": y,
                                    "text": line,
                                    "color": "#FFFFFF",
                                    "strokeWidth": 1,
                                    "fontSize": 14,
                                })
                                y += 22
                    # If step has other drawable data (points, shapes, etc.)
                    elif isinstance(step.get("points"), list) or step.get("type") in ("line", "arrow", "rect", "circle", "text", "path"):
                        elements.append({**step, "id": step.get("id", "e0"), "color": step.get("color", "#FFFFFF"), "strokeWidth": step.get("strokeWidth", 2)})

                    if elements:
                        normalized.append({
                            "elements": elements,
                            "title": step_title,
                            "clear": step.get("clear", False),
                            "narration": step.get("narration", ""),
                        })

                if not normalized:
                    return None, None
                return title, normalized

            for idx, action in enumerate(ui_actions):
                if not isinstance(action, dict):
                    _safe_log(f"[AI Commands] Skipping invalid UI action at index {idx}: {action!r}")
                    continue

                action_type = str(action.get("type", "")).lower().strip()
                action_name = str(action.get("action", "")).lower().strip()
                payload = action.get("payload") if isinstance(action.get("payload"), (dict, list)) else action
                _safe_log(f"[AI Commands] UI action {idx}: type={action_type} action={action_name}")

                if action_type == "whiteboard":
                    # Allow whiteboard UI action when correcting exam answer (exam_context=True)
                    if suppress_whiteboard and not exam_context:
                        _safe_log(f"[AI Commands] Whiteboard UI action '{action_name}' suppressed — exam mode active (flow continues to exam fallback)")
                        # Do NOT mark as handled — flow must continue to exam_exercise detection
                        continue
                    if action_name in {"show_schema", "schema", "open_schema"}:
                        schema_id = action.get("schema_id") or (payload.get("schema_id") if isinstance(payload, dict) else None)
                        if schema_id:
                            await self.websocket.send_json({"type": "hide_exercise"})
                            await self.websocket.send_json({"type": "hide_media"})
                            await self.websocket.send_json({"type": "clear_whiteboard"})
                            await self.websocket.send_json({
                                "type": "whiteboard_schema",
                                "schema_id": schema_id,
                            })
                            self._remember_mode("whiteboard")
                            ui_actions_handled = True
                        else:
                            _safe_log(f"[AI Commands][WARN] whiteboard schema action missing schema_id. action={action!r}")
                    elif action_name in {"show_board", "board"}:
                        board_source = action.get("payload") if isinstance(action.get("payload"), dict) else action.get("board")
                        if not isinstance(board_source, dict):
                            board_source = action
                        board_payload = normalize_board_payload(board_source)
                        if board_payload:
                            collected_board_payloads.append(board_payload)
                            ui_actions_handled = True
                        else:
                            _safe_log(f"[AI Commands][WARN] whiteboard board action had no valid lines/title payload. action={action!r}")
                    elif action_name in {"show_draw", "draw"}:
                        draw_source = action.get("payload") if isinstance(action.get("payload"), (dict, list)) else action.get("draw")
                        if not isinstance(draw_source, (dict, list)):
                            draw_source = action
                        draw_title, draw_steps = normalize_draw_steps(draw_source)
                        if draw_steps:
                            await self.websocket.send_json({"type": "hide_exercise"})
                            await self.websocket.send_json({"type": "hide_media"})
                            await self.websocket.send_json({"type": "clear_whiteboard"})
                            await self.websocket.send_json({
                                "type": "whiteboard_draw",
                                "title": draw_title,
                                "steps": draw_steps,
                            })
                            self._remember_mode("whiteboard")
                            ui_actions_handled = True
                        else:
                            _safe_log(f"[AI Commands][WARN] whiteboard draw action had no valid steps. action={action!r}")
                    elif action_name in {"clear", "reset"}:
                        await self.websocket.send_json({"type": "clear_whiteboard"})
                        ui_actions_handled = True
                    elif action_name in {"close", "hide"}:
                        await self.websocket.send_json({"type": "hide_whiteboard"})
                        ui_actions_handled = True

                elif action_type == "media":
                    if action_name in {"open", "show"}:
                        resource_source = action.get("payload") if isinstance(action.get("payload"), dict) else action
                        resource_type = str(resource_source.get("resource_type", resource_source.get("resource", "image"))).lower().strip()
                        if not resource_type:
                            _safe_log(f"[AI Commands][WARN] media action missing resource_type, defaulting to image. action={action!r}")
                        await self.websocket.send_json({"type": "hide_exercise"})
                        await self.websocket.send_json({"type": "hide_whiteboard"})
                        if resource_type == "simulation":
                            await self._auto_suggest_resource(preferred_resource_type="simulation")
                        else:
                            await self._auto_suggest_resource(preferred_resource_type="image")
                        ui_actions_handled = True
                    elif action_name in {"close", "hide"}:
                        await self.websocket.send_json({"type": "hide_media"})
                        ui_actions_handled = True

                elif action_type == "exercise":
                    if action_name in {"open", "show"}:
                        await self.websocket.send_json({"type": "hide_whiteboard"})
                        await self.websocket.send_json({"type": "hide_media"})
                        await self._auto_suggest_exercise()
                        ui_actions_handled = True
                    elif action_name in {"close", "hide"}:
                        await self.websocket.send_json({"type": "hide_exercise"})
                        ui_actions_handled = True

                elif action_type == "session":
                    if action_name in {"close_all", "close_everything"}:
                        _safe_log("[AI Commands] session close_all received — hiding all resource panels")
                        await self.websocket.send_json({"type": "hide_whiteboard"})
                        await self.websocket.send_json({"type": "hide_media"})
                        await self.websocket.send_json({"type": "hide_exercise"})
                        ui_actions_handled = True
                    elif action_name in {"next_phase", "advance_phase"}:
                        # Close exam panel and other resources before advancing
                        await self.websocket.send_json({"type": "hide_exam_panel"})
                        await self.websocket.send_json({"type": "hide_exercise"})
                        await self._auto_advance_phase()
                        ui_actions_handled = True

            # ── Merge and send all collected board payloads as ONE combined board ──
            if collected_board_payloads:
                merged_title = collected_board_payloads[0]["title"]
                merged_lines = []
                for bp_idx, bp in enumerate(collected_board_payloads):
                    if bp_idx > 0 and bp.get("title") and bp["title"] != merged_title:
                        # Add a separator + subtitle for subsequent boards
                        merged_lines.append({"type": "separator", "content": ""})
                        merged_lines.append({"type": "subtitle", "content": bp["title"]})
                    merged_lines.extend(bp["lines"])
                _safe_log(f"[AI Commands] Merged {len(collected_board_payloads)} board payloads into one ({len(merged_lines)} total lines)")
                # Defense in depth: rewrite any residual ASCII genetics
                # notation (``DO//dø``, ``dø/``) to LaTeX ``\dfrac`` before
                # the board lands on the student's screen.
                merged_lines = _sanitize_genetics_cells(merged_lines)
                await self.websocket.send_json({"type": "hide_exercise"})
                await self.websocket.send_json({"type": "hide_media"})
                await self.websocket.send_json({"type": "clear_whiteboard"})
                await self.websocket.send_json({
                    "type": "whiteboard_board",
                    "title": merged_title,
                    "lines": merged_lines,
                })
                self._remember_mode("whiteboard")

            if ui_actions_handled:
                # ── ALWAYS run exam exercise detection even when UI actions
                # were handled.  The AI often emits BOTH a <ui> block (for
                # whiteboard/media) AND an <exam_exercise> tag.  Without
                # this, the early `return` would skip exam detection and
                # leave a stale Chemistry panel visible when the student
                # asked for SVT / Maths / etc.
                exam_ex_match_early = re.search(
                    r'<exam_exercise>(.*?)</exam_exercise>', ai_response, re.DOTALL
                )
                if exam_ex_match_early or (force_exam_panel and not exam_context):
                    _safe_log("[AI Commands] UI actions handled but exam detection still pending — continuing to exam block")
                else:
                    return

        # Support both <draw> and [draw] formats
        draw_data_match = re.search(r'<draw>\s*(\[.*?\])\s*</draw>', ai_response, re.DOTALL)
        if not draw_data_match:
            draw_data_match = re.search(r'<draw>\s*(\[.*)', ai_response, re.DOTALL)
        if not draw_data_match:
            # Support [draw] format (square brackets)
            draw_data_match = re.search(r'\[draw\]\s*(\[.*?\])', ai_response, re.DOTALL)
        if not draw_data_match:
            draw_data_match = re.search(r'\[draw\]\s*(\[.*)', ai_response, re.DOTALL)
        
        lower_response = ai_response.lower()
        
        # ══════════════════════════════════════════════════════════════════════════
        # 0. CLEAR command — must run FIRST before any display commands
        # ══════════════════════════════════════════════════════════════════════════
        if "EFFACER_TABLEAU" in ai_response or "RESET_TABLEAU" in ai_response:
            _safe_log("[AI Commands] EFFACER_TABLEAU/RESET_TABLEAU detected — clearing whiteboard BEFORE new content")
            await self.websocket.send_json({"type": "clear_whiteboard"})

        # ══════════════════════════════════════════════════════════════════════════
        # 1. CONTENT DISPLAY COMMANDS (board, schema, draw)
        # ══════════════════════════════════════════════════════════════════════════
        
        # ── 1a. BOARD detection — structured math/text content for whiteboard ──
        # Suppress whiteboard only if exam exercises were sent AND it's not a correction context
        # When exam_context=True, we're correcting an answer, so allow whiteboard for explanation
        should_suppress_board = suppress_whiteboard and not exam_context
        if should_suppress_board:
            _safe_log("[AI Commands] Whiteboard suppressed — exam exercises active, skipping board/schema/draw")
        
        board_match = re.search(r'<board>(.*?)</board>', ai_response, re.DOTALL)
        if not board_match:
            board_match = re.search(r'<board>(.*)', ai_response, re.DOTALL)
        board_handled = False
        if board_match and not should_suppress_board:
            board_json_str = board_match.group(1).strip().replace('</board>', '').strip()
            _safe_log(f"[AI Commands] Raw board JSON length: {len(board_json_str)} chars")
            
            def try_fix_board_json(s):
                """
                Try several repair strategies on LLM-generated board JSON.
                Uses shared module-level helpers (see _json_cleanup_variants).
                """
                # 1-3. cleanup variants: raw, quotes/commas, LaTeX backslashes
                last_variant = s
                for variant in _json_cleanup_variants(s):
                    last_variant = variant
                    try:
                        return json.loads(variant)
                    except json.JSONDecodeError:
                        continue

                # 4. truncation repair on the most-cleaned variant
                base = last_variant
                for suffix in (']}', '"}]}', '"}}]}', '"]}}', '"}]}}', '}]}', '}'):
                    try:
                        return json.loads(base + suffix)
                    except json.JSONDecodeError:
                        continue
                # Cut at last `}` then close
                last_brace = base.rfind("}")
                if last_brace > 0:
                    candidate = base[: last_brace + 1]
                    if candidate.count('"') % 2 != 0:
                        candidate += '"'
                    for suffix in (']}', '}]}', ''):
                        try:
                            return json.loads(candidate + suffix)
                        except json.JSONDecodeError:
                            continue
                return None
            
            board_data = try_fix_board_json(board_json_str)
            if board_data and isinstance(board_data, dict) and board_data.get("lines"):
                # Normalize lines: AI may use "text" field but frontend expects "content"
                normalized_lines = []
                for line in board_data["lines"]:
                    if isinstance(line, dict):
                        normalized = dict(line)
                        # Map "text" → "content" if "content" is missing
                        if "content" not in normalized and "text" in normalized:
                            normalized["content"] = normalized.pop("text")
                        elif "content" not in normalized:
                            normalized["content"] = ""
                        
                        # Validate and fix table rows: must be array of arrays
                        if normalized.get("type") == "table" and "rows" in normalized:
                            rows = normalized["rows"]
                            if not isinstance(rows, list):
                                # Convert single row to array of rows
                                rows = [rows]
                            
                            MAX_CELL_LEN = 80  # Guard: cells should be keywords, not paragraphs
                            
                            def _clean_cell(c):
                                s = str(c) if c is not None else ""
                                # Truncate if a long paragraph sneaked into a cell
                                if len(s) > MAX_CELL_LEN:
                                    s = s[:MAX_CELL_LEN].rstrip() + "…"
                                return s
                            
                            # Ensure each row is an array
                            fixed_rows = []
                            for row in rows:
                                if isinstance(row, list):
                                    fixed_rows.append([_clean_cell(cell) for cell in row])
                                elif isinstance(row, dict):
                                    fixed_rows.append([_clean_cell(v) for v in row.values()])
                                else:
                                    fixed_rows.append([_clean_cell(row)])
                            normalized["rows"] = fixed_rows
                        
                        # Guard: generic text lines shouldn't contain the entire discussion
                        # (prevent LLM from dumping paragraphs into board content)
                        if normalized.get("type") in ("text", "title", "subtitle", "box", "note", "warning", "tip", "step"):
                            content = normalized.get("content", "")
                            if isinstance(content, str) and len(content) > 400:
                                normalized["content"] = content[:400].rstrip() + "…"
                        
                        normalized_lines.append(normalized)
                
                _safe_log(f"[AI Commands] Board content detected: {board_data.get('title', 'Tableau')} ({len(normalized_lines)} lines)")
                for i, line in enumerate(normalized_lines[:3]):
                    _safe_log(f"[AI Commands]   Line {i}: type={line.get('type')} content={repr(line.get('content', '')[:80])}")

                # Defense in depth: rewrite ASCII genetics (DO//dø) to \dfrac.
                normalized_lines = _sanitize_genetics_cells(normalized_lines)
                await self.websocket.send_json({"type": "hide_media"})
                await self.websocket.send_json({"type": "clear_whiteboard"})
                await self.websocket.send_json({
                    "type": "whiteboard_board",
                    "title": board_data.get("title", "Tableau"),
                    "lines": normalized_lines
                })
                self._remember_mode("whiteboard")
                board_handled = True
            elif board_data and isinstance(board_data, dict):
                _safe_log(f"[AI Commands][WARN] Board JSON parsed but missing usable 'lines'. Keys: {list(board_data.keys())}")
            else:
                # Re-run a strict parse on the last-cleaned variant so we can
                # pinpoint where the JSON was broken for debugging.
                diag = ""
                try:
                    json.loads(_strip_md_fence(board_json_str))
                except json.JSONDecodeError as e:
                    pos = getattr(e, "pos", 0) or 0
                    start = max(0, pos - 60)
                    end = min(len(board_json_str), pos + 60)
                    diag = f" | err={e.msg} at pos={pos} ctx=…{board_json_str[start:end]!r}…"
                _safe_log(
                    f"[AI Commands][ERROR] Failed to parse board JSON even after "
                    f"fix attempts.{diag} Preview: {board_json_str[:200]}"
                )

        # ── 1. SCHEMA detection (suppressed when exam mode active) ──
        schema_match = re.search(r'<schema>(.*?)</schema>', ai_response, re.DOTALL)
        schema_handled = False
        if schema_match and not board_handled and not should_suppress_board:
            schema_id = schema_match.group(1).strip()
            _safe_log(f"[AI Commands] Schema command detected: {schema_id}")
            await self.websocket.send_json({"type": "hide_media"})
            await self.websocket.send_json({"type": "clear_whiteboard"})
            await self.websocket.send_json({
                "type": "whiteboard_schema",
                "schema_id": schema_id
            })
            self._remember_mode("whiteboard")
            schema_handled = True

        # ── 1b. EXAM EXERCISE detection ──
        exam_ex_match = re.search(r'<exam_exercise>(.*?)</exam_exercise>', ai_response, re.DOTALL)
        exam_exercises_sent = False
        if exam_ex_match:
            exam_query = exam_ex_match.group(1).strip()
            # Capture the AI's announcement text right before the tag — this often
            # contains the explicit subject name (e.g. "exercice BAC en SVT sur la
            # gestion des déchets") even when the tag content is just a topic.
            exam_pre_text = ai_response[:exam_ex_match.start()][-400:]
            _safe_log(f"[AI Commands] Exam exercise request detected: '{exam_query}'")
            try:
                from app.services.exam_bank_service import exam_bank
                ctx = self.session_context
                subject_hint = ctx.get("subject", None)
                subject_from_user = False
                if subject_hint and subject_hint.lower() in {"général", "general", "mode libre"}:
                    subject_hint = None
                elif subject_hint:
                    subject_from_user = True  # Subject explicitly set from session context (coaching mode)
                # ── Detect subject from the LLM's exam query text (libre/explain mode) ──
                if not subject_hint and self.session_mode in ("libre", "explain"):
                    subject_hint = self._detect_subject_from_text(exam_query)
                    if subject_hint:
                        subject_from_user = True
                        _safe_log(f"[SubjectDetect] exam_query='{exam_query[:60]}' -> {subject_hint}")
                # ── If the tag content was too vague, fall back to the announcement
                # text immediately before the tag (the AI often says "en SVT…" there).
                if not subject_hint and self.session_mode in ("libre", "explain"):
                    subject_hint = self._detect_subject_from_text(exam_pre_text)
                    if subject_hint:
                        subject_from_user = True
                        _safe_log(f"[SubjectDetect] from_pre_text -> {subject_hint} (preview='{exam_pre_text[-120:]!r}')")
                if not subject_hint and self.session_mode in ("libre", "explain"):
                    subject_hint = self._infer_subject_from_context(None)
                    _safe_log(f"[SubjectDetect] fallback infer_from_context -> {subject_hint}")
                student_level = ctx.get("proficiency", None)
                conv_context = ctx.get("lesson_title", "") or ctx.get("chapter_title", "")
                exercises = exam_bank.search_full_exercises(
                    query=exam_query,
                    subject=subject_hint,
                    count=1,
                    student_level=student_level,
                    conversation_context=conv_context if conv_context else None,
                )
                if not exercises and subject_hint:
                    if subject_from_user:
                        _safe_log(f"[AI Commands] No exam exercises found for subject='{subject_hint}' (user explicitly asked for this subject). NOT retrying without subject filter.")
                    else:
                        _safe_log(f"[AI Commands] No exam exercises found with subject='{subject_hint}', retrying without subject filter")
                        exercises = exam_bank.search_full_exercises(
                            query=exam_query,
                            subject=None,
                            count=1,
                            student_level=student_level,
                            conversation_context=conv_context if conv_context else None,
                        )
                if exercises:
                    _safe_log(f"[AI Commands] Found {len(exercises)} full exercises for '{exam_query}' with {sum(len(e['questions']) for e in exercises)} questions")
                    # Hide any whiteboard/media before showing exam panel
                    await self.websocket.send_json({"type": "hide_whiteboard"})
                    await self.websocket.send_json({"type": "hide_media"})
                    await self.websocket.send_json({
                        "type": "exam_exercise",
                        "exercises": exercises,
                        "query": exam_query,
                    })
                    exam_exercises_sent = True
                else:
                    _safe_log(f"[AI Commands] No exam exercises found for '{exam_query}' — hiding stale panel")
                    await self.websocket.send_json({"type": "hide_exam_panel"})
            except Exception as e:
                _safe_log(f"[AI Commands] Error searching exam bank: {e}")

        # ── 1b-bis. Force exam panel when decision chose exam but LLM forgot the tag ──
        if force_exam_panel and not exam_exercises_sent and not exam_context:
            _safe_log(f"[AI Commands] Force exam panel fallback for: '{student_text}'")
            try:
                from app.services.exam_bank_service import exam_bank
                search_query = student_text or self.session_context.get("lesson_title", "") or self.session_context.get("chapter_title", "")
                subject_hint = self.session_context.get("subject", None)
                # subject_from_user is True when we have a strong signal about
                # which subject was requested (explicit session subject, AI
                # announcement keyword, or detection on the AI text). When
                # True, we MUST NOT drop the subject filter as a fallback —
                # otherwise an SVT request silently loads a Physique exercise.
                subject_from_user = False
                if subject_hint and subject_hint.lower() in {"général", "general", "mode libre"}:
                    subject_hint = None
                elif subject_hint:
                    subject_from_user = True
                # ── Detect subject from student query text (libre/explain mode) ──
                if not subject_hint:
                    subject_hint = self._detect_subject_from_text(search_query)
                    if subject_hint:
                        subject_from_user = True
                        _safe_log(f"[SubjectDetect] force_fallback query='{search_query[:60]}' -> {subject_hint}")
                # ── Try the AI's announcement text too — it often says 'en SVT' / 'en Physique' ──
                if not subject_hint and ai_response:
                    subject_hint = self._detect_subject_from_text(ai_response[-600:])
                    if subject_hint:
                        subject_from_user = True
                        _safe_log(f"[SubjectDetect] force_fallback ai_response -> {subject_hint}")
                if not subject_hint and self.session_mode in ("libre", "explain"):
                    subject_hint = self._infer_subject_from_context(None)
                    _safe_log(f"[SubjectDetect] force_fallback fallback infer -> {subject_hint}")
                student_level = self.session_context.get("proficiency", None)
                conv_context = self.session_context.get("lesson_title", "") or self.session_context.get("chapter_title", "")

                # ── Cascading retry so the exam panel ALWAYS opens when the
                # user explicitly requested a BAC exercise. The subject filter
                # is preserved as long as possible — we only drop it when the
                # subject genuinely has zero BAC questions available. This
                # prevents a Chimie student from receiving an SVT exercise.
                # Order:
                #   1. Full exercise + subject + lesson context
                #   2. Full exercise + subject (no lesson filter)
                #   3. Single-question search + subject (more permissive)
                #   4. Single-question search + subject + generic "exercice bac"
                #   5. Only as last resort: drop the subject filter
                exercises = exam_bank.search_full_exercises(
                    query=search_query,
                    subject=subject_hint,
                    count=1,
                    student_level=student_level,
                    conversation_context=conv_context if conv_context else None,
                )
                if not exercises and conv_context:
                    _safe_log(f"[AI Commands] Force exam fallback: 0 with lesson filter, retrying WITHOUT conversation_context (keeping subject='{subject_hint}')")
                    exercises = exam_bank.search_full_exercises(
                        query=search_query,
                        subject=subject_hint,
                        count=1,
                        student_level=student_level,
                        conversation_context=None,
                    )
                # Try single-question search WITH subject before dropping subject
                single_qs = None
                if not exercises and subject_hint:
                    _safe_log(f"[AI Commands] Force exam fallback: no full exercises, trying single-question search with subject='{subject_hint}'")
                    single_qs = exam_bank.search_exercises(
                        query=search_query,
                        subject=subject_hint,
                        count=2,
                    )
                    if not single_qs:
                        _safe_log(f"[AI Commands] Force exam fallback: single-question search empty for subject='{subject_hint}', trying generic 'exercice bac' within same subject")
                        single_qs = exam_bank.search_exercises(
                            query="exercice bac",
                            subject=subject_hint,
                            count=2,
                        )
                # Last resort: drop the subject filter entirely — but ONLY
                # when we DON'T know which subject was requested. If the user
                # (or the AI's announcement) explicitly asked for a specific
                # subject, NEVER load a different-subject exercise as fallback;
                # better to open no exercise than load a Physique RC/RL one
                # when the student asked for SVT/glycolyse.
                if not exercises and not single_qs and not subject_from_user:
                    _safe_log(f"[AI Commands] Force exam fallback: exhausted subject='{subject_hint}', dropping subject filter as last resort (subject_from_user=False)")
                    exercises = exam_bank.search_full_exercises(
                        query=search_query,
                        subject=None,
                        count=1,
                        student_level=student_level,
                        conversation_context=None,
                    )
                    if not exercises:
                        single_qs = exam_bank.search_exercises(
                            query=search_query or "exercice bac",
                            subject=None,
                            count=2,
                        )
                elif not exercises and not single_qs and subject_from_user:
                    _safe_log(f"[AI Commands] Force exam fallback: 0 exercises for subject='{subject_hint}' but subject_from_user=True — NOT cross-loading another subject. Panel will not open.")
                if not exercises and single_qs:
                        # ⚠️ Expand each matched question to its FULL parent
                        # exercise so the student gets Q1..Qn (not only the
                        # specific question whose text matched the query).
                        # A BAC exercise is a coherent whole — earlier
                        # questions introduce the document/variables needed
                        # to answer later ones. Without this expansion, the
                        # student is dropped mid-exercise.
                        seen_ex_keys: set = set()
                        expanded: list = []
                        for q in single_qs:
                            ex_key = (
                                q.get("exam_id", ""),
                                q.get("exercise_name") or "",
                                q.get("part_name") or "",
                            )
                            if ex_key in seen_ex_keys:
                                continue
                            seen_ex_keys.add(ex_key)
                            full_ex = exam_bank.get_full_exercise_for_question(
                                exam_id=ex_key[0],
                                exercise_name=ex_key[1],
                                part_name=ex_key[2],
                            )
                            if full_ex:
                                expanded.append(full_ex)
                            else:
                                # Fallback: wrap the single question if we cannot
                                # find siblings (e.g. legacy / standalone question).
                                expanded.append({
                                    "exam_id": q.get("exam_id", ""),
                                    "exam_label": q.get("exam_label", ""),
                                    "subject": q.get("subject", ""),
                                    "year": q.get("year"),
                                    "session": q.get("session", ""),
                                    "exercise_name": q.get("exercise_name") or q.get("part_name") or "Question BAC",
                                    "exercise_context": q.get("exercise_context", ""),
                                    "part_name": q.get("part_name", ""),
                                    "questions": [q],
                                })
                        exercises = expanded

                if exercises:
                    _safe_log(f"[AI Commands] Force exam panel fallback: found {len(exercises)} exercises")
                    await self.websocket.send_json({"type": "hide_whiteboard"})
                    await self.websocket.send_json({"type": "hide_media"})
                    await self.websocket.send_json({
                        "type": "exam_exercise",
                        "exercises": exercises,
                        "query": search_query,
                    })
                    exam_exercises_sent = True
                else:
                    _safe_log(f"[AI Commands] Force exam panel fallback: no exam exercises found for '{search_query}' (all retries exhausted) — hiding stale panel")
                    await self.websocket.send_json({"type": "hide_exam_panel"})
            except Exception as e:
                _safe_log(f"[AI Commands] Force exam panel fallback error: {e}")

        # ── 1c. FALLBACK: Auto-detect exam exercise intent from student text ──
        # Skip fallback when exam_context=True (follow-up from exam panel)
        if False and not exam_exercises_sent and student_text and not exam_context:
            student_lower = student_text.lower()
            exam_keywords = ["examen", "bac", "question bac", "exercice bac", 
                             "national", "exercice d'examen", "exercice de examen",
                             "entraîne", "entraine", "évaluation", "evaluation",
                             "teste moi", "tester", "exercice svt", "exercice physique",
                             "exercice chimie", "exercice math"]
            is_exam_request = any(kw in student_lower for kw in exam_keywords)
            if is_exam_request:
                _safe_log(f"[AI Commands] Fallback: student asked for exam exercise, auto-searching exam bank")
                try:
                    from app.services.exam_bank_service import exam_bank
                    # Detect subject from student text directly
                    subject_map = {
                        "svt": "SVT", "biologie": "SVT", "vie": "SVT", "terre": "SVT",
                        "physique": "Physique", "phys": "Physique",
                        "chimie": "Chimie", "chim": "Chimie",
                        "math": "Mathématiques", "maths": "Mathématiques",
                    }
                    subject_hint = None
                    for kw, subj in subject_map.items():
                        if kw in student_lower:
                            subject_hint = subj
                            break
                    # If no subject detected from text, search ALL subjects
                    _safe_log(f"[AI Commands] Fallback: subject_hint='{subject_hint}' for query '{student_text}'")
                    exercises = exam_bank.search_exercises(
                        query=student_text,
                        subject=subject_hint,
                        count=2,
                    )
                    if exercises:
                        _safe_log(f"[AI Commands] Fallback: found {len(exercises)} exam exercises")
                        await self.websocket.send_json({"type": "hide_whiteboard"})
                        await self.websocket.send_json({"type": "hide_media"})
                        await self.websocket.send_json({
                            "type": "exam_exercise",
                            "exercises": exercises,
                            "query": student_text,
                        })
                        exam_exercises_sent = True
                    else:
                        _safe_log(f"[AI Commands] Fallback: no exercises found with subject filter, trying without...")
                        # Retry without subject filter
                        exercises = exam_bank.search_exercises(
                            query=student_text,
                            subject=None,
                            count=2,
                        )
                        if exercises:
                            _safe_log(f"[AI Commands] Fallback (no filter): found {len(exercises)} exam exercises")
                            await self.websocket.send_json({"type": "hide_whiteboard"})
                            await self.websocket.send_json({"type": "hide_media"})
                            await self.websocket.send_json({
                                "type": "exam_exercise",
                                "exercises": exercises,
                                "query": student_text,
                            })
                            exam_exercises_sent = True
                        else:
                            _safe_log(f"[AI Commands] Fallback: no exam exercises found at all for '{student_text}'")
                except Exception as e:
                    _safe_log(f"[AI Commands] Fallback exam search error: {e}")
                    import traceback
                    traceback.print_exc()

        # ── 2. Try to upgrade <draw> to a pre-built schema ONLY if match is very strong ──
        # Score >= 3 required: the LLM explicitly generated <draw> JSON, so we only
        # override it when we're very confident a pre-built SVG covers the exact topic.
        if draw_data_match and not schema_handled and not suppress_whiteboard:
            auto_schema_id, auto_score = self._auto_match_schema()
            if auto_schema_id and auto_score >= 3:
                _safe_log(f"[AI Commands] Upgrading <draw> to pre-built schema: {auto_schema_id} (score={auto_score})")
                await self.websocket.send_json({"type": "hide_media"})
                await self.websocket.send_json({"type": "clear_whiteboard"})
                await self.websocket.send_json({
                    "type": "whiteboard_schema",
                    "schema_id": auto_schema_id
                })
                self._remember_mode("whiteboard")
                schema_handled = True
            elif auto_schema_id:
                _safe_log(f"[AI Commands] Auto-match {auto_schema_id} score={auto_score} too low to override explicit <draw>, letting canvas draw proceed")

        # ── 3. Fallback: LLM expressed drawing intent but no tag — auto-match schema ──
        if not draw_data_match and not schema_handled and not suppress_whiteboard:
            drawing_intent_patterns = [
                r"je vais te dessiner", r"voici le sch[ée]ma", r"je vais te montrer au tableau",
                r"voici le processus", r"voici un sch[ée]ma", r"regarde le sch[ée]ma",
                r"je dessine", r"voici le diagramme", r"je vais te montrer ça au tableau",
                r"dessiner un", r"dessiner une", r"dessiner le", r"dessiner la",
                r"\[draw\]", r"tableau blanc", r"whiteboard",
            ]
            has_drawing_intent = any(re.search(p, lower_response) for p in drawing_intent_patterns)
            
            # Also force auto-match when decision system requested whiteboard
            if has_drawing_intent or force_schema:
                reason = "force_schema=True" if force_schema and not has_drawing_intent else "drawing intent in text"
                _safe_log(f"[AI Commands] Attempting auto-match schema (reason: {reason})")
                auto_schema_id, auto_score = self._auto_match_schema()
                if auto_schema_id and auto_score >= 3:
                    _safe_log(f"[AI Commands] Auto-matched schema: {auto_schema_id} (score={auto_score})")
                    await self.websocket.send_json({"type": "hide_media"})
                    await self.websocket.send_json({"type": "clear_whiteboard"})
                    await self.websocket.send_json({
                        "type": "whiteboard_schema",
                        "schema_id": auto_schema_id
                    })
                    self._remember_mode("whiteboard")
                    schema_handled = True
                else:
                    _safe_log(f"[AI Commands] Auto-match score too low ({auto_score}), skipping")

        # ── 4. Natural language media triggers ──
        media_triggers = ["regarde ce schéma", "observe cette image", "voici une illustration", 
                         "regarde cette image", "observe le diagramme"]
        
        if not draw_data_match and not schema_handled and any(trigger in lower_response for trigger in media_triggers):
            if suppress_media:
                _safe_log(f"[AI Commands] Media trigger detected but suppressed (already sent explicit media)")
            else:
                _safe_log(f"[AI Commands] Media trigger detected in AI response")
                await self.websocket.send_json({"type": "hide_whiteboard"})
                await self._auto_suggest_resource()

        # ── 5. <draw> canvas drawing — suppressed when exam mode active ──
        if draw_data_match and not schema_handled and not should_suppress_board:
            draw_title_match = re.search(r'DESSINER_SCHEMA:(.+?)(?:\n|$)', ai_response)
            draw_title = draw_title_match.group(1).strip() if draw_title_match else "Schema"
            draw_json_str = draw_data_match.group(1).strip()
            draw_json_str = draw_json_str.replace('</draw>', '').strip()
            
            _safe_log(f"[AI Commands] Raw draw JSON length: {len(draw_json_str)} chars")
            
            def try_fix_json(s):
                """Try to fix truncated JSON by closing open brackets."""
                try:
                    return json.loads(s)
                except json.JSONDecodeError:
                    pass
                for suffix in [']', ']}]', ']}', '"}]}]', '"}]}', '"]}}]']:
                    try:
                        return json.loads(s + suffix)
                    except json.JSONDecodeError:
                        continue
                return None
            
            draw_steps = try_fix_json(draw_json_str)
            if draw_steps is not None:
                if not isinstance(draw_steps, list):
                    draw_steps = [draw_steps]
                if not draw_title_match and draw_steps and isinstance(draw_steps[0], dict) and draw_steps[0].get('title'):
                    draw_title = draw_steps[0]['title']
                
                draw_steps = self._fix_overlapping_elements(draw_steps)
                
                # Normalize steps to ensure each has an 'elements' array
                norm_title, norm_steps = normalize_draw_steps({"title": draw_title, "steps": draw_steps})
                if norm_steps:
                    draw_title = norm_title or draw_title
                    draw_steps = norm_steps
                
                _safe_log(f"[AI Commands] Whiteboard drawing detected: {draw_title} ({len(draw_steps)} steps)")
                await self.websocket.send_json({"type": "hide_media"})
                await self.websocket.send_json({
                    "type": "whiteboard_draw",
                    "title": draw_title,
                    "steps": draw_steps
                })
                self._remember_mode("whiteboard")
            else:
                _safe_log(f"[AI Commands][ERROR] Failed to parse draw JSON even after fix attempts. Preview: {draw_json_str[:200]}")

        # ══════════════════════════════════════════════════════════════════════════
        # 6. RESOURCE MANAGEMENT COMMANDS (new unified system)
        # Note: EFFACER_TABLEAU is handled at the beginning of this function
        # ══════════════════════════════════════════════════════════════════════════

        # FERMER_TABLEAU — close whiteboard
        if "FERMER_TABLEAU" in ai_response:
            _safe_log("[AI Commands] FERMER_TABLEAU detected")
            await self.websocket.send_json({"type": "hide_whiteboard"})

        # OUVRIR_IMAGE — open relevant image from lesson resources
        if "OUVRIR_IMAGE" in ai_response:
            _safe_log("[AI Commands] OUVRIR_IMAGE detected")
            await self.websocket.send_json({"type": "hide_whiteboard"})
            await self._auto_suggest_resource(preferred_resource_type="image")

        # FERMER_IMAGE — close image/media
        if "FERMER_IMAGE" in ai_response or "CACHER_MEDIA" in ai_response:
            _safe_log("[AI Commands] FERMER_IMAGE/CACHER_MEDIA detected")
            await self.websocket.send_json({"type": "hide_media"})

        # OUVRIR_SIMULATION — open relevant simulation
        if "OUVRIR_SIMULATION" in ai_response:
            _safe_log("[AI Commands] OUVRIR_SIMULATION detected")
            await self.websocket.send_json({"type": "hide_whiteboard"})
            await self._auto_suggest_resource(preferred_resource_type="simulation")

        # FERMER_SIMULATION — close simulation
        if "FERMER_SIMULATION" in ai_response:
            _safe_log("[AI Commands] FERMER_SIMULATION detected")
            await self.websocket.send_json({"type": "hide_media"})

        # OUVRIR_EXERCICE — open relevant exercise (search exam bank first)
        if "OUVRIR_EXERCICE" in ai_response:
            _safe_log("[AI Commands] OUVRIR_EXERCICE detected")
            await self.websocket.send_json({"type": "hide_whiteboard"})
            await self.websocket.send_json({"type": "hide_media"})
            if not exam_exercises_sent:
                # Try to search exam bank for relevant exercises
                try:
                    from app.services.exam_bank_service import exam_bank
                    ctx = self.session_context
                    subject_hint = ctx.get("subject", None)
                    subject_from_user = False
                    if not subject_hint or subject_hint.lower() in ["général", "general", "mode libre"]:
                        subject_hint = self._detect_subject_from_text(student_text)
                        if subject_hint:
                            subject_from_user = True
                            _safe_log(f"[SubjectDetect] OUVRIR_EXERCICE query='{student_text[:60]}' -> {subject_hint}")
                        else:
                            subject_hint = self._infer_subject_from_context(None)
                            _safe_log(f"[SubjectDetect] OUVRIR_EXERCICE fallback infer -> {subject_hint}")
                    query = student_text if student_text else (ctx.get("lesson_title", "") or ctx.get("chapter_title", ""))
                    # Prefer full-exercise search so the student gets Q1..Qn,
                    # not only the question whose text matched the query.
                    exercises = exam_bank.search_full_exercises(
                        query=query, subject=subject_hint, count=1,
                    )
                    if not exercises:
                        single_qs = exam_bank.search_exercises(query=query, subject=subject_hint, count=2)
                        if not single_qs and subject_hint and not (self.session_mode in ("libre", "explain") and subject_from_user):
                            _safe_log(f"[AI Commands] OUVRIR_EXERCICE: no results with subject='{subject_hint}', retrying without subject filter")
                            single_qs = exam_bank.search_exercises(query=query, subject=None, count=2)
                        elif not single_qs and subject_from_user:
                            _safe_log(f"[AI Commands] OUVRIR_EXERCICE: no results for subject='{subject_hint}' (user explicitly asked). NOT retrying without filter.")
                        # Expand each matched question to its FULL parent exercise
                        if single_qs:
                            seen_ex_keys: set = set()
                            expanded: list = []
                            for q in single_qs:
                                ex_key = (
                                    q.get("exam_id", ""),
                                    q.get("exercise_name") or "",
                                    q.get("part_name") or "",
                                )
                                if ex_key in seen_ex_keys:
                                    continue
                                seen_ex_keys.add(ex_key)
                                full_ex = exam_bank.get_full_exercise_for_question(
                                    exam_id=ex_key[0],
                                    exercise_name=ex_key[1],
                                    part_name=ex_key[2],
                                )
                                if full_ex:
                                    expanded.append(full_ex)
                                else:
                                    expanded.append({
                                        "exam_id": q.get("exam_id", ""),
                                        "exam_label": q.get("exam_label", ""),
                                        "subject": q.get("subject", ""),
                                        "year": q.get("year"),
                                        "session": q.get("session", ""),
                                        "exercise_name": q.get("exercise_name") or q.get("part_name") or "Question BAC",
                                        "exercise_context": q.get("exercise_context", ""),
                                        "part_name": q.get("part_name", ""),
                                        "questions": [q],
                                    })
                            exercises = expanded
                    if exercises:
                        _safe_log(f"[AI Commands] OUVRIR_EXERCICE: found {len(exercises)} exam exercises")
                        await self.websocket.send_json({"type": "hide_whiteboard"})
                        await self.websocket.send_json({"type": "hide_media"})
                        await self.websocket.send_json({
                            "type": "exam_exercise",
                            "exercises": exercises,
                            "query": query,
                        })
                        exam_exercises_sent = True
                    else:
                        await self._auto_suggest_exercise()
                except Exception as e:
                    _safe_log(f"[AI Commands] OUVRIR_EXERCICE exam search error: {e}")
                    await self._auto_suggest_exercise()
            else:
                _safe_log("[AI Commands] OUVRIR_EXERCICE: exam exercises already sent")

        # FERMER_EXERCICE — close exercise panel and exam panel
        if "FERMER_EXERCICE" in ai_response:
            _safe_log("[AI Commands] FERMER_EXERCICE detected")
            await self.websocket.send_json({"type": "hide_exercise"})
            await self.websocket.send_json({"type": "hide_exam_panel"})

        # TOUT_FERMER — close everything
        if "TOUT_FERMER" in ai_response:
            _safe_log("[AI Commands] TOUT_FERMER detected")
            await self.websocket.send_json({"type": "hide_whiteboard"})
            await self.websocket.send_json({"type": "hide_media"})
            await self.websocket.send_json({"type": "hide_exercise"})
            await self.websocket.send_json({"type": "hide_exam_panel"})

        # Detect PHASE_SUIVANTE command
        if "PHASE_SUIVANTE" in ai_response:
            await self._auto_advance_phase()
        
        # Detect legacy EXERCICE:id command (specific exercise by ID)
        exercise_match = re.search(r'EXERCICE:(\S+)', ai_response)
        if exercise_match:
            exercise_id = exercise_match.group(1)
            await self.websocket.send_json({
                "type": "show_exercise",
                "exercise_id": exercise_id
            })
            self._remember_mode("exercise")
            return

        # ══════════════════════════════════════════════════════════════════════════
        # 7. AUTO-BOARD FALLBACK: Convert AI text to board when no visual command
        #    was generated. This ensures all responses appear on the whiteboard.
        #    SKIP if media was already displayed (suppress_media=True) to avoid
        #    overwriting an image/simulation that was just shown.
        # ══════════════════════════════════════════════════════════════════════════
        has_any_visual = (
            board_handled
            or schema_handled
            or exam_exercises_sent
            or (draw_data_match and not suppress_draw)
            or suppress_media  # media was already sent by decision engine
            or "OUVRIR_IMAGE" in ai_response
            or "OUVRIR_SIMULATION" in ai_response
            or "OUVRIR_EXERCICE" in ai_response
            or "FERMER_TABLEAU" in ai_response
            or "TOUT_FERMER" in ai_response
        )
        if not has_any_visual:
            # Strip command tags but PRESERVE newlines for paragraph splitting.
            # Important: also strip <suggestions> and <exam_exercise> — otherwise
            # their raw JSON body ends up rendered as board lines.
            _strip_tag_re = (
                r'<(?:ui|draw|schema|board|suggestions|exam_exercise)>'
                r'[\s\S]*?'
                r'</(?:ui|draw|schema|board|suggestions|exam_exercise)>'
            )
            clean_text = re.sub(_strip_tag_re, '', ai_response, flags=re.DOTALL)
            # Also handle unterminated tags (e.g. stream cut mid-block)
            clean_text = re.sub(
                r'<(?:ui|draw|schema|board|suggestions|exam_exercise)>[\s\S]*',
                '', clean_text, flags=re.DOTALL
            ).strip()
            # Remove command keywords
            for kw in ["EFFACER_TABLEAU", "RESET_TABLEAU", "FERMER_TABLEAU", "PHASE_SUIVANTE",
                        "FERMER_IMAGE", "CACHER_MEDIA", "FERMER_SIMULATION", "FERMER_EXERCICE"]:
                clean_text = clean_text.replace(kw, "")
            # Only collapse horizontal whitespace, keep newlines intact
            clean_text = re.sub(r'[^\S\n]+', ' ', clean_text).strip()

            # ── SKIP auto-board for conversational / short / chit-chat responses ──
            # These shouldn't pollute the whiteboard with raw discussion text.
            _clean_lower = clean_text.lower()
            conversational_markers = [
                "d'accord", "super !", "super!", "parfait !", "parfait!",
                "content de te revoir", "tu progresses", "très bien !", "excellent !",
                "bravo", "tu as raison", "je comprends que tu",
                "es-tu prêt", "es tu prêt", "prêt pour",
                "on peut passer", "on passe à", "passons à", "passons a",
                "félicitations", "bonne continuation",
            ]
            is_conversational = (
                len(clean_text) < 300
                or any(m in _clean_lower for m in conversational_markers)
            )
            # Also skip if response has no substantial educational content markers
            has_educational_content = (
                any(m in _clean_lower for m in [
                    "définition", "formule", "théorème", "propriété",
                    "démonstration", "étape ", "exemple :", "exemple:",
                    "$", "\\(", "\\[",  # LaTeX math
                    "voici la correction", "correction détaillée",
                ])
                or len(clean_text) > 600
            )
            if is_conversational and not has_educational_content and not force_schema:
                _safe_log(f"[AI Commands] Skipping auto-board fallback (conversational response, {len(clean_text)} chars)")
                return

            if len(clean_text) > 20:
                if force_schema:
                    retry_count = getattr(self, '_structured_board_retry_count', 0)
                    max_retries = 3  # Increased from 1 to 3 retries
                    if retry_count < max_retries:
                        self._structured_board_retry_count = retry_count + 1
                        _safe_log(f"[AI Commands] Structured whiteboard retry triggered ({self._structured_board_retry_count}/{max_retries})")
                        
                        # Escalating retry messages - more strict each time
                        retry_prompts = [
                            # Retry 1: Gentle reminder
                            (
                                "Tu n'as pas généré le contenu visuel demandé. Réessaie maintenant en produisant UNIQUEMENT le contenu visuel final. "
                                "Génère un bloc <ui>{\"actions\":[{\"type\":\"whiteboard\",\"action\":\"show_board\",\"payload\":{\"title\":\"...\",\"lines\":[...]}}]}</ui> complet. "
                                "Ne paraphrase pas. Donne directement le JSON structuré."
                            ),
                            # Retry 2: More strict
                            (
                                "ERREUR: Ta réponse ne contient pas de tableau structuré valide. "
                                "Tu DOIS générer UNIQUEMENT un bloc <ui> avec le JSON complet du tableau. "
                                "Format EXACT requis: <ui>{\"actions\":[{\"type\":\"whiteboard\",\"action\":\"show_board\",\"payload\":{\"title\":\"TITRE\",\"lines\":[{\"type\":\"title\",\"content\":\"...\"}]}}]}</ui> "
                                "AUCUN texte avant ou après le bloc <ui>. Juste le JSON."
                            ),
                            # Retry 3: Final warning - very strict
                            (
                                "DERNIÈRE TENTATIVE. Tu as échoué 2 fois à générer un tableau. "
                                "Génère MAINTENANT ce bloc EXACT (remplace les ... par le contenu): "
                                "<ui>{\"actions\":[{\"type\":\"whiteboard\",\"action\":\"show_board\",\"payload\":{\"title\":\"...\",\"lines\":[{\"type\":\"title\",\"content\":\"...\"},{\"type\":\"text\",\"content\":\"...\"}]}}]}</ui> "
                                "RIEN D'AUTRE. PAS DE TEXTE. JUSTE LE BLOC <ui>."
                            ),
                        ]
                        
                        retry_messages = list(self.conversation_history)
                        retry_messages.append({"role": "assistant", "content": self._sanitize_history_content(ai_response)})
                        retry_messages.append({
                            "role": "user",
                            "content": retry_prompts[min(retry_count, len(retry_prompts) - 1)]
                        })
                        try:
                            retried_response = ""
                            async for token in llm_service.chat_stream(
                                messages=retry_messages,
                                system_prompt=getattr(self, '_last_system_prompt', ''),
                                max_tokens=2400,
                            ):
                                retried_response += token
                            _safe_log(f"[AI Commands] Structured retry response preview: {retried_response[:200]}...")
                            
                            # Validate the retry response has a valid <ui> block
                            has_valid_ui = bool(re.search(r'<ui>\s*\{.*"actions".*"whiteboard".*"payload".*\}\s*</ui>', retried_response, re.DOTALL))
                            
                            if has_valid_ui:
                                # Retry: first attempt failed to display (suppressed whiteboard + exam fallback failed).
                                # Allow whiteboard through and disable exam fallback to avoid infinite loop.
                                await self._execute_ai_commands(
                                    retried_response,
                                    suppress_draw=suppress_draw,
                                    suppress_media=suppress_media,
                                    force_schema=True,
                                    student_text=student_text,
                                    suppress_whiteboard=False,
                                    exam_context=exam_context,
                                    force_exam_panel=False,
                                )
                                return
                            else:
                                _safe_log(f"[AI Commands] Max retries ({max_retries}) reached, falling back to auto-board")
                                self._structured_board_retry_count = 0
                        except Exception as e:
                            _safe_log(f"[AI Commands] Structured whiteboard retry failed: {e}")
                            self._structured_board_retry_count = 0

                auto_lines = []

                def _clean_md(s: str) -> str:
                    """Strip markdown formatting from a string for clean board display."""
                    s = re.sub(r'\*\*(.+?)\*\*', r'\1', s)  # **bold**
                    s = re.sub(r'\*(.+?)\*', r'\1', s)        # *italic*
                    s = re.sub(r'__(.+?)__', r'\1', s)        # __bold__
                    s = re.sub(r'_(.+?)_', r'\1', s)          # _italic_
                    s = re.sub(r'`(.+?)`', r'\1', s)          # `code`
                    return s.strip()

                # Split by double-newline for paragraphs, or single-newline for lines
                paragraphs = re.split(r'\n{2,}', clean_text)
                for para in paragraphs:
                    para = para.strip()
                    if not para:
                        continue
                    # Process each line within a paragraph
                    sub_lines = para.split('\n')
                    for raw_line in sub_lines:
                        raw_line = raw_line.strip()
                        if not raw_line:
                            continue
                        # Detect headings
                        if raw_line.startswith('### '):
                            auto_lines.append({"type": "subtitle", "content": _clean_md(raw_line[4:])})
                        elif raw_line.startswith('## '):
                            auto_lines.append({"type": "subtitle", "content": _clean_md(raw_line[3:])})
                        elif raw_line.startswith('# '):
                            auto_lines.append({"type": "title", "content": _clean_md(raw_line[2:])})
                        # Detect bold-only lines as subtitles
                        elif re.match(r'^\*\*(.+?)\*\*\s*:?\s*$', raw_line):
                            title_text = re.sub(r'\*\*', '', raw_line).strip().rstrip(':')
                            auto_lines.append({"type": "subtitle", "content": title_text})
                        # Detect bullet points as steps
                        elif re.match(r'^[-•*]\s+', raw_line):
                            bullet_text = re.sub(r'^[-•*]\s+', '', raw_line)
                            auto_lines.append({"type": "step", "content": _clean_md(bullet_text), "label": "•"})
                        # Detect numbered items as steps
                        elif re.match(r'^\d+[\.\)]\s+', raw_line):
                            num_match = re.match(r'^(\d+)[\.\)]\s+(.+)', raw_line)
                            if num_match:
                                auto_lines.append({"type": "step", "content": _clean_md(num_match.group(2)), "label": num_match.group(1)})
                        # Display-mode math ($$...$$)
                        elif raw_line.startswith('$$') and raw_line.endswith('$$'):
                            auto_lines.append({"type": "math", "content": raw_line})
                        else:
                            auto_lines.append({"type": "text", "content": _clean_md(raw_line)})

                    # Add separator between paragraphs
                    if para != paragraphs[-1].strip():
                        auto_lines.append({"type": "separator", "content": ""})

                if auto_lines:
                    _safe_log(f"[AI Commands] Auto-board fallback: converting AI text to board ({len(auto_lines)} lines)")
                    # Defense in depth: rewrite ASCII genetics (DO//dø) to \dfrac.
                    auto_lines = _sanitize_genetics_cells(auto_lines)
                    await self.websocket.send_json({"type": "clear_whiteboard"})
                    await self.websocket.send_json({
                        "type": "whiteboard_board",
                        "title": "Explication",
                        "lines": auto_lines,
                    })
                    self._remember_mode("whiteboard")

    async def _auto_advance_phase(self):
        """Automatically advance to the next phase and update progress."""
        phases = ["activation", "exploration", "explanation", "application", "consolidation"]
        try:
            current_idx = phases.index(self.current_phase)
            if current_idx < len(phases) - 1:
                # Mark current objective as completed before advancing
                if hasattr(self, 'lesson_objectives') and self.lesson_objectives:
                    objective_index = min(current_idx, len(self.lesson_objectives) - 1)
                    await self.websocket.send_json({
                        "type": "objective_completed",
                        "objective_index": objective_index,
                        "objective": self.lesson_objectives[objective_index] if objective_index < len(self.lesson_objectives) else None
                    })
                    _safe_log(f"[Progress] Objective {objective_index} completed")
                
                self.current_phase = phases[current_idx + 1]
                await self.websocket.send_json({
                    "type": "phase_changed",
                    "phase": self.current_phase,
                    "auto": True
                })
                _safe_log(f"[Phase] Advanced to {self.current_phase}")
        except ValueError:
            pass

    def _available_resource_types(self) -> set[str]:
        return {
            resource.get("resource_type")
            for resource in self.lesson_resources
            if resource.get("resource_type")
        }

    def _remember_mode(self, mode: str):
        if not mode:
            return
        self.recent_resource_modes.append(mode)
        if len(self.recent_resource_modes) > 5:
            self.recent_resource_modes = self.recent_resource_modes[-5:]

    def _auto_match_schema(self) -> tuple[str | None, int]:
        """Auto-match a pre-built SVG schema based on current lesson context.
        Returns (schema_id, score) tuple. Callers decide the minimum threshold."""
        SCHEMA_KEYWORDS = {
            "svt_glycolyse": ["glycolyse", "glucose", "pyruvate", "تحلل سكري"],
            "svt_respiration_cellulaire": ["respiration cellulaire", "krebs", "chaîne respiratoire", "تنفس خلوي"],
            "svt_fermentation": ["fermentation", "anaérobie", "lactique", "alcoolique", "تخمر"],
            "svt_chaine_respiratoire": ["chaîne respiratoire", "phosphorylation oxydative", "atp synthase", "complexe respiratoire", "nadh", "fadh2", "gradient", "السلسلة التنفسية", "الفسفرة التأكسدية"],
            "svt_cycle_krebs": ["cycle de krebs", "acétyl-coa", "citrate", "oxaloacétate", "acide citrique", "حلقة كريبس", "دورة كريبس"],
            "svt_bilan_energetique": ["bilan énergétique", "rendement", "comparaison respiration fermentation", "36 atp", "حصيلة طاقية", "مقارنة"],
            "svt_transcription_traduction": ["transcription", "traduction", "arn", "ribosome", "استنساخ", "ترجمة"],
            "svt_mitose": ["mitose", "division cellulaire", "prophase", "métaphase", "انقسام"],
            "svt_subduction": ["subduction", "plaque", "tectonique", "اندساس"],
            "phys_ondes_mecaniques": ["onde", "longueur d'onde", "fréquence", "diffraction", "موجة"],
            "phys_dipole_rc": ["dipôle rc", "condensateur", "charge", "décharge", "مكثف"],
            "phys_rlc": ["rlc", "oscillation", "résonance", "تذبذب"],
            "phys_newton": ["newton", "force", "inertie", "accélération", "قوة", "نيوتن"],
            "chem_cinetique": ["cinétique", "vitesse de réaction", "catalyseur", "حركية"],
            "chem_radioactivite": ["radioactivité", "décroissance", "demi-vie", "نشاط إشعاعي"],
            "chem_acides_bases": ["acide", "base", "ph", "titrage", "حمض", "قاعدة"],
            "chem_piles_electrolyse": ["pile", "électrolyse", "anode", "cathode", "عمود كهربائي"],
            "chem_esterification": ["ester", "estérification", "hydrolyse", "أسترة"],
            "math_limites": ["limite", "asymptote", "نهاية"],
            "math_derivation": ["dérivée", "dérivation", "tangente", "اشتقاق"],
            "math_exp_ln": ["exponentielle", "logarithme", "ln", "exp", "أسية"],
            "math_suites": ["suite", "arithmétique", "géométrique", "متتالية"],
            "math_integrales": ["intégrale", "primitive", "aire", "تكامل"],
            "math_probabilites": ["probabilité", "binomiale", "dénombrement", "احتمال"],
        }
        
        # Build context string from lesson info + recent conversation
        context_parts = []
        ctx = self.session_context or {}
        if ctx.get("lesson_title"):
            context_parts.append(ctx["lesson_title"].lower())
        if ctx.get("chapter_title"):
            context_parts.append(ctx["chapter_title"].lower())
        if ctx.get("subject") or ctx.get("subject_name"):
            context_parts.append((ctx.get("subject") or ctx.get("subject_name", "")).lower())
        if ctx.get("objective"):
            context_parts.append(ctx["objective"].lower())
        # Include only STUDENT messages (not AI responses which list many topics)
        for msg in self.conversation_history[-6:]:
            if isinstance(msg, dict) and msg.get('role') == 'user':
                content = msg.get('content', '')
                context_parts.append(content.lower())
        
        context = ' '.join(context_parts)
        _safe_log(f"[AutoMatch] Context string (first 300 chars): {context[:300]}")
        if not context.strip():
            _safe_log(f"[AutoMatch] Empty context — cannot match")
            return None
        
        best_id = None
        best_score = 0
        for schema_id, keywords in SCHEMA_KEYWORDS.items():
            score = sum(1 for kw in keywords if kw.lower() in context)
            if score > 0:
                _safe_log(f"[AutoMatch] {schema_id}: score={score} (matched: {[kw for kw in keywords if kw.lower() in context]})")
            if score > best_score:
                best_score = score
                best_id = schema_id
        
        _safe_log(f"[AutoMatch] Best match: {best_id} (score={best_score})")
        return (best_id, best_score) if best_score >= 1 else (None, 0)

    async def _load_all_resources(self):
        """Load ALL resources from lesson_resources table (for libre mode)."""
        try:
            supabase = get_supabase()
            result = supabase.table("lesson_resources")\
                .select("*")\
                .order("order_index")\
                .execute()
            
            self.lesson_resources = result.data if result.data else []
            _safe_log(f"[Resources] Libre mode: Loaded {len(self.lesson_resources)} total resources from all lessons")
        except Exception as e:
            _safe_log(f"[Resources] Error loading all resources: {e}")
            self.lesson_resources = []

    async def _load_lesson_resources(self, lesson_id: str):
        """Load all resources for the current lesson from lesson_resources table."""
        try:
            supabase = get_supabase()
            
            # Load lesson data with chapter info
            lesson_result = supabase.table("lessons")\
                .select("learning_objectives, content, title_fr, chapter_id, chapters(title_fr, subject_id)")\
                .eq("id", lesson_id)\
                .execute()
            
            if lesson_result.data and len(lesson_result.data) > 0:
                lesson_data = lesson_result.data[0]
                self.lesson_objectives = lesson_data.get("learning_objectives", [])
                _safe_log(f"[Resources] Loaded {len(self.lesson_objectives)} learning objectives")
                
                # Update session_context with correct subject from DB
                chapter_data = lesson_data.get("chapters", {})
                if chapter_data:
                    if chapter_data.get("title_fr"):
                        self.session_context["chapter_title"] = chapter_data["title_fr"]
                    
                    # Get subject name from separate query (nested join doesn't work)
                    subject_id = chapter_data.get("subject_id")
                    if subject_id:
                        subj_result = supabase.table("subjects")\
                            .select("name_fr")\
                            .eq("id", subject_id)\
                            .execute()
                        if subj_result.data and subj_result.data[0].get("name_fr"):
                            db_subject = subj_result.data[0]["name_fr"]
                            self.session_context["subject"] = db_subject
                            _safe_log(f"[Resources] Updated subject from DB: {db_subject}")
                
                if lesson_data.get("title_fr"):
                    self.session_context["lesson_title"] = lesson_data["title_fr"]
            
            # Load resources
            result = supabase.table("lesson_resources")\
                .select("*")\
                .eq("lesson_id", lesson_id)\
                .order("order_index")\
                .execute()
            
            self.lesson_resources = result.data if result.data else []
            _safe_log(f"[Resources] Loaded {len(self.lesson_resources)} resources for lesson {lesson_id}")
            
            # Log each resource's file_path to debug local path issue
            for resource in self.lesson_resources:
                file_path = resource.get('file_path', 'N/A')
                title = resource.get('title', 'N/A')
                _safe_log(f"[Resources] - {title}: {file_path}")
                if file_path and file_path.startswith('/media/'):
                    _safe_log(f"[Resources] WARNING: Resource '{title}' has legacy local path: {file_path}")
                if file_path == 'local:metadata':
                    metadata = resource.get('metadata', {})
                    _safe_log(f"[Resources] local:metadata resource '{title}' — metadata keys: {list(metadata.keys()) if isinstance(metadata, dict) else type(metadata)}")
        except Exception as e:
            _safe_log(f"[Resources] Error loading resources: {e}")
            self.lesson_resources = []
            self.lesson_objectives = []

    def _find_best_resource(self, concepts: list[str], resource_type: str = None, phase: str = None) -> dict:
        """Find the best matching resource based on concepts, type, and phase."""
        if not self.lesson_resources:
            return None
        
        phase_filter = phase or self.current_phase
        candidates = [r for r in self.lesson_resources if not r.get('phase') or r.get('phase') == phase_filter]
        
        if resource_type:
            candidates = [r for r in candidates if r.get('resource_type') == resource_type]
        
        if not candidates:
            candidates = self.lesson_resources
        
        scored = []
        for resource in candidates:
            resource_concepts = resource.get('concepts', [])
            if not resource_concepts:
                score = 0
            else:
                matches = sum(1 for c in concepts if any(rc.lower() in c.lower() or c.lower() in rc.lower() for rc in resource_concepts))
                score = matches
            
            scored.append((score, resource))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        
        if scored and scored[0][0] > 0:
            return scored[0][1]
        
        if candidates:
            return candidates[0]
        
        return None

    async def _auto_suggest_exercise(self):
        """Find and suggest a relevant exercise based on current context."""
        try:
            ctx = self.session_context or {}
            lesson_id = ctx.get("lesson_id") or self.current_lesson_id
            
            if not lesson_id:
                _safe_log("[Exercise] No lesson_id available for exercise suggestion")
                return
            
            supabase = get_supabase()
            
            # Try to find exercises for this lesson
            result = supabase.table("exercises")\
                .select("*")\
                .eq("lesson_id", lesson_id)\
                .order("difficulty_level")\
                .limit(5)\
                .execute()
            
            exercises = result.data if result.data else []
            
            if not exercises:
                # Try to find exercises for the chapter
                chapter_id = ctx.get("chapter_id")
                if chapter_id:
                    result = supabase.table("exercises")\
                        .select("*")\
                        .eq("chapter_id", chapter_id)\
                        .order("difficulty_level")\
                        .limit(5)\
                        .execute()
                    exercises = result.data if result.data else []
            
            if exercises:
                # Pick one based on proficiency
                proficiency = ctx.get("proficiency", "intermédiaire")
                if proficiency == "débutant":
                    exercise = exercises[0]  # Easiest
                elif proficiency == "avancé":
                    exercise = exercises[-1]  # Hardest
                else:
                    exercise = exercises[len(exercises) // 2]  # Middle
                
                _safe_log(f"[Exercise] Suggesting exercise: {exercise.get('id')} - {exercise.get('title', 'Sans titre')}")
                await self.websocket.send_json({
                    "type": "show_exercise",
                    "exercise_id": exercise.get("id"),
                    "exercise": exercise
                })
                self._remember_mode("exercise")
            else:
                _safe_log("[Exercise] No exercises found for current context")
                
        except Exception as e:
            _safe_log(f"[Exercise] Error suggesting exercise: {e}")

    def _fix_overlapping_elements(self, draw_steps: list) -> list:
        """Detect and fix overlapping elements by adjusting their positions."""
        try:
            for step in draw_steps:
                if not isinstance(step, dict) or 'elements' not in step:
                    continue
                
                elements = step['elements']
                if not isinstance(elements, list):
                    continue

                def get_bounds(elem: dict) -> tuple[float, float, float, float]:
                    elem_type = elem.get('type')
                    x = float(elem.get('x', 0) or 0)
                    y = float(elem.get('y', 0) or 0)

                    if elem_type in ['cell', 'circle', 'nucleus']:
                        r = float(elem.get('radius', 50) or 50)
                        return (x - r, y - r, x + r, y + r)

                    width = float(elem.get('width', 100) or 100)
                    height = float(elem.get('height', 50) or 50)
                    return (x, y, x + width, y + height)

                def is_contained(inner: dict, outer: dict) -> bool:
                    outer_type = outer.get('type')
                    if outer_type not in ['cell', 'nucleus']:
                        return False

                    ix1, iy1, ix2, iy2 = get_bounds(inner)
                    ox1, oy1, ox2, oy2 = get_bounds(outer)
                    padding = 8
                    return (
                        ix1 >= ox1 + padding and
                        iy1 >= oy1 + padding and
                        ix2 <= ox2 - padding and
                        iy2 <= oy2 - padding
                    )
                
                # Check each pair of elements for overlap
                for i, elem1 in enumerate(elements):
                    if not isinstance(elem1, dict):
                        continue
                    
                    for j, elem2 in enumerate(elements[i+1:], start=i+1):
                        if not isinstance(elem2, dict):
                            continue
                        
                        # Skip if one is text or arrow (they can overlap)
                        if elem1.get('type') in ['text', 'arrow', 'line'] or elem2.get('type') in ['text', 'arrow', 'line']:
                            continue

                        # Allow intentional containment inside biological containers
                        if is_contained(elem2, elem1) or is_contained(elem1, elem2):
                            continue
                        
                        # Get positions and sizes
                        x1 = elem1.get('x', 0)
                        y1 = elem1.get('y', 0)
                        x2 = elem2.get('x', 0)
                        y2 = elem2.get('y', 0)
                        
                        # Calculate sizes
                        if elem1.get('type') in ['cell', 'circle', 'nucleus']:
                            size1 = elem1.get('radius', 50) * 2
                        elif elem1.get('type') == 'mitochondria':
                            size1 = max(elem1.get('width', 100), elem1.get('height', 50))
                        else:
                            size1 = max(elem1.get('width', 100), elem1.get('height', 50))
                        
                        if elem2.get('type') in ['cell', 'circle', 'nucleus']:
                            size2 = elem2.get('radius', 50) * 2
                        elif elem2.get('type') == 'mitochondria':
                            size2 = max(elem2.get('width', 100), elem2.get('height', 50))
                        else:
                            size2 = max(elem2.get('width', 100), elem2.get('height', 50))

                        b1x1, b1y1, b1x2, b1y2 = get_bounds(elem1)
                        b2x1, b2y1, b2x2, b2y2 = get_bounds(elem2)
                        overlap_x = min(b1x2, b2x2) - max(b1x1, b2x1)
                        overlap_y = min(b1y2, b2y2) - max(b1y1, b2y1)

                        # If overlapping, adjust position
                        if overlap_x > 0 and overlap_y > 0:
                            _safe_log(f"[Whiteboard] Overlap detected between {elem1.get('id')} and {elem2.get('id')}, adjusting...")
                            
                            # Move elem2 away from elem1
                            shift = max(overlap_x, overlap_y) + 20
                            
                            # Calculate direction vector
                            if x2 != x1 or y2 != y1:
                                dx = x2 - x1
                                dy = y2 - y1
                                length = (dx**2 + dy**2)**0.5
                                dx /= length
                                dy /= length
                            else:
                                # If same position, move along the less crowded axis
                                dx = 1 if overlap_x <= overlap_y else 0
                                dy = 0 if overlap_x <= overlap_y else 1
                            
                            # Move elem2 away
                            new_x = x2 + dx * shift
                            new_y = y2 + dy * shift
                            
                            # Keep within canvas bounds (30-570 x 20-380)
                            elem2['x'] = max(30, min(570, new_x))
                            elem2['y'] = max(20, min(380, new_y))
                            
                            _safe_log(f"[Whiteboard] Moved {elem2.get('id')} to ({elem2['x']}, {elem2['y']})")
            
            return draw_steps
        except Exception as e:
            _safe_log(f"[Whiteboard] Error fixing overlaps: {e}")
            return draw_steps

    async def _auto_suggest_resource(self, preferred_resource_type: str = None):
        """Automatically suggest a resource based on conversation context."""
        try:
            _safe_log(f"[Auto Suggest] Starting resource suggestion...")
            
            # Reload resources fresh from DB to get latest updates
            if self.current_lesson_id:
                await self._load_lesson_resources(self.current_lesson_id)
            elif not self.lesson_resources:
                supabase = get_supabase()
                result = supabase.table("lesson_resources")\
                    .select("*")\
                    .order("order_index")\
                    .execute()
                self.lesson_resources = result.data if result.data else []
                _safe_log(f"[Auto Suggest] Fallback loaded {len(self.lesson_resources)} resources without lesson_id")
            
            if not self.lesson_resources:
                _safe_log(f"[Auto Suggest] No resources available for this lesson")
                return
            
            _safe_log(f"[Auto Suggest] Available resources: {len(self.lesson_resources)}")
            
            # Get recent conversation context (last AI response + last student input)
            recent_texts = []
            for msg in self.conversation_history[-4:]:
                recent_texts.append(msg.get('content', ''))
            combined_text = " ".join(recent_texts).lower()
            _safe_log(f"[Auto Suggest] Context text length: {len(combined_text)} chars")
            
            target_resource_type = preferred_resource_type or resource_decision_service.choose_resource_type(
                phase=self.current_phase,
                lesson_title=self.session_context.get("lesson_title", ""),
                objective=self.session_context.get("objective", ""),
                proficiency=self.session_context.get("proficiency", "intermédiaire"),
                available_resource_types=self._available_resource_types(),
                recent_modes=self.recent_resource_modes,
                simulation_active=bool(self.simulation_state.get("id")),
            )
            
            # For simulations, allow legacy /media/ paths (local HTML files may still work)
            # For images/videos, strict filter to avoid broken legacy paths
            if target_resource_type == 'simulation':
                candidate_resources = [
                    r for r in self.lesson_resources 
                    if r.get('resource_type') == target_resource_type
                    and (r.get('file_path') or r.get('external_url'))
                ]
            else:
                candidate_resources = [
                    r for r in self.lesson_resources 
                    if r.get('resource_type') == target_resource_type
                    and (r.get('file_path') or r.get('external_url'))
                    and not (r.get('file_path') or '').startswith('/media/')
                ]

            if not candidate_resources and preferred_resource_type:
                _safe_log(f"[Auto Suggest] No valid {preferred_resource_type} resources found, falling back to image")
                target_resource_type = 'image'
                candidate_resources = [
                    r for r in self.lesson_resources 
                    if r.get('resource_type') == 'image'
                    and (r.get('file_path') or r.get('external_url'))
                    and not (r.get('file_path') or '').startswith('/media/')
                ]
            
            if not candidate_resources:
                _safe_log(f"[Auto Suggest] No valid {target_resource_type} resources found")
                return
            
            # Score resources by concept match
            best_resource = None
            best_score = -1
            for resource in candidate_resources:
                score = 0
                title = (resource.get('title') or '').lower()
                description = (resource.get('description') or '').lower()
                concepts = resource.get('concepts', []) or []
                
                # Check concept matches
                for concept in concepts:
                    if concept.lower() in combined_text:
                        score += 3
                
                # Check title keywords in context
                for word in title.split():
                    if len(word) > 3 and word in combined_text:
                        score += 2
                
                # Check description keywords
                for word in description.split():
                    if len(word) > 3 and word in combined_text:
                        score += 1
                
                if score > best_score:
                    best_score = score
                    best_resource = resource
            
            if best_resource:
                _safe_log(f"[Auto Suggest] Best match: {best_resource.get('title')} (score: {best_score})")
                await self._display_resource(best_resource)
            else:
                # Fallback: show first resource of the preferred type
                _safe_log(f"[Auto Suggest] No concept match, showing first {target_resource_type}")
                await self._display_resource(candidate_resources[0])
                
        except Exception as e:
            _safe_log(f"[Auto Suggest] ERROR: {str(e)}")
            import traceback
            traceback.print_exc()

    async def _display_resource(self, resource: dict):
        """Display a resource to the student."""
        import time
        
        resource_type = resource.get('resource_type')
        file_path = resource.get('file_path')
        title = resource.get('title', '')
        description = resource.get('description', '')
        
        _safe_log(f"[Display Resource] Attempting to display: {title}")
        _safe_log(f"[Display Resource] Type: {resource_type}, Path: {file_path}")
        
        if not file_path and not resource.get('external_url'):
            _safe_log(f"[Display Resource] No file_path or external_url for {title}")
            return
        
        url = file_path or resource.get('external_url')
        
        # Handle 'local:metadata' — simulation HTML stored in the metadata column
        if url == 'local:metadata':
            import urllib.parse
            metadata = resource.get('metadata', {})
            html_content = metadata.get('html') or metadata.get('content') or metadata.get('simulation_html', '')
            if html_content:
                url = 'data:text/html;charset=utf-8,' + urllib.parse.quote(html_content, safe='')
                _safe_log(f"[Display Resource] Built data:text/html URL from metadata ({len(html_content)} chars)")
            else:
                _safe_log(f"[Display Resource] ERROR: file_path is 'local:metadata' but no HTML found in metadata keys: {list(metadata.keys())}")
                return
        
        if url.startswith('/media/'):
            _safe_log(f"[Display Resource] ERROR: Trying to display legacy local path: {url}")
            _safe_log(f"[Display Resource] Resource ID: {resource.get('id')}")
            _safe_log(f"[Display Resource] This resource needs to be re-uploaded to Supabase Storage")
        
        # Add cache-busting timestamp to force fresh reload of images
        # This prevents browser/CDN from serving stale cached versions
        if url.startswith('data:'):
            url_with_cache_buster = url
        elif '?' in url:
            cache_buster = f"&_t={int(time.time())}"
            url_with_cache_buster = url + cache_buster
        else:
            cache_buster = f"?_t={int(time.time())}"
            url_with_cache_buster = url + cache_buster
        
        _safe_log(f"[Display Resource] URL with cache buster: {url_with_cache_buster}")
        
        if resource_type == 'image':
            await self.websocket.send_json({
                "type": "show_media",
                "media": {
                    "type": "image",
                    "url": url_with_cache_buster,
                    "caption": title,
                    "trigger": description
                }
            })
            self._remember_mode("image")
        elif resource_type == 'video':
            await self.websocket.send_json({
                "type": "show_media",
                "media": {
                    "type": "video",
                    "url": url_with_cache_buster,
                    "caption": title
                }
            })
            self._remember_mode("video")
        elif resource_type == 'simulation':
            await self.websocket.send_json({
                "type": "show_media",
                "media": {
                    "type": "simulation",
                    "url": url,
                    "caption": title
                }
            })
            self._remember_mode("simulation")
        elif resource_type == 'exam':
            await self.websocket.send_json({
                "type": "show_exam",
                "exam_url": url,
                "title": title,
                "description": description
            })
            self._remember_mode("exam")
        
        _safe_log(f"[Resources] Displayed {resource_type}: {title}")

    async def _handle_simulation_manifest(self, message: dict):
        """Handle simulation manifest — learn about ANY simulation's capabilities."""
        simulation_id = message.get('simulation_id', 'unknown')
        capabilities = message.get('capabilities', {})
        page_text = message.get('page_text', '')

        self.simulation_orchestration[simulation_id] = {
            'manifest': {
                'id': simulation_id,
                'capabilities': capabilities,
                'page_text': page_text,
            },
            'states_seen': [],
            'state_results': {},
            'step_count': 0,
            'finalized': False,
            # ---- STATE MACHINE ----
            # Phases: RUNNING_VARIANT | WAITING_STUDENT | EVALUATING | DONE
            'phase': 'RUNNING_VARIANT',
            'current_variant_index': 0,
            'variants_completed': [],
            'student_answers': [],
            'evaluations': [],
        }

        _safe_log(f"[Simulation] Manifest received for '{simulation_id}'")
        _safe_log(f"[Simulation]   globals: {capabilities.get('globals', [])}")
        _safe_log(f"[Simulation]   buttons: {[b.get('text') for b in capabilities.get('buttons', [])]}")
        _safe_log(f"[Simulation]   page_text: {page_text[:120]}...")

        # Automatically start the first variant to kick off orchestration
        orch = self.simulation_orchestration[simulation_id]
        variants = self._get_simulation_variants(orch)
        if variants:
            first = variants[0]
            _safe_log(f"[Simulation] Auto-starting first variant: {first['label']} ({first['command']})")
            await asyncio.sleep(1.5)  # Give iframe time to fully initialize
            await self._send_simulation_control(
                simulation_id, first['command'], first['params'],
                f"Lancement de la simulation: {first['label']}"
            )
            # Also send 'start' if the command was set_variant (need both)
            if first['command'] != 'start':
                await asyncio.sleep(0.5)
                await self._send_simulation_control(simulation_id, 'start', {})
        else:
            _safe_log(f"[Simulation] No variants found, sending generic start")
            await asyncio.sleep(1.0)
            await self._send_simulation_control(simulation_id, 'start', {})

    async def _handle_simulation_update(self, message: dict):
        """Handle simulation state updates — deterministic state machine.
        
        STATE MACHINE PHASES:
        RUNNING_VARIANT  — simulation is animating, ignore intermediate updates
        INTERPRETING     — variant just finished, LLM interprets + asks question
        WAITING_STUDENT  — waiting for student to answer the question
        EVALUATING       — student answered, LLM evaluates the answer
        SWITCHING        — sending command to start the next variant
        DONE             — all variants explored, final summary sent
        """
        simulation_id = message.get('simulation_id', 'unknown')
        student_actions = message.get('student_actions', [])
        current_state = message.get('current_state', {})
        objective_progress = message.get('objective_progress', 0)

        _safe_log(f"[Simulation] Update: {simulation_id} | actions={len(student_actions)} | progress={objective_progress*100:.0f}%")

        self.simulation_state = {
            'id': simulation_id,
            'state': current_state,
            'actions': student_actions,
            'progress': objective_progress
        }

        self.simulation_history.append({
            'timestamp': message.get('timestamp'),
            'actions': student_actions,
            'state': current_state
        })

        # Find the orchestration entry — try exact ID and any stored ID
        orch = self._find_simulation_orch(simulation_id)
        if not orch:
            _safe_log(f"[Simulation] No orchestration found for '{simulation_id}', ignoring")
            return

        orch.setdefault('states_seen', []).append(current_state)
        orch['step_count'] = orch.get('step_count', 0) + 1

        phase = orch.get('phase', 'RUNNING_VARIANT')
        _safe_log(f"[Simulation] Phase={phase} | variant_idx={orch.get('current_variant_index', 0)}")

        # ---- DETECT: has a variant just finished? ----
        # Check simulation_status field (new template) or last action (legacy)
        sim_status = current_state.get('simulation_status', '')
        last_action = student_actions[-1] if student_actions else ''
        if isinstance(last_action, dict):
            last_action = last_action.get('action', str(last_action))

        is_finished = (
            sim_status == 'finished'
            or last_action == 'finish_simulation'
            # Legacy fallback: if state has result-like keys
            or 'atp_produced' in current_state
            or ('pathway' in current_state and 'atp_produced' not in current_state and sim_status != 'running')
        )
        variant_just_finished = is_finished and phase == 'RUNNING_VARIANT'

        if variant_just_finished:
            # Store this variant's results
            variant_idx = orch.get('current_variant_index', 0)
            orch['state_results'][variant_idx] = current_state.copy()
            orch['variants_completed'].append(current_state.copy())
            orch['phase'] = 'INTERPRETING'
            _safe_log(f"[Simulation] Variant {variant_idx} finished! Interpreting...")

            # Determine variant info for LLM
            await self._sim_interpret_and_ask(orch, simulation_id, current_state)

    def _find_simulation_orch(self, simulation_id: str):
        """Find orchestration entry, handling ID mismatches."""
        if simulation_id in self.simulation_orchestration:
            return self.simulation_orchestration[simulation_id]
        # Try to find any orchestration entry (there should be only one active)
        for orch_id, orch in self.simulation_orchestration.items():
            if orch.get('manifest'):
                # Link this simulation_id to the existing entry
                _safe_log(f"[Simulation] Linking '{simulation_id}' to existing orch '{orch_id}'")
                self.simulation_orchestration[simulation_id] = orch
                return orch
        return None

    # ---------------------------------------------------------------------------
    # DETERMINISTIC STATE MACHINE ORCHESTRATION
    # Backend controls the flow — LLM is only used for text generation
    # ---------------------------------------------------------------------------

    def _get_simulation_variants(self, orch: dict) -> list:
        """Determine the variants to explore based on manifest capabilities.
        
        Priority:
        1. SIMULATION_CONFIG.variants from manifest (new template)
        2. Button pattern detection (O2 / simulate)
        3. Generic fallback
        """
        caps = orch.get('manifest', {}).get('capabilities', {})
        config = caps.get('config', {})
        buttons = caps.get('buttons', [])
        globals_list = caps.get('globals', [])

        # ── 1) New template: SIMULATION_CONFIG.variants declared ──
        config_variants = config.get('variants', [])
        if config_variants:
            result = []
            for v in config_variants:
                result.append({
                    'label': v.get('label', v.get('id', 'Variante')),
                    'command': 'set_variant',
                    'params': {'variant_id': v.get('id')},
                })
            if result:
                _safe_log(f"[Simulation] Using SIMULATION_CONFIG variants: {[v['label'] for v in result]}")
                return result

        # ── 2) Button pattern: O2/No-O2 ──
        button_texts = ' '.join((b.get('text', '') + ' ' + (b.get('className', ''))) for b in buttons).lower()
        if 'o2' in button_texts or 'oxygène' in button_texts or 'oxygen' in button_texts:
            return [
                {'label': 'Respiration aérobie (avec O₂)', 'command': 'set_oxygen', 'params': {'oxygen_present': True}},
                {'label': 'Fermentation (sans O₂)', 'command': 'set_oxygen', 'params': {'oxygen_present': False}},
            ]

        # ── 3) Global function: simulate(bool) ──
        if 'simulate' in globals_list:
            return [
                {'label': 'Condition 1', 'command': 'call_function', 'params': {'name': 'simulate', 'args': [True]}},
                {'label': 'Condition 2', 'command': 'call_function', 'params': {'name': 'simulate', 'args': [False]}},
            ]

        # ── 4) Multiple buttons → one variant per button ──
        if len(buttons) >= 2:
            result = []
            for i, b in enumerate(buttons):
                btn_text = (b.get('text', '') or '').strip()
                if not btn_text or btn_text.lower() in ('reset', 'réinitialiser', 'pause'):
                    continue
                btn_id = b.get('id')
                if btn_id:
                    result.append({'label': btn_text, 'command': 'click_button', 'params': {'id': btn_id}})
                else:
                    result.append({'label': btn_text, 'command': 'click_button', 'params': {'selector': f'button:nth-child({i+1})'}})
            if result:
                return result

        # ── 5) Fallback: just start ──
        return [
            {'label': 'Simulation', 'command': 'start', 'params': {}},
        ]

    async def _sim_interpret_and_ask(self, orch: dict, simulation_id: str, state: dict):
        """After a variant finishes: LLM interprets results + asks a question. Then WAIT."""
        variant_idx = orch.get('current_variant_index', 0)
        variants = self._get_simulation_variants(orch)
        variant_label = variants[variant_idx]['label'] if variant_idx < len(variants) else f'Variante {variant_idx+1}'
        
        state_summary = ', '.join(f"{k}={v}" for k, v in state.items()) if state else 'état initial'
        ctx = self.session_context

        prompt = f"""Tu es un tuteur IA en {ctx.get('subject', 'Sciences')} pour un élève de 2ème BAC.
Leçon: {ctx.get('lesson_title', '')}
Objectif: {ctx.get('objective', '')}

La simulation vient de terminer la variante: {variant_label}
Résultats observés: {state_summary}

CONSIGNE: 
1. Explique en 2-3 phrases ce que l'élève vient d'observer scientifiquement. 
2. Relie au cours.
3. Pose UNE question de compréhension à l'élève sur ce qu'il vient de voir.

IMPORTANT: Sois concis. Parle en français. Termine par ta question."""

        try:
            ai_text = await llm_service.chat(
                messages=[{"role": "user", "content": prompt}],
                system_prompt="Tu es un tuteur scientifique bienveillant. Sois concis et clair.",
                max_tokens=300,
            )
        except Exception as e:
            _safe_log(f"[Simulation] LLM error in interpret: {e}")
            ai_text = f"Nous venons d'observer les résultats de {variant_label}. Qu'as-tu remarqué ?"

        # Send to student
        self.conversation_history.append({"role": "assistant", "content": ai_text})
        await self.websocket.send_json({"type": "ai_response", "text": ai_text})
        asyncio.create_task(self.generate_and_send_audio_chunks(ai_text))

        # Switch phase to WAITING_STUDENT
        orch['phase'] = 'WAITING_STUDENT'
        _safe_log(f"[Simulation] Phase → WAITING_STUDENT (waiting for student answer)")

    async def handle_simulation_student_answer(self, student_text: str):
        """Called when student sends text while simulation is in WAITING_STUDENT phase.
        Returns True if the answer was handled by simulation orchestration."""
        # Find active simulation orchestration
        active_orch = None
        active_sim_id = None
        for sim_id, orch in self.simulation_orchestration.items():
            if orch.get('phase') == 'WAITING_STUDENT':
                active_orch = orch
                active_sim_id = sim_id
                break

        if not active_orch:
            return False  # No simulation waiting — let normal chat handle it

        _safe_log(f"[Simulation] Student answered while WAITING_STUDENT: '{student_text[:80]}...'")
        active_orch['student_answers'].append(student_text)
        active_orch['phase'] = 'EVALUATING'

        # LLM evaluates the student's answer
        variant_idx = active_orch.get('current_variant_index', 0)
        variant_state = active_orch.get('state_results', {}).get(variant_idx, {})
        variants = self._get_simulation_variants(active_orch)
        variant_label = variants[variant_idx]['label'] if variant_idx < len(variants) else f'Variante {variant_idx+1}'
        
        state_summary = ', '.join(f"{k}={v}" for k, v in variant_state.items()) if variant_state else ''
        ctx = self.session_context

        prompt = f"""Tu es un tuteur IA en {ctx.get('subject', 'Sciences')}.
Leçon: {ctx.get('lesson_title', '')}

Variante simulée: {variant_label}
Résultats: {state_summary}

L'élève a répondu: "{student_text}"

CONSIGNE: 
1. Évalue brièvement si la réponse de l'élève est correcte (2 phrases max).
2. Si incorrect, corrige gentiment.
3. Annonce que tu passes à la variante suivante (ou au bilan si c'est la dernière).

Sois concis. Parle en français."""

        try:
            eval_text = await llm_service.chat(
                messages=[{"role": "user", "content": prompt}],
                system_prompt="Tu es un tuteur bienveillant. Évalue la réponse de l'élève de manière constructive.",
                max_tokens=250,
            )
        except Exception as e:
            _safe_log(f"[Simulation] LLM error in evaluate: {e}")
            eval_text = "Merci pour ta réponse ! Passons à la suite."

        active_orch['evaluations'].append(eval_text)

        # Send evaluation to student
        self.conversation_history.append({"role": "assistant", "content": eval_text})
        await self.websocket.send_json({"type": "ai_response", "text": eval_text})
        asyncio.create_task(self.generate_and_send_audio_chunks(eval_text))

        # Move to next variant or final summary
        next_idx = variant_idx + 1
        if next_idx < len(variants):
            # Switch to next variant
            active_orch['current_variant_index'] = next_idx
            active_orch['phase'] = 'SWITCHING'
            _safe_log(f"[Simulation] Phase → SWITCHING to variant {next_idx}")

            # Wait a bit then send the switch command + start
            await asyncio.sleep(2.0)
            next_variant = variants[next_idx]
            await self._send_simulation_control(
                active_sim_id,
                next_variant['command'],
                next_variant['params'],
                f"Passons à: {next_variant['label']}"
            )

            # The switch command (click_button, set_oxygen, etc.) only changes
            # parameters — we must also send 'start' to actually run the animation
            if next_variant['command'] != 'start':
                await asyncio.sleep(0.8)
                await self._send_simulation_control(
                    active_sim_id, 'start', {},
                    None  # no extra guidance text
                )
                _safe_log(f"[Simulation] Sent 'start' after variant switch")

            active_orch['phase'] = 'RUNNING_VARIANT'
            _safe_log(f"[Simulation] Phase → RUNNING_VARIANT (variant {next_idx})")
        else:
            # All variants done — final summary
            active_orch['phase'] = 'DONE'
            _safe_log(f"[Simulation] All variants done! Generating final summary...")
            await self._sim_final_summary(active_orch, active_sim_id)

        return True

    async def _sim_final_summary(self, orch: dict, simulation_id: str):
        """Generate final formative evaluation after all variants explored."""
        ctx = self.session_context
        variants = self._get_simulation_variants(orch)

        results_summary = ""
        for i, state in enumerate(orch.get('variants_completed', [])):
            label = variants[i]['label'] if i < len(variants) else f'Variante {i+1}'
            state_str = ', '.join(f"{k}={v}" for k, v in state.items())
            results_summary += f"\n- {label}: {state_str}"

        answers_summary = ""
        for i, ans in enumerate(orch.get('student_answers', [])):
            answers_summary += f"\n- Réponse {i+1}: \"{ans}\""

        evals_summary = "\n".join(orch.get('evaluations', []))

        prompt = f"""Tu es un tuteur IA en {ctx.get('subject', 'Sciences')}.
Leçon: {ctx.get('lesson_title', '')}
Objectif: {ctx.get('objective', '')}

L'élève vient de terminer une simulation interactive. Voici le récap:

RÉSULTATS DES VARIANTES SIMULÉES: {results_summary}

RÉPONSES DE L'ÉLÈVE: {answers_summary}

ÉVALUATIONS INTERMÉDIAIRES:
{evals_summary}

CONSIGNE: Produis une ÉVALUATION FORMATIVE FINALE:
1. Résumé comparatif des résultats (2-3 phrases)
2. Bilan de compréhension de l'élève basé sur ses réponses verbales
3. Note sur 20 basée UNIQUEMENT sur la qualité des réponses de l'élève (pas sur la simulation)
4. Points forts et points à améliorer
5. Conseil pour la suite

Sois bienveillant mais rigoureux. Parle en français."""

        try:
            summary = await llm_service.chat(
                messages=[{"role": "user", "content": prompt}],
                system_prompt="Tu es un tuteur qui produit des bilans formatifs clairs et motivants.",
                max_tokens=500,
            )
        except Exception as e:
            _safe_log(f"[Simulation] LLM error in final summary: {e}")
            summary = "Bravo pour avoir complété la simulation ! Tu as bien progressé."

        self.conversation_history.append({"role": "assistant", "content": summary})
        await self.websocket.send_json({"type": "ai_response", "text": summary})
        asyncio.create_task(self.generate_and_send_audio_chunks(summary))
        orch['finalized'] = True

    async def _send_simulation_control(self, simulation_id: str, command: str, parameters: dict = None, guidance_text: str = None):
        """Send control command to any simulation."""
        msg = {
            "type": "simulation_control",
            "simulation_id": simulation_id,
            "command": command,
            "parameters": parameters or {},
            "guidance_text": guidance_text
        }
        await self.websocket.send_json(msg)
        _safe_log(f"[Simulation Control] Sent {command} to {simulation_id} params={parameters}")

    # _generate_opening is now inlined in _init_session with streaming support
