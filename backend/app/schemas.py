from pydantic import BaseModel
from typing import List, Optional, Dict

from typing import Any

class SendMessageRequest(BaseModel):
    userMessage: str
    currentStage: str
    candidateInfo: dict
    currentTechQuestionIndex: int

class SendMessageResponse(BaseModel):
    message: str
    nextStage: str
    updatedCandidateInfo: dict = {}
    technicalQuestion: str = ""
    isComplete: bool = False

class ChatResponse(BaseModel):
    response: str
    stage: str
    options: Optional[List[str]] = None

class CandidateData(BaseModel):
    session_id: str
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    years_experience: Optional[int] = None
    desired_position: Optional[str] = None
    location: Optional[str] = None
    tech_skills: Optional[List[str]] = None
    qa_responses: Optional[List[Dict]] = None
    english_proficiency_score: Optional[float] = None

class RejectCandidateRequest(BaseModel):
    email: str
    reason: str = "malpractice_fullscreen_exit"

class RejectCandidateResponse(BaseModel):
    success: bool
    message: str
    email: str