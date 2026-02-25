import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.v1.api import api_router
from app.api.v1.endpoints import admin
from app.core.db import engine
from app.models import user

app = FastAPI(
    title="NexusFlag API",
    description="Lightweight API for Community Capture The Flag competitions",
    version="1.0.0"
)

user.Base.metadata.create_all(bind=engine)

os.makedirs("static/challenges", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routes from your v1 router
app.include_router(api_router, prefix="/api/v1")
app.include_router(admin.router, prefix="/api/v1/admin", tags=["admin"])

@app.get("/")
async def root():
    return {"message": "System Online", "status": "Ready for exploitation"}
