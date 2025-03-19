import os
from dotenv import load_dotenv #type:ignore

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
LLM_MODEL = "mistral-small"  
MAX_TOKENS = 1000
TEMPERATURE = 0.7

APP_TITLE = "TalentScout Hiring Assistant"
APP_DESCRIPTION = """
This AI-powered assistant will help you through the initial screening process for technology positions at TalentScout.
Please provide your information and answer the technical questions to the best of your ability.
"""

AVATAR_ASSISTANT = "https://api.dicebear.com/7.x/bottts/svg?seed=talent&backgroundColor=b6e3f4"
AVATAR_USER = "https://api.dicebear.com/7.x/personas/svg?seed=candidate"

DATA_DIR = "data"
CANDIDATE_DATA_FILE = os.path.join(DATA_DIR, "candidate_data.csv")

END_KEYWORDS = ["exit", "quit", "bye", "goodbye", "end", "stop"]

os.makedirs(DATA_DIR, exist_ok=True)