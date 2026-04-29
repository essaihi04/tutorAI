"""
Exam Service — Manages national exam data, serving questions, corrections,
and LLM-based evaluation of student answers.
"""
import asyncio
import json
import os
import re
import uuid
from pathlib import Path
from typing import Optional

from app.supabase_client import get_supabase_admin

EXAMS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "exams"
MOCK_EXAMS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "mock_exams"


def _find_mock_exam_dir(exam_id: str) -> Path | None:
    """Locate <subject>/<exam_id>/ directory under mock_exams/.

    Mock exam IDs start with ``mock_`` (e.g. ``mock_svt_..._cascade``).
    The subject sub-directory is unknown a priori, so we scan all of them.
    Returns ``None`` if not found.
    """
    if not exam_id or not exam_id.startswith("mock_"):
        return None
    if not MOCK_EXAMS_DIR.exists():
        return None
    for subj_dir in MOCK_EXAMS_DIR.iterdir():
        if not subj_dir.is_dir():
            continue
        candidate = subj_dir / exam_id
        if (candidate / "exam.json").exists():
            return candidate
    return None


def _autofill_doc_src_from_assets(exam: dict, assets_dir: Path) -> None:
    """Walk every document dict and, if its ``src`` is empty but a file
    matching ``{doc_id}.*`` exists in ``assets_dir``, set ``src`` to that
    relative path so the frontend serves the image.

    This recovers transparently from situations where the on-disk image was
    uploaded but the JSON ``src`` got cleared (or vice-versa).
    """
    if not assets_dir.exists():
        return
    files_by_stem: dict[str, str] = {}
    for f in assets_dir.iterdir():
        if f.is_file() and f.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}:
            files_by_stem.setdefault(f.stem, f.name)

    def walk(node):
        if isinstance(node, dict):
            for k, v in node.items():
                if k == "documents" and isinstance(v, list):
                    for d in v:
                        if not isinstance(d, dict):
                            continue
                        doc_id = d.get("id")
                        if doc_id and not d.get("src") and doc_id in files_by_stem:
                            d["src"] = f"assets/{files_by_stem[doc_id]}"
                else:
                    walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(exam)


def _load_mock_exam_meta(exam_id: str) -> dict | None:
    """Build an exam meta dict from a mock exam's ``exam.json``.

    Mirrors the shape of national exam metadata so downstream callers
    (``_structure_exam``, ``start_attempt``…) work transparently.
    """
    exam_dir = _find_mock_exam_dir(exam_id)
    if exam_dir is None:
        return None
    try:
        with open(exam_dir / "exam.json", "r", encoding="utf-8-sig") as f:
            raw = json.load(f)
    except Exception:
        return None
    # The DB ``exam_attempts.exam_session`` column has a CHECK constraint
    # restricted to ('normale', 'rattrapage'). Mock exams may carry a
    # display label like "Blanc (Normale)" — extract the canonical token so
    # start_attempt/submit_exam inserts don't violate the constraint.
    raw_session = (raw.get("session") or "").lower()
    if "rattrapage" in raw_session:
        canonical_session = "rattrapage"
    else:
        canonical_session = "normale"
    return {
        "id": raw.get("id") or exam_id,
        "subject": raw.get("subject") or "",
        "subject_full": raw.get("subject_full") or raw.get("title") or "",
        "year": raw.get("year") or 0,
        "session": canonical_session,
        "session_label": raw.get("session") or "Blanc",
        "exam_title": raw.get("title") or "",
        "duration_minutes": raw.get("duration_minutes") or 180,
        "coefficient": raw.get("coefficient") or 5,
        "total_points": raw.get("total_points") or 20,
        # Path is RELATIVE to MOCK_EXAMS_DIR (not EXAMS_DIR) — callers that need
        # to load the JSON or assets must use ``_find_mock_exam_dir`` instead.
        "path": str(exam_dir.relative_to(MOCK_EXAMS_DIR.parent.parent)),
        "is_mock": True,
    }


