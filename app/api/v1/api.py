# app/api/v1/api.py
from fastapi import APIRouter
from app.api.v1.endpoints import game, auth, users

api_router = APIRouter()

# Include the routers from the endpoint files
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(game.router, prefix="/game", tags=["game"])
api_router.include_router(users.router, prefix="/users", tags=["users"])