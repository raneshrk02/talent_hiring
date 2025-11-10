import logging
from llama_cpp import Llama
from ..config import settings
from ..system_prompt import SYSTEM_PROMPT, TECHNICAL_QUESTION_PROMPT

import os
from dotenv import load_dotenv
load_dotenv()

class GGUFService:
    def __init__(self):
        self.model_path = os.getenv("GGUF_MODEL_PATH")
        self.model_name = os.getenv("GGUF_MODEL_NAME", "local-llm")
        ctx_length = os.getenv("GGUF_CONTEXT_LENGTH", "4096")
        if not ctx_length or not ctx_length.strip():
            ctx_length = "4096"
        self.n_ctx = int(ctx_length)
        threads = os.getenv("GGUF_THREADS", "4")
        if not threads or not threads.strip():
            threads = "4"
        self.n_threads = int(threads)
        self.n_gpu_layers = int(os.getenv("GGUF_GPU_LAYERS", "0"))
        
        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=self.n_ctx,
                n_threads=self.n_threads,
                n_gpu_layers=self.n_gpu_layers,
                verbose=False
            )
            logging.info(f"Loaded GGUF model: {self.model_name} from {self.model_path}")
        except Exception as e:
            logging.error(f"Failed to load GGUF model: {e}")
            self.llm = None
    
    def generate_response(self, prompt: str, context: str = None) -> str:
        if not self.llm:
            return "Sorry, the AI assistant is currently unavailable. Model failed to load."
        
        system_context = context if context else SYSTEM_PROMPT
        
        formatted_prompt = f"""<|system|>
                                {system_context}
                                
                                <|user|>
                                {prompt}
                                <|assistant|>"""
        
        try:
            response = self.llm(
                formatted_prompt,
                max_tokens=512,
                temperature=0.7,
                top_p=0.9,
                stop=["<|user|>", "<|system|>"],
                echo=False
            )
            
            return response["choices"][0]["text"].strip()
        except Exception as e:
            logging.error(f"GGUF model generation error: {e}")
            return "Sorry, the AI assistant encountered an error. Please try again."
    
    def generate_question(self, skill: str, difficulty: str = "intermediate") -> str:
        prompt = TECHNICAL_QUESTION_PROMPT.format(skill=skill)
        return self.generate_response(prompt)