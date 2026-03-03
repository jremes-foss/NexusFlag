from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models.challenge import Difficulty

class CategoryBase(BaseModel):
    name: str

class ChallengeBase(BaseModel):
    title: str
    description: str
    points: int = 100
    difficulty: Difficulty = Difficulty.MEDIUM
    category_id: int

class ChallengeCreate(ChallengeBase):
    flag: str

class ChallengeResponse(ChallengeBase):
    id: int
    download_url: Optional[str] = None    
    model_config = ConfigDict(from_attributes=True)

class CategoryResponse(CategoryBase):
    id: int
    challenges: List["ChallengeResponse"]
    model_config = ConfigDict(from_attributes=True)

class SubmissionCreate(BaseModel):
    challenge_id: int
    flag_input: str

class SubmissionResponse(BaseModel):
    status: str
    is_correct: bool
    new_score: int
    message: str
    model_config = ConfigDict(from_attributes=True)

CategoryResponse.model_rebuild()
