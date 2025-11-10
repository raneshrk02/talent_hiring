import logging
import os
from typing import Optional, List
from dotenv import load_dotenv

from groq import Groq  # type: ignore

from ..system_prompt import SYSTEM_PROMPT, TECHNICAL_QUESTION_PROMPT

load_dotenv()


class GroqService:
    """LLM service backed by Groq's hosted models.

    Expects environment variables:
      - GROQ_API: API key string
                    - GROQ_MODEL: Optional model name (auto-selected if not set)
    """

    def __init__(self):
        self.api_key = os.getenv("GROQ_API")
        if not self.api_key:
            logging.warning("GROQ_API is not set; GroqService will not function without it.")

        # If model not provided, will auto-select from available Groq models
        env_model = os.getenv("GROQ_MODEL") or "llama-3.1-8b-instant"
        self.model: Optional[str] = env_model if env_model and env_model.strip() else None

        try:
            self.client = Groq(api_key=self.api_key)
        except Exception as e:
            logging.error(f"Failed to initialize Groq client: {e}")
            self.client = None

    def _complete(self, model: str, prompt: str, system_context: str) -> str:
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_context},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=512,
            top_p=0.9,
            stream=False,
        )
        text = completion.choices[0].message.content if completion.choices else ""
        return (text or "").strip()

    def _list_models(self) -> List[str]:
        try:
            models = self.client.models.list()
            # SDK returns object with .data similar to OpenAI; be defensive
            ids: List[str] = []
            data = getattr(models, "data", None) or []
            for m in data:
                # m may be dict-like or object with id attr
                mid = getattr(m, "id", None) or (m.get("id") if isinstance(m, dict) else None)
                if isinstance(mid, str):
                    ids.append(mid)
            return ids
        except Exception as e:
            logging.error(f"GroqService failed to list models: {e}")
            return []

    def _pick_supported_model(self, available: Optional[List[str]] = None) -> Optional[str]:
        if available is None:
            available = self._list_models()
        if not available:
            return None

        # Prefer up-to-date Llama or Gemma chat-capable models
        preferences = [
            # Newer Llama variants first
            "llama-\d", "llama3", "llama-", "llama",
            # Then Gemma
            "gemma", "gemma2",
            # As a broad fallback, anything else
            ""
        ]

        def score(model_id: str) -> int:
            s = 0
            lower = model_id.lower()
            # Rank by family
            if "llama-3.1-8b-instant" in lower:
                s += 150  # hard preference for requested model
            elif "llama" in lower:
                s += 100
            if "gemma" in lower:
                s += 80
            # Prefer instruction/assistant tuned variants
            for tag in ("instruct", "it", "instant", "versatile"):
                if tag in lower:
                    s += 20
            # Prefer larger context length or newer versions heuristically
            for tag in ("70b", "405b", "9b", "11b", "32k", "128k", "8192"):
                if tag in lower:
                    s += 5
            return s

        ranked = sorted(available, key=score, reverse=True)
        return ranked[0] if ranked else None

    def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate a completion using Groq Chat Completions API with fallbacks."""
        if not self.client:
            return (
                "Sorry, the AI assistant is currently unavailable due to a configuration issue. "
                "Please try again later."
            )

        system_context = context if context else SYSTEM_PROMPT

        # Ensure we have a current model id; auto-select if missing
        if not self.model:
            selected = self._pick_supported_model()
            if selected:
                logging.info(f"GroqService auto-selected model: {selected}")
                self.model = selected
            else:
                return (
                    "Sorry, the AI assistant is currently unavailable due to a configuration issue. "
                    "No supported Groq models were found."
                )

        # Try the configured/selected model first
        try:
            return self._complete(self.model, prompt, system_context)
        except Exception as e:
            msg = str(e)
            logging.error(f"Groq generate_response error with model '{self.model}': {msg}")

            # If the model is decommissioned or invalid, query models and retry with best candidate
            decommissioned = "model_decommissioned" in msg or "decommissioned" in msg.lower()
            invalid = "invalid_request_error" in msg or "not found" in msg.lower()

            if decommissioned or invalid:
                available = self._list_models()
                # Remove current model if present
                available = [m for m in available if m != self.model]
                alt = self._pick_supported_model(available)
                if alt:
                    try:
                        logging.info(f"GroqService retrying with discovered model: {alt}")
                        self.model = alt
                        return self._complete(alt, prompt, system_context)
                    except Exception as e2:
                        logging.error(f"Groq discovered model '{alt}' failed: {e2}")

        # Final failure case
        return (
            "Sorry, the AI assistant is currently unavailable due to a technical issue. "
            "Please try again in a moment."
        )

    def generate_question(self, skill: str, difficulty: str = "intermediate") -> str:
        prompt = TECHNICAL_QUESTION_PROMPT.format(skill=skill)
        return self.generate_response(prompt)
