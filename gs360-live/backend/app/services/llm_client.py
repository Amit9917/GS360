"""
LLM Client — delegates to DeepTutor's provider system when available,
falls back to direct OpenAI SDK.
"""

from __future__ import annotations

import logging
from typing import Any

from ..config import settings

logger = logging.getLogger("gs360.llm")


class LLMClient:
    """Unified LLM client for GS360."""

    def __init__(self) -> None:
        self._dt_client = None
        self._openai_client = None
        self.enabled = False
        self._init()

    def _init(self) -> None:
        # Try DeepTutor's LLM client first
        if settings.deeptutor_available:
            try:
                from deeptutor.services.llm import get_llm_client

                self._dt_client = get_llm_client()
                self.enabled = True
                logger.info("Using DeepTutor LLM client (model=%s)", self._dt_client.config.model)
            except Exception as exc:
                logger.warning("DeepTutor LLM init failed: %s", exc)

        # Also initialize direct OpenAI when an API key is available.
        api_key = settings.llm_api_key
        if api_key:
            try:
                from openai import OpenAI

                self._openai_client = OpenAI(api_key=api_key, base_url=settings.llm_host)
                self.enabled = True
                logger.info("Using direct OpenAI client (model=%s)", settings.llm_model)
            except Exception as exc:
                logger.warning("OpenAI client init failed: %s", exc)

    async def complete(self, prompt: str, **kwargs: Any) -> str:
        """Get a completion from the LLM."""
        if self._dt_client and hasattr(self._dt_client, "acomplete"):
            try:
                response = await self._dt_client.acomplete(prompt, **kwargs)
                return str(response)
            except Exception as exc:
                logger.warning("DeepTutor LLM call failed: %s", exc)

        if self._openai_client:
            resp = self._openai_client.chat.completions.create(
                model=settings.llm_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=kwargs.get("max_tokens", 2048),
            )
            return resp.choices[0].message.content or ""

        return "[LLM not configured — set LLM_API_KEY in .env]"

    def evaluate_answer(self, question: str, reference_answer: str) -> dict:
        """Synchronous answer evaluation."""
        if not self.enabled:
            return {"score": 0, "feedback": "LLM not configured"}

        prompt = (
            "You are an UPSC evaluator. Score this answer 0-10.\n"
            f"Question: {question}\nAnswer: {reference_answer}\n"
            "Respond as JSON: {{\"score\": <float>, \"feedback\": \"...\"}}"
        )

        if self._openai_client:
            resp = self._openai_client.chat.completions.create(
                model=settings.llm_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1024,
                temperature=0.0,
            )
            return {"live_model_used": True, "raw_response": resp.choices[0].message.content or ""}

        return {"live_model_used": False, "feedback": "Use async bridge for DeepTutor evaluation"}

