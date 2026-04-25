"""
Study Plan Service — Proficiency-Driven Adaptive Coaching
==========================================================
Generates and adapts study plans using LIVE proficiency data from the
student proficiency agent. Combines diagnostic scores with ongoing
answer history for truly adaptive coaching.

PEDAGOGICAL PRINCIPLES:
- Zone Proximale de Développement (Vygotsky): Focus on topics within ZPD
- Spiraling curriculum (Bruner): Revisit topics at increasing difficulty
- Spaced repetition (Ebbinghaus): Schedule reviews at optimal intervals
- Mastery-based progression: Don't advance until current topic is "acquis"
- Interleaving (Rohrer): Mix subjects for better transfer
- Testing effect (Roediger): Low-stakes testing > re-reading

TIME ALLOCATION STRATEGY:
- Phase 1 (APPRENTISSAGE): ~55% du temps — Cours structurés par chapitre
- Phase 2 (RÉVISION):      ~25% du temps — Révision ciblée + examens blancs
- Phase 3 (LACUNES):       ~20% du temps — Comblement des lacunes identifiées par l'agent
- Total planifié: ~85% du temps disponible (15% de marge pour repos/imprévus)
"""
from datetime import date, datetime, timedelta
from typing import Optional
from app.supabase_client import get_supabase_admin
from app.services.rag_service import get_rag_service
import uuid
import logging

_log = logging.getLogger(__name__)

# BAC exam coefficients by subject (Sciences Physiques branch)
# Source: Ministère de l'Éducation Nationale Marocain — 2BAC Sciences Physiques BIOF
BAC_COEFFICIENTS = {
    "Physique": 7,       # Part of Physique-Chimie coeff 7
    "Chimie": 7,         # Part of Physique-Chimie coeff 7
    "Mathématiques": 7,  # Same as Physique-Chimie
    "SVT": 5,            # Sciences de la Vie et de la Terre
    "Mathematiques": 7,  # Alias without accent
}

# Effective weight considering coefficient * exam weight
def _parse_pct(s: str) -> float:
    """Parse '67%' or '67% de l\\'examen' to 67.0"""
    try:
        return float(s.replace('%', '').split()[0].strip())
    except (ValueError, IndexError):
        return 0.0


