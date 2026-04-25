import re


class ResourceDecisionService:
    def decide(
        self,
        *,
        phase: str,
        student_text: str,
        lesson_title: str,
        objective: str,
        proficiency: str,
        available_resource_types: list[str] | set[str] | None = None,
        recent_modes: list[str] | None = None,
        simulation_active: bool = False,
    ) -> dict:
        lower_student_text = (student_text or "").lower()
        available = set(available_resource_types or [])
        recent = list(recent_modes or [])
        preferred_mode = self._detect_explicit_mode(lower_student_text)
        explicit_draw_request = preferred_mode == "whiteboard"
        explicit_media_request = preferred_mode in {"image", "simulation", "video", "exam"}
        concept_type = self._infer_concept_type(
            f"{lesson_title or ''} {objective or ''} {student_text or ''}".lower()
        )

        scores = {
            "whiteboard": 0,
            "image": 0,
            "simulation": 0,
            "video": 0,
            "exercise": 0,
            "evaluation": 0,
            "exam": 0,
        }
        reasons = {mode: [] for mode in scores}

        if preferred_mode:
            scores[preferred_mode] += 100
            reasons[preferred_mode].append("explicit_request")

        phase_weights = {
            "activation": {"image": 4, "whiteboard": 2},
            "exploration": {"simulation": 5, "image": 2},
            "explanation": {"whiteboard": 5, "image": 2},
            "application": {"exercise": 5, "simulation": 3, "whiteboard": 1},
            "consolidation": {"evaluation": 5, "image": 1},
        }
        for mode, weight in phase_weights.get(phase or "", {}).items():
            scores[mode] += weight
            reasons[mode].append(f"phase_{phase}")

        concept_weights = {
            "dynamic_process": {"simulation": 4, "whiteboard": 2, "image": 1},
            "structural_visual": {"image": 4, "whiteboard": 2},
            "comparative": {"whiteboard": 4, "image": 2, "simulation": 1},
            "causal_mechanism": {"whiteboard": 4, "simulation": 2},
            "exercise_practice": {"exercise": 4, "whiteboard": 1},
            "assessment": {"evaluation": 4, "image": 1},
        }
        for mode, weight in concept_weights.get(concept_type, {}).items():
            scores[mode] += weight
            reasons[mode].append(f"concept_{concept_type}")

        proficiency_text = (proficiency or "").lower()
        if "début" in proficiency_text or "debut" in proficiency_text or "faible" in proficiency_text:
            scores["image"] += 2
            scores["whiteboard"] += 2
            scores["simulation"] -= 1
            reasons["image"].append("beginner_support")
            reasons["whiteboard"].append("beginner_support")
        elif "avanc" in proficiency_text:
            scores["simulation"] += 2
            scores["exercise"] += 1
            reasons["simulation"].append("advanced_support")

        if simulation_active:
            scores["simulation"] -= 1
            scores["whiteboard"] += 1
            reasons["whiteboard"].append("simulation_already_active")

        if recent:
            last_mode = recent[-1]
            if last_mode in scores:
                scores[last_mode] -= 2
                reasons[last_mode].append("repeat_penalty")

        if len(recent) >= 2 and recent[-1] == recent[-2] and recent[-1] in scores:
            scores[recent[-1]] -= 2
            reasons[recent[-1]].append("double_repeat_penalty")

        for mode in ["image", "simulation", "video", "exam"]:
            if available and mode not in available:
                scores[mode] -= 6
                reasons[mode].append("resource_unavailable")

        primary_mode = max(scores, key=scores.get)
        fallback_mode = self._best_available_resource_mode(scores, available)
        chosen_resource_type = preferred_mode if explicit_media_request else fallback_mode
        should_prepare_whiteboard = primary_mode == "whiteboard" and not explicit_media_request
        auto_present_resource = explicit_media_request

        if not auto_present_resource and phase == "exploration" and chosen_resource_type == "simulation":
            auto_present_resource = any(
                token in lower_student_text
                for token in ["voir", "montre", "montrer", "observer", "tester", "comparer"]
            ) and not simulation_active

        if not auto_present_resource and phase == "activation" and chosen_resource_type == "image":
            auto_present_resource = any(
                token in lower_student_text
                for token in ["quoi", "qu'est", "c'est quoi", "voir", "montre", "montrer"]
            )

        return {
            "primary_mode": primary_mode,
            "preferred_resource_type": preferred_mode if explicit_media_request else None,
            "resource_type_for_suggestion": chosen_resource_type,
            "explicit_draw_request": explicit_draw_request,
            "explicit_media_request": explicit_media_request,
            "should_prepare_whiteboard": should_prepare_whiteboard,
            "auto_present_resource": auto_present_resource,
            "concept_type": concept_type,
            "reason_code": reasons[primary_mode][0] if reasons[primary_mode] else "default",
            "confidence": max(scores.values()),
            "max_tokens": 2000 if (should_prepare_whiteboard or explicit_draw_request) else 800,
            "scores": scores,
        }

    def choose_resource_type(
        self,
        *,
        phase: str,
        lesson_title: str,
        objective: str,
        proficiency: str,
        available_resource_types: list[str] | set[str] | None = None,
        recent_modes: list[str] | None = None,
        simulation_active: bool = False,
    ) -> str:
        decision = self.decide(
            phase=phase,
            student_text="",
            lesson_title=lesson_title,
            objective=objective,
            proficiency=proficiency,
            available_resource_types=available_resource_types,
            recent_modes=recent_modes,
            simulation_active=simulation_active,
        )
        return decision["resource_type_for_suggestion"] or "image"

    def _best_available_resource_mode(self, scores: dict, available: set[str]) -> str:
        resource_modes = ["simulation", "image", "video", "exam"]
        valid_modes = [mode for mode in resource_modes if not available or mode in available]
        if not valid_modes:
            return "image"
        return max(valid_modes, key=lambda mode: scores.get(mode, -999))

    def _detect_explicit_mode(self, text: str) -> str | None:
        whiteboard_patterns = [
            r"\bdessine[rz]?\b",
            r"\bdessin[es]?\b",
            r"\btableau\b",
            r"explique avec sch[ée]ma",
            r"fais un sch[ée]ma",
            r"dessine[- ]?moi",
            r"\bsch[ée]matis",
            r"\bsch[ée]ma\b",
            r"\bschema\b",
            r"\bdiagramme\b",
            r"\bcourbe\b",
            r"\btracer?\b",
            r"\btrace[rz]?\b",
            r"graphique",
            r"graphe",
            r"\b[ée]cris\b",
            r"\b[ée]crire\b",
            r"\bmontre[rz]?\b.*\b(formule|equation|équation|tableau)",
            r"interpr[ée]tation\s+chromosomique",
            r"\b[ée]chiquier\b",
            r"\bpunnet",
            r"\bcroisement\b",
        ]
        if any(re.search(pattern, text) for pattern in whiteboard_patterns):
            return "whiteboard"

        simulation_patterns = [
            r"\bsimulation\b",
            r"\bsimulateur\b",
            r"\binteractive\b",
            r"\banim[ée]e?\b",
            r"montre.*simulation",
            r"voir.*simulation",
            r"essaie.*simulation",
        ]
        if any(re.search(pattern, text) for pattern in simulation_patterns):
            return "simulation"

        exam_patterns = [
            r"interface d[' ]examen",
            r"interface d[' ]exam",
            r"comme dans l[' ]examen",
            r"ouvre l[' ]examen",
            r"sujet bac",
            r"bac national",
            r"exam national",
            r"exercice.*\bbac\b",
            r"\bbac\b.*exercice",
            r"\bbac\b.*\b20\d{2}\b",
            r"\bexamen\b.*\b20\d{2}\b",
        ]
        if any(re.search(pattern, text) for pattern in exam_patterns):
            return "exam"

        keyword_groups = [
            ("video", ["vidéo", "video", "film", "capsule"]),
            ("image", ["image", "illustration", "photo"]),
            ("exercise", ["exercice", "exercices", "application", "entrainement"]),
            ("evaluation", ["évaluation", "evaluation", "qcm", "test", "quiz"]),
            ("exam", ["examen", "exam national", "sujet d'examen"]),
        ]
        for mode, keywords in keyword_groups:
            if any(keyword in text for keyword in keywords):
                return mode
        return None

    def _infer_concept_type(self, text: str) -> str:
        dynamic_keywords = [
            "cycle", "respiration", "fermentation", "glycolyse", "réplication", "replication",
            "transcription", "traduction", "mitose", "méiose", "meiose", "subduction",
            "collision", "mouvement", "formation", "processus", "mécanisme", "mecanisme",
        ]
        structural_keywords = [
            "structure", "organisation", "schéma", "schema", "muscle", "sarcomère", "sarcomere",
            "adn", "chromosome", "cellule", "mitochondrie", "roche",
        ]
        comparative_keywords = ["différence", "difference", "compare", "comparaison", "versus", "vs"]
        assessment_keywords = ["évaluation", "evaluation", "test", "qcm", "quiz"]
        exercise_keywords = ["exercice", "application", "entrainement", "problème", "probleme"]

        if any(keyword in text for keyword in assessment_keywords):
            return "assessment"
        if any(keyword in text for keyword in exercise_keywords):
            return "exercise_practice"
        if any(keyword in text for keyword in comparative_keywords):
            return "comparative"
        if any(keyword in text for keyword in dynamic_keywords):
            return "dynamic_process"
        if any(keyword in text for keyword in structural_keywords):
            return "structural_visual"
        return "causal_mechanism"


resource_decision_service = ResourceDecisionService()
