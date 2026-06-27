from datetime import datetime
from pydantic import BaseModel, Field

class NotificationCreate(BaseModel):
    # Enforces min 1 char, max 280 chars via Pydantic validation
    content: str = Field(..., min_length=1, max_length=280, description="The announcement content")

class NotificationResponse(BaseModel):
    id: int
    content: str
    created_at: datetime

    class Config:
        from_attributes = True
