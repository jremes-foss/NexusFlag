import os
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.models.challenge import Challenge
from app.models.user import User
from app.api.deps import get_current_admin_user

router = APIRouter()

# The directory where local files are saved
UPLOAD_DIR = "static/challenges"

@router.post("/challenges/{challenge_id}/upload")
async def upload_challenge_file(
    challenge_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user)
):

    challenge = db.query(Challenge).filter(Challenge.id == challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")
        
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
        
    challenge.file_path = file.filename
    challenge.is_custom_url = False # Mark as local storage
    db.commit()
    
    return {
        "filename": file.filename,
        "challenge_id": challenge_id,
        "status": "successfully uploaded"
    }
