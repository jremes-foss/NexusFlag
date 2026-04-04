from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.db import Base
import enum

class Difficulty(enum.Enum):
    EASY = "Easy"
    MEDIUM = "Medium"
    HARD = "Hard"
    INSANE = "Insane"

class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    challenges = relationship("Challenge", back_populates="category")

class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    points = Column(Integer, default=100)
    difficulty = Column(Enum(Difficulty), default=Difficulty.MEDIUM)
    flag = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    is_custom_url = Column(Boolean, default=False)

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="challenges")
    submissions = relationship("Submission", back_populates="challenge")

class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    content = Column(String, nullable=False)
    is_correct = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    is_first_blood = Column(Boolean, default=False)

    challenge = relationship("Challenge", back_populates="submissions")
