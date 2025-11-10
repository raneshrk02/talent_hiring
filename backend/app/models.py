from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime
import uuid

class Candidate(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: str
    phone: Optional[str] = None
    years_experience: Optional[int] = None
    desired_position: Optional[str] = None
    location: Optional[str] = None
    tech_skills: Optional[List[str]] = None
    qa_responses: Optional[List[Dict]] = None
    english_proficiency_score: Optional[float] = 0.0
    status: Optional[str] = "active"  # Can be: "active", "rejected", "completed"
    rejection_reason: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)