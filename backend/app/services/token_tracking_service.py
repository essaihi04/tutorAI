"""
Token Usage Tracking Service
Records all LLM API calls (DeepSeek, Mistral, Gemini) with token counts and costs.
"""
import logging
import time
from typing import Optional
from datetime import datetime
from app.supabase_client import get_supabase_admin

logger = logging.getLogger(__name__)

# Pricing per 1M tokens (USD) - updated as of 2025
PRICING = {
    "deepseek-chat": {"input": 0.14, "output": 0.28},
    "deepseek-reasoner": {"input": 0.55, "output": 2.19},
    "mistral-ocr-latest": {"input": 1.0, "output": 1.0},
    "mistral-small-latest": {"input": 0.2, "output": 0.6},
    "pixtral-large-latest": {"input": 2.0, "output": 6.0},
    "gemini-2.5-flash-preview-tts": {"input": 0.15, "output": 0.60},
}


def _calc_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate cost in USD based on model pricing."""
    pricing = PRICING.get(model, {"input": 0.5, "output": 1.0})
    cost = (prompt_tokens * pricing["input"] + completion_tokens * pricing["output"]) / 1_000_000
    return round(cost, 6)


class TokenTrackingService:
    """Tracks token usage for all LLM API calls."""

    def __init__(self):
        self._supabase = None

    @property
    def supabase(self):
        if self._supabase is None:
            self._supabase = get_supabase_admin()
        return self._supabase

    async def record_usage(
        self,
        student_id: Optional[str],
        student_email: Optional[str],
        provider: str,
        model: str,
        endpoint: str = "chat",
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
        total_tokens: int = 0,
        request_duration_ms: int = 0,
        session_type: str = "coaching",
        metadata: Optional[dict] = None,
    ):
        """Record a single API call's token usage."""
        if total_tokens == 0:
            total_tokens = prompt_tokens + completion_tokens

        cost = _calc_cost(model, prompt_tokens, completion_tokens)

        record = {
            "student_id": student_id,
            "student_email": student_email or "",
            "provider": provider,
            "model": model,
            "endpoint": endpoint,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": total_tokens,
            "cost_usd": float(cost),
            "request_duration_ms": request_duration_ms,
            "session_type": session_type,
            "metadata": metadata or {},
        }

        try:
            self.supabase.table("token_usage").insert(record).execute()
        except Exception as e:
            logger.warning(f"Failed to record token usage: {e}")

    def start_timer(self) -> float:
        """Return current time for measuring request duration."""
        return time.time()

    def elapsed_ms(self, start: float) -> int:
        """Return elapsed milliseconds since start."""
        return int((time.time() - start) * 1000)


token_tracker = TokenTrackingService()
