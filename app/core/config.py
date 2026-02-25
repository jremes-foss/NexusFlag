from app.models.challenge import Category, Challenge, Submission
from typing import Optional

STORAGE_MODE = "local"  # or "s3"
BASE_URL = "http://localhost:8000"
S3_BUCKET_URL = "https://nexusflag-assets.s3.amazonaws.com"

def get_file_url(challenge: Challenge) -> Optional[str]:
    if not challenge.file_path:
        return None
    
    if challenge.is_custom_url:
        return challenge.file_path
        
    if STORAGE_MODE == "s3":
        return f"{S3_BUCKET_URL}/{challenge.file_path}"
    else:
        return f"{BASE_URL}/static/challenges/{challenge.file_path}"
