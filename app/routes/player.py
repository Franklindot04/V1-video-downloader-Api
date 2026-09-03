from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class PlayerRequest(BaseModel):
    url: str

@router.post("/player")
def get_player_info(payload: PlayerRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "is_private": info.get("is_private"),
            "is_unlisted": info.get("is_unlisted"),
            "is_family_safe": info.get("is_family_safe"),
            "is_live": info.get("is_live"),
            "live_status": info.get("live_status"),
            "availability": info.get("availability"),
            "chapters": info.get("chapters"),
            "subtitles": info.get("subtitles"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
