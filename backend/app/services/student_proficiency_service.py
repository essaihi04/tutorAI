"""
Student Proficiency Agent — Expert EdTech Edition
==================================================
Pedagogy-driven student tracking based on:
- Taxonomie de Bloom (cognitive levels: remembering → creating)
- Courbe d'oubli d'Ebbinghaus (exponential decay weighting)
- Zone Proximale de Développement de Vygotsky (ZPD)
- Différenciation pédagogique (adaptation au profil individuel)

Tracks every student answer, computes weighted proficiency, detects lacunes,
and generates rich pedagogical context for the LLM.
"""
import logging
import math
from datetime import datetime, timezone, timedelta
from typing import Optional
from collections import defaultdict
from app.supabase_client import get_supabase_admin

_log = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════
#  BLOOM'S TAXONOMY — Cognitive level weights
#  Higher levels = more weight in proficiency score
#  Restitution (remembering) < Compréhension < Application < Analyse
# ═══════════════════════════════════════════════════════════════
BLOOM_WEIGHTS = {
    "remembering":    1.0,   # QCM, vrai/faux — simple recall
    "understanding":  1.3,   # Open questions explaining concepts
    "applying":       1.6,   # Schema labeling, calculations
    "analyzing":      2.0,   # Raisonnement scientifique, multi-doc analysis
}

# Map question_type + part_name to Bloom level
def _bloom_level(question_type: str, part_name: str = "") -> str:
    part_lower = part_name.lower()
    if "raisonnement" in part_lower:
        return "analyzing"       # Partie 2: Raisonnement = high-order thinking
    if question_type in ("qcm", "vrai_faux"):
        return "remembering"     # Multiple choice = recall
    if question_type == "schema":
        return "applying"        # Schema labeling = application
    if "restitution" in part_lower:
        return "understanding"   # Partie 1: Restitution = understanding
    return "understanding"       # Default for open questions

# ═══════════════════════════════════════════════════════════════
#  EBBINGHAUS DECAY — Recent answers weighted more
#  Half-life = 14 days → answer from 14 days ago counts 50%
# ═══════════════════════════════════════════════════════════════
# Adaptive half-life: shorter when exam is close (urgency mode)
EXAM_DATE = datetime(2026, 6, 4, tzinfo=timezone.utc)

def _days_to_exam() -> int:
    return max(0, (EXAM_DATE - datetime.now(timezone.utc)).days)

def _adaptive_half_life() -> float:
    """Shorter half-life when exam is closer → recent data matters MORE."""
    days = _days_to_exam()
    if days <= 14:
        return 5.0    # Last 2 weeks: very aggressive recency
    elif days <= 30:
        return 7.0    # Last month: aggressive
    elif days <= 60:
        return 10.0   # ~2 months: moderate urgency
    return 14.0       # Relaxed

def _time_weight(created_at: str) -> float:
    """Exponential decay: recent answers count more. Adapts to exam proximity."""
    try:
        if isinstance(created_at, str):
            ts = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        else:
            ts = created_at
        age_days = (datetime.now(timezone.utc) - ts).total_seconds() / 86400
        half_life = _adaptive_half_life()
        return math.exp(-0.693 * age_days / half_life)  # ln(2) ≈ 0.693
    except Exception:
        return 0.5  # Fallback: moderate weight

# ═══════════════════════════════════════════════════════════════
#  CADRE DE RÉFÉRENCE BAC — 2ème BAC Sciences Physiques BIOF
#  Source: Cadre de référence de l'examen national du baccalauréat
# ═══════════════════════════════════════════════════════════════

# Official BAC coefficients for 2BAC Sciences Physiques
# These are the CANONICAL subject names used in the system
ALL_SUBJECTS = [
    "Mathematiques",
    "Physique", 
    "Chimie",
    "SVT",
]

# BAC coefficient weights (official) — 2BAC Sciences Physiques BIOF
# Source: Ministère de l'Éducation Nationale Marocain
BAC_COEFFICIENTS = {
    "Mathematiques": 7,
    "Physique": 7,
    "Chimie": 7,
    "SVT": 5,
    # Aliases for matching
    "Mathématiques": 7, "Maths": 7,
    "Sciences de la Vie et de la Terre (SVT)": 5,
}

# Total chapters per subject (from seed data)
SUBJECT_TOTAL_CHAPTERS = {
    "Mathematiques": 11,
    "Physique": 15,
    "Chimie": 14,
    "SVT": 4,
    # Aliases
    "Mathématiques": 11, "Maths": 11,
    "Sciences de la Vie et de la Terre (SVT)": 4,
}

# Normalize subject name to canonical form
def _normalize_subject(name: str) -> str:
    """Convert subject name variants to canonical form."""
    name_lower = name.lower().strip()
    if "math" in name_lower:
        return "Mathematiques"
    if "physi" in name_lower:
        return "Physique"
    if "chimi" in name_lower:
        return "Chimie"
    if "svt" in name_lower or "vie" in name_lower:
        return "SVT"
    return name  # Return as-is if unknown

