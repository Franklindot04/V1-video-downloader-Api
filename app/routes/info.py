from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

from app.cache import cache_get, cache_set

router = APIRouter()

class InfoRequest(BaseModel):
    url: str

@router.post("/info", tags=["Metadata"])
def get_info(payload: InfoRequest):
    key = f"info:{payload.url}"
    cached = cache_get(key)
    if cached is not None:
        # Cache hit
        return cached

    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        result = {
            "title": info.get("title"),
            "uploader": info.get("uploader"),
            "duration": info.get("duration"),
            "description": info.get("description"),
        }

        cache_set(key, result)
        return result

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))