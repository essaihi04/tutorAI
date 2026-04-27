"""
Exam Bank Service — Searchable index of ALL national exam questions.
Used by Libre and Coaching modes to propose formative exercises to students.
Loads all exams from data/exams/, indexes questions by topic/keywords,
and provides search_exercises(query, subject, count) for retrieval.
"""
import json
import logging
import re
import unicodedata
from pathlib import Path
from typing import Optional

_log = logging.getLogger(__name__)


def _strip_accents(s: Optional[str]) -> str:
    """NFD decomposition + drop combining marks (accents)."""
    if not s:
        return ""
    return "".join(
        c for c in unicodedata.normalize("NFD", s)
        if unicodedata.category(c) != "Mn"
    )


def _normalize_subject(name: Optional[str]) -> Optional[str]:
    """Strip accents and lowercase for robust subject comparison."""
    if not name:
        return None
    return _strip_accents(name).lower()


def _norm_kw(kw: str) -> str:
    """Lowercase + accent-stripped form of a keyword for matching."""
    return _strip_accents(kw).lower() if kw else ""


def _subject_matches(stored: Optional[str], wanted: Optional[str]) -> bool:
    """Return True if a question stored under `stored` subject should be
    counted when the caller asks for `wanted`. Handles the 'Physique-Chimie'
    combined label: a query for 'Physique' or 'Chimie' matches 'Physique-Chimie'.
    """
    if not wanted:
        return True
    s = _normalize_subject(stored) or ""
    w = _normalize_subject(wanted) or ""
    if not s or not w:
        return False
    if s == w:
        return True
    # Substring match both ways (physique ⊂ physique-chimie, math ⊂ mathematiques).
    return w in s or s in w


# Domain markers used in the "Exercice N — <Domain> : <title>" header of
# Moroccan BAC Physique-Chimie exams. Used to distinguish the Chimie
# exercise (typically Exercice 1, 7 pts) from the Physique ones
# (Nucléaire, Ondes, Mécanique, Électricité, Optique, …).
_PHYSIQUE_DOMAIN_MARKERS = {
    "physique", "mecanique", "electricite", "ondes", "onde",
    "optique", "nucleaire", "radioactivite", "transformations nucleaires",
    "ondes lumineuses", "ondes mecaniques", "circuit", "rlc",
    "oscillateur", "oscillations",
}
_CHIMIE_DOMAIN_MARKERS = {"chimie", "transformations chimiques"}


def _extract_exercise_domain(exercise_name: Optional[str]) -> Optional[str]:
    """Extract the domain word from 'Exercice N — Domain : Title' headers.
    Returns a normalized (accent-stripped, lowercase) domain string, or None
    if no domain marker is found."""
    if not exercise_name:
        return None
    # Accept em-dash, en-dash or hyphen, then capture everything up to ':'
    import re as _re
    m = _re.search(r"[—–\-]\s*([^:—–\-]+?)\s*:", exercise_name)
    if not m:
        return None
    return _normalize_subject(m.group(1).strip())


def _question_matches_subject(q: dict, wanted: Optional[str]) -> bool:
    """Refined subject filter. For Moroccan BAC Physique-Chimie exams the
    combined 'Physique-Chimie' label covers BOTH chimie and physique
    exercises, so a plain subject match is not enough — a student studying
    Chimie must not receive a Nucléaire/Ondes/Mécanique exercise.
    We narrow down using the 'Exercice N — Domain :' header that is
    consistently present in every BAC physique-chimie paper.
    """
    if not wanted:
        return True
    stored = q.get("subject") or ""
    if not _subject_matches(stored, wanted):
        return False

    stored_norm = _normalize_subject(stored) or ""
    wanted_norm = _normalize_subject(wanted) or ""

    # Only disambiguate when the stored subject is the combined label
    # AND the caller asks for one of the two sub-disciplines.
    is_combined = "physique" in stored_norm and "chimie" in stored_norm
    if not is_combined:
        return True
    if wanted_norm not in ("chimie", "physique"):
        return True

    domain = _extract_exercise_domain(q.get("exercise_name"))
    if not domain:
        # Fallback: inspect the part_name / topic as a secondary hint
        fallback = " ".join([
            q.get("part_name") or "",
            q.get("topic") or "",
        ]).lower()
        fallback_norm = _normalize_subject(fallback) or ""
        if wanted_norm == "chimie":
            # Accept if any chimie marker is present and no hard physics marker
            has_chimie = any(k in fallback_norm for k in _CHIMIE_DOMAIN_MARKERS)
            has_physique = any(k in fallback_norm for k in _PHYSIQUE_DOMAIN_MARKERS)
            return has_chimie and not has_physique
        else:  # wanted == physique
            has_physique = any(k in fallback_norm for k in _PHYSIQUE_DOMAIN_MARKERS)
            has_chimie = any(k in fallback_norm for k in _CHIMIE_DOMAIN_MARKERS)
            return has_physique and not has_chimie

    if wanted_norm == "chimie":
        # Match if domain word is a chimie marker.
        return any(mk in domain for mk in _CHIMIE_DOMAIN_MARKERS)
    # wanted == physique: match anything labelled as a physics sub-domain.
    return any(mk in domain for mk in _PHYSIQUE_DOMAIN_MARKERS)


EXAMS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "exams"