# ═══════════════════════════════════════════════════════════════
#  PROFICIENCY LEVELS — Based on educational research thresholds
#  < 30% = not yet acquired (non acquis)
#  30-55% = in progress (en cours d'acquisition)
#  55-75% = acquired (acquis)
#  > 75% = mastered (maîtrisé)
# ═══════════════════════════════════════════════════════════════
LEVEL_THRESHOLDS = {
    "non acquis":             (0,  30),
    "en cours d'acquisition": (30, 55),
    "acquis":                 (55, 75),
    "maîtrisé":               (75, 100),
}


class StudentProficiencyService:
    """
    Core agent that:
    1. Records every answer (exam, chat, exercise)
    2. Computes per-topic proficiency scores (0-100)
    3. Identifies lacunes (weak topics needing reinforcement)
    4. Generates context string for LLM personalization
    5. Updates student_profiles in DB
    """

    def __init__(self):
        self._supabase = None

    @property
    def supabase(self):
        if self._supabase is None:
            self._supabase = get_supabase_admin()
        return self._supabase

    # ──────────────────────────────────────────────
    #  1. RECORD ANSWERS
    # ──────────────────────────────────────────────

    async def record_answer(
        self,
        student_id: str,
        subject: str,
        topic: str,
        question_content: str,
        student_answer: str,
        correct_answer: str,
        is_correct: bool,
        question_type: str = "open",
        score: float = 0,
        max_score: float = 1,
        source: str = "exam",
        exam_id: str = "",
        exercise_name: str = "",
        part_name: str = "",
        year: str = "",
        skip_update: bool = False,
    ) -> Optional[dict]:
        """Record a single student answer in the history table.
        Set skip_update=True when recording in batch (call flush_proficiency after)."""
        try:
            row = {
                "student_id": student_id,
                "subject": subject,
                "topic": topic or "Général",
                "question_content": question_content[:500],
                "student_answer": student_answer[:500],
                "correct_answer": correct_answer[:500],
                "is_correct": is_correct,
                "score": score,
                "max_score": max_score,
                "question_type": question_type,
                "source": source,
                "exam_id": exam_id,
                "exercise_name": exercise_name,
                "part_name": part_name,
                "year": year,
            }
            result = self.supabase.table("student_answer_history").insert(row).execute()
            _log.info(f"[Proficiency] Recorded answer: student={student_id[:8]}.. "
                      f"subject={subject} topic={topic} correct={is_correct} "
                      f"score={score}/{max_score} source={source}")

            # After recording, update proficiency summary (unless batching)
            if not skip_update:
                await self._update_proficiency_summary(student_id)

            return result.data[0] if result.data else None
        except Exception as e:
            _log.error(f"[Proficiency] Error recording answer: {e}")
            return None

    async def flush_proficiency(self, student_id: str):
        """Force a proficiency recompute. Call after batch recording."""
        await self._update_proficiency_summary(student_id)

    async def record_exam_answers_batch(
        self,
        student_id: str,
        answers: list[dict],
    ) -> int:
        """
        Record multiple exam answers at once.
        Each answer dict should have: subject, topic, question_content,
        student_answer, correct_answer, is_correct, question_type, score, max_score, etc.
        """
        recorded = 0
        for ans in answers:
            result = await self.record_answer(
                student_id=student_id,
                subject=ans.get("subject", ""),
                topic=ans.get("topic", ""),
                question_content=ans.get("question_content", ""),
                student_answer=ans.get("student_answer", ""),
                correct_answer=ans.get("correct_answer", ""),
                is_correct=ans.get("is_correct", False),
                question_type=ans.get("question_type", "open"),
                score=ans.get("score", 0),
                max_score=ans.get("max_score", 1),
                source=ans.get("source", "exam"),
                exam_id=ans.get("exam_id", ""),
                exercise_name=ans.get("exercise_name", ""),
                part_name=ans.get("part_name", ""),
                year=ans.get("year", ""),
            )
            if result:
                recorded += 1
        return recorded

    # ──────────────────────────────────────────────
    #  2. COMPUTE PROFICIENCY
    # ──────────────────────────────────────────────

    async def get_proficiency_summary(self, student_id: str) -> dict:
        """
        Compute full proficiency summary from answer history.
        Returns:
        {
            "overall_level": "intermédiaire",
            "overall_score": 52.0,
            "total_answers": 25,
            "subjects": {
                "SVT": {
                    "score": 60.0,
                    "level": "intermédiaire",
                    "total": 15,
                    "correct": 9,
                    "topics": {
                        "Géologie": {"score": 40.0, "total": 5, "correct": 2, "level": "intermédiaire"},
                        ...
                    }
                },
                ...
            },
            "lacunes": [...],       # Weak topics
            "strengths": [...],     # Strong topics
            "recent_trend": "improving" | "declining" | "stable",
            "last_activity": "2026-04-07T15:30:00Z",
        }
        """
        try:
            result = self.supabase.table("student_answer_history").select(
                "subject, topic, is_correct, score, max_score, question_type, source, part_name, student_answer, created_at"
            ).eq("student_id", student_id).order(
                "created_at", desc=True
            ).limit(500).execute()

            answers = result.data if result.data else []
            if not answers:
                return self._empty_summary()

            return self._compute_summary(answers)
        except Exception as e:
            _log.error(f"[Proficiency] Error fetching summary: {e}")
            return self._empty_summary()

    def _compute_summary(self, answers: list[dict]) -> dict:
        """
        Compute proficiency using:
        - Bloom's taxonomy weights (analyzing > applying > understanding > remembering)
        - Ebbinghaus decay (recent answers weighted more, half-life 14 days)
        - BAC coefficient weighting for overall score
        """
        # Group by subject and topic with weighted scoring
        by_subject = defaultdict(lambda: {
            "correct": 0, "total": 0,
            "weighted_score": 0.0, "weighted_max": 0.0,
            "bloom_profile": defaultdict(lambda: {"correct": 0, "total": 0}),
            "topics": defaultdict(lambda: {
                "correct": 0, "total": 0,
                "weighted_score": 0.0, "weighted_max": 0.0,
                "bloom_profile": defaultdict(lambda: {"correct": 0, "total": 0}),
            }),
        })

        total_weighted_score = 0.0
        total_weighted_max = 0.0
        total_answers = len(answers)

        for ans in answers:
            # Normalize subject name to canonical form
            subj = _normalize_subject(ans["subject"])
            topic = ans.get("topic", "Général") or "Général"
            is_correct = ans["is_correct"]
            score = float(ans.get("score", 0))
            max_score = float(ans.get("max_score", 1)) or 1
            q_type = ans.get("question_type", "open")
            part_name = ans.get("part_name", "") if "part_name" in ans else ""
            created_at = ans.get("created_at", "")

            # Compute composite weight: Bloom × Time decay
            bloom = _bloom_level(q_type, part_name)
            bloom_w = BLOOM_WEIGHTS.get(bloom, 1.0)
            time_w = _time_weight(created_at)
            w = bloom_w * time_w  # Combined weight

            weighted_score = (score / max_score) * w * max_score
            weighted_max = w * max_score

            # Subject level
            by_subject[subj]["total"] += 1
            by_subject[subj]["weighted_score"] += weighted_score
            by_subject[subj]["weighted_max"] += weighted_max
            by_subject[subj]["bloom_profile"][bloom]["total"] += 1
            if is_correct:
                by_subject[subj]["correct"] += 1
                by_subject[subj]["bloom_profile"][bloom]["correct"] += 1

            # Topic level
            by_subject[subj]["topics"][topic]["total"] += 1
            by_subject[subj]["topics"][topic]["weighted_score"] += weighted_score
            by_subject[subj]["topics"][topic]["weighted_max"] += weighted_max
            by_subject[subj]["topics"][topic]["bloom_profile"][bloom]["total"] += 1
            if is_correct:
                by_subject[subj]["topics"][topic]["correct"] += 1
                by_subject[subj]["topics"][topic]["bloom_profile"][bloom]["correct"] += 1

            total_weighted_score += weighted_score
            total_weighted_max += weighted_max

        # Build subject summaries
        subjects = {}
        all_topic_scores = []

        for subj, data in by_subject.items():
            subj_score = (data["weighted_score"] / data["weighted_max"] * 100) if data["weighted_max"] > 0 else 0

            # Bloom profile summary for subject
            bloom_summary = {}
            for bl, bd in data["bloom_profile"].items():
                bl_rate = (bd["correct"] / bd["total"] * 100) if bd["total"] > 0 else 0
                bloom_summary[bl] = {"correct": bd["correct"], "total": bd["total"], "rate": round(bl_rate, 1)}

            topics = {}
            for topic, tdata in data["topics"].items():
                t_score = (tdata["weighted_score"] / tdata["weighted_max"] * 100) if tdata["weighted_max"] > 0 else 0
                t_level = self._score_to_level(t_score)
                topics[topic] = {
                    "score": round(t_score, 1),
                    "total": tdata["total"],
                    "correct": tdata["correct"],
                    "level": t_level,
                }
                all_topic_scores.append((subj, topic, t_score, tdata["total"]))

            # Calculate coverage based on unique topics covered vs total chapters
            total_chapters = SUBJECT_TOTAL_CHAPTERS.get(subj, 10)
            topics_covered = len(topics)  # Number of unique topics with answers
            coverage_ratio = min(1.0, topics_covered / total_chapters)
            
            subjects[subj] = {
                "score": round(subj_score, 1),           # Performance score (% correct)
                "level": self._score_to_level(subj_score),  # Level based on performance
                "total": data["total"],
                "correct": data["correct"],
                "coverage_percent": round(coverage_ratio * 100, 0),  # % of chapters covered
                "chapters_covered": topics_covered,
                "chapters_total": total_chapters,
                "bloom_profile": bloom_summary,
                "topics": dict(topics),
            }

        # ══════════════════════════════════════════════════════════════
        # ENSURE ALL SUBJECTS FROM CADRE DE RÉFÉRENCE ARE INCLUDED
        # Even subjects with no answers should appear with 0% score/coverage
        # ══════════════════════════════════════════════════════════════
        for canonical_subj in ALL_SUBJECTS:
            if canonical_subj not in subjects:
                total_chapters = SUBJECT_TOTAL_CHAPTERS.get(canonical_subj, 10)
                subjects[canonical_subj] = {
                    "score": 0,
                    "level": "non acquis",
                    "total": 0,
                    "correct": 0,
                    "coverage_percent": 0,
                    "chapters_covered": 0,
                    "chapters_total": total_chapters,
                    "bloom_profile": {},
                    "topics": {},
                }

        # ══════════════════════════════════════════════════════════════
        # OVERALL SCORE CALCULATION (CADRE DE RÉFÉRENCE)
        # Includes ALL subjects weighted by official BAC coefficients:
        # - Mathématiques: coeff 7
        # - Physique: coeff 7
        # - Chimie: coeff 7
        # - SVT: coeff 5
        # Total coefficients = 26
        # 
        # Two components:
        # 1. Performance score (70%): How well the student answers
        # 2. Coverage score (30%): How much of the program has been studied
        # ══════════════════════════════════════════════════════════════
        
        # Calculate weighted scores across ALL subjects
        perf_coeff_sum = 0.0
        cov_coeff_sum = 0.0
        total_coeff = 0.0
        
        for canonical_subj in ALL_SUBJECTS:
            coeff = BAC_COEFFICIENTS.get(canonical_subj, 5)
            total_coeff += coeff
            
            sdata = subjects.get(canonical_subj, {"score": 0, "coverage_percent": 0})
            perf_coeff_sum += sdata["score"] * coeff
            cov_coeff_sum += sdata["coverage_percent"] * coeff
        
        # Performance component (70% weight) - how well you answer
        # Normalized by total possible (100% × total_coeff)
        performance_score = (perf_coeff_sum / (100 * total_coeff) * 100) if total_coeff > 0 else 0
        # Coverage component (30% weight) - how much you've studied
        coverage_score = (cov_coeff_sum / (100 * total_coeff) * 100) if total_coeff > 0 else 0
        
        # Combined overall score
        overall_score = (performance_score * 0.7) + (coverage_score * 0.3)

        # ── Identify LACUNES using ZPD logic ──
        # ZPD: topics where score is 15-55% are in the "zone" — student CAN learn with help
        # Below 15% = too hard (needs prerequisites first)
        # Above 55% = already acquired
        # MINIMUM 2 answers required for statistical reliability
        lacunes = []
        for subj, topic, score, total in all_topic_scores:
            if total < 2:
                continue  # Not enough data — avoid false lacunes from 1 answer
            coeff = BAC_COEFFICIENTS.get(subj, 5)
            if score < 55:
                # Priority based on ZPD + BAC coefficient
                if score < 15:
                    priority = "critique"    # Below ZPD — needs prerequisite review
                    zpd_action = "Reprendre les bases avant d'avancer"
                elif score < 30:
                    priority = "haute"       # Lower ZPD — needs guided instruction
                    zpd_action = "Explication guidée avec exemples simples"
                else:
                    priority = "moyenne"     # In ZPD — can learn with scaffolding
                    zpd_action = "Exercices progressifs avec étayage"
                lacunes.append({
                    "subject": subj,
                    "topic": topic,
                    "score": round(score, 1),
                    "total_answers": total,
                    "priority": priority,
                    "zpd_action": zpd_action,
                    "bac_coefficient": coeff,
                    "urgency": round((100 - score) * coeff / 9, 1),  # Normalized urgency
                })
        # Sort by urgency (high BAC coeff + low score = most urgent)
        lacunes.sort(key=lambda x: -x["urgency"])

        # Identify strengths (score >= 75% = maîtrisé)
        strengths = []
        for subj, topic, score, total in all_topic_scores:
            if score >= 75 and total >= 2:
                strengths.append({
                    "subject": subj,
                    "topic": topic,
                    "score": round(score, 1),
                    "total_answers": total,
                })
        strengths.sort(key=lambda x: -x["score"])

        # Recent trend with weighted comparison
        recent_trend = self._compute_trend(answers)

        last_activity = answers[0].get("created_at", "") if answers else ""

        # ── EXAM READINESS SCORE ──
        # How ready is the student for the BAC? Per-subject + overall
        # Factors: score × coverage × trend bonus × coefficient weight
        days_left = _days_to_exam()
        exam_readiness = self._compute_exam_readiness(subjects, lacunes, strengths, days_left)

        # ── Detect recurring errors (topics where the student keeps failing) ──
        recurring_errors = self._detect_recurring_errors(answers)

        return {
            "overall_level": self._score_to_level(overall_score),
            "overall_score": round(overall_score, 1),
            "performance_score": round(performance_score, 1),  # % correct on answered questions
            "coverage_score": round(coverage_score, 1),        # % of program covered
            "total_answers": total_answers,
            "subjects": subjects,
            "lacunes": lacunes[:10],
            "strengths": strengths[:10],
            "recurring_errors": recurring_errors[:10],
            "recent_trend": recent_trend,
            "last_activity": last_activity,
            "exam_readiness": exam_readiness,
            "days_to_exam": days_left,
        }

    def _detect_recurring_errors(self, answers: list[dict]) -> list[dict]:
        """Detect (subject, topic) pairs where the student makes repeated errors.

        A topic is flagged as 'recurring error' when EITHER:
          - 3+ consecutive wrong answers on the most recent attempts (streak), OR
          - ≥4 total attempts AND error rate on the last 5 ≥ 60%.

        Each flagged topic is classified:
          - total_block        : 100% wrong (streak == total) → prerequisites missing
          - conceptual         : same wrong answer chosen ≥2 times → misconception
          - regressing         : was correct before, now failing → needs refresh
          - struggling         : persistent difficulty without clear pattern

        Returns list sorted by urgency = streak × BAC_coefficient × (1 + recency).
        `answers` is expected to be the raw list from student_answer_history
        (any order — we re-sort chronologically per topic).
        """
        if not answers:
            return []

        by_topic: dict[tuple, list[dict]] = defaultdict(list)
        for ans in answers:
            subj = _normalize_subject(ans.get("subject", ""))
            topic = (ans.get("topic") or "Général") or "Général"
            by_topic[(subj, topic)].append(ans)

        recurring: list[dict] = []
        for (subj, topic), topic_answers in by_topic.items():
            # Sort chronologically (oldest → newest) for streak logic
            sorted_ans = sorted(topic_answers, key=lambda a: a.get("created_at", ""))
            total = len(sorted_ans)
            if total < 3:
                continue

            # Streak of CONSECUTIVE errors from the most recent attempt backwards
            streak = 0
            for a in reversed(sorted_ans):
                if not a.get("is_correct"):
                    streak += 1
                else:
                    break

            # Error rate on last 5 attempts
            last5 = sorted_ans[-5:]
            last5_errors = sum(1 for a in last5 if not a.get("is_correct"))
            err_rate_recent = last5_errors / len(last5) if last5 else 0

            is_recurring = streak >= 3 or (total >= 4 and err_rate_recent >= 0.6)
            if not is_recurring:
                continue

            # Classify the error pattern
            wrong_answers = [
                (a.get("student_answer") or "").strip().lower()
                for a in sorted_ans if not a.get("is_correct")
            ]
            wrong_answers = [w for w in wrong_answers if w]
            same_wrong_max = max(
                (wrong_answers.count(w) for w in set(wrong_answers)),
                default=0,
            )

            if streak == total and total >= 3:
                pattern = "total_block"
                action = "Reprendre les prérequis — les bases ne passent pas"
            elif same_wrong_max >= 2:
                pattern = "conceptual"
                action = "Erreur conceptuelle (même mauvaise réponse répétée) — clarifier le concept"
            else:
                # Detect regression: early correct, late wrong
                if total >= 5:
                    mid = total // 2
                    first_half = sorted_ans[:mid]
                    second_half = sorted_ans[mid:]
                    first_rate = sum(1 for a in first_half if a.get("is_correct")) / len(first_half)
                    second_rate = sum(1 for a in second_half if a.get("is_correct")) / len(second_half)
                    if first_rate >= second_rate + 0.25 and first_rate >= 0.5:
                        pattern = "regressing"
                        action = "Régression détectée — rafraîchir les connaissances"
                    else:
                        pattern = "struggling"
                        action = "Difficulté persistante — exercices progressifs avec étayage"
                else:
                    pattern = "struggling"
                    action = "Difficulté persistante — exercices progressifs avec étayage"

            coeff = BAC_COEFFICIENTS.get(subj, 5)
            last_created = sorted_ans[-1].get("created_at", "")
            recency = _time_weight(last_created)  # 1.0 = just now, ~0 = very old
            urgency = streak * coeff * (1 + recency)

            recurring.append({
                "subject": subj,
                "topic": topic,
                "total_attempts": total,
                "streak_errors": streak,
                "error_rate_recent": round(err_rate_recent * 100, 0),
                "pattern": pattern,
                "action": action,
                "bac_coefficient": coeff,
                "urgency": round(urgency, 1),
                "last_error_at": last_created,
            })

        recurring.sort(key=lambda x: -x["urgency"])
        return recurring

    def _compute_trend(self, answers: list[dict]) -> str:
        """Compute weighted trend: compare last 7 days vs previous 7 days."""
        if len(answers) < 4:
            return "stable"
        now = datetime.now(timezone.utc)
        recent_cutoff = now - timedelta(days=7)
        older_cutoff = now - timedelta(days=14)

        recent_correct, recent_total = 0, 0
        older_correct, older_total = 0, 0

        for ans in answers:
            try:
                ts = datetime.fromisoformat(ans.get("created_at", "").replace("Z", "+00:00"))
            except Exception:
                continue
            if ts >= recent_cutoff:
                recent_total += 1
                if ans["is_correct"]:
                    recent_correct += 1
            elif ts >= older_cutoff:
                older_total += 1
                if ans["is_correct"]:
                    older_correct += 1

        if recent_total < 2 or older_total < 2:
            return "stable"

        recent_rate = recent_correct / recent_total
        older_rate = older_correct / older_total
        diff = recent_rate - older_rate

        if diff > 0.1:
            return "improving"
        elif diff < -0.1:
            return "declining"
        return "stable"

    def _compute_exam_readiness(self, subjects: dict, lacunes: list, strengths: list, days_left: int) -> dict:
        """
        Compute exam readiness score (0-100) per subject and overall.
        Factors:
        - Base score (proficiency percentage)
        - Coverage penalty (not enough answers = less confident)
        - Critical lacune penalty (any critique lacune = big drop)
        - Trend bonus (improving = slight boost)
        """
        MIN_ANSWERS_FOR_READY = 10  # Need at least 10 answers per subject to be "ready"
        readiness_by_subject = {}
        total_coeff_readiness = 0
        total_coeff = 0

        for subj, sdata in subjects.items():
            base = sdata["score"]
            total = sdata["total"]
            coeff = BAC_COEFFICIENTS.get(subj, 5)

            # Coverage factor: 0-1 based on answer count
            coverage = min(1.0, total / MIN_ANSWERS_FOR_READY)

            # Critical lacune penalty for this subject
            subj_lacunes = [l for l in lacunes if l["subject"] == subj]
            has_critique = any(l["priority"] == "critique" for l in subj_lacunes)
            lacune_penalty = 0.7 if has_critique else (0.85 if subj_lacunes else 1.0)

            readiness = base * coverage * lacune_penalty
            readiness = max(0, min(100, readiness))

            label = "Prêt" if readiness >= 65 else ("En progrès" if readiness >= 40 else "À renforcer")

            readiness_by_subject[subj] = {
                "score": round(readiness, 1),
                "label": label,
                "base_proficiency": round(base, 1),
                "coverage": round(coverage * 100, 0),
                "answers_count": total,
                "bac_coefficient": coeff,
                "critical_lacunes": len([l for l in subj_lacunes if l["priority"] == "critique"]),
            }

            total_coeff_readiness += readiness * coeff
            total_coeff += coeff

        overall_readiness = (total_coeff_readiness / total_coeff) if total_coeff > 0 else 0

        # Global label
        if overall_readiness >= 65:
            overall_label = "Prêt pour le BAC"
        elif overall_readiness >= 45:
            overall_label = "En bonne voie — continue!"
        elif overall_readiness >= 25:
            overall_label = "Effort nécessaire — concentre-toi sur les lacunes"
        else:
            overall_label = "Travail intensif requis"

        return {
            "overall": round(overall_readiness, 1),
            "overall_label": overall_label,
            "days_left": days_left,
            "by_subject": readiness_by_subject,
        }

    def _score_to_level(self, score: float) -> str:
        for level, (lo, hi) in LEVEL_THRESHOLDS.items():
            if lo <= score < hi:
                return level
        return "maîtrisé" if score >= 75 else "non acquis"

    def _empty_summary(self) -> dict:
        return {
            "overall_level": "inconnu",
            "overall_score": 0,
            "performance_score": 0,
            "coverage_score": 0,
            "total_answers": 0,
            "subjects": {},
            "lacunes": [],
            "strengths": [],
            "recurring_errors": [],
            "recent_trend": "stable",
            "last_activity": "",
            "exam_readiness": {
                "overall": 0,
                "overall_label": "Pas encore de données",
                "days_left": _days_to_exam(),
                "by_subject": {},
            },
            "days_to_exam": _days_to_exam(),
        }

    # ──────────────────────────────────────────────
    #  3. GENERATE LLM CONTEXT
    # ──────────────────────────────────────────────

    async def get_llm_context(self, student_id: str) -> dict:
        """
        Generate rich pedagogical context for LLM personalization.
        Uses Zone Proximale de Développement (Vygotsky) to guide teaching strategy.

        ZPD Principle:
        - Score < 15%: BELOW ZPD → needs prerequisite remediation first
        - Score 15-55%: IN ZPD → optimal learning zone, needs scaffolding
        - Score 55-75%: ABOVE ZPD → consolidation, can work more independently
        - Score > 75%: MASTERED → ready for enrichment and deeper challenges
        """
        summary = await self.get_proficiency_summary(student_id)

        if summary["total_answers"] == 0:
            return {
                "proficiency": "inconnu (pas encore de données)",
                "struggles": "aucune identifiée",
                "mastered": "aucun",
                "adaptation_hints": "",
            }

        # Proficiency string
        proficiency = f"{summary['overall_level']} ({summary['overall_score']}% sur {summary['total_answers']} réponses)"

        # Struggles string with ZPD actions
        if summary["lacunes"]:
            struggles_parts = []
            for lac in summary["lacunes"][:5]:
                struggles_parts.append(
                    f"{lac['topic']} en {lac['subject']} ({lac['score']}%, "
                    f"priorité {lac['priority']}: {lac.get('zpd_action', '')})"
                )
            struggles = "; ".join(struggles_parts)
        else:
            struggles = "aucune lacune détectée"

        # Mastered string
        if summary["strengths"]:
            mastered_parts = []
            for st in summary["strengths"][:5]:
                mastered_parts.append(f"{st['topic']} en {st['subject']} ({st['score']}%)")
            mastered = ", ".join(mastered_parts)
        else:
            mastered = "aucun sujet maîtrisé confirmé"

        # ── Build rich adaptation hints using ZPD + Bloom + URGENCY ──
        hints = []
        days_left = _days_to_exam()

        # 0-bis. RECURRING ERRORS — top priority: these are patterns, not random failures
        recurring_errors = summary.get("recurring_errors", []) or []
        if recurring_errors:
            top_errors = recurring_errors[:3]
            parts = []
            for err in top_errors:
                pattern_emoji = {
                    "total_block": "🚫",
                    "conceptual": "🧠",
                    "regressing": "📉",
                    "struggling": "⚠️",
                }.get(err["pattern"], "⚠️")
                parts.append(
                    f"{pattern_emoji} {err['topic']} ({err['subject']}, "
                    f"coeff {err['bac_coefficient']}): {err['streak_errors']} erreurs consécutives "
                    f"sur {err['total_attempts']} tentatives — type: {err['pattern']}. "
                    f"→ {err['action']}"
                )
            hints.append(
                "🔁 ERREURS RÉCURRENTES À CORRIGER EN PRIORITÉ (avant toute autre activité): "
                + " | ".join(parts)
                + " | Stratégie: aborde EXPLICITEMENT ces topics dès le début de la session, "
                "diagnostique la source de l'erreur (prérequis manquant? confusion conceptuelle? "
                "lecture trop rapide?), puis propose un exercice de remédiation ciblé."
            )

        # 0. TIME URGENCY — Critical context for the LLM
        if days_left <= 14:
            hints.append(
                f"🚨 URGENCE MAXIMALE: {days_left} JOURS avant le BAC! "
                f"Concentre-toi UNIQUEMENT sur les exercices type BAC et les lacunes critiques. "
                f"Pas de nouvelles leçons — révision intensive et entraînement. "
                f"Chaque minute compte."
            )
        elif days_left <= 30:
            hints.append(
                f"⏰ URGENCE: {days_left} jours avant le BAC. "
                f"Priorise les matières à fort coefficient (Math coeff 7, Physique-Chimie coeff 7, SVT coeff 5). "
                f"Alterne révision ciblée et exercices de type BAC. "
                f"Ne perds pas de temps sur les sujets déjà maîtrisés."
            )
        elif days_left <= 60:
            hints.append(
                f"📅 {days_left} jours avant le BAC. "
                f"Phase de consolidation: renforce les lacunes et pratique avec des sujets d'examen."
            )

        # 1. Trend-based emotional regulation
        if summary["recent_trend"] == "declining":
            hints.append(
                "⚠️ PERFORMANCE EN BAISSE RÉCENTE. Stratégie: "
                "Encourage l'étudiant, valorise ses progrès passés. "
                "Propose des exercices plus faciles pour restaurer la confiance. "
                "Utilise le renforcement positif systématiquement."
            )
        elif summary["recent_trend"] == "improving":
            hints.append(
                "📈 EN PROGRESSION. L'étudiant s'améliore! "
                "Augmente progressivement la difficulté (principe de progression spiralaire). "
                "Propose des exercices de type BAC pour consolider."
            )

        # 2. ZPD-based differentiation per lacune
        for lac in summary["lacunes"][:3]:
            if lac["priority"] == "critique":
                hints.append(
                    f"🔴 {lac['topic']} ({lac['subject']}): SOUS la ZPD ({lac['score']}%). "
                    f"→ Reviens aux PRÉREQUIS. Explique le vocabulaire de base. "
                    f"Utilise des analogies simples du quotidien. "
                    f"PAS d'exercices complexes tant que les bases ne sont pas acquises."
                )
            elif lac["priority"] == "haute":
                hints.append(
                    f"🟠 {lac['topic']} ({lac['subject']}): ZPD basse ({lac['score']}%). "
                    f"→ Instruction guidée: explique pas-à-pas avec des schémas au tableau. "
                    f"Pose des questions fermées d'abord, puis ouvertes. "
                    f"Donne des indices (étayage) avant la réponse."
                )
            else:
                hints.append(
                    f"🟡 {lac['topic']} ({lac['subject']}): DANS la ZPD ({lac['score']}%). "
                    f"→ Zone optimale d'apprentissage! Propose des exercices progressifs. "
                    f"Laisse l'étudiant essayer seul, puis corrige. "
                    f"Utilise la méthode socratique (questions guidées)."
                )

        # 3. Bloom taxonomy-based cognitive scaffolding
        for subj, sdata in summary["subjects"].items():
            bloom = sdata.get("bloom_profile", {})
            remembering = bloom.get("remembering", {})
            analyzing = bloom.get("analyzing", {})

            # Can memorize but can't analyze → needs transfer exercises
            if (remembering.get("rate", 0) > 60 and
                    analyzing.get("total", 0) >= 2 and
                    analyzing.get("rate", 0) < 40):
                hints.append(
                    f"📊 {subj}: Bonne mémorisation ({remembering.get('rate', 0)}%) "
                    f"mais faible en raisonnement ({analyzing.get('rate', 0)}%). "
                    f"→ Propose des exercices de TRANSFERT: application à des situations nouvelles, "
                    f"analyse de documents, comparaison de phénomènes."
                )

            # Good at analysis but weak in basics → gaps in fundamentals
            if (analyzing.get("rate", 0) > 60 and
                    remembering.get("total", 0) >= 2 and
                    remembering.get("rate", 0) < 50):
                hints.append(
                    f"📊 {subj}: Bon raisonnement mais lacunes en connaissances de base. "
                    f"→ Renforce le vocabulaire et les définitions fondamentales avec des fiches."
                )

        # 4. Subject-level teaching strategy
        for subj, sdata in summary["subjects"].items():
            if sdata["level"] == "non acquis" and sdata["total"] >= 3:
                coeff = BAC_COEFFICIENTS.get(subj, 5)
                hints.append(
                    f"🎯 {subj} (coeff {coeff}): Niveau non acquis ({sdata['score']}%). "
                    f"Priorité {'MAXIMALE' if coeff >= 7 else 'haute'}. "
                    f"Simplifie les explications au maximum. Utilise des exemples concrets du quotidien."
                )
            elif sdata["level"] == "maîtrisé":
                hints.append(
                    f"✅ {subj}: Maîtrisé ({sdata['score']}%). "
                    f"Propose des sujets BAC complets et des exercices d'approfondissement."
                )

        adaptation_hints = " ".join(hints) if hints else ""

        return {
            "proficiency": proficiency,
            "struggles": struggles,
            "mastered": mastered,
            "adaptation_hints": adaptation_hints,
        }

    # ──────────────────────────────────────────────
    #  4. UPDATE STUDENT PROFILE
    # ──────────────────────────────────────────────

    async def _update_proficiency_summary(self, student_id: str):
        """Update student_profiles table with latest proficiency data.
        Gracefully handles missing columns in the database."""
        try:
            summary = await self.get_proficiency_summary(student_id)

            # Build subject_proficiencies dict for profile
            subject_profs = {}
            for subj, sdata in summary["subjects"].items():
                subject_profs[subj] = {
                    "score": sdata["score"],
                    "level": sdata["level"],
                    "total_answers": sdata["total"],
                }

            # Build weaknesses and strengths lists
            weaknesses = [
                f"{lac['topic']} ({lac['subject']}): {lac['score']}%"
                for lac in summary["lacunes"][:5]
            ]
            strengths_list = [
                f"{st['topic']} ({st['subject']}): {st['score']}%"
                for st in summary["strengths"][:5]
            ]

            # Try updating with all fields first, fall back to minimal update
            update_data = {
                "overall_proficiency": summary["overall_level"],
                "subject_proficiencies": subject_profs,
                "weaknesses": weaknesses,
                "strengths": strengths_list,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }

            try:
                self.supabase.table("student_profiles").update(update_data).eq(
                    "student_id", student_id
                ).execute()
            except Exception as col_err:
                # If columns don't exist, just log and skip — proficiency still works via answer_history
                if "column" in str(col_err).lower() or "PGRST204" in str(col_err):
                    _log.debug(f"[Proficiency] student_profiles missing columns, skipping profile update")
                    return
                raise

            _log.info(f"[Proficiency] Updated profile: student={student_id[:8]}.. "
                      f"level={summary['overall_level']} score={summary['overall_score']}%")

            # Auto-adapt coaching plan every 10 answers
            if summary["total_answers"] % 10 == 0 and summary["total_answers"] >= 10:
                try:
                    from app.services.study_plan_service import study_plan_service
                    result = await study_plan_service.adapt_plan_from_proficiency(student_id)
                    if result.get("adapted"):
                        _log.info(f"[Proficiency] Auto-adapted plan: {result['sessions_reordered']} sessions reordered")
                except Exception as adapt_err:
                    _log.error(f"[Proficiency] Auto-adapt plan failed: {adapt_err}")
        except Exception as e:
            _log.error(f"[Proficiency] Error updating profile: {e}")

    # ──────────────────────────────────────────────
    #  5. DASHBOARD DATA
    # ──────────────────────────────────────────────

    async def get_dashboard_data(self, student_id: str) -> dict:
        """
        Get complete dashboard data for the frontend.
        Returns proficiency, lacunes, progression timeline, subject breakdown.
        """
        summary = await self.get_proficiency_summary(student_id)

        # Get progression timeline (answers per day, last 30 days)
        try:
            thirty_days_ago = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
            result = self.supabase.table("student_answer_history").select(
                "created_at, is_correct, subject, score, max_score"
            ).eq("student_id", student_id).gte(
                "created_at", thirty_days_ago
            ).order("created_at").execute()

            daily_data = defaultdict(lambda: {"total": 0, "correct": 0, "score_sum": 0, "max_sum": 0})
            for ans in (result.data or []):
                day = ans["created_at"][:10]
                daily_data[day]["total"] += 1
                daily_data[day]["score_sum"] += float(ans.get("score", 0))
                daily_data[day]["max_sum"] += float(ans.get("max_score", 1))
                if ans["is_correct"]:
                    daily_data[day]["correct"] += 1

            progression = []
            for day, data in sorted(daily_data.items()):
                rate = (data["score_sum"] / data["max_sum"] * 100) if data["max_sum"] > 0 else 0
                progression.append({
                    "date": day,
                    "total_answers": data["total"],
                    "correct_answers": data["correct"],
                    "success_rate": round(rate, 1),
                })
        except Exception as e:
            _log.error(f"[Proficiency] Error fetching progression: {e}")
            progression = []

        return {
            **summary,
            "progression": progression,
        }

    # ──────────────────────────────────────────────
    #  6. AUTO-EVALUATE ANSWER (for QCM, vrai/faux)
    # ──────────────────────────────────────────────

    def evaluate_answer(
        self,
        question_type: str,
        student_answer: str,
        correct_answer: str,
        max_points: float = 1.0,
    ) -> tuple[bool, float]:
        """
        Auto-evaluate an answer for deterministic question types.
        Returns (is_correct, score).
        """
        if not student_answer or not correct_answer:
            return False, 0

        student_clean = student_answer.strip().lower()
        correct_clean = str(correct_answer).strip().lower()

        if question_type in ("qcm", "vrai_faux"):
            is_correct = student_clean == correct_clean
            return is_correct, max_points if is_correct else 0

        # For open/schema questions, partial credit via simple heuristics
        if question_type == "open":
            # Can't auto-grade open questions reliably, return partial
            return False, 0

        return student_clean == correct_clean, max_points if student_clean == correct_clean else 0


# Singleton
proficiency_service = StudentProficiencyService()
