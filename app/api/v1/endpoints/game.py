from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List

from app.core.config import get_file_url
from app.core.db import get_db
from app.api.deps import get_current_admin_user
from app.api.deps import get_current_user

from app.models.user import User
from app.schemas.user import ScoreboardEntry
from app.models.challenge import Category, Challenge, Submission
from app.schemas.game import SubmissionCreate, SubmissionResponse

from app.schemas.game import (
    CategoryResponse,
    ChallengeCreate, 
    ChallengeResponse, 
    SubmissionCreate, 
    SubmissionResponse
)

router = APIRouter()

@router.post("/submit", response_model=SubmissionResponse)
def submit_flag(
    submission_in: SubmissionCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    challenge = db.query(Challenge).filter(Challenge.id == submission_in.challenge_id).first()
    if not challenge:
        raise HTTPException(status_code=404, detail="Challenge not found")

    # 1. Prevent double-scoring
    already_solved = db.query(Submission).filter(
        Submission.user_id == current_user.id,
        Submission.challenge_id == challenge.id,
        Submission.is_correct == True
    ).first()

    if already_solved:
        return SubmissionResponse(
            status="already_solved",
            is_correct=True,
            new_score=current_user.score,
            message="You've already captured this flag!"
        )

    is_correct = submission_in.flag_input.strip() == challenge.flag.strip()

    bonus_points = 0
    if is_correct:
        first_blood_exists = db.query(Submission).filter(
            Submission.challenge_id == challenge.id,
            Submission.is_correct == True
        ).first()

        if not first_blood_exists:
            bonus_points = int(challenge.points * 0.1)
            message = f"FIRST BLOOD! Correct! +{challenge.points + bonus_points} points (inc. bonus)."
        else:
            message = f"Correct! +{challenge.points} points."

        current_user.score += (challenge.points + bonus_points)
        current_user.last_solve_at = datetime.utcnow()
        db.add(current_user)
    else:
        message = "Incorrect flag. Keep trying!"

    new_submission = Submission(
        user_id=current_user.id,
        challenge_id=challenge.id,
        content=submission_in.flag_input,
        is_correct=is_correct,
        is_first_blood=(is_correct and not first_blood_exists)
    )
    db.add(new_submission)

    db.commit()
    db.refresh(current_user)

    return SubmissionResponse(
        status="correct" if is_correct else "incorrect",
        is_correct=is_correct,
        new_score=current_user.score,
        message=message
    )

@router.post("/challenges", response_model=ChallengeResponse)
def create_new_challenge(
    challenge_in: ChallengeCreate,
    db: Session = Depends(get_db),
    admin_user: User = Depends(get_current_admin_user) 
):
    new_challenge = Challenge(
        title=challenge_in.title,
        description=challenge_in.description,
        flag=challenge_in.flag,
        points=challenge_in.points,
        category_id=challenge_in.category_id,
        difficulty=challenge_in.difficulty
    )
    db.add(new_challenge)
    db.commit()
    db.refresh(new_challenge)
    return new_challenge

@router.get("/challenges", response_model=List[CategoryResponse])
def list_challenges(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = db.query(Category).all()
    for cat in categories:
        for chal in cat.challenges:
            chal.download_url = get_file_url(chal)

    return categories

@router.get("/scoreboard", response_model=List[ScoreboardEntry])
def get_scoreboard(
    db: Session = Depends(get_db),
    limit: int = 50
):
    users = db.query(User) \
             .order_by(
                 User.score.desc(),
                 User.last_solve_at.asc()
            ) \
             .limit(limit) \
             .all()

    return users
