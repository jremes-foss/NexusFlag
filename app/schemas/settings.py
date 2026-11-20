from pydantic import BaseModel, Field

class RateLimitUpdate(BaseModel):
    rate_limit_enabled: bool
    login_rate_limit: str = Field(..., pattern=r"^\d+/(second|minute|hour|day)$")
    submit_rate_limit: str = Field(..., pattern=r"^\d+/(second|minute|hour|day)$")
