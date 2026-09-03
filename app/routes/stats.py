from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class StatsRequest(BaseModel):
    url: str

@router.post("/stats")
def get_stats(payload: StatsRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "view_count": info.get("view_count"),
            "like_count": info.get("like_count"),
            "comment_count": info.get("comment_count"),
            "average_rating": info.get("average_rating"),
            "age_limit": info.get("age_limit"),
            "is_live": info.get("is_live"),
            "categories": info.get("categories"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
