"""
Spaced Repetition Service
Implements the SM-2 algorithm for optimal review scheduling.
"""
from datetime import date, timedelta
from typing import Optional


class SpacedRepetitionService:
    """
    SM-2 Algorithm Implementation:
    - quality: 0-5 rating of recall quality
      0: Complete blackout
      1: Incorrect, but remembered upon seeing answer
      2: Incorrect, but answer seemed easy to recall
      3: Correct with serious difficulty
      4: Correct with some hesitation
      5: Perfect recall
    """

    def calculate_next_review(
        self,
        repetition_number: int,
        ease_factor: float,
        interval_days: int,
        quality: int,
    ) -> dict:
        """Calculate next review date and updated parameters."""
        quality = max(0, min(5, quality))

        if quality < 3:
            # Failed recall - reset
            new_repetition = 0
            new_interval = 1
        else:
            if repetition_number == 0:
                new_interval = 1
            elif repetition_number == 1:
                new_interval = 3
            else:
                new_interval = round(interval_days * ease_factor)
            new_repetition = repetition_number + 1

        # Update ease factor
        new_ease = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease = max(1.3, new_ease)  # Minimum ease factor

        next_review = date.today() + timedelta(days=new_interval)

        return {
            "next_review_date": next_review,
            "repetition_number": new_repetition,
            "ease_factor": round(new_ease, 2),
            "interval_days": new_interval,
            "last_review_quality": quality,
        }

    def quality_from_performance(
        self,
        is_correct: bool,
        hints_used: int,
        time_taken_seconds: int,
        estimated_time_seconds: int,
    ) -> int:
        """Estimate SM-2 quality rating from exercise performance."""
        if not is_correct:
            return 1 if hints_used == 0 else 0

        # Correct answer
        time_ratio = time_taken_seconds / max(estimated_time_seconds, 1)

        if hints_used == 0 and time_ratio < 0.5:
            return 5  # Perfect, fast recall
        elif hints_used == 0 and time_ratio < 1.0:
            return 4  # Good recall
        elif hints_used <= 1:
            return 3  # Correct but with difficulty
        else:
            return 3  # Correct but needed multiple hints

    def get_due_reviews(self, review_items: list[dict]) -> list[dict]:
        """Filter review items that are due today or overdue."""
        today = date.today()
        return [
            item for item in review_items
            if item.get("next_review_date") and item["next_review_date"] <= today
        ]


spaced_repetition_service = SpacedRepetitionService()
