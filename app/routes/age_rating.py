from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class AgeRatingRequest(BaseModel):
    url: str

@router.post("/age-rating")
def get_age_rating(payload: AgeRatingRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "age_limit": info.get("age_limit"),
            "is_family_safe": info.get("is_family_safe"),
            "content_rating": info.get("content_rating"),
            "allowed_regions": info.get("allowed_regions"),
            "blocked_regions": info.get("blocked_regions"),
            "is_kids_video": info.get("is_kids_video"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
