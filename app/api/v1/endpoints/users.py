from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import db, security
from app.models.user import User
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    password: str

@router.post("/register")
def register_user(user_in: UserCreate, db: Session = Depends(db.get_db)):

    existing_user = db.query(User).filter(User.username == user_in.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    new_user = User(
        username=user_in.username,
        hashed_password=security.get_password_hash(user_in.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"msg": "User created successfully", "id": new_user.id}