class StudyPlanService:
    def __init__(self):
        self.supabase = get_supabase_admin()
        self.exam_date = date(2026, 6, 4)  # BAC exam date
        
    def calculate_days_until_exam(self) -> int:
        """Calculate days remaining until exam"""
        today = date.today()
        delta = self.exam_date - today
        return max(0, delta.days)
    
    def calculate_study_hours_available(self, days_remaining: int) -> int:
        """
        Calculate total study hours available with progressive intensity.
        As the exam approaches, daily study hours increase:
        - >60 days: 2.5h weekday / 3h weekend
        - 30-60 days: 3h weekday / 4h weekend
        - 14-30 days: 3.5h weekday / 4.5h weekend
        - <14 days: 4h weekday / 5h weekend (crunch mode)
        """
        total = 0.0
        today = date.today()
        for d in range(days_remaining):
            day = today + timedelta(days=d)
            days_left = days_remaining - d
            is_weekend = day.weekday() >= 5
            is_sunday = day.weekday() == 6
            if is_sunday:
                # Rest day — light session only
                total += 1.0
                continue
            if days_left <= 14:
                total += 5.0 if is_weekend else 4.0
            elif days_left <= 30:
                total += 4.5 if is_weekend else 3.5
            elif days_left <= 60:
                total += 4.0 if is_weekend else 3.0
            else:
                total += 3.0 if is_weekend else 2.5
        return int(total)

    def _get_exam_weights(self) -> dict:
        """Get official exam weights from cadres de référence via RAG."""
        try:
            rag = get_rag_service()
            return rag.get_exam_weights_data()
        except Exception as e:
            print(f"[StudyPlan] Failed to get exam weights from RAG: {e}")
            return {}

    def _compute_phase_split(self, days_remaining: int) -> dict:
        """
        Compute intelligent phase split based on time remaining.
        Returns dict with percentage for each phase.
        """
        if days_remaining <= 14:
            # < 2 weeks: full revision + exam practice mode
            return {"apprentissage": 0.10, "revision": 0.45, "lacunes": 0.45}
        elif days_remaining <= 30:
            # 2-4 weeks: mostly revision
            return {"apprentissage": 0.25, "revision": 0.40, "lacunes": 0.35}
        elif days_remaining <= 60:
            # 1-2 months: balanced
            return {"apprentissage": 0.45, "revision": 0.30, "lacunes": 0.25}
        else:
            # > 2 months: focus on learning
            return {"apprentissage": 0.55, "revision": 0.25, "lacunes": 0.20}
    
    def prioritize_subjects(self, diagnostic_scores: dict) -> list:
        """
        Prioritize subjects based on diagnostic scores AND official exam weights.
        Subjects with low scores AND high exam coefficient get top priority.
        Returns list of (subject_name, score, priority, effective_weight) tuples.
        """
        if not diagnostic_scores:
            return []
        
        exam_weights = self._get_exam_weights()
        
        result = []
        for name, score in diagnostic_scores.items():
            # Get BAC coefficient
            coeff = BAC_COEFFICIENTS.get(name, 5)
            
            # Compute effective urgency: low score + high coeff = most urgent
            # urgency = (100 - score) * coefficient_normalized
            urgency = (100 - score) * (coeff / 9.0)  # Normalize by max coeff (9 for Maths)
            
            if score < 40:
                priority = 'high'
            elif score < 60:
                priority = 'medium'
            else:
                priority = 'low'
            
            result.append((name, score, priority, urgency))
        
        # Sort by urgency descending (most urgent first)
        result.sort(key=lambda x: x[3], reverse=True)
        return result
    
    def allocate_hours_per_subject(
        self, 
        total_hours: int, 
        prioritized_subjects: list
    ) -> dict:
        """
        Allocate study hours using BOTH diagnostic weakness AND exam coefficients.
        A subject with coeff 7 and score 30% gets much more time than coeff 3 and score 70%.
        """
        if not prioritized_subjects:
            return {}
        
        exam_weights = self._get_exam_weights()
        
        weights = {}
        for item in prioritized_subjects:
            subject_name = item[0]
            score = item[1]
            
            # BAC coefficient importance
            coeff = BAC_COEFFICIENTS.get(subject_name, 5)
            
            # Combined weight: inverse score * coefficient
            # score 20 with coeff 7 → (80) * 7 = 560
            # score 80 with coeff 5 → (20) * 5 = 100
            weakness_factor = max(20, 100 - score)  # Minimum 20 even for strong subjects
            weights[subject_name] = weakness_factor * coeff
        
        total_weight = sum(weights.values())
        if total_weight == 0:
            return {}
        
        # Allocate hours proportionally, with minimum per subject
        allocation = {}
        min_hours = max(8, total_hours // (len(prioritized_subjects) * 3))
        
        for subject_name, weight in weights.items():
            hours = int((weight / total_weight) * total_hours)
            allocation[subject_name] = max(min_hours, hours)
        
        return allocation
    
    async def get_chapters_for_subject(self, subject_id: str) -> list:
        """Get all chapters for a subject, ordered by priority"""
        result = self.supabase.table('chapters').select(
            'id, chapter_number, title_fr, difficulty_level, estimated_hours'
        ).eq('subject_id', subject_id).order('order_index').execute()
        
        return result.data if result.data else []

    def _fetch_student_weak_topics(
        self, student_id: str, last_n: int = 5
    ) -> dict[str, set[str]]:
        """Return {subject_name_lower: {weak_topic_lower, ...}} from the N last diagnostics.

        Used to order chapters so that weak areas are prioritised in each phase of
        the study plan.
        """
        try:
            res = self.supabase.table('diagnostic_results').select(
                'weak_topics, subjects(name_fr)'
            ).eq('student_id', student_id).eq(
                'evaluation_type', 'diagnostic'
            ).order('created_at', desc=True).limit(last_n).execute()
        except Exception as e:
            _log.warning(f"[PLAN] weak_topics fetch failed: {e}")
            return {}

        weak: dict[str, set[str]] = {}
        for row in res.data or []:
            subj = (row.get('subjects') or {}).get('name_fr') or ''
            subj_key = subj.strip().lower()
            if not subj_key:
                continue
            topics = row.get('weak_topics') or []
            if not isinstance(topics, list):
                continue
            weak.setdefault(subj_key, set()).update(
                str(t).strip().lower() for t in topics if t
            )
        return weak

    @staticmethod
    def _chapter_matches_weak(chapter: dict, weak_topics: set[str]) -> bool:
        """Return True if the chapter's title contains any of the weak topic keywords."""
        if not weak_topics:
            return False
        title = (chapter.get('title_fr') or '').lower()
        if not title:
            return False
        for topic in weak_topics:
            if not topic:
                continue
            # Match if significant overlap: topic substring in title OR vice versa
            if topic in title:
                return True
            # Also match on individual keywords (≥ 4 chars to avoid noise)
            for word in topic.split():
                if len(word) >= 4 and word in title:
                    return True
        return False

    def _order_chapters_by_weakness(
        self, chapters: list, weak_topics: set[str]
    ) -> list:
        """Return chapters reordered so weak ones come first, preserving relative order.

        Weak chapters are identified by title ↔ weak_topics fuzzy match.
        """
        if not weak_topics:
            return list(chapters)
        weak: list = []
        others: list = []
        for ch in chapters:
            if self._chapter_matches_weak(ch, weak_topics):
                weak.append(ch)
            else:
                others.append(ch)
        return weak + others

    def _get_exam_id_allocator(self, subject_name: str) -> "callable":
        """Return a function that yields the next real BAC exam id for this subject.

        Used to attach a non-repeating real exam to each `examen_blanc` session.
        Cycles through the N most recent exams (2024-2025 normale/rattrapage…).
        """
        try:
            rag = get_rag_service()
            exams = rag.get_recent_exams_for_subject(subject_name, n=6)
        except Exception as e:
            _log.warning(f"[PLAN] recent_exams fetch failed for {subject_name}: {e}")
            exams = []

        idx = [0]
        def next_exam_id() -> Optional[str]:
            if not exams:
                return None
            exam = exams[idx[0] % len(exams)]
            idx[0] += 1
            return exam.get("id")
        return next_exam_id
    
    async def generate_plan(
        self, 
        student_id: str, 
        diagnostic_scores: dict
    ) -> dict:
        """
        Generate a complete study plan with 3 intelligent phases:
        - Phase 1 (APPRENTISSAGE): Cours structurés par chapitre
        - Phase 2 (RÉVISION): Révision ciblée + examens blancs
        - Phase 3 (LACUNES): Comblement des lacunes + dernières révisions
        
        Only plans ~85% of available time (15% margin for rest/unexpected).
        Uses official exam weights from cadres de référence for prioritization.
        """
        # STEP 1: Archive existing plans
        existing_plans = self.supabase.table('study_plans').select('id, status').eq(
            'student_id', student_id
        ).execute()
        
        if existing_plans.data:
            for old_plan in existing_plans.data:
                if old_plan['status'] in ['active', 'completed']:
                    self.supabase.table('study_plans').update({
                        'status': 'archived'
                    }).eq('id', old_plan['id']).execute()
                    self.supabase.table('study_plan_sessions').delete().eq(
                        'plan_id', old_plan['id']
                    ).execute()
        
        # STEP 2: Calculate time
        days_remaining = self.calculate_days_until_exam()
        total_hours_raw = self.calculate_study_hours_available(days_remaining)
        # Only plan 85% of time — leave 15% margin
        total_hours = int(total_hours_raw * 0.85)
        
        print(f"[PLAN] === Generating plan ===")
        print(f"[PLAN] Days: {days_remaining}, Raw hours: {total_hours_raw}, Planned: {total_hours} (85%)")
        
        # STEP 3: Get subjects and exam weights
        subjects_result = self.supabase.table('subjects').select('id, name_fr').execute()
        subject_map = {s['name_fr']: s['id'] for s in subjects_result.data}
        
        exam_weights = self._get_exam_weights()
        print(f"[PLAN] Exam weights from RAG: {list(exam_weights.keys())}")
        
        # Complete scores for all subjects
        complete_scores = {}
        for subject_name in subject_map.keys():
            complete_scores[subject_name] = diagnostic_scores.get(subject_name, 50.0)
        print(f"[PLAN] Scores: {complete_scores}")
        
        # STEP 4: Phase split
        phase_split = self._compute_phase_split(days_remaining)
        hours_apprentissage = int(total_hours * phase_split["apprentissage"])
        hours_revision = int(total_hours * phase_split["revision"])
        hours_lacunes = int(total_hours * phase_split["lacunes"])
        print(f"[PLAN] Phase split: apprentissage={hours_apprentissage}h, revision={hours_revision}h, lacunes={hours_lacunes}h")
        
        # Determine proficiency
        avg_score = sum(complete_scores.values()) / len(complete_scores) if complete_scores else 50
        proficiency = "débutant" if avg_score < 40 else ("intermédiaire" if avg_score < 65 else "avancé")
        
        # STEP 5: Create plan record
        plan_data = {
            "id": str(uuid.uuid4()),
            "student_id": student_id,
            "exam_date": self.exam_date.isoformat(),
            "diagnostic_scores": complete_scores,
            "total_hours_available": total_hours,
            "status": "active"
        }
        plan_result = self.supabase.table('study_plans').insert(plan_data).execute()
        if not plan_result.data:
            raise Exception("Failed to create study plan")
        plan_id = plan_result.data[0]['id']
        
        # STEP 6: Prioritize and allocate
        prioritized = self.prioritize_subjects(complete_scores)
        
        # Allocate APPRENTISSAGE hours
        hours_alloc_apprentissage = self.allocate_hours_per_subject(hours_apprentissage, prioritized)
        # Allocate REVISION hours (same proportions but focused on weak)
        hours_alloc_revision = self.allocate_hours_per_subject(hours_revision, prioritized)
        # Allocate LACUNES hours (only high/medium priority subjects)
        weak_subjects = [s for s in prioritized if s[2] in ['high', 'medium']]
        hours_alloc_lacunes = self.allocate_hours_per_subject(
            hours_lacunes, weak_subjects if weak_subjects else prioritized
        )
        
        print(f"[PLAN] Apprentissage alloc: {hours_alloc_apprentissage}")
        print(f"[PLAN] Revision alloc: {hours_alloc_revision}")
        print(f"[PLAN] Lacunes alloc: {hours_alloc_lacunes}")
        
        # STEP 7: Compute date boundaries for each phase
        phase1_days = int(days_remaining * phase_split["apprentissage"])
        phase2_days = int(days_remaining * phase_split["revision"])
        # phase3 = remaining days
        
        today = date.today()
        phase1_end = today + timedelta(days=phase1_days)
        phase2_end = phase1_end + timedelta(days=phase2_days)
        # Phase 3 runs until the day before exam (June 3 = dernière révision)
        phase3_end = self.exam_date - timedelta(days=1)
        
        print(f"[PLAN] Phase dates: P1 until {phase1_end}, P2 until {phase2_end}, P3 until {phase3_end}")

        # Fetch weak topics per subject once (reused across all phases)
        student_weak_topics = self._fetch_student_weak_topics(student_id, last_n=5)
        print(f"[PLAN] Weak topics from diagnostics: {student_weak_topics}")

        def _weak_for(subject_name: str) -> set[str]:
            return student_weak_topics.get((subject_name or '').lower(), set())

        # ── BAC 2026 topic priorities from historical atlas ──
        # HIGH-priority domains (predicted to fall in 2026) get an additional time boost
        # alongside the student's personal weak topics.
        bac2026_priorities: dict[str, set[str]] = {}
        try:
            from app.services.topic_atlas_service import topic_atlas
            for subj_item in prioritized:
                subj = subj_item[0]
                priorities = topic_atlas.predict_2026_priorities(subj)
                high_domains = {p['domain'].lower() for p in priorities.get('HIGH', [])}
                if high_domains:
                    bac2026_priorities[subj.lower()] = high_domains
            print(f"[PLAN] BAC 2026 HIGH-priority domains: {bac2026_priorities}")
        except Exception as e:
            print(f"[PLAN] atlas unavailable: {e}")

        def _bac_high_for(subject_name: str) -> set[str]:
            return bac2026_priorities.get((subject_name or '').lower(), set())

        def _combined_priority_topics(subject_name: str) -> set[str]:
            """Union of student's weak topics + BAC 2026 HIGH-priority domains."""
            return _weak_for(subject_name) | _bac_high_for(subject_name)

        # STEP 8: Build session queues for each phase
        sessions = []
        
        # ─── PHASE 1: APPRENTISSAGE (cours structurés) ───
        phase1_queue = []
        for item in prioritized:
            subject_name = item[0]
            score = item[1]
            priority = item[2]
            subject_id = subject_map.get(subject_name)
            if not subject_id:
                continue
            
            hours_for_subject = hours_alloc_apprentissage.get(subject_name, 0)
            if hours_for_subject <= 0:
                continue
            
            chapters = await self.get_chapters_for_subject(subject_id)
            if not chapters:
                continue
            
            # Filter chapters for advanced students with high scores
            if proficiency == "avancé" and score >= 65:
                filtered = [c for c in chapters if c.get('difficulty_level') in ['intermediate', 'advanced', None]]
                chapters = filtered or chapters

            # Priority chapters = student's weak topics UNION BAC 2026 HIGH-priority domains
            weak_set = _combined_priority_topics(subject_name)
            chapters = self._order_chapters_by_weakness(chapters, weak_set)
            
            hours_per_chapter = hours_for_subject / max(len(chapters), 1)
            for chapter in chapters:
                # Weak chapters get 1.5x time, strong chapters normal time
                is_weak = self._chapter_matches_weak(chapter, weak_set)
                chapter_hours = hours_per_chapter * (1.5 if is_weak else 1.0)
                num_sessions = max(1, int(chapter_hours / 1.25))  # ~75min sessions
                duration = min(90, max(45, int((chapter_hours * 60) / max(num_sessions, 1))))
                for _ in range(num_sessions):
                    phase1_queue.append({
                        'subject_name': subject_name,
                        'subject_id': subject_id,
                        'chapter': chapter,
                        'duration_minutes': duration,
                        'priority': priority,
                        'session_type': 'cours',
                        'is_weak_chapter': is_weak,
                    })
        
        # ─── PHASE 2: RÉVISION + EXAMENS BLANCS ───
        phase2_queue = []
        # One exam allocator per subject (round-robin over 2024/2025 exams)
        exam_allocators: dict[str, callable] = {}
        for item in prioritized:
            subject_name = item[0]
            score = item[1]
            priority = item[2]
            subject_id = subject_map.get(subject_name)
            if not subject_id:
                continue
            
            hours_for_subject = hours_alloc_revision.get(subject_name, 0)
            if hours_for_subject <= 0:
                continue
            
            chapters = await self.get_chapters_for_subject(subject_id)
            if not chapters:
                continue

            # Priority chapters first in revision queue (weak + BAC 2026 HIGH)
            weak_set = _combined_priority_topics(subject_name)
            chapters = self._order_chapters_by_weakness(chapters, weak_set)
            
            # Revision: cover each chapter with shorter sessions
            hours_per_chapter = hours_for_subject / max(len(chapters), 1)
            for chapter in chapters:
                num_sessions = max(1, int(hours_per_chapter / 1.0))
                duration = min(60, max(30, int((hours_per_chapter * 60) / max(num_sessions, 1))))
                for _ in range(num_sessions):
                    phase2_queue.append({
                        'subject_name': subject_name,
                        'subject_id': subject_id,
                        'chapter': chapter,
                        'duration_minutes': duration,
                        'priority': priority,
                        'session_type': 'revision',
                        'is_weak_chapter': self._chapter_matches_weak(chapter, weak_set),
                    })
            
            # Add 1 exam blanc session per subject (90 min) with a REAL BAC exam attached
            if chapters:
                if subject_name not in exam_allocators:
                    exam_allocators[subject_name] = self._get_exam_id_allocator(subject_name)
                exam_source_id = exam_allocators[subject_name]()
                phase2_queue.append({
                    'subject_name': subject_name,
                    'subject_id': subject_id,
                    'chapter': chapters[0],  # Placeholder; the real exam overrides content
                    'duration_minutes': 90,
                    'priority': priority,
                    'session_type': 'examen_blanc',
                    'exam_source_id': exam_source_id,
                })
        
        # ─── PHASE 3: LACUNES + DERNIÈRES RÉVISIONS ───
        phase3_queue = []
        target_subjects = weak_subjects if weak_subjects else prioritized
        for item in target_subjects:
            subject_name = item[0]
            score = item[1]
            priority = item[2]
            subject_id = subject_map.get(subject_name)
            if not subject_id:
                continue
            
            hours_for_subject = hours_alloc_lacunes.get(subject_name, 0)
            if hours_for_subject <= 0:
                continue
            
            chapters = await self.get_chapters_for_subject(subject_id)
            if not chapters:
                continue
            
            # Focus on weak chapters (diagnostic) + BAC 2026 HIGH-priority domains
            weak_set = _combined_priority_topics(subject_name)
            weak_chapters = [c for c in chapters if self._chapter_matches_weak(c, weak_set)]
            if weak_chapters:
                focus_chapters = weak_chapters
                print(f"[PLAN] Phase 3 ({subject_name}): {len(focus_chapters)} weak chapters matched")
            else:
                # Fallback: first half of chapters if no weak_topics match
                focus_chapters = chapters[:max(2, len(chapters) // 2)]
                print(f"[PLAN] Phase 3 ({subject_name}): no weak match, falling back to {len(focus_chapters)} chapters")

            hours_per_chapter = hours_for_subject / max(len(focus_chapters), 1)
            for chapter in focus_chapters:
                num_sessions = max(1, int(hours_per_chapter / 1.0))
                duration = min(60, max(30, int((hours_per_chapter * 60) / max(num_sessions, 1))))
                for _ in range(num_sessions):
                    phase3_queue.append({
                        'subject_name': subject_name,
                        'subject_id': subject_id,
                        'chapter': chapter,
                        'duration_minutes': duration,
                        'priority': priority,
                        'session_type': 'lacunes',
                        'is_weak_chapter': bool(weak_chapters),
                    })
            
            # Add final exam blanc with a REAL BAC exam attached
            if chapters:
                if subject_name not in exam_allocators:
                    exam_allocators[subject_name] = self._get_exam_id_allocator(subject_name)
                exam_source_id = exam_allocators[subject_name]()
                phase3_queue.append({
                    'subject_name': subject_name,
                    'subject_id': subject_id,
                    'chapter': chapters[0],
                    'duration_minutes': 90,
                    'priority': priority,
                    'session_type': 'examen_blanc',
                    'exam_source_id': exam_source_id,
                })
        
        print(f"[PLAN] Queues: P1={len(phase1_queue)}, P2={len(phase2_queue)}, P3={len(phase3_queue)}")
        
        # STEP 9: Schedule sessions across dates with progressive intensity
        # Slot templates by intensity level
        _SLOTS = {
            'light': {
                'weekday': ["16:00-17:00", "17:15-18:00"],
                'weekend': ["14:00-15:00", "15:15-16:00", "16:15-17:00"],
                'sunday':  ["15:00-16:00"],
            },
            'moderate': {
                'weekday': ["16:00-16:50", "17:00-17:50", "18:00-18:50"],
                'weekend': ["14:00-14:50", "15:00-15:50", "16:00-16:50", "17:00-17:50"],
                'sunday':  ["15:00-15:50"],
            },
            'intense': {
                'weekday': ["16:00-16:45", "16:55-17:40", "17:50-18:35", "18:45-19:30"],
                'weekend': ["14:00-14:45", "15:00-15:45", "16:00-16:45", "17:00-17:45", "18:00-18:45"],
                'sunday':  ["15:00-15:45", "16:00-16:45"],
            },
            'crunch': {
                'weekday': ["15:30-16:10", "16:20-17:00", "17:10-17:50", "18:00-18:40", "18:50-19:30"],
                'weekend': ["10:00-10:40", "10:50-11:30", "14:00-14:40", "14:50-15:30", "15:40-16:20", "16:30-17:10"],
                'sunday':  ["15:00-15:40", "15:50-16:30"],
            },
        }

        def _intensity_for_day(d: date) -> str:
            """Pick intensity level based on how many days remain until exam."""
            days_left = (self.exam_date - d).days
            if days_left <= 14:
                return 'crunch'
            elif days_left <= 30:
                return 'intense'
            elif days_left <= 60:
                return 'moderate'
            return 'light'

        def _day_slots(d: date) -> list[str]:
            """Return time slots for a given date."""
            intensity = _intensity_for_day(d)
            template = _SLOTS[intensity]
            if d.weekday() == 6:
                return template['sunday']
            elif d.weekday() >= 5:
                return template['weekend']
            return template['weekday']

        def schedule_queue(queue, start_date, end_date):
            """Schedule sessions spread **evenly** across the date range.

            Instead of front-loading (filling day-by-day until the queue
            runs out — which leaves the tail end empty), we collect every
            available (date, slot) pair and pick evenly-spaced indices so
            the sessions cover the entire phase, including the last days.
            """
            scheduled = []
            if not queue:
                return scheduled

            # 1. Collect every available (date, time_slot) pair
            all_slots: list[tuple] = []
            d = start_date
            while d <= end_date:
                for slot in _day_slots(d):
                    all_slots.append((d, slot))
                d += timedelta(days=1)

            if not all_slots:
                return scheduled

            n_sessions = len(queue)
            n_slots = len(all_slots)

            # 2. Pick evenly-spaced slot indices
            if n_sessions >= n_slots:
                # More sessions than slots → fill every slot (excess dropped)
                indices = list(range(n_slots))
            elif n_sessions == 1:
                indices = [0]
            else:
                # Spread across the full range: first session → first slot,
                # last session → last slot, rest evenly in between.
                indices = [round(i * (n_slots - 1) / (n_sessions - 1))
                           for i in range(n_sessions)]

            # 3. Place sessions into the selected slots
            for q_idx, slot_idx in enumerate(indices):
                if q_idx >= len(queue) or slot_idx >= len(all_slots):
                    break
                day, time_slot = all_slots[slot_idx]
                item = queue[q_idx]

                # Compute duration from slot width (fallback to item duration)
                try:
                    st, et = time_slot.split('-')
                    sh, sm = map(int, st.split(':'))
                    eh, em = map(int, et.split(':'))
                    slot_minutes = (eh * 60 + em) - (sh * 60 + sm)
                except Exception:
                    slot_minutes = item['duration_minutes']

                session_row = {
                    "id": str(uuid.uuid4()),
                    "plan_id": plan_id,
                    "subject_id": item['subject_id'],
                    "chapter_id": item['chapter']['id'],
                    "scheduled_date": day.isoformat(),
                    "scheduled_time": time_slot,
                    "duration_minutes": slot_minutes,
                    "priority": item['priority'],
                    "status": "pending",
                    "session_type": item.get('session_type', 'cours'),
                }
                if item.get('exam_source_id'):
                    session_row['exam_source_id'] = item['exam_source_id']
                scheduled.append(session_row)

            return scheduled
        
        # Interleave subjects within each phase queue for variety
        def interleave_queue(queue):
            """Reorder queue so subjects alternate (round-robin)."""
            if not queue:
                return queue
            by_subject = {}
            for item in queue:
                by_subject.setdefault(item['subject_name'], []).append(item)
            
            result = []
            subject_keys = list(by_subject.keys())
            while any(by_subject[k] for k in subject_keys):
                for k in subject_keys:
                    if by_subject[k]:
                        result.append(by_subject[k].pop(0))
            return result
        
        phase1_queue = interleave_queue(phase1_queue)
        phase2_queue = interleave_queue(phase2_queue)
        phase3_queue = interleave_queue(phase3_queue)
        
        sessions_p1 = schedule_queue(phase1_queue, today, phase1_end)
        sessions_p2 = schedule_queue(phase2_queue, phase1_end + timedelta(days=1), phase2_end)
        sessions_p3 = schedule_queue(phase3_queue, phase2_end + timedelta(days=1), phase3_end)
        
        sessions = sessions_p1 + sessions_p2 + sessions_p3
        
        print(f"[PLAN] Scheduled: P1={len(sessions_p1)}, P2={len(sessions_p2)}, P3={len(sessions_p3)}, Total={len(sessions)}")
        
        # STEP 10: Insert sessions
        if sessions:
            # Insert in batches of 50 to avoid payload limits
            strip_exam_source_id = False
            for i in range(0, len(sessions), 50):
                batch = sessions[i:i+50]
                if strip_exam_source_id:
                    batch = [{k: v for k, v in s.items() if k != 'exam_source_id'} for s in batch]
                try:
                    self.supabase.table('study_plan_sessions').insert(batch).execute()
                except Exception as e:
                    # If the column doesn't exist yet (migration 003 not applied),
                    # strip exam_source_id and retry — once — for this and future batches.
                    err = str(e).lower()
                    if not strip_exam_source_id and ('exam_source_id' in err or 'column' in err):
                        _log.warning(
                            "[PLAN] exam_source_id column missing, falling back "
                            "(apply migrations/003_add_exam_source_id.sql to enable real exams on examen_blanc)"
                        )
                        strip_exam_source_id = True
                        batch = [{k: v for k, v in s.items() if k != 'exam_source_id'} for s in batch]
                        self.supabase.table('study_plan_sessions').insert(batch).execute()
                    else:
                        raise
        
        # Count sessions per subject
        subject_counts = {}
        for s in sessions:
            sid = s['subject_id']
            subject_counts[sid] = subject_counts.get(sid, 0) + 1
        print(f"[PLAN] Sessions per subject: {subject_counts}")
        
        if sessions:
            print(f"[PLAN] Date range: {sessions[0]['scheduled_date']} to {sessions[-1]['scheduled_date']}")
        
        # Update student profile
        self.supabase.table('student_profiles').update({
            "coaching_mode_active": True,
            "current_plan_id": plan_id,
            "overall_progress": 0
        }).eq('student_id', student_id).execute()
        
        return {
            "plan_id": plan_id,
            "days_remaining": days_remaining,
            "total_hours": total_hours,
            "sessions_count": len(sessions),
            "phase_split": {
                "apprentissage": {"hours": hours_apprentissage, "sessions": len(sessions_p1), "end_date": phase1_end.isoformat()},
                "revision": {"hours": hours_revision, "sessions": len(sessions_p2), "end_date": phase2_end.isoformat()},
                "lacunes": {"hours": hours_lacunes, "sessions": len(sessions_p3), "end_date": phase3_end.isoformat()},
            },
            "exam_weights_used": bool(exam_weights),
            "sessions": sessions[:10]
        }

    async def get_active_plan(self, student_id: str) -> Optional[dict]:
        """Get the active study plan for a student (most recent one)"""
        result = self.supabase.table('study_plans').select(
            '*'
        ).eq('student_id', student_id).eq('status', 'active').order(
            'created_at', desc=True
        ).limit(1).execute()

        if not result.data:
            return None

        plan = result.data[0]

        sessions_result = self.supabase.table('study_plan_sessions').select(
            'id, status'
        ).eq('plan_id', plan['id']).execute()

        sessions_data = sessions_result.data if sessions_result and sessions_result.data else []
        total_sessions = len(sessions_data)
        completed_sessions = sum(1 for s in sessions_data if s.get('status') == 'completed')

        plan['total_sessions'] = total_sessions
        plan['completed_sessions'] = completed_sessions
        plan['progress_percentage'] = (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
        if plan.get('diagnostic_scores') is None:
            plan['diagnostic_scores'] = {}

        return plan

    async def get_today_schedule(self, student_id: str) -> list:
        """Get today's scheduled sessions"""
        plan = await self.get_active_plan(student_id)
        if not plan:
            return []

        today = date.today().isoformat()

        result = self.supabase.table('study_plan_sessions').select(
            '*, subjects(name_fr), chapters(title_fr, chapter_number)'
        ).eq('plan_id', plan['id']).eq('scheduled_date', today).order(
            'scheduled_time'
        ).execute()

        sessions = result.data if result.data else []
        all_sessions_result = self.supabase.table('study_plan_sessions').select(
            'id, status'
        ).eq('plan_id', plan['id']).order('scheduled_date').order('scheduled_time').execute()
        ordered_sessions = all_sessions_result.data if all_sessions_result.data else []

        unlocked_session_id = None
        for ordered in ordered_sessions:
            if ordered.get('status') != 'completed':
                unlocked_session_id = ordered.get('id')
                break

        for session in sessions:
            session['is_unlocked'] = session.get('status') == 'completed' or session.get('id') == unlocked_session_id

        return sessions

    async def get_all_sessions(self, student_id: str) -> dict:
        """Get all sessions grouped by date and subject"""
        # Get active plan
        plan = await self.get_active_plan(student_id)
        if not plan:
            return {"sessions_by_date": {}, "sessions_by_subject": {}}
        
        # Get all sessions for the plan
        result = self.supabase.table('study_plan_sessions').select(
            '*, subjects(name_fr, id), chapters(title_fr, chapter_number)'
        ).eq('plan_id', plan['id']).order('scheduled_date').order('scheduled_time').execute()
        
        sessions = result.data if result.data else []
        first_pending_id = None
        for session in sessions:
            if session['status'] != 'completed':
                first_pending_id = session['id']
                break
        
        # Group by date
        sessions_by_date = {}
        sessions_by_subject = {}
        
        for session in sessions:
            session['is_unlocked'] = session['status'] == 'completed' or session['id'] == first_pending_id
            # Group by date
            session_date = session['scheduled_date']
            if session_date not in sessions_by_date:
                sessions_by_date[session_date] = []
            sessions_by_date[session_date].append(session)
            
            # Group by subject
            subject_name = session['subjects']['name_fr'] if session.get('subjects') else 'Autre'
            if subject_name not in sessions_by_subject:
                sessions_by_subject[subject_name] = []
            sessions_by_subject[subject_name].append(session)
        
        total_duration = sum(s.get('duration_minutes', 0) for s in sessions)
        completed_duration = sum(s.get('duration_minutes', 0) for s in sessions if s['status'] == 'completed')
        
        return {
            "sessions_by_date": sessions_by_date,
            "sessions_by_subject": sessions_by_subject,
            "total_sessions": len(sessions),
            "total_duration_minutes": total_duration,
            "completed_duration_minutes": completed_duration,
        }
    
    async def mark_session_completed(self, session_id: str, student_id: str) -> dict:
        """Mark a session as completed and update progress"""
        # Update session
        self.supabase.table('study_plan_sessions').update({
            "status": "completed",
            "completed_at": datetime.utcnow().isoformat()
        }).eq('id', session_id).execute()
        
        # Get plan and recalculate progress
        session_result = self.supabase.table('study_plan_sessions').select(
            'plan_id'
        ).eq('id', session_id).execute()
        
        if not session_result.data:
            return {"success": False}
        
        plan_id = session_result.data[0]['plan_id']
        
        # Calculate new progress
        all_sessions = self.supabase.table('study_plan_sessions').select(
            'id, status, subject_id'
        ).eq('plan_id', plan_id).execute()
        
        total = len(all_sessions.data)
        completed = sum(1 for s in all_sessions.data if s['status'] == 'completed')
        progress = (completed / total * 100) if total > 0 else 0
        
        # Calculate per-subject progress
        subject_progress = {}
        for session in all_sessions.data:
            subject_id = session['subject_id']
            if subject_id not in subject_progress:
                subject_progress[subject_id] = {'total': 0, 'completed': 0}
            subject_progress[subject_id]['total'] += 1
            if session['status'] == 'completed':
                subject_progress[subject_id]['completed'] += 1
        
        # Convert to percentages
        subject_progress_pct = {
            sid: (data['completed'] / data['total'] * 100)
            for sid, data in subject_progress.items()
        }
        
        # Update student profile
        self.supabase.table('student_profiles').update({
            "overall_progress": round(progress, 2),
            "subject_progress": subject_progress_pct
        }).eq('student_id', student_id).execute()
        
        return {
            "success": True,
            "overall_progress": round(progress, 2),
            "completed_sessions": completed,
            "total_sessions": total
        }
    
    async def get_progress(self, student_id: str) -> dict:
        """Get overall and per-subject progress"""
        profile_result = self.supabase.table('student_profiles').select(
            'overall_progress, subject_progress'
        ).eq('student_id', student_id).execute()
        
        if not profile_result.data:
            return {"overall_progress": 0, "subject_progress": {}}
        
        return profile_result.data[0]

    # ══════════════════════════════════════════════════════════════
    #  ADAPTIVE COACHING ENGINE — Powered by Proficiency Agent
    # ══════════════════════════════════════════════════════════════

    async def get_adaptive_next_session(self, student_id: str) -> dict:
        """
        Determine the BEST thing for this student to study RIGHT NOW,
        using live proficiency data + pedagogical principles.

        Decision algorithm (priority order):
        1. CRITICAL LACUNES (score < 15%) on high-coefficient subjects → prerequisite review
        2. ZPD LACUNES (score 15-55%) → optimal learning zone, most efficient use of time
        3. SPACED REPETITION → topics not reviewed in 7+ days that need consolidation
        4. NEXT PLANNED SESSION → fall back to the regular study plan
        5. EXAM PRACTICE → if all topics are "acquis", practice with real BAC exams

        Returns:
        {
            "recommendation": "lacune_critique" | "zpd_optimal" | "spaced_review" | "plan_next" | "exam_practice",
            "subject": "Mathématiques",
            "subject_id": "...",
            "topic": "Suites numériques",
            "chapter_id": "...",
            "chapter_title": "...",
            "reason": "Score de 22% en Suites numériques (coeff 7). Zone proximale basse...",
            "session_type": "cours" | "revision" | "exercices" | "examen_blanc",
            "duration_minutes": 60,
            "proficiency_score": 22.0,
            "bac_coefficient": 7,
            "zpd_strategy": "Explication guidée avec exemples simples",
        }
        """
        try:
            from app.services.student_proficiency_service import proficiency_service
            summary = await proficiency_service.get_proficiency_summary(student_id)
        except Exception as e:
            _log.error(f"[AdaptiveCoach] Proficiency fetch failed: {e}")
            summary = {"total_answers": 0, "lacunes": [], "subjects": {}, "strengths": []}

        # Get subject map for chapter lookup
        subjects_result = self.supabase.table('subjects').select('id, name_fr').execute()
        subject_map = {s['name_fr']: s['id'] for s in (subjects_result.data or [])}

        # ── Priority 0: Recurring errors (patterns of repeated failure) ──
        # These take precedence over everything else: the student is actively
        # failing the SAME topic multiple times. Fix the pattern before
        # moving on. See StudentProficiencyService._detect_recurring_errors.
        recurring_errors = summary.get("recurring_errors") or []
        if recurring_errors:
            top = recurring_errors[0]  # Already sorted by urgency
            chapter = await self._find_chapter_for_topic(top["subject"], top["topic"], subject_map)
            pattern = top.get("pattern", "struggling")
            # Session type adapts to the error pattern
            if pattern == "total_block":
                session_type = "cours"          # Back to basics
                duration = 60
            elif pattern == "conceptual":
                session_type = "revision"       # Clarify the misconception
                duration = 45
            elif pattern == "regressing":
                session_type = "revision"       # Refresh forgotten knowledge
                duration = 30
            else:
                session_type = "exercices"      # Guided practice with scaffolding
                duration = 45
            return {
                "recommendation": "erreur_recurrente",
                "subject": top["subject"],
                "subject_id": subject_map.get(top["subject"], ""),
                "topic": top["topic"],
                "chapter_id": chapter["id"] if chapter else "",
                "chapter_title": chapter["title_fr"] if chapter else top["topic"],
                "reason": (
                    f"⚠️ Erreur récurrente détectée: {top['streak_errors']} échecs consécutifs "
                    f"en {top['topic']} ({top['subject']}, coeff {top['bac_coefficient']}) "
                    f"sur {top['total_attempts']} tentatives. "
                    f"Type: {pattern}. {top.get('action', '')}"
                ),
                "session_type": session_type,
                "duration_minutes": duration,
                "proficiency_score": None,
                "bac_coefficient": top["bac_coefficient"],
                "zpd_strategy": top.get("action", "Remédiation ciblée"),
                "error_pattern": pattern,
                "streak_errors": top["streak_errors"],
            }

        # ── Priority 1: Critical lacunes (below ZPD) ──
        if summary.get("lacunes"):
            for lac in summary["lacunes"]:
                if lac.get("priority") == "critique":
                    chapter = await self._find_chapter_for_topic(lac["subject"], lac["topic"], subject_map)
                    return {
                        "recommendation": "lacune_critique",
                        "subject": lac["subject"],
                        "subject_id": subject_map.get(lac["subject"], ""),
                        "topic": lac["topic"],
                        "chapter_id": chapter["id"] if chapter else "",
                        "chapter_title": chapter["title_fr"] if chapter else lac["topic"],
                        "reason": (
                            f"Score critique de {lac['score']}% en {lac['topic']} ({lac['subject']}, "
                            f"coeff {lac.get('bac_coefficient', 5)}). "
                            f"Les bases ne sont pas acquises — il faut reprendre les prérequis."
                        ),
                        "session_type": "cours",
                        "duration_minutes": 60,
                        "proficiency_score": lac["score"],
                        "bac_coefficient": lac.get("bac_coefficient", 5),
                        "zpd_strategy": lac.get("zpd_action", "Reprendre les bases"),
                    }

        # ── Priority 2: ZPD lacunes (optimal learning zone) ──
        if summary.get("lacunes"):
            # Sort by urgency (high coefficient * low score)
            zpd_lacunes = [l for l in summary["lacunes"] if l.get("priority") in ("haute", "moyenne")]
            if zpd_lacunes:
                best = zpd_lacunes[0]
                chapter = await self._find_chapter_for_topic(best["subject"], best["topic"], subject_map)
                session_type = "exercices" if best["score"] >= 30 else "cours"
                return {
                    "recommendation": "zpd_optimal",
                    "subject": best["subject"],
                    "subject_id": subject_map.get(best["subject"], ""),
                    "topic": best["topic"],
                    "chapter_id": chapter["id"] if chapter else "",
                    "chapter_title": chapter["title_fr"] if chapter else best["topic"],
                    "reason": (
                        f"Score de {best['score']}% en {best['topic']} ({best['subject']}). "
                        f"Cette compétence est dans ta zone d'apprentissage optimale (ZPD). "
                        f"C'est le meilleur moment pour progresser!"
                    ),
                    "session_type": session_type,
                    "duration_minutes": 45 if session_type == "exercices" else 60,
                    "proficiency_score": best["score"],
                    "bac_coefficient": best.get("bac_coefficient", 5),
                    "zpd_strategy": best.get("zpd_action", "Exercices progressifs avec étayage"),
                }

        # ── Priority 3: Spaced repetition (topics not reviewed recently) ──
        stale_topic = await self._find_stale_topic(student_id, summary, subject_map)
        if stale_topic:
            return stale_topic

        # ── Priority 4: Next planned session ──
        plan = await self.get_active_plan(student_id)
        if plan:
            today = date.today().isoformat()
            next_session = self.supabase.table('study_plan_sessions').select(
                '*, subjects(name_fr), chapters(title_fr)'
            ).eq('plan_id', plan['id']).eq('status', 'pending').gte(
                'scheduled_date', today
            ).order('scheduled_date').order('scheduled_time').limit(1).execute()

            if next_session.data:
                s = next_session.data[0]
                subj_name = s.get('subjects', {}).get('name_fr', '')
                chap_title = s.get('chapters', {}).get('title_fr', '')
                return {
                    "recommendation": "plan_next",
                    "subject": subj_name,
                    "subject_id": s.get("subject_id", ""),
                    "topic": chap_title,
                    "chapter_id": s.get("chapter_id", ""),
                    "chapter_title": chap_title,
                    "reason": f"Session planifiée: {s.get('session_type', 'cours')} — {chap_title} ({subj_name})",
                    "session_type": s.get("session_type", "cours"),
                    "duration_minutes": s.get("duration_minutes", 60),
                    "proficiency_score": None,
                    "bac_coefficient": BAC_COEFFICIENTS.get(subj_name, 5),
                    "zpd_strategy": "",
                    "plan_session_id": s["id"],
                }

        # ── Priority 5: Exam practice (all topics are "acquis") ──
        return {
            "recommendation": "exam_practice",
            "subject": "",
            "subject_id": "",
            "topic": "Examen blanc",
            "chapter_id": "",
            "chapter_title": "Entraînement BAC complet",
            "reason": (
                "Toutes les compétences sont acquises ou en cours de consolidation. "
                "Entraîne-toi avec un sujet complet du BAC pour gagner en rapidité et confiance."
            ),
            "session_type": "examen_blanc",
            "duration_minutes": 90,
            "proficiency_score": summary.get("overall_score", 0),
            "bac_coefficient": 0,
            "zpd_strategy": "Pratique en conditions d'examen",
        }

    async def _find_chapter_for_topic(self, subject_name: str, topic: str, subject_map: dict) -> Optional[dict]:
        """Find the best matching chapter for a topic name."""
        subject_id = subject_map.get(subject_name)
        if not subject_id:
            return None
        try:
            chapters = self.supabase.table('chapters').select(
                'id, title_fr, chapter_number'
            ).eq('subject_id', subject_id).execute()
            if not chapters.data:
                return None
            # Fuzzy match: find chapter whose title contains the topic name (or vice versa)
            topic_lower = topic.lower()
            for ch in chapters.data:
                if topic_lower in ch['title_fr'].lower() or ch['title_fr'].lower() in topic_lower:
                    return ch
            # Fallback: first chapter
            return chapters.data[0]
        except Exception:
            return None

    async def _find_stale_topic(self, student_id: str, summary: dict, subject_map: dict) -> Optional[dict]:
        """
        Find a topic that was studied but not reviewed recently
        and is not yet "maîtrisé" — needs spaced repetition.
        Interval adapts to exam proximity:
        - >60 days: 7 days
        - 30-60 days: 4 days
        - <30 days: 2 days
        """
        try:
            days_left = self.calculate_days_until_exam()
            if days_left <= 30:
                stale_days = 2
            elif days_left <= 60:
                stale_days = 4
            else:
                stale_days = 7
            cutoff = (datetime.utcnow() - timedelta(days=stale_days)).isoformat()
            # Get topics with answers, ordered by last activity (oldest first)
            result = self.supabase.table('student_answer_history').select(
                'subject, topic, created_at'
            ).eq('student_id', student_id).lt(
                'created_at', cutoff
            ).order('created_at').limit(50).execute()

            if not result.data:
                return None

            # Find the oldest topic that's not mastered
            seen = set()
            for row in result.data:
                key = f"{row['subject']}|{row['topic']}"
                if key in seen:
                    continue
                seen.add(key)
                subj = row['subject']
                topic = row['topic']

                # Check if this topic is mastered
                subj_data = summary.get("subjects", {}).get(subj, {})
                topic_data = subj_data.get("topics", {}).get(topic, {})
                score = topic_data.get("score", 50)

                if score < 75:  # Not yet mastered → needs review
                    chapter = await self._find_chapter_for_topic(subj, topic, subject_map)
                    return {
                        "recommendation": "spaced_review",
                        "subject": subj,
                        "subject_id": subject_map.get(subj, ""),
                        "topic": topic,
                        "chapter_id": chapter["id"] if chapter else "",
                        "chapter_title": chapter["title_fr"] if chapter else topic,
                        "reason": (
                            f"Tu n'as pas revu {topic} ({subj}) depuis plus de 7 jours "
                            f"(score: {score}%). La révision espacée renforce ta mémoire à long terme."
                        ),
                        "session_type": "revision",
                        "duration_minutes": 30,
                        "proficiency_score": score,
                        "bac_coefficient": BAC_COEFFICIENTS.get(subj, 5),
                        "zpd_strategy": "Révision rapide + exercices ciblés",
                    }
        except Exception as e:
            _log.error(f"[AdaptiveCoach] Stale topic search failed: {e}")
        return None

    async def get_coaching_session_context(self, student_id: str) -> dict:
        """
        Generate full coaching context for a session, combining:
        - Live proficiency data from agent
        - Study plan progress
        - Adaptive recommendation for what to do next

        This is injected into the LLM system prompt during coaching sessions.
        """
        try:
            from app.services.student_proficiency_service import proficiency_service
            prof_summary = await proficiency_service.get_proficiency_summary(student_id)
            llm_ctx = await proficiency_service.get_llm_context(student_id)
        except Exception:
            prof_summary = {"total_answers": 0}
            llm_ctx = {}

        recommendation = await self.get_adaptive_next_session(student_id)
        plan = await self.get_active_plan(student_id)

        return {
            "proficiency": llm_ctx,
            "recommendation": recommendation,
            "plan_progress": plan.get("progress_percentage", 0) if plan else 0,
            "total_answers": prof_summary.get("total_answers", 0),
            "days_remaining": self.calculate_days_until_exam(),
        }

    async def adapt_plan_from_proficiency(self, student_id: str) -> dict:
        """
        Re-prioritize the existing study plan based on LIVE proficiency data.
        Called after significant proficiency changes (e.g. after exam submission).

        This reorders pending sessions to prioritize:
        1. Topics with critical/haute lacunes
        2. Topics within ZPD (most efficient learning)
        3. High-coefficient subjects
        """
        plan = await self.get_active_plan(student_id)
        if not plan:
            return {"adapted": False, "reason": "No active plan"}

        try:
            from app.services.student_proficiency_service import proficiency_service
            summary = await proficiency_service.get_proficiency_summary(student_id)
        except Exception:
            return {"adapted": False, "reason": "Proficiency data unavailable"}

        if summary.get("total_answers", 0) < 5:
            return {"adapted": False, "reason": "Not enough data yet (< 5 answers)"}

        # Get all pending sessions
        pending = self.supabase.table('study_plan_sessions').select(
            '*, subjects(name_fr), chapters(title_fr)'
        ).eq('plan_id', plan['id']).eq('status', 'pending').order(
            'scheduled_date'
        ).order('scheduled_time').execute()

        if not pending.data or len(pending.data) < 2:
            return {"adapted": False, "reason": "Too few pending sessions"}

        # Build urgency score for each session based on proficiency
        lacune_topics = {
            f"{l['subject']}|{l.get('topic', '')}": l
            for l in summary.get("lacunes", [])
        }

        sessions_with_score = []
        for s in pending.data:
            subj_name = s.get('subjects', {}).get('name_fr', '')
            chap_title = s.get('chapters', {}).get('title_fr', '')

            # Check if this session's topic is a lacune
            urgency = 50  # Default mid-priority
            for key, lac in lacune_topics.items():
                if lac['subject'] == subj_name and (
                    lac.get('topic', '').lower() in chap_title.lower() or
                    chap_title.lower() in lac.get('topic', '').lower()
                ):
                    urgency = lac.get('urgency', 70)
                    break

            # Boost by BAC coefficient
            coeff = BAC_COEFFICIENTS.get(subj_name, 5)
            urgency *= (coeff / 9.0)

            sessions_with_score.append((s, urgency))

        # Sort by urgency (highest first)
        sessions_with_score.sort(key=lambda x: -x[1])

        # Re-assign dates: keep the same date slots but reorder sessions
        original_dates = [(s['scheduled_date'], s['scheduled_time']) for s in pending.data]
        reordered_count = 0

        for i, (session, _) in enumerate(sessions_with_score):
            if i >= len(original_dates):
                break
            new_date, new_time = original_dates[i]
            if session['scheduled_date'] != new_date or session['scheduled_time'] != new_time:
                self.supabase.table('study_plan_sessions').update({
                    'scheduled_date': new_date,
                    'scheduled_time': new_time,
                }).eq('id', session['id']).execute()
                reordered_count += 1

        _log.info(f"[AdaptiveCoach] Adapted plan for {student_id[:8]}: "
                  f"reordered {reordered_count}/{len(pending.data)} sessions")

        return {
            "adapted": True,
            "sessions_reordered": reordered_count,
            "total_pending": len(pending.data),
            "top_priority": sessions_with_score[0][0].get('chapters', {}).get('title_fr', '') if sessions_with_score else "",
        }


study_plan_service = StudyPlanService()
