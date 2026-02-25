from app.api.deps import get_current_user
from fastapi import APIRouter, HTTPException, APIRouter, Depends
from pydantic import BaseModel

router = APIRouter()

class Submission(BaseModel):
    challenge_id: int
    flag: str

@router.post("/submit")
async def submit_flag(submission: Submission):

    if submission.flag == "CTF{placeholder}":
        return {"status": "correct", "points": 100}
    
    raise HTTPException(status_code=400, detail="Invalid Flag")

@router.get("/secret-challenge")
async def get_challenge(current_user: dict = Depends(get_current_user)):
    """
    Only authenticated players can see this.
    """
    return {
        "challenge_name": "Ghost in the API",
        "points": 500,
        "hint": f"Good luck, {current_user['username']}!"
    }
