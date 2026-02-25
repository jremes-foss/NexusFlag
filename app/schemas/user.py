from pydantic import BaseModel, ConfigDict

class ScoreboardEntry(BaseModel):
    username: str
    score: int
    
    model_config = ConfigDict(from_attributes=True)
