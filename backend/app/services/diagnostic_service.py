"""
Diagnostic Service
Generates and evaluates diagnostic/formative assessments.
Uses RAG from cadres de référence to align questions with official BAC program.
"""
from typing import Optional
from app.supabase_client import get_supabase_admin
from app.services.llm_service import llm_service
from app.services.rag_service import get_rag_service
import uuid
import json
import re


# Match a backslash NOT followed by a valid JSON escape character.
# Valid JSON escapes: \" \\ \/ \b \f \n \r \t \uXXXX
_INVALID_ESCAPE_RE = re.compile(r'\\(?!["\\/bfnrtu])')


def _safe_json_loads(raw: str) -> dict | list:
    """Parse JSON, tolerant to LaTeX-style stray backslashes (\\frac, \\pi, …)
    that the LLM occasionally emits inside string values.
    Tries strict parse first; on InvalidEscape error, escapes lone backslashes
    and retries once.
    """
    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        if "Invalid \\escape" not in str(e) and "Invalid escape" not in str(e):
            raise
        # Escape any backslash that isn't part of a valid JSON escape sequence
        fixed = _INVALID_ESCAPE_RE.sub(r'\\\\', raw)
        return json.loads(fixed)


class DiagnosticService:
    # Shared instruction injected into every question-generation prompt so
    # all math/physics/chem formulas are emitted as LaTeX (rendered by
    # <LatexRenderer> on the frontend) instead of ASCII placeholders.
    _MATH_FORMAT_INSTRUCTION = r"""

⚠️ FORMATAGE MATHÉMATIQUE OBLIGATOIRE (Physique / Chimie / Maths) :
Écris TOUTES les formules, grandeurs, équations et unités en LaTeX entre $...$ (inline) ou $$...$$ (bloc).
Exemples CORRECTS :
  - Dérivée : $\frac{du_C}{dt}$   (pas "du_C/dt")
  - Fraction : $\frac{1}{RC}$     (pas "(1/RC)" ou "1/RC")
  - Indice / exposant : $u_C$, $x^2$, $e^{-t/\tau}$, $\mathrm{H}_2\mathrm{O}$
  - Vecteurs : $\vec{F}$, $\vec{v}$
  - Unités : $\Omega$, $\mu\mathrm{F}$, $\mathrm{m \cdot s^{-1}}$, $^{\circ}\mathrm{C}$
  - Équation différentielle : $\frac{du_C}{dt} + \frac{1}{RC}\, u_C = 0$
  - Loi / relation : $U = R \cdot I$, $E = \frac{1}{2} C u^2$, $pH = -\log[\mathrm{H_3O^+}]$
  - Racine, intégrale, somme : $\sqrt{2}$, $\int_0^T f(t)\,dt$, $\sum_{i=1}^n x_i$
Les **options A/B/C/D** DOIVENT aussi utiliser ce formatage LaTeX (pas de "du_C/dt", toujours $\frac{du_C}{dt}$).
Le texte narratif (non mathématique) reste en français normal, hors $...$.
"""

    def __init__(self):
        self.supabase = get_supabase_admin()
        # Store ongoing diagnostic sessions for question-by-question generation
        self._sessions: dict[str, dict] = {}  # session_id -> {subject_id, questions_generated, total_questions, chapter_context, etc.}

    # Subject disambiguation: domain keywords unique to Physique vs Chimie.
    # Used post-generation to drop questions that leaked from the wrong subject
    # (e.g. a Chimie pile question produced during a Physique diagnostic).
    _CHIMIE_KEYWORDS = (
        "acide", "base", " ph ", "dosage", "titrage", "pka", "ka ", "kb ",
        "pile", "électrode", "electrode", "électrolyse", "electrolyse",
        "estérification", "esterification", "hydrolyse", "ester ", "estérique",
        "cinétique", "cinetique chimique", "réaction chimique", "reaction chimique",
        "concentration", "molaire", "conductivité", "conductivite", "équilibre chimique",
        "equilibre chimique", "quotient de réaction", "avancement",
    )
    _PHYSIQUE_KEYWORDS = (
        "newton", "vitesse", "accélération", "acceleration", "accélere",
        "mécanique", "mecanique", "masse ", "gravitation", "chute libre",
        "pendule", "satellite", "oscillateur",
        "onde", "diffraction", "interférence", "interference", "longueur d'onde",
        "rlc ", "rl ", "rc ", "bobine", "condensateur", "oscillation",
        "nucléaire", "nucleaire", "radioactiv", "désintégration", "desintegration",
        "energie cinetique", "énergie cinétique", "forces", "moment d'inertie",
    )

    def _question_fits_subject(self, q: dict, subject_name: str) -> bool:
        """Return True if the question content is compatible with the subject.

        Only tries to catch obvious Physique ↔ Chimie leaks (since they share
        the BIOF exam paper). Math / SVT don't need this check.
        """
        s = (subject_name or "").lower().replace("é", "e")
        if s not in ("physique", "chimie"):
            return True

        text = " ".join([
            str(q.get("question", "")),
            str(q.get("topic", "")),
            str(q.get("domain", "")),
        ]).lower()
        if not text.strip():
            return True

        chimie_hits = sum(1 for kw in self._CHIMIE_KEYWORDS if kw in text)
        physique_hits = sum(1 for kw in self._PHYSIQUE_KEYWORDS if kw in text)

        if s == "physique" and chimie_hits >= 2 and physique_hits == 0:
            return False
        if s == "chimie" and physique_hits >= 2 and chimie_hits == 0:
            return False
        return True

    def _clean_question_text(self, text: str) -> str:
        """Clean question text by replacing problematic Unicode chars with readable alternatives."""
        if not text:
            return text
        # Replace combining characters (vector arrows, etc.)
        # ⃗ (combining right arrow above) is U+20D7
        cleaned = text.replace('\u20d7', '')  # Remove combining arrow
        # Replace other problematic chars with LaTeX-style notation
        cleaned = cleaned.replace('F⃗', '\\vec{F}')
        cleaned = cleaned.replace('u⃗', '\\vec{u}')
        cleaned = cleaned.replace('n⃗', '\\vec{n}')
        cleaned = cleaned.replace('v⃗', '\\vec{v}')
        cleaned = cleaned.replace('a⃗', '\\vec{a}')
        # Clean up multiple spaces
        cleaned = ' '.join(cleaned.split())
        return cleaned

    # Markdown table separator row pattern: '|---|---|' (with optional spaces / colons).
    _MD_TABLE_SEP_RE = re.compile(r'\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|')

    def _strip_markdown_table(self, text: str) -> str:
        """Remove Markdown-table noise that the LLM sometimes copies verbatim
        from a BAC source. Keeps the rest of the sentence readable.

        Strategy:
          1) Drop the separator line ``|---|---|---|`` entirely.
          2) Replace any remaining pipe-cell run by a single space.
          3) Collapse runs of whitespace.
        """
        if not text or '|' not in text:
            return text
        cleaned = self._MD_TABLE_SEP_RE.sub(' ', text)
        # Replace pipe-cell sequences (e.g. " | a | b | c | ") with a space.
        cleaned = re.sub(r'(\s*\|\s*[^|\n]{1,40})+\s*\|', ' ', cleaned)
        cleaned = re.sub(r'\s{2,}', ' ', cleaned).strip()
        return cleaned
    
    def _get_subject_rag_context(self, subject_name: str) -> str:
        """Get RAG context from cadres de référence for a specific subject."""
        try:
            rag = get_rag_service()
            return rag.get_subject_program_context(subject_name)
        except Exception as e:
            print(f"[Diagnostic] RAG context error for {subject_name}: {e}")
            return ""

    def _get_chapter_course_excerpts(
        self,
        subject_name: str,
        chapter_title: str,
        n: int = 3,
    ) -> list[dict]:
        """Pull up to ``n`` COURSE chunks (lessons, not exams) for the target
        chapter, used to ground question generation in the indexed course PDFs.

        Returns a list of ``{text, source, page}`` dicts (text already truncated).
        """
        if not chapter_title:
            return []
        try:
            rag = get_rag_service()
            # Over-fetch then filter — search() doesn't filter by subject server-side.
            hits = rag.search(chapter_title, top_k=20)
            subj_lower = (subject_name or "").lower()
            picked: list[dict] = []
            seen_sources: set[str] = set()
            for h in hits:
                # Drop exam questions and the cadre de référence — keep only lessons/courses.
                if h.get("doc_type") in ("exam", "cadre_reference"):
                    continue
                # Subject filter: tolerant match (Physique-Chimie ≈ Physique ≈ Chimie).
                doc_subj = (h.get("subject") or "").lower()
                if subj_lower and doc_subj:
                    if subj_lower not in doc_subj and doc_subj not in subj_lower:
                        # Allow Physique-Chimie source for Physique or Chimie subject.
                        if not (("physique" in doc_subj and "chimie" in doc_subj)
                                and (subj_lower in ("physique", "chimie"))):
                            continue
                # Avoid stacking 3 chunks from the same source page.
                key = f"{h.get('source', '')}::{h.get('page', '')}"
                if key in seen_sources:
                    continue
                seen_sources.add(key)
                text = (h.get("text") or "").strip()
                if len(text) < 60:  # too short to be useful
                    continue
                picked.append({
                    "text": text[:500],  # truncate to keep prompt budget
                    "source": h.get("source", ""),
                    "page": h.get("page", ""),
                })
                if len(picked) >= n:
                    break
            return picked
        except Exception as e:
            print(f"[Diagnostic] Course excerpt error for {subject_name}/{chapter_title}: {e}")
            return []

    def _get_tested_concepts(
        self,
        student_id: str,
        subject_id: str,
        last_n: int = 5,
    ) -> tuple[list[str], list[str]]:
        """Extract all topics/concepts already tested in the student's last N diagnostics.

        Returns (tested_topics, sample_question_heads) where
          tested_topics  — every distinct question.topic + question.domain value
          sample_question_heads — first 100 chars of each past question, for dedup hints
        """
        history = self.supabase.table('diagnostic_results').select(
            'questions_data'
        ).eq(
            'student_id', student_id
        ).eq(
            'subject_id', subject_id
        ).eq(
            'evaluation_type', 'diagnostic'
        ).order(
            'created_at', desc=True
        ).limit(last_n).execute()

        topics: set[str] = set()
        q_heads: list[str] = []
        for row in history.data or []:
            for q in row.get('questions_data') or []:
                for key in ('topic', 'domain', 'chapter_title'):
                    v = (q.get(key) or '').strip()
                    if v:
                        topics.add(v.lower())
                head = (q.get('question') or '')[:100].strip()
                if head:
                    q_heads.append(head)
        return sorted(topics), q_heads

    async def start_diagnostic_session(
        self,
        subject_id: str,
        num_questions: int = 10,
        student_id: Optional[str] = None,
    ) -> str:
        """
        Start a diagnostic session for question-by-question generation.
        Returns a session_id that can be used to generate questions one by one.

        Args:
            subject_id: Subject UUID
            num_questions: Total number of questions to generate
            student_id: Student UUID for anti-repetition

        Returns:
            session_id: UUID for the diagnostic session
        """
        # Get subject info
        subject_result = self.supabase.table('subjects').select(
            'name_fr, name_ar'
        ).eq('id', subject_id).execute()

        if not subject_result.data:
            raise Exception("Subject not found")

        subject_name = subject_result.data[0]['name_fr']

        # Get ALL chapters with their lessons and learning objectives
        chapters_result = self.supabase.table('chapters').select(
            'id, title_fr, chapter_number, lessons(id, title_fr, learning_objectives)'
        ).eq('subject_id', subject_id).order('order_index').execute()

        # Build detailed chapter info with key concepts
        chapters_info = []
        for chapter in (chapters_result.data if chapters_result.data else []):
            chapter_data = {
                'title': chapter['title_fr'],
                'number': chapter.get('chapter_number', 0),
                'key_concepts': []
            }

            if chapter.get('lessons'):
                for lesson in chapter['lessons']:
                    if lesson.get('learning_objectives'):
                        objectives = lesson['learning_objectives']
                        if isinstance(objectives, list):
                            chapter_data['key_concepts'].extend(objectives)
                        elif isinstance(objectives, str):
                            chapter_data['key_concepts'].append(objectives)

            chapters_info.append(chapter_data)

        # Build chapter context for LLM
        chapters_context = ""
        for ch in chapters_info:
            chapters_context += f"\n\n**Chapitre {ch['number']}: {ch['title']}**\n"
            if ch['key_concepts']:
                chapters_context += "Points cruciaux à tester:\n"
                for concept in ch['key_concepts'][:3]:
                    chapters_context += f"  - {concept}\n"

        # Get RAG context
        rag_context = self._get_subject_rag_context(subject_name)

        # Get tested concepts for anti-repetition
        tested_topics: list[str] = []
        previous_q_heads: list[str] = []
        if student_id:
            tested_topics, previous_q_heads = self._get_tested_concepts(
                student_id, subject_id, last_n=5
            )

        # ── Build weighted question plan: how many questions per chapter ──
        # Uses cadre-de-référence domain weights → distributed across chapters.
        chapter_weights = self._extract_chapter_weights(subject_name, chapters_info)
        print(f"[Diagnostic] {subject_name} chapter weights: {chapter_weights or '(fallback equal distribution)'}")

        # Distribute num_questions across chapters proportionally to weights
        question_plan = self._build_question_plan(
            chapters_info, chapter_weights, num_questions
        )
        plan_summary = [(ch.get('number'), ch.get('title', '')[:40]) for ch in question_plan]
        print(f"[Diagnostic] {subject_name} question plan ({num_questions} Q): {plan_summary}")

        # Create session
        session_id = str(uuid.uuid4())
        self._sessions[session_id] = {
            'subject_id': subject_id,
            'subject_name': subject_name,
            'num_questions': num_questions,
            'student_id': student_id,
            'questions_generated': 0,
            'generated_questions': [],
            'generated_question_heads': [],  # for strong anti-repetition
            'chapters_context': chapters_context,
            'rag_context': rag_context,
            'tested_topics': tested_topics,
            'previous_q_heads': previous_q_heads,
            'chapters_info': chapters_info,
            'question_plan': question_plan,  # ordered list of chapters to target
            'plan_cursor': 0,
        }

        return session_id

    def _extract_chapter_weights(self, subject_name: str, chapters_info: list) -> dict:
        """Map cadre-de-référence DOMAIN weights → per-chapter weights.

        Uses the structured ``rag.get_exam_weights_data()`` dump (already parsed
        from the official 'cadres de référence' PDFs) and matches each chapter
        title against a domain keyword set. Domain weight is then divided
        equally across the chapters that map to it.

        Returns ``{chapter_number: relative_weight_int}`` or ``{}`` if nothing
        could be extracted — in which case ``_build_question_plan`` falls back
        to an equal distribution.
        """
        try:
            rag = get_rag_service()
            weights_data = rag.get_exam_weights_data() or {}
        except Exception as e:
            print(f"[Diagnostic] get_exam_weights_data failed: {e}")
            return {}

        if not weights_data:
            return {}

        # Pick the right subject bucket(s).
        sl = (subject_name or "").lower()
        candidates: list[dict] = []
        if 'physique-chimie' in sl or sl in ('pc', 'physique chimie'):
            candidates += [weights_data.get('Physique') or {}, weights_data.get('Chimie') or {}]
        elif 'physique' in sl:
            candidates.append(weights_data.get('Physique') or {})
        elif 'chimie' in sl:
            candidates.append(weights_data.get('Chimie') or {})
        elif 'svt' in sl or 'biologie' in sl or 'vie' in sl:
            candidates.append(weights_data.get('SVT') or {})
        elif 'math' in sl:
            candidates.append(weights_data.get('Mathématiques') or {})

        # Flatten domain → raw-weight string across candidates.
        domain_weights: dict[str, float] = {}
        for bucket in candidates:
            for dname, raw in (bucket.get('domains') or {}).items():
                m = re.search(r'(\d+(?:[\.,]\d+)?)', str(raw))
                if m:
                    try:
                        domain_weights[dname] = float(m.group(1).replace(',', '.'))
                    except ValueError:
                        continue

        if not domain_weights:
            return {}

        # Stop-words we don't want to count in fuzzy keyword matching.
        _STOP = {"de", "la", "le", "les", "du", "des", "et", "à", "au", "aux",
                 "un", "une", "d", "l", "en", "dans", "sur"}

        def _kw(s: str) -> list[str]:
            return [w for w in re.findall(r"[\wÀ-ÿ]+", (s or "").lower())
                    if len(w) > 3 and w not in _STOP]

        # First pass: find best domain per chapter.
        chapter_to_domain: dict[int, str] = {}
        for ch in chapters_info:
            ch_title = ch.get('title', '')
            ch_num = ch.get('number')
            if ch_num is None:
                continue
            title_kw = _kw(ch_title)
            best_domain: str | None = None
            best_score = 0
            for dname in domain_weights:
                d_kw = _kw(dname)
                if not d_kw:
                    continue
                score = sum(1 for w in d_kw if w in title_kw)
                if score > best_score:
                    best_score, best_domain = score, dname
            if best_domain:
                chapter_to_domain[ch_num] = best_domain

        if not chapter_to_domain:
            return {}

        # Second pass: divide each domain's weight across the chapters that mapped to it.
        domain_chapter_count: dict[str, int] = {}
        for d in chapter_to_domain.values():
            domain_chapter_count[d] = domain_chapter_count.get(d, 0) + 1

        weights: dict = {}
        for ch_num, dname in chapter_to_domain.items():
            per_chapter = domain_weights[dname] / max(1, domain_chapter_count[dname])
            weights[ch_num] = max(1, int(round(per_chapter)))

        # Unmapped chapters get at least weight=1 so they're not excluded.
        for ch in chapters_info:
            n = ch.get('number')
            if n is not None and n not in weights:
                weights[n] = 1

        return weights

    def _build_question_plan(
        self, chapters_info: list, weights: dict, total: int
    ) -> list:
        """
        Build an ordered list of chapter targets for questions.
        Distributes proportionally to weights; falls back to equal distribution.
        Returns list of chapter dicts (one per question).
        """
        if not chapters_info:
            return []

        n_chapters = len(chapters_info)

        if weights and sum(weights.values()) > 0:
            # Proportional distribution
            total_w = sum(weights.values())
            counts = {}
            for ch in chapters_info:
                num = ch.get('number', 0)
                w = weights.get(num, total_w / n_chapters)
                counts[num] = max(1, round((w / total_w) * total))
        else:
            # Equal distribution
            base = total // n_chapters
            extra = total % n_chapters
            counts = {}
            for i, ch in enumerate(chapters_info):
                num = ch.get('number', i)
                counts[num] = base + (1 if i < extra else 0)

        # Adjust total to exactly match target
        assigned = sum(counts.values())
        while assigned > total:
            # Remove from the chapter with the most questions
            top = max(counts, key=counts.get)
            if counts[top] > 1:
                counts[top] -= 1
                assigned -= 1
            else:
                break
        while assigned < total:
            # Add to the chapter with the fewest questions
            bot = min(counts, key=counts.get)
            counts[bot] += 1
            assigned += 1

        # Build interleaved plan: cycle through chapters so the order is diversified
        plan = []
        remaining = dict(counts)
        while sum(remaining.values()) > 0:
            for ch in chapters_info:
                num = ch.get('number', 0)
                if remaining.get(num, 0) > 0:
                    plan.append(ch)
                    remaining[num] -= 1
                    if len(plan) >= total:
                        break
            if len(plan) >= total:
                break
        return plan[:total]

    async def generate_next_question(
        self,
        session_id: str,
    ) -> Optional[dict]:
        """
        Generate the next question in a diagnostic session.

        Args:
            session_id: Session UUID from start_diagnostic_session

        Returns:
            Question dict or None if all questions generated
        """
        if session_id not in self._sessions:
            raise Exception("Session not found")

        session = self._sessions[session_id]

        if session['questions_generated'] >= session['num_questions']:
            return None

        # ── Rotate question types so each diagnostic has variety ──
        # Pattern over 10 questions: ~5 QCM · ~3 V/F · ~2 association
        # 0,3,5,7,9 -> qcm  | 1,4,8 -> vrai_faux  | 2,6 -> association
        idx = session['questions_generated']
        _type_rotation = {0: 'qcm', 1: 'vrai_faux', 2: 'association',
                          3: 'qcm', 4: 'vrai_faux', 5: 'qcm',
                          6: 'association', 7: 'qcm', 8: 'vrai_faux', 9: 'qcm'}
        target_type = _type_rotation.get(idx % 10, 'qcm')

        # ── Rotate BAC years so the 10 questions don't all come from 2025 ──
        # Cycle through 2025 → 2020 → 2024 → 2021 → 2023 → 2022 → … to ensure
        # at least 4-5 distinct years are represented in one diagnostic.
        _year_rotation = ["2025", "2020", "2024", "2021", "2023", "2022",
                          "2025", "2021", "2024", "2023"]
        preferred_year = _year_rotation[idx % len(_year_rotation)]

        # ── Get target chapter from plan ──
        plan = session.get('question_plan', [])
        plan_cursor = session.get('plan_cursor', 0)
        target_chapter = plan[plan_cursor] if plan_cursor < len(plan) else None

        target_chapter_section = ""
        if target_chapter:
            concepts_list = target_chapter.get('key_concepts', [])[:5]
            concepts_text = "\n".join(f"  • {c}" for c in concepts_list) if concepts_list else "  (concepts fondamentaux du chapitre)"
            target_chapter_section = (
                f"\n\n🎯 CHAPITRE CIBLE OBLIGATOIRE POUR CETTE QUESTION:\n"
                f"  Chapitre {target_chapter.get('number', '?')}: {target_chapter.get('title', '')}\n"
                f"  Concepts à tester (choisis-en UN):\n{concepts_text}\n"
                f"  ⚠️ Ta question DOIT porter sur ce chapitre précisément, pas un autre."
            )

        # Build variation instruction based on already generated questions
        generated_topics = [q.get('topic', '') for q in session['generated_questions']]
        generated_heads = session.get('generated_question_heads', [])
        variation_instruction = ""
        if generated_topics:
            topics_list = "\n".join(f"  - {t}" for t in generated_topics[:20])
            variation_instruction += (
                f"\n\n⚠️ INTERDIT — topics DÉJÀ générés dans cette session:\n{topics_list}\n"
                f"Tu dois OBLIGATOIREMENT choisir un topic DIFFÉRENT."
            )
        if generated_heads:
            heads_list = "\n".join(f"  - \"{h[:120]}...\"" for h in generated_heads[-10:])
            variation_instruction += (
                f"\n\n⚠️ INTERDIT — questions DÉJÀ posées (même reformulées):\n{heads_list}\n"
                f"Ta nouvelle question DOIT être sémantiquement différente."
            )

        # Pull real BAC exam questions for inspiration
        rag = get_rag_service()
        try:
            exam_inspiration = rag.get_exam_inspiration(
                subject=session['subject_name'],
                n=3,
                years=["2020", "2021", "2022", "2023", "2024", "2025"],
                exclude_topics=generated_topics + session['tested_topics'],
                exclude_question_texts=(session['previous_q_heads'] + generated_heads)[:20],
                preferred_year=preferred_year,
            )
        except Exception as e:
            print(f"[Diagnostic] Could not fetch exam inspiration: {e}")
            exam_inspiration = []

        # Build inspiration section — these are REAL BAC questions the LLM must
        # transform/adapt rather than invent from scratch.
        inspiration_section = ""
        primary_bac_year = ""
        if exam_inspiration:
            primary_bac_year = str(exam_inspiration[0].get("year") or "")
            inspiration_section = "\n\n📚 SOURCES BAC RÉELLES (transforme l'une de ces questions en QCM/V-F) :\n"
            for i, ex in enumerate(exam_inspiration, 1):
                head = (ex.get("text") or "")[:280].replace("\n", " ")
                inspiration_section += (
                    f"\n[Source {i} — BAC {ex.get('year')} {ex.get('session') or 'normale'}"
                    + (f", topic: {ex['topic']}" if ex.get('topic') else "")
                    + f"]\n{head}...\n"
                )

        # ── Pull COURSE excerpts for the target chapter (lessons indexed in RAG) ──
        course_section = ""
        if target_chapter and target_chapter.get('title'):
            course_excerpts = self._get_chapter_course_excerpts(
                session['subject_name'],
                target_chapter.get('title', ''),
                n=3,
            )
            if course_excerpts:
                course_section = "\n\n📖 EXTRAITS DU COURS OFFICIEL INDEXÉ (utilise EXACTEMENT ce vocabulaire et ces définitions) :\n"
                for i, ex in enumerate(course_excerpts, 1):
                    src = ex.get("source", "")
                    page = ex.get("page", "")
                    head = ex["text"].replace("\n", " ")
                    course_section += (
                        f"\n[Cours {i} — {src}{f', p.{page}' if page else ''}]\n{head}\n"
                    )

        # Build rag section
        rag_section = ""
        if session['rag_context']:
            rag_section = f"""

CADRE DE RÉFÉRENCE OFFICIEL DU BAC MAROCAIN POUR {session['subject_name'].upper()}:
{session['rag_context']}"""

        # ── Build per-type JSON schema + tailored instructions ──
        chapter_num_value = target_chapter.get('number', 1) if target_chapter else 1
        if target_type == 'vrai_faux':
            type_instruction = (
                "TYPE IMPOSÉ : VRAI / FAUX\n"
                "→ Une affirmation claire, courte (≤ 25 mots), précise, ni piège ni double négation.\n"
                "→ correct_answer = \"vrai\" OU \"faux\" (en minuscules, en français)."
            )
            json_schema = (
                '{\n'
                '  "question": "affirmation à juger vraie ou fausse",\n'
                '  "type": "vrai_faux",\n'
                '  "correct_answer": "vrai",\n'
                f'  "topic": "nom_concept_précis",\n'
                f'  "chapter_number": {chapter_num_value},\n'
                '  "difficulty": "facile",\n'
                f'  "bac_year": "{primary_bac_year or "2024"}",\n'
                '  "grounded_in": "course"\n'
                '}'
            )
        elif target_type == 'association':
            type_instruction = (
                "TYPE IMPOSÉ : ASSOCIATION\n"
                "→ 4 paires (left ↔ right) à relier : concept ↔ définition, ou cause ↔ effet, ou formule ↔ grandeur, ou symbole ↔ unité.\n"
                "→ Les 4 termes 'left' courts (≤ 6 mots), les 4 'right' courts (≤ 10 mots).\n"
                "→ Pas d'option \"je ne sais pas\" ; correct_answer = \"pairs\" (sentinelle, le frontend vérifie les paires)."
            )
            json_schema = (
                '{\n'
                '  "question": "Associe chaque élément de gauche à sa correspondance.",\n'
                '  "type": "association",\n'
                '  "pairs": [\n'
                '    {"left": "...", "right": "..."},\n'
                '    {"left": "...", "right": "..."},\n'
                '    {"left": "...", "right": "..."},\n'
                '    {"left": "...", "right": "..."}\n'
                '  ],\n'
                '  "correct_answer": "pairs",\n'
                f'  "topic": "nom_concept_précis",\n'
                f'  "chapter_number": {chapter_num_value},\n'
                '  "difficulty": "facile",\n'
                f'  "bac_year": "{primary_bac_year or "2024"}",\n'
                '  "grounded_in": "course"\n'
                '}'
            )
        else:  # qcm
            type_instruction = (
                "TYPE IMPOSÉ : QCM (4 options)\n"
                "→ 4 propositions UNE seule correcte (A, B, C ou D). correct_answer = \"A\" / \"B\" / \"C\" / \"D\".\n"
                "→ Distracteurs = erreurs typiques d'élèves marocains, jamais absurdes.\n"
                "→ Chaque option ≤ 18 mots, sur UNE ligne."
            )
            json_schema = (
                '{\n'
                '  "question": "énoncé clair et précis",\n'
                '  "type": "qcm",\n'
                '  "options": ["...", "...", "...", "..."],\n'
                '  "correct_answer": "A",\n'
                f'  "topic": "nom_concept_précis",\n'
                f'  "chapter_number": {chapter_num_value},\n'
                '  "difficulty": "facile",\n'
                f'  "bac_year": "{primary_bac_year or "2024"}",\n'
                '  "grounded_in": "course"\n'
                '}'
            )

        # Generate 1 question — strictly grounded + concise + no markdown tables
        prompt = f"""Tu es un expert du BAC marocain 2ème année Sciences Physiques BIOF.

🎯 TÂCHE : Génère 1 question de diagnostic STRICTEMENT FIDÈLE au cours marocain et inspirée des questions BAC réelles ci-dessous.

PROGRAMME OFFICIEL:{session['chapters_context']}{rag_section}{target_chapter_section}{course_section}{inspiration_section}

⚠️ RÈGLES DE GROUNDAGE (NON NÉGOCIABLES) :
- Tu DOIS t'appuyer sur les [Source N — BAC ...] et [Cours N — ...] ci-dessus.
- INTERDIT d'inventer un concept, une formule, une définition ou une grandeur qui ne figure NI dans le cours indexé NI dans le programme officiel.
- INTERDIT de poser une question hors-programme (ex. notion de prépa, niveau supérieur).
- Les valeurs numériques, unités, symboles doivent être ceux du cours officiel marocain.

⚠️ RÈGLES DE FORMAT (NON NÉGOCIABLES) :
- INTERDIT d'écrire un tableau Markdown (`| col | col |`, `|---|---|`, etc.) dans l'énoncé. Si la [Source] BAC contient un tableau, RÉSUME-le en 1 phrase ou choisis 1 seule paire de valeurs représentative.
- INTERDIT les listes de plus de 3 valeurs numériques dans l'énoncé.
- L'énoncé COMPLET doit tenir en ≤ 60 mots (≤ 320 caractères) — concis comme un QCM de classe, pas un exercice d'examen.
- Si une donnée numérique est nécessaire, donne-la directement dans la phrase ; ne demande JAMAIS de lire un tableau.
- Une seule idée par question : ne combine pas plusieurs concepts.

{type_instruction}

RÈGLES PÉDAGOGIQUES :
1. Question basée sur un concept DIFFÉRENT des questions déjà générées dans cette session
2. Teste la COMPRÉHENSION, pas la mémorisation pure
3. Niveau: facile ou moyen (difficile seulement si nécessaire)
4. La question DOIT porter sur le CHAPITRE CIBLE indiqué ci-dessus (si précisé){variation_instruction}
{self._MATH_FORMAT_INSTRUCTION}

FORMAT JSON STRICT (1 seule question, pas de texte hors JSON, pas de code-fence) :
{json_schema}

Le champ "bac_year" DOIT être l'année de la [Source] BAC dont tu t'es inspiré (ou l'année la plus récente d'un concept testé fréquemment)."""

        response = await llm_service.chat(
            messages=[{"role": "user", "content": prompt}],
            system_prompt="Tu es un générateur de questions d'évaluation BAC. Réponds UNIQUEMENT avec du JSON valide (un seul objet), sans texte avant/après.",
            temperature=0.7,
            # Association needs more tokens (4 pairs + structure); QCM/VF stay short.
            max_tokens=800 if target_type == 'association' else 500,
        )

        # Parse JSON response
        try:
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            cleaned = cleaned.strip()

            question = _safe_json_loads(cleaned)

            # Validate and clean
            if 'question' not in question or 'topic' not in question:
                raise ValueError("Invalid question structure")

            # Strip any leftover Markdown table from the question text — last
            # safety net if the LLM ignored the format rule. Replace pipe rows
            # by a single space so the rest of the sentence remains readable.
            question['question'] = self._strip_markdown_table(
                self._clean_question_text(question.get('question', ''))
            )
            if 'options' in question and isinstance(question['options'], list):
                question['options'] = [self._clean_question_text(opt) for opt in question['options']]

            # ── Post-generation scope validation ──
            # Reject if the LLM drifted off-program or crossed Physique ↔ Chimie.
            subject_name_local = session['subject_name']
            valid_nums = {ch.get('number') for ch in session.get('chapters_info', []) if ch.get('number')}
            if valid_nums:
                ch_num = question.get('chapter_number')
                try:
                    ch_num_int = int(ch_num) if ch_num is not None else None
                except (TypeError, ValueError):
                    ch_num_int = None
                if ch_num_int is None or ch_num_int not in valid_nums:
                    print(
                        f"[Diagnostic] REJECT off-program next-question "
                        f"(chapter_number={ch_num!r} not in {sorted(valid_nums)}): "
                        f"{question.get('question', '')[:100]}"
                    )
                    return None
            if not self._question_fits_subject(question, subject_name_local):
                print(
                    f"[Diagnostic] REJECT wrong-subject next-question "
                    f"(expected={subject_name_local}): {question.get('question', '')[:100]}"
                )
                return None

            q_type = (question.get('type') or 'qcm').lower()
            if q_type in ('vrai_faux', 'true_false', 'vf'):
                ans = str(question.get('correct_answer', '')).strip().lower()
                question['type'] = 'vrai_faux'
                question['correct_answer'] = 'vrai' if ans in ('vrai', 'true') else 'faux'
                question['options'] = ['Vrai', 'Faux']
            elif q_type == 'association':
                # Validate pairs structure
                pairs = question.get('pairs', [])
                if not isinstance(pairs, list) or len(pairs) < 2:
                    print(f"[Diagnostic] REJECT association without valid pairs: {question.get('question', '')[:100]}")
                    return None
                # Clean each pair text
                cleaned_pairs = []
                for p in pairs:
                    if not isinstance(p, dict):
                        continue
                    left = self._clean_question_text(str(p.get('left', '')))
                    right = self._clean_question_text(str(p.get('right', '')))
                    if left and right:
                        cleaned_pairs.append({'left': left, 'right': right})
                if len(cleaned_pairs) < 2:
                    print(f"[Diagnostic] REJECT association with invalid pair contents")
                    return None
                question['type'] = 'association'
                question['pairs'] = cleaned_pairs
                question['correct_answer'] = 'pairs'
                # Frontend's <select> uses options for the dropdown choices
                question['options'] = [p['right'] for p in cleaned_pairs]
            else:
                question['type'] = 'qcm'

            # Store in session
            session['generated_questions'].append(question)
            session['questions_generated'] += 1
            # Track question head for strong anti-repetition
            head = (question.get('question') or '')[:200]
            if head:
                session.setdefault('generated_question_heads', []).append(head)
            # Advance plan cursor
            session['plan_cursor'] = session.get('plan_cursor', 0) + 1

            return question

        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse LLM response: {e}")
            return None

    async def generate_diagnostic_questions(
        self, 
        subject_id: str,
        num_questions: int = 10,
        variation_seed: Optional[str] = None,
        student_id: Optional[str] = None,
    ) -> list:
        """
        Generate diagnostic questions for a subject using LLM.
        Each call generates different questions to allow retaking the exam.
        
        Args:
            subject_id: Subject UUID
            num_questions: Number of questions to generate (default 6)
            variation_seed: Optional seed for variation (timestamp, random string, etc.)
        
        Returns:
            [
                {
                    "question": "...",
                    "options": ["A", "B", "C", "D"],
                    "correct_answer": "B",
                    "topic": "glycolyse",
                    "difficulty": "medium"
                },
                ...
            ]
        """
        # Get subject info
        subject_result = self.supabase.table('subjects').select(
            'name_fr, name_ar'
        ).eq('id', subject_id).execute()
        
        if not subject_result.data:
            raise Exception("Subject not found")
        
        subject_name = subject_result.data[0]['name_fr']
        
        # Get ALL chapters with their lessons and learning objectives
        chapters_result = self.supabase.table('chapters').select(
            'id, title_fr, chapter_number, lessons(id, title_fr, learning_objectives)'
        ).eq('subject_id', subject_id).order('order_index').execute()
        
        # Build detailed chapter info with key concepts
        chapters_info = []
        for chapter in (chapters_result.data if chapters_result.data else []):
            chapter_data = {
                'title': chapter['title_fr'],
                'number': chapter.get('chapter_number', 0),
                'key_concepts': []
            }
            
            # Extract key concepts from lesson learning objectives
            if chapter.get('lessons'):
                for lesson in chapter['lessons']:
                    if lesson.get('learning_objectives'):
                        # learning_objectives is a JSON array
                        objectives = lesson['learning_objectives']
                        if isinstance(objectives, list):
                            chapter_data['key_concepts'].extend(objectives)
                        elif isinstance(objectives, str):
                            chapter_data['key_concepts'].append(objectives)
            
            chapters_info.append(chapter_data)
        
        chapters_list = [c['title'] for c in chapters_info]
        
        # ── Anti-repetition: gather ALL topics tested in last 5 diagnostics ──
        tested_topics: list[str] = []
        previous_q_heads: list[str] = []
        if student_id:
            tested_topics, previous_q_heads = self._get_tested_concepts(
                student_id, subject_id, last_n=5
            )
        else:
            # No student_id (anonymous/preview) — fall back to global history (3 last)
            history_result = self.supabase.table('diagnostic_results').select(
                'questions_data'
            ).eq('subject_id', subject_id).order(
                'created_at', desc=True
            ).limit(3).execute()
            for row in history_result.data or []:
                for q in row.get('questions_data') or []:
                    t = (q.get('topic') or '').strip().lower()
                    if t:
                        tested_topics.append(t)
                    head = (q.get('question') or '')[:100].strip()
                    if head:
                        previous_q_heads.append(head)

        # ── Pull real BAC exam questions as the SOURCE (not just inspiration) ──
        # We fetch ~2x the needed count across 2020-2025 so the LLM has a rich
        # pool of official questions to transform into QCM/association format.
        rag = get_rag_service()
        try:
            exam_inspiration = rag.get_exam_inspiration(
                subject=subject_name,
                n=max(num_questions * 2, 16),
                years=["2020", "2021", "2022", "2023", "2024", "2025"],
                exclude_topics=tested_topics or None,
                exclude_question_texts=previous_q_heads[:10] or None,
            )
        except Exception as e:
            print(f"[Diagnostic] Could not fetch exam inspiration: {e}")
            exam_inspiration = []

        # Build variation / anti-repetition instruction
        variation_instruction = ""
        if variation_seed:
            variation_instruction += f"\n\nVARIATION #{variation_seed}: questions COMPLÈTEMENT DIFFÉRENTES."

        if tested_topics:
            topics_list = "\n".join(f"  - {t}" for t in tested_topics[:20])
            variation_instruction += (
                f"\n\n⚠️ INTERDIT — sujets DÉJÀ testés avec cet élève "
                f"(dans ses {min(5, len(tested_topics))} derniers diagnostics):\n{topics_list}\n"
                f"Tu dois OBLIGATOIREMENT choisir des topics DIFFÉRENTS "
                f"(même chapitre OK, mais angles/concepts autres)."
            )
        if previous_q_heads:
            sample = previous_q_heads[:5]
            variation_instruction += (
                "\n\nNe reformule pas ces questions déjà posées :\n- "
                + "\n- ".join(sample)
            )

        # ── Build SOURCE section from real BAC questions (LLM transforms these) ──
        inspiration_section = ""
        if exam_inspiration:
            inspiration_section = (
                "\n\nQUESTIONS RÉELLES BAC 2020-2025 (SOURCE — transforme-les en QCM/association):\n"
            )
            for i, ex in enumerate(exam_inspiration, 1):
                head = (ex.get("text") or "")[:320].replace("\n", " ")
                inspiration_section += (
                    f"\n[Source {i} — BAC {ex.get('year')} {ex.get('session')}"
                    + (f", {ex['exercise_name']}" if ex.get('exercise_name') else "")
                    + (f", topic: {ex['topic']}" if ex.get('topic') else "")
                    + f"]\n{head}\n"
                )
            inspiration_section += (
                "\n⚠️ STRATÉGIE: PRENDS chaque question BAC ci-dessus et TRANSFORME-la "
                "en QCM (4 options) ou en question d'association (paires à matcher).\n"
                "- Si question ouverte → extrais le concept testé → crée 4 options plausibles\n"
                "- Si question numérique → garde le calcul, propose 4 résultats\n"
                "- Si énoncé long → isole 1 sous-question précise pour le QCM\n"
                "- Varie les années (2020, 2021, 2022, 2023, 2024, 2025) pour couverture max\n"
            )

        # Build detailed chapter context for LLM
        chapters_context = ""
        for ch in chapters_info:
            chapters_context += f"\n\n**Chapitre {ch['number']}: {ch['title']}**\n"
            if ch['key_concepts']:
                chapters_context += "Points cruciaux à tester:\n"
                for concept in ch['key_concepts'][:3]:  # Top 3 concepts per chapter
                    chapters_context += f"  - {concept}\n"
        
        # ── Historical BAC context from topic atlas (2016-2025 rotation analysis) ──
        atlas_section = ""
        try:
            from app.services.topic_atlas_service import topic_atlas
            atlas_section = topic_atlas.build_historical_context_for_prompt(
                subject_name, max_years=5
            )
            if atlas_section:
                atlas_section = (
                    "\n\n" + atlas_section
                    + "\n\n⚠️ UTILISE CES PRÉDICTIONS: au moins 2 questions sur les domaines HIGH, "
                    + "1-2 sur MEDIUM, au moins 1 sur LOW pour la couverture."
                )
        except Exception as e:
            print(f"[Diagnostic] atlas context unavailable: {e}")

        # Get RAG context from cadres de référence for this subject
        rag_context = self._get_subject_rag_context(subject_name)
        rag_section = ""
        if rag_context:
            rag_section = f"""

CADRE DE RÉFÉRENCE OFFICIEL DU BAC MAROCAIN POUR {subject_name.upper()}:
⚠️ UTILISE CES POIDS ET DOMAINES POUR ÉQUILIBRER TES QUESTIONS!
{rag_context}

RÈGLE: Répartis tes questions PROPORTIONNELLEMENT aux poids ci-dessus.
- Les domaines à fort poids doivent avoir PLUS de questions
- Chaque question doit correspondre à un domaine officiel du cadre de référence"""
        
        # Build a strict "stay-on-subject" stay-in-program constraint block.
        valid_chapter_numbers = [ch.get("number") for ch in chapters_info if ch.get("number")]
        valid_chapter_titles = [ch.get("title") for ch in chapters_info if ch.get("title")]
        stay_in_scope_block = f"""
[CONTRAINTE STRICTE — NE PAS SORTIR DU PROGRAMME]
Matière ciblée UNIQUEMENT : {subject_name}
Chapitres autorisés (numéros) : {valid_chapter_numbers}
Titres des chapitres autorisés :
{chr(10).join(f'  - Chapitre {ch.get("number")}: {ch.get("title")}' for ch in chapters_info)}

⚠️ INTERDITS ABSOLUS :
- Générer une question qui porte sur une autre matière (ex: si matière={subject_name}, ne PAS inclure de Chimie si c'est Physique, ou l'inverse).
- Générer une question sur un concept qui n'apparaît PAS dans les chapitres ci-dessus.
- Générer une question sur un chapitre dont le numéro n'est pas dans la liste {valid_chapter_numbers}.
- Si une [Source] fournie ci-dessous parle d'un autre sujet (ex: Chimie alors que matière=Physique), IGNORE-LA et pioche dans les autres sources ou invente une question fidèle au programme.

Pour chaque question générée, le champ "chapter_number" DOIT appartenir à {valid_chapter_numbers}.
"""

        # Build LLM prompt: transform real BAC questions → QCM/association
        prompt = f"""Tu es un expert du BAC marocain 2ème année Sciences Physiques BIOF.

TÂCHE: Transforme {num_questions} VRAIES questions BAC (fournies ci-dessous) en QCM ou questions d'association, pour un diagnostic {subject_name}.
{stay_in_scope_block}
PROGRAMME OFFICIEL:{chapters_context}
{rag_section}{atlas_section}{inspiration_section}

RÈGLES (STRICT):
1. Chaque question doit être DIRECTEMENT dérivée d'une des [Source] ci-dessus (cite l'année dans le champ "bac_year")
2. COUVERTURE MAX: {num_questions} questions → {num_questions} topics/domaines DIFFÉRENTS (un par chapitre si possible)
3. Difficulté répartie: ~30% facile, ~50% moyen, ~20% difficile
4. Types mixtes OBLIGATOIRES: ~60% QCM + ~20% vrai/faux + ~20% association
5. Pour QCM: 4 options plausibles, UNE seule correcte — les distracteurs = erreurs fréquentes d'élèves
6. Pour vrai/faux: affirmation claire, correct_answer = "vrai" ou "faux"
7. Pour association: 4 paires à relier (concept ↔ définition, cause ↔ effet, formule ↔ grandeur)
8. RESTE FIDÈLE au style BAC marocain (pas français)
9. ⚠️ CHAQUE question DOIT porter sur la matière {subject_name} UNIQUEMENT et sur l'un des chapitres {valid_chapter_numbers}. Questions hors programme ou hors matière = REJETÉES.{variation_instruction}
{self._MATH_FORMAT_INSTRUCTION}

FORMAT JSON STRICT (pas de texte hors JSON):
[
  {{
    "question": "énoncé clair et précis",
    "type": "qcm",
    "options": ["...", "...", "...", "..."],
    "correct_answer": "A",
    "topic": "nom_concept_précis",
    "domain": "domaine_officiel",
    "chapter_number": 1,
    "difficulty": "facile",
    "bac_year": "2024",
    "exam_weight": "27%"
  }},
  {{
    "question": "L'ADN est composé de deux brins antiparallèles.",
    "type": "vrai_faux",
    "correct_answer": "vrai",
    "topic": "structure_adn",
    "domain": "Information génétique",
    "chapter_number": 2,
    "difficulty": "facile",
    "bac_year": "2022",
    "exam_weight": "20%"
  }},
  {{
    "question": "Associez chaque concept à sa définition:",
    "type": "association",
    "pairs": [
      {{"left": "Glycolyse", "right": "Dégradation du glucose en pyruvate"}},
      {{"left": "Fermentation", "right": "Production d'énergie sans O2"}},
      {{"left": "Respiration", "right": "Oxydation complète en CO2+H2O"}},
      {{"left": "Krebs", "right": "Cycle matriciel produisant NADH"}}
    ],
    "options": ["Voir paires"],
    "correct_answer": "voir pairs",
    "topic": "métabolisme_énergétique",
    "domain": "Consommation matière organique",
    "chapter_number": 1,
    "difficulty": "moyen",
    "bac_year": "2023",
    "exam_weight": "25%"
  }}
]

Génère {num_questions} questions maintenant:"""

        # Call LLM with moderate temperature (faster convergence since we transform, not invent)
        response = await llm_service.chat(
            messages=[{"role": "user", "content": prompt}],
            system_prompt="Tu es un générateur de questions d'évaluation BAC. Réponds UNIQUEMENT avec du JSON valide (tableau d'objets), sans texte avant/après. Transforme les questions BAC source en QCM/association diversifiées.",
            temperature=0.7,  # Lower temp = faster, more deterministic transformation
            max_tokens=3000,  # ~300 tokens/question × 10 questions
        )
        
        # Parse JSON response
        try:
            # Clean response (remove markdown code blocks if present)
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            cleaned = cleaned.strip()
            
            questions = _safe_json_loads(cleaned)
            
            # Validate structure
            if not isinstance(questions, list):
                raise ValueError("Response is not a list")
            
            valid_questions = []
            valid_nums_set = set(valid_chapter_numbers)
            for q in questions:
                if 'question' not in q or 'topic' not in q:
                    continue
                # Clean question text
                q['question'] = self._clean_question_text(q.get('question', ''))
                # Clean options if present
                if 'options' in q and isinstance(q['options'], list):
                    q['options'] = [self._clean_question_text(opt) for opt in q['options']]

                # ── Post-generation scope validation ──
                # 1. Chapter must belong to the subject's chapter list.
                if valid_nums_set:
                    ch_num = q.get('chapter_number')
                    try:
                        ch_num_int = int(ch_num) if ch_num is not None else None
                    except (TypeError, ValueError):
                        ch_num_int = None
                    if ch_num_int is None or ch_num_int not in valid_nums_set:
                        print(
                            f"[Diagnostic] REJECT off-program question "
                            f"(chapter_number={ch_num!r} not in {sorted(valid_nums_set)}): "
                            f"{q.get('question', '')[:100]}"
                        )
                        continue
                # 2. Wrong-subject leak detection (Physique ↔ Chimie).
                if not self._question_fits_subject(q, subject_name):
                    print(
                        f"[Diagnostic] REJECT wrong-subject question "
                        f"(expected={subject_name}): {q.get('question', '')[:100]}"
                    )
                    continue

                q_type = (q.get('type') or 'qcm').lower()
                if q_type == 'association':
                    pairs = q.get('pairs') or []
                    if not isinstance(pairs, list) or len(pairs) < 2:
                        continue
                    q['type'] = 'association'
                    q['options'] = [self._clean_question_text(p.get('right', '')) for p in pairs]
                    q['correct_answer'] = 'pairs'
                elif q_type in ('vrai_faux', 'true_false', 'vf'):
                    ans = str(q.get('correct_answer', '')).strip().lower()
                    if ans not in ('vrai', 'faux', 'true', 'false'):
                        continue
                    q['type'] = 'vrai_faux'
                    q['correct_answer'] = 'vrai' if ans in ('vrai', 'true') else 'faux'
                    q['options'] = ['Vrai', 'Faux']
                else:
                    # QCM path
                    if not all(k in q for k in ['options', 'correct_answer']):
                        continue
                    q['type'] = 'qcm'
                valid_questions.append(q)
            
            return valid_questions[:num_questions]
            
        except (json.JSONDecodeError, ValueError) as e:
            # Fallback: return empty list if LLM response is invalid
            print(f"Failed to parse LLM response: {e}")
            return []
    
    async def evaluate_diagnostic(
        self,
        student_id: str,
        subject_id: str,
        questions: list,
        answers: dict
    ) -> dict:
        """
        Evaluate diagnostic answers and identify weak/strong topics.
        
        Args:
            student_id: Student UUID
            subject_id: Subject UUID
            questions: List of question dicts
            answers: {"0": "A", "1": "B", ...} (question index -> answer)
        
        Returns:
            {
                "score": 66.67,
                "correct_answers": 4,
                "total_questions": 6,
                "weak_topics": ["glycolyse", "krebs"],
                "strong_topics": ["adn_structure"],
                "result_id": "..."
            }
        """
        correct_count = 0
        topic_performance = {}  # {topic: [correct, total]}
        
        for i, question in enumerate(questions):
            student_answer = answers.get(str(i))
            correct_answer = question.get('correct_answer')
            topic = question.get('topic', 'unknown')
            q_type = question.get('type', 'qcm')

            if q_type == 'association':
                pairs = question.get('pairs') or []
                expected = {str(p.get('left', '')).strip(): str(p.get('right', '')).strip() for p in pairs}
                user_map = {}
                if isinstance(student_answer, dict):
                    user_map = {str(k).strip(): str(v).strip() for k, v in student_answer.items()}
                elif isinstance(student_answer, list):
                    for p in student_answer:
                        if isinstance(p, dict):
                            user_map[str(p.get('left', '')).strip()] = str(p.get('right', '')).strip()
                matches = sum(1 for k, v in expected.items() if user_map.get(k) == v)
                is_correct = len(expected) > 0 and matches == len(expected)
            elif q_type == 'vrai_faux':
                user = str(student_answer or '').strip().lower()
                user_norm = 'vrai' if user in ('vrai', 'true', 'v', 't') else ('faux' if user in ('faux', 'false', 'f') else user)
                is_correct = user_norm == str(correct_answer or '').strip().lower()
            else:
                is_correct = student_answer == correct_answer

            if is_correct:
                correct_count += 1
            
            # Track topic performance
            if topic not in topic_performance:
                topic_performance[topic] = [0, 0]
            topic_performance[topic][1] += 1  # total
            if is_correct:
                topic_performance[topic][0] += 1  # correct
        
        total_questions = len(questions)
        score = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        # Identify weak/strong topics
        weak_topics = []
        strong_topics = []
        
        for topic, (correct, total) in topic_performance.items():
            topic_score = (correct / total * 100) if total > 0 else 0
            if topic_score < 50:
                weak_topics.append(topic)
            elif topic_score >= 75:
                strong_topics.append(topic)
        
        # Save to database
        result_data = {
            "id": str(uuid.uuid4()),
            "student_id": student_id,
            "subject_id": subject_id,
            "evaluation_type": "diagnostic",
            "score": round(score, 2),
            "total_questions": total_questions,
            "correct_answers": correct_count,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "questions_data": questions
        }
        
        result = self.supabase.table('diagnostic_results').insert(result_data).execute()
        
        # ── Feed proficiency agent with diagnostic answers (batched) ──
        try:
            from app.services.student_proficiency_service import proficiency_service
            # Get subject name
            subj_res = self.supabase.table('subjects').select('name_fr').eq('id', subject_id).execute()
            subj_name = subj_res.data[0]['name_fr'] if subj_res.data else ""
            for i, question in enumerate(questions):
                student_answer = answers.get(str(i), "")
                correct_answer = question.get('correct_answer', '')
                is_correct = student_answer == correct_answer
                await proficiency_service.record_answer(
                    student_id=student_id,
                    subject=subj_name,
                    topic=question.get('topic', question.get('domain', '')),
                    question_content=question.get('question', '')[:300],
                    student_answer=str(student_answer),
                    correct_answer=str(correct_answer),
                    is_correct=is_correct,
                    question_type="qcm",
                    score=1.0 if is_correct else 0.0,
                    max_score=1.0,
                    source="diagnostic",
                    skip_update=True,
                )
            await proficiency_service.flush_proficiency(student_id)
        except Exception as e:
            print(f"[Diagnostic] Failed to feed proficiency agent: {e}")
        
        return {
            "score": round(score, 2),
            "correct_answers": correct_count,
            "total_questions": total_questions,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "result_id": result.data[0]['id'] if result.data else None
        }
    
    async def generate_formative_evaluation(
        self,
        student_id: str,
        chapter_id: str,
        num_questions: int = 5
    ) -> list:
        """
        Generate formative evaluation for a specific chapter.
        Similar to diagnostic but focused on one chapter.
        """
        # Get chapter info
        chapter_result = self.supabase.table('chapters').select(
            'title_fr, subject_id, subjects(name_fr)'
        ).eq('id', chapter_id).execute()
        
        if not chapter_result.data:
            raise Exception("Chapter not found")
        
        chapter = chapter_result.data[0]
        chapter_title = chapter['title_fr']
        subject_name = chapter['subjects']['name_fr']
        
        # Build LLM prompt
        prompt = f"""Tu es un expert en évaluation pédagogique pour le BAC marocain.

Génère {num_questions} questions d'évaluation formative pour:
- Matière: {subject_name}
- Chapitre: {chapter_title}

RÈGLES:
1. Questions ciblées sur ce chapitre uniquement
2. Mix de QCM et questions ouvertes courtes
3. Vérifier la compréhension des concepts clés
4. Niveaux progressifs (facile → difficile)

FORMAT DE RÉPONSE (JSON uniquement):
[
  {{
    "question": "...",
    "type": "qcm",
    "options": ["A", "B", "C", "D"],
    "correct_answer": "B",
    "explanation": "..."
  }},
  {{
    "question": "...",
    "type": "open",
    "expected_answer": "...",
    "explanation": "..."
  }},
  ...
]

Génère exactement {num_questions} questions maintenant:"""

        response = await llm_service.chat(
            messages=[{"role": "user", "content": prompt}],
            system_prompt="Tu es un générateur de questions d'évaluation. Réponds UNIQUEMENT avec du JSON valide.",
            temperature=0.8,
            max_tokens=2000
        )
        
        try:
            cleaned = response.strip()
            if cleaned.startswith("```"):
                cleaned = cleaned.split("```")[1]
                if cleaned.startswith("json"):
                    cleaned = cleaned[4:]
            cleaned = cleaned.strip()
            
            questions = _safe_json_loads(cleaned)
            return questions[:num_questions]
            
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Failed to parse formative evaluation: {e}")
            return []
    
    async def evaluate_formative(
        self,
        student_id: str,
        chapter_id: str,
        questions: list,
        answers: dict
    ) -> dict:
        """Evaluate formative assessment answers"""
        correct_count = 0
        total_questions = len(questions)
        
        for i, question in enumerate(questions):
            student_answer = answers.get(str(i))
            
            if question.get('type') == 'qcm':
                is_correct = student_answer == question['correct_answer']
                if is_correct:
                    correct_count += 1
            # Open questions need manual/AI evaluation - for now count as partial credit
            elif question.get('type') == 'open':
                # Simple check: if student answered something, give partial credit
                if student_answer and len(student_answer.strip()) > 10:
                    correct_count += 0.5
        
        score = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        # Get chapter's subject_id and name
        chapter_result = self.supabase.table('chapters').select(
            'subject_id, title_fr, subjects(name_fr)'
        ).eq('id', chapter_id).execute()
        
        subject_id = chapter_result.data[0]['subject_id'] if chapter_result.data else None
        chapter_title = chapter_result.data[0].get('title_fr', '') if chapter_result.data else ''
        subject_name = chapter_result.data[0].get('subjects', {}).get('name_fr', '') if chapter_result.data else ''
        
        # Save result
        result_data = {
            "id": str(uuid.uuid4()),
            "student_id": student_id,
            "subject_id": subject_id,
            "chapter_id": chapter_id,
            "evaluation_type": "formative",
            "score": round(score, 2),
            "total_questions": total_questions,
            "correct_answers": int(correct_count),
            "weak_topics": [],
            "strong_topics": [],
            "questions_data": questions
        }
        
        self.supabase.table('diagnostic_results').insert(result_data).execute()
        
        # ── Feed proficiency agent with formative answers (batched) ──
        try:
            from app.services.student_proficiency_service import proficiency_service
            for i, question in enumerate(questions):
                student_answer = answers.get(str(i), "")
                if question.get('type') == 'qcm':
                    is_correct = student_answer == question.get('correct_answer', '')
                    q_score = 1.0 if is_correct else 0.0
                else:
                    is_correct = bool(student_answer and len(student_answer.strip()) > 10)
                    q_score = 0.5 if is_correct else 0.0
                await proficiency_service.record_answer(
                    student_id=student_id,
                    subject=subject_name,
                    topic=chapter_title,
                    question_content=question.get('question', '')[:300],
                    student_answer=str(student_answer),
                    correct_answer=str(question.get('correct_answer', question.get('expected_answer', ''))),
                    is_correct=is_correct,
                    question_type=question.get('type', 'qcm'),
                    score=q_score,
                    max_score=1.0,
                    source="formative",
                    skip_update=True,
                )
            await proficiency_service.flush_proficiency(student_id)
        except Exception as e:
            print(f"[Formative] Failed to feed proficiency agent: {e}")
        
        return {
            "score": round(score, 2),
            "correct_answers": int(correct_count),
            "total_questions": total_questions,
            "passed": score >= 60
        }
    
    async def get_diagnostic_history(self, student_id: str) -> list:
        """Get all diagnostic results for a student"""
        result = self.supabase.table('diagnostic_results').select(
            '*, subjects(name_fr)'
        ).eq('student_id', student_id).order('created_at', desc=True).execute()
        
        return result.data if result.data else []


diagnostic_service = DiagnosticService()
