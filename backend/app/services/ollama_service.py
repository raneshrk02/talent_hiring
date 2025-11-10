"""Deprecated OllamaService.

This file is retained for reference only after migrating to Groq.
Prefer using `GroqService` in `groq_service.py`.
"""

import requests
import logging
from ..config import settings
from ..system_prompt import SYSTEM_PROMPT, TECHNICAL_QUESTION_PROMPT

import os
from dotenv import load_dotenv
load_dotenv()

class OllamaService:
    def __init__(self):
        self.base_url = os.getenv("OLLAMA_BASE_URL")
        self.model = os.getenv("OLLAMA_MODEL")
    
    def generate_response(self, prompt: str, context: str = None) -> str:
        system_context = context if context else SYSTEM_PROMPT
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "system": system_context,
            "stream": False
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        except Exception as e:
            logging.error(f"Ollama Llama2 error: {e}")
            return "Sorry, the AI assistant is currently unavailable due to a technical issue. Please try again in a moment."
    
    def generate_question(self, skill: str, difficulty: str = "intermediate") -> str:
        prompt = TECHNICAL_QUESTION_PROMPT.format(skill=skill)
        return self.generate_response(prompt)