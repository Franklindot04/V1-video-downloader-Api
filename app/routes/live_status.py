from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import yt_dlp

router = APIRouter()

class LiveStatusRequest(BaseModel):
    url: str

@router.post("/live-status")
def get_live_status(payload: LiveStatusRequest):
    try:
        ydl_opts = {
            "quiet": True,
            "skip_download": True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(payload.url, download=False)

        return {
            "is_live": info.get("is_live"),
            "live_status": info.get("live_status"),
            "was_live": info.get("was_live"),
            "availability": info.get("availability"),
            "release_timestamp": info.get("release_timestamp"),
            "live_start_time": info.get("live_start_time"),
            "live_end_time": info.get("live_end_time"),
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