class ExamService:
    def __init__(self):
        self.supabase = get_supabase_admin()

    # ------------------------------------------------------------------ #
    #  Catalog
    # ------------------------------------------------------------------ #

    def _load_index(self) -> list:
        index_path = EXAMS_DIR / "index.json"
        if not index_path.exists():
            return []
        with open(index_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    def list_exams(
        self,
        subject: Optional[str] = None,
        year: Optional[int] = None,
    ) -> list:
        """Return the exam catalog, optionally filtered."""
        exams = self._load_index()
        if subject:
            exams = [e for e in exams if e["subject"].lower() == subject.lower()]
        if year:
            exams = [e for e in exams if e["year"] == year]
        return exams

    def get_extracted_exam_meta(self, exam_id: str) -> dict | None:
        """Return metadata for a transferred extracted exam stored in exam_documents."""
        result = self.supabase.table("exam_documents") \
            .select("id, subject, year, session, exam_title, duration_minutes, coefficient, total_points, structured_content") \
            .eq("id", exam_id) \
            .limit(1) \
            .execute()

        if not result.data:
            return None

        row = result.data[0]
        structured = row.get("structured_content") or {}
        metadata = structured.get("metadata") or {}

        return {
            "id": row["id"],
            "subject": structured.get("subject") or row.get("subject") or metadata.get("subject") or "Examen",
            "subject_full": row.get("exam_title") or structured.get("title") or structured.get("subject") or row.get("subject") or "Examen transféré",
            "year": structured.get("year") or row.get("year") or metadata.get("year"),
            "session": structured.get("session") or row.get("session") or metadata.get("session") or "normale",
            "exam_title": row.get("exam_title") or structured.get("title") or "Examen transféré",
            "duration_minutes": row.get("duration_minutes") or 180,
            "coefficient": row.get("coefficient") or 5,
            "total_points": float(row.get("total_points") or 20),
            "structured_content": structured,
        }

    def get_exam_meta(self, exam_id: str) -> dict | None:
        """Return metadata for a single exam by id.

        Order of resolution:
        1. National exam catalog (data/exams/index.json)
        2. Mock exam (data/mock_exams/<subject>/<id>/exam.json) if id starts with ``mock_``
        3. Extracted/imported exam (DB)
        """
        for e in self._load_index():
            if e["id"] == exam_id:
                return e
        mock_meta = _load_mock_exam_meta(exam_id)
        if mock_meta is not None:
            return mock_meta
        return self.get_extracted_exam_meta(exam_id)

    # ================================================================== #
    #  Extracted-exam deep text cleaner + question parser
    # ================================================================== #

    _ARABIC_RE = re.compile(r'[\u0600-\u06FF\u0750-\u077F\uFB50-\uFDFF\uFE70-\uFEFF]+')
    _PIPE_LINE_RE = re.compile(r'^\s*\|.*\|\s*$')
    _SEPARATOR_RE = re.compile(r'^[\s|:\-–—=_*#]+$')
    _IMG_MD_RE = re.compile(r'!\[[^\]]*\]\([^)]+\)')
    _HEADER_NOISE = [
        "المملكة المغربية", "وزارة التربية", "والتكوين المهني", "والتعليم العالي",
        "المركز الوطني", "الامتحان الوطني", "الموحد للبكالوريا", "الدورة الاستدراكية",
        "الدورة العادية", "المادة:", "المعامل:", "مدة الإنجاز:", "الشعبة:", "الصفحة",
        "royaume du maroc", "ministère", "centre national",
        "examen national", "session normale", "session de rattrapage",
        "sciences physiques", "sciences de la vie et de la terre",
        "il est permis d'utiliser", "l'usage de la calculatrice",
        "rn 34f", "rs 34f", "rn34f", "rs34f", "rrn ",
        "description visuelle", "voici une description détaillée",
        "éléments annotés", "informations importantes",
    ]
    _STANDALONE_NOISE = re.compile(
        r'^\s*(?:completed|pending|processing|failed|skipped'
        r'|\d{1,2}\s*$'  # standalone single/double digit
        r'|rs\s*\d+\w*|rn\s*\d+\w*'  # RS 34F, RN 34F etc.
        r')\s*$', re.IGNORECASE
    )

    def _clean_extracted_text(self, text: str) -> str:
        """Deep cleaning of OCR extracted text."""
        if not text:
            return ""
        text = text.replace("\r", "")

        # Remove entire "Description visuelle" blocks (vision AI output mixed in)
        text = re.sub(
            r'(?:^|\n)\s*(?:Description visuelle|Voici une description détaillée).*',
            '', text, flags=re.DOTALL | re.IGNORECASE
        )

        # Remove markdown image references ![...](...)
        text = self._IMG_MD_RE.sub("", text)

        # Strip markdown bold/italic
        text = text.replace("**", "")
        text = re.sub(r"^\s*\*+\s*", "", text, flags=re.MULTILINE)
        # Strip markdown headers used as decoration (keep content)
        text = re.sub(r"^#{1,4}\s*", "", text, flags=re.MULTILINE)
        # Strip markdown bullet markers
        text = re.sub(r"^\s*[-•]\s+", "", text, flags=re.MULTILINE)

        lines = text.split("\n")
        cleaned = []
        for raw_line in lines:
            line = raw_line.strip()
            if not line:
                if cleaned and cleaned[-1] != "":
                    cleaned.append("")
                continue

            # Drop pure Arabic lines
            stripped_ar = self._ARABIC_RE.sub("", line).strip()
            if not stripped_ar:
                continue

            # Drop lines that are mostly Arabic with a few Latin chars (headers)
            latin_only = self._ARABIC_RE.sub("", line)
            if len(latin_only.strip()) < len(line.strip()) * 0.3 and len(line) > 10:
                continue

            # Drop pipe-table lines (OCR artifacts)
            if self._PIPE_LINE_RE.match(line):
                continue

            # Drop separator lines (-----, =====, |:---|, etc.)
            if self._SEPARATOR_RE.match(line):
                continue

            # Drop standalone noise (status words, isolated numbers, RS codes)
            if self._STANDALONE_NOISE.match(line):
                continue

            # Drop known header noise
            lower = line.lower()
            if any(noise in lower for noise in self._HEADER_NOISE):
                continue

            # Drop page number lines
            if re.match(r'^\s*page\s+\d+', lower):
                continue

            # Drop standalone page markers like "1/4", "2/6"
            if re.match(r'^\s*\d+\s*/\s*\d+\s*$', line):
                continue

            # Drop lines that are just image placeholders
            if re.match(r'^\s*\[(?:Image|Document)\s+\d+[^\]]*\]\s*$', line):
                continue

            cleaned.append(line)

        result = "\n".join(cleaned)
        result = re.sub(r"\n{3,}", "\n\n", result)
        return result.strip()

    # -- Question / structure detection patterns --

    _ROMAN_Q_RE = re.compile(
        r'^\s*(I{1,3}V?|IV|VI{0,3}|V)\s*[\.\-–)]\s*', re.IGNORECASE
    )
    _NUMBERED_Q_RE = re.compile(
        r'^\s*(\d+)\s*[\.\-–)]\s*'
    )
    _SUB_Q_RE = re.compile(
        r'^\s*([a-d])\s*[\.\-–)]\s*', re.IGNORECASE
    )
    _PART_RE = re.compile(
        r'(?:première|premiere|deuxième|deuxieme|troisième|troisieme)\s+partie'
        r'|restitution\s+des\s+connaissances'
        r'|raisonnement\s+scientifique',
        re.IGNORECASE
    )
    _EXERCISE_RE = re.compile(
        r'^\s*(?:exercice|activité)\s+\d+', re.IGNORECASE
    )
    _POINTS_RE = re.compile(
        r'\((\d+(?:[.,]\d+)?)\s*(?:pts?|points?)\)', re.IGNORECASE
    )
    _FIGURE_RE = re.compile(
        r'\[(?:Figure|Document|Doc|Fig)\s*(\d+[a-z]?)\]', re.IGNORECASE
    )
    _DOC_REF_RE = re.compile(
        r'(?:document|doc|figure|fig)\s*(\d+[a-z]?)', re.IGNORECASE
    )

    def _detect_question_type(self, text: str) -> str:
        """Detect question type from text content.
        
        Returns: 'qcm', 'vrai_faux', 'association', 'schema', or 'open'
        """
        lower = text.lower()

        # QCM indicators
        qcm_keywords = [
            "recopiez les couples", "proposition correcte", "proposition est correcte",
            "la bonne proposition", "suggestion correcte", "suggestion est correcte",
            "la bonne réponse", "cochez", "choisissez", "entourez",
            "une seule suggestion", "une seule réponse",
        ]
        if any(kw in lower for kw in qcm_keywords):
            return "qcm"

        # Vrai/Faux indicators
        vf_keywords = [
            "vrai ou faux", "« vrai » ou « faux »", '"vrai" ou "faux"',
            "vrai» ou «faux", "écrivez devant", "recopiez le numéro",
        ]
        if any(kw in lower for kw in vf_keywords):
            return "vrai_faux"

        # Association indicators
        assoc_keywords = [
            "associez", "associer", "faites correspondre", "mettre en relation",
            "relier", "reliez", "correspond à", "correspondance",
        ]
        if any(kw in lower for kw in assoc_keywords):
            return "association"

        # Schema/document-based question
        doc_keywords = [
            "le document", "du document", "les documents", "des documents",
            "la figure", "le schéma", "le graphique", "le tableau",
            "d'après le document", "en exploitant le document",
            "en vous basant sur le document", "à partir du document",
        ]
        if any(kw in lower for kw in doc_keywords):
            return "schema"

        return "open"

    def _extract_doc_references(self, text: str) -> list[int]:
        """Extract document/figure numbers referenced in the text."""
        refs = set()
        for m in self._DOC_REF_RE.finditer(text):
            try:
                refs.add(int(m.group(1)))
            except ValueError:
                pass
        return sorted(refs)

    def _detect_qcm_choices(self, text: str) -> list | None:
        """Extract QCM choices only when they are real multiple-choice options.
        
        Distinguishes from sub-questions (a-, b-) which have individual point values
        and are full open questions, not choices.
        """
        # First check: does the question context indicate QCM?
        lower = text.lower()
        is_qcm_context = any(kw in lower for kw in [
            "recopiez les couples", "proposition est correcte",
            "proposition correcte", "bonne réponse", "la bonne proposition",
            "cochez", "choisissez", "entourez",
        ])
        if not is_qcm_context:
            return None

        # Find choice patterns (a./b./c./d. with short text, no individual points)
        choice_pattern = re.compile(
            r'(?:^|\|)\s*([a-d])\s*[\.\-–)]\s*(.+?)(?=\s*(?:\||;|$))',
            re.IGNORECASE | re.MULTILINE
        )
        matches = list(choice_pattern.finditer(text))
        if len(matches) < 2:
            return None

        choices = []
        seen_letters = set()
        for m in matches:
            letter = m.group(1).lower()
            choice_text = m.group(2).strip().rstrip(";|").strip()
            if not choice_text or letter in seen_letters:
                continue
            # If a "choice" has its own point value, it's a sub-question, not a QCM choice
            if re.search(r'\(\s*\d+(?:[.,]\d+)?\s*(?:pts?|points?)\)', choice_text, re.IGNORECASE):
                return None
            seen_letters.add(letter)
            choices.append({"letter": letter, "text": choice_text})

        if len(choices) >= 2:
            return choices
        return None

    def _build_correction_map(self, correction_text: str) -> dict:
        """Build a map of question_key -> correction text."""
        if not correction_text:
            return {}
        cmap = {}
        current_key = None
        current_lines = []

        for raw_line in correction_text.split("\n"):
            line = raw_line.strip()
            if not line:
                if current_lines:
                    current_lines.append("")
                continue

            # Try to match a question start
            m_num = self._NUMBERED_Q_RE.match(line)
            m_roman = self._ROMAN_Q_RE.match(line)
            key = None
            if m_num:
                key = m_num.group(1)
            elif m_roman:
                key = m_roman.group(1).upper()

            if key:
                if current_key and current_lines:
                    cmap[current_key] = "\n".join(current_lines).strip()
                current_key = key
                current_lines = [line]
            elif current_key:
                current_lines.append(line)

        if current_key and current_lines:
            cmap[current_key] = "\n".join(current_lines).strip()
        return cmap

    def _extract_pages_as_questions(self, structured: dict) -> list:
        """Last-resort fallback: one question per page."""
        exam_section = structured.get("exam") or {}
        correction_section = structured.get("correction") or {}
        corr_pages = (correction_section.get("pages") or []) if correction_section else []
        correction_by_page = {
            p.get("page"): p
            for p in corr_pages
            if p.get("page") is not None
        }
        questions = []
        for idx, page in enumerate(exam_section.get("pages") or []):
            pn = page.get("page") or (idx + 1)
            cp = correction_by_page.get(pn)
            text = self._clean_extracted_text(page.get("text") or "")
            questions.append({
                "index": idx,
                "id": f"page_{pn}",
                "number": str(pn),
                "type": "open",
                "points": 0,
                "content": text,
                "part": "Examen",
                "exercise": None,
                "exercise_context": None,
                "documents": [],
                "schema": None,
                "correction": {"content": self._clean_extracted_text(cp.get("text") or ""), "details": {}} if cp else None,
            })
        return questions

    def _parse_extracted_questions(self, structured: dict, job_id: str = "") -> list:
        """Parse extracted text into structured questions with proper splitting."""
        exam_section = structured.get("exam") or {}
        correction_section = structured.get("correction") or {}

        # Combine page texts — track page boundaries for image linking
        exam_pages = exam_section.get("pages") or []

        # Build per-page cleaned text with page number tags
        tagged_lines = []  # (line_text, page_number)
        for p in sorted(exam_pages, key=lambda x: x.get("page", 0)):
            pn = p.get("page", 0)
            cleaned = self._clean_extracted_text(p.get("text") or "")
            for line in cleaned.split("\n"):
                tagged_lines.append((line, pn))

        corr_full = ""
        if correction_section:
            corr_full = correction_section.get("full_text") or ""
            if not corr_full:
                corr_pages = correction_section.get("pages") or []
                corr_full = "\n\n".join(p.get("text", "") for p in sorted(corr_pages, key=lambda x: x.get("page", 0)))

        correction_text = self._clean_extracted_text(corr_full)
        correction_map = self._build_correction_map(correction_text)

        # Build page image map and global document image index
        page_image_map = {}
        # Global index: doc_num -> {url, label, page_number, image_index}
        all_extracted_docs = {}
        global_doc_counter = 0
        for p in exam_pages:
            pn = p.get("page", 0)
            page_extracted = p.get("extracted_images") or []
            if p.get("has_diagrams") or page_extracted:
                img_url = f"/api/v1/exam/extracted-page-image/{job_id}/{pn}" if (job_id and p.get("has_diagrams")) else ""
                page_image_map[pn] = {
                    "image_url": img_url,
                    "vision_description": p.get("vision_description", ""),
                    "extracted_images": page_extracted,
                }
                # Index each extracted image by sequential document number
                for idx, eimg in enumerate(page_extracted):
                    global_doc_counter += 1
                    fig_url = f"/api/v1/exam/extracted-figure-image/{job_id}/{pn}/{idx}" if job_id else ""
                    all_extracted_docs[global_doc_counter] = {
                        "id": eimg.get("id", f"doc_{global_doc_counter}"),
                        "label": eimg.get("label", f"Document {global_doc_counter}"),
                        "src": fig_url,
                        "page": pn,
                    }

        # -- Split into questions --
        questions = []
        current_part = "Examen"
        current_exercise = None
        current_exercise_pts = None
        exercise_context_lines = []
        current_q_key = None
        current_q_lines = []
        current_q_pages = set()  # track which pages this question spans
        current_q_is_roman = False

        def _flush_question():
            nonlocal current_q_key, current_q_lines, current_q_is_roman, current_q_pages
            if not current_q_key or not current_q_lines:
                current_q_key = None
                current_q_lines = []
                current_q_pages = set()
                return

            content = "\n".join(current_q_lines).strip()
            if not content:
                current_q_key = None
                current_q_lines = []
                current_q_pages = set()
                return

            # Detect points
            points = 0.0
            pts_match = self._POINTS_RE.search(content)
            if pts_match:
                points = float(pts_match.group(1).replace(",", "."))

            # Detect question type and QCM choices
            q_type = self._detect_question_type(content)
            choices = self._detect_qcm_choices(content)
            if choices:
                q_type = "qcm"
                # Remove choice lines from content to keep just the question stem
                stem_lines = []
                for cline in current_q_lines:
                    has_choice = False
                    for ch in choices:
                        if re.search(rf'\b{ch["letter"]}\s*[\.\-–)]', cline, re.IGNORECASE):
                            has_choice = True
                            break
                    if not has_choice:
                        stem_lines.append(cline)
                content = "\n".join(stem_lines).strip()

            # Link documents/figures referenced in the question text
            documents = []
            doc_refs = self._extract_doc_references(content)
            linked_doc_nums = set()

            # Match references like "document 1" to extracted images
            for doc_num in doc_refs:
                if doc_num in all_extracted_docs:
                    edoc = all_extracted_docs[doc_num]
                    documents.append({
                        "id": edoc["id"],
                        "type": "schema",
                        "title": edoc["label"],
                        "description": "",
                        "src": edoc["src"],
                    })
                    linked_doc_nums.add(doc_num)

            # If question references documents but none matched extracted images,
            # fall back to full page images for the pages this question spans
            if doc_refs and not linked_doc_nums:
                seen_page_imgs = set()
                for pn in sorted(current_q_pages):
                    if pn in page_image_map and pn not in seen_page_imgs:
                        seen_page_imgs.add(pn)
                        pi = page_image_map[pn]
                        if pi.get("image_url"):
                            documents.append({
                                "id": f"page_img_{pn}",
                                "type": "schema",
                                "title": f"Document page {pn}",
                                "description": pi.get("vision_description", ""),
                                "src": pi["image_url"],
                            })

            # If no doc refs in text but question type is "schema", attach all extracted
            # images from the pages this question spans
            if q_type == "schema" and not documents:
                for pn in sorted(current_q_pages):
                    if pn in page_image_map:
                        pi = page_image_map[pn]
                        for idx, eimg in enumerate(pi.get("extracted_images", [])):
                            fig_url = f"/api/v1/exam/extracted-figure-image/{job_id}/{pn}/{idx}" if job_id else ""
                            documents.append({
                                "id": eimg.get("id", f"fig_{pn}_{idx}"),
                                "type": "schema",
                                "title": eimg.get("label", f"Document {idx+1}"),
                                "description": "",
                                "src": fig_url,
                            })

            # Build exercise context
            ex_ctx = "\n".join(exercise_context_lines).strip() if exercise_context_lines else None

            # Lookup correction
            corr_text = correction_map.get(current_q_key, "")
            correction = {"content": corr_text, "details": {}} if corr_text else None

            q = {
                "index": len(questions),
                "id": f"q{current_q_key}",
                "number": current_q_key,
                "type": q_type,
                "points": points,
                "content": content,
                "part": current_part,
                "exercise": current_exercise,
                "exercise_context": ex_ctx,
                "documents": documents,
                "schema": None,
                "correction": correction,
            }
            if choices:
                q["choices"] = choices

            questions.append(q)
            current_q_key = None
            current_q_lines = []
            current_q_pages = set()
            current_q_is_roman = False

        for line_text, page_num in tagged_lines:
            line = line_text.strip()

            # Empty line
            if not line:
                if current_q_lines:
                    current_q_lines.append("")
                elif exercise_context_lines:
                    exercise_context_lines.append("")
                continue

            # Detect part heading
            if self._PART_RE.search(line):
                _flush_question()
                current_part = re.sub(r'\(\d+.*?\)', '', line).strip(" :#")
                current_exercise = None
                exercise_context_lines = []
                continue

            # Detect exercise heading
            if self._EXERCISE_RE.match(line):
                _flush_question()
                current_exercise = re.sub(r'\(\d+.*?\)', '', line).strip(" :#")
                pts_m = self._POINTS_RE.search(line)
                current_exercise_pts = float(pts_m.group(1).replace(",", ".")) if pts_m else None
                exercise_context_lines = []
                continue

            # Detect Roman numeral question (I., II., III., IV., V.)
            m_roman = self._ROMAN_Q_RE.match(line)
            if m_roman:
                _flush_question()
                current_q_key = m_roman.group(1).upper()
                current_q_is_roman = True
                current_q_pages = {page_num}
                remainder = line[m_roman.end():].strip()
                current_q_lines = [remainder] if remainder else []
                exercise_context_lines = []
                continue

            # Detect numbered question (1., 2., 3-, etc.)
            m_num = self._NUMBERED_Q_RE.match(line)
            if m_num:
                _flush_question()
                current_q_key = m_num.group(1)
                current_q_is_roman = False
                current_q_pages = {page_num}
                remainder = line[m_num.end():].strip()
                current_q_lines = [remainder] if remainder else []
                continue

            # If we are inside a question, append to it
            if current_q_key is not None:
                current_q_lines.append(line)
                current_q_pages.add(page_num)
            else:
                # Context text before first question or between exercises
                exercise_context_lines.append(line)

        _flush_question()
        return questions

    def get_extracted_exam(self, exam_id: str) -> dict | None:
        """Return a transferred extracted exam in the same shape as static exams."""
        meta = self.get_extracted_exam_meta(exam_id)
        if not meta:
            return None

        structured = meta.get("structured_content") or {}
        job_id = (structured.get("metadata") or {}).get("exam_job_id", "")
        questions = self._parse_extracted_questions(structured, job_id=job_id)
        if not questions:
            questions = self._extract_pages_as_questions(structured)

        return {
            "id": meta["id"],
            "subject": structured.get("subject") or meta["subject"],
            "year": structured.get("year") or meta["year"],
            "session": structured.get("session") or meta["session"],
            "duration_minutes": meta.get("duration_minutes") or 180,
            "coefficient": meta.get("coefficient") or 5,
            "total_points": meta.get("total_points") or 20,
            "note": structured.get("title") or meta.get("exam_title") or "",
            "questions": questions,
            "question_count": len(questions),
            "source": "extracted",
        }

    # ------------------------------------------------------------------ #
    #  Exam content
    # ------------------------------------------------------------------ #

    def _load_exam_json(self, exam_id: str) -> dict | None:
        # Mock exams live under data/mock_exams/<subject>/<id>/exam.json
        mock_dir = _find_mock_exam_dir(exam_id)
        if mock_dir is not None:
            with open(mock_dir / "exam.json", "r", encoding="utf-8-sig") as f:
                raw = json.load(f)
            _autofill_doc_src_from_assets(raw, mock_dir / "assets")
            return raw
        meta = self.get_exam_meta(exam_id)
        if not meta:
            return None
        if not meta.get("path"):
            return None
        exam_path = EXAMS_DIR / meta["path"] / "exam.json"
        if not exam_path.exists():
            return None
        with open(exam_path, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    def get_exam(self, exam_id: str) -> dict | None:
        """Return full exam content with structured questions and corrections."""
        raw = self._load_exam_json(exam_id)
        if raw is not None:
            meta = self.get_exam_meta(exam_id)
            return self._structure_exam(raw, meta)
        return self.get_extracted_exam(exam_id)

    def _structure_exam(self, raw: dict, meta: dict) -> dict:
        """Parse the clean structured exam JSON into a flat list of questions."""
        # New clean format has 'parts' with 'questions' and 'exercises'
        if "parts" in raw:
            return self._structure_clean_exam(raw, meta)
        # Legacy format with 'blocks'
        return self._structure_legacy_exam(raw, meta)

    def _structure_clean_exam(self, raw: dict, meta: dict) -> dict:
        """Parse the new clean JSON format with parts/exercises/questions.
        
        Handles two cases:
        1. Well-structured JSON (2 parts, corrections embedded) → direct processing
        2. Partially structured JSON (extra parts with only corrections) → auto-merge corrections
        """
        # Track the current subject so LaTeX-aware helpers (``_normalize_inline_math``)
        # can branch on it. For math exams we preserve raw LaTeX for KaTeX rendering.
        self._current_subject = meta.get("subject", "") if meta else ""
        parts = raw.get("parts", [])

        # ── Step 1: Collect corrections from ALL parts into a lookup map ──
        # Key: question id → value: correction dict
        # This handles the common pattern where corrections are in separate parts
        correction_map = self._collect_corrections(parts)

        # ── Step 2: Determine which parts contain actual questions vs. just corrections ──
        # A part is "correction-only" if ALL its questions have empty/no content
        # and it has no exercises with context
        main_parts = []
        for part in parts:
            if self._is_correction_only_part(part):
                continue  # skip — corrections already collected in step 1
            main_parts.append(part)

        # ── Step 3: Process main parts and merge corrections ──
        questions = []
        q_index = 0

        for part in main_parts:
            part_name = part.get("name", "")
            part_docs = part.get("documents", []) or []

            # Direct questions in part (e.g., Première partie)
            for q in part.get("questions", []):
                self._merge_correction(q, correction_map)
                # Resolve q.documents (list of IDs or objects) against part.documents
                q_docs = self._resolve_question_docs(q, part_docs)
                # If question has sub_questions, only add the sub_questions (skip parent)
                if q.get("sub_questions"):
                    for sq in q.get("sub_questions", []):
                        self._merge_correction(sq, correction_map)
                        sq_docs = self._resolve_sub_question_docs(sq, q_docs)
                        questions.append(self._format_question(sq, q_index, part_name, None, q, sq_docs))
                        q_index += 1
                else:
                    # Regular question without sub_questions
                    questions.append(self._format_question(q, q_index, part_name, None, None, q_docs))
                    q_index += 1

            # Questions inside exercises (e.g., Deuxième partie)
            for ex in part.get("exercises", []):
                ex_name = ex.get("name", "")
                ex_context = ex.get("context", "")
                ex_docs = ex.get("documents", [])

                for q in ex.get("questions", []):
                    self._merge_correction(q, correction_map)
                    if q.get("sub_questions"):
                        # Resolve parent-question docs first so sub-questions inherit
                        # that narrower scope (not the entire exercise doc list).
                        parent_docs = self._resolve_question_docs(q, ex_docs)
                        for sq in q.get("sub_questions", []):
                            self._merge_correction(sq, correction_map)
                            sq_docs = self._resolve_sub_question_docs(sq, parent_docs)
                            questions.append(self._format_question(sq, q_index, part_name, ex, q, sq_docs))
                            q_index += 1
                    else:
                        q_docs = self._resolve_question_docs(q, ex_docs)
                        questions.append(self._format_question(q, q_index, part_name, ex, None, q_docs))
                        q_index += 1

        # Part metadata (alternatives flag, instruction text) for frontend hints
        parts_meta = []
        for part in main_parts:
            pm = {
                "name": part.get("name", ""),
                "points": part.get("points", 0),
            }
            if part.get("alternatives"):
                pm["alternatives"] = True
            if part.get("instruction"):
                pm["instruction"] = part["instruction"]
            parts_meta.append(pm)

        return {
            "id": meta["id"],
            "subject": meta["subject"],
            "year": meta["year"],
            "session": meta["session"],
            "duration_minutes": meta["duration_minutes"],
            "coefficient": meta.get("coefficient", 5),
            "total_points": meta.get("total_points", 20),
            "note": raw.get("note", ""),
            "parts_meta": parts_meta,
            "questions": questions,
            "question_count": len(questions),
        }

    def _collect_corrections(self, parts: list) -> dict:
        """Build a map of question_id → correction from ALL parts.
        
        Scans every part (including correction-only parts) and collects
        corrections keyed by question id. For sub_questions, uses the
        compound id format (e.g., "II.1", "III.3").
        """
        correction_map: dict[str, dict] = {}

        for part in parts:
            # Direct questions
            for q in part.get("questions", []):
                q_id = q.get("id", "")
                corr = q.get("correction")
                if q_id and corr and isinstance(corr, dict):
                    correction_map[q_id] = corr
                # Sub-questions
                for sq in q.get("sub_questions", []):
                    sq_id = sq.get("id", "")
                    sq_corr = sq.get("correction")
                    if sq_id and sq_corr and isinstance(sq_corr, dict):
                        correction_map[sq_id] = sq_corr

            # Questions inside exercises
            for ex in part.get("exercises", []):
                for q in ex.get("questions", []):
                    q_id = q.get("id", "")
                    corr = q.get("correction")
                    if q_id and corr and isinstance(corr, dict):
                        correction_map[q_id] = corr
                    for sq in q.get("sub_questions", []):
                        sq_id = sq.get("id", "")
                        sq_corr = sq.get("correction")
                        if sq_id and sq_corr and isinstance(sq_corr, dict):
                            correction_map[sq_id] = sq_corr

        return correction_map

    def _is_correction_only_part(self, part: dict) -> bool:
        """Check if a part contains only corrections (no real question content).
        
        A part is correction-only if:
        - It has questions but ALL have empty content
        - It has no exercises with context
        """
        questions = part.get("questions", [])
        exercises = part.get("exercises", [])

        # If no questions and no exercises, skip it (empty part)
        if not questions and not exercises:
            return True

        # If it has exercises with context or questions with content, it's a main part
        for ex in exercises:
            if ex.get("context") or ex.get("questions"):
                return False

        # Check if ALL questions have empty content
        for q in questions:
            content = (q.get("content") or "").strip()
            if content:
                return False  # Has real content → not correction-only

        # All questions are empty → this is a correction-only part
        return True

    def _merge_correction(self, q: dict, correction_map: dict) -> None:
        """Merge correction from the map into a question if its correction is empty/missing.
        
        Handles:
        - Empty correction.content ("", "Non fournie")
        - Missing correct_answer for QCM/vrai_faux
        - Missing correct_pairs for association
        """
        q_id = q.get("id", "")
        if not q_id:
            return

        current_corr = q.get("correction")
        source_corr = correction_map.get(q_id)

        # No correction found in map → nothing to merge
        if not source_corr:
            return

        # No current correction at all → use the one from the map
        if not current_corr or not isinstance(current_corr, dict):
            q["correction"] = source_corr
            return

        # Current correction exists but content is empty/placeholder
        current_content = (current_corr.get("content") or "").strip().lower()
        is_empty = current_content in ("", "non fournie", "non fourni", "réponse détaillée dans la correction officielle.")

        if is_empty and source_corr.get("content"):
            current_corr["content"] = source_corr["content"]

        # Merge correct_answer if missing in current but present in source
        if not current_corr.get("correct_answer") and source_corr.get("correct_answer"):
            current_corr["correct_answer"] = source_corr["correct_answer"]

        # Merge correct_pairs if missing/empty in current but present in source
        if (not current_corr.get("correct_pairs") or current_corr.get("correct_pairs") == []) and source_corr.get("correct_pairs"):
            current_corr["correct_pairs"] = source_corr["correct_pairs"]
            # Also set at question level since _format_question reads q.get("correct_pairs")
            if not q.get("correct_pairs") or q.get("correct_pairs") == [] or q.get("correct_pairs") == {}:
                q["correct_pairs"] = source_corr["correct_pairs"]

        # Merge points_breakdown if missing in current but present in source
        if not current_corr.get("points_breakdown") and source_corr.get("points_breakdown"):
            current_corr["points_breakdown"] = source_corr["points_breakdown"]

        # Also merge correct_answer at question level for QCM/vrai_faux
        # since _format_question reads q.get("correct_answer") first
        if not q.get("correct_answer") and source_corr.get("correct_answer"):
            q["correct_answer"] = source_corr["correct_answer"]

    def _resolve_sub_question_docs(self, sq: dict, ex_docs: list) -> list:
        """Resolve document list for a sub-question.
        
        Sub-questions may specify doc IDs like ["doc1", "doc2"] in their
        'documents' field.  Map those IDs against the exercise doc list.
        If the sub-question has no explicit list, fall back to the full
        exercise list so that _extract_referenced_docs can filter later.
        """
        sq_doc_refs = sq.get("documents")
        if not sq_doc_refs:
            return ex_docs
        # Build id→doc map from exercise docs
        doc_map = {d.get("id", ""): d for d in ex_docs}
        resolved = [doc_map[ref] for ref in sq_doc_refs if ref in doc_map]
        return resolved if resolved else ex_docs

    def _resolve_question_docs(self, q: dict, ex_docs: list) -> list:
        """Resolve document list for a question inside an exercise.

        If the question explicitly declares document ids in its 'documents'
        field, only those documents should be available for rendering.
        If 'documents' is explicitly [] (empty list), return no docs.
        If 'documents' key is missing, fall back to the full exercise document list.
        """
        q_doc_refs = q.get("documents")
        # Key missing entirely → inherit exercise docs
        if q_doc_refs is None:
            return ex_docs
        # Explicitly empty list → no docs for this question
        if isinstance(q_doc_refs, list) and len(q_doc_refs) == 0:
            return []
        # Question has its own document objects (not just ID refs)
        if q_doc_refs and isinstance(q_doc_refs[0], dict):
            return q_doc_refs
        doc_map = {d.get("id", ""): d for d in ex_docs}
        resolved = [doc_map[ref] for ref in q_doc_refs if ref in doc_map]
        return resolved if resolved else ex_docs

    def _extract_referenced_docs(self, content: str, all_docs: list) -> list:
        """Extract only the documents referenced in the question content."""
        import re
        
        if not all_docs or not content:
            return all_docs or []
        
        content_lower = content.lower()
        referenced_docs = []
        
        # Pattern to match "document 1", "documents 1 et 2", "doc 3", etc.
        # Also match "document 1 :", "documents 3 et 4 :", etc.
        doc_patterns = [
            r'documents?\s+(\d+)(?:\s+et\s+(\d+))?(?:\s+et\s+(\d+))?(?:\s+et\s+(\d+))?(?:\s+et\s+(\d+))?',
            r'docs?\s+(\d+)(?:\s+et\s+(\d+))?(?:\s+et\s+(\d+))?',
        ]
        
        referenced_numbers = set()
        for pattern in doc_patterns:
            matches = re.finditer(pattern, content_lower)
            for match in matches:
                for group in match.groups():
                    if group:
                        referenced_numbers.add(int(group))
        
        # If no documents referenced, return all (for context questions)
        if not referenced_numbers:
            return all_docs
        
        # Filter documents by referenced numbers
        for doc in all_docs:
            doc_id = doc.get("id", "")
            # Extract number from doc ID. Supports:
            #   - legacy: "doc1", "doc_g5"      → capture the only/last digits
            #   - new:    "doc_e1_2"            → capture the final digit (doc# within exercise)
            # Strategy: take the LAST group of digits in the id.
            matches = re.findall(r'\d+', doc_id)
            if matches:
                doc_num = int(matches[-1])
                if doc_num in referenced_numbers:
                    referenced_docs.append(doc)
        
        return referenced_docs if referenced_docs else all_docs

    def _format_question(self, q: dict, index: int, part_name: str, exercise: dict | None, parent_q: dict | None, docs: list | None = None) -> dict:
        """Format a question for the frontend with all needed fields."""
        # If this is a sub-question, inherit parent type
        if parent_q:
            q_type = parent_q.get("type", "open")
        else:
            q_type = q.get("type", "open")

        # Filter documents based on what's referenced in the question
        content = q.get("content", "")
        filtered_docs = self._extract_referenced_docs(content, docs or [])

        # Strip inline answer choices / association tables from content to avoid
        # duplication — the interactive panel already renders them on the right.
        if q_type == "qcm" and q.get("choices"):
            content = self._strip_qcm_choices(content)
        elif q_type == "association" and (q.get("items_left") or q.get("items_right")):
            content = self._strip_association_table(content)

        # Light LaTeX → Unicode normalisation for inline math that isn't rendered
        content = self._normalize_inline_math(content)
        
        # For sub-questions, use parent correction if sub-question doesn't have one
        correction = q.get("correction")
        if parent_q and not correction:
            correction = parent_q.get("correction")

        # Build exercise_context: prefer per-question context if present,
        # then parent question context, then exercise-level context.
        # This lets different questions in the same exercise show different contexts.
        ex_context = q.get("context") or (parent_q.get("context") if parent_q else None) or (exercise.get("context") if exercise else None)

        # Points: use own points, or inherit from parent/exercise and divide equally
        points = q.get("points")
        if not points and parent_q:
            parent_pts = parent_q.get("points", 0)
            num_siblings = len(parent_q.get("sub_questions", []) or [1])
            points = round(parent_pts / max(num_siblings, 1), 2) if parent_pts else 0
        if not points and exercise:
            ex_pts = exercise.get("points", 0)
            ex_qs = exercise.get("questions", [])
            # Count total leaf questions (expand sub_questions)
            total_leaves = 0
            for eq in ex_qs:
                sqs = eq.get("sub_questions", [])
                total_leaves += len(sqs) if sqs else 1
            points = round(ex_pts / max(total_leaves, 1), 2) if ex_pts else 0
        points = points or 0

        formatted = {
            "index": index,
            "id": q.get("id", f"q{index}"),
            "number": q.get("number", str(index + 1)),
            "type": q_type,
            "points": points,
            "content": content,
            "part": part_name,
            "exercise": exercise.get("name") if exercise else None,
            "exercise_context": ex_context,
            "documents": filtered_docs,
            "schema": q.get("schema"),
            "correction": correction,
        }

        # Interactive question types — correct_answer may live in correction dict
        correct_answer = q.get("correct_answer") or (correction.get("correct_answer") if isinstance(correction, dict) else None)
        if q_type == "qcm":
            raw_choices = q.get("choices", [])
            formatted["choices"] = [
                {**c, "text": self._normalize_inline_math(c.get("text", ""))}
                for c in raw_choices
            ]
            formatted["correct_answer"] = correct_answer
        elif q_type == "vrai_faux":
            formatted["correct_answer"] = correct_answer
        elif q_type == "association":
            formatted["items_left"] = [self._normalize_inline_math(x) for x in q.get("items_left", [])]
            formatted["items_right"] = [self._normalize_inline_math(x) for x in q.get("items_right", [])]
            formatted["correct_pairs"] = q.get("correct_pairs", {})

        # If this is a sub-question, add parent info
        if parent_q:
            formatted["parent_id"] = parent_q.get("id")
            parent_content = parent_q.get("content", "")
            # For vrai_faux/qcm with sub_questions, extract only the instruction
            # (before "1-" items or markdown table) to avoid repeating all statements
            # in each sub-question.
            if parent_q.get("type") in ("vrai_faux", "qcm") and parent_q.get("sub_questions"):
                parent_content = self._extract_vf_instruction(parent_content)
            formatted["parent_content"] = parent_content

        return formatted

    def _extract_vf_instruction(self, content: str) -> str:
        """Extract only the instruction part from a vrai/faux or QCM parent question.

        Strips everything starting from the first numbered item (``1-``, ``1.``,
        ``1)``) or the first markdown table row (``| 1- ...`` / ``| --- |``),
        whichever comes first.

        Example: "Recopiez... (1pt)\n1- ...\n2- ..." → "Recopiez... (1pt)"
        Example: "Recopiez... (2 pts)\n|  1- Au Maroc..." → "Recopiez... (2 pts)"
        """
        if not content:
            return ""
        lines = content.split('\n')
        instruction_lines = []
        for line in lines:
            stripped = line.lstrip()
            # Stop at first numbered item at line start
            if re.match(r'^\s*1[-.)\s]', line):
                break
            # Stop at first markdown table row containing "1-" or at a separator row
            if stripped.startswith('|'):
                if re.search(r'\|\s*1[-.)\s]', line) or re.match(r'\|\s*-+\s*\|', stripped):
                    break
                # Any table row likely means the content body started
                break
            instruction_lines.append(line)
        return '\n'.join(instruction_lines).strip()

    # ---------------------------------------------------------------
    # Content cleanup helpers (shared by _format_question)
    # ---------------------------------------------------------------
    _CHOICE_LINE_RE = re.compile(r"^\s*[a-dA-D][\.\)\-]\s+")

    def _strip_qcm_choices(self, content: str) -> str:
        """Remove inline ``a./b./c./d.`` choice lines from a QCM question body.

        The choices are already rendered interactively on the right panel, so we
        keep only the question stem to avoid duplication.
        """
        if not content:
            return content
        out = []
        for line in content.split("\n"):
            if self._CHOICE_LINE_RE.match(line):
                # first choice line reached → stop collecting
                break
            out.append(line)
        # Trim trailing empty/punctuation-only lines
        while out and not out[-1].strip():
            out.pop()
        return "\n".join(out).strip()

    def _strip_association_table(self, content: str) -> str:
        """Remove the markdown table from an association question body.

        The ``items_left`` / ``items_right`` arrays are already rendered
        interactively, so the raw table only adds visual noise.
        """
        if not content:
            return content
        out = []
        in_table = False
        for line in content.split("\n"):
            stripped = line.lstrip()
            if stripped.startswith("|"):
                in_table = True
                continue
            if in_table and not stripped:
                # allow blank lines between table and further text
                continue
            if in_table and not stripped.startswith("|"):
                # text resumed after the table → keep everything from here
                in_table = False
            out.append(line)
        return "\n".join(out).strip()

    # Minimal LaTeX → Unicode map for common baccalauréat math snippets
    _LATEX_SIMPLE_SUBS = [
        (re.compile(r"\\rightarrow"), "→"),
        (re.compile(r"\\leftarrow"), "←"),
        (re.compile(r"\\Rightarrow"), "⇒"),
        (re.compile(r"\\leftrightarrow"), "↔"),
        (re.compile(r"\\times"), "×"),
        (re.compile(r"\\alpha\b"), "α"),
        (re.compile(r"\\beta\b"), "β"),
        (re.compile(r"\\gamma\b"), "γ"),
        (re.compile(r"\\delta\b"), "δ"),
        (re.compile(r"\\Delta\b"), "Δ"),
    ]
    # \mathrm{O}_2 → O₂  (subscript digits)
    _SUB_DIGIT_MAP = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
    _SUP_DIGIT_MAP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    _MATHRM_RE = re.compile(r"\\mathrm\{([^{}]*)\}")
    _SUB_RE = re.compile(r"_\{([0-9]+)\}|_([0-9])")
    _SUP_RE = re.compile(r"\^\{([0-9]+)\}|\^([0-9])")
    _MATH_DELIM_RE = re.compile(r"\$+([^$]*?)\$+")

    def _normalize_inline_math(self, text: str) -> str:
        """Best-effort LaTeX → Unicode for short inline math.

        Handles common constructs seen in Moroccan baccalauréat PDFs:
        ``\\rightarrow``, ``\\mathrm{X}``, ``_{N}`` / ``_N`` subscripts,
        ``^{N}`` / ``^N`` superscripts.  Non-convertible LaTeX passes through
        stripped of ``$`` delimiters so at least it is readable.

        For mathematics exams, this normalization is disabled so the raw
        LaTeX (``$...$`` / ``$$...$$``) is delivered as-is to the frontend
        where KaTeX renders it properly.
        """
        # Skip normalization entirely for subjects whose JSON uses proper LaTeX
        # ($...$ / $$...$$) — the frontend renders these via KaTeX. Stripping the
        # delimiters here would leave unrendered commands like "\tau" in the UI.
        subject = (getattr(self, "_current_subject", "") or "").lower()
        latex_subjects = {
            "mathematiques", "mathématiques", "maths", "math",
            "physique", "physique-chimie", "physique chimie", "pc", "chimie",
        }
        if subject in latex_subjects:
            return text

        if not text or "\\" not in text and "$" not in text and "_" not in text and "^" not in text:
            return text

        def _convert_inside_math(m: re.Match) -> str:
            s = m.group(1)
            for rx, repl in self._LATEX_SIMPLE_SUBS:
                s = rx.sub(repl, s)
            s = self._MATHRM_RE.sub(lambda mm: mm.group(1), s)
            s = self._SUB_RE.sub(lambda mm: (mm.group(1) or mm.group(2)).translate(self._SUB_DIGIT_MAP), s)
            s = self._SUP_RE.sub(lambda mm: (mm.group(1) or mm.group(2)).translate(self._SUP_DIGIT_MAP), s)
            return s

        # First, convert content inside $...$ delimiters (unwrap them)
        text = self._MATH_DELIM_RE.sub(_convert_inside_math, text)
        # Then convert any stray LaTeX still present outside $...$
        for rx, repl in self._LATEX_SIMPLE_SUBS:
            text = rx.sub(repl, text)
        text = self._MATHRM_RE.sub(lambda mm: mm.group(1), text)
        text = self._SUB_RE.sub(lambda mm: (mm.group(1) or mm.group(2)).translate(self._SUB_DIGIT_MAP), text)
        text = self._SUP_RE.sub(lambda mm: (mm.group(1) or mm.group(2)).translate(self._SUP_DIGIT_MAP), text)
        return text

    def _structure_legacy_exam(self, raw: dict, meta: dict) -> dict:
        """Parse the legacy format with 'blocks' array."""
        blocks = raw.get("blocks", raw) if isinstance(raw, dict) else raw
        if isinstance(raw, dict) and "blocks" in raw:
            blocks = raw["blocks"]

        questions = []
        corrections = []
        context_blocks = []
        current_documents = []

        for i, block in enumerate(blocks):
            btype = block.get("type", "")
            origin = block.get("origin", "")

            if origin == "correction" or btype == "answer":
                corrections.append({
                    "content": block.get("content", ""),
                    "details": block.get("details", {}),
                })
                continue

            if btype == "question":
                # Determine question type from content
                content = block.get("content", "")
                q_type = self._detect_question_type(content)
                
                # Check if next block is a QCM table
                if (i + 1 < len(blocks) and 
                    blocks[i + 1].get("type") == "table" and 
                    self._is_qcm_table(blocks[i + 1])):
                    
                    # Extract individual QCM sub-questions from the table
                    qcm_subquestions = self._extract_qcm_choices(blocks[i + 1])
                    
                    if qcm_subquestions:
                        # Create the main QCM question as a container
                        main_question = {
                            "index": len(questions),
                            "content": content,
                            "details": block.get("details", {}),
                            "context": list(context_blocks),
                            "documents": self._normalize_document_paths(current_documents),
                            "page_context": block.get("page_context", ""),
                            "points": self._extract_points(content),
                            "type": "qcm",
                            "sub_questions": []
                        }
                        
                        # Add each QCM sub-question
                        for sub_q in qcm_subquestions:
                            sub_question = {
                                "id": sub_q["id"],
                                "number": sub_q["number"],
                                "content": sub_q["content"],
                                "type": "qcm",
                                "points": sub_q["points"],
                                "choices": sub_q["choices"]
                            }
                            main_question["sub_questions"].append(sub_question)
                        
                        questions.append(main_question)
                    else:
                        # Fallback to regular question
                        question = {
                            "index": len(questions),
                            "content": content,
                            "details": block.get("details", {}),
                            "context": list(context_blocks),
                            "documents": self._normalize_document_paths(current_documents),
                            "page_context": block.get("page_context", ""),
                            "points": self._extract_points(content),
                            "type": q_type,
                        }
                        questions.append(question)
                else:
                    # Regular question
                    question = {
                        "index": len(questions),
                        "content": content,
                        "details": block.get("details", {}),
                        "context": list(context_blocks),
                        "documents": self._normalize_document_paths(current_documents),
                        "page_context": block.get("page_context", ""),
                        "points": self._extract_points(content),
                        "type": q_type,
                    }
                    questions.append(question)
                context_blocks = []
                current_documents = []
                
            elif btype in ("text", "schema", "table"):
                ctx = {
                    "type": btype,
                    "content": block.get("content", ""),
                    "details": block.get("details", {}),
                }
                if block.get("src"):
                    ctx["src"] = block["src"]
                    # Add to documents if it has an image
                    current_documents.append({
                        "id": f"doc_{len(current_documents)}",
                        "type": btype,
                        "title": block.get("details", {}).get("description", f"Document {len(current_documents) + 1}"),
                        "src": block["src"],
                        "description": block.get("details", {}).get("data_summary", "")
                    })
                context_blocks.append(ctx)

        # Pair corrections with questions
        paired = self._pair_corrections(questions, corrections)

        return {
            "id": meta["id"],
            "subject": meta["subject"],
            "year": meta["year"],
            "session": meta["session"],
            "duration_minutes": meta["duration_minutes"],
            "coefficient": meta.get("coefficient", 5),
            "total_points": meta.get("total_points", 20),
            "questions": paired,
            "question_count": len(paired),
        }

    def _detect_question_type(self, content: str) -> str:
        """Detect question type from content."""
        content_lower = content.lower()
        if "recopiez les couples" in content_lower or "proposition est correcte" in content_lower:
            return "qcm"
        elif "vrai" in content_lower and "faux" in content_lower:
            return "vrai_faux"
        elif "reliez" in content_lower or "associez" in content_lower:
            return "association"
        return "open"
    
    def _is_qcm_table(self, block: dict) -> bool:
        """Check if a table block contains QCM choices."""
        content = block.get("content", "")
        return ("a-" in content and "b-" in content and 
                ("c-" in content or "d-" in content))
    
    def _extract_qcm_choices(self, table_block: dict) -> list:
        """Extract QCM choices from a table block."""
        content = table_block.get("content", "")
        
        # Parse the 2x2 table format more carefully
        lines = [line.strip() for line in content.split("\n") if line.strip()]
        
        questions = {}
        current_questions_in_row = {}  # Track which questions are in the current row
        
        # Process each table row
        for line in lines:
            if line.startswith("|---") or not line.startswith("|"):
                continue
                
            # Split into cells and clean up
            cells = [cell.strip() for cell in line.split("|") if cell.strip()]
            
            # Check if this row contains question headers
            row_has_questions = any(any(cell.startswith(f"{i}-") for i in range(1, 5)) for cell in cells)
            
            if row_has_questions:
                # This is a question header row - reset current questions
                current_questions_in_row = {}
                for cell_idx, cell in enumerate(cells):
                    if any(cell.startswith(f"{i}-") for i in range(1, 5)):
                        question_num = cell[0]
                        question_text = cell[2:].strip().rstrip(" :")
                        questions[question_num] = {
                            "id": f"q{question_num}",
                            "number": question_num,
                            "content": question_text,
                            "type": "qcm",
                            "points": 0.5,
                            "choices": []
                        }
                        current_questions_in_row[cell_idx] = question_num
            else:
                # This is a choices row - assign choices to questions based on column
                for cell_idx, cell in enumerate(cells):
                    if any(cell.startswith(f"{letter}-") for letter in ["a", "b", "c", "d"]):
                        letter = cell[0]
                        choice_text = cell[2:].strip()
                        
                        # Find the question for this column
                        if cell_idx in current_questions_in_row:
                            question_num = current_questions_in_row[cell_idx]
                            if question_num in questions:
                                questions[question_num]["choices"].append({
                                    "letter": letter,
                                    "text": choice_text
                                })
        
        # Convert to list format
        result = []
        for q_num in sorted(questions.keys()):
            q = questions[q_num]
            if q["choices"]:  # Only include questions that have choices
                result.append(q)
        
        return result
    
    def _normalize_document_paths(self, documents: list) -> list:
        """Normalize document src paths to use assets/ folder."""
        normalized = []
        for doc in documents:
            doc_copy = dict(doc)
            src = doc_copy.get("src", "")
            if src:
                # Extract filename and put in assets/
                filename = src.rsplit("/", 1)[-1] if "/" in src else src
                doc_copy["src"] = f"assets/{filename}"
            normalized.append(doc_copy)
        return normalized
    
    def _extract_points(self, content: str) -> float:
        """Try to extract point value from question text like '(1.5pt)' or '(0.5pts)'."""
        import re
        match = re.search(r"\((\d+(?:[.,]\d+)?)\s*pts?\)", content, re.IGNORECASE)
        if match:
            return float(match.group(1).replace(",", "."))
        return 0

    def _pair_corrections(self, questions: list, corrections: list) -> list:
        """Best-effort pairing of corrections to questions."""
        if len(corrections) == len(questions):
            for i, q in enumerate(questions):
                q["correction"] = corrections[i]
            return questions
        for q in questions:
            q["correction"] = None
        for i, c in enumerate(corrections):
            if i < len(questions):
                questions[i]["correction"] = c
        return questions

    def get_question(self, exam_id: str, question_index: int) -> dict | None:
        """Return a single question with its context."""
        exam = self.get_exam(exam_id)
        if not exam:
            return None
        questions = exam["questions"]
        if question_index < 0 or question_index >= len(questions):
            return None
        return questions[question_index]

    # ------------------------------------------------------------------ #
    #  Assets path
    # ------------------------------------------------------------------ #

    def get_assets_dir(self, exam_id: str) -> Path | None:
        # Mock exams: assets under data/mock_exams/<subject>/<id>/assets
        mock_dir = _find_mock_exam_dir(exam_id)
        if mock_dir is not None:
            assets_dir = mock_dir / "assets"
            return assets_dir if assets_dir.exists() else None
        meta = self.get_exam_meta(exam_id)
        if not meta:
            return None
        assets_dir = EXAMS_DIR / meta["path"] / "assets"
        if not assets_dir.exists():
            return None
        return assets_dir

    # ------------------------------------------------------------------ #
    #  Evaluate answer (LLM-based)
    # ------------------------------------------------------------------ #

    async def evaluate_answer(
        self,
        exam_id: str,
        question_index: int,
        student_answer: str,
        student_image: str | None = None,
    ) -> dict:
        """Use LLM to evaluate a student's answer against the official correction.
        If student_image (base64) is provided, uses Gemini Vision to analyze it first."""
        question = self.get_question(exam_id, question_index)
        if not question:
            return {"error": "Question not found"}

        question_type = question.get("type", "open")
        correction = question.get("correction") or {}

        # Closed-form questions are graded deterministically from
        # ``correct_answer`` / ``correct_pairs`` and do NOT require a
        # ``correction`` field. Many BAC datasets only ship those keys for
        # QCM / vrai-faux / association — fail fast for OPEN questions only.
        if question_type in ["qcm", "vrai_faux"] and not student_image:
            if question.get("correct_answer") in (None, ""):
                return {"error": "No correct answer available for this question"}
            return self._evaluate_closed_question(question, correction, student_answer, question_index)
        if question_type == "association" and not student_image:
            if not (question.get("correct_pairs") or correction.get("correct_pairs")):
                return {"error": "No correct pairs available for this question"}
            return self._evaluate_association(question, correction, student_answer, question_index)

        if not correction:
            return {"error": "No correction available for this question"}

        # --- Image analysis with Gemini Vision ---
        image_analysis = None
        if student_image:
            from app.services.vision_service import analyze_student_image
            image_analysis = await analyze_student_image(
                image_base64=student_image,
                question_content=question["content"],
                correction_content=correction.get("content", "") or "",
                question_type=question_type,
            )
            # Enrich student_answer with extracted text from image
            if image_analysis.get("extracted_text"):
                extracted = image_analysis["extracted_text"]
                student_answer = f"{student_answer}\n\n[Contenu extrait de l'image de l'élève]:\n{extracted}" if student_answer.strip() else extracted

        from app.services.llm_service import llm_service

        prompt = self._build_eval_prompt(question, correction, student_answer, image_analysis)
        try:
            response = await llm_service.chat(
                messages=[{"role": "user", "content": prompt}],
                system_prompt=(
                    "Tu es un correcteur BIENVEILLANT, JUSTE et FLEXIBLE du BAC marocain (2ème BAC Sciences Physiques BIOF).\n\n"
                    "PRINCIPES FONDAMENTAUX:\n"
                    "1) Tu corriges des LYCÉENS de 17-18 ans, pas des doctorants. Sois tolérant sur la formulation.\n"
                    "2) Si un élément est scientifiquement VRAI et PERTINENT à la question, il est CORRECT — même s'il n'est pas dans la correction officielle.\n"
                    "3) JAMAIS de 0 si l'élève a fourni au moins UN élément partiellement correct ou pertinent. Un 0 signifie que RIEN n'est correct.\n"
                    "4) Note PROPORTIONNELLE: chaque élément correct = fraction de la note. Ex: 1 bon élément sur 4 demandés = au moins 25% de la note.\n"
                    "5) Ne fais PAS de distinction pédante entre 'caractéristique', 'propriété', 'élément structural', etc. — en SVT/BAC, ce sont des synonymes acceptables.\n"
                    "6) La correction officielle montre des EXEMPLES, pas les SEULES réponses possibles.\n"
                    "7) NIVEAU 2BAC STRICT : ta « réponse attendue en mieux » et tes explications restent au NIVEAU LYCÉE 2BAC PC. "
                    "N'invoque JAMAIS de notion universitaire (espaces vectoriels, opérateurs, lagrangien, thermodynamique ΔG/ΔS, RMN, mécanismes SN/E, immunologie/photosynthèse pour PC, etc.). "
                    "Reste sur les formules / vocabulaire / méthodes du programme officiel BIOF. Si la correction officielle utilise une formulation simple, NE la remplace pas par une version plus 'rigoureuse'."
                ),
                temperature=0.2,
                max_tokens=650 if image_analysis else 450,
            )
            points_max = float(question.get("points", 0) or 0)
            score = self._extract_score_from_feedback(response, points_max)
            result = {
                "question_index": question_index,
                "points_max": points_max,
                "score": score,
                "feedback": response,
                "correction": correction.get("content", "") or "",
            }
            if image_analysis:
                result["image_analysis"] = {
                    "extracted_text": image_analysis.get("extracted_text", ""),
                    "errors_found": image_analysis.get("errors_found", []),
                    "curve_analysis": image_analysis.get("curve_analysis"),
                }
            return result
        except Exception as e:
            return {"error": str(e)}

    def _evaluate_closed_question(
        self,
        question: dict,
        correction: dict,
        student_answer: str,
        question_index: int,
    ) -> dict:
        question_type = question.get("type", "open")
        points_max = question.get("points", 0)
        raw_correct_answer = question.get("correct_answer")

        normalized_student = self._normalize_closed_answer(student_answer, question_type)
        normalized_correct = self._normalize_closed_answer(raw_correct_answer, question_type)
        is_correct = normalized_student == normalized_correct and normalized_student != ""
        awarded_points = points_max if is_correct else 0

        # Build a concise, non-duplicative feedback for QCM / vrai-faux
        correct_choice_text = self._get_correct_choice_text(question, normalized_correct, question_type)

        if is_correct:
            feedback = (
                f"## Note\n{awarded_points}/{points_max}\n\n"
                f"## Appréciation générale\n"
                f"Bonne réponse ! Tu as bien identifié la bonne proposition. "
                f"Continue à bien lire chaque proposition avant de valider."
            )
        else:
            answer_label = self._format_closed_answer_label(normalized_student, question_type)
            # Build explanation from question content + correct choice
            explanation = self._build_closed_explanation(question, correction, correct_choice_text, question_type)

            feedback = (
                f"## Note\n{awarded_points}/{points_max}\n\n"
                f"## Appréciation générale\n"
                f"Ta réponse ({answer_label}) n'est pas correcte.\n\n"
                f"## Conseil méthode\n"
                f"Lis chaque proposition en te demandant si elle est cohérente avec le cours. Élimine d'abord celles qui sont clairement fausses.\n\n"
                f"## Réponse attendue en mieux\n"
                f"{explanation}"
            )

        return {
            "question_index": question_index,
            "points_max": points_max,
            "score": float(awarded_points),
            "feedback": feedback,
            "correction": correction.get("content", "") or "",
        }

    def _evaluate_association(
        self,
        question: dict,
        correction: dict,
        student_answer: str,
        question_index: int,
    ) -> dict:
        """Deterministic evaluation of an association question.

        Parses pairs like '(1,e) (2,g) (3,f)' from the student answer and
        compares against question['correct_pairs']. Partial credit per
        correct pair. Works with any letter (a-z) for right items.
        """
        points_max = question.get("points", 0) or 0
        correct_pairs_raw = question.get("correct_pairs") or correction.get("correct_pairs") or []
        items_left = question.get("items_left") or []
        items_right = question.get("items_right") or []

        # Build correct map: {left_num(str) → right_letter(str)}
        correct_map: dict[str, str] = {}
        if isinstance(correct_pairs_raw, list):
            for p in correct_pairs_raw:
                if isinstance(p, dict):
                    left = str(p.get("left", "")).strip().lower()
                    right = str(p.get("right", "")).strip().lower()
                    if left and right:
                        correct_map[left] = right
        elif isinstance(correct_pairs_raw, dict):
            for k, v in correct_pairs_raw.items():
                correct_map[str(k).strip().lower()] = str(v).strip().lower()

        # Parse student pairs: "(1,e) (2,g)..." or "1-e;2-g" etc.
        student_map: dict[str, str] = {}
        for m in re.finditer(r"\(?(\d+)\s*[,\-)]\s*([a-z])\)?", student_answer or "", flags=re.IGNORECASE):
            student_map[m.group(1)] = m.group(2).lower()

        total_expected = len(correct_map)
        if total_expected == 0:
            # No correct pairs defined → fall back to LLM-style feedback
            return {
                "question_index": question_index,
                "points_max": points_max,
                "score": 0.0,
                "feedback": f"## Note\n0/{points_max}\n\nImpossible d'évaluer automatiquement (pas de corrigé d'association disponible).",
                "correction": correction.get("content", "") or "",
            }

        correct_count = sum(1 for k, v in correct_map.items() if student_map.get(k) == v)
        per_pair = points_max / total_expected if total_expected else 0
        awarded = round(correct_count * per_pair, 2)

        # Build per-pair feedback using item labels when available
        def _left_label(idx_str: str) -> str:
            try:
                i = int(idx_str) - 1
                if 0 <= i < len(items_left):
                    return str(items_left[i])
            except Exception:
                pass
            return idx_str

        def _right_label(letter: str) -> str:
            if not letter:
                return ""
            i = ord(letter.lower()) - ord("a")
            if 0 <= i < len(items_right):
                return str(items_right[i])
            return letter.upper()

        lines: list[str] = []
        for left, right_correct in sorted(correct_map.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 0):
            student_right = student_map.get(left, "")
            if student_right == right_correct:
                lines.append(f"- ✅ {_left_label(left)} → {_right_label(right_correct)}")
            else:
                student_part = _right_label(student_right) if student_right else "_(non répondu)_"
                lines.append(
                    f"- ❌ {_left_label(left)} → {student_part} "
                    f"(attendu : **{_right_label(right_correct)}**)"
                )

        if correct_count == total_expected:
            header = (
                f"## Note\n{awarded}/{points_max}\n\n"
                f"## Appréciation générale\nExcellent ! Toutes les associations sont correctes."
            )
        elif correct_count == 0:
            header = (
                f"## Note\n{awarded}/{points_max}\n\n"
                f"## Appréciation générale\nAucune association correcte. Relis attentivement la liste des termes et observe bien les figures."
            )
        else:
            header = (
                f"## Note\n{awarded}/{points_max}\n\n"
                f"## Appréciation générale\n{correct_count}/{total_expected} associations correctes."
            )

        feedback = header + "\n\n## Détail\n" + "\n".join(lines)

        corr_text = (correction.get("content", "") or "").strip()
        if corr_text:
            feedback += f"\n\n## Correction officielle\n{corr_text}"

        return {
            "question_index": question_index,
            "points_max": points_max,
            "points_awarded": awarded,
            "score": float(awarded),
            "feedback": feedback,
            "correction": corr_text,
        }

    def _normalize_closed_answer(self, answer, question_type: str) -> str:
        if answer is None:
            return ""

        value = str(answer).strip().lower()
        if question_type == "vrai_faux":
            if value in ["true", "vrai", "v"]:
                return "vrai"
            if value in ["false", "faux", "f"]:
                return "faux"
        return value

    def _format_closed_answer_label(self, answer: str, question_type: str) -> str:
        if not answer:
            return "Aucune réponse"
        if question_type == "qcm":
            return f"option {answer.upper()}"
        if question_type == "vrai_faux":
            return answer.capitalize()
        return answer

    def _get_correct_choice_text(self, question: dict, normalized_correct: str, question_type: str) -> str:
        """Get the text of the correct choice for QCM, or 'Vrai'/'Faux' for vrai_faux."""
        if question_type == "qcm":
            choices = question.get("choices", [])
            selected = next(
                (c for c in choices if str(c.get("letter", "")).strip().lower() == normalized_correct),
                None,
            )
            if selected:
                return f"{selected['letter'].upper()} : {selected['text']}"
            return f"option {normalized_correct.upper()}"
        if question_type == "vrai_faux":
            return normalized_correct.capitalize()
        return ""

    def _build_closed_explanation(self, question: dict, correction: dict, correct_choice_text: str, question_type: str) -> str:
        """Build an explanation for a wrong QCM / vrai-faux answer.
        
        Structure: state the correct answer once, then explain WHY using
        the question stem + the correct choice text.  No duplication.
        """
        q_content = question.get("content", "").strip()

        if question_type == "qcm":
            # Build a concept sentence from question stem + correct choice
            # e.g. "La lutte biologique :" + "B : se base sur l'introduction..."
            # → "La lutte biologique se base sur l'introduction des organismes..."
            if q_content.endswith(":") or q_content.endswith("："):
                stem = q_content.rstrip(":：").strip()
                choice_text = correct_choice_text.split(" : ", 1)[-1] if " : " in correct_choice_text else ""
                if choice_text:
                    explanation = f"La bonne réponse est {correct_choice_text.split(' : ')[0]}. {stem} {choice_text.rstrip('.')}."
                else:
                    explanation = f"La bonne réponse est {correct_choice_text}."
            else:
                explanation = f"La bonne réponse est {correct_choice_text}."
        elif question_type == "vrai_faux":
            explanation = f"La bonne réponse est : {correct_choice_text}."
            if q_content:
                if correct_choice_text.lower() == "vrai":
                    explanation += f"\nL'affirmation « {q_content.rstrip('.')} » est effectivement correcte."
                else:
                    explanation += f"\nL'affirmation « {q_content.rstrip('.')} » est incorrecte."
        else:
            explanation = correct_choice_text

        # Append any extra explanation from the correction content (if it's not just "Réponse correcte : X")
        corr_content = (correction.get("content", "") or "").strip() if correction else ""
        useful_content = re.sub(r"(?i)r[ée]ponse\s+correcte\s*:\s*\w+\.?\s*", "", corr_content).strip()
        if useful_content and useful_content.lower() not in explanation.lower():
            explanation += f"\n{useful_content}"

        return explanation

    def _build_eval_prompt(self, question: dict, correction: dict, student_answer: str, image_analysis: dict | None = None) -> str:
        context_text = ""
        for ctx in question.get("context", []):
            context_text += f"\n[{ctx['type'].upper()}]: {ctx['content']}"

        part_name = (question.get("part") or "").lower()
        question_type = question.get("type", "open")
        is_knowledge = "connaissance" in part_name or "restitution" in part_name
        evaluation_focus = (
            "ÉTAPE 1: Lis la question — combien d'éléments sont demandés? Quel type de réponse? ÉTAPE 2: Lis la réponse de l'élève — ses éléments sont-ils scientifiquement corrects? ÉTAPE 3: La correction officielle donne des EXEMPLES de bonnes réponses, mais d'autres réponses correctes existent. Note = (éléments corrects fournis / éléments demandés par la question) × note max."
            if is_knowledge
            else "ÉTAPE 1: Identifie les étapes de raisonnement que la QUESTION exige. ÉTAPE 2: Vérifie si le raisonnement de l'élève est scientifiquement valide. ÉTAPE 3: La correction officielle montre UN chemin possible — si l'élève suit un chemin différent mais scientifiquement correct, c'est VALIDE."
        )
        tone_guidance = (
            "IMPORTANT: Si la question demande N éléments et l'élève en donne N qui sont scientifiquement corrects (même s'ils diffèrent de la correction officielle), c'est la note COMPLÈTE. La correction = guide, pas checklist."
            if is_knowledge
            else "IMPORTANT: Valorise tout raisonnement scientifiquement correct, même s'il ne suit pas exactement le chemin de la correction officielle. Pénalise uniquement les erreurs scientifiques et les éléments manquants PAR RAPPORT À LA QUESTION (pas par rapport à la correction)."
        )
        type_guidance = {
            "qcm": "Si c'est un QCM, indique très clairement si la réponse choisie est correcte ou non, puis explique brièvement pourquoi.",
            "vrai_faux": "Si c'est une question vrai/faux, indique clairement si l'affirmation est vraie ou fausse et justifie en une ou deux phrases.",
            "schema": "Si c'est une question liée à un schéma, vérifie l'identification correcte des éléments et la cohérence des relations entre eux.",
            "open": "Si c'est une question ouverte, évalue le fond scientifique, l'organisation et la formulation.",
        }.get(question_type, "Évalue le fond scientifique, la méthode et la clarté.")

        # Build image analysis block if present
        image_block = ""
        if image_analysis:
            image_block = "\n\nANALYSE DE L'IMAGE FOURNIE PAR L'ÉLÈVE (extraite par Vision IA):"
            if image_analysis.get("extracted_text"):
                image_block += f"\nTexte extrait: {image_analysis['extracted_text']}"
            if image_analysis.get("elements"):
                image_block += f"\nÉléments de réponse identifiés: {image_analysis['elements']}"
            if image_analysis.get("errors_found"):
                image_block += f"\nErreurs détectées dans l'image: {'; '.join(image_analysis['errors_found'])}"
            if image_analysis.get("curve_analysis"):
                image_block += f"\nAnalyse courbe/schéma: {image_analysis['curve_analysis']}"
            image_block += "\n\nIMPORTANT: Base ton évaluation sur TOUT ce que l'élève a fourni (texte + image). L'image fait partie intégrante de la réponse."

        return f"""Corrige une réponse du BAC marocain en suivant cette méthode OBLIGATOIRE en 3 étapes.

═══ ÉTAPE 1 — ANALYSE DE LA QUESTION ═══
QUESTION ({question.get('points', '?')} pts)
{question['content']}
{context_text}
TYPE: {question_type} | PARTIE: {question.get('part', 'Non précisée')}

→ Combien d'éléments la QUESTION demande-t-elle? Quel type de réponse attend-elle?

═══ ÉTAPE 2 — ANALYSE DE LA RÉPONSE ÉLÈVE ═══
{student_answer}{image_block}

→ Quels éléments l'élève a-t-il fournis? Sont-ils scientifiquement CORRECTS?

═══ ÉTAPE 3 — COMPARAISON AVEC LA CORRECTION (GUIDE, PAS CHECKLIST) ═══
{correction['content']}

→ La correction montre des EXEMPLES de bonnes réponses. D'autres réponses scientifiquement correctes sont AUSSI VALIDES.

═══ RÈGLES DE NOTATION ═══
- {evaluation_focus}
- {tone_guidance}
- {type_guidance}
- RÈGLE ANTI-ZÉRO: Si l'élève a donné AU MOINS un élément scientifiquement vrai et pertinent → la note ne peut PAS être 0. Un 0 = réponse totalement fausse ou vide.
- NOTE PROPORTIONNELLE: Chaque élément correct de l'élève = une fraction de la note. Ex: question à 1pt demandant 4 éléments, 1 correct = 0.25pt minimum.
- TOLÉRANCE TERMINOLOGIQUE: Ne distingue PAS entre "caractéristique", "propriété", "élément", "composante", etc. Si c'est scientifiquement vrai ET pertinent au sujet → c'est CORRECT.
- EXEMPLE 1: "Citez 2 caractéristiques d'une chaîne de subduction". Si l'élève dit "prisme d'accrétion" → c'est une caractéristique VALIDE d'une zone de subduction, même si la correction dit "fosse océanique".
- EXEMPLE 2: Si la question demande "2 procédures de valorisation" et l'élève cite "méthanisation, compostage" (2 réponses correctes) → note COMPLÈTE même si la correction cite d'autres réponses.
- Accepte les synonymes, reformulations et formulations simples si le sens scientifique est correct.
- Ne pénalise QUE les erreurs factuelles (faux scientifiquement) et les éléments manquants PAR RAPPORT À LA QUESTION.

Réponds en français simple avec EXACTEMENT ce format:

## Note
X/{question.get('points', '?')}

## Appréciation générale
1 phrase courte.

## Points réussis
- 1 ou 2 puces courtes, ou "Aucun élément clé n'est présent."

## Ce qu'il faut améliorer
- 1 ou 2 puces courtes et concrètes (seulement si des éléments manquent PAR RAPPORT À LA QUESTION).

## Conseil méthode
1 phrase courte et actionnable.

## Réponse attendue en mieux
2 à 4 lignes maximum, claires et complètes.
"""

    # ------------------------------------------------------------------ #
    #  Submit full exam (real mode)
    # ------------------------------------------------------------------ #

    # ------------------------------------------------------------------ #
    #  Start an attempt (creates an in-progress row as soon as the
    #  student opens an exam, so dashboards can show activity).
    # ------------------------------------------------------------------ #

    async def start_attempt(
        self,
        student_id: str,
        exam_id: str,
        mode: str = "practice",
    ) -> dict:
        """Create an in-progress exam_attempts row (completed_at IS NULL).

        If an in-progress row already exists for this (student, exam, mode),
        we reuse it so the student can resume seamlessly.
        """
        meta = self.get_exam_meta(exam_id)
        if not meta:
            return {"error": "Exam not found"}

        # Reuse existing in-progress row if present
        try:
            existing = (
                self.supabase.table("exam_attempts")
                .select("id, answers, current_question_index, duration_seconds")
                .eq("student_id", student_id)
                .eq("exam_subject", meta["subject"])
                .eq("exam_year", meta["year"])
                .eq("exam_session", (meta["session"] or "").lower())
                .eq("mode", mode)
                .is_("completed_at", "null")
                .order("started_at", desc=True)
                .limit(1)
                .execute()
            )
            if existing.data:
                row = existing.data[0]
                return {
                    "attempt_id": row["id"],
                    "resumed": True,
                    "answers": row.get("answers") or {},
                    "current_question_index": row.get("current_question_index") or 0,
                    "duration_seconds": row.get("duration_seconds") or 0,
                }
        except Exception as e:
            print(f"[EXAM] Lookup existing attempt failed: {e}")

        attempt_id = str(uuid.uuid4())
        try:
            self.supabase.table("exam_attempts").insert({
                "id": attempt_id,
                "student_id": student_id,
                "exam_id": exam_id,
                "exam_subject": meta["subject"],
                "exam_year": meta["year"],
                "exam_session": (meta["session"] or "").lower(),
                "mode": mode,
                "answers": {},
                "scores": {},
                "total_score": 0,
                "max_score": meta.get("total_points", 20),
                "duration_seconds": 0,
                "current_question_index": 0,
            }).execute()
        except Exception as e:
            print(f"[EXAM] start_attempt insert failed: {e}")
            return {"error": str(e)}
        return {"attempt_id": attempt_id, "resumed": False}

    # ------------------------------------------------------------------ #
    #  Save progress on an in-progress attempt (periodic autosave)
    # ------------------------------------------------------------------ #

    async def save_progress(
        self,
        student_id: str,
        attempt_id: str,
        answers: dict | None = None,
        current_question_index: int | None = None,
        duration_seconds: int | None = None,
    ) -> dict:
        updates: dict = {}
        if answers is not None:
            updates["answers"] = answers
        if current_question_index is not None:
            updates["current_question_index"] = int(current_question_index)
        if duration_seconds is not None:
            updates["duration_seconds"] = int(duration_seconds)
        if not updates:
            return {"ok": True, "noop": True}
        try:
            res = (
                self.supabase.table("exam_attempts")
                .update(updates)
                .eq("id", attempt_id)
                .eq("student_id", student_id)
                .execute()
            )
            if not res.data:
                return {"error": "attempt not found"}
            return {"ok": True, "attempt_id": attempt_id}
        except Exception as e:
            print(f"[EXAM] save_progress failed: {e}")
            return {"error": str(e)}

    async def record_practice_score(
        self,
        student_id: str,
        attempt_id: str,
        question_index: int,
        score: float,
        points_max: float,
    ) -> dict:
        """Persist a per-question score on an in-progress attempt (practice mode).

        Updates the ``scores`` JSON column with ``{question_index: score}`` and
        recomputes ``total_score`` from the sum of recorded scores. ``max_score``
        is left untouched (it stores the exam's total points). This lets the
        dashboard show partial avg even before the student finalises the exam.
        """
        try:
            row = (
                self.supabase.table("exam_attempts")
                .select("scores")
                .eq("id", attempt_id)
                .eq("student_id", student_id)
                .limit(1)
                .execute()
            )
            if not row.data:
                return {"error": "attempt not found"}
            current_scores = row.data[0].get("scores") or {}
            if not isinstance(current_scores, dict):
                current_scores = {}
            current_scores[str(question_index)] = {
                "s": float(score or 0),
                "m": float(points_max or 0),
            }
            new_total = sum(
                float(v.get("s") or 0) if isinstance(v, dict) else float(v or 0)
                for v in current_scores.values()
            )
            self.supabase.table("exam_attempts").update({
                "scores": current_scores,
                "total_score": round(new_total, 2),
            }).eq("id", attempt_id).eq("student_id", student_id).execute()
            return {"ok": True}
        except Exception as e:
            print(f"[EXAM] record_practice_score failed: {e}")
            return {"error": str(e)}

    async def submit_exam(
        self,
        student_id: str,
        exam_id: str,
        answers: dict,  # {question_index: student_answer}
        mode: str = "practice",
        duration_seconds: int = 0,
        attempt_id: str | None = None,
    ) -> dict:
        """Submit a full exam attempt: evaluate all answers, compute total score, save to DB.

        If ``attempt_id`` is provided AND points to an existing in-progress row,
        we UPDATE that row (set completed_at) rather than inserting a new one.
        """
        exam = self.get_exam(exam_id)
        if not exam:
            return {"error": "Exam not found"}

        meta = self.get_exam_meta(exam_id)
        scores = {}
        feedbacks = {}
        total_score = 0

        semaphore = asyncio.Semaphore(4)

        async def _evaluate_one(q_idx_str: str, student_answer: str):
            q_idx = int(q_idx_str)
            async with semaphore:
                result = await self.evaluate_answer(exam_id, q_idx, student_answer)
            return q_idx_str, q_idx, result

        evaluation_tasks = [
            _evaluate_one(q_idx_str, student_answer)
            for q_idx_str, student_answer in answers.items()
            if student_answer and str(student_answer).strip()
        ]

        for q_idx_str, q_idx, result in await asyncio.gather(*evaluation_tasks):
            if "error" not in result:
                score = self._extract_score_from_feedback(
                    result.get("feedback", ""),
                    exam["questions"][q_idx].get("points", 0),
                )
                scores[q_idx_str] = score
                total_score += score
                feedbacks[q_idx_str] = result.get("feedback", "")

        # Save / finalize attempt in DB
        from datetime import datetime as _dt
        final_payload = {
            "student_id": student_id,
            "exam_id": exam_id,
            "exam_subject": meta["subject"],
            "exam_year": meta["year"],
            "exam_session": (meta["session"] or "").lower(),
            "mode": mode,
            "answers": answers,
            "scores": scores,
            "total_score": total_score,
            "max_score": meta.get("total_points", 20),
            "duration_seconds": duration_seconds,
            "completed_at": _dt.utcnow().isoformat(),
        }
        try:
            if attempt_id:
                res = (
                    self.supabase.table("exam_attempts")
                    .update(final_payload)
                    .eq("id", attempt_id)
                    .eq("student_id", student_id)
                    .execute()
                )
                if not res.data:
                    # Row not found — fall back to insert
                    attempt_id = str(uuid.uuid4())
                    self.supabase.table("exam_attempts").insert(
                        {"id": attempt_id, **final_payload}
                    ).execute()
            else:
                attempt_id = str(uuid.uuid4())
                self.supabase.table("exam_attempts").insert(
                    {"id": attempt_id, **final_payload}
                ).execute()
        except Exception as e:
            print(f"[EXAM] Failed to save attempt: {e}")
            if not attempt_id:
                attempt_id = str(uuid.uuid4())

        # ── Feed proficiency agent with every answer (batched — single recompute) ──
        try:
            from app.services.student_proficiency_service import proficiency_service
            for q_idx_str, student_answer in answers.items():
                q_idx = int(q_idx_str)
                if q_idx >= len(exam["questions"]):
                    continue
                q = exam["questions"][q_idx]
                q_score = scores.get(q_idx_str, 0)
                q_max = q.get("points", 1) or 1
                is_correct = q_score >= q_max * 0.6  # 60%+ = correct
                await proficiency_service.record_answer(
                    student_id=student_id,
                    subject=meta.get("subject", ""),
                    topic=q.get("exercise", q.get("part", "")),
                    question_content=q.get("content", "")[:300],
                    student_answer=str(student_answer)[:300],
                    correct_answer=q.get("correction", {}).get("content", "")[:300] if isinstance(q.get("correction"), dict) else str(q.get("correction", ""))[:300],
                    is_correct=is_correct,
                    question_type=q.get("type", "open"),
                    score=q_score,
                    max_score=q_max,
                    source="exam_real",
                    exam_id=exam_id,
                    exercise_name=q.get("exercise", ""),
                    part_name=q.get("part", ""),
                    year=str(meta.get("year", "")),
                    skip_update=True,  # Don't recompute after each answer
                )
            # Single recompute after all answers recorded
            await proficiency_service.flush_proficiency(student_id)
        except Exception as e:
            print(f"[EXAM] Failed to feed proficiency agent: {e}")

        return {
            "attempt_id": attempt_id,
            "total_score": total_score,
            "max_score": meta.get("total_points", 20),
            "scores": scores,
            "feedbacks": feedbacks,
            "question_count": len(exam["questions"]),
            "answered_count": len(answers),
        }

    def _extract_score_from_feedback(self, feedback: str, max_points: float) -> float:
        """Try to extract numeric score from LLM feedback like 'Note: 1.5/2'."""
        import re
        match = re.search(r"(?:##\s*Note|\*?\*?Note)\s*:?[ \t]*\n?[ \t]*(\d+(?:[.,]\d+)?)\s*/", feedback, re.IGNORECASE)
        if match:
            return min(float(match.group(1).replace(",", ".")), max_points)
        return 0

    # ------------------------------------------------------------------ #
    #  History
    # ------------------------------------------------------------------ #

    async def get_history(self, student_id: str, limit: int = 20) -> list:
        """Get exam attempt history for a student (includes in-progress attempts)."""
        result = self.supabase.table("exam_attempts").select(
            "id, exam_id, exam_subject, exam_year, exam_session, mode, "
            "total_score, max_score, duration_seconds, started_at, completed_at, "
            "current_question_index, answers"
        ).eq("student_id", student_id).order(
            "started_at", desc=True
        ).limit(limit).execute()
        rows = result.data or []
        # Derive convenient flags and counts for the frontend
        for r in rows:
            r["in_progress"] = r.get("completed_at") is None
            answers = r.get("answers") or {}
            if isinstance(answers, dict):
                r["answered_count"] = sum(
                    1 for v in answers.values() if v and str(v).strip()
                )
            else:
                r["answered_count"] = 0
            # Strip bulky answers payload from history listing
            r.pop("answers", None)
        return rows

    # ------------------------------------------------------------------ #
    #  Per-student aggregated stats (for the ExamHub hero + sharing)
    # ------------------------------------------------------------------ #

    async def get_student_exam_stats(self, student_id: str) -> dict:
        """Aggregate personal exam statistics for the given student.

        Returns:
          - exams_taken             : distinct (subject, year, session) completed
          - attempts                : total attempts (may include retries)
          - total_questions_answered: sum of answers keys across attempts
          - avg_score_pct / best_score_pct
          - total_duration_seconds  : total time spent on exam mode
          - by_subject[]            : per-subject breakdown with exams,
                                      questions, attempts, avg_score_pct
        """
        result = self.supabase.table("exam_attempts").select(
            "exam_subject, exam_year, exam_session, mode, answers, scores, "
            "total_score, max_score, duration_seconds, completed_at"
        ).eq("student_id", student_id).execute()

        attempts = result.data or []

        per_subject: dict[str, dict] = {}
        total_attempts = 0
        in_progress_count = 0
        total_questions = 0
        total_score_sum = 0.0
        total_max_sum = 0.0
        total_duration = 0
        best_pct = 0.0
        unique_exams: set[tuple] = set()

        for a in attempts:
            is_done = bool(a.get("completed_at"))
            if is_done:
                total_attempts += 1
            else:
                in_progress_count += 1
            subj = a.get("exam_subject", "Inconnu") or "Inconnu"
            answers = a.get("answers") or {}
            # answers stored as dict {question_index: str}; count non-empty
            if isinstance(answers, dict):
                q_count = sum(
                    1 for v in answers.values() if v and str(v).strip()
                )
            else:
                q_count = 0
            # Count answered questions from BOTH completed and in-progress
            # attempts so the dashboard counter moves as soon as the student types.
            total_questions += q_count
            total_duration += int(a.get("duration_seconds") or 0)

            ts = float(a.get("total_score") or 0)
            ms = float(a.get("max_score") or 0) or 20

            # For in-progress attempts, derive partial score / max from the
            # scores dict so that practice mode evaluations contribute to the
            # dashboard avg even before the exam is submitted.
            partial_score = 0.0
            partial_max = 0.0
            scores_dict = a.get("scores") or {}
            if isinstance(scores_dict, dict):
                for v in scores_dict.values():
                    if isinstance(v, dict):
                        partial_score += float(v.get("s") or 0)
                        partial_max += float(v.get("m") or 0)
                    else:
                        # legacy format: numeric score, no max recorded → skip
                        try:
                            partial_score += float(v or 0)
                        except (TypeError, ValueError):
                            pass

            bucket = per_subject.setdefault(subj, {
                "attempts": 0,
                "in_progress": 0,
                "questions": 0,
                "score_sum": 0.0,
                "max_sum": 0.0,
                "unique_exams": set(),
            })

            if is_done:
                total_score_sum += ts
                total_max_sum += ms
                pct = (ts / ms * 100) if ms else 0
                if pct > best_pct:
                    best_pct = pct

                exam_key = (subj, a.get("exam_year"), a.get("exam_session"))
                unique_exams.add(exam_key)

                bucket["attempts"] += 1
                bucket["score_sum"] += ts
                bucket["max_sum"] += ms
                bucket["unique_exams"].add(
                    (a.get("exam_year"), a.get("exam_session"))
                )
            else:
                bucket["in_progress"] += 1
                # Partial contribution from in-progress attempts (practice mode)
                if partial_max > 0:
                    total_score_sum += partial_score
                    total_max_sum += partial_max
                    bucket["score_sum"] += partial_score
                    bucket["max_sum"] += partial_max

            # Treat any attempt with at least one answered question as a
            # "taken" exam (real submitted OR practice with progress). This
            # prevents the Dashboard from showing "Pas encore de score" when
            # the student already practiced an exam and produced a score —
            # which previously contradicted a positive avg_score_pct. The
            # `unique_exams` set de-duplicates by (subject, year, session),
            # so re-attempting the same exam later won't double-count.
            if q_count > 0 or partial_max > 0:
                exam_key = (subj, a.get("exam_year"), a.get("exam_session"))
                unique_exams.add(exam_key)
                bucket["unique_exams"].add(
                    (a.get("exam_year"), a.get("exam_session"))
                )

            bucket["questions"] += q_count

        by_subject = sorted(
            [
                {
                    "subject": s,
                    "attempts": b["attempts"],
                    "in_progress": b["in_progress"],
                    "exams": len(b["unique_exams"]),
                    "questions": b["questions"],
                    "avg_score_pct": (
                        round(b["score_sum"] / b["max_sum"] * 100, 1)
                        if b["max_sum"] > 0 else 0.0
                    ),
                    "exams_detail": sorted(
                        [{"year": y, "session": se} for y, se in b["unique_exams"]],
                        key=lambda x: (-(x["year"] or 0), x["session"] or ""),
                    ),
                }
                for s, b in per_subject.items()
            ],
            key=lambda x: (-x["questions"], -x["exams"]),
        )

        avg_score_pct = (
            round(total_score_sum / total_max_sum * 100, 1)
            if total_max_sum > 0 else 0.0
        )

        # Global list of unique exams the student attempted
        exams_detail = sorted(
            [{"subject": s, "year": y, "session": se} for s, y, se in unique_exams],
            key=lambda x: (-(x["year"] or 0), x["subject"] or "", x["session"] or ""),
        )

        return {
            "exams_taken": len(unique_exams),
            "unique_exams_taken": len(unique_exams),  # alias used by Dashboard
            "attempts": total_attempts,
            "in_progress_count": in_progress_count,
            "total_questions_answered": total_questions,
            "avg_score_pct": avg_score_pct,
            "best_score_pct": round(best_pct, 1),
            "total_duration_seconds": total_duration,
            "by_subject": by_subject,
            "exams_detail": exams_detail,
        }


exam_service = ExamService()