class ExamBankService:
    def __init__(self):
        self._questions: list[dict] = []
        self._loaded = False

    # ------------------------------------------------------------------ #
    #  Loading & Indexing
    # ------------------------------------------------------------------ #

    def _ensure_loaded(self):
        if self._loaded:
            return
        self._load_all_exams()
        self._loaded = True

    def _load_all_exams(self):
        """Load all exams from index.json and parse every question."""
        index_path = EXAMS_DIR / "index.json"
        if not index_path.exists():
            print("[ExamBank] No index.json found")
            return

        with open(index_path, "r", encoding="utf-8") as f:
            catalog = json.load(f)

        for meta in catalog:
            exam_path = EXAMS_DIR / meta["path"] / "exam.json"
            if not exam_path.exists():
                continue
            try:
                with open(exam_path, "r", encoding="utf-8") as f:
                    raw = json.load(f)
                self._index_exam(raw, meta)
            except Exception as e:
                print(f"[ExamBank] Error loading {meta['id']}: {e}")

        print(f"[ExamBank] Indexed {len(self._questions)} questions from {len(catalog)} exams")

    def _index_exam(self, raw: dict, meta: dict):
        """Index all questions from an exam (supports both clean and legacy format)."""
        exam_label = f"{meta['subject']} {meta['year']} {meta['session']}"
        exam_id = meta["id"]
        exam_path = meta.get("path", exam_id)  # e.g. "svt/2019_normale"
        subject = meta["subject"]
        year = meta["year"]
        session = meta["session"]

        if "parts" in raw:
            self._index_clean_format(raw, exam_id, exam_label, subject, year, session, meta, exam_path)
        elif "blocks" in raw:
            self._index_legacy_format(raw, exam_id, exam_label, subject, year, session)

    def _index_clean_format(self, raw: dict, exam_id: str, label: str,
                            subject: str, year: int, session: str, meta: dict, exam_path: str = ""):
        """Parse the new clean format with parts/exercises/questions."""
        q_index = 0
        for part in raw.get("parts", []):
            part_name = part.get("name", "")

            # Direct questions in part (e.g. "Restitution des connaissances")
            for q in part.get("questions", []):
                if q.get("sub_questions"):
                    for sq in q.get("sub_questions", []):
                        self._add_question(
                            sq, q_index, exam_id, label, subject, year, session,
                            part_name=part_name, topic="", exercise_name="",
                            exercise_context="", parent_q=q, exam_path=exam_path,
                        )
                        q_index += 1
                else:
                    self._add_question(
                        q, q_index, exam_id, label, subject, year, session,
                        part_name=part_name, topic="", exercise_name="",
                        exercise_context="", exam_path=exam_path,
                    )
                    q_index += 1

            # Questions inside exercises
            for ex in part.get("exercises", []):
                ex_name = ex.get("name", "")
                ex_topic = ex.get("topic", "")
                ex_context = ex.get("context", "")
                ex_documents = ex.get("documents", [])
                # Normalize document src paths: "tables/table_1.png" -> "assets/table_1.png"
                normalized_docs = []
                for doc in ex_documents:
                    ndoc = dict(doc)
                    src = ndoc.get("src", "")
                    if src:
                        # Extract filename and put in assets/
                        filename = src.rsplit("/", 1)[-1] if "/" in src else src
                        ndoc["src"] = f"assets/{filename}"
                    normalized_docs.append(ndoc)

                for q in ex.get("questions", []):
                    self._add_question(
                        q, q_index, exam_id, label, subject, year, session,
                        part_name=part_name, topic=ex_topic,
                        exercise_name=ex_name, exercise_context=ex_context,
                        exercise_documents=normalized_docs, exam_path=exam_path,
                    )
                    q_index += 1

        # Also index topics from meta parts for search
        for mp in meta.get("parts", []):
            for ex in mp.get("exercises", []):
                topic = ex.get("topic", "")
                if topic:
                    # Tag all questions from this exercise with the topic
                    pass  # Already handled above

    def _index_legacy_format(self, raw: dict, exam_id: str, label: str,
                             subject: str, year: int, session: str):
        """Parse legacy blocks format."""
        blocks = raw.get("blocks", [])
        questions = []
        corrections = []
        current_context = ""

        for block in blocks:
            btype = block.get("type", "")
            origin = block.get("origin", "")

            if origin == "correction" or btype == "answer":
                corrections.append(block.get("content", ""))
                continue
            if btype == "text":
                current_context += " " + block.get("content", "")
            elif btype == "question":
                page_ctx = block.get("page_context", "")
                questions.append({
                    "content": block.get("content", ""),
                    "context": current_context.strip(),
                    "page_context": page_ctx,
                    "correction_text": "",
                })
                current_context = ""

        # Pair corrections
        for i, q in enumerate(questions):
            if i < len(corrections):
                q["correction_text"] = corrections[i]

        for i, q in enumerate(questions):
            self._questions.append({
                "exam_id": exam_id,
                "exam_label": label,
                "subject": subject,
                "year": year,
                "session": session,
                "question_index": i,
                "part_name": "",
                "exercise_name": "",
                "exercise_context": "",
                "topic": q.get("page_context", ""),
                "content": q["content"],
                "type": "open",
                "points": self._extract_points(q["content"]),
                "correction": q["correction_text"],
                "keywords": self._extract_keywords(
                    q["content"] + " " + q.get("page_context", "") + " " + q.get("context", "")
                ),
            })

    def _add_question(self, q: dict, index: int, exam_id: str, label: str,
                      subject: str, year: int, session: str,
                      part_name: str = "", topic: str = "",
                      exercise_name: str = "", exercise_context: str = "",
                      parent_q: dict = None, exercise_documents: list = None,
                      exam_path: str = ""):
        """Add a single question to the index."""
        content = q.get("content", "")
        q_type = q.get("type", parent_q.get("type", "open") if parent_q else "open")
        points = q.get("points", 0)

        # Get correction text. The schema can be:
        #   {"content": "..."}                         → open / step-by-step
        #   {"correct_answer": "vrai" | "a"}           → vrai/faux / QCM single
        #   {"correct_answers": ["1-c", "2-a", ...]}   → association
        # vrai/faux & QCM questions are perfectly valid exercises with a known
        # answer — index them too.
        correction = q.get("correction", {})
        correction_text = ""
        if isinstance(correction, dict):
            correction_text = (
                correction.get("content")
                or correction.get("correct_answer")
                or correction.get("answer")
                or ""
            )
            if not correction_text:
                ca = correction.get("correct_answers")
                if isinstance(ca, list):
                    correction_text = ", ".join(str(x) for x in ca)
                elif isinstance(ca, dict):
                    correction_text = ", ".join(f"{k}: {v}" for k, v in ca.items())
        elif isinstance(correction, str):
            correction_text = correction

        # Fallback: top-level correct_answer field on the question itself
        if not correction_text and q.get("correct_answer"):
            correction_text = str(q.get("correct_answer"))

        # If still no correction, inherit from parent question
        if not correction_text and parent_q:
            parent_corr = parent_q.get("correction", {})
            if isinstance(parent_corr, dict):
                correction_text = (
                    parent_corr.get("content")
                    or parent_corr.get("correct_answer")
                    or ""
                )

        # Build keyword string for search (include subject for keyword matching)
        full_text = " ".join(filter(None, [
            content, topic, part_name, exercise_name, subject,
            exercise_context[:200] if exercise_context else "",
            correction_text[:200] if correction_text else "",
        ]))

        # Auto-infer topic from content when topic is empty (e.g. Part 1 questions)
        inferred_topic = topic
        if not inferred_topic:
            inferred_topic = self._infer_topic_from_content(full_text)

        # Get documents (images) for this question
        documents = list(exercise_documents) if exercise_documents else []
        
        # Also check for schema property on the question itself (used in "restitution des connaissances")
        if q.get("schema"):
            schema = q["schema"]
            src = schema.get("src", "")
            if src:
                # Normalize path: "schemas/schema_1.png" -> "assets/schema_1.png"
                filename = src.rsplit("/", 1)[-1] if "/" in src else src
                documents.append({
                    "id": f"schema_{index}",
                    "type": "schema",
                    "title": schema.get("title", "Schéma"),
                    "src": f"assets/{filename}",
                    "description": schema.get("description", ""),
                })
        
        kws = self._extract_keywords(full_text)
        # Pre-compute accent-stripped variants so query keywords match no
        # matter whether they have accents (genetique → génétique).
        kws_norm = {_norm_kw(k) for k in kws if k}
        full_text_norm = _strip_accents(full_text).lower()
        self._questions.append({
            "exam_id": exam_id,
            "exam_path": exam_path,
            "exam_label": label,
            "subject": subject,
            "year": year,
            "session": session,
            "question_index": index,
            "part_name": part_name,
            "exercise_name": exercise_name,
            "exercise_context": exercise_context,
            "topic": inferred_topic,
            "content": content,
            "type": q_type,
            "points": points,
            "correction": correction_text,
            "choices": q.get("choices"),
            "correct_answer": q.get("correct_answer"),
            "documents": documents,
            "keywords": kws,
            "keywords_norm": kws_norm,
            "_full_text": full_text.lower(),
            "_full_text_norm": full_text_norm,
        })

    # ------------------------------------------------------------------ #
    #  Search
    # ------------------------------------------------------------------ #

    def search_exercises(
        self,
        query: str,
        subject: Optional[str] = None,
        count: int = 3,
        exclude_exam_id: Optional[str] = None,
        question_type: Optional[str] = None,
    ) -> list[dict]:
        """
        Search for exam exercises matching a topic/concept query.
        Returns up to `count` questions with their corrections.
        """
        self._ensure_loaded()
        if not self._questions:
            return []

        expanded_query = self._expand_query_aliases(query)
        query_kw = self._extract_keywords(expanded_query)
        is_generic_exam_request = self._is_generic_exam_request(query)
        _log.info(f"[ExamSearch] query='{query}' subject='{subject}' expanded='{expanded_query[:120]}' keywords={sorted(query_kw)[:10]}")
        if not query_kw and not is_generic_exam_request:
            _log.info("[ExamSearch] No keywords and not generic → returning empty")
            return []

        scored = []
        for q in self._questions:
            # Filter by subject (uses _question_matches_subject so 'Chimie' matches
            # only the Chimie exercise within a Physique-Chimie exam, not Nucléaire/Ondes/…)
            if subject and not _question_matches_subject(q, subject):
                continue
            # Filter by exam_id
            if exclude_exam_id and q["exam_id"] == exclude_exam_id:
                continue
            # Filter by type
            if question_type and q["type"] != question_type:
                continue
            # Skip questions without corrections
            if not q.get("correction"):
                continue

            # Score: count keyword matches (accent-insensitive)
            score = self._score_match(
                query_kw, q["keywords"], q.get("topic", ""),
                q.get("content", ""), q.get("_full_text", ""),
                doc_kw_norm=q.get("keywords_norm"),
                full_text_norm=q.get("_full_text_norm", ""),
            )
            if score > 0:
                scored.append((score, q))

        # Sort by score descending, then by year descending (newer first)
        scored.sort(key=lambda x: (x[0], x[1]["year"]), reverse=True)
        if scored:
            _log.info(f"[ExamSearch] {len(scored)} matches. Top 5:")
            for s, q in scored[:5]:
                _log.info(f"  score={s:.2f} topic='{q.get('topic','')}' content='{q['content'][:60]}...'")
        else:
            _log.info("[ExamSearch] No keyword matches, trying fallback...")

        # Fallback: if no keyword matches but subject filter is set,
        # try relaxed substring matching on full text before falling back to random.
        # Accent-insensitive so "genetique" finds "génétique".
        if not scored and subject:
            topical_kw = query_kw - {
                "exercice", "examen", "bac", "national", "svt", "donne",
                "donner", "donné", "type", "sujet", "question",
                "interface", "ouvre", "ouvrir", "montre", "montrer",
            }
            topical_norm = {_norm_kw(k) for k in topical_kw if k}
            if topical_norm:
                for q in self._questions:
                    if not _question_matches_subject(q, subject):
                        continue
                    if not q.get("correction"):
                        continue
                    ft_norm = q.get("_full_text_norm") or _strip_accents(q.get("_full_text", "")).lower()
                    hits = sum(1 for kw in topical_norm if kw in ft_norm)
                    # 5-char prefix fuzzy fallback
                    if hits == 0:
                        hits = sum(
                            1 for kw in topical_norm
                            if len(kw) >= 6 and kw[:5] in ft_norm
                        ) * 0.5
                    if hits > 0:
                        scored.append((hits / len(topical_norm), q))
                scored.sort(key=lambda x: (x[0], x[1]["year"]), reverse=True)
            if not scored:
                # Truly generic: return recent exercises with corrections
                fallback = [q for q in self._questions
                            if _question_matches_subject(q, subject) and q.get("correction")]
                fallback.sort(key=lambda q: (q.get("points", 0), q.get("year", 0)), reverse=True)
                scored = [(0.1, q) for q in fallback[:count]]

        # Fallback: generic exam request without a precise topic.
        # IMPORTANT: still honour the subject filter — a Chimie search must
        # never leak Physique/SVT/Math questions just because the query was
        # generic ("donne-moi un exercice BAC").
        if not scored and is_generic_exam_request:
            fallback = [
                q for q in self._questions
                if q.get("correction")
                and (not subject or _question_matches_subject(q, subject))
            ]
            fallback.sort(
                key=lambda q: (
                    q.get("points", 0),
                    q.get("year", 0),
                ),
                reverse=True,
            )
            scored = [(0.1, q) for q in fallback[:count]]

        results = []
        for _, q in scored[:count]:
            results.append({
                "exam_id": q["exam_id"],
                "exam_path": q.get("exam_path", ""),
                "exam_label": q["exam_label"],
                "subject": q["subject"],
                "year": q["year"],
                "session": q["session"],
                "question_index": q["question_index"],
                "part_name": q["part_name"],
                "exercise_name": q["exercise_name"],
                "exercise_context": q["exercise_context"],
                "topic": q["topic"],
                "content": q["content"],
                "type": q["type"],
                "points": q["points"],
                "correction": q["correction"],
                "choices": q.get("choices"),
                "correct_answer": q.get("correct_answer"),
                "documents": q.get("documents", []),
            })

        return results

    def search_full_exercises(
        self,
        query: str,
        subject: Optional[str] = None,
        count: int = 1,
        exclude_exam_id: Optional[str] = None,
        student_level: Optional[str] = None,
        conversation_context: Optional[str] = None,
        part_filter: Optional[str] = None,  # "part1" or "part2" to filter by part
    ) -> list[dict]:
        """
        Search for the BEST matching exercise across all exams.
        Scores exercises as a whole (aggregating all question scores) rather
        than picking by individual question. Returns exercises grouped with
        all their questions and per-question filtered documents.
        
        part_filter: "part1" for Restitution des connaissances, "part2" for Raisonnement
        """
        self._ensure_loaded()
        if not self._questions:
            return []

        expanded_query = self._expand_query_aliases(query)
        # Also expand from conversation context if available
        if conversation_context:
            expanded_query += " " + self._expand_query_aliases(conversation_context)
        query_kw = self._extract_keywords(expanded_query)
        is_generic_exam_request = self._is_generic_exam_request(query)

        # ── STRICT LESSON FILTER ──
        # If the student is studying a specific lesson/chapter, build a set of
        # topical keywords from that context. Any exercise whose topic, context,
        # and content have ZERO overlap with these keywords must be rejected
        # so we never show an off-topic exam (e.g. exp/ln when studying derivatives).
        lesson_kw: set[str] = set()
        if conversation_context:
            expanded_ctx = self._expand_query_aliases(conversation_context)
            ctx_kw = self._extract_keywords(expanded_ctx)
            lesson_kw = self._get_topical_keywords(ctx_kw) - {"exercice", "examen", "bac"}
        _log.info(f"[ExamSearchFull] lesson_kw={sorted(lesson_kw)[:10]}")
        
        # Detect part filter from query if not explicitly provided
        query_lower = query.lower()
        if not part_filter:
            if any(p in query_lower for p in ["première partie", "premiere partie", "premier partie", 
                                               "part 1", "partie 1", "restitution"]):
                part_filter = "part1"
            elif any(p in query_lower for p in ["deuxième partie", "deuxieme partie", "second partie",
                                                 "part 2", "partie 2", "raisonnement"]):
                part_filter = "part2"
        
        _log.info(f"[ExamSearchFull] query='{query}' subject='{subject}' part_filter={part_filter} "
                  f"expanded_kw={sorted(query_kw)[:15]} level={student_level}")
        if not query_kw and not is_generic_exam_request:
            return []

        # ── Step 1: Group all questions by exercise key ──
        exercises_map: dict[tuple, list[dict]] = {}
        for q in self._questions:
            if subject and not _question_matches_subject(q, subject):
                continue
            if exclude_exam_id and q["exam_id"] == exclude_exam_id:
                continue
            if not q.get("correction"):
                continue
            # Apply part filter
            part_name = q.get("part_name", "").lower()
            if part_filter == "part1" and "restitution" not in part_name:
                continue
            if part_filter == "part2" and "raisonnement" not in part_name:
                continue
            ex_key = (q["exam_id"], q.get("exercise_name", ""), q.get("part_name", ""))
            exercises_map.setdefault(ex_key, []).append(q)

        if not exercises_map:
            _log.info("[ExamSearchFull] No exercises found in index after filtering")
            return []

        # ── Step 2: Score each EXERCISE as a whole ──
        exercise_scores: list[tuple[float, tuple, list[dict]]] = []
        for ex_key, questions in exercises_map.items():
            # Aggregate: best question score + average score + topic bonus
            q_scores = []
            for q in questions:
                s = self._score_match(
                    query_kw, q["keywords"],
                    q.get("topic", ""), q.get("content", ""),
                    q.get("_full_text", ""),
                    doc_kw_norm=q.get("keywords_norm"),
                    full_text_norm=q.get("_full_text_norm", "")
                )
                q_scores.append(s)

            best_q_score = max(q_scores) if q_scores else 0
            avg_q_score = sum(q_scores) / len(q_scores) if q_scores else 0
            matching_qs = sum(1 for s in q_scores if s > 0)

            # Exercise-level scoring: combine best + average + coverage
            ex_score = best_q_score * 0.6 + avg_q_score * 0.3 + (matching_qs / len(q_scores)) * 0.1

            # Strong bonus: exercise topic directly matches query theme
            rep_q = questions[0]  # representative question
            ex_topic = rep_q.get("topic", "").lower()
            ex_context = rep_q.get("exercise_context", "").lower()
            topical_kw = self._get_topical_keywords(query_kw)

            if ex_topic:
                topic_hits = sum(1 for kw in topical_kw if kw in ex_topic)
                if topic_hits > 0:
                    ex_score += topic_hits * 1.0  # strong topic bonus

            # Bonus for exercise context matching
            if ex_context and topical_kw:
                ctx_hits = sum(1 for kw in topical_kw if kw in ex_context)
                if ctx_hits > 0:
                    ex_score += ctx_hits * 0.4

            # Student level preference: prefer simpler exercises for weaker students
            if student_level:
                total_pts = sum(q.get("points", 0) for q in questions)
                if student_level in ("faible", "débutant", "weak"):
                    if total_pts <= 3:
                        ex_score += 0.3  # prefer easier exercises
                elif student_level in ("avancé", "fort", "advanced"):
                    if total_pts >= 5:
                        ex_score += 0.3  # prefer harder exercises

            # Year bonus: prefer newer exams slightly
            ex_year = rep_q.get("year", 2019)
            ex_score += (ex_year - 2015) * 0.02

            if ex_score > 0:
                exercise_scores.append((ex_score, ex_key, questions))

        exercise_scores.sort(key=lambda x: x[0], reverse=True)

        # ── Step 2b: STRICT LESSON TOPIC FILTER ──
        # Reject any exercise whose topic/exercise_context/questions have zero
        # keyword overlap with the current lesson. Without this, the generic
        # fallback (Step 4) would return arbitrary exercises unrelated to what
        # the student is studying (e.g. exp/ln when the lesson is derivatives).
        if lesson_kw:
            # Use stem matching (first 6 chars) so plural/singular variants match
            # e.g. 'logarithmiques' (kw) matches 'logarithme' in haystack via 'logari'
            def _kw_stem(kw: str) -> str:
                return kw[:6] if len(kw) > 6 else kw
            lesson_stems = {_kw_stem(kw) for kw in lesson_kw}
            filtered_scores = []
            for score, ex_key, questions in exercise_scores:
                rep = questions[0]
                haystack = " ".join([
                    rep.get("topic", "") or "",
                    rep.get("exercise_context", "") or "",
                    rep.get("exercise_name", "") or "",
                    " ".join((q.get("_full_text", "") or "")[:500] for q in questions),
                ]).lower()
                if any(stem in haystack for stem in lesson_stems):
                    filtered_scores.append((score, ex_key, questions))
            dropped = len(exercise_scores) - len(filtered_scores)
            if dropped:
                _log.info(f"[ExamSearchFull] Lesson filter dropped {dropped} off-topic exercises (kept {len(filtered_scores)})")
            exercise_scores = filtered_scores

        # ── Step 3: Fallback — substring matching on full text (accent-insensitive + fuzzy stem) ──
        if not exercise_scores:
            topical_kw = self._get_topical_keywords(query_kw)
            topical_norm = {_norm_kw(k) for k in topical_kw if k}
            if topical_norm:
                _log.info(f"[ExamSearchFull] No scored matches, trying substring/fuzzy fallback with {sorted(topical_norm)}")
                for ex_key, questions in exercises_map.items():
                    hits = 0
                    fuzzy = 0
                    total = 0
                    for q in questions:
                        ft_norm = q.get("_full_text_norm") or _strip_accents(q.get("_full_text", "")).lower()
                        total += 1
                        h = sum(1 for kw in topical_norm if kw in ft_norm)
                        if h > 0:
                            hits += h
                        else:
                            # 5-char prefix fuzzy stem (génétique → génét)
                            fuzzy += sum(
                                1 for kw in topical_norm
                                if len(kw) >= 6 and kw[:5] in ft_norm
                            )
                    weighted = hits + fuzzy * 0.5
                    if weighted > 0:
                        exercise_scores.append((weighted / (len(topical_norm) * max(total, 1)), ex_key, questions))
                exercise_scores.sort(key=lambda x: x[0], reverse=True)

        # ── Step 4: Last resort fallback for generic requests ──
        if not exercise_scores and is_generic_exam_request:
            _log.info("[ExamSearchFull] Generic exam request fallback")
            for ex_key, questions in exercises_map.items():
                total_pts = sum(q.get("points", 0) for q in questions)
                year = questions[0].get("year", 2019)
                # Only return actual exercises (with exercise_name), not standalone questions
                if questions[0].get("exercise_name"):
                    exercise_scores.append((0.1 + total_pts * 0.01 + (year - 2015) * 0.01, ex_key, questions))
            exercise_scores.sort(key=lambda x: x[0], reverse=True)

        # ── Re-apply lesson filter after fallbacks so off-topic exercises never slip through ──
        if lesson_kw and exercise_scores:
            filtered_scores = []
            for score, ex_key, questions in exercise_scores:
                rep = questions[0]
                haystack = " ".join([
                    rep.get("topic", "") or "",
                    rep.get("exercise_context", "") or "",
                    rep.get("exercise_name", "") or "",
                    " ".join((q.get("_full_text", "") or "")[:500] for q in questions),
                ]).lower()
                if any(kw in haystack for kw in lesson_kw):
                    filtered_scores.append((score, ex_key, questions))
            if len(filtered_scores) < len(exercise_scores):
                _log.info(f"[ExamSearchFull] Post-fallback lesson filter kept {len(filtered_scores)}/{len(exercise_scores)} exercises")
            exercise_scores = filtered_scores

        if not exercise_scores:
            _log.info("[ExamSearchFull] No exercises found matching current lesson")
            return []

        # ── Step 5: Log top candidates for debugging ──
        _log.info(f"[ExamSearchFull] {len(exercise_scores)} exercise candidates. Top 5:")
        for score, ex_key, qs in exercise_scores[:5]:
            rep = qs[0]
            _log.info(f"  score={score:.3f} topic='{rep.get('topic','')}' "
                      f"exercise='{rep.get('exercise_name','')}' "
                      f"exam={rep.get('exam_label','')} ({len(qs)} questions)")

        # ── Step 6: Build result from top exercises ──
        exercise_results = []
        for score, ex_key, questions in exercise_scores[:count]:
            rep_q = questions[0]
            # ⚠️ DO NOT filter individual questions out of an exercise.
            # A BAC exercise is a coherent whole: Q1 introduces the document,
            # Q2 defines the variables, Q3 builds on them, etc. Removing
            # earlier questions because their text alone doesn't match the
            # query keywords leaves the student stranded mid-exercise without
            # the setup needed to answer. We always keep ALL the questions
            # of the chosen exercise, ordered by question_index. The
            # exercise-level selection (Step 2) already ensured this is the
            # most relevant exercise as a whole.
            relevant = list(questions)
            _log.info(
                f"[ExamSearchFull] Exercise '{rep_q.get('exercise_name','')}' "
                f"— keeping ALL {len(relevant)} questions to preserve exercise integrity"
            )

            exercise_questions = []
            for cand in relevant:
                all_docs = cand.get("documents", [])
                filtered_docs = self._extract_referenced_docs(cand.get("content", ""), all_docs, cand.get("type", ""))
                exercise_questions.append({
                    "question_index": cand["question_index"],
                    "content": cand["content"],
                    "type": cand["type"],
                    "points": cand["points"],
                    "correction": cand["correction"],
                    "choices": cand.get("choices"),
                    "correct_answer": cand.get("correct_answer"),
                    "documents": filtered_docs,
                })
            exercise_questions.sort(key=lambda x: x["question_index"])

            all_exercise_docs = rep_q.get("documents", [])

            exercise_results.append({
                "exam_id": rep_q["exam_id"],
                "exam_path": rep_q.get("exam_path", ""),
                "exam_label": rep_q["exam_label"],
                "subject": rep_q["subject"],
                "year": rep_q["year"],
                "session": rep_q["session"],
                "part_name": rep_q["part_name"],
                "exercise_name": rep_q["exercise_name"],
                "exercise_context": rep_q["exercise_context"],
                "topic": rep_q["topic"],
                "all_documents": all_exercise_docs,
                "questions": exercise_questions,
                "total_points": sum(eq["points"] for eq in exercise_questions),
                "_match_score": round(score, 3),
            })

        _log.info(f"[ExamSearchFull] Returning {len(exercise_results)} exercises "
                  f"(best: topic='{exercise_results[0]['topic']}' score={exercise_results[0]['_match_score']})")
        return exercise_results

    def _get_topical_keywords(self, query_kw: set) -> set:
        """Filter out generic noise words from query keywords, keeping only topical ones."""
        noise_words = {
            "exercice", "examen", "bac", "national", "svt", "donne",
            "donner", "donné", "type", "sujet", "question", "2019",
            "2020", "2021", "2022", "2023", "normale", "rattrapage",
            "interface", "ouvre", "ouvrir", "montre", "montrer",
            "moi", "exemple", "qcm", "veux", "veut", "veuillez",
            "veuiller", "donne", "donnez", "ramener", "afficher",
            "chercher", "trouver", "voir", "proposer",
            # Generic words that are too broad to discriminate topics
            # (e.g. "fonction" matches both derivatives and exp/ln exams)
            "fonction", "fonctions", "étude", "etude", "courbe", "courbes",
            "calcul", "calculer", "trouver", "problème", "probleme",
            "exercice", "partie", "mathématique", "mathematique",
            "mathématiques", "mathematiques",
            # Stats-query framing words ("combien de fois X est tombé en
            # restitution de connaissances partie I ces 10 dernières années")
            # These are about the QUESTION, not the TOPIC. If we let them
            # through, they match hundreds of questions whose part_name or
            # exercise_context happens to contain "restitution", etc.
            "combien", "fois", "apparition", "apparitions", "apparu",
            "apparus", "apparue", "apparues", "tombé", "tombe", "tombés",
            "tombes", "tombée", "tombee", "tombées", "tombees", "déjà",
            "deja", "fréquence", "frequence", "récurrent", "recurrent",
            "statistique", "statistiques", "occurrence", "occurrences",
            "restitution", "connaissance", "connaissances", "raisonnement",
            "exploitation", "première", "premiere", "deuxième", "deuxieme",
            "année", "annee", "années", "annees", "dernière", "derniere",
            "dernières", "dernieres", "dix", "session", "sessions",
            "vrai", "faux", "association", "ouverte", "ouvertes", "ouvert",
            "schéma", "schema", "schémas", "schemas",
        }
        topical = query_kw - noise_words
        return topical if topical else query_kw

    def _extract_referenced_docs(self, content: str, all_docs: list, q_type: str = "") -> list:
        """Return the documents that should be shown ALONGSIDE this question.

        Policy (matches real BAC paper UX where ALL documents stay visible
        throughout the whole exercise):
          • No documents indexed → return [].
          • Schema-type question → return all_docs (the schema itself).
          • Empty content → return all_docs (safe default).
          • Specific reference (« document 2 », « doc 3 ») → return ONLY the
            matching docs. This is the only case where we narrow the set,
            because the question explicitly points at a subset.
          • Generic reference (« le document », « ci-contre », « ci-dessous »,
            « la figure », « le schéma ») → return all_docs.
          • No reference at all (« Calcule X », « Justifie ta réponse »…) →
            return all_docs. Earlier this returned [], which caused all the
            docs to "accumulate" on the final synthesis question while
            intermediate questions had nothing to look at — students were
            stranded without the figures they needed.
        """
        if not all_docs:
            return []

        if q_type == "schema":
            return all_docs

        if not content:
            return list(all_docs)

        content_lower = content.lower()

        # ── 1. Specific numeric reference → narrow to the matching subset ──
        # Strategy: find every "<doc-keyword> [n°] <num>" anchor, then ALSO
        # collect any extra numbers that immediately follow via "et" or
        # comma so that lists like "documents 1, 2 et 3" or "doc 1 et 2"
        # are fully captured. We use re.finditer with a single anchor regex
        # plus a lookahead pass for the trailing list.
        referenced_numbers: set[int] = set()
        anchor_re = re.compile(
            r'(?:documents?|docs?|figures?|sch[ée]mas?|tableaux?|tableau|annexes?|courbes?|graphiques?)'
            r'\s*(?:n\s*[°ºo]\s*)?'   # optional "n°" / "n o" / "no"
            r'[\s.:\-]*'              # optional separators (space, dot, colon, dash)
            r'(\d+)'                  # ← the number we want
            r'(?P<tail>(?:\s*(?:,|et|and|&)\s*\d+)*)',  # optional list tail
        )
        for match in anchor_re.finditer(content_lower):
            referenced_numbers.add(int(match.group(1)))
            tail = match.group('tail') or ""
            for n in re.findall(r'\d+', tail):
                referenced_numbers.add(int(n))

        if referenced_numbers:
            specific = []
            for doc in all_docs:
                doc_id = doc.get("id", "")
                m = re.search(r'(\d+)', doc_id)
                if m and int(m.group(1)) in referenced_numbers:
                    specific.append(doc)
            # If a specific reference was made but we couldn't match any doc
            # (e.g. mismatched numbering), fall through to "show all" rather
            # than displaying nothing.
            if specific:
                return specific

        # ── 2. Generic reference OR no reference → show ALL docs ──
        # Both cases are treated identically: a BAC exercise always exposes
        # the full document set to the student. We do NOT hide documents
        # just because the question prose doesn't mention them.
        return list(all_docs)

    def get_full_exercise_for_question(
        self,
        exam_id: str,
        exercise_name: str,
        part_name: str = "",
    ) -> Optional[dict]:
        """Return the FULL exercise (all sibling questions, in order) that
        contains the given (exam_id, exercise_name, part_name) triplet.

        Used when a search returned a single matching question — we still
        want to display the WHOLE exercise to preserve the document /
        introduction / setup that earlier questions establish.
        """
        self._ensure_loaded()
        if not self._questions:
            return None

        siblings = [
            q for q in self._questions
            if q.get("exam_id") == exam_id
            and (q.get("exercise_name") or "") == (exercise_name or "")
            and (q.get("part_name") or "") == (part_name or "")
        ]
        if not siblings:
            return None

        siblings.sort(key=lambda q: q.get("question_index", 0))
        rep = siblings[0]
        exercise_questions = []
        for cand in siblings:
            all_docs = cand.get("documents", [])
            filtered_docs = self._extract_referenced_docs(
                cand.get("content", ""), all_docs, cand.get("type", "")
            )
            exercise_questions.append({
                "question_index": cand["question_index"],
                "content": cand["content"],
                "type": cand["type"],
                "points": cand["points"],
                "correction": cand["correction"],
                "choices": cand.get("choices"),
                "correct_answer": cand.get("correct_answer"),
                "documents": filtered_docs,
            })
        return {
            "exam_id": rep["exam_id"],
            "exam_path": rep.get("exam_path", ""),
            "exam_label": rep["exam_label"],
            "subject": rep["subject"],
            "year": rep["year"],
            "session": rep["session"],
            "part_name": rep.get("part_name", ""),
            "exercise_name": rep.get("exercise_name", ""),
            "exercise_context": rep.get("exercise_context", ""),
            "topic": rep.get("topic", ""),
            "all_documents": rep.get("documents", []),
            "questions": exercise_questions,
            "total_points": sum(eq["points"] for eq in exercise_questions),
        }

    def get_topics(self, subject: Optional[str] = None) -> list[str]:
        """Get all unique topics from indexed exams."""
        self._ensure_loaded()
        topics = set()
        for q in self._questions:
            if subject and not _question_matches_subject(q, subject):
                continue
            if q.get("topic"):
                topics.add(q["topic"])
        return sorted(topics)

    def get_exercise_for_prompt(self, exercises: list[dict]) -> str:
        """
        Format exercises into a text block suitable for including in the LLM prompt
        when the AI wants to propose an exercise to the student.
        """
        if not exercises:
            return ""

        parts = []
        for i, ex in enumerate(exercises, 1):
            block = f"--- Exercice {i} (BAC {ex['subject']} {ex['year']} {ex['session']}"
            if ex.get("exercise_name"):
                block += f" — {ex['exercise_name']}"
            block += f") ---\n"
            if ex.get("topic"):
                block += f"Thème: {ex['topic']}\n"
            if ex.get("exercise_context"):
                block += f"Contexte: {ex['exercise_context'][:300]}\n"
            block += f"Question ({ex['points']} pts): {ex['content']}\n"
            block += f"Correction officielle: {ex['correction']}\n"
            if ex.get("choices"):
                for c in ex["choices"]:
                    block += f"  {c['letter']}) {c['text']}\n"
                if ex.get("correct_answer"):
                    block += f"  Réponse correcte: {ex['correct_answer']}\n"
            parts.append(block)

        return "\n".join(parts)

    def get_chapter_stats(
        self,
        query: str,
        subject: Optional[str] = None,
    ) -> dict:
        """Count how many times a chapter/topic appears in the exam bank,
        broken down by exam part (Restitution / Raisonnement) and question
        type (qcm / vrai_faux / association / open / schema).

        Returns a structured dict intended for LLM injection so it can answer
        precise statistical questions ("combien de fois ce chapitre est tombé
        comme QCM dans la partie restitution ?") with ground-truth numbers.
        """
        self._ensure_loaded()
        if not self._questions:
            return {"total": 0, "matched": 0, "by_part": {}, "by_type": {},
                    "by_year": {}, "examples": []}

        expanded = self._expand_query_aliases(query or "")
        query_kw = self._extract_keywords(expanded)
        topical_kw = self._get_topical_keywords(query_kw) if query_kw else set()

        def _classify_part(part_name: str) -> str:
            p = (part_name or "").lower()
            if "restitution" in p:
                return "restitution"
            if "raisonnement" in p or "exploitation" in p:
                return "raisonnement"
            if "deuxième" in p or "deuxieme" in p or "partie ii" in p:
                return "raisonnement"
            if "première" in p or "premiere" in p or "partie i" in p:
                return "restitution"
            return "autre"

        matched: list[dict] = []
        for q in self._questions:
            if not _subject_matches(q["subject"], subject):
                continue
            # Match if query keywords overlap with the question's full indexed text
            haystack = " ".join([
                q.get("topic", "") or "",
                q.get("exercise_name", "") or "",
                q.get("exercise_context", "") or "",
                q.get("content", "") or "",
                q.get("_full_text", "") or "",
            ]).lower()
            if not haystack:
                continue
            # Use topical keywords first (more precise); fall back to all kw
            needles = topical_kw or query_kw
            if not needles:
                continue
            # Word-boundary matching so stems like 'gène' don't match inside
            # 'dioxygène' (ecology) or 'allèle' inside 'parallèle' etc.
            hits = sum(1 for kw in needles if kw and self._whole_word_hit(kw, haystack))
            if hits == 0:
                continue
            matched.append(q)

        by_part: dict[str, int] = {"restitution": 0, "raisonnement": 0, "autre": 0}
        by_type: dict[str, int] = {}
        by_part_type: dict[str, dict[str, int]] = {
            "restitution": {}, "raisonnement": {}, "autre": {},
        }
        by_year: dict[int, int] = {}
        examples: list[dict] = []

        for q in matched:
            bucket = _classify_part(q.get("part_name", ""))
            by_part[bucket] = by_part.get(bucket, 0) + 1
            qtype = q.get("type", "open") or "open"
            by_type[qtype] = by_type.get(qtype, 0) + 1
            by_part_type[bucket][qtype] = by_part_type[bucket].get(qtype, 0) + 1
            y = q.get("year", 0)
            if y:
                by_year[y] = by_year.get(y, 0) + 1
            if len(examples) < 8:
                examples.append({
                    "year": q.get("year"),
                    "session": q.get("session", ""),
                    "part": q.get("part_name", ""),
                    "type": qtype,
                    "topic": q.get("topic", "") or q.get("exercise_name", ""),
                    "content": (q.get("content", "") or "")[:140],
                })

        return {
            "total": len(self._questions),
            "matched": len(matched),
            "subject": subject or "tous",
            "query": query,
            "by_part": by_part,
            "by_type": by_type,
            "by_part_type": by_part_type,
            "by_year": dict(sorted(by_year.items())),
            "examples": examples,
        }

    def get_exam_topic_map(
        self,
        subject: Optional[str] = None,
        max_exams: int = 12,
    ) -> dict:
        """Return the list of topics covered by each past national exam.

        Structure:
          {
            "subject": "Mathematiques" | "Physique" | ...,
            "exams": [ { year, session, label, exercises:[{name, topic, n_questions, points}] }, ... ],
            "topic_frequency": [ (topic, count), ... ],       # top 25 across all exams
            "domain_frequency": [ (domain, count), ... ],     # inferred chapter groupings
          }

        Used by Libre mode to answer meta-questions like "quels chapitres
        tombent en math dans les examens précédents ?" with ground-truth
        data instead of hallucinated lists.
        """
        self._ensure_loaded()
        if not self._questions:
            return {"subject": subject or "tous", "exams": [], "topic_frequency": [], "domain_frequency": []}

        # ── Group questions by exam ─────────────────────────────────
        # NOTE: Physique/Chimie share the 'Physique-Chimie' label in the index,
        # so we use _subject_matches to allow substring matching.
        exam_groups: dict[str, dict] = {}
        for q in self._questions:
            if not _subject_matches(q["subject"], subject):
                continue
            ek = q["exam_id"]
            if ek not in exam_groups:
                exam_groups[ek] = {
                    "exam_id": ek,
                    "subject": q["subject"],
                    "year": q.get("year"),
                    "session": q.get("session", ""),
                    "label": q.get("exam_label", ek),
                    "_exercises": {},
                }
            ex_name = (q.get("exercise_name") or q.get("topic") or "").strip()
            if not ex_name:
                continue
            bucket = exam_groups[ek]["_exercises"].setdefault(
                ex_name,
                {"name": ex_name, "topic": q.get("topic", ""), "n_questions": 0, "points": 0},
            )
            bucket["n_questions"] += 1
            bucket["points"] += q.get("points", 0) or 0

        # ── Keep most recent exams (ordered year desc, normale before rattrapage) ──
        exams_sorted = sorted(
            exam_groups.values(),
            key=lambda e: (-(e.get("year") or 0), 0 if "normale" in (e.get("session") or "").lower() else 1),
        )[:max_exams]

        exam_list = []
        for e in exams_sorted:
            exercises = sorted(e["_exercises"].values(), key=lambda x: x["name"])
            exam_list.append({
                "year": e["year"],
                "session": e["session"],
                "label": e["label"],
                "exercises": exercises,
            })

        # ── Global topic frequency (all years) ──────────────────────
        topic_counter: dict[str, int] = {}
        for e in exam_groups.values():
            for ex in e["_exercises"].values():
                name = ex["name"]
                topic_counter[name] = topic_counter.get(name, 0) + 1
        topic_freq = sorted(topic_counter.items(), key=lambda kv: -kv[1])[:25]

        # ── Domain aggregation (infer chapter from exercise_name keywords) ──
        # (label, list of keywords). Each keyword is matched with word
        # boundaries so that short tokens like 'rc' don't hit 'exeRCice'.
        DOMAIN_RULES = [
            # Maths
            ("Nombres complexes", ["complexe", "complexes"]),
            ("Géométrie dans l'espace", ["géométrie", "geometrie", "espace"]),
            ("Suites numériques", ["suite", "suites"]),
            ("Calcul intégral", ["intégral", "integral", "intégrale", "integrale", "intégrales", "integrales"]),
            ("Étude de fonctions", ["fonction", "fonctions"]),
            ("Probabilités / Dénombrement", ["probabilité", "probabilités", "probabilites", "dénombrement", "denombrement"]),
            ("Logarithme / Exponentielle", ["logarithme", "logarithmique", "exponentiel", "exponentielle"]),
            ("Équations différentielles", ["différentielle", "differentielle", "différentielles", "differentielles"]),
            # Physique
            ("Mécanique / Lois de Newton", ["mécanique", "mecanique", "newton", "chute", "mouvement", "pendule", "satellite"]),
            ("Ondes mécaniques / lumineuses", ["onde", "ondes", "diffraction", "interférence", "lumineuse", "lumineuses"]),
            ("Nucléaire / Radioactivité", ["nucléaire", "nucleaire", "radioactivité", "radioactivite", "désintégration", "desintegration"]),
            ("Circuits RC / RL / RLC", ["rc", "rl", "rlc", "condensateur", "bobine", "oscillation", "oscillations", "circuit"]),
            # Chimie
            ("Cinétique chimique", ["cinétique", "cinetique"]),
            ("Acides / Bases / pH", ["acide", "base", "ph", "dosage"]),
            ("Piles électrochimiques", ["pile", "piles"]),
            ("Électrolyse", ["électrolyse", "electrolyse"]),
            ("Estérification / Hydrolyse", ["estérification", "esterification", "hydrolyse", "ester"]),
            # SVT
            ("Génétique humaine", ["génétique humaine", "genetique humaine"]),
            ("Génétique des populations", ["génétique des populations", "genetique des populations"]),
            ("Géologie / Tectonique", ["géologie", "geologie", "tectonique", "plaques"]),
            ("Consommation matière organique / Flux énergie", ["consommation", "matière organique", "matiere organique", "flux d'énergie", "flux d energie"]),
            ("Écologie / Environnement", ["écologie", "ecologie", "environnement"]),
        ]

        # Compile word-boundary regex patterns once per label
        compiled_rules: list[tuple[str, "re.Pattern[str]"]] = []
        for label, keywords in DOMAIN_RULES:
            # Use word boundaries (\b) so 'rc' doesn't match 'exercice'.
            alt = "|".join(re.escape(kw) for kw in keywords)
            pattern = re.compile(r"\b(?:" + alt + r")\b", re.IGNORECASE)
            compiled_rules.append((label, pattern))

        domain_counter: dict[str, int] = {}
        for name, count in topic_counter.items():
            for label, pattern in compiled_rules:
                if pattern.search(name):
                    domain_counter[label] = domain_counter.get(label, 0) + count
                    break
        domain_freq = sorted(domain_counter.items(), key=lambda kv: -kv[1])

        return {
            "subject": subject or "tous",
            "exams": exam_list,
            "topic_frequency": topic_freq,
            "domain_frequency": domain_freq,
        }

    def get_stats(self) -> dict:
        """Get statistics about the exam bank.

        Returns both flat counts (total_questions, total_exams) and a
        per-subject breakdown with number of distinct exams, number of
        questions, covered years and an estimate of total points.
        """
        self._ensure_loaded()
        per_subject: dict[str, dict] = {}
        all_exam_ids: set[str] = set()
        all_years: set[int] = set()
        topics: set[str] = set()

        for q in self._questions:
            subj = q["subject"]
            exam_id = q.get("exam_id", "")
            year = q.get("year") or 0

            bucket = per_subject.setdefault(subj, {
                "questions": 0,
                "exam_ids": set(),
                "years": set(),
                "points": 0.0,
            })
            bucket["questions"] += 1
            if exam_id:
                bucket["exam_ids"].add(exam_id)
                all_exam_ids.add(exam_id)
            if year:
                bucket["years"].add(year)
                all_years.add(year)
            try:
                bucket["points"] += float(q.get("points", 0) or 0)
            except (TypeError, ValueError):
                pass
            if q.get("topic"):
                topics.add(q["topic"])

        # Stable ordering: most questions first
        by_subject = sorted(
            [
                {
                    "subject": s,
                    "questions": b["questions"],
                    "exams": len(b["exam_ids"]),
                    "years": sorted(b["years"]),
                    "points": round(b["points"], 1),
                }
                for s, b in per_subject.items()
            ],
            key=lambda x: (-x["exams"], -x["questions"]),
        )

        years_sorted = sorted(all_years)
        year_range = [years_sorted[0], years_sorted[-1]] if years_sorted else []

        # Legacy field kept for backwards compatibility
        legacy_subjects = {row["subject"]: row["questions"] for row in by_subject}

        return {
            "total_questions": len(self._questions),
            "total_exams": len(all_exam_ids),
            "by_subject": by_subject,
            "years": years_sorted,
            "year_range": year_range,
            "topics": sorted(topics),
            "subjects": legacy_subjects,  # legacy
        }

    # ------------------------------------------------------------------ #
    #  Helpers
    # ------------------------------------------------------------------ #

    # Cache of compiled word-boundary patterns, keyed by keyword.
    # Pre-populated lazily on first use so we don't recompile inside hot loops.
    _WORD_PATTERN_CACHE: dict[str, "re.Pattern[str]"] = {}

    def _whole_word_hit(self, kw: str, haystack: str) -> bool:
        """Return True if `kw` appears as a whole word in `haystack` (both lower).

        Word boundaries use a French-friendly definition: word chars are
        letters (including accented) + digits + underscore. `re.escape` handles
        any special chars in the keyword. Result is cached per keyword.
        """
        if not kw or not haystack:
            return False
        pat = self._WORD_PATTERN_CACHE.get(kw)
        if pat is None:
            # (?<![...]) lookbehind / (?![...]) lookahead to assert the keyword
            # isn't surrounded by letters (accented included) or digits.
            letter_class = r"A-Za-zÀ-ÖØ-öø-ÿ0-9_"
            pat = re.compile(
                rf"(?<![{letter_class}]){re.escape(kw)}(?![{letter_class}])",
                re.IGNORECASE,
            )
            self._WORD_PATTERN_CACHE[kw] = pat
        return pat.search(haystack) is not None

    def _extract_keywords(self, text: str) -> set[str]:
        """Extract meaningful keywords from text for matching."""
        if not text:
            return set()
        text = text.lower()
        # Remove punctuation but keep accented chars
        text = re.sub(r'[^\w\sàâäéèêëïîôùûüÿçœæ]', ' ', text)
        words = text.split()
        # Remove short words and stopwords
        stopwords = {
            'le', 'la', 'les', 'de', 'du', 'des', 'un', 'une', 'et', 'en',
            'est', 'au', 'aux', 'que', 'qui', 'par', 'pour', 'sur', 'dans',
            'ce', 'se', 'ne', 'pas', 'son', 'sa', 'ses', 'ou', 'avec',
            'il', 'elle', 'on', 'nous', 'vous', 'ils', 'elles', 'sont',
            'cette', 'ces', 'leur', 'leurs', 'tout', 'tous', 'toute',
            'être', 'avoir', 'fait', 'faire', 'peut', 'plus', 'aussi',
            'entre', 'après', 'avant', 'comme', 'même', 'donc', 'car',
            'mais', 'puis', 'ainsi', 'très', 'bien', 'deux', 'trois',
            'quel', 'quelle', 'quels', 'quelles', 'chaque',
        }
        # Keep short but meaningful math notations (ln, exp, log, pi, etc.)
        math_keep = {"ln", "exp", "log", "pi", "dx", "dy", "nz", "iz", "rc", "rl"}
        return {w for w in words if (len(w) > 2 or w in math_keep) and w not in stopwords}

    def _is_generic_exam_request(self, text: str) -> bool:
        """Detect broad exam requests like 'exercice d examen' or 'qcm type bac'."""
        if not text:
            return False
        lowered = text.lower()
        markers = [
            "examen",
            "bac",
            "national",
            "qcm",
            "question bac",
            "exercice bac",
            "exercice d'examen",
            "exercice de examen",
            "type bac",
            "sujet bac",
        ]
        return any(marker in lowered for marker in markers)

    def _expand_query_aliases(self, text: str) -> str:
        """Expand broad curriculum aliases to concrete BAC keywords for retrieval."""
        if not text:
            return ""
        lowered = text.lower()
        aliases = {
            # Geology
            "géologie": [
                "subduction", "tectonique", "plaques", "métamorphisme",
                "convergence", "chaîne de montagnes", "lithosphère",
                "chevauchement", "ophiolite", "gneiss", "foliation",
                "andésite", "magma", "faille",
            ],
            "geologie": [
                "subduction", "tectonique", "plaques", "métamorphisme",
                "convergence", "chaîne de montagnes", "lithosphère",
                "chevauchement", "ophiolite", "gneiss", "foliation",
                "andésite", "magma", "faille",
            ],
            # Cell energy
            "respiration": ["respiration cellulaire", "mitochondrie", "atp", "énergie", "krebs", "glycolyse"],
            "energie": ["consommation matière organique", "atp", "mitochondrie", "chaîne respiratoire"],
            "énergie": ["consommation matière organique", "atp", "mitochondrie", "chaîne respiratoire"],
            "fermentation": ["fermentation", "glycolyse", "anaérobie", "éthanol", "lactique"],
            # Genetics (broad: information génétique, méiose/mitose, transmission,
            # monohybridisme/dihybridisme, ADN/ARN, Mendel, drosophile, BRCA1…)
            "genetique": [
                "génétique", "croisement", "brca1", "hérédité", "allèle",
                "gène", "mutation", "méiose", "meiose", "mitose", "chromosome",
                "chromosomes", "crossing-over", "brassage", "interchromosomique",
                "intrachromosomique", "monohybridisme", "dihybridisme",
                "homozygote", "hétérozygote", "heterozygote", "dominant",
                "récessif", "recessif", "adn", "arn", "arnm", "transcription",
                "traduction", "réplication", "replication", "gamète", "gamete",
                "drosophile", "mendel", "caryotype", "phénotype", "phenotype",
                "génotype", "genotype", "interphase", "diploïde", "diploide",
                "haploïde", "haploide",
            ],
            "génétique": [
                "génétique", "croisement", "brca1", "hérédité", "allèle",
                "gène", "mutation", "méiose", "meiose", "mitose", "chromosome",
                "chromosomes", "crossing-over", "brassage", "interchromosomique",
                "intrachromosomique", "monohybridisme", "dihybridisme",
                "homozygote", "hétérozygote", "heterozygote", "dominant",
                "récessif", "recessif", "adn", "arn", "arnm", "transcription",
                "traduction", "réplication", "replication", "gamète", "gamete",
                "drosophile", "mendel", "caryotype", "phénotype", "phenotype",
                "génotype", "genotype", "interphase", "diploïde", "diploide",
                "haploïde", "haploide",
            ],
            "hérédité": [
                "génétique", "croisement", "allèle", "gène", "dominant",
                "récessif", "mendel", "phénotype", "génotype", "hétérozygote",
                "homozygote", "gamète", "méiose",
            ],
            "croisement": [
                "génétique", "mendel", "hétérozygote", "homozygote",
                "dihybridisme", "monohybridisme", "gamète", "allèle", "gène",
                "dominant", "récessif", "phénotype", "drosophile",
            ],
            "méiose": [
                "génétique", "méiose", "mitose", "crossing-over", "brassage",
                "interchromosomique", "intrachromosomique", "gamète",
                "chromosome", "interphase", "diploïde", "haploïde",
            ],
            "meiose": [
                "génétique", "méiose", "mitose", "crossing-over", "brassage",
                "interchromosomique", "intrachromosomique", "gamète",
                "chromosome", "interphase", "diploïde", "haploïde",
            ],
            "mitose": [
                "génétique", "mitose", "méiose", "chromosome", "interphase",
                "réplication", "métaphase", "prophase", "anaphase", "télophase",
            ],
            # Ecology & pollution
            "ecologie": ["écologie", "population", "pesticides", "environnement", "bioaccumulation", "ddt", "pollution"],
            "écologie": ["écologie", "population", "pesticides", "environnement", "bioaccumulation", "ddt", "pollution"],
            "pollution": ["écologie", "pesticides", "environnement", "bioaccumulation", "contamination", "lutte biologique", "écosystème", "agadir", "endosulfan"],
            "environnement": ["écologie", "pollution", "pesticides", "bioaccumulation", "écosystème", "lutte biologique"],
            "pesticide": ["pollution", "écologie", "contamination", "bioaccumulation", "environnement", "agadir", "endosulfan"],
            "pesticides": ["pollution", "écologie", "contamination", "bioaccumulation", "environnement", "agadir", "endosulfan"],
            # Immunology
            "immunologie": [
                "immunité", "immunologie", "anticorps", "antigène", "antigene",
                "lymphocyte", "lymphocytes", "vaccin", "vaccination",
                "phagocytose", "macrophage", "plasmocyte", "interleukine",
                "cmh", "hiv", "vih", "sida", "inflammation",
            ],
            "immunité": [
                "immunité", "immunologie", "anticorps", "antigène",
                "lymphocyte", "vaccin", "phagocytose", "macrophage",
                "plasmocyte", "cmh",
            ],
            # Reproduction
            "reproduction": [
                "reproduction", "fécondation", "fecondation", "gamète", "gamete",
                "spermatozoïde", "spermatozoide", "ovule", "ovocyte", "embryon",
                "gonade", "testicule", "ovaire", "hormone", "oestrogène",
                "progestérone", "testostérone", "fsh", "lh",
            ],
            # Consommation matière organique / Flux énergie
            "respiration cellulaire": [
                "respiration", "mitochondrie", "atp", "krebs", "glycolyse",
                "chaîne respiratoire", "phosphorylation", "oxydative",
                "nadh", "fadh", "hyaloplasme", "matrice",
            ],
            "photosynthèse": [
                "photosynthèse", "chloroplaste", "thylakoïde", "stroma",
                "calvin", "chlorophylle", "lumière", "nadph",
            ],
            # Système nerveux (Communication nerveuse)
            "nerveux": [
                "neurone", "axone", "synapse", "potentiel action",
                "potentiel repos", "myéline", "nerf", "influx", "nerveux",
                "sensitif", "moteur", "récepteur", "dépolarisation",
                "repolarisation", "acétylcholine", "neurotransmetteur",
            ],
            "neurone": [
                "neurone", "axone", "synapse", "potentiel", "myéline",
                "influx", "nerveux", "acétylcholine", "neurotransmetteur",
            ],

            # ══════════════════════════ PHYSIQUE ══════════════════════════
            "mécanique": [
                "mécanique", "newton", "chute", "mouvement", "pendule",
                "satellite", "gravitation", "référentiel", "accélération",
                "vitesse", "trajectoire", "frottement", "énergie cinétique",
                "énergie potentielle", "conservation énergie",
            ],
            "mecanique": [
                "mécanique", "newton", "chute", "mouvement", "pendule",
                "satellite", "gravitation", "référentiel", "accélération",
                "vitesse", "trajectoire", "frottement",
            ],
            "newton": [
                "newton", "mécanique", "force", "mouvement", "accélération",
                "référentiel galiléen", "deuxième loi",
            ],
            "chute libre": [
                "chute", "chute libre", "pesanteur", "mouvement rectiligne",
                "accélération", "gravitation",
            ],
            "pendule": [
                "pendule", "pendule simple", "pendule élastique", "oscillation",
                "oscillateur", "période propre", "amortissement", "pulsation",
                "harmonique",
            ],
            "satellite": [
                "satellite", "gravitation", "planète", "kepler", "orbite",
                "géostationnaire", "périodicité",
            ],
            "ondes": [
                "onde", "ondes", "longueur onde", "célérité", "fréquence",
                "diffraction", "interférence", "interférences", "propagation",
                "mécanique progressive", "lumineuse", "sinusoïdale",
                "transversale", "longitudinale", "milieu dispersif",
            ],
            "diffraction": [
                "diffraction", "ouverture", "fente", "laser", "onde",
                "lumière", "longueur onde",
            ],
            "interférence": [
                "interférence", "interférences", "fentes", "young",
                "franges", "superposition", "onde", "longueur onde",
            ],
            "nucléaire": [
                "nucléaire", "radioactivité", "radioactif", "désintégration",
                "demi-vie", "période", "noyau", "proton", "neutron",
                "isotope", "fission", "fusion", "alpha", "bêta", "gamma",
                "becquerel", "curie", "masse", "énergie liaison",
            ],
            "nucleaire": [
                "nucléaire", "radioactivité", "radioactif", "désintégration",
                "demi-vie", "période", "noyau", "isotope", "fission", "fusion",
            ],
            "radioactivité": [
                "radioactivité", "radioactif", "nucléaire", "désintégration",
                "demi-vie", "alpha", "bêta", "gamma", "isotope",
            ],
            "radioactivite": [
                "radioactivité", "radioactif", "nucléaire", "désintégration",
                "demi-vie",
            ],
            # Électricité (RC / RL / RLC)
            "rc": [
                "dipôle rc", "condensateur", "charge", "décharge", "capacité",
                "constante temps", "tau", "circuit rc",
            ],
            "rl": [
                "dipôle rl", "bobine", "inductance", "auto-induction",
                "constante temps", "circuit rl",
            ],
            "rlc": [
                "circuit rlc", "oscillations", "oscillations libres",
                "oscillations forcées", "résonance", "condensateur",
                "bobine", "amortissement", "période propre",
            ],
            "condensateur": [
                "condensateur", "capacité", "charge", "décharge", "circuit rc",
                "armatures", "diélectrique",
            ],
            "bobine": [
                "bobine", "inductance", "auto-induction", "circuit rl",
                "flux magnétique",
            ],
            "oscillations": [
                "oscillations", "oscillateur", "rlc", "pendule", "période propre",
                "résonance", "amortissement", "harmonique",
            ],
            "modulation": [
                "modulation", "démodulation", "modulation amplitude",
                "porteuse", "signal modulant", "antenne",
            ],

            # ══════════════════════════ CHIMIE ══════════════════════════
            "cinétique": [
                "cinétique", "cinetique", "vitesse réaction", "temps demi",
                "concentration", "catalyseur", "facteurs cinétiques",
                "loi vitesse", "avancement",
            ],
            "cinetique": [
                "cinétique", "cinetique", "vitesse réaction", "temps demi",
                "catalyseur", "avancement",
            ],
            "acide": [
                "acide", "base", "ph", "pka", "ka", "kb", "couple",
                "réaction acido-basique", "dosage", "titrage", "équivalence",
                "solution tampon", "indicateur coloré", "conductimétrie",
            ],
            "base": [
                "acide", "base", "ph", "pka", "couple",
                "réaction acido-basique", "dosage", "titrage",
            ],
            "ph": [
                "ph", "acide", "base", "pka", "dosage", "titrage",
                "équivalence", "solution tampon",
            ],
            "dosage": [
                "dosage", "titrage", "acide", "base", "équivalence",
                "conductimétrie", "ph-métrie", "indicateur coloré",
            ],
            "titrage": [
                "dosage", "titrage", "équivalence", "ph-métrie",
                "conductimétrie", "acide", "base",
            ],
            "pile": [
                "pile", "piles", "électrochimique", "électrode", "oxydant",
                "réducteur", "anode", "cathode", "force électromotrice",
                "fem", "oxydoréduction", "demi-équation", "potentiel",
            ],
            "piles": [
                "pile", "piles", "électrochimique", "oxydoréduction",
                "anode", "cathode", "fem", "potentiel",
            ],
            "électrolyse": [
                "électrolyse", "electrolyse", "électrolyseur", "anode",
                "cathode", "oxydoréduction", "faraday",
            ],
            "electrolyse": [
                "électrolyse", "electrolyse", "électrolyseur", "anode",
                "cathode", "oxydoréduction", "faraday",
            ],
            "ester": [
                "ester", "estérification", "esterification", "hydrolyse",
                "acide carboxylique", "alcool", "équilibre chimique",
                "rendement", "estérification hydrolyse",
            ],
            "estérification": [
                "estérification", "esterification", "hydrolyse", "ester",
                "acide carboxylique", "alcool", "rendement",
            ],
            "esterification": [
                "estérification", "esterification", "hydrolyse", "ester",
                "acide carboxylique", "alcool",
            ],
            "hydrolyse": [
                "hydrolyse", "ester", "acide carboxylique", "alcool",
                "estérification",
            ],

            # ══════════════════════════ MATHS ══════════════════════════
            "dérivation": ["dérivée", "dérivable", "dérivabilité", "tangente", "nombre dérivé", "taux accroissement"],
            "derivation": ["dérivée", "dérivable", "dérivabilité", "tangente", "nombre dérivé"],
            "dérivée": ["dérivée", "dérivable", "tangente", "nombre dérivé"],
            "limites": ["limite", "continuité", "asymptote", "indétermination"],
            "continuité": ["continue", "continuité", "limite", "théorème valeurs intermédiaires", "tvi"],
            "logarithme": ["ln", "logarithme", "log", "logarithme népérien"],
            "logarithmique": ["ln", "logarithme", "log"],
            "exponentielle": ["exp", "exponentielle", "exponentiel"],
            "exponentielles": ["exp", "exponentielle", "exponentiel"],
            "primitive": ["primitive", "intégrale", "intégration"],
            "primitives": ["primitive", "intégrale", "intégration"],
            "intégrale": ["intégrale", "primitive", "intégration", "aire", "calcul intégral"],
            "intégral": ["intégrale", "primitive", "intégration", "aire"],
            "intégration": ["intégrale", "primitive", "intégration"],
            "suites": [
                "suite", "suites", "récurrence", "arithmétique", "géométrique",
                "convergence", "monotone", "majorée", "minorée", "limite suite",
            ],
            "suite": [
                "suite", "suites", "récurrence", "convergence", "monotone",
                "arithmétique", "géométrique",
            ],
            "équations différentielles": [
                "équation différentielle", "équations différentielles",
                "y prime", "y seconde", "solution particulière",
            ],
            "différentielle": [
                "équation différentielle", "équations différentielles",
            ],
            "complexes": [
                "nombre complexe", "nombres complexes", "module", "argument",
                "affixe", "forme trigonométrique", "forme algébrique",
                "forme exponentielle", "conjugué", "image",
            ],
            "complexe": [
                "nombre complexe", "module", "argument", "affixe",
                "forme trigonométrique",
            ],
            "espace": [
                "géométrie dans l'espace", "géométrie espace", "droite",
                "plan", "vecteur", "produit scalaire", "produit vectoriel",
                "équation plan", "équation droite", "sphère",
            ],
            "géométrie": [
                "géométrie", "géométrie dans l'espace", "droite", "plan",
                "vecteur", "produit scalaire",
            ],
            "probabilités": [
                "probabilité", "probabilités", "aléatoire", "loi",
                "variable aléatoire", "espérance", "variance", "binomiale",
                "conditionnelle", "indépendance",
            ],
            "probabilité": [
                "probabilité", "probabilités", "aléatoire", "variable aléatoire",
                "espérance", "loi binomiale",
            ],
            "dénombrement": [
                "combinaison", "arrangement", "permutation", "factoriel",
                "dénombrement", "cardinal",
            ],
            "denombrement": [
                "combinaison", "arrangement", "permutation", "factoriel",
                "dénombrement",
            ],
            "arithmétique": [
                "arithmétique", "divisibilité", "pgcd", "ppcm", "congruence",
                "bezout", "gauss", "nombre premier",
            ],
            "divisibilité": [
                "divisibilité", "pgcd", "ppcm", "congruence", "bezout",
                "nombre premier",
            ],
            "structures algébriques": [
                "loi composition", "groupe", "anneau", "corps", "sous-groupe",
                "élément neutre", "symétrique",
            ],
        }
        expanded_parts = [text]
        for alias, values in aliases.items():
            if alias in lowered:
                expanded_parts.extend(values)
        return " ".join(expanded_parts)

    def _infer_topic_from_content(self, text: str) -> str:
        """Auto-infer a topic label from question content for questions with no explicit topic."""
        if not text:
            return ""
        lowered = text.lower()
        topic_signatures = [
            ("Géologie et tectonique des plaques", [
                "subduction", "chevauchement", "prisme", "accrétion", "tectonique",
                "plaque", "lithosphère", "convergence", "ophiolite", "métamorphisme",
                "gneiss", "schiste", "foliation", "schistosité", "andésite",
                "magma", "faille inverse", "chaîne de montagnes", "oman",
            ]),
            ("Consommation de la matière organique et flux d'énergie", [
                "respiration cellulaire", "mitochondrie", "atp", "glycolyse",
                "krebs", "chaîne respiratoire", "nadh", "fadh",
                "fermentation", "dioxygène", "oxydation",
            ]),
            ("Génétique humaine", [
                "gène", "allèle", "mutation", "brca", "cancer",
                "adn", "arnm", "codon", "traduction", "transcription",
                "hérédité", "génotype", "phénotype",
            ]),
            ("Génétique des populations", [
                "croisement", "mendel", "dominance", "récessif",
                "hétérozygote", "homozygote", "dihybridisme",
                "échiquier", "f1", "f2", "gamète",
            ]),
            ("Écologie et environnement", [
                "écosystème", "pesticide", "pollution", "bioaccumulation",
                "lutte biologique", "chaîne alimentaire", "environnement",
                "ddt", "cochenille",
            ]),
        ]
        best_topic = ""
        best_count = 0
        for topic_name, signatures in topic_signatures:
            count = sum(1 for sig in signatures if sig in lowered)
            if count > best_count:
                best_count = count
                best_topic = topic_name
        return best_topic if best_count >= 2 else ""

    def _score_match(self, query_kw: set, doc_kw: set, topic: str, content: str,
                     full_text: str = "", doc_kw_norm: Optional[set] = None,
                     full_text_norm: str = "") -> float:
        """Score how well a question matches the query keywords.

        Matching is **accent-insensitive**: query keywords are compared against
        the question's accent-stripped keyword set and full text. A small
        fuzzy-stem match (first 5 chars) catches common French inflections
        (génétique↔génétiques, croisement↔croisements, allèle↔allèles).
        """
        if not query_kw or not doc_kw:
            return 0

        topical_kw = self._get_topical_keywords(query_kw)
        if not topical_kw:
            topical_kw = query_kw

        # Accent-stripped query keywords
        topical_norm = {_norm_kw(k) for k in topical_kw if k}
        if doc_kw_norm is None:
            doc_kw_norm = {_norm_kw(k) for k in doc_kw if k}

        # 1) Exact accent-insensitive overlap
        overlap = topical_norm & doc_kw_norm

        # 2) Substring matching on accent-stripped full text
        search_text = full_text_norm or _strip_accents(full_text or content).lower()
        substring_hits = 0
        for kw in topical_norm:
            if len(kw) >= 4 and kw in search_text and kw not in overlap:
                substring_hits += 1

        # 3) Fuzzy stem match: 5-char prefix overlap (e.g. "génét" matches
        #    génétique / génétiques / génétiquement). This catches plurals,
        #    feminine forms, derivatives without an explicit alias list.
        fuzzy_hits = 0
        already = overlap | {kw for kw in topical_norm if kw in search_text}
        for kw in topical_norm - already:
            if len(kw) >= 6:
                stem = kw[:5]
                if any(dk.startswith(stem) for dk in doc_kw_norm if len(dk) >= 5):
                    fuzzy_hits += 1
                elif stem in search_text:
                    fuzzy_hits += 1

        total_hits = len(overlap) + substring_hits + fuzzy_hits * 0.5
        if total_hits == 0:
            return 0

        score = total_hits / max(len(topical_norm), 1)

        # Strong bonus for topic match (most important signal)
        if topic:
            topic_norm = _strip_accents(topic).lower()
            topic_matches = sum(1 for kw in topical_norm if kw in topic_norm)
            score += topic_matches * 0.8

        # Bonus for content containing query words as substrings
        content_norm = _strip_accents(content).lower()
        for kw in topical_norm:
            if kw in content_norm:
                score += 0.2

        return score

    def _extract_points(self, content: str) -> float:
        match = re.search(r"\((\d+(?:[.,]\d+)?)\s*pts?\)", content, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(",", "."))
        return 0


# Singleton
exam_bank = ExamBankService()
