"""
Exercise Evaluator Service
Validates student answers and provides feedback.
"""
from typing import Any, Optional


class ExerciseEvaluator:
    def evaluate_qcm(self, student_answer: str, correct_answer: str) -> bool:
        """Evaluate a multiple choice answer."""
        return str(student_answer).strip().upper() == str(correct_answer).strip().upper()

    def evaluate_numeric(
        self, student_answer: float, correct_answer: float, tolerance: float = 0.01
    ) -> bool:
        """Evaluate a numeric answer with tolerance."""
        try:
            student_val = float(student_answer)
            correct_val = float(correct_answer)
            if correct_val == 0:
                return abs(student_val) <= tolerance
            return abs(student_val - correct_val) / abs(correct_val) <= tolerance
        except (ValueError, TypeError):
            return False

    def evaluate_answer(
        self,
        question_type: str,
        student_answer: Any,
        correct_answer: Any,
        tolerance: float = 0.05
    ) -> dict:
        """Evaluate any type of answer and return feedback data."""
        is_correct = False

        if question_type == "qcm":
            is_correct = self.evaluate_qcm(str(student_answer), str(correct_answer))
        elif question_type == "numeric":
            is_correct = self.evaluate_numeric(
                float(student_answer), float(correct_answer), tolerance
            )
        elif question_type == "open_text":
            # Open text answers are evaluated by the LLM
            is_correct = None  # Will be determined by AI

        return {
            "is_correct": is_correct,
            "student_answer": student_answer,
            "correct_answer": correct_answer,
            "needs_ai_evaluation": is_correct is None,
        }

    def get_hint(self, hints: list[dict], hint_level: int) -> Optional[str]:
        """Get a progressive hint based on the current hint level."""
        for hint in hints:
            if hint.get("level") == hint_level:
                return hint.get("text_fr", hint.get("text_ar", ""))
        return None

    def calculate_score(self, attempts: list[dict]) -> dict:
        """Calculate overall score from exercise attempts."""
        if not attempts:
            return {"total": 0, "correct": 0, "percentage": 0.0}

        total = len(attempts)
        correct = sum(1 for a in attempts if a.get("is_correct"))
        return {
            "total": total,
            "correct": correct,
            "percentage": round((correct / total) * 100, 1) if total > 0 else 0.0,
        }


exercise_evaluator = ExerciseEvaluator()
